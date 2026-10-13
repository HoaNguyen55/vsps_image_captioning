#!/usr/bin/env python
"""PLAN-F1 (judge D10 (ii)): choose the object set a caption should name by the metric's own Bayes act, then let a
list-conditioned realiser write it. Pre-registration: manuscript/prereg/2026-10-13_plan_f1.md.

    python scripts/plan_f1.py realiser-data --sft BASE/sft.jsonl --out DIR      # P1_dev's rows + the plan suffix
    python scripts/plan_f1.py plan --split dev --greedy G.preds.json --samples S05.jsonl S08.jsonl --out PLAN.json
    python scripts/plan_f1.py plan --split test --greedy GT.preds.json --samples T05.jsonl T08.jsonl \\
        --dev-greedy G.preds.json --dev-samples S05.jsonl S08.jsonl --out PLAN.json
    python scripts/plan_f1.py upe --split dev --greedy G.preds.json --samples S05.jsonl --out U-short.preds.json
    python scripts/plan_f1.py score --split dev --plan PLAN.json --greedy G.preds.json --upe U.preds.json \\
        --realised R.preds.json --eval greedy=G.json upe=U.json realised=R.json --out SCORE.json
    python scripts/plan_f1.py --self-check

Posterior: per image, the classes (rescap.chair.objects_in, the 113-entry lexicon) of the greedy caption and of 12
samples (6 at T 0.5, then 6 at T 0.8). q(class in the union of the 5 references) is an L2 logistic regression on
[1, v, g, v*g, lp, v*lp]: v = share of the 12 samples naming it, g = the greedy caption names it, lp = logit of its
train-minus-dev300 prior. Dev: 5 folds (random.Random(0) shuffle of the int-sorted ids, rank mod 5), each fold scored by
a model fitted on the other 4. Test: one model fitted on all of dev300.
Decision (object_prf.py's metric: micro P, macro R): include o iff q_o + kappa E[y_o/|G|] >= P*, kappa = P*^2 m / R*^2,
(P*, R*, m) the operating point the posterior itself expects, iterated to a fixed point; E[y_o/|G|] under independent
classes plus Poisson(lam) gold outside the pool. Then at most CAP classes per image, highest q first.
Realiser: the plan reaches the model through evaluate.py --tags, whose suffix the training rows carry verbatim.
Writes numbers, plans and file hashes; the only captions it writes are model outputs (the UPE picks).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from object_prf import image_counts, paired, scores  # noqa: E402
from rescap.chair import objects_in  # noqa: E402

TEMPS, N_PER_T = ("0.5", "0.8"), 6          # frozen (pre-registration)
FOLDS, FOLD_SEED, L2, NEWTON = 5, 0, 1e-2, 50
START, FP_STEPS, POIS_MAX, CAP = (0.75, 0.45), 100, 30, 3
T_STAR = "0.5"                               # UPE-MBR's T* (D9 step B, data/results/upe/upe_temperature.txt)
K1_NAMED, K1_UNPLANNED, K2_GREEDY, K2_UPE, K3_CIDER, K3_BLEU4 = 0.85, 0.3, 3.0, 1.0, 5.0, 3.0
TEST_DF1, TEST_CIDER, B = 2.0, 8.0, 2000
SUFFIX = " Các đối tượng có thể có trong ảnh: "  # evaluate.py --tags appends SUFFIX + ", ".join(tags) + "."
SYSTEMS = ("greedy", "upe", "realised")
DEV = ROOT / "data" / "splits" / "ktvic_dev300.txt"
UPE_DIR = ROOT / "data" / "results" / "upe"
FRONTIER = ROOT / "manuscript" / "prereg" / "2026-10-12_ladder_predictions.json"
EXACT = lambda c: {c}  # noqa: E731  (object_prf's flat class space)


# ----------------------------------------------------------------------------------------------- plans and prompts
def objs(text: str) -> frozenset[str]:
    return frozenset(objects_in(text))


def plan_of(text: str) -> list[str]:
    """A caption's own plan: its classes in first-mention order, each once (the realiser's training list)."""
    return list(dict.fromkeys(objects_in(text)))


def with_plan(prompt: str, plan: list[str]) -> str:
    return prompt + SUFFIX + ", ".join(plan) + "." if plan else prompt


def plan_in(prompt: str) -> list[str]:
    return prompt.split(SUFFIX, 1)[1][:-1].split(", ") if SUFFIX in prompt else []


def realiser_data(args) -> dict:
    """P1_dev's SFT rows (build_gold_sft.py, first caption, train minus dev300) with the target's plan in the prompt."""
    from evaluate import PROMPTS
    src = Path(args.sft)
    rows = [json.loads(line) for line in src.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert all(r["prompt"] == PROMPTS["short"] and r["variant"] == "gold" for r in rows), "not P1's short rows"
    out = [{**r, "prompt": with_plan(r["prompt"], plan_of(r["response"])), "variant": "gold_plan"} for r in rows]
    for r in out:  # D10: every training list equals objects_in(target)
        assert plan_in(r["prompt"]) == plan_of(r["response"]) and set(plan_in(r["prompt"])) == objs(r["response"]), r
    dst = Path(args.out)
    dst.mkdir(parents=True, exist_ok=True)
    (dst / "sft.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out), encoding="utf-8")
    sizes = Counter(min(len(plan_in(r["prompt"])), 5) for r in out)
    return {"source_sha256": sha(src), "out_sha256": sha(dst / "sft.jsonl"), "rows": len(out),
            "plan_size_hist_0_to_5plus": [sizes[k] for k in range(6)],
            "mean_plan_size": float(np.mean([len(plan_in(r["prompt"])) for r in out]))}


# ----------------------------------------------------------------------------------------------- posterior
def sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def captions(path, ids: list[str]) -> dict[str, str]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    caps = {str(k): (v[0] if isinstance(v, list) else v) or "" for k, v in raw.items()}
    missing = [i for i in ids if i not in caps]
    if missing:
        raise SystemExit(f"{path}: no caption for {len(missing)} of {len(ids)} images")
    return caps


def pools(greedy, samples: list[str], ids: list[str]) -> list[list[str]]:
    """pool[n] = [greedy, 6 samples at T 0.5, 6 at T 0.8] for ids[n]."""
    if len(samples) != len(TEMPS):
        raise SystemExit(f"need {len(TEMPS)} sample files (T {', '.join(TEMPS)}), got {len(samples)}")
    g, rows = captions(greedy, ids), []
    for path in samples:
        r = {str(x["image_id"]): x["samples"] for x in map(json.loads, Path(path).read_text(encoding="utf-8").splitlines())}
        if any(len(r.get(i, [])) != N_PER_T for i in ids):
            raise SystemExit(f"{path}: an image lacks {N_PER_T} samples")
        rows.append(r)
    return [[g[i]] + [s for r in rows for s in r[i]] for i in ids]


def class_prior(train_refs: dict[str, list[str]]) -> tuple[dict[str, float], float]:
    """Share of the train-minus-dev300 images whose 5-reference union names each class, smoothed (c + .5) / (n + 1)."""
    dev = set(DEV.read_text(encoding="utf-8").split())
    unions = [frozenset().union(*map(objs, rs)) for i, rs in train_refs.items() if i not in dev]
    cnt, n = Counter(o for u in unions for o in u), len(unions)
    return {o: (c + 0.5) / (n + 1) for o, c in cnt.items()}, 0.5 / (n + 1)


def items(pool_rows: list[list[str]], prior) -> tuple[np.ndarray, list[str], np.ndarray]:
    """(image index, class, features) for every class any pool caption names."""
    p, unk = prior
    n_idx, names, x = [], [], []
    for n, pool in enumerate(pool_rows):
        cls = [objs(c) for c in pool]
        for o in sorted(set().union(*cls)):
            v, g = sum(o in c for c in cls[1:]) / (len(cls) - 1), float(o in cls[0])
            lp = math.log(p.get(o, unk) / (1 - p.get(o, unk)))
            n_idx.append(n)
            names.append(o)
            x.append([1.0, v, g, v * g, lp, v * lp])
    return np.array(n_idx, int), names, np.array(x).reshape(-1, 6)


def fit(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """L2 logistic regression (intercept unpenalised) by Newton's method."""
    w, pen = np.zeros(x.shape[1]), np.r_[0.0, np.full(x.shape[1] - 1, L2)]
    for _ in range(NEWTON):
        p = predict(w, x)
        step = np.linalg.solve(x.T @ (x * (p * (1 - p))[:, None]) + np.diag(pen), x.T @ (y - p) - pen * w)
        w += step
        if np.abs(step).max() < 1e-9:
            break
    return w


