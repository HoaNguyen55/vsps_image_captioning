#!/bin/bash
# Paper C tier 1 (DEV-EXPLORE, C-T1) on the dev-role machine (machine id m4). Rule:
# manuscript/prereg/2026-10-30_c_t1/PREREG.md. Dev data only: KTVIC dev299, OV-dev-B, a 1,000-image carve of
# Flickr30K train (+ its other 28,000 train images as the X5 memory). Never a Flickr30K val or test image, never an
# OpenViIC/KTVIC/XM3600 test image. Blocks run in priority order B0..B7 under one 20 GPU-h cap (b1.left accounting); a
# timeout is a CAP STOP, final, and the remaining blocks are reported NOT RUN. rc 3 from vicheck = that backbone is not
# Vietnamese-assessable, next in the fallback order. Scoring of B2..B7 happens on the laptop after the pull; only the
# KTVIC dev299 selection (B1) is scored here (venv-c1score, kit B), because B2 needs the chosen configuration.
# Staged before (operator, one LOG checklist line, no host string), under $NCS_DATA/datasets, and only after BD-T1
# tier 1 has finished and cleaned up (CC-172 W5; A and B jobs pre-empt this job: stop it between steps, unstage
# ktvic/ and openviic/, resume later from the .done/partial files; after C-T1, delete ktvic/ and openviic/, logged):
#   ktvic/, openviic/ (as for C stage 2), c_t1_f30k_carve/{images,manifest.json,carve_refs.json},
#   c_t1_f30k_memory/{images,manifest.json,f30k_memory_captions.json} (both from M1's train-only .tar, extracted by list, the .tar
#   deleted before this job: W4), cen_memory/images (ALL 111,927 members[0], per file, never an archive: W10),
#   c_t1_mem/{memfiles_vi.json,memfiles_coco.json,coco_captions.json} (caption stores: never in the repo).
# Snapshots fetched beforehand with `c_t1.py fetch` (writes .c_t1_ok; models with open pins are skipped, W9).
# Usage, inside tmux:  bash scripts/c_t1/c_t1_job.sh <expected 40-hex HEAD>
set -euo pipefail
EXPECT=${1:?usage: c_t1_job.sh <expected HEAD>}
[ "$(cat /root/.vsps_machine_id 2>/dev/null)" = m4 ] || { echo "REFUSED: /root/.vsps_machine_id is not m4"; exit 1; }
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=m4
LB=/root/venv-lb/bin/python; T1=/root/venv-t1/bin/python; SC=/root/venv-c1score/bin/python; PY=/root/vsps/.venv/bin/python
LB_FREEZE=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784   # setup_gpu.sh H_LB
T1_FREEZE=${T1_FREEZE:?set T1_FREEZE to the judge-read venv-t1 freeze sha256}   # W-item: recorded at build
X=scripts/c_t1/c_t1.py; JOB=scripts/c_t1/c_t1_job.sh
O=/root/outputs/c_t1; P=$O/out; LOG=$O/logs; USED=$O/gpu_seconds.tsv; MARK=$O/CAP_STOP.json
DS=$NCS_DATA/datasets; MEM=$DS/c_t1_mem; CARVE=$DS/c_t1_f30k_carve; F30M=$DS/c_t1_f30k_memory
CEN=/root/outputs/c_en   # C-EN memory record and SigLIP2 vectors (restored from the backup, sha-checked below)
CS1=/root/outputs/c_stage1; CS2=/root/outputs/c_stage2   # C's embeddings and example files (restored, sha-checked)
CL=manuscript/prereg/2026-10-22_c_stage1/lists.json
SIG=$NCS_DATA/models/siglip2; XG=$NCS_DATA/models/c_t1_xglm_2_9b; MC=$NCS_DATA/models/c_t1_mclip_h14
snap() { echo $NCS_DATA/models/c_t1_$1; }
export C_T1_LOCK=$O/RUNNING VSPS_JOB_SHA256=$(sha256sum $JOB | cut -c1-64)
mkdir -p $O $P $LOG
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*" | tee -a $LOG/job.log; }
stop() { say "JOB STOP $*"; exit 1; }
$PY $X lock --path $C_T1_LOCK || exit 1
trap 'rm -f $C_T1_LOCK' EXIT

