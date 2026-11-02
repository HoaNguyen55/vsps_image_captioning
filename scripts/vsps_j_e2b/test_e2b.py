#!/usr/bin/env python
"""CPU selftest for scripts/vsps_j_e2b (no weights, no data, no network: every socket raises).

    <venv with numpy> -I scripts/vsps_j_e2b/test_e2b.py
"""
from __future__ import annotations

import json
import math
import random
import socket
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace


def _no_net(*_a, **_k):
    raise OSError("selftest: network blocked")


socket.socket = socket.create_connection = socket.getaddrinfo = _no_net  # type: ignore[assignment,misc]

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import e2b  # noqa: E402
import m0  # noqa: E402


def test_split():
    # pinned id -> half pairs (NB-C9); the rule is sha256(UTF-8 "<decimal id>e2b"), last hex char parity
    got = {i: e2b.half(i) for i in (139, 285, 632, 724, 776)}
    assert got == {139: "tune", 285: "tune", 632: "select", 724: "tune", 776: "select"}, got
    import hashlib
    for i in random.Random(0).sample(range(1, 600000), 200):
        d = hashlib.sha256(f"{i}e2b".encode("utf-8")).hexdigest()
        assert e2b.half(i) == ("tune" if int(d[-1], 16) % 2 == 0 else "select")
    for bad in ("139", 139.0, True):
        try:
            e2b.half(bad)
        except TypeError:
            continue
        raise AssertionError(f"half accepted {bad!r}")


def test_type_rule():
    cases = {"two dogs on a bed": "number", "a red bus": "colour", "a large bus": "attribute",
             "a man riding a horse": "action", "a cup under the table": "relation", "a giraffe": "object"}
    for span, want in cases.items():
        assert e2b.e2b_type(span) == want, (span, e2b.e2b_type(span))
    rng = random.Random(1)
    words = "a two red large on riding cat sitting grey several dog under small".split()
    for _ in range(2000):  # object and number are exactly M0's object and count sets
        s = " ".join(rng.choice(words) for _ in range(rng.randint(1, 6)))
        assert (e2b.e2b_type(s) == "object") == (m0.claim_type(s) == "object")
        assert (e2b.e2b_type(s) == "number") == (m0.claim_type(s) == "count")


def test_prompts():
    span = '  A dog  sits on "the" mat. '
    assert e2b.prompt("FA", "vi", span) == m0.instruct(m0.question(span))  # M0 frame byte for byte
    for f in e2b.FORMS:
        for g in e2b.LANGS:
            assert "A dog sits on" in e2b.prompt(f, g, span)


class FakeTok:
    """Whole-word ids; a leading space maps to the same id; 'KH' prefix collides when clash=True."""

    def __init__(self, clash=False, space_token=False):
        self.clash, self.space_token, self.v = clash, space_token, {" ": 0}

    def encode(self, s, add_special_tokens=False):
        ids = [0] if self.space_token and s.startswith(" ") else []
        w = s.strip().split()[0]
        if self.clash and w.upper().startswith("KH"):
            w = "KH"
        return ids + [self.v.setdefault(w, len(self.v))]

    def decode(self, ids):
        inv = {v: k for k, v in self.v.items()}
        return inv[ids[0]]


def test_token_sets():
    for f in e2b.FORMS:
        for g in e2b.LANGS:
            s = e2b.token_sets(FakeTok(space_token=True), f, g)
            assert all(s.values()) and 0 not in sum(s.values(), [])
    try:
        e2b.token_sets(FakeTok(clash=True), "FB", "vi")
    except e2b.Fault:
        return
    raise AssertionError("KHÔNG RÕ / không clash not caught")


def test_fb_and_band():
    assert e2b.decide_fb({"S": 0.2, "U": 0.1, "R": 0.15}) == ("U", True)
    assert e2b.decide_fb({"S": 0.2, "U": 0.1, "R": 0.6}) == ("R", False)
    rng = random.Random(2)
    y = [int(rng.random() < 0.3) for _ in range(2000)]
    p = [min(0.999, max(0.001, rng.gauss(0.3 if t else 0.75, 0.2))) for t in y]
    tlo, thi = e2b.band(p, y)
    assert e2b.recall([v <= tlo for v in p], y) >= 0.83
    lower = [t for t in e2b.GRID if t < tlo]
    assert not lower or e2b.recall([v <= lower[-1] for v in p], y) < 0.83
    assert thi >= tlo and sum(tlo < v < thi for v in p) / len(p) <= 0.12 + 1e-9
    assert e2b.band(p, [0] * len(p)) == (0.5, 0.5)
    assert e2b.band([0.99] * 10, [1] * 10) == (0.5, 0.5)  # no feasible t_lo
    assert e2b.band_label(tlo, tlo, tlo) == "R"
    lo = e2b.match_lo(p, y, 0.7)
    assert e2b.recall([v <= lo for v in p], y) >= 0.7
    assert e2b.recall([v < lo for v in p], y) < 0.7
    assert e2b.match_lo(p, y, 0.0) == float("-inf")


