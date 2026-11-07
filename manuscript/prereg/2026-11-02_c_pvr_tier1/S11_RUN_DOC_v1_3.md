# C-PVR-T1 tier-1 GPU block run document S11 v1.3 (Paper C, ACM TALLIP; plan S11-S15; prereg §10.1, host v3): DRAFT for its one-judge read

**Status (v1.3):** DRAFT v1.3 for the one-judge FULL read CC-286r3, round 3/3, the last (CC-286r2 REQUIRED FIXES),
REVERSIBLE 85 (PI-1029o as amended by PI-1103ae). It supersedes `S11_RUN_DOC_v1_2.md` 0433d523, `S11_RUN_DOC_v1_1.md`
e87fb032 and `S11_RUN_DOC_v1.md` 4710e265 (all three unchanged, untracked). **Scope of v1.3:** CC-286r2 W5-W7
(BLOCKING) and the doc-text NON-BLOCKING N-a to N-i (item map §A0). Nothing else changed from v1.2. It licenses nothing
until its GO and the registration commit of exactly this file. Nothing in it has been rented, pushed, run or
committed. v1 written 2026-11-07 about 02:30-03:05Z; v1.1 about 03:10-03:31Z (LOG 03:31:22Z); v1.2 about 04:00-04:08Z
(the v1.2 NGRAM line is OPS-1107c-s11v12-ngram); v1.3 about 04:20-04:45Z (`date -u`). HEAD = H = 1880951. AI opinion throughout; every
time and cost marked [est.] is an estimate, and every value marked **[proposal]** is fixed by this file before any
output.
- **Label:** TIER 1 / DEV-EXPLORE (C-PVR-T1).
- **Rental trigger.** The GO of this file is the rental trigger of host v3 l.5-6 (`AMENDMENT_HOST_3090_DRAFT_v3.md`
  e9c04955, commit 5d6f5ca). The rental itself still needs §4 (preconditions) and §5.1 (L-before).
- **The two v1 placeholders are filled (v1.1).**
  - **TMAN** = `4849a08f1fc384f1901fd294950f9ea20a5622879838c4a5ecac73cec62c3efe`, the sha256 of the sealed `MANIFEST.sha256` from H4: TMAN_N = 11,571 lines, out dir
    `/home/hoanguyen/c_pvr_h4_1107` (OPS-1107c-h4; H4 record `~/c_pvr_h4w_1107/H4_RECORD.txt` 36464741).
  - **H** = `1880951352c532456e29e5bbfb42e0733d3a97c1`, the R-P6 commit (CC-284 GO 88; OPS-1107c-r-p6-committed). It sets `c_pvr_job.sh` l.24-25 to
    `9a0745307b3b8d7c4e4c195bc78e2e1a9a52eb5046fd6f438c6402802fe9c09f` and
    `8e8a13c359b3e7e549f9006ddfce61a9e1d15b3d9046884c23d2938a8d87afcc` (E-G instance, OPS-1107c-emb).
- **Format.** House style of `W25_DEV_RUN_DOC_v1_4.md` (4d5f707c, registered 186af09) and its committed addendum
  `W25_DEV_RUN_DOC_v1_5_ADDENDUM_r2.md`. Committed documents are cited by sha, not restated.
- **PI lines cited (CC-280 AM6):**
  - PI-1106j: the E-G instance, with its money inside C's block S;
  - PI-1106k: the KT-C fetch departure;
  - PI-1106l: the speed stop of 3.0 h, which amends host v3 H-9;
  - PI-1106m: the laptop stays on for the whole job (watcher, backups, final pull);
  - PI-1107a: CPU floor Ryzen 7 5800XT class, and Ubuntu 22.04 with deadsnakes python3.12;
  - PI-1104ae: 1× RTX 3090 / 3090 Ti only.
- **Sources read:**
  - PRE_S11_PLAN_v1.md (bb2f5eec) §8-§11;
  - CC-280 (AM1-AM9, AD1-AD6, WORK LIST), CC-270 (Rulings 6-8, Q2-Q6, N1-N14), CC-270r2 (N-S11a-e), CC-272 (Ruling
    2, N1-N9), CC-273 (N1-N8), CC-276 (W5, W6), CC-277 (Rulings 1-11, H1-H5, N1-N4), CC-278 (W7), CC-279 (N2, N4),
    CC-281 (N1-N9, O3), CC-282 (Rulings 1-15, N1-N8), CC-283 (Rulings 3, 5-7, N1-N5), CC-284 (Rulings 1-8, N1-N5; v1.1);
  - host v3 §1-§6, T1-REP v4 §9 (4124ef3), R_EMB_JOB_SHEET_v1.md (b36faf46 at H, with the R-P6 step-8 erratum;
    dc23ed40 before), C_NEXT_STEPS_2026-11-04 rows S11-S16;
  - LOG l.1729-1770: the E-G lines OPS-1107c-eg-*, OPS-1107c-h4, OPS-1107c-a12-delete, CC-284 and
    OPS-1107c-r-p6-committed in particular; the H4 record `~/c_pvr_h4w_1107/H4_RECORD.txt`;
  - code at H (1880951): c_pvr_job.sh 9532c085, setup_host.sh 4779afa8, c_pvr_watch.py 3a4c60f8, c_pvr_gpu.py 9a9c6eb5
    (l.1-130, 486-800, 1630-1720), c_pvr_manifest.py bb7c6c9a (l.1-40, 206-240);
  - the E-G pull `.session_backup/machines/EG/root/` (setup logs, probe json; §19).

## A0. Changes from v1.2 0433d523 (CC-286r2; item map, each with its section)

| # | CC-286r2 item | v1.2 text | v1.3 |
|---|---|---|---|
| W5 | §10.2 ENV4 sentence | "the exact `env -i …` prefix … copied from the H4 OPS line" (stale v1.1 text) | replaced by the §1.3 description (H4 form, no `env -i`, inherits HOME / PATH, P21 checks the decomposers under it). No other ENV4-source text names an H4 OPS line |
| W6 | rental gate | §0 rows 3-4 said "P1-P20" | row 3 = P0a-P0d, P1-P19, P21, P22; row 4 gate = the same set PASS; P20 after the rental, before push 1 (§0, §4 head) |
| W7 | resume watcher | RS-8 had no command; RS-1 could wait forever | §11.3: an exact RS-8 relaunch block (old pid file moved to a UTC-stamped name, the §10.2 self-pid line, T_J1 read back from pre.txt, cmdline recorded) and an RS-1 block (kp, a bounded 60 s lock wait; kp ≠ 0 or the lock still held = OPS line, a bracketed listing of live watchers, STOP for the PI) |
| N-a | env sourcing | RS-1, RS-6, §13.2 and the §9.5 U line did not source the env file | each starts with `. "$HOME/s11_env.sh";` |
| N-b | §9.5 pull list | job.log, timing.jsonl | plus sizes.json and CAP.json |
| N-c | U, SHORT | no unit | integer seconds; SHORT = U is the no-launch branch |
| N-d | P22 output | a bare number | `echo "P22 <n>"` |
| N-e | `$!` sentence | "NOT reliable when the shell has job control" | softened to what was seen in one shell; the self-written pid is right either way |
| N-f | §12 decomp alert | repeated every 30 min | each flagged line is alerted once (`$PRE/decomp_flagged`) |
| N-g | P18 | run.log only | wall times from run.log, text counts from OPS-1107c-h4 (demos column) |
| N-h | top-up tar | no link-member tee | the same tee as the main streams |
| N-i | pull-loop children | kp stops only the parent bash | `kpg` stops the loop's whole process group (it is a setsid session leader; tested); §13.3 still waits for nothing to run |

## A0-v1.2. Changes from v1.1 e87fb032 (CC-286; item map, each with its section)

| # | CC-286 item | v1.1 text | v1.2 |
|---|---|---|---|
| W1 | DOC pointer | `DOC=` named the v1 file | `DOC=…/S11_RUN_DOC_v1_2.md` (§1.3). P1 also requires the file to be tracked. Every other mention of v1 / v1.1 is a history line (status, §A0, §A, §19) |
| W2(a) | ENV4 | a placeholder with a source that does not exist | `ENV4='env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1'`, the H4 form (run_sets.sh l.5); it inherits HOME and PATH (§1.3) |
| W2(b) | real decomposers | not exercised before the launch (P11 is fake) | P21 + §4.1: decompose_vi / decompose_en on four fixed synthetic sentences under ENV4; tested PASS; negative controls fail closed |
| W2(c) / AD1-a | failure threshold | none | §10.3: M > 50 % of N on any set = systematic: read while phase 1 runs, DEGRADED label if A8 / S2 ran; below = record only; pull-loop flag (§12) |
| W3 | §9.5 FAIL branch | "shortfall can only fall on phase 3" | SHORT < U (uncut phase-3 seconds by `project()`) = launch; SHORT ≥ U = no launch, PI; §10.1 sentence corrected |
| W4 | process stops | `-f` pattern stops / counts in RS-1, §13.2, P14 | pid files (§10.2) and the `kp` helper with a cmdline check (§1.3); bracketed listing patterns (P14, P15, §10.2); P22 check |
| N1 | T_J1 clock | laptop `date -u` | `ssh hc1 date -u`; skew check < 60 s (§6.2) |
| N2 | env sourcing | §8.1, §9.1, RS-7 used $H / $TMAN unsourced | source line + non-empty check |
| N3 | `.torn` | "wb", one name | `.torn.<UTC stamp>`, "xb" (RS-3) |
| N4 | manual wipe | named only | exact command (RS-2; §14.1 cites it) |
| N5 | top-up / §13.1 | described | `sed` list command and tar re-send (§7.2); `[ ! -e /dev/shm/c_pvr_hc ]` (§13.1) |
| N6 / N7 | NGRAM line; records | D-R12 open | P0a-P0d; P0a met by OPS-1107c-eg-repo-record (§1.4) |
| N8 | v1.1 window | "03:30-03:55Z" | 03:10-03:31Z (LOG 03:31:22Z) |
| N9 | PQ-S11-4 | re-push from the last pull | an addendum read first, with the reasons (§18) |
| N10 | P18 source | "H4 build log" | H4 run.log wall time / texts; HB_MAX 1800 s stands (P18) |
| N11 | balance check | "with the pull loop's coordinator check" | the coordinator, by hand, with an OPS line; a missed check is logged, not a STOP (§5.3) |

## A. Changes from v1 4710e265 (each cites its source)

| # | item | v1 text | source | v1.1 |
|---|---|---|---|---|
| V1 | H | placeholder "the R-P6 commit" | OPS-1107c-r-p6-committed | `H` = 1880951352c532456e29e5bbfb42e0733d3a97c1 everywhere (header, §0, §1.2, §1.3 env, P2) |
| V2 | TMAN | placeholder | OPS-1107c-h4 | 4849a08f…3efe, 11,571 lines; TMAN_BYTES 2,199,372,292 measured; NEED 2,749,215,365 B (§0, §1.2, §1.3, §2, P6, P10, §7.2) |
| V3 | code shas | c_pvr_gpu 1179c4b3, job.sh 41a633be, gpu SUMS ed6d5226, sheet dc23ed40 | CC-284 N4 | 9a9c6eb5, 9532c085, b8e62ba5, b36faf46 (header sources, §1.1 table, §8.2 C2 expected value) |
| V4 | job.sh line cites | l.29, 32, 47-61, 48, 51, 52-53, 55, 58-61, 62-63, 67-68, 69, 72-74, 78, 85, 87, 90, 102, 106 | CC-284 N4; job.sh at H | +2 after l.25: l.31, 34, 49-63, 50, 53, 54-55, 57, 60-63, 64-65, 69-70, 71, 74-76, 80, 87, 89, 92, 104, 108 (verified against H); c_pvr_gpu CODE l.37-38 → l.38-39 |
| V5 | regular files on tmpfs | `tar -h`; arrival `find . ! -type d` count | CC-284 N1, Ruling 3 | per-stream link-member count (tee, must be 0); extraction `--no-same-owner`; arrival `find . ! -type d ! -type f` = 0 (§7.1, §7.2) |
| V6 | direct probe calls | not mentioned | CC-284 N3, Ruling 5 | §8.1: none in S11; if one is ever needed, the exact `export C_PVR_FREEZE=… C_PVR_FREEZE_EN=…` of job.sh l.54-55 precedes it, `--out ~/c_pvr_out/probe` |
| V7 | EN freeze ≠ 8e8a13c3 on HC-1 | not covered (only the main-freeze fallback) | CC-284 N5, Ruling 7 | §1.1 fallback; STOP at §6.5 (setup.log), backstop job.sh l.76, no decode; §8.2 C7 |
| V8 | H4 push sources | "the H4 lines name the --images dir" | OPS-1107c-h4; H4 record | `$O` = ~/c_pvr_h4_1107 (manifest, democap), `$EP` (5 sets), `$K` (kt_c), kept by exact name (§1.3, §2, §7.1); per-set manifest shas in §2 |
| V9 | P7 | conditions only | OPS-1107c-h4, OPS-1107c-a12-delete | stated as met |
| V10 | sparse clone test | at 9b3fd8d | v1.1 re-run | repeated at H: 36 blobs, SUMS OK, selftest rc 0 at 9a9c6eb5; the "filtering not recognized" warning noted, blob count binding (§1.4, P5) |
| V11 | money | balance example only | LOG l.1761-1770 | last balance 759,965 VND, no rental since, Σ R_j = 0; S 38,493 unchanged (§5.1) |
| V12 | carried table, rulings | CC-282 N2 / N7 open | CC-284 | closed by CC-284; CC-284 N1-N5 rows; D-R14 (§16, §17) |

**Brief text for every agent of this run (CC-281 N9, verbatim):** "No command may name ~/.vsps_sealed, including
ls/find/grep with output discarded; ACCESS_LOG is referred to as 'the file of hand row 52/53' and only the coordinator
appends." This run needs no sealed-custody access and no new hand row (§19). Further rules:
- no `t2pool_*` file is opened, and `c_datastores/` is never listed or globbed: kept files are taken by exact KEPT
  name only (CC-276 W5);
- no test caption or label, and no NoCaps-test, OI-test or tier-3 material, goes anywhere;
- never `rm -rf`, and new dir names after a failure (CC-273 N8);
- no host, IP, port or password in any repo file or LOG line: the host is `hc1`, an `~/.ssh/config` alias;
- every LOG stamp comes from `date -u` (memory rule).

## 0. Summary

| item | value |
|---|---|
| What runs | on HC-1 (one rented RTX 3090 / 3090 Ti): S12 GPU-host selftest (`c_pvr_job.sh selftest`), S13 speed test (`speed`, 18 steps), S14 P1 line (`c_pvr_gpu.py cap`), S15 tier-1 block (`tier1`, 72 steps in three phases). On the laptop: the a1_decomp watcher, the 30-min pull loop, the final pull |
| Host | HC-1, GPU_RENTAL_SPEC as amended by PI-1107a (§5.2); deleted after the final pull |
| Code | `H` = 1880951 (the R-P6 code commit, §1.1). scripts/c_pvr_gpu SUMS b8e62ba5 and scripts/c_pvr SUMS at `H` |
| Arrival set | sealed `MANIFEST.sha256`, TMAN 4849a08f, 11,571 lines: 6 manifests, 3 democap files, 3 kept files, 11,559 query images (xm3600_vi 3,600, kt_c 3,907, ktvic_explore 286, openviic_explore 1,020, vitextvqa_dev 1,676, t_a 1,070). TMAN_BYTES = 2,199,372,292 (exact sum over the 11,571 laptop source files, v1.1) |
| Money | M = 350,000 VND (465,000 under PQ-C2, after every cut). S already spent = 38,493 VND (m9 20,864 + E-G 17,629). H_350k at the P1 line ≈ 22-26 h (§5.3), so cuts are certain at P1 ≥ 21 h |
| Time | about 3-4.5 billed h before the P1 line [est.], then the cap (≈ 22-26 h). Laptop on and online for about 30 h (PI-1106m) |
| Gold | none on HC-1: ids, booleans (A12 masks), demonstration texts and pixels only (host v3 §5; CC-277 Ruling 11) |
| New download | none on the laptop. On HC-1: pinned weights and the 12 pinned LLaVA code files only (setup_host.sh) |

