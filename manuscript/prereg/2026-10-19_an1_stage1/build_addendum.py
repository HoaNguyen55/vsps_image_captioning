#!/usr/bin/env python3
"""Build ADDENDUM_DRAFT.json and render ADDENDUM_DRAFT.md from ADDENDUM_DRAFT.template.md (A-N1).

Every number in the rendered markdown is a placeholder {{alias:key.path|fmt}} resolved from a file. The rendered file
ends with a table that gives each number's file, sha256 and key. The JSON's theta is computed by the STAGE1_PLAN.md
section 3 theta rule. Existing outputs are never overwritten.

  python3 build_addendum.py
"""
from __future__ import annotations

import json
import math
import re
import subprocess
from pathlib import Path

import measures as me

g = me.g
HERE = Path(__file__).resolve().parent
OUT_JSON, OUT_MD = HERE / "ADDENDUM_DRAFT.json", HERE / "ADDENDUM_DRAFT.md"
S1, DG = HERE / "stage1_results.json", HERE / "stage1_diagnostic.json"
SETS = ("cv295", "xm600", "uv231")
COMMIT_PATHS = {"measures": "scripts/g2b/an1/measures.py", "score_an1": "scripts/g2b/an1/score_an1.py",
                "addendum_json": "manuscript/prereg/2026-10-19_an1_g2b_addendum.json",
                "addendum_md": "manuscript/prereg/2026-10-19_an1_g2b_addendum.md",
                "stage1_record": "manuscript/prereg/2026-10-19_an1_stage1/ (every other file of the task folder)"}


def rel(p: Path) -> str:
    return str(p.resolve().relative_to(me.ROOT))


def theta_rule(s1: dict, mu: str) -> float:
    """STAGE1_PLAN.md section 3, step 5, for measure mu."""
    his = [v["measures"][mu]["rho"][1] for v in s1["sets"].values()]
    if any(h is None for h in his):
        return me.CAP
    return min(me.CAP, round(math.ceil(max(h[1] for h in his) / me.STEP - 1e-9) * me.STEP, 10))


