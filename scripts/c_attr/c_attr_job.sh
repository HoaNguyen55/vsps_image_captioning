#!/bin/bash
# C-ATTR-DEV block 1 on one rented RTX 3090 / 3090 Ti 24 GB (machine id h1). Rule:
# manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md §6.3, §9, §10 (rulings CC-331, CC-332); run document
# C_ATTR_BLOCK1_RUN_DOC_v1.md. Label: DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. Development sets only (OV-dev-A,
# OV-dev-B, XM-dev500); every test set is refused by name and by file (c_attr.py guard, items_of, open() hook).
# Steps in registered order 1.0 -> 1.5 under one 12 GPU-h cap (b1.left accounting); each GPU step runs under `timeout`
# for the time left; a timeout is a CAP STOP, final, and every later step is NOT RUN (so steps drop from the bottom:
# 1.5, the XM-dev500 half of 1.4, 1.4, 1.3). A failed step resumes from its own partial file, at most 3 attempts, then
# JOB STOP. Step 1.0: per backbone, check (a) host parity (first 50 OV-dev-B ret items, stored order and batch slices;
# plus the first 50 OV-dev-A items of Qwen2.5-VL and InternVL3, CC-331 N12) and check (b) A1 (reversed order, batch 1).
# A failed (a) triggers the §6.3 fallback before that backbone's perm step: zs, ret and rand d0 decoded again on this
# host for the sets of its perm step (rows labelled "base arms re-decoded on the new host"). A failed (b) is recorded
# (K1: that backbone leaves the families); nothing is dropped for it. No scoring here; the comparators print counts and
# item ids only. InternVL3 and every backbone at tau = -inf (no deletion step).
# Usage, inside tmux:  bash scripts/c_attr/c_attr_job.sh selftest|block1|block1b <expected 40-hex HEAD>
# block1b (addendum v1.2, CC-340/CC-341): outputs under /root/outputs/c_attr_b1; never beside block 1. 1b.0 D1 per
# backbone (forward batch-1 decode of the first 50 OV-dev-B ret items against this host's step-1.0 (b) rev50 decode;
# on a host without it, a rev50 decode first), then plan1b (V7 cap from the D1 load / decode seconds) and a PAUSE so
# the cap is logged before Tier A; the second call runs STEPS_1B.tsv at batch size 1 under that cap (drops from the
# bottom: Tier C, Tier B zs, Aya-Vision Tier B). C_ATTR_1B_MODELS limits the backbones on a second host (h2).
# block3 (registration v1.1 §6.5, addendum v1.2 V8; C_ATTR_BLOCK3_RUN_DOC_v1.md): outputs under /root/outputs/c_attr_b3,
# never beside another job. D1 per runner (LMCap lmcap_ri and Qwen2.5-VL ret_img: first 50 OV-dev-B items, reversed
# then forward, batch size 1), then plan3 (cap min(12, 1.5 P3) from the forward D1 load / decode seconds) and a PAUSE so
# the cap is logged; the second call runs STEPS_3.tsv (LMCap OV-dev-B ri, rand, perm; LMCap XM-dev500; Qwen2.5-VL
# ret_img, rand_img d0 on OV-dev-B, then XM-dev500) under that cap, so a cap stop drops from the bottom.
# Dry run: C_ATTR_DRY=1 on the host itself (PI 2026-11-11: checks run on the rented host, not the laptop; outputs
# under /root/outputs/c_attr_dry; scripts/c_attr/dryrun.sh is the laptop harness of the same run): every decode runs with
# --limit 2 --dry-run and stops before the model load; checks that need the host (GPU, weights, venv freeze) are skipped
# with a DRY line; the comparators answer rc 3, so the fallback branch is exercised too.
set -euo pipefail
MODE=${1:?usage: c_attr_job.sh selftest|block1|block1b|block3 <expected HEAD>}; EXPECT=${2:?usage: c_attr_job.sh MODE <expected HEAD>}
DRY=${C_ATTR_DRY:-0}
case $MODE in selftest|block1|block1b|block3) ;; *) echo "unknown mode $MODE"; exit 2;; esac
MID=$(cat /root/.vsps_machine_id 2>/dev/null || true)
case "$MID" in h1|h2) ;; *) echo "REFUSED: /root/.vsps_machine_id is not h1 or h2"; exit 1;; esac
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=$MID
LB=/root/venv-lb/bin/python; PY=/root/vsps/.venv/bin/python
LB_FREEZE=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784   # setup_gpu.sh H_LB (as C-T1 / C-T2)
X=scripts/c_attr/c_attr.py; JOB=scripts/c_attr/c_attr_job.sh
O=/root/outputs/c_attr; [ $MODE = block1b ] && O=/root/outputs/c_attr_b1; [ $MODE = block3 ] && O=/root/outputs/c_attr_b3
[ "$DRY" = 1 ] && O=${O}_dry   # a dry run never leaves .done files for block 1 or 1b
P=$O/out; LOG=$O/logs; Q=$O/parity; USED=$O/gpu_seconds.tsv; MARK=$O/CAP_STOP.json
DS=$NCS_DATA/datasets; CL=manuscript/prereg/2026-10-22_c_stage1/lists.json
snap() { case $1 in qwen25vl_7b|internvl3_8b) echo $NCS_DATA/models/$1;; *) echo $NCS_DATA/models/c_t1_$1;; esac; }
export C_ATTR_LOCK=$O/RUNNING VSPS_JOB_SHA256=$(sha256sum $JOB | cut -c1-64)
mkdir -p $O $P $LOG $Q
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*" | tee -a $LOG/job.log; }
stop() { say "JOB STOP $*"; exit 1; }
dry() { [ "$DRY" = 1 ]; }
$PY $X lock --path $C_ATTR_LOCK || exit 1
( while sleep 60; do ts > $O/HEARTBEAT; done ) & HB=$!
trap 'kill $HB 2>/dev/null; rm -f $C_ATTR_LOCK' EXIT
dry && say "DRY RUN (laptop, PI-1109g): mode $MODE, decodes stop before the model load"

