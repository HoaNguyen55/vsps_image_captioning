#!/bin/bash
# Laptop operator chain for C-2 (PREREG 2026-10-28_c2_ablation §1.2, §4, §10; CC-128 W9-W11; the c_test_chain.sh /
# cen_chain.sh pattern). One step per call:
#   dry-run            local only, no ssh: the inputs, their shas and the staging lists; prints counts and shas
#   stage              M3: restore outputs/c_stage2 and c_stage1/emb.npz from the mirror if absent (sha-checked);
#                      the two memory-caption sources; the 925 OV-dev-B images by list (sha 925/925) into
#                      datasets/openviic/images and the 1,836-key annotation subset (550cfe06)
#   run                M3: c2_job.sh in tmux c2, wait, mirror, sha-confirm (resume after a crash: run again)
#   cleanup <reason>   after BLOCK DONE or a final stop: outputs back with a local sha list, then the OV-dev-B images,
#                      the annotation subset and the memory sources removed and recorded (CC-099)
# Every M3 step refuses while any tmux session or any /root/outputs/*/RUNNING exists, and requires grl
# common.m3_clear. C-EN steps run only through cen_chain.sh; the queue follows CC-126 ruling 5; run needs ~5 h of
# usage headroom (W11).
# W10 operator rule: until decide.json exists, no agent opens a dec_*/score log, a preds file, the C-2 ledger or the
# stage-2 ledger, on M3 or in the mirror; monitoring reads only job.log, gpu_seconds.tsv, return codes and counts.
# Host and port are read from the backup config at run time, never stored here.
# Usage: c2_chain.sh <expected 40-hex HEAD> dry-run|stage|run|cleanup [reason]
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd)
HEAD=${1:?HEAD}; STEP=${2:?step}; REASON=${3:-}
O=/root/outputs/c2_ablation; DS=/root/ncs-data/datasets; OPLOG=$O/operator.log
MIRB=$REPO/.session_backup/machines/M3/root/outputs; MIR=$MIRB/c2_ablation
WORK=$REPO/.session_backup/2026-10-28/c2_ablation; STG=$WORK/staging; LOCAL_LOG=$WORK/CHAIN.log
DATA=$REPO/data/datasets; L=$REPO/manuscript/prereg/2026-10-22_c_stage1/lists.json
ANN=$REPO/.session_backup/2026-10-22/c_stage2/subsets/uit-openviic-annotation-dev.json
ANN_SHA=550cfe06b06084976e81286531f7f4e52bea717e29004c699ccaf1e48919bdff
EMB1=59e65f6f6432af97504c59c72fa07b644acbff26938e1365473fad659421f7c0
MEM="ktvic/train_data.json:72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f
openviic/uit-openviic-annotation-train.json:d757520e76b8490df6c7275c2beb8b3ecef0342635a436bea8c3cfd07eb49df0"
mkdir -p $STG $MIR
say() { echo "$(date -u +%FT%TZ) $*" | tee -a $LOCAL_LOG; }
die() { say "CHAIN STOP $*"; exit 1; }
lsha() { sha256sum "$1" | cut -c1-64; }
[ "$(git -C $REPO rev-parse HEAD)" = "$HEAD" ] || die "local HEAD is not $HEAD"
(cd $REPO && git diff --quiet HEAD -- scripts/c2_ablation && sha256sum --quiet -c scripts/c2_ablation/SHA256SUMS) \
  || die "local scripts/c2_ablation differs from HEAD"

