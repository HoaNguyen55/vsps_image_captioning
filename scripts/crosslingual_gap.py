#!/usr/bin/env python
"""Vietnamese vs English on the SAME images: every caption metric side by side, raw, normalised by the human
ceiling of its language, and the method effect fuse2 - P1, with paired bootstrap CIs (R5_02_CROSSLINGUAL.md).

    # datasets (CPU, seconds): $NCS_DATA/datasets/{uitviic_en,coco_en,coco_vi} + data/coco_probe/instance_gold.json
    NCS_DATA=data python scripts/crosslingual_gap.py build
    # n-gram + object metrics of the references (leave-one-out) and of every system of PREDS found (CPU)
    nice -n 19 taskset -c 12-15 python scripts/crosslingual_gap.py score --results $NCS_DATA/results --out xl_score.json
    # CLIP-S, RefCLIP-S, BERTScore with the same multilingual models for both languages (GPU, queue job)
    python scripts/crosslingual_gap.py embed --results $NCS_DATA/results --out xl_embed.json
    # tables: vi | en | vi - en; raw, normalised and Delta(fuse2 - P1); 95% CIs; any number of score/embed JSONs
    python scripts/crosslingual_gap.py report xl_score.json xl_embed.json --out xl_report.json

Parallel sets (SETS; both languages list the same images):
  uitviic_test, uitviic_val  UIT-ViIC test 231 / val 924 COCO images: its 5 Vietnamese captions, and the first 5 COCO
                             English captions of each image (Karpathy's dataset_coco.json) in uitviic_en; train too
  coco                       the 2,441 COCO Karpathy-test images of data/coco_probe/manifest.json not in UIT-ViIC
                             train: English references (coco_en); Vietnamese ones do not exist, coco_vi lists the
                             images only (evaluate.py captions it, scores nothing): compared on CLIP-S + instances
  xm3600                     the 600-image XM3600 subset of xm3600_oiv7.py build: first 2 captions per language
Images: uitviic_en/images -> ../uitviic/images, coco_{en,vi}/images -> ../coco_probe/val2014 (relative symlinks).
Systems (PREDS): zero-shot, P1, fuse2; P1 and fuse2 are trained on UIT-ViIC train in each language (52_*, 53_*).

Metrics per language: BLEU-1/4, METEOR, ROUGE-L, CIDEr-D (pycocoevalcap, x100) after evaluate.py's tokenization:
Vietnamese word-level (RDRSegmenter) and syllable-level (whitespace), both with punctuation kept, and pycocoevalcap's
PTB tokenizer (lowercased, punctuation removed) -- what English gets, also run on Vietnamese as a same-tokenizer
control; SPICE (English references only); object P/R/F1, CHAIR_i = 100 - P and CHAIR_s over the 80 COCO classes
(score_coco_probe: coco80_vi.json in Vietnamese, CHAIR's synonyms in English) against the classes the references
name and against the COCO instance labels; CLIP-S / RefCLIP-S (clip_score.py, MLAION xlm-roberta-large-ViT-H-14)
and BERTScore F (xlm-roberta-large, layer 17, no rescaling); caption length in tokens.

Human ceiling: each reference against the other k-1 (k = 5; XM3600 k = 2), averaged over the k folds. A system is
scored against all k references (raw, as evaluate.py) and against the k-1 of every fold; normalised = its fold score
/ the human ceiling of the same language (100 = one more human annotator). Delta = fuse2 - P1 within a language.
CIs: 95% percentile bootstrap over images, the same draws for both languages and every system, so vi - en and
Delta_vi - Delta_en are paired. METEOR is a corpus statistic of the METEOR jar: point estimate only.
METEOR is skipped for detailed captions (evaluate.py: they deadlock its pipe); SPICE is scored for the references
only (evaluate.py reports it for systems).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

DATA = Path(os.environ.get("NCS_DATA", Path.home() / "ncs-data"))
DATASETS = DATA / "datasets"
UIT_GOLD = ROOT / "data" / "uitviic" / "instance_gold.json"
COCO_GOLD = ROOT / "data" / "coco_probe" / "instance_gold.json"
MANIFEST = ROOT / "data" / "coco_probe" / "manifest.json"

#: parallel set -> (references per image, {language: (dataset under $NCS_DATA/datasets, split)}, COCO instance gold)
SETS = {
    "uitviic_test": (5, {"vi": ("uitviic", "test_data.json"), "en": ("uitviic_en", "test_data.json")}, UIT_GOLD),
    "uitviic_val": (5, {"vi": ("uitviic", "val_data.json"), "en": ("uitviic_en", "val_data.json")}, UIT_GOLD),
    "coco": (5, {"vi": ("coco_vi", "test_data.json"), "en": ("coco_en", "test_data.json")}, COCO_GOLD),
    "xm3600": (2, {"vi": ("xm3600", "test_data.json"), "en": ("xm3600_en", "test_data.json")}, None),
}
#: (set, language, system) -> predictions under --results; {m} = evaluate.py's prompt (short/detailed, + _en in
#: English); the comment names the queue job that writes them
PREDS = {
    ("uitviic_test", "vi", "zeroshot"): "uitviic/uitviic_zeroshot-{m}",                  # n2 38_uitviic_eval
    ("uitviic_test", "vi", "p1"): "uitviic_ind_test/uitviic_p1_s42-{m}",                 # n3 52_a
    ("uitviic_test", "vi", "fuse2"): "uitviic_ind_test/uitviic_fuse2_s42-{m}",           # n3 52_b
    ("uitviic_test", "en", "zeroshot"): "uitviic_en_ind_test/uitviic_en_zeroshot-{m}",   # n2 39_b
    ("uitviic_test", "en", "p1"): "uitviic_en_ind_test/uitviic_en_p1_s42-{m}",           # n3 53_a
    ("uitviic_test", "en", "fuse2"): "uitviic_en_ind_test/uitviic_en_fuse2_s42-{m}",     # n3 53_b
    ("uitviic_val", "vi", "zeroshot"): "uitviic_ind_val/uitviic_zeroshot-{m}",           # n2 39_b
    ("uitviic_val", "vi", "p1"): "uitviic_ind_val/uitviic_p1_s42-{m}",                   # n3 52_a
    ("uitviic_val", "vi", "fuse2"): "uitviic_ind_val/uitviic_fuse2_s42-{m}",             # n3 52_b
    ("uitviic_val", "en", "zeroshot"): "uitviic_en_ind_val/uitviic_en_zeroshot-{m}",     # n2 39_b
    ("uitviic_val", "en", "p1"): "uitviic_en_ind_val/uitviic_en_p1_s42-{m}",             # n3 53_a
    ("uitviic_val", "en", "fuse2"): "uitviic_en_ind_val/uitviic_en_fuse2_s42-{m}",       # n3 53_b
    ("coco", "vi", "zeroshot"): "coco_vi/coco_vi_zeroshot-{m}",                          # n2 39_b
    ("coco", "vi", "p1"): "coco_vi/uitviic_p1_s42-{m}",                                  # n3 53_c
    ("coco", "vi", "fuse2"): "coco_vi/uitviic_fuse2_s42-{m}",                            # n3 53_c
    ("coco", "en", "zeroshot"): "coco_en/coco_en_zeroshot-{m}",                          # n2 39_b
    ("coco", "en", "p1"): "coco_en/uitviic_en_p1_s42-{m}",                               # n3 53_a
    ("coco", "en", "fuse2"): "coco_en/uitviic_en_fuse2_s42-{m}",                         # n3 53_b
    ("xm3600", "vi", "zeroshot"): "xm3600/xm3600_zeroshot-{m}",                          # n2 39_xm3600_eval
    ("xm3600", "en", "zeroshot"): "xm3600_en/xm3600_en_zeroshot-{m}",                    # n2 39_b
}
SYSTEMS, MODES = ("zeroshot", "p1", "fuse2"), ("short", "detailed")
TOKS = {"vi": ("word", "syl", "ptb"), "en": ("ptb",)}
OBJ = ("P", "R", "F1", "CHAIR_i", "CHAIR_s")
#: report rows: (label, Vietnamese metric, English metric); None = no counterpart in that language
ROWS = ([(f"{m} (vi {t})", f"{m}@{tok}", f"{m}@ptb") for m in ("BLEU-1", "BLEU-4", "METEOR", "ROUGE-L", "CIDEr-D")
         for tok, t in (("word", "word"), ("syl", "syllable"), ("ptb", "PTB"))]
        + [("SPICE", None, "SPICE@ptb")]
        + [(f"{k} vs {what}", f"obj:{g}:{k}", f"obj:{g}:{k}") for g, what in (("ref", "references"), ("inst", "instances"))
           for k in OBJ]
        + [(m, m, m) for m in ("CLIP-S", "RefCLIP-S", "BERT-F")]
        + [(f"length (vi {t} / en PTB tokens)", f"len@{tok}", "len@ptb")
           for tok, t in (("word", "words"), ("syl", "syllables"), ("ptb", "PTB"))])


def held_out(xs: list, j: int) -> list:
    """xs without its j-th element: the references of fold j."""
    return xs[:j] + xs[j + 1:]


# ---------------------------------------------------------------- datasets
def _write(path: Path, images: list[dict], annotations: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"images": images, "annotations": annotations}, ensure_ascii=False, indent=1),
                    encoding="utf-8")
    print(f"  {path}: {len(images)} images, {len(annotations)} captions")


def _link(dataset: Path, target: Path) -> None:
    if not (dataset / "images").is_symlink():
        (dataset / "images").symlink_to(target, target_is_directory=True)


def cmd_build(args) -> None:
    from score_coco_probe import ANN, KARPATHY

    kar = {i["cocoid"]: i for i in json.loads(KARPATHY.read_text(encoding="utf-8"))["images"]}
    part = {int(i): v["coco2014"] for i, v in json.loads(UIT_GOLD.read_text(encoding="utf-8")).items()}

    def english(cocoid: int) -> list[dict]:
        """The first 5 COCO captions of an image, in Karpathy's order (324 images have 6 or 7)."""
        return [{"id": s["sentid"], "image_id": cocoid, "caption": s["raw"].strip()}
                for s in kar[cocoid]["sentences"][:5]]

    uit = DATASETS / "uitviic"
    for split in ("train", "val", "test"):
        data = json.loads((uit / f"{split}_data.json").read_text(encoding="utf-8"))
        for img in data["images"]:
            k = kar[img["id"]]
            # the same photograph: Karpathy's COCO-2014 file is UIT-ViIC's 2017-named one, in the COCO-2014 part
            # build_uitviic_gold.py matched (file name, size, flickr url, capture date)
            if k["filename"] != f"COCO_{k['filepath']}_{img['file_name']}" or k["filepath"] != part[img["id"]]:
                raise SystemExit(f"UIT-ViIC image {img['id']} is not Karpathy's {k['filename']}")
        _write(DATASETS / "uitviic_en" / f"{split}_data.json", data["images"],
               [a for img in data["images"] for a in english(img["id"])])
    _link(DATASETS / "uitviic_en", Path("..") / "uitviic" / "images")

    train = {img["id"] for img in json.loads((uit / "train_data.json").read_text(encoding="utf-8"))["images"]}
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))["images"]
    if any(kar[m["cocoid"]]["filename"] != m["filename"] for m in manifest):
        raise SystemExit("the coco_probe manifest disagrees with Karpathy's file names")
    keep = sorted(m["cocoid"] for m in manifest if m["cocoid"] not in train)
    images = [{"id": c, "file_name": kar[c]["filename"]} for c in keep]
    print(f"  coco: {len(manifest)} manifest images, {len(manifest) - len(keep)} in UIT-ViIC train dropped")
    _write(DATASETS / "coco_en" / "test_data.json", images, [a for c in keep for a in english(c)])
    _write(DATASETS / "coco_vi" / "test_data.json", images, [])
    for name in ("coco_en", "coco_vi"):
        _link(DATASETS / name, Path("..") / "coco_probe" / "val2014")

    # COCO instance classes of every manifest image, the shape of data/uitviic/instance_gold.json
    inst = json.loads((ANN / "instances_val2014.json").read_text(encoding="utf-8"))
    files = {r["id"]: r["file_name"] for r in inst["images"]}
    if any(files.get(m["cocoid"]) != m["filename"] for m in manifest):
        raise SystemExit("a manifest image is not in instances_val2014.json under its file name")
    cat = {c["id"]: c["name"] for c in inst["categories"]}
    gold: dict[int, set[str]] = {m["cocoid"]: set() for m in manifest}
    for a in inst["annotations"]:
        if a["image_id"] in gold:
            gold[a["image_id"]].add(cat[a["category_id"]])
    COCO_GOLD.write_text("{\n" + ",\n".join(f'"{c}": {json.dumps({"coco2014": "val2014", "coco": sorted(g)})}'
                                             for c, g in sorted(gold.items())) + "\n}\n", encoding="utf-8")
    print(f"  {COCO_GOLD}: {len(gold)} images, {sum(map(len, gold.values())) / len(gold):.2f} classes/image")


