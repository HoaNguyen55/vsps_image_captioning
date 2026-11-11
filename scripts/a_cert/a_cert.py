#!/usr/bin/env python3
"""A-CERT (Paper A): certification of a conclusion under incomplete gold, tested on the human-completed object gold
of XM3600-600. Spec: manuscript/prereg/2026-11-11_a_cert/A_CERT_ANALYSIS_REG_v1_1.md (v1 + CC-333 B1-B5); H2d:
A_CERT_ANALYSIS_REG_v1_3_H2D.md (CC-336, CC-337); erratum B1 of A_CERT_ADDENDUM_VP_v1_1.md §V.4a.

  selftest --out F   synthetic fixtures only (registration §11 (i)-(vii), CC-333 Ruling 5(2) (viii)-(x))
  gate               label-free: reproduces the registered slopes, Table S7.2 ends, BUILD.json counts, part-1 set
  freeze             label-free: FREEZE.json (§8); refuses unless the gate passed and code + v1.1 equal HEAD blobs
  score --labels L --labels-sha H --key K
                     once, after the FREEZE pin line; fault rule B4: every statistic in memory, one atomic write

Every mode installs an open/listdir audit hook first: a path under a label directory is refused unless the mode is
`score` and the path is one of its two named files. Run:
  OMP_NUM_THREADS=2 nice -n 15 ~/.venvs/c_stage1_lists/bin/python -I -B scripts/a_cert/a_cert.py <mode>
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import subprocess
import sys
import tempfile
from collections import defaultdict
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SELF = "scripts/a_cert/a_cert.py"
REG = "manuscript/prereg/2026-11-11_a_cert/A_CERT_ANALYSIS_REG_v1_1.md"
H2D = "manuscript/prereg/2026-11-11_a_cert/A_CERT_ANALYSIS_REG_v1_3_H2D.md"
OUT = "data/results/a_cert"
P_REAL = {"gate": f"{OUT}/gate/gate.json", "freeze": f"{OUT}/freeze/FREEZE.json",
          "result": f"{OUT}/score/A_CERT_RESULT.json", "log": ".session_backup/2026-10-13/decisions/LOG.md",
          "part1_n": 2233}
PLAN_DIR = "manuscript/prereg/2026-11-11_xm600_gold_completion"
BUILD = f"{PLAN_DIR}/BUILD.json"
ASSIGN = f"{PLAN_DIR}/assignment.json"
BRACKET = "data/results/n_f1/bracket_result.json"
PINS = {BUILD: None, ASSIGN: "55e07337218acc820aafc27659e499ade4ae622cc6eaf41be2f7bb3df510cb2d",
        BRACKET: "4796ed12", "data/xm3600/vi_oiv7_map.json": "27f2b1ca", "tools/obj_rater/build_assignment.py":
        "497e5747", "scripts/pascal50s/p50x.py": "3f562e87", "scripts/n_f1/bracket.py": None,
        "scripts/a_m1/a_m1.py": None}
KEY_SHA = "a2cef89475675b66867577d399d7050ccf2925abc7a0b04f9572718a85a1c73a"

# §4, §6, §7 constants
ALPHA, ALPHA_S, M_FAM = 0.05, 0.025, 6
GRID, W0 = (0.0, 0.10, 0.20, 0.30, 0.50), 0.20
W_LO, BISECT = 0.001, 30
N_MIN, SHARE = 10, 0.05
SEED, B_TRUTH = 20261111, 2000
H2B_PASS, H3_MIN = 11, 50
BONF = 100 * ALPHA / 6 / 2
H2D_SESOI, H2D_MIN = Fr(1, 10), 5
BONF7 = 100 * ALPHA / 7 / 2  # v1.3 §3: "the 0.36th percentile" (Bonferroni over seven), descriptive
H2D_LABEL = ("registered on 2026-11-11 after the aggregate look on COCO-5000, before anyone but the annotator opened a "
             "human label value; the human answers are unseen by the analysts, the Open Images statuses that enter the "
             "outcome are partly seen (v1.1 §9)")
BONF7_TXT = "0.36th percentile (100 alpha/14 = 0.357)"  # CC-343 N5
GOLD_II_LABEL = "pooled gold; favours systems that name more"  # plan §5; CC-343 S2
SHA_REG = "e564b7b10cf500db50e48748f9e4e2e010378313eaeca89c4d14bde6d072aa7e"  # CC-343 N4: v1.1 at 0519b82
SHA_H2D = "d0afcaf0390031f1a2825a2d1e1b49ede6e57d42424be8281682c48f1e440515"  # CC-343 N4: v1.3 at 659f6c7
N_TARGETS1, N_NAMED, N_CTRL = 1790, 4910, 443
REG_SLOPE = {"Q25": 19.3247, "Q3": 13.70847}
S72 = {"Q25": (5.83, 20.13), "Q3": (1.97, 14.78)}
S5 = {"Q25": {"F": (2.31, 23.65), "P": (-45.67, 26.43)}, "Q3": {"F": (-4.68, 21.42), "P": (-59.01, 38.81)}}
BKEY = {"Q25": "s75", "Q3": "xm600"}
PRINT_LABEL = {"ABSTAIN": "NOT CERTIFIED (ABSTAIN; §4.1, excluded from V_c, V_n and counts by B2)"}
LABEL_DIRS = ("vsps_labels",)
DENY = (".vsps_sealed", "bpa1pull_1108", "machines/hbt1")


class Fault(Exception):
    pass


# ------------------------------------------------------------------------------------------------ custody
_LABEL_OK: set[str] = set()


def refused(path) -> bool:
    p = os.path.abspath(os.fsdecode(path))
    low = p.replace(os.sep, "/").lower()
    if any(d in low for d in DENY):
        return True
    return any(f"/{d}/" in low + "/" for d in LABEL_DIRS) and p not in _LABEL_OK


def _audit(event: str, args) -> None:
    if event in ("open", "os.listdir", "os.scandir") and args and \
            isinstance(args[0], (str, bytes, os.PathLike)) and refused(args[0]):
        raise Fault(f"custody: {event} refused")


def sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def committed(rel: str) -> bool:
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{rel}"], capture_output=True)
    return r.returncode == 0 and hashlib.sha256(r.stdout).hexdigest() == sha(ROOT / rel)


def check_pins() -> dict:
    out = {}
    for p, want in PINS.items():
        h = sha(ROOT / p)
        if want and not h.startswith(want):
            raise Fault(f"pin mismatch: {p}")
        out[p] = h
    return out


def write_atomic(path: Path, obj: dict) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp_")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, indent=1, ensure_ascii=False, default=float) + "\n")
    os.replace(tmp, path)
    return sha(path)


# ------------------------------------------------------------------------------------------------ §4 certificate math
def c_of(w):
    return (1 - w) / (2 * w)


def beta_B(cell: dict, w, a_s) -> float:
    """V-B (A2 plan §3.5): c f1 + (1+c)L/3 + sqrt(((1+c)L/3)^2 + 2c(1+c) f1+ L)."""
    c, f1, L = c_of(w), cell["f1"], math.log(2 / a_s)
    f1p = f1 + L + math.sqrt(L * L + 2 * L * f1)
    t = (1 + c) * L / 3
    return c * f1 + t + math.sqrt(t * t + 2 * c * (1 + c) * f1p * L)


def beta_H(cell: dict, w, a_s) -> float:
    """V-H (A2 plan §3.5, secondary): c f1 + (1+c) sqrt(1/2 sum_i |O_i|^2 ln(1/a_s))."""
    c = c_of(w)
    return c * cell["f1"] + (1 + c) * math.sqrt(0.5 * sum(s * s for s in cell["sz"]) * math.log(1 / a_s))


def cap(cell: dict, w, a_s, beta=beta_B) -> int:
    return cell["U"] if w == 0 else min(cell["U"], math.floor(beta(cell, w, a_s)))


def delta_min(tA, nA, tB, nB, XB, XS) -> Fr:
    """§4.1 worst case over the box, exact."""
    return Fr(tA, nA) - Fr(tB + XB, nB) + min(Fr(0), Fr(1, nA) - Fr(1, nB)) * XS


def certify(pc: dict, w, a_s=ALPHA_S, beta=beta_B) -> dict:
    """§4.1 verdict of one pair; A is the side with the higher observed t/n; tie = ABSTAIN; n = 0 = NOT DEFINED."""
    if pc["nA"] == 0 or pc["nB"] == 0:
        return {"verdict": "NOT DEFINED", "dmin": None, "better": None}
    pa, pb = Fr(pc["tA"], pc["nA"]), Fr(pc["tB"], pc["nB"])
    if pa == pb:
        return {"verdict": "ABSTAIN", "dmin": None, "better": None}
    a, b = ("A", "B") if pa > pb else ("B", "A")
    d = delta_min(pc["t" + a], pc["n" + a], pc["t" + b], pc["n" + b], cap(pc[b], w, a_s, beta), cap(pc["S"], w, a_s, beta))
    return {"verdict": "CERTIFIED" if d > 0 else "NOT CERTIFIED", "dmin": d, "better": a}


def w_star(pc: dict, a_s=ALPHA_S, beta=beta_B):
    """Break-down floor: 0 if certified at w = 0; NI if not at w = 1; else 30 bisection steps on [0.001, 1]."""
    ok = lambda w: certify(pc, w, a_s, beta)["verdict"] == "CERTIFIED"  # noqa: E731
    if certify(pc, 0.0, a_s, beta)["verdict"] in ("ABSTAIN", "NOT DEFINED"):
        return None
    if ok(0.0):
        return 0.0
    if not ok(1.0):
        return "NI"
    lo, hi = W_LO, 1.0
    if ok(lo):
        return lo
    for _ in range(BISECT):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if ok(mid) else (mid, hi)
    return hi


def corner(x, lo, hi, slope):
    """§4.1 slope interval: above the mean ln M take the low end for the minimum, below it the high end."""
    x = np.asarray(x, float)
    up = x > x.mean()
    return slope(x, np.where(up, lo, hi)), slope(x, np.where(up, hi, lo))


def ols(x, y) -> float:
    x, y = np.asarray(x, float), np.asarray(y, float)
    dx = x - x.mean()
    return float((dx * (y - y.mean())).sum() / (dx ** 2).sum())


# ------------------------------------------------------------------------------------------------ golds and cells
def draw_two(refs_all: list, ids: list, first_two: bool = False) -> tuple[list, dict]:
    """§4.2: two references per image; the 3-reference images draw once, ascending id, choice(3, 2)."""
    rng, out, picks = np.random.default_rng(SEED), [], {}
    for i, rs in sorted(zip(ids, refs_all), key=lambda t: t[0]):
        j = [0, 1] if len(rs) == 2 or first_two else sorted(int(x) for x in rng.choice(len(rs), 2, replace=False))
        if len(rs) == 3:
            picks[i] = j
        out.append((i, [rs[j[0]], rs[j[1]]]))
    d = dict(out)
    return [d[i] for i in ids], picks


def gold_ref(two: list, vm: set) -> list:
    return [{"kp": (r1 | r2) & vm, "ka": set(), "once": (r1 ^ r2) & vm, "twice": r1 & r2 & vm} for r1, r2 in two]


def gold_label(oi: list) -> list:
    return [{"kp": {c for c, s in d.items() if s == "present"}, "ka": {c for c, s in d.items() if s == "absent"},
             "once": set(), "twice": set()} for d in oi]


def cell_of(sets: list, gold: list, idx) -> dict:
    U = f1 = 0
    sz = []
    for k in idx:
        m, gd = sets[k], gold[k]
        U += len(m - gd["kp"] - gd["ka"])
        f1 += len(m & gd["once"])
        sz.append(len(m))
    return {"U": U, "f1": f1, "sz": sz}


def pair_cells(ms: dict, A: str, B: str, gold: list, idx) -> dict:
    a, b = ms[A], ms[B]
    return {"nA": sum(len(a[k]) for k in idx), "nB": sum(len(b[k]) for k in idx),
            "tA": sum(len(a[k] & gold[k]["kp"]) for k in idx), "tB": sum(len(b[k] & gold[k]["kp"]) for k in idx),
            "A": cell_of([x - y for x, y in zip(a, b)], gold, idx), "B": cell_of([y - x for x, y in zip(a, b)], gold, idx),
            "S": cell_of([x & y for x, y in zip(a, b)], gold, idx)}


def sys_cell(ms: dict, s: str, gold: list, idx) -> dict:
    m = ms[s]
    c = cell_of(m, gold, idx)
    return {**c, "n": sum(len(m[k]) for k in idx), "t": sum(len(m[k] & gold[k]["kp"]) for k in idx),
            "phi1": sum(len(m[k] & gold[k]["once"]) for k in idx), "phi2": sum(len(m[k] & gold[k]["twice"]) for k in idx)}


# ------------------------------------------------------------------------------------------------ labels -> status
def answers(lines) -> dict:
    """Last line of a qid is its answer."""
    out = {}
    for ln in lines:
        if ln.strip():
            r = json.loads(ln)
            out[r["qid"]] = r["label"]
    return out


def human(key: dict, ans: dict, syn: dict) -> tuple[dict, int]:
    """(image, class) -> Y | N | None for part-1 targets only (controls and part 3 never enter a status). No
    propagation: each pair keeps its own answer; same-map synonym disagreements are only counted."""
    h = {}
    for q, k in key.items():
        if k["role"] == "target" and k["part"] == 1:
            a = ans.get(q)
            h[(k["image"], k["class"])] = a if a in ("Y", "N") else None
    grp = defaultdict(set)
    for (i, c), a in h.items():
        if a:
            grp[(i, syn.get(c, c))].add(a)
    return h, sum(len(v) > 1 for v in grp.values())


def counts(w: dict, s: str, h: dict) -> dict:
    """Per image (all ids) over distinct mapped classes: pm, am (Open Images), hy, hn (human), rem."""
    n = len(w["ids"])
    o = {k: np.zeros(n) for k in ("pm", "am", "hy", "hn", "rem")}
    for k, i in enumerate(w["ids"]):
        for c in w["ms"][s][k]:
            st = w["oi"][k].get(c)
            a = h.get((i, c)) if st is None else None
            key = {"present": "pm", "absent": "am"}.get(st) or {"Y": "hy", "N": "hn"}.get(a, "rem")
            o[key][k] += 1
    return o


def pc_ends(cn: dict, W: np.ndarray, idx) -> dict:
    """Completed precision P_c and its remainder ends, one value per weight row."""
    g = {k: W @ v[idx] for k, v in cn.items()}
    num, den = g["pm"] + g["hy"], g["pm"] + g["am"] + g["hy"] + g["hn"]
    with np.errstate(invalid="ignore", divide="ignore"):
        return {"reg": num / den, "lo": num / (den + g["rem"]), "hi": (num + g["rem"]) / (den + g["rem"])}


def confirmed(ea: dict, eb: dict) -> np.ndarray:
    """Truth (§6 H2): P_c(A) - P_c(B) > 0 at the registered value and both ends; a tie or NaN is not confirmed."""
    return np.all([ea[k] - eb[k] > 0 for k in ("reg", "lo", "hi")], axis=0)


# ------------------------------------------------------------------------------------------------ verdict rules
def h1a_rule(pt, ci, lo, hi) -> str:
    """B1: PASS/FAIL only if the rule holds at the registered value and both ends; CI at the registered value only."""
    p_reg, f_reg = pt > 0 and ci is not None and ci[0] > 0, pt <= 0
    if p_reg and lo > 0 and hi > 0:
        return "PASS"
    if f_reg and lo <= 0 and hi <= 0:
        return "FAIL"
    return "INCONCLUSIVE (remainder)" if p_reg or f_reg else "INCONCLUSIVE"


def h1_inside_rule(pt, lo, hi, a, b) -> str:
    ins = [a <= x <= b for x in (pt, lo, hi)]
    return "PASS" if all(ins) else "FAIL" if not any(ins) else "INCONCLUSIVE (remainder)"


def h2a_rule(prs: list) -> dict:
    """B2: ABSTAIN and NOT DEFINED pairs are excluded before every count."""
    ev = [p for p in prs if p["verdict"] in ("CERTIFIED", "NOT CERTIFIED")]
    ce = [p for p in ev if p["verdict"] == "CERTIFIED"]
    ot = [p for p in ev if p["verdict"] == "NOT CERTIFIED"]
    bad, lim = sum(not p["confirmed"] for p in ce), math.floor(SHARE * len(ce))
    Vc = (len(ce) - bad) / len(ce) if ce else None
    Vn = sum(p["confirmed"] for p in ot) / len(ot) if ot else None
    if len(ce) < N_MIN or len(ot) < N_MIN:
        lab = "NOT EVALUABLE"
    elif bad > lim:
        lab = "FAIL"
    else:
        lab = "PASS" if Vc > Vn else "VALID, NOT DISCRIMINATING"
    return {"label": lab, "n_cert": len(ce), "n_other": len(ot), "n_excluded": len(prs) - len(ev),
            "n_cert_unconfirmed": bad, "limit": lim, "V_c": Vc, "V_n": Vn,
            "refuted_by_error_rule": bad > lim}


def h2b_rule(covered: list, binds: int) -> str:
    if binds == 0:
        return "PASS (vacuous)"
    return "PASS" if sum(covered) >= H2B_PASS else "FAIL"


def h3_rule(phi1, phi2, d_star, dhi_star) -> str:
    if phi2 == 0 or phi1 + phi2 < H3_MIN:
        return "NOT EVALUABLE"
    if np.percentile(d_star, 2.5) > 0:
        return "RESPECTED"
    if np.percentile(dhi_star, 97.5) < 0:
        return "VIOLATED"
    return "INCONCLUSIVE"


def null_select(prs: list, n_cert: int) -> dict:
    """§6 null rules on the evaluable pairs (label-free, fixed at the freeze): constant = all; margin = the n_cert
    largest exact |dt/n| (Fractions), ties by ascending pair index (B2); length = the better side names strictly more."""
    ev = [p for p in prs if p["verdict"] in ("CERTIFIED", "NOT CERTIFIED")]
    return {"constant": [p["idx"] for p in ev],
            "margin": [p["idx"] for p in sorted(ev, key=lambda p: (-p["dabs"], p["idx"]))[:n_cert]],
            "length": [p["idx"] for p in ev if p["n_better"] > p["n_worse"]]}


def h2d_scores(prs: list) -> list:
    """v1.3 §2 (from FREEZE): w* ascending (score -w*, NI lowest and tied), the exact two-reference margin (rank of the
    Fraction), the binary length rule; each as the doubled win matrix 2*1[s_i > s_j] + 1[s_i = s_j], no tie-break."""
    if any(p["w_star"] == 0 for p in prs):
        raise Fault("§V.4a: w* = 0")
    m = sorted({p["dabs"] for p in prs})
    S = [[-math.inf if p["w_star"] == "NI" else -p["w_star"] for p in prs], [m.index(p["dabs"]) for p in prs],
         [int(p["n_better"] > p["n_worse"]) for p in prs]]
    return [2 * (a[:, None] > a[None, :]) + (a[:, None] == a[None, :]) for a in (np.array(s, float) for s in S)]


def h2d_rule(prs: list, Y) -> dict:
    """v1.3 §1, §3: ABSTAIN and NOT DEFINED excluded first; Y = confirmed status, row 0 the point, rows 1.. the
    replicates, one column per pair; D = AUC(w*) - max(AUC margin, AUC length); an empty class gives D* = -1."""
    ev = [k for k, p in enumerate(prs) if p["verdict"] in ("CERTIFIED", "NOT CERTIFIED")]
    P, Y = [prs[k] for k in ev], np.asarray(Y, bool)[:, ev]
    Yf = Y.astype(float)
    num, n10 = [((Yf @ s) * (1 - Yf)).sum(1) for s in h2d_scores(P)], Yf.sum(1) * (1 - Yf).sum(1)
    n1, n0 = int(Y[0].sum()), int((~Y[0]).sum())
    with np.errstate(invalid="ignore", divide="ignore"):
        A = [x / (2 * n10) for x in num]
        ds = np.where(n10[1:] > 0, A[0][1:] - np.maximum(A[1][1:], A[2][1:]), -1.0)
    auc = [Fr(int(x[0]), 2 * n1 * n0) for x in num] if n1 and n0 else [None] * 3
    D = auc[0] - max(auc[1:]) if n1 and n0 else None
    ci, N = np.percentile(ds, [2.5, 97.5]), n1 + n0
    lab = "NOT EVALUABLE" if n1 < H2D_MIN or n0 < H2D_MIN else \
        "PASS" if D >= H2D_SESOI and np.percentile(ds, 2.5) > 0 else "FAIL"
    if lab == "PASS":
        read = ("the break-down floor w* ranked the robustness of comparisons better than the observed margin and the "
                f"length rule on a new benchmark's human-completed gold (single annotator, {N} dependent pairs)")
    elif lab == "FAIL":
        read = (f"On the human-completed gold of XM3600-600 (single annotator, {N} dependent pairs), the break-down "
                "floor w* did not rank the comparisons better than the observed two-reference margin and the length rule"
                f" by the registered amount (D = {float(D):.3f}, 95% interval {ci[0]:.3f} to {ci[1]:.3f}; SESOI 0.10). "
                f"With {N} dependent pairs the test has low power; this result alone does not show that w* ranks worse.")
    else:
        read = f"H2d could not be evaluated: {n1} confirmed and {n0} unconfirmed pairs, at least 5 of each needed."
    return {"label": lab, "printed_label": H2D_LABEL, "reading": read,
            "fail_adds": "the rule with the larger AUC (margin or length) ranked them better than w* here"
            if lab == "FAIL" and ci[1] < 0 else None,
            "n1": n1, "n0": n0, "n_excluded": len(prs) - len(P), "n_NI": sum(p["w_star"] == "NI" for p in P),
            "AUC_w_star_margin_length": auc, "D": D, "D_ci95": ci.tolist(),
            "D_star_p036_bonferroni7": float(np.percentile(ds, BONF7)), "D_star_p036_label": BONF7_TXT,
            "n_replicates": len(ds),
            "n_replicates_empty_class": int((n10[1:] == 0).sum())}


# ------------------------------------------------------------------------------------------------ score-side rows (CC-343)
def ctl_row(got: list, want: str) -> dict:
    """Plan §4 control agreement of one group (descriptive, gates nothing): answers equal to the Open Images answer."""
    agree, yn = sum(a == want for a in got), sum(a in ("Y", "N") for a in got)
    return {"n": len(got), "agree": agree, "agreement_of_all": agree / len(got) if got else None,
            "agreement_among_YN": agree / yn if yn else None, "Y": got.count("Y"), "N": got.count("N"),
            "U": got.count("U"), "A": got.count("A"), "unanswered": got.count(None)}


def hint_full(w: dict, i: str, c: str) -> bool:
    """S1: full hint coverage iff every MID of vmap[c]["pos"] is among the image's verified-absent MIDs."""
    return w["pos_mids"][c] <= w["oi_neg"].get(i, frozenset())


