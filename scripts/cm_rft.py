#!/usr/bin/env python
"""CM-RFT targets for S3 (prereg 2026-10-18_tier3_S3 §5; R14-2 P-2): count-matched rejection-sampling SFT rows.

    python scripts/cm_rft.py --merge T05.jsonl T08.jsonl --out POOL.jsonl            # 6 + 6 samples per RL image
    python scripts/cm_rft.py --pool POOL.jsonl --greedy GREEDY.preds.json --out DIR   # needs the JVM (RDRSegmenter)
    python scripts/cm_rft.py --selftest

Per RL image, among the usable pool samples (cm_pairs.usable, the pairs' own filters, after de-duplication) whose
number of distinct classes equals that of P1_dev's greedy caption: the one with the most ktvic5 train-gold classes, kept
only if its TP exceeds the greedy's; ties by CIDEr-D against references 1-4 (reference 0 is the SFT target;
rl_reward.CiderD with document frequencies from every reference of train minus dev300, RDRSegmenter tokens as
evaluate.py), then by the lower pool index. DIR/sft.jsonl holds, per kept image, the target (MODEL-GENERATED) and the
image's first human caption, 1:1, in train_stage2.py's format; DIR/_rft_report.json the counts. Never overwrites.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

from s3_gate import SAMPLER, _dump, _write_once, dev_ids, provenance, rl_ids  # noqa: E402


def _jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]


def merge(a: Path, b: Path, out: Path, ids: list[str], n: int) -> None:
    """One row per image: the n samples of `a` (T 0.5) then the n of `b` (T 0.8), on exactly the RL images."""
    rows = [{r["image_id"]: r for r in _jsonl(p)} for p in (a, b)]
    if not set(rows[0]) == set(rows[1]) == set(ids):
        raise SystemExit("the two pools do not both cover exactly the RL images")
    if any(len(r[i]["samples"]) != n for r in rows for i in ids):
        raise SystemExit(f"every pool row must hold {n} samples")
    _write_once(out, "".join(json.dumps({"image_id": i, "file_name": rows[0][i]["file_name"],
                                         "samples": rows[0][i]["samples"] + rows[1][i]["samples"]},
                                        ensure_ascii=False) + "\n" for i in sorted(ids)))


def targets(pool: dict, greedy: dict, refs: dict, names: dict, cider) -> tuple[list[dict], dict]:
    """The rows and counts; cider(image_id, texts) -> CIDEr-D of each text against the image's references 1-4."""
    from cm_pairs import PROMPT_SHORT, usable
    from rescap.chair import objects_in

    def cls(c: str) -> frozenset:
        return frozenset(objects_in(c))

    rows, rep = [], Counter()
    for iid in sorted(pool):
        gold = frozenset().union(*map(cls, refs[iid]))
        k, tp_greedy = len(cls(greedy[iid])), len(cls(greedy[iid]) & gold)
        first: dict[str, int] = {}
        for n, c in enumerate(pool[iid]):
            first.setdefault(c, n)
        cands = [(n, c) for c, n in first.items() if usable(c, refs[iid]) and len(cls(c)) == k]
        best = max((len(cls(c) & gold) for _, c in cands), default=-1)
        if best <= tp_greedy:
            rep["no_usable_same_count_candidate" if not cands else "not_above_greedy_tp"] += 1
            continue
        tied = [(n, c) for n, c in cands if len(cls(c) & gold) == best]
        if len(tied) > 1:
            scores = cider(iid, [c for _, c in tied])
            tied = [t for t, s in zip(tied, scores) if s == max(scores)]
            rep["tie_broken_by_cider" if len(tied) == 1 else "tie_broken_by_pool_index"] += 1
        target = min(tied)[1]
        rep["tp_gain_total"] += best - tp_greedy
        rows += [{"image_id": iid, "file_name": names[iid], "prompt": PROMPT_SHORT, "response": target,
                  "source": "model_sample (MODEL-GENERATED)", "label_source": "human"},
                 {"image_id": iid, "file_name": names[iid], "prompt": PROMPT_SHORT, "response": refs[iid][0],
                  "source": "human_reference_0 (P1's SFT target)"}]
    rep.update(images=len(pool), kept=len(rows) // 2, rows=len(rows))
    return rows, dict(rep)


def cider_scorer(dev: list[str]):
    """CIDEr-D against references 1-4: rl_reward.CiderD, df from every reference of train minus dev300, RDRSegmenter."""
    from evaluate import references
    from rl_reward import CiderD, Reward, Segmenter

    refs = references("train_data.json")
    reward = Reward(refs, Segmenter())  # every train reference segmented once, as evaluate.py segments
    cd = CiderD([reward.refs[i] for i in sorted(set(refs) - set(dev))])

    def score(iid: str, texts: list[str]) -> list[float]:
        return [cd.score(s.split(), reward.refs[iid][1:5]) for s in reward.seg(texts)]
    return score


def selftest() -> None:
    """Count match, the TP rule, the filters, both tie-breaks, the 1:1 rows, and the merge order."""
    ref_a = "phụ nữ với xe máy trên đường"  # synthetic captions stay under 8 syllables (the OpenViIC 8-gram scan)
    refs = {"1": [ref_a] * 5, "2": ["con chó và con mèo"] * 5, "3": ["con chó và con mèo"] * 5,
            "4": [ref_a] * 5, "5": [ref_a] * 5}
    pool = {"1": ["phụ nữ ngồi xe máy",  # k 2, TP 2, index 0
                  "đàn ông cạnh ô tô",  # k 2, TP 0
                  "phụ nữ trên xe máy",  # k 2, TP 2, index 2: wins on CIDEr below
                  "phụ nữ ngồi xe máy trên đường", ""],  # k 3: other count; empty
            "2": ["một con mèo", "một chiếc xe máy"],  # best TP 1 = the greedy's: not kept
            "3": ["một con chó", "một con mèo", "một con chó"],  # TP 1 > 0, tie, equal CIDEr: lower index
            "4": ["một chiếc xe máy", "một con chó"],  # k 1 only, the greedy has k 2
            "5": [ref_a, "phụ nữ ngồi trên"]}  # a copy and a function-word end only
    greedy = {"1": "phụ nữ ngồi ô tô", "2": "con chó nằm", "3": "một cái bàn", "4": "phụ nữ ngồi ô tô",
              "5": "phụ nữ ngồi ô tô"}

    def cider(iid: str, texts: list[str]) -> list[float]:
        return [2.0 if t == pool["1"][2] else 1.0 for t in texts]

    rows, rep = targets(pool, greedy, refs, {i: f"{i}.jpg" for i in refs}, cider)
    assert [(r["image_id"], r["response"]) for r in rows] == [
        ("1", pool["1"][2]), ("1", ref_a), ("3", pool["3"][0]), ("3", refs["3"][0])], rows
    assert rep == {"tie_broken_by_cider": 1, "tie_broken_by_pool_index": 1, "not_above_greedy_tp": 1,
                   "no_usable_same_count_candidate": 2, "tp_gain_total": 2, "images": 5, "kept": 2, "rows": 4}, rep
    assert all(r["prompt"] == rows[0]["prompt"] for r in rows) and "MODEL" in rows[0]["source"]
    with tempfile.TemporaryDirectory() as tmp:
        a, b, out = Path(tmp) / "a.jsonl", Path(tmp) / "b.jsonl", Path(tmp) / "pool.jsonl"
        for path, tag in ((a, "x"), (b, "y")):
            path.write_text("".join(json.dumps({"image_id": i, "file_name": f"{i}.jpg", "samples": [tag + i, tag]}) + "\n"
                                    for i in ("2", "1")), encoding="utf-8")
        merge(a, b, out, ["1", "2"], 2)
        assert [r["samples"] for r in _jsonl(out)] == [["x1", "x", "y1", "y"], ["x2", "x", "y2", "y"]]
        merge(a, b, out, ["1", "2"], 2)  # an identical rewrite is a no-op
    print("cm_rft selftest ok: count match, TP rule, filters, CIDEr and pool-index tie-breaks, 1:1 rows, merge")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--merge", nargs=2, metavar=("T05", "T08"))
    ap.add_argument("--pool")
    ap.add_argument("--greedy", help="P1_dev's greedy short decode of the RL images (evaluate.py .preds.json)")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    if a.merge and a.out:
        merge(Path(a.merge[0]), Path(a.merge[1]), Path(a.out), rl_ids(), SAMPLER["n"])
        return 0
    if not (a.pool and a.greedy and a.out):
        ap.error("--merge T05 T08 --out POOL, or --pool --greedy --out DIR, or --selftest")
    from evaluate import file_names, references

    ids = rl_ids()
    pool = {r["image_id"]: r["samples"] for r in _jsonl(Path(a.pool))}
    greedy = {str(k): (v[0] if isinstance(v, list) else v) for k, v in json.loads(Path(a.greedy).read_text(
        encoding="utf-8")).items()}
    if set(pool) != set(ids) or not set(ids) <= set(greedy):
        raise SystemExit("the pool and the greedy decode must cover the RL images")
    rows, rep = targets(pool, greedy, references("train_data.json"), file_names("train_data.json"),
                        cider_scorer(dev_ids()))
    out = Path(a.out)
    _write_once(out / "sft.jsonl", "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    _write_once(out / "_rft_report.json", _dump(dict(rep, provenance=provenance())))
    print(json.dumps(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
