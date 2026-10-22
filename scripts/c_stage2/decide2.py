#!/usr/bin/env python3
"""Paper C stage 2 (STAGE 2 / DEV-B, ONE LOOK): `decide --phase confirm`, the fixed rules of the prereg applied to
the stage-2 ledger, with the frozen configuration as constants (pick() is never called).
Prereg manuscript/prereg/2026-10-22_c_stage2/PREREG.md §6.4, §7.1-§7.5, §12 item 8; CC-086b O4.

  python scripts/c_stage2/decide2.py --selftest                                                      CPU, no data
  python scripts/c_stage2/decide2.py confirm --ledger F [--verified V] --out D.json                  CPU
The output records the sha256 of every ledger it read (O4). OV-dev-B gates (§7.2); XM-dev500 is secondary (§7.3);
H_G (§7.5) decides the guard claim on OV-dev-B. Gate rows are found by exact run id, so no image-blind or NN row can
enter G1-G3, L, S1-S3 or H_G. Bootstrap: B = 2000, default_rng(0), one index matrix per set (§6.4).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stage2 as S2  # noqa: E402

C, lb = S2.C, S2.lb
import score as S  # noqa: E402  boot, pcm_ci, diff, length_gap, latest: stage 1, unchanged

SESOI = 2.0
GATE = 2 * SESOI
PCM_FLOOR, COPY_MAX, HG_COST, VP_FLOOR = -1.0, 0.05, -1.0, -1.0


def draws(n: int) -> np.ndarray:
    """The set's one (B, n) resample matrix: the first draw of a fresh default_rng(0), as score.boot and pcm_ci."""
    return np.random.default_rng(S.SEED).integers(0, n, (S.DRAWS, n))


def ratio(num: np.ndarray, den: np.ndarray, num0: np.ndarray | None = None, den0: np.ndarray | None = None) -> dict:
    """100 * sum num / sum den (minus the same for a base), numerator and denominator resampled together over
    images; percentile 95% CI over the draws whose denominators are non-zero."""
    def stat(ix):
        with np.errstate(divide="ignore", invalid="ignore"):
            v = 100 * num[ix].sum(-1) / den[ix].sum(-1)
            return v if num0 is None else v - 100 * num0[ix].sum(-1) / den0[ix].sum(-1)

    point = stat(np.arange(len(num)))
    d = stat(draws(len(num)))
    ok = np.isfinite(d)
    if not np.isfinite(point) or not ok.any():
        return {"d": None, "lo": None, "hi": None, "undefined_draws": int((~ok).sum())}
    lo, hi = np.percentile(d[ok], [2.5, 97.5])
    return {"d": float(point), "lo": float(lo), "hi": float(hi), "undefined_draws": int((~ok).sum())}


def get(rows: list[dict], run_id: str, tau: str = "-inf") -> dict:
    hit = [r for r in rows if r["run_id"] == run_id and r["tau"] == tau]
    if len(hit) != 1:
        raise SystemExit(f"ledger: {len(hit)} rows for {run_id} at tau {tau}")
    return hit[0]


def arr(row: dict, key: str) -> np.ndarray:
    return np.array(row["per_image"][key], float)


def same_ids(*rows: dict) -> None:
    if len({tuple(r["per_image"]["ids"]) for r in rows}) != 1:
        raise SystemExit("rows are not on the same images")


def cider_diff(a: dict, b: dict, key: str = "cider_s") -> np.ndarray:
    same_ids(a, b)
    return arr(a, key) - arr(b, key)


def rid(cfg: dict, ds: str, m: str, arm: str) -> str:
    return S2.spec(cfg, ds, m, arm)["run_id"]


def safe(fn, *a) -> dict:
    """A set or a row that is not complete is reported as incomplete and gives no verdict (§7.4)."""
    try:
        return fn(*a)
    except SystemExit as e:
        return {"incomplete": str(e)}


