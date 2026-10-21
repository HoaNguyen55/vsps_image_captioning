#!/usr/bin/env python3
"""N-F1 bracket for Paper A: the XM3600 OIV7 rung re-scored with unverified mapped mentions counted as errors
(P_lower) and as correct (P_upper). POST_HOC exploratory (PD-28 item 1); design in DESIGN.md next to gate.json.

  --selftest  synthetic data with known answers                                       -> selftest.json
  gate        reproduces the registered F1_pos slopes (point and CI) through the same function `run` uses, in
              precision mode "registered" only; computes no bracket statistic                -> gate.json
  run         refuses unless this script and DESIGN.md equal their HEAD blobs; one pass       -> bracket_result.json

Every mode first refuses unless every input equals its recorded sha256 (PINS).
  OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 nice -n 15 python3 -B scripts/n_f1/bracket.py run
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PRE = "manuscript/prereg/2026-10-21_n_f1_bracket"
DESIGN = ROOT / PRE / "DESIGN.md"
RESULT = "data/results/n_f1/bracket_result.json"
V3 = ".session_backup/2026-10-14/r12_verify/evaluate_xm3600_predictions_v3.py"
VERDICT = ".session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json"
VERDICT_V2 = ".session_backup/2026-10-14/r12_verify/xm3600_full_verdict_v2.json"
SCORE = "data/results/g2b/g2b_score.json"
OUT_G2B = ".session_backup/2026-10-20/g2b_score/outputs"
S75_KEY = "matcher_v2_tone_normalised.n1_f1_vs_logM_slopes.oiv7_verified"
MODES = ("registered", "lower", "upper")
SENTENCES = {  # PD-28 item (1), fixed before the run
    "i": "it stays positive when unverifiable mentions count as errors (post hoc)",
    "ii": "it is positive only when unverifiable mentions are excluded; counting them as errors removes the positive "
          "slope (post hoc)"}

# path -> sha256; the source of each value is listed in DESIGN.md (Inputs)
PINS = dict(line.split()[::-1] for line in """
fde27b7e527eca7db740eb983f22cd269d6549de82f02fb48ac51525b2bf4d75 .session_backup/2026-10-13/decisions/PD-28.txt
66c665c7a71d3b97abbf89fd5bf13871910449ad1c053ff5fb0b18663e3e7ae5 scripts/g2b/score_g2b.py
c506bc777b483f5097561d2894a535f33e5e9e27745af07c0f979fbac5560055 manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json
68be2b7a0904027ccb6723129fe86cc10c4976a9e59fbc7862251fe715090824 data/results/g2b/g2b_score.json
02bdca27949e781ab90376ce97e25555df35d140369f967ae6b7feef63b9f78e data/results/g2b/g2b_score_record/precheck.json
82b6ef5fdb9bc98a34e07b9a68e99b1403277d275285fe6df54864d319f57e5e .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-short-T0.preds.json
a66647d12140858e8c013fdce6133949c4b97179d91acc92c413608bf0a560df .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-detailed-T0.preds.json
522819dfe54dc8a9e191b9ddf88c0df6edb3a1bda6e9a1c4932533c273e1ae76 .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-short-T05.preds.json
3e6189d627affaec4e327b1eb3ac1a55a3b76cbc8ae5001dc3c63de9c6baa9ee .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-detailed-T05.preds.json
71b168e7909913fe2f95c63727be1f9a664dea5b8271a82357aae15d61f698fc .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-short-T08.preds.json
944668eb32fb4a76209837f394bf6cd62a3245d8ac467e715105b3953dd2e751 .session_backup/2026-10-20/g2b_score/outputs/g2b_q3_xm600-detailed-T08.preds.json
24356632c1c9b8023d8319de5ebc30b15c517f7f5b3ad7d519eea9c73d2c626d .session_backup/2026-10-14/r12_verify/evaluate_xm3600_predictions_v3.py
5d0134bfded091d47153226c427ceb8ee29fe8b2a698daf8d533d8365fb5dc32 manuscript/prereg/2026-10-14_xm3600_predictions.json
0b2b3aa5e1a3f532e62e836c2b8011a46c811f7c01aaed4711aa9eae9a133dbf .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json
c88d503f8089ba97ac17f2d918cca8996565d6ced8411041f3c9d944ca14ac54 .session_backup/2026-10-14/r12_verify/xm3600_full_verdict_v2.json
e29f0a4f8078e72d334f2b421b9e703bd788606ba02c96f7232fe8bc96bc5acc data/results/g2b/selfcheck.json
1f3573324772c67de3eebcdef326f84a39ecbe7fd705ceb5dd4e6863a0d73d4c data/results/xm3600/xm3600_zeroshot-short.preds.json
47db3b9d279508e89f0332482c3e268a119186af9e0cbf6426cc85ce1a52a32f data/results/xm3600/xm3600_zeroshot-detailed.preds.json
1150a046e63470c09268f0045b7b4976b6cad2a571453873277a9fc82fd2aad9 data/results/xm3600/xm3600_p1_s43-short.preds.json
296a26bfe17635afe61ab28ba16fae40714577b4981b96786cc021700410c7e2 data/results/xm3600/xm3600_p1_s43-detailed.preds.json
426c2d8140a912d17d296dddfcaa807aa93b5e673d3ee8fd5dea6c44885a2943 data/results/xm3600/xm3600_fuse2_s42-short.preds.json
b941181c7b118c73fdac8f3f66797beee9d07891096a98927b1aa30f36b31203 data/results/xm3600/xm3600_fuse2_s42-detailed.preds.json
6b711280d70b780d596414896d832738da58f1b079015dee888605d1ba350adc scripts/object_prf.py
e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3 rescap/chair.py
a9253060131aacfca8eaab9a4b2c473c487db96a7c1222f0b8e31f9f61b24003 rescap/svp/matching.py
fbc945f2247418275144ac75b893f7c51f8951b9ea42018680d433775dd79eb9 rescap/vi/lexicon.py
242fc46f68ecb06c8eefde23350481d99e60566b3da64ab90cfa79db38fd3875 rescap/vi/color.py
9a79403f4fc38609282d40082ab7f878133edca8aff9e0dc2462db467b7193f0 scripts/xm3600_oiv7.py
d11db7e192f689980bb2b2bb717d852d9aa339ad857ce9411fe7bdd6fe416070 scripts/score_coco_probe.py
01f172002a607ba9ee55bccb332439f10650832cae1f64a9b74b35c48cd9c231 scripts/clean_supervision.py
33793de01b4f2790964342b1af2d4c2de18d793ae4693608283992475ed62ce7 rescap/vlm/mock.py
0a613214f95605ff137879f70cb84f8160172c28a650317766ac4a1d9c3b72e8 data/datasets/xm3600/test_data.json
bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2 data/xm3600/oiv7_labels.json
84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3 data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv
""".strip().splitlines())


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_pins() -> None:
    """Runs before any project module is imported, so a changed instrument never executes."""
    bad = [p for p, want in PINS.items() if not (ROOT / p).exists() or sha(ROOT / p) != want]
    if bad:
        raise SystemExit(f"refused: inputs differ from their recorded sha256: {bad}")


def load_modules():
    global g, v
    sys.path.insert(0, str(ROOT / "scripts/g2b"))
    import score_g2b as g  # noqa: E402
    spec = importlib.util.spec_from_file_location("evaluate_xm3600_predictions_v3", ROOT / V3)
    v = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v)  # module level defines constants and functions only; evaluate_suite is never called
    bad = g.check_pins(g.jload(g.PREREG))
    if bad:
        raise SystemExit(f"refused: G2-B frozen files differ from the prereg: {bad}")


def dig(d, key: str):
    for k in key.split("."):
        d = d[k]
    return d


def write(rel: str, obj: dict) -> None:
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": rel, "sha256": sha(out)}))


def provenance() -> dict:
    return {"script_sha256": sha(Path(__file__)), "design_sha256": sha(DESIGN) if DESIGN.exists() else None}


# ------------------------------------------------------------------------------------------------ precision modes
def s75_cols(a: np.ndarray, mode: str) -> np.ndarray:
    """caption_rows columns: 0 mapped, 1 verified-present, 2 verified-absent (5, 6 feed recall and stay unchanged).
    lower: absent := mapped - present, so vp = present / mapped. upper: present := mapped - absent, so
    vp = (present + unverified) / mapped."""
    a = a.copy()
    if mode == "lower":
        a[:, 2] = a[:, 0] - a[:, 1]
    elif mode == "upper":
        a[:, 1] = a[:, 0] - a[:, 2]
    return a


def g2b_scores(r: dict, mapped: np.ndarray, idx: np.ndarray, W: np.ndarray, mode: str) -> dict:
    """score_g2b.scores on oiv7_rows. lower: am := mapped - pm (P = pm / mapped; R = pm / pos unchanged).
    upper: P from pm' = mapped - am, R from the registered rows, F by the expression scores uses."""
    if mode == "registered":
        return g.scores(r, idx, W)
    if mode == "lower":
        return g.scores({**r, "am": mapped - r["pm"]}, idx, W)
    base, up = g.scores(r, idx, W), g.scores({**r, "pm": mapped - r["am"]}, idx, W)
    P, R = up["P"], base["R"]
    return {"P": P, "R": R, "F": g.div(2 * P * R, P + R, 0.0), "M": base["M"]}