def predict(w: np.ndarray, x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-np.clip(x @ w, -40, 40)))


def folds(ids: list[str]) -> np.ndarray:
    order = sorted(ids, key=int)
    random.Random(FOLD_SEED).shuffle(order)
    rank = {i: k for k, i in enumerate(order)}
    return np.array([rank[i] % FOLDS for i in ids])


def labels(n_idx, names, gold) -> tuple[np.ndarray, np.ndarray]:
    """y per item, and the number of gold classes outside each image's pool."""
    y = np.array([o in gold[n] for n, o in zip(n_idx, names)], float)
    named = [set() for _ in gold]
    for n, o in zip(n_idx, names):
        named[n].add(o)
    return y, np.array([len(g - u) for g, u in zip(gold, named)], float)


def auroc(s: np.ndarray, y: np.ndarray) -> float:
    r = np.empty(len(s))
    r[np.argsort(s, kind="mergesort")] = np.arange(1, len(s) + 1)
    for v in np.unique(s):
        r[s == v] = r[s == v].mean()
    pos = y.sum()
    return float((r[y == 1].sum() - pos * (pos + 1) / 2) / (pos * (len(y) - pos)))


# ----------------------------------------------------------------------------------------------- decision
def inv_g(q: np.ndarray, lam: float) -> np.ndarray:
    """E[y_o / |G|] = q_o E[1 / (1 + sum_{o' != o} y_o' + Z)], independent y ~ Bernoulli(q), Z ~ Poisson(lam)."""
    k = np.arange(POIS_MAX + 1)
    pz = np.exp(-lam + k * math.log(max(lam, 1e-12)) - np.array([math.lgamma(x + 1) for x in k]))
    out = np.zeros(len(q))
    for j in range(len(q)):
        d = np.array([1.0])
        for p in np.delete(q, j):
            d = np.convolve(d, [1 - p, p])
        rest = np.convolve(d, pz)
        out[j] = q[j] * float((rest / (1 + np.arange(len(rest)))).sum())
    return out


