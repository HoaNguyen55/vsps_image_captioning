#!/usr/bin/env python
"""CPU selftest for scripts/vsps_j_e2b/e2b_1c.py (TIER1C O1 §9 T1-T5, CC-233r2 NB1-NB4). Synthetic fixtures only:
no weights, no data file, no real runs folder, no network (every socket raises).

    <venv with numpy> -I scripts/vsps_j_e2b/test_e2b_1c.py
"""
from __future__ import annotations

import builtins
import contextlib
import io
import json
import math
import random
import socket
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


_no_net = mock.Mock(side_effect=OSError("selftest: network blocked"))
socket.socket = socket.create_connection = socket.getaddrinfo = _no_net  # type: ignore[assignment,misc]
patched = mock.patch.multiple  # patched(obj, name=value, ...) as a context manager


def raises(exc, fn) -> None:
    try:
        fn()
    except exc:
        return
    raise AssertionError(f"{exc.__name__} not raised")

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import e2b  # noqa: E402
import e2b_1c as X  # noqa: E402
import m0  # noqa: E402

BASE = 9_400_000  # synthetic image ids, far above every COCO id
GRID = e2b.GRID
clamp = lambda v: min(0.999, max(0.001, v))  # noqa: E731
rows_of = e2b.per_image_counts


def toy(n_img=80, seed=20261121, gap_e=0.42, gap_v=0.22, e_const=None):
    """Synthetic probes: per segment a gold flag y (1 = gold false), an E2b F-A p and a Vintern p_yes."""
    rng = random.Random(seed)
    segs, mass, pv = [], {}, {}
    for i in range(n_img):
        img = BASE + i
        for j in range(rng.randint(8, 14)):
            y = int(rng.random() < 0.35)
            s = {"rec": img, "seg": j, "image": img, "y": y, "t2": e2b.TYPES[j % 6], "half": e2b.half(img)}
            pe = e_const if e_const is not None else clamp(rng.gauss(0.5 - gap_e if y else 0.5 + 0.9 * gap_e, 0.1))
            mass[e2b.key(s)] = {"yes": 0.9 * pe, "no": 0.9 * (1 - pe)}
            pv[e2b.key(s)] = clamp(rng.gauss(0.5 - gap_v if y else 0.5 + gap_v, 0.18))
            segs.append(s)
    return segs, mass, pv


def labels(segs, mass, pv, tE=(0.4, 0.6), tV=(0.4, 0.6)):
    fE = lambda s: e2b.band_label(e2b.fa_p(mass[e2b.key(s)]), *tE)  # noqa: E731
    fV = lambda s: e2b.band_label(pv[e2b.key(s)], *tV)  # noqa: E731
    return fE, fV


# ------------------------------------------------------------------------------------------------ T1 fit_1c
def one_type_rows(t, spec, half="tune", start=0):
    """spec: list of (y, pE, pV, count) -> synthetic segments of type t."""
    out, mass, pv, k = [], {}, {}, start
    for y, pe, pV, c in spec:
        for _ in range(c):
            s = {"rec": BASE + k, "seg": 0, "image": BASE + k, "y": y, "t2": t, "half": half}
            mass[e2b.key(s)], pv[e2b.key(s)] = pe, pV
            out.append(s)
            k += 1
    return out, mass, pv


def fit_spec(extra=()):
    """object: 100 gold-false, 100 gold-true. Vintern p for false 83 x 0.08 (band -> GRID 0.10, recall 0.83), 17 x
    0.90; true 0.97. E2b false 80 x 0.05, 5 x 0.27, 15 x 0.70; true 0.97. k_V 83, k* 85: the 0.05-GRID t_lo is 0.30
    (an exact hit of 85), a 0.01 grid would give 0.27."""
    spec = [(1, 0.05, 0.08, 80), (1, 0.27, 0.08, 3), (1, 0.27, 0.90, 2), (1, 0.70, 0.90, 15), (0, 0.97, 0.97, 100)]
    segs, mass, pv = one_type_rows("object", spec)
    num, m2, p2 = one_type_rows("number", spec, start=1000)
    segs, mass, pv = segs + num, {**mass, **m2}, {**pv, **p2}
    for t, sp, half in extra:
        s3, m3, p3 = one_type_rows(t, sp, half=half, start=5000 + len(segs))
        segs, mass, pv = segs + s3, {**mass, **m3}, {**pv, **p3}
    return segs, (lambda s: mass[e2b.key(s)]), (lambda s: pv[e2b.key(s)])


