#!/usr/bin/env python
"""Near-duplicate images between two KTVIC-style splits (CLIP image-embedding cosine).

    python scripts/near_dup.py --a train_data.json --b test_data.json --thr 0.95 --out dup.json
    python scripts/near_dup.py --self-check

Reports, for every image of split B, its most similar image in split A; pairs at or above
--thr are near-duplicates. Within-split duplicates are not counted.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np

ROOT = Path(os.environ.get("NCS_DATA", "~/ncs-data")).expanduser() / "datasets" / "ktvic"


def nearest(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Row-normalised embeddings a (n,d), b (m,d) -> for each b row: best a index and cosine."""
    sims = b @ a.T
    idx = sims.argmax(axis=1)
    return idx, sims[np.arange(len(b)), idx]


def embed(paths: list[Path], batch: int = 64) -> np.ndarray:
    import torch
    from PIL import Image
    from transformers import CLIPModel, CLIPProcessor

    name = "openai/clip-vit-base-patch32"
    model = CLIPModel.from_pretrained(name).eval().to("cuda" if torch.cuda.is_available() else "cpu")
    proc = CLIPProcessor.from_pretrained(name)
    out = []
    for i in range(0, len(paths), batch):
        ims = [Image.open(p).convert("RGB") for p in paths[i:i + batch]]
        with torch.no_grad():
            x = proc(images=ims, return_tensors="pt").to(model.device)
            e = model.get_image_features(**x)
        out.append(torch.nn.functional.normalize(e, dim=-1).float().cpu().numpy())
    return np.concatenate(out)


def split_files(name: str) -> list[str]:
    return [im["filename"] for im in json.loads((ROOT / name).read_text(encoding="utf-8"))["images"]]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", default="train_data.json")
    ap.add_argument("--b", default="test_data.json")
    ap.add_argument("--thr", type=float, default=0.95)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    fa, fb = split_files(args.a), split_files(args.b)
    same_name = sorted(set(fa) & set(fb))
    ea, eb = embed([ROOT / "images" / f for f in fa]), embed([ROOT / "images" / f for f in fb])
    idx, sim = nearest(ea, eb)
    pairs = [{"b": fb[j], "a": fa[idx[j]], "cos": round(float(sim[j]), 4)} for j in range(len(fb))]
    dup = [p for p in pairs if p["cos"] >= args.thr]
    report = {"a": args.a, "b": args.b, "thr": args.thr, "n_a": len(fa), "n_b": len(fb),
              "same_filename": len(same_name), "n_dup": len(dup),
              "cos_quantiles": {q: round(float(np.quantile(sim, q)), 4) for q in (0.5, 0.9, 0.99)},
              "clean_b": [p["b"] for p in pairs if p["cos"] < args.thr], "pairs": pairs}
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{args.b} vs {args.a}: {len(dup)}/{len(fb)} near-dup at cos>={args.thr}; "
          f"same filename {len(same_name)}; quantiles {report['cos_quantiles']}")


def self_check() -> None:
    a = np.eye(3, dtype=np.float32)
    b = np.array([[0.0, 1.0, 0.0], [0.6, 0.0, 0.8]], dtype=np.float32)
    idx, sim = nearest(a, b)
    assert idx.tolist() == [1, 2] and np.allclose(sim, [1.0, 0.8])
    print("self-check OK")


if __name__ == "__main__":
    import sys
    self_check() if "--self-check" in sys.argv else main()
