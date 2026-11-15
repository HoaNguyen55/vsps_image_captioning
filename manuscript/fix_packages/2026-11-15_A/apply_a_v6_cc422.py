#!/usr/bin/env python3
"""Paper A fix package v6 (A_FIX_PACKAGE_v6.md): rebuild the changed files in memory and, only on request, write them.

Source of the items: readiness audit manuscript/READY_AUDIT_A_2026-11-15.md (sha256 500de478...).
Blocks (OLD/NEW pairs of the package): group N (two unprinted source comments), group F (build filter: figure
captions, breaks in DOIs printed as text), group H (revision-history wording of Supplementary S1-S10), group L
(two labels of Section 9.1 glossed), group D (heading of the declarations).
Steps that are not blocks: S1 manifest rows; R1 reference list appended to the supplement; B1 new build script;
T1 the abstract made to stand alone (three patterns); V1 the abstract's sentence on the registered predictions
copied into the cover letter; S2 published supplement and provenance table from scrub(); S3 length comment.

Default mode: CHECK ONLY. Nothing is written. The script
  1. checks the pins (package, reference list, build script), that BASE_COMMIT is HEAD or an ancestor of HEAD, a
     clean paper/ tree, and that every file it reads has its sha256 of BASE_COMMIT;
  2. applies each block to `git show HEAD:paper/<file>` (OLD exactly once at HEAD, NEW absent), then the steps;
  3. asserts the custody zones: sec7_verbosity_sign.md (Section 6.7), highlights_A.md and the title page are not
     written; the bytes of Supplementary S11 stand unchanged in both supplement files; every supplement block lies
     before S11; the abstract body changes only by the three patterns of T1 and gains no number; no run of 8
     words from Section 6.7, S11, the abstract body or the highlights occurs in the package, its two files or
     this script;
  4. asserts that the count of printed agreement clauses is unchanged in every file, that no block adds wording
     on AI tools, and that the registration ledger row of Section 1.2 is untouched (sec1 is not written);
  5. prints the sha256 of every resulting file and compares it with TARGETS.

Write mode:  python3 -I -B apply_a_v6.py --write --ruling CC-xxx
  writes the files to the working tree only if every result equals TARGETS. TARGETS hold only for SKIP = ();
  if the ruling drops a block or a step, set SKIP and replace TARGETS by the values the ruling fixes.
  Never runs git add or git commit.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = pathlib.Path("/mnt/d/vsps_image_captioning")
DIR = HERE / "manuscript/fix_packages/2026-11-15_A"
PINS = {
    "A_FIX_PACKAGE_v6.md": "df8d66260d1ac5bf997c3adc8e2aed46f35024521fb988b0f1295fc9fdf3077f",
    "SUPP_REFERENCES_A_v6.md": "147aa1e9204528c022c2763d8cb497c962a3d47a8a6d22f81ecaf5c1bdee0381",
    "build_A_supp.sh": "e3a4cab2a1d4a5d23facaf8812498c70e536d99ac5386e1a8abb8c1da09183f4",
}
R = pathlib.Path("/mnt/d/vsps_papers/vsps-paperA-spic")
BASE_COMMIT = "0b542cf"
SKIP = ("V1",)  # block ids (e.g. "A6-H05") or steps ("S1", "R1", "B1", "T1", "V1", "S3") the ruling does not apply
BASE = {
    "abstract_A.md": "b566eb8e8f4ca29d9ccc5383c987aca53bd54678cddd414e68836d81c7c29752",
    "anon/declarations_anon.md": "e407d32ddd13b2903482472e35cf011e71177ea23f271425e9e38f60ee5172ca",
    "build/filter.lua": "7ce939e753ec1913f53c67543c0fbebee7420d3558e945bde9be7e0d88e5063a",
    "cover_letter_A.md": "7c14bb274f6e50c47abdbaceeebacad22da86d52043ac731dbac6835b8737957",
    "declarations.md": "3b2381ca23d22682dd431dfed5c7a738c2ae41bf55356fa5291b23c6a598b5d2",
    "highlights_A.md": "64c671615bd5106cba42cf168ff7ff85460bd9bd72b3c52a2d9903861c281aa5",
    "number_manifest.tsv": "dd2bce1797bb5bbe52da2d832750038bbfc7f2d39c10d99fe6eacb9de9b716c8",
    "sec5_exchangeability.md": "280b0e87e80d387df432515d392d50400a39c798581ad8b2e25c5ce52883a8fd",
    "sec7_verbosity_sign.md": "b6f46b8aaf33ef133b54e5e4d91f2c1f037e061d48f495e1b23eed5b0aaf4817",
    "sec11_limitations_ethics.md": "dff441d598ae945c459dfbc348d2dd51e2a8c2a2621a62a781c0d6836d74a34f",
    "supplementary.md": "dd7277069ced9d4d66c2b57e933d06a9b05cc41aae546b5cefa0c10ddcccc2ee",
    "supplementary_SPIC.md": "0c746c2127cac8bcb25340172e3859cc3c023d4739e7e8d812967287e554f280",
    "supplementary_provenance_internal.tsv": "1162582f16633e11d26d9d1a72fd20a3b04389a51453c3e1e8c2605068002a07",
}
NOT_WRITTEN = {"sec7_verbosity_sign.md", "highlights_A.md", "title_page_A.md", "sec1_introduction.md", "anon/declarations_anon.md"}
WRITABLE = set(BASE) - NOT_WRITTEN | {"build/build_A_supp.sh"}
COMMENT_ONLY = {"A6-N01", "A6-N02"}
N_BLOCKS = 53
TARGETS = {
    "abstract_A.md": "91e9802c81a7807051a0862a9b13bd47598c5a11b7e5d7031c792cf63fab967f",
    "build/build_A_supp.sh": "e3a4cab2a1d4a5d23facaf8812498c70e536d99ac5386e1a8abb8c1da09183f4",
    "build/filter.lua": "89e187af95d4f70ba617eb9c7c488b9b70a78f0bc0e26cca7a64fb5833840108",
    "declarations.md": "69ceb15e18535fca9e50664b8b0dd20e4ec421739a827fc4c70f7f54f85e5906",
    "number_manifest.tsv": "f5d517cc56df8302fd43996f677bbead29f6fd0bfd95029b08620cc83de91b07",
    "sec11_limitations_ethics.md": "bb7ff51c373bc4427639fec39b7826b170eb7e2a0969322a25884aacca3ad3b3",
    "sec5_exchangeability.md": "9167bd8ce84bf8ef6e8ed65ba2e93abde128328d3daf8f289e910f0097dcfa27",
    "supplementary.md": "67d36d9583e7b032c74d2a91529782af056e2ec077fccf373f35b1ed36d5b88d",
    "supplementary_SPIC.md": "68b1dfab60d90610e35014d49080fb1ca45a4eab71b6bea8773f3c5b27f85026",
    "supplementary_provenance_internal.tsv": "1fcc915f39f77aa287429766402ccd4c335ebbcb102eda6d4fa69e282d437d62",
}
MAIN = ["sec1_introduction.md", "sec2_related_work.md", "sec3_measurement_setup.md", "sec4_theory.md", "sec5_exchangeability.md",
        "sec6_rescoring_published_methods.md", "sec7_verbosity_sign.md", "sec8_human_validity.md", "sec9_preference_audit.md",
        "sec10_discussion.md", "sec11_limitations_ethics.md", "declarations.md"]
S11 = "\n## S11 "
CLAUSE = "agreed to this use"
AI_WORDS = re.compile(r"\bAI\b|artificial intelligence|generative|ChatGPT|GPT-|Claude|Gemini|Copilot|writing assistant|language tool")
HISTORY = re.compile(r"revision \d|[Pp]re-revision|[Mm]oved from|Material moved|old Section|^#+ From Section", re.M)
# T1: the three patterns on the printed text of the abstract paragraph; (pattern, replacement, expected matches)
T1 = [(r" \((?:H\d[a-z]?, )*H\d[a-z]?\)", "", 3),
      (r"\(H\d[a-z]? [A-Z_]+; single annotator; Section 6\.7(?:\.\d+)?\)", "(single annotator)", 1),
      (r"\bfour LVLMs\b", "four large vision-language models", 1)]
T1_NOTE = ("<!-- fix package v6 (audit A5-02): the section pointer and the eight hypothesis codes removed, LVLMs written out; "
           "no number added; %d words, comments stripped -->")
# V1: the sentence of the abstract that the cover letter gains, found by its first and last words
V1_SPAN = r"Of seven predictions.*?was not validated\."
V1_ANCHOR = "rest on one verbose system (both post hoc). "
V1_NOTE = ("<!-- fix package v6 (audit A4-02): the sentence before this comment is the abstract's sentence on the seven "
           "predictions and the certificate, copied from abstract_A.md by script -->")

args = sys.argv[1:]
write = "--write" in args
ruling = args[args.index("--ruling") + 1] if "--ruling" in args else None
assert not write or ruling, "--write needs --ruling <id of the GO ruling>"
sha = lambda b: hashlib.sha256(b).hexdigest()
pinned = {}
for name, pin in PINS.items():
    pinned[name] = (DIR / name).read_bytes()
    assert sha(pinned[name]) == pin, "pin differs: " + name
text, refs, build_sh = (pinned[n].decode() for n in PINS)
run = lambda *a: subprocess.run(["git", "-C", str(R), *a], capture_output=True)
git = lambda *a: subprocess.run(["git", "-C", str(R), *a], capture_output=True, check=True).stdout
assert run("merge-base", "--is-ancestor", BASE_COMMIT, "HEAD").returncode == 0, BASE_COMMIT + " is not HEAD or an ancestor of HEAD"
assert git("status", "--porcelain", "--", "paper") == b"", "paper/ tree not clean"
head_cache = {}


def head(f):
    if f not in head_cache:
        head_cache[f] = git("show", "HEAD:paper/" + f).decode()
    return head_cache[f]


for f, h in BASE.items():
    assert sha(head(f).encode()) == h, "base sha differs: " + f
print("HEAD", git("rev-parse", "--short", "HEAD").decode().strip(), "| base", BASE_COMMIT, "is HEAD or an ancestor | SKIP", SKIP)

printed = lambda t: re.sub(r"<!--.*?-->", "", t, flags=re.S)
words = lambda t: len(printed(t).split())
sys.path.insert(0, str(R / "paper/build"))
from scrub_supp import scrub, LEAK  # noqa: E402  (the functions only; the script is not run)

# blocks
blocks = re.findall(r"<<<(A6-[NFHLD]\d+) (\S+) OLD>>>\n(.*?)\n<<<\1 \2 NEW>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", text, flags=re.S)
assert len(blocks) == N_BLOCKS and len({b[0] for b in blocks}) == N_BLOCKS, len(blocks)
files, done = {}, []
for bid, f, old, new in blocks:
    if bid in SKIP:
        continue
    assert f in WRITABLE, (bid, f)
    s = files.setdefault(f, head(f))
    assert head(f).count(old) == 1 and s.count(old) == 1 and head(f).replace(old, "").count(new) == 0, (bid, head(f).count(old), s.count(old))
    assert not AI_WORDS.search(printed(new)), bid + ": wording on AI tools"
    if f == "supplementary.md":
        assert s.index(old) + len(old) < s.index(S11), bid + ": block inside S11"
    t = s.replace(old, new)
    assert (printed(t) == printed(s)) == (bid in COMMENT_ONLY), bid + ": printed text"
    files[f] = t
    done.append(bid)
print("blocks applied: %d of %d (each OLD once at HEAD; no NEW at HEAD outside its OLD)" % (len(done), N_BLOCKS))

# S1: manifest rows
if "S1" not in SKIP:
    rows = re.search(r"\*\*S1\. .*?\n```\n(.*?)\n```\n", text, flags=re.S).group(1).split("\n")
    man = head("number_manifest.tsv")
    assert man.endswith("\n") and len(rows) == 34
    for r in rows:
        c = r.split("\t")
        assert len(c) == 6 and c[1] == "A" and r + "\n" not in man, r[:60]
        assert sha((HERE / c[2]).read_bytes())[:12] == c[4], "source sha differs: " + c[2]
    files["number_manifest.tsv"] = man + "\n".join(rows) + "\n"
    print("S1: %d manifest rows; the sha256 prefix of each source file equals the file in the run repository" % len(rows))

# R1: reference list after the last line of the supplement (S11 bytes stay where they are)
src0 = head("supplementary.md")
zone = src0[src0.index(S11):]
src = files.get("supplementary.md", src0)
assert src.endswith(zone) and src0.endswith("\n") and not src0.endswith("\n\n")
if "R1" not in SKIP:
    assert refs.startswith("## References for the Supplementary Material\n") and "## References" not in src0 and not LEAK.search(refs)
    src = src + "\n" + refs
    files["supplementary.md"] = src
    print("R1: reference list appended, %d entries" % (refs.count("\n\n") - 1))

# S2: published supplement and provenance table
out0, prov0 = scrub(src0)
assert out0 == head("supplementary_SPIC.md"), "scrub(supplementary.md) != supplementary_SPIC.md at HEAD"
zone_spic = out0[out0.index(S11):]
if "supplementary.md" in files:
    out, prov = scrub(src)
    files["supplementary_SPIC.md"] = out
    files["supplementary_provenance_internal.tsv"] = ("comment_no\tsrc_line\theading\tvisible_text_before\tcomment\n"
                                                      + "".join("\t".join(r) + "\n" for r in prov))
    a, b = out.index(S11), out.index(S11) + len(zone_spic)
    assert src.count(zone) == 1 and out.count(zone_spic) == 1, "S11 bytes changed"
    assert all(a < m.start() < b for m in LEAK.finditer(out)), "leak hit outside S11"
    left = HISTORY.findall(out[:a])
    assert not left or any(x.startswith("A6-H") for x in SKIP), left
    print("S2: published supplement = scrub(source); S11 bytes unchanged in both files; leak hits only inside S11; "
          "revision-history wording left in S1-S10: %d" % len(left))

# T1: the abstract stands alone
ab0 = head("abstract_A.md")
cut = ab0.index("## Abstract")
body = ab0[cut:]
para = lambda b: next(l for l in b.split("\n")[1:] if l.strip())
if "T1" not in SKIP:
    line = para(body)
    k = line.index("<!--")
    vis = line[:k]
    assert printed(line) == vis and body.count(line) == 1
    for pat, rep, n in T1:
        assert len(re.findall(pat, vis)) == n, (pat, len(re.findall(pat, vis)))
        vis = re.sub(pat, rep, vis)
    body = body.replace(line, vis + T1_NOTE % len(vis.split()) + line[k:])
    nums = lambda t: sorted(re.findall(r"\d[\d.,]*", printed(t)))
    gone = list(nums(ab0[cut:]))
    for x in nums(body):
        gone.remove(x)  # raises if the new body prints a number the old body does not
    assert words(para(body)) <= 250 and not AI_WORDS.search(printed(body))
    print("T1: abstract %d -> %d words; numbers printed: %d -> %d, none added (the %d dropped are digits of codes and of the section pointer)"
          % (words(para(ab0[cut:])), words(para(body)), len(nums(ab0[cut:])), len(nums(body)), len(gone)))

# V1: the cover letter gains the abstract's sentence on the registered predictions
if "V1" not in SKIP:
    span = re.findall(V1_SPAN, printed(body))
    cl = head("cover_letter_A.md")
    assert len(span) == 1 and cl.count(V1_ANCHOR) == 1 and span[0] not in cl
    files["cover_letter_A.md"] = cl.replace(V1_ANCHOR, V1_ANCHOR + span[0] + V1_NOTE + " ")
    assert printed(files["cover_letter_A.md"]) == printed(cl).replace(V1_ANCHOR, V1_ANCHOR + span[0] + " ")
    print("V1: cover letter gains one sentence of %d words, equal to the abstract's" % len(span[0].split()))

# S3: counts of the length comment of abstract_A.md (before "## Abstract")
c0 = {f: words(head(f)) for f in MAIN}
c1 = {f: words(files.get(f, head(f))) for f in MAIN}
t0, t1 = sum(c0.values()), sum(c1.values())
longest = lambda c: "Longest files: " + "; ".join("%s %s" % (f, format(n, ",")) for f, n in sorted(c.items(), key=lambda x: -x[1])[:3]) + "."
print("main text words:", t0, "->", t1, {f: c1[f] - c0[f] for f in MAIN if c1[f] != c0[f]})
top = ab0[:cut]
if "S3" not in SKIP:
    for a, b in [
        ("recounted after fix package v5 of 2026-11-15).",
         "recounted after fix package v5 of 2026-11-15; recounted after fix package v6 of 2026-11-15)."),
        ("Main text now: %s words" % format(t0, ","), "Main text now: %s words" % format(t1, ",")),
        ("Over the limit by %s words." % format(t0 - 8500, ","), "Over the limit by %s words." % format(t1 - 8500, ",")),
        ("Abstract: %d words" % words(para(ab0[cut:])), "Abstract: %d words" % words(para(body))),
        (longest(c0), longest(c1)),
    ]:
        assert top.count(a) == 1, a
        top = top.replace(a, b)
if top + body != ab0:
    files["abstract_A.md"] = top + body

# B1: the new build script
dest = R / "paper/build/build_A_supp.sh"
if "B1" not in SKIP:
    assert not dest.exists() or dest.read_text() == build_sh, "build_A_supp.sh exists with other bytes"
    files["build/build_A_supp.sh"] = build_sh

# custody zones and standing rules
assert set(files) <= WRITABLE and not set(files) & NOT_WRITTEN, sorted(set(files) - WRITABLE)
tail = lambda s, mark: s[s.index(mark):]
held = " ".join([tail(head("sec7_verbosity_sign.md"), "\n## 6.7"), zone, zone_spic, tail(ab0, "## Abstract"), head("highlights_A.md")])
grams = lambda t: {" ".join(w[i:i + 8]) for w in [re.findall(r"\w+", t.lower())] for i in range(len(w) - 7)}
ours = grams(text) | grams(refs) | grams(build_sh) | grams(pathlib.Path(__file__).read_text(encoding="utf-8"))
hits = len(grams(held) & ours)
assert hits == 0, "%d runs of 8 words of a held zone occur in the package, its files or the script" % hits
for f in sorted(set(BASE) - {"number_manifest.tsv", "supplementary_provenance_internal.tsv", "build/filter.lua"}):
    n0, n1 = printed(head(f)).count(CLAUSE), printed(files.get(f, head(f))).count(CLAUSE)
    assert n0 == n1, f + ": agreement clauses %d -> %d" % (n0, n1)
print("custody: Section 6.7 file, highlights, title page, Section 1 and the anonymised declarations not written; S11 bytes unchanged; "
      "0 shared runs of 8 words with Section 6.7, S11, the abstract body, the highlights; agreement clauses unchanged in every file")

got = {f: sha(s.encode()) for f, s in sorted(files.items())}
for f, h in got.items():
    print("OK   " if TARGETS.get(f) == h else "DIFF ", f, h)
same = got == TARGETS
print("ALL RESULTS EQUAL TARGETS" if same else "RESULTS DIFFER FROM TARGETS (with SKIP set, the targets are those of the ruling)")
if write:
    assert same, "no file written: results differ from TARGETS"
    for f, s in files.items():
        (R / "paper" / f).write_bytes(s.encode())
    print("WRITTEN under ruling %s: %d files to the working tree of the paper repository (not staged, not committed)" % (ruling, len(files)))
else:
    print("CHECK MODE: nothing written")
