"""merge_search.py WORKDIR -> merged.json: records of all queries, de-duplicated; prints counts per step 0 and the scripted part of step 1."""
import glob, json, os, re, sys, xml.etree.ElementTree as ET
W = sys.argv[1]
recs = []
def add(src, qid, title, abstract, date, doi=None, arxiv=None, venue=None, oid=None):
    recs.append(dict(src=src, q=qid, title=re.sub(r"\s+", " ", title or "").strip(), abstract=re.sub(r"\s+", " ", abstract or "").strip(),
                     date=date or "", doi=(doi or "").lower().replace("https://doi.org/", "") or None, arxiv=arxiv, venue=venue or "", oid=oid))
for f in sorted(glob.glob(os.path.join(W, "raw", "OA-*_p*.json"))):
    qid = os.path.basename(f).split("_p")[0]
    for r in json.load(open(f, encoding="utf-8")).get("results", []):
        inv = r.get("abstract_inverted_index") or {}
        pos = sorted((p, w) for w, ps in inv.items() for p in ps)
        doi = (r.get("doi") or "").lower().replace("https://doi.org/", "")
        m = re.match(r"10\.48550/arxiv\.(\d{4}\.\d{4,5})", doi)
        src = ((r.get("primary_location") or {}).get("source") or {}).get("display_name")
        add("OpenAlex", qid, r.get("title"), " ".join(w for _, w in pos), r.get("publication_date"), doi, m.group(1) if m else None, src, r["id"].split("/")[-1])
ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
for f in sorted(glob.glob(os.path.join(W, "raw", "AX-*_s*.xml"))):
    qid = os.path.basename(f).split("_s")[0]
    for e in ET.parse(f).getroot().findall("a:entry", ns):
        aid = re.sub(r"v\d+$", "", e.find("a:id", ns).text.rsplit("/", 1)[-1])
        doi = e.find("x:doi", ns)
        add("arXiv", qid, e.find("a:title", ns).text, e.find("a:summary", ns).text, e.find("a:published", ns).text[:10],
            doi.text if doi is not None else None, aid, (e.find("x:journal_ref", ns).text if e.find("x:journal_ref", ns) is not None else ""))
for f in sorted(glob.glob(os.path.join(W, "raw", "S2-*.json"))):
    qid = os.path.basename(f)[:-5]
    try: data = json.load(open(f, encoding="utf-8")).get("data") or []
    except Exception: data = []
    for r in data:
        x = r.get("externalIds") or {}
        add("SemanticScholar", qid, r.get("title"), r.get("abstract"), r.get("publicationDate") or str(r.get("year") or ""), x.get("DOI"), x.get("ArXiv"), r.get("venue"))
print("records fetched:", len(recs), {s: sum(1 for r in recs if r["src"] == s) for s in ("OpenAlex", "arXiv", "SemanticScholar")})
norm = lambda t: re.sub(r"[^a-z0-9]+", "", t.lower())
groups, key2g = [], {}
for r in recs:
    keys = [k for k in (("ax", r["arxiv"]) if r["arxiv"] else None, ("doi", r["doi"]) if r["doi"] and not r["doi"].startswith("10.48550/") else None, ("t", norm(r["title"])) if r["title"] else None) if k]
    g = next((key2g[k] for k in keys if k in key2g), None)
    if g is None:
        g = dict(recs=[]); groups.append(g)
    g["recs"].append(r)
    for k in keys: key2g[k] = g
works = []
for g in groups:
    rs = g["recs"]
    best = max(rs, key=lambda r: len(r["abstract"]))
    works.append(dict(title=max((r["title"] for r in rs), key=len), abstract=best["abstract"], date=min((r["date"] for r in rs if r["date"]), default=""),
                      doi=next((r["doi"] for r in rs if r["doi"] and not r["doi"].startswith("10.48550/")), None), arxiv=next((r["arxiv"] for r in rs if r["arxiv"]), None),
                      venue=next((r["venue"] for r in rs if r["venue"] and "arxiv" not in r["venue"].lower()), ""), found=sorted({r["q"] for r in rs}), oid=next((r["oid"] for r in rs if r["oid"]), None)))
print("step 0, unique works:", len(works))
KW = ("in-context", "in context", "few-shot", "few shot", "retriev", "demonstration", "example selection", "exemplar", "prompt")
def scripted(w):
    t = (w["title"] + " " + w["abstract"]).lower()
    return "caption" in t and any(k in t for k in KW)
for w in works: w["pass1a"] = scripted(w)
print("step 1a (script: 'caption' and one method term in title or abstract):", sum(w["pass1a"] for w in works), "pass;", sum(not w["pass1a"] for w in works), "dropped; without abstract:", sum(1 for w in works if not w["abstract"]))
works.sort(key=lambda w: (not w["pass1a"], w["title"].lower()))
for i, w in enumerate(works, 1): w["n"] = i
json.dump(works, open(os.path.join(W, "merged.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
