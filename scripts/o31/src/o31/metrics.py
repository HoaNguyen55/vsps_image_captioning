"""Object metrics, count-matched precision (W2), paired bootstrap, H1-H5 with Holm (W3), tier-2 rehearsal (§7).

Every registered statistic is a ratio of sums of per-image columns, recomputed inside each replicate.
Bootstrap: numpy PCG64 (default_rng(seed)), one (B, n) index matrix drawn in row chunks and shared by every
statistic; percentile CI = sorted[int(0.025 B)], sorted[int(0.975 B) - 1] (object_prf.py convention, sha 6b711280).
An undefined replicate (zero denominator) is NaN: it is counted, left out of the CI, and counted on the null side
of every p-value (conservative).
"""
from __future__ import annotations

import numpy as np

B_MAIN, SEED_MAIN = 10_000, 20261127
B_OUT, B_IN, N_SUB, SEED_REH = 1_000, 1_000, 4_224, 20261128
ALPHA, MARGIN_H2, RHO_MIN, GAP_MIN = 0.05, 0.25, 0.50, 2.0
H3_NULL, H4_POINT, H4_FA = -2.0, 10.0, 5.0
CHUNK = 500


# ------------------------------------------------------------------ per caption / per image
def counts(m: set, g: set) -> dict:
    """The four counts of Objective 3.2 for one caption (distinct classes)."""
    return {"m": len(m), "tp": len(m & g), "fp": len(m - g), "fn": len(g - m), "g": len(g)}


def aggregate(rows: list[dict]) -> dict:
    """R = 100 sum TP / sum |G|; h = sum FP / N; CHAIR_i = 100 sum FP / sum m; CHAIR_s; P; F1."""
    s = {k: sum(r[k] for r in rows) for k in ("m", "tp", "fp", "g")}
    n = len(rows)
    r = 100 * s["tp"] / s["g"] if s["g"] else float("nan")
    p = 100 * s["tp"] / s["m"] if s["m"] else float("nan")
    return {"n": n, "R": r, "h": s["fp"] / n if n else float("nan"), "P": p,
            "F1": 2 * p * r / (p + r) if p == p and r == r and p + r else float("nan"),
            "CHAIR_i": 100 * s["fp"] / s["m"] if s["m"] else float("nan"),
            "CHAIR_s": 100 * sum(x["fp"] > 0 for x in rows) / n if n else float("nan")}


def cmp_counts(order_x: list[str], order_y: list[str], gold: set) -> tuple[int, int, int]:
    """W2 for one image: k = min(m_X, m_Y) over distinct classes in first-mention order;
    returns (TP_X(k), TP_Y(k), k)."""
    ux, uy = list(dict.fromkeys(order_x)), list(dict.fromkeys(order_y))
    k = min(len(ux), len(uy))
    return sum(c in gold for c in ux[:k]), sum(c in gold for c in uy[:k]), k


def cmp_score(tpk: np.ndarray, k: np.ndarray) -> dict:
    """CMP = 100 sum TP(k) / sum k over images with k > 0; images with k = 0 are counted."""
    keep = k > 0
    return {"CMP": 100 * tpk[keep].sum() / k[keep].sum() if keep.any() else float("nan"),
            "n_used": int(keep.sum()), "n_k0": int((~keep).sum())}


def seed_mean(per_seed: list[np.ndarray]) -> np.ndarray:
    """Each image's caption-level count averaged over seeds before resampling (§6.3)."""
    return np.mean(np.stack(per_seed), axis=0)


# ------------------------------------------------------------------ bootstrap engine
def index_chunks(n: int, b: int, seed: int, chunk: int = CHUNK):
    rng = np.random.default_rng(seed)
    done = 0
    while done < b:
        c = min(chunk, b - done)
        yield rng.integers(0, n, size=(c, n))
        done += c


def _ratio(num, den):
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(den != 0, num / np.where(den != 0, den, 1), np.nan)


