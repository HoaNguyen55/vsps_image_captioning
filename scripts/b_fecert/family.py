#!/usr/bin/env python3
"""B-FECERT front-end family (Paper B, LRE). Registration manuscript/prereg/2026-11-12_b_fecert/B_FECERT_PREREG_v1_1.md
(sha256 736b7e6a...) §2 and §5.1; definitions imported from manuscript/prereg/2026-11-11_b_kappa/B_KAPPA_PREREG_v1.md
§2.2-§2.5 (the 25 White_Space code points, the final-punctuation set, letter runs, tone marks, vowel modifiers, onsets,
the strict g2 domain).

A member is f = (U, T, P, C); it is applied to a text in the order of §2.1: N, T, P-pre, U (case as written), C, P-post,
NFC per token. The word units are injected (SEG) so that the self-test runs without Java or any segmenter; the real
units are imported lazily on the host. Nothing here prints or writes text.
"""
from __future__ import annotations

import hashlib
import unicodedata
from collections import defaultdict

# ---------------------------------------------------------------------------------------------- B_KAPPA §2.2
WS = frozenset(map(chr, [*range(0x09, 0x0E), 0x20, 0x85, 0xA0, 0x1680, *range(0x2000, 0x200B), 0x2028, 0x2029,
                         0x202F, 0x205F, 0x3000]))
FINAL = frozenset(".!?…;:,")
TONES = frozenset("\u0300\u0301\u0309\u0303\u0323")  # huyền, sắc, hỏi, ngã, nặng
MODS = frozenset("\u0306\u0302\u031b")  # breve, circumflex, horn
ONSETS = frozenset("b c ch d đ g gh gi h k kh l m n ng ngh nh p ph qu r s t th tr v x".split()) | {""}
PAIRS = {("o", "a"), ("o", "e"), ("u", "y")}  # B_KAPPA §2.3

# ---------------------------------------------------------------------------------------------- §2.2 axes, §2.4 sets
T_LEVELS, P_LEVELS, C_LEVELS = ("tw", "tm", "tf"), ("pk", "pf", "pa"), ("cf", "ck")
DEV_UNITS, HELD_UNITS, CHR = ("syl", "rdr", "pyvi"), ("uts",), "chr"
WAYS = ("matched", "out", "ref")  # §5.1: both sides, outputs only, references only
RSTAR = ("rstar", None)  # §5.1: pycocoevalcap 1.2, PTB tokens, both sides as released
F0 = ("rdr", "tw", "pk", "cf")  # §2.5: the committed protocol P0


def members(units) -> list[tuple]:
    """§2.3: 3 x 3 x 2 = 18 matched members per unit."""
    return [(u, t, p, c) for u in units for t in T_LEVELS for p in P_LEVELS for c in C_LEVELS]


F_DEV = members(DEV_UNITS)  # 54
F_HELD = members(HELD_UNITS)  # 18
F = F_DEV + F_HELD  # 72 (§2.4; chr is not in F, CC-350 ruling 2)
F_CHR = members((CHR,))
FPLUS = [(w, m) for m in F + F_CHR for w in WAYS] + [RSTAR]  # 90 x 3 + 1 = 271 (§5.1)


def name(m) -> str:
    """Member name for outputs: 'rdr.tw.pk.cf'; F+ entries 'out:rdr.tw.pk.cf' and 'r*'."""
    if len(m) == 4:
        return ".".join(m)
    return "r*" if m == RSTAR else (name(m[1]) if m[0] == "matched" else f"{m[0]}:{name(m[1])}")


# ---------------------------------------------------------------------------------------------- §2.1 steps
def n_step(t: str) -> str:
    """Step N: NFC; U+005F to U+0020; every maximal White_Space run to one space; trimmed."""
    t = unicodedata.normalize("NFC", t).replace("_", " ")
    out, sp = [], False
    for ch in t:
        if ch in WS:
            sp = True
            continue
        if sp and out:
            out.append(" ")
        sp = False
        out.append(ch)
    return "".join(out)


def _letter(ch: str) -> bool:
    return unicodedata.category(ch)[0] in "LM"


