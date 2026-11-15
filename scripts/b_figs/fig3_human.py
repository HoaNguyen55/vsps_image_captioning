"""Paper B Fig. 3 (FIGURE_TABLE_SPEC A1): human-arm consensus shares with their 95% Clopper-Pearson
intervals, and each rater's own share in the two hypothesis strata. Input: HUMAN.json only.

Usage:  python3 fig3_human.py [--out DIR]      build from the held HUMAN.json (run on the rented host)
        python3 fig3_human.py --selftest      build from a synthetic input made here; asserts the plotted values

Self-contained (no import from a sibling file): each script in this folder carries its own helpers.
"""
import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.text import Text  # noqa: E402

plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["font.size"] = 9

ROOT = Path(__file__).resolve().parents[2]
HUMAN_REL = ".session_backup/2026-11-13/b_stages/host_pull/H_20261115T083124Z/b_work/HUMAN.json"
HUMAN_SHA = "990a0df51ba3e35349fbe2dcf37826150ce9d5c3aa88b3e375c697377f745057"
DEFAULT_OUT = ROOT / "scripts/b_figs/out"
STRATA = ("P", "U", "C")
RATERS_ALONE = ("R2", "PI")  # non-author, author; no row exists for stratum C
FORBIDDEN = re.compile(r"supported|underpowered|agrees more|equivalent|inconclusive|trend|\bPI\b|\bR2\b", re.I)
POSITION = {"P": "Punctuation flip (P)", "U": "Unit flip (U)", "C": "Control (C)"}


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def read_checked(path, sha):
    data = path.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if got != sha:
        fail(f"sha256 of {path.name} is {got}, expected {sha}")
    print(f"input {path.name} sha256 {got} ok")
    return json.loads(data)


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
            fail(f"forbidden word in figure text: {t.get_text()!r}")


def build(h):
    if h["gate"] != "low inter-rater agreement":
        fail(f"gate is {h['gate']!r}")
    if h["raters"] != ["PI", "R2"]:
        fail(f"raters are {h['raters']!r}")
    xs = list(range(len(STRATA)))
    q, lows, highs = [], [], []
    for s in STRATA:
        st = h["strata"][s]
        if abs(st["q"] - st["k_word"] / st["n_dec"]) > 1e-9:
            fail(f"stratum {s}: q is not k_word / n_dec")
        q.append(st["q"])
        lows.append(st["q"] - st["ci95"][0])
        highs.append(st["ci95"][1] - st["q"])

    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    cons = ax.errorbar(xs, q, yerr=[lows, highs], fmt="o", color="black", ecolor="black",
                       capsize=4, markersize=6, label="both raters (consensus)")
    alone_x = {"R2": -0.15, "PI": 0.15}
    alone_mark = {"R2": ("s", "white", "non-author rater alone"), "PI": ("^", "0.6", "author rater alone")}
    alone_plotted = {}
    alone_lines = {}
    for r in RATERS_ALONE:
        pos, vals = [], []
        for i, s in enumerate(STRATA):
            if s not in h["rater_alone"][r]:  # stratum C: no row in HUMAN.json, so no mark
                continue
            row = h["rater_alone"][r][s]
            pos.append(xs[i] + alone_x[r])
            vals.append(row["k_word"] / row["n"])
        marker, face, label = alone_mark[r]
        line = ax.plot(pos, vals, ls="none", marker=marker, markersize=7, mfc=face, mec="black", label=label)[0]
        alone_lines[r] = line
        alone_plotted[r] = vals
    ax.axhline(0.5, color="0.35", ls=":", lw=1)
    ax.set_ylim(0, 1)
    ax.set_ylabel("share of pairs that match")
    ax.set_xticks(xs)
    ax.set_xticklabels([f"{POSITION[s]}\n{h['strata'][s]['k_word']} of {h['strata'][s]['n_dec']}" for s in STRATA])
    ax.legend(loc="upper right", frameon=False, fontsize=8)
    fig.tight_layout()
    check_text(fig)

    segments = cons.lines[2][0].get_segments()
    readback = {
        "consensus_points": [round(float(v), 12) for v in cons.lines[0].get_ydata()],
        "consensus_intervals": [(round(float(min(seg[:, 1])), 12), round(float(max(seg[:, 1])), 12)) for seg in segments],
        "rater_alone": {r: [round(float(v), 12) for v in alone_lines[r].get_ydata()] for r in RATERS_ALONE},
        "rater_alone_x": {r: [round(float(v), 12) for v in alone_lines[r].get_xdata()] for r in RATERS_ALONE},
    }
    plotted = {"q": q, "ci": [(h["strata"][s]["ci95"][0], h["strata"][s]["ci95"][1]) for s in STRATA],
               "alone": alone_plotted}
    return fig, readback, plotted


