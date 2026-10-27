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
# Machine (PI-1026ai, CC-132): GPU=m3|m4 is required and selects the backup-config entry, the machine-id check,
# the mirror folder (.session_backup/machines/M3|M4/) and the messages. GPU=m3 behaves as before. GPU=m4 (dev-only,
# never holds test images): m3_clear's C-EN record requirement is skipped (no cen_ set and no C-EN process still
# refuse), and stage/run add a scan of $NCS_DATA/datasets that refuses any test-split path and any file whose sha is
# a test-side sha (exclusion.json + C-EN's three test-side records mirrored here), beyond the allowed list.
# Usage: GPU=m3|m4 c2_chain.sh <expected 40-hex HEAD> dry-run|stage|run|cleanup [reason]
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd)
HEAD=${1:?HEAD}; STEP=${2:?step}; REASON=${3:-}
GPU=${GPU:?set GPU=m3 or GPU=m4 (PI-1026ai)}
case $GPU in m3|m4) ;; *) echo "GPU must be m3 or m4, not $GPU"; exit 1 ;; esac
MNAME=${GPU^^}  # M3 or M4: the backup-config entry, the mirror folder, the messages
O=/root/outputs/c2_ablation; DS=/root/ncs-data/datasets; OPLOG=$O/operator.log
MIRB=$REPO/.session_backup/machines/M3/root/outputs  # stage-1/2 sources: M3 outputs
MIR=$REPO/.session_backup/machines/$MNAME/root/outputs/c2_ablation
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
  (cd $DATA && sha256sum ktvic/train_data.json openviic/uit-openviic-annotation-train.json) > $STG/c2_json.sha256
  sha256sum $ANN >> $STG/c2_json.sha256
  say "LOCAL OK: 925 OV-dev-B images, annotation $ANN_SHA, 2 memory sources, c_stage2 mirror, emb.npz $EMB1"
}
test_side_list() {  # GPU=m4 (PI-1026ai): every test-side image sha: exclusion.json, C-EN's three test-side records
  # and lists.json refuse.image_sha256 minus its dev parts (CC-133 W2, CC-134); every source count must be exact
  # (CC-133 W3: a truncated rsync --partial record would shrink the list silently)
  python3 - $REPO $STG/test_side.sha256 <<'PY' || die "test-side sha list: a source count is not exact (CC-133 W3)"
import json, re, sys
r = sys.argv[1]
ex = json.load(open(f"{r}/manuscript/prereg/2026-10-21_dev_pools/exclusion.json"))["image_sha256"]
src = {"exclusion.json": set().union(*map(set, ex.values()))}
for s in ("coco_test", "coco_kval", "nocaps_val"):
    rec = f"{r}/.session_backup/machines/M3/root/outputs/c_en/fetch/{s}.sha256.tsv"
    src[s] = set(re.findall(r"\b[0-9a-f]{64}\b", open(rec).read()))
lists = json.load(open(f"{r}/manuscript/prereg/2026-10-22_c_stage1/lists.json"))
refuse = set(lists["refuse"]["image_sha256"])  # stage 1's memory-refusal list: test sets AND C's own dev-B sets
dev = {x[2] for k in ("ov_dev_b", "xm_dev500") for x in lists["sets"][k]}  # CC-134: its dev parts, from lists.json
src["lists.refuse_test_side"] = refuse - dev
want = {"exclusion.json": 5180, "coco_test": 5000, "coco_kval": 5000, "nocaps_val": 4500,
        "lists.refuse_test_side": 5175}
if len(refuse) != 6599 or len(refuse & dev) != 1424:  # 924 OV-dev-B + 500 XM-dev500 shas, exact
    sys.exit(1)
out = set().union(*src.values())
got = {k: len(v) for k, v in src.items()}
print(" ".join(f"{k}={n}" for k, n in got.items()), f"union={len(out)}")
if got != want or len(out) != 21336:
    sys.exit(1)
open(sys.argv[2], "w").write("".join(f"{h}\n" for h in sorted(out)))
PY
  say "test-side sha list: $(wc -l < $STG/test_side.sha256) shas (5 sources exact)"
}
allowed_list() { : > $STG/allowed.sha256; }  # C-2 on M4: no test-side sha is allowed
STAGED_SHAS="$STG/ov_dev_b.sha256 $STG/c2_json.sha256"  # 925 OV-dev-B images; the 3 staged json files
staged_vs_test_side() {  # CC-134: the staged image shas may hit the test-side union only at the allowed shas
  python3 - $STG/test_side.sha256 $STG/allowed.sha256 $STAGED_SHAS <<'PY' \
    || die "the staged shas intersect the test-side union beyond the allowed list (CC-134)"
import sys
test = set(open(sys.argv[1]).read().split())
allowed = {x.split()[0] for x in open(sys.argv[2]) if x.strip()}
staged = {x.split()[0] for f in sys.argv[3:] for x in open(f) if x.strip()}
hits = staged & test
print(f"staged {len(staged)} shas, test-side hits {len(hits)}, allowed {len(allowed)}")
sys.exit(0 if hits == allowed else 1)
PY
  say "STAGED vs TEST-SIDE OK: hits = allowed ($(wc -l < $STG/allowed.sha256))"
}
if [ "$STEP" = dry-run ]; then
  bash -n "$0" || die "bash -n"
  local_inputs
  [ $GPU = m3 ] || { allowed_list; test_side_list; staged_vs_test_side
                     say "M4 lists: $(wc -l < $STG/allowed.sha256) allowed"; }
  say "DRY-RUN OK (no ssh): next steps stage, run, cleanup"
  exit 0
fi