def plug_in(q: np.ndarray, w: np.ndarray, n_images: int, m0: float) -> tuple[np.ndarray, dict]:
    """Fixed point of: include iff q + kappa w >= P, kappa = P^2 m / R^2, (P, R, m) expected under q."""
    P, R, m, inc = START[0], START[1], m0, None
    for step in range(1, FP_STEPS + 1):
        kappa = P * P * m / (R * R)
        new = q + kappa * w >= P
        if inc is not None and (new == inc).all():
            break
        inc = new
        P, R, m = q[inc].sum() / max(inc.sum(), 1), w[inc].sum() / n_images, inc.sum() / n_images
    return inc, {"P": float(P), "R": float(R), "m": float(m), "kappa": float(kappa), "steps": step}


def capped(n_idx, names, q, inc, n_images: int) -> list[list[str]]:
    """At most CAP included classes per image, highest q first (ties: class name); the list keeps that order."""
    out = [[] for _ in range(n_images)]
    for j in sorted(np.flatnonzero(inc), key=lambda j: (n_idx[j], -q[j], names[j])):
        if len(out[n_idx[j]]) < CAP:
            out[n_idx[j]].append(names[j])
    return out


def decide(n_idx, names, q, lam_img: np.ndarray, greedy_m: float) -> tuple[list[list[str]], dict]:
    w = np.zeros(len(q))
    for n in range(len(lam_img)):
        j = np.flatnonzero(n_idx == n)
        w[j] = inv_g(q[j], lam_img[n])
    inc, op = plug_in(q, w, len(lam_img), greedy_m)
    return capped(n_idx, names, q, inc, len(lam_img)), op


