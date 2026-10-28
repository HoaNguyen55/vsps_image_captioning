#!/usr/bin/env python3
"""Paper D, D-alpha (DEV CURVE): does a scaling form fitted on B-1's L1-L4 points predict the L5 point?
Prereg manuscript/prereg/2026-10-28_d_extrap/PREREG.md (CC-147 ruling 1). Laptop CPU, after B-1's decide.

    python3 scripts/d_extrap/d_extrap.py --selftest                      synthetic ledgers only
    python3 scripts/d_extrap/d_extrap.py run --ledger L --out O          L = B-1 ledger.json; decide.json must sit beside it

Forms (fitted on L1-L4, never on L5): F1 y = a_s + b log2 N; F2 log y = c_s + beta ln N; F3 y = E_s - A N^-alpha.
e = mean over seeds of (y_L5 - yhat_L5); 95% percentile CI over B-1's own image index matrix; T = 2.0:
EXTRAPOLATES if the CI lies in [-T, +T], FAILS if it lies wholly outside, INCONCLUSIVE otherwise. Numbers only;
no caption is read (the ledger holds per-image scores, not text).
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True  # never write into scripts/b1_scaling/
sys.path[:0] = [str(ROOT / "scripts" / "b1_scaling")]
import b1  # noqa: E402  B-1's frozen code: plan(), run_name, SEEDS, DEV_TWIN, fe_slope, SP (B, BOOT_SEED, DEV_N)

B1_SUMS = ROOT / "scripts/b1_scaling/SHA256SUMS"
LABEL = "dev curve (dev300); D-alpha extrapolation, KTVIC development split, not a test result"
T = 2.0  # C's registered SESOI, manuscript/prereg/2026-10-25_c_test/PREREG.md l.148 (stripped CIDEr-D)
PRIMARY, REPLICATION = (43, 44), (42,)
FIT, TARGET = ("L1", "L2", "L3", "L4"), "L5"
F3_LO = {"A": 0.0, "alpha": 0.05, "E": 0.0}
F3_HI = {"A": 1e5, "alpha": 2.0, "E": 400.0}
MAX_FAIL = 0.05  # F3: NO VERDICT if more than 5% of bootstrap refits fail
SENT = {
    "EXTRAPOLATES": "On the KTVIC development split (dev300), {form} fitted to the four smaller training sizes "
                    "(216-1,734 images) predicted the full-data point (3,469 images) within +-2.0 stripped CIDEr-D: "
                    "e = {e:+.2f} [{lo:+.2f}, {hi:+.2f}] ({seeds}; image-bootstrap 95% CI, image sampling only).",
    "FAILS": "On the KTVIC development split (dev300), {form} fitted to the four smaller training sizes "
             "(216-1,734 images) {dir}-predicted the full-data point (3,469 images) by more than 2.0 stripped "
             "CIDEr-D: e = {e:+.2f} [{lo:+.2f}, {hi:+.2f}] ({seeds}; image-bootstrap 95% CI, image sampling only).",
    "INCONCLUSIVE": "On the KTVIC development split (dev300), {form} fitted to the four smaller training sizes gave "
                    "e = {e:+.2f} [{lo:+.2f}, {hi:+.2f}] at the full-data point ({seeds}); the interval overlaps "
                    "+-2.0 stripped CIDEr-D without lying inside it, so neither extrapolation nor failure is shown.",
    "NO VERDICT": "{form} gave no verdict on dev300 ({why}).",
}
NOTE = {"primary": "Seeds 43 and 44 are new draws whose L5 level is partly foreseeable from the B-F1 test scores "
                   "and S5; the CI covers image sampling only.",
        "replication": "Replication (S5's L3-L5 known).",
        "descriptive": "Descriptive row (all complete seeds); no verdict.",
        "mask": "Descriptive row (dev300 minus image 2004, byte twin of L5 train image 4487); no verdict."}
NAMES = {"F1": "the log-linear form (F1)", "F2": "the log-log power form (F2)", "F3": "the saturating power form (F3)"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def points() -> dict[tuple[int, str], tuple[str, int]]:
    """(seed, level) -> (ledger row name, N), from B-1's plan(); never hardcoded here."""
    return {(x["seed"], x["level"]): (k, x["N"]) for k, x in b1.plan(Path(".")).items() if x["kind"] == "point"}


