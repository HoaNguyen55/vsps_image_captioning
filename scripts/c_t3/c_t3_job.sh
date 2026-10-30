#!/bin/bash
# Paper C tier 3 (TEST, one look, C-T3) on M1 only (machine id m3). Rule: manuscript/prereg/2026-10-31_c_t3/PREREG.md
# (C-T1 PREREG §8; family = T2_DECISION e29bbe8a: the three E3 claims). Flickr30K Karpathy test (all 1,000 images) is the
# evaluation set. Preflight runs the test-side near-duplicate pass (c_t3_neardup.py, W25 RULE §3, CPU) BEFORE any GPU
# step. Frozen tier-1/2 configurations, COCO memory, no tuning, one look; on f30k_test c_t3.py refuses every run outside
# T3_RUN_IDS (no rand arm). Claim arms first, then the W2 zs arms; one 2.5 GPU-h cap (b1.left accounting); a timeout is a
# CAP STOP, final, and the arms not reached are NOT RUN. No scoring here: references never come to M1 (PREREG §6).
# Staged before (operator, one LOG checklist line, no host string; PREREG §7):
#   $NCS_DATA/datasets/c_t3_f30k_test/{images,manifest.json} from `c_t3.py extract` (test-only .tar, untarred by list,
#   the .tar deleted before this job); c_t2_f30k_val and c_t1_f30k_carve still staged (neardup); cen_memory/images and
#   c_t1_mem/{memfiles_coco.json,coco_captions.json} (memcheck); /root/outputs/c_en/feats_memory.npz (caf4a621) and
#   $NCS_DATA/models/sscd_disc_mixup.torchscript.pt (9f26bd4c); venv-cenfeat; no other datasets dir than the allow-list
#   (A-T3's a_t3/ parked outside, logged).
# Usage, inside tmux:  bash scripts/c_t3/c_t3_job.sh <expected 40-hex HEAD>
set -euo pipefail
EXPECT=${1:?usage: c_t3_job.sh <expected HEAD>}
MID=$(cat /root/.vsps_machine_id 2>/dev/null)
[ "$MID" = m3 ] || { echo "REFUSED: C-T3 runs on M1 (machine id m3) only"; exit 1; }
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=$MID
LB=/root/venv-lb/bin/python; T1=/root/venv-t1/bin/python; SC=/root/venv-c1score/bin/python; PY=/root/vsps/.venv/bin/python
FT=/root/venv-cenfeat/bin/python
LB_FREEZE=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784   # setup_gpu.sh H_LB
FT_FREEZE=1a639a50adf550c50c6dfe284146e279b2a2bf2a716ade743e9eb357ccbf0778   # C-EN cenfeat_venv_freeze.txt (W25, W25-K1)
T1_FREEZE=${T1_FREEZE:?set T1_FREEZE to the venv-t1 freeze sha256 recorded for C-T1}
X=scripts/c_t3/c_t3.py; JOB=scripts/c_t3/c_t3_job.sh; ND=scripts/c_t3/c_t3_neardup.py
O=/root/outputs/c_t3; P=$O/out; LOG=$O/logs; USED=$O/gpu_seconds.tsv; MARK=$O/CAP_STOP.json
DS=$NCS_DATA/datasets; MEM=$DS/c_t1_mem; VAL=$DS/c_t2_f30k_val; TEST=$DS/c_t3_f30k_test; CEN=/root/outputs/c_en
CL=manuscript/prereg/2026-10-22_c_stage1/lists.json
SIG=$NCS_DATA/models/siglip2; XG=$NCS_DATA/models/c_t1_xglm_2_9b; MC=$NCS_DATA/models/c_t1_mclip_h14
snap() { case $1 in qwen25vl_7b|internvl3_8b) echo $NCS_DATA/models/$1;; *) echo $NCS_DATA/models/c_t1_$1;; esac; }
export C_T3_LOCK=$O/RUNNING VSPS_JOB_SHA256=$(sha256sum $JOB | cut -c1-64)
mkdir -p $O $P $LOG
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*" | tee -a $LOG/job.log; }
stop() { say "JOB STOP $*"; exit 1; }
$PY $X lock --path $C_T3_LOCK || exit 1
trap 'rm -f $C_T3_LOCK' EXIT

