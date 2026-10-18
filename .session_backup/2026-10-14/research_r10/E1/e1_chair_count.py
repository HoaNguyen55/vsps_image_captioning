"""E1: count-controlled re-evaluation of released LVLM caption outputs (CHAIR protocol, COCO val2014).

Re-implements CHAIR (Rohrbach et al. 2018 rules: synonyms, double words, baby/adult/passenger, toilet seat) without
nltk/pattern (regex tokens + vocabulary-aware singularisation), then compares each method with its own baseline
at matched object count:
  MCP  per image k* = min(#classes_X, #classes_B); precision of the first k* distinct classes of each caption.
  TRF  baseline truncation frontier: truncate baseline captions after k distinct classes (k = 1..K), interpolate TP at the
       method's mean count (log-log); residual = TP_X - TP_B(M_X).
Usage: python3 -I e1_chair_count.py SYNONYMS COCO_ZIP OPERA_DIR LIM_DIR OUT_JSON
"""
import json, re, sys, zipfile
from pathlib import Path
import numpy as np

SYN, ZIP, OPERA, LIM, OUT = sys.argv[1:6]
lines = [l.strip() for l in open(SYN) if l.strip()]
inv = {}
for l in lines:
    syns = [s.strip().lower() for s in l.split(",") if s.strip()]
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
    # ponytail: vocabulary-aware singulariser instead of pattern.en; exact only for words that can reach the CHAIR vocab
    if w in IRREG:
        return IRREG[w]
    if w in VOCAB:
        return w
    for c in ([w[:-3] + 'y'] if w.endswith('ies') else []) + ([w[:-3] + 'f', w[:-3] + 'fe'] if w.endswith('ves') else []) \
            + ([w[:-2]] if w.endswith('es') else []) + ([w[:-1]] if w.endswith('s') else []):
        if c in VOCAB:
            return c
    return w


def nodes(cap):
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
    return [inv[w] for w in out if w in inv]


def load_systems():
    sysd = {}
    for f in sorted(Path(OPERA).glob('*.jsonl')):
        sysd['opera/' + f.stem] = {int(r['image_id']): r['caption'] for r in map(json.loads, f.open())}
    for f in sorted(Path(LIM).glob('r*.jsonl')):
        sysd['lim/' + f.stem] = {int(re.sub(r'\D', '', r['image_id'].split('.')[0])): r['text'] for r in map(json.loads, f.open())}
    return sysd


def load_gt(ids):
    z = zipfile.ZipFile(ZIP)
    caps = json.load(z.open('annotations/captions_val2014.json'))['annotations']
    gt = {i: set() for i in ids}
    for a in caps:
        if a['image_id'] in gt:
            gt[a['image_id']].update(nodes(a['caption']))
    cat, pairs, tail = {}, set(), ''
    pat = re.compile(r'"image_id":\s*(\d+),\s*"bbox":\s*\[[^\]]*\],\s*"category_id":\s*(\d+)')
    with z.open('annotations/instances_val2014.json') as fh:  # streamed: never holds the 160 MB JSON in memory
        while True:
            chunk = fh.read(1 << 22)
            if not chunk:
                break
            buf = tail + chunk.decode('utf-8', 'ignore')
            pairs.update((int(a), int(b)) for a, b in pat.findall(buf) if int(a) in gt)
            cat.update({int(a): b for a, b in re.findall(r'"id":\s*(\d+),\s*"name":\s*"([^"]+)"', buf)})
            tail = buf[-4000:]
    for im, c in pairs:
        gt[im].add(inv.get(cat[c], cat[c]))
    found = {im for im, _ in pairs}
    return gt, found


def per_image(cap, g):
    ns = nodes(cap)
    uniq = list(dict.fromkeys(ns))
    return {'n': len(ns), 'h': sum(n not in g for n in ns), 'u': uniq, 'tp': [n in g for n in uniq],
            'len': len(cap.split()), 'g': len(g)}


def agg(rows):
    n = sum(r['n'] for r in rows); h = sum(r['h'] for r in rows)
    M = np.mean([len(r['u']) for r in rows]); TP = np.mean([sum(r['tp']) for r in rows])
    R = 100 * sum(sum(r['tp']) for r in rows) / sum(r['g'] for r in rows)
    return {'CHAIR_s': round(100 * np.mean([r['h'] > 0 for r in rows]), 1), 'CHAIR_i': round(100 * h / max(n, 1), 2),
            'Recall': round(R, 1), 'M_cls': round(M, 3), 'TP_cls': round(TP, 3), 'P_cls': round(100 * TP / M, 2),
            'F1_cls': round(2 * (100 * TP / M) * R / (100 * TP / M + R), 2), 'Len': round(np.mean([r['len'] for r in rows]), 1)}


