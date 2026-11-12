#!/usr/bin/env python3
"""Mutant harness for scripts/a_cert/a_cert_vp.py: addendum VP v1.1 §V.7 mutants, the coder brief's list, and one or
more mutants per registered rule and custody guard. Runs a_cert_mutants.main unchanged with its SRC and M pointed here
(same loader, KILLED rule and mutants_result.json schema). Synthetic fixtures only.
Usage: <venv python> -I -B a_cert_vp_mutants.py <scratch dir outside the repo>
Each target is one whole source line and must occur exactly once (else BAD_TARGET)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a_cert_mutants as am  # noqa: E402

M = {
    # coder brief
    "M01_masking_seed_changed": [("SEED_MASK = 20261115\n", "SEED_MASK = 20261116\n")],
    "M02_instance_gold_loaded_before_freeze": [("        fz = v_freeze_core(w)\n",
                                                "        load_inst(P, w[\"ids\"])\n        fz = v_freeze_core(w)\n")],
    "M03_certificate_from_full_gold": [("    n = Counter(c for j in pick for c in refs_i[j])\n",
                                        "    n = Counter(c for j in range(len(refs_i)) for c in refs_i[j])\n")],
    "M04a_V1_error_bound_changed": [("V1_ERR = Fr(1, 20)\n", "V1_ERR = Fr(1, 10)\n")],
    "M04b_V1_evaluability_bound_changed": [("V1_MIN_CERT, V1_MIN_PAIRS, V1_MIN_OTHER = 72, 5, 72\n",
                                            "V1_MIN_CERT, V1_MIN_PAIRS, V1_MIN_OTHER = 71, 5, 72\n")],
    "M05_pair_union_not_intersection": [
        ("    return [pos[i] for i in sorted(set(pw[\"caps\"][A]) & set(pw[\"caps\"][B])) if i in pos]\n",
         "    return [pos[i] for i in sorted(set(pw[\"caps\"][A]) | set(pw[\"caps\"][B])) if i in pos]\n")],
    "M06a_part_P_written_into_XM3600_input": [
        ("        out = p_score_core(P, _e1(), json.loads(Path(ROOT, P[\"v_result\"]).read_text(encoding=\"utf-8\")))\n",
         "        out = p_score_core(P, _e1(), json.loads(Path(ROOT, P[\"v_result\"]).read_text(encoding=\"utf-8\")))\n"
         "        write_atomic(ROOT / \"data/results/a_cert/freeze/P_w_star.json\", {\"w_star\": 0.5})\n")],
    "M06b_part_P_written_into_OC1_input": [
        ("        out = p_score_core(P, _e1(), json.loads(Path(ROOT, P[\"v_result\"]).read_text(encoding=\"utf-8\")))\n",
         "        out = p_score_core(P, _e1(), json.loads(Path(ROOT, P[\"v_result\"]).read_text(encoding=\"utf-8\")))\n"
         "        write_atomic(ROOT / \".session_backup/2026-10-27/a1_precheck/raw/P_w0.json\", {\"w0\": 0.2})\n")],
    "M07a_POST_HOC_label_missing_on_rows": [
        ("    rec = {\"label\": P_LABEL, \"comparison\": f\"{method} vs {base}\", \"k\": k, \"image_set\": row[\"family\"],\n",
         "    rec = {\"comparison\": f\"{method} vs {base}\", \"k\": k, \"image_set\": row[\"family\"],\n")],
    "M07b_POST_HOC_label_text_lost": [("P_LABEL = \"POST HOC; truth already scored by the paper\"\n",
                                       "P_LABEL = \"post hoc\"\n")],
    # addendum §V.7
    "S01_k_ignored_in_c": [("    return (1 - w) / (k * w)\n", "    return (1 - w) / (2 * w)\n")],
    "S02_truth_from_drawn_references": [("    top = top_gold(w[\"refs\"], inst)\n",
                                         "    top = [g[\"kp\"] for g in golds2[0]]\n")],
    "S03_freeze_may_open_instance_gold": [("    if MODE[\"m\"] == \"v-freeze\" and \"instance_gold\" in low:\n",
                                           "    if False:\n")],
    "S04a_freeze_forms_five_reference_union": [("    for k in (1, 2, 3):\n", "    for k in (1, 2, 3, 5):\n")],
    "S04b_five_union_guard_removed": [("    if MODE[\"m\"] == \"v-freeze\" and len(pick) >= len(refs_i):\n",
                                       "    if False:\n")],
    "S05_certified_set_recomputed_in_score": [
        ("    units = [{\"pair\": u[\"pair\"], \"verdict\": u[\"verdict\"][W0S]} for u in u2]\n",
         "    units = [{\"pair\": u[\"pair\"], \"verdict\": \"CERTIFIED\" if (u[\"dmin\"][W0S] or 0) > 0 else "
         "\"NOT CERTIFIED\"} for u in u2]\n")],
    "S06_tie_counted_as_right": [
        ("    return p_better is not None and p_worse is not None and p_better - p_worse > 0\n",
         "    return p_better is not None and p_worse is not None and p_better - p_worse >= 0\n")],
    # seeds and registered constants
    "X01_reference_draw_seed": [("SEED_REF = 20261114\n", "SEED_REF = 20261115\n")],
    "X02_V3_bootstrap_seed": [("SEED_V3 = 20261116\n", "SEED_V3 = 20261117\n")],
    "X03_COCO_K2_bootstrap_seed": [("SEED_K2 = 20261113\n", "SEED_K2 = 20261116\n")],
    "X04_halves_seed": [("SEED_HALF = 20261111\n", "SEED_HALF = 20261112\n")],
    "X05_COCO_K2_gain_changed": [("K2_GAIN = Fr(1, 20)\n", "K2_GAIN = Fr(1, 25)\n")],
    "X06_cov5_strict_prefix_rule": [("    ok = 20 * np.cumsum(f) <= m\n", "    ok = 20 * np.cumsum(f) < m\n")],
    "X07_V2_alpha_changed": [("V2_ALPHA = Fr(1, 40)\n", "V2_ALPHA = Fr(1, 20)\n")],
    "X08_abstain_counted_as_certified": [("    ce = [u for u in units if u[\"verdict\"] == \"CERTIFIED\"]\n",
                                          "    ce = [u for u in units if u[\"verdict\"] in (\"CERTIFIED\", \"ABSTAIN\")]\n")],
    "X09_V1_pair_majority_rule_dropped": [("    major = sorted(p for p in n_p if 2 * f_p[p] > n_p[p])\n",
                                           "    major = []\n")],
    "X10_v4a_fault_removed": [("        raise Fault(\"§V.4a: a C-ref certificate at w = 0\")\n", "        pass\n")],
    # Part P rules
    "X11_Pb_I0_cap_ignored": [("    return max(0.0, b - cell[\"I0\"]) if use_i0 else b\n", "    return b\n")],
    "X12_Pb_floor_refutation_dropped": [
        ("        bad = [c for c in \"ABS\" if pc[c][\"I0\"] > math.floor(beta_Bk(pc[c], w, a_s, 5))]\n",
         "        bad = []\n")],
    "X13_not_certified_without_tail": [("                      (\"\" if c == n else f\"; {NOT_CERT_TAIL}\")\n",
                                        "                      \"\"\n")],
    "X14_KV1_ignored_in_part_P": [("    kv1 = vres.get(\"registered\", {}).get(\"V1\") == \"FAIL\"\n", "    kv1 = False\n")],
    "X15_matcher_gate_always_passes": [("        ok = ok and got == want\n", "        ok = True\n")],
    # custody and the fault rule
    "X16_gt_cache_guard_removed": [
        ("    if low.endswith(\"/gt_cache.json\") and not (MODE[\"m\"] == \"p-score\" and MODE[\"gt\"]):\n",
         "    if False:\n")],
    "X17_OC1_raw_guard_removed": [("    if \"a1_precheck/raw\" in low:\n", "    if False:\n")],
    "X18_part_P_write_restriction_removed": [
        ("        if write and not (ok and (low == ok or low.startswith(ok + \"/\"))):\n", "        if False:\n")],
    "X19_score_without_freeze_pin": [
        ("        fz, fsha = ac.pinned_freeze({\"freeze\": str(Path(P[\"out\"], \"freeze\", \"FREEZE_V.json\")), "
         "\"log\": P[\"log\"]})\n",
         "        fz, fsha = json.loads(Path(ROOT, P[\"out\"], \"freeze\", \"FREEZE_V.json\").read_text(encoding=\"utf-8\")), "
         "\"x\"\n")],
    "X20_fault_prints_a_statistic": [("    print(f\"FAULT {type(e).__name__}\")\n",
                                      "    print(f\"FAULT {type(e).__name__}: {e}\")\n")],
    "X21_second_pass_allowed": [("    if target.exists():\n", "    if False:\n")],
    "X22_KV3_ignored": [("    if len(prev) >= 2:\n", "    if False:\n")],
    # CC-347 W1-W4
    "W1_V2_at_cross_fitted_floor_dropped": [("                    **xfit_v2(hu, info, w0h, beta)}\n",
                                             "                    }\n")],
    "W2a_baseline_direction_counted_certified": [("    c, n = cm, len(us)\n", "    c, n = cm + cb, len(us)\n")],
    "W2b_Pb_baseline_direction_called_certified": [
        ("    cert = vi[\"verdict\"] == \"CERTIFIED\" and vi[\"better\"] == \"A\"\n",
         "    cert = vi[\"verdict\"] == \"CERTIFIED\"\n")],
    "W3_same_image_V2_x_top_under_drawn_gold": [
        ("        xs = x_top(ms, gold, A, B, v[\"better\"], T, idx)\n",
         "        xs = x_top(ms, gold, A, B, v[\"better\"], [g[\"kp\"] for g in gold], idx)\n")],
    "W4_units_include_images_without_instance_entry": [
        ("    ids = sorted(set().union(*(set(pw[\"caps\"][s]) for s in names)) & set(pw[\"inst\"]))  # E1's kept ids "
         "(CC-347 W4)\n",
         "    ids = sorted(set().union(*(set(pw[\"caps\"][s]) for s in names)))\n")],
}

if __name__ == "__main__":
    am.SRC = Path(__file__).resolve().parent / "a_cert_vp.py"
    am.M = M
    sys.exit(am.main())
