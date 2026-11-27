"""COCO-80 entity propositions of a Vietnamese caption, in order of first mention (prereg §3.2, §5 CMP).

Matcher = score_coco_probe.py matcher v2 (LEX_V2 rewrites, longest-phrase-first span consumption, tone-normalised),
read from the tracked repo file data/coco_probe/coco80_vi.json through its sha pin (926e0857). The only addition is the start offset of
each class's first consumed span, which CMP needs; the class SET always equals score_coco_probe.vi_objects (checked
at runtime and in the tests).
"""
from __future__ import annotations

import json
import re

from . import COCO80_VI, COCO80_VI_SHA, repo, sha_file

_LETTER = r"a-zA-ZÀ-ỹ"  # score_coco_probe._LETTER
_TERMS: list | None = None


def load_terms() -> list[tuple[str, str]]:
    """score_coco_probe.load_vi_terms() on the pinned repo file: [(phrase, class)], most specific first."""
    global _TERMS
    if _TERMS is None:
        repo()
        from rescap.chair import norm_tone
        from rescap.vi.lexicon import CLASSIFIERS

        if sha_file(COCO80_VI) != COCO80_VI_SHA:
            raise SystemExit("FAULT coco80_vi.json sha")

        def head(term: str) -> str:
            first, _, rest = term.partition(" ")
            return rest if rest and first in CLASSIFIERS else term

        d = json.loads(COCO80_VI.read_text(encoding="utf-8"))
        pairs = [(norm_tone(t.lower()), c) for c, ts in d.items() if not c.startswith("_")
                 for t in ts if isinstance(t, str) and not t.startswith("_rui_ro")]
        _TERMS = sorted(pairs, key=lambda x: (-len(head(x[0])), -len(x[0])))
    return _TERMS


def mentions(caption: str, check: bool = True) -> list[dict]:
    """[{cls, term, start}] of a caption, one per distinct class, sorted by the class's first consumed span."""
    repo()
    from rescap.chair import norm_tone
    from score_coco_probe import LEX_V2

    text = caption.lower()
    for pattern, repl in LEX_V2:
        text = re.sub(pattern, repl, text)
    text = " " + norm_tone(text) + " "
    first: dict[str, tuple[int, str]] = {}
    for term, cls in load_terms():
        spans = [m.span() for m in re.finditer(re.escape(term), text)
                 if not re.match(f"[{_LETTER}]", text[m.start() - 1]) and not re.match(f"[{_LETTER}]", text[m.end()])]
        for a, b in spans:
            text = text[:a] + "\0" * (b - a) + text[b:]
            if cls not in first or a < first[cls][0]:
                first[cls] = (a, term)
    out = [{"cls": c, "term": t, "start": s} for c, (s, t) in sorted(first.items(), key=lambda kv: (kv[1][0], kv[0]))]
    if check:
        import score_coco_probe as sc

        if {m["cls"] for m in out} != sc.vi_objects(caption, load_terms()):
            raise SystemExit("FAULT ordered mentions disagree with score_coco_probe.vi_objects")
    return out


def ordered_classes(caption: str) -> list[str]:
    return [m["cls"] for m in mentions(caption)]


def entity_propositions(caption: str) -> list[dict]:
    """V-COCO units of one caption: one entity proposition per mentioned COCO-80 class (the probe text is the
    matched Vietnamese phrase; the Q+ template is applied by the probe runner)."""
    return [{"type": "entity", "cls": m["cls"], "text_vi": m["term"], "order": i} for i, m in enumerate(mentions(caption))]


def en_classes(caption: str) -> set[str]:
    """English COCO-80 classes (H5): score_coco_probe.en_classes with the CHAIR synonym map, unchanged."""
    repo()
    import score_coco_probe as sc

    return sc.en_classes(caption, sc.load_synonyms())