def _g2(run: str, level: str) -> str:
    """B_KAPPA §2.3 strict domain on one letter run; the mark goes to the second (tm) or first (tf) pair letter.
    Matched on a lower-cased NFD copy because T runs before case here (§2.1); the written case is kept."""
    letters = []  # [base char, [marks]]
    for ch in unicodedata.normalize("NFD", run):
        if unicodedata.combining(ch) and letters:
            letters[-1][1].append(ch)
        elif unicodedata.combining(ch):
            return run
        else:
            letters.append([ch, []])
    if len(letters) < 2:
        return run
    marks = [(k, m) for k, (_, ms) in enumerate(letters) for m in ms]
    if len(marks) != 1 or marks[0][1] not in TONES or marks[0][0] < len(letters) - 2:
        return run
    pair = (letters[-2][0].lower(), letters[-1][0].lower())
    onset = "".join(b for b, _ in letters[:-2]).lower()
    if pair not in PAIRS or onset not in ONSETS:
        return run
    tone = marks[0][1]
    letters[-2][1], letters[-1][1] = ([], [tone]) if level == "tm" else ([tone], [])
    return unicodedata.normalize("NFC", "".join(b + "".join(ms) for b, ms in letters))


def tone(t: str, level: str) -> str:
    """Axis T (§2.2): tw as written; tm, tf rewrite every g2-variable letter run (letter run = categories L*, M*)."""
    if level == "tw":
        return t
    out, run = [], []
    for ch in t + "\0":
        if _letter(ch):
            run.append(ch)
            continue
        if run:
            out.append(_g2("".join(run), level))
            run = []
        out.append(ch)
    return "".join(out[:-1])


def _punct(ch: str) -> bool:
    return unicodedata.category(ch).startswith("P")


def p_pre(t: str, level: str) -> str:
    """Axis P before the unit (§2.2): pf strips the trailing run over FINAL and White_Space (κ step 5); pa puts one
    space before and after every character of general category P*."""
    if level == "pf":
        k = len(t)
        while k and (t[k - 1] in FINAL or t[k - 1] in WS):
            k -= 1
        return t[:k]
    if level == "pa":
        return "".join(f" {ch} " if _punct(ch) else ch for ch in t)
    return t


def p_post(toks: list[str], level: str) -> list[str]:
    """Axis P after the unit: pa drops every token made only of P* characters."""
    return [w for w in toks if not all(map(_punct, w))] if level == "pa" else toks


def case(toks: list[str], level: str) -> list[str]:
    return [w.casefold() for w in toks] if level == "cf" else toks


# ---------------------------------------------------------------------------------------------- units (§2.2 U)
def _rdr(texts: list[str]) -> list[list[str]]:
    import protocol_pilot as E4  # scripts/kit_b, reused unchanged (§12)
    out = []
    for k in range(0, len(texts), 20000):
        out += E4.rdr(texts[k:k + 20000])
    return [s.split() for s in out]


def _pyvi(texts: list[str]) -> list[list[str]]:
    from pyvi import ViTokenizer
    return [ViTokenizer.tokenize(t).split() for t in texts]


def _uts(texts: list[str]) -> list[list[str]]:
    from underthesea import word_tokenize  # call form of §2.2; the code read checks it on the installed release
    return [word_tokenize(t, format="text").split() for t in texts]


SEG = {"syl": lambda ts: [t.split() for t in ts], "rdr": _rdr, "pyvi": _pyvi, "uts": _uts,
       "chr": lambda ts: [[ch for ch in t if ch not in WS] for t in ts]}