def test_metrics_and_vote():
    m = e2b.metrics(["R", "R", "S", "U", "S"], [1, 0, 0, 1, 1])
    assert m["prec_R"] == 50 and abs(m["recall"] - 100 / 3) < 1e-9 and m["retention"] == 50 and m["U"] == 20
    assert abs(m["loose_recall"] - 200 / 3) < 1e-9
    assert [e2b.vote(a, b) for a, b in (("R", "S"), ("S", "S"), ("U", "S"), ("S", "R"))] == ["R", "S", "U", "R"]
    assert e2b.macro({"object": {"x": 10.0}, "number": {"x": float("nan")}}, "x") == 10.0


def test_pick():
    tr = {"object": 0.9, "number": 0.9}
    row = lambda c, f, d, u=5.0, r=0.0, v=False: {"cand": c, "form": f, "dprec": d, "U": u, "dret": r, "vote": v,  # noqa: E731
                                                  "tune_recall": dict(tr)}
    rows = {"internvl3_8b|FA": row("internvl3_8b", "FA", 8.0), "aya_vision_8b|FA": row("aya_vision_8b", "FA", 7.8),
            "qwen25vl_7b|FB": row("qwen25vl_7b", "FB", 7.7), "qwen3vl_8b|FA": row("qwen3vl_8b", "FA", 20, u=13),
            "PA2 vintern+aya_vision_8b|FA": row("aya_vision_8b", "FA", 30, v=True)}
    win, rec = e2b.pick(rows)
    assert win == "qwen25vl_7b|FB" and rec == "aya_vision_8b|FA", (win, rec)  # F-B tie-break, then N9
    rows["qwen25vl_7b|FB"]["dret"] = -2.5
    assert e2b.pick(rows) == ("aya_vision_8b|FA", "aya_vision_8b|FA")
    only_vote = {k: v for k, v in rows.items() if v["vote"] or k == "qwen3vl_8b|FA"}
    assert e2b.pick(only_vote)[0] == "PA2 vintern+aya_vision_8b|FA"
    assert e2b.pick({"qwen3vl_8b|FA": rows["qwen3vl_8b|FA"]}) == (None, None)
    # D4 (R-a, amends PREREG l.226): tune strict recall >= 0.83 on each primary type; undefined (NaN) = infeasible
    rows = {"internvl3_8b|FA": row("internvl3_8b", "FA", 8.0), "qwen3vl_8b|FB": row("qwen3vl_8b", "FB", 9.0)}
    rows["qwen3vl_8b|FB"]["tune_recall"]["number"] = 0.82
    assert e2b.pick(rows)[0] == "internvl3_8b|FA"
    rows["qwen3vl_8b|FB"]["tune_recall"]["number"] = float("nan")
    assert e2b.pick(rows)[0] == "internvl3_8b|FA"
    rows["qwen3vl_8b|FB"]["tune_recall"]["number"] = 0.83
    assert e2b.pick(rows)[0] == "qwen3vl_8b|FB"
    segs = [s for s in segs_fixture() if s["t2"] == "number"]
    assert math.isnan(e2b.tune_recall(lambda s: "R", [dict(s, y=0) for s in segs])["number"])


def test_macro_pair():
    """D3: the difference is taken over the primary types both systems define."""
    E = {"object": {"x": 30.0}, "number": {"x": 50.0}}
    V = {"object": {"x": 10.0}, "number": {"x": float("nan")}}
    assert e2b.macro_pair(E, V, "x") == (20.0, ["object"])
    assert math.isnan(e2b.macro_pair(E, {"object": {"x": float("nan")}, "number": {"x": float("nan")}}, "x")[0])


def test_projection_mean():
    """D5 = C.1 (CC-223 W1), including a resume: rate mean until 200 total probes across starts; then all probes
    minus the first of each start; empty set -> rate mean."""
    assert e2b.proj_mean([(1, 1.3)] + [(1, 0.08)] * 20, 0.081) == 0.081  # cold first probe, < 200: rate mean
    assert abs(e2b.proj_mean([(1, 1.3)] + [(1, 0.08)] * 199, 0.5) - 0.08) < 1e-12  # first probe excluded
    rows = [(1, 1.3)] + [(1, 0.08)] * 120 + [(2, 2.0)] + [(2, 0.1)] * 79  # resume: 200 in total across two starts
    assert abs(e2b.proj_mean(rows, 0.5) - (120 * 0.08 + 79 * 0.1) / 199) < 1e-12
    assert e2b.proj_mean(rows[:199], 0.5) == 0.5  # 199 in total: still the rate mean
    one_each = [(i, 0.2) for i in range(200)]  # every probe is a first probe: empty set
    assert e2b.proj_mean(one_each, 0.33) == 0.33
    pj = e2b.projected_h(167.0 / 3600, 16006, e2b.proj_mean([(1, 1.276)] + [(1, 0.081)] * 20, 0.0811))
    assert pj < 0.6  # the C.1 worked example no longer trips the 0.6 h cap


