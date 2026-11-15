"""Paper B Table 6 (FIGURE_TABLE_SPEC A2): regenerate the human-arm table from HUMAN.json and BUILD.json,
print it in Markdown, and compare every value cell with the table of paper.md block T6.
Any difference is a failure (exit 1). This script never edits paper.md.

Usage:  python3 table6_human.py [--out DIR]      build, print, compare with the held paper.md
        python3 table6_human.py --selftest       synthetic inputs; asserts cells and a mismatch detection

Self-contained: each script in this folder carries its own helpers.
"""
import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HELD = ".session_backup/2026-11-14/b_text_held/draft_v3"
HUMAN_REL = ".session_backup/2026-11-13/b_stages/host_pull/H_20261115T083124Z/b_work/HUMAN.json"
HUMAN_SHA = "990a0df51ba3e35349fbe2dcf37826150ce9d5c3aa88b3e375c697377f745057"
BUILD_REL = "manuscript/prereg/2026-11-12_b_fecert/b_pref_pin/BUILD.json"
BUILD_SHA = "05a6c5b72aa4c17c6baf1b1bd520700730f90f073997e8c5977f1f8188c3b201"
PAPER_REL = f"{HELD}/paper.md"
PAPER_SHA = "cb462dfc4797f3b7030fbe58a7b873aabef8a204cba62b55392cde92c1ed6a0e"
DEFAULT_OUT = ROOT / "scripts/b_figs/out"
STRATA = ("P", "U", "C")
SIDED = {"P": "one-sided", "U": "two-sided"}  # as in the draft: H-P one-sided, H-U two-sided
NO_TEST = "no test registered"
NOT_IN_FILE = "not in the result file"
LABEL = "no label: low inter-rater agreement"
# Printed in the draft after the registered band; the band text is not in any input, so it is not checked.
BAND_PREFIX_SPLIT = "; "


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def read_checked(path, sha):
    data = path.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if got != sha:
        fail(f"sha256 of {path.name} is {got}, expected {sha}")
    print(f"input {path.name} sha256 {got} ok")
    return data


def f3(x):
    return f"{x:.3f}"


def near_int(x):
    n = round(x)
    if abs(x - n) > 1e-6:
        fail(f"{x} is not a whole count")
    return int(n)


def holm_text(v):
    if v == 0.0:
        return "not rejected"
    if v == 1.0:
        return "rejected"
    fail(f"holm_rejected value {v!r} is neither 0.0 nor 1.0")


