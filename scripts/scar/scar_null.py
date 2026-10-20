#!/usr/bin/env python3
"""SCAR random-deletion null for Paper A. POST_HOC exploratory (PD-23 (d), PD-23b item 1); design in SCAR_DESIGN.md.

  selftest  synthetic data with known answers                                   -> selftest.json
  gate      pins every input by sha and reproduces committed slope cells through the reused score_g2b path;
            computes no intersection or null statistic                          -> gate.json
  run       refuses unless this script and SCAR_DESIGN.md equal their HEAD blobs -> scar_null_result.json

  OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 nice -n 15 python3 -B <this file> run
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts/g2b"))
import score_g2b as g  # noqa: E402

PD23 = ".session_backup/2026-10-13/decisions/PD-23.txt"
R, SEED = map(int, re.search(r"R = (\d+), numpy default_rng\((\d+)\)", (ROOT / PD23).read_text()).groups())
G2B_SETS, LEVELS = ("cv295", "uv231", "xm600"), ("refs1_randk", "refs_all")
OUTPUTS = ROOT / ".session_backup/2026-10-20/g2b_score/outputs"
SCORE = "data/results/g2b/g2b_score.json"
PRECHECK = "data/results/g2b/g2b_score_record/precheck.json"
SELFCHECK = "data/results/g2b/selfcheck.json"
VERDICT75 = ".session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json"
EVAL75 = ".session_backup/2026-10-14/r12_verify/evaluate_xm3600_predictions.py"
V75_KEY = "matcher_v2_tone_normalised.n1_f1_vs_logM_slopes"
DESIGN = ROOT / "manuscript/prereg/2026-10-21_scar_null/SCAR_DESIGN.md"


def rel(p: Path) -> str:
    return str(Path(p).resolve().relative_to(ROOT))


def dig(d: dict, key: str):
    for k in key.split("."):
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d


def write(name: str, obj: dict) -> None:
    out = ROOT / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": rel(out), "sha256": g.sha256_file(out)}))


# ------------------------------------------------------------------------------------------------ core
def slope(ments: list[list[set]], golds: list[list[set]], idx: np.ndarray, floor: float) -> float:
    """Registered statistic: score_g2b.stat_slope over the ladder; F is the mean over the gold subsets."""
    one = np.ones((1, len(idx)))
    return float(g.stat_slope([g.scores(g.rows(m, golds), idx, one) for m in ments], floor)[0])


def intersect(golds: list[list[set]], comp: list[set]) -> list[list[set]]:
    return [[s & c for s, c in zip(gs, comp)] for gs in golds]


def null_slopes(st: dict, level: str, rng: np.random.Generator, n_rep: int, floor: float) -> np.ndarray:
    """One permutation per (replicate, image) of the image's sorted complete classes; registered subset s keeps
    the first k_i^(s). The gold is built once per replicate and shared by every ladder system."""
    comp = [sorted(c) for c in st["comp"]]
    ks = [[len(x) for x in gs] for gs in intersect(st["golds"][level], st["comp"])]
    out = np.empty(n_rep)
    for r in range(n_rep):
        perms = [[c[j] for j in rng.permutation(len(c))] for c in comp]
        out[r] = slope(st["ments"], [[set(p[:k]) for p, k in zip(perms, kk)] for kk in ks], st["idx"], floor)
    return out


def summarise(obs: float, null: np.ndarray, lo_q: float, hi_q: float) -> dict:
    return {"observed_intersection_slope": obs, "null_mean": float(null.mean()), "null_percentiles": [lo_q, hi_q],
            "null_lo": float(np.percentile(null, lo_q)), "null_hi": float(np.percentile(null, hi_q)),
            "share_same_sign": float(np.mean(np.sign(null) == np.sign(obs))),
            "n_finite": int(np.isfinite(null).sum())}


# ------------------------------------------------------------------------------------------------ inputs
def pins(reg: dict) -> tuple[dict, list[str]]:
    rec, bad = {}, []

    def pin(path: str, want: str | None, src: str, tracked: bool = False) -> None:
        got = g.sha256_file(ROOT / path)
        blob = g.git_blob_sha(path) if tracked else None
        rec[path] = {"sha256": got, "expected_from": src, **({"head_blob_sha256": blob} if tracked else {})}
        if (want is not None and got != want) or (tracked and blob != got):
            bad.append(path)

    score = g.jload(ROOT / SCORE)
    for p in (SCORE, PRECHECK, SELFCHECK):
        pin(p, None, "HEAD blob", tracked=True)
    pin(SCORE, (ROOT / (SCORE + ".sha256")).read_text().split()[0], SCORE + ".sha256", tracked=True)
    pin("scripts/g2b/score_g2b.py", score["scorer_sha256"], SCORE + ":scorer_sha256", tracked=True)
    pin(rel(g.PREREG), score["prereg_sha256"], SCORE + ":prereg_sha256", tracked=True)
    frozen = g.check_pins(reg)
    bad += frozen
    for f in reg["frozen_files"]["instruments"] + reg["frozen_files"]["data"]:
        rec.setdefault(f["path"], {"sha256": f["sha256"], "expected_from": "prereg frozen_files (score_g2b.check_pins)"})
    pre = g.jload(ROOT / PRECHECK)
    runs = pre["runs"]
    if not (pre["checked_ok"] == pre["registered_runs"] == len(runs) == len(
            [f for f in OUTPUTS.iterdir() if not f.name.endswith(".sha256")])) or pre["problems"]:
        bad.append(PRECHECK + " (run count)")
    for rid in sorted(runs):
        pin(rel(OUTPUTS / runs[rid]["file"]), runs[rid]["sha256"], f"{PRECHECK}:runs.{rid}.sha256")
    pin(VERDICT75, g.jload(ROOT / SELFCHECK)["references_sha256"][VERDICT75], f"{SELFCHECK}:references_sha256")
    landed = g.jload(ROOT / VERDICT75)["landed_result_files"]
    for f in sorted((ROOT / "data/results/xm3600").glob("*.preds.json")):
        pin(rel(f), landed[f.name]["sha256"], f"{VERDICT75}:landed_result_files.{f.name}.sha256")
    pin(EVAL75, None, "no committed pin; recorded here (source of the §7.5 randk constants)")
    pin(PD23, None, "no committed pin; recorded here (source of R and the seed)")
    return rec, bad


def s75_randk(refs: list[list[set]]) -> list[list[set]]:
    """§7.5's registered refs1_randk choice (evaluate_xm3600_predictions.py: rng_rk, randk_golds_v2)."""
    src = (ROOT / EVAL75).read_text(encoding="utf-8")
    nsub = int(re.search(r"^NSUB_RANDK = (\d+)", src, re.M).group(1))
    rng = np.random.default_rng(int(re.search(r"^SEED_MAIN = (\d+)", src, re.M).group(1)))
    return [[r[int(rng.integers(len(r)))] for r in refs] for _ in range(nsub)]


