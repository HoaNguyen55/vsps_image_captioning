"""T-4 in the form of ERRATUM_O31_4 E4-7 (CODE_NEEDS C24). Reads ops5.json and tier-2 outputs only.

- The five points in ops5.json's R order (`order_by_R`, E4-3); for k = 1..4, Delta_k = R(point k+1) - R(point k), with
  R the §5 object recall (100 * sum TP / sum |G|) of the seed-42 student at that point on the tier-2 list (E11 gold).
- V_k = the variance of Delta_k over the B = 10,000 shared replicates: the §6.3 / E9 paired image bootstrap, i.e. the
  index matrix of metrics.index_chunks with metrics.B_MAIN and metrics.SEED_MAIN.
- sigma2_seed = mean of the sample variances (ddof 1) of S1's three and S2's three tier-2 per-seed R values.
- z_k = Delta_k / sqrt(V_k + 2 sigma2_seed); p_k = 1 - Phi(z_k); p = max_k p_k (intersection-union).
- A zero denominator at any k -> NOT_IDENTIFIED with p = 1 (CC-526 N9).
- ops5.json NOT RUN or NOT_IDENTIFIED -> that label and p = 1, without reading any decode (E4-7).
Open in the text (OPEN.txt): the ddof of V_k and how an undefined replicate enters V_k. Both fail closed here: V_k is
computed only with an explicitly given ddof, and any undefined replicate refuses the computation.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from . import metrics, points

NOT_RUN, NOT_IDENTIFIED, COMPUTED = "NOT RUN", "NOT_IDENTIFIED", "COMPUTED"
STUDENT = {"OP_strict": "S1", "OP_25": "OP_25", "OP_mid": "A-1", "OP_75": "OP_75", "OP*": "S2"}  # seed-42 students (E-B3)


def phi(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def load_ops5(path: Path) -> dict:
    """ops5.json only (E4-7 what reads what): its sha line must match; a k0.json is refused."""
    import hashlib

    path = Path(path)
    rec = json.loads(path.read_text(encoding="utf-8"))
    if rec.get("schema") != points.SCHEMA or "points" in rec or "decision" in rec:
        raise SystemExit("REFUSED T-4 reads ops5.json only, never a k0.json")
    side = Path(str(path) + ".sha256")
    line = side.read_text().split() if side.exists() else []
    if not line or line[0] != hashlib.sha256(path.read_bytes()).hexdigest():
        raise SystemExit("REFUSED ops5.json differs from its recorded sha256")
    return rec


def sigma2_seed(r_s1: list[float], r_s2: list[float]) -> float:
    """Pooled between-seed variance: mean of the two sample variances (n - 1 in the denominator)."""
    if len(r_s1) != 3 or len(r_s2) != 3:
        raise SystemExit("REFUSED sigma2_seed needs the three tier-2 per-seed R of S1 and of S2")
    return float(np.mean([np.var(r_s1, ddof=1), np.var(r_s2, ddof=1)]))


def t4(ops5: dict, load_columns, r_s1: list[float], r_s2: list[float], vk_ddof: int | None = None,
       b: int = metrics.B_MAIN, seed: int = metrics.SEED_MAIN) -> dict:
    """load_columns() -> {"g": |G| per tier-2 image, "tp": {student: TP per image}}, called only if ops5 is IDENTIFIED."""
    if ops5.get("result") != "IDENTIFIED":
        return {"label": ops5.get("result"), "p": 1.0, "reason": "ops5.json result (E4-7)"}
    if vk_ddof is None:
        raise SystemExit("REFUSED the ddof of V_k is not fixed by ERRATUM_O31_4 E4-7 (OPEN.txt)")
    order = ops5["order_by_R"]
    cols = load_columns()
    g = np.asarray(cols["g"], float)
    tp = [np.asarray(cols["tp"][STUDENT[lab]], float) for lab in order]
    point_r = [100 * t.sum() / g.sum() for t in tp]
    delta = [point_r[k + 1] - point_r[k] for k in range(4)]
    reps = [[] for _ in range(4)]
    for idx in metrics.index_chunks(len(g), b, seed):
        gs = g[idx].sum(axis=1)
        if np.any(gs == 0):
            raise SystemExit("REFUSED an undefined replicate (sum |G| = 0); its handling in V_k is OPEN")
        r = [100 * t[idx].sum(axis=1) / gs for t in tp]
        for k in range(4):
            reps[k].append(r[k + 1] - r[k])
    v = [float(np.var(np.concatenate(x), ddof=vk_ddof)) for x in reps]
    s2 = sigma2_seed(r_s1, r_s2)
    den = [vk + 2 * s2 for vk in v]
    base = {"order_by_R": order, "R": point_r, "Delta": delta, "V": v, "sigma2_seed": s2, "vk_ddof": vk_ddof}
    if any(x == 0 for x in den):
        return {**base, "label": NOT_IDENTIFIED, "p": 1.0, "reason": "zero denominator at some k (E4-7)"}
    z = [dk / math.sqrt(x) for dk, x in zip(delta, den)]
    pk = [1.0 - phi(zk) for zk in z]
    return {**base, "z": z, "p_k": pk, "p": max(pk), "label": COMPUTED, "reason": "E4-7"}
