#!/usr/bin/env python
"""Object-level precision, recall, and F1 over unique classes per image (Table IV).

    python scripts/object_prf.py                       # KTVIC test split, all *.preds.json in data/results
    python scripts/object_prf.py --coco-preds data/results/coco5000   # add the COCO-2014 block

Definitions (Section IV-C of the paper): with M_i the set of object classes mentioned
in the caption of image i and G_i its gold classes, precision = sum|M_i & G_i| / sum|M_i|,
recall = mean over images with non-empty G_i of |M_i & G_i| / |G_i|, F1 = harmonic mean.
KTVIC uses the same 113-entry object lexicon and reference-derived gold as CHAIR-vi;
COCO uses the frozen instance-plus-reference gold of score_coco_probe.py. Because the
sets count unique classes rather than mentions, precision is close to but not identical
to 1 - CHAIR_i.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))


def prf(tp: int, mentions: int, recalls: list[float]) -> tuple[float, float, float]:
    p = tp / mentions if mentions else 0.0
    r = statistics.mean(recalls) if recalls else 0.0
    f = 2 * p * r / (p + r) if (p + r) else 0.0
    return 100 * p, 100 * r, 100 * f


def _specific(gold: set[str], ancestors) -> set[str]:
    """Gold pruned to its most specific classes: `người` goes when `phụ nữ` is there."""
    return {g for g in gold if not any(g != o and g in ancestors(o) for o in gold)}


def image_counts(m: set[str], g: set[str], ancestors) -> tuple[int, int, int, float, float, float]:
    """(exact tp, |M|, hypernym-credited tp, R_exact, R_spec, R_vague) for one image; nan R when no gold.

    The hypernym rule is the one CHAIR-vi already uses: a mention is correct when
    it is a gold class or an ancestor of one. R_spec counts a specific gold class
    only when it is named exactly; R_vague also credits naming one of its ancestors.
    """
    g_h = set().union(*[ancestors(x) for x in g]) if g else set()
    spec = _specific(g, ancestors)
    r_spec = sum(x in m for x in spec) / len(spec) if spec else float("nan")
    r_vague = sum(bool(ancestors(x) & m) for x in spec) / len(spec) if spec else float("nan")
    r_exact = len(m & g) / len(g) if g else float("nan")
    return len(m & g), len(m), len(m & g_h), r_exact, r_spec, r_vague


def scores(rows: list[tuple]) -> dict[str, float]:
    tp = sum(r[0] for r in rows); n = sum(r[1] for r in rows); tph = sum(r[2] for r in rows)
    has_gold = [r for r in rows if r[3] == r[3]]
    out = {}
    out["P"], out["R"], out["F1"] = prf(tp, n, [r[3] for r in has_gold])
    out["P_h"], out["R_spec"], out["F1_spec"] = prf(tph, n, [r[4] for r in has_gold])
    _, out["R_vague"], out["F1_vague"] = prf(tph, n, [r[5] for r in has_gold])
    return out


def bootstrap(rows: list[tuple], keys=("F1", "F1_spec", "F1_vague"), n: int = 1000, seed: int = 0):
    """95% percentile CI over images resampled with replacement."""
    import random
    rng = random.Random(seed)
    draws = {k: [] for k in keys}
    for _ in range(n):
        s = scores([rows[rng.randrange(len(rows))] for _ in rows])
        for k in keys:
            draws[k].append(s[k])
    return {k: (sorted(v)[int(0.025 * n)], sorted(v)[int(0.975 * n) - 1]) for k, v in draws.items()}


def ktvic_block(results_dir: Path, split: str, ci: bool = False) -> None:
    from evaluate import references
    from rescap.chair import _ancestors, objects_in

    refs = references(split)
    gold = {str(k): set().union(*[set(objects_in(r)) for r in rs]) for k, rs in refs.items()}
    print(f"KTVIC ({split}, {len(gold)} images) -- object precision / recall / F1 (%)")
    print("  exact match | CHAIR-vi hypernym rule: P_h, R_spec (F1), R_vague (F1)")
    for f in sorted(results_dir.glob("*-detailed.preds.json")):
        preds = json.loads(f.read_text(encoding="utf-8"))
        preds = {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in preds.items()}
        rows = []
        for k, cap in preds.items():
            m, g = set(objects_in(cap)), gold.get(k, set())
            rows.append(image_counts(m, g, _ancestors))
        s = scores(rows)
        tp = sum(r[0] for r in rows)
        name = f.name.removesuffix("-detailed.preds.json")
        line = (f"  {name:26s} true/cap={tp/len(preds):.2f}  P={s['P']:5.1f}  R={s['R']:5.1f}  F1={s['F1']:5.1f}"
                f" | P_h={s['P_h']:5.1f}  R_spec={s['R_spec']:5.1f} ({s['F1_spec']:5.1f})"
                f"  R_vague={s['R_vague']:5.1f} ({s['F1_vague']:5.1f})")
        if ci:
            line += "  CI95 " + " ".join(f"{k}=[{a:.1f},{b:.1f}]" for k, (a, b) in bootstrap(rows).items())
        print(line)


def coco_block(preds_dir: Path, manifest: Path) -> None:
    import score_coco_probe as sc

    syn = sc.load_synonyms()
    vi_terms = sc.load_vi_terms()
    want = {i["cocoid"] for i in json.loads(manifest.read_text(encoding="utf-8"))["images"]}
    inst = json.loads((sc.ANN / "instances_val2014.json").read_text())
    cat = {c["id"]: c["name"] for c in inst["categories"]}
    gold_inst: dict[int, set[str]] = defaultdict(set)
    for a in inst["annotations"]:
        if a["image_id"] in want:
            gold_inst[a["image_id"]].add(cat[a["category_id"]])
    gold_ref: dict[int, set[str]] = defaultdict(set)
    for img in json.loads(sc.KARPATHY.read_text())["images"]:
        if img["cocoid"] in want:
            for s in img["sentences"]:
                gold_ref[img["cocoid"]] |= sc.en_classes(s["raw"], syn)
    gold = {i: gold_inst[i] | gold_ref[i] for i in want}
    print(f"\nCOCO-2014 ({len(want)} images, instance + reference gold) -- object precision / recall / F1 (%)")
    for system in ("zeroshot", "distill"):
        rows: dict[int, str] = {}
        for f in sorted(preds_dir.glob(f"{system}-detailed.shard*.jsonl")):
            for line in f.read_text(encoding="utf-8").splitlines():
                r = json.loads(line)
                rows[r["cocoid"]] = r["caption"]
        if not rows:
            continue
        tp = mentions = 0
        recalls: list[float] = []
        for cid, cap in rows.items():
            m = sc.vi_classes(cap, vi_terms)
            tp += len(m & gold[cid])
            mentions += len(m)
            if gold[cid]:
                recalls.append(len(m & gold[cid]) / len(gold[cid]))
        p, r, f1 = prf(tp, mentions, recalls)
        label = "VSPS" if system == "distill" else "zero-shot"
        print(f"  {label:26s} n={len(rows)}  true/cap={tp/len(rows):.2f}  P={p:5.1f}  R={r:5.1f}  F1={f1:5.1f}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", default=str(ROOT / "data" / "results"))
    ap.add_argument("--split", default="test_data.json")
    ap.add_argument("--coco-preds", default=None, help="directory with {zeroshot,distill}-detailed.shard*.jsonl")
    ap.add_argument("--coco-manifest", default=str(ROOT / "data" / "coco_probe" / "manifest_full5000.json"))
    ap.add_argument("--ci", action="store_true", help="add 95%% bootstrap CIs over images")
    args = ap.parse_args()
    ktvic_block(Path(args.results).expanduser(), args.split, args.ci)
    if args.coco_preds:
        coco_block(Path(args.coco_preds).expanduser(), Path(args.coco_manifest))
    return 0


def _check() -> None:
    anc = {"phụ nữ": {"phụ nữ", "người"}, "người": {"người"}, "chó": {"chó"}}.get
    ancestors = lambda x: anc(x) or {x}
    # caption says người, gold has phụ nữ (and người from another annotator)
    c = image_counts({"người", "chó"}, {"phụ nữ", "người"}, ancestors)
    assert c[:4] == (1, 2, 1, 0.5) and c[4] == 0.0 and c[5] == 1.0, c


if __name__ == "__main__":
    _check()
    sys.exit(main())

