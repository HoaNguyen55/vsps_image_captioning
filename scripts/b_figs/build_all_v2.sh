#!/usr/bin/env bash
# Paper B figures and Table 6 from the held result files. Run on the rented host, from any directory.
# Supersedes build_all.sh (left unchanged): adds Fig. 1 (schematic, no input) and Fig. EF1.
#   build_all_v2.sh            build Fig. 1, Fig. 2, Fig. 3, Fig. EF1 and the Table 6 comparison (exit non-zero on any failure)
#   build_all_v2.sh --selftest run the selftest of each script (synthetic inputs only; no held file is read)
# Requires python3 with matplotlib installed (no other dependency, no network).
# Fig. EF1 drawing choices are ruled by CC-428 (SPEC_ADDENDUM_EF1.md, O1 to O5). The three scripts of build_all.sh run first.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-build}"
case "$MODE" in
  build) ARG="" ;;
  --selftest) ARG="--selftest" ;;
  *) echo "usage: $0 [--selftest]" >&2; exit 2 ;;
esac

for script in fig2_breaking.py fig3_human.py table6_human.py fig1_schematic.py figEF1.py; do
  echo "== $script $ARG"
  python3 "$HERE/$script" $ARG
done
echo "== done ($MODE)"