def build_json(s1: dict) -> dict:
    plan = (HERE / "STAGE1_PLAN.md").read_text(encoding="utf-8")
    pre = (HERE / "pre_stage1.sha256").read_text(encoding="utf-8")
    head = subprocess.run(["git", "-C", str(me.ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    cite = {"source": rel(S1), "sha256": g.sha256_file(S1)}
    return {
        "addendum_id": "2026-10-19_an1_g2b_addendum",
        "title": "A-N1: object measures robust to incomplete gold on the G2-B outputs (registered secondary analysis)",
        "status": "DRAFT for the judge (PD-16 final ruling). Registered only if committed before the first computation "
                  "of the statistic on G2-B data, and only as computed by the committed score_an1.py",
        "parent_prereg": {"path": rel(g.PREREG), "sha256": g.sha256_file(g.PREREG), "commit": "0932ba1"},
        "does_not_change": "any G2-B prediction, verdict rule, kill rule, family or gold; score_g2b.py, the G2-B prereg "
                           "and the confirmation map stay byte-identical",
        "tier": "registered secondary; body only, never the abstract or conclusions as confirmatory (map section 6; "
                "PD-16 item 1)",
        "preconditions": ["all registered G2-B decodes present with sidecars (prereg runs)",
                          "CC-027 (b) provenance check: score_g2b.load_runs (KD)", "clean subsets (KL)",
                          "main's go for G2-B scoring (CC-027 (c))"],
        "sets": list(SETS),
        "scope": "NEW-BACKBONE test on development images, not image-out-of-sample: CV295 is part of COCO-2500, XM600 "
                 "is the Paper A XM3600 image set, UV231 is UIT-ViIC test (PD-16 item 4; binding 3). UV231 follows prereg "
                 "exposure.uv231_handling: a FAIL counts, a PASS is never counted as support",
        "family": "LADDER (prereg families.<set>.LADDER), clean subset as for G2B-E1/E2/O1",
        "lexicon": "the primary lexicon of each set (score_g2b.score: the first lexicon); uv231's secondary lexicon "
                   "is not analysed (DESIGN.md D7)",
        "gold_levels": "prereg golds.<set>.one_ref, all_refs, complete",
        "verified_negatives": {"coco80": "U80 minus the instance classes of the image (U80 = the 80 classes of "
                                         "score_coco_probe.load_vi_terms)",
                               "objects_in": "OIV7 classes with status absent (xm3600_oiv7.statuses)"},
        "measures": {"F1": "registered mixed F1 (score_g2b.scores)",
                     "cF1": "condensed F1: precision over judged mentions J = G | (N - G), registered recall; "
                            "equals F1 at the complete level (DESIGN.md D3)",
                     "bpref": "bpref_set, trec_eval min(R, N) form, random order of the mentioned classes"},
        "primary": {"measure": "cF1",
                    "statistic": "Q = theta * Range_F1 - Range_cF1; Range = max - min over the three gold levels of "
                                 "the OLS slope of 100 * measure on ln M over LADDER (score_g2b.stat_slope)",
                    "direction": "Q > 0", "rule": "sign_gt_0",
                    "theta": {"value": theta_rule(s1, "cF1"), **cite,
                              "derivation": "STAGE1_PLAN.md section 3 step 5 applied to cF1: max over the stage-1 sets "
                                            "of sets.<set>.measures.cF1.rho[1][1], rounded up to a multiple of "
                                            "measures.STEP, capped at measures.CAP"}},
        "deviation_from_stage1_plan": {
            "plan_choice": s1["choice"]["primary"], "plan_theta": s1["choice"]["theta"],
            "frozen_choice": "cF1",
            "reason": "stage1_diagnostic.json (computed after the choice was seen): bpref_set / R is close to 1 on every "
                      "set (bpref_over_R_median), so bpref_set's larger shrink comes mostly from dropping precision, a "
                      "near form of degenerate case D1 the rule did not screen; cF1 keeps precision, equals F1 under "
                      "complete gold, and has the larger stage-1 rho, so the deviation makes the test harder",
            "diagnostic": {"source": rel(DG), "sha256": g.sha256_file(DG)}},
        "alternative_if_rule_kept": {"measure": s1["choice"]["primary"],
                                     "theta": {"value": s1["choice"]["theta"], **cite, "key": "choice.theta"}},
        "descriptive": "slopes per level, Range and rho for F1, cF1 and bpref_set; the non-primary candidate's Q at "
                       "theta; unjudged shares, D2 and D6 counts; every statistic on all images (sensitivity); no "
                       "verdicts",
        "bootstrap": "prereg analysis_plan.bootstrap: default_rng(design_constants.set_by_this_registration."
                     "bootstrap_seed).multinomial(N, [1/N]*N, size=design_constants.n_boot) over the clean LADDER "
                     "subset in id order; CI percentiles design_constants.ci_lo_percentile and ci_hi_percentile",
        "verdict_rules": "prereg verdict_rules: sign_gt_0, not_evaluable, counting",
        "outcome_rule": {"order": ["NOT_TESTABLE", "NOT_SUPPORTED", "SUPPORTED", "MIXED"],
                         "not_supported_min_fail_sets": 2, "support_sets": ["cv295", "xm600"],
                         "text": "NOT_TESTABLE if no set is PASS, FAIL or INCONCLUSIVE; NOT_SUPPORTED if 2 or more "
                                 "sets are FAIL (uv231 counts); SUPPORTED if cv295 and xm600 are PASS and no set is "
                                 "FAIL; MIXED otherwise"},
        "consequences": {
            "SUPPORTED": "section 7 body, labelled registered secondary, per-set verdicts and the D1 scope (verified "
                         "negatives needed); cF1 may be offered as the adoptable measure with that scope",
            "MIXED": "per-set verdicts verbatim; no general claim; cF1 stays exploratory",
            "NOT_SUPPORTED": "a registered negative; cF1 is not proposed (A-N1 kill); the IR framing stays as discussion",
            "NOT_TESTABLE": "the paper says the test was not run or not evaluable"},
        "code": {"score_g2b": {"path": "scripts/g2b/score_g2b.py",
                               "sha256": g.sha256_file(me.ROOT / "scripts/g2b/score_g2b.py")},
                 "prereg": {"path": rel(g.PREREG), "sha256": g.sha256_file(g.PREREG)},
                 "measures": {"path": rel(me.HERE), "sha256": g.sha256_file(me.HERE)},
                 "score_an1": {"path": rel(HERE / "score_an1.py"), "sha256": g.sha256_file(HERE / "score_an1.py")}},
        "code_at_head": head,
        "proposed_commit_paths": COMMIT_PATHS,
        "no_overwrite": "measures.py, stage1_diag.py, score_an1.py and build_addendum.py refuse an existing output; a "
                        "delivered file is never overwritten (a new version is _v2)",
        "stage1_record": {
            "status": "EXPLORATORY",
            "plan": {"path": rel(HERE / "STAGE1_PLAN.md"), "sha256": g.sha256_file(HERE / "STAGE1_PLAN.md"),
                     "written_utc": re.search(r"\*\*Written:\*\* (\S+)", plan).group(1)},
            "design": {"path": rel(HERE / "DESIGN.md"), "sha256": g.sha256_file(HERE / "DESIGN.md")},
            "pre_stage1_hashes": {"path": rel(HERE / "pre_stage1.sha256"),
                                  "sha256": g.sha256_file(HERE / "pre_stage1.sha256"),
                                  "recorded_utc": re.search(r"# recorded (\S+)", pre).group(1)},
            "run": {"path": rel(S1), "sha256": g.sha256_file(S1), "started_utc": s1["started_utc"],
                    "finished_utc": s1["finished_utc"], "measures_py_sha256": s1["measures_py_sha256"]},
            "diagnostic": {"path": rel(DG), "sha256": g.sha256_file(DG)}},
        "g2b_outputs_read": "none; data/results/g2b/selfcheck.json is the only file read under data/results/g2b",
        "paper_b_numbers": "none; no Paper-B manifest is read",
        "open_models_only": "Qwen3-VL-8B-Instruct (prereg model.licence)"}


def table(s1: dict) -> str:
    f = lambda v: f"{v:.2f}"  # noqa: E731
    lines = ["| Set | Measure | slope one_ref | slope all_refs | slope complete | Range (95% CI) | ρ = Range/Range_F1 (95% CI) |",
             "|---|---|---|---|---|---|---|"]
    for name, s in s1["sets"].items():
        for mu, m in s["measures"].items():
            sl = [m["slope"][lv][0] for lv in s["levels"]]
            r = m["range"]
            rho = m.get("rho")
            lines.append(f"| {name} | {mu} | {' | '.join(map(f, sl))} | {f(r[0])} ({f(r[1][0])}, {f(r[1][1])}) | "
                         + (f"{f(rho[0])} ({f(rho[1][0])}, {f(rho[1][1])})" if rho else "—") + " |")
    return ("Table S1 (EXPLORATORY). Verbosity slopes (points of 100·measure per unit ln M), their range over the three "
            f"gold levels, and ρ. Source: `{rel(S1)}` (sha256 {g.sha256_file(S1)}), keys "
            "`sets.<set>.measures.<measure>.{slope, range, rho}` ([point, [2.5%, 97.5%]]).\n\n" + "\n".join(lines))


def render(sources: dict[str, Path], s1: dict) -> str:
    data = {a: g.jload(p) for a, p in sources.items()}
    used: dict[tuple, str] = {}

    def sub(m: re.Match) -> str:
        alias, key, fmt = m.group(1), m.group(2), m.group(3) or ""
        v = data[alias]
        for k in key.split("."):
            v = v[int(k)] if isinstance(v, list) else v[k]
        out = str(len(v)) if fmt == "len" else format(v, fmt)
        used[(alias, key + ("|len" if fmt == "len" else ""))] = out
        return out

    text = (HERE / "ADDENDUM_DRAFT.template.md").read_text(encoding="utf-8").replace("{{TABLE}}", table(s1))
    text = re.sub(r"\{\{(\w+):([^|}]+)(?:\|([^}]+))?\}\}", sub, text)
    rows = [f"| {v} | `{rel(sources[a])}` | {g.sha256_file(sources[a])[:16]} | `{k}` |" for (a, k), v in used.items()]
    return text + "\n## Number sources\n\nEvery number above that is not in Table S1 comes from this table (sha256 " \
                  "prefix; full values in MANIFEST.json).\n\n| Value | File | sha256 | Key |\n|---|---|---|---|\n" + \
        "\n".join(rows) + "\n"


def main() -> None:
    for p in (OUT_JSON, OUT_MD):
        if p.exists():
            raise SystemExit(f"{p} exists; never overwritten (write a _v2)")
    s1 = g.jload(S1)
    OUT_JSON.write_text(json.dumps(build_json(s1), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(render({"s1": S1, "dg": DG, "ad": OUT_JSON, "pr": g.PREREG}, s1), encoding="utf-8")
    print(json.dumps({"theta_cF1": g.jload(OUT_JSON)["primary"]["theta"]["value"],
                      "json_sha256": g.sha256_file(OUT_JSON), "md_sha256": g.sha256_file(OUT_MD)}))


if __name__ == "__main__":
    main()
