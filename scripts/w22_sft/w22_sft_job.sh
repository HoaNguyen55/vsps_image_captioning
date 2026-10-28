#!/bin/bash
# W22-SFT memory probe on M3 (manuscript/prereg/2026-10-28_w22_sft/PREREG.md; CC-148 W2, PI-1026ax: M3 kept, train images
# only). QLoRA NF4 SFT of Qwen3-VL-8B @ 0c351dd, 512-token synthetic targets, micro-batch 1; C1 without gradient
# checkpointing, C2 with it only after a C1 memory failure. Cap 0.75 GPU-h over every GPU process, faults included.
#   EXPECT_HEAD=<commit of the PREREG> bash scripts/w22_sft/w22_sft_job.sh       (M3, /root/vsps, inside tmux)
#   bash scripts/w22_sft/w22_sft_job.sh --selftest                               (CPU, repo root)
# One look = w22_decide.json. A fault writes W22_FAULT_<utc>.md and exits 0; a rerun is logged and allowed until
# w22_decide.json exists. Exit 124 (the cap) is NOT-RUN (cost) and closes the probe.
set -euo pipefail
H_Q3=2bb7397e7db350a2c225df590cdd9531df6a3247f7a3f217e1b64ed2d9f1be80   # sha256 of venv_q3_freeze.txt
D=scripts/w22_sft
if [ "${1:-}" = "--selftest" ]; then
  bash -n "$0" && python3 $D/w22_sft.py --selftest && sha256sum --quiet -c $D/SHA256SUMS \
    && [ "$(sha256sum < $D/venv_q3_freeze.txt | cut -c1-64)" = "$H_Q3" ] && echo "w22_sft_job selftest ok"
  exit
fi
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
HEAD=${EXPECT_HEAD:?set EXPECT_HEAD to the commit of the W22-SFT PREREG}
VQ=/root/venv-q3; PY=$VQ/bin/python; X=$D/w22_sft.py
SNAP=/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd
O=/root/outputs/w22_sft; LOCK=$O/RUNNING; L=$O/gpu_seconds.tsv
[ ! -e "$O/w22_decide.json" ] || { echo "STOP: W22-SFT already decided (one look)"; exit 1; }
[ "$(git rev-parse HEAD)" = "$HEAD" ] || { echo "REFUSED: HEAD is not $HEAD"; exit 1; }
git diff --quiet HEAD -- || { echo "REFUSED: tracked files differ from HEAD"; exit 1; }
[ -n "${TMUX:-}" ] || { echo 'REFUSED: run inside a tmux session'; exit 1; }
[ "$(tmux ls 2>/dev/null | wc -l)" = 1 ] || { echo "REFUSED: another tmux session exists"; exit 1; }
[ ! -e /root/ncs-data/b2_stage ] || { echo "REFUSED: /root/ncs-data/b2_stage exists"; exit 1; }
OTHER=$(ls /root/outputs/*/RUNNING 2>/dev/null || true)
[ -z "$OTHER" ] || { echo "REFUSED: a lock exists: $OTHER"; exit 1; }
mkdir -p "$O"; touch "$L"
( set -o noclobber; echo "$0 $(date -u +%FT%TZ)" > "$LOCK" ) || { echo "REFUSED: $LOCK exists"; exit 1; }
trap 'rm -f "$LOCK"' EXIT
echo "$(date -u +%FT%TZ) start head $HEAD" >> "$O/runs.log"
fault() {
  printf '# W22-SFT fault (%s)\n\n%s\n\nNo verdict; a rerun is allowed and logged (PREREG §6).\n' "$(date -u +%FT%TZ)" "$1" \
    > "$O/W22_FAULT_$(date -u +%Y%m%dT%H%M%SZ).md"
  echo "$(date -u +%FT%TZ) FAULT: $1" >> "$O/runs.log"
  echo "W22-SFT FAULT: $1"
  exit 0
}
cost() {
  python3 $X decide --dir "$O" --cost "$1"
  echo "$(date -u +%FT%TZ) NOT-RUN (cost): $1" >> "$O/runs.log"
  echo "W22-SFT NOT-RUN (cost) -> TO-PI: $1"
  exit 0
}
bash $0 --selftest || fault "selftest"
# venv-q3: built once if absent (no .built marker), then the freeze sha and pip check on every run
if [ ! -e $VQ/.built ]; then
  rm -rf $VQ
  python3.10 -m venv $VQ || fault "venv create"
  $PY -m pip install --no-deps --index-url https://download.pytorch.org/whl/cu121 \
    --extra-index-url https://pypi.org/simple -r $D/venv_q3_freeze.txt >> "$O/venv_build.log" 2>&1 || fault "venv install"
fi
[ "$($PY -m pip freeze | sha256sum | cut -c1-64)" = "$H_Q3" ] || fault "venv-q3 freeze differs from venv_q3_freeze.txt"
$PY -m pip check >> "$O/runs.log" 2>&1 || fault "venv-q3 pip check"
touch $VQ/.built   # only after the freeze sha and pip check pass
python3 $X snapcheck --snapshot $SNAP || fault "snapshot pins"
G() { /root/vsps/.venv/bin/python scripts/grl/common.py guard "$HEAD"; }   # host, idle GPU, HEAD + clean tree, test scan
G || fault "guard refused"
rc=0; $PY $X imports --snapshot $SNAP || rc=$?   # every module the probe uses, before any GPU step
[ "$rc" = 0 ] || fault "import check exit $rc (3 = a module or symbol is missing)"
[ -s "$O/plan.json" ] || $PY $X plan --out "$O/plan.json" || fault "plan (UT-2402 images staged and sha-checked?)"
used() { awk -F'\t' '{s += $2} END {print s + 0}' "$L"; }
gpu() {  # one config in its own process, under timeout = the cap minus every earlier GPU second
  local c=$1 left t0 rc=0
  if [ -s "$O/$c.json" ] && (cd "$O" && sha256sum -c --status "$c.json.sha256" 2>/dev/null); then
    echo "$(date -u +%FT%TZ) $c.json from an earlier attempt matches its hash: reused, no GPU step" >> "$O/runs.log"
    return 0
  fi
  left=$(( 2700 - $(used) ))
  [ "$left" -gt 0 ] || cost "cap spent before $c"
  G || fault "guard refused before $c"
  rm -f "$O/$c.json"
  t0=$(date +%s)
  timeout "$left" $PY $X run --config "$c" --plan "$O/plan.json" --snapshot $SNAP --out "$O/$c.json" \
    2>&1 | tee -a "$O/$c.log" || rc=$?
  printf '%s\t%s\n' "$c" $(( $(date +%s) - t0 )) >> "$L"
  [ "$rc" = 124 ] && cost "exit 124 in $c (the 0.75 GPU-h cap)"
  [ "$rc" = 0 ] || fault "$c exit $rc"
  (cd "$O" && sha256sum "$c.json" > "$c.json.sha256")
}
gpu c1
if python3 $X memfail --rec "$O/c1.json"; then
  echo "$(date -u +%FT%TZ) C1 memory failure: C2 (gradient checkpointing) runs" >> "$O/runs.log"
  gpu c2
fi
python3 $X decide --dir "$O" || fault "decide"
(cd "$O" && sha256sum plan.json c*.json w22_decide.json > SHA256SUMS)
echo "$(date -u +%FT%TZ) decided $(sha256sum < "$O/w22_decide.json" | cut -c1-16)" >> "$O/runs.log"
