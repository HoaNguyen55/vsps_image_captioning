#!/usr/bin/env python
"""Policy-diverse committee, true-precision headroom and typicality inflation on KTVIC test (V5; R5-03).

    NCS_DATA=data python scripts/committee_headroom.py          # -> data/results/committee_headroom.json
    # pre-registered rule, to re-run when the target-policy ladder lands (members = every stem given):
    NCS_DATA=data python scripts/committee_headroom.py --members p1-gold p1_s43 p1_s44 fuse2_s42 fuse2_s43 \\
        fuse2_s44 cons_s42 unf2_s42 rnd2_s42 multiref_s42 p1ep4_s42

Committees (A3's rules, frozen by V5): the members' captions under both prompts (n = 2 x members);
  short     object-F1 MBR: the short-prompt member caption with the highest mean object F1 against the other
            pool captions of the image;
  detailed  extractive cover: member sentences whose objects all have >= k votes, k = round(0.3 n), greedy
            cover of the agreed objects, <= 2 sentences (fallback: the member caption with the fewest unagreed
            objects). SEED8 = P1 s42/s43/s44 + fuse2 s42 (k = 2); FT10 = A3's pool with E5/E5-DPO (k = 3).
Golds, on the 555 test images with a UIT-OpenViIC panel: the 5 KTVIC references; their union with the panel.
mix: excess over the per-image P1-s42 <-> fuse2 mixture with the committee's total object count (A3's chord
     test: a Pareto gain, not a move along the trade-off); NaN draws (count outside the chord) are dropped.
Corrected precision (1v4: each system vs the other 4 KTVIC captions, 5 folds): its reference-false mentions
     that the OpenViIC panel names are 'confirmed'; the panel sensitivity s is the confirmed share of a held-out
     KTVIC caption's reference-false mentions, per class (shrunk to the global rate, prior weight 10) and
     averaged over the system's own class mix; hallucinated = max(rf - confirmed / s, 0); corrected P =
     1 - hallucinated / mentions. 'global' uses the pooled human rate. Assumes the panel detects a system's real
     extras as often as a human's in the same class.
Typicality inflation: a precision method's dP against the KTVIC references, the union gold, and corrected.
VTF (A8 vote-then-fuse, k = 3, <= 1 sentence) uses job 35's six T=0.8 short samples of fuse2_s42
(data/results/samples/fuse2_s42-test-short.jsonl, copied from n2:/root/ncs-data/samples).
"""
from __future__ import annotations

import argparse
import json
import re
import statistics as st
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from build_gold_sft import consensual  # noqa: E402
from object_prf import image_counts  # noqa: E402
from rescap.chair import _ancestors, objects_in  # noqa: E402
from second_panel import prf_arrays  # noqa: E402
from two_gold_audit import summ, weights  # noqa: E402

RESULTS = ROOT / "data" / "results"
SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
SEED8 = ("p1-gold", "p1_s43", "p1_s44", "fuse2_s42")
FT10 = ("p1-gold", "p1_s43", "fuse2_s42", "e5_s42", "e5dpo_s42")
MODES = ("short", "detailed")


def uniq(text: str) -> list[str]:
    return list(dict.fromkeys(objects_in(text)))


def sentences(text: str) -> list[str]:
    return [x.strip() for x in SPLIT.split(text.strip()) if x.strip()]


def close(c: str) -> str:
    return c if c.rstrip().endswith((".", "!", "?")) else c.rstrip() + "."


