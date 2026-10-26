#!/usr/bin/env python3
"""Deterministic Decision Engine for DrivingVQA Pilot P1, P2, P3 (CC-104 F1-F4, F7, F9-F12, R4, R5; W7).

Reads `ledger.jsonl` (from `score.py`) and `gpu_seconds.tsv` (from `job.sh`), applies the pre-specified
decision rules and stop conditions without interim looks, and writes `decide_pilot.json`.

REVIEW_KEN_BATCH8 W7 updates:
  - All threshold comparisons (5.0 shortcut, 3.0 P1 SESOI, 0.0 CI lower bounds, 10.0 P3 gap, 0.50 P2 recovery,
    0.10 unparseable stop, 0.20 empty caption stop) are evaluated on UNROUNDED floating-point values before
    rounding to 2 or 4 decimals for JSON display.
  - Every return branch (`INCOMPLETE`, `JOB_STOP_UNPARSEABLE`, `JOB_STOP_EMPTY_CAPTIONS`, and `COMPLETE`)
    includes the `"cells"` summary table and `"k_ge_1_descriptive_check"` (`F9`).

v4 (PI-1026c): P1, P2 and P3 are all evaluated on train3142 (n = 3,142) with one (10000, 3142) index matrix;
P3 compares P1-Full and P3-SelfCap on the same 3,142 items. Rules and thresholds are unchanged.

Usage:
  python3 scripts/ken_dvqa_pilot/decide.py --selftest
  python3 scripts/ken_dvqa_pilot/decide.py --ledger .session_backup/2026-10-26/dvqa_pilot/ledger.jsonl --gpu-seconds .session_backup/2026-10-26/dvqa_pilot/gpu_seconds.tsv --out .session_backup/2026-10-26/dvqa_pilot/decide_pilot.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score as SC  # noqa: E402


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def paired_contrast_raw_and_display(
    vec_a: list[float] | np.ndarray,
    vec_b: list[float] | np.ndarray,
    boot_idx: np.ndarray,
) -> tuple[dict[str, float], dict[str, float]]:
    """Return (display_dict_rounded_2dp, raw_dict_unrounded) so decisions compare unrounded floats (W7)."""
    a = np.asarray(vec_a, dtype=np.float64)
    b = np.asarray(vec_b, dtype=np.float64)
    diff = a - b
    point = float(np.mean(diff))
    boot_means = np.mean(diff[boot_idx], axis=1)
    lo, hi = np.percentile(boot_means, [2.5, 97.5])
    display = {
        "delta": round(point, 2),
        "ci_lo": round(float(lo), 2),
        "ci_hi": round(float(hi), 2),
    }
    raw = {
        "delta": point,
        "ci_lo": float(lo),
        "ci_hi": float(hi),
    }
    return display, raw


def pooled_vec(cell_qwen: dict, cell_iv3: dict, key: str) -> np.ndarray:
    vq = np.asarray(cell_qwen[key], dtype=np.float64)
    vi = np.asarray(cell_iv3[key], dtype=np.float64)
    return 0.5 * (vq + vi)


def parse_gpu_seconds_tsv(path: Path | None) -> dict:
    if path is None or not path.is_file():
        return {"steps": [], "total_gpu_seconds": 0, "total_gpu_hours": 0.0, "timeout_hit": False}
    steps: list[dict] = []
    total_sec = 0
    timeout_hit = False
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t") if "\t" in line else line.split()
        step_name = parts[0]
        sec = int(parts[1]) if len(parts) >= 2 and parts[1].lstrip("-").isdigit() else 0
        status = parts[2] if len(parts) >= 3 else "OK"
        if status.upper() in ("TIMEOUT", "CAP_STOP", "INCOMPLETE"):
            timeout_hit = True
        total_sec += max(0, sec)
        steps.append({"step": step_name, "gpu_seconds": sec, "status": status})
    return {
        "steps": steps,
        "total_gpu_seconds": int(total_sec),
        "total_gpu_hours": round(total_sec / 3600.0, 4),
        "timeout_hit": timeout_hit,
    }


def build_cell_table_and_k1_check(cells: dict[str, dict]) -> tuple[dict[str, dict], dict]:
    """Build the F9 per-cell summary table and K >= 1 descriptive check across all available cells (even on STOP/INCOMPLETE)."""
    cell_table: dict[str, dict] = {}
    for k, v in sorted(cells.items()):
        cell_table[k] = {
            "arm": v["arm"],
            "model": v["model"],
            "set": v["set"],
            "n_samples": v["n_samples"],
            "complete": bool(v.get("complete", False)),
            "exam": v["exam"],
            "f1": v["f1"],
            "unparseable_count": v["unparseable_count"],
            "unparseable_rate": v["unparseable_rate"],
            "empty_caption_count": v.get("empty_caption_count", 0),
            "empty_caption_rate": v.get("empty_caption_rate", 0.0),
        }

    k1_check: dict = {}
    req_k1 = ("P1-Full__qwen25vl_7b", "P1-Full__internvl3_8b", "P1-Oracle__qwen25vl_7b", "P1-Oracle__internvl3_8b")
    if all(c in cells and "k_ge_1_subset" in cells[c] for c in req_k1):
        p1_full_q = cells["P1-Full__qwen25vl_7b"]
        p1_full_i = cells["P1-Full__internvl3_8b"]
        p1_ora_q = cells["P1-Oracle__qwen25vl_7b"]
        p1_ora_i = cells["P1-Oracle__internvl3_8b"]
        n_k1 = int(p1_full_q["k_ge_1_subset"]["n_samples"])
        boot_k1 = SC.make_bootstrap_matrix(n_k1, SC.BOOTSTRAP_B, SC.BOOTSTRAP_SEED)
        k1_full_pool = 0.5 * (
            np.asarray(p1_full_q["k_ge_1_subset"]["exam_vec"], dtype=np.float64)
            + np.asarray(p1_full_i["k_ge_1_subset"]["exam_vec"], dtype=np.float64)
        )
        k1_ora_pool = 0.5 * (
            np.asarray(p1_ora_q["k_ge_1_subset"]["exam_vec"], dtype=np.float64)
            + np.asarray(p1_ora_i["k_ge_1_subset"]["exam_vec"], dtype=np.float64)
        )
        k1_disp, _ = paired_contrast_raw_and_display(k1_ora_pool, k1_full_pool, boot_k1)
        k1_check = {
            "n_samples_k_ge_1": n_k1,
            "role": "DESCRIPTIVE_ONLY_DECIDES_NOTHING",
            "pooled_oracle_vs_full_exam": k1_disp,
        }
    return cell_table, k1_check


def evaluate_decision_from_cells(
    cells: dict[str, dict],
    gpu_info: dict,
    ledger_sha256: str | None = None,
    stage: str = "A",
) -> dict:
    boot_all = SC.make_bootstrap_matrix(SC.N_ITEMS, SC.BOOTSTRAP_B, SC.BOOTSTRAP_SEED)

    # Always build cell_table and k_ge_1_descriptive_check first so every branch includes them (F9, W7)
    cell_table, k1_check = build_cell_table_and_k1_check(cells)

    # 1. Check timeout / cap stop first (CC-104 F3)
    if gpu_info.get("timeout_hit", False):
        return {
            "schema": "vsps.ken_dvqa_decide_pilot.v2",
            "label": "EXPLORATORY",
            "ruling_authority": "CC-104 (F1-F12) & REVIEW_KEN_BATCH8 (W7)",
            "status": "INCOMPLETE",
            "stop_reason": "GPU_TIMEOUT_CAP_REACHED",
            "P1_verdict": None,
            "P2_verdict": None,
            "P3_verdict": None,
            "k_ge_1_descriptive_check": k1_check,
            "cells": cell_table,
            "ledger_sha256": ledger_sha256,
            "gpu_budget": gpu_info,
        }

    required_stage_a = [f"{arm}__{m}" for arm in SC.STAGE_A_ARMS for m in SC.MODELS]
    missing_stage_a = [c for c in required_stage_a if c not in cells or not cells[c].get("complete", False)]
    if missing_stage_a:
        return {
            "schema": "vsps.ken_dvqa_decide_pilot.v2",
            "label": "EXPLORATORY",
            "ruling_authority": "CC-104 (F1-F12) & REVIEW_KEN_BATCH8 (W7)",
            "status": "INCOMPLETE",
            "stop_reason": f"MISSING_OR_INCOMPLETE_CELLS:{missing_stage_a}",
            "P1_verdict": None,
            "P2_verdict": None,
            "P3_verdict": None,
            "k_ge_1_descriptive_check": k1_check,
            "cells": cell_table,
            "ledger_sha256": ledger_sha256,
            "gpu_budget": gpu_info,
        }

    # 2. Check >10% unparseable stop and >20% empty caption stop using unrounded counts/n_samples (CC-104 F1, F2, F12; W7)
    unparseable_violations = [
        k for k, v in sorted(cells.items())
        if (float(v.get("unparseable_count", 0)) / float(max(1, v.get("n_samples", 1)))) > 0.10
    ]
    if unparseable_violations:
        return {
            "schema": "vsps.ken_dvqa_decide_pilot.v2",
            "label": "EXPLORATORY",
            "ruling_authority": "CC-104 (F1-F12) & REVIEW_KEN_BATCH8 (W7)",
            "status": "JOB_STOP_UNPARSEABLE",
            "stop_reason": f"UNPARSEABLE_RATE_GT_10PCT:{unparseable_violations}",
            "P1_verdict": None,
            "P2_verdict": None,
            "P3_verdict": None,
            "k_ge_1_descriptive_check": k1_check,
            "cells": cell_table,
            "ledger_sha256": ledger_sha256,
            "gpu_budget": gpu_info,
        }

    empty_cap_violations = [
        k for k, v in sorted(cells.items())
        if v.get("arm") == "P3-SelfCap"
        and (float(v.get("empty_caption_count", 0)) / float(max(1, v.get("n_samples", 1)))) > 0.20
    ]
    if empty_cap_violations:
        return {
            "schema": "vsps.ken_dvqa_decide_pilot.v2",
            "label": "EXPLORATORY",
            "ruling_authority": "CC-104 (F1-F12) & REVIEW_KEN_BATCH8 (W7)",
            "status": "JOB_STOP_EMPTY_CAPTIONS",
            "stop_reason": f"EMPTY_CAPTION_RATE_GT_20PCT:{empty_cap_violations}",
            "P1_verdict": None,
            "P2_verdict": None,
            "P3_verdict": None,
            "k_ge_1_descriptive_check": k1_check,
            "cells": cell_table,
            "ledger_sha256": ledger_sha256,
            "gpu_budget": gpu_info,
        }

    # 3. Evaluate P1 on train3142 (n=3142) using unrounded floats for all threshold comparisons (W7)
    p1_blind_q = cells["P1-Blind__qwen25vl_7b"]
    p1_blind_i = cells["P1-Blind__internvl3_8b"]
    p1_full_q = cells["P1-Full__qwen25vl_7b"]
    p1_full_i = cells["P1-Full__internvl3_8b"]
    p1_ora_q = cells["P1-Oracle__qwen25vl_7b"]
    p1_ora_i = cells["P1-Oracle__internvl3_8b"]

    blind_pool_exam = pooled_vec(p1_blind_q, p1_blind_i, "exam_vec")
    full_pool_exam = pooled_vec(p1_full_q, p1_full_i, "exam_vec")
    ora_pool_exam = pooled_vec(p1_ora_q, p1_ora_i, "exam_vec")
    full_pool_f1 = pooled_vec(p1_full_q, p1_full_i, "f1_vec")
    ora_pool_f1 = pooled_vec(p1_ora_q, p1_ora_i, "f1_vec")

    p1_ora_vs_full_pool_exam, p1_ora_vs_full_pool_exam_raw = paired_contrast_raw_and_display(
        ora_pool_exam, full_pool_exam, boot_all
    )
    p1_ora_vs_full_pool_f1, _ = paired_contrast_raw_and_display(ora_pool_f1, full_pool_f1, boot_all)
    p1_ora_vs_full_q_exam, _ = paired_contrast_raw_and_display(p1_ora_q["exam_vec"], p1_full_q["exam_vec"], boot_all)
    p1_ora_vs_full_i_exam, _ = paired_contrast_raw_and_display(p1_ora_i["exam_vec"], p1_full_i["exam_vec"], boot_all)

    full_minus_blind_pool = float(np.mean(full_pool_exam - blind_pool_exam))
    full_minus_blind_q = float(np.mean(np.asarray(p1_full_q["exam_vec"]) - np.asarray(p1_blind_q["exam_vec"])))
    full_minus_blind_i = float(np.mean(np.asarray(p1_full_i["exam_vec"]) - np.asarray(p1_blind_i["exam_vec"])))
    shortcut_stop = bool(
        full_minus_blind_pool <= 5.0 or full_minus_blind_q <= 5.0 or full_minus_blind_i <= 5.0
    )

    if shortcut_stop:
        p1_verdict = "STOP"
        p1_reason = "SHORTCUT_FAILURE_BLIND_WITHIN_5PTS_OF_FULL"
    elif p1_ora_vs_full_pool_exam_raw["delta"] >= 3.0 and p1_ora_vs_full_pool_exam_raw["ci_lo"] > 0.0:
        p1_verdict = "GO"
        p1_reason = "POOLED_ORACLE_GAIN_GE_3PTS_AND_CI_LO_GT_0"
    else:
        p1_verdict = "STOP"
        p1_reason = "POOLED_ORACLE_GAIN_BELOW_3PTS_OR_CI_INCLUDES_0"

    # 4. Evaluate P3 on train3142 (n=3142, same items as P1-Full) using unrounded floats
    p3_cap_q = cells["P3-SelfCap__qwen25vl_7b"]
    p3_cap_i = cells["P3-SelfCap__internvl3_8b"]

    p3_q_exam_diff, p3_q_exam_raw = paired_contrast_raw_and_display(p1_full_q["exam_vec"], p3_cap_q["exam_vec"], boot_all)
    p3_i_exam_diff, p3_i_exam_raw = paired_contrast_raw_and_display(p1_full_i["exam_vec"], p3_cap_i["exam_vec"], boot_all)
    p3_q_f1_diff, _ = paired_contrast_raw_and_display(p1_full_q["f1_vec"], p3_cap_q["f1_vec"], boot_all)
    p3_i_f1_diff, _ = paired_contrast_raw_and_display(p1_full_i["f1_vec"], p3_cap_i["f1_vec"], boot_all)

    p3_pool_cap_exam = pooled_vec(p3_cap_q, p3_cap_i, "exam_vec")
    p3_pool_exam_diff, _ = paired_contrast_raw_and_display(full_pool_exam, p3_pool_cap_exam, boot_all)

    p3_q_ok = p3_q_exam_raw["delta"] >= 10.0 and p3_q_exam_raw["ci_lo"] > 0.0
    p3_i_ok = p3_i_exam_raw["delta"] >= 10.0 and p3_i_exam_raw["ci_lo"] > 0.0
    p3_verdict = "GO" if (p3_q_ok and p3_i_ok) else "STOP"

    # 5. Evaluate P2 on train3142 (n=3142) ONLY if P1_verdict == "GO"
    p2_summary: dict = {}
    if p1_verdict != "GO":
        p2_verdict = "CANCELLED_P1_STOP"
        p2_summary = {
            "verdict": p2_verdict,
            "reason": "P1_STOP_ZERO_GPU_SPENT_ON_P2",
        }
    else:
        required_stage_b = [f"{arm}__{m}" for arm in SC.STAGE_B_ARMS for m in SC.MODELS]
        missing_stage_b = [c for c in required_stage_b if c not in cells or not cells[c].get("complete", False)]
        if missing_stage_b:
            p2_verdict = "PENDING_STAGE_B" if stage == "A" else "INCOMPLETE_STAGE_B"
            p2_summary = {
                "verdict": p2_verdict,
                "missing_stage_b_cells": missing_stage_b,
            }
        else:
            p2_grid_q = cells["P2-Grid__qwen25vl_7b"]
            p2_grid_i = cells["P2-Grid__internvl3_8b"]
            p2_att_q = cells["P2-AttCrop__qwen25vl_7b"]
            p2_att_i = cells["P2-AttCrop__internvl3_8b"]

            grid_pool_exam = pooled_vec(p2_grid_q, p2_grid_i, "exam_vec")
            att_pool_exam = pooled_vec(p2_att_q, p2_att_i, "exam_vec")
            grid_pool_f1 = pooled_vec(p2_grid_q, p2_grid_i, "f1_vec")
            att_pool_f1 = pooled_vec(p2_att_q, p2_att_i, "f1_vec")

            p2_att_vs_grid_pool_exam, p2_att_vs_grid_pool_exam_raw = paired_contrast_raw_and_display(
                att_pool_exam, grid_pool_exam, boot_all
            )
            p2_att_vs_grid_pool_f1, _ = paired_contrast_raw_and_display(att_pool_f1, grid_pool_f1, boot_all)
            p2_att_vs_grid_q_exam, _ = paired_contrast_raw_and_display(p2_att_q["exam_vec"], p2_grid_q["exam_vec"], boot_all)
            p2_att_vs_grid_i_exam, _ = paired_contrast_raw_and_display(p2_att_i["exam_vec"], p2_grid_i["exam_vec"], boot_all)

            oracle_gap = float(np.mean(ora_pool_exam - full_pool_exam))
            att_gain = float(np.mean(att_pool_exam - full_pool_exam))
            recovery_ratio_raw = (att_gain / oracle_gap) if oracle_gap > 0.0 else 0.0
            recovery_ratio_disp = round(recovery_ratio_raw, 4)

            if p2_att_vs_grid_pool_exam_raw["ci_lo"] > 0.0 and recovery_ratio_raw >= 0.50:
                p2_verdict = "GO"
                p2_reason = "POOLED_ATT_VS_GRID_CI_LO_GT_0_AND_RECOVERY_GE_50PCT"
            else:
                p2_verdict = "STOP"
                p2_reason = "POOLED_ATT_VS_GRID_CI_INCLUDES_0_OR_RECOVERY_LT_50PCT"

            p2_summary = {
                "verdict": p2_verdict,
                "reason": p2_reason,
                "n_samples": SC.N_ITEMS,
                "pooled_att_vs_grid_exam": p2_att_vs_grid_pool_exam,
                "pooled_att_vs_grid_f1": p2_att_vs_grid_pool_f1,
                "qwen25vl_7b_att_vs_grid_exam": p2_att_vs_grid_q_exam,
                "internvl3_8b_att_vs_grid_exam": p2_att_vs_grid_i_exam,
                "pooled_oracle_recovery_ratio": recovery_ratio_disp,
            }

    return {
        "schema": "vsps.ken_dvqa_decide_pilot.v2",
        "label": "EXPLORATORY",
        "ruling_authority": "CC-104 (F1-F12) & REVIEW_KEN_BATCH8 (W7)",
        "status": "COMPLETE",
        "P1_verdict": p1_verdict,
        "P2_verdict": p2_verdict,
        "P3_verdict": p3_verdict,
        "P1_oracle_crop_gap": {
            "verdict": p1_verdict,
            "reason": p1_reason,
            "sesoi_anchor_note": "Anchored on Table 3 fine-tuned oracle-vs-predicted gain (62.0 vs 58.7 = +3.3 pts) in 2501.04671 (CC-104 F7)",
            "n_samples": SC.N_ITEMS,
            "pooled_oracle_vs_full_exam": p1_ora_vs_full_pool_exam,
            "pooled_oracle_vs_full_f1": p1_ora_vs_full_pool_f1,
            "qwen25vl_7b_oracle_vs_full_exam": p1_ora_vs_full_q_exam,
            "internvl3_8b_oracle_vs_full_exam": p1_ora_vs_full_i_exam,
            "shortcut_check_full_minus_blind_pts": {
                "pooled": round(full_minus_blind_pool, 2),
                "qwen25vl_7b": round(full_minus_blind_q, 2),
                "internvl3_8b": round(full_minus_blind_i, 2),
                "shortcut_stop_triggered": shortcut_stop,
            },
            "k_ge_1_descriptive_check": k1_check,
        },
        "P2_training_free_attention_crops": p2_summary,
        "P3_caption_bottleneck": {
            "verdict": p3_verdict,
            "n_samples": SC.N_ITEMS,
            "pooled_full_minus_selfcap_exam": p3_pool_exam_diff,
            "qwen25vl_7b_full_minus_selfcap_exam": p3_q_exam_diff,
            "qwen25vl_7b_full_minus_selfcap_f1": p3_q_f1_diff,
            "internvl3_8b_full_minus_selfcap_exam": p3_i_exam_diff,
            "internvl3_8b_full_minus_selfcap_f1": p3_i_f1_diff,
            "both_backbones_ge_10pts_and_ci_lo_gt_0": bool(p3_q_ok and p3_i_ok),
        },
        "k_ge_1_descriptive_check": k1_check,
        "cells": cell_table,
        "ledger_sha256": ledger_sha256,
        "gpu_budget": gpu_info,
    }


def make_synthetic_cell(arm: str, model: str, exam_vec: np.ndarray, unparseable_rate: float = 0.0, empty_cap_rate: float = 0.0) -> dict:
    n = len(exam_vec)
    boot = SC.make_bootstrap_matrix(n, SC.BOOTSTRAP_B, SC.BOOTSTRAP_SEED)
    res = {
        "cell": f"{arm}__{model}",
        "arm": arm,
        "model": model,
        "set": "train3142",
        "n_samples": n,
        "complete": True,
        "unparseable_count": int(round(unparseable_rate * n)),
        "unparseable_rate": unparseable_rate,
        "empty_caption_count": int(round(empty_cap_rate * n)),
        "empty_caption_rate": empty_cap_rate,
        "exam": SC.bootstrap_mean_ci(exam_vec, boot),
        "f1": SC.bootstrap_mean_ci(exam_vec, boot),
        "exam_vec": exam_vec.tolist(),
        "f1_vec": exam_vec.tolist(),
    }
    if arm in ("P1-Blind", "P1-Full", "P1-Oracle"):
        n_k1 = 3050  # train3142 items with K >= 1 (dvqa_train_descriptive_stats_v2.json :: subsets.train_all_3142)
        boot_k1 = SC.make_bootstrap_matrix(n_k1, SC.BOOTSTRAP_B, SC.BOOTSTRAP_SEED)
        sub_k1 = exam_vec[:n_k1]
        res["k_ge_1_subset"] = {
            "n_samples": n_k1,
            "exam": SC.bootstrap_mean_ci(sub_k1, boot_k1),
            "f1": SC.bootstrap_mean_ci(sub_k1, boot_k1),
            "exam_vec": sub_k1.tolist(),
            "f1_vec": sub_k1.tolist(),
        }
    return res


def selftest() -> None:
    rng = np.random.default_rng(123)
    gpu_ok = {"steps": [{"step": "P1", "gpu_seconds": 3100, "status": "OK"}], "total_gpu_seconds": 3100, "total_gpu_hours": 0.8611, "timeout_hit": False}

    # Build deterministic binary outcome vectors (0 or 100) for N=3142 (every arm on train3142)
    n = SC.N_ITEMS
    base_full = (rng.random(n) < 0.50).astype(np.float64) * 100.0
    base_blind = (rng.random(n) < 0.25).astype(np.float64) * 100.0
    ora_vec = np.where((base_full == 0.0) & (rng.random(n) < 0.14), 100.0, base_full)
    grid_vec = np.where((base_full == 0.0) & (rng.random(n) < 0.04), 100.0, base_full)
    att_vec = np.where((ora_vec == 100.0) & (base_full == 0.0) & (rng.random(n) < 0.85), 100.0, grid_vec)
    cap_vec = np.where((base_full == 100.0) & (rng.random(n) < 0.35), 0.0, base_full)

    cells_go = {}
    for m in SC.MODELS:
        cells_go[f"P1-Blind__{m}"] = make_synthetic_cell("P1-Blind", m, base_blind)
        cells_go[f"P1-Full__{m}"] = make_synthetic_cell("P1-Full", m, base_full)
        cells_go[f"P1-Oracle__{m}"] = make_synthetic_cell("P1-Oracle", m, ora_vec)
        cells_go[f"P3-SelfCap__{m}"] = make_synthetic_cell("P3-SelfCap", m, cap_vec)
        cells_go[f"P2-Grid__{m}"] = make_synthetic_cell("P2-Grid", m, grid_vec)
        cells_go[f"P2-AttCrop__{m}"] = make_synthetic_cell("P2-AttCrop", m, att_vec)

    # 1. Synthetic all-GO check
    d_go = evaluate_decision_from_cells(cells_go, gpu_ok, ledger_sha256="0" * 64, stage="B")
    assert d_go["status"] == "COMPLETE"
    assert d_go["P1_verdict"] == "GO"
    assert d_go["P2_verdict"] == "GO"
    assert d_go["P3_verdict"] == "GO"
    assert len(d_go["cells"]) == 12

    # 2. Synthetic P1 STOP check (Oracle == Full -> +0.0 gain -> P1 STOP and P2 CANCELLED_P1_STOP)
    cells_p1_stop = dict(cells_go)
    for m in SC.MODELS:
        cells_p1_stop[f"P1-Oracle__{m}"] = make_synthetic_cell("P1-Oracle", m, base_full)
    d_p1_stop = evaluate_decision_from_cells(cells_p1_stop, gpu_ok, ledger_sha256="0" * 64, stage="A")
    assert d_p1_stop["P1_verdict"] == "STOP"
    assert d_p1_stop["P2_verdict"] == "CANCELLED_P1_STOP"
    assert len(d_p1_stop["cells"]) == 12

    # 3. Synthetic Shortcut Failure STOP check (Blind == Full)
    cells_shortcut = dict(cells_go)
    cells_shortcut["P1-Blind__qwen25vl_7b"] = make_synthetic_cell("P1-Blind", "qwen25vl_7b", base_full)
    d_sc = evaluate_decision_from_cells(cells_shortcut, gpu_ok, ledger_sha256="0" * 64, stage="A")
    assert d_sc["P1_verdict"] == "STOP" and "SHORTCUT" in d_sc["P1_oracle_crop_gap"]["reason"]
    assert len(d_sc["cells"]) == 12

    # 4. Synthetic >10% unparseable rate -> JOB_STOP_UNPARSEABLE with no verdict, still includes cells (W7 / F9)
    cells_unp = dict(cells_go)
    cells_unp["P1-Full__internvl3_8b"] = make_synthetic_cell("P1-Full", "internvl3_8b", base_full, unparseable_rate=0.12)
    d_unp = evaluate_decision_from_cells(cells_unp, gpu_ok, ledger_sha256="0" * 64, stage="A")
    assert d_unp["status"] == "JOB_STOP_UNPARSEABLE" and d_unp["P1_verdict"] is None
    assert "cells" in d_unp and len(d_unp["cells"]) == 12 and "k_ge_1_descriptive_check" in d_unp

    # 5. Synthetic >20% empty captions -> JOB_STOP_EMPTY_CAPTIONS with no verdict, still includes cells (W7 / F9)
    cells_empty_cap = dict(cells_go)
    cells_empty_cap["P3-SelfCap__qwen25vl_7b"] = make_synthetic_cell("P3-SelfCap", "qwen25vl_7b", cap_vec, empty_cap_rate=0.25)
    d_ec = evaluate_decision_from_cells(cells_empty_cap, gpu_ok, ledger_sha256="0" * 64, stage="A")
    assert d_ec["status"] == "JOB_STOP_EMPTY_CAPTIONS" and d_ec["P3_verdict"] is None
    assert "cells" in d_ec and len(d_ec["cells"]) == 12

    # 6. Synthetic timeout cap reached -> INCOMPLETE with no verdict, still includes cells (W7 / F9)
    gpu_timeout = {**gpu_ok, "timeout_hit": True}
    d_to = evaluate_decision_from_cells(cells_go, gpu_timeout, ledger_sha256="0" * 64, stage="A")
    assert d_to["status"] == "INCOMPLETE" and d_to["P1_verdict"] is None
    assert "cells" in d_to and len(d_to["cells"]) == 12

    # 7. W7 unrounded threshold test: raw delta 2.996 rounds to 3.00 for display but is < 3.0 unrounded -> STOP
    cells_edge = dict(cells_go)
    ora_edge = base_full.copy()
    ora_edge[:94] = base_full[:94] + 100.14289361702128  # mean diff = 94 * 100.142893617 / 3142 = 2.996 (< 3.0 unrounded, rounds to 3.00)
    for m in SC.MODELS:
        cells_edge[f"P1-Oracle__{m}"] = make_synthetic_cell("P1-Oracle", m, ora_edge)
    d_edge = evaluate_decision_from_cells(cells_edge, gpu_ok, ledger_sha256="0" * 64, stage="A")
    assert d_edge["P1_oracle_crop_gap"]["pooled_oracle_vs_full_exam"]["delta"] == 3.0
    edge_raw = float(np.mean(ora_edge - base_full))
    assert 2.995 <= edge_raw < 3.0, edge_raw
    assert d_edge["P1_verdict"] == "STOP", "W7 unrounded threshold check failed: 2.996 must not pass >= 3.0"

    print(json.dumps({
        "script": "decide.py",
        "selftest": "OK",
        "go_case_p1_delta": d_go["P1_oracle_crop_gap"]["pooled_oracle_vs_full_exam"]["delta"],
        "go_case_p2_recovery": d_go["P2_training_free_attention_crops"]["pooled_oracle_recovery_ratio"],
        "go_case_p3_qwen_delta": d_go["P3_caption_bottleneck"]["qwen25vl_7b_full_minus_selfcap_exam"]["delta"],
        "checks_passed": 7,
    }, sort_keys=True))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--ledger", type=Path, default=Path(".session_backup/2026-10-26/dvqa_pilot/ledger.jsonl"))
    ap.add_argument("--gpu-seconds", type=Path, default=Path(".session_backup/2026-10-26/dvqa_pilot/gpu_seconds.tsv"))
    ap.add_argument("--stage", choices=["A", "B"], default="A")
    ap.add_argument("--out", type=Path, default=Path(".session_backup/2026-10-26/dvqa_pilot/decide_pilot.json"))
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    if not args.ledger.is_file():
        raise SystemExit(f"REFUSED: missing ledger file {args.ledger}")
    cells: dict[str, dict] = {}
    for line in args.ledger.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        cells[row["cell"]] = row

    gpu_info = parse_gpu_seconds_tsv(args.gpu_seconds)
    decision = evaluate_decision_from_cells(
        cells=cells,
        gpu_info=gpu_info,
        ledger_sha256=sha256_file(args.ledger),
        stage=args.stage,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out_text = json.dumps(decision, indent=2, sort_keys=True) + "\n"
    args.out.write_text(out_text, encoding="utf-8")
    print(out_text, end="")


if __name__ == "__main__":
    main()