**Order and performers.** Each laptop shell block starts with `. "$HOME/s11_env.sh"` (§1.3).

| # | step | who | gate |
|---|---|---|---|
| 1 | R-S11 read of this file (TMAN and R-P6 filled in first, §1.2) | one judge | GO 85 |
| 2 | registration commit of exactly this file | gatekeeper | after 1 |
| 3 | preconditions P0a-P0d, P1-P19, P21, P22 (§4) into `$PRE/pre.txt` | coordinator | all PASS |
| 4 | L-before (§5.1), offer check (§5.2), rent, rental line `OPS-<MMDD>c-hc1-rent`; then P20 (after the rental, before push 1) | coordinator; PI only if no offer passes | P0a-P0d, P1-P19, P21, P22 PASS (P20 before push 1) |
| 5 | host prep, setup checks, sparse repo, `setup_host.sh` (§6) | coordinator | every check PASS |
| 6 | push 1 + S12 selftest (§7, §8); S12 output read (pre-queued) | coordinator; one judge | §8.2 criteria |
| 7 | push 2 + S13 speed test (§7, §9.1-§9.3) | coordinator | S12 GO |
| 8 | push 3 + L-P1 + S14 `cap`, the load check, the P1 line (§9.4-§9.6) | coordinator (mechanical) | `decision` RUN |
| 9 | S15 launch: job, watcher, pull loop in one shell call (§10) | coordinator | right after 8 |
| 10 | watch; stops and resume (§11, §12) | scripts; coordinator; one judge on a STOP | – |
| 11 | final pull, verification, wipe, L-final, delete, L-after (§13, §14) | coordinator | job DONE or cap stop |
| 12 | result-read hand-off (§15) | coordinator | after 11 |

## 1. Code, environment and the same-sha rule

### 1.1 Which sha runs
- **`H`** = the R-P6 gatekeeper commit (FREEZE_SHA / FREEZE_SHA_EN set, CC-280 WORK LIST 9), always. This file's own
  registration commit and other papers' commits may come later; they must not touch the code (P3). The host gets `H`
  exactly (§1.4 checks out `H`), so job.sh's `EXPECT` is `H`.
- Code pins expected at `H`, re-hashed by P3. Any change here is a new `H` and needs a diff read.

| file | sha at H = 1880951 | changed at R-P6 (vs 9b3fd8d)? |
|---|---|---|
| scripts/c_pvr_gpu/c_pvr_job.sh | 9532c085 | yes: l.24-25 pins; CC-282 N7 folded in: yes (l.62 `find . ! -type d`); lines after l.25 move +2 (freeze export l.54-55, compare l.74-76) |
| scripts/c_pvr_gpu/c_pvr_gpu.py | 9a9c6eb5 | yes: CC-282 N2 folded in: yes (hostcheck_fresh also checks the recorded freeze against C_PVR_FREEZE / _EN; unset = FAULT). HOSTCHECK on HC-1 must record 9a9c6eb5 |
| scripts/c_pvr_gpu/setup_host.sh | 4779afa8 | no |
| scripts/c_pvr_gpu/c_pvr_watch.py | 3a4c60f8 | no (CC-282 N6 is carried, §10.4) |
| scripts/c_pvr_gpu/c_pvr_manifest.py | bb7c6c9a | no (the H4 builds ran at it) |
| scripts/c_pvr_gpu/requirements_c_pvr_gpu.host.lock | 966eb327 (venv name LK) | no |
| scripts/c_pvr_gpu/requirements_c_pvr_llava.lock | d2f0f262 (venv name LKE) | no |
| scripts/c_pvr/c_pvr.py, c_pvr_run.py | a503644a, 0c80ee68 (c_pvr_gpu CODE l.38-39) | no |
| scripts/c_pvr_gpu/SHA256SUMS | b8e62ba5 | yes, with the files above (c_pvr_gpu_mutants.py c65bbf16) |
| manuscript/prereg/2026-11-02_c_pvr_tier1/R_EMB_JOB_SHEET_v1.md | b36faf46 | yes: the labelled step-8 erratum (a record; E-G is done) |

- **Same-sha rule (binding).** No byte of `scripts/c_pvr_gpu/` or `scripts/c_pvr/` changes from the S12 selftest until
  the S15 final pull. A change means a fresh S12 (hostcheck_fresh refuses older HOSTCHECK files) and a new read.
- **Freeze.** job.sh l.54-55 and l.74-76 recompute both venv freezes at every job start and compare them with FREEZE_SHA /
  FREEZE_SHA_EN. HC-1 reproduces 9a074530 by construction (CC-280 AM1: `--require-hashes --no-deps` from host.lock
  966eb327; setup_host.sh l.59 STOPs on a difference). **Fallback (PRE_S11 §7, kept by AM1):** a difference stops setup
  before any push. Then pull `setup.log`, `pip_report.json` and both freeze files, wipe, delete, and the R-P6 reader
  rules. Billed cost about 0.3-0.5 h [est.].
- **EN freeze on HC-1 (CC-284 N5, Ruling 7).** 8e8a13c3 has been seen on one host only (E-G). setup_host.sh l.86
  compares the EN freeze only with its own first build, so the first check against 8e8a13c3 is this file's §6.5 (the
  `EN lock installed: freeze …` line of setup.log). A difference = **STOP there, before any push and any decode.**
  The binding backstop is job.sh l.76 at the first `speed` or `tier1` start, also before any decode.
  - Fallback: `~/venvs/c_pvr_llava_d2f0f262/bin/python -m pip freeze > ~/c_pvr_out/en_freeze.txt`, then pull it with
    `setup.log` and `gpu_lock_llava_d2f0f262/freeze.sha256`, and report.
  - A one-judge diff read rules on any FREEZE_SHA_EN change. That change is a job.sh diff, so a new `H` and a fresh
    S12. No decode until then; the delete-when-idle rule applies if the wait exceeds about 1 h.
- **Env disclosure (CC-280 Ruling 2(b)).** The EN embedding pair (def163d3 / 6e8bdba2) came from torch 2.5.1 /
  transformers 4.57.6 on M3. The seven fresh VI/TC npz came from the main lock (torch 2.6.0 / transformers 4.51.3) on
  E-G. Each query/datastore pair stays inside one run, env and dtype.

### 1.2 Filled values (v1.1; the reader checks each against its LOG line)
- `H` = 1880951352c532456e29e5bbfb42e0733d3a97c1 (OPS-1107c-r-p6-committed; `git rev-parse HEAD` at drafting).
- `TMAN` = 4849a08f1fc384f1901fd294950f9ea20a5622879838c4a5ecac73cec62c3efe, `TMAN_N` = 11,571 = 6 + 3 + 3 + 11,559 (OPS-1107c-h4; re-hashed at drafting from
  `/home/hoanguyen/c_pvr_h4_1107/MANIFEST.sha256`).
- `TMAN_BYTES` = 2,199,372,292, the exact sum of the 11,571 laptop source files (§7.1 mapping, `stat -c %s`, v1.1).
- The H4 STOP lines (CC-282 N1) are in OPS-1107c-h4, and the a12 output deletion is OPS-1107c-a12-delete (P7).
- Still open, written by the coordinator on the rental day: the rental-line values (§5.2) and S at L-P1. `ENV4` is
  fixed in §1.3 (v1.2).

### 1.3 Notation (env file; written once, on the rental day)
```sh
[ ! -e "$HOME/s11_env.sh" ] || { echo "GUARD: s11_env.sh exists"; exit 1; }
{ echo "D0=$(date -u +%m%d)"; cat <<'EOF'
R=/mnt/d/vsps_image_captioning
L=.session_backup/2026-10-13/decisions/LOG.md
CV=$HOME/.venvs/c_pvr/bin/python
H=1880951352c532456e29e5bbfb42e0733d3a97c1
TMAN=4849a08f1fc384f1901fd294950f9ea20a5622879838c4a5ecac73cec62c3efe
O=/home/hoanguyen/c_pvr_h4_1107
EP=$HOME/c_pvr_eg_1107/emb_push/images
K=/home/hoanguyen/c_pvr_ktc_1106
KM=f4d8e5e44d1a9cc48e0ad026d2fb3c12dbf8a8f6bdb6614e3798500c95245171
DS=/mnt/d/vsps_image_captioning/.session_backup/2026-11-06/c_datastores
ENV4='env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1'
DOC=manuscript/prereg/2026-11-02_c_pvr_tier1/S11_RUN_DOC_v1_3.md
EOF
} > "$HOME/s11_env.sh"
cat >> "$HOME/s11_env.sh" <<'EOF'
PRE=$HOME/s11pre_$D0
PUSH=$HOME/s11push_$D0
W=$HOME/c_pvr_watch_$D0
PULL=$HOME/s11pull_$D0
HR=$HOME/s11hr_$D0
kp() { p=$(cat "$1") && tr '\0' ' ' < "/proc/$p/cmdline" | grep -qF -- "$2" && kill -TERM "$p"; }   # §10.2, W4: pid file, never a pattern
kpg() { p=$(cat "$1") && tr '\0' ' ' < "/proc/$p/cmdline" | grep -qF -- "$2" && [ "$(ps -o pgid= -p "$p" | tr -d ' ')" = "$p" ] && kill -TERM -- "-$p"; }   # the same, whole process group (CC-286r2 N-i)
EOF
chmod 400 "$HOME/s11_env.sh"; sha256sum "$HOME/s11_env.sh"
```
- `KM` is the full sha of `/home/hoanguyen/c_pvr_ktc_1106.sha256` (OPS-1107c-ktc), never a prefix. `H`, `TMAN` and
  `O` are filled from their LOG lines (§1.2).
- **`ENV4` (CC-286 W2(a)), fixed here.** It is the H4 form. The H4 run (`~/c_pvr_h4w_1107/bin/run_sets.sh` l.5) used no
  `env -i`; it exported only `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1` in the coordinator's shell,
  under `nice -n 19`.
  - `env` with these three assignments inherits HOME and PATH, which the watcher needs: ssh reads `~/.ssh/config` and
    the key; `/usr/bin/java` serves VnCoreNLP; `VNCORENLP_DIR` defaults to `~/c_pvr_tools/vncorenlp` (c_pvr.py l.40).
  - It is used unquoted on purpose, so that it splits into words. P20 and P21 run under it.
- `$PRE` (checklist), `$PUSH` (push farm), `$W` (watcher work dir), `$PULL` (pulls) and `$HR` (host repo) are five
  **new** ext4 dirs, each 0700. A failed attempt keeps its dirs; a retry writes `s11_env_2.sh` with `_2` names
  (W25 v1.4 §2 rule).
- On HC-1: `$HOME/c_pvr_repo` (the sparse repo), `O=$HOME/c_pvr_out` (job.sh l.31), `HC=/dev/shm/c_pvr_hc`.

### 1.4 The repository on HC-1 (CC-270 N13): sparse, code only [proposal]
- **Finding.** A full clone or bundle puts every tracked file on the host disk: 2,015 paths, 619 of them under `data/`.
  These include `data/xm3600/oiv7_labels.json` (A12 gold, which CC-270 Q4 / CC-277 Ruling 1(f) keep off the host),
  `data/annotations/*` and other papers' files. Host v3 §4.2 allows only "model weights and code" on disk, and §5 l.224
  says that what is not listed is not covered.
- **The E-G record (v1.2):** LOG OPS-1107c-eg-repo-record (2026-11-07T04:00:04Z). The code reached E-G as
  `git archive --format=tar HEAD` (9b3fd8d) of `scripts/` plus the three prereg json files of the SUMS, piped into
  `tar -C /root/vsps -xf -`. There was no `.git` and no `data/` dir, and the three SUMS were checked OK on the host. So
  no tracked gold reached E-G's disk. HC-1 differs, because job.sh needs `git rev-parse` / `git diff`: hence the sparse
  clone.
- **Route.** A partial, sparse clone on the laptop, then copied to the host. The path set is the union of the two
  SUMS that job.sh checks:
  - `scripts/c_pvr/` and `scripts/c_pvr_gpu/`;
  - the three json files that scripts/c_pvr/SHA256SUMS lists under manuscript/prereg: g_c2_provenance.json,
    ovqa_count_rule.json and ovqa_pin.json.
- **Tested at drafting** (laptop; v1 in `/tmp/s11_hr_1107` at 9b3fd8d; **repeated for v1.1 in `/tmp/s11_hr_1107b` at
  H = 1880951**):
  - 36 blobs, a 714 KB pack and a 1.0 MB `.git`, no `data/` dir. git printed "filtering not recognized by server,
    ignoring" once at the clone, yet the result is filtered (36 blobs, against 2,015 tracked files at HEAD). So the binding check is
    the blob count, which must be 36 at H (the `HR OK` line), not the absence of that warning;
  - `git rev-parse HEAD` = H; `git diff --quiet HEAD --` rc 0 even with the promisor remote unreachable;
  - both SUMS `sha256sum -c` OK;
  - `c_pvr_gpu.py selftest` rc 0 in that tree ("selftest ok … c_pvr_gpu.py 9a9c6eb5… torch=real transformers=real").
  - 1179c4b3 was the v1 run at 9b3fd8d.
  - `git status` tries to fetch a missing blob and fails, so it is **never run on the host**. job.sh uses only
    `rev-parse` and `diff --quiet`.
```sh
. "$HOME/s11_env.sh"
[ ! -e "$HR" ] || { echo "GUARD: $HR exists"; exit 1; }
git clone -q --no-local --filter=blob:none --no-checkout -u 'git -c uploadpack.allowFilter=true upload-pack' "file://$R" "$HR"
P=manuscript/prereg/2026-11-02_c_pvr_tier1
git -C "$HR" sparse-checkout set --no-cone 'scripts/c_pvr/' 'scripts/c_pvr_gpu/' "$P/g_c2_provenance.json" "$P/ovqa_count_rule.json" "$P/ovqa_pin.json"
git -C "$HR" checkout -q "$H"
git -C "$HR" config remote.origin.url /nonexistent                 # the host never fetches
[ "$(git -C "$HR" rev-parse HEAD)" = "$H" ] && git -C "$HR" diff --quiet HEAD -- \
  && (cd "$HR" && sha256sum --quiet -c scripts/c_pvr_gpu/SHA256SUMS && sha256sum --quiet -c scripts/c_pvr/SHA256SUMS) \
  && [ ! -e "$HR/data" ] && echo "HR OK $(git -C "$HR" cat-file --batch-all-objects --batch-check | awk '$2=="blob"' | wc -l) blobs" >> "$PRE/pre.txt"
```
- Transfer: `tar -C "$HR" -cf - . | ssh -o BatchMode=yes hc1 'mkdir -m 700 c_pvr_repo && tar --no-same-owner -C c_pvr_repo -xf -'`.
  `--no-same-owner` matters. Root's tar keeps the laptop uid 1000 otherwise, and git ≥ 2.35.2 (Ubuntu 22.04's patched
  2.34.1 too, CVE-2022-24765) then refuses the repo as "dubious ownership", so job.sh l.50 STOPs. Then the same three
  checks on the host, run as the user that runs job.sh: rev-parse = `H`, diff --quiet, both SUMS.
- **Sufficiency of the path set, checked in code at drafting.** The host code paths read only
  `scripts/c_pvr/prompts/*` from the repo root: `CP.prompts(x.root)` in decode, hostcheck and hostcheck-en; cap reads
  only its arguments. `data/xm3600/vi_oiv7_map.json` and `rescap/` are read only by the laptop decomposers
  (c_pvr.py l.629, l.799). The three json files hold pins and field-name rules only, with no data rows:
  - ovqa_pin.json: keys files / label / revision;
  - ovqa_count_rule.json: per vlsp2023 file, the field names images / qa;
  - g_c2_provenance.json: a provenance record.
  They are needed only because job.sh l.53 checks scripts/c_pvr/SHA256SUMS.
- If the reader rejects the route, the alternative is a code change in job.sh: a pinned tree manifest instead of
  `git rev-parse` / `git diff`. That needs its own diff read. A full clone needs a stated custody departure with a PI
  line (§18 PQ-S11-3).

