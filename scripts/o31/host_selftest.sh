#!/usr/bin/env bash
# O31 host self-test, CC-504 host items H1-H4 (record match, before P0r). Run on the rented host, CPU only.
#
#   PY=<venv python> REPO_TAR=<git archive tar of rescap scripts data/coco_probe at COMMIT> COMMIT=<hash> \
#   RECORDS_TAR=<stage1_records.tar.gz> PROBES=<E1b probes.jsonl> [JMUT=<jmut_cc504.py>] [GPU=1] \
#   ./host_selftest.sh <OUT dir>
#
# H1 freeze (+ GPU=1: transformers 4.51.3 and trl 0.19.1, repo requirements.txt; torch/peft/bitsandbytes recorded)
# H2 repo snapshot from the named commit; the package refuses on any REUSED mismatch
# H3 run_tests.sh (self-tests + own, W3/W5 and judge mutants; JMUT also runs the judge's script unchanged)
# H4 P0r inputs: records tarball b312de68, probes ffd27917 (OPS-1031e1bdone); 0 gender_uncap; no_q all REJECTED
# Writes counts and shas only. Exit 0 iff every item passes; the last line of OUT/host_selftest.log says so.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:?usage: host_selftest.sh <OUT dir>}"
: "${PY:?PY}" "${REPO_TAR:?REPO_TAR}" "${COMMIT:?COMMIT}" "${RECORDS_TAR:?RECORDS_TAR}" "${PROBES:?PROBES}"
RECORDS_SHA=b312de68180a2f9bf31602bae917ed170b2630174c30c11e9ea59c64aff840b0
PROBES_SHA=ffd2791721912683964145cc6954d1ada471495cb9ba9898eb928a073fb32cc8
mkdir -p "$OUT"
LOG="$OUT/host_selftest.log"
: > "$LOG"
say() { echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }
fail() { say "FAIL $*"; echo "FAIL $*" >&2; exit 1; }

# H1 -------------------------------------------------------------------------------------------------------------
say "H1 python $("$PY" -V 2>&1)"
"$PY" -m pip freeze > "$OUT/pip_freeze.txt"
say "H1 pip_freeze.txt sha256 $(sha256sum "$OUT/pip_freeze.txt" | cut -d' ' -f1)"
"$PY" -I -B -c "import numpy; print(numpy.__version__)" > "$OUT/numpy_version.txt" || fail "H1 numpy"
say "H1 numpy $(cat "$OUT/numpy_version.txt")"
if [ "${GPU:-0}" = 1 ]; then
  "$PY" -I -B - >> "$LOG" 2>&1 <<'EOF' || fail "H1 GPU stack"
import importlib.metadata as md
pins = {"transformers": "4.51.3", "trl": "0.19.1"}
for k, v in pins.items():
    got = md.version(k)
    print(f"H1 {k} {got}")
    assert got == v, f"{k} {got} != {v}"
for k in ("torch", "peft", "bitsandbytes", "accelerate"):
    print(f"H1 {k} {md.version(k)} (recorded)")
import torch  # noqa: F401
EOF
fi
say "H1 PASS"

# H2 -------------------------------------------------------------------------------------------------------------
REPO="$OUT/repo_$COMMIT"
[ -d "$REPO" ] && chmod -R u+w "$REPO" && rm -rf "$REPO"
mkdir -p "$REPO"
tar -xf "$REPO_TAR" -C "$REPO"
say "H2 repo tar $REPO_TAR sha256 $(sha256sum "$REPO_TAR" | cut -d' ' -f1) commit $COMMIT"
chmod -R a-w "$REPO"
VSPS_REPO="$REPO" "$PY" -I -B -c "import sys; sys.path.insert(0, '$HERE/src'); import o31; o31.repo(); print(len(o31.REUSED))" \
  >> "$LOG" 2>&1 || fail "H2 REUSED sha check"
say "H2 PASS (every REUSED file equals its pin)"

# H3 -------------------------------------------------------------------------------------------------------------
export TMPDIR="$OUT/tmp" && mkdir -p "$TMPDIR"
PY="$PY" VSPS_REPO="$REPO" "$HERE/run_tests.sh" > "$OUT/run_tests.log" 2>&1 || fail "H3 run_tests.sh (see run_tests.log)"
grep -E "^[0-9]+/[0-9]+ passed$" "$OUT/run_tests.log" | tail -1 | { read -r l; say "H3 tests $l"; }
grep -E "killed; survived \[\]; bad sites \[\]$" "$OUT/run_tests.log" > /dev/null || fail "H3 mutant survivors"
if [ -n "${JMUT:-}" ]; then
  VSPS_REPO="$REPO" "$PY" -I -B "$JMUT" "$HERE" > "$OUT/jmut.log" 2>&1
  grep -q "^survived 0 \[\]$" "$OUT/jmut.log" || fail "H3 judge mutants survived (see jmut.log)"
  say "H3 judge script: $(grep -c '^killed' "$OUT/jmut.log") killed, sites re-pointed: $(grep -c '^SITE' "$OUT/jmut.log")"
fi
say "H3 run_tests.log sha256 $(sha256sum "$OUT/run_tests.log" | cut -d' ' -f1)"
say "H3 PASS"

# H4 -------------------------------------------------------------------------------------------------------------
[ "$(sha256sum "$RECORDS_TAR" | cut -d' ' -f1)" = "$RECORDS_SHA" ] || fail "H4 records tarball sha"
[ "$(sha256sum "$PROBES" | cut -d' ' -f1)" = "$PROBES_SHA" ] || fail "H4 probes.jsonl sha"
VSPS_REPO="$REPO" "$PY" -I -B - "$RECORDS_TAR" "$PROBES" "$HERE/src" >> "$LOG" 2>&1 <<'EOF' || fail "H4 record checks"
import json, sys, tarfile
sys.path.insert(0, sys.argv[3])
from o31 import gate, verify
recs = 0; uncap = 0; no_q = 0; no_q_status = {}; names = set()
with tarfile.open(sys.argv[1], "r:gz") as tf:
    for m in tf:
        if not (m.isfile() and m.name.endswith(".json")):
            continue
        r = json.loads(tf.extractfile(m).read().decode("utf-8"))
        recs += 1
        names.add(r["file_name"])
        for p in r["propositions"]:
            uncap += (p.get("backoff") or {}).get("kind") == "gender_uncap"
            if verify.affirmative_key(p) is None:
                no_q += 1
                st = (p.get("verification") or {}).get("status")
                no_q_status[st] = no_q_status.get(st, 0) + 1
tab = gate.load_table(sys.argv[2])
print(f"H4 records {recs}; gender_uncap traces {uncap}; no_q {no_q} by status {no_q_status}; "
      f"probe images {len(tab)}; images without probes {len(names - set(tab))}")
assert recs == 3700 and uncap == 0 and set(no_q_status) <= {"REJECTED"}, "H4 record facts"
EOF
say "H4 PASS (expected no_q 1,625, all REJECTED: CC-504 E3)"
say "ALL PASS H1-H4"
echo "ALL PASS H1-H4; log $LOG"
