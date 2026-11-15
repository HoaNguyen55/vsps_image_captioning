#!/usr/bin/env python3
"""Paper C fix package v3, related-work rows (C_FIX_PACKAGE_v3_related.md): check, or write to the paper repo WORKING TREE.

Default mode (no argument): CHECK ONLY. Nothing is written. The script
  1. checks the pin of the package file, that commit 9b8e6ae is an ancestor of HEAD, and that the two files this
     package changes are clean against HEAD and equal their 9b8e6ae text (PRE). Neither the freeze shell C2 nor fix
     package v2 changes them, so the same gate holds before and after both;
  2. reads the OLD/NEW blocks from the package and applies them in package order to `git show HEAD:<file>`
     (each OLD exactly once at HEAD and at its turn, each NEW exactly once at the end), skipping the ids in SKIP;
  3. asserts: no number token of 02_related_work.md changes; no table label 10-18 appears there (package v2
     renumbers those); the captions of Tables 1 and 1b are still there; the RAGCap row is byte-unchanged and is
     the only row of Table 1 with a "–" cell; no cell of Table 1b is "–"; the cell changed by C-L06 is the cell
     the evidence file quotes after C-L09;
  4. prints the sha256 of each resulting file and compares it with TARGETS.

Write mode:  python3 -I apply_c_v3_related.py --write --ruling CC-xxx
  writes the two files to the working tree only if every result equals TARGETS and nothing is staged in the paper
  repo (the package is a commit of its own). TARGETS holds the package writer's values for the full package and
  for the package without C-L07. If the ruling drops or changes another block, set SKIP and put the sha256 values
  the ruling fixes into TARGETS; blocks that go together (package section 1) can only be skipped together.
  Never runs git add or git commit.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

PKG = pathlib.Path("/mnt/d/vsps_image_captioning/manuscript/fix_packages/2026-11-15_C/C_FIX_PACKAGE_v3_related.md")
PKG_SHA256 = "e43bd6e7dac448631350e01741d87d4c16d2c382c95e6edd41989246c58cba85"
R = "/mnt/d/vsps_papers/vsps-paperC-tallip"
BASE = "9b8e6ae"
P02, PEV = "paper_v1_analysis/02_related_work.md", "docs/TABLE1B_W5_EVIDENCE.md"
PRE = {  # sha256 at 9b8e6ae
    P02: "da4ba3748a9b6f55d7b911378f14b19bbfa0a0588dd09b83f6bc1dd2bc14e887",
    PEV: "415598fd8bb70d6ff4cb8f6862622657314aff2537d21e924d194f0a3668bce2",
}
SKIP = ()  # block ids the ruling does not apply, e.g. ("C-L07",)
TARGETS = {  # by the sorted tuple of skipped ids
    (): {P02: "8dbc299bd816bb2fd9ec689b1ef1b97a1c2cab1e331232072dc4d7afee1a60fb", PEV: "c3b5aa79df8109cbd7de45933ee77126c5c5a49b4ceab6daf93d01020157d56d"},
    ("C-L07",): {P02: "a31d484361f8e794d59db6635d9a95917aa39e191856979316975b57aebff847", PEV: "c3b5aa79df8109cbd7de45933ee77126c5c5a49b4ceab6daf93d01020157d56d"},
}
RAGCAP_ROW = "| RAGCap [@Bazi2025RAGCap], from its abstract | no | yes | image-caption pairs | – | – | – |"
LI_CELL = "decoder columns in the order-test tables only"
# the two patterns of apply_c_v2.py's renumbering pass, copied
LABEL = r"S?\d+[a-z]?(?:\s*\([a-z]\))?"
TABLE_REF = re.compile(rf"\bTables?\s+{LABEL}(?:(?:,\s*|\s+and\s+|–){LABEL})*")
TABLE_LAB = re.compile(r"(?<![\dS.])(1[0-8])(?![\da-z])")

sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
write = "--write" in sys.argv
ruling = sys.argv[sys.argv.index("--ruling") + 1] if "--ruling" in sys.argv else None
assert not write or ruling, "--write needs --ruling <id of the GO ruling>"

pkg = PKG.read_bytes()
assert hashlib.sha256(pkg).hexdigest() == PKG_SHA256, "package pin"
git = lambda *a: subprocess.run(["git", "-C", R, *a], capture_output=True, check=True).stdout
git("merge-base", "--is-ancestor", BASE, "HEAD")  # raises unless 9b8e6ae is in the history
assert git("status", "--porcelain", "--", *PRE) == b"", "a file of this package differs from HEAD"
head = {f: git("show", "HEAD:" + f).decode() for f in PRE}
for f, h in PRE.items():
    assert sha(head[f]) == h, f + " is not its 9b8e6ae text"

blocks = re.findall(r"<<<(C-L\d+[ab]?) (\S+) OLD>>>\n(.*?)\n<<<\1 \2 NEW>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", pkg.decode(), flags=re.S)
assert len(blocks) == 14 and len({b[0] for b in blocks}) == 14 and {b[1] for b in blocks} == set(PRE), len(blocks)
assert set(SKIP) <= {b[0] for b in blocks}, "unknown id in SKIP"
for group in ({"C-L02", "C-L03", "C-L12"}, {"C-L04", "C-L05", "C-L08", "C-L11", "C-L13"}, {"C-L06", "C-L09"}):
    assert not group & set(SKIP) or group <= set(SKIP), "blocks that go together (package section 1): %s" % sorted(group)
todo = [b for b in blocks if b[0] not in SKIP]
files = {}
for bid, f, old, new in todo:
    s = files.setdefault(f, head[f])
    assert head[f].count(old) == 1 and s.count(old) == 1, (bid, head[f].count(old), s.count(old))
    files[f] = s.replace(old, new)
for bid, f, old, new in todo:
    assert files[f].count(new) == 1, (bid, "NEW not exactly once")
print("blocks applied:", [b[0] for b in todo])

# content checks
ids = {b[0] for b in todo}
new02, newev = files.get(P02, head[P02]), files.get(PEV, head[PEV])
numbers = lambda t: sorted(re.findall(r"\d+(?:[.,]\d+)*", t))
assert numbers(new02) == numbers(head[P02]), "a number token of 02_related_work.md changed"
assert not TABLE_LAB.search(" ".join(TABLE_REF.findall(new02))), "02_related_work.md holds a table label 10-18"
assert new02.count("\n**Table 1. Design of the closest prior work") == 1 and new02.count("\n**Table 1b. This study among") == 1
t1 = new02.split("\n**Table 1. Design")[1].split("\n**Table 1b.")[0]
t1b = new02.split("\n**Table 1b.")[1].split("\n**Position among the analyses.")[0]
cells = lambda row: [c.strip() for c in row.strip().strip("|").split("|")]
dash = lambda tab: [r for r in tab.splitlines() if r.startswith("|") and any(c.startswith("–") for c in cells(r))]
assert new02.count(RAGCAP_ROW) == 1 and head[P02].count(RAGCAP_ROW) == 1, "RAGCap row"
if "C-L03" in ids:
    assert dash(t1) == [RAGCAP_ROW], "Table 1: a row other than RAGCap holds a dash cell"
if "C-L05" in ids:
    assert dash(t1b) == [], "Table 1b holds a dash cell"
if {"C-L06", "C-L09"} <= ids:
    assert new02.count(LI_CELL) == 1 and newev.count("| per-backbone rows | " + LI_CELL + " |") == 1, "C-L06 and C-L09 differ"
print("checks passed: numbers of 02 unchanged; no table label 10-18; captions present; RAGCap row unchanged; dash cells as stated")

got = {f: sha(s) for f, s in sorted(files.items())}
want = TARGETS.get(tuple(sorted(SKIP)))
for f, h in got.items():
    print("OK   " if want and want.get(f) == h else "DIFF ", f, h)
same = want is not None and got == want
print("ALL RESULTS EQUAL TARGETS" if same else "RESULTS DIFFER FROM TARGETS, or no target is pinned for this SKIP")
if write:
    assert same, "no file written: results differ from TARGETS"
    assert git("diff", "--cached", "--name-only") == b"", "no file written: something is staged in the paper repo"
    for f, s in files.items():
        (pathlib.Path(R) / f).write_bytes(s.encode())
    print("WRITTEN: %d files to the working tree under ruling %s (not staged, not committed); paper HEAD %s"
          % (len(files), ruling, git("rev-parse", "--short", "HEAD").decode().strip()))
else:
    print("CHECK MODE: nothing written; paper HEAD", git("rev-parse", "--short", "HEAD").decode().strip())
