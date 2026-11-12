"""Mechanical checks of the v1.1 files against CC-350, independent of the build script's extraction.

Each CC replacement text is located in the raw CC file by hand-typed start/end markers, whitespace-collapsed,
and searched for in the whitespace-collapsed v1.1 files. Then the brief's consistency greps are classified.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
CC = FOLDER.parents[2] / ".session_backup/2026-10-13/decisions/CC-350.txt"
PRE = (FOLDER / "B_FECERT_PREREG_v1_1.md").read_text(encoding="utf-8")
PLAN = (FOLDER / "B_PREF_LABELLING_PLAN_v1_1.md").read_text(encoding="utf-8")


def col(s):
    return re.sub(r"\s+", " ", s).strip()


CCC = col(CC.read_text(encoding="utf-8"))
BOTH = col(PRE) + " || " + col(PLAN)

# (item, start marker, end marker) : the CC text from start through end must appear verbatim in v1.1.
MARKERS = [
    ("W1a", "- **Sensitivity control NC (computed and pinned at stage 1", "had little room to fail'."),
    ("W1b", "is written, with the ids of V, into", "before stage 2b runs any held-out member"),
    ("W1c", "Stage 2b refuses to start", "without the V.json LOG line."),
    ("W1d", "held-out member scored before", "the V.json LOG line"),
    ("W1e", "one-sided 95% Clopper-Pearson upper bound", "upper bound <= 0.05"),
    ("W2a", "### 6.4 P4, FE-ID planted check", "reported as a reproduction table."),
    ("W2b-s9", "P3; P4 method check", "P3; P4 method check"),
    ("W2b-s11", "P4 wrong recovery: FAULT;", "IDENTIFIED: reproduction table"),
    ("W2b-s12", "a wrong recovery raises FAULT", "a wrong recovery raises FAULT"),
    ("W3", "- **Labels.** P3b is POST HOC", "are reported for each baseline."),
    ("W3-s11", "on the metrics never compared before (M_new)", "(M_new)"),
    ("W4b", "round-2 diff read; gatekeeper commit of this file", "PI names the second rater"),
    ("W4c-0a", "0a documents (before any fetch", "or schema print)"),
    ("W4c-0b", "0b code (after the code", "read)"),
    ("W5-2.2", "not in F (CC-350 ruling 2); in F+ only", "in F+ only"),
    ("W5-2.3", "not admissible (CC-350 ruling 2)", "(CC-350 ruling 2)"),
    ("W5-5.1", "|F+| = 90 x 3 + 1 = 271, `chr` included", "`chr` included"),
    ("W5-6.1", "r for `uts`, and DESCRIPTIVE 'with chr' rows", "(chr members added to F_held), no verdict"),
    ("W5-6.6", "with `chr`", "with `chr`"),
    ("W6-2.1", "image files `data/datasets/ktvic/images/<filename>`", "6 `.jpeg`)"),
    ("W6-route", "The image route regex becomes", "`image/jpeg` otherwise."),
    ("W6-test", "every drawn image's path exists", "served by the endpoint test"),
    ("W7-dir", "`~/vsps_labels_b/b_pref/`", "`~/vsps_labels_b/b_pref/`"),
    ("W7-item6", "`--port` default 8791;", "must not be under `~/vsps_labels/`."),
    ("W7-custody", "The custody rules of plan §6 apply", "in the same way."),
    ("R8d", "sha only, a generic client", "plus the already-fetched X3 and K2 files, aggregate only."),
    ("R9a", "300 distinct pairs, 30 hidden repeats", "not new items."),
    ("R10", "the output went to /dev/null", "in the access record)."),
    ("Plan-Q", "Plan §11: Q1 yes;", "Q5 yes; Q6 yes."),
    ("N3-pyvi", "pyvi also ran on K1, K5 and K6", "(b2.py l.711-752)."),
    ("N3-826", "the 82.6% is on 2,000 KTVIC captions", "prefers train_data.json"),
    ("N3-gate", "The gate v2 thresholds were set after", "unknown-id counts)."),
]
ok = True
for item, start, end in MARKERS:
    i = CCC.find(start)
    j = CCC.find(end, i)
    assert i >= 0 and j >= 0, f"marker not in CC: {item}"
    text = CCC[i:j + len(end)]
    hit = text in BOTH
    ok &= hit
    print(f"{'OK ' if hit else 'MISSING'} {item:10s} ({len(text)} chars)")

# §16 rulings, one per question: CC text from "Q<n> " up to the next "Q<n+1> " (Q15 up to "Plan §11:").
qblock = CCC[CCC.find("Q1 PI-1111l"):CCC.find("Plan §11: Q1 yes")]
for n, q in enumerate(re.split(r" (?=Q\d+ )", qblock), 1):
    hit = q.strip() in BOTH
    ok &= hit
    print(f"{'OK ' if hit else 'MISSING'} Q-ruling {q.split()[0]:4s} ({len(q)} chars)")


def hits(pattern, text, name):
    return [(name, n, ln) for n, ln in enumerate(text.split("\n"), 1) if re.search(pattern, ln)]


def show(title, rows):
    print(f"\n== {title}: {len(rows)} line(s)")
    for name, n, ln in rows:
        m = re.search(r".{0,70}(" + PAT + r").{0,70}", ln)
        print(f"  {name}:{n}: …{m.group(0) if m else ln[:140]}…")


FILES = (("prereg", PRE), ("plan", PLAN))
for title, PAT in (("[proposal]", r"\[proposal"),
                   ("P4", r"\bP4\b"),
                   ("\\b90\\b", r"\b90\b"),
                   ("\\b72\\b", r"\b72\b"),
                   ("879x", r"879\d"),
                   ("~/vsps_labels", r"~/vsps_labels")):
    rows = [r for f, t in FILES for r in hits(PAT, t, f)]
    show(title, rows)

# P4 as a prediction: any line naming P4 together with prediction/PASS/FAIL wording (excluding E4 row names).
bad = [(f, n, ln) for f, t in FILES for n, ln in enumerate(t.split("\n"), 1)
       if re.search(r"\bP4\b(?!_T3bug)", ln) and re.search(r"P4[^|]{0,60}(REGISTERED PREDICTION|\bPASS\b|\bFAIL\b)", ln)
       and "not a registered prediction" not in ln and "not a prediction" not in ln and "not a FAIL" not in ln]
print(f"\nP4-as-prediction lines: {len(bad)}")
for f, n, ln in bad:
    print(f"  {f}:{n}: {ln[:200]}")
print("\nVERBATIM:", "ALL PRESENT" if ok else "SOME MISSING")
sys.exit(0 if ok else 1)
