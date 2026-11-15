"""Paper B Fig. 1 (FIGURE_TABLE_SPEC A3, paper.md block F1): the fixed order of the steps of a member and the
decision rule for one comparison over a family. Schematic; no data, no number, no input file.
Box labels follow the F1 placeholder of draft_v3/paper.md; the sub-steps of normalisation follow the paragraph
above it (paper.md l.88).

Usage:  python3 fig1_schematic.py [--out DIR]
        python3 fig1_schematic.py --selftest      draws into a temporary folder; asserts the step order and labels

Self-contained: each script in this folder carries its own helpers.
"""
import argparse
import hashlib
import re
import sys
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402
from matplotlib.text import Text  # noqa: E402

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["font.size"] = 8

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "scripts/b_figs/out"
FORBIDDEN = re.compile(r"supported|underpowered|agrees more|equivalent|inconclusive|trend|\bPI\b|\bR2\b|\d", re.I)
STEPS = (  # (label, dashed edge = applied at level pa only)
    ("normalisation\n(Unicode\ncomposition;\nunderscore to\nspace;\nwhitespace\ncollapsed and\ntrimmed)", False),
    ("tone\nplacement\n(T)", False),
    ("punctuation\nbefore\nthe unit\n(P)", False),
    ("unit\n(U)", False),
    ("case\n(C)", False),
    ("removal of\npunctuation\ntokens\n(level pa\nonly)", True),
    ("Unicode\ncomposition\nper token", False),
)
RULE_IN = "one comparison\n(a, b) over a family:\nsignificance of D\nunder each class"
OUTCOMES = (  # (verdict, condition, hatch, fill, x, width)
    ("CERTIFIED", "every class significant\nwith a above b,\nor every class\nwith b above a", "", "white", 2.9, 3.0),
    ("FRAGILE", "significant under\nsome classes only", "//", "0.85", 6.3, 4.4),
    ("NULL-STABLE", "significant\nunder none", "..", "white", 11.1, 3.1),
)
REVERSED = ("REVERSED", "significant in both\ndirections (a subset\nof FRAGILE)", "xx", "white")
WHITE = {"facecolor": "white", "edgecolor": "none", "pad": 1.5}


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def save(fig, stem, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        target = outdir / f"{stem}.{ext}"
        if ext == "pdf":
            fig.savefig(target, metadata={"CreationDate": None})
        else:
            fig.savefig(target, dpi=600, metadata={"Software": None})
        print(f"output {target.name} sha256 {hashlib.sha256(target.read_bytes()).hexdigest()}")


def check_text(fig):
    for t in fig.findobj(Text):
        if t.get_text() and FORBIDDEN.search(t.get_text()):
            fail(f"forbidden word or digit in figure text: {t.get_text()!r}")


def box(ax, x, y, w, h, dashed=False, hatch="", fill="white"):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor="black", hatch=hatch, linewidth=0.8,
                           linestyle="--" if dashed else "-"))


def label(ax, x, y, title, body, va="center"):
    """Bold title over a plain body, on a white ground so that hatching stays behind the words."""
    t = ax.text(x, y, title, ha="center", va="bottom" if va == "center" else "top", fontweight="bold", bbox=WHITE)
    b = ax.text(x, y - (0.05 if va == "center" else 0.45), body, ha="center", va="top", bbox=WHITE)
    return f"{title}\n{body}", (t, b)


def arrow(ax, x0, y0, x1, y1):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=8, linewidth=0.8,
                                 color="black", shrinkA=0, shrinkB=0))


