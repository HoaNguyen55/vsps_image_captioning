#!/bin/bash
# M4 Operator Job Script: DrivingVQA Feasibility Pilot P1, P3, and Conditional P2 (CC-104 F1-F12; CC-104a W1-W8).
# Runs EXCLUSIVELY on M4 (never on M3).
# v4 (PI-1026c, CC-108 W8): P1, P2 and P3 all run on the 3,142 train ids (drivingvqa_train3142_ids.tsv). Exploratory.
# Caps scale CC-104 F3's estimates to n = 3,142, each >= 25% over its estimate, total 45,360 s = 12.6 GPU-h:
#   P1 est 0.9 h x 3.142 = 2.83 h -> cap 14040 s (3.90 h); P3 est 0.6 h x 6.284 = 3.77 h -> cap 17100 s (4.75 h);
#   P2 est 1.0 h x 3.142 = 3.14 h -> cap 14220 s (3.95 h).
# Stage A: P1 (cap 14040s = 3.90 GPU-h) then P3 (cap 17100s = 4.75 GPU-h) -> score.py -> decide.py (--stage A -> decide_pilot.json).
# Stage B: P2 (cap 14220s = 3.95 GPU-h) runs ONLY if decide_pilot.json reports status=="COMPLETE" and P1_verdict=="GO",
#          writing ONLY decide_pilot_stageB.json (never rewriting Stage A decide_pilot.json, W6).
# Usage: bash scripts/ken_dvqa_pilot/job.sh <expected_40_hex_git_HEAD> [<expected_SHA256SUMS_sha>]
set -u

EXPECT=${1:-}
EXPECT_SUMS_ARG=${2:-${EXPECT_SUMS_SHA:-}}
cd /root/vsps || exit 1
export PYTHONHASHSEED=0
export PYTHONDONTWRITEBYTECODE=1
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=${VSPS_MACHINE_ID:-$(hostname)}

# CC-104a W8: Hard-require D=scripts/ken_dvqa_pilot (no v2 or manuscript fallbacks)
D="scripts/ken_dvqa_pilot"

LB=/root/venv-lb/bin/python
DVQA_DIR=/root/dvqa_pilot
IMG_SHA_TSV=manuscript/ken/dvqa_train3142_image_sha256.tsv
O=.session_backup/2026-10-26/dvqa_pilot
R=$O/runs
LOG=$O/logs
LED=$O/ledger.jsonl
GPU_TSV=$O/gpu_seconds.tsv
DECIDE_OUT=$O/decide_pilot.json
DECIDE_B_OUT=$O/decide_pilot_stageB.json
SUMS=$D/SHA256SUMS

HUB=/root/.cache/huggingface/hub
Q25=$HUB/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/cc594898137f460bfe9f0759e9844b3ce807cfb5
IV3=$HUB/models--OpenGVLab--InternVL3-8B-hf/snapshots/259a3b64a14623c0ec91a045cb43f7c5af5fa6af
VENV_PIN_PREFIX="685ffe2a"

P1_CAP=14040
P3_CAP=17100
P2_CAP=14220

ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*"; }
stop() { say "JOB STOP: $*"; exit 1; }

[ -d "$D" ] || stop "Refused (W8): required directory $D does not exist"
mkdir -p "$R" "$LOG"

# ---------------------------------------------------------------- 0. One-Run-Only Check (CC-104a W5: never truncate or resume)
compgen -G "$R/*.jsonl" >/dev/null && stop "Refused (W5): $R already holds *.jsonl; one run only without judge ruling"
[ ! -e "$GPU_TSV" ] || stop "Refused (W5): $GPU_TSV already exists; never truncate or resume"
[ ! -e "$LED" ] || stop "Refused (W5): $LED already exists; never truncate or resume"
[ ! -e "$DECIDE_OUT" ] || stop "Refused (W5): $DECIDE_OUT already exists; one run only"
[ ! -e "$DECIDE_B_OUT" ] || stop "Refused (W5): $DECIDE_B_OUT already exists; one run only"

# ---------------------------------------------------------------- 1. CPU Preflight & Host Hygiene BEFORE any GPU timer (CC-104 F5, F8, F10; CC-104a W2, W8)
[ "$VSPS_MACHINE_ID" = "m3" ] || [ "$VSPS_MACHINE_ID" = "M3" ] && stop "Refused (W2): DrivingVQA pilot must run on M4, never on M3"
[ -f /root/.vsps_machine_id ] && [ "$(tr -d '[:space:]' < /root/.vsps_machine_id | tr '[:upper:]' '[:lower:]')" = "m4" ] \
  || stop "Refused (W2): /root/.vsps_machine_id must exist and equal 'm4'"
