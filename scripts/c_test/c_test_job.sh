#!/bin/bash
# M3: Paper C test (TEST, ONE LOOK PER SET), manuscript/prereg/2026-10-25_c_test/PREREG.md §11-§13; CC-103 E4-E7,
# CC-103a. The local chain (c_test_chain.sh) stages, mirrors and deletes around each block (E6); this job runs one:
#   e4  decode parity of both frozen ret arms on the first 52 KTVIC dev299 images (c_e4_dev299/) against stage 1
#   ov  embed -> exemplars -> Qwen2.5 runs -> InternVL3 runs -> InternVL3 items + Qwen3-VL verifier -> score the
#       1,941 and the 2,001 -> decide once
#   xm  the same on XM-test2500 (scored 2,500 and 2,392) whatever the OV result (W9) -> decide once (XM-a);
#       verified precision (XM-b) is local only
# No Qwen verifier pass (OQ-2). The Qwen3-VL answer-position stop (rc 3) is registered and final for the set (W16):
# no retry, the block goes on, decide reports InternVL3's frozen arms as incomplete, and the XM block still runs.
# Hard cap 20 GPU-h over all blocks, E4 included (E7), counted as job wall time: an open record with a heartbeat
# survives a hard kill and is counted (CC-103b W4). Every step, preflight call and decide runs under `timeout -k 60`
# with the time left (W3). A cap stop is final: CAP_STOP is written and no block starts again (W8). A failed step is
# retried from its resume point up to 3 attempts, then JOB STOP; decide is not retried. Every output lies under
# /root/outputs/c_test (CC-103a). W10: this log carries counts, times and return codes only, never a score.
# Usage: c_test_job.sh <expected 40-hex HEAD> e4|ov|xm          c_test_job.sh --selftest   (CPU, repo root)
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*"; }
stop() { say "JOB STOP $*"; exit 1; }
cap_stop() { echo "$(ts) $BLOCK $*" >> $O/CAP_STOP; stop "$*"; }  # final for the set (W8)
no_cap_stop() { [ ! -e $O/CAP_STOP ]; }
used() {  # closed blocks, plus every record a hard kill left open, up to its last heartbeat (CC-103b W4)
  local s r t0 hb; s=$(awk '{s += $2} END {print s + 0}' $O/gpu_seconds.tsv)
  for r in $O/gpu_open_*.rec; do
    [ -e "$r" ] || continue
    t0=$(cut -d' ' -f2 "$r"); hb=$(cat "${r%.rec}.hb" 2>/dev/null || echo $t0)
    for x in "$t0" "$hb"; do case $x in ''|*[!0-9]*) return 1 ;; esac; done  # CC-103c W1: fail closed
    s=$((s + hb - t0))
  done
  echo $s
}
left() { echo $((CAP - BEFORE - ($(date +%s) - T0))); }
capped() { [ $1 = 124 ] || { [ $1 = 137 ] && [ "$(left)" -le "${MIN_LEFT:-60}" ]; }; }  # timeout, TERM then KILL
sums() {  # sums OUT FILE...: a block's SHA256SUMS without resume scratch (*.partial.jsonl), which the mirror skips
  local out=$1; shift
  printf '%s\n' "$@" | grep -v '\.partial\.jsonl$' | xargs -d '\n' sha256sum > $out
}
timed() {  # timed NAME LOGFILE CMD...: once, under the time left (E7, CC-103b W3); a timeout is a cap stop
  local name=$1 log=$2; shift 2
  local t; t=$(left); [ "$t" -gt "${MIN_LEFT:-60}" ] || cap_stop "20 GPU-h cap before $name"
  timeout -k 60 ${t}s "$@" >> $log 2>&1; local rc=$?
  capped $rc && cap_stop "20 GPU-h cap reached during $name"
  return $rc
}
step() {  # step NAME CMD...: up to 3 attempts under the time left; 124 = cap reached
  local name=$1; shift
  for a in 1 2 3; do
    local t; t=$(left); [ "$t" -gt "${MIN_LEFT:-60}" ] || cap_stop "20 GPU-h cap before $name"
    say "START $name attempt $a (left $((t / 60)) min)"
    timeout -k 60 ${t}s "$@" >> $LOG/$name.log 2>&1; local rc=$?
    [ $rc = 0 ] && { say "OK $name"; return 0; }
    capped $rc && cap_stop "20 GPU-h cap reached during $name"
    [ $rc = 3 ] && [ "${name#verify_}" != "$name" ] && { say "REGISTERED STOP $name (W16): final, no retry"; return 0; }
    say "FAIL $name attempt $a rc=$rc"
  done
  stop "$name failed 3 times"
}

