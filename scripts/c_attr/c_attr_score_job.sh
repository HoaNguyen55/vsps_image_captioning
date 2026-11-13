#!/bin/bash
# C-ATTR-DEV scoring on the rented host: CC-338 S1, CC-346 ruling 5, PI-1111j. CPU scoring runs on the host. The laptop
# keeps the 444 copy and the hashes only. Run document: manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_SCORING_RUN_DOC_v1.md.
# One stage per call, in the order verify -> ova | close -> ovb -> rest -> posthoc (c_attr_score.py cmd_stage holds
# the rules). Every stage after verify needs --prev <sha256 of the previous stage's file, as logged>. Each stage
# prints the sha256 of its own file and stops. Nothing prints a caption. CPU only, under nice 19. A stage never runs
# beside a decode job: it is refused while /root/outputs/c_attr*/RUNNING exists (§6.7).
# Usage:  bash scripts/c_attr/c_attr_score_job.sh <expected HEAD> selftest
#         bash scripts/c_attr/c_attr_score_job.sh <expected HEAD> verify --b1-sums <sha256> --b-sums <sha256>
#         bash scripts/c_attr/c_attr_score_job.sh <expected HEAD> ova|ovb|rest|posthoc --prev <sha256>
#         bash scripts/c_attr/c_attr_score_job.sh <expected HEAD> close --prev <sha256> --reason "<reason>"
# Block 3 (C_ATTR_BLOCK3_SCORING_RUN_DOC_v1.md, CC-368 ruling 12), work folder /root/c_attr_score_b3:
#         bash scripts/c_attr/c_attr_score_job.sh <expected HEAD> b3verify --b3-sums <sha256>
#         bash scripts/c_attr/c_attr_score_job.sh <expected HEAD> b3k5|b3rest --prev <sha256>
set -euo pipefail
EXPECT=${1:?usage: c_attr_score_job.sh <expected HEAD> STAGE [args]}; STAGE=${2:?usage: c_attr_score_job.sh HEAD STAGE}
shift 2
cd "$(dirname "$0")/../.."
MID=$(cat /root/.vsps_machine_id 2>/dev/null || true)
case "$MID" in h1|h2) ;; *) echo "REFUSED: /root/.vsps_machine_id is not h1 or h2 (scoring runs on the rented host)"; exit 1;; esac
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1 VSPS_MACHINE_ID=$MID
PY=/root/vsps/.venv/bin/python; W=/root/c_attr_score
case "$STAGE" in b3*) W=/root/c_attr_score_b3;; esac
mkdir -p $W/logs
say() { echo "$(date -u +%FT%TZ) $*" | tee -a $W/logs/score.log; }
stop() { say "SCORE STOP $*"; exit 1; }
[ "$(git rev-parse HEAD)" = "$EXPECT" ] || stop "HEAD is not $EXPECT"
git diff --quiet HEAD -- || stop "tracked files differ from HEAD"
(cd scripts/c_attr && sha256sum --quiet -c SHA256SUMS) || stop "scripts/c_attr/SHA256SUMS"
for d in /root/outputs/c_attr /root/outputs/c_attr_b1 /root/outputs/c_attr_b3; do
  if [ -e $d/RUNNING ]; then stop "$d/RUNNING exists: never beside a decode job (§6.7)"; fi
done
say "START $STAGE head $EXPECT"
if [ "$STAGE" = selftest ]; then
  for f in c_attr c_attr_lists c_attr_score; do
    nice -n 19 $PY -I -B scripts/c_attr/$f.py --selftest >> $W/logs/selftest.log 2>&1 || stop "$f selftest"
  done
  say "SELFTEST OK"; exit 0
fi
rc=0; nice -n 19 $PY -I -B scripts/c_attr/c_attr_score.py stage $STAGE "$@" >> $W/logs/$STAGE.log 2>&1 || rc=$?
say "$(tail -1 $W/logs/$STAGE.log)"
[ $rc = 0 ] || stop "stage $STAGE rc=$rc"
