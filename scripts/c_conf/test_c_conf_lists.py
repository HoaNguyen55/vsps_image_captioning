"""Self-test and mutants of the carve order builder (c_conf_lists.py) on synthetic fixtures only.

Runs on a rented host (the investigator's rule of 2026-11-11: no test runs on the laptop), in a venv holding only
numpy==2.5.4 (by hash), from a copy of the repository holding at least the import closure of the builder:
    scripts/c_conf/c_conf_lists.py, scripts/c_conf/test_c_conf_lists.py, scripts/c_stage1/build_memory.py,
    scripts/c_stage1/decode_icl.py, scripts/lb/decode_hf_vlm.py, scripts/g2b/decode_qwen3vl.py,
    scripts/match_openviic.py, scripts/evaluate.py   (build_memory and match_openviic import numpy)
    env -u PYTHONPATH venv/bin/python -I -B scripts/c_conf/test_c_conf_lists.py   # self-test, then every mutant must fail it
Reads no study file: every input is written into a temporary folder by this script.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "c_conf_lists.py"


def load(path: Path):
    spec = importlib.util.spec_from_file_location(f"ccl_{abs(hash(str(path)))}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fixture(L, root: Path) -> tuple[dict, list[str]]:
    """Writes every input of L.INPUTS under root; returns the pins and the expected P1 (sorted cluster ids)."""
    sha = lambda f: f"{f:0>64}"[-64:]  # noqa: E731
    memory = [{"cid": f"m{i:05d}", "members": [["openviic", f"ov{i:03d}.jpg", f"ov{i:03d}.jpg", sha(i)]]} for i in range(40)]
    memory += [{"cid": "m00100", "members": [["openviic", "ovm1.jpg", "ovm1.jpg", sha(101)], ["openviic", "ovm2.jpg", "ovm2.jpg", sha(102)]]},
               {"cid": "m00101", "members": [["ktvic", "7", "00000000007.jpg", sha(103)]]},
               {"cid": "m00102", "members": [["ktvic", "8", "00000000008.jpg", sha(104)], ["openviic", "ov900.jpg", "ov900.jpg", sha(105)]]}]
    lists = {"memory": memory, "sets": {"ov_dev_a": [["ov005.jpg", "ov005.jpg", sha(5)]], "ov_dev_b": [["devonly.jpg", "devonly.jpg", sha(9)]]},
             "refuse": {"openviic_files": ["never_read.jpg"]}}
    # (i): ov001 via a KTVIC train copy, ov002 via a KTVIC test copy only, ov003 via an owner (dev300 id 30)
    pairs = {"train": {"11": [["ov001.jpg", "train", 1, 2, 0.9]], "30": [["ov003.jpg", "train", 0, 0, 0.99]]},
             "test": {"5": [["ov002.jpg", "train", 3, 3, 0.8], ["tst.jpg", "test", 1, 1, 0.9]]}}
    head = json.dumps({"_provenance": {"what": "fixture"}, "_pairs": pairs})[:-1]
    # Nothing after _pairs may be parsed: invalid JSON, then a sentinel far beyond one chunk.
    panel = head + ', "train": @@ not json @@' + " " * (3 * L.CHUNK) + '"SENTINEL_CAPTION"}'
    owners = {k: {} for k in L.KTVIC_OWNERS | L.OPENVIIC_OWNERS | L.OTHER_OWNERS}
    files = {
        L.LISTS: json.dumps(lists), L.PANEL: panel, L.OWNERS: json.dumps({"owners": owners}),
        L.VIHAL + "pool_trainonly_2153_ids.txt": "11\n12\n", L.VIHAL + "survivors_ordered.tsv": "pos\tktvic_id\tfile\timage_sha256\n1\t11\tx\ty\n",
        L.VIHAL + "removed_ids.txt": "12\n",
        "manuscript/prereg/2026-10-30_bd_t1/bd_t1_lists.json": json.dumps({"H": {"ids": ["11"]}, "T2": {"ids": ["40"]}}),
        "data/splits/ktvic_dev300.txt": "30\n31\n",
        "manuscript/prereg/2026-10-21_dev_pools/ktvic_dev299.tsv": "31\tf\ts\n",
        "manuscript/prereg/2026-10-21_dev_pools/exclusion.json": json.dumps({"ids": {"ktvic": {"ktvic_dev_near_duplicate_of_test": ["1437"]}}}),
    }
    pins = {}
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        pins[rel] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert set(pins) == set(L.INPUTS)
    p1 = sorted(f"m{i:05d}" for i in range(40) if i not in (1, 2, 3, 5))
    return pins, p1


def selftest(L) -> None:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        pins, p1 = fixture(L, root)
        reg = {"base": 40, "after_i": 37, "i_file": "ov002.jpg"}
        rows, counts = L.build(root, pins, reg)
        assert counts["base"] == 40 and counts["removed_i"] == 3 and counts["P1"] == 36, counts
        expect = random.Random(L.BM.seed("carve", "ov_train", "c0")).sample(p1, len(p1))
        assert [r[0] for r in rows] == expect, "order differs from the registered formula"
        assert all(len(r) == 3 and r[1] == f"ov{int(r[0][1:]):03d}.jpg" for r in rows), "row is not [cid, file, sha256]"
        assert rows == L.build(root, pins, reg)[0], "not deterministic"
        assert counts["panel_chars_read_past_pairs"] <= L.CHUNK
        assert counts["iii_id_ktvic_dev300"] == "2 ids, 1 base matches, all inside (i)", counts
        assert counts["iii_id_openviic_dev_c1"] == "2 files, 1 base matches", counts
        text = (root / L.PANEL).read_text(encoding="utf-8")
        pairs, over = L.pairs_block(root / L.PANEL, chunk=64)
        assert over <= 64 and text.index("SENTINEL") > text.index(', "train": @@') + 64, "the sentinel would have been read"
        assert set(pairs) == {"train", "test"}
        for bad in ({**reg, "base": 41}, {**reg, "after_i": 36}, {**reg, "i_file": "ov004.jpg"}):
            try:
                L.build(root, pins, bad)
            except AssertionError:
                continue
            raise AssertionError(f"registered check not enforced: {bad}")
        wrong = {**pins, L.LISTS: "0" * 64}
        try:
            L.build(root, wrong, reg)
        except AssertionError:
            pass
        else:
            raise AssertionError("sha256 pin not enforced")
        owners = json.loads((root / L.OWNERS).read_text())
        owners["owners"]["new_owner"] = {}
        (root / L.OWNERS).write_text(json.dumps(owners))
        try:
            L.build(root, {**pins, L.OWNERS: hashlib.sha256((root / L.OWNERS).read_bytes()).hexdigest()}, reg)
        except AssertionError:
            pass
        else:
            raise AssertionError("an owner outside the table was accepted")


MUTANTS = [
    ("seed string", '"carve", "ov_train", "c0")).sample(p1, len(p1))', '"carve", "ov_train", "c1")).sample(p1, len(p1))'),
    ("unsorted P1", "p1 = sorted(set(base) - out_i - out_iii)", "p1 = list(set(base) - out_i - out_iii)"),
    ("multi-member clusters in base", 'if len(c["members"]) == 1 and c["members"][0][0] == "openviic"', 'if c["members"][0][0] == "openviic"'),
    ("(i) from the train split only", "for split in pairs.values()", "for split in [pairs[\"train\"]]"),
    ("OpenViIC owner not removed", "out_iii |= hit - out_i", "out_iii |= set()"),
    ("panel parsed in full", "pairs, over = pairs_block(root / PANEL)", "pairs, over = json.loads((root / PANEL).read_text())[\"_pairs\"], 0"),
    ("sha256 not checked", 'assert got == pins[rel], f"sha256 of {rel} is {got}, pinned {pins[rel]}"', "pass"),
    ("row with a fourth field", "[[cid, base[cid][2], base[cid][3]] for cid in order]", "[[cid, base[cid][2], base[cid][3], 0] for cid in order]"),
]


def main() -> None:
    selftest(load(SRC))
    print("self-test PASS")
    src = SRC.read_text(encoding="utf-8")
    alive = []
    with tempfile.TemporaryDirectory() as d:
        for name, old, new in MUTANTS:
            assert src.count(old) == 1, f"mutant anchor not found once: {name}"
            p = Path(d) / f"m_{len(alive)}_{abs(hash(name))}.py"
            p.write_text(src.replace(old, new), encoding="utf-8")
            try:
                mod = load_with_root(p)
                selftest(mod)
                alive.append(name)
            except Exception:  # noqa: BLE001  any failure kills the mutant
                pass
    print(f"mutants: {len(MUTANTS) - len(alive)} of {len(MUTANTS)} killed")
    assert not alive, f"mutants alive: {alive}"


def load_with_root(path: Path):
    """Load a mutant copy so that its imports resolve against the real repository (for build_memory.seed)."""
    text = path.read_text(encoding="utf-8").replace(
        "ROOT = Path(__file__).resolve().parents[2]", f"ROOT = Path({str(SRC.parents[2])!r})")
    path.write_text(text, encoding="utf-8")
    return load(path)


if __name__ == "__main__":
    main()