# ----------------------------------------------------------------------------------------------- modes
def split_data(split: str) -> tuple[list[str], dict, dict]:
    """(ids, their references, their non-empty OpenViIC panel captions; read for scoring only, never written)."""
    from evaluate import references
    if split == "dev":
        ids, refs, key = sorted(DEV.read_text(encoding="utf-8").split()), references("train_data.json"), "train"
    else:
        refs, key = references("test_data.json"), "test"
        ids = sorted(refs)
    panel = json.loads((ROOT / "data" / "ktvic_openviic_refs.json").read_text(encoding="utf-8"))[key]
    assert len(ids) == (300 if split == "dev" else 558), len(ids)
    return ids, {i: refs[i] for i in ids}, {i: panel[i] for i in ids if panel.get(i)}


def plan(args) -> dict:
    from evaluate import references
    tr = references("train_data.json")
    prior = class_prior(tr)
    dev_ids = sorted(DEV.read_text(encoding="utf-8").split())
    dev_gold = [frozenset().union(*map(objs, tr[i])) for i in dev_ids]
    if args.split == "dev":
        ids, rows = dev_ids, pools(args.greedy, args.samples, dev_ids)
        n_idx, names, x = items(rows, prior)
        y, z = labels(n_idx, names, dev_gold)
        fold, q, lam, ws = folds(ids), np.zeros(len(n_idx)), np.zeros(len(ids)), []
        for f in range(FOLDS):
            held = fold[n_idx] == f
            ws.append(fit(x[~held], y[~held]))
            q[held] = predict(ws[-1], x[held])
            lam[fold == f] = z[fold != f].mean()
        calib = {"weights_per_fold": [w.tolist() for w in ws], "lam_per_fold": sorted(set(lam.tolist())),
                 "auroc_crossfitted": auroc(q, y)}
    else:
        if not (args.dev_greedy and args.dev_samples):
            raise SystemExit("--split test needs --dev-greedy and --dev-samples (the calibrator is fitted on dev300)")
        dn, dnames, dx = items(pools(args.dev_greedy, args.dev_samples, dev_ids), prior)
        dy, dz = labels(dn, dnames, dev_gold)
        w = fit(dx, dy)
        ids = sorted(references("test_data.json"))
        rows = pools(args.greedy, args.samples, ids)
        n_idx, names, x = items(rows, prior)
        q, lam = predict(w, x), np.full(len(ids), dz.mean())
        calib = {"weights": w.tolist(), "lam": float(dz.mean())}
    greedy_m = float(np.mean([len(objs(r[0])) for r in rows]))
    lists, op = decide(n_idx, names, q, lam, greedy_m)
    Path(args.out).write_text(json.dumps(dict(zip(ids, lists)), ensure_ascii=False, indent=0), encoding="utf-8")
    sizes = Counter(len(lst) for lst in lists)
    rep = {"split": args.split, "inputs": {"greedy": sha(args.greedy),
                                           **{f"samples_T{t}": sha(p) for t, p in zip(TEMPS, args.samples)}},
           "calibrator": calib, "fixed_point": op, "greedy_classes_per_caption": greedy_m,
           "plan_size_hist": [sizes[k] for k in range(CAP + 1)],
           "plan_classes_per_image": float(np.mean([len(lst) for lst in lists])), "plan_sha256": sha(args.out)}
    if args.split == "dev":  # plan-level numbers on dev only: the test plan is made without test labels
        rp = [image_counts(set(lst), set(g), EXACT) for lst, g in zip(lists, dev_gold)]
        rg = [image_counts(set(objs(r[0])), set(g), EXACT) for r, g in zip(rows, dev_gold)]
        idx = np.random.default_rng(0).integers(0, len(ids), (B, len(ids)))
        fres = frontier_residual(rp, idx)
        rep["plan_level_dev"] = {
            "plan": {**scores(rp), "frontier_residual_F1": float(frontier_residual(rp, np.arange(len(ids))[None])[0]),
                     "frontier_residual_ci95": [float(np.percentile(fres, 2.5)), float(np.percentile(fres, 97.5))]},
            "greedy": scores(rg),
            "plan_minus_greedy": {k: list(v) for k, v in paired(rg, rp, n=5000).items()},
        }
    return rep


