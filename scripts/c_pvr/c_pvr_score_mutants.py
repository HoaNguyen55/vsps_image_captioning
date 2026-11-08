#!/usr/bin/env python3
"""Mutant harness for the S16 laptop scorer files (pattern of scripts/a_m1/a_m1_mutants.py and c_pvr_mutants.py):
c_pvr_cay.py (T1-REP §5), c_pvr_cm.py (T1-ANALYSIS v1.1 C-M1 / C-M2), c_pvr_score.py (score --tier 1).
Usage: ~/.venvs/c_pvr/bin/python -I -B c_pvr_score_mutants.py <scratch dir outside /mnt>
Each mutant replaces exact strings (each must occur once) in one file and runs that file's own `selftest` on the
mutated source, executed with __file__ = the original path, so pins and imports resolve unchanged (the other two
files load unmutated behind their pins). Each unmutated file runs first and must print 'selftest ok'. KILLED = exit
!= 0 and a named selftest case FAILED; any other exit != 0 is CRASH, which is not a kill. Synthetic data only."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOADER = ("import sys; src, orig = sys.argv[1:3]; sys.argv = [orig, 'selftest']; "
          "ns = {'__name__': '__main__', '__file__': orig}; "
          "exec(compile(open(src, encoding='utf-8').read(), orig, 'exec'), ns)")

M = {  # name: (file, old, new)
    # 'cây' rule (T1-REP §5)
    "cay_K_any_match": ("c_pvr_cay.py", "ign += hit in k", "ign += hit is not None"),
    "cay_shortest_key": ("c_pvr_cay.py", "key=len, default=None)", "key=lambda x: -len(x), default=None)"),
    "cay_no_space_check": ("c_pvr_cay.py", 'if s[m.end():q] != " " or not LETTER.match(s, q):', "if not LETTER.match(s, q):"),
    "cay_no_key_boundary": ("c_pvr_cay.py", ' and not re.match(r"\\w", s[q + len(key):q + len(key) + 1])', ""),
    "cay_rule5_any": ("c_pvr_cay.py", "gone = occ > 0 and ign == occ", "gone = ign > 0"),
    "cay_no_nfc": ("c_pvr_cay.py", 's = unicodedata.normalize("NFC", text).lower()', "s = text.lower()"),
    "cay_no_lower": ("c_pvr_cay.py", 's = unicodedata.normalize("NFC", text).lower()', 's = unicodedata.normalize("NFC", text)'),
    "cay_K_has_cay": ("c_pvr_cay.py", 'if c == CAY and n != CAY)', "if c == CAY)"),
    "cay_inside_word": ("c_pvr_cay.py", 'OCC = re.compile(r"(?<!\\w)cây(?!\\w)")', 'OCC = re.compile(r"cây")'),
    # C-M1 / C-M2 (T1-ANALYSIS §4-§6; CC-292r2)
    "cm_g2_before_g1": ("c_pvr_cm.py",
                        '        if g1 and name == "A7-PVR" and or_ci[0] <= 1 <= or_ci[1]:\n            gate = "G1"\n'
                        '        elif holds0(dci) or bad.mean() > 0.01:\n            gate = "G2"\n',
                        '        if holds0(dci) or bad.mean() > 0.01:\n            gate = "G2"\n'
                        '        elif g1 and name == "A7-PVR" and or_ci[0] <= 1 <= or_ci[1]:\n            gate = "G1"\n'),
    "cm_g2_no_zero_clause": ("c_pvr_cm.py", "        elif holds0(dci) or bad.mean() > 0.01:\n", "        elif holds0(dci):\n"),
    "cm_g1_open_interval": ("c_pvr_cm.py", "or_ci[0] <= 1 <= or_ci[1]", "or_ci[0] < 1 < or_ci[1]"),
    "cm_per_ratio_drop": ("c_pvr_cm.py", '\n    keep = ~(r["A7-PVR"]["_bad"] | r["A1-A7"]["_bad"] | r["A1-PVR"]["_bad"])',
                          '\n    keep = ~r["A7-PVR"]["_bad"]'),
    "cm_union_is_fault": ("c_pvr_cm.py", "    p_check(ps, int(keep.sum()))\n",
                          "    p_check(ps, int(keep.sum()))\n    if keep.mean() < 0.99:\n        raise Fault('union')\n"),
    "cm_p2_one_sided": ("c_pvr_cm.py", "return min(1.0, 2 * min(int((d <= 0).sum()), int((d >= 0).sum())) / len(d))",
                        "return min(1.0, min(int((d <= 0).sum()), int((d >= 0).sum())) / len(d))"),
    "cm_holm_bonferroni": ("c_pvr_cm.py", "if ps[j] > alpha / (len(ps) - k):", "if ps[j] > alpha / len(ps):"),
    "cm_pct_90": ("c_pvr_cm.py", "return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]",
                  "return [float(np.percentile(v, 5)), float(np.percentile(v, 95))]"),
    "cm_e2b_default_seed": ("c_pvr_cm.py", "e2b.boot(rows, len(rows), seed=SEED, B=B)", "e2b.boot(rows, len(rows), B=B)"),
    "cm_B_5000": ("c_pvr_cm.py", "SEED, B, ALPHA = 20261102, 10_000, 0.05", "SEED, B, ALPHA = 20261102, 5_000, 0.05"),
    "cm_accounting_sign": ("c_pvr_cm.py", 'hat = top / (top + hm7 - km * na * (rho["PVR-drop"] - rho["A7"]))',
                           'hat = top / (top + hm7 + km * na * (rho["PVR-drop"] - rho["A7"]))'),
    "cm_bounds_swapped": ("c_pvr_cm.py", "base - s8 / n8 + sb * np.minimum(0, c), base + sp / np_ + sb * np.maximum(0, c)",
                          "base - s8 / n8 + sb * np.maximum(0, c), base + sp / np_ + sb * np.minimum(0, c)"),
    "cm_band_inner": ("c_pvr_cm.py", "band = [float(np.percentile(blo, 2.5)), float(np.percentile(bhi, 97.5))]",
                      "band = [float(np.percentile(blo, 97.5)), float(np.percentile(bhi, 2.5))]"),
    "cm_placebo_flipped": ("c_pvr_cm.py", '"PLACEBO_CONSISTENT" if ci[0] <= 0 <= ci[1] else "PLACEBO_INCONSISTENT"',
                           '"PLACEBO_INCONSISTENT" if ci[0] <= 0 <= ci[1] else "PLACEBO_CONSISTENT"'),
    "cm_k4_for_g2": ("c_pvr_cm.py", '    if m["gate"] == "G1":\n        return "K4"', '    if m["gate"]:\n        return "K4"'),
    "cm_fault_before_not_run": ("c_pvr_cm.py",
                                'if miss := {a: missing[a] for a in ("A1", "A7", "PVR-drop") if missing.get(a)}:  # §9.2',
                                'if not t1rep_fault and (miss := {a: missing[a] for a in ("A1", "A7", "PVR-drop") if missing.get(a)}):  # §9.2'),
    "cm_post_hoc_keeps_sentence": ("c_pvr_cm.py", "        main = []\n        for k in (\"C-M1\", \"C-M2\"):\n",
                                   "        for k in (\"C-M1\", \"C-M2\"):\n"),
    "cm_post_hoc_no_scrub": ("c_pvr_cm.py", 'res[k] = {**scrub(strip(res[k])), "label": "POST_HOC",',
                             'res[k] = {**strip(res[k]), "label": "POST_HOC",'),
    "cm_scrub_keeps_case": ("c_pvr_cm.py", 'if k != "case" and not (isinstance(v, str) and LABELS.search(v))}',
                            'if not (isinstance(v, str) and LABELS.search(v))}'),
    # CC-293 N1 hand mutants
    "g2_holds0_open": ("c_pvr_cm.py", "    return not (ci[0] > 0 or ci[1] < 0)\n", "    return ci[0] < 0 < ci[1]\n"),
    "g1_wholly_below": ("c_pvr_cm.py", 'if g1 and name == "A7-PVR" and or_ci[0] <= 1 <= or_ci[1]:',
                        'if g1 and name == "A7-PVR" and or_ci[1] >= 1:'),
    "g2_strata_no_zero": ("c_pvr_cm.py", 'gate = "G2" if holds0(dci) or bad.mean() > 0.01 else None',
                          'gate = "G2" if holds0(dci) else None'),
    "g_guard_point": ("c_pvr_score.py", '"passes": lo > -DELTA_C,', '"passes": float(sum(x.sum() for x in d) / n) > -DELTA_C,'),
    "h_created_vs_carried": ("c_pvr_score.py", '"created": set() if masks is None else found - units,',
                             '"created": set() if masks is None else found - carried,'),
    "cm_fallback_keep": ("c_pvr_cm.py", 'pvr = variant or "PVR-drop"', 'pvr = variant or "PVR-keep"'),
    "cm_kplus_gets_g1": ("c_pvr_cm.py", 'plus = ratios(np.r_[hp, dp], np.c_[thp.T, tdp.T], None, g1=False)',
                         'plus = ratios(np.r_[hp, dp], np.c_[thp.T, tdp.T], or_ratio["ci"])'),
    "cm_p_holm_unadjusted": ("c_pvr_cm.py", '"p_holm": min(1.0, 2 * min(ps))', '"p_holm": min(ps)'),
    "cm_degraded_dropped": ("c_pvr_cm.py", '(("DEGRADED", degraded), ("INCONCLUSIVE", inconclusive))',
                            '(("INCONCLUSIVE", inconclusive),)'),
    # score --tier 1 (prereg §3, §5, §12; T1-GUARD; T1-REP §1-§6; S11 §10.3)
    "sc_survival_no_removal": ("c_pvr_score.py", '"kept": units & found,', '"kept": units,'),
    "sc_rebuild_never_empties": ("c_pvr_score.py", "CP.rebuild(dc, masks[n])", "CP.rebuild(dc, masks[n], emptied=False)"),
    "sc_a7_is_pvr": ("c_pvr_score.py", 'return CP.a7_masks(qid, rec["PVR-drop"]["masks"])', 'return rec["PVR-drop"]["masks"]'),
    "sc_labels_swapped": ("c_pvr_score.py", '"REJECTED" if k else "UNCERTAIN" if d else "SUPPORTED"',
                          '"UNCERTAIN" if k else "REJECTED" if d else "SUPPORTED"'),
    "sc_labels_no_count_check": ("c_pvr_score.py",
                                 '\n          and all((r["yes"], r["no"], r["maybe"] + r["parse_fail"] + r["cap_hits"], r["cap_hits"]) == want for r in (rd, rk)))',
                                 ")"),
    "sc_unit_label_last": ("c_pvr_score.py",
                           'return next(lab for p, lab in zip(dc["props"], labs) if p["kind"] == "obj" and c in p["classes"])',
                           'return [lab for p, lab in zip(dc["props"], labs) if p["kind"] == "obj" and c in p["classes"]][-1]'),
    "sc_sesoi_floor_1_5": ("c_pvr_score.py", "SESOI_FLOOR, SESOI_FRAC, HEADROOM = 1.0, 0.25, 2.0",
                           "SESOI_FLOOR, SESOI_FRAC, HEADROOM = 1.5, 0.25, 2.0"),
    "sc_sesoi_frac_0_5": ("c_pvr_score.py", "SESOI_FLOOR, SESOI_FRAC, HEADROOM = 1.0, 0.25, 2.0",
                          "SESOI_FLOOR, SESOI_FRAC, HEADROOM = 1.0, 0.5, 2.0"),
    "sc_headroom_le": ("c_pvr_score.py", '"headroom_stop": p["A12"] - p["A1"] < HEADROOM', '"headroom_stop": p["A12"] - p["A1"] <= HEADROOM'),
    "sc_tie_full_sesoi": ("c_pvr_score.py", '< sesoi / 2:', '< sesoi:'),
    "sc_dR_nonstrict": ("c_pvr_score.py", '"dR": var[v]["dR_lo"] > -DELTA_R', '"dR": var[v]["dR_lo"] >= -DELTA_R'),
    "sc_dC_nonstrict": ("c_pvr_score.py", 'var[v]["dC_lo"] > -DELTA_C', 'var[v]["dC_lo"] >= -DELTA_C'),
    "sc_go_strict": ("c_pvr_score.py", 'var[v]["dA8"] >= sesoi', 'var[v]["dA8"] > sesoi'),
    "sc_harm_on_HW0": ("c_pvr_score.py", 'if hw not in ("HW-3", "HW-0"):', 'if hw != "HW-3":'),
    "sc_harm_verb_point": ("c_pvr_score.py", '"reduced" if pa1["ci"][0] > 0', '"reduced" if pa1["point"] > 0'),
    "sc_hw2_point": ("c_pvr_score.py", 'hw2 = a1a0["ci"][1] < 0', 'hw2 = a1a0["point"] < 0'),
    "sc_family_A12": ("c_pvr_score.py", 'FAMILY = ("A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A9", "A10", "A11")',
                      'FAMILY = ("A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A9", "A10", "A11", "A12")'),
    "sc_family_keeps_cut": ("c_pvr_score.py", "    fam = [a for a in FAMILY if a in arms]\n", "    fam = list(FAMILY)\n"),
    "sc_vi_letters_f": ("c_pvr_score.py", 'set("abcdeghiklmnopqrstuvxyđăâêôơư")', 'set("abcdefghiklmnopqrstuvxyđăâêôơư")'),
    "sc_vi_specific_all": ("c_pvr_score.py", '"".join(c for c in VI_LETTERS if c not in "abcdeghiklmnopqrstuvxy")',
                           '"".join(VI_LETTERS)'),
    "sc_truncation_not_eos": ("c_pvr_score.py", 'sum(f == "length" for f in gen)', 'sum(f != "eos" for f in gen)'),
    "sc_est_5pct": ("c_pvr_score.py", "if strict and ((~ok).sum() > 0.01 * len(reps)", "if strict and ((~ok).sum() > 0.05 * len(reps)"),
    "sc_guard_unstratified": ("c_pvr_score.py", "    reps = sum(ws) / n\n",
                              "    reps = (lambda y: rng.multinomial(len(y), [1 / len(y)] * len(y), size=CM.B) @ y)(np.concatenate(d)) / n\n"),
    "sc_per_set_ci_unscaled": ("c_pvr_score.py", '"ci": CM.pct(w / len(x)), "label": "descriptive"', '"ci": CM.pct(w), "label": "descriptive"'),
    "sc_split_any_compound": ("c_pvr_score.py", 'out |= {"split"} if i1 - i0 > 1 else set()', 'out |= {"split"} if i1 - i0 > 0 else set()'),
    "sc_classifier_no_boundary": ("c_pvr_score.py", 'CLF_RX = re.compile(r"(?<!\\w)(?:"', 'CLF_RX = re.compile(r"(?:"'),
    "sc_fallback_keep_from_drop": ("c_pvr_score.py", 'cell[f"KR|{stat(c)}"] += mk[carry[0]]', 'cell[f"KR|{stat(c)}"] += md[carry[0]]'),
    "sc_fallback_off": ("c_pvr_score.py", '    if side["label_mismatch_images"]:  # CC-293 N2', "    if False:  # CC-293 N2"),
    "sc_job_done_off": ("c_pvr_score.py", 'if Path(x.sums).name == "SHA256SUMS_tier1":', "if False:"),
    "sc_cider_no_A0": ("c_pvr_score.py", 'need = [(XM, "A0")] + [', "need = [] + ["),
    "sc_rerun_cm_unstamped": ("c_pvr_score.py", "cm.update(rerun=res[\"rerun\"], label=f\"{cm['label']}; {res['rerun']}\")",
                              'cm.update(rerun=res["rerun"])'),
    "sc_rerun_any_id": ("c_pvr_score.py", 'if not re.fullmatch(r"OPS-[A-Za-z0-9_.:-]+", x.rerun_of):', "if False:"),
    "sc_hw3_no_datastore": ("c_pvr_score.py", '"HW-3": "With this datastore (KTVIC and OpenViIC training captions), verifying',
                            '"HW-3": "With this datastore, verifying'),
    "sc_degrade_ge": ("c_pvr_score.py", '"DEGRADED": m > DEGRADE * len(dec)', '"DEGRADED": m >= DEGRADE * len(dec)'),
    "sc_no_torn_check": ("c_pvr_score.py", '    if b and not b.endswith(b"\\n"):\n        fault(f"{rel}: torn last line")\n', ""),
    "sc_no_tman_check": ("c_pvr_score.py", "    if sha(man) != tman:\n", "    if False:\n"),
    "sc_no_emptied_check": ("c_pvr_score.py", 'if sc == "" and sum(u["emptied"] for u in sv) != rec[a]["emptied"]:', "if False:"),
    "sc_no_demo_ids_check": ("c_pvr_score.py", 'if any(rec[a]["demo_ids"] != dids for a in DEMO_ARMS):', "if False:"),
    "sc_rule_i_lower_end": ("c_pvr_score.py", 'idn["OR_PVR-drop/OR_A7"]["ci"][1] < 1)', 'idn["OR_PVR-drop/OR_A7"]["ci"][0] < 1)'),
    "sc_rule_ii_no_direction": ("c_pvr_score.py", 'a7["point"] > 0 and a7["holm_reject"]', 'a7["holm_reject"]'),
    "sc_post_hoc_inverted": ("c_pvr_score.py", "post_hoc = sha((root / APPENDIX[0]).read_bytes()) != APPENDIX[1]",
                             "post_hoc = sha((root / APPENDIX[0]).read_bytes()) == APPENDIX[1]"),
    "sc_primary_unknown_wrong": ("c_pvr_score.py", '{"primary": est(get, D(P, v, "A8"), True)', '{"primary": est(get, D(PW, v, "A8"), True)'),
    "sc_P_over_all_mentions": ("c_pvr_score.py",
                               'P = lambda a, sc="": lambda S: 100 * S("Hp" + sfx(a, sc)) / (S("Hp" + sfx(a, sc)) + S("Hm" + sfx(a, sc)))',
                               'P = lambda a, sc="": lambda S: 100 * S("Hp" + sfx(a, sc)) / S("n" + sfx(a, sc))'),
    "sc_cay_scorer_is_primary": ("c_pvr_score.py", "return frozenset(CAY.apply(set(primary(text)), text, nouns, k)[0])",
                                 "return primary(text)"),
    "sc_identity_check_inverted": ("c_pvr_score.py", "if c * r1 / (c * r1 + (1 - c) * f1) != F(ka, ka + kp):",
                                   "if c * r1 / (c * r1 + (1 - c) * f1) == F(ka, ka + kp):"),
    "sc_cm_runs_when_pending": ("c_pvr_score.py", 'if "variant_status" not in dec or dec["variant_status"].startswith("NOT_DECIDED"):',
                                "if False:"),
    # CC-293r2 W4: the no-CIDEr path
    "w4_cm_runs_when_not_decided": ("c_pvr_score.py", 'dec["variant_status"].startswith("NOT_DECIDED"):  # T1-ANALYSIS §1 order',
                                    'dec["variant_status"].startswith("PENDING"):  # T1-ANALYSIS §1 order'),
    "w4_no_cider_under_job_done": ("c_pvr_score.py", 'if x.no_cider and Path(x.sums).name == "SHA256SUMS_tier1":', "if False:"),
    "w4_status_pending": ("c_pvr_score.py", 'f"NOT_DECIDED: no CIDEr-VI input ({no_cider})"', 'f"PENDING: no CIDEr-VI input ({no_cider})"'),
    "w4_headroom_after_not_decided": ("c_pvr_score.py",
                                      '    out["decision"] = ("STOP (headroom, §12 ii)" if out["headroom_stop"] else\n'
                                      '                       "NOT_DECIDED (§6.3 variant: no CIDEr-VI input)" if out["variant_status"].startswith("NOT_DECIDED") else\n',
                                      '    out["decision"] = ("NOT_DECIDED (§6.3 variant: no CIDEr-VI input)" if out["variant_status"].startswith("NOT_DECIDED") else\n'
                                      '                       "STOP (headroom, §12 ii)" if out["headroom_stop"] else\n'),
    "w4_exactly_one_off": ("c_pvr_score.py", "if bool(x.cider) == bool(x.no_cider) or bool(x.cider) != bool(x.cider_sha):", "if False:"),
    "w4_both_flags_allowed": ("c_pvr_score.py", "if bool(x.cider) == bool(x.no_cider) or", "if not (x.cider or x.no_cider) or"),
    "w4_sha_optional": ("c_pvr_score.py", " or bool(x.cider) != bool(x.cider_sha):  # CC-293r2 W4 (a)", ":  # CC-293r2 W4 (a)"),
    "w4_guard_record_none": ("c_pvr_score.py", 'xm["guard_G1"] = dC if cider else f"NOT_COMPUTED: no CIDEr-VI input ({x.no_cider})"',
                             'xm["guard_G1"] = dC'),
    "nh_nonfinite_ok": ("c_pvr_score.py", "type(y) in (int, float) and math.isfinite(y) and 0 <= y <= 1000",
                        "type(y) in (int, float) and 0 <= y <= 1000 or y != y"),
    "nh_no_upper": ("c_pvr_score.py", "math.isfinite(y) and 0 <= y <= 1000", "math.isfinite(y) and 0 <= y"),
    "nh_no_lower": ("c_pvr_score.py", "math.isfinite(y) and 0 <= y <= 1000", "math.isfinite(y) and y <= 1000"),
    "nh_bool_ok": ("c_pvr_score.py", "type(y) in (int, float) and math.isfinite(y)", "isinstance(y, (int, float)) and math.isfinite(y)"),
    # CC-293r2 N-A / N-B: the round-2 hand mutants that survived
    "w1_labels_no_placebo": ("c_pvr_cm.py", 'LABELS = re.compile(r"IDENTIFIED|E1_|OVERID_|SIGN_|PLACEBO_")',
                             'LABELS = re.compile(r"IDENTIFIED|E1_|OVERID_|SIGN_")'),
    "nf_reason_dropped": ("c_pvr_cm.py", '"label": "POST_HOC",\n                          "reason": ', '"label": "POST_HOC",\n                          "why": '),
    "w2_fc_status_swapped": ("c_pvr_score.py", 'for h, s0 in (("Hp", "present"), ("Hm", "absent")):', 'for h, s0 in (("Hp", "absent"), ("Hm", "present")):'),
    "w2_pf_numerator_hm": ("c_pvr_score.py", 'PF = lambda f: lambda a, sc="": lambda S: 100 * S(f"FC|{f}|Hp|{a}") /',
                           'PF = lambda f: lambda a, sc="": lambda S: 100 * S(f"FC|{f}|Hm|{a}") /'),
    "w2_demo_toks_k3": ("c_pvr_score.py", 'for d in q["ranked"][:CP.K]})', 'for d in q["ranked"][:3]})'),
    "w2_cap_toks_wrong_arm": ("c_pvr_score.py", 'seg["cap"].get((a, i))', 'seg["cap"].get(("A8", i))'),
    "w2_conflicts_never": ("c_pvr_score.py", 'side["unit_label_conflicts"] += len({lab[j] for j in carry}) > 1',
                           'side["unit_label_conflicts"] += len({lab[j] for j in carry}) > 2'),
    "n3_note_never": ("c_pvr_score.py", "    if (~ok).sum() > 0.01 * len(reps):  # only reachable", "    if False:  # only reachable"),
    "seg_swallow_pin_both": ("c_pvr_score.py", [
        ('        if "differs from its pin" in str(e):\n            raise\n        words = [None]', '        words = [None]'),
        ('            if "differs from its pin" in str(e):\n                raise\n            out.append(None)', '            out.append(None)')]),
    "seg_no_text_fallback": ("c_pvr_score.py", "            w = segment([u])[0] if w is None else w\n", ""),
    "sc_cut_output_allowed": ("c_pvr_score.py", "                if r is not None:\n                    fault(", "                if False:\n                    fault("),
}
EQUIV = {  # run and expected to SURVIVE; each with its proof
    # Proof: the only SIGN_ labels are SIGN_IDENTIFIED_POS, SIGN_IDENTIFIED_NEG and SIGN_NOT_IDENTIFIED (cm cm2()); each
    # contains "IDENTIFIED", so LABELS without SIGN_ still matches every one and scrub() removes the same fields.
    "w1_labels_no_sign": ("c_pvr_cm.py", 'LABELS = re.compile(r"IDENTIFIED|E1_|OVERID_|SIGN_|PLACEBO_")',
                          'LABELS = re.compile(r"IDENTIFIED|E1_|OVERID_|PLACEBO_")'),
}


def run(name: str, fname: str, pairs, scratch: Path) -> str:
    """pairs: [(old, new), ...], each old exactly once in the original file."""
    orig = HERE / fname
    src = orig.read_text(encoding="utf-8")
    for a, b in pairs:
        if src.count(a) != 1:
            return f"PATTERN({src.count(a)})"
        src = src.replace(a, b)
    p = scratch / f"{name}.py"
    p.write_text(src, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "-B", "-c", LOADER, str(p), str(orig)], capture_output=True, text=True)
    out = r.stdout + r.stderr
    if r.returncode == 0 and "selftest ok" in r.stdout:
        return "SURVIVED"
    return "KILLED" if "selftest FAILED:" in out else "CRASH"


def main() -> None:
    scratch = Path(sys.argv[1]).resolve()
    if str(scratch).startswith("/mnt/"):
        raise SystemExit("scratch dir must not be under /mnt (EIO mitigation)")
    scratch.mkdir(parents=True, exist_ok=True)
    for f in ("c_pvr_cay.py", "c_pvr_cm.py", "c_pvr_score.py"):
        if run(f"_original_{f[:-3]}", f, [("#!/usr/bin/env python3\n", "#!/usr/bin/env python3\n")], scratch) != "SURVIVED":
            raise SystemExit(f"the unmutated {f} does not pass its selftest; no mutant is counted")
    res = {}
    for n, (f, *ab) in M.items():
        res[n] = run(n, f, ab[0] if len(ab) == 1 else [tuple(ab)], scratch)
        print(f"{n:30s} {res[n]}", flush=True)
    eq = {}
    for n, (f, *ab) in EQUIV.items():
        eq[n] = run(n, f, ab[0] if len(ab) == 1 else [tuple(ab)], scratch)
        print(f"{n:30s} {eq[n]} (equivalent)", flush=True)
    print(f"mutants {len(M)}: killed {sum(v == 'KILLED' for v in res.values())}, other "
          f"{[n for n, v in res.items() if v != 'KILLED']}; equivalent {len(EQUIV)}: {eq}")


if __name__ == "__main__":
    main()
