#!/bin/bash
# K2 P2 dev pilot (K2_GATE0_RULE.md §6c; CC-136P W2-W3, W8-W9, W12-W13): Grounding DINO-T presence sets on UIT-ViIC
# val 924 replace gold in the pinned K2 editor, on Gate 0's own decodes; the CPU part reproduces E_gold first (W3)
# and decides. A target ceiling only. M3 after B-2 CLEANUP DONE, never concurrent with another job (W12).
#   EXPECT_HEAD=<commit of §6c> GD_FREEZE=<venv-gd freeze sha256 from the OPS line> bash scripts/grl/k2_p2.sh
# One look = p2_decide.json (W13). A fault writes P2_FAULT_<utc>.md and exit 0; a rerun is allowed (and logged)
# until p2_decide.json exists. A cap hit (124) is NOT RUN (cost) and closes the pilot.
set -euo pipefail
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
HEAD=${EXPECT_HEAD:?set EXPECT_HEAD to the commit of K2_GATE0_RULE §6c}
GD_FREEZE=${GD_FREEZE:?set GD_FREEZE to the venv-gd pip-freeze sha256 recorded in the OPS line after the build (W8)}
PY=/root/vsps/.venv/bin/python
GD=/root/venv-gd/bin/python
UV=$NCS_DATA/datasets/uitviic
K2=/root/outputs/grl_pilot/k2
O=$K2/p2
G0=0b6da7e083af7da3d2cc7c7584c9888007c0ec33d9b8b58d2ecd763b324317a5   # gate0_decide.json (OPS-1028c); never written here
[ ! -e "$O/p2_decide.json" ] || { echo "STOP: K2 P2 already decided (one look, W13)"; exit 1; }
# W12: inside its own tmux session, with no other session, no other lock, no B-2 stage and no B-2 process
[ -n "${TMUX:-}" ] || { echo 'REFUSED: run inside a tmux session (C-EN PREREG l.129 / cen_chain.sh:42)'; exit 1; }
[ "$(tmux ls 2>/dev/null | wc -l)" = 1 ] || { echo "REFUSED: another tmux session exists (W12)"; exit 1; }
[ ! -e /root/ncs-data/b2_stage ] || { echo "REFUSED: /root/ncs-data/b2_stage exists: B-2 cleanup is not done (W12)"; exit 1; }
! pgrep -f scripts/b2_external/ > /dev/null || { echo "REFUSED: a B-2 process is running (W12)"; exit 1; }
OTHER=$(ls /root/outputs/*/RUNNING 2>/dev/null || true)
[ -z "$OTHER" ] || { echo "REFUSED: a lock exists: $OTHER"; exit 1; }
LOCK=/root/outputs/grl_pilot/RUNNING   # common.LOCK (rule §3)
mkdir -p "$O"
( set -o noclobber; echo "$0 $(date -u +%FT%TZ)" > "$LOCK" ) || { echo "REFUSED: $LOCK exists"; exit 1; }
trap 'rm -f "$LOCK"' EXIT
echo "$(date -u +%FT%TZ) start head $HEAD" >> "$O/runs.log"   # W13: every attempt, faulted or not, is logged
fault() {
  $PY scripts/grl/k2_p2.py notrun --class fault --why "$1" --out-dir "$O"
  echo "$(date -u +%FT%TZ) NOT RUN (fault): $1" >> "$O/runs.log"
  echo "K2 P2 NOT RUN (fault) -> TO-PI: $1"
  exit 0
}
g0() { [ "$(sha256sum "$K2/gate0_decide.json" | cut -c1-64)" = "$G0" ] || fault "gate0_decide.json differs from 0b6da7e0"; }
g0
[ "$($GD -m pip freeze | sha256sum | cut -c1-64)" = "$GD_FREEZE" ] || fault "venv-gd freeze differs from GD_FREEZE (W8)"
export GD_FREEZE_SHA256="$GD_FREEZE"
for s in common reward k2_gate0 k2_p2; do $PY scripts/grl/$s.py --selftest; done
$GD scripts/grl/k2_p2_detect.py --selftest
G() { $PY scripts/grl/common.py guard "$HEAD"; }   # host, idle GPU, HEAD + clean tree, m3_clear, test-image scan
G
if [ ! -s "$UV/images.sha256" ]; then   # separate lines: a stage failure stops the job (set -e)
  $PY scripts/grl/common.py stage "$UV/src"
  rm -rf "$UV/src"
fi
G
$PY scripts/grl/k2_p2_detect.py fetch || fault "pinned weights / BERT fetch or sha256 (W8)"
# W3 + W9 before any GPU work: shas, val_ids_ok, the 924 staged val shas, the class space, E_gold = 1.795 / 65.28 / 277
rc=0
$PY scripts/grl/k2_p2.py repro --k2-dir "$K2" --out-dir "$O" || rc=$?
if [ "$rc" = 3 ]; then
  echo "$(date -u +%FT%TZ) NOT RUN (fault): W3 (P2_FAULT_*.md)" >> "$O/runs.log"
  echo "K2 P2 NOT RUN (fault) -> TO-PI: W3 (P2_FAULT_*.md)"
  exit 0
elif [ "$rc" != 0 ]; then
  fault "repro exit $rc"
fi
if [ -s "$O/p2_detect.json" ] && (cd "$O" && sha256sum -c --status p2_detect.sha256 2> /dev/null); then
  echo "p2_detect.json from a faulted attempt matches its hash: reused, no GPU step (W13)"
else
  [ ! -e "$O/p2_detect.json" ] || fault "p2_detect.json exists without a matching p2_detect.sha256"
  # W12 smoke: 2 UT-2402 train images (never val), asserts and run figures only, D not kept; not a look
  G
  rc=0
  timeout 600 $GD scripts/grl/k2_p2_detect.py smoke --out "$O/smoke_$(date -u +%Y%m%dT%H%M%SZ).json" 2>&1 | tee -a "$O/smoke.log" || rc=$?
  [ "$rc" = 0 ] || fault "smoke exit $rc (W12; 124 = the 600 s smoke timeout, CC-137 W1)"
  G
  rc=0
  timeout 1800 $GD scripts/grl/k2_p2_detect.py run --out "$O/p2_detect.json" 2>&1 | tee -a "$O/detect.log" || rc=$?
  if [ "$rc" = 124 ]; then
    $PY scripts/grl/k2_p2.py notrun --class cost --why "detector exit 124 (the 1800 s cap)" --out-dir "$O"
    echo "$(date -u +%FT%TZ) NOT RUN (cost)" >> "$O/runs.log"
    echo "K2 P2 NOT RUN (cost) -> TO-PI; not a negative pilot"
    exit 0
  fi
  [ "$rc" = 0 ] || fault "detector exit $rc"
  (cd "$O" && sha256sum p2_detect.json > p2_detect.sha256)   # W13: hashed before E_det is built
fi
rc=0
$PY scripts/grl/k2_p2.py decide --k2-dir "$K2" --detect "$O/p2_detect.json" --out-dir "$O" || rc=$?
g0
[ "$rc" = 0 ] || [ "$rc" = 3 ] || fault "decide exit $rc"
echo "$(date -u +%FT%TZ) end rc $rc" >> "$O/runs.log"
