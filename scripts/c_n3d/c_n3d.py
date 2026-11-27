"""C-N3D: rule-based failure categories of the retrieval contrast on stored development decodes (Paper C).

Registration: manuscript/prereg/2026-11-27_c_n3d/PREREG_DRAFT_C_N3D_v3.md (CC-509, CC-509 r2). Every output is an
aggregate (counts, shares, CIs, p-like statistics, labels); no caption and no per-image row is ever written.

  python3 c_n3d.py selftest                      synthetic only; opens no input (laptop allowed, CC-509 r2 §10 step 1)
  python3 c_n3d.py custody --root R --data D     host step 2 (all pins) + 2a: id/sha256 intersections, counts only
  python3 c_n3d.py run --root R --data D --out J host step 4: the one run (refuses unless custody and selftest passed)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np

# ------------------------------------------------------------------------------------------------ registered constants
M_MARGIN = 10.0            # prereg §5, T8 margin (NOTE1 W7-b)
B = 2000                   # prereg §6
SEED = 1127001             # prereg §6 [W6b]
ALPHA = 0.025              # one-sided family-wise
M_HOLM = 6                 # H1-H3 x {Qwen2.5-VL-7B, InternVL3-8B} on OV-dev-B; NOT DECIDABLE enters with p = 1
MIN_N = 30                 # decidability: each of L, W, P-, P+
D_MIN = 0.10               # H1, H2 point threshold
C_MIN, C_TEST, C_GAP = 0.60, 0.50, 0.10   # H3
LN_REL = 0.25              # LN flag
CP_M = 0.90                # near-verbatim copy statistic (supplement l.791)
SET_N = {"ov_dev_b": 925, "xm_dev500": 500, "f30k_carve": 1000}   # rng order [W6b]
FAMILY_MODELS = ("qwen25vl_7b", "internvl3_8b")
MODELS = ("qwen25vl_7b", "internvl3_8b", "aya_vision_8b")
FLAGS = ("CP", "BO", "ZL", "LN")
PREC = ("CP", "BO", "ZL", "LN")            # exclusive precedence; index 4 = OTHER
PREC_REV = ("LN", "ZL", "BO", "CP")        # SR6
OTHER = 4
LABEL = "DEVELOPMENT / C-N3D, NON-CONFIRMATORY; rule-based categories, no human labels"
EN_LABEL = "not placebo-differenced; coupled by construction (prereg §6); length counted in words"
EN_NOT_RUN = "NOT RUN (no COCO-memory shown captions; erratum 1 E3)"
EN_CATS = "categories ZL > LN > OTHER only; BO and CP not run"
EN_NOT_RUN_KEY = re.compile(r"(?:^|_)(?:BO|CP)(?:_|$)")
H_NOTE = "335 of the 925 OV-dev-B images are OpenViIC-dev copies of Paper B's BD-T1 set H; none is a memory member (CC-493e1)"
AYA_FLAG = "placebo flagged on this set (Section 6.10.5)"
#: parity gate: mean per-image contrast must equal the printed value of the text of record (2 dp)
PARITY = {("ov_dev_b", "qwen25vl_7b"): 8.27, ("ov_dev_b", "internvl3_8b"): 5.22, ("ov_dev_b", "aya_vision_8b"): 6.25,
          ("xm_dev500", "qwen25vl_7b"): 1.79, ("xm_dev500", "internvl3_8b"): 0.11, ("xm_dev500", "aya_vision_8b"): 1.74,
          ("f30k_carve", "aya_vision_8b"): 6.12, ("f30k_carve", "internvl3_8b"): -1.00,
          ("f30k_carve", "qwen25vl_7b"): 5.04}   # Table 11, Table S21 (R = 3 mean); Table S19 (d0, PTB)
PARITY_SR3 = {("ov_dev_b", "qwen25vl_7b"): 9.67, ("ov_dev_b", "internvl3_8b"): 5.36,
              ("xm_dev500", "qwen25vl_7b"): 4.44, ("xm_dev500", "internvl3_8b"): 1.54}   # Tables S16, S17 (d0)
PARITY_TOL = 0.0051


# ------------------------------------------------------------------------------------------------ bootstrap
def index_matrices() -> dict[str, np.ndarray]:
    """One generator, called once per set in the registered order, always all three sets [W6b]."""
    rng = np.random.default_rng(SEED)
    return {s: rng.integers(0, n, (B, n)) for s, n in SET_N.items()}


def ptilde(stat_b: np.ndarray, thr: float) -> float:
    """(1 + #{b : stat_b <= thr}) / (B + 1); a replicate with an empty group (nan) counts as <= thr."""
    s = np.asarray(stat_b, float)
    return float((1 + np.sum(np.isnan(s) | (s <= thr))) / (s.size + 1))


def ci(stat_b: np.ndarray) -> list[float]:
    s = np.asarray(stat_b, float)
    s = s[~np.isnan(s)]
    return [float(np.percentile(s, 2.5)), float(np.percentile(s, 97.5))] if s.size else [math.nan, math.nan]


def holm(ps: list[float]) -> list[float]:
    """Holm-adjusted p for a family of size len(ps) (step-down, monotone)."""
    m = len(ps)
    order = np.argsort(ps, kind="stable")
    adj, run = [0.0] * m, 0.0
    for j, k in enumerate(order):
        run = max(run, min(1.0, (m - j) * ps[k]))
        adj[k] = run
    return adj


# ------------------------------------------------------------------------------------------------ flags
@dataclass
class Instruments:
    """The existing instruments, injected (synthetic in selftest; the pinned modules on the host)."""
    classes: Callable[[str], list]
    key: Callable[[str], str]
    copy_m: Callable[[str, list], float]
    length: Callable[[str], int]

    def neighbour_only(self, cap: str, zs: str, shown: list[str]) -> list[str]:
        """Section 3.4: in the caption, absent from the zero-shot caption, present in a shown caption."""
        z = {self.key(o) for o in self.classes(zs)}
        ex = {self.key(o) for s in shown for o in self.classes(s)}
        return [o for o in self.classes(cap) if self.key(o) not in z and self.key(o) in ex]


def flags_zl_ln(inst: Instruments, cap: str, zs: str, status: Callable[[str], str], med_len: float,
                ln_rel: float = LN_REL) -> dict[str, bool]:
    """ZL and LN: the two flags that need no shown list (the only ones run in English, erratum 1 E3)."""
    have = {inst.key(o) for o in inst.classes(cap)}
    return {"ZL": any(status(o) == "present" and inst.key(o) not in have for o in inst.classes(zs)),
            "LN": abs(inst.length(cap) - med_len) >= ln_rel * med_len}


def flags_of(inst: Instruments, cap: str, zs: str, shown: list[str], status: Callable[[str], str],
             med_len: float, ln_rel: float = LN_REL) -> dict[str, bool]:
    """BO, CP, ZL, LN of one caption against its own shown list (prereg §5). status(o) -> 'present' | 'absent'."""
    return {"BO": any(status(o) == "absent" for o in inst.neighbour_only(cap, zs, shown)),
            "CP": inst.copy_m(cap, shown) >= CP_M, **flags_zl_ln(inst, cap, zs, status, med_len, ln_rel)}


def category(fl: dict[str, np.ndarray], prec=PREC) -> np.ndarray:
    """Exclusive category code per image: index of the first flag in prec that holds, else OTHER (4)."""
    n = len(next(iter(fl.values())))
    out = np.full(n, OTHER)
    for j in reversed(range(len(prec))):
        out = np.where(fl[prec[j]], PREC.index(prec[j]), out)
    return out


# ------------------------------------------------------------------------------------------------ estimands
@dataclass
class Cell:
    """One backbone x set. d = s(ret) - s(rand d0); e = s(rand d1) - s(rand d2) (None: no placebo split).
    f_ret, f_d0, f_d1, f_d2: {flag: bool[n]} (f_d1/f_d2 None without placebo)."""
    d: np.ndarray
    e: np.ndarray | None
    f_ret: dict
    f_d0: dict
    f_d1: dict | None
    f_d2: dict | None


def _rate(f: np.ndarray, g: np.ndarray) -> np.ndarray:
    with np.errstate(invalid="ignore", divide="ignore"):
        return (f & g).sum(-1) / g.sum(-1)


def stats(c: Cell, rows: np.ndarray, m: float = M_MARGIN, prec=PREC) -> dict[str, np.ndarray]:
    """Every statistic on the rows (n,) or (B, n); groups recomputed from the resampled differences."""
    d = c.d[rows]
    L, W = d < -m, d > m
    cat_ret = category(c.f_ret, prec)[rows]
    out = {"nL": L.sum(-1), "nW": W.sum(-1), "n": np.full(L.shape[:-1], L.shape[-1])}
    for f in FLAGS:
        fr = c.f_ret[f][rows]
        out[f"Pr_{f}_L"], out[f"Pr_{f}_W"] = _rate(fr, L), _rate(fr, W)
        out[f"D_{f}_ret"] = out[f"Pr_{f}_L"] - out[f"Pr_{f}_W"]
        out[f"base_{f}_ret"] = fr.mean(-1)
    for g, gm in (("L", L), ("W", W)):
        for j, name in enumerate(PREC + ("OTHER",)):
            out[f"share_{name}_{g}"] = _rate(cat_ret == j, gm)
        out[f"C_{g}"] = 1 - out[f"share_OTHER_{g}"]
    out["C_all"] = 1 - (cat_ret == OTHER).mean(-1)
    for f in ("BO", "CP"):  # S1, S2 (coupled by construction, prereg §6)
        out[f"S_{f}"] = _rate(c.f_ret[f][rows], L) - _rate(c.f_d0[f][rows], L)
    if c.e is None:
        return out
    e = c.e[rows]
    Pm, Pp = e < -m, e > m
    cat_d1 = category(c.f_d1, prec)[rows]
    out.update({"nPm": Pm.sum(-1), "nPp": Pp.sum(-1), "E": (L.sum(-1) - Pm.sum(-1)) / L.shape[-1]})
    for f in FLAGS:
        f1 = c.f_d1[f][rows]
        a, b = _rate(f1, Pm), _rate(f1, Pp)
        out[f"D_{f}_plac"] = a - b
        out[f"Delta_{f}"] = out[f"D_{f}_ret"] - out[f"D_{f}_plac"]
        out[f"base_{f}_d1"] = f1.mean(-1)
        with np.errstate(invalid="ignore", divide="ignore"):
            out[f"SR7_{f}"] = np.log(out[f"Pr_{f}_L"] / out[f"Pr_{f}_W"]) - np.log(a / b)
    for g, gm in (("Pm", Pm), ("Pp", Pp)):
        for j, name in enumerate(PREC + ("OTHER",)):
            out[f"share_{name}_{g}"] = _rate(cat_d1 == j, gm)
        out[f"C_{g}"] = 1 - out[f"share_OTHER_{g}"]
    out["H3_gap_minus_plac"] = (out["C_L"] - out["C_W"]) - (out["C_Pm"] - out["C_Pp"])
    for f in ("BO", "CP"):
        out[f"S_{f}_twin"] = _rate(c.f_d1[f][rows], Pm) - _rate(c.f_d2[f][rows], Pm)
    return out


def summarise(c: Cell, idx: np.ndarray, **kw) -> tuple[dict, dict]:
    """(point, {stat: {point, ci}}) with the full-sample point and the bootstrap CI of each statistic."""
    full = stats(c, np.arange(c.d.size), **kw)
    boot = stats(c, idx, **kw)
    rows = {k: {"point": float(full[k]), "ci": ci(boot[k])} for k in full}
    return {k: float(v) for k, v in full.items()}, {"rows": rows, "boot": boot}


def s_label(cint: list[float]) -> str:
    lo, hi = cint
    return "DETECTED" if lo > 0 else "REVERSED" if hi < 0 else "UNRESOLVED"


def decidable(pt: dict) -> bool:
    return min(pt["nL"], pt["nW"], pt.get("nPm", 0), pt.get("nPp", 0)) >= MIN_N


def h_row(h: str, pt: dict, boot: dict) -> dict:
    """One primary row before Holm: its p-like statistic and point conditions."""
    if not decidable(pt):
        return {"h": h, "p": 1.0, "conds": False, "decidable": False}
    if h in ("H1", "H2"):
        f = "BO" if h == "H1" else "ZL"
        return {"h": h, "point": pt[f"Delta_{f}"], "p": ptilde(boot[f"Delta_{f}"], 0.0),
                "conds": pt[f"Delta_{f}"] >= D_MIN, "sr7": pt[f"SR7_{f}"], "decidable": True}
    gap = pt["C_L"] - pt["C_W"]
    return {"h": h, "point": pt["C_L"], "p": ptilde(boot["C_L"], C_TEST), "gap": gap,
            "gap_minus_plac": pt["H3_gap_minus_plac"], "decidable": True,
            "conds": pt["C_L"] >= C_MIN and gap >= C_GAP and pt["H3_gap_minus_plac"] >= 0}


def family_verdicts(rows: list[dict]) -> list[dict]:
    """Holm over the six primary rows (m = 6 always; NOT DECIDABLE rows enter with p = 1) [W6a]; N4 wording."""
    if len(rows) != M_HOLM:
        raise SystemExit(f"family must have {M_HOLM} rows, has {len(rows)}")
    adj = holm([r["p"] for r in rows])
    out = []
    for r, a in zip(rows, adj):
        if not r["decidable"]:
            v = "NOT DECIDABLE"
        elif a < ALPHA and r["conds"]:
            v = "PASS (base-rate attributed)" if r["h"] in ("H1", "H2") and not r["sr7"] >= 0 else "PASS"
        else:
            v = "FAIL"
        out.append({**r, "p_holm": a, "verdict": v})
    return out


def analyse(c: Cell, idx: np.ndarray, **kw) -> dict:
    """Every printed row of one cell: G0, S1-S3, the H estimands; aggregates only."""
    pt, res = summarise(c, idx, **kw)
    rows = res["rows"]
    for k in ("S_BO", "S_CP", "S_BO_twin", "S_CP_twin"):
        if k in rows:
            rows[k]["label"] = s_label(rows[k]["ci"])
    return {"rows": rows, "decidable": c.e is not None and decidable(pt), "_pt": pt, "_boot": res["boot"]}


def public(a: dict) -> dict:
    return {k: v for k, v in a.items() if not k.startswith("_")}


def english_public(a: dict) -> dict:
    """English rows (erratum 1 E3): every BO / CP statistic is the NOT RUN string, never a number; S3 shares and
    C_L, C_W, C_all carry the reduced-category label."""
    rows = {}
    for k, v in a["rows"].items():
        if EN_NOT_RUN_KEY.search(k):
            rows[k] = EN_NOT_RUN
        elif k.startswith(("share_", "C_")):
            rows[k] = {**v, "label": EN_CATS}
        else:
            rows[k] = v
    return {**public(a), "rows": rows, "label": EN_LABEL}


# ------------------------------------------------------------------------------------------------ custody (step 2a)
def custody_counts(lists: dict, ov_test_tsv: str, carve_order: list, f30k: dict) -> dict[str, int]:
    """R2 check: counts only, no image file read. lists = stage-1 lists.json; f30k = c_t1_f30k_lists.json."""
    dev = {s: lists["sets"][s] for s in ("ov_dev_b", "xm_dev500")}
    if len(dev["ov_dev_b"]) != 925 or len(dev["xm_dev500"]) != 500 or len(f30k["carve"]) != 1000:
        raise SystemExit("STOP: query-set sizes are not 925 / 500 / 1,000")
    tsv = [ln.split("\t") for ln in ov_test_tsv.splitlines() if ln.strip()]
    t_ids, t_sha = {r[0] for r in tsv}, {r[1] for r in tsv}
    o_ids, o_sha = {r[1] for r in carve_order}, {r[2] for r in carve_order}
    xm_test = {r[0] for r in lists["sets"]["xm_test2500"]}
    out = {}
    for s, rows in dev.items():
        ids = {r[0] for r in rows} | {r[1] for r in rows}
        sha = {r[2] for r in rows}
        out[f"{s}&ov_test.ids"], out[f"{s}&ov_test.sha"] = len(ids & t_ids), len(sha & t_sha)
        out[f"{s}&carve.ids"], out[f"{s}&carve.sha"] = len(ids & o_ids), len(sha & o_sha)
    out["xm_dev500&xm_test2500.ids"] = len({r[0] for r in dev["xm_dev500"]} & xm_test)
    carve = set(f30k["carve"])
    out["f30k_carve&refuse.val"] = len(carve & set(f30k["refuse"]["val"]))
    out["f30k_carve&refuse.test"] = len(carve & set(f30k["refuse"]["test"]))
    return out


def custody_gate(counts: dict[str, int]) -> None:
    bad = {k: v for k, v in counts.items() if v}
    if bad:
        raise SystemExit(f"STOP: custody counts above 0: {bad}")


def row_guard(ids, refused: set, what: str) -> None:
    """R1: no refused id (Flickr30K val/test, XM-test2500) enters any row."""
    hit = len(set(ids) & refused)
    if hit:
        raise SystemExit(f"STOP: {hit} refused ids ({what}) would enter a row")


# ------------------------------------------------------------------------------------------------ host adapters
def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_pinned(p: Path, want: str) -> bytes:
    if sha(p) != want:
        raise SystemExit(f"STOP: {p.name} sha256 is not {want[:8]}")
    return p.read_bytes()


def push_list(path: Path) -> dict[str, str]:
    """PUSH_LIST.sha256 of this folder: '<sha256>  <relative path>' per line (COMPUTE v3 §2.1)."""
    out = {}
    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.strip() and not ln.startswith("#"):
            h, p = ln.split(None, 1)
            out[p.strip()] = h
    return out


def check_push(root: Path, pins: dict[str, str]) -> None:
    bad = [p for p, h in pins.items() if not (root / p).is_file() or sha(root / p) != h]
    if bad:
        raise SystemExit(f"STOP: {len(bad)} pushed files missing or not as pinned, e.g. {bad[:2]}")


def vi_instruments():
    """The pinned Vietnamese instruments: guard (matcher v2, neighbour_only), rl_reward (copy_stat, syllables)."""
    import guard as G
    import rl_reward as R

    def copy_m(cap, shown):
        return R.copy_stat(R.syllables(cap), [R.syllables(s) for s in shown])[0]
    return Instruments(classes=G.classes, key=G.key, copy_m=copy_m, length=lambda t: len(R.syllables(t)))


def en_instruments():
    """English: the committed COCO-80 matcher (score_coco_probe.en_classes); words for length and the copy statistic."""
    import rl_reward as R
    import score_coco_probe as SC
    syn = SC.load_synonyms()

    def words(t):
        return t.lower().split()
    return Instruments(classes=lambda t: sorted(SC.en_classes(t, syn)), key=lambda o: o,
                       copy_m=lambda cap, shown: R.copy_stat(words(cap), [words(s) for s in shown])[0],
                       length=lambda t: len(words(t)))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    c = sub.add_parser("custody")
    for k in ("root", "data"):
        c.add_argument(f"--{k}", type=Path, required=True)
    r = sub.add_parser("run")
    for k in ("root", "data", "out"):
        r.add_argument(f"--{k}", type=Path, required=True)
    a = ap.parse_args()
    if a.cmd == "selftest":
        import test_c_n3d
        test_c_n3d.main()
        return
    if a.cmd == "custody":
        import c_n3d_host as H
        H.custody(a.root, a.data)
        return
    import c_n3d_host as H
    H.run(a.root, a.data, a.out)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    os.environ.setdefault("PYTHONHASHSEED", "0")
    main()
