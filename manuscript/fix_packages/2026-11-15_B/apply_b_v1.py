#!/usr/bin/env python3
"""Paper B fix package v1 (B_FIX_PACKAGE_v1.md): rebuild the changed files in memory and, only on request, write them.

Source of the items: ruling CC-420 (ruling 5 "owed", N1, N3, N4, N5) and the readiness audit
manuscript/READY_AUDIT_B_2026-11-15.md, re-checked against paper/rev_2026-11-15/ at commit 568eaec.
Blocks (OLD/NEW pairs of the package): group L (two unprinted length comments), group D (declarations), group T
(title page), group C (cover letter and the companion manuscript), group P (pointers to Online Resource 1),
group I (log line ids), group R (reading note of Online Resource 2), group M (models used as instruments).
Steps that are not blocks: R1 pointers "Supplement S..." of the moved old text; C2 the first author's ORCID link
copied from the earlier title page; X1 internal ids inside four ruled sentences (NOT applied by default: it needs a
ruling); S1 the two generated side files; N1 the sums file of the folder; B1 the new build script.

Default mode: CHECK ONLY. Nothing is written. The script
  1. checks the pins (package, build script, the two side files), that BASE_COMMIT is HEAD or an ancestor of HEAD,
     a clean paper/ tree, and that every file it reads has its sha256 of BASE_COMMIT;
  2. applies each block to `git show HEAD:<file>` (OLD exactly once at HEAD, NEW absent), then the steps;
  3. asserts that every ruled sentence stands as often as at HEAD (step X1 excepted, for its four places only),
     that no number of the reader-visible text is added or removed, that no block adds wording on AI tools as
     writing aids, a personal e-mail address, an IPv4 address or the words "in writing" / "on file", and that the
     count of agreement clauses changes only by block B1-D03;
  4. prints the sha256 of every resulting file and compares it with TARGETS.

Write mode:  python3 -I -B apply_b_v1.py --write --ruling CC-xxx
  writes the files to the working tree only if every result equals TARGETS. TARGETS hold for SKIP = ("X1",) and,
  with TARGETS_X1, for SKIP = (). If the ruling drops another block or step, set SKIP, regenerate the two side
  files with the draft's checker and replace TARGETS by the values the ruling fixes. Never runs git add or commit.
--repo DIR: another copy of the paper repository (for the write test on a scratch clone).
"""
import collections
import hashlib
import pathlib
import re
import subprocess
import sys