# ---------------------------------------------------------------- preflight
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
sha256sum --quiet -c scripts/c_t1/SHA256SUMS || stop "scripts/c_t1/SHA256SUMS"
sha256sum --quiet -c manuscript/prereg/2026-10-30_c_t1/SHA256SUMS || stop "prereg SHA256SUMS"
sha256sum --quiet -c manuscript/prereg/2026-10-30_c_t1/RESTORED_SHA256 || stop "restored C/C-EN artefacts differ"
[ "$(/root/venv-lb/bin/pip freeze | sha256sum | cut -c1-64)" = $LB_FREEZE ] || stop "venv-lb freeze differs"
[ "$(/root/venv-t1/bin/pip freeze | sha256sum | cut -c1-64)" = $T1_FREEZE ] || stop "venv-t1 freeze differs"
$LB $X --selftest >> $LOG/selftest.log 2>&1 || stop "c_t1 selftest (venv-lb)"
$SC $X --selftest >> $LOG/selftest.log 2>&1 || stop "c_t1 selftest (venv-c1score, the scorer's venv; W8)"
$PY $X guard --roots $NCS_DATA /root/outputs >> $LOG/guard.log 2>&1 || stop "custody guard (W4)"
$PY $X memcheck --mem-files $MEM/memfiles_vi.json --root $DS >> $LOG/memcheck.log 2>&1 || stop "memcheck vi (W10)"
$PY $X memcheck --mem-files $MEM/memfiles_coco.json --root $DS/cen_memory/images >> $LOG/memcheck.log 2>&1 || stop "memcheck coco (W10)"
for m in xglm_2_9b mclip_h14; do $PY $X pinsok --model $m --snapshot $(snap $m) >> $LOG/pins.log 2>&1 || stop "$m snapshot"; done
HF_HUB_OFFLINE=1 $T1 $X t1check --mclip $MC >> $LOG/t1check.log 2>&1 || stop "venv-t1 open_clip offline (W8)"
sha256sum $X $JOB > $O/code_at_start.sha256
say "JOB START head $EXPECT"

finish() {
  (cd $O && find out logs -type f ! -name '*.partial*' | sort | xargs -r sha256sum) > $O/SHA256SUMS
  say "JOB DONE gpu_h $(awk '$2 != "start" {s += $2} END {printf "%.2f", s / 3600}' $USED)"; exit 0; }
cap_stop() { [ -e $MARK ] || printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > $MARK; say "CAP STOP $1"; finish; }
gpu() {  # gpu NAME CMD...: one GPU step under the time left; rc 3 is returned, any other failure stops
  local name=$1; shift
  [ -s $LOG/$name.done ] && return 0
  local t; t=$($PY $X left --used $USED --marker $MARK) || stop "cap arithmetic"
  [ "$t" -gt 0 ] || cap_stop "20 GPU-h cap before $name"
  say "START $name (left $((t / 60)) min)"
  local t0 rc=0; t0=$(date +%s)
  echo "$name start $t0" >> $USED
  timeout ${t}s "$@" >> $LOG/$name.log 2>&1 || rc=$?
  echo "$name $(( $(date +%s) - t0 ))" >> $USED
  [ $rc = 124 ] && cap_stop "20 GPU-h cap reached during $name"
  [ $rc = 0 ] && { say "OK $name"; date -u +%FT%TZ > $LOG/$name.done; return 0; }
  [ $rc = 3 ] && { say "RC3 $name"; return 3; }
  [[ $name == S_* ]] && { say "SMOKE FAIL $name rc=$rc (non-fatal, N-b)"; date -u +%FT%TZ > $LOG/$name.done; return 0; }
  stop "$name rc=$rc"
}
dec() {  # dec NAME MODEL SET ARM [extra args]: one decode
  local name=$1 m=$2 s=$3 arm=$4; shift 4
  local snapdir; snapdir=$( [ $m = qwen25vl_7b ] || [ $m = internvl3_8b ] && echo $NCS_DATA/models/$m || snap $m )
  gpu $name $LB $X decode --model $m --set $s --arm $arm --snapshot $snapdir --out-dir $P --c-lists $CL "$@"
}
VI_IMG=(--images $DS); OVB_EX=$P/x1_ov_dev_b.json; KT_EX=$P/x1_ktvic_dev299.json
EN_IMG=(--images $CARVE/images --manifest $CARVE/manifest.json); CARVE_EX=$P/x1_f30k_carve_coco.json
EN_MEM=(--captions $MEM/coco_captions.json --memory coco)

# ---------------------------------------------------------------- B0: vectors and example lists (CPU parity first)
$PY $X draws --mem-emb $CS1/emb.npz --query-emb $CS2/emb_ov_dev_b.npz --set ov_dev_b --ex $CS2/ex_ov_dev_b.json --out $OVB_EX >> $LOG/draws.log 2>&1 || stop "X1 parity ov_dev_b"
$PY $X draws --mem-emb $CS1/emb.npz --query-emb $CS1/emb.npz --set ktvic_dev299 --ex $CS1/exemplars.json --out $KT_EX >> $LOG/draws.log 2>&1 || stop "X1 parity ktvic_dev299"
gpu B0_embed_carve $LB $X embed --set f30k_carve --images $CARVE/images --snapshot $SIG --manifest $CARVE/manifest.json --out $P/emb_f30k_carve.npz
$PY $X draws --mem-emb $CEN/cen_memory_emb.npz --query-emb $P/emb_f30k_carve.npz --set f30k_carve --out $CARVE_EX >> $LOG/draws.log 2>&1 || stop "draws f30k_carve"