def test_T1_fit_1c():
    assert X.k_target(83, 100) == 85 and X.k_target(0, 698) == 14 and X.k_target(10, 50) == 11
    assert X.k_target(0, 100) == 2 and X.k_target(0, 1) == 1
    segs, pE, pV = fit_spec()
    thrE, thrV, info, why = X.fit_1c(pE, pV, segs)
    o = info["object"]
    assert (o["n_f"], o["k_V"], o["k_star"], o["kE"]) == (100, 83, 85, 85), o
    assert thrV["object"][0] == 0.10 and thrV["object"] == e2b.band([pV(s) for s in segs if s["t2"] == "object"],
                                                                    [s["y"] for s in segs if s["t2"] == "object"])
    assert thrE["object"][0] == 0.30 and thrE["object"][0] in GRID, thrE  # exact hit accepted; registered GRID
    tu = [s for s in segs if s["t2"] == "object"]
    assert thrE["object"][1] == e2b.hi_rule([pE(s) for s in tu], [s["y"] for s in tu], 0.30)
    assert o["feasible"] and not why
    # select rows with extreme values never move a tune-fit threshold
    segs2, pE2, pV2 = fit_spec(extra=[("object", [(1, 0.01, 0.01, 300), (0, 0.02, 0.99, 50)], "select")])
    t2E, t2V, info2, _ = X.fit_1c(pE2, pV2, segs2)
    assert (t2E["object"], t2V["object"], info2["object"]["k_star"]) == (thrE["object"], thrV["object"], 85)
    # unreachable k*: E2b never rejects -> infeasible, no fallback on a primary type
    _, _, info3, why3 = X.fit_1c(lambda s: 0.99 if s["t2"] == "number" else pE(s), pV, segs)
    assert not info3["number"]["feasible"] and "unreachable" in info3["number"]["reason"]
    assert info3["object"]["feasible"] and len(why3) == 1 and why3[0].startswith("number:")
    # Vintern band with no feasible t_lo -> infeasible
    _, _, info4, why4 = X.fit_1c(pE, lambda s: 0.99, segs)
    assert not info4["object"]["feasible"] and "Vintern" in info4["object"]["reason"] and len(why4) == 2
    # a descriptive type that cannot reach k* takes the registered (0.5, 0.5) and is not a reason
    segs5, pE5, pV5 = fit_spec(extra=[("colour", [(1, 0.99, 0.05, 20), (0, 0.99, 0.97, 20)], "tune")])
    t5E, _, info5, why5 = X.fit_1c(pE5, pV5, segs5)
    assert t5E["colour"] == (0.5, 0.5) and not info5["colour"]["feasible"] and not why5


# ------------------------------------------------------------------------------------------------ T2 rules_pass
def test_T2_rules_pass():
    p = {"dprec": 5.0, "U": 15.0, "dret": 1.0, "drecall": 1.0}
    ci = {"dprec": [0.1, 9.0], "U": [0, 0], "dret": [-1.9, 3.0], "drecall": [-1.9, 3.0]}
    assert X.rules_pass(p, ci)
    assert not X.rules_pass({**p, "dprec": 4.999}, ci)
    assert not X.rules_pass(p, {**ci, "dprec": [0.0, 9.0]})
    assert not X.rules_pass({**p, "U": 15.001}, ci)
    assert not X.rules_pass(p, {**ci, "dret": [-2.0, 3.0]})
    assert not X.rules_pass(p, {**ci, "drecall": [-2.0, 3.0]})
    assert X.rules_pass(p, {**ci, "drecall": [-1.9999, 3.0]})
    assert not X.rules_pass({**p, "dprec": float("nan")}, ci)
    assert 490 / 500 >= X.PASS_GATE  # the gate is >=; 490/500 rounds to the double of 0.98


