#!/usr/bin/env python3
"""R13 Q2: object metrics vs LongCap-Arena human Relevance (VELA, EMNLP 2025), adapted DOCCI G3 design.

Prereg: manuscript/prereg/2026-10-15_q2_longcap_arena.md + .json (frozen predictions, input sha256s).
LongCap-Arena releases one candidate per image and no system label, so:
  (i)   slope of human Relevance on M is pooled over captions (no within-system slope possible);
  (ii)  delta tau_b = tau_b(z_P, Rel) - tau_b(P_raw, Rel) over captions with M >= 1 (no system ranking possible);
  (iii) acc(-CHAIR -> Rel) on count-equal minus count-differing caption pairs (pairs are across images).
Bootstrap: 2,000 image-clustered resamples (one caption per image, so image = caption), seed 0.
Run (from a cwd outside the data dir; -E -P = -I minus -s, needed because numpy is a user-site install):
  nice -n 19 env OMP_NUM_THREADS=2 python3 -E -P /mnt/d/vsps_image_captioning/scripts/r13/r13_q2_longcap_arena.py
"""
import ast
import csv
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.stats import kendalltau

ROOT = Path("/mnt/d/vsps_image_captioning")
DATA = ROOT / ".session_backup/2026-10-15/r13_data/longcap_arena_vela_repo"
PREREG = ROOT / "manuscript/prereg/2026-10-15_q2_longcap_arena.json"
OUT = ROOT / ".session_backup/2026-10-15/r13_human/q2_longcap_arena.json"
SYN = ROOT / "data/coco_probe/chair_synonyms.txt"
E1_PATH = ROOT / ".session_backup/2026-10-14/research_r10/E1/e1_chair_count.py"
NBOOT, SEED, BCHUNK = 2000, 0, 200

sys.argv = ["e1_chair_count.py", str(SYN), "", "", "", ""]
_spec = importlib.util.spec_from_file_location("e1_chair_count", str(E1_PATH))
e1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(e1)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def ordered_coco80(text):
    return list(dict.fromkeys(e1.nodes(text or "")))


def load(aspect):
    csv.field_size_limit(10 ** 8)
    rows = {}
    for f in sorted(DATA.glob(f"*/{aspect}_*.csv")):
        for r in csv.DictReader(f.open(encoding="utf-8")):
            rows[(r["imgid"], r["cand"])] = (float(r["score"]), ast.literal_eval(r["refs"]))
    return rows


def weighted_pair_counts(x, h, mask, W):
    """Per bootstrap row w: sum over a<b with mask of w_a w_b [concordant], same for discordant (ties dropped)."""
    s = np.sign(x[:, None] - x[None, :]) * np.sign(h[:, None] - h[None, :])
    conc = ((s > 0) & mask).astype(np.float32)
    disc = ((s < 0) & mask).astype(np.float32)
    del s
    out = []
    for K in (conc, disc):
        tot = np.concatenate([((W[b:b + BCHUNK] @ K) * W[b:b + BCHUNK]).sum(1) / 2 for b in range(0, len(W), BCHUNK)])
        out.append(tot)
    return out


def acc_from(conc, disc):
    return conc / np.maximum(conc + disc, 1e-12)


def ci(a):
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]


def zP(P, M, w):
    """Count-residualized precision: P_raw minus the (bootstrap-weighted) mean P_raw at the same M."""
    z = np.zeros_like(P)
    for m in np.unique(M):
        k = M == m
        z[k] = P[k] - (w[k] * P[k]).sum() / max(w[k].sum(), 1e-12)
    return z


def _selftest():
    x = np.array([1., 2., 3., 3.])
    h = np.array([1., 3., 2., 4.])
    m = ~np.eye(4, dtype=bool)
    c, d = weighted_pair_counts(x, h, m, np.ones((1, 4), np.float32))
    assert (c[0], d[0]) == (4.0, 1.0), (c, d)  # pairs: (0,1)+ (0,2)+ (0,3)+ (1,2)- (1,3)+ (2,3) tie
    c2, _ = weighted_pair_counts(x, h, m, np.array([[2., 1., 0., 1.]], np.float32))
    assert c2[0] == 2 * 1 + 2 * 1 + 1 * 1, c2  # (0,1)=2, (0,3)=2, (1,3)=1


def write(res):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(res, indent=1))
    tmp.replace(OUT)