# ---------------------------------------------------------------- inputs
def load_set(name: str) -> tuple[list[str], dict[str, dict], dict[str, set[str]] | None]:
    """(image ids, {language: {"refs": {id: first k captions} or {} without captions, "files", "dir"}},
    {id: COCO instance classes} or None) of a parallel set; both languages must list the same images."""
    k, langs, gold_file = SETS[name]
    out = {}
    for lang, (dataset, split) in langs.items():
        d = json.loads((DATASETS / dataset / split).read_text(encoding="utf-8"))
        files = {str(i["id"]): i.get("file_name") or i.get("filename") for i in d["images"]}
        refs: dict[str, list[str]] = {}
        for a in d["annotations"]:
            if (a.get("caption") or "").strip():
                refs.setdefault(str(a["image_id"]), []).append(a["caption"].strip())
        if refs:
            short = sorted(i for i in files if len(refs.get(i, [])) < k)
            if short:
                raise SystemExit(f"{dataset}/{split}: {len(short)} images with fewer than {k} captions ({short[:3]})")
            refs = {i: refs[i][:k] for i in files}
        out[lang] = {"refs": refs, "files": files, "dir": DATASETS / dataset}
    ids = sorted(out["vi"]["files"])
    if ids != sorted(out["en"]["files"]):
        raise SystemExit(f"{name}: the Vietnamese and English splits list different images")
    gold = None
    if gold_file:
        g = json.loads(gold_file.read_text(encoding="utf-8"))
        gold = {i: set(g[i]["coco"]) for i in ids}
    return ids, out, gold


