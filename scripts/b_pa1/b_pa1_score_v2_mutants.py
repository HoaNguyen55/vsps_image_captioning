#!/usr/bin/env python3
"""Rule mutants for b_pa1_score_v2.py (DRAFT for the CC-316 round-2 read). v2 of b_pa1_score_mutants.py 8ad6b555: the
runner is unchanged; the list follows the v2 code and adds the rules of AMENDMENT_T1_SCORING_RULES_v1.md (CC-316 V7).
Each mutant breaks one registered rule or guard in a scratch copy and must make `b_pa1_score_v2.py selftest` fail,
offline (unshare -rn). Three scratch trees run side by side.
Run:  ~/.venvs/c_stage1_lists/bin/python -I -B scripts/b_pa1/b_pa1_score_v2_mutants.py
"""
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mutants import VENV_T, tree  # noqa: E402  scratch scripts/ of symlinks, so common.ROOT stays the repo

F = "b_pa1_score_v2.py"
HITS = "hits = [any(x[2] for x in t if x[1] in tags) for t in terms if any(x[1] in tags for x in t)]"
MUT = [  # (id, old, new): each old must occur exactly once
    ("T1 tau_c = scipy variant c (§8.1)", 'def tau_c(x, y, variant: str = "c") -> float:',
     'def tau_c(x, y, variant: str = "b") -> float:'),
    ("T2 tau_b row = scipy variant b (§8.1)", 'tau_c(x, y, "b") for m, x in xs.items()',
     'tau_c(x, y, "c") for m, x in xs.items()'),
    ("T3 the variant reaches scipy (§8.1)", "scipy.stats.kendalltau(x, y, variant=variant)",
     "scipy.stats.kendalltau(x, y)"),
    ("S1 seed 20261101 (§8.2)", "N_SLICE, N_BOOT, SEED = 2000, 10_000, 20261101",
     "N_SLICE, N_BOOT, SEED = 2000, 10_000, 20261102"),
    ("S2 B = 10,000 (§8.2)", "N_SLICE, N_BOOT, SEED = 2000, 10_000, 20261101",
     "N_SLICE, N_BOOT, SEED = 2000, 1_000, 20261101"),
    ("S9 B = 10,000 is the step-7 default (§8.2)",
     "def cmd_thresholds(a, log: Path = B.LOG, pins: dict = PINS, nb: int = N_BOOT) -> int:",
     "def cmd_thresholds(a, log: Path = B.LOG, pins: dict = PINS, nb: int = 1_000) -> int:"),
    ("S10 B = 10,000 is the step-8 default (§8.2)",
     "def cmd_tau(a, log: Path = B.LOG, pins: dict = PINS, nb: int = N_BOOT) -> int:",
     "def cmd_tau(a, log: Path = B.LOG, pins: dict = PINS, nb: int = 1_000) -> int:"),
    ("S3 image clusters (§8.2)",
     "rows = np.repeat(np.arange(len(img)), np.bincount(rng.integers(0, n, n), minlength=n)[img])",
     "rows = rng.integers(0, len(img), len(img))"),
    ("S4 SE_A = bootstrap SD (§8.5)", "se_a = float(reps.std())", "se_a = float(reps.var())"),
    ("S5 SESOI floor (§8.5)", "return max(SESOI_FLOOR, 2 * se_a)", "return 2 * se_a"),
    ("S6 SESOI 2 SE_A (§8.5)", "return max(SESOI_FLOOR, 2 * se_a)", "return max(SESOI_FLOOR, se_a)"),
    ("S7 SESOI floor 0.02 (§8.5)", "NI, SESOI_FLOOR, TIE = 0.02, 0.02, 0.005",
     "NI, SESOI_FLOOR, TIE = 0.02, 0.01, 0.005"),
    ("S8 NI 0.02 (§8.5)", "NI, SESOI_FLOOR, TIE = 0.02, 0.02, 0.005", "NI, SESOI_FLOOR, TIE = 0.05, 0.02, 0.005"),
    ("J1 tie width 0.005 (§7.1, §7.2)", "NI, SESOI_FLOOR, TIE = 0.02, 0.02, 0.005",
     "NI, SESOI_FLOOR, TIE = 0.02, 0.02, 0.01"),
    ("J2 highest tau_c (§7.1)", "best = max(taus.values())", "best = min(taus.values())"),
    ("J3 judge tie order J-a, J-b (§7.1)", "judge = pick({j: t[j] for j in JUDGES}, JUDGES)",
     "judge = pick({j: t[j] for j in JUDGES}, list(JUDGES)[::-1])"),
    ("L1 0.5 imputation (§7.2)", "return [0.5 if (s := b_score(cnt[c][k])) is None else s for k in G]",
     "return [0.0 if (s := b_score(cnt[c][k])) is None else s for k in G]"),
    ("L2 lever tie order (§7.2)", "cfg = pick(lever, [c for c in CFGS if c in cfgs])",
     "cfg = pick(lever, [c for c in list(CFGS)[::-1] if c in cfgs])"),
    ("L3 partial A3 never compared (§7.2)", 'return got if len(got) == len(CFGS) else {"d1v1": got["d1v1"]}',
     "return got"),
    ("L4 A3 completeness (§7.2)", "if set(d) == keys and set(v) == keys:", "if True:"),
    ("B1 yes iff p >= 0.5 (§7.1)", 'y = x["p_yes"] >= 0.5', 'y = x["p_yes"] > 0.5'),
    ("B2 abstains removed (§7.1)", "            ab += m\n            continue", "            ab += m"),
    ("B3 object propositions only (l.96-99)", 'if p["type"] != "object":', 'if p["type"] == "count":'),
    ("B4 mapped propositions only (l.91-93)", "yes + (y and m), n + m,", "yes + y, n + 1,"),
    ("B5 abstain out of the denominator (§7.1)", '"b": (c[0], c[1])', '"b": (c[0], c[1] + c[2])'),
    ("B6 B_open over all object props (§8.7)", '"open": (c[3], c[4])', '"open": (c[0], c[1])'),
    ("G1 gold = class has a box (l.229)", "int(c in gold[key[1]])", "int(c not in gold[key[1]])"),
    ("G2 final map pin (§6.4 step 6)", 'mp = json.loads(pinned(a.map, pins["map"]))\n    caps = {}',
     "mp = json.loads(a.map.read_bytes())\n    caps = {}"),
    ("G3 any-of, not all-of (amendment §1(b))", "any(x[2] for x in t if x[1] in tags)",
     "all(x[2] for x in t if x[1] in tags)"),
    ("G4 unit = matched term, not class (amendment §1(a), (c))", HITS,
     "hits = list({x[0]: x[2] for t in terms for x in t if x[1] in tags}.values())"),
    ("G5 rows of the tag set only (amendment §1(d), §6.2)", HITS, "hits = [any(x[2] for x in t) for t in terms if t]"),
    ("G6 a term with no row in the tag set is no mention (amendment §1(a))", HITS,
     "hits = [any(x[2] for x in t if x[1] in tags) for t in terms]"),
    ("M1 head noun through the matcher, not a lookup (amendment §2)", "for v in sc.vi_objects(obj, self.terms)",
     "for v in [obj]"),
    ("M2 the tag set on B's side (amendment §2)", "return bool(self.seen[obj] & tags)", "return bool(self.seen[obj])"),
    ("O1 tau needs the LOG sha (§6.4 step 7)", "if not B.pin_line(log, M.sha(tb), TH_NAME):", "if False:"),
    ("O2 thresholds written once (§8.5)", "    B.write_new(p, b)\n    sys.stdout.write",
     "    p.write_bytes(b)\n    sys.stdout.write"),
    ("O3 thresholds reads no B output (§8.5)", "    base = baselines(P, sorted(J))\n    t = {m",
     "    base = baselines(P, sorted(J))\n    configs(P, set(J))\n    t = {m"),
    ("O4 SHA256SUMS_rest pin", "if not B.pin_line(log, self.sha, SUMS):", "if False:"),
    ("O5 file sha through the manifest", "if self.sums.get(rel) != M.sha(b):", "if False:"),
    ("O6 annotation file pin (R6)", 'if a.ann.name != B.ANN_NAME or B.K.sha_file(a.ann) != pins["ann"]:',
     "if a.ann.name != B.ANN_NAME:"),
    ("O7 lists pin", 'ids = json.loads(pinned(lists, pins["lists"]))["slice_a"]',
     'ids = json.loads(lists.read_bytes())["slice_a"]'),
    ("C1 contacts cover slice A (CC-316 V6)", "if ids != set(slice_a(a.lists, pins, n)):",
     "if not ids <= set(slice_a(a.lists, pins, n)):"),
    ("C2 contacts ids only (§3)", '"ids": sorted(ids), "sums_rest_sha256"',
     '"ids": sorted(ids), "rows": P.rows(WALK), "sums_rest_sha256"'),
    ("C3 contacts over every out/ jsonl (§3)", 'if rel.startswith("out/") and rel.endswith(".jsonl") and rel != WALK:',
     'if rel.startswith("out/a1") and rel.endswith(".jsonl"):'),
    ("C4 contacts inside slice A (§3)", "if ids != set(slice_a(a.lists, pins, n)):",
     "if not ids >= set(slice_a(a.lists, pins, n)):"),
    ("H1 H1a margin -NI (§8.3)", "h1a = lb95 > -NI", "h1a = lb95 > 0"),
    ("H2 H1a one-sided 95% (§8.3)", 'bound(star["H1b"], 0.05)', 'bound(star["H1b"], 0.025)'),
    ("H3 Holm levels 0.025 then 0.05 (§8.3)", "alpha = (0.025, 0.05)[step]", "alpha = (0.05, 0.025)[step]"),
    ("H4 Holm step-down (§8.3)", "ok = bool(ok and p[h] <= alpha)", "ok = bool(h1a and p[h] <= alpha)"),
    ("H5 bootstrap p (§8.3)", "(1 + int((~(x > sesoi)).sum())) / (len(x) + 1)", "int((~(x > sesoi)).sum()) / len(x)"),
    ("H6 smaller p first (§8.3)", "enumerate(sorted(p, key=p.get))", "enumerate(p)"),
    ("H7 the p form governs (amendment §7)", "ok = bool(ok and p[h] <= alpha)", "ok = bool(ok and lb > sesoi)"),
    ("P1 PA3: point delta < SESOI (§11)", '"pa3_effect_trigger": not d_judge >= sesoi,',
     '"pa3_effect_trigger": not d_judge >= 0,'),
    ("U1 an undefined replicate ranks lowest (amendment §3)", "return np.where(np.isnan(d), -np.inf, d)",
     "return np.where(np.isnan(d), np.inf, d)"),
    ("U2 an undefined point delta fires PA3 (amendment §3)", '"pa3_effect_trigger": not d_judge >= sesoi,',
     '"pa3_effect_trigger": d_judge < sesoi,'),
    ("U3 an undefined lever tau selects nothing (amendment §3)", "if any(v != v for v in lever.values()):",
     "if False:"),
    ("U4 a null baseline stops step 7 (amendment §3)", "if any(v is None for v in out[name].values()):", "if False:"),
    ("U5 an undefined tau stops step 7 (amendment §3)", "if any(v != v for v in t.values()):", "if False:"),
    ("U6 an undefined SE_A replicate stops step 7 (amendment §3)", "if np.isnan(reps).any():", "if False:"),
    ("U7 undefined numbers are null, strict JSON (amendment §3)", "b = MV.canon(strict(doc))", "b = MV.canon(doc)"),
    ("V1 RESCAP_RAW_TONE refused (CC-316 V6)", 'if "RESCAP_RAW_TONE" in os.environ:', "if False:"),
    ("V2 imported module shas (CC-316 V6)", 'if meta["imports_sha256"] != IMPORTS:', "if False:"),
    ("V3 one T1_THRESHOLDS.json pin line (CC-316 V6)", "if pin_lines(log, TH_NAME) != 1:", "if False:"),
    ("Q4 P(PASS) deviation recorded (amendment §4)", '"p_pass_planning": P_PASS, ', ""),
    ("K1 conventions in T1_THRESHOLDS.json (amendment §7, V4)",
     '"conventions": CONV,\n        "amendment": AMEND, "gold_join_sha256"', '"amendment": AMEND, "gold_join_sha256"'),
    ("D1 dictionary-only gold (§6.2)", "dy = [gold_of(J[k], DICT) for k in dA]", "dy = [gold_of(J[k]) for k in dA]"),
    ("D2 dictionary-only B score (§6.2)", "mapped, DICT) for k in keys}", "mapped, TAGS) for k in keys}"),
    ("W1 mention counts (CC-316 W11)", "multi + sum(len(c) > 1 for c in ts)", "multi + sum(len(c) > 0 for c in ts)"),
]