def test_images_exact_and_lists():
    """D8 exact staged set; D11 W25 lists (refused until pinned; drops and holds from the selection only)."""
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "a.jpg"
        f.write_bytes(b"x")
        e2b.check_images(Path(d), {"a.jpg": m0.sha_file(f)})
        (Path(d) / "extra.jpg").write_bytes(b"y")
        try:
            e2b.check_images(Path(d), {"a.jpg": m0.sha_file(f)})
        except SystemExit:
            pass
        else:
            raise AssertionError("an extra staged file was accepted")
    with tempfile.TemporaryDirectory() as d:  # pinned only by a matching line in the prereg SHA256SUMS
        sums, lf = Path(d) / "SHA256SUMS", Path(d) / "e2b_w25_lists.json"
        lf.write_text(json.dumps({"drop": [3], "hold": [4, 5]}))
        for text in ("", f"{'0' * 64}  e2b_w25_lists.json\n"):
            sums.write_text(text)
            try:
                e2b.w25_lists(sums, lf)
            except SystemExit:
                continue
            raise AssertionError("unpinned W25 lists accepted")
        sums.write_text(f"{m0.sha_file(lf)}  e2b_w25_lists.json\n")
        assert e2b.w25_lists(sums, lf) == ({3}, {4, 5})
    probe, held = set(range(1, 11)), {1, 2}
    sel = probe - held
    assert e2b.apply_w25(probe, sel, held, set(), set()) == (probe, sel, held)
    p2, s2, h2 = e2b.apply_w25(probe, sel, held, {3}, {4, 5})
    assert p2 == probe - {3} and s2 == sel - {3, 4, 5} and h2 == {1, 2, 4, 5}
    for drop, hold in (({1}, set()), (set(), {2}), ({3}, {3}), ({99}, set())):
        try:
            e2b.apply_w25(probe, sel, held, drop, hold)
        except SystemExit:
            continue
        raise AssertionError(f"bad W25 lists accepted: {drop} {hold}")


def run_folder(root: Path, name: str, rc=None, prior=None, rows=None) -> Path:
    d = root / name
    d.mkdir(parents=True)
    (d / "launch.json").write_text(json.dumps({"t0": 0, "starts": 1, "rerun_of": {"rc": prior} if prior else None}))
    if rc is not None:
        (d / "STOP").write_text(json.dumps({"rc": rc, "reason": "t"}))
        (d / "probes.jsonl").write_text("{not json")  # a stopped folder is never opened
    if rows is not None:
        pf = d / "probes.jsonl"
        pf.write_text("".join(json.dumps({"rec": r, "seg": s, "mass": {"yes": 1.0, "no": 0.0}}) + "\n" for r, s in rows))
        (d / "probes.jsonl.sha256").write_text(f"{m0.sha_file(pf)}  probes.jsonl\n")
    return d


