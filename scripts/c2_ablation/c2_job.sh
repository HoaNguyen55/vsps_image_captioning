#!/bin/bash
# Paper C, C-2 (DEV-B MECHANISM, NON-CONFIRMATORY) on M3: replay of the four stage-2 rows (CPU, before any decode),
# then AB-M (ret at 10% / 30% memory) and AB-K (ret, rand at the new k) on OV-dev-B, InternVL3's verifier pass, the
# score and the registered decide once (AB-tau is CPU-only on the stage-2 ledger). PREREG
# manuscript/prereg/2026-10-28_c2_ablation/PREREG.md (CC-126 W12). OV-dev-B only: never OV-test or XM-test.
# Cap: no GPU step starts after 5 GPU-h; every GPU step runs under `timeout` up to 6 GPU-h in total; a timeout or
# the soft cap is a CAP STOP, final (CAP_STOP.json): the steps not run leave their ablation INCOMPLETE, then score
# and decide run on what exists. Any other failure is a JOB STOP back to the judge.
# Usage, inside tmux on M3, after the laptop chain staged the 925 OV-dev-B images, the 1,836-key annotation subset
# and the two memory-caption sources (as stage 2 and C test did):
#   bash scripts/c2_ablation/c2_job.sh <expected 40-hex HEAD>
EXPECT=${1:?usage: c2_job.sh <expected HEAD>}
cd /root/vsps || exit 1
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=$(tr -d '[:space:]' < /root/.vsps_machine_id)
export VSPS_JOB_SHA256=$(sha256sum "$0" | cut -c1-64)
unset NCS_DATASET
LB=/root/venv-lb/bin/python; SC=/root/venv-c1score/bin/python; PY=$LB
LB_FREEZE=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784   # setup_gpu.sh H_LB
SC_FREEZE=4b81b6b6a549771115529e6900b9589835cdbfff0c6acf179aef53d283b744d5   # setup_gpu.sh H_C1 (stage-2 §6.2)
X=scripts/c2_ablation/c2.py; O=/root/outputs/c2_ablation; LOG=$O/logs; USED=$O/gpu_seconds.tsv
MARK=$O/CAP_STOP.json; LOCK=$O/RUNNING; LED=$O/ledger.jsonl; CACHE=$O/ov_dev_b_internvl3_8b.cache.jsonl
S2O=/root/outputs/c_stage2; L=manuscript/prereg/2026-10-22_c_stage1/lists.json; EMB1=/root/outputs/c_stage1/emb.npz
KIT=scripts/kit_b; HUB=/root/.cache/huggingface/hub
Q25=$HUB/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/cc594898137f460bfe9f0759e9844b3ce807cfb5
IV3=$HUB/models--OpenGVLab--InternVL3-8B-hf/snapshots/259a3b64a14623c0ec91a045cb43f7c5af5fa6af
Q3VL=/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd
mkdir -p $O $LOG
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*" | tee -a $LOG/job.log; }
stop() { say "JOB STOP $*"; exit 1; }
$PY $X lock --path $LOCK || exit 1   # tmux only, no cen* session, no other /root/outputs/*/RUNNING; O_EXCL
trap 'rm -f $LOCK' EXIT

# ---------------------------------------------------------------- preflight (PREREG §1.2)
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
for s in manuscript/prereg/2026-10-22_c_stage2/SHA256SUMS scripts/c2_ablation/SHA256SUMS; do
  sha256sum --quiet -c $s || stop "$s does not verify"; done
(cd $S2O && sha256sum --quiet -c SHA256SUMS) || stop "outputs/c_stage2 SHA256SUMS (stage-2 runs, ledger, guard)"
[ "$(sha256sum $EMB1 | cut -c1-64)" = 59e65f6f6432af97504c59c72fa07b644acbff26938e1365473fad659421f7c0 ] \
  || stop "stage-1 embeddings differ"
[ "$(/root/venv-lb/bin/pip freeze | sha256sum | cut -c1-64)" = $LB_FREEZE ] || stop "venv-lb freeze differs"
[ "$(/root/venv-c1score/bin/pip freeze | sha256sum | cut -c1-64)" = $SC_FREEZE ] || stop "scoring venv differs"
java -version 2>&1 | grep -q '11.0.32.1' || stop "Java is not openjdk 11.0.32.1"
export VSPS_VENV_FREEZE_SHA256=$LB_FREEZE
$LB $X --selftest >> $LOG/selftest.log 2>&1 || stop "c2 selftest (venv-lb)"
$SC $X --selftest >> $LOG/selftest.log 2>&1 || stop "c2 selftest (scoring venv)"
$SC scripts/c_stage2/score2.py --selftest --kit-b $KIT >> $LOG/selftest.log 2>&1 || stop "score2 selftest (kit B)"
$SC scripts/c_stage2/decide2.py --selftest >> $LOG/selftest.log 2>&1 || stop "decide2 selftest"
$LB $X check >> $LOG/check.log 2>&1 || stop "c2 check (prereg folder, subsets)"
G() { $LB $X guard --head "$EXPECT" >> $LOG/guard.log 2>&1 || stop "guard (host, GPU, C-EN, locks)"; }
G
$LB scripts/c_stage2/stage2.py check-host --block ov --lists $L > $O/host_ov.json 2>> $LOG/host.log \
  || stop "stage-2 host check (no test or XM image, 925/925 OV-dev-B, the 1,836-key subset)"