def upe(args) -> dict:
    """The frozen D9 rule at T* on [greedy, the 6 samples at T*]; writes the picked captions (model outputs)."""
    import upe_mbr as U
    from evaluate import references
    ids, refs, _ = split_data(args.split)
    tr = references("train_data.json")
    train = {j: rs for j, rs in tr.items() if args.split == "test" or j not in set(ids)}
    assert len(train) == (3469 if args.split == "dev" else 3769), len(train)
    tok = U.segmenter()
    pool = U.load_pool(args.greedy, args.samples[0], ids)
    gold = [frozenset().union(*map(objs, refs[i])) for i in ids]
    v = U.Scorer(pool, ids, refs, {"ktvic": gold}, tok, objs)
    u = U.utilities(v.tok, v.cls, U.tok_groups(tok, train))
    pk = U.pick(u["base"], u["E"], U.LAM)
    Path(args.out).write_text(json.dumps({i: pool[n][pk[n]] for n, i in enumerate(ids)}, ensure_ascii=False, indent=1),
                              encoding="utf-8")
    d = U.obj(v.picked("ktvic", np.zeros(len(ids), int)), v.picked("ktvic", pk))
    rep = {"switched": float(np.mean(pk != 0)), "obj_vs_greedy": d,
           "cider_vs_greedy": U.boot(v.cider[np.arange(len(ids)), pk] - v.cider[:, 0]), "samples": sha(args.samples[0])}
    if args.split == "dev":  # it must reproduce D9 step B's committed number exactly
        ref = json.loads((UPE_DIR / "upe_choose_t.json").read_text(encoding="utf-8"))[f"T{T_STAR}"]
        assert abs(ref["upe_vs_greedy"]["obj_ktvic"]["F1"][0] - d["F1"][0]) < 1e-6, (ref["upe_vs_greedy"], d)
        rep["reproduces_step_B"] = True
    return rep


def k1(plans: list[list[str]], mentioned: list[frozenset]) -> dict:
    planned = sum(len(p) for p in plans)
    named = sum(len(set(p) & m) for p, m in zip(plans, mentioned)) / max(planned, 1)
    unplanned = sum(len(m - set(p)) for p, m in zip(plans, mentioned)) / len(plans)
    by_size = {}
    for sz in range(CAP + 1):
        sub = [(set(p), m) for p, m in zip(plans, mentioned) if len(p) == sz]
        if sub:
            pl = sum(len(p) for p, _ in sub)
            by_size[str(sz)] = {
                "n_images": len(sub),
                "named_share": sum(len(p & m) for p, m in sub) / pl if pl else 1.0,
                "unplanned_per_caption": sum(len(m - p) for p, m in sub) / len(sub),
                "exact_match_share": sum(p == m for p, m in sub) / len(sub),
            }
    return {"named_share": named, "unplanned_per_caption": unplanned,
            "pass": named >= K1_NAMED and unplanned <= K1_UNPLANNED, "by_plan_size": by_size}


