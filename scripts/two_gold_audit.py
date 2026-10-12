#!/usr/bin/env python
"""Two-gold audit: fused human references (training targets) and the models trained on them, scored against
the dataset's OWN held-out references and against independent evidence (V3 verification, R5-03).

    NCS_DATA=data python scripts/two_gold_audit.py                    # every block -> data/results/two_gold_audit.json
    NCS_DATA=data python scripts/two_gold_audit.py --blocks ktvic_targets ktvic_models --B 1000
    # pre-registered G3' (UIT-ViIC in-domain, jobs 59a/59b) and job 36 (COCO 2,500), once their preds exist:
    NCS_DATA=data python scripts/two_gold_audit.py --blocks uitviic_models coco_models \\
        --uit-results ~/ncs-data/results/uitviic --uit-pair uitviic_p1_s42:uitviic_fuse2_s42 \\
        --coco-results data/results/coco_transfer --coco-pair p1_s43:fuse2_s42

Golds, per image and per fold (an image's 5 captions: 3 build the target, the other 2 are held out; 10 folds,
human_parity.py offline 'common'):  A = classes the 2 held-out captions name (the annotator team's typicality),
I = independent evidence (KTVIC: the UIT-OpenViIC panel of the same image, data/ktvic_openviic_refs.json;
UIT-ViIC and COCO: the COCO-2014 instance labels), U = A | I.
  targets  build_gold_sft.py's policies (p1, cons, fuse2, rnd2, unf2, multiref) from the 3 kept captions;
           fuse2/rnd2 are one joined row, unf2/multiref average their rows (human_parity.pool).
  models   trained systems against the same golds next to the human targets of the same images:
           DiD = d(model) - d(targets), the precision change the model adds beyond its references.
P_g / R_g are object_prf.py's micro P and macro R per fold, then the fold mean; x_false_g = mentions outside g
per caption; tau_I = d(I-false)/d(A-false) (share of a reference-precision change that is also a truth change;
V3), tau_U the same with U; conf = share of A-false mentions that I names (the legacy gate G3 for fuse2).
Singletons: P(c in I | c named by k of the 5 captions) and the rate a class drawn from the mention mix would
have by chance. Extractors: KTVIC objects_in (113 nouns); COCO-80 in Vietnamese (score_coco_probe.vi_classes,
lexicon v1 = data/coco_probe/coco80_vi.json, v2 = score_coco_probe.LEX_V2); English en_classes (Rohrbach synonyms). Families:
all; nosel = without sports ball and person (in 100% / 97.5% of UIT-ViIC images); reliable = classes named by
5/5 captions that are >= 99% instance-present (n >= 10) on Karpathy VAL. 95% CIs resample images (weights
shared by every statistic of a block); p two-sided, floored at 2/B.
"""
from __future__ import annotations

import argparse
import gc
import itertools
import json
import random
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
import score_coco_probe as sc  # noqa: E402
from build_gold_sft import consensual, fusion_set  # noqa: E402
from rescap.chair import objects_in  # noqa: E402

RESULTS = ROOT / "data" / "results"
POLICIES = ("p1", "cons", "fuse2", "rnd2", "unf2", "multiref")
FIELDS = ("m", "tpA", "tpI", "tpU", "rA", "hA", "rI", "hI", "rU", "hU")
K = {f: j for j, f in enumerate(FIELDS)}
SEL = frozenset({"sports ball", "person"})
VI_TERMS = sc.load_vi_terms()
EN_SYN = sc.load_synonyms()
#: G3' (V3 sec. 4): replaces gate G3, which cannot fail on UIT-ViIC (human targets 98.6%, chance ~88%)
G3_PRIME = {
    "frozen": "2026-10-12, before any UIT-ViIC in-domain prediction (jobs 59a/59b) or job-36 fuse2 output exists",
    "data": "UIT-ViIC test+val with 5 captions (1,155 images), family nosel, lexicon v2, B = 5000",
    "G3a": "short, fuse2-short - P1-short: 90% CI of dP_I inside [-3, +3] and the 95% CI of dR_I above 0",
    "G3b": "two-sentence: DiD_I = [P_I(fuse2-detailed) - P_I(P1-short)] - [P_I(fused human pair) - P_I(single "
           "human caption)], targets from 3 of 5 captions: pass if the 95% CI lower bound > -3, kill if the upper < -3",
    "G3c": "tau_model = d(I-false)/d(A-false): 'mostly typicality' if its 95% CI upper < 0.5, 'mostly truth' if the "
           "lower > 0.5; benchmark tau_human = uitviic_valtest|v2|nosel pairs fuse2-p1 tau_I",
    "job36": "COCO 2,500 (data/coco_probe/manifest.json), KTVIC-trained: 'no worse than human fusion' if "
             "(tau_model - tau_human) 95% CI upper < +0.15, families all and reliable",
    "legacy_G3": "report only as 'uninformative on UIT-ViIC' (fuse2 human targets conf ~98.6%, chance ~88%)",
}