# ---------------------------------------------------------------- preflight (both modes)
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
if dry; then say "DRY: GPU-busy check skipped (no GPU)"
else [ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ] || stop "GPU busy (another job): never concurrent"; fi
(cd scripts/c_attr && sha256sum --quiet -c SHA256SUMS) || stop "scripts/c_attr/SHA256SUMS"
(cd manuscript/prereg/2026-11-11_c_attr_dev && sha256sum --quiet -c SHA256SUMS) || stop "registration SHA256SUMS"
if [ $MODE = block1b ]; then
  (cd manuscript/prereg/2026-11-11_c_attr_dev && sha256sum --quiet -c SHA256SUMS_1B) || stop "addendum v1.2 SHA256SUMS_1B"
  [ -e /root/outputs/c_attr/RUNNING ] && stop "block 1 is still running (never beside it, §6.7)"
  dry || [ "$MID" = h2 ] || [ -s /root/outputs/c_attr/SHA256SUMS ] || stop "block 1 not closed: /root/outputs/c_attr/SHA256SUMS missing"
fi
MODELS="qwen25vl_7b internvl3_8b aya_vision_8b"
if [ $MODE = block3 ]; then   # block 3 reads Qwen2.5-VL, LMCap's pinned models and three stored vector files only
  MODELS=qwen25vl_7b
  (cd manuscript/prereg/2026-11-11_c_attr_dev && sha256sum --quiet -c SHA256SUMS_1B) || stop "addendum v1.2 SHA256SUMS_1B (V8)"
  sha256sum --quiet -c manuscript/prereg/2026-10-30_c_t1/SHA256SUMS || stop "c_t1 registry SHA256SUMS (LMCap pins)"
  for r in /root/outputs/c_attr/RUNNING /root/outputs/c_attr_b1/RUNNING; do [ -e $r ] && stop "$r exists (never beside another job, §6.7)"; done
  grep -E 'c_stage1/emb\.npz|c_stage2/emb_(ov_dev_b|xm_dev500)\.npz' scripts/c_attr/STORED_SHA256 | sha256sum --quiet -c \
    || stop "stored SigLIP2 vectors differ"
