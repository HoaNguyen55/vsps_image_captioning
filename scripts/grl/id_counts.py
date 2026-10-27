#!/usr/bin/env python3
"""G-RL ID-only gatekeeper script (CC-114 W2, CC-118 W2). Reads image ids only, never a caption.

    python3 scripts/grl/id_counts.py --selftest      synthetic ids, no data
    python3 scripts/grl/id_counts.py                 laptop, CPU: asserts every count, writes OUT/id_counts.json and the
                                                     id lists the pilot runners pin (ut2532.txt, val924.txt, kv5000.txt)

Fields read: UIT-ViIC `images[].id` and `annotations[].image_id` (reference counts only); Karpathy `images[].cocoid`
and `images[].split`; exclusion.json `ids.coco`; the keys of A's a_n3 instance gold and of gt_cache's `refs`/`inst`.
The JSON loader parses the caption fields of the UIT-ViIC and Karpathy files; they are never used, printed or written.
exclusion.json's image_sha256 rule needs the image bytes, so the M3 runner applies it (scripts/grl/common.py).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "manuscript/prereg/2026-10-27_grl_pilot"
INPUTS = {  # path -> sha256
    "manuscript/prereg/2026-10-21_dev_pools/exclusion.json":
        "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f",
    "data/datasets/uitviic/train_data.json": "441d22d29eb7aa12d32d49e330778a4a918c3a9413c23294a9daec92a238d110",
    "data/datasets/uitviic/val_data.json": "fee7d116683670ef5ce14f405594aa73bb08dd1bdbf1f2cdc3f9e01bbfa9b044",
    "data/datasets/karpathy/dataset_coco.json": "2fd999220673258012acfb411a4e7e66af7d488050b2519b0badcc49b7600b8d",
    ".session_backup/2026-10-14/r12_verify/gt_cache.json":
        "f986f8ff9e429cc71232902c6c2a64b6d9d4ce5657760cf8031cf3fe3e9c9418",
    ".session_backup/2026-10-19/HL_human_labels/a_n3_instance_gold.json":
        "00e19c285fa459176de508344d12d88112fc7aa50e151f01e1469e11d512bcad",
    "manuscript/prereg/2026-10-27_c_en/cen_coco_kval.tsv":
        "f7d8369f9e16375be087c87be454e90b021fb48670db8a29fbd3ce9379e2dbcd",
    "manuscript/prereg/2026-10-27_c_en/cen_coco_test.tsv":
        "67555b281d87b01a0f742214da552be0f7c4f4977f543db98a9acd2901787eb1",
}
#: every value the rulings state (CC-106 l.41-48, CC-114 l.40, CC-118 l.156, W2)
EXPECT = {
    "kv": 5000, "kv_minus_refused": 4870, "kv_pool": 4740, "kv_pool_a_excluded": 4224,
    "kv_refused": 130, "kv_refused_by_source": {"chair500": 61, "pope500": 70},
    "train": 2695, "train_refused": 163,
    "train_refused_by_source": {"coco_karpathy_test": 133, "coco2500": 59, "chair500": 14, "pope500": 21},
    "ut": 2532, "ut_a_excluded": 2431, "train_kv_raw": 132, "ut_kv": 130,
    "ut_gate1": 2402, "ut_gate1_x_kv": 0, "a_touched_ut_gate1": 88, "ut_gate1_restval": 857,  # PI-1026u Q2: 2,532 minus the 130 Karpathy-val ids (disclosed exclusion)
    "train_x_cen_coco_kval": 132, "train_x_cen_coco_test": 133,  # CC-119 W19 (judges' counts)
    "ut_gate1_x_cen_coco_kval": 0, "ut_gate1_x_cen_coco_test": 0, "val_x_cen_coco_kval": 0, "val_x_cen_coco_test": 0,
    "ut_x_kv_pool": 0, "ut_x_kv_pool_a_excluded": 0,
    "a_touched_kv_pool": 516, "a_touched_ut": 101, "a_touched_train_raw": 131,
    "val": 924, "val_refused": 0, "val_x_kv": 0, "val_x_a_touched": 0, "val_karpathy_split": {"train": 924},
    "restval": 30504, "restval_chair_or_pope_union": 734, "restval_chair_plus_pope_sum": 739,
    "restval_minus_refused": 29770, "restval_minus_refused_minus_uitviic_train": 28913,
}


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha_ids(ids) -> str:
    return hashlib.sha256("".join(f"{i}\n" for i in sorted(ids)).encode()).hexdigest()


def counts(train: set, val: set, kp_split: dict, ex: dict, touched: set, cen: dict) -> dict:
    """kp_split: cocoid -> Karpathy split; ex: exclusion.json ids.coco {source: [ids]}; touched: A-touched ids;
    cen: C-EN's protected id lists {"kval": ids, "test": ids}."""
    refused = set().union(*map(set, ex.values()))
    kv = {i for i, s in kp_split.items() if s == "val"}
    rv = {i for i, s in kp_split.items() if s == "restval"}
    ut = train - refused
    g1 = ut - kv
    kv_pool = (kv - refused) - ut
    kv_a = kv_pool - touched
    chair, pope = set(ex.get("chair500", ())), set(ex.get("pope500", ()))
    by = lambda pool: {k: n for k, v in ex.items() if (n := len(pool & set(v)))}  # noqa: E731
    vsplit: dict = {}
    for i in val:
        vsplit[kp_split.get(i)] = vsplit.get(kp_split.get(i), 0) + 1
    return {
        "kv": len(kv), "kv_minus_refused": len(kv - refused), "kv_pool": len(kv_pool), "kv_pool_a_excluded": len(kv_a),
        "kv_refused": len(kv & refused), "kv_refused_by_source": by(kv),
        "train": len(train), "train_refused": len(train & refused), "train_refused_by_source": by(train),
        "ut": len(ut), "ut_a_excluded": len(ut - touched), "train_kv_raw": len(train & kv), "ut_kv": len(ut & kv),
        "ut_gate1": len(g1), "ut_gate1_x_kv": len(g1 & kv), "a_touched_ut_gate1": len(g1 & touched),
        "ut_gate1_restval": len(g1 & rv),
        "train_x_cen_coco_kval": len(train & cen["kval"]), "train_x_cen_coco_test": len(train & cen["test"]),
        "ut_gate1_x_cen_coco_kval": len(g1 & cen["kval"]), "ut_gate1_x_cen_coco_test": len(g1 & cen["test"]),
        "val_x_cen_coco_kval": len(val & cen["kval"]), "val_x_cen_coco_test": len(val & cen["test"]),
        "ut_x_kv_pool": len(ut & kv_pool), "ut_x_kv_pool_a_excluded": len(ut & kv_a),
        "a_touched_kv_pool": len(kv_pool & touched), "a_touched_ut": len(ut & touched),
        "a_touched_train_raw": len(train & touched),
        "val": len(val), "val_refused": len(val & refused), "val_x_kv": len(val & kv),
        "val_x_a_touched": len(val & touched), "val_karpathy_split": vsplit,
        "restval": len(rv), "restval_chair_or_pope_union": len(rv & (chair | pope)),
        "restval_chair_plus_pope_sum": len(rv & chair) + len(rv & pope),
        "restval_minus_refused": len(rv - refused), "restval_minus_refused_minus_uitviic_train": len(rv - refused - train),
    }, {"ut": ut, "ut_gate1": g1, "val": val, "kv": kv, "kv_pool": kv_pool, "kv_pool_a_excluded": kv_a}


