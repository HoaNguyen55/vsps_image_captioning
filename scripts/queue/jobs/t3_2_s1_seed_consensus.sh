cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -eo pipefail
# Tier-3 T3.2 / S1 (PD-9 Q1), pre-registered in manuscript/prereg/2026-10-18_tier3_S1.{md,json}; the instrument
# addendum manuscript/prereg/2026-10-18_tier3_S1_instrument.json pins this file and scripts/seed_consensus.py.
# Step 0 re-decodes p1dev_s42 on dev300 on this machine. p1dev_s43 and p1dev_s44 are trained with job 35_a's recipe
# (only R and --seed change; gold_p1dev is the 35_a build, sha-checked, not rebuilt). The delta-space soup of the three
# adapters is built and self-checked on CPU before any further decode; s43, s44 and the soup are decoded on dev300
# (evaluate.py, short prompt, bf16, its defaults); the cross-seed MBR caption is picked and scored; the gate follows.
# dev300 only, no test look; about 4.0 GPU-h. Results: /root/outputs/t3_2_s1_seed_consensus (backed up). Adapters:
# $NCS_DATA/runs, final files copied to /root/outputs/runs. A step whose output exists is skipped (resume after a
# restart); nothing is overwritten.
export HF_HUB_OFFLINE=1  # the base loads from the cached snapshot, whose revision seed_consensus.py check pins
SC=scripts/seed_consensus.py
echo "2b72dc417d60c5ec6a0be9cfd3b69692a783e2ba9bd1fc7dcb14c5195296c486  $SC" | sha256sum -c -
grep -q "$(sha256sum "$0" | cut -c1-64)" manuscript/prereg/2026-10-18_tier3_S1_instrument.json
python scripts/queue/check_g1_pass.py
O=/root/outputs/t3_2_s1_seed_consensus; mkdir -p $O
python $SC --selftest
python $SC check --out $O/check.json
python scripts/ktvic_dev_split.py --verify --json-dir $NCS_DATA/datasets/ktvic_dev
python scripts/ktvic_dev_split.py --sft $NCS_DATA/gold_p1dev/sft.jsonl
dev() {  # $1 run under $NCS_DATA/runs, $2 result name: greedy dev300 decode; captions kept if scoring has to be redone
  [ -e $O/$2.preds.json ] || NCS_DATASET=ktvic_dev timeout 3600 python scripts/evaluate.py --model qwen2.5-vl-7b \
    --adapter $NCS_DATA/runs/$1 --split dev_data.json --prompt short --name $2 --out $O/$2.json
  [ -e $O/$2.json ] || NCS_DATASET=ktvic_dev python scripts/evaluate.py --predictions $O/$2.preds.json \
    --split dev_data.json --prompt short --name $2 --out $O/$2.json
}
keep() {  # the final adapter into the backed-up mirror, never over an existing copy
  mkdir -p /root/outputs/runs/$1
  cp -n $NCS_DATA/runs/$1/adapter_model.safetensors $NCS_DATA/runs/$1/adapter_config.json /root/outputs/runs/$1/
}
dev p1dev_s42 p1dev_s42_redecode-dev300-short  # step 0, before any training
for s in 43 44; do
  R=p1dev_s$s
  [ -e $NCS_DATA/runs/$R/metrics.jsonl ] || python scripts/train_stage2.py --stage sft --data $NCS_DATA/gold_p1dev \
    --out $NCS_DATA/runs/$R --epochs 2 --seed $s --loss-mask assistant 2>&1 | tee -a $O/train_$R.log
  grep -q "loss mask: assistant" $O/train_$R.log
  keep $R
done
S=p1dev_soup3_s42s43s44
[ -e $O/soup_selfcheck.json ] || CUDA_VISIBLE_DEVICES= python $SC soup --runs $NCS_DATA/runs --report $O/soup_selfcheck.json
python -c "import json, sys; sys.exit(0 if json.load(open('$O/soup_selfcheck.json'))['self_check_pass'] else 1)"
keep $S
for R in p1dev_s43 p1dev_s44 $S; do dev $R $R-dev300-short; done
M=p1dev_mbr3-dev300-short
[ -e $O/$M.preds.json ] || python $SC mbr --dir $O
[ -e $O/$M.json ] || NCS_DATASET=ktvic_dev python scripts/evaluate.py --predictions $O/$M.preds.json \
  --split dev_data.json --prompt short --name $M --out $O/$M.json
[ -e $O/gate.json ] || python $SC gate --dir $O
F=$O/SHA256SUMS; n=2; while [ -e $F ]; do F=$O/SHA256SUMS_v$n; n=$((n + 1)); done
{ find $O -type f ! -name 'SHA256SUMS*' -print0 | sort -z | xargs -0 sha256sum
  sha256sum $NCS_DATA/runs/{p1dev_s43,p1dev_s44,$S}/adapter_{model.safetensors,config.json}; } > $F
python -c "import json; g = json.load(open('$O/gate.json')); print('S1', g['verdict'], g['carried'], g['D_cider_x100_mean_lo_hi'], g['dCHAIR_i_points'])"