# ---------------------------------------------------------------- smoke (W-d / N7): timing only, never scored
SM=$O/smoke; mkdir -p $SM
for m in aya_vision_8b gemma3_4b idefics3_8b; do
  $PY $X pinsok --model $m --snapshot $(snap $m) >> $LOG/pins.log 2>&1 || continue
  gpu S_${m}_zs $LB $X decode --model $m --set f30k_carve --arm zs --snapshot $(snap $m) --out-dir $SM --limit 16 "${EN_IMG[@]}"
  gpu S_${m}_img $LB $X decode --model $m --set f30k_carve --arm ret_img --k 8 --order first --tpl T1 --ex $CARVE_EX \
    --snapshot $(snap $m) --out-dir $SM --limit 16 --mem-images $DS/cen_memory/images --mem-files $MEM/memfiles_coco.json "${EN_MEM[@]}" "${EN_IMG[@]}"
  break
done
gpu S_lmcap $T1 $X lmcap --set f30k_carve --variant ri --xglm $XG --mclip $MC --mem-emb $CEN/cen_memory_emb.npz --limit 16 \
  --query-emb $P/emb_f30k_carve.npz --ex $CARVE_EX --mem-images $DS/cen_memory/images --mem-files $MEM/memfiles_coco.json \
  --out-dir $SM "${EN_MEM[@]}" "${EN_IMG[@]}"
say "SMOKE seconds: $(grep '^S_' $USED | awk '$2 != "start"' | tr '\n' ' ')"

# ---------------------------------------------------------------- B1: third backbone, Vietnamese check and selection
TB=""
for m in aya_vision_8b gemma3_4b idefics3_8b; do   # fallback order (PREREG §6.1)
  $PY $X pinsok --model $m --snapshot $(snap $m) >> $LOG/pins.log 2>&1 || { say "SKIP $m (pins open or not fetched; W9)"; continue; }
  dec B1_${m}_kt_zs $m ktvic_dev299 zs "${VI_IMG[@]}"
  $PY $X vicheck --preds $P/t1_${m}_ktvic_dev299-zs.preds.json >> $LOG/vicheck.log 2>&1 || { say "NOT VIETNAMESE-ASSESSABLE $m"; continue; }
  for c in "2 first T1" "2 last T1" "4 first T1" "4 last T1" "8 first T1" "8 last T1" "4 last T2"; do set -- $c
    dec B1_${m}_kt_k$1$2$3 $m ktvic_dev299 ret --k $1 --order $2 --tpl $3 --ex $KT_EX --memory vi "${VI_IMG[@]}"
  done
  rm -f $O/ledger_kt_$m.jsonl   # W6: written fresh on every (re)run
  $SC $X score --set ktvic_dev299 --runs $P/t1_${m}_ktvic_dev299-*.preds.json --ledger $O/ledger_kt_$m.jsonl --kit-b scripts/kit_b --c-lists $CL >> $LOG/score_kt.log 2>&1 || stop "score ktvic_dev299 $m"
  rc=0; $PY $X select --ledger $O/ledger_kt_$m.jsonl --model $m --out $O/t_config.json >> $LOG/select.log 2>&1 || rc=$?
  [ $rc = 0 ] && { TB=$m; break; }
  [ $rc = 3 ] && { say "FAILS SELECTION $m (C's stage-A rule, W1)"; continue; }
  stop "select $m rc=$rc"
done
if [ -n "$TB" ]; then
  read -r TK TO TT < <($PY $X cfg --file $O/t_config.json)
  say "THIRD BACKBONE $TB k=$TK order=$TO tpl=$TT tau=-inf"
else
  say "THIRD BACKBONE NOT RUN (no backbone passed §6.2 and W1); the other blocks continue (N8)"
fi

# ---------------------------------------------------------------- B2: third backbone on OV-dev-B
if [ -n "$TB" ]; then
  dec B2_${TB}_ovb_zs $TB ov_dev_b zs "${VI_IMG[@]}"
  dec B2_${TB}_ovb_ret $TB ov_dev_b ret --k $TK --order $TO --tpl $TT --ex $OVB_EX --memory vi "${VI_IMG[@]}"
  dec B2_${TB}_ovb_rand $TB ov_dev_b rand --k $TK --tpl $TT --draw 0 --ex $OVB_EX --memory vi "${VI_IMG[@]}"
