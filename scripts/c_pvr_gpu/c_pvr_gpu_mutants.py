#!/usr/bin/env python3
"""Mutant harness for scripts/c_pvr_gpu/c_pvr_gpu.py (pattern of scripts/c_pvr/c_pvr_mutants.py).
Usage: <venv python> -I -B c_pvr_gpu_mutants.py <repo root> <empty scratch dir outside /mnt>.
The scratch dir gets scripts/c_pvr/{c_pvr.py,c_pvr_run.py,prompts/} and one mutated scripts/c_pvr_gpu/c_pvr_gpu.py per mutant.
Each mutant replaces one exact string (it must occur once) and runs `selftest` on the copy. The unmutated copy runs
first and must print 'selftest ok'. KILLED = the selftest fails.
Then c_pvr_job.sh (CC-270 N9): the unmutated script must pass every dry-run case of job_dry() under <scratch>/job, and
each J mutant must fail at least one case (KILLED). The two tallies are printed separately."""
import shutil
import subprocess
import sys
from pathlib import Path

M = {
    # money (T1-REP §9, host v3 §3)
    "cut_order_swapped": ('CUT_ORDER = ("A10", "A5",', 'CUT_ORDER = ("A5", "A10",'),
    "t_down_omitted": ("return (m - s - T_DOWN_H * r) // r", "return (m - s) // r"),
    "fit_strict_lt": ("return ceil125(sum(left.values()) + fixed_sec) <= h_m(m, s, r)",
                      "return ceil125(sum(left.values()) + fixed_sec) < h_m(m, s, r)"),
    "a8_wait_not_projected": ("return ceil125(sum(left.values()) + fixed_sec) <= h_m(m, s, r)",
                              "return ceil125(sum(left.values())) <= h_m(m, s, r)"),
    "r_host_rounded_down": ("r = math.ceil(Fraction(line))", "r = math.floor(Fraction(line))"),
    "speed_incomplete_silent": ('    if miss := sorted({a for _, _, arms in SETS.values() for a in arms} - set(rate)):',
                                '    if miss := []:'),
    "ceil_is_floor": ("return -(-5 * sec // 14400)", "return 5 * sec // 14400"),
    "pqc2_restores_cuts": ("        m = M_PQC2\n", "        m = M_PQC2\n        left, cuts = dict(arm_sec), []\n"),
    "pqc2_no_solvency": ("        if not pqc2_solvent:\n", "        if False:\n"),
    "timer_not_wall_clock": ('return int(cap["p1_epoch"] + cap["cap_h"] * 3600 - now)',
                             'return int(cap["cap_h"] * 3600)'),
    # loader, generation, echo (PINS-A §12 Q-LLAVA, Ruling 2)
    "weights_only_false_passes": ('        if k.get("weights_only", True) is not True:\n', "        if False:\n"),
    "genconfig_none_only": ("if k not in d or d[k] != v)", "if v is None and d.get(k) is not None)"),
    "echo_check_off": ("        if body in CP.clean(text) or CP.clean(text).startswith(body[:24]):\n",
                       "        if False:\n"),
    # ids only, datastores (meta item 17, OPS-1106c-datastores, CC-261 N6)
    "log_accepts_text": ("            if isinstance(x, str) and not ID_RX.fullmatch(x):\n", "            if False:\n"),
    "log_any_key": ("        if k not in keys:\n", "        if False:\n"),
    "kept_rehash_skipped": ("    if hashlib.sha256(b).hexdigest() != sha:\n        fault(f\"{fname}",
                            "    if False:\n        fault(f\"{fname}"),
    "str_norm_removed": ("ids = [str(x) for x in (a.tolist() if hasattr(a, \"tolist\") else a)]",
                         "ids = list(a.tolist() if hasattr(a, \"tolist\") else a)"),
    "t2pool_allowed": ('BARRED = re.compile(r"\\.vsps_sealed|t2pool_", re.I)', 'BARRED = re.compile(r"\\.vsps_sealed", re.I)'),
    # decode and block rules (NB-SPEED, T1-REP R-1, host v3 §4.4)
    "speed_writes_captions": ('out = None if x.speed else open(outp, "a")', 'out = open(outp, "a")'),
    "never_cut_skipped": ("    for a in sorted(NEVER_CUT):\n        need(a)\n", ""),
    "a7_before_pvr_drop": ('PHASES = (("A1", "S3", "PVR-drop", "PVR-keep", "A12", "A0", "A6", "A7",',
                           'PHASES = (("A1", "S3", "A7", "PVR-drop", "PVR-keep", "A12", "A0", "A6",'),
    # CC-270 B1: the v1 set-major order, cuttable phase first, A10 not last, A8/S2 after the cuttable arms
    "set_major_order": ("for a in sum(PHASES, ()) for s, (_, lang, arms) in SETS.items()",
                        "for s, (_, lang, arms) in SETS.items() for a in sum(PHASES, ())"),
    "cuttable_first": ("for a in sum(PHASES, ()) for s", "for a in sum(PHASES[::-1], ()) for s"),
    "cut_tail_not_a10": ("          tuple(reversed(CUT_ORDER)))", "          CUT_ORDER)"),
    "a8_after_cuttable": ("for a in sum(PHASES, ()) for s", "for a in sum((PHASES[0], PHASES[2], PHASES[1]), ()) for s"),
    # CC-270 B2: the A8 wait bound, the decomposition arrival check, the wipe count of the mid-run push
    "a8_wait_unbounded": ("        if clock() - t0 > A8_WAIT_SEC:\n", "        if False:\n"),
    "a1_decomp_sha_unchecked": ("    if want.get(f.name) != hashlib.sha256(b).hexdigest():\n", "    if False:\n"),
    "a1_decomp_ids_unchecked": ("    if set(dec) != ids:\n", "    if False:\n"),
    "wipe_skips_a1_decomp": ('(d / "MANIFEST.sha256", d / "a1_decomp" / "MANIFEST.sha256")', '(d / "MANIFEST.sha256",)'),
    # CC-270 N9: DEMOCAP pins (W5) must refuse d_tc / d_en
    "democap_need_removed": ('    if ds != "d_vi":\n        need(f"DEMOCAP_{ds}")\n', ""),
    "speed_log_full": ("        keep = SPEED_LOG if x.speed else LOG_KEYS", "        keep = LOG_KEYS"),
    "hostcheck_sha_unchecked": ("    if {k: rep.get(k) for k in now} != now:\n", "    if False:\n"),
    "wipe_ignores_count": ("    return 0 if files == expect else 5", "    return 0"),
    # N8 demonstration caption (CC-269r2 Ruling 4, W2-W3) and S9 helper pins (S9 §8.1)
    "democap_last_caption": ('        first.setdefault(str(a["image_id"]), a["caption"])',
                             '        first[str(a["image_id"])] = a["caption"]'),
    "democap_int_key": ('        first.setdefault(str(a["image_id"]), a["caption"])',
                        '        first.setdefault(a["image_id"], a["caption"])'),
    "democap_src_unhashed": ("        if hashlib.sha256(b).hexdigest() != CR.LISTS_IN[k][1]:\n", "        if False:\n"),
    "democap_manifest_unchecked": ('    if bad := [i for i, d in M["demos"].items() if d["text"] != want[i]]:',
                                   '    if bad := []:'),
    "helper_blob_as_sha256": ('        if (s256 if kind == "lfs" else s1) != want:', '        if s256 != want:'),
}


