#!/usr/bin/env python
"""Three-state detector vote, box attachment, replayed verification and the recall funnel (VSPS H1).

    python scripts/vsps_h1/vote.py --records <stage-1 dir> --boxes <boxes.jsonl> --out <scratch dir>

Per entity (detector outputs from detect_boxes.py):
    unmapped noun (no prompt)          -> UNCERTAIN
    GroundingDINO and OWLv2 both find  -> SUPPORTED, entity gets a box
    neither finds                      -> REFUTED
    one finds                          -> UNCERTAIN
Entities sharing a prompt take distinct GroundingDINO boxes in score order; one
that finds none left keeps no box. Only SUPPORTED entities get a box.

The verifier is NOT rerun on a GPU: Stage 1 recorded every probe answer, so
`verify` is replayed (rescap.vlm.replay, as scripts/validate_replay.py does) on
the same records under three conditions over the same image set:
    R0  baseline : no boxes, no votes (v1 rule)
    R1  boxes    : boxes attached, spatial_verification on, absent box = ⊥
    R2  H1       : R1 + the detector vote on existence (verify.detector_vote);
                   registered as a "GroundingDINO-led vote" (PREREG §2)
    R3  falsifier: R1 + every entity R1 left UNCERTAIN promoted, no detector vote
                   (CC-198 ruling 6; descriptive, gates only a judge read)
Detector lines must all carry the pinned config/map sha and one device (CC-198 W1).
Each condition's records go to <out>/<cond>/ and scripts/recall_funnel.py runs
on them. <out> must be outside the repo: the records carry reference captions.
Writes <out>/summary.json with the prereg metrics and the GO/STOP verdict.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HERE))

GO_RECALL_GAIN = 5.0     # points of supported-stage recall, R2 - R0
GO_PRECISION_DROP = 2.0  # max points of supported-stage precision lost, R0 - R2
R3_PRECISION_MARGIN = 2.0  # GO with R2 - R3 supported P below this -> judge read
CONDITIONS = ("R0", "R1", "R2", "R3")


def vote(gdino: list, owlv2: list, mapped: bool) -> str:
    if not mapped:
        return "UNCERTAIN"
    if gdino and owlv2:
        return "SUPPORTED"
    if not gdino and not owlv2:
        return "REFUTED"
    return "UNCERTAIN"


def votes_and_boxes(det: dict) -> tuple[dict[str, str], dict[str, list[float]]]:
    """Entity id -> vote, and entity id -> [x, y, w, h] for SUPPORTED entities."""
    votes, boxes = {}, {}
    used: Counter[str] = Counter()
    for eid, prompt in det["entities"].items():
        hits = (det["prompts"].get(prompt) or {}) if prompt else {}
        votes[eid] = vote(hits.get("gdino") or [], hits.get("owlv2") or [], bool(prompt))
        if votes[eid] == "SUPPORTED":
            ranked = sorted(hits["gdino"], key=lambda b: -b[4])
            if used[prompt] < len(ranked):
                boxes[eid] = ranked[used[prompt]][:4]
                used[prompt] += 1
    return votes, boxes


def promote_uncertain_votes(r1: dict) -> dict[str, str]:
    """R3: a SUPPORTED vote for every entity whose existence R1 left UNCERTAIN; REJECTED stays."""
    return {p["subject"]["entity_id"]: "SUPPORTED" for p in r1["propositions"]
            if p["type"] == "entity" and (p.get("verification") or {}).get("status") == "UNCERTAIN"}


def replay(record: dict, cond: str, det: dict, sizes: dict, r1: dict | None = None) -> dict:
    from rescap.pipeline.verify import VerificationConfig, verify
    from rescap.vlm.replay import ReplayVLM
    from validate_replay import _SizeOnly

    rec = copy.deepcopy(record)
    for p in rec["propositions"]:
        p["verification"] = {"status": None}
    votes, boxes = votes_and_boxes(det)
    if cond != "R0":
        for e in rec["entities"]:
            if e["id"] in boxes:
                e["bbox"] = boxes[e["id"]]
    models = Counter(str(pr.get("model", "")) for p in record["propositions"]
                     for pr in ((p.get("evidence") or {}).get("probes") or []))
    if not models:
        return rec
    verifier = models.most_common(1)[0][0]
    second = [m for m in models if m != verifier]
    config = VerificationConfig() if cond == "R0" else VerificationConfig(absent_bbox_is_evidence=False)
    verify(ReplayVLM(record["propositions"], model_name=verifier),
           _SizeOnly(sizes[rec["file_name"]]) if rec["file_name"] in sizes else None,
           rec["entities"], rec["propositions"], config=config,
           colour_verifier=ReplayVLM(record["propositions"], model_name=second[0]) if second else None,
           entity_votes={"R2": votes, "R3": promote_uncertain_votes(r1) if r1 else None}.get(cond))
    return rec


def funnel(records_dir: Path) -> dict[str, dict[str, float]]:
    out = subprocess.run([sys.executable, str(ROOT / "scripts" / "recall_funnel.py"), "--in", str(records_dir)],
                         capture_output=True, text=True, check=True).stdout
    return {m[1]: {"P": float(m[2]), "R": float(m[3])}
            for m in re.finditer(r"^(\w+)\s+P=\s*([\d.]+)\s+R=\s*([\d.]+)", out, re.M)}


def entity_reference_precision(records: list[dict]) -> float | None:
    """Of the lexicon objects named by SUPPORTED entity propositions, the share the references name."""
    from rescap.chair import objects_in

    hit = named = 0
    for rec in records:
        gold = set().union(*[set(objects_in(c)) for c in rec["reference_captions"]])
        for p in rec["propositions"]:
            if p["type"] == "entity" and (p.get("verification") or {}).get("status") == "SUPPORTED":
                objs = set(objects_in(p["text_vi"]))
                hit += len(objs & gold)
                named += len(objs)
    return round(100 * hit / named, 2) if named else None


def spatial_shares(records: list[dict]) -> dict[str, float]:
    """Spatial propositions: share not UNCERTAIN, and share the bbox geometry decided."""
    props = [p for r in records for p in r["propositions"] if p["type"] == "spatial_relation"]
    n = max(1, len(props))
    return {
        "n": len(props),
        "left_uncertain": round(sum((p.get("verification") or {}).get("status") != "UNCERTAIN" for p in props) / n, 4),
        "geometry_decided": round(sum(
            ((p.get("spatial_relation") or {}).get("geometric_check") or {}).get("consistent") is not None
            for p in props) / n, 4),
    }


def supported_recall(records: list[dict]) -> float | None:
    """recall_funnel's `supported` R (mean per-image |M & G| / |G|), in process, for a subset of images."""
    from rescap.chair import objects_in

    recalls = []
    for rec in records:
        gold = set().union(*[set(objects_in(c)) for c in rec["reference_captions"]])
        if gold:
            named = set().union(*[set(objects_in(p["text_vi"])) for p in rec["propositions"]
                                  if (p.get("verification") or {}).get("status") == "SUPPORTED"])
            recalls.append(len(named & gold) / len(gold))
    return round(100 * sum(recalls) / len(recalls), 2) if recalls else None