def build():
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.set_xlim(0, 14.4)
    ax.set_ylim(0, 9.2)
    ax.axis("off")

    # upper row: outputs and references enter the same chain of steps
    ax.text(0.05, 9.0, "applied alike to system outputs and to references", ha="left", va="center",
            fontstyle="italic")
    src_x, w_src = 0.05, 1.35
    x, w_norm, w, gap, y, h = 1.75, 1.7, 1.45, 0.22, 5.0, 3.5
    for yc, text in ((7.4, "system\noutputs"), (6.1, "references")):
        box(ax, src_x, yc - 0.45, w_src, 0.9)
        ax.text(src_x + w_src / 2, yc, text, ha="center", va="center", fontsize=7)
        arrow(ax, src_x + w_src, yc, x, y + h / 2)
    step_texts = []
    for i, (text, dashed) in enumerate(STEPS):
        bw = w_norm if i == 0 else w
        box(ax, x, y, bw, h, dashed=dashed)
        step_texts.append(ax.text(x + bw / 2, y + h / 2, text, ha="center", va="center", fontsize=7))
        if i < len(STEPS) - 1:
            arrow(ax, x + bw, y + h / 2, x + bw + gap, y + h / 2)
        x += bw + gap
    ax.text(14.35, 4.65, "dashed edge: applied at level pa only", ha="right", va="center", fontsize=7)

    # lower row: the decision rule for one comparison over a family
    box(ax, 0.05, 0.9, 2.45, 2.2)
    rule_text = ax.text(1.275, 2.0, RULE_IN, ha="center", va="center", fontsize=7)
    bus_y, top = 3.95, 3.45
    ax.plot([1.275, 1.275, OUTCOMES[-1][4] + OUTCOMES[-1][5] / 2], [3.1, bus_y, bus_y], color="black", lw=0.8)
    verdict_texts = {}
    for verdict, cond, hatch, fill, bx, bw in OUTCOMES:
        box(ax, bx, 0.15, bw, top - 0.15, hatch=hatch, fill=fill)
        arrow(ax, bx + bw / 2, bus_y, bx + bw / 2, top)
        if verdict == "FRAGILE":
            verdict_texts[verdict], _ = label(ax, bx + bw / 2, top - 0.15, verdict, cond, va="top")
        else:
            verdict_texts[verdict], _ = label(ax, bx + bw / 2, 1.9, verdict, cond)
    rv, rc, rh, rf = REVERSED
    rx, rw = OUTCOMES[1][4] + 0.35, OUTCOMES[1][5] - 0.7
    box(ax, rx, 0.4, rw, 1.75, hatch=rh, fill=rf)
    verdict_texts[rv], _ = label(ax, rx + rw / 2, 1.35, rv, rc)
    fig.tight_layout()
    check_text(fig)
    return fig, [t.get_text() for t in step_texts], verdict_texts, rule_text


def run_selftest():
    fig, steps, verdicts, _ = build()
    assert steps == [label for label, _ in STEPS], steps
    order = ["normalisation", "tone", "punctuation", "unit", "case", "removal", "Unicode"]
    assert [s.split("\n")[0].split()[0] for s in steps] == order, steps
    assert sum("Unicode composition" in s.replace("\n", " ") for s in steps) == 2, "composition appears in normalisation and per token"
    assert set(verdicts) == {"CERTIFIED", "FRAGILE", "REVERSED", "NULL-STABLE"}
    assert "a subset of FRAGILE" in verdicts["REVERSED"].replace("\n", " ")
    tmp = Path(tempfile.mkdtemp(prefix="fig1_selftest_"))
    save(fig, "fig1_schematic_selftest", tmp)
    for ext in ("pdf", "png"):
        assert (tmp / f"fig1_schematic_selftest.{ext}").stat().st_size > 0
    bad = plt.figure()
    bad.text(0.5, 0.5, "a trend")
    try:
        check_text(bad)
        raise AssertionError("a forbidden word must fail")
    except SystemExit:
        pass
    print("selftest fig1_schematic: PASS")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    if args.selftest:
        run_selftest()
        return
    fig, steps, verdicts, _ = build()
    for s in steps:
        print("step", s.replace("\n", " "))
    for v in verdicts.values():
        print("rule", v.replace("\n", " "))
    save(fig, "fig1_schematic", args.out)


if __name__ == "__main__":
    main()
