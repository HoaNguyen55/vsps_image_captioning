#!/usr/bin/env python3
"""PASCAL-50S companion evaluator (Paper A): manuscript/prereg/2026-10-29_a_companion/RULE.md, prereg_id
2026-10-29_a_p50_companion (CC-158 W1). X1/X2 (few-reference extrapolation), X4/X5 (salience excess over a
size-matched random-deletion null), Holm over the companion family and a descriptive family-wise reading with
P50-A4/O2. Runs inside p50_job.sh after `p50.py score` and before the data are deleted; it is part of P50's one look.
Numbers only. Reuses p50.py (ids, references, draw, V20, VOC gold, bootstrap constants) and score_g2b (rows, scores,
stat_slope, verdict, compound) unchanged.

  p50x.py --selftest                                         CPU, synthetic data only
  p50x.py score --raw DIR --stage S --decide D --out O       after p50.py score; refuses if O exists
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p50  # noqa: E402  (also puts the repo, scripts/, scripts/g2b, scripts/lb on sys.path)

PREREG_ID = "2026-10-29_a_p50_companion"
RESTORE_X1 = False  # CC-159 ruling 1: X1 stays descriptive (RULE §2.2); X2 has no confirmatory path (ruling 2)
T_REFS, X_LEVELS = 5, (1, 5)  # X1/X2 input rung; X4 levels
R_NULL, NULL_SEED, ALPHA = 1000, 0, 0.025
MIN_RUNS_X1 = 6


# ------------------------------------------------------------------------------------------- estimator (frozen, §2.1)
def f0_hat(q1, q2, T: int, K: float):
    """Unseen true mentions from T to K references (Chao et al. 2014, incidence); K = inf is the Chao2 asymptote."""
    q1, q2 = np.asarray(q1, float), np.asarray(q2, float)
    if T < 2:
        return np.zeros_like(q1)
    a = (T - 1) / T
    q0 = np.where(q2 > 0, a * q1 ** 2 / (2 * np.maximum(q2, 1)), a * q1 * np.maximum(q1 - 1, 0) / 2)
    if np.isinf(K):
        return q0
    with np.errstate(divide="ignore", invalid="ignore"):
        base = np.where(q0 > 0, 1 - q1 / (T * q0 + q1), 1.0)
    return np.where(q0 > 0, q0 * (1 - base ** (K - T)), 0.0)


def jack1(q1, T: int):
    return np.asarray(q1, float) * (T - 1) / T


def tau_b(x, y):
    """Kendall tau-b over axis 0 (runs), per column (score_a_n2.tau_b); nan when a vector is all ties."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    i, j = np.triu_indices(len(x), 1)
    dx, dy = np.sign(x[i] - x[j]), np.sign(y[i] - y[j])
    with np.errstate(invalid="ignore", divide="ignore"):
        return (dx * dy).sum(0) / np.sqrt((dx != 0).sum(0) * (dy != 0).sum(0))


def incidence(ments, refs, subsets, truth) -> dict:
    """(run, subset, image): TP_obs, Q1, Q2 of the mentioned classes over the drawn references; (run, image): M and
    TP against the truth; (subset, image): drawn gold size; (image): truth size."""
    X, S, N = len(ments), len(subsets), len(refs)
    tp, q1, q2 = (np.zeros((X, S, N)) for _ in range(3))
    gk = np.zeros((S, N))
    for s, sub in enumerate(subsets):
        for i in range(N):
            rs = [refs[i][j] for j in sub[i]]
            gk[s, i] = len(set().union(*rs))
            for x in range(X):
                y = [sum(c in r for r in rs) for c in ments[x][i]]
                tp[x, s, i], q1[x, s, i], q2[x, s, i] = sum(v >= 1 for v in y), y.count(1), y.count(2)
    m = np.array([[len(a) for a in mx] for mx in ments], float)
    tt = np.array([[len(a & t) for a, t in zip(mx, truth)] for mx in ments], float)
    return {"tp": tp, "q1": q1, "q2": q2, "m": m, "tt": tt, "gk": gk, "gt": np.array([len(t) for t in truth], float)}