def systems_of(results: Path, name: str, lang: str, ids: list[str]) -> dict[str, dict[str, str]]:
    """{"system/mode": {id: caption}} for every PREDS file of this set and language present under `results`."""
    found = {}
    for system in SYSTEMS:
        rel = PREDS.get((name, lang, system))
        for mode in MODES if rel else ():
            f = results / (rel.format(m=mode if lang == "vi" else f"{mode}_en") + ".preds.json")
            if not f.exists():
                continue
            raw = json.loads(f.read_text(encoding="utf-8"))
            caps = {str(i): (v[0] if isinstance(v, list) else v) or "" for i, v in raw.items()}
            missing = [i for i in ids if i not in caps]
            if missing:
                raise SystemExit(f"{f}: no caption for {len(missing)} of {len(ids)} images (no subset scoring)")
            found[f"{system}/{mode}"] = {i: caps[i] for i in ids}
    return found


def matcher(lang: str):
    """Caption -> the COCO-80 classes it names: coco80_vi.json in Vietnamese, CHAIR's synonyms in English."""
    import score_coco_probe as sc

    if lang == "vi":
        terms = sc.load_vi_terms()
        return lambda c: sc.vi_classes(c, terms)
    syn = sc.load_synonyms()
    return lambda c: sc.en_classes(c, syn)


