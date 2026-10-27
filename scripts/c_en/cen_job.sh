#!/bin/bash
# M3: C-EN (Paper C, English arm), manuscript/prereg/2026-10-27_c_en/PREREG.md §9-§10. One block per call; the
# laptop chain (cen_chain.sh) uploads the caption store and reference subsets, mirrors and deletes around each block.
#   pool    SigLIP2 vectors of the memory images (GPU; cap 3 GPU-h; measured-rate guard inside cen_pool.py)
#   feats   pHash/dHash/SSCD of the memory, then each protected set staged at its recorded sha, hashed, deleted (CPU)
#   build   memory-side near-duplicate drops, clusters, members[0] vectors (CPU)
#   smoke   CC-113 r5 format/guard check on 16 memory images, no score (GPU; cap 0.5 GPU-h)
#   coco    stage, query embed, examples, 6 decodes, InternVL3 items + verifier, score, decide once (GPU; test cap)
#   nocaps  the same, whatever COCO showed (PREREG §7); test cap 25 GPU-h shared with coco
# GPU-h are job wall time with an open record and heartbeat that a hard kill cannot lose (as c_test_job.sh). Every
# step runs under `timeout` for the time left; 3 attempts, then JOB STOP; a cap stop is final for its family. The
# log carries counts, times and return codes only.
# Usage: cen_job.sh <expected 40-hex HEAD> pool|feats|build|smoke|coco|nocaps          cen_job.sh --selftest
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*"; }
stop() { say "JOB STOP $*"; exit 1; }
fam() { case $1 in pool) echo pool ;; smoke) echo smoke ;; coco|nocaps) echo test ;; *) echo cpu ;; esac; }
cap_of() { case $1 in pool) echo $((3 * 3600)) ;; smoke) echo 1800 ;; test) echo $((25 * 3600)) ;; *) echo $((24 * 3600)) ;; esac; }
cap_stop() {  # final for a GPU family; a CPU step that runs out of time goes back to the operator (no ruled CPU cap)
  [ "$FAM" = cpu ] && { echo "$(ts) $BLOCK $*" >> $O/CPU_TIMEOUT; stop "CPU step out of time: $* (no cap stop; \
cleanup feats, then back to the operator; CC-121 W5)"; }
  echo "$(ts) $FAM $*" >> $O/CAP_STOP_$FAM; stop "$*"; }
used() {  # closed records of this family plus open ones up to their last heartbeat; fail closed on a bad record
  local s r t0 hb; s=$(awk -v f=$FAM '$1 == f {s += $2} END {print s + 0}' $O/gpu_seconds.tsv)
  for r in $O/gpu_open_${FAM}_*.rec; do
    [ -e "$r" ] || continue
    t0=$(cut -d' ' -f2 "$r"); hb=$(cat "${r%.rec}.hb" 2>/dev/null || echo $t0)
    for x in "$t0" "$hb"; do case $x in ''|*[!0-9]*) return 1 ;; esac; done
    s=$((s + hb - t0))
  done
  echo $s
}
left() { echo $((CAP - BEFORE - ($(date +%s) - T0))); }
capped() { [ $1 = 124 ] || { [ $1 = 137 ] && [ "$(left)" -le "${MIN_LEFT:-60}" ]; }; }
step() {  # step NAME CMD...: up to 3 attempts under the time left; rc 3 of a verifier is the registered stop
  local name=$1; shift
  for a in 1 2 3; do
    local t; t=$(left); [ "$t" -gt "${MIN_LEFT:-60}" ] || cap_stop "cap before $name"
    say "START $name attempt $a (left $((t / 60)) min)"
    timeout -k 60 ${t}s "$@" >> $LOG/$name.log 2>&1; local rc=$?
    [ $rc = 0 ] && { say "OK $name"; return 0; }
    capped $rc && cap_stop "cap reached during $name"
    [ $rc = 3 ] && [ "${name#verify_}" != "$name" ] && { say "REGISTERED STOP $name: final, no retry"; return 0; }
    say "FAIL $name attempt $a rc=$rc"
  done
  stop "$name failed 3 times"
}

