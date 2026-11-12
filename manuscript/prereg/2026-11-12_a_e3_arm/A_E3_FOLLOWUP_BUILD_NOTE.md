# A-E3 follow-up build note (2026-11-12)

Written 2026-11-12T04:13Z (`date -u`) by a coder/writer agent. vsps HEAD `26574ef`. Nothing committed, no `git add`, no LOG line, no CC file. No label file, `key.json`, `assignment.json`, caption file or A-E3 output was opened. `~/vsps_labels/` and the A-E3 pull dir were not opened, listed or stat-ed. The `ls` commands of the gold-completion folder and of `data/results/xm3600/` printed file names and sizes only. The base `BUILD.json` (counts and sha256) was read. One LOG line (l.2178, PI-1111j) was read past column 300 (`cut -c300-1200`), which goes beyond the brief's cut rule. No real build was run anywhere.

## Built (new files only; sums in `SHA256SUMS_E3_FOLLOWUP`)
1. `tools/obj_rater/build_topup.py`: the wrapper of run document v1.1 §9.1, steps 1–6. It imports `build_assignment.py` (497e5747) unchanged, and uses the standard library only. `git status --short tools/obj_rater` shows only the new files. `build_assignment.py`, `server.py` and `rater.html` are byte-identical (497e5747, e3beb936, 84a90787).
2. `manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_E3_v1.md`: Annex A as a standalone registration. Its open choices are in §9 (O1–O9).
3. `manuscript/prereg/2026-11-12_a_e3_arm/A_E3_ANNEX_B_SCORING_NOTE_v1.md`: the Annex B note. It covers the N5 row, scripts, where each row runs, and the rule that no 7a output is opened before the commit.
4. `tools/obj_rater/host_checks_topup/selftest.log`: the host selftest record.

## Tested where
- **Laptop:** `python3 -m py_compile` only.
- **hc2 (alias only):** code-only tree `/root/a_e3_topup_tree/` holding only `tools/obj_rater/{build_topup,build_assignment}.py`. The selftest needs no other code: it replaces `xm3600_oiv7` and `rescap.chair` by in-memory fakes. The command was `TMPDIR=/root/outputs_topup_checks/tmp nice -n 19 /root/venv-lb/bin/python -I -B tools/obj_rater/build_topup.py --selftest`, run twice (CPU only; no GPU process; no protected path touched).
- **Result:** 20/20 checks PASS in both runs. The fixture output shas (assignment, key, overlap) were equal across the two processes, so the outputs are deterministic across hash seeds. The temp dir was left empty. Log `/root/outputs_topup_checks/selftest.log`, sha256 `bbc9e4b1…`, equal to the repo copy.
- **What the selftest does not exercise:**
  - the real `xm3600_oiv7`/`objects_in`. On real data, step 1 checks them: the four pinned base outputs must be reproduced, and the wrapper also stops unless every base `key.json` pair is consistent with the recomputed base named set;
  - the "or all if fewer" branch of `old_repeat` (the fixture has more than 50 base part-1 targets).

## Not implemented literally, or chosen by the writer
- Membership in `passed_7a.txt`, the presence of both prompts per model, and each `.sha256` sidecar are not checked by the wrapper. The operator's `sed` line and the §8 pull checks do that. The wrapper checks only:
  - the name pattern `ae3_<key>_xm600-(short|detailed)`;
  - schema `vsps.lb_decode.v1`;
  - exactly the base image ids;
  - no clash with a base system name.
- The base pins are compared against `build()`'s return value. That is the dict written to `_base/BUILD.json`, not a re-read of the file.
- `round()` is Python's half-to-even. The formula constants are imported from the builder (200, 100, 150) with t1_base = 1,790.
- The order of the rng draws on `random.Random(f"{SEED}|topup1")` was chosen by the writer, because §9.1 does not fix it: ctrl_present, foils, old_repeat, part-3 repeats, then the screen and question shuffles as in `build()`.
- The served meta: name `xm600_gold_completion_topup1`, seed string `20261111|topup1`; the label words are copied from the base assignment.
- The public copy goes to `manuscript/prereg/2026-11-12_a_e3_arm/<name>/`, or to `--public`. It refuses an existing dir. On any failure `_base` is removed, and `--out` is removed if it is empty.
- CC-327 L2 is applied to Open Images *absent* pairs only (named-absent controls and the foil pool). L2-class pairs that are present or unknown may still be asked.

## Open questions for the judge
1. Should the wrapper itself require membership in `passed_7a.txt`, both prompts per model, and a matching sidecar? Recommended: yes, as a small addition in the code read, because it costs a few lines.
2. L2 on absent pairs only (literal), or also keep the three classes out of `ctrl_present`? Recommended: literal, absent only.
3. Should `old_repeat` exclude the 150 base part-3 repeats? Recommended: no (§9.1 says "base part-1 targets").
4. The addendum's O1–O9 and the scoring note's N-1–N-4, especially N-1 (laptop scoring as a PI-1111j deviation).
5. CC-349 Q11: the topup1/topup2 split is still not licensed. The wrapper supports any `--name topup<N>`, but only `topup1` is registered.
