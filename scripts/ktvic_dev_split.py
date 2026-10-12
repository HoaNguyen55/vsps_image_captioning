#!/usr/bin/env python
"""KTVIC dev split for method tuning (judge D1, C1): 300 TRAIN images, random.Random(0).sample(sorted(ids), 300) over
the STRING image ids. data/splits/ktvic_dev300.txt is B2's out/dev300_train_ids.txt byte for byte (md5 pinned below);
the same rule on int ids gives a sample that shares only 31 of its 300 images. Runs tuned on dev hold it out.

    python scripts/ktvic_dev_split.py --verify [--sft $NCS_DATA/gold_p1dev/sft.jsonl] [--json-dir DIR]
    python scripts/ktvic_dev_split.py --write-complement     # data/splits/ktvic_train_minus_dev300.txt

--json-dir writes DIR/dev_data.json (the dev images with their train references) beside an `images` symlink, so that
`NCS_DATASET=<DIR's name> evaluate.py --split dev_data.json` scores the dev images exactly as test is scored.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate import KTVIC, references  # noqa: E402

SPLITS = ROOT / "data" / "splits"
DEV, REST = SPLITS / "ktvic_dev300.txt", SPLITS / "ktvic_train_minus_dev300.txt"
DEV_MD5 = "e1af906906175ee46aa7ad52600af893"  # research_r6/B2_targets_data/out/dev300_train_ids.txt


def ids(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").split()


def verify(train: set[str], sft: str | None) -> None:
    """Assert C1 and print each check (every 35_* job starts with this)."""
    dev, rest = ids(DEV), ids(REST)
    checks = {
        "dev file md5 == B2 dev300_train_ids.txt": hashlib.md5(DEV.read_bytes()).hexdigest() == DEV_MD5,
        "dev set == Random(0).sample(sorted(str ids), 300)": set(dev) == set(random.Random(0).sample(sorted(train), 300)),
        "300 distinct dev ids": len(dev) == len(set(dev)) == 300,
        "train-minus-dev & dev == empty": not set(rest) & set(dev),
        "train-minus-dev | dev == KTVIC train (3,769)": set(rest) | set(dev) == train and len(rest) == len(set(rest)),
    }
    if sft:
        rows = {json.loads(line)["image_id"] for line in Path(sft).read_text(encoding="utf-8").splitlines() if line}
        checks["SFT rows' images == train-minus-dev"] = rows == set(rest)
    for name, ok in checks.items():
        print(f"  {'ok  ' if ok else 'FAIL'} {name}")
    assert all(checks.values()), "dev split check failed (judge D1, C1)"


def write_dataset(d: Path) -> None:
    """dev_data.json in KTVIC's layout (train references of the dev images) and an `images` symlink."""
    keep = set(ids(DEV))
    data = json.loads((KTVIC / "train_data.json").read_text(encoding="utf-8"))
    sub = {"images": [im for im in data["images"] if str(im.get("id", im.get("image_id"))) in keep],
           "annotations": [a for a in data["annotations"] if str(a["image_id"]) in keep]}
    assert len(sub["images"]) == len(keep), len(sub["images"])
    d.mkdir(parents=True, exist_ok=True)
    (d / "dev_data.json").write_text(json.dumps(sub, ensure_ascii=False), encoding="utf-8")
    link = d / "images"
    if not link.exists():
        link.symlink_to(KTVIC / "images")
    assert link.resolve() == (KTVIC / "images").resolve(), link
    print(f"  {len(sub['images'])} images, {len(sub['annotations'])} references -> {d / 'dev_data.json'}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--sft", help="sft.jsonl whose images must be exactly train minus dev")
    ap.add_argument("--json-dir", help="write the dev images as an evaluate.py dataset here")
    ap.add_argument("--write-complement", action="store_true")
    args = ap.parse_args()
    assert KTVIC.name == "ktvic", f"NCS_DATASET={KTVIC.name}: the split is defined on KTVIC train"
    train = set(references("train_data.json"))
    if args.write_complement:
        REST.write_text("\n".join(sorted(train - set(ids(DEV)), key=int)) + "\n", encoding="utf-8")
    if args.verify or args.sft:
        verify(train, args.sft)
    if args.json_dir:
        write_dataset(Path(args.json_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
