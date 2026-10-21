#!/usr/bin/env python3
"""Build the dev-pool manifests and the exclusion list of manuscript/prereg/2026-10-21_dev_pools (PD-31).

    python scripts/dev_pools/build_lists.py KTVIC_SHA XM3600_SHA UITVIIC_SHA
Each argument is a "sha256  file" list of that dataset's image folder (sha256sum output); UITVIIC_SHA comes from M3
(the UIT-ViIC images are downloaded there from COCO). Reads ids, file names and image hashes only, never a caption;
from data/ktvic_openviic_refs.json it reads only the match records (_pairs), not the OpenViIC captions.
"""
import hashlib, json, re, sys
KT, XM, UV = sys.argv[1:4]
OUT = "manuscript/prereg/2026-10-21_dev_pools"
def shalist(path):  # "sha  file" lines
    return {l.split()[1]: l.split()[0] for l in open(path) if l.strip()}
kt_img = shalist(KT)
xm_img = shalist(XM)
uv_img = shalist(UV)
cv_img = shalist("data/coco_probe/cv295_val2014.sha256")
ch_img = shalist("data/coco_probe/chair500_val2014.sha256")
tst = [l.rstrip("\n").split("\t") for l in open("data/lb/sets/ktvic_test.tsv")]
uvj = {s: json.load(open(f"data/datasets/uitviic/{s}_data.json"))["images"] for s in ("train", "val", "test")}
xm = json.load(open("data/datasets/xm3600/test_data.json"))["images"]
coco = {
    "uitviic_test": sorted(int(i["id"]) for i in uvj["test"]),
    "cv295": sorted(int(x) for x in open("data/coco_probe/probe_val2017_ids.txt").read().split()),
    "coco2500": sorted(int(i["cocoid"]) for i in json.load(open("data/coco_probe/manifest.json"))["images"]),
    "coco_karpathy_test": sorted(int(i["cocoid"]) for i in json.load(open("data/coco_probe/manifest_full5000.json"))["images"]),
    "chair500": sorted(int(x) for x in open("data/coco_probe/chair500_ids.txt").read().split()),
    "pope500": sorted({int(re.search(r"(\d+)\.jpg", json.loads(l)["image"]).group(1)) for l in open("data/results/pope_vi/zeroshot-vi.jsonl")}),
}
# KTVIC dev300 near-duplicates of KTVIC test: a dev image and a test image matched to the same OpenViIC file
pairs = json.load(open("data/ktvic_openviic_refs.json"))["_pairs"]
ok = lambda r: min(r[2], r[3]) <= 10 and r[4] >= 0.5
test_files = {r[0] for v in pairs["test"].values() for r in v if ok(r)}
dev = sorted(open("data/splits/ktvic_dev300.txt").read().split())
near = sorted(i for i in dev if any(ok(r) and r[0] in test_files for r in pairs["train"].get(i, [])))
ex_sha = {"ktvic_test": sorted({r[2] for r in tst}), "xm3600_all_images": sorted(set(xm_img.values())),
          "cv295": sorted(set(cv_img.values())), "chair500": sorted(set(ch_img.values())),
          "uitviic_test": sorted({uv_img[i["file_name"]] for i in uvj["test"]})}
exclusion = {"schema": "vsps.dev_pools_exclusion.v1",
             "rule": "an image is refused if its id is listed for its namespace or its sha256 is listed under image_sha256",
             "ids": {"ktvic": {"ktvic_test": sorted(r[0] for r in tst), "ktvic_dev_near_duplicate_of_test": near},
                     "coco": coco, "xm3600": {"xm600_test_data_json": sorted(str(i["id"]) for i in xm)}},
             "image_sha256": ex_sha,
             "sources": {p: hashlib.sha256(open(p, "rb").read()).hexdigest() for p in (
                 "data/lb/sets/ktvic_test.tsv", "data/datasets/uitviic/test_data.json", "data/coco_probe/probe_val2017_ids.txt",
                 "data/coco_probe/manifest.json", "data/coco_probe/manifest_full5000.json", "data/coco_probe/chair500_ids.txt",
                 "data/results/pope_vi/zeroshot-vi.jsonl", "data/datasets/xm3600/test_data.json",
                 "data/coco_probe/cv295_val2014.sha256", "data/coco_probe/chair500_val2014.sha256",
                 "data/ktvic_openviic_refs.json", "data/splits/ktvic_dev300.txt")}}
open(f"{OUT}/exclusion.json", "w").write(json.dumps(exclusion, indent=1) + "\n")
names = {str(i["id"]): i["filename"] for i in json.load(open("data/datasets/ktvic/train_data.json"))["images"]}
d299 = [i for i in dev if i not in near]
open(f"{OUT}/ktvic_dev299.tsv", "w").write("".join(f"{i}\t{names[i]}\t{kt_img[names[i]]}\n" for i in d299))
allsha = {h for v in ex_sha.values() for h in v}
val = sorted(uvj["val"], key=lambda i: int(i["id"]))
xid = {x for v in coco.values() for x in v}
val_ok = [i for i in val if int(i["id"]) not in xid and uv_img[i["file_name"]] not in allsha]
open(f"{OUT}/uitviic_val.tsv", "w").write("".join(f"{i['id']}\t{i['file_name']}\t{uv_img[i['file_name']]}\n" for i in val_ok))
print("near-dup", near, "dev299", len(d299), "val", len(val), "val kept", len(val_ok),
      "dev sha hits", len({kt_img[names[i]] for i in dev} & allsha))
