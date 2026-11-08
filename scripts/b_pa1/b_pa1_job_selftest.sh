#!/bin/bash
# Laptop selftest of b_pa1_job.sh (DRAFT, not read). Runs the job in a throwaway git repo under /tmp with a fake
# nvidia-smi and stub venv pythons: the GPU commands (run, hostcheck, inputs, selftest, feats) are faked, every other
# command (steps, left, ledger, cap-init, resume, wipe) is the real stdlib code of b_pa1_gpu.py. Each scenario gets a
# fresh HOME. Uses the laptop's /dev/shm/b_pa1_hb for a 1-file synthetic set (the job's trap wipes it). Deletes no
# directory tree: each run leaves its small sandbox under /tmp/bpa1_jobst.* (named at the end). No network.
#     bash scripts/b_pa1/b_pa1_job_selftest.sh [JOB_SH]      default: the b_pa1_job.sh beside this file; rc 0 = pass
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); R=$(cd "$(dirname "$(readlink -f "$0")")/../.." && pwd)
JOB=${1:-$HERE/b_pa1_job.sh}
HB=/dev/shm/b_pa1_hb
[ ! -e $HB ] || { echo "REFUSED: $HB exists"; exit 2; }
SB=$(mktemp -d /tmp/bpa1_jobst.XXXX); mkdir -p $SB/bin $SB/fake
REPO=$SB/repo; B=$REPO/scripts/b_pa1; mkdir -p $B $REPO/scripts/w25 $REPO/scripts/grl
LIST=$(cut -c67- $HERE/SHA256SUMS_GPU)
[ -n "$LIST" ] || { echo "REFUSED: empty SHA256SUMS_GPU"; exit 2; }
for f in $LIST $(cut -c67- $HERE/SHA256SUMS) SHA256SUMS; do cp -L $HERE/$f $B/; done
cp -L "$JOB" $B/b_pa1_job.sh
SUMS=$(cd $B && sha256sum $LIST) && echo "$SUMS" > $B/SHA256SUMS_GPU   # the job under test may be a mutant
[ "$(wc -l < $B/SHA256SUMS_GPU)" = "$(echo "$LIST" | wc -l)" ] || { echo "REFUSED: sandbox SUMS"; exit 2; }
cp $R/scripts/w25/w25.py $REPO/scripts/w25/; cp $R/scripts/grl/common.py $R/scripts/grl/id_counts.py $REPO/scripts/grl/
(cd $REPO && git init -q && git add -A && git -c user.email=st@local -c user.name=st commit -qm st)
(cd $REPO && sha256sum scripts/w25/w25.py scripts/grl/common.py > host_w25.sums)   # untracked, as run doc §1.4
H=$(git -C $REPO rev-parse HEAD)
UUID=GPU-0a1b2c3d-0000-1111-2222-333344445555
cat > $SB/bin/nvidia-smi <<EOF
#!/bin/bash
case "\$*" in *uuid*) echo "$UUID";; *) echo "NVIDIA GeForce RTX 3090";; esac
EOF
cat > $SB/fake/timeout <<'EOF'
#!/bin/bash
# fake GNU timeout for the rc-137 cases only: drop the options and the duration, run the command, pass its rc
while [[ $1 == --* ]]; do shift; done; shift; "$@"
EOF
chmod +x $SB/bin/nvidia-smi $SB/fake/timeout; export PATH=$SB/bin:$PATH
LKM=$(sha256sum $B/requirements_b_pa1_main.lock | cut -c1-8); LKL=$(sha256sum $B/requirements_b_pa1_legacy.lock | cut -c1-8)
FZ=$(echo "stub==1" | sha256sum | cut -c1-64); CODE=$(sha256sum $B/SHA256SUMS_GPU | cut -c1-64)
STUB='#!/bin/bash
if [ "$1" = -m ] && [ "$2" = pip ]; then if [[ $0 == */b_pa1_w/* ]]; then cat '$B'/requirements_b_pa1_w.txt; else echo "stub==1"; fi; exit 0; fi
for a in "$@"; do case "$a" in run|hostcheck|inputs|selftest|feats) CMD=$a; break;; esac; done
case "${CMD:-}" in
  run|feats) [ $CMD = run ] && ST=$5 || ST=w.feats; echo "$ST" >> $HOME/stub.log
     [ "${STUB_MONEY:-}" != "$ST" ] || echo "{}" > $HOME/b_pa1_out/MONEY_STOP.json
     [ -z "${STUB_READ:-}" ] || cat > /dev/null   # a step that reads stdin
     [ -z "${STUB_SLEEP:-}" ] || { echo $$ > $HOME/stub.pid; exec sleep $STUB_SLEEP; }
     [ -z "${STUB_SLOWTERM:-}" ] || {   # N-b: a step that needs 2 s to end on TERM; its exit time on CLOCK_MONOTONIC
       trap "sleep 2; /usr/bin/python3 -I -c \"import time; print(time.monotonic())\" > \$HOME/stub.exit; exit 0" TERM
       sleep 60 & wait $!; exit 0; }
     [ -z "${STUB_LATE137:-}" ] || { sleep $STUB_LATE137; exit 137; }
     V=STUB_RC_${ST//./_}; exit ${!V:-0};;
  hostcheck|inputs|selftest) exit 0;;
esac
if [ -n "${STUB_SLOWWIPE:-}" ] && [[ " $* " == *" wipe "* ]]; then touch $HOME/wipe.started; sleep 2; fi   # W9 (e)
exec /usr/bin/python3 "$@"'
newhome() {  # [done modes...]: a fresh HOME with venv stubs, first-build freezes, a fresh hostcheck, CAP.json
  export HOME=$(mktemp -d $SB/home.XXXX); O=$HOME/b_pa1_out; mkdir -p $O/in $O/out/s
  for v in main_$LKM legacy_$LKL w; do mkdir -p $HOME/venvs/b_pa1_$v/bin; echo "$STUB" > $HOME/venvs/b_pa1_$v/bin/python
    chmod +x $HOME/venvs/b_pa1_$v/bin/python; done
  echo $FZ > $O/freeze_main.sha256; echo $FZ > $O/freeze_legacy.sha256; hc $UUID
  ln -s $R/.session_backup/2026-11-02/b_pa1/o365_train_frame.tsv $O/in/o365_train_frame.tsv
  echo '{"accepted": ["internvl2_5_2b", "mblip_mt0_xl", "minicpm_v4", "phi3_5_vision"]}' > $O/out/s/ACCEPT.json
  echo '{"kept": ["a3", "h"], "core_fits": true}' > $O/out/s/TRIM.json
  B_PA1_OUT=$O /usr/bin/python3 -I -B $B/b_pa1_gpu.py cap-init --cap-h 28 --r-host 10092 --fee 30 \
    --t0 2026-11-10T01:00:00Z --used-sec ${USED:-0} > /dev/null
  for m in "$@"; do date -u > $O/RUN.$m.done; done
  export B_PA1_OUT=$O
}
hc() { for v in main legacy; do printf '{"code": "%s", "freeze": "%s", "gpu_uuid": "%s"}\n' $CODE $FZ "$1" > $O/HOSTCHECK_$v.json; done; }
mkset() { local s=${1:-a}; mkdir -p -m 700 $HB; chmod 700 $HB; mkdir -m 700 $HB/$s; printf x > $HB/$s/f1
  (cd $HB/$s && sha256sum f1 > MANIFEST.sha256); sha256sum < $HB/$s/MANIFEST.sha256 | cut -c1-64; }
M64=$(printf 'b%.0s' {1..64}); H64=$(printf 'c%.0s' {1..64}); FAIL=0; N=0
ok() { N=$((N + 1)); if eval "$2"; then echo "ok   $1"; else echo "FAIL $1"; FAIL=1; fi; }
verifies() { [ -s $O/$1 ] && grep -q ' logs/job.log$' $O/$1 && (cd $O && sha256sum --quiet -c $1); }   # job.log included
after_stub() {  # the ledger end of the last step came after the stub's exit: its sec exceeds (stub exit - start m)
  /usr/bin/python3 -I - $O/ledger.jsonl $HOME/stub.exit <<'PY'
import json, sys
rows = [json.loads(x) for x in open(sys.argv[1])]
st, en = [r for r in rows if r["ev"] == "start"][-1], rows[-1]
sys.exit(not (en["ev"] == "end" and en["step"] == st["step"] and en["sec"] > float(open(sys.argv[2]).read()) - st["m"]))
PY
}
expect() {  # name rc pattern command...
  local name=$1 want=$2 pat=$3 out rc; shift 3
  out=$("$@" 2>&1); rc=$?; LAST=$out
  N=$((N + 1)); if [ "$rc" = "$want" ] && grep -q -- "$pat" <<< "$out"; then echo "ok   $name"; else echo "FAIL $name (rc $rc)"; FAIL=1; fi
}
J="bash $B/b_pa1_job.sh"

# --- A: the main sequence, block S done
newhome s
mv $REPO/host_w25.sums $SB/host_w25.moved
MAN=$(mkset); expect "host_w25.sums required (N5)" 1 "host_w25.sums missing" $J a1decode $H $MAN
mv $SB/host_w25.moved $REPO/host_w25.sums
echo "# tampered" >> $B/b_pa1_registry.json; (cd $REPO && git -c user.email=st@local -c user.name=st commit -qam tamper)
MAN=$(mkset); expect "SUMS_GPU must check" 1 "scripts/b_pa1 SUMS" $J a1decode $(git -C $REPO rev-parse HEAD) $MAN
git -C $REPO reset -q --hard HEAD~1   # the sandbox repo only
echo "# dirty" >> $B/b_pa1_gpu.py
MAN=$(mkset); expect "tracked tree must be clean" 1 "tracked files differ" $J a1decode $H $MAN
git -C $REPO checkout -q -- scripts/b_pa1/b_pa1_gpu.py
hc GPU-ffffffff-0000-1111-2222-333344445555
MAN=$(mkset); expect "stale hostcheck (other GPU)" 1 "stale" $J a1decode $H $MAN
hc $UUID
MAN=$(mkset); expect "a1score before a1decode refused (W3)" 1 "needs RUN.a1decode.done" $J a1score $H $MAN $M64
MAN=$(mkset); expect "a1decode runs" 0 "JOB DONE a1decode" $J a1decode $H $MAN
ok "trap wiped the set" '[ ! -e $HB/a ]'
ok "mode manifest written last: it verifies with job.log (CC-295r2)" 'verifies SHA256SUMS_a1decode && tail -n 1 $O/logs/job.log | grep -q "EXIT a1decode rc=0"'
MAN=$(mkset); expect "a finished mode refuses" 1 "already done" $J a1decode $H $MAN
MAN=$(mkset); expect "a1score needs MAPF" 1 "final map sha" $J a1score $H $MAN -
MAN=$(mkset); expect "a1score runs" 0 "JOB DONE a1score" $J a1score $H $MAN $M64
MAN=$(mkset); expect "rest needs the H sha" 1 "TRIM keeps H" $J rest $H $MAN $M64 -
MAN=$(mkset); STUB_RC_rest_jc=2 expect "guard failure stops" 1 "rest.jc rc=2" $J rest $H $MAN $M64 $H64
MAN=$(mkset); expect "unfinished run needs RESUME.json" 1 "a resume needs RESUME.json" $J rest $H $MAN $M64 $H64
/usr/bin/python3 -I -B $B/b_pa1_gpu.py resume --cause guard --cc CC-999 > /dev/null
MAN=$(mkset); STUB_RC_rest_verify_d2v1=124 expect "resume, then rc 124 = CAP STOP" 0 "CAP STOP during rest.verify_d2v1" $J rest $H $MAN $M64 $H64
ok "resume skipped the finished step" '[ "$(grep -c "^rest.jb$" $HOME/stub.log)" = 1 ]'
ok "final stop writes its manifest (N4), and it verifies" 'verifies SHA256SUMS_rest_stop'
MAN=$(mkset); expect "CAP STOP is final" 1 "JOB STOP CAP_STOP.json exists: final" $J a1score $H $MAN $M64
mv $O/CAP_STOP.json $SB/CAP_STOP.moved
MAN=$(mkset); expect "one resume only" 1 "the one resume is used" $J rest $H $MAN $M64 $H64
MAN=$(mkset); expect "MAN must match" 1 "differs from MAN" $J a1score $H $(printf '0%.0s' {1..64}) $M64
MAN=$(mkset); printf y > $HB/a/extra; expect "no extra tmpfs file" 1 "file set differs" $J a1score $H $MAN $M64
MAN=$(mkset); expect "HEAD must be H_B" 1 "HEAD is not" $J a1score 0000000000000000000000000000000000000000 $MAN $M64

# --- B: TERM reaches a running step at once (W1)
newhome s a1decode
MAN=$(mkset); T0=$(date +%s)
( STUB_SLEEP=60 $J a1score $H $MAN $M64 > /dev/null 2>&1 & P=$!; sleep 3; kill -TERM $P; wait $P; echo $? > $SB/kill.rc )
EL=$(( $(date +%s) - T0 )); L=$(tail -n 1 $O/ledger.jsonl)
ok "TERM ends the job within 10 s (W1)" '[ $EL -le 10 ] && [ "$(cat $SB/kill.rc)" = 143 ]'
ok "the step process is gone" '! kill -0 $(cat $HOME/stub.pid) 2>/dev/null'
ok "the killed step is closed in the ledger" 'grep -q "\"rc\": 143" <<< "$L" && grep -q "\"step\": \"a1score.decomp_d1\"" <<< "$L"'
ok "the set is wiped after TERM" '[ ! -e $HB/a ]'
ok "TERM without the marker: no money line, no stop manifest (N-f HM28)" '! grep -q "MONEY STOP" $O/logs/job.log && [ ! -e $O/SHA256SUMS_a1score_stop ]'

# --- B2: money marker, then TERM to a step that takes 2 s to end (CC-295r2 N-a, N-b)
newhome s a1decode
MAN=$(mkset)
( STUB_SLOWTERM=1 $J a1score $H $MAN $M64 > /dev/null 2>&1 & P=$!; sleep 3; echo '{}' > $O/MONEY_STOP.json; kill -TERM $P
  wait $P; echo $? > $SB/kill2.rc )
ok "the trap waits for the step: ledger end after the step's exit (N-b)" '[ -s $HOME/stub.exit ] && after_stub'
ok "marker then TERM = MONEY STOP (final), manifest verifies (N-a)" '[ "$(cat $SB/kill2.rc)" = 143 ] && grep -q "MONEY STOP (final) on signal" $O/logs/job.log && verifies SHA256SUMS_a1score_stop'

# --- B4: marker, then tmux kill-session: teardown completes on a dead pty (CC-295r3 W9 d; own tmux socket)
newhome s a1decode
MAN=$(mkset); TS=bpa1st$$
tmux -L $TS new-session -d -s st -e "HOME=$HOME" -e "B_PA1_OUT=$O" -e "PATH=$PATH" -e STUB_SLEEP=60 \
  bash $B/b_pa1_job.sh a1score $H $MAN $M64   # argv form: PATH may hold spaces
for i in $(seq 1 100); do [ -s $HOME/stub.pid ] && break; sleep 0.1; done
echo '{}' > $O/MONEY_STOP.json; JP=$(cat $O/job.pid); tmux -L $TS kill-session -t st
for i in $(seq 1 100); do kill -0 $JP 2>/dev/null || break; sleep 0.1; done
tmux -L $TS kill-server 2>/dev/null
ok "dead pty: EXIT line, money line, stop manifest verifies (W9 d)" 'grep -q "EXIT a1score rc=143" $O/logs/job.log && grep -q "MONEY STOP (final) on signal" $O/logs/job.log && verifies SHA256SUMS_a1score_stop'
ok "dead pty: set wiped, one deletion line" '[ ! -e $HB/a ] && [ "$(wc -l < $O/b_pa1_hb_deletions.log)" = 1 ]'

# --- B5: marker, TERM, then a second TERM inside a slowed teardown (CC-295r3 W9 e)
newhome s a1decode
MAN=$(mkset)
( STUB_SLEEP=60 STUB_SLOWWIPE=1 $J a1score $H $MAN $M64 > /dev/null 2>&1 & P=$!
  for i in $(seq 1 100); do [ -s $HOME/stub.pid ] && break; sleep 0.1; done
  echo '{}' > $O/MONEY_STOP.json; kill -TERM $P
  for i in $(seq 1 100); do [ -e $HOME/wipe.started ] && break; sleep 0.1; done
  kill -TERM $P; wait $P; echo $? > $SB/kill5.rc )
ok "second TERM inside teardown: rc 143, EXIT line, stop manifest verifies (W9 e)" '[ -e $HOME/wipe.started ] && [ "$(cat $SB/kill5.rc)" = 143 ] && grep -q "EXIT a1score rc=143" $O/logs/job.log && grep -q "MONEY STOP (final) on signal" $O/logs/job.log && verifies SHA256SUMS_a1score_stop'
ok "second TERM inside teardown: set wiped, one deletion line" '[ ! -e $HB/a ] && [ "$(wc -l < $O/b_pa1_hb_deletions.log)" = 1 ]'

# --- C: block S, E-12 line
newhome
MAN=$(mkset); expect "block S logs E1/E2 NOT RUN" 0 "E1 E2 NOT RUN (pre-fixed, R5 E-12)" $J s $H $MAN

# --- D, E: rc 137 before LEFT = guard failure; at or after LEFT = CAP STOP (W2; fake timeout)
newhome s
MAN=$(mkset); PATH=$SB/fake:$PATH STUB_RC_a1decode_decode_internvl2_5_2b=137 expect "rc 137 before LEFT = guard stop (W2)" 1 "OOM or an outside KILL" $J a1decode $H $MAN
ok "rc 137 before LEFT is not final" '[ ! -e $O/CAP_STOP.json ]'
USED=$(( 28 * 3600 - 3 )) newhome s
MAN=$(mkset); PATH=$SB/fake:$PATH STUB_LATE137=5 expect "rc 137 after LEFT = CAP STOP (W2)" 0 "CAP STOP during a1decode.decode.internvl2_5_2b (KILL after its timeout)" $J a1decode $H $MAN

# --- F: no GPU-h left = CAP STOP before the step (timeout 0s would mean no limit)
USED=$(( 28 * 3600 )) newhome s
MAN=$(mkset); expect "LEFT 0 = CAP STOP before the step" 0 "CAP STOP cap reached before a1decode.decode.internvl2_5_2b" $J a1decode $H $MAN
ok "no step ran at LEFT 0" '[ ! -e $HOME/stub.log ]'

# --- G, H: core stop (W3), order
newhome
MAN=$(mkset); STUB_RC_s_trim=13 expect "rc 13 = CORE STOP (W3)" 0 "CORE STOP s.trim" $J s $H $MAN
ok "CORE_STOP.json written" '[ -e $O/CORE_STOP.json ] && verifies SHA256SUMS_s_stop'
date -u > $O/RUN.s.done
MAN=$(mkset); expect "no block after a core stop" 1 "CORE_STOP.json exists: final" $J a1decode $H $MAN
newhome
MAN=$(mkset); expect "a1decode needs RUN.s.done" 1 "needs RUN.s.done" $J a1decode $H $MAN
newhome
MAN=$(mkset); STUB_RC_s_smoke=3 expect "rc 3 = PA3 STOP" 0 "PA3 STOP s.smoke" $J s $H $MAN
ok "PA3 stop writes its manifest (N-f HM32)" 'verifies SHA256SUMS_s_stop'

# --- I: block W uses its own 1.0 GPU-h (left --w)
newhome
printf '{"ev": "start", "step": "w.feats0", "t": 1}\n{"ev": "end", "rc": 0, "sec": 3598, "step": "w.feats0", "t": 3599}\n' > $O/ledger.jsonl
MAN=$(mkset w); STUB_SLEEP=6 expect "W step bounded by the W cap" 0 "CAP STOP during w.feats1" $J w $H $MAN - 1

# --- J: a money stop written while a mode runs stops it at the next step
newhome s
MAN=$(mkset); STUB_MONEY=a1decode.decode.internvl2_5_2b expect "MONEY STOP at the next step (N3)" 0 "MONEY STOP (final) before a1decode.decode.mblip_mt0_xl" $J a1decode $H $MAN
ok "money stop writes its manifest" 'verifies SHA256SUMS_a1decode_stop'

# --- L: a step that reads stdin cannot eat the step list (N2)
newhome s
MAN=$(mkset); STUB_READ=1 expect "stdin-reading step: mode still done" 0 "JOB DONE a1decode" $J a1decode $H $MAN
ok "every step of the mode ran (N2)" '[ "$(wc -l < $HOME/stub.log)" = 4 ]'

# --- K: selftest mode (T8)
newhome
expect "selftest mode: T8 wipe line" 0 "HOSTCHECK OK" $J selftest $H -
ok "no set dir left" '[ ! -e $HB/a ] && [ ! -e $HB/w ] && [ ! -e $HB/st ]'
for s in a w; do [ ! -e $HB/$s ] || { rm -f $HB/$s/f1 $HB/$s/MANIFEST.sha256 $HB/$s/extra; rmdir $HB/$s; }; done
[ ! -e $HB ] || rmdir $HB
echo "sandbox $SB (left in place)"; [ $FAIL = 0 ] && echo "JOB SELFTEST PASS ($N checks)" || echo "JOB SELFTEST FAIL"
exit $FAIL
