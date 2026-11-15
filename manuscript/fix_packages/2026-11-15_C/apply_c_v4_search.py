#!/usr/bin/env python3
"""Paper C fix package v4, works found by the dated search (C_FIX_PACKAGE_v4_search.md): check, or write to the
paper repo WORKING TREE. APPLIES AFTER THE CC-408 COMMIT (fix package v2 as ruled, after the freeze shell).

Default mode (no argument): CHECK ONLY. Nothing is written. The script
  1. checks the pin of the package file and that commit 55315ca is an ancestor of HEAD;
  2. takes the base text of each file: `git show HEAD:<file>`, which must have the sha256 of PRE. For
     11_supplement_registered_rows.md PRE is the target of CC-408 Ruling 9, the text AFTER package v2. While
     package v2 is not committed, the check mode builds that text in memory with the functions of
     apply_c_v2_cc408.py (its own check mode), asserts that it has the PRE value and says so; the write mode
     refuses. This is the order gate: write only after the CC-408 commit, whether or not C-S15 is skipped;
  3. reads the OLD/NEW blocks from the package and applies them in package order (each OLD exactly once in the
     base text and at its turn, each NEW exactly once at the end), skipping the ids in SKIP;
  4. asserts: Tables 1 and 1b keep their cell counts and gain two rows each; the RAGCap row is byte-unchanged and
     is the only row of Table 1 with a dash cell; Table 1b has no dash cell; every citation key of
     02_related_work.md is defined in paperC.bib; the four new keys are defined once and have one audit row; the
     number tokens added to 02_related_work.md are exactly ADDED_TOKENS and each is a `number` of the manifest;
     no table label 10-18 appears; the new evidence rows repeat the cells of the new rows of Table 1b;
  5. prints the sha256 of each resulting file and compares it with TARGETS.

Write mode:  python3 -I apply_c_v4_search.py --write --ruling CC-xxx
  writes the files to the working tree only if every base text comes from HEAD at its PRE value, every result
  equals TARGETS and nothing is staged in the paper repo (the package is a commit of its own). TARGETS holds the
  package writer's values for the full package and for the package without C-S15. Any other choice needs SKIP
  and TARGETS set from the ruling. Never runs git add or git commit. The manifest is read, never written.
"""
import collections
import hashlib
import importlib.util
import pathlib
import re
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = pathlib.Path("/mnt/d/vsps_image_captioning/manuscript/fix_packages/2026-11-15_C")
PKG = HERE / "C_FIX_PACKAGE_v4_search.md"
PKG_SHA256 = "61ace3ab74fa7003265d2418e120fe5777577a6aaf15cb7e9529c476f55a4908"
V2 = HERE / "apply_c_v2_cc408.py"
R = "/mnt/d/vsps_papers/vsps-paperC-tallip"
BASE = "55315ca"
P02, PEV = "paper_v1_analysis/02_related_work.md", "docs/TABLE1B_W5_EVIDENCE.md"
PBIB, PAUD = "paper_v1_analysis/paperC.bib", "paper_v1_analysis/paperC_bib_audit.tsv"
P11, MAN = "paper_v1_analysis/11_supplement_registered_rows.md", "paper_v1_analysis/number_manifest_C.tsv"
PRE = {
    P02: "8dbc299bd816bb2fd9ec689b1ef1b97a1c2cab1e331232072dc4d7afee1a60fb",  # HEAD 55315ca; v2 checks it, does not change it
    PEV: "11a291b36b7822f3d006ac2e25ac1c01f243f136beb37f46fb079326c4458ab2",  # HEAD 55315ca
    PBIB: "a415c4daa4d8c40b5b14432913d62bfefdcc30d7ff347df05637f332c23010e2",  # HEAD 55315ca
    PAUD: "a1af33399c668a31efa2f13b91b85983f6f1ea780e1ccda0b3aaabcb9adb3826",  # HEAD 55315ca
    P11: "5a71a8a08085cdaabe385539208f008275aed18fabbd6c962cf0d0c5c44f0ff9",  # AFTER package v2 (CC-408 Ruling 9)
}
SKIP = ()  # block ids the ruling does not apply, e.g. ("C-S15",)
TARGETS = {  # by the sorted tuple of skipped ids
    (): {P02: "4288f1fb73a3df4a2629a8e0f6369c639d7a00c3a2c12e81eb425fafd355d64a", PEV: "03c79960beb66aac12b9fa482f9084b5cc3120f1aab9322099c13fc348d158c5", PBIB: "550b88d118f4bdb5dadbb930f05263e14ba65ab6df84c82285ccc824e1c777b8", PAUD: "55ece5075b17ff2b5d78d5760264d82b8e55918a5829d3a1545fbd45a83145d4", P11: "fc7608a33f069f4882f1f9b55cba70b5bd784f60877b0e08d90142a376e53c36"},
    ("C-S15",): {P02: "4288f1fb73a3df4a2629a8e0f6369c639d7a00c3a2c12e81eb425fafd355d64a", PEV: "03c79960beb66aac12b9fa482f9084b5cc3120f1aab9322099c13fc348d158c5", PBIB: "550b88d118f4bdb5dadbb930f05263e14ba65ab6df84c82285ccc824e1c777b8", PAUD: "55ece5075b17ff2b5d78d5760264d82b8e55918a5829d3a1545fbd45a83145d4"},
}
NEW_KEYS = ("Sharifymoghaddam2025UniRAG", "Freitas2026RAGMedCap", "Xiang2026GenderBiasICL", "Zong2025VLICLBench")
ADDED_TOKENS = ("3", "4", "4", "4", "4", "4", "8", "8")  # number tokens the package adds to 02_related_work.md; none is removed
RAGCAP_ROW = "| RAGCap [@Bazi2025RAGCap], from its abstract | no | yes | image-caption pairs | – | – | – |"
# the two patterns of apply_c_v2.py's renumbering pass and its token rule, copied
LABEL = r"S?\d+[a-z]?(?:\s*\([a-z]\))?"
TABLE_REF = re.compile(rf"\bTables?\s+{LABEL}(?:(?:,\s*|\s+and\s+|–){LABEL})*")
TABLE_LAB = re.compile(r"(?<![\dS.])(1[0-8])(?![\da-z])")
TOKEN = re.compile(r"(?<![\w.])[+−-]?\d[\d,]*(?:\.\d+)?")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", R, *args], capture_output=True, check=True).stdout.decode("utf-8")