if [ "$1" = "--selftest" ]; then  # cap stop final, open records counted, then every module's CPU selftest
  set -o pipefail  # CC-121 W1: a failing module fails the selftest
  O=$(mktemp -d); LOG=$O; FAM=test; CAP=5; MIN_LEFT=1; BEFORE=0; T0=$(date +%s); touch $O/gpu_seconds.tsv
  ( step sleeper sleep 10 ) > /dev/null
  [ -e $O/CAP_STOP_test ] || { echo "a cap stop was not recorded"; rm -rf $O; exit 1; }
  echo "test 50" > $O/gpu_seconds.tsv; echo "pool 999" >> $O/gpu_seconds.tsv
  echo "x 100" > $O/gpu_open_test_100_1.rec; echo 400 > $O/gpu_open_test_100_1.hb
  [ "$(used)" = 350 ] || { echo "used() is not 50 + 300 for the test family ($(used))"; rm -rf $O; exit 1; }
  : > $O/gpu_open_test_100_1.hb; ! used > /dev/null || { echo "an empty heartbeat was not refused"; rm -rf $O; exit 1; }
  FAM=cpu; BLOCK=feats; ( cap_stop "x" ) > /dev/null
  [ ! -e $O/CAP_STOP_cpu ] && [ -e $O/CPU_TIMEOUT ] || { echo "a CPU timeout wrote a cap stop"; rm -rf $O; exit 1; }
  rm -rf $O; echo "cap stop final per GPU family, none for CPU, open records counted, empty heartbeat refused ok"
  for b in pool feats build smoke coco nocaps; do grep -q "SHA256SUMS_\$BLOCK\|SHA256SUMS_$b" "$0" \
    || { echo "no SHA256SUMS for block $b"; exit 1; }; done
  grep -q 'mirror SHA256SUMS_\$1' "$(dirname "$0")/cen_chain.sh" || { echo "the chain mirrors another sums name"; exit 1; }
  bash -n "$0" && bash -n "$(dirname "$0")/cen_chain.sh" || exit 1
  for f in cen_fetch cen_pool cen_memory cen_decode; do ${PY:-python3} scripts/c_en/$f.py --selftest | tail -1 || exit 1; done
  CEN_REQUIRE_PTB=1 ${SCPY:-python3} scripts/c_en/cen_score.py --selftest 2>&1 | grep -v PTBTokenizer | tail -1 || exit 1
  sha256sum --quiet -c scripts/c_en/SHA256SUMS && echo "job selftest ok"
  exit $?
fi

EXPECT=$1; BLOCK=$2
cd /root/vsps || exit 1
case $BLOCK in pool|feats|build|smoke|coco|nocaps) ;; *) stop "block must be pool, feats, build, smoke, coco or nocaps" ;; esac
[ -f /root/.vsps_machine_id ] && [ "$(tr -d '[:space:]' < /root/.vsps_machine_id | tr '[:upper:]' '[:lower:]')" = m3 ] \
  || stop "/root/.vsps_machine_id is not m3"
