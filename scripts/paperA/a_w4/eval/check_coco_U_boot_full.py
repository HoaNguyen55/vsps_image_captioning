#!/usr/bin/env python
# PATCHED COPY for Paper A CP-111 W4 (2026-10-26) of .session_backup/2026-10-18/paperA_tasks/A3.3/check_coco_U_boot.py
# (the A3.3 v3 post hoc bootstrap behind the sec4.3 channel-split and Lambda intervals). Estimator, RNG order and
# bootstrap unchanged. Edits: manifest, instance gold, system set, output path and optional FULL_DIR from argv, as in
# check_coco_full.py; coverage assert. See check_coco_U_boot_full.diff.
# Run: python check_coco_U_boot_full.py MANIFEST INSTANCE_GOLD {all9|all9full} OUT_JSON [FULL_DIR]
# PATCHED COPY for Paper A task A3.3 v2 (2026-10-18) of .session_backup/2026-10-14/r11_litmaps/L1/scripts/check_coco.py.
# One change of method: gold size averaged over ALL images (U) instead of images with a non-empty gold.
# The other edits only import check_mstar from the original folder, rename the output key and write next to this copy.
# A3.3 v3 copy of check_coco_U.py: adds boot(), a post hoc image bootstrap run after the original loop, and keeps the
# per-image rows for it; the estimator is unchanged. See check_coco_U_boot.diff.
"""L1 check 1b (out-of-sample for direction C): COCO-2500, same statistic as check_mstar.py.

Predictions were written to ../check_coco_PREDICTIONS.txt before this ran. Systems and gold are G2's COCO-2500
setting (g2_frontier.py section 5): Vietnamese outputs mapped to COCO-80 by score_coco_probe.vi_objects, English
Karpathy references mapped by en_classes, instance labels from data/coco_probe/instance_gold.json. Read-only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/mnt/d/vsps_image_captioning/.session_backup/2026-10-14/r11_litmaps/L1/scripts")
from check_mstar import ROOT, mstar, per_image, prf, slope  # noqa: E402

sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
import score_coco_probe as sc  # noqa: E402

RES, DS = ROOT / "data/results", ROOT / "data/datasets"
NBOOT, NSUB = 500, 20


def karpathy_refs(want: set[int]) -> dict[int, list[str]]:
    """Copied from G2 g2_frontier.py: raw references of `want`, one image object parsed at a time."""
    text = (DS / "karpathy/dataset_coco.json").read_text()
    out = {}
    for m in re.finditer(r'"cocoid": (\d+)\}', text):
        c = int(m.group(1))
        if c in want:
            s = text.rfind('{"filepath"', 0, m.start())
            out[c] = [x["raw"] for x in json.loads(text[s:m.end()])["sentences"]]
    return out


BOOT_B, BOOT_SEED, BOOT_CI = 2000, 20261018, 95
BOOT_GOLDS = ("refs1_randk", "refs2_randk", "refs3_randk", "refs4_randk", "refs5_randk", "inst", "inst+refs5")
BOOT_SHARES = {"refs1_to_refs5": ("refs1_randk", "refs5_randk"), "refs1_to_inst": ("refs1_randk", "inst")}


def logit(p):
    return np.log(p / (1 - p))


def boot(keep: dict, variants: dict, names: list, n: int) -> dict:
    """A3.3 v3: post hoc image bootstrap of the v2 estimator. Uncertainty only, not a registered test.

    Row 0 of W is the point estimate (all weights 1). For each replicate and gold, as in main(): table = mean over the
    gold's draws of prf(rows, w); b = mstar's b; U = weighted mean gold size over ALL images (the v2 line); M0 = median
    over systems of M; Lambda_U = logit(b) + ln U - ln M0. The micro-F1 slope is the OLS slope over systems of
    200 * TP / (M + U) on ln M (the h4_check.py T2 formula), with TP = mean over draws of TP per image.
    """
    rng = np.random.default_rng(BOOT_SEED)
    W = np.vstack([np.ones(n), rng.multinomial(n, np.full(n, 1 / n), size=BOOT_B)]).astype(float)
    sizes = {g: np.array([[len(x) for x in d] for d in variants[g]], float) for g in BOOT_GOLDS}
    rep = {q: np.empty((len(W), len(BOOT_GOLDS))) for q in ("b", "U", "Lambda_U", "micro_F1_slope")}
    m0 = np.empty(len(W))
    for r, w in enumerate(W):
        for j, g in enumerate(BOOT_GOLDS):
            table = {s: tuple(np.mean([prf(x, w) for x in keep[g][s]], 0)) for s in names}
            m = np.array([table[s][3] for s in names])
            tp = np.array([table[s][0] for s in names]) / 100 * m
            u = float(np.mean(sizes[g] @ w) / w.sum())
            b = mstar(names, table, u)["b"]
            m0[r] = float(np.median(m))
            rep["b"][r, j], rep["U"][r, j] = b, u
            rep["Lambda_U"][r, j] = logit(b) + np.log(u) - np.log(m0[r])
            rep["micro_F1_slope"][r, j] = slope(np.log(m), 200 * tp / (m + u))
    pct = ((100 - BOOT_CI) / 2, 100 - (100 - BOOT_CI) / 2)

    def summ(v):
        return {"point": round(float(v[0]), 4), "ci": [round(float(np.percentile(v[1:], p)), 4) for p in pct]}

    res = {"label": "post hoc uncertainty, not a registered test", "B": BOOT_B, "seed": BOOT_SEED, "ci_level": BOOT_CI,
           "ci_method": "percentile over replicates 1..B; replicate 0 is the point estimate",
           "weights": "image multiplicities, multinomial(n, 1/n); each image keeps its random-k draws",
           "n_images": n, "M0": summ(m0), "gold": {g: {q: summ(v[:, j]) for q, v in rep.items()}
                                                 for j, g in enumerate(BOOT_GOLDS)}, "shares": {}}
    for c, (lo, hi) in BOOT_SHARES.items():
        a, z = BOOT_GOLDS.index(lo), BOOT_GOLDS.index(hi)
        db = logit(rep["b"][:, z]) - logit(rep["b"][:, a])
        dg = np.log(rep["U"][:, z] / rep["U"][:, a])
        res["shares"][c] = {"endpoints": [lo, hi], "dLambda_b": summ(db), "dLambda_G_U": summ(dg),
                            "b_channel_share": summ(db / (db + dg))}
    k1 = BOOT_GOLDS.index("refs1_randk")
    res["refs1_randk_share_of_replicates_with_opposite_signs"] = round(float(np.mean(
        np.sign(rep["Lambda_U"][1:, k1]) != np.sign(rep["micro_F1_slope"][1:, k1]))), 4)
    return res


def main() -> None:
    vi, syn = sc.load_vi_terms(), sc.load_synonyms()
    manifest, gold_file, sysset, out_path = sys.argv[1:5]
    full_dir = sys.argv[5] if len(sys.argv) > 5 else "coco_transfer_full5000"
    cids = sorted(i["cocoid"] for i in json.loads(Path(manifest).read_text("utf-8"))["images"])
    cinst = {int(k): set(v["coco"]) for k, v in json.loads(Path(gold_file).read_text()).items()}
    assert set(cids) <= set(cinst), "instance gold misses manifest ids"
    kr = karpathy_refs(set(cids))
    ref_sets = {c: [sc.en_classes(s, syn) for s in kr[c][:5]] for c in cids}
    ments = {}
    for d in {"all9": ("coco5000", "coco_transfer", "coco5000_vcd"),
              "all9full": ("coco5000", full_dir, "coco5000_vcd")}[sysset]:
        for f in sorted((RES / d).glob("*.shard*.jsonl")):
            name = f.name.split(".shard")[0] + ("+vcd" if d == "coco5000_vcd" else "")
            ms = {}
            for line in f.read_text("utf-8").splitlines():
                r = json.loads(line)
                ms[r["cocoid"]] = sc.vi_objects(r["caption"], vi)
            assert set(cids) <= set(ms), f"{name} misses {len(set(cids) - set(ms))} manifest ids"
            ments[name] = [ms.get(c, set()) for c in cids]
    names = list(ments)
    rng = np.random.default_rng(1)
    W = rng.multinomial(len(cids), np.full(len(cids), 1 / len(cids)), size=NBOOT).astype(float)
    variants = {"inst": [[cinst.get(c, set()) for c in cids]],
                "inst+refs5": [[cinst.get(c, set()) | set().union(*ref_sets[c]) for c in cids]]}
    for k in range(1, 6):
        variants[f"refs{k}_firstk"] = [[set().union(*ref_sets[c][:k]) for c in cids]]
        variants[f"refs{k}_randk"] = [[set().union(*[ref_sets[c][j] for j in rng.choice(len(ref_sets[c]), k,
                                                                                     replace=False)])
                                       for c in cids] for _ in range(NSUB)]
    out = {"n_img": len(cids), "systems": names, "gold": {}}
    keep = {}
    for gname, golds in variants.items():
        rows = {s: [per_image(ments[s], g) for g in golds] for s in names}
        keep[gname] = rows
        table = {s: tuple(np.mean([prf(r) for r in rows[s]], 0)) for s in names}
        gbar = float(np.mean([np.mean([len(x) for x in g]) for g in golds]))
        lm = np.log([table[s][3] for s in names]); f1 = np.array([table[s][2] for s in names])
        bs = []
        for wb in W[:NBOOT if len(golds) == 1 else 200]:
            t = np.array([prf(rows[s][rng.integers(len(golds))], wb) for s in names])
            bs.append(slope(np.log(t[:, 3]), t[:, 2]))
        fit = mstar(names, table, gbar)
        res = {"U": round(gbar, 3), "corr_logM_F1": round(float(np.corrcoef(lm, f1)[0, 1]), 3),
               "slope": round(slope(lm, f1), 2), "slope_ci": [round(float(np.percentile(bs, q)), 2) for q in (2.5, 97.5)],
               "median_M": round(float(np.median(np.exp(lm))), 2), **fit}
        out["gold"][gname] = res
        print(f"{gname:14s} U {res['U']:.2f} b {fit['b']:.3f} M*micro {fit['Mstar_micro']} M*mixed "
              f"{fit['Mstar_mixed']} Mrange {fit['M_range']} median {res['median_M']} | corr {res['corr_logM_F1']:+.2f} "
              f"slope {res['slope']:+.2f} {res['slope_ci']}", flush=True)
    out["bootstrap"] = boot(keep, variants, names, len(cids))
    Path(out_path).write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