def repeat_label(k: int, n: int) -> str:
    """CC-343 Ruling 4: part 3 may be partial at the part-1 unsealing."""
    return f"{k} of {n}" if k == n else f"partial ({k} of {n} answered at the part-1 unsealing)"


def completed_sets(w: dict, h: dict) -> tuple[list, list]:
    """Per image: present = OI present + human Y on part-1 targets; absent = OI absent + human N (S2 gold (ii)).
    With h = {} this is gold (i), the Open Images verified classes."""
    pres = [{c for c, s in o.items() if s == "present"} for o in w["oi"]]
    ab = [{c for c, s in o.items() if s == "absent"} for o in w["oi"]]
    pos = {i: k for k, i in enumerate(w["ids"])}
    for (i, c), a in h.items():
        if a == "Y":
            pres[pos[i]].add(c)
        elif a == "N":
            ab[pos[i]].add(c)
    return pres, ab


def gold_rows(w: dict, s: str, pres: list, ab: list, idx) -> dict:
    """Over distinct mapped classes per image, pooled over idx: recall = named present / present classes;
    hallucination = named absent / absent classes; share of captions naming at least one absent class."""
    m, P, A = [w["ms"][s][k] for k in idx], [pres[k] for k in idx], [ab[k] for k in idx]
    npos, nab = sum(map(len, P)), sum(map(len, A))
    return {"recall": sum(len(x & p) for x, p in zip(m, P)) / npos if npos else None,
            "hallucination": sum(len(x & a) for x, a in zip(m, A)) / nab if nab else None,
            "share_naming_absent": sum(bool(x & a) for x, a in zip(m, A)) / len(m) if m else None}


def f1_of(p, r):
    return 2 * p * r / (p + r) if p is not None and r is not None and p + r > 0 else None


def secondary_golds(w: dict, h: dict, cn: dict, idx) -> dict:
    """S2 (plan §5, v1.1 §10 row 2): per system, point values, the two golds never mixed in one row. Gold (i): the
    registered OI recall, F1 = 2 P_c R/(P_c + R) at reg, lo and hi. Gold (ii): F1 with P_c (reg); no verdict."""
    g1, g2 = completed_sets(w, {}), completed_sets(w, h)
    out = {"gold_i": {"label": "gold (i): Open Images verified classes, as registered", "systems": {}},
           "gold_ii": {"label": GOLD_II_LABEL, "verdict": None, "systems": {}}}
    for s in w["sys"]:
        e = {m: float(v[0]) for m, v in pc_ends(cn[s], np.ones((1, len(idx))), idx).items()}
        r1, r2 = gold_rows(w, s, *g1, idx), gold_rows(w, s, *g2, idx)
        out["gold_i"]["systems"][s] = {**r1, "P_c": e, "F1": {m: f1_of(p, r1["recall"]) for m, p in e.items()}}
        out["gold_ii"]["systems"][s] = {**r2, "P_c": e["reg"], "F1": f1_of(e["reg"], r2["recall"])}
    return out


def h3_row(w: dict, gr: list, h: dict, uni: list, Wb: np.ndarray, idx) -> dict:
    """S3 row 1 (v1.1 §6 H3 secondary): H3 on a universe uni of pairs per image. X = pairs named by neither reference
    that are OI present or human Y; X_hi adds the remainder (no OI status, no Y or N). No verdict."""
    per = {x: np.zeros(len(w["ids"])) for x in ("p1", "p2", "X", "Xhi")}
    for k in idx:
        i = w["ids"][k]
        per["p1"][k], per["p2"][k] = len(uni[k] & gr[k]["once"]), len(uni[k] & gr[k]["twice"])
        st = [(w["oi"][k].get(c), h.get((i, c))) for c in uni[k] - gr[k]["kp"]]
        per["X"][k] = sum(o == "present" or (o is None and a == "Y") for o, a in st)
        per["Xhi"][k] = per["X"][k] + sum(o is None and a is None for o, a in st)
    g = {x: Wb @ per[x][idx] for x in per}
    f0 = w["f0_hat"](g["p1"], g["p2"], 2, np.inf)
    D, Dhi = g["X"] - f0, g["Xhi"] - f0
    return {"phi1": float(g["p1"][0]), "phi2": float(g["p2"][0]), "f0_hat": float(f0[0]), "X": float(g["X"][0]),
            "X_hi": float(g["Xhi"][0]), "D": float(D[0]), "D_hi": float(Dhi[0]),
            "D_ci95": np.percentile(D[1:], [2.5, 97.5]).tolist(), "D_hi_ci95": np.percentile(Dhi[1:], [2.5, 97.5]).tolist(),
            "reading_no_verdict": h3_rule(g["p1"][0], g["p2"][0], D[1:], Dhi[1:])}


def dl_rule(d_star) -> str:
    """secondary (v1.1 §6): A-M1 D_L over all completed-present pairs; only "consistent" can be read"""
    return ("no reading (A-M1 VIOLATED rule met; v1.1 §6: only consistent can be read, the labels are not a complete "
            "inventory)") if np.percentile(np.asarray(d_star, float), 97.5) < 0 else "consistent"


