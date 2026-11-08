#!/bin/bash
# B-PA1-T1 HB-T1 job (v3.1 l.12; B_RUN_DOC_v1 RB4; DRAFT, not read). One tmux session per mode, started by the coordinator:
#   bash scripts/b_pa1/b_pa1_job.sh MODE <expected 40-hex HEAD = H_B> <MAN: sha256 of /dev/shm/b_pa1_hb/<set>/MANIFEST.sha256> [MAPF] [EXTRA]
# MODE selftest  CPU selftest in both GPU venvs, hostcheck main + legacy (T1-T7, T9), the T8 wipe check; MAN = '-'
#      w         block W: b_pa1_w25.py feats in the W venv (freeze 1a639a50), EXTRA = blocks through (NBLK); set w
#      s         block S: the §4.3 walk with the §4.4 gate, the A4 decode rates, the smoke, rates.json + TRIM.json; set a
#      a1decode  4 accepted captioners x slice A (captions only, v3.1 §6.4 step 3); set a
#      a1score   MAPF = final map sha (recorded only; the host never holds the map): d1, v1, J-a, CLIPScore; set a
#      rest      MAPF as a1score; EXTRA = sha of ~/b_pa1_out/in/h_input.jsonl or '-'; A2, then TRIM.json's A3, H, A4
# Never rents, tops up or deletes a machine; it only stops. Final stops: a cap stop (rc 124, or rc 137 at or after the
# step's LEFT; W: its own 1.0 GPU-h), a money stop (MONEY_STOP.json, written by the coordinator, who then kills this job
# by ~/b_pa1_out/job.pid; a TERM with MONEY_STOP.json present is that final stop), PA3.json and CORE_STOP.json (the core
# cannot finish: the PI decides). Each final stop writes SHA256SUMS_<run>_stop, a done mode SHA256SUMS_<mode>; the EXIT
# trap writes either one last, after the EXIT line, so logs/job.log verifies at the pull (CC-295r2); teardown ignores
# TERM / HUP / INT / PIPE and say() cannot fail on a dead console, so a tmux kill-session or a second TERM cannot cut it
# short (CC-295r3 W9). Only a KILL of the job itself (untrappable) loses the manifest. A rc 137 before LEFT (OOM or an outside KILL) is a guard failure, not final. Each step runs in
# the background with stdin </dev/null; TERM / HUP / INT to the job is forwarded to the step's process group (GNU
# timeout makes its own), so a running step ends at once and the trap closes its ledger step and wipes (CC-295 W1).
# The one registered resume (guard failure or machine loss, v3.1 l.519-520) needs RESUME.json (`b_pa1_gpu.py resume`).
# Images only in /dev/shm/b_pa1_hb/<set> (0700); a trap deletes the set dir on ANY exit and logs (utc, folder, files,
# manifest count) to ~/b_pa1_out/b_pa1_hb_deletions.log (R6 §I.4). Logs hold ids and counts only.
set -euo pipefail
MODE=${1:?usage: b_pa1_job.sh selftest|w|s|a1decode|a1score|rest H_B MAN [MAPF] [EXTRA]}; EXPECT=${2:?H_B}; MAN=${3:?MAN}
MAPF=${4:--}; EXTRA=${5:--}
cd "$(dirname "$0")/../.."
FRAME_SHA=863ad3e90577c37dac2d2384062239fc71e747c167700d2566926ba2d69b7234   # LOG l.1226
W_FREEZE=1a639a50adf550c50c6dfe284146e279b2a2bf2a716ade743e9eb357ccbf0778    # R5 §D.2 (= requirements_b_pa1_w.txt)
B=scripts/b_pa1; X=$B/b_pa1_gpu.py
LKM=$(sha256sum $B/requirements_b_pa1_main.lock | cut -c1-8); LKL=$(sha256sum $B/requirements_b_pa1_legacy.lock | cut -c1-8)
PYM=$HOME/venvs/b_pa1_main_$LKM/bin/python; PYL=$HOME/venvs/b_pa1_legacy_$LKL/bin/python; PYW=$HOME/venvs/b_pa1_w/bin/python
O=$HOME/b_pa1_out; LOG=$O/logs; HB=/dev/shm/b_pa1_hb; SSCD=$HOME/b_pa1_models/sscd_disc_mixup.torchscript.pt
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HOME=$HOME/b_pa1_models/hf B_PA1_OUT=$O B_PA1_HB=$HB
case "$MODE" in selftest) SET=st;; w) SET=w;; s|a1decode|a1score|rest) SET=a;; *) echo "unknown mode $MODE"; exit 2;; esac
mkdir -p $LOG
ts() { date -u +%FT%TZ; }
mono() { local u; read -r u _ < /proc/uptime; echo ${u%.*}; }   # monotonic seconds: a wall-clock step cannot skew EL
say() { local l; l="$(ts) $*"; echo "$l" >> $LOG/job.log; echo "$l" 2>/dev/null || true; }   # W9 (b): file first; a dead console cannot fail it
stop() { say "JOB STOP $*"; exit 1; }
exec 9> $O/.job.lock
flock -n 9 || { echo "REFUSED: another b_pa1 job is running"; exit 1; }
echo $$ > $O/job.pid   # the coordinator stops this job only through this file (kp, never a pattern)
FINAL="CAP_STOP.json MONEY_STOP.json PA3.json CORE_STOP.json"
STEP=; SPID=; RK=$MODE; MANIFEST=
teardown() {
  local rc=$?; trap '' TERM HUP INT PIPE   # CC-295r3 W9 (a): no second signal can cut teardown short
  if [ -n "$STEP" ]; then $PYM -I -B $X ledger end "$STEP" --rc $rc || say "LEDGER END FAILED $STEP"; fi
  if [ -d $HB/$SET ]; then $PYM -I -B $X wipe --dir $HB/$SET --log $O/b_pa1_hb_deletions.log || say "WIPE COUNT MISMATCH"; fi
  if [ $rc = 143 ] && [ -e $O/MONEY_STOP.json ]; then MANIFEST=SHA256SUMS_${RK}_stop; say "MONEY STOP (final) on signal"; fi  # CC-295r2 N-a
  say "EXIT $MODE rc=$rc"
  [ -z "$MANIFEST" ] || sums > $O/$MANIFEST   # last: the lines above are in job.log before it is hashed
}
on_signal() {  # CC-295 W1: forward to the running step's process group, wait for it, then the EXIT trap runs
  if [ -n "$SPID" ]; then kill -TERM -- -$SPID 2>/dev/null || kill -TERM $SPID 2>/dev/null || true; wait $SPID 2>/dev/null || true; fi
  exit 143
}
trap teardown EXIT
trap on_signal TERM HUP INT
sums() {  # CC-295 N4: the manifest the final pull checks (out, logs, w25_parts)
  (cd $O && find $(for d in out logs w25_parts; do [ -d $d ] && echo $d; done) -type f | LC_ALL=C sort | xargs -r sha256sum)
}
final() { printf '{"%s": "%s", "utc": "%s"}\n' "$1" "$2" "$(ts)" > $O/$3; MANIFEST=SHA256SUMS_${RK}_stop; say "$4 $2 (final)"; exit 0; }