# ------------------------------------------------------------------------------------------------ §7.2 / §7.3
def gate(rows: list[dict], cfg: dict, ds: str) -> dict:
    rep, diffs = {}, []
    for m in C.MODELS:
        t = cfg["models"][m]["tau"]
        ret, rand, fix = (get(rows, rid(cfg, ds, m, a), t) for a in ("ret", "rand", "fix"))
        zs = get(rows, rid(cfg, ds, m, "zs"))
        diffs.append(cider_diff(ret, rand))
        rep[m] = {"vs_rand": S.boot(diffs[-1]), "vs_fix": S.boot(cider_diff(ret, fix)),
                  "vs_zs": S.boot(cider_diff(ret, zs)), "pcm_vs_zs": S.pcm_ci(ret),
                  "verbatim_share": ret["verbatim_share"], "length": S.length_gap(ret, rand),
                  "ptb_vs_rand": S.boot(cider_diff(ret, rand, "cider_ptb")),
                  "style": {a: x["style"] for a, x in (("ret", ret), ("rand", rand), ("fix", fix))},
                  "src_share": {a: x.get("src_share") for a, x in (("ret", ret), ("rand", rand), ("fix", fix))}}
    pooled = S.boot(np.mean(diffs, axis=0))
    g1 = pooled["d"] >= GATE and pooled["lo"] > 0
    g2 = all(rep[m]["pcm_vs_zs"]["lo"] > PCM_FLOOR for m in C.MODELS)
    g3 = all(rep[m]["verbatim_share"] <= COPY_MAX for m in C.MODELS)
    tied = any(rep[m]["length"]["not_separated_from_length"] for m in C.MODELS)
    verdict = "JUDGE: not separated from length" if tied else "PASS" if g1 and g2 and g3 else "FAIL"
    return {"pooled_vs_rand": pooled, "G1": g1, "G2": g2, "G3": g3, "L": tied, "per_model": rep,
            "pooled_vs_fix": S.boot(np.mean([rep_d(rows, cfg, ds, m, "fix") for m in C.MODELS], axis=0)),
            "pooled_vs_zs": S.boot(np.mean([rep_d(rows, cfg, ds, m, "zs") for m in C.MODELS], axis=0)),
            "verdict": verdict}


def rep_d(rows, cfg, ds, m, arm) -> np.ndarray:
    t = cfg["models"][m]["tau"]
    return cider_diff(get(rows, rid(cfg, ds, m, "ret"), t), get(rows, rid(cfg, ds, m, arm), t if arm != "zs" else
                                                                "-inf"))


# ------------------------------------------------------------------------------------------------ §7.5 H_G, S3
def np_block(row: dict, tk: str, mk: str) -> tuple[np.ndarray, np.ndarray]:
    return arr(row, tk), arr(row, mk)


def j3(tp: np.ndarray, m: np.ndarray) -> dict:
    return {"np": 100 * tp.sum() / m.sum() if m.sum() else None, "sum_m": int(m.sum()),
            "share_m_pos": float((m > 0).mean())}


def h_g(rows: list[dict], cfg: dict, ds: str, src: list[dict], tk: str, mk: str) -> dict:
    """H_G = NP(ret@tau_G) - NP(ret@-inf), pooled over the backbones (tp and m summed per image); passes if the CI
    lower bound > 0 and the pooled CIDEr-D (stripped) cost >= -1.0; Sigma m = 0 at tau_G is not passed. J1 scope."""
    per, g_tp, g_m, u_tp, u_m, cost = {}, 0, 0, 0, 0, []
    for m in C.MODELS:
        r, tg = rid(cfg, ds, m, "ret"), cfg["models"][m]["tau_G"]
        g, u = get(src, r, tg), get(src, r, "-inf")
        same_ids(g, u)
        (gt, gm), (ut, um) = np_block(g, tk, mk), np_block(u, tk, mk)
        g_tp, g_m, u_tp, u_m = g_tp + gt, g_m + gm, u_tp + ut, u_m + um
        cost.append(cider_diff(get(rows, r, tg), get(rows, r, "-inf")))
        dele = get(rows, r, "inf")
        per[m] = {"tau_G": tg, "h_g": ratio(gt, gm, ut, um)["d"], "at_tau_G": j3(gt, gm), "at_-inf": j3(ut, um),
                  "cost": float(cost[-1].mean()),
                  "delete_all": {"mentions_per_image": dele["mentions_per_image"], "chair_i": dele["chair_i"]}}
    pooled = ratio(g_tp, g_m, u_tp, u_m)
    c = float(np.mean(cost, axis=0).mean())
    passed = bool(g_m.sum() > 0 and pooled["lo"] is not None and pooled["lo"] > 0 and c >= HG_COST)
    pos = [m for m in C.MODELS if per[m]["h_g"] is not None and per[m]["h_g"] > 0]
    scope = ("not passed" if not passed else "general" if len(pos) == len(C.MODELS)
             else f"scoped to {pos[0]}" if pos else "no backbone with a positive point estimate")
    return {"pooled": pooled, "cost": c, "passed": passed, "scope": scope, "per_model": per,
            "pooled_at_tau_G": j3(g_tp, g_m), "pooled_at_-inf": j3(u_tp, u_m)}


