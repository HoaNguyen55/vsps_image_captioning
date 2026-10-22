#!/bin/bash
# M3: Paper C stage 2 (STAGE 2 / DEV-B, ONE LOOK), manuscript/prereg/2026-10-22_c_stage2/PREREG.md §9.3 order.
# Blocks, one call each, in this order:
#   ov     embed -> exemplars -> Qwen2.5 runs -> InternVL3 runs -> verifiers -> score -> §7.2 verdict
#   xm     the same on XM-dev500, only after E's stage-2 prereg is committed or E stopped (X2, F3); CIDEr-D on M3,
#          verified precision later, locally (§6.3)
#   blind  the image-blind arm (C-c) on the sets whose block ran, then score; first item dropped if the cap binds
# Hard cap min(10, 20 - 6.84) = 10 GPU-h over all blocks (§9.2), counted as job wall time; every step runs under
# `timeout` with the time left. A failed step is retried from its resume point up to 3 attempts, then JOB STOP.
# Usage: c_stage2_job.sh <expected 40-hex HEAD> ov|xm|blind [<E stage-2 prereg commit, or the ruling of E's stop>]
EXPECT=$1; BLOCK=$2; XM_OK=$3
cd /root/vsps || exit 1
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=$(hostname)
export VSPS_JOB_SHA256=$(sha256sum "$0" | cut -c1-64)
unset NCS_DATASET
LB=/root/venv-lb/bin/python; S2PY=/root/vsps/.venv/bin/python; SC=/root/venv-c1score/bin/python
D=scripts/c_stage2; O=/root/outputs/c_stage2; R=$O/runs; GD=$O/guard; LOG=$O/logs; LED=$O/ledger.jsonl
L=manuscript/prereg/2026-10-22_c_stage1/lists.json; EMB1=/root/outputs/c_stage1/emb.npz; KIT=scripts/kit_b
SUMS=manuscript/prereg/2026-10-22_c_stage2/SHA256SUMS
HUB=/root/.cache/huggingface/hub
Q25=$HUB/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/cc594898137f460bfe9f0759e9844b3ce807cfb5
IV3=$HUB/models--OpenGVLab--InternVL3-8B-hf/snapshots/259a3b64a14623c0ec91a045cb43f7c5af5fa6af
Q3VL=/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd
SIG=$HUB/models--google--siglip2-so400m-patch14-384/snapshots/e8e487298228002f3d8a82e0cd5c8ea9c567f57f
SIGREV=e8e487298228002f3d8a82e0cd5c8ea9c567f57f
SCORE_FREEZE=4b81b6b6a549771115529e6900b9589835cdbfff0c6acf179aef53d283b744d5  # §6.2
CAP=$((10 * 3600)); USED=$O/gpu_seconds.tsv; T0=$(date +%s)
mkdir -p $R $GD $LOG; touch $USED
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*"; }
stop() { say "JOB STOP $*"; exit 1; }
used() { awk '{s += $2} END {print s + 0}' $USED; }
BEFORE=$(used)
left() { echo $((CAP - BEFORE - ($(date +%s) - T0))); }
trap 'echo "$BLOCK $(( $(date +%s) - T0 ))" >> $USED' EXIT
freeze() { export VSPS_VENV_FREEZE_SHA256=$(${1%/python}/pip freeze | sha256sum | cut -c1-64); }

step() {  # step NAME CMD...: up to 3 attempts under the time left; 124 = cap reached
  local name=$1; shift
  for a in 1 2 3; do
    local t; t=$(left); [ "$t" -gt 60 ] || stop "10 GPU-h cap before $name"
    say "START $name attempt $a (left $((t / 60)) min)"
    timeout ${t}s "$@" >> $LOG/$name.log 2>&1; local rc=$?
    [ $rc = 0 ] && { say "OK $name"; return 0; }
    [ $rc = 124 ] && stop "10 GPU-h cap reached during $name"
    say "FAIL $name attempt $a rc=$rc"
  done
  stop "$name failed 3 times"
}
decode_left() { for r in "$@"; do [ -e $R/$r.preds.json ] || echo $r; done; }
_dec() {  # _dec SNAPSHOT EXEMPLARS RUN...: re-reads what is left on every attempt
  local snap=$1 ex=$2; shift 2; local todo; todo=$(decode_left "$@"); [ -z "$todo" ] && return 0
  $LB $D/decode2.py decode --run-ids $todo --snapshot $snap --lists $L --exemplars $ex --out-dir $R; }
export -f decode_left _dec; export LB D R L
decode() { local snap=$1 ex=$2 name=$3; shift 3; freeze $LB; step $name bash -c '_dec "$@"' _ $snap $ex "$@"; }
runs() { for x in "$@"; do echo $R/$x.preds.json; done; }
ids() { $LB $D/stage2.py runs "$@"; }  # run ids of the frozen grid