def test_classify_cells_and_guards():
    """D1 folder classes and the kept-cell rule; D2 scored-once guards; score-en folder check."""
    keys = {(0, 0), (0, 1)}
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        for rc in (2, 3, 4):
            assert e2b.classify(run_folder(root, f"a{rc}_FA_vi", rc), keys, "vi") == ("DROPPED_STOP", None)
        assert e2b.classify(run_folder(root, "t2_FA_vi", 7, prior=7), keys, "vi") == ("DROPPED_STOP", None)  # W1: 7 -> 7
        for prior in (5, 6, 8):  # W1: any other first fault before a clash is a second operator FAULT
            try:
                e2b.classify(run_folder(root, f"p{prior}_FA_vi", 7, prior=prior), keys, "vi")
            except SystemExit as e:
                assert "to a judge" in str(e), e
            else:
                raise AssertionError(f"rc {prior} -> 7 dropped")
        for rc in (7, 8):
            assert e2b.classify(run_folder(root, f"e{rc}_FA_en", rc), keys, "en") == ("EN_NOT_RUN", None)
        for name, rc in (("r5_FA_vi", 5), ("r6_FA_vi", 6), ("r7_FA_vi", 7), ("e6_FA_en", 6)):
            try:
                e2b.classify(run_folder(root, name, rc), keys, name[-2:])
            except SystemExit:
                continue
            raise AssertionError(f"operator FAULT rc {rc} accepted ({name})")
        st, rows = e2b.classify(run_folder(root, "ok_FA_vi", rows=sorted(keys)), keys, "vi")
        assert st == "DONE" and set(rows) == keys
        for name, rws in (("short_FA_vi", [(0, 0)]),):
            try:
                e2b.classify(run_folder(root, name, rows=rws), keys, "vi")
            except SystemExit:
                pass
            else:
                raise AssertionError("short coverage accepted")
        inc = run_folder(root, "inc_FA_vi", rows=sorted(keys))  # crashed before the sha write: no STOP, no sha file
        (inc / "probes.jsonl.sha256").unlink()
        try:
            e2b.classify(inc, keys, "vi")
        except SystemExit:
            pass
        else:
            raise AssertionError("incomplete folder accepted")
        bad = root / "bad.json"
        bad.write_text("{}")
        try:
            e2b.kept_cells(bad)
        except SystemExit:
            pass
        else:
            raise AssertionError("an unpinned rate.json accepted")
        g = root / "SCORED.json"
        e2b.once(g)
        g.write_text("{}")
        try:
            e2b.once(g)
        except SystemExit:
            pass
        else:
            raise AssertionError("second score accepted")
        runs = root / "runs"
        runs.mkdir()
        res = root / "res.json"
        res.write_text(json.dumps({"winner": "qwen3vl_8b|FA", "configs": {"qwen3vl_8b|FA": {"vote": False}}}))
        (runs / "SCORED.json").write_text(json.dumps({"res_sha256": m0.sha_file(res)}))
        (runs / "internvl3_8b_FA_en").mkdir()
        a = SimpleNamespace(runs=runs, res=res)
        try:
            e2b.cmd_score_en(a)
        except SystemExit as e:
            assert "only EN folder" in str(e), e
        else:
            raise AssertionError("score-en accepted a non-winner EN folder")
        (runs / "SCORED.json").write_text(json.dumps({"res_sha256": "0" * 64}))  # NB-1: res sha must match
        try:
            e2b.cmd_score_en(a)
        except SystemExit as e:
            assert "no SCORED.json for this res.json" in str(e), e
        else:
            raise AssertionError("score-en accepted a res.json whose sha differs from SCORED.json")
        try:  # NB-1: cmd_score refuses a second run at its call site
            e2b.cmd_score(SimpleNamespace(runs=runs, rate=None))
        except SystemExit as e:
            assert "SCORED.json exists" in str(e), e
        else:
            raise AssertionError("a second score was accepted")
        rate = e2b.ROOT / ".session_backup/2026-11-02/e2b_rate/rate.json"
        if rate.exists():  # laptop only: cmd_score refuses run folders that differ from the kept cells
            r2 = root / "runs2"
            for c in ("qwen25vl_7b_FA_vi", "internvl3_8b_FA_vi", "qwen3vl_8b_FA_vi", "aya_vision_8b_FA_vi"):
                (r2 / c).mkdir(parents=True)
            try:
                e2b.cmd_score(SimpleNamespace(runs=r2, rate=rate))
            except SystemExit as e:
                assert "differ from the kept cells" in str(e), e
            else:
                raise AssertionError("run folders that differ from the kept cells were accepted")
    rate = e2b.ROOT / ".session_backup/2026-11-02/e2b_rate/rate.json"
    if rate.exists():
        assert e2b.kept_cells(rate) == {("qwen25vl_7b", "FA"), ("internvl3_8b", "FA"), ("qwen3vl_8b", "FA"),
                                        ("qwen3vl_8b", "FB")}


