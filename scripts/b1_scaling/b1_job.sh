#!/bin/bash
# Paper B, B-1 (DEV CURVE) on M3: the P1_dev recipe (S5 §5) retrained at 5 nested levels x seeds 42, 43, 44 and
# decoded on KTVIC dev300 only; Step 0 and a zero-shot decode; then kit-B scoring and the registered decide, once.
# Prereg manuscript/prereg/2026-10-28_b1_scaling/PREREG.md (CC-126 W11, PI-1026ac Q7). Never a test split.
# Cap: 20 GPU-h over the GPU steps (train, decode), counted as step wall time in gpu_seconds.tsv; every GPU step
# runs under `timeout` with the time left; a timeout is a CAP STOP, final: CAP_STOP.json, no GPU step after it,
# then score and decide on what exists. Any other failure is a JOB STOP back to the judge. Resume-safe: a step whose
# output exists is skipped, training resumes from the hook's checkpoints, nothing is overwritten.
# Usage, inside tmux on M3 (the laptop chain uploads s5_preds/ and starts it):
#   bash scripts/b1_scaling/b1_job.sh <expected 40-hex HEAD>
EXPECT=${1:?usage: b1_job.sh <expected HEAD>}
cd /root/vsps || exit 1
. .venv/bin/activate
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
unset NCS_DATASET RESCAP_RAW_TONE RESCAP_G1_BYTE_CHECK RESCAP_SAVE_STEPS RESCAP_SAVE_LIMIT RESCAP_MIRROR_ROOT
set -o pipefail
B1=scripts/b1_scaling/b1.py; JOB=scripts/b1_scaling/b1_job.sh; KIT=scripts/kit_b
O=/root/outputs/b1_scaling; D=$O/data; LOG=$O/logs; USED=$O/gpu_seconds.tsv; MARK=$O/CAP_STOP.json; LOCK=$O/RUNNING
VS_FREEZE=7332d343173e5681365cf6871671e36209c77803a1b2db70da1cc766d5c943ed   # setup_gpu.sh H_VS = S5's venv pins
# Amendment 3 (STOP-M4-3): kit B imports scipy, which .venv lacks; every kit-B step runs in the scoring venv, as c2_job.sh
SC=/root/venv-c1score/bin/python
SC_FREEZE=4b81b6b6a549771115529e6900b9589835cdbfff0c6acf179aef53d283b744d5   # setup_gpu.sh H_C1 (numpy, scipy)
N2=$O/s5_preds/p1dev_s42_redecode-dev300-short.preds.json   # = the registered n2 preds (1e183383), Step 0
mkdir -p $O $D $LOG
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*" | tee -a $LOG/job.log; }
stop() { say "JOB STOP $*"; exit 1; }
python $B1 lock --path $LOCK || exit 1   # tmux only, no cen* session, no other /root/outputs/*/RUNNING; O_EXCL
trap 'rm -f $LOCK' EXIT

# ---------------------------------------------------------------- preflight (PREREG §1.2)
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
sha256sum --quiet -c scripts/b1_scaling/SHA256SUMS || stop "scripts/b1_scaling/SHA256SUMS does not verify"
[ "$(pip freeze | sha256sum | cut -c1-64)" = $VS_FREEZE ] || stop ".venv freeze differs from H_VS"
[ "$(/root/venv-c1score/bin/pip freeze | sha256sum | cut -c1-64)" = $SC_FREEZE ] || stop "scoring venv differs from H_C1"
# CC-128 W1: the resume hook (S5 pin 05466ef5 = scripts/checkpoint_resume_hook.py) is the .venv sitecustomize
HOOK=/root/vsps/.venv/lib/python3.10/site-packages/sitecustomize.py
HOOK_SHA=05466ef5ed3bef2b732ccd01f530a8c977c4c822ef8619b0238f562fb11e5895
[ -e $HOOK ] && [ "$(sha256sum $HOOK | cut -c1-64)" = $HOOK_SHA ] \
  || stop "resume hook not installed at $HOOK (b1_chain.sh stage)"
python $B1 --selftest >> $LOG/selftest.log 2>&1 || stop "b1 selftest"
$SC $B1 --selftest-kit >> $LOG/selftest.log 2>&1 || stop "b1 kit selftest (scoring venv)"
java -version 2>&1 | grep -q '11.0.32.1' || stop "Java is not openjdk 11.0.32.1 (kit B segmenter)"
python $B1 check --machine --job $JOB >> $LOG/check.log 2>&1 \
  || stop "b1 check (prereg, lists, code, weights, train_data.json, job)"
$SC $B1 check --kit-b $KIT >> $LOG/check.log 2>&1 || stop "b1 check kit B (scoring venv)"
G() { python $B1 guard --head "$EXPECT" >> $LOG/guard.log 2>&1 || stop "guard (host, GPU, C-EN, locks, test files)"; }
G
sha256sum $B1 $JOB scripts/b1_scaling/SHA256SUMS > $O/code_at_start.sha256
say "JOB START head $EXPECT"

