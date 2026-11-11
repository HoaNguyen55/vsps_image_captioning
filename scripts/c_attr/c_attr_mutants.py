#!/usr/bin/env python3
"""Mutants of the C-ATTR-DEV code (registration §11.1 plus the two of CC-331 NEXT STEPS 2). Each mutant changes one rule
in a scratch copy of scripts/c_attr/ (the rest of the repo mirrored by symlinks, scripts/c_diag/c_diag_mutants.py form);
the three self-tests must then fail. One KILLED / SURVIVED line per mutant; rc 0 only when all are killed. Offline,
CPU, laptop:
    ~/.venvs/c_stage1_lists/bin/python -I -B scripts/c_attr/c_attr_mutants.py [--jobs 2]
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(os.path.abspath(__file__)).parent
REPO = HERE.parents[1]
L, A, S = "c_attr_lists.py", "c_attr.py", "c_attr_score.py"
TESTS = (A, L, S)
MUT = [  # (id, file, old, new): each old occurs exactly once
    ("L1 identity permutation allowed", L, "j = rng.randrange(i)\n        a[i], a[j]", "j = i\n        a[i], a[j]"),
    ("L2 near cut on the donor only", L, "keep = [c for c in donor_rank[:N_EX] if row_q[c] < NEAR]\n"
     "    refill = [c for c in donor_rank[N_EX:] if row_q[c] < NEAR]",
     "keep = list(donor_rank[:N_EX])\n    refill = list(donor_rank[N_EX:])"),
    ("L3 fix seed without f<j>", L, 'BM.seed("fix", ds) if j == 0 else BM.seed("fix", ds, f"f{j}")', 'BM.seed("fix", ds)'),
    ("L4 refill from q's own list", L, "lst, r = perm_list(ranks[pi[n]], cos[n])",
     "lst, r = perm_list(ranks[pi[n]][:N_EX] + ranks[n][N_EX:], cos[n])"),
    ("L5 randrange(i + 1)", L, "j = rng.randrange(i)\n        a[i], a[j]", "j = rng.randrange(i + 1)\n        a[i], a[j]"),
    ("A1 perm reads the ret list", A, 'ids = ex["perm"][str(draw)][qid][:k] if arm == "perm" else ex["ret"][qid][:k]',
     'ids = ex["ret"][qid][:k]'),
    ("A2 rand_img uses ret clusters", A, 'if arm in ("ret", "ret_img", "perm"):', 'if arm in ("ret", "ret_img", "perm", "rand_img"):'),
    ("A3 lmcap_rand keeps one retrieved caption", A,
     'return [c for c in ex["rand"]["0"][qid] if c not in shots][:LMCAP_K]',
     'return [c for c in ex["rand"]["0"][qid] if c not in shots][:LMCAP_K - 1] + retrieved[:1]'),
    ("A4 guard without the Flickr30K test names", A, 'return set(load_lists()["refuse"]["test"]) | (set(',
     "return set() | (set("),
    ("A5 deletion step applied to InternVL3 (tau rows other than -inf)", A,
     'if r.get("dataset") != ds or r.get("tau", "-inf") != "-inf" or', 'if r.get("dataset") != ds or'),
    ("S1 draw 0 in place of the draw mean", S, "return (np.mean([per[k] for k in keys], axis=0), len(keys)) if keys",
     "return (per[keys[0]], len(keys)) if keys"),
    ("S2 unpaired bootstrap", S, "a[rows].mean(1) - b[rows].mean(1)", "a[rows].mean(1) - b[rows[::-1]].mean(1)"),
    ("S3 a fresh index matrix per contrast", S, "rows = idx  # one index",
     "rows = np.random.default_rng(int(abs(a.sum())) % 997).integers(0, len(a), idx.shape)  # one index"),
    ("S4 kappa without the placebo term", S, "return loss_arm - loss_zs", "return loss_arm"),
    ("S5 Holm skipped", S, "p <= alpha / (m - j + 1)):", "p <= alpha):"),
    ("S6 >= and > swapped in DETECTED", S, "if not (d >= SESOI and p <= alpha / (m - j + 1)):",
     "if not (d > SESOI and p < alpha / (m - j + 1)):"),
    ("S7 >= and > swapped in NEGLIGIBLE", S, 'if s["lo90"] > -SESOI and s["hi90"] < SESOI:',
     'if s["lo90"] >= -SESOI and s["hi90"] <= SESOI:'),
    ("S8 > and >= swapped in REVERSED", S, 'if s["hi"] < 0:', 'if s["hi"] <= 0:'),
    ("S9 V_b divided by V_a, not V_img", S, "omega, omega_u = v_b / v_img, v_bu / v_img",
     "omega, omega_u = v_b / v_a, v_bu / v_a"),
    ("S10 masking applied to the references", S,
     'mk = score({i: A.masked(caps[i], shown[i], n) or "." for i in ids}, refs)',
     'mk = score({i: A.masked(caps[i], shown[i], n) or "." for i in ids}, '
     '{i: [A.masked(r, shown[i], n) for r in refs[i]] for i in refs})'),
    ("S11 Holm at 0.05 in place of 0.025 (CC-331)", S, "SESOI, ALPHA = A.SESOI, 0.025", "SESOI, ALPHA = A.SESOI, 0.05"),
    ("S12 'split of a known τ_sel' missing on OV-dev-B (CC-331)", S, 'KNOWN_SUM = ("ov_dev_a", "ov_dev_b")',
     'KNOWN_SUM = ("ov_dev_a",)'),
]
PY = sys.executable


def tree(root: Path) -> Path:
    """root mirrors the repo by symlinks; scripts/c_attr is a real copy (its modules find each other by path)."""
    (root / "scripts").mkdir(parents=True)
    for e in REPO.iterdir():
        if e.name not in ("scripts", ".git"):
            (root / e.name).symlink_to(e)
    for e in (REPO / "scripts").iterdir():
        if e.name != "c_attr":
            (root / "scripts" / e.name).symlink_to(e)
    d = root / "scripts" / "c_attr"
    d.mkdir()
    for f in HERE.iterdir():
        if f.is_file():
            shutil.copy2(f, d / f.name) if f.suffix == ".py" else (d / f.name).symlink_to(f)
    return d


def run(d: Path) -> tuple[bool, str]:
    for t in TESTS:
        r = subprocess.run(["unshare", "-rn", PY, "-X", "utf8", "-I", "-B", str(d / t), "--selftest"],
                           capture_output=True, text=True, timeout=900)
        if r.returncode:
            tail = [x for x in (r.stderr or r.stdout).splitlines() if x.strip()]
            return False, f"{t}: {(tail[-1] if tail else str(r.returncode))[:100]}"
    return True, ""


def one(m) -> tuple[str, bool, str]:
    mid, f, old, new = m
    src = (HERE / f).read_text(encoding="utf-8")
    if src.count(old) != 1:
        return mid, True, f"PATTERN NOT FOUND ONCE ({src.count(old)})"
    root = Path(tempfile.mkdtemp(prefix="c_attr_mut_"))
    try:
        d = tree(root)
        (d / f).write_text(src.replace(old, new), encoding="utf-8")
        return (mid, *run(d))
    finally:
        shutil.rmtree(root)  # the scratch holds copies and symlinks only; rmtree never follows symlinks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=2)
    a = ap.parse_args()
    root = Path(tempfile.mkdtemp(prefix="c_attr_mut_"))
    try:
        ok, why = run(tree(root))
        assert ok, f"control fails: {why}"
    finally:
        shutil.rmtree(root)
    print("control: the three self-tests pass on the unmutated files", flush=True)
    with ThreadPoolExecutor(a.jobs) as ex:
        results = list(ex.map(one, MUT))
    survived = [mid for mid, ok, _w in results if ok]
    for mid, ok, why in results:
        print(f"{mid}: {'SURVIVED' if ok else 'KILLED'} {why}", flush=True)
    print(f"{len(MUT) - len(survived)}/{len(MUT)} killed; survived: {survived or 'none'}")
    return 1 if survived else 0


if __name__ == "__main__":
    sys.exit(main())