if [ "$1" = "--selftest" ]; then  # the cap stop is final; the block refusals; then the CPU selftests
  O=$(mktemp -d); LOG=$O; BLOCK=st; CAP=5; MIN_LEFT=1; BEFORE=0; T0=$(date +%s); touch $O/gpu_seconds.tsv
  ( step sleeper sleep 10 ) > /dev/null
  [ -e $O/CAP_STOP ] && ! no_cap_stop || { echo "a cap stop was not recorded"; rm -rf $O; exit 1; }
  echo "cap stop (rc 124) written to CAP_STOP; the preflight refuses every later block ok"
  rm -f $O/CAP_STOP; echo "a 50" > $O/gpu_seconds.tsv; echo "x 100" > $O/gpu_open_100_1.rec; echo 400 > $O/gpu_open_100_1.hb
  [ "$(used)" = 350 ] || { echo "an open record was not counted ($(used))"; rm -rf $O; exit 1; }
  echo "a record left open by a hard kill counts up to its last heartbeat ok"
  : > $O/gpu_open_100_1.hb; ! used > /dev/null && [ ! -e $O/CAP_STOP ] \
    || { echo "an empty heartbeat was not refused"; rm -rf $O; exit 1; }
  echo "an empty heartbeat makes used() fail, with no CAP_STOP ok"
  T0=$(date +%s); S0=$T0; ( timed quick $O/q.log sleep 10 ) > /dev/null
  [ -e $O/CAP_STOP ] && [ $(( $(date +%s) - S0 )) -ge 2 ] || { echo "timed: no cap stop by timeout"; rm -rf $O; exit 1; }
  echo "a preflight or decide call under timeout stops at the cap ok"
  mkdir -p $O/b/e4 $O/m && echo 1 > $O/b/e4/e4_x.json && echo 2 > $O/b/e4/r.preds.json.partial.jsonl && echo 3 > $O/b/h.json
  (cd $O/b && sums SHA256SUMS_e4 e4/* h.json) && rsync -a --exclude='*.partial.jsonl' $O/b/ $O/m/ \
    && [ "$(wc -l < $O/m/SHA256SUMS_e4)" = 2 ] && (cd $O/m && sha256sum --quiet -c SHA256SUMS_e4) \
    || { echo "a block's SHA256SUMS does not verify on a mirror without partials"; rm -rf $O; exit 1; }
  echo "SHA256SUMS without partials verifies on an rsync mirror that skips them ok"
  rm -rf $O
  bash -n "$0" && ${PY:-python3} scripts/c_test/score_t.py --selftest && \
    sha256sum --quiet -c scripts/c_test/SHA256SUMS && echo "job selftest ok"
  exit $?
fi

EXPECT=$1; BLOCK=$2
cd /root/vsps || exit 1
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=$(hostname)
export VSPS_JOB_SHA256=$(sha256sum "$0" | cut -c1-64)
unset NCS_DATASET
LB=/root/venv-lb/bin/python; SC=/root/venv-c1score/bin/python
D=scripts/c_test; O=/root/outputs/c_test; R=$O/runs; GD=$O/guard; LOG=$O/logs; E4O=$O/e4
L=manuscript/prereg/2026-10-22_c_stage1/lists.json; EMB1=/root/outputs/c_stage1/emb.npz; S1=/root/outputs/c_stage1
KIT=scripts/kit_b
HUB=/root/.cache/huggingface/hub
Q25=$HUB/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/cc594898137f460bfe9f0759e9844b3ce807cfb5
IV3=$HUB/models--OpenGVLab--InternVL3-8B-hf/snapshots/259a3b64a14623c0ec91a045cb43f7c5af5fa6af
Q3VL=/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd
SIG=$HUB/models--google--siglip2-so400m-patch14-384/snapshots/e8e487298228002f3d8a82e0cd5c8ea9c567f57f
SIGREV=e8e487298228002f3d8a82e0cd5c8ea9c567f57f
SCORE_FREEZE=4b81b6b6a549771115529e6900b9589835cdbfff0c6acf179aef53d283b744d5  # PR2 §6.2
CAP=$((20 * 3600)); T0=$(date +%s)
mkdir -p $R $GD $LOG $E4O; touch $O/gpu_seconds.tsv
BEFORE=$(used) || stop "unreadable GPU-h record (W4); to the judge"
OPEN=$O/gpu_open_${T0}_$$.rec; HBF=${OPEN%.rec}.hb  # W4: open record and heartbeat, each written by tmp + mv
echo "$BLOCK $T0" > $OPEN.tmp && mv -f $OPEN.tmp $OPEN; date +%s > $HBF.tmp && mv -f $HBF.tmp $HBF
( while kill -0 $$ 2>/dev/null; do date +%s > $HBF.tmp && mv -f $HBF.tmp $HBF; sleep 30; done ) & HB=$!
trap 'kill $HB 2>/dev/null; echo "$BLOCK $(( $(date +%s) - T0 ))" >> $O/gpu_seconds.tsv; rm -f $OPEN ${OPEN%.rec}.hb' EXIT
freeze() { export VSPS_VENV_FREEZE_SHA256=$(${1%/python}/pip freeze | sha256sum | cut -c1-64); }
decode_left() { for r in "$@"; do [ -e $R/$r.preds.json ] || echo $r; done; }
_dec() {  # _dec SNAPSHOT EXEMPLARS RUN...: re-reads what is left on every attempt
  local snap=$1 ex=$2; shift 2; local todo; todo=$(decode_left "$@"); [ -z "$todo" ] && return 0
  $LB $D/ctest.py decode --run-ids $todo --snapshot $snap --lists $L --exemplars $ex --out-dir $R; }
export -f decode_left _dec; export LB D R L
decode() { local snap=$1 ex=$2 name=$3; shift 3; freeze $LB; step $name bash -c '_dec "$@"' _ $snap $ex "$@"; }
runs() { for x in "$@"; do echo $R/$x.preds.json; done; }
ids() { $LB $D/ctest.py runs "$@"; }

# ---------------------------------------------------------------- preflight (§1.2, §11)
case $BLOCK in e4|ov|xm) ;; *) stop "block must be e4, ov or xm" ;; esac
no_cap_stop || stop "a cap stop is recorded in $O/CAP_STOP; it is final (W8)"
[ -n "$EXPECT" ] && [ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
for s in scripts/c_test/SHA256SUMS manuscript/prereg/2026-10-25_c_test/SHA256SUMS \
         manuscript/prereg/2026-10-22_c_stage2/SHA256SUMS; do sha256sum --quiet -c $s || stop "$s does not verify"; done
[ "$(sha256sum $EMB1 | cut -c1-64)" = 59e65f6f6432af97504c59c72fa07b644acbff26938e1365473fad659421f7c0 ] \
  || stop "stage-1 embeddings differ"
[ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ] || stop "another GPU process is running"
[ -z "$(find /root/outputs /root/ncs-data \( -name 'decide_final*' -o -name 'verified*.jsonl' -o -name 'oiv7*' \) \
  2>/dev/null)" ] || stop "a local-only or OIV7 file is on M3"
case $BLOCK in
  e4) [ ! -e $E4O/e4_qwen25vl_7b.json ] || [ ! -e $E4O/e4_internvl3_8b.json ] || stop "E4 has run on this rental" ;;
  ov) for m in qwen25vl_7b internvl3_8b; do grep -q '"passed": true' $E4O/e4_$m.json 2>/dev/null \
        || stop "E4 has not passed for $m"; done
      [ -e $O/e4_deleted.json ] || stop "the dev299 deletion is not recorded (CC-103a X3)"
      [ ! -e $O/decide_ov.json ] || stop "the OV decide has run; no block is re-run after a decide" ;;
  xm) [ -e $O/decide_ov.json ] && [ -e $O/ov_deleted.json ] || stop "XM block before the OV block and its deletion"
      [ ! -e $O/decide_xm_m3.json ] || stop "the XM decide has run; no block is re-run after a decide" ;;
esac
SL=$LOG/selftest.log
timed ctest_selftest $SL $LB $D/ctest.py --selftest || stop "ctest selftest"
timed score_t_selftest $SL $SC $D/score_t.py --selftest || stop "score_t selftest"
for f in stage2 decode2 guard2; do timed ${f}_selftest $SL $LB scripts/c_stage2/$f.py --selftest || stop "$f selftest"; done
timed score2_selftest $SL $SC scripts/c_stage2/score2.py --selftest --kit-b $KIT || stop "score2 selftest"
timed decide2_selftest $SL $SC scripts/c_stage2/decide2.py --selftest || stop "decide2 selftest"
[ "$(/root/venv-c1score/bin/pip freeze | sha256sum | cut -c1-64)" = $SCORE_FREEZE ] || stop "scoring venv differs (§6.2)"
java -version 2>&1 | grep -q '11.0.32.1' || stop "Java is not openjdk 11.0.32.1 (§6.2)"
timed check_host $LOG/host.log $LB $D/ctest.py check-host --block $BLOCK --lists $L --out $O/host_$BLOCK.json \
  || stop "host check (§11.2)"
sha256sum $D/*.py $D/*.sh $D/SHA256SUMS > $O/code_at_start_$BLOCK.sha256
say "JOB START $BLOCK head $EXPECT (GPU-h used before: $(( BEFORE / 36 ))e-2)"

block() {  # block SET: embed, examples, the 8 decodes, InternVL3's verifier pass, the scored sets
  local s=$1 zq zi
  freeze $LB
  [ -e $O/emb_$s.npz ] || step embed_$s $LB $D/ctest.py embed --set $s --lists $L --emb1 $EMB1 --snapshot $SIG \
    --revision $SIGREV --out $O/emb_$s.npz
  [ -e $O/ex_$s.json ] || step exemplars_$s $LB $D/ctest.py exemplars --set $s --lists $L --emb1 $EMB1 \
    --emb $O/emb_$s.npz --out $O/ex_$s.json
  decode $Q25 $O/ex_$s.json dec_qwen_$s $(ids --set $s --model qwen25vl_7b)
  decode $IV3 $O/ex_$s.json dec_internvl_$s $(ids --set $s --model internvl3_8b)
  zq=$(ids --set $s --model qwen25vl_7b --arm zs); zi=$(ids --set $s --model internvl3_8b --arm zs)
  [ -e $GD/${s}_internvl3_8b.items.jsonl ] || step items_$s $LB $D/ctest.py items --set $s \
    --runs $(runs $(ids --set $s --model internvl3_8b --arm ret rand fix)) --zs $R/$zi.preds.json --lists $L \
    --out $GD/${s}_internvl3_8b.items.jsonl
  freeze $LB
  step verify_$s $LB $D/ctest.py verify --set $s --items $GD/${s}_internvl3_8b.items.jsonl --lists $L \
    --snapshot $Q3VL --out $GD/${s}_internvl3_8b.cache.jsonl
  step score_$s $SC $D/score_t.py score --set $s --runs $(runs $(ids --set $s --arm ret rand fix)) \
    --zs $R/$zq.preds.json $R/$zi.preds.json --cache $GD/${s}_internvl3_8b.cache.jsonl --lists $L \
    --exemplars $O/ex_$s.json --ledger-dir $O
}
decide() {  # decide PHASE OUT: once; the JSON holds the sha256 of every ledger it read (CC-086b O4)
  timed decide_$1 $LOG/decide.log $SC $D/score_t.py decide --phase $1 --ledger-dir $O --lists $L --out $O/$2 \
    || stop "decide $1 failed (no retry)"; }

case $BLOCK in
  e4) for m in qwen25vl_7b internvl3_8b; do
        snap=$Q25; [ $m = internvl3_8b ] && snap=$IV3; freeze $LB
        [ -e $E4O/e4_$m.json ] || step e4_$m $LB $D/ctest.py e4 --model $m --snapshot $snap --lists $L --stage1 $S1 --out-dir $E4O
      done
      (cd $O && sums SHA256SUMS_e4 e4/* host_e4.json) ;;
  ov) block ov_test; decide ov decide_ov.json
      (cd $O && sums SHA256SUMS_ov runs/ct_*_ov_test-*.preds.json guard/ov_test_* emb_ov_test.npz ex_ov_test.json \
         ledger_ov_test_*.jsonl decide_ov.json host_ov.json $(ls runs/t6_retry_ov_test.jsonl guard/t6_retry_ov_test.jsonl \
         t6_retry_ov_test.jsonl 2>/dev/null)) ;;
  xm) block xm_test2500; decide xm decide_xm_m3.json
      (cd $O && sums SHA256SUMS_xm runs/ct_*_xm_test2500-*.preds.json guard/xm_test2500_* emb_xm_test2500.npz \
         ex_xm_test2500.json ledger_xm_test*.jsonl decide_xm_m3.json host_xm.json $(ls runs/t6_retry_xm_test2500.jsonl \
         guard/t6_retry_xm_test2500.jsonl t6_retry_xm_test2500.jsonl 2>/dev/null)) ;;
esac
say "BLOCK DONE $BLOCK gpu_h_wall $(( ($(date +%s) - T0) / 36 ))e-2 total $(( (BEFORE + $(date +%s) - T0) / 36 ))e-2"