# ---------------------------------------------------------------------------------------------- preflight
for m in $FINAL; do [ ! -e $O/$m ] || stop "$m exists: final"; done
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
(cd $B && sha256sum --quiet -c SHA256SUMS && sha256sum --quiet -c SHA256SUMS_GPU) || stop "scripts/b_pa1 SUMS"
[ -s host_w25.sums ] && sha256sum --quiet -c host_w25.sums || stop "host_w25.sums missing or failing (run doc §1.4)"
nvidia-smi --query-gpu=name --format=csv,noheader | grep -Eq '^NVIDIA GeForce RTX 3090( Ti)?$' || stop "GPU is not one 3090"
UUID=$(nvidia-smi --query-gpu=uuid --format=csv,noheader)   # binds HOSTCHECK_*.json to this machine (HB-T1' restores ~/b_pa1_out)
[[ $UUID =~ ^GPU-[0-9a-f-]+$ ]] || stop "no GPU uuid"
for v in main legacy; do
  P=$PYM; [ $v = legacy ] && P=$PYL
  F=$($P -m pip freeze | sha256sum | cut -c1-64); [ -s $O/freeze_$v.sha256 ] || stop "no first-build freeze for $v (setup)"
  [ "$F" = "$(cat $O/freeze_$v.sha256)" ] || stop "$v venv freeze differs from its first build (R2)"
  eval "FREEZE_$v=$F"
done
CODE=$(sha256sum $B/SHA256SUMS_GPU | cut -c1-64)
$PYM -I -B $X selftest >> $LOG/selftest.log 2>&1 || stop "b_pa1_gpu selftest (main venv)"
$PYL -I -B $X selftest >> $LOG/selftest.log 2>&1 || stop "b_pa1_gpu selftest (legacy venv)"
sha256sum $B/b_pa1_gpu.py $B/b_pa1_models.py $B/b_pa1_registry.json $0 > $O/code_at_start_$MODE.sha256

