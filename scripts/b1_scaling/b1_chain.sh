#!/bin/bash
# Laptop operator chain for B-1 (PREREG 2026-10-28_b1_scaling §1.2, §4, §10; CC-128 W9-W11; the cen_chain.sh /
# c_test_chain.sh pattern). One step per call:
#   dry-run            local only, no ssh: the inputs, their shas and the staging lists; prints counts and shas
#   stage              M3: KTVIC train_data.json + the 3,769 train images only (by list, sha 3769/3769), no KTVIC test
#                      file or test-sha image under datasets/ktvic* except the 2 named twins (CC-130), the
#                      ktvic_dev json-dir, s5_preds/ (3 files),
#                      the n2 p1dev_s42 adapter (227a3312), the .venv resume hook (05466ef5)
#   run                M3: b1_job.sh in tmux b1, wait, mirror, sha-confirm (resume after a crash: run again)
#   cleanup <reason>   after BLOCK DONE or a final stop: outputs back with a local sha list, then the hook (first),
#                      datasets/ktvic and datasets/ktvic_dev removed and recorded (CC-099, CC-130 W4), then the
#                      staged n2 p1dev_s42 adapter (Amendment 3: removed only if its sha is 227a3312; stage uploads it
#                      fresh and refuses an existing copy). Idempotent: run it again to clear a leftover adapter.
# Every M3 step refuses while any tmux session or any /root/outputs/*/RUNNING exists, and requires grl
# common.m3_clear (C-EN test-side records complete, no cen_ set staged, no C-EN process). C-EN steps run only through
# cen_chain.sh; the queue follows CC-126 ruling 5; run needs ~12 h of usage headroom (W11).
# Hook rule (CC-130 W4): while the .venv resume hook (vsps_resume_hook.py + .pth, Amendment 4) exists on M3, no evaluate.py or train_stage2.py process starts
# outside b1_job.sh; the hook lives only between stage and cleanup (cleanup removes it first), and the staged KTVIC
# images make every grl common.guard refuse in that window (CC-130 r5). Test twins: the two KTVIC train images whose
# bytes equal KTVIC test images (train 3589 = test 1335, train 7511 = test 507) are staged as train data and exempted
# by name, path and sha (b1.TRAIN_TEST_TWINS; CC-130 amends CC-128 W9(b)); any other test-sha hit STOPs.
# W10 operator rule: until decide.json exists, no agent opens dec_*.log, a result JSON or a preds file, on M3 or in
# the mirror; monitoring reads only job.log, gpu_seconds.tsv, return codes and counts. This chain reads job.log only.
# Host and port are read from the backup config at run time, never stored here.
# Machine (PI-1026ai, CC-132): GPU=m3|m4 is required and selects the backup-config entry, the machine-id check,
# the mirror folder (.session_backup/machines/M3|M4/) and the messages. GPU=m3 behaves as before. GPU=m4 (dev-only,
# never holds test images): m3_clear's C-EN record requirement is skipped (no cen_ set and no C-EN process still
# refuse), and stage/run add a scan of $NCS_DATA/datasets that refuses any test-split path and any file whose sha is
# a test-side sha (exclusion.json + C-EN's three test-side records mirrored here), beyond the allowed list.
# Usage: GPU=m3|m4 b1_chain.sh <expected 40-hex HEAD> dry-run|stage|run|cleanup [reason]
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd)
HEAD=${1:?HEAD}; STEP=${2:?step}; REASON=${3:-}
GPU=${GPU:?set GPU=m3 or GPU=m4 (PI-1026ai)}
case $GPU in m3|m4) ;; *) echo "GPU must be m3 or m4, not $GPU"; exit 1 ;; esac
MNAME=${GPU^^}  # M3 or M4: the backup-config entry, the mirror folder, the messages
O=/root/outputs/b1_scaling; DS=/root/ncs-data/datasets; RUNS=/root/ncs-data/runs; OPLOG=$O/operator.log
MIR=$REPO/.session_backup/machines/$MNAME/root/outputs/b1_scaling
WORK=$REPO/.session_backup/2026-10-28/b1_scaling; STG=$WORK/staging; LOCAL_LOG=$WORK/CHAIN.log
DATA=$REPO/data/datasets; TRAIN=$DATA/ktvic/train_data.json
TRAIN_SHA=72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f
S5DIR=$REPO/.session_backup/machines/O-2308423/root/outputs/t3_4_s5_data_scaling
ADAPTER=$REPO/.session_backup/machines/n2/ncs-data/runs/p1dev_s42
AD_SHA=227a3312a18cf69b355c20311ff1228167b2af1436e0cb443055dfdfcd40c5c3
AD_CFG=93f042284aea64fcdf831590c592a7459849632dcb3ee4448b379177b7a298c5
HOOK=/root/vsps/.venv/lib/python3.10/site-packages/vsps_resume_hook.py; PTH=${HOOK%.py}.pth  # Amendment 4: /usr/lib/python3.10/sitecustomize.py shadows a venv sitecustomize
HOOK_SHA=05466ef5ed3bef2b732ccd01f530a8c977c4c822ef8619b0238f562fb11e5895
S5_PREDS="p1dev_s42_f25-dev300-short.preds.json:b0ecf307c42486d4558eb1a2cf97cad01aa6ab52292ee7627fd028fbbb5c6b43
p1dev_s42_f50-dev300-short.preds.json:a394053d8823ae09c4885358facda7aabb6c998a0ec1c0ba405e0e29f8db551d
p1dev_s42_redecode-dev300-short.preds.json:1e183383e91daf32f4683fbea2bdb09d24b7deba956343ca16ef332014cba84b"
mkdir -p $STG $MIR
say() { echo "$(date -u +%FT%TZ) $*" | tee -a $LOCAL_LOG; }
die() { say "CHAIN STOP $*"; exit 1; }
lsha() { sha256sum "$1" | cut -c1-64; }
[ "$(git -C $REPO rev-parse HEAD)" = "$HEAD" ] || die "local HEAD is not $HEAD"
(cd $REPO && git diff --quiet HEAD -- scripts/b1_scaling && sha256sum --quiet -c scripts/b1_scaling/SHA256SUMS) \
  || die "local scripts/b1_scaling differs from HEAD"

