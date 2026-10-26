#!/usr/bin/env python3
"""Deterministic builder and verifier for DrivingVQA train-derived dev splits (CC-104 F4, R2, R4, R6).

Generates and verifies:
  - manuscript/ken/drivingvqa_dev500_ids.tsv   (500 IDs, seed=20261025, pinned sha256 9896af11...)
  - manuscript/ken/drivingvqa_dev500b_ids.tsv  (first 500 of the remaining 2,642 train IDs ordered by
                                                sha256("vsps|dvqa|p1b|" + str(id)))
  - manuscript/ken/drivingvqa_dev1000_ids.tsv  (1,000 IDs = dev500 followed by dev500b)
  - manuscript/ken/dvqa_train_descriptive_stats.json (pure deterministic counts from train.json; no simulation)

Usage:
  python3 manuscript/ken/ken_dvqa_pilot/build_splits_and_stats.py
  python3 manuscript/ken/ken_dvqa_pilot/build_splits_and_stats.py --selftest
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import random
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
KEN_DIR = ROOT / "manuscript" / "ken"
TRAIN_JSON_DEFAULT = Path(
    "<ken local scratch>"
    "/scratch/drivingvqa_pilot/train.json"
)
TRAIN_JSON_SHA256 = "4a204e3fa7516db313ceeb91ac989919979e31da20e484bc5f4018c261bd483d"
DEV500_TSV_SHA256 = "9896af1186ddd6a5806095ba696851b5aef512079f5d0813cff3f7f4fae9c4ce"
DEV500_ID_COL_SHA256 = "b034ec50c3c52bd45d9e6ab004239d14603d1fbc14ca951a0d0eab97897cfd97"
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

    # Disjointness and union checks
    assert len(set(dev500_ids) & set(dev500b_ids)) == 0
    assert len(set(dev1000_ids)) == 1000
    assert len(set(dev1000_ids) & set(bank2142_ids)) == 0
    assert len(set(dev1000_ids) | set(bank2142_ids)) == 3142

    dev500_path = KEN_DIR / "drivingvqa_dev500_ids.tsv"
    dev500b_path = KEN_DIR / "drivingvqa_dev500b_ids.tsv"
    dev1000_path = KEN_DIR / "drivingvqa_dev1000_ids.tsv"
    stats_path = KEN_DIR / "dvqa_train_descriptive_stats.json"

    # Extract image number gaps in train.json (CC-104 line 53 verification)
    img_nums = sorted(
        int(Path(str(train_data[sid]["img_filename"])).stem) for sid in all_ids
    )
    min_img_num, max_img_num = img_nums[0], img_nums[-1]
    distinct_img_nums = len(set(img_nums))
    missing_gaps_in_span = (max_img_num - min_img_num + 1) - distinct_img_nums

    stats = {
        "schema": "vsps.ken_dvqa_descriptive_stats.v1",
        "label": "EXPLORATORY_DESCRIPTIVE_ONLY",
        "ruling_authority": "CC-104 (F4, R2, R4, R6)",
        "source_dataset": {
            "name": "EPFL-DrivingVQA train.json",
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
                "no_entities_QP_EA": 55.6,
                "anyres4_upper_bound": 60.7,
                "predicted_entities_visual_crops": 58.7,
                "oracle_entities_visual_crops_QPRV_EA": 62.0,
                "oracle_vs_predicted_finetuned_gain_pts": 3.3,
                "sesoi_p1_threshold_pts": 3.0,
            },
            "sec5_2_random_baseline_test_exam_pct": 19.8,
            "sec5_2_human_expert_explanation_upper_bound_exam_pct": 78.3,
        },
    }

    if write_files:
        if not dev500_path.exists() or sha256_file(dev500_path) != DEV500_TSV_SHA256:
            dev500_path.write_text(tsv_dev500, encoding="utf-8")
        dev500b_path.write_text(tsv_dev500b, encoding="utf-8")
        dev1000_path.write_text(tsv_dev1000, encoding="utf-8")
        stats_path.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return stats


def selftest() -> None:
    # Verify p1b ordering determinism
    k1 = p1b_order_key("6")
    k2 = p1b_order_key("26")
    assert k1[0] == hashlib.sha256(b"vsps|dvqa|p1b|6").hexdigest()
    assert k1 != k2
    if TRAIN_JSON_DEFAULT.is_file():
        s1 = build_all(TRAIN_JSON_DEFAULT, write_files=False)
        s2 = build_all(TRAIN_JSON_DEFAULT, write_files=False)
        b1 = json.dumps(s1, sort_keys=True).encode("utf-8")
        b2 = json.dumps(s2, sort_keys=True).encode("utf-8")
        assert b1 == b2, "build_all must be byte-identical across calls"
        assert s1["manifests"]["dev500"]["tsv_sha256"] == DEV500_TSV_SHA256
        assert s1["manifests"]["dev500"]["id_column_sha256"] == DEV500_ID_COL_SHA256
        assert s1["manifests"]["dev1000"]["n_samples"] == 1000
    print(json.dumps({
        "script": "build_splits_and_stats.py",
        "selftest": "OK",
        "p1b_sample6_sha256": k1[0],
    }, sort_keys=True))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-json", type=Path, default=TRAIN_JSON_DEFAULT)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
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
