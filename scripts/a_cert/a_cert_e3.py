#!/usr/bin/env python3
"""A-CERT addendum E3 (Paper A): the E rows (E1-E6) of the other-family arm on the top-up labels.
Spec: manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_E3_v1.md (c0eee4fb), rulings CC-355 (W1-W5, O1-O12) and
CC-359 (ruling 6: S_E = the 7a and 7c passing models). Registered functions are imported from a_cert.py (2e872588),
which is not changed; this file holds the S_E world, the FREEZE_E3 loop and the E rows only.

  selftest --out F       synthetic fixtures in a temp dir only
  e3-freeze --extra F..  label-free: FREEZE_E3.json (addendum §3) from the references, the Open Images statuses and the
                         12 + S_E caption sets; refuses any label path; writes once; prints its sha256
  e3-score --labels L --labels-sha H --key K --topup-labels T --topup-labels-sha H2 --topup-key K2
                         once, after the FREEZE_E3 pin line, the part-1 result pin line and the top-up session-end line;
                         fault rule of A-CERT §12 step 5 (statistics in memory, one atomic write; FAULT <type> only)

One audit hook guards every mode: label directories, sealed paths, any labels_*.jsonl / practice_*.jsonl / key.json and
any assignment.json but the base public copy are refused, except e3-score's four named inputs. Outputs hold counts,
labels and sha256 only. Run (laptop, named exception, see E3_READ_PACKAGE.md):
  OMP_NUM_THREADS=2 nice -n 15 ~/.venvs/c_stage1_lists/bin/python -I -B scripts/a_cert/a_cert_e3.py <mode> ...
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import re
import sys
import tempfile
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a_cert as A  # noqa: E402
from a_cert import Fault  # noqa: E402

ROOT = A.ROOT
SELF = "scripts/a_cert/a_cert_e3.py"
ADD = "manuscript/prereg/2026-11-11_a_cert/A_CERT_ADDENDUM_E3_v1.md"
CC359 = ".session_backup/2026-10-13/decisions/CC-359.txt"
SHA_ADD = "c0eee4fbf66dc928202053bc14f1942ea26424b6aa50a0a5ac282c425b650075"
SHA_ACERT = "2e872588baf6109fad20111aecd25e2504fd0096f9033a95649027a2eed46cf4"
FREEZE12, FREEZE12_SHA = A.P_REAL["freeze"], "c51ea7dc"
OUT = "data/results/a_cert_e3"
P_REAL = {"freeze": f"{OUT}/freeze/FREEZE_E3.json", "result": f"{OUT}/score/A_CERT_E3_RESULT.json",
          "log": A.P_REAL["log"], "part1": A.P_REAL["result"], "part1_n": A.P_REAL["part1_n"],
          "build": "manuscript/prereg/2026-11-12_a_e3_arm/topup1/BUILD_TOPUP1.json"}
S_E_REAL = {f"ae3_{k}_xm600-{m}" for k in ("aya_vision_8b", "smolvlm2_2b", "llava16_mistral_7b", "gemma3_4b_lb26")
            for m in ("short", "detailed")}  # CC-359 ruling 6, as named by the coordinator's brief
EXTRA_RE = re.compile(r"ae3_([a-z0-9_]+)_xm600-(short|detailed)")
SCORE_ARGS = ("--labels", "--labels-sha", "--key", "--topup-labels", "--topup-labels-sha", "--topup-key")
ROW_LABEL = ("development; new decodes on previously analysed images; new labels; single annotator until the second "
             "annotator's top-up overlap is labelled")  # addendum §0
DISCLOSE = {  # addendum §2, printed beside every top-up row
    "annotator": "The PI, an author who knows the study. He saw every value while labelling. He cannot see which caption "
                 "set or reference named a pair.",
    "images_seen_in_part1": "The PI has seen these images in part 1.",
    "leak": "The annotator knows that a top-up session asks about pairs named by new models, so that group is not blind. "
            "Which of the new models named a pair is still hidden. The 50 old repeats and the controls dilute the group, "
            "and they give a cross-session test-retest figure (run document §9.2).",
    "images_and_captions": "The 600 images were analysed before. The S_E captions are new decodes on these images; the "
                           "labels are new."}
D7C = "added after the first batch (A-E3 addendum); second software environment (PyTorch 2.6.0)"  # CC-359 1(b)
KAPPA = ("single annotator: the top-up target kappa (plan §4, 0.60, top-up overlap only; O7) waits for the second "
         "annotator; a row that uses base labels also carries the base part-1 kappa outcome when it exists (CC-355 N5)")


# ------------------------------------------------------------------------------------------------ custody
def refused(path) -> bool:
    p = os.path.abspath(os.fsdecode(path))
    b = os.path.basename(p)
    named = b == "key.json" or (b.startswith(("labels_", "practice_")) and b.endswith(".jsonl")) or \
        (b == "assignment.json" and p != str(ROOT / A.ASSIGN))
    return A.refused(p) or (named and p not in A._LABEL_OK)


def _audit(event: str, args) -> None:
    if event in ("open", "os.listdir", "os.scandir") and args and \
            isinstance(args[0], (str, bytes, os.PathLike)) and refused(args[0]):
        raise Fault(f"custody: {event} refused")


# ------------------------------------------------------------------------------------------------ S_E world
def rel(f: Path) -> str:
    f = Path(f).resolve()
    return str(f.relative_to(ROOT)) if f.is_relative_to(ROOT) else str(f)


def load_extras(paths: list, objects_in, ids: list) -> tuple[dict, dict]:
    """§0 S_E, checked as build_topup step 3: ae3_<key>_xm600-{short,detailed}, LB schema, exactly the I600 ids, str
    captions; both prompts of every model. Mention sets as build_assignment l.74 (objects_in on the caption)."""
    ms_all, meta = {}, {}
    for f in map(Path, paths):
        s = f.name.removesuffix(".preds.json")
        m = EXTRA_RE.fullmatch(s)
        d = json.loads(f.read_text(encoding="utf-8"))
        p = d.get("predictions")
        if not m or s in ms_all or d.get("schema") != "vsps.lb_decode.v1" or not isinstance(p, dict) or \
                set(p) != set(ids) or not all(isinstance(x, str) for x in p.values()):
            raise Fault(f"--extra {f.name}: not an ae3 LB run on exactly the I600 images")
        ms_all[s] = [set(objects_in(p[i])) for i in ids]
        meta[s] = {"model": m[1], "prompt": m[2], "path": rel(f), "sha256": A.sha(f),
                   "batch": "7c" if "/ATTR_H1_7c/" in str(f.resolve()) else "7a"}
    prompts = {}
    for x in meta.values():
        prompts.setdefault(x["model"], set()).add(x["prompt"])
    if not meta or any(v != {"short", "detailed"} for v in prompts.values()):
        raise Fault("S_E needs both prompts of every model")
    return ms_all, meta


def e_ctx(w: dict, names: list) -> dict:
    """bracket.s75_context l.165-170 for the named systems: caption_rows over all mentions, recall over the Open Images
    present classes, M = mentions per caption; the Q25 bootstrap rows (O1)."""
    q, xo, n = w["ctx"]["Q25"], w["br"].v.xo, len(w["ids"])
    g_all = [set().union(*r) for r in w["refs_all"]]
    pos = [{c for c, s in o.items() if s == "present"} for o in w["oi"]]
    out = {}
    for s in names:
        m = w["ms_all"][s]
        L = np.array([len(x) for x in m], float)
        out[s] = {"a": np.asarray([xo.caption_rows(m[k], w["oi"][k], g_all[k], w["vm"]) for k in range(n)], dtype=float),
                  "pr": np.array([len(m[k] & pos[k]) / len(pos[k]) if pos[k] else np.nan for k in range(n)], dtype=float),
                  "M_pt": float(L[q["full"]].sum(1)[0] / n), "M_dr": L[q["idx_boot"]].sum(1) / n}
    return {"name": "s75", "full": q["full"], "idx_boot": q["idx_boot"], "systems": out}


def e_world(w: dict, paths: list, objects_in) -> dict:
    """Addendum §3: the a_cert world of the twelve (built unchanged) plus the S_E caption sets; one family per model."""
    ms_all, meta = load_extras(paths, objects_in, w["ids"])
    se = sorted(ms_all)
    fam = {}
    for s in se:
        fam.setdefault(f"E:{meta[s]['model']}", []).append(s)
    v = {**w, "sys12": list(w["sys"]), "se": se, "sys": list(w["sys"]) + se, "ms_all": {**w["ms_all"], **ms_all},
         "ms": {**w["ms"], **{s: [m & w["vm"] for m in ms_all[s]] for s in se}}, "fam": {**w["fam"], **fam},
         "extras": meta, "pins": {**w["pins"], **{x["path"]: x["sha256"] for x in meta.values()}}}
    v["ctx"] = {**w["ctx"], **{f: e_ctx(v, names) for f, names in fam.items()}}
    return v


def ctx_check(w: dict) -> bool:
    """e_ctx rebuilt for the Q25 systems equals the registered context (a, pr exact; M within 1e-12)."""
    q = w["ctx"]["Q25"]
    mine = e_ctx(w, list(q["systems"]))["systems"]
    return all(np.array_equal(mine[s]["a"], d["a"]) and np.array_equal(mine[s]["pr"], d["pr"], equal_nan=True) and
               abs(mine[s]["M_pt"] - d["M_pt"]) <= 1e-12 and np.allclose(mine[s]["M_dr"], d["M_dr"], rtol=0, atol=1e-12)
               for s, d in q["systems"].items())


def check_build(w: dict, rec: dict) -> None:
    """CC-359 LC4': S_E = counts.new_systems of BUILD_TOPUP1.json, and every file sha = its --extra sha there."""
    ex = {Path(k).name: x for k, x in rec["inputs_sha256"].items()
          if EXTRA_RE.fullmatch(Path(k).name.removesuffix(".preds.json"))}
    if rec["counts"]["new_systems"] != w["se"] or ex != {Path(m["path"]).name: m["sha256"] for m in w["extras"].values()}:
        raise Fault("S_E differs from BUILD_TOPUP1.json")


