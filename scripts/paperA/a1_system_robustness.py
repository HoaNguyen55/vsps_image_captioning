#!/usr/bin/env python3
"""System-level robustness of Paper A's Table 7.1 slopes (CC-088 A-1; POST_HOC, registered verdicts unchanged).

Each Table 7.1 cell is an OLS slope of object F1 on ln M across the systems of a family, with an image-bootstrap
interval that holds the systems fixed. This script asks how much the sign depends on which systems are in the family:
  - leave-one-system-out (LOO): the slope with each system dropped, its range, and the drops that flip the sign;
  - system jackknife: SE = sqrt((n-1)/n * sum (s_(i) - mean)^2) and a t(n-1) 95% interval around the full slope;
  - subset slopes wherever a subset has >= 3 systems: within one prompt (short / detailed) and zero-shot only.
Per-system (M, F1) points come from the committed result files: stored per-system values for every family except
COCO-2500, which stores none; its table is rebuilt with `coco-table` by the procedure of check_coco.py (L1).

    python scripts/paperA/a1_system_robustness.py coco-table data/results/a1_robustness/coco2500_per_system.json
    python scripts/paperA/a1_system_robustness.py run data/results/a1_robustness/a1_system_robustness.json
    python scripts/paperA/a1_system_robustness.py --selftest
Writes numbers only.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
BK = ROOT / ".session_backup/2026-10-14"
SRC = {
    "coco": ROOT / "data/results/a1_robustness/coco2500_per_system.json",
    "h3": BK / "r12/H3/out/n1_results.json",
    "c2": BK / "r11_verify/c2_n1_uitviic_mstar.json",
    "xm": BK / "r12_verify/xm3600_full_verdict.json",
    "g2b": ROOT / "data/results/g2b/g2b_score.json",
}
# Table 7.1 values (rounded as printed) that each recomputed full slope must reproduce
TABLE = {
    "COCO-2500": (-4.28, 11.08, 22.41), "F-B (OPERA)": (-35.18, -29.57, 4.24), "F-C (Less-is-More)": (-31.89, -22.86, 6.91),
    "UIT-ViIC coco80": (-13.97, 4.80, 37.52), "UIT-ViIC vi lexicon": (-17.25, -6.28, 7.66),
    "XM3600": (-8.99, -2.43, 19.32), "G2-B cv295": (-11.46, None, 13.14), "G2-B uv231": (-20.96, None, 37.36),
    "G2-B xm600": (-12.27, None, 13.71),
}
COLS = ("1 ref", "5 refs", "label gold")
# per-system points stored rounded to 2 dp in these sources, so the recomputed full slope may differ by rounding
ROUNDED = {"F-B (OPERA)", "F-C (Less-is-More)", "UIT-ViIC coco80", "UIT-ViIC vi lexicon"}


def slope(x, y) -> float:
    x, y = np.asarray(x, float), np.asarray(y, float)
    dx = x - x.mean()
    den = (dx ** 2).sum()
    return float((dx * (y - y.mean())).sum() / den) if den > 1e-12 else float("nan")  # equal M: undefined


def analyse(points: dict[str, tuple[float, float]]) -> dict:
    """points: system -> (M, F1)."""
    names = sorted(points)
    lm = np.log([points[s][0] for s in names]); f1 = np.array([points[s][1] for s in names])
    n, full = len(names), slope(lm, f1)
    loo = {s: slope(np.delete(lm, i), np.delete(f1, i)) for i, s in enumerate(names)}
    v = np.array([b for b in loo.values() if np.isfinite(b)])
    se = float(np.sqrt((n - 1) / n * ((v - v.mean()) ** 2).sum()))
    t = float(stats.t.ppf(0.975, n - 1))
    flips = sorted(s for s, b in loo.items() if np.isfinite(b) and np.sign(b) != np.sign(full))
    return {"n_systems": n, "M_range": [round(float(np.exp(lm).min()), 4), round(float(np.exp(lm).max()), 4)],
            "slope_full": round(full, 4), "system_r": round(float(np.corrcoef(lm, f1)[0, 1]), 4),
            "loo": {s: (round(b, 4) if np.isfinite(b) else None) for s, b in loo.items()},
            "loo_undefined": sorted(s for s, b in loo.items() if not np.isfinite(b)), "loo_min": round(float(v.min()), 4),
            "loo_max": round(float(v.max()), 4), "loo_sign_flips": flips, "sign_stable_under_loo": not flips,
            "jackknife_se": round(se, 4), "jackknife_t95": [round(full - t * se, 4), round(full + t * se, 4)],
            "jackknife_t95_excludes_0": bool(full - t * se > 0 or full + t * se < 0)}


def subsets(points: dict, prompt_of, zeroshot_of) -> dict:
    groups = {}
    if all(prompt_of(s) is None for s in points):
        return {"prompt": "single prompt", "zero-shot only": "same as the full family" if all(map(zeroshot_of, points))
                else f"not computed ({sum(map(zeroshot_of, points))} systems)"}
    for p in ("short", "detailed"):
        groups[f"prompt={p}"] = {s: v for s, v in points.items() if prompt_of(s) == p}
    groups["zero-shot only"] = {s: v for s, v in points.items() if zeroshot_of(s)}
    out = {}
    for g, pts in groups.items():
        if len(pts) == len(points):
            out[g] = "same as the full family"
        elif len(pts) >= 3:
            a = analyse(pts)
            out[g] = {k: a[k] for k in ("n_systems", "M_range", "slope_full", "loo_min", "loo_max", "sign_stable_under_loo")}
            out[g]["lnM_spread"] = round(float(np.log(a["M_range"][1] / a["M_range"][0])), 4)  # small spread: ill-conditioned
        else:
            out[g] = f"not computed ({len(pts)} systems)"
    return out


def suffix_prompt(s: str) -> str | None:
    return "short" if "-short" in s else "detailed" if "-detailed" in s else None


def load_families() -> dict[str, dict[str, dict[str, tuple[float, float]]]]:
    fam = {}
    coco = json.loads(SRC["coco"].read_text())
    fam["COCO-2500"] = {c: {s: (v[3], v[2]) for s, v in coco["tables"][g].items()}
                        for c, g in zip(COLS, ("refs1_randk", "refs5_randk", "inst"))}
    h3 = json.loads(SRC["h3"].read_text())["families"]
    for key, label in (("F-B", "F-B (OPERA)"), ("F-C", "F-C (Less-is-More)")):
        fam[label] = {c: {s: (v[3], v[2]) for s, v in h3[key]["gold"][g]["per_system"].items()}
                      for c, g in zip(COLS, ("refs1_randk", "refs5_randk", "inst"))}
    c2 = json.loads(SRC["c2"].read_text())["uitviic_test"]
    for lex, label in (("coco80", "UIT-ViIC coco80"), ("vi_objects_in", "UIT-ViIC vi lexicon")):
        gv = c2["lexicons"][lex]["gold_variants"]
        fam[label] = {c: {s: (gv[g]["per_system_M"][s], gv[g]["per_system_F1_mixed"][s]) for s in c2["systems"]}
                      for c, g in zip(COLS, ("refs1_randk", "refs5_randk", "inst_only"))}
    xm = json.loads(SRC["xm"].read_text())["matcher_v2_tone_normalised"]["systems"]
    xs = [s for s in xm if s.startswith("xm3600_")]
    fam["XM3600"] = {"1 ref": {s: (xm[s]["refs1_randk"]["M"], xm[s]["refs1_randk"]["F1"]) for s in xs},
                     "5 refs": {s: (xm[s]["refs_all"]["M"], xm[s]["refs_all"]["F1"]) for s in xs},
                     "label gold": {s: (xm[s]["oiv7_verified"]["M_total_vi_classes"], xm[s]["oiv7_verified"]["F1_pos"])
                                    for s in xs}}
    g2 = json.loads(SRC["g2b"].read_text())["datasets"]
    for ds in ("cv295", "uv231", "xm600"):
        g = g2[ds]["descriptive"]["golds"]
        lab = "oiv7_verified" if ds == "xm600" else "inst"
        fam[f"G2-B {ds}"] = {"1 ref": {s: (v["M"][0], v["F"][0]) for s, v in g["refs1_randk"]["systems"].items()},
                             "label gold": {s: (v["M"][0], v["F"][0]) for s, v in g[lab]["systems"].items()}}
    return fam


def is_zeroshot(s: str) -> bool:
    return "zeroshot" in s or s.startswith(("opera/", "lim/", "g2b_")) or "/" in s


def run(out: Path) -> None:
    res = {"label": "POST_HOC (CC-088 A-1); system-level robustness; registered verdicts unchanged",
           "inputs_sha256": {k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in SRC.items()},
           "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "families": {}}
    for label, cols in load_families().items():
        row = {}
        for c, pts in cols.items():
            a = analyse(pts)
            want = TABLE[label][COLS.index(c)]
            a["table_7_1_value"] = want
            a["points"] = "stored per-system values rounded to 2 dp" if label in ROUNDED else "full precision"
            a["tolerance"] = 0.15 if label in ROUNDED else 0.01
            a["reproduces_table"] = bool(abs(a["slope_full"] - want) <= a["tolerance"])
            a["subsets"] = subsets(pts, suffix_prompt, is_zeroshot)
            row[c] = a
        res["families"][label] = row
    bad = [(f, c) for f, r in res["families"].items() for c, a in r.items() if not a["reproduces_table"]]
    assert not bad, f"full slopes do not reproduce Table 7.1: {bad}"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1) + "\n")
    for f, r in res["families"].items():
        for c, a in r.items():
            print(f"{f:22s} {c:10s} full {a['slope_full']:+8.2f} LOO [{a['loo_min']:+8.2f}, {a['loo_max']:+8.2f}] "
                  f"flips {a['loo_sign_flips']} JK95 {a['jackknife_t95']}")


def coco_table(out: Path) -> None:
    """Point tables of check_coco.py (.session_backup/2026-10-14/r11_litmaps/L1/scripts/check_coco.py), same rng order."""
    sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
    import score_coco_probe as sc
    RES, DS = ROOT / "data/results", ROOT / "data/datasets"
    vi, syn = sc.load_vi_terms(), sc.load_synonyms()
    cids = sorted(i["cocoid"] for i in json.loads((ROOT / "data/coco_probe/manifest.json").read_text("utf-8"))["images"])
    cinst = {int(k): set(v["coco"]) for k, v in json.loads((ROOT / "data/coco_probe/instance_gold.json").read_text()).items()}
    want, text, kr = set(cids), (DS / "karpathy/dataset_coco.json").read_text(), {}
    for m in re.finditer(r'"cocoid": (\d+)\}', text):
        c = int(m.group(1))
        if c in want:
            s = text.rfind('{"filepath"', 0, m.start())
            kr[c] = [x["raw"] for x in json.loads(text[s:m.end()])["sentences"]]
    ref_sets = {c: [sc.en_classes(s, syn) for s in kr[c][:5]] for c in cids}
    ments = {}
    for d in ("coco5000", "coco_transfer", "coco5000_vcd"):
        for f in sorted((RES / d).glob("*.shard*.jsonl")):
            name = f.name.split(".shard")[0] + ("+vcd" if d == "coco5000_vcd" else "")
            ms = {json.loads(l)["cocoid"]: sc.vi_objects(json.loads(l)["caption"], vi) for l in f.read_text("utf-8").splitlines()}
            ments[name] = [ms.get(c, set()) for c in cids]
    rng = np.random.default_rng(1)
    rng.multinomial(len(cids), np.full(len(cids), 1 / len(cids)), size=500)  # consumed as in check_coco.py
    golds = {"inst": [[cinst.get(c, set()) for c in cids]]}
    for k in range(1, 6):
        golds[f"refs{k}_randk"] = [[set().union(*[ref_sets[c][j] for j in rng.choice(len(ref_sets[c]), k, replace=False)])
                                    for c in cids] for _ in range(20)]

    def prf(m_list, g_list):
        tp = np.array([len(m & g) for m, g in zip(m_list, g_list)], float)
        nm = np.array([len(m) for m in m_list], float)
        hg = np.array([bool(g) for g in g_list])
        rec = np.array([len(m & g) / len(g) if g else 0.0 for m, g in zip(m_list, g_list)])
        p = tp.sum() / nm.sum() if nm.sum() else 0.0
        r = rec[hg].mean()
        return 100 * p, 100 * r, (200 * p * r / (p + r) if p + r else 0.0), nm.mean()

    tables = {}
    for g in ("refs1_randk", "refs5_randk", "inst"):
        tables[g] = {s: [float(x) for x in np.mean([prf(ments[s], gg) for gg in golds[g]], 0)] for s in ments}
    rec = {"procedure": "check_coco.py point tables (P, R, F1 mixed, M); rng seed 1, multinomial(500) consumed, NSUB 20",
           "n_img": len(cids), "systems": list(ments), "tables": tables}
    for g, want in zip(("refs1_randk", "refs5_randk", "inst"), TABLE["COCO-2500"]):
        t = tables[g]; got = round(slope(np.log([t[s][3] for s in t]), [t[s][2] for s in t]), 2)
        assert got == want, (g, got, want)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=1) + "\n")
    print("coco table ok", {g: len(t) for g, t in tables.items()})


def selftest() -> None:
    line = {f"s{i}": (m, 10 + 5 * np.log(m)) for i, m in enumerate((1.0, 1.5, 2.0, 3.0))}
    a = analyse(line)
    assert abs(a["slope_full"] - 5) < 1e-9 and a["jackknife_se"] < 1e-9 and a["sign_stable_under_loo"]
    lev = {"a": (1.0, 50.0), "b": (1.1, 51.0), "c": (1.2, 52.0), "d": (1.3, 53.0), "big": (4.3, 30.0)}
    b = analyse(lev)
    assert b["slope_full"] < 0 and b["loo_sign_flips"] == ["big"] and not b["sign_stable_under_loo"]
    assert suffix_prompt("xm3600_p1_s43-short") == "short" and suffix_prompt("zeroshot-detailed+vcd") == "detailed"
    assert suffix_prompt("opera/llava-1.5__greedy") is None
    assert is_zeroshot("zeroshot-detailed+vcd") and is_zeroshot("opera/llava-1.5__greedy") and not is_zeroshot("p1_s43-short")
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif sys.argv[1] == "coco-table":
        coco_table(Path(sys.argv[2]))
    elif sys.argv[1] == "run":
        run(Path(sys.argv[2]))
    else:
        sys.exit(__doc__)
