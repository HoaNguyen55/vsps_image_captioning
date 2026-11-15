#!/usr/bin/env python3
"""Mutant harness for scripts/a_cert/a_cert_perann.py, round 2 (CC-391 B1-B3; pattern of a_cert_kappa_mutants.py,
CC-371 standard). Several mutants may share one target (G02/G03, G04-G07, H02/H05); each target occurs once.
Usage: <venv python> -I -B a_cert_perann_mutants.py <scratch dir outside the repo>
Each mutant replaces one source line (its target must occur exactly once) and runs `selftest --out
<scratch>/<name>.json` on the mutated source, executed with __file__ = the original path (so a_cert.py and
a_cert_kappa.py are imported from the repo tree). The unmutated source runs first and must exit 0 with 'selftest ok'.
KILLED = exit != 0, at least one of the mutant's NAMED checks FAILED, and no `no_exception` entry (a crash is never a
kill). Synthetic fixtures only."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "a_cert_perann.py"
LOADER = ("import sys; src, orig, out = sys.argv[1:4]; sys.argv = [orig, 'selftest', '--out', out]; "
          "ns = {'__name__': '__main__', '__file__': orig}; "
          "exec(compile(open(src, encoding='utf-8').read(), orig, 'exec'), ns)")
GUARD = "if False:"
OUT = "answers_outside_overlap_change_nothing"
H3 = "H3_overlap_wiring_by_hand"
H2B = "H2b_all_images_equals_score_core"
NONFIN = "nonfinite_overlap_faults_label_free_before_key"
END_NEED = 'end_need = ("R2 finished all screens yes", a["labels_r2_sha"])'
UP_NEED = 'up_need = (UNSEAL_TOKEN, a["labels_r2_sha"], a["labels_pi_sha"], hx(Path(__file__).read_bytes()))'

# name: (old, new, [checks that must catch it])
M = {
    # overlap wiring and values (reg v1.1 §6 H1, H3; a_cert functions reused)
    "W01_M_from_mapped_mentions": ('len(w["ms_all"][s][k])', 'len(w["ms"][s][k])',
                                   ["restricted_M_on_all_images_equals_context_M",
                                    "restriction_on_all_images_reproduces_fam_slopes"]),
    "W02_Q3_not_within_I537": ('q3 = np.intersect1d(np.asarray(g2["idx"]), pos)', "q3 = pos",
                               ["Q3_is_overlap_within_I537", "H1_n_images_Q25_overlap_Q3_within_I537"]),
    "W03_s75_point_on_all_images": ('c75 = {**s75, "full": pos[None],', 'c75 = {**s75, "full": np.arange(len(w["ids"]))[None],',
                                    [OUT]),
    "W04_xm600_index_not_restricted": ('c3 = {**g2, "idx": q3, "W": np.ones((1, len(q3)))}',
                                       'c3 = {**g2, "W": np.ones((1, len(g2["idx"])))}', [OUT]),
    "W05_remainder_to_wrong_end": ('cn[s]["hy"] + (cn[s]["rem"] if m == "hi" else 0)',
                                   'cn[s]["hy"] + (cn[s]["rem"] if m == "lo" else 0)',
                                   ["H1_all_images_equals_score_core_reg_lo_hi"]),
    "W06_human_N_dropped": ('cn[s]["hn"] + (cn[s]["rem"] if m == "lo" else 0)',
                            '0 * cn[s]["hn"] + (cn[s]["rem"] if m == "lo" else 0)',
                            ["H1_all_images_equals_score_core_reg_lo_hi"]),
    "W07_rows_on_all_images": ("ws = sub_world(w, pos)", 'ws = sub_world(w, np.arange(len(w["ids"])))',
                               ["overlap_rows_differ_from_all_image_rows", OUT]),
    "W08_H3_stream_seed": ("np.random.default_rng(ac.SEED), ac.B_TRUTH)", "np.random.default_rng(0), ac.B_TRUTH)",
                           ["H3_stream_boot_weights_20_seed_20261111_rows_1_2000", "H3_all_images_equals_score_core"]),
    "W09_H3_universe_keeps_OI_pairs": ('nu = [{c for c in nm[k] if c not in w["oi"][k]} for k in range(len(w["ids"]))]',
                                       'nu = [set(nm[k]) for k in range(len(w["ids"]))]',
                                       [H3, "H3_all_images_equals_score_core"]),
    "W10_H3_on_all_images": ("row = ac.h3_row(w, gr, h, nu, Wb, pos)",
                             'row = ac.h3_row(w, gr, h, nu, w["boot_weights"](len(w["ids"]), np.random.default_rng('
                             'ac.SEED), ac.B_TRUTH), np.arange(len(w["ids"])))', [H3, OUT]),
    "W11_completed_absent_needs_both": ('w["oi"][k].get(c) == "absent" or h.get((w["ids"][k], c)) == "N"',
                                        'w["oi"][k].get(c) == "absent" and h.get((w["ids"][k], c)) == "N"', [H3]),
    "W12_stop_guard_P_unchecked": ('([(rng["P"]["range"], bP)] if fam == "Q3" else [])', "[]", ["stop_guard_by_hand"]),
    "W13_stop_guard_off": ("if any(not lo - 1e-9 <= x <= hi + 1e-9 for x in vals.values()):", GUARD,
                           ["stop_guard_by_hand"]),
    "W14_stamp_without_no_verdict": ('return f"descriptive; no verdict; {n} overlap images; annotator {who}"',
                                     'return f"descriptive; {n} overlap images; annotator {who}"', ["stamp_text"]),
    "W15_H2d_reason_of_H2a": ('"H2d": nc(who, n, "H2d")', '"H2d": nc(who, n, "H2a")',
                              ["not_computable_rows_with_their_reasons"]),
    "W16_H1_interval_reason_swapped": ('out["interval"] = nc(who, n, "H1_interval")',
                                       'out["interval"] = nc(who, n, "H1_rule_words")',
                                       ["not_computable_rows_with_their_reasons"]),
    "W17_missing_overlap_id_allowed": ("if len(pos) != len(ov):", GUARD, ["positions_by_hand_and_missing_id_fault"]),
    "W18_restriction_guard_off": ('if any(abs(a[k][0] - b[k][0]) > 1e-9 for k in ("F", "P")):', GUARD,
                                  ["refuses_restriction_not_reproducing_slopes"]),
    "W19_label_sources_swapped": ('{"PI": {q: pi[q] for q in t}, "R2": {q: r2[q] for q in t}}',
                                  '{"PI": {q: r2[q] for q in t}, "R2": {q: pi[q] for q in t}}',
                                  ["score_writes_once_rows_equal_direct_compute"]),
    "W20_annotator_names_swapped": ('ak.answers(lp.decode("utf-8").splitlines(), "PI")',
                                    'ak.answers(lp.decode("utf-8").splitlines(), "R2")',
                                    ["score_writes_once_rows_equal_direct_compute"]),
    "W21_code_pins_never_checked": ("return [f for f, want in pins.items() if hashlib.sha256((HERE / f).read_bytes())"
                                    ".hexdigest() != want]", "return []", ["code_pins_hold_and_other_sha_refused"]),
    # H2b on the overlap (CC-391 B1)
    "H01_H2b_x_on_all_images": ('"H2b": h2b_rows(ws, gr, h, pos, pre["h2b"], who, n)',
                                '"H2b": h2b_rows(ws, gr, h, np.arange(len(ws["ids"])), pre["h2b"], who, n)', [OUT]),
    "H02_H2b_budget_on_all_images": ("bud = h2b_budgets(ws, gr, pos)", 'bud = h2b_budgets(ws, gr, np.arange(len(w["ids"])))',
                                     ["overlap_rows_differ_from_all_image_rows"]),
    "H03_x_hi_without_remainder": ('h.get((i, cc)) in ("Y", None)', 'h.get((i, cc)) in ("Y",)',
                                   [H2B, "H2b_counts_binding_and_word_by_hand"]),
    "H04_covered_at_other_grid_w": ('"floor_beta_w0": math.floor(b[str(ac.W0)])',
                                    '"floor_beta_w0": math.floor(b[str(ac.GRID[3])])', [H2B]),
    "H05_H2b_index_within_I537": ("bud = h2b_budgets(ws, gr, pos)", 'bud = h2b_budgets(ws, gr, ws["idx"]["Q3"])', [H2B]),
    "H06_binding_from_x_not_U": ('binds = sum(bud[s]["floor_beta_w0"] < bud[s]["U"] for s in bud)',
                                 'binds = sum(bud[s]["floor_beta_w0"] < rows[s]["x"] for s in bud)',
                                 ["H2b_counts_binding_and_word_by_hand"]),
    # gate-line content (CC-391 B2)
    "G01_line_content_untested": ("pat.search(ln) and all(x in ln for x in need)", "pat.search(ln)", [
        "refuses_end_line_without_phrase", "refuses_end_line_with_other_R2_sha", "refuses_unsealing_line_without_token",
        "refuses_unsealing_line_without_PI_sha", "refuses_unsealing_line_without_R2_sha",
        "refuses_unsealing_line_without_script_sha"]),
    "G02_end_phrase_dropped": (END_NEED, 'end_need = (a["labels_r2_sha"],)', ["refuses_end_line_without_phrase"]),
    "G03_end_R2_sha_dropped": (END_NEED, 'end_need = ("R2 finished all screens yes",)',
                               ["refuses_end_line_with_other_R2_sha"]),
    "G04_up_token_dropped": (UP_NEED, 'up_need = (a["labels_r2_sha"], a["labels_pi_sha"], hx(Path(__file__).read_bytes()))',
                             ["refuses_unsealing_line_without_token"]),
    "G05_up_R2_sha_dropped": (UP_NEED, 'up_need = (UNSEAL_TOKEN, a["labels_pi_sha"], hx(Path(__file__).read_bytes()))',
                              ["refuses_unsealing_line_without_R2_sha"]),
    "G06_up_PI_sha_dropped": (UP_NEED, 'up_need = (UNSEAL_TOKEN, a["labels_r2_sha"], hx(Path(__file__).read_bytes()))',
                              ["refuses_unsealing_line_without_PI_sha"]),
    "G07_up_script_sha_dropped": (UP_NEED, 'up_need = (UNSEAL_TOKEN, a["labels_r2_sha"], a["labels_pi_sha"])',
                                  ["refuses_unsealing_line_without_script_sha"]),
    # label-free overlap construction before the key read (CC-391 B3)
    "P01_construction_after_labels": (
        "    pre = prepare(w, pos)\n    key = read_key(a, P)\n    t = key_targets(key, r2a, ov, P)\n"
        "    pi, r2 = read_labels(a, seen)\n",
        "    key = read_key(a, P)\n    t = key_targets(key, r2a, ov, P)\n    pi, r2 = read_labels(a, seen)\n"
        "    pre = prepare(w, pos)\n", [NONFIN]),
    "P02_finiteness_unchecked": ("if not np.all(np.isfinite(np.asarray(vals, float))):", GUARD, [NONFIN]),
    # score refusals, gate conditions and the fault rule (kappa pattern; CC-372 rulings 1, 2, 4, 8; CC-374 ruling 6)
    "S01_out_exists_allowed": ('if Path(a["out"]).exists():', GUARD,
                               ["refuses_out_exists_before_labels", "second_run_refused_FAULT_type_label_free"]),
    "S02_sha_argument_unchecked": ('if not all(re.fullmatch(r"[0-9a-f]{64}", x) for x in shas):', GUARD,
                                   ["refuses_sha_argument_not_64_hex"]),
    "S03_shas_not_distinct": ("if shas[0] == shas[1]:", GUARD, ["refuses_sha_arguments_not_distinct"]),
    "S04_pi_sha_not_PI1_SHA": ('if a["labels_pi_sha"] != P["pi1_sha"]:', GUARD,
                               ["refuses_pi_sha_not_PI1_SHA_before_labels", "main_maps_score_argv_to_a_label_free_fault"]),
    "S05_public_pins_unchecked": ('if any(hx(b[k]) != P[k + "_sha"] for k in b):', GUARD,
                                  ["refuses_base_assignment_pin", "refuses_r2_assignment_pin", "refuses_overlap_list_pin"]),
    "S06_overlap_not_the_R2_screens": ('if len(ov) != P["n_images"] or ov != {Path(s["image"]).stem for s in '
                                       'r2a["screens"]}:', GUARD, ["refuses_overlap_list_not_the_R2_screens"]),
    "S07_R2_end_line_unchecked": ("if end < 0:", GUARD, ["refuses_without_R2_session_end_line"]),
    "S08_unsealing_line_unchecked": ("if un <= end:", GUARD,
                                     ["refuses_without_unsealing_line", "refuses_unsealing_line_before_R2_end"]),
    "S09_freeze_sha_unchecked": ('if fsha != P["freeze_sha"]:', GUARD, ["refuses_freeze_sha_not_pinned"]),
    "S10_world_pins_unchecked": ('if w["pins"] != fz["pins"]:', GUARD, ["refuses_world_pins_not_FREEZE_pins"]),
    "S11_key_sha_unchecked": ('if hx(kb) != P["key_sha"]:', GUARD, ["refuses_key_sha_before_labels"]),
    "S12_label_sha_unchecked": ('if (hx(lp), hx(lr)) != (a["labels_pi_sha"], a["labels_r2_sha"]):', GUARD,
                                ["refuses_label_sha_mismatch"]),
    "S13_PI_qid_outside_base": ('if not set(pi) <= {q["qid"] for s in base["screens"] for q in s["q"]}:', GUARD,
                                ["refuses_PI_qid_outside_base"]),
    "S14_R2_qid_outside_r2": ('if not set(r2) <= {q["qid"] for s in r2a["screens"] for q in s["q"]}:', GUARD,
                              ["refuses_R2_qid_outside_R2_assignment"]),
    "S15_R2_part1_unchecked": ('if len(rq1) != P["n_p1"] or any(q not in key or key[q]["part"] != 1 or key[q]["image"] '
                               'not in ov for q in rq1):', GUARD, ["refuses_R2_part1_count_before_labels"]),
    "S16_target_count_unchecked": ('if len(t) != P["n_target"]:', GUARD, ["refuses_overlap_targets_count_before_labels"]),
    "S17_PI_incomplete_allowed": ("if not t <= pi.keys():", GUARD, ["refuses_PI_incomplete_on_overlap"]),
    "S18_R2_incomplete_allowed": ("if not t <= r2.keys():", GUARD,
                                  ["refuses_R2_incomplete_on_overlap", "after_labels_fault_prints_stage_and_writes_nothing"]),
    "S19_fault_prints_message": ('print(f"FAULT {type(e).__name__} {', 'print(f"FAULT {type(e).__name__}: {e} {',
                                 ["second_run_refused_FAULT_type_label_free"]),
    "S20_stage_never_after_labels": ('seen["labels"] = True', 'seen["labels"] = False',
                                     ["after_labels_fault_prints_stage_and_writes_nothing"]),
    "S21_main_argv_keys_unmapped": ('zip((x[2:].replace("-", "_") for x in SCORE_ARGS)', "zip((x[2:] for x in SCORE_ARGS)",
                                    ["main_maps_score_argv_to_a_label_free_fault"]),
    # custody
    "C01_part1_result_not_refused": ('return ak.refused(p) or (p not in ak._OK and any(d in p.replace(os.sep, "/") for d '
                                     'in DENY_EXTRA))', "return ak.refused(p)",
                                     ["custody_refuses_key_labels_and_part1_result"]),
    "C02_ok_list_kept": ("        ak._OK.clear()\n", "        pass\n", ["ok_list_cleared_after_score"]),
    "C03_hook_off": ("isinstance(args[0], (str, bytes, os.PathLike)) and refused(args[0]):",
                     "isinstance(args[0], (str, bytes, os.PathLike)) and False:", ["custody_hook_blocks_open_of_key_json"]),
    "C04_key_path_kept_after_key_read": ("ak._OK.discard(path)", "ak._OK.add(path)", ["ok_list_empty_after_key_fault"]),
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
