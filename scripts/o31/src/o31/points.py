"""ERRATUM_O31_4 E4-1 to E4-3 (CODE_NEEDS C06): OP_25, OP_75 and the five points, a pure function of P1's k0.json;
the E4-5 edge row; and the guard that E-B3's trainer and decoders call (CC-526 N9).

Read from P1's k0.json only (E4-1): `"complete": true` and a `decision` that is not null, all 30 grid points in
ERRATUM_O31_1 E7 order. Values are the IEEE-754 doubles json.loads returns; t25 = a + 0.25 * (b - a) and
t75 = a + 0.75 * (b - a) in that order; distances |R - t| in the same arithmetic.
E4-2: K0 FAIL -> NOT RUN. Eligible = all 30 points except those whose sft_sha256 equals S1's, OP*'s or OP_mid's;
OP_25 = smallest |R - t25|, ties to the higher P, then the earlier grid point; OP_25's sha is then excluded and OP_75
is picked the same way for t75; no eligible point at either step -> NOT_IDENTIFIED.
E4-3: the five points OP_strict (= S1), OP_25, OP_mid, OP_75, OP* in ascending R, equal R in that label order; an
adjacent difference < 1.0 percentage point -> NOT_IDENTIFIED; else IDENTIFIED.
gate.py, k0.py and run_k0 are not changed: this module only reads their output.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from . import verify

GAP = 1.0  # E4-3
LABELS = ("OP_strict", "OP_25", "OP_mid", "OP_75", "OP*")  # E4-3 label order
EDGE_TAU_ACC, EDGE_TAU_REJ = (0.50, 0.90), (0.10, 0.30)  # E4-5
SCHEMA = "o31.ops5.v1"


def check_p1(k0: dict) -> None:
    """E4-1: only P1's k0.json, the file that carries the K0 verdict, with the 30 points in E7 grid order."""
    if k0.get("complete") is not True or k0.get("decision") is None:
        raise SystemExit("REFUSED not P1's k0.json: complete must be true and decision not null (a preview has no verdict)")
    if [p.get("op") for p in k0.get("points", [])] != [[a, r, list(f)] for a, r, f in verify.grid()]:
        raise SystemExit("REFUSED points are not the 30 grid points in ERRATUM_O31_1 E7 order")


def _entry(p: dict, idx: int | None) -> dict:
    return {"grid_index": idx, "op": p.get("op"), "store": p.get("store"), "R": p["R"], "P": p["P"],
            "sft_sha256": p["sft_sha256"]}


def extra_points(k0: dict) -> dict:
    """{result, reason, t25, t75, op_25, op_75, five, order_by_label, order_by_R, gaps}."""
    check_p1(k0)
    d, s1, pts = k0["decision"], k0["s1"], k0["points"]
    out = {"result": None, "reason": None, "t25": None, "t75": None, "op_25": None, "op_75": None, "five": None,
           "order_by_label": list(LABELS), "order_by_R": None, "gaps": None}
    if not d["pass"]:
        return {**out, "result": "NOT RUN", "reason": "K0 FAIL (E4-2 step 1)"}
    a, b = s1["R"], d["op_star"]["R"]
    t25 = a + 0.25 * (b - a)
    t75 = a + 0.75 * (b - a)
    out.update(t25=t25, t75=t75)
    excl = {s1["sft_sha256"], d["op_star"]["sft_sha256"], d["op_mid"]["sft_sha256"]}
    picks = {}
    for name, t in (("OP_25", t25), ("OP_75", t75)):
        el = [(i, p) for i, p in enumerate(pts) if p["sft_sha256"] not in excl]
        if not el:
            step = 4 if name == "OP_25" else 5
            return {**out, "result": "NOT_IDENTIFIED", "reason": f"no eligible point for {name} (E4-2 step {step})",
                    "op_25": _entry(picks["OP_25"][1], picks["OP_25"][0]) if "OP_25" in picks else None}
        i, p = min(el, key=lambda ip: (abs(ip[1]["R"] - t), -ip[1]["P"], ip[0]))
        picks[name] = (i, p)
        excl.add(p["sft_sha256"])
    five = [("OP_strict", _entry(s1, None)), ("OP_25", _entry(picks["OP_25"][1], picks["OP_25"][0])),
            ("OP_mid", _entry(d["op_mid"], pts.index(d["op_mid"]))), ("OP_75", _entry(picks["OP_75"][1], picks["OP_75"][0])),
            ("OP*", _entry(d["op_star"], pts.index(d["op_star"])))]
    by_r = sorted(five, key=lambda lp: lp[1]["R"])  # stable sort: equal R keep the label order (E4-3)
    gaps = [y[1]["R"] - x[1]["R"] for x, y in zip(by_r, by_r[1:])]
    small = [g for g in gaps if g < GAP]
    return {**out, "result": "NOT_IDENTIFIED" if small else "IDENTIFIED",
            "reason": f"adjacent R difference < {GAP} (E4-3)" if small else "E4-3",
            "op_25": five[1][1], "op_75": five[3][1], "five": dict(five), "order_by_R": [lab for lab, _ in by_r],
            "five_in_label_order": [{"label": lab, **e} for lab, e in five],
            "five_in_R_order": [{"label": lab, **e} for lab, e in by_r], "gaps": gaps}


def edge_row(k0: dict) -> dict:
    """E4-5 (descriptive): OP* at the edge iff tau_acc in {0.50, 0.90} or tau_rej in {0.10, 0.30}; from P1's k0.json."""
    check_p1(k0)
    star = k0["decision"].get("op_star")
    if star is None:
        return {"op_star": None, "edge": None, "reason": "no OP* (no feasible point)"}
    tau_acc, tau_rej, _fams = star["op"]
    return {"op_star": star["op"], "edge": tau_acc in EDGE_TAU_ACC or tau_rej in EDGE_TAU_REJ,
            "tau_acc_at_edge": tau_acc in EDGE_TAU_ACC, "tau_rej_at_edge": tau_rej in EDGE_TAU_REJ}


def require_identified(ops5_path: Path, label: str, store_sft: Path) -> dict:
    """CC-526 N9 (E-B3, E5): a trainer or decoder of the OP_25 / OP_75 student refuses unless ops5.json equals its
    .sha256 line, says IDENTIFIED, and the store's sft.jsonl sha256 equals that point's sft_sha256."""
    if label not in ("OP_25", "OP_75"):
        raise SystemExit(f"REFUSED {label!r} is not an E-B3 extra point")
    ops5_path = Path(ops5_path)
    sha = hashlib.sha256(ops5_path.read_bytes()).hexdigest()
    side = Path(str(ops5_path) + ".sha256")
    line = side.read_text().split() if side.exists() else []
    if not line or line[0] != sha:
        raise SystemExit("REFUSED ops5.json differs from its recorded sha256")
    rec = json.loads(ops5_path.read_text(encoding="utf-8"))
    if rec.get("schema") != SCHEMA or rec.get("result") != "IDENTIFIED":
        raise SystemExit(f"REFUSED ops5.json result is {rec.get('result')!r}, not IDENTIFIED (ERRATUM_O31_4 E4-4)")
    if hashlib.sha256(Path(store_sft).read_bytes()).hexdigest() != rec["five"][label]["sft_sha256"]:
        raise SystemExit(f"REFUSED the store is not the {label} store that ops5.json names (E5)")
    return {"ops5_sha256": sha, "label": label, "sft_sha256": rec["five"][label]["sft_sha256"]}
