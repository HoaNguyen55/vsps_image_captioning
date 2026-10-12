#!/usr/bin/env python
"""Are an image's 5 KTVIC captions exchangeable? Object overlap of adjacent vs non-adjacent file positions (V4 1d).

    NCS_DATA=data python scripts/caption_exchangeability.py      # -> data/results/caption_exchangeability.json

The fold protocols (human_parity.py, second_panel.py, two_gold_audit.py) and the implicit-threshold model treat
the 5 captions of an image as i.i.d. annotators. If captions at adjacent positions (1-2, 2-3, 3-4, 4-5) share
more objects than non-adjacent ones, positions are not exchangeable (e.g. 3 annotators wrote 5 captions, or
reviewers revised neighbours), and a "held-out annotator" is often a held-out caption of the same writer.
Per image: mean over position pairs of shared objects |A & B|, Jaccard |A & B| / |A | B| (1 when both are
empty) and union size; adjacent minus non-adjacent with 95% CIs over images (objects_in, all images with 5).
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from rescap.chair import objects_in  # noqa: E402
from two_gold_audit import summ, weights  # noqa: E402

PAIRS = list(itertools.combinations(range(5), 2))
ADJ = [p for p in PAIRS if p[1] == p[0] + 1]
STATS = {"shared": lambda a, b: len(a & b), "jaccard": lambda a, b: len(a & b) / len(a | b) if a | b else 1.0,
         "union": lambda a, b: len(a | b)}


def image_stats(sets: list[set]) -> dict[str, float]:
    out = {"single": float(np.mean([len(s) for s in sets]))}
    for k, f in STATS.items():
        v = {p: f(sets[p[0]], sets[p[1]]) for p in PAIRS}
        out[f"{k}_adjacent"] = float(np.mean([v[p] for p in ADJ]))
        out[f"{k}_nonadjacent"] = float(np.mean([v[p] for p in PAIRS if p not in ADJ]))
        out.update({f"{k}_{p[0] + 1}{p[1] + 1}": v[p] for p in PAIRS})
    return out


def main() -> int:
    from evaluate import references
    out = {"what": "scripts/caption_exchangeability.py (V4 1d): adjacent vs non-adjacent caption positions", "B": 2000}
    for split in ("train", "test"):
        refs = references(f"{split}_data.json")
        rows = [image_stats([set(objects_in(c)) for c in cs]) for _, cs in sorted(refs.items()) if len(cs) == 5]
        keys = list(rows[0])
        t = weights(len(rows), out["B"]) @ np.array([[r[k] for k in keys] for r in rows]) / len(rows)
        col = dict(zip(keys, t.T))
        res = {"n_images": len(rows), **{k: summ(v) for k, v in col.items()}}
        for k in STATS:
            res[f"{k}_adjacent_minus_nonadjacent"] = summ(col[f"{k}_adjacent"] - col[f"{k}_nonadjacent"], test=True)
        new_adj, new_non = col["union_adjacent"] - col["single"], col["union_nonadjacent"] - col["single"]
        res["new_objects_adjacent_vs_nonadjacent_%"] = summ(100 * (1 - new_adj / new_non))
        out[split] = res
        print(f"{split} ({len(rows)}): " + "  ".join(f"{k} {res[f'{k}_adjacent_minus_nonadjacent'][:2]}" for k in STATS)
              + f"  union adj {res['union_adjacent'][0]:.2f} non {res['union_nonadjacent'][0]:.2f} single "
                f"{res['single'][0]:.2f}; adjacent adds {res['new_objects_adjacent_vs_nonadjacent_%'][0]:.1f}% fewer")
    dst = ROOT / "data" / "results" / "caption_exchangeability.json"
    dst.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(f"-> {dst}")
    return 0


def _check() -> None:
    s = image_stats([{"a"}, {"a"}, set(), set(), {"b"}])
    assert s["shared_12"] == 1 and s["jaccard_34"] == 1.0 and s["jaccard_12"] == 1.0 and s["union_15"] == 2
    assert s["shared_adjacent"] == 0.25 and s["jaccard_adjacent"] == 0.5 and abs(s["single"] - 0.6) < 1e-9


if __name__ == "__main__":
    _check()
    sys.exit(main())
