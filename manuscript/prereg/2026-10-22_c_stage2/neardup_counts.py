#!/usr/bin/env python3
"""Paper C stage 2, pre-commit counts (CC-086 F2 reproduction, CC-087 C-g). CPU, counts and ids only, no caption.

Rows come from the git-excluded stage-1 feature cache through build_memory.features(), cache hit only: a missing
cache file stops the script before the SSCD pass. The rule is build_memory.near() (DESIGN §2.4), unchanged.

    NCS_DATA=<repo>/data nice -n 15 ~/.venvs/c_stage1_lists/bin/python \
        .session_backup/2026-10-22/c_stage2/neardup_counts.py --out .session_backup/2026-10-22/c_stage2/neardup_counts.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/c_stage1"))
import build_memory as BM  # noqa: E402

SSCD = ROOT / ".session_backup/2026-10-22/c_stage1/sscd_disc_mixup.torchscript.pt"
CACHE = ROOT / ".session_backup/2026-10-22/c_stage1/feat_cache"
LISTS = ROOT / "manuscript/prereg/2026-10-22_c_stage1/lists.json"
ESPLIT = ROOT / "manuscript/prereg/2026-10-22_e_stage1/e_split.json"
DEV299 = ROOT / "manuscript/prereg/2026-10-21_dev_pools/ktvic_dev299.tsv"


def sha_file(p: Path) -> str:
    return BM.C.lb.sha256_file(p)


def cached(paths: list[Path]) -> dict:
    """build_memory.features() on a cache hit; refuse before the SSCD pass if the cache file is missing."""
    key = hashlib.sha256(("|".join(sha_file(p) for p in paths) + sha_file(SSCD)).encode()).hexdigest()[:16]
    if not (CACHE / f"feat_{key}.npz").exists():
        raise SystemExit(f"cache miss for key {key}; not recomputing")
    f = BM.features(paths, str(SSCD), cache=CACHE)
    f["cache_file"] = f"feat_{key}.npz"
    return f


def rows_of(f: dict, shas) -> dict:
    """Rows of f whose image sha256 is in shas (all must be found)."""
    want = set(shas)
    idx = [i for i, s in enumerate(f["sha"]) if s in want]
    if len({f["sha"][i] for i in idx}) != len(want):
        raise SystemExit(f"{len(want) - len({f['sha'][i] for i in idx})} sha(s) not found in the group")
    return BM.subset(f, idx)


def masked(f: dict) -> dict:
    """Same rows with byte identity masked, so only the hash and SSCD rule can fire."""
    return {**f, "sha": [f"masked{i}" for i in range(len(f["sha"]))]}


def near_cols(fx: dict, fy: dict) -> np.ndarray:
    """Boolean (len y) mask: y has a near-duplicate in x with x on the left, i.e. build_memory.near()'s mask with
    x's mirrored hashes, reduced over x instead of y. This covers the orientation near(y, x) misses. x is small."""
    sim = np.nan_to_num(fx["sscd"]) @ np.nan_to_num(fy["sscd"]).T
    ph = np.minimum(BM.MO.hamming(fx["phash"], fy["phash"]), BM.MO.hamming(fx["phash_m"], fy["phash"]))
    dh = np.minimum(BM.MO.hamming(fx["dhash"], fy["dhash"]), BM.MO.hamming(fx["dhash_m"], fy["dhash"]))
    same = np.array(fx["sha"])[:, None] == np.array(fy["sha"])[None, :]
    return (((np.minimum(ph, dh) <= BM.HASH_MAX) & (sim >= BM.SSCD_MIN)) | same).any(0)


