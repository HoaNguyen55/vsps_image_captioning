#!/bin/bash
# G-RL Gate 1 (PILOT_RULE.md §6): full UT-2402 train (2,532 reported beside it), full val-924 dev, Vietnamese; arms base (no training), SFT-ref,
# RFT, G-RL; one look; GO iff G-RL - SFT-ref passes every criterion. Stops at the Gate-0 cap (no result).
# M3 (PI-1026r) or M4, idle GPU, never concurrent with a test decode. Pilot runs are not confirmatory seeds.
#   EXPECT_HEAD=<commit of the pilot rule> SIZE=<Gate-0 size with verdict GO, or TO-PI with PI_OK=<LOG id>> bash scripts/grl/gate1.sh
set -euo pipefail
cd /root/vsps && . .venv/bin/activate
export NCS_DATA=/root/ncs-data NCS_DATASET=uitviic HF_HUB_OFFLINE=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
HEAD=${EXPECT_HEAD:?set EXPECT_HEAD to the commit of the pilot rule}
SIZE=${SIZE:?set SIZE to the Gate-0 size}
D0=/root/outputs/grl_pilot/gate0_$SIZE/gate0_decide.json
O=/root/outputs/grl_pilot/gate1
[ ! -e "$O/gate1_decide.json" ] || { echo "STOP: Gate 1 already decided (one look)"; exit 1; }
K2=/root/outputs/grl_pilot/k2   # CC-119 PD-GR-3: K2 Gate 1 (if approved) runs before this; a K2 STOP or a logged waiver frees it
[ -e "$K2/STOP.md" ] || [ -e "$K2/gate1_decide.json" ] || [ -n "${K2_ORDER_WAIVER:-}" ] \
  || { echo "REFUSED: K2 Gate 1 not decided and no K2_ORDER_WAIVER=<LOG id>"; exit 1; }
CAP=$(python3 - "$D0" "${PI_OK:-}" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1]))
ok = d["verdict"] == "GO" or (d["verdict"] == "TO-PI" and sys.argv[2])
sys.exit(f"REFUSED: Gate 0 verdict {d['verdict']}") if not ok else print(d["cap_gpuh"])
EOF
)
# CC-124 W1: inside tmux only. cen_chain.sh refuses to start a C-EN step while any tmux session exists (C-EN PREREG
# l.129), so a pilot in tmux blocks C-EN at code level; m3_clear + the RUNNING lock block the pilot while C-EN runs.
[ -n "${TMUX:-}" ] || { echo 'REFUSED: run inside a tmux session (C-EN PREREG l.129 / cen_chain.sh:42 refuse while one exists)'; exit 1; }
# Lock for the whole run (PILOT_RULE.md §7): refused if it exists; the operator starts no C-EN step while it exists.
LOCK=/root/outputs/grl_pilot/RUNNING
mkdir -p /root/outputs/grl_pilot
[ ! -e "$LOCK" ] || { echo "REFUSED: $LOCK exists"; exit 1; }
echo "$0 $(date -u +%FT%TZ)" > "$LOCK"; trap 'rm -f "$LOCK"' EXIT
[ "$(pip freeze | sha256sum | cut -c1-64)" = 7332d343173e5681365cf6871671e36209c77803a1b2db70da1cc766d5c943ed ] \
  || { echo "REFUSED: .venv freeze differs from setup_gpu.sh H_VS"; exit 1; }
for s in common reward train score_dev decide; do python3 scripts/grl/$s.py --selftest; done
M=$(python3 -c "import sys; sys.path.insert(0, 'scripts/grl'); import common as K; print(K.MODELS['$SIZE'][2])")
mkdir -p "$O"
T0=$(cat "$O/started_epoch" 2>/dev/null || { date +%s | tee "$O/started_epoch"; })
left() { python3 -c "print(round($CAP - ($(date +%s) - $T0) / 3600, 3))"; }
G() {  # guard + cap before every GPU stage
  python3 scripts/grl/common.py guard "$HEAD"
  if python3 -c "import sys; sys.exit(0 if $(left) > 0 else 1)"; then return 0; fi
  echo "{\"verdict\": \"STOP\", \"why\": \"cap $CAP GPU-h reached before $1\"}" > "$O/gate1_decide.json"; exit 3
}
A=(--size "$SIZE" --anchors "$O/anchors.json")
if [ ! -s "$O/samples.jsonl.summary.json" ]; then
  G samples; rc=0
  python3 scripts/grl/train.py sample --size "$SIZE" --out "$O/samples.jsonl" --budget-hours "$(left)" || rc=$?
  if [ "$rc" = 3 ]; then echo '{"verdict": "STOP", "why": "cap reached in samples"}' > "$O/gate1_decide.json"; fi
  [ "$rc" = 0 ] || exit "$rc"
fi
[ -s "$O/anchors.json" ] || python3 scripts/grl/train.py anchors --samples "$O/samples.jsonl" --out "$O/anchors.json"
[ -s "$O/picks.jsonl" ] || python3 scripts/grl/train.py rft-pick --samples "$O/samples.jsonl" --anchors "$O/anchors.json" --out "$O/picks.jsonl"
for arm in grl rft sftref; do
  [ -s "$O/$arm/summary.json" ] && continue
  G "$arm"
  rc=0
  python3 scripts/grl/train.py train --arm "$arm" "${A[@]}" --out "$O/$arm" --picks "$O/picks.jsonl" \
    --budget-hours "$(left)" || rc=$?
  if [ "$rc" = 3 ]; then echo "{\"verdict\": \"STOP\", \"why\": \"cap reached in $arm\"}" > "$O/gate1_decide.json"; fi
  [ "$rc" = 0 ] || exit "$rc"   # any other failure is a crash, not a verdict: fix the cause, rerun this stage
done
for s in base sftref rft grl; do
  P=$O/dev/$s-val924-detailed
  [ -s "$P.preds.json" ] && continue
  G "decode $s"
  mkdir -p "$O/dev"
  AD=(); [ "$s" = base ] || AD=(--adapter "$O/$s/last")
  rc=0  # CC-124 W5: the decode timeout is the remaining cap; CC-125 X4: zero remaining budget is a cap STOP
  s=$(python3 -c "print(int($(left) * 3600))")
  if [ "$s" -lt 1 ]; then echo "{\"verdict\": \"STOP\", \"why\": \"cap $CAP GPU-h reached before decode $s\"}" > "$O/gate1_decide.json"; exit 3; fi
  timeout "$s" python3 scripts/evaluate.py --model "$M" "${AD[@]}" \
    --split val_data.json --prompt detailed --name "$s-val924-detailed" --out "$P.json" || rc=$?
  if [ "$rc" = 124 ]; then echo "{\"verdict\": \"STOP\", \"why\": \"cap $CAP GPU-h reached in decode $s\"}" > "$O/gate1_decide.json"; exit 3; fi
  [ "$rc" = 0 ] || exit "$rc"
done
python3 scripts/grl/score_dev.py --dir "$O/dev" --out "$O/scores.json"
python3 scripts/grl/decide.py gate1 --scores "$O/scores.json" --run "$O" --out "$O/gate1_decide.json"
