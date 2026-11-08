#!/usr/bin/env python3
"""'cây' sensitivity rule of T1-REP v4 §5 (AMENDMENT_T1_REPORTING_DRAFT_v4.md 0e9793f3, commit 4124ef3; PI-1104ah
Q5 = YES, sensitivity only). The scorer of record stays rescap/chair.py (e47d249a), unedited; this file only says
which 'cây' mentions the sensitivity scorer ignores. Stdlib only; the lexicon is passed in by the caller.

    ~/.venvs/c_pvr/bin/python -I -B scripts/c_pvr/c_pvr_cay.py selftest     synthetic short phrases only

Rule (T1-REP §5, hardened per CC-253 N-7):
  1. the caption's raw NFC, lower-cased string;
  2. an occurrence of the word 'cây' counts only if exactly one space and then a word follow it ('cây, dù' does not);
  3. the longest NOUN_CLASSIFIER key that matches from that word and ends at a word boundary;
  4. the occurrence is ignored only if that key is in K, K = {n : NOUN_CLASSIFIER[n] == 'cây', n != 'cây'},
     recomputed from the pinned lexicon (fbc945f2), never typed;
  5. the class 'cây' leaves the caption's mention set only if every occurrence is ignored (once per caption).
Disclosed limits (T1-REP §5): classifier uses with unlisted nouns are not caught; a compound that starts with a K
noun and is not a key ('cầu thủ') is matched as the K noun alone. The count of mentions this rule ignores is a
scorer-side count, not a data removal (CC-253 CX2), supplement only.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

CAY = "cây"
OCC = re.compile(r"(?<!\w)cây(?!\w)")
LETTER = re.compile(r"[^\W\d_]")


def classifier_set(noun_classifier: dict) -> frozenset:
    """K of rule 4, from the lexicon table itself."""
    return frozenset(n for n, c in noun_classifier.items() if c == CAY and n != CAY)


def occurrences(text: str, keys, k: frozenset) -> tuple[int, int]:
    """(occurrences of the word 'cây', occurrences the rule ignores) in one caption (rules 1-4)."""
    s = unicodedata.normalize("NFC", text).lower()
    occ = ign = 0
    for m in OCC.finditer(s):
        occ += 1
        q = m.end() + 1
        if s[m.end():q] != " " or not LETTER.match(s, q):
            continue
        hit = max((key for key in keys if s.startswith(key, q) and not re.match(r"\w", s[q + len(key):q + len(key) + 1])),
                  key=len, default=None)
        ign += hit in k
    return occ, ign


def apply(classes: set, text: str, keys, k: frozenset) -> tuple[set, bool]:
    """Rule 5: (the caption's class set under the sensitivity scorer, whether 'cây' was ignored)."""
    if CAY not in classes:
        return classes, False
    occ, ign = occurrences(text, keys, k)
    gone = occ > 0 and ign == occ
    return (classes - {CAY} if gone else classes), gone


# ---------------------------------------------------------------------------------------------- selftest
def selftest(root: Path) -> None:
    sys.path.insert(0, str(root))
    from rescap.vi.lexicon import NOUN_CLASSIFIER
    keys, k = list(NOUN_CLASSIFIER), classifier_set(NOUN_CLASSIFIER)
    cases = {
        "K_from_lexicon": lambda: k == {"dù", "bút", "chổi", "cầu"},  # T1-REP l.234 lists this K at fbc945f2
        "keys_nfc_lower": lambda: all(x == unicodedata.normalize("NFC", x).lower() for x in keys),
        "adjacent_ignored": lambda: occurrences("một cây dù đỏ", keys, k) == (1, 1),
        "bút_chổi_ignored": lambda: [occurrences(t, keys, k) for t in ("cây bút", "cây chổi")] == [(1, 1), (1, 1)],
        "comma_not_adjacent": lambda: occurrences("cây, dù", keys, k) == (1, 0),
        "two_spaces_not_adjacent": lambda: occurrences("cây  dù", keys, k) == (1, 0),
        "no_space_not_adjacent": lambda: occurrences("cây,dù", keys, k) == (1, 0),
        "end_of_text_kept": lambda: occurrences("dưới gốc cây", keys, k) == (1, 0),
        "noun_not_in_K_kept": lambda: occurrences("cây nhà", keys, k) == (1, 0),
        "word_boundary_on_key": lambda: occurrences("cây dùng", keys, k) == (1, 0),
        "cầu_thủ_limit": lambda: occurrences("cây cầu thủ", keys, k) == (1, 1),
        "longer_key_wins": lambda: occurrences("cây cầu thang", ["cây", "cầu", "cầu thang"], frozenset({"cầu"})) == (1, 0),
        "longer_key_shorter_in_K": lambda: occurrences("cây cầu", ["cây", "cầu", "cầu thang"], frozenset({"cầu"})) == (1, 1),
        "nfc_and_case": lambda: occurrences(unicodedata.normalize("NFD", "Cây Dù"), keys, k) == (1, 1),
        "not_inside_a_word": lambda: occurrences("mâycây dù", keys, k) == (0, 0),
        "rule5_all_ignored": lambda: apply({"cây", "dù"}, "hai cây dù", keys, k) == ({"dù"}, True),
        "rule5_one_left": lambda: apply({"cây", "dù"}, "cây dù cạnh cây lớn", keys, k) == ({"cây", "dù"}, False),
        "rule5_no_cay_class": lambda: apply({"dù"}, "cây dù", keys, k) == ({"dù"}, False),
        "rule5_no_occurrence": lambda: apply({"cây"}, "", keys, k) == ({"cây"}, False),
    }
    for name, fn in cases.items():
        try:
            good = fn()
        except Exception as e:  # a crash inside a named case is that case's failure
            good = f"{type(e).__name__}: {e}"
        if good is not True:
            raise SystemExit(f"selftest FAILED: {name} ({good})")
    print(f"c_pvr_cay selftest ok ({len(cases)} cases)")


if __name__ == "__main__":
    if sys.argv[1:] != ["selftest"]:
        raise SystemExit(__doc__)
    selftest(Path(__file__).resolve().parents[2])