def obj_row(m: set[str], g: set[str]) -> list:
    """[true classes, mentioned classes, recall or None]: object_prf.image_counts in the flat 80-class space."""
    return [len(m & g), len(m), len(m & g) / len(g) if g else None]


# ---------------------------------------------------------------- n-gram metrics (CPU)
def tokenize(tok: str, sentences) -> dict[str, str]:
    """{sentence: tokens} as evaluate.py tokenizes: `word` RDRSegmenter, `syl` whitespace (lowercased, punctuation
    kept), `ptb` pycocoevalcap's PTB tokenizer (lowercased, punctuation removed)."""
    sents = sorted(set(sentences))
    if tok == "ptb":
        from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer

        out = PTBTokenizer().tokenize({str(n): [{"caption": s}] for n, s in enumerate(sents)})
        return {s: out[str(n)][0] for n, s in enumerate(sents)}
    if tok == "word":
        from rescap.metrics import _rdrsegmenter

        segment = _rdrsegmenter()[0]
    else:
        segment = lambda t: t  # noqa: E731
    return {s: segment(s.strip()).lower() for s in sents}


def bleu_stats(hyp: str, refs: list[str]) -> list[float]:
    """pycocoevalcap's per-image BLEU statistics: test length, closest reference length, guesses and correct n-grams."""
    from pycocoevalcap.bleu.bleu_scorer import cook_refs, cook_test

    c = cook_test(hyp, cook_refs(refs))
    reflen = min((abs(r - c["testlen"]), r) for r in c["reflen"])[1]
    return [c["testlen"], reflen, *c["guess"], *c["correct"]]


def bleu_from(s) -> tuple:
    """Corpus BLEU-1 and BLEU-4 (x100) from summed bleu_stats (scalars, or arrays of one value per bootstrap draw):
    pycocoevalcap's BleuScorer arithmetic with `closest` reference lengths."""
    import numpy as np

    s = [np.asarray(x, float) for x in s]
    tiny, small = 1e-15, 1e-9
    acc, bleus = 1.0, []
    for k in range(4):
        acc = acc * (s[6 + k] + tiny) / (s[2 + k] + small)
        bleus.append(acc ** (1 / (k + 1)))
    bp = np.exp(1 - 1 / np.minimum((s[0] + tiny) / (s[1] + small), 1.0))  # brevity penalty, 1 when not too short
    return 100 * bleus[0] * bp, 100 * bleus[3] * bp


def ngram_run(gts: dict[str, list[str]], res: dict[str, str], meteor: bool, spice: bool) -> dict:
    """One pycocoevalcap run on tokenized text, per image where the corpus score is a mean (x100)."""
    from pycocoevalcap.bleu.bleu import Bleu
    from pycocoevalcap.cider.cider import Cider
    from pycocoevalcap.rouge.rouge import Rouge

    ids = list(gts)
    one = {i: [res[i]] for i in ids}
    out = {"bleu": [bleu_stats(res[i], gts[i]) for i in ids],
           "ROUGE-L": [100 * float(x) for x in Rouge().compute_score(gts, one)[1]],
           "CIDEr-D": [100 * float(x) for x in Cider().compute_score(gts, one)[1]]}
    corpus = Bleu(4).compute_score(gts, one, verbose=0)[0]
    mine = bleu_from([sum(c) for c in zip(*out["bleu"])])
    if abs(mine[0] - 100 * corpus[0]) > 1e-6 or abs(mine[1] - 100 * corpus[3]) > 1e-6:
        raise SystemExit(f"BLEU from per-image statistics {mine} != pycocoevalcap {corpus}")
    if meteor:
        from pycocoevalcap.meteor.meteor import Meteor

        scorer = Meteor()
        out["METEOR"] = 100 * scorer.compute_score(gts, one)[0]
        del scorer  # its JVM
    if spice:
        from pycocoevalcap.spice.spice import Spice

        from rescap.metrics import _java, legacy_java_home

        if ids != sorted(ids):
            raise SystemExit("SPICE returns images in sorted order")
        with _java(legacy_java_home()):
            out["SPICE"] = [100 * s["All"]["f"] for s in Spice().compute_score(gts, one)[1]]
    return out


