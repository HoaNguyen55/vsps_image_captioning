"""R14-1 CPU feasibility: where KTVIC hallucination mass sits, and the precision bound of detector-based removal.

nice -n 19 python3 -I feas.py   (repo code imported from ROOT; data read from repo files only)
"""
import json
import os
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/mnt/d/vsps_image_captioning")
os.environ["NCS_DATA"] = str(ROOT / "data")
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from evaluate import references  # noqa: E402
from rescap.chair import _ancestors, _gold_objects, canonical, objects_in  # noqa: E402

R = ROOT / "data" / "results"
coco = json.loads((ROOT / "data/coco_probe/coco80_vi.json").read_text())
COCO_ALL, COCO_FIRST = set(), set()
for k, v in coco.items():
    if k.startswith("_") or not isinstance(v, list):
        continue
    for j, ph in enumerate(v):
        cls = set(objects_in(ph))
        COCO_ALL |= cls
        if j == 0:
            COCO_FIRST |= cls
OIV7 = {k for k in json.loads((ROOT / "data/xm3600/vi_oiv7_map.json").read_text()) if not k.startswith("_")}
PERSON_SUB = {c for c in OIV7 if "người" in _ancestors(c) and c != "người"}
panel_all = json.loads((ROOT / "data/ktvic_openviic_refs.json").read_text())


def cn(n):
    return canonical(n) or n