sys.dont_write_bytecode = True
DIR = pathlib.Path(__file__).resolve().parent
PINS = {
    "B_FIX_PACKAGE_v1.md": "9426de18d595ef25a5b9f550b9c0ed6d7c3d964982c1ab39a36786bb46a1a2b0",
    "build_B_rev.sh": "bd24f0c84e51d1703185247945adc0a29f9e37d8d06099048f0d1a25eba06956",
    "number_manifest_B_v2.after_v1.tsv": "da7614f0189811c02ddf7d958277d6a275b74e6bc49024dcbf5ad859727e3261",
    "PARAGRAPH_SOURCES.after_v1.tsv": "1a4e6e5557768b3b7823d423df0d9c921d4ca4c1a58267067c944a03c53a3342",
}
BASE_COMMIT = "568eaec"
REL = "paper/rev_2026-11-15/"
SKIP = ("X1",)  # block ids (e.g. "B1-D03") or steps ("R1", "C2", "X1", "S1", "N1", "B1") that are not applied
BASE = {
    REL + "paper.md": "aeeaa0161768ff954013ebd3634e60703778ca7b534857f7ca578ecc2905d74e",
    REL + "online_resource.md": "72be760a96de10853f8d7d642fc5984277ef0984ba1b7d9e53d15491b85df738",
    REL + "cover_letter.md": "0ea8ad6e983c05759678857a6b4177332a0b97c7e47a7fa1c73480ccacc777f4",
    REL + "title_page.md": "50397e9d13e763536936813166b4549b1c36f93628ea52fc4b2c0075b09a4971",
    REL + "number_manifest_B_v2.tsv": "da7614f0189811c02ddf7d958277d6a275b74e6bc49024dcbf5ad859727e3261",
    REL + "PARAGRAPH_SOURCES.tsv": "4514c505f3729823091a733f7ca460f0526d17d2b5155ad3d9f775a722fa4233",
    REL + "SNAPSHOT.sha256": "c68d9bebf3adb26819e7647e7a3b76c208193c69308a5fe9c915b007a7f1d8c7",
    "paper/title_page_B.md": "c90471ab94136225e209a9da38501b5b430753811a536d954bda9aef70ef0ff6",
}
NEW_FILE = "paper/build/build_B_rev.sh"
NOT_WRITTEN = {"paper/title_page_B.md"}
N_BLOCKS = 18
COMMENT_ONLY = {"B1-L01", "B1-L02"}
TARGETS = {
    "paper/build/build_B_rev.sh": "bd24f0c84e51d1703185247945adc0a29f9e37d8d06099048f0d1a25eba06956",
    "paper/rev_2026-11-15/PARAGRAPH_SOURCES.tsv": "1a4e6e5557768b3b7823d423df0d9c921d4ca4c1a58267067c944a03c53a3342",
    "paper/rev_2026-11-15/SNAPSHOT.sha256": "e956a461cdae3a62b504b1b1637ae1ee54413967af0aabd816550f71009b1514",
    "paper/rev_2026-11-15/cover_letter.md": "4432a7650c69f61ea23aaf802a1d252148be5f9df569c05483626889b8317b1e",
    "paper/rev_2026-11-15/online_resource.md": "a297079051410a6d1ea52d2136545545cfc173ef92f0ff26c1ae6deb2c587e9b",
    "paper/rev_2026-11-15/paper.md": "6c042e2d8f191bcd187c21ea9d1362288ba0dbbf66ebf864d6b7bc512dd42432",
    "paper/rev_2026-11-15/title_page.md": "c80121d214969cf0749076e7c5edd5088b05c9e43d16b78b6b7509c989104218",
}
TARGETS_X1 = {  # the three files that differ when step X1 is applied as well (SKIP = ())
    "paper/rev_2026-11-15/SNAPSHOT.sha256": "33e008cb534d532e2d9ba69f0a0a89191bc7a57ae2a3a3d3c7a05dc8dad63366",
    "paper/rev_2026-11-15/online_resource.md": "22a6bdf844912ec0303c96c14112d7f8128b7214c42103a5123697864d1600bc",
    "paper/rev_2026-11-15/paper.md": "afae736135877485c1337fad2871e4f3bf4d160ce3e3abd2de80c95eb465ed9f",
}
SNAPSHOT_ORDER = ["paper.md", "online_resource.md", "cover_letter.md", "title_page.md", "FIGURE_TABLE_SPEC.md",
                  "REFERENCE_VERIFICATION.md", "number_manifest_B_v2.tsv", "PARAGRAPH_SOURCES.tsv", "paperB_additions_PROPOSED.bib"]