# ------------------------------------------------------------------------------------------------ sets
def s75_context() -> dict:
    """§7.5 six systems, rebuilt as evaluate_suite builds them (v3 functions, v2 tone-normalised matcher)."""
    vi = v.load_caption_json(ROOT / "data/datasets/xm3600/test_data.json")
    ids = sorted(vi)
    n = len(ids)
    labels = {k: x for k, x in g.jload(ROOT / "data/xm3600/oiv7_labels.json").items() if not k.startswith("_")}
    vmap = v.xo.resolve_map(ROOT / "data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv")
    st, mapped = v.xo.statuses(vmap, labels), set(vmap)
    refs = [[set(v.objects_in(c, raw_tone=False)) for c in vi[i]] for i in ids]
    g_all = [set().union(*r) for r in refs]
    pos = [{c for c, s in st.get(i, {}).items() if s == "present"} for i in ids]
    idx_boot = np.random.default_rng(v.SEED_MAIN).integers(0, n, size=(v.B_PAIRED, n))
    rng_rk = np.random.default_rng(v.SEED_MAIN)
    randk = [[r[int(rng_rk.integers(len(r)))] for r in refs] for _ in range(v.NSUB_RANDK)]
    names = g.jload(v.PREREG_JSON)["systems_queued_in_58_z"]
    full = np.arange(n)[None]
    systems = {}
    for name in names:
        caps = v.load_preds_file(ROOT / f"data/results/xm3600/{name}.preds.json")
        ms = [set(v.objects_in(caps[i], raw_tone=False)) for i in ids]
        rows = [v.image_counts(m, gg, v._ancestors) for m, gg in zip(ms, g_all)]
        systems[name] = {
            "a": np.asarray([v.xo.caption_rows(ms[k], st.get(i, {}), g_all[k], mapped) for k, i in enumerate(ids)],
                            dtype=float),
            "pr": np.array([len(ms[k] & pos[k]) / len(pos[k]) if pos[k] else np.nan for k in range(n)], dtype=float),
            "M_pt": float(v.prf_draws_extended(rows, full)["M"][0]),
            "M_dr": v.prf_draws_extended(rows, idx_boot)["M"]}
    return {"name": "s75", "ids": ids, "idx_boot": idx_boot, "full": full, "systems": systems,
            "golds": {"refs1_randk": randk, "refs_all": [g_all], "oiv7_verified": [pos]}, "scored": np.arange(n)}


