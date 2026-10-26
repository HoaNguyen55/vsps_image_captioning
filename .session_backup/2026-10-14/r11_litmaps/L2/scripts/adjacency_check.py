"""R11/L2 CPU check: is the KTVIC 'adjacent-reference paraphrase chain' a general multi-reference artifact?

For each image with exactly 5 ordered references, an object (class or entity chain) named by exactly 2 references
is a doubleton. Under exchangeable references, 4 of the C(5,2)=10 pairs are adjacent, so E[adjacent share] = 0.40,
and lags 1/2/3/4 hold 0.4/0.3/0.2/0.1 of doubletons. Also reports the mean pair Jaccard of object sets by lag.
Outputs aggregates only (no caption text is written; OpenViIC text stays in memory).
Run: nice -n 19 env OMP_NUM_THREADS=1 python3 adjacency_check.py OUT.json
"""
import json
import random
import re
import sys
import zipfile
from collections import defaultdict
from itertools import combinations

ROOT = '/mnt/d/vsps_image_captioning'
sys.path[:0] = [ROOT, ROOT + '/scripts']
from rescap.chair import objects_in  # noqa: E402
import score_coco_probe as sc  # noqa: E402

DS = ROOT + '/data/datasets'
EXPECT = {1: 0.4, 2: 0.3, 3: 0.2, 4: 0.1}


def image_stats(sets):
    """Per image: doubleton counts by lag, and Jaccard sums/counts by lag."""
    dlag = {d: 0 for d in EXPECT}
    jsum = {d: 0.0 for d in EXPECT}
    jn = {d: 0 for d in EXPECT}
    for o in set().union(*sets):
        idx = [r for r in range(5) if o in sets[r]]
        if len(idx) == 2:
            dlag[idx[1] - idx[0]] += 1
    for a, b in combinations(range(5), 2):
        u = sets[a] | sets[b]
        if u:
            jsum[b - a] += len(sets[a] & sets[b]) / len(u)
            jn[b - a] += 1
    return dlag, jsum, jn


def summarize(name, per_image, B=1000, seed=0):
    import numpy as np
    rows = [image_stats(s) for s in per_image]
    n = len(rows)
    lags = sorted(EXPECT)
    DL = np.array([[r[0][d] for d in lags] for r in rows], float)
    JS = np.array([[r[1][d] for d in lags] for r in rows], float)
    JN = np.array([[r[2][d] for d in lags] for r in rows], float)

    def agg(w):  # w: per-image bootstrap counts (or ones)
        dl, js, jn = w @ DL, w @ JS, w @ JN
        jac = js / np.maximum(jn, 1)
        return dl.sum(), dl / dl.sum(), jac

    tot, share, jac = agg(np.ones(n))
    rng = np.random.default_rng(seed)
    W = rng.multinomial(n, np.full(n, 1 / n), size=B).astype(float)
    bs = [agg(w) for w in W]
    bs_adj = np.array([b[1][0] for b in bs])
    bs_j = np.array([b[2][0] - b[2][1:].mean() for b in bs])
    ci = lambda v: [round(float(np.percentile(v, 2.5)), 4), round(float(np.percentile(v, 97.5)), 4)]
    out = {'images': n, 'doubletons_per_img': round(tot / n, 4),
           'adjacent_share': round(float(share[0]), 4), 'adjacent_share_ci95': ci(bs_adj),
           'lag_share': {d: round(float(share[k]), 4) for k, d in enumerate(lags)},
           'jaccard_by_lag': {d: round(float(jac[k]), 4) for k, d in enumerate(lags)},
           'jac_lag1_minus_mean_lag2to4': round(float(jac[0] - jac[1:].mean()), 4),
           'jac_diff_ci95': ci(bs_j)}
    print(name, json.dumps(out), flush=True)
    return out


