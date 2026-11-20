#!/bin/bash
# Host records for scripts/a_e3_e6split (REG-1119a E6 split): synthetic self-test, then the 14 named mutants.
# RENTED HOST ONLY (PI-1111j; CC-366 4(e) names no laptop exception for tests). Code-only tree: the 43 paths of
# scripts/a_cert/host_checks_e3code/status.log plus scripts/a_e3_e6split/{a_e6_split.py,test_a_e6_split.py}.
# Nothing from data/results/, no label, key, assignment or Open Images file. CPU only.
# Usage (from the tree root): bash scripts/a_e3_e6split/run_a_e6_split_tests.sh <out dir outside the tree> <python>
# Expected: "selftest rc 0" with 20 ok and "selftest ok"; "mutants rc 0" with "14/14 killed".
O=${1:?out dir}; PY=${2:?python (3.12.3, numpy 2.5.4, as the e3 host venv)}
R="env CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2 nice -n 19 ionice -c3"
T=scripts/a_e3_e6split
test -e "$T/a_e6_split.py" || { echo "run from the tree root"; exit 1; }
mkdir -p "$O"
{ echo "start $(date -u +%FT%TZ) tree $PWD (code only) python $($PY -V 2>&1)"
  find . -type f -not -path '*/__pycache__/*' | sort | xargs sha256sum; } > "$O/status.log"
$R "$PY" -I -B "$T/test_a_e6_split.py" selftest --out "$O/selftest_e6split.json" > "$O/selftest_e6split.log" 2>&1
echo "selftest rc $? $(date -u +%FT%TZ)" >> "$O/status.log"
$R "$PY" -I -B "$T/test_a_e6_split.py" mutants --out "$O/mutants_e6split.json" > "$O/mutants_e6split.log" 2>&1
echo "mutants rc $? $(date -u +%FT%TZ)" >> "$O/status.log"
"$PY" -m pip freeze > "$O/venv_freeze.txt" 2>&1
echo "DONE $(date -u +%FT%TZ)" >> "$O/status.log"
cd "$O" && sha256sum status.log selftest_e6split.log selftest_e6split.json mutants_e6split.log mutants_e6split.json \
  venv_freeze.txt > SHA256SUMS
tail -3 status.log; tail -1 mutants_e6split.log
