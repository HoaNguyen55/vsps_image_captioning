#!/usr/bin/env python3
"""B-alpha protocol-disclosure census (Paper B), rule manuscript/prereg/2026-10-29_b_alpha_audit/RULE_v3.md.

Commands:
  --selftest                       synthetic strings, synthetic PDFs, mocked API; network blocked
  toolcheck --out DIR              T1/T2 tool check on our own texts (no network)
  run --run --out DIR              the one live run (S1 search ... decide); refuses without --run
Laptop CPU only. No dataset file, image or caption is opened, except by the pinned n-gram scanner on quotes.tsv.
"""
import argparse, hashlib, http.client, json, os, re, shutil, signal, socket, subprocess, sys, tempfile, time, unicodedata
import urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = os.path.join(REPO, "manuscript/prereg/2026-10-29_b_alpha_audit/RULE_v3.md")
FLAGS = re.IGNORECASE | re.MULTILINE


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    with open(p, "rb") as f:
        return sha256_bytes(f.read())


def load_patterns(path=os.path.join(HERE, "patterns.json")):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_words(path=os.path.join(HERE, "english_words.txt")):
    with open(path, encoding="utf-8") as f:
        return [w.strip() for w in f if w.strip() and not w.startswith("#")]


# ---------------------------------------------------------------- text
def normalise(raw):
    """NFC, drop a line-end hyphen before a lower-case letter, collapse whitespace (RULE §1.2)."""
    t = unicodedata.normalize("NFC", raw)
    t = re.sub(r"-\n(?=\w)", lambda m: "" if t[m.end()].islower() else m.group(0), t)
    return re.sub(r"\s+", " ", t).strip()


def pre_reference(raw, P):
    """Raw text before the LAST reference heading (W2/CC-210 W4a); flag if none."""
    t = unicodedata.normalize("NFC", raw)  # search and slice the same string (CC-210a W5)
    hits = list(re.finditer(P["ref_heading"], t, FLAGS))
    if not hits:
        return t, True
    return t[: hits[-1].start()], False


def title_key(t):
    return re.sub(r"[^0-9a-z]", "", unicodedata.normalize("NFC", t or "").lower())


def e5_share(text, words):
    toks = re.findall(r"[^\W\d_]+", text.lower())
    if not toks:
        return 0.0
    ws = set(words)
    return sum(1 for t in toks if t in ws) / len(toks)


