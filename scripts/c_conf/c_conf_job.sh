#!/bin/bash
# C-CONF host job on one rented RTX 3090 / 3090 Ti 24 GB (machine id h1 or h2). DRAFT on synthetic fixtures under CC-438
# FP-7: no study data, no host run, no token, no commit before a GO. Rule: registration draft
# manuscript/directions/C_CONFIRM_PREREG_DRAFT_2026-11-16_v3.md (18e61111) §6 (blocks), §6.5 (test-host order), §9 (D1), §10.1
# (G0-G6), §10.2 (cap, drop order), §10.3 (custody), with CC-450 X5 (time check before T0). Labels: rehearsal
# "TIER 2 / DEV-CONFIRM (C-CONF), OV-CARVE"; test "TIER 3 / TEST (C-CONF), SECOND LOOK AT OV-TEST". No scoring here
# (scripts/c_conf/c_conf_score.py stage, after the pull); comparators print counts and item ids only.
#
# Usage, inside tmux:  bash scripts/c_conf/c_conf_job.sh selftest|block0|rehearsal <expected HEAD>
#                      bash scripts/c_conf/c_conf_job.sh test <expected HEAD> <token file> <rehearsal decision file>
#  block0     §6.2 (CPU): 0.1 inputs hashed; 0.2 carve from the pinned order, lists of every arm, K0 and K0 on the
#             first-look form; 0.3 perm diagnostics and the refill gate (G0b); 0.4 dry run of every host mode; 0.5 the
#             scoring parity gate (§7.1). No OV-test byte on the host.
#  rehearsal  §6.3: call 1 = R.0 (D1 per runner) and the cap (§10.2; 1.5 P > 30 is a STOP), then a PAUSE so the cap
#             is logged; call 2 = R.1 Qwen2.5-VL-7B, R.4 LMCap, R.2 InternVL3-8B, R.3 Aya-Vision-8B under the cap.
#  test       §6.5, only with a token whose four fields verify: call 1 = T.0 (D1 on the 50 OV-dev-B items, no OV-test
#             byte) and the cap, logged with the X5 time check (drop order applied here, before any OV-test byte), then
#             a PAUSE; call 2 = the time check again, the scoring parity gate, the dry run of step 0.4, and the time check
#             at the moment T0 would start; it writes T0_READY.json and stops: the operator stages the OV-test files
#             named in §6.4a into /root/c_conf_ov_test (the look begins at the first byte); call 3 = T0 (staged files
#             against their sha256, lists from the stored first-look vectors, K0-T, refill gate) and T.1, T.4, T.2, T.3.
#             A stop before T0 spends no look; a stop at or after T0 is the look, and its rows are NOT RUN.
# Every GPU step runs under `timeout` for min(cap left, time left to G6); a timeout is a CAP STOP, final, and every
# later step is NOT RUN (steps drop from the bottom). A failed step resumes from its own partial file, at most 3
# attempts, then JOB STOP; a .done step is never decoded twice. C_CONF_RUNNERS limits the runners of one host (two
# hosts: one LMCap then InternVL3-8B, the other Qwen2.5-VL-7B then Aya-Vision-8B; each runs its own D1).
# Dry run: C_CONF_DRY=1 on the host itself (PI 2026-11-11): every decode runs with --limit 2 --dry-run and stops before
# the model load; GPU, venv freeze and weight checks are skipped with a DRY line; the comparators answer rc 3 and D1 is
# taken as PASS; the cap uses the §6.1 planning rates; one call runs every phase without the PAUSEs and the OV-test
# staging is simulated by an empty folder (no OV-test byte). Only in a dry run are these honoured: C_CONF_ROOT (the
# sandbox in place of /root), C_CONF_FREEZE_UTC (G6) and C_CONF_FORCE_CAP_H (a forced binding cap).
# Interface of scripts/c_conf/c_conf.py, c_conf_arms.py (block0, diag, t0) and c_conf_score.py used here: the table of
# manuscript/directions/CODE_INTEGRATION_REPORT_C_CONF_2026-11-18.md. c_conf_lists.py (the pinned order builder, c774f1a4)
# is not called; c_conf_arms.py imports it (ktvic_owner_ids, pairs_block), so it is hashed with the code at start.
set -euo pipefail
MODE=${1:?usage: c_conf_job.sh selftest|block0|rehearsal|test <expected HEAD> [token decision]}
EXPECT=${2:?usage: c_conf_job.sh MODE <expected HEAD>}
case $MODE in selftest|block0|rehearsal|test) ;; *) echo "unknown mode $MODE"; exit 2;; esac
DRY=${C_CONF_DRY:-0}
dry() { [ "$DRY" = 1 ]; }
FREEZE=2026-11-27T11:00:00Z   # G6 = 2026-11-27 18:00 (UTC+7), §10.1
R=/root; FORCE=()
if dry; then
  R=${C_CONF_ROOT:-/root}; FREEZE=${C_CONF_FREEZE_UTC:-$FREEZE}
  [ -n "${C_CONF_FORCE_CAP_H:-}" ] && FORCE=(--force-ceiling-h $C_CONF_FORCE_CAP_H)