def decision(fun: dict, complete: bool = True, subset_gain: float | None = None) -> dict:
    """GO/STOP per PREREG §5; INCOMPLETE (no verdict) unless every registered image has a valid detector line.
    A GO goes to a judge read before any Phase B prereg if R2 beats R3 on precision by < 2.0 (CC-198 ruling 6)
    or the recall gain on exactly-replayed images is < +5.0 (W3)."""
    if not complete:
        return {"verdict": "INCOMPLETE"}
    gain = fun["R2"]["supported"]["R"] - fun["R0"]["supported"]["R"]
    drop = fun["R0"]["supported"]["P"] - fun["R2"]["supported"]["P"]
    margin = fun["R2"]["supported"]["P"] - fun["R3"]["supported"]["P"]
    go = gain >= GO_RECALL_GAIN and drop <= GO_PRECISION_DROP
    judge = []
    if go and margin < R3_PRECISION_MARGIN:
        judge.append("R2-R3 supported precision < +2.0")
    if go and (subset_gain is None or subset_gain < GO_RECALL_GAIN):
        judge.append("recall gain on exact-replay images < +5.0")
    return {"recall_gain_pts": round(gain, 2), "precision_drop_pts": round(drop, 2),
            "r2_minus_r3_precision_pts": round(margin, 2), "exact_replay_recall_gain_pts": subset_gain,
            "verdict": "GO" if go else "STOP", "judge_read_required": judge}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--records", required=True, type=Path)
    ap.add_argument("--boxes", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--expect", type=int, default=3700, help="registered image count; fewer gives INCOMPLETE")
    args = ap.parse_args()
    out = args.out.resolve()
    if out.is_relative_to(ROOT):
        raise SystemExit("CUSTODY STOP: --out is inside the repo; re-verified records carry reference captions")

    from validate_replay import _load_sizes

    sizes = _load_sizes()
    from detect_boxes import file_sha, read_lines

    dets = read_lines(args.boxes, file_sha(HERE / "config.json"), file_sha(HERE / "vi_en_map.json"))
    files = sorted(args.records.glob("*.json"))
    exact: set[str] = set()  # image ids whose R0 entity verdicts equal the recorded ones (W3)
    stats: dict[str, Counter] = {c: Counter() for c in CONDITIONS}
    agree = Counter()
    kept: dict[str, list[dict]] = {c: [] for c in CONDITIONS}
    for f in files:
        record = json.loads(f.read_text(encoding="utf-8"))
        det = dets.get(record["image_id"])
        if det is None:
            continue
        for eid, v in votes_and_boxes(det)[0].items():
            prompt = det["entities"][eid]
            agree["mapped" if prompt else "unmapped"] += 1
            if prompt:
                agree[v] += 1
                agree["gdino_positive"] += bool(det["prompts"][prompt]["gdino"])
                agree["owlv2_positive"] += bool(det["prompts"][prompt]["owlv2"])
        done: dict[str, dict] = {}
        for cond in CONDITIONS:
            rec = done[cond] = replay(record, cond, det, sizes, done.get("R1"))
            (out / cond).mkdir(parents=True, exist_ok=True)
            (out / cond / f.name).write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
            kept[cond].append(rec)
            for p in rec["propositions"]:
                st = (p.get("verification") or {}).get("status")
                stats[cond][f"{p['type']}:{st}"] += 1
        if all(a["verification"]["status"] == (b.get("verification") or {}).get("status")
               for a, b in zip(done["R0"]["propositions"], record["propositions"]) if a["type"] == "entity"):
            exact.add(record["image_id"])
    if not kept["R0"]:
        raise SystemExit("no record has a detector line")
    complete = len(kept["R0"]) == len(files) == args.expect
    sub_r = {c: supported_recall([r for r in kept[c] if r["image_id"] in exact]) for c in ("R0", "R2")}
    subset_gain = round(sub_r["R2"] - sub_r["R0"], 2) if None not in sub_r.values() else None

    fun = {c: funnel(out / c) for c in CONDITIONS}
    for c in CONDITIONS:  # the in-process recall must reproduce recall_funnel before it is trusted on a subset
        if abs(supported_recall(kept[c]) - fun[c]["supported"]["R"]) > 0.051:
            raise SystemExit(f"supported_recall disagrees with recall_funnel on {c}")
    mapped = agree["mapped"] or 1
    summary = {
        "n_images": len(kept["R0"]),
        "funnel": fun,
        "entity_reference_precision": {c: entity_reference_precision(kept[c]) for c in CONDITIONS},
        "spatial": {c: spatial_shares(kept[c]) for c in CONDITIONS},
        "detector_agreement_rate": round((agree["SUPPORTED"] + agree["REFUTED"]) / mapped, 4),
        "entity_votes": dict(agree),
        "detector_positive_rate": {d: round(agree[f"{d}_positive"] / mapped, 4) for d in ("gdino", "owlv2")},
        "verdicts": {c: dict(stats[c]) for c in CONDITIONS},
        "exact_replay_images": len(exact),
        "exact_replay_supported_recall": sub_r,
        "decision": decision(fun, complete, subset_gain),
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("n_images", "funnel", "entity_reference_precision",
                                              "spatial", "detector_agreement_rate", "detector_positive_rate", "exact_replay_images",
                                              "decision")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
