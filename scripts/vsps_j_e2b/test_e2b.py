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
    row = lambda c, f, d, u=5.0, r=0.0, v=False: {"cand": c, "form": f, "dprec": d, "U": u, "dret": r, "vote": v}  # noqa: E731
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
