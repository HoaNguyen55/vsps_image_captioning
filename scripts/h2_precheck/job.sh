#!/bin/bash
# M3: Paper E' H2 flip-budget precheck (EXPLORATORY / DEV-PRECHECK, CC-098, CC-101), manuscript/prereg/2026-10-25_h2_precheck/PRECHECK_NOTE.md.
# Arm D of the E' pilot (Qwen2.5-VL-7B, InternVL3-8B; KTVIC dev299 and XM-dev300) decoded again with per-step scores kept.
# Never in C's January test window. Hard cap 1 GPU-h (wall time of this job, retries included). Runs only after the CPU
# ceiling (flipbudget.py ceiling, step 0) has not stopped H2.
# The host check (stage2.py check-host --block xm) needs C's stage-2 XM dev state staged, as for the E' pilot (CC-100b).
# Usage: job.sh <expected 40-hex HEAD>        job.sh --selftest   (CPU, repo root; PY=<python> overrides the interpreter)
old_outputs() { [ -n "$(ls "$1"/h2_* 2>/dev/null)" ]; }  # CC-101 W4: outputs of an earlier job in the runs dir
if [ "$1" = "--selftest" ]; then
  PY=${PY:-python}; D=scripts/h2_precheck; export NCS_DATA=$(mktemp -d); T=$(mktemp -d)
  ! old_outputs $T && touch $T/h2_x.preds.json && old_outputs $T && echo "refusal of earlier h2_* outputs ok" && \
  bash -n "$0" && $PY $D/flipbudget.py --selftest && \
    sha256sum --quiet -c manuscript/prereg/2026-10-25_h2_precheck/SHA256SUMS && echo "job selftest ok"
  exit $?
fi
EXPECT=$1
cd /root/vsps || exit 1
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=$(hostname)
export VSPS_JOB_SHA256=$(sha256sum "$0" | cut -c1-64)
unset NCS_DATASET
LB=/root/venv-lb/bin/python
D=scripts/h2_precheck; CD=scripts/c_stage2; O=/root/outputs/h2_precheck; R=$O/runs; LOG=$O/logs
L=manuscript/prereg/2026-10-22_c_stage1/lists.json
SUMS=manuscript/prereg/2026-10-25_h2_precheck/SHA256SUMS
HUB=/root/.cache/huggingface/hub
Q25=$HUB/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/cc594898137f460bfe9f0759e9844b3ce807cfb5
IV3=$HUB/models--OpenGVLab--InternVL3-8B-hf/snapshots/259a3b64a14623c0ec91a045cb43f7c5af5fa6af
LB_FREEZE=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784  # every pilot arm-D output records it
CAP=3600; T0=$(date +%s)
! old_outputs $R || { echo "$R holds h2_* outputs of an earlier job; move them away (CC-101 W4)"; exit 1; }
mkdir -p $R $LOG
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*"; }
stop() { say "JOB STOP $*"; exit 1; }
left() { echo $((CAP - ($(date +%s) - T0))); }
trap 'echo "h2_precheck $(( $(date +%s) - T0 ))" >> $O/gpu_seconds.tsv' EXIT

step() {  # step NAME CMD...: up to 3 attempts under the time left; 124 = cap reached. decode resumes from its partials
  local name=$1; shift
  for a in 1 2 3; do
    local t; t=$(left); [ "$t" -gt 60 ] || stop "1 GPU-h cap before $name"
    say "START $name attempt $a (left $((t / 60)) min)"
    timeout ${t}s "$@" >> $LOG/$name.log 2>&1; local rc=$?
    [ $rc = 0 ] && { say "OK $name"; return 0; }
    [ $rc = 124 ] && stop "1 GPU-h cap reached during $name"
    say "FAIL $name attempt $a rc=$rc"
  done
  stop "$name failed 3 times"
}

# ---------------------------------------------------------------- preflight
[ -n "$EXPECT" ] && [ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
sha256sum --quiet -c $SUMS || stop "$SUMS does not verify"
[ "$(${LB%/python}/pip freeze | sha256sum | cut -c1-64)" = $LB_FREEZE ] || stop "venv-lb freeze differs from the pilot's (CC-101 O1)"
[ ! -e data/xm3600/oiv7_labels.json ] || stop "oiv7_labels.json is in the checkout (CC-101 O1)"
[ -z "$(find /root/outputs /root/ncs-data \( -name 'decide_final*' -o -name 'verified*.jsonl' -o -name 'oiv7*' \) 2>/dev/null)" ] || stop "a CC-099-deleted or OIV7 file is on M3 (CC-101 O1)"
$LB $D/flipbudget.py --selftest >> $LOG/selftest.log 2>&1 || stop "flipbudget selftest"
$LB $CD/stage2.py check-host --block xm --lists $L > $O/host.json 2>> $LOG/host.log || stop "host check"
sha256sum $D/*.py $D/job.sh $SUMS > $O/code_at_start.sha256
export VSPS_VENV_FREEZE_SHA256=$(${LB%/python}/pip freeze | sha256sum | cut -c1-64)
say "JOB START head $EXPECT"

step dec_qwen $LB $D/flipbudget.py decode --model qwen25vl_7b --snapshot $Q25 --lists $L --out-dir $R
step dec_internvl $LB $D/flipbudget.py decode --model internvl3_8b --snapshot $IV3 --lists $L --out-dir $R
n=$(ls $R/h2_*-d.preds.json $R/h2_*-d.steps.jsonl 2>/dev/null | wc -l); [ "$n" = 8 ] || stop "$n of 8 outputs"
(cd $O && sha256sum runs/h2_*-d.preds.json runs/h2_*-d.steps.jsonl > SHA256SUMS)
say "JOB DONE gpu_h_wall $(( ($(date +%s) - T0) / 36 ))e-2"