## 2. Data pins (CC-280 AM8; CC-279 N4)

| item | value | record |
|---|---|---|
| KEPT d_vi / d_tc / d_en | 753cf695 (9,098) / a5f32465 (20,842) / 619839a8 (80,040) | LOG l.1655; c_pvr_gpu KEPT |
| democap d_vi / d_en / d_tc | e02f259a (1,054,946 B) / 56f7fba9 (5,270,650 B) / f3675eaa (1,880,182 B, written at builder 9f944063), all three in `/home/hoanguyen/c_pvr_h4_1107/democap/` (the push source) | CC-277 Ruling 9; CC-279 N4; CC-282 Ruling 1; reproduced bit-exact and re-hashed at H4 (OPS-1107c-h4) |
| QTSV.sha256 | 6962b7e6360983b0a9f702a9155ac6bd74a437058dd00df0bd91555d5e61fa5e (10 lists + shots 20a53fc8) | OPS-1107c-qtsv |
| EMB_PUSH | abe5aac1c512781d3c5b2d53c3ea18ff3620f3a1a26c7614bb522eb68f997fe6 (37,592 files, 9,727,886,983 B) | OPS-1107c-emb-push |
| embeddings (9) | emb_xm3600_vi dc5840fc; emb_ktvic_explore f6250f83; emb_openviic_explore 3bdb7345; emb_vitextvqa_dev 7e1b6649; emb_t_a b44567fc; emb_d_tc 3b2ec4e6; emb_d_vi 37f00db3; D-EN emb_memory def163d3; KT-C emb_coco_test 6e8bdba2 | OPS-1107c-emb (full shas there) |
| host v3 l.211 departure | D-EN embeddings = emb_memory.npz def163d3, not "cen_memory_emb.npz" (cluster vectors; CC-277 Ruling 3; CC-280 Ruling 2(a)). File-name departure, no custody effect: embeddings never go to HC-1 | this file |
| parity anchor | PASS: XM n 3,000 min 0.998717; OV n 1,020 min 0.99956 (PARITY_MIN 0.995 in code) | OPS-1107c-eg-wipe-rekey-parity |
| freezes | main 9a074530 from host.lock 966eb327; EN 8e8a13c3 from d2f0f262; source instance E-G (2026-11-07); pinned in job.sh l.24-25 at H | OPS-1107c-emb; CC-284 Ruling 1; commit 1880951 |
| a12 | 5e19c78a; queries_with_absent 1,290; label_keys_outside_qids 0 | OPS-1106c-a12 |
| KT-C pixels | K = /home/hoanguyen/c_pvr_ktc_1106, 3,907 files, 640,065,284 B, manifest sha f4d8e5e4 (full in LOG) | OPS-1107c-ktc; CC-282 Ruling 13 (used in place, no copy) |
| **TMAN** | **4849a08f1fc384f1901fd294950f9ea20a5622879838c4a5ecac73cec62c3efe**: sealed MANIFEST.sha256, 11,571 lines `<sha256>  <path under /dev/shm/c_pvr_hc>` (manifest 6, democap 3, kept 3, images 11,559); TMAN_BYTES 2,199,372,292 | OPS-1107c-h4 |
| set manifests (H4) | xm3600_vi f81323d1 (3,600 q / 7,923 demos / 2 decomp_fail; a12 5e19c78a, labelled 1,290, true 733); ktvic_explore 74e7988d (286 / 2,422 / 0); openviic_explore 16dd76d5 (1,020 / 5,785 / 2); vitextvqa_dev 1b3f838f (1,676 / 6,804 / 2); t_a 9cd89c5e (1,070 / 8,246 / 0); kt_c 44754b1b (3,907 / 19,600 / 0); pins.json 4872eb30; n_rank 7; numpy 2.5.4, scipy-openblas 0.3.34, threads 1 | OPS-1107c-h4; H4 record 36464741 |
| sizes file | `{"kt_c": 3907, "ktvic_explore": 286, "openviic_explore": 1020, "t_a": 1070, "vitextvqa_dev": 1676, "xm3600_vi": 3600}` + LF, sha256 **1fcbc910e6e4b8d67fcf4235fb54810345dadedd6656d0c965e7ef650130218e** (computed at drafting; sum 11,559) | CC-270 N12 [proposal] |

## 3. Registered [proposal] items, fixed here before any output

| # | item | value | source |
|---|---|---|---|
| R1 | N_RANK and ties | N_RANK = 7 (= A9_POOL = A3_TOP); ties to the smaller id in Python str order ("00000007870.jpg" < "1964"); numpy / BLAS versions recorded in the H4 line; the manifest sha, not a re-run, is the reproducibility anchor | CC-272 2(6); CC-277 Ruling 4 |
| R2 | A5 shot rule | `arm_rng("A5","lmcap_shots").sample(sorted(D-VI), 3)` = '00000007870.jpg', '7292', '1964'; disjoint from every tier-1 query image by sha (checked in `seal`) | CC-272 2(5), N5 |
| R3 | A8 / S2 timing proxy | rate(A8) = max(0, rate(PVR-drop) − rate(A1)); rate(S2) = max(0, rate(S1) − rate(S3)) (A8_PROXY). It over-estimates (the safe side for a never-cut arm). Departure from prereg §10.1 "every VI arm timed", because a direct timing needs the A1 speed captions, which NB-SPEED forbids | CC-270 Q2 |
| R4 | speed sample | the first 200 query ids by sha256(id + "c_pvr_speed") (speed_ids) | CC-270 Q5 |
| R5 | T_A rate proxy | `project()` applies the XM3600-vi rate of each arm to T_A (EN prompt, D-TC) | CC-270 N12 |
| R6 | T_A arm list | A0, A1, A2, A3, A6, A7, A8, A11, PVR-drop, PVR-keep (mBLIP, EN prompt, D-TC). A4 / A5 / A9 / A10 are not on T_A: S9 v2 pins D-VI only (l.43-44), and prereg §5.1 assigns T_A no S9 arm. This is a correction of a [proposal] code list, not a dropped arm | CC-273 Ruling 1, N1(a) |
| R7 | S1 | S1 = PVR-drop (EN_AS), fixed before any output, because §6.3's variant choice needs tier-1 results that do not exist yet | CC-273 2(a), N1(b) |
| R8 | LLaVA env | torch 2.6.0 instead of LLaVA's 2.1.2 (CVE-2025-32434, weights_only guard); mm_projector.bin is not used (the shards hold the projector); the CPU-then-cuda load is equivalent to model_vqa's device_map='auto' (tower fp32, LM fp16) | CC-273 N1(c)-(e) |
| R9 | S9 pass order | departure from S9 v2 §5's registered pass order (one M-CLIP pass, one XGLM pass, then mBLIP): M-CLIP runs per A4 / A9 step and XGLM per A5 step, so a cap stop falls on cuttable arms only (CC-270 B1). Never co-resident; pass seconds are timed; loads are untimed (R11) | CC-272 2(4), N3 |
| R10 | A8_WAIT_SEC | 1800 s (c_pvr_gpu l.101), funded in P1 as fixed_sec. Why 1800: the A1 / S3 sources finish in the first 6 of 72 steps, so the laptop has hours of phase-1 slack, and 30 min is about 2-6 × the pull + decompose + push time for 6 sources [est. 5-15 min]. Over it = JOB STOP, PI; never a cap stop | CC-270 B2; CC-270r2 N-S11b |
| R11 | load seconds | not in P1 (cap fixed_sec = A8_WAIT_SEC only). The 1.25 margin covers them, under the measured check of §9.5 | CC-270 Q3; CC-272 N3 |
| R12 | M1 load rule (mBLIP) | input embedding := the checkpoint's own `language_model.lm_head.weight` from the pinned shards, then tied (1096/1097 index keys); the weights are unchanged | CC-270r2 N-S11e |
| R13 | transformers messages | mBLIP under 4.51.3: the BLIP-2 legacy "Expanding inputs for image tokens" path; model-config max_length 51 / min_length 32, overridden by the pinned max_new_tokens / min_new_tokens; "generation_config default values have been modified … {'bos_token_id': 1}". Effective bos_token_id 1 for every arm, so no contrast changes. S12 records the effective GenerationConfig for both kinds (caption, verify) of mBLIP and LLaVA, and for XGLM | CC-270r2 N-S11d; CC-272 2(10); CC-273 N5 |
| R14 | covered tmpfs material | `MANIFEST.sha256`; `manifest/<set>.json` (6); `democap/<ds>.json` (3); `kept/<KEPT name>` (3); `images/<set>/<file>` (11,559); and mid-run `a1_decomp/<set>.json` (6) + `a1_decomp/MANIFEST.sha256`. No source caption json reaches HC-1 (CC-277 Ruling 11; CC-276 W6 closed in code). KTVIC / OpenViIC train jsons, dataset_coco.json and TextCaps train never leave the laptop | host v3 §5; CC-270r2 N-S11a |
| R15 | a1_decomp departure | the a1_decomp files are produced mid-run, so no run doc can list them. Departure from host v3 §4.2 "against the run-doc manifest": their own `MANIFEST.sha256` (`<sha256>  <basename>`) is logged in one OPS line before the push, the push is atomic (temp, sha check, `mv` on the same tmpfs), MANIFEST last | CC-270r2 N-S11a |
| R16 | watcher poll | EVERY = 60 s (c_pvr_watch l.42) | PRE_S11 §6.3 |
| R17 | heartbeat threshold | the pull loop flags `W/FAULT` at once and a heartbeat older than **HB_MAX = 30 min** (§12). Why not 5 min: the heartbeat is written once per loop, and one source's VnCoreNLP / spaCy decomposition of up to 3,907 captions can outlast 5 min (CC-282 N6). P18 checks 30 min against the H4 decomposition rate | CC-280 R6(b); CC-282 N6 |
| R18 | speed stop | END = speed_start.epoch + 10800 s (job.sh l.80), a constant fixed before the speed test. This amends host v3 H-9 (≤ 1.5 h) by PI-1106l. The first-arm projection is logged, not used as a switch | CC-280 AM4 |
| R19 | test-split XM3600 labels | the 104 XM3600 ∩ NoCaps-test images are ordinary xm3600_vi queries. G-A removed them from tier 3, so their A12 labels are XM3600 dev gold, and only booleans reach HC-1 | CC-280 Ruling 1(f) |

## 4. Preconditions (coordinator, laptop; each one a STOP; output to `$PRE/pre.txt`)
The full set is P0a-P0d, P1-P22. All except P20 must PASS before the rental (§0 row 4); P20 must PASS after the rental
and before push 1.

| # | check | PASS |
|---|---|---|
| P0a | LOG holds OPS-1107c-eg-repo-record (the E-G repo-transfer form; CC-286 N7 / D-R12) | present (since 04:00:04Z) |
| P0b | LOG holds the CC-272 N9 record line (the P2 evidence-root and harness note), written by the coordinator before registration | present |
| P0c | LOG holds a CC-279 N2 status line for P5_W2_DTC_CHECK_PLAN_v1.md (eff19552): committed under CC-278, or "still uncommitted, not a rental gate" | present |
| P0d | LOG holds an NGRAM PASS line for this file at its read sha (CC-286 N6 / D-R13) | present |
| P1 | R-S11 GO and the registration commit of exactly this file; `git ls-files --error-unmatch $DOC` and `sha256sum $DOC` = the read sha (`DOC` names this v1.2 file; W1) | equal |
| P2 | R-P6 commit 1880951 present; `grep -E '^FREEZE_SHA(_EN)?=' scripts/c_pvr_gpu/c_pvr_job.sh` shows 9a074530… and 8e8a13c3… (full; true at H, v1.1 drafting); `sha256sum` of job.sh / c_pvr_gpu.py / gpu SUMS = 9532c085 / 9a9c6eb5 / b8e62ba5 | equal |
| P3 | `git diff --quiet "$H" HEAD -- scripts/c_pvr scripts/c_pvr_gpu scripts/c_en` (no code moved since `H`); `git diff --quiet HEAD -- scripts/c_pvr scripts/c_pvr_gpu`; the three SUMS (c_pvr_gpu, c_pvr, c_en) `sha256sum -c` from the repo root; the §1.1 shas | all OK |
| P4 | `mkdir -m 700 "$PRE"` (absent before) | – |
| P5 | `$HR` built and checked (§1.4) | "HR OK 36 blobs" (36 at H = 1880951, v1.1 test) |
| P6 | sealed set: `sha256sum < $O/MANIFEST.sha256` = TMAN 4849a08f…; `wc -l` = 11,571 (both true at v1.1 drafting) | equal |
| P7 | the H4 lines exist and hold: democap e02f259a / 56f7fba9 reproduced and f3675eaa re-hashed (CC-282 Ruling 1); the 10 list shas + QTSV 6962b7e6 reproduced (Ruling 6); xm3600_vi `inputs.a12` = 5e19c78a, a12_labelled = 1,290, a12_true > 0 (Ruling 12(c)); every kt_c image_sha256 = the H6 manifest's (Ruling 13); the a12 output deleted and logged (A12_RUN_SHEET §6). **All present at v1.1 drafting:** OPS-1107c-h4 (democap = pins; xm3600_vi a12 5e19c78a, labelled 1,290, true 733; kt_c 3,907 / 3,907 = H6 manifest) and OPS-1107c-a12-delete | all present |
| P8 | KT-C in place: `cd "$K" && sha256sum -c "../$(basename "$K").sha256" \| grep -c ': OK$'` = 3907, no FAILED; `sha256sum "$K.sha256"` = KM | equal |
| P9 | push farm built and checked (§7.1): `LAPTOP OK` with TMAN_N files | present |
| P10 | tmpfs need: `NEED = ceil(1.25 × TMAN_BYTES)` = ceil(1.25 × 2,199,372,292) = **2,749,215,365 B** (v1.1); §7.1 re-sums TMAN_BYTES into pre.txt and must give the same value | equal |
| P11 | watcher selftest under ENV4: `cd "$R" && $ENV4 "$CV" -I -B scripts/c_pvr_gpu/c_pvr_watch.py selftest` rc 0, prints 3a4c60f8. It uses a fake decomposer and a fake ssh (c_pvr_watch l.241-243), so the real ones are P21 and P20 | rc 0 |
| P12 | `$W` absent (the watcher makes it 0700 on ext4) | absent |
| P13 | pull loop extracted from this file: `awk '/^#!\/bin\/bash$/,/^done$/' $DOC > "$PRE/s11_pull.sh"` (the only such block); `sha256sum` recorded; `grep -c '/dev/shm' "$PRE/s11_pull.sh"` = 0 (host v3 §4.5) | 0 |
| P14 | the old `gpu_backup.sh` is NOT started for hc1 (it pulls `/root/` with the model cache; §12): `pgrep -fc '[g]pu_backup.sh'` (bracketed, so it cannot count the calling shell; W4) recorded, and `grep -c hc1 ~/.config/vsps/gpu_backup.sh` = 0 | count recorded; 0 |
| P15 | d_watch live (the /mnt/d EIO monitor, W25 P0 form): `pgrep -fc '[d]_watch.sh'` | count ≥ 1 |
| P16 | usage guard (`~/.config/vsps/usage_check.sh`): 5-h and 7-day fields above the stop level, so that the coordinator can serve S12-S14 without a pause | recorded |
| P17 | PI-1106m: laptop on mains power, sleep off, online for about 30 h; Windows Update restart deferred | PI line on the day |
| P18 | HB_MAX check (CC-286 N10, CC-286r2 N-g): wall times from `~/c_pvr_h4w_1107/run.log` stamps, text counts from the demos column of OPS-1107c-h4 (LOG l.1763). Whole `set` steps, so this is an upper bound on the decomposition rate: xm3600_vi 81 s / 7,923 texts (VnCoreNLP), t_a 180 s / 8,246 (spaCy), kt_c 292 s / 19,600 (spaCy), i.e. ≤ 0.022 s per text, so ≤ 1.5 min for 3,907 captions. That is ≤ 15 min, so HB_MAX = 1800 s stands; P21's seconds are recorded beside it. `echo 1800 > "$PRE/hb_max"` before the launch | ≤ 15 min |
| P19 | no other C, A or B job writes heavily to /mnt/d during S15's first 6 h (the watcher reads code and VnCoreNLP from /mnt/d; EIO note) | stated |
| P20 | ssh key login for `hc1` works in BatchMode, both plain and inside the watcher's env: `ssh -o BatchMode=yes hc1 true` and `$ENV4 ssh -o BatchMode=yes hc1 true`. The watcher selftest (P11) uses a fake ssh and cannot catch a missing HOME. No password in any argv | rc 0 both (after rental, before push 1) |
| P21 | **real decomposers under ENV4 (CC-286 W2(b))**: the §4.1 block, from `$R`. PASS = rc 0, no `decomp_fail` key, every props count > 0; the seconds are recorded. FAULT otherwise: no launch until a read | rc 0, "P21 PASS" |
| P22 | **no self-matching process pattern (CC-286 W4)**: the §4.1 one-line check gives 0 | 0 |