def build_sets(reg: dict) -> list[dict]:
    lang = {r["run_id"]: ("en" if r["prompt_mode"].endswith("_en") else "vi") for r in reg["runs"]}
    n_ids = {d: reg["datasets"][d]["n_images"] for d in G2B_SETS}
    caps, excluded = g.load_runs(reg, OUTPUTS, n_ids)
    if excluded:
        raise SystemExit(f"runs excluded by score_g2b.load_runs: {excluded}")
    score = g.jload(ROOT / SCORE)
    out = []
    for name in G2B_SETS:
        ds = g.Dataset(reg, name, {k: v for k, v in caps.items() if k.startswith(f"g2b_q3_{name}-")}, lang)
        lx = next(iter(ds.lex))  # primary lexicon
        lad = reg["families"][name]["LADDER"]
        lex = ds.lex[lx]
        comp = [set(c) for c in lex["complete"]] if "complete" in lex else \
            [{c for c, v in s.items() if v == "present"} for s in lex["oiv7"]]
        key = f"datasets.{name}.descriptive.golds.{{}}.slope_F1_per_lnM.0"
        out.append({"name": name, "lexicon": lx, "systems": lad, "ids": ds.ids, "comp": comp,
                    "golds": {L: ds.variants[lx][L] for L in LEVELS}, "ments": [ds.ment(s, lx) for s in lad],
                    "idx": ds.clean_index(lad, True), "ds": ds,
                    "registered": {G: {"value": dig(score, key.format(G)), "source": f"{SCORE}:{key.format(G)}"}
                                   for G in (*LEVELS, ds.complete)}})
    ctx = g.xm3600_context()
    lex = ctx["lexicons"]["objects_in"]
    files = sorted((ROOT / "data/results/xm3600").glob("*.preds.json"))
    ver = g.jload(ROOT / VERDICT75)
    out.append({"name": "s75", "lexicon": "objects_in", "systems": [rel(f) for f in files], "ids": ctx["ids"],
                "comp": [{c for c, v in s.items() if v == "present"} for s in lex["oiv7"]],
                "golds": {"refs1_randk": s75_randk(lex["refs"]), "refs_all": g.gold_variants(lex, None)["refs_all"]},
                "ments": [g.mentions(g.read_captions(f), ctx["ids"], g.MATCH["objects_in"]["vi"]) for f in files],
                "idx": np.arange(len(ctx["ids"])), "lex": lex,
                "registered": {G: {"value": dig(ver, f"{V75_KEY}.{G}.slope_F1_per_logM"),
                                   "source": f"{VERDICT75}:{V75_KEY}.{G}.slope_F1_per_logM", "decimals": 4}
                               for G in (*LEVELS, "oiv7_verified")}})
    return out


