#!/usr/bin/env python3
"""Paper C test (CC-103 W14): pin Paper A's 108 three-reference images of XM-test2500, CPU, local.

  NCS_DATA=data python3 scripts/c_test/make_xm_threeref108.py

The rule is scripts/e_stage1/e_lists.py:102 (images with >= 3 Vietnamese references), counting annotation rows per
image_id only; no caption is read. Writes xm_test2500_threeref108.txt: image ids only, sorted. Nothing is written
unless every check passes.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(os.environ.get("NCS_DATA", ROOT / "data"))
OUT = ROOT / "manuscript/prereg/2026-10-25_c_test/xm_test2500_threeref108.txt"
LISTS = ("manuscript/prereg/2026-10-22_c_stage1/lists.json",
         "5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371")  # LISTS_ADDENDUM
ESPLIT = ("manuscript/prereg/2026-10-22_e_stage1/e_split.json",
          "795652f1af45597b3a89f8a937056a1810504d54e1e41319198b3fb27fea2ef9")  # E stage-1 SHA256SUMS


def load(pin: tuple[str, str]) -> dict:
    p = ROOT / pin[0]
    if hashlib.sha256(p.read_bytes()).hexdigest() != pin[1]:
        raise SystemExit(f"pin mismatch: {pin[0]}")
    return json.loads(p.read_text(encoding="utf-8"))


def check(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"CHECK FAILED, nothing written: {msg}")
    print(f"ok  {msg}")


def main() -> None:
    lists, esplit = load(LISTS), load(ESPLIT)
    full = json.loads((DATA / "datasets/xm3600/full_data.json").read_text(encoding="utf-8"))
    n_caps = Counter(str(a["image_id"]) for a in full["annotations"])  # e_lists.py:101, counts only
    three = {i for i, n in n_caps.items() if n >= 3}  # e_lists.py:102
    test = {r[0] for r in lists["sets"]["xm_test2500"]}
    ids = sorted(three & test)
    check(len(three) == esplit["counts"]["paperA_n2_three_ref_images"] == 150, f"150 three-ref images ({len(three)})")
    check(len(ids) == esplit["counts"]["paperA_n2_three_ref_in"]["xm_test2500"] == 108, f"108 in XM-test2500 ({len(ids)})")
    check(set(ids) <= test, "subset of lists.json sets.xm_test2500")
    check(all(re.fullmatch(r"[0-9a-f]{16}", i) for i in ids), "every line is a 16-hex image id only")
    OUT.write_text("\n".join(ids) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name} sha256 {hashlib.sha256(OUT.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
