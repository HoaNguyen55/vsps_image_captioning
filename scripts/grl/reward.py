#!/usr/bin/env python3
"""G-RL reward: gold-instance object F1 over COCO-80 with the language, finish, repetition and length gates and the
matcher-gaming guard. Rule: manuscript/prereg/2026-10-27_grl_pilot/PILOT_RULE.md §4.

    python3 scripts/grl/reward.py --selftest                CPU, synthetic matcher fixtures
    python3 scripts/grl/reward.py gold                      laptop, CPU: gold_instances.json from COCO-2014 instances
                                                            (UT-2402 and val-924 ids only)

Matchers (score_coco_probe.py, unchanged): v1 = the coco80_vi.json lexicon, longest phrase first, spans consumed;
v2 = LEX_V2's six rewrites, then v1. The reward uses v1; the dev score uses v2. v1's rules are a subset of v2's, but
the detected classes are not nested: LEX_V2 removes some v1 hits (`ghi bàn` is not a dining table) and adds others
(`cầu thủ` is a person). The selftest pins both directions.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent), str(HERE.parents[1])]
import common as K  # noqa: E402
from clean_supervision import CJK_RE, HEDGE_RE, OUT_OF_SCRIPT_RE  # noqa: E402
from rl_reward import syllables  # noqa: E402
from score_coco_probe import _LETTER, LEX_V2, load_vi_terms, norm_tone, vi_objects  # noqa: E402

NEG_RE = re.compile(r"\b(không\s+(có|thấy|phải|hề)|chẳng|chưa\s+(có|thấy))\b", re.I)
CLAUSE_RE = re.compile(r"[.,;:!?\n]|\bnhưng\b", re.I)
BULLET_RE = re.compile(r"(^|\n)\s*([-*•+]|\d+[.)])\s", re.M)
VI_MARKS = set("ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ")  # = rescap looks_vietnamese


@lru_cache(maxsize=1)
def terms():
    return load_vi_terms()


def ordered(caption: str, ver: str) -> tuple[list[str], str]:
    """(COCO-80 classes in order of first mention, the caption with every matched span blanked) under matcher v1/v2.
    The same loop as score_coco_probe.vi_classes, keeping each class's first span start; the selftest asserts the
    class set equals vi_objects."""
    text = caption.lower()
    for pattern, repl in LEX_V2 if ver == "v2" else ():
        text = re.sub(pattern, repl, text)
    text = " " + norm_tone(text) + " "
    first: dict[str, int] = {}
    for term, cls in terms():
        spans = [m.span() for m in re.finditer(re.escape(term), text)
                 if not re.match(f"[{_LETTER}]", text[m.start() - 1]) and not re.match(f"[{_LETTER}]", text[m.end()])]
        for a, b in spans:
            text = text[:a] + "\0" * (b - a) + text[b:]
        if spans:
            first[cls] = min(first.get(cls, 1 << 30), spans[0][0])
    return sorted(first, key=first.get), text.replace("\0", " ")


def vietnamese_only(c: str) -> bool:
    return any(ch in VI_MARKS for ch in c.lower()) and not CJK_RE.search(c) and not OUT_OF_SCRIPT_RE.search(c)


def degenerate(c: str) -> bool:
    w, n = syllables(c), K.CFG["repeat_ngram"]
    grams = Counter(tuple(w[i:i + n]) for i in range(len(w) - n + 1))
    return bool(grams) and max(grams.values()) > K.CFG["repeat_max"]


def noun_list(c: str) -> bool:
    """4+ segments (split at , ; . or a newline) of at most 3 syllables each: a bare noun list (the F1-gaming
    form). Ordinary multi-sentence captions have long segments and pass (CC-124 W4)."""
    seg = [s for s in re.split(r"[,;.\n]", c) if s.strip()]
    return sum(len(syllables(s)) <= 3 for s in seg) >= 4


def list_style(c: str) -> bool:
    """A noun list or bullet/numbered lines (the CC-114 r6 list-style guard)."""
    return noun_list(c) or bool(BULLET_RE.search(c))


def unasserted(c: str) -> tuple[str, str]:
    """(asserted text, negated or hedged text): clauses with a negation or a hedge assert none of their classes."""
    parts = CLAUSE_RE.split(c)
    hedged = [p for p in parts if NEG_RE.search(p) or HEDGE_RE.search(p)]
    return " . ".join(p for p in parts if p not in hedged), " . ".join(hedged)


def reward(c: str, finished: bool, g: set[str], window: tuple[float, float]) -> tuple[float, str]:
    """(reward in [0, 1], why). Gates (unfinished, language, repetition, list style, length) give 0. F1 = 2PR/(P+R) of v1 classes against the instance gold, where a class
    named only in a negated or hedged clause counts as a false positive (the matcher-gaming guard: naming a class
    without asserting it never earns a true positive). No class named and no gold class = 1."""
    if not finished:
        return 0.0, "unfinished"
    if not vietnamese_only(c):
        return 0.0, "language"
    if degenerate(c):
        return 0.0, "repetition"
    if list_style(c):
        return 0.0, "noun-list"
    if not window[0] <= len(syllables(c)) <= window[1]:
        return 0.0, "length"
    said, hedged = unasserted(c)
    m = set(ordered(said, "v1")[0])
    extra = set(ordered(hedged, "v1")[0]) - m
    if not m and not extra:
        return (1.0 if not g else 0.0), "f1"
    tp = len(m & g)
    p, r = tp / (len(m) + len(extra)), (tp / len(g) if g else 0.0)
    return (2 * p * r / (p + r) if p + r else 0.0), "f1"


def anchors(sample_lengths: list[int]) -> dict:
    """The length window from the base model's step-0 samples on train (syllables)."""
    s = sorted(sample_lengths)
    med = s[len(s) // 2] if len(s) % 2 else (s[len(s) // 2 - 1] + s[len(s) // 2]) / 2
    lo, hi = K.CFG["window"]
    return {"median_syllables": med, "window": [lo * med, hi * med], "n_samples": len(s)}


def build_gold() -> int:
    """gold_instances.json: {id: sorted COCO class names} for UT-2402 and val-924, from instances_{train,val}2014."""
    ann = K.ROOT / "data/datasets/coco_probe/annotations"
    pins = {"instances_train2014.json": "777ef504abfeba349930485bb32ecd5b6529129a3e010f7852e1437cb049b732",
            "instances_val2014.json": "e1b4d1bc54906827b1a029981b1c77f2088bd4462569b7615db7929070c3ab47"}
    want = set(K.ids("ut2402")) | set(K.ids("val924"))
    gold: dict[int, set] = {i: set() for i in want}
    seen: set[int] = set()
    for f, sha in pins.items():
        if K.sha_file(ann / f) != sha:
            raise SystemExit(f"{f}: sha256 differs from its pin")
        inst = json.loads((ann / f).read_text())
        cat = {c["id"]: c["name"] for c in inst["categories"]}
        seen |= {r["id"] for r in inst["images"] if r["id"] in want}
        for a in inst["annotations"]:
            if a["image_id"] in want:
                gold[a["image_id"]].add(cat[a["category_id"]])
    if seen != want:
        raise SystemExit(f"{len(want - seen)} ids are not in COCO-2014")
    out = K.PDIR / "gold_instances.json"
    rec = {"schema": "vsps.grl.gold.v1", "definition": "COCO-2014 categories with >= 1 instance (crowd included), "
           "80 classes; instances only, no reference-derived class (CC-114 W8)", "inputs_sha256": pins,
           "n": len(gold), "gold": {str(i): sorted(gold[i]) for i in sorted(gold)}}
    out.write_text(json.dumps(rec, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    print(json.dumps({"n": len(gold), "empty": sum(not v for v in gold.values()), "sha256": K.sha_file(out)}))
    return 0


def selftest() -> None:
    t = terms()
    # v1 rules are a subset of v2's, detected classes are not nested (both directions)
    for c, v1, v2 in (("cầu thủ ghi bàn", {"dining table"}, {"person"}),
                      ("người cầm quả bóng", {"person", "sports ball"}, {"person", "sports ball"}),
                      ("con chó chạy cạnh cái bàn", {"dog", "dining table"}, {"dog", "dining table"})):
        for ver, want in (("v1", v1), ("v2", v2)):
            got = ordered(c, ver)[0]
            assert set(got) == want == vi_objects(c, t, ver), (c, ver, got)
    assert ordered("cái bàn cạnh con chó", "v1")[0] == ["dining table", "dog"]  # first-mention order
    assert ordered("con chó cạnh cái bàn", "v1")[0] == ["dog", "dining table"]
    assert "chó" not in ordered("con chó cạnh cái bàn", "v1")[1]
    g, w = {"person", "sports ball"}, (2, 40)
    full = reward("một người cầm quả bóng", True, g, w)
    assert full == (1.0, "f1"), full
    half = reward("một người", True, g, w)[0]
    assert abs(half - 2 * 1 * 0.5 / 1.5) < 1e-9, half
    # a hedged or negated class earns nothing and costs precision
    hedged = reward("một người, có vẻ là con chó", True, g, w)[0]
    assert abs(hedged - 2 * 0.5 * 0.5 / 1.0) < 1e-9, hedged
    assert reward("một người, không có quả bóng", True, g, w)[0] < half
    assert reward("một người cầm quả bóng", False, g, w) == (0.0, "unfinished")
    assert reward("a person holds a ball", True, g, w)[1] == "language"
    assert reward("một người 人", True, g, w)[1] == "language"
    loop = " ".join(["người cầm quả bóng xanh"] * 3)
    assert reward(loop, True, g, (2, 99))[1] == "repetition"
    assert reward("một người cầm quả bóng", True, g, (10, 20))[1] == "length"
    for lst in ("người, quả bóng, cái bàn, con chó", "- người\n- quả bóng\n- cái bàn\n- con chó",
                "người\nquả bóng\ncái bàn\ncon chó", "1. người\n2. quả bóng\n3. cái bàn\n4. con chó",
                "người. quả bóng. cái bàn. con chó.", "Ảnh có:\n- một người\n- quả bóng"):
        assert reward(lst, True, g, w) == (0.0, "noun-list"), lst
    assert not list_style("một người, đang xoay quả bóng tím bên cột đèn hồng nhấp nháy")  # CC-125 X5 strings
    assert reward("một người khẽ hất quả bóng bạc lơ lửng. phía xa có cột đèn tím nhấp nháy liên hồi.", True, g,
                  (2, 99))[1] == "f1"
    assert reward("bầu trời xanh", True, set(), w)[0] == 1.0 and reward("bầu trời xanh", True, g, w)[0] == 0.0
    a = anchors([10, 20, 30, 40])
    assert a["median_syllables"] == 25 and a["window"] == [18.75, 31.25], a
    print("reward selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    elif sys.argv[1:2] == ["gold"]:
        sys.exit(build_gold())
    else:
        sys.exit(__doc__)
