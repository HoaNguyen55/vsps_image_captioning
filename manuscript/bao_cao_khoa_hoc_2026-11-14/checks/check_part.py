#!/usr/bin/env python3
"""Check one report part against its sources.

1. Every decimal, every percentage and every integer >= 100 in the part must appear, as written, in the source files.
2. Every pandoc citation key ([@key]) must exist in the given .bib files.
3. Strings that must never appear (addresses, internal ruling ids) are listed for review.

    python3 -I check_part.py PART.md --src FILE [FILE...] --bib FILE [FILE...] [--allow ALLOW.tsv]

ALLOW.tsv: token<TAB>reason  (one line per number that is correct but not printed in a source, e.g. a count of
items in this report itself). Exit 0 only when nothing is unmatched and no key is missing.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NUM = re.compile(r"(?<![\w.,/\-])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+|\d+)(?![\w/]|[.,]\d)")
STRIP = [
    re.compile(r"```.*?```", re.S),                      # fenced code
    re.compile(r"`[^`\n]*`"),                            # code spans: paths, file::key, shas
    re.compile(r"<!--.*?-->", re.S),                     # comments
    re.compile(r"\[(?:[^\[\]]*@)[^\[\]]*\]"),            # citations
    re.compile(r"(?<=\])\([^)\s]+\)"),                   # link and image targets
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}(?:/\d{4})?\b|\b\d{1,2}:\d{2}\b"),  # dates, times
    re.compile(r"\b(?:CC|OPS|PI|CP|INC|PD)-[\w.]+"),      # internal ids
    re.compile(r"(?:§+|\b(?:[Mm]ục|[Pp]hần|[Bb]ảng|[Hh]ình|[Pp]hụ lục|Sections?|Tables?|Figures?|Fig\.|Appendix|Eq\.|Supplement(?:ary)?(?: Section| Table)?)\s+)[A-Z]?\.?\d+(?:\.\d+)*[a-z]?(?:\s*(?:[-–,]|và|and)\s*[A-Z]?\.?\d+(?:\.\d+)*[a-z]?)*"),
    re.compile(r"\((?:[A-Z]\.)?\d+(?:\.\d+)*[a-z]?\)"),   # equation and item labels such as (A.3) or (2)
]
FORBIDDEN = [("address", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")), ("tunnel", re.compile(r"trycloudflare|\bssh\s")),
             ("internal ruling id", re.compile(r"\bCC-\d+"))]


def norm(text: str) -> str:
    return text.replace("−", "-").replace("{,}", ",").replace("\\,", "").replace(" ", "").replace(" ", "")


def tokens(part: str) -> list[tuple[str, int, str]]:
    out = []
    for ln, line in enumerate(part.split("\n"), 1):
        if re.match(r"\s*#{1,6}\s", line):                # heading numbers
            line = re.sub(r"^(\s*#{1,6}\s+)(?:[A-Z]\.)?\d+(?:\.\d+)*\.?", r"\1", line)
        for m in NUM.finditer(line):
            tok = m.group(1)
            pct = line[m.end():m.end() + 1] == "%" or line[m.end():m.end() + 2] == "\\%"
            is_dec = "." in tok
            val = float(tok.replace(",", ""))
            if not is_dec and not pct and (val < 100 or 1900 <= val <= 2099):
                continue
            out.append((tok, ln, line.strip()[:110]))
    return out


def present(tok: str, corpus: str) -> bool:
    forms = {tok, tok.replace(",", "")}
    if "," not in tok and "." not in tok and len(tok) > 3:
        forms.add(f"{int(tok):,}")
    return any(re.search(r"(?<![\d.])(?<!\d,)" + re.escape(f) + r"(?!\d|\.\d)", corpus) for f in forms)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("part")
    ap.add_argument("--src", nargs="+", required=True)
    ap.add_argument("--bib", nargs="*", default=[])
    ap.add_argument("--allow")
    a = ap.parse_args()
    raw = Path(a.part).read_text(encoding="utf-8")
    corpus = norm("\n".join(Path(p).read_text(encoding="utf-8", errors="replace") for p in a.src))
    allow = {}
    if a.allow and Path(a.allow).exists():
        for line in Path(a.allow).read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                t, _, why = line.partition("\t")
                allow[t.strip()] = why.strip()
    keys_used = set(re.findall(r"@([A-Za-z][\w:.\-]*[\w])", " ".join(re.findall(r"\[[^\[\]]*@[^\[\]]*\]", raw))))
    bibkeys = set()
    for b in a.bib:
        bibkeys |= set(re.findall(r"^@\w+\{\s*([^,\s]+)", Path(b).read_text(encoding="utf-8", errors="replace"), re.M))
    missing = sorted(keys_used - bibkeys) if a.bib else []
    part = norm(raw)
    for rx in STRIP:
        part = rx.sub(lambda m: "\n" * m.group(0).count("\n") + " ", part)
    toks = tokens(part)
    bad = [(t, ln, ctx) for t, ln, ctx in toks if not present(t, corpus) and t not in allow]
    n_allowed = sum(1 for t, _, _ in toks if t in allow and not present(t, corpus))
    print(f"part: {a.part}")
    print(f"words: {len(raw.split())}  numbers checked: {len(toks)}  matched: {len(toks) - len(bad) - n_allowed}  allowed by list: {n_allowed}  UNMATCHED: {len(bad)}")
    for t, ln, ctx in bad:
        print(f"  UNMATCHED {t}\tline {ln}\t{ctx}")
    print(f"citation keys used: {len(keys_used)}  MISSING from bib: {len(missing)}")
    for k in missing:
        print(f"  MISSING KEY {k}")
    for name, rx in FORBIDDEN:
        hits = [(i, l.strip()[:100]) for i, l in enumerate(raw.split("\n"), 1) if rx.search(l)]
        print(f"review [{name}]: {len(hits)}")
        for i, l in hits[:20]:
            print(f"  line {i}\t{l}")
    return 1 if bad or missing else 0


def demo() -> None:
    c = norm("slope 0.412 on 1,755 items; 37.5% pass; n = 600")
    assert present("0.412", c) and present("1755", c) and present("37.5", c) and present("600", c)
    assert not present("0.41", c) and not present("0.4120", c) and not present("755", c)
    t = [x[0] for x in tokens("Bảng A.3 gives 0.412 and 12 items, 600 images in 2026, 37.5%, 5%.")]
    assert t == ["0.412", "600", "37.5", "5"], t


if __name__ == "__main__":
    demo()
    sys.exit(main())
