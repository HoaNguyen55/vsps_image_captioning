#!/usr/bin/env bash
# One B-ALT (FE-LOCUS) stage under its own 8 CPU-h hard stop (prereg v2 §5; CC-510 ruling 6), child processes included.
#   scripts/b_alt/run_stage.sh s0  RECORDS - - [WHEEL_DIR]       the S0 checks (run_tests.sh, with --env if given)
#   scripts/b_alt/run_stage.sh s1a RECORDS WORK OUT --pyvi-wheel P --uts-wheel U
#   scripts/b_alt/run_stage.sh s1b RECORDS WORK OUT --baselines B --pyvi-wheel P --uts-wheel U --census-sha C
#   scripts/b_alt/run_stage.sh g0  RECORDS WORK OUT --npz-sha N
#   scripts/b_alt/run_stage.sh s2  RECORDS WORK OUT --census-sha C --npz-sha N --g0-sha G
# Budget: scripts/b_d1/b_d1.py budget (reused unchanged) on THIS study's RECORDS dir: 28,800 s minus user+sys of every
# *.time record there; refuse at 0 or when RECORDS/STOP exists. RECORDS must not be D1's records dir.
# During the stage: GNU `time -v` (record RECORDS/<stage>.<utc>.time; counts the guard and every waited descendant),
# `prlimit --cpu=<left>` (per process) and cpu_guard.py <left> (the whole process tree: kills the group at the limit).
# Outputs go to OUT/.staging-<stage>; on rc != 0 (guard kill 7, SIGXCPU, FAULT 3 included) or no seconds left: write
# RECORDS/STOP, keep the staging dir as .rejected-<stage>, move nothing. PY defaults to $BALT_BASE/venv-bd1/bin/python
# (BALT_BASE defaults to /root). prlimit --cpu=<left> (<= 28,800) is the per-process backstop of erratum H4.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
S=$1; R=$2; W=$3; O=$4; shift 4
PY=${PY:-${BALT_BASE:-/root}/venv-bd1/bin/python}
case $R in *b_d1_records*) echo "REFUSED: RECORDS is the D1 records dir; FE-LOCUS has its own 8 CPU-h"; exit 6;; esac
mkdir -p "$R"
left() { $PY -X utf8 -I -B "$ROOT/scripts/b_d1/b_d1.py" budget --records "$R"; }
LEFT=$(left) || { echo "STOP: CPU budget spent or STOP marker present; $S does not run"; exit 5; }
T="$R/$S.$(date -u +%Y%m%dT%H%M%SZ).time"
[ -e "$T" ] && { echo "REFUSED: $T exists"; exit 6; }
export CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2
if [ "$S" = s0 ]; then
  if [ -n "${1:-}" ]; then CMD=(bash "$HERE/run_tests.sh" "$PY" --env "$1"); else CMD=(bash "$HERE/run_tests.sh" "$PY"); fi
  STG=""
else
  case $S in s1a|s1b|g0|s2) ;; *) echo "REFUSED: unknown stage $S"; exit 6;; esac
  mkdir -p "$O"
  STG="$O/.staging-$S"
  [ -e "$STG" ] && { echo "REFUSED: $STG exists"; exit 6; }
  mkdir "$STG"
  for f in "$O"/*; do [ -f "$f" ] && ln -s "$(cd "$(dirname "$f")" && pwd)/$(basename "$f")" "$STG/"; done
  CMD=("$PY" -X utf8 -I -B "$HERE/b_alt.py" "$S" --work "$W" --out "$STG" "$@")
fi
echo "$S start $(date -u +%FT%TZ) cpu_seconds_left $LEFT"
nice -n 19 /usr/bin/time -v -o "$T" prlimit --cpu="$LEFT" "$PY" -I -B "$HERE/cpu_guard.py" "$LEFT" -- "${CMD[@]}"
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