def tokens(text: str) -> collections.Counter:
    found = TOKEN.finditer(re.sub(r"`[^`]*`", " ", text))
    return collections.Counter(m.group(0).replace("−", "-").replace("+", "").replace(",", "") for m in found)


def after_v2_in_memory() -> str:
    """Text of file 11 after package v2 as ruled, built by the check mode of apply_c_v2_cc408.py. Nothing is written."""
    spec = importlib.util.spec_from_file_location(V2.stem, V2)
    cc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cc)
    for path, pin in cc.PINS.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == pin, f"pin {path.name}"
    spec = importlib.util.spec_from_file_location(cc.MODULE.stem, cc.MODULE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    src = cc.after_c2_in_memory()
    cc.gate(mod, src)
    return cc.build(mod, src)[P11.split("/")[-1]]


def table(text: str, start: str, end: str) -> list[list[str]]:
    part = text.split(start)[1].split(end)[0]
    rows = [r for r in part.splitlines() if r.startswith("|") and not r.startswith("|---")]
    return [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows[1:]]  # without the header row


def check_content(old: dict[str, str], new: dict[str, str]) -> None:
    t1 = table(new[P02], "\n**Table 1. Design", "\n**Table 1b.")
    t1b = table(new[P02], "\n**Table 1b.", "\n**Position among the analyses.")
    was1 = table(old[P02], "\n**Table 1. Design", "\n**Table 1b.")
    was1b = table(old[P02], "\n**Table 1b.", "\n**Position among the analyses.")
    assert len(t1) == len(was1) + 2 and {len(r) for r in t1} == {7}, "Table 1: rows or cells"
    assert len(t1b) == len(was1b) + 2 and {len(r) for r in t1b} == {9}, "Table 1b: rows or cells"
    assert t1[-1][0] == "**this study**" and t1b[-1][0] == "**this study**", "the row of this study is not the last"
    assert new[P02].count(RAGCAP_ROW) == 1, "RAGCap row"
    assert [r[0] for r in t1 if any(c.startswith("–") for c in r)] == ["RAGCap [@Bazi2025RAGCap], from its abstract"]
    assert not [r for r in t1b if any(c.startswith("–") for c in r)], "Table 1b holds a dash cell"

    entry_key = re.compile(r"^@\w+\{([^,\s]+),", flags=re.M)
    defined = collections.Counter(entry_key.findall(new[PBIB]))
    cited = set(re.findall(r"@([A-Za-z][A-Za-z0-9]+)", new[P02]))
    assert cited <= set(defined), sorted(cited - set(defined))
    assert max(defined.values()) == 1 and len(defined) == len(entry_key.findall(old[PBIB])) + 4, "bibliography entries"
    audit = [r.split("\t") for r in new[PAUD].splitlines()[len(old[PAUD].splitlines()):]]
    assert [r[0] for r in audit] == list(NEW_KEYS) and {len(r) for r in audit} == {5}, "audit rows"
    for key in NEW_KEYS:
        assert key not in old[PBIB] and defined[key] == 1 and key in cited, key
        entry = new[PBIB].split("{" + key + ",")[1].split("\n}\n")[0]
        assert entry.count("{") == entry.count("}"), key + ": braces"

    added, removed = tokens(new[P02]) - tokens(old[P02]), tokens(old[P02]) - tokens(new[P02])
    assert not removed and added == collections.Counter(ADDED_TOKENS), (dict(added), dict(removed))
    manifest = {line.split("\t")[0] for line in git("show", "HEAD:" + MAN).splitlines()[1:]}
    assert set(added) <= manifest, sorted(set(added) - manifest)
    assert not TABLE_LAB.search(" ".join(TABLE_REF.findall(new[P02]))), "02_related_work.md holds a table label 10-18"

    lines = new[PEV].splitlines()
    for key in ("Xiang2026GenderBiasICL", "Freitas2026RAGMedCap"):
        row = next(r for r in t1b if r[0].startswith("@" + key))
        first = next(i for i, ln in enumerate(lines) if ln.startswith("| " + key + " ("))
        values = [ln.split(" | ")[2] for ln in lines[first:first + 7]]
        assert values == row[2:], (key, values, row[2:])


def main() -> int:
    write = "--write" in sys.argv
    ruling = sys.argv[sys.argv.index("--ruling") + 1] if "--ruling" in sys.argv else None
    assert not write or ruling, "--write needs --ruling <id of the GO ruling>"
    pkg = PKG.read_bytes()
    assert hashlib.sha256(pkg).hexdigest() == PKG_SHA256, "package pin"
    git("merge-base", "--is-ancestor", BASE, "HEAD")  # raises unless 55315ca is in the history
    assert git("status", "--porcelain", "--", *PRE) == "", "a file of this package differs from HEAD"
    old = {f: git("show", "HEAD:" + f) for f in PRE}
    for f in (P02, PEV, PBIB, PAUD):
        assert sha(old[f]) == PRE[f], f + " is not at its PRE value"
    v2_committed = sha(old[P11]) == PRE[P11]
    if not v2_committed:
        assert not write, "no file written: 11_supplement_registered_rows.md is not at the CC-408 target, package v2 is not committed"
        old[P11] = after_v2_in_memory()
        assert sha(old[P11]) == PRE[P11], "the in-memory text after package v2 is not the CC-408 target"
    print("order gate:", "package v2 is committed (file 11 at the CC-408 target)" if v2_committed
          else "package v2 is NOT committed yet; file 11 is checked on its after-v2 text built in memory; write mode would refuse")

    blocks = re.findall(r"<<<(C-S\d+) (\S+) OLD>>>\n(.*?)\n<<<\1 \2 NEW>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", pkg.decode("utf-8"), flags=re.S)
    assert len(blocks) == 15 and len({b[0] for b in blocks}) == 15 and {b[1] for b in blocks} == set(PRE), len(blocks)
    assert set(SKIP) <= {b[0] for b in blocks}, "unknown id in SKIP"
    todo = [b for b in blocks if b[0] not in SKIP]
    new = dict(old)
    for bid, f, was, now in todo:
        assert old[f].count(was) == 1 and new[f].count(was) == 1, (bid, old[f].count(was), new[f].count(was))
        new[f] = new[f].replace(was, now)
    for bid, f, was, now in todo:
        assert new[f].count(now) == 1, (bid, "NEW not exactly once")
    print("blocks applied:", [b[0] for b in todo])
    if not set(SKIP) - {"C-S15"}:
        check_content(old, new)
        print("content checks passed: table shapes; RAGCap row; keys cited and defined; audit rows; added number tokens; evidence rows equal table cells")
    else:
        print("content checks SKIPPED: they are written for the full package, with or without C-S15")

    changed = {f: s for f, s in sorted(new.items()) if s != old[f]}
    want = TARGETS.get(tuple(sorted(SKIP)))
    for f, s in changed.items():
        print("OK   " if want and want.get(f) == sha(s) else "DIFF ", f, sha(s))
    same = want is not None and {f: sha(s) for f, s in changed.items()} == want
    print("ALL RESULTS EQUAL TARGETS" if same else "RESULTS DIFFER FROM TARGETS, or no target is pinned for this SKIP")
    if write:
        assert same, "no file written: results differ from TARGETS"
        assert git("diff", "--cached", "--name-only") == "", "no file written: something is staged in the paper repo"
        for f, s in changed.items():
            (pathlib.Path(R) / f).write_bytes(s.encode("utf-8"))
        print(f"WRITTEN: {len(changed)} files to the working tree under ruling {ruling} (not staged, not committed)")
    print("WRITE MODE" if write else "CHECK MODE: nothing written;", "paper HEAD", git("rev-parse", "--short", "HEAD").strip())
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())
