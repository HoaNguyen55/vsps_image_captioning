#!/bin/bash
# A-N2 registered run (prereg 2026-10-19_a_n2_lvlm_gold_ladder; scorer committed in 269046e; judge CC-039/CP-039):
# freeze the 32 mirrored decodes with their sidecars, then run the committed scorer ONCE. Needs G2-B's results
# committed at HEAD (reading R7). A second run is refused.
set -euo pipefail
REPO=/mnt/d/vsps_image_captioning
RUN=$REPO/.session_backup/2026-10-20/a_n2_run
SRC=$REPO/.session_backup/machines/O-2308423/root/outputs/2026-10-19_a_n2_lvlm_gold_ladder
OUT=data/results/a_n2/a_n2_run.json
cd "$REPO"
[ -e "$RUN/RAN_ONCE" ] && { echo "REFUSED: already ran once" >&2; exit 3; }
[ -e "$OUT" ] && { echo "REFUSED: $OUT exists" >&2; exit 3; }
[ -e "$RUN/outputs" ] && { echo "REFUSED: $RUN/outputs exists; inspect it first" >&2; exit 3; }
LOG=$RUN/run.log; : > "$LOG"
die() { echo "ABORT: $*" | tee -a "$LOG" >&2; exit 2; }
for f in scripts/lb/score_a_n2.py manuscript/prereg/2026-10-19_a_n2_record/a_n2_gate.json data/results/g2b/g2b_score.json; do
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
[ "$n" -eq 32 ] || die "expected 32 decodes, found $n"
mkdir -p "${OUT%/*}"
CMD=(python3 -E -P scripts/lb/score_a_n2.py run "$OUT" --gate manuscript/prereg/2026-10-19_a_n2_record/a_n2_gate.json
     --outputs "$RUN/outputs" --g2b-results data/results/g2b/g2b_score.json --g2b-outputs .session_backup/2026-10-20/g2b_score/outputs)
echo "CMD ${CMD[*]}" >> "$LOG"; echo "HEAD $(git rev-parse HEAD)" >> "$LOG"
touch "$RUN/RAN_ONCE"
T0=$(date -u +%FT%T.%3NZ)
set +e
env -i HOME="$HOME" PATH=/usr/bin:/bin LANG=C.UTF-8 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 \
    nice -n 15 "${CMD[@]}" > "$RUN/run.stdout" 2> "$RUN/run.stderr"
RC=$?
set -e
echo "RUN rc=$RC start=$T0 end=$(date -u +%FT%T.%3NZ)" >> "$LOG"
[ $RC -eq 0 ] || die "scorer exited rc=$RC; see run.stderr. Report to the judge before any retry"
echo "DONE $(sha256sum "$OUT" | cut -c1-64)  $OUT" | tee -a "$LOG"
