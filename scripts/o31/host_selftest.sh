#!/usr/bin/env bash
# O31 host self-test, CC-504 host items H1-H4 (record match) plus H-G before G1/G2. Runs on the PI's PC under
# ERRATUM_O31_2 E1: every file inside O31_BASE (the job folder), interpreters inside it, HF_HOME/TMPDIR/pip cache too.
#
#   O31_BASE=<job folder> PY=<venv python inside it> REPO_TAR=<git archive tar of rescap scripts data/coco_probe and
#   every other REUSED path (configs/main.env, data/lb/sets, manuscript/prereg/...), at COMMIT> COMMIT=<hash> \
#   RECORDS_TAR=<stage1_records.tar.gz> PROBES=<E1b probes.jsonl> [JMUT=<jmut_cc504.py>] [GPU=1] \
#   [HG=1 PY_LB=<venv-lb python, transformers 4.57.6> HF_HOME=<cache> SMOKE_IMAGES=<dir> SMOKE_NAMES="f1 .. f5"] ./host_selftest.sh <OUT dir>
#
# H1 freeze (+ GPU=1: transformers 4.51.3 and trl 0.19.1, repo requirements.txt; torch/peft/bitsandbytes recorded)
# H2 repo snapshot from the named commit; the package refuses on any REUSED mismatch
# H3 run_tests.sh (self-tests + own, W3/W5 and judge mutants; JMUT also runs the judge's script unchanged)
# H4 P0r inputs: records tarball b312de68, probes ffd27917 (OPS-1031e1bdone); 0 gender_uncap; no_q all REJECTED
# H-G (HG=1, GPU, before G1/G2): download the three pinned models (Vintern b98f263e and Qwen2.5-VL-7B cc594898 into the HF cache with
#     refs/main = the pin, as E1b/E1a; InternVL3-8B-hf 259a3b64 via decode_hf_vlm.fetch; B-N1 file pins checked), then
#     g12.py smoke on 5 already-explored M-HalDetect val images (CC-501 ruling 6): token check, finite s, median
#     mass >= 0.5 over 20 probes, InternVL3 batch-8 agreement on those 5 images, student batch-1 repeat equality and non-empty captions (batch-5 parity and first differing positions recorded only; Q13 decides the decode batch)
# Writes counts and shas only. Exit 0 iff every item passes; the last line of OUT/host_selftest.log says so.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
: "${O31_BASE:?O31_BASE (the job folder, E1 O-H1)}"
BASE="$(readlink -f "$O31_BASE")"
inside() { case "$(readlink -f "$1")" in "$BASE"/*) return 0;; *) return 1;; esac; }
OUT="${1:?usage: host_selftest.sh <OUT dir>}"
: "${PY:?PY}" "${REPO_TAR:?REPO_TAR}" "${COMMIT:?COMMIT}" "${RECORDS_TAR:?RECORDS_TAR}" "${PROBES:?PROBES}"
RECORDS_SHA=b312de68180a2f9bf31602bae917ed170b2630174c30c11e9ea59c64aff840b0
PROBES_SHA=ffd2791721912683964145cc6954d1ada471495cb9ba9898eb928a073fb32cc8
mkdir -p "$OUT"
LOG="$OUT/host_selftest.log"
: > "$LOG"
say() { echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }
fail() { say "FAIL $*"; echo "FAIL $*" >&2; exit 1; }

# O-H1/O-H2 (ERRATUM_O31_2 E1) ---------------------------------------------------------------------------------
for v in PY ${PY_LB:+PY_LB}; do
  inside "${!v}" || fail "O-H2 $v is not inside O31_BASE"
  [ "$("${!v}" -I -c 'import platform; print(platform.python_implementation(), platform.python_version())')" = "CPython 3.12.3" ] \
    || fail "O-H2 $v is not CPython 3.12.3"
  say "O-H2 $v $(readlink -f "${!v}")"
done
for v in TMPDIR HF_HOME PIP_CACHE_DIR; do
  [ -n "${!v:-}" ] && inside "${!v}" || fail "O-H1 $v must be set inside O31_BASE"
done
inside "$OUT" || fail "O-H1 OUT is not inside O31_BASE"
[ -z "$(find "$BASE" -name .git -print -quit)" ] || fail "O-H3 a .git folder is inside O31_BASE"
say "O-H1 O-H3 PASS (folder, caches, no .git)"

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
mkdir -p "$TMPDIR"
PY="$PY" VSPS_REPO="$REPO" bash "$HERE/run_tests.sh" > "$OUT/run_tests.log" 2>&1 || fail "H3 run_tests.sh (see run_tests.log)"
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
if [ "${HG:-0}" = 1 ]; then
  : "${PY_LB:?PY_LB}" "${HF_HOME:?HF_HOME}" "${SMOKE_IMAGES:?SMOKE_IMAGES}" "${SMOKE_NAMES:?SMOKE_NAMES}"
  "$PY_LB" -I -B -c "import importlib.metadata as m; v = m.version('transformers'); print('H-G venv-lb transformers', v); assert v == '4.57.6'" >> "$LOG" 2>&1 \
    || fail "H-G venv-lb is not transformers 4.57.6"
  SNAPS="$OUT/models" && mkdir -p "$SNAPS"
  fetch() {  # $1 python, $2 B-N1 key
    VSPS_REPO="$REPO" "$1" -I -B -c "import sys; from pathlib import Path; sys.path.insert(0, '$HERE/src'); import o31; o31.repo(); \
import decode_hf_vlm as LB; from o31.probe import registry_entry; LB.fetch({'models': {'$2': registry_entry('$2')}}, '$2', Path('$SNAPS/$2'))" \
      >> "$LOG" 2>&1 || fail "H-G fetch $2"
  }
  fetch "$PY_LB" internvl3_8b
  QREV=cc594898137f460bfe9f0759e9844b3ce807cfb5  # Qwen goes to the HF cache: stage-1 (G1) loads it by hub id
  "$PY" -I -B -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen2.5-VL-7B-Instruct', revision='$QREV')" \
    >> "$LOG" 2>&1 || fail "H-G fetch qwen"
  QDIR="$HF_HOME/hub/models--Qwen--Qwen2.5-VL-7B-Instruct"
  [ -f "$QDIR/refs/main" ] || { mkdir -p "$QDIR/refs" && printf %s "$QREV" > "$QDIR/refs/main"; }
  HF_HUB_OFFLINE=1 VSPS_REPO="$REPO" "$PY" -I -B -c "import sys; from pathlib import Path; sys.path.insert(0, '$HERE/src'); \
from o31 import stage1; stage1.check_qwen(Path('$QDIR/snapshots/$QREV'))" >> "$LOG" 2>&1 || fail "H-G Qwen pins (B-N1)"
  VREV=b98f263eab246eb5269ade64edbdca8a887dc44d
  "$PY" -I -B -c "from huggingface_hub import snapshot_download; snapshot_download('5CD-AI/Vintern-1B-v3_5', revision='$VREV')" >> "$LOG" 2>&1 \
    || fail "H-G fetch vintern"
  VDIR="$HF_HOME/hub/models--5CD-AI--Vintern-1B-v3_5"
  [ -f "$VDIR/refs/main" ] || { mkdir -p "$VDIR/refs" && printf %s "$VREV" > "$VDIR/refs/main"; }
  [ "$(cat "$VDIR/refs/main")" = "$VREV" ] || fail "H-G Vintern refs/main is not the pin"
  run_smoke() {  # $1 python, $2 family, $3 snapshot
    HF_HUB_OFFLINE=1 VSPS_REPO="$REPO" "$1" -I -B "$HERE/g12.py" smoke --family "$2" --snapshot "$3" --images "$SMOKE_IMAGES" \
      --names $SMOKE_NAMES --out "$OUT/hg" >> "$LOG" 2>&1 || fail "H-G smoke $2 (see smoke_$2.json)"
    say "H-G smoke $2 PASS; smoke_$2.json sha256 $(sha256sum "$OUT/hg/smoke_$2.json" | cut -d' ' -f1)"
  }
  run_smoke "$PY" vintern "$VDIR/snapshots/$VREV"
  run_smoke "$PY_LB" internvl3 "$SNAPS/internvl3_8b"
  run_smoke "$PY" student "$QDIR/snapshots/$QREV"
  "$PY_LB" -m pip freeze > "$OUT/pip_freeze_lb.txt"
  say "H-G venv-lb pip_freeze sha256 $(sha256sum "$OUT/pip_freeze_lb.txt" | cut -d' ' -f1)"
  say "H-G PASS"
fi
TAG="H1-H4"; [ "${HG:-0}" = 1 ] && TAG="H1-H4 + H-G"
say "ALL PASS $TAG"
echo "ALL PASS $TAG; log $LOG"