# CC-270 N9: c_pvr_job.sh dry run with stubbed PY (decode/selftest/pip faked; steps/left/wipe real), git, nvidia-smi.
# The copy's HC points into the scratch dir (the real /dev/shm path is never created); FREEZE_SHA = the fake freeze.
J = {
    "trap_before_lock": ("exec 9> $O/.job.lock\n",
                         'teardown() { $PY -I -B $X wipe --dir $HC --log $O/c_pvr_hc_deletions.log; say "EXIT $MODE"; }\n'
                         "trap teardown EXIT\nexec 9> $O/.job.lock\n"),
    "cap_mark_ignored": ('[ -e $MARK ] && stop "CAP_STOP.json exists: a cap stop is final"', "true"),
    "rc4_not_cap_stop": ("if [ $rc = 124 ] || [ $rc = 4 ]; then", "if [ $rc = 124 ]; then"),
    "speed_end_per_run": ("END=$(( $(cat $O/speed_start.epoch) + 5400 ))", "END=$(( $(date +%s) + 5400 ))"),
    "a8_no_decomp_arg": ("    case $ARM in A8|S2) ARGS+=(--a1-decomp $HC/a1_decomp/$SET.json);; esac\n", ""),
}
FAKE_PY = r"""#!/bin/bash
echo "$*" >> "$DRY_CALLS"
[ "$1 $2 $3" = "-m pip freeze" ] && { echo "torch==2.6.0+cu124"; exit 0; }
case "$4" in
  selftest|hostcheck) exit 0;;
  preflight) exit ${DRY_PREFLIGHT_RC:-0};;
  decode) a=("$@"); for i in "${!a[@]}"; do case "${a[$i]}" in --set) S=${a[$((i+1))]};; --arm) A=${a[$((i+1))]};; esac; done
          [ "$S $A" = "${DRY_RC4:-}" ] && exit 4; [ "$S $A" = "${DRY_RC1:-}" ] && exit 1; exit 0;;
  *) exec "$DRY_REALPY" "$@";;
esac
"""