fi
MID=$(cat $R/.vsps_machine_id 2>/dev/null || true)
case "$MID" in h1|h2) ;; *) echo "REFUSED: $R/.vsps_machine_id is not h1 or h2"; exit 1;; esac
cd $R/vsps
export NCS_DATA=$R/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=$MID
PY=$R/vsps/.venv/bin/python; LB=$R/venv-lb/bin/python; T1=$R/venv-t1/bin/python
FT=$R/venv-cenfeat/bin/python   # block 0 only: the feature pass (image hashes, SSCD), as the W25 / C-PVR passes (I5)
# venv-cenfeat on a fresh host: install_system.sh base (scripts/host_bundle), then python3.12 -m venv $R/venv-cenfeat and
# pip install --no-deps --extra-index-url https://download.pytorch.org/whl/cpu -r manuscript/prereg/2026-10-27_c_en/
# cenfeat_venv_freeze.txt (the form of scripts/b_pa1/b_pa1_setup_host.sh l.55-57); its freeze is checked below.
LB_FREEZE=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784   # environment freeze of v1.2 (§4)
T1_FREEZE=1766dc23a71509ba4fb6b8adb34b1999a3a2bf78ebe1e227730fd6647bea3599   # venv-t1 of record (LMCap)
FT_FREEZE=1a639a50adf550c50c6dfe284146e279b2a2bf2a716ade743e9eb357ccbf0778   # cenfeat_venv_freeze.txt (C-EN), block 0
X=scripts/c_conf/c_conf.py; L=scripts/c_conf/c_conf_arms.py; SC=scripts/c_conf/c_conf_score.py; L1=scripts/c_conf/c_conf_lists.py
JOB=scripts/c_conf/c_conf_job.sh; REG=manuscript/prereg/2026-11-18_c_conf   # the folder name is set at the registration commit
DS=$NCS_DATA/datasets; CL=manuscript/prereg/2026-10-22_c_stage1/lists.json; STAGE_T=$R/c_conf_ov_test
TOKEN=${3:-}; DECISION=${4:-}
case $MODE in block0) O=$R/outputs/c_conf_b0;; rehearsal) O=$R/outputs/c_conf_r;; test) O=$R/outputs/c_conf_t;; *) O=$R/outputs/c_conf_selftest;; esac
dry && O=${O}_dry
P=$O/out; LOG=$O/logs; Q=$O/parity; USED=$O/gpu_seconds.tsv; MARK=$O/CAP_STOP.json; CAP=$O/CAP.json
mkdir -p $O $P $LOG $Q
ts() { date -u +%FT%TZ; }
say() { echo "$(ts) $*" | tee -a $LOG/job.log; }
stop() {  # after T0 every stop is the look (§6.5, I3): LOOK_STOP.json is written once and later sessions are refused
  say "JOB STOP $*"
  if [ -s $LOG/T0.done ] && [ ! -e $O/LOOK_STOP.json ]; then
    printf '{"look_stop": "JOB STOP after T0: %s", "utc": "%s"}\n' "$*" "$(ts)" > $O/LOOK_STOP.json
  fi
  exit 1; }