def fbeta(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    tp = len(a & b)
    return 2 * tp / (len(a) + len(b)) if tp else 0.0


def mbr(caps: list[str], cands: list[int]) -> str:
    """The candidate caption with the highest mean object F1 against the other captions of the pool."""
    o = [set(uniq(c)) for c in caps]
    return caps[max(cands, key=lambda c: (st.mean(fbeta(o[c], o[r]) for r in range(len(caps)) if r != c), -cands.index(c)))]


def cover(caps: list[str], k: int, max_sents: int = 2) -> str:
    """Member sentences whose objects all have >= k votes; greedy cover of the agreed objects (A3)."""
    votes = Counter(x for c in caps for x in uniq(c))
    agreed = {x for x, v in votes.items() if v >= k}
    sents = list(dict.fromkeys(s for c in caps for s in sentences(c)))
    so = {s: set(uniq(s)) for s in sents}
    ok, chosen, have = [s for s in sents if so[s] and so[s] <= agreed], [], set()
    while ok and len(chosen) < max_sents:
        best = max(ok, key=lambda s: (len(so[s] - have), sum(votes[x] for x in so[s] - have), -len(s.split())))
        if not so[best] - have:
            break
        chosen.append(best)
        have |= so[best]
        ok.remove(best)
    if not chosen:
        chosen = [min(caps, key=lambda c: (len(set(uniq(c)) - agreed), -len(set(uniq(c)) & agreed)))]
    return " ".join(map(close, chosen))


def vote_fuse(samples: list[str], k: int, max_sent: int = 1) -> str:
    """A8's VTF: sentences of the samples whose objects all have >= k sample votes, greedy cover; else the MBR pick."""
    objs = [set(objects_in(s)) for s in samples]
    voted = {o for o in set().union(*objs) if sum(o in s for s in objs) >= k}
    sents = [t.strip() for s in samples for t in re.split(r"(?<=[.!?])\s+", s) if t.strip()]
    count = Counter(sents)
    cand = [(t, set(objects_in(t))) for t in count if set(objects_in(t)) <= voted]
    chosen, covered = [], set()
    while len(chosen) < max_sent:
        best = max(cand, key=lambda x: (len(x[1] & voted - covered), count[x[0]], -len(x[0])), default=None)
        if best is None or not (best[1] & voted - covered) and chosen:
            break
        chosen.append(best[0])
        covered |= best[1]
        cand.remove(best)
    return " ".join(map(close, chosen)) if chosen else consensual(samples)


def mix_excess(rc, ra, rb, w) -> tuple[np.ndarray, np.ndarray]:
    """(dP, dR) of C over the mixture of A and B with C's total object count, per weight row (NaN off the chord)."""
    def tot(rows):
        x = np.asarray(rows, float)
        return w @ x[:, 0], w @ x[:, 1], 100 * (w @ np.nan_to_num(x[:, 3])) / (w @ ~np.isnan(x[:, 3]))
    (ta, ma, r_a), (tb, mb, r_b), (tc, mc, r_c) = tot(ra), tot(rb), tot(rc)
    with np.errstate(invalid="ignore", divide="ignore"):
        lam = (mc - ma) / (mb - ma)
        ok = (lam >= 0) & (lam <= 1)
        dp = np.where(ok, 100 * (tc - ((1 - lam) * ta + lam * tb)) / mc, np.nan)
        dr = np.where(ok, r_c - ((1 - lam) * r_a + lam * r_b), np.nan)
    return dp, dr


def extras(sets_by_fold: list[list[frozenset]], rest, go, classes: list[str]) -> tuple[np.ndarray, np.ndarray]:
    """(N, C)[image, class]: reference-false mentions vs the other 4 captions and those the panel names, over 5 folds."""
    col = {c: j for j, c in enumerate(classes)}
    n, c = np.zeros((len(rest), len(classes))), np.zeros((len(rest), len(classes)))
    for t, folds in enumerate(sets_by_fold):
        for f, m in enumerate(folds):
            for o in m - rest[t][f]:
                n[t, col[o]] += 1
                c[t, col[o]] += o in go[t]
    return n, c


def corrected(sys_nc, human_nc, mentions: np.ndarray, w: np.ndarray) -> dict[str, np.ndarray]:
    """Panel-sensitivity-corrected precision per weight row, class-adjusted and global."""
    (ns, cs), (nh, ch) = sys_nc, human_nc
    wnh, wch, wns = w @ nh, w @ ch, w @ ns
    g = wch.sum(1) / wnh.sum(1)
    rate = (wch + 10 * g[:, None]) / (wnh + 10)
    rf, cf, m = wns.sum(1), (w @ cs).sum(1), w @ mentions
    s = (wns * rate).sum(1) / np.maximum(rf, 1e-9)
    return {"P_corrected": 100 * (1 - np.maximum(rf - cf / s, 0) / m), "P_corrected_global": 100 * (1 - np.maximum(rf - cf / g, 0) / m),
            "sensitivity_class": 100 * s, "sensitivity_global": 100 * g, "confirmed": 100 * cf / np.maximum(rf, 1e-9)}


def main() -> int:
    from evaluate import references
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--members", nargs="+", default=None, help="one committee of these stems (else SEED8 and FT10)")
    ap.add_argument("--samples", default=str(RESULTS / "samples" / "fuse2_s42-test-short.jsonl"))
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--out", default=str(RESULTS / "committee_headroom.json"))
    a = ap.parse_args()
    refs = references("test_data.json")
    panel = json.loads((ROOT / "data" / "ktvic_openviic_refs.json").read_text(encoding="utf-8"))["test"]
    ids = sorted(refs.keys() & panel.keys(), key=lambda x: (len(x), x))
    load = lambda s: {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in json.loads(  # noqa: E731
        (RESULTS / f"{s}.preds.json").read_text(encoding="utf-8")).items()}
    caps = {f"{s}-{m}": load(f"{s}-{m}") for s in dict.fromkeys((*SEED8, *FT10, "tags_fuse2_s42", "zeroshot", *(a.members or ()))) for m in MODES}
    pools = {f"C{len(a.members) * 2}": a.members} if a.members else {"SEED8": SEED8, "FT10": FT10}
    for name, mem in pools.items():
        pool = [f"{s}-{m}" for s in mem for m in MODES]
        short = [j for j, p in enumerate(pool) if p.endswith("short")]
        caps[f"{name}-MBR-short"] = {i: mbr([caps[p][i] for p in pool], short) for i in ids}
        for k in sorted({round(0.3 * len(pool)), 3}):
            caps[f"{name}-cover-k{k}-detailed"] = {i: cover([caps[p][i] for p in pool], k) for i in ids}
    if Path(a.samples).exists():
        smp = {r["image_id"]: [s for s in r["samples"] if s.strip()] or [""]
               for r in map(json.loads, Path(a.samples).read_text(encoding="utf-8").splitlines())}
        caps["fuse2-VTF-k3-short"] = {i: vote_fuse(smp[i], 3) for i in ids}
    obj = {s: [frozenset(objects_in(c[i])) for i in ids] for s, c in caps.items()}
    gk = [frozenset().union(*map(frozenset, map(objects_in, refs[i]))) for i in ids]
    go = [frozenset().union(*map(frozenset, map(objects_in, panel[i]))) for i in ids]
    golds = {"ktvic5": gk, "union": [x | y for x, y in zip(gk, go)]}
    w = weights(len(ids), a.B)
    idx = np.array([np.repeat(np.arange(len(ids)), c.astype(int)) for c in w])  # the same draws as index rows
    rows = {g: {s: [image_counts(set(m), set(t), _ancestors) for m, t in zip(ms, gold)] for s, ms in obj.items()}
            for g, gold in golds.items()}
    prf = {g: {s: prf_arrays(r, idx) for s, r in rs.items()} for g, rs in rows.items()}
    # 1v4: each KTVIC caption vs the other 4, systems vs the same 4; + the panel; extras for the corrected precision
    kc = [[frozenset(objects_in(c)) for c in refs[i][:5]] for i in ids]
    rest = [[frozenset().union(*(cs[j] for j in range(5) if j != f)) for f in range(5)] for cs in kc]
    p1v4 = {s: np.mean([prf_arrays([image_counts(set(ms[t] if s != "human" else kc[t][f]), set(rest[t][f] | go[t]),
                                                 _ancestors) for t in range(len(ids))], idx)["P"] for f in range(5)], axis=0)
            for s, ms in {"human": None, **obj}.items()}
    classes = sorted({o for cs in kc for c in cs for o in c} | {o for ms in obj.values() for m in ms for o in m})
    human = extras(kc, rest, go, classes)
    corr = {s: corrected(extras([[m] * 5 for m in ms], rest, go, classes), human, np.array([5.0 * len(m) for m in ms]), w)
            for s, ms in obj.items()}
    out = {"what": "scripts/committee_headroom.py (V5): committees, corrected precision, typicality inflation",
           "n_images": len(ids), "B": a.B, "pools": {k: list(v) for k, v in pools.items()}, "systems": {}}
    for s in obj:
        out["systems"][s] = {"objects_per_caption": round(float(np.mean([len(m) for m in obj[s]])), 3),
                             **{f"{q}_{g}": summ(prf[g][s][q]) for g in golds for q in ("P", "R", "F1")},
                             **{k: summ(v) for k, v in corr[s].items()}, "P_1v4_plus_panel": summ(p1v4[s])}
    out["human_P_1v4_plus_panel"] = summ(p1v4["human"])
    base = {"short": "fuse2_s42-short", "detailed": "fuse2_s42-detailed"}
    out["vs_fuse2"] = {}
    for s in obj:
        mode = "short" if s.endswith("short") else "detailed"
        if s in (base[mode], f"p1-gold-{mode}"):
            continue
        d = {f"d{q}_{g}": summ(prf[g][s][q] - prf[g][base[mode]][q], test=True) for g in golds for q in ("P", "R")}
        d["dP_corrected"] = summ(corr[s]["P_corrected"] - corr[base[mode]]["P_corrected"], test=True)
        for g in golds:
            dp, dr = mix_excess(rows[g][s], rows[g][f"p1-gold-{mode}"], rows[g][base[mode]], w)
            if not np.isnan(dp[0]):  # only for a count on the chord
                d[f"mix_dP_{g}"], d[f"mix_dR_{g}"] = summ(dp), summ(dr)
        out["vs_fuse2"][s] = d
        print(f"  {s:28s} " + "  ".join(f"{k} {v[:2]}" for k, v in d.items() if k in ("dP_ktvic5", "dP_union",
                                                                                    "dP_corrected", "mix_dP_union")), flush=True)
    out["fuse2_minus_p1"] = {m: summ(corr[f"fuse2_s42-{m}"]["P_corrected"] - corr[f"p1-gold-{m}"]["P_corrected"], test=True)
                             for m in MODES}
    print("corrected P: " + " | ".join(f"{s} {v['P_corrected'][0]:.1f}" for s, v in out["systems"].items()), flush=True)
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"-> {a.out}")
    return 0


