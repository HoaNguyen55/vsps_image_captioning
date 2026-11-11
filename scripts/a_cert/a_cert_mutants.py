#!/usr/bin/env python3
"""Mutant harness for scripts/a_cert/a_cert.py: registration §11 mutants, CC-333 Ruling 5(2) additions, and one or
more mutants per blocking rule B1, B2, B4. Pattern of scripts/a_m1/a_m1_mutants.py.
Usage: <venv python> -I -B a_cert_mutants.py <scratch dir outside the repo>
Each mutant applies its exact replacements (each target must occur exactly once) and runs `selftest --out
<scratch>/<name>.json` on the mutated source, executed with __file__ = the original path. The unmutated source runs
first and must exit 0 with 'selftest ok'. KILLED = exit != 0 and at least one named selftest check FAILED; anything
else is SURVIVED or CRASH, and neither is a kill. Synthetic fixtures only."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "a_cert.py"
LOADER = ("import sys; src, orig, out = sys.argv[1:4]; sys.argv = [orig, 'selftest', '--out', out]; "
          "ns = {'__name__': '__main__', '__file__': orig}; "
          "exec(compile(open(src, encoding='utf-8').read(), orig, 'exec'), ns)")

M = {
    # registration §11
    "01_separate_intervals": [("    return Fr(tA, nA) - Fr(tB + XB, nB) + min(Fr(0), Fr(1, nA) - Fr(1, nB)) * XS\n",
                               "    return Fr(tA, nA) - Fr(tB + XB + XS, nB)\n")],
    "02_shared_cell_sign_flipped": [("min(Fr(0), Fr(1, nA) - Fr(1, nB))", "min(Fr(0), Fr(1, nB) - Fr(1, nA))")],
    "03_c_ignores_k": [("    return (1 - w) / (2 * w)\n", "    return (1 - w) / w\n")],
    "04_cap_without_min_U": [("min(cell[\"U\"], math.floor(beta(cell, w, a_s)))", "math.floor(beta(cell, w, a_s))")],
    "05_tie_counted_confirmed": [("- eb[k] > 0 for k", "- eb[k] >= 0 for k")],
    "06_human_N_overrides_OI": [(
        'key = {"present": "pm", "absent": "am"}.get(st) or {"Y": "hy", "N": "hn"}.get(a, "rem")',
        'key = {"Y": "hy", "N": "hn"}.get(h.get((i, c))) or {"present": "pm", "absent": "am"}.get(st) or "rem"')],
    "06b_controls_enter_status": [('if k["role"] == "target" and k["part"] == 1:', 'if k["part"] == 1:')],
    "07_part3_answer_as_label": [('if k["role"] == "target" and k["part"] == 1:',
                                  'if k["role"] in ("target", "repeat"):')],
    "08_Y_propagated_to_synonym": [("    grp = defaultdict(set)\n",
                                    "    for (i, c), a in list(h.items()):\n"
                                    "        for c2 in [x for x in syn if a == 'Y' and x != c and syn[x] == syn.get(c, c)]:\n"
                                    "            h[(i, c2)] = 'Y'\n    grp = defaultdict(set)\n")],
    "09_recall_from_completed_gold": [('(b1["R"], bW["R"])  #', '(p1["R"], pW["R"])  #')],
    "10_remainder_dropped_from_ends": [(
        'return {"reg": num / den, "lo": num / (den + g["rem"]), "hi": (num + g["rem"]) / (den + g["rem"])}',
        'return {"reg": num / den, "lo": num / den, "hi": num / den}')],
    "10b_remainder_dropped_from_H1_hi": [('((cn[s]["hy"] + (cn[s]["rem"] if m == "hi" else 0)),',
                                          '((cn[s]["hy"] + 0),')],
    "11_certified_set_recomputed_after_labels": [(
        '"scope": p["scope"], "verdict": p["cref"][str(W0)]["verdict"],',
        '"scope": p["scope"], "verdict": certify(pair_cells(w["ms"], p["A"], p["B"], gr, idx), W0)["verdict"],')],
    "12_H3_wrong_percentile": [("np.percentile(d_star, 2.5) > 0", "np.percentile(d_star, 97.5) > 0")],
    "13_freeze_may_open_label_path": [(
        '    return any(f"/{d}/" in low + "/" for d in LABEL_DIRS) and p not in _LABEL_OK\n', "    return False\n")],
    # CC-333 Ruling 5(2)
    "14_orientation_from_completed_gold": [('        bt = p["cref"][str(W0)]["better"]\n',
                                            '        bt = "A" if ea["reg"][0] > eb["reg"][0] else "B"\n')],
    "15_all_three_references": [("out.append((i, [rs[j[0]], rs[j[1]]]))",
                                 "out.append((i, [rs[j[0]], set().union(*[rs[x] for x in range(len(rs)) if x != j[0]])]))")],
    "16_I537_I600_swapped": [('return w["idx"]["Q25"] if scope == "Q25" else w["idx"]["Q3"]',
                              'return w["idx"]["Q3"] if scope == "Q25" else w["idx"]["Q25"]')],
    "17_slope_alpha_not_divided_by_m": [("cap(c, wv, ALPHA / M_FAM)", "cap(c, wv, ALPHA_S)")],
    "18_abstain_counted_confirmed": [("np.zeros(Wi.shape[0], bool)", "np.ones(Wi.shape[0], bool)")],
    "19_P_c_remainder_in_denominator": [('{"reg": num / den,', '{"reg": num / (den + g["rem"]),')],
    "20_score_without_freeze_pin": [('    if not any("FREEZE" in ln and h in ln for ln in log):\n',
                                     "    if False:\n")],
    "21_fault_path_prints_a_statistic": [('raise Fault("§5 STOP")', 'raise Fault(f"§5 STOP {sorted(vv.values())}")'),
                                         ('print(f"FAULT {type(e).__name__}")', 'print(f"FAULT {type(e).__name__}: {e}")')],
    # blocking rules
    "B1a_remainder_one_end_only_H1bc": [("ins = [a <= x <= b for x in (pt, lo, hi)]",
                                         "ins = [a <= x <= b for x in (pt, lo)]")],
    "B1b_remainder_one_end_only_H1a": [("if p_reg and lo > 0 and hi > 0:", "if p_reg and lo > 0:")],
    "B2_tied_pairs_counted_in_V_c": [('ce = [p for p in ev if p["verdict"] == "CERTIFIED"]',
                                      'ce = [p for p in prs if p["verdict"] in ("CERTIFIED", "ABSTAIN")]')],
    "B4_faulting_score_writes_output": [("        out = score_core(w, fz, key, ans)\n",
                                         "        write_atomic(res, {'partial': True})\n"
                                         "        out = score_core(w, fz, key, ans)\n")],
    # H2d (v1.3 §3, §5; CC-336 Q3, CC-337 W3)
    "H2d_01_SESOI_changed": [("H2D_SESOI, H2D_MIN = Fr(1, 10), 5", "H2D_SESOI, H2D_MIN = Fr(1, 20), 5")],
    "H2d_02_percentile_bound_not_required": [("D >= H2D_SESOI and np.percentile(ds, 2.5) > 0", "D >= H2D_SESOI")],
    "H2d_03_NI_ranked_first": [('-math.inf if p["w_star"] == "NI"', 'math.inf if p["w_star"] == "NI"')],
    "H2d_04_stream_other_seed": [("Wd = w[\"boot_weights\"](len(w[\"ids\"]), np.random.default_rng(SEED), B_TRUTH)",
                                  "Wd = w[\"boot_weights\"](len(w[\"ids\"]), np.random.default_rng(SEED + 1), B_TRUTH)")],
    "H2d_05_stream_other_rng_call": [("Wd = w[\"boot_weights\"](len(w[\"ids\"]), np.random.default_rng(SEED), B_TRUTH)",
                                      "Wd = w[\"boot_weights\"](len(w[\"ids\"]), np.random.Generator(np.random.MT19937(SEED)),"
                                      " B_TRUTH)")],
    "H2d_06_evaluable_at_4": [("H2D_SESOI, H2D_MIN = Fr(1, 10), 5", "H2D_SESOI, H2D_MIN = Fr(1, 10), 4")],
    "H2d_07_ties_scored_0": [(" + (a[:, None] == a[None, :]) for a in", " for a in")],
    "H2d_08_ties_scored_1": [("2 * (a[:, None] > a[None, :]) + (a[:, None] == a[None, :])", "2 * (a[:, None] >= a[None, :])")],
    "H2d_09_max_replaced_by_min": [("np.maximum(A[1][1:], A[2][1:])", "np.minimum(A[1][1:], A[2][1:])"),
                                   ("max(auc[1:])", "min(auc[1:])")],
    "H2d_10_margin_alone": [("np.maximum(A[1][1:], A[2][1:])", "A[1][1:]"), ("max(auc[1:])", "auc[1]")],
    "H2d_11_excluded_pairs_kept": [('ev = [k for k, p in enumerate(prs) if p["verdict"] in ("CERTIFIED", "NOT CERTIFIED")]',
                                    "ev = list(range(len(prs)))")],
}


def run(src: Path, out: Path):
    r = subprocess.run([sys.executable, "-I", "-B", "-c", LOADER, str(src), str(SRC), str(out)],
                       capture_output=True, text=True)
    rec = json.loads(out.read_text()) if out.exists() else None
    return r.returncode, r.stdout + r.stderr, rec


def main() -> int:
    scratch = Path(sys.argv[1]).resolve()
    if scratch.is_relative_to(SRC.parents[2]):
        raise SystemExit("scratch dir must be outside the repo")
    scratch.mkdir(parents=True, exist_ok=True)
    text = SRC.read_text(encoding="utf-8")
    base = scratch / "unmutated.py"
    base.write_text(text, encoding="utf-8")
    rc, log, _ = run(base, scratch / "unmutated.json")
    if rc != 0 or "selftest ok" not in log:
        print(log[-2000:])
        raise SystemExit("unmutated selftest did not pass")
    res = {}
    for name, subs in M.items():
        mutated, bad = text, [a for a, _ in subs if text.count(a) != 1]
        if bad:
            res[name] = {"status": f"BAD_TARGET ({[text.count(a) for a in bad]})"}
            print(f"BAD_TARGET {name}")
            continue
        for a, b in subs:
            mutated = mutated.replace(a, b)
        src = scratch / f"{name}.py"
        src.write_text(mutated, encoding="utf-8")
        rc, log, rec = run(src, scratch / f"{name}.json")
        failed = [k for k, v in (rec or {}).get("checks", {}).items() if not v]
        status = "SURVIVED" if rc == 0 else "KILLED" if failed else "CRASH"
        res[name] = {"status": status, "rc": rc, "failed_checks": failed}
        print(f"{status:8s} {name}: {failed[:3] if failed else log.strip().splitlines()[-1:]}")
    killed = sum(v["status"] == "KILLED" for v in res.values())
    summary = {"source_sha256": hashlib.sha256(text.encode()).hexdigest(), "n": len(M), "killed": killed,
               "mutants": res}
    (scratch / "mutants_result.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(f"{killed}/{len(M)} killed")
    return 0 if killed == len(M) else 1


if __name__ == "__main__":
    sys.exit(main())