exec 9>$O/RUNNING; flock -n 9 || { echo "REFUSED: $O/RUNNING is locked (a job of this mode runs)"; exit 1; }
( while sleep 60; do ts > $O/HEARTBEAT; done ) > /dev/null 2>&1 9>&- & HB=$!
trap 'kill $HB 2>/dev/null; rm -f $O/RUNNING' EXIT
dry && say "DRY RUN: mode $MODE, decodes stop before the model load, freeze $FREEZE${FORCE:+, forced ceiling ${FORCE[1]} GPU-h}"

# ---------------------------------------------------------------- preflight (every mode)
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
if dry; then say "DRY: GPU-busy check skipped (no GPU)"
else [ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ] || stop "GPU busy (another job): never concurrent"; fi
for d in $R/outputs/c_conf_b0 $R/outputs/c_conf_r $R/outputs/c_conf_t; do
  [ "$d" != "$O" ] && [ -e $d/RUNNING ] && stop "$d/RUNNING exists (never beside another job, §6.6)"
done
(cd scripts/c_conf && sha256sum --quiet -c SHA256SUMS) || stop "scripts/c_conf/SHA256SUMS"
(cd $REG && sha256sum --quiet -c SHA256SUMS) || stop "registration SHA256SUMS"
if dry; then say "DRY: venv freeze checks skipped (laptop-like venv)"
else
  [ "$($R/venv-lb/bin/pip freeze | sha256sum | cut -c1-64)" = $LB_FREEZE ] || stop "venv-lb freeze differs"
  [ "$($R/venv-t1/bin/pip freeze | sha256sum | cut -c1-64)" = $T1_FREEZE ] || stop "venv-t1 freeze differs"
  [ $MODE != block0 ] || [ "$($FT -m pip freeze | sha256sum | cut -c1-64)" = $FT_FREEZE ] || stop "venv-cenfeat freeze differs"
fi
if [ $MODE = block0 ]; then   # I5: the feature pass imports in venv-cenfeat (in a dry run too)
  $FT $L envcheck >> $LOG/envcheck.log 2>&1 || stop "venv-cenfeat import check (block 0)"
fi
$PY $X guard --datasets $DS --roots $DS $NCS_DATA/models $O >> $LOG/guard.log 2>&1 || stop "custody guard (§5.4 refusals)"
[ $MODE = test ] || [ ! -e $STAGE_T ] || stop "$STAGE_T exists outside the test session (no OV-test byte before the token, §10.3)"
if [ $MODE = test ]; then   # G3: no token, nothing of block T (§6.4 item 5, §10.1)
  [ -s "$TOKEN" ] && [ -s "$DECISION" ] || stop "test needs the token file and the rehearsal decision file (G3)"
  $PY $X token --token $TOKEN --decision $DECISION >> $LOG/token.log 2>&1 || stop "the token does not verify (G3)"
fi
sha256sum $X $L $L1 $SC $JOB > $O/code_at_start.sha256
say "PREFLIGHT OK head $EXPECT mode $MODE"
[ $MODE = selftest ] && { say "SELFTEST MODE DONE"; exit 0; }

# ---------------------------------------------------------------- shared steps
finish() {  # the host's sums; the laptop pulls only after the job has ended (§10.3)
  (cd $O && find out logs parity -type f ! -name '*.partial*' | LC_ALL=C sort | xargs -r sha256sum) > $O/SHA256SUMS
  say "JOB DONE gpu_h $(awk '$2 != "start" {s += $2} END {printf "%.2f", s / 3600}' $USED 2>/dev/null || echo 0)"; exit ${1:-0}; }