# ----------------------------------------------------------------------------------------------- extraction
@lru_cache(maxsize=None)
def ktvic_obj(text: str) -> frozenset[str]:
    return frozenset(objects_in(text))


@lru_cache(maxsize=None)
def vi_obj(text: str, v2: bool = True) -> frozenset[str]:
    """COCO-80 matcher v2 (frozen for G3', score_coco_probe.LEX_V2) or v1."""
    return frozenset(sc.vi_objects(text, VI_TERMS, "v2" if v2 else "v1"))


@lru_cache(maxsize=None)
def en_obj(text: str) -> frozenset[str]:
    return frozenset(sc.en_classes(text, EN_SYN))


def rows_of(policy: str, kept: list[str], obj, rng: random.Random) -> list[frozenset]:
    """Mention sets of the training rows a build_gold_sft.py policy makes from the kept captions."""
    if policy == "p1":
        return [obj(kept[0])]
    if policy == "cons":
        return [obj(consensual(kept, obj))]
    if policy == "multiref":
        return [obj(c) for c in kept]
    used = fusion_set(kept, 2, rng if policy == "rnd2" else None, obj)
    return [frozenset().union(*map(obj, used))] if policy in ("fuse2", "rnd2") else [obj(c) for c in used]


# ----------------------------------------------------------------------------------------------- counting
def counts(m: frozenset, a: frozenset, i: frozenset) -> list[float]:
    u = a | i
    out = [len(m), len(m & a), len(m & i), len(m & u)]
    for g in (a, i, u):
        out += [len(m & g) / len(g), 1.0] if g else [0.0, 0.0]
    return out


def fold_array(ids, caps, indep, obj, fam, systems: dict, seed: int = 42) -> np.ndarray:
    """X[image, fold, system, field]; a system maps (kept captions, image id, rng) to its rows' mention sets."""
    rng = random.Random(seed)
    cut = (lambda s: s) if fam is None else (lambda s: s & fam)
    x = np.zeros((len(ids), 10, len(systems), len(FIELDS)))
    for n, i in enumerate(ids):
        cs, ind = caps[i], cut(frozenset(indep[i]))
        for f, keep in enumerate(itertools.combinations(range(5), 3)):
            kept = [cs[j] for j in keep]
            a = cut(frozenset().union(*(obj(cs[j]) for j in range(5) if j not in keep)))
            for s, make in enumerate(systems.values()):
                x[n, f, s] = np.mean([counts(cut(m), a, ind) for m in make(kept, i, rng)], axis=0)
    return x


def weights(n: int, B: int, seed: int = 0) -> np.ndarray:
    """Row 0 = the full sample, rows 1..B = image resamples (multinomial counts)."""
    return np.vstack([np.ones((1, n)), np.random.default_rng(seed).multinomial(n, [1 / n] * n, size=B)])


