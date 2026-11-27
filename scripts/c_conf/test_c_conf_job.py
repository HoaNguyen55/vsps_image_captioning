"""Dry-run self-test of the C-CONF host job (c_conf_job.sh) in a sandbox, on synthetic fixtures only (§11.1 row
c_conf_job.sh; CC-450 X5).

Runs on a rented host (the investigator's rule of 2026-11-11: no test runs on the laptop), with git, flock, timeout,
GNU date and sha256sum, in a venv holding numpy:
    env -u PYTHONPATH venv/bin/python -I -B scripts/c_conf/test_c_conf_job.py
Each case builds a throwaway root (a git repository holding the job, the real c_conf_score.py and logging stubs of
c_conf.py, c_conf_arms.py and c_conf_lists.py) and runs the job with C_CONF_DRY=1 and C_CONF_ROOT set to that root: decodes are
stubbed calls, the cap uses the §6.1 planning rates, the OV-test staging is an empty folder. No study file is read,
nothing is written outside the temporary folder, and /root is never touched.
Checks: the host push list (scripts/c_conf/SHA256SUMS) names no test-set file; every mode starts, checks its inputs and stops before a model load (step 0.4); the rehearsal order R.0, R.1,
R.4, R.2, R.3; a rehearsal cap above the ceiling is a STOP; the test-host order T.0, cap line with the time check, the
scoring parity gate, the dry run, the time check again, then T0; a dry run with the freeze set 20 hours ahead stops
before T0 (no staging, no OV-test decode); a forced binding cap drops Aya-Vision-8B first, then InternVL3-8B, and never
LMCap or Qwen2.5-VL-7B; no token, or an OV-test folder present before T.0, stops before any decode; block 0 runs the
venv-cenfeat import check first (I5); a JOB STOP after T0 writes LOOK_STOP.json and a stop before T0 does not (I3),
with one mutant of the job (the write removed) that this case must kill. CC-454: call 3 with nothing staged stops
before T0 with no LOOK_STOP (B1, with its mutant); K0 on OV-dev-B (k0dev) runs between the parity gate and the dry
run and its failure stops before T0_READY (B4); an LMCap decode on OV-test gets one attempt (B5).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = "manuscript/prereg/2026-11-18_c_conf"
STUB = '''import os, sys
args = sys.argv[1:]
with open(os.environ["C_CONF_CALLS"], "a", encoding="utf-8") as f:
    f.write("{who} " + " ".join(args) + "\\n")
for flag in ("--out",):
    if flag in args and args[0] in ("block0",):
        open(args[args.index(flag) + 1], "w").write("[]\\n")
fail = os.environ.get("C_CONF_STUB_FAIL")
if fail and fail in " ".join(args):
    sys.exit(int(os.environ.get("C_CONF_STUB_RC", "1")))
sys.exit(3 if args[0] == "compare" else 0)
'''
Q, I, AY, LM = "qwen25vl_7b", "internvl3_8b", "aya_vision_8b", "lmcap"
#: test-set names that may never be in the host push list (coordinator 2026-11-18): KTVIC test, Karpathy / COCO test,
#: NoCaps, UIT-ViIC test, XM3600 (all of it), OV-test (files, vectors, example file, ledgers, annotation)
TEST_SET = re.compile(r"ktvic_test|karpathy|coco_test|nocaps|uitviic_test|xm3600|xm_test|openviic_test|ov_test|"
                      r"annotation-test|primary1941", re.I)


def test_set_files(sums: str) -> list[str]:
    """The file names of a SHA256SUMS text that name a test set."""
    names = [ln.split(maxsplit=1)[1] for ln in sums.splitlines() if ln.strip()]
    return [n for n in names if TEST_SET.search(n)]


def utc(ts: float) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts))


def sandbox(tmp: Path, job_src: str | None = None) -> tuple[Path, str]:
    root = tmp / "root"
    repo = root / "vsps"
    cc = repo / "scripts/c_conf"
    cc.mkdir(parents=True)
    (cc / "c_conf_job.sh").write_text(job_src or (HERE / "c_conf_job.sh").read_text(encoding="utf-8"), encoding="utf-8")
    shutil.copy(HERE / "c_conf_score.py", cc)
    (cc / "c_conf.py").write_text(STUB.format(who="c_conf"), encoding="utf-8")
    (cc / "c_conf_arms.py").write_text(STUB.format(who="lists"), encoding="utf-8")  # block0, diag, t0
    (cc / "c_conf_lists.py").write_text(STUB.format(who="order"), encoding="utf-8")  # pinned, never called by the job
    files = ["c_conf_job.sh", "c_conf_score.py", "c_conf.py", "c_conf_arms.py", "c_conf_lists.py"]
    sums = subprocess.run(["sha256sum", *files], cwd=cc,
                          capture_output=True, text=True, check=True).stdout
    (cc / "SHA256SUMS").write_text(sums, encoding="utf-8")
    (repo / REG).mkdir(parents=True)
    (repo / REG / "x.txt").write_text("registration placeholder\n", encoding="utf-8")
    (repo / REG / "SHA256SUMS").write_text(subprocess.run(["sha256sum", "x.txt"], cwd=repo / REG, capture_output=True,
                                                          text=True, check=True).stdout, encoding="utf-8")
    for venv in (repo / ".venv", root / "venv-lb", root / "venv-t1", root / "venv-cenfeat"):
        (venv / "bin").mkdir(parents=True)
        (venv / "bin/python").write_text(f'#!/bin/sh\nexec {sys.executable} "$@"\n', encoding="utf-8")
        (venv / "bin/python").chmod(0o755)  # a wrapper, so the host venv (numpy) is the one that runs
    (root / ".vsps_machine_id").write_text("h1\n", encoding="utf-8")
    (repo / ".gitignore").write_text(".venv/\n", encoding="utf-8")
    git = ["git", "-C", str(repo), "-c", "user.email=dry@local", "-c", "user.name=dry"]
    subprocess.run(git + ["init", "-q"], check=True)
    subprocess.run(git + ["add", "-A"], check=True)
    subprocess.run(git + ["commit", "-qm", "dry"], check=True)
    head = subprocess.run(git + ["rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    return root, head


def run(mode: str, env_extra: dict | None = None, entered=(Q, I, AY), token: bool = True, pre=None,
        job_src: str | None = None) -> dict:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        root, head = sandbox(tmp, job_src)
        calls = tmp / "calls.log"
        calls.touch()
        args = ["bash", str(root / "vsps/scripts/c_conf/c_conf_job.sh"), mode, head]
        if mode == "test":
            dec = tmp / "decision.json"
            dec.write_text(json.dumps({"entered": list(entered), "look": True}), encoding="utf-8")
            tok = tmp / "token.json"
            tok.write_text(json.dumps({"backbones": list(entered)}), encoding="utf-8")
            args += [str(tok) if token else str(tmp / "missing.json"), str(dec)]
        if pre:
            pre(root)
        env = {k: v for k, v in os.environ.items() if not k.startswith("C_CONF_")}
        env |= {"C_CONF_DRY": "1", "C_CONF_ROOT": str(root), "C_CONF_CALLS": str(calls),
                "C_CONF_FREEZE_UTC": utc(time.time() + 10 * 86400), **(env_extra or {})}
        p = subprocess.run(args, env=env, capture_output=True, text=True, timeout=600)
        out = {"rc": p.returncode, "calls": calls.read_text(encoding="utf-8").splitlines(),
               "decision": str(tmp / "decision.json"),
               "staged": (root / "c_conf_ov_test").exists(), "stdout": p.stdout + p.stderr,
               "look_stop": [json.loads(x.read_text(encoding="utf-8")) for x in (root / "outputs").glob("*/LOOK_STOP.json")]}
        logs = sorted((root / "outputs").glob("*/logs/job.log"))
        out["log"] = logs[0].read_text(encoding="utf-8").splitlines() if logs else []
        cap = sorted((root / "outputs").glob("*/CAP.json"))
        out["cap"] = json.loads(cap[0].read_text(encoding="utf-8")) if cap else None
        return out


def first(lines: list[str], text: str, start: int = 0) -> int:
    for k in range(start, len(lines)):
        if text in lines[k]:
            return k
    raise AssertionError(f"not found after line {start}: {text!r}")


def decodes(r: dict, s: str) -> list[str]:
    return [c for c in r["calls"] if c.startswith("c_conf ") and c.split()[1] in ("decode", "lmcap") and f"--set {s} " in c + " "
            and "--redecode" not in c]


def model_of(call: str) -> str:
    return LM if call.split()[1] == "lmcap" else call.split("--model ")[1].split()[0]


def order_of(calls: list[str]) -> list[str]:
    seen = []
    for c in calls:
        if model_of(c) not in seen:
            seen.append(model_of(c))
    return seen


def main() -> None:
    ok = []
    h = "0" * 64
    for bad in ("ktvic_test.npz", "feats_coco_test.npz", "feats_nocaps_val.npz", "uitviic_test.npz",
                "of_xm3600_all.npz", "openviic_test.npz", "emb_ov_test.npz", "uit-openviic-annotation-test.json",
                "ledger_ov_test_1941.jsonl", "ov_test_primary1941.txt"):
        assert test_set_files(f"{h}  c_conf.py\n{h}  {bad}\n") == [bad], bad
    assert test_set_files(f"{h}  of_ktvic_dev299.npz\n{h}  test_c_conf_job.py\n") == []
    listed = test_set_files((HERE / "SHA256SUMS").read_text(encoding="utf-8"))
    assert not listed, f"the host push list names {len(listed)} test-set files"
    ok.append("the host push list (SHA256SUMS) names no test-set file")
    r = run("selftest")
    assert r["rc"] == 0 and any("SELFTEST MODE DONE" in x for x in r["log"]), r["stdout"]
    ok.append("selftest mode")

    r = run("block0")
    assert r["rc"] == 0 and any("BLOCK 0 DONE" in x for x in r["log"]), r["stdout"]
    steps = ["lists envcheck", "c_conf inputs --block0", "lists block0", "lists diag"]
    assert [first(r["calls"], s) for s in steps] == sorted(first(r["calls"], s) for s in steps)
    dry = [c for c in r["calls"] if c.split()[1] in ("decode", "lmcap")]
    assert len(dry) == 4 and all("--limit 2 --dry-run" in c and "--set ov_carve" in c and "--batch1" in c for c in dry)
    assert not r["staged"] and not any("ov_test" in c for c in r["calls"])
    ok.append("block 0: the venv-cenfeat import check, 0.1, 0.2, 0.3, every host mode dry (--limit 2 --dry-run, stops "
              "before a model load), 0.5")

    r = run("rehearsal")
    assert r["rc"] == 0, r["stdout"]
    carve = decodes(r, "ov_carve")
    assert len(carve) == 3 * 7 + 3 and order_of(carve) == [Q, LM, I, AY], order_of(carve)
    assert all("--batch1" in c and "--limit 2 --dry-run" in c for c in carve)
    last_d1 = max(k for k, c in enumerate(r["calls"]) if "--redecode" in c)
    assert last_d1 < r["calls"].index(carve[0]), "every D1 before the first registered step"
    assert first(r["log"], "CAP PLAN rehearsal") < first(r["log"], "START R_qwen25vl_7b_qwen25vl_7b_zs")
    ok.append("rehearsal: R.0 D1 for every runner, the cap, then R.1, R.4, R.2, R.3 (24 runs at batch size 1)")

    r = run("rehearsal", {"C_CONF_FORCE_CAP_H": "20"})
    assert r["rc"] == 1 and any("back to the judge" in x for x in r["log"]) and not decodes(r, "ov_carve")
    ok.append("rehearsal: 1.5 P above the ceiling is a STOP before the first step")

    r = run("test")
    assert r["rc"] == 0, r["stdout"]
    lg = r["log"]
    marks = ["PREFLIGHT OK", "STEP D1 qwen25vl_7b", "CAP PLAN test", "TIME CHECK", "STEP parity gate",
             "STEP dry run", "TIME CHECK", "T0 READY", "T0 BEGINS", "T0 ok", "START T_qwen25vl_7b_qwen25vl_7b_zs"]
    at = 0
    for m in marks:
        at = first(lg, m, at) + 1
    assert first(r["calls"], "c_conf token --token") < first(r["calls"], "--redecode"), "token before T.0"
    names = first(r["calls"], "--names-only")
    assert names < first(r["calls"], "c_conf stagecheck") < first(r["calls"], "lists t0")
    assert not any("ov_test" in c for c in r["calls"][:first(r["calls"], "c_conf stagecheck")]), \
        "no OV-test set named in any call before T0"
    tdec = decodes(r, "ov_test")
    assert order_of(tdec) == [Q, LM, I, AY] and len(tdec) == 24 and all("--token" in c for c in tdec)
    dec_arg = "--decision " + str(Path(r["decision"]))
    assert all(dec_arg in c for c in tdec + [x for x in r["calls"] if x.split()[1] in ("stagecheck", "t0")]), \
        "every OV-test decode, the stage check and T0 get the rehearsal decision with the token"
    assert not any(c.startswith("order ") for c in r["calls"]), "the pinned order builder is never called"
    assert r["staged"] and r["cap"]["dropped"] == []
    k0 = first(r["calls"], "lists k0dev")
    assert max(k for k, c in enumerate(r["calls"]) if "--redecode" in c) < k0 < first(r["calls"], "_dry/dry "), \
        "CC-454 B4: k0dev after T.0 and the parity gate, before the dry run"
    ok.append("test: token, T.0, cap + time check, parity gate, k0dev, dry run, time check, T0 READY, T0, T.1, T.4, T.2, "
              "T.3")

    r = run("test", {"C_CONF_FREEZE_UTC": utc(time.time() + 20 * 3600)})
    assert r["rc"] == 1 and any("TIME CHECK FAIL" in x for x in r["log"]), r["stdout"]
    assert not any("T0 READY" in x or "T0 BEGINS" in x for x in r["log"]) and not r["staged"]
    assert not any(c.split()[1] in ("stagecheck", "t0") for c in r["calls"]) and not decodes(r, "ov_test")
    assert not r["look_stop"], "a stop before T0 spends no look"
    ok.append("test: a dry run with the freeze set 20 hours ahead stops before T0 (no staging, no OV-test call)")

    r = run("test", {"C_CONF_FORCE_CAP_H": "12"})
    assert r["rc"] == 0 and r["cap"]["dropped"] == [AY, I], r["stdout"]
    assert order_of(decodes(r, "ov_test")) == [Q, LM]
    r = run("test", {"C_CONF_FORCE_CAP_H": "20"})
    assert r["rc"] == 0 and r["cap"]["dropped"] == [AY] and order_of(decodes(r, "ov_test")) == [Q, LM, I]
    r = run("test", {"C_CONF_FORCE_CAP_H": "5"})
    assert r["rc"] == 1 and any("no look spent" in x for x in r["log"]) and not r["staged"]
    ok.append("test: a forced binding cap drops Aya-Vision-8B first, then InternVL3-8B, never LMCap or Qwen2.5-VL-7B; "
              "if it still does not fit, STOP before T0")

    r = run("test", entered=(Q, AY))
    assert r["rc"] == 0 and order_of(decodes(r, "ov_test")) == [Q, LM, AY] and \
        not any("--model internvl3_8b" in c for c in r["calls"] if "--redecode" in c), "a backbone not entered never runs"
    ok.append("test: only the backbones the token names (and LMCap) are decoded, D1 included")

    r = run("test", token=False)
    assert r["rc"] == 1 and any("G3" in x for x in r["log"]) and not any("--redecode" in c for c in r["calls"])
    r = run("test", pre=lambda root: (root / "c_conf_ov_test").mkdir())
    assert r["rc"] == 1 and not any("--redecode" in c for c in r["calls"]), "an OV-test folder before T.0 stops"
    ok.append("test: no token, or an OV-test folder before T.0, stops before any decode")

    assert look_stop_case(), "a stop after T0 (a decode failing 3 attempts) writes LOOK_STOP.json"
    ok.append("test: a JOB STOP after T0 writes LOOK_STOP.json (I3); a stop before T0 does not")
    assert nothing_staged_case(), "CC-454 B1: call 3 with nothing staged stops before T0 and spends no look"
    ok.append("test: call 3 with nothing staged stops before T0, no LOOK_STOP, no stagecheck or t0 call (B1)")
    r = run("test", {"C_CONF_STUB_FAIL": "k0dev", "C_CONF_STUB_RC": "3"})
    assert r["rc"] == 1 and any("K0 on OV-dev-B under T0's interpreter" in x for x in r["log"]), r["stdout"]
    assert not any("T0 READY" in x for x in r["log"]) and not r["staged"] and not r["look_stop"]
    assert not any(c.split()[1] in ("stagecheck", "t0") for c in r["calls"])
    ok.append("test: k0dev rc 3 stops before T0_READY with no LOOK_STOP (B4)")
    r = run("test", {"C_CONF_STUB_FAIL": "lmcap --set ov_test"})
    assert r["rc"] == 1 and sum("START T_lmcap_lmcap_ri attempt" in x for x in r["log"]) == 1, r["stdout"]
    assert any("T_lmcap_lmcap_ri failed 1 attempt(s)" in x for x in r["log"]) and len(r["look_stop"]) == 1
    ok.append("test: an LMCap decode on OV-test that fails gets one attempt, then JOB STOP and LOOK_STOP (B5)")
    src = (HERE / "c_conf_job.sh").read_text(encoding="utf-8")
    alive = []
    for name, old, new, case in JOB_MUTANTS:
        assert src.count(old) == 1, f"mutant anchor not found once: {name}"
        if case(src.replace(old, new)):
            alive.append(name)
    print(f"mutants: {len(JOB_MUTANTS) - len(alive)} of {len(JOB_MUTANTS)} killed")
    assert not alive, f"mutants alive: {alive}"
    print("c_conf_job dry-run self-test PASS: " + "; ".join(ok))


def stage_ready(root: Path) -> None:
    """A test session after call 2: CAP.json and T0_READY.json written, nothing staged."""
    o = root / "outputs/c_conf_t_dry"
    o.mkdir(parents=True)
    (o / "CAP.json").write_text(json.dumps({"runners": [Q, LM], "cap_s": 3600, "dropped": []}), encoding="utf-8")
    (o / "T0_READY.json").write_text(json.dumps({"cap_sha256": "0" * 64, "utc": "x"}), encoding="utf-8")


def nothing_staged_case(job_src: str | None = None) -> bool:
    """CC-454 B1: call 3 with CAP.json and T0_READY.json present and no staging folder stops before T0."""
    r = run("test", pre=stage_ready, job_src=job_src)
    return (r["rc"] == 1 and any("nothing is staged" in x for x in r["log"]) and not r["look_stop"]
            and not any(c.split()[1] in ("stagecheck", "t0") for c in r["calls"]) and not r["staged"])


def look_stop_case(job_src: str | None = None) -> bool:
    """I3: an InternVL3-8B decode on OV-test fails all three attempts after T0; the JOB STOP must be the look."""
    r = run("test", {"C_CONF_STUB_FAIL": "--model internvl3_8b --set ov_test"}, job_src=job_src)
    return (r["rc"] == 1 and any("T0 ok" in x for x in r["log"]) and any("JOB STOP" in x for x in r["log"])
            and len(r["look_stop"]) == 1 and r["look_stop"][0]["look_stop"].startswith("JOB STOP after T0"))


JOB_MUTANTS = [("a stop after T0 writes no LOOK_STOP",
                "  if [ -s $LOG/T0.done ] && [ ! -e $O/LOOK_STOP.json ]; then\n", "  if false; then\n", look_stop_case),
               ("call 3 runs with nothing staged (CC-454 B1)", '  { dry && [ -d $STAGE_T ]; } || [ -n "$(ls -A $STAGE_T 2>/dev/null)" ] \\\n    || stop "nothing is staged in $STAGE_T: T0 has not begun; no look spent (run call 3 only after staging)"\n', "", nothing_staged_case)]


if __name__ == "__main__":
    main()
