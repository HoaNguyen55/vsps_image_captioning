#!/usr/bin/env python3
"""Mutant harness for scripts/c_pvr_a12/c_pvr_a12.py (form of scripts/c_pvr_gpu/c_pvr_gpu_mutants.py).
Usage: <c_pvr venv python> -I -B c_pvr_a12_mutants.py <repo root> <new scratch dir outside /mnt>.
Per mutant the scratch dir gets <name>/scripts/xm3600_oiv7.py (unchanged copy) and one mutated
<name>/scripts/c_pvr_a12/c_pvr_a12.py, which runs `selftest`. Each mutant replaces one exact string that occurs
once. The unmutated copy runs first and must print 'selftest ok'. KILLED = the selftest fails."""
import shutil
import subprocess
import sys
from pathlib import Path

M = {
    "pin_check_off": ("    if hashlib.sha256(b).hexdigest() != sha:\n", "    if False:\n"),
    "module_unpinned": ("    b = pinned(path, sha)\n    mod", "    b = Path(path).read_bytes()\n    mod"),
    "labels_unpinned": ('raw = json.loads(pinned(paths["labels"], pins["labels"]))',
                        'raw = json.loads(Path(paths["labels"]).read_bytes())'),
    "map_unpinned": ('    pinned(paths["map"], pins["map"])\n', ""),
    "desc_unpinned": ('    pinned(paths["desc"], pins["desc"])\n', ""),
    "ga_unpinned": ('ga = set(pinned(paths["ga"], pins["ga"])', 'ga = set(Path(paths["ga"]).read_bytes()'),
    "underscore_kept": ('if not k.startswith("_")}', "}"),
    "present_kept": ('if v == "absent")', 'if v != "unknown")'),
    "empty_kept": ('res = {q: r for q, r in res.items() if r["absent"]}', "res = res"),
    "count_check_off": ("    if got != expect:\n", "    if False:\n"),
    "outside_ok": ("if n_out := len(labels.keys() - qids):", "if n_out := 0:"),
    "ga_check_off": ("if n_ga := len(labels.keys() & ga):", "if n_ga := 0:"),
    "absence_guard_off": ("    if os.path.lexists(out):\n", "    if False:\n"),
    "fs_check_off": ('or fstype(out.parent) != "ext4"', "or False"),
    "barred_out_off": ('    if BARRED.search(str(out)) or', "    if"),
    "dir_mode_0755": ("    os.chmod(out, 0o700)\n", "    os.chmod(out, 0o755)\n"),
    "file_mode_0644": ("    os.chmod(tmp, 0o600)\n", "    os.chmod(tmp, 0o644)\n"),
    "meta_key_added": ("json.dumps(res, ensure_ascii", 'json.dumps({**res, "_meta": {"n": len(res)}}, ensure_ascii'),
    "ascii_escaped": ("ensure_ascii=False", "ensure_ascii=True"),
}


def main() -> int:
    root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    if str(scratch.resolve()).startswith("/mnt/"):
        raise SystemExit("scratch must be outside /mnt")
    scratch.mkdir()  # new dir only
    src = (root / "scripts/c_pvr_a12/c_pvr_a12.py").read_text(encoding="utf-8")

    def run(name: str, text: str) -> bool:
        d = scratch / name / "scripts"
        (d / "c_pvr_a12").mkdir(parents=True)
        shutil.copy2(root / "scripts/xm3600_oiv7.py", d / "xm3600_oiv7.py")
        (d / "c_pvr_a12/c_pvr_a12.py").write_text(text, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", "-B", str(d / "c_pvr_a12/c_pvr_a12.py"), "selftest"],
                           capture_output=True, text=True, timeout=300)
        return r.returncode == 0 and "selftest ok" in r.stdout

    if not run("_unmutated", src):
        raise SystemExit("the unmutated copy fails its selftest")
    killed = 0
    for name, (old, new) in M.items():
        if src.count(old) != 1:
            raise SystemExit(f"{name}: target string occurs {src.count(old)} times")
        k = not run(name, src.replace(old, new))
        killed += k
        print(f"{'KILLED' if k else 'SURVIVED'}  {name}")
    print(f"mutants killed {killed}/{len(M)}")
    return 0 if killed == len(M) else 1


if __name__ == "__main__":
    sys.exit(main())