def s3(cfg: dict, ds: str, src: list[dict], tk: str, mk: str) -> dict:
    """S3 (C-e): neighbour-only precision of ret at the frozen tau, per backbone and pooled, with CIs."""
    out, tp, mm = {}, 0, 0
    for m in C.MODELS:
        row = get(src, rid(cfg, ds, m, "ret"), cfg["models"][m]["tau"])
        t, n = np_block(row, tk, mk)
        out[m] = {**ratio(t, n), **j3(t, n)}
        tp, mm = tp + t, mm + n
    return {"per_model": out, "pooled": {**ratio(tp, mm), **j3(tp, mm)}}


def s2(cfg: dict, vrows: list[dict]) -> dict:
    """S2: pooled over mentions, Delta verified precision (OIV7) of ret at the frozen tau against zs; lo > -1.0."""
    p, a, p0, a0 = 0, 0, 0, 0
    for m in C.MODELS:
        ret = get(vrows, rid(cfg, "xm_dev500", m, "ret"), cfg["models"][m]["tau"])
        zs = get(vrows, rid(cfg, "xm_dev500", m, "zs"))
        same_ids(ret, zs)
        p, a, p0, a0 = p + arr(ret, "vp_p"), a + arr(ret, "vp_a"), p0 + arr(zs, "vp_p"), a0 + arr(zs, "vp_a")
    d = ratio(p, p + a, p0, p0 + a0)
    return {**d, "confirmed": d["lo"] is not None and d["lo"] > VP_FLOOR}


# ------------------------------------------------------------------------------------------------ reported rows
def reported(rows: list[dict], cfg: dict, ds: str) -> dict:
    """NN baselines (C-b), the image-blind arm (C-c) and the cosine-bin dose-response; none of them gates."""
    out = {"nn": {}, "blind": {}}
    for name, other in (("vs_nn_top1", lambda m, c: (f"c2_nn_{ds}-top1", "-inf", c["tau"])),
                        ("vs_nn_cons", lambda m, c: (f"c2_nn_{ds}-cons-k{c['k']}", "-inf", c["tau"])),
                        ("vs_blind", lambda m, c: (rid(cfg, ds, m, "blind"), "-inf", "-inf"))):
        out["nn" if name != "vs_blind" else "blind"][name] = safe(paired, rows, cfg, ds, other)
    out["dose_response"] = safe(dose, rows, cfg, ds)
    return out


def paired(rows: list[dict], cfg: dict, ds: str, other) -> dict:
    """ret minus another row, per backbone and pooled (per-image differences averaged over the backbones)."""
    d = {}
    for m in C.MODELS:
        c = cfg["models"][m]
        o_id, o_tau, r_tau = other(m, c)
        d[m] = cider_diff(get(rows, rid(cfg, ds, m, "ret"), r_tau), get(rows, o_id, o_tau))
    return {**{m: S.boot(x) for m, x in d.items()}, "pooled": S.boot(np.mean(list(d.values()), axis=0))}


def dose(rows: list[dict], cfg: dict, ds: str) -> dict:
    top1 = get(rows, f"c2_nn_{ds}-top1")
    cos, (c1, c2) = arr(top1, "top1_cos"), top1["dose_tertile_cuts"]
    d = []
    for m in C.MODELS:
        t = cfg["models"][m]["tau"]
        ret, rand = get(rows, rid(cfg, ds, m, "ret"), t), get(rows, rid(cfg, ds, m, "rand"), t)
        same_ids(ret, top1)
        d.append(cider_diff(ret, rand))
    pooled = np.mean(d, axis=0)
    bins = {"low": cos < c1, "mid": (cos >= c1) & (cos < c2), "high": cos >= c2}
    return {"cuts": [c1, c2], **{k: {"n": int(b.sum()), **S.boot(pooled[b])} for k, b in bins.items() if b.any()}}