def run_selftest():
    syn = {
        "gate": "low inter-rater agreement",
        "raters": ["PI", "R2"],
        "strata": {
            "P": {"k_word": 2, "n_dec": 5, "q": 0.4, "ci95": [0.1, 0.7]},
            "U": {"k_word": 6, "n_dec": 10, "q": 0.6, "ci95": [0.4, 0.8]},
            "C": {"k_word": 1, "n_dec": 4, "q": 0.25, "ci95": [0.1, 0.5]},
        },
        "rater_alone": {
            "R2": {"P": {"k_word": 2, "n": 5}, "U": {"k_word": 5, "n": 9}},
            "PI": {"P": {"k_word": 4, "n": 8}, "U": {"k_word": 3, "n": 6}},
        },
    }
    tmp = Path(tempfile.mkdtemp(prefix="fig3_selftest_"))
    path = tmp / "HUMAN.json"
    path.write_text(json.dumps(syn), encoding="utf-8")
    try:
        read_checked(path, "0" * 64)
        raise AssertionError("a wrong sha must exit non-zero")
    except SystemExit as exc:
        assert exc.code == 1
    loaded = read_checked(path, hashlib.sha256(path.read_bytes()).hexdigest())
    fig, readback, plotted = build(loaded)
    expect_points = [0.4, 0.6, 0.25]
    assert readback["consensus_points"] == expect_points, readback["consensus_points"]
    assert readback["consensus_intervals"] == [(0.1, 0.7), (0.4, 0.8), (0.1, 0.5)], readback["consensus_intervals"]
    assert readback["rater_alone"]["R2"] == [round(2 / 5, 12), round(5 / 9, 12)]
    assert readback["rater_alone"]["PI"] == [round(4 / 8, 12), round(3 / 6, 12)]
    assert readback["rater_alone_x"]["R2"] == [-0.15, 0.85], readback["rater_alone_x"]
    assert readback["rater_alone_x"]["PI"] == [0.15, 1.15], readback["rater_alone_x"]
    assert len(readback["rater_alone"]["R2"]) == 2, "no rater-alone mark may be drawn for stratum C"
    save(fig, "fig3_human_selftest", tmp)
    for ext in ("pdf", "png"):
        assert (tmp / f"fig3_human_selftest.{ext}").stat().st_size > 0
    bad = dict(syn, gate="supported")
    try:
        build(bad)
        raise AssertionError("gate check must fail")
    except SystemExit:
        pass
    print("selftest fig3_human: PASS")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    if args.selftest:
        run_selftest()
        return
    h = read_checked(ROOT / HUMAN_REL, HUMAN_SHA)
    fig, readback, plotted = build(h)
    for i, s in enumerate(STRATA):
        print(f"plotted consensus {s} {plotted['q'][i]:.3f} interval {plotted['ci'][i][0]:.3f} {plotted['ci'][i][1]:.3f}")
    for r in RATERS_ALONE:
        for s, v in zip([x for x in STRATA if x in h["rater_alone"][r]], plotted["alone"][r]):
            print(f"plotted rater_alone {r} {s} {v:.3f}")
    save(fig, "fig3_human", args.out)


if __name__ == "__main__":
    main()
