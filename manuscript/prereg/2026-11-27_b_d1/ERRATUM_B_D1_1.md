# ERRATUM B-D1-1 to the B-D1/A3 registration (PREREG_DRAFT_B_D1_A3_v3.md bf3a55f7, COMPUTE_B_D1_v2.md 92244910; commit adebac7): host rule

Written by ruling CC-506e1 (2026-11-27), before use.
- No D1 or A3 quantity exists: no `PER_IMAGE_D1.npz`, `G0.json` or `RESULT_D1.json`.
- The one host session (2026-11-27) ran S0 only. S0 stopped in its environment part. No data was pushed. The host was wiped and deleted.
- This erratum changes no hypothesis, threshold, floor, seed, split, estimand, data set, gate, stage order or the 8 CPU-h hard stop. It replaces only the host rules.

**Why.** The registered rule ("rented host only"; "the PI's own PC is not used") rested on PI-1127h: the project rented when money allowed, and the PI's PC was neither the default nor switched on (CC-505 ruling 9). The PI has replaced that rule (PI-1127m, LOG 2026-11-27T13:54:47Z): no new rentals, and his PC is used and kept on when needed. The same change was ruled for FE-LOCUS (CC-510e2).

## E1. Replacement for PREREG v3 §6, bullet "Host"

**Host (CC-505 ruling 9 as amended by CC-506e1).** S0, S1 and S2 run on the PI's PC, under the record checks H1–H8 below. The laptop writes files only. Details are in `COMPUTE_B_D1_v2.md` as amended by this erratum, including the **hard stop at 8 CPU-h**. S0, S1 and S2 all run on the same host. A move between hosts after S0 has started needs a new judge line.

## E2. Replacement for COMPUTE_B_D1_v2.md, the first three bullets of "Where it runs" and the last bullet of "Custody"

**Host: the PI's PC (PI-1127m).** No new rental, and so no money order. The laptop writes files only. No host alias, IP or port appears in any registered or committed file.

**Record checks.** Each check is written to the session record before the step it guards.
- **H1 Own folder.** Every D1 file lives in one new folder in the agent's own work area on that machine, for example `~/vsps_host/b_d1`.
  - The code tree is `<folder>/b_d1_tree`.
  - The venv, the wheels, `ncs-data`, the records, the outputs and the pinned Java and Python are siblings of the tree inside `<folder>`, never inside the tree, because the closure check would see them.
  - `host_selftest.sh` is run with `BD1_BASE=<folder>`.
  - Nothing is read or written outside the folder. No other study's folder and nothing of Paper A is touched (PI-1127a).
  - One exception is allowed: if GNU `time` (`/usr/bin/time`) is missing, the Ubuntu `time` package may be installed with the PI's sudo. That step and its version are recorded, and nothing else is installed system-wide.
- **H2 Push by tar, no repository.**
  - The code tree is `git archive` of the commit named in the S0 pin. It holds the 25 PINS files, the registration and `scripts/b_d1/`.
  - The data tar holds the 73 own output files, the 2 baselines, `test_data.json`, `DEV.json`, `RESULT.json`, `FAMILY.json`, `CENSUS.json` and `SYSTEMS.tsv`. It is pushed only after the S0 record is pinned (CC-506 W5).
  - For each tar, the sha256 is printed on the laptop before the push and matched on the host after it.
  - `find <folder> -name .git` returns nothing before S0.
- **H3 Environment.**
  - The interpreter is CPython 3.12.3 (`PY3`). Java must report `21.0.13.0.3`. The VnCoreNLP 1.2 jar has a sha256 beginning `9e2811cd`, and the wheels are those of `WHEELS_SHA256.txt`.
  - Python and Java are installed inside `<folder>` without system changes.
  - A build from another fetch source is allowed only if its version string is identical. The source and the sha256 of the archive are then recorded ("same version, different fetch source", as for the deleted host's Java).
  - `env_check` and the S0 self-tests and mutants pass on this host through `host_selftest.sh`.
  - G0 is the numeric check of the environment: any difference is a FAULT, not a substitution.
- **H4 CPU stop.**
  - Every stage, S0 included, runs under `run_stage.sh`. It records the user and system time of the whole waited process tree (GNU `time -v`) and sets `prlimit --cpu` to the seconds left as a per-process backstop.
  - The cumulative check refuses or discards any stage at 28,800 CPU-seconds, counted from the first S0 on this host.
  - A STOP writes a judge line, and nothing runs again without one.
  - `nice -n 19`, `CUDA_VISIBLE_DEVICES=` (no GPU).
- **H5 No overlap with C-CONF.**
  - No D1 process runs on that machine from 2026-11-28T09:00Z until the LOG carries the C-CONF test session's end line, or the C-CONF chair's line that C-CONF will not use this machine. If CC-481 names other hours, the window is from 30 minutes before its staging until its session-end line.
  - Before every stage and at the window's start, `pgrep -af` for `b_d1.py` and `run_stage.sh` is run and its output recorded.
  - A stage that could still be running at the window's start is not started.
- **H6 Pull and pin.**
  - `PER_IMAGE_D1.npz`, `S1.json`, `G0.json`, `RESULT_D1.json`, the `.time` records and the S0 record are pulled to the laptop's home file system, not to `/mnt/d`.
  - Each is checked against the sha printed on the host, pinned on the LOG and set to mode 444.
  - The order of CC-506 ruling 5 and prereg §6 is unchanged: S0 pin, then data push, then S1 pin, then G0 pin, then S2 pin.
- **H7 Wipe.**
  - After H6 the whole folder is deleted on the host: both tars, the references, the output files, the matrix and the environment.
  - `ls` on the folder path, showing it absent, goes to the session record. If the `time` package was installed under H1, that is recorded too and the package is left in place.
- **H8 No text.** No caption or reference text is printed or kept outside the folder, and nothing is committed from that machine.

## E3. Text left as it was
- PREREG v3 §§0–5, §6 apart from its Host bullet, and §§7–11 are unchanged.
- COMPUTE_B_D1_v2.md is unchanged apart from E2: the CPU estimate, the hard stop, the inputs by sha256, "Not needed" and the custody of the matrix.
- Where these files say "the host" or "the rented host", they now mean the PI's PC under E1–E2.
