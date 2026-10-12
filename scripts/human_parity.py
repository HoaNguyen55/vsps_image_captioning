#!/usr/bin/env python
"""Human parity and leakage-free target-policy scores: object P/R/F1 against held-out annotators.

    NCS_DATA=data python scripts/human_parity.py parity    # test: humans and systems vs the SAME held-out gold
    NCS_DATA=data python scripts/human_parity.py offline   # train: each target policy vs annotators it never saw
    NCS_DATA=data python scripts/human_parity.py rank p1=data/results/p1-gold-short.preds.json \\
        fuse2=data/results/fuse2_s42-detailed.preds.json,data/results/fuse2_s43-detailed.preds.json

parity (KTVIC test, 5 captions per image):
  1v4  each caption vs the union of the other 4 (5 folds); short-mode systems vs the same 4-caption unions.
  2v3  fused() of each pair of captions vs the union of the other 3 (10 folds); detailed-mode systems vs
       the same 3-caption unions.
  delta_vs_human: system - human on the same resampled images (paired, as object_prf.paired).

offline (KTVIC train), the target policies of build_gold_sft.py:
  common  for each of the C(5,2) held-out pairs of an image, every policy is built from the other 3
          captions only and scored vs the union of the 2. One gold for all policies, never seen by the
          construction: the ranking protocol.
  own     the policy built from all 5 captions, scored vs the captions it does not contain (p1 vs 2-5,
          fuse2 vs the other 3; multiref contains all 5, so it has no score). consensual() reads every
          caption, so cons/fuse2/rnd2/unf2 chose by agreement with the held-out captions (optimistic), and
          gold size differs between policies (3 or 4 captions): report, do not rank.
  fuse2/rnd2 are one fused target row; unf2/multiref train on each caption as its own row, scored
  separately and averaged (the expected score of one row). rnd2 replays build_gold_sft's single
  Random(seed) over sorted image ids, so its own-protocol targets are the trained ones.

rank: Kendall tau-b over policies between the common-protocol offline score and the trained test score
(vs all 5 references, as object_prf.py); several files for one policy (seeds) are averaged. Pair each
policy with the mode trained on its target: short for p1/cons/unf2/multiref, detailed for fuse2/rnd2.

Metrics are object_prf.py's image_counts/scores: exact-match P/R/F1 and the hypernym-credited P_h,
R_spec, F1_spec. Every score is the fold average (scores() on each fold over all images, then the
mean over folds); 95% percentile CIs resample images with all their folds (--B draws).
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from build_gold_sft import consensual, fused, fusion_set  # noqa: E402
from object_prf import image_counts, scores  # noqa: E402
from rescap.chair import _ancestors, objects_in  # noqa: E402

RESULTS = ROOT / "data" / "results"
KEYS = ("P", "R", "F1", "P_h", "R_spec", "F1_spec")
SYSTEMS = ("p1-gold", "fuse2_s42", "tags_fuse2_s42", "e5_s42", "e5dpo_s42", "zeroshot")
N_CAPTIONS = 5

#: The captions each build_gold_sft.py policy takes from an image's list; rng is --fuse-order random's.
USED = {
    "p1": lambda cs, rng: [cs[0]],
    "cons": lambda cs, rng: [consensual(cs)],
    "fuse2": lambda cs, rng: fusion_set(cs, 2),
    "rnd2": lambda cs, rng: fusion_set(cs, 2, rng),
    "unf2": lambda cs, rng: fusion_set(cs, 2),
    "multiref": lambda cs, rng: list(cs),
}
JOINED = {"fuse2", "rnd2"}  # one fused target row; the other policies make a row per caption


def load_captions(split: str) -> dict[str, list[str]]:
    from evaluate import references

    refs = {i: [c.strip() for c in cs] for i, cs in references(split).items()}
    if any(len(cs) != N_CAPTIONS for cs in refs.values()):
        sys.exit(f"{split}: the fold protocols assume {N_CAPTIONS} captions per image")
    return refs


def load_preds(path: Path | str, ids: list[str]) -> dict[str, str]:
    preds = json.loads(Path(path).read_text(encoding="utf-8"))
    preds = {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in preds.items()}
    missing = set(ids) - set(preds)
    if missing:
        sys.exit(f"{path}: no caption for {len(missing)} images (e.g. {sorted(missing)[:3]})")
    return preds


def gold_of(captions) -> set[str]:
    return set().union(*(objects_in(c) for c in captions))


def counts(text: str, gold: set[str]) -> tuple:
    return image_counts(set(objects_in(text)), gold, _ancestors)


def pool(rows: list[tuple]) -> tuple:
    """Mean of image_counts tuples (the rows of one multi-row target): tp, |M| and tp_h averaged, so P
    stays a ratio of sums; recalls averaged over the rows that have gold, nan when none has."""
    out = [sum(r[i] for r in rows) / len(rows) for i in range(3)]
    for i in range(3, 6):
        have = [r[i] for r in rows if r[i] == r[i]]
        out.append(sum(have) / len(have) if have else float("nan"))
    return tuple(out)


def folds(cs: list[str], k: int):
    """(k kept captions, the held-out rest) for every choice of k, both in file order."""
    for keep in itertools.combinations(range(len(cs)), k):
        yield [cs[i] for i in keep], [c for i, c in enumerate(cs) if i not in keep]


def join(used: list[str]) -> str:
    """fused()'s text for captions already chosen (fused() redraws them; _check pins the two equal)."""
    return " ".join(c if c.rstrip().endswith((".", "!", "?")) else c.rstrip() + "." for c in used)