# Sentences fixed word for word by rulings CC-418 (S1, S5, S6, S7, S8, D1, D4, the quotation of S3), CC-415
# (ruling 3 = D2) and CC-417 (ruling 5 = D3), and the registered words of P2; with the count at HEAD in the two
# text files together. They are compared on whitespace-normalised reader-visible text.
RULED = [
    ("In the human arm, two raters judged 300 caption pairs. Inter-rater agreement was low (Cohen's kappa = 0.351, bootstrap 95% interval 0.270 to 0.433; registered band 0.20 to below 0.40), so by the registered rule neither hypothesis carries a label. On pairs whose order changes with punctuation handling, the order with punctuation removed matched both raters' choice in 16 of 28 decisive pairs (0.571; 95% interval 0.372 to 0.755; one-sided p = 0.286). On pairs whose order changes with the unit, the word order matched both raters' choice in 37 of 75 decisive pairs (0.493; 0.376 to 0.611; two-sided p = 1.000). Neither test was rejected under Holm's correction; no label is attached.", 3),
    ("the human arm, at low inter-rater agreement, gave no labelled result on which to recommend another member.", 3),
    ("The band is set by the point value; its interval reaches above 0.40.", 1),
    ("On control pairs, which all three members order the same way, both raters chose the caption the metric ranks higher in 20 of 26 decisive pairs (0.769; 0.564 to 0.910).", 1),
    ("Two raters judged the pairs, one of them an author. They agreed on the preferred caption or on a tie in 170 of 300 pairs (kappa 0.351). On the 30 hidden repeats the author rater repeated the first answer in 0.933 of cases and the non-author rater in 0.567. The rows of each rater alone are in Table 6; none carries a verdict.", 1),
    ("Under the project's custody rule, the results of the other stages were withheld from the author rater until the labelling was closed; the project log records no disclosure to him before that.", 1),
    ("\"One rater is an author (the PI), who knows the study's hypotheses but could not see which system or front end produced a caption.\"", 2),
    ("In a departure from the registered procedure, neither rater took the eight-pair practice round: both answered on the main page, where the instructions panel starts closed; the registered analysis uses all answers unchanged.", 3),
    ("The second rater answered in person on an author's laptop, on the same rating page and instructions; a key-protected remote link had been prepared and opened but no answer was saved through it. During the session the author passed on one request to pause and one to continue, and said nothing about the items. That this rater worked alone, without the author watching or explaining and without search or AI tools, rests on the statement of the author; no third party observed the session, and the rating server keeps no record of the answering client.", 2),
    ("Before the second rater began, that rater's rating page was reachable for about 27 minutes at a public address without the access key, opened by another software tool on the laptop; no answer existed at that time, and it is not known whether anyone opened the page.", 2),
    ("\"never changes F, a certificate, a P1 to P3 label or the P4 method check\"", 2),
    ("\"the certificate changed few conclusions in this pool (2 of 10)\"", 4),
]
X1_OLD, X1_NEW, X1_N = "(registration l.304)", "(registration, Section 6.5)", 3
X1_RES_OLD = ("the recommendation sentence departs from the verbatim clause as ruled before stage H existed (CC-396 JQ6). "
              "Stage H is the analysis of the human arm; the verbatim clause")
X1_RES_NEW = ("the recommendation sentence departs from the verbatim clause, as an internal read fixed before the analysis "
              "of the human arm existed; the verbatim clause")
# R1: the three pointer forms of the moved old text, applied to the reader-visible part of the lines inside the
# @OLD regions of online_resource.md; expected number of replacements and of changed lines
R1 = [(r"Supplementary Table (S\d+\.\d+)", r"Table \1"), (r"Supplementary (S\d+)\b", r"Section \1"), (r"Supplement (S\d+)\b", r"Section \1")]
R1_N, R1_LINES = 21, 14
R1_NOTE = ('<!-- EDITED: fix package v1 of 2026-11-15: %d pointer(s) of the form "Supplement S…" or "Supplementary S…" renamed to '
           '"Section S…" or "Table S…" of this resource; no other word, no number and no verdict changed. -->')
C2_TOKEN = "{ORCID link of the first author, copied by the script}"
ORCID = re.compile(r"https://orcid\.org/\d{4}-\d{4}-\d{4}-\d{3}[\dX]")
AI_WORDS = re.compile(r"\bAI\b|artificial intelligence|generative|ChatGPT|GPT-|Claude|Gemini|Copilot|writing assistant|language tool")
FORBIDDEN_NEW = re.compile(r"\bin writing\b|\bon file\b|written confirmation|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}|\b(?:\d{1,3}\.){3}\d{1,3}\b|HELD from the PI")
CLAUSE = re.compile(r"\bagreed to\b")
# reader-visible numbers, as the draft's checker counts them (check_draft.py: STRIP, NUM)
PLACEHOLDER = (r"\[(STAGE H|AUTHOR TO PROVIDE|AUTHOR TO CONFIRM|AUTHORS:|TO CONFIRM|TO VERIFY|TO RE-VERIFY"
               r"|CITE-TO-VERIFY|PI-\d ANCHOR|FIGURE TO BUILD)[^\]]*\]")
