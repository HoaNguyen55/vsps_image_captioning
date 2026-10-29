#!/bin/bash
# Build Paper C acmart [manuscript] source + PDF in this scratch dir. Usage: build.sh <journal_draft_C dir>
set -euo pipefail
SRC=$(realpath "$1"); H=$(dirname "$(realpath "$0")"); cd "$H"
cp "$SRC/paperC.bib" .; rsvg-convert -f pdf -o fig1_ret_minus_rand.pdf "$SRC/fig1_ret_minus_rand.svg"
ABS=$(sed -n '/^## Abstract/,$p' "$SRC/00_abstract.md" | tail -n +2 | sed '/^\s*$/d')
TITLE=$(head -1 "$SRC/00_abstract.md" | sed 's/^# //')
body(){ pandoc "$@" -f markdown-implicit_figures+implicit_figures+lists_without_preceding_blankline --natbib --shift-heading-level-by=-1 --lua-filter=strip_num.lua -t latex --columns=100; }
body $(ls "$SRC"/0[1-9]_*.md "$SRC"/10_*.md | sort -V) > body.tex
body "$SRC/11_supplement_registered_rows.md" > supp_body.tex
python3 - <<'PY'
# acmart wants \Description (accessibility text) inside each figure
from pathlib import Path
p = Path("body.tex"); t = p.read_text()
g = r"\pandocbounded{\includegraphics[keepaspectratio]{fig1_ret_minus_rand.pdf}}"
assert t.count(g) == 1
p.write_text(t.replace(g, g + "\n\\Description{Forest plot of ret minus rand differences with 95 percent confidence intervals for Qwen2.5-VL, InternVL3 and the pooled estimate on four test sets: OpenViIC test, XM3600 Vietnamese test, COCO Karpathy test and NoCaps val. A solid line marks zero and a dashed line the smallest effect of interest.}"))
# acmart: the AI-use paragraph goes in the acks environment
t = p.read_text(); a = r"\textbf{Use of generative AI.}"
assert t.count(a) == 1
i = t.index(a); j = t.find("\n\n", i); j = len(t) if j < 0 else j
p.write_text(t[:i] + "\\begin{acks}\n" + t[i:j].rstrip() + "\n\\end{acks}\n" + t[j:])
# supplement: let long \texttt run ids break after _ and - (layout only)
import re
s = Path("supp_body.tex")
s.write_text(re.sub(r"\\texttt\{[^{}]*\}", lambda m: m.group(0).replace("\\_", "\\_\\allowbreak{}").replace("-", "-\\allowbreak{}"), s.read_text()))
# supplement: plain header cells; pandoc's minipage headers crash LuaTeX on consecutive longtables (layout only)
s.write_text(re.sub(r"\\begin\{minipage\}\[b\]\{\\linewidth\}\\raggedright\n(.*?)\n\\end\{minipage\}", r"\1", s.read_text()))
PY
printf '%s' "$ABS" | pandoc -f markdown -t latex > abstract.tex
mk(){ python3 - "$@" <<'PY'
import sys
from pathlib import Path
d, title, body, abstract, secnum, bib = sys.argv[1:7]
t = Path("preamble.tex").read_text()
for k, v in (("@@TITLE@@", title), ("@@BODY@@", body), ("@@ABSTRACT@@", abstract), ("@@SECNUM@@", secnum), ("@@BIB@@", bib)): t = t.replace(k, v)
Path(f"paperC_{d}.tex").write_text(t)
PY
}
mk main "$TITLE" body.tex '\begin{abstract}\input{abstract.tex}\end{abstract}' '' '\bibliographystyle{ACM-Reference-Format}\bibliography{paperC}'
mk supp "Supplementary Material: $TITLE" supp_body.tex '' '\setcounter{secnumdepth}{0}\footnotesize\setlength{\tabcolsep}{3pt}' ''
for d in main supp; do
  latexmk -g -lualatex -interaction=nonstopmode -halt-on-error paperC_$d.tex > build_$d.out 2>&1 || { tail -30 build_$d.out; exit 1; }
done
# self-contained sources for submission: inline the \input files
python3 - <<'PY'
import re
from pathlib import Path
for d, out in (("main", "paperC.tex"), ("supp", "paperC_supp.tex")):
    t = Path(f"paperC_{d}.tex").read_text()
    t = re.sub(r"\\input\{(body|supp_body|abstract)\.tex\}", lambda m: Path(m.group(1) + ".tex").read_text(), t)
    Path(out).write_text(t)
PY
cp paperC_main.pdf paperC.pdf; cp paperC_supp.pdf paperC_supp_out.pdf
