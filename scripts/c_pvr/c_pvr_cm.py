#!/usr/bin/env python3
"""C-M1 and C-M2 of T1-ANALYSIS v1.1 (T1_ANALYSIS_APPENDIX_v1_1.md 59b6eae5, commit f5cc716; CC-292r2 GO 88), the
registered §10 sketch taken over unchanged in logic. The one change of form: every function takes column sums (the
point, shape (k,)) and their bootstrap replicates (shape (B, k)) instead of per-image rows. Image-bootstrap sums are
linear in the rows, so W @ (x - y) = W @ x - W @ y and every number equals the sketch's, while one W (one e2b.boot
call per set) serves every statistic of the file (§6). Binding readings of CC-292r2: Ruling 6 (the §4.4 union drop
is printed with B_eff and is never a FAULT), Ruling 8 (the raw l.400 row: no main-text C-M2 sentence for NOT_RUN,
FAULT or POST_HOC, only the supplement line).

    ~/.venvs/c_pvr/bin/python -I -B scripts/c_pvr/c_pvr_cm.py selftest     synthetic arrays only, reads no data

Label of every number: TIER 1 / DEV-EXPLORE, "dev, in-sample (XM3600-vi)". Bootstrap: prereg §5.5, the e2b.py
boot() form (multinomial image weights), seed 20261102, B = 10,000, rows in sorted image-id order (c_pvr_score.py).
"""
from __future__ import annotations

import hashlib
import itertools
import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SEED, B, ALPHA = 20261102, 10_000, 0.05  # prereg §5.5, §5.2; e2b's own default seed is 20261101, never used here
E2B = {"scripts/vsps_j_e2b/e2b.py": "a952755f3c311f368f9153e786ac322cd819898267d4a4192f64dfd36f113388",
       "scripts/vsps_j_m0/m0.py": "5d3c02f414bd5743d437ec399e07431b4d38d970b16b901c52a9a657505ef7b2"}
DEV = "dev, in-sample (XM3600-vi)"
PAIRS = {"A7-PVR": (1, 2), "A1-A7": (0, 1), "A1-PVR": (0, 2)}  # column order: A1, A7, PVR-drop (§4.2)


class Fault(Exception):
    """§9.1: no C-M1 / C-M2 number; one OPS line by the coordinator; fix under a one-judge read."""


def boot_fn(root: Path = ROOT):
    """e2b.boot (scripts/vsps_j_e2b/e2b.py l.748-754) behind its sha and m0's; e2b's sys.path inserts are undone."""
    for rel, h in E2B.items():
        if hashlib.sha256((root / rel).read_bytes()).hexdigest() != h:
            raise SystemExit(f"FAULT: {rel} differs from its pin {h[:8]}; nothing is imported")
    saved = list(sys.path)
    sys.path.insert(0, str(root / "scripts/vsps_j_e2b"))
    try:
        import e2b
    finally:
        sys.path[:] = saved
    return lambda rows: e2b.boot(rows, len(rows), seed=SEED, B=B)


def pct(v) -> list[float]:
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]


def p2(d) -> float:  # prereg §5.2 two-sided bootstrap p
    return min(1.0, 2 * min(int((d <= 0).sum()), int((d >= 0).sum())) / len(d))


def holm(ps, alpha: float = ALPHA) -> list[bool]:
    order, rej = sorted(range(len(ps)), key=ps.__getitem__), [False] * len(ps)
    for k, j in enumerate(order):
        if ps[j] > alpha / (len(ps) - k):
            break
        rej[j] = True
    return rej


def holds0(ci) -> bool:
    return not (ci[0] > 0 or ci[1] < 0)


def ratios(pt, T, or_ci, g1: bool = True) -> dict:
    """§4.2-§4.3: the three pooled Wald ratios of one sign. pt / T columns: H_A1, H_A7, H_PVR, D_A1, D_A7, D_PVR.
    G1 (PI-1107d) applies to κ⁻(A7−PVR) only and is checked before G2; G2 on every denominator (CC-292 W2)."""
    out = {}
    for name, (a, b) in PAIRS.items():
        num, den = T[:, a] - T[:, b], T[:, 3 + a] - T[:, 3 + b]
        dci, bad = pct(den), den == 0
        gate = None
        if g1 and name == "A7-PVR" and or_ci[0] <= 1 <= or_ci[1]:
            gate = "G1"
        elif holds0(dci) or bad.mean() > 0.01:
            gate = "G2"
        ok = gate is None
        with np.errstate(divide="ignore", invalid="ignore"):
            r = num / den
        assert not (ok and bad.mean() > 0.01)  # prereg §5.5 FAULT; unreachable after G2 (§9.1 item 8)
        pn, pd = float(pt[a] - pt[b]), float(pt[3 + a] - pt[3 + b])
        out[name] = {"label": "IDENTIFIED" if ok else f"NOT_IDENTIFIED ({gate})", "gate": gate, "num": pn,
                     "den": pd, "num_ci": pct(num), "den_ci": dci, "zero_den_share": float(bad.mean()),
                     "kappa": pn / pd if ok else None, "ci": pct(r[~bad]) if ok else None,
                     "dropped": int(bad.sum()), "_rep": r, "_bad": bad}
    return out


