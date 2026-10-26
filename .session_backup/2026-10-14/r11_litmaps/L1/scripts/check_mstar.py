#!/usr/bin/env python
"""L1 check 1: is raw object F1's verbosity reward a property of the gold?

Lipton et al. (arXiv 1402.1892, Cor. 1 / proof of Thm 1): adding mentions raises micro-F1 iff their precision
exceeds F/2. With G2's frontier TP = a*M^b the marginal precision is b*P, so micro-F1 peaks at
    M* = b * Gbar / (1 - b)          (Gbar = mean gold classes per image)
and b -> 1 gives Lipton's Thm 3 (uninformative scores: predict everything). G2 shows b falls with sparser gold,
so the prediction is: under a 1-reference gold M* sits BELOW the trained systems' counts and F1 should fall with
M across them; under 5 references it sits far above and F1 rises.

Metric = scripts/object_prf.py: micro P, R = mean over images with non-empty gold, exact classes.
KTVIC test, the 73 data/results/*.preds.json, gold = union of k references (first-k in file order, and the mean
over 20 random k-subsets per image). Read-only on the repo; prints aggregates only (no caption text).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path("/mnt/d/vsps_image_captioning")
sys.path[:0] = [str(ROOT)]
from rescap.chair import objects_in  # noqa: E402

FT_EXCLUDE = re.compile(r"(zeroshot|tags_zeroshot|vcd|official|vsps|main_|seed4|roundA|roundB|v3_|p2-|off|offsft)")
NBOOT, NSUB = 500, 20


def load():
    refs: dict[str, list[str]] = {}
    for a in json.loads((ROOT / "data/datasets/ktvic/test_data.json").read_text("utf-8"))["annotations"]:
        if a.get("caption"):
            refs.setdefault(str(a["image_id"]), []).append(a["caption"])
    ids = sorted(refs)
    ref_sets = {i: [set(objects_in(r)) for r in refs[i]] for i in ids}
    ments = {}
    for f in sorted((ROOT / "data/results").glob("*.preds.json")):
        p = json.loads(f.read_text("utf-8"))
        ments[f.name.removesuffix(".preds.json")] = [
            set(objects_in((p.get(i)[0] if isinstance(p.get(i), list) else p.get(i)) or "")) for i in ids]
    return ids, ref_sets, ments


def per_image(ment: list[set], gold: list[set]) -> np.ndarray:
    """(N, 4): TP, |M|, recall (nan if no gold), has_gold."""
    out = np.empty((len(gold), 4))
    for n, (m, g) in enumerate(zip(ment, gold)):
        tp = len(m & g)
        out[n] = (tp, len(m), tp / len(g) if g else np.nan, 1.0 if g else 0.0)
    return out


def prf(rows: np.ndarray, w: np.ndarray | None = None) -> tuple[float, float, float, float]:
    """object_prf convention; w = bootstrap multiplicities. Returns P, R, F1 (in %), M per image."""
    w = np.ones(len(rows)) if w is None else w
    tp, m = (w * rows[:, 0]).sum(), (w * rows[:, 1]).sum()
    hg = rows[:, 3] > 0
    p = tp / m if m else 0.0
    r = (w[hg] * rows[hg, 2]).sum() / w[hg].sum()
    f = 2 * p * r / (p + r) if p + r else 0.0
    return 100 * p, 100 * r, 100 * f, m / w.sum()


def slope(x: np.ndarray, y: np.ndarray) -> float:
    dx = x - x.mean()
    return float((dx * (y - y.mean())).sum() / (dx ** 2).sum())


def mstar(names, table, gbar) -> dict:
    """Fit log TP = a + b log M and log R = c + d log M over `names`; return micro closed form and the
    numeric argmax of F(M) = 2PR/(P+R) on the fitted curves (mixed micro-P / macro-R metric)."""
    M = np.array([table[s][3] for s in names]); P = np.array([table[s][0] for s in names]) / 100
    R = np.array([table[s][1] for s in names]) / 100
    lm, ltp, lr = np.log(M), np.log(P * M), np.log(R)
    b = slope(lm, ltp); a = ltp.mean() - b * lm.mean()
    d = slope(lm, lr); c = lr.mean() - d * lm.mean()
    grid = np.exp(np.linspace(np.log(0.2), np.log(60), 4000))
    Pg, Rg = np.exp(a) * grid ** (b - 1), np.minimum(np.exp(c) * grid ** d, 1.0)
    Fg = 2 * Pg * Rg / (Pg + Rg)
    return {"b": round(b, 3), "d_recall": round(d, 3), "Mstar_micro": round(b * gbar / (1 - b), 2) if b < 1 else None,
            "Mstar_mixed": round(float(grid[Fg.argmax()]), 2), "M_range": [round(M.min(), 2), round(M.max(), 2)]}


def main() -> None:
    ids, ref_sets, ments = load()
    names = list(ments)
    ft = [s for s in names if not FT_EXCLUDE.match(s)]
    rng = np.random.default_rng(0)
    W = rng.multinomial(len(ids), np.full(len(ids), 1 / len(ids)), size=NBOOT).astype(float)
    out = {"matcher_sha256": hashlib.sha256((ROOT / "rescap/chair.py").read_bytes()).hexdigest()[:8],
           "n_img": len(ids), "n_sys": len(names), "n_ft": len(ft), "gold": {}}
    for k in range(1, 6):
        for mode in ("firstk", "randk"):
            if mode == "firstk":
                golds = [[set().union(*ref_sets[i][:k]) for i in ids]]
            else:
                golds = []
                for _ in range(NSUB):
                    golds.append([set().union(*[ref_sets[i][j] for j in rng.choice(5, k, replace=False)])
                                  for i in ids])
            # average P/R/F1/M over subsets (point) and over subsets x bootstrap draws (slope CI)
            rows = {s: [per_image(ments[s], g) for g in golds] for s in names}
            table = {s: tuple(np.mean([prf(r) for r in rows[s]], 0)) for s in names}
            gbar = float(np.mean([np.mean([len(x) for x in g if x]) for g in golds]))
            res = {"Gbar": round(gbar, 3), "empty_gold_share": round(float(np.mean([np.mean([not x for x in g])
                                                                                    for g in golds])), 3)}
            for label, group in (("ft", ft), ("all", names)):
                lm = np.log([table[s][3] for s in group]); f1 = np.array([table[s][2] for s in group])
                bs = []
                for wb in W[:200 if mode == "randk" else NBOOT]:
                    t = [np.mean([prf(r, wb) for r in rows[s]], 0) for s in group] if mode == "firstk" else \
                        [prf(rows[s][rng.integers(NSUB)], wb) for s in group]
                    t = np.array(t)
                    bs.append(slope(np.log(t[:, 3]), t[:, 2]))
                res[label] = {"corr_logM_F1": round(float(np.corrcoef(lm, f1)[0, 1]), 3),
                              "slope_F1_per_logM": round(slope(lm, f1), 2),
                              "slope_ci": [round(float(np.percentile(bs, 2.5)), 2),
                                           round(float(np.percentile(bs, 97.5)), 2)],
                              **mstar(group, table, gbar)}
            out["gold"][f"k{k}_{mode}"] = res
            print(f"k={k} {mode:6s} Gbar={res['Gbar']:.2f} empty={res['empty_gold_share']:.3f} | "
                  + " | ".join(f"{g}: corr {res[g]['corr_logM_F1']:+.2f} slope {res[g]['slope_F1_per_logM']:+.2f} "
                               f"{res[g]['slope_ci']} b {res[g]['b']:.3f} M*micro {res[g]['Mstar_micro']} "
                               f"M*mixed {res[g]['Mstar_mixed']} Mrange {res[g]['M_range']}"
                               for g in ("ft", "all")), flush=True)
    Path(__file__).resolve().parents[1].joinpath("check_mstar.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
