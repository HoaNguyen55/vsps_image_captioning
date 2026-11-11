#!/bin/bash
# PI-1109g laptop dry run of every c_attr_job.sh mode (selftest, block1) in the host tree: a sandbox laid out as the
# host's /root (vsps = a sparse code-only clone (scripts, manuscript/prereg, rescap, configs, data/coco_probe/chair_synonyms.txt) with the c_attr files committed in a throwaway commit, ncs-data with the
# two memory-caption annotation files and empty image and model dirs, outputs with the five stored ret runs, venv-lb and
# vsps/.venv = the laptop venv, .vsps_machine_id = h1) is bind-mounted over /root in a user + mount namespace, then the
# job runs with C_ATTR_DRY=1 (decodes: --limit 2 --dry-run, no model load). No network, no GPU. The sandbox is deleted
# at the end; the job log is copied to the given file.
#     bash scripts/c_attr/dryrun.sh LOGFILE            from the repo root; rc = the job's rc
set -uo pipefail
OUTLOG=${1:?usage: dryrun.sh LOGFILE}
REPO=$(git rev-parse --show-toplevel); VENV=$HOME/.venvs/c_stage1_lists
SB=$(mktemp -d "${TMPDIR:-/tmp}/c_attr_dry.XXXX")
git clone -q --no-checkout --shared "$REPO" $SB/vsps
git -C $SB/vsps sparse-checkout set --no-cone /scripts/ /manuscript/prereg/ /rescap/ /configs/ \
  /data/coco_probe/chair_synonyms.txt  # the one tracked data file the C modules read on import (rescap.chair)
git -C $SB/vsps checkout -q "$(git -C "$REPO" rev-parse HEAD)"
mkdir -p $SB/vsps/scripts/c_attr
for f in c_attr.py c_attr_lists.py c_attr_score.py c_attr_job.sh c_attr_mutants.py dryrun.sh STORED_SHA256 SHA256SUMS \
         c_attr_lists.json c_attr_lists.json.sha256; do cp "$REPO/scripts/c_attr/$f" $SB/vsps/scripts/c_attr/; done
git -C $SB/vsps add -f scripts/c_attr
git -C $SB/vsps -c user.email=dry@local -c user.name=dry commit -qm "dry run: c_attr files" || exit 2
H=$(git -C $SB/vsps rev-parse HEAD)
D=$SB/ncs-data/datasets
mkdir -p $D/ktvic/images $D/openviic/images $D/c_xm_dev500/images $SB/.cache/huggingface/hub
for m in qwen25vl_7b internvl3_8b c_t1_aya_vision_8b; do mkdir -p $SB/ncs-data/models/$m; done
cp "$REPO/data/datasets/ktvic/train_data.json" $D/ktvic/
cp "$REPO/data/datasets/openviic/uit-openviic-annotation-train.json" $D/openviic/
B=$REPO/.session_backup/machines
while read -r h p; do  # the five stored ret runs of step 1.0, from the laptop's read-only backup copies
  case $p in */c_stage1/*|*/c_stage2/*) src=$B/M3$p;; *) src=$B/M1$p;; esac
  mkdir -p "$(dirname $SB/${p#/root/})"; cp "$src" $SB/${p#/root/}
done < <(grep -E 'ov_dev_[ab]-ret-' "$REPO/scripts/c_attr/STORED_SHA256")
ln -s $VENV $SB/venv-lb; ln -s $VENV $SB/vsps/.venv
echo h1 > $SB/.vsps_machine_id
rc=0
unshare -rm bash -c "mount --bind $SB /root && cd /root && export HOME=/root TMUX=dryrun-no-tmux C_ATTR_DRY=1 && \
  bash /root/vsps/scripts/c_attr/c_attr_job.sh selftest $H && bash /root/vsps/scripts/c_attr/c_attr_job.sh block1 $H" \
  > $SB/stdout.txt 2>&1 || rc=$?
{ echo "# c_attr dry run $(date -u +%FT%TZ); sandbox HEAD $H (throwaway commit on repo HEAD $(git -C "$REPO" rev-parse HEAD)); rc=$rc"
  echo "# ---- logs/job.log"; cat $SB/outputs/c_attr/logs/job.log
  for f in $SB/outputs/c_attr/logs/*.log; do [ "$(basename $f)" = job.log ] || { echo "# ---- logs/$(basename $f)"; cat $f; }; done
  echo "# ---- parity/"; cat $SB/outputs/c_attr/parity/*.json 2>/dev/null
  echo "# ---- stdout"; cat $SB/stdout.txt; } > "$OUTLOG"
rm -rf $SB
exit $rc