def confirm(rows: list[dict], vrows: list[dict] | None, cfg: dict) -> dict:
    rows = S.latest(rows)
    vrows = S.latest(vrows) if vrows else None
    ov = safe(gate, rows, cfg, "ov_dev_b")
    out = {"ov_dev_b": {"gate": ov, "verdict": ov.get("verdict", f"INCOMPLETE: {ov.get('incomplete')}"),
                        "H_G": safe(h_g, rows, cfg, "ov_dev_b", rows, "np_tp", "np_m"),
                        "S3": safe(s3, cfg, "ov_dev_b", rows, "np_tp", "np_m"),
                        "reported": reported(rows, cfg, "ov_dev_b")}}
    if any(r["dataset"] == "xm_dev500" for r in rows):
        xm = safe(gate, rows, cfg, "xm_dev500")
        s1 = xm.get("pooled_vs_rand")
        out["xm_dev500"] = {"S1": {**s1, "confirmed": s1["d"] > 0} if s1 else xm, "L": xm.get("L"), "detail": xm,
                            "reported": reported(rows, cfg, "xm_dev500")}
        if vrows:
            out["xm_dev500"].update(S2=safe(s2, cfg, vrows),
                                    H_G=safe(h_g, rows, cfg, "xm_dev500", vrows, "npx_tp", "npx_m"),
                                    S3=safe(s3, cfg, "xm_dev500", vrows, "npx_tp", "npx_m"))
        else:
            out["xm_dev500"]["S2"] = "pending: local verified precision (§6.3)"
    return out