def s75_bracket(ctx: dict, mode: str) -> dict:
    """The registered N1 slope loop of evaluate_suite (point; B_MSTAR draws of idx_boot) with F1_pos from
    v3.oi_draws_extended on the mode's columns."""
    names = list(ctx["systems"])
    pts, drs = {}, {}
    for s in names:
        a, pr = s75_cols(ctx["systems"][s]["a"], mode), ctx["systems"][s]["pr"]
        p = v.oi_draws_extended(a, ctx["full"], pr)
        pts[s] = {k: float(p[k][0]) for k in ("P_pos", "R_pos", "F1_pos")}
        drs[s] = v.oi_draws_extended(a, ctx["idx_boot"], pr)["F1_pos"]
    lm = np.log(np.array([ctx["systems"][s]["M_pt"] for s in names], dtype=float))
    point = v.ols_slope(lm, np.array([pts[s]["F1_pos"] for s in names], dtype=float))
    bs = np.array([v.ols_slope(np.log(np.maximum(np.array([ctx["systems"][s]["M_dr"][b] for s in names],
                                                          dtype=float), v.EPS9)),
                               np.array([drs[s][b] for s in names], dtype=float)) for b in range(v.B_MSTAR)])
    return {"point": float(point), "point_4dp": round(float(point), 4), "ci95_2dp": v.ci_bounds(bs, 2),
            "ci95_raw": [float(np.nanpercentile(bs, v.PCT_LO)), float(np.nanpercentile(bs, v.PCT_HI))],
            "ci_finite": bool(np.all(np.isfinite(bs))), "B": v.B_MSTAR,
            "per_system": {s: {"P": pts[s]["P_pos"], "R": pts[s]["R_pos"], "F1": pts[s]["F1_pos"],
                               "M": ctx["systems"][s]["M_pt"]} for s in names}}


