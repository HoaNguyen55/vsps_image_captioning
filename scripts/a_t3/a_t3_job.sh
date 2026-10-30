#!/bin/bash
# Paper A, A-T3 (TIER 1, DEV-EXPLORE ONLY): the A-T3 model set decodes D1 = 1,000 COCO train2017 images (Karpathy
# restval minus val2017 minus every exclusion list), short_en and detailed_en, with scripts/lb/decode_hf_vlm.py
# unchanged. M2 (machine id m4) runs the m4 families; M1 (machine id m3) runs aya_vision_8b only, after C-T1 has ended
# and been mirrored (CC-183 r10, PI default Q7). No val2017 image, id or annotation is ever on M2 (guard, W8).
# No scoring here: preds go to the laptop, scored once by `a_t3.py score --tier 1` (PREREG §5-§6).
# Cap (PREREG §8): 6 GPU-h on m4, 2 GPU-h on m3 inside a_t3.py CAP_GPU_H; a timeout or an exhausted cap is a final
# CAP STOP. Host loss: before any restart the operator closes the open run with one ledger row (PREREG §8, CC-184 F4).
# Staged before (operator): $NCS_DATA/datasets/a_t3/{images,sets} from `a_t3.py stage --set D1` (after the D1 premise
# held), $NCS_DATA/datasets/a_t3/a_t3_reg.json from `a_t3.py register`, and the m3-made val2017 sha list at $VALSHA.
# Usage, inside tmux:   bash scripts/a_t3/a_t3_job.sh <expected 40-hex HEAD>
set -euo pipefail
EXPECT=${1:?usage: a_t3_job.sh <expected HEAD>}
MID=$(cat /root/.vsps_machine_id 2>/dev/null || true)
case "$MID" in m4) CAP=6 ;; m3) CAP=2 ;; *) echo "REFUSED: machine id is not m3/m4"; exit 1 ;; esac
[ -n "${TMUX:-}" ] || { echo "REFUSED: run inside a tmux session"; exit 1; }
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1
PY=/root/venv-lb/bin/python; X=scripts/a_t3/a_t3.py; P=scripts/pascal50s/p50.py; DEC=scripts/lb/decode_hf_vlm.py
S=$NCS_DATA/datasets/a_t3; REG=$S/a_t3_reg.json; VALSHA=$NCS_DATA/a_t3_val2017_sha.json
V17=manuscript/prereg/2026-10-30_a_t3/val2017_ids.txt
O=/root/outputs/a_t3; RAW=$O/raw; LOG=$O/runs.log; L=$O/gpu_seconds_$MID.tsv; LOCK=$O/RUNNING; MARK=$O/CAP_STOP_$MID.json
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
  say "BLOCK DONE $MID gpu_h $(awk -F'\t' '{s += $2} END {printf "%.2f", s / 3600}' "$L")"; exit 0; }
cap_stop() { [ -e "$MARK" ] || printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > "$MARK"; say "CAP STOP $1"; finish; }

# ---------------------------------------------------------------- preflight (CPU)
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
for D in a_t3 a_t1 pascal50s; do sha256sum --quiet -c scripts/$D/SHA256SUMS || stop "scripts/$D/SHA256SUMS"; done
sha256sum --quiet -c manuscript/prereg/2026-10-30_a_t3/SHA256SUMS || stop "prereg SHA256SUMS"
$PY $P imports >> "$LOG" 2>&1 || stop "import check"
$PY $X --selftest >> "$LOG" 2>&1 || stop "a_t3 selftest"
$PY $X registry --check >> "$LOG" 2>&1 || stop "A registry differs from its sources"
G() { $PY $X guard --head "$EXPECT" --val2017-ids "$V17" --valsha "$VALSHA" >> "$LOG" 2>&1 || stop "guard (W8)"; }
G
[ -s "$REG" ] || stop "runtime registration not staged"
MODELS=$($PY $X models --host "$MID") || stop "model list"
say "JOB START $MID head $EXPECT reg $(sha256sum < "$REG" | cut -c1-64) models [$MODELS] venv-lb $($PY -m pip freeze | sha256sum | cut -c1-64)"
for M in $MODELS; do   # snapshots at the A-registry pins; gated models (aya) are never fetched here (no token in a job)
  W=${SNAP_DIR:-$NCS_DATA/models/lb}/$M
  $PY $DEC --prereg "$REG" --check-snapshot "$M" --snapshot "$W" >> "$LOG" 2>&1 && continue
  [ "$M" = aya_vision_8b ] && stop "aya snapshot missing or changed at $W (fetch it by hand with the PI token per command)"
  HF_HUB_OFFLINE=0 timeout 2h $PY $DEC --prereg "$REG" --fetch "$M" --snapshot "$W" >> "$LOG" 2>&1 || stop "fetch $M"
done

# ---------------------------------------------------------------- GPU: D1 decodes (decode_hf_vlm resumes by slice)
run() {
  local t; t=$($PY $X left --ledger "$L" --cap-h "$CAP") || stop "cap arithmetic"
  [ "$t" -gt 60 ] || cap_stop "$CAP GPU-h cap before $1"
  $PY $X datecheck --reg "$REG" >> "$LOG" 2>&1 || stop "DATE STOP (CC-184 F2) before $1"
  G; say "START $1 (left $((t / 60)) min)"
  local rc=0
  $PY $P timed --timeout "$t" --ledger "$L" --label "$1" -- \
    $PY $DEC --prereg "$REG" --run-id "$1" --snapshot "${SNAP_DIR:-$NCS_DATA/models/lb}/$3" --out-dir "$2" >> "$LOG" 2>&1 || rc=$?
  [ $rc = 0 ] && { say "OK $1"; return 0; }
  [ $rc = 124 ] && cap_stop "$CAP GPU-h cap reached during $1"
  stop "$1 rc=$rc"
}
for M in $MODELS; do   # A-registry order: internvl3_8b llava_ov_7b idefics3_8b gemma3_4b (m4); aya_vision_8b (m3)
  for Q in short_en detailed_en; do
    R=at3t1_$M-$Q
    [ -s "$RAW/$R.preds.json" ] || run "$R" "$RAW" "$M"
  done
done
finish