def stats(x: np.ndarray, w: np.ndarray) -> dict[str, np.ndarray]:
    """{statistic: (B+1, systems)}: P/R fold-averaged, per-caption rates and conf pooled over folds."""
    n = x.shape[0]
    t = (w @ x.reshape(n, -1)).reshape(len(w), *x.shape[1:])
    out = {"M": t[..., K["m"]].mean(1) / n}
    with np.errstate(invalid="ignore", divide="ignore"):
        for g in "AIU":
            out[f"P_{g}"] = 100 * np.nanmean(t[..., K[f"tp{g}"]] / t[..., K["m"]], axis=1)
            out[f"R_{g}"] = 100 * np.nanmean(t[..., K[f"r{g}"]] / t[..., K[f"h{g}"]], axis=1)
            out[f"false_{g}"] = (t[..., K["m"]] - t[..., K[f"tp{g}"]]).mean(1) / n
        s = t.sum(1)
        out["conf"] = 100 * (s[..., K["tpU"]] - s[..., K["tpA"]]) / (s[..., K["m"]] - s[..., K["tpA"]])
    return out


def summ(v: np.ndarray, test: bool = False) -> list:
    """[point, [2.5%, 97.5%]] (+ two-sided p floored at 2/B) of a (B+1,) array; None where undefined."""
    bs = v[1:][~np.isnan(v[1:])]
    r = lambda q: None if np.isnan(q) else round(float(q), 3)  # noqa: E731
    out = [r(v[0]), [r(q) for q in np.percentile(bs, [2.5, 97.5])] if len(bs) else [None, None]]
    if test and len(bs):
        out.append(round(max(min(1.0, 2 * min((bs <= 0).mean(), (bs >= 0).mean())), 2 / len(bs)), 4))
    return out


STATS = ("M", "P_A", "P_I", "P_U", "R_A", "R_I", "R_U", "false_A", "false_I", "false_U", "conf")


def seed_weights(k: int, rows: int, rng: np.random.Generator) -> np.ndarray:
    """(rows, k) weights of k seeds: row 0 uniform, then the seeds resampled with replacement (two-level bootstrap)."""
    return np.vstack([np.full((1, k), 1 / k), rng.multinomial(k, [1 / k] * k, size=rows - 1) / k])


def diff(st: dict, names: list[str], a, b, wa=None, wb=None) -> dict[str, np.ndarray]:
    """b - a per statistic; a/b are a name or a list of names averaged (per-draw weights wa/wb), + tau_I, tau_U."""
    def col(v, s, w):
        idx = [names.index(x) for x in ([s] if isinstance(s, str) else s)]
        return v[:, idx].mean(1) if w is None else (v[:, idx] * w).sum(1)
    d = {k: col(st[k], b, wb) - col(st[k], a, wa) for k in STATS}
    with np.errstate(invalid="ignore", divide="ignore"):
        d["tau_I"], d["tau_U"] = d["false_I"] / d["false_A"], d["false_U"] / d["false_A"]
    return d


def singletons(ids, caps, indep, obj, fam) -> dict:
    cut = (lambda s: s) if fam is None else (lambda s: s & fam)
    base = Counter(c for i in ids for c in cut(frozenset(indep[i])))
    mix, byk = Counter(), defaultdict(lambda: [0, 0])
    for i in ids:
        named = [cut(obj(c)) for c in caps[i]]
        mix.update(c for s in named for c in s)
        for c in frozenset().union(*named):
            byk[sum(c in s for s in named)][0] += c in indep[i]
            byk[sum(c in s for s in named)][1] += 1
    tot = max(sum(mix.values()), 1)
    return {"present_by_k": {k: [v[1], round(100 * v[0] / v[1], 2)] for k, v in sorted(byk.items())},
            "chance_present": round(100 * sum(v * base[c] / len(ids) for c, v in mix.items()) / tot, 2),
            "mentions_per_caption": round(tot / (5 * len(ids)), 3)}


def policy_systems(obj) -> dict:
    return {p: (lambda kept, i, rng, p=p: rows_of(p, kept, obj, rng)) for p in POLICIES}