def precisions(A: dict, W: np.ndarray, T: int, K: float) -> dict:
    """Precision (%) per run and weight column (X, B): raw, the two uniform corrections (pooled-uniform, G-bar ratio),
    Chao and jackknife-1, and the truth. The subset mean is taken after each estimator (score_g2b convention)."""
    tp, q1, q2 = (A[k] @ W.T for k in ("tp", "q1", "q2"))
    m = (A["m"] @ W.T)[:, None, :]
    p = {"raw": tp / m, "chao": np.minimum(tp + f0_hat(q1, q2, T, K), m) / m,
         "jack1": np.minimum(tp + jack1(q1, T), m) / m}
    pooled = np.minimum(tp.sum(0) + f0_hat(q1.sum(0), q2.sum(0), T, K), m.sum(0)) / tp.sum(0)
    p["uniform_pooled"] = np.minimum(tp * pooled[None] / m, 1.0)
    p["gbar_ratio"] = np.minimum(tp * ((A["gt"] @ W.T) / (A["gk"] @ W.T))[None] / m, 1.0)
    out = {k: 100 * v.mean(1) for k, v in p.items()}
    out["truth"] = 100 * (A["tt"] @ W.T) / (A["m"] @ W.T)
    return out


# ------------------------------------------------------------------------------------------- null (SCAR_DESIGN, §3.1)
def null_slopes(g, comp, ks, ments, idx, rng, n_rep: int) -> np.ndarray:
    """scar_null.null_slopes with the gold passed in: one uniform permutation per (replicate, image) of sorted(C_i) over
    ALL images; subset s keeps the first k_i^(s); shared by every run; statistic stat_slope over the runs."""
    comp = [sorted(c) for c in comp]
    out = np.empty(n_rep)
    one = np.ones((1, len(idx)))
    for r in range(n_rep):
        perms = [[c[j] for j in rng.permutation(len(c))] for c in comp]
        gold = [[set(p[:k]) for p, k in zip(perms, kk)] for kk in ks]
        out[r] = float(g.stat_slope([g.scores(g.rows(m, gold), idx, one) for m in ments], None)[0])
    return out


def obs_slope(g, ments, golds, idx) -> float:
    one = np.ones((1, len(idx)))
    return float(g.stat_slope([g.scores(g.rows(m, golds), idx, one) for m in ments], None)[0])


def salience(g, ments, golds, comp, idx, rng, n_rep, evaluable: bool) -> dict:
    inter = [[s & c for s, c in zip(gs, comp)] for gs in golds]
    ks = [[len(x) for x in gs] for gs in inter]
    null = null_slopes(g, comp, ks, ments, idx, rng, n_rep)
    obs = obs_slope(g, ments, inter, idx)
    lo, med, hi = (float(np.percentile(null, q)) for q in (2.5, 50, 97.5))
    v = "NOT_EVALUABLE" if not evaluable or lo == hi or not np.isfinite(obs) else \
        "PASS" if obs < lo else "FAIL" if obs >= med else "INCONCLUSIVE"
    return {"observed": obs, "null_mean": float(null.mean()), "null_lo": lo, "null_median": med, "null_hi": hi,
            "excess": obs - float(null.mean()), "p_one_sided": float((1 + (null <= obs).sum()) / (n_rep + 1)),
            "sum_k_scored_mean": float(np.mean([sum(k[i] for i in idx) for k in ks])),
            "sum_complete_scored": int(sum(len(comp[i]) for i in idx)), "verdict": v}


def holm(ps: dict[str, float], alpha: float = ALPHA) -> dict[str, bool]:
    """Step-down Holm: True = survives."""
    order, keep, ok = sorted(ps, key=ps.get), {}, True
    for j, k in enumerate(order):
        ok = ok and ps[k] <= alpha / (len(order) - j)
        keep[k] = ok
    return keep