def statistics_of(S: dict) -> dict:
    """Every registered statistic from column sums S (scalars or arrays over replicates).
    Columns: n; tp_k, g_k, fp_k for k in S0, S1, S2 (VI) and e0, e1, e2 (EN); cmp_x, cmp_y, cmp_k (S2 vs S1);
    pr_n, pr_o, pr_f, ab_n, ab_o, ab_f (V-COCO units: present/absent totals, supported by V_O31 / V_FAIR)."""
    out = {}
    for lang, (a, b, c) in {"vi": ("S0", "S1", "S2"), "en": ("e0", "e1", "e2")}.items():
        if f"tp_{a}" not in S:
            continue
        R = {k: 100 * _ratio(S[f"tp_{k}"], S[f"g_{k}"]) for k in (a, b, c)}
        h = {k: _ratio(S[f"fp_{k}"], S["n"]) for k in (a, b, c)}
        out[f"{lang}.dR21"] = R[c] - R[b]
        out[f"{lang}.gap01"] = R[a] - R[b]
        out[f"{lang}.rho"] = _ratio(R[c] - R[b], R[a] - R[b])
        out[f"{lang}.D"] = (h[c] - h[b]) - MARGIN_H2 * (h[a] - h[b])
    if "cmp_k" in S:
        out["H3.d"] = 100 * _ratio(S["cmp_x"], S["cmp_k"]) - 100 * _ratio(S["cmp_y"], S["cmp_k"])
    if "pr_n" in S:
        out["H4.dRT"] = 100 * _ratio(S["pr_o"], S["pr_n"]) - 100 * _ratio(S["pr_f"], S["pr_n"])
        out["H4.dFA"] = 100 * _ratio(S["ab_o"], S["ab_n"]) - 100 * _ratio(S["ab_f"], S["ab_n"])
    return out


def bootstrap(cols: dict[str, np.ndarray], b: int = B_MAIN, seed: int = SEED_MAIN) -> tuple[dict, dict]:
    """(point statistics, {stat: replicate array}) with one shared index matrix."""
    n = len(next(iter(cols.values())))
    cols = {**{k: np.asarray(v, float) for k, v in cols.items()}, "n": np.ones(n)}
    point = {k: float(v) for k, v in statistics_of({k: v.sum() for k, v in cols.items()}).items()}
    reps: dict[str, list] = {k: [] for k in point}
    for idx in index_chunks(n, b, seed):
        st = statistics_of({k: v[idx].sum(axis=1) for k, v in cols.items()})
        for k in point:
            reps[k].append(st[k])
    return point, {k: np.concatenate(v) for k, v in reps.items()}


def ci(rep: np.ndarray) -> tuple[float, float, int]:
    """Percentile 95 % CI over defined replicates, and the undefined count."""
    ok = np.sort(rep[~np.isnan(rep)])
    nb = len(ok)
    if not nb:
        return float("nan"), float("nan"), len(rep)
    return float(ok[int(0.025 * nb)]), float(ok[int(0.975 * nb) - 1]), int(len(rep) - nb)


def p_null(rep: np.ndarray, null: float, side: str) -> float:
    """W3: p = (1 + #{b on the null side}) / (1 + B); side 'le' = null is d <= null, 'ge' = d >= null (inclusive)."""
    on = (rep <= null) if side == "le" else (rep >= null)
    return (1 + int(on.sum()) + int(np.isnan(rep).sum())) / (1 + len(rep))


def holm(p: dict[str, float]) -> dict[str, float]:
    """Holm step-down adjusted p (cumulative max), ties in name order."""
    order = sorted(p, key=lambda k: (p[k], k))
    m, run, out = len(order), 0.0, {}
    for i, k in enumerate(order):
        run = max(run, min(1.0, (m - i) * p[k]))
        out[k] = run
    return out


# ------------------------------------------------------------------ hypotheses
def primary(point: dict, reps: dict, lang: str = "vi") -> dict:
    """H1 and H2 (IUT, no correction)."""
    lo, _, und1 = ci(reps[f"{lang}.dR21"])
    _, hi, und2 = ci(reps[f"{lang}.D"])
    gap, rho = point[f"{lang}.gap01"], point[f"{lang}.rho"]
    h1 = "NOT_IDENTIFIED" if not gap >= GAP_MIN else "PASS" if rho >= RHO_MIN and lo > 0 else "FAIL"
    h2 = "PASS" if hi < 0 else "FAIL"
    return {"H1": h1, "H1.rho": rho, "H1.gap": gap, "H1.dR_ci_lo": lo, "H2": h2, "H2.D": point[f"{lang}.D"],
            "H2.D_ci_hi": hi, "undefined": und1 + und2, "primary": "PASS" if h1 == h2 == "PASS" else "FAIL"}