[ -n "$EXPECT" ] && [ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git cat-file -e HEAD:manuscript/prereg/2026-10-27_c_en/PREREG.md 2>/dev/null || stop "the C-EN prereg is not in HEAD"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
for s in scripts/c_en/SHA256SUMS manuscript/prereg/2026-10-27_c_en/SHA256SUMS; do sha256sum --quiet -c $s || stop "$s"; done
grep -q 'manuscript/prereg/2026-10-27_c_en/PREREG.md' manuscript/prereg/2026-10-27_c_en/SHA256SUMS \
  || stop "the C-EN prereg is not committed; no M3 step runs before it"
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=m3 VSPS_JOB_SHA256=$(sha256sum "$0" | cut -c1-64)
LB=/root/venv-lb/bin/python; SC=/root/vsps/.venv/bin/python; FT=/root/venv-cenfeat/bin/python
FREEZE_LB=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784
FREEZE_SC=7332d343173e5681365cf6871671e36209c77803a1b2db70da1cc766d5c943ed
FREEZE_FT=1a639a50adf550c50c6dfe284146e279b2a2bf2a716ade743e9eb357ccbf0778  # = cenfeat_venv_freeze.txt (CC-121 W8)
[ "$(sha256sum manuscript/prereg/2026-10-27_c_en/cenfeat_venv_freeze.txt | cut -c1-64)" = $FREEZE_FT ] \
  || stop "the committed venv-cenfeat freeze is not $FREEZE_FT"
D=scripts/c_en; O=/root/outputs/c_en; LOG=$O/logs; DS=/root/ncs-data/datasets; ST=$DS/cen_store
HUB=/root/.cache/huggingface/hub
Q25=$HUB/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/cc594898137f460bfe9f0759e9844b3ce807cfb5
IV3=$HUB/models--OpenGVLab--InternVL3-8B-hf/snapshots/259a3b64a14623c0ec91a045cb43f7c5af5fa6af
Q3VL=/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd
SIG=$HUB/models--google--siglip2-so400m-patch14-384/snapshots/e8e487298228002f3d8a82e0cd5c8ea9c567f57f
SIGREV=e8e487298228002f3d8a82e0cd5c8ea9c567f57f; EMB1=/root/outputs/c_stage1/emb.npz
SSCD=/root/ncs-data/models/sscd_disc_mixup.torchscript.pt
H="--expect-head $EXPECT"
NEED="$LB $FREEZE_LB"  # only the venvs this block uses
case $BLOCK in feats|build) NEED="$NEED $FT $FREEZE_FT" ;; coco|nocaps) NEED="$NEED $SC $FREEZE_SC" ;; esac
set -- $NEED
while [ $# -gt 0 ]; do [ "$(${1%/python}/pip freeze | sha256sum | cut -c1-64)" = $2 ] || stop "$1: venv freeze differs"
  shift 2; done
case $BLOCK in coco|nocaps) java -version 2>&1 | grep -q '11.0.32.1' || stop "Java is not openjdk 11.0.32.1" ;; esac
FAM=$(fam $BLOCK); CAP=$(cap_of $FAM); T0=$(date +%s)
mkdir -p $O/runs $O/guard $LOG; touch $O/gpu_seconds.tsv
[ ! -e $O/CAP_STOP_$FAM ] || stop "a $FAM cap stop is recorded; it is final"
BEFORE=$(used) || stop "unreadable GPU-h record; to the judge"
if [ $FAM = cpu ]; then  # CC-121 W5: cumulative CPU wall logged; a second timeout or over 24 h goes to the judge
  N_TO=$(cat $O/CPU_TIMEOUT 2>/dev/null | wc -l)
  { [ "$N_TO" -ge 2 ] || [ "$BEFORE" -ge $CAP ]; } && [ -z "${CEN_JUDGE_LINE:-}" ] \
    && stop "CPU: $N_TO timeout(s), $(( BEFORE / 36 ))e-2 h used; re-run only with a judge line (CEN_JUDGE_LINE)"
  [ -n "${CEN_JUDGE_LINE:-}" ] && { echo "$(ts) $BLOCK judge line $CEN_JUDGE_LINE" >> $O/CPU_TIMEOUT; CAP=$((BEFORE + 24 * 3600)); }
  trap 'echo "cpu $(( $(date +%s) - T0 ))" >> $O/gpu_seconds.tsv' EXIT
fi
if [ $FAM != cpu ]; then
  [ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ] || stop "another GPU process is running"
  OPEN=$O/gpu_open_${FAM}_${T0}_$$.rec; HBF=${OPEN%.rec}.hb
  echo "$BLOCK $T0" > $OPEN.tmp && mv -f $OPEN.tmp $OPEN; date +%s > $HBF.tmp && mv -f $HBF.tmp $HBF
  ( while kill -0 $$ 2>/dev/null; do date +%s > $HBF.tmp && mv -f $HBF.tmp $HBF; sleep 30; done ) & HB=$!
  trap 'kill $HB 2>/dev/null; echo "$FAM $(( $(date +%s) - T0 ))" >> $O/gpu_seconds.tsv; rm -f $OPEN $HBF' EXIT
