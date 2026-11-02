#!/usr/bin/env python3
"""B-PA1-T1 R6 class list (v3.1 §6.1 l.325-327, W11; CC-226r3 Ruling 6(e)). TIER 1 / DEV-EXPLORE (B-PA1-T1).
DRAFT, uncommitted: needs its own P8 one-judge read before any run on the real json.

    $PY -I -B scripts/b_pa1/categories_extract.py selftest                       synthetic fixtures, no repo data
    $PY -I -B scripts/b_pa1/categories_extract.py run --ann J --ann-sha S --out F   F new (O_EXCL)

$PY = ~/.venvs/b_pa1_ijson (freeze dffafd50, LOG l.1201). `run` takes the train json only by its R6 pin (file name,
--ann-sha, and a LOG pin line, exactly as `b_pa1.py slices frame`), streams `categories[]` with ijson and keeps only
int `id` and str `name`; images[] and annotations[] are never built. Output bytes: canonical json, sorted by id.
stdout: counts and the output sha only, never a class name.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I drops the script folder
import b_pa1 as B  # noqa: E402  ANN_NAME, LABEL, LOG, pin_line, write_new, must_refuse, pin_cases; B.K.sha_file

N_CLASSES = 365  # v3.1 §6.1 l.325: "the 365 Objects365 class names"


def categories_of(fh, n: int = N_CLASSES) -> bytes:
    import ijson  # R2: pinned in the venv freeze

    rows = []
    for c in ijson.items(fh, "categories.item"):
        i, name = c.get("id"), c.get("name")
        if type(i) is not int or type(name) is not str or not name.strip() or any(ch in name for ch in "\t\n\r"):
            raise SystemExit("REFUSED: a categories[] record has no plain int id or one-line str name")
        rows.append((i, name))
    if len(rows) != n or len({i for i, _ in rows}) != n or len({m for _, m in rows}) != n:
        raise SystemExit(f"REFUSED: {len(rows)} categories[] records, {n} distinct ids and names needed")
    doc = {"schema": "vsps.b_pa1.o365_categories.v1", "tier": B.LABEL,
           "categories": [{"id": i, "name": m} for i, m in sorted(rows)]}
    return (json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def run(ann: Path, ann_sha: str, out: Path, log: Path = B.LOG, n: int = N_CLASSES) -> dict:
    if ann.name != B.ANN_NAME or B.K.sha_file(ann) != ann_sha or not B.pin_line(log, ann_sha, B.ANN_NAME):
        raise SystemExit(f"REFUSED: not the R6-pinned {B.ANN_NAME} (name, --ann-sha, LOG pin line)")
    with open(ann, "rb") as fh:
        data = categories_of(fh, n)
    B.write_new(out, data)
    return {"tier": B.LABEL, "n_categories": n, "ann_sha256": ann_sha,
            "sha256": hashlib.sha256(data).hexdigest()}


def selftest() -> int:
    import random
    import tempfile

    sent = "SENTINEL caption xyzzy"
    cats = [{"id": i, "name": f"c{i}", "supercategory": sent} for i in range(1, N_CLASSES + 1)]
    doc = lambda cs: {"images": [{"id": 1, "file_name": sent}], "annotations": [{"note": sent}], "categories": cs}  # noqa
    js = lambda o: io.BytesIO(json.dumps(o).encode())  # noqa: E731

    a = categories_of(js(doc(cats)))
    shuf = cats[:]
    random.Random(7).shuffle(shuf)
    assert a == categories_of(js(doc(shuf))), "input order changes the bytes"
    assert sent.encode() not in a and b"xyzzy" not in a, "non-categories text reached the output"
    got = json.loads(a)["categories"]
    assert [c["id"] for c in got] == list(range(1, N_CLASSES + 1)) and set(got[0]) == {"id", "name"}, got[:2]
    for bad, word in ((cats[:-1], "distinct"), ([*cats, cats[0]], "366 categories"),
                      ([*cats[:-1], {"id": 1, "name": "x"}], "distinct"),
                      ([*cats[:-1], {"id": 999, "name": "c1"}], "distinct"),
                      ([*cats[:-1], {"id": "365", "name": "c365"}], "plain int id"),
                      ([*cats[:-1], {"id": 365, "name": "a\tb"}], "plain int id"),
                      ([*cats[:-1], {"id": 365, "name": " "}], "plain int id")):
        B.must_refuse(lambda: categories_of(js(doc(bad))), word)

    with tempfile.TemporaryDirectory() as d:  # the R6 gate: name, sha and a LOG pin line; new file only
        d = Path(d)
        ann, val, log = d / B.ANN_NAME, d / "zhiyuan_objv2_val.json", d / "LOG.md"
        for p in (ann, val):
            p.write_bytes(json.dumps(doc(cats)).encode())
        good = B.K.sha_file(ann)
        go = lambda p=ann, s=good, o="c.json": run(p, s, d / o, log)  # noqa: E731
        pin_ok, no_pins = B.pin_cases(B.ANN_NAME, good)
        for bad in [*no_pins, B.pin_cases(val.name, good)[0]]:
            log.write_text(bad + "\n")
            B.must_refuse(lambda: go(), "R6")
        log.write_text(pin_ok + "\n")
        B.must_refuse(lambda: go(s="0" * 64), "R6")
        B.must_refuse(lambda: go(p=val), "R6")
        ann.write_bytes(ann.read_bytes() + b" ")  # pinned name and --ann-sha, other bytes
        B.must_refuse(lambda: go(), "R6")
        ann.write_bytes(json.dumps(doc(cats)).encode())
        r = go()
        assert r["sha256"] == hashlib.sha256((d / "c.json").read_bytes()).hexdigest() == hashlib.sha256(a).hexdigest()
        try:
            go()
            raise AssertionError("existing --out overwritten")
        except FileExistsError as e:
            assert "c.json" in str(e), e
    print(json.dumps({"tier": B.LABEL, "selftest": "categories ok",
                      "checks": ["order-free-bytes", "no-other-text", "record-guards", "R6-pin", "new-file"]}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    r = sp.add_parser("run")
    r.add_argument("--ann", type=Path, required=True, help=f"{B.ANN_NAME}")
    r.add_argument("--ann-sha", required=True, help="its R6 LOG pin")
    r.add_argument("--out", type=Path, required=True, help="new file; never overwritten")
    a = ap.parse_args()
    if a.cmd == "selftest":
        return selftest()
    print(json.dumps(run(a.ann, a.ann_sha, a.out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
