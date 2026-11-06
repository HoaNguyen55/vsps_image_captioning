#!/usr/bin/env python3
"""C-PVR-T1 a1_decomp watcher (Paper C, H5; CC-270r2 N-S11a/b, N5'; CC-277 Ruling 7; CC-280 Ruling 6). LAPTOP ONLY:
one process, started by the coordinator in the same step as `c_pvr_job.sh tier1`; no agent after launch.

    PY=~/.venvs/c_pvr/bin/python    (VnCoreNLP for the VI sets, spaCy for t_a / kt_c: the builder's decomposers)
    setsid nohup $PY -I -B scripts/c_pvr_gpu/c_pvr_watch.py run --ssh ALIAS --work W --build O --tman SHA \\
        --start UTC --log LOG.md > /dev/null 2>&1 &
    $PY -I -B scripts/c_pvr_gpu/c_pvr_watch.py selftest

Every EVERY s, for each source (A1 on the 5 VI sets, S3 on kt_c: c_pvr_gpu A8_SRC) without a local decomposition:
its host marker c_pvr_out/logs/tier1.<set>.<arm>.done, once present, must not be older than --start (the job's start
stamp; an older marker is a FAULT, never re-processed); c_pvr_out/out/<set>.<arm>.jsonl is pulled and checked against
its host-side sha256; a torn last line is dropped and logged by id (CC-270 N11); the ids must equal the sealed
manifest's query ids of the set (O/manifest/<set>.json, sha-checked against O/MANIFEST.sha256 = --tman); the
captions are decomposed by the set's datastore rule (as the builder: decompose_vi for D-VI, else decompose_en) and
W/a1_decomp/<set>.json is written atomically. When all 6 exist: W/a1_decomp/MANIFEST.sha256 ('<sha256>  <basename>'),
then ONE OPS line, BEFORE any push (fsynced ext4 side file W/ops_side.log first, then O_APPEND to LOG.md in one
write; a LOG.md error, e.g. /mnt/d EIO, leaves the side-file record, which counts and is copied later: CC-280 Ruling
6(a)), then the push: each file to <hc>/a1_decomp/<f>.tmp, sha-checked there, renamed on the same tmpfs,
MANIFEST.sha256 last. W/heartbeat is rewritten every loop (the 30-min backup loop flags an age > 5 min: Ruling 6(b));
any error -> W/FAULT and rc 1 (the host then waits A8_WAIT_SEC and STOPs: PI). --ssh is an ~/.ssh/config alias: no
host, IP or port is written. Logs hold ids and counts only.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c_pvr_gpu as G  # noqa: E402  SETS, A8_SRC, load() (c_pvr behind its pin), guard, fault
import c_pvr_manifest as B  # noqa: E402  put (temp, fsync, rename), jbytes

EVERY = 60  # [proposal] seconds between polls (plan §6.3); A8_WAIT_SEC = 1800 covers pull + decompose + push
HC = "/dev/shm/c_pvr_hc"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


SRC = {s: G.A8_SRC["S2" if "S2" in arms else "A8"] for s, (_, _, arms) in G.SETS.items()}  # CC-270r2 N5'


class Remote:
    """One primitive: run a shell command in the host's home dir, bytes in and out; rc != 0 is a FAULT."""

    def __init__(self, argv: list, cwd=None):
        self.argv, self.cwd = argv, cwd

    def sh(self, cmd: str, data: bytes = b"") -> bytes:
        r = subprocess.run([*self.argv, cmd], input=data, capture_output=True, timeout=600, cwd=self.cwd)
        if r.returncode:
            G.fault(f"remote command rc {r.returncode}: {cmd.split()[0]}")
        return r.stdout


def query_ids(build: Path, tman: str) -> dict:
    """{set: [query ids]} from the sealed laptop manifests, each checked against the arrival MANIFEST.sha256."""
    man = G.guard(build / "MANIFEST.sha256").read_bytes()
    if sha(man) != tman:
        G.fault("MANIFEST.sha256 differs from --tman")
    want = {p: h for h, p in (x.split("  ", 1) for x in man.decode().splitlines())}
    out = {}
    for s in SRC:
        b = (build / "manifest" / f"{s}.json").read_bytes()
        if want.get(f"manifest/{s}.json") != sha(b):
            G.fault(f"manifest/{s}.json differs from MANIFEST.sha256")
        out[s] = [q["id"] for q in json.loads(b)["queries"]]
    return out


