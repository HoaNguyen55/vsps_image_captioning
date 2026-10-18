#!/usr/bin/env python3
"""H1 pilot: do count-controlled object metrics agree with EXISTING human judgments? (THumB 1.0 and Composite-COCO)

Predictions were frozen first in ../PREDICTIONS_FROZEN.txt. Object pipeline = the E1 CHAIR re-implementation (COCO-80 + CHAIR
synonyms, class level), copied from research_r10/E1/e1_chair_count.py because that module reads sys.argv at import.
Usage: python3 -I h1_pilot.py SYNONYMS INSTANCES_VAL2014_JSON KARPATHY_JSON THUMB_DIR COMPOSITE_ZIP OUT_JSON
"""
import csv
import io
import json
import re
import sys
import zipfile
from collections import defaultdict

import numpy as np

SYN, INST, KARP, THUMB, COMP, OUT = sys.argv[1:7]
NDRAW, NBOOT = 20, 2000

# ---------------- matcher (verbatim logic of E1 e1_chair_count.py) ----------------
inv = {}
for line in open(SYN):
    syns = [s.strip().lower() for s in line.split(",") if s.strip()]
    for s in syns:
        inv.setdefault(s, syns[0])
DOUBLE = {w: w for w in ['motor bike', 'motor cycle', 'air plane', 'traffic light', 'street light', 'traffic signal',
                         'stop light', 'fire hydrant', 'stop sign', 'parking meter', 'suit case', 'sports ball',
                         'baseball bat', 'baseball glove', 'tennis racket', 'wine glass', 'hot dog', 'cell phone',
                         'mobile phone', 'teddy bear', 'hair drier', 'potted plant', 'bow tie', 'laptop computer',
                         'stove top oven', 'home plate', 'train track']}
