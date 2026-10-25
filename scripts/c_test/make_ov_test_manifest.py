#!/usr/bin/env python3
"""Paper C test (CC-103 W2): pin the OV-test manifest, CPU, local.

  NCS_DATA=data python3 scripts/c_test/make_ov_test_manifest.py

Reads the OpenViIC test annotation for its keys only (as build_memory.py:208 and :286), hashes the image bytes, and
writes file names and sha256 only: ov_test_files.tsv (2,001 rows, name<TAB>sha256, sorted by name; the W6 bootstrap
order) and ov_test_primary1941.txt (that order minus the 60 near-duplicates of dev299). Every W2 check is asserted
before anything is written; on any failure nothing is written.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(os.environ.get("NCS_DATA", ROOT / "data"))
OUT = ROOT / "manuscript/prereg/2026-10-25_c_test"
PINS = {  # input -> sha256 (LISTS_ADDENDUM; stage-2 PREREG header; decode_icl.PINS[EXCL])
    "manuscript/prereg/2026-10-22_c_stage1/lists.json":
        "5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371",
    "manuscript/prereg/2026-10-22_c_stage2/ov_test_dev299_neardup_files.txt":
        "737e617a966478d9bcadb0c932d72a6f8de7dd5c7e83c98730e1a88720f2f41f",
    "manuscript/prereg/2026-10-21_dev_pools/exclusion.json":
        "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f",
}
PAIRS = {  # CC-103 "OV-test manifest invariants": the 4 byte-identical pairs
    ("00000005497.jpg", "00000009980.jpg"), ("00000006957.jpg", "00000009950.jpg"),
    ("00000009345.jpg", "00000009997.jpg"), ("00000009606.jpg", "00000009892.jpg"),
}
TRUNCATED = {"00000000768.jpg", "00000001010.jpg", "00000005095.jpg"}  # lists.json truncated_protected_decoded
LINE = re.compile(r"^\d{11}\.(jpg|jpeg|png|JPG)(\t[0-9a-f]{64})?$")  # names and shas only: no caption can fit


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pinned(rel: str) -> Path:
    p = ROOT / rel
    assert sha(p) == PINS[rel], f"pin mismatch: {rel}"
    return p


def check(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"CHECK FAILED, nothing written: {msg}")
    print(f"ok  {msg}")


def main() -> None:
    lists = json.loads(pinned("manuscript/prereg/2026-10-22_c_stage1/lists.json").read_text(encoding="utf-8"))
    ex = json.loads(pinned("manuscript/prereg/2026-10-21_dev_pools/exclusion.json").read_text(encoding="utf-8"))
    near60 = pinned("manuscript/prereg/2026-10-22_c_stage2/ov_test_dev299_neardup_files.txt").read_text(
        encoding="utf-8").split()
    ann = DATA / "datasets/openviic/uit-openviic-annotation-test.json"
    names = sorted(json.loads(ann.read_text(encoding="utf-8")))  # keys only
    rows = [(n, sha(DATA / "datasets/openviic/images" / n)) for n in names]
    shas = {h for _n, h in rows}
    by_sha: dict[str, list[str]] = {}
    for n, h in rows:
        by_sha.setdefault(h, []).append(n)
    pairs = {tuple(sorted(v)) for v in by_sha.values() if len(v) > 1}
    in_pairs = {n for p in pairs for n in p}
    s60 = set(near60)
    primary = [(n, h) for n, h in rows if n not in s60]

    check(len(names) == 2001 and len(set(names)) == 2001, f"2,001 names ({len(names)})")
    check(len(shas) == 1997, f"1,997 distinct sha256 ({len(shas)})")
    check(pairs == PAIRS, f"byte-identical pairs = CC-103's 4: {sorted(pairs)}")
    check(len(near60) == 60 and s60 <= set(names), "the 60-list lies inside the 2,001")
    check(not in_pairs & s60, "none of the 8 paired files is in the 60")
    check(len(primary) == 1941 and len({h for _n, h in primary}) == 1937,
          f"primary 1,941 entries / 1,937 distinct images ({len(primary)} / {len({h for _n, h in primary})})")
    check(TRUNCATED <= {n for n, _h in primary}, "the 3 truncated files are in the 1,941")
    check(set(names) <= set(lists["refuse"]["openviic_files"]), "every name is in refuse.openviic_files")
    check(shas <= set(lists["refuse"]["image_sha256"]), "every sha256 is in refuse.image_sha256")
    for s in ("ov_dev_a", "ov_dev_b", "xm_dev500", "xm_test2500"):
        rs = lists["sets"][s]
        check(not shas & {r[2] for r in rs} and not set(names) & {r[1] for r in rs}, f"0 overlap with {s}")
    for k, v in ex["image_sha256"].items():
        check(not shas & set(v), f"0 overlap with exclusion.json image_sha256.{k}")

    tsv = [f"{n}\t{h}" for n, h in rows]
    txt = [n for n, _h in primary]
    check([t.split("\t")[0] for t in tsv if t.split("\t")[0] not in s60] == txt, "1,941 = TSV order filtered")
    check(all(LINE.match(x) for x in tsv + txt), "every output line is name[<TAB>sha256] only")
    (OUT / "ov_test_files.tsv").write_text("\n".join(tsv) + "\n", encoding="utf-8")
    (OUT / "ov_test_primary1941.txt").write_text("\n".join(txt) + "\n", encoding="utf-8")
    for f in ("ov_test_files.tsv", "ov_test_primary1941.txt"):
        print(f"wrote {f} sha256 {sha(OUT / f)}")


if __name__ == "__main__":
    main()
