#!/bin/bash
# Laptop selftest of c_diag_job.sh (CC-299r3 / CC-307 code reads; B's b_pa1_job_selftest.sh form). Runs the job in a throwaway
# git repo under ${TMPDIR:-/tmp} with a fake nvidia-smi and a stub venv python: the GPU commands (hostcheck, gate,
# run) and the CPU selftest are faked; cap, left, next, project and wipe are the real stdlib code of c_diag_gpu.py.
# Each scenario gets a fresh HOME. Uses the laptop's /dev/shm/c_diag_hd for a tiny synthetic push (the job's trap
# wipes it). Deletes no directory tree; the sandbox is left under $TMPDIR (named at the end). No network.
#     bash scripts/c_diag/c_diag_job_selftest.sh [JOB_SH]      default: c_diag_job.sh beside this file; rc 0 = pass
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
JOB=${1:-$HERE/c_diag_job.sh}
HD=/dev/shm/c_diag_hd
[ ! -e $HD ] || { echo "REFUSED: $HD exists"; exit 2; }
SB=$(mktemp -d "${TMPDIR:-/tmp}/c_diag_jobst.XXXX"); mkdir -p $SB/bin
REPO=$SB/repo; mkdir -p $REPO/scripts/c_diag $REPO/scripts/c_pvr_gpu
for f in c_diag.py c_diag_gpu.py; do cp -L $HERE/$f $REPO/scripts/c_diag/; done
cp -L "$JOB" $REPO/scripts/c_diag/c_diag_job.sh
cp -L $HERE/../c_pvr_gpu/c_pvr_gpu.py $REPO/scripts/c_pvr_gpu/
(cd $REPO/scripts/c_diag && sha256sum c_diag.py c_diag_gpu.py c_diag_job.sh > SHA256SUMS)
(cd $REPO && git init -q && git add -A && git -c user.email=st@local -c user.name=st commit -qm st)
H=$(git -C $REPO rev-parse HEAD)
printf '#!/bin/bash\necho "NVIDIA GeForce RTX 3090"\n' > $SB/bin/nvidia-smi
cat > $SB/bin/date <<'EOF'
#!/bin/bash
# fake `date +%s` for the verdict-wait scenario only (STUB_JUMP): each call moves 4,000 s on
if [ "${1:-}" = +%s ] && [ -n "${STUB_JUMP:-}" ]; then n=$(cat $HOME/date.n 2>/dev/null || echo 0); echo $((n + 1)) > $HOME/date.n
  echo $(( $(/usr/bin/date +%s) + n * 4000 )); exit 0; fi
exec /usr/bin/date "$@"
EOF
chmod +x $SB/bin/nvidia-smi $SB/bin/date; export PATH=$SB/bin:$PATH
STUB='#!/bin/bash
# CC-307 W1: every call must carry -X utf8. The real interpreter runs under LC_ALL=C; a call without the flag is
# logged (the scenario then fails) and runs with -X utf8=0, as on an ASCII-default host.
U=(); if [ "${1:-}" = -X ] && [ "${2:-}" = utf8 ]; then shift 2; else echo "no -X utf8: $*" >> $HOME/noutf8.log; U=(-X utf8=0); fi
set -- -X utf8 "$@"; [ ${#U[@]} = 0 ] || set -- "${U[@]}" "${@:3}"
if [ "$3" = -m ] && [ "$4" = pip ]; then echo "stub==1"; exit 0; fi
CMD=; prev=
for a in "$@"; do case "$prev" in *c_diag_gpu.py) case "$a" in hostcheck|gate|run) CMD=$a;; esac;; esac
  case "$a" in *test_c_diag.py) CMD=test_c_diag.py;; esac; prev=$a; done