def g2b_context() -> dict:
    reg = g.jload(g.PREREG)
    runs = [r for r in reg["runs"] if r["dataset"] == "xm600"]
    caps, excluded = g.load_runs({**reg, "runs": runs}, ROOT / OUT_G2B, {"xm600": reg["datasets"]["xm600"]["n_images"]})
    if excluded:
        raise SystemExit(f"refused: runs excluded by score_g2b.load_runs: {excluded}")
    lang = {r["run_id"]: ("en" if r["prompt_mode"].endswith("_en") else "vi") for r in reg["runs"]}
    ds = g.Dataset(reg, "xm600", caps, lang)
    lx = next(iter(ds.lex))
    lad = reg["families"]["xm600"]["LADDER"]
    idx = ds.clean_index(lad, True)
    n = len(idx)
    dc = reg["design_constants"]
    W = np.random.default_rng(dc["set_by_this_registration"]["bootstrap_seed"]).multinomial(
        n, np.full(n, 1.0 / n), size=dc["n_boot"]["value"]).astype(float)
    mapped = ds.lex[lx]["mapped"]
    return {"name": "xm600", "ds": ds, "lx": lx, "systems": lad, "idx": idx, "W": W, "scored": idx,
            "floor": dc["tp_floor"]["value"], "lo_q": dc["ci_lo_percentile"]["value"],
            "hi_q": dc["ci_hi_percentile"]["value"], "ids": ds.ids,
            "rows": {s: ds.rows(s, "oiv7_verified", lx) for s in lad},
            "mapped": {s: np.array([len(m & mapped) for m in ds.ment(s, lx)], float) for s in lad},
            "golds": {G: ds.variants[lx][G] for G in ("refs1_randk", "refs_all")} | {
                "oiv7_verified": [[{c for c, x in s.items() if x == "present"} for s in ds.lex[lx]["oiv7"]]]}}


def g2b_bracket(ctx: dict, mode: str) -> dict:
    """slope[complete](LADDER) as eval_stat computes it (stat_slope over LADDER, registered W) in the given mode."""
    one = np.ones((1, len(ctx["idx"])))
    pts = [g2b_scores(ctx["rows"][s], ctx["mapped"][s], ctx["idx"], one, mode) for s in ctx["systems"]]
    reps = [g2b_scores(ctx["rows"][s], ctx["mapped"][s], ctx["idx"], ctx["W"], mode) for s in ctx["systems"]]
    rep = g.stat_slope(reps, ctx["floor"])
    ci = g.ci(rep, ctx["lo_q"], ctx["hi_q"])
    return {"point": float(g.stat_slope(pts, ctx["floor"])[0]), "ci95": ci, "ci95_raw": ci,
            "ci_finite": ci is not None, "B": int(ctx["W"].shape[0]),
            "per_system": {s: {k: float(100 * p[k][0]) for k in ("P", "R", "F")} | {"M": float(p["M"][0])}
                           for s, p in zip(ctx["systems"], pts)}}


