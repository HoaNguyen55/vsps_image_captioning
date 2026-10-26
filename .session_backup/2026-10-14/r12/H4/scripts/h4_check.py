#!/usr/bin/env python3
"""R12/H4 CPU check of the propensity theory of the gold-indexed count frontier (C2) and the verbosity sign flip (N1).

T1 kernel self-check: c_k(pi) = 1-(1-pi)^k and its 5-reference analogue w_k(n) = 1-C(5-n,k)/C(5,k) are RR2 in (k, pi):
   c_{k+1}/c_k falls with pi, so extra references help low-propensity objects relatively more.
T2 support profile: a system mention has support n = number of the 5 references naming it. Exact identity for the mean
   over all k-subsets: TP_k = sum_n h(n) w_k(n). Reports b(k) from the identity and the ratio r(n) = marginal/average
   share of support-n mentions along the family (the likelihood-ratio ordering assumption says r falls with n).
T3 exchangeability: golds from one reference slot (k=1) and from slot pairs (k=2); lag-1 vs lag>=2 pairs.
T4 sign statistic Lambda = logit(b) + ln Gbar - ln M0 (micro closed form: F1 rises with M iff Lambda > 0), split into a
   b-channel and a Gbar-channel between the sparsest and the fullest gold.
Families: KTVIC test FT ladder (36 systems, L1 FT_EXCLUDE) and COCO-2500 (9 systems, L1 check_coco). Metric = object_prf
(micro P, image-macro R over non-empty golds). Aggregates only; no caption text is written.
Run: nice -n 19 env OMP_NUM_THREADS=1 python3 h4_check.py OUT_DIR
"""
from __future__ import annotations

import json
import sys
from itertools import combinations
from math import comb
from pathlib import Path

import numpy as np

L1 = Path("/mnt/d/vsps_image_captioning/.session_backup/2026-10-14/r11_litmaps/L1")
sys.path.insert(0, str(L1 / "scripts"))
from check_mstar import FT_EXCLUDE, ROOT, load, mstar  # noqa: E402  (L1's KTVIC loader, FT family, M* fits)
from check_coco import karpathy_refs, sc  # noqa: E402  (sc = scripts/score_coco_probe.py)

B = 500
SLOTS = {f"s{j + 1}": (j,) for j in range(5)}
PAIRS = {f"p{a + 1}{b + 1}": (a, b) for a, b in combinations(range(5), 2)}


def w(k: int, n: int) -> float:
    """P(an object named by n of 5 references is in the union of a random k-subset)."""
    return 1 - comb(5 - n, k) / comb(5, k)


def _check() -> None:
    pi = np.linspace(0.01, 0.99, 99)
    c = lambda k: 1 - (1 - pi) ** k
    chain = lambda k, rho: 1 - (1 - pi) * (1 - (1 - rho) * pi) ** (k - 1)  # stationary lag-1 binary Markov chain
    for k in range(1, 10):
        assert np.all(np.diff(c(k + 1) / c(k)) < 0), k
    for rho in (0.2, 0.5, 0.8):
        for k in range(2, 6):
            assert np.all(chain(k, rho) <= c(k) + 1e-12) and np.all(np.diff(chain(k + 1, rho) / chain(k, rho)) < 0)
    for k in range(1, 5):
        r = [w(k + 1, n) / w(k, n) for n in range(1, 6)]
        assert all(x >= y - 1e-12 for x, y in zip(r, r[1:])), (k, r)
    rng = np.random.default_rng(3)  # identity: mean over all k-subsets of |m & union| = sum_o w_k(support(o))
    refs = [set(rng.choice(8, rng.integers(0, 5), replace=False)) for _ in range(5)]
    m = set(range(8))
    for k in range(1, 6):
        exact = np.mean([len(m & set().union(*(refs[j] for j in sub))) for sub in combinations(range(5), k)])
        ident = sum(w(k, sum(o in r for r in refs)) for o in m)
        assert abs(exact - ident) < 1e-9, (k, exact, ident)


