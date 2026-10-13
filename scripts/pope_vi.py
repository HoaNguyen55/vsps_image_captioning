#!/usr/bin/env python
"""POPE-COCO (random / popular / adversarial) asked in Vietnamese and in English, scored under
the original POPE labels and under RePOPE's corrected ones.

    python scripts/pope_vi.py --fetch       # question/label files at pinned commits + images.json
    python scripts/download_coco_images.py --manifest $NCS_DATA/datasets/pope/images.json --out IMAGES
    python scripts/pope_vi.py --images-dir IMAGES --out-dir $NCS_DATA/results/pope_vi            # zero-shot
    python scripts/pope_vi.py --images-dir IMAGES --out-dir ... --adapter $NCS_DATA/runs/p1_s43 --name p1_s43
    python scripts/pope_vi.py --score --out-dir $NCS_DATA/results/pope_vi   # every <name>-<lang>.jsonl there

Sources, pinned in URLS: POPE (Li et al., EMNLP 2023), RUCAIBox/POPE@109985c, and RePOPE
(Neuhaus & Hein, arXiv 2504.15707), YanNeu/RePOPE@127ad0f: the same questions with 139 'yes'
relabelled 'no', 5/39/33 'no' relabelled 'yes' and 226/273/316 ambiguous ones dropped
(random/popular/adversarial). The splits share their 1,500 'yes' questions, so each distinct
(image, object) is asked once per language: 5,127 questions on 500 val2014 images.

vi: "Trong ảnh có {name} không? Trả lời có hoặc không." with the first coco80_vi.json term of
the class; en: POPE's own question + " Answer yes or no.". Model loading is coco_probe.py's
(bf16, merged adapter, 256-1024 vision tokens); greedy, at most 10 new tokens.
parse(): the first word decides when it is có/không or yes/no; else a negation in the first
sentence means no (POPE's own rule) and an existential có / "there is" means yes; anything else
is unparsed, reported, and left out of the metrics, as RePOPE's evaluation code does. Metrics
take 'yes' as the positive class: accuracy, precision, recall, F1 and yes-ratio (%).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from coco_probe import BACKBONES, DEFAULT, read_jsonl  # noqa: E402
from score_coco_probe import NCS_DATA, PROBE_DATA  # noqa: E402

SPLITS = ("random", "popular", "adversarial")
URLS = {
    "pope": "https://raw.githubusercontent.com/RUCAIBox/POPE/109985c74a00a88ba5341f9b0c1d4900f2a1f789"
            "/output/coco/coco_pope_{split}.json",
    "repope": "https://raw.githubusercontent.com/YanNeu/RePOPE/127ad0fa5a2b46d32fc8718e7126727dcc61a117"
              "/annotations/coco_repope_{split}.json",
}
PROMPTS = {"vi": "Trong ảnh có {name} không? Trả lời có hoặc không.", "en": "{question} Answer yes or no."}
MAX_NEW = 10
YES = {"có", "vâng", "đúng", "yes", "yeah", "yep"}
NO = {"không", "chẳng", "chả", "no", "not", "none", "nope"}


def obj_of(question: str) -> str:
    """'Is there a dining table in the image?' -> 'dining table'."""
    return re.fullmatch(r"Is there an? (.+) in the image\?", question).group(1)


def vi_names() -> dict[str, str]:
    d = json.loads((PROBE_DATA / "coco80_vi.json").read_text(encoding="utf-8"))
    return {cls: terms[0] for cls, terms in d.items() if not cls.startswith("_")}


def load(data_dir: Path, which: str, split: str) -> list[dict]:
    path = data_dir / f"{which}_{split}.json"
    if not path.exists():
        raise SystemExit(f"{path} is missing: run --fetch first")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def fetch(data_dir: Path) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    for which, url in URLS.items():
        for split in SPLITS:
            dst, src = data_dir / f"{which}_{split}.json", url.format(split=split)
            if not dst.exists():
                urllib.request.urlretrieve(src, dst.with_suffix(".part"))
                dst.with_suffix(".part").rename(dst)
            print(f"  {dst.name} <- {src}")
    qs = [q for split in SPLITS for q in load(data_dir, "pope", split)]
    names = vi_names()
    unnamed = {obj_of(q["text"]) for q in qs} - names.keys()
    if unnamed:
        raise SystemExit(f"coco80_vi.json has no name for {sorted(unnamed)}")
    images = sorted({q["image"] for q in qs})
    (data_dir / "images.json").write_text(json.dumps({"images": [{"filename": i} for i in images]}, indent=1))
    asked = {(q["image"], obj_of(q["text"])) for q in qs}
    print(f"  {len(qs)} questions, {len(asked)} distinct, {len(images)} images -> {data_dir / 'images.json'}")
    print("  vi names: " + ", ".join(f"{o}={names[o]}" for o in sorted({o for _, o in asked})))


def parse(answer: str) -> str | None:
    """'yes', 'no' or None (unparsed) from a free-form Vietnamese or English reply."""
    text = unicodedata.normalize("NFC", answer).lower().replace("n't", " not")
    first = re.split(r"[.!?\n]", text, maxsplit=1)[0]
    words = re.findall(r"[a-zà-ỹ]+", first)
    if words and words[0] in YES | NO:
        return "yes" if words[0] in YES else "no"
    if NO & set(words):
        return "no"
    if YES & set(words) or re.search(r"\bthere(?:'s| is| are)\b", first):
        return "yes"
    return None


def metrics(pairs: list[tuple[str | None, str]]) -> dict[str, float]:
    """Over (parsed reply, label) pairs; unparsed replies are counted, then left out."""
    got = [(p, lab) for p, lab in pairs if p]
    tp = sum(p == lab == "yes" for p, lab in got)
    fp = sum(p == "yes" != lab for p, lab in got)
    tn = sum(p == lab == "no" for p, lab in got)
    fn = sum(p == "no" != lab for p, lab in got)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    n = len(got)
    return {"n": len(pairs), "unparsed": len(pairs) - n, "acc": 100 * (tp + tn) / n if n else 0.0,
            "P": 100 * prec, "R": 100 * rec, "F1": 200 * prec * rec / (prec + rec) if prec + rec else 0.0,
            "yes": 100 * (tp + fp) / n if n else 0.0}


def run(args) -> None:
    from PIL import Image

    from coco_probe import generate, load_model

    names = vi_names()
    asked = {(q["image"], obj_of(q["text"])): q["text"]
             for split in SPLITS for q in load(Path(args.data_dir), "pope", split)}
    keys = sorted(asked)[: args.limit or None]
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    model, processor = load_model(args.adapter, args.model, args.weights)
    for lang in args.langs.split(","):
        out = out_dir / f"{args.name}-{lang}.jsonl"
        done = {(r["image"], r["object"]) for r in read_jsonl(out, repair=True)}
        todo = [k for k in keys if k not in done]
        print(f"[{args.name}/{lang}] {len(done)} already answered, {len(todo)} to ask", flush=True)
        t0 = time.time()
        with out.open("a", encoding="utf-8") as fh:
            for k, (img, obj) in enumerate(todo, 1):
                prompt = PROMPTS[lang].format(name=names[obj], question=asked[img, obj])
                image = Image.open(Path(args.images_dir) / img).convert("RGB")
                answer = generate(model, processor, image, prompt, MAX_NEW)
                fh.write(json.dumps({"image": img, "object": obj, "prompt": prompt, "answer": answer},
                                    ensure_ascii=False) + "\n")
                fh.flush()
                if k % 500 == 0:
                    rate = (time.time() - t0) / k
                    print(f"  {k}/{len(todo)} · {rate:.2f}s/question · ~{rate*(len(todo)-k)/60:.0f} min left", flush=True)
        print(f"[{args.name}/{lang}] DONE -> {out}", flush=True)


def score(data_dir: Path, out_dir: Path) -> None:
    qs = {split: load(data_dir, "pope", split) for split in SPLITS}
    labels = {"POPE": {s: {q["question_id"]: q["label"] for q in qs[s]} for s in SPLITS},
              "RePOPE": {s: {q["question_id"]: q["label"] for q in load(data_dir, "repope", s)} for s in SPLITS}}
    print("POPE-COCO (500 val2014 images) -- % over parsed replies, 'yes' = positive; "
          "RePOPE = corrected labels, ambiguous questions dropped")
    print(f"  {'system':20s} {'lang':4s} {'split':11s} {'labels':6s} {'n':>5s} {'unparsed':>8s} {'missing':>7s}"
          f"  {'Acc':>5s} {'P':>5s} {'R':>5s} {'F1':>5s} {'yes':>5s}")
    rows = []
    for f in sorted(out_dir.glob("*-*.jsonl")):
        name, lang = f.stem.rsplit("-", 1)
        reply = {(r["image"], r["object"]): parse(r["answer"]) for r in read_jsonl(f)}
        for split in SPLITS:
            for which, lab in labels.items():
                asked = [((q["image"], obj_of(q["text"])), lab[split][q["question_id"]])
                         for q in qs[split] if q["question_id"] in lab[split]]
                pairs = [(reply[k], label) for k, label in asked if k in reply]
                m = {"system": name, "lang": lang, "split": split, "labels": which,
                     "missing": len(asked) - len(pairs), **metrics(pairs)}
                rows.append(m)
                print(f"  {name:20s} {lang:4s} {split:11s} {which:6s} {m['n']:5d} {m['unparsed']:8d} {m['missing']:7d}"
                      f"  {m['acc']:5.1f} {m['P']:5.1f} {m['R']:5.1f} {m['F1']:5.1f} {m['yes']:5.1f}")
    out = out_dir / "scores.json"
    out.write_text(json.dumps({"sources": URLS, "prompts": PROMPTS, "max_new_tokens": MAX_NEW,
                               "parse": "first word, else negation, else có/there is; unparsed left out",
                               "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", default=str(NCS_DATA / "datasets" / "pope"))
    ap.add_argument("--fetch", action="store_true", help="download the question/label files, write images.json")
    ap.add_argument("--score", action="store_true", help="score every <name>-<lang>.jsonl in --out-dir")
    ap.add_argument("--images-dir", help="val2014 images (download_coco_images.py)")
    ap.add_argument("--out-dir")
    ap.add_argument("--adapter", default=None, help="leave empty = zero-shot")
    ap.add_argument("--name", default=None, help="output file stem; required with --adapter or non-default --model")
    ap.add_argument("--model", default=DEFAULT, choices=sorted(BACKBONES))
    ap.add_argument("--weights", default=None, help="local pinned snapshot of --model (default: its hub id)")
    ap.add_argument("--langs", default="vi,en")
    ap.add_argument("--limit", type=int, default=0, help="first N distinct questions only (smoke tests)")
    args = ap.parse_args()
    if args.fetch:
        fetch(Path(args.data_dir))
        return 0
    if not args.out_dir:
        ap.error("--out-dir is required")
    if args.score:
        score(Path(args.data_dir), Path(args.out_dir))
        return 0
    if not args.images_dir or ((args.adapter or args.model != DEFAULT) and not args.name):
        ap.error("generation needs --images-dir, and --name with --adapter or non-default --model")
    args.name = args.name or "zeroshot"
    run(args)
    return 0


def _check() -> None:
    assert DEFAULT == "qwen2.5-vl-7b" and "qwen3-vl-8b" in BACKBONES and len(vi_names()) == 80
    for reply, want in (("Có.", "yes"), ("Không.", "no"), ("KHÔNG", "no"), ("Không có.", "no"),
                        ("Có, trong ảnh có một con chó.", "yes"), ("Trong ảnh không có ô tô.", "no"),
                        ("Trong ảnh có một chiếc ô tô màu đỏ.", "yes"), ("Yes, there is a dog.", "yes"),
                        ("No.", "no"), ("There is no car in the image.", "no"), ("There isn't a car.", "no"),
                        ("There's a car.", "yes"), ("Một người đàn ông đang đi xe đạp.", None), ("", None)):
        assert parse(reply) == want, (reply, parse(reply))
    assert obj_of("Is there an traffic light in the image?") == "traffic light"
    m = metrics([("yes", "yes"), ("yes", "no"), ("no", "no"), ("no", "yes"), (None, "yes")])
    assert (m["n"], m["unparsed"], m["acc"], m["P"], m["R"], m["yes"]) == (5, 1, 50.0, 50.0, 50.0, 50.0), m


if __name__ == "__main__":
    _check()
    sys.exit(main())
