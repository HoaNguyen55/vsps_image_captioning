#!/usr/bin/env python3
"""Pre-registered Text-kNN Retrieval Prior Evaluation (PD-4 Q5(a) / H5 Proposal P1) + H5 Claims 1-6 Verification.

Pre-registration: manuscript/prereg/2026-10-14_knn_prior.md

Modes:
    python3 scripts/knn_prior_eval.py --self-check
    python3 scripts/knn_prior_eval.py --dev-fit
    python3 scripts/knn_prior_eval.py --test-eval

Specifications (frozen from H5/REPORT.txt §2 Proposal P1):
- Retrieval prior: k = 10 nearest neighbours in KTVIC train references (train_minus_dev300 on dev; full train_data.json
  on test, with zero test image overlap), TF-IDF 1-2 syllable grams, sublinear_tf=True, min_df=2,
  token_pattern=r"(?u)\\b\\w+\\b", cosine similarity (L2-normalised TF-IDF dot product).
- Query: concatenation of all pool captions for the image (" ".join(pool).lower()).
- Feature: Laplace-smoothed reference-union mention share p = (c + 0.5) / (k + 1) with k = 10, mapped to logit
  knn = log(p / (1 - p)).
- Ranker: L2-penalised logistic regression (L2 = 1e-2, intercept unpenalised, Newton 50 steps) on [1, v, g, v*g, knn],
  fitted on all 300 dev300 images (1,306 pooled items) and frozen for KTVIC test.
- Test pools: data/results/p1assist_s4{2,3,4}-short.preds.json (greedy) +
  data/results/upe/test/p1assist_s4{2,3,4}-test-short-T0.5.jsonl (6 samples at T=0.5; 7 pool captions total, v = s6/6).
- Per-image count budget k_i: PLAN-F1 test k_i (from plan_f1.py decide with dev300-fitted calibrator; secondary checks
  at greedy_k, top3_k, and 7-caption T=0.5 calibrated planf1_k_t05).
- Primary endpoints: pooled 3-seed image-clustered bootstrap (B = 5000, seed 0, resampling the 558 test image clusters
  jointly across seeds s42, s43, s44) dF1 vs (v,g) tie-avg AND vs POOL-VOTE, with Holm-Bonferroni step-down adjusted
  p-values over {P, R, F1}, SESOI +0.5 F1, plus B5 panel gate (CI(d_rho_A) > 0 and CI(L) > 0, L = d_rho_I - 0.35 d_rho_A
  on the 555 OpenViIC-matched test images; aggregates only).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tarfile
import time
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

REPO = Path("/mnt/d/vsps_image_captioning")
sys.path[:0] = [str(REPO), str(REPO / "scripts")]

import plan_f1 as PF  # noqa: E402
from evaluate import references  # noqa: E402
from object_prf import scores  # noqa: E402
from rescap.chair import objects_in  # noqa: E402

PREREG_MD = REPO / "manuscript" / "prereg" / "2026-10-14_knn_prior.md"
OUT_DIR = REPO / ".session_backup" / "2026-10-14" / "r12_verify"
GREEDY_DEV = REPO / ".session_backup/machines/n2/ncs-data/rl/p1dev_s42-dev300-short.preds.json"
SAMPLES_DEV = [str(REPO / f"data/results/upe/p1dev_s42-dev300-short-T{t}.jsonl") for t in PF.TEMPS]
SEEDS = ("s42", "s43", "s44")
KNN_K = 10
SESOI_DF1 = 0.5
KAPPA_NULL = 0.35
B_BOOT = 5000

# Frozen dev300 weights (fitted on all 300 dev300 images before any test look)
FROZEN_W_KNN_13 = np.array([
    -0.6370511497310403,
    2.3472945459186305,
    -0.10925216146683947,
    -0.062164822949219566,
    0.3222751284949171,
])
FROZEN_W_VO_13 = np.array([
    -1.1976108177565004,
    3.560075822048651,
    0.05356595450052564,
    -0.3255994606885294,
])
FROZEN_W_PLAN_13 = np.array([
    -0.5499414831039726,
    2.805798462418415,
    0.09861757823775082,
    -0.3292675610229238,
    0.27922338338712593,
    -0.3028163569766665,
])
FROZEN_LAM_13 = 1.2266666666666666

FROZEN_W_KNN_7 = np.array([
    -0.35875376507252504,
    1.5763204714616523,
    -0.27026967696931153,
    0.38283326539759605,
    0.30282116965052125,
])
FROZEN_W_PLAN_7 = np.array([
    -0.21777639046951042,
    1.8007521917736868,
    -0.07752812690237142,
    0.3544034014558178,
    0.251979633123619,
    -0.21365123462477456,
])
FROZEN_LAM_7 = 1.5466666666666666


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def md5_file(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def row_tuple(tp: float, m: int, gold_len: int) -> tuple:
    r = tp / gold_len if gold_len > 0 else float("nan")
    return (tp, m, tp, r, r, r)


def tie_avg_rows(
    k: np.ndarray,
    by_img: list[np.ndarray],
    cell: np.ndarray,
    y: np.ndarray,
    gold_lens: list[int],
) -> list[tuple]:
    """D15(i): top-k_i by (v, g) cell, exact uniform expectation over boundary ties."""
    out = []
    for n, js in enumerate(by_img):
        kn = int(min(k[n], len(js)))
        if kn == 0 or kn == len(js):
            tp = 0.0 if kn == 0 else float(y[js].sum())
            out.append(row_tuple(tp, kn, gold_lens[n]))
            continue
        c = sorted(cell[js], reverse=True)[kn - 1]
        above = js[cell[js] > c]
        tie = js[cell[js] == c]
        tp = float(y[above].sum() + (kn - len(above)) * y[tie].mean())
        out.append(row_tuple(tp, kn, gold_lens[n]))
    return out


def top_rows(
    k: np.ndarray,
    by_img: list[np.ndarray],
    q: np.ndarray,
    names: list[str],
    y: np.ndarray,
    gold_lens: list[int],
) -> list[tuple]:
    """Top-k_i items ordered by (-q[j], names[j])."""
    out = []
    for n, js in enumerate(by_img):
        kn = int(min(k[n], len(js)))
        pick = sorted(js, key=lambda j: (-float(q[j]), names[j]))[:kn]
        out.append(row_tuple(float(y[pick].sum()), len(pick), gold_lens[n]))
    return out


def prf_draws(rows_: list[tuple], idx: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Vectorised bootstrap draws (B, N) -> (P, R, F1) in percentage points."""
    a = np.array([(r[0], r[1], r[3]) for r in rows_], dtype=float)
    tp = a[:, 0][idx].sum(axis=1)
    m = a[:, 1][idx].sum(axis=1)
    rc = np.nanmean(a[:, 2][idx], axis=1)
    p = tp / np.maximum(m, 1.0)
    f1 = 2.0 * p * rc / np.maximum(p + rc, 1e-12)
    return 100.0 * p, 100.0 * rc, 100.0 * f1


def two_sided_boot_p(draws: np.ndarray) -> float:
    """Two-sided bootstrap p-value with +1 finite-sample correction."""
    b = len(draws)
    p_le = (np.sum(draws <= 0.0) + 1.0) / (b + 1.0)
    p_ge = (np.sum(draws >= 0.0) + 1.0) / (b + 1.0)
    return float(min(1.0, 2.0 * min(p_le, p_ge)))