### 4.1 P21 and P22 blocks (v1.2)
P21 uses four fixed sentences written here (synthetic, made up for this check, not from any dataset; each shorter
than 6 words, so no 6-gram can match a caption corpus). Every noun is a lexicon class: chó / mèo / ghế / xe đạp are
keys of vi_oiv7_map.json, and dog / cat / chair / bicycle are forms in en_oiv7_map.json. They are decomposed by the
pinned c_pvr.py (a503644a), loaded through c_pvr_gpu.load(), exactly as the watcher's `decomposer` does
(c_pvr_watch l.212-213).
```sh
. "$HOME/s11_env.sh"; cd "$R" || exit 1
$ENV4 nice -n 19 "$CV" -I -B -c '
import sys, time
sys.path.insert(0, "scripts/c_pvr_gpu")
import c_pvr_gpu as G
G.load()
t0 = time.time(); vi = G.CP.decompose_vi(["Mèo xám trên ghế.", "Chó đen cạnh xe đạp."], G.ROOT)
t1 = time.time(); en = G.CP.decompose_en(["Grey cat beside chair.", "Black dog near bicycle."], G.ROOT)
t2 = time.time()
bad = [d.get("decomp_fail", "no props") for d in vi + en if "decomp_fail" in d or not d["props"]]
print("P21", "PASS" if not bad else "FAULT", "vi", [len(d["props"]) for d in vi], round(t1 - t0, 1),
      "en", [len(d["props"]) for d in en], round(t2 - t1, 1), "bad", bad)
sys.exit(1 if bad else 0)' >> "$PRE/pre.txt" 2>&1; echo "P21 rc=$?" >> "$PRE/pre.txt"
echo "P22 $(grep -oE "p(kill|grep)( -[A-Za-z]+)* (-- )?[^ ]+" "$DOC" | grep -vcE "'\[")" >> "$PRE/pre.txt"   # must read "P22 0"
```
- **Tested at v1.2 drafting** (laptop, at H, `~/.venvs/c_pvr`): `P21 PASS vi [2, 2] 2.3 en [2, 2] 3.9 bad []`, rc 0,
  about 7 s in total. (A first draft used longer sentences; NGRAM flagged one 6-gram in COCO, so all four are now ≤ 5
  words.)
- **Negative controls.** With `VNCORENLP_DIR` pointing at a missing dir, the call raised FileNotFoundError (rc 1).
  With java off PATH, it raised `FileNotFoundError: 'java'`. So both break the check closed.
- **Why P21 matters.** decompose_vi turns a per-caption java / VnCoreNLP error into a silent `decomp_fail` row
  (c_pvr.py l.633-647), not a FAULT. A broken env would therefore feed empty propositions into A8 ×5 and S2.
- **P22** finds every process-pattern command in this file (sh blocks, tables and inline code) and counts those
  whose pattern is not bracketed. The answer must be 0. A bracketed pattern (`'[g]pu…'`) cannot match the calling
  shell's own argv, since that argv holds the bracket. Kills use pid files (§10.2), never a pattern.

## 5. Money

### 5.1 L-before (host v3 §3; immediately before renting)
- Read the ckey panel: account balance B0 and every live rental with its remaining capped spend R_j.
  - Under PI-1105a and PI-1107c, A's GPU branch and B queue **after** C, so Σ R_j = 0 is expected. Any live rental
    is named by its LOG line.
- **Solvency:** B0 ≥ 350,000 + 3 × r_offer + Σ R_j, else nothing is rented and the PI is asked (§18 PQ-S11-2).
  - Example: at 759,965 VND (L-after of E-G), with r ≈ 10,800 and Σ R_j = 0, the need is 382,400. It passes.
- **Money figures at v1.1 drafting (LOG up to l.1770).** Last balance read: **759,965 VND** (L-after of E-G,
  OPS-1107c-eg-done, about 2026-11-07T02:23Z). No C, A or B rental has been logged since, so Σ R_j = 0 now. A top-up
  for B (PI-1107b, about 3.3-4.1 M VND, PI funds) is not logged as made. The R-P6 commit and the H4 builds were
  laptop-only, 0 VND.
- **S so far (block ledger).** m9 20,864 + E-G 17,629 = **38,493 VND**.
  - Both are balance differences (LOG l.1675, OPS-1107c-eg-done), not panel per-instance figures as host v3 §3 asks.
  - At L-before the coordinator reads the panel usage history for both instances. If the history is readable, its
    figures replace these; if not, these stand, with the basis stated.
  - E-G's implied rate is 17,629 / 1.63 h ≈ 10.8k VND/h [est.].
- Line `OPS-<MMDD>c-hc1-lbefore`: B0, Σ R_j (named), S so far, solvency PASS.

### 5.2 The offer and the rental line (host v3 §1 as amended)
- Accept only an offer that meets **every** field.
  - **CPU (PI-1107a):** Ryzen 7 5800XT class (8C/16T, Zen 3) or better. This replaces host v3 §1's "5900X or ≥ 12C /
    24T".
  - GPU 1× RTX 3090 / 3090 Ti 24 GB; CUDA ≥ 12.4; RAM ≥ 32 GB; disk 200 GB at ≥ 1000 MB/s; net ≥ 400 Mbps;
    uptime > 99 %.
  - **Max rental time ≥ 72 h.** The block is about 30-33 billed h, plus 1-2 h of margin.
  - OS: Ubuntu 22.04 is accepted with the deadsnakes python3.12 prep (PI-1107a); 24.04 needs no prep.
- If no offer meets every field, nothing is rented. The PI gets the closest offer and a recommendation (§18
  PQ-S11-1). OPS-1107c-eg-offers found 0 of 73 3090 offers on the old spec; the PI-1107a floor is the one that applies now.
- Rental line `OPS-<MMDD>c-hc1-rent` (`date -u`; this stamp is **T0**): offer id (LOG only), every §1 field value, r_host
  as the panel writes it (e.g. 10053.38), B0, Σ R_j, "all GPU_RENTAL_SPEC fields met (PI-1107a CPU floor)".
- r_host enters `cap` as written. It is rounded **up** in code and must lie in 1,000-100,000 (CC-270 N1, N1';
  `r_host_up`).

### 5.3 Cap projection with H_350k (T1-REP v4 §9; c_pvr_gpu `cap_plan`)
- T_down = 1.0 h × r_host.
- **H_M = ⌊(M − S − T_down) / r_host⌋**.
- cap = ⌈1.25 × P1′⌉ after the cuts A10 → A5 → A3 → A2 → A11, then PQ-C2, then the PI.
- S at the P1 line = 38,493 + HC-1 per-instance spent at L-P1, which includes setup, S12, S13, the three pushes and
  idle time.
- **HC-1 time before the P1 line [est.]:**
  - host prep and setup: about 0.5 h. E-G's `setup.log`: main 00:56:06 → 00:57:35Z; the rest (EN venv + every weight)
    02:06:14 → 02:15:06Z. m9 took 1.7 h with one retry. Host v3 §6's "about 4 h" is withdrawn for planning;
  - push 1 + S12: about 0.5 h;
  - push 2: about 0.15 h;
  - S13: 1.5-3.0 h;
  - push 3 + P1: about 0.25 h.
  - Total **about 3.0 h (speed 1.5 h) to 4.5 h (speed 3.0 h)**, with 5.5 h as the worst row (one setup retry).

| r_host (VND/h) | HC-1 h before P1 | S at P1 | H_350k | H_465k |
|---|---|---|---|---|
| 10,054 (m9) | 3.0 | 68,655 | **26** | 38 |
| 10,054 | 4.5 | 83,736 | **25** | 36 |
| 10,054 | 5.5 | 93,790 | **24** | 35 |
| 10,800 (E-G implied) | 3.0 | 70,893 | **24** | 35 |
| 10,800 | 4.5 | 87,093 | **23** | 33 |
| 10,800 | 5.5 | 97,893 | **22** | 32 |

- At P1 = 24-30 h [est., host v3 §6], ⌈1.25 × P1⌉ = 30-38 > H_350k in every row, so **cuts are certain**. They follow
  the registered order. Each VI arm is about 1.6-2.0 h (T1-REP §9 example), so 3-5 cuts are likely. With equal-cost
  arms and H_350k = 24, the PQ-C2 branch opens at P1 above about 26-29 h (v = 0.8-1.0) [illustrative, T1-REP §9 table form].
- **Worst case (money).**
  - The block total stays ≤ M by construction: the money stop is at M − T_down, the cap counts wall time from the P1
    stamp, and the `cap_plan` assert is total ≤ M.
  - C's remaining worst case from now: 350,000 − 38,493 = **311,507 VND**, or 465,000 − 38,493 = **426,507 VND**
    under PQ-C2.
  - Under PQ-C2 the solvency at that moment is balance ≥ (465,000 − S) + 3r + Σ R_j. At B0 ≈ 760k with Σ R_j = 0
    it passes. If B (≤ about 332k worst case, CC-280 AD1) or A's branch (about 114-141k, PI-1107c) were live, it
    fails, and a top-up is needed first (§18 PQ-S11-2).
- **Account balance STOP** (prereg §10.1 l.730 as H-11): the coordinator reads the ckey panel balance by hand at L-P1
  and then about every 6 h [proposal], with one `OPS-<MMDD>c-hc1-balance` line each. A missed or late check is
  logged when noticed and is not a STOP. Below 3 × r_host = STOP (delete-when-idle rule).

## 6. Host prep and setup (after T0; every check is a STOP, as in host v3 §1)

1. `ssh-copy-id`, then ssh key login in BatchMode (P20). The alias `hc1` lives only in `~/.ssh/config`. The password
   sits in a 0600 file outside the repo and is never printed.
2. **Setup checks (host v3 §1 table), output to `$PRE/hc1_facts.txt`**, names and numbers only:
   - `nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader` (1 × 3090 / 3090 Ti, 24 GB) and
     the driver CUDA version ≥ 12.4;
   - `lscpu | grep -E 'Model name|^CPU\(s\)|Thread|Core'` (≥ 5800XT class);
   - clock skew (CC-286 N1): `echo "$(ssh -o BatchMode=yes hc1 date -u +%s) $(date -u +%s)"`, with |host − laptop|
     < 60 s. The watcher compares host marker stamps with T_J1, which is itself taken from the host clock (§10.2);
   - `free -g` total ≥ 32;
   - `df -B1 /dev/shm` avail ≥ NEED (P10);
   - `df -B1 ~` ≥ 200 GB;
   - one timed sequential 4 GB write and read on `~`, then the one file is removed: `dd if=/dev/zero of=~/s11_dd
     bs=1M count=4096 oflag=direct` and `dd if=~/s11_dd of=/dev/null bs=1M iflag=direct`, then `rm ~/s11_dd`;
     ≥ 1000 MB/s each;
   - `. /etc/os-release; echo $VERSION_ID`;
   - `command -v git tmux rsync flock python3.12` (job.sh needs git and flock; the launch needs tmux; §12 and §13 need
     rsync on both ends). Missing tools are installed before anything else: `apt-get install -y git tmux rsync
     util-linux`. This is host prep with no repo code change.
   A fact that contradicts the offer = FAULT. No C file moves; pull hc1_facts; delete; the money counts (host v3 §1).
3. **Python (PI-1107a).** If `python3.12` is absent (Ubuntu 22.04): `apt-get install -y software-properties-common &&
   add-apt-repository -y ppa:deadsnakes/ppa && apt-get install -y python3.12 python3.12-venv`, as on E-G
   (OPS-1107c-eg-rent: 3.12.16). This is host prep with no repo code change. `python3.12 --version` goes into the
   facts file.
4. Repo: the §1.4 transfer, then on the host `cd ~/c_pvr_repo && [ "$(git rev-parse HEAD)" = $H ] && git diff --quiet
   HEAD -- && sha256sum --quiet -c scripts/c_pvr_gpu/SHA256SUMS && sha256sum --quiet -c scripts/c_pvr/SHA256SUMS`.
5. `bash scripts/c_pvr_gpu/setup_host.sh` (stage `all` = main + rest; no SigLIP2 on HC-1), in tmux. It must end with
   `SETUP OK`, and `setup.log` must show:
   - `freeze 9a0745307b3b…c09f` (l.59), `torch 2.6.0+cu124 cuda 12.4`;
   - `EN lock installed: freeze 8e8a13c359b3…afcc` (a different value = STOP here, CC-284 N5: §1.1 EN fallback),
     `EN venv torch 2.6.0+cu124 transformers 4.37.2`;
   - `mblip ok`, `helper ok` for mclip / xglm / xlmr, `en ok` for llava / clip336 / llava_code, `refs/main ok` for xlmr
     and clip336.
   Any `SETUP STOP` = STOP (§1.1 fallback for a freeze difference).
6. `/dev/shm/c_pvr_hc` does not exist before push 1. If setup made it (l.64), `rmdir` it while it is empty, so that
   every push starts from a fresh 0700 dir.
7. Line `OPS-<MMDD>c-hc1-setup`: the facts, python, `H`, both freezes, the setup.log sha.

## 7. Push (once per job mode: selftest, speed, tier1; CC-270 Q6)

### 7.1 The laptop push farm (built once; no second copy of any pixel)
The sealed MANIFEST names paths under `/dev/shm/c_pvr_hc`. Their laptop sources are:
- `manifest/`, `democap/`: `$O`;
- `kept/<exact KEPT name>`: `$DS`;
- `images/<set>/`: `$EP/<set>` for the five non-KT-C sets, and `$K` for kt_c (CC-282 Ruling 13; CC-281 O3).

These are the H4 sources (OPS-1107c-h4, v1.1):
- `$O` = `/home/hoanguyen/c_pvr_h4_1107` for manifest/ and democap/;
- `$EP` = `~/c_pvr_eg_1107/emb_push/images` for the five non-KT-C sets (the H4 record: their 7,652 EMB_PUSH lines OK);
- `$K` = `~/c_pvr_ktc_1106` for kt_c (`sha256sum -c` 3,907 OK; image shas = the H6 manifest, 3,907 / 3,907);
- `kept/` from `c_datastores` by the three exact KEPT names (never listed, never globbed).

The H4 record states, per set, that the image shas in the manifest equal the source and TMAN (n = 3,600, 286, 1,020,
1,676, 1,070, 3,907: all True).
- **Regular files only (CC-284 N1, Ruling 3).** The farm on the laptop is symlinks, but `tar -h` dereferences them. The
  archive then holds the targets' bytes as regular members, with no symlink and no hard-link entry. Each stream counts
  its link members through `tee` (must be 0; §7.2).
- On arrival, `find /dev/shm/c_pvr_hc ! -type d ! -type f` must be empty, so no symlink or other non-regular file is on
  tmpfs. job.sh's own set check (l.62, `! -type d`) would let a listed symlink with matching bytes pass (CC-284 Ruling
  3), so this check is the binding one until the N1 job.sh diff.