def p_check(ps, b_eff: int) -> None:
    if abs(ps[0] - ps[1]) > 1 / b_eff:  # δ₂ = w·δ₁, w > 0 (§4.4); in effect p₁ ≠ p₂ (CC-292 N8)
        raise Fault("over-identification p-values differ (§9.1 item 7)")


def overid(r: dict) -> dict:
    """§4.4 on κ⁻ only. Kept replicates = the complement of the UNION of the three ratios' undefined replicates, one
    set for δ₁ and δ₂; B_eff and the union drop count are printed and never a FAULT (CC-292r2 Ruling 6)."""
    if bad := [k for k in PAIRS if r[k]["gate"]]:
        return {"verdict": "OVERID_NOT_RUN", "failing": [f"{k}: {r[k]['gate']}" for k in bad]}
    keep = ~(r["A7-PVR"]["_bad"] | r["A1-A7"]["_bad"] | r["A1-PVR"]["_bad"])
    d1 = (r["A1-A7"]["_rep"] - r["A7-PVR"]["_rep"])[keep]
    d2 = (r["A1-PVR"]["_rep"] - r["A7-PVR"]["_rep"])[keep]
    ps = [p2(d1), p2(d2)]
    p_check(ps, int(keep.sum()))
    w = r["A1-A7"]["den"] / r["A1-PVR"]["den"]
    return {"verdict": "E1_REJECTED" if any(holm(ps)) else "E1_NOT_REJECTED", "p": ps, "p_holm": min(1.0, 2 * min(ps)),
            "delta": [r["A1-A7"]["kappa"] - r["A7-PVR"]["kappa"], r["A1-PVR"]["kappa"] - r["A7-PVR"]["kappa"]],
            "ci_unadjusted": [pct(d1), pct(d2)], "w": w, "B_eff": int(keep.sum()), "union_dropped": int((~keep).sum())}


def stratum(pn, tn, pd, td) -> dict:
    """§4.5: κ̂⁻(A7−PVR) in one D⁻_A1 stratum, with G2 per stratum and its CI (descriptive, no label)."""
    dci, bad = pct(td), td == 0
    gate = "G2" if holds0(dci) or bad.mean() > 0.01 else None
    with np.errstate(divide="ignore", invalid="ignore"):
        r = tn / td
    return {"num": float(pn), "den": float(pd), "den_ci": dci, "gate": gate, "kappa": None if gate else pn / pd,
            "ci": None if gate else pct(r[~bad]), "dropped": int(bad.sum()), "_rep": r, "_bad": bad}


def strata(get) -> dict:
    out = {k: stratum(*get(f"st{k}:dHm"), *get(f"st{k}:dDm")) for k in ("1", "2", "3")}
    a, b = out["3"], out["1"]
    if not (a["gate"] or b["gate"]):
        keep = ~(a["_bad"] | b["_bad"])
        out["3-1"] = {"diff": a["kappa"] - b["kappa"], "ci": pct((a["_rep"] - b["_rep"])[keep]),
                      "dropped": int((~keep).sum())}
    pn, tn = get("st0:dHm")
    pc, tc = get("st0")
    with np.errstate(divide="ignore", invalid="ignore"):
        m = tn / tc
    ok = np.isfinite(m)
    ci = pct(m[ok]) if ok.any() and pc else None
    out["placebo"] = {"n_images": float(pc), "mean": float(pn / pc) if pc else None, "ci": ci,
                      "dropped": int((~ok).sum()), "label": None if ci is None else
                      "PLACEBO_CONSISTENT" if ci[0] <= 0 <= ci[1] else "PLACEBO_INCONSISTENT"}
    return out


def accounting(s: dict, km: float, kp: float) -> dict:
    """§4.6, printed only when κ⁻ and κ⁺ (A7−PVR) are IDENTIFIED. s: point sums (Hp/Hm of A7 and PVR-drop, the A1
    unit counts Dm|A1 = N_A, Dp|A1 = N_P, the kept counts Dm/Dp of A7 and PVR-drop). Reproduces P(PVR-drop) by
    construction at tier 1; off by more than 1e-9 = FAULT. 'accounting, in-sample, not a test'."""
    na, npr = s["Dm|A1"], s["Dp|A1"]
    rho = {a: 1 - s[f"Dm|{a}"] / na for a in ("A7", "PVR-drop")}
    phi = {a: 1 - s[f"Dp|{a}"] / npr for a in ("A7", "PVR-drop")}
    hp7, hm7, hpv, hmv = s["Hp|A7"], s["Hm|A7"], s["Hp|PVR-drop"], s["Hm|PVR-drop"]
    top = hp7 - kp * npr * (phi["PVR-drop"] - phi["A7"])
    hat = top / (top + hm7 - km * na * (rho["PVR-drop"] - rho["A7"]))
    p7, pv = hp7 / (hp7 + hm7), hpv / (hpv + hmv)
    if abs(hat - pv) > 1e-9:
        raise Fault("§4.6 reproduction off by more than 1e-9 (§9.1 item 7)")
    dm, dp = hp7 / (hp7 + hmv) - p7, hpv / (hpv + hm7) - p7
    return {"label": "accounting, in-sample, not a test", "P_hat": 100 * hat, "P_PVR-drop": 100 * pv, "P_A7": 100 * p7,
            "dP_minus": 100 * dm, "dP_plus": 100 * dp, "remainder": 100 * ((pv - p7) - dm - dp)}


