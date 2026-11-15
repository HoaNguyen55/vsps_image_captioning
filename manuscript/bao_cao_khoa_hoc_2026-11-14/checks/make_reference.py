"""Write checks/reference.docx: pandoc's default styles with Times New Roman (body 12 pt, tables 10 pt)."""
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

out = Path(sys.argv[1])
out.write_bytes(subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"], check=True, capture_output=True).stdout)
doc = Document(str(out))
for st in doc.styles:
    if st.type not in (1, 2) or st.font is None:  # paragraph and character styles
        continue
    if "Verbatim" in st.name or "Source" in st.name:
        continue
    st.font.name = "Times New Roman"
    rpr = st.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is not None:
        for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rfonts.set(qn(attr), "Times New Roman")
        for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
            if rfonts.get(qn(attr)) is not None:
                del rfonts.attrib[qn(attr)]
    if st.name.startswith("Heading") or st.name in ("Title", "TOC Heading"):
        st.font.color.rgb = RGBColor(0, 0, 0)
for name, size in (("Normal", 12), ("Body Text", 12), ("First Paragraph", 12), ("Compact", 10), ("Table Caption", 11), ("Image Caption", 11)):
    try:
        doc.styles[name].font.size = Pt(size)
    except KeyError:
        pass
doc.save(str(out))