IFS=: read -r _ HOST PORT <<< "$(grep -o "$MNAME:[^\" ]*" ~/.config/vsps/gpu_backup.sh | head -1)"
[ -n "${PORT:-}" ] || die "no $MNAME entry in the backup config"
SSH="ssh -o BatchMode=yes -o ConnectTimeout=30 -o ServerAliveInterval=30 -p $PORT root@$HOST"
SCP="scp -q -o BatchMode=yes -P $PORT"
remote() { $SSH "$1" 2>&1 | tee -a $LOCAL_LOG; return "${PIPESTATUS[0]}"; }
rec() { remote "mkdir -p $O && echo \"\$(date -u +%FT%TZ) $*\" >> $OPLOG" > /dev/null; }
put() { $SCP "$1" root@$HOST:"$2" < /dev/null || die "upload $(basename $1)"; }
rsha() { $SSH "sha256sum $1" < /dev/null | cut -c1-64; }  # CC-134: never reads the caller's stdin
RS() { rsync -a -e "ssh -o BatchMode=yes -p $PORT" "$@"; }
[ "$(remote 'tr -d "[:space:]" < /root/.vsps_machine_id')" = $GPU ] || die "the host is not $GPU"
[ "$(remote 'git -C /root/vsps rev-parse HEAD')" = "$HEAD" ] || die "$MNAME is not at $HEAD"
test_scan() {  # GPU=m4: no test-split path and no test-side sha under $DS, except the allowed (sha path) lines
  allowed_list; test_side_list; staged_vs_test_side; remote "mkdir -p $O/staging"
  put $STG/test_side.sha256 $O/staging/test_side.sha256; put $STG/allowed.sha256 $O/staging/allowed.sha256
  remote "[ -z \"\$(find $DS \( -iname 'test*' -o -iname '*-test*' -o -iname '*_test*' -o -name 'cen_*' \
    -o -iname 'xm3600*' -o -name 'c_ov_test' -o -name 'c_xm_test2500' \) 2>/dev/null)\" ]" \
    || die "a test-split path on $MNAME"
  remote "mkdir -p $O/staging && cd $O/staging && find $DS -type f -print0 | xargs -0 -r sha256sum > ds.sha256 \
    && awk 'NR==FNR {t[\$1]; next} (\$1 in t)' test_side.sha256 ds.sha256 | sort > hits.sha256 \
    && sort allowed.sha256 | cmp -s - hits.sha256" \
    || die "a test-side sha under $DS on $MNAME (beyond the allowed list)"
  say "TEST SCAN OK on $MNAME: no test-split path, test-side sha hits = allowed list ($(wc -l < $STG/allowed.sha256))"
}
isolated() {  # W9 (a): no tmux session, no experiment lock, m3_clear (M3) or no C-EN trace (M4)
  remote "[ -z \"\$(tmux ls 2>/dev/null)\" ]" || die "a tmux session is running on $MNAME"
  remote "[ -z \"\$(ls /root/outputs/*/RUNNING 2>/dev/null)\" ]" \
    || die "a /root/outputs/*/RUNNING lock exists on $MNAME"
  if [ $GPU = m3 ]; then
    remote "cd /root/vsps && /root/venv-lb/bin/python -c \"import sys; sys.path.insert(0, 'scripts/grl'); \
import common; common.m3_clear()\"" > /dev/null || die "m3_clear refused (C-EN has priority)"
  else  # M4 holds no C-EN data: no record requirement; still no cen_ set and no C-EN process (PI-1026ai)
    remote "[ -z \"\$(ls -d $DS/cen_* 2>/dev/null)\" ] && ! pgrep -f 'scripts/c_e[n]/' > /dev/null" \
      || die "a C-EN set or process on $MNAME"
  fi
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
    for p in $STAGED; do remote "[ ! -e $p ]" || die "$p already on $MNAME"; done
    remote "mkdir -p $DS/ktvic $DS/openviic/images $O/staging"
    n=0; while IFS=: read -r f h; do put $DATA/$f $DS/$f; [ "$(rsha $DS/$f)" = $h ] || die "$f sha on $MNAME"
      n=$((n + 1)); done <<< "$MEM"
    [ $n = 2 ] || die "not 2 memory sources uploaded (CC-134)"
    tar -C $DATA/openviic/images -cf - -T $STG/ov_dev_b.files | $SSH "tar -C $DS/openviic/images -xf -" \
      || die "copy the OV-dev-B images"
    put $STG/ov_dev_b.sha256 $O/staging/ov_dev_b.sha256
    remote "cd $DS/openviic/images && N=\$(ls | wc -l) && OK=\$(sha256sum -c $O/staging/ov_dev_b.sha256 2>/dev/null \
      | grep -c ': OK\$') && echo \"\$(date -u +%FT%TZ) C-2 OV-dev-B staged: \$N files, sha OK \$OK/925\" >> $OPLOG \
      && [ \$N = 925 ] && [ \$OK = 925 ]" || die "OV-dev-B sha check"
    put $ANN $DS/openviic/uit-openviic-annotation-dev.json
    [ "$(rsha $DS/openviic/uit-openviic-annotation-dev.json)" = $ANN_SHA ] || die "annotation sha on $MNAME"
    rec "C-2 STAGED head $HEAD: 925 OV-dev-B, annotation $ANN_SHA, 2 memory sources"
    [ $GPU = m3 ] || test_scan
    say "STAGE OK" ;;
  run)
    isolated; [ $GPU = m3 ] || test_scan
    ~/.config/vsps/usage_check.sh >> $LOCAL_LOG 2>&1 || die "usage_check: not enough headroom (~5 h needed, W11)"
    N0=$($SSH "cat $O/logs/job.log 2>/dev/null | wc -l") || die "$MNAME unreachable"
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
