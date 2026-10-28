#!/bin/bash
# N9 rescue on M3: manuscript/prereg/2026-10-28_n9_rescue_addendum.md (CC-140 r3, CC-142 W1, PI-1026ao/ap).
# Decode only. No method output is scored or read on M3, and no COCO caption file is on M3 (K_F runs on the laptop).
# One lock, /root/outputs/n9_rescue/RUNNING, is held from stage to cleanup, so no other M3 job runs in between.
#   stage             refuses on any other lock, a B-2 stage or a GPU process; takes the lock; fetches the nine pinned
#                     snapshots and the 500 CHAIR-500 val2014 images into /root/ncs-data/n9_stage (sha-checked). CPU.
#   base A            A = 1: batch 1, 512 new tokens; A = 2: batch 1, 1024 new tokens, only if trigger2 passes on a1.
#                     Decodes n9_base into $O/aA/. The operator pulls it; K_F runs on the laptop; aA/kf.json comes back.
#   methods A         only with a K_F PASS for attempt A: cap + start rule (n9_rescue.py plan), then the 7 other runs
#                     of prereg §1 in its order, each under timeout = the remaining cap. A CAP STOP is final.
#   cleanup REASON    removes /root/ncs-data/n9_stage, checks it is gone, releases the lock (outputs stay).
# Usage (M3, /root/vsps, inside tmux n9):
#   bash scripts/lvlm/n9_rescue_job.sh stage|base|methods|cleanup <A or REASON> <expected 40-hex HEAD>
#   bash scripts/lvlm/n9_rescue_job.sh --selftest            (CPU, repo root)
if [ "$1" = "--selftest" ]; then
  bash -n "$0" && python3 scripts/lvlm/n9_rescue.py --selftest && sha256sum --quiet -c scripts/lvlm/SHA256SUMS \
    && [ "$(sha256sum < scripts/lvlm/venv_n9_freeze.txt | cut -c1-64)" = "$(grep -o '^H_N9=[0-9a-f]*' "$0" | cut -c6-)" ] \
    && echo "n9_rescue_job selftest ok"
  exit
fi
STAGE=${1:?stage}; A=${2:?attempt 1 or 2, or a cleanup reason}; EXPECT=${3:?expected HEAD}
case "$STAGE" in stage|cleanup) ;; base|methods) case "$A" in 1|2) ;; *) echo "attempt must be 1 or 2"; exit 1 ;; esac ;;
  *) echo "usage: stage|base|methods|cleanup A|REASON HEAD"; exit 1 ;; esac
cd /root/vsps || exit 1
export NCS_DATA=/root/ncs-data VSPS_MACHINE_ID=$(tr -d '[:space:]' < /root/.vsps_machine_id)
VN=/root/venv-n9; PY=$VN/bin/python; FRZ=scripts/lvlm/venv_n9_freeze.txt   # amendment 1; /root/vsps/.venv untouched
H_N9=193d4cc337451c548dc6c4f2ba9079c97e5682896115b43f8c0eaa1d7875fb4e   # sha256 of $FRZ = setup_gpu.sh H_VS + protobuf
H=scripts/lvlm/n9_rescue.py; DL=scripts/lvlm/decode_llava.py; IDS=data/coco_probe/chair500_ids.txt
MAN=data/coco_probe/chair500_val2014.sha256
O=/root/outputs/n9_rescue; LOCK=$O/RUNNING; L=$O/gpu_seconds.tsv; LOG=$O/logs
ST=/root/ncs-data/n9_stage; IMG=$ST/images; D=$O/a$A
mkdir -p $LOG
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) [$STAGE $A] $*" | tee -a $LOG/job.log; }
stop() { say "JOB STOP $*"; exit 1; }

