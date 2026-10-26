#!/usr/bin/env python
"""Sec 5 COCO (Karpathy test) EN exchangeability row on the full test: the per-image lists that
c1_b1_b6_reproduction.run_b2 builds from data/datasets/coco_en/test_data.json (crosslingual_gap.py cmd_build: manifest
images not in UIT-ViIC train, first 5 Karpathy captions, en_classes), rebuilt for a chosen manifest, then
adjacency_check.summarize unchanged. Gate: manifest.json must reproduce the frozen 2,441-image row.
Run: python exch_full.py OUT_JSON"""
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path("/mnt/d/vsps_image_captioning")
sys.path[:0] = [str(ROOT / ".session_backup/2026-10-14/r11_litmaps/L2/scripts"), str(ROOT), str(ROOT / "scripts")]
import adjacency_check as adj  # noqa: E402

syn = adj.sc.load_synonyms()
kar = {i["cocoid"]: i for i in json.loads((ROOT / "data/datasets/karpathy/dataset_coco.json").read_text())["images"]}
train = {i["id"] for i in json.loads((ROOT / "data/datasets/uitviic/train_data.json").read_text())["images"]}


def per_image(manifest):
    keep = sorted(m["cocoid"] for m in json.loads((ROOT / "data/coco_probe" / manifest).read_text())["images"]
                  if m["cocoid"] not in train)
    return keep, [[adj.sc.en_classes(s["raw"].strip(), syn) for s in sorted(kar[c]["sentences"][:5], key=lambda s: s["sentid"])]
                  for c in keep]


frozen = json.loads((ROOT / ".session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json").read_text())
frozen = frozen["B2_L2_exchangeability"]["datasets"]["coco_en_test_coco80"]
out = {}
for man in ("manifest.json", "manifest_full5000.json", "manifest_rest2500.json"):
    keep, sets = per_image(man)
    with redirect_stdout(io.StringIO()):
        out[man] = adj.summarize("coco_en_test_coco80", sets)
    out[man]["n_kept"] = len(keep)
assert json.loads(json.dumps({k: out["manifest.json"][k] for k in frozen}, default=float)) == frozen, "gate: 2,441-image row not reproduced"
Path(sys.argv[1]).write_text(json.dumps(out, indent=1, default=str) + "\n")
for m, r in out.items():
    print(m, r["n_kept"], r.get("adjacent_share"), r.get("adjacent_share_ci95"), r.get("jac_lag1_minus_mean_lag2to4"), r.get("jac_diff_ci95"))
