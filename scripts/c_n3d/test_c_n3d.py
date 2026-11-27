"""Synthetic self-tests and mutants for c_n3d.py (prereg v3 §10 step 1). Opens no input; planted toy cells only.

  python3 -I test_c_n3d.py          all tests on the module as written, then every mutant must be killed
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SRC = (HERE / "c_n3d.py").read_text(encoding="utf-8")
HSRC = (HERE / "c_n3d_host.py").read_text(encoding="utf-8")


def load(src: str = SRC) -> types.ModuleType:
    mod = types.ModuleType("c_n3d")
    mod.__file__ = str(HERE / "c_n3d.py")
    sys.modules["c_n3d"] = mod  # dataclasses resolve annotations through sys.modules
    exec(compile(src, "c_n3d.py", "exec"), mod.__dict__)
    return mod


def load_host(src: str = HSRC) -> types.ModuleType:
    """c_n3d_host bound to the c_n3d now in sys.modules (its instrument imports are inside functions)."""
    mod = types.ModuleType("c_n3d_host")
    mod.__file__ = str(HERE / "c_n3d_host.py")
    sys.modules["c_n3d_host"] = mod
    exec(compile(src, "c_n3d_host.py", "exec"), mod.__dict__)
    return mod


# ------------------------------------------------------------------------------------------------ planted cells
def first(n: int, idx, p: float) -> np.ndarray:
    """bool[n], True on the first round(p * len(idx)) members of idx."""
    out = np.zeros(n, bool)
    idx = list(idx)
    out[idx[:round(p * len(idx))]] = True
    return out


N_OV = 925
L_IDX, W_IDX = range(0, 200), range(200, 600)
PM_IDX, PP_IDX = range(100, 400), range(400, 700)


def planted(N, bo=(0.6, 0.1, 0.2, 0.2), zl=(0.8, 0.3, 0.3, 0.3), n=N_OV, sizes=None) -> "N.Cell":
    """d: L -> -20, W -> +20; e: P- -> -20, P+ -> +20. Flag rates (in L, in W, in P-, in P+) for ret (L, W) and
    rand d1 (P-, P+); CP and LN never hold, so OTHER = not BO and not ZL."""
    li, wi, pm, pp = (L_IDX, W_IDX, PM_IDX, PP_IDX) if sizes is None else sizes
    d, e = np.zeros(n), np.zeros(n)
    d[list(li)], d[list(wi)] = -20.0, 20.0
    e[list(pm)], e[list(pp)] = -20.0, 20.0
    z = np.zeros(n, bool)

    def arm(rates_a, rates_b, ga, gb):
        return {"BO": first(n, ga, rates_a[0]) | first(n, gb, rates_a[1]),
                "ZL": first(n, ga, rates_b[0]) | first(n, gb, rates_b[1]), "CP": z.copy(), "LN": z.copy()}
    f_ret = arm(bo[:2], zl[:2], li, wi)
    f_d1 = arm(bo[2:], zl[2:], pm, pp)
    f_d0 = {k: z.copy() for k in N.FLAGS}
    return N.Cell(d=d, e=e, f_ret=f_ret, f_d0=f_d0, f_d1=f_d1, f_d2={k: z.copy() for k in N.FLAGS})


def family(N, cells) -> list[dict]:
    idx = N.index_matrices()["ov_dev_b"]
    rows = []
    for c in cells:
        a = N.analyse(c, idx)
        rows += [N.h_row(h, a["_pt"], a["_boot"]) for h in ("H1", "H2", "H3")]
    return N.family_verdicts(rows)


# ------------------------------------------------------------------------------------------------ tests
def suite(N, H=None) -> list[str]:
    """Every check; returns the names of the failed ones (empty = all pass)."""
    bad: list[str] = []
    H = H or load_host()

    def check(name: str, cond) -> None:
        try:
            ok = bool(cond() if callable(cond) else cond)
        except (Exception, SystemExit):  # noqa: BLE001  a mutant that raises is a failed check
            ok = False
        if not ok:
            bad.append(name)

    # bootstrap matrices: one generator, three calls in the registered order
    def rng_ok():
        g = np.random.default_rng(1127001)
        want = [g.integers(0, n, (2000, n)) for n in (925, 500, 1000)]
        got = N.index_matrices()
        return list(got) == ["ov_dev_b", "xm_dev500", "f30k_carve"] and all(
            np.array_equal(got[k], w) for k, w in zip(got, want))
    check("rng", rng_ok)
    check("ptilde", lambda: abs(N.ptilde(np.array([-1.0, 0.0, 1.0, 2.0]), 0.0) - 3 / 5) < 1e-12)
    check("ptilde_nan", lambda: abs(N.ptilde(np.array([np.nan, 5.0, 5.0, 5.0]), 0.0) - 2 / 5) < 1e-12)
    check("holm", lambda: np.allclose(N.holm([0.01, 0.04, 0.03, 0.005, 0.5, 1.0]),
                                      [0.05, 0.12, 0.12, 0.03, 1.0, 1.0]))
    check("holm_monotone", lambda: np.allclose(N.holm([0.01, 0.011]), [0.02, 0.02]))
    # categories: precedence CP > BO > ZL > LN > OTHER, and SR6 reversed
    fl = {"CP": np.array([1, 0, 0, 0, 0, 1], bool), "BO": np.array([1, 1, 0, 0, 0, 0], bool),
          "ZL": np.array([0, 1, 1, 0, 0, 1], bool), "LN": np.array([0, 0, 1, 1, 0, 1], bool)}
    check("category", lambda: N.category(fl).tolist() == [0, 1, 2, 3, 4, 0])
    check("category_rev", lambda: N.category(fl, N.PREC_REV).tolist() == [1, 2, 3, 3, 4, 3])

    # flags with toy instruments: classes = words in a vocabulary
    voc = {"dog", "cat", "car", "tree", "man"}
    copy = {"copy": 0.90, "near": 0.8999}
    inst = N.Instruments(classes=lambda t: [w for w in t.split() if w in voc], key=lambda o: o,
                         copy_m=lambda cap, shown: copy.get(cap.split()[0], 0.0), length=lambda t: len(t.split()))
    st = {"dog": "present", "cat": "absent", "car": "absent", "tree": "present", "man": "present"}.get
    check("neighbour_only", lambda: inst.neighbour_only("near dog cat car", "near dog", ["a cat", "a tree"]) == ["cat"])
    f1 = N.flags_of(inst, "copy dog cat x", "copy dog tree", ["a cat"], st, 4.0)
    check("flags_BO", lambda: f1["BO"])
    check("flags_CP_at_0.90", lambda: f1["CP"])
    check("flags_ZL", lambda: f1["ZL"])                       # tree: present in zs, supported, dropped
    check("flags_LN_below", lambda: not f1["LN"])              # 4 words vs median 4
    f2 = N.flags_of(inst, "near dog tree man w", "near dog tree", ["a man"], st, 4.0)
    check("flags_BO_supported_not_BO", lambda: not f2["BO"])   # man is neighbour-only but present
    check("flags_CP_below", lambda: not f2["CP"])
    check("flags_ZL_kept", lambda: not f2["ZL"])
    check("flags_LN_at_0.25", lambda: N.flags_of(inst, "a b c d e", "x", [], st, 4.0)["LN"])   # |5 - 4| = 0.25 * 4

    # groups: strict margins (d = -10 is not a loser; e = +10 is not a placebo winner)
    def margin_ok():
        c = planted(N)
        c.d[600:610], c.e[700:710] = -10.0, 10.0
        pt = N.stats(c, np.arange(N_OV))
        return pt["nL"] == 200 and pt["nW"] == 400 and pt["nPm"] == 300 and pt["nPp"] == 300
    check("margins", margin_ok)

    def estimand_ok():
        pt = N.stats(planted(N), np.arange(N_OV))
        return (abs(pt["D_BO_ret"] - 0.5) < 1e-9 and abs(pt["D_BO_plac"]) < 1e-9 and abs(pt["Delta_BO"] - 0.5) < 1e-9
                and abs(pt["C_L"] - 0.8) < 1e-9 and abs(pt["C_W"] - 0.3) < 1e-9 and pt["E"] == (200 - 300) / N_OV)
    check("estimands", estimand_ok)

    # family: planted effect PASS; coupling-only (the same enrichment in the placebo split) FAIL [W4]
    def fam_pass():
        v = family(N, [planted(N), planted(N)])
        return [r["verdict"] for r in v] == ["PASS"] * 6
    check("family_pass", fam_pass)

    def fam_coupled():
        c = planted(N, bo=(0.6, 0.1, 0.6, 0.1), zl=(0.8, 0.3, 0.85, 0.3))
        v = family(N, [c, c])
        return [r["verdict"] for r in v] == ["FAIL"] * 6
    check("family_coupling_only_fails", fam_coupled)

    def fam_below_dmin():  # Delta = 0.08, very precise: FAIL on the point threshold
        c = planted(N, bo=(1.0, 0.0, 0.0, 0.0), zl=(0.8, 0.3, 0.3, 0.3))
        c.f_d1["BO"] = first(N_OV, PM_IDX, 0.92)
        return family(N, [c, c])[0]["verdict"] == "FAIL" and abs(N.stats(c, np.arange(N_OV))["Delta_BO"] - 0.08) < 1e-9
    check("family_point_threshold", fam_below_dmin)

    def fam_not_decidable():  # P+ holds 25 images: NOT DECIDABLE, p = 1, m stays 6
        small = planted(N, sizes=(L_IDX, W_IDX, PM_IDX, range(400, 425)))
        v = family(N, [small, planted(N)])
        return ([r["verdict"] for r in v[:3]] == ["NOT DECIDABLE"] * 3 and all(r["p"] == 1.0 for r in v[:3])
                and [r["verdict"] for r in v[3:]] == ["PASS"] * 3)
    check("family_not_decidable", fam_not_decidable)

    def fam_base_rate():  # N4: Delta >= 0.10 but the relative-risk form is negative
        c = planted(N, bo=(0.95, 0.70, 0.20, 0.10))
        v = family(N, [c, c])
        return v[0]["verdict"] == "PASS (base-rate attributed)" and v[3]["verdict"] == "PASS (base-rate attributed)"
    check("family_N4", fam_base_rate)

    # verdict lines on handcrafted rows
    def rows(p, conds=True, h="H3", sr7=1.0):
        return [{"h": h, "p": p, "conds": conds, "decidable": True, "sr7": sr7}] + \
               [{"h": "H3", "p": 1.0, "conds": False, "decidable": True}] * 5
    check("alpha", lambda: N.family_verdicts(rows(0.0041))[0]["verdict"] == "PASS"
          and N.family_verdicts(rows(0.0042))[0]["verdict"] == "FAIL")   # 6 * p vs 0.025
    check("conds", lambda: N.family_verdicts(rows(0.0001, conds=False))[0]["verdict"] == "FAIL")
    def m6_stops():
        try:
            N.family_verdicts(rows(0.0001)[:5])
        except SystemExit:
            return True
        return False
    check("m6", m6_stops)

    def h3(cl, cw, gp, pc=0.0):
        pt = {"nL": 99, "nW": 99, "nPm": 99, "nPp": 99, "C_L": cl, "C_W": cw, "H3_gap_minus_plac": gp}
        return N.h_row("H3", pt, {"C_L": np.full(2000, pc + cl)})
    check("h3_pass", lambda: h3(0.60, 0.45, 0.0)["conds"])
    check("h3_cmin", lambda: not h3(0.59, 0.40, 0.1)["conds"])
    check("h3_gap", lambda: not h3(0.70, 0.61, 0.1)["conds"])
    check("h3_plac", lambda: not h3(0.70, 0.40, -0.01)["conds"])
    check("h3_test_0.50", lambda: h3(0.70, 0.4, 0.1, pc=-0.2)["p"] == 2001 / 2001
          and h3(0.70, 0.4, 0.1, pc=-0.1)["p"] == 1 / 2001)

    def h12_flag():
        pt = {"nL": 99, "nW": 99, "nPm": 99, "nPp": 99, "Delta_BO": 0.2, "Delta_ZL": 0.0, "SR7_BO": 1, "SR7_ZL": 1}
        bt = {"Delta_BO": np.full(2000, 0.2), "Delta_ZL": np.full(2000, 0.0)}
        return N.h_row("H1", pt, bt)["conds"] and not N.h_row("H2", pt, bt)["conds"]
    check("h1_bo_h2_zl", h12_flag)
    check("s_label", lambda: (N.s_label([0.1, 0.2]), N.s_label([-0.2, -0.1]), N.s_label([-0.1, 0.1]))
          == ("DETECTED", "REVERSED", "UNRESOLVED"))

    # CC-511 W5 (a): a class in both zs and shown is not neighbour-only; (b) decidability at 30, not 29
    check("neighbour_only_zs_excluded", lambda: inst.neighbour_only("near dog cat", "near cat", ["a cat"]) == [])

    def dec(npp):
        pt = {"nL": 99, "nW": 99, "nPm": 99, "nPp": npp, "Delta_BO": 0.5, "Delta_ZL": 0.5, "SR7_BO": 1, "SR7_ZL": 1}
        return N.h_row("H1", pt, {"Delta_BO": np.full(2000, 0.5)})["decidable"]
    check("decidable_30", lambda: dec(30) and not dec(29))

    # CC-511 N5: S1 rows on L, G0 E with P-
    def s1_g0():
        c = planted(N, sizes=(L_IDX, W_IDX, PM_IDX, range(400, 650)))
        c.f_d0["BO"] = first(N_OV, W_IDX, 1.0)
        pt = N.stats(c, np.arange(N_OV))
        return abs(pt["S_BO"] - 0.6) < 1e-9 and pt["E"] == (200 - 300) / N_OV
    check("s1_g0", s1_g0)

    # English output (erratum 1 E3, CC-511 W3): BO / CP rows are the NOT RUN string; reduced-category label
    def en_out():
        c = planted(N)
        c.e, c.f_d1, c.f_d2 = None, None, None
        a = N.english_public(N.analyse(c, N.index_matrices()["ov_dev_b"]))
        r = a["rows"]
        return (r["D_BO_ret"] == N.EN_NOT_RUN and r["S_CP"] == N.EN_NOT_RUN and r["share_BO_L"] == N.EN_NOT_RUN
                and r["C_L"]["label"] == N.EN_CATS and isinstance(r["D_ZL_ret"]["point"], float)
                and "words" in a["label"])
    check("english_not_run", en_out)
    check("flags_zl_ln", lambda: N.flags_zl_ln(inst, "copy dog cat x", "copy dog tree", st, 4.0) == {"ZL": True, "LN": False})

    host_checks(N, H, inst, st, check)

    # custody counts (R2): planted overlaps in every key, then a clean set
    def lists_(ov, xm, xmt):
        return {"sets": {"ov_dev_b": ov, "xm_dev500": xm, "xm_test2500": xmt}}
    ov = [[f"o{i}", f"o{i}.jpg", f"{i:064x}"] for i in range(925)]
    xm = [[f"x{i}", f"x{i}.jpg", f"{i + 5000:064x}"] for i in range(500)]
    xmt = [[f"t{i}", f"t{i}.jpg", f"{i + 9000:064x}"] for i in range(2500)]
    f30k = {"carve": [f"c{i}" for i in range(1000)], "refuse": {"val": ["v1"], "test": ["w1"]}}
    clean = N.custody_counts(lists_(ov, xm, xmt), "a.jpg\t" + "f" * 64 + "\n", [["k", "b.jpg", "e" * 64]], f30k)
    check("custody_clean", lambda: set(clean.values()) == {0} and len(clean) == 11)
    dirty = N.custody_counts(lists_(ov, xm, xmt + [["x3", "q", "0" * 64]]),
                             f"o1.jpg\t{0:064x}\nzz\t{5001:064x}\n", [["k", "x7", f"{8:064x}"], ["k", "o2.jpg", "1" * 64]],
                             {"carve": f30k["carve"], "refuse": {"val": ["c1"], "test": ["c2", "c3"]}})
    check("custody_dirty", lambda: dirty == {
        "ov_dev_b&ov_test.ids": 1, "ov_dev_b&ov_test.sha": 1, "ov_dev_b&carve.ids": 1, "ov_dev_b&carve.sha": 1,
        "xm_dev500&ov_test.ids": 0, "xm_dev500&ov_test.sha": 1, "xm_dev500&carve.ids": 1, "xm_dev500&carve.sha": 0,
        "xm_dev500&xm_test2500.ids": 1, "f30k_carve&refuse.val": 1, "f30k_carve&refuse.test": 2})

    def gate_stops():
        try:
            N.custody_gate({"a": 0, "b": 1})
        except SystemExit:
            return True
        return False
    check("custody_gate", gate_stops)
    check("custody_gate_clean", lambda: N.custody_gate({"a": 0}) is None)

    def guard_stops():
        try:
            N.row_guard(["a", "b"], {"b"}, "t")
        except SystemExit:
            return True
        return False
    check("row_guard", guard_stops)
    return bad


# ------------------------------------------------------------------------------------------------ host wiring (W6)
def host_checks(N, H, inst, st, check) -> None:
    import json
    import tempfile

    def raises(fn) -> bool:
        try:
            fn()
        except SystemExit:
            return True
        return False

    # cell_of: d = ret - rand d0 (SR1: R = 3 mean), e = d1 - d2, flags of each arm in its slot
    sc = {"ret": np.array([10.0, 0.0]), "rand_d0": np.array([1.0, 2.0]), "rand_d1": np.array([4.0, 8.0]),
          "rand_d2": np.array([16.0, 32.0])}
    fl = {a: {"BO": np.array([a == "ret", a == "rand_d1"])} for a in sc}

    def cell_ok():
        c, m = H.cell_of(sc, fl), H.cell_of(sc, fl, rand="mean")
        return (c.d.tolist() == [9.0, -2.0] and c.e.tolist() == [-12.0, -24.0] and c.f_ret is fl["ret"]
                and c.f_d0 is fl["rand_d0"] and c.f_d1 is fl["rand_d1"] and c.f_d2 is fl["rand_d2"]
                and np.allclose(m.d, [10 - 7.0, 0 - 14.0]))
    check("host_cell_of", cell_ok)

    # arm parsing: five planted batch-1 names; perm and fwd50 never matched
    names = {"at_q_s-zs-b1.preds.json": "zs", "at_q_s-ret-k8-first-T1-mvi-b1.preds.json": "ret",
             "at_q_s-rand-k8--T1-d0-mvi-b1.preds.json": "rand_d0", "at_q_s-rand-k8--T1-d1-mvi-b1.preds.json": "rand_d1",
             "at_q_s-rand-k8--T1-d2-mvi-b1.preds.json": "rand_d2", "at_q_s-perm-k8-first-T1-p1-mvi-b1.preds.json": None,
             "at_q_s-ret-k8-first-T1-mvi-b1-fwd50.preds.json": None, "at_q_s-ret-k8-first-T1-mvi.preds.json": None,
             "at_q_s-ret_img-k8-first-T1-b1.preds.json": None}
    check("host_arm_of", lambda: all(H.arm_of(n) == a for n, a in names.items()))

    def b1_ok():
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / H.ATTR_OUT
            d.mkdir(parents=True)
            for n, a in names.items():
                (d / n).write_text(json.dumps({"tag": a or "never"}))
            got = H.b1_runs(Path(t), "q", "s")
            ok = {k: v["tag"] for k, v in got.items()} == {a: a for a in names.values() if a}
            (d / "at_q_s-rand-k8--T1-d2-mvi-b1.preds.json").unlink()
            return ok and raises(lambda: H.b1_runs(Path(t), "q", "s"))
    check("host_b1_runs", b1_ok)

    # status: verified first (through key), then the reference union; tally counts classes; None does not count
    def status_ok():
        tally = {"verified": 0, "reference": 0}
        f = H.status_fn(lambda o: o.lower(), {"cho", "meo"}, {"cho": "absent", "xe": "present"}, tally)
        r = [f("CHO"), f("MEO"), f("xe"), f("cay")]
        g = H.status_fn(lambda o: o, {"a"}, None, None)
        return r == ["absent", "present", "present", "absent"] and tally == {"verified": 2, "reference": 2} \
            and g("a") == "present" and g("b") == "absent"
    check("host_status_fn", status_ok)

    # flag arrays: each arm's own shown list, the same zs caption
    def flags_ok():
        runs = {"ret": {"predictions": {"i": "near dog cat"}, "ex": ["a cat"]},
                "rand_d0": {"predictions": {"i": "near dog cat"}, "ex": ["a tree"]}}
        zs = {"predictions": {"i": "near dog tree"}}
        out = H.flag_arrays(inst, ["i"], runs, zs, lambda r, i: r["ex"], {"i": st}, {"i": 3.0})
        return out["ret"]["BO"].tolist() == [True] and out["rand_d0"]["BO"].tolist() == [False] \
            and out["ret"]["ZL"].tolist() == [True]
    check("host_flag_arrays", flags_ok)

    # CC-511e5: the zs arm is never flagged; an empty shown list of a flagged arm is a STOP; refs must be non-empty
    real = N.Instruments(classes=inst.classes, key=inst.key, length=inst.length,
                         copy_m=lambda cap, shown: max(0.0 for _ in shown))   # raises on [] like rl_reward.copy_stat
    def zs_skipped():
        runs = {"ret": {"predictions": {"i": "near dog cat", "j": "near cat"}, "ex": ["a cat"]},
                "zs": {"predictions": {"i": "near dog tree", "j": "near tree"}, "ex": []}}
        out = H.flag_arrays(real, ["i", "j"], runs, runs["zs"], lambda r, i: r["ex"], {"i": st, "j": st},
                            {"i": 3.0, "j": 2.0})
        return set(out) == {"ret"} and out["ret"]["BO"].tolist() == [True, True]
    check("host_flag_arrays_zs_not_flagged", zs_skipped)

    def empty_stops():
        runs = {"ret": {"predictions": {"i": "near dog cat", "j": "near cat"}, "ex": {"i": ["a cat"], "j": []}}}
        try:
            H.flag_arrays(real, ["i", "j"], runs, {"predictions": {"i": "x", "j": "x"}},
                          lambda r, i: r["ex"][i], {"i": st, "j": st}, {"i": 3.0, "j": 2.0})
        except SystemExit:
            return True
        return False
    check("host_flag_arrays_empty_shown_stops", empty_stops)

    def refs_stop():
        try:
            H.refs_nonempty({"i": ["a"], "j": []}, ["i", "j"])
        except SystemExit:
            return H.refs_nonempty({"i": ["a"], "j": ["b"]}, ["i", "j"]) is None
        return False
    check("host_refs_nonempty", refs_stop)

    # CC-511e6: statuses are bound to their own set at creation (the late-bound ids of the SR4 fault)
    def statuses_bound():
        ids_a = ["a1", "a2"]
        sa = H.make_statuses(lambda o: o, ids_a, {"a1": {"dog"}, "a2": set()}, None)
        sb = H.make_statuses(lambda o: o, ["b1", "b2"], {"b1": {"cat"}, "b2": {"cat"}}, {"b1": {"cat": "absent"}})
        ids_a.append("zz")                      # the caller's list changes after creation
        ra, rb = sa(None), sb(None)
        return (sorted(ra) == ["a1", "a2"] and sorted(rb) == ["b1", "b2"] and ra["a1"]("dog") == "present" and rb["b2"]("cat") == "present"
                and ra["a2"]("dog") == "absent" and rb["b1"]("cat") == "absent")
    check("host_make_statuses_bound", statuses_bound)

    # English flags: no copy statistic, no shown list; BO / CP placeholders
    def en_ok():
        boom = N.Instruments(classes=inst.classes, key=inst.key, copy_m=lambda *_: 1 / 0, length=inst.length)
        runs = {"zs": {"predictions": {"i": "near dog tree"}}, "ret": {"predictions": {"i": "near dog cat"}},
                "rand_d0": {"predictions": {"i": "near dog tree"}}}
        out = H.en_flags(boom, runs, ["i"], {"i": {"tree", "dog"}}, {"i": 3.0})
        return out["ret"]["ZL"].tolist() == [True] and out["rand_d0"]["ZL"].tolist() == [False] \
            and not out["ret"]["BO"].any() and not out["ret"]["CP"].any()
    check("host_en_flags", en_ok)

    # family assembly: six rows, OV-dev-B, Qwen then InternVL3, H1-H3
    def fake(v):
        pt = {"nL": 99, "nW": 99, "nPm": 99, "nPp": 99, "Delta_BO": v, "Delta_ZL": v, "SR7_BO": 1, "SR7_ZL": 1,
              "C_L": v, "C_W": 0.0, "H3_gap_minus_plac": 0.0}
        return {"_pt": pt, "_boot": {"Delta_BO": np.full(2000, v), "Delta_ZL": np.full(2000, v), "C_L": np.full(2000, v)}}
    an = {(s, m): fake(0.11 * (k + 1) + (0.5 if s == "xm_dev500" else 0)) for s in ("ov_dev_b", "xm_dev500")
          for k, m in enumerate(N.MODELS)}

    def fam_ok():
        rows = H.family_rows(an)
        return ([(r["model"], r["h"], r["set"]) for r in rows] == [(m, h, "ov_dev_b") for m in N.FAMILY_MODELS
                                                                     for h in ("H1", "H2", "H3")]
                and [round(r["point"], 2) for r in rows] == [0.11, 0.11, 0.11, 0.22, 0.22, 0.22])
    check("host_family_rows", fam_ok)

    # parity: within tolerance passes; a miss STOPs naming the cell and no value
    def parity_ok():
        H.parity(("ov_dev_b", "q"), 8.2749, {("ov_dev_b", "q"): 8.27}, "w")
        try:
            H.parity(("ov_dev_b", "q"), 8.2853, {("ov_dev_b", "q"): 8.27}, "w")
        except SystemExit as e:
            return "8.2" not in str(e) and "ov_dev_b q" in str(e)
        return False
    check("host_parity", parity_ok)

    # wall clock: a STOP past the cap
    def clock_ok():
        t = [0.0]
        c = H.Clock(cap_h=1.0, now=lambda: t[0])
        t[0] = 3599.0
        c.check("a")
        t[0] = 3601.0
        return raises(lambda: c.check("b"))
    check("host_clock", clock_ok)
    check("host_aya_flag", lambda: H.flagged({}, "ov_dev_b", "aya_vision_8b") == {"flag": N.AYA_FLAG}
          and H.flagged({}, "xm_dev500", "aya_vision_8b") == {} and H.flagged({}, "ov_dev_b", "qwen25vl_7b") == {})

    # module pin check and $NCS_DATA pins on a planted tree
    def pins_ok():
        import hashlib
        import importlib.util
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "pkgm").mkdir()
            f = root / "pkgm" / "n3d_probe_mod.py"
            f.write_text("X = 1\n")
            spec = importlib.util.spec_from_file_location("n3d_probe_mod", f)
            m = importlib.util.module_from_spec(spec)
            sys.modules["n3d_probe_mod"] = m
            spec.loader.exec_module(m)
            good, bad_ = root / "good.sha256", root / "bad.sha256"
            good.write_text(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  pkgm/n3d_probe_mod.py\n")
            bad_.write_text(f"{'0' * 64}  pkgm/n3d_probe_mod.py\n")
            ok = H.module_pin_check(root, good) == 1 and raises(lambda: H.module_pin_check(root, bad_))
            del sys.modules["n3d_probe_mod"]
            (root / "d").mkdir()
            (root / "d" / "x.txt").write_text("x")
            saved = dict(H.DATA_PINS)
            try:
                H.DATA_PINS.clear()
                H.DATA_PINS["d/x.txt"] = hashlib.sha256(b"x").hexdigest()
                (root / "vncorenlp/models/wordsegmenter").mkdir(parents=True)
                ok = ok and H.data_pins(root)["data_pins"] == "ok"
                H.DATA_PINS["d/x.txt"] = "0" * 64
                ok = ok and raises(lambda: H.data_pins(root))
            finally:
                H.DATA_PINS.clear()
                H.DATA_PINS.update(saved)
            return ok and len(H.DATA_PINS) == 6
    check("host_pins", pins_ok)


# ------------------------------------------------------------------------------------------------ mutants
MUTANTS = [  # (old, new): each old text occurs once in c_n3d.py; every mutant must make the suite fail
    ("SEED = 1127001", "SEED = 1127002"),
    ('SET_N = {"ov_dev_b": 925, "xm_dev500": 500, "f30k_carve": 1000}',
     'SET_N = {"xm_dev500": 500, "ov_dev_b": 925, "f30k_carve": 1000}'),
    ("M_HOLM = 6 ", "M_HOLM = 5 "),
    ("MIN_N = 30 ", "MIN_N = 20 "),
    ("D_MIN = 0.10 ", "D_MIN = 0.05 "),
    ("C_MIN, C_TEST, C_GAP = 0.60, 0.50, 0.10", "C_MIN, C_TEST, C_GAP = 0.55, 0.50, 0.10"),
    ("C_MIN, C_TEST, C_GAP = 0.60, 0.50, 0.10", "C_MIN, C_TEST, C_GAP = 0.60, 0.40, 0.10"),
    ("C_MIN, C_TEST, C_GAP = 0.60, 0.50, 0.10", "C_MIN, C_TEST, C_GAP = 0.60, 0.50, 0.05"),
    ("LN_REL = 0.25 ", "LN_REL = 0.30 "),
    ("CP_M = 0.90 ", "CP_M = 0.95 "),
    ("ALPHA = 0.025", "ALPHA = 0.05"),
    ("PREC = (\"CP\", \"BO\", \"ZL\", \"LN\")  ", "PREC = (\"BO\", \"CP\", \"ZL\", \"LN\")  "),
    ("np.sum(np.isnan(s) | (s <= thr))", "np.sum(s <= thr)"),
    ("np.sum(np.isnan(s) | (s <= thr))", "np.sum(np.isnan(s) | (s < thr))"),
    ("float((1 + np.sum", "float((0 + np.sum"),
    ("run = max(run, min(1.0, (m - j) * ps[k]))", "run = max(run, min(1.0, (m - j - 1) * ps[k]))"),
    ("run = max(run, min(1.0, (m - j) * ps[k]))", "run = min(1.0, (m - j) * ps[k])"),
    ("if self.key(o) not in z and", "if self.key(o) in z and"),
    ("and self.key(o) in ex]", "]"),
    ('"BO": any(status(o) == "absent"', '"BO": any(status(o) == "present"'),
    ('"CP": inst.copy_m(cap, shown) >= CP_M', '"CP": inst.copy_m(cap, shown) > CP_M'),
    ('status(o) == "present" and inst.key(o) not in have', 'status(o) == "present" and inst.key(o) in have'),
    ("abs(inst.length(cap) - med_len) >= ln_rel", "abs(inst.length(cap) - med_len) > ln_rel"),
    ("for j in reversed(range(len(prec))):", "for j in range(len(prec)):"),
    ("L, W = d < -m, d > m", "L, W = d <= -m, d > m"),
    ("Pm, Pp = e < -m, e > m", "Pm, Pp = e < -m, e >= m"),
    ('out[f"Delta_{f}"] = out[f"D_{f}_ret"] - out[f"D_{f}_plac"]', 'out[f"Delta_{f}"] = out[f"D_{f}_ret"]'),
    ('out[f"D_{f}_plac"] = a - b', 'out[f"D_{f}_plac"] = b - a'),
    ('out[f"C_{g}"] = 1 - out[f"share_OTHER_{g}"]\n    out["C_all"]', 'out[f"C_{g}"] = out[f"share_OTHER_{g}"]\n    out["C_all"]'),
    ('return min(pt["nL"], pt["nW"], pt.get("nPm", 0), pt.get("nPp", 0)) >= MIN_N',
     'return min(pt["nL"], pt["nW"]) >= MIN_N'),
    ('return {"h": h, "p": 1.0, "conds": False, "decidable": False}',
     'return {"h": h, "p": 0.0, "conds": False, "decidable": False}'),
    ('f = "BO" if h == "H1" else "ZL"', 'f = "ZL" if h == "H1" else "BO"'),
    ('"conds": pt[f"Delta_{f}"] >= D_MIN', '"conds": pt[f"Delta_{f}"] > -1'),
    ('"p": ptilde(boot["C_L"], C_TEST)', '"p": ptilde(boot["C_L"], 0.0)'),
    ('"conds": pt["C_L"] >= C_MIN and gap >= C_GAP and pt["H3_gap_minus_plac"] >= 0',
     '"conds": pt["C_L"] >= C_MIN and pt["H3_gap_minus_plac"] >= 0'),
    ('"conds": pt["C_L"] >= C_MIN and gap >= C_GAP and pt["H3_gap_minus_plac"] >= 0',
     '"conds": pt["C_L"] >= C_MIN and gap >= C_GAP'),
    ('elif a < ALPHA and r["conds"]:', 'elif a < ALPHA:'),
    ('elif a < ALPHA and r["conds"]:', 'elif r["p"] < ALPHA and r["conds"]:'),
    ('and not r["sr7"] >= 0 else "PASS"', 'and r["sr7"] < -99 else "PASS"'),
    ("if len(rows) != M_HOLM:", "if len(rows) < 1:"),
    ("lo > 0 else", "lo >= -1 else"),
    ('out[f"{s}&ov_test.ids"], out[f"{s}&ov_test.sha"] = len(ids & t_ids), len(sha & t_sha)',
     'out[f"{s}&ov_test.ids"], out[f"{s}&ov_test.sha"] = len(ids & t_ids), 0'),
    ('out[f"{s}&ov_test.ids"], out[f"{s}&ov_test.sha"] = len(ids & t_ids), len(sha & t_sha)',
     'out[f"{s}&ov_test.ids"], out[f"{s}&ov_test.sha"] = 0, len(sha & t_sha)'),
    ('out[f"{s}&carve.ids"], out[f"{s}&carve.sha"] = len(ids & o_ids), len(sha & o_sha)',
     'out[f"{s}&carve.ids"], out[f"{s}&carve.sha"] = 0, len(sha & o_sha)'),
    ('out[f"{s}&carve.ids"], out[f"{s}&carve.sha"] = len(ids & o_ids), len(sha & o_sha)',
     'out[f"{s}&carve.ids"], out[f"{s}&carve.sha"] = len(ids & o_ids), 0'),
    ("ids = {r[0] for r in rows} | {r[1] for r in rows}", "ids = {r[0] for r in rows}"),
    ('out["xm_dev500&xm_test2500.ids"] = len({r[0] for r in dev["xm_dev500"]} & xm_test)',
     'out["xm_dev500&xm_test2500.ids"] = 0'),
    ('out["f30k_carve&refuse.val"] = len(carve & set(f30k["refuse"]["val"]))', 'out["f30k_carve&refuse.val"] = 0'),
    ('out["f30k_carve&refuse.test"] = len(carve & set(f30k["refuse"]["test"]))', 'out["f30k_carve&refuse.test"] = 0'),
    ("bad = {k: v for k, v in counts.items() if v}", "bad = {}"),
    ("if hit:", "if hit > 1:"),
]


#: CC-511 judge mutants on verdict lines of c_n3d.py, byte for byte from expected_fixes/JUDGE_MUTANTS_CC511.py (8d410a7d)
JUDGE_MUTANTS = [
 ("L, W = d < -m, d > m", "L, W = d > m, d < -m"),
 ('out[f"D_{f}_ret"] = out[f"Pr_{f}_L"] - out[f"Pr_{f}_W"]', 'out[f"D_{f}_ret"] = out[f"Pr_{f}_W"] - out[f"Pr_{f}_L"]'),
 ("cat_d1 = category(c.f_d1, prec)[rows]", "cat_d1 = category(c.f_ret, prec)[rows]"),
 ("f1 = c.f_d1[f][rows]", "f1 = c.f_d2[f][rows]"),
 ("fr = c.f_ret[f][rows]", "fr = c.f_d0[f][rows]"),
 ('out["H3_gap_minus_plac"] = (out["C_L"] - out["C_W"]) - (out["C_Pm"] - out["C_Pp"])', 'out["H3_gap_minus_plac"] = (out["C_L"] - out["C_W"]) + (out["C_Pm"] - out["C_Pp"])'),
 ('out["H3_gap_minus_plac"] = (out["C_L"] - out["C_W"]) - (out["C_Pm"] - out["C_Pp"])', 'out["H3_gap_minus_plac"] = (out["C_L"] - out["C_W"]) - (out["C_Pp"] - out["C_Pm"])'),
 ('"p": ptilde(boot[f"Delta_{f}"], 0.0)', '"p": ptilde(boot[f"Delta_{f}"], D_MIN)'),
 ('"p": ptilde(boot[f"Delta_{f}"], 0.0)', '"p": ptilde(boot[f"D_{f}_ret"], 0.0)'),
 ('"p": ptilde(boot["C_L"], C_TEST)', '"p": ptilde(boot["C_W"], C_TEST)'),
 ('gap = pt["C_L"] - pt["C_W"]', 'gap = pt["C_L"] - pt["C_Pm"]'),
 ('adj = holm([r["p"] for r in rows])', 'adj = [r["p"] for r in rows]'),
 ("run = max(run, min(1.0, (m - j) * ps[k]))", "run = max(run, min(1.0, m * ps[k]))"),
 ('order = np.argsort(ps, kind="stable")', 'order = np.argsort(ps, kind="stable")[::-1]'),
 ("/ (s.size + 1))", "/ (s.size))"),
 ("e = c.e[rows]", "e = c.d[rows]"),
 ('if not r["decidable"]:', "if False:"),
 ('"sr7": pt[f"SR7_{f}"]', '"sr7": 1.0'),
 ('np.log(out[f"Pr_{f}_L"] / out[f"Pr_{f}_W"]) - np.log(a / b)', 'np.log(out[f"Pr_{f}_L"] / out[f"Pr_{f}_W"]) - np.log(b / a)'),
 ('out[f"Pr_{f}_L"], out[f"Pr_{f}_W"] = _rate(fr, L), _rate(fr, W)', 'out[f"Pr_{f}_L"], out[f"Pr_{f}_W"] = _rate(fr, W), _rate(fr, L)'),
 ("return (f & g).sum(-1) / g.sum(-1)", "return (f & g).sum(-1) / g.shape[-1]"),
 ('"ZL": any(status(o) == "present"', '"ZL": any(status(o) == "absent"'),
 ("z = {self.key(o) for o in self.classes(zs)}", "z = set()"),
 ('out[f"share_{name}_{g}"] = _rate(cat_ret == j, gm)', 'out[f"share_{name}_{g}"] = _rate(cat_ret != j, gm)'),
 ("out = np.where(fl[prec[j]], PREC.index(prec[j]), out)", "out = np.where(fl[prec[j]], j, out)"),
 ('pt.get("nPp", 0)) >= MIN_N', 'pt.get("nPp", 0)) > MIN_N'),
 ("return {s: rng.integers(0, n, (B, n)) for s, n in SET_N.items()}", "return {s: np.random.default_rng(SEED).integers(0, n, (B, n)) for s, n in SET_N.items()}"),
 ('"conds": pt[f"Delta_{f}"] >= D_MIN', '"conds": pt[f"D_{f}_ret"] >= D_MIN'),
 ("t_ids, t_sha = {r[0] for r in tsv}, {r[1] for r in tsv}", "t_ids, t_sha = {r[1] for r in tsv}, {r[0] for r in tsv}"),
 ("o_ids, o_sha = {r[1] for r in carve_order}, {r[2] for r in carve_order}", "o_ids, o_sha = {r[0] for r in carve_order}, {r[2] for r in carve_order}"),
 ('xm_test = {r[0] for r in lists["sets"]["xm_test2500"]}', 'xm_test = {r[1] for r in lists["sets"]["xm_test2500"]}'),
 ('elif a < ALPHA and r["conds"]:', 'elif a <= ALPHA and r["conds"]:'),
 ("np.sum(np.isnan(s) | (s <= thr))", "np.sum(np.isnan(s) & (s <= thr))"),
 ('out[f"S_{f}"] = _rate(c.f_ret[f][rows], L) - _rate(c.f_d0[f][rows], L)', 'out[f"S_{f}"] = _rate(c.f_ret[f][rows], W) - _rate(c.f_d0[f][rows], W)'),
 ('"E": (L.sum(-1) - Pm.sum(-1)) / L.shape[-1]', '"E": (L.sum(-1) - Pp.sum(-1)) / L.shape[-1]'),
 ('return "DETECTED" if lo > 0 else "REVERSED" if hi < 0 else "UNRESOLVED"', 'return "DETECTED" if lo > 0 else "UNRESOLVED"'),
]
#: equivalent mutants, excluded with the reason (CC-511 C5 (c))
EQUIVALENT = {('elif a < ALPHA and r["conds"]:', 'elif a <= ALPHA and r["conds"]:'):
              "Holm p = (k / 2001) x j, j = 1..6, never equals 0.025 (CC-511 C5 (c))"}
#: CC-511 W6: mutants on the host wiring lines of c_n3d_host.py
HOST_MUTANTS = [
    ("    ids = list(ids)\n\n    def statuses(t):", "    def statuses(t):"),                          # CC-511e6
    ("status_fn(key, gold[i], None if verified", "status_fn(key, gold[ids[0]], None if verified"),         # CC-511e6
    ("verified.get(i, {}), t) for i in ids}", "verified.get(ids[0], {}), t) for i in ids}"),               # CC-511e6
    ('if arm == "zs":\n            continue\n        if any(not shown(r, i)',
     'if arm == "none":\n            continue\n        if any(not shown(r, i)'),                     # CC-511e5
    ('if any(not shown(r, i) for i in ids):', 'if False:'),                                      # CC-511e5
    ('if any(not shown(r, i) for i in ids):', 'if all(not shown(r, i) for i in ids):'),          # CC-511e5
    ('if any(not refs[i] for i in ids):', 'if False:'),                                          # CC-511e5
    ('if any(not refs[i] for i in ids):', 'if all(not refs[i] for i in ids):'),                  # CC-511e5
    ('e=sc["rand_d1"] - sc["rand_d2"]', 'e=sc["rand_d2"] - sc["rand_d1"]'),
    ('f_d1=fl["rand_d1"], f_d2=fl["rand_d2"])', 'f_d1=fl["rand_d2"], f_d2=fl["rand_d1"])'),
    ('base = sc["rand_d0"] if rand == "d0" else', 'base = sc["rand_d1"] if rand == "d0" else'),
    ('np.mean([sc[f"rand_d{d}"] for d in range(3)], 0)\n    return N.Cell', 'np.mean([sc[f"rand_d{d}"] for d in range(2)], 0)\n    return N.Cell'),
    ('f_ret=fl["ret"], f_d0=fl["rand_d0"],\n                  f_d1', 'f_ret=fl["rand_d0"], f_d0=fl["ret"],\n                  f_d1'),
    ('if "-zs-" in name:\n        return "zs"', 'if "-zs-" in name:\n        return "ret"'),
    ('for d in range(3) if "-rand-" in name and f"-d{d}-" in name), None)', 'for d in range(2) if "-rand-" in name and f"-d{d}-" in name), None)'),
    ('if "-ret-" in name:\n        return "ret"', 'if "-ret" in name:\n        return "ret"'),
    ('if set(out) != {"zs", "ret", "rand_d0", "rand_d1", "rand_d2"}:', 'if not out:'),
    ('v = None if verified is None else verified.get(o, verified.get(key(o)))', 'v = None if verified is None else verified.get(o)'),
    ('how = "verified" if v in ("present", "absent") else "reference"', 'how = "reference"'),
    ('return "present" if key(o) in gold else "absent"', 'return "present" if o in gold else "absent"'),
    ('if tally is not None:\n            tally[how] += 1', 'if tally is not None:\n            tally["verified"] += 1'),
    ('N.flags_of(inst, r["predictions"][i], zs["predictions"][i], shown(r, i)', 'N.flags_of(inst, r["predictions"][i], zs["predictions"][i], shown(zs, i)'),
    ('N.flags_of(inst, r["predictions"][i], zs["predictions"][i], shown(r, i)', 'N.flags_of(inst, r["predictions"][i], r["predictions"][i], shown(r, i)'),
    ('    for m in N.FAMILY_MODELS:\n        a = analyses[("ov_dev_b", m)]', '    for m in N.MODELS[1:]:\n        a = analyses[("ov_dev_b", m)]'),
    ('a = analyses[("ov_dev_b", m)]', 'a = analyses[("xm_dev500", m)]'),
    ('if abs(value - table[key]) > N.PARITY_TOL:', 'if abs(value - table[key]) > 0.02:'),
    ('raise SystemExit(f"STOP: parity {what} {key[0]} {key[1]}")', 'raise SystemExit(f"STOP: parity {what} {key[0]} {key[1]} {value}")'),
    ('if h * 3600 > self.cap:', 'if h * 3600 > 2 * self.cap:'),
    ('if pins.get(rel) != N.sha(Path(f)):', 'if rel not in pins:'),
    ('bad = [r for r, h in DATA_PINS.items() if not (data / r).is_file() or N.sha(data / r) != h]', 'bad = [r for r, h in DATA_PINS.items() if not (data / r).is_file()]'),
    ('return {**rows, "flag": N.AYA_FLAG} if (s, m) == ("ov_dev_b", "aya_vision_8b") else rows', 'return {**rows, "flag": N.AYA_FLAG} if m == "aya_vision_8b" else rows'),
    ('rows = [N.flags_zl_ln(inst, runs[a]["predictions"][i], runs["zs"]["predictions"][i],', 'rows = [N.flags_zl_ln(inst, runs[a]["predictions"][i], runs["ret"]["predictions"][i],'),
]


def kill(src_n: str, src_h: str) -> bool:
    """True if the suite fails on this pair of sources (the mutant is killed)."""
    n = load(src_n)
    return bool(suite(n, load_host(src_h)))


def main() -> None:
    bad = suite(load(), load_host())
    if bad:
        print(f"SELFTEST FAIL: {bad}")
        sys.exit(1)
    print("selftest: all checks pass")
    groups = (("own", MUTANTS, SRC, True), ("judge CC-511", JUDGE_MUTANTS, SRC, True),
              ("host", HOST_MUTANTS, HSRC, False))
    failed = False
    for name, muts, src, on_core in groups:
        alive, run_n, equiv = [], 0, 0
        for old, new in muts:
            if (old, new) in EQUIVALENT:
                equiv += 1
                continue
            if src.count(old) != 1:
                print(f"MUTANT TEXT NOT UNIQUE ({src.count(old)}): {old[:70]}")
                sys.exit(1)
            mut = src.replace(old, new)
            run_n += 1
            if not (kill(mut, HSRC) if on_core else kill(SRC, mut)):
                alive.append(old[:70] + " -> " + new[:40])
        print(f"mutants {name}: {run_n - len(alive)}/{run_n} killed" + (f"; {equiv} equivalent excluded" if equiv else ""))
        for a in alive:
            print(f"  ALIVE: {a}")
        failed |= bool(alive)
    load()
    load_host()
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
