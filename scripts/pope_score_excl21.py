#!/usr/bin/env python3
"""POPE-500 scores with the 21 UIT-ViIC train images excluded (decision CC-005), reusing scripts/pope_vi.py.

python pope_score_excl21.py --repo /root/vsps --data-dir $NCS_DATA/datasets/pope \
    --uitviic-train $NCS_DATA/datasets/uitviic/train_data.json --out OUT.json <name>-<lang>.jsonl ...
Same questions, labels (POPE and RePOPE), parse() and metrics() as `pope_vi.py --score`; the only change is that
questions on the excluded images are dropped. The excluded ids are recomputed (UIT-ViIC train ids x POPE images)
and must equal the 21 recorded for CC-005. --all-images keeps all 500 (validation against pope_vi --score only).
Refuses to overwrite OUT.json.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

CC005_IDS = [15738, 45685, 124629, 155131, 198397, 199122, 298633, 327532, 333756, 363908, 365317, 405762, 419453,
             429913, 468169, 468997, 482829, 485564, 499105, 501898, 524979]


def coco_id(fname):
    return int(fname.rsplit("_", 1)[-1].split(".")[0])


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="/root/vsps")
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--uitviic-train", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--all-images", action="store_true")
    ap.add_argument("jsonl", nargs="+")
    a = ap.parse_args()
    if Path(a.out).exists():
        raise SystemExit(f"{a.out} exists: results are never overwritten")
    sys.path.insert(0, str(Path(a.repo) / "scripts"))
    import pope_vi as pv
    from coco_probe import read_jsonl

    data_dir = Path(a.data_dir)
    qs = {s: pv.load(data_dir, "pope", s) for s in pv.SPLITS}
    images = {q["image"] for s in pv.SPLITS for q in qs[s]}
    train_ids = {int(im["id"]) for im in json.loads(Path(a.uitviic_train).read_text(encoding="utf-8"))["images"]}
    excl = sorted(train_ids & {coco_id(i) for i in images})
    assert len(images) == 500 and excl == CC005_IDS, (len(images), excl)
    keep = images if a.all_images else {i for i in images if coco_id(i) not in set(excl)}
    labels = {"POPE": {s: {q["question_id"]: q["label"] for q in qs[s]} for s in pv.SPLITS},
              "RePOPE": {s: {q["question_id"]: q["label"] for q in pv.load(data_dir, "repope", s)} for s in pv.SPLITS}}
    rows = []
    for f in map(Path, a.jsonl):
        name, lang = f.stem.rsplit("-", 1)
        reply = {(r["image"], r["object"]): pv.parse(r["answer"]) for r in read_jsonl(f)}
        for split in pv.SPLITS:
            for which, lab in labels.items():
                asked = [((q["image"], pv.obj_of(q["text"])), lab[split][q["question_id"]])
                         for q in qs[split] if q["question_id"] in lab[split] and q["image"] in keep]
                pairs = [(reply[k], label) for k, label in asked if k in reply]
                rows.append({"system": name, "lang": lang, "split": split, "labels": which,
                             "missing": len(asked) - len(pairs), **pv.metrics(pairs)})
    out = {"rule": "CC-005: POPE-500 for UIT-ViIC-trained adapters excludes the UIT-ViIC train images",
           "excluded_coco_ids": [] if a.all_images else excl, "n_images_total": len(images), "n_images_scored": len(keep),
           "inputs_sha256": {str(f): sha(f) for f in a.jsonl}, "pope_vi_sha256": sha(Path(a.repo) / "scripts/pope_vi.py"),
           "scorer_sha256": sha(__file__), "sources": pv.URLS, "prompts": pv.PROMPTS, "max_new_tokens": pv.MAX_NEW,
           "parse": "pope_vi.parse (first word, else negation, else có/there is; unparsed left out)", "rows": rows}
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {a.out}: {len(rows)} rows, {len(keep)} images scored, {len(out['excluded_coco_ids'])} excluded")


if __name__ == "__main__":
    main()
