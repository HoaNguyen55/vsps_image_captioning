#!/bin/bash
# Local operator chain for Paper C's test (PREREG §11.1-§11.3; CC-103 E4, E6; CC-103a X3). One block per call, in
# this order: e4, ov, xm on M3, then xmb locally on CPU. Each M3 block: stage by explicit list into the block's own
# folder, sha-check, record, run c_test_job.sh in tmux, wait, mirror and sha-confirm, delete the block's data on M3,
# and record times and shas. Before e4 it stages the two memory-caption sources the decode reads
# (C.memory_captions: KTVIC train_data.json, OpenViIC train annotation), as on M3 for stage 2; they are deleted with
# the last block. Host and port are read from the backup config at run time, never stored here. On M3 it writes only
# under /root/outputs/c_test and the block's $NCS_DATA/datasets folder. It prints counts and shas only (W10).
# CC-103b W5: `resume <block>` restarts a crashed block with the same HEAD and no staging; `cleanup <block> <reason>`
# ends a block that stopped for good (CAP_STOP, an E4 FAIL, or a stop the judge rules final): outputs back with a
# local sha list, then the block folder and the memory sources deleted and recorded.
# Usage: c_test_chain.sh <expected 40-hex HEAD> e4|ov|xm|xmb | resume e4|ov|xm | cleanup e4|ov|xm <reason>
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd)
HEAD=${1:?HEAD}; BLOCK=${2:?block}; ARG=${3:-}; REASON=${4:-}
O=/root/outputs/c_test; DS=/root/ncs-data/datasets; OPLOG=$O/operator.log
MIR=$REPO/.session_backup/machines/M3/root/outputs/c_test
WORK=$REPO/.session_backup/2026-10-26/c_test; STG=$WORK/staging; FINAL=$WORK/final; LOCAL_LOG=$WORK/CHAIN.log
DATA=$REPO/data/datasets; L=manuscript/prereg/2026-10-22_c_stage1/lists.json
TSV=$REPO/manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv
DEV299=$REPO/manuscript/prereg/2026-10-21_dev_pools/ktvic_dev299.tsv
MEM="ktvic/train_data.json openviic/uit-openviic-annotation-train.json"
mkdir -p $STG $FINAL $MIR
say() { echo "$(date -u +%FT%TZ) $*" | tee -a $LOCAL_LOG; }
die() { say "CHAIN STOP $*"; exit 1; }
[ "$(git -C $REPO rev-parse HEAD)" = "$HEAD" ] || die "local HEAD is not $HEAD"
git -C $REPO diff --quiet HEAD -- scripts/c_test && (cd $REPO && sha256sum --quiet -c scripts/c_test/SHA256SUMS) \
  || die "local scripts/c_test differs from HEAD (W5e)"
folder() { case $1 in e4) echo c_e4_dev299 ;; ov) echo c_ov_test ;; xm) echo c_xm_test2500 ;; *) die "block $1?" ;; esac; }
passed_e4() { for m in qwen25vl_7b internvl3_8b; do grep -q '"passed": true' $MIR/e4/e4_$m.json 2>/dev/null || return 1
  done; }