def boot_index(draws: int = b1.SP.B) -> np.ndarray:
    """B-1's registered index matrix, built exactly as b1.decide builds it."""
    return np.random.default_rng(b1.SP.BOOT_SEED).integers(0, b1.SP.DEV_N, (draws, b1.SP.DEV_N))


def label(lo: float, hi: float) -> str:
    if -T <= lo and hi <= T:
        return "EXTRAPOLATES"
    if hi < -T or lo > T:
        return "FAILS"
    return "INCONCLUSIVE"


def f1(N: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Y (S, 5, ...) -> mean_s (y_L5 - yhat_L5) for y = a_s + b log2 N fitted on the first four levels."""
    x = np.log2(N)
    b = b1.fe_slope(x[:4], Y[:, :4])
    a = Y[:, :4].mean(1) - b * x[:4].mean()
    return (Y[:, 4] - (a + b * x[4])).mean(0)


def f2(N: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """log y = c_s + beta ln N on the first four levels; the residual is taken in CIDEr-D units."""
    x, L = np.log(N), np.log(Y[:, :4])
    beta = b1.fe_slope(x[:4], L)
    c = L.mean(1) - beta * x[:4].mean()
    return (Y[:, 4] - np.exp(c + beta * x[4])).mean(0)


def f3_fit(N: np.ndarray, y4: np.ndarray):
    """y4 (S, 4): least_squares(trf) for y = E_s - A N^-alpha, common A, alpha. Starts (clipped into the bounds):
    alpha0 = 0.5, E_s0 = max over L1-L4 of y_s + 1, A0 = mean_s (E_s0 - y_s,L1) * 216^0.5."""
    S = y4.shape[0]
    E0 = y4.max(1) + 1
    lo = np.array([F3_LO["A"], F3_LO["alpha"]] + [F3_LO["E"]] * S)
    hi = np.array([F3_HI["A"], F3_HI["alpha"]] + [F3_HI["E"]] * S)
    x0 = np.clip(np.r_[np.mean(E0 - y4[:, 0]) * N[0] ** 0.5, 0.5, E0], lo, hi)
    res = least_squares(lambda p: (p[2:, None] - p[0] * N[:4] ** -p[1] - y4).ravel(), x0, bounds=(lo, hi),
                        method="trf")
    return res, f3_failed(res)


def f3_failed(res) -> str:
    if res.status <= 0:
        return f"not converged (status {res.status})"
    if res.active_mask[1] != 0:
        return "alpha-hat at a bound"
    return ""


def f3_e(N: np.ndarray, Y: np.ndarray) -> tuple[float, str]:
    res, why = f3_fit(N, Y[:, :4])
    A, alpha, E = res.x[0], res.x[1], res.x[2:]
    return float((Y[:, 4] - (E - A * N[4] ** -alpha)).mean()), why


def form_row(form: str, N: np.ndarray, Y: np.ndarray, D: np.ndarray, seeds: list[int]) -> dict:
    """One form on one seed set: point e, its CI over the index matrix, the three-way label, the sentence."""
    tag = f"seeds {', '.join(map(str, seeds))}" + (" (one seed)" if len(seeds) == 1 else "")
    out = {"seeds": seeds}
    if form == "F2" and (Y <= 0).any() | (D <= 0).any():
        return out | no_verdict(form, "a point mean is <= 0, log undefined")
    if form == "F3":
        if len(seeds) < 2:
            return out | no_verdict(form, "one seed: 3 parameters on 4 points")
        e, why = f3_e(N, Y)
        if why:
            return out | no_verdict(form, f"point fit {why}")
        reps = [f3_e(N, D[..., k]) for k in range(D.shape[-1])]
        ok = np.array([not w for _, w in reps])
        out["bootstrap_refits_failed"] = int((~ok).sum())
        if (~ok).mean() > MAX_FAIL:
            return out | no_verdict(form, f"{int((~ok).sum())} of {len(ok)} bootstrap refits failed (> 5%)")
        draws = np.array([v for v, _ in reps])[ok]
    else:
        e, draws = float((f1 if form == "F1" else f2)(N, Y)), (f1 if form == "F1" else f2)(N, D)
    lo, hi = (float(v) for v in np.percentile(draws, [2.5, 97.5]))
    v = label(lo, hi)
    return out | {"e": e, "ci95": [lo, hi], "verdict": v, "sentence": SENT[v].format(
        form=NAMES[form], e=e, lo=lo, hi=hi, seeds=tag, dir="under" if e > 0 else "over")}


def no_verdict(form: str, why: str) -> dict:
    return {"verdict": "NO VERDICT", "why": why, "sentence": SENT["NO VERDICT"].format(form=NAMES[form], why=why)}


def seed_set(cid: dict, idx: np.ndarray, seeds: list[int], mask: int | None = None) -> dict:
    """Y (S, 5) point means and D (S, 5, B) replicate means for these seeds; mask = dev position dropped (§6 B-1)."""
    P = points()
    lv = FIT + (TARGET,)
    N = np.array([P[seeds[0], v][1] for v in lv], float) if seeds else np.array([])
    if not seeds:
        return {"N": N}
    keep = np.ones(b1.SP.DEV_N, bool) if mask is None else np.arange(b1.SP.DEV_N) != mask
    M = idx != (-1 if mask is None else mask)
    Y = np.array([[cid[P[s, v][0]][keep].mean() for v in lv] for s in seeds])
    D = np.array([[(cid[P[s, v][0]][idx] * M).sum(1) / M.sum(1) for v in lv] for s in seeds])
    return {"N": N, "Y": Y, "D": D}


def row(cid: dict, idx: np.ndarray, seeds: list[int], role: str, note: str, mask: int | None = None,
        descriptive: bool = False) -> dict:
    """One row of §4: the three forms, each sentence followed by the row's note (§9); a descriptive row carries
    label_descriptive in place of verdict."""
    key = "label_descriptive" if descriptive else "verdict"
    if not seeds:
        return {"role": role, key: "NO VERDICT", "why": "no complete seed in this row"}
    d = seed_set(cid, idx, seeds, mask)
    forms = {f: form_row(f, d["N"], d["Y"], d["D"], seeds) for f in ("F1", "F2", "F3")}
    for v in forms.values():
        v["sentence"] += " " + note
        v[key] = v.pop("verdict")
    return {"role": role, "seeds": seeds, "fit_levels": list(FIT), "target": TARGET, "forms": forms}


def analyse(led: dict, draws: int = b1.SP.B) -> dict:
    rows = led["rows"]
    P = points()
    assert len(P) == 15, "B-1 plan() must list 15 points"
    complete = [s for s in b1.SEEDS if all(P[s, v][0] in rows for v in FIT + (TARGET,))]
    cid = {k: np.array(v["cider_s"], float) for k, v in rows.items()}
    assert all(len(v) == b1.SP.DEV_N for v in cid.values()), "every row must carry 300 per-image scores"
    idx = boot_index(draws)
    prim = [s for s in PRIMARY if s in complete]
    out = {"label": LABEL, "T": T, "complete_seeds": complete,
           "bootstrap": {"B": draws, "rng": f"numpy default_rng({b1.SP.BOOT_SEED})", "n_images": b1.SP.DEV_N,
                         "note": "B-1's own index matrix; the CI covers image sampling only"},
           "primary": row(cid, idx, prim, "primary (seeds 43, 44)", NOTE["primary"]),
           "replication_seed42": row(cid, idx, [s for s in REPLICATION if s in complete], "replication (seed 42)",
                                     NOTE["replication"]),
           "all_complete_descriptive": row(cid, idx, complete, "descriptive (all complete seeds)",
                                           NOTE["descriptive"], descriptive=True)}
    ids = {tuple(v["ids"]) for v in rows.values() if "ids" in v}
    if len(ids) == 1 and b1.DEV_TWIN in next(iter(ids)):
        j = next(iter(ids)).index(b1.DEV_TWIN)
        out["mask_2004_descriptive"] = row(cid, idx, prim, "descriptive: dev300 minus image 2004", NOTE["mask"], j,
                                           descriptive=True) | {"n_images": 299}
    else:
        out["mask_2004_descriptive"] = {"computable": False, "why": "no common id list holding image 2004"}
    return out


def cmd_run(a) -> None:
    dec = a.ledger.parent / "decide.json"
    if not dec.exists():
        raise SystemExit(f"{dec} missing: D-alpha runs only after B-1's decide (W2)")
    if a.out.exists():
        raise SystemExit(f"{a.out} exists; D-alpha runs once")
    pin = {ln.split()[1]: ln.split()[0] for ln in B1_SUMS.read_text().splitlines() if ln.strip()}
    if sha(Path(b1.__file__)) != pin["scripts/b1_scaling/b1.py"]:
        raise SystemExit("imported b1.py differs from scripts/b1_scaling/SHA256SUMS")
    if json.loads(dec.read_text(encoding="utf-8")).get("ledger_sha256") != sha(a.ledger):
        raise SystemExit("ledger sha256 differs from decide.json ledger_sha256")
    res = analyse(json.loads(a.ledger.read_text(encoding="utf-8"))) | {
        "inputs": {"ledger_sha256": sha(a.ledger), "decide_sha256": sha(dec), "b1_sha256": sha(Path(b1.__file__)),
                   "code_sha256": sha(Path(__file__)), "numpy": np.__version__, "scipy": scipy.__version__}}
    a.out.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: {f: v.get("verdict") for f, v in res[k].get("forms", {}).items()}
                      for k in ("primary", "replication_seed42")}, indent=1))


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def synth(fn, shift=(0.0, 1.0, -1.0), jump: float = 0.0, noise: float = 0.0) -> dict:
    """Synthetic ledger: per-image score = fn(N) + seed shift (+ jump at L5) + centred noise, so every point mean is
    exact and only the bootstrap sees the noise. Ids hold image 2004."""
    rng = np.random.default_rng(7)
    rows = {}
    for (s, lv), (name, n) in points().items():
        z = rng.normal(size=b1.SP.DEV_N) * noise
        rows[name] = {"cider_s": (fn(n) + shift[b1.SEEDS.index(s)] + jump * (lv == TARGET) + z - z.mean()).tolist()}
    ids = sorted([b1.DEV_TWIN] + [f"zq{i:03d}" for i in range(b1.SP.DEV_N - 1)])
    for r in rows.values():
        r["ids"] = ids
    return {"rows": rows}


def selftest() -> None:
    run = functools.partial(analyse, draws=40)  # selftest speed; the registered B = 2000 is asserted below
    def verdicts(out, key="primary"):
        return {f: v["verdict"] for f, v in out[key]["forms"].items()}

    loglin = lambda n: 60 + 6 * np.log2(n)  # noqa: E731
    sat = lambda n: 150 - 900 * n ** -0.5  # noqa: E731
    # row names come from B-1's plan(); the index matrix is B-1's
    assert sorted(k for k, _ in points().values()) == sorted(b1.run_name(s, lv) for s in b1.SEEDS for lv in b1.LEVELS)
    assert boot_index().shape == (2000, 300) and (boot_index(5) == boot_index()[:5]).all()
    # exact log-linear: F1 e ~ 0, EXTRAPOLATES; +15 at L5: F1 FAILS (under-predicted)
    out = run(synth(loglin))
    assert abs(out["primary"]["forms"]["F1"]["e"]) < 1e-9 and verdicts(out)["F1"] == "EXTRAPOLATES"
    out = run(synth(loglin, jump=15.0))
    f = out["primary"]["forms"]["F1"]
    assert f["verdict"] == "FAILS" and abs(f["e"] - 15) < 1e-9 and "under-predicted" in f["sentence"]
    # wide image noise around a small miss: INCONCLUSIVE
    f = run(synth(loglin, jump=1.5, noise=60.0))["primary"]["forms"]["F1"]
    assert f["verdict"] == "INCONCLUSIVE", f
    # exact power law: F2 e ~ 0; exact saturating curve: F3 e ~ 0, both EXTRAPOLATE
    out = run(synth(lambda n: 20 * n ** 0.25, shift=(0.0, 0.0, 0.0)))
    assert abs(out["primary"]["forms"]["F2"]["e"]) < 1e-6 and verdicts(out)["F2"] == "EXTRAPOLATES"
    out = run(synth(sat))
    f3 = out["primary"]["forms"]["F3"]
    assert abs(f3["e"]) < 1e-3 and f3["verdict"] == "EXTRAPOLATES" and f3["bootstrap_refits_failed"] == 0, f3
    # L5 never enters a fit: a jump at L5 moves e by exactly the jump in every form
    for form in ("F1", "F3"):
        e0 = run(synth(sat))["primary"]["forms"][form]["e"]
        assert abs(run(synth(sat, jump=9.0))["primary"]["forms"][form]["e"] - e0 - 9.0) < 1e-6, form
    # F3 fit-fail paths: alpha-hat at its upper bound (a step at L1 only), and a non-converged status
    step = lambda n: 140.0 - 1.0 * (n < 300)  # noqa: E731
    f3 = run(synth(step))["primary"]["forms"]["F3"]
    assert f3["verdict"] == "NO VERDICT" and "bound" in f3["why"], f3
    fake = argparse.Namespace(status=0, active_mask=np.zeros(4))
    assert f3_failed(fake).startswith("not converged")
    # seed 42 is a replication row; F3 never gives a verdict on one seed
    out = run(synth(sat))
    assert out["replication_seed42"]["seeds"] == [42] and verdicts(out, "replication_seed42")["F3"] == "NO VERDICT"
    # an incomplete seed is dropped; one primary seed is labelled; none gives NO VERDICT
    led = synth(loglin)
    del led["rows"][b1.run_name(44, "L3")]
    out = run(led)
    assert out["complete_seeds"] == [42, 43] and out["primary"]["seeds"] == [43]
    f = out["primary"]["forms"]
    assert f["F1"]["verdict"] == "EXTRAPOLATES" and "(one seed)" in f["F1"]["sentence"]
    assert f["F3"]["verdict"] == "NO VERDICT" and "one seed" in f["F3"]["why"]
    del led["rows"][b1.run_name(43, "L5")]
    assert run(led)["primary"]["verdict"] == "NO VERDICT"
    # mask row: image 2004 dropped; a jump on that image at L5 only moves the full-data row
    led = synth(loglin)
    j = led["rows"][b1.run_name(43, "L1")]["ids"].index(b1.DEV_TWIN)
    for s in PRIMARY:
        led["rows"][b1.run_name(s, TARGET)]["cider_s"][j] += 900.0
    out = run(led)
    assert abs(out["primary"]["forms"]["F1"]["e"] - 3.0) < 1e-6 and out["mask_2004_descriptive"]["n_images"] == 299
    m = out["mask_2004_descriptive"]["forms"]["F1"]
    assert abs(m["e"]) < 1e-9 and "verdict" not in m and m["sentence"].endswith(NOTE["mask"])
    a = out["all_complete_descriptive"]["forms"]["F1"]
    assert "verdict" not in a and "label_descriptive" in a and a["sentence"].endswith(NOTE["descriptive"])
    assert out["replication_seed42"]["forms"]["F1"]["sentence"].endswith(NOTE["replication"])
    assert out["primary"]["forms"]["F1"]["sentence"].endswith(NOTE["primary"])
    # the boundary is inclusive; F2 refuses a non-positive point
    assert label(-T, T) == "EXTRAPOLATES" and label(T + 0.1, 9) == "FAILS" and label(1.0, 2.5) == "INCONCLUSIVE"
    assert run(synth(lambda n: 0.0 * n))["primary"]["forms"]["F2"]["verdict"] == "NO VERDICT"
    assert "protocol_pilot" not in sys.modules
    print("d_extrap self-test ok: EXTRAPOLATES / FAILS / INCONCLUSIVE, F3 bound and status fail, one seed, "
          "no seed, incomplete seed dropped, L5 kept out of every fit, mask 2004")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    r = sub.add_parser("run")
    r.add_argument("--ledger", type=Path, required=True)
    r.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.cmd == "run":
        cmd_run(a)
    else:
        ap.error("--selftest or run")


if __name__ == "__main__":
    main()