def cmd_confirm(a) -> None:
    led = [json.loads(x) for x in Path(a.ledger).read_text(encoding="utf-8").splitlines() if x]
    ver = [json.loads(x) for x in Path(a.verified).read_text(encoding="utf-8").splitlines() if x] if a.verified \
        else None
    res = confirm(led, ver, S2.frozen())
    rec = {"label": S2.LABEL, "c_schema": S2.SCHEMA, "phase": "confirm", "utc": lb.utc(),
           "ledger": {"path": str(a.ledger), "sha256": S2.sha_file(a.ledger), "rows": len(led)},
           "verified": {"path": str(a.verified), "sha256": S2.sha_file(a.verified), "rows": len(ver)} if a.verified
           else None, "c_prereg_sha256": S2.PINS[S2.PREREG], "frozen_config_sha256": S2.PINS[S2.FROZEN],
           "SESOI": SESOI, "gate": GATE, **res}
    Path(a.out).write_text(json.dumps(rec, indent=1, default=str) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def fake_ledger(cfg: dict, gain: float = 6.0, pcm: float = 0.0, verb: float = 0.0, long_ret: float = 12.0,
                hg: float = 0.3, cost: float = 0.0, n: int = 60) -> list[dict]:
    """A synthetic stage-2 ledger: per-image numbers only."""
    ids = [str(i) for i in range(n)]
    wig = np.sin(np.arange(n)) * 3
    rows = []

    def row(ds, m, arm, tau, x, extra=None):
        rid_ = rid(cfg, ds, m, arm) if m else arm
        tp_u = (np.arange(n) % 3 == 0).astype(int)
        tp = tp_u + ((np.arange(n) % 2 == 0) & (np.arange(n) % 3 != 0) if hg > 0 else 0)
        mm = np.full(n, 2)
        rows.append({"run_id": rid_, "dataset": ds, "model": m, "arm": arm, "tau": tau, "verbatim_share": verb,
                     "mentions_per_image": 1.0, "chair_i": 0.1,
                     "style": {"mean_syllables": long_ret if arm == "ret" else 12.0},
                     "per_image": {"ids": ids, "cider_s": x.tolist(), "cider_ptb": (x + 1).tolist(),
                                   "tp_cm": [1 if pcm < 0 else 2] * n, "tp_cm_zs": [2] * n,
                                   "k_cm": [2] * n, "np_tp": (tp if tau not in ("-inf", "inf") else tp_u).tolist(),
                                   "np_m": mm.tolist(), "top1_cos": np.linspace(0.3, 0.9, n).tolist()},
                     **(extra or {})})

    for ds in S2.SETS:
        for m in C.MODELS:
            c = cfg["models"][m]
            base = np.linspace(20, 40, n) + wig
            for tau in sorted({c["tau"], c["tau_G"], "-inf", "inf"}):
                row(ds, m, "ret", tau, base + gain + (cost if tau == c["tau_G"] and tau != "-inf" else 0))
            for arm in ("rand", "fix"):
                for tau in sorted({c["tau"], "-inf"}):
                    row(ds, m, arm, tau, base)
            row(ds, m, "zs", "-inf", base - 5)
            row(ds, m, "blind", "-inf", base + 100)  # never read by a gate
        row(ds, None, f"c2_nn_{ds}-top1", "-inf", np.linspace(20, 40, n), {"dose_tertile_cuts": [0.5, 0.7]})
        for k in sorted({c["k"] for c in cfg["models"].values()}):
            row(ds, None, f"c2_nn_{ds}-cons-k{k}", "-inf", np.linspace(20, 40, n))
    return rows


def selftest() -> None:
    cfg = S2.frozen()
    x = np.linspace(-1, 3, 50) + np.sin(np.arange(50))
    lo, hi = np.percentile(x[draws(50)].mean(1), [2.5, 97.5])
    assert S.boot(x) == {"d": float(x.mean()), "lo": float(lo), "hi": float(hi)}, "one index matrix per set (§6.4)"
    num, den = np.arange(50) % 3, np.full(50, 2)
    assert ratio(num, den)["d"] == 100 * num.sum() / den.sum() and ratio(num, 0 * den)["d"] is None
    ok = confirm(fake_ledger(cfg), None, cfg)
    assert ok["ov_dev_b"]["verdict"] == "PASS", ok["ov_dev_b"]["gate"]
    assert confirm(fake_ledger(cfg, gain=3.5), None, cfg)["ov_dev_b"]["verdict"] == "FAIL", "G1 needs point >= 2 SESOI"
    assert confirm(fake_ledger(cfg, pcm=-1), None, cfg)["ov_dev_b"]["verdict"] == "FAIL", "G2"
    assert confirm(fake_ledger(cfg, verb=0.06), None, cfg)["ov_dev_b"]["verdict"] == "FAIL", "G3"
    j = confirm(fake_ledger(cfg, long_ret=13.5), None, cfg)["ov_dev_b"]
    assert j["verdict"] == "JUDGE: not separated from length" and j["gate"]["G1"], "L fires whatever G1-G3 say"
    no_blind = [r for r in fake_ledger(cfg) if r["arm"] != "blind"]
    g_with, g_without = ok["ov_dev_b"]["gate"], confirm(no_blind, None, cfg)["ov_dev_b"]["gate"]
    assert g_with == g_without and ok["ov_dev_b"]["H_G"] == confirm(no_blind, None, cfg)["ov_dev_b"]["H_G"]
    part = [r for r in fake_ledger(cfg) if not (r["dataset"] == "ov_dev_b" and r["arm"] == "rand")]
    assert confirm(part, None, cfg)["ov_dev_b"]["verdict"].startswith("INCOMPLETE"), "an incomplete set: no verdict"
    hg = ok["ov_dev_b"]["H_G"]
    assert hg["passed"] and hg["scope"] == "general" and hg["pooled_at_tau_G"]["sum_m"] == 2 * 2 * 60
    assert hg["per_model"]["qwen25vl_7b"]["tau_G"] == "0.00", "tau_G = 0.0 when tau = -inf"
    assert not confirm(fake_ledger(cfg, hg=0), None, cfg)["ov_dev_b"]["H_G"]["passed"], "H_G fails on the CI"
    assert not confirm(fake_ledger(cfg, cost=-1.5), None, cfg)["ov_dev_b"]["H_G"]["passed"], "H_G fails on the cost"
    empty = [{**r, "per_image": {**r["per_image"], "np_m": [0] * 60, "np_tp": [0] * 60}} for r in fake_ledger(cfg)]
    assert confirm(empty, None, cfg)["ov_dev_b"]["H_G"]["scope"] == "not passed", "empty denominator: not passed"
    one = [{**r, "per_image": {**r["per_image"], "np_tp": r["per_image"]["np_tp"] if r["model"] != "internvl3_8b"
                               else ((np.arange(60) % 3 == 0).astype(int)).tolist()}} for r in fake_ledger(cfg)]
    sc = confirm(one, None, cfg)["ov_dev_b"]["H_G"]
    assert sc["passed"] and sc["scope"] == "scoped to qwen25vl_7b", sc["scope"]
    rep = ok["ov_dev_b"]["reported"]
    assert rep["blind"]["vs_blind"]["qwen25vl_7b"]["d"] < 0 and rep["nn"]["vs_nn_cons"]["internvl3_8b"]["d"] > 0
    assert rep["nn"]["vs_nn_top1"]["pooled"]["d"] > 0
    assert set(rep["dose_response"]) >= {"low", "mid", "high", "cuts"}
    assert ok["xm_dev500"]["S2"].startswith("pending") and ok["xm_dev500"]["S1"]["confirmed"]
    print("selftest ok: same resample indices, ratio CIs, PASS/FAIL/JUDGE (G1 2 x SESOI, G2, G3, L), incomplete set, "
          "blind rows never read, H_G pass/CI/cost/empty and J1 scope, tau_G, NN/blind/dose rows")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("confirm")
    p.add_argument("--ledger", type=Path, required=True)
    p.add_argument("--verified", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd != "confirm":
        ap.error("mode?")
    cmd_confirm(a)


if __name__ == "__main__":
    main()