[ -n "$EXPECT" ] && [ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD does not match expected commit $EXPECT"
git diff --quiet HEAD -- || stop "Tracked files differ from HEAD"
[ -f "$SUMS" ] || stop "Refused (W8): missing $SUMS"
PINNED_SUMS=${EXPECT_SUMS_ARG:-$(git log -1 --format=%B HEAD 2>/dev/null | grep -oE 'SHA256SUMS[^0-9a-fA-F]*[0-9a-f]{8,64}' | grep -oE '[0-9a-f]{8,64}$' | head -n1)}
[ -n "$PINNED_SUMS" ] || stop "Refused (W8): missing gatekeeper SHA256SUMS pin (pass as arg 2, EXPECT_SUMS_SHA, or in HEAD commit message)"
ACTUAL_SUMS=$(sha256sum "$SUMS" | cut -d' ' -f1)
case "$ACTUAL_SUMS" in
  ${PINNED_SUMS}*) ;;
  *) stop "Refused (W8): $SUMS sha256 ($ACTUAL_SUMS) does not match gatekeeper pin ($PINNED_SUMS)" ;;
esac
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
  --out "$O/host_check.json" >> "$LOG/host_check.log" 2>&1 \
  || stop "M4 host_check failed (F5 / W2 / W3 / W4)"

say "JOB START head=$EXPECT sums=$ACTUAL_SUMS venv=$FREEZE_SHA"

run_capped_block() {
  # run_capped_block STAGE CAP_SECONDS DECIDE_STAGE DECIDE_TARGET
  local stage=$1
  local cap=$2
  local d_stage=${3:-A}
  local d_out=${4:-$DECIDE_OUT}
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
      $LB -B "$D/decide.py" --ledger "$LED" --gpu-seconds "$GPU_TSV" --stage "$d_stage" --out "$d_out" >> "$LOG/decide.log" 2>&1 || true
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
      $LB -B "$D/decide.py" --ledger "$LED" --gpu-seconds "$GPU_TSV" --stage "$d_stage" --out "$d_out" >> "$LOG/decide.log" 2>&1 || true
      stop "${stage}_${model} hit timeout cap -> INCOMPLETE"
    elif [ "$rc" -ne 0 ]; then
      echo -e "${stage}_${model}\t${step_sec}\tFAIL" >> "$GPU_TSV"
      $LB -B "$D/score.py" --runs-dir "$R" --dvqa-dir "$DVQA_DIR" --ledger "$LED" >> "$LOG/score.log" 2>&1 || true
      $LB -B "$D/decide.py" --ledger "$LED" --gpu-seconds "$GPU_TSV" --stage "$d_stage" --out "$d_out" >> "$LOG/decide.log" 2>&1 || true
      stop "${stage}_${model} failed with rc=$rc"
    fi
    echo -e "${stage}_${model}\t${step_sec}\tOK" >> "$GPU_TSV"
    say "OK ${stage}_${model} (${step_sec}s)"
  done
}

# ---------------------------------------------------------------- 2. Stage A: P1 (3.90 GPU-h cap) then P3 (4.75 GPU-h cap)
run_capped_block P1 "$P1_CAP" A "$DECIDE_OUT"
run_capped_block P3 "$P3_CAP" A "$DECIDE_OUT"

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

# ---------------------------------------------------------------- 3. Stage B: P2 (3.95 GPU-h cap), ONLY if P1_verdict == GO (W6: writes only decide_pilot_stageB.json)
if [ "$P1_VERDICT" = "GO" ]; then
  say "P1_verdict is GO -> starting Stage B (P2, cap ${P2_CAP}s)"
  run_capped_block P2 "$P2_CAP" B "$DECIDE_B_OUT"
  $LB -B "$D/score.py" --runs-dir "$R" --dvqa-dir "$DVQA_DIR" --ledger "$LED" >> "$LOG/score.log" 2>&1 \
    || stop "Stage B score.py failed"
  $LB -B "$D/decide.py" --ledger "$LED" --gpu-seconds "$GPU_TSV" --stage B --out "$DECIDE_B_OUT" >> "$LOG/decide.log" 2>&1 \
    || stop "Stage B decide.py failed"
  P2_VERDICT=$($LB -B -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('P2_verdict',''))" "$DECIDE_B_OUT")
  say "STAGE B DONE: P2_verdict=$P2_VERDICT"
else
  say "P1_verdict is $P1_VERDICT -> Stage B (P2) cancelled with 0 GPU spent"
  $LB -B "$D/decide.py" --ledger "$LED" --gpu-seconds "$GPU_TSV" --stage B --out "$DECIDE_B_OUT" >> "$LOG/decide.log" 2>&1 \
    || stop "Stage B cancelled decide.py failed"
fi

(cd "$O" && sha256sum host_check.json gpu_seconds.tsv ledger.jsonl decide_pilot.json decide_pilot_stageB.json > SHA256SUMS)
say "PILOT JOB COMPLETE"
