#!/usr/bin/env python3
"""Paper A fix package v4, group U only (UIT-ViIC training statement), applied on top of the C+N commit f57c091.

CC-412 Ruling 8 and W3: apply_a_v4.py cannot be reused after the C+N commit, so this is the new apply step. It
  1. checks the pins of the package and of the ruling file, that C_N_COMMIT is HEAD or an ancestor of HEAD, a clean
     paper/ tree, and that every file it reads is byte-equal at HEAD and at C_N_COMMIT;
  2. applies the seven A4-U blocks of the package to `git show HEAD:paper/<file>` (each OLD exactly once), after checking
     the wording limits of CC-412 Ruling 4 on the NEW strings;
  3. runs the steps the package gives to group U: S1 two manifest rows, S2 the provenance table from scrub()'s rows
     (scrub() is imported; scrub_supp.py is NOT run), S3 the counts of the length comment of abstract_A.md
     (its ONE "recounted after fix package v4 of 2026-11-15" mention is kept, not repeated);
  4. asserts the custody zones byte-unchanged: S11 to the end of both supplement files, sec7_verbosity_sign.md from
     "## 6.7", abstract_A.md from "## Abstract"; highlights, cover letter, title page and Section 2 are not written;
  5. compares every file of the end-state table of Ruling 8 (parsed from the ruling file, 11 files) with the result.

Default: CHECK ONLY, prints EQUAL or DIFFERENT per file with both shas.
Write:   python3 -I -B apply_a_v4_groupU.py --write --ruling CC-412 --pi-decision PI-1115i
         writes the changed files to the working tree only if all 11 are EQUAL. Never runs git add or git commit.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = pathlib.Path("/mnt/d/vsps_image_captioning")
PKG = HERE / "manuscript/fix_packages/2026-11-15_A/A_FIX_PACKAGE_v4.md"
PKG_SHA256 = "53ebce0260bc39c3341c1d108392277b1b4b187236d1300f884db1cc1429c390"
RULING = HERE / ".session_backup/2026-10-13/decisions/CC-412.txt"
RULING_SHA256 = "64f9b55c7f84122b26555426ebd5af6f36961782defcdf068754e1b806af6fb9"
R = "/mnt/d/vsps_papers/vsps-paperA-spic"
C_N_COMMIT = "f57c091"
MAIN = ["sec1_introduction.md", "sec2_related_work.md", "sec3_measurement_setup.md", "sec4_theory.md", "sec5_exchangeability.md",
        "sec6_rescoring_published_methods.md", "sec7_verbosity_sign.md", "sec8_human_validity.md", "sec9_preference_audit.md",
        "sec10_discussion.md", "sec11_limitations_ethics.md", "declarations.md"]
V4_MENTION = "recounted after fix package v4 of 2026-11-15"

args = sys.argv[1:]
opt = lambda name: args[args.index(name) + 1] if name in args else None
write, ruling, pi = "--write" in args, opt("--ruling"), opt("--pi-decision")
assert not write or (ruling == "CC-412" and pi), "--write needs --ruling CC-412 --pi-decision <LOG id of the investigator's decision>"
sha = lambda b: hashlib.sha256(b).hexdigest()

pkg, rul = PKG.read_bytes(), RULING.read_bytes()
assert sha(pkg) == PKG_SHA256, "package pin"
assert sha(rul) == RULING_SHA256, "ruling pin"
text = pkg.decode()

# end-state table: Ruling 8 only (from its heading to the REQUIRED FIXES heading)
r8 = rul.decode()
r8 = r8[r8.index("\nRULING 8."):r8.index("\nREQUIRED FIXES")]
want = dict(re.findall(r"^  paper/(\S+)\s+([0-9a-f]{64})$", r8, flags=re.M))
assert len(want) == 11, len(want)
words_want = int(re.search(r"The main text then has ([\d,]+) words", r8).group(1).replace(",", ""))

run = lambda *a: subprocess.run(["git", "-C", R, *a], capture_output=True)
git = lambda *a: subprocess.run(["git", "-C", R, *a], capture_output=True, check=True).stdout
assert run("merge-base", "--is-ancestor", C_N_COMMIT, "HEAD").returncode == 0, C_N_COMMIT + " is not HEAD or an ancestor of HEAD"
assert git("status", "--porcelain", "--", "paper") == b"", "paper/ tree not clean"
read = sorted(set(want) | set(MAIN) | {"build/scrub_supp.py"})
assert run("diff", "--quiet", C_N_COMMIT, "HEAD", "--", *("paper/" + f for f in read)).returncode == 0, \
    "a file differs between %s and HEAD" % C_N_COMMIT
head = lambda f: git("show", "HEAD:paper/" + f).decode()
print("HEAD", git("rev-parse", "--short", "HEAD").decode().strip(), "|", C_N_COMMIT, "is HEAD or an ancestor | group U")

sys.path.insert(0, R + "/paper/build")
from scrub_supp import scrub, LEAK  # noqa: E402  (the function only; the script is not run)

blocks = re.findall(r"<<<(A4-U\d+[a-f]?) (\S+) OLD>>>\n(.*?)\n<<<\1 \2 NEW>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", text, flags=re.S)
assert [b[0] for b in blocks] == ["A4-U01", "A4-U02", "A4-U03", "A4-U04a", "A4-U04b", "A4-U05a", "A4-U05b"], [b[0] for b in blocks]

# CC-412 Ruling 4: no stronger wording for the second adapter; the kept clauses word for word
KEPT = {
    "A4-U01": ["we have not received written permission from the UIT-ViIC authors and claim none"],
    "A4-U02": ["we have not received written permission from the UIT-ViIC authors and claim none"],
    "A4-U03": ["we have not received written permission from the UIT-ViIC authors (Lam et al., 2020)",
               "One of us contacted the UIT-OpenViIC authors, who agreed to this use;", "aggregate statistics and pointers"],
    "A4-U04a": ["and we have not received written permission from the UIT-ViIC authors"],
    "A4-U04b": ["and we have not received written permission from the UIT-ViIC authors"],
}
files, done = {}, []
for bid, f, old, new in blocks:
    assert not re.search(r"first caption|fused caption|verbatim|\d rows|rows per|licen[cs]e|agreement|overlap", new, flags=re.I), bid
    for k in KEPT.get(bid, []):
        assert old.count(k) == 1 and new.count(k) == 1, (bid, k)
    s = files.setdefault(f, head(f))
    assert head(f).count(old) == 1 and s.count(old) == 1, (bid, head(f).count(old), s.count(old))
    files[f] = s.replace(old, new)
    assert files[f].count(new) == 1, bid
    done.append(bid)
print("blocks applied:", done)

# S1: two manifest rows
rows = re.search(r"\*\*S1\. .*?\n```\n(.*?)\n```\n", text, flags=re.S).group(1)
assert rows.count("\n") == 1 and all(r.count("\t") == 5 for r in rows.split("\n")), "manifest rows"
man = head("number_manifest.tsv")
assert man.endswith("\n") and rows not in man
files["number_manifest.tsv"] = man + rows + "\n"

# S2: supplement sync and provenance table
out, prov = scrub(files["supplementary.md"])
assert out == files["supplementary_SPIC.md"], "scrub(supplementary.md) != supplementary_SPIC.md"
assert all(m.start() > out.index("\n## S11 ") for m in LEAK.finditer(out)), "leak hit outside S11"
files["supplementary_provenance_internal.tsv"] = ("comment_no\tsrc_line\theading\tvisible_text_before\tcomment\n"
                                                  + "".join("\t".join(r) + "\n" for r in prov))

# S3: counts of the length comment (the v4 mention is already there, exactly once)
words = lambda t: len(re.sub(r"<!--.*?-->", "", t, flags=re.S).split())
c1 = {f: words(files.get(f, head(f))) for f in MAIN}
t1 = sum(c1.values())
print("main text words:", sum(words(head(f)) for f in MAIN), "->", t1, "| Ruling 8:", words_want)
ab = head("abstract_A.md")
assert ab.count(V4_MENTION) == 1 and ab.index(V4_MENTION + ").") < ab.index("## Abstract"), "length comment: v4 mention"
for pat, new in [
    (r"Main text now: [\d,]+ words", "Main text now: %s words" % format(t1, ",")),
    (r"Over the limit by [\d,]+ words\.", "Over the limit by %s words." % format(t1 - 8500, ",")),
    (r"Longest files: [^\n]*\.", "Longest files: " + "; ".join(
        "%s %s" % (f, format(n, ",")) for f, n in sorted(c1.items(), key=lambda x: -x[1])[:3]) + "."),
]:
    assert len(re.findall(pat, ab)) == 1, pat
    ab = re.sub(pat, new, ab)
assert ab.count(V4_MENTION) == 1
files["abstract_A.md"] = ab

# custody zones
tail = lambda s, mark: s[s.index(mark):]
for f in ("supplementary.md", "supplementary_SPIC.md"):
    assert tail(files[f], "\n## S11 ") == tail(head(f), "\n## S11 "), f
assert "sec7_verbosity_sign.md" not in files and "\n## 6.7" in head("sec7_verbosity_sign.md")
assert tail(files["abstract_A.md"], "## Abstract") == tail(head("abstract_A.md"), "## Abstract")
assert not {"highlights_A.md", "cover_letter_A.md", "title_page_A.md", "sec2_related_work.md"} & set(files)
assert set(files) <= set(want), sorted(set(files) - set(want))
print("custody zones unchanged: S11 (both supplement files), Section 6.7 (file not written), abstract body; "
      "highlights, cover letter, title page, Section 2 not written")

same = True
for f, h in sorted(want.items()):
    got = sha(files.get(f, head(f)).encode())
    same &= got == h
    print("EQUAL    " if got == h else "DIFFERENT", f, "result", got, "ruling", h, "" if f in files else "(not changed by group U)")
print("ALL 11 EQUAL THE RULING 8 END STATE" if same else "RESULT DIFFERS FROM RULING 8: needs a one-judge diff read; no target is adjusted")
if write:
    assert same, "no file written: results differ from the Ruling 8 end state"
    for f, s in files.items():
        (pathlib.Path(R) / "paper" / f).write_bytes(s.encode())
    print("WRITTEN: %d files to the working tree under ruling %s, investigator's decision %s (not staged, not committed)" % (
        len(files), ruling, pi))
else:
    print("CHECK MODE: nothing written")