def load_coco():
    """Copied from L1 check_coco.main: refs = first 5 Karpathy EN refs -> COCO-80; systems = VI outputs -> COCO-80."""
    vi, syn = sc.load_vi_terms(), sc.load_synonyms()
    cids = sorted(i["cocoid"] for i in json.loads((ROOT / "data/coco_probe/manifest.json").read_text("utf-8"))["images"])
    cinst = {int(k): set(v["coco"]) for k, v in json.loads((ROOT / "data/coco_probe/instance_gold.json").read_text()).items()}
    kr = karpathy_refs(set(cids))
    refs = [[sc.en_classes(s, syn) for s in kr[c][:5]] for c in cids]
    ments = {}
    for d in ("coco5000", "coco_transfer", "coco5000_vcd"):
        for f in sorted((ROOT / "data/results" / d).glob("*.shard*.jsonl")):
            name = f.name.split(".shard")[0] + ("+vcd" if d == "coco5000_vcd" else "")
            ms = {}
            for line in f.read_text("utf-8").splitlines():
                r = json.loads(line)
                ms[r["cocoid"]] = sc.vi_objects(r["caption"], vi)
            ments[name] = [ms.get(c, set()) for c in cids]
    return refs, [cinst.get(c, set()) for c in cids], ments, list(ments)


def ols(x, y):
    dx = x - x.mean(-1, keepdims=True)
    return (dx * (y - y.mean(-1, keepdims=True))).sum(-1) / (dx ** 2).sum(-1)


def ci(v):
    return [round(float(np.percentile(v, 2.5)), 3), round(float(np.percentile(v, 97.5)), 3)]