REFS = (r"(?i:\b(?:sections?|tables?|figs?\.|figures?|online resources?|stages?|rules?|predictions?"
        r"|recommendations?))\s+[A-Z]?\d[\w.]*(?:(?:,\s*|\s+and\s+|\s+to\s+|–)[A-Z]?\d[\w.]*)*")
STRIP = [r"<!--.*?-->", r"`[^`]*`", r"https?://\S+", PLACEHOLDER, r"\d{4}-\d{2}-\d{2}(?:T[\d:]+Z?)?", r"\b\d{2}:\d{2}:\d{2}Z",
         r"(?<=, )(?:19|20)\d\d[a-z]?(?=[;),])", r"(?<=\()(?:19|20)\d\d[a-z]?(?=\))", REFS, r"(?m)^\s*\d+\.\s"]
NUM = re.compile(r"(?<![A-Za-z0-9_.,/§])(?<![A-Za-z][-–])[+\-−]?\d+(?:,\d{3})*(?:\.\d+)?%?(?![A-Za-z0-9_])")

args = sys.argv[1:]
write = "--write" in args
ruling = args[args.index("--ruling") + 1] if "--ruling" in args else None
R = pathlib.Path(args[args.index("--repo") + 1] if "--repo" in args else "/mnt/d/vsps_papers/vsps-paperB-lre")
assert not write or ruling, "--write needs --ruling <id of the GO ruling>"
sha = lambda b: hashlib.sha256(b).hexdigest()
pinned = {}
for name, pin in PINS.items():
    pinned[name] = (DIR / name).read_bytes()
    assert sha(pinned[name]) == pin, "pin differs: " + name
text, build_sh, man_new, src_new = (pinned[n].decode("utf-8") for n in PINS)
run = lambda *a: subprocess.run(["git", "-C", str(R), *a], capture_output=True)
git = lambda *a: subprocess.run(["git", "-C", str(R), *a], capture_output=True, check=True).stdout
assert run("merge-base", "--is-ancestor", BASE_COMMIT, "HEAD").returncode == 0, BASE_COMMIT + " is not HEAD or an ancestor of HEAD"
assert git("status", "--porcelain", "--", "paper") == b"", "paper/ tree not clean"
head_cache = {}


def head(f):
    if f not in head_cache:
        head_cache[f] = git("show", "HEAD:" + f).decode("utf-8")
    return head_cache[f]


for f, h in BASE.items():
    assert sha(head(f).encode("utf-8")) == h, "base sha differs: " + f
assert run("cat-file", "-e", "HEAD:" + NEW_FILE).returncode != 0, NEW_FILE + " exists at HEAD"
print("HEAD", git("rev-parse", "--short", "HEAD").decode().strip(), "| base", BASE_COMMIT, "is HEAD or an ancestor | SKIP", SKIP)

printed = lambda t: re.sub(r"<!--.*?-->", "", t, flags=re.S)
flat = lambda t: re.sub(r"\s+", " ", printed(t))


def numbers(t):
    t = re.sub(r"(\d)(?:st|nd|rd|th)\b", r"\1", t)
    for pat in STRIP:
        t = re.sub(pat, " ", t, flags=re.S)
    return collections.Counter(NUM.findall(t))