def targets(ids, caps, indep, obj, fams: dict, B: int) -> dict:
    w, out = weights(len(ids), B), {"n_images": len(ids)}
    for fname, fam in fams.items():
        st = stats(fold_array(ids, caps, indep, obj, fam, policy_systems(obj)), w)
        out[fname] = {"policies": {p: {k: summ(st[k][:, s]) for k in STATS} for s, p in enumerate(POLICIES)},
                      "vs_p1": {f"{b}-p1": {k: summ(v, test=k.startswith(("P", "R"))) for k, v in
                                            diff(st, list(POLICIES), "p1", b).items()} for b in POLICIES[1:]},
                      "singletons": singletons(ids, caps, indep, obj, fam)}
        d = out[fname]["vs_p1"]["fuse2-p1"]
        print(f"  [{fname}] fuse2-p1 dP_A {d['P_A']} dP_I {d['P_I']} dP_U {d['P_U']} dR_I {d['R_I'][:2]} "
              f"tau_I {d['tau_I']} | conf fuse2 {out[fname]['policies']['fuse2']['conf']}", flush=True)
    return out


def models(data: tuple, preds: dict, p1s: list, f2s: list, B: int, seed: int = 0) -> dict:
    """Model contrasts next to the human-target contrasts of the same images and golds; one entry per
    (P1 seed, fuse2 seed) and a two-level pooled entry (seeds resampled within every image draw).
    data = (ids, captions, independent evidence, extractor, family)."""
    ids, caps, indep, obj, fam = data
    systems = {f"T_{p}": policy_systems(obj)[p] for p in ("p1", "cons", "fuse2")}
    systems.update({s: (lambda kept, i, rng, m=m: [m[i]]) for s, m in preds.items()})
    names = list(systems)
    w = weights(len(ids), B, seed)
    st = stats(fold_array(ids, caps, indep, obj, fam, systems), w)
    rng = np.random.default_rng(seed + 1)
    out = {"n_images": len(ids), "systems": {s: {k: summ(st[k][:, j]) for k in STATS} for j, s in enumerate(names)},
           "contrasts": {}}
    for mode, f_mode, t_b in (("two-sentence", "detailed", "T_fuse2"), ("short", "short", "T_cons")):
        tgt = diff(st, names, "T_p1", t_b)
        pa = [f"{p}-short" for p in p1s if f"{p}-short" in preds]
        pb = [f"{f}-{f_mode}" for f in f2s if f"{f}-{f_mode}" in preds]
        dms = {f"{b} - {a}": diff(st, names, a, b) for a in pa for b in pb}
        if len(dms) > 1:  # two-level: images (rows of w) x seeds (resampled within every draw)
            dms["pooled"] = diff(st, names, pa, pb, seed_weights(len(pa), len(w), rng), seed_weights(len(pb), len(w), rng))
        rows = {key: {k: {"model": summ(dm[k], test=True), "targets": summ(tgt[k], test=True),
                          "DiD": summ(dm[k] - tgt[k], test=True)} for k in STATS + ("tau_I", "tau_U")}
                for key, dm in dms.items()}
        for key, dm in dms.items():  # G3'a reads a 90% CI
            rows[key]["P_I"]["model_ci90"] = [round(float(q), 3) for q in np.percentile(dm["P_I"][1:], [5, 95])]
        out["contrasts"][mode] = rows
        for key, r in rows.items():
            print(f"  [{mode}] {key}: dP_A model {r['P_A']['model'][:2]} targets {r['P_A']['targets'][:2]} DiD "
                  f"{r['P_A']['DiD'][:2]} | dP_U DiD {r['P_U']['DiD'][:2]} | dP_I DiD {r['P_I']['DiD'][:2]}", flush=True)
    return out


# ----------------------------------------------------------------------------------------------- data
def ktvic(split: str):
    from evaluate import references
    refs = references(f"{split}_data.json")
    panel = json.loads((ROOT / "data" / "ktvic_openviic_refs.json").read_text(encoding="utf-8"))[split]
    ids = sorted(i for i in refs.keys() & panel.keys() if len(refs[i]) == 5 and panel[i])
    return ids, {i: [c.strip() for c in refs[i]] for i in ids}, {i: frozenset().union(*map(ktvic_obj, panel[i])) for i in ids}