def dl_row(w: dict, gr: list, pres: list, Wb: np.ndarray, idx) -> dict:
    """S3 row 2: the A-M1 form D_L = (L - S_hat)/L (A_M1_PLAN_v3 l.83, l.283; a_m1.compute_set) over the completed-present
    pairs: L = their number, S_hat = U + f0_hat(phi1, phi2, 2) with U, phi1, phi2 = those named by at least one, exactly
    one and both of the two references (§4.2 draw)."""
    per = {x: np.zeros(len(w["ids"])) for x in ("L", "U", "p1", "p2")}
    for k in idx:
        per["L"][k], per["U"][k] = len(pres[k]), len(pres[k] & gr[k]["kp"])
        per["p1"][k], per["p2"][k] = len(pres[k] & gr[k]["once"]), len(pres[k] & gr[k]["twice"])
    g = {x: Wb @ per[x][idx] for x in per}
    S = g["U"] + w["f0_hat"](g["p1"], g["p2"], 2, np.inf)
    with np.errstate(invalid="ignore", divide="ignore"):
        D = (g["L"] - S) / g["L"]
    return {"label_row": 'secondary (v1.1 §6): A-M1 D_L over all completed-present pairs; only "consistent" can be read',
            "L": float(g["L"][0]), "U_L": float(g["U"][0]), "phi1": float(g["p1"][0]), "phi2": float(g["p2"][0]),
            "S_hat": float(S[0]), "D_L": float(D[0]), "D_L_ci95": np.percentile(D[1:], [2.5, 97.5]).tolist(),
            "label": dl_rule(D[1:])}


# ------------------------------------------------------------------------------------------------ registered slopes
def mods():
    """score_g2b and evaluate_xm3600_predictions_v3 as bracket.py loads them (pins checked by the caller)."""
    sys.path[:0] = [str(ROOT / "scripts/n_f1"), str(ROOT / "scripts"), str(ROOT)]
    import bracket as br  # noqa: E402
    if not hasattr(br, "v"):
        br.load_modules()
    return br


def fam_slopes(w: dict, fam: str, add: dict | None = None) -> dict:
    """The registered slope loop of bracket.s75_bracket / g2b_bracket with the precision columns shifted by
    add[s] = (to present, to absent) per image; recall columns never change."""
    br, ctx = w["br"], w["ctx"][fam]
    v, g = br.v, br.g
    per = {}
    if ctx["name"] == "s75":
        B = v.B_MSTAR
        for s, d in ctx["systems"].items():
            a = d["a"].copy()
            if add:
                a[:, 1] += add[s][0]
                a[:, 2] += add[s][1]
            p, r = v.oi_draws_extended(a, ctx["full"], d["pr"]), v.oi_draws_extended(a, ctx["idx_boot"][:B], d["pr"])
            per[s] = {"P": (p["P_pos"][0], r["P_pos"]), "F": (p["F1_pos"][0], r["F1_pos"]), "R": (p["R_pos"][0], r["R_pos"]),
                      "lnM": (np.log(d["M_pt"]), np.log(np.maximum(d["M_dr"][:B], v.EPS9)))}
        slope = v.ols_slope
        ci = lambda x: [float(np.nanpercentile(x, v.PCT_LO)), float(np.nanpercentile(x, v.PCT_HI))]  # noqa: E731
    else:
        one = np.ones((1, len(ctx["idx"])))
        for s in ctx["systems"]:
            r0 = ctx["rows"][s]
            b1, bW = g.scores(r0, ctx["idx"], one), g.scores(r0, ctx["idx"], ctx["W"])
            p1, pW = (b1, bW) if not add else [g.scores({**r0, "pm": r0["pm"] + add[s][0], "am": r0["am"] + add[s][1]},
                                                        ctx["idx"], x) for x in (one, ctx["W"])]
            P, R = (p1["P"], pW["P"]), (b1["R"], bW["R"])  # as bracket.g2b_scores: P shifted, R from the OI rows
            F = [g.div(2 * p * r, p + r, 0.0) for p, r in zip(P, R)]
            per[s] = {"P": (100 * P[0][0], 100 * P[1]), "F": (100 * F[0][0], 100 * F[1]), "R": (R[0][0], R[1]),
                      "lnM": (np.log(b1["M"][0]), np.log(bW["M"]))}
        slope = lambda x, y: float(g.ols(np.asarray(x, float), np.asarray(y, float)))  # noqa: E731
        ci = lambda x: g.ci(x, ctx["lo_q"], ctx["hi_q"])  # noqa: E731
    names = list(per)
    X = np.array([per[s]["lnM"][1] for s in names])
    xp = np.array([per[s]["lnM"][0] for s in names])
    out = {"per": per, "slope": slope, "ci": ci, "lnM": xp}
    for k in ("F", "P"):
        Y = np.array([per[s][k][1] for s in names])
        out[k] = (slope(xp, np.array([per[s][k][0] for s in names])),
                  np.array([slope(X[:, b], Y[:, b]) for b in range(X.shape[1])]))
    return out


def unknown_add(w: dict, fam: str, mode: str) -> dict:
    """Table S7.2 modes: lower = every unknown mapped mention absent; upper = present."""
    out = {}
    for s in w["fam"][fam]:
        u = np.array([sum(1 for c in m if c not in o) for m, o in zip(w["ms"][s], w["oi"])], float)
        out[s] = (u, 0 * u) if mode == "upper" else (0 * u, u)
    return out


def clabel_slope(w: dict, fam: str) -> dict:
    """§4.1/§5: label-gold slope range over all completions (outer corner), point and per bootstrap draw."""
    lo, hi = fam_slopes(w, fam, unknown_add(w, fam, "lower")), fam_slopes(w, fam, unknown_add(w, fam, "upper"))
    names, sl = list(lo["per"]), lo["slope"]
    out = {}
    for k in ("F", "P"):
        a = np.array([lo["per"][s][k][0] for s in names])
        b = np.array([hi["per"][s][k][0] for s in names])
        rng_pt = corner(lo["lnM"], a, b, sl)
        X = np.array([lo["per"][s]["lnM"][1] for s in names])
        A = np.array([lo["per"][s][k][1] for s in names])
        Bm = np.array([hi["per"][s][k][1] for s in names])
        reps = np.array([corner(X[:, j], A[:, j], Bm[:, j], sl) for j in range(X.shape[1])])
        out[k] = {"range": [float(rng_pt[0]), float(rng_pt[1])], "ci_min": lo["ci"](reps[:, 0]),
                  "ci_max": lo["ci"](reps[:, 1]), "certified_sign": bool(rng_pt[0] > 0 or rng_pt[1] < 0)}
    out["s72"] = {"lower": float(lo["F"][0]), "upper": float(hi["F"][0])}
    return out


