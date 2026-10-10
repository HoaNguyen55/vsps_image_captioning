#!/usr/bin/env python
"""Clean the SFT supervision store and report what each filter caught.

    python scripts/clean_supervision.py --out <dir> [--suffix _v2]  # sft_clean<suffix>.jsonl + clean_report<suffix>.json
    python scripts/clean_supervision.py --selftest

Policy: repair in place when a deterministic repair exists, drop only when nothing
valid remains; never invent content. Filters (patterns found empirically on
data/supervision/sft.jsonl):

  token repairs (text rewritten)
    gender      person_uncap.neutralise (same neutralisation the method applies to
                gendered propositions); "anh ta"/"cô ta" -> pronoun then neutralised
    truncation  "biển quảng" -> "biển quảng cáo", "(số|cái|...) sản" -> "sản phẩm",
                "một cái số X" -> "một số X": a syllable that is meaningless alone
                has exactly one completion, so no content is added
    repeat_adj  an immediately repeated word span collapses ("một nhóm người một
                nhóm người" -> "một nhóm người")
  clause repairs (a caption is sentences -> clauses -> comma pieces; a clause opens
  a sentence or starts with a template connective "bên cạnh đó (có)", "còn (có)",
  "ngoài ra (còn) (có)", "cùng với đó (có)"; its first piece is the head, later
  pieces are attributes of it). Removing a piece removes text only, so it cannot
  turn a guess into a claim; removing a head removes its whole clause.
    repeat_clause  a clause subsumed by an earlier kept clause (after stripping
                quantifiers/classifiers/"đang"/"có"/"trong ảnh": contiguous
                containment, or token set subset with >=2 tokens); a piece repeating
                an earlier piece of the same clause
    repeat_span a >=NGRAM_N-word "(trong ảnh) đang ..." suffix already said earlier
                in the same clause is cut
    hedge       piece containing "có vẻ", "có thể", "hoặc"...
    garbled:*   vague/ambiguous heads ("cái hệ thống", bare "cái đồ", "bảng thông"),
                headless colour ("người màu đỏ"), dangling function word ("và một
                số"), dangling "của" + verb, gendered role noun ("cô dâu"), residual
                gendered word
    dangling_connective  connective whose clause body is empty ("Bên cạnh đó có .");
                a connective left opening the caption becomes "Có" or is dropped
  drops
    cjk / out_of_script  stripping leaves broken clauses; translating would invent
    <filter>    every clause was removed by that filter
    duplicate   identical (image_id, prompt, response) after cleaning
  Legitimate template repeats across distinct objects ("kích thước đa dạng, từ nhỏ
  đến lớn" for two objects) are kept and counted as repeat_ngram_residual.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from person_uncap import _GENDER_RE, neutralise  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NGRAM_N = 5  # 3-/4-grams repeat legitimately in template enumerations ("màu xanh dương", "một số người mặc áo")

CJK_RE = re.compile(r"[⺀-〿぀-ヿ㐀-鿿가-힯豈-﫿＀-￯]")
# Latin + Latin Ext. Additional (Vietnamese) + combining marks + general punctuation.
OUT_OF_SCRIPT_RE = re.compile(r"[^\u0000-ɏ̀-ͯḀ-ỿ -⁯]")
HEDGE_RE = re.compile(
    r"\b(có vẻ|vẻ như|dường như|hình như|có lẽ|có thể(?!\s+(?:nhìn\s+)?thấy)|chắc là|không rõ|gì đó|hoặc)\b", re.I
)
GARBLED = {
    "vague_head": re.compile(r"\bcái (hệ thống|đồ)\b(?!\s+(?!này)\w)", re.I),
    "ambiguous_truncation": re.compile(r"\bbảng thông\b(?!\s+(báo|tin))", re.I),
    "headless_colour": re.compile(r"\b(người màu|màu người)\b", re.I),
    "dangling_function_word": re.compile(
        r"\b(và|của|với|các|những|một số|một|đang|là|hoặc|bao gồm)\s*([.,;:]|$)", re.I
    ),
    "dangling_cua": re.compile(r"\bcủa\s+(đang|nâng|cầm|là|đi|đứng|ngồi)\b", re.I),
    "cai_so_other": re.compile(r"\bcái số\b", re.I),
    "gender_role_noun": re.compile(r"\bngười (dâu|giáo|gái|trai)\b", re.I),
}
TRUNCATIONS = (
    (re.compile(r"\bbiển quảng\b(?!\s+cáo)", re.I), "biển quảng cáo"),
    (re.compile(r"\b(số|cái|các|nhiều|những|loại) sản\b(?!\s+phẩm)", re.I), r"\1 sản phẩm"),
    (re.compile(r"\bmột cái số\b", re.I), "một số"),
)
REPAIRS = ("gender", "truncation", "repeat_adj", "headless_colour_span")
# a lone repeated syllable may be two overlapping compounds ("xanh lá lá chuối"), so only
# "người người" (a neutralisation artifact) collapses at length 1
ADJ_REPEAT_RE = re.compile(r"\b(người|\w+(?:\s+\w+)+?)(?:\s+\1\b)+", re.I)
COLOUR = r"(?:xanh (?:dương|lá(?: cây)?|lam|ngọc|nước biển|da trời)|xanh|đỏ|vàng|trắng|đen|nâu|hồng|cam|tím|xám|kem|be|bạc|ghi)"
_COLOUR_ITEM = COLOUR + r"(?: \([^()]*\))?"
# only before punctuation or a word that cannot fuse with "người" into a new noun
# ("người màu trắng lớn" must not become "người lớn" = adults)
_COLOUR_FOLLOW = (r"(?=\s*(?:[.,;:]|$)|\s+(?:áo|váy|quần|đầm|đồng phục|quân phục|bộ|trang phục|mũ|nón|khăn|"
                  r"với|trong|đang|đứng|đi|ngồi|mặc|đội|đeo|cầm)\b)")
HEADLESS_COLOUR_SPAN_RE = re.compile(
    rf"\b(người) màu {_COLOUR_ITEM}(?:(?:,| và) {_COLOUR_ITEM})*{_COLOUR_FOLLOW}", re.I)
GENDER_PROTECT = re.compile(r"\bông già noel\b", re.I)  # a character name, not a gendered person
GENDER_TOKEN = ""


def mode(row: dict) -> str:
    return "short" if row.get("variant") == "short" else "detailed"


def _tidy(s: str) -> str:
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    s = re.sub(r"([,.;:])(?:\s*[,;:])+", r"\1", s)
    s = re.sub(r"\s{2,}", " ", s).strip()
    return re.sub(r"(^|[.!?]\s+)(\w)", lambda m: m.group(1) + m.group(2).upper(), s)


def repair_gender(s: str) -> str:
    s = GENDER_PROTECT.sub(GENDER_TOKEN, s)
    s = re.sub(r"\bbé (gái|trai)\b", "bé", s, flags=re.I)
    s = re.sub(r"\b(anh|cô|chị|ông|bà)\s+ta\b", r"\1", s, flags=re.I)
    # neutralise() deletes "cô ấy"; at a sentence start that would orphan the predicate
    s = re.sub(r"(^|[.!?]\s+)(cô|anh|chị|ông|bà|em|họ)\s+ấy\b", r"\1người này", s, flags=re.I)
    # neutralise() is lowercase-only; lower sentence-initial letters, _tidy restores them
    s = re.sub(r"(^|[.!?]\s+)(\w)", lambda m: m.group(1) + m.group(2).lower(), s)
    s = neutralise(s)
    return re.sub(r"\bngười này người\b", "người này", s).replace(GENDER_TOKEN, "ông già Noel")


def collapse_repeats(s: str) -> str:
    prev = None
    while prev != s:
        prev, s = s, ADJ_REPEAT_RE.sub(r"\1", s)
    return s


def repeated_ngram(s: str, n: int = NGRAM_N) -> str | None:
    t = re.findall(r"\w+", s.lower())
    seen = set()
    for i in range(len(t) - n + 1):
        g = " ".join(t[i:i + n])
        if g in seen:
            return g
        seen.add(g)
    return None


ANAPHORA = {"này", "khác", "kia"}
CONNECTIVE_RE = re.compile(
    r"^(bên cạnh đó(?: có)?|cùng với đó(?: có)?|ngoài ra(?: còn)?(?: có)?|còn có|còn(?! lại))(?:\s+|$)", re.I
)
# dropped before comparing clauses: quantifiers, classifiers, copula/aspect, "trong ảnh"
# counts ("vài", "nhiều", "số") are kept: "một vài chiếc xe máy" is not "một chiếc xe máy"
COMPARE_STOP = {"một", "các", "những", "mỗi", "cái", "chiếc", "con", "có", "đang", "là", "này"}


def _norm(s: str) -> list[str]:
    s = re.sub(r"\btrong ảnh\b", " ", s.lower())
    return collapse_repeats(" ".join(t for t in re.findall(r"\w+", s) if t not in COMPARE_STOP)).split()


def _subsumed(c: list[str], earlier: list[list[str]]) -> bool:
    """Contiguous containment only: a token-set subset can be a different object ("túi màu trắng"
    vs "túi màu đen")."""
    j = f" {' '.join(c)} "
    return any(j in f" {' '.join(e)} " for e in earlier)


def _piece_flags(p: str) -> list[str]:
    hits = ["hedge"] if HEDGE_RE.search(p) else []
    hits += [f"garbled:{k}" for k, rx in GARBLED.items() if rx.search(p)]
    if _GENDER_RE.search(GENDER_PROTECT.sub(" ", re.sub(r'"[^"]*"', " ", p)).lower()):  # quoted sign text is a proper noun
        hits.append("garbled:gender_residual")
    return hits


def _trim_repeated_suffix(p: str, prior: str, n: int) -> str:
    """Cut a >=n-word "(trong ảnh) đang ..." suffix already said earlier in the clause."""
    w = p.split()
    low = [x.lower() for x in w]
    for i in range(len(w) - n + 1):
        before = f" {prior} {' '.join(low[:i])} "
        if low[i] == "đang" and any(f" {' '.join(low[j:])} " in before for j in (i, i + 1)):
            cut = i - 2 if low[max(i - 2, 0):i] == ["trong", "ảnh"] else i
            if cut > 0:
                return re.sub(r"(\s+(cũng|và|đều|thì|mà))+$", "", " ".join(w[:cut]), flags=re.I)
    return p


def _parse(s: str) -> list[tuple[list[dict], str]]:
    sents = []
    for sent in re.split(r"(?<=[.!?])\s+", s):
        body, end = re.match(r"(.*?)([.!?]*)$", sent.strip(), re.S).groups()
        clauses: list[dict] = []
        pending = ""  # "Ngoài ra, còn có X": a bare connective piece joins the next one
        parts = [x.strip() for x in body.split(",") if x.strip()]
        for k, p in enumerate(parts):
            m = CONNECTIVE_RE.match(p)
            if m and m.end() == len(p) and k + 1 < len(parts):
                pending += m.group(1) + ", "
                continue
            if pending:
                m2 = m.group(1) if m else ""
                clauses.append({"conn": (pending + m2).rstrip(", "), "pieces": [p[m.end():] if m else p]})
                pending = ""
            elif m or not clauses:
                clauses.append({"conn": m.group(1) if m else "", "pieces": [p[m.end():] if m else p]})
            else:
                clauses[-1]["pieces"].append(p)
        sents.append((clauses, end or "."))
    return sents


def repair_clauses(s: str, n: int = NGRAM_N) -> tuple[str, list[str]]:
    """Remove repeated / hedged / garbled clauses and pieces; return (text, reasons).

    Repeat removal runs only when the caption has a repeated n-word span, so a caption
    without one is never shortened for being redundant."""
    dedup = repeated_ngram(s, n) is not None
    reasons: list[str] = []
    kept_norms: list[list[str]] = []
    out_sents = []
    parsed = _parse(s)
    first_clause = parsed[0][0][0] if parsed and parsed[0][0] else None
    for clauses, end in parsed:
        out_clauses = []
        for c in clauses:
            pieces, prior = [], ""
            for k, p in enumerate(c["pieces"]):
                t = _trim_repeated_suffix(p, prior, n) if dedup else p
                if t != p:
                    reasons.append("repeat_span")
                flags = _piece_flags(t)
                # short attribute pieces ("kích thước lớn") legitimately recur for a new object
                if not flags and dedup and k and len(_norm(t)) >= 4 \
                        and _subsumed(_norm(t), [_norm(q) for q in pieces]):
                    flags = ["repeat_clause"]
                if flags:
                    reasons += flags
                    if k == 0:  # head gone -> its attributes have no subject
                        pieces = []
                        break
                    continue
                pieces.append(t)
                prior += " " + t.lower()
            if not pieces:
                continue
            norm = _norm(" ".join(pieces))
            if not norm:  # "Bên cạnh đó có ." or a lone "Trong ảnh" whose content was removed
                reasons.append("dangling_connective")
                continue
            if dedup and _subsumed(norm, kept_norms):
                reasons.append("repeat_clause")
                continue
            kept_norms.append(norm)
            c["pieces"] = pieces
            out_clauses.append(c)
        if out_clauses:
            out_sents.append((out_clauses, end))
    first_removed = not (out_sents and out_sents[0][0][0] is first_clause)
    while first_removed and out_sents:  # "Người này ..." whose antecedent was removed
        head = out_sents[0][0][0]["pieces"]
        w = head[0].split()
        i = next((i for i, x in enumerate(w[:5]) if x.lower().strip(".,") in ANAPHORA), None)
        if i is None:
            break
        reasons.append("orphan_anaphor")
        if i:
            head[0] = " ".join(w[:i] + w[i + 1:])
            break
        out_sents[0][0].pop(0)  # sentence opens with the anaphor itself: no subject left
        if not out_sents[0][0]:
            out_sents.pop(0)
    if out_sents and out_sents[0][0][0]["conn"]:  # a connective cannot open the caption
        first = out_sents[0][0][0]
        first["conn"] = "có" if first["conn"].lower().endswith("có") else ""
    text = " ".join(
        ", ".join(((c["conn"] + " ") if c["conn"] else "") + ", ".join(c["pieces"]) for c in cl) + end
        for cl, end in out_sents
    )
    return _tidy(text), reasons


def clean(text: str, n: int = NGRAM_N) -> tuple[str | None, list[str], list[str]]:
    """Return (cleaned text or None if dropped, repair hits, drop hits)."""
    s = unicodedata.normalize("NFC", text)
    if CJK_RE.search(s):
        return None, [], ["cjk"]
    if OUT_OF_SCRIPT_RE.search(s):
        return None, [], ["out_of_script"]
    repairs = []
    for rx, rep in TRUNCATIONS:
        new = rx.sub(rep, s)
        if new != s:
            repairs.append("truncation")
            s = new
    new = HEADLESS_COLOUR_SPAN_RE.sub(r"\1", s)  # "người màu đỏ áo phông" -> "người áo phông"
    if new != s:
        repairs.append("headless_colour_span")
        s = new
    new = repair_gender(s)
    if _tidy(new) != _tidy(s):
        repairs.append("gender")
    s = new
    new = collapse_repeats(s)
    if new != s:
        repairs.append("repeat_adj")
    s, reasons = repair_clauses(_tidy(new), n)
    if not s:
        return None, sorted(set(repairs)), sorted(set(reasons)) or ["empty"]
    return s, sorted(set(repairs + reasons)), []


def run(src: Path, out_dir: Path, n: int, suffix: str = "") -> dict:
    rows = [json.loads(line) for line in src.open(encoding="utf-8") if line.strip()]
    hits: dict[str, dict[str, Counter]] = defaultdict(lambda: {"repaired": Counter(), "dropped": Counter()})
    dropped_first: Counter = Counter()
    by_mode_in, by_mode_out = Counter(), Counter()
    examples: dict[str, list] = defaultdict(list)
    kept, seen = [], set()
    for row in rows:
        m = mode(row)
        by_mode_in[m] += 1
        new, repairs, drops = clean(row["response"], n)
        if new is not None:
            key = (row["image_id"], row["prompt"], new)
            if key in seen:
                drops, new = ["duplicate"], None
            seen.add(key)
        outcome = "dropped" if new is None else "repaired"
        for h in set(repairs + drops):
            hits[h][outcome][m] += 1
        if new is not None and repeated_ngram(new, n):
            hits["repeat_ngram_residual"]["repaired"][m] += 1  # kept as is: same template attribute on distinct objects
        for h in sorted(set(repairs + drops) - set(REPAIRS)) or repairs[:1]:  # one example slot per clause filter
            if len(examples[h]) < 4:
                examples[h].append({"image_id": row["image_id"], "mode": m, "hits": repairs + drops,
                                    "before": row["response"], "after": new})
                break
        if new is None:
            dropped_first[drops[0]] += 1
            continue
        by_mode_out[m] += 1
        kept.append({**row, "response": new})

    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"sft_clean{suffix}.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for row in kept:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    had = defaultdict(set)
    for row in rows:
        had[mode(row)].add(row["image_id"])
    has = defaultdict(set)
    for row in kept:
        has[mode(row)].add(row["image_id"])
    all_in = had["short"] | had["detailed"]
    all_out = has["short"] | has["detailed"]
    picked = []  # round-robin across filters -> 20 diverse before/after pairs
    while len(picked) < 20 and any(examples.values()):
        for k in sorted(examples, key=lambda k: (k in REPAIRS, k)):
            if examples[k] and len(picked) < 20:
                picked.append(examples[k].pop(0))
    resp_counts = Counter(r["response"] for r in kept)
    report = {
        "input": str(src), "output": str(out), "ngram_n": n,
        "n_in": len(rows), "n_out": len(kept),
        "by_mode": {m: {"in": by_mode_in[m], "out": by_mode_out[m]} for m in ("short", "detailed")},
        "filter_hits": {k: {o: {"short": v[o]["short"], "detailed": v[o]["detailed"]} for o in ("repaired", "dropped")}
                        for k, v in sorted(hits.items())},
        "dropped_by_first_reason": dict(dropped_first.most_common()),
        "images_losing_detailed": len(had["detailed"] - has["detailed"]),
        "images_losing_short": len(had["short"] - has["short"]),
        "images_losing_all": len(all_in - all_out),
        "cross_image_identical_responses_kept": sum(v - 1 for v in resp_counts.values() if v > 1),
        "examples": picked,
    }
    (out_dir / f"clean_report{suffix}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                                        encoding="utf-8")
    return report


def selftest() -> None:
    assert clean("Có một cái thìa羹, còn có một cái tô phở.")[0] is None
    assert clean("Một cái biển quảng lớn.")[0] == "Một cái biển quảng cáo lớn."
    assert clean("Có một cái số bao màu đỏ.")[0] == "Có một số bao màu đỏ."
    assert clean("Có một người anh ta mặc áo khoác màu xanh lá.")[0] == "Có một người mặc áo khoác màu xanh lá."
    assert clean("Cô gái đang đứng trên bậc thang.")[0] == "Người đang đứng trên bậc thang."
    assert clean("Một nhóm người một nhóm người đang đứng.")[0] == "Một nhóm người đang đứng."
    assert clean("Một người có vẻ như đang cầm một cây cọ.")[1:] == ([], ["hedge"])
    two = "Một người đang ngồi trên một chiếc ghế, còn một người khác đang ngồi trên một chiếc ghế."
    assert clean(two)[0] == two  # distinct objects sharing a template predicate: kept
    # repeated clause (across sentences) -> later copy removed, first kept
    assert clean("Có một chiếc xe máy đang đỗ bên cạnh quầy hàng. Ngoài ra một chiếc xe máy đang đỗ bên cạnh quầy hàng.")[:2] \
        == ("Có một chiếc xe máy đang đỗ bên cạnh quầy hàng.", ["repeat_clause"])
    # subsumed clause (quantifier/aspect words ignored, inner repeat collapsed)
    assert clean("Có một con thuyền neo đậu trên sông, cùng với đó một con thuyền neo đậu trên sông "
                 "đang neo đậu trên sông. Ngoài ra có một con thuyền đang di chuyển.")[0] \
        == "Có một con thuyền neo đậu trên sông. Ngoài ra có một con thuyền đang di chuyển."
    # repeated "đang ..." suffix inside one clause is cut
    assert clean("Một người đang nằm trên một chiếc ghế dài ở bãi biển, chân duỗi ra phía trước "
                 "đang nằm trên một chiếc ghế dài ở bãi biển.")[:2] \
        == ("Một người đang nằm trên một chiếc ghế dài ở bãi biển, chân duỗi ra phía trước.", ["repeat_span"])
    # hedged attribute piece removed; hedged head removes its whole clause; connective re-opens the caption
    assert clean("Có một cái ô màu đỏ lớn, có thể che phủ một khu vực rộng, còn có một chiếc xe.")[:2] \
        == ("Có một cái ô màu đỏ lớn, còn có một chiếc xe.", ["hedge"])
    assert clean("Một người có vẻ đang cười, áo đỏ. Bên cạnh đó có một cái bàn.")[0] == "Có một cái bàn."
    assert clean("Một người có vẻ đang cười. Bên cạnh đó một chiếc xe đạp.")[0] == "Một chiếc xe đạp."
    # dangling connectives
    assert clean("Có một cái bàn. Bên cạnh đó có .")[:2] == ("Có một cái bàn.", ["dangling_connective"])
    assert clean("Có một cái bàn, còn có")[0] == "Có một cái bàn."
    assert clean("Có một cái bàn. Ngoài ra, còn có một cái ghế.")[0] == "Có một cái bàn. Ngoài ra, còn có một cái ghế."
    assert clean("Trong ảnh, có một cái bàn, có vẻ cũ.")[0] == "Trong ảnh, có một cái bàn."
    assert clean("Một người đang lái xe máy, còn có một chiếc xe máy.")[0] \
        == "Một người đang lái xe máy, còn có một chiếc xe máy."  # no repeated span -> not shortened
    # garbled clause removed in place
    assert clean("Trong ảnh có một cái bảng giá, bên cạnh đó có một cái hệ thống.")[0] == "Trong ảnh có một cái bảng giá."
    assert clean("Có một chiếc xe, ngoài ra có một người màu đỏ, quần đen.")[0] \
        == "Có một chiếc xe, ngoài ra có một người, quần đen."
    # v3 regressions (review of v2)
    # 1. set-subset no longer deletes a different object / count
    bags = ("Một người áo trắng đang cầm một cái túi màu đen. Một người đang đứng trên vỉa hè. "
            "Một người đang đứng trên vỉa hè. Còn có một cái túi màu trắng.")
    assert clean(bags)[0] == ("Một người áo trắng đang cầm một cái túi màu đen. Một người đang đứng trên vỉa hè. "
                              "Còn có một cái túi màu trắng.")
    moto = "Một chiếc xe máy màu đỏ đang đỗ trên đường. Một chiếc xe máy màu đỏ đang đỗ trên đường. Còn có một vài chiếc xe máy."
    assert clean(moto)[0] == "Một chiếc xe máy màu đỏ đang đỗ trên đường. Còn có một vài chiếc xe máy."
    signs = ('Có một tấm biển "A" có màu đỏ, kích thước lớn, tấm biển "B" có màu vàng, kích thước lớn. '
             'Bên cạnh đó có một cái cửa màu nâu. Bên cạnh đó có một cái cửa màu nâu.')
    assert clean(signs)[0].count("kích thước lớn") == 2 and clean(signs)[0].count("cửa") == 1
    # 2. headless colour: delete the colour span only
    assert clean("Một người màu đỏ áo phông màu đỏ, quần đen.")[:2] \
        == ("Một người áo phông màu đỏ, quần đen.", ["headless_colour_span"])
    assert clean("Có một người màu xanh dương.")[0] == "Có một người."
    assert "người lớn" not in (clean("Một nhóm người màu đen, trắng lớn, khoảng 20 người đang đứng.")[0] or "")
    assert clean("Một người màu đỏ và trắng áo len đang đứng.")[0] == "Một người áo len đang đứng."
    # 3. gender: character name kept, "bé gái" -> "bé", sentence-initial "cô ấy" -> "người này"
    assert clean("Có một ông già Noel màu đỏ.")[0] == "Có một ông già Noel màu đỏ."
    assert clean("Một bé gái đang chơi.")[0] == "Một bé đang chơi."
    assert clean("Có một người. Cô ấy đang cười.")[0] == "Có một người. Người này đang cười."
    # 4. orphaned anaphor after the first clause is removed
    assert clean("Một người có vẻ đang cười. Người này đang đứng.")[0] == "Người đang đứng."
    assert clean("Một người có vẻ đang cười. Này có mái tóc. Có một cái bàn.")[0] == "Có một cái bàn."
    # 5. "có thể nhìn thấy" is not a hedge; "còn lại" is not a connective; no overlapping-compound merge
    assert clean("Một người có vẻ đang cười. Còn lại là một cái bàn.")[0] == "Còn lại là một cái bàn."
    assert clean("Có thể nhìn thấy một cái bàn.")[0] == "Có thể nhìn thấy một cái bàn."
    assert clean("Có hai cái ghế, còn lại là một cái bàn.")[0] == "Có hai cái ghế, còn lại là một cái bàn."
    assert clean("Một chiếc áo màu xanh lá lá chuối.")[0] == "Một chiếc áo màu xanh lá lá chuối."
    # template attribute repeated for a distinct object is not a repeat
    keep = "Có nhiều đôi giày, từ nhỏ đến lớn, còn có nhiều chiếc áo, từ nhỏ đến lớn."
    assert clean(keep)[0] == keep
    assert "garbled:headless_colour" in clean("Có một người màu sắc rực rỡ.")[2]
    assert "garbled:dangling_function_word" in clean("Một số người mặc áo vàng và một số.")[2]
    assert "garbled:vague_head" in clean("Bên cạnh đó có một cái hệ thống.")[2]
    assert clean("Có một cái đồ chơi màu đỏ.")[0] == "Có một cái đồ chơi màu đỏ."
    assert clean("Một người áo màu xám, quần dài màu xanh dương.")[0] == "Một người áo màu xám, quần dài màu xanh dương."
    print("selftest ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="src", default=str(ROOT / "data/supervision/sft.jsonl"))
    ap.add_argument("--out", dest="out_dir", help="output directory")
    ap.add_argument("--ngram", type=int, default=NGRAM_N, help="min length of a repeated suffix that is cut")
    ap.add_argument("--suffix", default="", help="output name suffix, e.g. _v2")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    selftest()
    if args.selftest:
        return 0
    if not args.out_dir:
        ap.error("--out is required")
    r = run(Path(args.src), Path(args.out_dir).expanduser(), args.ngram, args.suffix)
    print(json.dumps({k: v for k, v in r.items() if k != "examples"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
