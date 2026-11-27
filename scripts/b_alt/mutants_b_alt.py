#!/usr/bin/env python3
"""Mutants of scripts/b_alt/b_alt.py and cpu_guard.py (prereg v2 §5 S0: M1-M10 as registered, plus every rule, floor,
label, gate and guard line). Each mutant changes one line in a scratch copy of the push tree (every other file copied
unchanged, so the pins still hold) and runs test_b_alt.py --only <check>. KILLED only when `SELFTEST FAIL <check>` is
printed; a crash or a pass is SURVIVED. The unmutated named checks must pass first. Exit 0 only if all are killed.
    python3 -I -B scripts/b_alt/mutants_b_alt.py [--jobs 2]"""
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
B, G = "b_alt.py", "cpu_guard.py"
MUT = [  # (id, file, old, new, check): each old occurs exactly once in its file
    # registered (prereg v2 §5 S0; CC-510 W1)
    ("M1 census fed outputs", B, "strings = [r for i in half_a for r in refs[i]]  #",
     "strings = [r for i in half_a for r in refs[i]] + [s for p in sorted(BF.RES.glob('*.preds.json')) "
     "for s in PT.load_preds(p).values()]  #", "census_reads_half_a_references_only"),
    ("M2 pin applied to pyvi only", B, "        if len(m) == 5:\n            d, ml",
     "        if len(m) == 5 and m[0] == \"pyvi\":\n            d, ml", "pin_tok_both_units"),
    ("M3 T/P/C mismatched in a pair", B, 'mname(("pyvi",) + lv), lv) for lv in LEVELS]',
     'mname(("pyvi",) + LEVELS[0]), lv) for lv in LEVELS]', "pairs_same_levels"),
    ("M4 sigma recomputed per resampled image", B, 'a0, ah, aa = sg @ x[""], sg @ x["h"], sg @ x["a"]',
     'a0, ah, aa = (np.sign(x[""]) * x[""]).sum(0), (np.sign(x[""]) * x["h"]).sum(0), '
     '(np.sign(x[""]) * x["a"]).sum(0)', "sigma_fixed_unit_sums"),
    ("M5 W_B reseeded", B, "SEED_SPLIT, SEED_WB = 20261127, 20261128", "SEED_SPLIT, SEED_WB = 20261127, 20261112",
     "bootstrap_draws_registered_seed"),
    ("M5b W_B with the FE-CERT seed in s2", B, "WB = BF.boot_W(len(cols), SEED_WB)", "WB = BF.boot_W(len(cols))",
     "bootstrap_draws_registered_seed"),
    ("M6a >= at the TAIL boundary", B, "    if d_lo[1] < 0:", "    if d_lo[1] <= 0:", "hl1_boundaries"),
    ("M6b >= at the HEAD boundary", B, "    if d_hi[0] > 0:", "    if d_hi[0] >= 0:", "hl1_boundaries"),
    ("M6c >= at PRACTICAL", B, "    if rho_head[0] > PRACTICAL:", "    if rho_head[0] >= PRACTICAL:", "hl2_boundaries"),
    ("M6d <= at NOT PRACTICAL", B, "    if rho_head[1] < PRACTICAL:", "    if rho_head[1] <= PRACTICAL:", "hl2_boundaries"),
    ("M6e <= at floor (iv)", B, 'if s["abs_shift"] < SHIFT_FLOOR * s["abs_Dr"]:',
     'if s["abs_shift"] <= SHIFT_FLOOR * s["abs_Dr"]:', "floors_order_and_boundaries"),
    ("M6f <= at floor (v)", B, "    if rho_all_iv[0] < RHO_ALL_FLOOR:", "    if rho_all_iv[0] <= RHO_ALL_FLOOR:",
     "floors_order_and_boundaries"),
    ("M7 tone key not applied", B,
     'return unicodedata.normalize("NFC", FM.tone(unicodedata.normalize("NFC", s), "tm")).casefold()',
     'return unicodedata.normalize("NFC", s).casefold()', "tone_key_and_explode"),
    ("M8a census on all images", B, "strings = [r for i in half_a for r in refs[i]]  #",
     "strings = [r for i in ids for r in refs[i]]  #", "census_reads_half_a_references_only"),
    ("M8b estimands on half A", B, "cols = np.array([pos[i] for i in half_b])",
     "cols = np.array([pos[i] for i in half_a])", "bootstrap_draws_registered_seed"),
    ("M9 H-L1 read from rho_head", B, '"d_lo": kap - np.minimum(cr, co), "d_hi": kap - np.maximum(cr, co),',
     '"d_lo": (1 - rh) - np.minimum(cr, co), "d_hi": (1 - rh) - np.maximum(cr, co),',
     "kappa_label_reads_kappa_not_rho"),
    ("M10a c_ref held at its full-sample value", B, "cr, z4 = ratio_draws(Wx @ cref[:, 0], Wx @ cref[:, 1])",
     "cr, z4 = ratio_draws(np.full(Wx.shape[0], cref[:, 0].sum()), np.full(Wx.shape[0], cref[:, 1].sum()))",
     "coverage_recomputed_per_draw"),
    ("M10b c_out held at its full-sample value", B, "co, z5 = ratio_draws(Wx @ cout[:, 0], Wx @ cout[:, 1])",
     "co, z5 = ratio_draws(np.full(Wx.shape[0], cout[:, 0].sum()), np.full(Wx.shape[0], cout[:, 1].sum()))",
     "coverage_recomputed_per_draw"),
    # estimands
    ("E1 kappa denominator rho_head's", B, "kap, z3 = ratio_draws(A - Ah, A - Aa)", "kap, z3 = ratio_draws(A - Ah, A)",
     "nonremovable_shift_leaves_kappa"),
    ("E2 rho_head not complemented", B, '"rho_head": 1 - rh,', '"rho_head": rh,', "head_only_tail_only_worlds"),
    ("E3 rho_all not complemented", B, '"rho_all": 1 - ra,', '"rho_all": ra,', "head_only_tail_only_worlds"),
    ("E4 Pi_all shift from Pi_head members", B, '(("", ""), ("h", "+Ph"), ("a", "+Pa"))',
     '(("", ""), ("h", "+Ph"), ("a", "+Ph"))', "head_only_tail_only_worlds"),
    ("E5 shift without the rdr side", B, 'x[tag] = (Cp[ia] - Cp[ib]) - (Cr[ia] - Cr[ib])',
     'x[tag] = (Cp[ia] - Cp[ib])', "sigma_fixed_unit_sums"),
    ("E6 zero-denominator draws ignored", B, "    if zero:\n", "    if False:\n", "floors_order_and_boundaries"),
    # census and pin rules
    ("P1 coverage strictly above 0.80", B, "if cum * COVER_DEN >= COVER_NUM * total:",
     "if cum * COVER_DEN > COVER_NUM * total:", "pin_list_rules"),
    ("P2 ties not by code point", B, "key=lambda t: (-occ[t], type_str(t))", "key=lambda t: (-occ[t],)",
     "pin_list_rules"),
    ("P3 tie to more tokens", B, "(-kv[1], sum(kv[0]), tuple(int(x) for x in kv[0]))",
     "(-kv[1], -sum(kv[0]), tuple(int(x) for x in kv[0]))", "pin_list_rules"),
    ("P4 tie to the largest vector", B, "(-kv[1], sum(kv[0]), tuple(int(x) for x in kv[0]))",
     "(-kv[1], sum(kv[0]), tuple(-int(x) for x in kv[0]))", "pin_list_rules"),
    ("P5 start boundary not forced", B, "                if i > 0:\n", "                if False:\n", "pin_rule"),
    ("P6 end boundary not forced", B, "                if i + ln < n:\n", "                if False:\n", "pin_rule"),
    ("P7 shortest match first", B, "for ln in range(min(maxlen, n - i), 1, -1):",
     "for ln in range(2, min(maxlen, n - i) + 1):", "pin_rule"),
    ("P8 spans without the difference test", B, "e - s >= 2 and ba[s:e - 1] != bb[s:e - 1]]", "e - s >= 2]",
     "spans_rule"),
    ("P9 common boundary = either", B, "if ba[j] and bb[j]] + [n]", "if ba[j] or bb[j]] + [n]", "spans_rule"),
    ("P10 unaligned keys accepted", B, "    if ka != kb:\n        return None", "    if False:\n        return None",
     "spans_rule"),
    ("P11 malformed tokens accepted", B, '        if any(p == "" for p in parts):', "        if False:",
     "tone_key_and_explode"),
    ("P12 halves swapped", B, "return [ids[k] for k in perm[:HALF]], [ids[k] for k in perm[HALF:]]",
     "return [ids[k] for k in perm[HALF:]], [ids[k] for k in perm[:HALF]]", "split_exact"),
    ("P13 split seed", B, "SEED_SPLIT, SEED_WB = 20261127, 20261128", "SEED_SPLIT, SEED_WB = 20261126, 20261128",
     "split_exact"),
    # floors and constants
    ("F1 floor (iii) <=", B, 'elif len(pl["order"]) < MIN_TYPES:', 'elif len(pl["order"]) <= MIN_TYPES:',
     "census_floor_iii_stops_chain"),
    ("F2 floor (ii) >=", B, "    if share > UNALIGNED_MAX:", "    if share >= UNALIGNED_MAX:", "census_floor_ii_unaligned"),
    ("F3 s1b runs after a floor", B, '    if cz.get("floor"):', "    if False:", "census_floor_iii_stops_chain"),
    ("F4 MIN_TYPES 29", B, "MIN_TYPES = 30", "MIN_TYPES = 29", "floors_order_and_boundaries"),
    ("F5 SHIFT_FLOOR 0.02", B, "SHIFT_FLOOR = 0.01", "SHIFT_FLOOR = 0.02", "floors_order_and_boundaries"),
    ("F6 RHO_ALL_FLOOR 0.10", B, "RHO_ALL_FLOOR = 0.20", "RHO_ALL_FLOOR = 0.10", "floors_order_and_boundaries"),
    ("F7 PRACTICAL 0.40", B, "PRACTICAL = 0.50", "PRACTICAL = 0.40", "hl2_boundaries"),
    # gates and guards
    ("G1 G0 tolerance 1e-5", B, "G0_TOL = 1e-6", "G0_TOL = 1e-5", "g0_tolerance_and_sig"),
    ("G2 G0 sig gate dropped", B, 's["member_mismatch"] == 0\n                 and s["sig_mismatch"] == 0',
     's["member_mismatch"] == 0', "g0_tolerance_and_sig"),
    ("G3 G0 ignores membership", B, 'if sorted(want[k]["members"]) != sorted(got["classes"][k]["members"]):',
     "if False:", "g0_membership_and_keys"),
    ("G4 G0 ignores keys", B, '"key_mismatch": set(want) != set(got["classes"])', '"key_mismatch": False',
     "g0_membership_and_keys"),
    ("G5 G0 ignores the comparison count", B, 's["pass"] = (len(rows) == EXPECT_D and ', 's["pass"] = (',
     "g0_membership_and_keys"),
    ("G6 class key without references", B, "key = f\"{M['keys'][k, ja]}|{M['keys'][k, jb]}|{M['rkeys'][k]}\"",
     "key = f\"{M['keys'][k, ja]}|{M['keys'][k, jb]}\"", "g0_pass_on_fecert_world"),
    ("G7 G0 keeps syl members", B, 'mm = [m for m in cl["members"] if m in G_W]', 'mm = list(cl["members"])',
     "g0_pass_on_fecert_world"),
    ("G8 s2 runs on a failed G0", B, 'if not g0.get("pass") or g0.get("PER_IMAGE_ALT.npz") != a.npz_sha:',
     'if g0.get("PER_IMAGE_ALT.npz") != a.npz_sha:', "stage_guards"),
    ("G9 s2 G0 binding dropped", B, 'if not g0.get("pass") or g0.get("PER_IMAGE_ALT.npz") != a.npz_sha:',
     'if not g0.get("pass"):', "stage_guards"),
    ("G10 a json stage runs twice", B, "    if path.exists():\n", "    if False:\n", "stage_guards"),
    ("G11 s1b overwrites its matrix", B, "    if npz.exists():\n", "    if False:\n", "stage_guards"),
    ("G12 jar prefix only", B, 'if SEG is None and env.get("jar_sha256") != JAR_SHA_FULL:', "if False:",
     "jar_full_pin"),
    ("G13 pin check skipped", B, "bad = [rel for rel, h in pins.items() if not (root / rel).is_file() or "
     "sha_file(root / rel) != h]", "bad = []", "pins_and_closure"),
    ("C1 guard limit x100", G, "        if peak >= limit:", "        if peak >= limit * 100:", "cpu_guard_kills_tree"),
    ("C2 guard ignores descendants", G, "        todo += kids.get(p, [])", "        todo += []",
     "cpu_guard_kills_tree"),
    ("C3 guard ignores reaped children", G, "tick[int(d)] = sum(int(x) for x in r[11:15])",
     "tick[int(d)] = sum(int(x) for x in r[11:13])", "cpu_guard_kills_tree"),
]