def job_dry(root: Path, base: Path, text: str) -> list[str]:
    """Run the job-script cases on `text`; return the names of the cases that fail (empty = all hold)."""
    import hashlib
    import json
    import os
    import time
    fails = []
    if base.exists():
        shutil.rmtree(base)  # only ever a dir this harness created inside its own scratch
    repo, home, fb = base / "repo", base / "home", base / "bin"
    shutil.copytree(root / "scripts/c_pvr/prompts", repo / "scripts/c_pvr/prompts")
    for f in ("c_pvr.py", "c_pvr_run.py"):
        shutil.copy2(root / "scripts/c_pvr" / f, repo / "scripts/c_pvr" / f)
    g = repo / "scripts/c_pvr_gpu"
    g.mkdir()
    for f in ("c_pvr_gpu.py", "requirements_c_pvr_gpu.lock"):
        shutil.copy2(root / "scripts/c_pvr_gpu" / f, g / f)
    hc = base / "hc"
    freeze = hashlib.sha256(b"torch==2.6.0+cu124\n").hexdigest()
    for a, b in (("HC=/dev/shm/c_pvr_hc;", f"HC={hc};"), ("FREEZE_SHA=PENDING ", f"FREEZE_SHA={freeze} ")):
        if text.count(a) != 1:
            raise SystemExit(f"job.sh pattern {a!r} occurs {text.count(a)} times")
        text = text.replace(a, b)
    (g / "c_pvr_job.sh").write_text(text)
    sums = lambda d, names: "".join(  # noqa: E731
        f"{hashlib.sha256((repo / d / n).read_bytes()).hexdigest()}  {d}/{n}\n" for n in names)
    (g / "SHA256SUMS").write_text(sums("scripts/c_pvr_gpu", ("c_pvr_gpu.py", "c_pvr_job.sh",
                                                            "requirements_c_pvr_gpu.lock")))
    (repo / "scripts/c_pvr/SHA256SUMS").write_text(sums("scripts/c_pvr", ("c_pvr.py", "c_pvr_run.py")))
    lk = hashlib.sha256((g / "requirements_c_pvr_gpu.lock").read_bytes()).hexdigest()[:8]
    py = home / f"venvs/c_pvr_gpu_{lk}/bin/python"
    fb.mkdir(parents=True)
    py.parent.mkdir(parents=True)
    for p, body in ((py, FAKE_PY), (fb / "git", '#!/bin/bash\n[ "$1" = rev-parse ] && echo "$DRY_HEAD"; exit 0\n'),
                    (fb / "nvidia-smi", "#!/bin/bash\necho 'NVIDIA GeForce RTX 3090'\n")):
        p.write_text(body)
        p.chmod(0o755)
    o = home / "c_pvr_out"
    head = "a" * 40

    def case(mode, cap=None, env=(), pre=None, run_head=head):
        if o.exists():
            shutil.rmtree(o)
        (o / "logs").mkdir(parents=True)
        (o / "mblip_snapshot.path").write_text("/nonexistent\n")
        (o / "HOSTCHECK_OK.json").write_text("{}\n")
        if cap:
            (o / "CAP.json").write_text(json.dumps({"decision": "RUN", "cap_h": 1, "p1_epoch": int(time.time())} | cap))
        if hc.exists():
            shutil.rmtree(hc)
        hc.mkdir(mode=0o700)
        (hc / "a.bin").write_bytes(b"x")
        (hc / "MANIFEST.sha256").write_text(f"{hashlib.sha256(b'x').hexdigest()}  a.bin\n")
        tman = hashlib.sha256((hc / "MANIFEST.sha256").read_bytes()).hexdigest()
        if pre:
            pre()
        calls = base / "calls.txt"
        calls.write_text("")
        e = {"PATH": f"{fb}:/usr/bin:/bin", "HOME": str(home), "DRY_CALLS": str(calls), "DRY_HEAD": head,
             "DRY_REALPY": sys.executable, **dict(env)}
        cmd = ["bash", str(g / "c_pvr_job.sh"), mode, run_head, tman]
        if "lock" in dict(env):
            cmd = ["flock", str(o / ".job.lock")] + cmd
        r = subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=600)
        log = (o / "logs/job.log").read_text() if (o / "logs/job.log").exists() else ""
        dec = [ln.split() for ln in calls.read_text().splitlines() if " decode " in f" {ln} "]
        return r, log, dec, hc.exists()

    def check(name, ok):
        if not ok:
            fails.append(name)

    r, log, dec, alive = case("tier1", {"arms": ["A1"]}, env={"lock": "1"})
    check("lock_held_refused_hc_kept", r.returncode == 1 and "REFUSED" in r.stdout and alive and "EXIT" not in log)
    r, log, dec, alive = case("tier1", {"arms": ["A1"]}, pre=lambda: (o / "CAP_STOP.json").write_text("{}"))
    check("cap_mark_final", r.returncode == 1 and "CAP_STOP.json exists" in log and not dec and not alive
          and "EXIT tier1 rc=1" in log)
    r, log, dec, alive = case("tier1", {"arms": ["A1"]}, run_head="b" * 40)
    check("head_mismatch", r.returncode == 1 and "HEAD is not" in log and not dec and not alive)
    r, log, dec, alive = case("tier1", {"arms": ["A1"]}, env={"DRY_PREFLIGHT_RC": "1"})
    check("preflight_refusal", r.returncode == 1 and "pins PENDING" in log and not dec and not alive)
    r, log, dec, alive = case("tier1", {"arms": ["A1"], "p1_epoch": 0})
    check("cap_before_step", r.returncode == 0 and "CAP STOP cap reached before" in log and not dec
          and (o / "CAP_STOP.json").exists())
    r, log, dec, alive = case("tier1", {"arms": ["A1", "A8", "A11"]}, env={"DRY_RC4": "xm3600_vi A11"})
    arms = [d[d.index("--arm") + 1] for d in dec]
    a8 = [d for d in dec if d[d.index("--arm") + 1] == "A8"]
    dl = (o / "c_pvr_hc_deletions.log").read_text().split("\t") if (o / "c_pvr_hc_deletions.log").exists() else []
    check("rc4_cap_stop_then_wipe", r.returncode == 0 and (o / "CAP_STOP.json").exists() and not alive
          and log.index("CAP STOP during xm3600_vi A11") < log.index("EXIT tier1 rc=0") and dl[2:] == ["2", "2\n"]
          and "WIPE COUNT MISMATCH" not in log)
    check("phased_order_in_job", arms == ["A1"] * 5 + ["A8"] * 5 + ["A11"] and len(a8) == 5 and all(
        d[d.index("--a1-decomp") + 1] == f"{hc}/a1_decomp/{d[d.index('--set') + 1]}.json" for d in a8
        if "--a1-decomp" in d) and all("--a1-decomp" in d for d in a8))
    r, log, dec, alive = case("speed", env={"DRY_RC1": "xm3600_vi A1"})
    stamp = o / "speed_start.epoch"
    check("speed_stamp_written", r.returncode == 1 and stamp.exists() and len(dec) == 1)
    r, log, dec, alive = case("speed", pre=lambda: (o / "speed_start.epoch").write_text(f"{int(time.time()) - 6000}\n"))
    check("speed_total_1h30", r.returncode == 1 and "speed test over 1.5 h before" in log and not dec)
    return fails