def reproduce(st: dict, floor: float) -> list[dict]:
    """Registered gold cells only (no intersection, no null)."""
    cells = []
    for G, reg_v in st["registered"].items():
        t0 = time.perf_counter()
        if st["name"] == "s75":
            sl = [g.scores(g.oiv7_rows(m, st["lex"]), st["idx"], np.ones((1, len(st["idx"])))) for m in st["ments"]] \
                if G == "oiv7_verified" else None
            mine = float(g.stat_slope(sl, floor)[0]) if sl else slope(st["ments"], st["golds"][G], st["idx"], floor)
        else:
            ds = st["ds"]
            one = np.ones((1, len(st["idx"])))
            mine = float(g.stat_slope([g.scores(ds.rows(s, G, st["lexicon"]), st["idx"], one)
                                       for s in st["systems"]], floor)[0])
        dp = reg_v.get("decimals")
        ok = mine == reg_v["value"] if dp is None else abs(round(mine, dp) - reg_v["value"]) <= 0.5 * 10 ** -dp + 1e-9
        print(f"{st['name']} {G}: {time.perf_counter() - t0:.2f}s", file=sys.stderr)
        cells.append({"set": st["name"], "gold": G, "reference": reg_v["value"], "reference_source": reg_v["source"],
                      "reproduced": mine, "match": "exact" if dp is None else f"{dp} dp", "ok": bool(ok)})
    return cells


def header(reg: dict) -> tuple[dict, dict, list[dict]]:
    rec, bad = pins(reg)
    if bad:
        raise SystemExit(f"pins differ: {bad}")
    sets = build_sets(reg)
    s75, xm = sets[3], sets[2]
    if s75["ids"] != xm["ids"]:
        raise SystemExit("§7.5 ids differ from G2-B xm600 ids")
    dc = reg["design_constants"]
    floor = dc["tp_floor"]["value"]
    cells = [c for st in sets for c in reproduce(st, floor)]
    info = {"pins": rec, "sets": {st["name"]: {"lexicon": st["lexicon"], "systems": st["systems"],
                                               "n_ids": len(st["ids"]), "n_images_scored": int(len(st["idx"]))}
                                  for st in sets},
            "reproduced_cells": cells, "all_cells_ok": all(c["ok"] for c in cells)}
    return info, {"floor": floor, "lo_q": dc["ci_lo_percentile"]["value"], "hi_q": dc["ci_hi_percentile"]["value"]}, sets


# ------------------------------------------------------------------------------------------------ modes
def provenance() -> dict:
    return {"script_sha256": g.sha256_file(Path(__file__)), "design_sha256": g.sha256_file(DESIGN)}


def gate() -> int:
    info, _, _ = header(g.jload(g.PREREG))
    write("manuscript/prereg/2026-10-21_scar_null/gate.json", {"schema": "vsps.scar_null.gate.v1", "status": "POST_HOC exploratory (PD-23 (d), PD-23b)",
                        **provenance(),
                        "statistics_computed": "registered gold cells only; no intersection or null slope", **info})
    return 0 if info["all_cells_ok"] else 1


def committed(path: Path) -> bool:
    return g.git_blob_sha(rel(path)) == g.sha256_file(path)


def run() -> int:
    if not (committed(Path(__file__)) and committed(DESIGN)):
        raise SystemExit("refused: scar_null.py and SCAR_DESIGN.md must equal their HEAD blobs")
    if (ROOT / "data/results/scar/scar_null_result.json").exists():
        raise SystemExit("refused: scar_null_result.json exists (one pass only)")
    info, c, sets = header(g.jload(g.PREREG))
    if not info["all_cells_ok"]:
        raise SystemExit("refused: registered cells do not reproduce")
    rng = np.random.default_rng(SEED)
    res = {}
    for st in sets:
        for L in LEVELS:
            inter = intersect(st["golds"][L], st["comp"])
            null = null_slopes(st, L, rng, R, c["floor"])
            res[f"{st['name']}/{L}"] = {
                "registered_slope": st["registered"][L], **summarise(slope(st["ments"], inter, st["idx"], c["floor"]),
                                                                       null, c["lo_q"], c["hi_q"]),
                "n_images": int(len(st["idx"])),
                "sum_k_scored_mean_over_subsets": float(np.mean([sum(len(gs[i]) for i in st["idx"]) for gs in inter])),
                "sum_complete_scored": int(sum(len(st["comp"][i]) for i in st["idx"])), "null_slopes": null.tolist()}
    write("data/results/scar/scar_null_result.json", {"schema": "vsps.scar_null.v1", "status": "POST_HOC exploratory; no verdict",
                                    **provenance(), "R": R, "seed": SEED, "R_seed_source": PD23,
                                    "results": res, **info})
    return 0


