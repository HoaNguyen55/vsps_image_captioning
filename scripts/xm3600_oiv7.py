#!/usr/bin/env python
"""XM3600 in Vietnamese, scored against its human captions and against Open Images V7 human-verified labels.

    # layout + labels + coverage (CPU, seconds): $NCS_DATA/datasets/xm3600/{images/, full_data.json, test_data.json},
    # the English captions of the same images in $NCS_DATA/datasets/xm3600_en/ (images -> ../xm3600/images),
    # data/xm3600/oiv7_labels.json, data/xm3600/manifest.json, data/xm3600_subset.txt (the eval subset's ids)
    NCS_DATA=data python scripts/xm3600_oiv7.py build --raw data/datasets/xm3600/raw --oiv7 data/datasets/xm3600/oiv7
    # captions of the eval subset: NCS_DATASET=xm3600 scripts/evaluate.py (queue job 39_xm3600_eval.sh), then
    NCS_DATA=/root/ncs-data python scripts/xm3600_oiv7.py score --results /root/ncs-data/results/xm3600 --vs xm3600_p1_s43

Sources. Crossmodal-3600 (Thapliyal, Pont-Tuset, Chen & Soricut, EMNLP 2022; https://google.github.io/crossmodal-3600/):
3,600 Open Images photos (all CC BY 2.0, image_attributions.csv) with human captions in 36 languages, 7,350
Vietnamese (2 per image, 3 for 150); captions.zip CC BY 4.0. Open Images V7 (Kuznetsova et al., IJCV 2020;
https://storage.googleapis.com/openimages/web/download_v7.html; labels CC BY 4.0): the human-verified image-level
labels oidv7-{train,val,test}-annotations-human-imagelabels.csv, filtered to the XM3600 ids while streaming
(the full files' md5 checked against the bucket's), Confidence 1 = verified present, 0 = verified absent.

Vocabulary. data/xm3600/vi_oiv7_map.json maps a lexicon class c (objects_in) to `pos` OI classes (verified
present -> c present) and `neg` OI classes (verified absent -> c absent); status(image, c) = present if a pos
class is verified positive, else absent if a neg class is verified negative, else unknown (OI labels both ways
for one class, from two sources, count as unknown).

score, per <system>-<mode>.preds.json in --results and for the XM3600 captions themselves (each caption vs the
other(s), mean over the first two):
  refs      object P/R/F1 against the Vietnamese XM3600 captions (object_prf.image_counts, exact + hypernym).
  oiv7      mapped-class mentions: share verifiable; verified precision = present / (present + absent);
            verified-negative hallucination = mentioned / all (image, c) pairs verified absent, and the % of
            captions naming one; verified-positive recall; mentions no reference names, split by OI status.
  paired    every system minus --vs on the same resampled images (B draws), as object_prf.paired.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
import tarfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

DATA = Path(os.environ.get("NCS_DATA", Path.home() / "ncs-data"))
DATASET = DATA / "datasets" / "xm3600"
MAP = ROOT / "data" / "xm3600" / "vi_oiv7_map.json"
LABELS = ROOT / "data" / "xm3600" / "oiv7_labels.json"
MANIFEST = ROOT / "data" / "xm3600" / "manifest.json"
#: the image ids of the GPU eval subset (test_data.json of xm3600 and xm3600_en), one per line
SUBSET = ROOT / "data" / "xm3600_subset.txt"
OI_SPLITS = ("train", "val", "test")


def resolve_map(desc_csv: Path) -> dict[str, dict[str, set[str]]]:
    """vi_oiv7_map.json with display names turned into MIDs; refuses a name OIV7 does not have exactly once."""
    mids = defaultdict(list)
    with open(desc_csv, encoding="utf-8") as f:
        for mid, name in csv.reader(f):
            mids[name].append(mid)
    raw = json.loads(MAP.read_text(encoding="utf-8"))
    out = {}
    for c, v in raw.items():
        if c.startswith("_"):
            continue
        bad = [n for n in v["pos"] + v["neg"] if len(mids.get(n, [])) != 1]
        if bad:
            raise SystemExit(f"{MAP}: {c!r} names {bad}, not exactly one OIV7 class each")
        out[c] = {k: {mids[n][0] for n in v[k]} for k in ("pos", "neg")}
    return out


def status(c_map: dict[str, set[str]], pos: set[str], neg: set[str]) -> str:
    if c_map["pos"] & pos:
        return "present"
    return "absent" if c_map["neg"] & neg else "unknown"


def statuses(vmap: dict, labels: dict[str, dict[str, list[str]]]) -> dict[str, dict[str, str]]:
    """{image: {lexicon class: present|absent}} (unknown omitted)."""
    out = {}
    for img, lab in labels.items():
        pos, neg = set(lab["pos"]), set(lab["neg"])
        s = {c: st for c, m in vmap.items() if (st := status(m, pos, neg)) != "unknown"}
        if s:
            out[img] = s
    return out


def cmd_build(args) -> None:
    raw, oiv7 = Path(args.raw), Path(args.oiv7)
    lines = zipfile.ZipFile(raw / "captions.zip").read("captions.jsonl").decode("utf-8").splitlines()
    vi, en = {}, {}
    for line in lines:
        r = json.loads(line)
        vi[r["image/key"]] = [c.strip() for c in r["vi"]["caption"] if c.strip()]
        en[r["image/key"]] = [c.strip() for c in r["en"]["caption"] if c.strip()]
    with open(raw / "image_attributions.csv", encoding="utf-8") as f:
        attrib = {r["ImageID"]: r for r in csv.DictReader(f)}
    assert vi.keys() == attrib.keys() and len(vi) == 3600, (len(vi), len(attrib))

    seen = defaultdict(lambda: defaultdict(set))  # image -> mid -> {0, 1}
    rows = Counter()
    for split in OI_SPLITS:
        with open(oiv7 / f"xm3600-{split}-annotations-human-imagelabels.csv", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                assert r["ImageID"] in vi, r
                seen[r["ImageID"]][r["LabelName"]].add(int(float(r["Confidence"])))
                rows[split] += 1
    labels, conflicts = {}, 0
    for img in sorted(seen):
        conflicts += sum(len(v) > 1 for v in seen[img].values())
        labels[img] = {"pos": sorted(m for m, v in seen[img].items() if v == {1}),
                       "neg": sorted(m for m, v in seen[img].items() if v == {0})}
    vmap = resolve_map(oiv7 / "oidv7-class-descriptions.csv")
    st = statuses(vmap, labels)
    lexicon = _lexicon()
    pool = sorted(st)
    subset = sorted(random.Random(args.seed).sample(pool, args.n_eval))

    out_dir = Path(args.dataset_dir)
    (out_dir / "images").mkdir(parents=True, exist_ok=True)
    have = {p.name for p in (out_dir / "images").iterdir()}
    if len(have) < len(vi):
        with tarfile.open(raw / "images.tgz") as t:
            members = [m for m in t.getmembers() if m.isfile() and m.name.endswith(".jpg") and "/" not in m.name]
            t.extractall(out_dir / "images", members=members, filter="data")
    missing = [i for i in vi if not (out_dir / "images" / f"{i}.jpg").exists()]
    assert not missing, f"{len(missing)} images missing, e.g. {missing[:3]}"
    # Vietnamese layout, and the English captions of the same images (paired vi/en evaluation) beside it,
    # sharing the image files: $NCS_DATA/datasets/xm3600_en/images -> ../xm3600/images
    en_dir = out_dir.parent / f"{out_dir.name}_en"
    en_dir.mkdir(exist_ok=True)
    if not (en_dir / "images").exists():
        (en_dir / "images").symlink_to(Path("..") / out_dir.name / "images", target_is_directory=True)
    for d, caps in ((out_dir, vi), (en_dir, en)):
        for name, ids in (("full_data.json", sorted(vi)), ("test_data.json", subset)):
            data = {"images": [{"id": i, "filename": f"{i}.jpg"} for i in ids], "annotations": []}
            for i in ids:
                for c in caps[i]:
                    data["annotations"].append({"id": len(data["annotations"]), "image_id": i, "caption": c})
            (d / name).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    SUBSET.write_text("".join(f"{i}\n" for i in subset), encoding="utf-8")

    per_class = Counter(c for s in st.values() for c in s)
    coverage = {
        "lexicon_classes": len(lexicon), "mapped_classes": len(vmap),
        "mapped_classes_with_a_verified_label_on_xm3600": len(per_class),
        "xm3600_images": len(vi), "images_with_any_verified_label": len(labels),
        "images_with_a_verified_label_on_a_mapped_class": len(st),
        "image_class_pairs": {"present": sum(v == "present" for s in st.values() for v in s.values()),
                              "absent": sum(v == "absent" for s in st.values() for v in s.values())},
        "verified_labels": {"positive": sum(len(v["pos"]) for v in labels.values()),
                            "negative": sum(len(v["neg"]) for v in labels.values()), "conflicting": conflicts,
                            "rows_per_oi_split": dict(rows)},
        "pairs_per_class": {c: {"present": sum(s.get(c) == "present" for s in st.values()),
                                "absent": sum(s.get(c) == "absent" for s in st.values())}
                            for c, _ in per_class.most_common()},
        "oi_split_of_images": dict(Counter(attrib[i]["Subset"] for i in vi)),
        "eval_subset": {"n": len(subset), "seed": args.seed, "drawn_from": "images with a verified label on a mapped class",
                        "present": sum(v == "present" for i in subset for v in st[i].values()),
                        "absent": sum(v == "absent" for i in subset for v in st[i].values())}}
    prov = {"xm3600": "https://google.github.io/crossmodal-3600/ captions.zip (CC BY 4.0) + images.tgz "
                      "(Open Images photos, CC BY 2.0 each, image_attributions.csv)",
            "oiv7": "https://storage.googleapis.com/openimages/v7/oidv7-{train,val,test}-annotations-human-imagelabels.csv "
                    "(CC BY 4.0), rows of the 3,600 XM3600 ids; md5 of the full files checked against the bucket",
            "made_by": "scripts/xm3600_oiv7.py build", "map": str(MAP.relative_to(ROOT))}
    LABELS.parent.mkdir(parents=True, exist_ok=True)
    LABELS.write_text("{\n" + f'"_provenance": {json.dumps(prov, ensure_ascii=False)},\n' + ",\n".join(
        f"{json.dumps(k)}: {json.dumps(v)}" for k, v in labels.items()) + "\n}\n", encoding="utf-8")
    MANIFEST.write_text(json.dumps({"_provenance": prov, "coverage": coverage, "eval_subset": subset},
                                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in coverage.items() if k != "pairs_per_class"}, indent=1))
    print(f"wrote {out_dir}/{{full,test}}_data.json, {en_dir}/{{full,test}}_data.json (English), {LABELS}, {MANIFEST}, {SUBSET}")


def _lexicon() -> list[str]:
    from rescap.chair import _NOT_OBJECTS
    from rescap.vi.lexicon import NOUN_CLASSIFIER

    return [c for c in NOUN_CLASSIFIER if c not in _NOT_OBJECTS]


# ---------------------------------------------------------------- score
def caption_rows(m: set[str], st: dict[str, str], ref_gold: set[str], vmap_classes: set[str]) -> list[int]:
    """Per caption: [mapped mentions, present, absent, absent pairs, absent mentioned, present pairs, present
    mentioned, ref-false mapped, ref-false present, ref-false absent]."""
    mm = m & vmap_classes
    ab = {c for c, s in st.items() if s == "absent"}
    pr = {c for c, s in st.items() if s == "present"}
    rf = mm - ref_gold
    return [len(mm), len(mm & pr), len(mm & ab), len(ab), len(m & ab), len(pr), len(m & pr),
            len(rf), len(rf & pr), len(rf & ab)]


OI_KEYS = ("verifiable_share", "verified_precision", "neg_hallucination", "captions_naming_absent", "pos_recall")


def oi_stats(a: np.ndarray, idx: np.ndarray) -> dict[str, np.ndarray]:
    """a: (n, 10) caption_rows over images; idx: (B, n) resamples -> {key: (B,) array}."""
    s = a[idx]  # (B, n, 10)
    t = s.sum(1)
    div = lambda x, y: 100 * x / np.maximum(y, 1e-9)
    return {"verifiable_share": div(t[:, 1] + t[:, 2], t[:, 0]), "verified_precision": div(t[:, 1], t[:, 1] + t[:, 2]),
            "neg_hallucination": div(t[:, 4], t[:, 3]), "captions_naming_absent": 100 * (s[:, :, 4] > 0).mean(1),
            "pos_recall": div(t[:, 6], t[:, 5])}


def cmd_score(args) -> dict:
    from object_prf import image_counts, scores
    from rescap.chair import _ancestors, objects_in
    from second_panel import ci, delta, prf_arrays

    data = json.loads((Path(args.dataset_dir) / args.split).read_text(encoding="utf-8"))
    refs = defaultdict(list)
    for a in data["annotations"]:
        refs[str(a["image_id"])].append(a["caption"])
    ids = sorted(refs)
    labels = {k: v for k, v in json.loads(LABELS.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    vmap = resolve_map(Path(args.desc))
    st = statuses(vmap, labels)
    classes = set(vmap)
    objs = {i: [set(objects_in(c)) for c in refs[i]] for i in ids}
    gold = {i: set().union(*objs[i]) for i in ids}

    systems = {}
    for f in sorted(Path(args.results).glob("*.preds.json")):
        preds = json.loads(f.read_text(encoding="utf-8"))
        preds = {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in preds.items()}
        if set(ids) - preds.keys():
            print(f"  {f.name}: no caption for {len(set(ids) - preds.keys())} images, skipped")
            continue
        systems[f.name.removesuffix(".preds.json")] = {i: set(objects_in(preds[i])) for i in ids}
    rng = np.random.default_rng(0)
    idx = rng.integers(0, len(ids), size=(args.B, len(ids)))
    out = {"split": args.split, "n_images": len(ids), "B": args.B, "mapped_classes": len(classes),
           "images_with_status": sum(i in st for i in ids), "systems": {}}
    draws, points = {}, {}

    def record(name, prf_rows_by_fold, oi_rows_by_fold):
        """Fold-averaged (one fold for a system) point + CI for P/R/F1 and the OIV7 statistics."""
        p_pts = [scores(r) for r in prf_rows_by_fold]
        p_drw = [prf_arrays(r, idx) for r in prf_rows_by_fold]
        o_arr = [np.asarray(r, float) for r in oi_rows_by_fold]
        o_pts = [{k: float(v[0]) for k, v in oi_stats(a, np.arange(len(ids))[None]).items()} for a in o_arr]
        o_drw = [oi_stats(a, idx) for a in o_arr]
        pt = {k: float(np.mean([p[k] for p in p_pts])) for k in ("P", "R", "F1", "P_h", "R_spec", "F1_spec")}
        pt.update({k: float(np.mean([p[k] for p in o_pts])) for k in OI_KEYS})
        dr = {k: np.mean([d[k] for d in p_drw], axis=0) for k in ("P", "R", "F1")}
        dr.update({k: np.mean([d[k] for d in o_drw], axis=0) for k in OI_KEYS})
        tot = np.sum([a.sum(0) for a in o_arr], axis=0) / len(o_arr)
        n = len(ids)
        points[name], draws[name] = pt, dr
        out["systems"][name] = {
            **{k: round(v, 2) for k, v in pt.items()}, "ci95": {k: ci(v) for k, v in dr.items()},
            "per_caption": {"objects": round(float(np.mean([sum(r[1] for r in rows) for rows in prf_rows_by_fold]) / n), 3),
                            **{k: round(float(tot[j] / n), 3) for j, k in ((0, "mapped_mentions"), (1, "present"), (2, "absent"))}},
            "ref_false_mapped": {"per_caption": round(float(tot[7] / n), 3), "oi_present": round(float(tot[8] / n), 3),
                                 "oi_absent": round(float(tot[9] / n), 3),
                                 "oi_unknown": round(float((tot[7] - tot[8] - tot[9]) / n), 3)}}

    for name, ms in systems.items():
        record(name, [[image_counts(ms[i], gold[i], _ancestors) for i in ids]],
               [[caption_rows(ms[i], st.get(i, {}), gold[i], classes) for i in ids]])
    # XM3600 humans: caption k vs the union of the others, k = 0, 1 (every image has at least 2)
    record("human_xm3600", [[image_counts(objs[i][k], set().union(*(o for j, o in enumerate(objs[i]) if j != k)), _ancestors)
                             for i in ids] for k in (0, 1)],
           [[caption_rows(objs[i][k], st.get(i, {}), set().union(*(o for j, o in enumerate(objs[i]) if j != k)), classes)
             for i in ids] for k in (0, 1)])
    out["note"] = ("human_xm3600 is scored against the OTHER caption(s) only (1 or 2), systems against all; "
                   "its P/R are therefore not comparable to the systems', its OIV7 numbers are")
    if args.vs:
        out["paired_vs"] = args.vs
        for name in systems:
            mode = name.rsplit("-", 1)[-1]
            base = f"{args.vs}-{mode}"
            if name == base or base not in systems:
                continue
            out["systems"][name]["delta_vs_" + args.vs] = {
                k: delta(draws[base][k], draws[name][k], points[base][k], points[name][k])
                for k in ("P", "R", "F1", *OI_KEYS)}
    show(out)
    if args.out:
        Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"-> {args.out}")
    return out


def show(out: dict) -> None:
    print(f"XM3600 {out['split']}: {out['n_images']} images, {out['images_with_status']} with an OIV7 status on "
          f"{out['mapped_classes']} mapped classes; B={out['B']}")
    print("  P/R/F1 vs the Vietnamese XM3600 captions | OIV7: verifiable %, verified precision, verified-negative "
          "hallucination (pairs, % captions), verified-positive recall")
    for name, s in out["systems"].items():
        print(f"  {name:28s} P={s['P']:5.1f} R={s['R']:5.1f} F1={s['F1']:5.1f} | ver={s['verifiable_share']:5.1f} "
              f"vP={s['verified_precision']:5.1f} {s['ci95']['verified_precision']} negH={s['neg_hallucination']:5.1f} "
              f"({s['captions_naming_absent']:4.1f}% caps) posR={s['pos_recall']:5.1f} | ref-false {s['ref_false_mapped']}")
        if f"delta_vs_{out.get('paired_vs')}" in s:
            print("      vs " + out["paired_vs"] + ": " + "  ".join(
                f"d{k}={v['d']:+.1f} {v['ci95']} p={v['p']}" for k, v in s[f"delta_vs_{out['paired_vs']}"].items()))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="KTVIC-format layout, OIV7 labels of the XM3600 ids, coverage, eval subset")
    b.add_argument("--raw", default=str(DATASET / "raw"), help="captions.zip, image_attributions.csv, images.tgz")
    b.add_argument("--oiv7", default=str(DATASET / "oiv7"), help="xm3600-*-annotations-human-imagelabels.csv, class descriptions")
    b.add_argument("--n-eval", type=int, default=600, help="images captioned on the GPU (~14 s/image for 3 systems x 2 modes)")
    b.add_argument("--seed", type=int, default=0)
    s = sub.add_parser("score", help="P/R/F1 vs the XM3600 captions and OIV7 verified precision / hallucination")
    s.add_argument("--results", required=True, help="directory of <system>-<mode>.preds.json")
    s.add_argument("--split", default="test_data.json")
    s.add_argument("--desc", default=str(DATASET / "oiv7" / "oidv7-class-descriptions.csv"))
    s.add_argument("--vs", default=None, help="stem without -mode (e.g. xm3600_p1_s43): paired deltas of every system")
    s.add_argument("--B", type=int, default=2000)
    s.add_argument("--out", default=None)
    for p in (b, s):
        p.add_argument("--dataset-dir", default=str(DATASET))
    args = ap.parse_args()
    {"build": cmd_build, "score": cmd_score}[args.cmd](args)
    return 0


def _check() -> None:
    m = {"pos": {"/m/dog"}, "neg": {"/m/dog", "/m/animal"}}
    assert status(m, {"/m/dog"}, {"/m/animal"}) == "present"  # positive wins
    assert status(m, set(), {"/m/animal"}) == "absent" and status(m, {"/m/cat"}, set()) == "unknown"
    st = {"chó": "present", "mèo": "absent", "người": "absent"}
    r = caption_rows({"chó", "mèo", "xe"}, st, {"chó"}, {"chó", "mèo", "người"})
    assert r == [2, 1, 1, 2, 1, 1, 1, 1, 0, 1], r
    a = np.array([r, caption_rows(set(), st, set(), {"chó", "mèo", "người"})], float)
    o = {k: float(v[0]) for k, v in oi_stats(a, np.arange(2)[None]).items()}
    assert o["verified_precision"] == 50.0 and o["neg_hallucination"] == 25.0 and o["captions_naming_absent"] == 50.0
    assert o["pos_recall"] == 50.0 and o["verifiable_share"] == 100.0


if __name__ == "__main__":
    _check()
    sys.exit(main())
