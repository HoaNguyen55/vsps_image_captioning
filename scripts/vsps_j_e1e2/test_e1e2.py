#!/usr/bin/env python
"""CPU selftest for scripts/vsps_j_e1e2 (no weights, no downloaded data; the tracked sample records only).

    <venv>/bin/python -I scripts/vsps_j_e1e2/test_e1e2.py
"""
from __future__ import annotations

import json
import math
import os
import random
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import e1e2  # noqa: E402
import m0  # noqa: E402
import ret  # noqa: E402

SAMPLES = sorted((e1e2.ROOT / "data/stage1_records").glob("sample_*.json"))


def samples() -> list:
    return [json.loads(p.read_text(encoding="utf-8")) for p in SAMPLES]


def test_keys_and_prompt():
    from rescap.vlm.base import VLM
    from rescap.vlm.replay import ReplayVLM

    for q in ("Trong ảnh có A  B không?", "Có đúng là X KHÔNG có Y không."):
        assert e1e2.qkey(q) == ReplayVLM._key(q)
    seen = []

    class Cap(VLM):
        name = "cap"

        def _generate(self, image, prompt, *, max_new_tokens, temperature):
            seen.append(prompt)
            return "Có.", None
    q = "Trong ảnh có A B không"
    Cap().probe_yes_no(None, q)
    assert seen == [m0.instruct(q)], "the logit probe must ask the K=5 path's exact prompt"
    assert m0.chat_args(q, [], [], 3)[1] == f"<image>\n{seen[0]}"


def test_replay_and_metrics():
    recs = samples()
    assert recs, "tracked sample records missing"
    prep = e1e2.kt_prepare(recs)
    st_rec = [[p["verification"]["status"] for p in r["propositions"]] for r in recs]
    m = e1e2.kt_metrics(prep, st_rec)
    r = ret.rates(ret.counts(recs))
    assert abs(m["retention"] - r["retention"]) < 1e-9 and abs(m["mirror"] - r["mirror"]) < 1e-9
    for rec in recs:
        q = e1e2.vintern_questions(rec)
        assert q, "sample record has Vintern probes"
        yes = {k: 1.0 if e1e2.is_yes(v.get("answer")) else 0.0 for k, v in q.items()}
        st_hi, miss = e1e2.replay(rec, yes, {})
        assert miss == 0 and len(st_hi) == len(rec["propositions"])
        st_lo, _ = e1e2.replay(rec, dict.fromkeys(q, 0.0), {})
        assert st_lo.count("SUPPORTED") == 0 and st_hi.count("SUPPORTED") >= st_lo.count("SUPPORTED")
        _st, miss = e1e2.replay(rec, {}, {})
        assert miss > 0, "an empty logit table must register misses"
        loose, _ = e1e2.replay(rec, yes, dict.fromkeys(e1e2.TYPES, 0.5))
        tight, _ = e1e2.replay(rec, yes, dict.fromkeys(e1e2.TYPES, 0.95))
        assert loose.count("SUPPORTED") >= tight.count("SUPPORTED")


def test_select_rule():
    def ev(s):  # retention rises as S_hi falls; P falls below the floor for entity below 0.6
        ret_ = sum(1 - v for v in s.values())
        p = 40.0 if s["entity"] >= 0.6 else 30.0
        return {"P": p, "retention": ret_}
    s_hi, trace = e1e2.select_s_hi(ev)
    assert s_hi["entity"] == 0.6 and all(s_hi[t] == 0.5 for t in e1e2.TYPES[1:])
    assert len(trace) == e1e2.PASSES * len(e1e2.TYPES) * len(e1e2.GRID)
    s_hi, _ = e1e2.select_s_hi(lambda s: {"P": 50.0, "retention": 1.0})
    assert all(v == e1e2.GRID[-1] for v in s_hi.values()), "ties go to the larger S_hi"
    s_hi, _ = e1e2.select_s_hi(lambda s: {"P": 10.0, "retention": 1.0})
    assert all(v == e1e2.S_HI_V1 for v in s_hi.values()), "no feasible value keeps v1"


def test_tcoco_and_kappa():
    units = [(1, True, "REJECTED"), (1, True, "SUPPORTED"), (2, False, "SUPPORTED"), (2, False, "UNCERTAIN")]
    r = e1e2.tcoco_rates(units)
    assert (r["n_absent"], r["n_present"], r["DR"], r["DR_strict"], r["RT"]) == (2, 2, 50.0, 50.0, 50.0)
    ci = e1e2.cluster_ci({"a": units, "b": units}, "a")
    assert ci["b.dDR"] == [0.0, 0.0] and ci == e1e2.cluster_ci({"a": units, "b": units}, "a")
    sys.path.insert(0, str(e1e2.ROOT / "scripts"))
    import gate_t05

    rng = random.Random(1)
    a = [rng.random() < 0.6 for _ in range(500)]
    b = [x if rng.random() < 0.85 else not x for x in a]
    assert abs(e1e2.kappa(a, b) - gate_t05.kappa(a, b)) < 1e-12


