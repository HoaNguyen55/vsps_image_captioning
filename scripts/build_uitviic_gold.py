#!/usr/bin/env python
"""Instance gold for UIT-ViIC: the COCO-2014 classes present in each image, named in Vietnamese.

    NCS_DATA=data python scripts/build_uitviic_gold.py      # -> data/uitviic/instance_gold.json

UIT-ViIC v1.0 (Lam et al., ICCCI 2020; 3,850 COCO ball-sport images x 5 human
Vietnamese captions, published "for researching purpose") comes from the UIT NLP
lab page https://sites.google.com/uit.edu.vn/uit-nlp/datasets as
https://drive.google.com/file/d/1YexKrE6o0UiJhFWpE8M5LKoe6-k3AiM4/view
(UIT-ViIC-20200417T021508Z-001.zip, sha256
7a00b84c7fe8418cbcfcea6ce749a0e57e1b9962a0859c88a074ef639d14e087). Its
uitviic_captions_{train,val,test}2017.json are $NCS_DATA/datasets/uitviic/
{train,val,test}_data.json unchanged, and images/ holds each image fetched from
its `coco_url`.

The release's `id` is the COCO image id. Every image is checked against its
COCO-2014 record (file name, size, flickr_url, capture date) before its instances
are used, so a wrong id fails here instead of producing a plausible gold set.
Gold = the 80-class COCO categories with at least one instance (crowd regions
included, as in score_coco_probe.py); `vi` is each class's first coco80_vi.json name.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from score_coco_probe import ANN, NCS_DATA, PROBE_DATA  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SAME = ("width", "height", "flickr_url", "date_captured")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", default=str(NCS_DATA / "datasets" / "uitviic"))
    ap.add_argument("--out", default=str(ROOT / "data" / "uitviic" / "instance_gold.json"))
    args = ap.parse_args()

    images = {}
    for split in ("train_data.json", "val_data.json", "test_data.json"):
        for img in json.loads((Path(args.dataset) / split).read_text(encoding="utf-8"))["images"]:
            images[img["id"]] = img
    vi = {c: t[0] for c, t in json.loads((PROBE_DATA / "coco80_vi.json").read_text(encoding="utf-8")).items()
          if not c.startswith("_")}

    part_of: dict[int, str] = {}
    gold: dict[int, set[str]] = defaultdict(set)
    for part in ("train2014", "val2014"):
        inst = json.loads((ANN / f"instances_{part}.json").read_text())
        cat = {c["id"]: c["name"] for c in inst["categories"]}
        for rec in inst["images"]:
            ours = images.get(rec["id"])
            if ours is None:
                continue
            differ = [k for k in SAME if rec[k] != ours[k]]
            if differ or rec["file_name"] != f"COCO_{part}_{ours['file_name']}":
                raise SystemExit(f"image {rec['id']}: COCO-2014 record differs ({differ or 'file_name'})")
            part_of[rec["id"]] = part
        for a in inst["annotations"]:
            if a["image_id"] in images:
                gold[a["image_id"]].add(cat[a["category_id"]])
    missing = sorted(images.keys() - part_of.keys())
    if missing:
        raise SystemExit(f"{len(missing)} UIT-ViIC images are not in COCO-2014 (e.g. {missing[:3]})")

    rows = {str(i): {"coco2014": part_of[i], "coco": sorted(gold[i]), "vi": [vi[c] for c in sorted(gold[i])]}
            for i in sorted(images)}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("{\n" + ",\n".join(f"{json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}"
                                       for k, v in rows.items()) + "\n}\n", encoding="utf-8")
    freq = Counter(c for v in rows.values() for c in v["coco"])
    print(f"{len(rows)} images ({dict(Counter(part_of.values()))}), {sum(not v['coco'] for v in rows.values())} "
          f"without instances, {sum(freq.values()) / len(rows):.2f} classes/image; top: {freq.most_common(8)}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