cap_stop() {  # final: no GPU step after it
  [ -e $MARK ] || printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > $MARK
  say "CAP STOP $1"; finish; }
step() {  # step NAME CMD...: one GPU step under the time left; its wall seconds are added to gpu_seconds.tsv
  local name=$1; shift
  local t; t=$(python $B1 left --used $USED --marker $MARK) || stop "cap arithmetic"
  [ "$t" -gt 0 ] || cap_stop "20 GPU-h cap before $name"
  G; say "START $name (left $((t / 60)) min)"
  local t0; t0=$(date +%s)
  echo "$name start $t0" >> $USED   # CC-128 W6: a reboot mid-step is charged from here (b1.py used_seconds)
  timeout ${t}s "$@" >> $LOG/$name.log 2>&1; local rc=$?
  echo "$name $(( $(date +%s) - t0 ))" >> $USED
  [ $rc = 0 ] && { say "OK $name"; return 0; }
  [ $rc = 124 ] && cap_stop "20 GPU-h cap reached during $name"
  stop "$name rc=$rc"
}
decode() {  # decode NAME [ADAPTER]: greedy short-prompt dev300 decode by evaluate.py (bf16, its defaults)
  local res=$O/$1-dev300-short.json; local ad=(); [ -n "${2:-}" ] && ad=(--adapter "$2")
  [ -s $res ] && return 0
  if [ -s ${res%.json}.preds.json ]; then  # decoded but not scored: evaluate.py's recovery, never a second decode
    NCS_DATASET=ktvic_dev python scripts/evaluate.py --predictions ${res%.json}.preds.json --split dev_data.json \
      --prompt short --name $1-dev300-short --out $res >> $LOG/dec_$1.log 2>&1 || stop "rescore $1"
  else
    step dec_$1 env NCS_DATASET=ktvic_dev python scripts/evaluate.py --model qwen2.5-vl-7b "${ad[@]}" \
      --split dev_data.json --prompt short --name $1-dev300-short --out $res
  fi
}
finish() {  # CPU: kit-B score of whatever exists, then the registered decide once; mirror sums
  [ -e $O/ledger.json ] || $SC $B1 score --dir $O --kit-b $KIT --out $O/ledger.json >> $LOG/score.log 2>&1 \
    || stop "score"
  [ -e $O/decide.json ] || python $B1 decide --ledger $O/ledger.json --out $O/decide.json >> $LOG/decide.log 2>&1 \
    || stop "decide"
  (cd $O && find . -type f ! -name 'SHA256SUMS*' ! -name RUNNING ! -name '*.partial*' | sort | xargs sha256sum) \
    > $O/SHA256SUMS
  say "BLOCK DONE gpu_h $(awk '{s += $2} END {printf "%.2f", s / 3600}' $USED)"
  exit 0
}

# ---------------------------------------------------------------- data (CPU): ids, dev300 dataset, SFT rows
for f in p1dev_s42_f25 p1dev_s42_f50 p1dev_s42_redecode; do [ -s $O/s5_preds/$f-dev300-short.preds.json ] \
  || stop "S5 preds $f not uploaded"; done
python $B1 ids --dir $D || stop "ids"
python scripts/ktvic_dev_split.py --verify --json-dir $NCS_DATA/datasets/ktvic_dev >> $LOG/data.log 2>&1 \
  || stop "dev300 split"
for lv in L1 L2 L3 L4 L5; do
  [ -s $D/gold_b1_$lv/sft.jsonl ] || python scripts/build_gold_sft.py --annotations \
    $NCS_DATA/datasets/ktvic/train_data.json --out $D/gold_b1_$lv \
    --images-file $D/ktvic_train_minus_dev300_${lv}_s42.txt >> $LOG/data.log 2>&1 || stop "build_gold_sft $lv"
done
python $B1 sft --dir $D >> $LOG/data.log 2>&1 || stop "sft.jsonl pins (L3-L5 = S5's; L1/L2 recorded once)"

# ---------------------------------------------------------------- GPU: Step 0, zero-shot, 15 points (seed-major)
decode b1_step0_p1dev_s42 $NCS_DATA/runs/p1dev_s42
python $B1 step0 --redecode $O/b1_step0_p1dev_s42-dev300-short.preds.json --n2 $N2 > $O/step0.json 2>> $LOG/job.log \
  || stop "Step 0: fewer than 95% identical captions to the registered n2 decode"
decode b1_zeroshot
for S in 42 43 44; do
  for lv in L1 L2 L3 L4 L5; do
    R=b1_s${S}_$lv; RUN=$NCS_DATA/runs/$R
    if [ ! -s $RUN/metrics.jsonl ]; then
      step train_$R python scripts/train_stage2.py --stage sft --data $D/gold_b1_$lv --out $RUN \
        --epochs 2 --seed $S --loss-mask assistant
    fi
    for want in "loss mask: assistant" "save_steps=200" "512 vision tokens, 4-bit"; do
      grep -q "$want" $LOG/train_$R.log || stop "$R: '$want' not in its training log"
    done
    decode $R $RUN
  done
done
finish