def fold_stats(runs: list[dict], tok: str) -> dict:
    """Runs of the k folds (or the one all-reference run) -> stats: BLEU keeps per-fold statistics, the per-image
    metrics are averaged over folds (the fold mean of a corpus mean), METEOR is a point."""
    out = {f"BLEU@{tok}": {"bleu": [r["bleu"] for r in runs]}}
    for m in ("ROUGE-L", "CIDEr-D", "SPICE"):
        if m in runs[0]:
            out[f"{m}@{tok}"] = {"mean": [round(sum(v) / len(v), 4) for v in zip(*(r[m] for r in runs))]}
    if "METEOR" in runs[0]:
        out[f"METEOR@{tok}"] = {"point": sum(r["METEOR"] for r in runs) / len(runs)}
    return out


def score_language(ids, refs, gold, lang, systems, human: bool) -> dict:
    match = matcher(lang)
    k = len(refs[ids[0]]) if refs else 0
    sentences = {c for cs in refs.values() for c in cs} | {c for caps in systems.values() for c in caps.values()}
    named = {s: match(s) for s in sentences}

    def ref_gold(i, skip=None):
        return set().union(*(named[r] for j, r in enumerate(refs[i]) if j != skip))

    out = {key: {"std": {}, "fold": {}} for key in systems}
    if human and refs:
        h = out["human"] = {"fold": {"obj:ref": {"obj": [[obj_row(named[refs[i][j]], ref_gold(i, j)) for i in ids]
                                                         for j in range(k)]}}}
        if gold:
            h["fold"]["obj:inst"] = {"obj": [[obj_row(named[refs[i][j]], gold[i]) for i in ids] for j in range(k)]}
    for key, caps in systems.items():
        std, fold = out[key]["std"], out[key]["fold"]
        if refs:
            std["obj:ref"] = {"obj": [[obj_row(named[caps[i]], ref_gold(i)) for i in ids]]}
            fold["obj:ref"] = {"obj": [[obj_row(named[caps[i]], ref_gold(i, j)) for i in ids] for j in range(k)]}
        if gold:
            std["obj:inst"] = fold["obj:inst"] = {"obj": [[obj_row(named[caps[i]], gold[i]) for i in ids]]}

    for tok in TOKS[lang]:
        t = tokenize(tok, sentences)
        if "human" in out:
            out["human"]["fold"][f"len@{tok}"] = {"mean": [sum(len(t[r].split()) for r in refs[i]) / k for i in ids]}
            runs = [ngram_run({i: [t[r] for r in held_out(refs[i], j)] for i in ids}, {i: t[refs[i][j]] for i in ids},
                              meteor=True, spice=lang == "en") for j in range(k)]
            out["human"]["fold"].update(fold_stats(runs, tok))
        for key, caps in systems.items():
            res = {i: t[caps[i]] for i in ids}
            out[key]["std"][f"len@{tok}"] = out[key]["fold"][f"len@{tok}"] = {"mean": [len(res[i].split()) for i in ids]}
            if not refs:
                continue
            meteor = key.endswith("/short")  # detailed captions deadlock pycocoevalcap's METEOR pipe (evaluate.py)
            out[key]["std"].update(fold_stats([ngram_run({i: [t[r] for r in refs[i]] for i in ids}, res, meteor, False)],
                                              tok))
            out[key]["fold"].update(fold_stats([ngram_run({i: [t[r] for r in held_out(refs[i], j)] for i in ids}, res,
                                                          meteor, False) for j in range(k)], tok))
        print(f"    {lang} {tok}: done", flush=True)
    return out


def cmd_score(args) -> None:
    out = {}
    for name in args.sets:
        ids, langs, gold = load_set(name)
        entry = out[name] = {"ids": ids, "k": SETS[name][0]}
        for lang, d in langs.items():
            systems = systems_of(Path(args.results), name, lang, ids)
            print(f"{name}/{lang}: {len(ids)} images, {'k=' + str(SETS[name][0]) if d['refs'] else 'no'} references, "
                  f"systems: {', '.join(sorted(systems)) or 'none'}", flush=True)
            entry[lang] = score_language(ids, d["refs"], gold, lang, systems, not args.skip_human)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out), encoding="utf-8")
    print(f"wrote {args.out}")


