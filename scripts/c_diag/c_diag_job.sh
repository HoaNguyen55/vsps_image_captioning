#!/bin/bash
# C-DIAG HD-1 job (prereg C_DIAG_PREREG_DRAFT_v1_2.md afbb61fb §8-§9, Appendix C; CC-299r3). One tmux session, started by
# the coordinator after `c_diag_gpu.py cap` wrote ~/c_diag_out/CAP.json at the rental:
#   bash scripts/c_diag/c_diag_job.sh MODE <expected 40-hex HEAD> <TMAN: sha256 of /dev/shm/c_diag_hd/MANIFEST.sha256>
# MODE selftest   host-safe selftest, then hostcheck of both backbones (VRAM peak, §7 N16); TMAN of the pushed tmpfs
#      gate-only  S1 for both verifiers, then exit (R2-W1: the host is deleted right after the gate pull)
#      main       S1 -> SHA256SUMS_gate (log excluded) -> wait for ~/c_diag_out/VERDICT.json (relayed by the coordinator
#                 from `c_diag_score.py gate`) at most 1.0 h (§4.3 N2) -> S2/S3 per passing backbone in §5.2 order
# The manifest sha is an argument (CC-298 J3-N3). The cap is billed hours from the rental stamp in CAP.json (20 h or
# 3.0 h, and (210,000 - 30) / r, §8.3); each step runs under `timeout` with the time left minus 0.5 h for pull and
# delete. Cuts are made by the projection (c_diag_gpu.py project, at each step start and after 100 queries) and are
# sticky (CUTS.json). Final stops: a cap stop (rc 124, or rc 137 at or after LEFT) and a money stop (MONEY_STOP.json,
# written by the coordinator, who then kills this job by ~/c_diag_out/job.pid). A FAULT (rc 9) is a JOB STOP; a crash
# is retried up to 3 attempts per step (§8.4). Never rents, tops up or deletes a machine.
# SHA256SUMS_<mode> is written by the EXIT trap AFTER the "JOB DONE" and "EXIT" lines (CC-297 N-4), so logs/job.log
# verifies at the pull; teardown ignores TERM / HUP / INT / PIPE (B's CC-295r3 W9 form).
# Pixels and demonstration text only in /dev/shm/c_diag_hd (0700, Appendix C 3); the trap deletes it on ANY exit and
# appends (utc, folder, files, manifest count) to ~/c_diag_out/c_diag_hd_deletions.log (Appendix C 6). Logs: ids,
# counts and return codes only. Every interpreter call runs with `-X utf8` (CC-307 W1; B's CC-304 form): an ASCII
# default locale on the host must not change how any file is read.
set -euo pipefail
MODE=${1:?usage: c_diag_job.sh selftest|gate-only|main HEAD TMAN}; EXPECT=${2:?HEAD}; TMAN=${3:?TMAN}
cd "$(dirname "$0")/../.."
X=scripts/c_diag/c_diag_gpu.py
PY=$HOME/venvs/c_diag/bin/python   # the CC-212 decode venv (B-N1 packages), freeze in CAP.json
O=$HOME/c_diag_out; LOG=$O/logs; HD=/dev/shm/c_diag_hd; SNAP=$HOME/c_diag_models
WAIT_S=3600   # §4.3 [N2] verdict wait bound (main branch)
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HOME=$SNAP/hf
case "$MODE" in selftest|gate-only|main) ;; *) echo "unknown mode $MODE"; exit 2;; esac
mkdir -p $LOG $O/out
ts() { date -u +%FT%TZ; }
mono() { local u; read -r u _ < /proc/uptime; echo ${u%.*}; }
say() { local l; l="$(ts) $*"; echo "$l" >> $LOG/job.log; echo "$l" 2>/dev/null || true; }
stop() { say "JOB STOP $*"; exit 1; }
exec 9> $O/.job.lock
flock -n 9 || { echo "REFUSED: another c_diag job is running"; exit 1; }
echo $$ > $O/job.pid
FINAL="CAP_STOP.json MONEY_STOP.json"
SPID=; MANIFEST=
sums() { (cd $O && find out logs -type f | LC_ALL=C sort | xargs -r sha256sum); }
teardown() {
  local rc=$?; trap '' TERM HUP INT PIPE
  if [ -d $HD ]; then $PY -X utf8 -I -B $X wipe --dir $HD --log $O/c_diag_hd_deletions.log || say "WIPE COUNT MISMATCH"; fi
  if [ $rc = 143 ] && [ -e $O/MONEY_STOP.json ]; then MANIFEST=SHA256SUMS_${MODE}_stop; say "MONEY STOP (final) on signal"; fi
  say "EXIT $MODE rc=$rc"
  [ -z "$MANIFEST" ] || sums > $O/$MANIFEST   # last: every line above is in job.log before it is hashed (CC-297 N-4)
}
on_signal() {
  if [ -n "$SPID" ]; then kill -TERM -- -$SPID 2>/dev/null || kill -TERM $SPID 2>/dev/null || true; wait $SPID 2>/dev/null || true; fi
  exit 143
}
trap teardown EXIT
trap on_signal TERM HUP INT
final() { printf '{"%s": "%s", "utc": "%s"}\n' "$1" "$2" "$(ts)" > $O/$3; MANIFEST=SHA256SUMS_${MODE}_stop; say "$4 $2 (final)"; exit 0; }