def test_rerun_of():
    """W1 (§F): a re-run names its archived faulted folder; 7 -> 7 is the only drop path; no prior folder, an
    unstopped folder, a folder in the runs folder or of another cell, and a re-run of a re-run are refused."""
    keys = {(0, 0)}
    with tempfile.TemporaryDirectory() as d:
        runs, arch = Path(d) / "runs", Path(d) / "arch"
        cell = "qwen3vl_8b_FA_vi"
        first = run_folder(arch.mkdir(parents=True) or arch, cell + ".1", 7)
        out = e2b.prep_out(runs / cell, first, "f" * 64)
        assert json.loads((out / "launch.json").read_text())["w25_lists_sha256"] == "f" * 64  # NB-4
        rec = json.loads((out / "launch.json").read_text())["rerun_of"]
        assert rec["rc"] == 7 and rec["stop_sha256"] == m0.sha_file(first / "STOP")
        (out / "STOP").write_text(json.dumps({"rc": 7, "reason": "t"}))
        assert e2b.classify(out, keys, "vi") == ("DROPPED_STOP", None)
        live = run_folder(arch, "qwen3vl_8b_FB_vi.1")  # no STOP
        again = arch / (cell + ".2")
        out.rename(again)  # archive the re-run, then try to re-run it
        for prev, target in ((arch / "missing.1", cell), (live, "qwen3vl_8b_FB_vi"), (again, cell),
                             (first, "internvl3_8b_FA_vi")):
            try:
                e2b.prep_out(runs / target, prev)
            except SystemExit:
                continue
            raise AssertionError(f"re-run of {prev.name} accepted for {target}")
        try:  # one re-run per cell: the first faulted folder cannot be named a second time
            e2b.prep_out(runs / cell, first)
        except SystemExit as e:
            assert "re-run already" in str(e), e
        else:
            raise AssertionError("a second re-run of the same cell was accepted")
        try:  # a re-run of a re-run is refused even in a fresh runs folder (no marker there, e.g. a new host)
            e2b.prep_out(Path(d) / "runs_new_host" / cell, again)
        except SystemExit as e:
            assert "re-run itself" in str(e), e
        else:
            raise AssertionError("a re-run of a re-run was accepted")
        try:  # NB-1: an archive anywhere under the runs folder is refused
            e2b.prep_out(runs / "internvl3_8b_FA_vi", run_folder(runs / "deep" / "x", "internvl3_8b_FA_vi.1", 5))
        except SystemExit as e:
            assert "outside the runs folder" in str(e), e
        else:
            raise AssertionError("an archive nested under the runs folder was accepted")
        inside = run_folder(runs, cell + ".9", 7)
        try:
            e2b.prep_out(runs / cell, inside)
        except SystemExit:
            pass
        else:
            raise AssertionError("an archived folder inside the runs folder was accepted")


def test_rerun_scope_and_stops():
    """W4 (§F): only rc 5, rc 6 and a vi rc 7 may be re-run; a registered stop (vi rc 2/3/4, EN rc 7/8) is final and a
    refusal leaves no .rerun marker. NB-6: a stopped cell launches or resumes only as the declared re-run of that stop."""
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        cases = [("qwen3vl_8b_FA_vi", rc, False) for rc in (2, 3, 4)] + [("qwen3vl_8b_FA_en", rc, False) for rc in (7, 8)]
        cases += [("qwen3vl_8b_FA_vi", 5, True), ("qwen3vl_8b_FB_en", 6, True), ("internvl3_8b_FA_vi", 7, True)]
        for k, (cell, rc, ok) in enumerate(cases):
            runs = root / f"runs{k}"
            arch = run_folder(root / f"arch{k}", cell + ".1", rc)
            try:
                e2b.prep_out(runs / cell, arch)
            except SystemExit as e:
                assert not ok and "registered stop" in str(e), (cell, rc, e)
                assert not (runs / f".{cell}.rerun").exists(), "a refused re-run left a marker"
                continue
            assert ok, f"a registered stop rc {rc} on {cell} was accepted for a re-run"
            assert (runs / f".{cell}.rerun").exists()
        # NB-6: stop -> archive -> undeclared relaunch refused; declared re-run of that exact STOP accepted
        runs, cell = root / "runsS", "qwen25vl_7b_FA_vi"
        out = e2b.prep_out(runs / cell)
        assert e2b.guarded(out, lambda: m0.halt(out, e2b.RC_PROJ, "PROJECTION_STOP t")) == 3
        reg = root / "archS" / (cell + ".1")
        reg.parent.mkdir()
        out.rename(reg)
        for prev in (None, run_folder(root / "archT", cell + ".1", 5)):  # undeclared, or another folder's STOP
            try:
                e2b.prep_out(runs / cell, prev)
            except SystemExit as e:
                assert "stopped before" in str(e), e
            else:
                raise AssertionError(f"an undeclared relaunch of a stopped cell was accepted ({prev})")
        out = e2b.prep_out(runs / "qwen25vl_7b_FB_vi")  # a 5 -> declared re-run -> crash -> resume works
        e2b.guarded(out, lambda: m0.halt(out, e2b.RC_ENV, "ENV_FAULT t"))
        a5 = root / "archS" / "qwen25vl_7b_FB_vi.1"
        out.rename(a5)
        out = e2b.prep_out(runs / "qwen25vl_7b_FB_vi", a5)
        assert e2b.prep_out(runs / "qwen25vl_7b_FB_vi") == out  # the one resume keeps the declared re-run
        out = e2b.prep_out(runs / "internvl3_8b_FA_vi")  # STOP deleted by hand: the resume is still refused
        e2b.guarded(out, lambda: m0.halt(out, e2b.RC_PROJ, "PROJECTION_STOP t"))
        (out / "STOP").unlink()
        try:
            e2b.prep_out(runs / "internvl3_8b_FA_vi")
        except SystemExit as e:
            assert "stopped before" in str(e), e
        else:
            raise AssertionError("a resume after a deleted STOP was accepted")