# ------------------------------------------------------------------------------------------------ T3 ppass
def strong_rows():
    segs, mass, pv = toy(n_img=60)
    fE = lambda s: "R" if s["y"] else "S"  # noqa: E731
    fV = lambda s: "R" if (s["y"] and s["rec"] % 2) or (not s["y"] and s["seg"] % 3 == 0) else "S"  # noqa: E731
    return rows_of(segs, fE, fV), segs, fE, fV


def test_T3_ppass():
    rows, segs, fE, fV = strong_rows()
    pt = X.point_from_rows(rows)
    E, V = e2b.table(fE, segs), e2b.table(fV, segs)
    for k, m in (("dprec", "prec_R"), ("dret", "retention"), ("drecall", "recall")):
        assert abs(pt[k] - e2b.macro_pair(E, V, m)[0]) < 1e-9, (k, pt[k])
    assert abs(pt["U"] - e2b.macro(E, "U")) < 1e-9
    r = X.ppass(rows, n_t3=200, B_out=30, B_in=200, seed=7)
    assert r["p_hat"] == 1.0 and r["n_pass"] == 30 and r["mc_se"] == 0.0 and r["n_undefined"] == r["n_inner_fault"] == 0
    weak = rows_of(segs, lambda s: "R" if s["y"] and s["rec"] % 3 == 0 else "S", lambda s: "R" if s["y"] else "S")
    r0 = X.ppass(weak, n_t3=200, B_out=30, B_in=200, seed=7)
    assert r0["p_hat"] == 0.0 and r0["n_undefined"] == 0
    mid = rows_of(segs, lambda s: "R" if s["y"] and s["seg"] % 4 else "S", lambda s: "R" if s["y"] else "S")
    a1, a2 = (X.ppass(mid, n_t3=120, B_out=40, B_in=200, seed=11) for _ in range(2))
    assert a1 == a2  # seeded
    p = a1["p_hat"]
    assert abs(a1["mc_se"] - math.sqrt(p * (1 - p) / 40)) < 1e-12
    # an undefined outer point (E2b never rejects object) is not passing and is counted
    und = rows_of(segs, lambda s: "R" if s["y"] and s["t2"] != "object" else "S", fV)
    ru = X.ppass(und, n_t3=100, B_out=12, B_in=100, seed=3)
    assert ru["n_undefined"] == 12 and ru["p_hat"] == 0.0
    # predictive variant: same keys, pre fields recorded
    rp = X.ppass(rows, n_t3=150, B_out=10, B_in=100, seed=7, pre_n=len(rows), pre_seed=5)
    assert rp["pre_n"] == len(rows) and rp["pre_seed"] == 5 and rp["p_hat"] == 1.0
    raises(ValueError, lambda: X.ppass(rows, n_t3=10, B_out=1, B_in=10, pre_n=5))  # no unseeded predictive draw
    # deadline in the past -> CapStop, never a partial result
    raises(X.CapStop, lambda: X.ppass(rows, n_t3=50, B_out=5, B_in=50, seed=1, deadline=time.monotonic() - 1))


