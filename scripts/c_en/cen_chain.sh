#!/bin/bash
# Laptop operator chain for C-EN (PREREG 2026-10-27_c_en §9, §11; the c_test_chain.sh pattern). One step per call:
#   hash          M3: hash-only fetch of coco_test, coco_kval, nocaps_val (no image written; before the prereg, CC-120 r2)
#   memory        M3: memory fetch (after the three records, PI-1026t)
#   pool|feats|build|smoke|coco|nocaps   M3: cen_job.sh block in tmux, wait, mirror, sha-confirm, then the deletions
#   cleanup <block> <reason>             a final stop: outputs back with a local sha list, the block's data deleted
# Around the blocks: after build the memory caption store is made here (cen_memory.py store) and uploaded; before
# coco/nocaps the reference subset is made here and the images are staged on M3 at their recorded sha (--stage);
# after smoke the memory images are deleted, after each test block its folder, after nocaps the caption store.
# Host and port are read from the backup config at run time, never stored here. Prints counts and shas only.
# Usage: cen_chain.sh <expected 40-hex HEAD> <step> [NoCaps captions file | block reason]
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd)
HEAD=${1:?HEAD}; STEP=${2:?step}; ARG=${3:-}; REASON=${4:-}
O=/root/outputs/c_en; DS=/root/ncs-data/datasets; ST=$DS/cen_store; OPLOG=$O/operator.log
MIR=$REPO/.session_backup/machines/M3/root/outputs/c_en
WORK=$REPO/.session_backup/2026-10-27/c_en; STG=$WORK/staging; LOCAL_LOG=$WORK/CHAIN.log
SSCD_LOCAL=$REPO/.session_backup/2026-10-22/c_stage1/sscd_disc_mixup.torchscript.pt
SSCD=9f26bd4c848cc19b73d2ae92eea6e04886f61a7b764ceb7a13aeee62e6a6db56
mkdir -p $STG $MIR
say() { echo "$(date -u +%FT%TZ) $*" | tee -a $LOCAL_LOG; }
die() {  # a feats stop is followed by its cleanup in the same session (CC-121 W5)
  say "CHAIN STOP $*"
  if [ -n "${CLEAN_ON_FAIL:-}" ]; then local b=$CLEAN_ON_FAIL; CLEAN_ON_FAIL=""; cleanup_block $b "auto after: $*"; fi
  exit 1; }
[ "$(git -C $REPO rev-parse HEAD)" = "$HEAD" ] || die "local HEAD is not $HEAD"
(cd $REPO && git diff --quiet HEAD -- scripts/c_en && sha256sum --quiet -c scripts/c_en/SHA256SUMS) \
  || die "local scripts/c_en differs from HEAD"
IFS=: read -r _ HOST PORT <<< "$(grep -o 'M3:[^" ]*' ~/.config/vsps/gpu_backup.sh | head -1)"
[ -n "${PORT:-}" ] || die "no M3 entry in the backup config"
SSH="ssh -o BatchMode=yes -o ConnectTimeout=30 -o ServerAliveInterval=30 -p $PORT root@$HOST"
SCP="scp -q -o BatchMode=yes -P $PORT"
remote() { $SSH "$1" 2>&1 | tee -a $LOCAL_LOG; return "${PIPESTATUS[0]}"; }
rec() { remote "mkdir -p $O && echo \"\$(date -u +%FT%TZ) $*\" >> $OPLOG" > /dev/null; }
put() { $SCP "$1" root@$HOST:"$2" || die "upload $(basename $1)"; }
[ "$(remote 'tr -d "[:space:]" < /root/.vsps_machine_id')" = m3 ] || die "the host is not m3"
[ "$(remote 'git -C /root/vsps rev-parse HEAD')" = "$HEAD" ] || die "M3 is not at $HEAD"
PY="cd /root/vsps && /root/venv-lb/bin/python scripts/c_en/cen_fetch.py"

