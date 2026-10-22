#!/usr/bin/env python3
"""Paper E stage 1 (EXPLORATORY / DEV): the E-dev-A / E-dev-B split of XM-dev500, the refusal every E script runs,
and the n-gram scan of files before a commit. Design: manuscript/prereg/2026-10-22_e_stage1/DESIGN.md (sha pinned).

  python scripts/e_stage1/e_lists.py --selftest                                       CPU, no data
  python scripts/e_stage1/e_lists.py split --out e_split.json --c-lists lists.json     CPU, local only, never on M3
  python scripts/e_stage1/e_lists.py scan FILE [FILE ...]                              CPU, local: hit counts only
`split` reads XM3600 image bytes, ids, file names and the number of captions per image; it never reads a caption.
XM-dev500 is Paper C's set (build_memory.split, tag "xm", first 500), so both papers name the same 500 images.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(ROOT / "scripts/c_stage1")]
import build_memory as BM  # noqa: E402  C's split rule and caption list for the scan, reused unchanged
import decode_icl as C  # noqa: E402  C's pins and exclusion.json loader

LABEL = "EXPLORATORY / DEV"
SCHEMA = "vsps.e_stage1_split.v1"
DESIGN = "manuscript/prereg/2026-10-22_e_stage1/DESIGN.md"
DESIGN_SHA256 = "c793cbe6f9b57aca71a70e5cdcc954d914624e89b93661015a430802a9ae98bd"
#: e_split.json, set by the split addendum (DESIGN §2.4); every GPU step refuses while it is None
SPLIT_SHA256 = "795652f1af45597b3a89f8a937056a1810504d54e1e41319198b3fb27fea2ef9"
N_A = 250  # E-dev-A: the first 250 of XM-dev500 in sha256("paperE|xmdev|" + image sha256) order


def sha256_file(path: Path) -> str:
    return C.lb.sha256_file(Path(path))


#: committed files the GPU modes import (retarget relies on guard's internals); judge.py checks only these
GPU_PINS = {"scripts/c_stage1/guard.py": "5f930e96bd1e1db85e6f8e8445b9172d734c8900800551e6a119e7ec93351cb4",
            "scripts/clip_score.py": "c70b0be214504afbea4d6d5458bb1126c677bcc24122ecda4c1dec0472cdf38f"}
#: added for the local modes (split, pairs build / items, score), which read labels and references; never on M3
LOCAL_PINS = {"scripts/xm3600_oiv7.py": "9a79403f4fc38609282d40082ab7f878133edca8aff9e0dc2462db467b7193f0",
              "data/xm3600/oiv7_labels.json": "bac3953a511a9793c22e928a29b68ae05dbf9654502abcbe7b64fd9f6d74c8b2",
              "data/xm3600/vi_oiv7_map.json": "27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a",
              "data/coco_probe/coco80_vi.json": "926e08571ef6e80a7f8aae8f2b73753d6c5c54c431a750ba2b67bfaae71b540b"}
#: E's test gold and the XM3600 annotation files: absent on M3 before any E GPU step (DESIGN §2.6, CC-081 E1)
M3_ABSENT = ("data/xm3600/oiv7_labels.json",)
M3_ABSENT_DATA = ("datasets/xm3600/full_data.json", "datasets/xm3600/test_data.json", "datasets/xm3600/oiv7",
                  "datasets/xm3600/raw", "datasets/xm3600/images",  # E's pair images live elsewhere (SPLIT_ADDENDUM)
                  "datasets/xm3600_en/full_data.json", "datasets/xm3600_en/test_data.json")
#: e_split.json counts the split addendum must reproduce (CC-081 E4)
EXPECT = {"xm600": 600, "e_dev_a": 250, "e_dev_b": 250, "xm_test2500": 2500}
EXPECT_THREE = {"xm600": 27, "e_dev_a": 7, "e_dev_b": 8, "xm_test2500": 108}


def design(local: bool) -> None:
    """The design and the pinned inputs are as committed. GPU modes (local=False) hash only DESIGN, guard.py and
    clip_score.py, so they never open the labels file; local modes also hash the label tooling and files."""
    for rel, pin in {DESIGN: DESIGN_SHA256, **GPU_PINS, **(LOCAL_PINS if local else {})}.items():
        if sha256_file(ROOT / rel) != pin:
            raise SystemExit(f"{rel}: sha256 differs from the pin in {Path(__file__).name}")


def local_only(what: str) -> None:
    if os.environ.get("VSPS_MACHINE_ID"):
        raise SystemExit(f"{what} reads OIV7 labels or references: it runs locally, never on M3")
    design(local=True)


def m3_clean(data: Path, root: Path = ROOT) -> None:
    """GPU modes refuse while E's test gold or an XM3600 annotation file is on this host (DESIGN §2.6)."""
    there = [str(root / r) for r in M3_ABSENT if (root / r).exists()] + [
        str(data / r) for r in M3_ABSENT_DATA if (data / r).exists()]
    if there:
        raise SystemExit(f"REFUSED: remove from the GPU host before E's GPU steps: {there}")


