#!/bin/bash
# PASCAL-50S k-ladder for Paper A on M3 (manuscript/prereg/2026-10-28_pascal50s/PREREG.md, prereg_id
# 2026-10-28_a_p50_kladder; CC-144, CC-142 W2/W4/W8). Decodes the frozen A-N2 set with scripts/lb/decode_hf_vlm.py
# (unchanged) on the 1,000 UIUC/PASCAL-50S images; one look = scripts/pascal50s/p50.py score.
#   EXPECT_HEAD=<commit of the PREREG> bash scripts/pascal50s/p50_job.sh run     M3, /root/vsps, inside tmux
#   EXPECT_HEAD=<same commit> bash scripts/pascal50s/p50_job.sh score            after the local backup of preds/ matches
#   bash scripts/pascal50s/p50_job.sh --selftest                                  CPU, repo root
# Data (images, XML, pascal50S.json) and raw decodes live under $NCS_DATA, which the 30-min backup never pulls; only
# numbers and decode files with 0 8-gram hits reach /root/outputs/p50. A fault writes P50_FAULT_<utc>.md and exits 0;
# rerunning the same command resumes (PREREG §7). Exit codes of p50.py: 2 = NOT_EVALUABLE (input), 3 = STOP (cost) or
# a model leaves.
set -euo pipefail
D=scripts/pascal50s
X=$D/p50.py
XX=$D/p50x.py   # companion X1-X5 (manuscript/prereg/2026-10-29_a_companion), after score, before the delete
PY=${P50_PY:-/root/venv-lb/bin/python}   # the run's venv, also for --selftest (CC-159 W9; M3 system python lacks numpy)
if [ "${1:-}" = "--selftest" ]; then
  bash -n "$0" && $PY $X --selftest > /dev/null && $PY $XX --selftest > /dev/null && sha256sum --quiet -c $D/SHA256SUMS && echo "p50_job selftest ok"
  exit
fi
STAGE=${1:?run or score}
cd /root/vsps
export NCS_DATA=/root/ncs-data HF_HUB_OFFLINE=1
HEAD=${EXPECT_HEAD:?set EXPECT_HEAD to the commit of the P50 PREREG}
DEC=scripts/lb/decode_hf_vlm.py
P=$NCS_DATA/datasets/pascal50s
RAW=$NCS_DATA/p50_raw
O=/root/outputs/p50
EV=$O/EVENTS; LOG=$O/runs.log; L=$O/gpu_seconds.tsv; LEFT=$O/left.tsv; LOCK=$O/RUNNING; REG=$P/p50_reg.json
JSON_URL=https://raw.githubusercontent.com/ramavedantam/cider/f281464c60d496b8fabb89a7a8c120f655a3a2bd/data/pascal50S.json
TAR_URL=https://thor.robots.ox.ac.uk/pascal/VOC/voc2008/VOCtrainval_14-Jul-2008.tar
[ "$(git rev-parse HEAD)" = "$HEAD" ] || { echo "REFUSED: HEAD is not $HEAD"; exit 1; }
git diff --quiet HEAD -- || { echo "REFUSED: tracked files differ from HEAD"; exit 1; }
[ -n "${TMUX:-}" ] || { echo "REFUSED: run inside a tmux session"; exit 1; }
# one look: stop once both decide files are delivered; a score rerun may only finish the delivery (CC-159 W2)
if [ -e "$O/p50_decide.json" ] && { [ "$STAGE" != score ] || [ -e "$O/p50x_decide.json" ]; }; then
  echo "STOP: P50 already decided (one look)"; exit 1