else
  grep -E 'ov_dev_[ab]-ret-' scripts/c_attr/STORED_SHA256 | sha256sum --quiet -c || stop "stored ret runs differ"
fi
(cd scripts/c_attr && sha256sum --quiet -c c_attr_lists.json.sha256) || stop "c_attr_lists.json differs from its sidecar"
if dry; then say "DRY: venv-lb freeze check skipped (laptop venv)"
else [ "$(/root/venv-lb/bin/pip freeze | sha256sum | cut -c1-64)" = $LB_FREEZE ] || stop "venv-lb freeze differs"; fi
$LB $X --selftest >> $LOG/selftest.log 2>&1 || stop "c_attr selftest (venv-lb)"
$PY scripts/c_attr/c_attr_lists.py --selftest >> $LOG/selftest.log 2>&1 || stop "c_attr_lists selftest"
$PY $X guard --datasets $DS --roots $DS $NCS_DATA/models $O ${HF_HOME:-/root/.cache/huggingface}/hub \
  >> $LOG/guard.log 2>&1 || stop "custody guard (§5 refusal lists, archives, datasets allow-list)"
for m in $MODELS; do
  [ -d "$(snap $m)" ] || stop "$m snapshot dir missing"
done
T1=/root/venv-t1/bin/python; MEM=$DS/c_t1_mem; CS1=/root/outputs/c_stage1; CS2=/root/outputs/c_stage2
XG=$NCS_DATA/models/c_t1_xglm_2_9b; MC=$NCS_DATA/models/c_t1_mclip_h14
T1_FREEZE=1766dc23a71509ba4fb6b8adb34b1999a3a2bf78ebe1e227730fd6647bea3599   # venv-t1 of record (OPS-1030n; C-T2, C-T3)
if [ $MODE = block3 ]; then
  if dry; then say "DRY: venv-t1 freeze, LMCap pins and t1check skipped (no weights on the laptop)"
  else
    [ "$(/root/venv-t1/bin/pip freeze | sha256sum | cut -c1-64)" = $T1_FREEZE ] || stop "venv-t1 freeze differs"
    for m in xglm_2_9b mclip_h14; do $PY $X pinsok --model $m --snapshot $(snap $m) >> $LOG/pins.log 2>&1 || stop "$m snapshot"; done
    $T1 $X t1check --mclip $MC >> $LOG/t1check.log 2>&1 || stop "venv-t1 open_clip offline (W8)"
  fi
  $T1 $X --selftest >> $LOG/selftest.log 2>&1 || stop "c_attr selftest (venv-t1)"
  $PY $X memcheck --mem-files $MEM/memfiles_vi.json --root $DS >> $LOG/memcheck.log 2>&1 || stop "memcheck vi (8,190 representatives)"
elif dry; then say "DRY: aya_vision_8b pinsok skipped (no weights on the laptop)"
else $PY $X pinsok --model aya_vision_8b --snapshot $(snap aya_vision_8b) >> $LOG/pins.log 2>&1 || stop "aya snapshot"; fi
sha256sum $X $JOB scripts/c_attr/c_attr_lists.json > $O/code_at_start.sha256
say "PREFLIGHT OK head $EXPECT mode $MODE"
[ $MODE = selftest ] && { say "SELFTEST MODE DONE"; exit 0; }

# ---------------------------------------------------------------- block 1
finish() {
  (cd $O && find out logs parity -type f ! -name '*.partial*' | LC_ALL=C sort | xargs -r sha256sum) > $O/SHA256SUMS
  say "JOB DONE gpu_h $(awk '$2 != "start" {s += $2} END {printf "%.2f", s / 3600}' $USED)"; exit 0; }