def bounds(t):
    """§5.2 sharp bounds of Δ_all = P_all(PVR) − P_all(A8) from sums (H⁺_P, n_P, H⁺_8, n_8, S_P, S_8, S_b)."""
    kp, np_, k8, n8, sp, s8, sb = (t[..., j] for j in range(7))
    base, c = kp / np_ - k8 / n8, 1 / np_ - 1 / n8
    return base - s8 / n8 + sb * np.minimum(0, c), base + sp / np_ + sb * np.maximum(0, c)


def cm2(pt, T) -> dict:
    lo, hi = bounds(pt)
    blo, bhi = bounds(T)
    band = [float(np.percentile(blo, 2.5)), float(np.percentile(bhi, 97.5))]
    lab = "SIGN_IDENTIFIED_POS" if band[0] > 0 else "SIGN_IDENTIFIED_NEG" if band[1] < 0 else "SIGN_NOT_IDENTIFIED"
    return {"lo": 100 * float(lo), "hi": 100 * float(hi), "band": [100 * band[0], 100 * band[1]], "label": lab}


def per_arm(hp, hm, u, n) -> dict:
    """§5.1 per-arm [L_a, U_a] (L_a = P_obj^VI,wrong) and the §5.3 MA range [P_wrong, P_obj], in points."""
    return {"L": 100 * hp / n, "U": 100 * (hp + u) / n, "P_obj": 100 * hp / (hp + hm), "unknown": float(u),
            "unknown_share": 100 * u / n}


# ---------------------------------------------------------------------------------------------- §8 sentences
K1A = ("On the development set, in the count-matched contrast (PVR-drop vs A7), each additional absent object class "
       "carried by a demonstration (counted once per demonstration) went with {k} additional absent-object mentions "
       "in the captions.")
K1B = (" Under the stated exclusion assumption E1 (including a common copy rate across units), this is the rate at "
       "which absent demonstration objects are copied into captions; an over-identification test against unfiltered "
       "demonstrations did not reject E1 (δ = {d} [unadjusted 95% CI], Holm p = {p}).")
K2B = (" An over-identification test rejected the exclusion assumption E1 (δ = {d} [unadjusted 95% CI], Holm p = {p}): "
       "the contrasts with unfiltered demonstrations imply a different ratio. So either the effect on captions also "
       "runs through a channel other than the count of absent demonstration objects (such as demonstration length or "
       "emptied demonstrations), or the copy rate differs between the units the verifier removes and other units, or "
       "with their number; the test does not separate these, and the ratio is not read as a copy rate.")
K3B = " E1 could not be tested on this set ({gate} not met), so the ratio is reported under E1 untested."
K4 = ("On the development set, filtering (PVR-drop) did not remove absent-object propositions at a rate "
      "distinguishable from count-matched random removal (OR_PVR-drop / OR_A7 = {o}), so this design does not "
      "identify the copy channel and no rate is reported.")
K5 = ("On the development set, the count-matched contrast did not change the number of absent demonstration objects "
      "distinguishably from zero (Σ ΔD⁻ = {s}), so this design does not identify the copy channel and no rate is "
      "reported.")
PLACEBO = (" Among images whose unfiltered demonstrations held no absent-object proposition, the same contrast still "
           "changed absent-object mentions ({m} per image), which E1 rules out.")
M2_SIGN = ("With no assumption about mentions whose status the existing labels leave unknown, all-mention object "
           "precision was {dir} under PVR than under A8 on the development set (sharp bounds [{lo}, {hi}]; 95% band "
           "[{a}, {b}]; unknown share {x}% PVR, {y}% A8).")
M2_NONE = ("With no assumption about mentions whose status the existing labels leave unknown, the sign of the PVR − A8 "
           "difference in all-mention object precision is not identified on the development set (sharp bounds [{lo}, "
           "{hi}]; 95% band [{a}, {b}]); the primary rule excludes those mentions (unknown share {x}% PVR, {y}% A8).")


def f(x, nd: int = 3) -> str:
    return f"{x:.{nd}f}"


def xci(x, ci, nd: int = 3) -> str:
    return f"{f(x, nd)} [{f(ci[0], nd)}, {f(ci[1], nd)}]"