def uitviic(splits):
    caps = defaultdict(list)
    for sp in splits:
        for a in json.loads((ROOT / "data/datasets/uitviic" / f"{sp}_data.json").read_text(encoding="utf-8"))["annotations"]:
            if a["caption"].strip():
                caps[str(a["image_id"])].append(a["caption"].strip())
    inst = json.loads((ROOT / "data/uitviic/instance_gold.json").read_text(encoding="utf-8"))
    ids = sorted(i for i, cs in caps.items() if len(cs) == 5)
    return ids, {i: caps[i] for i in ids}, {i: frozenset(inst[i]["coco"]) for i in ids}


def coco_sources(uit_ids: set[str]):
    """English captions (first 5, Karpathy) and COCO-2014 instance classes of the Karpathy val/test images
    and of the UIT-ViIC images; splits for val/test."""
    kar = json.loads(sc.KARPATHY.read_text())
    en, split = {}, {}
    for img in kar["images"]:
        k = str(img["cocoid"])
        s = [x["raw"].strip() for x in img["sentences"] if x["raw"].strip()]
        if len(s) >= 5 and (img["split"] in ("val", "test") or k in uit_ids):
            en[k], split[k] = s[:5], img["split"]
    del kar
    gc.collect()
    inst = json.loads((sc.ANN / "instances_val2014.json").read_text())
    cat = {c["id"]: c["name"] for c in inst["categories"]}
    gold = {k: set() for k, s in split.items() if s in ("val", "test")}
    for a in inst["annotations"]:
        if str(a["image_id"]) in gold:
            gold[str(a["image_id"])].add(cat[a["category_id"]])
    del inst
    gc.collect()
    return en, split, {k: frozenset(v) for k, v in gold.items()}


def reliable_classes(en, split, gold) -> list[str]:
    hit = defaultdict(lambda: [0, 0])
    for i in (k for k, s in split.items() if s == "val"):
        named = [en_obj(c) for c in en[i]]
        for c in frozenset.intersection(*named):
            hit[c][0] += c in gold[i]
            hit[c][1] += 1
    return sorted(c for c, (h, n) in hit.items() if n >= 10 and h / n >= 0.99)


def tau_buckets(x: np.ndarray, ncls: np.ndarray, B: int) -> dict:
    """tau_I of fuse2 vs p1 targets by the number of instance classes in the image."""
    out = {}
    for b, (lo, hi) in {"all": (0, 99), "1-2": (1, 2), "3-4": (3, 4), "5+": (5, 99)}.items():
        sel = np.where((ncls >= lo) & (ncls <= hi))[0]
        d = diff(stats(x[sel], weights(len(sel), B)), list(POLICIES), "p1", "fuse2")
        out[b] = {"n": int(len(sel)), "d_false_A": summ(d["false_A"]), "d_false_I": summ(d["false_I"]),
                  "tau_I": summ(d["tau_I"])}
    return out


def panel_validate(ids, en, gold, B: int) -> dict:
    """R5-01's second-panel estimator where truth exists (V3 P5): COCO test, panel A = English captions 0-2,
    panel B = 3-4, truth = instances; systems = the Vietnamese zero-shot / VSPS captions in data/results/coco5000.
    real_fraction_est = system share of A-unsupported mentions that B confirms / the held-out human's share;
    true_ratio = the same with instance presence."""
    systems = {}
    for f in sorted((RESULTS / "coco5000").glob("*.shard0of1.jsonl")):
        rows = {str(json.loads(x)["cocoid"]): json.loads(x)["caption"] for x in f.read_text(encoding="utf-8").splitlines()}
        if set(ids) <= rows.keys():
            systems[f.name.split(".shard")[0]] = [vi_obj(rows[i], False) for i in ids]
    a = [[en_obj(c) for c in en[i][:3]] for i in ids]
    bp = [frozenset().union(*(en_obj(c) for c in en[i][3:5])) for i in ids]

    def table(cap_of):  # per image, mean over the 3 folds: unsupported, confirmed by B, instance-present
        x = np.zeros((len(ids), 3))
        for k, i in enumerate(ids):
            for j in range(3):
                u = cap_of(k, j) - frozenset().union(*(a[k][q] for q in range(3) if q != j))
                x[k] += [len(u), len(u & bp[k]), len(u & gold[i])]
        return x / 3
    w = weights(len(ids), B)
    t = {"human_1v2": w @ table(lambda k, j: a[k][j])}
    t.update({s: w @ table(lambda k, j, m=m: m[k]) for s, m in systems.items()})
    h = t["human_1v2"]
    out = {"human_1v2": {"unsupported_per_caption": round(h[0, 0] / len(ids), 3), "confirmed": summ(100 * h[:, 1] / h[:, 0]),
                         "present": summ(100 * h[:, 2] / h[:, 0])}}
    for s in systems:
        v = t[s]
        est, tru = (v[:, 1] / v[:, 0]) / (h[:, 1] / h[:, 0]), (v[:, 2] / v[:, 0]) / (h[:, 2] / h[:, 0])
        out[s] = {"unsupported_per_caption": round(v[0, 0] / len(ids), 3), "real_fraction_est": summ(100 * est),
                  "true_ratio": summ(100 * tru), "est_minus_true": summ(100 * (est - tru))}
    return out