def coco_style(path, extract, order='id'):
    """{'annotations': [{'id','image_id','caption'}]} -> per-image list of 5 object sets, ordered by caption id."""
    d = json.load(open(path, encoding='utf-8'))
    per = defaultdict(list)
    for i, a in enumerate(d['annotations']):
        if a.get('caption'):
            per[a['image_id']].append((a['id'] if order == 'id' else i, a['caption']))
    return [[extract(c) for _, c in sorted(v)] for v in per.values() if len(v) == 5]


def flickr_entities():
    """Flickr30k Entities: object = coreference chain id (visual types only), caption order = file line order."""
    z = zipfile.ZipFile(DS + '/flickr30k_entities/annotations.zip')
    pat = re.compile(r'\[/EN#(\d+)/([a-z/]+) ')
    out_all, out_noscene = [], []
    for nm in z.namelist():
        if not (nm.startswith('Sentences/') and nm.endswith('.txt')):
            continue
        lines = [ln for ln in z.read(nm).decode('utf-8').splitlines() if ln.strip()]
        if len(lines) != 5:
            continue
        sets_all, sets_ns = [], []
        for ln in lines:
            ents = pat.findall(ln)
            sets_all.append({e for e, t in ents if 'notvisual' not in t})
            sets_ns.append({e for e, t in ents if 'notvisual' not in t and t != 'scene'})
        out_all.append(sets_all)
        out_noscene.append(sets_ns)
    return out_all, out_noscene


def openviic_panel():
    """KTVIC-image OpenViIC panel (independent students): images with exactly 5 captions, list order. Text in memory."""
    d = json.load(open(ROOT + '/data/ktvic_openviic_refs.json', encoding='utf-8'))['test']
    exact5 = [[set(objects_in(c)) for c in caps] for caps in d.values() if len(caps) == 5]
    first5 = [[set(objects_in(c)) for c in caps[:5]] for caps in d.values() if len(caps) >= 5]
    return exact5, first5


def _check():
    # one adjacent doubleton ('a' in refs 0,1), one lag-2 doubleton ('b' in refs 1,3)
    dl, js, jn = image_stats([{'a'}, {'a', 'b'}, set(), {'b'}, set()])
    assert dl == {1: 1, 2: 1, 3: 0, 4: 0}, dl
    # lag-1 unions all non-empty, only (0,1) overlaps (J=1/2); lag 2: (2,4) has an empty union, (1,3) gives J=1/2
    assert jn == {1: 4, 2: 2, 3: 2, 4: 1} and abs(js[1] - 0.5) < 1e-9 and abs(js[2] - 0.5) < 1e-9, (js, jn)


def main():
    _check()
    syn = sc.load_synonyms()
    en = lambda c: sc.en_classes(c, syn)
    vi = lambda c: set(objects_in(c))
    sets = {  # key -> zero-arg loader of per-image ordered object sets (lazy: argv[2:] picks keys, default all)
        'ktvic_test_objects_in': lambda: coco_style(DS + '/ktvic/test_data.json', vi),
        'ktvic_train_objects_in': lambda: coco_style(DS + '/ktvic/train_data.json', vi),
        'uitviic_vi_all_objects_in': lambda: sum((coco_style(f'{DS}/uitviic/{sp}_data.json', vi)
                                                  for sp in ('train', 'val', 'test')), []),
        'uitviic_images_coco_en_refs_coco80': lambda: sum((coco_style(f'{DS}/uitviic_en/{sp}_data.json', en)
                                                           for sp in ('train', 'val', 'test')), []),
        'coco_en_test_coco80': lambda: coco_style(DS + '/coco_en/test_data.json', en),
        'flickr30k_entities_chains_visual': lambda: flickr_entities()[0],
        'flickr30k_entities_chains_noscene': lambda: flickr_entities()[1],
        'openviic_panel_exact5_objects_in': lambda: openviic_panel()[0],
        'openviic_panel_first5_objects_in': lambda: openviic_panel()[1],
    }
    want = sys.argv[2:] or list(sets)
    res = {k: summarize(k, sets[k]()) for k in want}
    json.dump(res, open(sys.argv[1], 'w'), indent=1)


if __name__ == '__main__':
    main()