if [ "$MODE" = selftest ]; then
  [ "$MAN" = - ] || stop "selftest takes MAN '-' (no B image on the host yet)"
  B_PA1_CODE=$CODE B_PA1_FREEZE=$FREEZE_main B_PA1_GPU=$UUID $PYM -I -B $X hostcheck --venv main >> $LOG/hostcheck.log 2>&1 || stop "hostcheck main"
  B_PA1_CODE=$CODE B_PA1_FREEZE=$FREEZE_legacy B_PA1_GPU=$UUID $PYL -I -B $X hostcheck --venv legacy >> $LOG/hostcheck.log 2>&1 || stop "hostcheck legacy"
  NEW=0; [ -e $HB ] || { mkdir -m 700 $HB; NEW=1; }   # T8: the trap's wipe on a synthetic set, one log line
  mkdir -m 700 $HB/st && printf 'a' > $HB/st/f1 && printf 'b' > $HB/st/f2
  (cd $HB/st && sha256sum f1 f2 > MANIFEST.sha256)
  N0=$(wc -l < $O/b_pa1_hb_deletions.log 2>/dev/null || echo 0)
  $PYM -I -B $X wipe --dir $HB/st --log $O/b_pa1_hb_deletions.log || stop "T8 wipe count"
  [ ! -e $HB/st ] && [ "$(wc -l < $O/b_pa1_hb_deletions.log)" = $((N0 + 1)) ] \
    && [ "$(tail -n 1 $O/b_pa1_hb_deletions.log | cut -f3,4)" = "$(printf '3\t2')" ] || stop "T8 deletion log line"
  [ $NEW = 0 ] || rmdir $HB
  say "HOSTCHECK OK"; exit 0
fi
for v in main legacy; do
  eval "F=\$FREEZE_$v"
  $PYM -I -c 'import json, sys; d = json.load(open(sys.argv[1])); sys.exit(d["code"] != sys.argv[2] or d["freeze"] != sys.argv[3] or d["gpu_uuid"] != sys.argv[4])' \
    $O/HOSTCHECK_$v.json "$CODE" "$F" "$UUID" || stop "HOSTCHECK_$v.json missing or stale (run mode selftest at this H_B on this GPU)"
done
[ "$(stat -c %a $HB)" = 700 ] && [ "$(stat -c %a $HB/$SET)" = 700 ] || stop "$HB/$SET is not mode 0700"
[ "$(sha256sum < $HB/$SET/MANIFEST.sha256 | cut -c1-64)" = "$MAN" ] || stop "tmpfs MANIFEST.sha256 differs from MAN"
(cd $HB/$SET && sha256sum --quiet -c MANIFEST.sha256) || stop "a tmpfs file differs from its arrival sha (FAULT)"
[ "$(cd $HB/$SET && find . ! -type d | sed 's|^\./||' | LC_ALL=C sort)" = "$( (echo MANIFEST.sha256; cut -c67- $HB/$SET/MANIFEST.sha256) | LC_ALL=C sort)" ] \
  || stop "tmpfs file set differs from MANIFEST.sha256"
[ "$(sha256sum < $O/in/o365_train_frame.tsv | cut -c1-64)" = $FRAME_SHA ] || stop "frame file differs from 863ad3e9"
case "$MODE" in a1decode) PREV=s;; a1score) PREV=a1decode;; rest) PREV=a1score;; *) PREV=;; esac   # CC-295 W3
[ -z "$PREV" ] || [ -e $O/RUN.$PREV.done ] || stop "$MODE needs RUN.$PREV.done (the registered order, v3.1 §6.4)"
case "$MODE" in
  w) [[ $EXTRA =~ ^[1-9][0-9]*$ ]] || stop "w needs EXTRA = blocks through"; [ "$MAPF" = - ] || stop "w takes MAPF '-'"
     $PYM -I -B $X inputs --set w --nblk $EXTRA >> $LOG/job.log || stop "W set is not blocks ..$EXTRA of the frame";;
  s|a1decode) [ "$MAPF" = - ] && [ "$EXTRA" = - ] || stop "$MODE takes MAPF and EXTRA '-'"
     $PYM -I -B $X inputs --set a >> $LOG/job.log || stop "slice-A set";;
  a1score|rest) [[ $MAPF =~ ^[0-9a-f]{64}$ ]] || stop "$MODE needs the final map sha (MAPF)"
     $PYM -I -B $X inputs --set a >> $LOG/job.log || stop "slice-A set";;
esac
# ---------------------------------------------------------------------------------------------- steps
if [ "$MODE" = w ]; then
  [ "$($PYW -m pip freeze | sha256sum | cut -c1-64)" = $W_FREEZE ] || stop "W venv freeze differs from 1a639a50 (R5 §D.2 fallback: laptop)"
  STEPS="w.feats$EXTRA w"
