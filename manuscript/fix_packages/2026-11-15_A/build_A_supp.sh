#!/usr/bin/env bash
# Paper A -> Signal Processing: Image Communication: the two upload files that build_A_cas.sh does not make.
#   paperA_SPIC_supplementary.pdf  from supplementary_SPIC.md (the published copy that scrub_supp.py writes
#                                  from supplementary.md), with Fig. S1 from the vector PDF in figs/ and
#                                  its caption from figs/CAPTIONS.md (filter.lua)
#   highlights_A.docx              the bullet lines of highlights_A.md, comments removed
# The sources are never written. Output goes to $OUT (default outside the repo), never into paper/.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
src=$(cd "$here/.." && pwd)
out=${OUT:-${TMPDIR:-/tmp}/paperA_supp_build}
job=paperA_SPIC_supplementary
mkdir -p "$out"/figs
cp "$src"/figs/fig4_lambda_channels.pdf "$out"/figs/
cp "$here"/shims.tex "$out"/
cd "$out"
pandoc "$src"/supplementary_SPIC.md -f markdown -t latex -s --lua-filter "$here"/filter.lua \
  -V documentclass=article -V papersize=a4 -V geometry:margin=25mm -H shims.tex -o $job.tex
latexmk -xelatex -interaction=nonstopmode -f $job.tex > latexmk_supp.txt 2>&1 || true
grep '^- ' "$src"/highlights_A.md | sed 's/<!--.*-->//' | pandoc -f markdown -o highlights_A.docx
{ grep -E '^Output written' $job.log || echo "NO PDF: see $out/latexmk_supp.txt"
  echo "undefined references: $(grep -c 'undefined' $job.log || true)"
  echo "missing characters: $(grep -c '^Missing character' $job.log || true)"
  echo "overfull boxes: $(grep -c '^Overfull' $job.log || true)"
  echo "highlights: $(grep -c '^- ' "$src"/highlights_A.md) bullets -> highlights_A.docx"; } | tee report_supp.txt
