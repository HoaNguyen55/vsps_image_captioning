cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -eo pipefail
# Judge D10 (ii): PLAN-F1 dev300 pilot, pre-registered in manuscript/prereg/2026-10-13_plan_f1.md
# (committed through the gatekeeper before this job is queued on n3).
# 1. Preconditions: frozen sha256s of plan_f1.py, rescap/chair.py, evaluate.py, upe_mbr.py and the P1_dev dev300 inputs;
#    T* = 0.5; C1 dev split check + evaluate.py dataset at $NCS_DATA/datasets/ktvic_dev; plan_f1.py --self-check.
# 2. Data (CPU): deterministic rebuild of P1_dev's 3,469 train-minus-dev300 SFT rows (sha256 asserted), then
#    plan_f1.py realiser-data appends each target caption's own object list (sha256 and C1 disjointness asserted).
# 3. Plan (CPU): 5-fold cross-fitted posterior + corpus plug-in fixed point (cap 3) on P1_dev's greedy + 12 samples.
# 4. Train (GPU, ~1.75 GPU-h): P1_dev's exact 35_a SFT recipe (--epochs 2 --seed 42 --loss-mask assistant).
# 5. Decode (GPU, ~0.12 GPU-h): evaluate.py --tags $O/plan_dev.json on the 300 dev images.
# 6. Score (CPU): UPE dev picks at T*=0.5, evaluate.py --predictions for greedy and UPE, then plan_f1.py score (K1-K3).
G=$NCS_DATA/rl/p1dev_s42-dev300-short.preds.json
S05=data/results/upe/p1dev_s42-dev300-short-T0.5.jsonl
S08=data/results/upe/p1dev_s42-dev300-short-T0.8.jsonl
O=$NCS_DATA/results/planf1_dev
mkdir -p $O

grep -q "$(sha256sum scripts/plan_f1.py | cut -c1-64)" manuscript/prereg/2026-10-13_plan_f1.md
sha256sum -c - <<EOF
b06a25dc7cecae168d4f7229c3be15702789ec61d51a2f240a3abb431a962bcc  scripts/plan_f1.py
fd1d012398cae5d1984bb4effdf18919e157f1c770b8a13adbb070a8b659ec6b  rescap/chair.py
a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236  scripts/evaluate.py
4a65d3a910029ceb21d8b9625f5f9832e1a27e289748f1354ce5555d4abca19b  scripts/upe_mbr.py
1e161947087e90e58958399f59353433aa1d578dfcd578bfa55472d4de568603  data/results/upe/upe_choose_t.json
876a1d420c20d06ae388613beb8e30eb6fab5d4380ee13b26bbfa8eede5bea26  $S05
60ebd6403910837ed4ed036f70458a5cfdba92923238f8d4167a0d941460cf05  $S08
1e183383e91daf32f4683fbea2bdb09d24b7deba956343ca16ef332014cba84b  $G
EOF
[ "$(cat data/results/upe/upe_temperature.txt 2>/dev/null)" = "0.5" ] || {
  echo "expected T*=0.5 in data/results/upe/upe_temperature.txt"; exit 1
}
python scripts/ktvic_dev_split.py --verify --json-dir $NCS_DATA/datasets/ktvic_dev
python scripts/plan_f1.py --self-check

python scripts/build_gold_sft.py --annotations $NCS_DATA/datasets/ktvic/train_data.json \
  --out $NCS_DATA/gold_planf1/base --images-file data/splits/ktvic_train_minus_dev300.txt
echo "971879742e85d710fc828fa526b735d0c0b6469b4988e3d5402a26fb1b666f16  $NCS_DATA/gold_planf1/base/sft.jsonl" | sha256sum -c -
python scripts/plan_f1.py realiser-data --sft $NCS_DATA/gold_planf1/base/sft.jsonl --out $NCS_DATA/gold_planf1
echo "0dd84b27bebe8ebb7a006bc850ec118f7cf508b12e58486c4200f01c63cc4527  $NCS_DATA/gold_planf1/sft.jsonl" | sha256sum -c -
python scripts/ktvic_dev_split.py --sft $NCS_DATA/gold_planf1/sft.jsonl

python scripts/plan_f1.py plan --split dev --greedy $G --samples $S05 $S08 --out $O/plan_dev.json
echo "58ecef13ef3b1b31531c617b140f7934b1a8e218b4a931b6e889a7a06ea3a14f  $O/plan_dev.json" | sha256sum -c -

timeout 14400 python scripts/train_stage2.py --stage sft --data $NCS_DATA/gold_planf1 \
  --out $NCS_DATA/runs/planf1_s42 --epochs 2 --seed 42 --loss-mask assistant 2>&1 | tee $O/train_planf1_s42.log
grep -q "loss mask: assistant" $O/train_planf1_s42.log
grep -q "training set: 3469 examples" $O/train_planf1_s42.log
[ -s $NCS_DATA/runs/planf1_s42/adapter_model.safetensors ] || { echo "missing adapter planf1_s42"; exit 1; }

NCS_DATASET=ktvic_dev timeout 3600 python scripts/evaluate.py --model qwen2.5-vl-7b \
  --adapter $NCS_DATA/runs/planf1_s42 --split dev_data.json --prompt short --tags $O/plan_dev.json \
  --name planf1_s42-dev300-short --out $O/planf1_s42-dev300-short.json
[ -s $O/planf1_s42-dev300-short.preds.json ] || { echo "missing realised dev predictions"; exit 1; }
[ -s $O/planf1_s42-dev300-short.json ] || { echo "missing realised dev evaluation"; exit 1; }

nice -n 10 python scripts/plan_f1.py upe --split dev --greedy $G --samples $S05 \
  --out $O/upe_t05-dev300-short.preds.json
NCS_DATASET=ktvic_dev nice -n 10 python scripts/evaluate.py --predictions $G --split dev_data.json \
  --prompt short --name p1dev_s42-dev300-short --out $O/p1dev_s42-dev300-short.json
NCS_DATASET=ktvic_dev nice -n 10 python scripts/evaluate.py \
  --predictions $O/upe_t05-dev300-short.preds.json --split dev_data.json \
  --prompt short --name upe_t05-dev300-short --out $O/upe_t05-dev300-short.json
nice -n 10 python scripts/plan_f1.py score --split dev --plan $O/plan_dev.json --greedy $G \
  --upe $O/upe_t05-dev300-short.preds.json --realised $O/planf1_s42-dev300-short.preds.json \
  --eval greedy=$O/p1dev_s42-dev300-short.json upe=$O/upe_t05-dev300-short.json \
         realised=$O/planf1_s42-dev300-short.json \
  --out $O/score_dev.json > $O/score_dev.json
cat $O/score_dev.report.json
