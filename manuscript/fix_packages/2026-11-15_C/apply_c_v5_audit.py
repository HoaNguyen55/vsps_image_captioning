#!/usr/bin/env python3
"""Paper C fix package v5, the NOT READY items of the readiness audit (C_FIX_PACKAGE_v5_audit.md): check, or write
to the paper repo WORKING TREE. APPLIES AFTER THE CC-413 COMMIT (fix package v4 with Annex B, itself after the
CC-408 commit of package v2 and after the freeze shell).

Default mode (no argument): CHECK ONLY. Nothing is written. The script
  1. checks the pin of the package file and that commit 55315ca is an ancestor of HEAD;
  2. takes each file from `git show HEAD:<file>`, which must have the sha256 of PRE (the targets of CC-408 Ruling 9
     and of CC-413). While those commits do not exist, the check mode builds the same texts in memory: the section
     files and the manifest with the functions of apply_c_v2_cc408.py (the freeze transfer's own swap calls, a dummy
     stamp in the freeze row), then the 15 blocks of package v4, then the seven pairs of CC-413 Annex B read from
     the pinned ruling file. It asserts the PRE values and says so; both write modes refuse. This is the order gate;
  3. step 1: applies the blocks C-A01 ... C-A13 in package order (each OLD exactly once in the base text and at its
     turn, each NEW exactly once at the end; C-A13 is a new file), skipping the ids in SKIP, and runs the content
     checks;
  4. step 2 (manifest): checks that the lines before the two freeze rows have the sha256 of CC-408 Ruling 9 and
     that the freeze row and the row for 40 are the last two rows; appends the rows of C-M02 after re-checking each
     source; refreshes the used_in column (C-M03); checks that the two freeze rows and columns 1-5 of every earlier
     row are unchanged;
  5. prints the sha256 of each result and compares it with TARGETS and MAN_TARGETS. The freeze row carries a stamp
     that does not exist yet, so the manifest target is the sha256 of the manifest WITHOUT that one row.

Write modes (never git add / commit; each refuses unless nothing is staged in the paper repo):
  python3 -I -B apply_c_v5_audit.py --write --ruling CC-xxx            step 1: text, bibliography, tooling files
  python3 -I -B apply_c_v5_audit.py --write-manifest --ruling CC-xxx   step 2: the manifest only, run directly after
                                                                        step 1, while step 1 is in the working tree and
                                                                        not yet committed (HEAD still at the CC-413 state)
"""
import ast
import collections
import hashlib
import importlib.util
import pathlib
import re
import subprocess
import sys