# ------------------------------------------------------------------------------------------- the companion analysis
def analysis(g, ids, refs, voc, caps, models, label_rung="kept", n_boot=p50.N_BOOT, n_rep=R_NULL,
             restore_x1=RESTORE_X1) -> dict:
    en, V = g.MATCH["coco80"]["en"], set(p50.V20.values())
    runs = [f"p50_{m}-{q}" for m in models for q in p50.MODES]
    ment = [[en(caps[r].get(i, "")) for i in ids] for r in runs]
    refm = [[en(s) for s in refs[i]] for i in ids]
    sub = p50.draw([len(x) for x in refm])
    clean = [n for n, i in enumerate(ids)
             if all(isinstance(caps[r].get(i), str) and caps[r][i].strip() and g.is_clean(caps[r][i], "en") for r in runs)]
    if not clean:
        return {"status": "NOT_EVALUABLE", "reason": "empty analysis set"}
    idx, N = np.array(clean), len(clean)
    W = np.vstack([np.ones(N), np.random.default_rng(p50.BOOT_SEED).multinomial(N, [1 / N] * N, size=n_boot)]).astype(float)
    ci = lambda v: g.ci(v[1:], *p50.CI)  # noqa: E731
    res = {"prereg_id": PREREG_ID, "runs": runs, "n_runs": len(runs), "n_images": N, "restore_x1": restore_x1}

    # X1, X2 (§2): k = 5 rung of the P50 draw, truth refs50, analysis set only
    refs50 = [set().union(*r) for r in refm]
    keep = lambda L: [L[n] for n in clean]  # noqa: E731
    A = incidence([keep(m) for m in ment], keep(refm), [keep(s) for s in sub[T_REFS]], keep(refs50))
    m_ok = bool(np.all(A["m"].sum(1) > 0))
    P = precisions(A, W, T_REFS, 50)
    mae = {e: np.abs(P[e] - P["truth"]).mean(0) for e in ("raw", "uniform_pooled", "gbar_ratio", "chao", "jack1")}
    d1 = mae["jack1"] - np.minimum(mae["uniform_pooled"], mae["gbar_ratio"])
    x1_ne = not m_ok or len(runs) < MIN_RUNS_X1
    x1v = "NOT_EVALUABLE" if x1_ne else g.verdict("sign_lt_0", float(d1[0]), ci(d1))
    res["X1"] = {"point": float(d1[0]), "ci95": ci(d1), "p_one_sided": float((1 + (d1[1:] >= 0).sum()) / (n_boot + 1)),
                 "mae_pp": {e: float(v[0]) for e, v in mae.items()},
                 "verdict": x1v if restore_x1 else None, "rule_outcome_descriptive": x1v,
                 "precision_point": {e: dict(zip(runs, P[e][:, 0].tolist())) for e in P}}
    traw, tj = tau_b(P["raw"], P["truth"]), tau_b(P["jack1"], P["truth"])
    d2 = tj - traw
    res["X2"] = {"tau_raw": float(traw[0]), "tau_jack1": float(tj[0]), "point": float(d2[0]), "ci95": ci(d2),
                 "p_one_sided": float((1 + (d2[1:] <= 0).sum()) / (n_boot + 1)),
                 "n_runs": len(runs), "verdict": None}  # numbers only, no verdict wording (CC-159 ruling 2)

    # X4, X5 (§3): one default_rng(0) stream, prediction -> level -> replicate -> image
    rng = np.random.default_rng(NULL_SEED)
    ev = lambda ms: all(np.mean([len(x) for x in [ms_[i] for i in clean]]) > 0 for ms_ in ms) and \
        len({round(float(np.mean([len(ms_[i]) for i in clean])), 12) for ms_ in ms}) >= 2  # noqa: E731
    x4 = {}
    for k in X_LEVELS:
        golds = [[set().union(*(refm[i][j] for j in s[i])) for i in range(len(ids))] for s in sub[k]]
        x4[f"refs{k}_randk"] = salience(g, ment, golds, refs50, idx, rng, n_rep, ev(ment))
    res["X4"] = {"levels": x4, "verdict": g.compound([v["verdict"] for v in x4.values()]),
                 "p_one_sided": max(v["p_one_sided"] for v in x4.values())}
    if label_rung != "kept":
        res["X5"] = {"verdict": "NOT_EVALUABLE", "reason": f"label rung {label_rung}", "p_one_sided": None}
    else:
        mv = [[x & V for x in m] for m in ment]
        g1 = [[set().union(*(refm[i][j] & V for j in s[i])) for i in range(len(ids))] for s in sub[1]]
        comp = [voc[i] for i in ids]
        r5 = salience(g, mv, g1, comp, idx, rng, n_rep, ev(mv))
        if r5["sum_complete_scored"] < 2 * r5["sum_k_scored_mean"]:
            r5["verdict"] = "NOT_EVALUABLE"
            r5["reason"] = "sum |voc20| < 2 * sum k_i"
        res["X5"] = {"levels": {"refs1_randk|V20": r5}, "verdict": r5["verdict"], "p_one_sided": r5["p_one_sided"]}

    # Holm over the companion family (§5); NOT_EVALUABLE members leave first
    fam = {"X4": res["X4"], "X5": res["X5"]} | ({"X1": res["X1"]} if restore_x1 else {})
    ps = {k: v["p_one_sided"] for k, v in fam.items() if v["verdict"] not in (None, "NOT_EVALUABLE")}
    kept = holm(ps)
    res["holm_companion"] = {"alpha_one_sided": ALPHA, "family": sorted(fam), "p": ps, "survives": kept,
                             "final": {k: ("PASS" if fam[k]["verdict"] == "PASS" and kept.get(k) else fam[k]["verdict"])
                                       + ("" if fam[k]["verdict"] != "PASS" or kept.get(k) else
                                          " (not significant after Holm)") for k in fam}}
    return res


