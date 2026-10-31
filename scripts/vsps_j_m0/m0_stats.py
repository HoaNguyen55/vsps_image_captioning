"""VSPS-J M0 scoring statistics (PREREG section 6): matched-precision operating point, AUROC, paired image
bootstrap and the two stop rules. numpy only."""
from __future__ import annotations

import math

import numpy as np

SEED, B_BOOT, SESOI, AUROC_MIN, T_A = 20261031, 2000, 3.0, 0.65, 0.5


def cuts(p, y):
    """Flag iff P(yes) <= v, for each distinct v ascending (ties grouped). Returns (v, tp, fp)."""
    o = np.argsort(p, kind="stable")
    ps, ys = p[o], y[o]
    last = np.r_[ps[1:] != ps[:-1], True]
    return ps[last], np.cumsum(ys)[last], np.cumsum(1 - ys)[last]


def tau_matched(p, y, p0: float):
    """Highest-recall cut with precision >= p0; ties on recall -> fewer false flags. None if no cut reaches p0."""
    v, tp, fp = cuts(p, y)
    ok = np.flatnonzero(tp / (tp + fp) >= p0)
    if not len(ok):
        return None
    return float(v[ok[np.argmax(tp[ok])]])  # first max-tp cut = fewest false flags (tp, fp both non-decreasing)


def auroc(p, y) -> float:
    """Mann-Whitney AUROC of the Inaccurate class with score 1 - P(yes); ties count 1/2."""
    s = -p
    o = np.argsort(s, kind="mergesort")
    _, start, cnt = np.unique(s[o], return_index=True, return_counts=True)
    r = np.empty(len(s))
    r[o] = np.repeat(start + (cnt + 1) / 2, cnt)
    n1 = int(y.sum())
    n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def rp(flag, y) -> tuple[float, float]:
    tp = int((flag & (y == 1)).sum())
    return tp / max(int(y.sum()), 1), (tp / int(flag.sum()) if flag.sum() else float("nan"))


def prec_at_recall(p, y, r_min=0.8) -> float:
    v, tp, fp = cuts(p, y)
    ok = tp / y.sum() >= r_min
    return float((tp / (tp + fp))[ok].max()) if ok.any() else float("nan")


def stats(pA, pB, y) -> dict:
    rA, p0 = rp(pA < T_A, y)
    out = {"R_A": rA, "P_A": p0, "AUROC_A": auroc(pA, y)}
    if pB is not None:
        tau = tau_matched(pB, y, p0) if math.isfinite(p0) else None
        rB, pBp = rp(pB <= tau, y) if tau is not None else (0.0, float("nan"))
        out.update(tau_B=tau, R_B=rB, P_B=pBp, AUROC_B=auroc(pB, y), dR_pts=100 * (rB - rA))
    return out


def bootstrap(pA, pB, y, img, B: int = B_BOOT, seed: int = SEED) -> dict:
    """Paired percentile bootstrap resampling images; tau_B is re-selected inside every replicate."""
    ids = np.unique(img)
    groups = [np.flatnonzero(img == i) for i in ids]
    rng = np.random.default_rng(seed)
    keys = ("R_A", "AUROC_A") + (("R_B", "AUROC_B", "dR_pts") if pB is not None else ())
    reps = {k: [] for k in keys}
    for _ in range(B):
        ix = np.concatenate([groups[j] for j in rng.integers(0, len(ids), len(ids))])
        s = stats(pA[ix], None if pB is None else pB[ix], y[ix])
        for k in keys:
            reps[k].append(s[k])
    return {k: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] for k, v in reps.items()}


def decide(point: dict, ci: dict) -> dict:
    """Stop rules (program section 2, M0; PREREG section 6)."""
    if "dR_pts" in point:
        few = "KEEP" if point["dR_pts"] >= SESOI and ci["dR_pts"][0] > 0 else "DROP"
        aucs = (point["AUROC_A"], point["AUROC_B"])
    else:
        few, aucs = "N/A_ARM_B_DROPPED", (point["AUROC_A"],)
    return {"few_shot": few, "detector": "STOP_PIVOT" if all(a < AUROC_MIN for a in aucs) else "CONTINUE"}