# blocks
blocks = re.findall(r"<<<(B1-[A-Z]\d+) (\S+) OLD>>>\n(.*?)\n<<<\1 \2 NEW>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", text, flags=re.S)
assert len(blocks) == N_BLOCKS and len({b[0] for b in blocks}) == N_BLOCKS, len(blocks)
files, done = {}, []
for bid, name, old, new in blocks:
    if bid in SKIP:
        continue
    f = REL + name
    assert f in BASE and f not in NOT_WRITTEN, (bid, f)
    s = files.setdefault(f, head(f))
    assert head(f).count(old) == 1 and s.count(old) == 1 and head(f).replace(old, "").count(new) == 0, (bid, head(f).count(old), s.count(old))
    added = printed(new).replace(printed(old), "") if printed(old) in printed(new) else printed(new)
    assert not AI_WORDS.search(added), bid + ": wording on AI tools"
    assert not FORBIDDEN_NEW.search(new), bid + ": " + FORBIDDEN_NEW.search(new).group(0)
    t = s.replace(old, new)
    assert (printed(t) == printed(s)) == (bid in COMMENT_ONLY), bid + ": printed text"
    files[f] = t
    done.append(bid)
print("blocks applied: %d of %d (each OLD once at HEAD; no NEW at HEAD outside its OLD)" % (len(done), N_BLOCKS))

# R1: pointers of the moved old text (Online Resource 2, the @OLD regions only; comments untouched)
f_res = REL + "online_resource.md"
if "R1" not in SKIP:
    out, inside, n_all, n_lines = [], False, 0, 0
    for line in files.get(f_res, head(f_res)).split("\n"):
        if line.startswith("<!-- @OLD "):
            inside = True
        elif line.startswith("<!-- @OLDEND"):
            inside = False
        elif inside:
            parts, n = re.split(r"(<!--.*?-->)", line), 0
            for i in range(0, len(parts), 2):
                for pat, rep in R1:
                    parts[i], k = re.subn(pat, rep, parts[i])
                    n += k
            if n:
                line, n_all, n_lines = "".join(parts) + R1_NOTE % n, n_all + n, n_lines + 1
        out.append(line)
    assert (n_all, n_lines) == (R1_N, R1_LINES), (n_all, n_lines)
    files[f_res] = "\n".join(out)
    left = re.findall(r"Supplement(?:ary)?(?: Table)? S\d", printed(files[f_res]))
    assert not left, left
    print("R1: %d pointers renamed in %d paragraphs of the moved old text, each marked EDITED; none left" % (n_all, n_lines))

# C2: the first author's ORCID link, copied from the title page of the earlier version (not typed anywhere here)
f_cl = REL + "cover_letter.md"
if "C2" not in SKIP and "B1-C02" not in SKIP:
    link = ORCID.findall(printed(head("paper/title_page_B.md")))
    assert len(link) == 1 and files[f_cl].count(C2_TOKEN) == 1, (len(link), files[f_cl].count(C2_TOKEN))
    files[f_cl] = files[f_cl].replace(C2_TOKEN, link[0])
    print("C2: one ORCID link copied from paper/title_page_B.md into the cover letter")
assert all(C2_TOKEN not in s for s in files.values()), "the ORCID token is still in a file: skip B1-C02 together with C2"

# X1: internal ids inside ruled sentences (NOT applied unless a ruling narrows CC-418 S3 and S11 for them)
f_pap = REL + "paper.md"
if "X1" not in SKIP:
    s, r = files.get(f_pap, head(f_pap)), files.get(f_res, head(f_res))
    assert printed(s).count(X1_OLD) == X1_N == s.count(X1_OLD) and r.count(X1_RES_OLD) == 1
    files[f_pap], files[f_res] = s.replace(X1_OLD, X1_NEW), r.replace(X1_RES_OLD, X1_RES_NEW)
    print("X1: %d line references of the registration and one ruling id replaced inside ruled sentences" % X1_N)