def e_key(image_sha: str) -> str:
    return hashlib.sha256(f"paperE|xmdev|{image_sha}".encode()).hexdigest()


def split_dev(rows: list) -> tuple[list, list]:
    rows = sorted(rows, key=lambda r: (e_key(r[2]), r[0]))
    return rows[:N_A], rows[N_A:]


# ------------------------------------------------------------------------------------------------ split (CPU, local)
def build(data: Path) -> dict:
    xm = data / "datasets/xm3600"
    full = json.loads((xm / "full_data.json").read_text(encoding="utf-8"))
    xm600 = {str(i["id"]) for i in json.loads((xm / "test_data.json").read_text(encoding="utf-8"))["images"]}
    rows = [(str(i["id"]), i["filename"], sha256_file(xm / "images" / i["filename"])) for i in full["images"]]
    xm_dev, xm_test = BM.split([r for r in rows if r[0] not in xm600], "xm", 500)
    dev_a, dev_b = split_dev(xm_dev)
    n_caps = Counter(str(a["image_id"]) for a in full["annotations"])
    three = {i for i, n in n_caps.items() if n >= 3}  # Paper A's N2 adjacency check read these 150 images' references
    sets = {"xm600": [r for r in rows if r[0] in xm600], "e_dev_a": dev_a, "e_dev_b": dev_b, "xm_test2500": xm_test}
    return {
        "schema": SCHEMA, "label": LABEL, "design_sha256": DESIGN_SHA256,
        "rule": {"xm_dev500": "Paper C build_memory.split: XM3600 minus XM600, sha256('paperC|xm|'+image sha256) "
                              "order, first 500", "e_dev_a": f"XM-dev500 in sha256('paperE|xmdev|'+image sha256) "
                                                             f"order, first {N_A}; e_dev_b the rest"},
        "sets": {"e_dev_a": dev_a, "e_dev_b": dev_b},
        "refuse_image_sha256": sorted({r[2] for k in ("xm600", "e_dev_b", "xm_test2500") for r in sets[k]}),
        "xm_dev500_sha256": sorted(r[2] for r in xm_dev),
        "counts": {k: len(v) for k, v in sets.items()} | {
            "paperA_n2_three_ref_images": len(three),
            "paperA_n2_three_ref_in": {k: len({r[0] for r in v} & three) for k, v in sets.items()}},
    }


