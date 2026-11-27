"""Judge CC-511 mutants on verdict-deciding lines of c_n3d.py (scratch copy; synthetic suite only)."""
import sys
from pathlib import Path
W = Path(sys.argv[1]); sys.path.insert(0, str(W))
import test_c_n3d as T
SRC = T.SRC
M = [
 ("L, W = d < -m, d > m", "L, W = d > m, d < -m"),
 ('out[f"D_{f}_ret"] = out[f"Pr_{f}_L"] - out[f"Pr_{f}_W"]', 'out[f"D_{f}_ret"] = out[f"Pr_{f}_W"] - out[f"Pr_{f}_L"]'),
 ("cat_d1 = category(c.f_d1, prec)[rows]", "cat_d1 = category(c.f_ret, prec)[rows]"),
 ("f1 = c.f_d1[f][rows]", "f1 = c.f_d2[f][rows]"),
 ("fr = c.f_ret[f][rows]", "fr = c.f_d0[f][rows]"),
 ('out["H3_gap_minus_plac"] = (out["C_L"] - out["C_W"]) - (out["C_Pm"] - out["C_Pp"])', 'out["H3_gap_minus_plac"] = (out["C_L"] - out["C_W"]) + (out["C_Pm"] - out["C_Pp"])'),
 ('out["H3_gap_minus_plac"] = (out["C_L"] - out["C_W"]) - (out["C_Pm"] - out["C_Pp"])', 'out["H3_gap_minus_plac"] = (out["C_L"] - out["C_W"]) - (out["C_Pp"] - out["C_Pm"])'),
 ('"p": ptilde(boot[f"Delta_{f}"], 0.0)', '"p": ptilde(boot[f"Delta_{f}"], D_MIN)'),
 ('"p": ptilde(boot[f"Delta_{f}"], 0.0)', '"p": ptilde(boot[f"D_{f}_ret"], 0.0)'),
 ('"p": ptilde(boot["C_L"], C_TEST)', '"p": ptilde(boot["C_W"], C_TEST)'),
 ('gap = pt["C_L"] - pt["C_W"]', 'gap = pt["C_L"] - pt["C_Pm"]'),
 ('adj = holm([r["p"] for r in rows])', 'adj = [r["p"] for r in rows]'),
 ("run = max(run, min(1.0, (m - j) * ps[k]))", "run = max(run, min(1.0, m * ps[k]))"),
 ('order = np.argsort(ps, kind="stable")', 'order = np.argsort(ps, kind="stable")[::-1]'),
 ("/ (s.size + 1))", "/ (s.size))"),
 ("e = c.e[rows]", "e = c.d[rows]"),
 ('if not r["decidable"]:', "if False:"),
 ('"sr7": pt[f"SR7_{f}"]', '"sr7": 1.0'),
 ('np.log(out[f"Pr_{f}_L"] / out[f"Pr_{f}_W"]) - np.log(a / b)', 'np.log(out[f"Pr_{f}_L"] / out[f"Pr_{f}_W"]) - np.log(b / a)'),
 ('out[f"Pr_{f}_L"], out[f"Pr_{f}_W"] = _rate(fr, L), _rate(fr, W)', 'out[f"Pr_{f}_L"], out[f"Pr_{f}_W"] = _rate(fr, W), _rate(fr, L)'),
 ("return (f & g).sum(-1) / g.sum(-1)", "return (f & g).sum(-1) / g.shape[-1]"),
 ('"ZL": any(status(o) == "present"', '"ZL": any(status(o) == "absent"'),
 ("z = {self.key(o) for o in self.classes(zs)}", "z = set()"),
 ('out[f"share_{name}_{g}"] = _rate(cat_ret == j, gm)', 'out[f"share_{name}_{g}"] = _rate(cat_ret != j, gm)'),
 ("out = np.where(fl[prec[j]], PREC.index(prec[j]), out)", "out = np.where(fl[prec[j]], j, out)"),
 ('pt.get("nPp", 0)) >= MIN_N', 'pt.get("nPp", 0)) > MIN_N'),
 ("return {s: rng.integers(0, n, (B, n)) for s, n in SET_N.items()}", "return {s: np.random.default_rng(SEED).integers(0, n, (B, n)) for s, n in SET_N.items()}"),
 ('"conds": pt[f"Delta_{f}"] >= D_MIN', '"conds": pt[f"D_{f}_ret"] >= D_MIN'),
 ("t_ids, t_sha = {r[0] for r in tsv}, {r[1] for r in tsv}", "t_ids, t_sha = {r[1] for r in tsv}, {r[0] for r in tsv}"),
 ("o_ids, o_sha = {r[1] for r in carve_order}, {r[2] for r in carve_order}", "o_ids, o_sha = {r[0] for r in carve_order}, {r[2] for r in carve_order}"),
 ('xm_test = {r[0] for r in lists["sets"]["xm_test2500"]}', 'xm_test = {r[1] for r in lists["sets"]["xm_test2500"]}'),
 ('elif a < ALPHA and r["conds"]:', 'elif a <= ALPHA and r["conds"]:'),
 ("np.sum(np.isnan(s) | (s <= thr))", "np.sum(np.isnan(s) & (s <= thr))"),
 ('out[f"S_{f}"] = _rate(c.f_ret[f][rows], L) - _rate(c.f_d0[f][rows], L)', 'out[f"S_{f}"] = _rate(c.f_ret[f][rows], W) - _rate(c.f_d0[f][rows], W)'),
 ('"E": (L.sum(-1) - Pm.sum(-1)) / L.shape[-1]', '"E": (L.sum(-1) - Pp.sum(-1)) / L.shape[-1]'),
 ('return "DETECTED" if lo > 0 else "REVERSED" if hi < 0 else "UNRESOLVED"', 'return "DETECTED" if lo > 0 else "UNRESOLVED"'),
]
alive, killed = [], 0
for old, new in M:
    n = SRC.count(old)
    if n != 1:
        print("NOT UNIQUE", n, old[:60]); continue
    if T.suite(T.load(SRC.replace(old, new))):
        killed += 1
    else:
        alive.append(old[:90] + "  ->  " + new[:60])
T.load()
print(f"judge mutants: {killed}/{len(M)} killed")
for a in alive: print("ALIVE:", a)
