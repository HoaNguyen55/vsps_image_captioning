#!/bin/bash
# Laptop operator chain for B-2 (PREREG 2026-10-28_b2_external §5; the c2_chain.sh pattern). One step per call:
#   dry-run            local only, no ssh: the three image lists (id, file, sha256; no caption), C-EN overlap 0
#   stage              M3: refuses on any tmux session, any /root/outputs/*/RUNNING or a failed m3_clear; takes the
#                      B-2 lock (held until cleanup), then stages the KTVIC test (558) and OpenViIC test (2,001)
#                      images by list into /root/ncs-data/b2_stage (sha-checked) and the UIT-ViIC id/url list
#   run                M3: b2_job.sh in tmux b2, wait, mirror, sha-confirm (resume after a crash: run again)
#   cleanup <reason>   outputs back with a local sha list; /root/ncs-data/b2_stage (test images, snapshots) removed and
#                      checked absent; m3_clear re-run; the lock removed last
# Monitoring rule: until scores.json exists, no agent opens a preds file or a dec_* log, on M3 or in the mirror;
# monitoring reads only job.log, gpu_seconds.tsv, return codes and counts. Host and port are read at run time.
# Operator rule (CC-132 W8): no C-EN step and no other M3 chain starts while /root/outputs/b2_external/RUNNING exists.
# Usage: b2_chain.sh <expected 40-hex HEAD> dry-run|stage|run|cleanup [reason]
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd)
HEAD=${1:?HEAD}; STEP=${2:?step}; REASON=${3:-}
O=/root/outputs/b2_external; ST=/root/ncs-data/b2_stage; LOCK=$O/RUNNING; OPLOG=$O/operator.log
MIRB=$REPO/.session_backup/machines/M3/root/outputs; MIR=$MIRB/b2_external
WORK=$REPO/.session_backup/2026-10-28/b2_external; LISTS=$WORK/lists; LOCAL_LOG=$WORK/CHAIN.log
DATA=$REPO/data/datasets
LIST_SHA="ktvic:0a33004749ae47d0df8de22176d4fcc98e2be24b3bed664e18b65f18d9673ec2
openviic:ce0f277f244df3cf692fc2f1ae5da2004fcb426537e735f999eeade6005b4858
uitviic:4974b4c9c0e5d88bd2441fefc73662c853e8c1e9974aa43a730532902197ed4f"  # CC-132 W7
mkdir -p $WORK $MIR
say() { echo "$(date -u +%FT%TZ) $*" | tee -a $LOCAL_LOG; }
die() { say "CHAIN STOP $*"; exit 1; }
[ "$(git -C $REPO rev-parse HEAD)" = "$HEAD" ] || die "local HEAD is not $HEAD"
(cd $REPO && git diff --quiet HEAD -- scripts/b2_external && sha256sum --quiet -c scripts/b2_external/SHA256SUMS) \
  || die "local scripts/b2_external differs from HEAD"

local_lists() {
  [ -e $LISTS/ktvic.tsv ] || python3 $REPO/scripts/b2_external/b2.py lists --data $DATA --cen $MIRB/c_en/fetch \
    --out $LISTS >> $LOCAL_LOG 2>&1 || die "b2.py lists (counts or C-EN overlap)"
  while IFS=: read -r s h; do [ "$(sha256sum < $LISTS/$s.tsv | cut -c1-64)" = $h ] || die "$s list differs from its pin"
  done <<< "$LIST_SHA"
  say "LOCAL OK: lists pinned 3/3 (ktvic 558, openviic 2001, uitviic 231; no caption), C-EN overlap checked at build"
}
if [ "$STEP" = dry-run ]; then
  bash -n "$0" && bash -n $REPO/scripts/b2_external/b2_job.sh || die "bash -n"
  local_lists
  say "DRY-RUN OK (no ssh): next steps stage, run, cleanup"
  exit 0
fi

IFS=: read -r _ HOST PORT <<< "$(grep -o 'M3:[^" ]*' ~/.config/vsps/gpu_backup.sh | head -1)"
[ -n "${PORT:-}" ] || die "no M3 entry in the backup config"
SSH="ssh -o BatchMode=yes -o ConnectTimeout=30 -o ServerAliveInterval=30 -p $PORT root@$HOST"
SCP="scp -q -o BatchMode=yes -P $PORT"
remote() { $SSH "$1" 2>&1 | tee -a $LOCAL_LOG; return "${PIPESTATUS[0]}"; }
rec() { remote "mkdir -p $O && echo \"\$(date -u +%FT%TZ) $*\" >> $OPLOG" > /dev/null; }
put() { $SCP "$1" root@$HOST:"$2" || die "upload $(basename $1)"; }
RS() { rsync -a -e "ssh -o BatchMode=yes -p $PORT" "$@"; }
[ "$(remote 'tr -d "[:space:]" < /root/.vsps_machine_id')" = m3 ] || die "the host is not m3"
[ "$(remote 'git -C /root/vsps rev-parse HEAD')" = "$HEAD" ] || die "M3 is not at $HEAD"
clear_cen() {
  remote "cd /root/vsps && /root/venv-lb/bin/python -c \"import sys; sys.path.insert(0, 'scripts/grl'); \
import common; common.m3_clear()\"" > /dev/null || die "m3_clear refused (C-EN has priority)"
}
mirror() {
  RS --exclude='*.partial*' root@$HOST:$O/ $MIR/ || die "rsync"
  [ -z "${1:-}" ] || (cd $MIR && sha256sum --quiet -c $1) >> $LOCAL_LOG 2>&1 || die "mirror sha check ($1)"
  say "MIRROR OK ${1:-records}"
}

