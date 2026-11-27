#!/usr/bin/env bash
# B-D1 S0 checks, synthetic fixtures only (prereg v3 §6 S0). Run from anywhere inside the tree:
#   scripts/b_d1/run_tests.sh [PYTHON] [--env WHEEL_DIR]
# 1. test_b_d1.py (all checks), 2. mutants_b_d1.py (all killed), 3. with --env: the toy environment record
#    (b_fecert.env_record + env_check unchanged, and family.f3 on the registered toy strings; no data).
# NCS_DATA points to an empty temp dir for 1 and 2, so no data file can be read. Exit 0 only if every part passes.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
PY=${1:-python3}
export CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2
EMPTY=$(mktemp -d)
cd "$ROOT"
NCS_DATA=$EMPTY $PY -X utf8 -I -B scripts/b_d1/test_b_d1.py; t=$?
NCS_DATA=$EMPTY $PY -X utf8 -I -B scripts/b_d1/mutants_b_d1.py --jobs "${JOBS:-2}"; m=$?
e=0
if [ "${2:-}" = "--env" ]; then
  WH=$3
  $PY -X utf8 -I -B scripts/b_d1/env_toy.py "$WH"; e=$?  # CC-506e1: a file, not stdin (closure check)
fi
rm -rf "$EMPTY"
echo "run_tests: selftest rc=$t mutants rc=$m env rc=$e"
[ "$t" -eq 0 ] && [ "$m" -eq 0 ] && [ "$e" -eq 0 ]