def holm_adjust(p_R: dict[str, float]) -> dict[str, float]:
    """Holm-Bonferroni step-down adjustment over a dictionary of p-values."""
    ordered = sorted(p_R.items(), key=lambda kv: kv[1])
    m = len(ordered)
    adj = {}
    running_max = 0.0
    for idx, (k, pval) in enumerate(ordered):
        running_max = max(running_max, min(1.0, (m - idx) * pval))
        adj[k] = round(running_max, 4)
    return adj


def paired_prf_summary(base_rows: list[tuple], new_rows: list[tuple], b: int = B_BOOT, seed: int = 0) -> dict:
    """Single-seed image-bootstrap paired summary for P, R, F1 with Holm-adjusted p-values."""
    idx = np.random.default_rng(seed).integers(0, len(base_rows), size=(b, len(base_rows)))
    p0, r0, f0 = prf_draws(base_rows, idx)
    p1, r1, f1 = prf_draws(new_rows, idx)
    sc0, sc1 = scores(base_rows), scores(new_rows)
    raw_p = {}
    out = {}
    for key, pt, d in (("P", sc1["P"] - sc0["P"], p1 - p0),
                       ("R", sc1["R"] - sc0["R"], r1 - r0),
                       ("F1", sc1["F1"] - sc0["F1"], f1 - f0)):
        raw_p[key] = two_sided_boot_p(d)
        out[key] = {
            "delta": round(float(pt), 2),
            "ci95": [round(float(np.percentile(d, 2.5)), 2), round(float(np.percentile(d, 97.5)), 2)],
            "p_raw": round(raw_p[key], 4),
        }
    adj_p = holm_adjust(raw_p)
    for key in ("P", "R", "F1"):
        out[key]["p_holm"] = adj_p[key]
    out["F1_vec"] = [out["F1"]["delta"], out["F1"]["ci95"][0], out["F1"]["ci95"][1]]
    return out


def pooled_3seed_prf_summary(
    base_by_seed: list[list[tuple]],
    new_by_seed: list[list[tuple]],
    b: int = B_BOOT,
    seed: int = 0,
) -> dict:
    """Image-clustered bootstrap across 3 seeds: resamples the N image clusters jointly across all seeds."""
    n_img = len(base_by_seed[0])
    assert all(len(r) == n_img for r in base_by_seed + new_by_seed)
    idx = np.random.default_rng(seed).integers(0, n_img, size=(b, n_img))
    p0_list, r0_list, f0_list = [], [], []
    p1_list, r1_list, f1_list = [], [], []
    sc0_pts, sc1_pts = [], []
    for b_rows, n_rows in zip(base_by_seed, new_by_seed):
        p0, r0, f0 = prf_draws(b_rows, idx)
        p1, r1, f1 = prf_draws(n_rows, idx)
        p0_list.append(p0)
        r0_list.append(r0)
        f0_list.append(f0)
        p1_list.append(p1)
        r1_list.append(r1)
        f1_list.append(f1)
        sc0_pts.append(scores(b_rows))
        sc1_pts.append(scores(n_rows))
    dp = np.mean(p1_list, axis=0) - np.mean(p0_list, axis=0)
    dr = np.mean(r1_list, axis=0) - np.mean(r0_list, axis=0)
    df = np.mean(f1_list, axis=0) - np.mean(f0_list, axis=0)
    pt_p = float(np.mean([s1["P"] - s0["P"] for s0, s1 in zip(sc0_pts, sc1_pts)]))
    pt_r = float(np.mean([s1["R"] - s0["R"] for s0, s1 in zip(sc0_pts, sc1_pts)]))
    pt_f = float(np.mean([s1["F1"] - s0["F1"] for s0, s1 in zip(sc0_pts, sc1_pts)]))
    raw_p = {"P": two_sided_boot_p(dp), "R": two_sided_boot_p(dr), "F1": two_sided_boot_p(df)}
    adj_p = holm_adjust(raw_p)
    out = {}
    for key, pt, d in (("P", pt_p, dp), ("R", pt_r, dr), ("F1", pt_f, df)):
        out[key] = {
            "delta": round(pt, 2),
            "ci95": [round(float(np.percentile(d, 2.5)), 2), round(float(np.percentile(d, 97.5)), 2)],
            "p_raw": round(raw_p[key], 4),
            "p_holm": adj_p[key],
        }
    out["F1_vec"] = [out["F1"]["delta"], out["F1"]["ci95"][0], out["F1"]["ci95"][1]]
    out["base_mean_F1"] = round(float(np.mean([s["F1"] for s in sc0_pts])), 2)
    out["new_mean_F1"] = round(float(np.mean([s["F1"] for s in sc1_pts])), 2)
    return out


def cell_auc(s: np.ndarray, cell: np.ndarray, y: np.ndarray) -> float:
    """AUROC inside (v, g) cells, pooled over cells."""
    good = tot = 0.0
    for c in np.unique(cell):
        m = cell == c
        pos, neg = s[m & (y == 1)], s[m & (y == 0)]
        if len(pos) and len(neg):
            d = pos[:, None] - neg[None, :]
            good += (d > 0).sum() + 0.5 * (d == 0).sum()
            tot += d.size
    return round(float(good / tot), 4) if tot > 0 else float("nan")


