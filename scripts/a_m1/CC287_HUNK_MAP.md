# A-M1 code v1 → v2 hunk map (CC-287, round 1 → round 2)

- v1: a_m1.py 7998a844 (1,144 l.), a_m1_mutants.py 6b439f34.
- v2: a_m1.py 8ddd825b, a_m1_mutants.py (sha in SHA256SUMS).
- The plan (A_M1_PLAN_v3.md 12d6ad3d) is unchanged.
- Line numbers are v2 lines from `diff -u v1 v2`.

## a_m1.py

| v2 lines | Item | Change |
|---|---|---|
| 16–60 | N1 | Docstring readings renumbered R1–R14 in file order. R2 is reworded: +inf rows shift both percentiles, and `rows_G_le_0` is recorded. New entries: R10 (gate final), R11 (`__pycache__` branch, plus the N4 prefix), R12 (`status` subcommand, torn result treated as absent), R13 (failed S0 records, W2), R14 (atomic JSON outputs, W3). |
| 224–232, 251–254 | N3 | `_code_sig` compares bytecode, names and constants recursively, without line numbers. `load_libs` asserts that the restated `Fault.__init__`, `Fault.__str__`, `sha_file` and the Fault base equal a_dchecks'. |
| 260–310 | W3, N2 HMa | `_dir_fsync` is shared, so one errno rule (R8) applies everywhere. `_fsync` can be injected by tests. `write_json` is atomic: serialize, O_EXCL temp file, fsync, `os.replace`, directory fsync. `load_result` treats an unreadable (torn) result as absent. |
| 443–458 | N1 | `rows_G_le_0` is added to V2-A and to every descriptive ε_k. |
| 489–493 | N2 HMa | `write_v1_atomic` uses `_fsync` and `_dir_fsync`: EIO raises; EINVAL/ENOTSUP are skipped and logged. |
| 526–551 | W1, W3 | `run_sets` fills a caller-supplied `res` in place (W3). A `budget.check()` after `compute` returns, before COMPLETED (W1, plan l.307/l.446). |
| 565–625 | W3, W2, N4 | `finish_after_failure` keeps the partial result and every in-memory V1, then recomputes the status from both artefacts. `s0_failed` sums the failed freeze and gate times and refuses on an unreadable record. `s0_attempt` writes a failed record with cpu_s/wall_s when an attempt raises, then re-raises. `stamp()` adds the pid. `fresh_pycache()` sets `sys.pycache_prefix` to a fresh temp dir. |
| 834–838 | N2 HMa (helper) | `stat_is_dir` for the injected-fsync test. |
| 1066–1238 | W1, W2, W3, N2, N3 | New selftest checks: W1 cap after V1 (NOT_RUN; VIOLATED is still FALSIFIED); HMi (a FAULT after a CONSISTENT V1, on either set); W2 summing helper; W2 raising attempt is recorded; W3 fallback (persist fails, first result write fails, the fallback gives FALSIFIED), atomic write and torn result; W3 JSON round-trip of a real `compute_set` output and its V1 dict, with the same `json.dumps` arguments; HMa; HMc; N3. |
| 1282–1348 | W2, N4, N5 | `freeze` and `gate` handle the refusal first (no attempt), then `fresh_pycache`, then `s0_attempt(_freeze/_gate)`. The freeze record notes `pycache_prefix`. G5 also requires sha(selftest.json) = freeze.json `selftest_sha256` (N5). |
| 1350–1408 | W2, W3, N4 | `run`: `fresh_pycache` first. The budget's cpu0/wall0 include the failed S0 time, and STARTED.json lists those records (W2). On any later exception, the fallback keeps the partial `res` with every in-memory V1 (W3), and replaces the empty NOT_RUN skeleton only when no readable result exists. |
| 1408–1415 | W3 | `status` uses `load_result`; a torn result is treated as absent and reported. |

## a_m1_mutants.py

