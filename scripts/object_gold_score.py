#!/usr/bin/env python
"""Agreement, adjudicated gold, and object P/R/F1 on the exhaustive human object gold (plan B1).

    NCS_DATA=$PWD/data python scripts/object_gold_score.py \
        --annotations data/object_gold/annot_A.json data/object_gold/annot_B.json \
        [--adjudicator data/object_gold/annot_C.json] --out data/results/object_gold.json
    python scripts/object_gold_score.py --self-check

Agreement (first two annotators): per-class Cohen's kappa over the 300 binary
present/absent decisions (agreement.cohens_kappa), their macro mean, pooled kappa over
all image x class decisions, raw agreement, and mean per-image Jaccard of the tick sets.

Gold. A class both annotators ticked is gold. A disputed class (one tick) is gold only if
the adjudicator, who sees the image and both tick sets, ticks it. Without an adjudicator
file two golds are scored to bracket the result: `agreed` (disputes dropped) and `union`
(disputes kept). Lexicon words typed into "other objects" count as ticks.

Scoring, for every *-detailed.preds.json in --results, restricted to the sampled images:
`exact` is the set definition of scripts/object_prf.py (precision = sum|M&G| / sum|M|,
recall = mean over images of |M&G| / |G|, via its prf()) with M and G folded to the same
checkbox classes. `lenient` adds the hypernym rule of rescap/chair.py: a vaguer mention
(`người` for a gold `phụ nữ`) is a true mention and covers that gold class.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from agreement import cohens_kappa  # noqa: E402
from object_gold_sample import CLASSES, class_key, surface_forms  # noqa: E402
from object_prf import prf  # noqa: E402
from rescap.chair import _ancestors, objects_in  # noqa: E402

FORMS = surface_forms()
#: class -> strictly vaguer classes, through every lexicon form of the class.
ANCESTORS = {c: {class_key(a) for f in FORMS[c] for a in _ancestors(f)} - {c} for c in CLASSES}


def mentions(caption: str) -> set[str]:
    return {class_key(n) for n in objects_in(caption or "")}


def read_annotations(path: Path, image_ids: list[str]) -> dict[str, set[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    labels = data["labels"]
    not_done = [i for i in image_ids if not (i in labels and labels[i].get("done"))]
    if not_done:
        raise SystemExit(f"{path.name}: {len(not_done)} images not finished, e.g. {not_done[:5]}")
    out = {}
    for i in image_ids:
        ticks = set(labels[i]["classes"])
        bad = ticks - set(CLASSES)
        if bad:
            raise SystemExit(f"{path.name}: image {i} has unknown classes {sorted(bad)}")
        out[i] = ticks | mentions(labels[i].get("other", ""))
    return out


def agreement(a: dict[str, set[str]], b: dict[str, set[str]]) -> dict:
    ids = sorted(a, key=int)
    per_class = {}
    for c in CLASSES:
        pairs = [(c in a[i], c in b[i]) for i in ids]
        if any(x or y for x, y in pairs):
            k, raw = cohens_kappa(pairs)
            per_class[c] = {"kappa": k, "raw": raw, "n_a": sum(x for x, _ in pairs), "n_b": sum(y for _, y in pairs)}
    pooled, raw = cohens_kappa([(c in a[i], c in b[i]) for i in ids for c in CLASSES])
    defined = [v["kappa"] for v in per_class.values() if v["kappa"] is not None]
    jacc = [len(a[i] & b[i]) / len(a[i] | b[i]) for i in ids if a[i] | b[i]]
    return {"macro_kappa": statistics.mean(defined) if defined else None, "pooled_kappa": pooled, "raw": raw,
            "mean_jaccard": statistics.mean(jacc) if jacc else None, "per_class": per_class}


def build_gold(a, b, adjudicator=None) -> dict[str, dict[str, set[str]]]:
    if adjudicator is not None:
        return {"adjudicated": {i: (a[i] & b[i]) | ((a[i] ^ b[i]) & adjudicator[i]) for i in a}}
    return {"agreed": {i: a[i] & b[i] for i in a}, "union": {i: a[i] | b[i] for i in a}}


def score(captions: dict[str, str], gold: dict[str, set[str]], lenient: bool) -> tuple[float, float, float]:
    tp = n_mentions = 0
    recalls: list[float] = []
    for i, g in gold.items():
        m = mentions(captions.get(i, ""))
        if lenient:
            vague_ok = {x for x in m if any(x in ANCESTORS[y] for y in g)}
            tp += len((m & g) | vague_ok)
            covered = {y for y in g if y in m or ANCESTORS[y] & m}
        else:
            tp += len(m & g)
            covered = m & g
        n_mentions += len(m)
        if g:
            recalls.append(len(covered) / len(g))
    return prf(tp, n_mentions, recalls)


def load_preds(path: Path) -> dict[str, str]:
    preds = json.loads(path.read_text(encoding="utf-8"))
    return {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in preds.items()}


def run(sample_path: Path, annotation_paths: list[Path], adjudicator_path: Path | None,
        systems: dict[str, dict[str, str]], partial: bool = False) -> dict:
    image_ids = [im["id"] for im in json.loads(sample_path.read_text(encoding="utf-8"))["images"]]
    if partial:
        done = [json.loads(p.read_text(encoding="utf-8"))["labels"] for p in annotation_paths]
        image_ids = [i for i in image_ids if all(i in d and d[i].get("done") for d in done)]
    ann = [read_annotations(p, image_ids) for p in annotation_paths]
    adj = read_annotations(adjudicator_path, image_ids) if adjudicator_path else None
    golds = build_gold(ann[0], ann[1], adj)
    report = {"n_images": len(image_ids), "annotators": [p.name for p in annotation_paths],
              "agreement": agreement(ann[0], ann[1]),
              "n_disputed": sum(len(ann[0][i] ^ ann[1][i]) for i in image_ids),
              "gold_per_image": {k: statistics.mean(len(v) for v in g.values()) for k, g in golds.items()},
              "systems": {}}
    for name, caps in systems.items():
        report["systems"][name] = {
            f"{gname}/{mode}": dict(zip("PRF", score(caps, g, mode == "lenient")))
            for gname, g in golds.items() for mode in ("exact", "lenient")}
    return report


def print_report(r: dict) -> None:
    ag = r["agreement"]
    fmt = lambda x: "n/a" if x is None else f"{x:.3f}"  # noqa: E731
    print(f"{r['n_images']} images, annotators {r['annotators']}")
    print(f"  agreement: macro kappa={fmt(ag['macro_kappa'])}  pooled kappa={fmt(ag['pooled_kappa'])}  "
          f"raw={ag['raw']:.3f}  mean Jaccard={fmt(ag['mean_jaccard'])}  disputed ticks={r['n_disputed']}")
    low = sorted(((v["kappa"], c) for c, v in ag["per_class"].items()
                  if v["kappa"] is not None and v["n_a"] + v["n_b"] >= 10))[:8]
    print("  lowest-kappa classes (>=10 ticks): " + ", ".join(f"{c} {k:.2f}" for k, c in low))
    print("  gold classes/image: " + ", ".join(f"{k} {v:.2f}" for k, v in r["gold_per_image"].items()))
    for name, cols in r["systems"].items():
        print(f"  {name:26s} " + "  ".join(f"{k}: P={v['P']:5.1f} R={v['R']:5.1f} F1={v['F']:5.1f}"
                                           for k, v in cols.items()))


def self_check() -> None:
    """Fake annotators on fake ids; every number below is known in advance."""
    import random

    rng = random.Random(0)
    pool = [c for c in CLASSES if not ANCESTORS[c] and c not in ("người", "vật", "đồ")]
    ids = [str(i) for i in range(1, 41)]
    truth = {i: set(rng.sample(pool, 3)) for i in ids}
    say = lambda cs: "trong ảnh có " + " và ".join(FORMS[c][0] for c in sorted(cs))  # noqa: E731
    assert all(mentions(say(truth[i])) == truth[i] for i in ids)
    extra = {i: rng.choice(sorted(set(pool) - truth[i])) for i in ids}
    noisy = {i: (truth[i] | {extra[i]}) if int(i) % 4 == 0 else truth[i] for i in ids}

    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "sample.json").write_text(json.dumps({"images": [{"id": i} for i in ids]}))

        def dump(name, labels, other=None):
            body = {i: {"classes": sorted(labels[i]), "other": (other or {}).get(i, ""), "done": True} for i in ids}
            (d / name).write_text(json.dumps({"annotator": name, "labels": body}, ensure_ascii=False))
            return d / name

        a, b = dump("a.json", truth), dump("b.json", noisy)
        perfect = {i: say(truth[i]) for i in ids}
        half = {i: say(sorted(truth[i])[:1] + [extra[i]]) for i in ids}

        r = run(d / "sample.json", [a, a], None, {"perfect": perfect, "half": half})
        assert r["agreement"]["pooled_kappa"] == 1.0 and r["n_disputed"] == 0
        assert all(v["kappa"] == 1.0 for v in r["agreement"]["per_class"].values() if v["kappa"] is not None)
        assert r["systems"]["perfect"]["agreed/exact"] == {"P": 100.0, "R": 100.0, "F": 100.0}
        p, rec = r["systems"]["half"]["agreed/exact"]["P"], r["systems"]["half"]["agreed/exact"]["R"]
        assert abs(p - 50) < 1e-9 and abs(rec - 100 / 3) < 1e-9, (p, rec)

        r = run(d / "sample.json", [a, b], None, {"perfect": perfect})
        assert 0 < r["agreement"]["pooled_kappa"] < 1 and r["n_disputed"] == 10
        assert r["systems"]["perfect"]["agreed/exact"]["R"] == 100.0
        assert abs(r["systems"]["perfect"]["union/exact"]["R"] - 100 * (30 * 1 + 10 * 3 / 4) / 40) < 1e-9

        adj = dump("c.json", truth)
        r = run(d / "sample.json", [a, b], adj, {"perfect": perfect})
        assert r["systems"]["perfect"]["adjudicated/exact"] == {"P": 100.0, "R": 100.0, "F": 100.0}

        women = {i: {"phụ nữ"} for i in ids}
        w = dump("w.json", women)
        typed = dump("t.json", {i: set() for i in ids}, {i: "một phụ nữ, cái cặp" for i in ids})
        r = run(d / "sample.json", [w, typed], None, {"vague": {i: "một người đang đứng" for i in ids}})
        assert r["agreement"]["pooled_kappa"] == 1.0, "lexicon word typed in 'other' must count as a tick"
        assert r["systems"]["vague"]["agreed/exact"]["P"] == 0.0
        assert r["systems"]["vague"]["agreed/lenient"] == {"P": 100.0, "R": 100.0, "F": 100.0}
        print_report(run(d / "sample.json", [a, b], None, {"perfect": perfect, "half": half}))
    print("self-check OK")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sample", default=str(ROOT / "data" / "object_gold" / "sample.json"))
    ap.add_argument("--annotations", nargs="+", help="annot_<name>.json of the two annotators")
    ap.add_argument("--adjudicator", default=None)
    ap.add_argument("--results", default=str(ROOT / "data" / "results"))
    ap.add_argument("--split", default="test_data.json")
    ap.add_argument("--out", default=None)
    ap.add_argument("--partial", action="store_true", help="score only images every annotator finished (calibration)")
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args()
    if args.self_check:
        self_check()
        return 0
    if not args.annotations or len(args.annotations) != 2:
        ap.error("--annotations needs exactly two files")

    systems = {f.name.removesuffix("-detailed.preds.json"): load_preds(f)
               for f in sorted(Path(args.results).glob("*-detailed.preds.json"))}
    from evaluate import KTVIC, references

    if (KTVIC / args.split).exists():
        systems["human ref #1"] = {k: rs[0] for k, rs in references(args.split).items()}
    report = run(Path(args.sample), [Path(p) for p in args.annotations],
                 Path(args.adjudicator) if args.adjudicator else None, systems, args.partial)
    print_report(report)
    if args.out:
        Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