def p50_part_ps(g, ids, refs, voc, caps, models, decide_parts: dict, n_boot=p50.N_BOOT) -> dict:
    """Bootstrap p of every P50-A4 / P50-O2 part, recomputed exactly as p50.analysis on() does (same golds, same
    default_rng(BOOT_SEED) weights); each recomputed point must equal the decide file's point."""
    en, V = g.MATCH["coco80"]["en"], set(p50.V20.values())
    runs = [f"p50_{m}-{q}" for m in models for q in p50.MODES]
    refm = [[en(s) for s in refs[i]] for i in ids]
    sub = p50.draw([len(x) for x in refm])
    var = {"coco80": g.gold_variants({"refs": refm}, sub),
           "V20": g.gold_variants({"refs": [[s & V for s in r] for r in refm]}, sub)}
    var["V20"]["voc20"] = [[voc.get(i, set()) for i in ids]]
    for v in var.values():
        v["refs50"] = v.pop("refs_all")
    ment = {r: [en(caps[r].get(i, "")) for i in ids] for r in runs}
    mentv = {"coco80": ment, "V20": {r: [m & V for m in ment[r]] for r in runs}}
    clean = np.array([n for n, i in enumerate(ids) if all(isinstance(caps[r].get(i), str) and caps[r][i].strip()
                                                         and g.is_clean(caps[r][i], "en") for r in runs)])
    N = len(clean)
    Wb = np.random.default_rng(p50.BOOT_SEED).multinomial(N, [1 / N] * N, size=n_boot).astype(float)
    one, cache = np.ones((1, N)), {}

    def sl(lx, gd):
        if (lx, gd) not in cache:
            rows = [g.rows(mentv[lx][r], var[lx][gd]) for r in runs]
            cache[(lx, gd)] = (float(g.stat_slope([g.scores(x, clean, one) for x in rows], None)[0]),
                               g.stat_slope([g.scores(x, clean, Wb) for x in rows], None))
        return cache[(lx, gd)]

    out = {}
    for pid, parts in decide_parts.items():
        ps = []
        for q in parts:
            a, rest = q["stat"].split("slope[", 2)[1:]
            ga, la = a.split("](")[0].split("|")
            gb, lb = rest.split("](")[0].split("|")
            (pa, ra), (pb, rb) = sl(la, ga), sl(lb, gb)
            if abs((pa - pb) - q["point"]) > 1e-5:
                raise SystemExit(f"REFUSED: recomputed {q['stat']} differs from the decide file")
            ps.append(float((1 + ((ra - rb) <= 0).sum()) / (n_boot + 1)))
        out[pid] = max(ps)
    return out


