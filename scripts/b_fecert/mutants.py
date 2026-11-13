#!/usr/bin/env python3
"""Mutants of scripts/b_fecert and of the pair tool (registration B_FECERT_PREREG_v1_1.md §12; CC-350 W1, W2; CC-353;
CC-361 D5). Each mutant changes one registered rule in a scratch copy of the tree (scripts/b_fecert/ and
tools/obj_rater/ are real copies, the rest of the repo is mirrored by symlinks, as scripts/c_attr/c_attr_mutants.py
does) and runs one self-test:
  - a check name: `b_fecert.py selftest`; KILLED only when the line `SELFTEST FAIL <check>` is printed;
  - "bp:<text>": `build_pairs.py --selftest`; KILLED only when a line starting `SELFTEST FAIL: <text>` is printed.
A crash, or a failure of another check only, is SURVIVED. Both unmutated self-tests must pass first. Exit 0 only if
all are killed ("killed n of n"). Offline, CPU, on the host named at the code read (PI-1111j; CC-353 4(e)):
    python3 -I -B scripts/b_fecert/mutants.py [--jobs 2]
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
F, B = "scripts/b_fecert/family.py", "scripts/b_fecert/b_fecert.py"
BP, PS, PH = "tools/obj_rater/build_pairs.py", "tools/obj_rater/pair_server.py", "tools/obj_rater/pair.html"
MUT = [  # (id, file, old, new, check): each old occurs exactly once in its file
    ("M1 case applied before the unit (§2.1 order)", F, "return p_pre(tone(self.n[raw], t), p)",
     "return p_pre(tone(self.n[raw], t), p).casefold()", "toy_tokens"),
    ("M2 pa keeps tokens made only of punctuation (§2.2)", F,
     'return [w for w in toks if not all(map(_punct, w))] if level == "pa" else toks', "return toks", "toy_tokens"),
    ("M3 tm/tf outside the strict g2 domain: onset unchecked (B_KAPPA §2.3)", F,
     "if pair not in PAIRS or onset not in ONSETS:", "if pair not in PAIRS:", "tone_domain"),
    ("M4 tm and tf swapped (B_KAPPA §2.4)", F, '([], [tone]) if level == "tm" else ([tone], [])',
     '([tone], []) if level == "tm" else ([], [tone])', "tone_domain"),
    ("M5 chr admitted to F (CC-350 ruling 2)", F, "F_HELD = members(HELD_UNITS)  # 18",
     "F_HELD = members(HELD_UNITS + (CHR,))  # 18", "family_enumeration"),
    ("M6 step N keeps underscores (§2.1)", F, '.replace("_", " ")', '.replace("_", "_")', "toy_tokens"),
    ("M7 F1 drops a unit only above 5% (§2.6)", F, "F1_FAIL_MAX = 0.005", "F1_FAIL_MAX = 0.05", "f1_rule"),
    ("M8 mismatched pipeline in the certificate (§2.3)", B,
     'R = {i: [tk.side(r, "matched", m, True) for r in refs[i]] for i in ids}',
     'R = {i: [tk.side(r, "out", m, True) for r in refs[i]] for i in ids}', "matched_scoring"),
    ("M9 classes merged by score (§2.5)", B, "k = f\"{pa['key']}|{pb['key']}|{kr}\"",
     'k = str(round(float((pa["cider"] - pb["cider"]).mean()), 6))', "merge_by_tokens"),
    ("M10 one-sided interval (§3.1)", B, "return [float(d.mean()), float(lo), float(hi), float(boot.std(ddof=1))]",
     "return [float(d.mean()), *map(float, np.percentile(boot, [5.0, 95.0])), float(boot.std(ddof=1))]",
     "bootstrap_ref"),
    ("M11 no image resampling (files resampled, not images) (§3.1)", B, "boot = W @ d / len(d)",
     "boot = np.full(B, d.mean())", "bootstrap_ref"),
    ("M12 separate draws per member (§3.1)", B, 'add_class(c, m, per[c["a"]], per[c["b"]], per["_refs"], W)',
     'add_class(c, m, per[c["a"]], per[c["b"]], per["_refs"], boot_W(len(ids), SEED + len(c["classes"])))',
     "same_draws"),
    ("M13 CHANGED denominator over all comparisons (§3.2)", B, '"CHANGED_share": k / n_sig if n_sig else None,',
     '"CHANGED_share": k / len(vs) if vs else None,', "certificate_cases"),
    ("M14 REVERSED not counted as FRAGILE (§3.2)", B, '"fragile": not cert and any(sg),',
     '"fragile": not cert and any(sg) and not (1 in sg and -1 in sg),', "certificate_cases"),
    ("M15 near-margin z < 4 (§6.1)", B, "near = [i for i, z in cert if z <= Z_NEAR]",
     "near = [i for i, z in cert if z < Z_NEAR]", "near_margin"),
    ("M16 fallback below 58 (§6.1)", B, 'return (near, "near-margin z_min <= 4") if len(near) >= N_MIN else',
     'return (near, "near-margin z_min <= 4") if len(near) >= N_MIN - 1 else', "near_margin"),
    ("M17 two-sided Clopper-Pearson bound (§6.1)", B, "float(beta.ppf(1 - CP_ALPHA, k + 1, n - k))",
     "float(beta.ppf(1 - CP_ALPHA / 2, k + 1, n - k))", "cp_points"),
    ("M18 P1 FAIL read from the upper bound (§6.1)", B, "elif lo > R_MAX:", "elif up > R_MAX:", "p1_labels"),
    ("M19 P1 evaluable at N = 58 (§10 K-N)", B, "if held_empty or n < N_MIN:", "if held_empty or n < N_MIN - 1:",
     "p1_labels"),
    ("M20 P1 evaluable with F_held empty (§10 K-unit; CC-353 N4)", B, "if held_empty or n < N_MIN:",
     "if n < N_MIN:", "f_held_empty"),
    ("M21 K-unit drop ignored for F_held (§10)", B, "held = [u for u in FM.HELD_UNITS if u not in drop]",
     "held = list(FM.HELD_UNITS)", "f_held_empty"),
    ("M22 a census hit does not move uts (CC-353 N4)", B, 'if cen["uts_moved_to_dev"]:', "if False:", "census_uts"),
    ("M23 the census misses underthesea (CC-353 N4)", B,
     'uts = sorted({f for f, s in toks if "underthesea" in s or s.endswith("_uts")})', "uts = []", "census_uts"),
    ("M24 P2 at k >= 2 (§6.2)", B, '"SUPPORTED" if k >= KFL_MIN and k / n >= KFL_SHARE else',
     '"SUPPORTED" if k >= KFL_MIN - 1 and k / n >= KFL_SHARE else', "p2_labels"),
    ("M25 P2 share > 0.10 (§6.2)", B, '"SUPPORTED" if k >= KFL_MIN and k / n >= KFL_SHARE else',
     '"SUPPORTED" if k >= KFL_MIN and k / n > KFL_SHARE else', "p2_labels"),
    ("M26 P2 evaluable at n = 9 (§6.2)", B, "if n < NFL_MIN:", "if n < NFL_MIN - 1:", "p2_labels"),
    ("M27 NC breaks counted under syl (CC-350 W1)", B,
     'br = sum(held_break(c, v["certified"], other)[0] for c, v in cert if c["id"] in Vs)',
     'br = sum(held_break(c, v["certified"], syl)[0] for c, v in cert if c["id"] in Vs)', "nc_check"),
    ("M28 reproduction tolerance of a full unit (§5.1)", B, "return 0.5 * 10 ** (-d) + 1e-9",
     "return 10 ** (-d) + 1e-9", "fe_id_tolerance"),
    ("M29 wrong recovery not a FAULT (§6.4; CC-350 W2)", B, "    if wrong:", "    if False:", "p4_fault"),
    ("M30 K-plant at 13 (§6.4)", B, '"NOT_EVALUABLE (K-plant)" if c["IDENTIFIED"] < PLANT_MIN else',
     '"NOT_EVALUABLE (K-plant)" if c["IDENTIFIED"] <= PLANT_MIN else', "p4_fault"),
    ("M31 CIDEr-D counted in M_new (§6.3; CC-350 W3)", B,
     'm_new = sorted({m for b in rows for m in rows[b]} - {"CIDEr-D", "BLEU-4"})',
     'm_new = sorted({m for b in rows for m in rows[b]} - {"BLEU-4"})', "p3_labels"),
    ("M32 K-coco drop ignored in the P3 scope (§6.3)", B, "scope = [m for m in P3_SCOPE if m not in dropped]",
     "scope = list(P3_SCOPE)", "p3_labels"),
    ("M33 gate coverage 90% (§4.3 item 2)", B, 'GATE = {"coverage": 0.95,', 'GATE = {"coverage": 0.90,', "gate_rules"),
    ("M34 gate reference-copy share 50% (§4.3 item 5)", B, '"refcopy": 0.05,', '"refcopy": 0.5,', "gate_rules"),
    ("M35 gate diacritic rule off (§4.3 item 6)", B, '"diacritic": 0.50,', '"diacritic": 0.0,', "gate_rules"),
    ("M36 gate duplicate rule off (§4.3 item 3)", B, '("3 dup", v["dup"] <= GATE["dup"])', '("3 dup", True)',
     "gate_rules"),
    ("M37 comparison formed at 90% overlap (§4.3)", B, '"overlap": 0.95}', '"overlap": 0.90}', "gate_rules"),
    ("M38 stage started without the --prev sha (§9)", B, "if not prev or not p.is_file() or sha(p) != prev:",
     "if not p.is_file():", "stage_order"),
    ("M39 stage started without the previous LOG line (§9)", B,
     "if log is not None and not pin_line(log, prev, fname, *also):", "if False:", "stage_order"),
    ("M40 held-out member scored before the V.json LOG line (§9; CC-350 W1)", B,
     "if log is not None and not pin_line(log, prev, fname, *also):",
     'if log is not None and fname != "V.json" and not pin_line(log, prev, fname, *also):', "gate_2b_V"),
    ("M41 FL scored before GATE2.json is logged (§4.3)", B,
     '"2a": ("FAMILY.json", "GATE2.json", "NC.json"),', '"2a": ("FAMILY.json", "NC.json"),', "gate_2a_gate2"),
    ("M42 stage 2a without the DEV.json + NC.json pin line (§9)", B,
     'if not pin_line(log, sha(work / "NC.json"), "NC.json", a.prev, "DEV.json"):', "if False:", "gate_2a_pin"),
    ("M43 stage 2a with a RESULT*.json present (§9)", B, 'if any(work.glob("RESULT*.json")):', "if False:",
     "gate_2a_result"),
    ("M44 held-out member allowed before the pin (§9)", B, "mems = FM.members(dev)  # F_dev only before the pin (§9)",
     "mems = FM.members(dev + held)", "dev_no_heldout"),
    ("M45 K-time not enforced (§10)", B, 'raise SystemExit("REFUSED: K-time (§10): the stage is NOT RUN")', "pass",
     "k_time"),
    ("M46 stage 3 without a logged PRINTED.json (§10 K-print)", B, "elif not (a.k_print and now() > K_PRINT):",
     "elif False:", "k_print"),
    ("M47 stage H without the closing line (plan §6)", B,
     "if not pin_line(Path(a.log), sha(files[0]), files[0].name, *also):", "if False:", "h_closing"),
    ("M48 G-repro tolerance 0.1 (B_KAPPA §5.1)", B, "GREPRO_TOL = 0.01", "GREPRO_TOL = 0.1", "g_repro"),
    ("M49 pyvi version not pinned (§2.2)", B, 'if rec["pyvi"] != PYVI_VERSION:', "if False:", "env_pins"),
    ("M50 caption text written to GATE2.json (no caption text rule)", B, "v.update(admitted=not bad, reasons=bad)",
     'v.update(admitted=not bad, reasons=bad, first=rows[0][1] if rows else "")', "no_text"),
    ("M51 image file taken as '<id>.jpg' (CC-350 W6)", B, 'fn = im.get("filename")  # the one key',
     "fn = f\"{int(im['id']):011d}.jpg\"  # the one key", "image_route"),
    ("M52 image route regex .jpg only (plan §9 pair_server item 2)", B,
     'FN_RE = re.compile(r"([0-9]{11})\\.(jpg|jpeg|png)")', 'FN_RE = re.compile(r"([0-9]{11})\\.jpg")', "image_route"),
    ("M53 pair strata at ε = 9 (plan §2.2)", B, "EPS = 10.0  # plan §2.2", "EPS = 9.0  # plan §2.2", "pair_strata"),
    ("M54 display keeps final punctuation (plan §3.1)", B, 'd = FM.p_pre(FM.n_step(t), "pf")', "d = FM.n_step(t)",
     "pair_strata"),
    ("M55 H-P two-sided (plan §5.2)", B,
     'binomtest(rows["P"]["k_word"], rows["P"]["n_dec"], 0.5, alternative="greater").pvalue',
     'binomtest(rows["P"]["k_word"], rows["P"]["n_dec"], 0.5).pvalue', "h_labels"),
    ("M56 Holm skipped (plan §5.2)", B, "go = go and p[h] <= alpha / (len(order) - j)", "go = p[h] <= alpha",
     "kappa_hand"),
    ("M57 H-P power threshold n > 47 (plan §5.2)", B, '"NOT SUPPORTED" if nP >= H_P_POWER else "UNDERPOWERED"',
     '"NOT SUPPORTED" if nP > H_P_POWER else "UNDERPOWERED"', "h_labels"),
    ("M58 H-U eligibility at 99 (plan §7)", B, 'if elig["U"] < H_U_MIN:', 'if elig["U"] < H_U_MIN - 1:', "h_labels"),
    ("M59 kappa without chance correction (plan §5.4)", B,
     "pe = sum((x.count(c) / len(x)) * (y.count(c) / len(y)) for c in cats)", "pe = 0.0", "kappa_hand"),
    ("M60 BLEU-4 with the average reference length (kit 'closest')", B,
     "min((abs(x - len(h)), x) for x in lens)[1]]", "sum(lens) // len(lens)]", "bleu_counts"),
    # ---------------------------------------------------------------------------------- round 2 (CC-361 D5)
    ("R1 D1 printed ROUGE left unmapped", B, '"ROUGE": "ROUGE-L", "ROUGE-L": "ROUGE-L",', '"ROUGE-L": "ROUGE-L",',
     "printed_adapter"),
    ("R2 D1 an unmapped printed system accepted", B,
     'if k not in PRINTED_SYSTEMS or r["metric_as_printed"] not in PRINTED_METRICS:',
     'if r["metric_as_printed"] not in PRINTED_METRICS:', "printed_adapter"),
    ("R3 D1 PRINTED.json sha not asserted", B, "if sha(p) != PRINTED_SHA:", "if False:", "printed_adapter"),
    ("R4 D3 stage 1 writes a wrong field name", B, 'CAND_FIELDS = ("a", "b", "stratum", "d_syl", "d_word", "d_pk")',
     'CAND_FIELDS = ("a", "b", "stratum", "d_syl", "dword", "d_pk")', "pairs_integration"),
    ("R5 D3 build_pairs accepts a candidate field outside the contract", BP,
     "if any(set(c) != CAND_FIELDS for cs in cand[\"images\"].values() for c in cs):", "if False:",
     "bp:stops on a candidate field outside"),
    ("R6 D4 practice counted as main", B, 'main = sorted(q for q, k in key.items() if k["part"] == "main")',
     'main = sorted(q for q, k in key.items() if k["part"] != "repeat")', "key_contract"),
    ("R7 D4 a wrong field name in the key contract", B, '"file_left", "file_right", "d_syl", "d_word", "d_pk", "repeat_of"}',
     '"left", "file_right", "d_syl", "d_word", "d_pk", "repeat_of"}', "key_contract"),
    ("R8 D4 screen sides read from the wrong field", B,
     'return "a" if (k["file_left"] if lab == "A" else k["file_right"]) == k["a"] else "b"',
     'return "a" if (k["file_right"] if lab == "A" else k["file_left"]) == k["a"] else "b"', "key_contract"),
    ("R9 D6 a raising unit becomes a K-unit drop", F, "    got = seg[unit](xs)\n",
     "    try:\n        got = seg[unit](xs)\n    except Exception:\n        got = []\n", "f1_rule"),
    ("R10 D6 a different underthesea release accepted", B, 'if (rec["underthesea"] != UTS_VERSION or ', "if (",
     "env_pins"),
    ("R11 D6 underthesea without its wheel sha256 accepted", B,
     '(rec["underthesea_wheel"] or {}).get("sha256") != UTS_WHEEL_SHA', "False", "env_pins"),
    ("R12 D6 underthesea signature not required", B, '            or not rec["underthesea_signature"]):',
     "            ):", "env_pins"),
    ("R13 D7 pycocoevalcap version not checked", B, 'or rec["pycocoevalcap"] != COCO_VERSION ', "", "env_pins"),
    ("R14 D7 Java version not checked", B, '            or rec["java"] != JAVA_VERSION):', "            ):",
     "env_pins"),
    ("R15 D7 an r* ImportError becomes a K-coco drop", B,
     "except ImportError as e:  # an environment fault, never a K-coco drop (CC-361 D7)",
     "except ArithmeticError as e:", "k_coco_import"),
    ("R16 D8 a work file altered after its LOG line accepted", B, "    for n in names:\n        logged(log, work / n)",
     "    for n in names:\n        pass", "inputs_logged"),
    ("R17 D8 test_data.json not re-checked against FAMILY.json", B,
     'if sha(REFS) != jload(work / "FAMILY.json")["refs_sha256"]:', "if False:", "inputs_logged"),
    ("R18 D8 SYSTEMS.tsv not bound by CENSUS.json", B,
     'if sha(work / "SYSTEMS.tsv") != jload(work / "CENSUS.json")["systems_tsv_sha256"]:', "if False:",
     "inputs_logged"),
    ("R19 D9 a reference sha mismatch accepted", B, "if g in REF_SHA and sha(p) != REF_SHA[g]:", "if False:",
     "fl_provenance"),
    ("R20 D9 an FL output off its fetch record accepted", B, "    if not ok:\n        raise Fault(f\"{rel}",
     "    if False:\n        raise Fault(f\"{rel}", "fl_provenance"),
    ("R21 D9 reference file not re-checked against GATE2.json", B,
     'if d["refs_sha256"] != gate["refs_sha256"][g]:', "if False:", "fl_provenance"),
    ("R22 D10 --b2-score given as a file", B,
     'b2files = sorted(b2dir.rglob("*.json")) if b2dir is not None and b2dir.is_dir() else []',
     'b2files = sorted(b2dir.rglob("*.json")) if b2dir is not None and b2dir.is_dir() else ([b2dir] if b2dir else [])',
     "census_b2dir"),
    ("R23 D11 missing answers kept in the kappa gate", B,
     'all(ans[r][q] not in (None, "cannot") for r in ("PI", "R2"))', 'all(ans[r][q] != "cannot" for r in ("PI", "R2"))',
     "kappa_gate"),
    ("R24 D12 BLEU-1 dropped from FE-ID", B, 'ID_METRICS = ("BLEU-1", "BLEU-4", "ROUGE-L", "CIDEr-D")',
     'ID_METRICS = ("BLEU-4", "ROUGE-L", "CIDEr-D")', "identify_labels"),
    ("R25 D12 r* not held to every printed metric", B,
     "want = lambda c: printed if c[0] == FM.name(FM.RSTAR) else pm", "want = lambda c: pm", "identify_labels"),
    ("R26 D13 coded reading (a): a mismatch outside S not a FAULT", B, 'if not all(r["ok"] for r in rows):',
     'if not all(r["ok"] for r in rows if r["name"] in S_FILES):', "g_repro"),
    ("R27 D15 qid without the salt", BP, 'return hashlib.sha256(f"{salt}|{SEED}|{part}|{i}|{a}|{b}".encode())',
     'return hashlib.sha256(f"{SEED}|{part}|{i}|{a}|{b}".encode())', "key_contract"),
    ("R28 D15 a fixed salt on real builds", BP, "salt = salt or secrets.token_hex(16)", 'salt = salt or "0" * 32',
     "key_contract"),
    ("R29 D14 pair_server serves with a missing image", PS, "if fn not in names or not (images / fn).is_file():",
     "if fn not in names:", "bp:pair_server refuses to start when a served image is missing"),
    ("R30 D16 one character of the instruction block altered in pair.html", PH, "Trước hết", "Trước hét",
     "bp:pair_server starts on the built fixture with the real pair.html"),
    ("R31 D16 the instruction block not compared with the registration", PS,
     "if block is None or hashlib.sha256(block).hexdigest() != INSTRUCTIONS_VI_SHA256:", "if block is None:",
     "bp:pair_server refuses a page whose instruction block differs by one character"),
    ("R32 NB5 any annotator code accepted", PS, "if annotator not in ANNOTATORS:", "if False:",
     "bp:pair_server: --annotator PI or R2 only"),
    ("R33 NB5 --dir outside ~/vsps_labels_b/ accepted", PS, "if not under(d.resolve(), labels_root.resolve()):",
     "if False:", "bp:pair_server refuses a --dir under /mnt"),
    ("R34 NB9 PAIR_CANDIDATES.json sha not checked", BP, "if sha(cand_path) != cand_sha:", "if False:",
     "bp:stops when PAIR_CANDIDATES.json differs"),
]
PY = sys.executable


def tree(root: Path) -> Path:
    """root mirrors the repo by symlinks; scripts/b_fecert (family.py, b_fecert.py) and tools/obj_rater are real
    copies, so a mutant never writes through a symlink and every import resolves inside root."""
    for top in ("scripts", "tools"):
        (root / top).mkdir(parents=True)
    for e in REPO.iterdir():
        if e.name not in ("scripts", "tools", ".git"):
            (root / e.name).symlink_to(e)
    for top, real in (("scripts", "b_fecert"), ("tools", "obj_rater")):
        for e in (REPO / top).iterdir():
            if e.name != real:
                (root / top / e.name).symlink_to(e)
        (root / top / real).mkdir()
    for f in (F, B):
        shutil.copy2(REPO / f, root / f)
    for e in (REPO / "tools/obj_rater").iterdir():
        if e.is_file():
            shutil.copy2(e, root / "tools/obj_rater" / e.name)
    return root


def selftest(root: Path, bp: bool = False) -> tuple[int, list[str]]:
    cmd = [PY, "-X", "utf8", "-I", "-B", str(root / BP), "--selftest"] if bp else \
        [PY, "-X", "utf8", "-I", "-B", str(root / B), "selftest"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    return r.returncode, (r.stdout + "\n" + r.stderr).splitlines()


def one(m) -> tuple[str, bool, str]:
    mid, f, old, new, chk = m
    src = (REPO / f).read_text(encoding="utf-8")
    if src.count(old) != 1:
        return mid, False, f"PATTERN NOT FOUND ONCE ({src.count(old)})"
    root = Path(tempfile.mkdtemp(prefix="b_fecert_mut_"))
    try:
        tree(root)
        (root / f).write_text(src.replace(old, new), encoding="utf-8")
        bp = chk.startswith("bp:")
        rc, out = selftest(root, bp)
        killed = any(ln.startswith(f"SELFTEST FAIL: {chk[3:]}") for ln in out) if bp else f"SELFTEST FAIL {chk}" in out
        return mid, killed, f"rc {rc}; {chk} {'FAIL' if killed else 'not FAIL'}"
    finally:
        shutil.rmtree(root)  # copies and symlinks only; rmtree never follows symlinks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=2)
    a = ap.parse_args()
    for bp in (False, True):
        root = Path(tempfile.mkdtemp(prefix="b_fecert_mut_"))
        try:
            rc, out = selftest(tree(root), bp)
        finally:
            shutil.rmtree(root)
        if rc:
            print(out[-1] if out else f"rc {rc}")
            print("an unmutated self-test does not pass: no mutant run")
            return 2
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(one, MUT))
    for mid, killed, note in res:
        print(f"{'KILLED  ' if killed else 'SURVIVED'} {mid} ({note})")
    k = sum(r[1] for r in res)
    print(f"killed {k} of {len(res)}")
    return 0 if k == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
