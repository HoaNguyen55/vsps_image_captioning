#!/usr/bin/env python
"""NAP-lite: naming- and segmentation-aware object precision and recall for Vietnamese captions, with the
cross-annotator alternation statistic phi (V2 verification of A7's NAP; R5-03).

    NCS_DATA=data python scripts/nap.py                              # KTVIC test -> data/results/nap.json
    NCS_DATA=data python scripts/nap.py --f30ke ''                   # skip the Flickr30k Entities phi check

Extractors (captions and references alike):
  E0   rescap.chair.objects_in: syllable longest match over the 113-noun lexicon (object_prf.py, CHAIR-vi).
  E1t  E0 + tone-mark normalisation (tòa -> toà) + two exception tables, kept ONLY where KTVIC TRAIN references
       attest an entry: exocentric compounds whose first syllable is another lexicon noun (cửa hàng = shop, not
       door; '+x' = outside the 113 classes, None = not an object) and classifier readings (cây cầu = bridge, not
       tree). Candidates: A7's tables (88 compounds, 39 pairs; built with pyvi over train+test references and 8
       prediction files, hence the train filter).
  EW   list-free bound: the lexicon matched over whole pyvi words (+ a POS-Nc classifier rule); no tables.
phi(a, b) = 1 - sum_img k_ab / sum_img k_a k_b / n over each TRAIN image's n captions (k = captions naming a, b,
both; pairs with expected co-mention >= 5): 1 = two names that alternate across annotators but never appear
together (one referent), 0 = independent. Validated on Flickr30k Entities coreference (--f30ke).
Precision rules (credit of a mention m against the reference lemmas G):
  R0          E0, m in G (object_prf P)                 CHAIR-vi    E0, m or a hyponym of m in G (object_prf P_h)
  CHAIR-vi+p  CHAIR-vi with the person tree completed (8 entries; bé trai/bé gái under trẻ em, not man/woman)
  NAP-lite    E1t; same lemma, svp.matching.canonical synonym, an A7 near-synonym pair admitted by train
              phi >= 0.9, or a more general PERSON noun (completed tree). Never a more specific name, a person
              sibling or a group member.
  NAP-A7 / NAP-A7-roots   A7's own synonym/near/hierarchy lists (V2's NAP), with / without root
              superordinates (đồ, vật, con vật, +quần áo, +giày dép, +tàu thuyền) as creditable hypernyms.
  E0-phi.9    E0, m in G or train phi(m, g) >= 0.9 (list-free, symmetric)
  EW-exact, EW-NAP-lite   the pyvi whole-word extractor with exact / NAP-lite credit.
Recall: R_ex (object_prf R); R_ref = share of the reference referent clusters the caption names (E1t lemmas
linked by NAP-lite relations and never named together in one caption; a merge is refused when it would join two
co-mentioned names), a more specific name counted (R_ref) or not (R_ref_nohypo); R_ref_A7 = the same with A7's
relations (V2's R_ref, non-transitive); R_cl = clusters linked by train phi >= 0.9 alone over EW words (list-free). Decomposition of R0-false mentions (S_pred: E0 artefact;
S_gold: matches once the references are segmented; N_*: naming relation to a reference lemma; O: none), naming
level of each named referent vs the top name of the other captions (1v4), and the vague-caption stress test.
Systems vs all 5 references, and the 1v4 human protocol (each caption vs the other 4; systems vs the same 4,
fold-summed). 95% CIs resample images; paired deltas share the draws.
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from rescap.chair import _NOT_OBJECTS, _TOKEN, _ancestors, _strip_colour_phrases, objects_in  # noqa: E402
from rescap.svp.matching import canonical  # noqa: E402
from rescap.vi.lexicon import HYPERNYMS, NOUN_CLASSIFIER  # noqa: E402
from two_gold_audit import summ, weights  # noqa: E402

RESULTS = ROOT / "data" / "results"
SYSTEMS = {"P1": "p1-gold", "fuse2": "fuse2_s42", "tags_fuse2": "tags_fuse2_s42", "zero-shot": "zeroshot"}
LEXICON = frozenset(k for k in NOUN_CLASSIFIER if k not in _NOT_OBJECTS)

# ------------------------------------------------------------------------------- A7's lexical resources
_TONE = {"òa": "oà", "óa": "oá", "ỏa": "oả", "õa": "oã", "ọa": "oạ", "òe": "oè", "óe": "oé", "ỏe": "oẻ",
         "õe": "oẽ", "ọe": "oẹ", "ùy": "uỳ", "úy": "uý", "ủy": "uỷ", "ũy": "uỹ", "ụy": "uỵ"}
_TONE_RE = re.compile("(" + "|".join(_TONE) + r")(?![^\W\d_])")
COMPOUNDS: dict[str, str | None] = {
    "cửa hàng": "+cửa hàng", "cửa hiệu": "+cửa hàng", "cửa tiệm": "+cửa hàng", "cửa sổ": "+cửa sổ",
    "cửa kính": "cửa", "cửa cuốn": "cửa", "trái cây": "quả", "hoa quả": "quả", "hoa màu": "+hoa màu", "hoa văn": None,
    "pháo hoa": "+pháo hoa", "nước hoa": "+nước hoa", "hoa đăng": "+hoa đăng", "cây xăng": "+cây xăng",
    "quần áo": "+quần áo", "áo quần": "+quần áo", "giày dép": "+giày dép", "mũ nón": "mũ", "ô dù": "ô",
    "tàu thuyền": "+tàu thuyền", "nhà cửa": "nhà", "nhà sách": "nhà", "quây quần": None, "quần bò": "quần",
    "cầu thang": "+cầu thang", "cầu thang cuốn": "+cầu thang", "cầu trượt": "+cầu trượt", "cầu lông": "+cầu lông",
    "cầu nguyện": None, "quả cầu": "+quả cầu", "địa cầu": "+quả cầu", "bàn tay": "+bàn tay", "bàn chân": "+bàn chân",
    "bàn chải": "+bàn chải", "bàn phím": "+bàn phím", "bàn là": "+bàn là", "bóng đèn": "+bóng đèn", "bóng mát": None,
    "bóng râm": None, "bóng đá": "bóng", "bóng chuyền": "bóng", "túi bóng": "túi", "bong bóng": "+bong bóng",
    "cổ kính": None, "lồng kính": "+lồng kính", "bán kính": None, "kính lúp": "+kính lúp", "động vật": "+động vật",
    "cảnh vật": None, "nhân vật": None, "vật liệu": None, "vật tư": None, "bản đồ": "+bản đồ", "sơ đồ": "+bản đồ",
    "đồ vật": "đồ", "môi trường": None, "thị trường": None, "chiến trường": None, "quảng trường": "+quảng trường",
    "thông báo": None, "cảnh báo": None, "họp báo": None, "biển cảnh báo": "biển báo", "cá nhân": None,
    "phòng chống": None, "phòng dịch": None, "phòng ngừa": None, "cách ly": None, "chính sách": None,
    "mặc dù": None, "ngoại ô": None, "thịt bò": "+thịt", "thịt gà": "+thịt", "thịt lợn": "+thịt",
    "mật ong": "+mật ong", "người ta": None, "xe hơi": "+xe hơi", "xe ô tô": "ô tô", "xe ôtô": "ô tô",
    "xe mô tô": "xe máy", "xe gắn máy": "xe máy", "xe ôm": "xe máy", "tàu hoả": "+tàu hoả", "đường ray": "+đường ray",
    "đường sắt": "+đường ray", "lề đường": "+lề đường", "đường kẻ": None, "đường viền": None,
}
CLASSIFIED = {
    "cây": {"cầu", "cột", "đàn", "gậy", "trụ", "vợt", "cờ", "đèn", "chổi", "xẻng", "nhang", "nến", "kem", "dùi", "tháp",
            "bút", "dù", "ô", "súng", "kiếm", "thước", "đuốc", "sáo", "lao", "bút chì"},
    "quả": {"bóng", "bong", "núi", "chuông", "châu", "bom", "trứng", "cân", "tạ", "cầu", "lựu", "pháo", "đồi", "tim"},
}
_SYN = [("đường", "con đường"), ("phòng", "căn phòng"), ("tranh", "bức tranh"), ("sông", "dòng sông"), ("mũ", "nón"),
        ("bát", "chén"), ("cốc", "ly"), ("ô", "dù"), ("trẻ em", "đứa trẻ"), ("cặp đôi", "đôi bạn"),
        ("chàng trai", "nam thanh niên"), ("cô gái", "cô gái trẻ"), ("thanh niên", "bạn trẻ"), ("ô tô", "+xe hơi"),
        ("con vật", "+động vật"), ("đồ", "vật")]
CANON = {m: grp[0] for grp in _SYN for m in grp}
NEAR = {frozenset(p) for p in [("quầy hàng", "sạp hàng"), ("quầy hàng", "+cửa hàng"), ("sạp hàng", "+cửa hàng"),
                               ("tàu", "thuyền"), ("biển báo", "biển hiệu"), ("mỏm đá", "tảng đá"), ("vỉa hè", "+lề đường")]}
PARENTS: dict[str, tuple[str, ...]] = {
    "đàn ông": ("người",), "phụ nữ": ("người",), "trẻ em": ("người",), "thanh niên": ("người",), "học sinh": ("người",),
    "công nhân": ("người",), "cặp đôi": ("người",), "chàng trai": ("đàn ông", "thanh niên"),
    "cô gái": ("phụ nữ", "thanh niên"), "bé trai": ("trẻ em",), "bé gái": ("trẻ em",), "em bé": ("trẻ em",),
    **{v: ("xe",) for v in ("xe máy", "xe đạp", "ô tô", "xe buýt", "xe tải", "xe tăng", "xe đẩy", "xe ba gác", "xích lô")},
    "xe": ("@phương tiện",), "thuyền": ("+tàu thuyền",), "tàu": ("+tàu thuyền",), "+tàu thuyền": ("@phương tiện",),
    "máy bay": ("@phương tiện",), "+tàu hoả": ("@phương tiện",), "áo": ("+quần áo",), "quần": ("+quần áo",),
    "nón lá": ("mũ",), "giày": ("+giày dép",), "dép": ("+giày dép",), "+quần áo": ("đồ",), "+giày dép": ("đồ",),
    "mũ": ("đồ",),
    **{a: ("đồ",) for a in ("kính", "túi", "đồng hồ", "điện thoại", "ô", "bút", "dao", "chổi", "bóng", "sách", "báo",
                             "tranh", "mô hình", "bàn", "ghế", "bát", "đĩa", "cốc")},
    "toà nhà": ("nhà",), "dãy nhà": ("nhà",),
    **{a: ("con vật",) for a in ("chó", "mèo", "chim", "cá", "bò", "trâu", "gà", "vịt", "lợn", "ngựa", "voi", "khỉ",
                                  "rắn", "bướm", "ong")},
}
GROUPS = {"cặp đôi", "đôi bạn"}
ROOTS = {"đồ", "vật", "con vật", "+động vật", "+quần áo", "+giày dép", "+tàu thuyền"}
#: V2: the person tree of rescap's HYPERNYMS completed (replaces bé trai -> đàn ông and bé gái -> phụ nữ)
PERSON_FIX = {"cô gái": "phụ nữ", "chàng trai": "đàn ông", "học sinh": "người", "công nhân": "người",
              "em bé": "trẻ em", "đứa trẻ": "trẻ em", "bé trai": "trẻ em", "bé gái": "trẻ em"}
TREE = {**HYPERNYMS, **PERSON_FIX}
ORDER = ("syn", "near", "hyper", "hypo", "member", "sib_person")
LINK = {"same", "syn", "near", "hyper", "hypo", "member"}
CATS = ("S_pred", "S_gold", *(f"N_{r}" for r in ORDER), "O")
CREDITED = ("S_pred", "S_gold", "N_syn", "N_near", "N_hyper")
LEVELS = ("top", "above", "below", "other")
RULES = ("R0", "CHAIR-vi", "CHAIR-vi+p", "NAP-lite", "NAP-A7", "NAP-A7-roots", "E0-phi.9", "EW-exact", "EW-NAP-lite")
RECALLS = ("R_ex", "R_ref", "R_ref_nohypo", "R_ref_A7", "R_cl")


def norm_tone(text: str) -> str:
    return _TONE_RE.sub(lambda m: _TONE[m.group(1)], text)


def chain(x: str, tree: dict) -> set[str]:
    seen = {x}
    while x in tree and tree[x] not in seen:
        x = tree[x]
        seen.add(x)
    return seen


def a7_anc(x: str) -> set[str]:
    seen, stack = set(), [CANON.get(x, x)]
    while stack:
        n = stack.pop()
        if n not in seen:
            seen.add(n)
            stack.extend(PARENTS.get(n, ()))
    return seen


A7_PERSON = {n for n in set(PARENTS) | {"người"} if "người" in a7_anc(n)}
PERSON = {n for n in set(TREE) | set(TREE.values()) if "người" in chain(n, TREE)}


def collapse(found: list[str], anc) -> list[str]:
    """`người` + `đàn ông` names one man (objects_in's rule)."""
    out: list[str] = []
    for noun in found:
        if out and out[-1] in anc(noun) - {noun}:
            out[-1] = noun
        else:
            out.append(noun)
    return out


def make_extract(compounds: dict, classified: dict):
    vocab = {k: k for k in LEXICON} | compounds
    maxlen = max(len(k.split()) for k in vocab)

    @lru_cache(maxsize=None)
    def extract(text: str) -> frozenset[str]:
        tok, found, i = _TOKEN.findall(_strip_colour_phrases(norm_tone(text))), [], 0
        while i < len(tok):
            if tok[i] in classified and i + 1 < len(tok) and (
                    tok[i + 1] in classified[tok[i]] or " ".join(tok[i + 1:i + 3]) in classified[tok[i]]):
                i += 1
                continue
            for n in range(min(maxlen, len(tok) - i), 0, -1):
                if " ".join(tok[i:i + n]) in vocab:
                    found += [vocab[" ".join(tok[i:i + n])]] if vocab[" ".join(tok[i:i + n])] else []
                    i += n
                    break
            else:
                i += 1
        return frozenset(collapse(found, a7_anc))
    return extract


@lru_cache(maxsize=None)
def e0(text: str) -> frozenset[str]:
    return frozenset(objects_in(text))


@lru_cache(maxsize=None)
def ew(text: str) -> frozenset[str]:
    """The lexicon over WHOLE pyvi words: multi-word nouns first, a word tagged Nc skipped before a lexicon noun."""
    from pyvi import ViPosTagger, ViTokenizer
    s = " ".join(_TOKEN.findall(_strip_colour_phrases(norm_tone(text))))
    if not s:
        return frozenset()
    toks, tags = ViPosTagger.postagging(ViTokenizer.tokenize(s))
    ws = [(" ".join(_TOKEN.findall(w.replace("_", " "))), t) for w, t in zip(toks, tags) if _TOKEN.findall(w)]
    match = lambda j, ns: next((n for n in ns if j + n <= len(ws) and " ".join(w for w, _ in ws[j:j + n]) in LEXICON), 0)  # noqa: E731
    found, i = [], 0
    while i < len(ws):
        n = match(i, (3, 2))
        if not n and ws[i][1] == "Nc" and match(i + 1, (3, 2, 1)):
            i += 1
            continue
        n = n or match(i, (1,))
        found += [" ".join(w for w, _ in ws[i:i + n])] if n else []
        i += n or 1
    return frozenset(collapse(found, _ancestors))


def train_attested(refs_train: dict) -> tuple[dict, dict]:
    text = " " + " \n ".join(" ".join(_TOKEN.findall(_strip_colour_phrases(norm_tone(c))))
                             for cs in refs_train.values() for c in cs) + " "
    return ({k: v for k, v in COMPOUNDS.items() if f" {k} " in text},
            {c: {n for n in ns if f" {c} {n} " in text} for c, ns in CLASSIFIED.items()})


def alternation(caps: list[list[frozenset]], min_exp: float = 5.0) -> dict[frozenset, float]:
    obs, exp = Counter(), Counter()
    for cs in caps:
        k = Counter(o for c in cs for o in c)
        for a, b in itertools.combinations(sorted(k), 2):
            obs[a, b] += sum(1 for c in cs if a in c and b in c)
            exp[a, b] += k[a] * k[b] / len(cs)
    return {frozenset(p): 1 - obs[p] / e for p, e in exp.items() if e >= min_exp}


# ------------------------------------------------------------------------------- naming relations
@lru_cache(maxsize=None)
def a7_relation(m: str, g: str) -> str | None:
    """A7's relation of a mentioned lemma m to a reference lemma g."""
    if m == g:
        return "same"
    cm, cg = CANON.get(m, m), CANON.get(g, g)
    if cm == cg:
        return "syn"
    if frozenset((cm, cg)) in NEAR:
        return "near"
    if cm in a7_anc(cg):
        return "hyper"
    if cg in a7_anc(cm):
        return "hypo"
    if cm in A7_PERSON and cg in A7_PERSON:
        return "member" if {cm, cg} & GROUPS else "sib_person"
    return None


def lite_anc(x: str) -> set[str]:
    return chain(x, TREE) | chain(canonical(x) or x, TREE)


def lite_parent(x: str) -> str | None:
    return TREE.get(x) if x in PERSON else None


def make_lite(near_ok: set[frozenset]):
    @lru_cache(maxsize=None)
    def rel(m: str, g: str) -> str | None:
        if m == g:
            return "same"
        if (canonical(m) or m) == (canonical(g) or g):
            return "syn"
        if frozenset((m, g)) in near_ok:
            return "near"
        if m in lite_anc(g):
            return "hyper"
        if g in lite_anc(m):
            return "hypo"
        if m in PERSON and g in PERSON:
            return "member" if {m, g} & GROUPS else "sib_person"
        return None
    return rel


def best(rel, m: str, gold) -> str | None:
    rs = {rel(m, g) for g in gold}
    return next((r for r in ORDER if r in rs), None)


def clusters(caps: list[frozenset], linked) -> list[set[str]]:
    """Referent clusters: linked names never co-mentioned in one caption; a merge joining two co-mentioned
    names through a third (vague) one is refused (V2's fix of A7's union-find)."""
    lemmas = sorted(frozenset().union(*caps)) if caps else []
    together = {frozenset(p) for c in caps for p in itertools.combinations(sorted(c), 2)}
    groups = [{x} for x in lemmas]
    for a, b in itertools.combinations(lemmas, 2):
        if not linked(a, b) or frozenset((a, b)) in together:
            continue
        ga, gb = (next(g for g in groups if x in g) for x in (a, b))
        if ga is gb or any(frozenset((x, y)) in together for x in ga for y in gb):
            continue
        groups.remove(gb)
        ga |= gb
    return groups


def naming_level(m: frozenset, caps: list[frozenset], rel, canon, anc) -> list[tuple[str, float]]:
    """Per reference cluster the caption names: level of its most specific name vs the clusters' top name."""
    rows = []
    for c in clusters(caps, lambda a, b: rel(a, b) in LINK):
        hit = sorted(x for x in m if any(rel(x, g) in LINK for g in c))
        if not hit:
            continue
        names, n = Counter(), 0
        for cap in caps:
            used = {canon(x) for x in cap & c}
            n += bool(used)
            names.update(used)
        top = max(sorted(names.items()), key=lambda t: t[1])[0]
        cx = canon(max(hit, key=lambda h: len(anc(h))))
        rows.append(("top" if cx == top else "above" if cx in anc(top) else "below" if top in anc(cx) else "other",
                     names.get(cx, 0) / n))
    return rows


# ------------------------------------------------------------------------------- per-image rows
class Metric:
    """Extractors, phi tables and relations fixed from the TRAIN references."""

    def __init__(self, refs_train: dict):
        self.comp, self.clf = train_attested(refs_train)
        self.e1t = make_extract(self.comp, self.clf)
        self.ext = {"E0": e0, "E1t": self.e1t, "EW": ew}
        self.phi = {e: alternation([[f(c) for c in cs] for cs in refs_train.values()]) for e, f in self.ext.items()}
        self.near_ok = {p for p in NEAR if self.phi["E1t"].get(p, -9) >= 0.9}
        self.lite = make_lite(self.near_ok)
        lite_ok, a7_ok = {"same", "syn", "near", "hyper"}, {"same", "syn", "near"}
        self.credit = {  # rule -> (extractor, credit(m, G))
            "R0": ("E0", lambda m, G: m in G),
            "CHAIR-vi": ("E0", lambda m, G: any(m in _ancestors(g) for g in G)),
            "CHAIR-vi+p": ("E0", lambda m, G: any(m in chain(g, TREE) for g in G)),
            "NAP-lite": ("E1t", lambda m, G: any(self.lite(m, g) in lite_ok for g in G)),
            "NAP-A7": ("E1t", lambda m, G: any(a7_relation(m, g) in lite_ok for g in G)),
            "NAP-A7-roots": ("E1t", lambda m, G: any(a7_relation(m, g) in a7_ok or (a7_relation(m, g) == "hyper"
                                                                                   and m not in ROOTS) for g in G)),
            "E0-phi.9": ("E0", lambda m, G: m in G or any(self.phi["E0"].get(frozenset((m, g)), -9) >= 0.9 for g in G)),
            "EW-exact": ("EW", lambda m, G: m in G),
            "EW-NAP-lite": ("EW", lambda m, G: any(self.lite(m, g) in lite_ok for g in G)),
        }
        self.rels = {"lite": (self.lite, lambda x: canonical(x) or x, lite_anc),
                     "a7": (a7_relation, lambda x: CANON.get(x, x), a7_anc)}

    def sets(self, text: str) -> dict[str, frozenset]:
        return {e: f(text) for e, f in self.ext.items()}

    def row(self, ms: dict[str, frozenset], refs: list[str]) -> dict[str, float]:
        """Counts of one caption (mention sets per extractor) against the reference captions."""
        caps = {e: [f(r) for r in refs] for e, f in self.ext.items()}
        gold = {e: frozenset().union(*cs) for e, cs in caps.items()}
        out = {"n": 1.0}
        for r, (e, ok) in self.credit.items():
            out[f"M|{r}"], out[f"C|{r}"] = len(ms[e]), sum(ok(m, gold[e]) for m in ms[e])
        g0, g1 = gold["E0"], gold["E1t"]
        recalls = {"R_ex": (g0, lambda: len(ms["E0"] & g0) / len(g0))}
        cl = clusters(caps["E1t"], lambda a, b: self.lite(a, b) in LINK)
        for q, ok in (("R_ref", {"same", "syn", "near", "hypo"}), ("R_ref_nohypo", {"same", "syn", "near"})):
            recalls[q] = (g1, lambda ok=ok: np.mean([any(self.lite(m, g) in ok for m in ms["E1t"] for g in c) for c in cl]))
        cl7 = clusters(caps["E1t"], lambda a, b: a7_relation(a, b) in LINK)
        recalls["R_ref_A7"] = (g1, lambda: np.mean([any(a7_relation(m, g) in {"same", "syn", "near", "hypo"}
                                                        for m in ms["E1t"] for g in c) for c in cl7]))
        cl_w = clusters(caps["EW"], lambda a, b: self.phi["EW"].get(frozenset((a, b)), -9) >= 0.9)
        recalls["R_cl"] = (gold["EW"], lambda: np.mean([bool(ms["EW"] & c) for c in cl_w]))
        for q, (g, f) in recalls.items():
            out[f"r|{q}"], out[f"h|{q}"] = (f(), 1.0) if g else (0.0, 0.0)
        out["F0"] = len(ms["E0"] - g0)
        for tag, (rel, canon, anc) in self.rels.items():
            cnt = Counter()
            for f in ms["E0"] - g0:
                r = None if f not in ms["E1t"] or f in g1 else best(rel, f, g1)
                cnt["S_pred" if f not in ms["E1t"] else "S_gold" if f in g1 else f"N_{r}" if r else "O"] += 1
            out.update({f"{tag}|{c}": cnt[c] for c in CATS})
            lv = naming_level(ms["E1t"], caps["E1t"], rel, canon, anc)
            out.update({f"{tag}|n_{x}": sum(r[0] == x for r in lv) for x in LEVELS})
            out[f"{tag}|named"], out[f"{tag}|agree"] = len(lv), sum(r[1] for r in lv)
        return out


def derived(col: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Ratios of summed counts: precision per rule, recalls, decomposition shares, naming levels."""
    with np.errstate(invalid="ignore", divide="ignore"):
        out = {f"P|{r}": 100 * col[f"C|{r}"] / col[f"M|{r}"] for r in RULES}
        out.update({f"R|{q}": 100 * col[f"r|{q}"] / col[f"h|{q}"] for q in RECALLS})
        out["ref_false_per_caption"] = col["F0"] / col["n"]
        for tag in ("lite", "a7"):
            out.update({f"share|{tag}|{c}": 100 * col[f"{tag}|{c}"] / col["F0"] for c in CATS})
            out[f"credited|{tag}"] = sum(out[f"share|{tag}|{c}"] for c in CREDITED)
            out.update({f"level|{tag}|{x}": 100 * col[f"{tag}|n_{x}"] / col[f"{tag}|named"] for x in LEVELS})
            out[f"agree|{tag}"] = 100 * col[f"{tag}|agree"] / col[f"{tag}|named"]
    return out


def table(rows: dict[str, list[dict]], w: np.ndarray, base: str | None = None, prefix: str = "") -> dict:
    """Every system's derived statistics with CIs; with base, paired deltas (system - base) on the same draws."""
    keys = list(next(iter(rows.values()))[0])
    d = {s: derived(dict(zip(keys, (w @ np.array([[r[k] for k in keys] for r in rs])).T))) for s, rs in rows.items()}
    out = {s: {k: summ(v) for k, v in st.items()} for s, st in d.items()}
    if base:
        for s in d:
            if s != base:
                out[s][f"{prefix}minus_{base}"] = {k: summ(d[s][k] - d[base][k], test=True) for k in d[s]}
    return out


# ------------------------------------------------------------------------------- phi validation
def phi_by_relation(m: Metric) -> dict:
    out = {}
    for tag, rel in (("lite", m.lite), ("a7", a7_relation)):
        by = defaultdict(list)
        for p, v in m.phi["E1t"].items():
            a, b = sorted(p)
            r = rel(a, b) or rel(b, a) or "unrelated"
            by["hyper/hypo" if r in ("hyper", "hypo") else r].append(v)
        out[tag] = {r: {"pairs": len(v), "median_phi": round(float(np.median(v)), 3),
                        "share_phi>=0.9": round(float(np.mean(np.array(v) >= 0.9)), 3)} for r, v in sorted(by.items())}
    return out


def phi_f30ke(zip_path: Path) -> dict:
    """phi vs REFERENT gold: Flickr30k Entities links the NPs of an image's 5 captions to entity ids, so two head
    nouns of different captions with one id name the same referent. AUROC of phi for 'co-referent in >= half the
    images using both', precision of phi >= t, and phi vs coreference by the number of people entities."""
    phrase = re.compile(r"\[/EN#(\d+)/([^\s\]]+) ([^\]]+)\]")
    raw = {}
    with zipfile.ZipFile(zip_path) as z:
        for name in (n for n in z.namelist() if n.startswith("Sentences/") and n.endswith(".txt")):
            caps = [[(e, t.split("/")[0], re.findall(r"[a-z]+", p.lower())[-1]) for e, t, p in phrase.findall(line)
                     if e != "0" and "notvisual" not in t and re.findall(r"[a-z]+", p.lower())]
                    for line in z.read(name).decode("utf-8").splitlines()[:5]]
            if len(caps) == 5:
                raw[name] = caps
    sg = {h for caps in raw.values() for c in caps for _, _, h in c}
    irreg = {"men": "man", "women": "woman", "children": "child", "people": "people", "feet": "foot", "teeth": "tooth",
             "mice": "mouse", "geese": "goose", "knives": "knife", "wives": "wife", "leaves": "leaf"}

    def lemma(w):
        return irreg.get(w) or next((w[:-len(s)] + r for s, r in (("ies", "y"), ("es", ""), ("s", ""))
                                     if w.endswith(s) and w[:-len(s)] + r in sg), w)
    imgs = {k: [[(e, t, lemma(h)) for e, t, h in c] for c in caps] for k, caps in raw.items()}
    df = Counter(h for caps in imgs.values() for h in {h for c in caps for _, _, h in c})
    vocab = {w for w, n in df.items() if n >= 30 and len(w) > 2}
    sets = {k: [frozenset(h for _, _, h in c if h in vocab) for c in caps] for k, caps in imgs.items()}
    phi = alternation(list(sets.values()))
    both, coref = Counter(), Counter()
    for k, cs in sets.items():
        ent = defaultdict(lambda: defaultdict(set))
        for ci, c in enumerate(imgs[k]):
            for e, _, h in c:
                if h in vocab:
                    ent[e][ci].add(h)
        linked = {frozenset((a, b)) for by in ent.values() for (c1, h1), (c2, h2) in itertools.combinations(by.items(), 2)
                  for a in h1 for b in h2 if a != b}
        for p in itertools.combinations(sorted(frozenset().union(*cs)), 2):
            if frozenset(p) in phi:
                both[frozenset(p)] += 1
                coref[frozenset(p)] += frozenset(p) in linked
    ph = np.array([phi[p] for p in both])
    cr = np.array([coref[p] / both[p] for p in both])
    pos = cr >= 0.5
    ranks = rankdata(ph)
    out = {"images": len(sets), "vocab": len(vocab), "pairs": int(len(ph)), "coreferent_pairs": int(pos.sum()),
           "auroc_coref>=0.5": round(float((ranks[pos].sum() - pos.sum() * (pos.sum() + 1) / 2)
                                           / (pos.sum() * (~pos).sum())), 4)}
    out.update({f"share_coreferent_at_phi>={t}": round(float(pos[ph >= t].mean()), 3) for t in (0.5, 0.9)})
    npeople = {k: len({e for c in caps for e, t, _ in c if t == "people"}) for k, caps in imgs.items()}
    for a, b in (("man", "person"), ("person", "woman"), ("boy", "child"), ("man", "woman")):
        for lab, ok in (("1 people entity", lambda n: n == 1), (">=3 people entities", lambda n: n >= 3)):
            o = e = c = m = 0
            for k, cs in sets.items():
                if not ok(npeople[k]) or not any(a in x for x in cs) or not any(b in x for x in cs):
                    continue
                kk = Counter(x for cc in cs for x in cc)
                o, e, m = o + sum(a in cc and b in cc for cc in cs), e + kk[a] * kk[b] / 5, m + 1
                by = defaultdict(lambda: defaultdict(set))
                for ci, cc in enumerate(imgs[k]):
                    for eid, _, h in cc:
                        by[eid][ci].add(h)
                c += any(a in by[x][i] and b in by[x][j] for x in by for i in by[x] for j in by[x] if i != j)
            out[f"{a}~{b} | {lab}"] = {"images": m, "phi": round(1 - o / e, 3) if e else None,
                                       "coref": round(c / m, 3) if m else None}
    return out


# ------------------------------------------------------------------------------- main
def up(s: frozenset, parent) -> frozenset:
    """Each mention replaced by its parent (the vague-caption attack)."""
    return frozenset(parent(x) or x for x in s)


def main() -> int:
    from evaluate import references
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--f30ke", default=str(ROOT / "data/datasets/flickr30k_entities/annotations.zip"),
                    help="Flickr30k Entities annotations.zip (Plummer et al. 2015); '' skips the check")
    ap.add_argument("--out", default=str(RESULTS / "nap.json"))
    a = ap.parse_args()
    rtr, rte = references("train_data.json"), references("test_data.json")
    ids = sorted(rte)
    m = Metric(rtr)
    print(f"train-attested: {len(m.comp)}/{len(COMPOUNDS)} compounds, {sum(map(len, m.clf.values()))}/"
          f"{sum(map(len, CLASSIFIED.values()))} classifier pairs; near pairs admitted (train phi >= 0.9): "
          f"{sorted(map(sorted, m.near_ok))}", flush=True)
    out = {"what": "scripts/nap.py (V2): NAP-lite and its sensitivity band, KTVIC test", "B": a.B,
           "train_attested": {"compounds": [len(m.comp), len(COMPOUNDS)], "dropped": sorted(set(COMPOUNDS) - set(m.comp)),
                              "classifier_pairs": [sum(map(len, m.clf.values())), sum(map(len, CLASSIFIED.values()))]},
           "near_admitted": sorted(map(sorted, m.near_ok)), "phi_pairs": {e: len(v) for e, v in m.phi.items()},
           "phi_by_relation": phi_by_relation(m)}
    w = weights(len(ids), a.B)
    preds = {}
    for name, stem in SYSTEMS.items():
        for mode in ("short", "detailed"):
            p = json.loads((RESULTS / f"{stem}-{mode}.preds.json").read_text(encoding="utf-8"))
            preds[f"{name}-{mode}"] = {i: (p[i][0] if isinstance(p[i], list) else p[i]) or "" for i in ids}
    full = {s: [m.row(m.sets(p[i]), rte[i]) for i in ids] for s, p in preds.items()}
    out["systems"] = {}
    for mode in ("short", "detailed"):
        out["systems"].update(table({s: r for s, r in full.items() if s.endswith(mode)}, w, f"P1-{mode}"))
    print("vs 5 references: " + " | ".join(f"{s} R0 {v['P|R0'][0]:.1f} P_h {v['P|CHAIR-vi'][0]:.1f} lite "
                                         f"{v['P|NAP-lite'][0]:.1f} A7 {v['P|NAP-A7'][0]:.1f}" for s, v in out["systems"].items()), flush=True)

    def loo(cap_sets):  # 1v4: caption sets per fold vs the other 4 references, counts summed over the 5 folds
        rows = []
        for i in ids:
            folds = [m.row(cap_sets(i, j), rte[i][:j] + rte[i][j + 1:]) for j in range(len(rte[i]))]
            rows.append({k: sum(f[k] for f in folds) for k in folds[0]})
        return rows
    human = {"human": loo(lambda i, j: m.sets(rte[i][j]))}
    human.update({s: loo(lambda i, j, s=s: m.sets(preds[s][i])) for s in ("P1-short", "fuse2-short", "tags_fuse2-short",
                                                                        "zero-shot-short", "fuse2-detailed")})
    out["human_1v4"] = table(human, w, "human")
    print("1v4: " + " | ".join(f"{s} lite {v['P|NAP-lite'][0]:.1f} R_ref {v['R|R_ref'][0]:.1f}"
                               for s, v in out["human_1v4"].items()), flush=True)

    # vague-caption stress test: mentions moved one level up (each relation's own hierarchy), constant captions
    parents = {"lite": lite_parent,
               "a7": lambda x: next((q for q in PARENTS.get(CANON.get(x, x), ()) if not q.startswith("@")), CANON.get(x, x))}
    stress = {}
    for s in ("P1-short", "fuse2-short"):
        for tag, par in parents.items():
            stress[f"{s} up1 ({tag})"] = [m.row({e: up(v, par) for e, v in m.sets(preds[s][i]).items()}, rte[i]) for i in ids]
        stress[s] = full[s]
    for const in (["người"], ["người", "đồ"], ["người", "xe"]):
        stress[f"constant {'+'.join(const)}"] = [m.row({e: frozenset(const) for e in m.ext}, rte[i]) for i in ids]
    out["stress"] = table(stress, w)
    for s, v in out["stress"].items():
        print(f"  stress {s}: lite {v['P|NAP-lite'][0]:.1f} A7 {v['P|NAP-A7'][0]:.1f} R_ref {v['R|R_ref'][0]:.1f} "
              f"above(lite) {v['level|lite|above'][0]:.1f} above(a7) {v['level|a7|above'][0]:.1f}", flush=True)
    if a.f30ke and Path(a.f30ke).exists():
        out["phi_flickr30k_entities"] = phi_f30ke(Path(a.f30ke))
        print("Flickr30k Entities:", {k: v for k, v in out["phi_flickr30k_entities"].items() if "|" not in k}, flush=True)
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"-> {a.out}")
    return 0


