#!/bin/bash
# M3: Paper E' pilot (EXPLORATORY / DEV-PILOT, CC-098; not confirmatory), manuscript/prereg/2026-10-23_eprime_pilot/PILOT_NOTE.md.
# Decodes arms en, t, d, a for Qwen2.5-VL-7B and InternVL3-8B on KTVIC dev299 and the first 300 XM-dev500 images.
# Only after C's stage-2 XM block is scored (decide_xm_m3.json) and never in C's January test window.
# Hard cap 2 GPU-h (wall time of this job, retries included); every step runs under `timeout` with the time left.
# The host check (stage2.py check-host) also fails if oiv7_labels.json is anywhere on the host.
# Usage: job.sh <expected 40-hex HEAD>        job.sh --selftest   (CPU, repo root; PY=<python> overrides the interpreter)
if [ "$1" = "--selftest" ]; then
  PY=${PY:-python}; D=scripts/eprime_pilot; export NCS_DATA=$(mktemp -d)
  bash -n "$0" && $PY $D/decode_pilot.py --selftest && $PY $D/score_pilot.py --selftest && \
    sha256sum --quiet -c manuscript/prereg/2026-10-23_eprime_pilot/SHA256SUMS && echo "job selftest ok"
  exit $?
fi
EXPECT=$1
cd /root/vsps || exit 1
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=$(hostname)
export VSPS_JOB_SHA256=$(sha256sum "$0" | cut -c1-64)
unset NCS_DATASET
LB=/root/venv-lb/bin/python
D=scripts/eprime_pilot; CD=scripts/c_stage2; O=/root/outputs/eprime_pilot; R=$O/runs; LOG=$O/logs
L=manuscript/prereg/2026-10-22_c_stage1/lists.json
SUMS=manuscript/prereg/2026-10-23_eprime_pilot/SHA256SUMS
HUB=/root/.cache/huggingface/hub
Q25=$HUB/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/cc594898137f460bfe9f0759e9844b3ce807cfb5
IV3=$HUB/models--OpenGVLab--InternVL3-8B-hf/snapshots/259a3b64a14623c0ec91a045cb43f7c5af5fa6af
CAP=$((2 * 3600)); T0=$(date +%s)
mkdir -p $R $LOG
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*"; }
stop() { say "JOB STOP $*"; exit 1; }
left() { echo $((CAP - ($(date +%s) - T0))); }
trap 'echo "pilot $(( $(date +%s) - T0 ))" >> $O/gpu_seconds.tsv' EXIT

step() {  # step NAME CMD...: up to 3 attempts under the time left; 124 = cap reached. decode resumes from its partials
  local name=$1; shift
  for a in 1 2 3; do
    local t; t=$(left); [ "$t" -gt 60 ] || stop "2 GPU-h cap before $name"
    say "START $name attempt $a (left $((t / 60)) min)"
    timeout ${t}s "$@" >> $LOG/$name.log 2>&1; local rc=$?
    [ $rc = 0 ] && { say "OK $name"; return 0; }
    [ $rc = 124 ] && stop "2 GPU-h cap reached during $name"
    say "FAIL $name attempt $a rc=$rc"
  done
  stop "$name failed 3 times"
}

# ---------------------------------------------------------------- preflight
[ -n "$EXPECT" ] && [ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
sha256sum --quiet -c $SUMS || stop "$SUMS does not verify"
[ -e /root/outputs/c_stage2/decide_xm_m3.json ] || stop "C's stage-2 XM block is not scored (CC-098: pilot after it)"
$LB $D/decode_pilot.py --selftest >> $LOG/selftest.log 2>&1 || stop "decode_pilot selftest"
$LB $CD/stage2.py check-host --block xm --lists $L > $O/host.json 2>> $LOG/host.log || stop "host check"
sha256sum $D/*.py $D/job.sh $SUMS > $O/code_at_start.sha256
export VSPS_VENV_FREEZE_SHA256=$(${LB%/python}/pip freeze | sha256sum | cut -c1-64)
say "JOB START head $EXPECT"

step dec_qwen $LB $D/decode_pilot.py decode --model qwen25vl_7b --snapshot $Q25 --lists $L --out-dir $R
step dec_internvl $LB $D/decode_pilot.py decode --model internvl3_8b --snapshot $IV3 --lists $L --out-dir $R
n=$(ls $R/ep_*-{en,t,d,a}.preds.json 2>/dev/null | wc -l); [ "$n" = 16 ] || stop "$n of 16 outputs"
(cd $O && sha256sum runs/ep_*.preds.json > SHA256SUMS)
say "JOB DONE gpu_h_wall $(( ($(date +%s) - T0) / 36 ))e-2"