def check(got: dict, want: dict) -> None:
    bad = {k: (got.get(k), v) for k, v in want.items() if got.get(k) != v}
    if bad:
        raise SystemExit(f"COUNT MISMATCH (got, expected): {bad}")


def main() -> int:
    shas = {}
    for rel, want in INPUTS.items():
        shas[rel] = sha_file(ROOT / rel)
        if shas[rel] != want:
            raise SystemExit(f"{rel}: sha256 {shas[rel][:12]} is not the pinned {want[:12]}")
    load = lambda rel: json.loads((ROOT / rel).read_text(encoding="utf-8"))  # noqa: E731
    ex = load("manuscript/prereg/2026-10-21_dev_pools/exclusion.json")["ids"]["coco"]
    uv = {s: load(f"data/datasets/uitviic/{s}_data.json") for s in ("train", "val")}
    train, val = ({int(i["id"]) for i in uv[s]["images"]} for s in ("train", "val"))
    kp_split = {int(i["cocoid"]): i["split"] for i in load("data/datasets/karpathy/dataset_coco.json")["images"]}
    gt = load(".session_backup/2026-10-14/r12_verify/gt_cache.json")
    touched = {int(k) for k in (*gt["refs"], *gt["inst"], *load(".session_backup/2026-10-19/HL_human_labels/"
                                                                 "a_n3_instance_gold.json"))}
    cen = {k: {int(r.split("\t")[0]) for r in (ROOT / f"manuscript/prereg/2026-10-27_c_en/cen_coco_{k}.tsv")
                                          .read_text().splitlines()[1:]} for k in ("kval", "test")}
    got, pools = counts(train, val, kp_split, ex, touched, cen)
    check(got, EXPECT)
    ut_refs = sum(int(a["image_id"]) in pools["ut"] for a in uv["train"]["annotations"])
    g1_refs = sum(int(a["image_id"]) in pools["ut_gate1"] for a in uv["train"]["annotations"])
    val_refs = sum(1 for _ in uv["val"]["annotations"])
    OUT.mkdir(parents=True, exist_ok=True)
    lists = {"ut2532.txt": pools["ut"], "ut2402.txt": pools["ut_gate1"], "val924.txt": pools["val"],
             "kv5000.txt": pools["kv"]}
    for name, ids in lists.items():
        (OUT / name).write_text("".join(f"{i}\n" for i in sorted(ids)), encoding="utf-8")
    rec = {"schema": "vsps.grl.id_counts.v1", "script_sha256": sha_file(Path(__file__)),
           "inputs_sha256": shas, "counts": got,
           "references_per_split": {"ut2532": ut_refs, "ut2402": g1_refs, "val924": val_refs},
           "id_lists_sha256": {k: sha_ids(v) for k, v in pools.items()},
           "files_sha256": {name: sha_file(OUT / name) for name in lists},
           "notes": ["ids only; no caption field was used, printed or written",
                     "exclusion.json's image_sha256 rule is applied on M3 by scripts/grl/common.py (needs image bytes)",
                     "restval: 29,770 = minus exclusion.json; 28,913 = also minus UIT-ViIC train (885); "
                     "734 = CHAIR-500 or POPE-500 ids in restval, 739 = their sum (5 ids in both)",
                     "train-2695 has 131 A-touched ids, 101 of them in UT-2532 (training-side disclosure only)",
                     "Gate-1 pool = UT-2402 (PI-1026u Q2): the 130 Karpathy-val ids are a pre-fixed, disclosed leakage "
                     "exclusion so that no model output exists on Karpathy val (C-EN PREREG l.67/l.159); 2,532 beside it",
                     "cen_* lists: only the id column is read"]}
    (OUT / "id_counts.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"counts": got, "references_per_split": rec["references_per_split"]}, indent=1))
    return 0


def selftest() -> None:
    # 10 Karpathy ids: val 1-4, restval 5-7, test 8-9, train 10; train = {1, 5, 8, 10}, val = {10}
    kp = {1: "val", 2: "val", 3: "val", 4: "val", 5: "restval", 6: "restval", 7: "restval", 8: "test", 9: "test",
          10: "train"}
    ex = {"coco_karpathy_test": [8, 9], "chair500": [2, 6], "pope500": [6]}
    got, pools = counts({1, 5, 8, 10}, {10}, kp, ex, touched={3, 5}, cen={"kval": {1, 2, 3, 4}, "test": {8, 9}})
    assert got["train_refused"] == 1 and got["ut"] == 3 and got["ut_kv"] == 1 and got["train_kv_raw"] == 1, got
    assert pools["ut_gate1"] == {5, 10} and got["ut_gate1_x_kv"] == 0 and got["train_x_cen_coco_kval"] == 1, got
    assert got["train_x_cen_coco_test"] == 1 and got["ut_gate1_x_cen_coco_test"] == 0 and got["val_x_cen_coco_kval"] == 0
    assert got["kv_minus_refused"] == 3 and got["kv_pool"] == 2 and got["kv_pool_a_excluded"] == 1, got
    assert pools["kv_pool"] == {3, 4} and got["ut_x_kv_pool"] == 0 and got["a_touched_ut"] == 1, got
    assert got["restval_chair_or_pope_union"] == 1 and got["restval_chair_plus_pope_sum"] == 2, got
    assert got["restval_minus_refused"] == 2 and got["restval_minus_refused_minus_uitviic_train"] == 1, got
    assert got["val_karpathy_split"] == {"train": 1} and got["kv_refused_by_source"] == {"chair500": 1}, got
    try:
        check(got, {"ut": 4})
    except SystemExit as e:
        assert "COUNT MISMATCH" in str(e), e
    else:
        raise AssertionError("check accepted a wrong count")
    assert sha_ids([2, 1]) == sha_ids({1, 2})
    print("id_counts selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit(0)
    sys.exit(main())