fi

# ---------------------------------------------------------------- B3: LMCap re-implementation (both variants)
for v in ri se; do
  gpu B3_lmcap_${v}_ovb $T1 $X lmcap --set ov_dev_b --variant $v --xglm $XG --mclip $MC --mem-emb $CS1/emb.npz --query-emb $CS2/emb_ov_dev_b.npz \
    --ex $OVB_EX --c-lists $CL --mem-images $DS --mem-files $MEM/memfiles_vi.json --memory vi --out-dir $P "${VI_IMG[@]}"
  gpu B3_lmcap_${v}_carve $T1 $X lmcap --set f30k_carve --variant $v --xglm $XG --mclip $MC --mem-emb $CEN/cen_memory_emb.npz \
    --query-emb $P/emb_f30k_carve.npz --ex $CARVE_EX --mem-images $DS/cen_memory/images --mem-files $MEM/memfiles_coco.json \
    --out-dir $P "${EN_MEM[@]}" "${EN_IMG[@]}"
done

# ---------------------------------------------------------------- B4: Flickr30K carve, English, frozen configs, COCO memory
THIRD4=(); [ -n "$TB" ] && THIRD4=("$TB $TK $TO $TT")
for spec in "qwen25vl_7b 8 first T1" "internvl3_8b 4 last T2" "${THIRD4[@]}"; do set -- $spec
  dec B4_$1_carve_zs $1 f30k_carve zs "${EN_IMG[@]}"
  dec B4_$1_carve_ret $1 f30k_carve ret --k $2 --order $3 --tpl $4 --ex $CARVE_EX "${EN_MEM[@]}" "${EN_IMG[@]}"
  dec B4_$1_carve_rand $1 f30k_carve rand --k $2 --tpl $4 --draw 0 --ex $CARVE_EX "${EN_MEM[@]}" "${EN_IMG[@]}"
done

# ---------------------------------------------------------------- B5: X1 extra rand draws on OV-dev-B (draw 0 = C's own)
THIRD3=(); [ -n "$TB" ] && THIRD3=("$TB $TK $TT")
for spec in "qwen25vl_7b 8 T1" "internvl3_8b 4 T2" "${THIRD3[@]}"; do set -- $spec
  for d in 1 2; do dec B5_$1_ovb_rand_d$d $1 ov_dev_b rand --k $2 --tpl $3 --draw $d --ex $OVB_EX --memory vi "${VI_IMG[@]}"; done
done

# ---------------------------------------------------------------- B6: RICES-format interleaved examples (same examples)
dec B6_qwen_ovb_img qwen25vl_7b ov_dev_b ret_img --k 8 --order first --tpl T1 --ex $OVB_EX --memory vi --mem-images $DS --mem-files $MEM/memfiles_vi.json "${VI_IMG[@]}"
dec B6_qwen_carve_img qwen25vl_7b f30k_carve ret_img --k 8 --order first --tpl T1 --ex $CARVE_EX --mem-images $DS/cen_memory/images --mem-files $MEM/memfiles_coco.json "${EN_MEM[@]}" "${EN_IMG[@]}"
[ -n "$TB" ] && dec B6_${TB}_carve_img $TB f30k_carve ret_img --k $TK --order $TO --tpl $TT --ex $CARVE_EX --mem-images $DS/cen_memory/images --mem-files $MEM/memfiles_coco.json "${EN_MEM[@]}" "${EN_IMG[@]}"

# ---------------------------------------------------------------- B7: X5 memory swap (Flickr30K-train memory, same carve)
gpu B7_embed_f30k_memory $LB $X embed --set f30k_memory --images $F30M/images --snapshot $SIG --manifest $F30M/manifest.json --out $P/emb_f30k_memory.npz
$PY $X draws --mem-emb $P/emb_f30k_memory.npz --query-emb $P/emb_f30k_carve.npz --set f30k_carve --out $P/x1_f30k_carve_f30k.json >> $LOG/draws.log 2>&1 || stop "draws f30k memory"
F30_MEM=(--captions $F30M/f30k_memory_captions.json --memory f30k)
for spec in "qwen25vl_7b 8 first T1" "${THIRD4[@]}"; do set -- $spec
  dec B7_$1_carve_ret_f30k $1 f30k_carve ret --k $2 --order $3 --tpl $4 --ex $P/x1_f30k_carve_f30k.json "${F30_MEM[@]}" "${EN_IMG[@]}"
  dec B7_$1_carve_rand_f30k $1 f30k_carve rand --k $2 --tpl $4 --draw 0 --ex $P/x1_f30k_carve_f30k.json "${F30_MEM[@]}" "${EN_IMG[@]}"
done
finish