def load_vi_preds(results: Path, stem: str, mode: str) -> dict[str, str] | None:
    """<stem>-<mode>.preds.json (several stems joined by ',' are merged) or COCO shards <stem>-<mode>.shard*.jsonl."""
    out = {}
    for s in stem.split(","):
        f = results / f"{s}-{mode}.preds.json"
        if f.exists():
            out.update({str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in json.loads(f.read_text()).items()})
        for sh in sorted(results.glob(f"{s}-{mode}.shard*.jsonl")):
            out.update({str(json.loads(x)["cocoid"]): json.loads(x)["caption"] for x in sh.read_text().splitlines()})
    return out or None


def verdicts(res: dict, kind: str) -> dict:
    """The pre-registered G3' (kind 'uit') or job-36 (kind 'coco') decisions read off a models() result."""
    def get(mode, k):
        rows = res["contrasts"].get(mode, {})
        return next(iter(rows.values()))[k] if rows else None
    out = {}
    if kind == "coco":
        for mode in ("two-sentence", "short"):
            t = get(mode, "tau_I")
            out[f"job36_{mode}"] = t and ("no worse than human fusion" if t["DiD"][1][1] < 0.15 else "not shown")
        return out
    p, r = get("short", "P_I"), get("short", "R_I")
    if p:
        out["G3a"] = "pass" if -3 < p["model_ci90"][0] and p["model_ci90"][1] < 3 and r["model"][1][0] > 0 else "fail"
    d, t = get("two-sentence", "P_I"), get("two-sentence", "tau_I")
    if d:
        lo, hi = d["DiD"][1]
        out["G3b"] = "pass" if lo > -3 else "kill" if hi < -3 else "inconclusive"
        lo, hi = t["model"][1]
        out["G3c"] = "mostly typicality" if hi < 0.5 else "mostly truth" if lo > 0.5 else "undetermined"
    return out


def model_block(data: tuple, results: Path, pair: str, B: int, kind: str) -> dict:
    """models() on vi_classes preds <stem>-<mode> of a P1:fuse2 pair once they exist, with the frozen verdicts."""
    ids, caps, indep, obj, fam = data
    p1, f2 = pair.split(":")
    preds = {f"{s}-{m}": load_vi_preds(results, s, m) for s in (p1, f2) for m in ("short", "detailed")}
    preds = {k: v for k, v in preds.items() if v}
    if f"{p1}-short" not in preds or not any(k.startswith(f2) for k in preds):
        return {"status": f"not landed: {sorted(preds)} in {results}"}
    keep = [i for i in ids if all(i in v for v in preds.values())]
    print(f"  {len(keep)}/{len(ids)} images have every prediction", flush=True)
    res = models((keep, caps, indep, obj, fam), {k: {i: vi_obj(v[i]) for i in keep} for k, v in preds.items()},
                 [p1], [f2], B)
    res["verdicts"] = verdicts(res, kind)
    print(f"  pre-registered verdicts: {res['verdicts']}", flush=True)
    return res


