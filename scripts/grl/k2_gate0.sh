#!/bin/bash
# K2 Gate 0/0b dev pilot (K2_GATE0_RULE.md; CC-119 ruling 4): a 40-image UT-train probe freezes max_new_tokens and
# the cap, then Qwen3-VL-8B zero-shot detailed on UIT-ViIC val 924, then the CPU editor and scorer. A target ceiling
# only. M3 (PI-1026r(3)), idle GPU, after C-EN's test-side hash pass with no protected set staged and no C-EN process
# (CC-119 W6, CC-120, CC-121; C-EN has priority). One look: a STOP writes STOP.md and nothing is rerun.
#   EXPECT_HEAD=<commit of the rule> bash scripts/grl/k2_gate0.sh
set -euo pipefail
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1
HEAD=${EXPECT_HEAD:?set EXPECT_HEAD to the commit of the K2 Gate 0 rule}
PY=/root/vsps/.venv/bin/python
LB=/root/venv-lb/bin/python
LB_FREEZE=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784   # setup_gpu.sh H_LB
SNAP=/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd
DEC=scripts/lb/decode_hf_vlm.py
UV=$NCS_DATA/datasets/uitviic
O=/root/outputs/grl_pilot/k2
[ ! -e "$O/gate0_decide.json" ] && [ ! -e "$O/STOP.md" ] || { echo "STOP: K2 Gate 0 already decided (one look)"; exit 1; }
# CC-124 W1: inside tmux only. cen_chain.sh refuses to start a C-EN step while any tmux session exists (C-EN PREREG
# l.129), so a pilot in tmux blocks C-EN at code level; m3_clear + the RUNNING lock block the pilot while C-EN runs.
[ -n "${TMUX:-}" ] || { echo 'REFUSED: run inside a tmux session (C-EN PREREG l.129 / cen_chain.sh:42 refuse while one exists)'; exit 1; }
LOCK=/root/outputs/grl_pilot/RUNNING   # common.LOCK (rule §3): refused if it exists; the operator starts no C-EN step while it exists
mkdir -p /root/outputs/grl_pilot
[ ! -e "$LOCK" ] || { echo "REFUSED: $LOCK exists"; exit 1; }
echo "$0 $(date -u +%FT%TZ)" > "$LOCK"; trap 'rm -f "$LOCK"' EXIT
[ "$($LB -m pip freeze | sha256sum | cut -c1-64)" = "$LB_FREEZE" ] || { echo "REFUSED: venv-lb freeze differs"; exit 1; }
export VSPS_MACHINE_ID="$(tr -d '[:space:]' < /root/.vsps_machine_id)" VSPS_JOB_SHA256="$(sha256sum "$0" | cut -c1-64)" \
       VSPS_VENV_FREEZE_SHA256="$LB_FREEZE"
for s in common reward k2_gate0; do $PY scripts/grl/$s.py --selftest; done
$LB $DEC --selftest
G() { $PY scripts/grl/common.py guard "$HEAD"; }
G
if [ ! -s "$UV/images.sha256" ]; then $PY scripts/grl/common.py stage "$UV/src" && rm -rf "$UV/src"; fi
G
mkdir -p "$O"
mem() { nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -lms 1000 >> "$1" & echo $!; }
stamp() { while IFS= read -r l; do echo "$(date +%s.%N) $l"; done; }
# 1. probe: 40 UT-train images at 1024 new tokens (no val image before the freeze)
$PY scripts/grl/k2_gate0.py manifest --out "$O/probe.tsv"
$PY scripts/grl/k2_gate0.py reg --dataset probe --n-new 1024 --manifest "$O/probe.tsv" --out "$O/reg_probe.json"
$LB $DEC --prereg "$O/reg_probe.json" --check-snapshot qwen3vl_8b --snapshot "$SNAP"
G
MP=$(mem "$O/mem.log")
$LB $DEC --prereg "$O/reg_probe.json" --run-id k2g0_qwen3vl_8b_probe-detailed --snapshot "$SNAP" --out-dir "$O" 2>&1 \
  | stamp | tee "$O/probe.log"
kill "$MP"
$PY scripts/grl/k2_gate0.py freeze --probe "$O/k2g0_qwen3vl_8b_probe-detailed.preds.json" --probe-log "$O/probe.log" \
  --out "$O/freeze.json"
read -r V N CAP < <($PY -c "import json; d=json.load(open('$O/freeze.json')); print(d['verdict'], d.get('max_new_tokens', 0), d.get('cap_gpuh', 0))")
[ "$V" = GO ] || { echo "K2 Gate 0 NOT RUN (cost) at the freeze -> TO-PI (STOP.md); not a negative pilot"; exit 0; }
# 2. Gate 0: val 924 at the frozen max_new_tokens, under the cap (a cap hit is a STOP)
$PY scripts/grl/k2_gate0.py reg --dataset val --n-new "$N" --manifest manuscript/prereg/2026-10-21_dev_pools/uitviic_val.tsv \
  --out "$O/reg_val.json"
G
MV=$(mem "$O/mem.log")
rc=0
timeout "$($PY -c "print(int($CAP * 3600))")" $LB $DEC --prereg "$O/reg_val.json" --run-id k2g0_qwen3vl_8b_val-detailed \
  --snapshot "$SNAP" --out-dir "$O" 2>&1 | stamp | tee "$O/val.log" || rc=$?
kill "$MV"
if [ "$rc" != 0 ]; then  # CC-124 W2 / CC-125 X3: 124 = NOT RUN (cost), any other = NOT RUN (fault); both TO-PI, no rerun
  CLS=fault; [ "$rc" = 124 ] && CLS=cost
  printf '# K2 Gate 0/0b NOT RUN (%s) -> TO-PI; not a negative pilot\n\n- the val decode ended with exit %s (124 = the %s GPU-h cap; anything else is a fault)\n' "$CLS" "$rc" "$CAP" > "$O/STOP.md"
  printf '{"verdict": "NOT-RUN", "class": "%s -> TO-PI", "exit": %s, "cap_gpuh": %s}\n' "$CLS" "$rc" "$CAP" > "$O/gate0_decide.json"
  exit 0
fi
# 3. CPU: editor, scorer, STOP rules (a)-(e)
$PY scripts/grl/k2_gate0.py score --preds "$O/k2g0_qwen3vl_8b_val-detailed.preds.json" --freeze "$O/freeze.json" \
  --mem-log "$O/mem.log" --out "$O/gate0_decide.json"
