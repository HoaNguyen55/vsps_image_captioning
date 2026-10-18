cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 PYTHONUNBUFFERED=1
set -eo pipefail
# Tier-3 T3.3 / S3 (PD-9 Q2): M3 count-matched DPO stage 1 (arm A, cmdpo_A_s42) and CM-RFT (arm R, cmrft_s42), with
# the A-KL fallback (cmdpo_AKL_s42) only when arm A fails guard G2 or G3. Registered in
# manuscript/prereg/2026-10-18_tier3_S3.{md,json} (a68fb66) and amendment 1 (59901cc, the H5 kill rule). The instrument
# addendum manuscript/prereg/2026-10-18_tier3_S3_instrument.json pins this file and the four S3 scripts; s3_gate.py
# --check --machine refuses to start on any other code, constant, input, adapter or base-shard sha. Preference data
# and RFT targets come from the 1,000 registered RL images (KTVIC train minus dev300); the gate is on dev300; there is
# no test look. Order: step 0 (P1_dev re-decoded on dev300 on this machine), the 6 + 6 sample pool, P1_dev's greedy
# decode of the RL images, pairs and RFT targets (CPU), the 20-pair dry run, CM-DPO, CM-RFT, decodes (dev300 and the
# first 250 RL images), the JVM half of the gate, the A-KL trigger, the verdict. About 5.5-6 GPU-h, plus about 2.3 if
# A-KL runs. Results: /root/outputs/t3_3_s3_cm_dpo_rft (backed up). Adapters: $NCS_DATA/runs; final files go to
# /root/outputs/runs, DPO checkpoints (every 200 steps) are mirrored there by train_stage2_anchor.py and SFT ones by
# the hook. A step whose output exists is skipped, so a rerun resumes; nothing is overwritten. Without the panel file
# (data/ktvic_openviic_refs.json, git-excluded) the verdicts that depend on panel_cm stay PENDING_PANEL: rerun
# s3_gate.py --verdict where the panel is, with a new --out.
export HF_HUB_OFFLINE=1  # the base loads from the cached snapshot whose revision and shard shas the check pins
grep -q "$(sha256sum "$0" | cut -c1-64)" manuscript/prereg/2026-10-18_tier3_S3_instrument.json
python scripts/queue/check_g1_pass.py
O=/root/outputs/t3_3_s3_cm_dpo_rft; R=$NCS_DATA/runs; G=scripts/s3_gate.py; mkdir -p $O
python $G --check --machine > $O/check_$(date -u +%Y%m%dT%H%M%SZ).json
python $G --selftest
python scripts/cm_rft.py --selftest
python scripts/cm_pairs.py --self-check
python scripts/train_stage2_anchor.py --selftest > $O/selftest_train_stage2_anchor_$(date -u +%Y%m%dT%H%M%SZ).log 2>&1
python scripts/ktvic_dev_split.py --verify --json-dir $NCS_DATA/datasets/ktvic_dev
python scripts/ktvic_dev_split.py --sft $NCS_DATA/gold_p1dev/sft.jsonl
python $G --prep $O
log() { echo "$(date -u +%FT%TZ) $*" >> $O/events.log; }
decode() {  # $1 run, $2 result name, $3 NCS_DATASET, $4 split: greedy short decode; captions kept if scoring is redone
  [ -e $O/$2.preds.json ] || NCS_DATASET=$3 timeout 5400 python scripts/evaluate.py --model qwen2.5-vl-7b \
    --adapter $R/$1 --split $4 --prompt short --name $2 --out $O/$2.json
  [ -e $O/$2.json ] || NCS_DATASET=$3 python scripts/evaluate.py --predictions $O/$2.preds.json --split $4 \
    --prompt short --name $2 --out $O/$2.json
}
keep() {  # $1 run: the final adapter into the backed-up mirror and its records into $O/runs, never over a copy
  mkdir -p /root/outputs/runs/$1 $O/runs/$1
  cp -n $R/$1/adapter_model.safetensors $R/$1/adapter_config.json /root/outputs/runs/$1/
  for f in train_summary.json pairs_log.jsonl metrics.jsonl resume_manifest.json; do
    if [ -e $R/$1/$f ]; then cp -n $R/$1/$f $O/runs/$1/; fi
  done
}
arm() {  # $1 arm, $2 run: the dev300 decode, the copy-guard decode of the first 250 RL images, the JVM half of the gate
  decode $2 $2-dev300-short ktvic_dev dev_data.json
  decode $2 $2-rl250-short ktvic_s3rl rl250_data.json
  [ -e $O/score_$1.json ] || python $G --score $O $1
}
dpo() {  # $1 arm (A or AKL), $2 run, then the arm's own flags: the 20-pair dry run, then the run
  local a=$1 run=$2; shift 2
  local flags="--prereg-arm $a --stage dpo --data $O/cm/A --adapter $R/p1dev_s42 --epochs 1 --beta 0.1 --grad-accum 8 --seed 42 $*"
  [ -e $R/${run}_dry20/train_summary.json ] || python scripts/train_stage2_anchor.py $flags --dry-run \
    --out $R/${run}_dry20 2>&1 | tee -a $O/train_${run}_dry20.log
  python -c "import json, sys; sys.exit(0 if json.load(open('$R/${run}_dry20/train_summary.json'))['dry_run']['pass'] else 1)"
  [ -e $R/$run/train_summary.json ] || python scripts/train_stage2_anchor.py $flags --out $R/$run 2>&1 | tee -a $O/train_$run.log
  keep $run
  arm $a $run
}
decode p1dev_s42 p1dev_s42_redecode-dev300-short ktvic_dev dev_data.json  # step 0, before any training or scoring
for T in 0.5 0.8; do  # e5_sample.py appends and skips the images already written
  P=$O/p1dev_s42-rl1000-short-T$T.jsonl
  n=$(wc -l < $P 2>/dev/null || echo 0)
  if [ "$n" -lt 1000 ]; then
    if [ "$n" -gt 0 ]; then log "RESUME e5_sample T=$T after $n images"; fi
    python scripts/e5_sample.py --adapter $R/p1dev_s42 --split train_data.json --images-file $O/rl1000_ids.txt \
      --limit 0 --prompt short --n 6 --temperature $T --top-p 0.95 --seed 42 --out $P
  fi