def _check() -> None:
    caps = ["Một người đàn ông và con chó.", "Một người đàn ông. Con chó cạnh xe máy.", "Người đàn ông đứng."]
    assert cover(caps, 2) == "Một người đàn ông và con chó." and cover(caps, 3) == "Một người đàn ông."
    assert mbr(caps, [0, 2]) == caps[0]
    assert vote_fuse(["người đàn ông và con chó", "con chó", "con chó nằm"], 2) == "con chó."
    rows_a = [(1, 2, 1, 0.5, 0.5, 0.5)] * 4     # 2 objects/image, 1 true
    rows_b = [(2, 4, 2, 1.0, 1.0, 1.0)] * 4     # 4 objects/image, 2 true
    dp, dr = mix_excess([(3, 3, 3, 1.0, 1.0, 1.0)] * 4, rows_a, rows_b, np.ones((1, 4)))
    assert abs(dp[0] - 100 * (3 - 1.5) / 3) < 1e-9 and abs(dr[0] - 25) < 1e-9
    # human: 4 ref-false mentions of class 0, 2 confirmed (s = 0.5); system: 2 ref-false, 1 confirmed -> 0 hallucinated
    h = (np.array([[4.0, 0.0]]), np.array([[2.0, 0.0]]))
    c = corrected((np.array([[2.0, 0.0]]), np.array([[1.0, 0.0]])), h, np.array([10.0]), np.ones((1, 1)))
    assert c["P_corrected"][0] == 100 and abs(c["sensitivity_global"][0] - 50) < 1e-9


if __name__ == "__main__":
    _check()
    sys.exit(main())