def secondary(point: dict, reps: dict) -> dict:
    """H3, H4, H5a, H5b: one-sided bootstrap p, Holm-adjusted (W3); unadjusted CIs beside each member."""
    p = {"H3": p_null(reps["H3.d"], H3_NULL, "le"),
         "H4": max(p_null(reps["H4.dRT"], 0.0, "le"), p_null(reps["H4.dFA"], H4_FA, "ge")),
         "H5a": p_null(reps["en.dR21"], 0.0, "le"),
         "H5b": p_null(reps["en.D"], 0.0, "ge")}
    adj = holm(p)
    point_ok = {"H3": True, "H4": point["H4.dRT"] >= H4_POINT, "H5a": True, "H5b": True}
    stat = {"H3": "H3.d", "H4": "H4.dRT", "H5a": "en.dR21", "H5b": "en.D"}
    out = {}
    for k in p:
        lo, hi, und = ci(reps[stat[k]])
        out[k] = {"p": p[k], "p_holm": adj[k], "point": point[stat[k]], "ci95": (lo, hi), "undefined": und,
                  "verdict": "PASS" if adj[k] < ALPHA and point_ok[k] else "FAIL"}
    out["H4"]["dFA_point"], out["H4"]["dFA_ci95"] = point["H4.dFA"], ci(reps["H4.dFA"])[:2]
    return out


# ------------------------------------------------------------------ tier-2 rehearsal
def rehearsal(cols: dict[str, np.ndarray], b_out: int = B_OUT, b_in: int = B_IN, n_sub: int = N_SUB,
              seed: int = SEED_REH) -> dict:
    """P(PASS): share of outer draws (n_sub images WITH replacement, v3 §7) where H1 and H2 both PASS with b_in
    inner replicates. Outer and inner indices come from one PCG64 stream: outer draw j, then its b_in rows.
    H3-H5b pass shares are reported when their columns exist; they never gate."""
    n = len(next(iter(cols.values())))
    cols = {k: np.asarray(v, float) for k, v in cols.items()}
    rng = np.random.default_rng(seed)
    wins, sec, uniq = 0, {"H3": 0, "H4": 0, "H5a": 0, "H5b": 0}, 0.0
    for _ in range(b_out):
        sub = rng.integers(0, n, size=n_sub)
        uniq += len(np.unique(sub)) / n_sub
        sc = {k: v[sub] for k, v in cols.items()}
        sc["n"] = np.ones(n_sub)
        point = {k: float(v) for k, v in statistics_of({k: v.sum() for k, v in sc.items()}).items()}
        reps: dict[str, list] = {k: [] for k in point}
        done = 0
        while done < b_in:
            c = min(CHUNK, b_in - done)
            idx = rng.integers(0, n_sub, size=(c, n_sub))
            st = statistics_of({k: v[idx].sum(axis=1) for k, v in sc.items()})
            for k in reps:
                reps[k].append(st[k])
            done += c
        reps = {k: np.concatenate(v) for k, v in reps.items()}
        wins += primary(point, reps)["primary"] == "PASS"
        if {"H3.d", "H4.dRT", "en.dR21"} <= set(point):
            for k, v in secondary(point, reps).items():
                sec[k] += v["verdict"] == "PASS"
    out = {"P_PASS": wins / b_out, "gate": wins / b_out >= 0.98, "b_out": b_out, "b_in": b_in, "n_sub": n_sub,
           "outer_unique_share": uniq / b_out}  # about 0.63 at n_sub = n when drawn with replacement (E10)
    if any(sec.values()) or {"cmp_k", "pr_n", "tp_e0"} <= set(cols):
        out["secondary_pass_share_not_gating"] = {k: v / b_out for k, v in sec.items()}
    return out
