"""Paper B Fig. EF1 (FIGURE_TABLE_SPEC A3, online_resource.md block EF1): the standardised margin under f0,
|D_f0| / sd_boot(D_f0), of the comparisons CHANGED over F against those that are not (D and FL pooled).
Field names, margin, significance flag and inputs: SPEC_ADDENDUM_EF1.md items S1 to S7 (file::key evidence).
Before any figure is written, the two areas under the curve are recomputed and must equal RESULT.json and the
caption (0.8012 over all comparisons, 0.9546 over the 946 significant under f0; manifest n336, n339, n340).

Drawing choices ruled by CC-428 before any real margin was plotted (SPEC_ADDENDUM_EF1.md O1 to O5; constant RULED):
empirical cumulative distribution, linear horizontal axis from 0 with the upper limit left to matplotlib, no
area-under-the-curve value inside the figure, counts in the legend. They are not changed after the figure is seen.

Usage:  python3 figEF1.py [--out DIR]      build from the held RESULT.json, DEV.json, V.json (run on the rented host)
        python3 figEF1.py --selftest      synthetic input; asserts the join, the checks and the plotted values

Self-contained: each script in this folder carries its own helpers.
"""
import argparse
import hashlib
import json
import math
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
DEV_REL = ".session_backup/2026-11-13/b_stages/host_pull/20261113T174234Z/b_work/DEV.json"
DEV_SHA = "88ff39aa9552b671a0e439aec961d0fefe02df1f52a2a5df9765a9d8226f7e8d"
V_REL = ".session_backup/2026-11-13/b_stages/host_pull/20261113T174234Z/b_work/V.json"
V_SHA = "1f011538bf06a601c2104116ccef31f470eed473b2a96c9e6f8a5408f126f6b9"
INPUTS = {"RESULT.json": (RESULT_REL, RESULT_SHA), "DEV.json": (DEV_REL, DEV_SHA), "V.json": (V_REL, V_SHA)}
# CC-428 ruling 2, fixed before any real margin was plotted
RULED = {"form": "empirical cumulative distribution", "x_scale": "linear", "x_upper": "matplotlib autoscale",
         "auc_in_panel": False, "legend_counts": True}
DEFAULT_OUT = ROOT / "scripts/b_figs/out"
F0 = "rdr.tw.pk.cf"  # scripts/b_fecert/family.py:31, the committed protocol P0
# number_manifest_B_v2.tsv rows n090, n337, n338, n340, n336, n339
EXPECT = {"comparisons": 1123, "changed": 30, "not_changed": 1093, "significant_f0": 946,
          "printed_all": "0.8012", "printed_sig": "0.9546"}
AUC_TOL = 1e-12
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


def zval(s):
    """b_fecert.py zval(): |D| / sd_boot; s = [D, 2.5th pct, 97.5th pct, sd_boot]."""
    return abs(s[0]) / s[3] if s[3] > 0 else (math.inf if abs(s[0]) > 1e-9 else 0.0)


def sig(s):
    """b_fecert.py sig(): +1 if the 2.5th percentile > 0, -1 if the 97.5th < 0, else 0."""
    return 1 if s[1] > 0 else -1 if s[2] < 0 else 0


def auc(pos, neg):
    """b_fecert.py auc(): P(margin of a CHANGED comparison < margin of one not CHANGED), ties one half."""
    return sum((p < q) + 0.5 * (p == q) for p in pos for q in neg) / (len(pos) * len(neg))


def margins(result, dev, v):
    """Join RESULT.json::comparisons[i] with the f0 class of DEV.json::comparisons / V.json::fl on id."""
    scored = dev["comparisons"] + v["fl"]
    by_id = {c["id"]: c for c in scored}
    rows = result["comparisons"]
    ids = [r["id"] for r in rows]
    if len(by_id) != len(scored) or len(set(ids)) != len(ids):
        fail("a comparison id repeats")
    if set(ids) != set(by_id):
        fail("RESULT.json ids differ from DEV.json + V.json ids")
    out = []
    for r in rows:
        f0 = [cl["cider"] for cl in by_id[r["id"]]["classes"].values() if F0 in cl["members"]]
        if len(f0) != 1:
            fail(f"{r['id']}: {len(f0)} classes hold {F0}, expected 1")
        s = f0[0]
        if abs(s[0] - r["D_f0"]) > 1e-12:
            fail(f"{r['id']}: D_f0 differs from the stored f0 class")
        z = zval(s)
        if not math.isfinite(z):
            fail(f"{r['id']}: margin is not finite (sd_boot is 0)")
        if not isinstance(r["changed_F"], bool):
            fail(f"{r['id']}: changed_F is not a boolean")
        if r["changed_F"] and sig(s) == 0:
            fail(f"{r['id']}: CHANGED but not significant under f0")
        out.append({"id": r["id"], "z": z, "changed": r["changed_F"], "sig0": sig(s) != 0})
    return out