# ---------------------------------------------------------------- embedding metrics (GPU)
def cmd_embed(args) -> None:
    import torch
    from bert_score import BERTScorer
    from clip_score import Clip, clip_s, ref_clip_s

    device = "cuda" if torch.cuda.is_available() else "cpu"
    clip, bert = Clip(device), BERTScorer(model_type="xlm-roberta-large", device=device)
    out = {}
    for name in args.sets:
        ids, langs, _ = load_set(name)
        k, n = SETS[name][0], len(ids)
        en = langs["en"]
        img = clip.images([en["dir"] / "images" / en["files"][i] for i in ids])  # the same photographs for vi and en
        entry = out[name] = {"ids": ids, "k": k}
        for lang, d in langs.items():
            refs, src = d["refs"], {}
            entry[lang] = src
            if refs:
                emb = clip.text([r for i in ids for r in refs[i]]).view(n, k, -1)
                cos_img = (emb @ img[:, :, None]).squeeze(-1).tolist()          # [n][k]
                cos_ref = (emb @ emb.transpose(1, 2)).tolist()                    # [n][k][k]
                pairs = [(a, j, l) for a in range(n) for j in range(k) for l in range(k) if j != l]
                f = iter(bert.score([refs[ids[a]][j] for a, j, _ in pairs], [refs[ids[a]][l] for a, _, l in pairs])[2]
                         .tolist())
                bf = [[[next(f) if j != l else None for l in range(k)] for j in range(k)] for _ in range(n)]
                src["human"] = {"fold": {
                    "CLIP-S": {"mean": [sum(clip_s(c) for c in cos_img[a]) / k for a in range(n)]},
                    "RefCLIP-S": {"mean": [sum(ref_clip_s(cos_img[a][j], held_out(cos_ref[a][j], j)) for j in range(k)) / k
                                           for a in range(n)]},
                    "BERT-F": {"mean": [sum(max(held_out(bf[a][j], j)) for j in range(k)) / k for a in range(n)]}}}
            for key, caps in systems_of(Path(args.results), name, lang, ids).items():
                c_emb = clip.text([caps[i] for i in ids])
                cos_c = (c_emb * img).sum(-1).tolist()
                cs = {"mean": [clip_s(c) for c in cos_c]}
                std, fold = {"CLIP-S": cs}, {"CLIP-S": cs}
                if refs:
                    cos_cr = (emb @ c_emb[:, :, None]).squeeze(-1).tolist()        # [n][k]
                    bc = bert.score([caps[i] for i in ids for _ in range(k)], [r for i in ids for r in refs[i]])[2]
                    bc = bc.view(n, k).tolist()
                    std["RefCLIP-S"] = {"mean": [ref_clip_s(cos_c[a], cos_cr[a]) for a in range(n)]}
                    fold["RefCLIP-S"] = {"mean": [sum(ref_clip_s(cos_c[a], held_out(cos_cr[a], j)) for j in range(k)) / k
                                                  for a in range(n)]}
                    std["BERT-F"] = {"mean": [max(bc[a]) for a in range(n)]}
                    fold["BERT-F"] = {"mean": [sum(max(held_out(bc[a], j)) for j in range(k)) / k for a in range(n)]}
                src[key] = {"std": std, "fold": fold}
            print(f"{name}/{lang}: {', '.join(sorted(src)) or 'nothing to embed'}", flush=True)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out), encoding="utf-8")
    print(f"wrote {args.out}")


# ---------------------------------------------------------------- report
def merge(into: dict, more: dict) -> dict:
    """Deep merge of score/embed JSONs; a set's image order must agree."""
    for key, v in more.items():
        if key == "ids" and "ids" in into and into["ids"] != v:
            raise SystemExit("two inputs order the images of a set differently")
        if isinstance(v, dict) and isinstance(into.get(key), dict):
            merge(into[key], v)
        else:
            into[key] = v
    return into


def values(name: str, stat: dict, w) -> dict:
    """{metric: array over the rows of w}: the stat on images weighted by w (row 0 = all once, then bootstrap draws)."""
    import numpy as np

    if "mean" in stat:
        v = np.array(stat["mean"], float)
        ok = ~np.isnan(v)
        return {name: (w @ np.where(ok, v, 0.0)) / (w @ ok)}
    if "point" in stat:
        return {name: np.r_[stat["point"], np.full(len(w) - 1, np.nan)]}
    if "bleu" in stat:
        b = [bleu_from((w @ np.array(fold, float)).T) for fold in stat["bleu"]]
        return {name.replace("BLEU", "BLEU-1"): np.mean([x[0] for x in b], 0),
                name.replace("BLEU", "BLEU-4"): np.mean([x[1] for x in b], 0)}
    per_fold = []
    for fold in stat["obj"]:
        a = np.array(fold, float)
        tp, m, r = w @ a[:, 0], w @ a[:, 1], a[:, 2]
        has = ~np.isnan(r)
        p = 100 * np.divide(tp, m, out=np.zeros_like(tp), where=m > 0)
        n_has = w @ has
        rec = 100 * np.divide(w @ np.where(has, r, 0.0), n_has, out=np.zeros_like(tp), where=n_has > 0)
        f1 = np.divide(2 * p * rec, p + rec, out=np.zeros_like(tp), where=(p + rec) > 0)
        per_fold.append((p, rec, f1, 100 - p, 100 * (w @ (a[:, 1] > a[:, 0])) / w.sum(1)))
    return {f"{name}:{k}": np.mean([f[n] for f in per_fold], 0) for n, k in enumerate(OBJ)}


