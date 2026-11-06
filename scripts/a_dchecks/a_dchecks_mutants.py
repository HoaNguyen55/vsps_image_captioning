#!/usr/bin/env python3
"""Mutant harness for scripts/a_dchecks/a_dchecks.py (pattern of scripts/c_pvr/c_pvr_mutants.py): the plan §5 list,
CC-266r3 N1''/N2'', and extra rule mutants.
Usage: <venv python> -I -B a_dchecks_mutants.py <scratch dir outside the repo>
Each mutant replaces one exact string (it must occur exactly once) and runs `selftest --out <scratch>/<name>.json` on
the mutated source, executed with __file__ = the original path so pins and imports resolve unchanged. The unmutated
source runs first and must exit 0 with 'selftest ok'. KILLED = exit != 0 and at least one named selftest check FAILED;
an exit before any check ran is CRASH, which is not a kill. Mutants run one after another."""
import json
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "a_dchecks.py"
LOADER = ("import sys; src, orig, out = sys.argv[1:4]; sys.argv = [orig, 'selftest', '--out', out]; "
          "ns = {'__name__': '__main__', '__file__': orig}; "
          "exec(compile(open(src, encoding='utf-8').read(), orig, 'exec'), ns)")

M = {
    # plan §5
    "d2_averaged_over_k": ("            d = D[m][k]\n", "            d = D[m].mean(0)\n"),
    "coco_get_fallback": ('return [set(gold[i]["coco"]) for i in ids]',
                          'return [set(gold.get(i, {}).get("coco", [])) for i in ids]'),
    "kernel_rank_off_by_one": ('Z = (ranks[:, None, :] < q[:, cell["seg"]][None]).astype(float)',
                               'Z = (ranks[:, None, :] <= q[:, cell["seg"]][None]).astype(float)'),
    "kernel_recall_over_l": ("rn = (Z * invq[..., seg]) @ Hw.T",
                             'rn = (Z / np.maximum(cell["ell"], 1)[seg]) @ Hw.T'),
    "S_changed_after_p": ('        if self.p_seen:\n            raise Fault("S changed after a p-value was computed")\n',
                          ""),
    "d5_rule_on_point": ('"label": d5_rule(lo1, lo2)}', '"label": d5_rule(float(s1[0]), float(s2[0]))}'),
    "d3_pass_without_sesoi": ('"label": "FAIL" if rej[k] else "PASS" if up <= SESOI else "UNDERPOWERED"}',
                              '"label": "FAIL" if rej[k] else "PASS"}'),
    "level5_at_real_K5": ('return (1, 5) if world == "W50" and arm == "U" else (1,)',
                          'return (1, 5) if arm == "U" else (1,)'),
    "d3_overlap_pass_first": ('"label": "FAIL" if rej[k] else "PASS" if up <= SESOI else "UNDERPOWERED"}',
                              '"label": "PASS" if up <= SESOI else "FAIL" if rej[k] else "UNDERPOWERED"}'),
    "d1_m_is_cells": ("return sum(len(LINEAR) * (n + 1) for n in nsys_per_cell), sum(nsys_per_cell)",
                      "return len(nsys_per_cell), sum(nsys_per_cell)"),
    "w50_shared_null_level5": ('return not (world == "W50" and arm == "U")', "return True"),
    # CC-266r3 N1'', N2''; task and review extras
    "level5_in_w50_arm_L": ('return (1, 5) if world == "W50" and arm == "U" else (1,)',
                            'return (1, 5) if world == "W50" else (1,)'),
    "m_sd_equals_m": ("return 3 * n_cells, n_cells", "return 3 * n_cells, 3 * n_cells"),
    "d3_p_rule_flipped": ("return float((1 + (b <= 0).sum()) / (len(b) + 1))",
                          "return float((1 + (b >= 0).sum()) / (len(b) + 1))"),
    "ks_direction_flipped": ('alternative="greater"', 'alternative="less"'),
    "d4a_bound_unadjusted": ("return 0.025 + inv(1 - 0.05 / m) *", "return 0.025 + inv(1 - 0.05) *"),
    "single_draw_at_m": ('return "PASS" if ks2_p >= 0.05 / m_sd else "FAIL"',
                         'return "PASS" if ks2_p >= 0.05 / (3 * m_sd) else "FAIL"'),
    "d5_or_instead_of_and": ("lower_gold >= D5_MIN and lower_all >= D5_MIN", "lower_gold >= D5_MIN or lower_all >= D5_MIN"),
    "x5_rule_dropped": ('if arm == "L" and sl < 2 *', 'if False and sl < 2 *'),
    # stop propagation has two guards (pre-check of the monotone cap, and `stop`); removing one alone is equivalent
    "cap_not_propagated": ('            budget.check()\n            res[name] = fn()\n        except CapReached as e:\n'
                           '            res[name] = {"label": "NOT_RUN", "reason": f"cap reached during {name} ({e})"}\n'
                           '            stop = f"cap reached during {name}"\n',
                           '            res[name] = fn()\n        except CapReached as e:\n'
                           '            res[name] = {"label": "NOT_RUN", "reason": f"cap reached during {name} ({e})"}\n'),
    "running_check_kept": ('res[name] = {"label": "NOT_RUN", "reason": f"cap reached during {name} ({e})"}',
                           'res[name] = {"label": "PARTIAL", "reason": f"cap reached during {name} ({e})"}'),
    "fault_stop_ignored": ('            if res[name].get("stop"):\n                stop = res[name]["stop"]\n',
                           "            pass\n"),
    "d1_linear_alpha_two_sided_005": ("t_lin, t_mix = inv(1 - 0.025 / m_lin)", "t_lin, t_mix = inv(1 - 0.025 / 8)"),
    "d2_no_holm": ('return {k: "FAIL" if rej[k] else', 'return {k: "FAIL" if False else'),
    "compound_any_level_rejects": ('rej = L["g"].compound([v for v, _ in parts]) == "PASS" if len(lev) > 1 else '
                                   'parts[0][0] == "PASS"', 'rej = any(v == "PASS" for v, _ in parts)'),
    "compound_p_min": ("out[m] = (rej, max(p for _, p in parts))", "out[m] = (rej, min(p for _, p in parts))"),
    "decide_pass_below_median": ('"PASS" if obs < lo else', '"PASS" if obs < med else'),
    "d1_stop_removed": ('        out["stop"] = "D1 linear FAIL: implementation fault (plan D1)"\n', "        pass\n"),
    "d4a_stop_removed": ('        out["stop"] = "D4(a) single-draw FAIL: implementation fault (plan D4(a))"\n',
                         "        pass\n"),
    "t2_any_set": ("all(any(v) for v in evaluable_by_set.values())", "any(any(v) for v in evaluable_by_set.values())"),
    # CC-271 B1: non-cap exits, one attempt, result in finally
    "b1_step_catch_removed": ("        except (Exception, SystemExit) as e:  # noqa: BLE001  (B1: a FAULT or error is recorded, "
                              "never escapes)\n", "        except ZeroDivisionError as e:\n"),
    "b1_marker_not_exclusive": ('with open(marker, "x", encoding="utf-8") as fh:', 'with open(marker, "w", encoding="utf-8") as fh:'),
    "b1_result_not_in_finally": ("    finally:\n        for n in ORDER:\n", "    if fault is None:\n        for n in ORDER:\n"),
    "ranks_key_order_swapped": ('np.lexsort((keys, np.broadcast_to(cell["seg"], keys.shape)), axis=-1)',
                                'np.lexsort((np.broadcast_to(cell["seg"], keys.shape), keys), axis=-1)'),
}


def run(src: Path, out: Path) -> tuple[int, str, dict | None]:
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
    for name, (a, b) in M.items():
        n = text.count(a)
        if n != 1:
            res[name] = {"status": f"BAD_TARGET (occurs {n} times)"}
            continue
        src = scratch / f"{name}.py"
        src.write_text(text.replace(a, b), encoding="utf-8")
        rc, log, rec = run(src, scratch / f"{name}.json")
        failed = [k for k, v in (rec or {}).get("checks", {}).items() if not v]
        status = "SURVIVED" if rc == 0 else "KILLED" if failed else "CRASH"
        res[name] = {"status": status, "rc": rc, "failed_checks": failed}
        print(f"{status:8s} {name}: {failed[:2] if failed else log.strip().splitlines()[-1:]}")
    killed = sum(v["status"] == "KILLED" for v in res.values())
    summary = {"source_sha256": __import__("hashlib").sha256(text.encode()).hexdigest(), "n": len(M),
               "killed": killed, "mutants": res}
    (scratch / "mutants_result.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(f"{killed}/{len(M)} killed")
    return 0 if killed == len(M) else 1


if __name__ == "__main__":
    sys.exit(main())