def test_T3_nb3_inner_drop():
    """CC-233r2 NB3: exactly 1 % + 1 inner replicates dropped -> that outer replicate is not passing (counted), and
    the screen never aborts; exactly 1 % dropped is still allowed."""
    import numpy as np

    rows = strong_rows()[0]
    real = e2b.ci_from_table

    def fake(k):
        def f(T, B, seed):
            st = {"dprec": np.full(B, 20.0), "U": np.zeros(B), "dret": np.full(B, 5.0), "drecall": np.full(B, 5.0)}
            bad = np.zeros(B, dtype=bool)
            bad[:k] = True
            return st, bad
        return f

    try:
        e2b.ci_from_table = fake(11)
        r = X.ppass(rows, n_t3=100, B_out=6, B_in=1000, seed=1)
        assert r["n_inner_fault"] == 6 and r["p_hat"] == 0.0, r
        e2b.ci_from_table = fake(10)
        r = X.ppass(rows, n_t3=100, B_out=6, B_in=1000, seed=1)
        assert r["n_inner_fault"] == 0 and r["p_hat"] == 1.0, r
    finally:
        e2b.ci_from_table = real


def test_T3_nb1_timing():
    """CC-233r2 NB1: one outer replicate on a 1,004 x 20 toy, projected to the screen's 2 x 500 replicates."""
    import numpy as np

    rows = np.asarray(strong_rows()[0], dtype=float)
    big = rows[np.random.default_rng(0).integers(0, len(rows), 1004)]
    assert big.shape == (1004, 20)
    t0 = time.perf_counter()
    X.ppass(big, n_t3=X.N_SCREEN, B_out=3, B_in=X.B_IN, seed=1)
    per = (time.perf_counter() - t0) / 3
    proj = per * 2 * X.B_OUT
    print(f"TIMING one outer replicate {per:.3f} s; screen projection {proj / 60:.1f} min of the {X.CPU_CAP_H:.0f} h cap")
    assert proj < 0.5 * X.CPU_CAP_H * 3600, proj


# ------------------------------------------------------------------------------------------------ T4 K1 equality
GOLDEN = {"B": 2000, "seed": 20261101, "dropped": 0,  # pre-K1 paired_ci output (e2b.py d3aa5384), this fixture
          "dprec": [0.0, 8.2284946236559], "U": [60.18908023747979, 71.77470744280554],
          "dret": [-37.16838108954922, -18.57339588377724], "drecall": [-42.83602872698617, -17.988257409549647]}


def test_T4_k1_golden():
    s, m, p = toy(n_img=70, seed=20261131, gap_e=0.25)
    rows = rows_of(s, *labels(s, m, p, tE=(0.2, 0.75), tV=(0.35, 0.65)))
    got = e2b.paired_ci(rows, B=2000)
    for k, v in GOLDEN.items():
        if isinstance(v, list):
            assert all(abs(a - b) < 1e-12 for a, b in zip(got[k], v)), (k, got[k], v)
        else:
            assert got[k] == v, (k, got[k], v)
    st, bad = e2b.ci_from_table(rows, 2000, e2b.SEED)
    assert len(bad) == 2000 and int(bad.sum()) == got["dropped"] and set(st) == set(X.KEYS)


# ------------------------------------------------------------------------------------------------ T5 run_screen
def write_cell(d: Path, segs, mass):
    d.mkdir(parents=True)
    pf = d / "probes.jsonl"
    pf.write_text("".join(json.dumps({"rec": s["rec"], "seg": s["seg"], "mass": mass[e2b.key(s)]}) + "\n"
                          for s in segs), encoding="utf-8")
    (d / "probes.jsonl.sha256").write_text(f"{m0.sha_file(pf)}  probes.jsonl\n")
    return m0.sha_file(pf)