def analyse(name, refs, ments, fam, inst=None, seed=0):
    N, S = len(refs), len(fam)
    golds = {**SLOTS, **PAIRS}
    M = np.array([[len(ments[s][i]) for i in range(N)] for s in fam], float)
    TP = np.zeros((len(golds), S, N)); RI = np.zeros_like(TP); GS = np.zeros((len(golds), N))
    for g, slots in enumerate(golds.values()):
        for i in range(N):
            gold = set().union(*(refs[i][j] for j in slots))
            GS[g, i] = len(gold)
            for si, s in enumerate(fam):
                TP[g, si, i] = len(ments[s][i] & gold)
                RI[g, si, i] = TP[g, si, i] / len(gold) if gold else 0.0
    HG = (GS > 0).astype(float)
    # support profile per image: H[s, n, i], n = 0..5; index 6 = support 0 but in instance labels (COCO only)
    H = np.zeros((S, 7, N))
    for si, s in enumerate(fam):
        for i, m in enumerate(ments[s]):
            for o in m:
                n = sum(o in r for r in refs[i])
                H[si, 6 if (n == 0 and inst is not None and o in inst[i]) else n, i] += 1
    rng = np.random.default_rng(seed)
    W = np.vstack([np.ones(N), rng.multinomial(N, np.full(N, 1 / N), size=B)]).astype(float)  # row 0 = point
    Mb = W @ M.T / N                                                         # (B+1, S)
    res = {"n_img": N, "n_sys": S, "systems": fam, "median_M": round(float(np.median(Mb[0])), 3), "gold": {}}
    bs = {}
    for g, gname in enumerate(golds):
        TPb = W @ TP[g].T / N
        P = TPb / Mb
        R = (W * HG[g]) @ RI[g].T / (W @ HG[g])[:, None]
        F = 200 * P * R / (P + R)
        b = ols(np.log(Mb), np.log(TPb))
        sl = ols(np.log(Mb), F)
        gbar = (W @ GS[g]) / (W @ HG[g])            # L1 convention: mean over non-empty golds
        U = (W @ GS[g]) / N                          # accumulation value: mean over all images
        bs[gname] = dict(b=b, slope=sl, Gbar=gbar, U=U, F=F.mean(1))
        fit = mstar(fam, {s: (100 * P[0, j], 100 * R[0, j], F[0, j], Mb[0, j]) for j, s in enumerate(fam)}, gbar[0])
        res["gold"][gname] = {k: round(float(v[0]), 3) for k, v in bs[gname].items()} | {
            "b_ci": ci(b[1:]), "slope_ci": ci(sl[1:]), "d_recall": fit["d_recall"], "Mstar_mixed": fit["Mstar_mixed"],
            "Lambda_micro": round(lam(b[0], gbar[0], float(np.median(Mb[0]))), 3)}
    agree = lambda key: sum(np.sign(v[key] - (res["median_M"] if key == "Mstar_mixed" else 0)) == np.sign(v["slope"])
                            for v in res["gold"].values())
    res["sign_agree_mixed_of_15"] = int(agree("Mstar_mixed"))
    res["sign_agree_micro_of_15"] = int(agree("Lambda_micro"))
    res["slope_ci_excl0_agree_mixed"] = [g for g, v in res["gold"].items() if (v["slope_ci"][0] > 0 or v["slope_ci"][1] < 0)
                                         and np.sign(v["Mstar_mixed"] - res["median_M"]) != np.sign(v["slope"])]
    # T3 contrasts (bootstrap rows share draws across golds)
    def contrast(A, Bset, key):
        d = np.mean([bs[a][key] for a in A], 0) - np.mean([bs[x][key] for x in Bset], 0)
        return {"point": round(float(d[0]), 3), "ci": ci(d[1:])}
    lag1 = [p for p, (a, b) in PAIRS.items() if b - a == 1]
    lag2 = [p for p, (a, b) in PAIRS.items() if b - a >= 2]
    lag1_no1 = [p for p in lag1 if 0 not in PAIRS[p]]
    lag2_no1 = [p for p in lag2 if 0 not in PAIRS[p]]
    res["T3"] = {
        "slot1_minus_slots2to5": {k: contrast(["s1"], ["s2", "s3", "s4", "s5"], k) for k in ("b", "slope", "Gbar", "U")},
        "lag1_minus_lag2plus_all": {k: contrast(lag1, lag2, k) for k in ("b", "slope", "Gbar", "U")},
        "lag1_minus_lag2plus_slots2to5": {k: contrast(lag1_no1, lag2_no1, k) for k in ("b", "slope", "Gbar", "U")},
        "pairs": {"lag1": lag1, "lag2plus": lag2, "lag1_no_s1": lag1_no1, "lag2plus_no_s1": lag2_no1}}
    # effective number of independent captions in an adjacent pair (slots 2..5): 1 + (U_adj - U_1)/(U_spread - U_1)
    u1 = np.mean([bs[s]["U"] for s in ("s2", "s3", "s4", "s5")], 0)
    ua = np.mean([bs[p]["U"] for p in lag1_no1], 0); us = np.mean([bs[p]["U"] for p in lag2_no1], 0)
    keff = 1 + (ua - u1) / (us - u1)
    res["T3"]["k_eff_adjacent_pair_slots2to5"] = {"point": round(float(keff[0]), 3), "ci": ci(keff[1:])}
    # T2 support profile: identity b(k) and marginal/average ratio r(n)
    Hb = np.einsum("bn,smn->bsm", W, H) / N                                   # (B+1, S, 7)
    ids = {}
    for k in range(1, 6):
        tpk = sum(Hb[:, :, n] * w(k, n) for n in range(1, 6))
        ids[k] = ols(np.log(Mb), np.log(tpk))
    res["T2_identity_b_randk"] = {k: {"point": round(float(v[0]), 3), "ci": ci(v[1:])} for k, v in ids.items()}
    # micro-F1 (pooled TP/M and TP/G) for the exact random-k expectation: G = U(k) from reference frequency counts
    nref = [[sum(o in r for r in refs[i]) for o in set().union(*refs[i])] for i in range(N)]
    m0 = float(np.median(Mb[0]))
    res["T2_microF1_randk"] = {}
    for k in range(1, 6):
        tpk = sum(Hb[:, :, n] * w(k, n) for n in range(1, 6))
        uk = W @ np.array([sum(w(k, n) for n in ns) for ns in nref]) / N           # (B+1,)
        f = 200 * tpk / (Mb + uk[:, None])
        sl = ols(np.log(Mb), f)
        lam_k = lam(ids[k][0], uk[0], m0)
        res["T2_microF1_randk"][k] = {"U": round(float(uk[0]), 3), "slope": round(float(sl[0]), 2), "slope_ci": ci(sl[1:]),
                                      "Lambda_micro": round(lam_k, 3), "Mstar_micro": round(float(ids[k][0] * uk[0] / (1 - ids[k][0])), 2),
                                      "sign_agree": bool(np.sign(lam_k) == np.sign(sl[0]))}
    res["T2_identity_b5_minus_b1"] = {"point": round(float(ids[5][0] - ids[1][0]), 3), "ci": ci(ids[5][1:] - ids[1][1:])}
    mu = np.stack([ols(Mb, Hb[:, :, n]) for n in range(7)], 1)               # dh(n)/dM, (B+1, 7)
    av = Hb.mean(1) / Mb.mean(1)[:, None]                                     # h(n)/M at the family mean
    r = mu / np.where(av > 0, av, np.nan)
    labels = ["n0" + ("_notinst" if inst is not None else ""), "n1", "n2", "n3", "n4", "n5", "n0_inst"]
    res["T2_profile"] = {lab: {"avg_share": round(float(av[0, j]), 3), "marg_share": round(float(mu[0, j]), 3),
                               "ratio_r": round(float(r[0, j]), 3), "ratio_ci": ci(r[1:, j])}
                         for j, lab in enumerate(labels) if inst is not None or j < 6}
    mono =np.mean([np.all(np.diff(r[x, 1:6]) <= 0) for x in range(1, B + 1)])
    res["T2_share_draws_r_monotone_n1to5"] = round(float(mono), 3)
    print(name, json.dumps(res, default=str)[:4000], flush=True)
    return res