# ---------------------------------------------------------------- preflight (addendum §4, §5)
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
sha256sum --quiet -c scripts/lvlm/SHA256SUMS || stop "scripts/lvlm/SHA256SUMS does not verify"
OTHER=$(ls /root/outputs/*/RUNNING 2>/dev/null | grep -vx "$LOCK")
[ -z "$OTHER" ] || stop "another lock exists: $OTHER"
[ ! -e /root/ncs-data/b2_stage ] || stop "/root/ncs-data/b2_stage exists: B-2 cleanup is not done"
if [ $STAGE = cleanup ]; then
  [ -e $LOCK ] || stop "no N9 lock"
  rm -rf $ST; [ ! -e $ST ] || stop "$ST still exists"
  rm -f $LOCK; say "N9 CLEANUP ($A): $ST removed, lock released"; exit 0
fi
python3 $H clock || stop "past the 11-08 hard stop: N9 is final NOT-TESTABLE (run cleanup)"
[ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ] || stop "a GPU process is running"
B=liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234
V=openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1
P1=YiyangAiLab/llava_POVID_stage_one_lora@d6c79d54be16246404f910a4453eb64b8b31af25
P2=YiyangAiLab/llava_POVID_stage_two_lora@bdb48949e04cf7605a606b7159726ac161f96b25
RL=openbmb/RLAIF-V-7B@90e8e7338297c7ee753ae706b1571d46225c5c19
CD=aimagelab/CHAIR-DPO_LLaVA-1.5-7B@bd9ab77aa0f9183ad1a30e4cc8cecc2cd2b175b8
SE=psp-dada/LLaVA-v1.5-7B-SENTINEL@016b6dced6c24bd26b3736a8cab23ea874dca7c7
HA=juliozhao/hadpo-llava-1.5@72b1bcf8d86e60937e1df1ca1386d1c97bf95eb1
OP=zhyang2226/opadpo-lora_llava-v1.5-7b@f589492241ddfaf195cdedd20781edfa8d072717

if [ $STAGE = stage ]; then
  [ -e $LOCK ] || { mkdir -p $O && ( set -o noclobber; echo "n9_rescue_job stage $EXPECT $(ts)" > $LOCK ) 2>/dev/null; } \
    || stop "could not take $LOCK"
  say "N9 LOCK held until cleanup"
  for r in $B $V $P1 $P2 $RL $CD $SE $HA $OP; do
    HF_HUB_OFFLINE=0 /root/venv-lb/bin/hf download ${r%@*} --revision ${r#*@} >> $LOG/fetch.log 2>&1 || stop "fetch $r"
  done
  mkdir -p $IMG
  awk '{print $2}' $MAN | while read -r f; do
    [ -s $IMG/$f ] || curl -sSf -o $IMG/$f http://images.cocodataset.org/val2014/$f || exit 1
  done || stop "image fetch"
  (cd $IMG && sha256sum -c --quiet /root/vsps/$MAN) || stop "CHAIR-500 images differ from the manifest"
  say "STAGE OK: 9 pinned snapshots, 500 CHAIR-500 images sha-checked"; exit 0
fi
[ -e $LOCK ] || stop "no N9 lock: run stage first"
if [ ! -e $VN ]; then  # built once, as setup_gpu.sh mkvenv builds .venv (CPU, online, not charged)
  say "building $VN from $FRZ"
  { python3.10 -m venv $VN && grep -v '^py_vncorenlp==' $FRZ > $O/venv_n9.rest \
    && $VN/bin/pip install -q --no-deps --index-url https://pypi.org/simple \
         --extra-index-url https://download.pytorch.org/whl/cu121 -r $O/venv_n9.rest \
    && { ! grep -q '^py_vncorenlp==' $FRZ || $VN/bin/pip install -q --no-deps --use-pep517 $(grep '^py_vncorenlp==' $FRZ); }
  } >> $LOG/venv_n9.log 2>&1 || stop "building $VN failed: remove $VN before a retry"
fi
[ "$($VN/bin/pip freeze | sha256sum | cut -c1-64)" = $H_N9 ] || stop "$VN freeze differs from $FRZ"
$VN/bin/pip check >> $LOG/venv_n9.log 2>&1 || stop "$VN pip check"
(cd $IMG && sha256sum -c --quiet /root/vsps/$MAN) || stop "CHAIR-500 images differ from the manifest"
mkdir -p $D
$PY $DL --selftest >> $LOG/selftest.log 2>&1 || stop "decode_llava selftest"
export HF_HUB_OFFLINE=1
NEW=$([ $A = 2 ] && echo 1024 || echo 512)

# gpu NAME TIMEOUT_S --base REPO@REV [flags]: one decode into $D, wall seconds charged to the ledger
gpu() {
  local name=$1 t=$2; shift 2
  [ -e $D/$name.json ] && { say "SKIP $name (output exists)"; return 0; }
  [ "$t" -gt 0 ] || { touch $D/CAP_STOP; say "CAP STOP before $name: N9 is final NOT-TESTABLE"; exit 1; }
  local t0; t0=$(date +%s); printf '%s\tstart\t%s\n' a$A/$name $t0 >> $L
  say "START $name (timeout $((t / 60)) min, batch 1, $NEW new tokens)"
  timeout ${t}s $PY $DL --label $name --out $D/$name.json --image-ids $IDS --image-dir $IMG --vision $V "$@" \
    --max-new-tokens $NEW --batch-size 1 >> $LOG/a$A.$name.log 2>&1; local rc=$?
  printf '%s\tend\t%s\n' a$A/$name $(( $(date +%s) - t0 )) >> $L
  [ $rc = 124 ] && { touch $D/CAP_STOP; say "CAP STOP during $name: N9 is final NOT-TESTABLE"; exit 1; }
  [ $rc = 0 ] || stop "$name rc=$rc"
  say "OK $name $(sha256sum < $D/$name.json | cut -c1-16)"
}

if [ $STAGE = base ]; then
  if [ $A = 2 ]; then
    python3 $H trigger2 --dir $O/a1 | tee -a $LOG/job.log \
      || stop "attempt 2 is void (attempt 1 passed, or no base caption reached 512 tokens): N9 is final NOT-TESTABLE"
  fi
  U=$(python3 $H used --ledger $L) || stop "ledger"
  gpu n9_base $(( 6 * 3600 - U )) --base $B
  say "BASE DONE attempt $A: pull $D/n9_base.json, run K_F on the laptop (addendum §5 step 2), put kf.json in $D"
  exit 0
fi

# methods: K_F PASS on this attempt's base, then the cap and the start rule, fixed before any method decode
python3 $H kfok --dir $D || stop "no K_F PASS for attempt $A"
for f in START_RULE_STOP.json CAP_STOP; do [ -e $D/$f ] && stop "$D/$f exists: N9 is final NOT-TESTABLE"; done
if [ ! -e $D/cap.json ]; then
  python3 $H plan --ledger $L --attempt $A > $D/plan.json; rc=$?
  say "PLAN $(cat $D/plan.json)"
  [ $rc = 0 ] || { mv $D/plan.json $D/START_RULE_STOP.json; say "START RULE: no method decode starts; N9 is final NOT-TESTABLE"; exit 1; }
  mv $D/plan.json $D/cap.json
fi
run() { local name=$1 t; shift; t=$(python3 $H left --ledger $L --attempt $A) || stop "ledger"; gpu $name $t "$@"; }
run n9_povid --base $B --lora $P1 --lora $P2 --drop-vision-lora
run n9_rlaifv --base $RL
run n9_chairdpo --base $CD
run n9_sentinel --base $B --lora $SE
run n9_hadpo --base $B --lora $HA
run n9_opadpo --base $B --lora $OP
run n9_povid_fullmerge --base $B --lora $P1 --lora $P2
(cd $D && sha256sum n9_*.json kf.json cap.json > SHA256SUMS)
say "METHODS DONE attempt $A: run cleanup, pull $D, score once on the laptop (addendum §5 step 4)"