def run(d: Path) -> tuple[bool, str]:
    r = subprocess.run(["unshare", "-rn", VENV_T, "-I", "-B", F, "selftest"], cwd=d, capture_output=True, text=True,
                       timeout=600)
    tail = [x for x in (r.stderr or r.stdout).splitlines() if x.strip()]
    return r.returncode == 0, (tail[-1][:100] if tail else str(r.returncode))


def one(job: tuple) -> tuple[str, bool, str]:
    root, src, (mid, old, new) = job
    if src.count(old) != 1:
        return mid, True, f"PATTERN NOT FOUND ONCE ({src.count(old)})"
    d = tree(root / mid.split()[0])
    (d / F).unlink()
    (d / F).write_text(src.replace(old, new), encoding="utf-8")
    return (mid, *run(d))


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="b_pa1_score_mut_"))
    try:
        ok, why = run(tree(root / "control"))
        assert ok, f"control fails: {why}"
        print("control: selftest passes on the unmutated file", flush=True)
        src, survived = (HERE / F).read_text(encoding="utf-8"), []
        with ThreadPoolExecutor(3) as ex:
            for mid, ok, why in ex.map(one, [(root, src, m) for m in MUT]):
                print(f"{mid}: {'SURVIVED' if ok else 'KILLED'} {why}", flush=True)
                survived += [mid] if ok else []
        print(f"{len(MUT) - len(survived)}/{len(MUT)} killed; survived: {survived or 'none'}")
        return 1 if survived else 0
    finally:
        shutil.rmtree(root)


if __name__ == "__main__":
    sys.exit(main())