def test_lost_run():
    """CC-225r2 Ruling 4 in code: a relaunch after a lost host is declared; it is the cell's one §F re-run, so a vi
    rc 7 on it goes to a judge (never a drop) and nothing may re-run it."""
    with tempfile.TemporaryDirectory() as d:
        root, cell = Path(d), "qwen3vl_8b_FA_vi"
        out = e2b.prep_out(root / "runs" / cell, lost="OPS-1103lost")
        assert json.loads((out / "launch.json").read_text())["rerun_of"] == {"lost_run": "OPS-1103lost", "rc": "LOST"}
        e2b.guarded(out, lambda: m0.halt(out, e2b.RC_TOKEN, "TOKEN_FAULT t"))
        try:
            e2b.classify(out, {(0, 0)}, "vi")
        except SystemExit as e:
            assert "to a judge" in str(e), e
        else:
            raise AssertionError("a vi rc 7 after a lost run was not sent to a judge")
        arch = root / "arch" / (cell + ".1")
        arch.parent.mkdir()
        out.rename(arch)
        for kw in ({"rerun_of": arch}, {"rerun_of": arch, "lost": "x"}):
            try:
                e2b.prep_out(root / "runs" / cell, **kw)
            except SystemExit:
                continue
            raise AssertionError(f"a re-run after a lost-run relaunch was accepted ({kw})")


def test_probe_cell_paths():
    """D6 pre-load CAP_STOP; D1 PIN_FAULT rc 6 and TOKEN_FAULT rc 7; D5b EN smoke rc 8; D5 rows carry start;
    D7 ENV_FAULT rc 5 and a redacted error.json."""
    S = {"probe": {1001, 1002}, "probe769": {1001, 1002}}
    segs = [{"rec": r, "seg": s, "image": 1001 + r, "text": "a dog"} for r in (0, 1) for s in range(6)]
    saved = e2b.load_cand, e2b.make_probe, e2b.image_loader
    good = lambda img, text: ({"yes": 0.7, "no": 0.2}, 5)  # noqa: E731
    low = lambda img, text: ({"yes": 0.1, "no": 0.1}, 5)  # noqa: E731

    def run(lang="vi", cap=1.0, load=None, mk=None, probe=good):
        with tempfile.TemporaryDirectory() as d:
            out = e2b.prep_out(Path(d) / "c")
            e2b.load_cand = load or (lambda k, h: (None, None))
            e2b.make_probe = mk or (lambda p, n, f, g: (probe, {"yes": [1], "no": [2]}))
            e2b.image_loader = lambda folder: (lambda iid: None)
            a = SimpleNamespace(cap_h=cap, cand="qwen3vl_8b", hub=None, form="FA", lang=lang, images=None)
            rc = e2b.probe_cell(a, out, S, segs, 0.08)
            stop = json.loads((out / "STOP").read_text())["rc"] if (out / "STOP").exists() else None
            rows = [json.loads(x) for x in (out / "probes.jsonl").read_text().splitlines()] if (out / "probes.jsonl").exists() else []
            return rc, stop, rows

    def fault(*_a):
        raise e2b.Fault("x")
    try:
        assert run(cap=0.0)[:2] == (4, 4)
        assert run(load=fault)[:2] == (6, 6)
        assert run(mk=fault)[:2] == (7, 7)
        assert run(lang="en", probe=low)[:2] == (8, 8)
        rc, stop, rows = run()
        assert rc == 0 and stop is None and len(rows) == 12 and all(r["start"] == 1 for r in rows)
    finally:
        e2b.load_cand, e2b.make_probe, e2b.image_loader = saved
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "qwen3vl_8b_FA_vi"
        out.mkdir()

        def imp():
            raise ModuleNotFoundError("setuptools")
        assert e2b.guarded(out, imp) == 5 and json.loads((out / "STOP").read_text())["rc"] == 5
        mk = json.loads(e2b.stopped_marker(out).read_text())  # NB-6: the stop is marked beside the cell folder
        assert mk == {"rc": 5, "stop_sha256": m0.sha_file(out / "STOP")}
        (out / "STOP").unlink()

        def other():
            raise ValueError("token hf_" + "A" * 34)
        try:
            e2b.guarded(out, other)
        except ValueError:
            err = (out / "error.json").read_text()
            assert "hf_" + "A" * 34 not in err and "<redacted>" in err
        else:
            raise AssertionError("a crash was swallowed")
    # W2: after W25 drops the order is M0's order over the 769 with the drops removed (registered EN smoke items)
    ids = set(range(2001, 2013))
    full = m0.image_order(ids)
    S2 = {"probe769": ids, "probe": ids - set(full[:2])}
    want = [i for i in full if i in S2["probe"]][:e2b.N_SMOKE]
    assert want != m0.image_order(S2["probe"])[:e2b.N_SMOKE]  # the test can tell the two orders apart
    seen: list = []
    with tempfile.TemporaryDirectory() as d:
        out = e2b.prep_out(Path(d) / "c")
        e2b.load_cand, e2b.make_probe = (lambda k, h: (None, None)), (lambda p, n, f, g: (rec_probe, {}))
        e2b.image_loader = lambda folder: (lambda iid: iid)

        def rec_probe(img, text):
            seen.append(img)
            return {"yes": 0.7, "no": 0.2}, 5
        try:
            a = SimpleNamespace(cap_h=1.0, cand="qwen3vl_8b", hub=None, form="FA", lang="en", images=None)
            segs2 = [{"rec": i, "seg": 0, "image": i, "text": "a dog"} for i in sorted(S2["probe"])]
            assert e2b.probe_cell(a, out, S2, segs2, 0.08) == 0
        finally:
            e2b.load_cand, e2b.make_probe, e2b.image_loader = saved
    assert seen[:e2b.N_SMOKE] == want, (seen[:e2b.N_SMOKE], want)
    assert e2b.redact("x hf_" + "b" * 31 + " y") == "x <redacted> y"
    assert e2b.smoke_ok({"a": 0.3, "b": 0.2}) and not e2b.smoke_ok({"a": 0.3, "b": 0.1})
    assert not e2b.smoke_ok({"a": float("nan"), "b": 0.9})