def target_counts(policy: str, used: list[str], gold: set[str]) -> tuple:
    return pool([counts(t, gold) for t in ([join(used)] if policy in JOINED else used)])


def by_fold(data: list[list[tuple]], idx) -> list[dict]:
    """object_prf.scores of each fold over the images idx (data[image][fold])."""
    return [scores([data[i][f] for i in idx]) for f in range(len(data[0]))]


def fold_scores(data: list[list[tuple]], idx) -> dict:
    per = by_fold(data, idx)
    return {k: statistics.mean(s[k] for s in per) for k in KEYS}


def _ci(v: list[float]) -> list[float]:
    v = sorted(v)
    return [v[int(0.025 * len(v))], v[int(0.975 * len(v)) - 1]]


def report(data: dict[str, list[list[tuple]]], n: int, base: str | None = None) -> dict:
    """Fold-averaged scores with 95% CIs from n image resamples shared by every dataset (images keep all
    their folds, as object_prf.bootstrap); with base, each other dataset's paired difference to it on the
    same draws: point, CI, two-sided p floored at 2/n (as object_prf.paired)."""
    n_img = len(next(iter(data.values())))
    rng = random.Random(0)
    draws = {name: [] for name in data}
    for _ in range(n):
        idx = [rng.randrange(n_img) for _ in range(n_img)]
        for name, d in data.items():
            draws[name].append(fold_scores(d, idx))
    out = {}
    for name, d in data.items():
        out[name] = {**fold_scores(d, range(n_img)),
                     "objects_per_caption": statistics.mean(r[1] for folded in d for r in folded),
                     "ci95": {k: _ci([s[k] for s in draws[name]]) for k in KEYS}}
        if base is None or name == base:
            continue
        out[name][f"delta_vs_{base}"] = delta = {}
        for k in KEYS:
            v = [a[k] - b[k] for a, b in zip(draws[name], draws[base])]
            p = min(1.0, 2 * min(sum(x <= 0 for x in v), sum(x >= 0 for x in v)) / n)
            delta[k] = {"d": out[name][k] - out[base][k], "ci95": _ci(v), "p": max(p, 2 / n)}
    return out


def show(name: str, s: dict) -> None:
    line = f"  {name:24s} M/cap={s['objects_per_caption']:4.2f} " + "  ".join(
        f"{k}={s[k]:5.1f} [{s['ci95'][k][0]:5.1f},{s['ci95'][k][1]:5.1f}]" for k in ("P", "R", "F1", "F1_spec"))
    d = s.get("delta_vs_human")
    if d:
        line += "  vs human " + " ".join(f"d{k}={d[k]['d']:+.1f} (p={d[k]['p']:.4f})" for k in ("P", "R", "F1"))
    print(line)