cap_stop() { [ -e $MARK ] || printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > $MARK; say "CAP STOP $1 (later steps NOT RUN)"; finish; }
gpu() {  # gpu NAME CMD...: one GPU step under the time left; up to 3 attempts, each resuming from its partial file
  local name=$1; shift
  [ -s $LOG/$name.done ] && return 0
  local att t t0 rc
  for att in 1 2 3; do
    t=$($PY $X left --used $USED --marker $MARK "${CAPARGS[@]}") || stop "cap arithmetic"
    [ "$t" -gt 0 ] || cap_stop "GPU-h cap before $name"
    say "START $name attempt $att (left $((t / 60)) min)"
    rc=0; t0=$(date +%s); echo "$name start $t0" >> $USED
    timeout ${t}s "$@" >> $LOG/$name.log 2>&1 || rc=$?
    echo "$name $(( $(date +%s) - t0 ))" >> $USED
    [ $rc = 124 ] && cap_stop "GPU-h cap reached during $name"
    [ $rc = 0 ] && { say "OK $name"; ts > $LOG/$name.done; return 0; }
    say "FAIL $name rc=$rc attempt $att"
  done
  stop "$name failed 3 attempts"
}
DRYARGS=(); dry && DRYARGS=(--limit 2 --dry-run)
CAPARGS=()   # block 1: the 12 GPU-h CAP_S of c_attr.py
dec() {  # dec NAME MODEL SET ARM [extra args]: one decode, Vietnamese memory, example ids from c_attr_lists.json
  local name=$1 m=$2 s=$3 arm=$4; shift 4
  gpu $name $LB $X decode --model $m --set $s --arm $arm --snapshot $(snap $m) --out-dir $P --c-lists $CL \
    --images $DS "$@" "${DRYARGS[@]}"
}
cmp_() {  # cmp_ NAME SET NEW OLD [--stored]: rc 0 identical, 3 differs (counts and ids only); anything else stops
  local name=$1 s=$2 new=$3 old=$4; shift 4
  local rc=0 extra=(); dry && extra=(--dry-run)
  $PY $X compare --name $name --set $s --new $new --old $old --c-lists $CL --out $Q/$name.json "$@" "${extra[@]}" \
    >> $LOG/compare.log 2>&1 || rc=$?
  [ $rc = 0 ] || [ $rc = 3 ] || stop "compare $name rc=$rc"
  return $rc
}
declare -A CFG=([qwen25vl_7b]="8 first T1" [internvl3_8b]="4 last T2" [aya_vision_8b]="4 last T1")
declare -A REF_B=([qwen25vl_7b]=/root/outputs/c_stage2/runs/c2_qwen25vl_7b_ov_dev_b-ret-k8-first-T1.preds.json
                  [internvl3_8b]=/root/outputs/c_stage2/runs/c2_internvl3_8b_ov_dev_b-ret-k4-last-T2.preds.json
                  [aya_vision_8b]=/root/outputs/c_t1/out/t1_aya_vision_8b_ov_dev_b-ret-k4-last-T1-mvi.preds.json)
declare -A REF_A=([qwen25vl_7b]=/root/outputs/c_stage1/runs/c1_qwen25vl_7b_ov_dev_a-ret-k8-first-T1.preds.json
                  [internvl3_8b]=/root/outputs/c_stage1/runs/c1_internvl3_8b_ov_dev_a-ret-k4-last-T2.preds.json)
declare -A PERM_SETS=([qwen25vl_7b]="ov_dev_a ov_dev_b xm_dev500" [internvl3_8b]="ov_dev_a ov_dev_b xm_dev500"
                      [aya_vision_8b]="ov_dev_b xm_dev500")
declare -A FALLBACK_SETS=([qwen25vl_7b]="ov_dev_a ov_dev_b xm_dev500" [internvl3_8b]="ov_dev_a ov_dev_b xm_dev500"
                          [aya_vision_8b]="ov_dev_b")
