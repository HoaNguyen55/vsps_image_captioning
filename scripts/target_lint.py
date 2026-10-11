#!/usr/bin/env python
"""Count known defect patterns in SFT target captions (detailed rows).

    python scripts/target_lint.py data/supervision_v2/raw/sft.jsonl [more.jsonl ...]

Each pattern is a defect the renderer is known to produce; the rate is the share
of detailed captions with at least one hit. A target-quality check to run before
spending a training run, not a fluency metric.
"""
from __future__ import annotations

import json
import re
import sys

PATTERNS = {
    "gendered_word": r"\b(phụ nữ|đàn ông|cô gái|chàng trai|cậu bé|cô bé|bé gái|bé trai)\b",
    "person_has_colour": r"\bngười (có )?màu\b",
    "dup_word": r"\b(\S+) \1\b",
    "quantifier_as_noun": r"\b(cái|chiếc|con) số\b",
    "classifier_on_person": r"\b(cái|chiếc) (người|nhân viên|khách hàng|trẻ em|học sinh)\b",
    "np_echo": r"\b(một|hai|nhiều|các|những|một số) (người|nhóm người)\b,? (một|hai|nhiều|các|những|một số) (người|nhóm người)\b",
    "pronoun_remnant": r"\b(cô|anh|chị|ông|bà|em) (ấy|ta)\b",
    "dangling_end": r"\b(có một|còn có|có|một|cái|và|của)\s*$",
}


def lint(captions: list[str]) -> dict[str, float]:
    n = max(len(captions), 1)
    return {k: round(100 * sum(bool(re.search(p, c.lower().rstrip(". "))) for c in captions) / n, 1)
            for k, p in PATTERNS.items()}


def self_check() -> None:
    got = lint(["Một người có màu đỏ và trắng đang đứng.", "Một chiếc áo đỏ đỏ, còn có một cái số tủ"])
    assert got["person_has_colour"] == 50.0 and got["dup_word"] == 50.0, got
    assert got["quantifier_as_noun"] == 50.0 and got["dangling_end"] == 0.0, got
    assert lint(["Một người đang mặc một chiếc áo, đứng cạnh xe máy."]) == dict.fromkeys(PATTERNS, 0.0)


if __name__ == "__main__":
    self_check()
    for path in sys.argv[1:]:
        caps = [r["response"] for r in map(json.loads, open(path, encoding="utf-8"))
                if "Mô tả chi tiết" in r["prompt"]]
        print(path, len(caps), lint(caps))