def fake_world(tmp: Path, e_const=None):
    segs, mass, pv = toy(n_img=80, e_const=e_const)
    held = {BASE + i for i in range(8)}
    S = {"sel": {s["image"] for s in segs} - held, "held": held}
    runs = tmp / "runs"
    psha = write_cell(runs / "internvl3_8b_FA_vi", segs, mass)  # literal: the registered winner cell
    write_cell(runs / "qwen3vl_8b_FA_vi", segs, mass)  # traps: never opened
    write_cell(runs / "internvl3_8b_FA_en", segs, mass)
    res = tmp / "res.json"
    res.write_text(json.dumps({"winner": X.WINNER, "configs": {X.WINNER: {"dprec": 7.0, "U": 3.0, "dret": 15.0,
                                                                          "drecall": -2.5}},
                               "winner_ci_select": {"dprec": [5.0, 9.0]}}))
    (runs / "SCORED.json").write_text(json.dumps({"res_sha256": m0.sha_file(res)}))
    n_sel = len({s["image"] for s in segs if s["image"] in S["sel"] and s["half"] == "select"})
    pins = {"RES_SHA": m0.sha_file(res), "SCORED_SHA": m0.sha_file(runs / "SCORED.json"),
            "WIN_PROBES_PREFIX": psha[:8], "N_SELECT": n_sel}
    a = SimpleNamespace(runs=runs, res=res, probes_sha=psha, copy_to=tmp / "copy", data=None, m0_probes=None)
    return a, (lambda _a: (S, segs, pv)), pins, n_sel, held


@contextlib.contextmanager
def open_spy(seen: list):
    real = builtins.open

    def spy(p, *a, **k):
        seen.append(str(p))
        return real(p, *a, **k)
    with patched(builtins, open=spy), patched(io, open=spy):
        yield


def refused(fn) -> str:
    try:
        fn()
    except SystemExit as e:
        return str(e)
    except Exception as e:  # e.g. FileExistsError from O_EXCL: the preflight did not refuse
        raise AssertionError(f"not refused by the preflight ({type(e).__name__})") from e
    raise AssertionError("not refused")


def no_load(_a):
    raise AssertionError("data read before the once-guard refused")


def test_T5_screen_go_path_and_guards():
    calls, order, seen = [], [], []

    def ppass_spy(rows, **kw):
        calls.append((len(rows), kw))
        return {"p_hat": 0.0 if kw.get("pre_n") else 0.98, "mc_se": 0.0, "n_pass": 0}

    real_w = X.write_excl

    def w_spy(p, text):
        order.append(p.name)
        real_w(p, text)

    with tempfile.TemporaryDirectory() as td:
        a, load, pins, n_sel, held = fake_world(Path(td))
        out = io.StringIO()
        with patched(X, ppass=ppass_spy, write_excl=w_spy, **pins), open_spy(seen), contextlib.redirect_stdout(out):
            assert X.run_screen(a, load) == 0
        # decision call: the registered screen parameters, select rows only; predictive is descriptive
        (n1, k1), (n2, k2) = calls
        assert n1 == n2 == n_sel and k1["n_t3"] == 1004 and k1["B_out"] == 500 and k1["B_in"] == 1000
        assert k1["seed"] == 20261102 and not k1.get("pre_n") and k2["pre_seed"] == 20261105 and k2["pre_n"] == n_sel
        assert not any("qwen3vl_8b_FA_vi" in p or "_FA_en" in p for p in seen), "a non-winner folder was opened"
        assert order == [X.RES_NAME, X.GUARD_NAME], order
        r = json.loads((a.runs / X.RES_NAME).read_text())
        assert r["screen"] == "SCREEN GO" and r["label"] == X.LABEL_1C and r["post_hoc"] is True  # 0.98 is a GO
        for t in e2b.PRIMARY:  # NB4
            assert {"k_V", "k_star", "kE", "n_f", "feasible", "reason"} <= set(r["fit"][t]) and r["fit"][t]["k_star"]
        assert r["held_report_only"]["n_images"] == len(held) and list(r)[-1] == "held_report_only"
        g = json.loads((a.runs / X.GUARD_NAME).read_text())
        assert g["res_1c_sha256"] == m0.sha_file(a.runs / X.RES_NAME) == m0.sha_file(a.copy_to / X.RES_NAME)
        lines = out.getvalue().strip().splitlines()  # NB2: one line, after the files exist, no P-hat
        assert len(lines) == 1 and "p_hat" not in lines[0] and "SCREEN GO" in lines[0], lines
        # once-guard: a second run is refused before any data read
        with patched(X, ppass=ppass_spy, **pins):
            assert "exists" in refused(lambda: X.run_screen(a, no_load))
        # orphan res_1c.json without a guard is refused too
        (a.runs / X.GUARD_NAME).chmod(0o644)
        (a.runs / X.GUARD_NAME).unlink()
        with patched(X, ppass=ppass_spy, **pins):
            assert X.RES_NAME in refused(lambda: X.run_screen(a, no_load))


