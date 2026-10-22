#!/usr/bin/env python3
"""Paper E stage 1 (EXPLORATORY / DEV): minimal pairs from the XM3600 references of E-dev-A, with OIV7 human-verified
image labels deciding which object is present or absent, and the judge items. Design DESIGN.md §3.

  python scripts/e_stage1/pairs.py --selftest                                                    CPU, no data
  python scripts/e_stage1/pairs.py build --split S --out-dir DIR     CPU, LOCAL only: reads references and OIV7 labels
  python scripts/e_stage1/pairs.py items --split S --captions DIR/captions.jsonl [--preds P ...] --out-dir DIR   CPU
`build` writes pairs.jsonl (ids, types, classes: no text) and captions.jsonl (the E-dev-A base and perturbed texts:
never committed; the judge on M3 needs them). `items` reads captions.jsonl and zero-shot preds only; it runs
locally (CC-081): it adds the model captions and writes items.jsonl, one (image, class) per row, for M3.
Every perturbed caption is kept only if the matcher finds exactly the expected class set in it.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e_lists as L  # noqa: E402  pins, refusal (puts scripts/ and scripts/c_stage1 on the path)
import guard  # noqa: E402  C's matcher wrappers (classes, key), END and delete(), reused unchanged
import xm3600_oiv7 as X  # noqa: E402  Paper A's OIV7 label tooling: resolve_map, statuses
from rescap.chair import _ancestors, objects_in  # noqa: E402  matcher v2
from rescap.vi.lexicon import NOUN_CLASSIFIER  # noqa: E402

DS = "e_dev_a"
COCO80_VI = L.ROOT / "data/coco_probe/coco80_vi.json"
# type: (languages, the caption a hallucination scorer must rank higher; None = the difference is reported only)
TYPES = {"swap": (("vi", "en"), "base"), "add_absent": (("vi", "en"), "base"), "add_present": (("vi", "en"), None),
         "delete": (("vi",), None), "ool_absent": (("vi",), "base"), "pad": (("vi", "en"), "base"),
         "pad_control": (("vi", "en"), None)}
IRREGULAR = {"man": "men", "woman": "women", "child": "children", "person": "people"}


def key(o: str) -> str:
    return guard.key(o)


# ------------------------------------------------------------------------------------------------ matchers
def english_map() -> dict[str, str]:
    """S2's English noun phrase of every lexicon class (the per-object judge asks about these)."""
    return guard.s2()["verifier_protocol"]["english_class_map"]


def head(np: str) -> str:
    w = np.split(" ", 1)
    return w[1] if len(w) == 2 and w[0] in ("a", "an", "the", "some") else np


def plural(h: str) -> str:
    *rest, last = h.split()
    p = IRREGULAR.get(last) or (last + "es" if last.endswith(("s", "sh", "ch", "x")) else last + "s")
    return " ".join([*rest, p])


def en_forms(classes, en_np: dict[str, str]) -> list[tuple[str, str]]:
    """[(surface, class)], longest first, for the classes whose English head noun names one class key only.
    ponytail: head noun + regular/4 irregular plurals, no synonyms; English is secondary in stage 1 (DESIGN §3.5)."""
    by_head: dict[str, set[str]] = {}
    for c in classes:
        by_head.setdefault(head(en_np[c]), set()).add(c)
    out = []
    for h, cs in by_head.items():
        if len({key(c) for c in cs}) == 1:
            c = min(cs)
            out += [(h, c), (plural(h), c)]
    return sorted(out, key=lambda x: (-len(x[0]), x[0]))


def en_classes(text: str, forms: list[tuple[str, str]]) -> list[str]:
    t, taken, found = text.lower(), [], []
    for s, c in forms:
        for m in re.finditer(rf"(?<!\w){re.escape(s)}(?!\w)", t):
            if not any(m.start() < b and a < m.end() for a, b in taken):
                taken.append((m.start(), m.end()))
                found.append((m.start(), c))
    return list(dict.fromkeys(c for _p, c in sorted(found)))


def mentions(text: str, lang: str, forms) -> list[str]:
    return guard.classes(text) if lang == "vi" else en_classes(text, forms)


def related(c: str, mentioned) -> bool:
    return any(key(c) == key(m) or m in _ancestors(c) or c in _ancestors(m) for m in mentioned)