# ruled sentences, numbers, clauses
both = lambda get: flat(get(f_pap)) + " " + flat(get(f_res))
now = lambda f: files.get(f, head(f))
for sentence, n in RULED:
    assert both(head).count(sentence) == n, ("ruled sentence count at HEAD", sentence[:50], both(head).count(sentence))
    assert both(now).count(sentence) == n, ("ruled sentence changed", sentence[:50])
s3 = "`f0` remains the default for reporting " + (X1_OLD if "X1" in SKIP else X1_NEW) + "; the human arm, at low inter-rater agreement"
assert both(now).count(s3) == 3, "sentence S3"
for f in [k for k in BASE if k.endswith(".md") and k not in NOT_WRITTEN]:
    assert numbers(head(f)) == numbers(now(f)), (f, numbers(now(f)) - numbers(head(f)), numbers(head(f)) - numbers(now(f)))
    d = len(CLAUSE.findall(printed(now(f)))) - len(CLAUSE.findall(printed(head(f))))
    assert d == (1 if f == f_pap and "B1-D03" in done else 0), (f, "agreement clauses", d)
    assert "HELD from the PI" not in now(f)
print("ruled sentences: %d texts, each as often as at HEAD; numbers of the reader-visible text: none added, none removed, "
      "in each of the four text files; agreement clauses: +%d (block B1-D03)" % (len(RULED) + 1, int("B1-D03" in done)))

# S1: the two side files that the draft's checker generates from the annotations (pinned copies of this folder)
if "S1" not in SKIP:
    for f, new in ((REL + "number_manifest_B_v2.tsv", man_new), (REL + "PARAGRAPH_SOURCES.tsv", src_new)):
        assert new.split("\n", 1)[0] == head(f).split("\n", 1)[0], f + ": first line"
        if new != head(f):
            files[f] = new
    old_m, new_m = (set(x.split("\n")) for x in (head(REL + "number_manifest_B_v2.tsv"), man_new))
    print("S1: manifest rows %d -> %d (rows that differ: %d); paragraph sources %d -> %d lines" % (
        len(old_m), len(new_m), len(old_m ^ new_m), head(REL + "PARAGRAPH_SOURCES.tsv").count("\n"), src_new.count("\n")))

# N1: the sums file of the folder
if "N1" not in SKIP:
    lines = [sha(now(REL + n).encode("utf-8")) + "  " + n if REL + n in BASE else None for n in SNAPSHOT_ORDER]
    old_lines = head(REL + "SNAPSHOT.sha256").split("\n")
    assert len(old_lines) == len(SNAPSHOT_ORDER) + 1 and [l[66:] for l in old_lines[:-1]] == SNAPSHOT_ORDER
    files[REL + "SNAPSHOT.sha256"] = "\n".join(l or o for l, o in zip(lines, old_lines)) + "\n"

# B1: the new build script
if "B1" not in SKIP:
    dest = R / NEW_FILE
    assert not dest.exists() or dest.read_text(encoding="utf-8") == build_sh, NEW_FILE + " exists with other bytes"
    files[NEW_FILE] = build_sh

assert not set(files) & NOT_WRITTEN and set(files) <= set(BASE) | {NEW_FILE}, sorted(files)
target = dict(TARGETS, **({} if "X1" in SKIP else TARGETS_X1))
got = {f: sha(s.encode("utf-8")) for f, s in sorted(files.items())}
for f, h in got.items():
    print("OK   " if target.get(f) == h else "DIFF ", f, h)
same = got == target
print("ALL RESULTS EQUAL TARGETS" if same else "RESULTS DIFFER FROM TARGETS (TARGETS hold for SKIP = ('X1',) and, with TARGETS_X1, for SKIP = ())")
if write:
    assert same, "no file written: results differ from TARGETS"
    for f, s in files.items():
        (R / f).write_bytes(s.encode("utf-8"))
    print("WRITTEN under ruling %s: %d files to the working tree of the paper repository (not staged, not committed)" % (ruling, len(files)))
else:
    print("CHECK MODE: nothing written")