def test_T5_refusals_infeasible_cap():
    stub = lambda rows, **kw: {"p_hat": 1.0}  # noqa: E731
    with tempfile.TemporaryDirectory() as td:
        a, load, pins, _, _ = fake_world(Path(td))
        with patched(X, ppass=stub, **{**pins, "RES_SHA": "0" * 64}):
            assert "res.json" in refused(lambda: X.run_screen(a, load))
        with patched(X, ppass=stub, **{**pins, "SCORED_SHA": "0" * 64}):
            assert "SCORED" in refused(lambda: X.run_screen(a, load))
        with patched(X, ppass=stub, **{**pins, "WIN_PROBES_PREFIX": "ffffffff"}):
            assert "probes-sha" in refused(lambda: X.run_screen(a, load))
        with patched(X, ppass=stub, **{**pins, "N_SELECT": pins["N_SELECT"] + 1}):
            assert "select half" in refused(lambda: X.run_screen(a, load))
        cap_out = io.StringIO()  # the real ppass hits the past deadline first (NB2: no figure in the printed line)
        with patched(X, CPU_CAP_H=-1.0, **pins), contextlib.redirect_stdout(cap_out):
            assert X.cmd_screen_1c(a, load) == 4  # wall cap: no outcome written
        assert not any(ch.isdigit() for ch in cap_out.getvalue()), cap_out.getvalue()
        assert not (a.runs / X.RES_NAME).exists() and not (a.runs / X.GUARD_NAME).exists()
    with tempfile.TemporaryDirectory() as td:  # INFEASIBLE: E2b p above the GRID for every probe
        a, load, pins, _, _ = fake_world(Path(td), e_const=0.97)
        called = []
        with patched(X, ppass=lambda rows, **kw: called.append(1), **pins), contextlib.redirect_stdout(io.StringIO()):
            assert X.run_screen(a, load) == 0
        r = json.loads((a.runs / X.RES_NAME).read_text())
        assert r["screen"] == "INFEASIBLE" and not called and "decision" not in r
        assert len(r["infeasible_reasons"]) == 2 and all("unreachable" in w for w in r["infeasible_reasons"])
        assert all(r["fit"][t]["reason"] for t in e2b.PRIMARY)


def test_T5_end_to_end_small():
    """The real ppass and paired_ci inside run_screen, with small B (integration only)."""
    with tempfile.TemporaryDirectory() as td:
        a, load, pins, n_sel, _ = fake_world(Path(td))
        with patched(X, B_OUT=8, B_IN=60, **pins), contextlib.redirect_stdout(io.StringIO()):
            assert X.run_screen(a, load) == 0
        r = json.loads((a.runs / X.RES_NAME).read_text())
        assert r["screen"] in ("SCREEN GO", "SCREEN NO-GO") and 0.0 <= r["decision"]["p_hat"] <= 1.0
        assert r["decision"]["n_t3"] == 1004 and r["select"]["n_images"] == n_sel
        assert r["predictive_descriptive"]["pre_n"] == n_sel and "dprec" in r["select"]["paired_ci"]


def _no_real_data(*_a, **_k):
    raise AssertionError("selftest reached the real data loader")


def main() -> int:
    X.real_loader = _no_real_data  # synthetic fixtures only: the real loader must never run here
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
    try:
        socket.create_connection(("example.org", 443))
    except OSError:
        print("PASS network blocked during the selftest")
    print(f"selftest OK ({len(tests)} tests)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