if [ "$BLOCK" = xmb ]; then  # §11.1 step (5): verified precision once, then the XM-b decide once; local CPU only
  cd $REPO || exit 1
  [ -e $MIR/decide_xm_m3.json ] && [ -e $MIR/xm_deleted.json ] || die "the XM block is not mirrored and cleaned up"
  (cd $MIR && sha256sum --quiet -c SHA256SUMS_xm) || die "mirror sha check (xm)"
  R=$MIR/runs; ids() { python3 scripts/c_test/ctest.py runs --set xm_test2500 "$@"; }
  NCS_DATA=$REPO/data python3 scripts/c_test/score_t.py verified --runs $(for r in $(ids --arm ret rand fix); do
      echo $R/$r.preds.json; done) --zs $R/$(ids --model qwen25vl_7b --arm zs).preds.json \
    $R/$(ids --model internvl3_8b --arm zs).preds.json --cache $MIR/guard/xm_test2500_internvl3_8b.cache.jsonl \
    --lists $L --labels data/xm3600/oiv7_labels.json --desc data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv \
    --ledger $FINAL/verified.jsonl >> $LOCAL_LOG 2>&1 || die "verified"
  python3 scripts/c_test/score_t.py decide --phase xmb --verified $FINAL/verified.jsonl \
    --xm-decide $MIR/decide_xm_m3.json --lists $L --out $FINAL/decide_xmb.json >> $LOCAL_LOG 2>&1 || die "decide xmb"
  say "XMB DONE $(cd $FINAL && sha256sum verified.jsonl decide_xmb.json | tr '\n' ' ')"
  exit 0
fi

IFS=: read -r _ HOST PORT <<< "$(grep -o 'M3:[^" ]*' ~/.config/vsps/gpu_backup.sh | head -1)"
[ -n "${PORT:-}" ] || die "no M3 entry in the backup config"
SSH="ssh -o BatchMode=yes -o ConnectTimeout=30 -o ServerAliveInterval=30 -p $PORT root@$HOST"
SCP="scp -q -o BatchMode=yes -P $PORT"
remote() { $SSH "$1" 2>&1 | tee -a $LOCAL_LOG; return "${PIPESTATUS[0]}"; }
rec() { remote "mkdir -p $O && echo \"\$(date -u +%FT%TZ) $*\" >> $OPLOG" > /dev/null; }
put() { $SCP "$1" root@$HOST:"$2" || die "upload $(basename $1)"; }

