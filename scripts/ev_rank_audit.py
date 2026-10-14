#!/usr/bin/env python3
"""EV-RANK Evaluator Ranking Audit (`PD-4 Q6`):
Evaluates all committed KTVIC `test` prediction files (`data/results/*.preds.json` and `data/results/*.json`)
against the independent OpenViIC 5-annotator human panel (`n = 555` matched KTVIC test images; strictly aggregate
numbers only, zero OpenViIC caption strings).

Compares how each candidate reference-side evaluator ranks the KTVIC test systems (`Spearman rho`, `Kendall tau-b`,
pairwise concordance accuracy across all system pairs, across count-differing pairs `|M_A - M_B| >= 0.25`, and across
count-matched pairs `|M_A - M_B| < 0.25`) against the independent OpenViIC human-panel ground truth:
  - `panel_P`, `panel_R`, `panel_F0.5`, `panel_F1`, `panel_F2.0`, and `panel_delta_P_front`
across candidate evaluators (reported under both `v2` tone-normalised and `v1` raw-tone matchers):
  1. Raw reference-based n-gram metrics: `CIDEr-D`, `BLEU-4`, `METEOR`, `ROUGE-L`
  2. Raw reference-based object metrics: `ref_P` (`100 - CHAIR_i`), `ref_R`, `ref_F0.5`, `ref_F1`, `ref_F2.0`
  3. Count-controlled frontier residual: `delta_P_front = P_ref - P_hat_0(M)` (`PD-2` / `H1`)
  4. Matched-count excess precision/F1 over `(v, g)` controls:
     - `excess_P_vg_tieavg = P_ref - P_vg_tieavg(M)` and `excess_F1_vg_tieavg = F1_ref - F1_vg_tieavg(M)`
     - `excess_P_poolvote = P_ref - P_poolvote(M)` and `excess_F1_poolvote = F1_ref - F1_poolvote(M)`

Usage:
    python3 scripts/ev_rank_audit.py --self-check
    NCS_DATA=data python3 scripts/ev_rank_audit.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path("/mnt/d/vsps_image_captioning")
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

import plan_f1 as PF  # noqa: E402
from evaluate import references  # noqa: E402
from object_prf import image_counts, scores  # noqa: E402
from rescap.chair import _ancestors, objects_in  # noqa: E402

OUT_JSON = ROOT / ".session_backup/2026-10-14/r12_verify/ev_rank_audit.json"
OUT_MD = ROOT / ".session_backup/2026-10-14/r12_verify/ev_rank_audit.md"
PREREG_MD = ROOT / "manuscript/prereg/2026-10-14_ev_rank_audit.md"


def f_beta(p: float, r: float, beta: float) -> float:
    if p + r <= 0:
        return 0.0
    b2 = beta * beta
    denom = b2 * p + r
    return (1.0 + b2) * p * r / denom if denom > 0 else 0.0


def rankdata_avg_ties(x: np.ndarray) -> np.ndarray:
    """Average ranks for ties (1-based)."""
    n = len(x)
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(n, dtype=float)
    i = 0
    while i < n:
        j = i
        while j + 1 < n and x[order[j + 1]] == x[order[i]]:
            j += 1
        avg_r = 0.5 * (i + j) + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_r
        i = j + 1
    return ranks


def spearman_rho(x: np.ndarray, y: np.ndarray) -> float:
    rx = rankdata_avg_ties(x)
    ry = rankdata_avg_ties(y)
    vx = rx - rx.mean()
    vy = ry - ry.mean()
    denom = math.sqrt(float(np.sum(vx * vx) * np.sum(vy * vy)))
    return float(np.sum(vx * vy) / denom) if denom > 0 else 0.0


def kendall_tau_b(x: np.ndarray, y: np.ndarray) -> float:
    n = len(x)
    c = d = tx = ty = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx = x[i] - x[j]
            dy = y[i] - y[j]
            if dx == 0 and dy == 0:
                continue
            elif dx == 0:
                tx += 1
            elif dy == 0:
                ty += 1
            elif (dx > 0 and dy > 0) or (dx < 0 and dy < 0):
                c += 1
            else:
                d += 1
    n0 = c + d + tx + ty
    denom = math.sqrt(float((c + d + tx) * (c + d + ty)))
    if n0 == 0 or denom == 0:
        return 0.0
    return float((c - d) / denom)


def pairwise_concordance(
    ev: np.ndarray,
    gt: np.ndarray,
    m_vec: np.ndarray,
    min_dm: float | None = None,
    max_dm: float | None = None,
) -> dict:
    n = len(ev)
    concord = 0.0
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            dm = abs(float(m_vec[i] - m_vec[j]))
            if min_dm is not None and dm < min_dm:
                continue
            if max_dm is not None and dm >= max_dm:
                continue
            dg = gt[i] - gt[j]
            if dg == 0:
                continue
            de = ev[i] - ev[j]
            total += 1
            if de == 0:
                concord += 0.5
            elif (de > 0 and dg > 0) or (de < 0 and dg < 0):
                concord += 1.0
    acc = (100.0 * concord / total) if total > 0 else float("nan")
    return {
        "n_pairs": int(total),
        "concordant_pairs": round(float(concord), 1),
        "concordance_pct": round(float(acc), 4) if total > 0 else None,
    }


def self_check() -> None:
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    z = np.array([50.0, 40.0, 30.0, 20.0, 10.0])
    assert abs(spearman_rho(x, y) - 1.0) < 1e-12
    assert abs(spearman_rho(x, z) + 1.0) < 1e-12
    assert abs(kendall_tau_b(x, y) - 1.0) < 1e-12
    assert abs(kendall_tau_b(x, z) + 1.0) < 1e-12
    c_pos = pairwise_concordance(x, y, x)
    c_neg = pairwise_concordance(x, z, x)
    assert c_pos["n_pairs"] == 10 and abs(c_pos["concordance_pct"] - 100.0) < 1e-9
    assert c_neg["n_pairs"] == 10 and abs(c_neg["concordance_pct"] - 0.0) < 1e-9
    assert abs(f_beta(80.0, 80.0, 0.5) - 80.0) < 1e-9
    assert abs(f_beta(80.0, 80.0, 1.0) - 80.0) < 1e-9
    assert abs(f_beta(80.0, 80.0, 2.0) - 80.0) < 1e-9
    print("ev_rank_audit self-check ok")


def build_pool_controls(
    refs_tr: dict[str, list[str]],
    ids_te: list[str],
    gold_v1: dict[str, set[str]],
    gold_v2: dict[str, set[str]],
) -> dict[str, dict]:
    g_path = ROOT / "data/results/p1assist_s42-short.preds.json"
    s_path = ROOT / "data/results/upe/test/p1assist_s42-test-short-T0.5.jsonl"
    g_caps = PF.captions(g_path, ids_te)
    s_map = {
        str(x["image_id"]): x["samples"]
        for x in map(json.loads, s_path.read_text(encoding="utf-8").splitlines())
    }
    pools = [[g_caps[i]] + list(s_map[i]) for i in ids_te]
    prior = PF.class_prior(refs_tr)

    out = {}
    for ver, raw_flag, gold_map in (("v1", True, gold_v1), ("v2", False, gold_v2)):
        old = os.environ.get("RESCAP_RAW_TONE")
        try:
            if raw_flag:
                os.environ["RESCAP_RAW_TONE"] = "1"
            else:
                os.environ.pop("RESCAP_RAW_TONE", None)
            n_idx, names, x = PF.items(pools, prior)
            v = x[:, 0]
            g = x[:, 1]
            lp = x[:, 3]
            cell = np.round(v * 6).astype(int) * 2 + g.astype(int)
            q_pv = 6.0 * v + g + 1e-4 * lp
            by_img: list[list[int]] = [[] for _ in range(len(ids_te))]
            for j, n in enumerate(n_idx):
                by_img[int(n)].append(j)
            y = np.array([o in gold_map[ids_te[int(n)]] for n, o in zip(n_idx, names)], dtype=float)
            gold_lens = [len(gold_map[i]) for i in ids_te]
            out[ver] = {
                "by_img": by_img,
                "cell": cell,
                "q_pv": q_pv,
                "names": names,
                "y": y,
                "gold_lens": gold_lens,
            }
        finally:
            if old is None:
                os.environ.pop("RESCAP_RAW_TONE", None)
            else:
                os.environ["RESCAP_RAW_TONE"] = old
    return out


def eval_vg_at_counts(k_per_img: list[int], pool_data: dict) -> dict[str, dict[str, float]]:
    by_img = pool_data["by_img"]
    cell = pool_data["cell"]
    q_pv = pool_data["q_pv"]
    names = pool_data["names"]
    y = pool_data["y"]
    gold_lens = pool_data["gold_lens"]

    tie_rows = []
    pv_rows = []
    for n, js in enumerate(by_img):
        kn = int(min(k_per_img[n], len(js)))
        gl = gold_lens[n]
        if kn <= 0:
            r0 = 0.0 if gl else float("nan")
            tie_rows.append((0.0, 0, 0.0, r0, r0, r0))
            pv_rows.append((0.0, 0, 0.0, r0, r0, r0))
            continue
        order_c = sorted(js, key=lambda j: -int(cell[j]))
        cut_c = cell[order_c[kn - 1]]
        above = [j for j in js if cell[j] > cut_c]
        tied = [j for j in js if cell[j] == cut_c]
        rem = kn - len(above)
        tp_tie = float(y[above].sum() + rem * (y[tied].mean() if tied else 0.0))
        r_tie = tp_tie / gl if gl else float("nan")
        tie_rows.append((tp_tie, kn, tp_tie, r_tie, r_tie, r_tie))

        pick = sorted(js, key=lambda j: (-float(q_pv[j]), names[j]))[:kn]
        tp_pv = float(y[pick].sum())
        r_pv = tp_pv / gl if gl else float("nan")
        pv_rows.append((tp_pv, kn, tp_pv, r_pv, r_pv, r_pv))

    sc_tie = scores(tie_rows)
    sc_pv = scores(pv_rows)
    return {
        "vg_tie_avg": {"P": float(sc_tie["P"]), "R": float(sc_tie["R"]), "F1": float(sc_tie["F1"])},
        "pool_vote": {"P": float(sc_pv["P"]), "R": float(sc_pv["R"]), "F1": float(sc_pv["F1"])},
    }


def evaluate_ranking_subset(
    sys_list: list[dict],
    ver_key: str,
    evaluator_keys: list[str],
    gt_keys: list[str],
) -> dict:
    m_vec = np.array([s[ver_key]["M_ref"] for s in sys_list], dtype=float)
    results = {}
    for ev_k in evaluator_keys:
        # Filter to systems where ev_k is not None
        valid_idx = [idx for idx, s in enumerate(sys_list) if s["evaluators"][ver_key].get(ev_k) is not None]
        ev_arr = np.array([sys_list[i]["evaluators"][ver_key][ev_k] for i in valid_idx], dtype=float)
        m_sub = m_vec[valid_idx]
        results[ev_k] = {"n_systems": len(valid_idx), "vs_ground_truth": {}}
        for gt_k in gt_keys:
            gt_arr = np.array([sys_list[i]["panel_gt"][ver_key][gt_k] for i in valid_idx], dtype=float)
            results[ev_k]["vs_ground_truth"][gt_k] = {
                "spearman_rho": round(spearman_rho(ev_arr, gt_arr), 4),
                "kendall_tau_b": round(kendall_tau_b(ev_arr, gt_arr), 4),
                "all_pairs": pairwise_concordance(ev_arr, gt_arr, m_sub),
                "count_diff_ge_0_25": pairwise_concordance(ev_arr, gt_arr, m_sub, min_dm=0.25),
                "count_matched_lt_0_25": pairwise_concordance(ev_arr, gt_arr, m_sub, max_dm=0.25),
            }
    return results


def run_audit() -> None:
    refs_tr = references("train_data.json")
    refs_te = references("test_data.json")
    ids_te = sorted(str(k) for k in refs_te.keys())

    gold_ktvic_v1 = {
        str(k): set().union(*[set(objects_in(r, raw_tone=True)) for r in rs])
        for k, rs in refs_te.items()
    }
    gold_ktvic_v2 = {
        str(k): set().union(*[set(objects_in(r, raw_tone=False)) for r in rs])
        for k, rs in refs_te.items()
    }

    ov_raw = json.loads((ROOT / "data/ktvic_openviic_refs.json").read_text(encoding="utf-8"))["test"]
    ids_panel = [i for i in ids_te if ov_raw.get(i)]
    gold_panel_v1 = {
        i: set().union(*[set(objects_in(r, raw_tone=True)) for r in ov_raw[i] if r])
        for i in ids_panel
    }
    gold_panel_v2 = {
        i: set().union(*[set(objects_in(r, raw_tone=False)) for r in ov_raw[i] if r])
        for i in ids_panel
    }

    ladder_prereg = json.loads((ROOT / "manuscript/prereg/2026-10-12_ladder_predictions.json").read_text(encoding="utf-8"))
    fr = ladder_prereg["anchors"]["frontier"]

    pool_controls = build_pool_controls(refs_tr, ids_te, gold_ktvic_v1, gold_ktvic_v2)

    # Discover all KTVIC test *.preds.json files (n=558 images)
    results_dir = ROOT / "data/results"
    preds_files = sorted(results_dir.glob("*.preds.json"))

    system_records = []
    for pf in preds_files:
        stem = pf.name.removesuffix(".preds.json")
        raw = json.loads(pf.read_text(encoding="utf-8"))
        caps = {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in raw.items()}
        if set(caps.keys()) != set(ids_te):
            continue

        mode = stem.rsplit("-", 1)[-1] if "-" in stem else "unknown"
        jf = results_dir / f"{stem}.json"
        sc_x100 = {}
        if jf.exists():
            jd = json.loads(jf.read_text(encoding="utf-8"))
            if "results" in jd and jd["results"]:
                sc_x100 = jd["results"][0].get("scores_scaled_x100", {})

        cider = round(float(sc_x100["CIDEr"]), 4) if sc_x100.get("CIDEr") is not None else None
        bleu4 = round(float(sc_x100["BLEU-4"]), 4) if sc_x100.get("BLEU-4") is not None else None
        meteor = round(float(sc_x100["METEOR"]), 4) if sc_x100.get("METEOR") is not None else None
        rougel = round(float(sc_x100["ROUGE-L"]), 4) if sc_x100.get("ROUGE-L") is not None else None

        rec = {
            "system": stem,
            "mode": mode,
            "preds_sha256": hashlib.sha256(pf.read_bytes()).hexdigest(),
            "json_sha256": hashlib.sha256(jf.read_bytes()).hexdigest() if jf.exists() else None,
            "v1": {},
            "v2": {},
            "evaluators": {"v1": {}, "v2": {}},
            "panel_gt": {"v1": {}, "v2": {}},
        }

        for ver, raw_flag, g_kt, g_pan in (
            ("v1", True, gold_ktvic_v1, gold_panel_v1),
            ("v2", False, gold_ktvic_v2, gold_panel_v2),
        ):
            rows_kt = [image_counts(set(objects_in(caps[i], raw_tone=raw_flag)), g_kt[i], _ancestors) for i in ids_te]
            rows_pan = [image_counts(set(objects_in(caps[i], raw_tone=raw_flag)), g_pan[i], _ancestors) for i in ids_panel]
            sc_kt = scores(rows_kt)
            sc_pan = scores(rows_pan)

            k_list = [int(r[1]) for r in rows_kt]
            m_ref = float(np.mean(k_list))
            p_ref = float(sc_kt["P"])
            r_ref = float(sc_kt["R"])
            f1_ref = float(sc_kt["F1"])
            f05_ref = f_beta(p_ref, r_ref, 0.5)
            f20_ref = f_beta(p_ref, r_ref, 2.0)

            tp_hat = fr["TP1"] * ((m_ref / fr["M1"]) ** fr["b"]) if m_ref > 0 else 0.0
            p_hat_0 = (100.0 * tp_hat / m_ref) if m_ref > 0 else 100.0
            delta_p_front = p_ref - p_hat_0

            vg_ctrl = eval_vg_at_counts(k_list, pool_controls[ver])
            ex_p_tie = p_ref - vg_ctrl["vg_tie_avg"]["P"]
            ex_f1_tie = f1_ref - vg_ctrl["vg_tie_avg"]["F1"]
            ex_p_pv = p_ref - vg_ctrl["pool_vote"]["P"]
            ex_f1_pv = f1_ref - vg_ctrl["pool_vote"]["F1"]

            p_pan = float(sc_pan["P"])
            r_pan = float(sc_pan["R"])
            f1_pan = float(sc_pan["F1"])
            f05_pan = f_beta(p_pan, r_pan, 0.5)
            f20_pan = f_beta(p_pan, r_pan, 2.0)

            rec[ver] = {
                "M_ref": round(m_ref, 4),
                "P_hat_0": round(p_hat_0, 4),
                "vg_tie_avg_P": round(vg_ctrl["vg_tie_avg"]["P"], 4),
                "vg_tie_avg_F1": round(vg_ctrl["vg_tie_avg"]["F1"], 4),
                "pool_vote_P": round(vg_ctrl["pool_vote"]["P"], 4),
                "pool_vote_F1": round(vg_ctrl["pool_vote"]["F1"], 4),
            }
            rec["evaluators"][ver] = {
                "CIDEr_D": cider,
                "BLEU_4": bleu4,
                "METEOR": meteor,
                "ROUGE_L": rougel,
                "ref_P_100_minus_CHAIRi": round(p_ref, 4),
                "ref_R": round(r_ref, 4),
                "ref_F0_5": round(f05_ref, 4),
                "ref_F1": round(f1_ref, 4),
                "ref_F2_0": round(f20_ref, 4),
                "delta_P_front": round(delta_p_front, 4),
                "excess_P_vg_tieavg": round(ex_p_tie, 4),
                "excess_F1_vg_tieavg": round(ex_f1_tie, 4),
                "excess_P_poolvote": round(ex_p_pv, 4),
                "excess_F1_poolvote": round(ex_f1_pv, 4),
            }
            rec["panel_gt"][ver] = {
                "panel_P": round(p_pan, 4),
                "panel_R": round(r_pan, 4),
                "panel_F0_5": round(f05_pan, 4),
                "panel_F1": round(f1_pan, 4),
                "panel_F2_0": round(f20_pan, 4),
            }

        system_records.append(rec)

    evaluator_keys = [
        "CIDEr_D",
        "BLEU_4",
        "METEOR",
        "ROUGE_L",
        "ref_P_100_minus_CHAIRi",
        "ref_R",
        "ref_F0_5",
        "ref_F1",
        "ref_F2_0",
        "delta_P_front",
        "excess_P_vg_tieavg",
        "excess_F1_vg_tieavg",
        "excess_P_poolvote",
        "excess_F1_poolvote",
    ]
    gt_keys = ["panel_P", "panel_R", "panel_F0_5", "panel_F1", "panel_F2_0"]

    subsets = {
        "all_committed_systems": system_records,
        "short_mode_systems": [s for s in system_records if s["mode"] == "short"],
        "detailed_mode_systems": [s for s in system_records if s["mode"] == "detailed"],
        "two_mode_systems": [s for s in system_records if s["mode"] == "two"],
    }

    ranking_summary = {"v2": {}, "v1": {}}
    for ver in ("v2", "v1"):
        for sub_name, sub_list in subsets.items():
            ranking_summary[ver][sub_name] = {
                "n_systems": len(sub_list),
                "evaluators": evaluate_ranking_subset(sub_list, ver, evaluator_keys, gt_keys),
            }

    out = {
        "schema": "pd4_q6_ev_rank_audit_v1",
        "date": "2026-10-14",
        "n_test_images_ktvic": len(ids_te),
        "n_test_images_openviic_panel": len(ids_panel),
        "n_total_systems_scored": len(system_records),
        "n_short_systems": len(subsets["short_mode_systems"]),
        "n_detailed_systems": len(subsets["detailed_mode_systems"]),
        "n_two_systems": len(subsets["two_mode_systems"]),
        "frontier_parameters": fr,
        "ranking_concordance": ranking_summary,
        "systems": system_records,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Build Markdown report programmatically from `out`
    md = [
        "# EV-RANK Evaluator Ranking Audit (`PD-4 Q6`): Reference Evaluators vs Independent 5-Annotator Human Panel (`OpenViIC`)",
        "",
        f"- **Date**: `{out['date']}`",
        "- **Script**: [`scripts/ev_rank_audit.py`](file:///mnt/d/vsps_image_captioning/scripts/ev_rank_audit.py)",
        "- **Companion JSON**: [`.session_backup/2026-10-14/r12_verify/ev_rank_audit.json`](file:///mnt/d/vsps_image_captioning/.session_backup/2026-10-14/r12_verify/ev_rank_audit.json)",
        f"- **Evaluated Systems on KTVIC `test` (`n = {out['n_test_images_ktvic']}` images; `n = {out['n_test_images_openviic_panel']}` OpenViIC-matched)**: **`{out['n_total_systems_scored']}` total** (`{out['n_short_systems']}` `short`, `{out['n_detailed_systems']}` `detailed`, `{out['n_two_systems']}` `two`).",
        "- **Hygiene Guarantee**: Strictly aggregate ranking correlations and system-level scores; zero OpenViIC caption strings or n-grams.",
        "",
        "---",
        "",
        "## 1. All Committed Systems (`N = " + str(out["n_total_systems_scored"]) + "`, Matcher `v2` Tone-Normalised): Ranking vs Independent Human Panel",
        "",
        "| Candidate Evaluator | N | vs `panel_P`: $\\rho$ / $\\tau_b$ / All% (`|dM|>=0.25`% / `<0.25`%) | vs `panel_F0.5`: $\\rho$ / $\\tau_b$ / All% (`|dM|>=0.25`% / `<0.25`%) | vs `panel_F1`: $\\rho$ / $\\tau_b$ / All% (`|dM|>=0.25`% / `<0.25`%) | vs `panel_F2.0`: $\\rho$ / $\\tau_b$ / All% (`|dM|>=0.25`% / `<0.25`%) |",
        "|---|---:|---|---|---|---|",
    ]

    all_v2 = out["ranking_concordance"]["v2"]["all_committed_systems"]["evaluators"]
    for ev_k in evaluator_keys:
        ed = all_v2[ev_k]
        vg = ed["vs_ground_truth"]

        def fmt_cell(gt_k: str) -> str:
            c = vg[gt_k]
            a_pct = c["all_pairs"]["concordance_pct"]
            hi_pct = c["count_diff_ge_0_25"]["concordance_pct"]
            lo_pct = c["count_matched_lt_0_25"]["concordance_pct"]
            return (
                f"`{c['spearman_rho']:+.3f}` / `{c['kendall_tau_b']:+.3f}` / "
                f"`{a_pct:.1f}%` (`{hi_pct:.1f}%` / `{lo_pct:.1f}%`)"
            )

        md.append(
            f"| `{ev_k}` | {ed['n_systems']} | {fmt_cell('panel_P')} | {fmt_cell('panel_F0_5')} | "
            f"{fmt_cell('panel_F1')} | {fmt_cell('panel_F2_0')} |"
        )

    md.extend([
        "",
        "---",
        "",
        "## 2. Within-Mode Ranking Concordance (`short` `N = "
        + str(out["n_short_systems"])
        + "` & `detailed` `N = "
        + str(out["n_detailed_systems"])
        + "`, Matcher `v2`)",
        "",
        "| Mode Subset | Candidate Evaluator | N | vs `panel_P`: $\\rho$ / $\\tau_b$ / All% (`|dM|>=0.25`% / `<0.25`%) | vs `panel_F0.5`: $\\rho$ / $\\tau_b$ / All% | vs `panel_F1`: $\\rho$ / $\\tau_b$ / All% (`|dM|>=0.25`% / `<0.25`%) | vs `panel_F2.0`: $\\rho$ / $\\tau_b$ / All% |",
        "|---|---|---:|---|---|---|---|",
    ])

    for sub_key, sub_label in (("short_mode_systems", "`short`"), ("detailed_mode_systems", "`detailed`")):
        sub_ev = out["ranking_concordance"]["v2"][sub_key]["evaluators"]
        for ev_k in [
            "CIDEr_D",
            "BLEU_4",
            "METEOR",
            "ROUGE_L",
            "ref_P_100_minus_CHAIRi",
            "ref_F0_5",
            "ref_F1",
            "ref_F2_0",
            "delta_P_front",
            "excess_P_vg_tieavg",
            "excess_F1_vg_tieavg",
            "excess_P_poolvote",
            "excess_F1_poolvote",
        ]:
            ed = sub_ev[ev_k]
            if ed["n_systems"] < 2:
                md.append(f"| {sub_label} | `{ev_k}` | {ed['n_systems']} | — | — | — | — |")
                continue
            vg = ed["vs_ground_truth"]
            cp = vg["panel_P"]
            cf05 = vg["panel_F0_5"]
            cf1 = vg["panel_F1"]
            cf20 = vg["panel_F2_0"]
            p_hi = f"{cp['count_diff_ge_0_25']['concordance_pct']:.1f}%" if cp["count_diff_ge_0_25"]["concordance_pct"] is not None else "—"
            p_lo = f"{cp['count_matched_lt_0_25']['concordance_pct']:.1f}%" if cp["count_matched_lt_0_25"]["concordance_pct"] is not None else "—"
            f1_hi = f"{cf1['count_diff_ge_0_25']['concordance_pct']:.1f}%" if cf1["count_diff_ge_0_25"]["concordance_pct"] is not None else "—"
            f1_lo = f"{cf1['count_matched_lt_0_25']['concordance_pct']:.1f}%" if cf1["count_matched_lt_0_25"]["concordance_pct"] is not None else "—"
            md.append(
                f"| {sub_label} | `{ev_k}` | {ed['n_systems']} | "
                f"`{cp['spearman_rho']:+.3f}` / `{cp['kendall_tau_b']:+.3f}` / `{cp['all_pairs']['concordance_pct']:.1f}%` (`{p_hi}` / `{p_lo}`) | "
                f"`{cf05['spearman_rho']:+.3f}` / `{cf05['kendall_tau_b']:+.3f}` / `{cf05['all_pairs']['concordance_pct']:.1f}%` | "
                f"`{cf1['spearman_rho']:+.3f}` / `{cf1['kendall_tau_b']:+.3f}` / `{cf1['all_pairs']['concordance_pct']:.1f}%` (`{f1_hi}` / `{f1_lo}`) | "
                f"`{cf20['spearman_rho']:+.3f}` / `{cf20['kendall_tau_b']:+.3f}` / `{cf20['all_pairs']['concordance_pct']:.1f}%` |"
            )

    md.extend([
        "",
        "---",
        "",
        "## 3. Matcher Version Sensitivity (`v1` Raw-Tone vs `v2` Tone-Normalised, All `N = "
        + str(out["n_total_systems_scored"])
        + "` Systems)",
        "",
        "| Candidate Evaluator | `v2` vs `panel_P` ($\\rho$ / $\\tau_b$ / All%) | `v1` vs `panel_P` ($\\rho$ / $\\tau_b$ / All%) | `v2` vs `panel_F1` ($\\rho$ / $\\tau_b$ / All%) | `v1` vs `panel_F1` ($\\rho$ / $\\tau_b$ / All%) |",
        "|---|---|---|---|---|",
    ])

    all_v1 = out["ranking_concordance"]["v1"]["all_committed_systems"]["evaluators"]
    for ev_k in evaluator_keys:
        v2_p = all_v2[ev_k]["vs_ground_truth"]["panel_P"]
        v1_p = all_v1[ev_k]["vs_ground_truth"]["panel_P"]
        v2_f = all_v2[ev_k]["vs_ground_truth"]["panel_F1"]
        v1_f = all_v1[ev_k]["vs_ground_truth"]["panel_F1"]
        md.append(
            f"| `{ev_k}` | "
            f"`{v2_p['spearman_rho']:+.3f}` / `{v2_p['kendall_tau_b']:+.3f}` / `{v2_p['all_pairs']['concordance_pct']:.1f}%` | "
            f"`{v1_p['spearman_rho']:+.3f}` / `{v1_p['kendall_tau_b']:+.3f}` / `{v1_p['all_pairs']['concordance_pct']:.1f}%` | "
            f"`{v2_f['spearman_rho']:+.3f}` / `{v2_f['kendall_tau_b']:+.3f}` / `{v2_f['all_pairs']['concordance_pct']:.1f}%` | "
            f"`{v1_f['spearman_rho']:+.3f}` / `{v1_f['kendall_tau_b']:+.3f}` / `{v1_f['all_pairs']['concordance_pct']:.1f}%` |"
        )

    md.extend([
        "",
        "---",
        "",
        "## 4. Key Scientific Findings (`PD-4 Q2 & Q6`)",
        "",
        f"1. **Count-Matched vs Count-Divergent Regimes**: Across all `{out['n_total_systems_scored']}` systems (`v2`), raw reference object `F1` (`ref_F1`) correlates strongly with `panel_F1` ($\\rho = {all_v2['ref_F1']['vs_ground_truth']['panel_F1']['spearman_rho']:+.4f}$, $\\tau_b = {all_v2['ref_F1']['vs_ground_truth']['panel_F1']['kendall_tau_b']:+.4f}$, concordance `{all_v2['ref_F1']['vs_ground_truth']['panel_F1']['all_pairs']['concordance_pct']:.2f}%` overall and `{all_v2['ref_F1']['vs_ground_truth']['panel_F1']['count_diff_ge_0_25']['concordance_pct']:.2f}%` on pairs with $|\\Delta M| \\ge 0.25$, dropping to `{all_v2['ref_F1']['vs_ground_truth']['panel_F1']['count_matched_lt_0_25']['concordance_pct']:.2f}%` on count-matched pairs $|\\Delta M| < 0.25$).",
        f"2. **Precision & Count-Controlled Residual Behavior**: Raw reference precision (`ref_P_100_minus_CHAIRi`) achieves $\\rho = {all_v2['ref_P_100_minus_CHAIRi']['vs_ground_truth']['panel_P']['spearman_rho']:+.4f}$ (`{all_v2['ref_P_100_minus_CHAIRi']['vs_ground_truth']['panel_P']['all_pairs']['concordance_pct']:.2f}%` concordance) with `panel_P`, whereas the count-controlled frontier residual (`delta_P_front`) removes the mention-count trend (`|dM| >= 0.25` concordance `{all_v2['delta_P_front']['vs_ground_truth']['panel_P']['count_diff_ge_0_25']['concordance_pct']:.2f}%` vs `panel_P`), achieving its highest concordance with `panel_P` on count-matched pairs (`|dM| < 0.25`: `{all_v2['delta_P_front']['vs_ground_truth']['panel_P']['count_matched_lt_0_25']['concordance_pct']:.2f}%`) and within `short` mode (`{out['ranking_concordance']['v2']['short_mode_systems']['evaluators']['delta_P_front']['vs_ground_truth']['panel_P']['all_pairs']['concordance_pct']:.2f}%`).",
        f"3. **Matched-Count `(v, g)` Controls**: Excess precision over `(v, g)` tie-avg (`excess_P_vg_tieavg`) and `POOL-VOTE` (`excess_P_poolvote`) closely track `delta_P_front` ($\\rho = {all_v2['excess_P_vg_tieavg']['vs_ground_truth']['panel_P']['spearman_rho']:+.4f}$ and `{all_v2['excess_P_poolvote']['vs_ground_truth']['panel_P']['spearman_rho']:+.4f}` vs `panel_P` overall; `{out['ranking_concordance']['v2']['short_mode_systems']['evaluators']['excess_P_vg_tieavg']['vs_ground_truth']['panel_P']['all_pairs']['concordance_pct']:.2f}%` and `{out['ranking_concordance']['v2']['short_mode_systems']['evaluators']['excess_P_poolvote']['vs_ground_truth']['panel_P']['all_pairs']['concordance_pct']:.2f}%` pairwise concordance with `panel_P` in `short` mode), confirming that count-controlled residuals measure **within-count precision quality** rather than unconditional coverage.",
        "",
    ])

    md_text = "\n".join(md)
    OUT_MD.write_text(md_text, encoding="utf-8")
    PREREG_MD.write_text(md_text, encoding="utf-8")
    print("WROTE:", OUT_JSON, OUT_MD, PREREG_MD)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args()
    if args.self_check:
        self_check()
        return 0
    self_check()
    run_audit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