def k2(vs_greedy: dict, vs_upe: dict) -> bool:
    return vs_greedy["F1"][0] >= K2_GREEDY and vs_greedy["F1"][1] > 0 and vs_upe["F1"][0] >= K2_UPE


def k3(d_cider: float, d_bleu4: float) -> bool:
    return d_cider >= -K3_CIDER and d_bleu4 >= -K3_BLEU4


def frontier_residual(rows: list[tuple], idx: np.ndarray) -> np.ndarray:
    """F1 minus the pre-registered frontier's F1 at the same classes per caption (ladder anchors), per draw in idx."""
    from prereg_ladder_check import at
    fr = json.loads(FRONTIER.read_text(encoding="utf-8"))["anchors"]["frontier"]
    a = np.array([(r[0], r[1], r[3]) for r in rows], float)
    tp, m, rc = a[:, 0][idx], a[:, 1][idx], a[:, 2][idx]
    p = 100 * tp.sum(1) / np.maximum(m.sum(1), 1)
    r = 100 * np.nanmean(rc, axis=1)
    f1 = 2 * p * r / np.maximum(p + r, 1e-9)
    return f1 - np.array([at(fr, mm)[2] for mm in m.mean(1)])


def score(args) -> dict:
    """K1-K3 (dev) or the negative rule (test), with every column D10 requires next to an F1."""
    import second_panel as SP
    import upe_mbr as U
    from abs_halluc import CJK
    from rl_reward import boot
    ids, refs, panel = split_data(args.split)
    caps = {s: captions(p, ids) for s, p in zip(SYSTEMS, (args.greedy, args.upe, args.realised))}
    plans = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    ev = dict(e.split("=", 1) for e in args.eval)
    gold = [frozenset().union(*map(objs, refs[i])) for i in ids]
    v = U.Scorer([[caps[s][i] for s in SYSTEMS] for i in ids], ids, refs, {"ktvic": gold}, U.segmenter(), objs)
    rows = {s: v.picked("ktvic", np.full(len(ids), k)) for k, s in enumerate(SYSTEMS)}
    idx = np.random.default_rng(0).integers(0, len(ids), (B, len(ids)))
    full = np.arange(len(ids))[None]
    res = {"split": args.split, "inputs": {"plan": sha(args.plan), **{s: sha(p) for s, p in
                                                                       zip(SYSTEMS, (args.greedy, args.upe, args.realised))}},
           "systems": {}}
    sp = SP.analyse(refs, panel, {f"{s}-short": {i: caps[s][i] for i in panel} for s in SYSTEMS},
                    [("greedy", "realised"), ("upe", "realised")], B)
    for k, s in enumerate(SYSTEMS):
        sc, metrics = scores(rows[s]), json.loads(Path(ev[s]).read_text(encoding="utf-8"))["results"][0]
        chair = U.chair_counts({i: caps[s][i] for i in ids}, refs)
        fres = frontier_residual(rows[s], idx)
        res["systems"][s] = {
            "P": sc["P"], "R": sc["R"], "F1": sc["F1"], "classes_per_caption": float(np.mean([r[1] for r in rows[s]])),
            "chair_i_ktvic": float(100 * chair[:, 1].sum() / max(chair[:, 0].sum(), 1)),
            "panel_augmented_P": sp["prf"]["union"][f"{s}-short"]["P"], "panel_augmented_P_ci95":
                sp["prf"]["union"][f"{s}-short"]["ci95"]["P"], "panel_images": len(panel),
            "cider_d_x100": float(v.cider[:, k].mean()),
            **{f"eval_{m}": metrics["scores_scaled_x100"].get(m) for m in ("BLEU-4", "METEOR", "ROUGE-L", "CIDEr")},
            "frontier_residual_F1": float(frontier_residual(rows[s], full)[0]),
            "frontier_residual_ci95": [float(np.percentile(fres, 2.5)), float(np.percentile(fres, 97.5))],
            "cjk_pct": 100 * sum(bool(CJK.search(caps[s][i])) for i in ids) / len(ids)}
    vs_g, vs_u = paired(rows["greedy"], rows["realised"], n=5000), paired(rows["upe"], rows["realised"], n=5000)
    d_cider = boot(v.cider[:, 2] - v.cider[:, 0])
    d_bleu4 = res["systems"]["realised"]["eval_BLEU-4"] - res["systems"]["greedy"]["eval_BLEU-4"]
    d_front = frontier_residual(rows["realised"], idx) - frontier_residual(rows["greedy"], idx)
    res["realised_minus_greedy"] = {"objects": {k: list(x) for k, x in vs_g.items()}, "cider_d_x100": d_cider,
                                    "bleu4": d_bleu4, "panel": sp["paired"]["realised-short - greedy-short"],
                                    "frontier_residual_ci95": [float(np.percentile(d_front, 2.5)),
                                                               float(np.percentile(d_front, 97.5))]}
    res["realised_minus_upe"] = {"objects": {k: list(x) for k, x in vs_u.items()},
                                 "cider_d_x100": boot(v.cider[:, 2] - v.cider[:, 1]),
                                 "panel": sp["paired"]["realised-short - upe-short"]}
    mentioned = [objs(caps["realised"][i]) for i in ids]
    res["K1"] = k1([plans[i] for i in ids], mentioned)
    if args.split == "dev":
        res["K2"] = {"pass": k2(vs_g, vs_u), "dF1_vs_greedy": list(vs_g["F1"]), "dF1_vs_upe": list(vs_u["F1"])}
        res["K3"] = {"pass": k3(d_cider[0], d_bleu4), "d_cider_d": d_cider[0], "d_bleu4": d_bleu4}
        res["verdict"] = "PASS" if res["K1"]["pass"] and res["K2"]["pass"] and res["K3"]["pass"] else "KILL"
    else:
        res["verdict"] = "NEGATIVE" if vs_g["F1"][0] < TEST_DF1 or d_cider[0] < -TEST_CIDER else "POSITIVE"
    return res


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-check", action="store_true")
    sub = ap.add_subparsers(dest="mode")
    r = sub.add_parser("realiser-data", help="P1_dev's SFT rows with each target's plan in the prompt")
    r.add_argument("--sft", required=True)
    r.add_argument("--out", required=True)
    for name in ("plan", "upe", "score"):
        p = sub.add_parser(name)
        p.add_argument("--split", choices=("dev", "test"), required=True)
        p.add_argument("--greedy", required=True)
        p.add_argument("--out", required=True)
        if name != "score":
            p.add_argument("--samples", nargs="+", required=True, help="T 0.5 then T 0.8 (upe: the T* file only)")
    sub.choices["plan"].add_argument("--dev-greedy")
    sub.choices["plan"].add_argument("--dev-samples", nargs="+")
    s = sub.choices["score"]
    for a in ("--plan", "--upe", "--realised"):
        s.add_argument(a, required=True)
    s.add_argument("--eval", nargs=3, required=True, metavar="SYSTEM=RESULT.json", help="evaluate.py results")
    return ap


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()
    if args.self_check:
        _check()
        print("plan_f1 self-check ok")
        return 0
    if args.mode is None:
        ap.error("a mode (realiser-data, plan, upe, score) or --self-check")
    res = {"realiser-data": realiser_data, "plan": plan, "upe": upe, "score": score}[args.mode](args)
    res["script_sha256"] = sha(__file__)
    text = json.dumps(res, indent=1, default=float)
    if args.mode != "realiser-data":
        Path(args.out).with_suffix(".report.json").write_text(text, encoding="utf-8")
    else:
        (Path(args.out) / "_build_report.json").write_text(text, encoding="utf-8")
    print(text)
    return 0


