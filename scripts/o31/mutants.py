"""Mutation check: each mutant edits a COPY of src/ (never src/ itself); test_o31.py must fail on every one.
Own mutants M01-M25, W3/W5 mutants (CC-504), and the 35 judge mutants J01-J35 of CC-504 (J34 re-pointed).

    $PY -I -B mutants.py        exit 0 iff every mutant is killed and every mutation site exists exactly once
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent

MUTANTS = [
    ("M01 reject on any NO", "verify.py", 'if states and all(s == "NO" for s in states):', 'if "NO" in states:'),
    ("M02 missing family ignored", "verify.py", "states = [family_state(scores.get(f), tau_acc, tau_rej) for f in families]",
     "states = [family_state(scores.get(f), tau_acc, tau_rej) for f in families if f in scores]"),
    ("M03 accept strict >", "verify.py", 'return "YES" if s >= tau_acc', 'return "YES" if s > tau_acc'),
    ("M04 spatial not forced", "verify.py", "if ptype in ALWAYS_UNCERTAIN:", "if False:"),
    ("M05 recall micro in K0", "gate.py", '"R": 100 * sum(recalls) / len(recalls)', '"R": 100 * tp / sum(len(g) for g, _ in pairs if g)'),
    ("M06 floor -3.0", "gate.py", "R_GOAL, FLOOR_DROP = 47.1, 2.0", "R_GOAL, FLOOR_DROP = 47.1, 3.0"),
    ("M07 OP* tie -> lower P", "gate.py", 'key=lambda ip: (ip[1]["R"], ip[1]["P"], -ip[0])', 'key=lambda ip: (ip[1]["R"], -ip[1]["P"], -ip[0])'),
    ("M08 K0 strict >", "gate.py", '"pass": star["R"] >= R_GOAL', '"pass": star["R"] > R_GOAL'),
    ("M09 budget floor 4", "store.py", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 15, 9", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 4, 15, 9"),
    ("M10 budget floor() not ceil", "store.py", "math.ceil(K_SCALE * n)", "math.floor(K_SCALE * n)"),
    ("M11 S1 budget scaled too", "store.py", "b = budget(n_supp_entities(rec)) if scaled else B_FAIR", "b = budget(n_supp_entities(rec))"),
    ("M12 CMP k = max", "metrics.py", "k = min(len(ux), len(uy))", "k = max(len(ux), len(uy))"),
    ("M13 CMP ignores order", "metrics.py", "ux, uy = list(dict.fromkeys(order_x)), list(dict.fromkeys(order_y))",
     "ux, uy = sorted(set(order_x)), sorted(set(order_y))"),
    ("M14 null side exclusive", "metrics.py", 'on = (rep <= null) if side == "le" else (rep >= null)',
     'on = (rep < null) if side == "le" else (rep > null)'),
    ("M15 Holm without cummax", "metrics.py", "run = max(run, min(1.0, (m - i) * p[k]))", "run = min(1.0, (m - i) * p[k])"),
    ("M16 R per caption not per gold", "metrics.py", 'R = {k: 100 * _ratio(S[f"tp_{k}"], S[f"g_{k}"]) for k in (a, b, c)}',
     'R = {k: 100 * _ratio(S[f"tp_{k}"], S["n"]) for k in (a, b, c)}'),
    ("M17 H4 point condition dropped", "metrics.py", '"H4": point["H4.dRT"] >= H4_POINT', '"H4": True'),
    ("M18 H2 margin 0.5", "metrics.py", "ALPHA, MARGIN_H2, RHO_MIN, GAP_MIN = 0.05, 0.25, 0.50, 2.0",
     "ALPHA, MARGIN_H2, RHO_MIN, GAP_MIN = 0.05, 0.50, 0.50, 2.0"),
    ("M19 W4 (b) direction", "overlap.py", 'r = rule(feats[x], feats["uit_test"])', 'r = rule(feats["uit_test"], feats[x])'),
    ("M20 parity ignores image set", "decode.py", "if len(a) != PARITY_N or a.keys() != b.keys():", "if a.keys() != b.keys():"),
    ("M21 N_steps ceil", "train.py", "return epochs * (rows_s1 // grad_accum)", "return epochs * -(-rows_s1 // grad_accum)"),
    ("M22 mentions sorted by class", "extract.py", "key=lambda kv: (kv[1][0], kv[0])", "key=lambda kv: kv[0]"),
    ("M23 K0 keeps empty-gold images", "gate.py", "        if not gold:\n            continue\n        tp += len(m & gold)",
     "        tp += len(m & gold)"),
    ("M24 builder gets the caller's record", "store.py", "build(copy.deepcopy(rec), b)", "build(rec, b)"),
    ("M25 K0 driver accepts missing Q+", "gate.py", 'if n["miss"]:', "if False:"),
    ("M26 --exclude ignored", "gate.py", 'recs = [r for r in recs if r["file_name"] not in drop]', "recs = recs"),
    ("M27 reported sha not the written store", "gate.py", "sha = store.write_store(rows, Path(store_dir) / name) if store_dir",
     "sha = store.write_store(rows[::-1], Path(store_dir) / name) and store.store_sha(rows) if store_dir"),
    # W5 (CC-504)
    ("W5a old model string", "verify.py", 'FAIR_MODEL = "5CD-AI/Vintern-1B-v3_5"', 'FAIR_MODEL = "vintern-1b"'),
    ("W5b no-Q+ sent to UNCERTAIN", "verify.py", "        if k is None:\n", "        if False:\n"),
    ("W5c no-Q+ guard skipped", "gate.py", 'if n["no_q_not_rejected"]:', "if False:"),
    # W3 (CC-504)
    ("W3a S2 path without uncap", "gate.py", "**arm(*store.uncap(recs), scaled=True, name=name)", "**arm(recs, {}, scaled=True, name=name)"),
    ("W3b S1 path without uncap", "gate.py", 's1 = arm(*store.uncap(records), scaled=False, name="S1")', 's1 = arm(records, {}, scaled=False, name="S1")'),
    ("W3c gender_uncap guard skipped", "store.py",
     'if any((p.get("backoff") or {}).get("kind") == "gender_uncap"', 'if False and any((p.get("backoff") or {}).get("kind") == "gender_uncap"'),
]


def _judge() -> list:
    """The 35 mutants of CC-504 (~/vsps_out/judge_cc504/expected_fixes/jmut_cc504.py), J34 re-pointed (W3 moved it)."""
    return [
        ("J01 rho 0.40", "metrics.py", "0.05, 0.25, 0.50, 2.0", "0.05, 0.25, 0.40, 2.0"),
        ("J02 gap 1.0", "metrics.py", "0.05, 0.25, 0.50, 2.0", "0.05, 0.25, 0.50, 1.0"),
        ("J03 H1 lo>=0", "metrics.py", "rho >= RHO_MIN and lo > 0", "rho >= RHO_MIN and lo >= 0"),
        ("J04 H2 hi<=0", "metrics.py", 'h2 = "PASS" if hi < 0 else "FAIL"', 'h2 = "PASS" if hi <= 0 else "FAIL"'),
        ("J05 CI lo idx +1", "metrics.py", "float(ok[int(0.025 * nb)])", "float(ok[int(0.025 * nb) + 1])"),
        ("J06 CI hi idx", "metrics.py", "float(ok[int(0.975 * nb) - 1])", "float(ok[int(0.975 * nb)])"),
        ("J07 rehearsal no replacement", "metrics.py", "sub = rng.integers(0, n, size=n_sub)", "sub = rng.choice(n, size=n_sub, replace=False)"),
        ("J08 gate 0.95", "metrics.py", '"gate": wins / b_out >= 0.98', '"gate": wins / b_out >= 0.95'),
        ("J09 H4 min", "metrics.py", '"H4": max(p_null(', '"H4": min(p_null('),
        ("J10 H4b null 0", "metrics.py", 'p_null(reps["H4.dFA"], H4_FA, "ge")', 'p_null(reps["H4.dFA"], 0.0, "ge")'),
        ("J11 H5b side le", "metrics.py", '"H5b": p_null(reps["en.D"], 0.0, "ge")', '"H5b": p_null(reps["en.D"], 0.0, "le")'),
        ("J12 seed main", "metrics.py", "B_MAIN, SEED_MAIN = 10_000, 20261127", "B_MAIN, SEED_MAIN = 10_000, 20261128"),
        ("J13 B main 1000", "metrics.py", "B_MAIN, SEED_MAIN = 10_000, 20261127", "B_MAIN, SEED_MAIN = 1_000, 20261127"),
        ("J14 reh seed", "metrics.py", "B_OUT, B_IN, N_SUB, SEED_REH = 1_000, 1_000, 4_224, 20261128",
         "B_OUT, B_IN, N_SUB, SEED_REH = 1_000, 1_000, 4_224, 20261127"),
        ("J15 nan not null", "metrics.py", "(1 + int(on.sum()) + int(np.isnan(rep).sum()))", "(1 + int(on.sum()))"),
        ("J16 verdict unadjusted p", "metrics.py", '"verdict": "PASS" if adj[k] < ALPHA', '"verdict": "PASS" if p[k] < ALPHA'),
        ("J17 H3 null 0", "metrics.py", "H3_NULL, H4_POINT, H4_FA = -2.0, 10.0, 5.0", "H3_NULL, H4_POINT, H4_FA = 0.0, 10.0, 5.0"),
        ("J18 H4 point 5", "metrics.py", "H3_NULL, H4_POINT, H4_FA = -2.0, 10.0, 5.0", "H3_NULL, H4_POINT, H4_FA = -2.0, 5.0, 5.0"),
        ("J19 Q+ last probe", "verify.py", "            return qkey(q[\"question_vi\"])\n    return None",
         "            k = qkey(q[\"question_vi\"])\n    return locals().get('k')"),
        ("J20 budget max 20", "store.py", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 15, 9", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 20, 9"),
        ("J21 scale 2.0", "store.py", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 15, 9", "K_SCALE, B_MIN, B_MAX, B_FAIR = 2.0, 5, 15, 9"),
        ("J22 S1 B 5", "store.py", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 15, 9", "K_SCALE, B_MIN, B_MAX, B_FAIR = 1.5, 5, 15, 5"),
        ("J23 nsupp any type", "store.py", 'if p.get("type") == "entity" and', 'if'),
        ("J24 K0 goal 45", "gate.py", "R_GOAL, FLOOR_DROP = 47.1, 2.0", "R_GOAL, FLOOR_DROP = 45.0, 2.0"),
        ("J25 OPmid feasible only", "gate.py", "_, mid = min(enumerate(points),", "_, mid = min(feas,"),
        ("J26 load_table last", "gate.py", 't.setdefault(r["image"], {}).setdefault(r["q"], r["p_yes"])',
         't.setdefault(r["image"], {})[r["q"]] = r["p_yes"]'),
        ("J27 W4 pool last set only", "overlap.py", 'hit |= r["excluded"]', 'hit = r["excluded"]'),
        ("J28 seed_mean axis1", "metrics.py", "np.mean(np.stack(per_seed), axis=0)", "np.mean(np.stack(per_seed), axis=1)"),
        ("J29 parity batch 8 always", "decode.py", '"batch": 1 if mism else 8', '"batch": 8'),
        ("J30 min_supported 0", "store.py", "min_supported: int = 1", "min_supported: int = 0"),
        ("J31 tau order not enforced", "verify.py", "if not tau_rej < tau_acc:", "if False:"),
        ("J32 grid tau_acc missing 0.9", "verify.py", "TAU_ACC = (0.50, 0.60, 0.70, 0.80, 0.90)", "TAU_ACC = (0.50, 0.60, 0.70, 0.80)"),
        ("J33 reject strict <", "verify.py", 'else "NO" if s <= tau_rej', 'else "NO" if s < tau_rej'),
        ("J34 S1 from O31 states (re-pointed)", "gate.py", 's1 = arm(*store.uncap(records), scaled=False, name="S1")',
         's1 = arm(*store.uncap([verify.apply_states(r, {}, ("vintern",), 0.5, 0.1)[0] for r in records]), scaled=False, name="S1")'),
        ("J35 reh inner from full set", "metrics.py", "idx = rng.integers(0, n_sub, size=(c, n_sub))",
         "idx = rng.integers(0, n_sub, size=(c, n_sub)) * 0"),
    ]


MUTANTS += _judge()


def main() -> int:
    py = sys.executable
    survived, bad_site = [], []
    with tempfile.TemporaryDirectory(prefix="o31_mut_") as tmp:
        for name, f, old, new in MUTANTS:
            dst = Path(tmp) / name.split()[0]
            shutil.copytree(HERE / "src", dst, ignore=shutil.ignore_patterns("__pycache__"))
            path = dst / "o31" / f
            text = path.read_text(encoding="utf-8")
            if text.count(old) != 1:
                bad_site.append(name)
                print(f"SITE {name}: pattern found {text.count(old)} times")
                continue
            path.chmod(0o644)
            path.write_text(text.replace(old, new), encoding="utf-8")
            r = subprocess.run([py, "-I", "-B", str(HERE / "test_o31.py")], capture_output=True, text=True,
                               env={**os.environ, "O31_SRC": str(dst)})
            killed = r.returncode != 0
            fails = [ln.split(":")[0][5:] for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
            print(f"{'killed  ' if killed else 'SURVIVED'} {name}  {fails[:3]}")
            if not killed:
                survived.append(name)
    print(f"{len(MUTANTS) - len(survived) - len(bad_site)}/{len(MUTANTS)} killed; survived {survived}; bad sites {bad_site}")
    return 1 if survived or bad_site else 0


if __name__ == "__main__":
    sys.exit(main())