# ------------------------------------------------------------------------------------------------ descriptives (run)
def gold_sizes(ctx: dict) -> dict:
    """Mean |G_i| over the scored images per rung; refs1_randk is the mean over its registered subsets."""
    idx = ctx["scored"]
    return {G: float(np.mean([np.mean([len(gs[i]) for i in idx]) for gs in golds])) for G, golds in ctx["golds"].items()}


def verifiable_shares(ctx: dict) -> dict:
    """100 * (verified-present + verified-absent) / mapped mentions, per system, with the set's bootstrap."""
    out = {}
    if ctx["name"] == "s75":
        for s, d in ctx["systems"].items():
            vs = v.oi_draws_extended(d["a"], ctx["full"], d["pr"])["verifiable_share"]
            out[s] = {"point": float(vs[0]),
                      "ci95_2dp_Bpaired": v.ci_bounds(v.oi_draws_extended(d["a"], ctx["idx_boot"], d["pr"])
                                                      ["verifiable_share"], 2)}
        return out
    one = np.ones((1, len(ctx["idx"])))
    for s in ctx["systems"]:
        r, m, i = ctx["rows"][s], ctx["mapped"][s], ctx["idx"]
        share = [g.div(100 * (W @ (r["pm"][i] + r["am"][i])), W @ m[i], np.nan) for W in (one, ctx["W"])]
        out[s] = {"point": float(share[0][0]), "ci95": g.ci(share[1], ctx["lo_q"], ctx["hi_q"])}
    return out


def outcome(b: dict) -> str:
    lo = b["ci95_raw"][0] if b["ci95_raw"] else None
    return "i" if b["ci_finite"] and lo is not None and np.isfinite(lo) and lo > 0 else "ii"


def assemble(pairs: list) -> dict:
    """The run's result body: all three modes per set, the outcome from the lower bound, descriptives."""
    sets = {}
    for ctx, fn in pairs:
        br = {m: fn(ctx, m) for m in MODES}
        sets[ctx["name"]] = {"n_images_scored": int(len(ctx["scored"])), "slopes": br,
                             "outcome_from_lower": outcome(br["lower"]),
                             "verifiable_share": verifiable_shares(ctx), "mean_gold_size": gold_sizes(ctx)}
    paper = "i" if all(x["outcome_from_lower"] == "i" for x in sets.values()) else "ii"
    return {"sets": sets, "outcome_paper": paper, "sentence_paper": SENTENCES[paper],
            "sentence_by_set": {k: SENTENCES[x["outcome_from_lower"]] for k, x in sets.items()}}