# ---------------------------------------------------------------- preflight
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
[ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ] || stop "GPU busy (another job): never concurrent"
sha256sum --quiet -c scripts/c_t3/SHA256SUMS || stop "scripts/c_t3/SHA256SUMS"
sha256sum --quiet -c manuscript/prereg/2026-10-31_c_t3/SHA256SUMS || stop "C-T3 prereg SHA256SUMS"
sha256sum --quiet -c manuscript/prereg/2026-10-30_c_t1/SHA256SUMS || stop "C-T1 prereg SHA256SUMS (lists, registry)"
grep ' /root/outputs/c_en/' manuscript/prereg/2026-10-30_c_t1/RESTORED_SHA256 | sha256sum --quiet -c || stop "COCO memory differs"
[ "$(/root/venv-lb/bin/pip freeze | sha256sum | cut -c1-64)" = $LB_FREEZE ] || stop "venv-lb freeze differs"
[ "$(/root/venv-t1/bin/pip freeze | sha256sum | cut -c1-64)" = $T1_FREEZE ] || stop "venv-t1 freeze differs"
[ "$(/root/venv-cenfeat/bin/pip freeze | sha256sum | cut -c1-64)" = $FT_FREEZE ] || stop "venv-cenfeat freeze differs"
$LB $X --selftest >> $LOG/selftest.log 2>&1 || stop "c_t3 selftest (venv-lb)"
$SC $X --selftest >> $LOG/selftest.log 2>&1 || stop "c_t3 selftest (venv-c1score)"
$FT $ND --selftest >> $LOG/selftest.log 2>&1 || stop "c_t3_neardup selftest (venv-cenfeat)"
$PY $X guard --datasets $DS --roots $DS $NCS_DATA/models $NCS_DATA/vncorenlp $O ${HF_HOME:-/root/.cache/huggingface}/hub \
  >> $LOG/guard.log 2>&1 || stop "custody guard (Flickr30K test names, archives, datasets allow-list)"
$PY $X memcheck --mem-files $MEM/memfiles_coco.json --root $DS/cen_memory/images >> $LOG/memcheck.log 2>&1 || stop "memcheck coco"
for m in aya_vision_8b xglm_2_9b mclip_h14; do $PY $X pinsok --model $m --snapshot $(snap $m) >> $LOG/pins.log 2>&1 || stop "$m snapshot"; done
HF_HUB_OFFLINE=1 $T1 $X t1check --mclip $MC >> $LOG/t1check.log 2>&1 || stop "venv-t1 open_clip offline"
# PI-1030f test = full near-dup (W25 RULE §3), CPU, before any GPU step; once (it refuses an existing output).
# Codex #5: an existing neardup.json is reused only if `check` matches it to the staged manifests, else FAULT
if [ -e $O/neardup.json ]; then $FT $ND check --test $TEST --val $VAL --carve $DS/c_t1_f30k_carve --out $O/neardup.json \
  >> $LOG/neardup.log 2>&1 || stop "neardup.json exists but does not match the staged sets (FAULT: back to the judge)"; fi
[ -e $O/neardup.json ] || timeout 3600 $FT $ND run --test $TEST --val $VAL --carve $DS/c_t1_f30k_carve \
  --mem-feats $CEN/feats_memory.npz --mem-files $MEM/memfiles_coco.json --mem-root $DS/cen_memory/images \
  --sscd $NCS_DATA/models/sscd_disc_mixup.torchscript.pt --out $O/neardup.json >> $LOG/neardup.log 2>&1 \
  || stop "neardup (FAULT or 1 h wall: back to the judge, nothing decoded)"
