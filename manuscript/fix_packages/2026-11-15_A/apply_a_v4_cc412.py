#!/usr/bin/env python3
"""Paper A fix package v4 (A_FIX_PACKAGE_v4.md): rebuild the changed files in memory and, only on request, write them.

Groups: C (claim wording), N (CC-407 N1, N2, N4, N9), U (UIT-ViIC training statement; NEEDS THE INVESTIGATOR).
  --groups C,N      which groups to apply (default C,N); any non-empty subset of C,N,U

Default mode: CHECK ONLY. Nothing is written. The script
  1. checks the pin of the package file, that BASE_COMMIT is an ancestor of the paper HEAD, a clean paper/ tree, and that
     every file it can change still has its sha256 of BASE_COMMIT (so a later commit that leaves these files alone is fine);
  2. reads the OLD/NEW blocks of the chosen groups from the package and applies them in the order of the package to
     `git show HEAD:paper/<file>` (each OLD exactly once), skipping the ids in SKIP;
  3. runs the steps that are not blocks: S1 two manifest rows (group U only), S2 the provenance table from scrub()'s
     rows (when supplementary.md changes), S3 the length block of abstract_A.md;
  4. asserts scrub(supplementary.md) == supplementary_SPIC.md byte for byte and no leak hit outside S11
     (scrub() is imported; scrub_supp.py is NOT run);
  5. asserts the custody zones are byte-unchanged: S11 to the end of both supplement files, sec7_verbosity_sign.md from
     "## 6.7" to its end, abstract_A.md from "## Abstract"; highlights, cover letter, title page and Section 2 are not written;
  6. prints the sha256 of every resulting file and compares it with TARGETS for the chosen groups.

Write mode:  python3 -I -B apply_a_v4.py --groups C,N --write --ruling CC-xxx
  writes the files to the working tree only if every result equals TARGETS. Group U is written only with
  --pi-decision <LOG id of the investigator's decision> in addition. TARGETS are the package writer's own values
  (Section 7.3 of the package) and hold only for SKIP = (); if the ruling drops or changes a block, set SKIP and
  replace TARGETS[<groups>] by the sha256 values the ruling fixes. Never runs git add or git commit.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

sys.dont_write_bytecode = True
PKG = pathlib.Path("/mnt/d/vsps_image_captioning/manuscript/fix_packages/2026-11-15_A/A_FIX_PACKAGE_v4.md")
PKG_SHA256 = "53ebce0260bc39c3341c1d108392277b1b4b187236d1300f884db1cc1429c390"
R = "/mnt/d/vsps_papers/vsps-paperA-spic"
BASE_COMMIT = "ea12e51"
SKIP = ("A4-C04",)  # CC-412 Ruling 3 and Ruling 7 (coordinator copy)
BASE = {
    "abstract_A.md": "0d249d7c484ef41dfa8b4afc22d3e8cea1f78e7aa97790421cabf2c99561edd4",
    "anon/declarations_anon.md": "066a325d31be854ffda7abba6f1aa46995c573fadfb904136f4e438471c473db",
    "declarations.md": "4149bb37b23fd250164af378ea189d119e437f20b0d0dfa8049ec43ec7506fb4",
    "number_manifest.tsv": "d3ca0672f389ebd1621a49de625aa3d926e3603f0f78d7e1ae6881b1b2b41c8b",
    "sec10_discussion.md": "77ceb4083d5c1e39206f8badfabaa8651f6a6a4fb4af7627579035fa04e76a54",
    "sec11_limitations_ethics.md": "eec0ec50fbe5159b08412b43f1171d5a5c5e22959841e7e68214f72ef835e4df",
    "sec1_introduction.md": "46b7534e1936ce4841d8c23b5baf09a6e4457e651917c5055ef872de2475c914",
    "sec3_measurement_setup.md": "bfc5c286c533b52d881899486ef1eef534dd43940d4028898adc98da9ae8bd8d",
    "sec7_verbosity_sign.md": "b6f46b8aaf33ef133b54e5e4d91f2c1f037e061d48f495e1b23eed5b0aaf4817",
    "supplementary.md": "eb1b65708c56a2dd1e89cfbde7ffe01152586fdc88a5a0a0dad3d5daa33bd882",
    "supplementary_SPIC.md": "a76c820f0bbcbe1e54957ebf10f542ab49cdb7bc83480a634bdcae919b265305",
    "supplementary_provenance_internal.tsv": "82b663b1d2106662c3d1e6a4e9025ecb94288053239de5d1cde40643a87c5998",
}
TARGETS = {
    "C+N": {
        "abstract_A.md": "a6df61d40a8d3dd6a35db743b34981b2167ef84977aba1f4e34f440ac1cd5ef9",
        "declarations.md": "8fb28692d32e3688d0694ae6c84353f63d8968032e53f9bdf3c6b933ffbe288b",
        "sec10_discussion.md": "d48ce382b275e73e3f6de34e08814f7c7205a51fb394d5742ed382f9e8e252bf",
        "sec11_limitations_ethics.md": "9ff1cd8ecb84b000a08ed9e3f7ab5dc4bef8d745376860fc937c7662ee3523b7",
        "sec1_introduction.md": "7d6267cd363ceb68ab00760119ff4034f489af81b82b9890a62a2e57e7730233",
        "sec3_measurement_setup.md": "665c60aa1956df8dedab070db395bd794297fec88cf07d7242c6bc7c31e74575",
        "supplementary.md": "0349454b2d0549051da9b64eccf2c12b0843ce51c75882927425dafb6d1ec927",
        "supplementary_provenance_internal.tsv": "1162582f16633e11d26d9d1a72fd20a3b04389a51453c3e1e8c2605068002a07",
    },
    "C+N+U": {
        "abstract_A.md": "4b83b95edda87eec1cfb219909d23d3440de842bf0eff0e4c1cda445ea50e214",
        "anon/declarations_anon.md": "ec71a9b953ab3609a31f457b8368814c35a82443035885cfa64d9d8df84a96cb",
        "declarations.md": "5920d0fa7461f0a75cd6aae6d58df7e7588111ba9ad39ff76e1aa3af4c4702ba",
        "number_manifest.tsv": "dd2bce1797bb5bbe52da2d832750038bbfc7f2d39c10d99fe6eacb9de9b716c8",
        "sec10_discussion.md": "d48ce382b275e73e3f6de34e08814f7c7205a51fb394d5742ed382f9e8e252bf",
        "sec11_limitations_ethics.md": "a7258f2eddb6e137d6abe6990063ce2cc8a4e8e57c9e6bddcef6161e54d2a1e4",
        "sec1_introduction.md": "7d6267cd363ceb68ab00760119ff4034f489af81b82b9890a62a2e57e7730233",
        "sec3_measurement_setup.md": "665c60aa1956df8dedab070db395bd794297fec88cf07d7242c6bc7c31e74575",
        "sec7_verbosity_sign.md": "0e344d32b21457d66572022f6ceb72b77c1188df70068f52c52a5c5505211cc1",
        "supplementary.md": "dd7277069ced9d4d66c2b57e933d06a9b05cc41aae546b5cefa0c10ddcccc2ee",
        "supplementary_SPIC.md": "0c746c2127cac8bcb25340172e3859cc3c023d4739e7e8d812967287e554f280",
        "supplementary_provenance_internal.tsv": "1162582f16633e11d26d9d1a72fd20a3b04389a51453c3e1e8c2605068002a07",
    },
    "C": {
        "abstract_A.md": "c7be9fb60405f35b8bc27e52d06ea8e4032ac0d91ae2f3c09a37219370f97a40",
        "sec10_discussion.md": "3a2ac0007c10daf050a784aff4db54570649460b3cfde026e5dd3b06864ad9c2",
        "sec1_introduction.md": "7d6267cd363ceb68ab00760119ff4034f489af81b82b9890a62a2e57e7730233",
        "sec7_verbosity_sign.md": "0e344d32b21457d66572022f6ceb72b77c1188df70068f52c52a5c5505211cc1",
    },
    "N": {
        "abstract_A.md": "20be01d754a70915348cd6d21a0d76e2ae18cce2519a763db09dc42ad28d94d4",
        "declarations.md": "8fb28692d32e3688d0694ae6c84353f63d8968032e53f9bdf3c6b933ffbe288b",
        "sec10_discussion.md": "76c94324d302ef36351e357269c2e6b2cbe1bce24a4ec29552f55f9149d88d62",
        "sec11_limitations_ethics.md": "9ff1cd8ecb84b000a08ed9e3f7ab5dc4bef8d745376860fc937c7662ee3523b7",
        "sec3_measurement_setup.md": "665c60aa1956df8dedab070db395bd794297fec88cf07d7242c6bc7c31e74575",
        "supplementary.md": "0349454b2d0549051da9b64eccf2c12b0843ce51c75882927425dafb6d1ec927",
        "supplementary_provenance_internal.tsv": "1162582f16633e11d26d9d1a72fd20a3b04389a51453c3e1e8c2605068002a07",
    },
    "U": {
        "abstract_A.md": "2ddd6bb3176c412efa0c054c1473847461bf02634524c5d7b4c2a6b38a2a4907",
        "anon/declarations_anon.md": "ec71a9b953ab3609a31f457b8368814c35a82443035885cfa64d9d8df84a96cb",
        "declarations.md": "336e29b0453f8185e1e5797c9a81e27c24967f705f5464f7de1a29925d37d504",
        "number_manifest.tsv": "dd2bce1797bb5bbe52da2d832750038bbfc7f2d39c10d99fe6eacb9de9b716c8",
        "sec11_limitations_ethics.md": "ad831dea733e47600ba6d22b90ac5097e00a4a332f78ee78ca32f496709bc4d9",
        "supplementary.md": "78d33c2c1f19dc4e1dcdc67c6869e31bc5de0df725089d281fb9dcbb58864b0b",
        "supplementary_SPIC.md": "0c746c2127cac8bcb25340172e3859cc3c023d4739e7e8d812967287e554f280",
        "supplementary_provenance_internal.tsv": "82b663b1d2106662c3d1e6a4e9025ecb94288053239de5d1cde40643a87c5998",
    },
    "C+U": {
        "abstract_A.md": "44f2a36c4a68111078c355c38ca6b346371b17550fcdde893600f5fb9cbb7abf",
        "anon/declarations_anon.md": "ec71a9b953ab3609a31f457b8368814c35a82443035885cfa64d9d8df84a96cb",
        "declarations.md": "336e29b0453f8185e1e5797c9a81e27c24967f705f5464f7de1a29925d37d504",
        "number_manifest.tsv": "dd2bce1797bb5bbe52da2d832750038bbfc7f2d39c10d99fe6eacb9de9b716c8",
        "sec10_discussion.md": "3a2ac0007c10daf050a784aff4db54570649460b3cfde026e5dd3b06864ad9c2",
        "sec11_limitations_ethics.md": "ad831dea733e47600ba6d22b90ac5097e00a4a332f78ee78ca32f496709bc4d9",
        "sec1_introduction.md": "7d6267cd363ceb68ab00760119ff4034f489af81b82b9890a62a2e57e7730233",
        "sec7_verbosity_sign.md": "0e344d32b21457d66572022f6ceb72b77c1188df70068f52c52a5c5505211cc1",
        "supplementary.md": "78d33c2c1f19dc4e1dcdc67c6869e31bc5de0df725089d281fb9dcbb58864b0b",
        "supplementary_SPIC.md": "0c746c2127cac8bcb25340172e3859cc3c023d4739e7e8d812967287e554f280",
        "supplementary_provenance_internal.tsv": "82b663b1d2106662c3d1e6a4e9025ecb94288053239de5d1cde40643a87c5998",
    },
    "N+U": {
        "abstract_A.md": "464e857b5a91374d799f1f286de352bb46adc2b1d227fe3e1ec5f3686a0640d7",
        "anon/declarations_anon.md": "ec71a9b953ab3609a31f457b8368814c35a82443035885cfa64d9d8df84a96cb",
        "declarations.md": "5920d0fa7461f0a75cd6aae6d58df7e7588111ba9ad39ff76e1aa3af4c4702ba",
        "number_manifest.tsv": "dd2bce1797bb5bbe52da2d832750038bbfc7f2d39c10d99fe6eacb9de9b716c8",
        "sec10_discussion.md": "76c94324d302ef36351e357269c2e6b2cbe1bce24a4ec29552f55f9149d88d62",
        "sec11_limitations_ethics.md": "a7258f2eddb6e137d6abe6990063ce2cc8a4e8e57c9e6bddcef6161e54d2a1e4",
        "sec3_measurement_setup.md": "665c60aa1956df8dedab070db395bd794297fec88cf07d7242c6bc7c31e74575",
        "supplementary.md": "dd7277069ced9d4d66c2b57e933d06a9b05cc41aae546b5cefa0c10ddcccc2ee",
        "supplementary_SPIC.md": "0c746c2127cac8bcb25340172e3859cc3c023d4739e7e8d812967287e554f280",
        "supplementary_provenance_internal.tsv": "1162582f16633e11d26d9d1a72fd20a3b04389a51453c3e1e8c2605068002a07",
    },
}

args = sys.argv[1:]
opt = lambda name: args[args.index(name) + 1] if name in args else None
write, ruling, pi = "--write" in args, opt("--ruling"), opt("--pi-decision")
groups = sorted(set((opt("--groups") or "C,N").split(",")))
assert groups and set(groups) <= set("CNU"), "--groups takes a non-empty subset of C,N,U"
assert not write or ruling, "--write needs --ruling <id of the GO ruling>"
assert not (write and "U" in groups) or pi, "group U NEEDS THE INVESTIGATOR: --write with U needs --pi-decision <LOG id>"
assert ("A4-C02" in SKIP) == ("A4-C03" in SKIP), "A4-C02 and A4-C03 go together"
for p in ("A4-U04", "A4-U05"):
    assert (p + "a" in SKIP) == (p + "b" in SKIP), p + ": both supplement files or neither"

pkg = PKG.read_bytes()
assert hashlib.sha256(pkg).hexdigest() == PKG_SHA256, "package pin"
run = lambda *a: subprocess.run(["git", "-C", R, *a], capture_output=True)
git = lambda *a: subprocess.run(["git", "-C", R, *a], capture_output=True, check=True).stdout
assert run("merge-base", "--is-ancestor", BASE_COMMIT, "HEAD").returncode == 0, BASE_COMMIT + " is not an ancestor of HEAD"
assert git("status", "--porcelain", "--", "paper") == b"", "paper/ tree not clean"
head = lambda f: git("show", "HEAD:paper/" + f).decode()
for f, h in BASE.items():
    assert hashlib.sha256(head(f).encode()).hexdigest() == h, "base sha differs: " + f
print("HEAD", git("rev-parse", "--short", "HEAD").decode().strip(), "| base", BASE_COMMIT, "is an ancestor | groups", "+".join(groups),
      "| SKIP", SKIP)

sys.path.insert(0, R + "/paper/build")
from scrub_supp import scrub, LEAK  # noqa: E402  (the function only; the script is not run)

text = pkg.decode()
blocks = re.findall(r"<<<(A4-([CUN])\d+[a-f]?) (\S+) OLD>>>\n(.*?)\n<<<\1 \3 NEW>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", text, flags=re.S)
assert len(blocks) == 21 and len({b[0] for b in blocks}) == 21, len(blocks)
files, done = {}, []
for bid, g, f, old, new in blocks:
    if g not in groups or bid in SKIP:
        continue
    s = files.setdefault(f, head(f))
    assert head(f).count(old) == 1 and s.count(old) == 1, (bid, head(f).count(old), s.count(old))
    files[f] = s.replace(old, new)
    done.append(bid)
print("blocks applied:", done)

# S1: manifest rows (group U prints one number that is new to the paper)
if "U" in groups and "S1" not in SKIP:
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
assert all(m.start() > out.index("\n## S11 ") for m in LEAK.finditer(out)), "leak hit outside S11"
print("BYTE-EQUAL scrub(source) == journal supplement; leak hits, all inside S11, at lines",
      sorted({out.count("\n", 0, m.start()) + 1 for m in LEAK.finditer(out)}))
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
longest = lambda c: "Longest files: " + "; ".join("%s %s" % (f, format(n, ",")) for f, n in sorted(c.items(), key=lambda x: -x[1])[:3]) + "."
print("main text words:", t0, "->", t1)
if "S3" not in SKIP:
    ab = head("abstract_A.md")
    for a, b in [
        ("recounted after fix package v2 of 2026-11-15).",
         "recounted after fix package v2 of 2026-11-15; recounted after fix package v4 of 2026-11-15)."),
        ("Main text now: %s words" % format(t0, ","), "Main text now: %s words" % format(t1, ",")),
        ("Over the limit by %s words." % format(t0 - 8500, ","), "Over the limit by %s words." % format(t1 - 8500, ",")),
        (longest(c0), longest(c1)),
    ]:
        assert ab.count(a) == 1, a
        ab = ab.replace(a, b)
    files["abstract_A.md"] = ab

# custody zones
tail = lambda s, mark: s[s.index(mark):]
for f in ("supplementary.md", "supplementary_SPIC.md"):
    assert tail(files.get(f, head(f)), "\n## S11 ") == tail(head(f), "\n## S11 "), f
assert tail(files.get("sec7_verbosity_sign.md", head("sec7_verbosity_sign.md")), "\n## 6.7") == tail(head("sec7_verbosity_sign.md"), "\n## 6.7")
assert tail(files.get("abstract_A.md", head("abstract_A.md")), "## Abstract") == tail(head("abstract_A.md"), "## Abstract")
assert not {"highlights_A.md", "cover_letter_A.md", "title_page_A.md", "sec2_related_work.md"} & set(files)
assert set(files) <= set(BASE), "a file outside the base table"
print("custody zones unchanged: S11 (both supplement files), Section 6.7, abstract body; highlights, cover letter, title page, Section 2 not written")

want = TARGETS.get("+".join(groups))
got = {f: hashlib.sha256(s.encode()).hexdigest() for f, s in sorted(files.items())}
for f, h in got.items():
    print(("OK   " if want and want.get(f) == h else "DIFF "), f, h)
same = got == want
print("ALL RESULTS EQUAL TARGETS" if same else "RESULTS DIFFER FROM TARGETS (with SKIP set, the targets are those of the ruling)")
if write:
    assert same, "no file written: results differ from TARGETS"
    for f, s in files.items():
        (pathlib.Path(R) / "paper" / f).write_bytes(s.encode())
    print("WRITTEN: %d files to the working tree under ruling %s%s (not staged, not committed)" % (
        len(files), ruling, ", investigator's decision " + pi if "U" in groups else ""))
else:
    print("CHECK MODE: nothing written")