def count(x: dict, y: dict) -> int:
    return int(BM.near(x, y).sum())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    data = BM.C.lb.DATA / "datasets"
    kt = {s: json.loads((data / f"ktvic/{s}_data.json").read_text(encoding="utf-8"))["images"] for s in ("train", "test")}
    dev300 = set((ROOT / "data/splits/ktvic_dev300.txt").read_text(encoding="utf-8").split())
    ov_test = sorted(json.loads((data / "openviic/uit-openviic-annotation-test.json").read_text(encoding="utf-8")))
    xm = json.loads((data / "xm3600/full_data.json").read_text(encoding="utf-8"))["images"]
    xm600 = {str(i["id"]) for i in json.loads((data / "xm3600/test_data.json").read_text(encoding="utf-8"))["images"]}
    groups = {  # same groups, order and paths as build_memory.cmd_lists
        "kt_dev300": [data / "ktvic/images" / i["filename"] for i in kt["train"] if str(i["id"]) in dev300],
        "kt_test": [data / "ktvic/images" / i["filename"] for i in kt["test"]],
        "xm_all": [data / "xm3600/images" / i["filename"] for i in xm],
        "ov_test": [data / "openviic/images" / f for f in ov_test],
    }
    f = {g: cached(p) for g, p in groups.items()}
    lists = json.loads(LISTS.read_text(encoding="utf-8"))
    esplit = json.loads(ESPLIT.read_text(encoding="utf-8"))
    dev299_sha = [r.split("\t")[2] for r in DEV299.read_text(encoding="utf-8").splitlines()]
    assert len(dev299_sha) == 299
    s = {
        "dev299": rows_of(f["kt_dev300"], dev299_sha),
        "dev300": f["kt_dev300"],
        "xm_dev500": rows_of(f["xm_all"], [r[2] for r in lists["sets"]["xm_dev500"]]),
        "xm_test2500": rows_of(f["xm_all"], [r[2] for r in lists["sets"]["xm_test2500"]]),
        "xm600": rows_of(f["xm_all"], [h for r, h in zip(xm, f["xm_all"]["sha"]) if str(r["id"]) in xm600]),
        "e_dev_a": rows_of(f["xm_all"], [r[2] for r in esplit["sets"]["e_dev_a"]]),
        "e_dev_b": rows_of(f["xm_all"], [r[2] for r in esplit["sets"]["e_dev_b"]]),
        "ov_test": f["ov_test"],
        "kt_test": f["kt_test"],
    }
    sizes = {k: len(v["sha"]) for k, v in s.items()}
    assert sizes["xm600"] == 600 and sizes["xm_test2500"] == 2500 and sizes["ov_test"] == 2001
    assert set(s["e_dev_a"]["sha"]) | set(s["e_dev_b"]["sha"]) == set(s["xm_dev500"]["sha"])

    ov_left = BM.near(s["ov_test"], s["dev299"])  # test side, test on the left
    ov_right = near_cols(s["dev299"], s["ov_test"])  # test side, dev299 on the left
    xm_left = BM.near(s["xm_test2500"], s["dev299"])
    xm_right = near_cols(s["dev299"], s["xm_test2500"])
    ov_hit, xm_hit = ov_left | ov_right, xm_left | xm_right  # what C-g excludes: the union of both orientations
    assert int(near_cols(s["dev299"], s["dev299"]).sum()) == 299  # near_cols on a set against itself
    out = {
        "schema": "vsps.c_stage2_neardup_counts.v1",
        "rule": "build_memory.near() (DESIGN §2.4): min(pHash, dHash) <= 10 and SSCD >= 0.5, x's mirrored hashes, "
                "or byte-identical; count = left-hand images with >= 1 near-duplicate on the right",
        "inputs": {"script": sha_file(Path(__file__)), "build_memory.py": sha_file(Path(BM.__file__)),
                   "lists.json": sha_file(LISTS), "e_split.json": sha_file(ESPLIT),
                   "ktvic_dev299.tsv": sha_file(DEV299), "sscd": sha_file(SSCD),
                   "cache_files": {g: v["cache_file"] for g, v in f.items()}},
        "sizes": sizes,
        "f2_reproduction": {
            "xm_dev500_vs_xm_test2500": count(s["xm_dev500"], s["xm_test2500"]),
            "xm_dev500_vs_xm600": count(s["xm_dev500"], s["xm600"]),
            "xm_dev500_vs_ov_test": count(s["xm_dev500"], s["ov_test"]),
            "xm_dev500_vs_kt_test": count(s["xm_dev500"], s["kt_test"]),
            "e_dev_a_vs_e_dev_b": count(s["e_dev_a"], s["e_dev_b"]),
            "e_dev_b_vs_e_dev_a": count(s["e_dev_b"], s["e_dev_a"]),
        },
        "c_g": {
            "ov_test_vs_dev299": int(ov_left.sum()),
            "ov_test_hit_with_dev299_on_left": int(ov_right.sum()),
            "ov_test_excluded_union": int(ov_hit.sum()),
            "xm_test2500_hit_with_dev299_on_left": int(xm_right.sum()),
            "xm_test2500_excluded_union": int(xm_hit.sum()),
            "dev299_vs_ov_test": count(s["dev299"], s["ov_test"]),
            "xm_test2500_vs_dev299": int(xm_left.sum()),
            "dev299_vs_xm_test2500": count(s["dev299"], s["xm_test2500"]),
            "ov_test_vs_dev300": count(s["ov_test"], s["dev300"]),
            "dev300_vs_ov_test": count(s["dev300"], s["ov_test"]),
        },
        "controls": {
            "xm_dev500_vs_self": count(s["xm_dev500"], s["xm_dev500"]),
            "ov_test_vs_self_masked": count(s["ov_test"], masked(s["ov_test"])),
            "dev299_vs_self_masked": count(s["dev299"], masked(s["dev299"])),
        },
        "ov_test_excluded_files": [fn for fn, h in zip(ov_test, ov_hit) if h],
        "xm_test2500_excluded_sha256": sorted(h for h, x in zip(s["xm_test2500"]["sha"], xm_hit) if x),
    }
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("sizes", "f2_reproduction", "c_g", "controls")}))


if __name__ == "__main__":
    main()