def familywise(A: dict, p_p50: dict, res: dict) -> dict:
    """Descriptive Holm over {P50-A4 or P50-A4r, P50-O2, X4, X5} only (CC-159 W8); X1 and X2 never enter."""
    fw = {k: v for k, v in p_p50.items() if A[k]["verdict"] != "NOT_EVALUABLE"} | \
        {k: res[k]["p_one_sided"] for k in ("X4", "X5") if res[k]["verdict"] != "NOT_EVALUABLE"}
    return {"note": "P50 verdicts unchanged (CC-144 ruling 6); Holm reading only", "p": fw, "survives": holm(fw)}


def score(raw: Path, stage: dict, decide: dict, out: Path) -> dict:
    import score_g2b as g

    if out.exists():
        raise SystemExit("REFUSED: p50x decide file exists (one look)")
    base = {"prereg_id": PREREG_ID, "p50_prereg_id": p50.PREREG_ID, "restore_x1": RESTORE_X1,
            "self_sha256": p50.sha_file(Path(__file__))}
    if decide.get("status") != "SCORED":
        return base | {"status": f"not run: P50 status {decide.get('status')}"}
    ids, models = p50.id_list(), decide["models"]
    refs = p50.load_refs(p50.DATA_ROOT / "pascal50S.json", ids)
    caps = {}
    for m in models:
        for q in p50.MODES:
            f = raw / f"p50_{m}-{q}.preds.json"
            if Path(str(f) + ".sha256").read_text().split()[0] != p50.sha_file(f):
                raise SystemExit(f"REFUSED: sidecar sha differs for {f.name}")
            caps[f"p50_{m}-{q}"] = g.read_captions(f)
    rung = stage["label_rung"]
    voc = {i: p50.voc_gold((p50.DATA_ROOT / f"Annotations/{i}.xml").read_bytes()) for i in ids} if rung == "kept" else {}
    res = analysis(g, ids, refs, voc, caps, models, label_rung=rung)
    if "X4" not in res:  # empty analysis set: a record, never an exception (CC-159 W2 (iv))
        return base | {"status": "NOT_EVALUABLE", "reason": res.get("reason", "no companion statistic")}
    A = decide["analysis_set"]
    parts = {p: A[p]["parts"] for p in ("P50-A4", "P50-A4r", "P50-O2") if "parts" in A.get(p, {})}
    p_p50 = p50_part_ps(g, ids, refs, voc, caps, models, parts)
    res["familywise_descriptive"] = familywise(A, p_p50, res)
    return base | {"status": "SCORED"} | res


