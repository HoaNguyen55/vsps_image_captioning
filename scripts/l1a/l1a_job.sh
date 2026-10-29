#!/bin/bash
# L1-a (DEV ONLY) on M2 (machine id m4): ViTextVQA dev, 5,155 QA, 4 pinned backbones (B-N1 registry), each decoded
# with the real image (arm img) and with a grey 512x512 image in its place (arm grey, the contamination / language-
# prior probe). Greedy, one pinned Vietnamese prompt, 48 new tokens. No scoring here: the preds are pulled to the
# laptop and scored once by `l1a.py score` (rule manuscript/prereg/2026-10-29_l1a/RULE.md).
# Cap: 12 GPU-h over the GPU steps (B-1's accounting via l1a.py left); a timeout is a CAP STOP, final.
# Any other failure is a JOB STOP back to the judge. A finished step (preds + sidecar) is skipped on re-run; an
# interrupted decode resumes from its fsynced slices (decode_hf_vlm.decode_slices, same run key only).
# Staged before (operator, one LOG checklist line): $ST = $NCS_DATA/datasets/l1a_vitextvqa_dev with exactly
# images/<1,676 dev jpgs>, grey.png, questions.jsonl (no answers), all at the l1a_lists.json shas. Never the zip,
# never a train or test image, never a test json.
# Usage, inside tmux on M2:  bash scripts/l1a/l1a_job.sh <expected 40-hex HEAD>
set -euo pipefail
EXPECT=${1:?usage: l1a_job.sh <expected HEAD>}
[ "$(cat /root/.vsps_machine_id 2>/dev/null)" = m4 ] || { echo "REFUSED: /root/.vsps_machine_id is not m4"; exit 1; }
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=m4
LB=/root/venv-lb/bin/python   # decode (transformers 4.57.6, the B-N1 registry's venv)
PY=/root/vsps/.venv/bin/python   # selftest, guard, lock and cap arithmetic (they import b1.py), as B-R1
LB_FREEZE=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784   # setup_gpu.sh H_LB
X=scripts/l1a/l1a.py; JOB=scripts/l1a/l1a_job.sh
O=/root/outputs/l1a; P=$O/preds; LOG=$O/logs; USED=$O/gpu_seconds.tsv; MARK=$O/CAP_STOP.json
ST=$NCS_DATA/datasets/l1a_vitextvqa_dev
export L1A_LOCK=$O/RUNNING VSPS_JOB_SHA256=$(sha256sum $JOB | cut -c1-64)
mkdir -p $O $P $LOG
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*" | tee -a $LOG/job.log; }
stop() { say "JOB STOP $*"; exit 1; }
$PY $X lock --path $L1A_LOCK || exit 1   # tmux only, no other /root/outputs/*/RUNNING, O_EXCL
trap 'rm -f $L1A_LOCK' EXIT

# ---------------------------------------------------------------- preflight
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
sha256sum --quiet -c scripts/l1a/SHA256SUMS || stop "scripts/l1a/SHA256SUMS does not verify"
sha256sum --quiet -c manuscript/prereg/2026-10-29_l1a/SHA256SUMS || stop "prereg SHA256SUMS does not verify"
[ "$(/root/venv-lb/bin/pip freeze | sha256sum | cut -c1-64)" = $LB_FREEZE ] || stop "venv-lb freeze differs"
$PY $X --selftest >> $LOG/selftest.log 2>&1 || stop "l1a selftest"
G() { $PY $X guard --head "$EXPECT" --stage $ST >> $LOG/guard.log 2>&1 || stop "guard (m4, GPU, HEAD, stage, test, locks)"; }
G
sha256sum $X $JOB scripts/l1a/SHA256SUMS > $O/code_at_start.sha256
say "JOB START head $EXPECT"

# ---------------------------------------------------------------- fetch (CPU, online, not charged)
S3=$($LB $X snap --model qwen25vl_3b)
if [ ! -e $S3/.l1a_ok ]; then
  HF_HUB_OFFLINE=0 $LB $X fetch --model qwen25vl_3b --snapshot $S3 >> $LOG/fetch.log 2>&1 || stop "fetch qwen25vl_3b"
  touch $S3/.l1a_ok
fi

# ---------------------------------------------------------------- GPU: 4 backbones x {img, grey}, img arms first
cap_stop() {
  [ -e $MARK ] || printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > $MARK
  say "CAP STOP $1"; finish; }
finish() {  # no scoring on M2: sums for the laptop pull
  (cd $O && find preds logs -type f ! -name '*.partial*' | sort | xargs sha256sum) > $O/SHA256SUMS
  say "BLOCK DONE gpu_h $(awk '$2 != "start" {s += $2} END {printf "%.2f", s / 3600}' $USED)"
  exit 0
}
step() {  # step MODEL ARM: one decode under the time left
  local m=$1 arm=$2 name=dec_$1_$2
  [ -s $P/l1a_${m}_${arm}.preds.json.sha256 ] && return 0
  local t; t=$($PY $X left --used $USED --marker $MARK) || stop "cap arithmetic"
  [ "$t" -gt 0 ] || cap_stop "12 GPU-h cap before $name"
  G; say "START $name (left $((t / 60)) min)"
  local t0 rc=0; t0=$(date +%s)
  echo "$name start $t0" >> $USED
  timeout ${t}s $LB $X decode --model $m --arm $arm --stage $ST --snapshot "$($LB $X snap --model $m)" \
    --out-dir $P >> $LOG/$name.log 2>&1 || rc=$?
  echo "$name $(( $(date +%s) - t0 ))" >> $USED
  [ $rc = 0 ] && { say "OK $name"; return 0; }
  [ $rc = 124 ] && cap_stop "12 GPU-h cap reached during $name"
  stop "$name rc=$rc"
}
for arm in img grey; do
  for m in qwen25vl_7b qwen3vl_8b internvl3_8b qwen25vl_3b; do
    step $m $arm
  done
done
finish
