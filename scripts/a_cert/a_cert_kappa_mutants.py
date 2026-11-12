#!/usr/bin/env python3
"""Mutant harness for scripts/a_cert/a_cert_kappa.py, round 2 (CC-372 B5, N5; pattern of a_cert_e3_mutants.py).
Usage: python3 -I -B a_cert_kappa_mutants.py <scratch dir outside the repo>
Each mutant replaces one source line (its target must occur exactly once) and runs `selftest --out
<scratch>/<name>.json` on the mutated source, executed with __file__ = the original path. The unmutated source runs
first and must exit 0 with 'selftest ok'. KILLED = exit != 0, at least one of the mutant's NAMED checks FAILED, and no
`no_exception` entry (a crash is never a kill). Synthetic fixtures only."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "a_cert_kappa.py"
LOADER = ("import sys; src, orig, out = sys.argv[1:4]; sys.argv = [orig, 'selftest', '--out', out]; "
          "ns = {'__name__': '__main__', '__file__': orig}; "
          "exec(compile(open(src, encoding='utf-8').read(), orig, 'exec'), ns)")
W = "world_p1_target_"
SRC_LINE = 'src = pi1 if s.startswith("p1_") else pi2'
GUARD = "if False:"

# name: (old, new, [checks that must catch it])
M = {
    # statistics (plan §4 l.37) and the W11 inputs (CC-372 ruling 2)
    "K01_first_line_wins": ('out[r["qid"]] = r["label"]', 'out.setdefault(r["qid"], r["label"])',
                            ["answers_last_line_wins", W + "table_last_line_wins"]),
    "K02_p_e_Y_term_only": ("pe = Fr((yy + yn) * (yy + ny) + (ny + nn) * (yn + nn), n * n)", "pe = Fr((yy + yn) * (yy + ny), n * n)",
                            ["kappa_4_1_1_4_is_exactly_3_5", "kappa_6_2_0_2_unequal_marginals_6_11_pabak_3_5"]),
    "K03_undefined_reported_as_0": ("kappa = None if pe == 1 else", "kappa = Fr(0) if pe == 1 else",
                                    ["kappa_both_constant_same_answer_undefined",
                                     "world_p1_control_three_roles_pooled_undefined_flag_no_gate"]),
    "K04_pabak_is_raw_agreement": ('"pabak": 2 * po - 1', '"pabak": po',
                                   ["kappa_4_1_1_4_is_exactly_3_5", "kappa_opposite_constants_0_pabak_minus_1"]),
    "K05_PI_part1_from_L2": (SRC_LINE, "src = pi2", [W + "table_last_line_wins"]),
    "K06_U_rate_denominator": ('"U_rate": Fr(c["U"], n) if n else None', '"U_rate": Fr(c["U"], n - c["U"]) if n else None',
                               ["rater_counts_and_rates", W + "UA_rates_per_rater"]),
    "K07_part3_gets_statistics": ('STAT_STRATA = ("p1_target", "p1_control", "p2_target")',
                                  'STAT_STRATA = ("p1_target", "p1_control", "p2_target", "p3_repeat")',
                                  ["world_p3_repeat_count_only"]),
    "K08_control_roles_not_pooled": ('"p1_target" if role == "target" else "p1_control"',
                                     '"p1_control" if role == "ctrl_absent" else "p1_target"',
                                     ["world_p1_control_three_roles_pooled_undefined_flag_no_gate"]),
    "K09_parts_2_3_swapped": ('2: "p2_target", 3: "p3_repeat"', '3: "p2_target", 2: "p3_repeat"',
                              ["world_p2_target_from_L2_kappa_3_5_gate_GOLD"]),
    "K10_late_overlap_count_all": ('"overlap_part1": sum(q in st for q in late)', '"overlap_part1": len(late)',
                                   ["world_late_part1_lines_ignored_and_counted"]),
    "K11_W1_counts_lines_not_questions": ('len({q for q in tail if st.get(q) == "p2_target"})',
                                          'len([q for q in tail if st.get(q) == "p2_target"])',
                                          ["world_W1_part2_final_after_index_8"]),
    "K12_PI_part2_from_L1": (SRC_LINE, "src = pi1", ["world_p2_target_from_L2_kappa_3_5_gate_GOLD"]),
    "K13_late_lines_not_part1_only": ("bpart[q] == 1]", "bpart[q] >= 1]", ["world_late_part1_lines_ignored_and_counted"]),
    # gate (plan §4 l.38; CC-372 ruling 3)
    "G01_strictly_above": ("kappa >= THRESHOLD", "kappa > THRESHOLD",
                           ["gate_at_or_above_3_5_below_and_undefined_sensitivity",
                            "world_p2_target_from_L2_kappa_3_5_gate_GOLD"]),
    "G02_gate_on_pabak": ('row["gate"] = gate(row["kappa"])', 'row["gate"] = gate(row["pabak"])',
                          [W + "gate_on_kappa_not_pabak"]),
    "G03_threshold_0_50": ("THRESHOLD = Fr(3, 5)", "THRESHOLD = Fr(1, 2)",
                           ["gate_at_or_above_3_5_below_and_undefined_sensitivity", W + "gate_on_kappa_not_pabak"]),
    "G04_controls_gated": ('GATED = ("p1_target", "p2_target")', 'GATED = ("p1_target", "p1_control", "p2_target")',
                           ["world_p1_control_three_roles_pooled_undefined_flag_no_gate"]),
    "G05_undefined_is_gold": ('return "SENSITIVITY_ONLY"  # CC-372 ruling 3', 'return "GOLD"  # CC-372 ruling 3',
                              ["gate_at_or_above_3_5_below_and_undefined_sensitivity",
                               "undefined_row_sensitivity_kappa_null_flag_rule"]),
    "G06_undefined_flag_dropped": ('row["kappa_undefined"] = row["kappa"] is None', 'row["kappa_undefined"] = False',
                                   ["undefined_row_sensitivity_kappa_null_flag_rule",
                                    "world_p1_control_three_roles_pooled_undefined_flag_no_gate"]),
    "G07_undefined_rule_text_dropped": ('RULE_UNDEFINED if row["kappa_undefined"] else RULE[row["gate"]]', 'RULE[row["gate"]]',
                                        ["undefined_row_sensitivity_kappa_null_flag_rule"]),
    # score refusals, completeness and fault rule (CC-372 rulings 1, 2, 4, 8; N1, N2, N4)
    "S01_out_exists_allowed": ('if Path(a["out"]).exists():', GUARD,
                               ["refuses_out_exists_before_labels", "second_run_refused_FAULT_type_label_free"]),
    "S02_sha_argument_unchecked": ('if not all(re.fullmatch(r"[0-9a-f]{64}", h) for h in shas):', GUARD,
                                   ["refuses_sha_argument_not_64_hex"]),
    "S03_shas_not_distinct": ("if len(set(shas)) != 3:", GUARD, ["refuses_sha_arguments_not_distinct"]),
    "S04_pi1_not_PI1_SHA": ('if a["labels_pi1_sha"] != P["pi1_sha"]:', GUARD, ["refuses_pi1_sha_not_PI1_SHA_before_labels"]),
    "S05_assignment_pins_unchecked": ('if (hx(ab), hx(rb)) != (P["assign_sha"], P["r2_sha"]):', GUARD,
                                      ["refuses_base_assignment_pin_before_labels", "refuses_r2_assignment_pin_before_labels"]),
    "S06_key_sha_unchecked": ('if ksha != P["key_sha"]:', GUARD, ["refuses_key_sha_before_labels"]),
    "S07_r2_qid_not_in_key": ("if qid not in kmap:", GUARD, ["refuses_r2_qid_not_in_key"]),
    "S08_key_part_unchecked": ('if part != s["part"]:', GUARD, ["refuses_key_part_differs_from_screen_part"]),
    "S09_role_set_unchecked": ("if role not in ROLES[part]:", GUARD,
                               ["refuses_part1_role_outside_set", "refuses_part2_role_not_target"]),
    "S10_counts_unchecked": ('if n != P["n"]:', GUARD, ["refuses_stratum_sizes_not_registered"]),
    "S11_r2_not_checked_against_base": ('if bpart.get(qid) != s["part"]:', GUARD, ["refuses_r2_question_not_in_base"]),
    "S12_label_sha_unchecked": ("if (hx(l1), hx(l2), hx(l3)) != tuple(shas):", GUARD,
                                ["refuses_label_sha_mismatch", "after_labels_fault_prints_stage_and_writes_nothing"]),
    "S13_L2_prefix_unchecked": ("if not l2.startswith(l1):", GUARD, ["refuses_L2_not_extending_L1"]),
    "S14_PI_qid_outside_base": ("if not set(pi2) <= bpart.keys():", GUARD, ["refuses_PI_qid_not_in_base"]),
    "S15_R2_qid_outside_r2": ("if not set(r2) <= r2q:", GUARD, ["refuses_R2_qid_outside_R2_assignment"]),
    "S16_annotator_unchecked": ('if r.get("annotator") != who or r.get("label") not in LABELS:',
                                'if r.get("label") not in LABELS:',
                                ["answers_wrong_annotator_is_fault", "refuses_row_of_other_annotator_in_file"]),
    "S17_PI_part1_incomplete_allowed": ("if not p1q <= pi1.keys():", GUARD, ["refuses_PI_part1_incomplete"]),
    "S18_PI_part2_incomplete_allowed": ("if not p2q <= pi2.keys():", GUARD, ["refuses_PI_part2_incomplete"]),
    "S19_R2_incomplete_allowed": ("if not (p1q | p2q) <= r2.keys():", GUARD, ["refuses_R2_incomplete"]),
    "S20_fault_prints_message": ('print(f"FAULT {type(e).__name__} {', 'print(f"FAULT {type(e).__name__}: {e} {',
                                 ["second_run_refused_FAULT_type_label_free"]),
    "S21_stage_never_after_labels": ('seen["labels"] = True', 'seen["labels"] = False',
                                     ["after_labels_fault_prints_stage_and_writes_nothing"]),
    "S22_main_argv_keys_unmapped": ('zip((x[2:].replace("-", "_") for x in SCORE_ARGS)', "zip((x[2:] for x in SCORE_ARGS)",
                                    ["main_maps_score_argv_to_a_label_free_pin_fault"]),
    "S23_write_fault_leaves_temp_dir": ("        shutil.rmtree(tmp, ignore_errors=True)\n", "        pass\n",
                                        ["write_fault_leaves_no_temp_dir"]),
    "S24_PI_and_R2_swapped": ('ANNOT = ("PI", "R2")', 'ANNOT = ("R2", "PI")', [W + "table_last_line_wins"]),
    # custody
    "C01_key_json_not_refused": ('    return b == "key.json" or', '    return False and b == "key.json" or',
                                 ["custody_refuses_key_label_and_sealed_paths", "ok_list_cleared_and_key_refused_after_score"]),
    "C02_ok_list_kept": ("        _OK.clear()\n", "        pass\n", ["ok_list_cleared_and_key_refused_after_score"]),
    "C03_hook_off": ("isinstance(args[0], (str, bytes, os.PathLike)) and refused(args[0]):",
                     "isinstance(args[0], (str, bytes, os.PathLike)) and False:", ["custody_hook_blocks_open_of_key_json"]),
    "C04_label_name_rule_off": ('bool(re.fullmatch(r"(labels|practice)_.*\\.jsonl", b))', "False",
                                ["custody_refuses_key_label_and_sealed_paths"]),
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
    for name, (old, new, want) in M.items():
        if text.count(old) != 1:
            res[name] = {"status": f"BAD_TARGET ({text.count(old)})"}
            print(f"BAD_TARGET {name}")
            continue
        src = scratch / f"{name}.py"
        src.write_text(text.replace(old, new), encoding="utf-8")
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
