#!/usr/bin/env python3
"""C-CONF, laptop, hashing only (coordinator decision I1, 2026-11-18): the sha256 of record of the KTVIC images of the
near-copy list owners of §5.1 (iii) that have no register cache (the ViHal pool, survivors and removed list; KTVIC
dev300; registration 18e61111 l.146). Block 0 compares every featurised owner image with this list and stops (G0) on a
missing or differing row (c_conf_arms.record_check; l.454: "The host checks the sha256 of record of every file before
use.").

Reads: the four id lists through the pinned c_conf_lists.ktvic_owner_ids (each at its sha256 in c_conf_lists.INPUTS);
data/datasets/ktvic/train_data.json at 72ee9b57 for its "images" ids and file names only; lists.json at 5c479f03 for
refuse.image_sha256 (a sha256 list, counted only); the bytes of the listed KTVIC training images. Every id must be a
KTVIC training id, checked by id before any image is opened, so no KTVIC test image is read; the KTVIC test annotation
is never opened. No decode, no model, no feature. Prints counts only.
    python3 -I -B scripts/c_conf/c_conf_ktvic_hash.py      # writes scripts/c_conf/c_conf_ktvic_owner_images.sha256 once
Output lines: "<sha256>  <KTVIC file name>", sorted by file name.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import c_conf_lists as CLB  # noqa: E402  pinned order builder (c774f1a4): ktvic_owner_ids, read_checked, INPUTS

ID_OWNERS = ("vihal_pool", "vihal_survivors", "vihal_removed", "ktvic_dev300")  # = c_conf_arms.ID_OWNERS
TRAIN = "data/datasets/ktvic/train_data.json"
PINS = {TRAIN: "72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f"}
IMAGES = CLB.ROOT / "data/datasets/ktvic/images"
OUT = HERE / "c_conf_ktvic_owner_images.sha256"


def main() -> None:
    if OUT.exists():
        raise SystemExit(f"{OUT.name} exists; written once")
    lists = {k: v for k, v in CLB.ktvic_owner_ids(CLB.ROOT, CLB.INPUTS).items() if k in ID_OWNERS}
    ids = sorted(set().union(*lists.values()))
    name = {str(r["id"]): r["filename"] for r in json.loads(CLB.read_checked(CLB.ROOT, TRAIN, PINS))["images"]}
    outside = [i for i in ids if i not in name]
    if outside:
        raise SystemExit(f"STOP: {len(outside)} ids are not KTVIC training ids; nothing was hashed")
    refused = set(json.loads(CLB.read_checked(CLB.ROOT, CLB.LISTS, CLB.INPUTS))["refuse"]["image_sha256"])
    rows = sorted((name[i], hashlib.sha256((IMAGES / name[i]).read_bytes()).hexdigest()) for i in ids)
    with open(OUT, "x", encoding="utf-8") as f:
        f.writelines(f"{h}  {n}\n" for n, h in rows)
    print(json.dumps({"ids": len(ids), "per_list": {k: len(v) for k, v in lists.items()}, "files": len(rows),
                      "sha256_in_lists_refuse": sum(h in refused for _n, h in rows),
                      "out_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
