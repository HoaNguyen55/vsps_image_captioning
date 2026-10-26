#!/bin/bash
# M4 Operator Job Script: DrivingVQA Feasibility Pilot P1, P3, and Conditional P2 (CC-104 F1-F12; REVIEW_KEN_BATCH8 W1-W8).
# Runs EXCLUSIVELY on M4 (never on M3).
# Stage A: P1 (cap 4500s = 1.25 GPU-h) then P3 (cap 2700s = 0.75 GPU-h) -> score.py -> decide.py (--stage A).
# Stage B: P2 (cap 4500s = 1.25 GPU-h) runs ONLY if decide_pilot.json reports status=="COMPLETE" and P1_verdict=="GO".
# Total hard GPU cap: 3.25 GPU-h (11,700s). Any timeout (rc=124) records TIMEOUT in gpu_seconds.tsv and INCOMPLETE in decide_pilot.json.
# Usage: bash scripts/ken_dvqa_pilot/job.sh <expected_40_hex_git_HEAD>
set -u

EXPECT=${1:-}
cd /root/vsps || exit 1
export PYTHONHASHSEED=0
export PYTHONDONTWRITEBYTECODE=1
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=${VSPS_MACHINE_ID:-$(hostname)}

if [ -d "scripts/ken_dvqa_pilot" ]; then
  D="scripts/ken_dvqa_pilot"
elif [ -d "scripts/ken_dvqa_pilot_v2" ]; then
  D="scripts/ken_dvqa_pilot_v2"
else
  D="manuscript/ken/ken_dvqa_pilot_v2"
fi

LB=/root/venv-lb/bin/python
DVQA_DIR=/root/dvqa_pilot
IMG_SHA_TSV=manuscript/ken/dvqa_dev1000_image_sha256.tsv
O=.session_backup/2026-10-26/dvqa_pilot
R=$O/runs
LOG=$O/logs
LED=$O/ledger.jsonl
GPU_TSV=$O/gpu_seconds.tsv
DECIDE_OUT=$O/decide_pilot.json
SUMS=$D/SHA256SUMS

HUB=/root/.cache/huggingface/hub
Q25=$HUB/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/cc594898137f460bfe9f0759e9844b3ce807cfb5
IV3=$HUB/models--OpenGVLab--InternVL3-8B-hf/snapshots/259a3b64a14623c0ec91a045cb43f7c5af5fa6af
VENV_PIN_PREFIX="685ffe2a"

P1_CAP=4500
P3_CAP=2700
P2_CAP=4500

mkdir -p "$R" "$LOG"
: > "$GPU_TSV"

ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*"; }
stop() { say "JOB STOP: $*"; exit 1; }

# ---------------------------------------------------------------- 1. CPU Preflight & Host Hygiene BEFORE any GPU timer (CC-104 F5, F8, F10; W3, W4)
[ "$VSPS_MACHINE_ID" = "m3" ] || [ "$VSPS_MACHINE_ID" = "M3" ] && stop "Refused: DrivingVQA pilot must run on M4, never on M3"
! ls /root/outputs/claude_ops/m3_rebuild_*.log >/dev/null 2>&1 || stop "Refused: M3 rebuild marker detected on host"
ls /root/outputs/claude_ops/m4_rebuild_*.log >/dev/null 2>&1 || stop "Refused: M4 rebuild marker (/root/outputs/claude_ops/m4_rebuild_*.log) missing"
[ -n "$EXPECT" ] && [ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD does not match expected commit $EXPECT"
git diff --quiet HEAD -- || stop "Tracked files differ from HEAD"
(cd "$D" && sha256sum --quiet -c SHA256SUMS) || stop "$SUMS verification failed"

FREEZE_SHA=$(/root/venv-lb/bin/pip freeze | sha256sum | cut -c1-64)
case "$FREEZE_SHA" in
  ${VENV_PIN_PREFIX}*) ;;
  *) stop "venv-lb freeze sha256 ($FREEZE_SHA) does not start with $VENV_PIN_PREFIX" ;;
esac

for f in build_splits_and_stats stage_images host_check decode score decide; do
  $LB -B "$D/$f.py" --selftest >> "$LOG/selftest.log" 2>&1 || stop "$f.py --selftest failed"
done

$LB -B "$D/host_check.py" \
  --dvqa-dir "$DVQA_DIR" \
  --scan-root /root \
  --image-sha-tsv "$IMG_SHA_TSV" \
  --require-m4-marker \
  --out "$O/host_check.json" >> "$LOG/host_check.log" 2>&1 \
  || stop "M4 host_check failed (F5 / W3 / W4)"

say "JOB START head=$EXPECT venv=$FREEZE_SHA"

