#!/bin/bash
# Paper C tier-1 GPU job (plan S10; DRAFT, not judge-read). Host: one rented RTX 3090 / 3090 Ti (host amendment v3,
# 5d6f5ca). Modes:
#   selftest  laptop-mock selftest on both host venvs, then the GPU-host selftests: hostcheck (mBLIP + S9 helpers)
#             -> HOSTCHECK_OK.json, hostcheck-en (LLaVA, EN venv, Q-LLAVA) -> HOSTCHECK_EN_OK.json
#   speed     prereg §10.1: SPEED_N XM3600-vi images x every VI arm + KT-C x S1-S5 (A8/S2 untimed, A8_PROXY);
#             timing rows only, captions never written (NB-SPEED); whole mode under 1.5 h (host v3 §6)
#   EN arms S1-S5 run with the EN venv's python (requirements_c_pvr_llava.lock), every other arm with the main venv.
#   tier1     every uncut arm of CAP.json on every set, under the wall-clock cap from the P1 stamp (T1-REP §9),
#             arm-major in three phases (CC-270 B1): never-cut, then A8 / S2, then the cuttable arms (A10 last).
#             The laptop pulls <set>.A1 once logs/tier1.<set>.A1.done exists and decomposes it while phase 1 runs;
#             it pushes /dev/shm/c_pvr_hc/a1_decomp/<set>.json, then a1_decomp/MANIFEST.sha256 last (B2); for S2
#             the same from logs/tier1.kt_c.S3.done and kt_c.S3 (CC-270r2 N5'). A8 / S2 wait
#             at most A8_WAIT_SEC (funded in P1); over it = JOB STOP (PI), never a cap stop.
# CAP.json is written once by `c_pvr_gpu.py cap` at the P1 LOG line (coordinator inputs S, r_host, PQ-C2 solvency).
# A cap or money stop is final (CAP_STOP.json; every later run refuses). This script never rents, tops up or deletes
# a machine; it only stops. Images and datastore material sit only in /dev/shm/c_pvr_hc (0700), sha-checked on
# arrival; a trap deletes that folder on ANY exit and logs (utc, folder, files, manifest count).
# Usage (tmux): bash scripts/c_pvr_gpu/c_pvr_job.sh MODE <expected 40-hex HEAD> <sha256 of /dev/shm/c_pvr_hc/MANIFEST.sha256>
set -euo pipefail
MODE=${1:?usage: c_pvr_job.sh selftest|speed|tier1 HEAD MANIFEST_SHA}; EXPECT=${2:?HEAD}; TMAN=${3:?MANIFEST sha}
cd "$(dirname "$0")/../.."
FREEZE_SHA=PENDING   # the GPU-lock freeze (setup_host.sh writes it); only home; required from mode speed on
FREEZE_SHA_EN=PENDING   # the same for the EN (LLaVA) venv
LK=$(sha256sum scripts/c_pvr_gpu/requirements_c_pvr_gpu.lock | cut -c1-8)
LKE=$(sha256sum scripts/c_pvr_gpu/requirements_c_pvr_llava.lock | cut -c1-8)
PY=$HOME/venvs/c_pvr_gpu_$LK/bin/python; PYE=$HOME/venvs/c_pvr_llava_$LKE/bin/python; X=scripts/c_pvr_gpu/c_pvr_gpu.py
O=$HOME/c_pvr_out; LOG=$O/logs; P=$O/out; HC=/dev/shm/c_pvr_hc; CAP=$O/CAP.json; MARK=$O/CAP_STOP.json
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HOME=$HOME/c_pvr_models/hf
export C_PVR_MBLIP=$(cat $O/mblip_snapshot.path)
export C_PVR_SNAPS=$O   # decode reads $O/<helper>_snapshot.path (S9 M-CLIP / XGLM), as hostcheck does
mkdir -p $LOG $P
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*" | tee -a $LOG/job.log; }
stop() { say "JOB STOP $*"; exit 1; }
exec 9> $O/.job.lock
flock -n 9 || { echo "REFUSED: another c_pvr job is running"; exit 1; }
teardown() {
  local rc=$?
  if [ -d $HC ]; then $PY -I -B $X wipe --dir $HC --log $O/c_pvr_hc_deletions.log || say "WIPE COUNT MISMATCH (rc $?)"; fi
  say "EXIT $MODE rc=$rc"
}
trap teardown EXIT

