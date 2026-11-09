# C-DIAG code readings (for the S0r one-judge code read, reversible 85)

Prereg `manuscript/prereg/2026-11-08_c_diag/C_DIAG_PREREG_DRAFT_v1_2.md` (afbb61fb, registered at aa46a3a), read with
`.session_backup/2026-10-13/decisions/CC-299r3.txt` (0fdaa23b) R1-R8. Label: EXPLORATORY (C-DIAG). Nothing here has run
on data: R7 forbids any §10.2 subcommand before this code is committed with `SHA256SUMS` and its code read is GO.

## Files (§10.2)

| §10.2 item | file | venv |
|---|---|---|
| 1 Stage-0 laptop code, `allow` guard, solvency | `c_diag.py` | `~/.venvs/c_pvr` |
| 2 host code | `c_diag_gpu.py` | CC-212 decode venv (B-N1 packages) on HD-1 |
| 3 job | `c_diag_job.sh` (+ `c_diag_job_selftest.sh`) | bash |
| 4 scorer (`gate`, `cider`, `score`) | `c_diag_score.py` | `c_pvr` (`cider`: `c_pvr_cider`) |
| 5 CPU selftest | `test_c_diag.py` (+ `c_diag_mutants.py`) | `~/.venvs/c_pvr_cider` |
| 6 sums | `SHA256SUMS` | |
| 7 §4.5 mBLIP table | `c_diag_t1table.py` | `c_pvr` |

## Rule -> code (each anchor line holds the token it was found by; regenerated after the last edit; the row count is printed under the table)