```sh
. "$HOME/s11_env.sh"
[ ! -e "$PUSH" ] && mkdir -m 700 "$PUSH" "$PUSH/images" "$PUSH/kept" "$PUSH.parts" || { echo "GUARD: $PUSH"; exit 1; }
cp "$O/MANIFEST.sha256" "$PUSH/MANIFEST.sha256"
[ "$(sha256sum < "$PUSH/MANIFEST.sha256" | cut -c1-64)" = "$TMAN" ] || { echo "STOP: TMAN"; exit 1; }
ln -s "$O/manifest" "$PUSH/manifest"; ln -s "$O/democap" "$PUSH/democap"
for f in d_vi_kept_ids.txt d_tc_kept_ids.txt d_en_kept_ids.txt; do ln -s "$DS/$f" "$PUSH/kept/$f"; done   # exact names only (CC-276 W5)
for s in xm3600_vi ktvic_explore openviic_explore vitextvqa_dev t_a; do ln -s "$EP/$s" "$PUSH/images/$s"; done
ln -s "$K" "$PUSH/images/kt_c"
(cd "$PUSH" && sha256sum --quiet -c MANIFEST.sha256) && echo "LAPTOP OK $(wc -l < "$PUSH/MANIFEST.sha256") files" >> "$PRE/pre.txt"
cut -c67- "$PUSH/MANIFEST.sha256" | awk -v d="$PUSH.parts" '{ print > sprintf("%s/p%02d", d, (NR-1) % 6) }'
cat "$PUSH.parts"/p0? | LC_ALL=C sort | cmp - <(cut -c67- "$PUSH/MANIFEST.sha256" | LC_ALL=C sort) && echo "PARTS OK" >> "$PRE/pre.txt"
echo "TMAN_BYTES $(cd "$PUSH" && cut -c67- MANIFEST.sha256 | xargs -d '\n' stat -L -c %s | awk '{s+=$1} END {print s}')" >> "$PRE/pre.txt"   # NEED = ceil(1.25 x) (P10)
```
- Only the files named in MANIFEST are sent, so no extra file in a source dir can travel.
- The farm itself is never tarred as `.`: an archived `.` entry would overwrite `$HC`'s 0700 mode, and job.sh l.57
  would STOP.

### 7.2 One push (six parallel streams; the E-G lesson)
- E-G measured about 0.6-1.1 MB/s on one stream (a per-connection limit on the ckey relay) and about 5.7 MB/s on 6
  streams (OPS-1107c-eg-push-parallel, PI-1107a line).
- At 6 streams, 2.2 GB takes about 6.5 min [est.]. Each mode re-pushes, because the trap wipes on every exit.
```sh
. "$HOME/s11_env.sh"; T=$(date -u +%FT%TZ)
ssh -o BatchMode=yes hc1 '[ ! -e /dev/shm/c_pvr_hc ] && mkdir -m 700 /dev/shm/c_pvr_hc' || { echo "STOP: stale $T"; exit 1; }
for i in 0 1 2 3 4 5; do
  ( set -o pipefail; tar -h -C "$PUSH" -cf - -T "$PUSH.parts/p0$i" | tee >(tar -tvf - | grep -c '^[lh]' > "$PRE/push_$T.links.p0$i") \
      | ssh -o BatchMode=yes hc1 'tar --no-same-owner -C /dev/shm/c_pvr_hc -xf -'; echo "p0$i rc=$?" >> "$PRE/push_$T.rc" ) &
done; wait
grep -c 'rc=0$' "$PRE/push_$T.rc"                                          # must be 6
sleep 2; cat "$PRE/push_$T".links.p0?                                      # six lines, each 0 (no link member; CC-284 N1)
tar -h -C "$PUSH" -cf - MANIFEST.sha256 | ssh -o BatchMode=yes hc1 'tar --no-same-owner -C /dev/shm/c_pvr_hc -xf -'   # the manifest last
ssh -o BatchMode=yes hc1 'cd /dev/shm/c_pvr_hc && stat -c %a . && sha256sum --quiet -c MANIFEST.sha256 && sha256sum < MANIFEST.sha256 && find . ! -type d | wc -l && find . ! -type d ! -type f | wc -l' > "$PRE/arrival_$T.txt" 2>&1
```
- **PASS:** mode 700; no `sha256sum -c` line; the sha = TMAN (4849a08f…); the file count = 11,572 (TMAN_N + 1); the
  non-regular count = 0 (CC-284 N1: `find $HC -type l` empty); every links file 0.
- **Never stop a stream mid-file** (E-G: the stopped stream p04 tore one file). A slow stream is left to finish.
- **Top-up:** a stream with rc ≠ 0, or names that FAILED or are missing, are re-sent by an exact name list through
  one stream; tar replaces a torn file. The list command (CC-286 N5), on `$PRE/arrival_$T.txt`, whose `sha256sum -c`
  lines read `<name>: FAILED` or `<name>: FAILED open or read`:
  `sed -n 's/: FAILED.*$//p' "$PRE/arrival_$T.txt" | LC_ALL=C sort -u > "$PUSH.parts/top_$T"`. Then
  `tar -h -C "$PUSH" -cf - -T "$PUSH.parts/top_$T" | tee >(tar -tvf - | grep -c '^[lh]' > "$PRE/push_$T.links.top") | ssh -o BatchMode=yes hc1 'tar --no-same-owner -C /dev/shm/c_pvr_hc -xf -'`
  (the links file must read 0, as for the main streams; CC-286r2 N-h),
  and the arrival check runs again. The names are paths under the tmpfs root, which is the same form as `-T` takes.
- A second failure of the same file = STOP and read.
- Line `OPS-<MMDD>c-hc1-push-<mode>`: stamp, streams, seconds, the arrival sha (= TMAN), the count, any top-up names
  (ids only).

## 8. S12 GPU-host selftest (fresh HOSTCHECK at `H`)

### 8.1 Run
```sh
. "$HOME/s11_env.sh"; [ -n "$H" ] && [ -n "$TMAN" ] || exit 1      # CC-286 N2: no empty args
ssh -o BatchMode=yes hc1 "cd ~/c_pvr_repo && tmux new -d -s c_s12 'bash scripts/c_pvr_gpu/c_pvr_job.sh selftest $H $TMAN'"
```
- job.sh runs:
  - preflight l.49-63: HEAD, clean tree, both SUMS, GPU name, tmpfs 0700, TMAN, the arrival check, and the
    CC-277 N1 file-set check;
  - both laptop-mock selftests (l.64-65);
  - `hostcheck --out $O` and `hostcheck-en --out $O` (l.69-70), so HOSTCHECK_OK.json and HOSTCHECK_EN_OK.json are
    written fresh at `H`.
- **E-G snapshot-path mismatch: closed, no code change.** On E-G both probes failed on try 1 with FileNotFoundError
  (OPS-1107c-eg-done). The sheet's direct call used `--out ~/c_pvr_out/probe`, but hostcheck reads
  `<name>_snapshot.path` from `--out`. job.sh passes `--out $O` = `~/c_pvr_out`, which is where setup_host.sh writes
  those files (l.102, l.117, l.137), and decode reads them from `C_PVR_SNAPS=$O` (job.sh l.34).
  - S12 therefore runs **only** through `c_pvr_job.sh selftest`, never as a direct hostcheck.
  - The E-G probe files are INFRA PROBE only (PI-1106f form) and are not a record here.
- The trap wipes `$HC` at exit (logged).
- **No direct probe call (CC-284 N3).** S11 calls hostcheck / hostcheck-en only through job.sh, which exports
  `C_PVR_FREEZE` / `C_PVR_FREEZE_EN` at l.54-55 before the selftests (l.64-65) and before hostcheck (l.69-70). Since
  R-P6, hostcheck_fresh FAULTs when they are unset.
  - If a direct diagnostic call is ever needed after an S12 FAULT, it is labelled INFRA PROBE and never a record. Its
    `--out` is `~/c_pvr_out/probe`, never `$O` (CC-282 Ruling 2). It is preceded by exactly job.sh's export:
    `cd ~/c_pvr_repo && export C_PVR_FREEZE=$(~/venvs/c_pvr_gpu_966eb327/bin/python -m pip freeze | sha256sum | cut -c1-64) C_PVR_FREEZE_EN=$(~/venvs/c_pvr_llava_d2f0f262/bin/python -m pip freeze | sha256sum | cut -c1-64)`.
  - It also needs `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HOME=~/c_pvr_models/hf` and the `*_snapshot.path` files in
    its `--out` dir (the R_EMB sheet b36faf46 row 8 erratum).

### 8.2 Pass criteria (written before the run; the S12 read is pre-queued, one judge, 85; C_NEXT_STEPS S12)
| # | criterion | expected (E-G INFRA PROBE values, for orientation only) | source |
|---|---|---|---|
| C1 | job.log `HOSTCHECK OK`, rc 0; deletions log last line files = expect = TMAN_N + 1 | – | job.sh l.71; host v3 §4.4 |
| C2 | HOSTCHECK_OK.json c_pvr_gpu_sha256 / c_pvr_sha256 = the `H` shas; freeze_sha256 = FREEZE_SHA (and HOSTCHECK_EN_OK.json the same c_pvr_gpu sha) | **9a9c6eb5**…a260 / a503644a / 9a074530 (the E-G probe recorded 1179c4b3, the pre-R-P6 code: not valid at H) | hostcheck_fresh; CC-282 N2; CC-284 N4 |
| C3 | mBLIP echo caption and verify finish eos, chars > 0, strip_branch true; effective genconfig recorded for caption AND verify: bos 1, eos 2, max_new 64 / 8, do_sample false, num_beams 1 | caption 63 chars, verify 2; pad 3 | CC-270r2 N-S11d; CC-273 N5 |
| C4 | M1 tie (R12) passes: no "meta tensor" error; vram_peak recorded | 16,453,375,488 B | CC-270r2 Ruling 4 |
| C5 | helpers: mclip pins ok, context_length 77, trunc 1 on the 600-token text, cos finite; xglm chars > 0, eos, no LMCap-head echo; xlmr resolves BY NAME (refs/main) | trunc 1; xglm 5 chars | CC-272 N1, N7, N8 |
| C6 | kept d_vi 9,098, d_tc 20,842, d_en 80,040 | – | KEPT |
| C7 | HOSTCHECK_EN_OK.json: freeze = FREEZE_SHA_EN (a difference = CC-284 N5 fallback, §1.1); LLaVA echo caption and verify finish eos, chars > 0; effective genconfig for both kinds: bos 1, eos 2, **pad 0**, max_new 64 / 8 | 8e8a13c3; caption 48, verify 3 | CC-273 N4, N5; CC-284 N5 |
| C8 | setup.log (§6.5): EN venv from d2f0f262 with `--require-hashes --no-deps`; the EN import line; the 12-file GitHub fetch and blob check (`en ok llava_code`); refs/main for clip336 and xlmr; the real LLaVA config (model_type "llava") loads without error (hostcheck-en rc 0) | – | CC-273 N4 |
| C9 | open_clip 2.32.0 attributes `.tokenizer` / `.context_length` and the real M-CLIP / XGLM loader paths ran (C5) | – | CC-272 N8; CC-270 N6 |
| C10 | weights_only guard installed before the transformers import (no FAULT line) | – | CC-270 check 9 |
- Any failure = STOP: a code diff read before the speed test (PINS-A §12 condition (b)).
- The judge's read follows the pull of `~/c_pvr_out/{HOSTCHECK_OK.json,HOSTCHECK_EN_OK.json,logs/}` to
  `$PULL/s12/`, with no gap.
- Line `OPS-<MMDD>c-hc1-s12`: both json shas, C1-C10 results, the read's CC id.

## 9. S13 speed test, S14 P1 line and the cut rule

### 9.1 Run (after the S12 GO and push 2)
```sh
. "$HOME/s11_env.sh"; [ -n "$H" ] && [ -n "$TMAN" ] || exit 1
ssh -o BatchMode=yes hc1 "cd ~/c_pvr_repo && tmux new -d -s c_s13 'bash scripts/c_pvr_gpu/c_pvr_job.sh speed $H $TMAN'"
```
- 18 steps (`steps --mode speed`): 14 VI arms × 200 xm3600_vi + S1, S3, S4, S5 × 200 kt_c. A8 / S2 are untimed (R3).
- Timing rows only: `timing.jsonl` and ids-only logs. No caption file is opened, and no output is ever read
  (NB-SPEED).
- **Stop (R18):** `speed_start.epoch` is written once per host, at the first speed run, and is never removed. END =
  epoch + 10,800 s for every later speed invocation on that host (CC-270r2 N-S11c).
  - A new rental starts a new 3.0 h only under a PI line.
  - Over END = `JOB STOP speed test over 3.0 h` (l.92, l.104). That is STOP and PI, never a cut of N = 200.
- A rerun after a STOP continues to the same END. Finished steps are skipped by their `.done` markers.

### 9.2 The first-arm projection (logged, not a switch; CC-280 AM4)
After the first VI step finishes, the coordinator logs the projected speed total = Σ over the 18 steps of (that arm's
200-image seconds, taking each unmeasured step as equal to it) [est.]. This value is information only.

### 9.3 Incomplete speed = FAULT (CC-270 N3)
`project()` FAULTs "speed test incomplete … STOP, PI" when any arm lacks a rate. Then no cap is computed, and the PI is
asked.

### 9.4 Push 3, then L-P1 (host v3 §3)
- Push 3 (§7.2) first, so that the P1 wall clock does not pay for it.
- Then L-P1: HC-1's per-instance spent from the panel (or r_host × billed h since T0), the account balance, the PQ-C2
  solvency check (balance ≥ (465,000 − S) + 3r + Σ R_j).
- S = 38,493 + HC-1 spent.

### 9.5 Load-second check (R11; CC-270 Q3), right after `cap` and before the launch
- P1 exists only inside `cap`, which runs once, so this check reads CAP.json. The cap clock is already running from
  `p1_epoch` while it runs, so it is mechanical and takes minutes.
- Pull `logs/job.log`, `timing.jsonl`, `sizes.json` and `CAP.json` from `~/c_pvr_out/` to `$PULL/s13/` (CC-286r2
  N-b; the U command below reads all three of the last). Per speed step: load_i = (OK stamp − START stamp) −
  timing sec. Then LOAD_EST = 72 × max_i load_i + 2 × the push seconds of §7.2 (two possible restarts).
- MARGIN = cap_h × 3600 − p1_cut_sec − fixed_sec, from CAP.json.
- **PASS if LOAD_EST ≤ MARGIN**: the 1.25 margin covers the loads.
- **FAIL (CC-286 W3).** The shortfall is SHORT = LOAD_EST − MARGIN. It falls on the last steps first, so it stays
  inside phase 3 only while phase 3 has enough projected seconds left to absorb it. Those seconds are U = the projected
  decode seconds of the **uncut** phase-3 arms (CAP.json `arms` ∩ CUT_ORDER), computed on the laptop from the pulled
  files with the registered `project()`:
  `. "$HOME/s11_env.sh"; cd "$R" && "$CV" -I -B -c 'import sys,json; sys.path.insert(0,"scripts/c_pvr_gpu"); import c_pvr_gpu as G; G.load(); t=[json.loads(l) for l in open(sys.argv[1])]; z=json.load(open(sys.argv[2])); c=json.load(open(sys.argv[3])); p=G.project(t,z); print(sum(p[a] for a in c["arms"] if a in G.CUT_ORDER))' "$PULL/s13/timing.jsonl" "$PULL/s13/sizes.json" "$PULL/s13/CAP.json"`
  (sizes.json and CAP.json are pulled with the timing file). U is an integer number of seconds (`project()` rounds
  each arm up with `math.ceil`). SHORT = LOAD_EST − MARGIN is integer seconds too: load_i from whole-second stamps,
  MARGIN from integer CAP.json fields (CC-286r2 N-c).
  - **SHORT < U:** launch, with no read [proposal]. Only phase-3 tail steps are at risk, A10 first (CC-270 B1). The
    P1 line states LOAD_EST, MARGIN, SHORT, U and "phase-3 tail at risk".
  - **SHORT ≥ U** (few or no phase-3 arms left uncut; with all five cut, U = 0; SHORT = U included): **no launch.** The shortfall could
    reach phase 2 (A8 ×5, S2) or late phase 1, which are the never-cut arms (T1-REP §9; PHASES c_pvr_gpu l.773). STOP,
    `decision PI` in an OPS line, and the PI is asked. The delete-when-idle rule (about 1 h) applies while waiting.

