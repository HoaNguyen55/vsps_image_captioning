#!/bin/bash
# L1-b DEV-EXPLORE on M2 (machine id m4, the dev role): ViTextVQA dev half E only (l1b_split.json), training-free
# image-verified mark re-rank. GPU steps: both non-Qwen models in fixed order (gemma3_4b, skipped while G3_gemma or its
# pins are open; then idefics3_8b): first pass on E + re-rank; then the re-rank of the 3 Qwen-family backbones. The Qwen-family first passes are the staged L1-a img
# preds (no re-decode). No scoring here: outputs are pulled to the laptop and scored once by `l1b.py score`
# (rule manuscript/prereg/2026-10-29_l1b/PREREG.md). Cap 8 GPU-h (B-1 accounting via l1b.py left); a timeout is a
# CAP STOP, final. Any other failure is a JOB STOP back to the judge, except rc 3 = parity failure (that backbone is
# NOT_ASSESSABLE, the job goes on). Staged before (operator, one LOG checklist line, no host string):
# $ST = $NCS_DATA/datasets/l1b_vitextvqa_dev_E = the laptop's data/datasets/l1b_vitextvqa_dev_E (E images, grey.png,
# questions.jsonl without answers, preds/ = 3 L1-a img preds). Never a C, train or test image; never a gold answer.
# Usage, inside tmux on M2:  bash scripts/l1b/l1b_job.sh <expected 40-hex HEAD>
set -euo pipefail
EXPECT=${1:?usage: l1b_job.sh <expected HEAD>}
[ "$(cat /root/.vsps_machine_id 2>/dev/null)" = m4 ] || { echo "REFUSED: /root/.vsps_machine_id is not m4"; exit 1; }
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=m4
LB=/root/venv-lb/bin/python   # GPU steps (transformers 4.57.6, the B-N1 registry's venv)
PY=/root/vsps/.venv/bin/python   # selftest, guard, lock and cap arithmetic (they import b1.py), as L1-a
LB_FREEZE=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784   # setup_gpu.sh H_LB
X=scripts/l1b/l1b.py; JOB=scripts/l1b/l1b_job.sh
O=/root/outputs/l1b; P=$O/out; LOG=$O/logs; USED=$O/gpu_seconds.tsv; MARK=$O/CAP_STOP.json
ST=$NCS_DATA/datasets/l1b_vitextvqa_dev_E
export L1B_LOCK=$O/RUNNING VSPS_JOB_SHA256=$(sha256sum $JOB | cut -c1-64)
mkdir -p $O $P $LOG
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*" | tee -a $LOG/job.log; }
stop() { say "JOB STOP $*"; exit 1; }
$PY $X lock --path $L1B_LOCK || exit 1   # tmux only, no other /root/outputs/*/RUNNING, O_EXCL
trap 'rm -f $L1B_LOCK' EXIT

# ---------------------------------------------------------------- preflight
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
sha256sum --quiet -c scripts/l1a/SHA256SUMS || stop "scripts/l1a/SHA256SUMS does not verify"
sha256sum --quiet -c scripts/l1b/SHA256SUMS || stop "scripts/l1b/SHA256SUMS does not verify"
sha256sum --quiet -c manuscript/prereg/2026-10-29_l1b/SHA256SUMS || stop "prereg SHA256SUMS does not verify"
[ "$(/root/venv-lb/bin/pip freeze | sha256sum | cut -c1-64)" = $LB_FREEZE ] || stop "venv-lb freeze differs"
$PY $X --selftest >> $LOG/selftest.log 2>&1 || stop "l1b selftest"
G() { $PY $X guard --head "$EXPECT" --stage $ST >> $LOG/guard.log 2>&1 || stop "guard (m4, GPU, HEAD, gates, stage)"; }
G
sha256sum $X $JOB scripts/l1b/SHA256SUMS > $O/code_at_start.sha256
say "JOB START head $EXPECT"

cap_stop() {
  [ -e $MARK ] || printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > $MARK
  say "CAP STOP $1"; finish; }
finish() {  # no scoring on M2: sums for the laptop pull
  (cd $O && find out logs -type f ! -name '*.partial*' | sort | xargs -r sha256sum) > $O/SHA256SUMS
  say "BLOCK DONE gpu_h $(awk '$2 != "start" {s += $2} END {printf "%.2f", s / 3600}' $USED)"
  exit 0
}
gpu() {  # gpu NAME CMD...: one GPU step under the time left; returns the step's rc for 0 and 3, else stops
  local name=$1; shift
  local t; t=$($PY $X left --used $USED --marker $MARK) || stop "cap arithmetic"
  [ "$t" -gt 0 ] || cap_stop "8 GPU-h cap before $name"
  G; say "START $name (left $((t / 60)) min)"
  local t0 rc=0; t0=$(date +%s)
  echo "$name start $t0" >> $USED
  timeout ${t}s "$@" >> $LOG/$name.log 2>&1 || rc=$?
  echo "$name $(( $(date +%s) - t0 ))" >> $USED
  [ $rc = 124 ] && cap_stop "8 GPU-h cap reached during $name"
  [ $rc = 0 ] && { say "OK $name"; return 0; }
  [ $rc = 3 ] && { say "PARITY FAIL $name (NOT_ASSESSABLE)"; return 3; }
  stop "$name rc=$rc"
}
fetch() {  # CPU, online, not charged; returns 1 if the pinned files cannot be fetched (e.g. gate not granted)
  local m=$1 s; s=$($LB $X snap --model $m)
  [ -e $s/.l1b_ok ] && return 0
  HF_HUB_OFFLINE=0 $LB $X fetch --model $m --snapshot $s >> $LOG/fetch_$m.log 2>&1 || { say "FETCH FAIL $m"; return 1; }
  touch $s/.l1b_ok
}
rerank() {  # rerank MODEL BASEFILE
  local m=$1; [ -s $P/l1b_${m}_rerank.jsonl.sha256 ] && return 0
  [ -e $P/l1b_${m}_PARITY_FAIL.json ] && return 3
  gpu rr_$m $LB $X rerank --model $m --stage $ST --snapshot "$($LB $X snap --model $m)" --base $2 --out-dir $P
}

# ---------------------------------------------------------------- non-Qwen first (the verdict needs it), then Qwen
for m in gemma3_4b idefics3_8b; do   # both, always, in this order (CC-168 W2); score uses the first assessable
  $PY $X nqok --model $m >> $LOG/nqok.log 2>&1 || { say "SKIP $m (gate or pins open, see nqok.log)"; continue; }
  fetch $m || continue
  if [ ! -s $P/l1b_${m}_img.preds.json.sha256 ]; then
    gpu dec_$m $LB $X decode --model $m --stage $ST --snapshot "$($LB $X snap --model $m)" --out-dir $P
  fi
  rerank $m $P/l1b_${m}_img.preds.json || true   # rc 3 = parity fail, logged, next backbone
done
for m in qwen25vl_7b internvl3_8b qwen3vl_8b; do
  rerank $m $ST/preds/l1a_${m}_img.preds.json || true   # rc 3 = parity fail, logged, next backbone
done
finish