fi
OTHER=$(ls /root/outputs/*/RUNNING 2>/dev/null || true)
[ -z "$OTHER" ] || { echo "REFUSED: a lock exists: $OTHER"; exit 1; }
mkdir -p "$O/timing" "$RAW/smoke" "$P"
touch "$L" "$LEFT"
( set -o noclobber; echo "$0 $STAGE $(date -u +%FT%TZ)" > "$LOCK" ) || { echo "REFUSED: $LOCK exists"; exit 1; }
trap 'rm -f "$LOCK"' EXIT
ev() { echo "$(date -u +%FT%TZ) $*" >> "$EV"; echo "$*"; }
fault() {
  printf '# P50 fault (%s)\n\n%s\n\nNo verdict; rerun the same command (PREREG §7).\n' "$(date -u +%FT%TZ)" "$1" \
    > "$O/P50_FAULT_$(date -u +%Y%m%dT%H%M%SZ).md"
  ev "FAULT: $1"
  exit 0
}
cleanup() {  # W8: data and raw decodes deleted; the empty listing and the time go to EVENTS
  rm -rf "$P" "$RAW"
  ev "deleted $P and $RAW; ls: $(ls -A "$P" "$RAW" 2>&1 | tr '\n' ' ')"
}
notrun() {  # NOT_EVALUABLE (input) or STOP (cost): the decide file records it, then the data go
  printf '{"prereg_id": "2026-10-28_a_p50_kladder", "status": "%s", "reason": "%s", "utc": "%s"}\n' \
    "$1" "$2" "$(date -u +%FT%TZ)" > "$O/p50_decide.json"
  printf '{"prereg_id": "2026-10-29_a_p50_companion", "status": "not run: P50 %s", "utc": "%s"}\n' \
    "$1" "$(date -u +%FT%TZ)" > "$O/p50x_decide.json"
  ev "$1: $2"
  cleanup
  exit 0
}
CUT=$(date -u -d 2026-11-16T12:00:00Z +%s)   # registered run cutoff (CC-142 ruling 8); the start date is the operator's
# once P50's score has written its decide file the cutoff never fires: the job only delivers (CC-159 W2 (i))
cutoff() { [ -s "$RAW/p50_decide.json" ] || [ "$(date -u +%s)" -lt "$CUT" ] || notrun "not run" "the registered cutoff 2026-11-16 12:00Z passed (CC-142 ruling 8)"; }
ev "start $STAGE head $HEAD"
cutoff
# 1. import check first: every module the run uses, in the run's venv
rc=0; $PY $X imports >> "$LOG" 2>&1 || rc=$?
[ "$rc" = 0 ] || fault "import check exit $rc"
# 2. pins (prereg, evaluator, job, id lists, decoder, A-N2 registration, matchers) and the CPU self-test
sha256sum --quiet -c $D/SHA256SUMS >> "$LOG" 2>&1 || fault "SHA256SUMS"
$PY $X --selftest >> "$LOG" 2>&1 || fault "selftest"
$PY $XX --selftest >> "$LOG" 2>&1 || fault "p50x selftest"
ev "venv-lb freeze sha256 $($PY -m pip freeze | sha256sum | cut -c1-64)"
G() { cutoff; $PY $X guard --head "$HEAD" >> "$LOG" 2>&1; }   # cutoff; M3/M4, idle GPU, HEAD + clean tree, no B-1/B-2/C-EN
G || fault "guard refused"

if [ "$STAGE" = run ]; then
  # 3. W6: structure-only check of pascal50S.json (numbers only), before any image or decode
  if [ ! -s "$O/refcheck.json" ]; then
    [ -s "$P/pascal50S.json" ] || { curl -fsSL -o "$P/pascal50S.json.part" "$JSON_URL" \
      && mv "$P/pascal50S.json.part" "$P/pascal50S.json"; } || fault "pascal50S.json download"
    rc=0; $PY $X refcheck --json "$P/pascal50S.json" --out "$O/refcheck.json" >> "$LOG" 2>&1 || rc=$?
    [ "$rc" = 2 ] && notrun "NOT_EVALUABLE (input)" "pascal50S.json keys do not match the 1,000 ids 1:1 (PREREG §3.2)"
    [ "$rc" = 0 ] || { rm -f "$O/refcheck.json"; fault "refcheck exit $rc"; }
  fi
  # 4. W8: VOC tar sha256 into EVENTS before extraction; only the 1,020 images and 1,000 XML leave the tar; tar deleted
  if [ ! -s "$O/stage.json" ]; then
    AV=$(df -BG --output=avail "$NCS_DATA" | tail -1 | tr -dc 0-9)
    [ "$AV" -ge 2 ] || fault "disk: $AV GB free under NCS_DATA, 2 GB needed for the tar and its members"
    [ -s "$P/voc.tar" ] || { curl -fsSL -o "$P/voc.tar.part" "$TAR_URL" && mv "$P/voc.tar.part" "$P/voc.tar"; } \
      || fault "VOC tar download"
    TS=$(sha256sum < "$P/voc.tar" | cut -c1-64)
    ev "VOC tar sha256 $TS bytes $(stat -c %s "$P/voc.tar") (recorded before extraction)"
    rc=0; $PY $X stage --tar "$P/voc.tar" --tar-sha "$TS" --out "$O/stage.json" >> "$LOG" 2>&1 || rc=$?
    [ "$rc" = 2 ] && notrun "NOT_EVALUABLE (input)" "an image of the 1,000 or of the smoke list is missing from the tar"
    [ "$rc" = 0 ] || { rm -f "$O/stage.json"; fault "stage exit $rc"; }
    rm -f "$P/voc.tar"
    ev "VOC tar deleted; label rung: $($PY -c "import json; print(json.load(open('$O/stage.json'))['label_rung'])")"
  fi
  [ -s "$REG" ] || $PY $X register --out "$REG" || fault "register"
  ev "runtime registration sha256 $(sha256sum < "$REG" | cut -c1-64)"
  # 5. snapshots at their A-N2 pins (network, not GPU time)
  for M in $($PY $DEC --prereg "$REG" --models); do
    W=$NCS_DATA/models/lb/$M
    $PY $DEC --prereg "$REG" --check-snapshot "$M" --snapshot "$W" >> "$LOG" 2>&1 && continue
    AV=$(df -BG --output=avail "$NCS_DATA" | tail -1 | tr -dc 0-9)
    [ "$AV" -ge 20 ] || fault "disk: $AV GB free under NCS_DATA, 20 GB needed before fetching $M"
    HF_HUB_OFFLINE=0 timeout 2h $PY $DEC --prereg "$REG" --fetch "$M" --snapshot "$W" >> "$LOG" 2>&1 || fault "fetch $M"
  done
  # 6. smoke (§6): 20 non-test VOC trainval images, both prompts, timing only; outputs deleted, never scored.
  #    A smoke run may fault twice (timeout 3600 s included); at the third fault its model leaves, with no replacement.
  for M in $($PY $DEC --prereg "$REG" --models); do
    for Q in short_en detailed_en; do
      R=p50smoke_$M-$Q
      [ -s "$O/timing/$R.json" ] && continue
      grep -q "^$M	" "$LEFT" && continue 2
      NF=$(awk -F'\t' -v r="$R" '$1 == r && $3 != 0' "$L" | wc -l)
      if [ "$NF" -gt 2 ]; then
        $PY $X leave --left "$LEFT" --model "$M" --reason "$NF smoke faults on $R (KM)"
        ev "$M leaves: $NF smoke faults on $R"
        continue 2
      fi
      G || fault "guard refused before $R"
      rc=0; $PY $X timed --timeout 3600 --ledger "$L" --label "$R" --marks "$O/timing/$R.json" -- \
        $PY $DEC --prereg "$REG" --run-id "$R" --snapshot "$NCS_DATA/models/lb/$M" --out-dir "$RAW/smoke" \
        >> "$LOG" 2>&1 || rc=$?
      rm -f "$RAW/smoke/$R".preds.json*
      [ "$rc" = 0 ] || { rm -f "$O/timing/$R.json"; fault "smoke $R exit $rc"; }
    done
  done
  # 7. cap from the measured smoke: smoke + every run + every fault <= 8 GPU-h; whole models leave in the drop order
  if [ ! -s "$O/plan.json" ]; then
    rc=0; $PY $X plan --timing "$O/timing" --ledger "$L" --left "$LEFT" --out "$O/plan.json" >> "$LOG" 2>&1 || rc=$?
    [ "$rc" = 3 ] && notrun "STOP (cost)" "fewer than 3 models fit in 8 GPU-h after the smoke (PREREG §6)"
    [ "$rc" = 0 ] || { rm -f "$O/plan.json"; fault "plan exit $rc"; }
  fi
  # 8. decodes, most important model first; FAULT (time), a third fault or a breach of 8 GPU-h: the model leaves
  for M in $($PY $X kept --plan "$O/plan.json"); do
    for Q in short_en detailed_en; do
      R=p50_$M-$Q
      [ -s "$RAW/$R.preds.json" ] && continue
      rc=0; T=$($PY $X budget --plan "$O/plan.json" --ledger "$L" --left "$LEFT" --run "$R" 2>> "$LOG") || rc=$?
      if [ "$rc" = 3 ]; then ev "$M leaves: $(grep "^$M	" "$LEFT" | cut -f2 || true)"; continue 2; fi
      [ "$rc" = 0 ] || fault "budget $R exit $rc"
      G || fault "guard refused before $R"
      rc=0; $PY $X timed --timeout "$T" --ledger "$L" --label "$R" -- \
        $PY $DEC --prereg "$REG" --run-id "$R" --snapshot "$NCS_DATA/models/lb/$M" --out-dir "$RAW" \
        >> "$LOG" 2>&1 || rc=$?
      if [ "$rc" = 124 ]; then
        $PY $X leave --left "$LEFT" --model "$M" --reason "FAULT (time) on $R"
        ev "$M leaves: FAULT (time) on $R"
        continue 2
      fi
      [ "$rc" = 0 ] || fault "$R exit $rc (infrastructure fault; rerun allowed, PREREG §7)"
    done
  done
  # 9. W4: 8-gram check of every decode against pascal50S.json; a file with a hit never leaves M3
  mkdir -p "$O/preds"
  for F in "$RAW"/p50_*.preds.json; do
    [ -e "$F" ] || continue
    B=$(basename "$F")
    rc=0; $PY $X ngram --json "$P/pascal50S.json" "$F" > "$O/ngram_$B" 2>> "$LOG" || rc=$?
    if [ "$rc" = 0 ]; then cp "$F" "$F.sha256" "$O/preds/"; else ev "$B: 8-gram check rc $rc; stays on M3"; fi
  done
  (cd "$O/preds" && sha256sum ./*.preds.json > SHA256SUMS 2>/dev/null || true)
  ev "decodes done; next: verify the local backup of preds/ against preds/SHA256SUMS, then run: $0 score"
elif [ "$STAGE" = score ]; then
  [ -s "$O/plan.json" ] && [ -s "$O/stage.json" ] && [ -s "$REG" ] || fault "score before a finished run stage"
  if [ ! -s "$RAW/p50_decide.json" ]; then  # score writes its decide file only on success
    rc=0; $PY $X score --raw "$RAW" --plan "$O/plan.json" --left "$LEFT" --stage "$O/stage.json" --reg "$REG" \
      --out "$RAW/p50_decide.json" >> "$LOG" 2>&1 || rc=$?
    [ "$rc" = 0 ] || fault "score exit $rc"
  fi
  # (ii) P50's own decide: 8-gram check and copy BEFORE the companion runs; a hit keeps it on M3 (PREREG §6 W4)
  if [ ! -s "$O/p50_decide.json" ]; then
    rc=0; $PY $X ngram --json "$P/pascal50S.json" "$RAW/p50_decide.json" > "$O/ngram_decide.json" 2>> "$LOG" || rc=$?
    [ "$rc" = 0 ] || fault "the decide file fails the 8-gram check; it stays on M3"
    cp "$RAW/p50_decide.json" "$O/p50_decide.json"
    ev "P50 decided $(sha256sum < "$O/p50_decide.json" | cut -c1-16); companion next"
  fi
  # (iii) companion: at most 2 attempts, counted in EVENTS; then a terminal record, and the data are deleted anyway
  XFAIL='{"prereg_id": "2026-10-29_a_p50_companion", "status": "FAULT (code): companion not run", "reason": "%s"}\n'
  if [ ! -s "$O/p50x_decide.json" ]; then
    NA=$(grep -c ' p50x attempt ' "$EV" || true)
    if [ ! -s "$RAW/p50x_decide.json" ] && [ "$NA" -lt 2 ]; then
      NA=$((NA + 1)); ev "p50x attempt $NA of 2"
      rc=0; $PY $XX score --raw "$RAW" --stage "$O/stage.json" --decide "$RAW/p50_decide.json" \
        --out "$RAW/p50x_decide.json" >> "$LOG" 2>&1 || rc=$?
      if [ "$rc" != 0 ]; then
        rm -f "$RAW/p50x_decide.json"
        [ "$NA" -ge 2 ] || fault "p50x exit $rc (attempt $NA of 2; data kept; rerun score)"
        ev "p50x exit $rc at attempt $NA of 2: companion not run"
      fi
    fi
    if [ -s "$RAW/p50x_decide.json" ]; then
      rc=0; $PY $X ngram --json "$P/pascal50S.json" "$RAW/p50x_decide.json" > "$O/ngram_p50x.json" 2>> "$LOG" || rc=$?
      if [ "$rc" = 0 ]; then
        cp "$RAW/p50x_decide.json" "$O/p50x_decide.json"
      else  # stays on M3 and goes with the data
        ev "the p50x decide file fails the 8-gram check (rc $rc); it stays on M3 and is deleted with the data"
        printf "$XFAIL" "p50x decide file failed the 8-gram check" > "$O/p50x_decide.json"
      fi
    else
      printf "$XFAIL" "p50x failed twice" > "$O/p50x_decide.json"
    fi
  fi
  (cd "$O" && sha256sum p50_decide.json p50x_decide.json plan.json stage.json refcheck.json > SHA256SUMS)
  ev "decided $(sha256sum < "$O/p50_decide.json" | cut -c1-16)"
  cleanup
else
  echo "usage: $0 run|score|--selftest"; exit 1
fi
