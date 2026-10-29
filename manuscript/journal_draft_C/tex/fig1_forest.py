"""Figure 1 of Paper C: ret - rand per backbone and pooled on the four scored test sets (values from Tables 7, 8, 19).
Every value string must be a `number` row of number_manifest_C.tsv (ASCII minus there). Writes an SVG."""
import sys
from pathlib import Path
MAN = Path("/mnt/d/vsps_image_captioning/manuscript/journal_draft_C/number_manifest_C.tsv")
have = {l.split("\t")[0].lstrip("+") for l in MAN.read_text().splitlines()[1:]}
SETS = [  # (label, scorer, [(series, point, lo, hi)])
    ("OpenViIC test (1,941)", "stripped CIDEr-D", [("Qwen2.5-VL", "8.33", "7.01", "9.76"), ("InternVL3", "0.66", "-0.68", "1.99"), ("pooled", "4.49", "3.52", "5.57")]),
    ("XM3600 Vi test (2,500)", "stripped CIDEr-D", [("Qwen2.5-VL", "3.15", "1.50", "4.93"), ("InternVL3", "-1.75", "-3.35", "-0.09"), ("pooled", "0.70", "-0.45", "1.97")]),
    ("COCO Karpathy test (5,000)", "PTB CIDEr-D", [("Qwen2.5-VL", "7.80", "6.40", "9.17"), ("InternVL3", "-1.64", "-2.79", "-0.49"), ("pooled", "3.08", "2.08", "4.03")]),
    ("NoCaps val (4,500)", "PTB CIDEr-D", [("Qwen2.5-VL", "2.83", "1.69", "3.98"), ("InternVL3", "0.62", "-0.37", "1.62"), ("pooled", "1.73", "0.94", "2.50")]),
]
for _, _, rows in SETS:
    for r in rows:
        for v in r[1:]: assert v in have, f"{v} not in manifest"
STY = {"Qwen2.5-VL": ("#2a78d6", "circle"), "InternVL3": ("#eb6834", "square"), "pooled": ("#1f1f1e", "diamond")}
W, L, R, T, ROW, GAP = 680, 280, 30, 40, 20, 16
XMIN, XMAX = -4.0, 10.0
PANEL = 26  # header height per language panel
H = T + len(SETS) * (3 * ROW + GAP) + 2 * PANEL + 60
x = lambda v: L + (v - XMIN) / (XMAX - XMIN) * (W - L - R)
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Libertinus Sans, Linux Biolinum, DejaVu Sans, sans-serif" font-size="13">',
     f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
ybot = H - 50
for t in range(-4, 11, 2):
    o.append(f'<line x1="{x(t):.1f}" y1="{T-10}" x2="{x(t):.1f}" y2="{ybot}" stroke="#e4e3df" stroke-width="1"/>')
    o.append(f'<text x="{x(t):.1f}" y="{ybot+14}" text-anchor="middle" fill="#5f5e5a">{"−" if t < 0 else ("+" if t > 0 else "")}{abs(t)}</text>')
o.append(f'<line x1="{x(0):.1f}" y1="{T-10}" x2="{x(0):.1f}" y2="{ybot}" stroke="#5f5e5a" stroke-width="1"/>')
o.append(f'<line x1="{x(2):.1f}" y1="{T-10}" x2="{x(2):.1f}" y2="{ybot}" stroke="#5f5e5a" stroke-width="1" stroke-dasharray="4 3"/>')
o.append(f'<text x="{x(2)-4:.1f}" y="{T-14}" text-anchor="end" fill="#5f5e5a">registered threshold +2.0 (scale differs by panel)</text>')
o.append(f'<text x="{(L + W - R)/2:.1f}" y="{ybot+32}" text-anchor="middle" fill="#1f1f1e">ret − rand (CIDEr-D points, paired 95% bootstrap CI)</text>')
y = T
for j, (name, scorer, rows) in enumerate(SETS):
    if j in (0, 2):
        if j: o.append(f'<line x1="8" y1="{y-GAP/2:.1f}" x2="{W-R}" y2="{y-GAP/2:.1f}" stroke="#1f1f1e" stroke-width="1"/>')
        o.append(f'<text x="8" y="{y+16:.1f}" fill="#1f1f1e" font-weight="bold" font-size="14">{"Vietnamese panel (stripped CIDEr-D)" if j == 0 else "English panel (PTB CIDEr-D)"}</text>')
        y += PANEL
    o.append(f'<text x="8" y="{y+ROW*1.1:.1f}" fill="#1f1f1e" font-weight="bold">{name}</text>')
    o.append(f'<text x="8" y="{y+ROW*2.1:.1f}" fill="#5f5e5a">{scorer}</text>')
    for i, (s, p, lo, hi) in enumerate(rows):
        c, shape = STY[s]; yy = y + i * ROW + ROW / 2; px = x(float(p))
        o.append(f'<line x1="{x(float(lo)):.1f}" y1="{yy:.1f}" x2="{x(float(hi)):.1f}" y2="{yy:.1f}" stroke="{c}" stroke-width="2" stroke-linecap="round"/>')
        if shape == "circle": o.append(f'<circle cx="{px:.1f}" cy="{yy:.1f}" r="4.5" fill="{c}" stroke="#ffffff" stroke-width="2"/>')
        elif shape == "square": o.append(f'<rect x="{px-4.5:.1f}" y="{yy-4.5:.1f}" width="9" height="9" rx="1" fill="{c}" stroke="#ffffff" stroke-width="2"/>')
        else: o.append(f'<path d="M{px:.1f} {yy-6:.1f} L{px+6:.1f} {yy:.1f} L{px:.1f} {yy+6:.1f} L{px-6:.1f} {yy:.1f} Z" fill="{c}" stroke="#ffffff" stroke-width="2"/>')
        o.append(f'<text x="{L-8}" y="{yy+4:.1f}" text-anchor="end" fill="#5f5e5a">{s}</text>')
    y += 3 * ROW + GAP
o.append("</svg>")
Path(sys.argv[1]).write_text("\n".join(o) + "\n")
print("wrote", sys.argv[1])