def table_rows(h, b):
    """Return (rows, checks). rows: list of [P, U, C] value cells, in the order of the draft's Table 6."""
    ir = h["inter_rater"]
    st = h["strata"]
    drawn = b["counts"]["drawn"]
    elig = b["counts"]["eligible_images"]
    if ir["n"] != b["counts"]["main_pairs"]:
        fail("HUMAN inter_rater.n differs from BUILD counts.main_pairs")
    if sum(drawn[s] for s in STRATA) != ir["n"]:
        fail("BUILD counts.drawn over P, U, C does not sum to inter_rater.n")
    n_dec = {s: st[s]["n_dec"] for s in STRATA}
    dec_total = sum(n_dec.values())
    tie, split = h["not_decisive"]["tie"], h["not_decisive"]["split"]
    if dec_total + tie + split != ir["n"]:
        fail("decisive + tie + split does not equal the main pairs")
    for r in ("PI", "R2"):
        if h["tie_cannot_rates"][r]["cannot"] != 0.0:
            fail(f"tie_cannot_rates.{r}.cannot is not 0.0")
    raw_count = near_int(ir["raw"] * ir["n"])
    cannot_row = "not used by either rater; none"

    def alone(r, s):
        return h["rater_alone"][r][s] if s in h["rater_alone"][r] else None

    def alone_match(r, s):
        row = alone(r, s)
        return NOT_IN_FILE if row is None else f"{row['k_word']} of {row['n']}"

    def alone_share(r, s):
        row = alone(r, s)
        if row is None:
            return NOT_IN_FILE
        return f"{f3(row['k_word'] / row['n'])}; {f3(row['p'])}, {SIDED[s]}"

    def margin(s, key):
        k, n = h["margin_bins"][s][key]
        return f"{k} of {n}"

    def pval(s):
        return f"{f3(h['p']['H-P'])}, one-sided" if s == "P" else f"{f3(h['p']['H-U'])}, two-sided"

    upper = [
        [str(elig[s]) for s in STRATA],
        [str(drawn[s]) for s in STRATA],
        [str(n_dec[s]) for s in STRATA],
        [str(st[s]["k_word"]) for s in STRATA],
        [f"{f3(st[s]['q'])} [{f3(st[s]['ci95'][0])}, {f3(st[s]['ci95'][1])}]" for s in STRATA],
        [pval("P"), pval("U"), NO_TEST],
        [holm_text(h["holm_rejected"]["H-P"]), holm_text(h["holm_rejected"]["H-U"]), NO_TEST],
        [LABEL, LABEL, "no label registered"],
        [alone_match("R2", "P"), alone_match("R2", "U"), NOT_IN_FILE],
        [alone_share("R2", "P"), alone_share("R2", "U"), NOT_IN_FILE],
        [alone_match("PI", "P"), alone_match("PI", "U"), NOT_IN_FILE],
        [alone_share("PI", "P"), alone_share("PI", "U"), NOT_IN_FILE],
        [f3(ir["kappa_per_stratum"][s]) for s in STRATA],
        [margin(s, "below_or_at_median") for s in STRATA],
        [margin(s, "above_median") for s in STRATA],
    ]
    both_decided = dec_total + split
    lower_values = [
        f"{ir['n']}; {ir['n']}",
        str(dec_total),
        str(tie),
        str(split),
        cannot_row,
        f"{f3(ir['kappa'])} [{f3(ir['kappa_ci95'][0])}, {f3(ir['kappa_ci95'][1])}]",
        f"{f3(ir['raw'])} ({raw_count} of {ir['n']})",
        f3(ir["ac1"]),
        f"{f3(ir['kappa_two_category'])} ({both_decided} pairs)",
        f"{f3(h['tie_cannot_rates']['PI']['tie'])} ({near_int(h['tie_cannot_rates']['PI']['tie'] * ir['n'])}); "
        f"{f3(h['tie_cannot_rates']['R2']['tie'])} ({near_int(h['tie_cannot_rates']['R2']['tie'] * ir['n'])})",
        f"{f3(h['within_rater']['PI']['raw'])}; {f3(h['within_rater']['PI']['kappa'])}",
        f"{f3(h['within_rater']['R2']['raw'])}; {f3(h['within_rater']['R2']['kappa'])}",
    ]
    rows = [list(r) for r in upper] + [[v, "", ""] for v in lower_values]
    return rows


def check_registered(h, b):
    """The file-level checks that the table relies on; a failure stops the build."""
    if h["gate"] != "low inter-rater agreement":
        fail(f"gate is {h['gate']!r}")
    for s in STRATA:
        if abs(h["strata"][s]["q"] - h["strata"][s]["k_word"] / h["strata"][s]["n_dec"]) > 1e-9:
            fail(f"stratum {s}: q is not k_word / n_dec")


def t6_rows(paper_text):
    """Rows (value cells only, label dropped) of the table in the block T6 of paper.md."""
    lines = paper_text.splitlines()
    start = [i for i, ln in enumerate(lines) if "id=T6" in ln and ln.startswith("<!-- @P")]
    if len(start) != 1:
        fail("block T6 not found exactly once in paper.md")
    rows = []
    for ln in lines[start[0] + 1:]:
        if ln.startswith("<!-- @P"):
            break
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells) or cells[0] == "Quantity":
            continue
        rows.append(cells[1:4])
    return rows


