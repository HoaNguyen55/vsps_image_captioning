#!/usr/bin/env python3
"""Mutants of scripts/b_d1/b_d1.py (prereg v3 §6 S0; CC-505r2 N3; v2: CC-506 W4 adds the judge's 46). Each mutant changes one rule line of b_d1.py in a
scratch copy of the tree (b_d1.py rewritten; every other file copied unchanged, so the pins still hold) and runs
test_b_d1.py --only <check>. KILLED only when `SELFTEST FAIL <check>` is printed; a crash or a pass is SURVIVED.
The unmutated named checks must pass first. Mutants touch b_d1.py only: a change to a pinned FE-CERT file would stop
at the pin check, which is not a kill. Exit 0 only if every mutant is killed.
    python3 -I -B scripts/b_d1/mutants_b_d1.py [--jobs 2]"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(os.path.abspath(__file__)).parent
ROOT = HERE.parents[1]
REG = "manuscript/prereg/2026-11-27_b_d1/PREREG_DRAFT_B_D1_A3_v3.md"
SIGMA_PER_RESAMPLE = (
    "Wn = W / W.shape[1]\n"
    "    ks = [M[\"midx\"][m] for _k, m, _d in diffs(M, a, b, G)]\n"
    "    sb = [(Wn @ M[\"cider\"][k].T).std(axis=1, ddof=1) for k in ks]\n"
    "    boot = np.mean([(Wn @ d) / s for (_k, _m, d), s in zip(diffs(M, a, b, G), sb)], axis=0)\n"
    "    lo, hi = np.percentile(boot, [2.5, 97.5])\n"
    "    return [float(np.mean(terms, axis=0).mean()), float(lo), float(hi), float(boot.std(ddof=1))]")
MUT = [  # (id, old, new, check): each old occurs exactly once in b_d1.py
    # the registered list (prereg v3 §6 S0, CC-505r2 N3)
    ("R1 union-of-ties without the mixed-direction convention", "    return 0, True\n", "    return sg[0], True\n",
     "union_of_ties_cases"),
    ("R2 sigma_c recomputed per resample", "return BF.stats(np.mean(terms, axis=0), W)", SIGMA_PER_RESAMPLE,
     "aer_hand_toy"),
    ("R3 margin taken from the wrong member", 'next(cl["cider"] for cl in c["classes"].values() if BF.F0N in cl["members"])',
     'next(cl["cider"] for cl in c["classes"].values() if "syl.tw.pk.cf" in cl["members"])', "margin_from_f0"),
    ("R4 rdr held out", '"syl": (names(("rdr", "pyvi")), names(("syl",))),',
     '"syl": (names(("syl", "pyvi")), names(("rdr",))),', "fold_construction"),
    ("R5 touching counted as significant", 'sg = [BF.sig(cl["cider"]) for cl in c["classes"].values() for m in cl["members"] if m in G]',
     'sg = [(1 if cl["cider"][1] >= 0 else -1 if cl["cider"][2] <= 0 else 0) for cl in c["classes"].values() '
     'for m in cl["members"] if m in G]', "union_of_ties_touching"),
    ("R6 tw excluded from G_caption", 'G_CAPTION = names(("syl", "rdr", "pyvi"))',
     'G_CAPTION = [m for m in names(("syl", "rdr", "pyvi")) if ".tw." not in m]', "h3_grid_membership"),
    ("R7 A3 rule placed on r_A3", 'out = {"nulls": n, "label": a3_label(cnt["f0"][0], cnt["f0"][1], n)}',
     'out = {"nulls": n, "label": a3_label(cnt["A3_F_dev"][0], cnt["A3_F_dev"][1], n)}', "a3_rule_on_f0"),
    ("R8 a unit missing from G_contract", 'G_CONTRACT = names(("syl", "rdr", "pyvi"), "tw")',
     'G_CONTRACT = names(("syl", "rdr"), "tw")', "h3_grid_membership"),
    # gates and pins
    ("M9 G0 tolerance 1e-5", "G0_TOL = 1e-6", "G0_TOL = 1e-5", "g0_tolerance"),
    ("M10 G0 ignores class membership", 'if sorted(dev_got[k]["members"]) != sorted(dev_c["classes"][k]["members"]):',
     "if False:", "g0_membership_and_keys"),
    ("M11 G0 ignores the RESULT.json verdict", 'r["verdict_mismatch"] = BF.certify(got, set(F_ALL))["verdict"] != res_row["F"]',
     'r["verdict_mismatch"] = False', "g0_verdict_and_df0"),
    ("M12 G0 ignores D_f0", 'and s["verdict_mismatch"] == 0 and s["max_df0_diff"] <= G0_TOL)',
     'and s["verdict_mismatch"] == 0)', "g0_verdict_and_df0"),
    ("M13 s2 runs on a failed G0", 'if not g0.get("pass") or g0.get("PER_IMAGE_D1.npz") != a.npz_sha:',
     'if g0.get("PER_IMAGE_D1.npz") != a.npz_sha:', "g0_fault_stops"),
    ("M14 class key without the references", "f\"{M['keys'][k, ja]}|{M['keys'][k, jb]}|{M['rkeys'][k]}\"",
     "f\"{M['keys'][k, ja]}|{M['keys'][k, jb]}\"", "g0_pass_on_fecert_world"),
    ("M15 pin check skipped", "bad = [rel for rel, h in pins.items() if not (root / rel).is_file() or sha_file(root / rel) != h]",
     "bad = []", "pins_and_closure"),
    ("M16 s1 overwrites its matrix", "    if npz.exists():\n", "    if False:\n", "s1_matrix"),
    ("M17 M1 != M1' does not FAULT", "    if diff:\n        fault(", "    if diff and False:\n        fault(",
     "identity_m1_m1prime"),
    # H1/H2
    ("M18 floor n <= 10", "    if n < N_FLOOR:", "    if n <= N_FLOOR:", "contrast_labels"),
    ("M19 floor 9", "N_FLOOR, ALPHA = 10, 0.05", "N_FLOOR, ALPHA = 9, 0.05", "contrast_labels"),
    ("M20 two-sided binomial", 'alternative="greater"', 'alternative="two-sided"', "binomial_and_holm"),
    ("M21 n = 0 gives p = 0", "return 1.0 if n == 0 else", "return 0.0 if n == 0 else", "binomial_and_holm"),
    ("M22 ties broken by id descending", "key=lambda kv: (-kv[1][1], kv[0])",
     "key=lambda kv: (-kv[1][1], [-ord(ch) for ch in kv[0]])", "top_k_order"),
    ("M23 discordance by id, direction ignored", "sa, sb = set(A.items()), set(B.items())",
     "sa, sb = {(i, 1) for i in A}, {(i, 1) for i in B}", "held_break_and_discordant"),
    ("M24 AER weighted per class", "terms = [x for g in groups.values() for x in g] if not per_class else",
     "terms = [np.mean(g, axis=0) for g in groups.values()] if not per_class else", "aer_weighting"),
    ("M25 AER sigma with ddof 0", 'return M["cider"].mean(axis=2).std(axis=1, ddof=1)',
     'return M["cider"].mean(axis=2).std(axis=1, ddof=0)', "aer_hand_toy"),
    ("M26 uts fold without syl", '"uts": (names(("syl", "rdr", "pyvi")), names(("uts",))),',
     '"uts": (names(("rdr", "pyvi")), names(("uts",))),', "fold_construction"),
    # H3
    ("M27 H3 floor 50", "    if n < BF.N_MIN:", "    if n < 50:", "h3_trip_points"),
    ("M28 H3 NULL bar 0.06", "    if BF.cp_upper(k, n) <= BF.R_MAX:", "    if BF.cp_upper(k, n) <= 0.06:",
     "h3_trip_points"),
    ("M29 H3 SUPPORTED bar 0.04", "    if BF.cp_lower(k, n) > BF.R_MAX:", "    if BF.cp_lower(k, n) > 0.04:",
     "h3_trip_points"),
    ("M30 H3 grid on CIDEr-D only", "def grid_verdict(mc: dict, members, metrics=METRICS) -> int:",
     'def grid_verdict(mc: dict, members, metrics=("cider",)) -> int:', "h3_counts"),
    ("M31 k_T not counted", "            if grid_verdict(mc, G_CAPTION) != s:", "            if False:", "h3_counts"),
    # A3
    ("M32 A3 one-sided 95% bounds", "A3_CP, A3_NOM, A3_UP = 0.025, 0.025, 0.040", "A3_CP, A3_NOM, A3_UP = 0.05, 0.025, 0.040",
     "a3_trip_points"),
    ("M33 A3 pass bar 0.045", "A3_CP, A3_NOM, A3_UP = 0.025, 0.025, 0.040", "A3_CP, A3_NOM, A3_UP = 0.025, 0.025, 0.045",
     "a3_trip_points"),
    ("M34 A3 draws with replacement", "choice(n_comps, N_NULL, replace=False)", "choice(n_comps, N_NULL, replace=True)",
     "a3_draws_rule"),
    ("M35 A3 swap seed shifted", "np.random.default_rng(SEED_A3 + j)", "np.random.default_rng(SEED_A3 + j + 1)",
     "a3_draws_rule"),
    ("M36 A3 swap on f0 only", "cl[\"cider\"] = BF.stats(d if sign is None else sign * d, W)",
     "cl[\"cider\"] = BF.stats(d if sign is None or m != BF.F0N else sign * d, W)", "a3_null_stats"),
    # budget
    ("M37 budget 28,900 s", "CPU_BUDGET = 28_800", "CPU_BUDGET = 28_900", "cpu_budget"),
    ("M38 STOP marker ignored", '    if (records / "STOP").exists():', "    if False:", "cpu_budget"),
    # the judge's mutants of CC-506 (JUDGE_MUTANTS_CC506.py 42090d2f), (old, new) verbatim, each with a named check
    ("J01 tied contract ignored in M1'", '    if not sg or 0 in sg:\n        return 0, False', '    if not sg:\n        return 0, False', 'union_of_ties_cases'),
    ('J02 FE claims on FRAGILE', '        if v and v["certified"]:', '        if v and v["fragile"]:', 'fe_claims'),
    ('J03 FE margin sign flipped', 'out[c["id"]] = (v["certified"], v["z_min"])', 'out[c["id"]] = (v["certified"], -v["z_min"])', 'fe_claims'),
    ('J04 f0 claims without significance', '        if BF.sig(s) != 0:\n            out[c["id"]] = (int(np.sign(s[0])), BF.zval(s))', '        if True:\n            out[c["id"]] = (int(np.sign(s[0])), BF.zval(s))', 'margin_from_f0'),
    ('J05 f0 direction flipped', '(int(np.sign(s[0])), BF.zval(s))', '(-int(np.sign(s[0])), BF.zval(s))', 'margin_from_f0'),
    ('J06 sigma_c unstandardised', 'return M["cider"].mean(axis=2).std(axis=1, ddof=1)', 'return M["cider"].mean(axis=2).std(axis=1, ddof=1) * 0 + 1', 'aer_hand_toy'),
    ('J07 AER multiplies by sigma', 'append(d / sig_c[M["midx"][m]])', 'append(d * sig_c[M["midx"][m]])', 'aer_hand_toy'),
    ('J08 AER direction fixed +1', 'out[c["id"]] = (BF.sig(s), BF.zval(s))', 'out[c["id"]] = (1, BF.zval(s))', 'aer_claims_direction'),
    ('J09 H1 K = |f0|', 'k1 = min(len(fe), len(f0))', 'k1 = len(f0)', 'h1_h2_tests_and_holm'),
    ('J10 H2 K = |AER|', 'k2 = min(len(fe), len(aer))', 'k2 = len(aer)', 'h1_h2_tests_and_holm'),
    ('J11 pooled b_X takes b_FE', 'pool[h][1] += b[1]', 'pool[h][1] += b[0]', 'h1_h2_pooling'),
    ('J12 H1 p-values swapped', '"H1_FE_fewer": p_greater(pool["H1"][1]', '"H1_FE_fewer": p_greater(pool["H1"][0]', 'h1_h2_tests_and_holm'),
    ('J13 label branches swapped', '    if rej_fe:\n        return "SUPPORTED"', '    if rej_x:\n        return "SUPPORTED"', 'contrast_labels'),
    ('J14 shared claims counted', 'ba = sum(BF.held_break(byid[i], s, Hs)[0] for i, s in sa - sb)', 'ba = sum(BF.held_break(byid[i], s, Hs)[0] for i, s in sa)', 'held_break_and_discordant'),
    ('J15 breaks judged on F_dev, not H', '    Hs = set(H)\n    ba =', '    Hs = set(F_DEV)\n    ba =', 'held_break_and_discordant'),
    ('J16 pyvi fold breaks on syl', '"pyvi": (names(("syl", "rdr")), names(("pyvi",))),', '"pyvi": (names(("syl", "rdr")), names(("syl",))),', 'fold_construction'),
    ('J17 H3 n over the syl grid', '        s = grid_verdict(mc, G_CONTRACT)\n', '        s = grid_verdict(mc, G_SYL)\n', 'h3_counts'),
    ('J18 grid certified on any contract', 'all(s == sg[0] and s != 0 for s in sg)', 'any(s == sg[0] and s != 0 for s in sg)', 'h3_counts'),
    ('J19 H3 floor <= 59', '    if n < BF.N_MIN:', '    if n <= BF.N_MIN:', 'h3_trip_points'),
    ('J20 H3 split on agreeing classes', 'if any(BF.sig(mc[m][met]) != s for met in METRICS)', 'if any(BF.sig(mc[m][met]) == s for met in METRICS)', 'h3_counts'),
    ('J21 k_U against G_caption', 'k_u += grid_verdict(mc, G_CONTRACT) != s_syl', 'k_u += grid_verdict(mc, G_CAPTION) != s_syl', 'h3_counts'),
    ('J22 CP97 lower shape', 'beta.ppf(A3_CP, k, n - k + 1)', 'beta.ppf(A3_CP, k + 1, n - k)', 'a3_trip_points'),
    ('J23 CP97 upper shape', 'beta.ppf(1 - A3_CP, k + 1, n - k)', 'beta.ppf(1 - A3_CP, k, n - k + 1)', 'a3_trip_points'),
    ('J24 A3 pass on either direction', 'if all(up <= A3_UP for _lo, up in bounds):', 'if any(up <= A3_UP for _lo, up in bounds):', 'a3_trip_points'),
    ('J25 A3 ABOVE needs both directions', 'if any(lo > A3_NOM for lo, _up in bounds):', 'if all(lo > A3_NOM for lo, _up in bounds):', 'a3_trip_points'),
    ('J26 A3 directions pooled', 'cnt[key][0 if v > 0 else 1] += 1', 'cnt[key][0] += 1', 'a3_counts_by_family'),
    ('J27 A3_F over F_dev', '("A3_F", BF.certify(c, set(F_ALL))["certified"])', '("A3_F", BF.certify(c, set(F_DEV))["certified"])', 'a3_counts_by_family'),
    ('J28 A3 no swap applied', 'cl["cider"] = BF.stats(d if sign is None else sign * d, W)', 'cl["cider"] = BF.stats(d, W)', 'a3_null_stats'),
    ('J29 A3 pick seed shifted', 'pick = np.random.default_rng(SEED_A3).choice', 'pick = np.random.default_rng(SEED_A3 + 1).choice', 'a3_draws_rule'),
    ('J30 G0 keeps uts members in F_dev classes', 'mm = [m for m in cl["members"] if m in F_DEV]', 'mm = list(cl["members"])', 'g0_pass_on_fecert_world'),
    ('J31 G0 tolerance not applied', 's["max_abs_diff"] <= G0_TOL', 's["max_abs_diff"] <= 1.0', 'g0_tolerance'),
    ('J32 G0 key mismatch ignored', '"key_mismatch": set(dev_got) != set(dev_c["classes"])', '"key_mismatch": False', 'g0_membership_and_keys'),
    ('J33 G0 verdict over F_dev', 'BF.certify(got, set(F_ALL))["verdict"] != res_row["F"]', 'BF.certify(got, set(F_DEV))["verdict"] != res_row["F"]', 'g0_verdict_over_F'),
    ('J34 budget ignores records', 'return max(0, int(CPU_BUDGET - cpu_used(records)))', 'return max(0, int(CPU_BUDGET))', 'cpu_budget'),
    ('J35 budget counts user time only', '(User|System) time', '(User) time', 'cpu_budget'),
    ('J36 top_k one extra', 'kv[0]))[:k]}', 'kv[0]))[:k + 1]}', 'top_k_order'),
    ('J37 coverage counts claimed units', '"coverage": (sum(i not in cl for i in flips)', '"coverage": (sum(i in cl for i in flips)', 'h2_descriptive_rows'),
    ('J38 Holm at 0.10', 'rej = BF.holm(p, ALPHA)', 'rej = BF.holm(p, 0.10)', 'h1_h2_tests_and_holm'),
    ('J39 H2 p-values swapped', '"H2_AER_fewer": p_greater(pool["H2"][0]', '"H2_AER_fewer": p_greater(pool["H2"][1]', 'h1_h2_tests_and_holm'),
    ('J40 uts fold breaks on tw only', '"uts": (names(("syl", "rdr", "pyvi")), names(("uts",))),', '"uts": (names(("syl", "rdr", "pyvi")), names(("uts",), "tw")),', 'fold_construction'),
    ('J41 identity check over F_ALL', 'diff = sum(union_of_ties(c, G)[0] != BF.certify(c, Gs)["certified"] for c in comps)', 'diff = sum(union_of_ties(c, G)[0] != BF.certify(c, set(F_ALL))["certified"] for c in comps)', 'identity_m1_m1prime'),
    ('J42 s2 G0 npz binding dropped', ' or g0.get("PER_IMAGE_D1.npz") != a.npz_sha:', ':', 'stage_guards'),
    ('J43 G0 D_f0 tolerance 1e-3', 's["max_df0_diff"] <= G0_TOL)', 's["max_df0_diff"] <= 1e-3)', 'g0_verdict_and_df0'),
    ('J44 AER per-class used as primary', 'aer = claims_aer(M, comps, G, sig_c, W)\n', 'aer = claims_aer(M, comps, G, sig_c, W, per_class=True)\n', 'h1_h2_tests_and_holm'),
    ('J45 G0 sig gate dropped (v2)', 's["member_mismatch"] == 0 and s["sig_mismatch"] == 0', 's["member_mismatch"] == 0', 'g0_sig_gate'),
    ('J46 A3 max member rate over F (v2)', '"pos": max(per_member[m][0] for m in F_DEV) / n', '"pos": max(v[0] for v in per_member.values()) / n', 'a3_rule_on_f0'),
]


def tree(dst: Path) -> None:
    """The pinned files (read from the PINS block of b_d1.py), the registration and the two scripts/b_d1 files."""
    src = (HERE / "b_d1.py").read_text(encoding="utf-8")
    pins = src[src.index("PINS = {"):src.index("}\n", src.index("PINS = {")) + 1]
    rels = [ln.split('"')[1] for ln in pins.splitlines()[1:] if ln.strip().startswith('"')]
    for rel in rels + [REG]:
        (dst / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst / rel)
    (dst / "scripts/b_d1").mkdir(parents=True, exist_ok=True)
    for f in ("b_d1.py", "test_b_d1.py"):
        shutil.copy2(HERE / f, dst / "scripts/b_d1" / f)


def run_check(root: Path, check: str) -> str:
    r = subprocess.run([sys.executable, "-I", "-B", str(root / "scripts/b_d1/test_b_d1.py"), "--only", check],
                       capture_output=True, text=True, timeout=900, cwd=root)
    return r.stdout


def one(m) -> tuple[str, str]:
    mid, old, new, chk = m
    d = Path(tempfile.mkdtemp(prefix="b_d1_mut_"))
    try:
        tree(d)
        p = d / "scripts/b_d1/b_d1.py"
        s = p.read_text(encoding="utf-8")
        if s.count(old) != 1:
            return mid, f"BAD MUTANT (old occurs {s.count(old)} times)"
        os.chmod(p, 0o644)  # the tree copy keeps the 444 mode of the source
        p.write_text(s.replace(old, new), encoding="utf-8")
        out = run_check(d, chk)
        return mid, "KILLED" if f"SELFTEST FAIL {chk}" in out else "SURVIVED"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=2)
    a = ap.parse_args()
    d = Path(tempfile.mkdtemp(prefix="b_d1_mut_base_"))
    try:
        tree(d)
        checks = sorted({m[3] for m in MUT})
        base = {c: f"SELFTEST ok {c}" in run_check(d, c) for c in checks}
    finally:
        shutil.rmtree(d, ignore_errors=True)
    if not all(base.values()):
        print("BASE FAIL:", ", ".join(c for c, ok in base.items() if not ok))
        return 2
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(one, MUT))
    for mid, r in res:
        print(f"MUTANT {r}: {mid}")
    k = sum(r == "KILLED" for _m, r in res)
    print(f"killed {k} of {len(res)}")
    return 0 if k == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
