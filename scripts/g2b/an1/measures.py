#!/usr/bin/env python3
"""A-N1: object metrics under incomplete gold, ported from IR (DESIGN.md). Imports scripts/g2b/score_g2b.py unchanged.

  selftest  assert-based checks on toy cases with known answers
  stage1    EXPLORATORY development on COCO-2500, UIT-ViIC test and XM3600 (STAGE1_PLAN.md); never overwrites --out

  OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 nice -n 15 python3 measures.py stage1 --out stage1_results.json
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / "scripts/g2b/score_g2b.py").exists())
sys.path.insert(0, str(ROOT / "scripts/g2b"))
import score_g2b as g  # noqa: E402

U80 = frozenset(c for _, c in g.VI_TERMS)  # the 80 classes of the coco80 lexicon
MEASURES = ("F1", "cF1", "bpref")
CANDIDATES = ("cF1", "bpref")
TIE, STEP, CAP, KILL_MIN_SETS = 0.05, 0.05, 1.0, 2  # STAGE1_PLAN.md section 3
REPRO_TOL = 0.005  # STAGE1_PLAN.md section 2, data-path check


# ------------------------------------------------------------------------------------------------ measures
def negatives(lexd: dict, lx: str) -> list[set]:
    """Verified negatives N_i of the complete gold (DESIGN.md section 2 and D7)."""
    if "oiv7" in lexd:
        return [{c for c, v in s.items() if v == "absent"} for s in lexd["oiv7"]]
    if lx != "coco80" or "complete" not in lexd:
        raise ValueError(f"no verified negatives for lexicon {lx!r} (DESIGN.md D7)")
    return [set(U80 - c) for c in lexd["complete"]]


def positives(ds, lx: str, level: str) -> list[list[set]]:
    """G_is at a level: per random draw s, the per-image positive sets."""
    if level == "oiv7_verified":
        return [[{c for c, v in s.items() if v == "present"} for s in ds.lex[lx]["oiv7"]]]
    return ds.variants[lx][level]


def judged_rows(ment: list[set], gold: list[list[set]], neg: list[set]) -> dict:
    """score_g2b.rows plus j = |m & J| with the judged pool J = G | (N - G)."""
    r = g.rows(ment, gold)
    r["j"] = np.array([[len(m & (G | N)) for m, G, N in zip(ment, gs, neg)] for gs in gold], float)
    return r


def condensed(r: dict, idx: np.ndarray, W: np.ndarray) -> dict:
    """score_g2b.scores with unjudged mentions removed from precision (cF1); recall is unchanged."""
    tp, j, has, rec = (r[k][:, idx] for k in ("tp", "j", "has", "rec"))
    P = g.div(tp @ W.T, j @ W.T, 0.0)
    R = g.div((rec * has) @ W.T, has @ W.T, np.nan)
    F = g.div(2 * P * R, P + R, 0.0)
    return {"P": P.mean(0), "R": R.mean(0), "F": F.mean(0), "M": (W @ r["m"][idx]) / W.sum(1)}


def emin(fp, R):
    """E[min(K, R)] for K uniform on {0, ..., fp}: the capped count of negatives above a positive in random order."""
    fp, R = np.asarray(fp, float), np.asarray(R, float)
    return np.where(fp <= R, fp / 2, (R * (R + 1) / 2 + (fp - R) * R) / (fp + 1))


def bpref_rows(ment: list[set], gold: list[list[set]], neg: list[set]) -> dict:
    """Per draw and image: bpref_set = TP/R * (1 - E[min(K, R)] / min(R, N')); no penalty when N' = 0 (trec_eval)."""
    def grid(f):
        return np.array([[f(m, G, N) for m, G, N in zip(ment, gs, neg)] for gs in gold], float)
    tp, R = grid(lambda m, G, N: len(m & G)), grid(lambda m, G, N: len(G))
    fp, n = grid(lambda m, G, N: len(m & (N - G))), grid(lambda m, G, N: len(N - G))
    pen = g.div(emin(fp, R), np.minimum(R, n), 0.0)
    return {"b": g.div(tp, R, 0.0) * (1 - pen), "has": (R > 0).astype(float),
            "m": np.array([len(m) for m in ment], float)}


def bpref(r: dict, idx: np.ndarray, W: np.ndarray) -> dict:
    b, has = r["b"][:, idx], r["has"][:, idx]
    return {"F": g.div((b * has) @ W.T, has @ W.T, np.nan).mean(0), "M": (W @ r["m"][idx]) / W.sum(1)}


def analyse(ds, systems: list[str], lx: str, levels: list[str], idx: np.ndarray, W: np.ndarray,
            floor: float) -> dict[str, np.ndarray]:
    """Verbosity slopes (levels x weight rows) of F1, cF1 and bpref_set; row 0 of W should be the point estimate."""
    neg = negatives(ds.lex[lx], lx)
    out: dict[str, list] = {mu: [] for mu in MEASURES}
    for lv in levels:
        gold = positives(ds, lx, lv)
        per: dict[str, list] = {mu: [] for mu in MEASURES}
        for s in systems:
            reg = g.scores(ds.rows(s, lv, lx), idx, W)
            ment = ds.ment(s, lx)
            if lv == levels[-1]:
                if lx == "coco80":  # D3: nothing is unjudged under the complete coco80 gold
                    cond = condensed(judged_rows(ment, gold, neg), idx, W)
                    assert all(np.allclose(cond[k], reg[k], equal_nan=True) for k in ("P", "R", "F", "M")), s
                per["cF1"].append(reg)
            else:
                per["cF1"].append(condensed(judged_rows(ment, gold, neg), idx, W))
            per["F1"].append(reg)
            per["bpref"].append(bpref(bpref_rows(ment, gold, neg), idx, W))
        for mu in MEASURES:
            out[mu].append(g.stat_slope(per[mu], floor))
    return {mu: np.stack(v) for mu, v in out.items()}


def summary(S: dict[str, np.ndarray], levels: list[str], lo: float, hi: float) -> dict:
    """[point, CI] of the slopes, Range, rho = Range / Range_F1 and Q(theta = 1) = Range_F1 - Range."""
    with np.errstate(invalid="ignore", divide="ignore"):
        rng = {mu: S[mu].max(0) - S[mu].min(0) for mu in S}
        out = {}
        for mu in S:
            o = {"slope": {lv: pc(S[mu][k], lo, hi) for k, lv in enumerate(levels)}, "range": pc(rng[mu], lo, hi)}
            if mu != "F1":
                o["rho"] = pc(rng[mu] / rng["F1"], lo, hi)
                o["Q_theta1"] = pc(rng["F1"] - rng[mu], lo, hi)
            out[mu] = o
    return out


def pc(v: np.ndarray, lo: float, hi: float) -> list:
    return [float(v[0]), g.ci(v[1:], lo, hi)]


def diagnostics(ds, systems: list[str], lx: str, levels: list[str]) -> dict:
    """Unjudged share of mentions per level (all systems pooled, mean over draws), D6 conflicts and D2 images."""
    neg = negatives(ds.lex[lx], lx)
    out = {"unjudged_share": {}}
    for lv in levels:
        gold = positives(ds, lx, lv)
        j = sum(judged_rows(ds.ment(s, lx), gold, neg)["j"].sum(1) for s in systems)
        m = sum(sum(len(x) for x in ds.ment(s, lx)) for s in systems)
        out["unjudged_share"][lv] = float(np.mean(1 - j / m))
    allr = positives(ds, lx, levels[1])[0]
    out["conflict_pairs_all_refs"] = int(sum(len(G & N) for G, N in zip(allr, neg)))
    out["positive_pairs_all_refs"] = int(sum(len(G) for G in allr))
    out["images_without_negatives"] = int(sum(not N for N in neg))
    return out


# ------------------------------------------------------------------------------------------------ choice rule
def choose(sets: dict) -> dict:
    """STAGE1_PLAN.md section 3, from the stage-1 rho of each candidate."""
    shrink = {mu: {d: (None if not math.isfinite(v["measures"][mu]["rho"][0]) else 1 - v["measures"][mu]["rho"][0])
                   for d, v in sets.items()} for mu in CANDIDATES}
    adm = [mu for mu in CANDIDATES if all(x is not None for x in shrink[mu].values())]
    out = {"shrink_point": shrink, "admissible": adm}
    if not adm:
        return {**out, "primary": None, "kill": True, "theta": None}
    score = {mu: min(shrink[mu].values()) for mu in adm}
    best = max(adm, key=lambda mu: score[mu])
    if len(adm) == len(CANDIDATES) and abs(score["cF1"] - score["bpref"]) < TIE:
        best = "cF1"
    kill = sum(x <= 0 for x in shrink[best].values()) >= KILL_MIN_SETS
    his = [v["measures"][best]["rho"][1] for v in sets.values()]
    theta = CAP if any(h is None for h in his) else \
        min(CAP, round(math.ceil(max(h[1] for h in his) / STEP - 1e-9) * STEP, 10))
    return {**out, "score_min_shrink": score, "primary": best, "kill": kill, "theta": theta,
            "theta_source": "max over sets of the 97.5th percentile of rho, rounded up to a multiple of STEP, capped"}


# ------------------------------------------------------------------------------------------------ stage 1
def dev_dataset(reg: dict, ids: list[str], lexicons: dict, caps: dict, complete: str):
    """A score_g2b.Dataset over stage-1 data: registered random draws (k = 1) and the selfcheck's first-k golds."""
    dc = reg["design_constants"]
    ds = object.__new__(g.Dataset)
    ds.reg, ds.name, ds.caps, ds.lang, ds.complete, ds.ids, ds.lex = reg, "stage1", caps, {}, complete, ids, lexicons
    first = next(iter(lexicons.values()))
    ds.subsets = g.random_subsets([len(r) for r in first["refs"]], 1, dc["n_random_subsets"]["value"],
                                  dc["set_by_this_registration"]["subset_seed"])
    ds.variants = {lx: {**g.gold_variants(v, None, firstk=True), **g.gold_variants(v, ds.subsets)}
                   for lx, v in lexicons.items()}
    ds._ment, ds._rows = {}, {}
    return ds


def stage1_inputs() -> list[tuple]:
    """The three selfcheck families (score_g2b.selfcheck's file lists), primary lexicon only (DESIGN.md D7)."""
    res = ROOT / "data/results"
    cids = [str(i["cocoid"]) for i in sorted(g.jload(ROOT / "data/coco_probe/manifest.json")["images"],
                                              key=lambda x: x["cocoid"])]
    cfiles = {f.name.split(".shard")[0] + ("+vcd" if d == "coco5000_vcd" else ""): f
              for d in ("coco5000", "coco_transfer", "coco5000_vcd") for f in sorted((res / d).glob("*.shard*.jsonl"))}
    ufiles = {**{"transfer_" + f.name.removeprefix("uitviic_").removesuffix(".preds.json"): f
                 for f in sorted((res / "uitviic").glob("*.preds.json")) if "zeroshot" not in f.name},
              **{f.name.removeprefix("uitviic_").removesuffix(".preds.json"): f
                 for f in sorted((res / "uitviic").glob("*zeroshot*.preds.json"))},
              **{"ind_" + f.name.removeprefix("uitviic_").removesuffix(".preds.json"): f
                 for f in sorted((res / "uitviic_ind_test").glob("*.preds.json"))}}
    xfiles = {f.name.removesuffix(".preds.json"): f for f in sorted((res / "xm3600").glob("*.preds.json"))}
    u, x = g.uitviic_context(), g.xm3600_context()
    return [("COCO-2500", "COCO-2500 (check_coco)", cids, {"coco80": g.coco_context(cids)["lexicons"]["coco80"]},
             cfiles, "inst"),
            ("UIT-ViIC test", "UIT-ViIC test all_10 (coco80)", u["ids"], {"coco80": u["lexicons"]["coco80"]}, ufiles,
             "inst"),
            ("XM3600", "XM3600 (full verdict, v2)", x["ids"], x["lexicons"], xfiles, "oiv7_verified")]


def stage1(out: Path) -> int:
    if out.exists():
        raise SystemExit(f"{out} exists; never overwritten (AGENT_RULES 3)")
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    reg = g.jload(g.PREREG)
    dc = reg["design_constants"]
    floor, lo, hi, nb = (dc[k]["value"] for k in ("tp_floor", "ci_lo_percentile", "ci_hi_percentile", "n_boot"))
    cells = [c for c in g.jload(ROOT / "data/results/g2b/selfcheck.json")["cells"] if c["stat"] == "slope"]
    sets, inputs = {}, {}
    for name, fam, ids, lexicons, files, complete in stage1_inputs():
        caps = {s: g.read_captions(f) for s, f in files.items()}
        inputs[name] = {s: [str(f.relative_to(ROOT)), g.sha256_file(f)] for s, f in files.items()}
        ds = dev_dataset(reg, ids, lexicons, caps, complete)
        lx, systems, n = next(iter(lexicons)), list(caps), len(ids)
        one, idx = np.ones((1, n)), np.arange(n)
        check = []
        for c in (c for c in cells if c["family"] == fam):
            mine = float(g.stat_slope([g.scores(ds.rows(s, c["gold"], lx), idx, one) for s in systems], floor)[0])
            check.append({"gold": c["gold"], "selfcheck_reproduced": c["reproduced"], "stage1_path": mine,
                          "ok": abs(mine - c["reproduced"]) <= REPRO_TOL})
        if not check or not all(c["ok"] for c in check):
            raise SystemExit(f"{name}: data-path check failed: {check}")
        levels = ["refs1_randk", "refs_all", complete]  # prereg golds.<set>.one_ref, all_refs, complete
        W = np.random.default_rng(dc["set_by_this_registration"]["bootstrap_seed"]).multinomial(
            n, np.full(n, 1.0 / n), size=nb).astype(float)
        S = analyse(ds, systems, lx, levels, idx, np.vstack([one, W]), floor)
        sets[name] = {"family_in_selfcheck": fam, "lexicon": lx, "n_images": n, "systems": systems, "levels": levels,
                      "data_path_check": check, "measures": summary(S, levels, lo, hi),
                      "diagnostics": diagnostics(ds, systems, lx, levels)}
        print(name, json.dumps({mu: v["range"][0] for mu, v in sets[name]["measures"].items()}), flush=True)
    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    result = {"schema": "vsps.an1_stage1.v1", "status": "EXPLORATORY: stage 1 of A-N1 (DESIGN.md, STAGE1_PLAN.md)",
              "started_utc": t0, "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "code_at_head": head, "measures_py_sha256": g.sha256_file(HERE),
              "score_g2b_sha256": g.sha256_file(ROOT / "scripts/g2b/score_g2b.py"),
              "prereg_sha256": g.sha256_file(g.PREREG),
              "selfcheck_sha256": g.sha256_file(ROOT / "data/results/g2b/selfcheck.json"),
              "settings_from_prereg": {"n_boot": nb, "ci": [lo, hi], "tp_floor": floor,
                                       "n_random_subsets": dc["n_random_subsets"]["value"],
                                       **dc["set_by_this_registration"]},
              "system_files": inputs, "sets": sets, "choice": choose(sets)}
    out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    Path(str(out) + ".sha256").write_text(f"{g.sha256_file(out)}  {out.name}\n", encoding="utf-8")
    print(json.dumps(result["choice"]))
    return 0


# ------------------------------------------------------------------------------------------------ self-test
def brute_bpref(tp: int, fp: int, R: int, N: int) -> float:
    """bpref of one image averaged over every order of TP positives and FP negatives (trec_eval min(R, N) form)."""
    vals = []
    for negpos in itertools.combinations(range(tp + fp), fp):
        above = [sum(q < p for q in negpos) for p in range(tp + fp) if p not in negpos]
        vals.append(sum(1 - (min(a, R) / min(R, N) if N else 0) for a in above) / R)
    return float(np.mean(vals))


def selftest() -> int:
    one, i0 = np.ones((1, 1)), np.arange(1)
    cs = condensed(judged_rows([{"a", "b", "c"}], [[{"a"}]], [{"c"}]), i0, one)
    assert cs["P"][0] == 0.5 and cs["R"][0] == 1.0, cs  # the unjudged b is dropped
    assert abs(g.scores(g.rows([{"a", "b", "c"}], [[{"a"}]]), i0, one)["P"][0] - 1 / 3) < 1e-12
    cs = condensed(judged_rows([{"a", "b"}], [[{"a", "d"}]], [set()]), i0, one)
    assert cs["P"][0] == 1.0 and abs(cs["F"][0] - 2 * 0.5 / 1.5) < 1e-12  # D1: no negatives, P^c = 1
    rng = np.random.default_rng(0)
    U = sorted("abcdefgh")
    ment = [set(rng.choice(U, rng.integers(0, 5), replace=False)) for _ in range(7)]
    gold = [[set(rng.choice(U, rng.integers(0, 4), replace=False)) for _ in range(7)]]
    W = rng.multinomial(7, np.full(7, 1 / 7), size=5).astype(float)
    x = condensed(judged_rows(ment, gold, [set(U) - G for G in gold[0]]), np.arange(7), W)
    y = g.scores(g.rows(ment, gold), np.arange(7), W)
    assert all(np.allclose(x[k], y[k], equal_nan=True) for k in ("P", "R", "F", "M"))  # D3 identity
    for tp, fp, R, N in ((2, 0, 2, 10), (1, 0, 2, 10), (2, 1, 2, 10), (2, 4, 2, 10), (3, 1, 3, 1), (2, 3, 4, 5),
                         (1, 6, 3, 9), (2, 0, 3, 0)):
        G, Ns = {f"p{k}" for k in range(R)}, {f"n{k}" for k in range(N)}
        m = {f"p{k}" for k in range(tp)} | {f"n{k}" for k in range(fp)}
        got = float(bpref_rows([m], [[G]], [Ns])["b"][0, 0])
        assert abs(got - brute_bpref(tp, fp, R, N)) < 1e-12, (tp, fp, R, N, got)
    assert bpref_rows([{"p0", "p1", "n0"}], [[{"p0", "p1"}]], [{f"n{k}" for k in range(10)}])["b"][0, 0] == 0.75
    assert bpref_rows([{"a", "b"}], [[{"a", "c"}]], [set()])["b"][0, 0] == 0.5  # N' = 0: bpref = recall
    br = bpref(bpref_rows([{"a"}, {"z"}], [[{"a"}, set()]], [{"b"}, {"b"}]), np.arange(2), np.ones((1, 2)))
    assert br["F"][0] == 1.0 and br["M"][0] == 1.0  # the image without positives is excluded (D5)
    toy = {d: {"measures": {"cF1": {"rho": [r, [0.0, h]]}, "bpref": {"rho": [b, [0.0, 2.0]]}}}
           for d, r, h, b in (("A", 0.3, 0.42, 0.9), ("B", 0.5, 0.61, 1.2), ("C", 0.4, 0.5, 0.95))}
    c = choose(toy)
    assert c["primary"] == "cF1" and not c["kill"] and abs(c["theta"] - 0.65) < 1e-12, c
    toy["B"]["measures"]["cF1"]["rho"][0] = 1.1
    toy["C"]["measures"]["cF1"]["rho"][0] = 1.0
    assert choose(toy)["kill"] and choose(toy)["primary"] == "cF1"  # larger minimum shrink, but <= 0 on 2 sets
    tie = {d: {"measures": {"cF1": {"rho": [0.5, [0.0, 0.6]]}, "bpref": {"rho": [r, [0.0, 0.6]]}}}
           for d, r in (("A", 0.48), ("B", 0.47), ("C", 0.46))}
    assert choose(tie)["primary"] == "cF1"  # bpref leads by less than TIE
    print("selftest ok")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)
    sub.add_parser("selftest")
    s1 = sub.add_parser("stage1")
    s1.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    sys.exit(selftest() if a.mode == "selftest" else stage1(a.out))


if __name__ == "__main__":
    main()
