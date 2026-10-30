#!/bin/bash
# Paper A, A-T3 TIER 3 (the one test look; list reserved by CC-197, job by CC-203 W3-W7). M1 (machine id m3) only:
# the four tier-1 models decode the 3,232 reserved COCO val2017 ids, short_en and detailed_en, run ids at3t3_*, with
# scripts/lb/decode_hf_vlm.py (e2de1881) and the registration blocks and prompts of tiers 1-2 unchanged.
# Order (CC-203 ruling 3b): `t3gate` before `gold --set test`, before staging, before every decode cell and before
# `score --tier 3`. The pre-decode premise (PREREG §3) is checked by stage3; if it fails nothing is staged or decoded.
# Inputs on m3 (never leave M1): /root/a_t3_m3/val2017 (5,000 jpg), /root/a_t3_m3/ann/annotations_trainval2017.zip
# (113a836d), $KAR = Karpathy dataset_coco.json (2fd99922; check_pin), $NCS_DATA/a_t3_val2017_sha.json (51baa3e4).
# Outputs: gold /root/a_t3_m3/gold_test.json (stays on m3); staging $NCS_DATA/datasets/a_t3_t3 (images, sets, reg);
# decodes in /root/outputs/a_t3_t3 (own raw, ledger, EVENTS, SHA256SUMS, lock); data/results/a_t3/tier3.json once.
# Cap: a_t3.py CAP_H tier3_m3 19.69 GPU-h on this ledger (`jobcfg`); a timeout or an exhausted cap is a final CAP STOP.
# Host loss: the operator closes the open run with one ledger row (PREREG §8 F4); never moved to another host.
# Usage, inside tmux:   bash scripts/a_t3/a_t3_t3_job.sh <expected 40-hex HEAD>
set -euo pipefail
EXPECT=${1:?usage: a_t3_t3_job.sh <expected HEAD>}
MID=$(cat /root/.vsps_machine_id 2>/dev/null || true)
[ "$MID" = m3 ] || { echo "REFUSED: tier 3 runs on the m3-role machine only"; exit 1; }
[ -n "${TMUX:-}" ] || { echo "REFUSED: run inside a tmux session"; exit 1; }
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1
PY=/root/venv-lb/bin/python; X=scripts/a_t3/a_t3.py; P=scripts/pascal50s/p50.py; DEC=scripts/lb/decode_hf_vlm.py
PYV=3.10.12; NPV=2.2.6   # CC-203 W7: the interpreter and numpy that run `gold --set test` and `score --tier 3`
M3=/root/a_t3_m3; ANN=$M3/ann/annotations_trainval2017.zip; KAR=${KAR:-$M3/dataset_coco.json}; GOLD=$M3/gold_test.json
S=$NCS_DATA/datasets/a_t3_t3; REG=$S/a_t3_reg_t3.json; VALSHA=$NCS_DATA/a_t3_val2017_sha.json
V17=manuscript/prereg/2026-10-30_a_t3/val2017_ids.txt; TL=manuscript/prereg/2026-10-30_a_t3/r9/a_t3_testlist_r9_drop_all.json
T1=data/results/a_t3/tier1.json; T3J=data/results/a_t3/tier3.json
O=/root/outputs/a_t3_t3; RAW=$O/raw; LOG=$O/runs.log; L=$O/gpu_seconds_$MID.tsv; LOCK=$O/RUNNING; MARK=$O/CAP_STOP_$MID.json
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
T3G() { local o; o=$($PY $X t3gate --test-list "$TL" "$@" 2>> "$LOG") || stop "t3gate $*"; say "$o"; }
IV=$($PY -c 'import numpy,sys;print(sys.version,numpy.__version__)') || stop "interpreter"
say "INTERPRETER $PY: $IV"
case "$IV" in "$PYV "*" $NPV") ;; *) stop "interpreter is not the pre-named python $PYV numpy $NPV (CC-203 W7)" ;; esac

