#!/usr/bin/env bash
# Paper B -> Language Resources and Evaluation (Springer Nature sn-jnl, sn-apa), built from the rewritten draft
# in paper/rev_2026-11-15/ (paper.md, online_resource.md, title_page.md) and paper/paperB.bib.
# build_B_springer.sh (the build of the earlier text) is not changed and still reads its own path.
# Outputs, all in $OUT (default: a new temporary folder), never in the repository:
#   paperB_LRE.pdf   main text; ESM_1.pdf, ESM_2.pdf   Online Resources 1 and 2; report.txt
# Use: page count, placeholders left, citation mentions without a bib entry. It is a working build:
# keys that are cited but not yet in paperB.bib stay as typed text and are listed in report.txt.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
paper=$(cd "$here/.." && pwd)
src=${SRC:-$paper/rev_2026-11-15}
out=${OUT:-$(mktemp -d)}
job=paperB_LRE
mkdir -p "$out"
cp "$here"/templates/springer_sn_jnl/sn-jnl.cls "$here"/templates/springer_sn_jnl/bst/sn-apacite.bst \
   "$here"/shims.tex "$paper"/paperB.bib "$out"/
# Same DOI patch of the scratch copy of sn-apacite.bst as in build_B_springer.sh (DOI on every entry type).
python3 - "$out"/sn-apacite.bst <<'PY'
import sys
p = sys.argv[1]; t = open(p).read()
old = """FUNCTION {fin.entry}
{ %doi empty$
  %  'skip$
  %  { output.new.block
  %    format.doi
  %  }
  % if$
  output.end.block"""
new = """FUNCTION {fin.entry}
{ type$ "article" = type$ "magazine" = or type$ "newspaper" = or
  doi empty$ or
    'skip$
    { output.new.block
      format.doi
    }
  if$
  output.end.block"""
assert t.count(old) == 1
open(p, "w").write(t.replace(old, new))
PY

# Split the draft: title, abstract and keywords -> meta.yaml; Sections 1 to 9 and the declarations -> body.md
# (the key list under "## References" is a drafting aid; the list is made by BibTeX); the two Online Resources.
python3 - "$here" "$src" "$paper" "$out" <<'PY'
import json, re, sys
from pathlib import Path
here, src, paper, out = map(Path, sys.argv[1:])
sys.path.insert(0, str(here))
from prep import visible, section, yaml_block


def write(name, text):
    # A table follows its caption line directly in the draft; pandoc needs an empty line between them.
    (out / name).write_text(re.sub(r"(?m)^(\*\*Table [^\n]*)\n(?=\|)", r"\1\n\n", text), encoding="utf-8")


md = visible((src / "paper.md").read_text(encoding="utf-8"))
title = re.search(r"^# (.+)$", md, re.M).group(1).strip()
kw = re.search(r"^\*\*Keywords:\*\*\s*(.+)$", md, re.M).group(1)
abstract = re.sub(r"^\*\*Keywords.*$", "", section(md, "Abstract"), flags=re.M).strip()
body = md[md.index("\n## 1 "):md.index("\n## References")]
write("body.md", body)
(out / "meta.yaml").write_text(
    f"title: {json.dumps(title, ensure_ascii=False)}\n" + yaml_block("abstract", abstract)
    + "keywords:\n" + "".join(f"  - {json.dumps(k.strip(), ensure_ascii=False)}\n" for k in kw.split(";")), encoding="utf-8")
res = visible((src / "online_resource.md").read_text(encoding="utf-8"))
cut = res.index("\n# Online Resource 2")
write("ESM_1.md", res[:cut])
# Online Resource 2 = its frame (S.0), Sections S1 to S15 (the supplement of the earlier version, as its file
# stands in the repository) and Sections S16 to S28.
frame, moved = res[cut:].split("\n## S16 ", 1)
old = visible((paper / "supplementary_B.md").read_text(encoding="utf-8"))
old = re.sub(r"\A\s*# [^\n]*\n", "", old)  # its own title line; the frame carries the title
write("ESM_2.md", frame + "\n" + old + "\n\n## S16 " + moved)
PY

# Author block: from the title page when it has the "Name^a^" lines of the earlier title page, else a mark.
authorblock=$(python3 "$here"/prep.py authors "$src"/title_page.md 2>/dev/null) \
  || authorblock='\author*[1]{\fnm{[AUTHORS: to be set]}}\affil[1]{\orgname{[AUTHORS: to be set]}}'

pandoc -f bibtex -t csljson "$paper"/paperB.bib > "$out"/bib.json
python3 "$here"/prep.py cites "$out"/bib.json "$paper"/citation_map_B.tsv B "$out"/B "$out"/body.md

pandoc "$out"/body.md -f markdown+lists_without_preceding_blankline -t latex --shift-heading-level-by=-1 --template "$here"/sn_jnl.pandoc.tex \
  --metadata-file "$out"/meta.yaml --lua-filter "$here"/filter.lua -V authorblock="$authorblock" \
  -V nocite="$(cat "$out"/B_keys.txt)" -V bibs=paperB -o "$out"/$job.tex

cd "$out"
latexmk -xelatex -interaction=nonstopmode -f $job.tex > latexmk.txt 2>&1 || true
for n in 1 2; do
  pandoc ESM_$n.md --pdf-engine=xelatex -V mainfont="DejaVu Serif" -V geometry:margin=2.5cm \
    -o ESM_$n.pdf > ESM_${n}_build.txt 2>&1 || true
done
{ python3 "$here"/prep.py check . $job body.md
  cat B_cites_report.txt
  for n in 1 2; do [ -f ESM_$n.pdf ] && echo "ESM_$n.pdf: $(pdfinfo ESM_$n.pdf | grep ^Pages)" || echo "ESM_$n.pdf: NOT BUILT (see ESM_${n}_build.txt)"; done
  python3 - "$here" "$src" <<'PY'
import collections, re, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from prep import visible
text = "".join(visible((Path(sys.argv[2]) / f).read_text(encoding="utf-8")) for f in ("paper.md", "online_resource.md", "title_page.md", "cover_letter.md"))
marks = collections.Counter(re.findall(r"\[(AUTHOR TO PROVIDE|AUTHOR TO CONFIRM|AUTHORS:|TO CONFIRM|TO VERIFY|TO RE-VERIFY|CITE-TO-VERIFY|PI-\d ANCHOR|FIGURE TO BUILD)", text))
print("marks left in the visible text of the four draft files:", dict(sorted(marks.items())) or "none")
PY
  echo "output folder: $out"; } | tee report.txt
