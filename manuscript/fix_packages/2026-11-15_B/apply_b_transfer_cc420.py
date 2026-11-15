"""Paper B: transfer of the held draft (draft_v3_1, after W1 of ruling CC-420) into the paper repository.

Default mode: builds the ten files of CC-420 ruling 6 in memory and prints, per target path, the sha256 it
would write and whether it equals the table of the ruling. Nothing is written.
--write --ruling CC-420: the same, then writes the files into the working tree. Never stages, never commits.

The first-line texts and the file list are read from ANNEX B of the ruling file (sha-checked), and the target
shas from its ruling 6; none is typed here.

Usage: python3 -I apply_b_transfer_cc420.py [--write --ruling CC-420] [--src DIR] [--repo DIR]
"""
import argparse
import ast
import hashlib
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
RULING = ROOT / ".session_backup/2026-10-13/decisions/CC-420.txt"
RULING_SHA = "994552078aab6439e340c57750e74185b5bc51071b0fc78479fe3f42d31fb449"
SRC = ROOT / ".session_backup/2026-11-14/b_text_held/draft_v3_1"
REPO = pathlib.Path("/mnt/d/vsps_papers/vsps-paperB-lre")
HEAD = "edf7fee"
REL = "paper/rev_2026-11-15"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_ruling():
    raw = RULING.read_bytes()
    assert sha(raw) == RULING_SHA, "ruling file does not hash to its pinned value"
    text = raw.decode("utf-8")
    body = text.split("----- BEGIN transfer.py -----\n", 1)[1].split("----- END transfer.py -----", 1)[0]
    consts = {}
    for node in ast.parse(body).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") in ("NOTE", "FILES", "HELD", "SPEC"):
            consts[node.targets[0].id] = ast.literal_eval(node.value)
    table = dict(re.findall(rf"^\s+({REL}/\S+)\s+([0-9a-f]{{64}})$", text, re.M))
    assert len(consts) == 4 and len(table) == len(consts["FILES"]) + 1, "ruling not parsed"
    return consts, table


def build(src, c):
    """The transformation of ANNEX B: first line replaced by one release line, nothing else."""
    out, sums = {}, []
    for f in c["FILES"]:
        first, rest = (src / f).read_text(encoding="utf-8").split("\n", 1)
        if f.endswith(".md"):
            assert first == c["HELD"] or (f == "FIGURE_TABLE_SPEC.md" and first.startswith(c["SPEC"])), f
            new = "<!-- " + c["NOTE"] + " -->"
        elif f.endswith(".tsv"):
            assert first == c["HELD"], f
            new = "# " + c["NOTE"]
        else:
            assert first == "% " + c["HELD"], f
            new = "% " + c["NOTE"]
        data = (new + "\n" + rest).encode("utf-8")
        assert c["HELD"].encode("utf-8") not in data, f + ": the held line is still in the file"
        out[f] = data
        sums.append(sha(data) + "  " + f)
    out["SNAPSHOT.sha256"] = ("\n".join(sums) + "\n").encode("utf-8")
    return out


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--ruling")
    ap.add_argument("--src", type=pathlib.Path, default=SRC)
    ap.add_argument("--repo", type=pathlib.Path, default=REPO)
    a = ap.parse_args()
    consts, table = read_ruling()
    out = build(a.src, consts)
    diff = 0
    for f, data in out.items():
        path = f"{REL}/{f}"
        ok = table.get(path) == sha(data)
        diff += not ok
        print(f"{sha(data)}  {path}  {'EQUAL' if ok else 'DIFFERENT'}")
    assert set(table) == {f"{REL}/{f}" for f in out}, "path list differs from ruling 6"
    print(f"paths: {len(out)}; different from the ruling: {diff}")
    if not a.write:
        print("check mode: nothing written")
        return 1 if diff else 0
    assert a.ruling == "CC-420", "--write needs --ruling CC-420"
    assert diff == 0, "a sha differs from the ruling: nothing written"
    assert git(a.repo, "rev-parse", "--short=7", "HEAD").strip() == HEAD, "paper repository HEAD is not " + HEAD
    assert git(a.repo, "status", "--porcelain") == "", "paper repository tree is not clean"
    dst = a.repo / REL
    dst.mkdir(parents=True, exist_ok=False)
    for f, data in out.items():
        (dst / f).write_bytes(data)
    print(f"written {len(out)} files to {dst}; not staged, not committed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
