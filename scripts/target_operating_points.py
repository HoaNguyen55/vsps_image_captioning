#!/usr/bin/env python
"""Predicted operating points of SFT target policies from the TRAINING captions alone (KTVIC).

    cd /mnt/d/vsps_image_captioning
    NCS_DATA=data python3 <this> --out op_train.json            # target statistics + both models' predictions
    NCS_DATA=data python3 <this> --out op_train.json --check     # + score any ladder preds already in data/results

For each policy of build_gold_sft.py (rows rebuilt exactly as the ladder jobs train on them, all 5 captions,
--seed 42 for rnd2), per prompt mode:
  rows/image, objects/row, sentences/row          -> the LENGTH model: an MLE captioner reproduces its target's
                                                      object count; test count = rows' count x a calibration ratio
  inclusion function g(c) = P(o in row | c of 5 captions name o), averaged over the image's rows (the MLE mixture)
  implicit threshold tau: sum_c g(c) Bin(c; 5, tau) = 1/2 (A1's THRESHOLD model: greedy decoding keeps o iff the
  learned mention marginal exceeds 1/2, i.e. iff pi_o > tau)
  ideal-learner count E#{o: pi_o > tau} per image under per-class zero-truncated beta-binomial posteriors of pi
  (named objects; plus the extrapolated unnamed ones, which Link 2003 says are not identifiable: reported apart).
"""
from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from math import comb
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize
from scipy.special import betainc, betaln

#: the repo: this file's parent when it lives in scripts/, else the local checkout
ROOT = next(p for p in (Path(__file__).resolve().parents[1], Path("/mnt/d/vsps_image_captioning"))
            if (p / "scripts" / "build_gold_sft.py").exists())
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from build_gold_sft import consensual, fused, fusion_set  # noqa: E402
from evaluate import references  # noqa: E402
from rescap.chair import objects_in  # noqa: E402

K = 5


def policies(cs: list[str], rng: random.Random) -> dict[str, list[str]]:
    """{policy-mode: training rows of this image}, as build_gold_sft.py writes them (rnd2 draws from rng)."""
    cons = consensual(cs)
    pair = fusion_set(cs, 2)
    return {
        "p1-short": [cs[0]],                       # also p1ep4 (same rows, 4 epochs)
        "cons-short": [cons],                      # also the short row of fuse2 and rnd2
        "unf2-short": pair,                        # consensus + greedy partner, separate short rows
        "multiref-short": list(cs),
        "fuse2-detailed": [fused(cs, 2)],
        "rnd2-detailed": [fused(cs, 2, rng)],
    }


def n_sent(t: str) -> int:
    t = t.strip()
    return sum(t.count(p) for p in ".!?") + (0 if t[-1:] in ".!?" else 1)


def fit_betabin(ks_by: dict[str, list[int]]) -> dict[str, tuple[float, float]]:
    """Per-class zero-truncated beta-binomial (a, b), shrunk toward the pooled fit (A1's fit_bb, w = 2)."""
    def nll(t, ks, prior=None):
        a, b = np.exp(t)
        ks = np.asarray(ks, float)
        ll = betaln(ks + a, K - ks + b) - betaln(a, b) + np.log([comb(K, int(k)) for k in ks])
        p0 = np.exp(betaln(a, K + b) - betaln(a, b))
        pen = 0.0 if prior is None else 2.0 * float(((t - prior) ** 2).sum())
        return -(ll.sum() - len(ks) * np.log1p(-min(p0, 1 - 1e-12))) + pen

    allk = [k for v in ks_by.values() for k in v]
    g = minimize(nll, np.zeros(2), args=(allk,), method="Nelder-Mead").x
    return {o: tuple(np.exp(minimize(nll, g, args=(ks, g), method="Nelder-Mead").x)) for o, ks in ks_by.items()} | {
        "__global__": tuple(np.exp(g))}