# ---------------------------------------------------------------- preflight (§1.2)
case $BLOCK in ov|xm|blind) ;; *) stop "block must be ov, xm or blind" ;; esac
[ -n "$EXPECT" ] && [ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
sha256sum --quiet -c $SUMS || stop "$SUMS does not verify"
[ "$(sha256sum $EMB1 | cut -c1-64)" = 59e65f6f6432af97504c59c72fa07b644acbff26938e1365473fad659421f7c0 ] \
  || stop "stage-1 embeddings differ"
if [ $BLOCK = xm ]; then
  [ -n "$XM_OK" ] || stop "XM block: name E's stage-2 prereg commit or the ruling of E's stop (X2)"
  [ -e $O/decide_ov.json ] || stop "XM block before the OV-dev-B block"
  say "XM block allowed by: $XM_OK"
fi
for f in stage2 decode2 guard2; do $LB $D/$f.py --selftest >> $LOG/selftest.log 2>&1 || stop "$f selftest"; done
$S2PY $D/guard2.py --selftest >> $LOG/selftest.log 2>&1 || stop "guard2 selftest (S2 venv)"
$SC $D/score2.py --selftest --kit-b $KIT >> $LOG/selftest.log 2>&1 || stop "score2 selftest"
$SC $D/decide2.py --selftest >> $LOG/selftest.log 2>&1 || stop "decide2 selftest"
[ "$(/root/venv-c1score/bin/pip freeze | sha256sum | cut -c1-64)" = $SCORE_FREEZE ] || stop "scoring venv differs (§6.2)"
java -version 2>&1 | grep -q '11.0.32.1' || stop "Java is not openjdk 11.0.32.1 (§6.2)"
HB=$BLOCK; [ $BLOCK = blind ] && { HB=ov; [ -e $O/decide_xm_m3.json ] && HB=xm; }
$LB $D/stage2.py check-host --block $HB --lists $L > $O/host_$BLOCK.json 2>> $LOG/host.log || stop "host check (§1.2)"
sha256sum $D/*.py $D/*.sh $SUMS > $O/code_at_start_$BLOCK.sha256
say "JOB START $BLOCK head $EXPECT (GPU-h used before: $(( BEFORE / 36 ))e-2)"

guard_pass() {  # guard_pass SET GENERATOR: items of the arms §5.3 verifies (C-a), then the verifier (own process)
  local s=$1 gen=$2 tag=$1_$2; local arms; arms=$($LB $D/stage2.py verify-arms --model $gen)
  local zs; zs=$(ids --set $s --model $gen --arm zs)
  step ${tag}_items $LB $D/guard2.py items --set $s --generator $gen --runs $(runs $(ids --set $s --model $gen \
    --arm $arms)) --zs $R/$zs.preds.json --lists $L --out $GD/$tag.items.jsonl
  if [ $gen = qwen25vl_7b ]; then freeze $S2PY
    step ${tag}_verify $S2PY $D/guard2.py score --set $s --items $GD/$tag.items.jsonl --generator $gen --lists $L \
      --out $GD/$tag.cache.jsonl
  else freeze $LB
    step ${tag}_verify $LB $D/guard2.py score --set $s --items $GD/$tag.items.jsonl --generator $gen --lists $L \
      --snapshot $Q3VL --out $GD/$tag.cache.jsonl
  fi
}
score() {  # score SET NAME RUN...: every model's zs, both guard caches
  local s=$1 name=$2; shift 2
  local zq zi; zq=$(ids --set $s --model qwen25vl_7b --arm zs); zi=$(ids --set $s --model internvl3_8b --arm zs)
  step $name $SC $D/score2.py score --set $s --runs $(runs "$@") --zs $R/$zq.preds.json $R/$zi.preds.json \
    --cache $GD/${s}_qwen25vl_7b.cache.jsonl $GD/${s}_internvl3_8b.cache.jsonl --lists $L --exemplars $O/ex_$s.json \
    --kit-b $KIT --ledger $LED
}
block() {  # block SET: §9.3 step 1 (OV-dev-B) or step 4 (XM-dev500)
  local s=$1
  freeze $LB
  [ -e $O/emb_$s.npz ] || step embed_$s $LB $D/decode2.py embed --set $s --lists $L --emb1 $EMB1 --snapshot $SIG \
    --revision $SIGREV --out $O/emb_$s.npz
  [ -e $O/ex_$s.json ] || step exemplars_$s $LB $D/decode2.py exemplars --set $s --lists $L --emb1 $EMB1 \
    --emb $O/emb_$s.npz --out $O/ex_$s.json
  decode $Q25 $O/ex_$s.json dec_qwen_$s $(ids --set $s --model qwen25vl_7b)
  decode $IV3 $O/ex_$s.json dec_internvl_$s $(ids --set $s --model internvl3_8b)
  guard_pass $s qwen25vl_7b
  guard_pass $s internvl3_8b
  score $s score_$s $(ids --set $s --arm ret rand fix)
}
confirm() {  # confirm OUT: decide --phase confirm on the ledger (its sha256 is in the output, O4); sets V
  $SC $D/decide2.py confirm --ledger $LED --out $O/$1 >> $LOG/decide.log 2>&1 || stop "decide confirm failed"
  V=$($SC -c "import json,sys; print(json.load(open(sys.argv[1]))['ov_dev_b']['verdict'])" $O/$1) \
    || stop "no verdict in $O/$1"; }

case $BLOCK in
  ov) block ov_dev_b; confirm decide_ov.json; say "GATE-VERDICT $V" ;;
  xm) block xm_dev500; confirm decide_xm_m3.json; say "XM-SCORED (gate verdict unchanged: $V)" ;;
  blind)
    for s in ov_dev_b xm_dev500; do
      [ -e $O/ex_$s.json ] || continue
      decode $Q25 $O/ex_$s.json blind_qwen_$s $(ids --set $s --model qwen25vl_7b --arm blind)
      decode $IV3 $O/ex_$s.json blind_internvl_$s $(ids --set $s --model internvl3_8b --arm blind)
      score $s score_blind_$s $(ids --set $s --arm blind)
    done
    confirm decide_blind.json; say "BLIND-SCORED (gate verdict unchanged: $V)" ;;
esac
(cd $O && sha256sum runs/*.preds.json guard/*.jsonl emb_*.npz ex_*.json ledger.jsonl decide_*.json > SHA256SUMS)
say "BLOCK DONE $BLOCK gpu_h_wall $(( ($(date +%s) - T0) / 36 ))e-2 total $(( (BEFORE + $(date +%s) - T0) / 36 ))e-2"