else
  STEPS=$($PYM -I -B $X steps --mode $MODE) || stop "steps"
  if echo "$STEPS" | grep -q '^rest\.h_' && ! [[ $EXTRA =~ ^[0-9a-f]{64}$ ]]; then stop "TRIM keeps H: EXTRA = h_input.jsonl sha"; fi
fi
[ $MODE != w ] || RK=w$EXTRA   # §9.3: a W run with more blocks is a new run
if [ -e $O/RUN.$RK.started ] && [ ! -e $O/RUN.$RK.done ]; then   # v3.1 l.519-520: one resume, two causes
  [ -e $O/RESUME.json ] || stop "previous $RK run did not finish: a resume needs RESUME.json (cause read)"
  ( set -C; echo "$RK $(ts)" > $O/RESUME_USED ) 2>/dev/null || stop "the one resume is used: the PI decides"
  say "RESUME $RK ($(cat $O/RESUME.json))"
fi
[ ! -e $O/RUN.$RK.done ] || stop "run $RK is already done"
[ -e $O/RUN.$RK.started ] || ts > $O/RUN.$RK.started

while read -r ST V; do
  [ -s $LOG/done.$ST ] && continue
  for m in $FINAL; do   # CC-295 N3: a marker written while this job runs (e.g. MONEY_STOP.json) stops it here
    [ ! -e $O/$m ] || { n=${m%.json}; MANIFEST=SHA256SUMS_${RK}_stop; say "${n/_/ } (final) before $ST"; exit 0; }
  done
  if [ "$V" = w ]; then LEFT=$($PYM -I -B $X left --w); else LEFT=$($PYM -I -B $X left); fi
  [ "$LEFT" -gt 0 ] || final cap_stop "cap reached before $ST" CAP_STOP.json "CAP STOP"   # timeout 0s = no limit
  $PYM -I -B $X ledger start $ST || stop "ledger start $ST"
  STEP=$ST
  say "START $ST (left $(( LEFT / 60 )) min)"
  T0S=$(mono); rc=0
  case $V in
    w) timeout --kill-after=60 ${LEFT}s $PYW -I -B $B/b_pa1_w25.py feats --frame $O/in/o365_train_frame.tsv --images $HB/w \
         --sscd $SSCD --parts $O/w25_parts --blocks $EXTRA < /dev/null >> $LOG/w.log 2>&1 &;;
    main) timeout --kill-after=60 ${LEFT}s $PYM -I -B $X run $ST --mapf $MAPF --hin $EXTRA < /dev/null >> $LOG/steps.log 2>&1 &;;
    legacy) timeout --kill-after=60 ${LEFT}s $PYL -I -B $X run $ST --mapf $MAPF --hin $EXTRA < /dev/null >> $LOG/steps.log 2>&1 &;;
    *) stop "unknown venv $V";;
  esac
  SPID=$!; wait $SPID || rc=$?; SPID=
  EL=$(( $(mono) - T0S ))
  $PYM -I -B $X ledger end $ST --rc $rc; STEP=
  case $rc in
    0) ts > $LOG/done.$ST; say "OK $ST";;
    124) final cap_stop "during $ST" CAP_STOP.json "CAP STOP";;
    137) [ $EL -lt $LEFT ] || final cap_stop "during $ST (KILL after its timeout)" CAP_STOP.json "CAP STOP"   # CC-295 W2
         stop "$ST rc=137 after ${EL}s < LEFT ${LEFT}s: OOM or an outside KILL (guard failure, not a cap stop)";;
    3) MANIFEST=SHA256SUMS_${RK}_stop; say "PA3 STOP $ST (PA3.json; v3.1 §11)"; exit 0;;
    13) [ -e $O/CORE_STOP.json ] || printf '{"core_stop": "%s", "utc": "%s"}\n' "$ST" "$(ts)" > $O/CORE_STOP.json
        MANIFEST=SHA256SUMS_${RK}_stop; say "CORE STOP $ST (CORE_STOP.json; v3.1 l.506 as R5 E-12: the PI decides) (final)"; exit 0;;
    *) stop "$ST rc=$rc";;
  esac
done <<< "$STEPS"
ts > $O/RUN.$RK.done
MANIFEST=SHA256SUMS_$MODE   # written by the EXIT trap, after JOB DONE and EXIT
[ "$MODE" != s ] || say "E1 E2 NOT RUN (pre-fixed, R5 E-12)"   # in the run log before the end of A2 (R5 E-12)
say "JOB DONE $MODE"