def main() -> int:
    root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    if str(scratch).startswith("/mnt/") or any(scratch.iterdir()):
        raise SystemExit("scratch must be an empty dir outside /mnt")
    shutil.copytree(root / "scripts/c_pvr/prompts", scratch / "scripts/c_pvr/prompts")
    for f in ("c_pvr.py", "c_pvr_run.py"):
        shutil.copy2(root / "scripts/c_pvr" / f, scratch / "scripts/c_pvr" / f)
    (scratch / "scripts/c_pvr_gpu").mkdir()
    src = (root / "scripts/c_pvr_gpu/c_pvr_gpu.py").read_text("utf-8")
    dst = scratch / "scripts/c_pvr_gpu/c_pvr_gpu.py"

    def run(text: str) -> bool:
        dst.write_text(text, "utf-8")
        r = subprocess.run([sys.executable, "-I", "-B", str(dst), "selftest"], capture_output=True, text=True,
                           env={"PATH": "/usr/bin:/bin", "HF_HUB_OFFLINE": "1"})
        return r.returncode == 0 and "selftest ok" in r.stdout

    if not run(src):
        raise SystemExit("the unmutated copy fails its selftest")
    survived = []
    for name, (a, b) in M.items():
        if src.count(a) != 1:
            raise SystemExit(f"{name}: pattern occurs {src.count(a)} times")
        killed = not run(src.replace(a, b))
        print(f"{'KILLED' if killed else 'SURVIVED'}  {name}")
        if not killed:
            survived.append(name)
    print(f"{len(M) - len(survived)}/{len(M)} killed")
    job = (root / "scripts/c_pvr_gpu/c_pvr_job.sh").read_text("utf-8")
    if bad := job_dry(root, scratch / "job", job):
        raise SystemExit(f"the unmutated c_pvr_job.sh fails its dry run: {bad}")
    print("job dry run ok (unmutated)")
    js = []
    for name, (a, b) in J.items():
        if job.count(a) != 1:
            raise SystemExit(f"{name}: pattern occurs {job.count(a)} times")
        failed = job_dry(root, scratch / "job", job.replace(a, b))
        print(f"{'KILLED' if failed else 'SURVIVED'}  job:{name}  {failed}")
        if not failed:
            js.append(name)
    print(f"job.sh {len(J) - len(js)}/{len(J)} killed")
    return 1 if survived or js else 0


if __name__ == "__main__":
    sys.exit(main())