def lam(b, gbar, m0):
    return float(np.log(b / (1 - b)) + np.log(gbar) - np.log(m0))


def phi(k, p):
    """Elasticity of c_k(pi) = 1-(1-pi)^k with respect to pi."""
    return k * p * (1 - p) ** (k - 1) / (1 - (1 - p) ** k)


def closed_form(bk: dict, b_inf=None):
    """Fit b_k = 1 - D - theta*phi_k(pi_M), theta = 1 - D - b_1, on k = 2..5 (grid). b_inf given -> D fixed."""
    best, prof = None, []
    for D in ([1 - b_inf] if b_inf else np.linspace(0.0, 0.5, 501)):
        th = 1 - D - bk[1]
        best_d = np.inf
        for p in np.linspace(0.005, 0.995, 199):
            pred = {k: 1 - D - th * phi(k, p) for k in range(2, 6)}
            sse = sum((pred[k] - bk[k]) ** 2 for k in range(2, 6))
            best_d = min(best_d, sse)
            if best is None or sse < best[0]:
                best = (sse, D, p, pred)
        prof.append((float(D), best_d))
    sse, D, p, pred = best
    ok = [d for d, s in prof if np.sqrt(s / 4) <= 2 * max(np.sqrt(sse / 4), 0.0025)]  # D values fitting within 2x best RMSE
    return {"D": round(float(D), 3), "pi_M": round(float(p), 3), "rmse": round(float(np.sqrt(sse / 4)), 4),
            "D_range_within_2x_rmse": [round(min(ok), 3), round(max(ok), 3)],
            "pred_b2to5": [round(float(pred[k]), 3) for k in range(2, 6)], "obs_b2to5": [bk[k] for k in range(2, 6)]}