fi
others() {  # no other C-EN test-side folder while a block runs; no C (Vietnamese) test folder
  for f in "$@"; do [ ! -e $DS/$f ] || stop "$DS/$f is present in the $BLOCK block"; done
  [ -z "$(ls -d $DS/c_ov_test $DS/c_xm_test2500 2>/dev/null)" ] || stop "a C test folder is present"
}
for f in cen_fetch cen_pool cen_memory cen_decode; do $LB $D/$f.py --selftest >> $LOG/selftest.log 2>&1 || stop "$f selftest"; done
case $BLOCK in coco|nocaps) $SC $D/cen_score.py --selftest >> $LOG/selftest.log 2>&1 || stop "cen_score selftest" ;; esac
sha256sum $D/* > $O/code_at_start_$BLOCK.sha256
say "JOB START $BLOCK head $EXPECT ($FAM used before: $(( BEFORE / 36 ))e-2 h of $(( CAP / 36 ))e-2)"
MEM=$O/cen_memory.json; MEMV=$O/cen_memory_emb.npz; CAPS=$ST/cen_memory_captions.json
runs() { $LB $D/cen_decode.py runs "$@"; }
preds() { for r in "$@"; do echo $O/runs/$r.preds.json; done; }
dec() {  # dec SET SNAPSHOT MODEL IMAGES: the set's runs of one backbone still missing, in one process
  local s=$1 snap=$2 m=$3 img=$4 todo=""
  for r in $(runs --set $s --model $m ${ARMSEL:-}); do [ -e $O/runs/$r.preds.json ] || todo="$todo $r"; done
  [ -z "$todo" ] && return 0
  export VSPS_VENV_FREEZE_SHA256=$FREEZE_LB
  step dec_${m}_$s $LB $D/cen_decode.py decode --run-ids $todo --snapshot $snap --memory $MEM --captions $CAPS \
    --exemplars $O/ex_$s.json --images $img --out-dir $O/runs $H
}
guard() {  # guard SET IMAGES: InternVL3's neighbour-only items and the Qwen3-VL verifier pass
  local s=$1 img=$2
  [ -e $O/guard/${s}_items.jsonl ] || step items_$s $LB $D/cen_decode.py items --set $s --runs $(preds $(runs \
    --set $s --model internvl3_8b --arm ret rand)) --zs $(preds $(runs --set $s --model internvl3_8b --arm zs)) \
    --memory $MEM --captions $CAPS --out $O/guard/${s}_items.jsonl
  step verify_$s $LB $D/cen_decode.py verify --set $s --items $O/guard/${s}_items.jsonl --images $img \
    --snapshot $Q3VL --memory $MEM --out $O/guard/${s}_cache.jsonl $H
}
testblock() {  # testblock SET DECIDE_ARGS: one look
  local s=$1 img=$DS/cen_$1/images; shift
  [ -d $img ] && [ -e $DS/cen_$s/refs.json ] || stop "cen_$s is not staged with its reference subset"
  [ ! -e $O/decide_$s.json ] || stop "the $s decide has run; no block is re-run after a decide"
  [ -e $O/emb_$s.npz ] || step embed_$s $LB $D/cen_pool.py embed --set $s --images $img --snapshot $SIG \
    --revision $SIGREV --emb1 $EMB1 --out $O/emb_$s.npz $H
  [ -e $O/ex_$s.json ] || step exemplars_$s $LB $D/cen_memory.py exemplars --set $s --memory $MEM --memory-emb $MEMV \
    --query-emb $O/emb_$s.npz --out $O/ex_$s.json $H
  dec $s $Q25 qwen25vl_7b $img; dec $s $IV3 internvl3_8b $img
  guard $s $img
  step score_$s $SC $D/cen_score.py score --set $s --runs $(preds $(runs --set $s)) --cache $O/guard/${s}_cache.jsonl \
    --memory $MEM --captions $CAPS --refs $DS/cen_$s/refs.json --ledger-dir $O $H
  timeout -k 60 $(left)s $SC $D/cen_score.py decide --set $s --ledger-dir $O --out $O/decide_$s.json "$@" $H \
    >> $LOG/decide.log 2>&1 || stop "decide $s failed (no retry)"
  (cd $O && sha256sum runs/cen_*_$s-*.preds.json guard/${s}_* emb_$s.npz ex_$s.json ledger_${s}_*.jsonl \
    decide_$s.json > SHA256SUMS_$BLOCK)
}

case $BLOCK in
  pool) others cen_coco_test cen_nocaps_val cen_coco_kval
        [ -e $O/emb_memory.npz ] || step embed_memory $LB $D/cen_pool.py embed --set memory --images $DS/cen_memory/images \
          --snapshot $SIG --revision $SIGREV --emb1 $EMB1 --out $O/emb_memory.npz --cap-s $(left) $H
        (cd $O && sha256sum emb_memory.npz > SHA256SUMS_pool) ;;
  feats) [ -e $O/feats_memory.npz ] || step feats_memory $FT $D/cen_pool.py feats --set memory \
           --images $DS/cen_memory/images --sscd $SSCD --out $O/feats_memory.npz $H
         for s in coco_kval coco_test nocaps_val; do
           [ -e $O/feats_$s.npz ] && continue
           others $(for x in coco_kval coco_test nocaps_val; do [ $x = $s ] || echo cen_$x; done)
           step stage_$s $LB $D/cen_fetch.py fetch --set $s --stage $H
           step feats_$s $FT $D/cen_pool.py feats --set $s --images $DS/cen_$s/images --sscd $SSCD --out $O/feats_$s.npz $H
           rm -rf $DS/cen_$s && [ ! -e $DS/cen_$s ] || stop "cen_$s not deleted"
           echo "$(ts) deleted $DS/cen_$s after its features" >> $O/deletions.log
         done
         (cd $O && sha256sum feats_*.npz deletions.log > SHA256SUMS_feats) ;;
  build) others cen_coco_test cen_nocaps_val cen_coco_kval
         [ -e $MEM ] || step build $FT $D/cen_memory.py build --emb $O/emb_memory.npz --feats $O/feats_memory.npz \
           $(for s in coco_test nocaps_val coco_kval; do echo --protect $s=$O/feats_$s.npz; done) --out-dir $O $H
         (cd $O && sha256sum cen_memory.json cen_memory_emb.npz > SHA256SUMS_build) ;;
  smoke) others cen_coco_test cen_nocaps_val cen_coco_kval
         [ -e $CAPS ] || stop "the memory caption store is not staged"
         [ -e $O/ex_smoke.json ] || step exemplars_smoke $LB $D/cen_memory.py exemplars --set smoke --memory $MEM \
           --memory-emb $MEMV --out $O/ex_smoke.json $H
         dec smoke $Q25 qwen25vl_7b $DS/cen_memory/images; dec smoke $IV3 internvl3_8b $DS/cen_memory/images
         guard smoke $DS/cen_memory/images
         $LB -c "import json,sys; r=[json.load(open(p)) for p in sys.argv[2:]]; c=sys.argv[1].replace('_items', '_cache')
d={'runs': len(r), 'captions': sum(len(x['predictions']) for x in r),
   'empty': sum(not v.strip() for x in r for v in x['predictions'].values()),
   'hit_max': sum(sum(x['hit_max'].values()) for x in r), 'items': sum(1 for _ in open(sys.argv[1])),
   'verifier_rows': sum(1 for _ in open(c)) if __import__('os').path.exists(c) else 0}
d['passed'] = d['runs'] == 6 and d['captions'] == 96 and d['empty'] == 0 and d['verifier_rows'] == d['items']
print(json.dumps(d))" $O/guard/smoke_items.jsonl $(preds $(runs --set smoke)) > $O/smoke_record.json || stop "smoke record"
         grep -q '"passed": true' $O/smoke_record.json || stop "smoke failed its pass rule (PREREG §9.6); to the judge"
         rm -f $O/runs/cen_*_smoke-* $O/guard/smoke_* $O/ex_smoke.json*
         (cd $O && sha256sum smoke_record.json > SHA256SUMS_smoke) ;;
  coco) others cen_nocaps_val cen_coco_kval cen_memory
        grep -q '"passed": true' $O/smoke_record.json 2>/dev/null || stop "smoke first (a passing smoke_record, CC-121 W7)"
        testblock coco_test ;;
  nocaps) others cen_coco_test cen_coco_kval cen_memory
          [ -e $O/decide_coco_test.json ] || stop "NoCaps before the COCO decide"
          testblock nocaps_val --coco-decide $O/decide_coco_test.json ;;
esac
say "BLOCK DONE $BLOCK $FAM wall $(( ($(date +%s) - T0) / 36 ))e-2 h, $FAM total $(( (BEFORE + $(date +%s) - T0) / 36 ))e-2 h"
