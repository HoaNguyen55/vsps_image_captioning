#!/usr/bin/env bash
# B-ALT (FE-LOCUS) host set-up check and S0 (prereg v2 §5 as amended by ERRATUM_B_ALT_1, CC-510e2): host (a) the
# D1 rented host if still running under its existing payment, else host (b) the PI's PC in one own folder (H1).
# Run ON the host from the pushed tree:  BALT_BASE=<own folder> bash <own folder>/b_alt_tree/scripts/b_alt/host_selftest.sh
# BALT_BASE defaults to /root (host a). On host b every path below lives under BALT_BASE (H1); push by tar (H2).
# Expects: $BALT_BASE/b_alt_tree (exactly PUSH_LIST.txt), PY3 = a CPython 3.12.3 interpreter inside $BALT_BASE (CC-512e1;
# the host's system python is never used), `java` on PATH reporting 21.0.13.0.3, and the
# VnCoreNLP 1.2 jar + models at $NCS_DATA/vncorenlp (default $BALT_BASE/ncs-data). Reuses $BALT_BASE/venv-bd1 and
# $BALT_BASE/bd1-wheels when present (the D1 set-up, same wheel list), else builds them the same way. Writes only those,
# $BALT_BASE/outputs_b_alt_checks and $BALT_BASE/b_alt_records (its own 8 CPU-h budget). No host name, IP or port is written.
set -u
B=${BALT_BASE:?set BALT_BASE to the own folder of erratum H1 (host (a) no longer exists)}
P3=${PY3:?set PY3 to the CPython 3.12.3 interpreter inside BALT_BASE (CC-512e1)}
TREE=$B/b_alt_tree; V=$B/venv-bd1; WH=$B/bd1-wheels; O=$B/outputs_b_alt_checks; R=$B/b_alt_records
export NCS_DATA=${NCS_DATA:-$B/ncs-data} CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=2
N="nice -n 19 ionice -c3"
mkdir -p "$O"
fail() { echo "HOST_SELFTEST FAIL: $*" | tee -a "$O/host_selftest.log"; exit 1; }
cd "$TREE" || fail "no tree"
# 0. tools (install bundle: time, util-linux)
[ -x /usr/bin/time ] && /usr/bin/time -v true > /dev/null 2>&1 || fail "GNU time missing (install bundle: time)"
prlimit --cpu=10 true || fail "prlimit missing (install bundle: util-linux)"
[ -d "$NCS_DATA/vncorenlp/models" ] || fail "VnCoreNLP models missing under NCS_DATA/vncorenlp"
# 1. tree: exactly the push list, scripts/b_alt/SHA256SUMS, the registration (PINS are checked by b_alt.py at import)
(find . -type f | sed 's#^\./##' | sort) > "$O/tree_files.txt"
sort scripts/b_alt/PUSH_LIST.txt | diff - "$O/tree_files.txt" > "$O/tree_diff.txt" || fail "tree differs from PUSH_LIST.txt"
(cd scripts/b_alt && sha256sum -c SHA256SUMS) > "$O/b_alt_sha_check.txt" 2>&1 || fail "scripts/b_alt sha256"
sha256sum manuscript/prereg/2026-11-27_b_alt/PREREG_DRAFT_B_ALT_v2.md | grep -q '^ed05acdb7682b516738b00d2741fd87d0220e30eec9aa38ae5a2a92c3014f352 ' \
  || fail "registration sha"
sha256sum manuscript/prereg/2026-11-27_b_alt/ERRATUM_B_ALT_1.md | grep -q '^8367faceffbd2235d2c4cfe2a0b768c37e0e1d357140a995db5359c9a884958f ' \
  || fail "erratum sha"
