"""qcheck.py REPORT TXT_DIR -> for each table row N1..N17: every quoted string, the page(s) where it is found in that row's own full text, word count."""
import re, sys, os
MAP = {"N1":"arxiv_2405.10311","N2":"ceur_4283_paper255","N3":"arxiv_2609.27682","N4":"arxiv_2403.13164","N5":"arxiv_2312.10104",
       "N6":"acl_2024.findings-naacl.225","N7":"arxiv_2406.08707","N8":"arxiv_2305.18565","N9":"arxiv_2505.14462","N10":"arxiv_2502.17297",
       "N11":"arxiv_2610.30592","N12":"arxiv_2609.14100","N13":"ceur_4283_paper278","N14":"acl_2025.arabicnlp-sharedtasks.58",
       "N15":"arxiv_2511.01059","N16":"unige_192276","N17":"air_2026446"}
def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"-\n\s*", "", s)
    return re.sub(r"\s+", " ", s)
rep = open(sys.argv[1], encoding="utf-8").read()
bad = 0; tot = 0
for line in rep.splitlines():
    m = re.match(r"\| (N\d+) \|", line)
    if not m or m.group(1) not in MAP: continue
    pages = [norm(p) for p in open(os.path.join(sys.argv[2], MAP[m.group(1)] + ".txt"), encoding="utf-8", errors="replace").read().split("\f")]
    cells = line.split(" | ")
    body = norm(cells[-1])
    for q in re.finditer(r'"([^"]+)"', body):
        s = q.group(1); n = len(s.split())
        if n < 4: continue
        tot += 1
        where = [i for i, p in enumerate(pages, 1) if s in p]
        pre = body[max(0, q.start() - 40): q.start()]
        ok = bool(where) and n <= 25
        if not ok: bad += 1
        print(m.group(1), "|", n, "w |", "pages", where, "| before:", pre[-30:], "|", s[:60], "" if ok else "  <<<<< CHECK")
print("quotes checked:", tot, "problems:", bad)
