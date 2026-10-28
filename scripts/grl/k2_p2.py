#!/usr/bin/env python3
"""K2 P2 dev pilot, CPU part (K2_GATE0_RULE.md §6c; CC-136P W2-W4, W10, W13): gold editor vs detector editor on the
Gate 0 val-924 zero-shot decodes. TARGET CEILING ONLY: E_gold is edited with the gold that scores it.

    python3 scripts/grl/k2_p2.py --selftest                                         CPU, synthetic rows
    python3 scripts/grl/k2_p2.py repro  --k2-dir K2 --out-dir K2/p2                 M3 CPU: W3 before the GPU step
    python3 scripts/grl/k2_p2.py decide --k2-dir K2 --detect P2_DETECT --out-dir K2/p2   M3 CPU: W3, E_det, decide
    python3 scripts/grl/k2_p2.py notrun --class cost|fault --why TEXT --out-dir K2/p2

W3: the Gate 0 record and decode are sha-asserted, and E_gold is recomputed with k2_gate0's untruncate / edit / row /
rates (imported, not copied) and must equal the stored values; a mismatch is NOT RUN (fault), never a look, and the
detector output is not opened. Only then E_det = edit(c, D(img)). GO (W9, unchanged): CHAIR_i(E_det) - CHAIR_i(E_gold)
>= 6.0 or R(E_gold) - R(E_det) >= 4.0. Records go to p2/ only; gate0_decide.json is never written (W2).
One look (W13): the look is p2_decide.json. A fault writes P2_FAULT_<utc>.md only, so a fault rerun stays possible
until p2_decide.json exists; a cost NOT RUN, a GO and a NO-GO write p2_decide.json and close the pilot.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import common as K  # noqa: E402
import k2_gate0 as KG  # noqa: E402
import reward as RW  # noqa: E402
from k2_p2_detect import COCO80  # noqa: E402

GATE0_SHA = "0b6da7e083af7da3d2cc7c7584c9888007c0ec33d9b8b58d2ecd763b324317a5"  # OPS-1028c / LOG 18:49:30Z
DECODE_SHA = "8bb0192c76c1a52df883d2a03333062f7e4fde0d08813a919a36d179f50e0c51"  # gate0_decide.json decode_sha256
DECODE = "k2g0_qwen3vl_8b_val-detailed.preds.json"
#: CC-136 W3 / OPS-1028c, at the precision the LOG gives (decimals); the stored record binds at its own 4 decimals
REPRO = {"CHAIR_i": (1.795, 3), "R": (65.28, 2), "deleted_units": 277}
GO = {"chair": 2 * KG.G["sesoi_chair_i"], "recall": 2 * KG.G["margin_recall"]}  # 6.0 and 4.0 (CC-126 W9)
LABEL = "K2 P2 dev pilot (§6c): TARGET CEILING ONLY (val gold edits and scores E_gold); never a method result"
H_P2 = "H-P2 (K14 l.130): gold-student CHAIR_i lower by >= 3.0, recall margin -2.0"
H_P2R = "H-P2r: gold-student R higher by >= 2.0, CHAIR_i non-inferior at margin +1.0"
FULL_P2 = ("no GO by itself licenses the full P2 run: it still needs a K2 Gate 1 GO, the MT4 prereg and a fresh cost "
           "ruling (CC-136P W4)")
RECORDS = ("p2_decide.json", "P2_VERDICT.md", "P2_STOP.md")


class Fault(SystemExit):
    """NOT RUN (fault) -> TO-PI: never a negative pilot."""


# ------------------------------------------------------------------------------------------------ records (W2)
def write(p: Path, text: str) -> None:
    """The one writer: never gate0_decide.json, never after p2_decide.json exists (one look, W13)."""
    if p.name == "gate0_decide.json" or not (p.name in RECORDS or re.fullmatch(r"P2_FAULT_\d{8}T\d{6}Z\.md", p.name)):
        raise SystemExit(f"REFUSED: P2 writes only {RECORDS} and P2_FAULT_<utc>.md, not {p.name}")
    if (p.parent / "p2_decide.json").exists() or p.exists():
        raise SystemExit(f"REFUSED: p2_decide.json or {p.name} already exists in {p.parent} (one look)")
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".part")
    tmp.write_text(text)
    os.replace(tmp, p)


def records(out: Path, rec: dict) -> None:
    """p2_decide.json and its markdown, written together (the markdown first, so one look holds for both)."""
    md = "P2_VERDICT.md" if rec["verdict"] == "P2-GO" else "P2_STOP.md"
    head = {"P2-GO": f"# K2 P2 GO ({rec.get('fired_arm')} arm, {rec.get('driver') or 'R'}-driven): licenses drafting "
                     f"only; {FULL_P2}",
            "P2-NO-GO": "# K2 P2 NO-GO: pre-registered negative dev pilot; no rerun, no threshold or detector change",
            "NOT-RUN": f"# K2 P2 NOT RUN ({rec.get('class')}); not a negative pilot"}[rec["verdict"]]
    body = json.dumps(rec, indent=1, default=float)
    write(out / md, f"{head}\n\n- {LABEL}\n\n```json\n{body}\n```\n")
    (out / "p2_decide.json").write_text(body + "\n")


def notrun(out: Path, cls: str, why: str) -> dict:
    """cost: final, p2_decide.json + P2_STOP.md. fault: P2_FAULT_<utc>.md only (no look; a logged rerun may follow)."""
    rec = {"verdict": "NOT-RUN", "class": f"{cls} -> TO-PI", "why": why, "label": LABEL}
    if cls == "cost":
        records(out, rec)
    else:
        from datetime import datetime, timezone

        name = f"P2_FAULT_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.md"
        write(out / name, f"# K2 P2 NOT RUN (fault -> TO-PI); not a look, not a negative pilot\n\n- {why}\n")
        rec["record"] = name
    return rec


# ------------------------------------------------------------------------------------------------ W3
def pinned_file(p: Path, want: str) -> Path:
    if K.sha_file(p) != want:
        raise Fault(f"FAULT: {p.name} sha256 is not {want[:8]} (W3)")
    return p


def targets(p: dict, ids: list[int], presence: dict, gold: dict, refs: dict) -> tuple[list, list, list]:
    """k2_gate0.cmd_score's loop with the presence set as the only parameter: (zero-shot rows, edited rows, deleted
    units per image)."""
    zs, ed, gone = [], [], []
    for i in ids:
        c = KG.untruncate(p["predictions"][str(i)], p["hit_max"][str(i)])
        e, d = KG.edit(c, presence[i])
        gu = gold[i] | refs.get(i, set())
        zs.append(KG.row(c, gold[i], gu) | {"gold": gold[i]})
        ed.append(KG.row(e, gold[i], gu) | {"gold": gold[i]})
        gone.append(d)
    return zs, ed, gone


def reproduce(p: dict, stored: dict, ids: list[int], gold: dict, refs: dict, want: dict = REPRO) -> tuple:
    """W3: Gate 0 GO with fired [] and P1-GO (CC-136 W6), then E_gold recomputed equals the stored record at its 4
    decimals and the LOG constants at theirs. Raises Fault otherwise."""
    bad = []
    p1 = stored["p1_truncation_frontier"]["verdict"] if "p1_truncation_frontier" in stored else None
    if stored.get("verdict") != "GO" or stored.get("fired") != [] or p1 != "P1-GO":
        bad.append("precondition: Gate 0 GO, fired [], P1-GO")
    zs, ed, gone = targets(p, ids, gold, gold, refs)
    f = lambda x: round(float(x), 4)  # noqa: E731  k2_gate0.decide's rounding
    for name, rows in (("zero_shot", zs), ("edited", ed)):
        got = {k: f(v) for k, v in KG.rates(rows).items()}
        bad += [f"{name}.{k} {got[k]} != {v}" for k, v in stored[name].items() if got.get(k) != v]
    n_gone = sum(map(len, gone))
    if n_gone != stored["deleted_units"]:
        bad.append(f"deleted_units {n_gone} != {stored['deleted_units']}")
    for k in ("CHAIR_i", "R"):
        v, dec = want[k]
        if round(stored["edited"][k], dec) != v:
            bad.append(f"stored edited.{k} {stored['edited'][k]} is not {v} (CC-136 W3)")
    if stored["deleted_units"] != want["deleted_units"]:
        bad.append(f"stored deleted_units {stored['deleted_units']} is not {want['deleted_units']}")
    if bad:
        raise Fault("FAULT: W3 reproduction failed: " + "; ".join(bad))
    return zs, ed, gone


# ------------------------------------------------------------------------------------------------ decide
def arm(d_chair: float, d_recall: float) -> str:
    """The GO rule on point estimates: chair, recall, both or none."""
    a = d_chair >= GO["chair"], d_recall >= GO["recall"]
    return {(True, True): "both", (True, False): "chair", (False, True): "recall", (False, False): "none"}[a]


def presence_pr(D: dict, gold: dict, ids: list[int]) -> dict:
    """Pooled image-class precision and recall of D against gold (descriptive)."""
    tp = sum(len(set(D[i]) & gold[i]) for i in ids)
    nd, ng = sum(len(D[i]) for i in ids), sum(len(gold[i]) for i in ids)
    return {"precision": round(100 * tp / max(nd, 1), 4), "recall": round(100 * tp / max(ng, 1), 4),
            "mean_classes_per_image": round(nd / len(ids), 4)}


def unit_stats(gone: list[list[str]]) -> dict:
    """Deleted units and the negated-or-hedged share, as k2_gate0.decide counts them."""
    units = [u for d in gone for u in d]
    neg = [bool(RW.NEG_RE.search(u) or RW.unasserted(u)[1]) for u in units]
    return {"deleted_units": len(units), "negated_or_hedged_share": round(float(np.mean(neg)), 4) if units else 0.0}


def licence(fired: str, driver: str | None, hw: dict) -> dict:
    """CC-136P W4: a CHAIR-arm fire licenses H-P2 only if hallucinations drive it (sum hal(E_det) > sum hal(E_gold));
    otherwise it is recall-driven and, like an R-only GO, licenses H-P2r as a secondary only."""
    if fired == "none":
        return {"primary": None, "secondary": None, "note": "NO-GO: no licence for a full P2"}
    chair_h = fired in ("chair", "both") and driver == "hallucination"
    out = {"primary": H_P2 if chair_h else None, "secondary": H_P2R, "note": FULL_P2}
    wide = [a for a, k, m in (("chair", "half_width_CHAIR_i", KG.G["sesoi_chair_i"]),
                              ("recall", "half_width_R", KG.G["margin_recall"])) if fired in (a, "both") and hw[k] >= m]
    if wide:
        out["half_width"] = f"the {' and '.join(wide)} arm's 95% half-width is >= its SESOI (reported, not a rule)"
    return out


def decide(ed_gold: list, ed_det: list, gone_gold: list, gone_det: list, extra: dict) -> dict:
    n = len(ed_gold)
    idx = np.random.default_rng(KG.G["boot_seed"]).integers(0, n, (KG.G["boot_b"], n))  # one draw, both arms
    pg, pd = KG.rates(ed_gold), KG.rates(ed_det)
    bg, bd = KG.rates(ed_gold, idx), KG.rates(ed_det, idx)
    d_ch, d_r = float(pd["CHAIR_i"] - pg["CHAIR_i"]), float(pg["R"] - pd["R"])
    hw = lambda x: round(float(np.diff(np.percentile(x, [2.5, 97.5]))[0] / 2), 4)  # noqa: E731
    fired = arm(d_ch, d_r)
    tot = {name: {k: int(sum(r[k] for r in rows)) for k in ("hal", "men", "tp", "g")}
           for name, rows in (("E_gold", ed_gold), ("E_det", ed_det))}
    driver = None
    if fired in ("chair", "both"):
        driver = "hallucination" if tot["E_det"]["hal"] > tot["E_gold"]["hal"] else "recall-driven"
    delta = {"CHAIR_i_det_minus_gold": round(d_ch, 4), "R_gold_minus_det": round(d_r, 4),
             "half_width_CHAIR_i": hw(bd["CHAIR_i"] - bg["CHAIR_i"]), "half_width_R": hw(bg["R"] - bd["R"])}
    m_det, m_gold = KG.matched_f1(ed_det, ed_gold)
    f = lambda x: round(float(x), 4)  # noqa: E731
    return {"verdict": "P2-GO" if fired != "none" else "P2-NO-GO", "fired_arm": fired, "driver": driver,
            "licence": licence(fired, driver, delta), "label": LABEL, "n_images": n, "go_thresholds": GO,
            "E_gold": {k: f(v) for k, v in pg.items()}, "E_det": {k: f(v) for k, v in pd.items()},
            "sums": tot, "correct_mentions_lost": tot["E_gold"]["tp"] - tot["E_det"]["tp"], "delta": delta,
            "units_gold": unit_stats(gone_gold), "units_det": unit_stats(gone_det),
            "words_mean": {"E_gold": f(np.mean([r["words"] for r in ed_gold])),
                           "E_det": f(np.mean([r["words"] for r in ed_det]))},
            "matched_count_F1": {"E_det": f(m_det), "E_gold": f(m_gold)}, **extra}


def score(p: dict, stored: dict, det: dict, val: tuple, out: Path, want: dict = REPRO,
          extra: dict | None = None) -> dict:
    """W3 first (a fault writes NOT RUN and the detector record is never opened), then E_det and the decision.
    val = (val-924 ids, gold per id, reference classes per id)."""
    ids, gold, refs = val
    try:
        _, ed_gold, gone_gold = reproduce(p, stored, ids, gold, refs, want)
    except Fault as e:
        return notrun(out, "fault", str(e))
    D = {int(i): v for i, v in det["D_0.30"].items()}
    D35 = {int(i): v for i, v in det["D_0.35_descriptive"].items()}
    if sorted(D) != sorted(ids) or det["classes"] != list(COCO80) or any(set(v) - set(COCO80) for v in D.values()):
        return notrun(out, "fault", "FAULT: the detector record does not cover val-924 over COCO-80")
    _, ed_det, gone_det = targets(p, ids, {i: set(v) for i, v in D.items()}, gold, refs)
    rec = decide(ed_gold, ed_det, gone_gold, gone_det,
                 {"D_presence_vs_gold_0.30": presence_pr(D, gold, ids),
                  "D_presence_vs_gold_0.35_descriptive": presence_pr(D35, gold, ids), **(extra or {})})
    records(out, rec)
    return rec


# ------------------------------------------------------------------------------------------------ M3 commands
def load(k2: Path) -> tuple:
    """The sha-pinned Gate 0 record and decode, the val-924 ids, gold and the val reference classes (cmd_score's)."""
    stored = json.loads(pinned_file(k2 / "gate0_decide.json", GATE0_SHA).read_text())
    p = json.loads(pinned_file(k2 / DECODE, DECODE_SHA).read_text(encoding="utf-8"))
    if stored.get("decode_sha256") != DECODE_SHA:
        raise Fault("FAULT: gate0_decide.json does not name the pinned decode")
    KG.val_ids_ok(K.pinned("manuscript/prereg/2026-10-21_dev_pools/uitviic_val.tsv"))
    gold = K.gold()
    lex = set(json.loads(K.pinned("data/coco_probe/coco80_vi.json").read_text(encoding="utf-8"))) - {"_note"}
    if set(COCO80) != lex or not set().union(*gold.values()) <= set(COCO80):  # W10: never equality with gold (65)
        raise Fault("FAULT: the 80 prompt names are not coco80_vi.json's classes, or gold is not inside them")
    staged = {f: h for h, f in (x.split("  ") for x in (K.UV / "images.sha256").read_text().splitlines())}
    for r in K.pinned("manuscript/prereg/2026-10-21_dev_pools/uitviic_val.tsv").read_text().splitlines():
        _, name, want = r.split("\t")[:3]
        if staged.get(name) != want or K.sha_file(K.UV / "images" / name) != want:  # W9: before the GPU pass
            raise Fault(f"FAULT: staged val image {name} differs from uitviic_val.tsv")
    refs: dict[int, set] = {}
    for x in json.loads((K.UV / "val_data.json").read_text(encoding="utf-8"))["annotations"]:
        refs.setdefault(int(x["image_id"]), set()).update(RW.ordered(x["caption"], "v2")[0])
    return stored, p, K.ids("val924"), gold, refs


def cmd(a) -> int:
    out = Path(a.out_dir)
    if out.name != "p2":
        raise SystemExit("REFUSED: --out-dir must be the p2/ folder (W2)")
    if a.cmd == "notrun":
        notrun(out, a.cls, a.why)
        return 0
    try:
        stored, p, ids, gold, refs = load(Path(a.k2_dir))
        if a.cmd == "repro":
            reproduce(p, stored, ids, gold, refs)
            print("W3 reproduction ok")
            return 0
    except Fault as e:
        notrun(out, "fault", str(e))
        return 3
    det_p = Path(a.detect)
    det_sha = K.sha_file(det_p)
    if (det_p.parent / "p2_detect.sha256").read_text().split()[0] != det_sha:
        notrun(out, "fault", "FAULT: p2_detect.json changed after it was hashed")
        return 3
    det = json.loads(det_p.read_text())
    rec = score(p, stored, det, (ids, gold, refs), out, extra={
        "p2_detect_sha256": det_sha, "gate0_decide_sha256": GATE0_SHA, "decode_sha256": DECODE_SHA,
        "detector": {k: det.get(k) for k in ("pins", "prompt_tokens", "s_per_image", "load_s", "peak_gpu_mem_gib",
                                            "msda_cuda_calls", "load_state_dict_unexpected", "gpu")}})
    print(json.dumps({k: rec.get(k) for k in ("verdict", "fired_arm", "class")}))
    return 0 if rec["verdict"] != "NOT-RUN" else 3


# ------------------------------------------------------------------------------------------------ selftest
def selftest() -> None:
    import tempfile

    assert arm(6.0, 0) == "chair" and arm(0, 4.0) == "recall" and arm(6.0, 4.0) == "both"  # at the threshold: GO
    assert arm(5.9999, 3.9999) == "none" and arm(-9, -9) == "none"
    g = {"person", "sports ball"}
    n = 40
    ids = list(range(n))
    cases = {  # synthetic (k2_gate0 selftest strings): (caption, gold, D) -> (fired arm, driver, H-P2 primary?)
        "none": ("một người cầm quả bóng, cạnh con chó.", g, g, (None, False)),
        "recall": ("một người cầm quả bóng, cạnh con chó.", g, {"person"}, (None, False)),
        "chair": ("một người cầm quả bóng, cạnh con chó.", g, g | {"dog"}, ("hallucination", True)),
        "both": ("một người, quả bóng, con chó.", g, {"person", "dog"}, ("hallucination", True)),
        # v2-only person (LEX_V2 "cầu thủ") is a hallucination both editors keep; the miss of the ball shrinks
        # sum men, so CHAIR_i rises with sum hal unchanged: the CHAIR arm fires recall-driven (W4) -> no H-P2
        "both_recall_driven": ("cầu thủ, quả bóng.", {"sports ball"}, set(), ("recall-driven", False))}
    with tempfile.TemporaryDirectory() as t:
        for case, (c, gg, d, (want_driver, primary)) in cases.items():
            want_arm = case.split("_")[0]
            gold = {i: gg for i in ids}
            p = {"predictions": {str(i): c for i in ids}, "hit_max": {str(i): False for i in ids}}
            zs, ed, gone = targets(p, ids, gold, gold, {})
            stored = KG.decide(zs, ed, gone, {}) | {"verdict": "GO", "fired": [],
                                                    "p1_truncation_frontier": {"verdict": "P1-GO"}}
            want = {"CHAIR_i": (stored["edited"]["CHAIR_i"], 4), "R": (stored["edited"]["R"], 4),
                    "deleted_units": stored["deleted_units"]}
            det = {"D_0.30": {str(i): sorted(d) for i in ids}, "D_0.35_descriptive": {str(i): [] for i in ids},
                   "classes": list(COCO80)}
            out = Path(t) / case / "p2"
            rec = score(p, stored, det, (ids, gold, {}), out, want)
            assert (rec["fired_arm"], rec["driver"]) == (want_arm, want_driver), (case, rec["fired_arm"], rec["driver"])
            lic = rec["licence"]
            assert (lic["primary"] == H_P2) is primary and (lic["secondary"] == H_P2R) is (want_arm != "none"), lic
            assert set(rec["sums"]["E_det"]) == {"hal", "men", "tp", "g"} and "correct_mentions_lost" in rec
            md = "P2_VERDICT.md" if want_arm != "none" else "P2_STOP.md"
            assert (out / md).is_file() and json.loads((out / "p2_decide.json").read_text())["fired_arm"] == want_arm
            assert not (out / "gate0_decide.json").exists()
            try:  # one look
                score(p, stored, det, (ids, gold, {}), out, want)
            except SystemExit as e:
                assert "one look" in str(e), e
            else:
                raise AssertionError("a second P2 look was accepted")
        # W3: a stored value off by 1e-4, a wrong LOG constant, or a failed precondition -> NOT RUN (fault); the
        # detector record is never opened
        class Sealed(dict):
            def __getitem__(self, k):
                raise AssertionError("the detector record was opened before W3 passed")

        for k, tamper in (("edited", lambda s: s["edited"].update(CHAIR_i=s["edited"]["CHAIR_i"] + 1e-4)),
                          ("LOG", lambda s: None), ("pre", lambda s: s.update(verdict="STOP"))):
            s = json.loads(json.dumps(stored))
            tamper(s)
            w = want if k != "LOG" else want | {"deleted_units": want["deleted_units"] + 1}
            out = Path(t) / f"w3_{k}" / "p2"
            rec = score(p, s, Sealed(), (ids, gold, {}), out, w)
            assert rec["verdict"] == "NOT-RUN" and rec["class"] == "fault -> TO-PI" and "W3" in rec["why"], rec
            assert (out / rec["record"]).read_text().startswith("# K2 P2 NOT RUN (fault -> TO-PI)")
            assert not (out / "p2_decide.json").exists() and not (out / "P2_STOP.md").exists()  # W13: no look yet
        # W13: after a fault the rerun is allowed and decides; after p2_decide.json nothing more is written
        rec = score(p, stored, det, (ids, gold, {}), out, want)
        assert rec["verdict"] in ("P2-GO", "P2-NO-GO") and (out / "p2_decide.json").is_file()
        try:
            notrun(out, "fault", "late fault")
        except SystemExit as e:
            assert "one look" in str(e), e
        else:
            raise AssertionError("a record was written after p2_decide.json")
        # W2: never gate0_decide.json, never an unlisted name
        for name in ("gate0_decide.json", "STOP.md"):
            try:
                write(Path(t) / "x" / "p2" / name, "{}")
            except SystemExit as e:
                assert "REFUSED" in str(e), e
            else:
                raise AssertionError(f"P2 wrote {name}")
        f = Path(t) / "f"
        f.write_text("x")
        try:
            pinned_file(f, "0" * 64)
        except Fault as e:
            assert "W3" in str(e), e
        else:
            raise AssertionError("a sha mismatch was accepted")
        nr = notrun(Path(t) / "cost" / "p2", "cost", "detector exit 124 (the 1800 s cap)")
        assert nr["class"] == "cost -> TO-PI" and (Path(t) / "cost/p2/P2_STOP.md").is_file()
        assert (Path(t) / "cost/p2/p2_decide.json").is_file()  # a cost NOT RUN closes the pilot
    hw = {"half_width_CHAIR_i": 3.0, "half_width_R": 0.1}
    assert "chair arm" in licence("chair", "hallucination", hw)["half_width"]
    assert "half_width" not in licence("recall", None, hw)
    assert presence_pr({0: ["person", "dog"]}, {0: g}, [0]) == {"precision": 50.0, "recall": 50.0,
                                                               "mean_classes_per_image": 2.0}
    print("k2_p2 selftest ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", choices=("repro", "decide", "notrun"))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--k2-dir")
    ap.add_argument("--detect")
    ap.add_argument("--out-dir")
    ap.add_argument("--class", dest="cls", choices=("cost", "fault"))
    ap.add_argument("--why")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    if not a.cmd:
        ap.error("give --selftest or a command")
    return cmd(a)


if __name__ == "__main__":
    sys.exit(main())
