#!/usr/bin/env bash
# Build the B-ALT push tree from PUSH_LIST.txt ONLY, on ext4, and prove the closure there.
#   bash make_tree.sh REPO CODE_DIR DEST [PYTHON]
# REPO: the vsps repository (read with `git archive` only; nothing is written to it). The pinned files come from
# commit 38067d1 (the D1 code commit; FE-CERT files unchanged there), the registration and erratum 1 from 7f7cf4f. CODE_DIR holds
# the scripts/b_alt files. DEST must not exist. Then: every PINS file and the registration are checked by sha256;
# `python -I -B` imports b_alt, cpu_guard and test_b_alt inside DEST with NCS_DATA set to an empty dir (b_alt's own
# pin_check and closure_check run at import); no __pycache__ may appear. Prints CLOSURE PASS or exits non-zero.
set -eu
REPO=$1; CODE=$2; DEST=$3; PY=${4:-python3}
[ -e "$DEST" ] && { echo "REFUSED: $DEST exists"; exit 6; }
mkdir -p "$DEST/scripts/b_alt"
PL="$CODE/PUSH_LIST.txt"
REPO_FILES=$(grep -v '^scripts/b_alt/' "$PL" | grep -v '^manuscript/prereg/2026-11-27_b_alt/')
git -C "$REPO" archive 38067d1 $REPO_FILES | tar -x -C "$DEST"
git -C "$REPO" archive 7f7cf4f manuscript/prereg/2026-11-27_b_alt/PREREG_DRAFT_B_ALT_v2.md \
  manuscript/prereg/2026-11-27_b_alt/ERRATUM_B_ALT_1.md | tar -x -C "$DEST"
for f in $(grep '^scripts/b_alt/' "$PL"); do
  b=$(basename "$f")
  [ -f "$CODE/$b" ] && cp "$CODE/$b" "$DEST/$f"
done
missing=$(cd "$DEST" && while read -r f; do [ -f "$f" ] || [ "$f" = scripts/b_alt/SHA256SUMS ] || [ "$f" = scripts/b_alt/LAPTOP_DEBUG_RUN.txt ] || echo "$f"; done < "$PL")
[ -z "$missing" ] || { echo "CLOSURE FAIL: missing from the tree: $missing"; exit 1; }
extra=$(cd "$DEST" && find . -type f | sed 's#^\./##' | sort | comm -23 - <(sort "$PL"))
[ -z "$extra" ] || { echo "CLOSURE FAIL: files outside the push list: $extra"; exit 1; }
sha256sum "$DEST/manuscript/prereg/2026-11-27_b_alt/PREREG_DRAFT_B_ALT_v2.md" | grep -q '^ed05acdb7682b516738b00d2741fd87d0220e30eec9aa38ae5a2a92c3014f352 ' \
  || { echo "CLOSURE FAIL: registration sha"; exit 1; }
sha256sum "$DEST/manuscript/prereg/2026-11-27_b_alt/ERRATUM_B_ALT_1.md" | grep -q '^8367faceffbd2235d2c4cfe2a0b768c37e0e1d357140a995db5359c9a884958f ' \
  || { echo "CLOSURE FAIL: erratum sha"; exit 1; }
EMPTY=$(mktemp -d)
(cd "$DEST" && NCS_DATA=$EMPTY $PY -X utf8 -I -B - <<'EOF'
import sys
sys.path.insert(0, "scripts/b_alt")
import b_alt, cpu_guard, test_b_alt  # noqa: F401  b_alt runs pin_check and closure_check at import
b_alt.pin_check()
b_alt.closure_check()
pl = set(open("scripts/b_alt/PUSH_LIST.txt").read().split())
assert set(b_alt.PINS) <= pl, sorted(set(b_alt.PINS) - pl)
assert b_alt.REG in pl
import os
from pathlib import Path
root = Path(".").resolve()
mods = sorted({str(Path(m.__file__).resolve().relative_to(root)) for m in list(sys.modules.values())
               if getattr(m, "__file__", None) and Path(m.__file__).is_file()
               and str(Path(m.__file__).resolve()).startswith(str(root) + os.sep)})
assert set(mods) <= pl, sorted(set(mods) - pl)
print(f"imported {len(mods)} tree modules, all in the push list")
EOF
)
rm -rf "$EMPTY"
pyc=$(find "$DEST" -name __pycache__ -o -name '*.pyc')
[ -z "$pyc" ] || { echo "CLOSURE FAIL: bytecode written: $pyc"; exit 1; }
echo "CLOSURE PASS"