| v2 lines | Item | Change |
|---|---|---|
| 1–6 | docstring | Scope now includes CC-287 W1–W3 and N2. |
| 57–64 | (target) | The `17c_non_atomic_write` target is moved to the V1 `data =` line, because the O_EXCL line now also occurs in `write_json`. The mutant is unchanged. |
| 68–91 | W1, W2, W3, N2 | Nine new mutants: W1_completed_past_cap, W2_failed_gate_time_ignored, W2_raising_attempt_unrecorded, W3_fallback_skeleton, W3_result_not_atomic, W3_torn_result_raises, HMa_dir_fsync_eio_swallowed, HMc_refusal_glob_narrowed, HMi_fault_after_v1_completed. |

## Not covered by a synthetic test (code-read items)

- **HMg:** the `refuse_if_records` call inside `run()`.
- **N4 effect:** `sys.pycache_prefix` is used in freeze, gate and run only.
- **N5:** the G5 sha comparison.

None of these can be exercised without real inputs. HMb (file fsync removed) and HMk (temp file not O_EXCL) stay low risk, as in CC-287.

## v2 → v3 (CC-287r2, round 2 → round 3; scope W3r2 and N-a..N-c only)

- v2: a_m1.py 8ddd825b, a_m1_mutants.py 07de25b1.
- v3: shas in SHA256SUMS.
- Line numbers are v3 lines from `diff -u v2 v3`.

### a_m1.py

| v3 lines | Item | Change |
|---|---|---|
| 278–317 | W3r2 | `write_json` gets a unique temp name per call (pid plus an `itertools.count()` counter). Any in-process failure (write, file fsync, close, rename) removes that call's temp file before re-raising. `_SimulatedDeath` (an OSError subclass) is the test-only "process died between fsync and rename" injection, and it leaves the temp file as a dead process would. |
| 617–633 | N-b | `s0_attempt(..., out_root=None)` writes the failed record under `out_root` (default data/results/a_m1/) through `write_json`. freeze and gate call it unchanged. |
| 1136–1164 | N-a, N-b | `w2_attempt` raises both a RuntimeError and a Fault (SystemExit). Both leave a failed record with cpu_s/wall_s, and both are summed by `s0_failed`. It runs in a scratch root and asserts that no `gate.failed_*` appeared in the live data/results/a_m1/. |
| 1188–1200 | N-a | Torn-read test, OSError case: a result file made unreadable (chmod 0) is "unreadable, treated as absent". The case is skipped if euid is 0. |
| 1208–1253 | W3r2 | New check `w3r2` (the CC-287r2 Check 6 path). EIO is injected through `_fsync` on the first FILE fsync of the result write, and the V1 write fails too. The check asserts that the first write raised, that the fallback wrote a readable result, that `status(read_v1(d), loaded) == "FALSIFIED"`, that `loaded["status"] == "FALSIFIED"`, and that no temp file is left. |

### a_m1_mutants.py

| v3 lines | Item | Change |
|---|---|---|
| 1–6 | docstring | Scope now includes CC-287r2 W3r2. |
| 72–83 | (targets) | `W2_raising_attempt_unrecorded` now targets the `write_json(path, {` line (N-b replaced `out_json(rel,`). `W3_result_not_atomic` now targets the new temp-name line. Both mutations are unchanged in intent. |
| 86–97 | W3r2 | New mutant `W3r2_fix_reverted`: it restores the per-pid-only temp name and removes the cleanup on failure. It is KILLED by the `w3r2` check, and by the W3 check as well. |

### Notes

- **N-c:** HMh (removing the in-set cap check in `compute_set`) is now equivalent. Since W1, the budget check after `compute` returns already makes a set past the cap NOT_RUN. The in-set check is kept because it stops the remaining compute early. No mutant is needed.
- **Judge probe** `/tmp/cc287r2/probe_tmp.py`, re-run at v3 (synthetic only):
  - "first write raised: [Errno 5] injected transient EIO on the first result fsync";
  - "dir after first: []", so no temp file was left;
  - "fallback wrote; status from file: FALSIFIED";
  - "final dir: ['a_m1_result.json'] status from records only: FALSIFIED".
- **NM10** is covered by the W3r2 assertion `loaded["status"] == "FALSIFIED"`.