### 9.6 S14: `cap`, the cut rule, the P1 line (mechanical; no judge round; T1-REP §9; §9.5 follows it)
```sh
printf '{"kt_c": 3907, "ktvic_explore": 286, "openviic_explore": 1020, "t_a": 1070, "vitextvqa_dev": 1676, "xm3600_vi": 3600}\n' \
  | ssh -o BatchMode=yes hc1 '[ ! -e c_pvr_out/sizes.json ] && cat > c_pvr_out/sizes.json && sha256sum c_pvr_out/sizes.json'
# must print 1fcbc910e6e4b8d67fcf4235fb54810345dadedd6656d0c965e7ef650130218e
ssh -o BatchMode=yes hc1 "cd ~/c_pvr_repo && ~/venvs/c_pvr_gpu_966eb327/bin/python -I -B scripts/c_pvr_gpu/c_pvr_gpu.py cap --timing ~/c_pvr_out/timing.jsonl --sizes ~/c_pvr_out/sizes.json --s-vnd <S> --r-host <rental-line rate as written> --p1-epoch \$(date +%s) --pqc2-solvent <yes|no> --out ~/c_pvr_out/CAP.json"
```
- **The cut rule** (`cap_plan`):
  1. if ⌈1.25 × P1⌉ ≤ H_350k, cap = that;
  2. else cut A10 → A5 → A3 → A2 → A11, one at a time, re-checking before each cut;
  3. else, with `--pqc2-solvent yes`, M = 465,000 and the cuts are kept;
  4. else `decision: PI` (rc 3). A4 / A9 / A8 / S2 and every phase-1 arm are never cut.
- `cap` refuses if CAP.json exists: it is applied once, and a machine-loss resume goes to the PI.
- `decision PI` → no decode. The PI is asked at once. If the wait exceeds about 1 h (HC-1 setup time, measured in
  §6), back up, wipe and delete (PI-1031c).
- **P1 LOG line `OPS-<MMDD>c-hc1-p1`** (`date -u`): the CAP.json sha and its fields (decision, m, cap_h, h_m, cuts,
  arms, p1_sec, p1_cut_sec, fixed_sec 1800, block_max_vnd, r_host_line, r_host, s_vnd, t_down_vnd); the sizes sha;
  the timing.jsonl sha; LOAD_EST, MARGIN and the §9.5 result; L-P1; "T1-REP v4 §9 (4124ef3) applied". Cut arms are
  **reported cut, never run**.

## 10. S15 tier-1 job (phased; watcher; A8 wait bound)

### 10.1 Order (CC-270r2 Ruling 1; c_pvr_gpu PHASES)
- **Phase 1, never cut:** A1 and S3 first on every set, then PVR-drop, PVR-keep, A12 (xm3600_vi), A0, A6, A7, A4,
  A9, S1, S4, S5.
- **Phase 2:** A8 × 5, then S2.
- **Phase 3:** the uncut arms of A11 → A2 → A3 → A5 → A10, with A10 last.
- A cap stop falls on phase 3 only if §9.5 passes or its FAIL branch launches (SHORT < U, CC-286 W3). The M-CLIP
  pass checks the cap inside its loop (CC-272 N6, closed by CC-273).

### 10.2 Launch: one shell call (job, watcher, pull loop)
```sh
. "$HOME/s11_env.sh"
[ -n "$H" ] && [ -n "$TMAN" ] && [ ! -e "$PRE/watch.pid" ] && [ ! -e "$PRE/pull.pid" ] || exit 1
T_J1=$(ssh -o BatchMode=yes hc1 date -u +%FT%TZ) && [ -n "$T_J1" ] || exit 1   # host clock (CC-286 N1): markers carry host stamps
echo "T_J1=$T_J1" >> "$PRE/pre.txt"
ssh -o BatchMode=yes hc1 "cd ~/c_pvr_repo && tmux new -d -s c_t1 'bash scripts/c_pvr_gpu/c_pvr_job.sh tier1 $H $TMAN'" || exit 1
cd "$R" || exit 1
# W4: each process writes its own pid, then execs, so the pid survives setsid's possible fork (tested at v1.2 drafting)
setsid nohup bash -c 'echo $$ > "$1"; exec "${@:2}"' _ "$PRE/watch.pid" $ENV4 "$CV" -I -B scripts/c_pvr_gpu/c_pvr_watch.py \
  run --ssh hc1 --work "$W" --build "$O" --tman "$TMAN" --start "$T_J1" --log "$R/$L" > /dev/null 2>&1 < /dev/null &
setsid nohup bash -c 'echo $$ > "$1"; sleep 120; exec bash "$2"' _ "$PRE/pull.pid" "$PRE/s11_pull.sh" > /dev/null 2>&1 < /dev/null &   # §12; after the first heartbeat
sleep 2; for f in watch pull; do tr '\0' ' ' < "/proc/$(cat "$PRE/$f.pid")/cmdline" >> "$PRE/pre.txt"; echo >> "$PRE/pre.txt"; done
echo "launched $T_J1" >> "$PRE/pre.txt"
```
- Line `OPS-<MMDD>c-hc1-t1-launch`: T_J1, `H`, TMAN, the watcher sha 3a4c60f8, the pull-loop sha, HB_MAX.
- `--start` uses the `date -u +%FT%TZ` form, the same as job.sh `ts()` (the watcher compares strings; CC-282 N6). It is
  read from the **host** clock, so a laptop / host skew cannot make a fresh marker look stale (CC-286 N1; the §6.2
  skew check is the second guard).
- **Stopping a laptop process (W4).** A process is stopped only through its pid file, after checking that the pid's
  cmdline names it. Never by a pattern, because a pattern also matches the calling shell. The helper is defined in
  the env file (§1.3), so every shell that sources it has it; RS-1 and §13.2 use it:
  `kp() { p=$(cat "$1") && tr '\0' ' ' < "/proc/$p/cmdline" | grep -qF -- "$2" && kill -TERM "$p"; }`
  - `kp "$PRE/watch.pid" c_pvr_watch.py` stops the watcher. `kpg "$PRE/pull.pid" s11_pull.sh` stops the pull loop's
    whole process group, including a running rsync or sleep child (CC-286r2 N-i). This works because the loop's bash
    is a setsid session leader; kpg checks that pgid = pid before it signals. Tested at v1.3 drafting on a dummy group
    of a bash leader and two sleeps: a wrong name gave rc 1 with nothing killed; the right name gave rc 0 with 0
    processes left.
  - Tested at v1.2 drafting on a dummy `sleep` started the same way: with a wrong name, nothing was killed (rc 1, still
    alive); with the right name, it was stopped (rc 0). In the drafting shell, a plain `$!` named a setsid parent that
    had already exited: setsid forks when its caller is a process-group leader. CC-286r2 did not see this in `bash -ic`
    with no tty. The self-written pid is right either way (CC-286r2 N-e).
  - If the cmdline check fails (the pid is gone or reused), nothing is killed. The coordinator lists candidates with
    the bracketed `pgrep -af '[c]_pvr_watch.py'` (listing only) and records them.
- **`$ENV4`** is the H4 form fixed in §1.3 (no `env -i`; it inherits HOME and PATH). It is unquoted on purpose, so
  that it splits into words. The watcher uses the builder's decomposers, and P21 checks them under it (CC-286r2 W5).

### 10.3 The watcher (H5; c_pvr_watch.py 3a4c60f8; CC-280 Ruling 6; CC-282 Ruling 10)
- A laptop process with no agent after launch.
- Every 60 s it polls `c_pvr_out/logs/tier1.<set>.A1.done` (5 VI sets) and `tier1.kt_c.S3.done`. It refuses a marker
  older than `--start`, pulls the jsonl, checks its host sha, drops a torn last line by id, checks the ids against the
  sealed manifest, decomposes by the datastore rule, and writes `W/a1_decomp/<set>.json` atomically.
- When all 6 exist it writes `W/a1_decomp/MANIFEST.sha256`, then the OPS line `OPS-<MMDD>c-a1decomp` (fsynced
  `W/ops_side.log` first, then LOG.md in one O_APPEND write), then the push (`.tmp`, sha check, `mv`, MANIFEST last),
  then `W/PUSHED`.
- **After the push (CC-282 N5):** the coordinator checks that LOG.md holds the a1decomp line once per push attempt,
  with the MANIFEST sha of `W/ops_side.log`.
  - If LOG.md lacks it (an EIO on /mnt/d), the coordinator copies the side-file line into LOG.md with the note "copied
    from ops_side.log (CC-280 R6(a))".
  - A second attempt (§11 RS-8) gives a second line with the same sha. That is expected; the reason is noted.
