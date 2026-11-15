"""Paper B Fig. 2 (FIGURE_TABLE_SPEC A3, paper.md block F2): breaking classes by axis level, four series
(D over F_dev, FL over F_dev, D over F, FL over F). Input: RESULT.json only; the 46 counts of Table E2.
The two cells "not a member" (the level uts over the development family) are left empty, not drawn as zero.

Key paths are those of number_manifest_B_v2.tsv rows n091 to n136.

Usage:  python3 fig2_breaking.py [--out DIR]      build from the held RESULT.json (run on the rented host)
        python3 fig2_breaking.py --selftest      synthetic input; asserts the plotted counts

Self-contained: each script in this folder carries its own helpers.
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
RESULT_REL = ".session_backup/2026-11-13/b_stages/host_pull/20261113T174234Z/b_work/RESULT.json"
RESULT_SHA = "25614b469cf59dc61f15e839b89a8e78ca0b316905afc4bd2ae52eaa0d32b43a"
DEFAULT_OUT = ROOT / "scripts/b_figs/out"
ALL_LEVELS = ("syl", "rdr", "pyvi", "uts", "tw", "tm", "tf", "pk", "pf", "pa", "cf", "ck")
DEV_LEVELS = tuple(lv for lv in ALL_LEVELS if lv != "uts")  # the development family has no uts level
SERIES = (
    # (name, key prefix in RESULT.json, levels that are members)
    ("D over F_dev", "counts.D_over_F_dev_DEVELOPMENT.breaking_levels", DEV_LEVELS),
    ("FL over F_dev", "counts.FL_over_F_dev.breaking_levels", DEV_LEVELS),
    ("D over F", "counts.D_over_F_DEVELOPMENT.breaking_levels", ALL_LEVELS),
    ("FL over F", "counts.FL_over_F.breaking_levels", ALL_LEVELS),
)
STYLE = (
    {"color": "0.2", "hatch": ""},
    {"color": "0.5", "hatch": "//"},
    {"color": "#4477aa", "hatch": ".."},
    {"color": "#cc6677", "hatch": "xx"},
)
FORBIDDEN = re.compile(r"supported|underpowered|agrees more|equivalent|inconclusive|trend|\bPI\b|\bR2\b", re.I)


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


def lookup(doc, dotted):
    node = doc
    for part in dotted.split("."):
        if part not in node:
            return None
        node = node[part]
    return node


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


def build(result):
    counts = {}
    for name, prefix, members in SERIES:
        values = {}
        for lv in ALL_LEVELS:
            v = lookup(result, f"{prefix}.{lv}")
            if lv not in members:
                if v is not None:
                    fail(f"{name}: level {lv} is not a member but has a count")
                continue
            if not isinstance(v, int):
                fail(f"{name}: count for {lv} missing or not an integer")
            values[lv] = v
        counts[name] = values
    total = sum(len(v) for v in counts.values())
    if total != 46:
        fail(f"{total} counts, Table E2 has 46")

    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    width = 0.2
    handles = {}
    for k, (name, _, _) in enumerate(SERIES):
        xs, hs = [], []
        for i, lv in enumerate(ALL_LEVELS):
            if lv in counts[name]:
                xs.append(i + (k - 1.5) * width)
                hs.append(counts[name][lv])
        style = STYLE[k]
        handles[name] = ax.bar(xs, hs, width=width, color=style["color"], hatch=style["hatch"],
                               edgecolor="black", linewidth=0.5, label=name)
    ax.set_xticks(range(len(ALL_LEVELS)))
    ax.set_xticklabels(ALL_LEVELS)
    ax.set_xlabel("axis level")
    ax.set_ylabel("breaking comparisons (count)")
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.18), frameon=False, fontsize=8)
    fig.tight_layout()
    check_text(fig)

    readback = {}
    for name, _, _ in SERIES:
        level_of = {}
        for patch in handles[name].patches:
            idx = round(patch.get_x() + width / 2)
            level_of[idx] = patch.get_height()
        readback[name] = level_of
    return fig, counts, readback


def run_selftest():
    syn = {}
    for name, prefix, members in SERIES:
        node = {}
        for n_i, lv in enumerate(members):
            node[lv] = 7 * (n_i + 1) + len(name)
        parts = prefix.split(".")
        cur = syn
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = node
    tmp = Path(tempfile.mkdtemp(prefix="fig2_selftest_"))
    path = tmp / "RESULT.json"
    path.write_text(json.dumps(syn), encoding="utf-8")
    try:
        read_checked(path, "0" * 64)
        raise AssertionError("a wrong sha must exit non-zero")
    except SystemExit as exc:
        assert exc.code == 1
    loaded = read_checked(path, hashlib.sha256(path.read_bytes()).hexdigest())
    fig, counts, readback = build(loaded)
    for name, prefix, members in SERIES:
        for lv in members:
            expect = lookup(syn, f"{prefix}.{lv}")
            assert counts[name][lv] == expect, (name, lv)
            i = ALL_LEVELS.index(lv)
            assert readback[name][i] == expect, (name, lv, readback[name].get(i), expect)
        assert len(readback[name]) == len(members), name
    assert "uts" not in counts["D over F_dev"] and ALL_LEVELS.index("uts") not in readback["D over F_dev"]
    assert ALL_LEVELS.index("uts") in readback["D over F"], "uts is a member of the full family"
    save(fig, "fig2_breaking_selftest", tmp)
    for ext in ("pdf", "png"):
        assert (tmp / f"fig2_breaking_selftest.{ext}").stat().st_size > 0
    bad = json.loads(path.read_text(encoding="utf-8"))
    bad["counts"]["D_over_F_dev_DEVELOPMENT"]["breaking_levels"]["uts"] = 1
    try:
        build(bad)
        raise AssertionError("a count on a non-member cell must fail")
    except SystemExit:
        pass
    print("selftest fig2_breaking: PASS")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    if args.selftest:
        run_selftest()
        return
    result = read_checked(ROOT / RESULT_REL, RESULT_SHA)
    fig, counts, _ = build(result)
    for name, _, _ in SERIES:
        for lv in ALL_LEVELS:
            if lv in counts[name]:
                print(f"plotted {name} {lv} {counts[name][lv]}")
    save(fig, "fig2_breaking", args.out)


if __name__ == "__main__":
    main()