def m1_sentence(r: dict, ov: dict, pl: dict, or_ratio: dict) -> tuple[str, str | None]:
    """§8 C-M1 case K1-K5, chosen mechanically; the placebo clause only on PLACEBO_INCONSISTENT, after K1-K3."""
    m = r["A7-PVR"]
    if m["gate"] == "G1":
        return "K4", K4.format(o=xci(or_ratio["point"], or_ratio["ci"]))
    if m["gate"] == "G2":
        return "K5", K5.format(s=xci(m["den"], m["den_ci"], 0))
    head = K1A.format(k=xci(m["kappa"], m["ci"]))
    d = ov.get("delta") and xci(ov["delta"][0], ov["ci_unadjusted"][0])
    case, tail = {"E1_NOT_REJECTED": ("K1", K1B), "E1_REJECTED": ("K2", K2B), "OVERID_NOT_RUN": ("K3", K3B)}[ov["verdict"]]
    s = head + tail.format(d=d, p=ov.get("p_holm") is not None and f(ov["p_holm"], 4), gate="; ".join(ov.get("failing", [])))
    if pl.get("label") == "PLACEBO_INCONSISTENT":
        s += PLACEBO.format(m=xci(pl["mean"], pl["ci"]))
    return case, s


def m2_sentence(b: dict, xu: float, yu: float) -> str:
    g = {"lo": f(b["lo"], 2), "hi": f(b["hi"], 2), "a": f(b["band"][0], 2), "b": f(b["band"][1], 2), "x": f(xu, 1),
         "y": f(yu, 1)}
    if b["label"] == "SIGN_NOT_IDENTIFIED":
        return M2_NONE.format(**g)
    return M2_SIGN.format(dir="higher" if b["label"] == "SIGN_IDENTIFIED_POS" else "lower", **g)


def strip(d):
    """Drop the replicate arrays before the record is written."""
    if isinstance(d, dict):
        return {k: strip(v) for k, v in d.items() if not k.startswith("_")}
    return d


LABELS = re.compile(r"IDENTIFIED|E1_|OVERID_|SIGN_|PLACEBO_")  # every C-M1 / C-M2 label and verdict (§4.7, §5.4)


def scrub(d):
    """§9.4 (CC-293 W1): a POST_HOC record keeps its numbers, descriptive only, and loses every label, verdict and
    case field at every depth (IDENTIFIED, NOT_IDENTIFIED, E1_*, OVERID_*, SIGN_*, PLACEBO_*, case)."""
    if isinstance(d, dict):
        return {k: scrub(v) for k, v in d.items() if k != "case" and not (isinstance(v, str) and LABELS.search(v))}
    if isinstance(d, list):
        return [scrub(v) for v in d if not (isinstance(v, str) and LABELS.search(v))]
    return d