def t4(l1_mstar, l1_coco, m0_ktvic, m0_coco):
    """Two-channel split of Lambda between the sparsest and the fullest gold (L1's b and Gbar)."""
    out = {}
    km = {g: (r["ft"]["b"], r["Gbar"], r["ft"]["slope_F1_per_logM"]) for g, r in l1_mstar["gold"].items()}
    kc = {g: (r["b"], r["Gbar"], r["slope"]) for g, r in l1_coco["gold"].items()}
    cases = {"ktvic_randk": (km, m0_ktvic, "k1_randk", "k5_randk", [f"k{k}_randk" for k in range(1, 6)]),
             "ktvic_firstk": (km, m0_ktvic, "k1_firstk", "k5_firstk", [f"k{k}_firstk" for k in range(1, 6)]),
             "coco_randk": (kc, m0_coco, "refs1_randk", "refs5_randk", [f"refs{k}_randk" for k in range(1, 6)]),
             "coco_refs1_to_inst": (kc, m0_coco, "refs1_randk", "inst", [f"refs{k}_randk" for k in range(1, 6)] + ["inst", "inst+refs5"])}
    for name, (tab, m0, lo, hi, seq) in cases.items():
        (b1, g1, _), (b2, g2, _) = tab[lo], tab[hi]
        db, dg = lam(b2, g1, m0) - lam(b1, g1, m0), np.log(g2 / g1)
        out[name] = {"M0": round(m0, 3),
                     "Lambda": {g: round(lam(tab[g][0], tab[g][1], m0), 3) for g in seq},
                     "obs_slope": {g: tab[g][2] for g in seq},
                     "sign_agree": int(sum(np.sign(lam(tab[g][0], tab[g][1], m0)) == np.sign(tab[g][2]) for g in seq)),
                     "n": len(seq),
                     "dLambda_b_channel": round(float(db), 3), "dLambda_G_channel": round(float(dg), 3),
                     "b_channel_share": round(float(db / (db + dg)), 3),
                     "counterfactual_Lambda_b_lo_G_hi": round(lam(b1, g2, m0), 3),
                     "counterfactual_Lambda_b_hi_G_lo": round(lam(b2, g1, m0), 3)}
    return out


def main() -> None:
    _check()
    out_dir = Path(sys.argv[1])
    ids, ref_sets, ments = load()
    refs = [ref_sets[i] for i in ids]
    assert all(len(r) == 5 for r in refs)
    fam = [s for s in ments if not FT_EXCLUDE.match(s)]
    assert len(fam) == 36, len(fam)
    res = {"ktvic_ft": analyse("ktvic_ft", refs, ments, fam)}
    crefs, cinst, cments, cfam = load_coco()
    assert len(cfam) == 9 and all(len(r) == 5 for r in crefs)
    res["coco2500"] = analyse("coco2500", crefs, cments, cfam, inst=cinst, seed=1)
    l1m = json.loads((L1 / "check_mstar.json").read_text())
    l1c = json.loads((L1 / "check_coco.json").read_text())
    res["T4"] = t4(l1m, l1c, res["ktvic_ft"]["median_M"], res["coco2500"]["median_M"])
    print("T4", json.dumps(res["T4"]), flush=True)
    bk = {ds: {int(k): v["point"] for k, v in res[ds]["T2_identity_b_randk"].items()} for ds in ("ktvic_ft", "coco2500")}
    res["T5_closed_form"] = {"ktvic_free_D": closed_form(bk["ktvic_ft"]), "coco_free_D": closed_form(bk["coco2500"]),
                             "coco_D_from_inst+refs": closed_form(bk["coco2500"], b_inf=l1c["gold"]["inst+refs5"]["b"])}
    print("T5", json.dumps(res["T5_closed_form"]), flush=True)
    (out_dir / "h4_check.json").write_text(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
