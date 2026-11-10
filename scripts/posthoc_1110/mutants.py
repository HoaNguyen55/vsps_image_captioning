#!/usr/bin/env python3
"""Rule mutants for posthoc_rows.py, in the style of scripts/b_pa1/b_pa1_score_mutants.py. Each mutant breaks one
rule (R1-R4 of CC-315, a plan rule or a row's estimator) in a scratch copy and must make selftest.py fail. The
scratch copies sit outside the repo and run one at a time (one I/O-heavy command on /mnt/d). Synthetic fixtures only.
Run:  ~/.venvs/c_stage1_lists/bin/python -I -B scripts/posthoc_1110/mutants.py
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
F = "posthoc_rows.py"
KEPT = "    if len(set(drop)) != len(drop) or not set(drop) <= set(order):"
CLI = '    if str(a.ids.resolve()) != spec["ids"][0] or str(a.out.resolve()) != spec["out"]:'
MASK = "        keep, M = ~np.isin(np.arange(n), j), ~np.isin(idx, j)"
RNG = "np.random.default_rng(B.SP.BOOT_SEED).integers(0, n, (B.SP.B, n))"
MUT = [  # (id, old, new): each old must occur exactly once
    ("R1a every open is logged", "            log.append(p)", "            pass"),
    ("R1b the hook is installed", "    sys.addaudithook(hook)", "    pass"),
    ("R1c allow-list stop", "    if under(p, SCOPE) and p not in allow:", "    if False:"),
    ("R1d stop before the file is touched", '            raise SystemExit(f"R1 STOP: open of {p} refused: {why}")',
     "            pass"),
    ("R1e a swallowed stop still stops", "    if bad:", "    if False:"),
    ("R1f data root /mnt/d/vsps_papers", 'SCOPE = [RUN, "/mnt/d/vsps_papers", ', "SCOPE = [RUN, "),
    ("R1g sealed folder", "    if under(p, [SEALED]) or DENY.search(", "    if DENY.search("),
    ("R1h annotation-test name", 'r"annotation-test|preds|caption"', 'r"preds|caption"'),
    ("R1i preds name", 'r"annotation-test|preds|caption"', 'r"annotation-test|caption"'),
    ("R1j caption name", 'r"annotation-test|preds|caption"', 'r"annotation-test|preds"'),
    ("R1k name match on the file name", "DENY.search(os.path.basename(p))", "DENY.search(p)"),
    ("R1l interpreter and venv exempt", "    if under(p, EXEMPT):", "    if False:"),
    ("R1m exact allow-list", '    "b2": [],\n}', '    "b2": ["scripts/evaluate.py"],\n}'),
    ("R1n one row per process", "    if LOADED & set(sys.modules):", "    if False:"),
    ("R1o no .pyc stands in for the source", "sys.pycache_prefix = os.devnull", "sys.pycache_prefix = None"),
    ("R2 stored-scores statement", 'NOTE = "per-image scores as stored; document frequencies not recomputed"',
     'NOTE = "per-image scores as stored"'),
    ("R3 C2 is the COCO ledger", 'f"{M1E}/ledger_coco_test_5000.jsonl"', 'f"{M1E}/ledger_nocaps_val_4500.jsonl"'),
    ("R4a label POST HOC", '"label": "POST HOC", "verdict": None,', '"label": "REGISTERED", "verdict": None,'),
    ("R4b no verdict", '"label": "POST HOC", "verdict": None,', '"label": "POST HOC", "verdict": "PASS",'),
    ("R4c output folder", 'POST = f"{RUN}/.session_backup/2026-11-10/posthoc"', 'POST = f"{RUN}/data/results/posthoc"'),
    ("R4d run once", "    if out.exists():", "    if False:"),
    ("P5a input and pin sha first (rule 5)", "        if sha(p) != h:", "        if False:"),
    ("P5b --ids fixed", CLI, '    if str(a.out.resolve()) != spec["out"]:'),
    ("P5c --out fixed", CLI, '    if str(a.ids.resolve()) != spec["ids"][0]:'),
    ("P6a identity stops the row (rule 6)", "    if not gap <= tol:", "    if False:"),
    ("P6b identity within 1e-9 (rule 6)", "TOL = 1e-9", "TOL = 1e-3"),
    ("X1 pinned id inside the set", KEPT, "    if len(set(drop)) != len(drop):"),
    ("X2 pinned id once", KEPT, "    if not set(drop) <= set(order):"),
    ("X3 n before and after as planned", '    if [res["n_before"], res["n_after"]] != spec["n"]:', "    if False:"),
    ("C1a row on the kept queries", '"estimate": p1_p2(ST.reorder(raw, keep, subset=True)),',
     '"estimate": p1_p2(ST.reorder(raw, order, subset=True)),'),
    ("C1b identity on all 1,941 in the pinned order", "    full = p1_p2(ST.reorder(raw, order))",
     "    full = p1_p2(ST.reorder(raw, keep, subset=True))"),
    ("C1c P1 = pooled ret - rand", '{"P1": g["pooled_vs_rand"],', '{"P1": g["pooled_vs_fix"],'),
    ("C1d P2 = pcm_ci", '["pcm_vs_zs"] for m in models}}', '["vs_zs"] for m in models}}'),
    ("C1e registered block copied", '"registered": {"P1": dec["P1"], "P2": dec["P2"]}}',
     '"registered": {"P1": full["P1"], "P2": dec["P2"]}}'),
    ("C2a exclusion", "    sel = ~np.isin(ids, drop)", "    sel = np.ones(len(ids), bool)"),
    ("C2b ret - rand", 'CS.D.spec(cfg, "coco_test", m, "rand")', 'CS.D.spec(cfg, "coco_test", m, "zs")'),
    ("C2c frozen tau", 'm, "ret")["run_id"], cfg["models"][m]["tau"])', 'm, "ret")["run_id"], "-inf")'),
    ("C2d row on the kept queries", '"estimate": CS.ci(d[sel], CS.draws(int(sel.sum()))),',
     '"estimate": CS.ci(d, CS.draws(len(d))),'),
    ("B1a draws of the masked images dropped", MASK,
     "        keep, M = ~np.isin(np.arange(n), j), np.ones(idx.shape, bool)"),
    ("B1b point means over the kept images", MASK, "        keep, M = np.ones(n, bool), ~np.isin(idx, j)"),
    ("B1c bootstrap seed 0", RNG, "np.random.default_rng(B.SP.BOOT_SEED + 1).integers(0, n, (B.SP.B, n))"),
    ("B1d B = 2000", RNG, "np.random.default_rng(B.SP.BOOT_SEED).integers(0, n, (B.SP.B // 2, n))"),
    ("B1e the row masks the pinned list", "    b, lo, hi = slope(drop)", "    b, lo, hi = slope([B.DEV_TWIN])"),
    ("B1f one common id list", "    if len(common) != 1 or len(next(iter(common))) != n:", "    if False:"),
    ("B2a the three seeds, never mbr", 'for s in spec["identity"]}  # the seeds',
     'for s in rec["per_image_cider_x100"]}  # the seeds'),
    ("B2b sample SD", "ddof=1", "ddof=0"),
    ("B2c exclusion", "    keep = ~np.isin(ids, drop)", "    keep = np.ones(len(ids), bool)"),
    ("B2d headline result sha", '        if len(per[s]) != len(ids) or rec["F0"][s]["result_sha256"] != result:',
     "        if len(per[s]) != len(ids):"),
    ("B2e means at four decimals", "[mean4], 5e-5))", "[mean4], 5e-3))"),
    ("B2f scores computed on all images (Ruling 7)", '"scores_computed_on": f"all {len(ids)} images",',
     '"scores_computed_on": "",'),
    ("B2g the all-images recomputation", '"three_seed_mean_sd_all_images": every}',
     '"three_seed_mean_sd_all_images": mean_sd(keep)}'),
    ("B2h no registered verdict", '"registered": {"verdict": None},', '"registered": {"verdict": "PASS"},'),
]


def run(d: Path) -> tuple[bool, str]:
    r = subprocess.run([sys.executable, "-I", "-B", str(d / "selftest.py")], capture_output=True, text=True,
                       timeout=600)
    tail = [x for x in (r.stderr or r.stdout).splitlines() if x.strip()]
    return r.returncode == 0, (tail[-1][:110] if tail else str(r.returncode))


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="posthoc_mut_"))
    try:
        d = root / "m"
        d.mkdir()
        src = (HERE / F).read_text(encoding="utf-8")
        shutil.copy(HERE / "selftest.py", d)
        (d / F).write_text(src, encoding="utf-8")
        ok, why = run(d)
        assert ok, f"control fails: {why}"
        print("control: selftest passes on the unmutated file", flush=True)
        survived = []
        for mid, old, new in MUT:
            if src.count(old) != 1:
                ok, why = True, f"PATTERN NOT FOUND ONCE ({src.count(old)})"
            else:
                (d / F).write_text(src.replace(old, new), encoding="utf-8")
                ok, why = run(d)
            print(f"{mid}: {'SURVIVED' if ok else 'KILLED'} {why}", flush=True)
            survived += [mid] if ok else []
        print(f"{len(MUT) - len(survived)}/{len(MUT)} killed; survived: {survived or 'none'}")
        return 1 if survived else 0
    finally:
        shutil.rmtree(root)


if __name__ == "__main__":
    sys.exit(main())
