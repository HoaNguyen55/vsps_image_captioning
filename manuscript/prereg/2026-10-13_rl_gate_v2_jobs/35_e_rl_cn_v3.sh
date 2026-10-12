cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -e
# CN-RLOO pilot, FIRST LOOK (judges D1e, D1f; pre-registered in manuscript/prereg/2026-10-13_rl_gate_v2.md, committed
# before any output of this job). Two copies differ only in the T= line below: 35_e_rl_cn_v3.sh (T = 1.0) and
# 35_e_rl_cn_t08first_v3.sh (T = 0.8). Exactly one is queued, after 36_z_dev_samples (D9 step A) and D9's reading:
# the T = 0.8 copy if the R0 pick's dev panel CIDEr-D gain at T = 0.8 has a paired 95% CI above 0, else the T = 1.0
# copy. Either stops before any GPU command once a first look exists. The other temperature is the fallback after a
# clean kill (35_g).
# CN arm from P1_dev: the first 1,000 images of the seed-42 order of train minus dev, k=8, beta 0.03, lr 2e-5, 5 images
# per step, tau from 35_b, the fragment guard (END from train minus dev300: a rollout whose last word ends no reference
# gets a non-positive advantage), sampling and every log-prob at temperature T, the v2 memory fix (--micro 4,
# last-position logits, expandable_segments). A fresh 20-image C3 dry run first; it fails the job within minutes.
# Gate v2 judges the LAST checkpoint, decoded by evaluate.py (bf16) on the 300 dev images, against P1_dev (144.33):
# pass / grey / under-moved / kill, the same at both temperatures except the copy-rate baseline (G0 at T = 1.0, the
# arm's own first 250 images at T = 0.8). In-run 4-bit dev scores are monitoring only. No test decode. ~3.5 GPU-h.
T=1.0; TAG=
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
python scripts/ktvic_dev_split.py --verify
R=p1dev_s42; RL=$NCS_DATA/rl; G=$RL/g0; O=$RL/g1_cn${TAG}_v3_s42; P1=$RL/$R-dev300-short.json
if [ -e $RL/g1_cn_v3_s42 ] || [ -e $RL/g1_cn_t08_v3_s42 ]; then echo "STOP: a first look already exists (judge D1f)"; exit 1; fi
python scripts/rl_report.py --floor $P1
TAU=$(python -c "import json; print(json.load(open('$G/g0_report.json'))['tau'])")
A="--adapter $NCS_DATA/runs/$R --images-file data/splits/ktvic_train_minus_dev300.txt --dev-file data/splits/ktvic_dev300.txt --tau $TAU --k 8 --beta 0.03 --lr 2e-5 --seed 42 --micro 4 --temperature $T"
python scripts/train_rl.py $A --dry-run --out $RL/dryrun_cn${TAG}_v3_s42 --n-images 20 --dev-limit 20 --eval-every 20
python scripts/train_rl.py $A --out $O --n-images 1000 --eval-every 250
NCS_DATASET=ktvic_dev timeout 3600 python scripts/evaluate.py --model qwen2.5-vl-7b --adapter $O/last \
  --split dev_data.json --prompt short --name g1_cn${TAG}_v3_s42-dev300-short --out $RL/g1_cn${TAG}_v3_s42-dev300-short.json
python scripts/rl_report.py --gate $O --p1dev $P1 --rl $RL/g1_cn${TAG}_v3_s42-dev300-short.json --g0-report $G/g0_report.json
nice -n 10 python scripts/rl_report.py --panel $P1 $RL/g1_cn${TAG}_v3_s42-dev300-short.json --out $O/panel.json
python -c "import json; g = json.load(open('$O/gate.json')); print('first look (T = $T) verdict:', g['verdict'], '| clean kill:', g['clean_kill'], '| dev gain', g['dev_gain_x100_mean_lo_hi'])"
