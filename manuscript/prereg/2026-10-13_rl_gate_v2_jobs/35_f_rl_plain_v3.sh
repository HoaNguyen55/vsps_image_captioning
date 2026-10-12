cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -e
# CN-RLOO pilot, follow-up of the first look's gate-v2 verdict (judges D1e, D1f; pre-registered in
# manuscript/prereg/2026-10-13_rl_gate_v2.md). The first look is whichever of 35_e_rl_cn_v3 (T = 1.0, run g1_cn_v3_s42)
# and 35_e_rl_cn_t08first_v3 (T = 0.8, run g1_cn_t08_v3_s42) ran. Every run here keeps that temperature and 35_e's
# settings unless stated, and is judged by gate v2 on its last checkpoint (evaluate.py on dev). Dev only, no test decode.
# - pass: the plain-RLOO arm (--no-copy-mask, 1,000 images), then CN vs plain: the copy mask is claimed only if
#   CN - plain >= +3.0 with a paired 95% lower bound > 0 (both at 1,000 images). ~3.5 GPU-h.
# - grey: the one extension of the first look to all 3,469 train-minus-dev images (--resume: the policy continues, the
#   KL anchor stays P1_dev), judged with --look 2 (pass or kill). Only a look-2 pass is followed by the plain arm and
#   CN vs plain as above (judge D1f). ~6.9 GPU-h, ~10.4 with the plain arm.
# - under-moved (final KL < 0.2 nat with every guard holding): the one CN rerun at lr 5e-5, 1,000 images. ~3.5 GPU-h.
# - kill: nothing here; the fallback at the other temperature after a clean kill is 35_g.
# No first look or two, a missing or unknown verdict, a failed first-look dry run or P1_dev below the floor stop the
# job before any GPU command.
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
python scripts/ktvic_dev_split.py --verify
R=p1dev_s42; RL=$NCS_DATA/rl; G=$RL/g0; P1=$RL/$R-dev300-short.json
if [ -e $RL/g1_cn_v3_s42 ] && [ ! -e $RL/g1_cn_t08_v3_s42 ]; then T=1.0; TAG=
elif [ -e $RL/g1_cn_t08_v3_s42 ] && [ ! -e $RL/g1_cn_v3_s42 ]; then T=0.8; TAG=_t08
else echo "STOP: need exactly one first look (g1_cn_v3_s42 or g1_cn_t08_v3_s42)"; exit 1; fi
CN=$RL/g1_cn${TAG}_v3_s42
python -c "import json; c = json.load(open('$RL/dryrun_cn${TAG}_v3_s42/c3.json')); assert c['pass'], c['checks']; print('first-look C3 dry run passed (T = $T)')"
python scripts/rl_report.py --floor $P1
VERDICT=$(python -c "import json; v = json.load(open('$CN/gate.json')).get('verdict'); assert v in ('pass', 'grey', 'under-moved', 'kill'), v; print(v)")
TAU=$(python -c "import json; print(json.load(open('$G/g0_report.json'))['tau'])")
A="--adapter $NCS_DATA/runs/$R --images-file data/splits/ktvic_train_minus_dev300.txt --dev-file data/splits/ktvic_dev300.txt --tau $TAU --k 8 --beta 0.03 --seed 42 --micro 4 --temperature $T --eval-every 250"
judge() {  # RUN NAME LOOK: evaluate.py on RUN/last (dev), gate v2, OpenViIC panel
  NCS_DATASET=ktvic_dev timeout 3600 python scripts/evaluate.py --model qwen2.5-vl-7b --adapter $1/last \
    --split dev_data.json --prompt short --name $2 --out $RL/$2.json
  python scripts/rl_report.py --gate $1 --p1dev $P1 --rl $RL/$2.json --g0-report $G/g0_report.json --look $3
  nice -n 10 python scripts/rl_report.py --panel $P1 $RL/$2.json --out $1/panel.json
}
case $VERDICT in
  under-moved)
    echo "35_f branch: the one CN rerun at lr 5e-5, T = $T (first-look verdict: $VERDICT)"
    python scripts/train_rl.py $A --lr 5e-5 --n-images 1000 --out $RL/g1_cn${TAG}_v3_lr5e-5_s42
    judge $RL/g1_cn${TAG}_v3_lr5e-5_s42 g1_cn${TAG}_v3_lr5e-5_s42-dev300-short 1 ;;
  pass|grey)
    if [ $VERDICT = grey ]; then
      echo "35_f branch: the one CN extension to 3,469 images, T = $T, look 2 (first-look verdict: $VERDICT)"
      python scripts/train_rl.py $A --lr 2e-5 --n-images 3469 --resume $CN --out $RL/g1_cn${TAG}_v3_ext_s42
      judge $RL/g1_cn${TAG}_v3_ext_s42 g1_cn${TAG}_v3_ext_s42-dev300-short 2
      LOOK2=$(python -c "import json; print(json.load(open('$RL/g1_cn${TAG}_v3_ext_s42/gate.json'))['verdict'])")
      if [ "$LOOK2" != pass ]; then echo "35_f: look-2 verdict $LOOK2, so no plain-RLOO arm (judge D1f)"; exit 0; fi
    fi
    echo "35_f branch: the plain-RLOO arm, T = $T (first-look verdict: $VERDICT)"
    python scripts/train_rl.py $A --lr 2e-5 --n-images 1000 --no-copy-mask --out $RL/g1_plain${TAG}_v3_s42
    judge $RL/g1_plain${TAG}_v3_s42 g1_plain${TAG}_v3_s42-dev300-short 1
    python scripts/rl_report.py --compare $CN/gate.json $RL/g1_plain${TAG}_v3_s42/gate.json --out $RL/g1_compare${TAG}_v3_s42.json ;;
  kill)
    echo "35_f branch: none (first-look verdict: $VERDICT; the fallback after a clean kill is 35_g)" ;;
esac