def _check() -> None:
    ext = make_extract(COMPOUNDS, CLASSIFIED)
    assert ext("cô gái đứng trước một cửa hàng") == {"cô gái", "+cửa hàng"}
    assert ext("một cây cầu bắc qua sông") == {"cầu", "sông"} and ext("một cây thông lớn") == {"cây"}
    assert ext("một tòa nhà cổ kính") == {"toà nhà"} and ext("quần áo được treo") == {"+quần áo"}
    for s in ("một người đàn ông đứng cạnh chiếc xe máy màu đỏ", "chiếc áo màu xanh lá cây"):
        assert make_extract({}, {})(s) == e0(s)
    assert a7_relation("người", "cô gái") == "hyper" and a7_relation("nón", "mũ") == "syn"
    assert a7_relation("phụ nữ", "đàn ông") == "sib_person" and a7_relation("cô gái", "đôi bạn") == "member"
    lite = make_lite({frozenset(("quầy hàng", "sạp hàng"))})
    assert lite("người", "cô gái") == "hyper" and lite("cô gái", "người") == "hypo" and lite("nón", "mũ") == "syn"
    assert lite("đàn ông", "bé trai") == "sib_person" and lite("trẻ em", "bé trai") == "hyper"   # completed tree
    assert lite("quầy hàng", "sạp hàng") == "near" and lite("xe", "xe máy") is None
    caps = [frozenset({"người"}), frozenset({"phụ nữ", "đàn ông"}), frozenset({"phụ nữ"})]
    cl = clusters(caps, lambda a, b: lite(a, b) in LINK)
    assert not any({"phụ nữ", "đàn ông"} <= c for c in cl)       # never one referent through vague 'người'
    phi = alternation([[frozenset({"a"}), frozenset({"b"}), frozenset({"a", "c"})]] * 10)
    assert phi[frozenset("ab")] == 1.0 and phi[frozenset("ac")] < 0.5
    assert up(frozenset({"cô gái", "chó"}), lite_parent) == {"phụ nữ", "chó"}


if __name__ == "__main__":
    _check()
    sys.exit(main())