tmux_run() {  # tmux_run NAME CMD: nothing else may run; wait for BLOCK DONE / JOB STOP / DONE NAME in the log
  local name=$1 cmd=$2 log=$O/chain_$1.log n0
  remote "[ -z \"\$(tmux ls 2>/dev/null)\" ]" || die "another tmux session is running on M3"
  n0=$($SSH "cat $log 2>/dev/null | wc -l") || die "M3 unreachable"
  rec "START C-EN $name head $HEAD"
  remote "mkdir -p $O && tmux new -d -s cen$name \"($cmd) >> $log 2>&1 && echo DONE $name >> $log || echo 'JOB STOP $name' >> $log\"" \
    || die "start $name"
  while true; do
    l=$($SSH "tail -n +$((n0 + 1)) $log | grep -E 'BLOCK DONE|JOB STOP|DONE $name' | tail -1" 2>/dev/null) \
      || { sleep 60; continue; }
    case "$l" in *"JOB STOP"*) die "$name: $l" ;; *DONE*) say "$name: $l"; break ;; esac
    $SSH "tmux has-session -t cen$name" 2>/dev/null; rc=$?
    [ $rc = 1 ] && ! $SSH "tail -n +$((n0 + 1)) $log | grep -qE 'BLOCK DONE|JOB STOP|DONE $name'" \
      && die "tmux cen$name is gone without a terminal line (reboot?); re-run the step to resume"
    sleep 120
  done
  while $SSH "tmux has-session -t cen$name" 2>/dev/null; do sleep 10; done
}
mirror() {  # mirror [SUMS]: copy back (no partials), then the block's SHA256SUMS must verify here
  rsync -a --exclude='*.partial.jsonl' -e "ssh -o BatchMode=yes -p $PORT" root@$HOST:$O/ $MIR/ || die "rsync"
  [ -z "${1:-}" ] || (cd $MIR && sha256sum --quiet -c $1) >> $LOCAL_LOG 2>&1 || die "mirror sha check ($1)"
  say "MIRROR OK ${1:-records}"
}
delete() {  # delete WHY PATH...: remove, check gone, record
  local why=$1; shift
  remote "rm -rf $* && for p in $*; do [ ! -e \$p ] || exit 1; done && echo \"\$(date -u +%FT%TZ) DELETED ($why) $*\" >> $OPLOG" \
    || die "delete $*"
  mirror; say "DELETED ($why): $*"
}
job() { tmux_run $1 "cd /root/vsps && bash scripts/c_en/cen_job.sh $HEAD $1"; mirror SHA256SUMS_$1; }
declare -A PIN=([coco_test]=614afa1b7cf63bde693fc9692b1699d47ba527d396b7a1216d031b1d50018fdf
  [coco_kval]=8c93f306f24588fb6e66eed0a8ba2ba97e61adf901ddf5ab614b37d5b677ee1c
  [nocaps_val]=fbbcd21ccd8e036e5d1a94bb0fa143538882ceec62ba76a1e9104d31f321cb33)