def compare(rows, paper_rows):
    diffs = []
    if len(rows) != len(paper_rows):
        diffs.append(f"row count {len(rows)} generated, {len(paper_rows)} in paper.md")
        return diffs
    for i, (mine, theirs) in enumerate(zip(rows, paper_rows), start=1):
        if len(theirs) != 3:
            diffs.append(f"row {i}: paper.md has {len(theirs)} value cells")
            continue
        for col, (a, b_) in enumerate(zip(mine, theirs)):
            if a == b_:
                continue
            # The registered band cell of the kappa row ends with band text not present in any input.
            if a and b_.startswith(a + BAND_PREFIX_SPLIT) and col == 0 and "[" in a:
                print(f"note row {i}: band text not checked by this script: {b_[len(a) + 2:]!r}")
                continue
            diffs.append(f"row {i} column {col + 1}: generated {a!r}, paper.md {b_!r}")
    return diffs


def markdown(rows, labels):
    out = ["| Quantity | Punctuation flip (P) | Unit flip (U) | Control (C) |", "|---|---|---|---|"]
    for lab, cells in zip(labels, rows):
        out.append("| " + " | ".join([lab] + cells) + " |")
    return "\n".join(out) + "\n"


LABELS = [
    "Eligible images", "Pairs judged by both raters", "Decisive pairs", "Consensus: decisive pairs that match",
    "Consensus share [95% interval]", "Exact binomial p against 0.5", "Holm's correction at 0.05",
    "Registered label", "Non-author rater alone: pairs that match, of pairs decided",
    "Non-author rater alone: share; p", "Author rater alone: pairs that match, of pairs decided",
    "Author rater alone: share; p", "Cohen's κ within the stratum",
    "Margin at or below the stratum median: decisive pairs that match",
    "Margin above the stratum median: decisive pairs that match",
    "All main pairs; pairs answered by both raters", "Decisive pairs", "Not decisive: a tie by at least one rater",
    "Not decisive: split preference", 'Not decisive: "cannot judge"; missing',
    "Cohen's κ, three categories [bootstrap 95% interval]; registered band", "Raw agreement", "Gwet's AC1",
    "κ, two categories, on the pairs both raters decided", "Tie rate: author rater; non-author rater",
    "Within rater, 30 hidden repeats, author rater: raw; κ",
    "Within rater, 30 hidden repeats, non-author rater: raw; κ",
]


def synthetic():
    h = {
        "gate": "low inter-rater agreement",
        "raters": ["PI", "R2"],
        "inter_rater": {"n": 20, "raw": 0.7, "ac1": 0.25, "kappa": 0.4, "kappa_ci95": [0.2, 0.6],
                        "kappa_per_stratum": {"P": 0.1, "U": 0.2, "C": 0.3}, "kappa_two_category": 0.5},
        "strata": {
            "P": {"k_word": 2, "n_dec": 4, "q": 0.5, "ci95": [0.15, 0.85]},
            "U": {"k_word": 1, "n_dec": 5, "q": 0.2, "ci95": [0.05, 0.6]},
            "C": {"k_word": 3, "n_dec": 3, "q": 1.0, "ci95": [0.3, 1.0]},
        },
        "p": {"H-P": 0.25, "H-U": 1.0},
        "holm_rejected": {"H-P": 0.0, "H-U": 0.0},
        "rater_alone": {
            "R2": {"P": {"k_word": 1, "n": 2, "p": 0.5}, "U": {"k_word": 2, "n": 4, "p": 0.375}},
            "PI": {"P": {"k_word": 2, "n": 3, "p": 0.75}, "U": {"k_word": 3, "n": 6, "p": 1.0}},
        },
        "margin_bins": {"P": {"below_or_at_median": [1, 2], "above_median": [1, 2]},
                        "U": {"below_or_at_median": [2, 5], "above_median": [0, 1]},
                        "C": {"below_or_at_median": [1, 1], "above_median": [2, 2]}},
        "not_decisive": {"tie": 4, "split": 4},
        "tie_cannot_rates": {"PI": {"tie": 0.2, "cannot": 0.0}, "R2": {"tie": 0.1, "cannot": 0.0}},
        "within_rater": {"PI": {"raw": 0.9, "kappa": 0.8, "n": 10}, "R2": {"raw": 0.6, "kappa": 0.3, "n": 10}},
    }
    b = {"counts": {"main_pairs": 20, "drawn": {"P": 6, "U": 8, "C": 6},
                    "eligible_images": {"P": 30, "U": 40, "C": 50}}}
    return h, b


