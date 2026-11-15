"""step2view.py WORKDIR BIB GROUP -> condensed abstracts of the records that reached step 2 (GROUP: known | icl | rag | other | counts)."""
import json, re, sys, os
W, BIB, G = sys.argv[1:4]
ws = [w for w in json.load(open(os.path.join(W, "step1.json"), encoding="utf-8")) if w["step1"] == "to step 2"]
bib = open(BIB, encoding="utf-8").read()
norm = lambda t: re.sub(r"[^a-z0-9]+", "", t.lower())
known = {}
for key, body in re.findall(r"@\w+\{([^,]+),(.*?)\n\}", bib, flags=re.S):
    m = re.search(r"\btitle\s*=\s*\{(.*)\}", body)
    if m: known[norm(re.sub(r"[{}]", "", m.group(1)))[:60]] = key
ICL = re.compile(r"in-context|in context learning|few-shot|few shot|demonstration|exemplar|training-free|training free|without (any )?(fine-?tuning|training)|zero-shot prompting|prompt engineering", re.I)
PC = re.compile(r"vietnam|preregist|pre-regist|confidence interval|bootstrap", re.I)
KEY = re.compile(r"caption|in-context|retriev|random|few-shot|demonstrat|analy|robust|train|fine-tun|frozen|vietnam|preregist|confidence|bootstrap|multilingual|low-resource", re.I)
def group(w):
    if norm(w["title"])[:60] in known: return "known"
    t = w["title"] + " " + w["abstract"]
    if ICL.search(t): return "icl"
    if re.search(r"retriev", t, re.I): return "rag"
    return "other"
for w in ws: w["g"] = group(w); w["bib"] = known.get(norm(w["title"])[:60], "")
if G == "counts":
    import collections; print(collections.Counter(w["g"] for w in ws)); sys.exit()
for w in ws:
    if w["g"] != G: continue
    if G == "known": print(w["n"], w["bib"], "|", w["title"][:70]); continue
    sents = re.split(r"(?<=[.!?])\s+", w["abstract"])
    lim = {"icl": 62, "rag": 34, "other": 22}[G]
    if G == "icl": pick = [s for s in sents if re.search(r"in-context|few-shot|demonstrat|exemplar|random|retriev|training-free|analy|find|show that|Vietnam|multilingual", s, re.I)]
    elif G == "rag": pick = [s for s in sents if re.search(r"random|robust|analy|training-free|without (fine|train)|frozen|in-domain|Vietnam|multilingual|we (train|fine-tune|propose)", s, re.I)]
    else: pick = sents[:2]
    txt = " ".join(" ".join(pick).split()[:lim]) if w["abstract"] else "(no abstract)"
    flag = " [PC:" + ",".join(sorted({m.group(0).lower() for m in PC.finditer(w["title"] + " " + w["abstract"])})) + "]" if PC.search(w["title"] + " " + w["abstract"]) else ""
    print("%d %s %s%s :: %s" % (w["n"], w["date"][:4], w["title"][:80], flag, txt))