def e_pairs(w: dict) -> list:
    """Every pair of systems with at least one member in S_E, in the system order (12 as BUILD.json, then S_E)."""
    se = set(w["se"])
    return [(k, a, b) for k, (a, b) in enumerate(p for p in itertools.combinations(w["sys"], 2) if se & set(p))]


def e_idx(w: dict, a: str, b: str):
    """O3: I537 for a pair with a Q3 member, I600 otherwise."""
    return w["idx"]["Q3"] if {a, b} & set(w["fam"]["Q3"]) else w["idx"]["Q25"]


def fam_of(w: dict, s: str) -> str:
    return next(f for f, m in w["fam"].items() if s in m)


def e_scope(w: dict, a: str, b: str) -> str:
    """W5: the two prompts of one A-E3 model form the within-family pair; every other pair is cross-family."""
    return "within" if fam_of(w, a) == fam_of(w, b) else "cross"


def n_u(w: dict) -> list:
    """E4 universe N_u': pairs named by any of the 12 + S_E sets (mapped classes), with no Open Images status."""
    named = [set().union(*(w["ms"][s][k] for s in w["sys"])) for k in range(len(w["ids"]))]
    return [{c for c in named[k] if c not in w["oi"][k]} for k in range(len(w["ids"]))]


def evaluable(p1, p2) -> bool:
    """O6: H3's rule unchanged (NOT EVALUABLE if phi2 = 0 or phi1 + phi2 < 50)."""
    return not (p2 == 0 or p1 + p2 < A.H3_MIN)


def tag(w: dict, s: str) -> dict:
    b = w["extras"][s]["batch"]
    return {"batch": b, "disclosure": D7C if b == "7c" else None}


# ------------------------------------------------------------------------------------------------ freeze (§3)
def freeze_e3_core(w: dict) -> dict:
    """The a_cert freeze loop for the pairs with an S_E member: C-ref grid, w*, V-H, first-two row and the C-label
    verdict (W1); budgets and §4.4 low ends per S_E system on I600; the E4 evaluability. No label is read."""
    two, picks = A.draw_two(w["refs_all"], w["ids"])
    two_f, _ = A.draw_two(w["refs_all"], w["ids"], first_two=True)
    gr, gr_f, gl = A.gold_ref(two, w["vm"]), A.gold_ref(two_f, w["vm"]), A.gold_label(w["oi"])
    js = lambda r: {"verdict": r["verdict"], "dmin": None if r["dmin"] is None else float(r["dmin"]),  # noqa: E731
                    "better": r["better"], "label": A.PRINT_LABEL.get(r["verdict"], r["verdict"])}
    cells = lambda pc: {**{x: pc[x] for x in ("nA", "nB", "tA", "tB")},  # noqa: E731
                        **{x: {"U": pc[x]["U"], "f1": pc[x]["f1"]} for x in ("A", "B", "S")}}
    pairs = []
    for k, a, b in e_pairs(w):
        idx = e_idx(w, a, b)
        pc, pcf, pl = (A.pair_cells(w["ms"], a, b, g, idx) for g in (gr, gr_f, gl))
        grid = {str(x): js(A.certify(pc, x)) for x in A.GRID}
        bt = grid[str(A.W0)]["better"]
        nb, nw = (pc["nA"], pc["nB"]) if bt == "A" else (pc["nB"], pc["nA"])
        d = abs(Fr(pc["tA"], pc["nA"]) - Fr(pc["tB"], pc["nB"])) if pc["nA"] and pc["nB"] else None
        pairs.append({"idx": k, "A": a, "B": b, "scope": e_scope(w, a, b), "n_images": len(idx), "cells": cells(pc),
                      "cref": grid, "w_star": A.w_star(pc),
                      "vh": {str(x): A.certify(pc, x, beta=A.beta_H)["verdict"] for x in A.GRID},
                      "first_two": {str(x): A.certify(pcf, x)["verdict"] for x in A.GRID},
                      "clabel": js(A.certify(pl, 0.0)), "clabel_cells": cells(pl),
                      "dabs": None if d is None else float(d), "n_better": nb, "n_worse": nw})
    by_w = {sc: {str(x): sum(p["cref"][str(x)]["verdict"] == "CERTIFIED" for p in pairs if p["scope"] == sc)
                 for x in A.GRID} for sc in ("within", "cross")}
    i600, f0, rows = w["idx"]["Q25"], w["f0_hat"], {}
    for s in w["se"]:
        c = A.sys_cell(w["ms"], s, gr, i600)
        Lh = float(f0(c["phi1"], c["phi2"], 2, np.inf))
        bb = {str(x): (None if x == 0 else A.beta_B(c, x, A.ALPHA_S)) for x in A.GRID}
        rows[s] = {**{x: c[x] for x in ("n", "t", "U", "f1", "phi1", "phi2")}, "L_hat": Lh,
                   "low": (c["t"] + Lh) / c["n"] if c["n"] else None, "beta": bb,
                   "high": {str(x): (c["t"] + A.cap(c, x, A.ALPHA_S)) / c["n"] if c["n"] else None for x in A.GRID},
                   "floor_beta_w0": math.floor(bb[str(A.W0)]), "binds": math.floor(bb[str(A.W0)]) < c["U"],
                   "oi_present_in_Ns": sum(w["oi"][k].get(x) == "present" for k in i600
                                           for x in w["ms"][s][k] - gr[k]["kp"]), **tag(w, s)}
    nu = n_u(w)
    p1, p2 = sum(len(nu[k] & gr[k]["once"]) for k in i600), sum(len(nu[k] & gr[k]["twice"]) for k in i600)
    return {"schema": "vsps.a_cert_e3.freeze.v1", "status": "development (no labels)", "label": ROW_LABEL,
            "verdict": None, "pins": w["pins"], "extras": w["extras"], "systems_12": w["sys12"], "S_E": w["se"],
            "constants": {"alpha_S": A.ALPHA_S, "grid": A.GRID, "w0": A.W0, "seed": A.SEED, "B_truth": A.B_TRUTH,
                          "image_sets": "O3: I537 for a pair with a Q3 member, I600 otherwise"},
            "refs_draw": picks, "pairs": pairs, "certified_by_w": by_w, "budgets": rows,
            "e3_declared": {"n_binding": sum(r["binds"] for r in rows.values()),
                            "n_oi_above_budget": sum(r["oi_present_in_Ns"] > r["floor_beta_w0"] for r in rows.values())},
            "e4_declared": {"N_u_prime": sum(len(nu[k]) for k in i600), "phi1": p1, "phi2": p2,
                            "f0_hat": float(f0(p1, p2, 2, np.inf)), "evaluable": evaluable(p1, p2)}}