def run_selftest():
    h, b = synthetic()
    rows = table_rows(h, b)
    assert len(rows) == len(LABELS) == 27, len(rows)
    assert rows[0] == ["30", "40", "50"], rows[0]
    assert rows[1] == ["6", "8", "6"], rows[1]
    assert rows[2] == ["4", "5", "3"], rows[2]
    assert rows[4] == ["0.500 [0.150, 0.850]", "0.200 [0.050, 0.600]", "1.000 [0.300, 1.000]"], rows[4]
    assert rows[5] == ["0.250, one-sided", "1.000, two-sided", NO_TEST], rows[5]
    assert rows[6] == ["not rejected", "not rejected", NO_TEST], rows[6]
    assert rows[8] == ["1 of 2", "2 of 4", NOT_IN_FILE], rows[8]
    assert rows[9] == ["0.500; 0.500, one-sided", "0.500; 0.375, two-sided", NOT_IN_FILE], rows[9]
    assert rows[13] == ["1 of 2", "2 of 5", "1 of 1"], rows[13]
    assert rows[15] == ["20; 20", "", ""], rows[15]
    assert rows[16] == ["12", "", ""] and rows[17] == ["4", "", ""] and rows[18] == ["4", "", ""]
    assert rows[19][0] == "not used by either rater; none"
    assert rows[20][0] == "0.400 [0.200, 0.600]", rows[20]
    assert rows[21][0] == "0.700 (14 of 20)", rows[21]
    assert rows[23][0] == "0.500 (16 pairs)", rows[23]
    assert rows[24][0] == "0.200 (4); 0.100 (2)", rows[24]
    assert rows[25][0] == "0.900; 0.800", rows[25]
    check_registered(h, b)

    md = markdown(rows, LABELS)
    paper_rows = [[c.strip() for c in ln.strip().strip("|").split("|")[1:4]] for ln in md.splitlines()[2:]]
    assert compare(rows, paper_rows) == [], "identical text must compare equal"
    mutated = [list(r) for r in paper_rows]
    mutated[0][0] = "166"
    diffs = compare(rows, mutated)
    assert len(diffs) == 1 and "row 1 column 1" in diffs[0], diffs

    tmp = Path(tempfile.mkdtemp(prefix="table6_selftest_"))
    paper = tmp / "paper.md"
    paper.write_text("<!-- @P id=T6 | synthetic -->\n**Table 6** caption\n" + md + "\n<!-- @P id=F3 -->\n",
                     encoding="utf-8")
    if t6_rows(paper.read_text(encoding="utf-8")) != paper_rows:
        raise AssertionError("parsing the synthetic paper block must return the rows that were printed")
    (tmp / "table6_human.md").write_text(md, encoding="utf-8")
    print("selftest table6_human: PASS")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    if args.selftest:
        run_selftest()
        return
    h = json.loads(read_checked(ROOT / HUMAN_REL, HUMAN_SHA))
    b = json.loads(read_checked(ROOT / BUILD_REL, BUILD_SHA))
    paper_text = read_checked(ROOT / PAPER_REL, PAPER_SHA).decode("utf-8")
    check_registered(h, b)
    rows = table_rows(h, b)
    md = markdown(rows, LABELS)
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / "table6_human.md"
    target.write_text(md, encoding="utf-8")
    print(md)
    print(f"output {target.name} sha256 {hashlib.sha256(target.read_bytes()).hexdigest()}")
    diffs = compare(rows, t6_rows(paper_text))
    for d in diffs:
        print(f"DIFF {d}")
    if diffs:
        fail(f"{len(diffs)} cell(s) differ from block T6 of paper.md")
    print("compare table6_human vs paper.md block T6: 0 differences")


if __name__ == "__main__":
    main()