# ------------------------------------------------------------------------------------------------ perturbations
def surface(c: str, lang: str, en_np: dict) -> str:
    if lang == "en":
        return head(en_np[c])
    clf = NOUN_CLASSIFIER.get(c)
    return c if not clf or c.split()[0] == clf else f"{clf} {c}"


def phrase(c: str, lang: str, en_np: dict) -> str:
    return en_np[c] if lang == "en" else f"một {surface(c, lang, en_np)}"


def add(text: str, phrases: list[str], lang: str) -> str:
    body = text.strip()
    m = guard.END.search(body)
    end, body = (m.group(), body[:m.start()]) if m else ("", body)
    j = " và " if lang == "vi" else " and "
    return body + "".join(j + p for p in phrases) + end


def swap(text: str, c: str, a: str, lang: str, en_np: dict) -> str | None:
    hits = list(re.finditer(rf"(?<!\w){re.escape(surface(c, lang, en_np))}(?!\w)", text, re.I))
    if len(hits) != 1:
        return None
    h = hits[0]
    return text[:h.start()] + surface(a, lang, en_np) + text[h.end():]


def delete(text: str, c: str) -> str | None:
    out, how = guard.delete(text, {c}, "")
    return out if how == "deleted" else None


def seed(*parts: str) -> random.Random:
    return random.Random(int(hashlib.sha256("|".join(("paperE", "pair", *parts)).encode()).hexdigest()[:8], 16))


def construct(typ: str, base: str, lang: str, ctx: dict, rng: random.Random):
    """(text, added, removed) or None. ctx: M (mentions), pm (present mentioned), A/P (absent/present classes not
    mentioned and not related to a mention), ool (absent out-of-lexicon terms), en_np."""
    M, pm, A, P, en_np = ctx["M"], ctx["pm"], ctx["A"], ctx["P"], ctx["en_np"]
    pick = lambda xs: rng.choice(xs) if xs else None  # noqa: E731
    if typ == "swap" and pm and A:
        c, a = pick(pm), pick(A)
        return swap(base, c, a, lang, en_np), [a], [c]
    if typ in ("add_absent", "add_present") and (x := pick(A if typ == "add_absent" else P)):
        return add(base, [phrase(x, lang, en_np)], lang), [x], []
    if typ == "delete" and pm:
        c = pick(pm)
        return delete(base, c), [], [c]
    if typ == "ool_absent" and (t := pick(ctx["ool"])):
        return add(base, [f"một {t}"], lang), [], []
    if typ == "pad" and (p := pick(P)) and (a := pick([x for x in A if not related(x, [p])])):
        return add(base, [phrase(p, lang, en_np), phrase(a, lang, en_np)], lang), [p, a], []
    if typ == "pad_control" and (p := pick(P)) and (q := pick([x for x in P if not related(x, [p])])):
        return add(base, [phrase(p, lang, en_np), phrase(q, lang, en_np)], lang), [p, q], []
    return None


def build_pairs(refs: dict, st: dict, ool: dict, en_np: dict, forms) -> tuple[list, dict, Counter]:
    """refs {image: {lang: [caption, ...]}}, st {image: {class: present|absent}}, ool {image: [absent terms]}."""
    pairs, caps, skipped = [], {}, Counter()
    for img in sorted(refs):
        if img not in st:
            continue
        present = sorted(c for c, s in st[img].items() if s == "present")
        absent = sorted(c for c, s in st[img].items() if s == "absent")
        for lang in ("vi", "en"):
            usable = set(st[img]) if lang == "vi" else {c for _s, c in forms}
            for r, base in enumerate(refs[img][lang][:2]):
                M = mentions(base, lang, forms)
                if not M:
                    skipped[f"{lang}:no_mention"] += 1
                    continue
                free = lambda xs: [c for c in xs if c in usable and not related(c, M)]  # noqa: E731
                ctx = {"M": M, "pm": [m for m in M if st[img].get(m) == "present"], "A": free(absent),
                       "P": free(present), "ool": ool.get(img, []), "en_np": en_np}
                bid = f"{lang}|{img}|r{r}"
                caps[bid] = {"cid": bid, "image_id": img, "lang": lang, "source": "ref", "text": base, "classes": M}
                for typ, (langs, winner) in TYPES.items():
                    if lang not in langs:
                        continue
                    got = construct(typ, base, lang, ctx, seed(lang, img, str(r), typ))
                    if got is None or got[0] is None:
                        skipped[f"{lang}:{typ}"] += 1
                        continue
                    text, added, removed = got
                    want = ({key(m) for m in M} - {key(c) for c in removed}) | {key(c) for c in added}
                    got_m = mentions(text, lang, forms)
                    if {key(m) for m in got_m} != want:
                        skipped[f"{lang}:{typ}:matcher"] += 1
                        continue
                    pid = f"{bid}|{typ}"
                    caps[pid] = {"cid": pid, "image_id": img, "lang": lang, "source": typ, "text": text,
                                 "classes": got_m}
                    pairs.append({"pair_id": pid, "image_id": img, "lang": lang, "ref": r, "type": typ, "base": bid,
                                  "pert": pid, "added": added, "removed": removed, "winner": winner})
    return pairs, caps, skipped


