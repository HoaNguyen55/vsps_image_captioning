#!/bin/bash
# Paper B, B-2 (DESCRIPTIVE ONLY) on M3: the pinned class-(b) checkpoints and the UIT-ViIC test images are fetched
# (CPU, not charged to the cap), then each system is decoded once on the one test split it reports on (GPU).
# PREREG manuscript/prereg/2026-10-28_b2_external/PREREG.md (CC-126 W13). No scoring and no reference on M3.
# Cap: no GPU step starts after 2.5 GPU-h; every GPU step runs under `timeout` up to 3 GPU-h in total; a timeout or
# the soft cap is a CAP STOP, final (CAP_STOP.json). A load failure (rc 4, LOADFAIL json) makes that system class (c)
# and the job goes on; so does an immediate eos on both smoke inputs (rc 5, SMOKEFAIL json; Amendment 1, CC-138 W4).
# Any other failure is a JOB STOP back to the judge.
# Usage, inside tmux b2 on M3, after b2_chain.sh stage took the lock and staged /root/ncs-data/b2_stage:
#   bash scripts/b2_external/b2_job.sh <expected 40-hex HEAD>
EXPECT=${1:?usage: b2_job.sh <expected HEAD>}
cd /root/vsps || exit 1
export NCS_DATA=/root/ncs-data VSPS_MACHINE_ID=$(tr -d '[:space:]' < /root/.vsps_machine_id)
LB=/root/venv-lb/bin/python; X=scripts/b2_external/b2.py
LB_FREEZE=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784   # setup_gpu.sh H_LB
O=/root/outputs/b2_external; LOG=$O/logs; USED=$O/gpu_seconds.tsv; MARK=$O/CAP_STOP.json; P=$O/preds
ST=/root/ncs-data/b2_stage   # CC-132 W1: under NCS_DATA (grl guards refuse while staged; not mirrored)
mkdir -p $LOG $P
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*" | tee -a $LOG/job.log; }
stop() { say "JOB STOP $*"; exit 1; }
finish() { (cd $O && find preds logs -type f ! -path logs/job.log | sort | xargs -d '\n' sha256sum > SHA256SUMS); say "BLOCK DONE"; exit 0; }

# ---------------------------------------------------------------- preflight (PREREG §5)
[ -e $O/RUNNING ] || stop "no B-2 lock: run b2_chain.sh stage first"
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
sha256sum --quiet -c scripts/b2_external/SHA256SUMS || stop "scripts/b2_external/SHA256SUMS does not verify"
sha256sum --quiet -c manuscript/prereg/2026-10-28_b2_external/SHA256SUMS || stop "prereg SHA256SUMS"
[ "$(/root/venv-lb/bin/pip freeze | sha256sum | cut -c1-64)" = $LB_FREEZE ] || stop "venv-lb freeze differs"
G() { $LB $X guard --head "$EXPECT" >> $LOG/guard.log 2>&1 || stop "guard (host, GPU, C-EN, locks, tmux)"; }
G
for s in ktvic openviic; do
  [ "$(wc -l < $ST/lists/$s.tsv)" -gt 0 ] || stop "no $s list"
  (cd $ST/images/$s && awk -F'\t' '{print $3"  "$2}' $ST/lists/$s.tsv | sha256sum --quiet -c -) || stop "$s images"
done
$LB -c "import sys; sys.path.insert(0, 'scripts/grl'); import common as K; c = K.cen_test_shas(); \
sys.exit(any(l.split('\t')[2].strip() in c for s in ('ktvic', 'openviic') for l in open(f'$ST/lists/{s}.tsv')))" \
  || stop "a staged KTVIC or OpenViIC test image is in C-EN's test-side records (incl. nocaps_val)"
sha256sum $X scripts/b2_external/b2_job.sh > $O/code_at_start.sha256
say "JOB START head $EXPECT"