# ------------------------------------------------------------------------------------------------ E rows (§5)
def e2_rows(prs: list) -> dict:
    """H2a counts with no verdict word (§0); w0 primary, the grid secondary (O2); interval as A-CERT H2a."""
    keys = ("n_cert", "n_other", "n_excluded", "n_cert_unconfirmed", "V_c", "V_n")
    by = {}
    for x in A.GRID:
        r = A.h2a_rule([{"verdict": p["cref"][str(x)]["verdict"], "confirmed": p["confirmed"]} for p in prs])
        by[str(x)] = {k: r[k] for k in keys}
    v0 = lambda p: p["cref"][str(A.W0)]["verdict"]  # noqa: E731
    ce, ot = [p for p in prs if v0(p) == "CERTIFIED"], [p for p in prs if v0(p) == "NOT CERTIFIED"]
    ci = np.percentile(np.mean([p["cf_star"] for p in ce], 0) - np.mean([p["cf_star"] for p in ot], 0),
                       [2.5, 97.5]).tolist() if ce and ot else None
    return {"w0": by[str(A.W0)], "Vc_minus_Vn_ci95": ci, "grid_secondary": by,
            "pairs": [{"idx": p["idx"], "verdict": v0(p), "confirmed": p["confirmed"]} for p in prs]}


def stream(Wb: np.ndarray) -> dict:
    """The truth-side bootstrap stream of A-CERT H2a / H3: a_m1.boot_weights(n, default_rng(20261111), 2000)."""
    return {"call": f"a_m1.boot_weights({Wb.shape[1]}, numpy.random.default_rng({A.SEED}), {A.B_TRUTH})",
            "sha256_rows": hashlib.sha256(Wb[1:].tobytes()).hexdigest()}


def score_e3_core(w: dict, fz: dict, key0: dict, ans0: dict, key1: dict, ans1: dict) -> dict:
    """§4 completed status (base pairs: base part-1 labels; top-up pairs: top-up part-1 labels; last line wins; Open
    Images never overridden; agreement-only answers never enter a status), then E1-E6. Certified set, orientation and
    budgets come from FREEZE_E3 and are never recomputed."""
    h0, _ = A.human(key0, ans0, w["syn"])
    h1, _ = A.human(key1, ans1, w["syn"])
    named12 = {(w["ids"][k], c) for s in w["sys12"] for k in range(len(w["ids"])) for c in w["ms_all"][s][k]}
    if set(h0) & set(h1) or set(h1) & named12:
        raise Fault("a top-up target is a base pair")
    h = {**h0, **h1}
    cn = {s: A.counts(w, s, h) for s in w["sys"]}
    n, i600 = len(w["ids"]), w["idx"]["Q25"]
    gr = A.gold_ref(A.draw_two(w["refs_all"], w["ids"])[0], w["vm"])
    # E1 (P_c, Q25 bootstrap, remainder ends; O1, O11) and E5 (detailed - short, points only; O4, W5)
    e1, e5 = {}, {}
    for f in sorted(x for x in w["fam"] if x.startswith("E:")):
        add = {m: {s: (cn[s]["hy"] + (cn[s]["rem"] if m == "hi" else 0), cn[s]["hn"] + (cn[s]["rem"] if m == "lo" else 0))
                   for s in w["fam"][f]} for m in ("reg", "lo", "hi")}
        r = {m: A.fam_slopes(w, f, add[m]) for m in add}
        for s in w["fam"][f]:
            e1[s] = {"P_c": float(r["reg"]["per"][s]["P"][0]), "P_c_ci95": r["reg"]["ci"](r["reg"]["per"][s]["P"][1]),
                     "P_c_lo": float(r["lo"]["per"][s]["P"][0]), "P_c_hi": float(r["hi"]["per"][s]["P"][0]),
                     "counts_I600": {k: int(x[i600].sum()) for k, x in cn[s].items()}, **tag(w, s)}
        pr = {w["extras"][s]["prompt"]: s for s in w["fam"][f]}
        d = lambda m, k: float(r[m]["per"][pr["detailed"]][k][0] - r[m]["per"][pr["short"]][k][0])  # noqa: E731
        e5[f[2:]] = {"dF_c": {m: d(m, "F") for m in r}, "dP_c": d("reg", "P"), "d_lnM": d("reg", "lnM"),
                     "points": {s: {k: float(r["reg"]["per"][s][k][0]) for k in ("F", "P", "R", "lnM")}
                                for s in pr.values()}, **tag(w, pr["short"])}
    # E2: H2a counts on FREEZE_E3 verdicts; truth = P_c in the frozen direction at reg and both ends
    Wt = w["boot_weights"](n, np.random.default_rng(A.SEED), A.B_TRUTH)
    prs = []
    for p in fz["pairs"]:
        idx = e_idx(w, p["A"], p["B"])
        if len(idx) != p["n_images"]:
            raise Fault("image set differs from FREEZE_E3")
        ea, eb = A.pc_ends(cn[p["A"]], Wt[:, idx], idx), A.pc_ends(cn[p["B"]], Wt[:, idx], idx)
        bt = p["cref"][str(A.W0)]["better"]
        cf = A.confirmed(ea, eb) if bt == "A" else A.confirmed(eb, ea) if bt == "B" else np.zeros(len(Wt), bool)
        prs.append({"idx": p["idx"], "scope": p["scope"], "cref": p["cref"], "confirmed": bool(cf[0]), "cf_star": cf[1:]})
    e2 = {sc: e2_rows([p for p in prs if p["scope"] == sc]) for sc in ("within", "cross")}
    e2["stream"] = stream(Wt)
    # E3: budget coverage on I600 with the FREEZE_E3 budgets
    rows = {}
    for s in w["se"]:
        x = xh = 0
        for k in i600:
            for c in w["ms"][s][k] - gr[k]["kp"]:
                st, a = w["oi"][k].get(c), h.get((w["ids"][k], c))
                x += st == "present" or (st is None and a == "Y")
                xh += st == "present" or (st is None and a in ("Y", None))
        bz = fz["budgets"][s]
        rows[s] = {"x": int(x), "x_hi": int(xh), "U": bz["U"], "f1": bz["f1"], "floor_beta_w0": bz["floor_beta_w0"],
                   "covered": xh <= bz["floor_beta_w0"],
                   "covered_by_w": {k: xh <= math.floor(b) for k, b in bz["beta"].items() if b is not None},
                   "w_hat": bz["f1"] / (bz["f1"] + 2 * x) if bz["f1"] + x else None, **tag(w, s)}
    e3 = {"systems": rows, "n_covered": sum(r["covered"] for r in rows.values()), "n_systems": len(rows),
          "n_binding": sum(r["floor_beta_w0"] < r["U"] for r in rows.values())}
    # E4: H3 on N_u' (O6: no RESPECTED / VIOLATED word)
    Wb = w["boot_weights"](len(i600), np.random.default_rng(A.SEED), A.B_TRUTH)
    nu = n_u(w)
    e4 = A.h3_row(w, gr, h, nu, Wb, i600)
    e4.pop("reading_no_verdict")
    ev = evaluable(e4["phi1"], e4["phi2"])
    e4.update(N_u_prime=sum(len(nu[k]) for k in i600), evaluable=ev, label=None if ev else "NOT EVALUABLE", stream=stream(Wb),
              n_ref_named_completed_absent=sum(w["oi"][k].get(c) == "absent" or h.get((w["ids"][k], c)) == "N"
                                               for k in i600 for c in gr[k]["kp"]))
    # E6: agreement only (§4: these answers never enter a status)
    yn = ("Y", "N")
    b1 = {(k["image"], k["class"]): q for q, k in key0.items() if k["part"] == 1 and k["role"] == "target"}
    b3 = {(k["image"], k["class"]) for k in key0.values() if k["part"] == 3}
    old = []
    for q, k in key1.items():
        if k["role"] == "old_repeat":
            if (k["image"], k["class"]) not in b1:
                raise Fault("an old_repeat item is not a base part-1 target")
            old.append(((k["image"], k["class"]), ans1.get(q), ans0.get(b1[(k["image"], k["class"])])))
    both = [(a, b) for _, a, b in old if a in yn and b in yn]
    exp = {"ctrl_present": "Y", "ctrl_absent": "N", "foil_absent": "N"}
    c1 = [(k, ans1.get(q)) for q, k in key1.items() if k["part"] == 1 and k["role"] in exp]
    t1 = {(k["image"], k["class"]): ans1.get(q) for q, k in key1.items() if k["part"] == 1 and k["role"] == "target"}
    rep = [ans1.get(q) == t1.get((k["image"], k["class"])) for q, k in key1.items() if k["part"] == 3 and q in ans1]
    e6 = {"old_repeat": {"n": len(old), "n_YN_both": len(both), "agree": sum(a == b for a, b in both),
                         "agreement": sum(a == b for a, b in both) / len(both) if both else None,
                         **{f"topup_{u}": sum(a == u for _, a, _ in old) for u in ("U", "A")},
                         "topup_unanswered": sum(a is None for _, a, _ in old),
                         **{f"base_{u}": sum(b == u for _, _, b in old) for u in ("U", "A")}},
          "old_repeat_also_base_part3": sum(p in b3 for p, _, _ in old),
          "controls_by_role": {r: A.ctl_row([a for k, a in c1 if k["role"] == r], e) for r, e in exp.items()},
          "controls_absent_by_hint_coverage": {cov: A.ctl_row([a for k, a in c1 if k["role"] != "ctrl_present" and
                                                               A.hint_full(w, k["image"], k["class"]) == (cov == "full")],
                                                              "N") for cov in ("full", "partial")},
          "topup_part3_repeat": {"n_answered": len(rep), "agree": sum(rep), "agreement": sum(rep) / len(rep) if rep
                                 else None, "answered": A.repeat_label(len(rep), sum(k["part"] == 3 for k in key1.values()))},
          "note": "reported whatever its value; no gate (CC-355 W5)"}
    return {"schema": "vsps.a_cert_e3.result.v1", "label": ROW_LABEL, "verdict": None, "disclosures": DISCLOSE,
            "kappa": KAPPA, "added_models": {s: D7C for s in w["se"] if w["extras"][s]["batch"] == "7c"},
            **{k: {"row_label": ROW_LABEL, **v} for k, v in (("E1", e1), ("E2", e2), ("E3", e3), ("E4", e4), ("E5", e5),
                                                              ("E6", e6))}}