def selftest() -> int:
    checks = {}
    # stat_slope reused: F = 0.1 * ln M + c  ->  slope of 100 F on ln M = 10
    x = np.log(np.array([1.0, 2.0, 4.0, 8.0]))
    checks["stat_slope_known_10"] = bool(np.isclose(g.stat_slope(
        [{"M": np.array([np.exp(v)]), "F": np.array([0.1 * v + 0.2])} for v in x], 1e-9)[0], 10.0))
    # synthetic set: 6 images, 3 systems with growing mentions, 2 registered subsets
    comp = [{"a", "b", "c"}, {"b", "d"}, set(), {"a", "e", "f", "g"}, {"c"}, {"a", "b"}]
    vocab = sorted(set().union(*comp) | {"x", "y"})
    ments = [[set(vocab[(i + j) % len(vocab)] for j in range(n)) for i in range(6)] for n in (1, 3, 5)]
    full = [[set(c) for c in comp]] * 2
    part = [[{"a"}, {"b"}, set(), {"e", "zz"}, set(), {"a", "b"}], [{"b", "c"}, set(), {"q"}, {"a"}, {"c"}, set()]]
    idx = np.arange(6)
    st = {"comp": comp, "ments": ments, "idx": idx, "golds": {"full": full, "part": part}}
    obs_full = slope(ments, intersect(full, comp), idx, 1e-9)
    nf = null_slopes(st, "full", np.random.default_rng(0), 50, 1e-9)
    checks["k_eq_complete_null_equals_observed"] = bool(np.all(nf == obs_full))
    dc = g.jload(g.PREREG)["design_constants"]
    s = summarise(obs_full, nf, dc["ci_lo_percentile"]["value"], dc["ci_hi_percentile"]["value"])
    checks["k_eq_complete_percentiles_and_share"] = s["null_lo"] == s["null_hi"] == obs_full and \
        s["share_same_sign"] == 1.0
    # replicate 0 rebuilt by hand from the same stream: shared gold, nested prefixes, k from the registered subsets
    rng = np.random.default_rng(0)
    perms = [[sorted(c)[j] for j in rng.permutation(len(c))] for c in comp]
    ks = [[len(a & b) for a, b in zip(gs, comp)] for gs in part]
    hand = [[set(p[:k]) for p, k in zip(perms, kk)] for kk in ks]
    checks["k_from_registered_subsets"] = ks == [[1, 1, 0, 1, 0, 2], [2, 0, 0, 1, 1, 0]]
    checks["k0_image_empty_gold"] = all(hand[s][2] == set() for s in range(2))
    checks["nested_prefixes"] = all(hand[0][i] <= hand[1][i] or hand[1][i] <= hand[0][i] for i in range(6))
    checks["replicate0_matches_hand_rebuild"] = null_slopes(st, "part", np.random.default_rng(0), 1, 1e-9)[0] == \
        slope(ments, hand, idx, 1e-9)
    a = null_slopes(st, "part", np.random.default_rng(0), 30, 1e-9)
    checks["deterministic"] = bool(np.array_equal(a, null_slopes(st, "part", np.random.default_rng(0), 30, 1e-9)))
    r2 = np.random.default_rng(0)
    null_slopes(st, "full", r2, 5, 1e-9)
    checks["order_changes_draws"] = not np.array_equal(a, null_slopes(st, "part", r2, 30, 1e-9))
    # uniformity: |C| = 4, k = 2 -> each class kept with probability 1/2
    rng = np.random.default_rng(0)
    kept = np.array([[c in set(np.array(sorted("abcd"))[rng.permutation(4)][:2]) for c in "abcd"]
                     for _ in range(4000)])
    checks["uniform_inclusion_0.5"] = bool(np.all(np.abs(kept.mean(0) - 0.5) < 0.03))
    checks = {k: bool(v) for k, v in checks.items()}
    write("manuscript/prereg/2026-10-21_scar_null/selftest.json", {"schema": "vsps.scar_null.selftest.v1", **provenance(), "checks": checks, "pass": all(checks.values()),
                            "null_part_first5": a[:5].tolist()})
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    modes = {"selftest": selftest, "gate": gate, "run": run}
    if len(sys.argv) != 2 or sys.argv[1] not in modes:
        raise SystemExit(f"usage: {Path(__file__).name} {{{'|'.join(modes)}}}")
    sys.exit(modes[sys.argv[1]]())
