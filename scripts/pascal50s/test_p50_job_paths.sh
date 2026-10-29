#!/bin/bash
# Score-stage paths of p50_job.sh with stubs (CC-159 W2, W11): p50x fault x2, cutoff passed with a SCORED decide,
# p50x 8-gram hit, clean delivery, and a cutoff before any score. CPU only; a sandbox git repo under a temp dir; the
# job is copied with its /root paths (and, for the cutoff cases, its cutoff date) rewritten. No real data or model.
#   bash scripts/pascal50s/test_p50_job_paths.sh
set -euo pipefail
JOB=$(cd "$(dirname "$0")" && pwd)/p50_job.sh
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
fail() { echo "FAIL: $*"; exit 1; }
st() { python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['status'])" "$1"; }

setup() {  # $1 = sandbox name, $2 = cutoff date written into the job copy
  S=$T/$1; R=$S/vsps; mkdir -p "$R/scripts/pascal50s" "$S/ncs/datasets/pascal50s" "$S/ncs/p50_raw" "$S/out/p50"
  cat > "$R/scripts/pascal50s/p50.py" <<'EOF'
import json, sys
a = sys.argv[1:]
if a and a[0] == "score":
    json.dump({"status": "SCORED", "analysis_set": {}}, open(a[a.index("--out") + 1], "w"))
elif a and a[0] == "ngram":
    sys.exit(1 if "LEAK" in open(a[-1]).read() else 0)
EOF
  cat > "$R/scripts/pascal50s/p50x.py" <<'EOF'
import json, os, sys
a, mode = sys.argv[1:], open(os.environ["STUB_MODE"]).read().strip()
if a and a[0] == "score":
    if mode == "fail":
        sys.exit(1)
    json.dump({"status": "SCORED", "x": "LEAK" if mode == "leak" else "0"}, open(a[a.index("--out") + 1], "w"))
EOF
  (cd "$R" && sha256sum scripts/pascal50s/p50.py scripts/pascal50s/p50x.py > scripts/pascal50s/SHA256SUMS \
    && git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -qm stub)
  sed -e "s#cd /root/vsps#cd $R#" -e "s#/root/ncs-data#$S/ncs#" -e "s#O=/root/outputs/p50#O=$S/out/p50#" \
      -e "s#/root/outputs/\*/RUNNING#$S/out/*/RUNNING#" -e "s#2026-11-16T12:00:00Z#$2#" "$JOB" > "$S/job.sh"
  for f in plan stage refcheck; do echo '{"label_rung": "kept"}' > "$S/out/p50/$f.json"; done
  echo '{}' > "$S/ncs/datasets/pascal50s/p50_reg.json"; echo '{}' > "$S/ncs/datasets/pascal50s/pascal50S.json"
  echo '{}' > "$S/ncs/p50_raw/p50_x-short_en.preds.json"
  O=$S/out/p50; P=$S/ncs/datasets/pascal50s; RAW=$S/ncs/p50_raw
}
run() {  # $1 = stub mode; returns the job's exit code
  echo "$1" > "$S/mode"
  rc=0; (cd "$S" && STUB_MODE=$S/mode TMUX=1 P50_PY=python3 EXPECT_HEAD=$(git -C "$R" rev-parse HEAD) \
    bash "$S/job.sh" score > "$S/stdout" 2>&1) || rc=$?
  return $rc
}

# 1. p50x faults twice: P50 delivered before the companion; then FAULT (code) and the data are deleted; then STOP
setup fault 2099-01-01T00:00:00Z
run fail || fail "fault: attempt 1 rc"
[ "$(st "$O/p50_decide.json")" = SCORED ] || fail "fault: P50 decide not delivered before p50x"
[ ! -e "$O/p50x_decide.json" ] && [ -d "$RAW" ] || fail "fault: attempt 1 must keep the data and write no p50x record"
run fail || fail "fault: attempt 2 rc"
[ "$(grep -c ' p50x attempt ' "$O/EVENTS")" = 2 ] || fail "fault: attempts not counted in EVENTS"
[ "$(st "$O/p50x_decide.json")" = "FAULT (code): companion not run" ] || fail "fault: no terminal record"
[ ! -e "$RAW" ] && [ ! -e "$P" ] || fail "fault: data not deleted after the second failure"
! run fail && grep -q "STOP: P50 already decided" "$S/stdout" || fail "fault: a third run must STOP"
echo "PASS p50x fault x2 -> P50 delivered, companion FAULT (code), data deleted, then STOP"

# 2. cutoff passed with P50's SCORED decide present: delivered, never "not run"
setup cutscored 2020-01-01T00:00:00Z
echo '{"status": "SCORED", "analysis_set": {}}' > "$RAW/p50_decide.json"
run ok || fail "cutscored rc"
[ "$(st "$O/p50_decide.json")" = SCORED ] && [ "$(st "$O/p50x_decide.json")" = SCORED ] || fail "cutscored: not delivered"
! grep -q '"not run"' "$O/p50_decide.json" && [ ! -e "$RAW" ] || fail "cutscored: overwritten or data kept"
echo "PASS cutoff passed with a SCORED decide -> delivered (P50 SCORED, companion SCORED), not 'not run'"

# 3. cutoff passed before any score: "not run" for P50 and the companion, data deleted
setup cutnone 2020-01-01T00:00:00Z
run ok || fail "cutnone rc"
[ "$(st "$O/p50_decide.json")" = "not run" ] && grep -q "not run: P50" "$O/p50x_decide.json" && [ ! -e "$RAW" ] \
  || fail "cutnone"
echo "PASS cutoff before any score -> 'not run' recorded for both, data deleted"

# 4. p50x decide with an 8-gram hit: stays on the machine and goes with the data; FAULT (code) record delivered
setup leak 2099-01-01T00:00:00Z
run leak || fail "leak rc"
[ "$(st "$O/p50x_decide.json")" = "FAULT (code): companion not run" ] && ! grep -rq LEAK "$O" && [ ! -e "$RAW" ] \
  || fail "leak"
echo "PASS p50x 8-gram hit -> not copied, deleted with the data, FAULT (code) record"

# 5. clean path
setup ok 2099-01-01T00:00:00Z
run ok || fail "ok rc"
[ "$(st "$O/p50x_decide.json")" = SCORED ] && [ ! -e "$RAW" ] && (cd "$O" && sha256sum --quiet -c SHA256SUMS) || fail "ok"
echo "PASS clean path -> both decide files delivered with SHA256SUMS, data deleted"
echo "test_p50_job_paths ok"
