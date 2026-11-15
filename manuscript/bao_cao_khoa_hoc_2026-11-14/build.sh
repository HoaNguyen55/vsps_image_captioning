#!/usr/bin/env bash
# Build the report: resolve the citations of each part from that paper's .bib, join the parts, write DOCX and PDF.
#   bash build.sh            (run from anywhere; output in this folder and in build/)
set -euo pipefail
cd "$(dirname "$0")"
A=/mnt/d/vsps_papers/vsps-paperA-spic/paper
B=/mnt/d/vsps_papers/vsps-paperB-lre/paper
C=/mnt/d/vsps_papers/vsps-paperC-tallip/paper_v1_analysis
OUT=BAO_CAO_KHOA_HOC_VSPS_2026-11-14
mkdir -p build build/figs
for f in figs/*.svg; do rsvg-convert -z 3 "$f" -o "build/figs/$(basename "${f%.svg}").png"; done

resolve() { # resolve <part> <letter> <bib>...
  local part=$1 letter=$2; shift 2
  local args=(); for b in "$@"; do args+=(--bibliography "$b"); done
  pandoc "parts/$part.md" -f markdown --citeproc "${args[@]}" \
    -M reference-section-title="Tài liệu tham khảo của Phần $letter" -M link-citations=false \
    -t markdown-citations-simple_tables-multiline_tables-grid_tables --wrap=none \
  | sed -e "s/^# \(Tài liệu tham khảo của Phần $letter\) {#bibliography .unnumbered}/## \1/" \
        -e "s/{#refs /{#refs-$letter /" -e "s/{#ref-/{#ref-$letter-/" > "build/$part.md"
}
resolve A_report A "$A/paperA.bib" "$A/paperA_manual.bib"
resolve B_report B "$B/paperB.bib"
resolve C_report C "$C/paperC.bib"
resolve D_taimma_report D "$C/paperC.bib"
cp parts/00_mo_dau.md parts/E_tinh_trang.md build/

PARTS=(build/00_mo_dau.md build/A_report.md build/B_report.md build/C_report.md build/D_taimma_report.md build/E_tinh_trang.md)
: > "build/$OUT.md"
for p in "${PARTS[@]}"; do cat "$p"; printf '\n\n'; done >> "build/$OUT.md"
cp "build/$OUT.md" "$OUT.md"

sed 's#(figs/\([A-Za-z0-9_]*\)\.svg)#(build/figs/\1.png)#g' "$OUT.md" > build/docx_in.md
pandoc build/docx_in.md -f markdown --toc --toc-depth=2 -M toc-title="Mục lục" \
  --reference-doc=checks/reference.docx -o "$OUT.docx"

pandoc "$OUT.md" -f markdown --toc --toc-depth=2 -V toc-title="Mục lục" \
  --pdf-engine=xelatex -V mainfont="Times New Roman" -V monofont="DejaVu Sans Mono" -V fontsize=12pt \
  -V geometry:a4paper -V geometry:margin=2.3cm -V colorlinks=true -V linkcolor=black -V urlcolor=black \
  -H checks/header.tex -o "$OUT.pdf"
sha256sum "$OUT.md" "$OUT.docx" "$OUT.pdf" | tee build/SHA256SUMS