def trunc_curve(rows, K=12):
    ks = np.array([[min(k, len(r['u'])) for r in rows] for k in range(1, K + 1)], float)
    tps = np.array([[sum(r['tp'][:k]) for r in rows] for k in range(1, K + 1)], float)
    return ks.mean(1), tps.mean(1)


def interp_loglog(Mc, Tc, m):
    Mc, idx = np.unique(Mc, return_index=True); Tc = Tc[idx]
    if m >= Mc[-1]:
        return np.nan  # method longer than the baseline's own captions: truncation cannot reach it
    return float(np.exp(np.interp(np.log(m), np.log(Mc), np.log(Tc))))


def compare(B, X, ids, rng, nboot=1000):
    ids = np.array(ids)
    kst = np.array([min(len(X[i]['u']), len(B[i]['u'])) for i in ids], float)
    tx = np.array([sum(X[i]['tp'][:int(k)]) for i, k in zip(ids, kst)], float)
    tb = np.array([sum(B[i]['tp'][:int(k)]) for i, k in zip(ids, kst)], float)
    mX = np.array([len(X[i]['u']) for i in ids], float); tX = np.array([sum(X[i]['tp']) for i in ids], float)
    mB = np.array([len(B[i]['u']) for i in ids], float); tB = np.array([sum(B[i]['tp']) for i in ids], float)
    g = np.array([X[i]['g'] for i in ids], float)

    def stats(s):
        mcp = 100 * (tx[s].sum() - tb[s].sum()) / kst[s].sum()
        Mc, Tc = trunc_curve([B[i] for i in ids[s]])
        res = tX[s].mean() - interp_loglog(Mc, Tc, mX[s].mean())
        dP = 100 * (tX[s].sum() / mX[s].sum() - tB[s].sum() / mB[s].sum())
        dR = 100 * (tX[s].sum() - tB[s].sum()) / g[s].sum()
        return mcp, res, dP, dR, mX[s].mean() / mB[s].mean()
    full = stats(np.arange(len(ids)))
    boots = np.array([stats(rng.integers(0, len(ids), len(ids))) for _ in range(nboot)])
    lo, hi = np.nanpercentile(boots, [2.5, 97.5], axis=0)
    names = ['dP_matched_prefix', 'TP_resid_vs_trunc_frontier', 'dP_raw', 'dR_raw', 'M_ratio']
    return {n: [round(float(v), 3), round(float(a), 3), round(float(b), 3)] for n, v, a, b in zip(names, full, lo, hi)} | \
        {'n_img': len(ids), 'frac_imgs_X_shorter': round(float(np.mean(mX < mB)), 3)}


def main():
    sysd = load_systems()
    ids = set().union(*[set(v) for v in sysd.values()])
    gt, found = load_gt(ids)
    res = {'n_ids': len(ids), 'n_with_instances': len(found), 'systems': {}, 'pairs': {}}
    P = {}
    for s, caps in sysd.items():
        keep = [i for i in caps if i in found]
        P[s] = {i: per_image(caps[i], gt[i]) for i in keep}
        res['systems'][s] = agg(list(P[s].values())) | {'n_img': len(keep)}
    pairs = [(f'opera/{m}__{b}', f'opera/{m}__{x}') for m in ['instructblip', 'llava-1.5', 'minigpt4', 'shikra']
             for b, x in [('greedy', 'ours'), ('beam5', 'ours'), ('greedy', 'beam5')]]
    pairs += [('lim/r1-llava1.5-7b', f'lim/{x}') for x in ['r2-vcd', 'r3-opera', 'r4-opera-fast', 'r5-ours-inst', 'r6-ours-cap']]
    pairs += [('lim/r7-llava1.5-13b', 'lim/r8-ours-cap'), ('lim/r9-llava-7b', 'lim/r10-ours-cap'),
              ('lim/r11-minigptv2', 'lim/r12-ours-cap')]
    rng = np.random.default_rng(0)
    for b, x in pairs:
        common = sorted(set(P[b]) & set(P[x]))
        res['pairs'][f'{x} vs {b}'] = compare(P[b], P[x], common, rng)
    Path(OUT).write_text(json.dumps(res, indent=1))
    for s, a in res['systems'].items():
        print(f"{s:34s} " + ' '.join(f"{k}={v}" for k, v in a.items()))
    for k, v in res['pairs'].items():
        print(f"{k:58s} " + ' '.join(f"{n}={v[n]}" for n in v))


if __name__ == '__main__':
    main()