def cmd_split(a) -> None:
    local_only("split")
    out = build(C.lb.DATA)
    c = json.loads(Path(a.c_lists).read_text(encoding="utf-8"))  # C's committed lists.json: the same XM-dev500
    if sorted(r[2] for r in c["sets"]["xm_dev500"]) != out["xm_dev500_sha256"]:
        raise SystemExit("XM-dev500 differs from Paper C's lists.json")
    out["c_lists_sha256"] = sha256_file(Path(a.c_lists))
    got = {k: out["counts"][k] for k in EXPECT}, {k: out["counts"]["paperA_n2_three_ref_in"][k] for k in EXPECT}
    if got != (EXPECT, EXPECT_THREE):
        raise SystemExit(f"split counts {got} do not reproduce {EXPECT} / {EXPECT_THREE}: back to the judge")
    text = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    hits = scan_text(text, corpus(C.lb.DATA))
    if any(hits.values()):
        raise SystemExit(f"the split file would hold caption n-grams {hits}; not written")
    Path(a.out).write_text(text, encoding="utf-8")
    print(json.dumps(out["counts"]))


# ------------------------------------------------------------------------------------------------ refusal
def load_split(path: Path, pin: str | None = SPLIT_SHA256) -> dict:
    if pin is None:
        raise SystemExit("e_split.json is not pinned yet: the split addendum must be committed before any GPU step")
    if sha256_file(path) != pin:
        raise SystemExit(f"{path}: sha256 differs from the pinned e_split.json")
    split = json.loads(Path(path).read_text(encoding="utf-8"))
    if split.get("design_sha256") != DESIGN_SHA256:
        raise SystemExit(f"{path}: built under another design")
    return split


def refusal(split: dict) -> tuple[dict[str, tuple[str, str]], set[str], set[str]]:
    """(E-dev-A {id: (file, sha)}, refused ids, refused sha256). The only carve-out from exclusion.json is the
    E-dev-A images' sha256; XM600, E-dev-B, XM-test2500 and every other registered test image stay refused."""
    ex = json.loads(C.pinned(C.EXCL).read_text(encoding="utf-8"))
    allow = {i: (f, h) for i, f, h in split["sets"]["e_dev_a"]}
    carve = {h for _f, h in allow.values()}
    xm_all = set(ex["image_sha256"]["xm3600_all_images"])
    others = {h for k, v in ex["image_sha256"].items() if k != "xm3600_all_images" for h in v}
    if not carve <= xm_all or carve & others:
        raise SystemExit("the E-dev-A carve-out is not a subset of XM3600 alone")
    ids = {str(x) for v in ex["ids"]["xm3600"].values() for x in v}
    hashes = (xm_all - carve) | others | set(split["refuse_image_sha256"])
    if carve & hashes or set(allow) & ids:
        raise SystemExit("an E-dev-A image is also refused")
    return allow, ids, hashes


def check_images(image_ids, split: dict) -> dict[str, tuple[str, str]]:
    """{id: (file, sha)} for the given ids; refused unless every one is an E-dev-A image."""
    allow, ids, hashes = refusal(split)
    bad = sorted({i for i in image_ids if i not in allow or i in ids or allow[i][1] in hashes})
    if bad:
        raise SystemExit(f"REFUSED: {len(bad)} image(s) outside E-dev-A, e.g. {bad[:3]}")
    return {i: allow[i] for i in image_ids}


# ------------------------------------------------------------------------------------------------ n-gram scan
def grams(text: str, n: int) -> set:
    w = re.sub(r"[^\w\s]", " ", text.lower()).split()
    return {tuple(w[k:k + n]) for k in range(len(w) - n + 1)}


def corpus(data: Path) -> list[str]:
    """KTVIC train/test and OpenViIC train/dev/test (C's list), plus every XM3600 Vietnamese and English caption."""
    out = BM.dataset_captions(data / "datasets")
    for name in ("xm3600", "xm3600_en"):
        out += [a["caption"] for a in json.loads((data / f"datasets/{name}/full_data.json").read_text(
            encoding="utf-8"))["annotations"]]
    return out


def scan_text(text: str, captions: list[str], ns=(6, 8)) -> dict[int, int]:
    return {n: len(grams(text, n) & set().union(*(grams(c, n) for c in captions))) for n in ns}