def sentence_at(text, start, end, max_words):
    a = max(text.rfind(". ", 0, start), text.rfind("! ", 0, start), text.rfind("? ", 0, start))
    a = 0 if a < 0 else a + 2
    m = re.search(r"[.!?]\s", text[end:])
    b = len(text) if not m else end + m.start() + 1
    words = text[a:b].split()
    if len(words) <= max_words:
        return " ".join(words)
    pos = len(text[a:start].split())
    lo = max(0, min(pos - max_words // 2, len(words) - max_words))
    return " ".join(words[lo: lo + max_words])


def cells(raw, P):
    """Cell booleans on the whole text, plus hit locations (page, offset, sentence) per cell."""
    pages = [normalise(p) for p in raw.split("\f")]
    whole = " ".join(pages)
    row, hits = {}, {}
    for name, pat in P["cells"].items():
        row[name] = re.search(pat, whole, FLAGS) is not None
        hits[name] = []
        for pno, ptxt in enumerate(pages, 1):
            for m in re.finditer(pat, ptxt, FLAGS):
                hits[name].append({"page": pno, "offset": m.start(),
                                   "sentence": sentence_at(ptxt, m.start(), m.end(), P["thresholds"]["quote_max_words"])})
    row["S"] = row["C1"] and (row["C2"] or row["C2t"])
    return row, hits


def included(raw, P):
    pre, no_head = pre_reference(raw, P)
    t = normalise(pre)
    return (re.search(P["dataset"], t, FLAGS) is not None and re.search(P["metric"], t, FLAGS) is not None), no_head


def body_relevant(raw, P):
    """Dataset pattern on the pre-reference full text (CC-210a W8: E5 relevance)."""
    return re.search(P["dataset"], normalise(pre_reference(raw, P)[0]), FLAGS) is not None


def metadata_relevant(rec, P):
    t = normalise((rec.get("title") or "") + " " + (rec.get("abstract") or ""))
    return re.search(P["dataset"], t, FLAGS) is not None


def inaccessible_reason(pdf_bytes, text, n_pages, rc, P):
    th = P["thresholds"]
    if pdf_bytes is None:
        return "no_oa_pdf"
    if not pdf_bytes.startswith(b"%PDF"):
        return "not_pdf"
    if rc != 0 or text is None:
        return "extract_fail"
    n = len(text.strip())
    if n < th["scanned_min_chars_total"] or n / max(n_pages, 1) < th["scanned_min_chars_per_page"]:
        return "scanned"
    return None


# ---------------------------------------------------------------- records
def rec_ids(rec):
    ids = set()
    if rec.get("doi"):
        ids.add("doi:" + rec["doi"].lower().replace("https://doi.org/", ""))
    if rec.get("arxiv"):
        ids.add("arxiv:" + rec["arxiv"].lower())
        ids.add("doi:10.48550/arxiv." + rec["arxiv"].lower())
    return ids


def type_decision(rec, P):
    """E4 (CC-210 W1): returns (keep, flag)."""
    if rec["source"] == "openalex":
        oa = P["openalex"]
        if rec.get("type") in oa["accepted_types"]:
            return True, None
        if rec.get("type") in oa["excluded_types"]:
            return False, "E4"
        return True, "type_unlisted"
    s2 = P["semantic_scholar"]
    types = rec.get("publicationTypes")
    if not types:
        return (True, None) if (rec.get("arxiv") or rec.get("doi")) else (False, "E4")
    if any(t in s2["accepted_publication_types"] for t in types):
        return True, None
    if all(t in s2["excluded_publication_types"] for t in types):
        return False, "E4"
    return True, "type_unlisted"


def dataset_record_ids(P):
    ids = set()
    for d in P["dataset_records"]:
        ids |= rec_ids({"doi": d["doi"], "arxiv": d["arxiv"]})
    return ids


def paper_type_decision(paper, P):
    """E4 at paper level (CC-210a W4). Returns (keep, flag).
    The five Q3 dataset records bypass E4. If the paper has any OpenAlex record, it is kept when at least one OpenAlex
    record is accepted or unlisted; the S2 type rule decides only papers with no OpenAlex record."""
    recs = paper["records"]
    ds = dataset_record_ids(P)
    if any(rec_ids(r) & ds for r in recs):
        return True, None
    oa = [r for r in recs if r["source"] == "openalex"]
    decisions = [type_decision(r, P) for r in (oa or recs)]
    keepers = [f for k, f in decisions if k]
    if not keepers:
        return False, "E4"
    return True, (None if None in keepers else "type_unlisted")


def merge_records(recs, P):
    """Dedup on DOI, then arXiv id, then normalised title; pre-declared merges first (W10)."""
    alias = {}
    for group in P["predeclared_merges"]:
        for i in group:
            alias[i] = group[0]
    papers = []
    for r in recs:
        keys = {alias.get(i, i) for i in rec_ids(r)}
        if title_key(r.get("title")):
            keys.add("title:" + title_key(r.get("title")))
        for p in papers:
            if p["keys"] & keys:
                p["keys"] |= keys
                p["records"].append(r)
                break
        else:
            papers.append({"keys": set(keys), "records": [r]})
    changed = True
    while changed:  # transitive closure
        changed = False
        for i in range(len(papers)):
            for j in range(i + 1, len(papers)):
                if papers[i]["keys"] & papers[j]["keys"]:
                    papers[i]["keys"] |= papers[j]["keys"]
                    papers[i]["records"] += papers.pop(j)["records"]
                    changed = True
                    break
            if changed:
                break
    return papers


def e3_match(paper, P):
    titles = {title_key(t) for t in P["e3_titles"]}
    ids = set(P["e3_ids"])
    for r in paper["records"]:
        if title_key(r.get("title")) in titles or rec_ids(r) & ids:
            return True
    return False


def in_preread(paper, P):
    return any(set(g) & paper["keys"] for g in P["preread_set"])


# ---------------------------------------------------------------- decision
def verdict(k, n_acc, n_inr, P, toolcheck_ok=True):
    th = P["thresholds"]
    if not toolcheck_ok or n_acc < th["N_acc_min"] or k is None:
        return {"verdict": "NO-GO", "k": k, "N_acc": n_acc, "N_inr": n_inr, "N_all": n_acc + n_inr, "L": None, "U": None}
    n_all = n_acc + n_inr
    L, U = k / n_all, (k + n_inr) / n_all
    v = "REFUTES" if L >= th["T"] else "PASS" if U < th["T"] else "INCONCLUSIVE"
    return {"verdict": v, "k": k, "N_acc": n_acc, "N_inr": n_inr, "N_all": n_all, "L": L, "U": U}


def decide(population, P, toolcheck_ok=True):
    """Two-way decide (CC-210 W5). population: list of dicts with status 'acc'|'inr', S (acc only), preread."""
    def count(rows):
        acc = [r for r in rows if r["status"] == "acc"]
        k = None if any("S" not in r for r in acc) else sum(1 for r in acc if r["S"])  # S exists only after cells (CC-210a W1)
        return k, len(acc), sum(1 for r in rows if r["status"] == "inr")
    prim = verdict(*count(population), P, toolcheck_ok)
    sens = verdict(*count([r for r in population if not r["preread"]]), P, toolcheck_ok)
    return {"verdict": prim["verdict"], "primary": prim,
            "verdict_without_preread": sens["verdict"], "without_preread": sens,
            "template_licensed": prim["verdict"] == "PASS" and sens["verdict"] == "PASS",
            "T": P["thresholds"]["T"]}


# ---------------------------------------------------------------- tools
def pdftotext(pdf_path, timeout):
    try:
        cp = subprocess.run(["pdftotext", "-enc", "UTF-8", pdf_path, "-"], capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, 0, 124
    if cp.returncode != 0:
        return None, 0, cp.returncode
    txt = cp.stdout.decode("utf-8", "replace")
    return txt, max(1, txt.count("\f")), 0


def render_t1(P, workdir):
    pin = P["pins"]["t1_slice"]
    with open(os.path.join(REPO, pin["path"]), encoding="utf-8") as f:
        lines = f.read().split("\n")
    md = "\n".join(lines[pin["first_line"] - 1: pin["last_line"]]) + "\n"
    if sha256_bytes(md.encode("utf-8")) != pin["sha256"]:
        raise SystemExit("FAULT: T1 slice sha differs from the pin")
    src = os.path.join(workdir, "t1.md")
    out = os.path.join(workdir, "t1.pdf")
    with open(src, "w", encoding="utf-8") as f:
        f.write(md)
    tools = P["pins"]["tools"]
    env = dict(os.environ, SOURCE_DATE_EPOCH="0")
    tex = os.path.expanduser("~/.TinyTeX/bin/x86_64-linux")
    if os.path.isdir(tex):
        env["PATH"] = tex + os.pathsep + env["PATH"]
    subprocess.run(["pandoc", src, "-o", out, "--pdf-engine=" + tools["pdf_engine"], "-V", "mainfont=" + tools["mainfont"]],
                   check=True, env=env, capture_output=True, timeout=600)
    return out


def tool_versions():
    v = {}
    v["pdftotext"] = re.search(r"([\d.]+)", subprocess.run(["pdftotext", "-v"], capture_output=True, text=True).stderr).group(1)
    v["pandoc"] = subprocess.run(["pandoc", "--version"], capture_output=True, text=True).stdout.split()[1]
    return v


def toolcheck(P, words, workdir):
    """T1 (B's card, via pandoc -> PDF) and T2 (FAIR PDF) through the population path (RULE §3)."""
    res, ok = {}, True
    t1 = render_t1(P, workdir)
    t2 = os.path.join(REPO, P["pins"]["t2_pdf"]["path"])
    if sha256_file(t2) != P["pins"]["t2_pdf"]["sha256"]:
        raise SystemExit("FAULT: T2 PDF sha differs from the pin")
    for name, pdf in (("T1", t1), ("T2", t2)):
        txt, npg, rc = pdftotext(pdf, P["thresholds"]["pdftotext_timeout_s"])
        row, _ = cells(txt or "", P)
        share = e5_share(normalise(txt or ""), words)
        exp = P["toolcheck_expected"][name]
        match = all(row[c] == exp[c] for c in exp) and share >= P["thresholds"]["e5_min_share"]
        ok &= match
        res[name] = {"pdf_sha256": sha256_file(pdf), "cells": row, "e5_share": round(share, 4), "match": match}
    res["pass"] = ok
    return res


def check_sums():
    """scripts/b_alpha/SHA256SUMS (script, patterns, word list) and the prereg folder's SHA256SUMS (RULE_v3.md)."""
    for d in (HERE, os.path.dirname(RULE)):
        with open(os.path.join(d, "SHA256SUMS")) as f:
            for line in f:
                h, name = line.split()
                if sha256_file(os.path.join(d, name)) != h:
                    raise SystemExit("FAULT: SHA256SUMS mismatch for " + name)


def rule_strings_match(P, rule_path=RULE):
    """CC-210 W9: the rule's fenced patterns block must be byte-equal to patterns.json."""
    with open(rule_path, encoding="utf-8") as f:
        rule = f.read()
    m = re.search(r"<!-- patterns.json BEGIN -->\n```json\n(.*?)```\n<!-- patterns.json END -->", rule, re.S)
    with open(os.path.join(HERE, "patterns.json"), encoding="utf-8") as f:
        return m is not None and m.group(1) == f.read()


# ---------------------------------------------------------------- network layer (run only)
class Fetcher:
    """Cached, capped, spaced HTTP. Constructed only by `run --run` (never by selftest/toolcheck)."""

    def __init__(self, P, cache_dir, log, transport=None, sleep=time.sleep, clock=time.time):
        self.P, self.cache, self.log = P, cache_dir, log
        self.transport, self.sleep, self.clock = transport or http_get, sleep, clock
        self.t0 = clock()  # the wall cap is per start (CC-210c W2)
        # caps count live requests over the start and the resume together (CC-210b W2)
        self.n_api = sum(1 for e in log if not e["cached"] and e.get("kind") == "api")
        self.n_pdf = sum(1 for e in log if not e["cached"] and e.get("kind") == "pdf")
        # a resolution 404 logged before a FAULT is replayed from the log, not re-queried (CC-210b W3)
        self.logged_404 = {e["url"] for e in log if e.get("kind") == "api" and e.get("http") == 404}
        self.last = {}
        os.makedirs(cache_dir, exist_ok=True)

    def cache_path(self, url):
        return os.path.join(self.cache, hashlib.sha1(url.encode()).hexdigest())

    def _get(self, url, kind):
        key = self.cache_path(url)
        if os.path.exists(key):
            with open(key, "rb") as f:
                body = f.read()
            self.log.append({"url": url, "kind": kind, "http": 200, "sha256": sha256_bytes(body), "cached": True})
            return body
        if kind == "api" and url in self.logged_404:
            self.log.append({"url": url, "kind": kind, "http": 404, "cached": True, "replayed": True})
            raise urllib.error.HTTPError(url, 404, "replayed from search_log", None, None)
        if self.clock() - self.t0 > self.P["caps"]["wall_h"] * 3600:
            raise CapHit("wall")
        if kind == "api":
            self.n_api += 1
            if self.n_api > self.P["caps"]["api_requests"]:
                raise CapHit("api")
        else:
            self.n_pdf += 1
            if self.n_pdf > self.P["caps"]["pdfs"]:
                raise CapHit("pdf")
        host = urllib.parse.urlparse(url).netloc
        if "semanticscholar" in host:
            wait = self.P["semantic_scholar"]["min_spacing_s"]
        elif host == "arxiv.org" or host.endswith(".arxiv.org"):
            wait = self.P["caps"]["arxiv_min_spacing_s"]  # CC-210a W6
        else:
            wait = 1
        self.sleep(max(0, self.last.get(host, 0) + wait - time.time()))
        for attempt in range(6):
            try:
                body = self.transport(url)
                break
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 5:
                    self.sleep(2 ** (attempt + 2))
                    continue
                self.log.append({"url": url, "kind": kind, "http": e.code, "cached": False})  # non-2xx logged (CC-210b W3)
                if kind == "pdf":
                    raise FetchFail(e.code)
                raise
            except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as e:
                self.log.append({"url": url, "kind": kind, "http": None, "error": type(e).__name__, "cached": False})
                if kind == "pdf":  # IncompleteRead / RemoteDisconnected included (CC-210b W1)
                    raise FetchFail(type(e).__name__)
                raise
        self.last[host] = time.time()
        with open(key, "wb") as f:
            f.write(body)
        self.log.append({"url": url, "kind": kind, "http": 200, "sha256": sha256_bytes(body), "cached": False})
        return body

    def json(self, url):
        return json.loads(self._get(url, "api"))

    def pdf(self, url):
        return self._get(url, "pdf")


class CapHit(Exception):
    pass


class FetchFail(Exception):
    """A PDF URL that failed after retries (CC-210a W6); its reason is fetch_fail, never no_oa_pdf."""



def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "b_alpha/3 (vsps-research@example.org)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def oa_record(w):
    ids = w.get("ids") or {}
    doi = (w.get("doi") or "").replace("https://doi.org/", "") or None
    arx = None
    for loc in w.get("locations") or []:
        m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", (loc.get("landing_page_url") or "") + " " + (loc.get("pdf_url") or ""))
        if m:
            arx = m.group(1)
    if doi and doi.lower().startswith("10.48550/arxiv."):
        arx = arx or doi.split(".", 2)[-1]
    inv = w.get("abstract_inverted_index") or {}
    words = sorted(((p, t) for t, ps in inv.items() for p in ps))
    return {"source": "openalex", "id": w.get("id"), "doi": doi, "arxiv": arx, "title": w.get("title"),
            "abstract": " ".join(t for _, t in words), "year": w.get("publication_year"), "type": w.get("type"),
            "type_crossref": w.get("type_crossref"), "oa_pdf": ((w.get("best_oa_location") or {}).get("pdf_url")), "openalex_ids": ids}


def s2_record(p):
    ex = p.get("externalIds") or {}
    return {"source": "s2", "id": p.get("paperId"), "doi": ex.get("DOI"), "arxiv": ex.get("ArXiv"), "title": p.get("title"),
            "abstract": p.get("abstract"), "year": p.get("year"), "publicationTypes": p.get("publicationTypes"),
            "s2_pdf": ((p.get("openAccessPdf") or {}).get("url"))}


def s1_search(F, P):
    """S1 (RULE §1.1, CC-210 W2). Returns (records, resolution log)."""
    oa, s2 = P["openalex"], P["semantic_scholar"]
    y0, y1 = P["years"]
    recs, resolution = [], []
    # Q1: resolve the five dataset records, then their citing works
    for d in P["dataset_records"]:
        r = {"name": d["name"], "openalex": None, "s2": None, "openalex_http": 200, "s2_http": 200}
        try:
            w = F.json(oa["base"] + "/works/doi:" + urllib.parse.quote(d["doi"]))
            r["openalex"] = w.get("id")
            recs.append(oa_record(w))
        except urllib.error.HTTPError as e:
            if e.code != 404:  # only 404 means "does not resolve" (CC-210a W2); anything else is a FAULT
                raise
            r["openalex_http"] = 404
        s2id = ("ARXIV:" + d["arxiv"]) if d["arxiv"] else ("DOI:" + d["doi"])
        try:
            p = F.json(s2["base"] + "/paper/" + urllib.parse.quote(s2id) + "?fields=" + s2["fields"])
            r["s2"] = p.get("paperId")
            recs.append(s2_record(p))
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
            r["s2_http"] = 404
        r["status"] = "both" if r["openalex"] and r["s2"] else "unresolved" if not (r["openalex"] or r["s2"]) else "one_source"
        resolution.append(r)
        if r["openalex"]:
            wid = r["openalex"].rsplit("/", 1)[-1]
            recs += oa_pages(F, oa, "cites:%s,publication_year:%d-%d" % (wid, y0, y1))
        if r["s2"]:
            off = 0
            while True:
                j = F.json("%s/paper/%s/citations?fields=%s&offset=%d&limit=1000" % (s2["base"], r["s2"], s2["fields"], off))
                recs += [s2_record(c["citingPaper"]) for c in j.get("data", []) if (c["citingPaper"].get("year") or 0) in range(y0, y1 + 1)]
                if j.get("next") is None:
                    break
                off = j["next"]
    # Q2: keyword arms
    for q in oa["queries"]:
        recs += oa_pages(F, oa, "%s:%s,publication_year:%d-%d" % (oa["title_abstract_filter"], q, y0, y1))
    for q in s2["queries"]:
        token = None
        while True:
            url = "%s%s?query=%s&year=%d-%d&fields=%s" % (s2["base"], s2["search_endpoint"], urllib.parse.quote(q), y0, y1, s2["fields"])
            j = F.json(url + ("&token=" + token if token else ""))
            recs += [s2_record(p) for p in j.get("data") or []]
            token = j.get("token")
            if not token:
                break
    return recs, resolution


def oa_pages(F, oa, flt):
    out, cursor = [], "*"
    while cursor:
        j = F.json("%s/works?filter=%s&per-page=%d&cursor=%s&mailto=%s" % (
            oa["base"], urllib.parse.quote(flt, safe=":,-"), oa["per_page"], cursor, F.P["contact"]))
        out += [oa_record(w) for w in j.get("results", [])]
        cursor = (j.get("meta") or {}).get("next_cursor")
        if not j.get("results"):
            break
    return out


def classify(papers, P, words, fetch_pdf, workdir, extract=None):
    """S2 fetch + S3 inclusion/exclusions. fetch_pdf(url) -> bytes|None. Returns rows, counts, fulltext manifest."""
    th = P["thresholds"]
    extract = extract or (lambda path: pdftotext(path, th["pdftotext_timeout_s"]))
    os.makedirs(workdir, exist_ok=True)
    manifest = []
    rows, counts = [], {"E1-E3": 0, "E4": 0, "E5": 0, "type_unlisted": 0, "no_ref_heading": 0,
                        "excluded_not_relevant": 0, "inaccessible_unclassifiable": 0, "pdf_cap": 0, "reasons": {}}
    for i, p in enumerate(papers):
        if e3_match(p, P):
            counts["E1-E3"] += 1
            continue
        keep, flag = paper_type_decision(p, P)
        if not keep:
            counts["E4"] += 1
            continue
        if flag == "type_unlisted":
            counts["type_unlisted"] += 1
        urls = [r.get("oa_pdf") for r in p["records"]] + [r.get("s2_pdf") for r in p["records"]] + \
               ["https://arxiv.org/pdf/" + r["arxiv"] for r in p["records"] if r.get("arxiv")]
        body, reason, txt, npg, rc = None, "no_oa_pdf", None, 0, 1
        for u in [u for u in urls if u]:
            try:
                body = fetch_pdf(u)
            except CapHit as e:
                if e.args and e.args[0] == "wall":
                    raise  # the wall cap is a FAULT at S2, not a PDF-cap event (CC-210d W1)
                body, reason = None, "pdf_cap"
                counts["pdf_cap"] += 1
                break
            except FetchFail as e:
                body, reason = None, "fetch_fail"
                manifest.append({"paper": i, "url": u, "reason": "fetch_fail", "http": e.args[0] if e.args else None})
                continue
            if body is None:
                continue
            path = os.path.join(workdir, "p%04d.pdf" % i)
            with open(path, "wb") as f:
                f.write(body)
            txt, npg, rc = extract(path) if body.startswith(b"%PDF") else (None, 0, 1)
            reason = inaccessible_reason(body, txt, npg, rc, P)
            entry = {"paper": i, "url": u, "pdf_sha256": sha256_bytes(body), "reason": reason}
            if txt is not None:
                with open(path[:-4] + ".txt", "w", encoding="utf-8") as f:
                    f.write(txt)
                entry["text_sha256"] = sha256_bytes(txt.encode("utf-8"))
            manifest.append(entry)
            if reason is None:
                break
        rel = any(metadata_relevant(r, P) for r in p["records"])
        pre = in_preread(p, P)
        base = {"keys": sorted(p["keys"]), "titles": sorted({r.get("title") or "" for r in p["records"]}),
                "types": sorted({str(r.get("type") or r.get("publicationTypes")) for r in p["records"]}),
                "type_crossref": sorted({str(r.get("type_crossref")) for r in p["records"] if r.get("type_crossref")}),
                "preread": pre}
        if reason is not None:
            counts["reasons"][reason] = counts["reasons"].get(reason, 0) + 1
            if rel:
                rows.append(dict(base, status="inr", reason=reason))
            else:
                counts["inaccessible_unclassifiable"] += 1
            continue
        share = e5_share(normalise(txt), words)
        base["e5_share"] = share
        if share < th["e5_min_share"]:
            counts["E5"] += 1
            if rel or body_relevant(txt, P):  # metadata OR pre-reference full text (CC-210a W8)
                rows.append(dict(base, status="inr", reason="E5", e5_share=share))
            continue
        inc, no_head = included(txt, P)
        counts["no_ref_heading"] += int(no_head and inc)
        if not inc:
            counts["excluded_not_relevant"] += 1
            counts.setdefault("excluded_not_relevant_e5_shares", []).append(round(share, 4))
            continue
        rows.append(dict(base, status="acc", e5_share=share, text_file="p%04d.txt" % i, _text=txt))
    return rows, counts, manifest


def now_utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def write_json(out, name, obj):
    with open(os.path.join(out, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)


def fault(out, slog, step, err):
    """Write search_log.json and FAULT.json, then exit FAULT (CC-210a W3)."""
    write_json(out, "search_log.json", slog)
    tc = os.path.join(out, "toolcheck.json")
    write_json(out, "FAULT.json", {"step": step, "error": "%s: %s" % (type(err).__name__, err), "time": now_utc(),
                                   "resumable": not (os.path.exists(os.path.join(out, "RESUMED"))
                                                     or os.path.exists(os.path.join(out, "cells.json"))),
                                   "toolcheck_sha256": sha256_file(tc) if os.path.exists(tc) else None})
    raise SystemExit("FAULT at %s: %s" % (step, err))


def open_out(args):
    """A fresh OUT, or the one allowed resume of a FAULTed OUT (CC-210a W3; RULE §1.1, §4, §7)."""
    out = args.out
    if not getattr(args, "resume", False):
        if os.path.exists(out):
            raise SystemExit("refused: --out exists (one look; use --resume only after a FAULT)")
        os.makedirs(out)
        return {"run_dates": [now_utc()], "requests": []}
    if not os.path.exists(os.path.join(out, "FAULT.json")):
        raise SystemExit("refused: --resume needs FAULT.json in --out")
    if os.path.exists(os.path.join(out, "cells.json")):
        raise SystemExit("refused: cells.json exists (no rerun after the cells, RULE §4)")
    if os.path.exists(os.path.join(out, "RESUMED")):
        raise SystemExit("refused: this OUT was already resumed once (one FAULT gives one resume in total)")
    with open(os.path.join(out, "search_log.json"), encoding="utf-8") as f:  # read before the marker is written
        slog = json.load(f)
    with open(os.path.join(out, "RESUMED"), "w") as f:
        f.write(now_utc() + "\n")
    slog["run_dates"].append(now_utc())
    return slog


def verify_cache(out, slog):
    """Every logged 2xx response must have its cache file with the logged sha; a missing or differing file is a FAULT
    with no further resume (CC-210c W3)."""
    cache = os.path.join(out, "cache")
    for e in slog["requests"]:
        if not e.get("sha256"):
            continue
        path = os.path.join(cache, hashlib.sha1(e["url"].encode()).hexdigest())
        if not os.path.exists(path):
            fault(out, slog, "resume_cache_check", ValueError("cache file missing for a logged response: " + e["url"]))
        if sha256_file(path) != e["sha256"]:
            fault(out, slog, "resume_cache_check", ValueError("cached response differs from search_log: " + e["url"]))


RUN_STATE = {}  # out, slog and the current stage of the live run, for the outermost guard (guarded_run)


def stage(name):
    RUN_STATE["stage"] = name


def run(args, P, words, transport=None, sleep=time.sleep, toolcheck_fn=None, sums_fn=None, quotes_fn=None,
        extract=None, clock=time.time):
    """The one look (RULE §4). The keyword arguments exist only for the mocked selftest; the CLI passes none."""
    if not args.run:
        raise SystemExit("refused: the live run needs --run (CC-210 W9)")
    RUN_STATE.clear()
    slog = open_out(args)
    out = args.out
    RUN_STATE.update(out=out, slog=slog)
    stage("sums")
    (sums_fn or check_sums)()
    stage("rule_strings")
    if not rule_strings_match(P):
        raise SystemExit("FAULT: RULE_v3 patterns block != patterns.json")
    if getattr(args, "resume", False):
        stage("resume_cache_check")
        verify_cache(out, slog)
    stage("toolcheck")
    tc_path = os.path.join(out, "toolcheck.json")
    if os.path.exists(tc_path):
        with open(tc_path) as f:
            tc = json.load(f)
    else:
        tc = (toolcheck_fn or toolcheck)(P, words, out)
        write_json(out, "toolcheck.json", tc)
    if not tc["pass"]:
        write_json(out, "decide.json", decide([], P, toolcheck_ok=False))
        raise SystemExit("FAULT: tool check failed; no third-party text processed")
    F = Fetcher(P, os.path.join(out, "cache"), slog["requests"], transport=transport, sleep=sleep, clock=clock)
    stage("S1")
    try:
        recs, resolution = s1_search(F, P)
    except (Exception, KeyboardInterrupt) as e:  # any S1 error incl. CapHit (also "wall"), IncompleteRead, SIGINT (CC-210c W1)
        fault(out, slog, "S1", e)
    stage("freeze")
    write_json(out, "search_log.json", slog)
    cand = json.dumps({"records": recs, "resolution": resolution}, ensure_ascii=False, indent=1).encode()
    cpath = os.path.join(out, "candidates.json")
    if os.path.exists(cpath):  # a resume after the freeze: the cache replay must rebuild the same bytes (RULE §1.1)
        with open(cpath, "rb") as f:
            if f.read() != cand:
                fault(out, slog, "resume_candidates_check", ValueError("rebuilt candidates.json differs"))
    else:
        with open(cpath, "wb") as f:
            f.write(cand)
        with open(os.path.join(out, "candidates.sha256"), "w") as f:
            f.write(sha256_bytes(cand) + "  candidates.json\n")
    print("candidates.json sha256", sha256_bytes(cand))
    stage("S2")
    try:
        papers = merge_records(recs, P)
        rows, counts, manifest = classify(papers, P, words, F.pdf, os.path.join(out, "pdf"), extract=extract)
    except (Exception, KeyboardInterrupt) as e:  # any S2 error before the cells is a FAULT with one resume (RULE §4)
        fault(out, slog, "S2", e)
    stage("population")
    write_json(out, "search_log.json", slog)
    write_json(out, "fulltext_manifest.json", manifest)
    acc = [r for r in rows if r["status"] == "acc"]
    pop = {"N_acc": len(acc), "N_inr": sum(1 for r in rows if r["status"] == "inr"), "counts": counts,
           "rows": [{k: v for k, v in r.items() if k != "_text"} for r in rows]}
    write_json(out, "population.json", pop)
    if len(acc) < P["thresholds"]["N_acc_min"]:
        stage("decide_nogo")
        d = decide(rows, P)
        d["descriptive"] = None
        write_json(out, "decide.json", d)
        print("NO-GO: N_acc < %d; no cell pattern runs" % P["thresholds"]["N_acc_min"])
        return d
    stage("S3")
    try:
        cells_out = []
        for r in acc:
            row, hits = cells(r.pop("_text"), P)
            r["S"] = row["S"]
            cells_out.append({"keys": r["keys"], "cells": row, "hits": hits})
    except (Exception, KeyboardInterrupt) as e:  # CC-210c W1
        fault(out, slog, "S3", e)
    write_json(out, "cells.json", cells_out)
    stage("decide")
    d = decide(rows, P)
    d["descriptive"] = {c: sum(1 for x in cells_out if x["cells"][c]) for c in P["cells"]}
    write_json(out, "decide.json", d)
    stage("quotes")
    (quotes_fn or write_quotes)(cells_out, P, out)
    print(json.dumps({k: d[k] for k in ("verdict", "verdict_without_preread", "template_licensed")}))
    return d


def guarded_run(args, P, words, **kw):
    """Outermost guard: once the OUT exists, nothing that Python can catch leaves it without FAULT.json and a flushed
    search_log.json (stage = the last stage entered, "unknown" if none). fault() itself raises SystemExit, which passes."""
    try:
        return run(args, P, words, **kw)
    except (Exception, KeyboardInterrupt) as e:
        out, slog = RUN_STATE.get("out"), RUN_STATE.get("slog")
        if not out or not os.path.isdir(out) or slog is None:
            raise
        fault(out, slog, RUN_STATE.get("stage", "unknown"), e)


def install_signal_faults():
    """main() only (CC-210c W1): SIGTERM always, SIGHUP unless ignored (nohup), raise KeyboardInterrupt -> FAULT."""
    def to_kbi(signum, frame):
        raise KeyboardInterrupt("signal %d" % signum)
    signal.signal(signal.SIGTERM, to_kbi)
    if hasattr(signal, "SIGHUP") and signal.getsignal(signal.SIGHUP) is not signal.SIG_IGN:
        signal.signal(signal.SIGHUP, to_kbi)


def write_quotes(cells_out, P, out):
    """quotes.tsv, then the pinned n-gram scanner; any hit -> location only (RULE §4)."""
    pin = P["pins"]["scanner"]
    scanner = os.path.join(REPO, pin["path"])
    if sha256_file(scanner) != pin["sha256"]:
        raise SystemExit("FAULT: n-gram scanner sha differs from the pin (W12)")
    rows = []
    for c in cells_out:
        for cell, hs in c["hits"].items():
            for h in hs:
                rows.append([c["keys"][0], cell, str(h["page"]), str(h["offset"]), h["sentence"].replace("\t", " ")])
    path = os.path.join(out, "quotes.tsv")
    for i, r in enumerate(rows):
        tmp = os.path.join(out, "q.tmp")
        open(tmp, "w", encoding="utf-8").write(r[4] + "\n")
        res = subprocess.run([sys.executable, scanner, tmp], capture_output=True, text=True)
        if "NGRAM SCAN PASS" not in res.stdout:
            rows[i][4] = "[location only: n-gram hit]"
        os.remove(tmp)
    with open(path, "w", encoding="utf-8") as f:
        f.write("paper\tcell\tpage\toffset\tsentence\n" + "".join("\t".join(r) + "\n" for r in rows))


# ---------------------------------------------------------------- selftest
def block_network():
    def refuse(*a, **k):
        raise RuntimeError("network blocked in selftest")
    socket.socket = refuse
    socket.create_connection = refuse
    socket.getaddrinfo = refuse


def make_pdf(text, path):
    """A tiny valid one-page PDF holding `text` (ASCII), for the extraction tests."""
    lines = text.split("\n")
    stream = "BT /F1 10 Tf 40 780 Td 12 TL " + " ".join("(%s) '" % l.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") for l in lines) + " ET"
    objs = ["<< /Type /Catalog /Pages 2 0 R >>", "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 1600] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
            "<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream), "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out, offs = b"%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += ("%d 0 obj\n%s\nendobj\n" % (i, o)).encode()
    x = len(out)
    out += ("xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)).encode() + b"".join(("%010d 00000 n \n" % o).encode() for o in offs)
    out += ("trailer << /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, x)).encode()
    open(path, "wb").write(out)


def selftest():
    block_network()
    P, words = load_patterns(), load_words()
    assert len(words) == 50 and len(set(words)) == 50
    assert P["caps"]["arxiv_min_spacing_s"] == 3 and P["semantic_scholar"]["min_spacing_s"] == 3  # CC-210a W6
    c = lambda name, s: re.search(P["cells"][name], normalise(s), FLAGS) is not None
    ds = lambda s: re.search(P["dataset"], normalise(s), FLAGS) is not None
    # must fire (CC-156 W1/W3, CC-210 W4)
    for s in ["we use word-\nlevel tokens", "word-\nsegmentation", "syllable-based tokenisation", "RDRSeg-\nmenter",
              "VnCore-\nNLP", "VnCoreNLP", "pyvi", "underthesea"]:
        assert c("C1", s), s
    for s in ["VnCore-\nNLP", "RDRSegmenter"]:
        assert c("C1t", s), s
    assert not c("C1t", "word-level attention")
    for s in ["scored with CIDEr-\nD on", "CIDEr-D", "CIDEr (D)", "CIDEr –D", "CIDEr-R"]:
        assert c("C2", s), s
    assert not c("C2", "CIDEr\nResults") and not c("C2", "CIDEr scores")
    for s in ["pycocoevalcap", "the coco-caption evaluation code", "github.com/tylin/coco-caption", "COCO evaluation toolkit",
              "COCO captioning evaluation toolkit", "MS COCO caption evaluation code", "coco-caption repository"]:
        assert c("C2t", s), s
    for s in ["Microsoft COCO Captions: Data Collection and Evaluation Server", "the MS COCO Captions dataset"]:
        assert not c("C2t", s), s
    for s in ["Open-\nViIC", "UIT-ViIC", "UIT-OpenViIC", "KTVIC", "VieCap4H", "VieCap 4H"]:
        assert ds(s), s
    assert c("C3", "scores ×100") and c("C3", "multiplied by 100") and c("C4", "Punctuation") and c("C5", "github.com/x")
    # reference heading (CC-156 W2, CC-210 W4a)
    for h in ["References", "REFERENCES", "TÀI LIỆU THAM KHẢO", "7 References", "VII. REFERENCES", "References:", "Bibliography"]:
        pre, flag = pre_reference("body KTVIC CIDEr\n%s\n[1] cited KTVIC BLEU" % h, P)
        assert not flag and "cited" not in pre, h
    pre, flag = pre_reference("Related references are many.\nKTVIC", P)
    assert flag
    # inclusion on the pre-reference text only
    assert included("We report CIDEr on KTVIC.\nReferences\n[1] x", P)[0]
    assert not included("Image captioning study.\nReferences\n[1] KTVIC dataset. [2] CIDEr.", P)[0]
    # composite and descriptive
    row, hits = cells("Captions were word-segmented with VnCoreNLP.\fWe report CIDEr-D. See github.com/x.", P)
    assert row["S"] and row["C5"] and not row["C3"] and hits["C1"][0]["page"] == 1 and hits["C2"][0]["page"] == 2
    assert not cells("We report CIDEr-D only.", P)[0]["S"]
    assert cells("Tokenised with pyvi; scored with pycocoevalcap.", P)[0]["S"]
    long = " ".join(["w%d" % i for i in range(100)]) + " VnCoreNLP " + " ".join(["v%d" % i for i in range(100)]) + "."
    assert len(cells(long, P)[1]["C1"][0]["sentence"].split()) <= 40
    # E5 (CC-156 W5)
    assert e5_share("the model is trained on the data and it is evaluated with a metric for this task", words) >= 0.15
    assert e5_share("mô hình được huấn luyện trên dữ liệu và đánh giá bằng độ đo", words) < 0.15
    # inaccessibility reasons (CC-156 W4) with synthetic PDFs
    tmp = tempfile.mkdtemp()
    try:
        body_txt = "\n".join(["We fine-tune a model on KTVIC and report CIDEr-D and BLEU scores for every split of the data."] * 30)
        good = os.path.join(tmp, "good.pdf")
        make_pdf(body_txt, good)
        txt, npg, rc = pdftotext(good, 60)
        assert rc == 0 and inaccessible_reason(open(good, "rb").read(), txt, npg, rc, P) is None, (rc, len(txt or ""))
        assert included(txt, P)[0] and cells(txt, P)[0]["C2"]
        tiny = os.path.join(tmp, "tiny.pdf")
        make_pdf("KTVIC", tiny)
        txt2, npg2, rc2 = pdftotext(tiny, 60)
        assert inaccessible_reason(open(tiny, "rb").read(), txt2, npg2, rc2, P) == "scanned"
        assert inaccessible_reason(b"<html>landing</html>", None, 0, 1, P) == "not_pdf"
        bad = os.path.join(tmp, "bad.pdf")
        open(bad, "wb").write(b"%PDF-1.4 broken")
        txt3, npg3, rc3 = pdftotext(bad, 60)
        assert inaccessible_reason(b"%PDF-1.4 broken", txt3, npg3, rc3, P) == "extract_fail"
        assert inaccessible_reason(None, None, 0, 1, P) == "no_oa_pdf"
        # classify() end to end on synthetic PDFs with a fake fetcher (no network)
        pdfs = {"u_good": open(good, "rb").read(), "u_tiny": open(tiny, "rb").read(), "u_html": b"<html>x</html>"}
        papers = [{"keys": {"doi:10.9/a"}, "records": [{"source": "openalex", "type": "article", "doi": "10.9/a", "title": "A", "oa_pdf": "u_good"}]},
                  {"keys": {"doi:10.9/b"}, "records": [{"source": "openalex", "type": "article", "doi": "10.9/b", "title": "KTVIC study", "oa_pdf": "u_tiny"}]},
                  {"keys": {"doi:10.9/c"}, "records": [{"source": "openalex", "type": "dissertation", "doi": "10.9/c", "title": "KTVIC thesis", "oa_pdf": "u_good"}]},
                  {"keys": {"doi:10.9/d"}, "records": [{"source": "s2", "publicationTypes": ["Patent"], "doi": "10.9/d", "title": "Other", "s2_pdf": "u_html"}]}]
        rows, counts, man = classify(papers, P, words, lambda u: pdfs.get(u), os.path.join(tmp, "w"))
        st = sorted((r["status"], r.get("reason")) for r in rows)
        assert st == [("acc", None), ("inr", "scanned")], st
        assert counts["E4"] == 1 and counts["type_unlisted"] == 1 and counts["inaccessible_unclassifiable"] == 1
        assert all("pdf_sha256" in m for m in man) and any("text_sha256" in m for m in man)
        assert all("e5_share" in r for r in rows if r["status"] == "acc")
    finally:
        shutil.rmtree(tmp)
    # E4 partition (CC-210 W1)
    oa = P["openalex"]
    assert not set(oa["accepted_types"]) & set(oa["excluded_types"]) and len(oa["accepted_types"] + oa["excluded_types"]) == 25
    assert "proceedings-article" not in oa["accepted_types"] + oa["excluded_types"] and "grant" not in oa["excluded_types"]
    T = lambda **kw: type_decision(dict({"source": "openalex"}, **kw), P)
    assert T(type="conference-paper") == (True, None) and T(type="dissertation") == (False, "E4") and T(type="newtype") == (True, "type_unlisted")
    S = lambda **kw: type_decision(dict({"source": "s2"}, **kw), P)
    assert S(publicationTypes=["Conference"]) == (True, None) and S(publicationTypes=["Dataset"]) == (False, "E4")
    assert S(publicationTypes=None, arxiv="2401.00001") == (True, None) and S(publicationTypes=None) == (False, "E4")
    assert S(publicationTypes=["Patent"]) == (True, "type_unlisted")
    # dedup, pre-declared merges, E3, pre-read set
    recs = [{"source": "openalex", "doi": "10.1016/j.image.2025.117430", "title": "UIT-OpenViIC: An open-domain benchmark"},
            {"source": "s2", "arxiv": "2305.04166", "title": "UIT-OpenViIC: A Novel Benchmark"},
            {"source": "s2", "doi": "10.48550/arXiv.2401.08100", "title": "KTVIC"},
            {"source": "openalex", "arxiv": "2401.08100", "title": "KTVIC: A Vietnamese Image Captioning Dataset"},
            {"source": "openalex", "doi": "10.1/x", "title": P["e3_titles"][0].upper()},
            {"source": "s2", "doi": "10.1/y", "title": "Other paper"}, {"source": "openalex", "doi": "10.1/Y", "title": "Other paper!"}]
    papers = merge_records(recs, P)
    assert len(papers) == 4, [p["keys"] for p in papers]
    assert sum(e3_match(p, P) for p in papers) == 1 and sum(in_preread(p, P) for p in papers) == 2
    # bounds, NO-GO, two-way decide (CC-210 W5)
    mk = lambda acc_s, acc_n, inr, pre=0: ([{"status": "acc", "S": i < acc_s, "preread": i < pre} for i in range(acc_n)] +
                                            [{"status": "inr", "preread": False} for _ in range(inr)])
    d = decide(mk(2, 12, 2), P)
    assert d["verdict"] == "PASS" and abs(d["primary"]["U"] - 4 / 14) < 1e-12 and d["template_licensed"]
    assert decide(mk(8, 12, 2), P)["verdict"] == "REFUTES"
    assert decide(mk(5, 12, 4), P)["verdict"] == "INCONCLUSIVE"
    assert decide(mk(2, 9, 0), P)["verdict"] == "NO-GO"
    assert decide(mk(2, 12, 2), P, toolcheck_ok=False)["verdict"] == "NO-GO"
    d3 = decide([{"status": "acc", "S": False, "preread": True}] * 2 + mk(4, 10, 1), P)  # without pre-read: N_acc 10, k 4, U 5/11
    assert d3["verdict"] == "PASS" and d3["verdict_without_preread"] == "PASS"
    d4 = decide([{"status": "acc", "S": False, "preread": True}] * 3 + mk(4, 9, 1), P)   # without pre-read: N_acc 9 -> NO-GO
    assert d4["verdict"] == "PASS" and d4["verdict_without_preread"] == "NO-GO" and not d4["template_licensed"]
    # mocked S1 (no network): a fake fetcher returning canned JSON
    class Mock:
        def __init__(s):
            s.P, s.urls = P, []
        def json(s, url):
            s.urls.append(url)
            if "/works/doi:" in url:
                return {"id": "https://openalex.org/W1", "doi": "https://doi.org/10.1/a", "title": "rec", "type": "article", "publication_year": 2024}
            if "/works?" in url:
                return {"results": [{"id": "https://openalex.org/W2", "title": "cand", "type": "conference-paper", "publication_year": 2025}] if "cursor=*" in url else [],
                        "meta": {"next_cursor": "c2" if "cursor=*" in url else None}}
            if "/citations" in url:
                return {"data": [{"citingPaper": {"paperId": "p9", "title": "c", "year": 2023}}], "next": None}
            if "/search/bulk" in url:
                assert "UIT-ViIC" not in urllib.parse.unquote(url)
                return {"data": [{"paperId": "p1", "title": "bulk hit"}], "token": None}
            if "/paper/" in url:
                raise urllib.error.HTTPError(url, 404, "nf", None, None)
            raise AssertionError(url)
    m = Mock()
    recs, res = s1_search(m, P)
    assert {r["status"] for r in res} == {"one_source"} and len(res) == 5
    assert any("title_and_abstract.search:%22Vietnamese" in u or 'title_and_abstract.search:"Vietnamese' in urllib.parse.unquote(u) for u in m.urls)
    assert sum("/search/bulk" in u for u in m.urls) == len(P["semantic_scholar"]["queries"])
    assert any("UIT%20ViIC" in u or "UIT ViIC" in urllib.parse.unquote(u) for u in m.urls if "openalex" in u)
    assert all("publication_year:2020-2026" in urllib.parse.unquote(u) for u in m.urls if "/works?" in u)
    assert all("year=2020-2026" in u for u in m.urls if "/search/bulk" in u)
    # the live path refuses without --run
    try:
        run(argparse.Namespace(run=False, out="/nonexistent"), P, words)
        raise AssertionError("run without --run")
    except SystemExit as e:
        assert "needs --run" in str(e)
    # network really is blocked here
    try:
        urllib.request.urlopen("https://api.openalex.org/works", timeout=2)
        raise AssertionError("network reachable")
    except (RuntimeError, urllib.error.URLError):
        pass
    # CC-210a unit checks: NFD cut (W5), paper-level E4 (W4), 404 vs 429 resolution (W2), S-less NO-GO (W1), E5 body relevance (W8)
    nfd = unicodedata.normalize("NFD", "Tiếng Việt được đánh giá " * 20) + "We report CIDEr on KTVIC in the final line.\nReferences\n[1] x"
    assert included(nfd, P)[0] and pre_reference(nfd, P)[0].endswith("final line.\n")
    art = {"source": "openalex", "type": "article", "doi": "10.9/a", "title": "T"}
    assert paper_type_decision({"records": [art, {"source": "openalex", "type": "dataset", "doi": "10.5281/zenodo.1", "title": "T"}]}, P) == (True, None)
    assert paper_type_decision({"records": [art, {"source": "s2", "publicationTypes": None, "title": "T"}]}, P) == (True, None)
    assert paper_type_decision({"records": [{"source": "openalex", "type": "dataset", "doi": "10.9/z"}]}, P) == (False, "E4")
    assert paper_type_decision({"records": [{"source": "openalex", "type": "dataset", "doi": "10.48550/arXiv.2401.08100"}]}, P) == (True, None)
    assert paper_type_decision({"records": [{"source": "openalex", "type": "newtype", "doi": "10.9/u"},
                                            {"source": "s2", "publicationTypes": ["JournalArticle"], "doi": "10.9/u"}]}, P) == (True, "type_unlisted")
    class Code:
        def __init__(s, code):
            s.P, s.code = P, code
        def json(s, url):
            if "/works/doi:" in url or ("/paper/" in url and "/search" not in url and "/citations" not in url):
                raise urllib.error.HTTPError(url, s.code, "x", None, None)
            return {"results": [], "meta": {}} if "/works?" in url else {"data": [], "token": None}
    recs, res = s1_search(Code(404), P)
    assert {r["status"] for r in res} == {"unresolved"} and {r["openalex_http"] for r in res} == {404}
    try:
        s1_search(Code(429), P)
        raise AssertionError("429 must not be read as unresolved")
    except urllib.error.HTTPError as e:
        assert e.code == 429
    d = decide([{"status": "acc", "preread": False} for _ in range(5)] + [{"status": "inr", "preread": False}], P)
    assert d["verdict"] == "NO-GO" and d["primary"]["k"] is None and d["primary"]["L"] is None and d["primary"]["N_all"] == 6
    assert not d["template_licensed"]
    assert body_relevant("Chúng tôi dùng KTVIC.\nReferences\n[1] x", P) and not body_relevant("x\nReferences\n[1] KTVIC", P)
    selftest_run(P, words)
    # SIGTERM -> KeyboardInterrupt (always); SIGHUP left alone when ignored (nohup) (CC-210c W1)
    old = signal.getsignal(signal.SIGTERM), signal.getsignal(signal.SIGHUP)
    try:
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        install_signal_faults()
        assert signal.getsignal(signal.SIGHUP) is signal.SIG_IGN
        try:
            os.kill(os.getpid(), signal.SIGTERM)
            time.sleep(1)
            raise AssertionError("SIGTERM not mapped")
        except KeyboardInterrupt:
            pass
        signal.signal(signal.SIGHUP, signal.SIG_DFL)
        install_signal_faults()
        assert signal.getsignal(signal.SIGHUP) is not signal.SIG_DFL
    finally:
        signal.signal(signal.SIGTERM, old[0])
        signal.signal(signal.SIGHUP, old[1])
    # rule <-> patterns.json byte equality (CC-210 W9), when the rule exists
    if os.path.exists(RULE):
        assert rule_strings_match(P), "RULE_v3 patterns block != patterns.json"
    print("selftest ok")


def selftest_run(P, words):
    """Mocked end-to-end run() (CC-210a W9): fake transport, fake PDFs and extractor, temp OUT, sockets already blocked."""
    eng = ("The model is trained on the data and it is evaluated with a metric for this task, and we report what we "
           "find in the tables of this paper. ") * 20
    texts = {
        "nfd": unicodedata.normalize("NFD", "Tiếng Việt ") * 5 + eng + "We report CIDEr on KTVIC.\nReferences\n[1] x",
        "merged": eng + "BLEU on KTVIC is reported with VnCoreNLP and CIDEr-D.\nReferences\n[1] y",
        "vi": ("Chúng tôi huấn luyện mô hình trên tập KTVIC và đánh giá bằng BLEU cho mọi ảnh trong tập kiểm tra. " * 30)
              + "\nTài liệu tham khảo\n[1] z",
    }
    for i in range(12):
        texts["g%d" % i] = eng + ("Captions were word-segmented and scored with CIDEr-D on KTVIC." if i < 3 else "BLEU on KTVIC.") + "\nReferences\n[1] q"

    def work(wid, title, typ, pdf=None, doi=None):
        return {"id": "https://openalex.org/" + wid, "title": title, "type": typ, "publication_year": 2024, "doi": doi,
                "best_oa_location": {"pdf_url": pdf} if pdf else None}

    def make_transport(mode, state):
        def t(url):
            u = urllib.parse.unquote(url)
            state["calls"].append(url)
            if url.startswith("pdf://"):
                key = url[6:]
                if key == "forbidden":
                    raise urllib.error.HTTPError(url, 403, "forbidden", None, None)
                if key == "truncated":
                    raise http.client.IncompleteRead(b"%PDF-1.4 trunc")
                if mode == "s2fault" and key == "g5" and not state.get("s2fault_done"):
                    state["s2fault_done"] = True
                    raise ValueError("synthetic extraction-stage error")
                return ("%PDF-fake " + key).encode()
            if mode == "s1incomplete" and "/works/doi:" in u and not state.get("s1incomplete_done"):
                state["s1incomplete_done"] = True
                raise http.client.IncompleteRead(b'{"id": ')
            if mode == "s1shape" and "/paper/ARXIV:2401.08100" in u:
                return json.dumps({"paperId": "p1"}).encode()
            if mode == "s1shape" and "/paper/p1/citations" in u:
                return json.dumps({"data": [{"unexpected": {}}], "next": None}).encode()
            if "/works/doi:10.1007/978-3-030-63007-2_57" in u:
                return json.dumps(work("W100", "UIT-ViIC: A Dataset for the First Evaluation", "dataset", None, "https://doi.org/10.1007/978-3-030-63007-2_57")).encode()
            if "/works/doi:" in u or "/paper/" in u and "/search" not in u and "/citations" not in u:
                raise urllib.error.HTTPError(url, 404, "nf", None, None)
            if "/works?" in u:
                if "cursor=*" not in u:
                    return json.dumps({"results": [], "meta": {}}).encode()
                if mode == "s1fault" and "VieCap4H" in u and not state.get("s1fault_done"):
                    raise urllib.error.HTTPError(url, 429, "rate", None, None)
                if "KTVIC" in u and "title_and_abstract" in u:
                    if mode in ("full", "s2fault"):
                        res = [work("W%d" % (300 + i), "KTVIC paper %d" % i, "article", "pdf://g%d" % i) for i in range(12)]
                    else:
                        res = [work("W200", "Paper NFD", "article", "pdf://nfd"),
                               work("W201", "Merged title", "article", "pdf://merged", "https://doi.org/10.9/m"),
                               work("W202", "Merged title", "dataset", None, "https://doi.org/10.5281/zenodo.9"),
                               work("W203", "Nghien cuu chu thich anh", "article", "pdf://vi"),
                               work("W204", "KTVIC evaluation", "article", "pdf://forbidden"),
                               work("W205", "KTVIC truncated download", "article", "pdf://truncated")]
                    return json.dumps({"results": res, "meta": {"next_cursor": "c2"}}).encode()
                return json.dumps({"results": [], "meta": {"next_cursor": None}}).encode()
            if "/search/bulk" in u:
                return json.dumps({"data": [], "token": None}).encode()
            raise AssertionError(url)
        return t

    def extract(path):
        key = open(path, "rb").read().decode().split(" ", 1)[1]
        return texts[key], 1, 0

    def toolcheck_ok(P_, words_, out_):
        return {"pass": True, "mock": True}

    def quotes_stub(cells_out, P_, out_):
        with open(os.path.join(out_, "quotes.tsv"), "w") as f:
            f.write("mock\n")

    kw = dict(sleep=lambda x: None, toolcheck_fn=toolcheck_ok, sums_fn=lambda: None, quotes_fn=quotes_stub, extract=extract)
    A = lambda out, resume=False: argparse.Namespace(run=True, out=out, resume=resume)
    tmp = tempfile.mkdtemp()
    try:
        # 1. S1 FAULT (429 after retries) -> FAULT.json + search_log.json -> one resume from the cache -> NO-GO decide with k null
        o1, st = os.path.join(tmp, "o1"), {"calls": []}
        try:
            run(A(o1), P, words, transport=make_transport("s1fault", st), **kw)
            raise AssertionError("expected FAULT")
        except SystemExit as e:
            assert "FAULT at S1" in str(e)
        assert os.path.exists(os.path.join(o1, "FAULT.json")) and os.path.exists(os.path.join(o1, "search_log.json"))
        cached = {e["url"] for e in json.load(open(os.path.join(o1, "search_log.json")))["requests"]
                  if not e["cached"] and e["http"] in (200, 404)}  # 2xx replay from the cache, 404 from the log; the 429 is re-queried
        st2 = {"calls": [], "s1fault_done": True}
        d = run(A(o1, True), P, words, transport=make_transport("s1fault", st2), **kw)
        assert cached and not cached & set(st2["calls"]), "the resume must replay cached responses, not refetch them"
        assert d["verdict"] == "NO-GO" and d["primary"]["k"] is None and not d["template_licensed"]
        pop = json.load(open(os.path.join(o1, "population.json")))
        byreason = sorted((r["status"], r.get("reason")) for r in pop["rows"])
        assert ("acc", None) in byreason and byreason.count(("acc", None)) == 2, byreason   # NFD paper + merged article/dataset
        assert ("inr", "E5") in byreason and ("inr", "fetch_fail") in byreason and ("inr", "no_oa_pdf") in byreason, byreason
        assert pop["counts"]["E4"] == 0
        man = json.load(open(os.path.join(o1, "fulltext_manifest.json")))
        assert any(m.get("reason") == "fetch_fail" and m.get("http") == 403 for m in man)
        assert any(m.get("reason") == "fetch_fail" and m.get("http") == "IncompleteRead" for m in man)  # CC-210b W1
        assert byreason.count(("inr", "fetch_fail")) == 2, byreason
        slog = json.load(open(os.path.join(o1, "search_log.json")))
        assert len(slog["run_dates"]) == 2 and os.path.exists(os.path.join(o1, "candidates.sha256"))
        res = json.load(open(os.path.join(o1, "candidates.json")))["resolution"]
        assert sum(r["status"] == "unresolved" for r in res) == 4 and sum(r["status"] == "one_source" for r in res) == 1
        try:
            run(A(o1, True), P, words, transport=make_transport("s1fault", st2), **kw)
            raise AssertionError("second resume")
        except SystemExit as e:
            assert "already resumed" in str(e) or "needs FAULT" in str(e)
        # 2. S2 FAULT after the freeze -> resume rebuilds byte-identical candidates.json -> cells -> verdict; no resume after cells.json
        o2 = os.path.join(tmp, "o2")
        try:
            run(A(o2), P, words, transport=make_transport("s2fault", {"calls": []}), **kw)
            raise AssertionError("expected FAULT")
        except SystemExit as e:
            assert "FAULT at S2" in str(e)
        c_before = open(os.path.join(o2, "candidates.json"), "rb").read()
        logged404 = {e["url"] for e in json.load(open(os.path.join(o2, "search_log.json")))["requests"] if e.get("http") == 404}
        st_o2 = {"calls": [], "s2fault_done": True}
        d2 = run(A(o2, True), P, words, transport=make_transport("s2fault", st_o2), **kw)
        assert open(os.path.join(o2, "candidates.json"), "rb").read() == c_before
        assert logged404 and not logged404 & set(st_o2["calls"]), "logged 404s are replayed, not re-queried (CC-210b W3)"
        assert d2["primary"]["N_acc"] == 12 and d2["primary"]["k"] == 3 and d2["verdict"] == "PASS"
        assert d2["descriptive"]["C2"] == 3 and os.path.exists(os.path.join(o2, "cells.json"))
        write_json(o2, "FAULT.json", {"step": "synthetic"})
        os.remove(os.path.join(o2, "RESUMED"))
        try:
            run(A(o2, True), P, words, transport=make_transport("full", {"calls": []}), **kw)
            raise AssertionError("resume after cells.json")
        except SystemExit as e:
            assert "cells.json exists" in str(e)
        # 3. a tampered cache is a FAULT at resume, with no further resume
        o3 = os.path.join(tmp, "o3")
        try:
            run(A(o3), P, words, transport=make_transport("s1fault", {"calls": []}), **kw)
        except SystemExit:
            pass
        victim = os.path.join(o3, "cache", sorted(os.listdir(os.path.join(o3, "cache")))[0])
        open(victim, "ab").write(b" ")
        try:
            run(A(o3, True), P, words, transport=make_transport("s1fault", {"calls": [], "s1fault_done": True}), **kw)
            raise AssertionError("tampered cache")
        except SystemExit as e:
            assert "resume_cache_check" in str(e)
        assert json.load(open(os.path.join(o3, "FAULT.json")))["resumable"] is False
        # 5. S1 errors outside URLError (IncompleteRead, a changed response shape) still leave FAULT.json + search_log.json (CC-210b W1)
        for name, mode in (("o5", "s1incomplete"), ("o6", "s1shape")):
            o = os.path.join(tmp, name)
            try:
                run(A(o), P, words, transport=make_transport(mode, {"calls": []}), **kw)
                raise AssertionError("expected FAULT " + mode)
            except SystemExit as e:
                assert "FAULT at S1" in str(e), e
            f = json.load(open(os.path.join(o, "FAULT.json")))
            assert os.path.exists(os.path.join(o, "search_log.json")) and f["resumable"] and f["toolcheck_sha256"]
            assert ("IncompleteRead" if mode == "s1incomplete" else "KeyError") in f["error"], f
        d5 = run(A(os.path.join(tmp, "o5"), True), P, words, transport=make_transport("s1incomplete", {"calls": [], "s1incomplete_done": True}), **kw)
        assert d5["verdict"] == "NO-GO"
        # 6. caps hold over the start and the resume together: a cap FAULT re-hits the cap on resume (CC-210b W2)
        Pc = json.loads(json.dumps(P))
        Pc["caps"]["api_requests"] = 6
        o7 = os.path.join(tmp, "o7")
        try:
            run(A(o7), Pc, words, transport=make_transport("full", {"calls": []}), **kw)
            raise AssertionError("expected cap FAULT")
        except SystemExit as e:
            assert "FAULT at S1" in str(e) and "CapHit" in json.load(open(os.path.join(o7, "FAULT.json")))["error"]
        st7 = {"calls": []}
        try:
            run(A(o7, True), Pc, words, transport=make_transport("full", st7), **kw)
            raise AssertionError("expected cap FAULT on resume")
        except SystemExit as e:
            assert "FAULT at S1" in str(e)
        f7 = json.load(open(os.path.join(o7, "FAULT.json")))
        assert "CapHit" in f7["error"] and f7["resumable"] is False and st7["calls"] == []
        live = sum(1 for e in json.load(open(os.path.join(o7, "search_log.json")))["requests"] if not e["cached"] and e["kind"] == "api")
        assert live == 6, live
        # 7. CC-210c W1/W2/W3: SIGINT in S1, the wall cap, a missing cache file
        o8 = os.path.join(tmp, "o8")

        def kbi_once(url):
            if not kbi_state.get("done"):
                kbi_state["done"] = True
                raise KeyboardInterrupt
            return make_transport("s1fault", {"calls": [], "s1fault_done": True})(url)
        kbi_state = {}
        try:
            run(A(o8), P, words, transport=kbi_once, **kw)
            raise AssertionError("expected FAULT on SIGINT")
        except SystemExit as e:
            assert "FAULT at S1" in str(e)
        f8 = json.load(open(os.path.join(o8, "FAULT.json")))
        assert f8["resumable"] and "KeyboardInterrupt" in f8["error"] and os.path.exists(os.path.join(o8, "search_log.json"))
        assert run(A(o8, True), P, words, transport=kbi_once, **kw)["verdict"] == "NO-GO"
        o9, ticks = os.path.join(tmp, "o9"), iter([0] + [7 * 3600] * 10000)
        kw_clock = dict(kw, clock=lambda: next(ticks))
        try:
            run(A(o9), P, words, transport=make_transport("s1fault", {"calls": [], "s1fault_done": True}), **kw_clock)
            raise AssertionError("expected wall FAULT")
        except SystemExit as e:
            assert "FAULT at S1" in str(e)
        f9 = json.load(open(os.path.join(o9, "FAULT.json")))
        assert "wall" in f9["error"] and f9["resumable"]
        assert run(A(o9, True), P, words, transport=make_transport("s1fault", {"calls": [], "s1fault_done": True}), **kw)["verdict"] == "NO-GO"
        # S2 wall: the clock passes the wall cap after 2 PDF fetches -> FAULT at S2, not pdf_cap (CC-210d W1)
        o11, st11 = os.path.join(tmp, "o11"), {"calls": []}
        clock11 = lambda: 7 * 3600 if sum(u.startswith("pdf://") for u in st11["calls"]) >= 2 else 0
        try:
            run(A(o11), P, words, transport=make_transport("full", st11), **dict(kw, clock=clock11))
            raise AssertionError("expected wall FAULT at S2")
        except SystemExit as e:
            assert "FAULT at S2" in str(e), e
        f11 = json.load(open(os.path.join(o11, "FAULT.json")))
        assert f11["step"] == "S2" and "wall" in f11["error"] and f11["resumable"]
        assert not os.path.exists(os.path.join(o11, "population.json")) and not os.path.exists(os.path.join(o11, "cells.json"))
        d11 = run(A(o11, True), P, words, transport=make_transport("full", {"calls": []}), **kw)
        assert json.load(open(os.path.join(o11, "population.json")))["counts"]["pdf_cap"] == 0
        assert d11["verdict"] == "PASS" and d11["primary"]["k"] == 3 and d11["primary"]["N_acc"] == 12
        o10 = os.path.join(tmp, "o10")
        try:
            run(A(o10), P, words, transport=make_transport("s1fault", {"calls": []}), **kw)
        except SystemExit:
            pass
        os.remove(os.path.join(o10, "cache", sorted(os.listdir(os.path.join(o10, "cache")))[0]))
        st10 = {"calls": [], "s1fault_done": True}
        try:
            run(A(o10, True), P, words, transport=make_transport("s1fault", st10), **kw)
            raise AssertionError("missing cache file")
        except SystemExit as e:
            assert "resume_cache_check" in str(e)
        assert json.load(open(os.path.join(o10, "FAULT.json")))["resumable"] is False and st10["calls"] == []
        # 8. outermost guard: every stage function raising in turn leaves FAULT.json + search_log.json (CC-210c, coordinator)
        covered = selftest_guard(P, words, tmp, A, kw, make_transport)
        assert covered == ["sums", "rule_strings", "toolcheck", "S1", "S2:merge_records", "S2:classify", "S3", "decide", "quotes",
                           "resume_cache_check"], covered
        print("guard stages covered:", ", ".join(covered))
        # 4. a fresh run refuses an existing OUT
        try:
            run(A(o1), P, words, transport=make_transport("full", {"calls": []}), **kw)
            raise AssertionError("existing OUT")
        except SystemExit as e:
            assert "--out exists" in str(e)
    finally:
        shutil.rmtree(tmp)


def selftest_guard(P, words, tmp, A, kw, make_transport):
    """Patch each stage of run() in turn to raise; guarded_run must leave FAULT.json + search_log.json, and the one resume
    must complete, or be refused only by a documented final rule (cells.json exists; already resumed)."""
    g = globals()
    def boom(exc):
        def f(*a, **k):
            raise exc
        return f
    plan = [("sums", "kw", "sums_fn", "sums", "complete"),
            ("rule_strings", "glob", "rule_strings_match", "rule_strings", "complete"),
            ("toolcheck", "kw", "toolcheck_fn", "toolcheck", "complete"),
            ("S1", "glob", "s1_search", "S1", "complete"),
            ("S2:merge_records", "glob", "merge_records", "S2", "complete"),
            ("S2:classify", "glob", "classify", "S2", "complete"),
            ("S3", "glob", "cells", "S3", "complete"),
            ("decide", "glob", "decide", "decide", "refused: cells.json exists"),
            ("quotes", "kw", "quotes_fn", "quotes", "refused: cells.json exists")]
    covered = []
    for i, (label, how, name, step, resume_expect) in enumerate(plan):
        o = os.path.join(tmp, "g%d" % i)
        exc = KeyboardInterrupt("synthetic") if i % 2 else RuntimeError("synthetic")
        kwi, saved = dict(kw), None
        if how == "kw":
            kwi[name] = boom(exc)
        else:
            saved = g[name]
            g[name] = boom(exc)
        try:
            guarded_run(A(o), P, words, transport=make_transport("full", {"calls": []}), **kwi)
            raise AssertionError("no FAULT for " + label)
        except SystemExit as e:
            assert "FAULT" in str(e), (label, e)
        finally:
            if saved is not None:
                g[name] = saved
        f = json.load(open(os.path.join(o, "FAULT.json")))
        assert f["step"] == step and os.path.exists(os.path.join(o, "search_log.json")), (label, f)
        assert f["resumable"] == (resume_expect == "complete"), (label, f)  # false once cells.json exists
        try:
            d = guarded_run(A(o, True), P, words, transport=make_transport("full", {"calls": []}), **kw)
            assert resume_expect == "complete" and d["verdict"] == "PASS", (label, d)
        except SystemExit as e:
            assert resume_expect != "complete" and resume_expect.split(": ")[1] in str(e), (label, e)
        covered.append(label)
    # resume-only stage: verify_cache raising during the one resume -> FAULT, not resumable (one resume in total)
    o = os.path.join(tmp, "g_resume")
    try:
        guarded_run(A(o), P, words, transport=make_transport("s1fault", {"calls": []}), **kw)
    except SystemExit:
        pass
    saved, g["verify_cache"] = g["verify_cache"], boom(RuntimeError("synthetic"))
    try:
        guarded_run(A(o, True), P, words, transport=make_transport("s1fault", {"calls": [], "s1fault_done": True}), **kw)
        raise AssertionError("no FAULT for resume_cache_check")
    except SystemExit as e:
        assert "FAULT" in str(e)
    finally:
        g["verify_cache"] = saved
    f = json.load(open(os.path.join(o, "FAULT.json")))
    assert f["step"] == "resume_cache_check" and f["resumable"] is False and os.path.exists(os.path.join(o, "search_log.json"))
    covered.append("resume_cache_check")
    return covered


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("cmd", nargs="?", choices=["toolcheck", "run"])
    ap.add_argument("--out")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--resume", action="store_true", help="the one resume of a FAULTed OUT (RULE §1.1, §4)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    P, words = load_patterns(), load_words()
    if a.cmd == "toolcheck":
        os.makedirs(a.out, exist_ok=False)
        r = toolcheck(P, words, a.out)
        r["versions"] = tool_versions()
        print(json.dumps(r, indent=1))
    elif a.cmd == "run":
        install_signal_faults()
        guarded_run(a, P, words)
    else:
        ap.error("give --selftest, toolcheck or run")


if __name__ == "__main__":
    main()
