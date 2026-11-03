#!/usr/bin/env python
"""Author mutants M1-M20 for e2b_1c.py (TIER1C O1 §9 mutant plan; M20 = CC-233r2 NB3). Each mutant is applied to a
copy of e2b.py / e2b_1c.py / test_e2b_1c.py in a scratch tree (put it on ext4, not /mnt/d) and must make
test_e2b_1c.py fail. The unmutated copy must pass first.

    <venv with numpy> -I scripts/vsps_j_e2b/e2b_1c_mutants.py <scratch dir>
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = ("e2b.py", "e2b_1c.py", "test_e2b_1c.py")
C = "e2b_1c.py"
MUTANTS = [  # (id, file, [(old, new), ...]); every old string must occur exactly once
    ("M1 cushion 2 -> 0", C, [("CUSHION_PTS = 2  #", "CUSHION_PTS = 0  #")]),
    ("M2 ceil -> floor", C, [("(CUSHION_PTS * n_f + 99) // 100", "(CUSHION_PTS * n_f) // 100")]),
    ("M3 >= k* -> >", C, [("if hits(g) >= k_s), None)", "if hits(g) > k_s), None)")]),
    ("M4 GRID -> 0.01 steps", C, [("for g in e2b.GRID if hits(g)",
                                   "for g in tuple(round(0.01 * i, 2) for i in range(1, 100)) if hits(g)")]),
    ("M5 Vintern by match_lo", C, [("thrV[t] = e2b.band(pv, y)",
                                    "thrV[t] = (lambda q: (q, e2b.hi_rule(pv, y, q)))(e2b.match_lo(pv, y, e2b.R_DESIGN))"
                                    " if n_f else (0.5, 0.5)")]),
    ("M6 fit on tune and select", C, [("tu = e2b.tune_of(op, t)", 'tu = [s for s in op if s["t2"] == t]')]),
    ("M7 held rows in ppass", C, [("rows = e2b.per_image_counts(sel, fE, fV)",
                                   "rows = e2b.per_image_counts(sel + held, fE, fV)")]),
    ("M8 n_t3 = len(rows)", C, [("dec = ppass(rows, n_t3=N_SCREEN,", "dec = ppass(rows, n_t3=len(rows),")]),
    ("M9 decision seed swapped", C, [("B_in=B_IN, seed=SEED_T2, deadline=deadline)",
                                      "B_in=B_IN, seed=SEED_PRED, deadline=deadline)")]),
    ("M10 H4 margin -3.0", C, [('and ci["drecall"][0] > e2b.RET_MARGIN)', 'and ci["drecall"][0] > -3.0)')]),
    ("M11 gate > 0.98", C, [('if dec["p_hat"] >= PASS_GATE', 'if dec["p_hat"] > PASS_GATE')]),
    ("M12 undefined counted as pass", C, [("            n_undef += 1\n", "            n_pass += 1\n")]),
    ("M13 once-guard removed", C, [("for name in (GUARD_NAME, RES_NAME):", "for name in ():")]),
    ("M14 non-winner cell opened", C, [('"internvl3_8b_FA_vi"  #', '"qwen3vl_8b_FA_vi"  #')]),
    ("M15 predictive used for the decision", C, [("B_in=B_IN, seed=SEED_T2, deadline=deadline)",
                                                  "B_in=B_IN, seed=SEED_T2, pre_n=len(rows), pre_seed=SEED_PRED, "
                                                  "deadline=deadline)")]),
    ("M16 guard written before res_1c.json", C, [
        ('    write_excl(a.runs / RES_NAME, json.dumps(res, indent=1, default=str) + "\\n")\n'
         "    rsha = m0.sha_file(a.runs / RES_NAME)\n", '    rsha = "0" * 64\n'),
        ("    a.copy_to.mkdir(parents=True, exist_ok=True)\n",
         '    write_excl(a.runs / RES_NAME, json.dumps(res, indent=1, default=str) + "\\n")\n'
         "    a.copy_to.mkdir(parents=True, exist_ok=True)\n")]),
    ("M17 infeasible primary falls back", C, [("if reason and t in e2b.PRIMARY:", "if reason and t in ():")]),
    ("M18 start check ignores an orphan res_1c.json", C, [("for name in (GUARD_NAME, RES_NAME):",
                                                           "for name in (GUARD_NAME,):")]),
    ("M19 EN folder loaded as well", C, [('status, mass = e2b.classify(a.runs / WIN_CELL, keys, "vi")',
                                          'status, mass = e2b.classify(a.runs / WIN_CELL, keys, "vi"); '
                                          'e2b.classify(a.runs / "internvl3_8b_FA_en", keys, "en")')]),
    ("M20 inner drop at exactly 1 % counted as fault", C, [("if bad.mean() > e2b.MAX_DROP:",
                                                            "if bad.mean() >= e2b.MAX_DROP:")]),
    ("M21 cap message carries a progress figure", C, [('raise CapStop("wall cap reached")',
                                                       'raise CapStop(f"wall cap reached at outer replicate {b}")')]),
]


def stage(root: Path) -> Path:
    d = root / "scripts" / "vsps_j_e2b"
    d.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        shutil.copyfile(HERE / f, d / f)
    m = root / "scripts" / "vsps_j_m0"
    if not m.exists():
        os.symlink(HERE.parent / "vsps_j_m0", m)  # read-only import of m0
    return d


def run(d: Path) -> tuple[int, str]:
    """(rc, the last stderr line): the line shows which assertion killed a mutant."""
    shutil.rmtree(d / "__pycache__", ignore_errors=True)  # -B too: a same-size mutant must never reuse a stale .pyc
    p = subprocess.run([sys.executable, "-I", "-B", str(d / "test_e2b_1c.py")], stdout=subprocess.DEVNULL,
                       stderr=subprocess.PIPE, text=True, timeout=600)
    tail = [ln.strip() for ln in p.stderr.splitlines() if ln.strip()]
    at = [ln.split(", ", 1)[1] for ln in tail if ln.startswith('File "') and "test_e2b_1c.py" in ln]
    return p.returncode, ((at[-1] + " :: " if at else "") + (tail[-1][:120] if tail else ""))


def main() -> int:
    root = Path(sys.argv[1]).resolve() / "e2b_1c_mutants"
    if str(root).startswith("/mnt/"):
        raise SystemExit("REFUSED: put the mutant scratch on ext4, not /mnt")
    d = stage(root)
    if run(d)[0] != 0:
        raise SystemExit("FAULT: the unmutated copy fails its selftest")
    killed = 0
    for mid, f, edits in MUTANTS:
        src = (HERE / f).read_text(encoding="utf-8")
        for old, new in edits:
            if src.count(old) != 1:
                raise SystemExit(f"FAULT {mid}: pattern found {src.count(old)} times")
            src = src.replace(old, new)
        (d / f).write_text(src, encoding="utf-8")
        rc, why = run(d)
        shutil.copyfile(HERE / f, d / f)
        killed += rc != 0
        print(f"{'KILLED  ' if rc else 'SURVIVED'} {mid} | {why}")
    print(f"mutants: {killed}/{len(MUTANTS)} killed")
    return 0 if killed == len(MUTANTS) else 1


if __name__ == "__main__":
    sys.exit(main())