cap_stop() { [ -e $MARK ] || printf '{"cap_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > $MARK; say "CAP STOP $1 (later steps NOT RUN)"; finish; }
jget() { $PY -I -c 'import json, sys; v = json.load(open(sys.argv[1]))[sys.argv[2]]; print(" ".join(v) if isinstance(v, list) else v)' "$@"; }
left() {  # seconds left: min(hard cap - GPU seconds used, seconds to G6); before the cap line, the 30 GPU-h ceiling
  local used now g6 cs=$((30 * 3600)) c; used=$(awk '$2 != "start" {s += $2} END {print s + 0}' $USED 2>/dev/null || echo 0)
  [ -s $CAP ] && cs=$(jget $CAP cap_s)
  now=$(date +%s); g6=$(date -d $FREEZE +%s); c=$(( cs - ${used%.*} ))
  echo $(( c < g6 - now ? c : g6 - now ))
}
gpu() {  # gpu NAME CMD...: one GPU step under the time left; up to 3 attempts, each resuming from its partial file
  local name=$1; shift
  [ -s $LOG/$name.done ] && return 0
  [ -e $MARK ] && { say "NOT RUN $name (after a CAP STOP)"; return 0; }
  local att t t0 rc tries=3
  [[ $name == T_lmcap_* ]] && tries=1   # §6.5: LMCap keeps no partial file, so on OV-test it is never re-decoded (CC-454 B5)
  for att in $(seq 1 $tries); do
    t=$(left)
    [ "$t" -gt 0 ] || cap_stop "cap or G6 before $name"
    say "START $name attempt $att (left $((t / 60)) min)"
    rc=0; t0=$(date +%s); echo "$name start $t0" >> $USED
    timeout ${t}s "$@" >> $LOG/$name.log 2>&1 || rc=$?
    echo "$name $(( $(date +%s) - t0 ))" >> $USED
    [ $rc = 124 ] && cap_stop "cap or G6 reached during $name"
    [ $rc = 0 ] && { say "OK $name"; ts > $LOG/$name.done; return 0; }
    say "FAIL $name rc=$rc attempt $att"
  done
  stop "$name failed $tries attempt(s)"
}
DRYARGS=(); dry && DRYARGS=(--limit 2 --dry-run)
declare -A CFG=([qwen25vl_7b]="8 first T1" [internvl3_8b]="4 last T2" [aya_vision_8b]="4 last T1")
snap() { case $1 in qwen25vl_7b|internvl3_8b) echo $NCS_DATA/models/$1;; *) echo $NCS_DATA/models/c_t1_$1;; esac; }
out_of() { local m=$1 s=$2 rd=$3; set -- ${CFG[$m]}; echo "$P/cc_${m}_${s}-ret-k$1-$2-$3-mvi-$rd$(dry && echo -smoke).preds.json"; }
lm_out() { echo "$P/cc_lmcap-ri_ov_dev_b-mvi-$1$(dry && echo -smoke).preds.json"; }
TOK=(); [ $MODE = test ] && TOK=(--token $TOKEN --decision $DECISION)   # c_conf.py admits the token against this file
dec() {  # dec NAME MODEL SET ARM [args]: one decode at batch size 1 (binding 6), Vietnamese memory
  local name=$1 m=$2 s=$3 arm=$4; shift 4
  gpu $name $LB $X decode --model $m --set $s --arm $arm --snapshot $(snap $m) --out-dir $P --c-lists $CL \
    --images $DS --memory vi --batch1 "${TOK[@]}" "$@" "${DRYARGS[@]}"
}
lm() {  # lm NAME SET VARIANT [args]: one LMCap re-implementation decode (venv-t1), one query per call
  local name=$1 s=$2 v=$3; shift 3
  gpu $name $T1 $X lmcap --set $s --variant $v --out-dir $P --c-lists $CL --images $DS --memory vi --batch1 \
    "${TOK[@]}" "$@" "${DRYARGS[@]}"
}
arms() {  # arms STEP MODEL SET: the seven runs of §2 (zs, ret, rand d0-d2, perm p1-p2), or LMCap's three
  local st=$1 m=$2 s=$3
  if [ $m = lmcap ]; then for v in ri rand perm; do lm ${st}_lmcap_$v $s $v; done; return; fi
  set -- ${CFG[$m]}
  dec ${st}_${m}_zs $m $s zs
  dec ${st}_${m}_ret $m $s ret --k $1 --order $2 --tpl $3
  for d in 0 1 2; do dec ${st}_${m}_rand$d $m $s rand --k $1 --order $2 --tpl $3 --draw $d; done
  for p in 1 2; do dec ${st}_${m}_perm$p $m $s perm --k $1 --order $2 --tpl $3 --draw $p; done
}
cmp_() {  # cmp_ NAME NEW OLD: rc 0 identical, 3 differs (counts and ids only); anything else stops
  local rc=0 extra=(); dry && extra=(--dry-run)
  $PY $X compare --name $1 --set ov_dev_b --new $2 --old $3 --d1 --out $Q/$1.json "${extra[@]}" >> $LOG/compare.log 2>&1 || rc=$?
  [ $rc = 0 ] || [ $rc = 3 ] || stop "compare $1 rc=$rc"
  return $rc
}
D1_PASS=()
d1() {  # §9 D1 on this host: the first 50 OV-dev-B ret items at batch size 1, reversed then stored order
  local r=$1 v=PASS fwd rev
  if [ $r = lmcap ]; then
    lm D1r_lmcap ov_dev_b ri --redecode rev50; lm D1_lmcap ov_dev_b ri --redecode fwd50; fwd=$(lm_out fwd50); rev=$(lm_out rev50)
  else
    set -- ${CFG[$r]}
    dec D1r_$r $r ov_dev_b ret --k $1 --order $2 --tpl $3 --redecode rev50
    dec D1_$r $r ov_dev_b ret --k $1 --order $2 --tpl $3 --redecode fwd50
    fwd=$(out_of $r ov_dev_b b1-fwd50); rev=$(out_of $r ov_dev_b b1-rev50)
  fi
  cmp_ D1_$r $fwd $rev || v=FAIL
  dry && v=PASS   # dry: the comparator answers rc 3; every step is exercised
  printf '{"model": "%s", "D1": "%s", "host": "%s", "utc": "%s"}\n' $r $v $MID "$(ts)" > $Q/D1_$r.json
  say "STEP D1 $r $v$( [ $v = FAIL ] && echo ' (leaves the study on every host)')"
  [ $v = PASS ] && D1_PASS+=($r) && D1_FILES+=($fwd)
  [ $v = FAIL ] && [ $r = qwen25vl_7b ] && stop "D1 FAIL for Qwen2.5-VL-7B: the study stops (§9)"
  return 0
}
plan() {  # plan MODE RUNNERS...: §10.2 cap and drop order (and X5 in test), logged before the first registered step
  local mode=$1 rc=0; shift
  if dry; then $PY -I -B $SC plan --mode $mode --dry-run --runners "$@" --freeze-utc $FREEZE "${FORCE[@]}" --out $CAP >> $LOG/plan.log 2>&1 || rc=$?
  else $PY -I -B $SC plan --mode $mode --d1 "${D1_FILES[@]}" --out $CAP >> $LOG/plan.log 2>&1 || rc=$?; fi
  say "CAP $(tail -1 $LOG/plan.log)"
  [ $rc = 5 ] && { rm -f $CAP; stop "TIME CHECK FAIL (X5): T0 does not start; no look spent; back to the judge"; }
  [ $rc = 4 ] && { rm -f $CAP; stop "the cap does not fit (§10.2): back to the judge$( [ $mode = test ] && echo ' (before T0; no look spent)')"; }
  [ $rc = 0 ] || stop "plan rc=$rc"
}
timecheck() {  # X5: the time left to G6 covers the logged cap plus 24 h
  local rc=0 extra=(); dry && extra=(--dry-run --freeze-utc $FREEZE)
  $PY -I -B $SC timecheck --cap $CAP "${extra[@]}" >> $LOG/plan.log 2>&1 || rc=$?
  say "TIME CHECK $(tail -1 $LOG/plan.log)"
  [ $rc = 0 ] || stop "TIME CHECK FAIL (X5): T0 does not start; no look spent; back to the judge"
}
PARITY_PREDS=$R/outputs/c_attr_b1/out/at_qwen25vl_7b_ov_dev_b-ret-k8-first-T1-mvi-b1.preds.json
PARITY_LEDGER=$R/c_attr_score/led/ovb.jsonl
parity() {  # §7.1 scoring parity gate on the stored OV-dev-B run (no OV-test byte)
  if [ -s $PARITY_PREDS ] && [ -s $PARITY_LEDGER ]; then
    nice -n 19 $PY -I -B $SC parity --preds $PARITY_PREDS --ledger $PARITY_LEDGER >> $LOG/parity.log 2>&1 \
      || stop "scoring parity gate (§7.1)"
    say "STEP parity gate $(tail -1 $LOG/parity.log)"
  elif dry; then say "STEP parity gate (DRY: the pinned parity inputs are not in this tree; skipped)"
  else stop "the scoring parity inputs are missing (§6.4a)"; fi
}
dryrun() {  # step 0.4: every host mode starts, checks its inputs and stops before a model load (never an OV-test file)
  local m
  for m in qwen25vl_7b internvl3_8b aya_vision_8b; do set -- ${CFG[$m]}
    $LB $X decode --model $m --set $DRYSET --arm ret --k $1 --order $2 --tpl $3 --snapshot $(snap $m) --out-dir $O/dry \
      --c-lists $CL --images $DS --memory vi --batch1 --limit 2 --dry-run >> $LOG/dryrun.log 2>&1 || stop "dry run $m"
  done
  $T1 $X lmcap --set $DRYSET --variant ri --out-dir $O/dry --c-lists $CL --images $DS --memory vi --batch1 --limit 2 \
    --dry-run >> $LOG/dryrun.log 2>&1 || stop "dry run lmcap"
  if [ $MODE = test ]; then   # Q21: the OV-test inputs of §6.4a by name only; no file is present or opened
    $PY $X token --token $TOKEN --decision $DECISION --names-only >> $LOG/dryrun.log 2>&1 || stop "dry run: §6.4a names"
  fi
  say "STEP dry run of every host mode ok"
}
RUNNERS=${C_CONF_RUNNERS:-qwen25vl_7b lmcap internvl3_8b aya_vision_8b}
ordered() { local r; for r in qwen25vl_7b lmcap internvl3_8b aya_vision_8b; do [[ " $* " == *" $r "* ]] && echo $r; done; return 0; }