# ---------------------------------------------------------------- fetch (CPU, online, not charged)
for sid in K5 K1 K6; do
  [ -e $ST/hf/$sid.ok ] && continue
  HF_HUB_OFFLINE=0 $LB $X hf-fetch --sid $sid --dest $ST/hf >> $LOG/fetch.log 2>&1 || stop "hf-fetch $sid"
  touch $ST/hf/$sid.ok
done
$LB $X uit-fetch --list $ST/lists/uitviic.tsv --dest $ST/images/uitviic >> $LOG/fetch.log 2>&1 \
  || stop "uit-fetch (UIT-ViIC test images by coco_url, C-EN overlap refused)"
cp $ST/images/uitviic.sha.tsv $O/uitviic_test_images.sha256.tsv
$LB $X smoke-fetch --dest $ST/smoke >> $LOG/fetch.log 2>&1 || stop "smoke-fetch (pinned UIT-ViIC train image 368)"
say "FETCH OK: 3 snapshots verified, 231 UIT-ViIC test images, smoke image 368 pinned"

# ---------------------------------------------------------------- decode (GPU, one per system, priority order)
cap_stop() { [ -e $MARK ] || printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > $MARK; say "CAP STOP $1"; finish; }
gpu() {  # gpu NAME CMD...: one GPU step; no start after 2.5 GPU-h, killed at 3; wall seconds -> gpu_seconds.tsv
  local name=$1; shift
  local t; t=$($LB $X left --used $USED --marker $MARK) || stop "cap arithmetic"
  [ "$t" -gt 0 ] || cap_stop "2.5 GPU-h soft cap before $name"
  G; say "START $name (timeout $((t / 60)) min)"
  local t0; t0=$(date +%s)
  echo "$name start $t0" >> $USED
  HF_HUB_OFFLINE=1 timeout ${t}s "$@" >> $LOG/$name.log 2>&1; local rc=$?
  echo "$name $(( $(date +%s) - t0 ))" >> $USED
  [ $rc = 0 ] && { say "OK $name"; return 0; }
  [ $rc = 4 ] && { say "LOADFAIL $name: class (c) by the load rule"; return 0; }
  [ $rc = 5 ] && { say "SMOKEFAIL $name: not runnable, immediate eos on both smoke inputs (class (c))"; return 0; }
  [ $rc = 124 ] && cap_stop "3 GPU-h hard cap reached during $name"
  stop "$name rc=$rc"
}
declare -A SET=([K5]=uitviic [K1]=ktvic [K6]=openviic)
for sid in K5 K1 K6; do  # smoke (PREREG §5.2, Amendment 1): load, round trip, grey + train image 368; no test image
  [ -e $P/$sid.smoke.json ] || [ -e $P/$sid.LOADFAIL.json ] || [ -e $P/$sid.SMOKEFAIL.json ] && continue
  TOK=(); [ $sid = K1 ] && TOK=(--tok $ST/hf/K1_tok)
  gpu smoke_$sid $LB $X smoke --sid $sid --snap $ST/hf/$sid "${TOK[@]}" --img2 $ST/smoke/000000000368.jpg \
    --out $P/$sid.smoke.json
done
say "SMOKE DONE: $(ls $P/*.smoke.json 2>/dev/null | wc -l) ok, $(ls $P/*.LOADFAIL.json 2>/dev/null | wc -l) LOADFAIL," \
  "$(ls $P/*.SMOKEFAIL.json 2>/dev/null | wc -l) SMOKEFAIL"
for sid in K5 K1 K6; do
  [ -e $P/$sid.preds.json ] || [ -e $P/$sid.LOADFAIL.json ] || [ -e $P/$sid.SMOKEFAIL.json ] && continue
  s=${SET[$sid]}; L=$ST/lists/$s.tsv; [ $s = uitviic ] && L=$ST/images/uitviic.sha.tsv
  TOK=(); [ $sid = K1 ] && TOK=(--tok $ST/hf/K1_tok)
  gpu dec_$sid $LB $X decode --sid $sid --snap $ST/hf/$sid "${TOK[@]}" --images $ST/images/$s --list $L \
    --out $P/$sid.preds.json
done
finish