[ -z "$(find "$TREE" -name .git)" ] || fail "a .git directory is in the tree (H2)"
[ -e "$R/STOP" ] && fail "a STOP marker exists in $R"
# 2. interpreter and Java at their pins; the jar at its FULL sha256 (CC-510r2 N8)
P3R=$(readlink -f "$P3") || fail "PY3 not found"
case $P3R in "$(readlink -f "$B")"/*) ;; *) fail "PY3 is not inside BALT_BASE (H1)";; esac
[ "$("$P3R" -c 'import platform; print(platform.python_implementation(), platform.python_version())')" = "CPython 3.12.3" ] \
  || fail "PY3 is not CPython 3.12.3"
{ echo "PY3 $P3R"; sha256sum "$P3R"; "$P3R" -c 'import sys; print(sys.version)'; } > "$O/interpreter.txt" 2>&1 || fail "interpreter record"
JR=$(readlink -f "$(command -v java)") || fail "java not on PATH"
{ echo "java $JR"; sha256sum "$JR"; } > "$O/java_path.txt" 2>&1 || fail "java record"
java -version > "$O/java_version.txt" 2>&1
grep -q 'version "21.0.13.0.3"' "$O/java_version.txt" || fail "java is not 21.0.13.0.3"
sha256sum "$NCS_DATA/vncorenlp/VnCoreNLP-1.2.jar" > "$O/jar_sha256.txt" 2>&1 \
  && grep -q '^9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793 ' "$O/jar_sha256.txt" || fail "jar off its full pin"
# 3. venv from the FE-CERT wheel set (WHEELS_SHA256.txt = byte copy of scripts/b_d1/WHEELS_SHA256.txt)
sha256sum scripts/b_alt/WHEELS_SHA256.txt | grep -q '^51cc87787787c8f81cf9801464e25c3696179a4214ed3a2242fa9d64042f615a ' || fail "wheel list sha"
if [ ! -x "$V/bin/python" ]; then
  $N "$P3R" -m venv "$V" || fail venv
  $N "$V/bin/python" -m pip install -q pip==24.3.1 || fail "pip 24.3.1"
  mkdir -p "$WH"
  while read -r _h f; do
    n=${f%%-[0-9]*}; v=${f#"$n"-}; v=${v%%-*}
    $N "$V/bin/python" -m pip download -q --no-deps --only-binary=:all: --dest "$WH" "$n==$v" || fail "pip download $n==$v"
  done < scripts/b_alt/WHEELS_SHA256.txt
  $N "$V/bin/python" -m pip install -q --no-index --find-links "$WH" pyvi==0.1.1 underthesea==9.5.0 pycocoevalcap==1.2 \
    numpy==2.5.4 scipy==1.18.1 || fail "pip install"
fi
while read -r _h f; do [ -f "$WH/$f" ] || fail "listed wheel not downloaded: $f"; done < scripts/b_alt/WHEELS_SHA256.txt
(cd "$WH" && sha256sum *) > "$O/wheels_sha256.txt"
while read -r h f; do grep -q "^$h  $f\$" scripts/b_alt/WHEELS_SHA256.txt || fail "wheel not in the pinned list: $f"; done \
  < "$O/wheels_sha256.txt"
"$V/bin/python" -m pip freeze > "$O/pip_freeze.txt"
# 4. S0 under this study's CPU accounting: self-tests, mutants, toy environment record
PY="$V/bin/python" bash scripts/b_alt/run_stage.sh s0 "$R" - - "$WH" > "$O/s0.log" 2>&1 || fail "S0 (see s0.log)"
grep -qE '^selftest: ([0-9]+) ok of \1 checks$' "$O/s0.log" && grep -qE '^killed ([0-9]+) of \1$' "$O/s0.log" \
  && grep -q "^ENV OK$" "$O/s0.log" || fail "S0 summary lines"
cp "$R"/s0.*.time "$O/" || fail "S0 CPU record"
find "$TREE" -name __pycache__ | grep -q . && fail "bytecode written into the tree"
(cd "$O" && sha256sum *) > "$B/outputs_b_alt_checks.sha256"
echo "HOST_SELFTEST PASS" | tee -a "$O/host_selftest.log"