def check(rows, result, expect):
    pos = [r["z"] for r in rows if r["changed"]]
    neg = [r["z"] for r in rows if not r["changed"]]
    sig_rows = [r for r in rows if r["sig0"]]
    got = {"comparisons": len(rows), "changed": len(pos), "not_changed": len(neg), "significant_f0": len(sig_rows)}
    for k, n in got.items():
        if n != expect[k]:
            fail(f"{k}: {n}, expected {expect[k]}")
    a_all = auc(pos, neg)
    a_sig = auc([r["z"] for r in sig_rows if r["changed"]], [r["z"] for r in sig_rows if not r["changed"]])
    sec = result["secondary"]
    for name, val, key, printed in ((
            "all", a_all, "FE_PRED_AUC", expect["printed_all"]),
            ("sig", a_sig, "FE_PRED_AUC_f0_significant_EXTRA", expect["printed_sig"])):
        if abs(val - sec[key]) > AUC_TOL:
            fail(f"AUC {name}: recomputed {val!r}, RESULT.json::secondary.{key} = {sec[key]!r}")
        if f"{val:.4f}" != printed:
            fail(f"AUC {name}: recomputed {val:.4f}, caption prints {printed}")
        print(f"check AUC {name} {val!r} = secondary.{key}; printed {printed}")
    return pos, neg


def ecdf(values):
    xs = sorted(values)
    return xs, [(i + 1) / len(xs) for i in range(len(xs))]


def build(result, dev, v, expect):
    rows = margins(result, dev, v)
    pos, neg = check(rows, result, expect)
    fig, ax = plt.subplots(figsize=(5.0, 3.2))
    lines = {}
    for name, vals, style in (("CHANGED over F", pos, {"color": "black", "linestyle": "-"}),
                              ("not CHANGED over F", neg, {"color": "0.5", "linestyle": "--"})):
        xs, ys = ecdf(vals)
        (lines[name],) = ax.step(xs, ys, where="post", linewidth=1.2, label=f"{name} (n = {len(vals)})", **style)
    ax.set_xlabel(r"standardised margin under f0, $|D_{f0}|\,/\,\mathrm{sd_{boot}}(D_{f0})$")
    ax.set_ylabel("cumulative share of comparisons")
    ax.set_ylim(0, 1.02)
    ax.set_xscale(RULED["x_scale"])
    ax.set_xlim(left=0)
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    fig.tight_layout()
    check_text(fig)
    readback = {name: list(map(float, ln.get_xdata())) for name, ln in lines.items()}
    return fig, rows, readback


def synthetic():
    """7 comparisons. CHANGED margins 1, 2, 3; not CHANGED 2 (not significant), 4, 5, 6.
    AUC over all = (4 + 3.5 + 3) / 12 = 0.875 (one tie at 2); over the significant = 9 / 9 = 1."""
    spec = [("D:1", -1.0, 1.0, True, True), ("D:2", 2.0, 1.0, True, True), ("FL:3", 6.0, 2.0, True, True),
            ("D:4", 2.0, 1.0, False, False), ("D:5", 4.0, 1.0, False, True), ("D:6", -10.0, 2.0, False, True),
            ("FL:7", 6.0, 1.0, False, True)]
    dev, fl, res = [], [], []
    for cid, d, sd, changed, significant in spec:
        lo, hi = (d - 0.5, d + 0.5) if significant else (-0.1, 0.1)
        classes = {"k0": {"members": [F0, "syl.tw.pk.cf"], "cider": [d, lo, hi, sd]},
                   "k1": {"members": ["pyvi.tm.pa.ck"], "cider": [d / 3, -1.0, 1.0, 1.0]}}
        (fl if cid.startswith("FL:") else dev).append({"id": cid, "classes": classes})
        res.append({"id": cid, "D_f0": d, "changed_F": changed})
    result = {"comparisons": res, "secondary": {"FE_PRED_AUC": 0.875, "FE_PRED_AUC_f0_significant_EXTRA": 1.0}}
    expect = {"comparisons": 7, "changed": 3, "not_changed": 4, "significant_f0": 6,
              "printed_all": "0.8750", "printed_sig": "1.0000"}
    return result, {"comparisons": dev}, {"fl": fl}, expect


