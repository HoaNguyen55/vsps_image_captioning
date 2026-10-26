"""Paper A figures (PD-29 (b)): Fig. 2 and Fig. 4, drawn only from number_manifest.tsv values.

Every plotted number is looked up by its (source file, JSON key) row in
manuscript/journal_draft/number_manifest.tsv; nothing is typed in here. Output: SVG figures
and figs/VALUES.json (value, manifest row, file, key) for the verifier. Standard library only.

Run from the repo root:  python3 scripts/figures/paperA_figs.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "manuscript/journal_draft/number_manifest.tsv"
OUT = ROOT / "manuscript/journal_draft/figs"
NUM = re.compile(r"[-+−]?\d+(?:\.\d+)?")

XM = ".session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json"
XMK = "matcher_v2_tone_normalised.n1_f1_vs_logM_slopes."
COCO = ".session_backup/2026-10-26/a_full5000/out/r4_full5000_all9.json"  # r4, 9 systems x 5,000 (FILL_RULE)
COK = "gold."
H3 = ".session_backup/2026-10-14/r12/H3/out/n1_results.json"
UV = ".session_backup/2026-10-14/r11_verify/c2_n1_uitviic_mstar.json"
UVK = "uitviic_test.lexicons.{lex}.gold_variants.{g}.groups.all_10."
G2B = "data/results/g2b/g2b_score.json"
NF1 = "data/results/n_f1/bracket_result.json"
A33 = ".session_backup/2026-10-26/a_full5000/out/a33_r4_full5000_all9.json"  # A3.3 bootstrap re-run on r4
W4S = ".session_backup/2026-10-26/a_full5000/out/w4_summary.json"


def load_manifest():
    rows = {}
    for i, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        f = line.split("\t")
        if i == 1 or len(f) != 6 or f[1] != "A":
            continue
        rows.setdefault((f[2], f[3]), []).append((i, f[0]))
    return rows


ROWS = load_manifest()
USED = []


def get(file, key, what):
    """Numbers of the unique manifest row (file, key); records it in VALUES.json."""
    hits = ROWS.get((file, key), [])
    assert len(hits) == 1, f"manifest row for {file} :: {key}: {len(hits)} hits"
    row, text = hits[0]
    nums = [float(x.replace("−", "-")) for x in NUM.findall(text.split(" (")[0])]
    assert nums, f"no number in manifest row {row}: {text}"
    USED.append({"what": what, "manifest_row": row, "manifest_text": text, "file": file, "key": key, "values": nums})
    return nums


def pt_ci(pfile, pkey, cfile, ckey, what):
    """Point and CI, from one row (point [lo, hi]) or from two rows."""
    if ckey is None:
        v = get(pfile, pkey, what)
        assert len(v) == 3, (what, v)
        return tuple(v)
    p = get(pfile, pkey, what + " (point)")
    c = get(cfile, ckey, what + " (95% CI)")
    assert len(p) == 1 and len(c) == 2, (what, p, c)
    return p[0], c[0], c[1]


# ---------- SVG helpers ----------
def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="11">\n<rect width="{w}" height="{h}" fill="white"/>\n'
            + "\n".join(body) + "\n</svg>\n")


def text(x, y, s, anchor="middle", size=11, rot=None, style=""):
    t = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}"{t} {style}>{s}</text>'


def marker(kind, x, y, filled=True, color="#222"):
    fill = color if filled else "white"
    if kind == "circle":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{fill}" stroke="{color}" stroke-width="1.3"/>'
    if kind == "square":
        return f'<rect x="{x-4:.1f}" y="{y-4:.1f}" width="8" height="8" fill="{fill}" stroke="{color}" stroke-width="1.3"/>'
    if kind == "diamond":
        return (f'<polygon points="{x:.1f},{y-5:.1f} {x+5:.1f},{y:.1f} {x:.1f},{y+5:.1f} {x-5:.1f},{y:.1f}" '
                f'fill="{fill}" stroke="{color}" stroke-width="1.3"/>')
    return (f'<polygon points="{x:.1f},{y-5:.1f} {x+5:.1f},{y+4:.1f} {x-5:.1f},{y+4:.1f}" '
            f'fill="{fill}" stroke="{color}" stroke-width="1.3"/>')


def whisker(x, y0, y1, color="#222"):
    return (f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y1:.1f}" stroke="{color}" stroke-width="1"/>'
            f'<line x1="{x-3:.1f}" y1="{y0:.1f}" x2="{x+3:.1f}" y2="{y0:.1f}" stroke="{color}"/>'
            f'<line x1="{x-3:.1f}" y1="{y1:.1f}" x2="{x+3:.1f}" y2="{y1:.1f}" stroke="{color}"/>')


# ---------- Fig. 2: slope of F1 on ln M by gold rung ----------
SHORT = {"COCO-5000": ("COCO-5000", "Vietnamese outputs"), "LVLMs, OPERA release": ("English LVLMs", "OPERA release"),
         "LVLMs, Less-is-More release": ("English LVLMs", "Less-is-More"), "UIT-ViIC, COCO-80 lexicon": ("UIT-ViIC", "COCO-80 lexicon"),
         "UIT-ViIC, Vietnamese lexicon": ("UIT-ViIC", "Vietnamese lexicon"), "XM3600 (Section 7.5)": ("XM3600", "Section 7.5"),
         "2nd backbone, cv295": ("cv295", "discovery images"), "2nd backbone, uv231": ("uv231", "UIT-ViIC test"),
         "2nd backbone, xm600": ("xm600", "XM3600 images")}

def fig2_data():
    def uv(lex, g, what):
        k = UVK.format(lex=lex, g=g)
        return pt_ci(UV, k + "slope_F1_mixed_per_logM", UV, k + "slope_F1_mixed_ci95", what)

    fams = [
        ("COCO-5000", "exploratory", "instance labels", [
            pt_ci(COCO, COK + "refs1_randk.slope", COCO, COK + "refs1_randk.slope_ci", "COCO-5000 1 ref"),
            pt_ci(COCO, COK + "refs5_randk.slope", COCO, COK + "refs5_randk.slope_ci", "COCO-5000 5 refs"),
            pt_ci(COCO, COK + "inst.slope", COCO, COK + "inst.slope_ci", "COCO-5000 label gold")], None),
    ]
    for fam, name in (("F-B", "LVLMs, OPERA release"), ("F-C", "LVLMs, Less-is-More release")):
        k = f"families.{fam}.gold."
        fams.append((name, "exploratory", "instance labels", [
            pt_ci(H3, k + "refs1_randk.slope", H3, k + "refs1_randk.slope_ci", f"{name} 1 ref"),
            pt_ci(H3, k + "refs5_randk.slope", H3, k + "refs5_randk.slope_ci", f"{name} 5 refs"),
            pt_ci(H3, k + "inst.slope", H3, k + "inst.slope_ci", f"{name} label gold")], None))
    for lex, name in (("coco80", "UIT-ViIC, COCO-80 lexicon"), ("vi_objects_in", "UIT-ViIC, Vietnamese lexicon")):
        fams.append((name, "exploratory", "instance labels", [
            uv(lex, "refs1_randk", f"{name} 1 ref"), uv(lex, "refs5_randk", f"{name} 5 refs"),
            uv(lex, "inst_only", f"{name} label gold")], None))
    fams.append(("XM3600 (Section 7.5)", "registered", "human-verified labels, verified precision", [
        pt_ci(XM, XMK + "refs1_randk.slope_F1_per_logM", XM, XMK + "refs1_randk.slope_ci95_b500", "XM3600 1 ref"),
        pt_ci(XM, XMK + "refs_all.slope_F1_per_logM", XM, XMK + "refs_all.slope_ci95_b500", "XM3600 all 2-3 refs"),
        pt_ci(XM, XMK + "oiv7_verified.slope_F1_per_logM", XM, XMK + "oiv7_verified.slope_ci95_b500", "XM3600 label gold")],
        pt_ci(NF1, "sets.s75.slopes.lower.{point_4dp,ci95_2dp}", None, None, "XM3600 post hoc lower bound (N-F1)")))
    for st, lab, gold in (("cv295", "2nd backbone, cv295", "instance labels"), ("uv231", "2nd backbone, uv231", "instance labels"),
                          ("xm600", "2nd backbone, xm600", "human-verified labels, verified precision")):
        lb = pt_ci(NF1, "sets.xm600.slopes.lower.{point,ci95}", None, None, "xm600 post hoc lower bound (N-F1)") if st == "xm600" else None
        fams.append((lab, "registered", gold, [
            pt_ci(G2B, f"datasets.{st}.predictions.G2B-E1.parts[0].{{point,ci95}}", None, None, f"{lab} 1 ref"),
            None,
            pt_ci(G2B, f"datasets.{st}.predictions.G2B-E2.parts[0].{{point,ci95}}", None, None, f"{lab} label gold")], lb))
    return fams


def fig2(fams):
    W, H, L, R, T, B = 900, 430, 70, 20, 20, 110
    lo = min(c[1] for f in fams for c in f[3] + [f[4]] if c) - 3
    hi = max(c[2] for f in fams for c in f[3] + [f[4]] if c) + 3
    y = lambda v: T + (hi - v) / (hi - lo) * (H - T - B)
    gw = (W - L - R) / len(fams)
    body = [f'<line x1="{L}" y1="{y(0):.1f}" x2="{W-R}" y2="{y(0):.1f}" stroke="#999" stroke-dasharray="4 3"/>',
            f'<line x1="{L}" y1="{T}" x2="{L}" y2="{H-B}" stroke="#222"/>']
    for t in range(int(lo // 10) * 10, int(hi) + 1, 10):
        if lo <= t <= hi:
            body += [f'<line x1="{L-4}" y1="{y(t):.1f}" x2="{L}" y2="{y(t):.1f}" stroke="#222"/>', text(L - 7, y(t) + 4, str(t), "end")]
    body.append(text(18, (T + H - B) / 2, "slope of F1 (points) on ln M, 95% interval", rot=-90))
    kinds = ("circle", "square", "triangle")
    for gi, (name, grade, gold, pts, lb) in enumerate(fams):
        x0 = L + gi * gw + gw / 2
        xs = [x0 - 18, x0, x0 + 18]
        prev = None
        for j, c in enumerate(pts):
            if c is None:
                continue
            filled = not (j == 2 and gold.startswith("human"))
            body += [whisker(xs[j], y(c[1]), y(c[2])), marker(kinds[j], xs[j], y(c[0]), filled)]
            if prev:
                body.append(f'<line x1="{prev[0]:.1f}" y1="{prev[1]:.1f}" x2="{xs[j]:.1f}" y2="{y(c[0]):.1f}" stroke="#777" stroke-width="0.8"/>')
            prev = (xs[j], y(c[0]))
        if lb:
            body += [whisker(x0 + 30, y(lb[1]), y(lb[2]), "#888"), marker("diamond", x0 + 30, y(lb[0]), True, "#888")]
        short, sub = SHORT[name]
        body.append(text(x0, H - B + 16, short, "middle", 10))
        body.append(text(x0, H - B + 28, sub, "middle", 9))
        body.append(text(x0, H - B + 40, f"({grade})", "middle", 9, style='fill="#555"'))
    body.append(f'<line x1="{L + 6.1*gw:.1f}" y1="{H-B+46}" x2="{L + 8.9*gw:.1f}" y2="{H-B+46}" stroke="#555"/>')
    body.append(text(L + 7.5 * gw, H - B + 58, "second backbone (Qwen3-VL-8B, Section 7.6)", "middle", 9))
    lx, ly = L + 10, H - 18
    leg = [("circle", True, "#222", "one random reference"), ("square", True, "#222", "all references (5; XM3600: 2-3)"),
           ("triangle", True, "#222", "label gold: COCO instance labels"),
           ("triangle", False, "#222", "label gold: human-verified labels, verified precision"),
           ("diamond", True, "#888", "post hoc lower bound (unverifiable mentions = errors)")]
    for i, (k, f, col, lab) in enumerate(leg):
        cx = lx + (i % 3) * 280
        cy = ly - (12 if i < 3 else -4)
        body += [marker(k, cx, cy, f, col), text(cx + 9, cy + 4, lab, "start", 10)]
    return svg(W, H, body)


# ---------- Fig. 4: Lambda_k(M0) and the b-channel share, COCO-5000 ----------
def fig4_data():
    k = "bootstrap.gold."
    f = A33
    golds = [("refs1_randk", "1"), ("refs2_randk", "2"), ("refs3_randk", "3"), ("refs4_randk", "4"),
             ("refs5_randk", "5"), ("inst", "label|gold"), ("inst+refs5", "label gold|+ 5 refs")]
    lam = [(lab, pt_ci(f, k + g + ".Lambda_U.point", f, k + g + ".Lambda_U.ci", f"Lambda_U {g}")) for g, lab in golds]
    sh = [("1 → 5 references", pt_ci(W4S, "cells.r4_full5000_all9.channel_share.refs1_to_refs5",
                                       A33, "bootstrap.shares.refs1_to_refs5.b_channel_share.ci",
                                       "b-channel share 1->5")),
          ("1 reference → label gold", pt_ci(W4S, "cells.r4_full5000_all9.channel_share.refs1_to_inst",
                                              A33, "bootstrap.shares.refs1_to_inst.b_channel_share.ci",
                                              "b-channel share 1->label gold"))]
    return lam, sh


def fig4(lam, sh):
    W, H = 900, 350
    body = []
    # panel a
    L, R, T, B = 70, 470, 30, 280
    lo, hi = min(c[1] for _, c in lam) - 0.2, max(c[2] for _, c in lam) + 0.2
    y = lambda v: T + (hi - v) / (hi - lo) * (B - T)
    step = (R - L) / len(lam)
    body += [f'<line x1="{L}" y1="{y(0):.1f}" x2="{R}" y2="{y(0):.1f}" stroke="#999" stroke-dasharray="4 3"/>',
             f'<line x1="{L}" y1="{T}" x2="{L}" y2="{B}" stroke="#222"/>', text(L, T - 10, "(a) Λ_k(M0) with Ḡ(k) = U(k)", "start", 11)]
    t = 0.0
    while t <= hi:
        body += [f'<line x1="{L-4}" y1="{y(t):.1f}" x2="{L}" y2="{y(t):.1f}" stroke="#222"/>', text(L - 7, y(t) + 4, f"{t:.1f}", "end")]
        t += 0.5
    for i, (lab, c) in enumerate(lam):
        x = L + step * (i + 0.5)
        body += [whisker(x, y(c[1]), y(c[2])), marker("circle", x, y(c[0]))]
        for j, part in enumerate(lab.split("|")):
            body.append(text(x, B + 16 + 11 * j, part, "middle", 9))
    body.append(text((L + R) / 2, B + 44, "gold: k random references, then label gold (COCO instance labels)", "middle", 10))
    # panel b
    L2, R2 = 560, 860
    x = lambda v: L2 + v * (R2 - L2)
    body += [text(L2, T - 10, "(b) b-channel share of the rise in Λ", "start", 11),
             f'<line x1="{L2}" y1="{B}" x2="{R2}" y2="{B}" stroke="#222"/>']
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        body += [f'<line x1="{x(v):.1f}" y1="{B}" x2="{x(v):.1f}" y2="{B+4}" stroke="#222"/>', text(x(v), B + 16, f"{v:.2f}")]
    for i, (lab, c) in enumerate(sh):
        yy = T + 70 + i * 90
        body += [f'<rect x="{L2}" y="{yy-12}" width="{x(c[0])-L2:.1f}" height="24" fill="#bbb"/>',
                 f'<line x1="{x(c[1]):.1f}" y1="{yy}" x2="{x(c[2]):.1f}" y2="{yy}" stroke="#222" stroke-width="1.3"/>',
                 text(L2, yy - 18, lab, "start", 10)]
    body.append(text((L2 + R2) / 2, B + 44, "share (point, post hoc 95% interval)", "middle", 10))
    return svg(W, H, body)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fams = fig2_data()
    for _, _, _, pts, lb in fams:
        for c in [p for p in pts if p] + ([lb] if lb else []):
            assert c[1] <= c[0] <= c[2], c  # every point inside its interval
    (OUT / "fig2_slope_by_gold.svg").write_text(fig2(fams), encoding="utf-8")
    lam, sh = fig4_data()
    assert all(a[1][0] <= b[1][0] for a, b in zip(lam[:5], lam[1:6])), "Lambda not monotone over references"
    (OUT / "fig4_lambda_channels.svg").write_text(fig4(lam, sh), encoding="utf-8")
    doc = {"script": "scripts/figures/paperA_figs.py", "manifest": "manuscript/journal_draft/number_manifest.tsv",
           "rule": "every plotted value is read from the unique manifest row (file, key) listed here (PD-29 (b))",
           "figures": ["figs/fig2_slope_by_gold.svg", "figs/fig4_lambda_channels.svg"], "values": USED}
    (OUT / "VALUES.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote 2 figures, {len(USED)} manifest lookups")


if __name__ == "__main__":
    main()
