"""R14-4 CPU proxy: does more caption data of the same corpus still add test-reference n-grams?

Syllable n-grams (n=1..4), lowercased, punctuation stripped. For each train subset size, the share of test-reference
n-gram tokens (IDF-weighted over test images, as in CIDEr) whose n-gram occurs anywhere in the subset's captions.
"""
import json, math, random, re, sys
from collections import Counter, defaultdict

D = "/mnt/d/vsps_image_captioning/data/datasets/"


def load(path):
    d = json.load(open(D + path))
    caps = defaultdict(list)
    for a in d["annotations"]:
        caps[a["image_id"]].append(a["caption"])
    return caps


def grams(c):
    w = re.sub(r"[^\w\s]", " ", c.lower()).split()
    return [tuple(w[i:i + n]) for n in range(1, 5) for i in range(len(w) - n + 1)]


def test_weights(test):
    df = Counter(g for caps in test.values() for g in {g for c in caps for g in grams(c)})
    N = len(test)
    tok = Counter()
    for caps in test.values():
        for c in caps:
            for g in grams(c):
                tok[g] += math.log(N / df[g])
    return tok


def coverage(train_imgs, train, w):
    seen = {g for i in train_imgs for c in train[i] for g in grams(c)}
    tot = sum(w.values())
    by_n = defaultdict(lambda: [0.0, 0.0])
    for g, v in w.items():
        by_n[len(g)][1] += v
        if g in seen:
            by_n[len(g)][0] += v
    return sum(v for g, v in w.items() if g in seen) / tot, {n: a / b for n, (a, b) in sorted(by_n.items())}


kt_tr, kt_te = load("ktvic/train_data.json"), load("ktvic/test_data.json")
ui_tr, ui_te = load("uitviic/train_data.json"), load("uitviic/test_data.json")
w_kt, w_ui = test_weights(kt_te), test_weights(ui_te)
out = {}
for name, tr, w in [("ktvic", kt_tr, w_kt), ("uitviic", ui_tr, w_ui)]:
    ids = sorted(tr)
    rows = []
    for frac in (0.125, 0.25, 0.5, 1.0):
        vals = []
        for s in range(5 if frac < 1 else 1):
            sub = random.Random(s).sample(ids, int(len(ids) * frac))
            vals.append(coverage(sub, tr, w))
        cov = sum(v[0] for v in vals) / len(vals)
        n4 = sum(v[1][4] for v in vals) / len(vals)
        rows.append((int(len(ids) * frac), round(cov, 4), round(n4, 4)))
    out[name] = rows
    print(name, "n_img, idf-weighted 1-4gram coverage, 4gram coverage:", rows)
# cross-corpus: does the other corpus add test n-grams on top of in-domain train?
both = {**{("k", i): c for i, c in kt_tr.items()}, **{("u", i): c for i, c in ui_tr.items()}}
for name, w, own in [("ktvic_test", w_kt, "k"), ("uitviic_test", w_ui, "u")]:
    own_ids = [k for k in both if k[0] == own]
    oth_ids = [k for k in both if k[0] != own]
    print(name, "own", [round(x, 4) for x in [coverage(own_ids, both, w)[0]]],
          "other-only", round(coverage(oth_ids, both, w)[0], 4),
          "own+other", round(coverage(own_ids + oth_ids, both, w)[0], 4))
# style: share of captions starting with each first syllable
for name, tr in [("ktvic", kt_tr), ("uitviic", ui_tr)]:
    first = Counter(re.sub(r"[^\w\s]", " ", c.lower()).split()[0] for cs in tr.values() for c in cs if re.sub(r"[^\w\s]", " ", c).split())
    L = [len(c.split()) for cs in tr.values() for c in cs]
    print(name, "top first words", first.most_common(4), "mean syllables", round(sum(L) / len(L), 2))
# P1 sees one caption per image (first in file order); multiref sees all five.
kt_slot0 = {i: c[:1] for i, c in kt_tr.items()}
print("ktvic slot0-only full-set coverage", round(coverage(sorted(kt_slot0), kt_slot0, w_kt)[0], 4),
      "vs all-5", round(coverage(sorted(kt_tr), kt_tr, w_kt)[0], 4))
