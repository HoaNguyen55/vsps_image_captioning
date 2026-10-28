#!/bin/bash
# W25 near-duplicate pass on M3 (manuscript/prereg/2026-10-28_w25_neardup/RULE.md; CC-148 W9, CC-151). CPU only, in
# venv-cenfeat (C-EN's features venv, freeze 1a639a50). Import check first; guard verbatim before and after; OIV7 val
# bytes only in /dev/shm/w25, one batch at a time, every deletion logged; one wall cap of 3.25 h for the whole pass.
#   EXPECT_HEAD=<commit of the W25 rule> GPU=m3 bash scripts/w25/w25_job.sh        (/root/vsps, inside tmux)
#   bash scripts/w25/w25_job.sh --selftest                                       (CPU, repo root; needs $FT)
# A fault writes W25_FAULT_<utc>.txt and exits 0; a logged rerun resumes from finished parts. Exit 124 = NOT-RUN
# (cost) -> TO-PI, and K2 Gate 1 stays HELD.
set -euo pipefail
H_FT=1a639a50adf550c50c6dfe284146e279b2a2bf2a716ade743e9eb357ccbf0778   # cenfeat_venv_freeze.txt (C-EN PREREG §2)
D=scripts/w25
FT=${FT:-/root/venv-cenfeat/bin/python}
if [ "${1:-}" = "--selftest" ]; then
  bash -n "$0"
  $FT $D/w25.py --selftest
  sha256sum --quiet -c $D/SHA256SUMS
  ! grep -qE '[|] *t[e]e' "$0" || { echo "a tee pipe masks exit codes (the N9 bug)"; exit 1; }
  r=0; out=$(GPU=m4 EXPECT_HEAD=x bash "$0" 2>&1) || r=$?
  [ "$r" = 1 ] && [[ $out == *"M3 only"* ]] || { echo "GPU=m4 was not refused"; exit 1; }
  echo "w25_job selftest ok"
  exit 0
