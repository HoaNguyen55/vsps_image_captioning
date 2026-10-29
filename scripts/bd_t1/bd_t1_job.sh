#!/bin/bash
# Paper B+D, BD-T1 (TIER 1, DEV-EXPLORE ONLY) on M2 (machine id m4): B-1's P1_dev recipe, unchanged (KTVIC first
# caption, build_gold_sft.py default), on the reduced pool of bd_t1_lists.json (B-1 pool minus H minus near-twins),
# levels V1-V5 x seeds 42/43/44, each decoded on KTVIC dev300 with the short prompt. Never a test split, never an H
# image: the guard refuses while any H image sha256 exists under $NCS_DATA/datasets. No scoring here: preds are pulled
# to the laptop and scored once by `bd_t1.py score` (prereg manuscript/prereg/2026-10-30_bd_t1/PREREG.md).
# Cap: 15 GPU-h over the GPU steps (B-1's step accounting); a timeout is a final CAP STOP. Any other failure is a JOB
# STOP back to the judge. A crashed training run is NOT resumed (CC-152a): the job stops; the run folder is deleted
# unread before one from-scratch retrain.
# Staged before (operator): the B-1 stage set ($NCS_DATA/datasets/ktvic train images + train_data.json, ktvic_dev,
# base snapshot, $NCS_DATA/runs/p1dev_s42, $O/s5_preds/<n2 preds>, resume hook) WITH EVERY H IMAGE DELETED from
# $NCS_DATA/datasets/ktvic/images (bd_t1_lists.json H ids). No OpenViIC file of any split is staged.
# Usage, inside tmux on M2:  bash scripts/bd_t1/bd_t1_job.sh <expected 40-hex HEAD>
set -euo pipefail
EXPECT=${1:?usage: bd_t1_job.sh <expected HEAD>}
[ "$(cat /root/.vsps_machine_id 2>/dev/null)" = m4 ] || { echo "REFUSED: /root/.vsps_machine_id is not m4"; exit 1; }
cd /root/vsps
set +u; . .venv/bin/activate; set -u
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
unset NCS_DATASET RESCAP_RAW_TONE RESCAP_G1_BYTE_CHECK RESCAP_SAVE_STEPS RESCAP_SAVE_LIMIT RESCAP_MIRROR_ROOT
T1=scripts/bd_t1/bd_t1.py; B1=scripts/b1_scaling/b1.py; JOB=scripts/bd_t1/bd_t1_job.sh
O=/root/outputs/bd_t1; D=$O/data; LOG=$O/logs; USED=$O/gpu_seconds.tsv; MARK=$O/CAP_STOP.json
export T1_LOCK=$O/RUNNING
VS_FREEZE=7332d343173e5681365cf6871671e36209c77803a1b2db70da1cc766d5c943ed   # B-1's .venv pin (setup_gpu.sh H_VS)
HOOK_SHA=05466ef5ed3bef2b732ccd01f530a8c977c4c822ef8619b0238f562fb11e5895   # B-1's resume hook pin
N2=$O/s5_preds/p1dev_s42_redecode-dev300-short.preds.json   # B-1 Step 0 reference (1e183383)
mkdir -p $O $D $LOG
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*" | tee -a $LOG/job.log; }
stop() { say "JOB STOP $*"; exit 1; }
python $B1 lock --path $T1_LOCK || exit 1   # tmux only, no other /root/outputs/*/RUNNING, O_EXCL
trap 'rm -f $T1_LOCK' EXIT

# ---------------------------------------------------------------- preflight
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
sha256sum --quiet -c scripts/bd_t1/SHA256SUMS || stop "scripts/bd_t1/SHA256SUMS does not verify"
sha256sum --quiet -c scripts/b1_scaling/SHA256SUMS || stop "scripts/b1_scaling/SHA256SUMS does not verify"
sha256sum --quiet -c scripts/b_r1/SHA256SUMS || stop "scripts/b_r1/SHA256SUMS does not verify (imported helpers)"
[ "$(pip freeze | sha256sum | cut -c1-64)" = $VS_FREEZE ] || stop ".venv freeze differs from H_VS"
HOOK=/root/vsps/.venv/lib/python3.10/site-packages/vsps_resume_hook.py
[ -e $HOOK ] && [ "$(sha256sum $HOOK | cut -c1-64)" = $HOOK_SHA ] || stop "resume hook not installed"
python -c 'import sys; assert "vsps_resume_hook" in sys.modules' || stop "resume hook not imported"
python $T1 --selftest >> $LOG/selftest.log 2>&1 || stop "bd_t1 selftest"
python $B1 check --machine --job $JOB >> $LOG/check.log 2>&1 || stop "b1 check (S5 code, base, p1dev, job fragments)"
python $T1 rootscan --root /root >> $LOG/guard.log 2>&1 || stop "rootscan: an H image exists under /root (CC-171 W5)"
G() { python $T1 guard --head "$EXPECT" >> $LOG/guard.log 2>&1 || stop "guard (m4, GPU, HEAD, H images, openviic, test, locks)"; }
G
sha256sum $T1 $JOB scripts/bd_t1/SHA256SUMS > $O/code_at_start.sha256
say "JOB START head $EXPECT"

