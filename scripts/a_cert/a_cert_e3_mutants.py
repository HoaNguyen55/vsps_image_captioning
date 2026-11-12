#!/usr/bin/env python3
"""Mutant harness for scripts/a_cert/a_cert_e3.py (pattern of a_cert_mutants.py): one mutant per registered rule of
the freeze (addendum §3, O3, W1, W5), E1-E6 (§5, O1-O6, O11, W5), §4 (completed status, Q7), the e3-score refusals and
fault rule (§6 step 3, A-CERT §12 step 5), custody and the printed labels (§0, §2, CC-359 1(b)).
Usage: <venv python> -I -B a_cert_e3_mutants.py <scratch dir outside the repo>
Each mutant applies its exact replacements (each target must occur exactly once) and runs `selftest --out
<scratch>/<name>.json` on the mutated source, executed with __file__ = the original path. The unmutated source runs
first and must exit 0 with 'selftest ok'. KILLED = exit != 0, at least one of the mutant's NAMED checks FAILED, and no
`no_exception` entry (a crash is never a kill). Synthetic fixtures only."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "a_cert_e3.py"
LOADER = ("import sys; src, orig, out = sys.argv[1:4]; sys.argv = [orig, 'selftest', '--out', out]; "
          "ns = {'__name__': '__main__', '__file__': orig}; "
          "exec(compile(open(src, encoding='utf-8').read(), orig, 'exec'), ns)")
GUARD = '    if not any(word in ln and h in ln for ln in log_lines(P)):\n'
LBL = {"topup": 'h1, _ = A.human(key1, ans1, w["syn"])'}

# name: ([(old, new), ...], [checks that must catch it])
M = {
    # freeze (§3, O3, W1, W5, §4.4, E4 universe)
    "F01_O3_Q3_pairs_on_I600": ([('return w["idx"]["Q3"] if {a, b} & set(w["fam"]["Q3"]) else w["idx"]["Q25"]',
                                  'return w["idx"]["Q25"]')], ["freeze_O3_I537_for_Q3_member_else_I600"]),
    "F02_pairs_without_S_E_member": ([("if se & set(p))]", "if True)]")], ["freeze_pairs_with_an_S_E_member_only"]),
    "F03_W5_all_cross": ([('return "within" if fam_of(w, a) == fam_of(w, b) else "cross"', 'return "cross"')],
                         ["freeze_W5_within_is_the_model_pair"]),
    "F04_W1_clabel_on_reference_gold": ([('"clabel": js(A.certify(pl, 0.0))', '"clabel": js(A.certify(pc, 0.0))')],
                                        ["freeze_W1_clabel_by_hand"]),
    "F05_budget_alpha_not_alpha_S": ([("A.beta_B(c, x, A.ALPHA_S)) for x in A.GRID}", "A.beta_B(c, x, A.ALPHA)) for x in A.GRID}")],
                                     ["freeze_beta_w0_alpha_S_0.025"]),
    "F06_low_end_wrong_T": ([('Lh = float(f0(c["phi1"], c["phi2"], 2, np.inf))', 'Lh = float(f0(c["phi1"], c["phi2"], 3, np.inf))')],
                            ["freeze_budgets_and_44_low_ends_by_hand"]),
    "F07_E4_universe_twelve_only": ([('set().union(*(w["ms"][s][k] for s in w["sys"]))',
                                      'set().union(*(w["ms"][s][k] for s in w["sys12"]))')],
                                    ["freeze_E4_declared_by_hand", "E4_by_hand_on_N_u_prime"]),
    "F08_E4_universe_keeps_OI_status": ([('return [{c for c in named[k] if c not in w["oi"][k]}', 'return [{c for c in named[k]}')],
                                        ["freeze_E4_declared_by_hand", "E4_by_hand_on_N_u_prime"]),
    "F09_freeze_writes_twice": ([('        if out.exists():\n            raise Fault("FREEZE_E3.json exists")\n', "")],
                                ["freeze_writes_once"]),
    "F10_freeze_skips_build_record": ([('        check_build(w, json.loads((ROOT / P["build"]).read_text(encoding="utf-8")))\n', "")],
                                      ["freeze_refuses_S_E_not_in_build_record"]),
    "F11_single_prompt_model_accepted": ([('any(v != {"short", "detailed"} for v in prompts.values())', "False")],
                                         ["extras_need_both_prompts"]),
    "F12_context_M_on_mapped_only": ([('        m = w["ms_all"][s]\n        L = ', '        m = w["ms"][s]\n        L = ')],
                                     ["ctx_builder_equals_registered_s75_context"]),
    # E1 (O1, O11) and §4 completed status
    "E1_01_reg_with_remainder_as_absent": ([('cn[s]["hn"] + (cn[s]["rem"] if m == "lo" else 0))', 'cn[s]["hn"] + cn[s]["rem"])')],
                                           ["E1_P_c_by_hand_base_and_topup_labels"]),
    "E1_02_hi_end_without_remainder": ([('(cn[s]["hy"] + (cn[s]["rem"] if m == "hi" else 0)', '(cn[s]["hy"] + 0')],
                                       ["E1_remainder_ends_by_hand"]),
    "E1_03_bootstrap_not_Q25_first_500": ([('"name": "s75", "full": q["full"], "idx_boot": q["idx_boot"]',
                                            '"name": "s75", "full": q["full"], "idx_boot": q["idx_boot"][::-1]')],
                                          ["E1_ci_Q25_bootstrap_first_500_rows",
                                           "E1_ci_Q25_bootstrap_first_500_rows_fixture"]),
    "E1_04_topup_labels_ignored": ([("    h = {**h0, **h1}\n", "    h = dict(h0)\n")], ["E1_P_c_by_hand_base_and_topup_labels"]),
    "E1_05_base_labels_ignored_for_S_E": ([("    h = {**h0, **h1}\n", "    h = dict(h1)\n")],
                                          ["E1_P_c_by_hand_base_and_topup_labels"]),
    "E1_06_Q7_old_repeat_enters_status": ([(LBL["topup"], 'h1, _ = A.human({q: {**k, "role": "target"} if k["role"] == '
                                            '"old_repeat" else k for q, k in key1.items()}, ans1, w["syn"])'),
                                           ("    if set(h0) & set(h1) or set(h1) & named12:\n", "    if False:\n")],
                                          ["E1_P_c_by_hand_base_and_topup_labels"]),
    # E2 (O2, W5)
    "E2_01_orientation_recomputed": ([('        bt = p["cref"][str(A.W0)]["better"]\n        cf =',
                                       '        bt = "A" if ea["reg"][0] > eb["reg"][0] else "B"\n        cf =')],
                                     ["E2_orientation_from_freeze"]),
    "E2_02_certified_set_recomputed": ([('"scope": p["scope"], "cref": p["cref"],',
                                         '"scope": p["scope"], "cref": {str(x): A.certify(A.pair_cells(w["ms"], p["A"], p["B"], '
                                         'gr, idx), x) for x in A.GRID},')], ["E2_certified_set_from_freeze"]),
    "E2_03_no_within_cross_split": ([('e2_rows([p for p in prs if p["scope"] == sc])', "e2_rows(prs)")],
                                    ["E2_counts_by_hand_within_cross"]),
    "E2_04_verdict_word_kept": ([("        by[str(x)] = {k: r[k] for k in keys}\n",
                                  '        by[str(x)] = {**{k: r[k] for k in keys}, "label": r["label"]}\n')],
                                ["result_no_verdict_words"]),
    "E2_05_stream_other_seed": ([("Wt = w[\"boot_weights\"](n, np.random.default_rng(A.SEED), A.B_TRUTH)",
                                  "Wt = w[\"boot_weights\"](n, np.random.default_rng(A.SEED + 1), A.B_TRUTH)")],
                                ["E2_stream_boot_weights_rng_20261111"]),
    # E3
    "E3_01_covered_with_x_not_x_hi": ([('"covered": xh <= bz["floor_beta_w0"],', '"covered": x <= bz["floor_beta_w0"],')],
                                      ["E3_covered_uses_x_hi_and_freeze_budget"]),
    "E3_02_budget_recomputed": ([('        bz = fz["budgets"][s]\n', '        bz = freeze_e3_core(w)["budgets"][s]\n')],
                                ["E3_covered_uses_x_hi_and_freeze_budget"]),
    "E3_03_remainder_not_in_x_hi": ([('(st is None and a in ("Y", None))', '(st is None and a == "Y")')],
                                    ["E3_x_and_x_hi_by_hand"]),
    # E4 (O6)
    "E4_01_verdict_word_kept": ([('    e4.pop("reading_no_verdict")\n', '    e4.get("reading_no_verdict")\n')],
                                ["E4_O6_not_evaluable_no_verdict_word"]),
    "E4_02_evaluability_threshold": ([("return not (p2 == 0 or p1 + p2 < A.H3_MIN)", "return not (p2 == 0 or p1 + p2 < 2)")],
                                     ["E4_O6_not_evaluable_no_verdict_word", "freeze_E4_declared_by_hand"]),
    "E4_03_stream_other_seed": ([("Wb = w[\"boot_weights\"](len(i600), np.random.default_rng(A.SEED), A.B_TRUTH)",
                                  "Wb = w[\"boot_weights\"](len(i600), np.random.default_rng(A.SEED + 1), A.B_TRUTH)")],
                                ["E4_stream_boot_weights_rng_20261111"]),
    # E5 (O4)
    "E5_01_short_minus_detailed": ([('r[m]["per"][pr["detailed"]][k][0] - r[m]["per"][pr["short"]][k][0]',
                                     'r[m]["per"][pr["short"]][k][0] - r[m]["per"][pr["detailed"]][k][0]')],
                                   ["E5_detailed_minus_short_by_hand"]),
    "E5_02_P_c_instead_of_F_c": ([('"dF_c": {m: d(m, "F") for m in r}', '"dF_c": {m: d(m, "P") for m in r}')],
                                 ["E5_detailed_minus_short_by_hand"]),
    # E6 (O5, W5)
    "E6_01_old_repeat_vs_topup_session": ([('ans0.get(b1[(k["image"], k["class"])])',
                                            'ans1.get(next((q2 for q2, k2 in key1.items() if k2["role"] == "target" and '
                                            '(k2["image"], k2["class"]) == (k["image"], k["class"])), None))')],
                                          ["E6_old_repeat_vs_base_last_line_by_hand"]),
    "E6_02_U_counted_in_agreement": ([("both = [(a, b) for _, a, b in old if a in yn and b in yn]",
                                       "both = [(a, b) for _, a, b in old]")], ["E6_old_repeat_vs_base_last_line_by_hand"]),
    "E6_03_control_expectation_wrong": ([('exp = {"ctrl_present": "Y", "ctrl_absent": "N", "foil_absent": "N"}',
                                          'exp = {"ctrl_present": "Y", "ctrl_absent": "Y", "foil_absent": "N"}')],
                                        ["E6_controls_by_hand"]),
    "E6_04_part3_vs_base_answers": ([('t1 = {(k["image"], k["class"]): ans1.get(q) for q, k in key1.items()',
                                      't1 = {(k["image"], k["class"]): ans0.get(q) for q, k in key0.items()')],
                                    ["E6_topup_part3_and_old_in_base_part3_by_hand"]),
    "E6_05_old_in_base_part3_miscounted": ([("sum(p in b3 for p, _, _ in old)", "sum(p in b1 for p, _, _ in old)")],
                                           ["E6_topup_part3_and_old_in_base_part3_by_hand"]),
    # §4 / §5 guards
    "G01_base_pair_guard_dropped": ([("    if set(h0) & set(h1) or set(h1) & named12:\n", "    if set(h1) & named12:\n")],
                                    ["topup_target_on_a_base_pair_is_a_fault"]),
    "G02_twelve_system_guard_dropped": ([("    if set(h0) & set(h1) or set(h1) & named12:\n", "    if set(h0) & set(h1):\n")],
                                        ["topup_target_named_by_a_twelve_system_is_a_fault"]),
    # e3-score refusals and fault rule (§6 step 3; A-CERT §12 step 5)
    "S01_no_pin_lines_needed": ([(GUARD, "    if False:\n")], ["x_refuses_without_FREEZE_E3_pin"]),
    "S02_part1_result_not_pinned": ([('r1, r1sha = pinned(P, "part1", "A_CERT_RESULT")',
                                      'r1, r1sha = json.loads((ROOT / P["part1"]).read_text(encoding="utf-8")), ""')],
                                    ["x_refuses_without_part1_result_pin"]),
    "S03_base_copy_not_tied_to_part1": ([('        if r1["provenance"]["labels_sha256"] != a["labels_sha"]:\n',
                                          "        if False:\n")], ["x_refuses_base_copy_not_read_by_part1"]),
    "S04_no_session_end_line_needed": ([('if not any("topup1" in ln and a["topup_labels_sha"] in ln for ln in log):',
                                         "if False:")], ["x_refuses_without_topup_session_end_line"]),
    "S05_topup_key_not_pinned": ([('if not any("topup1" in ln and hx(kb1) in ln for ln in log):', "if False:")],
                                 ["x_refuses_unpinned_topup_key"]),
    "S06_label_sha_not_checked": ([('if hx(lb0) != a["labels_sha"] or hx(lb1) != a["topup_labels_sha"]:', "if False:")],
                                  ["x_refuses_label_sha_mismatch"]),
    "S07_part1_incomplete_allowed": ([('if len(part1) != P["part1_n"] or len(part1 & ans0.keys()) != P["part1_n"]:',
                                       "if False:")], ["x_refuses_base_part1_incomplete"]),
    "S08_pins_not_compared": ([('        if w["pins"] != fz["pins"]:\n', "        if False:\n")],
                              ["x_refuses_pins_differ_from_freeze"]),
    "S09_second_pass_allowed": ([('        if res.exists():\n            raise Fault("result exists (one pass only)")\n', "")],
                                ["x_refuses_if_result_exists"]),
    "S10_fault_prints_message": ([('        print(f"FAULT {type(e).__name__}")\n        return 2\n    finally:',
                                   '        print(f"FAULT {type(e).__name__}: {e}")\n        return 2\n    finally:')],
                                 ["x_refuses_without_FREEZE_E3_pin"]),
    "S11_fault_writes_partial_output": ([('            raise Fault("result exists (one pass only)")\n',
                                          '            raise Fault("result exists (one pass only)")\n'
                                          '        A.write_atomic(res, {"partial": True})\n')],
                                        ["x_refuses_without_FREEZE_E3_pin"]),
    # custody
    "C01_guard_off": ([("    return A.refused(p) or (named and p not in A._LABEL_OK)\n", "    return False\n")],
                      ["guard_refuses_label_files_anywhere", "guard_hook_refuses_open"]),
    "C02_label_file_names_allowed": ([('named = b == "key.json" or (b.startswith(("labels_", "practice_")) and b.endswith(".jsonl")) or',
                                       "named = False or")], ["guard_refuses_label_files_anywhere", "guard_hook_refuses_open"]),
    "C03_argument_guard_off": ([('if mode != "e3-score" and any(refused(x) for x in argv[1:]):', "if False:")],
                               ["freeze_refuses_a_label_path_argument"]),
    "C04_caption_text_in_freeze": ([('meta[s] = {"model": m[1],', 'meta[s] = {"first": p[ids[0]], "model": m[1],')],
                                   ["no_caption_text_in_any_output"]),
    # printed labels (§0, CC-359 1(b))
    "L01_row_label_changed": ([("annotator's top-up overlap is labelled\")", "annotator's overlap is labelled\")")],
                              ["labels_verbatim_addendum_and_CC359"]),
    "L03_row_label_dropped_from_E_rows": ([('{"row_label": ROW_LABEL, **v} for k, v in', "v for k, v in")],
                                          ["row_label_on_every_E_row"]),
    "L02_7c_disclosure_on_every_row": ([('"disclosure": D7C if b == "7c" else None', '"disclosure": D7C')],
                                       ["CC359_disclosure_on_7c_rows_only"]),
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
        print(log[-3000:])
        raise SystemExit("unmutated selftest did not pass")
    res = {}
    for name, (subs, want) in M.items():
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
        crash = any(k.startswith("no_exception") for k in failed) or rec is None
        hit = [k for k in want if k in failed]
        status = "SURVIVED" if rc == 0 else "KILLED" if hit and not crash else "CRASH"
        res[name] = {"status": status, "rc": rc, "named_checks": want, "named_failed": hit, "failed_checks": failed}
        print(f"{status:8s} {name}: {hit or failed[:3] or log.strip().splitlines()[-1:]}")
    killed = sum(v["status"] == "KILLED" for v in res.values())
    summary = {"source_sha256": hashlib.sha256(text.encode()).hexdigest(), "n": len(M), "killed": killed, "mutants": res}
    (scratch / "mutants_result.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(f"{killed}/{len(M)} killed")
    return 0 if killed == len(M) else 1


if __name__ == "__main__":
    sys.exit(main())