sha256sum $X scripts/c2_ablation/c2_job.sh scripts/c2_ablation/SHA256SUMS > $O/code_at_start.sha256
say "JOB START head $EXPECT"

cap_stop() {  # final: no GPU step after it
  [ -e $MARK ] || printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > $MARK
  say "CAP STOP $1"; finish; }
gpu() {  # gpu NAME CMD...: one GPU step; no start after 5 GPU-h, killed at 6; wall seconds -> gpu_seconds.tsv
  local name=$1; shift
  local t; t=$($PY $X left --used $USED --marker $MARK) || stop "cap arithmetic"
  [ "$t" -gt 0 ] || cap_stop "5 GPU-h soft cap before $name"
  G; say "START $name (timeout $((t / 60)) min)"
  local t0; t0=$(date +%s)
  echo "$name start $t0" >> $USED   # CC-128 W6: a reboot mid-step is charged from here (c2.py used_seconds)
  timeout ${t}s "$@" >> $LOG/$name.log 2>&1; local rc=$?
  echo "$name $(( $(date +%s) - t0 ))" >> $USED
  [ $rc = 0 ] && { say "OK $name"; return 0; }
  [ $rc = 124 ] && cap_stop "6 GPU-h hard cap reached during $name"
  [ $rc = 3 ] && { say "REGISTERED VERIFIER STOP in $name: InternVL3 rows of this ablation incomplete"; return 0; }
  stop "$name rc=$rc"
}
cpu() { local name=$1; shift; say "START $name"; "$@" >> $LOG/$name.log 2>&1 || stop "$name"; say "OK $name"; }
runs() { for r in "$@"; do [ -e $O/$r.preds.json ] && echo $O/$r.preds.json; done; }
todo() { for r in "$@"; do [ -e $O/$r.preds.json ] || echo $r; done; }
decode() {  # decode SNAPSHOT NAME [--parity] RUN...: the runs not yet decoded, one process
  local snap=$1 name=$2; shift 2; local par=; [ "$1" = --parity ] && { par=--parity; shift; }
  local left_; left_=$(todo "$@"); [ -z "$left_" ] && return 0
  gpu $name $LB $X decode --run-ids $left_ $par --snapshot $snap --lists $L --s2 $S2O --out-dir $O
}
guard_pass() {  # guard_pass NAME RUN...: InternVL3's items, then the Qwen3-VL verifier (cache seeded from stage 2)
  local name=$1; shift; local have; have=$(runs "$@"); [ -z "$have" ] && return 0
  [ -e $O/VERIFIER_STOP.json ] && return 0
  cpu items_$name $LB $X items --runs $have --s2 $S2O --lists $L --out $O/items_$name.jsonl
  gpu verify_$name $LB $X verify --items $O/items_$name.jsonl --s2 $S2O --lists $L --snapshot $Q3VL --out $CACHE
}
finish() {  # CPU: score the C-2 runs that exist, then decide once (AB-tau reads the archived tau rows here only)
  local all; all=$(runs $($PY $X runs))
  if [ -n "$all" ] && [ ! -e $LED ]; then
    [ -e $CACHE ] || cp $S2O/guard/ov_dev_b_internvl3_8b.cache.jsonl $CACHE
    cpu score $SC $X score --runs $all --s2 $S2O --cache $CACHE --lists $L --kit-b $KIT --ledger $LED
  fi
  [ -e $LED ] || : > $LED
  [ -e $O/decide.json ] || cpu decide $SC $X decide --l2 $S2O/ledger.jsonl --ledger $LED --s2 $S2O --out $O/decide.json
  (cd $O && find . -type f ! -name 'SHA256SUMS*' ! -name RUNNING ! -name '*.partial*' | sort | xargs sha256sum) \
    > $O/SHA256SUMS
  say "BLOCK DONE gpu_h $(awk '{s += $2} END {printf "%.2f", s / 3600}' $USED)"
  exit 0
}

# ---------------------------------------------------------------- 1. replay (CPU), before any decode
[ -e $O/replay.json ] || cpu replay $SC $X replay --l2 $S2O/ledger.jsonl --decide-ov $S2O/decide_ov.json \
  --out $O/replay.json
# ---------------------------------------------------------------- 2. AB-M: memory subsets (CPU), then ret decodes
for p in 10 30; do
  [ -e $O/ex_m$p.json ] || cpu exemplars_m$p $LB $X exemplars --pct $p --lists $L --emb1 $EMB1 \
    --emb $S2O/emb_ov_dev_b.npz --out $O/ex_m$p.json
done
decode $Q25 dec_qwen_M --parity $($PY $X runs --ablation M --model qwen25vl_7b)
decode $IV3 dec_internvl_M --parity $($PY $X runs --ablation M --model internvl3_8b)
guard_pass M $($PY $X runs --ablation M --model internvl3_8b)
# ---------------------------------------------------------------- 3. AB-K: ret and rand at the new k
decode $Q25 dec_qwen_K $($PY $X runs --ablation K --model qwen25vl_7b)
[ -e $O/VERIFIER_STOP.json ] && say "VERIFIER_STOP recorded: InternVL3 AB-K decodes skipped (CC-128 R1)" \
  || decode $IV3 dec_internvl_K $($PY $X runs --ablation K --model internvl3_8b)
guard_pass K $($PY $X runs --ablation K --model internvl3_8b)
finish
