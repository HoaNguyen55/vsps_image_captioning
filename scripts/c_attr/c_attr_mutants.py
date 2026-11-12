#!/usr/bin/env python3
"""Mutants of the C-ATTR-DEV code (registration §11.1, the two of CC-331 NEXT STEPS 2, addendum v1.2 and the scoring
package of CC-346 W3). Each mutant changes one rule in a scratch copy of scripts/c_attr/ (the rest of the repo mirrored by
symlinks, scripts/c_diag/c_diag_mutants.py form); the three self-tests must then fail. One KILLED / SURVIVED line per
mutant; rc 0 only when all are killed. Offline, CPU, on the rented host (PI-1111j):
    ~/.venvs/c_stage1_lists/bin/python -I -B scripts/c_attr/c_attr_mutants.py [--jobs 2]
--no-netns (CC-339 W3): run the self-tests without `unshare -rn`, for a host whose container refuses user
namespaces; the self-tests are offline by construction, so this changes no kill.
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
    # addendum v1.2, block 1b (CC-340 W1, CC-341)
    ("A6 '-b1' missing from the run id", A, '+ ("-b1" if a.batch1 else "")', '+ ""'),
    ("A7 D1 compared with the step-1.0 (a) host50 decode", A, 'return run_id[: -len("-b1-fwd50")] + "-rev50"',
     'return run_id[: -len("-b1-fwd50")] + "-host50"'),
    ("A8 D1 comparator prints a caption", A, "failing ids {bad}\")",
     "failing ids {bad} {[new['predictions'].get(i) for i in bad]}\")"),
    ("S13 V4 (1): only perm runs gated on OV-dev-B (CC-338 S4)", S,
     'ovb = [r for r in runs if str(r.get("run_id", "")).startswith("at_") or r.get("spec", {}).get("arm") == "perm"]',
     'ovb = [r for r in runs if r.get("spec", {}).get("arm") == "perm"]'),
    ("S14 V4 (3) removed: batched runs scored before the verdict", S, "if len(b1) < len(at) and not released(a):",
     "if False:"),
    ("S15 v11 file accepted by name", S, "if Path(path).name == V11_NAME or rec", "if rec"),
    ("S16 v11 file accepted by content", S, 'rec.get("registration") != REG12 or "K1" in str(rec.get("reason", ""))',
     "False"),
    ("S17 batched row missing its label", S, "r[\"batch\"] = BATCHED", "r[\"batch\"] = None"),
    ("S18 batched run accepted into a 1b contrast", S, 'b1 = [r for r in led if is_b1(r.get("run_id", ""))]',
     "b1 = list(led)"),
    ("S19 host-parity fallback label missing (CC-338 S2)", S, "r[\"host\"] = HOST_FB", "pass"),
    ("S20 batch-1 rows carry the batched label", S, "r[\"batch\"] = B1_NOTE", "r[\"batch\"] = BATCHED"),
    # scoring package (CC-346 W3: SC1-SC5, CC-338 S1, S3, S5, and the scorer defects found with them)
    ("A9 SC1: c_attr.py score without the V4 gate", A, "    CS.v4_gate(a)\n", ""),
    ("A10 OV-dev-A references through stage 2 (manifest2 refuses OV-dev-A)", A,
     'if ds in ("ktvic_dev299", "ov_dev_a") else', 'if ds == "ktvic_dev299" else'),
    ("A11 two zs runs of one backbone in one score call", A, "if len(zs_m) != len(set(zs_m)):", "if False:"),
    ("S21 SC2: batch-1 rows summarised without a D1 PASS", S, "        if no_d1:\n", "        if False:\n"),
    ("S22 SC2: batched rows summarised without a STEP10 record", S,
     'if r["model"] in OLD3 and "A1" not in par.get(r["model"], {}):', "if False:"),
    ("S23 SC2: a '-b1' run not at batch size 1 accepted", S,
     'if any(r.get("spec", {}).get("batch_size") != 1 for r in b1):', "if False:"),
    ("S24 SC3: parity() last file wins", S, 'cur[k] = "FAIL" if "FAIL" in (cur.get(k), r[k]) else r[k]', "cur[k] = r[k]"),
    ("S25 SC4: nomination before every D1-PASS nominator has its four columns", S, "    if miss:  # SC4",
     "    if False:  # SC4"),
    ("S26 SC5: prompt hashes not compared", S, "same = sum(old.get(i) == h for i, h in mine.items())", "same = len(mine)"),
    ("S27 masked3 columns enter the draw means", S, r'if re.fullmatch(rf"{re.escape(m)}\|{arm}\d+", k))',
     'if k.startswith(f"{m}|{arm}"))'),
    ("S28 S3: df not recomputed in the resample", S, "df_refs=[rseg[ids[j]] for j in rows])", "df_refs=None)"),
    ("S29 S3: an image drawn twice counted once in the df", S, "df_refs=[rseg[ids[j]] for j in rows])",
     "df_refs=[rseg[i] for i in u])"),
    ("S30 S3: fixed-df interval off the shared index matrix", S, "v[sub].mean(1)",
     "v[np.random.default_rng(1).integers(0, len(v), sub.shape)].mean(1)"),
    ("S31 S3: sensitivity row not tied to the ledger's scores", S,
     'np.abs(sc[k] - np.array(want[0]["per_image"]["cider_s"])).max() > A.C2_PARITY_TOL', "False"),
    ("S32 S5: unit (ii) masks syllables", S, "A.masked(sg[caps[i]], [sg[x] for x in shown[i]], n)",
     "A.masked(caps[i], shown[i], n)"),
    ("S33 S5: blind run admitted without the stage-2 ledger pin", S, 'if not any(x.get("arm") == "blind" and',
     'if False and not any(x.get("arm") == "blind" and'),
    ("S34 S5: blind loss against the rand list, not R_q", S, 'comp["blind_loss"] = pair(copy_loss(blind, r_q,',
     'comp["blind_loss"] = pair(copy_loss(blind, own_rand,'),
    ("S35 S5: K_ret - K_nc companion without K_nc", S, '"K_ret_minus_K_nc": pair(kq - knc, zero, idx)',
     '"K_ret_minus_K_nc": pair(kq, zero, idx)'),
    ("S36 §7.9: swap δ reversed", S, '"delta": pair(same, other, idx)', '"delta": pair(other, same, idx)'),
    ("S37 §7.9: rule L at >= 0.10", S, "abs(v - b) / b > LENGTH_GAP", "abs(v - b) / b >= LENGTH_GAP"),
    ("S38 S1: every file exempt like logs/job.log", S,
     'bad = [n for n, h in listed.items() if n != "logs/job.log" and A.sha(d / n) != h]', "bad = []"),
    ("S39 S1: unlisted files in the copy accepted", S, "    if have != set(listed):\n", "    if False:\n"),
    ("S40 S1: SHA256SUMS not checked against the logged sha", S,
     "if not sums.is_file() or A.sha(sums) != sums_sha:", "if not sums.is_file():"),
    ("S41 S1: a stage without the logged sha of the previous file", S,
     "if not prev.is_file() or A.sha(prev) != a.prev:", "if not prev.is_file():"),
    ("S42 S1: a stage runs twice", S, "    if out.exists():\n", "    if False:\n"),
    ("S43 S1: environment change not checked", S, "if env_record() != json.loads(",
     "if False and env_record() != json.loads("),
    ("S44 S1: rest follows the nomination although a verdict exists", S,
     'name = PREV[a.stage] if a.stage != "rest" or (res / PREV["rest"]).is_file() else FILES["ova"]',
     'name = PREV[a.stage] if a.stage != "rest" else FILES["ova"]'),
    ("S45 dedup: disagreeing copies of a scored run accepted", S,
     'raise SystemExit(f"REFUSED: two ledger rows of {k[0]} on {k[1]} disagree")', "pass"),
    ("S46 S1: verify beside a decode job", S, 'if (src / "RUNNING").exists():', "if False:"),
    ("S47 S1: verify without the stored pins", S,
     "bad = [p.name for p, h in stored_files().items() if not p.is_file() or A.sha(p) != h]", "bad = []"),
    ("S48 S1: verify without the §7.1 parity gate", S,
     '    A.c2_parity(A.read_ledgers([led]), w / "in/stage2_ledger.jsonl")\n', ""),
    ("S49 SC5: unequal prompts do not stop", S, '    if pc["unequal"]:\n', "    if False:\n"),
    ("S50 SC5: a check that compared nothing passes", S, '    if n_b1 and not pc["pairs"]:\n', "    if False:\n"),
    ("S51 S1: the VnCoreNLP jar not pinned", S, "if not jar.is_file() or A.sha(jar) != S.JAR_SHA256:",
     "if not jar.is_file():"),
    ("S52 V3: nomination from rows of a backbone without a D1 PASS", S, "if not d1 or stray:", "if not d1:"),
    ("S53 S1: ova without a D1-PASS nominator", S, "    if not ms:\n", "    if False:\n"),
    ("S54 SC4: an incomplete Tier A scored before the refusal", S, "        if not set(B1_COLS) <= have:\n",
     "        if False:\n"),
    ("S55 S1: ovb on a closed 1b", S, 'if nomination(nf).get("closed"):', "if False:"),
    ("S56 S1: a score call without a zs", S, "    if not zs:\n", "    if False:\n"),
    ("S57 §7.9: the carve ledger pin", S, "if A.sha(coco) != A.T1_CARVE_LEDGER_SHA256:", "if False:"),
]
PY = sys.executable
NETNS = ["unshare", "-rn"]


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
        r = subprocess.run([*NETNS, PY, "-X", "utf8", "-I", "-B", str(d / t), "--selftest"],
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
    ap.add_argument("--no-netns", action="store_true")
    a = ap.parse_args()
    if a.no_netns:
        NETNS.clear()
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
