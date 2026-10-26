#!/usr/bin/env python3
"""Deterministic Scorer & Paired Bootstrap Engine for DrivingVQA Pilot P1, P2, P3 (CC-104 F1, F2, F4, F9, F10, R4).

Parser rule (CC-104 F1):
  - Take the last line containing "Answer(s):" (case-insensitive).
  - Extract standalone letters A-D after "Answer(s):" that belong to the sample's `possible_answers` keys.
  - Otherwise, the predicted set is empty (Exam = 0.0, F1 = 0.0) and the item is counted in `unparseable_rate`.

Bootstrap rule (CC-104 F4):
  - B = 10,000 draws with `np.random.default_rng(0)`.
  - One shared index matrix per scored set: shape (10000, 1000) for P1/P2 (`dev1000`) and (10000, 500) for P3 (`dev500`).

Usage:
  python3 scripts/ken_dvqa_pilot/score.py --selftest
  python3 scripts/ken_dvqa_pilot/score.py --runs-dir /root/outputs/dvqa_pilot/runs --dvqa-dir /root/ncs-data/datasets/drivingvqa --ledger /root/outputs/dvqa_pilot/ledger.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = next(
    (p for p in HERE.parents if (p / "manuscript/ken/drivingvqa_dev500_ids.tsv").exists()),
    HERE.parents[2],
)

DEV500_TSV = ROOT / "manuscript/ken/drivingvqa_dev500_ids.tsv"
DEV500_SHA256 = "9896af1186ddd6a5806095ba696851b5aef512079f5d0813cff3f7f4fae9c4ce"
DEV1000_TSV = ROOT / "manuscript/ken/drivingvqa_dev1000_ids.tsv"
DEV1000_SHA256 = "636e04775153ef9cb879a7620d195fcaa7e86894ead73b008c8f95b47e268dec"
TRAIN_JSON_SHA256 = "4a204e3fa7516db313ceeb91ac989919979e31da20e484bc5f4018c268dec"
# Exact train.json sha256 from build_splits_and_stats.py:
TRAIN_JSON_PIN = "4a204e3fa7516db313ceeb91ac989919979e31da20e484bc5f4018c261bd483d"

MODELS = ("qwen25vl_7b", "internvl3_8b")
STAGE_A_ARMS = ("P1-Blind", "P1-Full", "P1-Oracle", "P3-SelfCap")
STAGE_B_ARMS = ("P2-Grid", "P2-AttCrop")
BOOTSTRAP_B = 10000
BOOTSTRAP_SEED = 0

ANSWER_LINE_RE = re.compile(r"answer\(s\)\s*:\s*(.*)$", flags=re.IGNORECASE)
LETTER_TOKEN_RE = re.compile(r"\b([A-D])\b")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest_ids(tsv_path: Path, expected_sha: str, expected_n: int) -> list[str]:
    if not tsv_path.is_file():
        raise SystemExit(f"REFUSED: missing manifest {tsv_path}")
    if sha256_file(tsv_path) != expected_sha:
        raise SystemExit(f"REFUSED: manifest SHA-256 mismatch for {tsv_path}")
    lines = tsv_path.read_text(encoding="utf-8").splitlines()[1:]
    ids = [line.split("\t")[0].strip() for line in lines if line.strip()]
    if len(ids) != expected_n or len(set(ids)) != expected_n:
        raise SystemExit(f"REFUSED: manifest {tsv_path} does not contain {expected_n} unique IDs")
    return ids


def parse_answer_output(raw_output: str, valid_options: set[str] | list[str]) -> tuple[list[str], bool]:
    """CC-104 F1 fixed parser:
    Take the last line containing 'Answer(s):', extract letters A-D within `valid_options`.
    Otherwise return ([], True) where True indicates unparseable (Exam = 0, F1 = 0).
    """
    if not isinstance(raw_output, str) or not raw_output.strip():
        return [], True
    valid_set = {str(o).strip().upper() for o in valid_options}
    matched_rhs: list[str] = []
    for line in raw_output.splitlines():
        m = ANSWER_LINE_RE.search(line)
        if m is not None:
            matched_rhs.append(m.group(1))
    if not matched_rhs:
        return [], True
    last_rhs = matched_rhs[-1].upper()
    letters = sorted({tok for tok in LETTER_TOKEN_RE.findall(last_rhs) if tok in valid_set})
    if not letters:
        return [], True
    return letters, False


def compute_item_exam_f1(pred_letters: list[str] | set[str], true_letters: list[str] | set[str]) -> tuple[float, float]:
    """Corbiere et al. (2025) Sec. 5.1 Exam Score (exact match * 100) and Multi-label F1 (* 100)."""
    p_set = {str(x).strip().upper() for x in pred_letters if str(x).strip()}
    t_set = {str(x).strip().upper() for x in true_letters if str(x).strip()}
    exam = 100.0 if p_set == t_set else 0.0
    if not p_set or not t_set:
        f1 = 0.0
    else:
        f1 = 100.0 * (2.0 * len(p_set & t_set)) / float(len(p_set) + len(t_set))
    return float(exam), float(f1)


def make_bootstrap_matrix(n_items: int, b_draws: int = BOOTSTRAP_B, seed: int = BOOTSTRAP_SEED) -> np.ndarray:
    """CC-104 F4: one shared bootstrap index matrix of shape (B, n_items) from np.random.default_rng(0)."""
    rng = np.random.default_rng(seed)
    return rng.integers(0, n_items, size=(b_draws, n_items), endpoint=False)


def bootstrap_mean_ci(vec: np.ndarray, boot_idx: np.ndarray) -> dict[str, float]:
    v = np.asarray(vec, dtype=np.float64)
    point = float(np.mean(v))
    boot_means = np.mean(v[boot_idx], axis=1)
    lo, hi = np.percentile(boot_means, [2.5, 97.5])
    return {
        "point": round(point, 2),
        "ci_lo": round(float(lo), 2),
        "ci_hi": round(float(hi), 2),
    }


def score_predictions_map(
    preds_by_id: dict[str, dict | str],
    sample_ids: list[str],
    gold_data: dict[str, dict],
    boot_idx: np.ndarray,
    is_p3: bool = False,
) -> dict:
    n = len(sample_ids)
    if boot_idx.shape != (BOOTSTRAP_B, n):
        raise ValueError(f"Bootstrap matrix shape {boot_idx.shape} != ({BOOTSTRAP_B}, {n})")

    exam_vec = np.zeros(n, dtype=np.float64)
    f1_vec = np.zeros(n, dtype=np.float64)
    unparseable_cnt = 0
    empty_caption_cnt = 0
    missing_ids: list[str] = []

    for idx, sid in enumerate(sample_ids):
        if sid not in preds_by_id:
            missing_ids.append(sid)
            unparseable_cnt += 1
            if is_p3:
                empty_caption_cnt += 1
            continue
        rec = preds_by_id[sid]
        raw_out = rec["raw_output"] if isinstance(rec, dict) else str(rec)
        if is_p3:
            cap_str = rec.get("caption", "") if isinstance(rec, dict) else ""
            if not str(cap_str).strip():
                empty_caption_cnt += 1

        gold_item = gold_data[sid]
        valid_opts = set(gold_item["possible_answers"].keys())
        true_ans = gold_item["true_answers"]
        parsed_letters, is_unparseable = parse_answer_output(raw_out, valid_opts)
        if is_unparseable:
            unparseable_cnt += 1
        e_val, f_val = compute_item_exam_f1(parsed_letters, true_ans)
        exam_vec[idx] = e_val
        f1_vec[idx] = f_val

    unparseable_rate = round(unparseable_cnt / float(n), 4)
    empty_caption_rate = round(empty_caption_cnt / float(n), 4) if is_p3 else 0.0

    return {
        "n_samples": n,
        "complete": len(missing_ids) == 0,
        "missing_count": len(missing_ids),
        "unparseable_count": int(unparseable_cnt),
        "unparseable_rate": unparseable_rate,
        "unparseable_stop_triggered": bool(unparseable_rate > 0.10),
        "empty_caption_count": int(empty_caption_cnt) if is_p3 else 0,
        "empty_caption_rate": empty_caption_rate,
        "empty_caption_stop_triggered": bool(is_p3 and empty_caption_rate > 0.20),
        "exam": bootstrap_mean_ci(exam_vec, boot_idx),
        "f1": bootstrap_mean_ci(f1_vec, boot_idx),
        "exam_vec": [round(float(x), 4) for x in exam_vec.tolist()],
        "f1_vec": [round(float(x), 4) for x in f1_vec.tolist()],
    }


def load_run_jsonl(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    out: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        out[str(rec["sample_id"])] = rec
    return out


def score_runs_directory(runs_dir: Path, dvqa_dir: Path, ledger_path: Path) -> dict:
    train_json = dvqa_dir / "train.json"
    if not train_json.is_file() or sha256_file(train_json) != TRAIN_JSON_PIN:
        raise SystemExit(f"REFUSED: missing or unverified train.json at {train_json}")
    gold_data = json.loads(train_json.read_text(encoding="utf-8"))

    dev500_ids = load_manifest_ids(DEV500_TSV, DEV500_SHA256, 500)
    dev1000_ids = load_manifest_ids(DEV1000_TSV, DEV1000_SHA256, 1000)

    boot_1000 = make_bootstrap_matrix(1000, BOOTSTRAP_B, BOOTSTRAP_SEED)
    boot_500 = make_bootstrap_matrix(500, BOOTSTRAP_B, BOOTSTRAP_SEED)

    # K >= 1 subset indices within dev1000 (CC-104 F9 descriptive check)
    k_ge_1_ids = [sid for sid in dev1000_ids if len(gold_data[sid].get("relevant_entities", [])) >= 1]
    boot_k_ge_1 = make_bootstrap_matrix(len(k_ge_1_ids), BOOTSTRAP_B, BOOTSTRAP_SEED)

    ledger_rows: list[dict] = []
    cells: dict[str, dict] = {}

    for arm in STAGE_A_ARMS + STAGE_B_ARMS:
        for model in MODELS:
            run_file = runs_dir / f"{arm}_{model}.preds.jsonl"
            if not run_file.is_file():
                continue
            preds_map = load_run_jsonl(run_file)
            is_p3 = arm == "P3-SelfCap"
            target_ids = dev500_ids if is_p3 else dev1000_ids
            boot_mat = boot_500 if is_p3 else boot_1000

            cell_res = score_predictions_map(preds_map, target_ids, gold_data, boot_mat, is_p3=is_p3)
            cell_key = f"{arm}__{model}"
            rec_row = {
                "cell": cell_key,
                "arm": arm,
                "model": model,
                "set": "dev500" if is_p3 else "dev1000",
                "run_file": run_file.name,
                "run_file_sha256": sha256_file(run_file),
                **cell_res,
            }
            if arm in ("P1-Blind", "P1-Full", "P1-Oracle"):
                # Also score on dev500 (so P3 can compare against P1-Full on the exact same 500 items)
                dev500_sub = score_predictions_map(preds_map, dev500_ids, gold_data, boot_500, is_p3=False)
                rec_row["dev500_subset"] = {
                    "n_samples": 500,
                    "exam": dev500_sub["exam"],
                    "f1": dev500_sub["f1"],
                    "exam_vec": dev500_sub["exam_vec"],
                    "f1_vec": dev500_sub["f1_vec"],
                }
                # Descriptive check on K >= 1 subset (CC-104 F9)
                k1_sub = score_predictions_map(preds_map, k_ge_1_ids, gold_data, boot_k_ge_1, is_p3=False)
                rec_row["k_ge_1_subset"] = {
                    "n_samples": len(k_ge_1_ids),
                    "exam": k1_sub["exam"],
                    "f1": k1_sub["f1"],
                    "exam_vec": k1_sub["exam_vec"],
                    "f1_vec": k1_sub["f1_vec"],
                }
            ledger_rows.append(rec_row)
            cells[cell_key] = rec_row

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_text = "\n".join(json.dumps(r, sort_keys=True) for r in ledger_rows) + ("\n" if ledger_rows else "")
    ledger_path.write_text(ledger_text, encoding="utf-8")
    return {
        "ledger_path": ledger_path.as_posix(),
        "ledger_sha256": sha256_file(ledger_path) if ledger_path.is_file() else None,
        "scored_cells": sorted(cells.keys()),
    }


def selftest() -> None:
    # 1. Parser tests: single-letter, multi-letter, multi-line with reasoning, out-of-range options, and garbage
    p1, u1 = parse_answer_output("Answer(s): B", {"A", "B"})
    assert p1 == ["B"] and u1 is False

    p2, u2 = parse_answer_output("Reasoning: step 1\nAnswer(s): A, C, D.", {"A", "B", "C", "D"})
    assert p2 == ["A", "C", "D"] and u2 is False

    # Takes the LAST Answer(s): line
    p3, u3 = parse_answer_output("Answer(s): A\nWait, revising:\nAnswer(s): B, C", {"A", "B", "C", "D"})
    assert p3 == ["B", "C"] and u3 is False

    # Filters out option letters not in the item's possible_answers (e.g. C, D on a 2-option question)
    p4, u4 = parse_answer_output("Answer(s): C, D", {"A", "B"})
    assert p4 == [] and u4 is True

    # Garbage without "Answer(s):" -> empty set and unparseable=True
    p5, u5 = parse_answer_output("The correct option is definitely A and B.", {"A", "B", "C", "D"})
    assert p5 == [] and u5 is True

    p6, u6 = parse_answer_output("", {"A", "B"})
    assert p6 == [] and u6 is True

    # 2. Exam and F1 math tests
    assert compute_item_exam_f1(["A", "C"], ["A", "C"]) == (100.0, 100.0)
    e_part, f_part = compute_item_exam_f1(["A"], ["A", "C"])
    assert e_part == 0.0 and abs(f_part - (200.0 / 3.0)) < 1e-12
    assert compute_item_exam_f1([], ["A", "C"]) == (0.0, 0.0)

    # 3. Bootstrap index matrix shape and determinism tests (CC-104 F4)
    m1000_a = make_bootstrap_matrix(1000, BOOTSTRAP_B, BOOTSTRAP_SEED)
    m1000_b = make_bootstrap_matrix(1000, BOOTSTRAP_B, BOOTSTRAP_SEED)
    m500 = make_bootstrap_matrix(500, BOOTSTRAP_B, BOOTSTRAP_SEED)
    assert m1000_a.shape == (10000, 1000) and np.array_equal(m1000_a, m1000_b)
    assert m500.shape == (10000, 500)
    mat1000_sha = hashlib.sha256(m1000_a.tobytes()).hexdigest()
    mat500_sha = hashlib.sha256(m500.tobytes()).hexdigest()

    print(json.dumps({
        "script": "score.py",
        "selftest": "OK",
        "bootstrap_10000x1000_sha256": mat1000_sha,
        "bootstrap_10000x500_sha256": mat500_sha,
        "parser_checks_passed": 6,
    }, sort_keys=True))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--runs-dir", type=Path, default=Path(".session_backup/2026-10-26/dvqa_pilot/runs"))
    ap.add_argument("--dvqa-dir", type=Path, default=Path("/root/dvqa_pilot"))
    ap.add_argument("--ledger", type=Path, default=Path(".session_backup/2026-10-26/dvqa_pilot/ledger.jsonl"))
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    res = score_runs_directory(args.runs_dir, args.dvqa_dir, args.ledger)
    print(json.dumps(res, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