run_capped_block() {
  # run_capped_block STAGE CAP_SECONDS
  local stage=$1
  local cap=$2
  local t_start t_now elapsed rem rc
  t_start=$(date +%s)

  for m_pair in "qwen25vl_7b:$Q25" "internvl3_8b:$IV3"; do
    local model=${m_pair%%:*}
    local snap=${m_pair#*:}
    t_now=$(date +%s)
    elapsed=$((t_now - t_start))
    rem=$((cap - elapsed))
    if [ "$rem" -le 5 ]; then
      echo -e "${stage}_${model}\t${elapsed}\tTIMEOUT" >> "$GPU_TSV"
      say "CAP STOP before ${stage}_${model} (cap ${cap}s exhausted)"
      $LB -B "$D/score.py" --runs-dir "$R" --dvqa-dir "$DVQA_DIR" --ledger "$LED" >> "$LOG/score.log" 2>&1 || true
      $LB -B "$D/decide.py" --ledger "$LED" --gpu-seconds "$GPU_TSV" --stage A --out "$DECIDE_OUT" >> "$LOG/decide.log" 2>&1 || true
      stop "${stage} exceeded hard cap ${cap}s -> INCOMPLETE"
    fi
    say "START ${stage}_${model} (remaining cap ${rem}s)"
    local step_t0
    step_t0=$(date +%s)
    timeout "${rem}s" $LB -B "$D/decode.py" --stage "$stage" --model "$model" --snapshot "$snap" --dvqa-dir "$DVQA_DIR" --out-dir "$R" \
      >> "$LOG/${stage}_${model}.log" 2>&1
    rc=$?
    local step_sec=$(( $(date +%s) - step_t0 ))
    if [ "$rc" -eq 124 ]; then
      echo -e "${stage}_${model}\t${step_sec}\tTIMEOUT" >> "$GPU_TSV"
      say "TIMEOUT ${stage}_${model} after ${step_sec}s"
      $LB -B "$D/score.py" --runs-dir "$R" --dvqa-dir "$DVQA_DIR" --ledger "$LED" >> "$LOG/score.log" 2>&1 || true
      $LB -B "$D/decide.py" --ledger "$LED" --gpu-seconds "$GPU_TSV" --stage A --out "$DECIDE_OUT" >> "$LOG/decide.log" 2>&1 || true
      stop "${stage}_${model} hit timeout cap -> INCOMPLETE"
    elif [ "$rc" -ne 0 ]; then
      echo -e "${stage}_${model}\t${step_sec}\tFAIL" >> "$GPU_TSV"
      $LB -B "$D/score.py" --runs-dir "$R" --dvqa-dir "$DVQA_DIR" --ledger "$LED" >> "$LOG/score.log" 2>&1 || true
      $LB -B "$D/decide.py" --ledger "$LED" --gpu-seconds "$GPU_TSV" --stage A --out "$DECIDE_OUT" >> "$LOG/decide.log" 2>&1 || true
      stop "${stage}_${model} failed with rc=$rc"
    fi
    echo -e "${stage}_${model}\t${step_sec}\tOK" >> "$GPU_TSV"
    say "OK ${stage}_${model} (${step_sec}s)"
  done
}

# ---------------------------------------------------------------- 2. Stage A: P1 (1.25 GPU-h cap) then P3 (0.75 GPU-h cap)
run_capped_block P1 "$P1_CAP"
run_capped_block P3 "$P3_CAP"

$LB -B "$D/score.py" --runs-dir "$R" --dvqa-dir "$DVQA_DIR" --ledger "$LED" >> "$LOG/score.log" 2>&1 \
  || stop "Stage A score.py failed"
$LB -B "$D/decide.py" --ledger "$LED" --gpu-seconds "$GPU_TSV" --stage A --out "$DECIDE_OUT" >> "$LOG/decide.log" 2>&1 \
  || stop "Stage A decide.py failed"

STATUS=$($LB -B -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('status',''))" "$DECIDE_OUT")
P1_VERDICT=$($LB -B -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('P1_verdict',''))" "$DECIDE_OUT")
P3_VERDICT=$($LB -B -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('P3_verdict',''))" "$DECIDE_OUT")

say "STAGE A DONE: status=$STATUS P1_verdict=$P1_VERDICT P3_verdict=$P3_VERDICT"
if [ "$STATUS" != "COMPLETE" ]; then
  stop "Stage A ended with status=$STATUS (no verdict)"
fi

# ---------------------------------------------------------------- 3. Stage B: P2 (1.25 GPU-h cap), ONLY if P1_verdict == GO
if [ "$P1_VERDICT" = "GO" ]; then
  say "P1_verdict is GO -> starting Stage B (P2, cap ${P2_CAP}s)"
  run_capped_block P2 "$P2_CAP"
  $LB -B "$D/score.py" --runs-dir "$R" --dvqa-dir "$DVQA_DIR" --ledger "$LED" >> "$LOG/score.log" 2>&1 \
    || stop "Stage B score.py failed"
  $LB -B "$D/decide.py" --ledger "$LED" --gpu-seconds "$GPU_TSV" --stage B --out "$DECIDE_OUT" >> "$LOG/decide.log" 2>&1 \
    || stop "Stage B decide.py failed"
  P2_VERDICT=$($LB -B -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('P2_verdict',''))" "$DECIDE_OUT")
  say "STAGE B DONE: P2_verdict=$P2_VERDICT"
else
  say "P1_verdict is $P1_VERDICT -> Stage B (P2) cancelled with 0 GPU spent"
fi

(cd "$O" && sha256sum host_check.json gpu_seconds.tsv ledger.jsonl decide_pilot.json > SHA256SUMS)
say "PILOT JOB COMPLETE"
