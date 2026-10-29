#!/bin/bash
# Paper A, A-T1 (TIER 1, DEV-EXPLORE ONLY) on M2 (machine id m4): the frozen A-N2 LVLM set (7 kept models, P50's
# kept order) decodes D1 = 1,000 ADE20K TRAINING images, short_en and detailed_en, with scripts/lb/decode_hf_vlm.py
# unchanged. No ADE20K validation file is ever on M2 (guard). No scoring here: preds are pulled to the laptop and
# scored once by `a_t1.py score` (prereg manuscript/prereg/2026-10-30_a_t1/PREREG.md).
# Cap: 10 GPU-h over the decodes (p50.timed ledger); a run gets the time left as its timeout; a timeout or an
# exhausted cap is a final CAP STOP (models already done in both prompts are scored; < 3 = NOT_EVALUABLE).
# Staged before (operator, from the laptop `a_t1.py stage`): $NCS_DATA/datasets/a_t1/{images,sets} (D1 only, staged only after the D1 premise held)
# and $NCS_DATA/datasets/a_t1/a_t1_reg.json (from `a_t1.py register`). Usage, inside tmux on M2:
#   bash scripts/a_t1/a_t1_job.sh <expected 40-hex HEAD>
set -euo pipefail
EXPECT=${1:?usage: a_t1_job.sh <expected HEAD>}
[ "$(cat /root/.vsps_machine_id 2>/dev/null)" = m4 ] || { echo "REFUSED: /root/.vsps_machine_id is not m4"; exit 1; }
[ -n "${TMUX:-}" ] || { echo "REFUSED: run inside a tmux session"; exit 1; }
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1
PY=/root/venv-lb/bin/python; X=scripts/a_t1/a_t1.py; P=scripts/pascal50s/p50.py; DEC=scripts/lb/decode_hf_vlm.py
S=$NCS_DATA/datasets/a_t1; REG=$S/a_t1_reg.json
O=/root/outputs/a_t1; RAW=$O/raw; LOG=$O/runs.log; L=$O/gpu_seconds.tsv; LOCK=$O/RUNNING; MARK=$O/CAP_STOP.json
mkdir -p "$O" "$RAW"; touch "$L"
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*" | tee -a "$O/EVENTS"; }
stop() { say "JOB STOP $*"; exit 1; }
OTHER=$(ls /root/outputs/*/RUNNING 2>/dev/null || true)
[ -z "$OTHER" ] || { echo "REFUSED: a lock exists: $OTHER"; exit 1; }
( set -o noclobber; echo "$0 $(ts)" > "$LOCK" ) || { echo "REFUSED: $LOCK exists"; exit 1; }
trap 'rm -f "$LOCK"' EXIT
finish() {
  (cd "$O" && find . -type f ! -name 'SHA256SUMS*' ! -name RUNNING ! -name '*.partial*' | sort | xargs sha256sum) \
    > "$O/SHA256SUMS"
  say "BLOCK DONE gpu_h $(awk -F'\t' '{s += $2} END {printf "%.2f", s / 3600}' "$L")"; exit 0; }
cap_stop() { [ -e "$MARK" ] || printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > "$MARK"; say "CAP STOP $1"; finish; }

# ---------------------------------------------------------------- preflight (CPU)
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
sha256sum --quiet -c scripts/a_t1/SHA256SUMS || stop "scripts/a_t1/SHA256SUMS does not verify"
sha256sum --quiet -c scripts/pascal50s/SHA256SUMS || stop "scripts/pascal50s/SHA256SUMS does not verify"
$PY $P imports >> "$LOG" 2>&1 || stop "import check"
$PY $X --selftest >> "$LOG" 2>&1 || stop "a_t1 selftest"
G() { $PY $X guard --head "$EXPECT" >> "$LOG" 2>&1 || stop "guard (m4, idle GPU, HEAD, no ADE_val or test-side set)"; }
G
[ -s "$REG" ] || stop "runtime registration not staged"
say "JOB START head $EXPECT reg $(sha256sum < "$REG" | cut -c1-64) venv-lb $($PY -m pip freeze | sha256sum | cut -c1-64)"
for M in $($PY $DEC --prereg "$REG" --models); do   # snapshots at their A-N2 pins (network, not GPU time)
  W=$NCS_DATA/models/lb/$M
  $PY $DEC --prereg "$REG" --check-snapshot "$M" --snapshot "$W" >> "$LOG" 2>&1 && continue
  HF_HUB_OFFLINE=0 timeout 2h $PY $DEC --prereg "$REG" --fetch "$M" --snapshot "$W" >> "$LOG" 2>&1 || stop "fetch $M"
done

# ---------------------------------------------------------------- GPU: D1 decodes (no smoke; decode_hf_vlm resumes by slice)
run() {  # run RUN_ID OUTDIR MODEL: one decode under the time left; ledger row via p50.timed
  local t; t=$($PY $X left --ledger "$L") || stop "cap arithmetic"
  [ "$t" -gt 60 ] || cap_stop "10 GPU-h cap before $1"
  G; say "START $1 (left $((t / 60)) min)"
  local rc=0
  $PY $P timed --timeout "$t" --ledger "$L" --label "$1" -- \
    $PY $DEC --prereg "$REG" --run-id "$1" --snapshot "$NCS_DATA/models/lb/$3" --out-dir "$2" >> "$LOG" 2>&1 || rc=$?
  [ $rc = 0 ] && { say "OK $1"; return 0; }
  [ $rc = 124 ] && cap_stop "10 GPU-h cap reached during $1"
  stop "$1 rc=$rc"
}
for M in qwen3vl_8b qwen25vl_7b qwen25vl_3b smolvlm2_2b llava15_7b internvl3_8b llava_ov_7b; do   # P50's kept order
  for Q in short_en detailed_en; do
    R=at1_$M-$Q
    [ -s "$RAW/$R.preds.json" ] || run "$R" "$RAW" "$M"
  done
done
finish