sys.dont_write_bytecode = True
RUN = pathlib.Path("/mnt/d/vsps_image_captioning")
HERE = RUN / "manuscript/fix_packages/2026-11-15_C"
PKG = HERE / "C_FIX_PACKAGE_v5_audit.md"
PKG_SHA256 = "29cd9b7882182067e06b51114784c126b1b9738ef7248e41724ee14205f371f8"
V4 = HERE / "apply_c_v4_search.py"
V4_SHA256 = "2660d082128cecc5020550c2cff51a760a2bde7b0ef41b4e0e9195dc21c04a9f"
CC413 = RUN / ".session_backup/2026-10-13/decisions/CC-413.txt"
CC413_SHA256 = "b9c9ec64c7120b8f10622559ce43caae5078349a2e7a796e02fba26c508bc2be"
ANNEX_B_SHA256 = "3fb2a675a822a1742c70c283426ca2a89b25180abe3267d118611b8359fc0b00"  # CC-413, l.26-27
LOG = RUN / ".session_backup/2026-10-13/decisions/LOG.md"
R = pathlib.Path("/mnt/d/vsps_papers/vsps-paperC-tallip")
BASE = "55315ca"
PD = "paper_v1_analysis/"
P02, P03, P04, P11 = PD + "02_related_work.md", PD + "03_method.md", PD + "04_data_and_splits.md", PD + "11_supplement_registered_rows.md"
PBIB, PAUD, MAN = PD + "paperC.bib", PD + "paperC_bib_audit.tsv", PD + "number_manifest_C.tsv"
PCHK, PREADME = "scripts/paperC/c_pass2_check.py", PD + "tex/readme.txt"
PRE = {  # the state after the CC-413 commit
    P02: "b9f0c1f88cde26884debce22099c5eed1fdadb782a28608ecfab20acd1efebee",  # CC-413 TARGETS
    P03: "5db109ab3b011cf658da599d5ef67636c7b282f378829abb3a35f176521da057",  # CC-408 Ruling 9
    P04: "58529b1dc3444b9a89830661a0a724e4ee3fc5ed8bb8acb9383639a70320c540",  # CC-408 Ruling 9
    PBIB: "550b88d118f4bdb5dadbb930f05263e14ba65ab6df84c82285ccc824e1c777b8",  # CC-413 TARGETS
    PAUD: "55ece5075b17ff2b5d78d5760264d82b8e55918a5829d3a1545fbd45a83145d4",  # CC-413 TARGETS
    PCHK: "a257bd14891403a11a709030bfb785c2c3f6302ca342a6ef96324fbe0c11e7e7",  # HEAD 55315ca; no scheduled commit changes it
    P11: "c4a24cd4da244af6d36385e9b7796cbb3b8d05883c6f513a2d365988650f0d55",  # CC-413 TARGETS; read for the readme list
}
MAN_HEAD_SHA = "bae5743928a30483d090f8abb6ee45aae78934d27c40a1122db688efe2c0f95f"  # CC-408 Ruling 9: lines before the two freeze rows
SKIP = ()  # () or ("C-A13",): the readme may be left for the packaging step; no other target depends on it
MAN_OPS = ("C-M02", "C-M03")  # or ("C-M02",) if the ruling strikes the used_in refresh
TARGETS = {
    P02: "397ce7971cca25bc5ec47856c966a189cadeed6a67f493fe117dfa31261592d4", P03: "3a36a06f84469a70edccfa5eeab365646a33c4cf523b930299dfdb8c4ec3b383", P04: "0334d0aa33c41258246797d7f73e483e4007f9cb1416f9389cba49eb59863545", PBIB: "21de95eaf16a88fdfdabbde76078d625e72d29dacbac1814d795ea0bf0ea92a2", PAUD: "8730a73ea2cbb14bd815fea6fdf8a9cc1d021a908a31afe4cf9634613b0fdfb0", PCHK: "254b4c2ea81cf07c097b189954e8c533da22fd81fdddfee08e37f75c6181bd21", PREADME: "31e73e128bae39b3538d7a8c48c50683a7f812327629149aec614d50671fa5dd",
}
MAN_TARGETS = {  # sha256 of the manifest without the freeze row, by MAN_OPS
    ("C-M02", "C-M03"): "fa91f4289a124a270a91803cc439eeedad06c93d681d0495492be458ad672140",
    ("C-M02",): "79af62fd02e7758628e856e2bfa21945961bbd3ac46903fd50716eff59c8fb7f",
}
M03_COUNTS = (271, 258, 29, 20)  # pointers removed, rows changed, tags moved, rows left without a file name
NEW_KEY = "Krasin2017OpenImages"
CHANGED_KEYS = ("Hussain2026SciRepLVLM", "Yang2023ReViLM", "Oduwole2025AfriCaption")
PREREG = RUN / "manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md"
MUTLOG = RUN / "scripts/c_attr/block0/MUTANTS_LOG.txt"
TOKEN = re.compile(r"(?<![\w.])[+−-]?\d[\d,]*(?:\.\d+)?")  # the token rule of c_pass2_check.py and of packages v2 and v4


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(R), *args], capture_output=True, check=True).stdout.decode("utf-8")


