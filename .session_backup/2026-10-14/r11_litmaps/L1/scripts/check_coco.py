#!/usr/bin/env python
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
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


def main() -> None:
    vi, syn = sc.load_vi_terms(), sc.load_synonyms()
    cids = sorted(i["cocoid"] for i in json.loads((ROOT / "data/coco_probe/manifest.json").read_text("utf-8"))["images"])
    cinst = {int(k): set(v["coco"]) for k, v in
             json.loads((ROOT / "data/coco_probe/instance_gold.json").read_text()).items()}
    kr = karpathy_refs(set(cids))
    ref_sets = {c: [sc.en_classes(s, syn) for s in kr[c][:5]] for c in cids}
    ments = {}
    for d in ("coco5000", "coco_transfer", "coco5000_vcd"):
        for f in sorted((RES / d).glob("*.shard*.jsonl")):
            name = f.name.split(".shard")[0] + ("+vcd" if d == "coco5000_vcd" else "")
            ms = {}
            for line in f.read_text("utf-8").splitlines():
                r = json.loads(line)
                ms[r["cocoid"]] = sc.vi_objects(r["caption"], vi)
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
    for gname, golds in variants.items():
        rows = {s: [per_image(ments[s], g) for g in golds] for s in names}
        table = {s: tuple(np.mean([prf(r) for r in rows[s]], 0)) for s in names}
        gbar = float(np.mean([np.mean([len(x) for x in g if x]) for g in golds]))
        lm = np.log([table[s][3] for s in names]); f1 = np.array([table[s][2] for s in names])
        bs = []
        for wb in W[:NBOOT if len(golds) == 1 else 200]:
            t = np.array([prf(rows[s][rng.integers(len(golds))], wb) for s in names])
            bs.append(slope(np.log(t[:, 3]), t[:, 2]))
        fit = mstar(names, table, gbar)
        res = {"Gbar": round(gbar, 3), "corr_logM_F1": round(float(np.corrcoef(lm, f1)[0, 1]), 3),
               "slope": round(slope(lm, f1), 2), "slope_ci": [round(float(np.percentile(bs, q)), 2) for q in (2.5, 97.5)],
               "median_M": round(float(np.median(np.exp(lm))), 2), **fit}
        out["gold"][gname] = res
        print(f"{gname:14s} Gbar {res['Gbar']:.2f} b {fit['b']:.3f} M*micro {fit['Mstar_micro']} M*mixed "
              f"{fit['Mstar_mixed']} Mrange {fit['M_range']} median {res['median_M']} | corr {res['corr_logM_F1']:+.2f} "
              f"slope {res['slope']:+.2f} {res['slope_ci']}", flush=True)
    Path(__file__).resolve().parents[1].joinpath("check_coco.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
