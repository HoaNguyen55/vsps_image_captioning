#!/usr/bin/env python3
"""Paper C: the KT-C pixel fetch (R-H6 plan R_H6_KTC_FETCH_PLAN_v1.md 3bbe0426 §3-§10; CC-280 Ruling 3 (a)-(h);
CC-281 O1-O4 and H6-AM1..AM4; CC-282 Ruling 13; PI-1106k).

  python3 -I -B scripts/c_pvr_ktc/c_pvr_ktc_fetch.py selftest                         synthetic fixtures, no network
  python3 -I -B scripts/c_pvr_ktc/c_pvr_ktc_fetch.py preflight --tsv F --tsv-sha H --out K       no network, no write
  python3 -I -B scripts/c_pvr_ktc/c_pvr_ktc_fetch.py fetch --tsv F --tsv-sha H --out K   coordinator, after the row
  python3 -I -B scripts/c_pvr_ktc/c_pvr_ktc_fetch.py resume --tsv F --tsv-sha H --out K --ruling CC-n   ruled only

Coordinator order: preflight -> ACCESS_LOG hand row (the coordinator appends it; this script never does) -> fetch.
preflight checks the pins (cen_fetch e51918e9, the C-EN record 614afa1b, B's owners file ae4b6630, QTSV.sha256 beside
the TSV, the TSV itself), the 3,907 (id, name) pairs against the record, H6-AM1 (TSV ids == record ids minus the
KT_C_OUT owners), the url_ok rule, the byte total, and the absence of K and of its manifest files. Every input is
parsed from the bytes that were hashed. fetch re-runs all of it (the second record read, H6-AM4), creates K (new,
0700, ext4), then makes one cen_fetch.get per TSV name, sequentially, at the plan §5 url
(http://images.cocodataset.org/val2014/<name>; integrity rests on the per-image sha, CC-280 3(a)). Each body is
checked in memory (sha256 and byte count = the record row) before any write; on a pass it is written O_EXCL 0600 as
.tmp_<name>, fsynced, renamed, and re-hashed from disk. Any failure is a STOP: nothing more is fetched, the verified
files stay, and the verified list goes to <K>.sha256.partial. On a complete run <K>.sha256 (sha256sum format, sorted)
is written last. There is no retry beyond get's own 3 tries and no second pass. A rerun is refused by the absence
guard; `resume` exists only for a ruled resume (CC-281 O1): it re-hashes every file in K against the record, removes
a stray .tmp_<name>, and fetches only the rest. Requests carry User-Agent vsps-research only and ignore proxy env.
Stdout: counts, shas, paths of K and its manifest; an id appears only in a STOP line.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import types
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = {  # repo path, full sha256 pin
    "cen_fetch": ("scripts/c_en/cen_fetch.py", "e51918e958ad86e832dd34fbf5ed86d2f7fc13cf41b602dfe537afa43af4c673"),
    "record": (".session_backup/machines/M1/root/outputs/c_en/fetch/coco_test.sha256.tsv",
               "614afa1b7cf63bde693fc9692b1699d47ba527d396b7a1216d031b1d50018fdf"),  # cen_fetch RECORD_PINS
    "owners": (".session_backup/2026-11-02/b_pa1/b_pa1_owners.json",
               "ae4b663064588a8a19dcd0c01a34284229b40c6de90cd24c88d098b7600b71b2"),  # c_pvr_run B_OWN
}
QTSV_PIN = "6962b7e6360983b0a9f702a9155ac6bd74a437058dd00df0bd91555d5e61fa5e"  # OPS-1107c-qtsv
EXPECT = {"record_rows": 5000, "kt_c": 3907, "bytes": 640065284}  # plan §3; c_pvr_run DEV_N; OPS-1107c-qtsv
KT_C_OUT = ("uitviic_train_pool", "m0_dev_touched_3454", "a_t3_val2017")  # c_pvr_run.py l.1248, the 1,093 owners
URL_BASE = "http://images.cocodataset.org/val2014/"  # plan §5: COCO_URL with filepath val2014
UA = "vsps-research"
BARRED = re.compile(r"\.vsps_sealed|t2pool_", re.I)
TSV_LINE = re.compile(r"([1-9][0-9]*)\t(\S+)")
RULING = re.compile(r"CC-[0-9]{3,}")
EVERY = 500


def fault(msg: str):
    raise SystemExit(f"FAULT: {msg}")


def stop(msg: str):
    raise SystemExit(f"STOP: {msg}")


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def pinned(path: Path, want: str) -> bytes:
    if BARRED.search(str(path)):
        fault(f"barred path {Path(path).name}")
    try:
        b = Path(path).read_bytes()
    except OSError as e:  # plan O4 / H6-AM4: an EIO on /mnt/d is a STOP before any network call
        fault(f"{Path(path).name}: read failed ({type(e).__name__}); no network call made")
    if sha(b) != want:
        fault(f"{Path(path).name} differs from its pin {want[:8]}")
    return b


def load_cen(path: Path, want: str) -> types.ModuleType:
    """cen_fetch built from its sha-checked bytes, __file__ = its repo path (H6-AM2); never re-opened by path."""
    b = pinned(path, want)
    mod = types.ModuleType("cen_fetch")
    mod.__file__ = str(path)
    exec(compile(b, str(path), "exec"), mod.__dict__)
    return mod


def fstype(p: Path) -> str:
    """Filesystem type of the mount holding realpath(p) (longest mount-point prefix; CC-281 N2)."""
    p, best, kind = os.path.realpath(p), "", ""
    for ln in Path("/proc/self/mountinfo").read_text().splitlines():
        f = ln.split()
        mp = f[4].replace("\\040", " ")
        if (p == mp or p.startswith(mp.rstrip("/") + "/")) and len(mp) >= len(best):
            best, kind = mp, f[f.index("-") + 1]
    return kind


def real_cfg() -> dict:
    return {"paths": {k: ROOT / p for k, (p, _) in P.items()}, "pins": {k: s for k, (_, s) in P.items()},
            "qtsv": QTSV_PIN, "expect": dict(EXPECT)}


def preflight(cfg: dict, tsv: Path, tsv_sha: str, out: Path, resume: bool = False) -> dict:
    """Plan §3-§4 + H6-AM1/AM3/AM4. No network, nothing written. Any failure is a FAULT (STOP before the row)."""
    tsv, k = Path(os.path.abspath(tsv)), Path(os.path.abspath(out))
    man, part = k.with_name(k.name + ".sha256"), k.with_name(k.name + ".sha256.partial")
    if BARRED.search(str(k)) or BARRED.search(str(tsv)):
        fault("barred path")
    if not resume and os.path.lexists(k):
        fault("K exists (absence guard, plan §6)")
    if not resume and (os.path.lexists(man) or os.path.lexists(part)):
        fault("a manifest file of K exists (H6-AM3 absence guard)")
    if resume and (not k.is_dir() or k.is_symlink() or not part.is_file() or os.path.lexists(man)):
        fault("resume needs K, its .partial manifest and no final manifest (CC-281 O1)")
    if fstype(k.parent) != "ext4":
        fault("K must sit on ext4")
    mod = load_cen(cfg["paths"]["cen_fetch"], cfg["pins"]["cen_fetch"])
    if f"{tsv_sha}  {tsv.name}" not in pinned(tsv.parent / "QTSV.sha256", cfg["qtsv"]).decode("ascii").splitlines():
        fault("--tsv-sha is not the kt_c line of the pinned QTSV.sha256")
    text = pinned(tsv, tsv_sha).decode("ascii")
    m = [TSV_LINE.fullmatch(x) for x in text[:-1].split("\n")] if text.endswith("\n") else [None]
    if None in m:
        fault("kt_c TSV: a malformed line or no final newline")
    rows = [(int(x[1]), x[2]) for x in m]
    n = cfg["expect"]["kt_c"]
    if len(rows) != n:
        fault(f"kt_c TSV has {len(rows)} rows, not {n}")
    ids = {i for i, _ in rows}
    if len(ids) != n or len({f for _, f in rows}) != n:
        fault("kt_c TSV ids or names are not unique")
    rb = pinned(cfg["paths"]["record"], cfg["pins"]["record"])
    rec = mod.read_rec(types.SimpleNamespace(name="coco_test.sha256.tsv", exists=lambda: True, read_text=rb.decode))
    if len(rec) != cfg["expect"]["record_rows"]:
        fault(f"record rows {len(rec)}, not {cfg['expect']['record_rows']}")
    doc = json.loads(pinned(cfg["paths"]["owners"], cfg["pins"]["owners"]))["owners"]
    own = {int(x[0] if isinstance(x, list) else x) for o in KT_C_OUT for x in doc[o]["ids"]}  # c_pvr_run ids_of form
    if ids != set(rec) - own:
        fault(f"H6-AM1: TSV ids != record ids minus the KT_C_OUT owners ({len(ids & own)} owner id(s) in the TSV, "
              f"{len(ids - set(rec))} outside the record, {len(set(rec) - own - ids)} missing)")
    plan = []
    for i, f in rows:
        if rec[i][1] != f:
            fault("a TSV (id, name) pair is not the record's")
        try:
            url = mod.url_ok("coco_test", (i, f, mod.COCO_URL.format(filepath="val2014", file=f), ""))
        except SystemExit:
            fault("a TSV name breaks the url_ok rule (COCO_val2014_<id:012d>.jpg)")
        if url != URL_BASE + f:
            fault("a url is not the plan §5 url")
        plan.append((i, f, rec[i][2], int(rec[i][3]), url))
    total = sum(r[3] for r in plan)
    if total != cfg["expect"]["bytes"]:
        fault(f"bytes total {total} != {cfg['expect']['bytes']}")
    return {"mod": mod, "plan": plan, "total": total, "k": k, "man": man, "part": part,
            "report": {"kt_c": len(plan), "record_rows": len(rec), "owners_in_record": len(set(rec) & own),
                       "tsv_ids_eq_record_minus_owners": True, "bytes": total, "out": str(k), "manifest": str(man),
                       "pins": {**{x: s[:8] for x, s in cfg["pins"].items()}, "qtsv": cfg["qtsv"][:8],
                                "tsv": tsv_sha[:8]}}}


def opener() -> urllib.request.OpenerDirector:
    """No proxy from the environment; User-Agent vsps-research and no other header (no e-mail). Installed globally
    in the real run, so cen_fetch.OPEN (= urllib.request.urlopen, never replaced there; H6-AM2) uses it."""
    o = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    o.addheaders = [("User-Agent", UA)]
    return o


def check(i: int, b: bytes, s: str, n: int, mod) -> None:
    """Plan §7.1: in memory, before any write."""
    bad = "sha" if mod.sha_bytes(b) != s else "bytes" if len(b) != n else ""
    if bad:
        stop(f"id {i} utc {utc()} {bad}; nothing written")


def keep(k: Path, f: str, b: bytes, s: str, mod, i: int) -> None:
    """Plan §7.2/§7.4: O_EXCL 0600 tmp, fsync, rename, re-hash from disk; a mismatch gets one unlink of that file."""
    tmp = k / f".tmp_{f}"
    with os.fdopen(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as fh:
        fh.write(b)
        fh.flush()
        os.fsync(fh.fileno())
    os.chmod(tmp, 0o600)
    os.replace(tmp, k / f)
    if mod.sha_file(k / f) != s:
        os.unlink(k / f)
        stop(f"id {i} utc {utc()} on-disk sha; that file was removed")


def write_manifest(dst: Path, done: dict, final: bool) -> str:
    """'<sha256>  <name>' per kept file, sorted by name (LC_ALL=C order). The final one never overwrites (H6-AM3)."""
    data = "".join(f"{s}  {f}\n" for f, s in sorted(done.items())).encode("ascii")
    tmp = dst.with_name(dst.name + ".tmp")
    with os.fdopen(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.chmod(tmp, 0o600)
    if final:
        os.link(tmp, dst)
        os.unlink(tmp)
    else:
        os.replace(tmp, dst)
    d = os.open(dst.parent, os.O_RDONLY)
    os.fsync(d)
    os.close(d)
    return sha(data)


def resume_scan(mod, k: Path, want: dict) -> dict:
    """CC-281 O1: every file in K re-hashed against the record before any request; a stray .tmp_<name> gets one
    unlink; anything else unlisted or different is a STOP."""
    done = {}
    for p in sorted(os.listdir(k)):
        if p.startswith(".tmp_") and p[5:] in want:
            os.unlink(k / p)
            print("resume: removed one stray .tmp file", flush=True)
        elif p not in want:
            stop("resume: K holds a file outside the TSV; to the judge")
        elif mod.sha_file(k / p) != want[p][1] or os.stat(k / p).st_size != want[p][2]:
            stop("resume: a kept file differs from the record; to the judge")
        else:
            done[p] = want[p][1]
    print(f"resume: {len(done)} kept files re-hashed OK", flush=True)
    return done


def fetch_run(pre: dict, ruling: str | None = None) -> dict:
    """Plan §5-§9. Sequential, one get per name, no second pass. Any failure = STOP; the verified files stay."""
    mod, plan, k, man, part = pre["mod"], pre["plan"], pre["k"], pre["man"], pre["part"]
    want = {f: (i, s, n) for i, f, s, n, _ in plan}
    start, done, complete = utc(), {}, False
    if ruling is None:
        try:
            os.mkdir(k, 0o700)
        except FileExistsError:
            stop("K appeared after the absence guard; nothing fetched")
        os.chmod(k, 0o700)
    else:
        if not RULING.fullmatch(ruling):
            fault("resume needs --ruling CC-<n> (CC-281 O1)")
        done = resume_scan(mod, k, want)
    urllib.request.install_opener(opener())
    try:
        for i, f, s, n, url in plan:
            if f in done:
                continue
            b, err = mod.get(url)
            if b is None:
                stop(f"id {i} utc {utc()} {err}; STOP and PI (CC-280 3(h)), no substitute image")
            check(i, b, s, n, mod)
            keep(k, f, b, s, mod, i)
            done[f] = s
            if len(done) % EVERY == 0:
                print(f"fetched {len(done)}/{len(plan)} failed 0", flush=True)
        if sorted(os.listdir(k)) != sorted(want):
            stop("K does not hold exactly the TSV names")
        if sum(os.stat(k / f).st_size for f in want) != pre["total"]:
            stop("the kept bytes differ from the preflight total")
        msha = write_manifest(man, done, final=True)
        complete = True
    except SystemExit:
        raise
    except BaseException as e:  # plan §8: class name only, no traceback
        raise SystemExit(f"STOP: {type(e).__name__} at {utc()}") from None
    finally:
        if not complete:
            write_manifest(part, done, final=False)
    if ruling is not None:
        os.unlink(part)
        print("resume: removed the .partial manifest", flush=True)
    return {"count": len(done), "bytes": pre["total"], "manifest": str(man), "manifest_sha256": msha,
            "start_utc": start, "end_utc": utc(), "failed": 0, "ruling": ruling,
            "script_sha256": sha(Path(__file__).read_bytes())}


class Resp:
    def __init__(self, body: bytes, url: str, status: int):
        self.body, self.url, self.status = body, url, status

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self):
        return self.body

    def geturl(self):
        return self.url


def selftest() -> None:
    """Synthetic record/owners/TSV fixtures and a fake cen_fetch.OPEN (its own test hook); any socket use fails."""
    import socket

    def blocked(*a, **kw):
        raise AssertionError("selftest: network call")
    socket.create_connection = blocked
    t = Path(tempfile.mkdtemp(prefix="c_pvr_ktc_st_"))
    if fstype(t) != "ext4":
        raise SystemExit("selftest needs TMPDIR on ext4")
    cen = load_cen(ROOT / P["cen_fetch"][0], P["cen_fetch"][1])
    assert cen.RECORD_PINS["coco_test"] == P["record"][1]
    assert cen.COCO_URL.format(filepath="val2014", file="x") == URL_BASE + "x" and cen.OPEN is urllib.request.urlopen

    ids = range(11, 19)  # 11/12/13 = the three KT_C_OUT owners, 14 also a non-KT_C_OUT owner key, 14-18 = kt_c
    body = {i: b"\xff\xd8" + f"img{i}".encode() * (i - 9) for i in ids}
    name = {i: f"COCO_val2014_{i:012d}.jpg" for i in ids}
    KT = [(i, name[i]) for i in range(14, 19)]
    total = sum(len(body[i]) for i, _ in KT)
    own = {"owners": {"uitviic_train_pool": {"ids": [11]}, "m0_dev_touched_3454": {"ids": [[12, "x"]]},
                      "a_t3_val2017": {"ids": [13]}, "other_owner": {"ids": [14]}}}

    def put(p: Path, data: bytes) -> str:
        p.write_bytes(data)
        return sha(data)

    def rec_text(names=name, nbytes=None) -> bytes:
        nb = nbytes or {}
        return "".join(f"{i}\t{names[i]}\t{sha(body[i])}\t{nb.get(i, len(body[i]))}\n" for i in ids).encode()

    def cfg(rec: bytes | None = None, **exp) -> dict:
        d = Path(tempfile.mkdtemp(dir=t))
        c = {"paths": {"cen_fetch": ROOT / P["cen_fetch"][0], "record": d / "coco_test.sha256.tsv",
                       "owners": d / "owners.json"},
             "pins": {"cen_fetch": P["cen_fetch"][1]}, "expect": {"record_rows": 8, "kt_c": 5, "bytes": total, **exp}}
        c["pins"]["record"] = put(c["paths"]["record"], rec_text() if rec is None else rec)
        c["pins"]["owners"] = put(c["paths"]["owners"], json.dumps(own).encode())
        return c

    def tsv(c: dict, rows: list) -> tuple:
        d = Path(tempfile.mkdtemp(dir=t))
        s = put(d / "kt_c.tsv", "".join(f"{i}\t{f}\n" for i, f in rows).encode())
        c["qtsv"] = put(d / "QTSV.sha256", f"{'0' * 64}  other.tsv\n{s}  kt_c.tsv\n".encode())
        return d / "kt_c.tsv", s

    calls = []

    def server(beh: dict):
        seen = {}

        def fake(url, timeout=None):
            calls.append(url)
            seen[url] = seen.get(url, 0) + 1
            kind = beh.get(int(url[-16:-4]), "ok")
            if kind == "net" or (kind == "flaky" and seen[url] < 3):
                raise OSError("down")
            if kind == "kbd":
                raise KeyboardInterrupt
            b = {"badsha": b"\xff\xd8junk", "notjpeg": b"GIF89a"}.get(kind, body[int(url[-16:-4])])
            return Resp(b, url + "?moved" if kind == "redirect" else url, 404 if kind == "404" else 200)
        return fake

    def run(c: dict, rows: list, out: Path, beh=None, ruling=None, tsv_sha=None, hook=None) -> dict:
        f, s = tsv(c, rows)
        pre = preflight(c, f, tsv_sha or s, out, resume=ruling is not None)
        pre["mod"].OPEN = server(beh or {})
        if hook:
            hook(pre)
        return fetch_run(pre, ruling)

    def refused(tag: str, needle: str, fn) -> str:
        try:
            fn()
        except SystemExit as e:
            assert needle in str(e), (tag, str(e))
            return str(e)
        raise AssertionError(f"{tag}: no FAULT/STOP")

    def mode(p: Path) -> int:
        return os.stat(p).st_mode & 0o777

    def lines(p: Path) -> list:
        return p.read_text().splitlines()

    # positive: preflight writes nothing; fetch requests exactly the 5 TSV urls once each, in TSV order
    KS = [KT[2], KT[0], KT[4], KT[1], KT[3]]  # TSV order != name order: the manifest is still sorted
    c = cfg()
    f, s = tsv(c, KS)
    snap = sorted(os.listdir(t))
    pre = preflight(c, f, s, t / "ok")
    assert sorted(os.listdir(t)) == snap and pre["report"]["owners_in_record"] == 3, pre["report"]
    calls.clear()
    pre["mod"].OPEN = server({})
    os.environ["http_proxy"] = os.environ["https_proxy"] = "http://proxy.invalid"
    r = fetch_run(pre)
    g = urllib.request._opener  # the global opener cen_fetch.OPEN (urlopen) uses in the real run
    assert g is not None and g.addheaders == [("User-Agent", UA)], g
    assert not [h for h in g.handlers if isinstance(h, urllib.request.ProxyHandler)]
    assert calls == [URL_BASE + n for _, n in KS], calls
    assert sorted(os.listdir(t / "ok")) == [n for _, n in KT] and mode(t / "ok") == 0o700
    assert all(mode(t / "ok" / n) == 0o600 and (t / "ok" / n).read_bytes() == body[i] for i, n in KT)
    man = t / "ok.sha256"
    assert man.read_text() == "".join(f"{sha(body[i])}  {name[i]}\n" for i, _ in KT) and mode(man) == 0o600
    assert (r["count"], r["bytes"], r["failed"], r["manifest_sha256"]) == (5, total, 0, sha(man.read_bytes())), r
    assert not os.path.lexists(t / "ok.sha256.partial") and not os.path.lexists(t / "ok.sha256.tmp")

    # flaky: two errors then a body, inside get's own 3 tries -> kept
    calls.clear()
    run(cfg(), KT, t / "flaky", {15: "flaky"})
    assert calls.count(URL_BASE + name[15]) == 3 and len(lines(t / "flaky.sha256")) == 5

    # preflight refusals: nothing created, no request
    refused("exists", "FAULT: K exists (absence guard", lambda: run(cfg(), KT, t / "ok"))
    (t / "m1.sha256").write_text("")
    (t / "m2.sha256.partial").write_text("")
    refused("man_exists", "H6-AM3", lambda: run(cfg(), KT, t / "m1"))
    refused("partial_exists", "H6-AM3", lambda: run(cfg(), KT, t / "m2"))
    n18 = [(i, n) for i, n in KT[:4]]

    def bad_tsv_bytes():
        c2 = cfg()
        f2, s2 = tsv(c2, KT)
        f2.write_bytes(f2.read_bytes() + b"19\tCOCO_val2014_000000000019.jpg\n")
        preflight(c2, f2, s2, t / "x_tsvbytes")

    def pin_off(key: str) -> dict:
        c2 = cfg()
        c2["pins"][key] = "0" * 64
        return c2

    def eio() -> dict:
        c2 = cfg()
        c2["paths"]["record"] = t
        return c2
    names_train = {**name, 14: "COCO_train2014_000000000014.jpg"}
    calls.clear()
    for tag, needle, fn in (
            ("proc_fs", "ext4", lambda: run(cfg(), KT, Path("/proc/c_pvr_ktc_x"))),
            ("barred", "barred", lambda: run(cfg(), KT, t / "t2pool_x")),
            ("tsv_sha_not_qtsv", "QTSV", lambda: run(cfg(), KT, t / "x_tsvsha", tsv_sha="0" * 64)),
            ("tsv_bytes", "kt_c.tsv differs", bad_tsv_bytes),
            ("qtsv_pin", "QTSV.sha256 differs", lambda: preflight({**cfg(), "qtsv": "0" * 64}, *tsv(cfg(), KT),
                                                                    t / "x_qtsv")),
            ("record_pin", "coco_test.sha256.tsv differs", lambda: run(pin_off("record"), KT, t / "x_rec")),
            ("owners_pin", "owners.json differs", lambda: run(pin_off("owners"), KT, t / "x_own")),
            ("cen_pin", "cen_fetch.py differs", lambda: run(pin_off("cen_fetch"), KT, t / "x_cen")),
            ("record_eio", "read failed (IsADirectoryError)", lambda: run(eio(), KT, t / "x_eio")),
            ("rows", "4 rows", lambda: run(cfg(), n18, t / "x_rows")),
            ("all_record_rows", "8 rows", lambda: run(cfg(), [(i, name[i]) for i in ids], t / "x_all")),
            ("dup", "not unique", lambda: run(cfg(), KT[:4] + [KT[3]], t / "x_dup")),
            ("owner_swap", "H6-AM1: TSV ids != record ids minus the KT_C_OUT owners (1 owner",
             lambda: run(cfg(), KT[:4] + [(13, name[13])], t / "x_swap")),
            ("pair", "not the record's", lambda: run(cfg(), [(14, name[18])] + KT[1:4] + [(18, name[14])],
                                                     t / "x_pair")),
            ("url_rule", "url_ok rule", lambda: run(cfg(rec_text(names_train)),
                                                    [(14, names_train[14])] + KT[1:], t / "x_url")),
            ("bytes_total", "bytes total", lambda: run(cfg(bytes=total + 1), KT, t / "x_total")),
            ("record_rows", "record rows", lambda: run(cfg(record_rows=9), KT, t / "x_recrows")),
            ("malformed", "malformed", lambda: run(cfg(), [("#id", "image")] + KT[:4], t / "x_mal"))):
        assert refused(tag, needle, fn).startswith("FAULT"), tag
    assert calls == [] and not [x for x in os.listdir(t) if x.startswith("x_")], os.listdir(t)

    # fetch STOPs: the failing name is never kept, later names are never requested, .partial lists the kept ones
    def stopped(tag: str, needle: str, beh=None, c=None, hook=None, kept=2) -> Path:
        out = t / tag
        calls.clear()
        refused(tag, needle, lambda: run(c or cfg(), KT, out, beh, hook=hook))
        assert sorted(os.listdir(out)) == [n for _, n in KT[:kept]], (tag, os.listdir(out))
        assert len(lines(t / f"{tag}.sha256.partial")) == kept and not os.path.lexists(t / f"{tag}.sha256"), tag
        assert not {URL_BASE + name[17], URL_BASE + name[18]} & set(calls), tag
        return out

    s404 = stopped("s404", "STOP: id 16 utc", {16: "404"})
    assert calls.count(URL_BASE + name[16]) == 3 and "status 404" in refused("s404b", "404", lambda: run(
        cfg(), KT, t / "s404b", {16: "404"}))
    snet = stopped("snet", "OSError; STOP and PI", {16: "net"})
    assert calls.count(URL_BASE + name[16]) == 3
    stopped("sredir", "redirected", {16: "redirect"})
    stopped("snotjpeg", "not a JPEG body", {16: "notjpeg"})
    stopped("ssha", "id 16 utc", {16: "badsha"})
    assert "sha; nothing written" in refused("ssha2", "sha;", lambda: run(cfg(), KT, t / "ssha2", {16: "badsha"}))
    stopped("sbytes", "bytes; nothing written", c=cfg(rec_text(nbytes={16: len(body[16]) + 1}),
                                                       bytes=total + 1))
    skbd = stopped("skbd", "STOP: KeyboardInterrupt", {16: "kbd"})

    def ondisk(pre):
        orig = pre["mod"].sha_file
        pre["mod"].sha_file = lambda p: "0" * 64 if Path(p).name == name[16] else orig(p)
    stopped("sdisk", "on-disk sha", hook=ondisk)
    refused("appeared", "appeared", lambda: run(cfg(), KT, t / "app", hook=lambda pre: os.mkdir(t / "app")))
    assert os.listdir(t / "app") == [] and not os.path.lexists(t / "app.sha256.partial")
    refused("man_race", "STOP: FileExistsError", lambda: run(cfg(), KT, t / "race",
                                                            hook=lambda pre: (t / "race.sha256").write_text("")))
    assert (t / "race.sha256").read_text() == "" and len(lines(t / "race.sha256.partial")) == 5

    def at_last(act):  # runs act(K) when the last TSV name is requested (plan §7.5 end checks)
        def hook(pre):
            orig = pre["mod"].OPEN

            def w(url, timeout=None):
                if url.endswith(name[18]):
                    act(pre["k"])
                return orig(url, timeout)
            pre["mod"].OPEN = w
        return hook
    refused("end_extra", "exactly the TSV names", lambda: run(cfg(), KT, t / "e1", hook=at_last(
        lambda k: (k / "extra.jpg").write_bytes(b"x"))))
    refused("end_bytes", "kept bytes differ", lambda: run(cfg(), KT, t / "e2", hook=at_last(
        lambda k: (k / name[14]).write_bytes(b"\xff\xd8"))))
    assert not os.path.lexists(t / "e1.sha256") and len(lines(t / "e2.sha256.partial")) == 5

    # resume (CC-281 O1): ruled only; re-hash K, drop a stray tmp, fetch only the rest, final manifest, .partial gone
    (s404 / f".tmp_{name[16]}").write_bytes(b"\xff\xd8torn")
    calls.clear()
    r = run(cfg(), KT, s404, ruling="CC-999")
    assert calls == [URL_BASE + name[i] for i in (16, 17, 18)] and r["count"] == 5 and r["ruling"] == "CC-999"
    assert sorted(os.listdir(s404)) == [n for _, n in KT] and len(lines(t / "s404.sha256")) == 5
    assert not os.path.lexists(t / "s404.sha256.partial") and (t / "s404.sha256").read_text() == man.read_text()
    (snet / "stray.jpg").write_bytes(b"x")
    (skbd / name[14]).write_bytes(b"\xff\xd8tampered")
    calls.clear()
    for tag, needle, out, ru in (("ruling_form", "--ruling", t / "snotjpeg", "PI-1"),
                                 ("resume_no_k", "resume needs K", t / "nok", "CC-999"),
                                 ("resume_complete", "resume needs K", t / "ok", "CC-999"),
                                 ("resume_unlisted", "outside the TSV", snet, "CC-999"),
                                 ("resume_tampered", "differs from the record", skbd, "CC-999")):
        refused(tag, needle, lambda: run(cfg(), KT, out, ruling=ru))
    assert calls == [] and (t / "snotjpeg.sha256.partial").exists() and len(lines(t / "skbd.sha256.partial")) == 2

    # opener: proxy env ignored (an empty ProxyHandler registers nothing and replaces the env one), UA only header
    os.environ["http_proxy"] = os.environ["https_proxy"] = "http://proxy.invalid"
    o = opener()
    ph = [h for h in o.handlers if isinstance(h, urllib.request.ProxyHandler)]
    assert ph == [] and o.addheaders == [("User-Agent", UA)], ([h.proxies for h in ph], o.addheaders)


def main(argv: list) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    for c in ("preflight", "fetch", "resume"):
        p = sp.add_parser(c)
        p.add_argument("--tsv", required=True, type=Path)
        p.add_argument("--tsv-sha", required=True)
        p.add_argument("--out", required=True, type=Path)
        if c == "resume":
            p.add_argument("--ruling", required=True)
    x = ap.parse_args(argv[1:])
    if x.cmd == "selftest":
        selftest()
        print("selftest ok")
        return 0
    pre = preflight(real_cfg(), x.tsv, x.tsv_sha, x.out, resume=x.cmd == "resume")
    print(json.dumps({"preflight": "ok", "network": "none so far", **pre["report"]}, sort_keys=True), flush=True)
    if x.cmd == "preflight":
        return 0
    print(json.dumps(fetch_run(pre, x.ruling if x.cmd == "resume" else None), sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