def test_job_caps():
    """D10: the job's fixed CAPS table equals AMENDMENT_1 section C (CC-223 W4): 0.7 / 2.3 / 0.6 / 0.6 GPU-h."""
    import re as _re

    job = (HERE / "e2b_job.sh").read_text()
    caps = dict(_re.findall(r"\[(\w+)\]=([\d.]+)", _re.search(r"declare -A CAPS=\((.*?)\)", job).group(1)))
    assert caps == {"qwen25vl_7b_FA": "0.7", "internvl3_8b_FA": "2.3", "qwen3vl_8b_FA": "0.6", "qwen3vl_8b_FB": "0.6"}, caps
    block = job.split('if [ "$SUB" = probe ]')[1].split("\nfi\n")[0]
    assert "unset HF_TOKEN" in block and "${HF_TOKEN" not in block  # NB-4: no token in the probe environment


def test_w25_dispositions():
    """CC-223r3 R-a / R-b and the precedence drop > hold > count (NB-5); the positive control runs first."""
    import e2b_w25 as W

    assert set(W.DROP) >= {"kv4224", "kv_ut2532_Ra"} and "kv_refused_Rb" in W.HOLD and "kv_a_touched" in W.COUNT
    assert W.KV_SPLIT_N == {"kv4224": 4224, "kv_ut2532_Ra": 130, "kv_refused_Rb": 130, "kv_a_touched": 516}
    ids = [1, 2, 3, 4, 5]
    hits = {g: [False] * 5 for g in W.DROP + W.HOLD + W.COUNT}
    hits["kv4224"][1] = hits["karpathy_test"][1] = True        # 2: drop > hold
    hits["kv_refused_Rb"][2] = hits["kv_a_touched"][2] = True  # 3: hold > count
    hits["kv_a_touched"][3] = True                             # 4: count
    hits["kv_ut2532_Ra"][0] = True                             # 1: held, no disposition
    assert W.dispose(ids, hits, {1}) == {"drop": [2], "hold": [3], "count": [4]}
    W.control(ids, [True, False, False, False, False], {1}, {1})
    for hit, k2 in (([False] * 5, {1}), ([True] + [False] * 4, set())):
        try:
            W.control(ids, hit, {1}, k2)
        except SystemExit as e:
            assert "FAULT positive control" in str(e)
        else:
            raise AssertionError("positive-control FAULT not raised")


def segs_fixture(n_img=60, seed=3):
    rng, out = random.Random(seed), []
    for i in range(n_img):
        for j in range(8):
            out.append({"rec": i, "seg": j, "image": 1000 + i, "y": int(rng.random() < 0.3),
                        "t2": ("object", "number")[j % 2], "half": e2b.half(1000 + i)})
    return out


