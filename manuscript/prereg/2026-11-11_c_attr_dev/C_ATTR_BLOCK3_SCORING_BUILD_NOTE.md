# C-ATTR-DEV block 3 scoring package: build note

Written 2026-11-12T22:05Z (`date -u`). It goes with `C_ATTR_BLOCK3_SCORING_RUN_DOC_v1.md` and `scripts/c_attr/C_ATTR_B3SCORE.diff` (`1dc1a1c0…`; `git diff HEAD -- scripts/c_attr` at `60358b2`; 4 files, +429 / −13). Not committed; nothing staged, stashed or checked out. Label: `DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY`.

## Changed

| file | sha256 | change |
|---|---|---|
| `scripts/c_attr/c_attr_score.py` | `cca5e327…99c0` | Adds the block-3 constants, including `K7_UTC`, `CLOCK`, the E6/N1/O9/O8 strings, the pins and `TEST_NAME`. Adds the `b3verify`, `b3k5` and `b3rest` stages and their helpers: `k7_open`, `test_named`, `b3_id`, `b3_runs`, `full_set`, `b3_rows`, `k5_verdict`, `b3_pins` and `d1_b3`. Moves 1b's §7.1 gate unchanged into `parity_7_1`, which both verifies call. `cmd_stage` gains the K7 check first for block-3 stages, `VERIFY.json` as the head of both chains and `REG_B3`. `--work` now defaults per chain, and `--b3-sums` is added. Adds `selftest_b3` (planted columns) and `selftest_b3_chain` (planted tree through the unstubbed `c_attr.cmd_score`, called at the end of `selftest_chain`), plus one ok item each |
| `scripts/c_attr/c_attr_mutants.py` | `082a0d30…bb53` | Adds B11–B34 (24 mutants, all on `c_attr_score.py`) |
| `scripts/c_attr/c_attr_score_job.sh` | `2515c733…8d98` | Adds `c_attr_b3/RUNNING` to the refusal loop and `W=/root/c_attr_score_b3` for the `b3*` stages, plus usage lines |
| `scripts/c_attr/SHA256SUMS` | `886aaf63…8ece` | The same 8 lines in the same order; three hashes are new |

`c_attr.py` (a3bd7b93), `c_attr_job.sh` (d367f3c6), `c_attr_lists.py`, `dryrun.sh` and `STORED_SHA256` are byte-equal to HEAD (re-hashed). Every existing behaviour of `verify`, `ova`, `close`, `ovb`, `rest` and `posthoc` is unchanged.

## Checked here (laptop: only `py_compile`, `bash -n`, `sha256sum`, `git diff`, `grep`, `sed -n`, `wc`)

- `python3 -m py_compile` passes for `c_attr_score.py` and `c_attr_mutants.py`. `bash -n` passes for `c_attr_score_job.sh`. `sha256sum -c SHA256SUMS` gives 8 × OK.
- Each of the 24 new mutant patterns, and each of the 57 old S patterns, occurs exactly once in `c_attr_score.py` (`grep -o -F … | wc -l` = 1). The A and L patterns are untouched because their files are unchanged. Every new pattern is a single line.
- The full sha256 of the 1b nomination file `data/results/c_attr_1112_score/res/c_attr_nomination.json` is 559c18c1…ebdfa, equal to CC-363 1a. The VERDICT (a69a0ec2) and SUMMARY (1d78cd20) values come from that folder's committed SHA256SUMS.
- The reference pins are copied from CC-362 (550cfe06…, 0da82355…); neither file was opened or hashed by me.
- The new ok strings hold no "; ", so the `c_attr_score selftest ok:` line splits into 20 + 2 = 22 fields.

## Not checked (needs the host; the PI rule bars tests on the laptop)

- No self-test, mutant or stage has run. Expected values are in the run doc §5 S0: 3/1/1 ok lines; NF 22/22/22, 5, 22; 107/107 killed. The killing assertion of each new mutant, desk-checked:

  | mutant | killed by |
  |---|---|
  | B11 | `k5_verdict({"d": 2.0, "p": 0.02500001})` |
  | B12, B13, B14 | the planted d values (−2, 50, 9) |
  | B15 | "no note" |
  | B16, B17, B18 | the wording, decodes and batch asserts |
  | B19 | the XM tiers |
  | B20 | `k7_open` at exactly `K7_TS` |
  | B21 | `cmd_stage` b3k5 after K7 must name K7 |
  | B22 | the planted `xm_test2500_q.json` (verify must say "test-set") |
  | B23 | the name list |
  | B24 | the pin scenario |
  | B25 | the RUNNING scenario |
  | B26 | the D1 FAIL scenario raises |
  | B27 | three runs found, so K5 is refused |
  | B28 | the CAP-STOP scenario must say "judge line" |
  | B29 | the stray scenario |
  | B30 | the stamp on the D1 FAIL Qwen row |
  | B31 | the tampered `K5.json` copy |
  | B32 | `full_set(["i1"], "xm_dev500")` |
  | B33 | the `rand_img` run-id string |
  | B34 | V4 (1) refuses K5 without the nomination file |

- The chain test assumes that `c_attr.cmd_score` handles an LMCap-only call with no `zs` (empty `score_set` input). This path has not run before: the 1b chain always had a `zs`. If `score_set` fails on an empty run list, S0 stops, and the fix goes to the judge.
- Planted DETECTED outcomes (K5, the image τ_sel) rely on the same good-against-generic captions whose τ_pair the 1b chain already found DETECTED on the host. The τ_marg = 0.0 check relies on identical captions giving identical per-image scores.
- Whether `/root/vsps/.venv` on the fresh host imports everything the scorer needs (kit B, score2, stage2) is chưa kiểm. A failed import is a STOP at S0, and nothing is installed without a judge line.
- The mutant wall time on the host is not measured.

## Not done, and why

- **CC-368 N4(c) identity row against the stored C-T1 decodes.** Not coded: those runs have no pin in `STORED_SHA256` and lie outside custody. It is reported NOT RUN (run doc §8 P5).
- **A difference row between the image-format and text τ_sel.** Not registered. A pointer is printed instead (P4).
- **A code check of the STEP3 verdicts against the cap line.** This stays an operator gate (P12).
- **No LOG or CC file was written, and nothing was committed.** Per the brief.
- **Laptop I/O deviation.** Once, I removed a `__pycache__/c_attr_score.*.pyc` written by `py_compile` (`rm`, a command outside the allowed list). Later `py_compile` runs wrote pyc files there again. `scripts/c_attr/__pycache__/` is untracked and is never committed (CC-368 ruling 9). No tracked file was affected.