out_of() { local m=$1 s=$2 rd=$3; set -- ${CFG[$m]}; echo "$P/at_${m}_${s}-ret-k$1-$2-$3-mvi-$rd$(dry && echo -smoke).preds.json"; }

# ---------------------------------------------------------------- block 1b (addendum v1.2, V3-V7)
if [ $MODE = block1b ]; then
  CAPARGS=(--cap-s 144000)   # D1 runs under the 40 GPU-h ceiling of V7; the D1 seconds count against the cap
  pass=()
  for m in ${C_ATTR_1B_MODELS:-qwen25vl_7b internvl3_8b aya_vision_8b}; do
    set -- ${CFG[$m]}; k=$1 o=$2 t=$3
    ref=/root/outputs/c_attr/out/$(basename $(out_of $m ov_dev_b rev50))
    if [ ! -s $ref ]; then   # V3 / second-host row: no step-1.0 (b) file here, so a batch-1 reversed decode first
      [ "$MID" = h1 ] && ! dry && stop "$ref missing on h1 (D1 needs the step-1.0 (b) decode)"
      dec D1r_$m $m ov_dev_b ret --k $k --order $o --tpl $t --memory vi --redecode rev50; ref=$(out_of $m ov_dev_b rev50)
    fi
    dec D1_$m $m ov_dev_b ret --k $k --order $o --tpl $t --memory vi --redecode fwd50 --batch1
    d1=PASS; cmp_ D1_$m ov_dev_b $(out_of $m ov_dev_b b1-fwd50) $ref --d1 || d1=FAIL
    dry && d1=PASS   # dry: the comparator answers rc 3; every step is exercised
    printf '{"model": "%s", "D1": "%s", "host": "%s", "utc": "%s"}\n' $m $d1 $MID "$(ts)" > $Q/STEP1B0_$m.json
    say "STEP 1b.0 $m D1 $d1$( [ $d1 = FAIL ] && echo ' (leaves the 1b families; its 1b steps NOT RUN)')"
    if [ $d1 = PASS ]; then pass+=($(out_of $m ov_dev_b b1-fwd50)); fi
  done
  if [ ! -s $O/CAP_1B.json ]; then
    rc=0; $PY $X plan1b --d1 "${pass[@]}" --out $O/CAP_1B.json --steps $O/STEPS_1B.tsv $(dry && echo --dry-run) \
      >> $LOG/plan.log 2>&1 || rc=$?
    say "$(tail -1 $LOG/plan.log)"
    [ $rc = 4 ] && { rm -f $O/CAP_1B.json; stop "Tier A does not fit the cap or ends later than 24 h before K7 (V7): back to the judge"; }
    [ $rc = 0 ] || stop "plan1b rc=$rc"
    dry || { say "PAUSE after D1: log the cap line ($O/CAP_1B.json sha256 $(sha256sum $O/CAP_1B.json | cut -c1-64)), then run block1b again"; exit 0; }
  fi
  CAPARGS=(--cap-s $($PY -I -c 'import json, sys; print(json.load(open(sys.argv[1]))["cap_s"])' $O/CAP_1B.json))
  say "BLOCK 1b: $(wc -l < $O/STEPS_1B.tsv) runs at batch size 1 under cap ${CAPARGS[1]} s"
  while read -r name m s arm rest <&3; do dec $name $m $s $arm $rest --batch1; done 3< $O/STEPS_1B.tsv
  finish
fi

