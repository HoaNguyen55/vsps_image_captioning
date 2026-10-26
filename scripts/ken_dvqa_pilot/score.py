#!/usr/bin/env python3
"""Deterministic Scorer & Paired Bootstrap Engine for DrivingVQA Pilot P1, P2, P3 (CC-104 F1, F2, F4, F9, F10, R4; W1, W7).

Parser rule (CC-104 F1 & REVIEW_KEN_BATCH8 W1):
  - Take the last line containing "Answer(s):" (header matched case-insensitively).
  - Case-sensitively match a leading uppercase option list immediately after "Answer(s):"
    using `^\\s*([A-D]\\b(?:\\s*(?:,|and|&|/)\\s*[A-D]\\b)*)` (so lowercase "Answer(s): a" is rejected
    and trailing prose like "Answer(s): B, because a car is coming" yields ["B"], not ["A", "B"]).
  - Keep only standalone uppercase letters A-D that belong to the sample's `possible_answers` keys.
  - Otherwise, the predicted set is empty (Exam = 0.0, F1 = 0.0) and the item is counted in `unparseable_rate`.

Bootstrap rule (CC-104 F4):
  - B = 10,000 draws with `np.random.default_rng(0)`.
  - v4 (PI-1026c): P1, P2 and P3 all score the full train split (`train3142`), so there is one shared index
    matrix of shape (10000, 3142). The K >= 1 descriptive check has its own (10000, n_K>=1) matrix.

Usage:
  python3 scripts/ken_dvqa_pilot/score.py --selftest
  python3 scripts/ken_dvqa_pilot/score.py --runs-dir .session_backup/2026-10-26/dvqa_pilot/runs --dvqa-dir /root/dvqa_pilot --ledger .session_backup/2026-10-26/dvqa_pilot/ledger.jsonl
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
    (p for p in HERE.parents if (p / "manuscript/ken/drivingvqa_train3142_ids.tsv").exists()),
    HERE.parents[2],
)

TRAIN3142_TSV = ROOT / "manuscript/ken/drivingvqa_train3142_ids.tsv"
TRAIN3142_SHA256 = "39219d099ea25ccb79ce7bae13aa61b7198b9409bd468a6075b2e0b4809afc45"
N_ITEMS = 3142
TRAIN_JSON_PIN = "4a204e3fa7516db313ceeb91ac989919979e31da20e484bc5f4018c261bd483d"

MODELS = ("qwen25vl_7b", "internvl3_8b")
STAGE_A_ARMS = ("P1-Blind", "P1-Full", "P1-Oracle", "P3-SelfCap")
STAGE_B_ARMS = ("P2-Grid", "P2-AttCrop")
BOOTSTRAP_B = 10000
BOOTSTRAP_SEED = 0

ANSWER_LINE_RE = re.compile(r"answer\(s\)\s*:\s*(.*)$", flags=re.IGNORECASE)
# Case-sensitive leading uppercase option list right after "Answer(s):" (REVIEW_KEN_BATCH8 W1; supports Oxford comma ", and")
LEADING_OPTION_LIST_RE = re.compile(r"^\s*([A-D]\b(?:\s*(?:,\s*(?:and|&)|,|and|&|/)\s*[A-D]\b)*)")
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


def parse_answer_output(
    raw_output: str,
    valid_options: set[str] | list[str],
    return_reason: bool = False,
) -> tuple[list[str], bool] | tuple[list[str], bool, str]:
    """CC-104a W1 fixed parser grammar after the last 'Answer(s):' header:
    - Uppercase A-D tokens separated by ',', ', and', 'and', '&', '/', ';' or whitespace,
      or a run of 2-4 distinct capitals ('AC').
    - A capital followed by a space and a lowercase word ('A car') is prose and ends the list.
    - After the list, any remaining standalone A-D token, 'or' or '.' between letters,
      or a letter outside the item's options -> UNPARSEABLE.
    - Never adds or drops a letter silently.
    """
    def _ret(letters: list[str], unparseable: bool, reason: str):
        if return_reason:
            return letters, unparseable, reason
        return letters, unparseable

    if not isinstance(raw_output, str) or not raw_output.strip():
        return _ret([], True, "empty_output")
    valid_set = {str(o).strip() for o in valid_options if str(o).strip() in {"A", "B", "C", "D"}}
    matched_rhs: list[str] = []
    for line in raw_output.splitlines():
        m = ANSWER_LINE_RE.search(line)
        if m is not None:
            matched_rhs.append(m.group(1))
    if not matched_rhs:
        return _ret([], True, "missing_answer_header")
    s = matched_rhs[-1].strip()
    if not s:
        return _ret([], True, "empty_after_header")

    single_opt_re = re.compile(r"^([A-Z])\b(?!\s+(?!(?:and|or)\b\s+[A-Z]\b)[a-z])")
    multi_opt_re = re.compile(r"^([A-D]{2,4})\b")
    sep_re = re.compile(r"^(?:\s*,\s*(?:and\b|&)?\s*|\s+(?:and\b|&)\s+|\s*[/;]\s*|\s+)")

    def _match_opt(sub: str) -> tuple[list[str] | None, int]:
        m_multi = multi_opt_re.match(sub)
        if m_multi is not None:
            tok = m_multi.group(1)
            if len(set(tok)) == len(tok):
                return list(tok), m_multi.end()
            return None, 0
        m_single = single_opt_re.match(sub)
        if m_single is not None:
            return [m_single.group(1)], m_single.end()
        return None, 0

    first_toks, consumed = _match_opt(s)
    if not first_toks:
        return _ret([], True, "no_leading_option_list")

    extracted: list[str] = list(first_toks)
    pos = consumed
    while pos < len(s):
        m_sep = sep_re.match(s[pos:])
        if m_sep is None:
            break
        next_pos = pos + m_sep.end()
        nxt_toks, nxt_len = _match_opt(s[next_pos:])
        if not nxt_toks:
            break
        extracted.extend(nxt_toks)
        pos = next_pos + nxt_len

    rem = s[pos:]
    if re.search(r"^\s*(?:,\s*)?\bor\b\s*[A-Z]\b", rem):
        return _ret([], True, "ambiguous_or_between_letters")
    if re.search(r"^\s*\.\s*[A-Z]\b(?!\s+(?!(?:and|or)\b\s+[A-Z]\b)[a-z])", rem):
        return _ret([], True, "period_between_letters")
    if re.search(r"\b[A-E]\b(?!\s+(?!(?:and|or)\b\s+[A-Z]\b)[a-z])", rem) or re.search(r"\b[A-D]{2,4}\b", rem):
        return _ret([], True, "trailing_standalone_option_token")

    if any(ch not in valid_set for ch in extracted):
        return _ret([], True, "option_out_of_range")

    letters = sorted(set(extracted))
    if not letters:
        return _ret([], True, "no_leading_option_list")
    return _ret(letters, False, "ok")


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
    unparseable_reasons: dict[str, int] = {}
    empty_caption_cnt = 0
    missing_ids: list[str] = []

    for idx, sid in enumerate(sample_ids):
        if sid not in preds_by_id:
            missing_ids.append(sid)
            unparseable_cnt += 1
            unparseable_reasons["missing_prediction"] = unparseable_reasons.get("missing_prediction", 0) + 1
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
        parsed_letters, is_unparseable, reason = parse_answer_output(raw_out, valid_opts, return_reason=True)
        if is_unparseable:
            unparseable_cnt += 1
            unparseable_reasons[reason] = unparseable_reasons.get(reason, 0) + 1
        e_val, f_val = compute_item_exam_f1(parsed_letters, true_ans)
        exam_vec[idx] = e_val
        f1_vec[idx] = f_val

    unparseable_rate_raw = unparseable_cnt / float(n)
    empty_caption_rate_raw = (empty_caption_cnt / float(n)) if is_p3 else 0.0
    unparseable_rate = round(unparseable_rate_raw, 4)
    empty_caption_rate = round(empty_caption_rate_raw, 4) if is_p3 else 0.0

    return {
        "n_samples": n,
        "complete": len(missing_ids) == 0,
        "missing_count": len(missing_ids),
        "unparseable_count": int(unparseable_cnt),
        "unparseable_rate": unparseable_rate,
        "unparseable_reasons": {k: int(unparseable_reasons[k]) for k in sorted(unparseable_reasons)},
        "unparseable_stop_triggered": bool(unparseable_rate_raw > 0.10),
        "empty_caption_count": int(empty_caption_cnt) if is_p3 else 0,
        "empty_caption_rate": empty_caption_rate,
        "empty_caption_stop_triggered": bool(is_p3 and empty_caption_rate_raw > 0.20),
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

    train_ids = load_manifest_ids(TRAIN3142_TSV, TRAIN3142_SHA256, N_ITEMS)
    boot_all = make_bootstrap_matrix(N_ITEMS, BOOTSTRAP_B, BOOTSTRAP_SEED)

    # K >= 1 subset indices within train3142 (CC-104 F9 descriptive check)
    k_ge_1_ids = [sid for sid in train_ids if len(gold_data[sid].get("relevant_entities", [])) >= 1]
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
            cell_res = score_predictions_map(preds_map, train_ids, gold_data, boot_all, is_p3=is_p3)
            cell_key = f"{arm}__{model}"
            rec_row = {
                "cell": cell_key,
                "arm": arm,
                "model": model,
                "set": "train3142",
                "run_file": run_file.name,
                "run_file_sha256": sha256_file(run_file),
                **cell_res,
            }
            if arm in ("P1-Blind", "P1-Full", "P1-Oracle"):
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
    # 1. Existing 10 parser tests (preserved verbatim from v2)
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

    # W1 test 7: trailing prose with article "a" must NOT be parsed as option A
    p7, u7 = parse_answer_output("Answer(s): B, because a car is coming", {"A", "B", "C", "D"})
    assert p7 == ["B"] and u7 is False, f"W1 trailing prose test failed: got {(p7, u7)}"

    # W1 test 8: lowercase "Answer(s): a" must be rejected as unparseable
    p8, u8 = parse_answer_output("Answer(s): a", {"A", "B", "C", "D"})
    assert p8 == [] and u8 is True, f"W1 lowercase test failed: got {(p8, u8)}"

    # W1 test 9: conjunctions 'and', '&', '/' and Oxford comma ', and' in leading uppercase list
    p9, u9 = parse_answer_output("Answer(s): A and C / D", {"A", "B", "C", "D"})
    assert p9 == ["A", "C", "D"] and u9 is False
    p10, u10 = parse_answer_output("Answer(s): A, B, and C.", {"A", "B", "C", "D"})
    assert p10 == ["A", "B", "C"] and u10 is False

    # 1b. CC-104a W1 pinned selftest asserts (options A-D unless stated):
    opts_abcd = {"A", "B", "C", "D"}
    w1_pinned_cases = [
        ("B, A car is coming", opts_abcd, ["B"], False),
        ("B, because a car", opts_abcd, ["B"], False),
        ("A C", opts_abcd, ["A", "C"], False),
        ("A; B", opts_abcd, ["A", "B"], False),
        ("A; C", opts_abcd, ["A", "C"], False),
        ("AC", opts_abcd, ["A", "C"], False),
        ("A, C.", opts_abcd, ["A", "C"], False),
        ("A and C", opts_abcd, ["A", "C"], False),
        ("A or B", opts_abcd, [], True),
        ("A. B.", opts_abcd, [], True),
        ("A, E", opts_abcd, [], True),
        ("A, C", {"A", "B"}, [], True),
        ("a", opts_abcd, [], True),
    ]
    for rhs_str, opts, exp_letters, exp_unp in w1_pinned_cases:
        got_l, got_u, got_reason = parse_answer_output(f"Answer(s): {rhs_str}", opts, return_reason=True)
        assert (got_l, got_u) == (exp_letters, exp_unp), (
            f"CC-104a W1 pinned assert failed for {rhs_str!r} with options {opts}: "
            f"got {(got_l, got_u, got_reason)}, expected {(exp_letters, exp_unp)}"
        )

    # 2. Exam and F1 math tests
    assert compute_item_exam_f1(["A", "C"], ["A", "C"]) == (100.0, 100.0)
    e_part, f_part = compute_item_exam_f1(["A"], ["A", "C"])
    assert e_part == 0.0 and abs(f_part - (200.0 / 3.0)) < 1e-12
    assert compute_item_exam_f1([], ["A", "C"]) == (0.0, 0.0)

    # 3. Bootstrap index matrix shape and determinism tests (CC-104 F4)
    m_all_a = make_bootstrap_matrix(N_ITEMS, BOOTSTRAP_B, BOOTSTRAP_SEED)
    m_all_b = make_bootstrap_matrix(N_ITEMS, BOOTSTRAP_B, BOOTSTRAP_SEED)
    assert m_all_a.shape == (10000, 3142) and np.array_equal(m_all_a, m_all_b)
    mat_all_sha = hashlib.sha256(m_all_a.tobytes()).hexdigest()
    train_ids = load_manifest_ids(TRAIN3142_TSV, TRAIN3142_SHA256, N_ITEMS)
    assert train_ids == sorted(train_ids, key=int)

    # 4. Verify per-cell unparseable_reasons logging in score_predictions_map (CC-104a W1)
    mini_boot = make_bootstrap_matrix(4, BOOTSTRAP_B, BOOTSTRAP_SEED)
    mini_gold = {
        "1": {"possible_answers": {"A": "x", "B": "y"}, "true_answers": ["B"]},
        "2": {"possible_answers": {"A": "x", "B": "y"}, "true_answers": ["A"]},
        "3": {"possible_answers": {"A": "x", "B": "y", "C": "z", "D": "w"}, "true_answers": ["A"]},
        "4": {"possible_answers": {"A": "x", "B": "y", "C": "z", "D": "w"}, "true_answers": ["A"]},
    }
    mini_preds = {
        "1": {"raw_output": "Answer(s): B, A car is coming"},
        "2": {"raw_output": "Answer(s): A, C"},
        "3": {"raw_output": "Answer(s): A or B"},
        "4": {"raw_output": "Answer(s): A. B."},
    }
    mini_res = score_predictions_map(mini_preds, ["1", "2", "3", "4"], mini_gold, mini_boot, is_p3=False)
    assert mini_res["unparseable_count"] == 3
    assert mini_res["unparseable_reasons"] == {
        "ambiguous_or_between_letters": 1,
        "option_out_of_range": 1,
        "period_between_letters": 1,
    }

    print(json.dumps({
        "script": "score.py",
        "selftest": "OK",
        "bootstrap_10000x3142_sha256": mat_all_sha,
        "parser_checks_passed": 23,
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
