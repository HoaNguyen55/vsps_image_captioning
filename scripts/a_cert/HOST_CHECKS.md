# A-CERT host checks (H2d added 2026-11-11; CC-343 S1-S4 score-side diff added 2026-11-11)

PI rule 2026-11-11: no test runs on the laptop. Run these on the rented host, from the repo root, with the same
venv as before. Synthetic fixtures only; neither command reads a label file.

Record history in this folder. Do not overwrite any of them:
- `selftest.json`, `selftest.log`, `mutants.log`, `mutants_result.json` (66/66 checks, 27/27 killed): previous
  `a_cert.py` (df8ae932…), **stale**.
- `host_checks/*_h2d.*` (76 checks, 38/38 killed): `a_cert.py` d507bf7e… (commit 11febfc), **stale** for the S1-S4
  file. They remain the record that CC-343 (a) read.
- The new run writes `*_s14.*`.

## Host tree

Same commit as the laptop plus the uncommitted S1-S4 files (`a_cert.py`, `a_cert_mutants.py`; shas in `SHA256SUMS`).
It must also hold, unchanged:
- `manuscript/prereg/2026-11-11_a_cert/A_CERT_ANALYSIS_REG_v1_3_H2D.md` (the label check reads it; committed in 659f6c7);
- `data/coco_probe/coco80_vi.json`;
- `.session_backup/2026-10-14/r12_verify/evaluate_xm3600_predictions_v3.py` (the self-test loads v3 as `bracket.py` does).

Check before the run: `sha256sum -c scripts/a_cert/SHA256SUMS` passes for `a_cert.py` and `a_cert_mutants.py`.

## Commands (S1-S4)

```sh
set -o pipefail
PY=~/.venvs/c_stage1_lists/bin/python
# self-test: expect "selftest ok", 92 checks (76 + 16 CC-343), exit 0
OMP_NUM_THREADS=2 nice -n 15 $PY -I -B scripts/a_cert/a_cert.py selftest --out scripts/a_cert/selftest_s14.json \
  2>&1 | tee scripts/a_cert/selftest_s14.log
# mutants: scratch dir outside the repo; expect "54/54 killed" (38 + 16 CC-343), exit 0
OMP_NUM_THREADS=2 nice -n 15 $PY -I -B scripts/a_cert/a_cert_mutants.py /tmp/a_cert_mut_s14 \
  2>&1 | tee scripts/a_cert/mutants_s14.log
cp /tmp/a_cert_mut_s14/mutants_result.json scripts/a_cert/mutants_result_s14.json
```

Pull the four `*_s14.*` files into `scripts/a_cert/host_checks/`, check that `script_sha256` and `source_sha256` equal
the `a_cert.py` line of `SHA256SUMS`, add them to `host_checks/SHA256SUMS` and run `sha256sum -c` on both sums files.
Every KILLED mutant must name a failed check that is not `no_exception (...)`. A crash kill is not accepted for the
new mutants.

## New self-test checks (16)

| Check | Covers |
|---|---|
| `S1_ctl_row_by_hand`, `S1_hint_full_by_hand`, `S1_rows_in_result` | S1: per-role rows; absent controls split full / partial by hint coverage |
| `repeat_label_partial_k_of_150` | Ruling 4: "partial (k of 150 answered at the part-1 unsealing)" |
| `S2_gold_i_by_hand`, `S2_gold_ii_by_hand`, `S2_rows_in_result` | S2: gold (i) and gold (ii) recall, hallucination, share and F1; the gold (ii) label; no verdict |
| `S3_h3_all_named_by_hand`, `S3_row1_universe_all_system_named` | S3 row 1: H3 on all system-named pairs |
| `S3_D_L_by_hand`, `S3_D_L_rule_boundary`, `S3_D_L_over_completed_present` | S3 row 2: A-M1 `D_L`; only "consistent" can be read (v1.1 §6 l.210; CC-344 W1) |
| `S4_H2d_w_star_from_freeze`, `S4_H2d_margin_from_freeze`, `S4_H2d_no_abs_delta_tiebreak_for_w_star` | S4: v1.3 §5 |
| `N5_label_and_S72_ends` | N5 text; the unrounded S7.2 ends beside H1b/H1c |

The S4 checks need at least one confirmed and one unconfirmed evaluable within-family pair in the fixture (they
compare AUCs). If either class is empty, the unmutated self-test fails visibly; no mutant result is then valid.

## New mutants (16), each with the check that must kill it

| Mutant | Named check |
|---|---|
| `H2d_12_w_star_recomputed_in_score` | `S4_H2d_w_star_from_freeze` |
| `H2d_13_margin_recomputed_from_completed_counts` | `S4_H2d_margin_from_freeze` |
| `H2d_14_abs_delta_tiebreak_for_w_star` | `S4_H2d_no_abs_delta_tiebreak_for_w_star` |
| `S1_01_hint_any_overlap` | `S1_hint_full_by_hand`, `S1_rows_in_result` |
| `S1_02_ctrl_present_in_hint_split`, `S1_03_role_rows_all_expect_N` | `S1_rows_in_result` |
| `S1_04_repeat_partial_label_dropped` | `repeat_label_partial_k_of_150` |
| `S2_01_gold_ii_without_human_Y`, `S2_04_gold_ii_without_human_N` | `S2_gold_ii_by_hand` |
| `S2_02_hallucination_over_named`, `S2_03_gold_i_F1_with_gold_ii_recall` | `S2_gold_i_by_hand` |
| `S2_05_gold_ii_label_changed` | `S2_rows_in_result` |
| `S3_01_row1_on_N_u_only` | `S3_row1_universe_all_system_named` |
| `S3_02_X_without_OI_present` | `S3_h3_all_named_by_hand` |
| `S3_03_D_L_on_2.5th_percentile` | `S3_D_L_rule_boundary` |
| `S3_04_D_L_without_human_Y` | `S3_D_L_over_completed_present` |

## For the round-2 reader

`A_CERT_SCORE_S1_S4.diff` = `git diff 11febfc -- scripts/a_cert/a_cert.py scripts/a_cert/a_cert_mutants.py`.
`gate`, `freeze`, `gate_core`, `freeze_core`, every function they call, every pre-existing constant, the imports and
the module docstring are byte-identical to 11febfc. The diff touches only `h2d_rule` (N5 field), `score_core`,
`score`, `fixture`, `fixture_labels` and `_selftest_checks`, and it adds new score-side functions and four new constants.