# ------------------------------------------------------------------------------------------- self-test (CPU)
def selftest() -> None:
    import score_g2b as g

    ok: list[str] = []

    def check(name, cond):
        if not cond:
            raise AssertionError(name)
        ok.append(name)

    check("Chao2: classic and bias-corrected forms; t = 0 adds nothing; K grows to the asymptote",
          np.isclose(f0_hat(4, 2, 5, np.inf), 3.2) and np.isclose(f0_hat(4, 0, 5, np.inf), 4.8)
          and f0_hat(5, 2, 3, 3) == 0 and f0_hat(4, 2, 5, 10) < f0_hat(4, 2, 5, 50) <= f0_hat(4, 2, 5, np.inf) + 1e-9)
    check("jackknife-1: Q1 (T-1)/T; one reference adds nothing", jack1(10, 5) == 8 and jack1(9, 1) == 0)
    rng = np.random.default_rng(1)
    x, y = rng.integers(0, 4, 9).astype(float), rng.integers(0, 4, 9).astype(float)
    c = d = tx = ty = 0
    for i in range(9):
        for j in range(i + 1, 9):
            s = np.sign(x[i] - x[j]) * np.sign(y[i] - y[j])
            c, d, tx, ty = c + (s > 0), d + (s < 0), tx + (x[i] == x[j]), ty + (y[i] == y[j])
    check("tau_b equals a brute-force tau-b with ties", np.isclose(tau_b(x, y), (c - d) / np.sqrt((36 - tx) * (36 - ty))))
    check("holm: step-down, stops at the first failure",
          holm({"a": 0.001, "b": 0.02, "c": 0.012}) == {"a": True, "c": True, "b": True}
          and holm({"a": 0.001, "b": 0.03, "c": 0.02}) == {"a": True, "c": False, "b": False})
    # synthetic PASCAL-like set: 6 models x 2 prompts = 12 runs, 60 images, 50 references, salience-biased mentions
    words = ["person", "dog", "cat", "car", "bus", "chair", "bottle", "bird", "boat", "horse", "sheep", "cow", "train"]
    tid = [f"2008_{n:06d}" for n in range(60)]
    comp = {i: list(rng.choice(words, 5, replace=False)) for i in tid}  # first class = most salient
    refs = {i: [" and ".join(w for r_, w in enumerate(comp[i]) if rng.random() < (0.95 if r_ == 0 else 0.15)) or comp[i][0]
                for _ in range(50)] for i in tid}
    voc = {i: {p50.V20.get(w, w) for w in comp[i]} & set(p50.V20.values()) for i in tid}
    models = ["qwen3vl_8b", "qwen25vl_7b", "qwen25vl_3b", "smolvlm2_2b", "llava15_7b", "internvl3_8b"]
    caps = {}
    for j, m in enumerate(models):
        for q, n in (("short_en", 1), ("detailed_en", 2 + j % 3)):
            caps[f"p50_{m}-{q}"] = {i: " ".join(comp[i][:n] + ([words[(j + 3) % 13]] if n > 2 else [])) for i in tid}
    res = analysis(g, tid, refs, voc, caps, models, n_boot=50, n_rep=60)
    check("analysis: 12 runs, X1-X5 present, X1 descriptive by default", res["n_runs"] == 12 and res["X1"]["verdict"] is None
          and all(k in res for k in ("X1", "X2", "X4", "X5", "holm_companion")))
    check("X4: salience-biased references give observed below the null (PASS at both levels)",
          all(v["verdict"] == "PASS" for v in res["X4"]["levels"].values()))
    check("X2: numbers only, no verdict and no verdict wording (CC-159 ruling 2)", res["X2"]["verdict"] is None
          and set(res["X2"]) == {"tau_raw", "tau_jack1", "point", "ci95", "p_one_sided", "n_runs", "verdict"})
    r1 = analysis(g, tid, refs, voc, caps, models, n_boot=20, n_rep=20, restore_x1=True)
    check("restore_x1: X1 gets a verdict and joins the Holm family", r1["X1"]["verdict"] is not None
          and "X1" in r1["holm_companion"]["family"])
    r2 = analysis(g, tid, refs, voc, caps, models[:5], n_boot=20, n_rep=20)
    check("X2 on 10 runs: still numbers only", r2["X2"]["n_runs"] == 10 and r2["X2"]["verdict"] is None)
    r3 = analysis(g, tid, refs, voc, caps, models, n_boot=20, n_rep=20, label_rung="dropped (PREREG §4.4(c))")
    check("X5: label rung dropped -> NOT_EVALUABLE, leaves the Holm family",
          r3["X5"]["verdict"] == "NOT_EVALUABLE" and "X5" not in r3["holm_companion"]["p"])
    full = [set(comp[i]) for i in tid]
    ment = [[set(comp[i][:2]) for i in tid], [set(comp[i][:4]) for i in tid]]
    nl = salience(g, ment, [full], full, np.arange(60), np.random.default_rng(0), 30, True)
    check("null: k_i = |C_i| collapses the null onto the observed slope -> NOT_EVALUABLE",
          nl["verdict"] == "NOT_EVALUABLE" and nl["null_lo"] == nl["null_hi"] == nl["observed"])
    try:
        sys.path.insert(0, str(p50.ROOT / "scripts/scar"))
        import scar_null as sn
        part = [[set(comp[i][:1]) for i in tid], [set(comp[i][1:3]) for i in tid]]
        st = {"comp": full, "golds": {"L": part}, "ments": ment, "idx": np.arange(60)}
        a = sn.null_slopes(st, "L", np.random.default_rng(0), 15, 1e-9)
        b = null_slopes(g, full, [[len(x & c) for x, c in zip(gs, full)] for gs in part], ment, np.arange(60),
                        np.random.default_rng(0), 15)
        check("null: equals scripts/scar/scar_null.null_slopes draw for draw", np.allclose(a, b))
    except (Exception, SystemExit) as e:  # scar_null reads an untracked decision file at import; absent on M3
        ok.append(f"SKIPPED (scar_null not importable here: {e}) null equality check")
    parts = {"P50-O2": [{"stat": "slope[refs50|coco80](ALL) - slope[refs20_randk|coco80](ALL)"}]}
    pa = p50.analysis(g, tid, refs, voc, caps, models, n_boot=30)["analysis_set"]
    q = pa["P50-O2"]["parts"][-1]
    parts["P50-O2"][0]["point"] = q["point"]
    check("P50 part p: recomputed point equals p50.analysis (same golds, same weights)",
          0 < p50_part_ps(g, tid, refs, voc, caps, models, parts, n_boot=30)["P50-O2"] <= 1)
    fwr = familywise({"P50-A4": {"verdict": "PASS"}, "P50-O2": {"verdict": "NOT_EVALUABLE"}},
                     {"P50-A4": 0.001, "P50-O2": 0.5}, res)
    check("familywise Holm: P50-A4/A4r, P50-O2, X4, X5 only; X1 and X2 never; NOT_EVALUABLE members leave (W8)",
          set(fwr["p"]) <= {"P50-A4", "P50-A4r", "P50-O2", "X4", "X5"} and "P50-O2" not in fwr["p"] and "X4" in fwr["p"])
    empty = analysis(g, tid, refs, voc, {r: {i: "" for i in tid} for r in caps}, models, n_boot=5, n_rep=5)
    check("empty analysis set: a NOT_EVALUABLE record without X keys, which score() returns as a record (W2 (iv))",
          empty.get("status") == "NOT_EVALUABLE" and "X4" not in empty)
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "x.json"
        f.write_text(json.dumps(res, indent=1))
        h = p50.ngram_hits({i: refs[i] for i in tid}, [f])
        check("output holds numbers only (p50.ngram_hits: 0 hits on the result file)", h["files"]["x.json"] == 0)
    print("\n".join("PASS " + n if not n.startswith("SKIPPED") else n for n in ok) + "\np50x selftest ok")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?")
    ap.add_argument("--selftest", action="store_true")
    for f in ("--raw", "--stage", "--decide", "--out"):
        ap.add_argument(f)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd != "score":
        raise SystemExit("usage: p50x.py --selftest | score --raw DIR --stage S --decide D --out O")
    res = score(Path(a.raw), json.loads(Path(a.stage).read_text()), json.loads(Path(a.decide).read_text()), Path(a.out))
    p50.dump(res, a.out)
    print(json.dumps({"status": res["status"], **{k: res.get(k, {}).get("verdict") for k in ("X1", "X2", "X4", "X5")}}))


if __name__ == "__main__":
    main()