done
POOL=$O/p1dev_s42-rl1000-short-pool12.jsonl
[ -e $POOL ] || python scripts/cm_rft.py --merge $O/p1dev_s42-rl1000-short-T0.5.jsonl $O/p1dev_s42-rl1000-short-T0.8.jsonl --out $POOL
decode p1dev_s42 p1dev_s42-rl1000-short ktvic_s3rl rl1000_data.json  # the CM-RFT count and the copy-guard baseline
[ -e $O/cm/A/_build_report.json ] || python scripts/cm_pairs.py --samples $POOL --dataset ktvic --mode cm --out $O/cm/A
[ -e $O/cm/R/_rft_report.json ] || python scripts/cm_rft.py --pool $POOL --greedy $O/p1dev_s42-rl1000-short.preds.json --out $O/cm/R
dpo A cmdpo_A_s42 --lr 5e-6 --anchor-sft 1.0
if [ ! -e $R/cmrft_s42/metrics.jsonl ]; then
  python scripts/train_stage2.py --stage sft --data $O/cm/R --adapter $R/p1dev_s42 --out $R/cmrft_s42 --epochs 1 \
    --lr 1e-5 --loss-mask assistant --seed 42 2>&1 | tee -a $O/train_cmrft_s42.log
fi
grep -q "loss mask: assistant" $O/train_cmrft_s42.log
keep cmrft_s42
arm R cmrft_s42
T=$(python $G --akl-trigger $O)
log "A-KL trigger (arm A failed G2 or G3): $T"
if [ "$T" = yes ]; then dpo AKL cmdpo_AKL_s42 --lr 2.5e-6 --token-kl 0.4; fi
[ -e $O/s3_verdict.json ] || python $G --verdict $O --out $O/s3_verdict.json
python scripts/checkpoint_resume_hook.py --stamp-results $O
log "DONE $(python -c "import json; print(json.load(open('$O/s3_verdict.json'))['outcome'])")"
F=$O/SHA256SUMS; n=2; while [ -e $F ]; do F=$O/SHA256SUMS_v$n; n=$((n + 1)); done
{ find $O -type f ! -name 'SHA256SUMS*' -print0 | sort -z | xargs -0 sha256sum
  for r in cmdpo_A_s42 cmrft_s42 cmdpo_AKL_s42; do
    if [ -e $R/$r/adapter_model.safetensors ]; then sha256sum $R/$r/adapter_model.safetensors $R/$r/adapter_config.json; fi
  done; } > $F
