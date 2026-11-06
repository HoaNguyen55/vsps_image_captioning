#!/usr/bin/env python3
"""Paper C: the A12 absent-label file for xm3600_vi (CC-277 H1; CC-280 Ruling 1 (a)-(g); LOG OPS-1106c-a12-source).

  <c_pvr venv python> -I -B scripts/c_pvr_a12/c_pvr_a12.py selftest        synthetic fixtures only, no repo data read
  <c_pvr venv python> -I -B scripts/c_pvr_a12/c_pvr_a12.py run --out DIR   coordinator only, after the ACCESS_LOG row

run reads the tracked label file data/xm3600/oiv7_labels.json once: the bytes are hashed against the pin and parsed
from the same bytes, and the file is never copied. It calls the pinned resolve_map + statuses of
scripts/xm3600_oiv7.py; the module is built from its sha-checked bytes, and that module imports numpy, hence the c_pvr
venv. It asserts the four registered counts (LOG l.1381, CC-280 Ruling 1(d)), keeps the absent classes of the 3,600
xm3600_vi query ids and writes DIR/a12_absent.json {qid: {"absent": [class, ...]}} (0600) into DIR, a NEW 0700 dir on
ext4. It prints counts and shas only. Any failed check is a FAULT, and nothing is written.
This script never writes ACCESS_LOG and never opens sealed custody; the coordinator appends the row (CC-280 R1(c)).
"""
import hashlib
import json
import os
import re
import sys
import tempfile
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = {  # repo path, full sha256 pin
    "module": ("scripts/xm3600_oiv7.py", "9a79403f4fc38609282d40082ab7f878133edca8aff9e0dc2462db467b7193f0"),
    "map": ("data/xm3600/vi_oiv7_map.json", "27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a"),
    "desc": ("data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv",
             "84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3"),
    "labels": ("data/xm3600/oiv7_labels.json", "bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2"),
    "qids": ("manuscript/prereg/2026-11-02_c_pvr_tier1/xm3600_all_ids.txt",
             "1bd00f466afc196ab51a6b86d3c1a5b6ea1e553393362b98199aa892287e1922"),
    "ga": ("manuscript/prereg/2026-11-02_c_pvr_tier1/ga_remaining_ids.txt",
           "3feccabc6da972396482faf0d2ae81296277e665ce094368019a3913c2fcbd24"),
}
EXPECT = {"label_keys": 2584, "with_status": 2119, "present": 4453, "absent": 8276}  # LOG l.1381; CC-280 R1(d)
BARRED = re.compile(r"\.vsps_sealed|t2pool_", re.I)
OUT_NAME = "a12_absent.json"


def fault(msg: str):
    raise SystemExit(f"FAULT: {msg}")


def pinned(path: Path, sha: str) -> bytes:
    if BARRED.search(str(path)):
        fault(f"barred path {Path(path).name}")
    b = Path(path).read_bytes()
    if hashlib.sha256(b).hexdigest() != sha:
        fault(f"{Path(path).name} differs from its pin {sha[:8]}")
    return b


def load_module(path: Path, sha: str) -> types.ModuleType:
    """The pinned module, built from the same bytes that were hashed (no second open of the file)."""
    b = pinned(path, sha)
    mod = types.ModuleType("xm3600_oiv7")
    mod.__file__ = str(path)
    exec(compile(b, str(path), "exec"), mod.__dict__)
    return mod


def fstype(p: Path) -> str:
    """Filesystem type of the mount holding p (longest mount-point prefix in /proc/self/mountinfo)."""
    best, kind = "", ""
    for ln in Path("/proc/self/mountinfo").read_text().splitlines():
        f = ln.split()
        mp = f[4].replace("\\040", " ")
        if (str(p) == mp or str(p).startswith(mp.rstrip("/") + "/")) and len(mp) >= len(best):
            best, kind = mp, f[f.index("-") + 1]
    return kind


