#!/usr/bin/env python3
"""Mutant harness for scripts/c_pvr_ktc/c_pvr_ktc_fetch.py (form of scripts/c_pvr_a12/c_pvr_a12_mutants.py).
Usage: TMPDIR=<ext4 dir> python3 -I -B c_pvr_ktc_fetch_mutants.py <repo root> <new scratch dir outside /mnt>.
Per mutant the scratch dir gets <name>/scripts/c_en/cen_fetch.py (unchanged copy; the pin and ROOT = parents[2]
need that place) and one mutated <name>/scripts/c_pvr_ktc/c_pvr_ktc_fetch.py, which runs `selftest` (no network: a
fake OPEN, and the selftest makes any socket connect fail). Each mutant replaces one exact string that occurs once.
The unmutated copy runs first and must print 'selftest ok'. KILLED = the selftest fails."""
import shutil
import subprocess
import sys
from pathlib import Path

GET = "            b, err = mod.get(url)\n"
LOOP = "    for i, f in rows:\n"
WM = "            write_manifest(part, done, final=False)\n"
UA_LINE = '    o.addheaders = [("User-Agent", UA)]\n'
M = {
    # plan §10
    "mismatch_kept": ('bad = "sha" if mod.sha_bytes(b) != s else', 'bad = "sha" if False else'),
    "bytes_unchecked": ('"bytes" if len(b) != n else ""', '"bytes" if False else ""'),
    "name_outside_tsv": (LOOP, "    for i, f in rows + [(j, rec[j][1]) for j in sorted(own & set(rec))[:1]]:\n"),
    "record_instead_of_tsv": (LOOP, "    for i, f in sorted((j, v[1]) for j, v in rec.items()):\n"),
    "redirect_accepted": (GET, '            b, err = mod.OPEN(url, timeout=60).read(), ""\n'),
    "absence_guard_off": ("    if not resume and os.path.lexists(k):\n", "    if False:\n"),
    "mkdir_exist_ok": ("            os.mkdir(k, 0o700)\n", "            os.makedirs(k, 0o700, exist_ok=True)\n"),
    "file_mode_0644": ("    os.chmod(tmp, 0o600)\n    os.replace(tmp, k / f)", "    os.chmod(tmp, 0o644)\n    os.replace(tmp, k / f)"),
    "dir_mode_0755": ("        os.chmod(k, 0o700)\n", "        os.chmod(k, 0o755)\n"),
    "write_before_check": ("            check(i, b, s, n, mod)\n            keep(k, f, b, s, mod, i)\n",
                           "            keep(k, f, b, s, mod, i)\n            check(i, b, s, n, mod)\n"),
    "retry_loop_added": (GET, "            b, err = mod.get(url, tries=4)\n"),
    "second_pass": (GET, GET + "            if b is None:\n                b, err = mod.get(url)\n"),
    # H6-AM1
    "owner_check_off": ("    if ids != set(rec) - own:\n", "    if False:\n"),
    "a_t3_dropped": ('KT_C_OUT = ("uitviic_train_pool", "m0_dev_touched_3454", "a_t3_val2017")',
                     'KT_C_OUT = ("uitviic_train_pool", "m0_dev_touched_3454")'),
    "all_owner_keys": ('for o in KT_C_OUT for x in doc[o]["ids"]', 'for o in doc for x in doc[o]["ids"]'),
    "owners_unpinned": ('json.loads(pinned(cfg["paths"]["owners"], cfg["pins"]["owners"]))',
                        'json.loads(Path(cfg["paths"]["owners"]).read_bytes())'),
    # H6-AM2
    "cen_unpinned": ("    b = pinned(path, want)\n    mod", "    b = Path(path).read_bytes()\n    mod"),
    "cen_file_unset": ("    mod.__file__ = str(path)\n", ""),
    # H6-AM3
    "manifest_guard_off": ("    if not resume and (os.path.lexists(man) or os.path.lexists(part)):\n", "    if False:\n"),
    "partial_named_final": (WM, "            write_manifest(man, done, final=False)\n"),
    "partial_not_written": (WM, "            pass\n"),
    "manifest_overwrites": ("        os.link(tmp, dst)\n        os.unlink(tmp)\n", "        os.replace(tmp, dst)\n"),
    "manifest_mode_0644": ("    os.chmod(tmp, 0o600)\n    if final:", "    os.chmod(tmp, 0o644)\n    if final:"),
    "manifest_unsorted": ("for f, s in sorted(done.items())", "for f, s in done.items()"),
    # H6-AM4 / O4
    "record_unpinned": ('rb = pinned(cfg["paths"]["record"], cfg["pins"]["record"])',
                        'rb = Path(cfg["paths"]["record"]).read_bytes()'),
    "eio_unhandled": ("    except OSError as e:", "    except ValueError as e:"),
    # other preflight checks
    "pin_compare_off": ("    if sha(b) != want:\n", "    if False:\n"),
    "qtsv_line_off": ('    if f"{tsv_sha}  {tsv.name}" not in', '    if False and f"{tsv_sha}  {tsv.name}" not in'),
    "tsv_unpinned": ('text = pinned(tsv, tsv_sha).decode("ascii")', 'text = Path(tsv).read_bytes().decode("ascii")'),
    "ext4_check_off": ('    if fstype(k.parent) != "ext4":\n', "    if False:\n"),
    "barred_off": ("    if BARRED.search(str(k)) or BARRED.search(str(tsv)):\n", "    if False:\n"),
    "row_count_off": ("    if len(rows) != n:\n", "    if False:\n"),
    "unique_off": ("    if len(ids) != n or len({f for _, f in rows}) != n:\n", "    if False:\n"),
    "pair_check_off": ("        if rec[i][1] != f:\n", "        if False:\n"),
    "url_rule_off": ('url = mod.url_ok("coco_test", (i, f, mod.COCO_URL.format(filepath="val2014", file=f), ""))',
                     "url = URL_BASE + f"),
    "bytes_total_off": ('    if total != cfg["expect"]["bytes"]:\n', "    if False:\n"),
    "record_rows_off": ('    if len(rec) != cfg["expect"]["record_rows"]:\n', "    if False:\n"),
    # per-image disk check, STOP form, request headers
    "rehash_off": ("    if mod.sha_file(k / f) != s:\n", "    if False:\n"),
    "rehash_mismatch_kept": ("        os.unlink(k / f)\n        stop(", "        stop("),
    "exception_escapes": ("    except BaseException as e:", "    except Exception as e:"),
    "proxy_env_used": ("urllib.request.ProxyHandler({})", "urllib.request.ProxyHandler()"),
    "ua_missing": (UA_LINE, ""),
    "install_opener_dropped": ("    urllib.request.install_opener(opener())\n", ""),
    "end_listing_off": ("        if sorted(os.listdir(k)) != sorted(want):\n", "        if False:\n"),
    "end_bytes_off": ('        if sum(os.stat(k / f).st_size for f in want) != pre["total"]:\n', "        if False:\n"),
    "from_header_added": (UA_LINE, '    o.addheaders = [("User-Agent", UA), ("From", "decoy")]\n'),
    # resume (CC-281 O1)
    "resume_guard_off": ("    if resume and (not k.is_dir() or", "    if False and (not k.is_dir() or"),
    "ruling_unchecked": ("        if not RULING.fullmatch(ruling):\n", "        if False:\n"),
    "resume_no_rehash": ("        elif mod.sha_file(k / p) != want[p][1] or os.stat(k / p).st_size != want[p][2]:\n",
                         "        elif False:\n"),
    "resume_unlisted_kept": ("        elif p not in want:\n", "        elif False:\n"),
    "resume_tmp_kept": ('            os.unlink(k / p)\n            print("resume: removed',
                        '            print("resume: removed'),
    "partial_kept_after_resume": ("        os.unlink(part)\n", "        pass\n"),
}


def main() -> int:
    root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    if str(scratch.resolve()).startswith("/mnt/"):
        raise SystemExit("scratch must be outside /mnt")
    scratch.mkdir()  # new dir only
    src = (root / "scripts/c_pvr_ktc/c_pvr_ktc_fetch.py").read_text(encoding="utf-8")

    def run(name: str, text: str) -> bool:
        d = scratch / name / "scripts"
        (d / "c_en").mkdir(parents=True)
        (d / "c_pvr_ktc").mkdir()
        shutil.copy2(root / "scripts/c_en/cen_fetch.py", d / "c_en/cen_fetch.py")
        (d / "c_pvr_ktc/c_pvr_ktc_fetch.py").write_text(text, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", "-B", str(d / "c_pvr_ktc/c_pvr_ktc_fetch.py"), "selftest"],
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
