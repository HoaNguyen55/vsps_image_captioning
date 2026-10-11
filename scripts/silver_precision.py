#!/usr/bin/env python
"""Is a precision loss under reference gold hallucination, or real objects the 5 references skip?

    NCS_DATA=$PWD/data python scripts/silver_precision.py --allow-ai
    python scripts/silver_precision.py --self-check

On the images of an exhaustive object annotation (default: the AI-produced
data/object_gold/annot_claude.json, 300 KTVIC test images; AI-silver, NOT human gold)
precision = sum|M&G| / sum|M| is computed for each system under three golds:
(a) the union of the 5 reference captions, (b) the silver annotation, (c) a | b.
`rescued` is the share of mentions false under (a) that (b) marks present.
M and both golds are folded to the same checkbox classes (object_gold_score.mentions),
exact match only. 95% percentile CIs resample images.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from object_gold_score import ai_produced, load_preds, mentions, read_annotations  # noqa: E402

SYSTEMS = ["p1-gold-short", "fuse2_s42-short", "e5_s42-short", "p1-gold-detailed", "fuse2_s42-detailed",
           "e5_s42-detailed", "zeroshot-detailed", "main_s42-detailed"]


def counts(m: set[str], ref: set[str], silver: set[str]) -> tuple[int, int, int, int, int]:
    """(|M|, tp ref, tp silver, tp union, ref-false mentions silver marks present) for one image."""
    false_ref = m - ref
    return len(m), len(m & ref), len(m & silver), len(m & (ref | silver)), len(false_ref & silver)


def precisions(rows: list[tuple]) -> dict[str, float]:
    n, tr, ts, tu, rescued = (sum(c) for c in zip(*rows))
    return {"P_ref": 100 * tr / n, "P_silver": 100 * ts / n, "P_union": 100 * tu / n,
            "rescued": 100 * rescued / (n - tr) if n > tr else float("nan"), "mentions/img": n / len(rows)}


def bootstrap(rows: list[tuple], n: int = 1000, seed: int = 0) -> dict[str, tuple[float, float]]:
    rng = random.Random(seed)
    draws = [precisions([rows[rng.randrange(len(rows))] for _ in rows]) for _ in range(n)]
    return {k: (sorted(d[k] for d in draws)[int(0.025 * n)], sorted(d[k] for d in draws)[int(0.975 * n) - 1])
            for k in ("P_ref", "P_silver", "P_union", "rescued")}


def paired_delta(rows: list[tuple], base: list[tuple], n: int = 1000, seed: int = 0) -> dict[str, tuple]:
    """Delta (rows - base) with 95% CI, same images resampled for both systems."""
    rng = random.Random(seed)
    keys = ("P_ref", "P_silver", "P_union")
    point = {k: precisions(rows)[k] - precisions(base)[k] for k in keys}
    draws = []
    for _ in range(n):
        idx = [rng.randrange(len(rows)) for _ in rows]
        a, b = precisions([rows[j] for j in idx]), precisions([base[j] for j in idx])
        draws.append({k: a[k] - b[k] for k in keys})
    return {k: (point[k], sorted(d[k] for d in draws)[int(0.025 * n)], sorted(d[k] for d in draws)[int(0.975 * n) - 1])
            for k in keys}


def self_check() -> None:
    # caption: chó (in refs), mèo (refs miss it, silver has it), voi (nobody has it)
    rows = [counts({"chó", "mèo", "voi"}, {"chó"}, {"chó", "mèo"})] * 4
    p = precisions(rows)
    assert abs(p["P_ref"] - 100 / 3) < 1e-9 and abs(p["P_silver"] - 200 / 3) < 1e-9
    assert abs(p["P_union"] - 200 / 3) < 1e-9 and p["rescued"] == 50.0 and p["mentions/img"] == 3
    assert counts({"chó"}, {"chó"}, set()) == (1, 1, 0, 1, 0)
    same = paired_delta(rows, rows)
    assert all(v == (0.0, 0.0, 0.0) for v in same.values()), same
    assert mentions("một con chó và một con mèo") == {"chó", "mèo"}
    print("self-check OK")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--silver", default=str(ROOT / "data" / "object_gold" / "annot_claude.json"))
    ap.add_argument("--results", default=str(ROOT / "data" / "results"))
    ap.add_argument("--split", default="test_data.json")
    ap.add_argument("--allow-ai", action="store_true", help="required when --silver is AI-produced")
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args()
    if args.self_check:
        self_check()
        return 0
    silver_path = Path(args.silver)
    if ai_produced(silver_path) and not args.allow_ai:
        ap.error(f"{silver_path.name} is AI-produced (not human gold); pass --allow-ai to use it as AI-silver")
    labels = json.loads(silver_path.read_text(encoding="utf-8"))["labels"]
    ids = sorted((i for i, v in labels.items() if v.get("done")), key=int)
    silver = read_annotations(silver_path, ids)

    from evaluate import references

    refs = references(args.split)
    missing = [i for i in ids if i not in refs]
    if missing:
        raise SystemExit(f"{len(missing)} silver images are not in {args.split}, e.g. {missing[:5]}")
    ref_gold = {i: set().union(*(mentions(r) for r in refs[i])) for i in ids}
    print(f"{len(ids)} {args.split} images; silver = {silver_path.name} (AI-silver, not human gold); "
          f"classes/img ref {sum(map(len, ref_gold.values())) / len(ids):.2f}, "
          f"silver {sum(map(len, silver.values())) / len(ids):.2f}")
    all_rows = {}
    for name in SYSTEMS:
        caps = load_preds(Path(args.results) / f"{name}.preds.json")
        rows = all_rows[name] = [counts(mentions(caps.get(i, "")), ref_gold[i], silver[i]) for i in ids]
        p, ci = precisions(rows), bootstrap(rows)
        print(f"  {name:20s} M/img={p['mentions/img']:.2f}  "
              + "  ".join(f"{k}={p[k]:5.1f} [{a:.1f}; {b:.1f}]" for k, (a, b) in ci.items()))
    for name in SYSTEMS:
        base = "p1-gold-" + name.rsplit("-", 1)[1]
        if name != base:
            d = paired_delta(all_rows[name], all_rows[base])
            print(f"  {name:20s} - {base}: "
                  + "  ".join(f"d{k}={x:+5.1f} [{a:+.1f}; {b:+.1f}]" for k, (x, a, b) in d.items()))
    return 0


if __name__ == "__main__":
    self_check()
    raise SystemExit(main())