def parity_block(refs: dict[str, list[str]], k: int, stems: list[str], n: int) -> dict:
    ids = sorted(refs)
    splits = [list(folds(refs[i], k)) for i in ids]
    golds = [[gold_of(held) for _, held in s] for s in splits]
    data = {"human": [[counts(fused(kept, k), g) for (kept, _), g in zip(s, gs)] for s, gs in zip(splits, golds)]}
    for stem in stems:
        preds = load_preds(RESULTS / f"{stem}.preds.json", ids)
        data[stem] = [[counts(preds[i], g) for g in gs] for i, gs in zip(ids, golds)]
    out = report(data, n, base="human")
    labels = ["+".join(str(c + 1) for c in keep) for keep in itertools.combinations(range(N_CAPTIONS), k)]
    out["human"]["per_fold"] = {lab: {m: s[m] for m in ("P", "R", "F1")}
                                for lab, s in zip(labels, by_fold(data["human"], range(len(ids))))}
    for name, s in out.items():
        show(name, s)
    return {"human": out.pop("human"), "systems": out}


def cmd_parity(args) -> dict:
    refs = load_captions(args.split)
    out = {"split": args.split, "n_images": len(refs), "B": args.B}
    for proto, k, stems, gold in (("1v4", 1, args.vs1, "union of the other 4 captions"),
                                  ("2v3", 2, args.vs2, "union of the other 3 captions")):
        print(f"{proto}: human = fused() of {k} caption(s), gold = {gold}, {len(refs)} images")
        out[proto] = {"gold": gold, **parity_block(refs, k, stems, args.B)}
    return out


def cmd_offline(args) -> dict:
    refs = load_captions(args.split)
    own = {p: [] for p in USED if p != "multiref"}
    common = {p: [] for p in USED}
    rng_own, rng_common = random.Random(args.seed), random.Random(args.seed)
    for i in sorted(refs):
        cs = refs[i]
        for p in own:
            used = USED[p](cs, rng_own)
            own[p].append([target_counts(p, used, gold_of(c for c in cs if c not in used))])
        per = {p: [] for p in USED}
        for kept, held in folds(cs, N_CAPTIONS - 2):
            gold = gold_of(held)
            for p in USED:
                per[p].append(target_counts(p, USED[p](kept, rng_common), gold))
        for p in USED:
            common[p].append(per[p])
    out = {"split": args.split, "n_images": len(refs), "B": args.B, "seed": args.seed, "protocols": {}}
    for proto, data in (("common", common), ("own", own)):
        print(f"{proto}: target policies vs held-out annotators, {len(refs)} images")
        out["protocols"][proto] = report(data, args.B)
        for p, s in out["protocols"][proto].items():
            show(p, s)
    return out