def main():
    _selftest()
    t0 = time.time()
    pre = json.loads(PREREG.read_text())
    inputs = {str(p.relative_to(ROOT)): sha(p) for p in sorted(DATA.glob("*/*.csv"))}
    inputs[str(SYN.relative_to(ROOT))] = sha(SYN)
    inputs[str(E1_PATH.relative_to(ROOT))] = sha(E1_PATH)
    mismatch = {k: v for k, v in inputs.items() if pre["input_sha256"].get(k) != v}
    script_sha = sha(__file__)
    res = {"test": "R13_Q2_LongCap_Arena", "prereg_json": str(PREREG.relative_to(ROOT)), "prereg_json_sha256": sha(PREREG),
           "script_sha256": script_sha, "script_sha_matches_prereg": script_sha == pre["script_sha256"],
           "input_sha256": inputs, "input_sha_mismatch_vs_prereg": mismatch, "nboot": NBOOT, "seed": SEED}
    if mismatch or not res["script_sha_matches_prereg"]:
        res["verdict"] = "ABORTED_SHA_MISMATCH"
        write(res)
        raise SystemExit("sha mismatch vs prereg; aborted")

    rel, desc = load("rel"), load("desc")
    keys = sorted(rel)
    H = np.array([rel[k][0] for k in keys])
    Hdesc = np.array([desc[k][0] if k in desc else np.nan for k in keys])
    u = [ordered_coco80(k[1]) for k in keys]
    gold = [set().union(*[set(ordered_coco80(r)) for r in rel[k][1]]) for k in keys]
    M = np.array([len(x) for x in u], float)
    TP = np.array([sum(c in g for c in x) for x, g in zip(u, gold)], float)
    G = np.array([len(g) for g in gold], float)
    words = np.array([len(k[1].split()) for k in keys], float)
    negCHAIR = np.where(M > 0, -(M - TP) / np.maximum(M, 1), 0.0)
    n = len(keys)
    res["data_summary"] = {"n_captions": n, "n_images": len({k[0] for k in keys}), "n_with_desc_rating": int(np.isfinite(Hdesc).sum()),
                           "mean_M": float(M.mean()), "median_M": float(np.median(M)), "share_M_ge_1": float((M >= 1).mean()),
                           "mean_gold_classes_G": float(G.mean()), "mean_words": float(words.mean())}
    write(res)

    rng = np.random.default_rng(SEED)
    W = rng.multinomial(n, np.full(n, 1.0 / n), size=NBOOT).astype(np.float32)
    thr = pre["frozen_predictions"]

    # (i) pooled OLS slope of Rel on M
    def slope(w, y, x):
        xb, yb = (w * x).sum() / w.sum(), (w * y).sum() / w.sum()
        return float((w * (x - xb) * (y - yb)).sum() / (w * (x - xb) ** 2).sum())
    b = slope(np.ones(n), H, M)
    bb = np.array([slope(W[i].astype(float), H, M) for i in range(NBOOT)])
    X = np.column_stack([np.ones(n), M, words, G])
    beta_ctrl = np.linalg.lstsq(X, H, rcond=None)[0]
    t_i = {"beta_M": b, "beta_M_ci_95": ci(bb), "clause_beta_lt_0": b < 0, "clause_ci_hi_lt_0": ci(bb)[1] < 0,
           "secondary_ols_M_words_G": dict(zip(["const", "M", "words", "G"], map(float, beta_ctrl)))}
    t_i["pass"] = bool(t_i["clause_beta_lt_0"] and t_i["clause_ci_hi_lt_0"])
    res["test_i_slope_rel_on_M"] = t_i
    write(res)

    # (ii) delta tau_b, captions with M >= 1
    s1 = M >= 1
    P = np.where(s1, TP / np.maximum(M, 1), np.nan)
    idx1 = np.flatnonzero(s1)

    def dtau(w):
        ix = np.repeat(idx1, w[idx1].astype(int))
        z = zP(P[ix], M[ix], np.ones(len(ix)))
        t_raw = kendalltau(P[ix], H[ix], variant="b").statistic
        t_z = kendalltau(z, H[ix], variant="b").statistic
        return t_z - t_raw, t_z, t_raw
    d0, tz0, tr0 = dtau(np.ones(n))
    db = np.array([dtau(W[i])[0] for i in range(NBOOT)])
    t_ii = {"n_captions_M_ge_1": int(s1.sum()), "tau_b_zP": float(tz0), "tau_b_P_raw": float(tr0), "delta_tau": float(d0),
            "delta_tau_ci_95": ci(db), "clause_delta_ge_threshold": d0 >= thr["ii_delta_tau_min"], "clause_ci_lo_gt_0": ci(db)[0] > 0}
    t_ii["pass"] = bool(t_ii["clause_delta_ge_threshold"] and t_ii["clause_ci_lo_gt_0"])
    t_ii["kill_rule_fired"] = bool(d0 <= 0)
    res["test_ii_delta_tau"] = t_ii
    write(res)

    # (iii) count-equal vs count-differing caption pairs, -CHAIR -> Rel
    eq = M[:, None] == M[None, :]
    np.fill_diagonal(eq, False)
    ne = ~eq
    np.fill_diagonal(ne, False)
    ones = np.ones((1, n), np.float32)
    out = {}
    for name, mask in (("ceq", eq), ("cdiff", ne)):
        c, d = weighted_pair_counts(negCHAIR, H, mask, np.vstack([ones, W]))
        out[name] = (acc_from(c, d), c[0] + d[0])
    diff = out["ceq"][0] - out["cdiff"][0]
    t_iii = {"acc_ceq": float(out["ceq"][0][0]), "acc_ceq_ci_95": ci(out["ceq"][0][1:]), "n_untied_ceq": float(out["ceq"][1]),
             "acc_cdiff": float(out["cdiff"][0][0]), "acc_cdiff_ci_95": ci(out["cdiff"][0][1:]), "n_untied_cdiff": float(out["cdiff"][1]),
             "diff_ceq_minus_cdiff": float(diff[0]), "diff_ci_95": ci(diff[1:])}
    t_iii["pass"] = bool(t_iii["diff_ceq_minus_cdiff"] > 0 and t_iii["diff_ci_95"][0] > 0)
    t_iii["kill_rule_fired"] = bool(t_iii["diff_ceq_minus_cdiff"] <= 0)
    res["test_iii_count_equal_vs_differing"] = t_iii

    passes = [t_i["pass"], t_ii["pass"], t_iii["pass"]]
    res["verdict"] = "PASS" if all(passes) else ("FAIL" if not any(passes) else "MIXED")
    res["n_primary_pass"] = int(sum(passes))
    res["elapsed_sec"] = round(time.time() - t0, 1)
    write(res)
    print(json.dumps({k: res[k] for k in ("verdict", "n_primary_pass", "elapsed_sec")}))


if __name__ == "__main__":
    main()
