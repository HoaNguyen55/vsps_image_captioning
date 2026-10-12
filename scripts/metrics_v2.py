#!/usr/bin/env python
"""Length-aware n-gram diagnostic + table over data/results/metrics_v2/*.json.

    python scripts/metrics_v2.py cider ~/ncs-data/results/*-short.preds.json ...
    python scripts/metrics_v2.py table            # markdown, Δ vs P1 with paired bootstrap

`cider` writes metrics_v2/<stem>.cider.json with per-image CIDEr-D (σ=6, the
official number), CIDEr with σ=∞ (Gaussian length penalty off, TF-IDF and
clipping kept — NON-STANDARD, diagnostic only) and length in words after
RDRSegmenter. scripts/clip_score.py writes <stem>.clip.json / <stem>.bert.json
in the same shape, so `table` merges them all by stem.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from score_ci import (B_DEFAULT, SCALE, SEED, ci95, load_preds,  # noqa: E402
                      p_two_sided, per_image_cider, tokenized)

OUT = Path(__file__).resolve().parents[1] / "data" / "results" / "metrics_v2"
P1 = "p1-gold"


def write(stem: str, kind: str, per_image: dict, extra: dict) -> None:
    """Common file shape: {"stem", "n_images", **extra, "per_image": {metric: {id: v}}}."""
    OUT.mkdir(parents=True, exist_ok=True)
    n = len(next(iter(per_image.values())))
    path = OUT / f"{stem}.{kind}.json"
    path.write_text(json.dumps({"stem": stem, "n_images": n, **extra, "per_image": per_image},
                               ensure_ascii=False), encoding="utf-8")
    print(f"  wrote {path}")


def full_split(refs: dict, preds: dict, path: str) -> list[str] | None:
    ids = sorted(refs)
    missing = [i for i in ids if i not in preds]
    if missing:
        print(f"  skip {path}: missing {len(missing)}/{len(ids)} images (no subset scoring)")
        return None
    return ids


def cmd_cider(args) -> None:
    from evaluate import references

    refs = references(args.split)
    for path in args.preds:
        preds = load_preds(path)
        ids = full_split(refs, preds, path)
        if ids is None:
            continue
        gt = {i: list(refs[i]) for i in ids}
        toks = tokenized(gt, preds, ids, args.segmenter)
        _, std = per_image_cider(gt, preds, ids, args.segmenter, toks=toks)
        _, nopen = per_image_cider(gt, preds, ids, args.segmenter, sigma=float("inf"), toks=toks)
        length = {i: float(len(toks[1][i][0].split())) for i in ids}
        stem = Path(path).name.removesuffix(".preds.json")
        write(stem, "cider", {
            "CIDEr-D": {i: v * SCALE for i, v in std.items()},
            "CIDEr-noLP(diag)": {i: v * SCALE for i, v in nopen.items()},
            "len_words": length,
        }, {"segmenter": args.segmenter, "split": args.split})


def cmd_table(args) -> None:
    import numpy as np

    merged: dict[str, dict] = {}
    for f in sorted(OUT.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        merged.setdefault(d["stem"], {}).update(d["per_image"])
    rng = np.random.default_rng(SEED)
    for mode in ("short", "detailed"):
        stems = sorted(s for s in merged if s.endswith(f"-{mode}"))
        if not stems:
            continue
        metrics = sorted({m for s in stems for m in merged[s]})
        ref = merged.get(f"{P1}-{mode}", {})
        ids = sorted(next(iter(merged[stems[0]].values())))
        idx = rng.integers(0, len(ids), size=(args.rounds, len(ids)))
        print(f"\n### KTVIC test — {mode} (mean; Δ vs {P1} [95% paired-bootstrap CI], B={args.rounds})\n")
        print("| system | " + " | ".join(metrics) + " |")
        print("|---" * (len(metrics) + 1) + "|")
        for s in stems:
            cells = []
            for m in metrics:
                if m not in merged[s]:
                    cells.append("–")
                    continue
                v = np.array([merged[s][m][i] for i in ids])
                cell = f"{v.mean():.2f}"
                if m in ref and s != f"{P1}-{mode}":
                    d = v[idx].mean(1) - np.array([ref[m][i] for i in ids])[idx].mean(1)
                    lo, hi = ci95(d)
                    star = "*" if lo > 0 or hi < 0 else ""
                    cell += f" ({d.mean():+.2f} [{lo:+.2f},{hi:+.2f}]{star}, p≈{p_two_sided(d):.3f})"
                cells.append(cell)
            print(f"| {s.removesuffix('-' + mode)} | " + " | ".join(cells) + " |")
    print("\nCIDEr-noLP(diag) = CIDEr with σ=∞ (no Gaussian length penalty): NON-STANDARD, diagnostic only. "
          "* = 95% CI of Δ excludes 0.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cider")
    c.add_argument("preds", nargs="+")
    c.add_argument("--split", default="test_data.json")
    c.add_argument("--segmenter", default="rdrsegmenter")
    t = sub.add_parser("table")
    t.add_argument("--rounds", type=int, default=B_DEFAULT)
    args = ap.parse_args()
    {"cider": cmd_cider, "table": cmd_table}[args.cmd](args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