fi
[ "${GPU:-}" = m3 ] || { echo "REFUSED: W25 runs on M3 only (CC-148 W9); GPU=${GPU:-unset}"; exit 1; }
cd /root/vsps
export NCS_DATA=/root/ncs-data
HEAD=${EXPECT_HEAD:?set EXPECT_HEAD to the commit of the W25 rule}
X=$D/w25.py
SSCD=/root/ncs-data/models/sscd_disc_mixup.torchscript.pt
O=/root/outputs/w25; LOCK=$O/RUNNING; SHM=/dev/shm/w25; CAP_S=11700   # 3.25 h (CC-151 r6: W25 reserve in dev 40)
[ ! -e "$O/w25_decide.json" ] || { echo "STOP: W25 already decided (one look)"; exit 1; }
[ "$(tr -d '[:space:]' < /root/.vsps_machine_id)" = m3 ] || { echo "REFUSED: this host is not m3"; exit 1; }
[ "$(git rev-parse HEAD)" = "$HEAD" ] || { echo "REFUSED: HEAD is not $HEAD"; exit 1; }
git diff --quiet HEAD -- || { echo "REFUSED: tracked files differ from HEAD"; exit 1; }
[ -n "${TMUX:-}" ] || { echo 'REFUSED: run inside a tmux session'; exit 1; }
[ "$(tmux ls 2>/dev/null | wc -l)" = 1 ] || { echo "REFUSED: another tmux session exists"; exit 1; }
OTHER=$(ls /root/outputs/*/RUNNING 2>/dev/null || true)
[ -z "$OTHER" ] || { echo "REFUSED: a lock exists: $OTHER"; exit 1; }
mkdir -p "$O"
( set -o noclobber; echo "$0 $(date -u +%FT%TZ)" > "$LOCK" ) || { echo "REFUSED: $LOCK exists"; exit 1; }
cleanup() {  # on every exit: no OIV7 byte survives the job, and the deletion is logged (RULE §5)
  if [ -e "$SHM" ]; then rm -rf "$SHM"; echo "$(date -u +%FT%TZ) deleted $SHM at job exit" >> "$O/deletions.log"; fi
  rm -f "$LOCK"
}
trap cleanup EXIT
echo "$(date -u +%FT%TZ) start head $HEAD" >> "$O/runs.log"
fault() {
  echo "$1" > "$O/W25_FAULT_$(date -u +%Y%m%dT%H%M%SZ).txt"
  echo "$(date -u +%FT%TZ) FAULT: $1" >> "$O/runs.log"
  echo "W25 NOT RUN (fault) -> TO-PI: $1"
  exit 0
}
# 0. import check first, then selftest, the freeze, the pinned weights and C-EN features (CC-153 W2), and the guard
#    verbatim (no /dev/shm/w25); all before any fetch
rc=0; $FT $X imports >> "$O/runs.log" 2>&1 || rc=$?
[ "$rc" = 0 ] || fault "venv-cenfeat import check exit $rc (3 = a module or symbol is missing)"
bash $0 --selftest >> "$O/runs.log" 2>&1 || fault "selftest"
[ "$($FT -m pip freeze | sha256sum | cut -c1-64)" = "$H_FT" ] || fault "venv-cenfeat freeze differs from ${H_FT:0:8}"
$FT -m pip check >> "$O/runs.log" 2>&1 || fault "venv-cenfeat pip check"
[ "$(sha256sum "$SSCD" | cut -c1-64)" = 9f26bd4c848cc19b73d2ae92eea6e04886f61a7b764ceb7a13aeee62e6a6db56 ] || fault "SSCD weights"
$FT $X preflight >> "$O/runs.log" 2>&1 || fault "preflight: C-EN features, KV ids or NoCaps id map"
$FT $X guard "$HEAD" >> "$O/runs.log" 2>&1 || fault "guard refused before W25"
# 1-2. features under one wall cap; the deadline is fixed at the first start, so a rerun never resets it
[ -s "$O/deadline" ] || echo $(( $(date +%s) + CAP_S )) > "$O/deadline"
run() {  # run NAME command...
  local name=$1 left rc=0; shift
  left=$(( $(cat "$O/deadline") - $(date +%s) ))
  [ "$left" -gt 0 ] || { echo "$(date -u +%FT%TZ) NOT-RUN (cost): cap spent before $name" >> "$O/runs.log"; exit 0; }
  timeout "$left" "$@" >> "$O/$name.log" 2>&1 || rc=$?
  if [ "$rc" = 124 ]; then
    echo "$(date -u +%FT%TZ) NOT-RUN (cost): exit 124 in $name (3.25 h cap); Gate 1 stays HELD" >> "$O/runs.log"
    echo "W25 NOT RUN (cost) -> TO-PI"; exit 0
  fi
  [ "$rc" = 0 ] || fault "$name exit $rc"
}
[ -s "$O/feats_ut.npz" ] || run feats_ut $FT $X feats-ut --sscd $SSCD --out "$O/feats_ut.npz"
run feats_oiv7 $FT $X feats-oiv7 --sscd $SSCD --parts "$O/oiv7_parts"
# 3. bytes gone: no w25.py process left (CC-153 W3; w25[.]py, as the plain path also matches this job), no
#    /dev/shm/w25, and the guard verbatim again (its scan is the logged proof)
rc=0; pgrep -f 'scripts/w25/w25[.]py' > /dev/null || rc=$?
[ "$rc" = 1 ] || fault "a w25.py process is still running (or pgrep failed, rc $rc) before the post-run guard"
[ ! -e "$SHM" ] || fault "$SHM still exists after the OIV7 pass"
$FT $X guard "$HEAD" >> "$O/runs.log" 2>&1 || fault "guard refused after W25"
echo "$(date -u +%FT%TZ) post-run guard ok; OIV7 val bytes deleted (deletions.log)" >> "$O/runs.log"
# 4. the one look (CPU)
$FT $X decide --ut "$O/feats_ut.npz" --parts "$O/oiv7_parts" --out-dir "$O" >> "$O/runs.log" 2>&1 || fault "decide"
(cd "$O" && sha256sum w25_decide.json w25_excluded_ids.txt feats_ut.npz deletions.log oiv7_parts/part_*.npz > SHA256SUMS)
echo "$(date -u +%FT%TZ) decided" >> "$O/runs.log"