# ---------------------------------------------------------------- block 0 (§6.2, CPU)
if [ $MODE = block0 ]; then
  $PY $X inputs --block0 >> $LOG/inputs.log 2>&1 || stop "G0: an input is missing or its sha256 differs (0.1)"
  say "STEP 0.1 inputs ok"
  $FT $L block0 --out $O/c_conf_carve.json --lists-out $O/lists_ov_carve.json >> $LOG/lists.log 2>&1 \
    || stop "G0: carve, lists, K0 or K0 on the first-look form (0.2)"
  say "STEP 0.2 carve and lists ok: c_conf_carve.json sha256 $(sha256sum $O/c_conf_carve.json | cut -c1-64)"
  rc=0; $PY $L diag --lists $O/lists_ov_carve.json --out $O/diag_ov_carve.json >> $LOG/lists.log 2>&1 || rc=$?
  [ $rc = 3 ] && stop "G0b: refill share above 0.10 on ov_carve: STOP before any decode; back to the judge"
  [ $rc = 0 ] || stop "diagnostics rc=$rc (0.3)"
  say "STEP 0.3 perm diagnostics and refill gate ok"
  DRYSET=ov_carve; dryrun
  parity
  say "BLOCK 0 DONE"; exit 0
fi

# ---------------------------------------------------------------- rehearsal (§6.3)
if [ $MODE = rehearsal ]; then
  if [ ! -s $CAP ]; then
    D1_FILES=()
    for r in $(ordered $RUNNERS); do d1 $r; done
    plan rehearsal "${D1_PASS[@]}"
    dry || { say "PAUSE after D1: log the cap line ($CAP sha256 $(sha256sum $CAP | cut -c1-64)), then run rehearsal again"; exit 0; }
  fi
  KEEP=$(jget $CAP runners)
  say "BLOCK R: runners $KEEP under cap $(jget $CAP cap_s) s (order R.1, R.4, R.2, R.3)"
  for r in $(ordered $KEEP); do arms R_$r $r ov_carve; done
  finish
