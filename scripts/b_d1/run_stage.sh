#!/usr/bin/env bash
# One B-D1 stage under the 8 CPU-h hard stop (COMPUTE_B_D1_v2.md; CC-505 B6).
#   scripts/b_d1/run_stage.sh s0 RECORDS - - [WHEEL_DIR]          the S0 checks (run_tests.sh, with --env if given)
#   scripts/b_d1/run_stage.sh s1 RECORDS WORK OUT --baselines B --pyvi-wheel P --uts-wheel U
#   scripts/b_d1/run_stage.sh g0 RECORDS WORK OUT --npz-sha X
#   scripts/b_d1/run_stage.sh s2 RECORDS WORK OUT --npz-sha X --g0-sha Y
# Before the stage: refuse when the CPU seconds left (28,800 minus user+sys of every *.time record) are 0 or a STOP
# marker exists. The stage runs under GNU `time -v` (record RECORDS/<stage>.<utc>.time) and `prlimit --cpu=<left>`,
# writing into OUT/.staging-<stage> (existing OUT files are linked in). After it: if rc != 0 (SIGXCPU included) or no
# seconds are left, write RECORDS/STOP, keep the staging dir as .rejected-<stage>, move nothing: no result. Otherwise
# move the new files into OUT. NCS_DATA must be set for s1, g0 and s2. PY defaults to /root/venv-bd1/bin/python.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
S=$1; R=$2; W=$3; O=$4; shift 4
PY=${PY:-/root/venv-bd1/bin/python}
mkdir -p "$R"
left() { $PY -X utf8 -I -B "$HERE/b_d1.py" budget --records "$R"; }
LEFT=$(left) || { echo "STOP: CPU budget spent or STOP marker present; $S does not run"; exit 5; }
T="$R/$S.$(date -u +%Y%m%dT%H%M%SZ).time"
[ -e "$T" ] && { echo "REFUSED: $T exists"; exit 6; }
export CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2
if [ "$S" = s0 ]; then
  if [ -n "${1:-}" ]; then CMD=(bash "$HERE/run_tests.sh" "$PY" --env "$1"); else CMD=(bash "$HERE/run_tests.sh" "$PY"); fi
  STG=""
else
  case $S in s1|g0|s2) ;; *) echo "REFUSED: unknown stage $S"; exit 6;; esac
  mkdir -p "$O"
  STG="$O/.staging-$S"
  [ -e "$STG" ] && { echo "REFUSED: $STG exists"; exit 6; }
  mkdir "$STG"
  for f in "$O"/*; do [ -f "$f" ] && ln -s "$(cd "$(dirname "$f")" && pwd)/$(basename "$f")" "$STG/"; done
  CMD=("$PY" -X utf8 -I -B "$HERE/b_d1.py" "$S" --work "$W" --out "$STG" "$@")
fi
echo "$S start $(date -u +%FT%TZ) cpu_seconds_left $LEFT"
nice -n 19 /usr/bin/time -v -o "$T" prlimit --cpu="$LEFT" "${CMD[@]}"
rc=$?
echo "$S end $(date -u +%FT%TZ) rc $rc"
if [ $rc -ne 0 ] || ! left >/dev/null; then
  touch "$R/STOP"
  [ -n "$STG" ] && mv "$STG" "$O/.rejected-$S"
  echo "STOP: rc $rc or CPU budget reached; no result is kept; write a judge line before anything else runs"
  exit 5
fi
if [ -n "$STG" ]; then
  find "$STG" -maxdepth 1 -type f -exec mv -n {} "$O"/ \;
  rm -rf "$STG"
fi
echo "$S done; cpu_seconds_left $(left)"
