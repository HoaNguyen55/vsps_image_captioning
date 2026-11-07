#!/usr/bin/env python3
"""Mutant harness for scripts/a_m1/a_m1.py: every mutant of A_M1_PLAN_v3.md §7.3 (1-18, 17b, 17c) plus 17d
(CC-285r3 N-F), the N-G record rules, CC-287 W1-W3 and N2 (HMa, HMc, HMi), and CC-287r2 W3r2. Pattern of scripts/a_dchecks/a_dchecks_mutants.py.
Usage: <venv python> -I -B a_m1_mutants.py <scratch dir outside the repo>
Each mutant applies its exact replacements (each target must occur exactly once) and runs `selftest --core --out
<scratch>/<name>.json` on the mutated source, executed with __file__ = the original path so pins and imports resolve
unchanged. The unmutated source runs first and must exit 0 with 'selftest ok'. KILLED = exit != 0 and at least one
named selftest check FAILED; an exit before any check ran is CRASH, which is not a kill. Synthetic data only; the
selftest's atomic-write probe uses data/results/a_m1/_selftest_probe_<pid>/ (never run_record/)."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "a_m1.py"
LOADER = ("import sys; src, orig, out = sys.argv[1:4]; sys.argv = [orig, 'selftest', '--core', '--out', out]; "
          "ns = {'__name__': '__main__', '__file__': orig}; "
          "exec(compile(open(src, encoding='utf-8').read(), orig, 'exec'), ns)")

M = {
    "01_per_image_summed": [("    U, p1, p2 = pooled(W, F, c)\n    return U + chao_f0(p1, p2, k, target)\n",
                             "    return W @ (F[:, c[0]] + chao_f0(F[:, c[1]], F[:, c[2]], k, target))\n")],
    "02_factor_dropped": [('    return L["f0"](phi1, phi2, k, target)\n',
                           '    return L["f0"](phi1, phi2, k, target) * k / max(k - 1, 1)\n')],
    "03_classic_at_phi2_0": [('    return L["f0"](phi1, phi2, k, target)\n',
                              '    return L["f0"](phi1, np.maximum(phi2, 1), k, target)\n')],
    "04_first_k_only": [("    return list(itertools.combinations(range(K), k))\n", "    return [tuple(range(k))]\n")],
    "05_G_first_k": [("    G = U5 - u_bar(W, F, cols, k)\n", "    G = U5 - pooled(W, F, cols[tuple(range(k))])[0]\n")],
    "06_v2a_on_point": [("    lo, hi = interval(e_star)\n    if hi < -delta", "    lo = hi = e_point\n    if hi < -delta")],
    "07_v2a_at_90pct": [("np.percentile(np.asarray(x, float), [2.5, 97.5])", "np.percentile(np.asarray(x, float), [5, 95])")],
    "08_v1_on_2p5th": [("np.percentile(np.asarray(d_star, float), 97.5) < 0", "np.percentile(np.asarray(d_star, float), 2.5) < 0")],
    "09_armL_not_intersected": [('uni = sorted(set().union(*rs)) if arm == "U" else sorted(c)',
                                 'uni = sorted(set().union(*rs)) if arm == "U" else sorted(c | set().union(*rs))')],
    "10_coco_more_than_5": [("return [[fn(s) for s in kr[int(i)][:K]] for i in ids]",
                             "return [[fn(s) for s in kr[int(i)]] for i in ids]")],
    "11_custody_hook_off": [('    if event != "open" or not _HOOK["on"] or not args:\n', "    if True:\n")],
    "12_v1_labelled_pass": [('97.5) < 0 else "CONSISTENT"', '97.5) < 0 else "PASS"')],
    "13_bootstrap_over_subsets": [("    return np.mean([s_hat(W, F, cols[A], k, K) for A in combos(k)], 0)\n",
                                   "    return np.mean([s_hat(W, F, cols[A], k, K) for A in [combos(k)[j] for j in "
                                   "np.random.default_rng(0).integers(0, len(combos(k)), len(combos(k)))]], 0)\n")],
    "14_own_draw_per_statistic": [("    G, eps = gain_error(W, FU, cU, K_PRIMARY)\n",
                                   "    G, eps = gain_error(np.vstack([W[:1], boot_weights(W.shape[1], "
                                   "np.random.default_rng(5), W.shape[0] - 1)]), FU, cU, K_PRIMARY)\n")],
    "15_basename_keys": [('return f"{kind}|{path}"', 'return f"{kind}|{Path(path).name}"')],
    "16_gate_computes_phi": [('        rec["G4"] = {"n":', '        features(*incidence(refs, comp, "U"), n, (K,))\n'
                              '        rec["G4"] = {"n":')],
    "17_precedence_swapped": [('    if "VIOLATED" in seen:\n        return "FALSIFIED"\n'
                               '    if any((sets.get(s) or {}).get("state") != "COMPLETED" for s in SETS):\n'
                               '        return "NOT_RUN/FAULT"\n',
                               '    if any((sets.get(s) or {}).get("state") != "COMPLETED" for s in SETS):\n'
                               '        return "NOT_RUN/FAULT"\n    if "VIOLATED" in seen:\n        return "FALSIFIED"\n')],
    "17b_v1_of_completed_sets_only": [(
        '    seen = [persisted.get(s) for s in SETS] + [((sets.get(s) or {}).get("V1") or {}).get("label") for s in SETS]\n',
        '    done = [s for s in SETS if (sets.get(s) or {}).get("state") == "COMPLETED"]\n'
        '    seen = [persisted.get(s) for s in done] + [((sets.get(s) or {}).get("V1") or {}).get("label") for s in done]\n')],
    "17c_dead_run_ignores_records": [("    sets = (result or {}).get(\"sets\") or {}\n",
                                      "    if result is None:\n        return \"NOT_RUN/FAULT\"\n"
                                      "    sets = (result or {}).get(\"sets\") or {}\n")],
    "17c_non_atomic_write": [('    data = (json.dumps(rec, indent=1) + "\\n").encode()\n',
                              '    data = (json.dumps(rec, indent=1) + "\\n").encode()\n    tmp = target\n')],
    "17c_late_v1_write": [('    trace.append("V1")\n    on_v1(v1)\n', '    trace.append("V1")\n'),
                          ('    trace.append("V2A")\n', '    trace.append("V2A")\n    on_v1(v1)\n')],
    "17c_record_rewritable": [('    if target.exists():\n        raise Fault(f"refused: {target.name} exists (one record per '
                               'set, never rewritten)")\n', "")],
    "17c_run_does_not_refuse_records": [("    if found:\n        raise Fault(f\"refused: V1 records exist",
                                         "    if False:\n        raise Fault(f\"refused: V1 records exist")],
    "17d_persist_before_memory": [("                v1_mem[s] = rec\n                persist(s, rec)\n",
                                   "                persist(s, rec)\n                v1_mem[s] = rec\n")],
    "17d_result_drops_memory_v1": [('        for s, rec in v1_mem.items():\n            res["sets"][s]["V1"] = rec\n', "")],
    # CC-287 W1-W3 and N2 (HMa, HMc, HMi)
    "W1_completed_past_cap": [("                out = compute(s, on_v1)\n                budget.check()  # W1",
                               "                out = compute(s, on_v1)\n                pass  # W1")],
    "W2_failed_gate_time_ignored": [(' + sorted(out_dir.glob("gate.failed_*.json"))', "")],
    "W2_raising_attempt_unrecorded": [("        try:\n            write_json(path, {", "        try:\n            raise RuntimeError\n            write_json(path, {")],
    "W3_fallback_skeleton": [('    res.setdefault("sets", {})\n    for s in SETS:\n        res["sets"].setdefault(s, {"state": "NOT_RUN", '
                              '"reason": "failure before the set"})\n',
                              '    res.clear()\n    res["sets"] = {}\n    for s in SETS:\n        res["sets"].setdefault(s, '
                              '{"state": "NOT_RUN", "reason": "failure before the set"})\n')],
    "W3_result_not_atomic": [('    tmp = path.with_name(f".{path.name}.tmp{os.getpid()}_{next(_TMP_N)}")\n', "    tmp = path\n")],
    "W3_torn_result_raises": [("    except (OSError, ValueError) as e:\n        return None, f\"unreadable",
                               "    except ZeroDivisionError as e:\n        return None, f\"unreadable")],
    "HMa_dir_fsync_eio_swallowed": [('        if e.errno not in (errno.EINVAL, errno.ENOTSUP, getattr(errno, "EOPNOTSUPP", errno.ENOTSUP)):\n'
                                     '            raise\n', "        if False:\n            raise\n")],
    "HMc_refusal_glob_narrowed": [('rec_dir.glob("v1_*.json")', 'rec_dir.glob("v1_coco*.json")')],
    "HMi_fault_after_v1_completed": [('                res["sets"][s] = {"state": "FAULT", "reason":',
                                      '                res["sets"][s] = {"state": "COMPLETED" if s in v1_mem else "FAULT", '
                                      '"V2A": {"label": "PASS"}, "reason":')],
    # CC-287r2 W3r2: revert both parts of the fix (per-pid temp name; no temp cleanup on failure)
    "W3r2_fix_reverted": [('    tmp = path.with_name(f".{path.name}.tmp{os.getpid()}_{next(_TMP_N)}")\n',
                           '    tmp = path.with_name(f".{path.name}.tmp{os.getpid()}")\n'),
                          ("    except _SimulatedDeath:\n        raise\n    except BaseException:\n        try:\n"
                           "            os.remove(tmp)\n        except FileNotFoundError:\n            pass\n        raise\n",
                           "    except _SimulatedDeath:\n        raise\n")],
    "18_wp_config_missing": [("WP_D_GRID = ((0.5, 0.2), (0.6, 0.05), (0.8, 0.1))", "WP_D_GRID = ((0.5, 0.2), (0.6, 0.05))")],
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
        print(f"{status:8s} {name}: {failed[:2] if failed else log.strip().splitlines()[-1:]}")
    killed = sum(v["status"] == "KILLED" for v in res.values())
    summary = {"source_sha256": hashlib.sha256(text.encode()).hexdigest(), "n": len(M), "killed": killed,
               "mutants": res}
    (scratch / "mutants_result.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(f"{killed}/{len(M)} killed")
    return 0 if killed == len(M) else 1


if __name__ == "__main__":
    sys.exit(main())
