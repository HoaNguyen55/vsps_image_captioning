#!/usr/bin/env bash
# Paper B figures and Table 6 from the held result files. Run on the rented host, from any directory.
#   build_all.sh            build Fig. 2, Fig. 3 and the Table 6 comparison (exit non-zero on any failure)
#   build_all.sh --selftest run the selftest of each script (synthetic inputs only; no held file is read)
# Requires python3 with matplotlib installed (no other dependency, no network).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-build}"
case "$MODE" in
  build) ARG="" ;;
  --selftest) ARG="--selftest" ;;
  *) echo "usage: $0 [--selftest]" >&2; exit 2 ;;
esac

for script in fig2_breaking.py fig3_human.py table6_human.py; do
  echo "== $script $ARG"
  python3 "$HERE/$script" $ARG
done
echo "== done ($MODE)"
