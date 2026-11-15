#!/bin/bash
set -u
TREE=/root/a_perann; VENV=/root/a_perann_venv; MUT=/root/a_perann_mut; REC=/root/a_perann_records
cd "$TREE" || exit 1               # the runner never starts outside the pushed tree
test -e "$MUT" && exit 1
mkdir -p "$REC" || exit 1
python3 -m venv "$VENV" && "$VENV/bin/pip" install numpy==2.5.4 || exit 1   # numpy of the a_cert host records
J="env CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2 nice -n 19 ionice -c3 $VENV/bin/python -I -B"
{ echo "start $(date -u +%FT%TZ) tree $TREE (code only)"; "$VENV/bin/python" --version
  find . -type f -not -path '*/__pycache__/*' | sort | xargs sha256sum; } > "$REC/status.log" 2>&1
$J scripts/a_cert/a_cert_perann.py selftest --out "$REC/selftest_perann.json" 2>&1 | tee "$REC/selftest_perann.log"
echo "selftest rc ${PIPESTATUS[0]} $(date -u +%FT%TZ)" >> "$REC/status.log"
$J scripts/a_cert/a_cert_perann_mutants.py "$MUT" 2>&1 | tee "$REC/mutants_perann.log"
echo "mutants rc ${PIPESTATUS[0]} $(date -u +%FT%TZ)" >> "$REC/status.log"
cp "$MUT/mutants_result.json" "$REC/mutants_result_perann.json"
"$VENV/bin/pip" freeze > "$REC/venv_freeze.txt"
cp "$0" "$REC/run_perann.sh"
echo "DONE $(date -u +%FT%TZ)" >> "$REC/status.log"
(cd "$REC" && find . -maxdepth 1 -type f ! -name SHA256SUMS | sort | xargs sha256sum > SHA256SUMS)
