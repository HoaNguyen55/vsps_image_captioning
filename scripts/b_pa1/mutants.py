#!/usr/bin/env python3
"""Guard mutants for b_pa1.py (C6) and b_pa1_w25.py (C3-C5, C7), CC-226 NB-3. Each mutant breaks one guard in a
scratch copy of scripts/ (every other file a symlink, so common.ROOT stays the repo), runs the selftests offline
(unshare -rn) and must make one fail. Run from anywhere:  python3 scripts/b_pa1/mutants.py
Venvs (named): ~/.venvs/c_stage1_lists (torch, imagehash; freeze 1a639a50) and ~/.venvs/b_pa1_ijson (ijson 3.6.0).
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENV_T = os.path.expanduser("~/.venvs/c_stage1_lists/bin/python")
VENV_J = os.path.expanduser("~/.venvs/b_pa1_ijson/bin/python")
P, W = "b_pa1.py", "b_pa1_w25.py"
RUNS = {P: [(VENV_J, [P, "slices", "selftest"]), (sys.executable, [P, "selftest"]), (VENV_T, [W, "selftest"])],
        W: [(VENV_T, [W, "selftest"])]}
MUT = [  # (id, file, old, new): each old must occur exactly once
    ("S1 patch filter", P, 'if not patched or t[0] in FRAME_PATCHES]', 'if True]'),
    ("S2 mixed patches", P, 'or 0 < patched < len(rows):', 'or False:'),
    ("S3 order salt", P, 'SALT, BLOCK, SLICE_N = "b-pa1-o365-slice|"', 'SALT, BLOCK, SLICE_N = "b-pa1-o365-slice"'),
    ("S4 '..' path", P, 'and ".." not in f.split("/")', ''),
    ("S5 absolute path", P, 'and not f.startswith("/")', ''),
    ("S6 tab in name", P, 'and "\\t" not in f ', ''),
    ("S7 int id", P, 'type(i) is int and i >= 0 and ', 'i is not None and '),
    ("S8 repeated name", P, 'or len({f for _, f in keep}) != len(keep):', ':'),
    ("S9 empty frame", P, 'if not keep or len(', 'if len('),
    ("S10 ann sha = --ann-sha", P, 'or K.sha_file(a.ann) != a.ann_sha or', 'or'),
    ("S11 new file only", P, 'None:\n    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)',
     'None:\n    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)'),
    ("S12 frame ids distinct", P, 'len({r[0] for r in rows}) != len(rows)', 'False'),
    ("S13 cut frame sha", P, 'if rec.get("frame_sha256") != frame_sha or rec.get', 'if rec.get'),
    ("S14 cut exclusion sha", P, 'or rec.get("excluded_sha256") != hashlib.sha256(excluded).hexdigest():', ':'),
    ("S15 cut shortage", P, 'if len(surv) < 2 * n:', 'if False:'),
    ("S16 cut decided blocks only", P, 'frame[:rec["n_frame_decided"]]', 'frame'),
    ("S17 W2 train json name", P, 'if a.ann.name != ANN_NAME or K.sha_file', 'if K.sha_file'),
    ("S18 W2 R6 LOG pin", P, 'or not pin_line(log, a.ann_sha, ANN_NAME):', ':'),
    ("S19 NB-1 pin token", P, 'any(PIN_RE.search(ln) and all(t.search(ln)', 'any(all(t.search(ln)'),
    ("S20 NB-1 full sha", P, 'if len(sha) != 64 or not log.is_file():', 'if not log.is_file():'),
    ("S21 W1(c) pick pin", P, 'if not pin_line(log, sha(db), "w25_decide.json", "P6 met"):', 'if False:'),
    ("S22 W1(c) 'P6 met' token", P, 'pin_line(log, sha(db), "w25_decide.json", "P6 met")', 'pin_line(log, sha(db), "w25_decide.json")'),
    ("S23 NB-6 missing FAULT", P, 'if rec["missing"]:', 'if False:'),
    ("S24 NB-6 name key", P, 'sum("/".join(f.split("/")[-2:]) not in have', 'sum(f not in have'),
    ("W1 overlay sha prefix", W, 'not e["sha256"].startswith(pre) or', ''),
    ("W2 overlay rows in cell", W, 'f"{e[\'n\']:,}" not in c[3] or', ''),
    ("W3 overlay path", W, 'not (e["path"] == path_r5 or (tail != path_r5 and e["path"].endswith(tail)))', 'False'),
    ("W4 overlay cache set", W, 'if set(ca) != set(cache):', 'if False:'),
    ("W5 overlay owner set", W, 'if {k for k, o in owners.items() if o["row"].isdigit()} != set(owner_keys):', 'if False:'),
    ("W6 overlay unknown cache", W, 'or set(ks) - set(caches) or', 'or'),
    ("W7 overlay rule required", W, 'if not (gs or c[4].startswith("exempt")) or', 'if'),
    ("W8 pinned doc sha", W, 'if not p.is_file() or K.sha_file(p) != sha:', 'if not p.is_file():'),
    ("W9 overlay LOG pin", W, 'if not B.pin_line(log, rules_sha, rules.name):', 'if False:'),
    ("W10 overlay = owners file", W, '{k for k, o in ru["owners"].items() if o["row"].isdigit()} != set(doc["owners"])', 'False'),
    ("W11 K2 LOG pin", W, 'return c["src"] != "LOG" or B.pin_line', 'return True or B.pin_line'),
    ("W12 C3 unreadable rows", W, ' - {int(i) for i in z["unreadable"].tolist()}', ''),
    ("W13 C3 row count", W, 'if len(ids) != c["n"] or (listed', 'if (listed'),
    ("W14 C3 C-EN list", W, '(listed is not None and not ids <= listed)', 'False'),
    ("W15 C3 cache sha", W, 'if K.sha_file(p) != c["sha256"]:', 'if False:'),
    ("W16 C3 owner ids sha", W, 'if len(o["ids"]) != o["n"] or IC.sha_ids(o["ids"]) != o["ids_sha256"]:', 'if len(o["ids"]) != o["n"]:'),
    ("W17 C3 base K2", W, 'BASE = ("K1", "K2", "K3")', 'BASE = ("K1", "K3")'),
    ("W18 C3 base K3 (J7)", W, 'BASE = ("K1", "K2", "K3")', 'BASE = ("K1", "K2")'),
    ("W19 C3 new out-dir", W, '    if out.exists():\n        raise SystemExit(f"REFUSED: {out} exists")\n    doc, ru', '    doc, ru'),
    ("W20 J6 overlay source = R5", W, 'if ru["source"]["sha256"] != R5_SHA or ru', 'if ru'),
    ("W21 C4 outside repo", W, 'if p == K.ROOT or K.ROOT in p.parents:', 'if False:'),
    ("W22 C4 staged", W, 'raise SystemExit(f"FAULT: block {n}: {lost} frame image(s) not staged")', 'pass'),
    ("W23 C4 unreadable", W, 'raise SystemExit(f"FAULT: block {n}: {len(f[\'unreadable\'])} frame image(s) cannot be hashed")', 'pass'),
    ("W24 C4 resume", W, 'if out.exists() or not blk:', 'if not blk:'),
    ("W25 NB-4 truncated count", W, 'block=n, truncated=len(f["truncated"]), utc', 'block=n, utc'),
    ("W26 C4 parity cosine", W, 'or not (cos >= PARITY_COS).all():', ':'),
    ("W27 C4 parity file sha", W, 'and new["sha"] == ref["sha"][:n] and', 'and'),
    ("W28 NB-2 decide needs parity", W, 'psha = parity_ok(parts, fsha, part_shas[0])', 'psha = None'),
    ("W29 NB-2 parity block 0", W, 'or r.get("part_0000_sha256") != part0_sha or', 'or'),
    ("W30 NB-2 parity frame", W, 'if r.get("frame_sha256") != fsha or r.get', 'if r.get'),
    ("W31 C5 contiguous parts", W, 'if not files or [p.name for p in files] != [f"part_{n:04d}.npz" for n in range(len(files))]:', 'if not files:'),
    ("W32 C5 part frame sha", W, 'if part_meta(p).get("frame_sha256") != fsha or f["unreadable"] or', 'if f["unreadable"] or'),
    ("W33 C5 part ids", W, ' or \\\n                f["ids"] != [i for i, _ in rows[n * block:(n + 1) * block]]:', ':'),
    ("W34 C5 never overwrite", W, '    if out.exists():\n        raise SystemExit(f"REFUSED: {out} exists (never overwritten)")\n', ''),
    ("W35 C5 cache usable", W, 'if not usable(c, log):\n        raise SystemExit(f"FAULT: {Path', 'if False:\n        raise SystemExit(f"FAULT: {Path'),
    ("W36 C5 cache rows", W, 'if len(f["ids"]) - len(f["unreadable"]) != c["n"]:', 'if False:'),
    ("W37 C5 K4 XM drop", W, 'keep = [i for i, n in enumerate(f["ids"]) if oid[n] not in xm]', 'keep = list(range(len(f["ids"])))'),
    ("W38 C5 union", W, '        ex |= r["excluded"]\n    ids = sorted(int(i)', '        ex = r["excluded"]\n    ids = sorted(int(i)'),
    ("W39 C5 G1 caches", W, 'if "G1" in o["rules"] for c', 'if False for c'),
    ("W40 C7 list ids distinct", W, 'len({r[0] for r in rows}) != len(rows):\n        raise SystemExit("REFUSED: not a C7', 'False:\n        raise SystemExit("REFUSED: not a C7'),
    ("W41 C7 list path plain", W, 'or not B.plain(0, r[1]) for r in rows', 'for r in rows'),
    ("W42 C7 unfetched count", W, '        else:\n            lost += 1', '        else:\n            pass'),
    ("W43 C7 M1 host", W, 'return mid.is_file() and mid.read_text().strip() == "m3"', 'return True'),
    ("W44 C7 COCO id", W, 'if space not in COCO_DIRS or not i.isdigit():', 'if space not in COCO_DIRS:'),
    ("W45 C7 unreadable count", W, '"n_readable": len(rows) - len(f["unreadable"])', '"n_readable": len(rows)'),
    ("W46 W1(b) provenance", W, 'if any(m.get(k) != v for k, v in expect.items()) or n != c["n"]', 'if n != c["n"]'),
    ("W47 W1(b) manifest count", W, 'or n != c["n"] or m.get("n_readable")', 'or m.get("n_readable")'),
    ("W48 W1(b) manifest owners", W, 'm.get("owners") != c["owners"] or not re', 'not re'),
    ("W49 W1(b) LOG pin", W, 'if not B.pin_line(log, c["sha256"], p.name, f"n={n}", *counts, *judged, m["list_sha256"]):', 'if False:'),
    ("W50 W1(b) n= on the pin", W, 'p.name, f"n={n}", *counts', 'p.name, *counts'),
    ("W51 W1(b) no K name", W, 'if k in caches or not c["owners"]', 'if not c["owners"]'),
    ("W52 W1(b) owners known", W, 'or not set(c["owners"]) <= set(doc["owners"]):', ':'),
    ("A1 W3 anchor ^", P, 'PIN_RE = re.compile(r"^\\d{4}', 'PIN_RE = re.compile(r"\\d{4}'),
    ("A2 W3 stamp -> \\S+", P, r'r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z OPS-', r'r"^\S+ OPS-'),
    ("A3 W3 '-pin:' id", P, 'OPS-[0-9A-Za-z-]+-pin: ")', 'OPS-[0-9A-Za-z-]+: ")'),
    ("A4 W3 free PIN branch", P, 'PIN_RE = re.compile(r"^\\d{4}', 'PIN_RE = re.compile(r"\\bPIN\\b|^\\d{4}'),
    ("A5 W3 OPS id", P, 'Z OPS-[0-9A-Za-z-]+-pin: ")', 'Z [0-9A-Za-z-]+-pin: ")'),
    ("A6 W3 pin test", P, 'PIN_RE.search(ln) and all(', 'True and all('),
    ("B1 delimit left", P, 'rf"(?<!\\S)(?:', 'rf"(?:'),
    ("B2 delimit right", P, ')})(?!\\S)")', ')})")'),
    ("B3 delimit both (substring)", P, 'rf"(?<!\\S)(?:{t.pattern if isinstance(t, re.Pattern) else re.escape(t)})(?!\\S)"', 'rf"(?:{t.pattern if isinstance(t, re.Pattern) else re.escape(t)})"'),
    ("B4 delimit right allows punctuation", P, ')})(?!\\S)")', ')})(?![^\\s,;])")'),
    ("B5 every token checked", P, 'toks = [delimited(t) for t in (sha, name, *also)]', 'toks = [delimited(t) for t in (sha, name)]'),
    ("B6 judged id required", W, 'r"truncated-judged=CC-[0-9A-Za-z-]+"', 'r"truncated-judged=CC-[0-9A-Za-z-]*"'),
    ("J7 pick file name", P, 'pin_line(log, sha(db), "w25_decide.json", "P6 met")', 'pin_line(log, sha(db), "", "P6 met")'),
    ("J1 --fetch host at call", W, 'if not a.images and not m1_host(mid):', 'if False:'),
    ("J2 C7 out outside repo", W, '    outside_repo(out.parent)\n    if out.exists():\n        raise SystemExit(f"REFUSED: {out} exists")\n    sscd', '    if out.exists():\n        raise SystemExit(f"REFUSED: {out} exists")\n    sscd'),
    ("J3a C7 retry flag passed", W, 'workers=workers, retry_truncated=retry)', 'workers=workers, retry_truncated=True)'),
    ("J3b C7 retry flag recorded", W, '"retry_truncated": retry, "n_listed"', '"retry_truncated": True, "n_listed"'),
    ("J5 W1(b) list sha hex", W, ' or not re.fullmatch(r"[0-9a-f]{64}", str(m.get("list_sha256")))', ''),
    ("N1 m1_host OSError", W, 'except OSError:\n        return False', 'except FileNotFoundError:\n        return False'),
    ("C7-listed token", W, 'for k in ("listed", "missing", "unreadable", "truncated")]', 'for k in ("missing", "unreadable", "truncated")]'),
    ("C7-missing token", W, 'for k in ("listed", "missing", "unreadable", "truncated")]', 'for k in ("listed", "unreadable", "truncated")]'),
    ("C7-unreadable token", W, 'for k in ("listed", "missing", "unreadable", "truncated")]', 'for k in ("listed", "missing", "truncated")]'),
    ("C7-truncated token", W, 'for k in ("listed", "missing", "unreadable", "truncated")]', 'for k in ("listed", "missing", "unreadable")]'),
    ("C7 truncated needs judge", W, 'judged = [JUDGED] if m["n_truncated"] else []', 'judged = []'),
    ("W53 W1(b) owner coverage", W, 'len({str(i) for i in doc["owners"][o].get("ids", [])} & have)', '0'),
]


def tree(root: Path) -> Path:
    (root / "scripts/b_pa1").mkdir(parents=True)
    for d in HERE.parent.iterdir():
        if d.name != "b_pa1":
            (root / "scripts" / d.name).symlink_to(d)
    for f in HERE.iterdir():
        if f.is_file():
            (root / "scripts/b_pa1" / f.name).symlink_to(f)
    return root / "scripts/b_pa1"


def run(d: Path, f: str) -> tuple[bool, str]:
    for py, args in RUNS[f]:
        r = subprocess.run(["unshare", "-rn", py, "-I", *args], cwd=d, capture_output=True, text=True, timeout=600)
        if r.returncode:
            tail = [x for x in (r.stderr or r.stdout).splitlines() if x.strip() and not x.startswith("unreadable")]
            return False, f"{args[0]} {args[1]}: {tail[-1][:100] if tail else r.returncode}"
    return True, ""


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="b_pa1_mut_"))
    try:
        d = tree(root)
        for f in (P, W):
            ok, why = run(d, f)
            assert ok, f"control fails: {why}"
        print("control: all selftests pass on the unmutated files")
        survived = []
        for mid, f, old, new in MUT:
            src = (HERE / f).read_text(encoding="utf-8")
            if src.count(old) != 1:
                print(f"{mid}: PATTERN NOT FOUND ONCE ({src.count(old)})")
                survived.append(mid)
                continue
            (d / f).unlink()
            (d / f).write_text(src.replace(old, new), encoding="utf-8")
            ok, why = run(d, f)
            print(f"{mid}: {'SURVIVED' if ok else 'KILLED'} {why}", flush=True)
            survived += [mid] if ok else []
            (d / f).unlink()
            (d / f).symlink_to(HERE / f)
        print(f"{len(MUT) - len(survived)}/{len(MUT)} killed; survived: {survived or 'none'}")
        return 1 if survived else 0
    finally:
        shutil.rmtree(root)


if __name__ == "__main__":
    sys.exit(main())