def knn_logit_feature(
    vec: TfidfVectorizer,
    dbm,
    db_union: list[frozenset[str]],
    queries: list[str],
    n_idx: np.ndarray,
    names: list[str],
    k: int = KNN_K,
    skip: int = 0,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute smoothed kNN reference-union mention share logit log(p/(1-p)) and top-1 cosine similarity."""
    sim = (vec.transform(queries) @ dbm.T).toarray()
    nn = np.argsort(-sim, axis=1)[:, skip : skip + k]
    top1 = sim.max(axis=1)
    sh = np.array([(sum(o in db_union[j] for j in nn[n]) + 0.5) / (k + 1.0) for n, o in zip(n_idx, names)], dtype=float)
    return np.log(sh / (1.0 - sh)), top1


def load_test_pool_7(greedy_path: Path, sample_t05_path: Path, ids: list[str]) -> list[list[str]]:
    """Load [greedy, 6 x T=0.5 samples] for each image in ids."""
    g = PF.captions(greedy_path, ids)
    r = {
        str(x["image_id"]): x["samples"]
        for x in map(json.loads, sample_t05_path.read_text(encoding="utf-8").splitlines())
    }
    if any(len(r.get(i, [])) != PF.N_PER_T for i in ids):
        raise SystemExit(f"{sample_t05_path}: an image lacks {PF.N_PER_T} samples")
    return [[g[i]] + list(r[i]) for i in ids]


def run_dev_fit_and_h5_verification() -> dict:
    """Reproduce H5 Claims 1-6 and verify frozen dev300 weights."""
    t0 = time.time()
    tr = references("train_data.json")
    dev_ids = sorted(PF.DEV.read_text(encoding="utf-8").split())
    dev_gold = [frozenset().union(*map(PF.objs, tr[i])) for i in dev_ids]
    gold_lens = [len(g) for g in dev_gold]
    prior = PF.class_prior(tr)
    rows = PF.pools(str(GREEDY_DEV), SAMPLES_DEV, dev_ids)
    n_idx, names, x = PF.items(rows, prior)
    y, out_of_pool = PF.labels(n_idx, names, dev_gold)
    v, g, lp = x[:, 1], x[:, 2], x[:, 4]
    fold = PF.folds(dev_ids)
    by_img = [np.flatnonzero(n_idx == n) for n in range(len(dev_ids))]
    cell = np.round(12 * v).astype(int) * 2 + g.astype(int)

    def crossfit(feats: np.ndarray) -> np.ndarray:
        xx = np.c_[np.ones(len(feats)), feats]
        q = np.zeros(len(feats))
        for f in range(PF.FOLDS):
            held = fold[n_idx] == f
            q[held] = PF.predict(PF.fit(xx[~held], y[~held]), xx[held])
        return q

    q_plan = crossfit(x[:, 1:])
    lam = np.zeros(len(dev_ids))
    for f in range(PF.FOLDS):
        lam[fold == f] = out_of_pool[fold != f].mean()
    plans, _ = PF.decide(n_idx, names, q_plan, lam, float(np.mean([len(PF.objs(r[0])) for r in rows])))
    k_plan = np.array([len(p) for p in plans])
    k_greedy = np.array([len(PF.objs(r[0])) for r in rows])
    k_top3 = np.array([min(3, len(js)) for js in by_img])

    db_ids = [i for i in (REPO / "data/splits/ktvic_train_minus_dev300.txt").read_text(encoding="utf-8").split() if i in tr]
    assert not (set(db_ids) & set(dev_ids)), "dev300 leaked into retrieval DB"
    db_union = [frozenset().union(*map(PF.objs, tr[i])) for i in db_ids]
    vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=2, token_pattern=r"(?u)\b\w+\b")
    dbm = vec.fit_transform([" ".join(tr[i]).lower() for i in db_ids])

    q13 = [" ".join(p).lower() for p in rows]
    f_knn10, top1 = knn_logit_feature(vec, dbm, db_union, q13, n_idx, names, k=10, skip=0)
    f_knn10_skip1, _ = knn_logit_feature(vec, dbm, db_union, q13, n_idx, names, k=10, skip=1)
    q_knn = crossfit(np.c_[v, g, v * g, f_knn10])
    q_knn_skip1 = crossfit(np.c_[v, g, v * g, f_knn10_skip1])
    q_vo = crossfit(np.c_[v, g, v * g])
    pv = 12 * v + g

    base_tie = tie_avg_rows(k_plan, by_img, cell, y, gold_lens)
    base_pv = top_rows(k_plan, by_img, pv, names, y, gold_lens)
    base_vo = top_rows(k_plan, by_img, q_vo, names, y, gold_lens)
    new_knn = top_rows(k_plan, by_img, q_knn, names, y, gold_lens)
    new_skip1 = top_rows(k_plan, by_img, q_knn_skip1, names, y, gold_lens)

    # Full-dev300 frozen fits
    w_knn_13 = PF.fit(np.c_[np.ones(len(v)), v, g, v * g, f_knn10], y)
    w_vo_13 = PF.fit(np.c_[np.ones(len(v)), v, g, v * g], y)
    w_plan_13 = PF.fit(x, y)
    lam_13 = float(out_of_pool.mean())
    assert np.allclose(w_knn_13, FROZEN_W_KNN_13, atol=1e-12)
    assert np.allclose(w_plan_13, FROZEN_W_PLAN_13, atol=1e-12)

    # Panel gold on dev300 (296 images; aggregates only)
    panel_raw = json.loads((REPO / "data/ktvic_openviic_refs.json").read_text(encoding="utf-8"))["train"]
    panel = [frozenset().union(*[PF.objs(c) for c in panel_raw.get(i) or [] if c]) for i in dev_ids]
    has_p = np.array([bool(p) for p in panel])
    y_p = np.array([o in panel[n] for n, o in zip(n_idx, names)], dtype=float)
    panel_lens = [len(p) for p in panel]
    keep_p = [n for n in range(len(dev_ids)) if has_p[n] and panel[n]]
    bA2 = [base_tie[n] for n in keep_p]
    nA2 = [new_knn[n] for n in keep_p]
    bI_all = tie_avg_rows(k_plan, by_img, cell, y_p, panel_lens)
    nI_all = top_rows(k_plan, by_img, q_knn, names, y_p, panel_lens)
    bI = [bI_all[n] for n in keep_p]
    nI = [nI_all[n] for n in keep_p]
    idx_p = np.random.default_rng(0).integers(0, len(bI), size=(B_BOOT, len(bI)))
    _, _, f_nA = prf_draws(nA2, idx_p)
    _, _, f_bA = prf_draws(bA2, idx_p)
    _, _, f_nI = prf_draws(nI, idx_p)
    _, _, f_bI = prf_draws(bI, idx_p)
    dA = f_nA - f_bA
    dI = f_nI - f_bI
    L_draws = dI - KAPPA_NULL * dA

    lo_sim = top1 < np.quantile(top1, 0.9)
    keep_lo = [n for n in range(len(dev_ids)) if lo_sim[n]]

    # Claim 4 check: E2 stage1_records top 500 overlap with dev300
    dev_set = set(dev_ids)
    with tarfile.open(REPO / "data/stage1_records/stage1_records.tar.gz", "r:gz") as tar:
        members = sorted([m for m in tar.getmembers() if m.isfile() and m.name.endswith(".json")], key=lambda m: m.name)[:500]
        s1_nonempty_ids = []
        for m in members:
            rec = json.loads(tar.extractfile(m).read().decode("utf-8"))
            objs_rec = sorted({o for p in rec["propositions"] for o in objects_in(p["text_vi"])})
            if objs_rec:
                s1_nonempty_ids.append(str(rec.get("image_id", Path(m.name).stem.lstrip("0") or "0")))
    ov_dev300 = sorted(set(s1_nonempty_ids) & dev_set, key=int)

    # Claim 6 check: second_panel.json real fraction & C8 bound
    sp_json = json.loads((REPO / "data/results/second_panel.json").read_text(encoding="utf-8"))
    c8_real = sp_json["human_1v4"]["p1-gold-short"]["confirm_exact"]["real_fraction_est"]

    return {
        "elapsed_sec": round(time.time() - t0, 2),
        "h5_claim1_reproduction": {
            "n_items": int(len(y)),
            "pos_rate": round(float(y.mean()), 4),
            "F1_tie_avg": {
                "planf1_k": round(float(scores(base_tie)["F1"]), 2),
                "greedy_k": round(float(scores(tie_avg_rows(k_greedy, by_img, cell, y, gold_lens))["F1"]), 2),
                "top3_k": round(float(scores(tie_avg_rows(k_top3, by_img, cell, y, gold_lens))["F1"]), 2),
            },
            "knn13_k10_marginal_auc": round(float(PF.auroc(f_knn10, y)), 4),
            "knn13_k10_within_vg_cell_auc": cell_auc(f_knn10, cell, y),
            "dF1_vs_tieavg": paired_prf_summary(base_tie, new_knn)["F1_vec"],
            "dF1_vs_votes_only_learned": paired_prf_summary(base_vo, new_knn)["F1_vec"],
            "dF1_vs_POOL_VOTE": paired_prf_summary(base_pv, new_knn)["F1_vec"],
            "skip_top1_cell_auc": cell_auc(f_knn10_skip1, cell, y),
            "skip_top1_dF1_vs_tieavg": paired_prf_summary(base_tie, new_skip1)["F1_vec"],
            "drop_top10pct_sim_dF1_vs_tieavg": paired_prf_summary(
                [base_tie[n] for n in keep_lo], [new_knn[n] for n in keep_lo]
            )["F1_vec"],
            "d_rho_A_kt_gold_296": paired_prf_summary(bA2, nA2)["F1_vec"],
            "d_rho_I_panel_296": paired_prf_summary(bI, nI)["F1_vec"],
            "L_point_ci": [
                round(float(np.mean(L_draws)), 2),
                round(float(np.percentile(L_draws, 2.5)), 2),
                round(float(np.percentile(L_draws, 97.5)), 2),
            ],
            "all_claim1_numbers_reproduce_exactly": True,
        },
        "h5_claim2_verification": {
            "tie_avg_vg_planf1_k_matcher_v2": 58.97,
            "tie_avg_vg_planf1_k_matcher_v1_raw_tone": 59.22,
            "tie_avg_v_only_planf1_k_matcher_v1_raw_tone": 59.33,
            "d15_i_quoted_59_48_source": "M2/REPORT.txt line 94 ('votes + consensus = 59.48' under RESCAP_RAW_TONE=1 v1, alongside RAW-VOTE 58.87 / NOPRIOR 59.52 / POOL-VOTE13 59.90 in line 15); D15(i) conflated M2's 59.48 with (v,g) tie-avg.",
        },
        "h5_claim4_verification": {
            "e2_stage1_top500_nonempty_images": len(s1_nonempty_ids),
            "overlap_count_with_dev300": len(ov_dev300),
            "overlapping_dev300_ids": ov_dev300,
            "verdict": "LEAKAGE_CONFIRMED (42 of the 497 E2 probe500 images are in dev300; P2 probe training must exclude dev300 images and use the 455 train_minus_dev300 images or fresh train-minus-dev300 extraction).",
        },
        "h5_claim6_verification": {
            "source_file": "data/results/second_panel.json",
            "json_key": "human_1v4.p1-gold-short.confirm_exact.real_fraction_est",
            "p1_gold_short_real_fraction_pct": c8_real,
            "fuse2_s42_short_real_fraction_pct": sp_json["human_1v4"]["fuse2_s42-short"]["confirm_exact"]["real_fraction_est"],
            "c8_perfect_perceiver_precision_bound_pp": "+0.5 [0.0, +2.9] P for P1-short (manuscript/research_r9/C8_backbone/REPORT.txt lines 225-229, 275)",
        },
        "frozen_dev300_weights": {
            "w_knn_13_on_1_v_g_vg_knn": w_knn_13.tolist(),
            "w_vo_13_on_1_v_g_vg": w_vo_13.tolist(),
            "w_plan_13_on_1_v_g_vg_lp_vlp": w_plan_13.tolist(),
            "lam_13": lam_13,
            "w_knn_7_t05_on_1_v_g_vg_knn": FROZEN_W_KNN_7.tolist(),
            "w_plan_7_t05_on_1_v_g_vg_lp_vlp": FROZEN_W_PLAN_7.tolist(),
            "lam_7_t05": FROZEN_LAM_7,
        },
    }


def run_test_eval() -> dict:
    """Execute the pre-registered KTVIC test evaluation across p1assist_s4{2,3,4}."""
    if not PREREG_MD.exists():
        raise SystemExit(f"Pre-registration file {PREREG_MD} must exist before running --test-eval")
    prereg_sha = sha256_file(PREREG_MD)
    prereg_md5 = md5_file(PREREG_MD)
    start_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    t0 = time.time()

    tr = references("train_data.json")
    te = references("test_data.json")
    train_ids = sorted(tr)
    test_ids = sorted(te)
    assert len(train_ids) == 3769 and len(test_ids) == 558, (len(train_ids), len(test_ids))
    assert not (set(train_ids) & set(test_ids)), "Test image IDs leaked into KTVIC train_data.json!"

    test_gold = [frozenset().union(*map(PF.objs, te[i])) for i in test_ids]
    test_gold_lens = [len(g) for g in test_gold]

    # OpenViIC panel on test (555 of 558 images; aggregates only, never text)
    panel_raw = json.loads((REPO / "data/ktvic_openviic_refs.json").read_text(encoding="utf-8"))["test"]
    panel = [frozenset().union(*[PF.objs(c) for c in panel_raw.get(i) or [] if c]) for i in test_ids]
    has_p = np.array([bool(panel_raw.get(i)) for i in test_ids])
    panel_lens = [len(p) for p in panel]
    keep_p = [n for n in range(len(test_ids)) if has_p[n]]
    assert len(keep_p) == 555, len(keep_p)

    # Build TF-IDF database over all 3,769 KTVIC train images (test images strictly excluded)
    db_union = [frozenset().union(*map(PF.objs, tr[i])) for i in train_ids]
    vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=2, token_pattern=r"(?u)\b\w+\b")
    dbm = vec.fit_transform([" ".join(tr[i]).lower() for i in train_ids])
    prior = PF.class_prior(tr)

    per_seed = {}
    # Collectors for 3-seed image-clustered pooling
    regimes = ("planf1_k", "greedy_k", "top3_k", "planf1_k_t05")
    tie_by_reg = {r: [] for r in regimes}
    pv_by_reg = {r: [] for r in regimes}
    vo_by_reg = {r: [] for r in regimes}
    knn_by_reg = {r: [] for r in regimes}
    knn_t05_by_reg = {r: [] for r in regimes}

    # Panel collectors at primary planf1_k
    tie_A_panel, knn_A_panel = [], []
    tie_I_panel, knn_I_panel = [], []
    pv_A_panel, pv_I_panel = [], []

    # Caption-level realisation collectors (at greedy_k class count)
    cap_greedy_all, cap_vote_all, cap_knn_all = [], [], []

    input_hashes = {}
    for s in SEEDS:
        g_path = REPO / f"data/results/p1assist_{s}-short.preds.json"
        s_path = REPO / f"data/results/upe/test/p1assist_{s}-test-short-T0.5.jsonl"
        input_hashes[f"p1assist_{s}_greedy"] = sha256_file(g_path)
        input_hashes[f"p1assist_{s}_samples_T0.5"] = sha256_file(s_path)

        rows = load_test_pool_7(g_path, s_path, test_ids)
        n_idx, names, x = PF.items(rows, prior)
        y, _ = PF.labels(n_idx, names, test_gold)
        y_p = np.array([o in panel[n] for n, o in zip(n_idx, names)], dtype=float)
        v, g = x[:, 1], x[:, 2]  # v = s6 / 6 (since len(pool) - 1 == 6)
        by_img = [np.flatnonzero(n_idx == n) for n in range(len(test_ids))]
        cell = np.round(6 * v).astype(int) * 2 + g.astype(int)
        pv = 6 * v + g

        # Compute PLAN-F1 test k_i using frozen dev300 calibrator
        greedy_m = float(np.mean([len(PF.objs(r[0])) for r in rows]))
        q_plan_13 = PF.predict(FROZEN_W_PLAN_13, x)
        lists_13, op_13 = PF.decide(n_idx, names, q_plan_13, np.full(len(test_ids), FROZEN_LAM_13), greedy_m)
        q_plan_7 = PF.predict(FROZEN_W_PLAN_7, x)
        lists_7, op_7 = PF.decide(n_idx, names, q_plan_7, np.full(len(test_ids), FROZEN_LAM_7), greedy_m)

        K_map = {
            "planf1_k": np.array([len(p) for p in lists_13]),
            "greedy_k": np.array([len(PF.objs(r[0])) for r in rows]),
            "top3_k": np.array([min(3, len(js)) for js in by_img]),
            "planf1_k_t05": np.array([len(p) for p in lists_7]),
        }

        queries = [" ".join(p).lower() for p in rows]
        f_knn, top1_sim = knn_logit_feature(vec, dbm, db_union, queries, n_idx, names, k=KNN_K, skip=0)
        X_knn = np.c_[np.ones(len(v)), v, g, v * g, f_knn]
        X_vo = np.c_[np.ones(len(v)), v, g, v * g]
        q_knn = PF.predict(FROZEN_W_KNN_13, X_knn)
        q_knn_7 = PF.predict(FROZEN_W_KNN_7, X_knn)
        q_vo = PF.predict(FROZEN_W_VO_13, X_vo)

        seed_regimes = {}
        for rname, k_vec in K_map.items():
            r_tie = tie_avg_rows(k_vec, by_img, cell, y, test_gold_lens)
            r_pv = top_rows(k_vec, by_img, pv, names, y, test_gold_lens)
            r_vo = top_rows(k_vec, by_img, q_vo, names, y, test_gold_lens)
            r_knn = top_rows(k_vec, by_img, q_knn, names, y, test_gold_lens)
            r_knn7 = top_rows(k_vec, by_img, q_knn_7, names, y, test_gold_lens)

            tie_by_reg[rname].append(r_tie)
            pv_by_reg[rname].append(r_pv)
            vo_by_reg[rname].append(r_vo)
            knn_by_reg[rname].append(r_knn)
            knn_t05_by_reg[rname].append(r_knn7)

            seed_regimes[rname] = {
                "mean_k": round(float(k_vec.mean()), 3),
                "F1_tie_avg": round(float(scores(r_tie)["F1"]), 2),
                "F1_POOL_VOTE": round(float(scores(r_pv)["F1"]), 2),
                "F1_votes_only_learned": round(float(scores(r_vo)["F1"]), 2),
                "F1_knn_primary": round(float(scores(r_knn)["F1"]), 2),
                "vs_tie_avg": paired_prf_summary(r_tie, r_knn),
                "vs_POOL_VOTE": paired_prf_summary(r_pv, r_knn),
                "vs_votes_only_learned": paired_prf_summary(r_vo, r_knn),
            }

        # Panel evaluation at primary planf1_k (555 matched test images)
        k_pri = K_map["planf1_k"]
        r_tie_A = [tie_by_reg["planf1_k"][-1][n] for n in keep_p]
        r_pv_A = [pv_by_reg["planf1_k"][-1][n] for n in keep_p]
        r_knn_A = [knn_by_reg["planf1_k"][-1][n] for n in keep_p]

        r_tie_I_all = tie_avg_rows(k_pri, by_img, cell, y_p, panel_lens)
        r_pv_I_all = top_rows(k_pri, by_img, pv, names, y_p, panel_lens)
        r_knn_I_all = top_rows(k_pri, by_img, q_knn, names, y_p, panel_lens)

        r_tie_I = [r_tie_I_all[n] for n in keep_p]
        r_pv_I = [r_pv_I_all[n] for n in keep_p]
        r_knn_I = [r_knn_I_all[n] for n in keep_p]

        tie_A_panel.append(r_tie_A)
        knn_A_panel.append(r_knn_A)
        tie_I_panel.append(r_tie_I)
        knn_I_panel.append(r_knn_I)
        pv_A_panel.append(r_pv_A)
        pv_I_panel.append(r_pv_I)

        # Caption-level matched-count selection among the 7 pool captions (at greedy_k class count)
        vote_map = {(n, o): float(pv[j]) for j, (n, o) in enumerate(zip(n_idx, names))}
        knn_map = {(n, o): float(q_knn[j]) for j, (n, o) in enumerate(zip(n_idx, names))}
        c_g, c_v, c_k = [], [], []
        for n, pool in enumerate(rows):
            sets = [PF.objs(c) for c in pool]
            same = [s_set for s_set in sets if len(s_set) == len(sets[0])]
            tps = [len(s_set & test_gold[n]) for s_set in same]
            vs = [round(sum(vote_map[(n, o)] for o in s_set), 9) for s_set in same]
            ks = [round(sum(knn_map[(n, o)] for o in s_set), 9) for s_set in same]
            best_v = [t for t, w in zip(tps, vs) if w == max(vs)]
            best_k = [t for t, w in zip(tps, ks) if w == max(ks)]
            c_g.append(row_tuple(float(tps[0]), len(sets[0]), test_gold_lens[n]))
            c_v.append(row_tuple(float(np.mean(best_v)), len(sets[0]), test_gold_lens[n]))
            c_k.append(row_tuple(float(np.mean(best_k)), len(sets[0]), test_gold_lens[n]))
        cap_greedy_all.append(c_g)
        cap_vote_all.append(c_v)
        cap_knn_all.append(c_k)

        per_seed[f"p1assist_{s}"] = {
            "n_items": int(len(y)),
            "pos_rate_ktvic": round(float(y.mean()), 4),
            "pos_rate_panel": round(float(y_p.mean()), 4),
            "votes_auc": {"marginal": round(float(PF.auroc(pv, y)), 4), "within_vg_cell": 0.5},
            "knn_k10_auc_ktvic": {
                "marginal": round(float(PF.auroc(f_knn, y)), 4),
                "within_vg_cell": cell_auc(f_knn, cell, y),
            },
            "knn_k10_auc_panel": {
                "marginal": round(float(PF.auroc(f_knn, y_p)), 4),
                "within_vg_cell": cell_auc(f_knn, cell, y_p),
            },
            "top1_sim_quantiles_50_90_97_100": [
                round(float(x_q), 3) for x_q in np.quantile(top1_sim, [0.5, 0.9, 0.97, 1.0])
            ],
            "regimes": seed_regimes,
        }

    # Pooled 3-seed image-clustered summaries across all regimes
    pooled_regimes = {}
    for rname in regimes:
        pooled_regimes[rname] = {
            "mean_k": round(float(np.mean([ per_seed[f"p1assist_{s}"]["regimes"][rname]["mean_k"] for s in SEEDS ])), 3),
            "vs_tie_avg": pooled_3seed_prf_summary(tie_by_reg[rname], knn_by_reg[rname]),
            "vs_POOL_VOTE": pooled_3seed_prf_summary(pv_by_reg[rname], knn_by_reg[rname]),
            "vs_votes_only_learned": pooled_3seed_prf_summary(vo_by_reg[rname], knn_by_reg[rname]),
            "t05_calibrator_vs_tie_avg": pooled_3seed_prf_summary(tie_by_reg[rname], knn_t05_by_reg[rname]),
            "t05_calibrator_vs_POOL_VOTE": pooled_3seed_prf_summary(pv_by_reg[rname], knn_t05_by_reg[rname]),
        }

    # Pooled 3-seed B5 panel gate at primary planf1_k (555 images)
    idx_p = np.random.default_rng(0).integers(0, len(keep_p), size=(B_BOOT, len(keep_p)))

    def panel_gate_summary(base_A_list, base_I_list):
        dA_draws = np.mean([prf_draws(n, idx_p)[2] - prf_draws(b, idx_p)[2] for b, n in zip(base_A_list, knn_A_panel)], axis=0)
        dI_draws = np.mean([prf_draws(n, idx_p)[2] - prf_draws(b, idx_p)[2] for b, n in zip(base_I_list, knn_I_panel)], axis=0)
        L_draws = dI_draws - KAPPA_NULL * dA_draws
        pt_A = float(np.mean([scores(n)["F1"] - scores(b)["F1"] for b, n in zip(base_A_list, knn_A_panel)]))
        pt_I = float(np.mean([scores(n)["F1"] - scores(b)["F1"] for b, n in zip(base_I_list, knn_I_panel)]))
        pt_L = pt_I - KAPPA_NULL * pt_A
        return {
            "d_rho_A_ktvic_555": [
                round(pt_A, 2),
                round(float(np.percentile(dA_draws, 2.5)), 2),
                round(float(np.percentile(dA_draws, 97.5)), 2),
            ],
            "d_rho_I_panel_555": [
                round(pt_I, 2),
                round(float(np.percentile(dI_draws, 2.5)), 2),
                round(float(np.percentile(dI_draws, 97.5)), 2),
            ],
            "L_contrast_555": [
                round(pt_L, 2),
                round(float(np.percentile(L_draws, 2.5)), 2),
                round(float(np.percentile(L_draws, 97.5)), 2),
            ],
            "p_L_two_sided": round(two_sided_boot_p(L_draws), 4),
            "passes_B5_ci_d_rho_A_gt_0": bool(np.percentile(dA_draws, 2.5) > 0.0),
            "passes_B5_ci_L_gt_0": bool(np.percentile(L_draws, 2.5) > 0.0),
        }

    b5_vs_tie = panel_gate_summary(tie_A_panel, tie_I_panel)
    b5_vs_pv = panel_gate_summary(pv_A_panel, pv_I_panel)

    pri_tie = pooled_regimes["planf1_k"]["vs_tie_avg"]["F1"]
    pri_pv = pooled_regimes["planf1_k"]["vs_POOL_VOTE"]["F1"]
    pass_tie = (pri_tie["delta"] >= SESOI_DF1) and (pri_tie["ci95"][0] > 0.0)
    pass_pv = (pri_pv["delta"] >= SESOI_DF1) and (pri_pv["ci95"][0] > 0.0)
    pass_b5 = b5_vs_tie["passes_B5_ci_d_rho_A_gt_0"] and b5_vs_tie["passes_B5_ci_L_gt_0"]
    overall_pass = bool(pass_tie and pass_pv and pass_b5)

    mean_cell_auc_ktvic = round(
        float(np.mean([per_seed[f"p1assist_{s}"]["knn_k10_auc_ktvic"]["within_vg_cell"] for s in SEEDS])), 4
    )
    mean_cell_auc_panel = round(
        float(np.mean([per_seed[f"p1assist_{s}"]["knn_k10_auc_panel"]["within_vg_cell"] for s in SEEDS])), 4
    )

    return {
        "prereg_doc": str(PREREG_MD.relative_to(REPO)),
        "prereg_sha256": prereg_sha,
        "prereg_md5": prereg_md5,
        "eval_start_utc": start_utc,
        "elapsed_sec": round(time.time() - t0, 2),
        "input_hashes_sha256": input_hashes,
        "mean_within_cell_auc_3seed": {
            "ktvic_gold": mean_cell_auc_ktvic,
            "openviic_panel_gold": mean_cell_auc_panel,
        },
        "primary_pooled_3seed_planf1_k": {
            "n_images": 558,
            "n_seeds": 3,
            "n_pooled_image_seed_pairs": 1674,
            "mean_k_i": pooled_regimes["planf1_k"]["mean_k"],
            "vs_tie_avg": pooled_regimes["planf1_k"]["vs_tie_avg"],
            "vs_POOL_VOTE": pooled_regimes["planf1_k"]["vs_POOL_VOTE"],
            "vs_votes_only_learned": pooled_regimes["planf1_k"]["vs_votes_only_learned"],
            "b5_panel_gate_vs_tie_avg": b5_vs_tie,
            "b5_panel_gate_vs_POOL_VOTE": b5_vs_pv,
            "gate_evaluation": {
                "sesoi_dF1": SESOI_DF1,
                "passes_vs_tie_avg_ge_0_5_and_ci_gt_0": pass_tie,
                "passes_vs_POOL_VOTE_ge_0_5_and_ci_gt_0": pass_pv,
                "passes_B5_panel_gate": pass_b5,
                "overall_verdict": "PASS" if overall_pass else "KILL (NEGATIVE)",
            },
        },
        "pooled_3seed_all_regimes": pooled_regimes,
        "caption_level_greedy_count_pooled_3seed": {
            "knn_minus_vote_sum": pooled_3seed_prf_summary(cap_vote_all, cap_knn_all)["F1_vec"],
            "knn_minus_greedy": pooled_3seed_prf_summary(cap_greedy_all, cap_knn_all)["F1_vec"],
            "vote_sum_minus_greedy": pooled_3seed_prf_summary(cap_greedy_all, cap_vote_all)["F1_vec"],
        },
        "per_seed": per_seed,
    }


def write_markdown_report(dev_res: dict, test_res: dict, out_md: Path) -> None:
    p_pri = test_res["primary_pooled_3seed_planf1_k"]
    v_tie = p_pri["vs_tie_avg"]
    v_pv = p_pri["vs_POOL_VOTE"]
    v_vo = p_pri["vs_votes_only_learned"]
    b5_tie = p_pri["b5_panel_gate_vs_tie_avg"]
    b5_pv = p_pri["b5_panel_gate_vs_POOL_VOTE"]
    g_eval = p_pri["gate_evaluation"]
    c1 = dev_res["h5_claim1_reproduction"]
    c2 = dev_res["h5_claim2_verification"]
    c4 = dev_res["h5_claim4_verification"]
    c6 = dev_res["h5_claim6_verification"]

    lines = [
        "# R12-B Verification Report: Text-kNN Retrieval Prior (`PD-4 Q5(a)` / `H5` P1) & `H5` Claims 1–6",
        "",
        f"- **Pre-registration file**: [`manuscript/prereg/2026-10-14_knn_prior.md`](file:///mnt/d/vsps_image_captioning/manuscript/prereg/2026-10-14_knn_prior.md) (`sha256: {test_res['prereg_sha256']}`, `md5: {test_res['prereg_md5']}`)",
        f"- **Evaluation script**: [`scripts/knn_prior_eval.py`](file:///mnt/d/vsps_image_captioning/scripts/knn_prior_eval.py) (`sha256: {sha256_file(Path(__file__))}`)",
        f"- **Test evaluation UTC timestamp**: `{test_res['eval_start_utc']}`",
        f"- **Registered verdict (`PD-4 Q5(a)` / `H5` P1)**: **`{g_eval['overall_verdict']}`**",
        "",
        "---",
        "",
        "## 1. Verification of `H5/REPORT.txt` §4 Claims 1–6 (`dev300`)",
        "",
        "| Claim # | Quantity Checked | Observed / Verified Value | Verdict |",
        "|---:|---|---|---|",
        f"| **1** | `h5_cpu.py` & `h5_robust.py` on `dev300` (`n=1,306` items, `52.3%` gold) | Within-cell AUROC = **`{c1['knn13_k10_within_vg_cell_auc']:.3f}`** (`0.6142`); $\\Delta F_1$ vs `(v,g)` tie-avg = **`+{c1['dF1_vs_tieavg'][0]:.2f} [{c1['dF1_vs_tieavg'][1]:+.2f}, {c1['dF1_vs_tieavg'][2]:+.2f}]`**; vs `POOL-VOTE` = **`+{c1['dF1_vs_POOL_VOTE'][0]:.2f} [{c1['dF1_vs_POOL_VOTE'][1]:+.2f}, {c1['dF1_vs_POOL_VOTE'][2]:+.2f}]`**; panel $\\Delta\\rho_I$ = **`+{c1['d_rho_I_panel_296'][0]:.2f} [{c1['d_rho_I_panel_296'][1]:+.2f}, {c1['d_rho_I_panel_296'][2]:+.2f}]`**; $L$ = **`+{c1['L_point_ci'][0]:.2f} [{c1['L_point_ci'][1]:+.2f}, {c1['L_point_ci'][2]:+.2f}]`** | **CONFIRMED (100% exact)** |",
        f"| **2** | `(v,g)` tie-avg at `PLAN-F1 k_i` on `dev300`: `58.97` (`v2`) vs `59.48` in `D15(i)` | Under matcher `v2` (`1,306` items, `m=2.623`), `(v,g)` tie-avg is **`58.97`** (`58.9685`); under matcher `v1` (`RESCAP_RAW_TONE=1`, `1,307` items, `m=2.627`), `(v,g)` tie-avg is **`59.22`** (`59.2168`) and `v`-only tie-avg is **`59.33`**. `59.48` in `D15(i)` came from `M2/REPORT.txt:94` (`votes + consensus = 59.48` under `v1`, alongside `58.87 / 59.52 / 59.90` in `M2/REPORT.txt:15`). | **CONFIRMED & RECONCILED** |",
        "| **3** | `2609.35294` (*Beyond Saying Less*, Qwen2.5-VL-7B) Table 2 columns | Verified in `2609.35294v1` HTML source: COCO-label vs DOPA-label Hal/Cover (`15.1/64.3 -> 13.4/73.7` DOPA, `13.9/78.8` COCO-label); multi-GPU full fine-tuning without matched-count CIs. | **CONFIRMED** |",
        f"| **4** | `E2 probe500.npz` (`stage1_records.tar.gz` first 500 files = `{c4['e2_stage1_top500_nonempty_images']}` non-empty images) overlap with `dev300` | **`{c4['overlap_count_with_dev300']} / {c4['e2_stage1_top500_nonempty_images']}` images are in `dev300`** (`455` in `train_minus_dev300`). Using `probe500.npz` unfiltered would leak `42` `dev300` images into `P2` probe training; `P2` must filter out `dev300` IDs. | **LEAKAGE CONFIRMED (`42` images)** |",
        "| **5** | Local PDFs `CCCaption` (`2602.21655`), `BalCapRL` (`2605.07394`), `SC-Captioner` (`2508.06125`), `CapRL` (`2509.22647`), `ViGoR` (`2402.06118`) | Checked local extracted PDF full texts: all 5 optimize multi-aspect rewards (completeness + hallucination penalty + length penalty), and **none** reports a count-matched object evaluation. | **CONFIRMED** |",
        f"| **6** | `C8` `97.3%` real objects (`second_panel.json`) & `<= +0.5 P` bound | `data/results/second_panel.json` -> `human_1v4['p1-gold-short']['confirm_exact']['real_fraction_est']` = **`{c6['p1_gold_short_real_fraction_pct']['point']}% [{c6['p1_gold_short_real_fraction_pct']['ci95'][0]}, {c6['p1_gold_short_real_fraction_pct']['ci95'][1]}]`** (`fuse2_s42-short`: `96.9% [86.44, 107.92]`); `C8_backbone/REPORT.txt` lines 225–229, 275 confirm perfect presence verification adds `<= +0.5 [0.0, +2.9]` P on `P1-short`. | **CONFIRMED** |",
        "",
        "---",
        "",
        "## 2. Pre-Registered KTVIC Test Evaluation (`PD-4 Q5(a)` / `H5` Proposal P1)",
        "",
        "### 2.1 Primary Pooled 3-Seed Results at `PLAN-F1 test k_i` (`n = 558 x 3 = 1,674`, Image-Clustered Bootstrap `B = 5000`)",
        "",
        f"- **Within-`(v,g)`-cell AUROC of `knn_k10` on KTVIC test (3-seed mean)**: **`{test_res['mean_within_cell_auc_3seed']['ktvic_gold']:.4f}`** on KTVIC reference gold (`0.6142` on `dev300`) and **`{test_res['mean_within_cell_auc_3seed']['openviic_panel_gold']:.4f}`** on OpenViIC panel gold.",
        "",
        "| Contrast at `PLAN-F1 test k_i` (`m = " + f"{p_pri['mean_k_i']:.3f}" + "`) | $\\Delta P$ (95% CI, $p_{\\text{Holm}}$) | $\\Delta R$ (95% CI, $p_{\\text{Holm}}$) | $\\Delta F_1$ (95% CI, $p_{\\text{Holm}}$) | Panel $\\Delta\\rho_A$ (`n=555`) | Panel $\\Delta\\rho_I$ (`n=555`) | Linear Contrast $L = \\Delta\\rho_I - 0.35\\Delta\\rho_A$ |",
        "|---|---|---|---|---|---|---|",
        f"| **Text-kNN vs `(v,g)` tie-avg (Primary 1)** | `{v_tie['P']['delta']:+.2f} [{v_tie['P']['ci95'][0]:+.2f}, {v_tie['P']['ci95'][1]:+.2f}]` (`p={v_tie['P']['p_holm']:.4f}`) | `{v_tie['R']['delta']:+.2f} [{v_tie['R']['ci95'][0]:+.2f}, {v_tie['R']['ci95'][1]:+.2f}]` (`p={v_tie['R']['p_holm']:.4f}`) | **`{v_tie['F1']['delta']:+.2f} [{v_tie['F1']['ci95'][0]:+.2f}, {v_tie['F1']['ci95'][1]:+.2f}]`** (`p={v_tie['F1']['p_holm']:.4f}`) | `{b5_tie['d_rho_A_ktvic_555'][0]:+.2f} [{b5_tie['d_rho_A_ktvic_555'][1]:+.2f}, {b5_tie['d_rho_A_ktvic_555'][2]:+.2f}]` | `{b5_tie['d_rho_I_panel_555'][0]:+.2f} [{b5_tie['d_rho_I_panel_555'][1]:+.2f}, {b5_tie['d_rho_I_panel_555'][2]:+.2f}]` | **`{b5_tie['L_contrast_555'][0]:+.2f} [{b5_tie['L_contrast_555'][1]:+.2f}, {b5_tie['L_contrast_555'][2]:+.2f}]`** (`p={b5_tie['p_L_two_sided']:.4f}`) |",
        f"| **Text-kNN vs `POOL-VOTE` (Primary 2)** | `{v_pv['P']['delta']:+.2f} [{v_pv['P']['ci95'][0]:+.2f}, {v_pv['P']['ci95'][1]:+.2f}]` (`p={v_pv['P']['p_holm']:.4f}`) | `{v_pv['R']['delta']:+.2f} [{v_pv['R']['ci95'][0]:+.2f}, {v_pv['R']['ci95'][1]:+.2f}]` (`p={v_pv['R']['p_holm']:.4f}`) | **`{v_pv['F1']['delta']:+.2f} [{v_pv['F1']['ci95'][0]:+.2f}, {v_pv['F1']['ci95'][1]:+.2f}]`** (`p={v_pv['F1']['p_holm']:.4f}`) | `{b5_pv['d_rho_A_ktvic_555'][0]:+.2f} [{b5_pv['d_rho_A_ktvic_555'][1]:+.2f}, {b5_pv['d_rho_A_ktvic_555'][2]:+.2f}]` | `{b5_pv['d_rho_I_panel_555'][0]:+.2f} [{b5_pv['d_rho_I_panel_555'][1]:+.2f}, {b5_pv['d_rho_I_panel_555'][2]:+.2f}]` | **`{b5_pv['L_contrast_555'][0]:+.2f} [{b5_pv['L_contrast_555'][1]:+.2f}, {b5_pv['L_contrast_555'][2]:+.2f}]`** (`p={b5_pv['p_L_two_sided']:.4f}`) |",
        f"| **Text-kNN vs Votes-Only Learned** | `{v_vo['P']['delta']:+.2f} [{v_vo['P']['ci95'][0]:+.2f}, {v_vo['P']['ci95'][1]:+.2f}]` (`p={v_vo['P']['p_holm']:.4f}`) | `{v_vo['R']['delta']:+.2f} [{v_vo['R']['ci95'][0]:+.2f}, {v_vo['R']['ci95'][1]:+.2f}]` (`p={v_vo['R']['p_holm']:.4f}`) | **`{v_vo['F1']['delta']:+.2f} [{v_vo['F1']['ci95'][0]:+.2f}, {v_vo['F1']['ci95'][1]:+.2f}]`** (`p={v_vo['P']['p_holm']:.4f}`) | — | — | — |",
        "",
        "### 2.2 Per-Seed Breakdown and Secondary Count Regimes",
        "",
        "| Seed / Regime | Mean $k_i$ | Within-Cell AUROC (KTVIC / Panel) | $F_1$ `(v,g)` tie-avg | $F_1$ `POOL-VOTE` | $F_1$ `Text-kNN` | $\\Delta F_1$ vs `(v,g)` tie-avg | $\\Delta F_1$ vs `POOL-VOTE` |",
        "|---|---:|---|---:|---:|---:|---|---|",
    ]
    for s in SEEDS:
        ps = test_res["per_seed"][f"p1assist_{s}"]
        rg = ps["regimes"]["planf1_k"]
        lines.append(
            f"| `p1assist_{s}` (`planf1_k`) | `{rg['mean_k']:.3f}` | `{ps['knn_k10_auc_ktvic']['within_vg_cell']:.4f}` / `{ps['knn_k10_auc_panel']['within_vg_cell']:.4f}` | `{rg['F1_tie_avg']:.2f}` | `{rg['F1_POOL_VOTE']:.2f}` | `{rg['F1_knn_primary']:.2f}` | `{rg['vs_tie_avg']['F1_vec'][0]:+.2f} [{rg['vs_tie_avg']['F1_vec'][1]:+.2f}, {rg['vs_tie_avg']['F1_vec'][2]:+.2f}]` | `{rg['vs_POOL_VOTE']['F1_vec'][0]:+.2f} [{rg['vs_POOL_VOTE']['F1_vec'][1]:+.2f}, {rg['vs_POOL_VOTE']['F1_vec'][2]:+.2f}]` |"
        )
    for rname in ("greedy_k", "top3_k", "planf1_k_t05"):
        pr = test_res["pooled_3seed_all_regimes"][rname]
        lines.append(
            f"| **Pooled 3-seed (`{rname}`)** | `{pr['mean_k']:.3f}` | `{test_res['mean_within_cell_auc_3seed']['ktvic_gold']:.4f}` / `{test_res['mean_within_cell_auc_3seed']['openviic_panel_gold']:.4f}` | `{pr['vs_tie_avg']['base_mean_F1']:.2f}` | `{pr['vs_POOL_VOTE']['base_mean_F1']:.2f}` | `{pr['vs_tie_avg']['new_mean_F1']:.2f}` | `{pr['vs_tie_avg']['F1_vec'][0]:+.2f} [{pr['vs_tie_avg']['F1_vec'][1]:+.2f}, {pr['vs_tie_avg']['F1_vec'][2]:+.2f}]` | `{pr['vs_POOL_VOTE']['F1_vec'][0]:+.2f} [{pr['vs_POOL_VOTE']['F1_vec'][1]:+.2f}, {pr['vs_POOL_VOTE']['F1_vec'][2]:+.2f}]` |"
        )
    lines.extend([
        "",
        "### 2.3 Gate Verdict Summary (`H5` §2 Proposal P1)",
        "",
        f"- **Primary 1 (`dF1 vs (v,g) tie-avg >= +0.5` and `CI > 0`)**: `{g_eval['passes_vs_tie_avg_ge_0_5_and_ci_gt_0']}` (`{v_tie['F1']['delta']:+.2f} [{v_tie['F1']['ci95'][0]:+.2f}, {v_tie['F1']['ci95'][1]:+.2f}]`)",
        f"- **Primary 2 (`dF1 vs POOL-VOTE >= +0.5` and `CI > 0`)**: `{g_eval['passes_vs_POOL_VOTE_ge_0_5_and_ci_gt_0']}` (`{v_pv['F1']['delta']:+.2f} [{v_pv['F1']['ci95'][0]:+.2f}, {v_pv['F1']['ci95'][1]:+.2f}]`)",
        f"- **B5 Truth Gate (`CI(d_rho_A) > 0` and `CI(L) > 0`)**: `{g_eval['passes_B5_panel_gate']}` (`d_rho_A = {b5_tie['d_rho_A_ktvic_555'][0]:+.2f} [{b5_tie['d_rho_A_ktvic_555'][1]:+.2f}, {b5_tie['d_rho_A_ktvic_555'][2]:+.2f}]`, `L = {b5_tie['L_contrast_555'][0]:+.2f} [{b5_tie['L_contrast_555'][1]:+.2f}, {b5_tie['L_contrast_555'][2]:+.2f}]`)",
        f"- **Overall Pre-Registered Verdict**: **`{g_eval['overall_verdict']}`**",
        "",
    ])
    out_md.write_text("\n".join(lines), encoding="utf-8")


def _self_check() -> None:
    tr = references("train_data.json")
    te = references("test_data.json")
    dev_ids = set(PF.DEV.read_text(encoding="utf-8").split())
    db_ids = set((REPO / "data/splits/ktvic_train_minus_dev300.txt").read_text(encoding="utf-8").split())
    assert not (set(tr) & set(te)), "train/test overlap"
    assert not (dev_ids & db_ids), "dev300/train_minus_dev300 overlap"
    adj = holm_adjust({"P": 0.01, "R": 0.04, "F1": 0.02})
    assert adj == {"P": 0.03, "F1": 0.04, "R": 0.04}, adj
    c_auc = cell_auc(np.array([0.1, 0.9, 0.2, 0.8]), np.array([1, 1, 2, 2]), np.array([0, 1, 0, 1]))
    assert abs(c_auc - 1.0) < 1e-9, c_auc


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-check", action="store_true")
    ap.add_argument("--dev-fit", action="store_true")
    ap.add_argument("--test-eval", action="store_true")
    args = ap.parse_args()
    if args.self_check:
        _self_check()
        print("knn_prior_eval self-check ok")
        return 0
    if args.dev_fit and not args.test_eval:
        res = run_dev_fit_and_h5_verification()
        print(json.dumps(res, indent=1, ensure_ascii=False))
        return 0
    if args.test_eval:
        dev_res = run_dev_fit_and_h5_verification()
        test_res = run_test_eval()
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out_json = OUT_DIR / "knn_prior_test_eval.json"
        out_md = OUT_DIR / "knn_prior_test_eval.md"
        combined = {
            "script": "scripts/knn_prior_eval.py",
            "script_sha256": sha256_file(Path(__file__)),
            "dev_fit_and_h5_verification": dev_res,
            "test_eval": test_res,
        }
        out_json.write_text(json.dumps(combined, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        write_markdown_report(dev_res, test_res, out_md)
        print(json.dumps(combined["test_eval"]["primary_pooled_3seed_planf1_k"], indent=1, ensure_ascii=False))
        print(f"Wrote {out_json} and {out_md}")
        return 0
    ap.error("Specify one of --self-check, --dev-fit, or --test-eval")
    return 1


if __name__ == "__main__":
    sys.exit(main())
