#!/usr/bin/env python3
"""G0 (Paper A, CC-181 item 1): output-free V20 gold sizes on all 1,000 PASCAL-50S images.
POST HOC DESCRIPTIVE, NO VERDICT. Pinned note: manuscript/prereg/2026-10-30_a_g0/NOTE.md.
Uses the frozen p50.py (V20, voc_gold, load_refs, draw) and score_g2b's English matcher, imported unchanged.
Reads only Annotations/<id>.xml members from the streamed VOC tar; writes numbers and class names only.

  a_g0.py --selftest                         CPU, synthetic data only
  a_g0.py --json pascal50S.json --tar voc.tar --out g0.json
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/pascal50s"))
import p50  # noqa: E402  (sets up the score_g2b path)
import score_g2b as g  # noqa: E402

P50_SHA = "2387ca05ae8a57304a5f696c4e2f73d29297d03ccc23debb416269dc7a676d31"  # committed at 353437f
TAR_SHA = "7f0ca53c1b5a838fbe946965fc106c6e86832183240af5c88e3f6c306318d42e"  # data/results/p50/stage.json


def check_pin(path, sha: str, size: int | None = None) -> None:
    p = Path(path)
    if (size is not None and p.stat().st_size != size) or p50.sha_file(p) != sha:
        raise SystemExit(f"REFUSED: {p.name} differs from its pin")


def read_voc(tar, ids: list[str]) -> dict[str, set[str]]:
    """{id: voc_gold} from the Annotations/<id>.xml members only; nothing is written, no JPEG is extracted."""
    want = {f"Annotations/{i}.xml": i for i in ids}
    voc: dict[str, set[str]] = {}
    with tarfile.open(tar, "r|") as tf:
        for m in tf:
            tail = "/".join(m.name.split("/")[-2:])
            if m.isfile() and tail in want:
                if want[tail] in voc:
                    raise SystemExit(f"REFUSED: two tar members end in {tail}")
                voc[want[tail]] = p50.voc_gold(tf.extractfile(m).read())
    if len(voc) != len(ids):
        raise SystemExit(f"REFUSED: {len(ids) - len(voc)} annotation(s) missing from the tar")
    return voc


def counts(refs: dict[str, list[str]], voc: dict[str, set[str]], ids: list[str]) -> dict:
    en, V = g.MATCH["coco80"]["en"], set(p50.V20.values())
    refm = [[en(s) & V for s in refs[i]] for i in ids]
    R = [set().union(*r) for r in refm]
    L = [voc[i] for i in ids]
    s_ref, s_voc = sum(map(len, R)), sum(map(len, L))
    per = {c: {"voc_not_refs50": sum(c in l - r for r, l in zip(R, L)),
               "refs50_not_voc": sum(c in r - l for r, l in zip(R, L)),
               "both": sum(c in r & l for r, l in zip(R, L))} for c in sorted(V)}
    sub = p50.draw([len(x) for x in refm])
    rungs = {}
    for k, reps in sub.items():
        Rk = [[set().union(*(refm[n][j] for j in s[n])) for n in range(len(ids))] for s in reps]
        rungs[f"refs{k}_randk"] = {"sum_refs_V20_mean": sum(sum(map(len, r)) for r in Rk) / len(Rk),
                                   "sum_refs_V20_and_voc_mean": sum(sum(len(a & b) for a, b in zip(r, L)) for r in Rk) / len(Rk)}
    return {"n_images": len(ids), "S_ref_refs50_V20": s_ref, "S_voc_voc20": s_voc,
            "ratio_voc_over_ref": round(s_voc / s_ref, 4) if s_ref else None,
            "outcome": "A" if s_voc >= 2 * s_ref else "B",
            "sum_both": sum(len(r & l) for r, l in zip(R, L)), "sum_voc_not_refs50": sum(len(l - r) for r, l in zip(R, L)),
            "sum_refs50_not_voc": sum(len(r - l) for r, l in zip(R, L)), "per_class": per, "rungs": rungs,
            "anchor_S_voc_ge_1782": s_voc >= 1782}


def run(json_path, tar, out) -> dict:
    check_pin(p50.__file__, P50_SHA)
    check_pin(json_path, *p50.P50_JSON)
    check_pin(tar, TAR_SHA, p50.VOC_TAR_BYTES)
    ids = p50.id_list()
    res = counts(p50.load_refs(json_path, ids), read_voc(tar, ids), ids)
    res.update({"label": "POST HOC DESCRIPTIVE, NO VERDICT (CC-181)", "p50_sha256": P50_SHA, "tar_sha256": TAR_SHA,
                "json_sha256": p50.P50_JSON[0], "a_g0_sha256": p50.sha_file(__file__)})
    p50.dump(res, out)
    return res


def selftest() -> None:
    def xml(*names):
        return ("<annotation>" + "".join(f"<object><name>{n}</name></object>" for n in names) + "</annotation>").encode()

    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        tar = d / "t.tar"
        with tarfile.open(tar, "w") as tf:
            for name, b in [("VOC/JPEGImages/a.jpg", b"\xff\xd8not-a-jpeg"), ("VOC/Annotations/a.xml", xml("dog", "person")),
                            ("VOC/Annotations/b.xml", xml("aeroplane")), ("VOC/Annotations/z.xml", xml("cat"))]:
                ti = tarfile.TarInfo(name)
                ti.size = len(b)
                tf.addfile(ti, io.BytesIO(b))
        before = sorted(d.iterdir())
        voc = read_voc(tar, ["a", "b"])
        assert voc == {"a": {"dog", "person"}, "b": {"airplane"}}, voc
        assert sorted(d.iterdir()) == before, "read_voc wrote a file"
        for bad in (lambda: read_voc(tar, ["a", "q"]), lambda: check_pin(tar, "0" * 64), lambda: check_pin(tar, p50.sha_file(tar), 1)):
            try:
                bad()
                raise AssertionError("no refusal")
            except SystemExit as e:
                assert str(e).startswith("REFUSED"), e
        check_pin(tar, p50.sha_file(tar), tar.stat().st_size)
    refs = {"a": ["a dog runs", "a man and a dog", "a cat"] + ["a dog"] * 47,
            "b": ["an aeroplane on the runway", "a plane", "a sofa"] + ["sky"] * 47}
    r = counts(refs, voc, ["a", "b"])
    # a: R = {dog, person, cat}, L = {dog, person}; b: R = {airplane, couch} (aeroplane gap; plane -> airplane), L = {airplane}
    assert (r["S_ref_refs50_V20"], r["S_voc_voc20"], r["outcome"]) == (5, 3, "B"), r
    assert (r["sum_both"], r["sum_voc_not_refs50"], r["sum_refs50_not_voc"]) == (3, 0, 2), r
    assert r["per_class"]["cat"] == {"voc_not_refs50": 0, "refs50_not_voc": 1, "both": 0}
    assert r["rungs"]["refs20_randk"]["sum_refs_V20_mean"] <= 5 and set(r["rungs"]) == {f"refs{k}_randk" for k in p50.K_LADDER}
    assert counts(refs, {"a": {"dog", "person", "cat", "car", "bus", "cow"}, "b": {"airplane"} | set(list(p50.V20.values())[:4])},
                  ["a", "b"])["outcome"] == "A"
    print("a_g0 selftest ok")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json")
    ap.add_argument("--tar")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.json and a.tar and a.out):
        ap.error("--json, --tar and --out are required")
    r = run(a.json, a.tar, a.out)
    print(json.dumps({k: r[k] for k in ("n_images", "S_ref_refs50_V20", "S_voc_voc20", "ratio_voc_over_ref", "outcome")}))


if __name__ == "__main__":
    main()