for a in ['bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'animal', 'cub']:
    DOUBLE[f'baby {a}'] = a
    DOUBLE[f'adult {a}'] = a
for v in ['jet', 'train']:
    DOUBLE[f'passenger {v}'] = v
DOUBLE['bow tie'] = 'tie'
DOUBLE['toilet seat'] = 'toilet'
VOCAB = set(inv) | {w for d in DOUBLE for w in d.split()}
IRREG = {'people': 'person', 'men': 'man', 'women': 'woman', 'children': 'child', 'mice': 'mouse', 'geese': 'goose',
         'teeth': 'tooth', 'feet': 'foot', 'knives': 'knife', 'leaves': 'leaf', 'shelves': 'shelf', 'oxen': 'ox',
         'skies': 'sky', 'buses': 'bus', 'glasses': 'glass', 'kids': 'kid', 'policemen': 'policeman'}


def sing(w):
    if w in IRREG:
        return IRREG[w]
    if w in VOCAB:
        return w
    for c in ([w[:-3] + 'y'] if w.endswith('ies') else []) + ([w[:-3] + 'f', w[:-3] + 'fe'] if w.endswith('ves') else []) \
            + ([w[:-2]] if w.endswith('es') else []) + ([w[:-1]] if w.endswith('s') else []):
        if c in VOCAB:
            return c
    return w


def classes(cap):
    ws = [sing(w) for w in re.findall(r"[a-z]+", cap.lower())]
    out, i = [], 0
    while i < len(ws):
        dw = ' '.join(ws[i:i + 2])
        if dw in DOUBLE:
            out.append(DOUBLE[dw])
            i += 2
        else:
            out.append(ws[i])
            i += 1
    if 'toilet' in out and 'seat' in out:
        out = [w for w in out if w != 'seat']
    return {inv[w] for w in out if w in inv}


assert classes("Two men riding motor bikes past a dining table.") == {'person', 'motorcycle', 'dining table'}
assert classes("A baby elephant next to a toilet seat and some doughnuts") == {'elephant', 'toilet', 'donut'}


# ---------------- gold ----------------
def instance_gold(want):
    """Stream instances_val2014.json (never json.load the 160 MB file); E1's regex on the official key order."""
    pat = re.compile(r'"image_id":\s*(\d+),\s*"bbox":\s*\[[^\]]*\],\s*"category_id":\s*(\d+)')
    pairs, cat, tail = set(), {}, ''
    with open(INST, encoding='utf-8', errors='ignore') as fh:
        while True:
            chunk = fh.read(1 << 22)
            if not chunk:
                break
            buf = tail + chunk
            pairs.update((int(a), int(b)) for a, b in pat.findall(buf) if int(a) in want)
            cat.update({int(a): b for a, b in re.findall(r'"id":\s*(\d+),\s*"name":\s*"([^"]+)"', buf)})
            tail = buf[-4000:]
    gold = {i: set() for i in want}
    for im, c in pairs:
        gold[im].add(inv.get(cat[c], cat[c]))
    return gold


def karpathy_refs(want):
    """L1 check_coco.py approach: slice one image object at a time out of the 137 MB file."""
    text = open(KARP, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'"cocoid": (\d+)\}', text):
        c = int(m.group(1))
        if c in want:
            s = text.rfind('{"filepath"', 0, m.start())
            out[c] = [x["raw"] for x in json.loads(text[s:m.end()])["sentences"]]
    return out


def norm(s):
    return ' '.join(re.findall(r"[a-z0-9]+", s.lower()))


# ---------------- datasets ----------------
def load_thumb():
    rows = [json.loads(x) for x in open(f'{THUMB}/mscoco_mscoco_THumB-1.0.jsonl')]
    refs = {int(r['seg_id']): r['refs'] for r in map(json.loads, open(f'{THUMB}/mscoco_mscoco_references.json').read().splitlines())}
    caps = [{'img': int(r['seg_id']), 'sys': r['SYS'], 'text': r['hyp'], 'P': r['P'], 'R': r['R'], 'T': r['human_score']}
            for r in rows]
    return caps, refs


def load_composite():
    z = zipfile.ZipFile(COMP)
    rat = {}
    for fn, key in (('coco_correctness.csv', 'P'), ('coco_throughness.csv', 'R')):
        r = list(csv.reader(io.StringIO(z.read(fn).decode('utf-8', 'replace')), delimiter=';'))
        h = {c: k for k, c in enumerate(r[0])}
        for row in r[1:]:
            mm = re.search(r'(\d+)\.jpg', row[h['Input.image_url']]) if len(row) > h['Input.image_url'] else None
            if not mm:
                continue  # 2 empty rows per file
            im = int(mm.group(1))
            for q in range(1, 5):
                t, a = row[h[f'Input.text{q}']], row[h[f'Answer.Q{q}Answer']]
                if t.strip() and a.strip().isdigit():
                    rat.setdefault((im, norm(t)), {'text': t, 'slot': q, 'P': [], 'R': []})[key].append(int(a))
    caps = [{'img': im, 'sys': f'text{v["slot"]}', 'text': v['text'], 'P': np.mean(v['P']), 'R': np.mean(v['R']),
             'T': (np.mean(v['P']) + np.mean(v['R'])) / 2} for (im, _), v in rat.items() if v['P'] and v['R']]
    kr = karpathy_refs({c['img'] for c in caps})
    cand = defaultdict(set)
    for c in caps:
        cand[c['img']].add(norm(c['text']))
    refs = {im: [r for r in rs if norm(r) not in cand[im]][:4] for im, rs in kr.items()}
    caps = [c for c in caps if len(refs.get(c['img'], [])) >= 4]
    return caps, refs


# ---------------- metrics ----------------
def build(caps, refs, inst, rng):
    imgs = sorted({c['img'] for c in caps})
    rcls = {i: [classes(r) for r in refs[i]] for i in imgs}
    golds = {'inst': [{i: inst[i] for i in imgs}], 'refs4': [{i: set().union(*rcls[i]) for i in imgs}]}
    golds['full'] = [{i: inst[i] | golds['refs4'][0][i] for i in imgs}]
    for k in (1, 2):
        golds[f'refs{k}'] = [{i: set().union(*[rcls[i][j] for j in rng.choice(len(rcls[i]), k, replace=False)]) for i in imgs}
                             for _ in range(NDRAW)]
    cl = [classes(c['text']) for c in caps]
    M = np.array([len(x) for x in cl], float)
    met = {}
    for g, draws in golds.items():
        TP = np.array([[len(cl[n] & d[c['img']]) for d in draws] for n, c in enumerate(caps)], float)
        G = np.array([[len(d[c['img']]) for d in draws] for c in caps], float)
        FP = M[:, None] - TP
        chair = np.where(M[:, None] > 0, FP / np.maximum(M[:, None], 1), 0.0)
        f1 = np.where(M[:, None] + G > 0, 2 * TP / np.maximum(M[:, None] + G, 1), 1.0)
        mc = np.minimum(M, 6)
        z = np.empty_like(TP)
        for d in range(TP.shape[1]):
            fr = {m: TP[mc == m, d].mean() for m in np.unique(mc)}
            z[:, d] = TP[:, d] - np.array([fr[m] for m in mc])
        met[g] = {'TP': TP, 'FP': FP, 'G': G, 'negCHAIR': -chair, 'F1': f1, 'z': z, 'R_obj': np.where(G > 0, TP / np.maximum(G, 1), 0)}
    pfp1 = np.array([[len(cl[n] & (golds['full'][0][c['img']] - d[c['img']])) for d in golds['refs1']] for n, c in enumerate(caps)],
                    float).mean(1)
    return imgs, golds, cl, M, met, pfp1


def pairs_of(caps, imgs):
    idx = {i: k for k, i in enumerate(imgs)}
    by = defaultdict(list)
    for n, c in enumerate(caps):
        by[c['img']].append(n)
    pa, pb, pi = [], [], []
    for im, ns in by.items():
        for x in range(len(ns)):
            for y in range(x + 1, len(ns)):
                pa.append(ns[x]); pb.append(ns[y]); pi.append(idx[im])
    return np.array(pa), np.array(pb), np.array(pi)


class Agree:
    """Per-image concordant/discordant counts -> image-bootstrap accuracy (mean over gold draws)."""

    def __init__(self, n_img, pi, W):
        self.n, self.pi, self.W = n_img, pi, W

    def counts(self, dX, dH, mask):
        dX = dX if dX.ndim == 2 else dX[:, None]
        s = np.sign(dX) * np.sign(dH)[:, None]
        m = mask[:, None]
        conc = np.stack([np.bincount(self.pi, (s[:, d] > 0) & m[:, 0], self.n) for d in range(s.shape[1])], 1)
        disc = np.stack([np.bincount(self.pi, (s[:, d] < 0) & m[:, 0], self.n) for d in range(s.shape[1])], 1)
        return conc, disc

    def acc(self, cd, W=None):
        conc, disc = cd
        W = np.ones((1, self.n)) if W is None else W
        with np.errstate(invalid='ignore'):
            return np.nanmean((W @ conc) / (W @ (conc + disc)), axis=1)

    def summary(self, cd, cd2=None):
        pt = float(self.acc(cd)[0]) - (float(self.acc(cd2)[0]) if cd2 else 0.0)
        bs = self.acc(cd, self.W) - (self.acc(cd2, self.W) if cd2 else 0.0)
        n_untied = int(cd[0].sum() + cd[1].sum()) // cd[0].shape[1]
        return {'est': round(pt, 4), 'ci': [round(float(np.nanpercentile(bs, q)), 4) for q in (2.5, 97.5)], 'n_untied': n_untied}


def analyse(name, caps, refs, inst, out):
    rng = np.random.default_rng(0)
    imgs, golds, cl, M, met, pfp1 = build(caps, refs, inst, rng)
    pa, pb, pi = pairs_of(caps, imgs)
    W = rng.multinomial(len(imgs), np.full(len(imgs), 1 / len(imgs)), size=NBOOT).astype(float)
    ag = Agree(len(imgs), pi, W)
    H = {k: np.array([c[k] for c in caps], float) for k in ('P', 'R', 'T')}
    dH = {k: v[pa] - v[pb] for k, v in H.items()}
    dM = M[pa] - M[pb]
    cdiff, call, ceq = dM != 0, np.ones(len(pa), bool), dM == 0
    d = lambda g, m: met[g][m][pa] - met[g][m][pb]
    res = {'n_img': len(imgs), 'n_cap': len(caps), 'n_pairs': len(pa), 'n_count_differing': int(cdiff.sum())}
    # descriptive per system
    sysn = sorted({c['sys'] for c in caps})
    sv = np.array([c['sys'] for c in caps])
    res['systems'] = {s: {'M': round(M[sv == s].mean(), 3), 'P_h': round(H['P'][sv == s].mean(), 3),
                          'R_h': round(H['R'][sv == s].mean(), 3), 'T_h': round(H['T'][sv == s].mean(), 3),
                          **{f'Pobj_{g}': round(float(np.mean(met[g]['TP'][sv == s].sum(0) / max(M[sv == s].sum(), 1))), 4)
                             for g in met},
                          **{f'Robj_{g}': round(float(met[g]['R_obj'][sv == s].mean()), 4) for g in met}} for s in sysn}
    res['M_hist'] = {int(k): int(v) for k, v in zip(*np.unique(np.minimum(M, 6), return_counts=True))}
    res['frontier_full'] = {int(m): round(float(met['full']['TP'][np.minimum(M, 6) == m, 0].mean()), 3) for m in np.unique(np.minimum(M, 6))}
    # full agreement table: metric x gold x human scale x pair subset
    tab = {}
    for g in met:
        for m in ('negCHAIR', 'F1', 'z', 'R_obj'):
            for h in ('P', 'R', 'T'):
                for sub, mask in (('all', call), ('cdiff', cdiff), ('ceq', ceq)):
                    tab[f'{m}|{g}|{h}|{sub}'] = ag.summary(ag.counts(d(g, m), dH[h], mask))
    res['agree'] = tab
    # P1
    cP_ch, cP_z = ag.counts(d('full', 'negCHAIR'), dH['P'], cdiff), ag.counts(d('full', 'z'), dH['P'], cdiff)
    cT_ch, cT_z = ag.counts(d('full', 'negCHAIR'), dH['T'], cdiff), ag.counts(d('full', 'z'), dH['T'], cdiff)
    res['P1a_acc(-CHAIR->P)-acc(z->P)'] = ag.summary(cP_ch, cP_z)
    res['P1b_acc(z->T)-acc(-CHAIR->T)'] = ag.summary(cT_z, cT_ch)
    # P2
    res['P2a_v_human'] = ag.summary(ag.counts(dH['T'], dM, cdiff))
    res['P2a_v_human_P'] = ag.summary(ag.counts(dH['P'], dM, cdiff))
    res['P2a_v_human_R'] = ag.summary(ag.counts(dH['R'], dM, cdiff))
    for g in ('refs1', 'refs2', 'refs4', 'inst', 'full'):
        res[f'P2b_v_F1_{g}'] = ag.summary(ag.counts(d(g, 'F1'), dM, cdiff))
        res[f'P2b_v_negCHAIR_{g}'] = ag.summary(ag.counts(d(g, 'negCHAIR'), dM, cdiff))
        res[f'P2b_v_z_{g}'] = ag.summary(ag.counts(d(g, 'z'), dM, cdiff))
    res['P2c_acc(F1_full->T)-acc(F1_refs1->T)'] = ag.summary(ag.counts(d('full', 'F1'), dH['T'], cdiff),
                                                             ag.counts(d('refs1', 'F1'), dH['T'], cdiff))
    res['P2c_acc(z_full->T)-acc(z_refs1->T)'] = ag.summary(ag.counts(d('full', 'z'), dH['T'], cdiff),
                                                           ag.counts(d('refs1', 'z'), dH['T'], cdiff))
    # P3: OLS P_h ~ 1 + FP_full + PFP1 + TP_full, image-cluster bootstrap
    X = np.column_stack([np.ones(len(caps)), met['full']['FP'][:, 0], pfp1, met['full']['TP'][:, 0]])
    ci = np.array([imgs.index(c['img']) for c in caps])
    ols = lambda w, y: np.linalg.solve((X * w[:, None]).T @ X, (X * w[:, None]).T @ y)
    for h in ('P', 'R', 'T'):
        b0 = ols(np.ones(len(caps)), H[h])
        bs = np.array([ols(W[k][ci], H[h]) for k in range(NBOOT)])
        res[f'P3_ols_{h}'] = {n: {'est': round(float(b0[j]), 4), 'ci': [round(float(np.percentile(bs[:, j], q)), 4) for q in (2.5, 97.5)]}
                              for j, n in enumerate(['const', 'FP_full', 'PFP_refs1', 'TP_full'])}
        db = bs[:, 2] - bs[:, 1]
        res[f'P3_ols_{h}']['PFP-FP'] = {'est': round(float(b0[2] - b0[1]), 4), 'ci': [round(float(np.percentile(db, q)), 4) for q in (2.5, 97.5)]}
    res['PFP1_mean'] = round(float(pfp1.mean()), 4)
    # P4: clean matched-count CHAIR wins vs count-confounded CHAIR wins (full gold)
    FP, TP, CH = met['full']['FP'][:, 0], met['full']['TP'][:, 0], -met['full']['negCHAIR'][:, 0]
    a_better = lambda a, b: (FP[a] < FP[b])
    clean = (M[pa] == M[pb]) & (FP[pa] != FP[pb])
    conf_ab = (FP[pa] < FP[pb]) & (TP[pa] < TP[pb]) & (CH[pa] < CH[pb])
    conf_ba = (FP[pb] < FP[pa]) & (TP[pb] < TP[pa]) & (CH[pb] < CH[pa])
    conf_ab_nc = (FP[pa] < FP[pb]) & (TP[pa] < TP[pb])
    conf_ba_nc = (FP[pb] < FP[pa]) & (TP[pb] < TP[pa])
    win = np.where(a_better(pa, pb), 1.0, -1.0)  # +1: CHAIR prefers a (fewer FP)
    for nm, mask, sgn in (('clean', clean, win), ('confounded', conf_ab | conf_ba, np.where(conf_ab, 1.0, -1.0)),
                          ('confounded_noCHAIRcond', conf_ab_nc | conf_ba_nc, np.where(conf_ab_nc, 1.0, -1.0))):
        for h in ('T', 'P', 'R'):
            res[f'P4_{nm}_{h}'] = ag.summary(ag.counts(sgn, dH[h], mask))
    cc = ag.counts(win, dH['T'], clean)
    cf = ag.counts(np.where(conf_ab, 1.0, -1.0), dH['T'], conf_ab | conf_ba)
    res['P4_clean-confounded_T'] = ag.summary(cc, cf)
    # P5 (system level) handled from res['systems']
    # caption-level correlations for comparison with THumB Table 4
    from scipy.stats import pearsonr, spearmanr
    cor = {}
    for g in ('refs1', 'refs4', 'full'):
        for m in ('negCHAIR', 'F1', 'z', 'R_obj'):
            x = met[g][m].mean(1)
            for h in ('P', 'R', 'T'):
                cor[f'{m}|{g}|{h}'] = [round(float(pearsonr(x, H[h])[0]), 3), round(float(spearmanr(x, H[h])[0]), 3)]
    cor['M|-|T'] = [round(float(pearsonr(M, H['T'])[0]), 3), round(float(spearmanr(M, H['T'])[0]), 3)]
    cor['M|-|P'] = [round(float(pearsonr(M, H['P'])[0]), 3), round(float(spearmanr(M, H['P'])[0]), 3)]
    cor['M|-|R'] = [round(float(pearsonr(M, H['R'])[0]), 3), round(float(spearmanr(M, H['R'])[0]), 3)]
    res['corr_pearson_spearman'] = cor
    out[name] = res
    print(f'== {name}: {len(imgs)} images, {len(caps)} captions, {len(pa)} pairs, {int(cdiff.sum())} count-differing', flush=True)
    for k, v in res.items():
        if k.startswith(('P1', 'P2', 'P4')):
            print(f'{k:42s} {v}', flush=True)
    for h in ('P', 'R', 'T'):
        print(f'P3_ols_{h}', res[f'P3_ols_{h}'], flush=True)
    for s, v in res['systems'].items():
        print(s, v, flush=True)


def main():
    out = {}
    tc, tr = load_thumb()
    cc, cr = load_composite()
    inst = instance_gold({c['img'] for c in tc} | {c['img'] for c in cc})
    print(f'instances: {sum(bool(v) for v in inst.values())}/{len(inst)} images with labels', flush=True)
    analyse('THumB', tc, tr, inst, out)
    analyse('Composite', cc, cr, inst, out)
    json.dump(out, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