# ------------------------------------------------------------------------------------------------ modes
def gate_cells() -> list[dict]:
    """Registered F1_pos slope cells only, through s75_bracket / g2b_bracket in mode "registered"."""
    cells = []
    ctx = s75_context()
    b = s75_bracket(ctx, "registered")
    ver = {f: dig(g.jload(ROOT / f), S75_KEY) for f in (VERDICT, VERDICT_V2)}
    for f, ref in ver.items():
        cells.append({"set": "s75", "stat": "slope_F1_per_logM (oiv7_verified, F1_pos)", "reference": ref[
            "slope_F1_per_logM"], "reference_source": f"{f}:{S75_KEY}.slope_F1_per_logM",
                      "reproduced_full_precision": b["point"], "reproduced_at_committed_dp": b["point_4dp"],
                      "abs_diff_at_committed_dp": abs(b["point_4dp"] - ref["slope_F1_per_logM"]),
                      "abs_diff_full_precision": abs(b["point"] - ref["slope_F1_per_logM"]), "committed_dp": 4})
        cells.append({"set": "s75", "stat": "slope_ci95_b500", "reference": ref["slope_ci95_b500"],
                      "reference_source": f"{f}:{S75_KEY}.slope_ci95_b500", "reproduced_at_committed_dp": b["ci95_2dp"],
                      "reproduced_full_precision": b["ci95_raw"],
                      "abs_diff_at_committed_dp": max(abs(x - y) for x, y in zip(b["ci95_2dp"], ref["slope_ci95_b500"])),
                      "committed_dp": 2})
    vsys = g.jload(ROOT / VERDICT)["matcher_v2_tone_normalised"]["systems"]
    for s, p in b["per_system"].items():
        ref = vsys[s]["oiv7_verified"]["F1_pos"]
        cells.append({"set": "s75", "stat": f"F1_pos[{s}]", "reference": ref,
                      "reference_source": f"{VERDICT}:matcher_v2_tone_normalised.systems.{s}.oiv7_verified.F1_pos",
                      "reproduced_full_precision": p["F1"], "reproduced_at_committed_dp": round(p["F1"], 4),
                      "abs_diff_at_committed_dp": abs(round(p["F1"], 4) - ref), "committed_dp": 4})
    gbar = g.jload(ROOT / VERDICT)["dataset_and_gold_density_verification"]
    sizes = gold_sizes(ctx)
    for G, key in (("refs_all", "refs_all.Gbar_all_600"), ("oiv7_verified", "oiv7_verified.Gbar_pos_all_600")):
        ref = dig(gbar, f"observed_gold_density_Gbar_eval600.{key}")
        cells.append({"set": "s75", "stat": f"mean gold size [{G}]", "reference": ref,
                      "reference_source": f"{VERDICT}:dataset_and_gold_density_verification.observed_gold_density_Gbar_eval600.{key}",
                      "reproduced_full_precision": sizes[G], "reproduced_at_committed_dp": round(sizes[G], 4),
                      "abs_diff_at_committed_dp": abs(round(sizes[G], 4) - ref), "committed_dp": 4})
    ctx = g2b_context()
    b = g2b_bracket(ctx, "registered")
    sc = g.jload(ROOT / SCORE)["datasets"]["xm600"]
    e2 = sc["predictions"]["G2B-E2"]
    if e2["n_images"] != len(ctx["idx"]) or e2["parts"][0]["stat"] != "slope[complete](LADDER)":
        raise SystemExit("G2B-E2 analysis set differs")
    desc = sc["descriptive"]["golds"]["oiv7_verified"]
    for key, ref_pt, ref_ci in (("datasets.xm600.predictions.G2B-E2.parts.0", e2["parts"][0]["point"],
                                 e2["parts"][0]["ci95"]),
                                ("datasets.xm600.descriptive.golds.oiv7_verified.slope_F1_per_lnM",
                                 desc["slope_F1_per_lnM"][0], desc["slope_F1_per_lnM"][1])):
        cells.append({"set": "xm600", "stat": "slope[complete](LADDER) point", "reference": ref_pt,
                      "reference_source": f"{SCORE}:{key}", "reproduced_full_precision": b["point"],
                      "abs_diff_full_precision": abs(b["point"] - ref_pt), "committed_dp": None})
        cells.append({"set": "xm600", "stat": "slope[complete](LADDER) ci95", "reference": ref_ci,
                      "reference_source": f"{SCORE}:{key}", "reproduced_full_precision": b["ci95"],
                      "abs_diff_full_precision": max(abs(x - y) for x, y in zip(b["ci95"], ref_ci)),
                      "committed_dp": None})
    for s, p in b["per_system"].items():
        ref = desc["systems"][s]["F"][0]
        cells.append({"set": "xm600", "stat": f"100*F[{s}]", "reference": ref,
                      "reference_source": f"{SCORE}:datasets.xm600.descriptive.golds.oiv7_verified.systems.{s}.F.0",
                      "reproduced_full_precision": p["F"], "abs_diff_full_precision": abs(p["F"] - ref),
                      "committed_dp": None})
    for c in cells:
        d = c.get("abs_diff_at_committed_dp", c.get("abs_diff_full_precision"))
        c["ok"] = d == 0 if c["committed_dp"] else d <= 1e-12
    return cells