def test_run_pass_guards():
    work = [(f"im{i}", [(f"q{j}", f"Q{j}") for j in range(3)]) for i in range(6)]
    with tempfile.TemporaryDirectory() as d:
        out = e1e2.prep_out(Path(d) / "pre")
        rc = e1e2.run_pass(lambda n, q: ("C", 0.9, 0.99), out, work, lambda n: n, 0.0, 2, 1e6)
        assert rc == 3 and (out / m0.STOP).exists()
        try:
            e1e2.prep_out(out)
            raise AssertionError("a stopped run must refuse to resume")
        except SystemExit as e:
            assert "REFUSED" in str(e)
        out = e1e2.prep_out(Path(d) / "nan")
        rc = e1e2.run_pass(lambda n, q: ("C", float("nan"), 0.0), out, work, lambda n: n, 5.0, 2, 0.0)
        assert rc == 2
        try:
            m0.check_scorable(out)
            raise AssertionError("a FAULTed run must not score")
        except SystemExit as e:
            assert "REFUSED" in str(e)
        out = e1e2.prep_out(Path(d) / "ok")
        assert e1e2.run_pass(lambda n, q: ("C", 0.9, 0.99), out, work[:3], lambda n: n, 5.0, 2, 0.0) == 0
        assert e1e2.run_pass(lambda n, q: ("C", 0.9, 0.99), out, work, lambda n: n, 5.0, 2, 0.0) == 0  # crash-resume
        rows = [json.loads(x) for x in (out / "probes.jsonl").read_text().splitlines()]
        assert len(rows) == 18 and len({(r["image"], r["q"]) for r in rows}) == 18
        (out / "probes.jsonl.sha256").write_text(f"{m0.sha_file(out / 'probes.jsonl')}  probes.jsonl\n")
        assert len(m0.check_scorable(out)) == 18
        assert json.loads((out / "projection.json").read_text())["stop"] is False


def test_score_isolation():
    """A stopped E1b never blocks the E1a score, and the reverse (PREREG section 6)."""
    import argparse

    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        (out / "e1b").mkdir()
        m0.halt(out / "e1b", 4, "CAP_STOP test", 1)
        res_f = out / "res.json"
        e1e2.cmd_score(argparse.Namespace(out=out, res=res_f))
        res = json.loads(res_f.read_text())
        assert "REFUSED" in res["e1b_e2_kt"]["not_scored"]
        assert "INCOMPLETE" in res["e1a_tcoco"]["not_scored"], "E1a is still scored (here: no records yet)"


def _stage(d: Path) -> Path:
    from PIL import Image

    (d / "datasets/ktvic/images").mkdir(parents=True)
    for i in (1, 2, 3):
        Image.new("RGB", (64, 48), (i * 60, 90, 120)).save(d / f"datasets/ktvic/images/{i:012d}.jpg")
    (d / "datasets/ktvic/t.json").write_text(json.dumps(
        {"images": [{"id": i, "file_name": f"{i:012d}.jpg"} for i in (1, 2, 3)], "annotations": []}))
    return d


def test_sidelog_stage1():
    """generate_stage1.main() under the side-log on mock models: records unchanged in shape, one logit row per probe
    call, coverage complete; a cap Halt writes the marker and no record for the stopped image."""
    from rescap.vlm.mock import MockVLM

    with tempfile.TemporaryDirectory() as d:
        os.environ["NCS_DATA"] = str(_stage(Path(d)))
        sys.modules.pop("generate_stage1", None)
        order = [f"{i:012d}.jpg" for i in (1, 2, 3)]
        fake = lambda self, image, q: ("C", 0.9, 0.99)  # noqa: E731
        out = e1e2.prep_out(Path(d) / "out" / "e1a")
        rc = e1e2.run_stage1(out, "t.json", MockVLM, fake, order, 5.0, 20, "mock", "mock")
        recs = [json.loads(p.read_text()) for p in e1e2.record_files(out / "records")]
        assert rc == 0 and len(recs) == 3
        rows = [json.loads(x) for x in (out / "probes.jsonl").read_text().splitlines()]
        assert rows and all(r["image"] in order and math.isfinite(r["p_yes"]) for r in rows)
        fid = e1e2.fidelity(recs, e1e2.logit_tables(rows), model="mock")  # raises INCOMPLETE on any uncovered question
        assert fid["n"] == sum(len(e1e2.vintern_questions(r, "mock")) for r in recs) > 0
        assert MockVLM.probe_yes_no.__name__ != "pyn", "the side-log must be uninstalled after the run"
        out2 = e1e2.prep_out(Path(d) / "out2" / "e1a")
        rc = e1e2.run_stage1(out2, "t.json", MockVLM, fake, order, -1.0, 20, "mock", "mock")
        assert rc == 4 and (out2 / m0.STOP).exists() and not e1e2.record_files(out2 / "records")


        def broken(self, image, q):
            raise RuntimeError("load error")  # caught per image by main(); the 2nd image open must FAULT
        orig = MockVLM.describe
        MockVLM.describe = broken
        try:
            out3 = e1e2.prep_out(Path(d) / "out3" / "e1a")
            rc = e1e2.run_stage1(out3, "t.json", MockVLM, fake, order, 5.0, 20, "mock", "mock")
        finally:
            MockVLM.describe = orig
        assert rc == 2 and "first image" in (out3 / m0.STOP).read_text()
        sys.modules.pop("generate_stage1", None)


def main() -> int:
    for t in (test_keys_and_prompt, test_replay_and_metrics, test_select_rule, test_tcoco_and_kappa,
              test_run_pass_guards, test_score_isolation, test_sidelog_stage1):
        t()
    print("selftest ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
