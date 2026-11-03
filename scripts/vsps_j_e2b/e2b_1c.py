#!/usr/bin/env python
"""VSPS-J E2b tier 1c, O1 screen (manuscript/prereg/2026-11-01_vsps_j_e2b_tier1/TIER1C_O1_AMENDMENT_DRAFT.md,
1895dad7; CC-233 O1-C1..C9, CC-233r2). One post-hoc config `internvl3_8b|FA|1c`, one read of the select half, laptop
CPU, 0 GPU-h, 1 h wall cap, its own once-guard. A SCREEN GO licenses nothing on a GPU.

    <m0 venv> -I scripts/vsps_j_e2b/e2b_1c.py screen-1c --runs O --m0-probes P --res R.json --probes-sha S \
                  [--data D] [--copy-to C]                                          laptop, once
    <any venv with numpy> -I scripts/vsps_j_e2b/e2b_1c.py selftest                  CPU, network blocked

K-numbers are the amendment's §9 items: K1 lives in e2b.py (ci_from_table); K2-K6 are here.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import e2b  # noqa: E402  tier-1 rules, unchanged except the K1 split of paired_ci
import m0  # noqa: E402

LABEL_1C = "TIER 1c / DEV-EXPLORE (POST HOC)"
CONFIG = "internvl3_8b|FA|1c"
WINNER, WIN_CELL = "internvl3_8b|FA", "internvl3_8b_FA_vi"  # the only run folder this command opens (O1-C4, C7)
RES_SHA = "9b9c3f6e5d4671ea6d69698be9f6431ed9d2937674e165272bf6ca460f545682"  # tier-1 res.json (OPS-1102e2b-score)
SCORED_SHA = "0101821e9815c662fa150569ce9893189b78708403ccf4cc696df7b62435e40c"  # tier-1 SCORED.json (same line)
WIN_PROBES_PREFIX = "498aea9e"  # OPS-1102e2b-cell2-done; the launch OPS line gives the full sha (--probes-sha)
N_SELECT = 338  # select-half images (the W25 hold 392985 is a tune-half id)
# K3 constants (PREREG §5; O1 §3-§4)
H1_MIN, H2_MAX, PASS_GATE = 5.0, 15.0, 0.98
N_SCREEN = 1004  # screen parameter (A1 l.330, AMBER generative 1,004), not a registered tier-3 n
B_OUT, B_IN, SEED_T2, SEED_PRED = 500, 1000, 20261102, 20261105
CUSHION_PTS = 2  # one value: +2.0 strict-recall points (= the H4 margin)
CPU_CAP_H = 1.0
RES_NAME, GUARD_NAME = "res_1c.json", "SCORED_1C.json"
KEYS = ("dprec", "U", "dret", "drecall")


class CapStop(Exception):
    """The 1 h wall cap was reached before any output was written (operator FAULT, no outcome)."""


# ------------------------------------------------------------------------------------------------ K2-K4
def point_from_rows(rows) -> dict:
    """K2: the un-resampled paired_ci estimator on per-image count rows: ratio per type, macro, difference.
    NaN everywhere when a primary type has no REJECTED for either system, no gold-true or no gold-false probe."""
    import numpy as np

    T = np.asarray(rows, dtype=float).sum(axis=0).reshape(len(e2b.PRIMARY), e2b.NCNT)
    RyE, RE, RyV, RV, StE, StV, nt, UE, n, nf = (T[:, j] for j in range(e2b.NCNT))
    if ((RE == 0) | (RV == 0) | (nt == 0) | (nf == 0)).any():
        return {k: float("nan") for k in KEYS}
    return {"dprec": float(100 * (RyE / RE - RyV / RV).mean()), "U": float(100 * (UE / n).mean()),
            "dret": float(100 * ((StE - StV) / nt).mean()), "drecall": float(100 * ((RyE - RyV) / nf).mean())}


def rules_pass(point: dict, ci: dict) -> bool:
    """K3: PASS = H1 and H2 and H3 and H4 at the PREREG §5 constants. ci: {k: [lo, hi]} (95 % percentile)."""
    if not all(math.isfinite(point[k]) for k in KEYS):
        return False
    return (point["dprec"] >= H1_MIN and ci["dprec"][0] > 0          # H1
            and point["U"] <= H2_MAX                                  # H2
            and ci["dret"][0] > e2b.RET_MARGIN                        # H3
            and ci["drecall"][0] > e2b.RET_MARGIN)                    # H4


def ppass(rows, n_t3: int, B_out: int = B_OUT, B_in: int = B_IN, seed: int = SEED_T2,
          pre_n: int | None = None, pre_seed: int | None = None, deadline: float | None = None) -> dict:
    """K4: nested image-cluster bootstrap (NB-C6). Outer: n_t3 image rows with replacement (default_rng(seed));
    with pre_n, each outer replicate first redraws pre_n rows (default_rng(pre_seed); the predictive variant).
    Inner: K1 ci_from_table with B_in, seed + b. An outer replicate whose point is undefined, or whose inner run
    drops more than MAX_DROP of its replicates, is not passing and is counted (CC-233r2 NB3: never aborts).
    Prints nothing (NB2). deadline: time.monotonic() value, checked between outer replicates -> CapStop."""
    import numpy as np

    if pre_n and pre_seed is None:
        raise ValueError("ppass: pre_n needs pre_seed (an unseeded predictive draw is not allowed)")
    R = np.asarray(rows, dtype=float)
    rng = np.random.default_rng(seed)
    rng_pre = np.random.default_rng(pre_seed) if pre_n else None
    n_pass = n_undef = n_fault = 0
    for b in range(B_out):
        if deadline is not None and time.monotonic() > deadline:
            raise CapStop("wall cap reached")  # no progress figure (CC-233r2 NB2)
        base = R[rng_pre.integers(0, len(R), pre_n)] if pre_n else R
        Tb = base[rng.integers(0, len(base), n_t3)]
        point = point_from_rows(Tb)
        if not all(math.isfinite(point[k]) for k in KEYS):
            n_undef += 1
            continue
        st, bad = e2b.ci_from_table(Tb, B_in, seed + b)
        if bad.mean() > e2b.MAX_DROP:
            n_fault += 1
            continue
        ci = {k: [float(np.percentile(v[~bad], 2.5)), float(np.percentile(v[~bad], 97.5))] for k, v in st.items()}
        n_pass += rules_pass(point, ci)
    p = n_pass / B_out
    return {"p_hat": p, "mc_se": math.sqrt(p * (1 - p) / B_out), "n_pass": n_pass, "n_undefined": n_undef,
            "n_inner_fault": n_fault, "B_out": B_out, "B_in": B_in, "seed": seed, "n_t3": n_t3,
            "pre_n": pre_n, "pre_seed": pre_seed}


# ------------------------------------------------------------------------------------------------ K5
def k_target(k_v: int, n_f: int) -> int:
    """k* = k_V + ceil(CUSHION_PTS * n_f / 100), in integers (O1 §3 step 2)."""
    return k_v + (CUSHION_PTS * n_f + 99) // 100


def fit_1c(pE, pV, op: list) -> tuple[dict, dict, dict, list]:
    """K5 (O1 §3): per type, on the tune rows of op only (e2b.tune_of). Vintern: its own registered band (GRID,
    R_DESIGN, hi_rule). E2b: the smallest GRID value whose tune hits reach k*, then hi_rule. A primary type with no
    gold-false tune probe, no feasible Vintern t_lo, or an unreachable k* makes the config infeasible (no fallback);
    a descriptive type takes the registered (0.5, 0.5). Returns (thrE, thrV, info, infeasible reasons)."""
    thrE, thrV, info, why = {}, {}, {}, []
    for t in e2b.TYPES:
        tu = e2b.tune_of(op, t)
        y = [s["y"] for s in tu]
        pe, pv = [pE(s) for s in tu], [pV(s) for s in tu]
        n_f = sum(y)
        v_ok = bool(n_f) and any(e2b.recall([v <= g for v in pv], y) >= e2b.R_DESIGN for g in e2b.GRID)
        thrV[t] = e2b.band(pv, y)
        k_v = sum(v <= thrV[t][0] and yy for v, yy in zip(pv, y)) if v_ok else None
        k_s = k_target(k_v, n_f) if v_ok else None
        hits = lambda g: sum(e <= g and yy for e, yy in zip(pe, y))  # noqa: E731
        lo = next((g for g in e2b.GRID if hits(g) >= k_s), None) if v_ok else None
        reason = ("no gold-false tune probe" if not n_f else "Vintern band has no feasible t_lo" if not v_ok
                  else f"k* {k_s} unreachable on GRID (max E2b tune hits {hits(e2b.GRID[-1])})" if lo is None else None)
        thrE[t] = (0.5, 0.5) if reason else (lo, e2b.hi_rule(pe, y, lo))
        info[t] = {"n_f": n_f, "k_V": k_v, "k_star": k_s, "kE": hits(thrE[t][0]) if n_f else 0,
                   "tE": list(thrE[t]), "tV": list(thrV[t]), "feasible": reason is None, "reason": reason}
        if reason and t in e2b.PRIMARY:
            why.append(f"{t}: {reason}")
    return thrE, thrV, info, why


# ------------------------------------------------------------------------------------------------ K6
def write_excl(path: Path, text: str) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)


def preflight(a) -> None:
    """Refuse before any data read: an existing res_1c.json or SCORED_1C.json (once-guard, either file), a res.json
    or SCORED.json other than the tier-1 pins, a winner other than internvl3_8b|FA, a probes sha not of cell 2."""
    for name in (GUARD_NAME, RES_NAME):
        if (a.runs / name).exists():
            raise SystemExit(f"REFUSED: {name} exists (screened once; an orphan res_1c.json goes to a judge)")
    if m0.sha_file(a.res) != RES_SHA or json.loads(a.res.read_text())["winner"] != WINNER:
        raise SystemExit("REFUSED: --res is not the tier-1 res.json 9b9c3f6e with winner internvl3_8b|FA")
    g = a.runs / "SCORED.json"
    if m0.sha_file(g) != SCORED_SHA or json.loads(g.read_text())["res_sha256"] != RES_SHA:
        raise SystemExit("REFUSED: runs/SCORED.json is not the tier-1 guard 0101821e")
    if not a.probes_sha.startswith(WIN_PROBES_PREFIX) or len(a.probes_sha) != 64:
        raise SystemExit(f"REFUSED: --probes-sha must be the full sha of cell 2 ({WIN_PROBES_PREFIX}...)")


def real_loader(a):
    S, segs = e2b.sets_and_segments(a.data, e2b.w25_lists())
    return S, segs, e2b.m0_pv(a.m0_probes, {e2b.key(s) for s in segs})


def run_screen(a, load=None) -> int:
    """K6: preflight, load, fit on tune, one select read, decision, reports; res_1c.json (O_EXCL) then the guard,
    then the byte copies. Nothing about the outcome is printed before res_1c.json exists (NB2)."""
    deadline = time.monotonic() + CPU_CAP_H * 3600
    preflight(a)
    S, segs, pv = (load or real_loader)(a)  # looked up at call time (the selftest traps real_loader)
    keys = {e2b.key(s) for s in segs}
    status, mass = e2b.classify(a.runs / WIN_CELL, keys, "vi")  # the only run folder read; never *_en
    if status != "DONE" or m0.sha_file(a.runs / WIN_CELL / "probes.jsonl") != a.probes_sha:
        raise SystemExit(f"REFUSED: {WIN_CELL} is {status} or its probes.jsonl is not --probes-sha")
    op = [s for s in segs if s["image"] in S["sel"]]
    sel = [s for s in op if s["half"] == "select"]
    held = [s for s in segs if s["image"] in S["held"]]
    if len({s["image"] for s in sel}) != N_SELECT:
        raise SystemExit(f"FAULT: select half has {len({s['image'] for s in sel})} images, not {N_SELECT}")
    thrE, thrV, info, why = fit_1c(lambda s: e2b.fa_p(mass[e2b.key(s)]), lambda s: pv[e2b.key(s)], op)
    fE = lambda s: e2b.band_label(e2b.fa_p(mass[e2b.key(s)]), *thrE[s["t2"]])  # noqa: E731
    fV = lambda s: e2b.band_label(pv[e2b.key(s)], *thrV[s["t2"]])  # noqa: E731
    rj = json.loads(a.res.read_text())
    res = {"label": LABEL_1C, "config": CONFIG, "post_hoc": True,
           "rule": {"grid": list(e2b.GRID), "cushion_pts": CUSHION_PTS, "n_screen": N_SCREEN, "B_out": B_OUT,
                    "B_in": B_IN, "seed": SEED_T2, "seed_pred": SEED_PRED, "pass_gate": PASS_GATE,
                    "H1_min": H1_MIN, "H2_max": H2_MAX, "H3_H4_margin": e2b.RET_MARGIN},
           "inputs": {"res": RES_SHA, "scored": SCORED_SHA, "m0_probes": e2b.M0_PROBES, "win_probes": a.probes_sha,
                      "w25_lists": m0.sha_file(e2b.W25_LISTS) if e2b.W25_LISTS.is_file() else None},
           "fit": info, "infeasible_reasons": why,
           "tier1_winner_record": {**{k: rj["configs"][WINNER][k] for k in KEYS}, "ci": rj.get("winner_ci_select")}}
    if why:
        res["screen"] = "INFEASIBLE"
    else:
        rows = e2b.per_image_counts(sel, fE, fV)
        dec = ppass(rows, n_t3=N_SCREEN, B_out=B_OUT, B_in=B_IN, seed=SEED_T2, deadline=deadline)
        res["screen"] = "SCREEN GO" if dec["p_hat"] >= PASS_GATE else "SCREEN NO-GO"
        res["decision"] = dec
        res["predictive_descriptive"] = ppass(rows, n_t3=N_SCREEN, B_out=B_OUT, B_in=B_IN, seed=SEED_T2,
                                              pre_n=len(rows), pre_seed=SEED_PRED, deadline=deadline)
        try:
            ci = e2b.paired_ci(rows)
        except e2b.Fault as e:
            ci = {"fault": str(e)}
        res["select"] = {"n_images": len(rows), "point": point_from_rows(rows), "paired_ci": ci,
                         "e2b": e2b.table(fE, sel), "vintern": e2b.table(fV, sel)}
    res["held_report_only"] = {"n_images": len({s["image"] for s in held}),  # after the decision field is set
                               "e2b": e2b.table(fE, held), "vintern": e2b.table(fV, held)}
    if time.monotonic() > deadline:
        raise CapStop("wall cap reached before the output was written")
    write_excl(a.runs / RES_NAME, json.dumps(res, indent=1, default=str) + "\n")
    rsha = m0.sha_file(a.runs / RES_NAME)
    write_excl(a.runs / GUARD_NAME, json.dumps({"res_1c_sha256": rsha, "res_sha256": RES_SHA, "inputs": res["inputs"],
                                                "utc": time.time()}) + "\n")
    a.copy_to.mkdir(parents=True, exist_ok=True)
    for name in (RES_NAME, GUARD_NAME):
        if (a.copy_to / name).exists():
            raise SystemExit(f"REFUSED: copy target {name} exists")
        shutil.copyfile(a.runs / name, a.copy_to / name)
        if m0.sha_file(a.copy_to / name) != m0.sha_file(a.runs / name):
            raise SystemExit(f"FAULT: copy of {name} differs")
    print(json.dumps({"screen": res["screen"], "res_1c_sha256": rsha,
                      "SCORED_1C.json_sha256 (OPS line)": m0.sha_file(a.runs / GUARD_NAME)}))
    return 0


def cmd_screen_1c(a, load=None) -> int:
    try:
        return run_screen(a, load)
    except CapStop as e:
        print(f"CAP_STOP (no outcome written): {e}")
        return 4


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    s = sp.add_parser("screen-1c")
    s.add_argument("--data", type=Path, default=e2b.ROOT / m0.MH)
    s.add_argument("--runs", type=Path, required=True, help="the one pulled runs folder of OPS-1102e2b-score")
    s.add_argument("--m0-probes", type=Path, required=True)
    s.add_argument("--res", type=Path, required=True, help="tier-1 res.json (9b9c3f6e)")
    s.add_argument("--probes-sha", required=True, help="full sha256 of internvl3_8b_FA_vi/probes.jsonl (498aea9e...)")
    s.add_argument("--copy-to", type=Path, default=e2b.ROOT / ".session_backup/2026-11-03/e2b_t1c")
    a = ap.parse_args()
    if a.cmd == "selftest":
        import test_e2b_1c

        return test_e2b_1c.main()
    return cmd_screen_1c(a)


if __name__ == "__main__":
    sys.exit(main())