def write_new(out: Path, data: bytes) -> Path:
    try:
        os.mkdir(out, 0o700)
    except FileExistsError:
        fault("output dir appeared during the run; nothing written")
    os.chmod(out, 0o700)
    tmp, dst = out / (OUT_NAME + ".tmp"), out / OUT_NAME
    with os.fdopen(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.chmod(tmp, 0o600)
    os.replace(tmp, dst)
    d = os.open(out, os.O_RDONLY)
    os.fsync(d)
    os.close(d)
    return dst


def extract(paths: dict, pins: dict, expect: dict, out: Path) -> dict:
    out = Path(os.path.abspath(out))
    if os.path.lexists(out):
        fault("output dir exists (absence guard, CC-278 A6 form)")
    if BARRED.search(str(out)) or fstype(out.parent) != "ext4":
        fault("output dir must be a new dir on ext4, outside custody")
    mod = load_module(paths["module"], pins["module"])
    pinned(paths["map"], pins["map"])
    pinned(paths["desc"], pins["desc"])
    mod.MAP = Path(paths["map"])  # resolve_map reads the module-level MAP; the real run passes the same repo path
    raw = json.loads(pinned(paths["labels"], pins["labels"]))
    labels = {k: v for k, v in raw.items() if not k.startswith("_")}  # drop _provenance, as cmd_score l.224
    qids = set(pinned(paths["qids"], pins["qids"]).decode("utf-8").splitlines())
    ga = set(pinned(paths["ga"], pins["ga"]).decode("utf-8").splitlines())

    vmap = mod.resolve_map(Path(paths["desc"]))
    st = mod.statuses(vmap, labels)
    vals = [v for s in st.values() for v in s.values()]
    got = {"label_keys": len(labels), "with_status": len(st),
           "present": vals.count("present"), "absent": vals.count("absent")}
    if got != expect:
        fault(f"counts {got} != registered {expect}")
    if n_out := len(labels.keys() - qids):
        fault(f"{n_out} label key(s) outside the {len(qids)} xm3600_vi query ids (CC-280 R1(e))")

    if n_ga := len(labels.keys() & ga):
        fault(f"{n_ga} label key(s) in ga_remaining_ids (C's tier-3 NoCaps test set; CC-277 AD1)")
    res = {q: {"absent": sorted(c for c, v in s.items() if v == "absent")} for q, s in sorted(st.items()) if q in qids}
    res = {q: r for q, r in res.items() if r["absent"]}
    classes = {c for r in res.values() for c in r["absent"]}
    if classes - set(vmap):
        fault(f"{len(classes - set(vmap))} output class(es) not a mapped class")
    total = sum(len(r["absent"]) for r in res.values())
    if total != got["absent"]:
        fault(f"absent total {total} != {got['absent']}")
    data = (json.dumps(res, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    dst = write_new(out, data)
    return {**got, "label_keys_outside_qids": 0, "label_keys_x_ga_remaining": 0, "queries_with_absent": len(res),
            "absent_total": total, "classes_used": len(classes), "mapped_classes": len(vmap),
            "out": str(dst), "out_bytes": len(data), "out_sha256": hashlib.sha256(data).hexdigest(),
            "pins": {k: v[:8] for k, v in pins.items()}}


def selftest() -> None:
    """Synthetic fixtures (no repo data file is read) through the real pinned module."""
    t = Path(tempfile.mkdtemp(prefix="c_pvr_a12_st_"))
    files = {
        "desc": "LabelName,DisplayName\n/m/a,Dog\n/m/b,Cat\n/m/c,Car\n/m/d,Tree\n",
        "map": json.dumps({"_note": "x", "chó": {"pos": ["Dog"], "neg": ["Dog"]},
                           "mèo": {"pos": ["Cat"], "neg": ["Cat"]}, "xe": {"pos": ["Car"], "neg": ["Car"]}}),
        "labels": json.dumps({"_provenance": {"made_by": "fixture"},
                              "q1": {"pos": ["/m/a"], "neg": ["/m/b", "/m/c"]},  # chó present, mèo + xe absent
                              "q2": {"pos": [], "neg": ["/m/a"]},                # chó absent
                              "q3": {"pos": ["/m/b"], "neg": []},                # mèo present only: no output key
                              "q4": {"pos": [], "neg": ["/m/d"]}}),              # unmapped class: no status
        "qids": "q1\nq2\nq3\nq4\nq5\n", "ga": "g1\ng2\n",
        "qids_short": "q1\nq2\nq3\n", "ga_hit": "g1\nq2\n",
    }
    paths, pins = {"module": ROOT / P["module"][0]}, {"module": P["module"][1]}
    for k, s in files.items():
        (t / k).write_text(s, encoding="utf-8")
        paths[k], pins[k] = t / k, hashlib.sha256(s.encode("utf-8")).hexdigest()
    exp = {"label_keys": 4, "with_status": 3, "present": 2, "absent": 3}

    r = extract(paths, pins, exp, t / "ok")
    want = '{"q1":{"absent":["mèo","xe"]},"q2":{"absent":["chó"]}}\n'.encode("utf-8")
    assert Path(r["out"]).read_bytes() == want, Path(r["out"]).read_bytes()
    assert os.listdir(t / "ok") == [OUT_NAME]
    assert (os.stat(t / "ok").st_mode & 0o777, os.stat(r["out"]).st_mode & 0o777) == (0o700, 0o600)
    assert (r["queries_with_absent"], r["absent_total"], r["classes_used"], r["mapped_classes"]) == (2, 3, 3, 3), r
    assert r["out_sha256"] == hashlib.sha256(want).hexdigest() and fstype(Path("/proc")) == "proc"

    def refused(tag: str, needle: str, out: Path, **over) -> None:
        pp, pn, ex = dict(paths), dict(pins), dict(exp)
        for k, v in over.items():
            if k == "expect":
                ex.update(v)
            elif k.endswith("_pin"):
                pn[k[:-4]] = "0" * 64
            else:
                pp[k], pn[k] = paths[v], pins[v]
        try:
            extract(pp, pn, ex, out)
        except SystemExit as e:
            assert str(e).startswith("FAULT") and needle in str(e), (tag, str(e))
        else:
            raise AssertionError(f"{tag}: no FAULT")

    (t / "pre").mkdir()
    refused("exists", "absence guard", t / "pre")
    for tag, needle, over in (
            ("proc_fs", "ext4", {}),
            ("module_pin", "xm3600_oiv7.py", {"module_pin": 1}),
            ("labels_pin", "labels", {"labels_pin": 1}),
            ("map_pin", "map", {"map_pin": 1}),
            ("desc_pin", "desc", {"desc_pin": 1}),
            ("qids_pin", "qids", {"qids_pin": 1}),
            ("ga_pin", "ga", {"ga_pin": 1}),
            ("counts", "counts", {"expect": {"absent": 4}}),
            ("outside", "outside", {"qids": "qids_short"}),
            ("ga_hit", "ga_remaining", {"ga": "ga_hit"})):
        out = Path("/proc/c_pvr_a12_x") if tag == "proc_fs" else t / f"out_{tag}"
        refused(tag, needle, out, **over)
        assert not os.path.lexists(out), tag
    refused("barred", "custody", t / "t2pool_x")
    assert sorted(os.listdir(t)) == sorted([*files, "ok", "pre"]), os.listdir(t)


def main(argv: list) -> int:
    if argv[1:] == ["selftest"]:
        selftest()
        print("selftest ok")
        return 0
    if len(argv) == 4 and argv[1:3] == ["run", "--out"]:
        r = extract({k: ROOT / p for k, (p, _) in P.items()}, {k: s for k, (_, s) in P.items()}, EXPECT, Path(argv[3]))
        print(json.dumps(r, sort_keys=True))
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
