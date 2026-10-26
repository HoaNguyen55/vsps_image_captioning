#!/usr/bin/env python
"""COCO instance classes for the full Karpathy test (5,000 images), by the block of scripts/crosslingual_gap.py that
wrote data/coco_probe/instance_gold.json (2,500 images), run over manifest_full5000.json. Same output format.
Asserts the 2,500 seed-42 ids reproduce the pinned file line for line. Run: python build_instance_gold_full5000.py OUT"""
import json
import sys
from pathlib import Path

ROOT = Path("/mnt/d/vsps_image_captioning")
manifest = json.loads((ROOT / "data/coco_probe/manifest_full5000.json").read_text("utf-8"))["images"]
inst = json.loads((ROOT / "data/datasets/coco_probe/annotations/instances_val2014.json").read_text("utf-8"))
files = {r["id"]: r["file_name"] for r in inst["images"]}
if any(files.get(m["cocoid"]) != m["filename"] for m in manifest):
    raise SystemExit("a manifest image is not in instances_val2014.json under its file name")
cat = {c["id"]: c["name"] for c in inst["categories"]}
gold: dict[int, set[str]] = {m["cocoid"]: set() for m in manifest}
for a in inst["annotations"]:
    if a["image_id"] in gold:
        gold[a["image_id"]].add(cat[a["category_id"]])
lines = {c: f'"{c}": {json.dumps({"coco2014": "val2014", "coco": sorted(g)})}' for c, g in sorted(gold.items())}
pinned = (ROOT / "data/coco_probe/instance_gold.json").read_text().strip().strip("{}").strip().split(",\n")
pinned = {int(l.split('"')[1]): l for l in pinned}
assert len(pinned) == 2500 and all(lines[c] == l for c, l in pinned.items()), "2,500 slice differs from pinned gold"
Path(sys.argv[1]).write_text("{\n" + ",\n".join(lines.values()) + "\n}\n", encoding="utf-8")
print(f"{len(gold)} images, {sum(map(len, gold.values())) / len(gold):.2f} classes/image; 2,500 slice identical")
