#!/usr/bin/env python3
"""Paper A fix package v2 (A_FIX_PACKAGE_v2.md): rebuild the changed files in memory and, only on request, write them.

Default mode (no argument): CHECK ONLY. Nothing is written. The script
  1. checks the pin of the package file, the paper HEAD and a clean paper/ tree;
  2. reads the OLD/NEW blocks from the package, applies them in id order to `git show HEAD:paper/<file>`
     (each OLD exactly once), skipping the ids in SKIP;
  3. runs the three steps that are not blocks: two manifest rows (read from the package), the provenance table from
     scrub()'s rows, the length block of abstract_A.md;
  4. asserts scrub(supplementary.md) == supplementary_SPIC.md byte for byte (scrub() is imported; scrub_supp.py is NOT run);
  5. asserts the custody zones are byte-unchanged: S11 to the end of both supplement files, sec7_verbosity_sign.md
     (whole file, so Section 6.7), abstract_A.md from "## Abstract", highlights_A.md;
  6. prints the sha256 of every resulting file and compares it with TARGETS.

Write mode:  python3 -I apply_a_v2.py --write --ruling CC-xxx
  writes the files to the working tree only if every result equals TARGETS. TARGETS below are the package writer's own
  values for the full package (Section 7.2 of the package). If the ruling drops or changes a block, set SKIP and replace
  TARGETS by the sha256 values the ruling fixes. Never runs git add or git commit.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

PKG = pathlib.Path("/mnt/d/vsps_image_captioning/manuscript/fix_packages/2026-11-15_A/A_FIX_PACKAGE_v2.md")
PKG_SHA256 = "b9cf7066e03f9bb0d519a6ceab6e822db92b27069f1aa4165fa7fa0b0df89d91"
R = "/mnt/d/vsps_papers/vsps-paperA-spic"
HEAD_SHORT = "dafba17"
SKIP = ()  # block ids the ruling does not apply, e.g. ("A2-F04", "A2-F05", "A2-F06a", "A2-F06b", "A2-F07a", "A2-F07b")
TARGETS = {
    "V2_PROGRESS.md": "42872dc943dab4e230ecaeb556302e93db6fb1d75102f8de64f9463354a6c77e",
    "abstract_A.md": "37f7130181476a46a61e2fc45cf284826899cc755ca51148806269e88b17ba33",
    "anon/declarations_anon.md": "066a325d31be854ffda7abba6f1aa46995c573fadfb904136f4e438471c473db",
    "declarations.md": "5dd7d041c52941017884148eb1f2478cfaf49bacd8ee8e383b7473ac8b89f444",
    "number_manifest.tsv": "d3ca0672f389ebd1621a49de625aa3d926e3603f0f78d7e1ae6881b1b2b41c8b",
    "sec10_discussion.md": "77ceb4083d5c1e39206f8badfabaa8651f6a6a4fb4af7627579035fa04e76a54",
    "sec11_limitations_ethics.md": "5f82aa9e2f96d2bc52d22d493482503c573b60455f2f5e95456de87af10844b0",
    "sec3_measurement_setup.md": "bfc5c286c533b52d881899486ef1eef534dd43940d4028898adc98da9ae8bd8d",
    "sec4_theory.md": "50024781b9b1b658f1671db39c846a72863b5dcb2ce2506041d6943a612c1d01",
    "supplementary.md": "5b77cd93390e12d9532187cae4fdb44dff6f406fbf673b07c36976656c6b13ec",
    "supplementary_SPIC.md": "f26f9209b02fa9071d47eb4dabf3270df690bb7cd85c9ce320e6d43865bdb47f",
    "supplementary_provenance_internal.tsv": "2add9e43ea3d0164462f6bad34dfc7b7028f4016014b01f392d5646e4d4e34fd",
}

write = "--write" in sys.argv
ruling = sys.argv[sys.argv.index("--ruling") + 1] if "--ruling" in sys.argv else None
assert not write or ruling, "--write needs --ruling <id of the GO ruling>"

pkg = PKG.read_bytes()
assert hashlib.sha256(pkg).hexdigest() == PKG_SHA256, "package pin"
git = lambda *a: subprocess.run(["git", "-C", R, *a], capture_output=True, check=True).stdout
assert git("rev-parse", "--short", "HEAD").decode().strip() == HEAD_SHORT, "paper HEAD"
assert git("status", "--porcelain", "--", "paper") == b"", "paper/ tree not clean"
head = lambda f: git("show", "HEAD:paper/" + f).decode()

sys.dont_write_bytecode = True  # leave no cache file in the paper repository
sys.path.insert(0, R + "/paper/build")
from scrub_supp import scrub, LEAK  # noqa: E402  (the function only; the script is not run)

text = pkg.decode()
blocks = re.findall(r"<<<(A2-F\d+[ab]?) (\S+) OLD>>>\n(.*?)\n<<<\1 \2 NEW>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", text, flags=re.S)
assert len(blocks) == 18 and len({b[0] for b in blocks}) == 18, len(blocks)
files = {}
for bid, f, old, new in blocks:
    if bid in SKIP:
        continue
    s = files.setdefault(f, head(f))
    assert head(f).count(old) == 1 and s.count(old) == 1, (bid, head(f).count(old), s.count(old))
    files[f] = s.replace(old, new)
print("blocks applied:", [b[0] for b in blocks if b[0] not in SKIP])

# S1: manifest rows (only if A2-F10 is applied)
if "A2-F10" not in SKIP:
    rows = re.search(r"\*\*S1\. .*?\n```\n(.*?)\n```\n", text, flags=re.S).group(1)
    assert rows.count("\n") == 1 and all(r.count("\t") == 5 for r in rows.split("\n")), "manifest rows"
    man = head("number_manifest.tsv")
    assert man.endswith("\n")
    files["number_manifest.tsv"] = man + rows + "\n"

# S2: supplement sync and provenance table
src = files.get("supplementary.md", head("supplementary.md"))
spic = files.get("supplementary_SPIC.md", head("supplementary_SPIC.md"))
out, prov = scrub(src)
assert out == spic, "scrub(supplementary.md) != supplementary_SPIC.md"
print("BYTE-EQUAL scrub(source) == journal supplement; leak hits (all must lie in S11):",
      sorted({out.count("\n", 0, m.start()) + 1 for m in LEAK.finditer(out)}))
assert all(m.start() > out.index("\n## S11 ") for m in LEAK.finditer(out)), "leak hit outside S11"
if "supplementary.md" in files:
    files["supplementary_provenance_internal.tsv"] = ("comment_no\tsrc_line\theading\tvisible_text_before\tcomment\n"
                                                      + "".join("\t".join(r) + "\n" for r in prov))

# S3: length block of abstract_A.md (an HTML comment before "## Abstract")
words = lambda t: len(re.sub(r"<!--.*?-->", "", t, flags=re.S).split())
MAIN = ["sec1_introduction.md", "sec2_related_work.md", "sec3_measurement_setup.md", "sec4_theory.md", "sec5_exchangeability.md",
        "sec6_rescoring_published_methods.md", "sec7_verbosity_sign.md", "sec8_human_validity.md", "sec9_preference_audit.md",
        "sec10_discussion.md", "sec11_limitations_ethics.md", "declarations.md"]
c0 = {f: words(head(f)) for f in MAIN}
c1 = {f: words(files.get(f, head(f))) for f in MAIN}
t0, t1 = sum(c0.values()), sum(c1.values())
top = sorted(c1.items(), key=lambda x: -x[1])[:3]
ab = head("abstract_A.md")
for a, b in [
    ("recounted 2026-11-14 UTC after the CC-403 text fixes).",
     "recounted 2026-11-14 UTC after the CC-403 text fixes; recounted after fix package v2 of 2026-11-15)."),
    ("Main text now: %s words" % format(t0, ","), "Main text now: %s words" % format(t1, ",")),
    ("Over the limit by %s words." % format(t0 - 8500, ","), "Over the limit by %s words." % format(t1 - 8500, ",")),
    ("Longest files: sec7_verbosity_sign.md 7,523; sec2_related_work.md 2,184; sec11_limitations_ethics.md 2,007.",
     "Longest files: " + "; ".join("%s %s" % (f, format(n, ",")) for f, n in top) + "."),
]:
    assert ab.count(a) == 1, a
    ab = ab.replace(a, b)
files["abstract_A.md"] = ab
print("main text words:", t0, "->", t1)

# custody zones
tail = lambda s, mark: s[s.index(mark):]
for f in ("supplementary.md", "supplementary_SPIC.md"):
    assert tail(files.get(f, head(f)), "\n## S11 ") == tail(head(f), "\n## S11 "), f
assert "sec7_verbosity_sign.md" not in files and "highlights_A.md" not in files
assert tail(ab, "## Abstract") == tail(head("abstract_A.md"), "## Abstract")
print("custody zones unchanged: S11 (both supplement files), Section 6.7, abstract body, highlights")

got = {f: hashlib.sha256(s.encode()).hexdigest() for f, s in sorted(files.items())}
for f, h in got.items():
    print(("OK   " if TARGETS.get(f) == h else "DIFF "), f, h)
same = got == TARGETS
print("ALL RESULTS EQUAL TARGETS" if same else "RESULTS DIFFER FROM TARGETS")
if write:
    assert same, "no file written: results differ from TARGETS"
    for f, s in files.items():
        (pathlib.Path(R) / "paper" / f).write_bytes(s.encode())
    print("WRITTEN: %d files to the working tree under ruling %s (not staged, not committed)" % (len(files), ruling))
else:
    print("CHECK MODE: nothing written")