- **Decomposition record and threshold (CC-286 W2(c), AD1-a), fixed before any data.**
  - Within 30 min of `W/PUSHED`, the coordinator copies the six per-set lines `<set>.<arm>: N decomposed, M
    decomp_fail` from `W/watch.log` into one OPS line `OPS-<MMDD>c-a1decomp-counts`. The pull loop also flags each
    such line at once (§12).
  - **Threshold: M > 50 % of N on any set** (or any later sign that P21's env broke). That is a **systematic
    failure**, a data-class event: one OPS line, then a one-judge read while phase 1 runs. A8 / S2 start only after
    phase 1, which is about 60 steps later, so the read has hours. It may order a JOB STOP before phase 2. If A8 / S2
    still ran on that set, S16 labels that set's A8 / S2 **DEGRADED**.
  - **Basis.** The failure this guards against is a broken env or java, where nearly every caption becomes
    decomp_fail and A8 corrects on empty propositions. P21 checks that env before the launch. Ordinary noise on model
    output is unmeasured (NB-SPEED forbids reading the speed captions) and must not trigger a read or a label. H4's
    rate on human demo captions was 0-2 per set (OPS-1107c-h4), far below 50 %.
  - **Below the threshold** the counts are recorded only (S16 reports them beside A8 / S2), with no read and no label.
- **A8 / S2 wait:** each A8 / S2 step waits at most A8_WAIT_SEC = 1800 s for `a1_decomp/MANIFEST.sha256` (R10). Over
  it = FAULT, JOB STOP (PI), not a cap stop.

### 10.4 Carried watcher hardening (CC-282 N6; not blocking)
The `--start` format regex and a heartbeat inside `pull()` are carried to the next watcher diff. Until then:
- the launch writes `--start` from `date -u +%FT%TZ` only;
- HB_MAX (R17, P18) replaces the 5-min flag.

## 11. Stops and the resume rule (CC-282 Ruling 8 / N4, HARD-DUE here; CC-270 N11)

### 11.1 Stop classes
| class | example | rule |
|---|---|---|
| cap or money stop | `CAP STOP` (CAP_STOP.json) | final, never resumed; go to §13 |
| JOB STOP on HC-1 | a step rc ≠ 0; the A8 wait FAULT; a preflight failure | STOP. Within 15 min an OPS line `OPS-<MMDD>c-hc1-stop` with the STOP line verbatim (ids at most one) and the class. The PI is told with a recommendation. A restart needs a one-judge cause read (REVERSIBLE 85) [proposal], at most 2 restarts (prereg l.730 "two failed restarts"). If the expected wait exceeds about 1 h, do a pull, wipe and delete (PI-1031c); the resume then becomes a re-rental (machine-loss row) |
| watcher-only FAULT, job running | `W/FAULT` while phase 1 runs (ssh drop, /mnt/d EIO, laptop network) | the job keeps running. Transport-class FAULT (`remote command rc`, TimeoutExpired, OSError): one watcher relaunch without a read, by RS-8 alone (the job is not touched) [proposal]. Data-class FAULT (sha differs, ids differ, stale marker, MANIFEST differs from --tman): no restart; one-judge read while the job runs, since the A8 wait is the only clock |
| machine loss / host reboot | ssh dead; `/dev/shm` empty after a reboot | prereg / host v3 H-4: one re-rental, same block ledger and M, under a PI line (§18 PQ-S11-4). Not a same-host resume |

### 11.2 Same-host resume procedure (RS-1 … RS-8)
| # | step | check |
|---|---|---|
| RS-1 | **Freeze the watcher** if `W/PUSHED` is absent, by the §11.3 RS-1 block. `flock -n "$W/.lock" true` rc ≠ 0 means it is alive. Then `kp "$PRE/watch.pid" c_pvr_watch.py` (pid file, §10.2; never a pattern: W4), and wait at most 60 s for `flock -n` to succeed. **If kp returns ≠ 0** (the pid is dead or not the watcher), or the lock is still held after 60 s: one OPS line `OPS-<MMDD>c-hc1-watcher-unfrozen`, a bracketed listing of live watchers (`pgrep -af '[c]_pvr_watch.py run'`, listing only), and a STOP for the PI. Never an unbounded wait, and never a kill by pattern (CC-286r2 W7). Reason: a live watcher could push into a wiped `$HC` (`mkdir -p` gives the parent mode 755, so job.sh l.57 STOPs) or race the re-push | flock free |
| RS-2 | **Host state.** `/dev/shm/c_pvr_hc` must be absent and the last line of `c_pvr_hc_deletions.log` must show files = expect (the trap ran). If the dir is present (no trap: kill -9), run by hand, and log it (CC-286 N4): `ssh -o BatchMode=yes hc1 'cd ~/c_pvr_repo && ~/venvs/c_pvr_gpu_966eb327/bin/python -I -B scripts/c_pvr_gpu/c_pvr_gpu.py wipe --dir /dev/shm/c_pvr_hc --log ~/c_pvr_out/c_pvr_hc_deletions.log'` | absent; count equal |
| RS-3 | **Torn trailing line (CC-270 N11): decode does not handle it.** decode builds `done` from `json.loads` of every output line (c_pvr_gpu l.681), and A7 / A8 read PVR-drop / A1 jsonl the same way, so a torn line FAULTs the resume. For each `c_pvr_out/out/*.jsonl` whose last byte is not `\n`, the coordinator runs one fixed command: `python3.12 -I -c 'import sys,time;p=sys.argv[1];b=open(p,"rb").read();i=b.rfind(b"\n")+1;open(p+".torn."+time.strftime("%Y%m%dT%H%M%SZ",time.gmtime()),"xb").write(b[i:]);open(p,"r+b").truncate(i)' <file>`. That keeps the dropped bytes in `<file>.torn.<UTC stamp>`, opened exclusive (`xb`), so a second torn event never overwrites the first (CC-286 N3). No rm. The dropped id goes into the OPS line (watcher regex form). More than one torn file, or a torn line in a `logs/*.ids.jsonl` only, is recorded and needs no action | every out file ends in `\n` |
| RS-4 | **Cause read** GO (one judge, REVERSIBLE 85), and restart count ≤ 2 | GO |
| RS-5 | **Re-push the arrival set** (§7.2, a fresh 0700 dir) | arrival = TMAN, TMAN_N + 1 |
| RS-6 | **a1_decomp re-push, if and only if `W/PUSHED` exists** (the watcher finished). `W/a1_decomp/MANIFEST.sha256`'s sha must equal the one in `W/ops_side.log`'s a1decomp line. **No re-decomposition.** Every command here runs after `. "$HOME/s11_env.sh"` in the same shell (CC-286r2 N-a). (a) `. "$HOME/s11_env.sh"; cd "$W/a1_decomp" && sha256sum -c MANIFEST.sha256` (6 OK). (b) One OPS line `OPS-<MMDD>c-a1decomp-repush`: the same MANIFEST sha, citing the first line's stamp, "re-push after the teardown wipe (CC-282 Ruling 8)", written BEFORE the push (N-S11a). (c) `ssh hc1 'mkdir -m 700 /dev/shm/c_pvr_hc/a1_decomp'`; for each of the 6 files and then MANIFEST.sha256 last: `ssh hc1 "cat > /dev/shm/c_pvr_hc/a1_decomp/$f.tmp" < "$W/a1_decomp/$f"`, a host `sha256sum` equal to the laptop's, then `mv -f` on the same tmpfs. This is the watcher's own push protocol (c_pvr_watch l.145-151). It runs BEFORE the job restart, so the preflight file-set check (job.sh l.60-63) includes a1_decomp | 7 files, MANIFEST last |
| RS-7 | **Restart the job** with the same `H` and TMAN: `. "$HOME/s11_env.sh"; [ -n "$H" ] && [ -n "$TMAN" ] && ssh -o BatchMode=yes hc1 "cd ~/c_pvr_repo && tmux new -d -s c_t1r<n> 'bash scripts/c_pvr_gpu/c_pvr_job.sh tier1 $H $TMAN'"` (CC-286 N2). CAP.json, the `.done` markers and the partial outputs persist on disk; finished steps are skipped (l.89) and finished ids are skipped (decode `done`). The wall-clock cap keeps running from the P1 stamp, so idle time is paid from the cap | job.log `START` |
| RS-8 | **Relaunch the watcher, if and only if `W/PUSHED` is absent.** This includes a watcher that died mid-push: it re-pushes and writes a second OPS line with the same sha (§10.3). Before the relaunch, `mv "$W/FAULT" "$W/FAULT.<n>"` if it exists (else the pull loop alerts every cycle), and move each stale `W/a1_decomp/*.tmp` aside with one `mv` to `<name>.stale.<n>`, logged (`put()` FAULTs on a stale temp). Then run the §11.3 RS-8 block, which relaunches the **watcher only, never the job**. It keeps the same `--work $W`, `--build` and `--tman`, uses **`--start` = T_J1** (the first tier1 start, read back from `$PRE/pre.txt`) and never the restart stamp, and writes a fresh self-pid file, so a later RS-1 stops the live instance (CC-286r2 W7). Sources already decomposed are skipped by the code (l.192) | heartbeat fresh; the new cmdline is in pre.txt |

### 11.3 RS-1 and RS-8 blocks (v1.3; CC-286r2 W7)
RS-1 (freeze; bounded; never a pattern kill):
```sh
. "$HOME/s11_env.sh"
if [ ! -e "$W/PUSHED" ] && ! flock -n "$W/.lock" true; then
  kp "$PRE/watch.pid" c_pvr_watch.py; k=$?
  i=0; while [ $k = 0 ] && [ $i -lt 60 ] && ! flock -n "$W/.lock" true; do sleep 1; i=$((i + 1)); done
  if [ $k != 0 ] || ! flock -n "$W/.lock" true; then
    echo "$(date -u +%FT%TZ) RS-1 FAIL kp rc=$k; live watchers:" >> "$PRE/pre.txt"
    pgrep -af '[c]_pvr_watch.py run' >> "$PRE/pre.txt"          # listing only, bracketed (W4)
    echo "STOP: OPS-<MMDD>c-hc1-watcher-unfrozen, then the PI"; exit 1
  fi
fi
echo "$(date -u +%FT%TZ) RS-1 OK (watcher absent or stopped)" >> "$PRE/pre.txt"
```
RS-8 (relaunch the watcher only; RS-1 and the RS-8 FAULT / stale-temp moves come first):
```sh
. "$HOME/s11_env.sh"; cd "$R" || exit 1
[ ! -e "$W/PUSHED" ] && flock -n "$W/.lock" true || { echo "STOP: PUSHED exists or a watcher holds the lock"; exit 1; }
T_J1=$(sed -n 's/^T_J1=//p' "$PRE/pre.txt" | head -n 1); [ -n "$T_J1" ] && [ -n "$TMAN" ] || exit 1
[ -e "$PRE/watch.pid" ] && mv "$PRE/watch.pid" "$PRE/watch.pid.$(date -u +%Y%m%dT%H%M%SZ)"
setsid nohup bash -c 'echo $$ > "$1"; exec "${@:2}"' _ "$PRE/watch.pid" $ENV4 "$CV" -I -B scripts/c_pvr_gpu/c_pvr_watch.py \
  run --ssh hc1 --work "$W" --build "$O" --tman "$TMAN" --start "$T_J1" --log "$R/$L" > /dev/null 2>&1 < /dev/null &
sleep 2; { echo "$(date -u +%FT%TZ) RS-8 relaunch T_J1=$T_J1"; tr '\0' ' ' < "/proc/$(cat "$PRE/watch.pid")/cmdline"; echo; } >> "$PRE/pre.txt"
```
- One OPS line `OPS-<MMDD>c-hc1-watcher-relaunch` records the stamp, T_J1, the moved pid-file name and the cmdline.

- **Correction of CC-282 Ruling 8 (for the reader).** Ruling 8 says that the watcher's `--start` is "the restarted job's
  start stamp if any source is still undecomposed". That FAILS in code.
  - The `.done` markers of the first run stay on disk, and job.sh never rewrites them (l.89).
  - The watcher refuses a marker older than `--start` (l.95). So a source whose A1 finished in run 1, but was not
    decomposed, would FAULT as "stale".
  - `--start` = T_J1 keeps the stale-marker guard against anything older than the first tier1 launch. That covers
    every marker, because only tier1 mode writes `tier1.*` markers.
  - The R-S11 reader rules this (§17 D-R7).
- **Speed-mode resume:** RS-2, RS-4, RS-5 and the same `speed` command; `speed_start.epoch` keeps END (§9.1).

## 12. Backups every 30 min (laptop; no /dev/shm; heartbeat reader)
- **Why not `~/.config/vsps/gpu_backup.sh`.** It rsyncs `/root/` minus a list of excludes. `c_pvr_models/` (HF_HOME,
  about 30 GB of weights) is not excluded, and `--max-size=3G` lets most shards through. Over the ~1 MB/s relay that
  would starve the output pulls, and it would write many GB to /mnt/d (EIO note). It also has no heartbeat check. It is
  not used for hc1 (P14).
- **The HC-1 pull loop** (`$PRE/s11_pull.sh`, extracted from this block, sha in the launch line; P13 greps it for
  `/dev/shm` = 0):
```sh
#!/bin/bash
# S11 HC-1 pull loop: c_pvr_out only, every 30 min, then the watcher heartbeat check. No tmpfs path.
. "$HOME/s11_env.sh"; HB_MAX=$(cat "$PRE/hb_max" 2>/dev/null || echo 1800); A="$PRE/alerts.txt"
mkdir -p "$PULL/loop"
while true; do
  t0=$(date +%s)
  rsync -a --partial --timeout=600 -e 'ssh -o BatchMode=yes -o ConnectTimeout=30' \
    hc1:c_pvr_out/ "$PULL/loop/c_pvr_out/" 2>> "$PULL/loop/rsync.err"; rc=$?
  echo "$(date -u +%FT%TZ) pull rc=$rc $(du -sb "$PULL/loop" | cut -f1)" >> "$PULL/loop/pull.log"
  if [ ! -e "$W/PUSHED" ]; then
    [ -e "$W/FAULT" ] && echo "$(date -u +%FT%TZ) WATCHER FAULT: $(cat "$W/FAULT")" >> "$A"
    age=$(( $(date +%s) - $(stat -c %Y "$W/heartbeat" 2>/dev/null || echo 0) ))
    [ "$age" -gt "$HB_MAX" ] && echo "$(date -u +%FT%TZ) HEARTBEAT AGE $age s > $HB_MAX" >> "$A"
  fi
  awk '{ for (i = 2; i < NF; i++) if ($i == "decomposed," && 2 * $(i+1) > $(i-1)) print }' "$W/watch.log" 2>/dev/null \
    | while IFS= read -r x; do grep -qxF -- "$x" "$PRE/decomp_flagged" 2>/dev/null && continue   # once per line (N-f)
        echo "$x" >> "$PRE/decomp_flagged"; echo "$(date -u +%FT%TZ) DECOMP_FAIL > 50 %: $x" >> "$A"; done   # §10.3 (CC-286 W2(c))
  grep -q 'JOB STOP\|CAP STOP\|JOB DONE' "$PULL/loop/c_pvr_out/logs/job.log" 2>/dev/null \
    && echo "$(date -u +%FT%TZ) $(grep 'JOB STOP\|CAP STOP\|JOB DONE' "$PULL/loop/c_pvr_out/logs/job.log" | tail -n 1)" >> "$A"
  s=$(( 1800 - ($(date +%s) - t0) )); [ $s -gt 0 ] && sleep $s
done
```
- The pull goes to laptop **ext4** (`$PULL/loop`), never /mnt/d during the run. Copies go to
  `.session_backup/machines/HC1/root/c_pvr_out/` once, at §13.
- The coordinator (or the dashboard tracker) reads `$PRE/alerts.txt` at each check-in. A new alert line is acted on
  per §11.
- What it pulls: outputs (model captions of the query images, ids, masks), ids-only logs, timing, CAP.json and the
  deletion logs. No image, no demonstration text and no tmpfs file.

## 13. Final pull and verification (after `JOB DONE tier1` or `CAP STOP`)
1. Confirm the trap ran: job.log `EXIT tier1 rc=…`; the deletions log last line files = expect (TMAN_N + 1 + 7 with
   a1_decomp); `ssh -o BatchMode=yes hc1 '[ ! -e /dev/shm/c_pvr_hc ]'` rc 0 (CC-286 N5: the host may keep system files in
   /dev/shm, so only our dir is tested).
2. Stop the pull loop: `. "$HOME/s11_env.sh"; kpg "$PRE/pull.pid" s11_pull.sh` (pid file, whole process group, §10.2;
   W4, CC-286r2 N-a / N-i). The watcher has already ended at PUSHED.
3. Final pull, after a no-op wait for any running rsync:
   - `rsync -a -e 'ssh -o BatchMode=yes' hc1:c_pvr_out/ "$PULL/final/c_pvr_out/"`, excluding nothing;
   - plus `~/c_pvr_repo` HEAD and status (`git rev-parse HEAD`, `git diff --quiet HEAD --` rc).
4. Verify on the laptop:
   - `cd "$PULL/final/c_pvr_out" && sha256sum -c SHA256SUMS_tier1` (written by job.sh l.108 on JOB DONE). After a cap
     stop job.sh exits at l.87 before l.108, so the coordinator first writes `SHA256SUMS_tier1_cap` on the host with
     the same command (`cd ~/c_pvr_out && find out logs -type f | sort | xargs -r sha256sum`) and checks that one;
   - every `out/<set>.<arm>.jsonl` ends in `\n` and has unique ids (counts only);
   - CAP.json sha = the P1 line; `code_at_start_tier1.sha256` = the `H` shas;
   - `timing.jsonl` sha = the P1 line.
5. Copy `$PULL/final` to `.session_backup/machines/HC1/root/` (/mnt/d, one copy, with SHA256SUMS; no other heavy
   /mnt/d writer).
6. Line `OPS-<MMDD>c-hc1-pulled`: files, bytes, SHA256SUMS_tier1 sha, per-(set, arm) row counts, cut arms, the
   A8_WAIT records (`event A8_WAIT`), any STOP / torn-line record, CAP_STOP presence.

## 14. Wipe, delete, L-final, L-after
1. The wipe is already logged by the trap (host v3 §4.4); step 13.1 checked it. If `/dev/shm/c_pvr_hc` exists, run the
   RS-2 wipe command by hand, logged.
2. **L-final:** HC-1 per-instance spent (panel) and the account balance, just before the delete.
3. Delete HC-1 in the ckey panel. First check that the ssh port of the instance being deleted matches the `hc1` alias
   (E-G practice).
4. **L-after:** the balance; HC-1 absent from the panel. The block total = S_final = 38,493 + HC-1 spent ≤ M.
5. Line `OPS-<MMDD>c-hc1-deleted`: L-final, L-after, the deletion log line, the block total.
6. **Laptop retention:**
   - KT-C pixels K: one manifest-driven, non-recursive deletion after this pull, logged, with every `<K>.sha256*` sibling
     removed by exact name (R-H6 plan §11; CC-283 Ruling 6(b)). Tier 2 never uses KT-C.
   - `$PUSH` symlinks: removed by exact names, one `rm` per name, logged (no pixels in them).
   - `$EP` images stay until the tier-2 plan rules on them.

## 15. Result-read hand-off (S16; not part of this file's licence)
- No score is computed in S11-S15. The S16 laptop step needs, before the first SCORED output:
  - `score --tier 1` (bootstrap B = 10,000), the 'cây' sensitivity scorer and the T1-REP descriptives (CC-270 N14),
    each committed after its own code read;
  - the T1-ANALYSIS appendix (PI-1107d). It never delays S12-S15.
- **Hand-off package** (one OPS line `OPS-<MMDD>c-t1-handoff`, then the S16 read):
  - the §13 pulled set and its SHA256SUMS;
  - CAP.json (cuts, cap_h, block_max_vnd);
  - the P1 line;
  - every STOP / resume / re-push line;
  - the a1decomp line(s);
  - the S12 read id;
  - the L-final / L-after lines.
- The S16 read is one judge at 85, or a full panel at 85 on any STOP or FAULT (C_NEXT_STEPS S16).
- Cut arms are reported as "cut by the registered cap rule (T1-REP §9)", never as results.
- Model outputs are dev outputs and hold no gold. No agent reads captions for a judgement before the scorer exists.

## 16. Carried N-items: where each is closed

| item | what | status in S11 | section |
|---|---|---|---|
| CC-270 Q2 | A8 timing proxy | registered | §3 R3 |
| CC-270 Q3 | per-step loads in P1 | stated, with a measured check | §3 R11, §9.5 |
| CC-270 Q5 | speed sample | registered | §3 R4 |
| CC-270 Q6 | one tmpfs re-push per mode | budgeted | §5.3, §7 |
| CC-270 N1 / N1' | r_host rounded up, range check | stated (in code since CC-272) | §5.2 |
| CC-270 N3 | incomplete speed = FAULT | stated | §9.3 |
| CC-270 N5 (rest) | EN path | closed by CC-273 (check 7) | record |
| CC-270 N6 | loader paths proven on the host only | S12 criterion | §8.2 C9 |
| CC-270 N8 | source jsons on the host | closed by P5 (CC-277 R11) | §3 R14 |
| CC-270 N11 | torn last line on resume | closed here (watcher in code; decode by RS-3) | §11 RS-3 |
| CC-270 N12 | T_A rate proxy; `--sizes` pin | registered; sizes sha fixed | §3 R5, §2, §9.6 |
| CC-270 N13 | git checkout or bundle on the host | closed here: sparse partial clone | §1.4 |
| CC-270 N14 | laptop scorers before the first SCORED output | carried to S16 | §15 |
| CC-270r2 N-S11a | a1_decomp as covered material, departure, OPS line before the push, atomic push, line format | registered | §3 R14-R15, §10.3, §11 RS-6 |
| CC-270r2 N-S11b | watcher as a script; A8_WAIT_SEC and its reason | closed | §3 R10, §10 |
| CC-270r2 N-S11c | speed_start.epoch rule | stated | §9.1 |
| CC-270r2 N-S11d | transformers messages; bos_token_id | stated; S12 records | §3 R13, §8.2 C3/C7 |
| CC-270r2 N-S11e | M1 load rule | registered | §3 R12 |
| CC-272 N3 | S9 §5 pass-order departure | registered | §3 R9 |
| CC-272 N5 | A5 rule, 3 ids; shot sha check | registered; seal checks | §3 R2 |
| CC-272 N6 | M-CLIP pass cap check | closed by CC-273 | §10.1 |
| CC-272 N8 | open_clip attributes; real loaders | S12 criterion | §8.2 C5, C9 |
| CC-272 N9 | OPS record of evidence / harness | record line outside S11; not found in LOG at drafting | §17 D-R12 |
| CC-273 N1 (a)-(e) | T_A list, S1, torch 2.6, mm_projector, CPU-then-cuda | registered | §3 R6-R8 |
| CC-273 N4 | EN venv build, imports, 12-file fetch, refs/main, hostcheck-en, model_type, pad 0 | S12 criteria | §8.2 C7-C8 |
| CC-273 N5 | genconfig of both kinds | closed by CC-276 (check 10); S12 shows | §8.2 C3/C7 |
| CC-273 N6 | hostcheck_en mutant | dropped: closed by CC-276 (CC-282 R15) | – |
| CC-273 N8 | no rm -rf | rule | header |
| CC-276 W5 | exact-name kept access | rule; push farm | header, §7.1 |
| CC-276 W6 | D-VI train jsons statement | closed in code (CC-277 R11); stated | §3 R14 |
| CC-277 H1 / H2 / H3 | a12, embeddings, query TSVs | done: OPS-1106c-a12, OPS-1107c-emb, OPS-1107c-qtsv | §2 |
| CC-277 H4 | real builds, seal | done: TMAN 4849a08f (OPS-1107c-h4) | §1.2, §2, P6-P7 |
| CC-277 H5 | a1_decomp watcher | closed (code CC-282; procedure here) | §10.3, §11 |
| CC-277 N1-N3 | file-set check, whitelist, --pins | closed by CC-282 | – |
| CC-277 N4 | dry counts on another sha | record | – |
| CC-278 W7 | fold A1-A8 into a plan v1.1 | no v1.1 written; carried | – |
| CC-279 N2 | P5_W2 plan commit (eff19552) under CC-278 | still uncommitted; carried (gatekeeper item, not a rental gate) | §17 D-R12 |
| CC-279 N4 | d_tc pin | closed | §2 |
| CC-280 AM1-AM5 | freeze closure, parity, two-pass queries, speed stop, E-G sheet | closed (OPS-1107c-*; code at 8834926) | §2, §3 R18 |
| CC-280 AM6 / AM7 / AM8 | PI cites, carried list, §2 additions | closed | header, this table, §2 |
| CC-280 AM9; W5-W9 | SUMS race; sheet; watcher; S11 additions; W9 OPS | closed (own SUMS; CC-282; here; OPS-1106c-a12-source) | – |
| CC-280 Ruling 2(b) | env disclosure | stated | §1.1 |
| CC-281 N1-N6 | A12 script records | records of a finished run; no S11 effect | – |
| CC-281 N8 | redirect disclosure | moot: the fetch ran with 0 failures (OPS-1107c-ktc) | – |
| CC-281 N9 | prohibition text in briefs | closed | header |
| CC-282 N1 | H4 STOP lines in S11 | precondition | P7 |
| CC-282 N2 | hostcheck_fresh compares freeze | closed by CC-284 (c_pvr_gpu 9a9c6eb5 at H) | §1.1, §8.2 C2 |
| CC-282 N3 | encode source-text assert | next embed diff; no embed in S11 | – |
| CC-282 N4 | resume / re-push procedure | **closed here** | §11 |
| CC-282 N5 | LOG a1decomp line check | closed here | §10.3 |
| CC-282 N6 | --start format; heartbeat | procedure here; code carried | §10.4, §3 R17 |
| CC-282 N7 | `find . ! -type d` | closed by CC-284 (job.sh 9532c085 l.62) | §7.1 |
| CC-284 N1 | regular files only on tmpfs | procedure here (tar -h, link-member count 0, arrival `! -type d ! -type f` empty); the job.sh check is carried to its next diff, not a rental gate | §7.1, §7.2 |
| CC-284 N2 | own fault text for the freeze mismatch | next c_pvr_gpu.py diff; not a rental gate | – |
| CC-284 N3 | the export before direct probe calls | stated (S11 makes none; the export form if one is needed) | §8.1 |
| CC-284 N4 | R-P6 shas and job.sh line moves into S11 | closed (v1.1) | header, §1.1, §2, §8.2 C2, every job.sh line cite |
| CC-284 N5 | EN freeze on HC-1 ≠ 8e8a13c3 | fallback named: STOP at §6.5 setup.log, backstop job.sh l.76, no decode | §1.1, §6.5, §8.2 C7 |
| CC-286 W1 | DOC= names an unregistered file | closed: DOC = this v1.2 file; P1 also checks it is tracked | §1.3, P1 |
| CC-286 W2 | ENV4 unfixed; real decomposers never checked | closed: ENV4 fixed (H4 form); P21; 50 % threshold with basis | §1.3, P21, §4.1, §10.3, §12 |
| CC-286 W3 | §9.5 FAIL premise | closed: SHORT < U launches; SHORT ≥ U = no launch, PI | §9.5, §10.1 |
| CC-286 W4 | self-matching process patterns | closed: pid files plus a cmdline check; bracketed listings; P22 | §1.3, §10.2, RS-1, §13.2, P14, P15, P22 |
| CC-286 N1 | T_J1 laptop clock | closed: T_J1 from the host; skew check | §6.2, §10.2 |
| CC-286 N2 | env not sourced before $H / $TMAN | closed | §8.1, §9.1, RS-7 |
| CC-286 N3 | `.torn` overwrite | closed: `.torn.<stamp>`, "xb" | RS-3 |
| CC-286 N4 | manual wipe command | closed: written out | RS-2, §14.1 |
| CC-286 N5 | top-up list; `ls -A /dev/shm` | closed | §7.2, §13.1 |
| CC-286 N6 / N7 | NGRAM line; D-R12 records | preconditions P0a-P0d; the E-G repo record exists | §4, §17 |
| CC-286 N8 | v1.1 window | corrected | header |
| CC-286 N9 | machine-loss wording | PQ-S11-4: addendum read first | §18 |
| CC-286 N10 | P18 source | H4 run.log wall time / texts | P18 |
| CC-286 N11 | balance check owner | coordinator by hand; a missed check is logged, not a STOP | §5.3 |
| CC-286r2 W5 | stale §10.2 ENV4 text | closed | §10.2 |
| CC-286r2 W6 | rental gate range | closed: P0a-P0d, P1-P19, P21, P22 before the rental; P20 before push 1 | §0, §4 head |
| CC-286r2 W7 | resume watcher stop / relaunch | closed: RS-1 bounded with a PI STOP; RS-8 exact self-pid relaunch | §11.2, §11.3 |
| CC-286r2 N-a to N-i | doc text | closed | §A0 rows |
| CC-282 N8 | E-G free space | moot (E-G done); HC-1 tmpfs check | §6.2 |
| CC-283 N1-N4 | fetch-script hardening | carried to any future fetch diff; no fetch in S11 | – |
| CC-283 N5 | owner ledgers by keys / counts | rule | header |
| host v3 §1 / §3 / tmpfs / N77 | offer fields; ledger lines; measured tmpfs; T_A pixels from the laptop copy | closed | §5, §6.2, §7.1 (t_a from `$EP`, laptop copies) |
| E-G record | 6 streams; python3.12 prep; hostcheck `--out` mismatch | closed | §7.2, §6.3, §8.1 |

## 17. Rulings needed (one judge, REVERSIBLE 85)

| # | ruling | recommended | default |
|---|---|---|---|
| D-R1 | this file as the S11 run document and the rental trigger (§4-§15) | GO | no rental |
| D-R2 | the sparse partial clone on HC-1 (§1.4), never `git status` there | YES | the job.sh tree-manifest diff, or a PI line for a full clone |
| D-R3 | the push farm and six streams with the top-up rule (§7) | YES | single stream: projected 0.6-1.1 h per push; more cap lost |
| D-R4 | the S12 pass criteria C1-C10, read pre-queued (§8.2) | YES | the same |
| D-R5 | the load-second check of §9.5 (after `cap`, from CAP.json) as the CC-270 Q3 closure. FAIL with SHORT < U = launch and record; SHORT ≥ U = no launch, PI (v1.2, CC-286 W3) | YES | add load seconds by a code diff before the rental |
| D-R6 | the sizes file bytes and sha 1fcbc910 (§2, §9.6) | YES | the same |
| D-R7 | the resume rule RS-1 … RS-8, including **`--start` = T_J1**, which corrects CC-282 Ruling 8's "restarted job's stamp" (§11.2) | YES | each restart goes to a read with the PI told |
| D-R8 | RS-3 torn-line truncation by the fixed command (`.torn` keeps the bytes) | YES | a decode code diff before any resume |
| D-R9 | stop classes (§11.1): one watcher-only restart for transport-class FAULTs without a read | YES | a read for every restart |
| D-R10 | the HC-1 pull loop instead of gpu_backup.sh; HB_MAX 30 min with the P18 check (§12, R17) | YES | the same, with HB_MAX from P18 |
| D-R11 | the R1-R19 [proposal] items (§3) | YES | the same |
| D-R12 | records before registration, now precondition rows P0a-P0d: the E-G repo record (present, OPS-1107c-eg-repo-record), the CC-272 N9 line, the CC-279 N2 status, an NGRAM PASS line for this file (CC-286 N6, N7) | coordinator lines | the same |
| D-R13 | registration: one gatekeeper commit of exactly this file, NGRAM PASS, no host / port / attribution string | YES | the same |
| D-R15 | (v1.2) ENV4 = the H4 form (§1.3); P21 real-decomposer check; decomposition threshold M > 50 % of N on any set = systematic, read and DEGRADED label; below that, record only (§10.3; CC-286 W2) | YES | the same |
| D-R16 | (v1.2) pid-file stops and bracketed listing patterns only; P22 check (CC-286 W4) | YES | the same |
| D-R17 | (v1.3) RS-1 bounded 60 s wait, else OPS line + listing + PI STOP; RS-8 relaunch by the self-pid form with the old pid file moved aside; kpg for the pull loop's group (CC-286r2 W7, N-i) | YES | the same |
| D-R14 | (v1.1) CC-284 N1 procedure (tar -h, link-member count 0, arrival non-regular count 0) and N5 fallback (EN freeze STOP at §6.5, backstop job.sh l.76, no decode, diff read) | YES | the same |

## 18. PI questions (each with a recommendation and a default; Vietnam time = UTC+7)

| # | question | recommended | default |
|---|---|---|---|
| **PQ-S11-1** | If no ckey offer meets every field on the rental day (the PI-1107a floor: 1× 3090 / 3090 Ti, CPU ≥ 5800XT class, RAM ≥ 32 GB, disk 200 GB ≥ 1000 MB/s, net ≥ 400 Mbps, CUDA ≥ 12.4, uptime > 99 %, max time ≥ 72 h), do we wait, or do you pick the closest offer as you did for E-G? | wait, with a poll every 15 min for up to 12 h. Then you get the closest offer with one line on what it misses | wait; nothing off-spec is rented without your line |
| **PQ-S11-2** | If B's or A's GPU block is live at C's rental or at the P1 line, and C needs the 465k option (PQ-C2), the balance is short (about 760k against about 426k + about 332k). Top up first, or keep C at 350k (more cut arms)? | keep 350k unless you top up anyway for B (PI-1107b) | 350k; the cap rule cuts in the registered order |
| **PQ-S11-3** | Only if the reader rejects the sparse repo (§1.4): may a full repo copy sit on the rented disk? It would hold labelled and other papers' files (none opened, none used), deleted with the machine | NO: use the tree-manifest code diff (about 1 h) | no full copy; the diff route |
| **PQ-S11-4** | If HC-1 is lost mid-block (machine loss), may a second 3090 be rented once (host v3 H-4), with the pulled outputs pushed back so that finished steps are not re-run, and no new speed test? | YES in principle, but only after a one-judge read of a short machine-loss addendum, before any re-push (CC-286 N9). The reasons: the 30-min loop pulls with `rsync --partial` and no sha check; `cap` refuses a second CAP.json; the P1 wall clock keeps running through an outage; and a new host needs a fresh S12 | the machine stays deleted; the PI is asked at the time |

Not asked: the speed stop (PI-1106l and AM4 fixed it); the laptop on for about 30 h (PI-1106m, re-confirmed on the
day in P17); the money cap (registered).

## 19. Touches during drafting (`date -u` 2026-11-07 about 02:30-03:05Z)
- **Read:** the sources at the top (code text; CC and LOG text); `R_EMB_JOB_SHEET_v1.md`; PRE_S11_PLAN_v1.md.
- **Read, E-G pull:** `.session_backup/machines/EG/root/{prep.log, setup_*.out}`, `c_pvr_out/logs/setup.log` (stamps),
  `probe/HOSTCHECK_OK.json` and `HOSTCHECK_EN_OK.json` (keys, echo, genconfig ids, vram). Names of `c_pvr_out/`.
- **Listed / measured (names, sizes and counts only):**
  - `~/c_pvr_eg_1107/` and `emb_push/images/` (set dir names; `du -sb` of the five non-KT-C query sets);
  - `du -sb` of K;
  - `~/c_pvr_p5_out/democap/` names and the d_tc.json size;
  - `df` of `~` and `/dev/shm`;
  - `git ls-files` counts by top dir and `git ls-files data | head` (file names only, none opened).
- **Read, laptop config:** `~/.config/vsps/` names; `gpu_backup.sh` text, which holds older machines' host and port
  strings. They were seen on screen only and are written nowhere, this file included.
- **Scratch:**
  - `/tmp/s11_hr_1107/hr`: a sparse partial clone of the repo at 9b3fd8d (36 code blobs, no data/ file) and one
    `c_pvr_gpu.py selftest` run in it (rc 0, 34 s, ~/.venvs/vsps_j_m0, env -i). Left in place, never rm -rf;
  - `/tmp/s11_sizes.json` (the sizes bytes, for the sha); `/tmp/s11_pull_test.sh` (the §12 extraction test: 18 lines,
    `bash -n` OK, 0 `/dev/shm`).
- **Code greps for §1.4:** repo-root reads in c_pvr_gpu.py and c_pvr.py; the keys and value types of ovqa_pin.json,
  ovqa_count_rule.json and g_c2_provenance.json (tracked C prereg files; pins and field names only).
- **Not touched:** ~/.vsps_sealed (not opened, listed or statted); the file of hand rows; any `t2pool_*` file;
  `c_datastores/` (not listed); any caption json, label file or test material; K's files (size only); any host.
- No network, no rental, no commit, no LOG write.

**v1.1 touches (`date -u` 2026-11-07 about 03:10-03:31Z):**
- **Read:** CC-284 (Rulings 1-8, required fixes, gatekeeper); LOG l.1763-1770; the H4 record
  `~/c_pvr_h4w_1107/H4_RECORD.txt` (counts and shas); `c_pvr_job.sh` at H (all lines, for the line moves);
  `c_pvr_gpu.py` hostcheck_fresh at H.
- **Listed / hashed:**
  - `~/c_pvr_h4_1107` names and sizes; `sha256sum` and `wc -l` of its MANIFEST.sha256; MANIFEST path classes
    (counts by top dir);
  - `stat -c %s` of the 11,571 mapped source files, sum only. Kept files by exact name; no listing of
    `c_datastores/`; K's files by size only;
  - the code shas at H.
- **Scratch:** `/tmp/s11_hr_1107b/hr`, a sparse partial clone at H = 1880951 (36 blobs; SUMS OK; selftest rc 0 at
  9a9c6eb5). Left in place.
- **Not touched:** the same list as v1. No network, no rental, no commit, no LOG write.

**v1.2 touches (`date -u` 2026-11-07 about 04:00-04:30Z):**
- **Read:** CC-286 in full, incl. AD1; LOG l.1771-1776 (OPS-1107c-eg-repo-record); `~/c_pvr_h4w_1107/bin/run_sets.sh`
  (l.1-40) and `run.log` (stamps); c_pvr.py l.626-717 (decompose_vi / decompose_en).
- **Read, keys only:** vi_oiv7_map.json (69 keys, membership of four nouns) and en_oiv7_map.json (four forms).
- **Run, laptop, in /tmp:** the `kp` helper on two dummy `sleep 300` processes (one pid file each; one plain `rm -f` of
  one stale test pid file, no rm -rf).
- **Run, laptop, at H:** the P21 block (rc 0, PASS) and two negative controls (missing VNCORENLP_DIR; java off PATH),
  each on the four synthetic sentences only. No dataset text was used.
- No network, no rental, no commit, no LOG write. No process-pattern kill or count was used. ~/.vsps_sealed and
  `c_datastores/` were not touched.

**v1.3 touches (`date -u` 2026-11-07 about 04:20-04:45Z):**
- **Read:** CC-286r2 in full.
- **Run, laptop, in /tmp:** `kpg` on one dummy process group (a bash session leader and two `sleep` children, its own
  self-written pid file `/tmp/s11_kpg_test.pid`): wrong name rc 1; right name rc 0, 0 processes left. No pattern kill.
- No network, no rental, no commit, no LOG write; ~/.vsps_sealed and `c_datastores/` were not touched; no rm -rf.
