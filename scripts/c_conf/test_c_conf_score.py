"""Self-test and mutants of the C-CONF scorer (c_conf_score.py) on planted data only (§11.1 row c_conf_score.py,
CC-450 J1 N1 and X5).

Runs on a rented host (the investigator's rule of 2026-11-11: no test runs on the laptop), in a venv holding numpy:
    env -u PYTHONPATH venv/bin/python -I -B scripts/c_conf/test_c_conf_score.py   # self-test, then every mutant must fail it
Reads no study file and imports no host module (c_conf.py is never imported): every input is planted here.
"""
from __future__ import annotations

import argparse
import calendar
import contextlib
import hashlib
import importlib.util
import io
import json
import sys
import tempfile
import types
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE / "c_conf_score.py"
Q, I, AY, LM = "qwen25vl_7b", "internvl3_8b", "aya_vision_8b", "lmcap"


def load(path: Path):
    spec = importlib.util.spec_from_file_location(f"ccs_{abs(hash(str(path)))}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def centred(rng, n: int, sd: float) -> np.ndarray:
    z = rng.normal(0, 1, n)
    z = z - z.mean()
    return z / z.std(ddof=1) * sd


def planted(n: int, taus: dict, seed: int = 3, lmcap: float | None = 17.0) -> dict:
    """Per backbone m with taus[m] = (τ_pair, SD of ret - perm): rand d0-d2 around one base, perm p1, p2 with mean
    equal to the rand mean (τ_marg = 0), ret = perm mean + τ_pair + centred noise. LMCap ri = rand + lmcap."""
    rng = np.random.default_rng(seed)
    base = rng.normal(40, 10, n)
    per = {}
    for m, (tau, sd) in taus.items():
        d = [base + rng.normal(0, 4, n) for _ in range(3)]
        rmean = (d[0] + d[1] + d[2]) / 3
        e = rng.normal(0, 3, n)
        p1, p2 = rmean + e, rmean - e
        per |= {f"{m}|zs": rmean - 5, f"{m}|rand_d0": d[0], f"{m}|rand_d1": d[1], f"{m}|rand_d2": d[2],
                f"{m}|perm_p1": p1, f"{m}|perm_p2": p2, f"{m}|ret": (p1 + p2) / 2 + tau + centred(rng, n, sd)}
    if lmcap is not None:
        rl = base + rng.normal(0, 4, n)
        per |= {f"{LM}|lmcap_rand": rl, f"{LM}|lmcap_perm": rl + rng.normal(0, 2, n),
                f"{LM}|lmcap_ri": rl + lmcap + rng.normal(0, 6, n)}
    return per


def refused(f, *args, **kw) -> str:
    try:
        f(*args, **kw)
    except (SystemExit, FileExistsError) as e:
        return str(e) or "refused"
    raise AssertionError(f"{f.__name__} was not refused")


def selftest_stats(S) -> None:
    a3 = S.ALPHA / 3
    t = {"a": (2.0, a3), "b": (2.0, S.ALPHA / 2), "c": (2.0, S.ALPHA)}
    assert S.detected(t) == {"a", "b", "c"}, "boundary (θ̂ = 2.0; p = α_j): both inclusive"
    assert S.detected({**t, "a": (1.999, a3)}) == set(), "a point below +2.0 fails and ends the step-down"
    assert S.detected({"a": (5, 0.009), "b": (5, 0.010), "c": (5, 0.012)}) == set(), "Holm: 0.009 > 0.025 / 3"
    assert S.detected({"a": (5, 0.005), "b": (5, 0.013), "c": (5, 0.014)}) == {"a"}, "stops at the first failure"
    assert S.detected({"a": (5, 0.0124), "b": (5, 0.02)}) == {"a", "b"}, "two-claim family: 0.0124 <= 0.025 / 2"
    assert S.detected({"a": (5, 0.0124), "b": (5, 0.02), "c": (5, 0.02)}) == set(), "three claims: 0.0124 > 0.025 / 3"
    floor = 1 / 2001
    tie = {Q: (8.0, floor), I: (1.9, floor), AY: (6.0, floor)}
    assert S.detected(tie) == {Q, AY}, "CC-450 J1 N1: ties in p taken by decreasing θ̂, then by key"
    assert S.detected({"x": (2.0, 0.025)}) == {"x"} and S.detected({"x": (2.0, 0.02500001)}) == set(), "m = 1"
    lab = lambda **kw: S.label({"d": 0, "lo": -1, "hi": 1, "lo90": -1, "hi90": 1, **kw}, False)  # noqa: E731
    assert lab() == "NEGLIGIBLE" and lab(hi90=2.0) == "UNRESOLVED" and lab(lo90=-2.0) == "UNRESOLVED"
    assert lab(hi=-0.25, hi90=-0.5) == "REVERSED" and lab(hi=0.0) == "NEGLIGIBLE", "REVERSED needs hi < 0"
    assert S.MARGIN == 3.65 and S.Z_HOLM3 == 2.394 and S.P_BAR == 0.98 and S.SESOI == 2.0 and S.ALPHA == 0.025
    rm = S.rehearsal_matrix()
    assert rm.shape == (2000, 1941) and np.array_equal(rm, np.random.default_rng(1).integers(0, 2000, (2000, 1941))), \
        "§7.6 item 2: resamples of 1,941 from 2,000, default_rng(1)"
    assert np.array_equal(S.boot_idx(50), np.random.default_rng(0).integers(0, 50, (2000, 50))), "§7.3 matrix"
    rng = np.random.default_rng(9)
    x = 4.0 + centred(rng, 2000, 60.0)
    se, ok = S.replicate_share(x, rm)
    assert abs(se - 60.0 / np.sqrt(1941)) < 1e-9, "SE = SD (ddof 1) / √1,941"
    assert abs(ok.mean() - 0.7065) < 0.03, f"P_m on a planted normal sample (Holm term binds): {ok.mean():.3f}"


def selftest_rows(S) -> None:
    n = 1941
    per = planted(n, {Q: (3.0, 8.0), I: (3.0, 8.0), AY: (3.0, 8.0)})
    idx = S.boot_idx(n)
    rows = S.set_rows(per, idx)
    assert abs(rows[f"{Q}|tau_pair"]["d"] - 3) < 1e-9 and abs(rows[f"{Q}|tau_marg"]["d"]) < 1e-9, \
        "ret = perm + 3 and perm = rand give τ_pair = 3, τ_marg = 0"
    rmean = np.mean([per[f"{Q}|rand_d{d}"] for d in range(3)], 0)
    assert abs(rows[f"{Q}|tau_sel"]["d"] - (per[f"{Q}|ret"] - rmean).mean()) < 1e-9, "rand is the mean over d0-d2"
    bm = {e: rows[f"{Q}|{e}"]["_bm"] for e in ("tau_sel", "tau_marg", "tau_pair")}
    assert np.allclose(bm["tau_sel"], bm["tau_marg"] + bm["tau_pair"]), "one shared index matrix per set"
    ref = S.pair(per[f"{Q}|ret"], (per[f"{Q}|perm_p1"] + per[f"{Q}|perm_p2"]) / 2, np.random.default_rng(0).integers(0, n, (2000, n)))
    assert abs(ref["lo"] - rows[f"{Q}|tau_pair"]["lo"]) < 1e-9 and abs(ref["p"] - rows[f"{Q}|tau_pair"]["p"]) < 1e-12
    m3 = S.set_rows({**per, **{f"{k}_m3": v + 50 for k, v in per.items()}}, idx)
    assert all(abs(m3[k]["d"] - rows[k]["d"]) < 1e-12 for k in rows), "no extra column enters a draw mean"
    short = {k: v for k, v in per.items() if k != f"{AY}|perm_p2"}
    assert not any(k.startswith(AY) for k in S.set_rows(short, idx)), "a backbone with an incomplete arm gives no row"
    assert {f"{LM}|tau_sel", f"{LM}|tau_pair", f"{LM}|tau_marg"} <= set(rows) and S.control(rows) == "DETECTED"
    no_ri = {k: v for k, v in per.items() if k != f"{LM}|lmcap_ri"}
    assert S.control(S.set_rows(no_ri, idx)) == "NOT DETECTED", "an incomplete positive control is NOT DETECTED"
    led = [{"run_id": f"r{k}", "scored_set": "s", "model": k.split("|")[0], "arm": a, "draw": d,
            "per_image": {"ids": [f"i{j}" for j in range(4)], "cider_s": [1.0, 2.0, 3.0, 4.0]}}
           for k, a, d in ((f"{Q}|x", "rand", 1), (f"{Q}|y", "perm", 2), (f"{LM}|z", "lmcap_ri", None))]
    per2, ids2 = S.columns(led, "s")
    assert set(per2) == {f"{Q}|rand_d1", f"{Q}|perm_p2", f"{LM}|lmcap_ri"} and ids2 == ["i0", "i1", "i2", "i3"]
    assert "two ledger rows" in refused(S.columns, led + led[:1], "s")
    bad = [{**led[0], "per_image": {"ids": ["i3", "i2", "i1", "i0"], "cider_s": [1, 2, 3, 4]}, "arm": "zs"}]
    assert "image order" in refused(S.columns, led + bad, "s")


def selftest_rehearsal(S) -> None:
    n = 2000
    per = planted(n, {Q: (5.0, 8.0), I: (3.0, 8.0), AY: (3.7, 40.0)})
    d = S.rehearsal_decision(per, [f"i{j}" for j in range(n)])
    c = d["claims"]
    assert all(c[m]["carve_pass"] for m in (Q, I, AY)) and c[Q]["family"] == sorted((Q, I, AY))
    assert c[Q]["status"] == "TEST FAMILY" and c[Q]["share_ok"] and c[Q]["margin_ok"]
    assert c[I]["status"] == "CARVE PASS, NO MARGIN" and c[I]["share_ok"] and not c[I]["margin_ok"], \
        "a carve point of 3.0 fails the margin +3.65"
    assert S.margin_ok(3.65) and not S.margin_ok(3.64), "§11.1: a carve mean of 3.64 fails the margin, 3.65 passes"
    assert c[AY]["status"] == "CARVE PASS, NO MARGIN" and c[AY]["margin_ok"] and not c[AY]["share_ok"], \
        f"P_m {c[AY]['P_m']:.3f} < 0.98: entry needs all three conditions"
    assert d["entered"] == [Q] and d["positive_control"] == "DETECTED" and d["look"] and d["sentence"] is None
    assert d["label"] == S.LABEL_R and all(r["row"] == S.CARVE_ROW for r in d["rows_development"].values())
    nq = S.rehearsal_decision(planted(n, {Q: (3.0, 8.0), I: (5.0, 8.0), AY: (5.0, 8.0)}), list(range(n)))
    assert nq["entered"] == [I, AY] and not nq["look"] and nq["sentence"] == S.NO_LOOK, \
        "no look without the primary backbone"
    pc = S.rehearsal_decision({k: v for k, v in per.items() if k != f"{LM}|lmcap_perm"}, list(range(n)))
    assert pc["positive_control"] == "NOT DETECTED" and not pc["look"], "incomplete control: NOT DETECTED, no look"
    two = S.rehearsal_decision({k: v for k, v in per.items() if k != f"{AY}|perm_p2"}, list(range(n)))
    assert two["claims"][AY]["status"] == "NOT RUN" and two["claims"][Q]["family"] == sorted((Q, I)), "Holm m = 2"
    assert "full set" in refused(S.rehearsal_decision, per, list(range(n - 1)))


def token(S, bb) -> dict:
    return {"rehearsal_decision_sha256": "0" * 64, "yes_log_id": "PI-x", "ledger_line_log_id": "OPS-x", "backbones": bb}


def selftest_test(S) -> None:
    n = 1941
    ids = [f"t{j:04d}" for j in range(n)]
    per = planted(n, {Q: (3.0, 8.0), I: (3.0, 8.0), AY: (3.0, 8.0)}, seed=5)
    t3 = token(S, [Q, I, AY])
    d = S.test_decision({"ov_test_1941": (per, ids)}, t3, [])
    f = d["F1"]
    assert [f["claims"][m]["verdict"] for m in (Q, I, AY)] == ["PASS"] * 3 and f["row"] == 1
    assert f["sentence"] == S.SENTENCE[1][0].format("Qwen2.5-VL-7B, InternVL3-8B and Aya-Vision-8B")
    assert f["the split may enter"] == 'contributions and abstract, with the words "second look"'
    assert d["beside_sentence"]["S-marg NEGLIGIBLE"] == 3 and d["secondaries"][f"S-marg({Q})"]["reading"] == S.S_MARG["NEGLIGIBLE"]
    assert d["secondaries"][f"S-rep({Q})"]["reading"] == S.S_REP[Q][0] and d["secondaries"]["S-bb"]["reading"] == S.S_BB[0]
    assert d["secondaries"]["S-bb"]["abstract"] == "never" and d["positive_control"]["verdict"] == "DETECTED"
    q = f["claims"][Q]["row"]["labels"]
    assert S.KNOWN in q and S.OV_ROW in q and S.SECONDARY not in q, "F1 row: §7.13 labels, no secondary label"
    assert S.FIRST_DEC in f["claims"][AY]["row"]["labels"] and S.FIRST_DEC in d["positive_control"]["row"]["labels"]
    sec_rows = [r for r in d["secondaries"].values() if isinstance(r, dict)] + list(d["placebo"].values()) \
        + [d["positive_control"]["row"]]
    assert sec_rows and all(S.SECONDARY in r["labels"] for r in sec_rows), "every row outside F1 is secondary"
    assert all(v == "NOT RUN" for v in d["sensitivities"].values())
    # Qwen2.5-VL-7B fails, two others pass
    d2 = S.test_decision({"ov_test_1941": (planted(n, {Q: (0.0, 8.0), I: (3.0, 8.0), AY: (3.0, 8.0)}, seed=5), ids)}, t3, [])
    assert d2["F1"]["claims"][Q]["verdict"] == "FAIL" and d2["F1"]["row"] == 2
    assert d2["F1"]["sentence"] == S.SENTENCE[2][0].format("InternVL3-8B and Aya-Vision-8B")
    assert d2["F1"]["the split may enter"] == "Section 6.10 and the limitations only"
    d8 = S.test_decision({"ov_test_1941": (planted(n, {Q: (0.0, 8.0), I: (0.0, 8.0), AY: (0.0, 8.0)}, seed=5), ids)}, t3, [])
    assert d8["F1"]["row"] == 4 and d8["F1"]["sentence"] == S.SENTENCE[4][0], "none passes: the FAIL sentence"
    # Aya-Vision-8B dropped under the cap (Holm m = 2); InternVL3-8B not entered (Holm m = 1)
    short = {k: v for k, v in per.items() if k != f"{AY}|perm_p2"}
    d3 = S.test_decision({"ov_test_1941": (short, ids)}, t3, [AY])
    assert d3["F1"]["claims"][AY]["words"] == S.CAP_DROP and d3["F1"]["claims"][Q]["holm_m"] == 2
    assert f"Aya-Vision-8B: {S.CAP_DROP}" in d3["F1"]["sentence"], "CC-454 B3: a cap-dropped backbone is named"
    d4 = S.test_decision({"ov_test_1941": (per, ids)}, token(S, [Q, AY]), [])
    assert d4["F1"]["claims"][I]["words"] == S.NOT_ENTERED and d4["F1"]["family"] == [Q, AY]
    # CC-454 B3: Qwen2.5-VL-7B alone entered and passes; Qwen2.5-VL-7B NOT RUN while two others pass
    s9 = S.test_decision({"ov_test_1941": (per, ids)}, token(S, [Q]), [])["F1"]
    assert s9["row"] == 3 and "and not for" not in s9["sentence"], s9["sentence"]
    assert all(f"{nm}: {S.NOT_ENTERED}" in s9["sentence"] for nm in ("InternVL3-8B", "Aya-Vision-8B")), s9["sentence"]
    noq = {k: v for k, v in per.items() if k != f"{Q}|perm_p2"}
    s10 = S.test_decision({"ov_test_1941": (noq, ids)}, t3, [])["F1"]
    assert s10["row"] == 2 and "not for Qwen2.5-VL-7B" not in s10["sentence"], s10["sentence"]
    assert f"Qwen2.5-VL-7B: {S.NOT_DONE.format('arms incomplete')}" in s10["sentence"], s10["sentence"]
    # a flagged placebo changes no label, verdict or sentence
    fl = {**per, f"{Q}|rand_d1": per[f"{Q}|rand_d1"] + 6, f"{Q}|rand_d2": per[f"{Q}|rand_d2"] - 6}
    d5 = S.test_decision({"ov_test_1941": (fl, ids)}, t3, [])
    assert d5["placebo"][f"{Q}|placebo_d1_d2"]["flag"] and not d["placebo"][f"{Q}|placebo_d1_d2"]["flag"]
    assert d5["F1"]["sentence"] == f["sentence"] and all(
        d5["F1"]["claims"][m]["verdict"] == f["claims"][m]["verdict"] and d5["F1"]["claims"][m]["label"] ==
        f["claims"][m]["label"] for m in (Q, I, AY)), "a flag changes no label, verdict or sentence"
    # G5: positive control incomplete on OV-test
    d6 = S.test_decision({"ov_test_1941": ({k: v for k, v in per.items() if k != f"{LM}|lmcap_ri"}, ids)}, t3, [])
    assert d6["positive_control"]["verdict"] == "NOT DETECTED" and d6["F1"]["sentence"].startswith(S.G5_PREFIX)
    assert d6["F1"]["the split may enter"] == "Section 6.10 and the limitations only" and "interpretation" in d6
    # sensitivities on their own index matrix; refusals
    p2 = planted(2001, {Q: (3.0, 8.0), I: (3.0, 8.0), AY: (3.0, 8.0)}, seed=6)
    d7 = S.test_decision({"ov_test_1941": (per, ids), "ov_test_2001": (p2, list(range(2001)))}, t3, [])
    s7 = d7["sensitivities"]["ov_test_2001"]
    assert s7["n"] == 2001 and all(S.SECONDARY in r["labels"] for r in s7["rows"].values())
    assert "four-field" in refused(S.test_decision, {"ov_test_1941": (per, ids)},
                                   {k: v for k, v in t3.items() if k != "yes_log_id"}, [])
    assert "1941" in refused(S.test_decision, {"ov_test_1941": (per, ids[:-1])}, t3, [])


def selftest_batch(S) -> None:
    n = 1941
    ids = [f"t{j:04d}" for j in range(n)]
    per = planted(n, {Q: (3.0, 8.0)}, seed=7, lmcap=None)
    rec = {k: f"v_{k}" for k in S.BATCH_RECORD}
    order = list(np.random.default_rng(2).permutation(n))
    old = [{"model": Q, "arm": arm, "draw": 0, "tau": "-inf", "variant": None,
            "per_image": {"ids": [ids[j] for j in order], "cider_s": [float(per[f"{Q}|{col}"][j]) for j in order]}}
           for arm, col in (("ret", "ret"), ("rand", "rand_d0"))]
    idx = S.boot_idx(n)
    r = S.batch_delta(per, ids, old, rec, rec, Q, idx)
    assert abs(r["d"]) < 1e-12 and r["label"] == "NEGLIGIBLE" and r["reading"] == S.S_BATCH[0], \
        "identical ledgers (paired by id, any order) give Δ_batch = 0"
    assert abs(r["lo"]) < 1e-9 and abs(r["hi"]) < 1e-9, "paired by id: identical ledgers give a zero-width interval"
    assert S.SECONDARY in r["labels"]
    for k in ("annotation_sha256", "kit_sha256", "list_sha256"):
        assert r_status(S.batch_delta(per, ids, old, {**rec, k: "other"}, rec, Q, idx)).startswith("NOT RUN"), k
    assert r_status(S.batch_delta(per, ids, old, {k: v for k, v in rec.items() if k != "jar_sha256"}, rec, Q, idx)) \
        .startswith("NOT RUN")
    tau010 = [{**x, "tau": "0.10"} for x in old]
    assert r_status(S.batch_delta(per, ids, tau010, rec, rec, Q, idx)).startswith("NOT RUN"), "no τ = −∞ row"
    assert r_status(S.batch_delta(per, ids, old + old[:1], rec, rec, Q, idx)).startswith("NOT RUN"), "two ret rows"
    shift = [{**old[0], "per_image": {**old[0]["per_image"], "cider_s": [v + 4 for v in old[0]["per_image"]["cider_s"]]}}, old[1]]
    r4 = S.batch_delta(per, ids, shift, rec, rec, Q, idx)
    assert abs(r4["lo"] + 4) < 1e-9 and abs(r4["hi"] + 4) < 1e-9, "paired by id: a constant shift is the interval"
    assert abs(r4["d"] + 4) < 1e-9 and r4["reading"] == S.S_BATCH[1].format(r4["d"], r4["lo"], r4["hi"])


def r_status(r: dict) -> str:
    return r.get("status", "")


def selftest_plan(S) -> None:
    now = 1_790_000_000.0
    rates = {m: (0.0, S.PLAN_RATE[m]) for m in S.STEP_ORDER}
    full = S.plan("test", rates, now, now + 10 * 86400)
    assert full["dropped"] == [] and full["rc"] == 0 and abs(full["P_h"] - 16.686) < 0.01 and full["time"]["ok"]
    p20 = S.plan("test", rates, now, now + 10 * 86400, ceil_h=20.0)
    assert p20["dropped"] == [AY] and p20["runners"] == [Q, LM, I], "a binding cap drops Aya-Vision-8B first"
    p12 = S.plan("test", rates, now, now + 10 * 86400, ceil_h=12.0)
    assert p12["dropped"] == [AY, I] and p12["runners"] == [Q, LM], "then InternVL3-8B; never LMCap or Qwen2.5-VL-7B"
    p5 = S.plan("test", rates, now, now + 10 * 86400, ceil_h=5.0)
    assert p5["rc"] == 4 and Q in p5["runners"] and LM in p5["runners"], "STOP before T0 rather than drop Qwen or LMCap"
    r20 = S.plan("rehearsal", rates, now, now + 10 * 86400, ceil_h=20.0)
    assert r20["rc"] == 4 and r20["dropped"] == [], "rehearsal: 1.5 P above the ceiling is a STOP"
    assert S.plan("rehearsal", {k: v for k, v in rates.items() if k != Q}, now)["rc"] == 4, "no Qwen D1 PASS: stop"
    t20 = S.plan("test", rates, now, now + 20 * 3600)
    assert t20["rc"] == 5 and "no look spent" in t20["stop"], "a dry run with the freeze 20 hours ahead stops before T0"
    cap_s = full["cap_s"]
    assert not S.timecheck(cap_s, now, now + cap_s + 23 * 3600)["ok"], "X5: the cap plus 24 h, not the cap alone"
    assert S.timecheck(cap_s, now, now + cap_s + 24 * 3600)["ok"], "X5 boundary inclusive"
    vn = datetime(2026, 11, 27, 18, 0, tzinfo=timezone(timedelta(hours=7))).timestamp()
    assert S.G6_TS == vn == calendar.timegm((2026, 11, 27, 11, 0, 0)), "G6 = 2026-11-27 18:00 (UTC+7)"
    saved = S.CLOCK
    try:
        S.CLOCK = lambda: S.G6_TS
        assert "G6" in refused(S.g6_open)
        S.CLOCK = lambda: S.G6_TS - 1
        S.g6_open()
    finally:
        S.CLOCK = saved
    ns = argparse.Namespace(force_ceiling_h=12.0, freeze_utc=S.G6_UTC, dry_run=False)
    assert "dry-run" in refused(S.test_knobs, ns)
    assert "dry-run" in refused(S.test_knobs, argparse.Namespace(freeze_utc="2026-11-20T00:00:00Z", dry_run=False))
    assert S.test_knobs(argparse.Namespace(force_ceiling_h=12.0, freeze_utc=S.G6_UTC, dry_run=True)) == S.G6_TS


def selftest_files(S) -> None:
    with tempfile.TemporaryDirectory() as d:
        dd = Path(d)
        out = dd / "res" / S.DECISION["test"]
        S.once(out)
        S.write_once(out, {"x": 1})
        assert "once per session" in refused(S.once, out)
        refused(S.write_once, out, {"x": 2})
        dec = dd / "R.json"
        dec.write_text(json.dumps({"entered": [Q, AY], "look": True}), encoding="utf-8")
        tok = {"rehearsal_decision_sha256": S.sha(dec), "yes_log_id": "PI-1", "ledger_line_log_id": "OPS-1",
               "backbones": [AY, Q]}
        tp = dd / "T.json"
        tp.write_text(json.dumps(tok), encoding="utf-8")
        assert S.token_ok(tp, dec)["backbones"] == [AY, Q]
        for bad in ({**tok, "rehearsal_decision_sha256": "1" * 64}, {**tok, "backbones": [Q]},
                    {k: v for k, v in tok.items() if k != "ledger_line_log_id"}, {**tok, "yes_log_id": ""},
                    {**tok, "ledger_line_log_id": ""}):
            tp.write_text(json.dumps(bad), encoding="utf-8")
            assert "token" in refused(S.token_ok, tp, dec)
        tp.write_text(json.dumps(tok), encoding="utf-8")
        dec2 = dd / "R2.json"
        dec2.write_text(json.dumps({"entered": [Q, AY], "look": False}), encoding="utf-8")
        tp.write_text(json.dumps({**tok, "rehearsal_decision_sha256": S.sha(dec2)}), encoding="utf-8")
        assert "token" in refused(S.token_ok, tp, dec2), "no token without a licensed look"

    def toy(capt, refs):
        return np.array([float(len(set(capt[i].split()) & set(refs[i][0].split()))) for i in sorted(capt)])
    preds = {"run_id": "p", "predictions": {"a": "x y", "b": "x"}}
    refs = {"a": ["x y z"], "b": ["y"]}
    row = {"run_id": "p", "tau": "-inf", "variant": None, "per_image": {"ids": ["a", "b"], "cider_s": [2.0, 0.0]}}
    assert S.parity_check(preds, [row], toy, refs) == 2
    off = {**row, "per_image": {"ids": ["a", "b"], "cider_s": [2.0, 2e-4]}}
    assert "PARITY FAIL" in refused(S.parity_check, preds, [off], toy, refs)
    assert "PARITY FAIL" in refused(S.parity_check, preds, [row, row], toy, refs)


def spec_of(col: str) -> tuple[str, int]:
    return (col[:4], int(col[-1])) if col.startswith(("rand_d", "perm_p")) else (col, 0)


def stage_tree(d: Path, per: dict, ids: list, ds: str) -> tuple[Path, str]:
    """A pulled output tree: one preds file per planted column and its SHA256SUMS; returns (tree, sums sha256)."""
    t = d / "tree"
    (t / "out").mkdir(parents=True)
    lines = []
    for k in per:
        m, col = k.split("|")
        arm, draw = spec_of(col)
        p = t / "out" / f"cc_{m}_{ds}-{col}.preds.json"
        p.write_text(json.dumps({"run_id": f"{m}-{col}", "spec": {"model": m, "arm": arm, "draw": draw},
                                 "predictions": {i: "x y" for i in ids}}), encoding="utf-8")
        lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  out/{p.name}\n")
    (t / "SHA256SUMS").write_text("".join(lines), encoding="utf-8")
    return t, hashlib.sha256((t / "SHA256SUMS").read_bytes()).hexdigest()


def stub_host(S, sets: dict) -> None:
    """S.A = a stub of c_conf.py whose cmd_score writes the planted columns of each run as ledger rows (stub kit
    scorer); env, parity gate, scored sets and the score2 kit are stubbed too. No study file is read."""
    def cmd_score(ns):
        per, ids = sets[ns.scored_set]
        with open(ns.ledger, "x", encoding="utf-8") as f:
            for p in ns.runs:
                r = json.loads(Path(p).read_text(encoding="utf-8"))
                sp = r["spec"]
                col = sp["arm"] if sp["arm"] in ("zs", "ret") or sp["arm"].startswith("lmcap_") else \
                    f"{sp['arm']}_{'d' if sp['arm'] == 'rand' else 'p'}{sp['draw']}"
                f.write(json.dumps({"run_id": r["run_id"], "scored_set": ns.scored_set, "model": sp["model"],
                                    "arm": sp["arm"], "draw": sp["draw"], "per_image": {
                                        "ids": ids, "cider_s": [float(x) for x in per[f"{sp['model']}|{col}"]]}}) + "\n")

    first = next(iter(sets.values()))[1]
    S.A = types.SimpleNamespace(sha=S.sha, CL="cl", C=types.SimpleNamespace(load_lists=lambda _p: {}),
                                STAGE_SCORE={"uit-openviic-annotation-test.json": "a" * 64}, cmd_score=cmd_score,
                                score_refs=lambda _ds, _l: {i: ["x y z"] for i in first})
    S.env_record = lambda: {"kit_b": {"protocol_pilot.py": "k1", "punctuation_audit.py": "k2", "score2.py": "k3"},
                            "jar_sha256": "j" * 64}
    S.parity_gate = lambda _p, _l: {"result": "ok (stub)"}
    S.scored_sets = lambda _root: {"ov_test_1941": first, "ov_test_2001": "NOT RUN: planted",
                                   "ov_test_1929": "NOT RUN: planted", "ov_test_confirm": "NOT RUN: planted"}
    S.CLOCK = lambda: S.G6_TS - 1

    class Cider:  # every full-df score 0, so the §9 parity with the planted ledger fails
        def __init__(self, refs, df_refs=None):
            self.n = len(refs)

        def per_image(self, hyps):
            return np.zeros(len(hyps))

    kit = types.ModuleType("score2")
    kit.kit2 = lambda _k: (types.SimpleNamespace(rdr=list, Cider=Cider),
                           types.SimpleNamespace(strip_trailing_punct_tokens=lambda t: t), None)
    sys.modules["score2"] = kit


def stage_args(w: Path, t: Path, sums: str, **kw) -> argparse.Namespace:
    base = dict(stage="test", work=w, tree=t, sums=sums, parity_preds=Path("p"), parity_ledger=Path("l"), carve=None,
                carve_sha=None, token=None, rehearsal=None, cap=None, record_old=None, fl_1941=None, fl_2001=None)
    return argparse.Namespace(**{**base, **kw})


def run_stage(S, a) -> dict:
    with contextlib.redirect_stdout(io.StringIO()):
        S.cmd_stage(a)
    return json.loads((Path(a.work) / "res" / S.DECISION[a.stage]).read_text(encoding="utf-8"))


def selftest_stage(S) -> None:
    """CC-454 B2 and B10: 'stage rehearsal' and 'stage test' end to end on synthetic trees (stub kit scorer, stub host
    module): the decision file is written once; a missing S-batch input or a df-sensitivity mismatch gives NOT RUN
    after scoring and never erases the decision; the carve list is checked before scoring; S-batch runs only on a
    pinned record of the first look."""
    with tempfile.TemporaryDirectory() as d:
        dd = Path(d)
        # rehearsal
        n = 2000
        ids = [f"c{j:04d}" for j in range(n)]
        per = planted(n, {Q: (5.0, 8.0), I: (3.0, 8.0), AY: (3.7, 40.0)})
        stub_host(S, {"ov_carve": (per, ids)})
        t, sums = stage_tree(dd / "r", per, ids, "ov_carve")
        carve = dd / "carve.json"
        carve.write_text(json.dumps({"ids": ids}), encoding="utf-8")
        assert "--carve-sha" in refused(S.cmd_stage, stage_args(dd / "w0", t, sums, stage="rehearsal")), "B2 (a)"
        bad = stage_args(dd / "w1", t, sums, stage="rehearsal", carve=carve, carve_sha="0" * 64)
        assert "carve list" in refused(S.cmd_stage, bad) and not (dd / "w1/led/ov_carve.jsonl").exists(), \
            "B2 (b): the carve list is checked before any scoring"
        a = stage_args(dd / "w2", t, sums, stage="rehearsal", carve=carve, carve_sha=S.sha(carve))
        r = run_stage(S, a)
        assert r["entered"] == [Q] and r["look"] and r["record"]["tree"]["files"] == len(per)
        assert "once per session" in refused(S.cmd_stage, a), "the decision file is written once"
        # test: token for Qwen2.5-VL-7B, the 1,941 scored, first-look ledger and record present or not
        n = 1941
        ids = [f"t{j:04d}" for j in range(n)]
        per = planted(n, {Q: (3.0, 8.0)}, seed=5)
        stub_host(S, {"ov_test_1941": (per, ids)})
        t, sums = stage_tree(dd / "t", per, ids, "ov_test")
        reh = dd / "R.json"
        reh.write_text(json.dumps({"entered": [Q], "look": True}), encoding="utf-8")
        tok = dd / "T.json"
        tok.write_text(json.dumps({"rehearsal_decision_sha256": S.sha(reh), "yes_log_id": "PI-x",
                                   "ledger_line_log_id": "OPS-x", "backbones": [Q]}), encoding="utf-8")
        cap = dd / "CAP.json"
        cap.write_text(json.dumps({"dropped": []}), encoding="utf-8")
        assert "--cap" in refused(S.cmd_stage, stage_args(dd / "w3", t, sums, token=tok, rehearsal=reh)) \
            and not (dd / "w3").exists(), "B2 (a): the test stage refuses before scoring without --cap"
        fl = dd / "fl_1941.jsonl"
        fl.write_text("".join(json.dumps({"model": Q, "arm": arm, "draw": 0, "tau": "-inf", "variant": None,
                                          "per_image": {"ids": ids, "cider_s": [float(x) for x in per[f"{Q}|{col}"]]}})
                              + "\n" for arm, col in (("ret", "ret"), ("rand", "rand_d0"))), encoding="utf-8")
        ann = "a" * 64
        same = {nm: {"kit_sha256": {"protocol_pilot.py": "k1", "punctuation_audit.py": "k2"}, "jar_sha256": "j" * 64,
                     "score_field": "cider_s", "annotation_sha256": ann,
                     "list_sha256": S.TEST_LISTS["primary" if nm == "ov_test_1941" else "tsv"][1]}
                for nm in ("ov_test_1941", "ov_test_2001")}
        old = dd / "record_old.json"
        old.write_text(json.dumps(same), encoding="utf-8")
        kw = dict(token=tok, rehearsal=reh, cap=cap)
        # (1) no first-look ledger and no record: decision written, S-batch NOT RUN, df_sensitivity NOT RUN
        r1 = run_stage(S, stage_args(dd / "w4", t, sums, **kw))
        assert str(r1["secondaries"][f"S-batch({Q})"]).startswith("NOT RUN"), r1["secondaries"][f"S-batch({Q})"]
        assert r1["df_sensitivity"]["status"].startswith("NOT RUN: SENSITIVITY PARITY FAIL"), "B2 (d)"
        assert r1["F1"]["claims"][Q]["verdict"] == "PASS" and r1["S-batch on the 2,001 (sensitivity)"] == "NOT RUN"
        assert "once per session" in refused(S.cmd_stage, stage_args(dd / "w4", t, sums, **kw))
        # (2) the pinned first-look ledger and the pinned record: S-batch runs (identical records, Δ_batch = 0)
        S.FL_LEDGER_SHA256 = {"ov_test_1941": S.sha(fl), "ov_test_2001": "0" * 64}
        S.RECORD_OLD_SHA256 = S.sha(old)
        r2 = run_stage(S, stage_args(dd / "w5", t, sums, record_old=old, fl_1941=fl, **kw))
        b2 = r2["secondaries"][f"S-batch({Q})"]
        assert isinstance(b2, dict) and b2.get("label") == "NEGLIGIBLE" and abs(b2["d"]) < 1e-9, b2
        # (3) a record that is not the pinned file: S-batch NOT RUN (B10)
        S.RECORD_OLD_SHA256 = "0" * 64
        r3 = run_stage(S, stage_args(dd / "w6", t, sums, record_old=old, fl_1941=fl, **kw))
        assert r3["secondaries"][f"S-batch({Q})"]["status"].startswith("NOT RUN"), "an unpinned record: NOT RUN"
        S.RECORD_OLD_SHA256 = None
        r4 = run_stage(S, stage_args(dd / "w7", t, sums, record_old=old, fl_1941=fl, **kw))
        assert r4["secondaries"][f"S-batch({Q})"]["status"].startswith("NOT RUN"), "no record of record: NOT RUN"


def selftest(S) -> None:
    selftest_stats(S)
    selftest_rows(S)
    selftest_rehearsal(S)
    selftest_test(S)
    selftest_batch(S)
    selftest_plan(S)
    selftest_files(S)
    selftest_stage(S)


MUTANTS = [  # §11.1 row c_conf_score.py, then CC-450 J1 N1 and X5, then the guards
    ("margin compared with 2.0", "    return d >= MARGIN", "    return d >= SESOI"),
    ("margin > in place of >=", "    return d >= MARGIN", "    return d > MARGIN"),
    ("resample size 2,000", "integers(0, CARVE_N, (BOOT, TEST_N))", "integers(0, CARVE_N, (BOOT, CARVE_N))"),
    ("P_m without the Holm term", "ok = (means >= SESOI) & (means / se >= Z_HOLM3)", "ok = means >= SESOI"),
    ("entry by any", 'if c["carve_pass"] and c["share_ok"] and c["margin_ok"]', 'if c["carve_pass"] or c["share_ok"] or c["margin_ok"]'),
    ("primary-backbone requirement dropped", 'look = PRIMARY in entered and pc == "DETECTED"', 'look = bool(entered) and pc == "DETECTED"'),
    ("incomplete control read as DETECTED", 'return "DETECTED" if r is not None and detected', 'return "DETECTED" if r is None or detected'),
    ("a flag that changes a verdict", "tested = [m for m in entered if complete(per, m)]",
     'tested = [m for m in entered if complete(per, m) and not rows[f"{m}|placebo_d1_d2"]["flag"]]'),
    ("a secondary row without its label", "    if not f1:\n        tags.append(SECONDARY)", "    if False:\n        tags.append(SECONDARY)"),
    ("Δ_batch with unpaired ids", 'was = np.array([old["ret"][i] - old["rand"][i] for i in ids], float)',
     'was = np.array(list(old["ret"].values()), float) - np.array(list(old["rand"].values()), float)'),
    ("Δ_batch on a differing annotation sha256", '"score_field", "annotation_sha256", "list_sha256")', '"score_field", "list_sha256")'),
    ("draw 0 in place of the draw mean", 'return np.mean([per[f"{m}|{c}"] for c in cols], axis=0)', 'return per[f"{m}|{cols[0]}"]'),
    ("a fresh index matrix per contrast", 'rows[f"{m}|{est}"] = {**pair(a, b, idx), "model": m, "estimand": est, "R": 3',
     'rows[f"{m}|{est}"] = {**pair(a, b, boot_idx(len(a), 1 + len(rows))), "model": m, "estimand": est, "R": 3'),
    ("≥ and > swapped in a label", 'if s["lo90"] > -SESOI and s["hi90"] < SESOI:', 'if s["lo90"] >= -SESOI and s["hi90"] <= SESOI:'),
    ("ties in p broken by backbone key", "key=lambda kv: (kv[1][1], -kv[1][0], kv[0])", "key=lambda kv: (kv[1][1], kv[0])"),
    ("time check without the 24 h", "ok = left >= cap_s + PULL_SCORE_S", "ok = left >= cap_s"),
    ("drop order swapped", 'DROP_ORDER = ("aya_vision_8b", "internvl3_8b")', 'DROP_ORDER = ("internvl3_8b", "aya_vision_8b")'),
    ("dry-run knobs outside a dry run", 'and not a.dry_run:\n        raise SystemExit("REFUSED: --force-ceiling-h', 'and False:\n        raise SystemExit("REFUSED: --force-ceiling-h'),
    ("second scoring call admitted", "    if out.exists():\n        raise SystemExit(f\"REFUSED: {out.name} exists; the scorer",
     "    if False:\n        raise SystemExit(f\"REFUSED: {out.name} exists; the scorer"),
    ("token check skipped", 'or not t["ledger_line_log_id"]:', 'or False:'),
    ("parity tolerance widened", "PARITY_TOL = 1e-4", "PARITY_TOL = 1e-3"),
    ("untested backbones not named in the sentence (CC-454 B3)",
     '    if untested:\n        s += "; " + "; ".join(f"{NAME[m]}: {w}" for m, w in sorted(untested.items()))\n', ""),
    ("S-batch on an unpinned record (CC-454 B10)", " and sha(a.record_old) == RECORD_OLD_SHA256", ""),
]


def main() -> None:
    selftest(load(SRC))
    print("self-test PASS")
    src = SRC.read_text(encoding="utf-8")
    alive = []
    with tempfile.TemporaryDirectory() as d:
        for k, (name, old, new) in enumerate(MUTANTS):
            assert src.count(old) == 1, f"mutant anchor not found once: {name}"
            p = Path(d) / f"m_{k}.py"
            p.write_text(src.replace(old, new).replace("ROOT = Path(__file__).resolve().parents[2]",
                                                       f"ROOT = Path({str(SRC.parents[2])!r})"), encoding="utf-8")
            try:
                selftest(load(p))
                alive.append(name)
            except Exception:  # noqa: BLE001  any failure kills the mutant
                pass
    print(f"mutants: {len(MUTANTS) - len(alive)} of {len(MUTANTS)} killed")
    assert not alive, f"mutants alive: {alive}"


if __name__ == "__main__":
    main()