def cmd_rank(args) -> dict:
    from scipy.stats import kendalltau

    offline = json.loads(Path(args.offline).read_text(encoding="utf-8"))["protocols"]["common"]
    refs = load_captions(args.split)
    ids = sorted(refs)
    gold = {i: gold_of(refs[i]) for i in ids}
    table = {}
    for spec in args.mapping:
        policy, _, files = spec.partition("=")
        if policy not in offline or not files:
            sys.exit(f"{spec!r}: want POLICY=PREDS[,PREDS...] with POLICY one of {', '.join(offline)}")
        runs = []
        for f in files.split(","):
            preds = load_preds(f, ids)
            runs.append(scores([counts(preds[i], gold[i]) for i in ids]))
        table[policy] = {"files": files.split(","),
                         "offline": {k: offline[policy][k] for k in ("P", "R", "F1")},
                         "trained": {k: statistics.mean(r[k] for r in runs) for k in ("P", "R", "F1")}}
        print(f"  {policy:10s} offline F1={table[policy]['offline']['F1']:5.1f}  "
              f"trained F1={table[policy]['trained']['F1']:5.1f}  ({len(runs)} file(s))")
    tau = {}
    for k in ("P", "R", "F1"):
        t, p = kendalltau([v["offline"][k] for v in table.values()], [v["trained"][k] for v in table.values()])
        tau[k] = {"tau_b": float(t), "p": float(p)}
        print(f"  Kendall tau-b ({k}, {len(table)} policies) = {tau[k]['tau_b']:+.3f}  p={tau[k]['p']:.4f}")
    return {"protocol": "common", "split": args.split, "policies": table, "kendall": tau}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    par = sub.add_parser("parity", help="test split: humans vs systems on the same held-out gold")
    par.add_argument("--split", default="test_data.json")
    par.add_argument("--vs1", nargs="+", default=[f"{s}-short" for s in SYSTEMS], help="preds stems vs 1 human")
    par.add_argument("--vs2", nargs="+", default=[f"{s}-detailed" for s in SYSTEMS], help="preds stems vs 2 humans")
    par.add_argument("--out", default=str(RESULTS / "human_parity.json"))
    off = sub.add_parser("offline", help="train split: target policies vs annotators not used to build them")
    off.add_argument("--split", default="train_data.json")
    off.add_argument("--seed", type=int, default=42, help="build_gold_sft --seed (rnd2's draw)")
    off.add_argument("--out", default=str(RESULTS / "policy_offline.json"))
    rank = sub.add_parser("rank", help="Kendall tau between offline and trained scores over policies")
    rank.add_argument("mapping", nargs="+", metavar="POLICY=PREDS[,PREDS...]")
    rank.add_argument("--offline", default=str(RESULTS / "policy_offline.json"))
    rank.add_argument("--split", default="test_data.json")
    rank.add_argument("--out", default=None)
    for p in (par, off):
        p.add_argument("--B", type=int, default=5000, help="bootstrap resamples")
    args = ap.parse_args()
    out = {"parity": cmd_parity, "offline": cmd_offline, "rank": cmd_rank}[args.cmd](args)
    if args.out:
        Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"  -> {args.out}")
    return 0


def _check() -> None:
    cs = ["một người đàn ông đứng.", "một người đàn ông và con chó", "con chó cạnh chiếc xe máy"]
    assert join(fusion_set(cs, 2)) == fused(cs, 2) and join(cs[:1]) == fused(cs[:1], 1)
    nan = float("nan")
    assert pool([(1, 2, 1, 0.5, 0.5, 1.0), (0, 2, 1, nan, nan, nan)]) == (0.5, 2.0, 1.0, 0.5, 0.5, 1.0)
    no_gold = pool([(0, 1, 0, nan, nan, nan)])
    assert no_gold[3] != no_gold[3]
    splits = list(folds(list("abcde"), 3))
    assert len(splits) == 10 and all(sorted(k + h) == list("abcde") and len(h) == 2 for k, h in splits)
    tp, m, *_ = target_counts("fuse2", fusion_set(cs, 2), gold_of(cs[1:]))
    assert tp == m == 3 and target_counts("unf2", cs[1:], gold_of(cs[:1]))[:2] == (0.5, 2.0)
    # fold average, not a pool: P is 1/1 on fold 0 and 0/3 on fold 1 -> 50 (pooling the folds gives 25)
    a = [[(1, 1, 1, 1.0, 1.0, 1.0), (0, 3, 0, 0.0, 0.0, 0.0)]] * 20
    b = [[(2, 2, 2, 1.0, 1.0, 1.0)] * 2] * 20
    r = report({"a": a, "b": b, "c": a}, 200, base="a")
    assert r["a"]["P"] == r["a"]["F1"] == 50.0 and r["a"]["ci95"]["P"] == [50.0, 50.0], r["a"]
    assert r["b"]["delta_vs_a"]["F1"]["d"] > 0 and r["b"]["delta_vs_a"]["F1"]["p"] == 0.01
    assert r["c"]["delta_vs_a"]["F1"] == {"d": 0.0, "ci95": [0.0, 0.0], "p": 1.0}


if __name__ == "__main__":
    _check()
    sys.exit(main())
