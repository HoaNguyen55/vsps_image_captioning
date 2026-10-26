#!/usr/bin/env python
# PATCHED COPY for Paper A CC-108 W3 (2026-10-26) of .session_backup/2026-10-14/r11_litmaps/L1/scripts/check_coco.py.
# Estimator unchanged. Edits: import check_mstar from the original folder; manifest, instance gold, system set and
# output path from argv; assert every system covers every manifest id; extra output keys "U" (gold size over ALL
# images, the A3.3 v2 line) and "tables" (per-system P, R, F1, M), both additive. See check_coco_full.diff.
# CP-111: optional FULL_DIR, the merged adapter directory read by all9full (default data/results/coco_transfer_full5000),
# so the W4 selftest can score a scratch merge.
# Run: python check_coco_full.py MANIFEST INSTANCE_GOLD {all9|five|all9full} OUT_JSON [FULL_DIR]
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
    for d in {"all9": ("coco5000", "coco_transfer", "coco5000_vcd"), "five": ("coco5000", "coco5000_vcd"),
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
    for gname, golds in variants.items():
        rows = {s: [per_image(ments[s], g) for g in golds] for s in names}
        table = {s: tuple(np.mean([prf(r) for r in rows[s]], 0)) for s in names}
        gbar = float(np.mean([np.mean([len(x) for x in g if x]) for g in golds]))
        u_all = float(np.mean([np.mean([len(x) for x in g]) for g in golds]))
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
        out.setdefault("U", {})[gname] = round(u_all, 3)
        out.setdefault("tables", {})[gname] = {s: [float(x) for x in table[s]] for s in names}
        print(f"{gname:14s} Gbar {res['Gbar']:.2f} b {fit['b']:.3f} M*micro {fit['Mstar_micro']} M*mixed "
              f"{fit['Mstar_mixed']} Mrange {fit['M_range']} median {res['median_M']} | corr {res['corr_logM_F1']:+.2f} "
              f"slope {res['slope']:+.2f} {res['slope_ci']}", flush=True)
    Path(out_path).write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