# ---------------------------------------------------------------------------------------------- preflight
for m in $FINAL; do [ ! -e $O/$m ] || stop "$m exists: final"; done
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
[ ! -e data ] || stop "the repo copy holds data/ (labels never on the host, Appendix C 4): use the sparse copy"
(cd scripts/c_diag && sha256sum --quiet -c SHA256SUMS) || stop "scripts/c_diag/SHA256SUMS"
nvidia-smi --query-gpu=name --format=csv,noheader | grep -Eq '^NVIDIA GeForce RTX 3090( Ti)?$' || stop "GPU is not one 3090"
[ -s $O/CAP.json ] || stop "no CAP.json (c_diag_gpu.py cap at the rental)"
BR=$($PY -X utf8 -I -c 'import json,sys; print(json.load(open(sys.argv[1]))["branch"])' $O/CAP.json)
FZ=$($PY -X utf8 -I -c 'import json,sys; print(json.load(open(sys.argv[1]))["freeze_sha256"])' $O/CAP.json)
case "$MODE" in gate-only) [ "$BR" = gate-only ] || stop "CAP.json branch $BR, not gate-only";;
                main) [ "$BR" = main ] || stop "CAP.json branch $BR, not main";; esac
export C_DIAG_FREEZE=$($PY -X utf8 -m pip freeze | sha256sum | cut -c1-64)
[ "$C_DIAG_FREEZE" = "$FZ" ] || stop "venv freeze differs from the CC-212 record in CAP.json (§7)"
export C_DIAG_CODE=$(sha256sum scripts/c_diag/SHA256SUMS | cut -c1-64)
[ "$(stat -c %a $HD)" = 700 ] || stop "$HD is not mode 0700"
[ "$(sha256sum < $HD/MANIFEST.sha256 | cut -c1-64)" = "$TMAN" ] || stop "tmpfs MANIFEST.sha256 differs from TMAN (NB-C3)"
(cd $HD && sha256sum --quiet -c MANIFEST.sha256) || stop "a tmpfs file differs from its arrival sha (FAULT)"
[ "$(cd $HD && find . ! -type d | sed 's|^\./||' | LC_ALL=C sort)" = "$( (echo MANIFEST.sha256; cut -c67- $HD/MANIFEST.sha256) | LC_ALL=C sort)" ] \
  || stop "tmpfs file set differs from MANIFEST.sha256"
if [ "$MODE" = gate-only ]; then   # R2-W1 (c): gate images and the gate unit file only
  [ -z "$(cut -c67- $HD/MANIFEST.sha256 | grep -v -e '^gate_units\.json$' -e '^img/xm_dev500/')" ] \
    || stop "gate-only push holds more than the gate images and the gate unit file"
fi
$PY -X utf8 -I -B scripts/c_diag/test_c_diag.py host >> $LOG/selftest.log 2>&1 || stop "host selftest"
sha256sum $X $0 scripts/c_diag/c_diag.py > $O/code_at_start_$MODE.sha256

step() {  # step NAME CMD...: up to 3 attempts for a crash (rc 1); FAULT (9) stops; timeout = cap stop (final)
  local name=$1; shift; local n rc LEFT T0S EL
  for n in 1 2 3; do
    for m in $FINAL; do [ ! -e $O/$m ] || { MANIFEST=SHA256SUMS_${MODE}_stop; say "${m%.json} (final) before $name"; exit 0; }; done
    LEFT=$($PY -X utf8 -I -B $X left --out $O); [ "$LEFT" -gt 0 ] || final cap_stop "cap reached before $name" CAP_STOP.json "CAP STOP"
    say "START $name attempt $n (left $(( LEFT / 60 )) min)"
    T0S=$(mono); rc=0
    timeout --kill-after=60 ${LEFT}s "$@" < /dev/null >> $LOG/steps.log 2>&1 &
    SPID=$!; wait $SPID || rc=$?; SPID=
    EL=$(( $(mono) - T0S ))
    case $rc in
      0) say "OK $name"; return 0;;
      124) final cap_stop "during $name" CAP_STOP.json "CAP STOP";;
      137) [ $EL -lt $LEFT ] || final cap_stop "during $name (KILL after its timeout)" CAP_STOP.json "CAP STOP"
           stop "$name rc=137 after ${EL}s < LEFT ${LEFT}s: OOM or an outside KILL";;
      9) stop "$name FAULT (rc 9; one OPS line, one-judge read, re-run after FAULT)";;
      *) say "CRASH $name rc=$rc (attempt $n)";;
    esac
  done
  stop "$name crashed 3 times (§8.4)"
}

