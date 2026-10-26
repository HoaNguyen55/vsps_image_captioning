#!/usr/bin/env python3
"""Deterministic builder and verifier for DrivingVQA train-derived dev splits (CC-104 F4, R2, R4, R6; W5, W8).

Generates and verifies:
  - manuscript/ken/drivingvqa_dev500_ids.tsv   (500 IDs, seed=20261025, pinned sha256 9896af11...)
  - manuscript/ken/drivingvqa_dev500b_ids.tsv  (first 500 of the remaining 2,642 train IDs ordered by
                                                sha256("vsps|dvqa|p1b|" + str(id)), pinned sha256 86cc908c...)
  - manuscript/ken/drivingvqa_dev1000_ids.tsv  (1,000 IDs = dev500 followed by dev500b, pinned sha256 636e0477...)
  - manuscript/ken/dvqa_train_descriptive_stats_v2.json (pure deterministic counts from train.json; W8 cleaned anchors)

REVIEW_KEN_BATCH8 W5 & W8 updates:
  - Dynamic `ROOT` discovery via `manuscript/prereg/2026-10-22_c_stage1/lists.json` so moving this folder
    from `manuscript/ken/ken_dvqa_pilot/` to `scripts/ken_dvqa_pilot/` works identically.
  - No hardcoded Gemini scratch path; default `--train-json` points to `/root/dvqa_pilot/train.json` (M4 path).
  - `--selftest` verifies all 3 pinned TSVs on disk, verifies deterministic split generation on 3,142 IDs,
    and when `/root/dvqa_pilot/train.json` (or `--train-json`) is present, recomputes `dev500b` and `dev1000`
    from `train.json` and verifies their exact SHA-256 digests (`86cc908c...` and `636e0477...`).
  - Writes `dvqa_train_descriptive_stats_v2.json` without overwriting `dvqa_train_descriptive_stats.json`,
    removing `55.6` and `78.3` and renaming `anyres4_upper_bound` to `table3_image_split_QPR_EA_anyres4: 60.7` (W8).

v4 (PI-1026c, CC-108 W8): P1, P2 and P3 all run on the full train split.
  - manuscript/ken/drivingvqa_train3142_ids.tsv: all 3,142 train IDs ordered by int(sample_id), same columns
    as dev1000. Written by `--write-train3142`; `--selftest` checks its pin, its count, dev1000 inside it.
  - The dev500/dev500b/dev1000 lists stay pinned as committed record; no v4 step reads them except that check.

Usage:
  python3 scripts/ken_dvqa_pilot/build_splits_and_stats.py --selftest
  python3 scripts/ken_dvqa_pilot/build_splits_and_stats.py --train-json /root/dvqa_pilot/train.json
  python3 scripts/ken_dvqa_pilot/build_splits_and_stats.py --train-json <train.json> --write-train3142
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
import os
from pathlib import Path
import random
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = next(
    (p for p in HERE.parents if (p / "manuscript/prereg/2026-10-22_c_stage1/lists.json").exists()),
    HERE.parents[2],
)
KEN_DIR = ROOT / "manuscript" / "ken"
TRAIN_JSON_DEFAULT = Path(os.environ.get("DVQA_TRAIN_JSON", "/root/dvqa_pilot/train.json"))
TRAIN_JSON_SHA256 = "4a204e3fa7516db313ceeb91ac989919979e31da20e484bc5f4018c261bd483d"

DEV500_TSV_SHA256 = "9896af1186ddd6a5806095ba696851b5aef512079f5d0813cff3f7f4fae9c4ce"
DEV500_ID_COL_SHA256 = "b034ec50c3c52bd45d9e6ab004239d14603d1fbc14ca951a0d0eab97897cfd97"
DEV500B_TSV_SHA256 = "86cc908cdf3e8622086caafd44572edf6ad35ef13ad0bdb8150bf393f3c30d54"
DEV500B_ID_COL_SHA256 = "4ab9977f21f73f6612dd15d713bf11e6d707451be0a12c9f61a16acda6570fee"
DEV1000_TSV_SHA256 = "636e04775153ef9cb879a7620d195fcaa7e86894ead73b008c8f95b47e268dec"
DEV1000_ID_COL_SHA256 = "c8bad8f202cd0038078f7646415bddd5deff29512b0bd987729ab4f5bc5ac7c9"

TRAIN3142_TSV_SHA256 = "39219d099ea25ccb79ce7bae13aa61b7198b9409bd468a6075b2e0b4809afc45"
TRAIN3142_TSV = KEN_DIR / "drivingvqa_train3142_ids.tsv"
N_TRAIN = 3142

HEADER = "sample_id\timg_filename\thas_multiple_questions\tnum_questions\tnum_gold_boxes\timage_size"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def p1b_order_key(sample_id: str) -> tuple[str, int]:
    """CC-104 F4: order remaining 2,642 train IDs by sha256('vsps|dvqa|p1b|' + str(id))."""
    h = sha256_text("vsps|dvqa|p1b|" + str(sample_id))
    return (h, int(sample_id))


def compute_splits(train_data: dict) -> tuple[list[str], list[str], list[str], list[str]]:
    all_ids = sorted(train_data.keys(), key=lambda x: int(x))
    if len(all_ids) != 3142:
        raise ValueError(f"Expected 3,142 train keys, got {len(all_ids)}")
    rng = random.Random(20261025)
    shuffled = list(all_ids)
    rng.shuffle(shuffled)
    dev500_ids = sorted(shuffled[:500], key=lambda x: int(x))
    dev500_set = set(dev500_ids)
    rem2642_ids = [sid for sid in all_ids if sid not in dev500_set]
    if len(rem2642_ids) != 2642:
        raise ValueError(f"Expected 2,642 remaining train IDs, got {len(rem2642_ids)}")
    rem_ordered = sorted(rem2642_ids, key=p1b_order_key)
    dev500b_ids = rem_ordered[:500]
    bank2142_ids = rem_ordered[500:]
    dev1000_ids = dev500_ids + dev500b_ids
    return dev500_ids, dev500b_ids, dev1000_ids, bank2142_ids


def train3142_ids(train_data: dict) -> list[str]:
    """v4: every train ID, ascending int(sample_id). No sampling, no remainder."""
    ids = sorted(train_data.keys(), key=lambda x: int(x))
    if len(ids) != N_TRAIN or len(set(ids)) != N_TRAIN:
        raise ValueError(f"Expected {N_TRAIN} unique train keys, got {len(set(ids))}")
    if len({str(train_data[sid]["img_filename"]) for sid in ids}) != N_TRAIN:
        raise ValueError("train img_filename values are not unique")
    return ids


def read_tsv_ids(path: Path) -> list[str]:
    return [r.split("\t")[0] for r in path.read_text(encoding="utf-8").splitlines()[1:] if r.strip()]


def check_train3142_tsv(path: Path = TRAIN3142_TSV) -> list[str]:
    """v4: pinned sha, 3,142 unique IDs in int order, and dev1000 is a subset."""
    if sha256_file(path) != TRAIN3142_TSV_SHA256:
        raise ValueError(f"{path} sha256 mismatch against pinned {TRAIN3142_TSV_SHA256[:8]}...")
    ids = read_tsv_ids(path)
    assert len(ids) == N_TRAIN and len(set(ids)) == N_TRAIN
    assert ids == sorted(ids, key=lambda x: int(x))
    dev1000 = read_tsv_ids(KEN_DIR / "drivingvqa_dev1000_ids.tsv")
    assert set(dev1000) <= set(ids), "dev1000 is not a subset of train3142"
    return ids


def power_table(ns: tuple[int, ...] = (500, 1000, N_TRAIN), discordance: tuple[float, ...] = (0.15, 0.25)) -> dict:
    """v4 planning arithmetic (normal approximation, no data): 95% CI half-width of a paired Exam difference,
    100 * 1.96 * sqrt(d / n) per backbone; pooled over two independent backbones divides by sqrt(2); fully
    correlated backbones keep the per-backbone width. `p_pass_p1_true_3p3` = P(estimate >= 3.0) for a true +3.3."""
    from statistics import NormalDist

    nd = NormalDist()
    out: dict = {}
    for n in ns:
        rows = {}
        for d in discordance:
            hw = 100.0 * 1.96 * (d / n) ** 0.5
            hw_pool = hw / 2 ** 0.5
            rows[f"d{int(round(d * 100))}"] = {
                "ci_half_width_per_backbone": round(hw, 2),
                "ci_half_width_pooled_independent": round(hw_pool, 2),
                "ci_half_width_pooled_correlated": round(hw, 2),
                "p_pass_p1_true_3p3_pooled_independent": round(nd.cdf((3.3 - 3.0) / (hw_pool / 1.96)), 3),
                "p_pass_p1_true_3p3_pooled_correlated": round(nd.cdf((3.3 - 3.0) / (hw / 1.96)), 3),
            }
        out[f"n{n}"] = rows
    return {"schema": "vsps.ken_dvqa_power.v4", "label": "PLANNING_ARITHMETIC_NO_DATA", "z": 1.96, "table": out}


def format_tsv_rows(sample_ids: list[str], train_data: dict) -> str:
    lines = [HEADER]
    for sid in sample_ids:
        item = train_data[sid]
        img_fn = str(item["img_filename"])
        has_multi = 1 if bool(item["has_multiple_questions"]) else 0
        q = item["questions"]
        num_q = len(q) if isinstance(q, list) else 1
        num_boxes = len(item.get("relevant_entities", []))
        w, h = item["img_size"]
        lines.append(f"{sid}\t{img_fn}\t{has_multi}\t{num_q}\t{num_boxes}\t{w}x{h}")
    return "\n".join(lines) + "\n"


def id_col_sha256(sample_ids: list[str]) -> str:
    return sha256_text("\n".join(sample_ids) + "\n")


def img_col_sha256(sample_ids: list[str], train_data: dict) -> str:
    return sha256_text("\n".join(str(train_data[sid]["img_filename"]) for sid in sample_ids) + "\n")


def describe_subset(sample_ids: list[str], train_data: dict, name: str) -> dict:
    n = len(sample_ids)
    multi_cnt = 0
    num_opts = Counter()
    num_true = Counter()
    num_boxes = Counter()
    res_counts = Counter()
    exam_types = Counter()
    entity_labels = Counter()
    total_boxes = 0
    k_ge_1_count = 0
    box_area_pcts: list[float] = []
    exact_combinatorial_exam_sum = 0.0
    exact_combinatorial_f1_sum = 0.0

    for sid in sample_ids:
        it = train_data[sid]
        hm = bool(it["has_multiple_questions"])
        if hm:
            multi_cnt += 1
        opts = sorted(it["possible_answers"].keys())
        ta = sorted(it["true_answers"])
        ta_set = set(ta)
        num_opts[len(opts)] += 1
        num_true[len(ta)] += 1
        ents = it.get("relevant_entities", [])
        k_boxes = len(ents)
        num_boxes[k_boxes] += 1
        total_boxes += k_boxes
        if k_boxes >= 1:
            k_ge_1_count += 1
        w, h = it["img_size"]
        img_area = float(w * h)
        for ent in ents:
            if isinstance(ent, dict):
                for ename, bbox in sorted(ent.items()):
                    lbl = str(ename).strip()
                    if lbl:
                        entity_labels[lbl] += 1
                    if isinstance(bbox, (list, tuple)) and len(bbox) == 4 and img_area > 0:
                        bx, by, bw, bh = (float(v) for v in bbox)
                        box_area_pcts.append(max(0.0, (bw * bh) / img_area) * 100.0)
        res_counts[f"{w}x{h}"] += 1
        exam_types[str(it.get("exam_type", "unknown"))] += 1

        # Exact combinatorial chance over the 2^|O| - 1 non-empty option subsets (deterministic arithmetic, no MC)
        nonempty = [set(c) for r in range(1, len(opts) + 1) for c in combinations(opts, r)]
        exact_combinatorial_exam_sum += sum(1.0 if c == ta_set else 0.0 for c in nonempty) / len(nonempty)
        exact_combinatorial_f1_sum += sum(
            (2.0 * len(c & ta_set)) / (len(c) + len(ta_set)) for c in nonempty
        ) / len(nonempty)

    distinct_imgs = sorted({str(train_data[sid]["img_filename"]) for sid in sample_ids})
    arr_area = np.asarray(box_area_pcts, dtype=np.float64) if box_area_pcts else np.zeros(1, dtype=np.float64)
    return {
        "subset_name": name,
        "n_samples": n,
        "n_distinct_images": len(distinct_imgs),
        "single_question_count": n - multi_cnt,
        "single_question_pct": round((n - multi_cnt) * 100.0 / n, 2),
        "multiple_question_count": multi_cnt,
        "multiple_question_pct": round(multi_cnt * 100.0 / n, 2),
        "k_ge_1_gold_box_samples": k_ge_1_count,
        "k_eq_0_gold_box_samples": n - k_ge_1_count,
        "total_gold_boxes": total_boxes,
        "mean_gold_boxes_per_sample": round(total_boxes / n, 4),
        "mean_gold_box_area_pct": round(float(np.mean(arr_area)), 2),
        "median_gold_box_area_pct": round(float(np.median(arr_area)), 2),
        "pct_gold_boxes_lt_1pct_area": round(float(np.mean(arr_area < 1.0) * 100.0), 2),
        "pct_gold_boxes_lt_2pct_area": round(float(np.mean(arr_area < 2.0) * 100.0), 2),
        "pct_gold_boxes_lt_5pct_area": round(float(np.mean(arr_area < 5.0) * 100.0), 2),
        "num_options_distribution": {str(k): int(num_opts[k]) for k in sorted(num_opts)},
        "num_true_answers_distribution": {str(k): int(num_true[k]) for k in sorted(num_true)},
        "num_gold_boxes_distribution": {str(k): int(num_boxes[k]) for k in sorted(num_boxes)},
        "top_10_image_resolutions": {
            k: int(v) for k, v in sorted(res_counts.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
        },
        "top_15_entity_labels": {
            k: int(v) for k, v in sorted(entity_labels.items(), key=lambda kv: (-kv[1], kv[0]))[:15]
        },
        "distinct_entity_labels": len(entity_labels),
        "combinatorial_uniform_nonempty_chance_exam_pct": round(exact_combinatorial_exam_sum * 100.0 / n, 2),
        "combinatorial_uniform_nonempty_chance_f1_pct": round(exact_combinatorial_f1_sum * 100.0 / n, 2),
    }


def build_all(train_json_path: Path = TRAIN_JSON_DEFAULT, write_files: bool = True) -> dict:
    if not train_json_path.is_file():
        raise FileNotFoundError(f"Missing DrivingVQA train.json at {train_json_path}")
    got_train_sha = sha256_file(train_json_path)
    if got_train_sha != TRAIN_JSON_SHA256:
        raise ValueError(f"train.json sha256 mismatch: {got_train_sha} != {TRAIN_JSON_SHA256}")

    train_data = json.loads(train_json_path.read_text(encoding="utf-8"))
    dev500_ids, dev500b_ids, dev1000_ids, bank2142_ids = compute_splits(train_data)
    all_ids = sorted(train_data.keys(), key=lambda x: int(x))

    tsv_dev500 = format_tsv_rows(dev500_ids, train_data)
    tsv_dev500b = format_tsv_rows(dev500b_ids, train_data)
    tsv_dev1000 = format_tsv_rows(dev1000_ids, train_data)

    if sha256_text(tsv_dev500) != DEV500_TSV_SHA256:
        raise ValueError("dev500 TSV sha256 mismatch against pinned 9896af11...")
    if id_col_sha256(dev500_ids) != DEV500_ID_COL_SHA256:
        raise ValueError("dev500 ID column sha256 mismatch against pinned b034ec50...")
    if sha256_text(tsv_dev500b) != DEV500B_TSV_SHA256:
        raise ValueError("dev500b TSV sha256 mismatch against pinned 86cc908c...")
    if sha256_text(tsv_dev1000) != DEV1000_TSV_SHA256:
        raise ValueError("dev1000 TSV sha256 mismatch against pinned 636e0477...")

    # Disjointness and union checks
    assert len(set(dev500_ids) & set(dev500b_ids)) == 0
    assert len(set(dev1000_ids)) == 1000
    assert len(set(dev1000_ids) & set(bank2142_ids)) == 0
    assert len(set(dev1000_ids) | set(bank2142_ids)) == 3142

    dev500_path = KEN_DIR / "drivingvqa_dev500_ids.tsv"
    dev500b_path = KEN_DIR / "drivingvqa_dev500b_ids.tsv"
    dev1000_path = KEN_DIR / "drivingvqa_dev1000_ids.tsv"
    # W8 & submission rule: write v2 descriptive stats without overwriting v1 dvqa_train_descriptive_stats.json
    stats_v2_path = KEN_DIR / "dvqa_train_descriptive_stats_v2.json"

    img_nums = sorted(
        int(Path(str(train_data[sid]["img_filename"])).stem) for sid in all_ids
    )
    min_img_num, max_img_num = img_nums[0], img_nums[-1]
    distinct_img_nums = len(set(img_nums))
    missing_gaps_in_span = (max_img_num - min_img_num + 1) - distinct_img_nums

    stats = {
        "schema": "vsps.ken_dvqa_descriptive_stats.v2",
        "label": "EXPLORATORY_DESCRIPTIVE_ONLY",
        "ruling_authority": "CC-104 (F4, R2, R4, R6) & REVIEW_KEN_BATCH8 (W5, W8)",
        "source_dataset": {
            "name": "EPFL-DrivingVQA train.json",
            "hf_revision": "02ce870cfe037b93cc034034cd747a7eecdd455c",
            "train_json_sha256": got_train_sha,
            "n_train_total": len(all_ids),
            "image_number_min": min_img_num,
            "image_number_max": max_img_num,
            "distinct_train_images": distinct_img_nums,
            "missing_image_number_gaps_in_span": missing_gaps_in_span,
        },
        "manifests": {
            "dev500": {
                "path": "manuscript/ken/drivingvqa_dev500_ids.tsv",
                "n_samples": len(dev500_ids),
                "rule": "random.Random(20261025).shuffle(sorted_ids)[:500], sorted by int(sample_id)",
                "tsv_sha256": sha256_text(tsv_dev500),
                "id_column_sha256": id_col_sha256(dev500_ids),
                "img_filename_column_sha256": img_col_sha256(dev500_ids, train_data),
                "first_5_ids": dev500_ids[:5],
                "last_5_ids": dev500_ids[-5:],
            },
            "dev500b": {
                "path": "manuscript/ken/drivingvqa_dev500b_ids.tsv",
                "n_samples": len(dev500b_ids),
                "rule": "First 500 of the 2,642 remaining train IDs ordered ascending by sha256('vsps|dvqa|p1b|' + str(id))",
                "tsv_sha256": sha256_text(tsv_dev500b),
                "id_column_sha256": id_col_sha256(dev500b_ids),
                "img_filename_column_sha256": img_col_sha256(dev500b_ids, train_data),
                "first_5_ids": dev500b_ids[:5],
                "last_5_ids": dev500b_ids[-5:],
                "first_id_p1b_sha256": p1b_order_key(dev500b_ids[0])[0],
                "last_id_p1b_sha256": p1b_order_key(dev500b_ids[-1])[0],
            },
            "dev1000": {
                "path": "manuscript/ken/drivingvqa_dev1000_ids.tsv",
                "n_samples": len(dev1000_ids),
                "rule": "dev500 (500 rows) concatenated with dev500b (500 rows) in exact pinned order",
                "tsv_sha256": sha256_text(tsv_dev1000),
                "id_column_sha256": id_col_sha256(dev1000_ids),
                "img_filename_column_sha256": img_col_sha256(dev1000_ids, train_data),
                "overlap_dev500_dev500b": 0,
            },
        },
        "subsets": {
            "train_all_3142": describe_subset(all_ids, train_data, "train_all_3142"),
            "dev500": describe_subset(dev500_ids, train_data, "dev500"),
            "dev500b": describe_subset(dev500b_ids, train_data, "dev500b"),
            "dev1000": describe_subset(dev1000_ids, train_data, "dev1000"),
            "remaining_bank_2142": describe_subset(bank2142_ids, train_data, "remaining_bank_2142"),
        },
        "published_paper_anchors_2501_04671": {
            "table3_llava_onevision_7b_finetuned_exam_pct": {
                "table3_image_split_QPR_EA_anyres4": 60.7,
                "predicted_entities_visual_crops": 58.7,
                "oracle_entities_visual_crops_QPRV_EA": 62.0,
                "oracle_vs_predicted_finetuned_gain_pts": 3.3,
                "sesoi_p1_threshold_pts": 3.0,
            },
            "sec5_2_random_baseline_test_exam_pct": 19.8,
        },
    }

    if write_files:
        if not dev500_path.exists() or sha256_file(dev500_path) != DEV500_TSV_SHA256:
            dev500_path.write_text(tsv_dev500, encoding="utf-8")
        if not dev500b_path.exists() or sha256_file(dev500b_path) != DEV500B_TSV_SHA256:
            dev500b_path.write_text(tsv_dev500b, encoding="utf-8")
        if not dev1000_path.exists() or sha256_file(dev1000_path) != DEV1000_TSV_SHA256:
            dev1000_path.write_text(tsv_dev1000, encoding="utf-8")
        stats_v2_path.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return stats


def can_read_file(path: Path) -> bool:
    try:
        return path.is_file() and os.access(path, os.R_OK)
    except OSError:
        return False


def selftest(train_json_path: Path = TRAIN_JSON_DEFAULT) -> None:
    # 1. Verify p1b ordering determinism
    k1 = p1b_order_key("6")
    k2 = p1b_order_key("26")
    assert k1[0] == hashlib.sha256(b"vsps|dvqa|p1b|6").hexdigest()
    assert k1 != k2

    # 2. Verify the 3 pinned TSVs in manuscript/ken/ match their exact SHA-256s, ID-column SHA-256s, and F4 ordering rule
    dev500_path = KEN_DIR / "drivingvqa_dev500_ids.tsv"
    dev500b_path = KEN_DIR / "drivingvqa_dev500b_ids.tsv"
    dev1000_path = KEN_DIR / "drivingvqa_dev1000_ids.tsv"
    assert sha256_file(dev500_path) == DEV500_TSV_SHA256
    assert sha256_file(dev500b_path) == DEV500B_TSV_SHA256
    assert sha256_file(dev1000_path) == DEV1000_TSV_SHA256

    ids_500 = [r.split("\t")[0] for r in dev500_path.read_text(encoding="utf-8").splitlines()[1:] if r.strip()]
    ids_500b = [r.split("\t")[0] for r in dev500b_path.read_text(encoding="utf-8").splitlines()[1:] if r.strip()]
    ids_1000 = [r.split("\t")[0] for r in dev1000_path.read_text(encoding="utf-8").splitlines()[1:] if r.strip()]
    assert id_col_sha256(ids_500) == DEV500_ID_COL_SHA256
    assert id_col_sha256(ids_500b) == DEV500B_ID_COL_SHA256
    assert id_col_sha256(ids_1000) == DEV1000_ID_COL_SHA256
    assert ids_1000 == ids_500 + ids_500b and len(set(ids_1000)) == 1000
    assert ids_500 == sorted(ids_500, key=lambda x: int(x))
    assert ids_500b == sorted(ids_500b, key=p1b_order_key)

    # 3. Verify compute_splits determinism on a 3,142-key dict
    synth_3142 = {str(i): {} for i in range(1, 3143)}
    s_500, s_500b, s_1000, s_bank = compute_splits(synth_3142)
    assert len(s_500) == 500 and len(s_500b) == 500 and len(s_1000) == 1000 and len(s_bank) == 2142
    assert len(set(s_500) & set(s_500b)) == 0 and s_1000 == s_500 + s_500b

    # 4. W5: When train.json is readable at train_json_path (e.g. /root/dvqa_pilot/train.json on M4),
    # recompute dev500, dev500b, and dev1000 from train.json and verify exact byte-level SHA-256 match
    recomputed_from_train = False
    if can_read_file(train_json_path):
        s1 = build_all(train_json_path, write_files=False)
        s2 = build_all(train_json_path, write_files=False)
        b1 = json.dumps(s1, sort_keys=True).encode("utf-8")
        b2 = json.dumps(s2, sort_keys=True).encode("utf-8")
        assert b1 == b2, "build_all must be byte-identical across calls"
        assert s1["manifests"]["dev500"]["tsv_sha256"] == DEV500_TSV_SHA256
        assert s1["manifests"]["dev500b"]["tsv_sha256"] == DEV500B_TSV_SHA256
        assert s1["manifests"]["dev1000"]["tsv_sha256"] == DEV1000_TSV_SHA256
        recomputed_from_train = True

    # 4b. v4 power arithmetic reproduces CC-104's n=500 per-backbone half-widths (3.4 / 4.4)
    pw = power_table()["table"]
    assert pw["n500"]["d15"]["ci_half_width_per_backbone"] == 3.39 and pw["n500"]["d25"]["ci_half_width_per_backbone"] == 4.38

    # 5. v4: pinned train3142 list, and byte-identical regeneration from train.json when readable
    ids_3142 = check_train3142_tsv(TRAIN3142_TSV)
    if can_read_file(train_json_path):
        train_data = json.loads(train_json_path.read_text(encoding="utf-8"))
        regen = format_tsv_rows(train3142_ids(train_data), train_data)
        assert sha256_text(regen) == TRAIN3142_TSV_SHA256

    print(json.dumps({
        "script": "build_splits_and_stats.py",
        "selftest": "OK",
        "train3142_tsv_sha256": TRAIN3142_TSV_SHA256,
        "train3142_n": len(ids_3142),
        "dev500_tsv_sha256": DEV500_TSV_SHA256,
        "dev500b_tsv_sha256": DEV500B_TSV_SHA256,
        "dev1000_tsv_sha256": DEV1000_TSV_SHA256,
        "recomputed_from_train_json": recomputed_from_train,
        "p1b_sample6_sha256": k1[0],
    }, sort_keys=True))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-json", type=Path, default=TRAIN_JSON_DEFAULT)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--write-train3142", action="store_true")
    ap.add_argument("--write-power", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest(args.train_json)
        return
    if args.write_power:
        out_p = KEN_DIR / "dvqa_train3142_power_v4.json"
        out_p.write_text(json.dumps(power_table(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"status": "OK", "path": out_p.relative_to(ROOT).as_posix(), "sha256": sha256_file(out_p)}))
        return
    if args.write_train3142:
        if sha256_file(args.train_json) != TRAIN_JSON_SHA256:
            raise SystemExit(f"REFUSED: train.json sha256 mismatch at {args.train_json}")
        train_data = json.loads(args.train_json.read_text(encoding="utf-8"))
        text = format_tsv_rows(train3142_ids(train_data), train_data)
        TRAIN3142_TSV.write_text(text, encoding="utf-8")
        print(json.dumps({"status": "OK", "path": TRAIN3142_TSV.relative_to(ROOT).as_posix(),
                          "n": N_TRAIN, "tsv_sha256": sha256_text(text)}, sort_keys=True))
        return
    stats = build_all(args.train_json, write_files=True)
    print(json.dumps({
        "status": "OK",
        "dev500_tsv_sha256": stats["manifests"]["dev500"]["tsv_sha256"],
        "dev500b_tsv_sha256": stats["manifests"]["dev500b"]["tsv_sha256"],
        "dev1000_tsv_sha256": stats["manifests"]["dev1000"]["tsv_sha256"],
        "dev500_id_col_sha256": stats["manifests"]["dev500"]["id_column_sha256"],
        "dev500b_id_col_sha256": stats["manifests"]["dev500b"]["id_column_sha256"],
        "dev1000_id_col_sha256": stats["manifests"]["dev1000"]["id_column_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