def must_fail(fn, what):
    try:
        fn()
    except SystemExit as exc:
        assert exc.code == 1, what
        return
    raise AssertionError(f"{what} must exit non-zero")


def run_selftest():
    result, dev, v, expect = synthetic()
    tmp = Path(tempfile.mkdtemp(prefix="figEF1_selftest_"))
    path = tmp / "RESULT.json"
    path.write_text(json.dumps(result), encoding="utf-8")
    must_fail(lambda: read_checked(path, "0" * 64), "a wrong sha")
    loaded = read_checked(path, hashlib.sha256(path.read_bytes()).hexdigest())
    fig, rows, readback = build(loaded, dev, v, expect)
    assert [r["z"] for r in rows] == [1.0, 2.0, 3.0, 2.0, 4.0, 5.0, 6.0]
    assert readback["CHANGED over F"] == [1.0, 2.0, 3.0], readback
    assert readback["not CHANGED over F"] == [2.0, 4.0, 5.0, 6.0], readback
    save(fig, "figEF1_selftest", tmp)
    for ext in ("pdf", "png"):
        assert (tmp / f"figEF1_selftest.{ext}").stat().st_size > 0

    def mutated(edit):
        r, d, vv, e = synthetic()
        edit(r, d, vv, e)
        return lambda: build(r, d, vv, e)

    def dup_f0(r, d, vv, e):
        d["comparisons"][0]["classes"]["k1"]["members"].append(F0)

    def no_f0(r, d, vv, e):
        d["comparisons"][0]["classes"]["k0"]["members"].remove(F0)

    def sd_zero(r, d, vv, e):
        d["comparisons"][1]["classes"]["k0"]["cider"][3] = 0.0

    def changed_not_sig(r, d, vv, e):
        d["comparisons"][0]["classes"]["k0"]["cider"][1:3] = [-0.1, 0.1]

    cases = {
        "a D_f0 mismatch": lambda r, d, vv, e: r["comparisons"][0].update(D_f0=-1.5),
        "a missing f0 class": no_f0,
        "a duplicate f0 class": dup_f0,
        "a missing comparison": lambda r, d, vv, e: vv["fl"].pop(),
        "a repeated id": lambda r, d, vv, e: r["comparisons"].append(dict(r["comparisons"][0])),
        "a zero sd_boot": sd_zero,
        "CHANGED without significance under f0": changed_not_sig,
        "an AUC that differs from RESULT.json": lambda r, d, vv, e: r["secondary"].update(FE_PRED_AUC=0.8751),
        "an AUC that differs from the caption": lambda r, d, vv, e: e.update(printed_sig="0.9999"),
        "a count that differs from the manifest": lambda r, d, vv, e: e.update(significant_f0=7),
        "a tie counted as a win": lambda r, d, vv, e: r["secondary"].update(FE_PRED_AUC=11 / 12),
    }
    for what, edit in cases.items():
        must_fail(mutated(edit), what)
    print(f"selftest figEF1: PASS ({len(cases) + 1} failure cases rejected)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    if args.selftest:
        run_selftest()
        return
    docs = {name: read_checked(ROOT / rel, sha) for name, (rel, sha) in INPUTS.items()}
    print(f"ruled {RULED}")
    fig, rows, _ = build(docs["RESULT.json"], docs["DEV.json"], docs["V.json"], EXPECT)
    for r in rows:
        print(f"plotted {r['id']} changed_F={r['changed']} margin={r['z']!r}")
    save(fig, "figEF1_margin", args.out)
    for text in sorted({t.get_text() for t in fig.findobj(Text) if t.get_text()}):
        print(f"text {text!r}")


if __name__ == "__main__":
    main()
