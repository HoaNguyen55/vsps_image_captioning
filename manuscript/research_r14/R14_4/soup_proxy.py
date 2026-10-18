"""R14-4 CPU proxy: what does seed consensus (MBR over K greedy captions) buy for the response-masked P1 seeds?

Syllable-level CIDEr-D (stdlib port of pycocoevalcap CIDEr-D: n=1..4, sigma 6, clipping, x10), so absolute values
differ from the paper's word-level RDRSegmenter numbers; only paired deltas are read. Bootstrap over images.
"""
import json, math, random, re, sys
from collections import Counter, defaultdict

R = "/mnt/d/vsps_image_captioning/data/results/"
refs_raw = json.load(open("/mnt/d/vsps_image_captioning/data/datasets/ktvic/test_data.json"))


def toks(c):
    return re.sub(r"[^\w\s]", " ", c.lower()).split()


def ngr(t):
    return Counter(tuple(t[i:i + n]) for n in range(1, 5) for i in range(len(t) - n + 1))


refs = defaultdict(list)
for a in refs_raw["annotations"]:
    refs[str(a["image_id"])].append(toks(a["caption"]))
ids = sorted(refs)
df = Counter(g for i in ids for g in {g for r in refs[i] for g in ngr(r)})
logN = math.log(len(ids))


def vec(t):
    c = ngr(t)
    v = [{}, {}, {}, {}]
    norm = [0.0] * 4
    for g, tf in c.items():
        n = len(g) - 1
        x = tf * (logN - math.log(max(1.0, df[g])))
        v[n][g] = x
        norm[n] += x * x
    return v, [math.sqrt(x) for x in norm], len(t)


def sim(a, b):
    (va, na, la), (vb, nb, lb) = a, b
    s = 0.0
    for n in range(4):
        dot = sum(min(x, vb[n].get(g, 0.0)) * vb[n].get(g, 0.0) for g, x in va[n].items())
        if na[n] and nb[n]:
            s += dot / (na[n] * nb[n]) * math.exp(-((la - lb) ** 2) / 72.0)
    return s / 4


ref_vecs = {i: [vec(r) for r in refs[i]] for i in ids}


def cider(i, cap):
    v = vec(toks(cap))
    return 10 * sum(sim(v, r) for r in ref_vecs[i]) / len(ref_vecs[i])


def preds(name):
    return {str(k): v for k, v in json.load(open(R + name))["predictions"].items()}


sets = {
    "assist": ["p1assist_s42-short.json", "p1assist_s43-short.json", "p1assist_s44-short.json"],
    "legacy": ["p1-gold-short.json", "p1_s43-short.json", "p1_s44-short.json"],
}
for label, files in sets.items():
    P = [preds(f) for f in files]
    per = {i: [cider(i, p[i]) for p in P] for i in ids}
    mean_seed = {i: sum(per[i]) / len(P) for i in ids}
    mbr = {}
    for i in ids:  # medoid: the caption with the highest mean CIDEr-D-style similarity to the other seeds' captions
        vs = [vec(toks(p[i])) for p in P]
        score = [sum(sim(vs[a], vs[b]) for b in range(len(P)) if b != a) for a in range(len(P))]
        mbr[i] = per[i][score.index(max(score))]
    seeds = [100 * sum(per[i][k] for i in ids) / len(ids) for k in range(len(P))]
    d = [mbr[i] - mean_seed[i] for i in ids]
    rng = random.Random(0)
    bs = sorted(100 * sum(d[rng.randrange(len(d))] for _ in d) / len(d) for _ in range(2000))
    agree = sum(len({p[i] for p in P}) == 1 for i in ids) / len(ids)
    print(label, "seed CIDEr(syl)", [round(s, 2) for s in seeds], "MBR-minus-seed-mean",
          round(100 * sum(d) / len(d), 2), "CI", (round(bs[50], 2), round(bs[1949], 2)), "all-agree", round(agree, 3))
