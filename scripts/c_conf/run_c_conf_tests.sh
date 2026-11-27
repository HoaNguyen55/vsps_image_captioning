#!/bin/bash
# C-CONF self-tests and mutants, in one run, on a rented host only (PI rule of 2026-11-11: no test on the laptop).
# Synthetic fixtures only: no study data, no token, no OV-test byte. Run from the checkout after the push, inside tmux:
#     bash scripts/c_conf/run_c_conf_tests.sh [/root]
# Checks the pushed files against scripts/c_conf/SHA256SUMS, then runs the five tests (each self-test, then its
# mutants) with the interpreter each one names, prints one rc line per test, and exits 1 if any test fails.
# Logs: <root>/c_conf_tests/<UTC stamp>/<test>.log (counts, rc and assertion text only; no caption exists here).
set -uo pipefail
R=${1:-/root}
cd "$(dirname "$0")/../.." || exit 2
PY=$R/vsps/.venv/bin/python; LB=$R/venv-lb/bin/python   # venv-lb: the decoder's interpreter (c_conf.py imports)
OUT=$R/c_conf_tests/$(date -u +%Y%m%dT%H%M%SZ); mkdir -p "$OUT"
(cd scripts/c_conf && sha256sum --quiet -c SHA256SUMS) || { echo "SUMS FAIL: scripts/c_conf/SHA256SUMS"; exit 1; }
fail=0
for t in "$PY test_c_conf_lists.py" "$PY test_c_conf_score.py" "$LB test_c_conf.py" "$LB test_c_conf_arms.py" \
         "$PY test_c_conf_job.py"; do
  set -- $t
  rc=0; env -u PYTHONPATH "$1" -I -B "scripts/c_conf/$2" > "$OUT/$2.log" 2>&1 || rc=$?
  echo "$(date -u +%FT%TZ) $2 rc=$rc $(grep -E '^mutants:' "$OUT/$2.log" | tail -1)"
  [ $rc = 0 ] || fail=1
done
echo "$(date -u +%FT%TZ) ALL $([ $fail = 0 ] && echo PASS || echo FAIL); logs $OUT"
exit $fail