# ---------------------------------------------------------------- block 3 (registration v1.1 §6.5, addendum v1.2 V8)
if [ $MODE = block3 ]; then
  CAPARGS=(--cap-s $((12 * 3600)))   # D1 runs under the 12 GPU-h ceiling of V8; the D1 seconds count against the cap
  VMEM=(--memory vi --mem-images $DS --mem-files $MEM/memfiles_vi.json)
  lm() {  # lm NAME SET VARIANT [extra]: one LMCap re-implementation decode (venv-t1), Vietnamese memory
    local name=$1 s=$2 v=$3; shift 3
    gpu $name $T1 $X lmcap --set $s --variant $v --xglm $XG --mclip $MC --mem-emb $CS1/emb.npz \
      --query-emb $CS2/emb_$s.npz --c-lists $CL --images $DS "${VMEM[@]}" --out-dir $P "$@" "${DRYARGS[@]}"
  }
  img() {  # img NAME SET ARM [extra]: one Qwen2.5-VL image-caption-pair decode (k = 8, T1; batch size 1 always)
    local name=$1 s=$2 arm=$3; local o=(); shift 3; [ $arm = ret_img ] && o=(--order first)
    dec $name qwen25vl_7b $s $arm --k 8 "${o[@]}" --tpl T1 "${VMEM[@]}" "$@"
  }
  pf() { echo "$P/$1$(dry && echo -smoke).preds.json"; }
  pass=()
  d1() {  # d1 RUNNER FWD REV: the D1 verdict (counts and ids only); a FAIL leaves the runner's block-3 steps NOT RUN
    local r=$1 v=PASS
    cmp_ D1_$r ov_dev_b $2 $3 --d1 || v=FAIL
    dry && v=PASS   # dry: the comparator answers rc 3; every step is exercised
    printf '{"model": "%s", "D1": "%s", "host": "%s", "block": 3, "utc": "%s"}\n' $r $v $MID "$(ts)" > $Q/STEP3_$r.json
    say "STEP 3.0 $r D1 $v$( [ $v = FAIL ] && echo ' (its block-3 steps NOT RUN)')"
    if [ $v = PASS ]; then pass+=($2); fi
  }
  lm D1r_lmcap ov_dev_b ri --redecode rev50
  lm D1_lmcap ov_dev_b ri --redecode fwd50 --batch1
  d1 lmcap $(pf at_lmcap-ri_ov_dev_b-mvi-b1-fwd50) $(pf at_lmcap-ri_ov_dev_b-mvi-rev50)
  img D1r_qwen25vl_7b ov_dev_b ret_img --redecode rev50
  img D1_qwen25vl_7b ov_dev_b ret_img --redecode fwd50 --batch1
  d1 qwen25vl_7b $(pf at_qwen25vl_7b_ov_dev_b-ret_img-k8-first-T1-mvi-b1-fwd50) $(pf at_qwen25vl_7b_ov_dev_b-ret_img-k8-first-T1-mvi-rev50)
  if [ ! -s $O/CAP_3.json ]; then
    rc=0; $PY $X plan3 --d1 "${pass[@]}" --out $O/CAP_3.json --steps $O/STEPS_3.tsv $(dry && echo --dry-run) \
      >> $LOG/plan.log 2>&1 || rc=$?
    say "$(tail -1 $LOG/plan.log)"
    [ $rc = 0 ] || stop "plan3 rc=$rc"
    dry || { say "PAUSE after D1: log the cap line ($O/CAP_3.json sha256 $(sha256sum $O/CAP_3.json | cut -c1-64)), then run block3 again"; exit 0; }
  fi
  CAPARGS=(--cap-s $($PY -I -c 'import json, sys; print(json.load(open(sys.argv[1]))["cap_s"])' $O/CAP_3.json))
  say "BLOCK 3: $(wc -l < $O/STEPS_3.tsv) runs at batch size 1 under cap ${CAPARGS[1]} s"
  while read -r name runner s arm <&3; do
    if [ $runner = lmcap ]; then lm $name $s $arm --batch1; else img $name $s $arm --batch1; fi
  done 3< $O/STEPS_3.tsv
  finish
fi

