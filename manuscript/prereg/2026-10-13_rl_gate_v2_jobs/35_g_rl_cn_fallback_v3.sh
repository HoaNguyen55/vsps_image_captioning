cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -e
# CN-RLOO pilot fallback (judges D1e, D1f; pre-registered in manuscript/prereg/2026-10-13_rl_gate_v2.md). Runs only
# after a CLEAN kill at look 1 (the run moved, final KL >= 0.2 nat, and every guard held) of the first look, or of its
# lr 5e-5 rerun when the first look was under-moved. Then one CN arm at the OTHER temperature: T = 0.8 after a T = 1.0
# first look (35_e_rl_cn_v3), T = 1.0 after a T = 0.8 first look (35_e_rl_cn_t08first_v3). Sampler, policy and
# reference log-probs share that temperature; 35_e's settings otherwise; a fresh dry run first; gate v2, whose copy-rate
# baseline is G0 at T = 1.0 and the arm's own first 250 images at T = 0.8. Any other outcome: nothing to do.
# No first look or two, or a missing or unknown verdict, stop the job before any GPU command. Dev only. ~3.5 GPU-h.
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
python scripts/ktvic_dev_split.py --verify
R=p1dev_s42; RL=$NCS_DATA/rl; G=$RL/g0; P1=$RL/$R-dev300-short.json
if [ -e $RL/g1_cn_v3_s42 ] && [ ! -e $RL/g1_cn_t08_v3_s42 ]; then TAG=; FT=0.8; FTAG=_t08
elif [ -e $RL/g1_cn_t08_v3_s42 ] && [ ! -e $RL/g1_cn_v3_s42 ]; then TAG=_t08; FT=1.0; FTAG=
else echo "STOP: need exactly one first look (g1_cn_v3_s42 or g1_cn_t08_v3_s42)"; exit 1; fi
python scripts/rl_report.py --floor $P1
FINAL=$RL/g1_cn${TAG}_v3_s42/gate.json
if python -c "import json, sys; sys.exit(0 if json.load(open('$FINAL'))['verdict'] == 'under-moved' else 1)"; then
  FINAL=$RL/g1_cn${TAG}_v3_lr5e-5_s42/gate.json
fi
CLEAN=$(python -c "import json; g = json.load(open('$FINAL')); v = g.get('verdict'); assert v in ('pass', 'grey', 'under-moved', 'kill'), v; print(int(v == 'kill' and g['clean_kill']))")
echo "35_g: first-look verdict read from $FINAL, clean kill: $CLEAN"
if [ "$CLEAN" != 1 ]; then echo "SKIP 35_g: no clean kill of the first look (judge D1e)"; exit 0; fi
O=$RL/g1_cn${FTAG}_v3_s42
TAU=$(python -c "import json; print(json.load(open('$G/g0_report.json'))['tau'])")
A="--adapter $NCS_DATA/runs/$R --images-file data/splits/ktvic_train_minus_dev300.txt --dev-file data/splits/ktvic_dev300.txt --tau $TAU --k 8 --beta 0.03 --lr 2e-5 --seed 42 --micro 4 --temperature $FT"
python scripts/train_rl.py $A --dry-run --out $RL/dryrun_cn${FTAG}_v3_s42 --n-images 20 --dev-limit 20 --eval-every 20
python scripts/train_rl.py $A --out $O --n-images 1000 --eval-every 250
NCS_DATASET=ktvic_dev timeout 3600 python scripts/evaluate.py --model qwen2.5-vl-7b --adapter $O/last \
  --split dev_data.json --prompt short --name g1_cn${FTAG}_v3_s42-dev300-short --out $RL/g1_cn${FTAG}_v3_s42-dev300-short.json
python scripts/rl_report.py --gate $O --p1dev $P1 --rl $RL/g1_cn${FTAG}_v3_s42-dev300-short.json --g0-report $G/g0_report.json
nice -n 10 python scripts/rl_report.py --panel $P1 $RL/g1_cn${FTAG}_v3_s42-dev300-short.json --out $O/panel.json
python -c "import json; g = json.load(open('$O/gate.json')); print('fallback (T = $FT) verdict:', g['verdict'], '| dev gain', g['dev_gain_x100_mean_lo_hi'])"