def say(w: Path, msg: str) -> None:
    with open(w / "watch.log", "a") as f:
        f.write(f"{utc()} {msg}\n")


def pull(R: Remote, w: Path, s: str, arm: str, qids: list, start: str, decompose) -> bool:
    """One source: False while its marker is absent; else the checked, decomposed W/a1_decomp/<set>.json."""
    mk = R.sh(f"cat c_pvr_out/logs/tier1.{s}.{arm}.done 2>/dev/null || true").decode().strip()
    if not mk:
        return False
    if mk < start:
        G.fault(f"tier1.{s}.{arm}.done {mk} is older than the job start {start}: a stale marker")
    f = f"c_pvr_out/out/{s}.{arm}.jsonl"
    want = R.sh(f"sha256sum {shlex.quote(f)}").split()[0].decode()
    b = R.sh(f"cat {shlex.quote(f)}")
    if sha(b) != want:
        G.fault(f"{s}.{arm}.jsonl differs from the host sha256")
    lines = b.decode().split("\n")
    if lines[-1]:  # no final newline: a torn last line (CC-270 N11), dropped and logged by id
        m = re.search(r'"id": *"([A-Za-z0-9_.:+-]{1,80})"', lines[-1])
        say(w, f"{s}.{arm}: torn last line dropped, id {m.group(1) if m else 'unparsed'}")
    rows = [json.loads(x) for x in lines[:-1]]
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)) or set(ids) != set(qids):
        G.fault(f"{s}.{arm}: output ids differ from the manifest query ids ({len(set(ids))} vs {len(qids)})")
    dcs = decompose(G.SETS[s][0], [r["caption"] for r in rows])
    B.put(w / "a1_decomp" / f"{s}.json", B.jbytes(dict(zip(ids, dcs))))
    say(w, f"{s}.{arm}: {len(ids)} decomposed, {sum('decomp_fail' in d for d in dcs)} decomp_fail")
    return True


