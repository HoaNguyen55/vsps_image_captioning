#!/usr/bin/env python3
"""A-N1 registered secondary analysis of the G2-B outputs (ADDENDUM_DRAFT.md and .json).

Imports scripts/g2b/score_g2b.py and measures.py (the stage-1 instrument), both unchanged. The primary measure, theta,
the verdict rule and the outcome rule come from the addendum JSON. Seeds, bootstrap draws, percentiles, clean subsets,
lexicons, families, gold levels and verdict rules come from the G2-B prereg, through score_g2b.

  selftest  checks of the outcome rule, plus measures.py selftest
  score     python3 score_an1.py score --addendum A.json --outputs-dir DIR --out RESULTS.json
            Refuses unless score_g2b.py, the prereg, its frozen files, measures.py and this file match their pins;
            this file, measures.py and the addendum are committed and unchanged at HEAD; every registered G2-B run has
            its output and sidecar; and --out does not exist.
  dryrun    python3 score_an1.py dryrun --addendum A.json --out DRYRUN.json
            The same analysis, with stage-1 captions standing in for the six LADDER runs. It is a code test, not a
            result, and it reads no G2-B output.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import measures as me  # noqa: E402

g, ROOT = me.g, me.ROOT
STAGE1_STANDIN = {"cv295": "COCO-2500", "uv231": "UIT-ViIC test", "xm600": "XM3600"}


def pin_problems(add: dict, add_path: Path, strict_git: bool) -> list[str]:
    files = {"score_g2b": ROOT / "scripts/g2b/score_g2b.py", "prereg": g.PREREG, "measures": me.HERE, "score_an1": HERE}
    bad = [f"{k}: sha256 differs from the addendum pin" for k, p in files.items()
           if g.sha256_file(p) != add["code"][k]["sha256"]]
    bad += [f"prereg frozen file differs: {p}" for p in g.check_pins(g.jload(g.PREREG))]
    if strict_git:
        for p in (me.HERE, HERE, add_path.resolve()):
            rel = str(p.relative_to(ROOT))
            if g.git_blob_sha(rel) != g.sha256_file(p):
                bad.append(f"not committed, or changed since HEAD: {rel}")
    return bad


def analyse_set(reg: dict, add: dict, ds, clean: bool) -> dict:
    dc = reg["design_constants"]
    floor, lo, hi = (dc[k]["value"] for k in ("tp_floor", "ci_lo_percentile", "ci_hi_percentile"))
    lad = reg["families"][ds.name]["LADDER"]
    if any(s not in ds.caps for s in lad):
        return {"verdict": "NOT_EVALUABLE", "reason": "a LADDER run is missing or excluded (KD)"}
    idx = ds.clean_index(lad, clean)
    n = len(idx)
    if n == 0:
        return {"verdict": "NOT_EVALUABLE", "reason": "empty analysis set", "n_images": 0}
    W = np.random.default_rng(dc["set_by_this_registration"]["bootstrap_seed"]).multinomial(
        n, np.full(n, 1.0 / n), size=dc["n_boot"]["value"]).astype(float)
    gl = reg["golds"][ds.name]
    levels = [gl["one_ref"], gl["all_refs"], gl["complete"]]
    lx = next(iter(ds.lex))  # the primary lexicon, as in score_g2b.score
    S = me.analyse(ds, lad, lx, levels, idx, np.vstack([np.ones((1, n)), W]), floor)
    rng = {mu: S[mu].max(0) - S[mu].min(0) for mu in S}
    p = add["primary"]
    mu, th = p["measure"], p["theta"]["value"]
    q = {m: th * rng["F1"] - rng[m] for m in me.CANDIDATES}
    point, interval = float(q[mu][0]), g.ci(q[mu][1:], lo, hi)
    return {"n_images": n, "n_images_full": len(ds.ids), "lexicon": lx, "levels": levels, "systems": lad,
            "primary": {"measure": mu, "theta": th, "stat": p["statistic"], "rule": p["rule"], "point": point,
                        "ci95": interval, "verdict": g.verdict(p["rule"], point, interval) if clean else None},
            "descriptive": me.summary(S, levels, lo, hi),
            "descriptive_Q_at_theta": {m: me.pc(q[m], lo, hi) for m in me.CANDIDATES},
            "diagnostics_all_images": me.diagnostics(ds, lad, lx, levels)}


def outcome(rule: dict, verdicts: dict) -> str:
    """The addendum's outcome rule, from the per-set verdicts of the primary statistic."""
    if not any(v in ("PASS", "FAIL", "INCONCLUSIVE") for v in verdicts.values()):
        return "NOT_TESTABLE"
    if sum(v == "FAIL" for v in verdicts.values()) >= rule["not_supported_min_fail_sets"]:
        return "NOT_SUPPORTED"
    if all(verdicts.get(d) == "PASS" for d in rule["support_sets"]) and "FAIL" not in verdicts.values():
        return "SUPPORTED"
    return "MIXED"