def cmd_scan(a) -> None:
    caps = corpus(C.lb.DATA)
    for f in a.files:
        print(f"{f}\t" + "\t".join(f"{n}-gram {k}" for n, k in scan_text(Path(f).read_text(encoding="utf-8"),
                                                                           caps).items()))


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def selftest() -> None:
    design(local=True)
    seen = []
    real = C.lb.sha256_file
    C.lb.sha256_file = lambda p: seen.append(Path(p).resolve()) or real(p)  # noqa: E731
    try:
        design(local=False)
    finally:
        C.lb.sha256_file = real
    assert not {(ROOT / r).resolve() for r in LOCAL_PINS} & set(seen), "the GPU check never opens labels or tooling"
    with tempfile.TemporaryDirectory() as tmp:
        root, data = Path(tmp) / "r", Path(tmp) / "d"
        m3_clean(data, root)
        (root / "data/xm3600").mkdir(parents=True)
        (root / M3_ABSENT[0]).write_text("{}")
        assert C.refuses(lambda: m3_clean(data, root)), "test gold on the GPU host is refused"
        (root / M3_ABSENT[0]).unlink()
        (data / "datasets/xm3600_en").mkdir(parents=True)
        (data / "datasets/xm3600_en/full_data.json").write_text("{}")
        assert C.refuses(lambda: m3_clean(data, root)), "an XM3600 annotation file on the GPU host is refused"
    h = lambda s: hashlib.sha256(s.encode()).hexdigest()  # noqa: E731
    rows = [(f"x{n}", f"x{n}.jpg", h(f"x{n}")) for n in range(600)]
    a, b = split_dev(rows[:500])
    assert len(a) == N_A and len(b) == 500 - N_A and not {r[0] for r in a} & {r[0] for r in b}
    assert split_dev(rows[:500][::-1]) == (a, b), "the split does not depend on input order"
    ex = json.loads(C.pinned(C.EXCL).read_text(encoding="utf-8"))
    xm_all = sorted(ex["image_sha256"]["xm3600_all_images"])
    xm600_id = str(ex["ids"]["xm3600"]["xm600_test_data_json"][0])
    fake = {"design_sha256": DESIGN_SHA256, "refuse_image_sha256": [xm_all[1]],
            "sets": {"e_dev_a": [["d1", "d1.jpg", xm_all[0]]], "e_dev_b": [["d2", "d2.jpg", xm_all[1]]]}}
    assert check_images(["d1"], fake) == {"d1": ("d1.jpg", xm_all[0])}
    for bad in (["d2"], [xm600_id], ["d1", "unknown"]):
        assert C.refuses(lambda b=bad: check_images(b, fake)), f"{bad} must be refused"
    other = next(v[0] for k, v in ex["image_sha256"].items() if k != "xm3600_all_images")
    assert C.refuses(lambda: refusal({**fake, "sets": {"e_dev_a": [["k", "k.jpg", other]]}})), "carve-out is XM only"
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "s.json"
        p.write_text(json.dumps(fake), encoding="utf-8")
        assert C.refuses(lambda: load_split(p, None)), "an unpinned split is refused"
        assert C.refuses(lambda: load_split(p, "0" * 64)), "a changed split is refused"
    caps = ["chuỗi thử nghiệm số một gồm các âm tiết giả và con chó"]
    assert scan_text("x chuỗi thử nghiệm số một gồm các âm tiết y", caps) == {6: 4, 8: 2}
    assert scan_text("chuỗi thử nghiệm số hai", caps) == {6: 0, 8: 0}
    print("selftest ok: GPU/local pin split, M3 absence check, dev-A/B split, E-dev-A carve-out, refusal of XM600 / "
          "dev-B / other test images, pins, scan")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("split")
    p.add_argument("--out", required=True)
    p.add_argument("--c-lists", type=Path, required=True)
    p = sub.add_parser("scan")
    p.add_argument("files", nargs="+")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    {"split": cmd_split, "scan": cmd_scan}.get(a.cmd, lambda _a: ap.error("mode?"))(a)


if __name__ == "__main__":
    main()