def gate() -> int:
    cells = gate_cells()
    by_set = {s: max(c.get("abs_diff_at_committed_dp", c.get("abs_diff_full_precision")) for c in cells
                     if c["set"] == s) for s in ("s75", "xm600")}
    write(f"{PRE}/gate.json", {
        "schema": "vsps.n_f1_bracket.gate.v1", "status": "POST_HOC exploratory (PD-28 item 1); no verdict",
        **provenance(), "pins": PINS,
        "statistics_computed": "registered F1_pos cells only (precision mode 'registered'); no P_lower or P_upper",
        "max_abs_diff_by_set": by_set, "cells": cells, "all_cells_ok": all(c["ok"] for c in cells)})
    return 0 if all(c["ok"] for c in cells) else 1


def committed(path: Path) -> bool:
    return g.git_blob_sha(str(path.resolve().relative_to(ROOT))) == sha(path)


def run() -> int:
    if not (committed(Path(__file__)) and committed(DESIGN)):
        raise SystemExit("refused: bracket.py and DESIGN.md must equal their HEAD blobs")
    if (ROOT / RESULT).exists():
        raise SystemExit(f"refused: {RESULT} exists (one pass only)")
    cells = gate_cells()
    if not all(c["ok"] for c in cells):
        raise SystemExit("refused: registered cells do not reproduce")
    write(RESULT, {"schema": "vsps.n_f1_bracket.v1", "status": "POST_HOC exploratory; no verdict; never changes a "
                   "registered verdict", **provenance(), "pins": PINS,
                   **assemble([(s75_context(), s75_bracket), (g2b_context(), g2b_bracket)]), "gate_cells": cells})
    return 0