def run(add: dict, datasets: dict, header: dict, out: Path) -> int:
    reg = g.jload(g.PREREG)
    result = {**header, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "sets": {}}
    for name, ds in datasets.items():
        result["sets"][name] = {"primary_analysis": analyse_set(reg, add, ds, clean=True),
                                "sensitivity_full_set": analyse_set(reg, add, ds, clean=False)}
    verdicts = {d: v["primary_analysis"].get("primary", v["primary_analysis"]).get("verdict")
                for d, v in result["sets"].items()}
    result["verdicts"] = verdicts
    result["outcome"] = outcome(add["outcome_rule"], verdicts)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    Path(str(out) + ".sha256").write_text(f"{g.sha256_file(out)}  {out.name}\n", encoding="utf-8")
    print(json.dumps({"verdicts": verdicts, "outcome": result["outcome"]}))
    return 0


def score(add_path: Path, outputs: Path, out: Path) -> int:
    if out.exists():
        raise SystemExit(f"{out} exists; never overwritten")
    add, reg = g.jload(add_path), g.jload(g.PREREG)
    bad = pin_problems(add, add_path, strict_git=True)
    if bad:
        raise SystemExit("refused: " + "; ".join(bad))
    files = {r["run_id"]: outputs / f"{r['run_id']}.{'samples.jsonl' if r['sequences_per_image'] > 1 else 'preds.json'}"
             for r in reg["runs"]}  # the file names of score_g2b.load_runs
    missing = [rid for rid, f in files.items() if not (f.exists() and Path(str(f) + ".sha256").exists())]
    if missing:
        raise SystemExit(f"refused: precondition 'all registered decodes' not met, missing {missing}")
    lang = {r["run_id"]: ("en" if r["prompt_mode"].endswith("_en") else "vi") for r in reg["runs"]}
    caps, excluded = g.load_runs(reg, outputs, {d: reg["datasets"][d]["n_images"] for d in reg["datasets"]})
    datasets = {d: g.Dataset(reg, d, {k: v for k, v in caps.items() if k.startswith(f"g2b_q3_{d}-")}, lang)
                for d in add["sets"]}
    header = {"schema": "vsps.an1_g2b.v1", "status": "registered secondary analysis (A-N1 addendum)",
              "code_sha256": {k: v["sha256"] for k, v in add["code"].items()},
              "addendum_sha256": g.sha256_file(add_path), "excluded_runs_KD": excluded,
              "outputs_sha256": {f.name: g.sha256_file(f) for f in sorted(outputs.glob("g2b_q3_*"))
                                 if not f.name.endswith((".sha256", ".partial.jsonl"))}}
    return run(add, datasets, header, out)


def dryrun(add_path: Path, out: Path) -> int:
    if out.exists():
        raise SystemExit(f"{out} exists; never overwritten")
    add, reg = g.jload(add_path), g.jload(g.PREREG)
    stand = {name: files for name, _, _, _, files, _ in me.stage1_inputs()}
    datasets, used = {}, {}
    for d in add["sets"]:
        lad = reg["families"][d]["LADDER"]
        files = list(stand[STAGE1_STANDIN[d]].values())[:len(lad)]
        used[d] = {rid: str(f.relative_to(ROOT)) for rid, f in zip(lad, files)}
        datasets[d] = g.Dataset(reg, d, {rid: g.read_captions(f) for rid, f in zip(lad, files)},
                                {rid: "vi" for rid in lad})
    header = {"schema": "vsps.an1_g2b.dryrun.v1",
              "status": "DRY RUN: stage-1 captions stand in for the LADDER runs; a code test, not a result; "
                        "no G2-B output was read", "pin_problems": pin_problems(add, add_path, strict_git=False),
              "standins": used}
    return run(add, datasets, header, out)


def selftest() -> int:
    rule = {"not_supported_min_fail_sets": 2, "support_sets": ["cv295", "xm600"]}
    cases = [({"cv295": "PASS", "xm600": "PASS", "uv231": "INCONCLUSIVE"}, "SUPPORTED"),
             ({"cv295": "PASS", "xm600": "PASS", "uv231": "FAIL"}, "MIXED"),
             ({"cv295": "PASS", "xm600": "INCONCLUSIVE", "uv231": "PASS"}, "MIXED"),
             ({"cv295": "FAIL", "xm600": "PASS", "uv231": "FAIL"}, "NOT_SUPPORTED"),
             ({"cv295": "NOT_EVALUABLE", "xm600": "NOT_EVALUABLE", "uv231": None}, "NOT_TESTABLE"),
             ({"cv295": "PASS", "xm600": "NOT_EVALUABLE", "uv231": "PASS"}, "MIXED")]
    for v, want in cases:
        assert outcome(rule, v) == want, (v, outcome(rule, v), want)
    return me.selftest()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)
    sub.add_parser("selftest")
    s = sub.add_parser("score")
    s.add_argument("--addendum", type=Path, required=True)
    s.add_argument("--outputs-dir", type=Path, required=True)
    s.add_argument("--out", type=Path, required=True)
    d = sub.add_parser("dryrun")
    d.add_argument("--addendum", type=Path, required=True)
    d.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    sys.exit(selftest() if a.mode == "selftest" else score(a.addendum, a.outputs_dir, a.out) if a.mode == "score"
             else dryrun(a.addendum, a.out))


if __name__ == "__main__":
    main()
