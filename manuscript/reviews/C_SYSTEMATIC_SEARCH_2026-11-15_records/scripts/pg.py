"""pg.py TXT REGEX [REGEX...]  -> per regex: hit count and (page, context) lines. TXT = pdftotext output with form feeds."""
import re, sys
txt = open(sys.argv[1], encoding="utf-8", errors="replace").read()
pages = txt.split("\f")
ctx = 110
for pat in sys.argv[2:]:
    rx = re.compile(pat, re.I)
    total = 0
    out = []
    for i, p in enumerate(pages, 1):
        flat = re.sub(r"-\n\s*", "", p)
        flat = re.sub(r"\s+", " ", flat)
        for m in rx.finditer(flat):
            total += 1
            if len(out) < 12:
                out.append("  p.%d: ...%s..." % (i, flat[max(0, m.start() - ctx): m.end() + ctx]))
    print("## /%s/ hits=%d" % (pat, total))
    print("\n".join(out))