# ------------------------------------------------------------------------------------------------ world (real data)
def _load_world() -> dict:
    """Label-free inputs. Matcher calls as build_assignment.py l.74/l.78; slopes through bracket.py contexts."""
    sys.path[:0] = [str(ROOT / "scripts/n_f1"), str(ROOT / "tools/obj_rater"), str(ROOT / "scripts"), str(ROOT)]
    import bracket as br
    br.check_pins()
    br.load_modules()
    import build_assignment as ba
    from rescap.chair import objects_in
    xo = br.v.xo
    data = json.loads((ROOT / "data/datasets/xm3600/test_data.json").read_text(encoding="utf-8"))
    refs_txt = defaultdict(list)
    for a in data["annotations"]:
        refs_txt[str(a["image_id"])].append(a["caption"])
    ids = sorted(refs_txt)
    labels = {k: x for k, x in json.loads(xo.LABELS.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    vmap = xo.resolve_map(ROOT / "data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv")
    st = xo.statuses(vmap, labels)
    vm = set(vmap)
    systems, shas = ba.load_systems()
    names = json.loads((ROOT / BUILD).read_text(encoding="utf-8"))["counts"]["systems"]
    if sorted(systems) != names:
        raise Fault("systems differ from BUILD.json")
    ms_all = {s: [set(objects_in(systems[s][i])) for i in ids] for s in names}
    s75, g2 = br.s75_context(), br.g2b_context()
    if s75["ids"] != ids or list(g2["ids"]) != ids:
        raise Fault("image order differs between contexts")
    syn = {c: json.dumps([sorted(m["pos"]), sorted(m["neg"])]) for c, m in vmap.items()}
    return {"ids": ids, "sys": names, "vm": vm, "syn": syn, "ms_all": ms_all,
            "ms": {s: [m & vm for m in ms_all[s]] for s in names},
            "refs_all": [[set(objects_in(r)) for r in refs_txt[i]] for i in ids], "oi": [st.get(i, {}) for i in ids],
            "fam": {"Q25": list(s75["systems"]), "Q3": list(g2["systems"])},
            "idx": {"Q25": np.arange(len(ids)), "Q3": np.asarray(g2["idx"])}, "ctx": {"Q25": s75, "Q3": g2},
            "br": br, "pins": {**check_pins(), **shas}, "f0_hat": _p50x().f0_hat, "boot_weights": _a_m1().boot_weights}


def _p50x():
    sys.path[:0] = [str(ROOT / "scripts/pascal50s")]
    import p50x
    return p50x


def _a_m1():
    """CC-333 N10: importing a_m1 defines functions only; its custody hook is installed only by install_hook()."""
    sys.path[:0] = [str(ROOT / "scripts/a_m1")]
    import a_m1
    if a_m1._HOOK["on"]:
        raise Fault("a_m1 guard active on import")
    return a_m1


def _score_world() -> dict:
    """score's world: _load_world (unchanged, pinned inputs) plus, for S1, each class's `pos` MIDs and the verified-absent
    MIDs per image, from the same pinned oiv7_labels.json and class descriptions."""
    w = _load_world()
    xo = w["br"].v.xo
    labels = json.loads(xo.LABELS.read_text(encoding="utf-8"))
    vmap = xo.resolve_map(ROOT / "data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv")
    return {**w, "pos_mids": {c: m["pos"] for c, m in vmap.items()},
            "oi_neg": {i: set(labels[i]["neg"]) for i in w["ids"] if i in labels}}


# ------------------------------------------------------------------------------------------------ gate / freeze
def scope_of(w: dict, A: str, B: str) -> str:
    fa = next(f for f, m in w["fam"].items() if A in m)
    fb = next(f for f, m in w["fam"].items() if B in m)
    return fa if fa == fb else "cross"


def all_pairs(w: dict) -> list:
    return [(k, A, B, scope_of(w, A, B)) for k, (A, B) in enumerate(itertools.combinations(w["sys"], 2))]


def idx_of(w: dict, scope: str):
    return w["idx"]["Q25"] if scope == "Q25" else w["idx"]["Q3"]


def freeze_core(w: dict) -> dict:
    two, picks = draw_two(w["refs_all"], w["ids"])
    two_f, _ = draw_two(w["refs_all"], w["ids"], first_two=True)
    gr, gr_f, gl = gold_ref(two, w["vm"]), gold_ref(two_f, w["vm"]), gold_label(w["oi"])
    js = lambda r: {"verdict": r["verdict"], "dmin": None if r["dmin"] is None else float(r["dmin"]),  # noqa: E731
                    "better": r["better"], "label": PRINT_LABEL.get(r["verdict"], r["verdict"])}
    pairs = []
    for k, A, B, sc in all_pairs(w):
        idx = idx_of(w, sc)
        pc, pcf, pl = pair_cells(w["ms"], A, B, gr, idx), pair_cells(w["ms"], A, B, gr_f, idx), \
            pair_cells(w["ms"], A, B, gl, idx)
        grid = {str(x): js(certify(pc, x)) for x in GRID}
        bt = grid[str(W0)]["better"]
        nb, nw = (pc["nA"], pc["nB"]) if bt == "A" else (pc["nB"], pc["nA"])
        pairs.append({"idx": k, "A": A, "B": B, "scope": sc, "n_images": len(idx),
                      "cells": {**{x: pc[x] for x in ("nA", "nB", "tA", "tB")},
                                **{x: {"U": pc[x]["U"], "f1": pc[x]["f1"]} for x in ("A", "B", "S")}},
                      "cref": grid, "w_star": w_star(pc),
                      "vh": {str(x): certify(pc, x, beta=beta_H)["verdict"] for x in GRID},
                      "first_two": {str(x): certify(pcf, x)["verdict"] for x in GRID},
                      "clabel": js(certify(pl, 0.0)),
                      "dabs": float(abs(Fr(pc["tA"], pc["nA"]) - Fr(pc["tB"], pc["nB"]))) if pc["nA"] and pc["nB"] else None,
                      "dabs_exact": abs(Fr(pc["tA"], pc["nA"]) - Fr(pc["tB"], pc["nB"])) if pc["nA"] and pc["nB"] else None,
                      "n_better": nb, "n_worse": nw})
    within = [p for p in pairs if p["scope"] != "cross"]
    sel = null_select([{"verdict": p["cref"][str(W0)]["verdict"], "dabs": p["dabs_exact"], "idx": p["idx"],
                        "n_better": p["n_better"], "n_worse": p["n_worse"]} for p in within],
                      sum(p["cref"][str(W0)]["verdict"] == "CERTIFIED" for p in within))
    for p in pairs:
        p.pop("dabs_exact")
    by_w = {str(x): sum(p["cref"][str(x)]["verdict"] == "CERTIFIED" for p in within) for x in GRID}
    w_ev = next((x for x in GRID if by_w[str(x)] >= N_MIN), "none")
    ev = lambda x: [{"verdict": p["cref"][str(x)]["verdict"], "confirmed": True} for p in within]  # noqa: E731
    decl = {str(x): {k: h2a_rule(ev(x))[k] for k in ("n_cert", "n_other", "n_excluded", "label")} for x in GRID}
    for d in decl.values():
        d["evaluable"] = d.pop("label") != "NOT EVALUABLE"
    # §4.4 and H2b on I600 per system
    i600 = w["idx"]["Q25"]
    f0 = w["f0_hat"]
    sysrows = {}
    for s in w["sys"]:
        c = sys_cell(w["ms"], s, gr, i600)
        Lh = float(f0(c["phi1"], c["phi2"], 2, np.inf))
        b = {str(x): (None if x == 0 else beta_B(c, x, ALPHA_S)) for x in GRID}
        oi_pres = sum(1 for k in i600 for m in [w["ms"][s][k] - gr[k]["kp"]] for cc in m if w["oi"][k].get(cc) == "present")
        sysrows[s] = {"n": c["n"], "t": c["t"], "U": c["U"], "f1": c["f1"], "phi1": c["phi1"], "phi2": c["phi2"],
                      "L_hat": Lh, "low": (c["t"] + Lh) / c["n"] if c["n"] else None, "beta": b,
                      "high": {str(x): (c["t"] + cap(c, x, ALPHA_S)) / c["n"] if c["n"] else None for x in GRID},
                      "floor_beta_w0": math.floor(b[str(W0)]), "oi_present_in_Ns": oi_pres,
                      "binds": math.floor(b[str(W0)]) < c["U"]}
    above = sum(r["oi_present_in_Ns"] > r["floor_beta_w0"] for r in sysrows.values())
    # slopes: C-ref (alpha/m) and C-label (corner range = §5 STOP ranges)
    slopes = {}
    for fam in ("Q25", "Q3"):
        reg = fam_slopes(w, fam)
        x = reg["lnM"]
        cr = {}
        for wv in GRID:
            lo_, hi_ = [], []
            for s in reg["per"]:
                c = sys_cell(w["ms"], s, gr, w["idx"][fam])
                lo_.append(100 * c["t"] / c["n"])
                hi_.append(100 * (c["t"] + cap(c, wv, ALPHA / M_FAM)) / c["n"])
            r = corner(x, np.array(lo_), np.array(hi_), reg["slope"])
            cr[str(wv)] = {"range": [float(r[0]), float(r[1])], "certified_sign": bool(r[0] > 0 or r[1] < 0)}
        slopes[fam] = {"cref_P": cr, "clabel": clabel_slope(w, fam),
                       "registered_F": float(reg["F"][0]), "registered_P": float(reg["P"][0])}
    # H3 universe
    named = [set().union(*(w["ms"][s][k] for s in w["sys"])) for k in range(len(w["ids"]))]
    nu = [{c for c in named[k] if c not in w["oi"][k]} for k in range(len(w["ids"]))]
    p1 = sum(len(nu[k] & gr[k]["once"]) for k in i600)
    p2 = sum(len(nu[k] & gr[k]["twice"]) for k in i600)
    if any(p["cref"]["0.0"]["verdict"] == "CERTIFIED" for p in pairs) or \
            any(s["cref_P"]["0.0"]["certified_sign"] for s in slopes.values()):
        raise Fault("§V.4a: a C-ref certificate at w = 0")
    return {"schema": "vsps.a_cert.freeze.v1", "status": "development (no labels)", "pins": w["pins"],
            "constants": {"alpha": ALPHA, "alpha_S": ALPHA_S, "alpha_slope": ALPHA / M_FAM, "grid": GRID, "w0": W0,
                          "seed": SEED, "B_truth": B_TRUTH, "N_min": N_MIN, "share": SHARE},
            "refs_draw": picks, "pairs": pairs, "nulls_w0": sel, "certified_by_w_within": by_w, "w_ev": w_ev,
            "h2a_declared": decl, "h2a_evaluable_w0": decl[str(W0)]["evaluable"], "intervals_44": sysrows,
            "h2b_declared": {"n_binding": sum(r["binds"] for r in sysrows.values()), "n_oi_above_budget": above,
                             "determined": "FAIL" if above >= 2 else None},
            "slopes": slopes, "h3": {"N_u": sum(len(nu[k]) for k in i600), "phi1": p1, "phi2": p2,
                                     "f0_hat": float(f0(p1, p2, 2, np.inf)),
                                     "evaluable": not (p2 == 0 or p1 + p2 < H3_MIN)}}


def gate_core(w: dict, assign: dict, build: dict, bracket_res: dict) -> list:
    cells = []

    def chk(name, got, want, tol=0.0):
        ok = (abs(got - want) <= tol) if isinstance(want, float) else got == want
        cells.append({"check": name, "got": got, "want": want, "ok": bool(ok)})

    named = defaultdict(set)
    for s in w["sys"]:
        for k, i in enumerate(w["ids"]):
            for c in w["ms_all"][s][k]:
                named[(i, c)].add(s)
    for k, i in enumerate(w["ids"]):
        for r in w["refs_all"][k]:
            for c in r:
                named[(i, c)].add("reference")
    pos = {i: k for k, i in enumerate(w["ids"])}
    t1 = sorted(p for p in named if p[1] in w["vm"] and p[1] not in w["oi"][pos[p[0]]])
    chk("named_pairs", len(named), build["counts"]["named_pairs"])
    chk("named_pairs_registered", len(named), N_NAMED)
    chk("part1_targets", len(t1), N_TARGETS1)
    part1 = {q["qid"] for s in assign["screens"] if s["part"] == 1 for q in s["q"]}
    q1 = {hashlib.sha256(f"{SEED}|1|{i}|{c}".encode()).hexdigest()[:12] for i, c in t1}
    chk("part1_targets_subset_of_assignment_part1", q1 <= part1, True)
    chk("part1_minus_targets", len(part1) - len(t1), N_CTRL)
    for fam in ("Q25", "Q3"):
        reg = fam_slopes(w, fam)
        chk(f"{fam} registered F slope", float(round(reg["F"][0], 4 if fam == "Q25" else 5)), REG_SLOPE[fam])
        for mode in ("registered", "lower", "upper"):
            r = reg if mode == "registered" else fam_slopes(w, fam, unknown_add(w, fam, mode))
            ref = bracket_res["sets"][BKEY[fam]]["slopes"][mode]
            chk(f"{fam} {mode} F slope = bracket_result", float(r["F"][0]), float(ref["point"]), 1e-9)
            chk(f"{fam} {mode} F CI = bracket_result", max(abs(a - b) for a, b in zip(r["ci"](r["F"][1]),
                                                                                      ref["ci95_raw"])), 0.0, 1e-9)
        cl = clabel_slope(w, fam)  # through the same fam_slopes that score uses
        for mode, end in (("lower", 0), ("upper", 1)):
            chk(f"{fam} S7.2 {mode} (2dp)", round(cl["s72"][mode], 2), S72[fam][end])
        for k in ("F", "P"):
            chk(f"{fam} §5 {k} range (2dp)", [round(x, 2) for x in cl[k]["range"]], list(S5[fam][k]))
        ctx = w["ctx"][fam]
        for s in w["fam"][fam]:
            pm = ctx["systems"][s]["a"][:, 1] if ctx["name"] == "s75" else ctx["rows"][s]["pm"]
            mine = np.array([sum(w["oi"][k].get(c) == "present" for c in w["ms"][s][k]) for k in range(len(w["ids"]))])
            chk(f"{fam} {s} present mentions per image = context", bool(np.array_equal(pm, mine)), True)
        v = w["br"].v
        for s in w["fam"][fam]:
            if ctx["name"] == "xm600":
                ment = ctx["ds"].ment(s, ctx["lx"])
            else:
                caps = v.load_preds_file(ROOT / f"data/results/xm3600/{s}.preds.json")
                ment = [set(v.objects_in(caps[i], raw_tone=False)) for i in w["ids"]]
            chk(f"{fam} {s} mention sets = objects_in as build_assignment", ment == w["ms_all"][s], True)
    return cells


# ------------------------------------------------------------------------------------------------ score
def score_core(w: dict, fz: dict, key: dict, ans: dict) -> dict:
    h, syn_dis = human(key, ans, w["syn"])
    cn = {s: counts(w, s, h) for s in w["sys"]}
    n = len(w["ids"])
    i600 = w["idx"]["Q25"]
    # (1) quality figures of plan §4 (gate nothing)
    exp = {"ctrl_present": "Y", "ctrl_absent": "N", "foil_absent": "N"}
    ctl = [ans.get(q) for q, k in key.items() if k["role"] in exp]
    agree = sum(a == exp[k["role"]] for q, k in key.items() if k["role"] in exp for a in [ans.get(q)])
    t1 = {(k["image"], k["class"]): ans.get(q) for q, k in key.items() if k["part"] == 1 and k["role"] == "target"}
    rep = [ans.get(q) == t1.get((k["image"], k["class"])) for q, k in key.items() if k["part"] == 3 and q in ans]
    ua = defaultdict(lambda: [0, 0])
    for q, k in key.items():
        if k["part"] == 1 and k["role"] == "target" and q in ans:
            ua[k["class"]][0] += ans[q] in ("U", "A")
            ua[k["class"]][1] += 1
    quality = {"control_agreement_of_all": agree / len(ctl) if ctl else None, "n_control": len(ctl),
               "control_agreement_among_YN": agree / max(1, sum(a in ("Y", "N") for a in ctl)),
               "control_U": sum(a == "U" for a in ctl), "control_A": sum(a == "A" for a in ctl),
               "repeat_agreement": float(np.mean(rep)) if rep else None, "n_repeat": len(rep),
               "UA_rate_by_class": {c: a / b for c, (a, b) in sorted(ua.items())}, "synonym_disagreements": syn_dis}
    # S1 (plan §4; CC-343 Ruling 5): per role, and the absent controls split by hint coverage (label-free membership)
    c1 = [(k, ans.get(q)) for q, k in key.items() if k["part"] == 1 and k["role"] in exp]
    quality["control_by_role"] = {r: ctl_row([a for k, a in c1 if k["role"] == r], e) for r, e in exp.items()}
    quality["control_absent_by_hint_coverage"] = {cov: ctl_row([a for k, a in c1 if k["role"] != "ctrl_present" and
                                                                hint_full(w, k["image"], k["class"]) == (cov == "full")],
                                                               "N") for cov in ("full", "partial")}
    quality["repeat_answered"] = repeat_label(len(rep), sum(k["part"] == 3 for k in key.values()))
    # (2) H3
    two, _ = draw_two(w["refs_all"], w["ids"])
    gr = gold_ref(two, w["vm"])
    named = [set().union(*(w["ms"][s][k] for s in w["sys"])) for k in range(n)]
    nu = [{c for c in named[k] if c not in w["oi"][k]} for k in range(n)]
    per = {x: np.zeros(n) for x in ("p1", "p2", "X", "Xhi")}
    for k in i600:
        i = w["ids"][k]
        per["p1"][k] = len(nu[k] & gr[k]["once"])
        per["p2"][k] = len(nu[k] & gr[k]["twice"])
        nn = nu[k] - gr[k]["kp"]
        per["X"][k] = sum(h.get((i, c)) == "Y" for c in nn)
        per["Xhi"][k] = per["X"][k] + sum(h.get((i, c)) is None for c in nn)
    Wb = w["boot_weights"](len(i600), np.random.default_rng(SEED), B_TRUTH)
    g = {x: Wb @ per[x][i600] for x in per}
    f0 = w["f0_hat"](g["p1"], g["p2"], 2, np.inf)
    D, Dhi = g["X"] - f0, g["Xhi"] - f0
    h3 = {"phi1": float(g["p1"][0]), "phi2": float(g["p2"][0]), "f0_hat": float(f0[0]), "X": float(g["X"][0]),
          "X_hi": float(g["Xhi"][0]), "D": float(D[0]), "D_hi": float(Dhi[0]),
          "D_ci95": np.percentile(D[1:], [2.5, 97.5]).tolist(), "D_hi_ci95": np.percentile(Dhi[1:], [2.5, 97.5]).tolist(),
          "D_bonf": np.percentile(D[1:], [BONF, 100 - BONF]).tolist(),
          "label": h3_rule(g["p1"][0], g["p2"][0], D[1:], Dhi[1:]),
          "ratio_X_f0": float(g["X"][0] / f0[0]) if f0[0] else None,
          "n_ref_named_completed_absent": int(sum(1 for k in i600 for c in gr[k]["kp"] if w["oi"][k].get(c) == "absent"
                                                   or h.get((w["ids"][k], c)) == "N"))}
    # (3) H2b
    one = np.ones((1, n))
    rows = {}
    for s in w["sys"]:
        c = sys_cell(w["ms"], s, gr, i600)
        x = xh = 0
        for k in i600:
            i = w["ids"][k]
            for cc in w["ms"][s][k] - gr[k]["kp"]:
                st = w["oi"][k].get(cc)
                x += st == "present" or (st is None and h.get((i, cc)) == "Y")
                xh += st == "present" or (st is None and h.get((i, cc)) in ("Y", None))
        b = {str(wv): (None if wv == 0 else beta_B(c, wv, ALPHA_S)) for wv in GRID}
        e = pc_ends(cn[s], one, i600)
        rows[s] = {"x": int(x), "x_hi": int(xh), "U": c["U"], "f1": c["f1"], "beta": b,
                   "covered": xh <= math.floor(b[str(W0)]), "w_hat": c["f1"] / (c["f1"] + 2 * x) if c["f1"] + x else None,
                   "low_44": fz["intervals_44"][s]["low"], "P_c": float(e["reg"][0])}
    binds = sum(math.floor(r["beta"][str(W0)]) < r["U"] for r in rows.values())
    h2b = {"systems": rows, "n_covered": sum(r["covered"] for r in rows.values()), "n_binding": binds,
           "label": h2b_rule([r["covered"] for r in rows.values()], binds)}
    # (4) H2a: certified set and orientation from FREEZE, never recomputed
    Wt = w["boot_weights"](n, np.random.default_rng(SEED), B_TRUTH)
    prs = []
    for p in fz["pairs"]:
        idx = idx_of(w, p["scope"])
        Wi = Wt[:, idx]
        ea, eb = pc_ends(cn[p["A"]], Wi, idx), pc_ends(cn[p["B"]], Wi, idx)
        bt = p["cref"][str(W0)]["better"]
        cf = confirmed(ea, eb) if bt == "A" else confirmed(eb, ea) if bt == "B" else np.zeros(Wi.shape[0], bool)
        hi_a, lo_b = (ea, eb) if bt == "A" else (eb, ea)
        prs.append({"idx": p["idx"], "scope": p["scope"], "verdict": p["cref"][str(W0)]["verdict"],
                    "confirmed": bool(cf[0]), "cf_star": cf[1:],
                    "n_better": p["n_better"], "n_worse": p["n_worse"], "w_star": p["w_star"],
                    "confirmed_reg_only": bool(hi_a["reg"][0] - lo_b["reg"][0] > 0) if bt else False,
                    "adversarial": bool(hi_a["lo"][0] - lo_b["hi"][0] > 0) if bt else False})
    within = [p for p in prs if p["scope"] != "cross"]
    r2 = h2a_rule(within)
    ce = [p for p in within if p["verdict"] == "CERTIFIED"]
    ot = [p for p in within if p["verdict"] == "NOT CERTIFIED"]
    if ce and ot:
        diff = np.mean([p["cf_star"] for p in ce], 0) - np.mean([p["cf_star"] for p in ot], 0)
        r2["Vc_minus_Vn_ci95"] = np.percentile(diff, [2.5, 97.5]).tolist()
    if ce and r2["n_cert_unconfirmed"] == 0:
        r2["exact_lower_limit"] = 0.05 ** (1 / len(ce))
    conf = {p["idx"]: p["confirmed"] for p in within}
    r2["nulls"] = {k: {"n": len(ix), "errors": sum(not conf[i] for i in ix), "idx": ix} for k, ix in fz["nulls_w0"].items()}
    r2["margin_beats_certificate"] = r2["nulls"]["margin"]["errors"] < r2["n_cert_unconfirmed"]
    r2["n_cert_unconfirmed_only_through_remainder"] = sum(p["confirmed_reg_only"] and not p["confirmed"] for p in ce)
    r2["n_cert_confirmed_adversarial"] = sum(p["adversarial"] for p in ce)
    sec = {}
    for x in [*GRID, fz["w_ev"]]:
        if x == "none":
            continue
        rr = h2a_rule([{**q, "verdict": p["cref"][str(x)]["verdict"]} for p, q in zip(
            [p for p in fz["pairs"] if p["scope"] != "cross"], within)])
        sec[str(x)] = {**{k: rr[k] for k in ("n_cert", "n_other", "n_cert_unconfirmed", "V_c", "V_n")},
                       "label": f"REFUTED AT {x}" if rr["refuted_by_error_rule"] else f"VALID AT {x}"}
    cross = h2a_rule([p for p in prs if p["scope"] == "cross"])
    h2a = {**r2, "secondary_by_w": sec, "cross_family_secondary": cross,
           "pairs": [{**{k: p[k] for k in ("idx", "scope", "verdict", "confirmed", "w_star")},
                      "label": PRINT_LABEL.get(p["verdict"], p["verdict"])} for p in prs]}
    # (4b) H2d (v1.3): scores and exclusions from FREEZE; y per row of its own stream (CC-336 Q3, CC-337 W3)
    Wd = w["boot_weights"](len(w["ids"]), np.random.default_rng(SEED), B_TRUTH)
    dprs, Yd = [], []
    for p in fz["pairs"]:
        if p["scope"] == "cross":
            continue
        idx, c, bd = idx_of(w, p["scope"]), p["cells"], p["cref"][str(W0)]["better"]
        e = {s: pc_ends(cn[p[s]], Wd[:, idx], idx) for s in ("A", "B")}
        Yd.append(confirmed(e[bd], e["B" if bd == "A" else "A"]) if bd else np.zeros(len(Wd), bool))
        dprs.append({"verdict": p["cref"][str(W0)]["verdict"], "scope": p["scope"], "w_star": p["w_star"],
                     "n_better": p["n_better"], "n_worse": p["n_worse"],
                     "dabs": abs(Fr(c["tA"], c["nA"]) - Fr(c["tB"], c["nB"])) if c["nA"] and c["nB"] else None})
    Yd = np.array(Yd).T
    h2d = h2d_rule(dprs, Yd)
    h2d["stream"] = {"call": f"a_m1.boot_weights({len(w['ids'])}, numpy.random.default_rng({SEED}), {B_TRUTH})",
                     "rows": f"1..{len(Wd) - 1}", "sha256_rows": hashlib.sha256(Wd[1:].tobytes()).hexdigest()}
    h2d["per_family_descriptive"] = {}
    for f in ("Q25", "Q3"):
        ix = [k for k, p in enumerate(dprs) if p["scope"] == f]
        h2d["per_family_descriptive"][f] = {k: v for k, v in h2d_rule([dprs[k] for k in ix], Yd[:, ix]).items()
                                            if k not in ("label", "printed_label", "reading", "fail_adds")}
    # (5) H1 with the §5 STOP guard (B4: a fault writes nothing)
    h1 = {}
    for fam in ("Q25", "Q3"):
        add = {m: {s: ((cn[s]["hy"] + (cn[s]["rem"] if m == "hi" else 0)),
                       (cn[s]["hn"] + (cn[s]["rem"] if m == "lo" else 0))) for s in w["fam"][fam]}
               for m in ("reg", "lo", "hi")}
        r = {m: fam_slopes(w, fam, add[m]) for m in add}
        bF = {m: float(r[m]["F"][0]) for m in r}
        bP = {m: float(r[m]["P"][0]) for m in r}
        rngF, rngP = fz["slopes"][fam]["clabel"]["F"]["range"], fz["slopes"][fam]["clabel"]["P"]["range"]
        guards = [rngF] + ([rngP] if fam == "Q3" else [])
        vals = [bF] + ([bP] if fam == "Q3" else [])
        for rg, vv in zip(guards, vals):
            if any(not (rg[0] - 1e-9 <= x <= rg[1] + 1e-9) for x in vv.values()):
                raise Fault("§5 STOP")
        ci = r["reg"]["ci"](r["reg"]["F"][1])
        lo_m, hi_m = fam_slopes(w, fam, unknown_add(w, fam, "lower")), fam_slopes(w, fam, unknown_add(w, fam, "upper"))
        x = r["reg"]["lnM"]
        names = list(r["reg"]["per"])
        adv = corner(x, np.array([r["lo"]["per"][s]["F"][0] for s in names]),
                     np.array([r["hi"]["per"][s]["F"][0] for s in names]), r["reg"]["slope"])
        h1[fam] = {"b_F": bF, "b_P": bP, "b_F_ci95": ci, "b_P_ci95": r["reg"]["ci"](r["reg"]["P"][1]),
                   "b_F_bonf": np.percentile(r["reg"]["F"][1], [BONF, 100 - BONF]).tolist(),
                   "b_F_minus_S72_lower_ci95": r["reg"]["ci"](r["reg"]["F"][1] - lo_m["F"][1]),
                   "b_F_minus_S72_upper_ci95": r["reg"]["ci"](r["reg"]["F"][1] - hi_m["F"][1]),
                   "remainder_corner_F_secondary": [float(adv[0]), float(adv[1])],
                   "label_inside_S72": h1_inside_rule(bF["reg"], bF["lo"], bF["hi"], *S72[fam]),
                   "S72_ends_unrounded_from_FREEZE": fz["slopes"][fam]["clabel"]["s72"],  # CC-343 3(g), no verdict
                   "direction": ["below" if v < S72[fam][0] else "above" if v > S72[fam][1] else "inside"
                                 for v in bF.values()]}
    h1["H1a"] = h1a_rule(h1["Q3"]["b_F"]["reg"], h1["Q3"]["b_F_ci95"], h1["Q3"]["b_F"]["lo"], h1["Q3"]["b_F"]["hi"])
    h1["H1b"], h1["H1c"] = h1["Q25"]["label_inside_S72"], h1["Q3"]["label_inside_S72"]
    labels = {"H1a": h1["H1a"], "H1b": h1["H1b"], "H1c": h1["H1c"], "H2a": h2a["label"], "H2b": h2b["label"],
              "H3": h3["label"], "H2d": h2d["label"]}
    # (6) secondary rows, no verdict: S2 golds (i)/(ii) on I600; S3 H3 on all system-named pairs and A-M1 D_L (CC-343)
    pres2, _ = completed_sets(w, h)
    sec_rows = {"golds_I600": secondary_golds(w, h, cn, i600),
                "H3_all_system_named": {"label_row": "secondary (v1.1 §6): H3 on all system-named pairs of V_m in I600; "
                                                     "no verdict", **h3_row(w, gr, h, named, Wb, i600)},
                "D_L": dl_row(w, gr, pres2, Wb, i600)}
    return {"schema": "vsps.a_cert.result.v1", "label": "single annotator; new labels on previously analysed captions",
            "registered": labels, "quality": quality, "H3": h3, "H2b": h2b, "H2a": h2a, "H2d": h2d, "H1": h1,
            "secondary": sec_rows}


# ------------------------------------------------------------------------------------------------ modes
def pinned_freeze(P: dict) -> tuple[dict, str]:
    fp = ROOT / P["freeze"]
    if not fp.exists():
        raise Fault("no FREEZE.json")
    h = sha(fp)
    log = (ROOT / P["log"]).read_text(encoding="utf-8").splitlines()
    if not any("FREEZE" in ln and h in ln for ln in log):
        raise Fault("no FREEZE pin line in the LOG")
    return json.loads(fp.read_text(encoding="utf-8")), h


def score(labels: str, labels_sha: str, key_path: str, P: dict = P_REAL, world_fn=None) -> int:
    """B4: statistics in memory; one atomic write after every check; on any fault no statistic, exit 2."""
    try:
        res = ROOT / P["result"]
        if res.exists():
            raise Fault("result exists (one pass only)")
        fz, fsha = pinned_freeze(P)
        if P is P_REAL and not (committed(SELF) and committed(REG) and committed(H2D)):
            raise Fault("a_cert.py, v1.1 and H2d v1.3 must equal their HEAD blobs")
        if P is P_REAL and (sha(ROOT / REG), sha(ROOT / H2D)) != (SHA_REG, SHA_H2D):
            raise Fault("v1.1 or H2d v1.3 is not the registered file")
        # CC-343 N12: every label-free check before the first label byte is read
        w = (world_fn or _score_world)()
        if w["pins"] != fz["pins"]:
            raise Fault("inputs differ from FREEZE pins")
        if P is P_REAL and len(w["ids"]) != 600:
            raise Fault("H2d stream needs boot_weights(600, ...)")
        _LABEL_OK.update({os.path.abspath(labels), os.path.abspath(key_path)})
        lab_b, key_b = Path(labels).read_bytes(), Path(key_path).read_bytes()  # N8: hash and parse the same bytes
        if hashlib.sha256(lab_b).hexdigest() != labels_sha:
            raise Fault("label copy sha differs from its argument")
        ksha = hashlib.sha256(key_b).hexdigest()
        if P is P_REAL and ksha != KEY_SHA:
            raise Fault("key.json sha differs from BUILD.json")
        key = json.loads(key_b.decode("utf-8"))
        ans = answers(lab_b.decode("utf-8").splitlines())
        part1 = {q for q, k in key.items() if k["part"] == 1}
        if len(part1) != P["part1_n"] or len(part1 & ans.keys()) != P["part1_n"]:
            raise Fault("part 1 is not complete")
        out = score_core(w, fz, key, ans)
        out["provenance"] = {"freeze_sha256": fsha, "labels_sha256": labels_sha, "key_sha256": ksha,
                             "script_sha256": sha(__file__)}
        json.dumps(out, default=float)
    except BaseException as e:  # noqa: BLE001  (B4: exit status and exception type only)
        print(f"FAULT {type(e).__name__}")
        return 2
    print(json.dumps({"wrote": P["result"], "sha256": write_atomic(res, out)}))
    return 0


def gate(P: dict = P_REAL) -> int:
    w = _load_world()
    cells = gate_core(w, json.loads((ROOT / ASSIGN).read_text(encoding="utf-8")),
                      json.loads((ROOT / BUILD).read_text(encoding="utf-8")),
                      json.loads((ROOT / BRACKET).read_text(encoding="utf-8")))
    ok = all(c["ok"] for c in cells)
    print(json.dumps({"wrote": P["gate"], "sha256": write_atomic(ROOT / P["gate"], {
        "schema": "vsps.a_cert.gate.v1", "status": "development (no labels)", "script_sha256": sha(__file__),
        "pins": w["pins"], "cells": cells, "all_ok": ok}), "all_ok": ok}))
    return 0 if ok else 1


def freeze(P: dict = P_REAL) -> int:
    if not (committed(SELF) and committed(REG)):
        raise Fault("a_cert.py and v1.1 must equal their HEAD blobs")
    gp = ROOT / P["gate"]
    gj = json.loads(gp.read_text(encoding="utf-8")) if gp.exists() else {}
    if not gj.get("all_ok") or gj.get("script_sha256") != sha(__file__):
        raise Fault("gate has not passed with this script")
    if (ROOT / P["freeze"]).exists():
        raise Fault("FREEZE.json exists")
    fz = freeze_core(_load_world())
    fz["provenance"] = {"script_sha256": sha(__file__), "registration_sha256": sha(ROOT / REG), "gate_sha256": sha(gp)}
    print(json.dumps({"wrote": P["freeze"], "sha256": write_atomic(ROOT / P["freeze"], fz)}))
    return 0


# ------------------------------------------------------------------------------------------------ selftest
def test_mods():
    """bracket with score_g2b and v3 loaded as bracket.load_modules does, without the real-data pin check."""
    import importlib.util
    sys.path[:0] = [str(ROOT / "scripts/n_f1"), str(ROOT / "scripts/g2b"), str(ROOT / "scripts"), str(ROOT)]
    import bracket as br
    import score_g2b as g
    spec = importlib.util.spec_from_file_location("evaluate_xm3600_predictions_v3", ROOT / br.V3)
    v = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v)
    br.g, br.v = g, v
    return br


def fixture(br, n: int = 40, seed: int = 7) -> dict:
    """Synthetic world: 12 systems in BUILD names, 8 mapped classes (c0 and c1 share a map) and one unmapped;
    Q3 images = a strict subset; contexts built by the registered row functions."""
    v, g = br.v, br.g
    rng = np.random.default_rng(seed)
    ids = [f"{k:016x}" for k in range(n)]
    vm = {f"c{j}" for j in range(8)}
    cls = sorted(vm) + ["u0"]
    syn = {c: c for c in vm} | {"c1": "c0"}
    q25 = [f"xm3600_{m}-{p}" for m in ("zeroshot", "p1_s43", "fuse2_s42") for p in ("short", "detailed")]
    q3 = [f"g2b_q3_xm600-{p}-T{t}" for p in ("short", "detailed") for t in ("0", "05", "08")]
    names = sorted(q25 + q3)
    oi = [{c: s for c in sorted(vm) if (s := rng.choice(["present", "absent", "u"], p=[.35, .25, .4])) != "u"}
          for _ in ids]
    ms_all = {}
    for j, s in enumerate(names):
        q = 0.25 + 0.06 * (j % 6) + (0.15 if "detailed" in s else 0)
        ms_all[s] = [{c for c in cls if rng.random() < (q + 0.2 if oi[k].get(c) == "present" else q)} for k in range(n)]
    refs_all = [[{c for c in cls if rng.random() < (0.5 if oi[k].get(c) == "present" else 0.15)}
                 for _ in range(3 if k < 6 else 2)] for k in range(n)]
    idx3 = np.array([k for k in range(n) if k % 8 != 0])
    gall = [set().union(*r) for r in refs_all]
    full = np.arange(n)[None]
    s75 = {"name": "s75", "full": full, "idx_boot": np.random.default_rng(0).integers(0, n, (v.B_PAIRED, n)),
           "systems": {}}
    for s in q25:
        a = np.array([v.xo.caption_rows(ms_all[s][k], oi[k], gall[k], vm) for k in range(n)], float)
        pres = [{c for c, x in oi[k].items() if x == "present"} for k in range(n)]
        m = np.array([len(x) for x in ms_all[s]], float)
        s75["systems"][s] = {"a": a, "pr": np.array([len(ms_all[s][k] & pres[k]) / len(pres[k]) if pres[k] else np.nan
                                                     for k in range(n)]),
                             "M_pt": float(m.mean()), "M_dr": m[s75["idx_boot"]].mean(1)}
    lex = {"oiv7": oi, "mapped": vm}
    g2 = {"name": "xm600", "systems": q3, "idx": idx3, "lo_q": 2.5, "hi_q": 97.5, "floor": 1e-9,
          "W": rng.multinomial(len(idx3), np.full(len(idx3), 1 / len(idx3)), size=200).astype(float),
          "rows": {s: g.oiv7_rows(ms_all[s], lex) for s in q3}}
    # S1 hint coverage, deterministic (no draw, so the fixture above is unchanged): two pos MIDs per class; an absent
    # status always verifies "/a", and "/b" only on alternate image-class parities (full vs partial coverage)
    neg = {i: {f"{c}/a" for c, s in oi[k].items() if s == "absent"} |
           {f"{c}/b" for c, s in oi[k].items() if s == "absent" and (k + int(c[1:])) % 2 == 0} for k, i in enumerate(ids)}
    return {"ids": ids, "sys": names, "vm": vm, "syn": syn, "ms_all": ms_all,
            "ms": {s: [m & vm for m in ms_all[s]] for s in names}, "refs_all": refs_all, "oi": oi,
            "fam": {"Q25": q25, "Q3": q3}, "idx": {"Q25": np.arange(n), "Q3": idx3}, "ctx": {"Q25": s75, "Q3": g2},
            "br": br, "pins": {"fixture": "synthetic"}, "f0_hat": _p50x().f0_hat, "boot_weights": _a_m1().boot_weights,
            "pos_mids": {c: {f"{c}/a", f"{c}/b"} for c in vm}, "oi_neg": neg}


def fixture_labels(w: dict, seed: int = 11) -> tuple[dict, list]:
    """key.json in build_assignment's shape (qid rule, parts, roles) and a labels jsonl with re-answers."""
    rng = np.random.default_rng(seed)
    q = lambda part, i, c: hashlib.sha256(f"{SEED}|{part}|{i}|{c}".encode()).hexdigest()[:12]  # noqa: E731
    named = set()
    for k, i in enumerate(w["ids"]):
        for s in w["sys"]:
            named |= {(i, c) for c in w["ms_all"][s][k]}
        for r in w["refs_all"][k]:
            named |= {(i, c) for c in r}
    pos = {i: k for k, i in enumerate(w["ids"])}
    key, lines = {}, []
    for i, c in sorted(named):
        st = w["oi"][pos[i]].get(c)
        if c in w["vm"]:
            role = "target" if st is None else "ctrl_present" if st == "present" else "ctrl_absent"
            key[q(1, i, c)] = {"image": i, "class": c, "part": 1, "role": role}
    for qq, k in list(key.items())[:15]:
        if k["role"] == "target":
            key[q(3, k["image"], k["class"])] = {"image": k["image"], "class": k["class"], "part": 3, "role": "repeat"}
    for qq, k in key.items():
        lab = str(rng.choice(["Y", "N", "U", "A"], p=[.45, .35, .12, .08])) if k["role"] != "ctrl_present" else "N"
        if rng.random() < 0.2:
            lines.append(json.dumps({"qid": qq, "label": "U"}))
        lines.append(json.dumps({"qid": qq, "label": lab}))
    # S1: six foil_absent controls on OI-absent pairs, added after the draws above, answers alternating N and Y.
    # Synthetic: almost every fixture pair is named, so a foil may share its pair with a ctrl_absent; qid part 9 avoids
    # a collision while the record says part 1.
    foils = [(i, c) for k, i in enumerate(w["ids"]) for c in sorted(w["vm"]) if w["oi"][k].get(c) == "absent"][:6]
    for j, (i, c) in enumerate(foils):
        key[q(9, i, c)] = {"image": i, "class": c, "part": 1, "role": "foil_absent"}
        lines.append(json.dumps({"qid": q(9, i, c), "label": "NY"[j % 2]}))
    return key, lines


def selftest(out: Path) -> int:
    ck = {}
    try:
        _selftest_checks(ck)
    except BaseException as e:  # noqa: BLE001  (recorded as a failed check, so a mutant that crashes is still caught)
        ck[f"no_exception ({type(e).__name__}: {str(e)[:80]})"] = False
    ck = {k: bool(x) for k, x in ck.items()}
    rec = {"schema": "vsps.a_cert.selftest.v1", "script_sha256": sha(__file__), "checks": ck, "n": len(ck),
           "pass": all(ck.values())}
    Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print("\n".join(f"{'ok  ' if v else 'FAIL'} {k}" for k, v in ck.items()))
    print("selftest ok" if rec["pass"] else "selftest FAILED")
    return 0 if rec["pass"] else 1


def _selftest_checks(ck: dict) -> None:
    import contextlib
    import io
    import shutil
    br = test_mods()
    E = 2.0  # alpha_S = 2 gives L = 0: the slack-0 budgets of A2 plan §3.10 (beta = c * f1)
    cell = lambda U, f1=0, sz=(): {"U": U, "f1": f1, "sz": list(sz)}  # noqa: E731
    # (i) toys T1 and T2 of A2 plan §3.10, restated for precision, exact
    T1 = {"nA": 4, "tA": 3, "nB": 12, "tB": 5, "A": cell(1), "B": cell(7, 2), "S": cell(0)}
    ck["T1_no_assumption_not_certified"] = certify(T1, 0.0)["verdict"] == "NOT CERTIFIED" and \
        certify(T1, 0.0)["dmin"] == Fr(-1, 4)
    ck["T1_tie_at_xB_4"] = delta_min(3, 4, 5, 12, 4, 0) == 0
    ck["T1_w02_tie_not_certified"] = certify(T1, Fr(1, 5), E, beta_B)["verdict"] == "NOT CERTIFIED"
    ck["T1_w0201_certified"] = certify(T1, 0.201, E)["verdict"] == "CERTIFIED"
    ws = w_star(T1, E)
    ck["T1_w_star_0.2"] = isinstance(ws, float) and 0.2 < ws <= 0.2 + 1e-8
    T2 = {"nA": 10, "tA": 7, "nB": 20, "tB": 13, "A": cell(2), "B": cell(6, 2), "S": cell(1, 3)}
    r = certify(T2, 0.6, E)
    ck["T2_paired_certified_+0.05"] = r["verdict"] == "CERTIFIED" and r["dmin"] == Fr(1, 20)
    ck["T2_separate_not_certified"] = Fr(7, 10) - Fr(13 + cap(T2["B"], .6, E) + cap(T2["S"], .6, E), 20) == 0
    ck["T2_caps_0_1"] = (cap(T2["B"], .6, E), cap(T2["S"], .6, E)) == (0, 1)
    ck["T2_no_assumption_-0.25"] = certify(T2, 0.0)["dmin"] == Fr(-1, 4)
    bf = min(Fr(7 + a + s, 10) - Fr(13 + s, 20) for a in (0, 1, 2) for s in (0, 1))
    ck["T2_brute_force_+0.05"] = bf == Fr(1, 20)
    ws = w_star(T2, E)
    ck["T2_w_star_0.5"] = isinstance(ws, float) and 0.5 < ws <= 0.5 + 1e-8
    nl = null_select([{"verdict": "CERTIFIED", "dabs": abs(Fr(7, 10) - Fr(13, 20)), "idx": 0, "n_better": 10,
                       "n_worse": 20}], 1)
    ck["T2_margin_0.05_length_rule_abstains"] = nl["length"] == [] and nl["margin"] == [0] and \
        abs(Fr(7, 10) - Fr(13, 20)) == Fr(1, 20)
    ck["part1_constant_2233"] = P_REAL["part1_n"] == 2233 == N_TARGETS1 + N_CTRL
    ck["cap_le_U"] = cap(cell(3, 50), 0.05, ALPHA_S) == 3 and cap(cell(3, 50), 0.0, ALPHA_S) == 3
    ck["beta_B_value"] = abs(beta_B(cell(9, 10), 0.2, ALPHA_S) - (
        2 * 10 + 3 * math.log(80) / 3 + math.sqrt(math.log(80) ** 2 + 12 * (10 + math.log(80) + math.sqrt(
            math.log(80) ** 2 + 20 * math.log(80))) * math.log(80)))) < 1e-9
    # (ii) closed form = exhaustive enumeration, (iv) monotone in w
    rng = np.random.default_rng(1)
    ok2 = ok4 = True
    for _ in range(300):
        uA, uB, uS = (int(x) for x in rng.integers(0, 4, 3))
        nA, nB = int(rng.integers(uA + uS + 1, 14)), int(rng.integers(uB + uS + 1, 14))
        tA, tB = int(rng.integers(0, nA - uA - uS + 1)), int(rng.integers(0, nB - uB - uS + 1))
        XA, XB, XS = (int(rng.integers(0, u + 1)) for u in (uA, uB, uS))
        en = min(Fr(tA + a + s, nA) - Fr(tB + b + s, nB) for a in range(XA + 1) for b in range(XB + 1)
                 for s in range(XS + 1))
        ok2 &= en == delta_min(tA, nA, tB, nB, XB, XS)
        pc = {"nA": nA, "tA": tA, "nB": nB, "tB": tB, "A": cell(uA, 2), "B": cell(uB, int(rng.integers(0, 6))),
              "S": cell(uS, int(rng.integers(0, 6)))}
        if Fr(tA, nA) > Fr(tB, nB):
            d = [certify(pc, x)["dmin"] for x in (*GRID, 0.7, 1.0)]
            ok4 &= all(a <= b for a, b in zip(d, d[1:]))
    ck["closed_form_equals_enumeration_300"], ck["dmin_monotone_in_w"] = ok2, ok4
    # (iii) corner range = enumeration over all corners
    ok3 = True
    for _ in range(50):
        x, lo = rng.normal(size=6), rng.normal(size=6)
        hi = lo + rng.random(6)
        en = [ols(x, np.where(np.array(b, bool), hi, lo)) for b in itertools.product((0, 1), repeat=6)]
        cmin, cmax = corner(x, lo, hi, ols)
        ok3 &= abs(cmin - min(en)) < 1e-12 and abs(cmax - max(en)) < 1e-12
    ck["corner_range_equals_enumeration"] = ok3
    # (v) size simulation of beta (code check, not evidence)
    se, ok5 = 2 * math.sqrt(ALPHA_S * (1 - ALPHA_S) / 2000), True
    for wv in (0.1, 0.2, 0.3):
        for law in ("point", "beta22", "beta05_3"):
            p = np.full((2000, 300), wv) if law == "point" else wv + (1 - wv) * (
                rng.beta(2, 2, (2000, 300)) if law == "beta22" else rng.beta(0.5, 3, (2000, 300)))
            N = rng.binomial(2, p)
            x, f1 = (N == 0).sum(1), (N == 1).sum(1)
            ok5 &= np.mean([xx > beta_B({"f1": int(ff)}, wv, ALPHA_S) for xx, ff in zip(x, f1)]) <= ALPHA_S + se
    ck["size_simulation_beta_B"] = ok5
    # (vi) status logic
    syn = {"c0": "c0", "c1": "c0", "c2": "c2"}
    key = {"q1": {"image": "i", "class": "c0", "part": 1, "role": "target"},
           "q2": {"image": "i", "class": "c1", "part": 1, "role": "target"},
           "q3": {"image": "i", "class": "c2", "part": 1, "role": "ctrl_present"},
           "q4": {"image": "i", "class": "c0", "part": 3, "role": "repeat"},
           "q5": {"image": "j", "class": "c0", "part": 1, "role": "target"},
           "q6": {"image": "j", "class": "c1", "part": 1, "role": "target"},
           "q7": {"image": "k", "class": "c0", "part": 1, "role": "target"}}
    lines = [json.dumps({"qid": a, "label": b}) for a, b in (("q1", "N"), ("q1", "Y"), ("q2", "U"), ("q3", "N"),
                                                             ("q4", "N"), ("q5", "Y"), ("q6", "N"), ("q7", "A"))]
    ans = answers(lines)
    h, dis = human(key, ans, syn)
    ck["last_line_wins_and_part3_ignored"] = h[("i", "c0")] == "Y"
    ck["U_A_to_remainder_no_propagation"] = h[("i", "c1")] is None and h[("k", "c0")] is None
    ck["controls_never_enter_status"] = ("i", "c2") not in h
    ck["synonym_disagreement_counted"] = dis == 1 and h[("j", "c1")] == "N"
    wmini = {"ids": ["i"], "ms": {"s": [{"c0", "c1", "c2", "c3"}]}, "oi": [{"c2": "present", "c3": "absent"}]}
    ck["oi_never_overridden"] = {k: int(v[0]) for k, v in counts(wmini, "s", {**h, ("i", "c2"): "N"}).items()} == \
        {"pm": 1, "am": 1, "hy": 1, "hn": 0, "rem": 1}
    cn = {"pm": np.array([2.0]), "am": np.array([1.0]), "hy": np.array([1.0]), "hn": np.array([0.0]),
          "rem": np.array([2.0])}
    e = pc_ends(cn, np.ones((1, 1)), np.array([0]))
    ck["P_c_and_ends_by_hand"] = [float(e[k][0]) for k in ("reg", "lo", "hi")] == [3 / 4, 3 / 6, 5 / 6]
    ck["tie_not_confirmed"] = not confirmed({"reg": np.array([.5]), "lo": np.array([.6]), "hi": np.array([.7])},
                                            {"reg": np.array([.5]), "lo": np.array([.5]), "hi": np.array([.6])})[0]
    # (vii) verdict labels at their boundaries
    mk = lambda v_, c_, n: [{"verdict": v_, "confirmed": c_}] * n  # noqa: E731
    ck["h2a_not_evaluable_9"] = h2a_rule(mk("CERTIFIED", True, 9) + mk("NOT CERTIFIED", False, 20))["label"] == \
        "NOT EVALUABLE"
    ck["h2a_pass_10_10"] = h2a_rule(mk("CERTIFIED", True, 10) + mk("NOT CERTIFIED", False, 10))["label"] == "PASS"
    ck["h2a_fail_1_of_19"] = h2a_rule(mk("CERTIFIED", True, 18) + mk("CERTIFIED", False, 1) +
                                      mk("NOT CERTIFIED", False, 10))["label"] == "FAIL"
    ck["h2a_1_of_20_allowed"] = h2a_rule(mk("CERTIFIED", True, 19) + mk("CERTIFIED", False, 1) +
                                         mk("NOT CERTIFIED", False, 10))["label"] == "PASS"
    ck["h2a_valid_not_discriminating"] = h2a_rule(mk("CERTIFIED", True, 10) + mk("NOT CERTIFIED", True, 10))[
        "label"] == "VALID, NOT DISCRIMINATING"
    r = h2a_rule(mk("CERTIFIED", True, 10) + mk("ABSTAIN", True, 5) + mk("NOT DEFINED", True, 2) +
                 mk("NOT CERTIFIED", False, 9))
    ck["B2_ties_and_undefined_excluded"] = r["label"] == "NOT EVALUABLE" and r["n_cert"] == 10 and r["n_excluded"] == 7
    tie = certify({"nA": 4, "tA": 2, "nB": 6, "tB": 3, "A": cell(1), "B": cell(1), "S": cell(0)}, 0.0)
    ck["abstain_printed_not_certified"] = tie["verdict"] == "ABSTAIN" and \
        PRINT_LABEL[tie["verdict"]].startswith("NOT CERTIFIED") and certify(
            {"nA": 0, "tA": 0, "nB": 6, "tB": 3, "A": cell(0), "B": cell(1), "S": cell(0)}, 0.0)["verdict"] == "NOT DEFINED"
    nl = null_select([{"verdict": "CERTIFIED", "dabs": Fr(1, 2) - Fr(1, 6), "idx": 3, "n_better": 5, "n_worse": 5},
                      {"verdict": "NOT CERTIFIED", "dabs": Fr(2, 3) - Fr(1, 3), "idx": 1, "n_better": 6, "n_worse": 5},
                      {"verdict": "ABSTAIN", "dabs": Fr(9, 10), "idx": 0, "n_better": 9, "n_worse": 1}], 1)
    ck["B2_nulls_exact_tie_by_index_length_strict"] = nl["margin"] == [1] and nl["length"] == [1] and \
        nl["constant"] == [3, 1] and (1 / 2 - 1 / 6) != (2 / 3 - 1 / 3)
    ck["h2b_rules"] = [h2b_rule([True] * 11 + [False], 1), h2b_rule([True] * 10 + [False] * 2, 1),
                       h2b_rule([False] * 12, 0)] == ["PASS", "FAIL", "PASS (vacuous)"]
    ck["h3_rules"] = [h3_rule(40, 9, [1, 2], [1, 2]), h3_rule(60, 0, [1], [1]),
                      h3_rule(40, 10, np.linspace(0.1, 5, 101), np.linspace(-1, 5, 101)),
                      h3_rule(40, 10, np.linspace(-5, 1, 101), np.linspace(-5, -0.1, 101)),
                      h3_rule(40, 10, np.linspace(-1, 1, 101), np.linspace(-1, 1, 101)),
                      h3_rule(40, 10, np.linspace(-5, 0.5, 101), np.linspace(-5, 0.5, 101))] == \
        ["NOT EVALUABLE", "NOT EVALUABLE", "RESPECTED", "VIOLATED", "INCONCLUSIVE", "INCONCLUSIVE"]
    ck["B1_h1a"] = [h1a_rule(1, [0.1, 2], 1, 1), h1a_rule(1, [0.1, 2], 1, -1), h1a_rule(1, [-0.1, 2], 1, 1),
                    h1a_rule(-1, [-2, 0], -1, -1), h1a_rule(0, [-2, 1], 1, 0), h1a_rule(1, None, 1, 1)] == \
        ["PASS", "INCONCLUSIVE (remainder)", "INCONCLUSIVE", "FAIL", "INCONCLUSIVE (remainder)", "INCONCLUSIVE"]
    ck["B1_h1_inside"] = [h1_inside_rule(6, 5.83, 20.13, 5.83, 20.13), h1_inside_rule(6, 6, 21, 5.83, 20.13),
                          h1_inside_rule(6, 5, 6, 5.83, 20.13), h1_inside_rule(4, 3, 21, 5.83, 20.13)] == \
        ["PASS", "INCONCLUSIVE (remainder)", "INCONCLUSIVE (remainder)", "FAIL"]
    # (ix) seeded 2-of-3 draw
    w = fixture(br)
    two, picks = draw_two(w["refs_all"], w["ids"])
    ck["draw_reproduces"] = (two, picks) == draw_two(w["refs_all"], w["ids"]) and \
        picks == {w["ids"][k]: j for k, j in enumerate(DRAW_EXPECTED)}
    ck["draw_uses_exactly_two"] = all(two[k] == [w["refs_all"][k][a] for a in picks[i]] for k, i in enumerate(w["ids"])
                                      if i in picks) and draw_two(w["refs_all"], w["ids"], True)[1] == \
        {i: [0, 1] for i in picks}
    # freeze on the fixture: image sets, slope alpha/m, N10 import, H2a declaration
    fz = freeze_core(w)
    ck["Q3_pairs_on_I537_Q25_on_I600"] = all(p["n_images"] == (40 if p["scope"] == "Q25" else 35) for p in fz["pairs"])
    gr = gold_ref(two, w["vm"])
    reg = fam_slopes(w, "Q3")
    ok_a = diff = True
    for wv in GRID[1:]:
        lo_, hi_, hi25 = [], [], []
        for s in reg["per"]:
            c = sys_cell(w["ms"], s, gr, w["idx"]["Q3"])
            lo_.append(100 * c["t"] / c["n"])
            hi_.append(100 * (c["t"] + cap(c, wv, 0.05 / 6)) / c["n"])
            hi25.append(100 * (c["t"] + cap(c, wv, 0.025)) / c["n"])
        ok_a &= fz["slopes"]["Q3"]["cref_P"][str(wv)]["range"] == list(corner(reg["lnM"], lo_, hi_, reg["slope"]))
        diff &= hi_ == hi25
    ck["slope_corners_alpha_over_m"] = ok_a and not diff
    ck["N10_a_m1_import_leaves_guard_off"] = _a_m1()._HOOK["on"] is False
    # (viii) §5 ranges and STOP guards for both families; completed columns; recall fixed
    key, lab = fixture_labels(w)
    ans = answers(lab)
    h, _ = human(key, ans, w["syn"])
    cn = {s: counts(w, s, h) for s in w["sys"]}
    ok8 = okr = okp = True
    exp_bF = {}
    for fam in ("Q25", "Q3"):
        rg = fz["slopes"][fam]["clabel"]
        base = fam_slopes(w, fam)
        for m in ("reg", "lo", "hi"):
            add = {s: (cn[s]["hy"] + (cn[s]["rem"] if m == "hi" else 0), cn[s]["hn"] + (cn[s]["rem"] if m == "lo" else 0))
                   for s in w["fam"][fam]}
            r = fam_slopes(w, fam, add)
            exp_bF[(fam, m)] = float(r["F"][0])
            ok8 &= all(rg[k]["range"][0] - 1e-9 <= r[k][0] <= rg[k]["range"][1] + 1e-9 for k in ("F", "P"))
            okr &= all(np.array_equal(r["per"][s]["R"][1], base["per"][s]["R"][1]) and
                       r["per"][s]["R"][0] == base["per"][s]["R"][0] for s in r["per"])
            if fam == "Q25":
                okp &= all(abs(r["per"][s]["P"][0] - 100 * pc_ends(cn[s], np.ones((1, 40)), np.arange(40))[m][0]) < 1e-9
                           for s in r["per"])
    ck["completed_slopes_inside_s5_range_both_families"] = ok8
    ck["recall_never_from_completed_gold"] = okr
    ck["P_c_columns_and_remainder_ends_in_slopes"] = okp
    ck["s72_ends_inside_clabel_range"] = all(fz["slopes"][f]["clabel"]["F"]["range"][0] - 1e-9 <=
                                             fz["slopes"][f]["clabel"]["s72"][m] <=
                                             fz["slopes"][f]["clabel"]["F"]["range"][1] + 1e-9
                                             for f in ("Q25", "Q3") for m in ("lower", "upper"))
    res = score_core(w, fz, key, ans)
    ck["H1_slopes_at_registered_and_both_remainder_ends"] = all(
        abs(res["H1"][f]["b_F"][m] - x) < 1e-12 for (f, m), x in exp_bF.items()) and \
        len({round(x, 9) for (f, m), x in exp_bF.items() if f == "Q25"}) == 3
    for fam, k in (("Q25", "F"), ("Q3", "F"), ("Q3", "P")):
        bad = json.loads(json.dumps(fz, default=float))
        bad["slopes"][fam]["clabel"][k]["range"] = [1e6, 1e6 + 1]
        try:
            score_core(w, bad, key, ans)
            ck[f"STOP_guard_{fam}_{k}"] = False
        except Fault as ex:
            ck[f"STOP_guard_{fam}_{k}"] = str(ex) == "§5 STOP"
    # certified set and orientation come from FREEZE; ABSTAIN never confirmed
    t = json.loads(json.dumps(fz, default=float))
    j = next(k for k in range(1, 65) if res["H2a"]["pairs"][k]["confirmed"])
    p0 = t["pairs"][0]["cref"][str(W0)]
    p0["verdict"] = "CERTIFIED" if p0["verdict"] != "CERTIFIED" else "NOT CERTIFIED"
    t["pairs"][j]["cref"][str(W0)]["better"] = "B" if t["pairs"][j]["cref"][str(W0)]["better"] == "A" else "A"
    t["pairs"][65]["cref"][str(W0)].update(verdict="ABSTAIN", better=None)
    r2 = score_core(w, t, key, ans)["H2a"]["pairs"]
    ck["certified_set_from_freeze"] = r2[0]["verdict"] == p0["verdict"]
    ck["orientation_from_freeze"] = r2[j]["confirmed"] is False
    ck["abstain_never_confirmed"] = r2[65]["confirmed"] is False and r2[65]["label"].startswith("NOT CERTIFIED")
    ck["nulls_fixed_at_freeze"] = set(fz["nulls_w0"]) == {"constant", "margin", "length"} and \
        res["H2a"]["nulls"]["margin"]["idx"] == fz["nulls_w0"]["margin"]
    nctl = sum(k["role"] in ("ctrl_present", "ctrl_absent", "foil_absent") for k in key.values())
    ck["control_agreement_over_all_controls"] = res["quality"]["n_control"] == nctl > 0 and \
        res["quality"]["control_agreement_of_all"] <= res["quality"]["control_agreement_among_YN"]
    ck["result_labels_present"] = set(res["registered"]) == {"H1a", "H1b", "H1c", "H2a", "H2b", "H3", "H2d"} and \
        bool(json.dumps(res, default=float))
    # H2d (v1.3): the stream on the fixture, then synthetic rankings checked in exact Fractions
    hd = res["H2d"]
    ro = np.random.default_rng(20261111)
    orc = np.array([np.bincount(ro.integers(0, 40, 40), minlength=40) for _ in range(2000)], float)
    ck["H2d_stream_rows_1_2000_of_boot_weights_rng_20261111"] = hd["n_replicates"] == 2000 and \
        hd["stream"]["sha256_rows"] == hashlib.sha256(orc.tobytes()).hexdigest()
    evp = [p for p in res["H2a"]["pairs"] if p["scope"] != "cross" and p["verdict"] in ("CERTIFIED", "NOT CERTIFIED")]
    ck["H2d_point_y_is_H2a_truth_on_30_pairs"] = hd["n1"] == sum(p["confirmed"] for p in evp) and \
        hd["n1"] + hd["n0"] == len(evp) and len(evp) + hd["n_excluded"] == 30
    ck["H2d_label_verbatim_v1_3"] = hd["printed_label"] == H2D_LABEL and \
        f'"{H2D_LABEL}"' in (ROOT / H2D).read_text(encoding="utf-8")

    def h2d_case(rows, reps=None):
        """rows: (verdict, w*, |dt/n|, n_better (n_worse = 1), y); Y = the point, then 20 copies unless reps."""
        prs = [{"verdict": v, "scope": "Q25", "w_star": x, "dabs": d, "n_better": nb, "n_worse": 1}
               for v, x, d, nb, _ in rows]
        y = [r[4] for r in rows]
        return h2d_rule(prs, np.array([y] + (reps if reps is not None else [y] * 20), bool))

    C, NC = "CERTIFIED", "NOT CERTIFIED"
    grid = lambda pos, neg: [(C, x, Fr(1, 3), 2, 1) for x in pos] + [(NC, x, Fr(1, 3), 2, 0) for x in neg]  # noqa: E731
    neg5 = [.15, .25, .35, .45, .55]
    r = h2d_case(grid([.1, .2, .3, .4, .5], neg5))
    ck["H2d_PASS_at_D_0.10"] = r["label"] == "PASS" and r["D"] == Fr(1, 10) and \
        r["AUC_w_star_margin_length"] == [Fr(3, 5), Fr(1, 2), Fr(1, 2)] and \
        r["reading"].endswith("(single annotator, 10 dependent pairs)")
    r = h2d_case(grid([.1, .2, .3, .4, .55], neg5))
    ck["H2d_FAIL_at_D_0.08_below_SESOI"] = r["label"] == "FAIL" and r["D"] == Fr(2, 25) and "D = 0.080" in r["reading"]
    y10 = [1] * 5 + [0] * 5
    r = h2d_case(grid([.1, .2, .3, .4, .5], neg5), [[1] * 10] * 2 + [y10] * 18)
    ck["H2d_FAIL_when_2.5th_percentile_not_above_0"] = r["label"] == "FAIL" and r["D"] == Fr(1, 10) and \
        r["n_replicates_empty_class"] == 2 and r["D_ci95"][0] == -1.0 and r["fail_adds"] is None
    r = h2d_case(grid([.1, .2, .3, .4], neg5))
    ck["H2d_NOT_EVALUABLE_n1_4"] = r["label"] == "NOT EVALUABLE" and r["reading"] == \
        "H2d could not be evaluated: 4 confirmed and 5 unconfirmed pairs, at least 5 of each needed."
    r = h2d_case([(C, .2, Fr(1, 3), 2, 1), (C, "NI", Fr(1, 6), 2, 1), (NC, "NI", Fr(1, 6), 1, 0),
                  (NC, .2, Fr(2, 6), 1, 0), (NC, .5, Fr(1, 12), 1, 0), ("ABSTAIN", None, Fr(0), 1, 1),
                  ("NOT DEFINED", None, None, 1, 0)])
    ck["H2d_ties_half_NI_last_and_tied_exclusions"] = r["AUC_w_star_margin_length"] == [Fr(1, 2), Fr(2, 3), Fr(1)] \
        and r["D"] == Fr(-1, 2) and (r["n1"], r["n0"], r["n_excluded"], r["n_NI"]) == (2, 3, 2, 2)
    try:
        h2d_case(grid([.1, 0.0], [.2]))
        ck["H2d_w_star_0_is_a_fault"] = False
    except Fault:
        ck["H2d_w_star_0_is_a_fault"] = True
    rb, okb = np.random.default_rng(5), True
    for _ in range(40):
        k = int(rb.integers(4, 10))
        rows = [(C, "NI" if u < .25 else 0.1 + round(float(u), 1), Fr(int(rb.integers(0, 4)), 4), int(rb.integers(1, 3)),
                 int(rb.random() < .5)) for u in rb.random(k)]
        y = [x[4] for x in rows]
        if 0 < sum(y) < k:
            sc = [[-math.inf if x[1] == "NI" else -x[1] for x in rows], [x[2] for x in rows], [x[3] > 1 for x in rows]]
            bf = [sum(Fr(1) if s[i] > s[j] else Fr(1, 2) if s[i] == s[j] else Fr(0) for i in range(k) for j in range(k)
                      if y[i] and not y[j]) / (sum(y) * (k - sum(y))) for s in sc]
            okb &= h2d_case(rows)["AUC_w_star_margin_length"] == bf
    ck["H2d_AUC_equals_brute_force_40"] = okb
    # CC-343 S4 (v1.3 §5): scores only from FREEZE (two tampered copies; a recomputed score would not follow both) and
    # no |Delta| tie-break for w*
    conf = {p["idx"]: p["confirmed"] for p in res["H2a"]["pairs"]}
    evi = {p["idx"] for p in fz["pairs"] if p["scope"] != "cross" and p["cref"][str(W0)]["verdict"] in (C, NC)}
    sent = []
    for ws_, sep in (("NI", False), (0.5, True)):
        t = json.loads(json.dumps(fz, default=float))
        for p in t["pairs"]:
            if p["idx"] in evi:
                p["w_star"] = ws_
                p["cells"].update(tA=2 if sep and conf[p["idx"]] else 1, nA=2, tB=0, nB=2)
        sent.append(score_core(w, t, key, ans)["H2d"])
    ck["S4_H2d_w_star_from_freeze"] = len(evi) > 0 and [d["n_NI"] for d in sent] == [len(evi), 0]
    ck["S4_H2d_margin_from_freeze"] = [d["AUC_w_star_margin_length"][1] for d in sent] == [Fr(1, 2), Fr(1)]
    r = h2d_case([(C, .3, Fr(1, 2), 2, 1), (NC, .3, Fr(1, 4), 2, 0), (C, "NI", Fr(1, 2), 2, 1), (NC, "NI", Fr(1, 4), 2, 0)])
    ck["S4_H2d_no_abs_delta_tiebreak_for_w_star"] = r["AUC_w_star_margin_length"][:2] == [Fr(1, 2), Fr(1)]
    ck["N5_label_and_S72_ends"] = res["H2d"]["D_star_p036_label"] == "0.36th percentile (100 alpha/14 = 0.357)" and \
        round(BONF7, 3) == 0.357 and all(res["H1"][f]["S72_ends_unrounded_from_FREEZE"] == fz["slopes"][f]["clabel"]["s72"]
                                         for f in ("Q25", "Q3"))
    # CC-343 S1: control rows per role and by hint coverage
    ck["S1_ctl_row_by_hand"] = ctl_row(["N", "N", "Y", "U", "A", None], "N") == {
        "n": 6, "agree": 2, "agreement_of_all": 1 / 3, "agreement_among_YN": 2 / 3, "Y": 1, "N": 2, "U": 1, "A": 1,
        "unanswered": 1} and ctl_row([], "Y")["agreement_of_all"] is None
    wh = {"pos_mids": {"c0": {"a", "b"}}, "oi_neg": {"i": {"a", "b", "x"}, "j": {"a"}}}
    ck["S1_hint_full_by_hand"] = [hint_full(wh, i, "c0") for i in "ijk"] == [True, False, False]
    qa = res["quality"]
    got = {r_: [ans.get(q) for q, k in key.items() if k["part"] == 1 and k["role"] == r_]
           for r_ in ("ctrl_present", "ctrl_absent", "foil_absent")}
    absk = [k for k in key.values() if k["part"] == 1 and k["role"] in ("ctrl_absent", "foil_absent")]
    nfull = sum(all(m in w["oi_neg"][k["image"]] for m in w["pos_mids"][k["class"]]) for k in absk)
    hc = qa["control_absent_by_hint_coverage"]
    ck["S1_rows_in_result"] = all(qa["control_by_role"][r_]["n"] == len(a) and qa["control_by_role"][r_]["agree"] ==
                                  a.count(e) for (r_, a), e in zip(got.items(), "YNN")) and \
        len(got["foil_absent"]) == 6 and 0 < nfull < len(absk) and (hc["full"]["n"], hc["partial"]["n"]) == \
        (nfull, len(absk) - nfull)
    ck["repeat_label_partial_k_of_150"] = [repeat_label(149, 150), repeat_label(150, 150)] == [
        "partial (149 of 150 answered at the part-1 unsealing)", "150 of 150"]
    # CC-343 S2 and S3 by hand: two images, one system; i: c0 OI present, c1 and c9 OI absent, c8 OI present (named by
    # no reference), c2/c4 human Y, c7 remainder; j: c3 OI present, c5 human N, c6 remainder
    wm = {"ids": ["i", "j"], "sys": ["s"], "f0_hat": _p50x().f0_hat, "ms": {"s": [{"c0", "c1", "c4", "c7"}, {"c5"}]},
          "oi": [{"c0": "present", "c1": "absent", "c8": "present", "c9": "absent"}, {"c3": "present"}]}
    hm = {("i", "c2"): "Y", ("i", "c4"): "Y", ("j", "c5"): "N", ("j", "c6"): None}
    grm = [{"kp": {"c0", "c2"}, "once": {"c2"}, "twice": {"c0"}}, {"kp": {"c3"}, "once": {"c3"}, "twice": set()}]
    ix2, Wm = np.arange(2), np.ones((3, 2))
    sg = secondary_golds(wm, hm, {"s": counts(wm, "s", hm)}, ix2)
    s1, s2 = sg["gold_i"]["systems"]["s"], sg["gold_ii"]["systems"]["s"]
    near = lambda a, b: a is not None and abs(a - b) < 1e-12  # noqa: E731
    ck["S2_gold_i_by_hand"] = near(s1["recall"], 1 / 3) and near(s1["hallucination"], 1 / 2) and \
        near(s1["share_naming_absent"], 1 / 2) and [s1["P_c"][m] for m in ("reg", "lo", "hi")] == [.5, .4, .6] and \
        all(near(s1["F1"][m], x) for m, x in (("reg", .4), ("lo", 4 / 11), ("hi", 3 / 7)))
    ck["S2_gold_ii_by_hand"] = near(s2["recall"], 2 / 5) and near(s2["hallucination"], 2 / 3) and \
        near(s2["share_naming_absent"], 1.0) and near(s2["F1"], 4 / 9) and s2["P_c"] == .5
    sr = res["secondary"]["golds_I600"]
    ck["S2_rows_in_result"] = set(sr["gold_i"]["systems"]) == set(sr["gold_ii"]["systems"]) == set(w["sys"]) and \
        sr["gold_ii"]["label"] == "pooled gold; favours systems that name more" and sr["gold_ii"]["verdict"] is None
    r = h3_row(wm, grm, hm, [{"c0", "c1", "c2", "c4", "c7", "c8"}, {"c3", "c5", "c6"}], Wm, ix2)
    ck["S3_h3_all_named_by_hand"] = (r["phi1"], r["phi2"], r["f0_hat"], r["X"], r["X_hi"], r["D"], r["D_hi"]) == \
        (2.0, 1.0, 1.0, 2.0, 4.0, 1.0, 3.0) and r["reading_no_verdict"] == "NOT EVALUABLE"
    r = dl_row(wm, grm, completed_sets(wm, hm)[0], Wm, ix2)
    ck["S3_D_L_by_hand"] = (r["L"], r["U_L"], r["phi1"], r["phi2"], r["S_hat"]) == (5.0, 3.0, 2.0, 1.0, 4.0) and \
        near(r["D_L"], 0.2) and r["label"] == "consistent"
    ck["S3_D_L_rule_boundary"] = [dl_rule(np.linspace(-0.2, -0.01, 401)), dl_rule(np.linspace(-0.2, 0.01, 401))] == \
        ["no reading (A-M1 VIOLATED rule met; v1.1 §6: only consistent can be read, the labels are not a complete "
         "inventory)", "consistent"]
    nmd = [set().union(*(w["ms"][s][k] for s in w["sys"])) for k in range(40)]
    sa = res["secondary"]["H3_all_system_named"]
    ck["S3_row1_universe_all_system_named"] = (sa["phi1"], sa["phi2"]) == (
        float(sum(len(nmd[k] & gr[k]["once"]) for k in range(40))), float(sum(len(nmd[k] & gr[k]["twice"]) for k in range(40))))
    ck["S3_D_L_over_completed_present"] = res["secondary"]["D_L"]["L"] == float(
        sum(x == "present" for o in w["oi"] for x in o.values()) + sum(a == "Y" for a in h.values()))
    # custody: a label path is refused before any allowance
    tmp = Path(tempfile.mkdtemp(prefix="a_cert_selftest_"))
    ldir = tmp / "vsps_labels"
    ldir.mkdir()
    lf, kf = ldir / "labels_PI.copy.jsonl", ldir / "key.json"
    try:
        open(lf, "w")
        ck["guard_refuses_label_path"] = False
    except Fault:
        ck["guard_refuses_label_path"] = True
    ck["guard_deny_list"] = refused("/home/x/.vsps_sealed/a") and refused("/r/.session_backup/machines/HBT1/x") and \
        not refused(str(tmp / "other.json"))
    # (x) score refusals and the B4 fault rule, end to end on the fixture
    _LABEL_OK.update({str(lf), str(kf)})
    lf.write_text("\n".join(lab) + "\n", encoding="utf-8")
    kf.write_text(json.dumps(key), encoding="utf-8")
    _LABEL_OK.clear()
    fzp, logp = tmp / "FREEZE.json", tmp / "LOG.md"
    fzh = write_atomic(fzp, fz)
    n1 = sum(k["part"] == 1 for k in key.values())
    P = {"freeze": str(fzp), "result": str(tmp / "out" / "RESULT.json"), "log": str(logp), "part1_n": n1}
    _LABEL_OK.add(str(lf))
    lsha = sha(lf)
    _LABEL_OK.clear()

    def run(**kw):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = score(str(lf), kw.get("lsha", lsha), str(kf), kw.get("P", P), kw.get("wf", lambda: w))
        _LABEL_OK.clear()
        return rc, buf.getvalue(), Path(P["result"]).exists()

    logp.write_text("2026-11-11T00:00:00Z OPS-x: no pin here\n", encoding="utf-8")
    ck["x_refuses_without_freeze_pin"] = run() == (2, "FAULT Fault\n", False)
    logp.write_text(f"2026-11-11T00:00:00Z OPS-x-a-cert-freeze: FREEZE.json sha256 {fzh}\n", encoding="utf-8")
    ck["x_refuses_label_sha_mismatch"] = run(lsha="0" * 64) == (2, "FAULT Fault\n", False)
    ck["x_refuses_part1_count"] = run(P={**P, "part1_n": n1 + 1}) == (2, "FAULT Fault\n", False)

    bad = json.loads(json.dumps(fz, default=float))
    bad["slopes"]["Q3"]["clabel"]["F"]["range"] = [1e6, 1e6 + 1]
    bp = tmp / "FREEZE_bad.json"
    logp.write_text(f"2026-11-11T00:00:00Z OPS-x-a-cert-freeze: FREEZE.json sha256 {write_atomic(bp, bad)}\n",
                    encoding="utf-8")
    ck["B4_STOP_writes_and_prints_no_statistic"] = run(P={**P, "freeze": str(bp)}) == (2, "FAULT Fault\n", False)
    logp.write_text(f"2026-11-11T00:00:00Z OPS-x-a-cert-freeze: FREEZE.json sha256 {fzh}\n", encoding="utf-8")
    ck["B4_exception_writes_nothing"] = run(wf=lambda: 1 / 0) == (2, "FAULT ZeroDivisionError\n", False)
    rc, so, ex = run()
    ck["x_valid_run_writes_once"] = rc == 0 and ex and json.loads(so)["wrote"] == P["result"]
    ck["x_refuses_if_result_exists"] = run() == (2, "FAULT Fault\n", True)
    os.rename(ldir, tmp / "labels_done")  # leaves the label-dir name so the custody hook lets rmtree walk it
    shutil.rmtree(tmp)


DRAW_EXPECTED = [[1, 2], [1, 2], [0, 2], [0, 2], [1, 2], [0, 2]]  # default_rng(20261111), six choice(3, 2) draws


def main(argv: list) -> int:
    sys.addaudithook(_audit)
    for a in argv:
        if refused(a) and (not argv or argv[0] != "score"):
            raise Fault("custody: label path given to a label-free mode")
    if argv[:1] == ["selftest"] and len(argv) == 3 and argv[1] == "--out":
        return selftest(Path(argv[2]))
    if argv == ["gate"]:
        return gate()
    if argv == ["freeze"]:
        return freeze()
    if len(argv) == 7 and argv[0] == "score" and argv[1::2] == ["--labels", "--labels-sha", "--key"]:
        return score(argv[2], argv[4], argv[6])
    raise SystemExit("usage: a_cert.py selftest --out F | gate | freeze | score --labels L --labels-sha H --key K")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