local_inputs() {  # the OV-dev-B list from lists.json (id, file, sha; no caption), the sources and the mirrors
  python3 -c "import json,sys; [print(r[1]) for r in json.load(open(sys.argv[1]))['sets']['ov_dev_b']]" $L \
    > $STG/ov_dev_b.files
  python3 -c "import json,sys; [print(r[2] + '  ' + r[1]) for r in json.load(open(sys.argv[1]))['sets'][
    'ov_dev_b']]" $L > $STG/ov_dev_b.sha256
  [ "$(wc -l < $STG/ov_dev_b.files)" = 925 ] || die "not 925 OV-dev-B rows"
  (cd $DATA/openviic/images && sha256sum --quiet -c $STG/ov_dev_b.sha256) || die "a local OV-dev-B image differs"
  [ "$(lsha $ANN)" = $ANN_SHA ] || die "the 1,836-key annotation subset differs from 550cfe06"
  while IFS=: read -r f h; do [ "$(lsha $DATA/$f)" = $h ] || die "memory source $f"; done <<< "$MEM"
  (cd $MIRB/c_stage2 && sha256sum --quiet -c SHA256SUMS) || die "local mirror of outputs/c_stage2"
  [ "$(lsha $MIRB/c_stage1/emb.npz)" = $EMB1 ] || die "local mirror of c_stage1/emb.npz"
  say "LOCAL OK: 925 OV-dev-B images, annotation $ANN_SHA, 2 memory sources, c_stage2 mirror, emb.npz $EMB1"
}
if [ "$STEP" = dry-run ]; then
  bash -n "$0" || die "bash -n"
  local_inputs
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
rsha() { $SSH "sha256sum $1" | cut -c1-64; }
RS() { rsync -a -e "ssh -o BatchMode=yes -p $PORT" "$@"; }
[ "$(remote 'tr -d "[:space:]" < /root/.vsps_machine_id')" = m3 ] || die "the host is not m3"
[ "$(remote 'git -C /root/vsps rev-parse HEAD')" = "$HEAD" ] || die "M3 is not at $HEAD"
isolated() {  # W9 (a): no tmux session, no experiment lock, m3_clear
  remote "[ -z \"\$(tmux ls 2>/dev/null)\" ]" || die "a tmux session is running on M3"
  remote "[ -z \"\$(ls /root/outputs/*/RUNNING 2>/dev/null)\" ]" || die "a /root/outputs/*/RUNNING lock exists on M3"
  remote "cd /root/vsps && /root/venv-lb/bin/python -c \"import sys; sys.path.insert(0, 'scripts/grl'); \
import common; common.m3_clear()\"" > /dev/null || die "m3_clear refused (C-EN has priority)"
}
mirror() {
  RS --exclude='*.partial*' root@$HOST:$O/ $MIR/ || die "rsync"
  [ -z "${1:-}" ] || (cd $MIR && sha256sum --quiet -c $1) >> $LOCAL_LOG 2>&1 || die "mirror sha check ($1)"
  say "MIRROR OK ${1:-records}"
}
STAGED="$DS/openviic/images $DS/openviic/uit-openviic-annotation-dev.json $DS/ktvic/train_data.json \
$DS/openviic/uit-openviic-annotation-train.json"