# ---------------------------------------------------------------------------------------------- orchestration
def analyse(get, or_ratio: dict | None, *, variant: str | None, missing: dict, degraded: bool, inconclusive: bool,
            post_hoc: bool, t1rep_fault: str | None, arms: list[str]) -> dict:
    """Both analyses, after S16 has written every registered decision (§1 order and isolation). get(name) -> (point
    sum, replicate sums). or_ratio = the T1-REP §2 OR_PVR-drop / OR_A7 point and CI as S16 printed it (never
    recomputed here). missing = {arm: missing ids} (§9.2); variant = the §6.3 variant or None (STOP)."""
    res, main, supp = {"label": DEV}, [], []
    # C-M1 (§4)
    try:
        if miss := {a: missing[a] for a in ("A1", "A7", "PVR-drop") if missing.get(a)}:  # §9.2 before §9.1 item 9
            res["C-M1"] = {"label": "NOT_RUN", "missing": miss}
        elif t1rep_fault:
            raise Fault(f"T1-REP §1/§2 is a FAULT ({t1rep_fault}); §9.1 item 9")
        else:
            cols = lambda s: tuple(np.array(x) for x in zip(*(get(f"{s}|{a}") for a in ("A1", "A7", "PVR-drop"))))
            (hm, thm), (dm, tdm), (hp, thp), (dp, tdp) = cols("Hm"), cols("Dm"), cols("Hp"), cols("Dp")
            minus = ratios(np.r_[hm, dm], np.c_[thm.T, tdm.T], or_ratio["ci"])
            plus = ratios(np.r_[hp, dp], np.c_[thp.T, tdp.T], None, g1=False)  # κ⁺: supplement; G1 is κ⁻'s gate
            ov = overid(minus)
            st = strata(get)
            m1 = {"kappa_minus": minus, "kappa_plus": plus, "overid": ov, "strata": st}
            if not (minus["A7-PVR"]["gate"] or plus["A7-PVR"]["gate"]):
                s = {k: get(k)[0] for k in ("Dm|A1", "Dp|A1", "Hp|A7", "Hm|A7", "Hp|PVR-drop", "Hm|PVR-drop",
                                            "Dm|A7", "Dp|A7", "Dm|PVR-drop", "Dp|PVR-drop")}
                m1["accounting"] = accounting(s, minus["A7-PVR"]["kappa"], plus["A7-PVR"]["kappa"])
            case, sent = m1_sentence(minus, ov, st["placebo"], or_ratio)
            m1.update(label=minus["A7-PVR"]["label"], verdict=ov["verdict"], placebo=st["placebo"]["label"], case=case)
            main.append({"id": "M1-M3", "case": case, "label": DEV, "sentence": sent})
            res["C-M1"] = m1
    except Fault as e:
        res["C-M1"] = {"label": "FAULT", "reason": str(e)}
    # C-M2 (§5); PVR = the §6.3 variant, PVR-drop if §6.3 STOPs (set by this appendix, §5.1); both in the supplement
    pvr = variant or "PVR-drop"
    try:
        if miss := {a: missing[a] for a in (pvr, "A8") if missing.get(a)}:
            res["C-M2"] = {"label": "NOT_RUN", "missing": miss}
        else:
            m2 = {"pvr": pvr, "fallback": variant is None, "variants": {}, "per_arm": {}}
            for v in ("PVR-drop", "PVR-keep"):
                if missing.get(v) or missing.get("A8"):
                    continue
                pt, T = (np.array(x) for x in zip(*(get(k) for k in (f"Hp|{v}", f"n|{v}", "Hp|A8", "n|A8", f"SP|{v}",
                                                                     f"S8|{v}", f"Sb|{v}"))))
                m2["variants"][v] = {**cm2(pt, T.T)}
            for a in arms:
                hp, hm, u, n = (get(f"{k}|{a}")[0] for k in ("Hp", "Hm", "U", "n"))
                m2["per_arm"][a] = per_arm(hp, hm, u, n)
            sel, pa, p8 = m2["variants"][pvr], m2["per_arm"][pvr], m2["per_arm"]["A8"]
            m2["per_arm_combination"] = [pa["L"] - p8["U"], pa["U"] - p8["L"]]  # valid, not sharp (§5.2)
            m2["MA_outer"] = [pa["L"] - p8["P_obj"], pa["P_obj"] - p8["L"]]  # under MA only (§5.3), no sign label
            tags = [t for t, on in (("DEGRADED", degraded), ("INCONCLUSIVE", inconclusive)) if on]
            m2["label"] = " ".join([sel["label"], *tags])
            main.append({"id": "M4", "label": DEV, "usable_as_claim": not tags,
                         "sentence": m2_sentence(sel, pa["unknown_share"], p8["unknown_share"])})
            res["C-M2"] = m2
    except Fault as e:
        res["C-M2"] = {"label": "FAULT", "reason": str(e)}
    if post_hoc:  # §9.4: no main-text sentence; the numbers stay, every label goes
        main = []
        for k in ("C-M1", "C-M2"):
            if res[k]["label"] not in ("NOT_RUN", "FAULT"):
                res[k] = {**scrub(strip(res[k])), "label": "POST_HOC",
                          "reason": "§9.4: descriptive numbers in cm_tier1.json, no label, no sentence"}  # CC-293r2 N-F
    for k in ("C-M1", "C-M2"):  # §8 l.391 / l.400 (CC-292r2 Ruling 8): the supplement line
        if res[k]["label"] in ("NOT_RUN", "FAULT", "POST_HOC"):
            supp.append(f"{k} not computed: {res[k]['label']} {res[k].get('reason', res[k].get('missing', '§9.4'))}")
    return strip({**res, "main_text": main, "supplement_lines": supp})


# ---------------------------------------------------------------------------------------------- selftest
def _getter(rows: dict, boot):
    """Synthetic {name: per-image column} -> get(name) through one boot call (one W, as in the scorer)."""
    names = list(rows)
    R = np.column_stack([np.asarray(rows[k], float) for k in names])
    T = boot(R)
    idx = {k: j for j, k in enumerate(names)}
    return lambda k: (R[:, idx[k]].sum(), T[:, idx[k]])


def _world(hm, dm, hp=None, dp=None):
    """C-M1 columns for arms A1, A7, PVR-drop plus the strata columns (§4.5) from D⁻_A1."""
    z = np.zeros_like(dm[0])
    hp, dp = hp or [z, z, z], dp or [z, z, z]
    rows = {f"{s}|{a}": v for s, vs in (("Hm", hm), ("Dm", dm), ("Hp", hp), ("Dp", dp))
            for a, v in zip(("A1", "A7", "PVR-drop"), vs)}
    d0 = np.asarray(dm[0])
    for k, sel in (("0", d0 == 0), ("1", d0 == 1), ("2", d0 == 2), ("3", d0 >= 3)):
        rows[f"st{k}"] = sel.astype(float)
        rows[f"st{k}:dHm"] = (np.asarray(hm[1]) - np.asarray(hm[2])) * sel
        rows[f"st{k}:dDm"] = (np.asarray(dm[1]) - np.asarray(dm[2])) * sel
    return rows


def _m1(rows, boot, or_ci):
    get = _getter(rows, boot)
    cols = lambda s: tuple(np.array(x) for x in zip(*(get(f"{s}|{a}") for a in ("A1", "A7", "PVR-drop"))))
    (h, th), (d, td) = cols("Hm"), cols("Dm")
    r = ratios(np.r_[h, d], np.c_[th.T, td.T], or_ci)
    return r, overid(r), get