def test_bootstrap_and_score_rules():
    segs = segs_fixture()
    lab = {e2b.key(s): ("R" if s["y"] else "S") for s in segs}
    f = lambda s: lab[e2b.key(s)]  # noqa: E731
    ci = e2b.paired_ci(e2b.per_image_counts(segs, f, f), B=500)
    assert ci["dprec"] == [0.0, 0.0] and ci["dret"] == [0.0, 0.0] and ci["dropped"] == 0
    assert ci == e2b.paired_ci(e2b.per_image_counts(segs, f, f), B=500)  # seeded
    flip = lambda s: "R" if (s["y"] or s["rec"] % 3 == 0) else "S"  # noqa: E731
    ci2 = e2b.paired_ci(e2b.per_image_counts(segs, f, flip), B=500)
    assert ci2["dprec"][0] > 0 and ci2["dret"][1] > 0
    rng = random.Random(4)
    pv = {e2b.key(s): min(0.99, max(0.01, rng.gauss(0.35 if s["y"] else 0.7, 0.2))) for s in segs}
    mass = {e2b.key(s): {"yes": pv[e2b.key(s)] * 0.9, "no": (1 - pv[e2b.key(s)]) * 0.9} for s in segs}
    fe, thr = e2b.config_fn(mass, "FA", segs)
    R = e2b.tune_recall(fe, segs)
    vf = e2b.vintern_fn(pv, segs, R)
    for t in e2b.PRIMARY:  # same scores -> matched Vintern rejects at least the same tune false probes
        tu = e2b.tune_of(segs, t)
        assert e2b.recall([vf(s) == "R" for s in tu], [s["y"] for s in tu]) >= R[t] - 1e-9
    fbm = {k: {"S": v["yes"], "U": 0.0, "R": v["no"]} for k, v in mass.items()}
    f3 = e2b.config_fn(fbm, "FB", segs)[0]
    ab = e2b.ablation("FB", fbm, f3, e2b.tune_recall(f3, segs), segs, segs)
    assert set(ab) == {"three_label", "binary"} and all(ab["binary"][t]["U"] == 0 for t in e2b.PRIMARY)


def test_guards():
    try:
        e2b.rate_row(cand="x", form="FA", i=0, sec=0.1, n_tok=5, phase="rate", p_yes=0.5)
    except e2b.Fault:
        pass
    else:
        raise AssertionError("rate row accepted p_yes")
    assert set(e2b.rate_row(cand="x", form="FA", i=0, sec=0.1, n_tok=5, phase="rate")) <= e2b.RATE_KEYS
    assert e2b.RATE_KEYS.isdisjoint({"p_yes", "mass", "text", "label", "pS", "pU", "pR"})
    assert e2b.summarise([{"form": "FA", "phase": "rate", "sec": s} for s in (0.4, 0.6)], "FA")["keep"] is True
    assert e2b.summarise([{"form": "FA", "phase": "rate", "sec": s} for s in (0.5, 0.6)], "FA")["keep"] is False
    assert not e2b.gpu_busy(0, False) and e2b.gpu_busy(1, False) and not e2b.gpu_busy(1, True) and e2b.gpu_busy(2, True)
    assert abs(e2b.projected_h(1.0, 7200, 0.5) - 2.0) < 1e-12
    try:
        e2b.prep_out(e2b.ROOT / "tmp_out")
    except SystemExit:
        pass
    else:
        raise AssertionError("OUT inside the repo accepted")
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "o"
        e2b.prep_out(out)
        t0 = json.loads((out / "launch.json").read_text())["t0"]
        e2b.prep_out(out)  # the one resume keeps t0
        assert json.loads((out / "launch.json").read_text())["t0"] == t0
        try:
            e2b.prep_out(out)
        except SystemExit:
            pass
        else:
            raise AssertionError("second resume accepted")
        (out / "STOP").write_text("{}")
        try:
            m0.refuse_if_stopped(out)
        except SystemExit:
            pass
        else:
            raise AssertionError("stopped run not refused")
    assert e2b.KEEP_S * 1.7 <= 0.85 + 1e-12 and e2b.CAP_RATE_H == 3.0 and e2b.N_RATE == 200


def test_plan_file():
    if not e2b.PLAN.exists():
        print("SKIP plan file: not built yet")
        return
    plan = json.loads(e2b.PLAN.read_text(encoding="utf-8"))
    assert plan["split_examples"] == {str(i): e2b.half(i) for i in (139, 285, 632, 724, 776)}
    assert plan["counts"]["selection"] == {"images": 663, "segments": 13813, "inaccurate": 3993}
    assert plan["counts"]["probe"] == {"images": 769, "segments": 16027, "inaccurate": 4605}
    assert len(plan["probe_images"]) == 769 and set(plan["rate"]["images"]) <= set(plan["probe_images"])
    assert len(plan["rate"]["probes"]) == 200 and len(plan["rate"]["images"]) == len({p[2] for p in plan["rate"]["probes"]})
    held = {int(x) for x in (e2b.M0DIR / "selection_excluded_ids.txt").read_text().split()}
    assert not {p[2] for p in plan["rate"]["probes"]} & held  # no held-out (incl. Karpathy test) image is timed
    assert plan["prompts_sha256"] == {f"{f}_{g}": m0.sha_text(e2b.prompt(f, g, "{s}")) for f in e2b.FORMS for g in e2b.LANGS}
    assert not any(k in json.dumps(plan) for k in ('"text"', '"caption"'))


def main() -> int:
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