def selftest() -> int:
    checks = {}
    # §7.5 path: 3 images; caption_rows columns [mapped, present, absent, -, -, present pairs, present mentioned, ...]
    a = np.array([[4, 1, 1, 0, 0, 2, 1, 0, 0, 0], [2, 2, 0, 0, 0, 3, 2, 0, 0, 0], [3, 0, 1, 0, 0, 1, 0, 0, 0, 0]], float)
    pr = np.array([0.5, 2 / 3, 0.0])
    full = np.arange(3)[None]
    P = {m: float(v.oi_draws_extended(s75_cols(a, m), full, pr)["P_pos"][0]) for m in MODES}
    R = {m: float(v.oi_draws_extended(s75_cols(a, m), full, pr)["R_pos"][0]) for m in MODES}
    # present 3, absent 2, unverified 4, mapped 9; R = 3 / 6
    checks["s75_hand_P"] = np.allclose([P["registered"], P["lower"], P["upper"]], [60.0, 100 / 3, 700 / 9])
    checks["s75_R_unchanged"] = R["registered"] == R["lower"] == R["upper"] and np.isclose(R["lower"], 50.0)
    a0 = a.copy()
    a0[:, 0] = a0[:, 1] + a0[:, 2]  # no unverified mentions
    f0 = [v.oi_draws_extended(s75_cols(a0, m), full, pr)["F1_pos"][0] for m in MODES]
    checks["s75_no_unverified_all_equal"] = f0[0] == f0[1] == f0[2]
    # G2-B path: 5 images, multinomial weights
    rng = np.random.default_rng(7)
    pm, am, unv = rng.integers(0, 4, 5).astype(float), rng.integers(0, 3, 5).astype(float), rng.integers(0, 3, 5) * 1.0
    r = {"pm": pm, "am": am, "pos": pm + rng.integers(0, 3, 5), "m": pm + am + unv + 1}
    idx, W = np.arange(5), rng.multinomial(5, np.full(5, 0.2), size=50).astype(float)
    sc = {m: g2b_scores(r, pm + am + unv, idx, W, m) for m in MODES}
    checks["g2b_P_order_per_draw"] = bool(np.all(sc["lower"]["P"] <= sc["registered"]["P"] + 1e-15) and
                                          np.all(sc["registered"]["P"] <= sc["upper"]["P"] + 1e-15))
    checks["g2b_F_order_per_draw"] = bool(np.all(sc["lower"]["F"] <= sc["registered"]["F"] + 1e-15) and
                                          np.all(sc["registered"]["F"] <= sc["upper"]["F"] + 1e-15))
    checks["g2b_R_and_M_unchanged"] = all(np.array_equal(sc[m]["R"], sc["registered"]["R"]) and
                                          np.array_equal(sc[m]["M"], sc["registered"]["M"]) for m in MODES)
    one = np.ones((1, 5))
    hand = g2b_scores(r, pm + am + unv, idx, one, "lower")["P"][0], g2b_scores(r, pm + am + unv, idx, one, "upper")["P"][0]
    checks["g2b_hand_P"] = np.allclose(hand, [pm.sum() / (pm + am + unv).sum(), (pm + unv).sum() / (pm + am + unv).sum()])
    z = [g2b_scores(r, pm + am, idx, W, m)["F"] for m in MODES]  # no unverified: the recombined F equals scores' F
    checks["g2b_no_unverified_all_equal"] = bool(np.array_equal(z[0], z[1]) and np.array_equal(z[0], z[2]))
    # run assembly end to end on synthetic contexts of both shapes (never on real data)
    n, sysn = 8, ("s1", "s2", "s3")
    gctx = {"name": "xm600", "systems": list(sysn), "idx": np.arange(n), "scored": np.arange(n), "floor": 1e-9,
            "lo_q": 2.5, "hi_q": 97.5, "W": rng.multinomial(n, np.full(n, 1 / n), size=40).astype(float),
            "rows": {}, "mapped": {}, "golds": {"refs_all": [[{"a"}, set(), {"b", "c"}] + [{"a"}] * 5]}}
    for j, s in enumerate(sysn):
        p_, a_, u_ = (rng.integers(0, 3, n) + j).astype(float), rng.integers(0, 2, n) * 1.0, rng.integers(0, 3, n) * 1.0
        gctx["rows"][s] = {"pm": p_, "am": a_, "pos": p_ + 2, "m": p_ + a_ + u_ + j}
        gctx["mapped"][s] = p_ + a_ + u_
    sctx = {"name": "s75", "full": np.arange(n)[None], "idx_boot": rng.integers(0, n, size=(v.B_PAIRED, n)),
            "scored": np.arange(n), "golds": {"oiv7_verified": [[{"a"}] * n]}, "systems": {}}
    for j, s in enumerate(sysn):
        a = np.zeros((n, 10))
        a[:, 1], a[:, 2] = rng.integers(0, 3, n) + j, rng.integers(0, 2, n)
        a[:, 0] = a[:, 1] + a[:, 2] + rng.integers(0, 3, n)
        a[:, 5] = a[:, 1] + 2
        a[:, 6] = a[:, 1]
        sctx["systems"][s] = {"a": a, "pr": a[:, 6] / a[:, 5], "M_pt": float(a[:, 0].mean() + j),
                              "M_dr": a[:, 0][sctx["idx_boot"]].mean(1) + j}
    body = assemble([(sctx, s75_bracket), (gctx, g2b_bracket)])
    checks["assemble_runs_and_serialises"] = bool(json.dumps(body)) and set(body["sets"]) == {"s75", "xm600"} and \
        body["sentence_paper"] in SENTENCES.values() and body["sets"]["xm600"]["mean_gold_size"]["refs_all"] == 1.0
    # outcome rule
    checks["outcome_rule"] = [outcome({"ci95_raw": c, "ci_finite": f}) for c, f in (
        ([0.01, 2.0], True), ([0.0, 2.0], True), ([-1.0, 2.0], True), (None, False), ([0.5, 1.0], False))] == \
        ["i", "ii", "ii", "ii", "ii"]
    checks["sentences_from_PD28"] = all(f'"{t}"' in (ROOT / ".session_backup/2026-10-13/decisions/PD-28.txt").read_text(
        encoding="utf-8").replace("\n       ", " ") for t in SENTENCES.values())
    checks = {k: bool(x) for k, x in checks.items()}
    write(f"{PRE}/selftest.json", {"schema": "vsps.n_f1_bracket.selftest.v1", **provenance(), "checks": checks,
                                   "pass": all(checks.values())})
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    modes = {"--selftest": selftest, "gate": gate, "run": run}
    if len(sys.argv) != 2 or sys.argv[1] not in modes:
        raise SystemExit(f"usage: {Path(__file__).name} {{{'|'.join(modes)}}}")
    check_pins()
    load_modules()
    sys.exit(modes[sys.argv[1]]())