stage_ok() {  # stage_ok SET: CC-121 W9 prereg in HEAD on M3; W2 the mirrored record at its pin, logged
  local s=$1 h
  remote "cd /root/vsps && git cat-file -e HEAD:manuscript/prereg/2026-10-27_c_en/PREREG.md && grep ' manuscript/prereg/2026-10-27_c_en/PREREG.md\$' manuscript/prereg/2026-10-27_c_en/SHA256SUMS | sha256sum --quiet -c -" \
    || die "the C-EN prereg is not committed on M3; no --stage"
  mirror; h=$(sha256sum $MIR/fetch/$s.sha256.tsv | cut -c1-64)
  [ "$h" = "${PIN[$s]}" ] || die "$s record $h is not its pin ${PIN[$s]}"
  say "W2 $s record $h = pin"; rec "C-EN W2 $s record $h = pin"
}
cleanup_block() {  # cleanup_block BLOCK REASON: outputs back with a local sha list, then the block's data deleted
  local b=$1 why=$2 p
  mirror; (cd $MIR && find . -type f | sort | xargs -d '\n' sha256sum) > $WORK/cleanup_$b.sha256
  case $b in coco) p=$DS/cen_coco_test ;; nocaps) p="$DS/cen_nocaps_val $ST" ;;
    feats) p="$DS/cen_coco_kval $DS/cen_coco_test $DS/cen_nocaps_val" ;; *) p=$DS/cen_memory ;; esac
  delete "$why" $p
}
store() {  # store WHAT DEST [captions]: made here from the pinned files, uploaded, sha recorded on M3
  local what=$1 dest=$2 f=$STG/$1.json; shift 2
  (cd $REPO && python3 scripts/c_en/cen_memory.py store --what $what --memory $MIR/cen_memory.json "$@" --out $f) \
    >> $LOCAL_LOG 2>&1 || die "store $what"
  remote "mkdir -p $(dirname $dest)" > /dev/null; put $f $dest
  [ "$($SSH "sha256sum $dest" | cut -c1-64)" = "$(sha256sum $f | cut -c1-64)" ] || die "$what sha on M3"
  rec "C-EN staged $what $(sha256sum $f | cut -c1-64)"
}

case $STEP in
  hash) for s in coco_test coco_kval nocaps_val; do tmux_run hash_$s "$PY fetch --set $s --expect-head $HEAD"; done
        mirror; for s in coco_test coco_kval nocaps_val; do [ -e $MIR/fetch/$s.done.json ] || die "$s incomplete"; done ;;
  memory) for s in coco_test coco_kval nocaps_val; do [ -e $MIR/fetch/$s.done.json ] || die "$s record first"; done
          tmux_run memory "$PY fetch --set memory --expect-head $HEAD"; mirror ;;
  pool) job pool ;;
  feats) [ "$(sha256sum $SSCD_LOCAL | cut -c1-64)" = $SSCD ] || die "local SSCD weights"
         remote "[ -e /root/ncs-data/models/sscd_disc_mixup.torchscript.pt ]" > /dev/null \
           || put $SSCD_LOCAL /root/ncs-data/models/sscd_disc_mixup.torchscript.pt
         for s in coco_kval coco_test nocaps_val; do stage_ok $s; done  # the job stages each in turn (W2, W9)
         CLEAN_ON_FAIL=feats; job feats; CLEAN_ON_FAIL=""
         say "CPU wall so far: $(awk '$1 == "cpu" {s += $2} END {print s + 0}' $MIR/gpu_seconds.tsv) s" ;;
  build) job build; store memory $ST/cen_memory_captions.json ;;
  smoke) job smoke; delete "memory images after BUILD and SMOKE" $DS/cen_memory ;;
  coco) store coco_test $DS/cen_coco_test/refs.json
        stage_ok coco_test; tmux_run stage_coco "$PY fetch --set coco_test --stage --expect-head $HEAD"
        job coco; delete "COCO block done" $DS/cen_coco_test ;;
  nocaps) [ -f "$ARG" ] || die "pass the NoCaps captions file"
          [ -e $MIR/decide_coco_test.json ] && ! $SSH "[ -e $DS/cen_coco_test ]" || die "COCO is not decided and cleaned"
          store nocaps_val $DS/cen_nocaps_val/refs.json --captions "$ARG"
          stage_ok nocaps_val; tmux_run stage_nocaps "$PY fetch --set nocaps_val --stage --expect-head $HEAD"
          job nocaps; delete "NoCaps block done; caption store" $DS/cen_nocaps_val $ST ;;
  cleanup) [ -n "$REASON" ] || die "cleanup needs a block and a reason"
           $SSH "tmux ls 2>/dev/null | grep -q cen" && die "a C-EN tmux session is still running"
           cleanup_block $ARG "$REASON" ;;
  *) die "step must be hash, memory, pool, feats, build, smoke, coco, nocaps or cleanup" ;;
esac
say "CHAIN DONE $STEP"
