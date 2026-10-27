#!/bin/bash
# G-RL Gate 0 (PILOT_RULE.md §5): 30 G-RL steps and 30 SFT steps on UT train images, a 40-image base sample and a
# 40-image greedy decode, to measure s/unit and peak memory and project Gate 1 at the full data. Its adapters are
# discarded. M3 (PI-1026r); M4 only after a K2 or G-RL Gate 1 GO (PI-1026aa Q6). Idle GPU, never concurrent with a
# test decode. Reads no val or test image.
#   EXPECT_HEAD=<commit of the pilot rule> [SIZE=7b|3b] bash scripts/grl/gate0.sh
set -euo pipefail
cd /root/vsps && . .venv/bin/activate
export NCS_DATA=/root/ncs-data NCS_DATASET=uitviic HF_HUB_OFFLINE=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
HEAD=${EXPECT_HEAD:?set EXPECT_HEAD to the commit of the pilot rule}
SIZE=${SIZE:-7b}
UV=$NCS_DATA/datasets/uitviic
O=/root/outputs/grl_pilot/gate0_$SIZE
[ ! -e "$O" ] || { echo "STOP: $O exists (Gate 0 runs once per size)"; exit 1; }
K2=/root/outputs/grl_pilot/k2   # CC-119 PD-GR-3 (ruling 8): K2 Gate 0/0b first on M3
[ -e "$K2/gate0_decide.json" ] || [ -e "$K2/STOP.md" ] || { echo "REFUSED: K2 Gate 0/0b has not been decided"; exit 1; }
if [ "$SIZE" = 3b ]; then  # CC-124 W6: SWITCH-3B verdict, or a logged PI line PI_OK=3B (memory STOP goes to the PI)
  python3 - "${PI_OK:-}" <<'PYEOF'
import json, sys
d = json.load(open("/root/outputs/grl_pilot/gate0_7b/gate0_decide.json"))
assert d["verdict"] == "SWITCH-3B" or sys.argv[1] == "3B", f"7B verdict {d['verdict']} and no PI_OK=3B"
PYEOF
  echo "3B run: Qwen2.5-VL-3B-Instruct rev 66285546 (qwen-research licence, disclosed); PI_OK=${PI_OK:-}"
fi
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
for s in id_counts common reward train score_dev decide; do python3 scripts/grl/$s.py --selftest; done
G() { python3 scripts/grl/common.py guard "$HEAD"; }
G
if [ ! -s "$UV/images.sha256" ]; then python3 scripts/grl/common.py stage "$UV/src" && rm -rf "$UV/src"; fi
G
mkdir -p "$O"
M=$(python3 -c "import sys; sys.path.insert(0, 'scripts/grl'); import common as K; print(K.MODELS['$SIZE'][2])")
# CC-124 W5: every GPU stage runs under timeout against a 3 GPU-h aggregate wall (planning 1.5-2.5); a cap hit is
# "NOT RUN (cost)" -> TO-PI, no decide.py, no rerun (CC-104d).
WALL=3.0; T0=$(date +%s)
left() { python3 -c "print(max(0.0, round($WALL - ($(date +%s) - $T0) / 3600, 3)))"; }
cost_stop() { printf '{"verdict": "NOT-RUN", "class": "cost -> TO-PI", "why": "%s", "wall_gpuh": %s}\n' "$1" "$WALL" > "$O/gate0_decide.json"
              printf '# G-RL Gate 0 NOT RUN (cost) -> TO-PI; not a verdict\n\n- %s\n' "$1" > "$O/STOP.md"; exit 0; }
T() { local what=$1; shift; local rc=0 s
      s=$(python3 -c "print(int($(left) * 3600))")   # CC-125 X4: zero remaining budget stops, never runs uncapped
      [ "$s" -ge 1 ] || cost_stop "3 GPU-h wall reached before $what"
      timeout "$s" "$@" || rc=$?
      if [ "$rc" = 124 ] || [ "$rc" = 3 ]; then cost_stop "3 GPU-h wall reached in $what"; fi
      [ "$rc" = 0 ] || exit "$rc"; }
T sample python3 scripts/grl/train.py sample --size "$SIZE" --limit 40 --out "$O/samples.jsonl" --budget-hours "$(left)"
# provisional window for the 30 timing steps only (Gate 1 re-anchors on all 2,402 UT images)
python3 - "$O" <<'EOF'
import json, sys
sys.path.insert(0, "scripts/grl")
import reward as RW
from rl_reward import syllables
o = sys.argv[1]
rows = [json.loads(x) for x in open(f"{o}/samples.jsonl", encoding="utf-8")]
lens = [len(syllables(c)) for r in rows for c, d in zip(r["samples"], r["finished"]) if d] or [1]
json.dump(RW.anchors(lens) | {"label": "Gate 0 provisional"}, open(f"{o}/anchors_gate0.json", "w"))
EOF
G
T grl python3 scripts/grl/train.py train --arm grl --size "$SIZE" --out "$O/grl" --anchors "$O/anchors_gate0.json" \
  --max-steps 30 --dry-run --budget-hours "$(left)"
G
T sftref python3 scripts/grl/train.py train --arm sftref --size "$SIZE" --out "$O/sft" --anchors "$O/anchors_gate0.json" \
  --max-steps 30 --budget-hours "$(left)"
G
T greedy bash -c "set -o pipefail; python3 scripts/evaluate.py --model '$M' --split train_data.json --prompt detailed --limit 40 \
  --name 'gate0_greedy_$SIZE' --out '$O/greedy_eval.json' | tee '$O/greedy.log'"
python3 - "$O" <<'EOF'
import json, re, sys
o = sys.argv[1]
m = re.findall(r"\[40/40\] ([0-9.]+)s/image", open(f"{o}/greedy.log").read())
assert m, "evaluate.py printed no 40/40 rate"
json.dump({"images": 40, "seconds": 40 * float(m[-1]), "source": "evaluate.py [40/40] rate"}, open(f"{o}/greedy.json", "w"))
EOF
python3 scripts/grl/decide.py gate0 --dir "$O" --size "$SIZE" --out "$O/gate0_decide.json"