# ------------------------------------------------------------------------------------------------ modes
def log_lines(P: dict) -> list:
    return (ROOT / P["log"]).read_text(encoding="utf-8").splitlines()


def pinned(P: dict, key: str, word: str) -> tuple[dict, str]:
    fp = ROOT / P[key]
    if not fp.exists():
        raise Fault(f"no {word}")
    h = A.sha(fp)
    if not any(word in ln and h in ln for ln in log_lines(P)):
        raise Fault(f"no {word} pin line in the LOG")
    return json.loads(fp.read_text(encoding="utf-8")), h


def real_world(paths: list, score: bool = False) -> dict:
    w = A._score_world() if score else A._load_world()
    from rescap.chair import objects_in
    return e_world(w, paths, objects_in)


def e3_freeze(paths: list, P: dict = P_REAL, wfn=None) -> int:
    """§3: label-free; the 12-system gate reproduces first (in memory); writes once; FAULT <type> only."""
    try:
        out = ROOT / P["freeze"]
        if out.exists():
            raise Fault("FREEZE_E3.json exists")
        extra = {}
        if P is P_REAL:
            if not all(A.committed(x) for x in (SELF, ADD, A.SELF)) or \
                    (A.sha(ROOT / ADD), A.sha(ROOT / A.SELF)) != (SHA_ADD, SHA_ACERT):
                raise Fault("a_cert_e3.py, a_cert.py and the addendum must equal their registered HEAD blobs")
            if not A.sha(ROOT / FREEZE12).startswith(FREEZE12_SHA):
                raise Fault("the 12-system FREEZE changed")
            w12 = A._load_world()
            cells = A.gate_core(w12, *(json.loads((ROOT / x).read_text(encoding="utf-8")) for x in (A.ASSIGN, A.BUILD,
                                                                                                  A.BRACKET)))
            if not all(c["ok"] for c in cells):
                raise Fault("the 12-system gate does not reproduce (A-CERT §11)")
            from rescap.chair import objects_in
            w = e_world(w12, paths, objects_in)
            if set(w["se"]) != S_E_REAL:
                raise Fault("S_E is not the CC-359 set")
            extra = {"gate12_cells_ok": len(cells), "freeze12_sha256": A.sha(ROOT / FREEZE12)}
        else:
            w = wfn(paths)
        check_build(w, json.loads((ROOT / P["build"]).read_text(encoding="utf-8")))
        if not ctx_check(w):
            raise Fault("the S_E context builder differs from bracket.s75_context")
        fz = freeze_e3_core(w)
        fz["provenance"] = {"script_sha256": A.sha(__file__), "a_cert_sha256": A.sha(A.__file__),
                            "build_topup1_sha256": A.sha(ROOT / P["build"]), **extra}
        json.dumps(fz, default=float)
    except BaseException as e:  # noqa: BLE001  (fault rule: exception type only)
        print(f"FAULT {type(e).__name__}")
        return 2
    print(json.dumps({"wrote": P["freeze"], "sha256": A.write_atomic(out, fz)}))
    return 0


def e3_score(a: dict, P: dict = P_REAL, wfn=None) -> int:
    """§6 step 3: once; every label-free check before the first label byte; one atomic write; FAULT <type> only."""
    try:
        res = ROOT / P["result"]
        if res.exists():
            raise Fault("result exists (one pass only)")
        fz, fsha = pinned(P, "freeze", "FREEZE_E3")
        r1, r1sha = pinned(P, "part1", "A_CERT_RESULT")  # §6 step 1: the part-1 scoring run comes first
        log = log_lines(P)
        if r1["provenance"]["labels_sha256"] != a["labels_sha"]:
            raise Fault("the base labels are not the copy the part-1 score read")
        if not any("topup1" in ln and a["topup_labels_sha"] in ln for ln in log):
            raise Fault("no top-up session-end line")
        if P is P_REAL and (not all(A.committed(x) for x in (SELF, ADD, A.SELF)) or
                            (A.sha(ROOT / ADD), A.sha(ROOT / A.SELF)) != (SHA_ADD, SHA_ACERT)):
            raise Fault("a_cert_e3.py, a_cert.py and the addendum must equal their registered HEAD blobs")
        w = wfn() if wfn else real_world([ROOT / m["path"] for m in fz["extras"].values()], score=True)
        if w["pins"] != fz["pins"]:
            raise Fault("inputs differ from FREEZE_E3 pins")
        files = [a["labels"], a["key"], a["topup_labels"], a["topup_key"]]
        A._LABEL_OK.update(os.path.abspath(x) for x in files)
        lb0, kb0, lb1, kb1 = (Path(x).read_bytes() for x in files)  # hash and parse the same bytes
        hx = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
        if hx(lb0) != a["labels_sha"] or hx(lb1) != a["topup_labels_sha"]:
            raise Fault("label copy sha differs from its argument")
        if hx(kb0) != r1["provenance"]["key_sha256"] or (P is P_REAL and hx(kb0) != A.KEY_SHA):
            raise Fault("base key.json is not the pinned key")
        if not any("topup1" in ln and hx(kb1) in ln for ln in log):
            raise Fault("top-up key.json not pinned")
        key0, key1 = json.loads(kb0.decode("utf-8")), json.loads(kb1.decode("utf-8"))
        ans0, ans1 = A.answers(lb0.decode("utf-8").splitlines()), A.answers(lb1.decode("utf-8").splitlines())
        part1 = {q for q, k in key0.items() if k["part"] == 1}
        if len(part1) != P["part1_n"] or len(part1 & ans0.keys()) != P["part1_n"]:
            raise Fault("base part 1 is not complete")
        out = score_e3_core(w, fz, key0, ans0, key1, ans1)
        out["provenance"] = {"freeze_e3_sha256": fsha, "part1_result_sha256": r1sha, "labels_sha256": hx(lb0),
                             "key_sha256": hx(kb0), "topup_labels_sha256": hx(lb1), "topup_key_sha256": hx(kb1),
                             "script_sha256": A.sha(__file__), "a_cert_sha256": A.sha(A.__file__)}
        json.dumps(out, default=float)
    except BaseException as e:  # noqa: BLE001  (fault rule: exception type only)
        print(f"FAULT {type(e).__name__}")
        return 2
    finally:
        A._LABEL_OK.clear()
    print(json.dumps({"wrote": P["result"], "sha256": A.write_atomic(res, out)}))
    return 0


