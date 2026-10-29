#!/usr/bin/env python3
"""Paper B Figures 5.1 (panel-swap design) and 5.2 (per-seed CIDEr-D against both panels), as plain SVG.

    python3 manuscript/journal_draft_B/figs/make_figs_B.py

The only input is fig_values_B.json (numbers only; slopes gated to the decided D0 / B-R1 values by
scripts/b_r1/fig_values.py). No caption text is read.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
V = json.loads((HERE / "fig_values_B.json").read_text(encoding="utf-8"))
K_COL, O_COL, INK, MUTED = "#1f5fa8", "#c4621b", "#222222", "#666666"
FONT = 'font-family="Helvetica, Arial, sans-serif"'


def text(x, y, s, size=12, anchor="middle", fill=INK, weight="normal"):
    return f'<text x="{x:.1f}" y="{y:.1f}" {FONT} font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}">{s}</text>'


def box(x, y, w, h, lines, stroke=INK, fill="#ffffff"):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>']
    for i, s in enumerate(lines):
        out.append(text(x + w / 2, y + 20 + 16 * i, s, 12, weight="bold" if i == 0 else "normal"))
    return out


def arrow(x1, y1, x2, y2, col=INK):
    return [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="1.4" marker-end="url(#a)"/>']


def design() -> str:
    W, H = 760, 330
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
         f'<path d="M0,0 L8,4 L0,8 z" fill="{INK}"/></marker></defs>', f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    p += box(20, 125, 170, 64, ["KTVIC training images", "outside dev300", "(nested subsets)"])
    p += box(250, 30, 230, 80, ["Forward direction", "one KTVIC caption per image", "216–3,469 images, 3 seeds"], K_COL, "#eef3fa")
    p += box(250, 205, 230, 80, ["Reverse direction", "one OpenViIC caption, same image", "216–1,734 images, 2 seeds"], O_COL, "#fbf1ea")
    p += arrow(190, 145, 248, 75) + arrow(190, 170, 248, 240)
    p += box(540, 115, 200, 84, ["187 dev300 images", "scored against both panels", "(same k references each)"])
    p += arrow(480, 70, 538, 140) + arrow(480, 245, 538, 175)
    p += [text(640, 232, "KTVIC references", 12, fill=K_COL, weight="bold"),
          text(640, 250, "OpenViIC captions", 12, fill=O_COL, weight="bold"),
          text(640, 280, "slope per doubling of training images,", 11, fill=MUTED),
          text(640, 296, "own panel vs other panel", 11, fill=MUTED)]
    return "\n".join(p + ["</svg>"])


def marker(seed, x, y, col):
    """Per-seed marker shape (readable in greyscale): 42 circle, 43 square, 44 triangle."""
    if seed == 42:
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{col}"/>'
    if seed == 43:
        return f'<rect x="{x - 3.2:.1f}" y="{y - 3.2:.1f}" width="6.4" height="6.4" fill="#ffffff" stroke="{col}" stroke-width="1.4"/>'
    return f'<path d="M{x:.1f},{y - 4:.1f} L{x + 3.8:.1f},{y + 3:.1f} L{x - 3.8:.1f},{y + 3:.1f} z" fill="{col}"/>'


def curves() -> str:
    W, H, pw, ph, top, left = 780, 360, 300, 230, 40, 70
    xs = {**{k: math.log2(n) for k, n in V["N"].items()}}
    x0, x1, y0, y1 = 7.5, 12.0, 40, 160
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    dash = {42: "", 43: 'stroke-dasharray="6 3"', 44: 'stroke-dasharray="2 3"'}
    for j, (key, title, own, other) in enumerate((("forward", "Trained on KTVIC captions (forward)", "K", "O"),
                                                 ("reverse", "Trained on OpenViIC captions (reverse)", "O", "K"))):
        ox = left + j * (pw + 110)
        X = lambda v: ox + (v - x0) / (x1 - x0) * pw  # noqa: E731
        Y = lambda v: top + ph - (v - y0) / (y1 - y0) * ph  # noqa: E731
        p.append(f'<rect x="{ox}" y="{top}" width="{pw}" height="{ph}" fill="none" stroke="#bbbbbb"/>')
        for g in range(40, 161, 20):
            p.append(f'<line x1="{ox}" y1="{Y(g):.1f}" x2="{ox + pw}" y2="{Y(g):.1f}" stroke="#eeeeee"/>')
            p.append(text(ox - 6, Y(g) + 4, str(g), 10, "end", MUTED))
        for n in (216, 433, 867, 1734, 3469):
            p.append(text(X(math.log2(n)), top + ph + 16, f"{n:,}", 10, fill=MUTED))
        p.append(text(ox + pw / 2, top - 12, title, 12, weight="bold"))
        p.append(text(ox + pw / 2, top + ph + 34, "training images (log scale)", 11, fill=MUTED))
        runs = V[key]
        seeds = sorted({int(r.split("_")[1][1:]) for r in runs})
        for panel, col in ((own, K_COL if own == "K" else O_COL), (other, K_COL if other == "K" else O_COL)):
            for s in seeds:
                pts = sorted((xs[r.split("_")[2]], v[panel]) for r, v in runs.items() if r.split("_")[1] == f"s{s}")
                d = " ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in pts)
                p.append(f'<polyline points="{d}" fill="none" stroke="{col}" stroke-width="1.6" {dash[s]}/>')
                p += [marker(s, X(a), Y(b), col) for a, b in pts]
    p.append(f'<g transform="translate(22 {top + ph / 2}) rotate(-90)">{text(0, 0, "mean CIDEr-D, 187 dev300 images", 11, fill=MUTED)}</g>')
    ly = H - 18
    p += [f'<line x1="70" y1="{ly - 4}" x2="95" y2="{ly - 4}" stroke="{K_COL}" stroke-width="2"/>',
          text(100, ly, "against KTVIC references", 11, "start", K_COL),
          f'<line x1="280" y1="{ly - 4}" x2="305" y2="{ly - 4}" stroke="{O_COL}" stroke-width="2"/>',
          text(310, ly, "against OpenViIC captions", 11, "start", O_COL),
          text(490, ly, "seed 42 solid ●, 43 dashed □, 44 dotted ▲", 11, "start", MUTED)]
    return "\n".join(p + ["</svg>"])


if __name__ == "__main__":
    (HERE / "fig5_1_panel_swap_design.svg").write_text(design() + "\n", encoding="utf-8")
    (HERE / "fig5_2_scaling_two_panels.svg").write_text(curves() + "\n", encoding="utf-8")
    print("wrote fig5_1_panel_swap_design.svg, fig5_2_scaling_two_panels.svg")