if [ "$MODE" = selftest ]; then
  for M in qwen25vl_7b internvl3_8b; do
    step hostcheck.$M $PY -X utf8 -I -B $X hostcheck --model $M --snapshot $SNAP/$M --hd $HD --out $O
  done
  MANIFEST=SHA256SUMS_selftest; say "HOSTCHECK OK"; say "JOB DONE $MODE"; exit 0
fi
for M in qwen25vl_7b internvl3_8b; do [ -s $O/HOSTCHECK_$M.json ] || stop "no HOSTCHECK_$M.json (mode selftest first)"; done

# ---------------------------------------------------------------------------------------------- S1 gate (both verifiers)
while ST=$($PY -X utf8 -I -B $X next --out $O --hd $HD --mode gate) && [ -n "$ST" ]; do
  M=${ST#gate.}
  [ "$MODE" = gate-only ] || $PY -X utf8 -I -B $X project --out $O --hd $HD --models qwen25vl_7b internvl3_8b >> $LOG/project.log
  step $ST $PY -X utf8 -I -B $X gate --model $M --snapshot $SNAP/$M --hd $HD --out $O
  ts > $LOG/done.$ST
done
date +%s > $LOG/gate_done.epoch
[ "$MODE" = gate-only ] || $PY -X utf8 -I -B $X project --out $O --hd $HD --models qwen25vl_7b internvl3_8b >> $LOG/project.log  # §8.3 first run
if [ "$MODE" = gate-only ]; then
  MANIFEST=SHA256SUMS_gate-only; say "JOB DONE $MODE (pull, then delete the host before the verdict, R2-W1 (d))"; exit 0
fi
(cd $O && find out logs -type f ! -name job.log ! -name steps.log ! -name project.log | LC_ALL=C sort | xargs -r sha256sum) > $O/SHA256SUMS_gate
say "GATE DONE: pull SHA256SUMS_gate (logs excluded) and relay the verdict as VERDICT.json within 1.0 h"

# ---------------------------------------------------------------------------------------------- verdict wait (§4.3 N2)
T0=$(cat $LOG/gate_done.epoch)
until [ -s $O/VERDICT.json ]; do
  [ $(( $(date +%s) - T0 )) -lt $WAIT_S ] || final idle_stop "no verdict within 1.0 h of the gate (pull and delete, §4.3)" IDLE_STOP.json "IDLE STOP"
  [ "$($PY -X utf8 -I -B $X left --out $O)" -gt 0 ] || final cap_stop "cap reached during the verdict wait" CAP_STOP.json "CAP STOP"
  sleep 20
done
PASS=$($PY -X utf8 -I -c 'import json,sys
d = json.load(open(sys.argv[1])); p = d["pass"]
ok = isinstance(p, list) and set(p) <= {"qwen25vl_7b", "internvl3_8b"} and len(d.get("verdict_sha256", "")) == 64
print(" ".join(p) if ok else "BAD")' $O/VERDICT.json)
[ "$PASS" != BAD ] || stop "VERDICT.json is not {pass: [models], verdict_sha256}"
cp $O/VERDICT.json $LOG/verdict.json
say "VERDICT pass: ${PASS:-none}"
[ -n "$PASS" ] || { MANIFEST=SHA256SUMS_main; say "JOB DONE $MODE (both verifiers failed the gate: delete the host)"; exit 0; }

# ---------------------------------------------------------------------------------------------- S2/S3
while ST=$($PY -X utf8 -I -B $X next --out $O --hd $HD --mode main --models $PASS) && [ -n "$ST" ]; do
  $PY -X utf8 -I -B $X project --out $O --hd $HD --models $PASS >> $LOG/project.log
  ST=$($PY -X utf8 -I -B $X next --out $O --hd $HD --mode main --models $PASS); [ -n "$ST" ] || break
  M=${ST#run.}
  step $ST $PY -X utf8 -I -B $X run --model $M --models $PASS --snapshot $SNAP/$M --hd $HD --out $O
done
MANIFEST=SHA256SUMS_main
say "JOB DONE $MODE"
