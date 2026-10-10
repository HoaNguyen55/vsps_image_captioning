"""Monthly literature watch for VSPS: prints arXiv/OpenAlex papers not seen in earlier runs.

    python3 .paper_work/research_wall/watch.py            # query, append new items to watch_log.md
    python3 .paper_work/research_wall/watch.py --self-check
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
SEEN = HERE / "watch_seen.json"
LOG = HERE / "watch_log.md"

ARXIV = {
    "hallucination decoding": 'abs:hallucination AND (abs:decoding OR abs:steering) AND abs:vision AND abs:language',
    "detailed caption eval": 'abs:detailed AND abs:caption AND (abs:evaluation OR abs:benchmark OR abs:metric)',
    "caption RL": "abs:caption* AND (abs:GRPO OR abs:verifiable)",
    "recaption data": "abs:recaption* AND abs:hallucination",
    "verifier yes-bias": 'abs:yes AND abs:bias AND abs:vision AND abs:language',
    "vietnamese multimodal": "abs:Vietnamese AND (abs:multimodal OR abs:vision OR abs:caption*)",
    "multilingual hallucination": "abs:multilingual AND abs:hallucination AND abs:vision",
    "scene graph hallucination": 'abs:scene AND abs:graph AND abs:hallucination AND abs:vision',
}
OPENALEX = {
    "journal: caption hallucination": "caption hallucination vision-language",
    "journal: vietnamese captioning": "Vietnamese image captioning",
    "journal: knowledge graph captioning": "knowledge graph image captioning hallucination",
}


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "vsps-watch"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def parse_arxiv(xml: bytes) -> list[dict]:
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in ET.fromstring(xml).findall("a:entry", ns):
        out.append({"id": e.findtext("a:id", "", ns).strip(),
                    "title": " ".join(e.findtext("a:title", "", ns).split()),
                    "date": e.findtext("a:published", "", ns)[:10]})
    return out


def arxiv(query: str, n: int = 25) -> list[dict]:
    q = urllib.parse.urlencode({"search_query": query, "sortBy": "submittedDate", "sortOrder": "descending",
                                "max_results": n})
    return parse_arxiv(_get("http://export.arxiv.org/api/query?" + q))


def openalex(search: str, since: str, n: int = 25) -> list[dict]:
    q = urllib.parse.urlencode({"search": search, "filter": f"from_publication_date:{since},type:article",
                                "sort": "publication_date:desc", "per-page": n})
    res = json.loads(_get("https://api.openalex.org/works?" + q))["results"]
    return [{"id": w.get("doi") or w["id"], "title": w.get("display_name") or "",
             "date": w.get("publication_date") or "",
             "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""}
            for w in res]


def new_items(found: dict[str, list[dict]], seen: set[str]) -> dict[str, list[dict]]:
    out = {}
    for topic, items in found.items():
        fresh = [it for it in items if it["id"] not in seen]
        seen.update(it["id"] for it in fresh)
        if fresh:
            out[topic] = fresh
    return out


def main() -> None:
    seen = set(json.loads(SEEN.read_text())) if SEEN.exists() else set()
    first_run = not seen
    found, failed = {}, []
    for topic, q in ARXIV.items():
        try:
            found[topic] = arxiv(q)
        except OSError as e:
            failed.append(f"arXiv '{topic}': {e}")
        time.sleep(3)  # arXiv API asks for >=3 s between calls
    since = f"{date.today().year - 1}-01-01"
    for topic, q in OPENALEX.items():
        try:
            found[topic] = openalex(q, since)
        except OSError as e:
            failed.append(f"OpenAlex '{topic}': {e}")
        time.sleep(2)
    fresh = new_items(found, seen)
    SEEN.write_text(json.dumps(sorted(seen), ensure_ascii=False, indent=0))
    lines = [f"\n## {date.today()}" + (" (lần đầu: toàn bộ là mốc nền)" if first_run else "")]
    for topic, items in fresh.items():
        lines.append(f"\n### {topic} ({len(items)} mới)")
        lines += [f"- {it['date']} · {it['title']}" + (f" · *{it['venue']}*" if it.get("venue") else "")
                  + f" · {it['id']}" for it in items]
    lines += [f"- LỖI (chạy lại sau): {f}" for f in failed]
    with LOG.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\n{sum(map(len, fresh.values()))} bài mới → {LOG}")
    if failed:
        sys.exit(f"{len(failed)} truy vấn lỗi; các chủ đề đó chưa được cập nhật")


def self_check() -> None:
    xml = (b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>http://arxiv.org/abs/1</id>'
           b'<title>A\n  B</title><published>2026-10-01T00:00:00Z</published></entry></feed>')
    items = parse_arxiv(xml)
    assert items == [{"id": "http://arxiv.org/abs/1", "title": "A B", "date": "2026-10-01"}]
    seen = {"x"}
    fresh = new_items({"t": items + [{"id": "x", "title": "", "date": ""}], "u": []}, seen)
    assert list(fresh) == ["t"] and len(fresh["t"]) == 1 and "http://arxiv.org/abs/1" in seen
    assert new_items({"t": items}, seen) == {}
    print("self-check OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-check", action="store_true")
    self_check() if ap.parse_args().self_check else main()