fi

# ---------------------------------------------------------------- test (§6.5): T.0, cap + time, parity, dry run, then T0
if [ ! -s $CAP ]; then
  [ ! -e $STAGE_T ] || stop "$STAGE_T exists before T.0: no OV-test byte before the pre-look steps (§6.5)"
  WANT=$(echo $(ordered $(jget $DECISION entered) lmcap))
  D1_FILES=()
  for r in $(ordered $RUNNERS); do if [[ " $WANT " == *" $r "* ]]; then d1 $r; fi; done
  plan test "${D1_PASS[@]}"
  say "CAP and TIME CHECK logged: runners $(jget $CAP runners); dropped $(jget $CAP dropped)"
  dry || { say "PAUSE after T.0: log the cap line and the time check ($CAP sha256 $(sha256sum $CAP | cut -c1-64)), then run test again"; exit 0; }
fi
if [ ! -s $O/T0_READY.json ]; then
  [ ! -e $STAGE_T ] || stop "$STAGE_T exists before the pre-look steps passed (§6.5)"
  timecheck
  parity
  $PY $L k0dev >> $LOG/k0dev.log 2>&1 || stop "K0 on OV-dev-B under T0's interpreter (§6.2 N8): T0 does not start; no look spent"
  DRYSET=ov_dev_b; dryrun
  timecheck   # at the moment T0 would start (X5)
  printf '{"cap_sha256": "%s", "utc": "%s"}\n' "$(sha256sum $CAP | cut -c1-64)" "$(ts)" > $O/T0_READY.json
  say "T0 READY: stage the OV-test files of §6.4a into $STAGE_T now; the second look begins at the first byte"
  if dry; then mkdir -p $STAGE_T; say "DRY: staging simulated by an empty folder (no OV-test byte)"
  else exit 0; fi
