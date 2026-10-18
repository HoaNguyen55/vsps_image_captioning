#!/usr/bin/env python
"""Count-matched preference pairs (R10/M3 draft for scripts/cm_pairs.py; CPU only, reads no model).

    python scripts/cm_pairs.py --samples S.jsonl --dataset ktvic --mode cm --out DIR            # treatment
    python scripts/cm_pairs.py --samples S.jsonl --dataset ktvic --mode unmatched --like DIR --out DIR_C1
    python scripts/cm_pairs.py --samples S.jsonl --dataset ktvic --mode vote --like DIR --out DIR_C2
    NCS_DATASET=uitviic python scripts/cm_pairs.py --samples U.jsonl --dataset uitviic --keep KEEP.json --mode cm --out DIR_U
    python scripts/cm_pairs.py --self-check

Candidates are the policy's own samples (e5_sample.py rows): MODEL-GENERATED, flagged in every row. Labels are human:
KTVIC = union of the image's reference classes (rescap.chair.objects_in, matcher v2); UIT-ViIC = COCO-2014 instance
classes (data/uitviic/instance_gold.json). A pair (w, l) of one image is kept when
  count:  |M(w)| = |M(l)| = k >= 1 (lexicon classes; on UIT-ViIC also equal COCO-80 counts, matcher v2),
  length: |syllables(w) - syllables(l)| <= 2,
  label:  TP(w) >= TP(l) + 1 against the image's gold,
after dropping candidates that are empty, contain CJK, end on a function word, or copy a reference (m >= 0.90,
rl_reward.copy_stat on syllables). At most CAP pairs per image, largest dTP first, then seeded random.
Controls reuse the treatment's images and per-image pair counts (--like): unmatched = best-vs-next by per-caption F1
with DIFFERENT counts (E5-style); vote = the count/length rule with the winner by higher leave-one-out vote share
(no label). Writes DIR/dpo.jsonl in train_stage2.py's format plus `ref` (first human caption: the SFT anchor).
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(os.environ.get("VSPS_ROOT", Path(__file__).resolve().parents[1]))
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

PROMPT_SHORT = ("Mô tả bức ảnh này bằng MỘT câu tiếng Việt ngắn gọn, "
                "giống chú thích ảnh. Không liệt kê, không giải thích.")
CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯]")
CAP, MAX_DSYL, COPY_TAU = 4, 2, 0.90


def syl(t: str) -> list[str]:
    return re.sub(r"[.,;:!?]", " ", t.lower()).split()


def usable(c: str, refs: list[str]) -> bool:
    from rl_reward import FUNCTION_END, copy_stat
    s = syl(c)
    return bool(s) and not CJK.search(c) and s[-1] not in FUNCTION_END and copy_stat(s, [syl(r) for r in refs])[0] < COPY_TAU


def pairs_for(cands, key, tp, rng, mode, n_like=None, vote=None):
    """cands: distinct usable captions; key(c) -> count signature; tp(c) -> true positives (None for vote mode)."""
    out = []
    for i in range(len(cands)):
        for j in range(i + 1, len(cands)):
            a, b = cands[i], cands[j]
            if abs(len(syl(a)) - len(syl(b))) > MAX_DSYL:
                continue
            same = key(a) == key(b)
            if mode == "cm" and same and key(a)[0] >= 1 and tp(a) != tp(b):
                w, l = (a, b) if tp(a) > tp(b) else (b, a)
                out.append((tp(w) - tp(l), rng.random(), w, l, f"cm_k{key(a)[0]}"))
            elif mode == "vote" and same and key(a)[0] >= 1 and vote(a) != vote(b):
                w, l = (a, b) if vote(a) > vote(b) else (b, a)
                out.append((abs(vote(a) - vote(b)), rng.random(), w, l, f"vote_k{key(a)[0]}"))
            elif mode == "unmatched" and not same and tp(a) != tp(b):
                fa, fb = tp(a), tp(b)  # here tp() returns per-caption F1
                w, l = (a, b) if fa > fb else (b, a)
                out.append((abs(fa - fb), rng.random(), w, l, f"unm_dk{key(w)[0] - key(l)[0]:+d}"))
    out.sort(key=lambda t: (-t[0], t[1]))
    return out[: (CAP if n_like is None else n_like)]


def build(samples, refs, names, gold, sig, mode, like=None, seed=42):
    rng, rows, rep = random.Random(seed), [], Counter()
    for iid in sorted(samples):
        if like is not None and iid not in like:
            continue
        cands = [c for c in dict.fromkeys(samples[iid]) if usable(c, refs[iid])]
        rep["dropped_candidates"] += len(set(samples[iid])) - len(cands)
        g = gold[iid]
        if mode == "unmatched":
            def tp(c, g=g):
                m = sig(c)[1]
                return 2 * len(m & g) / (len(m) + len(g)) if m & g else 0.0
        else:
            def tp(c, g=g):
                return len(sig(c)[1] & g)
        votes = Counter(o for c in cands for o in sig(c)[1])
        n = max(len(cands) - 1, 1)

        def vote(c):
            m = sig(c)[1]
            return sum((votes[o] - 1) / n for o in m) / len(m) if m else 0.0
        key = lambda c: (len(sig(c)[1]), len(sig(c)[2]))  # noqa: E731  (count, second-ontology count)
        for _, _, w, l, kind in pairs_for(cands, key, tp, rng, mode, like.get(iid) if like else None, vote):
            rows.append({"image_id": iid, "file_name": names[iid], "prompt": PROMPT_SHORT, "chosen": w,
                         "rejected": l, "ref": refs[iid][0], "pair_type": kind,
                         "candidate_source": "model_sample (MODEL-GENERATED)", "label_source": "human"})
            rep[kind] += 1
    rep["pairs"] = len(rows); rep["images"] = len({r["image_id"] for r in rows})
    return rows, rep


def self_check():
    import rescap.chair as ch
    sig = lambda c: (None, frozenset(ch.objects_in(c)), frozenset())  # noqa: E731
    refs = {"1": ["phụ nữ đứng cạnh xe máy"] * 5}  # under 8 syllables: clears the OpenViIC 8-gram scan
    s = {"1": ["phụ nữ ngồi xe máy",             # k=2, TP 2
               "phụ nữ ngồi ô tô",               # k=2, TP 1
               "phụ nữ ngồi xe máy trên đường",  # k=3 (đường): other count
               "một chiếc xe máy"]}              # k=1
    gold = {"1": frozenset(ch.objects_in(refs["1"][0]))}
    rows, rep = build(s, refs, {"1": "x.jpg"}, gold, lambda c: (len(sig(c)[1]),) + sig(c)[1:], "cm")
    assert rep["pairs"] == 1 and rows[0]["chosen"].endswith("xe máy") and rows[0]["rejected"].endswith("ô tô"), rows
    print("self-check ok")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-check", action="store_true")
    ap.add_argument("--samples"); ap.add_argument("--out")
    ap.add_argument("--dataset", choices=("ktvic", "uitviic"), default="ktvic")
    ap.add_argument("--split", default="train_data.json")
    ap.add_argument("--mode", choices=("cm", "unmatched", "vote"), default="cm")
    ap.add_argument("--like", help="treatment DIR: reuse its images and per-image pair counts (controls)")
    ap.add_argument("--keep", help="JSON list of image ids allowed (UIT-ViIC: train minus the 133 Karpathy-test)")
    ap.add_argument("--exclude", default=str(ROOT / "data/splits/ktvic_dev300.txt"))
    a = ap.parse_args()
    if a.self_check:
        return self_check()
    from evaluate import file_names, references
    from rescap.chair import objects_in
    refs, names = references(a.split), file_names(a.split)
    samples = {str(r["image_id"]): r["samples"] for r in map(json.loads, open(a.samples, encoding="utf-8"))}
    drop = set(Path(a.exclude).read_text().split()) if a.dataset == "ktvic" else set()
    keep = set(map(str, json.loads(Path(a.keep).read_text()))) if a.keep else None
    samples = {i: v for i, v in samples.items() if i not in drop and (keep is None or i in keep)}
    lex = lambda c: frozenset(objects_in(c))  # noqa: E731
    if a.dataset == "ktvic":
        gold = {i: frozenset().union(*map(lex, refs[i])) for i in samples}
        sig = lambda c: (len(lex(c)), lex(c), frozenset())  # noqa: E731
    else:
        from score_coco_probe import load_vi_terms, vi_objects
        terms, inst = load_vi_terms(), json.loads((ROOT / "data/uitviic/instance_gold.json").read_text())
        gold = {i: frozenset(inst[i]["coco"]) for i in samples}
        sig = lambda c: (len(vi_objects(c, terms)), frozenset(vi_objects(c, terms)), lex(c))  # noqa: E731
    like = None
    if a.like:
        like = Counter(json.loads(x)["image_id"] for x in open(Path(a.like) / "dpo.jsonl", encoding="utf-8"))
    rows, rep = build(samples, refs, names, gold, sig, a.mode, like)
    Path(a.out).mkdir(parents=True, exist_ok=True)
    with open(Path(a.out) / "dpo.jsonl", "w", encoding="utf-8") as fh:
        fh.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    (Path(a.out) / "_build_report.json").write_text(json.dumps(dict(rep, mode=a.mode, dataset=a.dataset), indent=1))
    print(json.dumps(rep))


if __name__ == "__main__":
    sys.exit(main())