def load(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm(s: str) -> str:
    return s.replace("−", "-").replace("+", "").replace(",", "")


def tokens(text: str) -> collections.Counter:
    return collections.Counter(norm(m.group(0)) for m in TOKEN.finditer(re.sub(r"`[^`]*`", " ", text)))


def after_cc413_in_memory() -> dict[str, str]:
    """Every section file, the manifest and the files of package v4 as they stand after C2, v2 (CC-408) and v4 with
    Annex B (CC-413), built with those scripts' own functions. Nothing is written."""
    assert hashlib.sha256(V4.read_bytes()).hexdigest() == V4_SHA256, "pin apply_c_v4_search.py"
    v4 = load(V4)
    cc = load(v4.V2)
    for path, pin in cc.PINS.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == pin, f"pin {path.name}"
    assert cc.MAN_HEAD_SHA == MAN_HEAD_SHA
    mod = load(cc.MODULE)
    src = cc.after_c2_in_memory()
    cc.gate(mod, src)
    st = {PD + f: text for f, text in (src | cc.build(mod, src)).items()}
    assert sha(st[P11]) == v4.PRE[P11], "file 11 after package v2 is not the CC-408 target"
    pkg = v4.PKG.read_bytes()
    assert hashlib.sha256(pkg).hexdigest() == v4.PKG_SHA256, "pin C_FIX_PACKAGE_v4_search.md"
    for f in (v4.P02, v4.PEV, v4.PBIB, v4.PAUD):
        st[f] = git("show", f"{BASE}:{f}")
        assert sha(st[f]) == v4.PRE[f], f + " at 55315ca is not at the PRE value of package v4"
    blocks = re.findall(r"<<<(C-S\d+) (\S+) OLD>>>\n(.*?)\n<<<\1 \2 NEW>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", pkg.decode("utf-8"), flags=re.S)
    assert len(blocks) == 15
    for bid, f, was, now in blocks:
        assert st[f].count(was) == 1, bid
        st[f] = st[f].replace(was, now)
    ruling = CC413.read_bytes()
    assert hashlib.sha256(ruling).hexdigest() == CC413_SHA256, "pin CC-413.txt"
    annex = ruling.split(b"----- BEGIN ANNEX B (annex_b.py) -----\n")[1].split(b"----- END ANNEX B -----")[0]
    assert hashlib.sha256(annex).hexdigest() == ANNEX_B_SHA256, "Annex B bytes"
    names: dict = {}
    exec(compile(annex.decode("utf-8").split("\n\n\ndef sha")[0], "CC-413 Annex B, constants", "exec"), names)  # the pinned bytes; its functions are not run
    for f, want in names["PRE"].items():
        assert sha(st[f]) == want, f + " is not at its package v4 target"
    for f, old, new in names["PAIRS"]:
        assert st[f].count(old) == 1, ("Annex B", old[:50])
        st[f] = st[f].replace(old, new)
    for f, want in names["POST"].items():
        assert sha(st[f]) == want, f + " is not at its CC-413 target"
    return st


def freeze_rows(lines: list[str]) -> int:
    """Index of the freeze row; asserts the manifest is the CC-408 manifest plus the two rows of shell C2."""
    assert lines[-1] == "", "manifest: no final line break"
    n = len(lines) - 3
    assert sha("\n".join(lines[:n]) + "\n") == MAN_HEAD_SHA, "manifest: the lines before the two freeze rows are not those of CC-408 Ruling 9"
    assert re.match(r"NOT RUN\tdecisions LOG::OPS-[0-9a-z]+-c-k7\t", lines[n]) and lines[n].endswith("\t06_results.md"), "freeze row missing"
    assert lines[n + 1].startswith("40\tmanuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md::§5 No Vietnamese memory swap"), "row for 40 missing"
    return n


def prints(num: str, text: str) -> bool:
    """Generous on purpose (a valid pointer must never be lost): any sign, trailing zeros, code spans included.
    A value that is not a plain number (a verdict, a label, a stamp, a description) is not judged: True."""
    raw = num.strip("'")
    if not TOKEN.fullmatch(raw):
        return True
    strip0 = lambda s: s.rstrip("0").rstrip(".") if "." in s else s
    have = {strip0(norm(m.group(0)).lstrip("-")) for m in TOKEN.finditer(text)}
    return strip0(norm(raw).lstrip("-")) in have


def refresh_used_in(rows: list[str], texts: dict[str, str]) -> tuple[list[str], tuple[int, int, int, int]]:
    """C-M03. texts: file name -> text, for the section files of the paper folder."""
    out, gone, changed, moved, empty = [], 0, 0, 0, 0
    for row in rows:
        c = row.split("\t")
        parts = [p.partition("|") for p in c[5].split(",")] if c[5] else []
        tags = [tag for _, _, tag in parts if tag]
        assert len(tags) <= 1 and len(c) == 6, row[:80]
        files = [f for f, _, _ in parts if f]
        keep = [f for f in files if f not in texts or prints(c[0], texts[f])]
        moved += bool(tags) and not parts[-1][2]
        gone += len(files) - len(keep)
        empty += bool(files) and not keep
        c[5] = ",".join(keep) + ("|" if keep and tags else "") + "".join(tags)
        changed += "\t".join(c) != row
        out.append("\t".join(c))
    return out, (gone, changed, moved, empty)


def new_rows(pkg: str, texts: dict[str, str]) -> list[str]:
    """C-M02: the rows of the package, each source checked again."""
    rows = re.search(r"<<<C-M02 (\S+) ROWS>>>\n(.*?)\n<<<C-M02 EVIDENCE>>>\n", pkg, flags=re.S)
    assert rows and rows.group(1) == MAN
    rows = rows.group(2).split("\n")
    cells = [r.split("\t") for r in rows]
    assert [c[0] for c in cells] == ["0.025", "0.0125", "22", "33", "73"] and {len(c) for c in cells} == {6}
    prereg = PREREG.read_bytes()
    assert hashlib.sha256(prereg).hexdigest()[:12] == cells[0][3] == cells[1][3], "registration v1.1 pin"
    for quote in (cells[0][2].strip("'"), "α_j = 0.025 / (m − j + 1)"):
        assert quote in prereg.decode("utf-8"), quote
    mut = MUTLOG.read_bytes()
    assert hashlib.sha256(mut).hexdigest()[:12] == cells[2][3] and mut.decode("utf-8").split("\n").count(cells[2][2].strip("'")) == 1, "mutant log"
    log = LOG.read_text(encoding="utf-8").split("\n")
    for c in cells[3:]:
        ident = c[1].removeprefix("decisions LOG::")
        hit = [ln for ln in log if re.match(r"\S+ (\| )?" + re.escape(ident) + r"[: ]", ln)]
        assert len(hit) == 1 and sha(hit[0])[:12] == c[3] and c[2].strip("'") in hit[0], ident
    for c in cells:
        for f in c[5].split(","):
            assert prints(c[0], texts[f]), (c[0], f)
    return rows


def manifest_step(man: str, pkg: str, texts: dict[str, str]) -> tuple[str, str]:
    """Returns the new manifest and the sha256 of it without the freeze row."""
    lines = man.split("\n")
    n = freeze_rows(lines)
    head, frozen = lines[1:n], lines[n:n + 2]
    add = new_rows(pkg, texts)
    assert not set(add) & set(lines), "a row of C-M02 is already in the manifest"
    if "C-M03" in MAN_OPS:
        new_head, counts = refresh_used_in(head, texts)
        assert [r.split("\t")[:5] for r in new_head] == [r.split("\t")[:5] for r in head], "C-M03 changed a column other than used_in"
        assert refresh_used_in(new_head, texts)[0] == new_head, "C-M03 is not stable on its own result"
        assert counts == M03_COUNTS, counts
        head = new_head
    out = [lines[0], *head, *frozen, *add, ""]
    assert out[n:n + 2] == lines[n:n + 2] and len(out) == len(lines) + len(add), "freeze rows moved or changed"
    return "\n".join(out), sha("\n".join(out[:n] + out[n + 1:]))


def check_content(old: dict[str, str], new: dict[str, str]) -> None:
    entry_key = re.compile(r"^@\w+\{([^,\s]+),", flags=re.M)
    defined = collections.Counter(entry_key.findall(new[PBIB]))
    assert max(defined.values()) == 1 and len(defined) == len(entry_key.findall(old[PBIB])) + 1 and NEW_KEY not in old[PBIB], "bibliography entries"
    for f in (P02, P03, P04):
        cited = set(re.findall(r"@([A-Za-z][A-Za-z0-9]+)", new[f]))
        assert cited <= set(defined), sorted(cited - set(defined))
        assert NEW_KEY in cited and tokens(new[f]) == tokens(old[f]), f + ": the new key is missing or a number token changed"
    audit = [r.split("\t") for r in new[PAUD].rstrip("\n").split("\n")]
    assert len(audit) == len(old[PAUD].rstrip("\n").split("\n")) + 1, "audit rows"
    for key in (NEW_KEY, *CHANGED_KEYS):
        entry = re.search(r"^@\w+\{" + key + r",.*?^\}$", new[PBIB], flags=re.S | re.M).group(0)
        assert entry.count("{") == entry.count("}") and ("doi" in entry or key == NEW_KEY), key
        mine = [r for r in audit if r[0] == key]
        assert len(mine) == 1 and len(mine[0]) == 5 and "2026-11-15" in mine[0][4], key
    ast.parse(new[PCHK])
    assert "/mnt/" not in new[PCHK] and (R / PCHK).parents[2] == R, "the checker must find the manifest from its own place"
    if PREADME in new:
        listed = [ln[4:] for ln in new[PREADME].split("\n") if ln.startswith("  - ")][1:]
        assert listed == re.findall(r"^### (.+)$", old[P11], flags=re.M), "readme list differs from the headings of file 11"


def main() -> int:
    mode = [a for a in sys.argv[1:] if a in ("--write", "--write-manifest")]
    ruling = sys.argv[sys.argv.index("--ruling") + 1] if "--ruling" in sys.argv else None
    assert len(mode) <= 1 and (not mode or ruling), "usage: no argument (check), or --write | --write-manifest with --ruling <id of the GO ruling>"
    assert set(SKIP) <= {"C-A13"} and MAN_OPS in MAN_TARGETS, "SKIP or MAN_OPS has no pinned target"
    raw = PKG.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PKG_SHA256, "package pin"
    pkg = raw.decode("utf-8")
    git("merge-base", "--is-ancestor", BASE, "HEAD")  # raises unless 55315ca is in the history
    sections = [f for f in git("ls-tree", "--name-only", "HEAD", PD).split("\n") if f.endswith(".md")]
    old = {f: git("show", "HEAD:" + f) for f in {*PRE, MAN, *sections}}
    assert git("ls-tree", "--name-only", "HEAD", PREADME) == "" and not (R / PREADME).exists(), "tex/readme.txt exists already"
    committed = all(sha(old[f]) == want for f, want in PRE.items())
    if not committed:
        assert not mode, "no file written: the paper repo is not at the state after the CC-413 commit"
        old |= {f: text for f, text in after_cc413_in_memory().items() if f in old}
        for f, want in PRE.items():
            assert sha(old[f]) == want, f + ": the in-memory text is not at its CC-408 / CC-413 target"
    print("order gate:", "the CC-413 commit is in place (every file at its target at HEAD)" if committed else
          "the CC-413 commit does NOT exist yet; every file is checked on its text built in memory; the write modes would refuse")

    blocks = re.findall(r"<<<(C-A\d+) (\S+) OLD>>>\n(.*?)\n<<<\1 \2 NEW>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", pkg, flags=re.S)
    created = re.findall(r"<<<(C-A\d+) (\S+) NEWFILE>>>\n(.*?)\n<<<\1 EVIDENCE>>>\n", pkg, flags=re.S)
    assert [b[0] for b in blocks] == [f"C-A{i:02d}" for i in range(1, 13)] and [(c[0], c[1]) for c in created] == [("C-A13", PREADME)]
    assert {b[1] for b in blocks} == set(PRE) - {P11}
    new = dict(old)
    for bid, f, was, now in blocks:
        assert old[f].count(was) == 1 and new[f].count(was) == 1, (bid, old[f].count(was), new[f].count(was))
        new[f] = new[f].replace(was, now)
    for bid, f, was, now in blocks:
        assert new[f].count(now) == 1, (bid, "NEW not exactly once")
    if "C-A13" not in SKIP:
        new[PREADME] = created[0][2] + "\n"
    check_content(old, new)
    print("step 1: blocks applied:", [b[0] for b in blocks] + [c[0] for c in created if c[0] not in SKIP], "; content checks passed")
    changed = {f: s for f, s in sorted(new.items()) if s != old.get(f)}
    want = {f: h for f, h in TARGETS.items() if f != PREADME or "C-A13" not in SKIP}
    for f, s in changed.items():
        print("OK   " if want.get(f) == sha(s) else "DIFF ", f, sha(s))
    same = {f: sha(s) for f, s in changed.items()} == want

    texts = {f.removeprefix(PD): new[f] for f in sections}
    man, man_sha = manifest_step(old[MAN], pkg, texts)
    print("OK   " if man_sha == MAN_TARGETS[MAN_OPS] else "DIFF ", MAN, "without the freeze row:", man_sha, "| ops", MAN_OPS,
          "| C-M03 (pointers removed, rows changed, tags moved, rows left without a file):", M03_COUNTS if "C-M03" in MAN_OPS else "not applied")
    same &= man_sha == MAN_TARGETS[MAN_OPS]
    print("ALL RESULTS EQUAL TARGETS" if same else "RESULTS DIFFER FROM TARGETS")

    if mode:
        assert same, "no file written: results differ from TARGETS"
        assert git("diff", "--cached", "--name-only") == "", "no file written: something is staged in the paper repo"
    if mode == ["--write"]:
        assert git("status", "--porcelain", "--", *PRE) == "", "no file written: a file of this package differs from HEAD"
        for f, s in changed.items():
            (R / f).write_bytes(s.encode("utf-8"))
        print(f"WRITTEN (step 1): {len(changed)} files to the working tree under ruling {ruling} (not staged, not committed)")
    if mode == ["--write-manifest"]:
        assert git("status", "--porcelain", "--", MAN) == "", "no file written: the manifest differs from HEAD"
        for f in changed:  # step 1 must be in the working tree (committed or not)
            assert sha((R / f).read_text(encoding="utf-8")) == want[f], f"no file written: step 1 is not applied ({f})"
        (R / MAN).write_bytes(man.encode("utf-8"))
        print(f"WRITTEN (step 2): the manifest, to the working tree under ruling {ruling} (not staged, not committed)")
    print("CHECK MODE: nothing written;" if not mode else mode[0], "paper HEAD", git("rev-parse", "--short", "HEAD").strip())
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())