def expand(source: dict, w) -> dict:
    """{"std"/"fold": {metric: array}} of one system (or the human references) of one language."""
    return {variant: {m: v for name, stat in stats.items() for m, v in values(name, stat, w).items()}
            for variant, stats in source.items()}


def ci(a) -> list:
    """[point, 2.5%, 97.5%] of one metric; no interval for a point statistic."""
    import numpy as np

    draws = a[1:][~np.isnan(a[1:])]
    lo, hi = (np.percentile(draws, [2.5, 97.5]) if len(draws) else (float("nan"), float("nan")))
    return [float(a[0]), float(lo), float(hi)]


def side_by_side(vi: dict, en: dict, rows=ROWS) -> dict:
    """{label: {"vi", "en", "vi-en"}} with CIs, for the rows both languages have (or the one that has it)."""
    out = {}
    for label, kv, ke in rows:
        a, b = vi.get(kv) if kv else None, en.get(ke) if ke else None
        if a is None and b is None:
            continue
        cell = {}
        if a is not None:
            cell["vi"] = ci(a)
        if b is not None:
            cell["en"] = ci(b)
        if a is not None and b is not None:
            cell["vi-en"] = ci(a - b)
        out[label] = cell
    return out


def cmd_report(args) -> None:
    import numpy as np

    data = {}
    for f in args.inputs:
        merge(data, json.loads(Path(f).read_text(encoding="utf-8")))
    report = {}
    for name, entry in data.items():
        ids = entry["ids"]
        rng = np.random.default_rng(args.seed)
        draws = rng.integers(0, len(ids), (args.B, len(ids)))
        w = np.vstack([np.ones(len(ids))] + [np.bincount(d, minlength=len(ids)) for d in draws])
        # (language, "human" or "system/mode", "std"/"fold") -> {metric: values}; a key is absent when nothing was
        # scored for it (no such system in the inputs, or no references: coco_vi)
        cells = {(L, src, variant): m for L in ("vi", "en") for src, stats in entry.get(L, {}).items()
                 for variant, m in expand(stats, w).items()}

        def at(L, src, variant):
            return cells.get((L, src, variant), {})

        human = {L: at(L, "human", "fold") for L in ("vi", "en")}
        rep = report[name] = {"n_images": len(ids), "k": entry["k"], "B": args.B,
                              "human": side_by_side(human["vi"], human["en"]), "systems": {}, "delta": {}}

        def norm(L, src):
            """fold score / human ceiling of the language, x100 (100 = one more annotator)."""
            return {m: 100 * v / human[L][m] for m, v in at(L, src, "fold").items() if m in human[L]}

        for system in SYSTEMS:
            for mode in MODES:
                src = f"{system}/{mode}"
                if not at("vi", src, "std") and not at("en", src, "std"):
                    continue
                rep["systems"][src] = {"raw": side_by_side(at("vi", src, "std"), at("en", src, "std")),
                                       "normalised": side_by_side(norm("vi", src), norm("en", src))}
        for mode in MODES:
            p1, f2 = f"p1/{mode}", f"fuse2/{mode}"
            if not all(at(L, s, "std") for s in (p1, f2) for L in ("vi", "en")):
                continue
            raw = {L: {m: v - at(L, p1, "std")[m] for m, v in at(L, f2, "std").items() if m in at(L, p1, "std")}
                   for L in ("vi", "en")}
            nrm = {L: {m: v - norm(L, p1)[m] for m, v in norm(L, f2).items() if m in norm(L, p1)} for L in ("vi", "en")}
            rep["delta"][mode] = {"raw": side_by_side(raw["vi"], raw["en"]),
                                  "normalised": side_by_side(nrm["vi"], nrm["en"])}
    if args.out:
        Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"wrote {args.out}\n")
    print(markdown(report))


def fmt(cell: list | None, d: int) -> str:
    if cell is None:
        return "–"
    p, lo, hi = cell
    return f"{p:.{d}f}" + (f" [{lo:.{d}f}, {hi:.{d}f}]" if lo == lo else "")


