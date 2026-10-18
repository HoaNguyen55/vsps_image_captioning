"""UIT-ViIC: reference-based hallucinations vs COCO instance labels (human presence evidence)."""
import json, os, sys
from pathlib import Path
ROOT = Path("/mnt/d/vsps_image_captioning")
os.environ["NCS_DATA"] = str(ROOT / "data"); os.environ["NCS_DATASET"] = "uitviic"
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from evaluate import references
from rescap.chair import _ancestors, _gold_objects, canonical, objects_in
coco = json.loads((ROOT / "data/coco_probe/coco80_vi.json").read_text())
COCO_ALL = set().union(*[set(objects_in(p)) for k, v in coco.items() if not k.startswith("_") and isinstance(v, list) for p in v])
COCO_ALL = {p for k, v in coco.items() if not k.startswith("_") and isinstance(v, list) for p in v if objects_in(p) == [p]}
print("strict COCO lexicon classes:", len(COCO_ALL))
from collections import Counter
inst = json.loads((ROOT / "data/uitviic/instance_gold.json").read_text())
refs = references("test_data.json")
for sysname in ("uitviic_p1_s43", "uitviic_fuse2_s42"):
    preds = json.loads((ROOT / f"data/results/uitviic/{sysname}-short.preds.json").read_text())
    TOP = Counter()
    M = H = Hc = Hc_inst = 0
    for i, cap in preds.items():
        cap = cap[0] if isinstance(cap, list) else cap
        gold = _gold_objects(refs[str(i)])
        ig = set().union(*[_ancestors(canonical(v) or v) for x in inst.get(str(i), {}).get("vi", []) for v in objects_in(x)]) if str(i) in inst else None
        for x in dict.fromkeys(canonical(n) or n for n in objects_in(cap)):
            M += 1
            if x in gold: continue
            H += 1
            if x in COCO_ALL and ig is not None:
                Hc += 1; Hc_inst += x in ig; TOP[(x, x in ig)] += 1
    print(sysname, dict(M=M, H=H, CHAIR_i=round(H / M, 3), H_coco=Hc, H_coco_instance_present=Hc_inst,
                        H_coco_absent=Hc - Hc_inst, removable_share_of_H=round((Hc - Hc_inst) / H, 3)), TOP.most_common(10))