# ---------------------------------------------------------------- gold, premise, staging, registration (CPU, m3)
T3G
[ -s "$GOLD" ] || $PY $X gold --karpathy "$KAR" --ann "$ANN" --set test --val2017-ids "$V17" --test-list "$TL" \
  --out "$GOLD" >> "$LOG" 2>&1 || stop "gold --set test"
say "GOLD $GOLD $(sha256sum < "$GOLD" | cut -c1-64)"
T3G --gold "$GOLD"
if [ ! -s "$S/sets/a_t3_test.tsv" ]; then
  ST=$($PY $X stage3 --test-list "$TL" --gold "$GOLD" --src "$M3/val2017" --root "$S" --valsha "$VALSHA" 2>> "$LOG") \
    || stop "stage3 (PREMISE_NOT_MET or an image sha; see runs.log)"
  say "STAGED $ST"
fi
MODELS=$($PY $X models --host "$MID" --tier 3) || stop "model list"
[ -s "$REG" ] || $PY $X register --root "$S" --set test --tier 3 --models $MODELS --out "$REG" >> "$LOG" 2>&1 \
  || stop "register"
CFG=$($PY $X jobcfg --tier 3 --host "$MID" --reg "$REG") || stop "jobcfg (tier 3, $REG)"
read -r O2 CAP <<< "$CFG"
[ "$O2" = "$O" ] || stop "jobcfg out dir $O2 is not $O"
say "JOB START $MID head $EXPECT reg $(sha256sum < "$REG" | cut -c1-64) models [$MODELS] venv-lb $($PY -m pip freeze | sha256sum | cut -c1-64)"
for M in $MODELS; do   # snapshots at the A-registry pins; gated models (aya) are never fetched here (no token in a job)
  W=${SNAP_DIR:-$NCS_DATA/models/lb}/$M
  $PY $DEC --prereg "$REG" --check-snapshot "$M" --snapshot "$W" >> "$LOG" 2>&1 && continue
  [ "$M" = aya_vision_8b ] && stop "aya snapshot missing or changed at $W (fetch it by hand with the PI token per command)"
  HF_HUB_OFFLINE=0 timeout 2h $PY $DEC --prereg "$REG" --fetch "$M" --snapshot "$W" >> "$LOG" 2>&1 || stop "fetch $M"
done

# ---------------------------------------------------------------- GPU: test decodes (decode_hf_vlm resumes by slice)
run() {
  local t; t=$($PY $X left --ledger "$L" --cap-h "$CAP") || stop "cap arithmetic"
  [ "$t" -gt 60 ] || cap_stop "$CAP GPU-h cap before $1"
  T3G --gold "$GOLD"
  $PY $X datecheck --reg "$REG" >> "$LOG" 2>&1 || stop "DATE STOP (CC-184 F2) before $1"
  G; say "START $1 (left $((t / 60)) min)"
  local rc=0
  $PY $P timed --timeout "$t" --ledger "$L" --label "$1" -- \
    $PY $DEC --prereg "$REG" --run-id "$1" --snapshot "${SNAP_DIR:-$NCS_DATA/models/lb}/$3" --out-dir "$2" >> "$LOG" 2>&1 || rc=$?
  [ $rc = 0 ] && { say "OK $1"; return 0; }
  [ $rc = 124 ] && cap_stop "$CAP GPU-h cap reached during $1"
  stop "$1 rc=$rc"
}
for M in $MODELS; do   # A-registry order: internvl3_8b llava_ov_7b idefics3_8b aya_vision_8b
  for Q in short_en detailed_en; do
    R=at3t3_$M-$Q
    [ -s "$RAW/$R.preds.json" ] || run "$R" "$RAW" "$M"
  done
done

# ---------------------------------------------------------------- the one score (m3, PREREG §6; refuses if it exists)
T3G --gold "$GOLD"
$PY $X score --tier 3 --raw "$RAW" --gold "$GOLD" --tier1 "$T1" >> "$LOG" 2>&1 || stop "score --tier 3"
say "SCORED $T3J $(sha256sum < "$T3J" | cut -c1-64) gold $(sha256sum < "$GOLD" | cut -c1-64)"
finish