# ------------------------------------------------------------------------------------------------ selftest
def selftest(out: Path) -> int:
    ck = {}
    try:
        _selftest_checks(ck)
    except BaseException as e:  # noqa: BLE001  (recorded; the mutant harness never counts it as a kill)
        ck[f"no_exception ({type(e).__name__}: {str(e)[:80]})"] = False
    ck = {k: bool(x) for k, x in ck.items()}
    rec = {"schema": "vsps.a_cert_e3.selftest.v1", "script_sha256": A.sha(__file__), "a_cert_sha256": A.sha(A.__file__),
           "checks": ck, "n": len(ck), "pass": all(ck.values())}
    Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print("\n".join(f"{'ok  ' if x else 'FAIL'} {k}" for k, x in ck.items()))
    print("selftest ok" if rec["pass"] else "selftest FAILED")
    return 0 if rec["pass"] else 1


def _lb(d: dict) -> str:
    return json.dumps({"schema": "vsps.lb_decode.v1", "predictions": d})


def _oi_fake(t: str) -> list:
    return [x for x in t.split(";") if x and x != "SENTINELCAP"]


def _q(tag_: str, part: int, i: str, c: str) -> str:
    return hashlib.sha256(f"{A.SEED}|{tag_}{part}|{i}|{c}".encode()).hexdigest()[:12]


def _mini(br, tmp: Path) -> tuple[dict, list]:
    """Two images, one Q25 system q, one Q3 system r (image j only), one A-E3 model aa (two prompts). Values in the
    checks below are computed by hand from these sets (E3_READ_PACKAGE.md §5)."""
    vm = set("abcde")
    ms_all = {"q": [{"a"}, {"c"}], "r": [{"a", "b"}, {"d"}]}
    w = {"ids": ["i", "j"], "sys": ["q", "r"], "vm": vm, "syn": {c: c for c in vm}, "ms_all": ms_all,
         "ms": {s: [m & vm for m in x] for s, x in ms_all.items()},
         "refs_all": [[{"a", "c"}, {"c", "u"}], [{"d"}, {"c"}]],
         "oi": [{"a": "present", "b": "absent"}, {"c": "present", "e": "absent"}],
         "fam": {"Q25": ["q"], "Q3": ["r"]}, "idx": {"Q25": np.arange(2), "Q3": np.array([1])},
         "ctx": {"Q25": {"full": np.arange(2)[None], "idx_boot": np.random.default_rng(0).integers(0, 2, (2000, 2))}},
         "br": br, "pins": {"mini": "synthetic"}, "f0_hat": A._p50x().f0_hat, "boot_weights": A._a_m1().boot_weights,
         "pos_mids": {"e": {"e/a"}}, "oi_neg": {"j": {"e/a"}}}
    d = tmp / "mini" / "ATTR_H1"
    d.mkdir(parents=True)
    caps = {"short": {"i": "a;c;d;SENTINELCAP", "j": "c;e;u;SENTINELCAP"},
            "detailed": {"i": "a;b;c;d;e;SENTINELCAP", "j": "c;d;e;u;SENTINELCAP"}}
    paths = []
    for m, cp in caps.items():
        paths.append(d / f"ae3_aa_xm600-{m}.preds.json")
        paths[-1].write_text(_lb(cp), encoding="utf-8")
    return w, paths


def _mini_labels() -> tuple[dict, dict, dict, dict]:
    """Base: targets (i,c) N then Y, (j,d) N; ctrl_present (i,a); part 3 (i,c). Top-up: targets (i,d) Y, (i,e) U;
    ctrl_absent (j,e) N; old_repeat (i,c) Y, (j,d) U; part 2 (j,u) Y; part 3 (i,d) Y."""
    k0 = {_q("", 1, "i", "c"): ("i", "c", 1, "target"), _q("", 1, "j", "d"): ("j", "d", 1, "target"),
          _q("", 1, "i", "a"): ("i", "a", 1, "ctrl_present"), _q("", 3, "i", "c"): ("i", "c", 3, "repeat")}
    k1 = {_q("topup1|", 1, "i", "d"): ("i", "d", 1, "target"), _q("topup1|", 1, "i", "e"): ("i", "e", 1, "target"),
          _q("topup1|", 1, "j", "e"): ("j", "e", 1, "ctrl_absent"), _q("topup1|", 1, "i", "c"): ("i", "c", 1, "old_repeat"),
          _q("topup1|", 1, "j", "d"): ("j", "d", 1, "old_repeat"), _q("topup1|", 2, "j", "u"): ("j", "u", 2, "target"),
          _q("topup1|", 3, "i", "d"): ("i", "d", 3, "repeat")}
    key = lambda kk: {q: {"image": i, "class": c, "part": p, "role": r} for q, (i, c, p, r) in kk.items()}  # noqa: E731
    l0 = ["N", "Y", "N", "Y", "Y"]
    q0 = list(k0)
    a0 = A.answers(json.dumps({"qid": q, "label": x}) for q, x in zip([q0[0]] + q0, l0))
    a1 = A.answers(json.dumps({"qid": q, "label": x}) for q, x in zip(k1, ["Y", "U", "N", "Y", "U", "Y", "Y"]))
    return key(k0), a0, key(k1), a1