finish() {  # no scoring on M2: sums for the laptop pull
  (cd $O && find . -type f ! -name 'SHA256SUMS*' ! -name RUNNING ! -name '*.partial*' | sort | xargs sha256sum) \
    > $O/SHA256SUMS
  say "BLOCK DONE gpu_h $(awk '$2 != "start" {s += $2} END {printf "%.2f", s / 3600}' $USED)"
  exit 0
}
cap_stop() {
  [ -e $MARK ] || printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > $MARK
  say "CAP STOP $1"; finish; }
step() {  # step NAME CMD...: one GPU step under the time left (B-1's accounting)
  local name=$1; shift
  local t; t=$(python $T1 left --used $USED --marker $MARK) || stop "cap arithmetic"
  [ "$t" -gt 0 ] || cap_stop "15 GPU-h cap before $name"
  G; say "START $name (left $((t / 60)) min)"
  local t0 rc=0; t0=$(date +%s)
  echo "$name start $t0" >> $USED
  timeout ${t}s "$@" >> $LOG/$name.log 2>&1 || rc=$?
  echo "$name $(( $(date +%s) - t0 ))" >> $USED
  [ $rc = 0 ] && { say "OK $name"; return 0; }
  [ $rc = 124 ] && cap_stop "15 GPU-h cap reached during $name"
  stop "$name rc=$rc"
}
decode() {  # decode NAME [ADAPTER]: B-1's greedy short-prompt dev300 decode (evaluate.py defaults)
  local res=$O/$1-dev300-short.json; local ad=(); [ -n "${2:-}" ] && ad=(--adapter "$2")
  [ -s $res ] && return 0
  [ -s ${res%.json}.preds.json ] && stop "$1: preds without result (judge)"
  step dec_$1 env NCS_DATASET=ktvic_dev python scripts/evaluate.py --model qwen2.5-vl-7b "${ad[@]}" \
    --split dev_data.json --prompt short --name $1-dev300-short --out $res
}

# ---------------------------------------------------------------- data (CPU)
[ -s $N2 ] || stop "n2 preds not uploaded"
python $T1 ids --dir $D || stop "ids"
python scripts/ktvic_dev_split.py --verify --json-dir $NCS_DATA/datasets/ktvic_dev >> $LOG/data.log 2>&1 \
  || stop "dev300 split"
for lv in V1 V2 V3 V4 V5; do
  [ -s $D/gold_t1_$lv/sft.jsonl ] || python scripts/build_gold_sft.py --annotations \
    $NCS_DATA/datasets/ktvic/train_data.json --out $D/gold_t1_$lv \
    --images-file $D/bd_t1_$lv.txt >> $LOG/data.log 2>&1 || stop "build_gold_sft $lv"
done
python $T1 sft --dir $D >> $LOG/data.log 2>&1 || stop "sft.jsonl pins"

# ---------------------------------------------------------------- GPU: Step 0 (machine parity), 15 points
decode t1_step0_p1dev_s42 $NCS_DATA/runs/p1dev_s42
python $B1 step0 --redecode $O/t1_step0_p1dev_s42-dev300-short.preds.json --n2 $N2 > $O/step0.json 2>> $LOG/job.log \
  || stop "Step 0: fewer than 95% identical captions to the registered n2 decode"
for S in 42 43 44; do
  for lv in V1 V2 V3 V4 V5; do
    R=t1_s${S}_$lv; RUN=$NCS_DATA/runs/$R
    [ -e $RUN ] && [ ! -s $RUN/metrics.jsonl ] && stop "$R partial run (CC-152a: delete unread, retrain once)"
    if [ ! -s $RUN/metrics.jsonl ]; then
      step train_$R python scripts/train_stage2.py --stage sft --data $D/gold_t1_$lv --out $RUN \
        --epochs 2 --seed $S --loss-mask assistant
    fi
    for want in "loss mask: assistant" "save_steps=200" "512 vision tokens, 4-bit"; do
      grep -q "$want" $LOG/train_$R.log || stop "$R: '$want' not in its training log"
    done
    decode $R $RUN
  done
done
finish
