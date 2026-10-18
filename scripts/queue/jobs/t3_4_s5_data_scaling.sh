SELF=$(readlink -f "$0")
cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -eo pipefail
# Tier-3 T3.4 = S5 (GPU_JOB_PLAN_v1; PD-9 Q1: diagnostic only, no selection, no claim, no gate on any other job): the
# P1_dev recipe (job 35_a) on nested 25% / 50% subsets of KTVIC train minus dev300; p1dev_s42 is the 100% point.
# dev300 only, no test decode; ~1.8 GPU-h. Registered in manuscript/prereg/2026-10-18_tier3_S5.{md,json}; this file
# and scripts/scaling_probe.py are pinned in manuscript/prereg/2026-10-18_tier3_S5_instrument.json. Resume-safe: a
# step whose output exists is skipped, training resumes from the hook's checkpoints (save_steps 200), and nothing is
# overwritten.
unset NCS_DATASET RESCAP_RAW_TONE RESCAP_G1_BYTE_CHECK RESCAP_SAVE_STEPS RESCAP_SAVE_LIMIT RESCAP_MIRROR_ROOT
export HF_HUB_OFFLINE=1
JOB=scripts/queue/jobs/t3_4_s5_data_scaling.sh; SP=scripts/scaling_probe.py
PINS=manuscript/prereg/2026-10-18_tier3_S5_instrument.json
cmp "$SELF" $JOB
git ls-files --error-unmatch $JOB $SP $PINS > /dev/null
git diff --quiet HEAD -- $JOB $SP $PINS
for f in $JOB $SP; do grep -q "$(sha256sum $f | cut -c1-64)" $PINS; done
python scripts/queue/check_g1_pass.py
python $SP --check --machine --instrument
python $SP --selftest
O=/root/outputs/t3_4_s5_data_scaling; D=$O/data; mkdir -p $O
python $SP --subsets $D --instrument
python scripts/ktvic_dev_split.py --verify --json-dir $NCS_DATA/datasets/ktvic_dev
for k in f25 f50; do
  if [ ! -s $D/gold_p1dev_$k/sft.jsonl ]; then
    python scripts/build_gold_sft.py --annotations $NCS_DATA/datasets/ktvic/train_data.json --out $D/gold_p1dev_$k \
      --images-file $D/ktvic_train_minus_dev300_${k}_s42.txt
  fi
done
(cd $D && sha256sum -c registered.sha256)

decode() {  # $1 name, $2 adapter: greedy short-prompt decode of dev300 by evaluate.py (bf16, its defaults)
  local res=$O/$1-dev300-short.json
  if [ -s $res ]; then
    return 0
  elif [ -s ${res%.json}.preds.json ]; then  # decoded but not scored: evaluate.py's recovery, never a second decode
    NCS_DATASET=ktvic_dev python scripts/evaluate.py --predictions ${res%.json}.preds.json --split dev_data.json \
      --prompt short --name $1-dev300-short --out $res
  else
    NCS_DATASET=ktvic_dev timeout 3600 python scripts/evaluate.py --model qwen2.5-vl-7b --adapter $2 \
      --split dev_data.json --prompt short --name $1-dev300-short --out $res
  fi
}
decode p1dev_s42_redecode $NCS_DATA/runs/p1dev_s42
for k in f25 f50; do
  R=p1dev_s42_$k; L=$O/train_$R.log
  if [ ! -s $NCS_DATA/runs/$R/metrics.jsonl ]; then
    python scripts/train_stage2.py --stage sft --data $D/gold_p1dev_$k --out $NCS_DATA/runs/$R \
      --epochs 2 --seed 42 --loss-mask assistant 2>&1 | tee -a $L
  fi
  grep -q "loss mask: assistant" $L
  grep -q "save_steps=200" $L
  grep -q "512 vision tokens, 4-bit" $L
  decode $R $NCS_DATA/runs/$R
done
[ -e $O/scaling.json ] || python $SP --analyse $O
if [ ! -e $O/SHA256SUMS ]; then
  (cd $O && find . -type f ! -name 'SHA256SUMS*' | sort | xargs sha256sum) > $O/SHA256SUMS.part
  for R in p1dev_s42_f25 p1dev_s42_f50; do
    sha256sum $NCS_DATA/runs/$R/{adapter_model.safetensors,adapter_config.json,metrics.jsonl,resume_manifest.json}
  done >> $O/SHA256SUMS.part
  mv $O/SHA256SUMS.part $O/SHA256SUMS
fi
python -c "import json, sys; print(json.load(open(sys.argv[1]))['decision'])" $O/scaling.json
