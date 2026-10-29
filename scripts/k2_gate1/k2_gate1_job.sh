#!/bin/bash
# K2 Gate 1 dev gate (manuscript/prereg/2026-10-28_k2_gate1/RULE.md; CC-148 W3-W13). Teacher decode of the UT pool
# (venv-lb, Gate 0 path), detector pass (venv-gd), targets (CPU), student timing probe + caps, four QLoRA arms
# (venv-q3, w22_sft.load C1), five val-924 decodes on the one student path (W7), then gate1_decide.py (one look).
#   EXPECT_HEAD=<latest commit of RULE + W25 amendment + MT4 PREREG> GPU=m3 bash scripts/k2_gate1/k2_gate1_job.sh
#                                                                    (/root/vsps, inside tmux; M3 only, CC-151 r2)
#   bash scripts/k2_gate1/k2_gate1_job.sh --selftest                                     (CPU, repo root)
# A fault writes GATE1_FAULT_<utc>.md and exits 0; a logged rerun reuses every finished step whose sha file matches.
# Exit 124 of any step, or caps above the Gate 1 total, is NOT-RUN (cost) and closes the gate. An OOM (exit 5) and
# a step that would cross NOT_AFTER (left exit 4) are faults: TO-PI, never a C2 switch, never a cost stop.
set -euo pipefail
H_Q3=2bb7397e7db350a2c225df590cdd9531df6a3247f7a3f217e1b64ed2d9f1be80   # venv_q3_freeze.txt (W22 PREREG §8)
H_LB=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784   # setup_gpu.sh H_LB (Gate 0 teacher path)
H_GD=696f7dc31a3d6de537d772a3f53f8b0a7db8ac2bc77af08ded8e4eeaaee16ef5   # venv-gd = sha256 of scripts/k2_gate1/venv_gd_freeze.txt (amendment 2a; M3 5291fc30 not reproducible)
D=scripts/k2_gate1
PY=/root/vsps/.venv/bin/python; [ -x $PY ] || PY=python3   # M3 system python3 has no numpy (OPS-1028x-op)
if [ "${1:-}" = "--selftest" ]; then
  bash -n "$0"
  $PY $D/k2_gate1.py --selftest
  $PY $D/gate1_decide.py --selftest
  sha256sum --quiet -c $D/SHA256SUMS
  ! grep -qE '[|] *t[e]e' "$0" || { echo "a tee pipe masks exit codes (the N9 bug)"; exit 1; }
  [ "$(grep -cE '^ *step [^#]*partial[.]jsonl" --' "$0")" = 3 ] || { echo "a decode step lacks its fresh partial (F1)"; exit 1; }
  r=0; out=$(GPU=m4 EXPECT_HEAD=x bash "$0" 2>&1) || r=$?
  [ "$r" = 1 ] && [[ $out == *"M3 only"* ]] || { echo "GPU=m4 was not refused"; exit 1; }
  echo "k2_gate1_job selftest ok"
  exit 0
fi
[ "${GPU:-}" = m3 ] || { echo "REFUSED: K2 Gate 1 runs on M3 only (CC-151 r2); GPU=${GPU:-unset}"; exit 1; }
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
HEAD=${EXPECT_HEAD:?set EXPECT_HEAD to the latest commit holding the rule, the W25 amendment and the MT4 PREREG}
MACHINE=$GPU
VQ=/root/venv-q3/bin/python; LB=/root/venv-lb/bin/python; GD=/root/venv-gd/bin/python
X=$D/k2_gate1.py; DEC=$D/gate1_decide.py
SNAP=/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd
UV=$NCS_DATA/datasets/uitviic; VAL=manuscript/prereg/2026-10-21_dev_pools/uitviic_val.tsv
O=/root/outputs/k2_gate1; LOCK=$O/RUNNING; L=$O/gpu_seconds.tsv
G0DEC=/root/outputs/grl_pilot/k2/k2g0_qwen3vl_8b_val-detailed.preds.json   # bf16 diagnostic row (RULE §2, judge item)
[ ! -e "$O/gate1_decide.json" ] || { echo "STOP: K2 Gate 1 already decided (one look)"; exit 1; }
[ "$(tr -d '[:space:]' < /root/.vsps_machine_id)" = "$MACHINE" ] || { echo "REFUSED: this host is not $MACHINE"; exit 1; }
[ "$(git rev-parse HEAD)" = "$HEAD" ] || { echo "REFUSED: HEAD is not $HEAD"; exit 1; }
git diff --quiet HEAD -- || { echo "REFUSED: tracked files differ from HEAD"; exit 1; }
[ -n "${TMUX:-}" ] || { echo 'REFUSED: run inside a tmux session'; exit 1; }
[ "$(tmux ls 2>/dev/null | wc -l)" = 1 ] || { echo "REFUSED: another tmux session exists"; exit 1; }
[ ! -e /root/ncs-data/b2_stage ] || { echo "REFUSED: /root/ncs-data/b2_stage exists"; exit 1; }
for p in /root/ncs-data/datasets/pascal50s /root/ncs-data/p50_raw; do   # amendment 2 (RULE §5): no P50 test data
  [ ! -e "$p" ] || { echo "REFUSED: $p exists (PASCAL-50S staging; delete and log it first)"; exit 1; }
done
OTHER=$(ls /root/outputs/*/RUNNING 2>/dev/null || true)
[ -z "$OTHER" ] || { echo "REFUSED: a lock exists: $OTHER"; exit 1; }
mkdir -p "$O"; touch "$L"
( set -o noclobber; echo "$0 $(date -u +%FT%TZ)" > "$LOCK" ) || { echo "REFUSED: $LOCK exists"; exit 1; }
trap 'rm -f "$LOCK"' EXIT
echo "$(date -u +%FT%TZ) start head $HEAD on $MACHINE" >> "$O/runs.log"
fault() {
  $PY $DEC notrun --class fault --why "$1" --dir "$O"
  echo "$(date -u +%FT%TZ) FAULT: $1" >> "$O/runs.log"
  echo "K2 Gate 1 NOT RUN (fault) -> TO-PI: $1"
  exit 0
}
cost() {
  $PY $DEC notrun --class cost --why "$1" --dir "$O"
  echo "$(date -u +%FT%TZ) NOT-RUN (cost): $1" >> "$O/runs.log"
  echo "K2 Gate 1 NOT RUN (cost) -> TO-PI: $1"
  exit 0
}
# 1. CPU checks before any GPU step: selftests, the three freezes + pip check, snapshot pins, W25 HOLD, imports
bash $0 --selftest >> "$O/runs.log" 2>&1 || fault "selftest"
for v in "$VQ $H_Q3" "$LB $H_LB" "$GD $H_GD"; do
  set -- $v
  [ -x "$1" ] || fault "$1 is missing (venvs are built by their own pinned procedures, never here)"
  [ "$($1 -m pip freeze | sha256sum | cut -c1-64)" = "$2" ] || fault "$1 freeze differs from ${2:0:8}"
  $1 -m pip check >> "$O/runs.log" 2>&1 || fault "$1 pip check"
done
$PY scripts/w22_sft/w22_sft.py snapcheck --snapshot $SNAP >> "$O/runs.log" 2>&1 || fault "snapshot pins"
for f in manuscript/prereg/2026-10-28_k2_gate1/w25_excluded_ids.txt manuscript/prereg/2026-10-28_mt4_kv/PREREG.md; do
  git cat-file -e "HEAD:$f" 2>/dev/null || fault "HELD: $f is not committed at HEAD (CC-148 W9, CC-151 W2/W3)"
done
[ ! -e /dev/shm/w25 ] || fault "W25 tmpfs stage /dev/shm/w25 still exists (W25 RULE §5: deleted and logged first)"
G() { $PY $X guard "$HEAD" >> "$O/runs.log" 2>&1; }
G || fault "guard refused"
rc=0; $VQ scripts/w22_sft/w22_sft.py imports --snapshot $SNAP >> "$O/runs.log" 2>&1 || rc=$?
[ "$rc" = 0 ] || fault "venv-q3 import check exit $rc (3 = a module or symbol is missing)"
for v in "$VQ q3" "$GD gd"; do
  set -- $v
  rc=0; $1 $X imports --venv $2 >> "$O/runs.log" 2>&1 || rc=$?
  [ "$rc" = 0 ] || fault "k2_gate1 import check ($2) exit $rc"
done
if [ ! -s "$UV/images.sha256" ]; then
  $PY scripts/grl/common.py stage "$UV/src" >> "$O/runs.log" 2>&1 || fault "stage"
  rm -rf "$UV/src"
  G || fault "guard refused after staging"
fi
# amendment 2: a reused manifest (resume on a restaged host) must name exactly the staged images
for m in ut probe; do
  [ ! -s "$O/$m.tsv" ] || $PY $X stagecheck --manifest "$O/$m.tsv" >> "$O/runs.log" 2>&1 || fault "staged images differ from $m.tsv"
done
export VSPS_MACHINE_ID="$MACHINE" VSPS_JOB_SHA256="$(sha256sum "$0" | cut -c1-64)"
# 2. GPU steps: each under timeout = min(its cap, the 36 GPU-h Gate 1 total left); ledger lines before and after
step() {  # step NAME CAPS_ARG PARTIAL -- command...   (skipped when NAME.done matches its recorded output sha)
  local name=$1 caps=$2 part=$3 left t0 rc=0; shift 4
  if [ -s "$O/$name.done" ] && (cd "$O" && sha256sum -c --status "$name.done" 2>/dev/null); then
    echo "$(date -u +%FT%TZ) $name reused (sha matches), no GPU step" >> "$O/runs.log"; return 0
  fi
  rc=0; left=$($PY $X left --ledger "$L" --stage "$name" $caps) || rc=$?
  [ "$rc" = 4 ] && fault "HELD: $name would cross NOT_AFTER (k2_gate1.NOT_AFTER) minus cleanup (a rerun needs a ruling)"
  [ "$rc" = 6 ] && fault "ledger: an open start before $name (closed at its full logged timeout; rerunnable, CC-162 W8)"
  [ "$rc" = 0 ] || fault "left exit $rc before $name"
  [ "$left" -gt 0 ] || cost "Gate 1 total spent before $name"
  G || fault "guard refused before $name"
  if [ -n "$part" ]; then   # CC-162a F1: every attempt starts from zero (no resume across a kill or a lost host)
    $PY $X fresh --partial "$part" >> "$O/runs.log" 2>&1 || fault "fresh $name"
  fi
  t0=$(date +%s)   # the start line logs the timeout (charged in full if left open) and is fsynced before the step
  $PY $X ledger --ledger "$L" --line "$name start $t0 $left" || fault "ledger start $name"
  timeout "$left" "$@" >> "$O/$name.log" 2>&1 || rc=$?
  $PY $X ledger --ledger "$L" --line "$name $(( $(date +%s) - t0 ))" || fault "ledger end $name"   # measured seconds
  [ "$rc" = 124 ] && cost "exit 124 in $name ($left s: its cap or the Gate 1 total)"
  [ "$rc" = 5 ] && fault "OOM in $name: NOT-RUN (fault), TO-PI; no switch to C2 (CC-151 r13)"
  [ "$rc" = 0 ] || fault "$name exit $rc"
}
done_sha() { (cd "$O" && sha256sum "${@:2}" > "$1.done"); }
# 2a. teacher: Gate 0's LB decoder and registration (bf16, batch 4, detailed, 512) on the UT pool minus W25
[ -s "$O/ut.tsv" ] || $PY $X manifest --set ut --out "$O/ut.tsv" || fault "UT manifest (HELD or staging)"
[ -s "$O/probe.tsv" ] || $PY $X manifest --set probe --out "$O/probe.tsv" || fault "probe manifest"
[ -s "$O/reg_teacher.json" ] || $PY $X reg --manifest "$O/ut.tsv" --out "$O/reg_teacher.json" || fault "teacher registration"
$LB scripts/lb/decode_hf_vlm.py --prereg "$O/reg_teacher.json" --check-snapshot qwen3vl_8b --snapshot $SNAP >> "$O/runs.log" 2>&1 \
  || fault "teacher snapshot check"
TP=$O/k2g1_qwen3vl_8b_ut-detailed.preds.json
export VSPS_VENV_FREEZE_SHA256=$H_LB
step teacher "" "$TP.partial.jsonl" -- \
  $LB scripts/lb/decode_hf_vlm.py --prereg "$O/reg_teacher.json" --run-id k2g1_qwen3vl_8b_ut-detailed --snapshot $SNAP --out-dir "$O"
done_sha teacher "$(basename "$TP")"
# 2b. detector: k2_p2_detect's pinned GD-T model and 0.30 rule on the same pool
export GD_FREEZE_SHA256=$H_GD
step detect "" "" -- $GD $X detect --manifest "$O/ut.tsv" --out "$O/detect.json"
done_sha detect detect.json
# 2c. targets (CPU): unedited / gold-edited / detector-edited / references; counts only on stdout
[ -s "$O/targets.json" ] || $PY $X targets --teacher "$TP" --detect "$O/detect.json" --out "$O/targets.json" >> "$O/runs.log" 2>&1 \
  || fault "targets"
# 2d. timing probe: the base path (fresh zero LoRA) on the 40 W22 train ids, no val image; then the caps (> 36 = cost)
export VSPS_VENV_FREEZE_SHA256=$H_Q3
step timing "" "$O/k2g1_timing.preds.json.partial.jsonl" -- \
  $VQ $X decode --arm timing --manifest "$O/probe.tsv" --out-dir "$O" --snapshot $SNAP
done_sha timing k2g1_timing.preds.json
if [ ! -s "$O/caps.json" ]; then
  rc=0; $PY $X caps --timing "$O/k2g1_timing.preds.json" --targets "$O/targets.json" --out "$O/caps.json" >> "$O/runs.log" 2>&1 || rc=$?
  [ "$rc" = 2 ] && cost "caps.json: stage caps exceed the 36 GPU-h Gate 1 total"
  [ "$rc" = 0 ] || fault "caps exit $rc"
fi
# 2e. four arms, seed 0, 2 epochs, last checkpoint
for A in unedited gold det ref; do
  step "train_$A" "--caps $O/caps.json" "" -- \
    $VQ $X train --arm $A --targets "$O/targets.json" --out-dir "$O/adapters" --snapshot $SNAP
  done_sha "train_$A" "adapters/$A/adapter_model.safetensors" "adapters/$A/train.json"
done
# 2f. five val-924 decodes on the one student path (base_s = the same net with its fresh, zero LoRA)
for S in base_s unedited gold det ref; do
  AD=(); [ "$S" = base_s ] || AD=(--adapter "$O/adapters/$S")
  step "decode_$S" "--caps $O/caps.json" "$O/k2g1_$S.preds.json.partial.jsonl" -- \
    $VQ $X decode --arm $S "${AD[@]}" --manifest $VAL --out-dir "$O" --snapshot $SNAP
  done_sha "decode_$S" "k2g1_$S.preds.json"
done
# 3. one look (CPU); never at or after NOT_AFTER (MT4 PREREG amendment 1, §0 row 3)
$PY $X deadline >> "$O/runs.log" 2>&1 || fault "HELD: past NOT_AFTER, no decision may be written (Branch K1+K6 binds)"
BF=(); [ -s "$G0DEC" ] && BF=(--bf16 "$G0DEC")   # the diagnostic row exists on M3 only
rc=0; $PY $DEC decide --dir "$O" "${BF[@]}" >> "$O/runs.log" 2>&1 || rc=$?
[ "$rc" = 0 ] || [ "$rc" = 3 ] || fault "decide exit $rc"
(cd "$O" && sha256sum gate1_decide.json caps.json targets.json.counts.json k2g1_*.preds.json adapters/*/adapter_model.safetensors \
  > SHA256SUMS 2>/dev/null || true)
echo "$(date -u +%FT%TZ) decided rc $rc" >> "$O/runs.log"
