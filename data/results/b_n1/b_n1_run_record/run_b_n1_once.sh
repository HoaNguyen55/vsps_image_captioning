#!/bin/bash
# B-N1 registered run (prereg 2026-10-19_b_n1_vi_leaderboard; scorer v2 with the R14 pre-check, judge CC-039/CP-039 (2)):
# freeze the 16 mirrored decodes with their sidecars, then run the committed scorer ONCE. A second run is refused.
set -euo pipefail
REPO=/mnt/d/vsps_image_captioning
RUN=$REPO/.session_backup/2026-10-20/b_n1_run
SRC=$REPO/.session_backup/machines/O-2308423/root/outputs/2026-10-19_b_n1_vi_leaderboard
VENV=${B_N1_VENV:?set B_N1_VENV to the venv of the gate (b_n1_gate.json env: python 3.12.3, numpy 2.5.4)}
OUT=data/results/b_n1/b_n1_run.json
cd "$REPO"
[ -e "$RUN/RAN_ONCE" ] && { echo "REFUSED: already ran once" >&2; exit 3; }
[ -e "$OUT" ] && { echo "REFUSED: $OUT exists" >&2; exit 3; }
[ -e "$RUN/outputs" ] && { echo "REFUSED: $RUN/outputs exists; inspect it first" >&2; exit 3; }
LOG=$RUN/run.log; : > "$LOG"
die() { echo "ABORT: $*" | tee -a "$LOG" >&2; exit 2; }
for f in scripts/lb/score_b_n1.py manuscript/prereg/2026-10-19_b_n1_record/b_n1_gate.json; do
  git ls-files --error-unmatch "$f" > /dev/null 2>&1 || die "not committed: $f"
  git diff --quiet HEAD -- "$f" || die "differs from HEAD: $f"
done
mkdir "$RUN/outputs"
n=0
for p in "$SRC"/*.preds.json; do
  side="$p.sha256"; [ -f "$side" ] || die "no sidecar for ${p##*/}"
  [ "$(cut -c1-64 "$side")" = "$(sha256sum "$p" | cut -c1-64)" ] || die "sidecar mismatch ${p##*/}"
  cp "$p" "$side" "$RUN/outputs/"
  cmp -s "$p" "$RUN/outputs/${p##*/}" || die "copy differs ${p##*/}"
  echo "OK $(cut -c1-64 "$side") ${p##*/}" >> "$LOG"; n=$((n + 1))
done
[ "$n" -eq 16 ] || die "expected 16 decodes, found $n"
mkdir -p "${OUT%/*}"
CMD=("$VENV/bin/python" -E -P scripts/lb/score_b_n1.py run "$OUT"
     --gate manuscript/prereg/2026-10-19_b_n1_record/b_n1_gate.json --outputs "$RUN/outputs")
echo "CMD score_b_n1.py run $OUT --gate manuscript/prereg/2026-10-19_b_n1_record/b_n1_gate.json --outputs <run>/outputs" >> "$LOG"
echo "HEAD $(git rev-parse HEAD)" >> "$LOG"
echo "ENV $("$VENV/bin/python" -c 'import sys, numpy; print("python", sys.version.split()[0], "numpy", numpy.__version__)')" >> "$LOG"
touch "$RUN/RAN_ONCE"
T0=$(date -u +%FT%T.%3NZ)
set +e
env -i HOME="$HOME" LANG=C.UTF-8 JAVA_HOME="$HOME/jdk21" PATH="$HOME/jdk21/bin:/usr/bin:/bin" NCS_DATA="$REPO/data" \
    VNCORENLP_DIR="$REPO/.session_backup/machines/n2/ncs-data/vncorenlp" OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 \
    MKL_NUM_THREADS=2 nice -n 15 "${CMD[@]}" > "$RUN/run.stdout" 2> "$RUN/run.stderr"
RC=$?
set -e
echo "RUN rc=$RC start=$T0 end=$(date -u +%FT%T.%3NZ)" >> "$LOG"
[ $RC -eq 0 ] || die "scorer exited rc=$RC; see run.stderr. Report to the judge before any retry"
echo "DONE $(sha256sum "$OUT" | cut -c1-64)  $OUT" | tee -a "$LOG"