# ----------------------------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--blocks", nargs="+", default=["ktvic_targets", "ktvic_models", "uitviic_train", "uitviic_valtest",
                                                    "coco", "uitviic_models", "coco_models"])
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--p1", nargs="+", default=["p1-gold", "p1_s43", "p1_s44"], help="KTVIC P1 seed stems")
    ap.add_argument("--fuse2", nargs="+", default=["fuse2_s42", "fuse2_s43", "fuse2_s44"], help="KTVIC fuse2 stems")
    ap.add_argument("--uit-results", default=str(RESULTS / "uitviic"))
    ap.add_argument("--uit-pair", default="uitviic_p1_s42:uitviic_fuse2_s42")
    ap.add_argument("--coco-results", default=str(RESULTS / "coco_transfer"))
    ap.add_argument("--coco-pair", default="p1_s43:fuse2_s42")
    ap.add_argument("--out", default=str(RESULTS / "two_gold_audit.json"))
    a = ap.parse_args()
    out = json.loads(Path(a.out).read_text()) if Path(a.out).exists() else {}
    out.update({"what": "scripts/two_gold_audit.py (V3): precision vs held-out references (A), independent "
                        "evidence (I) and their union (U)", "B": a.B, "G3_prime_prereg": G3_PRIME})
    if "ktvic_targets" in a.blocks:
        print("KTVIC train targets vs held-out KTVIC (A), OpenViIC (I), union (U)", flush=True)
        out["ktvic_targets"] = targets(*ktvic("train"), ktvic_obj, {"all": None}, a.B)
    if "ktvic_models" in a.blocks:
        ids, caps, ind = ktvic("test")
        preds = {}
        for s in a.p1 + a.fuse2:
            for m in ("short", "detailed"):
                f = RESULTS / f"{s}-{m}.preds.json"
                if f.exists():
                    p = json.loads(f.read_text(encoding="utf-8"))
                    preds[f"{s}-{m}"] = {i: ktvic_obj((p[i][0] if isinstance(p[i], list) else p[i]) or "") for i in ids}
        print(f"KTVIC test models ({len(ids)} images): {sorted(preds)}", flush=True)
        out["ktvic_models"] = models((ids, caps, ind, ktvic_obj, None), preds, [s for s in a.p1 if f"{s}-short" in preds],
                                     [s for s in a.fuse2 if f"{s}-short" in preds], a.B)
    fams_uit = {"all": None, "nosel": frozenset(EN_SYN.values()) - SEL}
    for block, splits in (("uitviic_train", ("train",)), ("uitviic_valtest", ("val", "test"))):
        if block in a.blocks:
            ids, caps, inst = uitviic(splits)
            out[block] = {}
            for lex in ("v1", "v2"):
                print(f"UIT-ViIC {'+'.join(splits)} ({len(ids)} images), lexicon {lex}", flush=True)
                out[block][lex] = targets(ids, caps, inst, lambda t, v2=lex == "v2": vi_obj(t, v2), fams_uit, a.B)
    if "uitviic_models" in a.blocks:
        ids, caps, inst = uitviic(("val", "test"))
        out["uitviic_models"] = model_block((ids, caps, inst, vi_obj, fams_uit["nosel"]), Path(a.uit_results).expanduser(),
                                            a.uit_pair, 5000, "uit")
    if {"coco", "coco_models"} & set(a.blocks):
        uit_ids, _, uit_inst = uitviic(("train",))
        en, split, gold = coco_sources(set(uit_ids))
        test = sorted(k for k, s in split.items() if s == "test")
        rel = reliable_classes(en, split, gold)
        fams = {"all": None, "reliable": frozenset(rel), "reliable_noperson": frozenset(rel) - {"person"}}
        man = {str(x["cocoid"]) for x in json.loads((ROOT / "data/coco_probe/manifest.json").read_text())["images"]}
        if "coco" in a.blocks:
            print(f"COCO Karpathy test ({len(test)}), English; reliable classes ({len(rel)}) from Karpathy val", flush=True)
            out["coco"] = {"reliable_classes": rel, "test5000": targets(test, en, gold, en_obj, fams, a.B)}
            x = fold_array(test, en, gold, en_obj, None, policy_systems(en_obj))
            out["coco"]["tau_by_scene_classes"] = tau_buckets(x, np.array([len(gold[i]) for i in test]), a.B)
            sub = [i for i in test if i in man]
            out["coco"]["manifest2500_tau"] = {f: summ(diff(stats(fold_array(sub, en, gold, en_obj, fam, policy_systems(en_obj)),
                                                                  weights(len(sub), a.B)), list(POLICIES), "p1", "fuse2")["tau_I"])
                                               for f, fam in fams.items()}
            uit_en = sorted(i for i in uit_ids if i in en)
            print(f"UIT-ViIC train, English COCO captions ({len(uit_en)} images)", flush=True)
            out["uitviic_en"] = targets(uit_en, en, uit_inst, en_obj, fams_uit, a.B)
            print("second-panel estimator vs instance truth (COCO test)", flush=True)
            out["panel_validate"] = panel_validate(test, en, gold, a.B)
        if "coco_models" in a.blocks:
            sub = sorted(i for i in test if i in man)
            out["coco_models"] = {f: model_block((sub, en, gold, en_obj, fam), Path(a.coco_results).expanduser(),
                                                 a.coco_pair, a.B, "coco") for f, fam in fams.items() if f != "reliable_noperson"}
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"-> {a.out}")
    return 0


