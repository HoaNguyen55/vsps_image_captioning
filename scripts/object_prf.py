#!/usr/bin/env python
"""Object-level precision, recall, and F1 over unique classes per image (Table IV).

    python scripts/object_prf.py                       # KTVIC test split, all *.preds.json in data/results
    python scripts/object_prf.py --coco-preds data/results/coco5000   # add the COCO-2014 block
    python scripts/object_prf.py --mode short --vs p1-gold            # paired bootstrap of each system vs P1
    NCS_DATASET=uitviic python scripts/object_prf.py --results ~/ncs-data/results/uitviic \\
        --instance-gold data/uitviic/instance_gold.json --mode short --vs uitviic_p1_s43   # UIT-ViIC transfer
    # COCO only (--results holds no KTVIC preds): every system in the dirs, paired bootstrap vs P1
    python scripts/object_prf.py --results data/results/coco_transfer --mode short --vs p1_s43 \\
        --coco-preds data/results/coco5000 data/results/coco_transfer --coco-manifest data/coco_probe/manifest.json

Definitions (Section IV-C of the paper): with M_i the set of object classes mentioned
in the caption of image i and G_i its gold classes, precision = sum|M_i & G_i| / sum|M_i|,
recall = mean over images with non-empty G_i of |M_i & G_i| / |G_i|, F1 = harmonic mean.
KTVIC uses the same 113-entry object lexicon and reference-derived gold as CHAIR-vi;
COCO uses the frozen instance-plus-reference gold of score_coco_probe.py and, as purely
human evidence, the instance labels alone; mentions no reference names are split into
instance-present (the references missed them) and instance-absent. Because the
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


def paired(rows_a: list[tuple], rows_b: list[tuple], keys=("P", "R", "F1"), n: int = 5000, seed: int = 0):
    """B - A on the SAME resampled images: {key: (point, ci_lo, ci_hi, two-sided p)}, p floored at 2/n."""
    import random
    rng = random.Random(seed)
    sa, sb = scores(rows_a), scores(rows_b)
    draws = {k: [] for k in keys}
    for _ in range(n):
        idx = [rng.randrange(len(rows_a)) for _ in rows_a]
        a, b = scores([rows_a[i] for i in idx]), scores([rows_b[i] for i in idx])
        for k in keys:
            draws[k].append(b[k] - a[k])
    out = {}
    for k, v in draws.items():
        v.sort()
        p = min(1.0, 2 * min(sum(d <= 0 for d in v), sum(d >= 0 for d in v)) / n)
        out[k] = (sb[k] - sa[k], v[int(0.025 * n)], v[int(0.975 * n) - 1], max(p, 2 / n))
    return out


def _preds(f: Path) -> dict[str, str]:
    preds = json.loads(f.read_text(encoding="utf-8"))
    return {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in preds.items()}


def _vs_table(per_system: dict[str, dict], vs: str, what: str = "") -> None:
    if vs not in per_system:
        print(f"  no {vs} preds{what}: paired bootstrap skipped")
        return
    base = per_system[vs]
    print(f"  paired bootstrap vs {vs}{what} (B=5000, same images): delta [95% CI] p")
    for name, by_id in per_system.items():
        if name == vs:
            continue
        ids = sorted(base.keys() & by_id.keys())
        d = paired([base[i] for i in ids], [by_id[i] for i in ids])
        print(f"  {name:26s} n={len(ids)}  " + "  ".join(
            f"d{k}={pt:+.1f} [{lo:+.1f},{hi:+.1f}] p={p:.4f}" for k, (pt, lo, hi, p) in d.items()))


def ktvic_block(results_dir: Path, split: str, ci: bool = False, mode: str = "detailed",
                vs: str | None = None) -> None:
    from evaluate import KTVIC, references
    from rescap.chair import _ancestors, objects_in

    refs = references(split)
    gold = {str(k): set().union(*[set(objects_in(r)) for r in rs]) for k, rs in refs.items()}
    print(f"{KTVIC.name.upper()} ({split}, {len(gold)} images, {mode} mode) -- object precision / recall / F1 (%)")
    print("  exact match | CHAIR-vi hypernym rule: P_h, R_spec (F1), R_vague (F1)")
    per_system = {}
    for f in sorted(results_dir.glob(f"*-{mode}.preds.json")):
        preds = _preds(f)
        by_id = {k: image_counts(set(objects_in(cap)), gold.get(k, set()), _ancestors) for k, cap in preds.items()}
        rows = list(by_id.values())
        s = scores(rows)
        tp = sum(r[0] for r in rows)
        name = f.name.removesuffix(f"-{mode}.preds.json")
        per_system[name] = by_id
        line = (f"  {name:26s} true/cap={tp/len(preds):.2f}  P={s['P']:5.1f}  R={s['R']:5.1f}  F1={s['F1']:5.1f}"
                f" | P_h={s['P_h']:5.1f}  R_spec={s['R_spec']:5.1f} ({s['F1_spec']:5.1f})"
                f"  R_vague={s['R_vague']:5.1f} ({s['F1_vague']:5.1f})")
        if ci:
            line += "  CI95 " + " ".join(f"{k}=[{a:.1f},{b:.1f}]" for k, (a, b) in bootstrap(rows).items())
        print(line)
    if vs:
        _vs_table(per_system, vs)


def instance_block(results_dir: Path, split: str, mode: str, gold_file: Path, vs: str | None = None) -> None:
    """P/R/F1 and CHAIR against human instance labels, with the COCO-2014 block's protocol.

    Gold = an image's COCO instance classes (build_uitviic_gold.py) plus the classes
    its references name; captions and references are matched with coco80_vi.json in
    the 80-class space, so CHAIR_i = 100 - P and CHAIR_s = % captions naming a non-gold class.
    """
    import score_coco_probe as sc
    from evaluate import KTVIC, references

    vi_terms = sc.load_vi_terms()
    inst = json.loads(gold_file.read_text(encoding="utf-8"))
    refs = references(split)
    if refs.keys() - inst.keys():
        raise SystemExit(f"{gold_file} lacks {len(refs.keys() - inst.keys())} images of {KTVIC.name}/{split}; "
                         "set NCS_DATASET to the dataset it was built for")
    gold = {k: set(inst[k]["coco"]).union(*[sc.vi_classes(r, vi_terms) for r in rs]) for k, rs in refs.items()}
    print(f"\n{KTVIC.name.upper()} ({split}, {len(gold)} images, {mode} mode) -- instance + reference gold, "
          "COCO-80 classes: P / R / F1, CHAIR_i = 100 - P, CHAIR_s (%)")
    mentions = {f.name.removesuffix(f"-{mode}.preds.json"): {k: sc.vi_classes(cap, vi_terms) for k, cap in _preds(f).items()}
                for f in sorted(results_dir.glob(f"*-{mode}.preds.json"))}
    per_system = _gold_table(mentions, gold)
    if vs:
        _vs_table(per_system, vs)


def _gold_table(mentions: dict[str, dict], gold: dict, label: dict[str, str] | None = None) -> dict[str, dict]:
    """Each system's mentioned classes against `gold` (flat class space): P / R / F1, CHAIR_i = 100 - P,
    CHAIR_s = % captions naming a non-gold class. Returns the per-image rows for _vs_table."""
    per_system = {}
    for name, ms in mentions.items():
        per_system[name] = {k: image_counts(m, gold.get(k, set()), lambda c: {c}) for k, m in ms.items()}
        rows = list(per_system[name].values())
        s, n, tp = scores(rows), len(rows), sum(r[0] for r in rows)
        print(f"  {(label or {}).get(name, name):26s} n={n}  true/cap={tp/n:.2f}  P={s['P']:5.1f}  R={s['R']:5.1f}"
              f"  F1={s['F1']:5.1f}  CHAIR_i={100 - s['P']:5.1f}  CHAIR_s={100 * sum(r[1] > r[0] for r in rows) / n:5.1f}")
    return per_system


#: paper names of the two systems shipped in data/results/coco5000
COCO_LABEL = {"zeroshot": "zero-shot", "distill": "VSPS"}


def ref_false(m: set[str], ref: set[str], inst: set[str]) -> tuple[int, int]:
    """(instance-present, instance-absent) counts among the mentioned classes no reference names."""
    unnamed = m - ref
    return len(unnamed & inst), len(unnamed - inst)


def coco_gold(manifest: Path) -> tuple[dict[int, set[str]], dict[int, set[str]]]:
    """(instance classes, reference classes) of every manifest image, as frozen in score_coco_probe.py."""
    import score_coco_probe as sc

    syn = sc.load_synonyms()
    want = {i["cocoid"] for i in json.loads(manifest.read_text(encoding="utf-8"))["images"]}
    inst = json.loads((sc.ANN / "instances_val2014.json").read_text())
    cat = {c["id"]: c["name"] for c in inst["categories"]}
    gold_inst: dict[int, set[str]] = {i: set() for i in want}
    for a in inst["annotations"]:
        if a["image_id"] in want:
            gold_inst[a["image_id"]].add(cat[a["category_id"]])
    gold_ref: dict[int, set[str]] = {i: set() for i in want}
    for img in json.loads(sc.KARPATHY.read_text())["images"]:
        if img["cocoid"] in want:
            for s in img["sentences"]:
                gold_ref[img["cocoid"]] |= sc.en_classes(s["raw"], syn)
    return gold_inst, gold_ref


def coco_block(preds_dirs: list[Path], manifest: Path, mode: str = "detailed", vs: str | None = None) -> None:
    """Every <system>-<mode>.shard*.jsonl under `preds_dirs`, on the manifest images, against
    instances + references and against the human instance labels alone; then the mentions no
    reference names, split into instance-present (reference gap) and instance-absent."""
    import score_coco_probe as sc

    vi_terms = sc.load_vi_terms()
    inst, ref = coco_gold(manifest)
    mentions: dict[str, dict[int, set[str]]] = defaultdict(dict)
    for d in preds_dirs:
        for f in sorted(d.glob(f"*-{mode}.shard*.jsonl")):
            name = f.name.split(f"-{mode}.shard")[0]
            for line in f.read_text(encoding="utf-8").splitlines():
                r = json.loads(line)
                if r["cocoid"] in inst:
                    mentions[name][r["cocoid"]] = sc.vi_classes(r["caption"], vi_terms)
    print(f"\nCOCO-2014 ({len(inst)} images, {mode} mode) -- object precision / recall / F1, "
          "CHAIR_i = 100 - P, CHAIR_s = captions with an invented class (%)")
    per_gold = {}
    for what, gold in (("instances + references", {i: inst[i] | ref[i] for i in inst}), ("instances only", inst)):
        print(f"  gold = {what}")
        per_gold[what] = _gold_table(mentions, gold, COCO_LABEL)
    print("  classes no reference names, per caption: in the instances (reference gap)"
          " | not in the instances (hallucination)")
    for name, ms in mentions.items():
        present, absent = (sum(c) for c in zip(*(ref_false(m, ref[k], inst[k]) for k, m in ms.items())))
        n, unnamed = len(ms), max(present + absent, 1)
        print(f"  {COCO_LABEL.get(name, name):26s} {(present + absent)/n:.2f}/cap  present {present/n:.2f}"
              f" ({100*present/unnamed:.1f}%)  absent {absent/n:.2f} ({100*absent/unnamed:.1f}%)")
    if vs:
        for what, per_system in per_gold.items():
            _vs_table(per_system, vs, f", gold = {what}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", default=str(ROOT / "data" / "results"))
    ap.add_argument("--split", default="test_data.json")
    ap.add_argument("--coco-preds", nargs="+", default=None,
                    help="directories with <system>-<mode>.shard*.jsonl (coco_probe.py output)")
    ap.add_argument("--coco-manifest", default=str(ROOT / "data" / "coco_probe" / "manifest_full5000.json"))
    ap.add_argument("--ci", action="store_true", help="add 95%% bootstrap CIs over images")
    ap.add_argument("--mode", default="detailed", help="prompt suffix of the preds files: detailed, short, two")
    ap.add_argument("--vs", default=None, help="baseline stem (e.g. p1-gold): paired bootstrap of every system against it")
    ap.add_argument("--instance-gold", default=None,
                    help="{image_id: {'coco': [classes]}} (build_uitviic_gold.py): add P/R/F1 and CHAIR against it")
    args = ap.parse_args()
    ktvic_block(Path(args.results).expanduser(), args.split, args.ci, args.mode, args.vs)
    if args.instance_gold:
        instance_block(Path(args.results).expanduser(), args.split, args.mode, Path(args.instance_gold), args.vs)
    if args.coco_preds:
        coco_block([Path(p).expanduser() for p in args.coco_preds], Path(args.coco_manifest), args.mode, args.vs)
    return 0


def _check() -> None:
    anc = {"phụ nữ": {"phụ nữ", "người"}, "người": {"người"}, "chó": {"chó"}}.get
    ancestors = lambda x: anc(x) or {x}
    # caption says người, gold has phụ nữ (and người from another annotator)
    c = image_counts({"người", "chó"}, {"phụ nữ", "người"}, ancestors)
    assert c[:4] == (1, 2, 1, 0.5) and c[4] == 0.0 and c[5] == 1.0, c
    a, b = [(1, 2, 1, 0.5, 0.5, 0.5)] * 20, [(2, 2, 2, 1.0, 1.0, 1.0)] * 20
    assert paired(a, b, n=200)["F1"][0] > 0 and paired(a, b, n=200)["F1"][3] <= 0.01
    assert paired(a, a, n=50)["F1"] == (0.0, 0.0, 0.0, 1.0)
    # chair: no reference names it but an instance box exists; dog: neither
    assert ref_false({"person", "chair", "dog"}, {"person"}, {"person", "chair"}) == (1, 1)


if __name__ == "__main__":
    _check()
    sys.exit(main())

