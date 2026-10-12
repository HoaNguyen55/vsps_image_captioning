#!/usr/bin/env python
"""Pre-registered predictions for the KTVIC target-policy ladder (V4), and their check once preds land.

    NCS_DATA=data python3 scripts/prereg_ladder_check.py --check   # score landed runs against
                                         # manuscript/prereg/2026-10-12_ladder_predictions.json (repo root)
    python3 scripts/prereg_ladder_check.py   # rebuild the predictions: needs V4's op_train.json and
                                         # observed_runs.json next to this file (not in the repo) -> PREDICTIONS.json

Two models of where a trained captioner operates (counts = unique lexicon classes per caption, objects_in):
  L (length + learner frontier): count = the target rows' object count (training captions, operating_points.py)
     x a train->test ratio r bracketed by the two observed regimes (P1 1.102, fuse2 1.028); P and R from ONE
     learner frontier TP(M) = TP1 (M/M1)^b, R = c0 + c1 TP, anchored on P1 (3 seeds) and fuse2_s42-detailed.
  T (A1's implicit threshold, ideal learner): count ratios = ratios of E#{o: pi_o > tau_T} (operating_points.py).
Metric: object_prf.py vs the union of the 5 test references (Table IV), 558 KTVIC test images.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R_LO, R_HI, R_DET, R_DET_TOL = 1.028, 1.102, 1.028, 0.03   # observed output/target count ratios
SEED_M, RES_P, RES_R = 0.035, 1.0, 1.0                      # ~2 SD of seed noise (count) and frontier residuals


def frontier(obs: dict) -> dict:
    p1 = [obs[k] for k in ("p1-gold-short", "p1_s43-short", "p1_s44-short")]
    f = obs["fuse2_s42-detailed"]
    m1, t1 = (sum(r[k] for r in p1) / 3 for k in ("M", "TP"))
    r1 = sum(r["R"] for r in p1) / 3
    from math import log
    b = log(f["TP"] / t1) / log(f["M"] / m1)
    c1 = (f["R"] - r1) / (f["TP"] - t1)
    return {"M1": m1, "TP1": t1, "P1": 100 * t1 / m1, "R1": r1, "b": b, "c0": r1 - c1 * t1, "c1": c1}


def at(fr: dict, m: float) -> tuple[float, float, float]:
    tp = fr["TP1"] * (m / fr["M1"]) ** fr["b"]
    p, r = 100 * tp / m, fr["c0"] + fr["c1"] * tp
    return p, r, 2 * p * r / (p + r)


def point(fr, m, lo, hi, extra=None):
    """count interval -> P/R/F1 point and intervals on the frontier, widened by the residual tolerance."""
    (p, r, f), (pl, rl, _), (ph, rh, _) = at(fr, m), at(fr, lo), at(fr, hi)
    out = {"M": [round(m, 3), round(lo, 3), round(hi, 3)], "M_ratio_vs_P1": [round(x / fr["M1"], 3) for x in (m, lo, hi)],
           "P": [round(p, 1), round(min(pl, ph) - RES_P, 1), round(max(pl, ph) + RES_P, 1)],
           "R": [round(r, 1), round(min(rl, rh) - RES_R, 1), round(max(rl, rh) + RES_R, 1)], "F1": round(f, 1),
           "dP_vs_P1": round(p - fr["P1"], 1), "dR_vs_P1": round(r - fr["R1"], 1)}
    return out | (extra or {})


def build() -> dict:
    tr = json.loads((HERE / "op_train.json").read_text())["policies"]
    obs = json.loads((HERE / "observed_runs.json").read_text())
    fr = frontier(obs)
    L = {k: v["objects_per_row"] for k, v in tr.items()}
    ideal = {k: v["ideal_count_named"] for k, v in tr.items()}

    def short(pol, extra=None):
        lo, hi = L[pol] * R_LO - SEED_M, L[pol] * R_HI + SEED_M
        return point(fr, (lo + hi) / 2, lo, hi, extra)

    f2s, f2d = obs["fuse2_s42-short"], obs["fuse2_s42-detailed"]
    lo = L["rnd2-detailed"] * (R_DET - R_DET_TOL) - 0.05
    hi = L["rnd2-detailed"] * (R_DET + R_DET_TOL) + 0.05
    rnd2_det = point(fr, L["rnd2-detailed"] * R_DET, lo, hi, {
        "sentences_per_caption_min": 1.95,
        "M_ratio_vs_fuse2_s42_detailed": [0.78, 0.86],
        "T_model_M_ratio_vs_fuse2": round(ideal["rnd2-detailed"] / ideal["fuse2-detailed"], 3)})
    rep = lambda o, dm: {"M": [round(o["M"], 3), round(o["M"] - dm, 3), round(o["M"] + dm, 3)],  # noqa: E731
                         "P": [round(o["P"], 1), round(o["P"] - 1.5, 1), round(o["P"] + 1.5, 1)],
                         "R": [round(o["R"], 1), round(o["R"] - 1.5, 1), round(o["R"] + 1.5, 1)]}
    t_ratio = lambda pol: round(ideal[pol] / ideal["p1-short"], 3)  # noqa: E731
    runs = {
        "p1ep4_s42-short": short("p1-short", {
            "frontier_residual_P": "point in [-1.5, +1.0]; H0 rejected only if the 95% CI excludes 0",
            "T_model": "an ideal (better-fit) learner thresholds pi at 0.505: count falls toward the majority set "
                       "(1.24 on test); L predicts no fall below 1.63"}),
        "multiref_s42-short": short("multiref-short", {
            "frontier_residual_P_H0": "point in [-1.0, +1.0]; H0 rejected only if the 95% CI (~+-2 P) excludes 0",
            "H1_variance_channel": "frontier residual P >= +1.0 with a CI excluding 0 (A1 proxy: +3.0 mP net)",
            "A1_stated": "recall <= P1 recall - 2.0 (A1 7a.1: multiref ~4 recall points below P1)",
            "T_model_M_ratio_vs_P1": t_ratio("multiref-short"),
            "T_model_ideal_count_test": 1.28}),
        "cons_s42-short": short("cons-short", {
            "T_model_M_ratio_vs_P1": t_ratio("cons-short"),
            "discriminator": "M/M_P1 <= 1.30 supports L; >= 1.40 supports T (ideal ratio 1.47 train / 1.55 test)",
            "vs_fuse2_s42_short_H0": "|dM| <= 0.12, |dP| <= 1.5 (bleed-over absent)",
            "H1_bleed_over": "unsupported mentions/caption (1v4, A1 unsupported.py) <= 0.52 vs 0.57 for fuse2-short "
                             "AND frontier residual P >= fuse2-short's (+0.34) + 1.0 with a CI excluding 0"}),
        "unf2_s42-short": short("unf2-short", {
            "M_ratio_vs_cons_s42": [0.97, 1.06],
            "T_model_M_ratio_vs_cons": round(ideal["unf2-short"] / ideal["cons-short"], 3),
            "discriminator": "unf2/cons count >= 0.97 supports L; <= 0.95 supports T"}),
        "rnd2_s42-detailed": rnd2_det,
        "rnd2_s42-short": rep(f2s, 0.06) | {"note": "same short rows as fuse2 (consensus); H0 = fuse2_s42-short"},
        "fuse2_s43-detailed": rep(f2d, 0.10), "fuse2_s44-detailed": rep(f2d, 0.10),
        "fuse2_s43-short": rep(f2s, 0.06), "fuse2_s44-short": rep(f2s, 0.06),
    }
    structural = {
        "short_only_policies_in_detailed_mode": "p1ep4/cons/unf2/multiref with the detailed prompt write one sentence "
                                                 "(mean sentences <= 1.03) and M within +-0.08 of their short mode",
        "ordering_is_not_a_test": "L (no thresholds) predicts the recall order {p1, p1ep4, multiref} < {cons, unf2} < "
                                  "rnd2 < fuse2, identical to A1's tau order; A1's kill rule (Kendall tau-b < 0.6) "
                                  "cannot fail under L",
        "rank_test": "human_parity.py rank (offline F1 vs trained F1, 6 policies): L's points give trained F1 "
                     "fuse2 64.4 > rnd2 61.2 > unf2 58.5 >= cons 58.1 > p1 54.6 >= multiref 54.2, Kendall tau-b 0.87 "
                     "(one swap, cons/unf2), range [0.73, 1.0]; a pass is therefore predicted by length alone",
        "joint_frontier_invariance": "mean frontier residual over all landed ladder runs: 95% CI contains 0 and "
                                     "its point lies in [-0.8, +0.8] (per-run CIs are ~+-2 P at 558 images)",
        "selection_targets_stay_on_frontier": "any target chosen for precision at equal recall offline (A1 Bayes "
                                              "dial, consensus) lands within +-1.0 P of the learner frontier, as "
                                              "e5 (best-of-6 self-samples) already does (-0.4/-0.3)",
    }
    return {"timestamp": "2026-10-12", "author": "V4 adversarial verifier", "status": "pre-registered before any "
            "ladder prediction (cons/unf2/rnd2/multiref/p1ep4/fuse2_s43/s44) was in data/results",
            "metric": "object_prf.py ktvic_block vs the union of the 5 test references, 558 images; M = unique "
                      "lexicon classes per caption; intervals are [point, lo, hi]",
            "anchors": {"frontier": {k: round(v, 4) for k, v in fr.items()},
                        "observed": {k: {kk: round(v, 3) for kk, v in obs[k].items()} for k in (
                            "p1-gold-short", "p1_s43-short", "p1_s44-short", "fuse2_s42-short", "fuse2_s42-detailed")}},
            "training_targets": {k: {"objects_per_row": round(v["objects_per_row"], 3), "tau": round(v["tau"], 3),
                                     "ideal_count": round(v["ideal_count_named"], 3),
                                     "rows_per_image": round(v["rows_per_image"], 2)} for k, v in tr.items()},
            "models": {"L": "count from target length (r in [1.028, 1.102] short, 1.028+-0.03 detailed) + one learner "
                            "frontier (frontier invariance); tolerances: +-0.035 count (2 seed SD), +-1.0 P/R",
                       "T": "A1 implicit threshold, ideal learner: count ratios = ratios of E#{pi > tau}"},
            "runs": runs, "structural": structural}


ANCHORS = ("p1-gold-short", "p1_s43-short", "p1_s44-short", "fuse2_s42-detailed")


def residual(arr: dict, run: str, idx) -> float:
    """P of `run` minus the learner frontier's P at the run's count, anchors refitted on the images idx.
    arr[name] = (N, 3) per-image (tp, |M|, recall)."""
    s = {k: (a[idx, 0].mean(), a[idx, 1].mean(), 100 * a[idx, 2].mean()) for k, a in arr.items()}
    tp1, m1, r1 = (sum(s[k][j] for k in ANCHORS[:3]) / 3 for j in range(3))
    tpf, mf, rf = s[ANCHORS[3]]
    import math
    fr = {"M1": m1, "TP1": tp1, "b": math.log(tpf / tp1) / math.log(mf / m1), "c0": 0.0, "c1": 1.0}
    tp, m, _ = s[run]
    return 100 * tp / m - at(fr, m)[0]


def check(pred: dict, B: int = 1000) -> None:
    """Score every predicted run whose preds file exists (run from the repo root with NCS_DATA set); the frontier
    residual gets a 95% CI from image resampling shared by the run and the four anchor runs."""
    import numpy as np
    sys.path[:0] = [".", "scripts"]
    from evaluate import references
    from object_prf import image_counts, scores
    from rescap.chair import _ancestors, objects_in
    refs = references("test_data.json")
    gold = {str(k): set().union(*[set(objects_in(r)) for r in rs]) for k, rs in refs.items()}
    ids = sorted(gold)

    def load(name):
        f = Path("data/results") / f"{name}.preds.json"
        if not f.exists():
            return None
        caps = {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in json.loads(f.read_text()).items()}
        return [image_counts(set(objects_in(caps[i])), gold[i], _ancestors) for i in ids]
    arr = {k: np.array([r[:2] + (r[3],) for r in load(k)], float) for k in ANCHORS}
    rng = np.random.default_rng(0)
    draws = [rng.integers(0, len(ids), len(ids)) for _ in range(B)]
    pooled = {}
    for run, p in pred["runs"].items():
        rows = load(run)
        if rows is None:
            print(f"  {run:22s} not landed")
            continue
        s, m = scores(rows), sum(r[1] for r in rows) / len(rows)
        got = {"M": m, "P": s["P"], "R": s["R"]}
        arr[run] = np.array([r[:2] + (r[3],) for r in rows], float)
        res = residual(arr, run, np.arange(len(ids)))
        pooled[run] = [residual(arr, run, d) for d in draws]
        bs = sorted(pooled[run])
        print(f"  {run:22s} " + "  ".join(f"{k}={v:.3f} {'IN' if p[k][1] <= v <= p[k][2] else 'OUT'} {p[k]}"
                                           for k, v in got.items())
              + f"  frontier residual P={res:+.2f} [{bs[int(.025 * B)]:+.2f}, {bs[int(.975 * B) - 1]:+.2f}]")
    if len(pooled) > 1:  # joint H0: the mean residual over every landed run, same draws
        mean = sorted(sum(v[b] for v in pooled.values()) / len(pooled) for b in range(B))
        print(f"  mean frontier residual over {len(pooled)} runs: 95% CI [{mean[int(.025 * B)]:+.2f}, "
              f"{mean[int(.975 * B) - 1]:+.2f}]")


def _check_self() -> None:
    fr = {"M1": 1.0, "TP1": 0.8, "P1": 80.0, "R1": 40.0, "b": 0.75, "c0": 0.0, "c1": 50.0}
    p, r, _ = at(fr, 1.0)
    assert abs(p - 80) < 1e-9 and abs(r - 40) < 1e-9
    assert at(fr, 2.0)[0] < 80 < at(fr, 0.5)[0]          # precision falls along the frontier as count grows


if __name__ == "__main__":
    _check_self()
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        check(json.loads((HERE.parent / "manuscript/prereg/2026-10-12_ladder_predictions.json").read_text()))
    else:
        out = build()
        (HERE / "PREDICTIONS.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
        for k, v in out["runs"].items():
            print(f"{k:22s} M={v['M']} P={v['P']} R={v['R']}"
                  + (f" dP={v['dP_vs_P1']} dR={v['dR_vs_P1']} F1={v['F1']}" if "dP_vs_P1" in v else ""))