def _check() -> None:
    a, i = frozenset({"chó", "người"}), frozenset({"người", "xe"})
    assert counts(frozenset({"chó", "xe", "mèo"}), a, i) == [3, 1, 1, 2, 0.5, 1.0, 0.5, 1.0, 2 / 3, 1.0]
    cs = ["một người đàn ông và con chó.", "người đàn ông đứng.", "con chó cạnh chiếc xe máy"]
    assert rows_of("p1", cs, ktvic_obj, random.Random(0)) == [frozenset({"đàn ông", "chó"})]
    assert rows_of("fuse2", cs, ktvic_obj, None) == [frozenset({"đàn ông", "chó", "xe máy"})]
    assert len(rows_of("unf2", cs, ktvic_obj, None)) == 2 and len(rows_of("multiref", cs, ktvic_obj, None)) == 3
    assert vi_obj("Cầu thủ đang ghi bàn", True) == {"person"} and "dining table" in vi_obj("Cầu thủ đang ghi bàn", False)
    # two systems on 2 images, 10 identical folds: B names one more A-false mention that I confirms
    x = np.zeros((2, 10, 2, len(FIELDS)))
    x[:, :, 0] = counts(frozenset({"chó"}), a, i)
    x[:, :, 1] = counts(frozenset({"chó", "xe"}), a, i)
    st = stats(x, weights(2, 50))
    assert st["P_A"][0].tolist() == [100.0, 50.0] and st["P_U"][0].tolist() == [100.0, 100.0]
    d = diff(st, ["a", "b"], "a", "b")
    assert d["false_A"][0] == 1 and d["false_I"][0] == 0 and d["tau_I"][0] == 0 and st["conf"][0, 1] == 100
    assert summ(np.array([1.0] * 51), test=True) == [1.0, [1.0, 1.0], 0.04]
    sw = seed_weights(3, 5, np.random.default_rng(0))
    assert sw.shape == (5, 3) and np.allclose(sw.sum(1), 1) and np.allclose(sw[0], 1 / 3)
    res = {"contrasts": {"short": {"x": {"P_I": {"model_ci90": [-1, 2]}, "R_I": {"model": [5, [1, 9]]}}},
                         "two-sentence": {"x": {"P_I": {"DiD": [-1, [-2.5, 0.5]]}, "tau_I": {"model": [0.2, [0.1, 0.4]]}}}}}
    assert verdicts(res, "uit") == {"G3a": "pass", "G3b": "pass", "G3c": "mostly typicality"}


if __name__ == "__main__":
    _check()
    sys.exit(main())