stage() {  # stage DIR SRC LIST SHALIST N: tar by the explicit list (names kept, exact case), then sha-check N/N
  local dir=$1 src=$2 list=$3 shas=$4 n=$5
  remote "[ ! -e $DS/$dir ] && mkdir -p $DS/$dir/images $O/staging" || die "$DS/$dir already exists"
  tar -C $src -cf - -T $list | $SSH "tar -C $DS/$dir/images -xf -" || die "copy into $dir"
  put $shas $O/staging/$(basename $shas)
  remote "cd $DS/$dir/images && N=\$(ls | wc -l) && OK=\$(sha256sum -c $O/staging/$(basename $shas) 2>/dev/null | \
    grep -c ': OK\$') && D=\$(sha256sum * | cut -c1-64 | sort -u | wc -l) && echo \"\$(date -u +%FT%TZ) C-TEST $dir \
    staged: \$N files, sha OK \$OK/$n, distinct sha \$D\" | tee -a $OPLOG && [ \$N = $n ] && [ \$OK = $n ]" \
    || die "$dir sha check"
}
start() {  # start BLOCK: the committed job in tmux ct<BLOCK>; nothing else may run on M3
  remote "[ -z \"\$(tmux ls 2>/dev/null)\" ]" || die "another tmux session is running on M3"
  N0=$($SSH "cat $O/job_$1.log 2>/dev/null | wc -l") || die "M3 unreachable"  # wait_block reads only newer lines
  rec "START C-TEST $1 block tmux ct$1 head $HEAD"
  remote "cd /root/vsps && tmux new -d -s ct$1 \"bash scripts/c_test/c_test_job.sh $HEAD $1 >> $O/job_$1.log 2>&1\" \
    && sleep 60 && tail -3 $O/job_$1.log" || die "start $1"
}
wait_block() {  # until job_<B>.log shows BLOCK DONE (return) or JOB STOP (die); progress lines only (W10)
  while true; do
    l=$($SSH "tail -n +$((N0 + 1)) $O/job_$1.log | grep -E 'BLOCK DONE $1 |JOB STOP' | tail -1" 2>/dev/null) \
      || { sleep 60; continue; }
    case "$l" in *"JOB STOP"*) die "$l" ;; *"BLOCK DONE"*) say "$l"; break ;; esac
    $SSH "tmux has-session -t ct$1" 2>/dev/null; rc=$?
    [ $rc = 1 ] && ! $SSH "tail -n +$((N0 + 1)) $O/job_$1.log | grep -qE 'BLOCK DONE $1 |JOB STOP'" \
      && die "tmux ct$1 is gone without BLOCK DONE or JOB STOP (W5d); resume or cleanup"
    sleep 300
  done
  while $SSH "tmux has-session -t ct$1" 2>/dev/null; do sleep 10; done
}
mirror() {  # mirror BLOCK: copy back, then the block's SHA256SUMS must verify locally
  rsync -a --exclude='*.partial.jsonl' -e "ssh -o BatchMode=yes -p $PORT" root@$HOST:$O/ $MIR/ || die "rsync"
  (cd $MIR && sha256sum --quiet -c SHA256SUMS_$1) >> $LOCAL_LOG 2>&1 || die "mirror sha check ($1)"
  say "MIRROR OK after $1: $(wc -l < $MIR/SHA256SUMS_$1) files sha OK"
}
delete() {  # delete BLOCK REASON PATH...: remove the block's data, check it is gone, write <block>_deleted.json
  local b=$1 why=$2; shift 2
  remote "rm -rf $* && for p in $*; do [ ! -e \$p ] || exit 1; done && printf '{\"block\": \"%s\", \"reason\": \"%s\", \
    \"utc\": \"%s\", \"removed\": \"%s\", \"datasets_left\": \"%s\"}\n' $b \"$why\" \$(date -u +%FT%TZ) \"$*\" \
    \"\$(ls $DS 2>/dev/null | tr '\n' ' ')\" > $O/${b}_deleted.json && cat $O/${b}_deleted.json >> $OPLOG" \
    || die "delete ($b)"
  for f in $O/${b}_deleted.json $OPLOG; do
    rsync -a -e "ssh -o BatchMode=yes -p $PORT" root@$HOST:$f $MIR/ || die "rsync the deletion record"
  done
  say "DELETED $b ($why): $*"
}
mem_paths() { for f in $MEM; do echo $DS/$f; done; }
finish() {  # finish BLOCK: run, wait, mirror and sha-confirm, then delete the block's data (the memory sources last)
  start $1; wait_block $1; mirror $1
  delete $1 done $DS/$(folder $1) $([ $1 = xm ] && mem_paths)
}

