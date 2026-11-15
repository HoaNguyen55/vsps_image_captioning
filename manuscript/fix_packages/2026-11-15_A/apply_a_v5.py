#!/usr/bin/env python3
"""Paper A fix package v5 (A_FIX_PACKAGE_v5.md): rebuild the changed files in memory and, only on request, write them.

Group K: the agreement clause of the KTVIC authors beside the KTVIC training sentence (PI-1115i item 8), 4 blocks.
Group R: the correction record to the PASCAL-50S registration (CC-407 W6), one new file at two paths.

Default mode: CHECK ONLY. Nothing is written. The script
  1. checks the pins of the package and of the record, that BASE_COMMIT is HEAD or an ancestor of HEAD, a clean paper/
     tree, and that every file it reads still has its sha256 of BASE_COMMIT;
  2. applies the OLD/NEW blocks of the package to `git show HEAD:paper/<file>` (each OLD exactly once), skipping SKIP;
     after each block the printed text (HTML comments stripped) must equal the printed text before it plus exactly the
     clause of INSERT, or equal it for a comment-only block;
  3. asserts that every agreement clause printed at HEAD is still printed;
  4. S3: updates the counts of the length comment of abstract_A.md (before "## Abstract");
  5. asserts the custody zones: abstract_A.md byte-unchanged from "## Abstract"; sec7_verbosity_sign.md (Section 6.7),
     highlights_A.md, both supplement files (S11), cover letter and title page not written; no run of 8 words from
     Section 6.7, S11, the abstract body or the highlights occurs in the package, the record or this script;
  6. asserts the registration sha256 at both paths, and that each record path is free or already byte-equal;
  7. prints the sha256 of every resulting file and compares it with TARGETS.

Write mode:  python3 -I -B apply_a_v5.py --write --ruling CC-xxx
  writes the files to the working tree and the record to RECORD_DEST only if every result equals TARGETS.
  TARGETS hold only for SKIP = (); if the ruling drops or changes a block, set SKIP and replace TARGETS by the sha256
  values the ruling fixes. Never runs git add or git commit.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = pathlib.Path("/mnt/d/vsps_image_captioning")
PKG = HERE / "manuscript/fix_packages/2026-11-15_A/A_FIX_PACKAGE_v5.md"
PKG_SHA256 = "ff39aeb69ed8358ed8efa30e800616c65cdeb9a0c7f8a67070d4af78bc867b58"
RECORD = HERE / "manuscript/fix_packages/2026-11-15_A/CORRECTION_PASCAL50S_2026-11-15.md"
RECORD_SHA256 = "465ad1b6828d7eb3117ced13717e4a216474e51308581b0c3fc2b616f324b038"
R = pathlib.Path("/mnt/d/vsps_papers/vsps-paperA-spic")
REG = "prereg/2026-10-28_pascal50s/"
REG_SHA256 = "1448ab13fcb509b4f6dff1e15344809f529478f6606df8880498427153c2db3b"
REG_DIRS = [HERE / "manuscript" / REG, R / REG]
RECORD_DEST = [d / "CORRECTION_2026-11-15.md" for d in REG_DIRS]
BASE_COMMIT = "59648b7"
SKIP = ()  # block ids or steps the ruling does not apply, e.g. ("A5-K02",) or ("S3",) or ("R",)
BASE = {
    "abstract_A.md": "38300b3f79fa5a3119dc9ec12f16e39005aa0eeefabe8d4ce02434f3489c41fd",
    "anon/declarations_anon.md": "ec71a9b953ab3609a31f457b8368814c35a82443035885cfa64d9d8df84a96cb",
    "declarations.md": "5920d0fa7461f0a75cd6aae6d58df7e7588111ba9ad39ff76e1aa3af4c4702ba",
    "sec11_limitations_ethics.md": "a7258f2eddb6e137d6abe6990063ce2cc8a4e8e57c9e6bddcef6161e54d2a1e4",
    "sec7_verbosity_sign.md": "b6f46b8aaf33ef133b54e5e4d91f2c1f037e061d48f495e1b23eed5b0aaf4817",
    "highlights_A.md": "64c671615bd5106cba42cf168ff7ff85460bd9bd72b3c52a2d9903861c281aa5",
    "supplementary.md": "dd7277069ced9d4d66c2b57e933d06a9b05cc41aae546b5cefa0c10ddcccc2ee",
    "supplementary_SPIC.md": "0c746c2127cac8bcb25340172e3859cc3c023d4739e7e8d812967287e554f280",
}
WRITABLE = {"abstract_A.md", "anon/declarations_anon.md", "declarations.md", "sec11_limitations_ethics.md"}
TARGETS = {
    "abstract_A.md": "b566eb8e8f4ca29d9ccc5383c987aca53bd54678cddd414e68836d81c7c29752",
    "anon/declarations_anon.md": "e407d32ddd13b2903482472e35cf011e71177ea23f271425e9e38f60ee5172ca",
    "declarations.md": "3b2381ca23d22682dd431dfed5c7a738c2ae41bf55356fa5291b23c6a598b5d2",
    "sec11_limitations_ethics.md": "dff441d598ae945c459dfbc348d2dd51e2a8c2a2621a62a781c0d6836d74a34f",
}
# the only printed text a block may add; None = comment-only block
INSERT = {
    "A5-K01a": " one of us contacted the KTVIC authors, who agreed to this use;",
    "A5-K01b": None,
    "A5-K02": " one of us contacted the KTVIC authors, who agreed to this use;",
    "A5-K03": " One of us contacted the KTVIC authors, who agreed to this use.",
}
MAIN = ["sec1_introduction.md", "sec2_related_work.md", "sec3_measurement_setup.md", "sec4_theory.md", "sec5_exchangeability.md",
        "sec6_rescoring_published_methods.md", "sec7_verbosity_sign.md", "sec8_human_validity.md", "sec9_preference_audit.md",
        "sec10_discussion.md", "sec11_limitations_ethics.md", "declarations.md"]

args = sys.argv[1:]
write = "--write" in args
ruling = args[args.index("--ruling") + 1] if "--ruling" in args else None
assert not write or ruling, "--write needs --ruling <id of the GO ruling>"
assert ("A5-K01a" in SKIP) == ("A5-K01b" in SKIP), "A5-K01a and A5-K01b go together"
sha = lambda b: hashlib.sha256(b).hexdigest()

pkg, rec = PKG.read_bytes(), RECORD.read_bytes()
assert sha(pkg) == PKG_SHA256, "package pin"
assert sha(rec) == RECORD_SHA256, "record pin"
run = lambda *a: subprocess.run(["git", "-C", str(R), *a], capture_output=True)
git = lambda *a: subprocess.run(["git", "-C", str(R), *a], capture_output=True, check=True).stdout
assert run("merge-base", "--is-ancestor", BASE_COMMIT, "HEAD").returncode == 0, BASE_COMMIT + " is not HEAD or an ancestor of HEAD"
assert git("status", "--porcelain", "--", "paper") == b"", "paper/ tree not clean"
head = lambda f: git("show", "HEAD:paper/" + f).decode()
for f, h in BASE.items():
    assert sha(head(f).encode()) == h, "base sha differs: " + f
print("HEAD", git("rev-parse", "--short", "HEAD").decode().strip(), "| base", BASE_COMMIT, "is HEAD or an ancestor | SKIP", SKIP)

printed = lambda t: re.sub(r"<!--.*?-->", "", t, flags=re.S)
CLAUSE = "agreed to this use"
text = pkg.decode()
blocks = re.findall(r"<<<(A5-K\d+[ab]?) (\S+) OLD>>>\n(.*?)\n<<<\1 \2 NEW>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", text, flags=re.S)
assert [b[0] for b in blocks] == list(INSERT), [b[0] for b in blocks]
files, done = {}, []
for bid, f, old, new in blocks:
    if bid in SKIP:
        continue
    assert f in WRITABLE and "\n" not in old + new, bid
    s = files.setdefault(f, head(f))
    assert head(f).count(old) == 1 and s.count(old) == 1 and s.count(new) == 0, (bid, head(f).count(old), s.count(old), s.count(new))
    t = s.replace(old, new)
    ins = INSERT[bid]
    if ins is None:
        assert printed(t) == printed(s), bid + ": a comment-only block changed printed text"
    else:
        assert printed(new).count(ins) == 1 and printed(new).replace(ins, "", 1) == old, bid + ": NEW is not OLD plus the clause"
        assert printed(t).count(ins) == 1 and printed(t).replace(ins, "", 1) == printed(s), bid + ": printed text"
        assert not re.search(r"writ|on file|licen[cs]e|terms|\d", ins), bid
    files[f] = t
    done.append(bid)
    print("%-8s %-28s OLD at HEAD 1 | NEW at HEAD %d | NEW after %d" % (bid, f, head(f).count(new), t.count(new)))
print("blocks applied:", done)

# no agreement clause printed at HEAD is lost: every sentence piece that carries one is still printed
for f in sorted(WRITABLE - {"abstract_A.md"}):
    before, after = printed(head(f)), printed(files.get(f, head(f)))
    for piece in re.split(r"(?<=[.;]) ", before):
        assert CLAUSE not in piece or piece in after, f + ": an agreement clause of HEAD is not printed any more"
    print("agreement clauses printed in %-28s %d -> %d" % (f, before.count(CLAUSE), after.count(CLAUSE)))
    assert after.count(CLAUSE) == before.count(CLAUSE) + sum(1 for b, bf, _, _ in blocks if b in done and INSERT[b] and bf == f)

# S3: counts of the length comment of abstract_A.md
words = lambda t: len(printed(t).split())
c0 = {f: words(head(f)) for f in MAIN}
c1 = {f: words(files.get(f, head(f))) for f in MAIN}
t0, t1 = sum(c0.values()), sum(c1.values())
longest = lambda c: "Longest files: " + "; ".join("%s %s" % (f, format(n, ",")) for f, n in sorted(c.items(), key=lambda x: -x[1])[:3]) + "."
print("main text words:", t0, "->", t1)
if "S3" not in SKIP:
    ab = head("abstract_A.md")
    for a, b in [
        ("recounted after fix package v4 of 2026-11-15).",
         "recounted after fix package v4 of 2026-11-15; recounted after fix package v5 of 2026-11-15)."),
        ("Main text now: %s words" % format(t0, ","), "Main text now: %s words" % format(t1, ",")),
        ("Over the limit by %s words." % format(t0 - 8500, ","), "Over the limit by %s words." % format(t1 - 8500, ",")),
        (longest(c0), longest(c1)),
    ]:
        assert ab.count(a) == 1 and ab.index(a) < ab.index("## Abstract"), a
        ab = ab.replace(a, b)
    files["abstract_A.md"] = ab

# custody zones
tail = lambda s, mark: s[s.index(mark):]
assert tail(files.get("abstract_A.md", head("abstract_A.md")), "## Abstract") == tail(head("abstract_A.md"), "## Abstract")
assert set(files) <= WRITABLE, sorted(set(files) - WRITABLE)
held = " ".join([tail(head("sec7_verbosity_sign.md"), "\n## 6.7"), tail(head("supplementary.md"), "\n## S11 "),
                 tail(head("supplementary_SPIC.md"), "\n## S11 "), tail(head("abstract_A.md"), "## Abstract"),
                 head("highlights_A.md")])
grams = lambda t: {" ".join(w[i:i + 8]) for w in [re.findall(r"\w+", t.lower())] for i in range(len(w) - 7)}
ours = grams(text) | grams(rec.decode()) | grams(pathlib.Path(__file__).read_text(encoding="utf-8"))
hits = len(grams(held) & ours)
assert hits == 0, "%d runs of 8 words of a held zone occur in the package, the record or the script" % hits
print("custody: abstract body unchanged; Section 6.7 file, highlights, both supplement files, cover letter, title page not written; "
      "0 shared runs of 8 words with Section 6.7, S11, the abstract body, the highlights")

# group R: the record beside the registration, which is not edited
if "R" not in SKIP:
    for d, dest in zip(REG_DIRS, RECORD_DEST):
        assert sha((d / "PREREG.md").read_bytes()) == REG_SHA256, "registration sha differs: " + str(d)
        assert not dest.exists() or dest.read_bytes() == rec, "record path is taken by other bytes: " + str(dest)
    print("record", RECORD_SHA256, "| registration unchanged at both paths | destinations free or equal")

got = {f: sha(s.encode()) for f, s in sorted(files.items())}
for f, h in got.items():
    print("OK   " if TARGETS.get(f) == h else "DIFF ", f, h)
same = got == TARGETS
print("ALL RESULTS EQUAL TARGETS" if same else "RESULTS DIFFER FROM TARGETS (with SKIP set, the targets are those of the ruling)")
if write:
    assert same, "no file written: results differ from TARGETS"
    for f, s in files.items():
        (R / "paper" / f).write_bytes(s.encode())
    if "R" not in SKIP:
        for dest in RECORD_DEST:
            dest.write_bytes(rec)
    print("WRITTEN under ruling %s: %d files to the working tree of the paper repository%s (not staged, not committed)" % (
        ruling, len(files), "" if "R" in SKIP else ", the record to %d paths" % len(RECORD_DEST)))
else:
    print("CHECK MODE: nothing written")