class Tok:
    """Applies members to texts. One segmenter call per unit over the unique pre-unit strings (prime), then cached."""

    def __init__(self, seg: dict | None = None):
        self.seg = seg or SEG
        self.cache: dict = {}
        self.n: dict = {}

    def _pre(self, raw: str, t: str, p: str) -> str:
        if raw not in self.n:
            self.n[raw] = n_step(raw)
        return p_pre(tone(self.n[raw], t), p)

    def prime(self, texts, mems) -> None:
        need = defaultdict(set)
        for u, t, p, _c in {m[:3] + ("",) for m in mems}:
            for raw in texts:
                x = self._pre(raw, t, p)
                if (u, x) not in self.cache:
                    need[u].add(x)
        for u, xs in need.items():
            xs = sorted(xs)
            got = self.seg[u](xs)
            if len(got) != len(xs):
                raise RuntimeError(f"unit {u}: alignment lost")
            self.cache.update({(u, x): g for x, g in zip(xs, got)})

    def tokens(self, raw: str, m) -> list[str]:
        """§2.1 steps 1-7 for member m = (U, T, P, C)."""
        u, t, p, c = m
        x = self._pre(raw, t, p)
        if (u, x) not in self.cache:
            self.prime([raw], [m])
        toks = p_post(case(list(self.cache[(u, x)]), c), p)
        return [unicodedata.normalize("NFC", w) for w in toks]

    def side(self, raw: str, way: str, m, is_ref: bool) -> str:
        """§5.1 ways. 'matched' applies m to both sides; 'out' to outputs only and 'ref' to references only, the other
        side getting N and a whitespace split. Returns the space-joined tokens the kit scorers read."""
        if (way == "out" and is_ref) or (way == "ref" and not is_ref):
            return " ".join(n_step(raw).split())
        return " ".join(self.tokens(raw, m))


def key(texts: list[str]) -> str:
    """Token identity of a side (§2.5 merging): sha256 of the token strings in image order."""
    return hashlib.sha256("\n".join(texts).encode("utf-8")).hexdigest()[:16]


def classes(keys: dict) -> list[list]:
    """§2.5: members are one class when their token keys are equal (never by score). keys: {member: key}."""
    out = defaultdict(list)
    for m, k in keys.items():
        out[k].append(m)
    return list(out.values())


# ---------------------------------------------------------------------------------------------- §2.6 F1, F3
TOY = [("hoà", "hòa"), ("khoẻ", "khỏe"), ("thuỷ", "thủy"), ("uỷ", "ủy"), ("xoè", "xòe"),  # B_KAPPA §3.1 g2 row
       ("hoà bình", "hòa bình"), ("toà nhà", "tòa nhà"), ("sức khoẻ", "sức khỏe"), ("thuỷ thủ", "thủy thủ")]  # O9
TOY_B_KAPPA = 5  # TOY[:5] is the B_KAPPA §3.1 row; TOY[5:] are additions, labelled so in FAMILY.json (CC-361 NB7)


def f1(unit: str, refs: list[str], seg: dict | None = None) -> dict:
    """§2.6 F1 on the references (after N). A string fails when it comes back empty from a non-empty input, or the
    batch loses alignment. A unit that raises (absent, wrong release, crash) is not a string failure: the exception
    goes up and stage F makes it a FAULT, never a K-unit drop (CC-361 D6). 'Whitespace fallback' = no token of any
    reference holds '_' (a word segmenter that joins no syllable)."""
    seg = seg or SEG
    xs = [n_step(r) for r in refs]
    got = seg[unit](xs)
    aligned = len(got) == len(xs)
    failed = len(xs) if not aligned else sum(bool(x.strip()) and not g for x, g in zip(xs, got))
    fallback = aligned and not any("_" in w for g in got for w in g)
    share = failed / max(1, len(xs))
    return {"unit": unit, "strings": len(xs), "failed": failed, "aligned": aligned, "whitespace_fallback": fallback,
            "dropped": (not aligned) or fallback or share > F1_FAIL_MAX}


F1_FAIL_MAX = 0.005  # §2.6 F1: more than 0.5% failed strings drops the unit


def f3(unit: str, seg: dict | None = None) -> list[dict]:
    """§2.6 F3: the unit's tokens for the tm and tf spellings of each toy string (registered toy strings, no data)."""
    tk, m = Tok(seg), (unit, "tw", "pk", "ck")
    out = []
    for k, (a, b) in enumerate(TOY):
        tm, tf = tk.tokens(a, m), tk.tokens(b, m)
        out.append({"tm": tm, "tf": tf, "equal": tm == tf, "addition": k >= TOY_B_KAPPA})
    return out