def table(title: str, rows: dict) -> list[str]:
    out = [f"\n**{title}**\n", "| metric | vi | en | vi − en |", "|---|---|---|---|"]
    for label, c in rows.items():
        d = 3 if max(abs(c[L][0]) for L in ("vi", "en") if L in c) < 5 else 1  # CLIP-S / BERT-F scale
        out.append(f"| {label} | " + " | ".join(fmt(c.get(L), d) for L in ("vi", "en", "vi-en")) + " |")
    return out


def markdown(report: dict) -> str:
    lines = []
    for name, rep in report.items():
        lines.append(f"\n### {name} — {rep['n_images']} images, k = {rep['k']} references per language, "
                     f"95% paired bootstrap CI (B = {rep['B']})")
        lines += table("human ceiling (each reference vs the other k−1)", rep["human"])
        for src, r in rep["systems"].items():
            lines += table(f"{src} — raw (all k references)", r["raw"])
            lines += table(f"{src} — normalised, % of the human ceiling (same folds)", r["normalised"])
        for mode, r in rep["delta"].items():
            lines += table(f"Δ = fuse2 − P1, {mode} — raw", r["raw"])
            lines += table(f"Δ = fuse2 − P1, {mode} — normalised (points of the human ceiling)", r["normalised"])
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help="uitviic_en, coco_en, coco_vi under $NCS_DATA/datasets; COCO instance gold")
    for cmd in ("score", "embed"):
        p = sub.add_parser(cmd)
        p.add_argument("--results", default=str(DATA / "results"), help="root of the PREDS paths")
        p.add_argument("--sets", nargs="+", default=list(SETS), choices=list(SETS))
        p.add_argument("--out", required=True)
    sub.choices["score"].add_argument("--skip-human", action="store_true",
                                      help="systems only (the reference leave-one-out runs are in another JSON)")
    r = sub.add_parser("report")
    r.add_argument("inputs", nargs="+", help="score/embed JSONs, merged")
    r.add_argument("--B", type=int, default=1000)
    r.add_argument("--seed", type=int, default=0)
    r.add_argument("--out", default=None)
    args = ap.parse_args()
    {"build": cmd_build, "score": cmd_score, "embed": cmd_embed, "report": cmd_report}[args.cmd](args)
    return 0


def _check() -> None:
    import numpy as np

    from object_prf import scores

    assert held_out([1, 2, 3], 1) == [1, 3] and held_out(["a", "b"], 0) == ["b"]
    assert obj_row({"person", "dog"}, {"person", "car"}) == [1, 2, 0.5] and obj_row({"dog"}, set()) == [0, 1, None]
    # identical hypothesis and reference: BLEU 100; a 2-word hypothesis vs a 4-word reference: brevity penalty
    same = [4, 4, 4, 3, 2, 1, 4, 3, 2, 1]
    assert all(abs(b - 100) < 1e-6 for b in bleu_from(same))
    b1, _ = bleu_from([2, 4, 2, 1, 0, 0, 2, 1, 0, 0])
    assert abs(b1 - 100 * math.exp(1 - 2)) < 1e-6
    assert ROWS[0] == ("BLEU-1 (vi word)", "BLEU-1@word", "BLEU-1@ptb") and ("SPICE", None, "SPICE@ptb") in ROWS
    assert PREDS[("coco", "en", "p1")].format(m="short_en") == "coco_en/uitviic_en_p1_s42-short_en"
    w = np.array([[1, 1, 1], [3, 0, 0]], float)
    v = values("x", {"mean": [1.0, None, 3.0]}, w)["x"]
    assert v.tolist() == [2.0, 1.0], v
    o = values("o", {"obj": [[[1, 2, 0.5], [0, 1, None], [2, 2, 1.0]]]}, w)
    assert np.allclose([o[f"o:{k}"][0] for k in OBJ], [60.0, 75.0, 2 * 60 * 75 / 135, 40.0, 200 / 3]), o
    # object_prf.scores on the same rows (exact match only: no hierarchy)
    nan = float("nan")
    s = scores([(1, 2, 1, 0.5, 0.5, 0.5), (0, 1, 0, nan, nan, nan), (2, 2, 2, 1.0, 1.0, 1.0)])
    assert np.allclose([s["P"], s["R"], s["F1"]], [o[f"o:{k}"][0] for k in ("P", "R", "F1")])
    stats = [[4, 4, 4, 3, 2, 1, 4, 3, 2, 1], [2, 4, 2, 1, 0, 0, 2, 1, 0, 0]]
    got = values("BLEU@ptb", {"bleu": [stats]}, np.array([[1.0, 1.0], [2.0, 0.0]]))
    assert abs(got["BLEU-4@ptb"][1] - 100) < 1e-6 and abs(got["BLEU-1@ptb"][0] - bleu_from([6, 8, 6, 4, 2, 1, 6, 4, 2, 1])[0]) < 1e-9
    assert ci(np.array([5.0, 4.0, 6.0, np.nan]))[0] == 5.0 and math.isnan(ci(np.array([1.0, np.nan]))[1])


if __name__ == "__main__":
    _check()
    sys.exit(main())
