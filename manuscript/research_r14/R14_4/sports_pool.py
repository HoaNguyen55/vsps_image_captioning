"""Count leak-free COCO Karpathy train/restval images whose English captions name a UIT-ViIC sport (translate-train pool)."""
import json, re
D = "/mnt/d/vsps_image_captioning/data/datasets/"
uit = set()
for s in ("train", "val", "test"):
    uit |= {im["id"] for im in json.load(open(D + f"uitviic/{s}_data.json"))["images"]}
uit_eval = set()
for s in ("val", "test"):
    uit_eval |= {im["id"] for im in json.load(open(D + f"uitviic/{s}_data.json"))["images"]}
probe = {im["id"] for im in json.load(open(D + "coco_vi/test_data.json"))["images"]}
d = json.load(open(D + "karpathy/dataset_coco.json"))["images"]
sport = re.compile(r"\b(tennis|baseball|softball|skateboard\w*|surf\w*|ski(s|er|ers|ing)?|snowboard\w*|frisbee|soccer|kite\w*|football|volleyball|racket|racquet|bat|batter)\b")
pool = [im for im in d if im["split"] in ("train", "restval") and im["cocoid"] not in uit_eval and im["cocoid"] not in probe
        and sum(bool(sport.search(s["raw"].lower())) for s in im["sentences"]) >= 3]
print("karpathy train+restval", sum(im["split"] in ("train", "restval") for im in d),
      "sports pool (>=3 of 5 captions)", len(pool), "of which already UIT-ViIC train", sum(im["cocoid"] in uit for im in pool),
      "UIT-ViIC val/test ids", len(uit_eval), "probe ids", len(probe))
