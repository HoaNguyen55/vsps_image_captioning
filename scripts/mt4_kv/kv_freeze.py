#!/usr/bin/env python3
"""MT4 KV freeze writer and validator (MT4 PREREG amendment 1 A3/A4; CC-160 W9, CC-162b G3, Codex round 3).
Every command first runs gate1_decide.check on the Gate 1 decision (anchored, before NOT_AFTER); it never reads a
KV prediction, only file shas. Nothing here runs before the cost-only amendment writes the kept set.

    python3 kv_freeze.py --selftest                                         CPU, synthetic files and a temp repo
    python3 kv_freeze.py append --system X --seed N --file F --gate1 O   one fsynced line of SUMS_KV_REL
    python3 kv_freeze.py costtest --gate1 O --out T.json                    A4: Branch K2 deadline test (cost)
    python3 kv_freeze.py freeze --gate1 O --out F.json                    A3: the frozen set, or a refusal / FAULT

KV_PRED_SUMS lives only at SUMS_KV_REL in the repo (no path option; round 6). Lines: SYSTEM<TAB>SEED<TAB>SHA256<TAB>UTC_EPOCH<TAB>FILE. The kept set is read ONLY from KEPT_REL as
committed at HEAD, and only if its sha256 is pinned in the MT4 SHA256SUMS committed at HEAD (the cost-only
amendment commits both): {"kept": [[system, seed], ...], "h": {"H1": [[system, seed], ...], ...}}. It must hold
every H system (base_s 0, gold 1-3, unedited 1-3: never cut, PREREG §8).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / "k2_gate1")]
import gate1_decide as GD  # noqa: E402

D = 1796040000  # 2026-11-30T12:00:00Z, the Branch K2 hard freeze date (amendment 1 A3)
WINDOW = 24 * 3600  # the freeze instant: the line that completes the kept set + 24 h
N_KV, LOAD_H, CAP_FACTOR, KV_STAGE_H = 4224, 0.1, 1.2, 2.0
H_TRAIN = [("gold", 3), ("unedited", 3)]  # K x 3, U x 3 (amendment 1 A4)
H_DECODE = 7  # base_s, K x 3, U x 3
VAL_SYSTEMS = ("base_s", "unedited", "gold", "det", "ref")
TRAIN_STAGES = ("unedited", "gold", "det", "ref")
KEPT_REL = "manuscript/prereg/2026-10-28_mt4_kv/kv_kept.json"
SUMS_KV_REL = "manuscript/prereg/2026-10-28_mt4_kv/KV_PRED_SUMS"  # the one KV_PRED_SUMS; the gatekeeper commits it
SUMS_REL = "manuscript/prereg/2026-10-28_mt4_kv/SHA256SUMS"
H_KEYS = {("base_s", 0)} | {(a, n) for a in ("gold", "unedited") for n in (1, 2, 3)}  # never cut (§8)


def now() -> float:
    return time.time()


def gate1(o: Path, root: Path | None = None) -> dict:
    """Before anything: the decision must pass gate1_decide.check (written and anchored before NOT_AFTER)."""
    return GD.check(o) if root is None else GD.check(o, root)


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def append(sums: Path, system: str, seed: int, f: Path) -> str:
    """The only writer of KV_PRED_SUMS: the file's sha and the append time, fsynced (file and directory)."""
    line = f"{system}\t{seed}\t{sha(f)}\t{int(now())}\t{f.name}"
    with sums.open("a") as fh:
        fh.write(line + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    fd = os.open(sums.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    return line


def lines(sums: Path) -> list[tuple[str, int, str, int]]:
    out = []
    for x in sums.read_text().splitlines():
        s, n, h, u, _ = x.split("\t")
        out.append((s, int(n), h, int(u)))
    return out


def at_head(root: Path, rel: str) -> bytes:
    r = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{rel}"], capture_output=True)
    if r.returncode:
        raise SystemExit(f"REFUSED: {rel} is not committed at HEAD")
    return r.stdout


def load_kept(root: Path) -> dict:
    """Codex round 4: the kept set comes only from the committed, SUMS-pinned file; no caller-supplied set."""
    raw = at_head(root, KEPT_REL)
    h = hashlib.sha256(raw).hexdigest()
    if f"{h}  {KEPT_REL}" not in at_head(root, SUMS_REL).decode().splitlines():
        raise SystemExit(f"REFUSED: {KEPT_REL} at HEAD ({h[:8]}) is not the sha pinned in the committed MT4 SHA256SUMS")
    kept = json.loads(raw)
    keys = {(s, int(n)) for s, n in kept["kept"]}
    if not H_KEYS <= keys or not all({(s, int(n)) for s, n in v} <= keys for v in kept["h"].values()):
        raise SystemExit("REFUSED: the kept set drops an H system or seed (never cut, PREREG §8)")
    return kept


def freeze(rows: list[tuple[str, int, str, int]], kept: dict, at: float, not_before: float = 0.0) -> dict:
    """A3. First line per (system, seed) counts; a later one is post-freeze descriptive, and a later one with another
    sha before the instant is a FAULT (the first still counts). Lines outside the kept set are descriptive. Instant =
    min(UTC of the line completing the kept set + 24 h, D). Before the instant: refused (no early or partial freeze).
    At D with the set incomplete: the lines up to D freeze and every H missing a seed is NOT-RUN."""
    us = [u for *_, u in rows]
    if us != sorted(us) or (us and us[0] < not_before):  # a line added out of order, or before the GO was pushed
        raise SystemExit("FAULT -> TO-PI: KV_PRED_SUMS times are out of order or precede the anchored GO; no freeze")
    want = {(s, int(n)) for s, n in kept["kept"]}
    first: dict[tuple[str, int], tuple[str, int]] = {}
    complete_at, faults, descriptive = None, [], []
    for s, n, h, u in rows:
        k = (s, n)
        if k not in want:
            descriptive.append([s, n, "outside the kept set"])
            continue
        if k in first:
            descriptive.append([s, n, "duplicate"])
            if h != first[k][0]:
                faults.append([s, n, "duplicate line with another sha"])
            continue
        first[k] = (h, u)
        if complete_at is None and want <= set(first):
            complete_at = u
    if faults:  # Codex round 4: a second sha for a kept system/seed halts the freeze; nothing is written
        raise SystemExit(f"FAULT -> TO-PI: duplicate KV_PRED_SUMS lines with another sha {faults}; no freeze")
    instant = min(complete_at + WINDOW, D) if complete_at is not None else D
    if at < instant:
        raise SystemExit(f"REFUSED: no freeze before its instant {instant} (kept set "
                         f"{'complete' if complete_at is not None else 'incomplete'}; no early or partial freeze)")
    frozen = {f"{s}:{n}": h for (s, n), (h, u) in first.items() if u <= instant}
    late = [[s, n, "after the freeze instant"] for (s, n), (h, u) in first.items() if u > instant]
    h_status = {hk: ("RUN" if all(f"{s}:{n}" in frozen for s, n in seeds) else "NOT-RUN (a registered seed missing)")
                for hk, seeds in kept.get("h", {}).items()}
    return {"freeze_instant": instant, "kept_set_complete_at": complete_at, "frozen": frozen,
            "descriptive": descriptive + late, "h_status": h_status}


def cap(proj_h: float) -> float:
    return math.ceil(round(10 * CAP_FACTOR * proj_h, 6)) / 10


def deadline_test(written_epoch: float, r_dec: float, r_tr: float, n_ex: dict[str, int]) -> dict:
    """A4: t0 = GO write time + 24 h; C_H = caps of the H systems (K x 3, U x 3 training at 2 epochs; 7 KV decodes)
    + 2.0 h staging and cleanup, on one m3-role GPU. t0 + C_H > D -> Branch K2 NOT-RUN (cost), K1+K6 binds."""
    train = sum(k * cap(2 * n_ex[a] * r_tr / 3600 + LOAD_H) for a, k in H_TRAIN)
    dec = H_DECODE * cap(N_KV * r_dec / 3600 + LOAD_H)
    c_h = round(train + dec + KV_STAGE_H, 1)
    t0 = written_epoch + WINDOW
    return {"t0": t0, "C_H_h": c_h, "D": D, "branch_k2": "NOT-RUN (cost)" if t0 + c_h * 3600 > D else "proceeds",
            "r_dec": r_dec, "r_tr": r_tr}


def rates(o: Path) -> tuple[float, float, dict[str, int]]:
    """A4 inputs, numbers only: r_dec = max s_per_image_decode over the five val-924 provenance records; r_tr = max
    over the four training stages of the closing ledger seconds of the attempt that wrote its .done (the last
    closing line) / that stage's examples (2 x examples_per_epoch)."""
    r_dec = max(json.loads((o / f"k2g1_{s}.preds.json").read_text())["s_per_image_decode"] for s in VAL_SYSTEMS)
    per = json.loads((o / "targets.json.counts.json").read_text())["examples_per_epoch"]
    last: dict[str, float] = {}
    for p in (x.split() for x in (o / "gpu_seconds.tsv").read_text().splitlines() if x.strip()):
        if len(p) == 2:
            last[p[0]] = float(p[1])
    r_tr = max(last[f"train_{a}"] / (2 * per[a]) for a in TRAIN_STAGES)
    return r_dec, r_tr, {a: per[a] for a in ("gold", "unedited")}


# ------------------------------------------------------------------------------------------------ selftest
def _refused(f, word: str) -> None:
    try:
        f()
    except SystemExit as e:
        assert word in str(e), e
    else:
        raise AssertionError(f"accepted, expected {word}")


def kept_selftest(repo: Path) -> None:
    """The kept set: committed + pinned -> loaded; a modified file not re-pinned, a missing pin, an uncommitted copy
    and a set that drops an H seed are refused."""
    g = ["git", "-C", str(repo), "-c", "user.name=x", "-c", "user.email=x", "-c", "core.hooksPath=/dev/null",
         "-c", "commit.gpgsign=false"]
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / KEPT_REL).parent.mkdir(parents=True)
    full = {"kept": [list(k) for k in sorted(H_KEYS)] + [["det", 1]], "h": {"H1": [["base_s", 0], ["gold", 1]]}}

    def commit(kept: dict, pin: bool = True) -> None:
        (repo / KEPT_REL).write_text(json.dumps(kept))
        pins = f"{sha(repo / KEPT_REL)}  {KEPT_REL}\n" if pin else "0" * 64 + f"  {KEPT_REL}\n"
        (repo / SUMS_REL).write_text(pins)
        subprocess.run(g + ["add", "-A"], check=True)
        subprocess.run(g + ["commit", "-qm", "k"], check=True)

    _refused(lambda: load_kept(repo), "not committed")
    commit(full)
    assert load_kept(repo)["kept"][-1] == ["det", 1]
    (repo / KEPT_REL).write_text(json.dumps({"kept": [["base_s", 0]], "h": {}}))  # edited, not committed: ignored
    assert len(load_kept(repo)["kept"]) == len(full["kept"])
    subprocess.run(g + ["add", KEPT_REL], check=True)
    subprocess.run(g + ["commit", "-qm", "shrink"], check=True)  # committed without its pin
    _refused(lambda: load_kept(repo), "not the sha pinned")
    commit(full, pin=False)
    _refused(lambda: load_kept(repo), "not the sha pinned")
    commit({"kept": [k for k in full["kept"] if k != ["gold", 3]], "h": full["h"]})  # an H seed dropped
    _refused(lambda: load_kept(repo), "drops an H system")


def selftest() -> None:
    import tempfile

    global now
    kept = {"kept": [["base_s", 0], ["gold", 1], ["gold", 2]], "h": {"H1": [["base_s", 0], ["gold", 1], ["gold", 2]],
                                                                    "H3": [["gold", 1], ["unedited", 1]]}}
    t0 = D - 10 * 86400
    rows = [("base_s", 0, "a", t0), ("gold", 1, "b", t0 + 10), ("det", 1, "x", t0 + 20),  # det: outside the set
            ("gold", 1, "b", t0 + 30), ("gold", 2, "c", t0 + 40), ("gold", 2, "c", t0 + 50)]
    _refused(lambda: freeze(rows, kept, t0 + 41), "no freeze before its instant")  # complete, inside the 24 h
    f = freeze(rows, kept, t0 + 40 + WINDOW)
    assert f["freeze_instant"] == t0 + 40 + WINDOW and f["kept_set_complete_at"] == t0 + 40
    assert f["frozen"] == {"base_s:0": "a", "gold:1": "b", "gold:2": "c"}  # the first line per system/seed counts
    assert ["det", 1, "outside the kept set"] in f["descriptive"] and ["gold", 1, "duplicate"] in f["descriptive"]
    _refused(lambda: freeze(rows + [("gold", 1, "b2", t0 + 60)], kept, D), "FAULT")  # another sha: halt
    _refused(lambda: freeze(rows + [("gold", 3, "z", t0 + 5)], kept, D), "out of order")  # a backdated insert
    _refused(lambda: freeze(rows, kept, D, not_before=t0 + 1), "precede the anchored GO")
    assert f["h_status"]["H1"] == "RUN" and f["h_status"]["H3"].startswith("NOT-RUN")
    part = rows[:2]  # gold 2 never arrives: no partial freeze before D
    _refused(lambda: freeze(part, kept, D - 1), "incomplete")
    g = freeze(part + [("gold", 2, "c", D + 5)], kept, D)
    assert g["freeze_instant"] == D and "gold:2" not in g["frozen"] and g["h_status"]["H1"].startswith("NOT-RUN")
    assert ["gold", 2, "after the freeze instant"] in g["descriptive"]
    late = [("base_s", 0, "a", D - 3600), ("gold", 1, "b", D - 3000), ("gold", 2, "c", D - 2000)]
    assert freeze(late, kept, D)["freeze_instant"] == D  # completion + 24 h after D: D wins
    n_ex = {"gold": 2392, "unedited": 2392}
    ok = deadline_test(D - 20 * 86400, 8.5, 0.99, n_ex)
    assert ok["branch_k2"] == "proceeds" and ok["C_H_h"] == round(6 * cap(2 * 2392 * 0.99 / 3600 + 0.1)
                                                                  + 7 * cap(4224 * 8.5 / 3600 + 0.1) + 2.0, 1)
    assert deadline_test(D - 3 * 86400, 8.5, 0.99, n_ex)["branch_k2"] == "NOT-RUN (cost)"
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "p.json").write_text("{}")
        real = now
        try:
            now = lambda: 1234.0  # noqa: E731
            line = append(d / "KV_PRED_SUMS", "gold", 1, d / "p.json")
        finally:
            now = real
        assert lines(d / "KV_PRED_SUMS") == [("gold", 1, sha(d / "p.json"), 1234)] and line.endswith("\tp.json")
        (d / "o").mkdir()
        (d / "o/gate1_decide.json").write_text(json.dumps({"verdict": "GO", "written_epoch": GD.NOT_AFTER - 99}))
        _refused(lambda: gate1(d / "o", d), "not anchored")  # every command starts here
        kept_selftest(d / "repo")
        import contextlib
        import io

        for cmd in (["freeze", "--sums", "x", "--gate1", "o", "--out", "f"], ["append", "--sums", "x", "--system", "gold",
                                                                          "--seed", "1", "--file", "f", "--gate1", "o"]):
            with contextlib.redirect_stderr(io.StringIO()):
                _refused(lambda: parser().parse_args(cmd), "2")  # round 6: no --sums override exists
        assert SUMS_KV_REL.startswith("manuscript/prereg/2026-10-28_mt4_kv/")
        o = d / "g1"
        o.mkdir()
        for i, s in enumerate(VAL_SYSTEMS):
            (o / f"k2g1_{s}.preds.json").write_text(json.dumps({"s_per_image_decode": 7.0 + i / 10}))
        (o / "targets.json.counts.json").write_text(json.dumps({"examples_per_epoch": {
            "unedited": 2392, "gold": 2392, "det": 2392, "ref": 11962}}))
        (o / "gpu_seconds.tsv").write_text("train_unedited start 1\ntrain_unedited 2876\ntrain_det start 9 6120\n"
                                           "train_det 6120\ntrain_det start 20 6120\ntrain_det 3000\n"
                                           "train_gold start 2 1\ntrain_gold 2857\ntrain_ref start 3 1\ntrain_ref 20000\n")
        r_dec, r_tr, _ = rates(o)
        assert r_dec == 7.4 and r_tr == max(2876, 2857, 3000, 20000 / 11962 * 2392) / (2 * 2392)  # det: the rerun
    print("kv_freeze selftest ok")


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    a_ = sp.add_parser("append")
    for f in ("--system", "--file", "--gate1"):
        a_.add_argument(f, required=True)
    a_.add_argument("--seed", type=int, required=True)
    c_ = sp.add_parser("costtest")
    for f in ("--gate1", "--out"):
        c_.add_argument(f, required=True)
    f_ = sp.add_parser("freeze")
    for f in ("--gate1", "--out"):
        f_.add_argument(f, required=True)
    return ap


def main() -> None:
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    a = parser().parse_args()
    g = gate1(Path(a.gate1))
    if g["verdict"] != "GO":
        raise SystemExit(f"REFUSED: Gate 1 is {g['verdict']}; Branch K2 has no KV step")
    if a.cmd == "append":
        print(append(GD.K.ROOT / SUMS_KV_REL, a.system, a.seed, Path(a.file)))
        return
    if a.cmd == "costtest":
        r_dec, r_tr, n_ex = rates(Path(a.gate1))
        res = deadline_test(g["written_epoch"], r_dec, r_tr, n_ex)
    else:
        res = freeze(lines(GD.K.ROOT / SUMS_KV_REL), load_kept(GD.K.ROOT), now(), g["push_received_epoch"])
    Path(a.out).write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k not in ("frozen", "descriptive")}))


if __name__ == "__main__":
    main()