| prereg rule | where | file:line |
|---|---|---|
| l.18-19 label on every output | LABEL | `scripts/c_diag/c_diag.py:40` |
| §1.3 [Q8] floor c_b = N_A/(N_A+N_P), ranks 1..k_b, unknown out | floor() | `scripts/c_diag/c_diag.py:526` |
| §1.3 floor 0.10 [proposal] | FLOOR | `scripts/c_diag/c_diag.py:126` |
| §1.3 c_b >= 0.10 | floor_pass | `scripts/c_diag/c_diag.py:547` |
| §1.3 [R2-W1 (a)] gate-only iff both c_b < 0.10 | gate_only_branch | `scripts/c_diag/c_diag.py:551` |
| §1.3 / §8.4 other empty main run = no rental | rental flag | `scripts/c_diag/c_diag.py:792` |
| §2.3 [W10] allow-list; FAULT on any other open; order of checks | Guard | `scripts/c_diag/c_diag.py:177` |
| §2.3 deny backstop (exact names / prefixes, .vsps_sealed) [R2-W7] | deny() | `scripts/c_diag/c_diag.py:164` |
| §2.3 deny patterns | DENY | `scripts/c_diag/c_diag.py:117` |
| §2.3 / NB-2 per-subcommand lists (row 8 only in label-subset) | SUBCMD | `scripts/c_diag/c_diag.py:103` |
| Appendix B rows 1-15 (path, sha256) | B | `scripts/c_diag/c_diag.py:46` |
| Appendix B row 12 (eight CC-212 preds) | PREDS | `scripts/c_diag/c_diag.py:71` |
| Appendix B row 17 code pins (§10.1) | CODE | `scripts/c_diag/c_diag.py:91` |
| Appendix B row 16 VnCoreNLP files | allow(helpers) | `scripts/c_diag/c_diag.py:280` |
| §2.3 selftest: Appendix B paths pass, stray copies and ~/.vsps_sealed refused | st_backstop | `scripts/c_diag/test_c_diag.py:92` |
| §2.4 [NB-3] label subset read once, XM600 discarded, keys asserted | label-subset | `scripts/c_diag/c_diag.py:734` |
| §2.4 NB-3 key assert on every later read | S0.status | `scripts/c_diag/c_diag.py:413` |
| §2.4 [W5] XM refs: staging file only, 2,500 keys, release 101d24ad; OV-dev-B keys only | references() | `scripts/c_diag/c_diag_score.py:343` |
| §3.1 decompose_vi over shown captions of ranks 1-8 | S0.decomp | `scripts/c_diag/c_diag.py:395` |
| §3.2 [W9 (a)] obj only, rank order, CAP 32, text never asked | verify_image | `scripts/c_diag/c_diag_gpu.py:67` |
| §3.2 remove REJECTED obj only | filt_masks | `scripts/c_diag/c_diag_gpu.py:79` |
| §3.2 prompt ver_3way, greedy, 8 tokens, batch 1, chat template | asker | `scripts/c_diag/c_diag_gpu.py:300` |
| §3.3 P_obj, P_wrong, R_obj, CHAIR_i, CIDEr-VI columns, flags | block_xm | `scripts/c_diag/c_diag_score.py:450` |
| §3.3 [N20] count-matched ΔP_cm | pcm | `scripts/c_diag/c_diag_score.py:416` |
| §3.3 VI-script guard, empty = non-VI, empty share | text_cols | `scripts/c_diag/c_diag_score.py:434` |
| §3.3 mention-share flag > 5 points | flag | `scripts/c_diag/c_diag_score.py:510` |
| §3.3 RESCAP_RAW_TONE unset | raw_tone_unset | `scripts/c_diag/c_diag_score.py:616` |
| §3.3 CIDEr-VI pinned route, as written + stripped | cmd_cider | `scripts/c_diag/c_diag_score.py:387` |
| §3.3 fallback / emptied shares, removed per image | arm_counts | `scripts/c_diag/c_diag_score.py:591` |
| §4.1 unit: one mapped class, present / absent | unit_ok | `scripts/c_diag/c_diag.py:463` |
| §4.1 bare rule | is_bare | `scripts/c_diag/c_diag.py:453` |
| §4.1 [N8] '_' tokens split into syllables | syllables | `scripts/c_diag/c_diag.py:448` |
| §4.1 order sha256(qid, rank, prop_index, class, salt c_diag_gate joined by a bar) | gate_units | `scripts/c_diag/c_diag.py:468` |
| §4.1 [W2] ladder (a)/(b)/(c), 150, 100-149, < 100 FAULT | ladder | `scripts/c_diag/c_diag.py:495` |
| §4.1 host file: no status | host_units | `scripts/c_diag/c_diag.py:518` |
| §4.1 image-blind pass (text-only chat path) | text_only | `scripts/c_diag/c_diag_gpu.py:115` |
| §4.2 measures, denominators | gate_table | `scripts/c_diag/c_diag_score.py:230` |
| §4.2 κ, degenerate = undefined | kappa | `scripts/c_diag/c_diag_score.py:116` |
| §4.2 [NB-1] κ CI, clusters, seed 20261109, > 1 % = gate FAULT | kappa_ci | `scripts/c_diag/c_diag_score.py:255` |
| §4.3 V1-V5 PASS rule | verdict | `scripts/c_diag/c_diag_score.py:278` |
| §4.3 / R2-W1 (d) gate-only: verdict only after the logged delete | cmd_gate | `scripts/c_diag/c_diag_score.py:308` |
| §4.3 [N2] verdict wait 1.0 h (main) | job | `scripts/c_diag/c_diag_job.sh:27` |
| §4.4 in-situ table, odds identity, zero-cap-hit ratio [R2-W10 (d)] | insitu_table | `scripts/c_diag/c_diag_score.py:539` |
| §4.5 [R2-W5] mBLIP table: own nine inputs, narrow manifest check, own draw | c_diag_t1table.py | `scripts/c_diag/c_diag_t1table.py:113` |
| §4.5 narrow T4 line, f81323d1 | t5_sha | `scripts/c_diag/c_diag_t1table.py:58` |
| §4.5 cells = c_pvr_score.py l.393-403, 3,000 ids [NB-C2] | cells | `scripts/c_diag/c_diag_t1table.py:66` |
| §4.5 seed 20261111, idx (10000, 3000) [DC1] | boot | `scripts/c_diag/c_diag_t1table.py:98` |
| §4.5 > 1 % undefined = FAULT [NB-C1] | faults | `scripts/c_diag/c_diag_t1table.py:108` |
| §5.1 arms rand / ret / filt / ctl, zero-shot fallback | arm_prompt | `scripts/c_diag/c_diag_gpu.py:101` |
| §5.1 [N4] ctl = a7_masks on obj-only masks, arm_rng A7 | ctl_masks | `scripts/c_diag/c_diag_gpu.py:84` |
| §5.1 InternVL3 'last' prompt order; verify in rank order | prompt_order | `scripts/c_diag/c_diag_gpu.py:96` |
| §5.2 execution order | ORDER | `scripts/c_diag/c_diag.py:139` |
| §5.3 CC-212 ret / rand prompts rebuilt and sha-checked (laptop) | work_file | `scripts/c_diag/c_diag.py:678` |
| §5.3 same check on the host | run_block | `scripts/c_diag/c_diag_gpu.py:359` |
| §5.3 [NB-6, DC2] byte-equal computable only with CC-212 order and batch | vi_pre | `scripts/c_diag/c_diag.py:583` |
| §5.3 byte-equal share | byte_equal | `scripts/c_diag/c_diag_score.py:601` |
| §6.1 [N1] one generator 20261108: idx_XM then idx_OV | cmd_score | `scripts/c_diag/c_diag_score.py:634` |
| §6.1 > 1 % undefined replicates = FAULT (block) | est | `scripts/c_diag/c_diag_score.py:148` |
| §6.1 [W4, R1] arm-swap permutation p, R = 10,000, seed 20261110, floor 1/10,001 | perm_p | `scripts/c_diag/c_diag_score.py:164` |
| §6.1 swaps drawn once, shared across contrasts | swaps | `scripts/c_diag/c_diag_score.py:640` |
| §6.3 [W1 (a)] Holm over the P_obj family, m from completed blocks, recorded first | m record | `scripts/c_diag/c_diag_score.py:633` |
| §6.3 Holm step-down | holm | `scripts/c_diag/c_diag_score.py:177` |
| §6.4 per-contrast state (D.1) | p_state | `scripts/c_diag/c_diag_score.py:189` |
| §6.4 summary label (D.2) | summary | `scripts/c_diag/c_diag_score.py:202` |
| §6.4 C1-C4 / R1-R4 | harm_state | `scripts/c_diag/c_diag_score.py:218` |
| §6.4 GF / GC / GB (both labels) | guard_of | `scripts/c_diag/c_diag_score.py:223` |
| §6.4 OV-dev-B CIDEr states, punctuation-dependent | block_ov | `scripts/c_diag/c_diag_score.py:563` |
| Appendix D enumeration against the scorer's functions | st_stats | `scripts/c_diag/test_c_diag.py:331` |
| §7 pins from the CC-212 records (B-N1, preds provenance) | pins | `scripts/c_diag/c_diag.py:828` |
| §7 snapshot pinned revision, B-N1 venv, check_snapshot | model | `scripts/c_diag/c_diag_gpu.py:288` |
| §7 [N16] VRAM peak at a full k-demonstration prompt | hostcheck | `scripts/c_diag/c_diag_gpu.py:408` |
| §7 offline | job | `scripts/c_diag/c_diag_job.sh:28` |
| §8.1 exact Stage-0 counts | counts | `scripts/c_diag/c_diag.py:607` |
| §8.2-8.3 pre-rental re-projection and cut order | plan | `scripts/c_diag/c_diag.py:632` |
| §8.3 20 h / 210,000 VND, gate-only 3.0 h [R2-W1 (b)] | hour_cap | `scripts/c_diag/c_diag.py:656` |
| §8.3 [N10, Q7, R2-W8] solvency, every term logged [NB-C4] | solvency | `scripts/c_diag/c_diag.py:663` |
| §8.3 CAP.json at the rental, live offer rate [NB-C6] | cmd_cap | `scripts/c_diag/c_diag_gpu.py:432` |
| §8.3 billed time from the rental stamp, 0.5 h for pull/delete | left | `scripts/c_diag/c_diag_gpu.py:179` |
| §8.3 [N2] projection + sticky cuts (stage start, 100 queries) | project | `scripts/c_diag/c_diag_gpu.py:229` |
| §8.3 cut order constants | CUT_ORDER | `scripts/c_diag/c_diag.py:141` |
| §8.4 cap stop final; FAULT stop; 3 attempts | step() | `scripts/c_diag/c_diag_job.sh:83` |
| §8.4 money stop marker | FINAL | `scripts/c_diag/c_diag_job.sh:38` |
| §8.4 FAULT exit code 9 | FAULT_RC | `scripts/c_diag/c_diag_gpu.py:34` |
| §8.4 a partial block: incomplete, never opened, by score and cider [CC-307 W3] | complete_block | `scripts/c_diag/c_diag_score.py:364` |
| §8.4 cider admits complete blocks only [CC-307 W3] | hyps | `scripts/c_diag/c_diag_score.py:370` |
| §5.3 OV-dev-B byte-equal share for ret and rand [CC-307 W2] | cmd_score | `scripts/c_diag/c_diag_score.py:663` |
| CC-307 W1 every interpreter call with -X utf8 | job | `scripts/c_diag/c_diag_job.sh:19` |
| CC-307 W1 the job selftest fails a call without -X utf8 | stub | `scripts/c_diag/c_diag_job_selftest.sh:31` |
| CC-307 N1 guard: entries, then deny, then write-only out dirs / read-only runtime | Guard.why | `scripts/c_diag/c_diag.py:221` |
| CC-307 N1 an out dir with a deny component is refused | allow | `scripts/c_diag/c_diag.py:272` |
| CC-307 N2 absolute SUMS paths refused | pulled | `scripts/c_diag/c_diag_score.py:71` |
| CC-307 N3 cap stop during the verdict wait | job | `scripts/c_diag/c_diag_job.sh:132` |
| CC-307 N5 --rate required for the re-projection | projection | `scripts/c_diag/c_diag.py:788` |
| §9 / Appendix C 3 tmpfs only, arrival sha check [NB-C3] | job | `scripts/c_diag/c_diag_job.sh:73` |
| Appendix C 4 / R2-W1 (c) gate-only push: gate material only | job | `scripts/c_diag/c_diag_job.sh:78` |
| Appendix C 4 no label on the host (no data/ in the repo copy) | job | `scripts/c_diag/c_diag_job.sh:60` |
| Appendix C 4 host open guard | host_guard | `scripts/c_diag/c_diag_gpu.py:52` |
| Appendix C 6 trap wipe + deletion log | teardown | `scripts/c_diag/c_diag_job.sh:41` |
| CC-297 N-4 SUMS after JOB DONE and EXIT | teardown | `scripts/c_diag/c_diag_job.sh:46` |
| CC-298 J3-N3 manifest sha as an argument | job | `scripts/c_diag/c_diag_job.sh:22` |
| §9 [N18] text-bearing outputs never under the repo | allow | `scripts/c_diag/c_diag.py:270` |
| §9 push manifests per branch [NB-C3] | push_manifest | `scripts/c_diag/c_diag.py:705` |
| §14 item 7 VI-script precondition per block | vi_pre block_ok | `scripts/c_diag/c_diag.py:603` |
| §14 item 5 XM-test2500 image sha list = lists.json | manifest | `scripts/c_diag/c_diag.py:812` |
| R1 H0 / independence wording | perm_p doc | `scripts/c_diag/c_diag_score.py:166` |
| R3 gate-only: one verifier incomplete = whole branch incomplete | cmd_gate | `scripts/c_diag/c_diag_score.py:320` |
| R5 no ret - rand number | (none computed) | `scripts/c_diag/test_c_diag.py:818` |
| R6 / NB-C5 §4.5 runs in every branch | t1table doc + next hint | `scripts/c_diag/c_diag.py:723` |
| R7 no Stage-0 subcommand before the code read GO | doc | `scripts/c_diag/c_diag.py:17` |