def _selftest_checks(ck: dict) -> None:
    import contextlib
    import io
    import shutil
    br = A.test_mods()
    tmp = Path(tempfile.mkdtemp(prefix="a_cert_e3_selftest_"))
    near = lambda a, b: a is not None and abs(a - b) < 1e-9  # noqa: E731
    # ---- mini world: FREEZE_E3 contents by hand
    m12, mp = _mini(br, tmp)
    w = e_world(m12, mp, _oi_fake)
    D, S = "ae3_aa_xm600-detailed", "ae3_aa_xm600-short"
    fz = freeze_e3_core(w)
    P_ = {p["idx"]: p for p in fz["pairs"]}
    ck["freeze_pairs_with_an_S_E_member_only"] = [(p["A"], p["B"]) for p in fz["pairs"]] == [
        ("q", D), ("q", S), ("r", D), ("r", S), (D, S)]
    ck["freeze_O3_I537_for_Q3_member_else_I600"] = [p["n_images"] for p in fz["pairs"]] == [2, 2, 1, 1, 2]
    ck["freeze_W5_within_is_the_model_pair"] = [p["scope"] for p in fz["pairs"]] == ["cross"] * 4 + ["within"]
    ck["freeze_cref_cells_by_hand"] = P_[0]["cells"] == {"nA": 2, "nB": 8, "tA": 2, "tB": 4, "A": {"U": 0, "f1": 0},
                                                         "B": {"U": 4, "f1": 1}, "S": {"U": 0, "f1": 2}} and \
        P_[4]["cells"] == {"nA": 8, "nB": 5, "tA": 4, "tB": 3, "A": {"U": 2, "f1": 1}, "B": {"U": 0, "f1": 0},
                           "S": {"U": 2, "f1": 2}}
    ck["freeze_cref_by_hand"] = [(p["cref"]["0.2"]["verdict"], p["cref"]["0.2"]["dmin"], p["cref"]["0.2"]["better"])
                                 for p in fz["pairs"]] == [("NOT CERTIFIED", 0.0, "A")] * 4 + [
        ("NOT CERTIFIED", float(Fr(-3, 20)), "B")]
    L80 = math.log(80)

    def beta1(w_):  # V-B by hand for f1 = 1, alpha_S = 0.025
        c = (1 - w_) / (2 * w_)
        f1p = 1 + L80 + math.sqrt(L80 ** 2 + 2 * L80)
        return c + (1 + c) * L80 / 3 + math.sqrt(((1 + c) * L80 / 3) ** 2 + 2 * c * (1 + c) * f1p * L80)

    ws = P_[0]["w_star"]  # pair 0 certifies once floor(beta) < U(B-only) = 4, i.e. beta(1, w) < 4
    ck["freeze_w_star_by_hand"] = isinstance(ws, float) and 0.9 < ws < 0.95 and beta1(ws) < 4 <= beta1(ws - 1e-6) and \
        [p["w_star"] for p in fz["pairs"][1:]] == ["NI"] * 4
    ck["freeze_W1_clabel_by_hand"] = [(p["clabel"]["verdict"], p["clabel"]["dmin"], p["clabel"]["better"])
                                      for p in fz["pairs"]] == [
        ("CERTIFIED", 0.25, "A"), ("CERTIFIED", 0.2, "A"), ("NOT CERTIFIED", float(Fr(-1, 3)), "B"),
        ("NOT CERTIFIED", -0.5, "B"), ("NOT CERTIFIED", -0.1, "B")] and \
        P_[0]["clabel_cells"]["B"] == {"U": 4, "f1": 0} and P_[3]["clabel_cells"]["A"]["U"] == 1
    ck["freeze_margin_and_lengths_by_hand"] = [(p["dabs"], p["n_better"], p["n_worse"]) for p in fz["pairs"]] == [
        (0.5, 2, 8), (0.4, 2, 5), (float(Fr(1, 3)), 1, 3), (0.5, 1, 2), (float(Fr(1, 10)), 5, 8)]
    bD, bS = fz["budgets"][D], fz["budgets"][S]
    ck["freeze_budgets_and_44_low_ends_by_hand"] = \
        [bD[k] for k in ("n", "t", "U", "f1", "phi1", "phi2")] == [8, 4, 4, 3, 3, 1] and bD["L_hat"] == 2.25 and \
        bD["low"] == 0.78125 and [bS[k] for k in ("n", "t", "U", "f1", "phi1", "phi2")] == [5, 3, 2, 2, 2, 1] and \
        bS["L_hat"] == 1.0 and bS["low"] == 0.8 and all(x == 1.0 for b in (bD, bS) for x in b["high"].values())
    ck["freeze_beta_w0_alpha_S_0.025"] = bD["floor_beta_w0"] == math.floor(
        2 * 3 + math.log(80) + math.sqrt(math.log(80) ** 2 + 12 * (3 + math.log(80) + math.sqrt(
            math.log(80) ** 2 + 6 * math.log(80))) * math.log(80))) == 37 and not bD["binds"] and bD["beta"]["0.0"] is None
    ck["freeze_E4_declared_by_hand"] = fz["e4_declared"] == {"N_u_prime": 4, "phi1": 1, "phi2": 1, "f0_hat": 0.25,
                                                             "evaluable": False}
    ck["freeze_label_and_no_verdict"] = fz["label"] == ROW_LABEL and fz["verdict"] is None and \
        fz["certified_by_w"]["within"]["0.2"] == fz["certified_by_w"]["cross"]["0.2"] == 0
    ck["extras_mention_sets_and_family"] = w["ms"][D] == [set("abcde"), set("cde")] and \
        w["fam"]["E:aa"] == [D, S] and w["extras"][S]["batch"] == "7a" and w["pins"][rel(mp[1])] == A.sha(mp[1])
    # ---- mini world: E rows by hand
    k0, a0, k1, a1 = _mini_labels()
    res = score_e3_core(w, fz, k0, a0, k1, a1)
    e1D, e1S = res["E1"][D], res["E1"][S]
    ck["E1_P_c_by_hand_base_and_topup_labels"] = near(e1D["P_c"], 400 / 7) and near(e1S["P_c"], 80.0) and \
        e1D["counts_I600"] == {"pm": 2, "am": 2, "hy": 2, "hn": 1, "rem": 1}
    ck["E1_remainder_ends_by_hand"] = near(e1D["P_c_lo"], 50.0) and near(e1D["P_c_hi"], 62.5) and \
        near(e1S["P_c_lo"], 80.0) and near(e1S["P_c_hi"], 80.0)
    ib = np.random.default_rng(0).integers(0, 2, (2000, 2))[:500]
    cnt = np.stack([(ib == 0).sum(1), (ib == 1).sum(1)], 1)
    pd = 100 * (cnt @ np.array([3.0, 1.0])) / np.maximum(cnt @ np.array([4.0, 3.0]), 1e-9)
    ck["E1_ci_Q25_bootstrap_first_500_rows"] = np.allclose(e1D["P_c_ci95"], np.nanpercentile(pd, [2.5, 97.5]),
                                                           rtol=0, atol=1e-9)
    e5 = res["E5"]["aa"]
    ck["E5_detailed_minus_short_by_hand"] = near(e5["dF_c"]["reg"], -1600 / 99) and near(e5["dP_c"], -800 / 35) and \
        near(e5["d_lnM"], math.log(1.5)) and near(e5["points"][D]["R"], 100.0) and \
        near(e5["dF_c"]["lo"], 100 * (2 / 3 - 8 / 9)) and near(e5["dF_c"]["hi"], 100 * (2 * .625 / 1.625 - 8 / 9))
    e2 = res["E2"]
    ck["E2_counts_by_hand_within_cross"] = \
        e2["within"]["w0"] == {"n_cert": 0, "n_other": 1, "n_excluded": 0, "n_cert_unconfirmed": 0, "V_c": None,
                               "V_n": 1.0} and \
        [p["confirmed"] for p in e2["cross"]["pairs"]] == [True, True, False, False] and e2["cross"]["w0"]["V_n"] == 0.5
    t = json.loads(json.dumps(fz, default=float))
    t["pairs"][1]["cref"]["0.2"]["verdict"] = "CERTIFIED"
    t["pairs"][4]["cref"]["0.2"]["better"] = "A"
    t["budgets"][D]["floor_beta_w0"] = t["budgets"][S]["floor_beta_w0"] = 1
    rt = score_e3_core(w, t, k0, a0, k1, a1)
    ck["E2_certified_set_from_freeze"] = rt["E2"]["cross"]["w0"] == {
        "n_cert": 1, "n_other": 3, "n_excluded": 0, "n_cert_unconfirmed": 0, "V_c": 1.0, "V_n": 1 / 3} and \
        rt["E2"]["cross"]["Vc_minus_Vn_ci95"] is not None
    ck["E2_orientation_from_freeze"] = [p["confirmed"] for p in rt["E2"]["within"]["pairs"]] == [False]
    e3 = res["E3"]["systems"]
    ck["E3_x_and_x_hi_by_hand"] = (e3[D]["x"], e3[D]["x_hi"], e3[S]["x"], e3[S]["x_hi"]) == (1, 2, 1, 1) and \
        near(e3[D]["w_hat"], 0.6) and near(e3[S]["w_hat"], 0.5) and res["E3"]["n_covered"] == 2
    ck["E3_covered_uses_x_hi_and_freeze_budget"] = rt["E3"]["systems"][D]["covered"] is False and \
        rt["E3"]["systems"][S]["covered"] is True and rt["E3"]["n_covered"] == 1
    e4 = res["E4"]
    ck["E4_by_hand_on_N_u_prime"] = (e4["phi1"], e4["phi2"], e4["f0_hat"], e4["X"], e4["X_hi"], e4["D"], e4["D_hi"],
                                     e4["N_u_prime"]) == (1.0, 1.0, 0.25, 1.0, 2.0, 0.75, 1.75, 4) and \
        e4["n_ref_named_completed_absent"] == 1
    ck["E4_O6_not_evaluable_no_verdict_word"] = e4["evaluable"] is False and e4["label"] == "NOT EVALUABLE" and \
        "reading_no_verdict" not in e4
    e6 = res["E6"]
    ck["E6_old_repeat_vs_base_last_line_by_hand"] = e6["old_repeat"] == {
        "n": 2, "n_YN_both": 1, "agree": 1, "agreement": 1.0, "topup_U": 1, "topup_A": 0, "topup_unanswered": 0,
        "base_U": 0, "base_A": 0}
    ck["E6_controls_by_hand"] = e6["controls_by_role"]["ctrl_absent"]["agree"] == 1 and \
        e6["controls_by_role"]["ctrl_absent"]["n"] == 1 and e6["controls_by_role"]["ctrl_present"]["n"] == 0 and \
        (e6["controls_absent_by_hint_coverage"]["full"]["n"], e6["controls_absent_by_hint_coverage"]["partial"]["n"]) \
        == (1, 0)
    ck["E6_topup_part3_and_old_in_base_part3_by_hand"] = e6["topup_part3_repeat"]["agree"] == 1 and \
        e6["topup_part3_repeat"]["answered"] == "1 of 1" and e6["old_repeat_also_base_part3"] == 1
    h0m = A.human(k0, a0, w["syn"])[0]
    hm = {**h0m, **A.human(k1, a1, w["syn"])[0]}
    ck["twelve_systems_untouched_by_topup_labels"] = len(hm) == 4 and all(
        np.array_equal(A.counts(w, s, hm)[x], A.counts(w, s, h0m)[x]) for s in w["sys12"]
        for x in ("pm", "am", "hy", "hn", "rem"))
    for name, (i_, c_) in (("topup_target_on_a_base_pair_is_a_fault", ("i", "c")),
                           ("topup_target_named_by_a_twelve_system_is_a_fault", ("i", "b"))):
        bad = {**k1, _q("topup1|", 1, i_, c_): {"image": i_, "class": c_, "part": 1, "role": "target"}}
        try:
            score_e3_core(w, fz, k0, a0, bad, {**a1, _q("topup1|", 1, i_, c_): "Y"})
            ck[name] = False
        except Fault:
            ck[name] = True
    blob = json.dumps(res, default=float)
    ck["result_no_verdict_words"] = res["verdict"] is None and not any(
        x in blob for x in ("PASS", "FAIL", "RESPECTED", "VIOLATED", "VALID", "REFUTED", "INCONCLUSIVE")) and \
        all("label" not in e2[s]["w0"] for s in ("within", "cross"))
    ro = np.random.default_rng(20261111)
    want = hashlib.sha256(np.array([np.bincount(ro.integers(0, 2, 2), minlength=2) for _ in range(2000)],
                                   float).tobytes()).hexdigest()
    ck["E2_stream_boot_weights_rng_20261111"] = e2["stream"]["sha256_rows"] == want
    ck["E4_stream_boot_weights_rng_20261111"] = res["E4"]["stream"]["sha256_rows"] == want
    txt = (ROOT / ADD).read_text(encoding="utf-8")
    ck["labels_verbatim_addendum_and_CC359"] = f'"{ROW_LABEL}"' in txt and all(x in txt for x in DISCLOSE.values()) \
        and D7C in " ".join((ROOT / CC359).read_text(encoding="utf-8").split()) and res["label"] == ROW_LABEL
    ck["row_label_on_every_E_row"] = all(res[f"E{j}"].get("row_label") == ROW_LABEL for j in range(1, 7))
    # ---- fixture world (A-CERT fixture, 40 images) + two models, one from the 7c pull
    w12 = A.fixture(br)
    rng = np.random.default_rng(3)
    cls = sorted(w12["vm"]) + ["u0"]
    paths = []
    for mdl, sub in (("aa", "ATTR_H1"), ("bb", "ATTR_H1_7c")):
        (tmp / sub).mkdir(exist_ok=True)
        for pmt, q in (("short", .35), ("detailed", .6)):
            paths.append(tmp / sub / f"ae3_{mdl}_xm600-{pmt}.preds.json")
            paths[-1].write_text(_lb({i: ";".join([c for c in cls if rng.random() < q] + ["SENTINELCAP"])
                                      for i in w12["ids"]}), encoding="utf-8")
    wf = lambda ps: e_world(w12, ps, _oi_fake)  # noqa: E731
    W = wf(paths)
    ck["ctx_builder_equals_registered_s75_context"] = ctx_check(W)
    try:
        load_extras(paths[:1], _oi_fake, w12["ids"])
        ck["extras_need_both_prompts"] = False
    except Fault:
        ck["extras_need_both_prompts"] = True
    rec = {"counts": {"new_systems": W["se"]}, "inputs_sha256": {str(p): A.sha(p) for p in paths}}
    (tmp / "BUILD_TOPUP1.json").write_text(json.dumps(rec), encoding="utf-8")
    (tmp / "BUILD_bad.json").write_text(json.dumps({**rec, "counts": {"new_systems": W["se"][:3]}}), encoding="utf-8")
    PF = {"freeze": str(tmp / "fz" / "FREEZE_E3.json"), "build": str(tmp / "BUILD_bad.json")}

    def quiet(fn):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = fn()
        return rc, buf.getvalue()

    ck["freeze_refuses_S_E_not_in_build_record"] = quiet(lambda: e3_freeze(paths, PF, wf)) == (2, "FAULT Fault\n") \
        and not Path(PF["freeze"]).exists()
    PF["build"] = str(tmp / "BUILD_TOPUP1.json")
    rc, so = quiet(lambda: e3_freeze(paths, PF, wf))
    fzt = Path(PF["freeze"]).read_text(encoding="utf-8") if rc == 0 else ""
    FZ = json.loads(fzt) if fzt else json.loads(json.dumps(freeze_e3_core(W), default=float))  # later checks still run
    ck["freeze_mode_writes_and_prints_sha"] = rc == 0 and json.loads(so)["sha256"] == A.sha(PF["freeze"])
    ck["freeze_writes_once"] = quiet(lambda: e3_freeze(paths, PF, wf)) == (2, "FAULT Fault\n") and \
        Path(PF["freeze"]).exists() and Path(PF["freeze"]).read_text(encoding="utf-8") == fzt
    ck["freeze_fixture_54_pairs_2_within_O3"] = len(FZ.get("pairs", [])) == 54 and \
        sum(p["scope"] == "within" for p in FZ["pairs"]) == 2 and all(
            p["n_images"] == (35 if {p["A"], p["B"]} & set(w12["fam"]["Q3"]) else 40) for p in FZ["pairs"])
    if not fzt:  # a failed freeze mode is already recorded above; the e3-score checks below still need a file
        A.write_atomic(Path(PF["freeze"]), FZ)
    # E1 through the registered slope code equals P_c of pc_ends on the fixture, all S_E systems, reg and both ends
    key0, lab0 = A.fixture_labels(w12)
    ans0 = A.answers(lab0)
    named = {(i, c) for k, i in enumerate(w12["ids"]) for s in w12["sys"] for c in w12["ms_all"][s][k]} | \
        {(i, c) for k, i in enumerate(w12["ids"]) for r in w12["refs_all"][k] for c in r}
    pos = {i: k for k, i in enumerate(w12["ids"])}
    new = sorted({(i, c) for s in W["se"] for k, i in enumerate(w12["ids"]) for c in W["ms_all"][s][k]} - named)
    key1 = {}
    for i, c in new:
        st = w12["oi"][pos[i]].get(c)
        part, role = (2, "target") if c not in w12["vm"] else (1, "target") if st is None else \
            (1, "ctrl_absent") if st == "absent" else (1, "ctrl_present")
        key1[_q("topup1|", part, i, c)] = {"image": i, "class": c, "part": part, "role": role}
    t1k = [k for k in key0.values() if k["part"] == 1 and k["role"] == "target"]
    for k in t1k[:5]:
        key1[_q("topup1|", 1, k["image"], k["class"])] = {**k, "role": "old_repeat"}
    for k in [k for k in list(key1.values()) if k["role"] == "target" and k["part"] == 1][:2]:
        key1[_q("topup1|", 3, k["image"], k["class"])] = {**k, "part": 3, "role": "repeat"}
    lab1 = [json.dumps({"qid": q, "label": str(rng.choice(["Y", "N", "U", "A"], p=[.5, .3, .1, .1]))}) for q in key1]
    ans1 = A.answers(lab1)
    rf = score_e3_core(W, FZ, key0, ans0, key1, ans1)
    hh = {**A.human(key0, ans0, W["syn"])[0], **A.human(key1, ans1, W["syn"])[0]}
    one = np.ones((1, 40))
    ck["E1_equals_P_c_of_pc_ends_fixture"] = all(near(rf["E1"][s][m], 100 * float(A.pc_ends(
        A.counts(W, s, hh), one, np.arange(40))[k][0])) for s in W["se"] for m, k in
        (("P_c", "reg"), ("P_c_lo", "lo"), ("P_c_hi", "hi")))
    s0 = W["se"][0]  # O1 on 40 images: the first 500 rows of default_rng(0).integers(0, n, (2000, n)), recomputed here
    c0 = A.counts(W, s0, hh)
    ib = np.random.default_rng(0).integers(0, 40, (2000, 40))[:500]
    pf = 100 * (c0["pm"] + c0["hy"])[ib].sum(1) / np.maximum((c0["pm"] + c0["am"] + c0["hy"] + c0["hn"])[ib].sum(1), 1e-9)
    ck["E1_ci_Q25_bootstrap_first_500_rows_fixture"] = np.allclose(rf["E1"][s0]["P_c_ci95"],
                                                                   np.nanpercentile(pf, [2.5, 97.5]), rtol=0, atol=1e-9)
    ck["CC359_disclosure_on_7c_rows_only"] = set(rf["added_models"]) == {s for s in W["se"] if "_bb_" in s} and \
        rf["E5"]["bb"]["disclosure"] == D7C and rf["E5"]["aa"]["disclosure"] is None and \
        rf["E1"]["ae3_bb_xm600-short"]["batch"] == "7c"
    # ---- e3-score end to end: refusals, fault rule, one write
    ldir = tmp / "vsps_labels"
    f0, f1 = ldir / "xm600_gold", ldir / "xm600_gold_topup1"
    files = {"labels": f0 / "labels_PI.copy.jsonl", "key": f0 / "key.json", "topup_labels": f1 / "labels_PI.copy.jsonl",
             "topup_key": f1 / "key.json"}
    data = {"labels": "\n".join(lab0) + "\n", "key": json.dumps(key0), "topup_labels": "\n".join(lab1) + "\n",
            "topup_key": json.dumps(key1)}
    A._LABEL_OK.update(str(p) for p in files.values())
    for k, p in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(data[k], encoding="utf-8")
    A._LABEL_OK.clear()
    hs = {k: hashlib.sha256(x.encode("utf-8")).hexdigest() for k, x in data.items()}
    r1p = tmp / "A_CERT_RESULT.json"
    r1p.write_text(json.dumps({"provenance": {"labels_sha256": hs["labels"], "key_sha256": hs["key"]}}), encoding="utf-8")
    logp = tmp / "LOG.md"
    fzh, r1h = A.sha(PF["freeze"]), A.sha(r1p)
    good = [f"x OPS-e3-freeze: FREEZE_E3.json sha256 {fzh}", f"x OPS-a-cert-score: A_CERT_RESULT.json sha256 {r1h}",
            f"x OPS-topup1-pin: key.json {hs['topup_key']}", f"x OPS-topup1-session-end: labels {hs['topup_labels']}"]
    P = {"freeze": PF["freeze"], "result": str(tmp / "out" / "RESULT.json"), "log": str(logp), "part1": str(r1p),
         "part1_n": sum(k["part"] == 1 for k in key0.values())}
    arg = {**{k: str(p) for k, p in files.items()}, "labels_sha": hs["labels"], "topup_labels_sha": hs["topup_labels"]}

    def run(lines=good, **kw):
        logp.write_text("\n".join(lines) + "\n", encoding="utf-8")
        rc, so = quiet(lambda: e3_score({**arg, **kw.get("a", {})}, kw.get("P", P), kw.get("wf", lambda: W)))
        return rc, so, Path(P["result"]).exists()

    nf = (2, "FAULT Fault\n", False)
    ck["x_refuses_without_FREEZE_E3_pin"] = run(good[1:]) == nf
    ck["x_refuses_without_part1_result_pin"] = run([good[0]] + good[2:]) == nf
    r1b = tmp / "A_CERT_RESULT_other.json"  # a part-1 result that read another base copy
    r1b.write_text(json.dumps({"provenance": {"labels_sha256": "0" * 64, "key_sha256": hs["key"]}}), encoding="utf-8")
    ck["x_refuses_base_copy_not_read_by_part1"] = run(
        [good[0], f"x OPS-a-cert-score: A_CERT_RESULT.json sha256 {A.sha(r1b)}"] + good[2:],
        P={**P, "part1": str(r1b)}) == nf
    ck["x_refuses_without_topup_session_end_line"] = run(good[:3]) == nf
    ck["x_refuses_unpinned_topup_key"] = run(good[:2] + good[3:]) == nf
    ck["x_refuses_label_sha_mismatch"] = run(good + ["x topup1 " + "1" * 64], a={"topup_labels_sha": "1" * 64}) == nf
    ck["x_refuses_base_part1_incomplete"] = run(P={**P, "part1_n": P["part1_n"] + 1}) == nf
    ck["x_fault_rule_exception_writes_nothing"] = run(wf=lambda: 1 / 0) == (2, "FAULT ZeroDivisionError\n", False)
    ck["x_refuses_pins_differ_from_freeze"] = run(wf=lambda: {**W, "pins": {}}) == nf
    rc, so, ex = run()
    rt = Path(P["result"]).read_text(encoding="utf-8") if ex else ""
    ck["x_valid_run_writes_once_prints_only_path_and_sha"] = rc == 0 and ex and \
        set(json.loads(so)) == {"wrote", "sha256"} and set(json.loads(rt)) >= {"E1", "E2", "E3", "E4", "E5", "E6"}
    ck["x_refuses_if_result_exists"] = run() == (2, "FAULT Fault\n", True)
    ck["no_caption_text_in_any_output"] = all("SENTINELCAP" not in x for x in (fzt, rt, so, json.dumps(rf, default=float)))
    # ---- custody
    ck["guard_refuses_label_files_anywhere"] = refused(ldir / "x.json") and refused(tmp / "labels_PI.x.jsonl") and \
        refused(tmp / "key.json") and refused(tmp / "practice_PI.jsonl") and refused(tmp / "assignment.json") and \
        refused("/r/.vsps_sealed/a") and not refused(ROOT / A.ASSIGN) and not refused(tmp / "BUILD_TOPUP1.json")
    try:
        open(tmp / "labels_PI.probe.jsonl", "w")
        ck["guard_hook_refuses_open"] = False
    except Fault:
        ck["guard_hook_refuses_open"] = True
    try:
        main(["e3-freeze", "--extra", str(files["labels"])])
        ck["freeze_refuses_a_label_path_argument"] = False
    except Fault:
        ck["freeze_refuses_a_label_path_argument"] = True
    os.rename(ldir, tmp / "lbl_done")  # the guard lets rmtree walk the renamed dir
    shutil.rmtree(tmp)


# ------------------------------------------------------------------------------------------------ main
def main(argv: list) -> int:
    if _audit not in getattr(main, "hooks", ()):
        sys.addaudithook(_audit)
        main.hooks = (_audit,)
    mode = argv[0] if argv else ""
    if mode != "e3-score" and any(refused(x) for x in argv[1:]):
        raise Fault("custody: label path given to a label-free mode")
    if mode == "selftest" and len(argv) == 3 and argv[1] == "--out":
        return selftest(Path(argv[2]))
    if mode == "e3-freeze" and len(argv) >= 3 and argv[1] == "--extra":
        return e3_freeze([Path(x) for x in argv[2:]])
    if mode == "e3-score" and len(argv) == 13 and tuple(argv[1::2]) == SCORE_ARGS:
        return e3_score(dict(zip((x[2:].replace("-", "_") for x in SCORE_ARGS), argv[2::2])))
    raise SystemExit("usage: a_cert_e3.py selftest --out F | e3-freeze --extra F... | e3-score " +
                     " ".join(f"{x} X" for x in SCORE_ARGS))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