def selftest(root: Path = ROOT) -> None:
    boot = boot_fn(root)
    g = np.random.default_rng(7)
    n = 400
    d1 = g.integers(0, 5, n)
    dpvr, d7 = d1 - np.minimum(d1, g.integers(0, 3, n)), d1 - np.minimum(d1, g.integers(0, 2, n))
    flags = [g.random(k) < 0.4 for k in d1]  # E1 true: each kept absent unit copied w.p. 0.4
    base = g.poisson(0.3, n)  # arm-invariant b_i
    copy = lambda dd, b0=base: [b0 + np.array([fl[:k].sum() for fl, k in zip(flags, x)]) for x in dd]
    h = copy((d1, d7, dpvr))
    z = np.zeros(3600, int)  # CC-292 W2 case: n 3,600, 400 images at 2, PVR one lower in 4
    z[:400] = 2
    zp = z.copy()
    zp[:4] -= 1
    hz = np.zeros(3600, int)
    u1 = np.zeros(n, int)  # CC-292r2 W1 case: two 5-image denominators, each <= 1 % zero, union > 1 %
    u1[:10] = 1
    u7 = np.zeros(n, int)
    u7[:5] = 1
    hu = [base + u1, base + u7, base]
    res = {}

    def case(name, fn):
        try:
            good = fn()
        except Exception as e:  # a crash inside a named case is that case's failure
            good = f"{type(e).__name__}: {e}"
        if good is not True:
            raise SystemExit(f"selftest FAILED: {name} ({good})")

    def e1_true():
        r, ov, _ = _m1(_world(h, [d1, d7, dpvr]), boot, (0.6, 0.9))
        res["e1"] = ov["verdict"]
        return (r["A7-PVR"]["label"] == "IDENTIFIED" and abs(r["A7-PVR"]["kappa"] - 0.4) < 0.2 and ov["B_eff"] == B
                and ov["p_holm"] == min(1.0, 2 * min(ov["p"])) and ov["union_dropped"] == 0)

    def g1_fires():
        r, ov, _ = _m1(_world(h, [d1, d7, dpvr]), boot, (0.8, 1.1))
        edge = _m1(_world(h, [d1, d7, dpvr]), boot, (1.0, 1.3))[0]["A7-PVR"]["gate"]  # "contains 1": closed interval
        above = _m1(_world(h, [d1, d7, dpvr]), boot, (1.1, 1.3))[0]["A7-PVR"]["gate"]  # wholly above 1: no G1
        return (r["A7-PVR"]["gate"] == "G1" and ov["verdict"] == "OVERID_NOT_RUN" and r["A1-A7"]["gate"] is None
                and edge == "G1" and above is None)

    def length_channel():
        hl = [h[0] + g.poisson(1.0, n), h[1], h[2]]  # a length channel only A1 has
        return _m1(_world(hl, [d1, d7, dpvr]), boot, (0.6, 0.9))[1]["verdict"] == "E1_REJECTED"

    def drops_counted():
        d7s = d1.copy()
        d7s[np.flatnonzero(d1 > 0)[:5]] -= 1  # A1-A7 moves D in 5 images only
        r, ov, _ = _m1(_world(copy((d1, d7s, dpvr)), [d1, d7s, dpvr]), boot, (0.6, 0.9))
        return r["A1-A7"]["dropped"] > 0 and ov["B_eff"] < B and ov["union_dropped"] == B - ov["B_eff"]

    def w2_case():
        r, ov, _ = _m1(_world([hz, hz, hz], [z, z, zp]), boot, (0.6, 0.9))
        m = r["A7-PVR"]
        res["w2"] = (m["den_ci"], round(m["zero_den_share"], 4))
        k5 = m1_sentence(r, ov, {}, {"point": 0.7, "ci": [0.6, 0.9]})[0]
        return (m["gate"] == "G2" and m["den_ci"] == [1.0, 8.0] and round(m["zero_den_share"], 4) == 0.0182 and m["dropped"] == 182
                and ov["verdict"] == "OVERID_NOT_RUN" and m["kappa"] is None and k5 == "K5")  # CC-292 W2 numbers

    def w2_then_g1():
        return _m1(_world([hz, hz, hz], [z, z, zp]), boot, (0.8, 1.1))[0]["A7-PVR"]["gate"] == "G1"

    def union_drop():
        r, ov, _ = _m1(_world(hu, [u1, u7, np.zeros(n, int)]), boot, (0.6, 0.9))
        each = max(r[k]["zero_den_share"] for k in PAIRS)
        res["union"] = (ov.get("B_eff"), ov.get("union_dropped"))
        return ov["verdict"] != "OVERID_NOT_RUN" and each <= 0.01 and ov["union_dropped"] / B > 0.01

    def p_rule():
        try:
            p_check([0.04, 0.05], 10_000)
        except Fault:
            p_check([0.04, 0.04 + 0.5 / 10_000], 10_000)
            return True
        return False

    def identity_200():
        bad = 0
        for s in range(200):
            gg = np.random.default_rng(1000 + s)
            a1 = gg.integers(0, 5, 300)
            a7, pv = a1 - np.minimum(a1, gg.integers(0, 2, 300)), a1 - np.minimum(a1, gg.integers(0, 3, 300))
            hh = [gg.poisson(0.5, 300) + x for x in (a1, a7, pv)]
            R = np.column_stack([*hh, a1, a7, pv]).astype(float)
            W = np.random.default_rng(s).multinomial(300, [1 / 300] * 300, size=200)
            r = ratios(R.sum(0), W @ R, (0.5, 0.9))
            if all(r[k]["gate"] is None for k in PAIRS):
                keep = ~(r["A7-PVR"]["_bad"] | r["A1-A7"]["_bad"] | r["A1-PVR"]["_bad"])
                d1_, d2_ = ((r[k]["_rep"] - r["A7-PVR"]["_rep"])[keep] for k in ("A1-A7", "A1-PVR"))
                bad += p2(d1_) != p2(d2_)
        return bad == 0

    def strata_placebo():
        _, _, get = _m1(_world(h, [d1, d7, dpvr]), boot, (0.6, 0.9))
        st = strata(get)
        hx = [h[0], h[1] + (d1 == 0), h[2]]  # A7 alone adds an absent mention where no absent unit exists
        st2 = strata(_m1(_world(hx, [d1, d7, dpvr]), boot, (0.6, 0.9))[2])
        return (st["placebo"]["label"] == "PLACEBO_CONSISTENT" and st2["placebo"]["label"] == "PLACEBO_INCONSISTENT"
                and st["1"]["gate"] == "G2" and st["1"]["kappa"] is None and st["3"]["gate"] is None
                and abs(st["3"]["kappa"] - 0.4) < 0.2 and "3-1" not in st)  # stratum 1 is weak by construction here

    def accounting_exact():
        s = {"Dm|A1": 50.0, "Dp|A1": 80.0, "Dm|A7": 40.0, "Dm|PVR-drop": 30.0, "Dp|A7": 70.0, "Dp|PVR-drop": 66.0,
             "Hp|A7": 120.0, "Hm|A7": 45.0, "Hp|PVR-drop": 117.0, "Hm|PVR-drop": 41.0}
        km, kp = (45 - 41) / (40 - 30), (120 - 117) / (70 - 66)
        a = accounting(s, km, kp)
        try:
            accounting(s, km + 0.1, kp)
        except Fault:
            return abs(a["P_hat"] - a["P_PVR-drop"]) < 1e-7 and abs(a["remainder"] + a["dP_minus"] + a["dP_plus"]
                                                                   - (a["P_PVR-drop"] - a["P_A7"])) < 1e-9
        return False

    def bounds_brute():
        gg = np.random.default_rng(3)
        for _ in range(300):
            nu = gg.integers(1, 6)
            inP, in8 = gg.random(nu) < 0.6, gg.random(nu) < 0.6
            kp, k8 = gg.integers(0, 5, 2)
            nP, n8 = kp + inP.sum() + gg.integers(1, 4), k8 + in8.sum() + gg.integers(1, 4)
            vals = [(kp + (x * inP).sum()) / nP - (k8 + (x * in8).sum()) / n8
                    for x in map(np.array, itertools.product((0, 1), repeat=nu))]
            t = np.array([kp, nP, k8, n8, (inP & ~in8).sum(), (in8 & ~inP).sum(), (inP & in8).sum()], float)
            lo, hi = bounds(t)
            if abs(lo - min(vals)) > 1e-12 or abs(hi - max(vals)) > 1e-12 or not lo <= hi:
                return False
            if not (kp / nP - (k8 + in8.sum()) / n8 <= lo + 1e-12 and hi <= (kp + inP.sum()) / nP - k8 / n8 + 1e-12):
                return False  # the per-arm combination is never narrower (§10)
        return True

    def cm2_labels():
        m = np.column_stack([g.integers(1, 4, n), np.full(n, 6), g.integers(1, 4, n), np.full(n, 6),
                             g.integers(0, 2, n), g.integers(0, 2, n), g.integers(0, 2, n)]).astype(float)
        b = cm2(m.sum(0), boot(m))
        hi_ = np.column_stack([np.full(n, 5), np.full(n, 6), np.full(n, 1), np.full(n, 6), np.zeros(n), np.zeros(n),
                               np.zeros(n)]).astype(float)
        pos = cm2(hi_.sum(0), boot(hi_))
        neg = cm2(hi_[:, [2, 3, 0, 1, 4, 5, 6]].sum(0), boot(hi_[:, [2, 3, 0, 1, 4, 5, 6]]))
        return (b["lo"] <= b["hi"] and b["band"][0] <= b["lo"] and b["hi"] <= b["band"][1]
                and pos["label"] == "SIGN_IDENTIFIED_POS" and neg["label"] == "SIGN_IDENTIFIED_NEG")

    def holds0_closed():  # CC-293 N1: integer sums make an endpoint of exactly 0 reachable
        return holds0([0.0, 5.0]) and holds0([-3.0, 0.0]) and holds0([-1.0, 1.0]) and not holds0([0.5, 2.0]) \
            and not holds0([-2.0, -0.5])

    def strata_zero_clause():  # 4 images carry the stratum denominator: CI excludes 0, but > 1 % zero replicates
        dd = np.zeros(n)
        dd[:4] = 1
        rows = {"x": dd, "y": dd * 2}
        gt = _getter(rows, boot)
        s = stratum(*gt("y"), *gt("x"))
        return s["den_ci"][0] > 0 and s["gate"] == "G2" and s["kappa"] is None

    def holm_rule():
        return holm([0.01, 0.04]) == [True, True] and holm([0.03, 0.03]) == [False, False] and holm([0.02, 0.2]) == [True, False]

    def p2_form():
        return p2(np.array([-1.0, 1, 2, 3])) == 0.5 and p2(np.array([0.0, 1, 2, 3])) == 0.5 and p2(np.ones(4)) == 0.0

    def analyse_branches():
        rows = _world(h, [d1, d7, dpvr], [h[0] + 3, h[1] + 3, h[2] + 3], [d1 + 4, d7 + 4, dpvr + 4])
        for v in ("PVR-drop", "PVR-keep"):
            rows.update({f"Hp|{v}": np.full(n, 3), f"n|{v}": np.full(n, 6), f"SP|{v}": g.integers(0, 2, n),
                         f"S8|{v}": g.integers(0, 2, n), f"Sb|{v}": g.integers(0, 2, n)})
        rows.update({"Hp|A8": np.full(n, 2), "n|A8": np.full(n, 6)})
        for a in ("PVR-drop", "PVR-keep", "A8"):
            rows.update({f"Hm|{a}": np.full(n, 1), f"U|{a}": np.full(n, 2)})
        get = _getter(rows, boot)
        orr = {"point": 0.7, "ci": [0.6, 0.9]}
        kw = dict(variant="PVR-keep", missing={}, degraded=False, inconclusive=False, post_hoc=False,
                  t1rep_fault=None, arms=["PVR-drop", "PVR-keep", "A8"])
        ok = analyse(get, orr, **kw)
        k4 = analyse(get, {"point": 1.0, "ci": [0.8, 1.1]}, **kw)
        nr = analyse(get, orr, **{**kw, "missing": {"A7": 12}})
        ph = analyse(get, orr, **{**kw, "post_hoc": True, "degraded": True})
        ph_text = json.dumps(ph, ensure_ascii=False)
        oracle = re.compile(r'IDENTIFIED|E1_|OVERID_|SIGN_|PLACEBO_|"K[1-5]"|INCONCLUSIVE|DEGRADED')  # not LABELS (N-A)
        res["post_hoc_clean"] = not oracle.search(ph_text) and '"case"' not in ph_text  # CC-293 W1
        fl = analyse(get, orr, **{**kw, "t1rep_fault": "c' mismatch", "degraded": True, "variant": None})
        both = analyse(get, orr, **{**kw, "t1rep_fault": "c' mismatch", "missing": {"PVR-drop": 3}})
        return (ok["C-M1"]["case"] in ("K1", "K2") and "accounting" in ok["C-M1"] and ok["C-M2"]["pvr"] == "PVR-keep"
                and len(ok["main_text"]) == 2 and not ok["supplement_lines"]
                and "filtering (PVR-drop)" in k4["main_text"][0]["sentence"] and k4["C-M1"]["case"] == "K4"
                and nr["C-M1"]["label"] == "NOT_RUN" and nr["supplement_lines"][0].startswith("C-M1 not computed: NOT_RUN")
                and ph["C-M1"]["label"] == "POST_HOC" and ph["C-M2"]["label"] == "POST_HOC" and not ph["main_text"]
                and len(ph["supplement_lines"]) == 2 and res["post_hoc_clean"] and "kappa_minus" in ph["C-M1"]
                and ph["supplement_lines"][0].endswith("POST_HOC §9.4: descriptive numbers in cm_tier1.json, no label, no sentence")
                and LABELS.search(json.dumps(ok)) and fl["C-M1"]["label"] == "FAULT"
                and fl["C-M2"]["pvr"] == "PVR-drop" and fl["C-M2"]["fallback"] and fl["C-M2"]["label"].endswith("DEGRADED")
                and fl["main_text"][0]["usable_as_claim"] is False and both["C-M1"]["label"] == "NOT_RUN"
                and k4["C-M1"]["kappa_plus"]["A7-PVR"]["gate"] != "G1")  # G1 is κ⁻'s gate only

    for name, fn in (("e1_true_identified", e1_true), ("g1_before_g2", g1_fires), ("length_channel_rejects", length_channel),
                     ("drops_counted", drops_counted), ("w2_case_g2_no_fault", w2_case), ("w2_case_g1", w2_then_g1),
                     ("union_drop_not_fault", union_drop), ("p_equality_rule", p_rule), ("identity_200", identity_200),
                     ("strata_placebo", strata_placebo), ("accounting_exact", accounting_exact),
                     ("bounds_brute_300", bounds_brute), ("cm2_labels", cm2_labels), ("holm_rule", holm_rule),
                     ("p2_form", p2_form), ("holds0_closed", holds0_closed), ("strata_zero_clause", strata_zero_clause),
                     ("analyse_branches", analyse_branches)):
        case(name, fn)
    print("c_pvr_cm selftest ok", res["e1"], res["w2"], f"union B_eff {res['union'][0]} dropped {res['union'][1]}")


if __name__ == "__main__":
    if sys.argv[1:] != ["selftest"]:
        raise SystemExit(__doc__)
    selftest()