def analyse(name, preds, refs, panel, tags=None):
    out = {"name": name, "n": 0, "M": 0, "H": 0}
    rows = []  # per image: (gold set, mentions, halluc list)
    hall = Counter()
    for i, cap in preds.items():
        if i not in refs:
            continue
        gold = _gold_objects(refs[i])
        m = [cn(x) for x in dict.fromkeys(objects_in(cap))]
        h = [x for x in m if x not in gold]
        rows.append((i, gold, m, h))
        hall.update(h)
    M = sum(len(r[2]) for r in rows); H = sum(len(r[3]) for r in rows)
    out.update(n=len(rows), M=M, H=H, CHAIR_i=H / M)
    cats = {"coco_any": COCO_ALL, "coco_first": COCO_FIRST, "oiv7": OIV7, "person_sub": PERSON_SUB}
    for k, s in cats.items():
        out[f"Hshare_{k}"] = sum(1 for r in rows for x in r[3] if x in s) / H
    # panel: a 2nd human panel (OpenViIC) names it -> object really there (salience miss, a detector would CONFIRM)
    cov = [r for r in rows if r[0] in panel]
    hp = [(x, x in _gold_objects(panel[r[0]])) for r in cov for x in r[3]]
    out["panel_images"] = len(cov)
    out["H_on_panel_images"] = len(hp)
    out["H_panel_confirmed"] = sum(c for _, c in hp) / max(1, len(hp))
    for k, s in cats.items():
        sub = [c for x, c in hp if x in s]
        out[f"panel_confirmed_{k}"] = (sum(sub) / len(sub), len(sub)) if sub else None

    def apply(drop):  # drop(i, x, is_h) -> bool ; returns CHAIR_i, mention P, removed TP, removed H
        m2 = h2 = rtp = rh = 0
        for i, gold, m, h in rows:
            for x in m:
                ish = x in h
                if drop(i, x, ish):
                    rtp += not ish; rh += ish
                else:
                    m2 += 1; h2 += ish
        return {"CHAIR_i": h2 / m2, "P_mention": 1 - h2 / m2, "removed_TP": rtp, "removed_H": rh, "M_after": m2}
    out["UB_oracle_coco_any"] = apply(lambda i, x, ish: ish and x in COCO_ALL)
    out["UB_oracle_oiv7"] = apply(lambda i, x, ish: ish and x in OIV7)
    out["UB_oracle_oiv7_noperson_sub"] = apply(lambda i, x, ish: ish and x in OIV7 - PERSON_SUB)
    out["UB_oracle_all"] = apply(lambda i, x, ish: ish)
    # perfect PRESENCE detector over OIV7 classes: removes only hallucinations the panel does not confirm
    pg = {r[0]: _gold_objects(panel[r[0]]) for r in cov}
    out["UB_presence_oiv7_panelimgs"] = apply(
        lambda i, x, ish: i in pg and ish and x in OIV7 - PERSON_SUB and x not in pg[i])
    out["UB_presence_all_panelimgs"] = apply(lambda i, x, ish: i in pg and ish and x not in pg[i])
    out["panelimgs_base"] = apply(lambda i, x, ish: False) if False else None
    if tags is not None:
        tcls = {i: set().union(*[_ancestors(cn(c)) for t in ts for c in objects_in(t)]) if ts else set()
                for i, ts in tags.items()}

        def unsupported(i, x):
            return x in COCO_FIRST and not (_ancestors(x) & tcls.get(i, set()) or any(x in _ancestors(t) for t in tcls.get(i, set())))
        out["GDINO_remove_untagged_cocofirst"] = apply(lambda i, x, ish: unsupported(i, x))
        n_cf = sum(1 for r in rows for x in r[2] if x in COCO_FIRST)
        n_cf_h = sum(1 for r in rows for x in r[3] if x in COCO_FIRST)
        n_unsup = sum(1 for r in rows for x in r[2] if unsupported(r[0], x))
        n_unsup_h = sum(1 for r in rows for x in r[3] if unsupported(r[0], x))
        out["GDINO_cocofirst_mentions"] = {"all": n_cf, "halluc": n_cf_h, "untagged": n_unsup, "untagged_halluc": n_unsup_h}
        # bootstrap on dCHAIR_i for the GDINO rule
        rng = random.Random(0); d = []
        per = []
        for i, gold, m, h in rows:
            a = (len(m), len(h)); kept = [x for x in m if not unsupported(i, x)]
            per.append((a[0], a[1], len(kept), sum(x in h for x in kept)))
        for _ in range(1000):
            s = [per[rng.randrange(len(per))] for _ in per]
            d.append(sum(x[3] for x in s) / max(1, sum(x[2] for x in s)) - sum(x[1] for x in s) / sum(x[0] for x in s))
        d.sort(); out["GDINO_dCHAIR_i_CI95"] = (d[25], d[974])
    from object_prf import image_counts, scores
    ogold = {i: set().union(*[set(objects_in(r)) for r in refs[i]]) for i, *_ in rows}

    def prf_after(drop):
        rr = [image_counts({x for x in m if not drop(i, x, x in h)}, ogold[i], _ancestors) for i, g, m, h in rows]
        s = scores(rr); return {k: round(s[k], 2) for k in ("P", "R", "F1")}
    out["PRF_base"] = prf_after(lambda i, x, ish: False)
    out["PRF_UB_oracle_oiv7"] = prf_after(lambda i, x, ish: ish and x in OIV7)
    out["PRF_UB_presence_oiv7"] = prf_after(lambda i, x, ish: i in pg and ish and x in OIV7 - PERSON_SUB and x not in pg[i])
    out["PRF_UB_presence_all"] = prf_after(lambda i, x, ish: i in pg and ish and x not in pg[i])
    if tags is not None:
        out["PRF_GDINO_rule"] = prf_after(lambda i, x, ish: unsupported(i, x))
    pc = Counter(); pn = Counter()
    for i, gold, m, h in cov:
        g2 = pg[i]
        for x in h:
            pn[x] += 1; pc[x] += x in g2
    out["panel_conf_top"] = [(x, n, pc[x]) for x, n in pn.most_common(12)]
    out["top_halluc"] = [(x, n, x in COCO_ALL, x in OIV7) for x, n in hall.most_common(20)]
    return out


def preds_of(f):
    d = json.loads(Path(f).read_text())
    return {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in d.items()}


test_refs = references("test_data.json")
train_refs = references("train_data.json")
dev_ids = (ROOT / "data/splits/ktvic_dev300.txt").read_text().split()
dev_refs = {i: train_refs[i] for i in dev_ids}
tags = json.loads((R / "tags_gdino.json").read_text())
res = {"lexicon": {"COCO_any": len(COCO_ALL), "COCO_first": len(COCO_FIRST), "OIV7": len(OIV7), "person_sub": sorted(PERSON_SUB)}}
res["dev300_p1dev_s42"] = analyse("dev300", preds_of(R / "rl/p1dev_s42-dev300-short.preds.json"), dev_refs, panel_all["train"])
res["test_p1assist_s42"] = analyse("test", preds_of(R / "p1assist_s42-short.preds.json"), test_refs, panel_all["test"], tags)
res["test_fuse2_s42"] = analyse("test", preds_of(R / "fuse2_s42-short.preds.json"), test_refs, panel_all["test"], tags)
print(json.dumps(res, ensure_ascii=False, indent=1))
