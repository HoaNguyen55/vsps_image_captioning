"""Self-test and mutants of the C-CONF host decoder, token guard and ledger writer (c_conf.py) on synthetic fixtures.

Runs on a rented host only (the investigator's rule of 2026-11-11), from the repository checkout, with the decoder's
interpreter (venv-lb, as the C-ATTR self-test). Reads no study file: every token, decision, run, list and name below is
written into a temporary folder by this script; OV-test is never staged, and ctest (whose import hashes the pinned TSV)
is never imported.
    env -u PYTHONPATH /root/venv-lb/bin/python -I -B scripts/c_conf/test_c_conf.py   # self-test, then every mutant must die
§11.1 row 2: OV-test names refused without a token and admitted with one for a listed backbone only; a token without
the ledger line's LOG id refused; XM-test2500 and Flickr30K names refused always; run ids unique per arm, draw and
set; a second decode of an existing run id refused; two arms' prompts differ only through the example block; batch
size other than 1 refused. Mutants: the six of §11.1 row 2 plus seven listed in MUTANTS.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
REAL_ROOT = HERE.parents[1]
FILES = ("c_conf.py", "c_conf_score.py", "c_conf_arms.py", "c_conf_lists.py")
ROOT_LINE = "ROOT = Path(__file__).resolve().parents[2]"


def refused(fn, word: str = "REFUSED") -> bool:
    """True iff fn raises SystemExit whose text holds word; any other exception escapes (and fails the self-test)."""
    try:
        fn()
    except SystemExit as e:
        assert word in str(e), e
        return True
    return False


def tokens(d: Path, entered: list[str]) -> dict[str, Path]:
    """A rehearsal decision beside six tokens: good, and five that must be refused."""
    dec = d / "C_CONF_REHEARSAL_DECISION.json"
    dec.write_text(json.dumps({"entered": entered, "look": True}), encoding="utf-8")
    h = hashlib.sha256(dec.read_bytes()).hexdigest()
    good = {"rehearsal_decision_sha256": h, "yes_log_id": "OPS-yes", "ledger_line_log_id": "OPS-ledger",
            "backbones": entered}
    kinds = {"good": good, "three_fields": {k: v for k, v in good.items() if k != "ledger_line_log_id"},
             "wrong_sha": {**good, "rehearsal_decision_sha256": "0" * 64}, "no_ledger_id": {**good, "ledger_line_log_id": ""},
             "other_backbones": {**good, "backbones": entered[:1]}, "five_fields": {**good, "extra": 1}}
    out = {}
    for k, t in kinds.items():
        out[k] = d / f"{k}.json"
        out[k].write_text(json.dumps(t), encoding="utf-8")
    return out


def selftest(A) -> list[str]:
    ok = []
    ns = argparse.Namespace
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        A.OV_STAGE = d / "c_conf_ov_test"  # never the host's folder
        tk = tokens(d, ["qwen25vl_7b", "aya_vision_8b"])
        # ---- token (G3, §6.4 item 5)
        A.ADMITTED = None
        assert refused(A.ov_gate), "no OV-test name or byte before a token is admitted"
        assert refused(lambda: A.admit(None)) and A.ADMITTED is None
        for k in ("three_fields", "wrong_sha", "no_ledger_id", "other_backbones", "five_fields"):
            A.ADMITTED = None
            assert refused(lambda: A.admit(tk[k])) and A.ADMITTED is None, f"token {k} must be refused"
        t = A.admit(tk["good"])  # the decision file is found beside the token
        assert t["backbones"] == ["qwen25vl_7b", "aya_vision_8b"] and A.ov_gate("aya_vision_8b") and A.ov_gate(None)
        assert refused(lambda: A.ov_gate("internvl3_8b")), "a backbone the token does not list is refused"
        moved = d / "elsewhere"
        moved.mkdir()
        shutil.copy(tk["good"], moved / "t.json")
        A.ADMITTED = None
        A.admit(moved / "t.json", d / "C_CONF_REHEARSAL_DECISION.json")  # --decision given explicitly
        ok.append("token: four fields, decision sha256, entered backbones, both LOG ids; one gate; backbone listed")
        # ---- refusals (§5.4)
        cl = {"sets": {"xm_test2500": [["x1", "xm1.jpg", "h"]], "ov_dev_b": [["d1.jpg", "d1.jpg", "h"]]},
              "refuse": {"openviic_files": ["t1.jpg", "d1.jpg"]}}
        f30k = {"refuse": {"test": ["f_test.jpg"], "val": ["f_val.jpg"]}}
        no, yes = A.refused_names(cl, f30k), A.refused_names(cl, f30k, admitted=True)
        assert {"t1.jpg", "xm1.jpg", "f_test.jpg", "f_val.jpg"} <= no and "d1.jpg" not in no
        assert {"xm1.jpg", "f_test.jpg", "f_val.jpg"} <= yes and "t1.jpg" not in yes, "XM and Flickr30K refused always"
        cfg_no, cfg_yes = (A.iso_config(d / "ncs", d / "outputs", [], r) for r in (no, yes))
        stage_img = A.OV_STAGE / "images/t1.jpg"
        assert A.iso_denied(stage_img, cfg_no) and A.iso_denied(stage_img, cfg_yes) is None
        assert A.iso_denied(d / "x/xm1.jpg", cfg_yes) and A.iso_denied(d / "x/f_val.jpg", cfg_yes)
        g = d / "g"
        g.mkdir()
        (g / "t1.jpg").write_text("")
        assert A.guard_problems([g], no) == [str(g / "t1.jpg")] and A.guard_problems([g], yes) == []
        # CC-466 W2: a refused name passes only as the pinned KTVIC file directly in datasets/ktvic/images
        kt = d / "ncs/datasets/ktvic/images"
        kt.mkdir(parents=True)
        cfg_kt = A.iso_config(d / "ncs", d / "outputs", [], no, kt_pins={"t1.jpg": hashlib.sha256(b"k").hexdigest()})
        (kt / "t1.jpg").write_bytes(b"k")
        assert A.guard_problems([kt], no, cfg_kt) == [], "(1) the pinned KTVIC file in its folder passes"
        (kt / "t1.jpg").write_bytes(b"other")
        assert A.guard_problems([kt], no, cfg_kt) == [str(kt / "t1.jpg")], "(2) other bytes under the name: refused"
        g3 = d / "g3"
        g3.mkdir()
        (g3 / "t1.jpg").write_bytes(b"k")
        assert A.guard_problems([g3], no, cfg_kt) == [str(g3 / "t1.jpg")], "(3) the pinned bytes elsewhere: refused"
        (kt / "t1.jpg").unlink()
        (kt / "t1.jpg").symlink_to(g3 / "t1.jpg")
        assert A.guard_problems([kt], no, cfg_kt) == [str(kt / "t1.jpg")], "(4) a symlink in the folder: refused"
        ok.append("refusals: OV-test names without a token only; XM-test2500 and Flickr30K always")
        # ---- run ids and job names
        rid = lambda **kw: A.run_id_of(ns(**{"model": "qwen25vl_7b", "set": "ov_dev_b", "arm": "ret", "k": 8,  # noqa: E731
                                           "order": "first", "tpl": "T1", "draw": 0, "memory": "vi",
                                           "redecode": None, "limit": 0, **kw}))
        ids = {rid(set=s, arm=arm, draw=dr, redecode=rd) for s in A.SETS
               for arm, draws in (("zs", (0,)), ("ret", (0,)), ("rand", A.DRAWS), ("perm", A.PERMS)) for dr in draws
               for rd in (None, "rev50", "fwd50")}
        assert len(ids) == 3 * 7 * 3 and all("b1" in x.split("-") for x in ids), "unique per set, arm, draw; '-b1'"
        assert rid(redecode="fwd50") == "cc_qwen25vl_7b_ov_dev_b-ret-k8-first-T1-mvi-b1-fwd50", "the job's out_of name"
        assert rid(redecode="fwd50", limit=2).endswith("-mvi-b1-fwd50-smoke")
        lm = lambda **kw: A.lmcap_run_id(ns(**{"variant": "ri", "set": "ov_dev_b", "memory": "vi", "redecode": None,  # noqa: E731
                                             "limit": 0, **kw}))
        assert lm(redecode="fwd50") == "cc_lmcap-ri_ov_dev_b-mvi-fwd50", "the job's lm_out name"
        assert A.d1_ref(rid(redecode="fwd50")) == rid(redecode="rev50") and \
            A.d1_ref(lm(redecode="fwd50")) == lm(redecode="rev50") and refused(lambda: A.d1_ref(rid()), "not a D1")
        ok.append("run ids: unique per set, arm and draw; '-b1'; the job's D1 names; D1 reference = rev50")
        # ---- decode refusals before anything is read
        out = d / "outputs/c_conf_t/out"
        out.mkdir(parents=True)
        base = {"model": "qwen25vl_7b", "set": "ov_dev_b", "arm": "ret", "k": 8, "order": "first", "tpl": "T1",
                "draw": 0, "memory": "vi", "redecode": None, "limit": 2, "batch1": True, "dry_run": True, "token": None,
                "decision": None, "out_dir": out, "snapshot": d, "c_lists": d / "none.json", "images": d}
        dec = lambda **kw: A.cmd_decode(ns(**{**base, **kw}))  # noqa: E731
        assert refused(lambda: dec(batch1=False), "batch size 1"), "batch size other than 1 refused"
        (out / f"{A.run_id_of(ns(**base))}.preds.json").write_text("{}")
        assert refused(dec, "exists"), "a second decode of an existing run id refused"
        assert refused(lambda: dec(arm="rand", k=4)), "rand uses the k, order and tail of the backbone's ret"
        assert refused(lambda: dec(arm="perm", draw=0), "not registered")
        assert refused(lambda: dec(set="ov_carve", redecode="fwd50")), "D1 on OV-dev-B ret only"
        A.ADMITTED = None
        assert refused(lambda: dec(set="ov_test")), "OV-test refused without a token"
        assert refused(lambda: dec(set="ov_test", token=tk["three_fields"]))
        A.ADMITTED = None
        assert refused(lambda: dec(set="ov_test", model="internvl3_8b", k=4, order="last", tpl="T2", token=tk["good"]))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            dec(set="ov_test", model="aya_vision_8b", k=4, order="last", tpl="T1", token=tk["good"])
        assert "DRY" in buf.getvalue(), "admitted for a listed backbone"
        A.ADMITTED = None
        lmc = lambda **kw: A.cmd_lmcap(ns(**{**base, "variant": "ri", **kw}))  # noqa: E731
        assert refused(lambda: lmc(set="ov_test")) and refused(lambda: lmc(batch1=False), "batch size 1")
        ok.append("decode and LMCap refusals before any read: batch 1, run once, ret's k / order / tail, token")
        # ---- custody helpers of the job (names only, stage check dry)
        A.ADMITTED = None
        with contextlib.redirect_stdout(io.StringIO()):
            A.cmd_token(ns(token=tk["good"], decision=None, names_only=True))
            A.OV_STAGE.mkdir()
            assert refused(lambda: A.cmd_token(ns(token=tk["good"], decision=None, names_only=True)))
            A.ADMITTED = None
            assert refused(lambda: A.cmd_stagecheck(ns(token=tk["wrong_sha"], decision=None, dir=A.OV_STAGE,
                                                       dry_run=True)))
            A.cmd_stagecheck(ns(token=tk["good"], decision=None, dir=A.OV_STAGE, dry_run=True))
        ok.append("token --names-only refuses a staged OV-test folder; stagecheck needs the token")
        # ---- examples, prompts, LMCap skip sets
        ex = {"ret": {"q": ["r1", "r2", "r3", "r4"]}, "rand": {"0": {"q": ["a1", "a2", "a3", "a4", "a5"]}},
              "perm": {"1": {"q": ["p1", "p2", "p3", "p4"]}, "2": {"q": ["s1", "s2", "s3", "s4"]}}}
        assert A.example_ids("perm", 3, "first", "q", ex, 1) == ["p1", "p2", "p3"], "perm from the perm list"
        assert A.example_ids("perm", 3, "last", "q", ex, 2) == ["s3", "s2", "s1"], "perm: k-prefix and order of ret"
        assert A.example_ids("ret", 2, "last", "q", ex, 0) == ["r2", "r1"] and A.example_ids("zs", 2, None, "q", ex, 0) == []
        assert A.example_ids("rand", 4, "first", "q", ex, 0) == ["a1", "a2", "a3", "a4"]
        pa, pb = A.C.prompt("T1", ["x y", "z"]), A.C.prompt("T1", ["u v w", "t"])
        assert A.C.sha(pa) != A.C.sha(pb) and A.skeleton(pa) == A.skeleton(pb) == A.skeleton(A.C.prompt("T1", []))
        assert A.skeleton(pa + "\nthêm") != A.skeleton(A.C.prompt("T1", [])), "a change outside the example block"
        near = {"q": {"n1"}, "r": set()}
        assert A.lmcap_skip("q", ["s1"], near, {"q": "own_q"}) == {"s1", "n1", "own_q"}, "own cluster skipped by id"
        assert A.lmcap_skip("r", ["s1"], near, {}) == {"s1"}
        assert A.lmcap_query("rand", "q", ex, {"a2"}, ["r9"]) == ["a1", "a3", "a4", "a5"] and \
            A.lmcap_query("ri", "q", ex, set(), ["r9"]) == ["r9"]
        ok.append("examples (perm from its list), A3 prompt shape, LMCap skip set (shots, near cut, own cluster)")
        # ---- tau and the ledger writer
        assert all(A.TAU[m] == "-inf" for m in ("qwen25vl_7b", "internvl3_8b", "aya_vision_8b")), "binding 10"
        mk = lambda name, **kw: {"schema": A.SCHEMA, "dataset": "ov_carve", "run_id": name, "model": "internvl3_8b",  # noqa: E731
                                 "spec": {"arm": "ret", "draw": 0, "tau": "-inf"}, "predictions": {"a": "x"}, **kw}
        runs = {"ok": mk("cc_ok"), "tau": mk("cc_t", spec={"arm": "ret", "draw": 0, "tau": "0.10"}),
                "d1": mk("cc_x-fwd50"), "other": mk("cc_o", dataset="ov_dev_b")}
        for k, r in runs.items():
            (d / f"{k}.json").write_text(json.dumps(r), encoding="utf-8")
        sr = lambda k, s="ov_carve": A.score_runs(ns(set=s, runs=[d / f"{k}.json"], token=None))  # noqa: E731
        assert sr("ok")[0]["_sha256"] and refused(lambda: sr("tau"), "tau = -inf"), "deletion step refused"
        assert refused(lambda: sr("d1"), "never scored") and refused(lambda: sr("other"), "not a C-CONF output")
        assert refused(lambda: sr("ok", "ov_dev_b"))
        lr = [{"run_id": "v", "model": "qwen25vl_7b", "spec": {"arm": "rand", "draw": 2}, "_sha256": "h",
               "predictions": {"b": "xx", "a": "x", "c": "xxx", "z": "o"}},
              {"run_id": "l", "model": "lmcap", "spec": {"arm": "lmcap", "variant": "ri"}, "_sha256": "h",
               "predictions": {"a": "y", "b": "yy", "c": "yyy"}}]
        score = lambda capt, refs: [float(len(capt[i]) + len(refs[i])) for i in sorted(capt)]  # noqa: E731
        rows = A.ledger_rows(lr, "ov_carve", "ov_carve", ["c", "a", "b"], {i: ["r"] for i in "abc"}, score)
        assert [r["per_image"]["ids"] for r in rows] == [["a", "b", "c"]] * 2 and rows[0]["per_image"]["cider_s"] == [2, 3, 4]
        assert (rows[0]["arm"], rows[0]["draw"], rows[1]["model"], rows[1]["arm"], rows[1]["draw"]) == \
            ("rand", 2, "lmcap", "lmcap_ri", None) and all(r["tau"] == "-inf" for r in rows)
        per, cids = A.CS.columns(rows, "ov_carve")
        assert set(per) == {"qwen25vl_7b|rand_d2", "lmcap|lmcap_ri"} and cids == ["a", "b", "c"], "the scorer reads it"
        assert refused(lambda: A.ledger_rows(lr, "ov_carve", "ov_carve", ["a", "z"], {"a": [], "z": []}, score),
                       "does not cover")
        ok.append("tau = -inf only; D1 and other sets never scored; ledger rows as c_conf_score.columns reads them")
        # ---- D1 comparator and the arm-list path rule of the job
        new = {"predictions": {"a": "x", "b": "y", "c": "z"}}
        assert A.differing(new, {"predictions": {"a": "x", "b": "y ", "c": "z"}}, ["a", "b", "c"]) == ["b"]
        assert A.differing({"predictions": {"a": "x"}}, new, ["a", "b"]) == ["b"], "a missing caption is a failure"
        o = Path("/h/outputs")
        assert A.arm_lists_path("ov_carve", o / "c_conf_r/out") == o / "c_conf_b0/lists_ov_carve.json"
        assert A.arm_lists_path("ov_carve", o / "c_conf_r_dry/out") == o / "c_conf_b0_dry/lists_ov_carve.json"
        assert A.arm_lists_path("ov_carve", o / "c_conf_b0/dry") == o / "c_conf_b0/lists_ov_carve.json"
        assert A.arm_lists_path("ov_test", o / "c_conf_t/out") == o / "c_conf_t/lists_ov_test.json"
        ok.append("D1 comparator (ids only); arm-list files beside the job's output folders")
    A.ADMITTED = None
    return ok


#: (file, name, old, new): each must make the self-test fail
MUTANTS = [
    ("c_conf_score.py", "token with a wrong decision sha256 accepted",
     'if sorted(t) != sorted(TOKEN_FIELDS) or t["rehearsal_decision_sha256"] != sha(rehearsal) \\',
     "if sorted(t) != sorted(TOKEN_FIELDS) \\"),
    ("c_conf_score.py", "a token with three fields accepted", "if sorted(t) != sorted(TOKEN_FIELDS) or t[",
     "if len(t) < 3 or t["),
    ("c_conf.py", "a backbone not in the token admitted",
     'if backbone is not None and backbone not in ADMITTED["backbones"]:', "if False:"),
    ("c_conf.py", "perm reading the ret list",
     'ids = ex["perm"][str(draw)][qid][:k] if arm == "perm" else ex["ret"][qid][:k]', 'ids = ex["ret"][qid][:k]'),
    ("c_conf.py", "batch size 2 accepted", "    if not a.batch1:\n", "    if False:\n"),
    ("c_conf.py", "deletion step applied to InternVL3-8B", 'TAU = {m: "-inf" for m in CS.BACKBONES}',
     'TAU = {m: "-inf" for m in CS.BACKBONES} | {"internvl3_8b": "0.10"}'),
    ("c_conf.py", "token check skipped (the one gate)", "    if ADMITTED is None:\n", "    if False:\n"),
    ("c_conf.py", "own cluster kept in lmcap_ri", " | ({own[qid]} if qid in own else set())", ""),
    ("c_conf.py", "OV-test names admitted without a token", '(set(cl["refuse"]["openviic_files"]) - ', "(set() - "),
    ("c_conf.py", "XM-test2500 and Flickr30K admitted with a token", "return out if admitted else out",
     "return set() if admitted else out"),
    ("c_conf.py", "run id without the draw", ' + (f"-{tagd}{a.draw}" if tagd else "")', ""),
    ("c_conf.py", "a D1 file scored", 'SKIP_RUNS = ("-smoke", "-rev50", "-fwd50")', 'SKIP_RUNS = ("-smoke",)'),
    ("c_conf.py", "ledger ids unsorted", "    ids = sorted(ids)\n    rows = []\n", "    rows = []\n"),
    ("c_conf.py", "kt_pinned without the sha256 comparison", "    return want is not None and sha(q) == want\n",
     "    return want is not None\n"),
    ("c_conf.py", "kt_pinned without the folder condition",
     '    if os.path.dirname(os.path.realpath(q)) != cfg["kt_images"] or os.path.realpath(q) != os.path.abspath(q):\n',
     "    if False:\n"),
]


def mutant_tree(d: Path, test: str, mutant: tuple | None = None) -> Path:
    """A copy of the C-CONF files and this test with ROOT pointing at the real checkout, one mutant applied."""
    for n in dict.fromkeys((*FILES, "test_c_conf.py", test)):
        src = (HERE / n).read_text(encoding="utf-8").replace(ROOT_LINE, f"ROOT = Path({str(REAL_ROOT)!r})")
        if mutant and mutant[0] == n:
            assert src.count(mutant[2]) == 1, f"mutant anchor not found once: {mutant[1]}"
            src = src.replace(mutant[2], mutant[3])
        (d / n).write_text(src, encoding="utf-8")
    return d / test


def run_mutants(test: str, mutants: list) -> None:
    alive = []
    for m in mutants:
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, "-I", "-B", str(mutant_tree(Path(tmp), test, m)), "--selftest"],
                               capture_output=True, text=True, timeout=900)
            if r.returncode == 0:
                alive.append(m[1])
    print(f"mutants: {len(mutants) - len(alive)} of {len(mutants)} killed")
    assert not alive, f"mutants alive: {alive}"


def main() -> None:
    import c_conf as A

    print("self-test PASS: " + "; ".join(selftest(A)))
    if "--selftest" not in sys.argv:
        run_mutants(Path(__file__).name, MUTANTS)


if __name__ == "__main__":
    main()