case $BLOCK in
  e4)  # CC-103a X3: memory sources, then dev299 by list into its own folder; no KTVIC test file
    for f in $MEM; do
      remote "[ ! -e $DS/$f ] && mkdir -p $DS/$(dirname $f)" || die "$DS/$f already exists"
      put $DATA/$f $DS/$f
      [ "$($SSH "sha256sum $DS/$f" | cut -c1-64)" = "$(sha256sum $DATA/$f | cut -c1-64)" ] || die "$f sha"
      rec "C-TEST memory source $f $(sha256sum $DATA/$f | cut -c1-64)"
    done
    cut -f2 $DEV299 > $STG/dev299.files; awk -F'\t' '{print $3"  "$2}' $DEV299 > $STG/dev299.sha256
    stage c_e4_dev299 $DATA/ktvic/images $STG/dev299.files $STG/dev299.sha256 299
    finish e4 ;;
  ov)  # E6 (1)-(2)
    passed_e4 && [ -e $MIR/e4_deleted.json ] || die "E4 has not passed on both backbones and been cleaned up (W5a)"
    cut -f1 $TSV > $STG/ov_test.files; awk -F'\t' '{print $2"  "$1}' $TSV > $STG/ov_test.sha256
    stage c_ov_test $DATA/openviic/images $STG/ov_test.files $STG/ov_test.sha256 2001
    ANN=$DATA/openviic/uit-openviic-annotation-test.json
    put $ANN $DS/c_ov_test/uit-openviic-annotation-test.json
    H=$(sha256sum $ANN | cut -c1-64)
    [ "$($SSH "sha256sum $DS/c_ov_test/uit-openviic-annotation-test.json" | cut -c1-64)" = $H ] || die "annotation sha"
    K=$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))))' $ANN)  # keys only, as the producer
    [ "$K" = 2001 ] || die "the OV-test annotation has $K keys, not 2,001"
    printf '{"utc": "%s", "ann": "uit-openviic-annotation-test.json", "ann_sha256": "%s", "ann_keys": %s}\n' \
      "$(date -u +%FT%TZ)" $H $K > $STG/staging_ov.json
    put $STG/staging_ov.json $O/staging_ov.json; rec "C-TEST OV annotation $H, $K keys (before the host check)"
    finish ov ;;
  xm)  # E6 (3)-(4), whatever the OV result (W9)
    [ -e $MIR/decide_ov.json ] && [ -e $MIR/ov_deleted.json ] || die "the OV block is not decided and cleaned up (W5a)"
    (cd $REPO && python3 scripts/c_test/ctest.py xm-subset --lists $L --xm-full $DATA/xm3600/full_data.json \
      --out $STG/xm_test2500_data.json) >> $LOCAL_LOG 2>&1 || die "XM reference subset"
    python3 -c "import json,sys; [print(r[1]) for r in json.load(open(sys.argv[1]))['sets']['xm_test2500']]" \
      $REPO/$L > $STG/xm_test2500.files
    python3 -c "import json,sys; [print(r[2] + '  ' + r[1]) for r in json.load(open(sys.argv[1]))['sets'][
      'xm_test2500']]" $REPO/$L > $STG/xm_test2500.sha256
    stage c_xm_test2500 $DATA/xm3600/images $STG/xm_test2500.files $STG/xm_test2500.sha256 2500
    put $STG/xm_test2500_data.json $DS/c_xm_test2500/xm_test2500_data.json
    rec "C-TEST XM reference subset $(sha256sum $STG/xm_test2500_data.json | cut -c1-64), 2500 keys"
    finish xm ;;
  resume)  # W5b: a crash; no staging, the block folder must be on M3 and its last START C-TEST head equal HEAD
    remote "[ -d $DS/$(folder $ARG) ]" || die "no $(folder $ARG) on M3; nothing to resume"
    h=$($SSH "grep -oE 'START C-TEST $ARG block tmux ct$ARG head [0-9a-f]{40}' $OPLOG | tail -1" | awk '{print $NF}')
    [ "$h" = "$HEAD" ] || die "the $ARG block started at ${h:-no HEAD}, not $HEAD"
    rec "RESUME C-TEST $ARG head $HEAD"; finish $ARG ;;
  cleanup)  # W5c: a final stop; outputs back with a sha list, then the block folder and the memory sources removed
    [ -n "$REASON" ] || die "cleanup needs a reason (CAP_STOP, E4 FAIL, or the judge's ruling)"
    folder $ARG > /dev/null
    $SSH "tmux has-session -t ct$ARG" 2>/dev/null && die "tmux ct$ARG is still running"
    rsync -a -e "ssh -o BatchMode=yes -p $PORT" root@$HOST:$O/ $MIR/ || die "rsync"
    (cd $MIR && find . -type f | sort | xargs -d '\n' sha256sum) > $WORK/cleanup_$ARG.sha256
    say "CLEANUP $ARG ($REASON): $(wc -l < $WORK/cleanup_$ARG.sha256) files back, sha list cleanup_$ARG.sha256"
    delete $ARG "$REASON" $DS/$(folder $ARG) $(mem_paths) ;;
  *) die "block must be e4, ov, xm, xmb, resume or cleanup" ;;
esac
say "CHAIN DONE $BLOCK"
