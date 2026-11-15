#!/usr/bin/env python3
"""Paper A fix package v3, related-work rows (A_FIX_PACKAGE_v3_related.md): check, or write to the paper repo WORKING TREE.

Default mode (no argument): CHECK ONLY. Nothing is written. The script
  1. checks the pin of the package file, that commit dafba17 is an ancestor of HEAD, and that
     paper/sec2_related_work.md is clean against HEAD and equals its dafba17 text (PRE). Package v2 (commit
     ea12e51) does not change that file, so the same gate holds before and after it;
  2. reads the OLD/NEW blocks from the package and applies them in id order to `git show HEAD:<file>`
     (each OLD exactly once at HEAD and at its turn, each NEW exactly once at the end), skipping the ids in SKIP;
  3. asserts: the word count of the file by the method of the length block of abstract_A.md is unchanged, so
     that block stays exact; no number token changes; the citation mentions found by the build's own pattern
     (paper/build/prep.py, imported, not run) are the same; the Rashidi row and the note "described from its
     abstract only" are byte-unchanged; the only file produced is paper/sec2_related_work.md, so Section 6.7,
     Supplementary S11, the abstract and the highlights are not written;
  4. prints the sha256 of the resulting file and compares it with TARGETS.

Write mode:  python3 -I apply_a_v3_related.py --write --ruling CC-xxx
  writes the file to the working tree only if the result equals TARGETS and nothing is staged in the paper repo
  (the package is a commit of its own). TARGETS holds the package writer's values for both blocks and for
  A3-L01 alone. If the ruling changes a NEW text, the pin and the targets must be recomputed. Never runs git add
  or git commit.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

PKG = pathlib.Path("/mnt/d/vsps_image_captioning/manuscript/fix_packages/2026-11-15_A/A_FIX_PACKAGE_v3_related.md")
PKG_SHA256 = "3ad1aa24be12b2106853a73e408529ebff8f20d7fc5bd3b55e0f8dfbcb67b7be"
R = "/mnt/d/vsps_papers/vsps-paperA-spic"
BASE = "dafba17"
SEC2 = "paper/sec2_related_work.md"
PRE = {SEC2: "de85f341f07c90b09d90164abcaec474f0f78c80ea1353cf7f2c3455a9d5b080"}  # sha256 at dafba17 and at ea12e51
SKIP = ()  # block ids the ruling does not apply: () or ("A3-L02",)
TARGETS = {  # by the sorted tuple of skipped ids
    (): {SEC2: "5beb9da16eec16b2c7afb67bb3512fa3422ea0b9e0a4e85fd311ed30224a38c4"},
    ("A3-L02",): {SEC2: "e901f2b3081634abd1e163946a807275f85af4ec5cc3730e7e547cebd4797400"},
}
KEPT = ("Rashidi et al. (2024) is described from its abstract only.",
        "| Rashidi et al. (2024), ACM TOIS, doi 10.1145/3596511 |",
        "under a tunable model of judge error (abstract only)",
        "except Rashidi et al. (2024), of which only the abstract was read")

sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
write = "--write" in sys.argv
ruling = sys.argv[sys.argv.index("--ruling") + 1] if "--ruling" in sys.argv else None
assert not write or ruling, "--write needs --ruling <id of the GO ruling>"

pkg = PKG.read_bytes()
assert hashlib.sha256(pkg).hexdigest() == PKG_SHA256, "package pin"
git = lambda *a: subprocess.run(["git", "-C", R, *a], capture_output=True, check=True).stdout
git("merge-base", "--is-ancestor", BASE, "HEAD")  # raises unless dafba17 is in the history
assert git("status", "--porcelain", "--", *PRE) == b"", "the file of this package differs from HEAD"
head = {f: git("show", "HEAD:" + f).decode() for f in PRE}
for f, h in PRE.items():
    assert sha(head[f]) == h, f + " is not its dafba17 text"

blocks = re.findall(r"<<<(A3-L\d+) (\S+) OLD>>>\n(.*?)\n<<<\1 \2 NEW>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", pkg.decode(), flags=re.S)
assert [b[0] for b in blocks] == ["A3-L01", "A3-L02"] and {b[1] for b in blocks} == set(PRE), blocks
assert set(SKIP) <= {"A3-L02"}, "only A3-L02 may be skipped"
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
assert set(files) == {SEC2}, "a file other than sec2_related_work.md would be written"
old2, new2 = head[SEC2], files[SEC2]
words = lambda t: len(re.sub(r"<!--.*?-->", "", t, flags=re.S).split())  # method of the length block
assert words(new2) == words(old2), "word count of sec2_related_work.md changes: the length block would be stale"
numbers = lambda t: sorted(re.findall(r"\d+(?:[.,]\d+)*", t))
assert numbers(new2) == numbers(old2), "a number token changed"
for s in KEPT:
    assert old2.count(s) == 1 and new2.count(s) == 1, "the note on Rashidi et al. changed: " + s
sys.dont_write_bytecode = True  # leave no cache file in the paper repository
sys.path.insert(0, R + "/paper/build")
from prep import COMMENT, MENTION, initials  # noqa: E402  (patterns only; prep.py is not run)
mentions = lambda t: sorted((initials(m.group("ini")), m.group("s1"), m.group("years"))
                            for m in MENTION.finditer(COMMENT.sub(lambda c: " " * len(c.group(0)), t)))
assert mentions(new2) == mentions(old2), "the citation mentions changed"
print("checks passed: %d words before and after; number tokens unchanged; %d citation mentions unchanged; "
      "Rashidi notes unchanged; only sec2_related_work.md is produced" % (words(new2), len(mentions(new2))))

got = {f: sha(s) for f, s in sorted(files.items())}
want = TARGETS.get(tuple(sorted(SKIP)))
for f, h in got.items():
    print("OK   " if want and want.get(f) == h else "DIFF ", f, h)
same = want is not None and got == want
print("ALL RESULTS EQUAL TARGETS" if same else "RESULTS DIFFER FROM TARGETS")
if write:
    assert same, "no file written: results differ from TARGETS"
    assert git("diff", "--cached", "--name-only") == b"", "no file written: something is staged in the paper repo"
    for f, s in files.items():
        (pathlib.Path(R) / f).write_bytes(s.encode())
    print("WRITTEN: %d file to the working tree under ruling %s (not staged, not committed); paper HEAD %s"
          % (len(files), ruling, git("rev-parse", "--short", "HEAD").decode().strip()))
else:
    print("CHECK MODE: nothing written; paper HEAD", git("rev-parse", "--short", "HEAD").decode().strip())