local_inputs() {  # the staging lists (file names from train_data.json `images`; no caption is read) and every sha
  [ "$(lsha $TRAIN)" = $TRAIN_SHA ] || die "train_data.json differs from 72ee9b57"
  python3 -c "import json,sys; [print(i['filename']) for i in json.load(open(sys.argv[1]))['images']]" $TRAIN \
    > $STG/ktvic_train.files
  [ "$(wc -l < $STG/ktvic_train.files)" = 3769 ] || die "not 3,769 KTVIC train images"
  (cd $DATA/ktvic/images && xargs -d '\n' sha256sum < $STG/ktvic_train.files) > $STG/ktvic_train.sha256 \
    || die "a KTVIC train image is missing locally"
  PYTHONDONTWRITEBYTECODE=1 python3 - $REPO $STG/ktvic_train.sha256 <<'PY' \
    || die "the train images' KTVIC-test-sha hits are not exactly the two named twins (CC-130)"
import json, sys
sys.path.insert(0, f"{sys.argv[1]}/scripts/b1_scaling")
import b1
test = set(json.load(open(b1.ROOT / b1.EXCL))["image_sha256"]["ktvic_test"])
hits = {(f.strip(), h) for h, f in (x.split(maxsplit=1) for x in open(sys.argv[2])) if h in test}
sys.exit(0 if hits == set(b1.TRAIN_TEST_TWINS.items()) else 1)  # zero hits or a third hit: STOP
PY
  say "2 train/test twins exempt (CC-130)"
  while IFS=: read -r f h; do [ "$(lsha $S5DIR/$f)" = $h ] || die "S5 preds $f"; done <<< "$S5_PREDS"
  [ "$(lsha $ADAPTER/adapter_model.safetensors)" = $AD_SHA ] && [ "$(lsha $ADAPTER/adapter_config.json)" = $AD_CFG ] \
    || die "p1dev_s42 adapter differs from 227a3312 / 93f04228"
  [ "$(lsha $REPO/scripts/checkpoint_resume_hook.py)" = $HOOK_SHA ] || die "checkpoint_resume_hook.py differs"
  say "LOCAL OK: train json $TRAIN_SHA, 3769 train images (test-sha hits = the 2 named twins), 3 S5 preds," \
    "adapter $AD_SHA, hook $HOOK_SHA"
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
allowed_list() {  # B-1 on M4: the two named train twins (b1.TRAIN_TEST_TWINS, CC-130), as "sha  path"
  PYTHONDONTWRITEBYTECODE=1 python3 -c "import sys; sys.path.insert(0, '$REPO/scripts/b1_scaling'); import b1; \
[print(f'{h}  $DS/ktvic/images/{f}') for f, h in b1.TRAIN_TEST_TWINS.items()]" > $STG/allowed.sha256 || die "twins"
}
STAGED_SHAS=$STG/ktvic_train.sha256  # all 3,769 KTVIC train images, dev300 included
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
no_test() {  # W9 (b): no file named test* and no KTVIC-test-sha image under datasets/ktvic*
  remote "cd /root/vsps && .venv/bin/python -c \"import json, sys; from pathlib import Path; \
sys.path.insert(0, 'scripts/b1_scaling'); import b1; \
t = set(json.load(open(b1.ROOT / b1.EXCL))['image_sha256']['ktvic_test']); \
sys.exit(1 if b1.ktvic_test_files(Path('$DS'), t) else 0)\"" > /dev/null || die "a KTVIC test file or image on $MNAME"
}
mirror() {
  rsync -a --exclude='*.partial*' -e "ssh -o BatchMode=yes -p $PORT" root@$HOST:$O/ $MIR/ || die "rsync"
  [ -z "${1:-}" ] || (cd $MIR && sha256sum --quiet -c $1) >> $LOCAL_LOG 2>&1 || die "mirror sha check ($1)"
  say "MIRROR OK ${1:-records}"
}

case $STEP in
  stage)
    isolated; local_inputs
    remote "[ ! -e $DS/ktvic ] && [ ! -e $DS/ktvic_dev ] && mkdir -p $DS/ktvic/images $O/s5_preds $O/staging" \
      || die "datasets/ktvic or ktvic_dev already on $MNAME"
    put $TRAIN $DS/ktvic/train_data.json
    [ "$(rsha $DS/ktvic/train_data.json)" = $TRAIN_SHA ] || die "train_data.json sha on $MNAME"
    tar -C $DATA/ktvic/images -cf - -T $STG/ktvic_train.files | $SSH "tar -C $DS/ktvic/images -xf -" \
      || die "copy the train images"
    put $STG/ktvic_train.sha256 $O/staging/ktvic_train.sha256
    remote "cd $DS/ktvic/images && N=\$(ls | wc -l) && OK=\$(sha256sum -c $O/staging/ktvic_train.sha256 2>/dev/null \
      | grep -c ': OK\$') && echo \"\$(date -u +%FT%TZ) B-1 ktvic staged: \$N files, sha OK \$OK/3769\" >> $OPLOG \
      && [ \$N = 3769 ] && [ \$OK = 3769 ]" || die "train image sha check"
    no_test
    remote "cd /root/vsps && NCS_DATA=/root/ncs-data .venv/bin/python scripts/ktvic_dev_split.py --verify \
      --json-dir $DS/ktvic_dev > /dev/null" || die "ktvic_dev json-dir"
    n=0; while IFS=: read -r f h; do put $S5DIR/$f $O/s5_preds/$f; [ "$(rsha $O/s5_preds/$f)" = $h ] || die "s5 $f"
      n=$((n + 1)); done <<< "$S5_PREDS"
    [ $n = 3 ] && [ "$($SSH "ls $O/s5_preds | wc -l" < /dev/null)" = 3 ] || die "not 3 S5 preds uploaded (CC-134)"
    remote "[ ! -e $RUNS/p1dev_s42 ] && mkdir -p $RUNS" || die "$RUNS/p1dev_s42 already exists"
    $SCP -r $ADAPTER root@$HOST:$RUNS/p1dev_s42 || die "upload the p1dev_s42 adapter"
    [ "$(rsha $RUNS/p1dev_s42/adapter_model.safetensors)" = $AD_SHA ] || die "adapter sha on $MNAME"
    remote "[ ! -e $HOOK ] && [ ! -e $PTH ] && ln -s /root/vsps/scripts/checkpoint_resume_hook.py $HOOK \
      && echo 'import vsps_resume_hook' > $PTH" || die "hook: $HOOK or $PTH exists"
    [ "$(rsha $HOOK)" = $HOOK_SHA ] || die "hook sha on $MNAME"
    # Amendment 4 (STOP-M4-4): prove the hook is imported by the .venv interpreter, not just present
    remote "/root/vsps/.venv/bin/python -c 'import sys; assert \"vsps_resume_hook\" in sys.modules'" \
      || die "resume hook is installed but not imported on $MNAME"
    rec "B-1 STAGED head $HEAD: train json $TRAIN_SHA, 3769 images, ktvic_dev, 3 s5 preds, adapter $AD_SHA, hook"
    [ $GPU = m3 ] || test_scan
    say "STAGE OK" ;;
  run)
    isolated; [ $GPU = m3 ] || test_scan; no_test
    ~/.config/vsps/usage_check.sh >> $LOCAL_LOG 2>&1 || die "usage_check: not enough headroom (~12 h needed, W11)"
    N0=$($SSH "cat $O/logs/job.log 2>/dev/null | wc -l") || die "$MNAME unreachable"
    rec "START B-1 tmux b1 head $HEAD"
    remote "cd /root/vsps && tmux new -d -s b1 \"bash scripts/b1_scaling/b1_job.sh $HEAD >> $O/job_tmux.log 2>&1\"" \
      || die "start b1"
    while true; do  # job.log lines only (W10)
      l=$($SSH "tail -n +$((N0 + 1)) $O/logs/job.log 2>/dev/null | grep -E 'BLOCK DONE|JOB STOP' | tail -1") \
        || { sleep 60; continue; }
      case "$l" in *"JOB STOP"*) mirror; die "$l" ;; *"BLOCK DONE"*) say "$l"; break ;; esac
      $SSH "tmux has-session -t b1" 2>/dev/null; rc=$?
      [ $rc = 1 ] && ! $SSH "tail -n +$((N0 + 1)) $O/logs/job.log | grep -qE 'BLOCK DONE|JOB STOP'" \
        && die "tmux b1 is gone without BLOCK DONE or JOB STOP (reboot?): run again to resume"
      sleep 300
    done
    while $SSH "tmux has-session -t b1" 2>/dev/null; do sleep 10; done
    mirror SHA256SUMS
    ~/.config/vsps/usage_check.sh >> $LOCAL_LOG 2>&1
    say "RUN DONE; next: cleanup" ;;
  cleanup)  # CC-099: outputs back with a local sha list, then the staged data and the hook removed
    [ -n "$REASON" ] || die "cleanup needs a reason (done, CAP_STOP, or the judge's ruling)"
    $SSH "tmux has-session -t b1" 2>/dev/null && die "tmux b1 is still running"
    mirror
    (cd $MIR && find . -type f | sort | xargs -d '\n' sha256sum) > $WORK/cleanup.sha256
    remote "rm -f $HOOK $PTH && [ ! -e $HOOK ] && [ ! -e $PTH ] && rm -rf $DS/ktvic $DS/ktvic_dev && [ ! -e $DS/ktvic ] \
      && [ ! -e $DS/ktvic_dev ] \
      && echo \"\$(date -u +%FT%TZ) B-1 CLEANUP ($REASON): datasets/ktvic, ktvic_dev, hook removed\" >> $OPLOG" \
      || die "cleanup delete"
    remote "[ ! -e $RUNS/p1dev_s42 ] || { [ \"\$(sha256sum $RUNS/p1dev_s42/adapter_model.safetensors | cut -c1-64)\" \
      = $AD_SHA ] && rm -rf $RUNS/p1dev_s42 && [ ! -e $RUNS/p1dev_s42 ] \
      && echo \"\$(date -u +%FT%TZ) B-1 CLEANUP ($REASON): runs/p1dev_s42 (n2 adapter $AD_SHA) removed\" >> $OPLOG; }" \
      || die "cleanup: $RUNS/p1dev_s42 is not the staged n2 adapter $AD_SHA (left in place)"
    mirror
    say "CLEANUP DONE ($REASON): $(wc -l < $WORK/cleanup.sha256) files back" ;;
  *) die "step must be dry-run, stage, run or cleanup" ;;
esac
