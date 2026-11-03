#!/usr/bin/env python3
"""B-PA1-T1 map v1 + crosswalk (v3.1 §6.1, §6.4 step 1) and parity run 1 (§6.3, §6.4 step 2).
TIER 1 / DEV-EXPLORE (B-PA1-T1). DRAFT, uncommitted, never run on real inputs: needs its own judge read.

    python3 -I -B scripts/b_pa1/map_v1.py selftest                                  synthetic fixtures only
    python3 -I -B scripts/b_pa1/map_v1.py build --categories C --out-dir D [--alias A]
    python3 -I -B scripts/b_pa1/map_v1.py parity --map D/b_pa1_map_v1.json          once; writes D/parity1.json

/usr/bin/python3 3.12.3 (the R3 pin interpreter); stdlib + repo only. No segmenter is loaded (R7 is re-hashed only).
crosswalk: an Objects365 class links to a COCO-80 class iff one '/'-part of its lowercased name is a key of Paper A's
  Rohrbach synonyms (score_coco_probe.load_synonyms) and all such parts name one class [dictionary]; then the
  LOG-pinned alias file (CC-230 W2-W4): strikes remove dictionary links, aliases add links [instrument], 'none'
  records a COCO class with no counterpart. The build refuses while any COCO class has no link and no 'none'.
map v1: Paper A's COCO-80 lexicon (score_coco_probe.load_vi_terms over coco80_vi.json, matcher v2), every distinct
  term in matcher order, first wins; rows = term x every Objects365 class the crosswalk links to the term's class.
parity: matcher v2 (vi_objects: LEX_V2, then vi_classes) vs the same procedure over the map v1 terms, mapped
  Objects365 -> COCO-80 by the crosswalk; UIT-ViIC test 231, all references, A's COCO instance gold. Micro P over
  mentions, Delta = 100 (P_new - P_v2); stdout and parity1.json carry only micro Delta, macro Delta, drop counts (W1).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]  # -I drops the script folder
import b_pa1 as B  # noqa: E402  LABEL, LOG, PIN_RE, delimited, pin_line, write_new, must_refuse, pin_cases, EX, EX_SHA
import score_coco_probe as sc  # noqa: E402  matcher v2 (Paper A); imports rescap.chair

ROOT = B.K.ROOT
CAT_NAME, ALIAS_NAME = "o365_categories_v1.json", "b_pa1_crosswalk_alias.json"
MAP_NAME, XW_NAME, OUT_NAME = "b_pa1_map_v1.json", "b_pa1_crosswalk_v1.json", "parity1.json"
N_CLASSES, N_IMAGES = 365, 231
#: matcher v2 files outside rescap/ (R3 addendum pin line); the rescap/ files are found at run time (R3, LOG l.1246)
SRC = ("scripts/score_coco_probe.py", "data/coco_probe/coco80_vi.json", "data/coco_probe/chair_synonyms.txt")
R7 = (".session_backup/machines/n2/ncs-data/vncorenlp/VnCoreNLP-1.2.jar",  # LOG l.1247, re-cited at the freeze
      ".session_backup/machines/n2/ncs-data/vncorenlp/models/wordsegmenter/wordsegmenter.rdr",
      ".session_backup/machines/n2/ncs-data/vncorenlp/models/wordsegmenter/vi-vocab",
      ".session_backup/2026-11-02/b_pa1/r7/vietnamese-stopwords-dash.txt",
      ".session_backup/2026-11-02/b_pa1/r7/R7_CHOICE.md")
REFS, GOLD = "data/datasets/uitviic/test_data.json", "data/uitviic/instance_gold.json"
_OPS = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z OPS-[0-9A-Za-z-]+-"
START_RE, DONE_RE = re.compile(_OPS + "parity1-start: "), re.compile(_OPS + "parity1-done: ")
LIMIT = Fraction(2)  # §6.3: |Delta| > 2.0 points fires PA3


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canon(o) -> bytes:
    return (json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def fires(delta: Fraction) -> bool:
    return abs(delta) > LIMIT


# ------------------------------------------------------------------------------------------------ pins
def pinned(log: Path, rel: str, root: Path = ROOT) -> str:
    p = root / rel
    s = B.K.sha_file(p) if p.is_file() else ""
    if not B.pin_line(log, s, rel):
        raise SystemExit(f"REFUSED: {rel} has no LOG pin line at its current sha")
    return s


def r3(log: Path, root: Path = ROOT) -> dict:
    """R3: every rescap/ file this process loaded (LOG l.1246) plus SRC (addendum); RESCAP_RAW_TONE must be unset."""
    if "RESCAP_RAW_TONE" in os.environ:
        raise SystemExit("REFUSED: RESCAP_RAW_TONE is set (R3 pin: unset)")
    pkg = (ROOT / "rescap").resolve()
    rels = sorted({Path(m.__file__).resolve().relative_to(ROOT.resolve()).as_posix()
                   for m in list(sys.modules.values())
                   if getattr(m, "__file__", None) and pkg in Path(m.__file__).resolve().parents})
    if "rescap/chair.py" not in rels:
        raise SystemExit("REFUSED: rescap.chair not loaded")
    return {**{r: pinned(log, r) for r in rels}, **{r: pinned(log, r, root) for r in SRC}}


def at(lines: list[str], rx: re.Pattern, *toks: str) -> list[int]:
    """Indices of LOG lines matching rx at the start and carrying every token, delimited as B.pin_line does."""
    ts = [B.delimited(t) for t in toks]
    return [i for i, ln in enumerate(lines) if rx.search(ln) and all(t.search(ln) for t in ts)]


# ------------------------------------------------------------------------------------------------ build
def crosswalk(cats: list[dict], syn: dict[str, str], alias: dict | None = None):
    """Dictionary links, then the pinned alias file (CC-230 W2-W4): `strikes` remove dictionary links, `aliases` add
    instrument links, `none` records a COCO-80 class with no Objects365 counterpart. Every entry carries a reason."""
    links, ambiguous = {}, []
    for c in cats:
        hit = {syn[a] for a in (x.strip().lower() for x in c["name"].split("/")) if a in syn}
        if len(hit) == 1:
            links[c["id"]] = (hit.pop(), "dictionary")
        elif hit:
            ambiguous.append(c["id"])
    al, coco, ids = alias or {}, set(syn.values()), {c["name"]: c["id"] for c in cats}
    for part in ("strikes", "aliases", "none"):
        for e in al.get(part, []):
            if e.get("coco80") not in coco or not str(e.get("why", "")).strip():
                raise SystemExit("REFUSED: an alias-file entry needs a COCO-80 class and a reason")
            if part != "none" and e.get("o365") not in ids:
                raise SystemExit("REFUSED: alias file names a class that is not in the pinned class list")
    struck = []
    for e in al.get("strikes", []):
        i = ids[e["o365"]]
        if links.get(i) != (e["coco80"], "dictionary"):
            raise SystemExit("REFUSED: a strike must name an existing dictionary link")
        del links[i]
        struck.append(i)
    for e in al.get("aliases", []):
        i = ids[e["o365"]]
        if i in links or i in struck:
            raise SystemExit("REFUSED: alias would change an existing or struck link (add-only)")
        links[i] = (e["coco80"], "instrument")
    return links, sorted(ambiguous), sorted(struck), [e["coco80"] for e in al.get("none", [])]


def build_docs(cats_b: bytes, vi_terms, syn: dict, prov: dict, alias: dict | None = None,
               n: int = N_CLASSES) -> tuple[bytes, bytes, dict]:
    cats = json.loads(cats_b)["categories"]
    if len(cats) != n or len({c["id"] for c in cats}) != n:
        raise SystemExit(f"REFUSED: {len(cats)} classes, {n} distinct needed")
    coco = sorted(set(syn.values()))
    if {k for _, k in vi_terms} - set(coco):
        raise SystemExit("REFUSED: a lexicon class is not a synonyms class")
    links, amb, struck, none = crosswalk(cats, syn, alias)
    pre = {k: sorted(i for i, (kk, _) in links.items() if kk == k) for k in coco}
    gap = [k for k in coco if not pre[k]]
    if len(set(none)) != len(none) or set(none) - set(gap):
        raise SystemExit("REFUSED: a 'none' record names a linked or repeated COCO-80 class")
    if set(gap) - set(none):  # CC-230 W2(a)/W4: no COCO class is ever left silently unlinked, a strike included
        raise SystemExit(f"REFUSED: {len(set(gap) - set(none))} COCO-80 classes have no link and no 'none' record")
    terms, seen = [], set()
    for v, k in vi_terms:  # matcher order; a repeated term never matches again in vi_classes, so first wins
        if v not in seen:
            seen.add(v)
            terms.append({"vi": v, "coco80": k})
    rows = [{"vi": t["vi"], "o365_id": i, "tag": links[i][1]} for t in terms for i in pre[t["coco80"]]]
    xw = canon({"schema": "vsps.b_pa1.crosswalk.v1", "tier": B.LABEL, **prov, "ambiguous": amb, "struck": struck,
                "coco80_none": sorted(none),
                "links": [{"o365_id": i, "coco80": k, "tag": t} for i, (k, t) in sorted(links.items())]})
    mp = canon({"schema": "vsps.b_pa1.map.v1", "tier": B.LABEL, **prov, "crosswalk_sha256": sha(xw),
                "terms": terms, "rows": rows})
    tags = Counter(t for _, t in links.values())
    return mp, xw, {"n_categories": n, "links_dictionary": tags["dictionary"], "links_instrument": tags["instrument"],
                    "strikes": len(struck), "ambiguous": len(amb), "unlinked": n - len(links) - len(amb),
                    "n_terms": len(terms), "terms_unmapped": sum(not pre[t["coco80"]] for t in terms),
                    "n_rows": len(rows), "coco80_without_o365": gap}


def cmd_build(a, log: Path = B.LOG, root: Path = ROOT, n: int = N_CLASSES,
              load=(sc.load_vi_terms, sc.load_synonyms)) -> int:
    cat_b = a.categories.read_bytes()
    if a.categories.name != CAT_NAME or not B.pin_line(log, sha(cat_b), CAT_NAME, f"n={n}"):
        raise SystemExit(f"REFUSED: not the R6-pinned {CAT_NAME} (name, sha, n={n} on a LOG pin line)")
    prov = {"categories_sha256": sha(cat_b), "sources": r3(log, root),
            "r7": {r: pinned(log, r, root) for r in R7}, "code_sha256": B.K.sha_file(Path(__file__)),
            "alias_sha256": None}
    alias = None
    if a.alias:
        al_b = a.alias.read_bytes()
        if a.alias.name != ALIAS_NAME or not B.pin_line(log, sha(al_b), ALIAS_NAME):
            raise SystemExit(f"REFUSED: not a LOG-pinned {ALIAS_NAME}")
        alias, prov["alias_sha256"] = json.loads(al_b), sha(al_b)
        who = alias.get("provenance")
        if not isinstance(who, dict) or not all(str(who.get(f, "")).strip() for f in ("drafter", "utc")):
            raise SystemExit("REFUSED: alias file has no provenance (drafter, utc; CC-230 W3)")
    out = a.out_dir.resolve()
    if root.resolve() in out.parents and (root / ".session_backup").resolve() not in out.parents:
        raise SystemExit("REFUSED: --out-dir is inside the tracked tree")
    vi_terms, syn = load[0](), load[1]()
    mp, xw, rec = build_docs(cat_b, vi_terms, syn, prov, alias, n)
    out.mkdir()  # new directory only
    B.write_new(out / XW_NAME, xw)
    B.write_new(out / MAP_NAME, mp)
    print(json.dumps({"tier": B.LABEL, **rec, "map_sha256": sha(mp), "crosswalk_sha256": sha(xw)},
                     ensure_ascii=False))
    return 0


# ------------------------------------------------------------------------------------------------ parity
def load_inputs(ids: list[int], refs_b: bytes, gold_b: bytes) -> tuple[dict, dict]:
    refs: dict[str, list[str]] = {}
    for x in json.loads(refs_b)["annotations"]:  # as Paper A's ann_refs: every reference, file order
        if x.get("caption"):
            refs.setdefault(str(x["image_id"]), []).append(x["caption"])
    want = {str(i) for i in ids}
    if len(want) != N_IMAGES or set(refs) != want:
        raise SystemExit(f"REFUSED: {len(want)} listed ids, {len(set(refs) ^ want)} differ from the references")
    inst = json.loads(gold_b)
    if want - set(inst):
        raise SystemExit(f"REFUSED: {len(want - set(inst))} images have no instance gold row")
    return refs, {i: set(inst[i]["coco"]) for i in want}


def parity(refs: dict, gold: dict, v2_terms, mp: dict, xw: dict) -> dict:
    tgt: dict[str, list[int]] = {}
    for r in mp["rows"]:
        tgt.setdefault(r["vi"], []).append(r["o365_id"])
    to80 = {x["o365_id"]: x["coco80"] for x in xw["links"]}
    new_terms = [(t["vi"], t["vi"]) for t in mp["terms"]]
    acc = {s: [0, 0, []] for s in ("v2", "new")}  # tp, mentions, per-reference precision
    drop = Counter()
    for i in sorted(refs, key=int):
        for text in refs[i]:
            new = set()
            for v in sc.vi_objects(text, new_terms):
                ids = tgt.get(v, [])
                drop["term_hits_without_o365_row"] += not ids
                drop["o365_hits_without_coco80"] += sum(c not in to80 for c in ids)
                new |= {to80[c] for c in ids if c in to80}
            for s, m in (("v2", sc.vi_objects(text, v2_terms)), ("new", new)):
                if not m:
                    drop[f"refs_without_mention_{s}"] += 1
                    continue
                tp = len(m & gold[i])
                acc[s][0] += tp
                acc[s][1] += len(m)
                acc[s][2].append(Fraction(tp, len(m)))
    micro = {s: Fraction(a[0], a[1]) for s, a in acc.items()}
    macro = {s: sum(a[2], Fraction(0)) / len(a[2]) for s, a in acc.items()}
    return {"delta": 100 * (micro["new"] - micro["v2"]), "delta_macro": 100 * (macro["new"] - macro["v2"]),
            "n_refs": sum(map(len, refs.values())), **{k: drop[k] for k in DROPS[1:]}}


DROPS = ("n_refs", "refs_without_mention_v2", "refs_without_mention_new", "term_hits_without_o365_row",
         "o365_hits_without_coco80")


def record(p: dict) -> dict:
    """W1: only micro Delta, its stop flag, macro Delta and drop counts leave the process. The exact fractions stay
    inside and the printed Deltas are rounded to 3 dp, so no denominator (mention count, hence P level) can be
    recovered from them (CC-230 N3); the stop flag is computed on the exact fraction."""
    return {"tier": B.LABEL, "run": "parity1", "delta_micro_points": round(float(p["delta"]), 3),
            "abs_delta_micro_gt_2": fires(p["delta"]), "delta_macro_points": round(float(p["delta_macro"]), 3),
            **{k: p[k] for k in DROPS}}


def cmd_parity(a, log: Path = B.LOG, root: Path = ROOT, load=sc.load_vi_terms) -> int:
    mp_b = a.map.read_bytes()
    xw_b = (a.map.parent / XW_NAME).read_bytes()
    mp, msha, xsha = json.loads(mp_b), sha(mp_b), sha(xw_b)
    if a.map.name != MAP_NAME or mp.get("crosswalk_sha256") != xsha:
        raise SystemExit("REFUSED: map v1 and its crosswalk do not belong together")
    freeze = (msha, MAP_NAME, XW_NAME, xsha, mp["categories_sha256"], *mp["r7"].values(),
              *([mp["alias_sha256"]] if mp["alias_sha256"] else []))
    if not B.pin_line(log, *freeze):
        raise SystemExit("REFUSED: no freeze pin line (map, crosswalk, class list, R7 and alias shas on one line)")
    if r3(log, root) != mp["sources"]:
        raise SystemExit("REFUSED: matcher v2 files differ from those map v1 was built with")
    ex_b, refs_b, gold_b = ((root / r).read_bytes() for r in (B.EX, REFS, GOLD))
    if sha(ex_b) != B.EX_SHA:
        raise SystemExit("REFUSED: exclusion.json differs from its pin")
    lines = log.read_text(encoding="utf-8").splitlines()
    here = str(a.map.parent.resolve())  # the run directory: a copied map elsewhere has no start line
    starts = at(lines, START_RE, msha, xsha, sha(refs_b), sha(gold_b), B.EX_SHA, here)
    if len(starts) != 1 or starts[0] < min(at(lines, B.PIN_RE, *freeze)):
        raise SystemExit("REFUSED: need exactly one parity1-start line, after the freeze pin line")
    if at(lines, DONE_RE, msha):
        raise SystemExit("REFUSED: parity run 1 is already done for this map")
    refs, gold = load_inputs(json.loads(ex_b)["ids"]["coco"]["uitviic_test"], refs_b, gold_b)
    xw, v2_terms = json.loads(xw_b), load()
    fd = os.open(a.map.parent / OUT_NAME, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)  # once: before computing
    with os.fdopen(fd, "wb") as f:
        data = canon(record(parity(refs, gold, v2_terms, mp, xw)))
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    sys.stdout.write(data.decode())
    return 0


# ------------------------------------------------------------------------------------------------ selftest
def exists_error(fn) -> bool:
    """True iff fn() stops on an existing output (O_EXCL / mkdir), the once-only guards."""
    try:
        fn()
    except FileExistsError:
        return True
    return False


def selftest() -> int:  # noqa: C901  one linear script of fixtures
    import random
    import tempfile
    from types import SimpleNamespace as NS

    syn = {"person": "person", "man": "person", "people": "person", "tv": "tv", "monitor": "tv",
           "dining table": "dining table", "table": "dining table", "desk": "dining table",
           "sports ball": "sports ball", "ball": "sports ball", "car": "car", "bowl": "bowl", "cup": "cup"}
    names = ["Person", "Moniter/TV", "Desk", "Golf Ball", "Cup/Bowl", "Lamp", "People", "Car"]
    cats = [{"id": i + 1, "name": m} for i, m in enumerate(names)]
    n = len(cats)
    vt = [("ô tô", "car"), ("người", "person"), ("ti vi", "tv"), ("bàn", "dining table"), ("tô", "bowl"),
          ("quả bóng", "sports ball"), ("người", "car"), ("ly", "cup")]
    cb = lambda cs: json.dumps({"categories": cs}).encode()  # noqa: E731
    prov = {"categories_sha256": "c" * 64}

    no = lambda *ks: [{"coco80": k, "why": "no class denotes it"} for k in ks]  # noqa: E731
    al = lambda o, k: {"o365": o, "coco80": k, "why": "name denotes it"}  # noqa: E731
    NONE = {"none": no("bowl", "cup", "sports ball")}

    links, amb, struck, none = crosswalk(cats, syn)
    assert links == {1: ("person", "dictionary"), 2: ("tv", "dictionary"), 3: ("dining table", "dictionary"),
                     7: ("person", "dictionary"), 8: ("car", "dictionary")} and amb == [5], (links, amb)
    lk, _, st, _ = crosswalk(cats, syn, {"aliases": [al("Golf Ball", "sports ball")], "strikes": [al("People", "person")]})
    assert lk[4] == ("sports ball", "instrument") and 7 not in lk and st == [7], (lk, st)
    for bad, word in (({"aliases": [al("Lamp", "lamp")]}, "COCO-80"), ({"aliases": [al("Telly", "tv")]}, "not in the"),
                      ({"aliases": [al("Person", "car")]}, "add-only"),
                      ({"strikes": [al("People", "person")], "aliases": [al("People", "car")]}, "add-only"),
                      ({"strikes": [al("Lamp", "car")]}, "existing dictionary link"),
                      ({"strikes": [al("People", "tv")]}, "existing dictionary link"),
                      ({"aliases": [{"o365": "Golf Ball", "coco80": "sports ball", "why": " "}]}, "reason"),
                      ({"none": [{"coco80": "bowl"}]}, "reason"), ({"none": no("kite")}, "COCO-80")):
        B.must_refuse(lambda: crosswalk(cats, syn, bad), word)

    mp_b, xw_b, rec = build_docs(cb(cats), vt, syn, prov, NONE, n)
    shuf = cats[:]
    random.Random(3).shuffle(shuf)
    assert (mp_b, xw_b) == build_docs(cb(shuf), vt, syn, prov, NONE, n)[:2], "class order changes the bytes"
    mp, xw = json.loads(mp_b), json.loads(xw_b)
    assert [t["vi"] for t in mp["terms"]] == ["ô tô", "người", "ti vi", "bàn", "tô", "quả bóng", "ly"], mp["terms"]
    assert [(r["vi"], r["o365_id"]) for r in mp["rows"]] == [("ô tô", 8), ("người", 1), ("người", 7),
                                                             ("ti vi", 2), ("bàn", 3)], mp["rows"]
    assert mp["crosswalk_sha256"] == sha(xw_b) and all(r["tag"] == "dictionary" for r in mp["rows"])
    assert rec["coco80_without_o365"] == ["bowl", "cup", "sports ball"] and rec["unlinked"] == 2, rec
    assert xw["coco80_none"] == ["bowl", "cup", "sports ball"] and rec["strikes"] == 0, xw
    assert not any(m.encode() in mp_b + xw_b for m in names), "an Objects365 class name reached map or crosswalk"
    ins = {"aliases": [al("Golf Ball", "sports ball")], "none": no("bowl", "cup")}
    mp_i = json.loads(build_docs(cb(cats), vt, syn, prov, ins, n)[0])
    assert {"vi": "quả bóng", "o365_id": 4, "tag": "instrument"} in mp_i["rows"], mp_i["rows"]
    # mandatory completeness: a gap without 'none' refuses, also when a strike opens it; 'none' on a linked class too
    B.must_refuse(lambda: build_docs(cb(cats), vt, syn, prov, n=n), "no link and no 'none'")
    B.must_refuse(lambda: build_docs(cb(cats), vt, syn, prov, {**NONE, "strikes": [al("Desk", "dining table")]}, n),
                  "no link and no 'none'")
    stk = {"strikes": [al("Desk", "dining table")], "none": no("bowl", "cup", "sports ball", "dining table")}
    xs, _, rs = build_docs(cb(cats), vt, syn, prov, stk, n)
    assert rs["strikes"] == 1 and "dining table" in rs["coco80_without_o365"] and json.loads(xs)["terms"], rs
    assert ("bàn", 3) not in [(r["vi"], r["o365_id"]) for r in json.loads(xs)["rows"]], "struck link made a row"
    B.must_refuse(lambda: build_docs(cb(cats), vt, syn, prov, {"none": no("bowl", "cup", "sports ball", "tv")}, n),
                  "linked or repeated")
    B.must_refuse(lambda: build_docs(cb(cats), vt, syn, prov, {"none": no("bowl", "cup", "sports ball", "cup")}, n),
                  "linked or repeated")
    B.must_refuse(lambda: build_docs(cb(cats[:-1]), vt, syn, prov, NONE, n), "distinct needed")
    B.must_refuse(lambda: build_docs(cb([*cats[:-1], {"id": 1, "name": "x"}]), vt, syn, prov, NONE, n), "distinct")
    B.must_refuse(lambda: build_docs(cb(cats), [*vt, ("x", "kite")], syn, prov, NONE, n), "synonyms class")

    # parity: hand-computed. Gold: image 1 {person, tv}, image 2 {car}. v2 terms = vt (A's lexicon stand-in).
    refs = {"1": ["người xem ti vi", "người ghi bàn", "một bàn", "x", "quả bóng và người", "ti vi"],
            "2": ["ô tô", "người lái ô tô"]}
    gold = {"1": {"person", "tv"}, "2": {"car"}}
    p = parity(refs, gold, vt, mp, xw)
    # v2 mentions/tp: {p,tv}2/2 {p}1/1 {table}0/1 - {ball,p}1/2 {tv}1/1 | {car}1/1 {p,car}1/2 -> 7/10; 1 ref none
    # new: ball has no row -> {p}1/1 there; table links -> {table}0/1 -> 7/9; 1 ref none
    dm = 100 * (sum([1, 1, 0, 1, 1, 1, Fraction(1, 2)], Fraction(0)) / 7 -
                sum([1, 1, 0, Fraction(1, 2), 1, 1, Fraction(1, 2)], Fraction(0)) / 7)
    assert (p["delta"], p["delta_macro"]) == (100 * (Fraction(7, 9) - Fraction(7, 10)), dm), p
    assert tuple(p[k] for k in DROPS) == (8, 1, 1, 1, 0), p
    full = json.loads(build_docs(cb(cats), [x for x in vt if x[1] in {"car", "person", "tv"}], syn, prov, NONE, n)[0])
    assert parity(refs, gold, [x for x in vt if x[1] in {"car", "person", "tv"}], full, xw)["delta"] == 0, \
        "complete crosswalk must round-trip to Delta 0"
    xw_cut = {"links": [x for x in xw["links"] if x["o365_id"] != 7]}  # People loses its link: one dropped hit
    pc = parity({"2": ["người"]}, {"2": {"person"}}, vt, mp, xw_cut)
    assert (pc["o365_hits_without_coco80"], pc["delta"]) == (1, 0), pc
    assert not fires(Fraction(2)) and fires(Fraction(2) + Fraction(1, 10 ** 12)) and fires(Fraction(-201, 100))
    rp = record(p)
    assert set(rp) == {"tier", "run", "delta_micro_points", "abs_delta_micro_gt_2", "delta_macro_points",
                       *DROPS}, "W1 whitelist"
    assert rp["abs_delta_micro_gt_2"] and rp["delta_micro_points"] == 7.778, rp  # 700/90 rounded to 3 dp (N3)
    assert rp["delta_macro_points"] == round(float(dm), 3) != float(dm), rp

    ids = list(range(1, N_IMAGES + 1))
    rb = lambda xs: json.dumps({"annotations": xs}).encode()  # noqa: E731
    anns = [{"image_id": i, "caption": "người"} for i in ids for k in range(6)] + [{"image_id": 1, "caption": ""}]
    gb = json.dumps({str(i): {"coco": ["person"]} for i in ids}).encode()
    r, g = load_inputs(ids, rb(anns), gb)
    assert len(r["1"]) == 6 and g["5"] == {"person"}, "all references per image, empty caption skipped"
    B.must_refuse(lambda: load_inputs(ids[:-1], rb(anns), gb), "listed ids")
    B.must_refuse(lambda: load_inputs(ids[:-1], rb([x for x in anns if x["image_id"] != N_IMAGES]), gb), "listed ids")
    B.must_refuse(lambda: load_inputs(ids, rb(anns[6:]), gb), "differ from the references")
    B.must_refuse(lambda: load_inputs(ids, rb(anns), json.dumps({"1": {"coco": []}}).encode()), "no instance gold")

    with tempfile.TemporaryDirectory() as td:  # CLI guards on a fixture root and a fixture LOG
        d = Path(td)
        root, log = d / "repo", d / "LOG.md"
        for rel in (*SRC, *R7, B.EX, REFS, GOLD):
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_bytes(rel.encode())
        (root / B.EX).write_bytes(json.dumps({"ids": {"coco": {"uitviic_test": ids}}}).encode())
        (root / REFS).write_bytes(rb(anns))
        (root / GOLD).write_bytes(gb)
        catp = d / CAT_NAME
        catp.write_bytes(cb(cats))
        rels = sorted({Path(m.__file__).resolve().relative_to(ROOT.resolve()).as_posix()
                       for m in list(sys.modules.values()) if getattr(m, "__file__", None)
                       and (ROOT / "rescap").resolve() in Path(m.__file__).resolve().parents})
        pins = [B.pin_cases(r, B.K.sha_file(ROOT / r))[0] for r in rels] + \
               [B.pin_cases(r, B.K.sha_file(root / r))[0] for r in (*SRC, *R7)]
        cat_pin = B.pin_cases(CAT_NAME, sha(cb(cats)), f"n={n}")[0]
        put = lambda *ls: log.write_text("\n".join(ls) + "\n")  # noqa: E731
        ld = (lambda: vt, lambda: syn)
        alp = d / ALIAS_NAME
        alias_doc = {"provenance": {"drafter": "fixture", "utc": B.T_UTC}, "aliases": [al("Golf Ball", "sports ball")],
                     "none": no("bowl", "cup")}
        alp.write_bytes(json.dumps(alias_doc).encode())
        al_pin = B.pin_cases(ALIAS_NAME, B.K.sha_file(alp))[0]
        bd = lambda o="out", a_=alp: cmd_build(NS(categories=catp, out_dir=d / o, alias=a_), log, root, n, ld)  # noqa
        for bad in [*B.pin_cases(CAT_NAME, sha(cb(cats)), f"n={n}")[1], B.pin_cases(CAT_NAME, sha(cb(cats)))[0]]:
            put(*pins, bad)
            B.must_refuse(bd, "R6-pinned")
        for i, _ in enumerate(pins):  # each matcher-v2 / R7 pin left out in turn
            put(*pins[:i], *pins[i + 1:], cat_pin)
            B.must_refuse(bd, "no LOG pin line")
        other = d / "other.json"
        other.write_bytes(cb(cats))
        put(*pins, cat_pin, B.pin_cases(other.name, sha(cb(cats)), f"n={n}")[0])
        B.must_refuse(lambda: cmd_build(NS(categories=other, out_dir=d / "o2", alias=None), log, root, n, ld),
                      "R6-pinned")
        put(*pins, cat_pin)
        os.environ["RESCAP_RAW_TONE"] = "1"
        B.must_refuse(bd, "RESCAP_RAW_TONE")
        del os.environ["RESCAP_RAW_TONE"]
        B.must_refuse(lambda: cmd_build(NS(categories=catp, out_dir=root / "x", alias=None), log, root, n, ld),
                      "tracked tree")
        B.must_refuse(lambda: bd("o_al"), "LOG-pinned")
        npv = d / "np"
        npv.mkdir()
        (npv / ALIAS_NAME).write_bytes(json.dumps({k: v for k, v in alias_doc.items() if k != "provenance"}).encode())
        put(*pins, cat_pin, B.pin_cases(ALIAS_NAME, B.K.sha_file(npv / ALIAS_NAME))[0])
        B.must_refuse(lambda: bd("o_np", npv / ALIAS_NAME), "provenance")
        put(*pins, cat_pin, al_pin)
        B.must_refuse(lambda: bd("o_none", None), "no link and no 'none'")  # gaps and no alias file: mandatory
        assert bd() == 0 and sorted(p.name for p in (d / "out").iterdir()) == [XW_NAME, MAP_NAME]
        assert exists_error(bd), "existing --out-dir reused"
        mpp = d / "out" / MAP_NAME
        msha, xsha = B.K.sha_file(mpp), B.K.sha_file(d / "out" / XW_NAME)
        m_doc = json.loads(mpp.read_bytes())
        assert m_doc["r7"] == {r: B.K.sha_file(root / r) for r in R7} and m_doc["categories_sha256"] == sha(cb(cats))
        assert m_doc["alias_sha256"] == B.K.sha_file(alp), m_doc["alias_sha256"]
        freeze = B.pin_cases(MAP_NAME, msha, XW_NAME, xsha, sha(cb(cats)), *m_doc["r7"].values(), m_doc["alias_sha256"])
        here = str((d / "out").resolve())
        st = lambda r_sha: f"{B.T_UTC} OPS-9-parity1-start: {msha} {xsha} {r_sha} {sha(gb)} {B.EX_SHA} {here}"  # noqa
        start = st(sha(rb(anns)))
        pr = lambda: cmd_parity(NS(map=mpp), log, root, lambda: vt)  # noqa: E731
        ex_real = (root / B.EX).read_bytes()
        B.must_refuse(lambda: (put(*pins, cat_pin, freeze[0], start), pr()), "exclusion.json")  # fixture != pin
        # the fixture exclusion.json cannot carry the real EX_SHA, so the success path patches B.EX_SHA locally
        real_ex = B.EX_SHA
        B.EX_SHA = sha(ex_real)
        try:
            start = st(sha(rb(anns)))
            for bad in freeze[1]:
                put(*pins, cat_pin, bad, start)
                B.must_refuse(pr, "freeze pin")
            put(*pins, cat_pin, B.pin_cases(MAP_NAME, msha, XW_NAME, xsha, sha(cb(cats)), m_doc["alias_sha256"])[0],
                start)
            B.must_refuse(pr, "freeze pin")  # R7 shas missing on the freeze line
            put(*pins, cat_pin, B.pin_cases(MAP_NAME, msha, XW_NAME, xsha, sha(cb(cats)), *m_doc["r7"].values())[0],
                start)
            B.must_refuse(pr, "freeze pin")  # alias sha missing on the freeze line
            put(*pins, cat_pin, freeze[0])
            B.must_refuse(pr, "parity1-start")
            put(*pins, cat_pin, start, freeze[0])
            B.must_refuse(pr, "parity1-start")  # start before the freeze pin
            put(*pins, cat_pin, freeze[0], start, start)
            B.must_refuse(pr, "parity1-start")
            for bad in (start.replace(sha(gb), "0" * 64), start.replace(sha(gb), sha(gb) + "0"), f"| {start}"):
                put(*pins, cat_pin, freeze[0], bad)
                B.must_refuse(pr, "parity1-start")
            (root / SRC[2]).write_bytes(b"re-pinned but not what map v1 was built with")
            put(*pins, cat_pin, freeze[0], start, B.pin_cases(SRC[2], B.K.sha_file(root / SRC[2]))[0])
            B.must_refuse(pr, "differ from those")
            (root / SRC[2]).write_bytes(SRC[2].encode())
            (d / "out" / "other.json").write_bytes(mpp.read_bytes())
            put(*pins, cat_pin, freeze[0], start)
            B.must_refuse(lambda: cmd_parity(NS(map=d / "out" / "other.json"), log, root, lambda: vt), "belong")
            put(*pins, cat_pin, freeze[0], start, f"{B.T_UTC} OPS-9-parity1-done: {msha}")
            B.must_refuse(pr, "already done")
            put(*pins, cat_pin, freeze[0], start)
            os.environ["RESCAP_RAW_TONE"] = "0"
            B.must_refuse(pr, "RESCAP_RAW_TONE")
            del os.environ["RESCAP_RAW_TONE"]
            (root / SRC[1]).write_bytes(b"changed")
            B.must_refuse(pr, "no LOG pin line")
            (root / SRC[1]).write_bytes(SRC[1].encode())
            for f in (MAP_NAME, XW_NAME):  # a copy of the frozen map in another directory: no start line names it
                (d / "out3").mkdir(exist_ok=True)
                (d / "out3" / f).write_bytes((d / "out" / f).read_bytes())
            B.must_refuse(lambda: cmd_parity(NS(map=d / "out3" / MAP_NAME), log, root, lambda: vt), "parity1-start")
            short = rb([x for x in anns if x["image_id"] != N_IMAGES])  # input REFUSED: before the once-only file
            (root / REFS).write_bytes(short)
            put(*pins, cat_pin, freeze[0], st(sha(short)))
            B.must_refuse(pr, "differ from the references")
            assert not (d / "out" / OUT_NAME).exists(), "an input refusal left parity1.json behind"
            (root / REFS).write_bytes(rb(anns))
            put(*pins, cat_pin, freeze[0], start)
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                assert pr() == 0
            out = (d / "out" / OUT_NAME).read_bytes()
            assert buf.getvalue().encode() == out and set(json.loads(out)) == set(rp), "stdout = file = whitelist"
            assert exists_error(pr), "parity run 1 ran twice"
        finally:
            B.EX_SHA = real_ex
        bad_map = d / "out2"
        bad_map.mkdir()
        (bad_map / MAP_NAME).write_bytes(mpp.read_bytes())
        (bad_map / XW_NAME).write_bytes(xw_b)
        B.must_refuse(lambda: cmd_parity(NS(map=bad_map / MAP_NAME), log, root, lambda: vt), "belong together")
    print(json.dumps({"tier": B.LABEL, "selftest": "map_v1 ok",
                      "checks": ["crosswalk", "alias-add-only", "map-order-first-wins", "order-free-bytes",
                                 "no-class-names", "parity-hand-value", "round-trip", "boundary", "W1-whitelist",
                                 "all-refs-ids", "build-pins", "R3-raw-tone", "out-dir", "freeze-pin", "start-line",
                                 "run-dir", "inputs-before-lock", "done-line", "once-only", "strike-route",
                                 "mandatory-alias", "alias-provenance", "freeze-alias", "3dp-rounding"]}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    b = sp.add_parser("build")
    b.add_argument("--categories", type=Path, required=True, help=f"{CAT_NAME} (R6 pin)")
    b.add_argument("--out-dir", type=Path, required=True, help="new directory, git-excluded")
    b.add_argument("--alias", type=Path, help=f"{ALIAS_NAME} (LOG-pinned; instrument links)")
    sp.add_parser("parity").add_argument("--map", type=Path, required=True, help=f"<build dir>/{MAP_NAME}")
    a = ap.parse_args()
    return {"selftest": lambda: selftest(), "build": lambda: cmd_build(a), "parity": lambda: cmd_parity(a)}[a.cmd]()


if __name__ == "__main__":
    sys.exit(main())