fi
look_stop() {  # a stop at or after T0 is the look (§6.5, G4): its rows are NOT RUN; no later session stages OV-test
  printf '{"look_stop": "%s", "utc": "%s"}\n' "$1" "$(ts)" > $O/LOOK_STOP.json
  say "LOOK STOP $1: the look has begun at T0; incomplete rows are NOT RUN; back to the judge for the wording only"
  finish 1
}
[ -e $O/LOOK_STOP.json ] && stop "a LOOK STOP is recorded: no later session may stage OV-test again"
if [ ! -s $LOG/T0.done ]; then
  { dry && [ -d $STAGE_T ]; } || [ -n "$(ls -A $STAGE_T 2>/dev/null)" ] \
    || stop "nothing is staged in $STAGE_T: T0 has not begun; no look spent (run call 3 only after staging)"
  say "T0 BEGINS: the second look begins with the OV-test files staged under the token"
  $PY $X stagecheck --token $TOKEN --decision $DECISION --dir $STAGE_T $(dry && echo --dry-run) >> $LOG/t0.log 2>&1 || look_stop "a staged file differs from §6.4a"
  $PY $L t0 --token $TOKEN --decision $DECISION --dir $STAGE_T --out $O/lists_ov_test.json $(dry && echo --dry-run) >> $LOG/t0.log 2>&1 \
    || look_stop "K0-T, the refill gate or the printed counts (G4, G0b)"
  ts > $LOG/T0.done; say "T0 ok"
fi
KEEP=$(jget $CAP runners)
say "BLOCK T: runners $KEEP under cap $(jget $CAP cap_s) s (order T.1, T.4, T.2, T.3)"
for r in $(ordered $KEEP); do arms T_$r $r ov_test; done
finish