def _check() -> None:
    from evaluate import PROMPTS
    src = (ROOT / "scripts" / "evaluate.py").read_text(encoding="utf-8")
    assert f'prompt += "{SUFFIX}" + ", ".join(tags[image_id]) + "."' in src, "evaluate.py --tags suffix changed"
    p = with_plan(PROMPTS["short"], ["người", "xe máy"])
    assert p == PROMPTS["short"] + SUFFIX + "người, xe máy." and plan_in(p) == ["người", "xe máy"]
    assert with_plan("x", []) == "x" and plan_in("x") == []
    assert plan_of("một người đàn ông đứng cạnh chiếc xe máy và một người đàn ông") == ["đàn ông", "xe máy"]
    f = folds([str(i) for i in range(1, 301)])
    assert np.bincount(f).tolist() == [60] * 5 and (f == folds([str(i) for i in range(1, 301)])).all()
    x = np.column_stack([np.ones(200), np.r_[np.zeros(100), np.ones(100)]])
    y = np.r_[np.zeros(80), np.ones(20), np.zeros(20), np.ones(80)]
    assert np.allclose(predict(fit(x, y), x)[[0, 150]], [0.2, 0.8], atol=1e-2)
    w = inv_g(np.array([1.0, 0.0]), 0.0)
    assert abs(w[0] - 1.0) < 1e-12 and w[1] == 0.0
    assert abs(inv_g(np.array([1.0, 1.0]), 0.0)[0] - 0.5) < 1e-12
    # two images: a sure class each, plus a 0.2 class; the operating point excludes the weak one
    q, n_idx = np.array([0.95, 0.2, 0.95]), np.array([0, 0, 1])
    lists, op = decide(n_idx, ["a", "b", "c"], q, np.zeros(2), 1.0)
    assert lists == [["a"], ["c"]] and abs(op["P"] - 0.95) < 1e-12, (lists, op)
    inc = np.ones(5, bool)
    assert capped(np.zeros(5, int), list("edcba"), np.array([.5, .9, .5, .7, .1]), inc, 1) == [["d", "b", "c"]]
    assert abs(auroc(np.array([.1, .2, .3, .4]), np.array([0, 0, 1, 1])) - 1.0) < 1e-12
    r = k1([["a", "b"], []], [frozenset({"a", "z"}), frozenset()])
    assert r["named_share"] == 0.5 and r["unplanned_per_caption"] == 0.5 and not r["pass"], r
    assert r["by_plan_size"]["2"]["named_share"] == 0.5 and r["by_plan_size"]["0"]["exact_match_share"] == 1.0, r
    assert k2({"F1": (3.0, 0.1, 6, 0)}, {"F1": (1.0, -1, 3, 0)}) and not k2({"F1": (3.5, 0.0, 6, 0)}, {"F1": (2, 0, 4, 0)})
    assert k3(-5.0, -3.0) and not k3(-5.01, 0.0) and not k3(0.0, -3.1)
    rows = [(1, 2, 1, 0.5, 0.5, 0.5)] * 4
    from prereg_ladder_check import at
    fr = json.loads(FRONTIER.read_text(encoding="utf-8"))["anchors"]["frontier"]
    assert abs(frontier_residual(rows, np.arange(4)[None])[0] - (2 * 50 * 50 / 100 - at(fr, 2.0)[2])) < 1e-9
    assert build_parser().parse_args(["score", "--split", "dev", "--greedy", "g", "--out", "o", "--plan", "p",
                                      "--upe", "u", "--realised", "r", "--eval", "greedy=a", "upe=b",
                                      "realised=c"]).eval == ["greedy=a", "upe=b", "realised=c"]


if __name__ == "__main__":
    sys.exit(main())
