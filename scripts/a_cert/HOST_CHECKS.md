# A-CERT host checks (H2d added 2026-11-11)

PI rule 2026-11-11: no test runs on the laptop. Run these on the rented host, from the repo root, with the same
venv as before. Synthetic fixtures only; neither command reads a label file.

The earlier `selftest.json`, `selftest.log`, `mutants.log` and `mutants_result.json` in this folder (66/66 checks,
27/27 killed) were made with the previous `a_cert.py` (df8ae932…) and are **stale** for the current file. They are
kept unchanged; do not overwrite them. The new run writes `*_h2d.*` files.

The self-test reads `manuscript/prereg/2026-11-11_a_cert/A_CERT_ANALYSIS_REG_v1_3_H2D.md` (label check); the host
tree must hold it (committed in 659f6c7).

```sh
set -o pipefail
PY=~/.venvs/c_stage1_lists/bin/python
# self-test: expect "selftest ok", 76 checks (66 + 10 H2d), exit 0
OMP_NUM_THREADS=2 nice -n 15 $PY -I -B scripts/a_cert/a_cert.py selftest --out scripts/a_cert/selftest_h2d.json \
  2>&1 | tee scripts/a_cert/selftest_h2d.log
# mutants: scratch dir outside the repo; expect "38/38 killed" (27 + 11 H2d), exit 0
OMP_NUM_THREADS=2 nice -n 15 $PY -I -B scripts/a_cert/a_cert_mutants.py /tmp/a_cert_mut_h2d \
  2>&1 | tee scripts/a_cert/mutants_h2d.log
cp /tmp/a_cert_mut_h2d/mutants_result.json scripts/a_cert/mutants_result_h2d.json
```

New self-test checks: `H2d_stream_rows_1_2000_of_boot_weights_rng_20261111`, `H2d_point_y_is_H2a_truth_on_30_pairs`,
`H2d_label_verbatim_v1_3`, `H2d_PASS_at_D_0.10`, `H2d_FAIL_at_D_0.08_below_SESOI`,
`H2d_FAIL_when_2.5th_percentile_not_above_0`, `H2d_NOT_EVALUABLE_n1_4`, `H2d_ties_half_NI_last_and_tied_exclusions`,
`H2d_w_star_0_is_a_fault`, `H2d_AUC_equals_brute_force_40`; `result_labels_present` now expects seven labels.

New mutants: `H2d_01_SESOI_changed` … `H2d_11_excluded_pairs_kept` in `a_cert_mutants.py`.
After the run, add the new logs to `SHA256SUMS`.