# ------------------------------------------------------------------------------------------------ build (CPU, local)
def ool_terms(desc_csv: Path) -> list[tuple[str, str]]:
    """[(Vietnamese term the matcher misses, OIV7 MID)] from coco80_vi.json; the COCO class name must be exactly one
    OIV7 display name (case-insensitive). Tooling, as coco80_vi.json is: it creates no label."""
    mids: dict[str, list[str]] = {}
    with open(desc_csv, encoding="utf-8") as f:
        for mid, name in csv.reader(f):
            mids.setdefault(name.lower(), []).append(mid)
    c80 = json.loads(COCO80_VI.read_text(encoding="utf-8"))
    return [(t, mids[k.lower()][0]) for k, terms in c80.items() if not k.startswith("_")
            and len(mids.get(k.lower(), [])) == 1 for t in terms if not t.startswith("_") and not objects_in(t)]


def references(data: Path, ids: set[str]) -> dict[str, dict[str, list[str]]]:
    out: dict[str, dict[str, list[str]]] = {i: {"vi": [], "en": []} for i in ids}
    for lang, name in (("vi", "xm3600"), ("en", "xm3600_en")):
        for a in json.loads((data / f"datasets/{name}/full_data.json").read_text(encoding="utf-8"))["annotations"]:
            if str(a["image_id"]) in ids:
                out[str(a["image_id"])][lang].append(" ".join(a["caption"].split()))
    return out


def cmd_build(a) -> None:
    L.local_only("build")
    split = L.load_split(a.split)
    ids = set(L.check_images([r[0] for r in split["sets"][DS]], split))
    data = L.C.lb.DATA
    desc = data / "datasets/xm3600/oiv7/oidv7-class-descriptions.csv"
    labels = {k: v for k, v in json.loads(X.LABELS.read_text(encoding="utf-8")).items() if k in ids}
    vmap = X.resolve_map(desc)
    st = X.statuses(vmap, labels)
    ool = {i: sorted({t for t, mid in ool_terms(desc) if mid in labels[i]["neg"] and mid not in labels[i]["pos"]})
           for i in labels}
    en_np = english_map()
    pairs, caps, skipped = build_pairs(references(data, ids), st, ool, en_np, en_forms(set(vmap), en_np))
    out = Path(a.out_dir)
    write_jsonl(out / "pairs.jsonl", pairs)
    write_jsonl(out / "captions.jsonl", list(caps.values()))
    counts = {"labelled_images": len(st), "pairs": dict(Counter(f"{p['lang']}:{p['type']}" for p in pairs)),
              "skipped": dict(skipped), "pairs_sha256": L.sha256_file(out / "pairs.jsonl")}
    (out / "pairs.counts.json").write_text(json.dumps(counts, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(counts))


def st_classes(st: dict) -> set[str]:
    return {c for s in st.values() for c in s}


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x]


# ------------------------------------------------------------------------------------------------ items (CPU, M3-safe)
def items(caps: list[dict]) -> list[dict]:
    return [{"dataset": DS, "image_id": i, "class": c} for i, c in sorted({(r["image_id"], c) for r in caps
                                                                           for c in r["classes"]})]


