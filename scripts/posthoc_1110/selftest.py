#!/usr/bin/env python3
"""Selftest of posthoc_rows.py on synthetic fixtures only (generators fix_c1, fix_c2, fix_b1, fix_b2; seed 20261110).

  ~/.venvs/c_stage1_lists/bin/python -I -B scripts/posthoc_1110/selftest.py

No real ledger, decide file or B2 record is opened or hashed; the real ROWS are never run and POST is never created.
Fixture ledgers are the registered fake_* ledgers with integer scores written over them, and the registered decide
functions write the fixture decide files. The planted ids carry +1000 (C1, C2, B2) or +600 at L5 (B1), so without
exactly the pinned ids every row is an exact literal: 6.0 [6.0, 6.0] and 0.0 (C1), 6.0 (C2), slope 3.0 (B1), mean
101.0 with SD 1.0 (B2). C1 uses the real pinned order and the real 12-id pin. Each row run is a fresh process.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import posthoc_rows as P  # noqa: E402

SEED = 20261110
R2 = "per-image scores as stored; document frequencies not recomputed"
ROOTS = ["/mnt/d/vsps_image_captioning", "/mnt/d/vsps_papers", os.path.expanduser("~/vsps_w25k1"),
         os.path.expanduser("~/c_pvr_w25_in"), os.path.expanduser("~/.vsps_sealed")]
POST = "/mnt/d/vsps_image_captioning/.session_backup/2026-11-10/posthoc"
PLAN_N = {"c1": [1941, 1929], "c2": [5000, 4999], "b1": [300, 293], "b2": [558, 542]}
PLAN_B2 = {"s42": 148.6640, "s43": 148.0630, "s44": 147.9615}
CHILD = ("import json, sys; sys.path.insert(0, sys.argv[1]); import posthoc_rows as P; P.ROWS.clear(); "
         "P.SCOPE.append(sys.argv[2]); exec(sys.argv[5]); P.run(sys.argv[3], json.loads(sys.argv[4]))")
SNEAK = "o = P.FN['b2']\ndef f(s, d):\n{}\n    return o(s, d)\nP.FN['b2'] = f"
OPEN = "open(sys.argv[2] + '/undeclared.json')"
OFFSET = {"ret": 6, "fix": 1, "zs": -5}


def child(tmp: Path, row: str, spec: dict, pre: str = "") -> tuple[int, str]:
    r = subprocess.run([sys.executable, "-I", "-B", "-c", CHILD, str(HERE), str(tmp), row, json.dumps(spec), pre],
                       capture_output=True, text=True)
    return r.returncode, (r.stderr.strip().splitlines() or [""])[-1]


def put(path: Path, text: str) -> list[str]:
    path.write_text(text, encoding="utf-8")
    return [str(path), hashlib.sha256(text.encode()).hexdigest()]


def planted(arm: str, frozen: bool, base: np.ndarray, hot: np.ndarray) -> list[int]:
    """Integer scores: ret = base + 6 (+1000 at the pinned ids, +50 off the frozen tau), fix + 1, zs - 5."""
    return (base + OFFSET.get(arm, 0) + (arm == "ret") * (1000 * hot + 50 * (not frozen))).tolist()


def near(a, b) -> bool:
    if isinstance(a, dict):
        return isinstance(b, dict) and a.keys() == b.keys() and all(near(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return isinstance(b, list) and len(a) == len(b) and all(map(near, a, b))
    return a == b or (isinstance(a, float) and isinstance(b, float) and abs(a - b) <= 1e-9)


# ------------------------------------------------------------------------------------------------ fixtures
def fix_c1(tmp: Path, rng) -> tuple[dict, dict, dict, dict]:
    sys.path.insert(0, f"{P.RUN}/scripts/c_test")
    import score_t as ST

    cfg = ST.S2.frozen()
    order = ST.T.scored_ids("ov_test_1941", ST.C.load_lists(ST.LISTS))
    drop = Path(P.ROWS["c1"]["ids"][0]).read_text(encoding="utf-8").split()
    ids = [str(i) for i in rng.permutation(order)]  # stored order differs from the pinned order
    hot, base = np.isin(ids, drop), 20 + np.arange(len(ids)) % 9
    rows = [{**r, "per_image": {**r["per_image"], "ids": ids,
                                "tp_cm": (2 - 2 * hot * (r["arm"] == "ret")).tolist(),
                                "cider_s": planted(r["arm"], not r["model"] or r["tau"] == cfg["models"][r["model"]][
                                    "tau"], base, hot)}} for r in ST.fake_test(cfg, n=len(ids))]
    led = ST.reorder(ST.aliased(ST.S.latest(rows), "ov_test"), order)
    dec = ST.norm(ST.decide_ov({"ov_test_1941": led, "ov_test_2001": led}, cfg, "ov_test", "ov_test_1941"))
    bad = copy.deepcopy(dec)
    bad["P2"][ST.IVL]["hi"] += 1e-6
    real = P.ROWS["c1"]
    spec = {**real, "out": str(tmp / "c1_out.json"), "inputs": {
        **real["inputs"], "ledger": put(tmp / "c1_ledger.jsonl", "".join(json.dumps(r) + "\n" for r in rows)),
        "decide": put(tmp / "c1_decide.json", json.dumps(dec))}}
    six, zero = dict.fromkeys(P.DLH, 6.0), dict.fromkeys(P.DLH, 0.0)
    return (spec, {"P1": six, "P2": dict.fromkeys(ST.C.MODELS, zero)}, {"P1": dec["P1"], "P2": dec["P2"]},
            {**spec, "out": str(tmp / "c1_bad.json"),
             "inputs": {**spec["inputs"], "decide": put(tmp / "c1_decide_bad.json", json.dumps(bad))}})


def fix_c2(tmp: Path, rng) -> tuple[dict, dict, dict, dict]:
    sys.path.insert(0, f"{P.RUN}/scripts/c_en")
    import cen_score as CS

    cfg = CS.S2.frozen()
    rows = CS.fake_rows("coco_test", ["coco_test_5000"], dict.fromkeys(CS.D.C.MODELS, 0.0))["coco_test_5000"]
    ids = rows[0]["per_image"]["ids"]
    drop = sorted(rng.choice(ids, 3, replace=False).tolist())
    hot, base = np.isin(ids, drop), 50 + np.arange(len(ids)) % 7
    rows = [{**r, "per_image": {**r["per_image"], "cider_ptb": planted(
        r["arm"], r["tau"] == cfg["models"][r["model"]]["tau"], base, hot)}} for r in rows]
    dec = CS.decide({"coco_test_5000": rows}, "coco_test", None)
    bad = copy.deepcopy(dec)
    bad["P1_EN"]["lo"] += 1e-6
    spec = {"ids": put(tmp / "c2_pin.txt", "\n".join(drop) + "\n"), "n": [len(ids), len(ids) - 3],
            "out": str(tmp / "c2_out.json"),
            "inputs": {"ledger": put(tmp / "c2_ledger.jsonl", "".join(json.dumps(r) + "\n" for r in rows)),
                       "decide": put(tmp / "c2_decide.json", json.dumps(dec)), "frozen": P.FROZEN,
                       "code": P.ROWS["c2"]["inputs"]["code"]}}
    return (spec, dict.fromkeys(P.DLH, 6.0), {"P1_EN": dec["P1_EN"]},
            {**spec, "out": str(tmp / "c2_bad.json"),
             "inputs": {**spec["inputs"], "decide": put(tmp / "c2_decide_bad.json", json.dumps(bad))}})


def fix_b1(tmp: Path, rng) -> tuple[dict, dict, dict, dict, dict]:
    sys.path.insert(0, f"{P.RUN}/scripts/b1_scaling")
    import b1 as B

    led = B.fake_ledger(3.0, 0.0)
    ids = led["rows"][B.run_name(42, "L1")]["ids"]
    drop = [B.DEV_TWIN, *sorted(rng.choice([i for i in ids if i != B.DEV_TWIN], 6, replace=False).tolist())]
    for s in B.SEEDS:
        for i in drop:
            led["rows"][B.run_name(s, "L5")]["cider_s"][ids.index(i)] += 600.0
    dec = B.decide(led)
    bad = copy.deepcopy(dec)
    bad["sensitivity_minus_dev_twin"]["pooled"]["ci95"][1] += 1e-6
    two = copy.deepcopy(led)
    two["rows"][B.run_name(43, "L2")]["ids"] = ids[::-1]
    spec = {"ids": put(tmp / "b1_pin.txt", "\n".join(drop) + "\n"), "n": [300, 293], "out": str(tmp / "b1_out.json"),
            "inputs": {"ledger": put(tmp / "b1_ledger.json", json.dumps(led)),
                       "decide": put(tmp / "b1_decide.json", json.dumps(dec)),
                       "code": P.ROWS["b1"]["inputs"]["code"], "probe": P.ROWS["b1"]["inputs"]["probe"]}}
    reg = {"P-B1": dec["P-B1"], "sensitivity_minus_dev_twin.pooled": dec["sensitivity_minus_dev_twin"]["pooled"]}
    return (spec, {"b": 3.0, "ci95": [3.0, 3.0]}, reg,
            {**spec, "out": str(tmp / "b1_bad.json"),
             "inputs": {**spec["inputs"], "decide": put(tmp / "b1_decide_bad.json", json.dumps(bad))}},
            {**spec, "out": str(tmp / "b1_two.json"),
             "inputs": {**spec["inputs"], "ledger": put(tmp / "b1_ledger_two.json", json.dumps(two))}})


def fix_b2(tmp: Path, rng) -> tuple[dict, dict, dict]:
    ids = sorted(str(1000 + 7 * k) for k in range(40))
    drop = sorted(rng.choice(ids, 5, replace=False).tolist())
    hot, seeds = np.isin(ids, drop), {"s42": 100.0, "s43": 101.0, "s44": 102.0}
    rec = {"test_ids": ids, "F0": {s: {"result_sha256": f"sha-of-{s}"} for s in seeds},
           "per_image_cider_x100": {**{s: (v + 1000 * hot).tolist() for s, v in seeds.items()}, "mbr": [999.0] * 40}}
    spec = {"ids": put(tmp / "b2_pin.txt", "\n".join(drop) + "\n"), "n": [40, 35], "out": str(tmp / "b2_out.json"),
            "identity": {s: [v + 125.0, f"sha-of-{s}"] for s, v in seeds.items()},
            "inputs": {"ledger": put(tmp / "b2_record.json", json.dumps(rec)),
                       "headline": put(tmp / "b2_headline.json", "{}")}}
    return (spec, {"per_seed": seeds, "mean": 101.0, "sd": 1.0},
            {"per_seed": {s: v + 125.0 for s, v in seeds.items()}, "mean": 226.0, "sd": 1.0})


# ------------------------------------------------------------------------------------------------ checks
def units() -> None:
    """R1 as a pure function (no file is opened; nothing under the sealed folder is touched)."""
    allow = {f"{P.RUN}/a.json"}
    assert P.SCOPE == ROOTS and P.DENY.pattern == "annotation-test|preds|caption", "R1 roots and name patterns"
    assert P.refusal(f"{P.RUN}/a.json", allow) is None and P.refusal("/tmp/x.json", allow) is None
    for root in ROOTS:
        assert P.refusal(f"{root}/b.json", allow), f"an undeclared file under {root} must stop the row"
    for p in (f"{ROOTS[4]}/a.json", "/tmp/uit-openviic-annotation-test.json", "/tmp/r.preds.json",
              "/tmp/captions.json"):
        assert P.refusal(p, allow | {p}), f"{p} must stop the row even when allow-listed"
    assert P.refusal(f"{sys.prefix}/lib/captions.py", allow) is None, "interpreter and venv paths are exempt"
    assert sys.pycache_prefix == os.devnull, "no .pyc may stand in for a sha-checked source"


def wiring() -> None:
    """The fixed paths and shas against the pinned manifests; the real row inputs are stat'ed, never opened."""
    inputs = Path(P.IDS, "INPUTS.sha256").read_text(encoding="utf-8").splitlines()
    pins = Path(P.IDS, "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    assert {r: s["n"] for r, s in P.ROWS.items()} == PLAN_N, "four rows; R3: C2 is COCO only (no XM, no NoCaps row)"
    assert P.ROWS["c2"]["inputs"]["ledger"][0].endswith("/c_en/ledger_coco_test_5000.jsonl"), "R3"
    for row, s in P.ROWS.items():
        for p, h in s["inputs"].values():
            assert f"{h}  {p}" in inputs and os.path.exists(p), f"{row}: {p} is not an INPUTS.sha256 line"
        p, h = s["ids"]
        assert f"{h}  {Path(p).name}" in pins and str(Path(p).parent) == P.IDS, f"{row}: pin not in ids/SHA256SUMS"
        assert len(Path(p).read_text(encoding="utf-8").split()) == s["n"][0] - s["n"][1], f"{row}: pin size"
        assert str(Path(s["out"]).parent) == POST, f"{row}: R4 output folder"
    for s, (mean, h) in P.ROWS["b2"]["identity"].items():
        assert mean == PLAN_B2[s] and f"{h}  {P.RUN}/data/results/p1assist_{s}-short.json" in inputs, s


def cli() -> None:
    """--ids and --out must be the planned files; run() is replaced, so no real row can start here."""
    called, s = [], P.ROWS["b2"]
    P.run = lambda *a: called.append(a)
    for ids, out in ((s["ids"][0], "/tmp/x.json"), ("/tmp/pin.txt", s["out"])):
        sys.argv = ["posthoc_rows.py", "b2", "--ids", ids, "--out", out]
        try:
            P.main()
        except SystemExit as e:
            assert "planned" in str(e) and not called
        else:
            raise AssertionError("the command line accepted another --ids or --out")
    sys.argv = ["posthoc_rows.py", "b2", "--ids", s["ids"][0], "--out", s["out"]]
    P.main()
    assert called == [("b2", s)]


def golden(tmp: Path, row: str, spec: dict, estimate: dict, registered: dict, identity: list[str]) -> dict:
    code, msg = child(tmp, row, spec)
    assert code == 0, f"{row}: the fixture run failed: {msg}"
    out = json.loads(Path(spec["out"]).read_text(encoding="utf-8"))
    declared = {os.path.realpath(p) for p, _h in (*spec["inputs"].values(), spec["ids"])} | {
        spec["out"], P.SELF} | {f"{P.RUN}/{c}" for c in P.CHAIN[row]}
    declared = {p for p in declared if P.under(p, [*ROOTS, str(tmp)])}
    assert set(out["opened"]) == declared, f"{row}: R1 audit list differs: {sorted(set(out['opened']) ^ declared)}"
    assert (out["row"], out["label"], out["verdict"], out["scores"]) == (row, "POST HOC", None, R2), f"{row}: R2, R4"
    assert "does not alter the registered result" in out["statement"]
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", out["utc"])
    assert out["inputs"] == {k: {"path": p, "sha256": h} for k, (p, h) in spec["inputs"].items()}
    assert out["pinned_ids"] == {"path": spec["ids"][0], "sha256": spec["ids"][1], "n": spec["n"][0] - spec["n"][1]}
    assert out["script"] == {"path": P.SELF, "sha256": P.sha(P.SELF)}
    assert [out["n_before"], out["n_after"]] == spec["n"], f"{row}: n"
    assert near(out["estimate"], estimate), f"{row}: estimate {out['estimate']} is not {estimate}"
    assert out["registered"] == registered, f"{row}: the registered block is not copied unchanged"
    assert [i["what"] for i in out["identity"]] == identity, f"{row}: identity checks {out['identity']}"
    return out


def refused(tmp: Path, row: str, spec: dict, why: str, pre: str = "") -> None:
    code, msg = child(tmp, row, spec, pre)
    assert code != 0 and why in msg and not Path(spec["out"]).exists(), f"{row}: wanted a stop on '{why}': {msg}"


def frame(tmp: Path, spec: dict) -> None:
    """The shared stops, on the B2 fixture (no registered import, so each child is fast)."""
    n = iter(range(99))

    def neg(**kw) -> dict:
        return {**spec, "out": str(tmp / f"b2_neg{next(n)}.json"), **kw}

    (tmp / "undeclared.json").write_text("{}")
    rec = json.loads(Path(spec["inputs"]["ledger"][0]).read_text())
    rec["F0"]["s43"]["result_sha256"] = "another-file"
    drop = Path(spec["ids"][0]).read_text()
    refused(tmp, "b2", neg(inputs={**spec["inputs"], "ledger": [spec["inputs"]["ledger"][0], "0" * 64]}),
            "sha256 differs")
    refused(tmp, "b2", neg(ids=[spec["ids"][0], "0" * 64]), "sha256 differs")
    refused(tmp, "b2", neg(ids=put(tmp / "b2_pin_foreign.txt", drop + "nope\n")), "pinned id")
    refused(tmp, "b2", neg(ids=put(tmp / "b2_pin_twice.txt", drop + drop.split()[0] + "\n")), "pinned id")
    refused(tmp, "b2", neg(n=[40, 34]), "is not the planned")
    refused(tmp, "b2", neg(), "R1 STOP: open of", SNEAK.format(f"    {OPEN}"))
    refused(tmp, "b2", neg(), "R1 STOP: refused opens",  # holds when the caller swallows the stop (decide2.safe)
            SNEAK.format(f"    try:\n        {OPEN}\n    except SystemExit:\n        pass"))
    refused(tmp, "b2", neg(), "one row per process", "sys.modules['b1'] = sys")
    refused(tmp, "b2", neg(inputs={**spec["inputs"], "ledger": put(tmp / "b2_record_other.json", json.dumps(rec))}),
            "result_sha256")
    refused(tmp, "b2", neg(identity={**spec["identity"], "s44": [227.0001, "sha-of-s44"]}), "identity check failed")
    before = Path(spec["out"]).read_bytes()
    code, msg = child(tmp, "b2", spec)
    assert code != 0 and "a row runs once" in msg and Path(spec["out"]).read_bytes() == before, f"R4 run once: {msg}"


def main() -> None:
    units()
    wiring()
    cli()
    tmp, rng = Path(tempfile.mkdtemp(prefix="posthoc_selftest_")).resolve(), np.random.default_rng(SEED)
    try:
        spec, est, every = fix_b2(tmp, rng)
        out = golden(tmp, "b2", spec, est, {"verdict": None},
                     [f"{s}: mean over all images at four decimals" for s in est["per_seed"]])
        assert out["scores_computed_on"] == "all 40 images", "CC-315 Ruling 7"
        assert near(out["three_seed_mean_sd_all_images"], every), "b2: the mean and SD over all images"
        frame(tmp, spec)
        spec, est, reg, bad, two = fix_b1(tmp, rng)
        golden(tmp, "b1", spec, est, reg, ["empty set = decide.json::P-B1",
                                          "image 2004 alone = decide.json::sensitivity_minus_dev_twin.pooled"])
        refused(tmp, "b1", bad, "identity check failed")
        refused(tmp, "b1", two, "one common id list")
        spec, est, reg, bad = fix_c2(tmp, rng)
        golden(tmp, "c2", spec, est, reg, ["one_set pooled = decide_coco_test.json::P1_EN",
                                          "subset form, nothing excluded = decide_coco_test.json::P1_EN"])
        refused(tmp, "c2", bad, "identity check failed")
        spec, est, reg, bad = fix_c1(tmp, rng)
        golden(tmp, "c1", spec, est, reg, ["all 1,941 = decide_ov.json::P1", *(
            f"all 1,941 = decide_ov.json::P2.{m}" for m in est["P2"])])
        refused(tmp, "c1", bad, "identity check failed")
    finally:
        shutil.rmtree(tmp)
    print("selftest ok: R1 (audit list = declared files, undeclared and denied opens stop, one row per process), "
          "R2 and R4 fields, R3 (COCO only), sha and pin stops, exclusion = exactly the pinned ids with exact "
          "answers on c1, c2, b1, b2, identity stops, registered block copied unchanged, run once, fixed command line")


if __name__ == "__main__":
    main()
