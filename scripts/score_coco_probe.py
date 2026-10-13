#!/usr/bin/env python
""" (research log) — standard CHAIR scoring on COCO-2014 for the cross-lingual probe.

    python scripts/score_coco_probe.py \\
        --preds-dir ~/ncs-data/coco_probe_out \\
        --out data/results/coco_probe_scores.json

PROTOCOL FROZEN BEFORE SEEING RESULTS (committed before the probe finished — that
is the entire value of this file):
1. Object universe = EXACTLY the 80 COCO classes (Rohrbach 2018). Objects outside
   the 80 classes are not counted — on the mention side or the gold side.
2. Gold(image) = classes in instances_val2014 ∪ classes mentioned in the 5
   Karpathy reference captions (EN matching via Rohrbach's original synonyms.txt,
   + simple s/es plurals).
3. Object detection in the VIETNAMESE caption: the coco80_vi.json lexicon
   (committed beforehand), longest-phrase-first matching, boundaries are
   non-letter characters; `_rui_ro` notes in the lexicon are skipped when matching.
   Fixed 2026-10-12 (it only ever removed classes): a matched phrase is consumed, so
   a term inside or overlapping a more specific one adds no second class (VI `ô tô`
   gave bowl too, `ngựa vằn` horse, `gấu bông` bear; EN `hot dog` gave dog), and
   "longest" ignores a leading classifier (`chiếc ô tô` is a car, not an umbrella).
   2026-10-12: every score uses matcher v2 (VI_LEXICON): LEX_V2's rewrites of the lowercased caption, then
   this lexicon; v1 = the lexicon alone. The version is written into the output.
   2026-10-13 (D10 (iv)(a)): tone-mark placement on open oa/oe/uy clusters is normalised via
   `rescap.chair.norm_tone` in both `load_vi_terms` and `vi_classes` (`tàu hỏa` == `tàu hoả`).
4. Metrics per (system × mode): classes mentioned/caption · CHAIR_i (invented
   classes / mentioned classes, pooled over the set) · CHAIR_s (% captions with
   ≥1 invented class) · absolute invented objects/caption (mean distinct
   invented classes).
5. Merge both shards in full; report every missing image by name; no post-hoc
   sample exclusion.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rescap.chair import norm_tone  # noqa: E402

NCS_DATA = Path(os.environ.get("NCS_DATA", Path.home() / "ncs-data"))
PROBE_DATA = Path(__file__).resolve().parents[1] / "data" / "coco_probe"
ANN = NCS_DATA / "datasets" / "coco_probe" / "annotations"
KARPATHY = NCS_DATA / "datasets" / "karpathy" / "dataset_coco.json"

_LETTER = r"a-zA-ZÀ-ỹ"


def load_synonyms() -> dict[str, str]:
    """EN synonym → COCO class name, with simple plurals."""
    mapping: dict[str, str] = {}
    for line in (PROBE_DATA / "chair_synonyms.txt").read_text().splitlines():
        parts = [p.strip().lower() for p in line.split(",") if p.strip()]
        if not parts:
            continue
        cls = parts[0]
        for p in parts:
            mapping[p] = cls
            mapping[p + "s"] = cls
            mapping[p + "es"] = cls
    return mapping


def load_vi_terms(*, raw_tone: bool = False) -> list[tuple[str, str]]:
    """[(VI phrase, COCO class)], most specific first: longest without a leading classifier
    (`ngựa vằn` before `con ngựa`, `ô tô` before `chiếc ô`), then longest; skip _rui_ro notes."""
    from rescap.vi.lexicon import CLASSIFIERS

    def head(term: str) -> str:
        first, _, rest = term.partition(" ")
        return rest if rest and first in CLASSIFIERS else term

    d = json.loads((PROBE_DATA / "coco80_vi.json").read_text(encoding="utf-8"))
    pairs = []
    for cls, terms in d.items():
        if cls.startswith("_"):
            continue
        for t in terms:
            if isinstance(t, str) and not t.startswith("_rui_ro"):
                pairs.append((norm_tone(t.lower(), raw_tone=raw_tone), cls))
    return sorted(pairs, key=lambda x: (-len(head(x[0])), -len(x[0])))


#: COCO-80 Vietnamese matcher v2: regex rewrites of the lowercased caption before vi_classes, frozen 2026-10-12 for
#: gate G3' (two_gold_audit.py, V3): non-object spans consumed (bóng bàn = table tennis, ghi bàn / bàn thắng = score
#: a goal), typos and misreads, sport-role person nouns v1 misses. Do not extend it in place: person nouns change
#: G3' through consensus/fusion target selection even on family nosel (tested 2026-10-12, R5_02 appendix).
LEX_V2 = [(r"\b(bóng|ghi) bàn\b", r"\1 _"), (r"\bbàn thắng\b", "_ thắng"), (r"\bgấu bống\b", "gấu bông"),
          (r"\bchó bông\b", "gấu bông"), (r"\bmàn hình máy tính\b", "màn hình tivi"),
          (r"\b(cầu thủ|vận động viên|vđv|thủ môn|trọng tài|khán giả|người chơi)\b", "người")]
#: the matcher of every Vietnamese COCO-80 score (written into its output); build_gold_sft.py --objects coco80 builds
#: training targets with v1, so the training data of the queued UIT-ViIC jobs stays byte-identical
VI_LEXICON = "v2"


def vi_objects(caption: str, vi_terms, lexicon: str = VI_LEXICON, *, raw_tone: bool = False) -> set[str]:
    """COCO-80 classes a Vietnamese caption names under lexicon v2 (LEX_V2 rewrites, then vi_classes) or v1."""
    if lexicon not in ("v1", "v2"):
        raise ValueError(f"unknown COCO-80 Vietnamese lexicon {lexicon!r}")
    text = caption.lower()
    for pattern, repl in LEX_V2 if lexicon == "v2" else ():
        text = re.sub(pattern, repl, text)
    return vi_classes(text, vi_terms, raw_tone=raw_tone)


def vi_classes(caption: str, vi_terms, *, raw_tone: bool = False) -> set[str]:
    """Classes named in a VI caption, phrases tried in load_vi_terms' order and each matched span
    consumed: `ô tô` (car) no longer also yields `tô` (bowl), nor `ghế dài` (bench) `ghế` (chair)."""
    text = " " + norm_tone(caption.lower(), raw_tone=raw_tone) + " "
    found: set[str] = set()
    for term, cls in vi_terms:
        spans = [m.span() for m in re.finditer(re.escape(term), text)
                 if not re.match(f"[{_LETTER}]", text[m.start() - 1]) and not re.match(f"[{_LETTER}]", text[m.end()])]
        for a, b in spans:
            text = text[:a] + "\0" * (b - a) + text[b:]
        if spans:
            found.add(cls)
    return found


def en_classes(caption: str, syn: dict[str, str]) -> set[str]:
    text = " " + re.sub(f"[^{_LETTER}]", " ", caption.lower()) + " "
    found: set[str] = set()
    # multi-word phrases first, consumed (Rohrbach's double words): `hot dog` does not also yield `dog`
    for phrase, cls in syn.items():
        if " " in phrase and f" {phrase} " in text:
            found.add(cls)
            text = re.sub(rf"(?<= ){re.escape(phrase)}(?= )", " ", text)
    for tok in text.split():
        if tok in syn:
            found.add(syn[tok])
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--preds-dir", required=False)
    ap.add_argument("--manifest", default=str(PROBE_DATA / "manifest.json"))
    ap.add_argument("--out", default="data/results/coco_probe_scores.json")
    ap.add_argument("--raw-tone", action="store_true")
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args()
    if args.self_check:
        print("score_coco_probe _check ok")
        return 0
    if not args.preds_dir:
        ap.error("--preds-dir is required")

    syn = load_synonyms()
    vi_terms = load_vi_terms(raw_tone=args.raw_tone)
    man = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    want = {i["cocoid"] for i in man["images"]}

    # gold 1 — real instances
    inst = json.loads((ANN / "instances_val2014.json").read_text())
    cat_name = {c["id"]: c["name"] for c in inst["categories"]}
    gold_inst: dict[int, set[str]] = defaultdict(set)
    for a in inst["annotations"]:
        if a["image_id"] in want:
            gold_inst[a["image_id"]].add(cat_name[a["category_id"]])
    # gold 2 — Karpathy reference captions
    kar = json.loads(KARPATHY.read_text())
    gold_ref: dict[int, set[str]] = defaultdict(set)
    for img in kar["images"]:
        if img["cocoid"] in want:
            for s in img["sentences"]:
                gold_ref[img["cocoid"]] |= en_classes(s["raw"], syn)
    gold = {i: gold_inst[i] | gold_ref[i] for i in want}

    preds_dir = Path(args.preds_dir).expanduser()
    results = {}
    for system in ("zeroshot", "distill"):
        for mode in ("short", "detailed"):
            rows: dict[int, str] = {}
            for f in sorted(preds_dir.glob(f"{system}-{mode}.shard*.jsonl")):
                for line in f.read_text(encoding="utf-8").splitlines():
                    r = json.loads(line)
                    rows[r["cocoid"]] = r["caption"]
            missing = sorted(want - set(rows))
            n = len(rows)
            if not n:
                continue
            men_total = hal_total = hal_caps = 0
            hal_per_cap = []
            for cid, cap in rows.items():
                mentioned = vi_objects(cap, vi_terms, raw_tone=args.raw_tone)
                halluc = mentioned - gold[cid]
                men_total += len(mentioned)
                hal_total += len(halluc)
                hal_caps += bool(halluc)
                hal_per_cap.append(len(halluc))
            results[f"{system}-{mode}"] = {
                "n_captions": n, "n_missing": len(missing),
                "missing_sample": missing[:5],
                "mentions_per_caption": round(men_total / n, 3),
                "chair_i": round(hal_total / max(men_total, 1), 4),
                "chair_s": round(hal_caps / n, 4),
                "abs_halluc_per_caption": round(sum(hal_per_cap) / n, 3),
            }
            r = results[f"{system}-{mode}"]
            print(f"{system:9s} {mode:9s}: mentions {r['mentions_per_caption']:.2f}/cap · "
                  f"CHAIR_i {100*r['chair_i']:.1f}% · CHAIR_s {100*r['chair_s']:.1f}% · "
                  f"absolute invented {r['abs_halluc_per_caption']:.2f}/cap"
                  + (f"  (MISSING {r['n_missing']} images)" if r["n_missing"] else ""))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "protocol": " (research log) frozen before seeing results; committed before the probe finished",
        "gold": "instances_val2014 ∪ ref-caption (synonyms.txt Rohrbach)", "vi_lexicon": VI_LEXICON,
        "results": results,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    return 0


def _check() -> None:
    from rescap.chair import _TONE, _TONE_RE

    terms = load_vi_terms()
    assert vi_classes("Một chiếc ô tô đỗ trên đường.", terms) == {"car"}
    assert vi_classes("Hai người ngồi trên ghế dài.", terms) == {"person", "bench"}
    assert vi_classes("Cậu bé cầm ván trượt tuyết.", terms) == {"person", "snowboard"}
    # overlaps: a leading classifier makes a term longer, not more specific
    assert vi_classes("Con ngựa vằn bên chiếc ô tô.", terms) == {"zebra", "car"}
    assert vi_classes("Con gấu bông trên cái bàn phím.", terms) == {"teddy bear", "keyboard"}
    # every occurrence is consumed; a standalone shorter term still counts
    assert vi_classes("ô tô, ô tô và một cái tô", terms) == {"car", "bowl"}
    # v2: non-object spans consumed, person nouns v1 misses; v1 is the lexicon alone
    assert vi_objects("Cầu thủ đang ghi bàn", terms) == {"person"}
    assert vi_objects("Cầu thủ đang ghi bàn", terms, "v1") == {"dining table"}
    assert vi_objects("Khán giả xem bóng bàn", terms) == {"person"} and vi_objects("bóng bàn", terms, "v1") == {"dining table"}
    assert vi_objects("một tòa nhà cao", terms) == vi_objects("một toà nhà cao", terms)
    assert vi_objects("tàu hỏa", terms) == vi_objects("tàu hoả", terms) == {"train"}
    assert vi_objects("vòi cứu hỏa", terms) == vi_objects("vòi cứu hoả", terms) == {"fire hydrant"}
    inv = {v: u for u, v in _TONE.items()}
    old_re = re.compile("(" + "|".join(inv) + r")(?![^\W\d_])")
    raw = json.loads((PROBE_DATA / "coco80_vi.json").read_text(encoding="utf-8"))
    clusters = [(t.lower(), cls) for cls, ts in raw.items() if not cls.startswith("_")
                for t in ts if isinstance(t, str) and not t.startswith("_rui_ro")
                and (old_re.search(t.lower()) or _TONE_RE.search(t.lower()))]
    assert len(clusters) == 7, clusters
    for t, cls in clusters:
        old_t = old_re.sub(lambda m: inv[m.group(1)], t)
        new_t = norm_tone(t)
        assert old_t != new_t
        for lex in ("v1", "v2"):
            s_old = vi_objects(old_t, terms, lex)
            s_new = vi_objects(new_t, terms, lex)
            assert s_old == s_new and cls in s_new, (t, cls, lex, s_old, s_new)
    syn = load_synonyms()
    assert en_classes("A teddy bear and hot dogs on a motor bike.", syn) == {"teddy bear", "hot dog", "motorcycle"}
    assert en_classes("A dog eats a hot dog.", syn) == {"dog", "hot dog"}


if __name__ == "__main__":
    _check()
    sys.exit(main())