case $STEP in
  stage)
    remote "[ -z \"\$(tmux ls 2>/dev/null)\" ]" || die "a tmux session is running on M3"
    remote "[ -z \"\$(ls /root/outputs/*/RUNNING 2>/dev/null)\" ]" || die "a /root/outputs/*/RUNNING lock exists on M3"
    clear_cen; local_lists
    remote "[ ! -e $ST ]" || die "$ST already exists on M3"
    remote "mkdir -p $O && set -o noclobber && echo \"b2_chain stage $HEAD\" > $LOCK" || die "take the B-2 lock"
    rec "B-2 LOCK taken by stage, head $HEAD"
    remote "mkdir -p $ST/lists $ST/images/ktvic $ST/images/openviic $ST/hf"
    for s in ktvic openviic uitviic; do  # CC-132a W10: a for loop, so ssh cannot eat the list of names
      h=$(grep "^$s:" <<< "$LIST_SHA" | cut -d: -f2); put $LISTS/$s.tsv $ST/lists/$s.tsv
      [ "$(remote "sha256sum < $ST/lists/$s.tsv" < /dev/null | cut -c1-64)" = "$h" ] || die "$s list sha on M3"; done
    for s in ktvic openviic; do
      cut -f2 $LISTS/$s.tsv | tar -C $DATA/$s/images -cf - -T - | $SSH "tar -C $ST/images/$s -xf -" \
        || die "copy the $s test images"
      n=$(wc -l < $LISTS/$s.tsv)
      remote "cd $ST/images/$s && [ \$(ls | wc -l) = $n ] && awk -F'\t' '{print \$3\"  \"\$2}' $ST/lists/$s.tsv \
        | sha256sum --quiet -c -" || die "$s sha check on M3"
    done
    rec "B-2 STAGED head $HEAD: ktvic 558, openviic 2001 test images (sha OK), uitviic id/url list"
    say "STAGE OK" ;;
  run)
    remote "[ -e $LOCK ]" || die "no B-2 lock on M3: stage first"
    remote "[ -z \"\$(tmux ls 2>/dev/null)\" ]" || die "a tmux session is running on M3"
    clear_cen
    ~/.config/vsps/usage_check.sh >> $LOCAL_LOG 2>&1 || die "usage_check: not enough headroom"
    N0=$($SSH "cat $O/logs/job.log 2>/dev/null | wc -l") || die "M3 unreachable"
    rec "START B-2 tmux b2 head $HEAD"
    remote "cd /root/vsps && tmux new -d -s b2 \"bash scripts/b2_external/b2_job.sh $HEAD >> $O/job_tmux.log 2>&1\"" \
      || die "start b2"
    while true; do  # job.log lines only
      l=$($SSH "tail -n +$((N0 + 1)) $O/logs/job.log 2>/dev/null | grep -E 'BLOCK DONE|JOB STOP' | tail -1") \
        || { sleep 60; continue; }
      case "$l" in *"JOB STOP"*) mirror; die "$l" ;; *"BLOCK DONE"*) say "$l"; break ;; esac
      $SSH "tmux has-session -t b2" 2>/dev/null; rc=$?
      [ $rc = 1 ] && ! $SSH "tail -n +$((N0 + 1)) $O/logs/job.log | grep -qE 'BLOCK DONE|JOB STOP'" \
        && die "tmux b2 is gone without BLOCK DONE or JOB STOP (reboot?): run again to resume"
      sleep 120
    done
    while $SSH "tmux has-session -t b2" 2>/dev/null; do sleep 10; done
    mirror SHA256SUMS
    say "RUN DONE; next: cleanup" ;;
  cleanup)
    [ -n "$REASON" ] || die "cleanup needs a reason (done, CAP_STOP, or the judge's ruling)"
    $SSH "tmux has-session -t b2" 2>/dev/null && die "tmux b2 is still running"
    mirror
    (cd $MIR && find . -type f | sort | xargs -d '\n' sha256sum) > $WORK/cleanup.sha256
    remote "rm -rf $ST && [ ! -e $ST ]" || die "cleanup delete"
    clear_cen
    remote "rm -f $LOCK && echo \"\$(date -u +%FT%TZ) B-2 CLEANUP ($REASON): $ST removed, m3_clear OK, lock \
released\" >> $OPLOG" || die "release the lock"
    mirror
    say "CLEANUP DONE ($REASON): $(wc -l < $WORK/cleanup.sha256) files back" ;;
  *) die "step must be dry-run, stage, run or cleanup" ;;
esac