# step 1.0: 300 registered captions (3 backbones x 2 x 50, OV-dev-B) + 100 per CC-331 N12 (OV-dev-A, check (a))
say "STEP 1.0 host parity (a) and A1 (b): 300 registered + 100 per CC-331 N12 captions"
for m in qwen25vl_7b aya_vision_8b internvl3_8b; do
  set -- ${CFG[$m]}; k=$1 o=$2 t=$3; par=PASS
  for s in ov_dev_b ov_dev_a; do
    ref=${REF_A[$m]:-}; [ $s = ov_dev_b ] && ref=${REF_B[$m]}
    [ -n "$ref" ] || continue
    dec S10a_${m}_$s $m $s ret --k $k --order $o --tpl $t --memory vi --redecode host50 --stored $ref
    cmp_ S10a_${m}_$s $s $(out_of $m $s host50) $ref --stored || par=FAIL
  done
  dec S10b_${m} $m ov_dev_b ret --k $k --order $o --tpl $t --memory vi --redecode rev50
  a1=PASS; cmp_ S10b_${m} ov_dev_b $(out_of $m ov_dev_b rev50) $(out_of $m ov_dev_b host50) || a1=FAIL
  printf '{"model": "%s", "host_parity": "%s", "A1": "%s", "utc": "%s"}\n' $m $par $a1 "$(ts)" > $Q/STEP10_$m.json
  say "STEP 1.0 $m host parity $par, A1 $a1$( [ $a1 = FAIL ] && echo ' (K1: leaves the families)')"
done
dry && say "DRY: comparators answered rc 3, so every fallback branch below is exercised"

fallback() {  # §6.3: base arms decoded again on this host for the sets of the backbone's perm step (K1b)
  local m=$1; grep -q '"host_parity": "FAIL"' $Q/STEP10_$m.json || return 0
  set -- ${CFG[$m]}
  say "FALLBACK $m: base arms re-decoded on the new host (${FALLBACK_SETS[$m]})"
  for s in ${FALLBACK_SETS[$m]}; do
    dec F_${m}_${s}_zs $m $s zs
    dec F_${m}_${s}_ret $m $s ret --k $1 --order $2 --tpl $3 --memory vi
    dec F_${m}_${s}_rand0 $m $s rand --k $1 --tpl $3 --draw 0 --memory vi
  done
}
perms() {  # perms STEP MODEL: perm p1, p2 on the backbone's perm sets
  local st=$1 m=$2; set -- ${CFG[$m]}
  for s in ${PERM_SETS[$m]}; do for p in 1 2; do
    dec ${st}_${m}_${s}_perm$p $m $s perm --k $1 --order $2 --tpl $3 --draw $p --memory vi
  done; done
}
# step 1.1: Qwen2.5-VL perm
fallback qwen25vl_7b; perms S11 qwen25vl_7b
# step 1.2: Aya-Vision zs, ret, rand d0 on XM-dev500; perm on OV-dev-B and XM-dev500
dec S12_aya_xm_zs aya_vision_8b xm_dev500 zs
dec S12_aya_xm_ret aya_vision_8b xm_dev500 ret --k 4 --order last --tpl T1 --memory vi
dec S12_aya_xm_rand0 aya_vision_8b xm_dev500 rand --k 4 --tpl T1 --draw 0 --memory vi
fallback aya_vision_8b; perms S12 aya_vision_8b
# step 1.3: InternVL3 (tau = -inf) perm
fallback internvl3_8b; perms S13 internvl3_8b
# step 1.4: Qwen2.5-VL fix f1-f4, OV-dev-B first (the XM-dev500 half drops first)
for s in ov_dev_b xm_dev500; do for j in 1 2 3 4; do
  dec S14_qwen_${s}_fix$j qwen25vl_7b $s fix --k 8 --tpl T1 --draw $j --memory vi
done; done
# step 1.5: rand d1, d2 on XM-dev500, all three
for m in qwen25vl_7b aya_vision_8b internvl3_8b; do set -- ${CFG[$m]}
  for d in 1 2; do dec S15_${m}_xm_rand$d $m xm_dev500 rand --k $1 --tpl $3 --draw $d --memory vi; done
done
finish