def implicit_tau(g: dict[int, float]) -> float:
    mu = lambda p: sum(g.get(c, 0.0) * comb(K, c) * p ** c * (1 - p) ** (K - c) for c in range(1, K + 1))  # noqa
    return brentq(lambda p: mu(p) - 0.5, 1e-6, 1 - 1e-6) if mu(1 - 1e-6) > 0.5 else float("nan")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="train_data.json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    refs = {i: [c.strip() for c in cs] for i, cs in references(args.split).items()}
    assert all(len(cs) == K for cs in refs.values()), "5 captions per image assumed"
    rng = random.Random(42)                         # build_gold_sft --seed 42 --fuse-order random, sorted ids
    stats = defaultdict(lambda: {"rows": 0, "objs": 0, "sent": 0, "imgs": 0})
    hit = defaultdict(lambda: Counter())            # policy -> c -> summed inclusion
    tot = Counter()                                 # c -> (image, object) pairs
    ks_by, named = defaultdict(list), []
    for i in sorted(refs):
        cs = refs[i]
        cnt = Counter(o for c in cs for o in set(objects_in(c)))
        named.append(cnt)
        for o, k in cnt.items():
            ks_by[o].append(k); tot[k] += 1
        for pol, rows in policies(cs, rng).items():
            s = stats[pol]
            s["imgs"] += 1; s["rows"] += len(rows)
            objs = [set(objects_in(r)) for r in rows]
            s["objs"] += sum(map(len, objs)); s["sent"] += sum(map(n_sent, rows))
            for o, k in cnt.items():
                hit[pol][k] += sum(o in x for x in objs) / len(rows)
    ab = fit_betabin(ks_by)
    n_img = len(refs)

    def ideal_count(tau: float) -> tuple[float, float]:
        """E #{o: pi_o > tau} per image: named objects, and the extrapolated unnamed ones."""
        seen = sum(1 - betainc(ab[o][0] + k, ab[o][1] + K - k, tau) for cnt in named for o, k in cnt.items())
        unseen = 0.0
        for o, ks in ks_by.items():
            a, b = ab[o]
            p0 = float(np.exp(betaln(a, b + K) - betaln(a, b)))
            unseen += len(ks) * p0 / (1 - p0) * (1 - betainc(a, b + K, tau))
        return seen / n_img, unseen / n_img

    out = {"split": args.split, "n_images": n_img, "pairs_by_count": dict(sorted(tot.items())),
           "union5_per_image": sum(tot.values()) / n_img, "policies": {}}
    for pol, s in stats.items():
        g = {k: hit[pol][k] / tot[k] for k in sorted(tot)}
        tau = implicit_tau(g)
        seen, unseen = ideal_count(tau)
        out["policies"][pol] = {
            "rows_per_image": s["rows"] / s["imgs"], "objects_per_row": s["objs"] / s["rows"],
            "sentences_per_row": s["sent"] / s["rows"], "g": g, "tau": tau,
            "ideal_count_named": seen, "ideal_count_unnamed_extrap": unseen}
        print(f"{pol:16s} rows/img={s['rows']/s['imgs']:.2f} obj/row={s['objs']/s['rows']:.3f} "
              f"sent/row={s['sent']/s['rows']:.2f} tau={tau:.3f} ideal#={seen:.3f} (+{unseen:.3f} unnamed)  g="
              + " ".join(f"{k}:{v:.2f}" for k, v in g.items()))
    for t in (0.5, 1 - 2 ** -0.5, 1 - 2 ** (-1 / 3), 1 - 2 ** -0.2):
        seen, unseen = ideal_count(t)
        print(f"  ideal count at tau={t:.3f}: {seen:.3f} named (+{unseen:.3f} unnamed)")
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("->", args.out)
    return 0


def _check() -> None:
    # separable policies: g(c) = c/5 gives tau = 1/2; union of k captions gives 1 - 2^(-1/k)
    assert abs(implicit_tau({c: c / K for c in range(1, 6)}) - 0.5) < 1e-6
    for k in (2, 3):
        g = {c: 1 - comb(K - c, k) / comb(K, k) for c in range(1, 6)}
        assert abs(implicit_tau(g) - (1 - 2 ** (-1 / k))) < 1e-6
    assert n_sent("a. b.") == 2 and n_sent("a") == 1 and n_sent("a. b") == 2


if __name__ == "__main__":
    _check()
    sys.exit(main())