case $STEP in
  stage)
    isolated; local_inputs
    if ! remote "cd /root/outputs/c_stage2 && sha256sum --quiet -c SHA256SUMS" > /dev/null; then  # W9 (c)
      RS --exclude='decide_final*' --exclude='verified*' $MIRB/c_stage2/ root@$HOST:/root/outputs/c_stage2/ \
        || die "restore outputs/c_stage2"
      remote "cd /root/outputs/c_stage2 && sha256sum --quiet -c SHA256SUMS" || die "restored c_stage2 sha check"
      rec "C-2 restored outputs/c_stage2 from the mirror (SHA256SUMS OK)"
    fi
    if [ "$(rsha /root/outputs/c_stage1/emb.npz)" != $EMB1 ]; then
      remote "mkdir -p /root/outputs/c_stage1"; put $MIRB/c_stage1/emb.npz /root/outputs/c_stage1/emb.npz
      [ "$(rsha /root/outputs/c_stage1/emb.npz)" = $EMB1 ] || die "restored emb.npz sha"
      rec "C-2 restored c_stage1/emb.npz $EMB1"
    fi
    for p in $STAGED; do remote "[ ! -e $p ]" || die "$p already on M3"; done
    remote "mkdir -p $DS/ktvic $DS/openviic/images $O/staging"
    while IFS=: read -r f h; do put $DATA/$f $DS/$f; [ "$(rsha $DS/$f)" = $h ] || die "$f sha on M3"; done <<< "$MEM"
    tar -C $DATA/openviic/images -cf - -T $STG/ov_dev_b.files | $SSH "tar -C $DS/openviic/images -xf -" \
      || die "copy the OV-dev-B images"
    put $STG/ov_dev_b.sha256 $O/staging/ov_dev_b.sha256
    remote "cd $DS/openviic/images && N=\$(ls | wc -l) && OK=\$(sha256sum -c $O/staging/ov_dev_b.sha256 2>/dev/null \
      | grep -c ': OK\$') && echo \"\$(date -u +%FT%TZ) C-2 OV-dev-B staged: \$N files, sha OK \$OK/925\" >> $OPLOG \
      && [ \$N = 925 ] && [ \$OK = 925 ]" || die "OV-dev-B sha check"
    put $ANN $DS/openviic/uit-openviic-annotation-dev.json
    [ "$(rsha $DS/openviic/uit-openviic-annotation-dev.json)" = $ANN_SHA ] || die "annotation sha on M3"
    rec "C-2 STAGED head $HEAD: 925 OV-dev-B, annotation $ANN_SHA, 2 memory sources"
    say "STAGE OK" ;;
  run)
    isolated
    ~/.config/vsps/usage_check.sh >> $LOCAL_LOG 2>&1 || die "usage_check: not enough headroom (~5 h needed, W11)"
    N0=$($SSH "cat $O/logs/job.log 2>/dev/null | wc -l") || die "M3 unreachable"
    rec "START C-2 tmux c2 head $HEAD"
    remote "cd /root/vsps && tmux new -d -s c2 \"bash scripts/c2_ablation/c2_job.sh $HEAD >> $O/job_tmux.log 2>&1\"" \
      || die "start c2"
    while true; do  # job.log lines only (W10)
      l=$($SSH "tail -n +$((N0 + 1)) $O/logs/job.log 2>/dev/null | grep -E 'BLOCK DONE|JOB STOP' | tail -1") \
        || { sleep 60; continue; }
      case "$l" in *"JOB STOP"*) mirror; die "$l" ;; *"BLOCK DONE"*) say "$l"; break ;; esac
      $SSH "tmux has-session -t c2" 2>/dev/null; rc=$?
      [ $rc = 1 ] && ! $SSH "tail -n +$((N0 + 1)) $O/logs/job.log | grep -qE 'BLOCK DONE|JOB STOP'" \
        && die "tmux c2 is gone without BLOCK DONE or JOB STOP (reboot?): run again to resume"
      sleep 300
    done
    while $SSH "tmux has-session -t c2" 2>/dev/null; do sleep 10; done
    mirror SHA256SUMS
    ~/.config/vsps/usage_check.sh >> $LOCAL_LOG 2>&1
    say "RUN DONE; next: cleanup" ;;
  cleanup)  # CC-099: outputs back with a local sha list, then the staged data removed (M3 holds no OV-dev-B after)
    [ -n "$REASON" ] || die "cleanup needs a reason (done, CAP_STOP, or the judge's ruling)"
    $SSH "tmux has-session -t c2" 2>/dev/null && die "tmux c2 is still running"
    mirror
    (cd $MIR && find . -type f | sort | xargs -d '\n' sha256sum) > $WORK/cleanup.sha256
    remote "rm -rf $STAGED && rmdir --ignore-fail-on-non-empty $DS/ktvic && for p in $STAGED; do [ ! -e \$p ] \
      || exit 1; done && echo \"\$(date -u +%FT%TZ) C-2 \
CLEANUP ($REASON): OV-dev-B images, annotation subset, memory sources removed\" >> $OPLOG" || die "cleanup delete"
    mirror
    say "CLEANUP DONE ($REASON): $(wc -l < $WORK/cleanup.sha256) files back" ;;
  *) die "step must be dry-run, stage, run or cleanup" ;;
esac