def ops(w: Path, log: Path, line: str) -> str:
    """The OPS line: the fsynced ext4 side file first, then LOG.md by one O_APPEND write; LOG.md may fail (EIO)."""
    fd = os.open(w / "ops_side.log", os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try:
        os.write(fd, line.encode())
        os.fsync(fd)
    finally:
        os.close(fd)
    try:
        fd = os.open(log, os.O_WRONLY | os.O_APPEND)
        try:
            os.write(fd, line.encode())
        finally:
            os.close(fd)
        return "LOG.md"
    except OSError as e:
        say(w, f"LOG.md not written ({type(e).__name__}); the side-file record stands (CC-280 Ruling 6(a))")
        return "side"


def push(R: Remote, w: Path, hc: str, log: Path) -> None:
    d = w / "a1_decomp"
    names = sorted(f"{s}.json" for s in SRC)
    man = "".join(f"{sha((d / n).read_bytes())}  {n}\n" for n in names).encode()
    h = B.put(d / "MANIFEST.sha256", man)
    line = (f"{utc()} OPS-{time.strftime('%m%d', time.gmtime())}c-a1decomp: a1_decomp MANIFEST.sha256 {h} "
            f"({len(names)} files: {', '.join(names)}); watcher c_pvr_watch.py {sha(Path(__file__).read_bytes())}; "
            f"pushed next to {hc}/a1_decomp, MANIFEST last (CC-270r2 N-S11a, CC-280 Ruling 6)\n")
    say(w, f"OPS line written ({ops(w, log, line)}); push starts")
    R.sh(f"mkdir -p -m 700 {shlex.quote(hc)}/a1_decomp")
    for n in [*names, "MANIFEST.sha256"]:
        b, dst = (d / n).read_bytes(), shlex.quote(f"{hc}/a1_decomp/{n}")
        R.sh(f"cat > {dst}.tmp", b)
        if R.sh(f"sha256sum {dst}.tmp").split()[0].decode() != sha(b):
            G.fault(f"{n}: pushed bytes differ")
        R.sh(f"mv -f {dst}.tmp {dst}")
    (w / "PUSHED").write_text(f"{utc()}\n")
    say(w, "push done")


def beat(w: Path, msg: str) -> None:
    t = w / "heartbeat.tmp"
    t.write_text(f"{utc()} {msg}\n")
    os.replace(t, w / "heartbeat")


def lock(w: Path) -> int:
    fd = os.open(w / ".lock", os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        G.fault("another watcher holds the lock")
    return fd


def workdir(w: Path) -> Path:
    if str(w.resolve()).startswith("/mnt/"):
        G.fault("the work dir must sit on ext4")
    if not w.exists():
        w.mkdir(parents=True)
        w.chmod(0o700)
    if w.stat().st_mode & 0o777 != 0o700:
        G.fault("the work dir is not 0700")
    (w / "a1_decomp").mkdir(exist_ok=True)
    return w


def run(R: Remote, w: Path, build: Path, tman: str, start: str, log: Path, decompose, hc: str = HC, every: int = EVERY,
        sleep=time.sleep, loops: int = 0) -> int:
    """loops = 0: until pushed. Any error -> W/FAULT, rc 1."""
    fd = None
    try:
        fd = lock(workdir(w))  # held until the watcher ends
        say(w, f"start c_pvr_watch.py {sha(Path(__file__).read_bytes())} job start {start}")
        qids, n = query_ids(build, tman), 0
        while not (w / "PUSHED").exists():
            done = [s for s, a in SRC.items() if (w / "a1_decomp" / f"{s}.json").exists()
                    or pull(R, w, s, a, qids[s], start, decompose)]
            beat(w, f"{len(done)}/{len(SRC)} decomposed")
            if len(done) == len(SRC):
                push(R, w, hc, log)
                break
            n += 1
            if loops and n >= loops:
                return 2
            sleep(every)
        beat(w, "pushed")
        return 0
    except (SystemExit, Exception) as e:  # noqa: BLE001  every error stops the watcher loudly
        (w / "FAULT").write_text(f"{utc()} {type(e).__name__}: {e}\n")
        return 1
    finally:
        if fd is not None:
            os.close(fd)


def decomposer(ds: str, texts: list) -> list:
    return G.CP.decompose_vi(texts, G.ROOT) if ds == "d_vi" else G.CP.decompose_en(texts, G.ROOT)


# ---------------------------------------------------------------------------------------------- selftest
class _Spy(Remote):
    """The fake host: bash in a local dir. Checks the push protocol as it happens."""

    def __init__(self, home: Path, w: Path, corrupt: bool = False):
        super().__init__(["bash", "-c"], home)
        self.w, self.corrupt, self.cmds = w, corrupt, []

    def sh(self, cmd: str, data: bytes = b"") -> bytes:
        self.cmds.append(cmd)
        if cmd.startswith("cat > "):
            assert cmd.endswith(".tmp"), "a push writes a temp name first"
            assert "c-a1decomp" in (self.w / "ops_side.log").read_text(), "the OPS line precedes the push"
        out = super().sh(cmd, data)
        return out + b"\n" if self.corrupt and cmd.startswith("cat c_pvr_out/out/") else out


def selftest() -> None:
    import tempfile

    G.load()
    assert SRC == {"xm3600_vi": "A1", "ktvic_explore": "A1", "openviic_explore": "A1", "vitextvqa_dev": "A1",
                   "t_a": "A1", "kt_c": "S3"}
    seen = []

    def dec(ds, texts):
        seen.append(ds)
        return [G._dc(t, [t.split()[0]]) for t in texts]
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        home, hc, build = t / "home", t / "hc", t / "build"
        (home / "c_pvr_out/logs").mkdir(parents=True)
        (home / "c_pvr_out/out").mkdir()
        hc.mkdir(mode=0o700)
        (build / "manifest").mkdir(parents=True)
        qids, lines = {s: [f"{s[:2]}q{j}" for j in range(3)] for s in SRC}, []
        for s, ids in qids.items():
            b = json.dumps({"queries": [{"id": i} for i in ids]}).encode()
            (build / "manifest" / f"{s}.json").write_bytes(b)
            lines.append(f"{sha(b)}  manifest/{s}.json\n")
        (build / "MANIFEST.sha256").write_text("".join(lines))
        tman = sha((build / "MANIFEST.sha256").read_bytes())
        log = t / "LOG.md"
        log.write_text("x\n")
        start = "2026-11-07T00:00:00Z"

        def host(s, ids, mark=start, tail=""):
            body = "".join(json.dumps({"id": i, "caption": f"Cap {i} ok"}) + "\n" for i in ids) + tail
            (home / f"c_pvr_out/out/{s}.{SRC[s]}.jsonl").write_text(body)
            (home / f"c_pvr_out/logs/tier1.{s}.{SRC[s]}.done").write_text(mark + "\n")

        def go(name, R=None, loops=1):
            w = t / name
            return w, run(R or _Spy(home, w), w, build, tman, start, log, dec, str(hc), 0, lambda _s: None, loops)

        w, rc = go("w0")
        assert rc == 2 and not list((w / "a1_decomp").iterdir()) and "0/6" in (w / "heartbeat").read_text()
        host("xm3600_vi", qids["xm3600_vi"], mark="2026-11-06T23:59:59Z")
        w, rc = go("w1")
        assert rc == 1 and "stale marker" in (w / "FAULT").read_text()
        host("xm3600_vi", qids["xm3600_vi"])
        w, rc = go("w2", _Spy(home, t / "w2", corrupt=True))
        assert rc == 1 and "differs from the host sha256" in (w / "FAULT").read_text()
        host("xm3600_vi", qids["xm3600_vi"][:2])
        w, rc = go("w3")
        assert rc == 1 and "ids differ" in (w / "FAULT").read_text()
        for s, ids in qids.items():
            host(s, ids, tail='{"id": "' + ids[0] + '", "capt' if s == "t_a" else "")  # a torn resumed line on t_a
        (t / "w4").mkdir(mode=0o700)
        lk = os.open(t / "w4" / ".lock", os.O_CREAT | os.O_RDWR)
        fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
        w, rc = go("w4")
        assert rc == 1 and "another watcher" in (w / "FAULT").read_text()
        os.close(lk)
        R = _Spy(home, t / "w5")
        w, rc = go("w5", R)
        assert rc == 0 and (w / "PUSHED").exists() and "pushed" in (w / "heartbeat").read_text(), rc
        assert sorted(seen[-6:]) == sorted(G.SETS[s][0] for s in SRC)  # the datastore's decomposer, per set
        assert "t_a.A1: torn last line dropped, id t_q0" in (w / "watch.log").read_text()
        pushed = [c.split()[2] for c in R.cmds if c.startswith("cat > ")]
        assert pushed[-1].endswith("MANIFEST.sha256.tmp") and len(pushed) == 7, pushed  # the manifest last
        side = (w / "ops_side.log").read_text()
        assert side.count("c-a1decomp") == 1 and log.read_text().endswith(side) and log.read_text().startswith("x\n")
        got = sorted(os.listdir(hc / "a1_decomp"))
        assert got == sorted([f"{s}.json" for s in SRC] + ["MANIFEST.sha256"]), got
        for s in SRC:  # the host's own reader accepts the push
            dc, _ = G.a1_decomp(hc / "a1_decomp" / f"{s}.json", set(qids[s]), lambda: 0, lambda _s: None)
            assert sorted(dc) == sorted(qids[s]) and dc[qids[s][0]]["text"] == f"Cap {qids[s][0]} ok"
        assert all(x.startswith("cat ") or x.startswith(("sha256sum", "mkdir", "mv -f")) for x in R.cmds)
        w, rc = go("w5")
        assert rc == 0 and len([c for c in R.cmds if c.startswith("cat > ")]) == 7  # pushed once: a restart is a no-op
        for f in os.listdir(hc / "a1_decomp"):
            os.unlink(hc / "a1_decomp" / f)
        log2 = t / "LOGDIR"
        log2.mkdir()  # LOG.md unwritable (an EIO stand-in): the side file holds the line, the push goes on
        w = t / "w6"
        rc = run(_Spy(home, w), w, build, tman, start, log2, dec, str(hc), 0, lambda _s: None, 1)
        assert rc == 0 and "c-a1decomp" in (w / "ops_side.log").read_text() and "side-file record" in (
            w / "watch.log").read_text() and len(os.listdir(hc / "a1_decomp")) == 7
        rc = run(_Spy(home, t / "w7"), t / "w7", build, "0" * 64, start, log, dec, str(hc), 0, lambda _s: None, 1)
        assert rc == 1 and "differs from --tman" in (t / "w7" / "FAULT").read_text()
    print(f"selftest ok  c_pvr_watch.py {sha(Path(__file__).read_bytes())}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    r = sp.add_parser("run")
    for k in ("--work", "--build", "--log"):
        r.add_argument(k, type=Path, required=True)
    for k in ("--ssh", "--tman", "--start"):
        r.add_argument(k, required=True)
    a = ap.parse_args()
    G.load()
    if a.cmd == "selftest":
        return selftest()
    return run(Remote(["ssh", "-o", "BatchMode=yes", a.ssh]), a.work, a.build, a.tman, a.start, a.log, decomposer)


if __name__ == "__main__":
    sys.exit(main())
