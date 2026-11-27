#!/usr/bin/env bash
# B-D1 host set-up check and S0, on a fresh rented host (CC-505 ruling 9; PI-1115r install bundle first).
# Run ON the host from the pushed tree:  bash $B/b_d1_tree/scripts/b_d1/host_selftest.sh, with B = ${BD1_BASE:-/root}
# (CC-506e1: on the PI's PC, BD1_BASE is the study's own folder; the tree is $B/b_d1_tree and every other path below is
# a sibling of it, never inside it, so the closure check sees no foreign module). PY3 (default /usr/bin/python3) must
# be CPython 3.12.3; `java` on PATH must report 21.0.13.0.3; the VnCoreNLP 1.2 jar + models at $NCS_DATA/vncorenlp
# (default $B/ncs-data). Writes only $B/venv-bd1, $B/bd1-wheels, $B/outputs_b_d1_checks and the S0 records.
# No host name, IP or port is written. Exit 0 only when every step passes.
set -u
B=${BD1_BASE:-/root}; P3=${PY3:-/usr/bin/python3}
TREE=$B/b_d1_tree; V=$B/venv-bd1; WH=$B/bd1-wheels; O=$B/outputs_b_d1_checks; RC=$B/b_d1_records
export NCS_DATA=${NCS_DATA:-$B/ncs-data} CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2
N="nice -n 19 ionice -c3"
mkdir -p "$O"
fail() { echo "HOST_SELFTEST FAIL: $*" | tee -a "$O/host_selftest.log"; exit 1; }
cd "$TREE" || fail "no tree"
# 0. tools whose absence would otherwise fail inside S0 and write STOP (install bundle: time, util-linux)
[ -x /usr/bin/time ] && /usr/bin/time -v true > /dev/null 2>&1 || fail "GNU time missing (install bundle: time)"
prlimit --cpu=10 true || fail "prlimit missing (install bundle: util-linux)"
[ -d "$NCS_DATA/vncorenlp/models" ] || fail "VnCoreNLP models missing under NCS_DATA/vncorenlp"
# 1. tree: scripts/b_d1/SHA256SUMS and the registration; the PINS are checked by b_d1.py at import
(cd scripts/b_d1 && sha256sum -c SHA256SUMS) > "$O/b_d1_sha_check.txt" 2>&1 || fail "scripts/b_d1 sha256"
sha256sum manuscript/prereg/2026-11-27_b_d1/PREREG_DRAFT_B_D1_A3_v3.md | grep -q '^bf3a55f7641cc91b' || fail "registration sha"
# 2. interpreter and Java at their pins
[ "$("$P3" -c 'import platform; print(platform.python_version())')" = 3.12.3 ] || fail "python is not 3.12.3"
java -version > "$O/java_version.txt" 2>&1
grep -q 'version "21.0.13.0.3"' "$O/java_version.txt" || fail "java is not 21.0.13.0.3"
JAR=$NCS_DATA/vncorenlp/VnCoreNLP-1.2.jar
sha256sum "$JAR" > "$O/jar_sha256.txt" 2>&1 && grep -q '^9e2811cd' "$O/jar_sha256.txt" || fail "VnCoreNLP jar off its pin"
# 3. venv from the FE-CERT wheel set; every downloaded wheel must be in WHEELS_SHA256.txt
if [ ! -x "$V/bin/python" ]; then
  $N "$P3" -m venv "$V" || fail venv
  $N "$V/bin/python" -m pip install -q pip==24.3.1 || fail "pip 24.3.1"
  mkdir -p "$WH"
  while read -r _h f; do  # CC-506 N2: every wheel of the FE-CERT list at its own version, no dependency resolution
    n=${f%%-[0-9]*}; v=${f#"$n"-}; v=${v%%-*}
    $N "$V/bin/python" -m pip download -q --no-deps --only-binary=:all: --dest "$WH" "$n==$v" || fail "pip download $n==$v"
  done < scripts/b_d1/WHEELS_SHA256.txt
fi
while read -r _h f; do [ -f "$WH/$f" ] || fail "listed wheel not downloaded: $f"; done < scripts/b_d1/WHEELS_SHA256.txt
(cd "$WH" && sha256sum *) > "$O/wheels_sha256.txt"
while read -r h f; do grep -q "^$h  $f\$" scripts/b_d1/WHEELS_SHA256.txt || fail "wheel not in the pinned list: $f"; done \
  < "$O/wheels_sha256.txt"
for w in pyvi-0.1.1 underthesea-9.5.0 pycocoevalcap-1.2 numpy-2.5.4 scipy-1.18.1; do
  ls "$WH"/$w-*.whl > /dev/null 2>&1 || fail "missing wheel $w"
done
$N "$V/bin/python" -m pip install -q --no-index --find-links "$WH" pyvi==0.1.1 underthesea==9.5.0 pycocoevalcap==1.2 \
  numpy==2.5.4 scipy==1.18.1 || fail "pip install"
"$V/bin/python" -m pip freeze > "$O/pip_freeze.txt"
# 4. S0 under the CPU accounting: self-tests, mutants, toy environment record (env_check unchanged)
PY="$V/bin/python" bash scripts/b_d1/run_stage.sh s0 "$RC" - - "$WH" > "$O/s0.log" 2>&1 || fail "S0 (see s0.log)"
grep -qE '^selftest: ([0-9]+) ok of \1 checks$' "$O/s0.log" && grep -qE '^killed ([0-9]+) of \1$' "$O/s0.log" \
  && grep -q "^ENV OK$" "$O/s0.log" || fail "S0 summary lines"
cp "$RC"/s0.*.time "$O/" || fail "S0 CPU record"  # CC-506 W3: the S0 .time record is part of the record
(cd "$O" && sha256sum *) > "$O.sha256"
echo "HOST_SELFTEST PASS" | tee -a "$O/host_selftest.log"
