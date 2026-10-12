#!/usr/bin/env python
"""Training-free selection over N sampled captions per image (e5_sample.py output).

    python scripts/self_fuse.py samples.jsonl --k 1 --out results/p1mbr-short.preds.json
    python scripts/self_fuse.py samples.jsonl --k 2 --out results/p1selffuse-two.preds.json

k = 1 keeps the consensual sample, the one naming the most objects another sample
also names (object-consensus MBR). k = 2 appends the sample adding the most new
objects, the same greedy rule build_gold_sft.py applies to human captions, so a
single-reference model gets a length-matched two-sentence output at inference time.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_gold_sft import fused  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("samples")
    ap.add_argument("--k", type=int, default=1)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    rows = [json.loads(line) for line in Path(args.samples).read_text(encoding="utf-8").splitlines()]
    preds = {r["image_id"]: fused([s for s in r["samples"] if s.strip()] or [""], args.k) for r in rows}
    Path(args.out).write_text(json.dumps(preds, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {len(preds)} captions (k={args.k}) -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