sha256sum $X $JOB $ND $O/neardup.json > $O/code_at_start.sha256
say "JOB START head $EXPECT"

finish() {
  (cd $O && find out logs neardup.json -type f ! -name '*.partial*' | sort | xargs -r sha256sum) > $O/SHA256SUMS
  say "JOB DONE gpu_h $(awk '$2 != "start" {s += $2} END {printf "%.2f", s / 3600}' $USED)"; exit 0; }
cap_stop() { [ -e $MARK ] || printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > $MARK; say "CAP STOP $1"; finish; }
gpu() {  # gpu NAME CMD...: one GPU step under the time left; any failure stops (no retry except a partial resume)
  local name=$1; shift
  [ -s $LOG/$name.done ] && return 0
  local t; t=$($PY $X left --used $USED --marker $MARK) || stop "cap arithmetic"
  [ "$t" -gt 0 ] || cap_stop "2.5 GPU-h cap before $name"
  say "START $name (left $((t / 60)) min)"
  local t0 rc=0; t0=$(date +%s)
  echo "$name start $t0" >> $USED
  timeout ${t}s "$@" >> $LOG/$name.log 2>&1 || rc=$?
  echo "$name $(( $(date +%s) - t0 ))" >> $USED
  [ $rc = 124 ] && cap_stop "2.5 GPU-h cap reached during $name"
  [ $rc = 0 ] && { say "OK $name"; date -u +%FT%TZ > $LOG/$name.done; return 0; }
  stop "$name rc=$rc"
}
EN_IMG=(--images $TEST/images --manifest $TEST/manifest.json); TEST_EX=$P/x1_f30k_test_coco.json
EN_MEM=(--captions $MEM/coco_captions.json --memory coco)
dec() {  # dec NAME MODEL ARM [extra args]: one decode on f30k_test
  local name=$1 m=$2 arm=$3; shift 3
  gpu $name $LB $X decode --model $m --set f30k_test --arm $arm --snapshot $(snap $m) --out-dir $P --c-lists $CL "${EN_IMG[@]}" "$@"
}

# ---------------------------------------------------------------- V0: test vectors and example lists (COCO memory)
gpu V0_embed_test $LB $X embed --set f30k_test --images $TEST/images --snapshot $SIG --manifest $TEST/manifest.json --out $P/emb_f30k_test.npz
$PY $X draws --mem-emb $CEN/cen_memory_emb.npz --query-emb $P/emb_f30k_test.npz --set f30k_test --out $TEST_EX >> $LOG/draws.log 2>&1 || stop "draws f30k_test"

# ---------------------------------------------------------------- V1: claim arms (frozen tier-1/2 configurations, tau = -inf; no rand)
gpu V1_lmcap_ri_test $T1 $X lmcap --set f30k_test --variant ri --xglm $XG --mclip $MC --mem-emb $CEN/cen_memory_emb.npz \
  --query-emb $P/emb_f30k_test.npz --ex $TEST_EX --mem-images $DS/cen_memory/images --mem-files $MEM/memfiles_coco.json \
  --out-dir $P "${EN_MEM[@]}" "${EN_IMG[@]}"
dec V1_aya_ret aya_vision_8b ret --k 4 --order last --tpl T1 --ex $TEST_EX "${EN_MEM[@]}"
dec V1_qwen_ret qwen25vl_7b ret --k 8 --order first --tpl T1 --ex $TEST_EX "${EN_MEM[@]}"
dec V1_internvl3_ret internvl3_8b ret --k 4 --order last --tpl T2 --ex $TEST_EX "${EN_MEM[@]}"

# ---------------------------------------------------------------- V2: W2 zero-shot arms (descriptive; cut first by the cap)
dec V2_qwen_zs qwen25vl_7b zs
dec V2_internvl3_zs internvl3_8b zs
dec V2_aya_zs aya_vision_8b zs
finish