109 rows.

## CC-299r3 NON-BLOCKING items routed to this code read

| item | handling |
|---|---|
| NB-C1 [J1 N-2] | `c_diag_t1table.faults()` applies the > 1 % undefined-replicate FAULT to every `s1_table` estimate (s1_table keeps `strict=False`); test + mutant T3. |
| NB-C2 [J3 NB-3] | `c_diag_t1table.cells()` is c_pvr_score.py l.393-403 (and its T/UN/KR/DS column appends) unchanged except the loop over the 3,000 sorted ids; test + mutant T4. The `allow` hook is a `sys.addaudithook` on every Python-level open, so opens inside imported helpers (`CP.pinned`, `rescap_mods`, `XO.resolve_map`, `CP.rdr`'s VnCoreNLP hashing) are checked; every subcommand runs end to end under the real hook in the selftest. |
| NB-C3 [J3 NB-4] | `manifest` writes `push_main/` or `push_gate_only/` (gate-only = gate images + gate unit file only); the job checks TMAN, every arrival sha, the exact file set, and in `gate-only` mode refuses any other file (job scenario 2, mutant J2). |
| NB-C4 [J1 N-8, J2 N5] | `solvency` logs every term per check; h_B = HB-T1 + HB-T1' billed hours, Σ_live given excluding both; the O_B = 0 under-reserve note is printed with every check. |
| NB-C5 [R6] | §4.5 has no branch precondition in code; `manifest` (rental or not) and `pins` print the R6 next-step line. It stays coordinator-run (T5 holds train caption text). |
| NB-C6 [J3 NB-9] | No 10,091.01 constant: `hour_cap(rate)` and CAP.json use the live offer rate (`--rate`); §8.2 planning figures only appear as [est.] rates. |

## Readings and choices made here (PI-1109d: the drafter's; none is a PI kind)

1. **Pulled host files** are not Appendix B rows: they are admitted by (path, sha) from the pulled `SHA256SUMS_<mode>`, whose own sha is a CLI argument (the tier-1 `records()` form). Stage-0 outputs are never read back except the label subset (row 9, by `--labels-sha`); every other derived value is recomputed in-process. **This widens nothing silently but is a reading of Appendix B for the code read.**
2. **Main branch = one job**: gate -> `SHA256SUMS_gate` (logs excluded, so the log stays verifiable later) -> wait ≤ 1.0 h for `VERDICT.json` (relayed by the coordinator from `c_diag_score.py gate`) -> S2/S3. The tmpfs trap therefore wipes only at the job's end. `gate-only` mode exits after the gate.
3. **One model load per backbone in S2/S3** (`run --model`): verify -> texts -> decode per set in §5.2 order (matches §8.2's four loads). Projection: LOAD_H = WAIT_H = 0.12 h (4 loads + 1 round trip = 0.6 h), overhead 1.4 h, pull 0.5 h [est.]. The in-run projection runs at each job step start (each `gate.<model>` and `run.<model>`), at the end of S1, and inside a step after the first 100 queries of each phase (verify, each decode arm) [CC-307 N6]. Measured rates replace planning rates (the gate image-pass rate first, then each phase's own).
4. **Cap stop margin**: each step's timeout is cap − billed elapsed − 0.5 h, so pull and delete fit in the cap.
5. **Crash vs FAULT**: a FAULT exits 9 (JOB STOP, no retry); any other non-zero rc is a crash, retried to 3 attempts.
6. **Permutation draw**: `default_rng(20261110).integers(0, 2, size=(10000, 2500))`, one row per permutation, shared by every contrast; ties counted with a 1e-9 tolerance.
7. **A block whose estimates hit > 1 % undefined replicates** is reported `FAULT (final)` and keeps its Holm slots at p = 1 (m unchanged, never a reject).
8. **Gate-only verdict** needs `--deleted-utc` later than the pulled `JOB DONE` / `CAP STOP` line (R2-W1 (d)); in that branch one incomplete verifier makes the whole branch incomplete (R3).
9. **Unit indices**: `rank` = 1-based retrieval rank; `prop_index` = 0-based index into `dc["props"]` (all kinds).
10. **filt with nothing removed** still goes through `rebuild` (tidy); `counts` reports `tidy_changed_demos`, the number of demonstrations where that differs from the shown caption.
11. **Borrowed read-only helpers** (choices): `c_pvr_score.VI_SPECIFIC` / `tokens` for the VI-script guard and syllables (tier-1 §5.7(b) definition); `c_pvr_cider_vi.tok / cider / in_range / jdk` for CIDEr-VI (the CIDER_VI_PIN_v1_1 producer route; its set table is not used); `c_pvr_gpu.wipe`. The `survival` and unit rule are re-implemented in a few lines in the c_pvr_score form (tested).
12. **Host**: the repo copy must hold no `data/` (labels are tracked in git); the host hook refuses any open under `data/` and the §2.3 backstop. `registration()` and the zero-shot prompt are loaded once before any hook (they lazily read `scripts/evaluate.py`), and the zero-shot prompt is checked against 8870589c.
13. **N15**: `c_stage1/guard.py` l.30 imports `objects_in` from `rescap.chair` unchanged, the function C-DIAG calls (raw_tone=False, RESCAP_RAW_TONE unset, the 69 keys). CC-212's `oiv7_counts` counted `caption_rows(set(objects_in), …, set(vmap))` = the same mapped mentions, so P_obj^VI is the same form.
14. **Stray `ktvic/test_data.json` copies**: tested by the recorded path prefixes (CC-299 l.57-58); the refusal is by basename, so their exact depth does not matter. Neither copy was listed or opened.
15. **Pre-hook opens [CC-307 N8]**: `D.load()` (sha-checked imports of decode_icl, c_pvr, xm3600_oiv7, decode_hf_vlm; `rescap_mods`), `registration()` (B-N1 json, DESIGN.md, `scripts/evaluate.py`, `scripts/g2b/decode_qwen3vl.py`), `c_pvr_score.load()` / `mention_fns()` (§4.5 only) and `c_pvr_cider_vi.load()` (cider only) run before the hook is installed, so the guard does not see them. They read code and registration files only (no data row); the zero-shot prompt they yield is checked against 8870589c.
16. **UTF-8 mode [CC-307 W1]**: every documented invocation and every job call uses `-X utf8`. Under `LC_ALL=C -X utf8=0` the host subset still passes (explicit encodings, N7); the full laptop suite needs `-X utf8` because the reused `c_pvr.rdr` pipes text to java in the locale encoding.

## Not exactly as registered (disclosed)

- **TMAN / T4**: the allow entry for T4 carries TMAN, so the guard and the explicit `sha(T4) == TMAN` check both enforce it (mutant T1 kills the explicit one).
- **RESCAP_RAW_TONE**: asserted at the head of `score`, and again by `decompose_vi` itself; a mutant of the explicit line would survive because of the second check, so it is not in the mutant list.
- **Parity re-decode under batched greedy decoding** is exact only if the host's software stack equals CC-212's; the job checks the pip-freeze sha in CAP.json against the CC-212 record (`pins`; CC-307 found 685ffe2a… in all eight Appendix A preds files).
- **GPU paths** (`gate`, `run_block`, `hostcheck`) are tested on the laptop with a fake model only; the real model calls are checked at HD-1 by `hostcheck` (selftest mode) before any S1 step.
- **Wiped tmpfs between gate and main**: not needed (one job), see reading 2.