# ---------------------------------------------------------------- preflight
[ -e $MARK ] && stop "CAP_STOP.json exists: a cap stop is final"
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
sha256sum --quiet -c scripts/c_pvr_gpu/SHA256SUMS || stop "scripts/c_pvr_gpu/SHA256SUMS"
sha256sum --quiet -c scripts/c_pvr/SHA256SUMS || stop "scripts/c_pvr/SHA256SUMS"
export C_PVR_FREEZE=$($PY -m pip freeze | sha256sum | cut -c1-64)   # recorded in HOSTCHECK_OK.json
export C_PVR_FREEZE_EN=$($PYE -m pip freeze | sha256sum | cut -c1-64)   # recorded in HOSTCHECK_EN_OK.json
nvidia-smi --query-gpu=name --format=csv,noheader | grep -Eq '^NVIDIA GeForce RTX 3090( Ti)?$' || stop "GPU is not one 3090"
[ "$(stat -c %a $HC)" = 700 ] || stop "$HC is not mode 0700"
[ "$(sha256sum < $HC/MANIFEST.sha256 | cut -c1-64)" = "$TMAN" ] || stop "tmpfs MANIFEST.sha256 differs from the run doc"
(cd $HC && sha256sum --quiet -c MANIFEST.sha256) || stop "a tmpfs file differs from its arrival sha (FAULT)"
$PY -I -B $X selftest >> $LOG/selftest.log 2>&1 || stop "c_pvr_gpu selftest"
$PYE -I -B $X selftest >> $LOG/selftest.log 2>&1 || stop "c_pvr_gpu selftest (EN venv)"
sha256sum $X $0 scripts/c_pvr/c_pvr.py > $O/code_at_start_$MODE.sha256

if [ "$MODE" = selftest ]; then
  $PY -I -B $X hostcheck --mblip "$C_PVR_MBLIP" --kept $HC/kept --out $O >> $LOG/hostcheck.log 2>&1 || stop "hostcheck"
  $PYE -I -B $X hostcheck-en --out $O >> $LOG/hostcheck.log 2>&1 || stop "hostcheck-en"
  say "HOSTCHECK OK"; exit 0
fi
[ -s $O/HOSTCHECK_OK.json ] && [ -s $O/HOSTCHECK_EN_OK.json ] || stop "no HOSTCHECK_OK.json / HOSTCHECK_EN_OK.json (run mode selftest first)"
[ "$FREEZE_SHA" != PENDING ] && [ "$FREEZE_SHA_EN" != PENDING ] || stop "FREEZE_SHA(_EN) is PENDING (GPU locks not yet read)"
[ "$C_PVR_FREEZE" = "$FREEZE_SHA" ] || stop "venv freeze differs from the GPU lock"
[ "$C_PVR_FREEZE_EN" = "$FREEZE_SHA_EN" ] || stop "EN venv freeze differs from the LLaVA lock"
case "$MODE" in
  speed) STEPS=$($PY -I -B $X steps --mode speed)
         [ -s $O/speed_start.epoch ] || date +%s > $O/speed_start.epoch   # CC-270 N2: 1.5 h in total, not per run
         END=$(( $(cat $O/speed_start.epoch) + 5400 ));;
  tier1) STEPS=$($PY -I -B $X steps --mode tier1 --cap $CAP) || stop "CAP.json missing or not RUN";;
  *) stop "unknown mode $MODE";;
esac
$PY -I -B $X preflight --hostcheck $O/HOSTCHECK_OK.json --hostcheck-en $O/HOSTCHECK_EN_OK.json \
  --steps $(echo "$STEPS" | tr ' ' ':') || stop "stale HOSTCHECK_OK.json or pins PENDING"

cap_stop() { printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > $MARK; say "CAP STOP $1 (final)"; exit 0; }
while read -r SET ARM; do
  [ -s $LOG/$MODE.$SET.$ARM.done ] && continue
  ARGS=(decode --set $SET --arm $ARM --manifest $HC/manifest/$SET.json --kept $HC/kept --images $HC/images/$SET --democap $HC/democap)
  if [ "$MODE" = speed ]; then  # ids-only logs under speed/; no caption file is opened in speed mode
    LEFT=$(( END - $(date +%s) )); [ $LEFT -gt 0 ] || stop "speed test over 1.5 h before $SET $ARM"
    mkdir -p $O/speed
    ARGS+=(--speed --timing $O/timing.jsonl --out $O/speed)
  else
    ARGS+=(--out $P)
    LEFT=$($PY -I -B $X left --cap $CAP); [ "$LEFT" -gt 0 ] || cap_stop "cap reached before $SET $ARM"
    ARGS+=(--cap $CAP)
    case $ARM in A8|S2) ARGS+=(--a1-decomp $HC/a1_decomp/$SET.json);; esac
  fi
  case $ARM in S[1-5]) PYS=$PYE;; *) PYS=$PY;; esac   # LLaVA's own venv (Q-LLAVA)
  say "START $SET $ARM (left $(( LEFT / 60 )) min)"
  rc=0; timeout ${LEFT}s $PYS -I -B $X "${ARGS[@]}" >> $LOG/decode.log 2>&1 || rc=$?
  if [ $rc = 124 ] || [ $rc = 4 ]; then [ "$MODE" = speed ] && stop "speed test over 1.5 h"; cap_stop "during $SET $ARM"; fi
  [ $rc = 0 ] || stop "$SET $ARM rc=$rc"
  ts > $LOG/$MODE.$SET.$ARM.done; say "OK $SET $ARM"
done <<< "$STEPS"
(cd $O && find out logs -type f | sort | xargs -r sha256sum) > $O/SHA256SUMS_$MODE
say "JOB DONE $MODE"