def cmd_items(a) -> None:
    L.local_only("items")
    split = L.load_split(a.split)
    caps = read_jsonl(a.captions)
    for p in a.preds or []:
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        if d.get("e_schema") != "vsps.e_stage1.v1":
            raise SystemExit(f"{p}: not an E stage-1 zero-shot decode")
        caps += [{"cid": f"vi|{i}|vlm:{d['model']}", "image_id": i, "lang": "vi", "source": f"vlm:{d['model']}",
                  "text": t, "classes": guard.classes(t)} for i, t in sorted(d["predictions"].items())]
    L.check_images({r["image_id"] for r in caps}, split)
    out = Path(a.out_dir)
    write_jsonl(out / "captions_all.jsonl", caps)
    rows = items(caps)
    write_jsonl(out / "items.jsonl", rows)
    print(f"{len(caps)} captions, {len(rows)} (image, class) items")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    en_np = english_map()
    assert {"chó", "mèo", "ghế", "bàn"} <= set(en_np)
    forms = en_forms({"chó", "mèo", "ghế", "người", "đàn ông", "phụ nữ"}, en_np)
    # strings written for this test: placeholder syllables plus the object words the asserts need
    vi = "chuỗi thử nghiệm số một gồm các âm tiết giả và một con chó."
    en = "test string number one of placeholder words with a dog."
    assert mentions(vi, "vi", forms) == ["chó"] and mentions(en, "en", forms) == ["chó"]
    assert en_classes("placeholder men and two dogs", forms) == ["đàn ông", "chó"], "plurals, longest match first"
    assert en_classes("placeholder woman", forms) == ["phụ nữ"], "'man' inside 'woman' is not a man"
    assert add(vi, ["một cái ghế"], "vi") == vi[:-1] + " và một cái ghế."
    assert swap(vi, "chó", "mèo", "vi", en_np) == vi.replace("con chó", "con mèo")
    assert swap(en, "chó", "mèo", "en", en_np) == en.replace("dog", "cat")
    assert swap("con chó và con chó", "chó", "mèo", "vi", en_np) is None, "an ambiguous surface is skipped"
    assert related("đàn ông", ["người"]) and not related("ghế", ["chó"])
    st = {"img1": {"chó": "present", "ghế": "present", "mèo": "absent", "bàn": "absent", "người": "absent"}}
    refs = {"img1": {"vi": [vi, "chuỗi giả số hai"], "en": [en]}}
    pairs, caps, skipped = build_pairs(refs, st, {"img1": ["con cừu"]}, en_np, forms)
    types = Counter(f"{p['lang']}:{p['type']}" for p in pairs)
    assert types == Counter({f"vi:{t}": 1 for t in TYPES if t != "pad_control"} | {
        f"en:{t}": 1 for t in ("swap", "add_absent", "add_present", "pad")}), types
    assert skipped == Counter({"vi:no_mention": 1, "vi:pad_control": 1, "en:pad_control": 1}), skipped
    assert caps["vi|img1|r0|add_present"]["classes"] == ["chó", "ghế"]
    assert caps["vi|img1|r0|ool_absent"]["classes"] == ["chó"], "the out-of-lexicon term is not seen by the matcher"
    assert caps["vi|img1|r0|delete"]["classes"] == [] and len(caps["vi|img1|r0|swap"]["classes"]) == 1
    sw = next(p for p in pairs if p["pair_id"] == "vi|img1|r0|swap")
    assert caps["vi|img1|r0|swap"]["classes"] == sw["added"] and st["img1"][sw["added"][0]] == "absent"
    assert (pairs, caps) == build_pairs(refs, st, {"img1": ["con cừu"]}, en_np, forms)[:2], "deterministic"
    assert delete("chuỗi giả số ba gồm hai con chó và một cái bàn", "bàn") == "chuỗi giả số ba gồm hai con chó"
    got = {r["class"] for r in items(list(caps.values()))}
    assert {"chó", "ghế", "mèo"} <= got <= set(st["img1"]), got
    assert all(c in en_np for c in st_classes(st)), "every judged class has S2's English noun phrase"
    print("selftest ok: vi/en matchers, swap/add/delete/out-of-lexicon/pad pairs, matcher validation, determinism, "
          "items")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("build")
    p.add_argument("--split", type=Path, required=True)
    p.add_argument("--out-dir", required=True)
    p = sub.add_parser("items")
    p.add_argument("--split", type=Path, required=True)
    p.add_argument("--captions", type=Path, required=True)
    p.add_argument("--preds", nargs="*", type=Path)
    p.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    {"build": cmd_build, "items": cmd_items}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