O=$HOME/c_diag_out
case "${CMD:-}" in
  test_c_diag.py) exit 0;;
  hostcheck) for x in "$@"; do case $x in qwen*|intern*) M=$x;; esac; done; echo "{}" > $O/HOSTCHECK_$M.json; exit 0;;
  gate|run) for x in "$@"; do case $x in qwen*|intern*) [ -n "${M:-}" ] || M=$x;; esac; done
     echo "$CMD.$M" >> $HOME/stub.log
     n=$(( $(cat $HOME/crash.n 2>/dev/null || echo 0) + 1 )); echo $n > $HOME/crash.n
     [ -z "${STUB_CRASH:-}" ] || [ $n -gt $STUB_CRASH ] || exit 1
     [ "${STUB_MONEY:-}" != "$CMD.$M" ] || echo "{}" > $O/MONEY_STOP.json
     [ "${STUB_EXPIRE:-}" != "$CMD.$M" ] || /usr/bin/python3 -I -c "import json, sys; p = sys.argv[1]; c = json.load(open(p))
c[\"rent_epoch\"] -= 30 * 3600; open(p, \"w\").write(json.dumps(c))" $O/CAP.json   # the cap runs out after this step
     if [ $CMD = gate ]; then echo "{\"u\": 0}" > $O/out/gate.$M.jsonl
     else for w in /dev/shm/c_diag_hd/work.$M.*.json; do ds=${w##*/work.$M.}; ds=${ds%.json}
       for p in verify texts; do echo x > $O/logs/done.$p.$M.$ds; done
       for a in rand ret filt ctl; do echo x > $O/logs/done.decode.$M.$ds.$a; done; done; fi
     V=STUB_RC_${CMD}_${M}; exit ${!V:-0};;
esac
exec env LC_ALL=C /usr/bin/python3 "$@"'
FAIL=0
pass() { if [ -e $HOME/noutf8.log ]; then bad "$1 (an interpreter call without -X utf8)"; else echo "ok   $1"; fi; }
bad() { echo "FAIL $1"; FAIL=1; }
newhome() {  # BRANCH: a fresh HOME, venv stub, CAP.json (real `cap`), HOSTCHECKs, the synthetic push
  export HOME=$(mktemp -d $SB/home.XXXX); O=$HOME/c_diag_out; mkdir -p $O/out $O/logs $HOME/venvs/c_diag/bin
  echo "$STUB" > $HOME/venvs/c_diag/bin/python; chmod +x $HOME/venvs/c_diag/bin/python
  FZ=$(echo "stub==1" | sha256sum | cut -c1-64)
  (cd $REPO && /usr/bin/python3 -I -B scripts/c_diag/c_diag_gpu.py cap --out $O --branch $1 --rate 10092 \
     --rent-utc "$(/usr/bin/date -u +%FT%TZ)" --freeze $FZ > /dev/null) || { echo "REFUSED: cap"; exit 2; }
  for m in qwen25vl_7b internvl3_8b; do echo "{}" > $O/HOSTCHECK_$m.json; done
  mkdir -m 700 $HD; mkdir -p $HD/img/xm_dev500; printf 'a' > $HD/img/xm_dev500/a.jpg; echo '[]' > $HD/gate_units.json
  if [ $1 = main ]; then printf '%s' '{"backbone": "qwen25vl_7b", "set": "xm_test2500", "items": [["i", "i.jpg", "0"]], "ret": {"i": ["c"]}, "dc": {"c": {"props": []}}, "order": "first"}' > $HD/work.qwen25vl_7b.xm_test2500.json; fi
  (cd $HD && find . -type f ! -name MANIFEST.sha256 | sed 's|^\./||' | LC_ALL=C sort | xargs sha256sum > MANIFEST.sha256)
  TMAN=$(sha256sum < $HD/MANIFEST.sha256 | cut -c1-64)
}
runjob() { (cd $REPO && timeout 120 bash scripts/c_diag/c_diag_job.sh "$@" > $HOME/job.out 2>&1); echo $?; }
gone() { [ ! -e $HD ] && [ "$(wc -l < $O/c_diag_hd_deletions.log)" = 1 ]; }
sums_ok() { (cd $O && [ -s $1 ] && sha256sum --quiet -c $1) && grep -q "  logs/job.log$" $O/$1 \
  && [ "$(tail -n 1 $O/logs/job.log | cut -d' ' -f2)" = EXIT ]; }   # CC-297 N-4: the EXIT line is inside the hash

# 1 gate-only: S1 for both verifiers, SUMS last, tmpfs wiped and logged
newhome gate-only; rc=$(runjob gate-only $H $TMAN)
[ $rc = 0 ] && grep -q "JOB DONE gate-only" $O/logs/job.log && sums_ok SHA256SUMS_gate-only && gone \
  && [ "$(cat $HOME/stub.log | tr '\n' ' ')" = "gate.qwen25vl_7b gate.internvl3_8b " ] && pass "gate-only" || bad "gate-only (rc $rc)"
# 2 gate-only push may hold only gate material (R2-W1 (c))
newhome gate-only; echo '{}' > $HD/work.qwen25vl_7b.xm_test2500.json
(cd $HD && find . -type f ! -name MANIFEST.sha256 | sed 's|^\./||' | LC_ALL=C sort | xargs sha256sum > MANIFEST.sha256)
rc=$(runjob gate-only $H $(sha256sum < $HD/MANIFEST.sha256 | cut -c1-64))
[ $rc = 1 ] && grep -q "gate-only push holds more" $O/logs/job.log && gone && pass "gate-only push check" || bad "gate-only push check"
# 3 main: gate, SUMS_gate without logs, verdict, run, SUMS_main last
newhome main; printf '{"pass": ["qwen25vl_7b"], "verdict_sha256": "%064d"}\n' 0 > $O/VERDICT.json
rc=$(runjob main $H $TMAN)
[ $rc = 0 ] && sums_ok SHA256SUMS_main && [ -s $O/SHA256SUMS_gate ] && ! grep -q "logs/job.log" $O/SHA256SUMS_gate \
  && grep -q "run.qwen25vl_7b" $HOME/stub.log && ! grep -q "run.internvl3_8b" $HOME/stub.log && gone \
  && pass "main" || bad "main (rc $rc)"
# 4 main with no verifier passing: the host is deleted after the gate
newhome main; printf '{"pass": [], "verdict_sha256": "%064d"}\n' 0 > $O/VERDICT.json
rc=$(runjob main $H $TMAN)
[ $rc = 0 ] && grep -q "both verifiers failed" $O/logs/job.log && ! grep -q "^run" $HOME/stub.log && sums_ok SHA256SUMS_main \
  && pass "both fail" || bad "both fail"
# 5 malformed VERDICT.json
newhome main; echo '{"pass": ["gpt"]}' > $O/VERDICT.json; rc=$(runjob main $H $TMAN)
[ $rc = 1 ] && grep -q "VERDICT.json is not" $O/logs/job.log && pass "verdict format" || bad "verdict format"
# 6 verdict wait over 1.0 h: IDLE STOP (final), SUMS _stop
newhome main; rc=$( (export STUB_JUMP=1; runjob main $H $TMAN) )
[ $rc = 0 ] && [ -s $O/IDLE_STOP.json ] && sums_ok SHA256SUMS_main_stop && pass "verdict wait 1.0 h" || bad "verdict wait (rc $rc)"
# 6b the cap runs out while waiting for the verdict: CAP STOP (final), not an idle wait (CC-307 N3)
newhome main; rc=$( (export STUB_EXPIRE=gate.internvl3_8b; runjob main $H $TMAN) )
[ $rc = 0 ] && grep -q "CAP STOP cap reached during the verdict wait" $O/logs/job.log && [ -s $O/CAP_STOP.json ] \
  && sums_ok SHA256SUMS_main_stop && pass "cap stop in the verdict wait" || bad "cap stop in the verdict wait (rc $rc)"
# 7 cap stop (rc 124) is final; a re-run refuses
newhome gate-only; rc=$( (export STUB_RC_gate_qwen25vl_7b=124; runjob gate-only $H $TMAN) )
[ $rc = 0 ] && [ -s $O/CAP_STOP.json ] && sums_ok SHA256SUMS_gate-only_stop && gone && pass "cap stop" || bad "cap stop (rc $rc)"
mkdir -m 700 $HD; cp /dev/null $HD/x; (cd $HD && sha256sum x > MANIFEST.sha256)
rc=$(runjob gate-only $H x); [ $rc = 1 ] && grep -q "CAP_STOP.json exists: final" $O/logs/job.log && pass "cap stop final" || bad "cap stop final"
rm -f $HD/x $HD/MANIFEST.sha256; rmdir $HD 2>/dev/null
# 8 FAULT (rc 9) is a JOB STOP, no retry, no SUMS
newhome gate-only; rc=$( (export STUB_RC_gate_qwen25vl_7b=9; runjob gate-only $H $TMAN) )
[ $rc = 1 ] && grep -q "FAULT (rc 9" $O/logs/job.log && [ "$(wc -l < $HOME/stub.log)" = 1 ] && ! ls $O/SHA256SUMS_* >/dev/null 2>&1 \
  && gone && pass "FAULT stop" || bad "FAULT stop (rc $rc)"
# 9 a crash is retried, 3 attempts per step (§8.4)
newhome gate-only; rc=$( (export STUB_CRASH=2; runjob gate-only $H $TMAN) )
[ $rc = 0 ] && [ "$(grep -c CRASH $O/logs/job.log)" = 2 ] && pass "crash retried" || bad "crash retried (rc $rc)"
newhome gate-only; rc=$( (export STUB_CRASH=3; runjob gate-only $H $TMAN) )
[ $rc = 1 ] && grep -q "crashed 3 times" $O/logs/job.log && pass "3 attempts" || bad "3 attempts (rc $rc)"
# 10 a money stop written during a step stops before the next one (final)
newhome gate-only; rc=$( (export STUB_MONEY=gate.qwen25vl_7b; runjob gate-only $H $TMAN) )
[ $rc = 0 ] && grep -q "MONEY_STOP (final) before gate.internvl3_8b" $O/logs/job.log && sums_ok SHA256SUMS_gate-only_stop \
  && pass "money stop" || bad "money stop (rc $rc)"
# 11 preflight: TMAN, freeze, data/ in the repo copy, branch vs mode
newhome gate-only; rc=$(runjob gate-only $(printf '%040d' 0) $TMAN)
[ $rc = 1 ] && grep -q "HEAD is not" $O/logs/job.log && pass "HEAD" || bad "HEAD"
newhome gate-only; rc=$(runjob gate-only $H $(printf '%064d' 1))
[ $rc = 1 ] && grep -q "differs from TMAN" $O/logs/job.log && pass "TMAN" || bad "TMAN"
newhome gate-only; echo "stub==2" > /dev/null; sed -i 's/stub==1/stub==2/' $HOME/venvs/c_diag/bin/python; rc=$(runjob gate-only $H $TMAN)
[ $rc = 1 ] && grep -q "venv freeze differs" $O/logs/job.log && pass "freeze" || bad "freeze"
newhome main; rc=$(runjob gate-only $H $TMAN)
[ $rc = 1 ] && grep -q "not gate-only" $O/logs/job.log && pass "branch vs mode" || bad "branch vs mode"
newhome gate-only; mkdir $REPO/data; rc=$(runjob gate-only $H $TMAN); rmdir $REPO/data
[ $rc = 1 ] && grep -q "holds data/" $O/logs/job.log && pass "no data/ on the host" || bad "no data/"
[ ! -e $HD ] || { rm -f $HD/img/xm_dev500/a.jpg $HD/gate_units.json $HD/MANIFEST.sha256 $HD/work.*.json; rmdir $HD/img/xm_dev500 $HD/img $HD; }
echo "sandbox: $SB"
[ $FAIL = 0 ] && echo "job selftest ok" || echo "job selftest FAILED"
exit $FAIL