def tree(dst: Path) -> None:
    for rel in (HERE / "PUSH_LIST.txt").read_text(encoding="utf-8").split():
        if (ROOT / rel).is_file():
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dst / rel)


def run_check(root: Path, check: str) -> str:
    r = subprocess.run([sys.executable, "-I", "-B", str(root / "scripts/b_alt/test_b_alt.py"), "--only", check],
                       capture_output=True, text=True, timeout=900, cwd=root)
    return r.stdout


def one(m) -> tuple[str, str]:
    mid, f, old, new, chk = m
    d = Path(tempfile.mkdtemp(prefix="b_alt_mut_"))
    try:
        tree(d)
        p = d / "scripts/b_alt" / f
        src = p.read_text(encoding="utf-8")
        if src.count(old) != 1:
            return mid, f"BAD MUTANT (old occurs {src.count(old)} times)"
        os.chmod(p, 0o644)  # the pushed files are mode 444
        p.write_text(src.replace(old, new), encoding="utf-8")
        out = run_check(d, chk)
        return mid, "KILLED" if f"SELFTEST FAIL {chk}" in out else "SURVIVED"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=2)
    a = ap.parse_args()
    checks = sorted({m[4] for m in MUT})
    base = subprocess.run([sys.executable, "-I", "-B", str(HERE / "test_b_alt.py"), "--only", *checks],
                          capture_output=True, text=True, timeout=1800, cwd=ROOT).stdout
    if not all(f"SELFTEST ok {c}" in base for c in checks):
        print("MUTANTS: the unmutated named checks do not all pass")
        print("\n".join(ln for ln in base.splitlines() if ln.startswith("SELFTEST") and " ok " not in ln))
        return 1
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(one, MUT))
    for mid, r in res:
        print(f"MUTANT {r}: {mid}")
    k = sum(r == "KILLED" for _m, r in res)
    print(f"killed {k} of {len(res)}")
    return 0 if k == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
