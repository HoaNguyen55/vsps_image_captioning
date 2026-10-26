#!/usr/bin/env python3
"""Paper C test (TEST, ONE LOOK PER SET): pins, the two test sets, the per-block carve-out, the host checks, the CC-082
T6 retry, and the M3 steps (SigLIP2 query embed, example lists, decodes, InternVL3's verifier pass, E4 parity).
Prereg manuscript/prereg/2026-10-25_c_test/PREREG.md §3, §4, §5, §11, §13 items 1-4, 7-9; CC-103, CC-103a.

The stage-2 modules are imported unchanged; their sha256 must match the stage-2 SHA256SUMS before any import, and the
test prereg folder's SHA256SUMS must verify with PREREG.md at its pinned sha256.

  python scripts/c_test/ctest.py --selftest                                                  CPU, synthetic only
  python scripts/c_test/ctest.py runs --set S [--model M] [--arm A ...]                       run ids (ct_ prefix)
  python scripts/c_test/ctest.py check-host --block e4|ov|xm --lists L --out J                CPU, on M3 (§11.2)
  python scripts/c_test/ctest.py embed --set S --lists L --emb1 E1 --snapshot DIR --revision REV --out Q      GPU
  python scripts/c_test/ctest.py exemplars --set S --lists L --emb1 E1 --emb Q --out X                     CPU
  python scripts/c_test/ctest.py decode --run-ids R ... --snapshot DIR --lists L --exemplars X --out-dir D  GPU
  python scripts/c_test/ctest.py items --set S --runs R ... --zs Z --lists L --out I                        CPU
  python scripts/c_test/ctest.py verify --set S --items I --lists L --snapshot DIR --out CACHE              GPU
  python scripts/c_test/ctest.py e4 --model M --snapshot DIR --lists L --stage1 D --out-dir D               GPU
  python scripts/c_test/ctest.py xm-subset --lists L --xm-full F --out F                       CPU, local, staging
Every output path on a GPU host must lie under /root/outputs/c_test/ (CC-103a). No caption is printed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
S2_SUMS = ROOT / "manuscript/prereg/2026-10-22_c_stage2/SHA256SUMS"
TDIR = "manuscript/prereg/2026-10-25_c_test"
T_SUMS = ROOT / TDIR / "SHA256SUMS"
PREREG = f"{TDIR}/PREREG.md"
TSV, P1941, T108 = f"{TDIR}/ov_test_files.tsv", f"{TDIR}/ov_test_primary1941.txt", f"{TDIR}/xm_test2500_threeref108.txt"
T_PINS = {PREREG: "acecd6527217c5c59b84917aa1571cfa8b2e50b7879be38d2e305ef91df6363f",
          TSV: "99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695",
          P1941: "6458295ed1df42b854fed3807be3541cc452d6eeb79ee565780b72a777c807e2",
          T108: "2d42a80972c6d0531bcc9d3d2aff43ced617b3bc808d1359b3577a564739fefb"}


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def check_sums(sums: Path, prefix: str = "") -> dict[str, str]:
    """Every line of a SHA256SUMS (paths from the repo root) whose path starts with prefix must verify."""
    out = {}
    for line in sums.read_text(encoding="utf-8").splitlines():
        h, rel = line.split(maxsplit=1)
        if rel.startswith(prefix):
            if sha_file(ROOT / rel) != h:
                raise SystemExit(f"{rel}: differs from {sums.relative_to(ROOT)}")
            out[rel] = h
    return out


def check_pins() -> None:
    """Stage-2 code as committed (CC-096); the test prereg folder 6/6 with PREREG.md and the lists at their pins."""
    check_sums(S2_SUMS, "scripts/c_stage2/")
    got = check_sums(T_SUMS)
    if len(got) != 6 or any(got.get(k) != v for k, v in T_PINS.items()):
        raise SystemExit(f"{T_SUMS.relative_to(ROOT)}: not the 6 committed lines with PREREG.md {T_PINS[PREREG][:8]}")


check_pins()
sys.path.insert(0, str(ROOT / "scripts/c_stage2"))
import decode2 as D2  # noqa: E402  stage-2 module, unchanged (imports stage2, which checks the stage-1 shas)
import stage2 as S2  # noqa: E402

C, G, lb, BM = S2.C, S2.G, S2.lb, D2.BM
LABEL = "TEST, ONE LOOK PER SET"
SCHEMA = "vsps.c_test.v1"
OUT_ROOT = Path("/root/outputs/c_test")  # CC-103a: every C test output on M3 lies under it
SETS = {"ov_test": {"src": "openviic", "dir": "c_ov_test", "n": 2001,
                    "ann": "uit-openviic-annotation-test.json"},  # the released file name (CC-103a point 3)
        "xm_test2500": {"src": "xm3600", "dir": "c_xm_test2500", "n": 2500, "ann": "xm_test2500_data.json"}}
for _k, _v in SETS.items():
    _v["image_dir"] = f"{_v['dir']}/images"
C.DATASETS.update({k: {"src": v["src"], "image_dir": v["image_dir"]} for k, v in SETS.items()})
E4_DIR, E4_N = "c_e4_dev299", 52  # CC-103a X3; the first 13 / 26 whole batches (b = 4 / 2) of the dev299 manifest
SCORED = {"ov_test_1941": "ov_test", "ov_test_2001": "ov_test", "xm_test2500": "xm_test2500",
          "xm_test2392": "xm_test2500"}  # §6.2: four scored sets, each with its own df and bootstrap matrix
TRUNC = {"00000000768.jpg", "00000001010.jpg", "00000005095.jpg"}  # CC-082 T6; lists.json truncated_protected_decoded
BRAW_TWINS = {"00000013129.jpg", "00000007592.jpeg", "00000012946.png"}  # CC-103a Q7 (v): refused by name
OV_EXT = {"jpg": 1930, "jpeg": 28, "png": 42, "JPG": 1}  # CC-103a Q7 (iv)
IMG = (".jpg", ".jpeg", ".png")  # discovery, case-insensitive (stage2.py:244); refusal covers every file
MEMORY = {"datasets/ktvic/train_data.json": "72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f",
          "datasets/openviic/uit-openviic-annotation-train.json":
              "d757520e76b8490df6c7275c2beb8b3ecef0342635a436bea8c3cfd07eb49df0"}  # C.memory_captions' two sources
XM_VI_FULL = "101d24ad98e9dec43625ee425fa1b49aa1bde98f9609945bf5dd4424fef1dacc"  # XM3600 Vietnamese full_data.json
INFINITE, MAIN = S2.INFINITE, S2.MAIN


def tpinned(rel: str) -> Path:
    p = ROOT / rel
    if sha_file(p) != T_PINS[rel]:
        raise SystemExit(f"{rel}: sha256 differs from the test pin")
    return p


def out_ok(p: Path | str) -> Path:
    """CC-103a: on a GPU host, a C test output outside /root/outputs/c_test/ is refused."""
    p = Path(p)
    if os.environ.get("VSPS_MACHINE_ID") and not p.resolve().is_relative_to(OUT_ROOT):
        raise SystemExit(f"REFUSED: {p} is not under {OUT_ROOT}")
    return p


# ------------------------------------------------------------------------------------------------ sets (§3, W6)
def ov_rows(lists: dict) -> list[tuple[str, str, str]]:
    """[(name, name, sha256)] of OV-test in the pinned TSV order (sorted names), checked as CC-103 W2 / CC-103a."""
    rows = [(n, n, h) for n, h in (x.split("\t") for x in tpinned(TSV).read_text(encoding="utf-8").splitlines())]
    names, shas = [r[1] for r in rows], {r[2] for r in rows}
    ext = Counter(n.rsplit(".", 1)[1] for n in names)
    ok = (len(rows) == len(set(names)) == 2001 and len(shas) == 1997 and names == sorted(names) and ext == OV_EXT
          and set(names) <= set(lists["refuse"]["openviic_files"]) and shas <= set(lists["refuse"]["image_sha256"])
          and TRUNC <= set(names) and not BRAW_TWINS & set(names))
    if not ok:
        raise SystemExit("ov_test_files.tsv: not 2,001 names / 1,997 sha256 with the 1,930/28/42/1 extensions")
    return rows


def xm_rows(lists: dict) -> list[tuple[str, str, str]]:
    rows = [tuple(r) for r in lists["sets"]["xm_test2500"]]  # the stored order, not re-sorted (W6)
    if len(rows) != 2500 or len({r[0] for r in rows}) != 2500 or len({r[2] for r in rows}) != 2500:
        raise SystemExit("xm_test2500: not 2,500 distinct (id, file, sha256) rows")
    return rows


def three108(lists: dict) -> list[str]:
    ids = tpinned(T108).read_text(encoding="utf-8").split()
    if len(ids) != 108 or not set(ids) <= {r[0] for r in xm_rows(lists)}:
        raise SystemExit("xm_test2500_threeref108.txt: not 108 ids inside xm_test2500 (CC-103 W14)")
    return ids


def set_rows(ds: str, lists: dict) -> list[tuple[str, str, str]]:
    if ds not in SETS:
        raise SystemExit(f"REFUSED: the test decodes only {sorted(SETS)}, not {ds}")
    return ov_rows(lists) if ds == "ov_test" else xm_rows(lists)


def scored_ids(name: str, lists: dict) -> list[str]:
    """The pinned image order of a scored set (W6): OV TSV order (1,941 filtered); XM lists order (2,392 filtered)."""
    ids = [r[0] for r in set_rows(SCORED[name], lists)]
    if name == "ov_test_1941":
        p = tpinned(P1941).read_text(encoding="utf-8").split()
        near = set(S2.pinned(S2.OVT60).read_text(encoding="utf-8").split())
        if p != [i for i in ids if i not in near] or len(p) != 1941:
            raise SystemExit("ov_test_primary1941.txt: not the TSV order minus the 60 (737e617a)")
        return p
    if name == "xm_test2392":
        drop = set(three108(lists))
        return [i for i in ids if i not in drop]
    return ids


# ------------------------------------------------------------------------------------------------ refusal (§11.2, W13)
def carve(block: str, lists: dict) -> tuple[set[str], set[str]]:
    """(sha256s, OpenViIC names) carved out for the active block only: OV 1,997 sha / 2,001 names; XM 2,500 sha."""
    if block == "ov":
        rows = ov_rows(lists)
        return {r[2] for r in rows}, {r[1] for r in rows}
    if block == "xm":
        return {r[2] for r in xm_rows(lists)}, set()
    return set(), set()


def refused_t(lists: dict, block: str) -> tuple[dict[str, set[str]], set[str]]:
    """The stage-1 refusal minus the active block's carve-out, with the asserts that every other test or dev-B set
    (and the B-raw names, the 3 twins included) stays refused."""
    ids, hashes = C.refused(lists)
    ex = json.loads(C.pinned(C.EXCL).read_text(encoding="utf-8"))
    shas, names = carve(block, lists)
    if not (shas <= hashes and names <= ids["openviic"]):
        raise SystemExit("carve-out: a carved-out image was not refused in stage 1")
    if block == "xm" and {r[0] for r in xm_rows(lists)} & ids["xm3600"]:
        raise SystemExit("carve-out: an XM600 id is in XM-test2500")
    ids2, hashes2 = {**ids, "openviic": ids["openviic"] - names}, hashes - shas
    ov = {r[2] for r in ov_rows(lists)}
    xm = {r[2] for r in xm_rows(lists)}
    stay = [{r[2] for r in lists["sets"][s]} for s in ("ov_dev_b", "xm_dev500")]
    stay += [set(lists["refuse"]["image_sha256"]) - shas, ov if block != "ov" else set(),
             xm if block != "xm" else set(), set(ex["image_sha256"]["xm3600_all_images"]) - xm]
    stay += [set(v) for n, v in ex["image_sha256"].items() if n != "xm3600_all_images"]
    braw = set(lists["refuse"]["openviic_files"]) - {r[1] for r in ov_rows(lists)}
    if (not all(s <= hashes2 for s in stay) or not braw | BRAW_TWINS <= ids2["openviic"]
            or ids2["xm3600"] != ids["xm3600"] or ids2["ktvic"] != ids["ktvic"]):
        raise SystemExit("carve-out: a test or dev-B set would no longer be refused")
    return ids2, hashes2


def manifest_t(ds: str, lists: dict) -> list[tuple[str, str, str]]:
    """[(id, file, sha256)] of a test set, refused unless every row is in the active block's carve-out."""
    rows = set_rows(ds, lists)
    C.refuse_rows(rows, SETS[ds]["src"], *refused_t(lists, "ov" if ds == "ov_test" else "xm"))
    return rows


# ------------------------------------------------------------------------------------------------ folders and refs
def ann_file(ds: str, data: Path | None = None) -> Path:
    return (data or lb.DATA) / "datasets" / SETS[ds]["dir"] / SETS[ds]["ann"]


def check_folder(ds: str, lists: dict, data: Path | None = None) -> dict:
    """CC-103 W13 with CC-103a point 3 and Q7: the folder holds images/ with exactly the set's files (exact case,
    sha-checked, every file whatever its extension) and exactly one non-image file, fixed by name, whose key set is
    the set. Returns its sha256 and key count for the run record."""
    data = data or lb.DATA
    top = data / "datasets" / (E4_DIR if ds == "e4_dev299" else SETS[ds]["dir"])
    want = {f: h for _i, f, h in (C.manifest("ktvic_dev299", lists) if ds == "e4_dev299" else set_rows(ds, lists))}
    fixed = None if ds == "e4_dev299" else SETS[ds]["ann"]
    if not top.is_dir():
        raise SystemExit(f"REFUSED: {top} is missing")
    extra = [p.name for p in top.iterdir() if p.name not in ("images", fixed)]
    files = [p for p in (top / "images").rglob("*") if not p.is_dir()]
    stray = [str(p.relative_to(top)) for p in files if p.parent != top / "images" or p.name not in want]
    got = {p.name: sha_file(p) for p in files if p.name in want and p.parent == top / "images"}
    bad = [n for n, h in got.items() if want[n] != h]
    if extra or stray or bad or len(got) != len(want):
        raise SystemExit(f"REFUSED: {top}: {len(got)}/{len(want)} files, {len(extra) + len(stray)} not in the set "
                         f"(e.g. {(extra + stray)[:3]}), {len(bad)} sha mismatches")
    rec = {"folder": top.name, "files": len(got), "distinct_sha256": len(set(got.values())),
           "extensions": dict(Counter(n.rsplit(".", 1)[1] for n in got))}
    if fixed:
        a = top / fixed
        if not a.is_file():
            raise SystemExit(f"REFUSED: {a} is missing")
        keys = ann_keys(ds, a)
        if keys != {i for i, _f, _h in set_rows(ds, lists)}:
            raise SystemExit(f"REFUSED: {a}: its key set is not the {ds} set")
        rec |= {"ann": fixed, "ann_sha256": sha_file(a), "ann_keys": len(keys)}
    if ds == "ov_test" and rec["extensions"] != OV_EXT:
        raise SystemExit(f"REFUSED: extensions {rec['extensions']} are not {OV_EXT}")
    return rec


def ann_keys(ds: str, path: Path) -> set[str]:
    d = json.loads(path.read_text(encoding="utf-8"))
    if ds == "ov_test":
        return set(d)
    if d.get("release_sha256") != XM_VI_FULL:  # Vietnamese references only (CC-103a point 3)
        raise SystemExit(f"{path}: not cut from the Vietnamese XM3600 release {XM_VI_FULL[:8]}")
    ids = {str(i["id"]) for i in d["images"]}
    if {str(a["image_id"]) for a in d["annotations"]} != ids:
        raise SystemExit(f"{path}: an image has no reference, or a reference has no image")
    return ids


def references_t(ds: str, lists: dict, data: Path | None = None) -> dict[str, list[str]]:
    """{image id: references} of a test set from its one annotation file, as stage2.references2 reads them."""
    p = ann_file(ds, data)
    ids = {i for i, _f, _h in manifest_t(ds, lists)}
    if ann_keys(ds, p) != ids:
        raise SystemExit(f"{p}: not the {ds} set")
    d = json.loads(p.read_text(encoding="utf-8"))
    if ds == "ov_test":
        return {f: [c.strip() for c in d[f]["captions"]] for f in ids}
    out: dict[str, list[str]] = {}
    for a in d["annotations"]:
        out.setdefault(str(a["image_id"]), []).append(a["caption"])
    return out


def cmd_xm_subset(a) -> None:
    """E6 step 3 (local, at staging): the 2,500-image Vietnamese reference subset, values unchanged (as
    stage2.cmd_subsets), with the release sha256 inside. Only sha and counts are printed."""
    if os.environ.get("VSPS_MACHINE_ID"):
        raise SystemExit("xm-subset runs locally, where the release is; not on a GPU host")
    if sha_file(a.xm_full) != XM_VI_FULL:
        raise SystemExit(f"{a.xm_full}: not the Vietnamese XM3600 full_data.json {XM_VI_FULL[:8]}")
    ids = {r[0] for r in xm_rows(C.load_lists(a.lists))}
    full = json.loads(Path(a.xm_full).read_text(encoding="utf-8"))
    sub = {"release_sha256": XM_VI_FULL, "images": [i for i in full["images"] if str(i["id"]) in ids],
           "annotations": [x for x in full["annotations"] if str(x["image_id"]) in ids]}
    if len(sub["images"]) != 2500 or ann_keys("xm_test2500", _dump(a.out, sub)) != ids:
        raise SystemExit("xm-subset: not the 2,500 XM-test2500 images")
    print(json.dumps({"file": Path(a.out).name, "sha256": sha_file(a.out), "keys": 2500,
                      "annotations": len(sub["annotations"])}))


def _dump(path: Path, obj) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)
    return Path(path)


# ------------------------------------------------------------------------------------------------ host check
def check_host(block: str, lists: dict, data: Path | None = None, repo: Path = ROOT) -> dict:
    """§11.2 (CC-103 W13, CC-103a): the stage-2 absences, the memory sources at their pins, the refused set minus the
    active block's carve-out, the B-raw names (twins included) by name, the active folder exact, every other C test
    folder absent. E4: dev299 only, no test file of any paper. Other papers' test images are counted (ov, xm)."""
    data = data or lb.DATA
    ds_dir = data / "datasets"
    ex = json.loads(C.pinned(C.EXCL).read_text(encoding="utf-8"))["image_sha256"]
    present = sorted(p.name for p in ds_dir.iterdir()) if ds_dir.is_dir() else []
    files = [p for p in ds_dir.rglob("*") if p.is_file()] if ds_dir.is_dir() else []
    bad = [n for n in ("xm3600", "xm3600_en", "e_dev_a_pairs", "c_xm_dev500") if n in present]
    active = {"e4": E4_DIR, "ov": SETS["ov_test"]["dir"], "xm": SETS["xm_test2500"]["dir"]}
    bad += [f"{d} present in the {block} block" for b, d in active.items() if b != block and d in present]
    bad += [str(p) for root in (repo, data) for p in root.rglob("oiv7_labels.json")]
    bad += [str(p) for p in files if p.name in ("full_data.json", "test_data.json")]  # XM3600 refs, KTVIC test
    bad += [str(p) for p in files if p.name == SETS["ov_test"]["ann"] and p != ann_file("ov_test", data)]
    devb = {r[0] for r in lists["sets"]["ov_dev_b"]}
    bad += [str(p) for p in files if p.name == "uit-openviic-annotation-dev.json"
            and devb & set(json.loads(p.read_text(encoding="utf-8")))]
    bad += [f"{rel} missing or not at its pin" for rel, h in MEMORY.items()
            if not (data / rel).is_file() or sha_file(data / rel) != h]
    shas = {p: sha_file(p) for p in files if p.suffix.lower() in IMG}
    c_shas, c_names = carve(block, lists)
    fail = (set(lists["refuse"]["image_sha256"]) - c_shas) | {r[2] for s in ("ov_dev_b", "xm_dev500")
                                                               for r in lists["sets"][s]}
    if block == "xm":
        fail |= set(ex["xm3600_all_images"]) - c_shas  # XM600 and XM-dev500
    if block == "e4":
        fail |= {h for v in ex.values() for h in v}  # no test file of any paper (CC-103a X3)
    names_refused = set(lists["refuse"]["openviic_files"]) - c_names
    home = ds_dir / active[block] / "images"
    # names are refused outside the active images/ folder only (CC-103b W1: KTVIC and OpenViIC share 11-digit names;
    # inside it check_folder tests every file by exact name and sha); the sha test covers every file
    hit = [str(p) for p in files if p.parent != home and (p.name in names_refused or p.name in c_names)]
    hit += [str(p) for p, h in shas.items() if h in fail or (h in c_shas and p.parent != home)]
    folder = check_folder({"e4": "e4_dev299", "ov": "ov_test", "xm": "xm_test2500"}[block], lists, data)
    have = set(shas.values())
    rec = {"block": block, "utc": lb.utc(), "datasets": present, "image_files": len(shas), "files": len(files),
           "refused_present": len(hit), "problems": bad, "folder": folder,
           "memory_sha256": {rel: MEMORY[rel] for rel in MEMORY},
           "other_papers_test_images_present": {n: len(have & set(v)) for n, v in ex.items()}}
    if hit or bad:
        print(json.dumps({k: v for k, v in rec.items() if k != "folder"} | {"examples": hit[:3]}))
        raise SystemExit("host check failed: back to the operator")
    return rec


# ------------------------------------------------------------------------------------------------ CC-082 T6 (W3)
def strict_ok(path: Path) -> bool:
    from PIL import Image

    try:
        with Image.open(path) as im:
            im.convert("RGB")
        return True
    except OSError:
        return False


def t6(step: str, paths: list[Path], call, log: Path | None):
    """Around one call of a pinned image-opening step: strict first; if it fails, every file of the call is probed
    strictly; only the 3 named files may fail, and then the same call (same batch) runs once more with PIL
    LOAD_TRUNCATED_IMAGES set and reset around it. Any other failure is a JOB STOP; a failure after the retry is
    CC-082 T5 and also stops, for the record and the judge. Retried files are logged per step."""
    from PIL import ImageFile

    if ImageFile.LOAD_TRUNCATED_IMAGES:
        raise SystemExit("LOAD_TRUNCATED_IMAGES is set outside a T6 retry")
    try:
        return call()
    except OSError as e:
        failed = [p for p in paths if not strict_ok(p)]
        if not failed or any(p.name not in TRUNC for p in failed):
            raise SystemExit(f"JOB STOP (CC-103 W3): strict decode failed outside the 3 named files "
                             f"{[p.name for p in failed if p.name not in TRUNC] or type(e).__name__}") from None
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    try:
        out = call()
    except OSError:
        raise SystemExit(f"JOB STOP (CC-082 T5): {[p.name for p in failed]} unreadable after the retry; record "
                         "unreadable_test_excluded and return to the judge") from None
    finally:
        ImageFile.LOAD_TRUNCATED_IMAGES = False
    if log:
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps({"step": step, "files": sorted(p.name for p in failed), "utc": lb.utc()}) + "\n")
    return out


# ------------------------------------------------------------------------------------------------ frozen grid (§4)
def spec_t(cfg: dict, ds: str, model: str, arm: str) -> dict:
    """S2.spec unchanged, with the ct_ prefix (CC-103 OQ-7); no image-blind arm at test."""
    if ds not in SETS or arm not in MAIN:
        raise SystemExit(f"REFUSED: no test run for {ds} / {arm}")
    s = S2.spec(cfg, ds, model, arm)
    return {**s, "run_id": "ct_" + s["run_id"].removeprefix("c2_")}


def grid_t(cfg: dict) -> dict[str, dict]:
    return {s["run_id"]: s for s in (spec_t(cfg, ds, m, a) for ds in SETS for m in C.MODELS for a in MAIN)}


def verify_arms_t(cfg: dict, model: str) -> list[str]:
    """§4 (CC-103 OQ-2, W11): C-a lapses with P3. Only a finite frozen tau needs a verifier: InternVL3's ret, rand,
    fix. Qwen (tau -inf) gets no verifier pass."""
    return [] if cfg["models"][model]["tau"] in INFINITE else ["ret", "rand", "fix"]


def zs_ok_t(prov: dict, model: str, ds: str) -> None:
    """stage2.zs_ok2's identity tuple, with the test schema, the ct_ prefix and this wrapper's sha256."""
    reg = C.registration()
    m = reg["models"][model]
    same = tuple(prov.get(k) for k in ("hub_id", "revision", "prompt_text_sha256", "max_new_tokens",
                                        "generate_kwargs", "dataset", "packages")) == (
        m["hub_id"], m["revision"], C.ZS_PROMPT_SHA256, 60, {"max_new_tokens": 60, "do_sample": False, "num_beams": 1},
        ds, reg["venv"]["packages"])
    sp = prov.get("spec")
    own = (prov.get("c_schema") == SCHEMA and isinstance(sp, dict) and sp.get("arm") == "zs"
           and prov.get("run_id", "").startswith("ct_") and prov.get("wrapper_sha256") == sha_file(Path(__file__)))
    if not (same and own):
        raise SystemExit(f"{prov.get('run_id')}: not a test zero-shot run of {model} on {ds}")


# ------------------------------------------------------------------------------------------------ embed, examples
def cmd_embed(a) -> None:
    """decode2.cmd_embed on a test set: the same SigLIP2 checks, fp16, batch 64, with the T6 wrapper per batch."""
    import torch
    from PIL import Image
    from transformers import AutoModel, AutoProcessor

    out = out_ok(a.out)
    lists = C.load_lists(a.lists)
    rows = manifest_t(a.set, lists)
    check_folder(a.set, lists)
    _k, _v, meta1 = D2.load_emb1(a.emb1)
    snap = {p.name: S2.sha_file(p) for p in sorted(Path(a.snapshot).iterdir()) if p.is_file()}
    if a.revision != meta1["revision"] or snap != meta1["snapshot_sha256"]:
        raise SystemExit("SigLIP2 revision or snapshot differs from the stage-1 embeddings")
    BM.need_licence(BM.card_licence(Path(a.snapshot) / "README.md"), f"{BM.SIGLIP2} model card")
    folder = lb.DATA / "datasets" / SETS[a.set]["image_dir"]
    proc = AutoProcessor.from_pretrained(a.snapshot)
    net = AutoModel.from_pretrained(a.snapshot, torch_dtype=torch.float16).eval().cuda()
    vecs = []
    for lo in range(0, len(rows), 64):
        paths = [folder / f for _i, f, _h in rows[lo:lo + 64]]
        if any(S2.sha_file(p) != h for p, (_i, _f, h) in zip(paths, rows[lo:lo + 64])):
            raise SystemExit(f"{folder}: a sha256 differs from the manifest")
        ims = t6(f"embed_{a.set}", paths, lambda ps=paths: [Image.open(p).convert("RGB") for p in ps],
                 out.parent / f"t6_retry_{a.set}.jsonl")
        with torch.no_grad():
            v = net.get_image_features(**proc(images=ims, return_tensors="pt").to("cuda", torch.float16)).float()
        vecs.append(torch.nn.functional.normalize(v, dim=-1).cpu().numpy())
    meta = {**{k: meta1[k] for k in ("model", "revision", "licence", "readme_sha256", "snapshot_sha256")},
            "set": a.set, "lists_sha256": S2.sha_file(a.lists), "stage1_emb_sha256": S2.EMB1_SHA256,
            "prereg_sha256": T_PINS[PREREG], "label": LABEL}
    np.savez(out, keys=np.array([f"{a.set}|{i}" for i, _f, _h in rows]), vecs=np.concatenate(vecs),
             meta=json.dumps(meta))
    Path(str(out) + ".sha256").write_text(f"{S2.sha_file(out)}  {out.name}\n")


def make_exemplars(ds: str, rows: list, emb1: Path, emb: Path, lists_path: Path, scored: dict[str, list[str]]) -> dict:
    """decode2.build_exemplars on the stage-1 memory and one set, plus the dose tertile cuts of every scored set of
    that set from its own queries (CC-103 OQ-6, J8), fixed before any caption exists."""
    mk, mv, _meta1 = D2.load_emb1(emb1)
    z = np.load(emb)
    meta = json.loads(str(z["meta"]))
    qk = [str(k) for k in z["keys"]]
    if (meta["set"], meta["lists_sha256"], meta["stage1_emb_sha256"]) != (ds, S2.sha_file(lists_path),
                                                                           S2.EMB1_SHA256) or \
            qk != [f"{ds}|{i}" for i, _f, _h in rows]:
        raise SystemExit(f"{emb}: not the {ds} query embeddings of this lists.json")
    ex = D2.build_exemplars(ds, mk, mv, qk, z["vecs"])
    cuts = {n: [float(x) for x in np.quantile([ex["ret"][ds][i][0][1] for i in ids], [1 / 3, 2 / 3])]
            for n, ids in scored.items()}
    return {"design_sha256": C.PINS[C.DESIGN], "lists_sha256": meta["lists_sha256"], "label": LABEL,
            "c_schema": SCHEMA, "prereg_sha256": T_PINS[PREREG], "set": ds,
            "emb_sha256": {"stage1": S2.EMB1_SHA256, ds: S2.sha_file(Path(emb))}, "near_cos": BM.NEAR_COS, **ex,
            "scored_dose_cuts": cuts}


def cmd_exemplars(a) -> None:
    out = out_ok(a.out)
    lists = C.load_lists(a.lists)
    ex = make_exemplars(a.set, manifest_t(a.set, lists), a.emb1, a.emb, a.lists,
                        {n: scored_ids(n, lists) for n, s in SCORED.items() if s == a.set})
    out.write_text(json.dumps(ex) + "\n", encoding="utf-8")
    Path(str(out) + ".sha256").write_text(f"{S2.sha_file(out)}  {out.name}\n")
    print(json.dumps({"set": a.set, "scored_dose_cuts": ex["scored_dose_cuts"]}))


# ------------------------------------------------------------------------------------------------ decode (GPU)
def decode_runs(run_ids: list[str], snapshot: Path, lists_path: Path, ex_path: Path, out_dir: Path) -> None:
    """decode2.decode_runs on the test grid: every refusal before the model loads."""
    g = grid_t(S2.frozen())
    if any(r not in g for r in run_ids):
        raise SystemExit(f"{next(r for r in run_ids if r not in g)}: not a test run")
    specs = [g[r] for r in run_ids]
    if len({(s["model"], s["dataset"]) for s in specs}) != 1:
        raise SystemExit("one model and one set per process")
    ds = specs[0]["dataset"]
    lists = C.load_lists(lists_path)
    ex = C.load_exemplars(ex_path, lists_path)
    if ex.get("set") != ds or ex.get("c_schema") != SCHEMA:
        raise SystemExit(f"{ex_path}: not the test example lists of {ds}")
    outs = [out_ok(out_dir / f"{s['run_id']}.preds.json") for s in specs]
    if any(o.exists() for o in outs):
        raise SystemExit("an output exists; a run is decoded once")
    plan = [(s, manifest_t(ds, lists)) for s in specs]
    plan = [(s, items, C.check_exemplars(items, s, ex, lists)) for s, items in plan]
    check_folder(ds, lists)
    ctx = load_ctx(specs[0]["model"], snapshot, lists, ex_path)
    for (s, items, exids), out in zip(plan, outs):
        decode_one_t(s, items, exids, out, ctx, lb.DATA / "datasets" / SETS[ds]["image_dir"])


def load_ctx(model: str, snapshot: Path, lists: dict, ex_path: Path) -> dict:
    reg = C.registration()
    m = reg["models"][model]
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit(f"package versions {lb.packages()} differ from the B-N1 venv")
    lb.check_snapshot(m, snapshot)
    ctx = {"caps": C.memory_captions(lists), "zs": lb.prompt_text(reg, "short"), "m": m, "ex_path": ex_path,
           "n_new": reg["decode"]["max_new_tokens"]["short"]}
    ctx["proc"], ctx["net"] = lb.load(m, snapshot, "cuda:0")
    return ctx


def decode_one_t(s: dict, items: list, exids: dict, out: Path, ctx: dict, folder: Path) -> dict:
    """decode2.decode_one (image arms) with the pinned lb.make_generate wrapped by t6, and the test provenance."""
    import torch

    proc, net, m, zs, n_new = (ctx[k] for k in ("proc", "net", "m", "zs", "n_new"))
    started = lb.utc()
    texts = D2.prompts(s, items, exids, ctx["caps"], zs)
    base = lb.make_generate(proc, net, zs, n_new, folder)
    t6log = out.parent / f"t6_retry_{s['dataset']}.jsonl"

    def gen(sl):
        return t6(s["run_id"], [folder / f for _i, f, _h in sl], lambda: base(sl, [texts[i] for i, _f, _h in sl]),
                  t6log)

    kw = {"max_new_tokens": n_new, "do_sample": False, "num_beams": 1}
    tsha = {i: C.sha(t) for i, t in texts.items()}
    part = Path(str(out) + ".partial.jsonl")
    resumed = part.exists()
    key = lb.run_key(C.PINS[C.B_N1], s, m, kw, json.dumps(tsha, sort_keys=True), items)
    rows = lb.decode_slices(items, m["batch_size"], gen, part, key)
    solo = [gen([it])[0][0] for it in items[:m["batch_size"]]] if m["batch_size"] > 1 else []
    status = lb.git("status", "--porcelain", "--untracked-files=no")
    prov = {"schema": lb.SCHEMA, "c_schema": SCHEMA, "label": LABEL, "design": C.DESIGN,
            "design_sha256": C.PINS[C.DESIGN], "c_prereg": PREREG, "c_prereg_sha256": T_PINS[PREREG],
            "frozen_config_sha256": S2.PINS[S2.FROZEN],
            "prereg_id": "B-N1 model blocks (decoder registration)", "prereg_sha256": C.PINS[C.B_N1],
            "decoder_sha256": C.PINS["scripts/lb/decode_hf_vlm.py"], "wrapper_sha256": sha_file(Path(__file__)),
            "run_id": s["run_id"], "spec": s, "model": s["model"], "hub_id": m["hub_id"], "revision": m["revision"],
            "dataset": s["dataset"], "image_input": True,
            "prompt_mode": "short" if s["arm"] == "zs" else f"icl-{s['tpl']}",
            "prompt_text_sha256": C.ZS_PROMPT_SHA256 if s["arm"] == "zs" else C.TEMPLATE_SHA256,
            "prompt_sha256_per_image": tsha, "exemplars": exids, "manifest_sha256": C.sha(json.dumps(items)),
            "lists_sha256": C.LISTS_SHA256, "exemplars_sha256": S2.sha_file(ctx["ex_path"]), "max_new_tokens": n_new,
            "batch_size": m["batch_size"], "dtype": m["dtype"], "attn_implementation": m["attn_implementation"],
            "processor_kwargs": m["processor_kwargs"], "generation_config": net.generation_config.to_diff_dict(),
            "machine_id": os.environ.get("VSPS_MACHINE_ID"), "git_head": lb.git("rev-parse", "HEAD"),
            "git_dirty": None if status is None else bool(status), "job_sha256": os.environ.get("VSPS_JOB_SHA256"),
            "venv_freeze_sha256": os.environ.get("VSPS_VENV_FREEZE_SHA256"), "packages": lb.packages(),
            "n_images": len(items), "resumed": resumed, "started_utc": started, "finished_utc": lb.utc(),
            "parity_slice0": {"n": len(solo), "identical": sum(a == r["caption"] for a, r in zip(solo, rows))},
            "gpu": torch.cuda.get_device_name(0), "cuda": torch.version.cuda, "generate_kwargs": kw}
    lb.write_output(out, prov, rows)
    print(f"wrote {out.name}")
    return {r["image_id"]: r["caption"] for r in rows} | {"_prompt_sha": tsha}


def cmd_e4(a) -> None:
    """E4 (CC-103, CC-103a): the frozen ret arm re-decodes the first E4_N dev299 images, from c_e4_dev299/images,
    through decode_one_t; >= 95% identical captions to the stage-1 preds of the frozen run passes, and every prompt
    sha256 must equal stage 1's. Only counts are written."""
    cfg = S2.frozen()
    rid = cfg["models"][a.model]["stage1_run_id"]
    s1 = C.run_spec(rid)
    out = out_ok(a.out_dir / f"e4_{a.model}.json")
    if out.exists():
        raise SystemExit(f"{out} exists; E4 runs once per rental")
    lists = C.load_lists(a.lists)
    sums = check_stage1_outputs(a.stage1, [f"runs/{rid}.preds.json", "exemplars.json"])
    ref = G.read_preds(a.stage1 / f"runs/{rid}.preds.json")
    items = C.manifest("ktvic_dev299", lists)[:E4_N]
    ex = C.load_exemplars(a.stage1 / "exemplars.json", a.lists)
    exids = C.check_exemplars(items, s1, ex, lists)
    check_folder("e4_dev299", lists)
    ctx = load_ctx(a.model, a.snapshot, lists, a.stage1 / "exemplars.json")
    spec = {**s1, "run_id": f"ct_e4_{rid}"}
    got = decode_one_t(spec, items, exids, out_ok(a.out_dir / f"ct_e4_{rid}.preds.json"), ctx,
                       lb.DATA / "datasets" / E4_DIR / "images")
    same = sum(got[i] == ref["predictions"][i] for i, _f, _h in items)
    prompts = all(got["_prompt_sha"][i] == ref["prompt_sha256_per_image"][i] for i, _f, _h in items)
    rec = {"model": a.model, "stage1_run_id": rid, "n": len(items), "identical": same,
           "pct": round(100 * same / len(items), 2), "prompts_identical": prompts,
           "passed": prompts and 100 * same / len(items) >= 95, "stage1_sha256": sums, "utc": lb.utc()}
    out.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    print(json.dumps({k: rec[k] for k in ("model", "n", "identical", "pct", "prompts_identical", "passed")}))
    if not rec["passed"]:
        raise SystemExit("E4 FAILED: the rebuild is not faithful; stop and return to the judge")


def check_stage1_outputs(d: Path, rels: list[str]) -> dict[str, str]:
    """The stage-1 output files E4 reads must match the stage-1 outputs' own SHA256SUMS."""
    sums = dict(reversed(x.split(maxsplit=1)) for x in (d / "SHA256SUMS").read_text().splitlines())
    got = {r: S2.sha_file(d / r) for r in rels}
    if any(sums.get(r) != h for r, h in got.items()):
        raise SystemExit(f"{d}: a stage-1 output differs from its SHA256SUMS")
    return got


# ------------------------------------------------------------------------------------------------ guard (§4, W11)
def cmd_items(a) -> None:
    lists = C.load_lists(a.lists)
    cfg = S2.frozen()
    runs, zs = [G.read_preds(p) for p in a.runs], G.read_preds(a.zs)
    model = zs["model"]
    want = {spec_t(cfg, a.set, model, arm)["run_id"] for arm in verify_arms_t(cfg, model)}
    if not want:
        raise SystemExit(f"REFUSED: {model} gets no verifier pass at test (CC-103 OQ-2)")
    if ({r["run_id"] for r in runs} != want or {(r["model"], r["dataset"]) for r in runs + [zs]} != {(model, a.set)}
            or any(r.get("c_schema") != SCHEMA for r in runs)):
        raise SystemExit(f"items: the runs must be exactly the test runs {sorted(want)}")
    zs_ok_t(zs, model, a.set)
    rows = G.items(runs, zs, C.memory_captions(lists))
    out_ok(a.out).write_text("".join(json.dumps({**r, "generator": model}) + "\n" for r in rows), encoding="utf-8")
    print(f"{len(rows)} neighbour-only items")


def verifier_plan(cfg: dict, generator: str) -> str:
    """The only verifier that runs at test: Qwen3-VL-8B on InternVL3's items (image-conditioned and no-image pass)."""
    if not verify_arms_t(cfg, generator) or G.VERIFIER[generator] != "qwen3vl_8b":
        raise SystemExit(f"REFUSED: no verifier pass for {generator}'s items at test (CC-103 OQ-2, CC-103a point 2)")
    return G.VERIFIER[generator]


def stop_marker(out: Path, ds: str) -> Path:
    return out.parent / f"{ds}_VERIFIER_STOP.json"


def registered_fill(out: Path, ds: str, fill):
    """W16: the Qwen3-VL answer-position stop (guard.answer_position_check) is registered and final for the set: a
    marker under c_test, exit code 3, no retry (a resumed process would ask other items first). The job then scores
    InternVL3 at -inf and +inf only, and decide reports the set's InternVL3 frozen arms as incomplete."""
    try:
        return fill()
    except SystemExit as e:
        if "not the answer position" not in str(e):
            raise
        stop_marker(out, ds).write_text(json.dumps({"set": ds, "stop": str(e), "utc": lb.utc()}) + "\n")
        print(f"REGISTERED VERIFIER STOP (W16) on {ds}")
        sys.exit(3)


def cmd_verify(a) -> None:
    out = out_ok(a.out)
    if stop_marker(out, a.set).exists():
        print(f"REGISTERED VERIFIER STOP (W16) on {a.set} is recorded; the verifier pass does not run again")
        sys.exit(3)
    lists = C.load_lists(a.lists)
    todo = [json.loads(x) for x in Path(a.items).read_text(encoding="utf-8").splitlines() if x]
    gens = {t["generator"] for t in todo}
    if len(gens) != 1:
        raise SystemExit("the items are not one generator's")
    verifier = verifier_plan(S2.frozen(), gens.pop())
    folder = lb.DATA / "datasets" / SETS[a.set]["image_dir"]
    paths = {(a.set, i): (folder / f, h) for i, f, h in manifest_t(a.set, lists)}
    if any((t["dataset"], t["image_id"]) not in paths for t in todo):
        raise SystemExit(f"REFUSED: an item image is not in the {a.set} manifest")
    check_folder(a.set, lists)
    reg = C.registration()
    if lb.packages() != reg["venv"]["packages"]:
        raise SystemExit("the Qwen3-VL verifier runs in the B-N1 venv")
    lb.check_snapshot(reg["models"][verifier], a.snapshot)
    load, ask, about = G.hf_verifier(reg["models"][verifier], a.snapshot)

    def checked(path_sha):
        path, h = path_sha
        if lb.sha256_file(path) != h:
            raise SystemExit(f"{path}: sha256 differs from the manifest")
        return t6(f"verify_{a.set}", [path], lambda: load(path), out.parent / f"t6_retry_{a.set}.jsonl")

    n = registered_fill(out, a.set, lambda: G.fill(out, todo, paths, (checked, ask), G.s2()["verifier_protocol"],
                                                   verifier))
    mass = sorted(about.pop("yes_no_mass"))
    about["yes_no_mass_median"] = mass[len(mass) // 2] if mass else None
    Path(str(out) + ".about.json").write_text(json.dumps({**about, "verifier": verifier, "label": LABEL,
                                                          "c_prereg_sha256": T_PINS[PREREG],
                                                          "packages": lb.packages(), "new_rows": n}) + "\n")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def under_root(tmp: str):
    """Selftest only: point OUT_ROOT at the temp dir, so out_ok holds on a GPU host too (VSPS_MACHINE_ID set by the
    job); returns the previous root to restore."""
    global OUT_ROOT
    old, OUT_ROOT = OUT_ROOT, Path(tmp).resolve()
    return old


def qwen_guard_selftest(cfg: dict) -> None:
    """CC-103a point 2: drive Qwen's guard path (items, then verify) with every verifier loader replaced by one that
    fails if called; both refuse before any load. InternVL3's items are planned for Qwen3-VL only."""
    calls = []

    def loaded(*_a):
        calls.append(1)
        raise AssertionError("a verifier was loaded")

    saved = G.s2_verifier, G.hf_verifier
    G.s2_verifier = G.hf_verifier = loaded
    lp = ROOT / "manuscript/prereg/2026-10-22_c_stage1/lists.json"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            old = under_root(tmp)
            zs, items = Path(tmp) / "zs.json", Path(tmp) / "i.jsonl"
            zs.write_text(json.dumps({"model": "qwen25vl_7b", "dataset": "ov_test"}))
            items.write_text(json.dumps({"dataset": "ov_test", "image_id": "a", "class": "c",
                                         "generator": "qwen25vl_7b"}) + "\n")
            ns = argparse.Namespace(set="ov_test", runs=[zs], zs=zs, lists=lp, out=Path(tmp) / "o", items=items,
                                    snapshot=Path(tmp))
            assert C.refuses(lambda: cmd_items(ns)) and C.refuses(lambda: cmd_verify(ns)), "Qwen: no verifier pass"
            under_root(old)
    finally:
        G.s2_verifier, G.hf_verifier = saved
    assert not calls and verifier_plan(cfg, "internvl3_8b") == "qwen3vl_8b", "no verifier loaded; Qwen3-VL only"
    with tempfile.TemporaryDirectory() as tmp:
        old = under_root(tmp)
        out = Path(tmp) / "ov_test_internvl3_8b.cache.jsonl"

        def stopped():
            G.answer_position_check([0.1] * 20)

        try:
            registered_fill(out, "ov_test", stopped)
            raise AssertionError("the answer-position stop did not fire")
        except SystemExit as e:
            assert e.code == 3 and stop_marker(out, "ov_test").is_file(), "W16 stop: marker and exit code 3"
        ns = argparse.Namespace(out=out, set="ov_test")
        try:
            cmd_verify(ns)
            raise AssertionError("a recorded verifier stop did not stop cmd_verify")
        except SystemExit as e:
            assert e.code == 3, "a recorded verifier stop is final"
        under_root(old)
        assert C.refuses(lambda: registered_fill(out, "xm_test2500", lambda: sys.exit("other failure"))), "re-raised"
        assert not stop_marker(out, "xm_test2500").exists()


def write_img(path: Path, mode: str, truncate: bool = False) -> None:
    """A synthetic 64 x 64 noise image (no dataset content) in the given PIL mode; format from the suffix."""
    from PIL import Image

    px = np.random.default_rng(int(hashlib.sha256(path.name.encode()).hexdigest()[:8], 16)).integers(0, 256, (64, 64, 4), dtype=np.uint8)
    im = Image.fromarray(px[:, :, :len(mode)] if mode != "P" else px[:, :, 0], {"P": "L"}.get(mode, mode))
    if mode == "P":
        im = im.convert("P")
    fmt = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG"}[path.suffix.lower()]
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, fmt)
    if truncate:
        b = path.read_bytes()
        path.write_bytes(b[:len(b) * 2 // 3])


def selftest() -> None:
    from PIL import Image, ImageFile

    cfg = S2.frozen()
    g = grid_t(cfg)
    assert len(g) == 16 and all(r.startswith("ct_") for r in g) and not any("blind" in r for r in g), "16 ct_ runs"
    assert C.refuses(lambda: spec_t(cfg, "ov_dev_b", "qwen25vl_7b", "ret")), "no test run on a dev set"
    assert C.refuses(lambda: spec_t(cfg, "ov_test", "qwen25vl_7b", "blind")), "no blind arm at test"
    assert verify_arms_t(cfg, "qwen25vl_7b") == [] and verify_arms_t(cfg, "internvl3_8b") == ["ret", "rand", "fix"]
    lists = C.load_lists(ROOT / "manuscript/prereg/2026-10-22_c_stage1/lists.json")
    qwen_guard_selftest(cfg)
    ov, xm = manifest_t("ov_test", lists), manifest_t("xm_test2500", lists)
    assert len(ov) == 2001 and len({r[2] for r in ov}) == 1997 and len(xm) == 2500
    assert [len(scored_ids(n, lists)) for n in SCORED] == [1941, 2001, 2500, 2392]
    assert scored_ids("xm_test2500", lists) == [r[0] for r in lists["sets"]["xm_test2500"]], "XM: stored order (W6)"
    ids1, h1 = C.refused(lists)
    io, ho = refused_t(lists, "ov")
    ix, hx = refused_t(lists, "xm")
    assert len(h1 - ho) == 1997 and len(ids1["openviic"] - io["openviic"]) == 2001 and len(h1 - hx) == 2500
    assert BRAW_TWINS <= io["openviic"] and BRAW_TWINS <= ix["openviic"], "the B-raw twins stay refused by name"
    for blk, (ids2, hashes2) in (("ov", (io, ho)), ("xm", (ix, hx))):
        other = xm if blk == "ov" else ov
        assert C.refuses(lambda: C.refuse_rows(other[:1], "xm3600" if blk == "ov" else "openviic", ids2, hashes2))
        for s in ("ov_dev_b", "xm_dev500"):
            r = [tuple(lists["sets"][s][0])]
            assert C.refuses(lambda: C.refuse_rows(r, "openviic" if s == "ov_dev_b" else "xm3600", ids2, hashes2))
        assert C.refuses(lambda: C.refuse_rows([("1", "00000000001.jpg", "2" * 64)], "ktvic", ids2, hashes2))
        twin = sorted(BRAW_TWINS)[0]
        assert C.refuses(lambda: C.refuse_rows([(twin, twin, "4" * 64)], "openviic", ids2, hashes2)), "twin by name"
    assert C.refuses(lambda: set_rows("ov_dev_a", lists)) and three108(lists)[0] in {r[0] for r in xm}
    with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
        tmp = Path(tmp)
        (tmp / "X.JPG").write_bytes(b"x")
        assert not (tmp / "x.jpg").exists() and not (tmp / "X.jpg").exists(), "/tmp must be case-sensitive"
        (tmp / "X.JPG").unlink()
        t6_selftest(tmp)
        host_selftest(tmp, lists)
    assert not ImageFile.LOAD_TRUNCATED_IMAGES and Image.MAX_IMAGE_PIXELS
    mid = os.environ.get("VSPS_MACHINE_ID")  # the same checks on and off a GPU host
    os.environ["VSPS_MACHINE_ID"] = mid or "selftest"
    try:
        assert OUT_ROOT == Path("/root/outputs/c_test"), "the real output root is restored after the selftests"
        assert C.refuses(lambda: out_ok("/root/outputs/c_stage2/x.json")) and out_ok(OUT_ROOT / "a/b.json")
        assert C.refuses(lambda: out_ok(Path(tempfile.gettempdir()) / "x.json")), "a temp path is refused on a host"
        assert C.refuses(lambda: cmd_xm_subset(argparse.Namespace(lists=None, xm_full=None, out=None)))
    finally:
        if mid is None:
            del os.environ["VSPS_MACHINE_ID"]
    print("selftest ok: 16 ct_ runs, no blind arm, no Qwen verifier pass (never loaded), W16 verifier stop final, per-block carve-out "
          "(1,997/2,001 OV, 2,500 XM; other sets, dev-B, KTVIC test and the B-raw twins stay refused), scored sets "
          "1,941/2,001/2,500/2,392 in the pinned order, T6 retry (3 names only, whole call, flag reset; else JOB "
          "STOP), exact-case folders (.JPG, .jpeg, RGBA and palette png), host checks e4/ov/xm (a real dev299 name that is also an OpenViIC name passes in its folder, is refused outside), output root")


def t6_selftest(tmp: Path) -> None:
    from PIL import Image, ImageFile

    tr = sorted(TRUNC)[0]
    good, bad, other = tmp / "t6/a.jpg", tmp / f"t6/{tr}", tmp / "t6/00000000999.jpg"
    write_img(good, "RGB")
    write_img(bad, "RGB", truncate=True)
    write_img(other, "RGB", truncate=True)
    log = tmp / "t6.jsonl"
    seen = []

    def call(ps):
        seen.append(ImageFile.LOAD_TRUNCATED_IMAGES)
        return [Image.open(p).convert("RGB").size for p in ps]

    assert t6("s", [good], lambda: call([good]), log) == [(64, 64)] and not log.exists(), "strict path, no retry"
    assert t6("s", [good, bad], lambda: call([good, bad]), log) == [(64, 64)] * 2 and seen[-2:] == [False, True]
    assert json.loads(log.read_text())["files"] == [tr] and not ImageFile.LOAD_TRUNCATED_IMAGES, "logged, reset"
    assert C.refuses(lambda: t6("s", [good, other], lambda: call([good, other]), log)), "another truncated file"
    assert C.refuses(lambda: t6("s", [bad, other], lambda: call([bad, other]), log)) and \
        not ImageFile.LOAD_TRUNCATED_IMAGES, "a named file with another failing file: JOB STOP"
    gone = tmp / f"t6/{sorted(TRUNC)[1]}"
    gone.write_bytes(b"\xff\xd8 not an image")
    assert C.refuses(lambda: t6("s", [gone], lambda: call([gone]), log)) and not ImageFile.LOAD_TRUNCATED_IMAGES
    for name, mode in (("p.png", "RGBA"), ("q.png", "P"), ("r.jpeg", "RGB"), ("S.JPG", "RGB")):
        write_img(tmp / "modes" / name, mode)
        assert strict_ok(tmp / "modes" / name) and Image.open(tmp / "modes" / name).convert("RGB").mode == "RGB"


def host_selftest(tmp: Path, lists: dict) -> None:
    """check_host / check_folder on a synthetic $NCS_DATA. The test sets' names and shas cannot be used (no test
    image is opened or made), so the folder checks run on a small synthetic set substituted for each test set."""
    import shutil

    saved = (globals()["ov_rows"], globals()["xm_rows"], C.manifest)
    fake = {}
    for ds, names in (("ov_test", ["00000005495.JPG", "00000000001.png", "00000000002.jpeg", "00000000003.png",
                                   sorted(TRUNC)[0]]), ("xm_test2500", ["x1", "x2"]), ("e4_dev299", ["00000001008.jpg", "k2.jpg"])):
        d = tmp / "src" / ds
        rows = []
        for n, f in enumerate(names):
            f = f if f.endswith((".jpg", ".png", ".jpeg", ".JPG")) else f"{f}.jpg"
            write_img(d / f, ("RGB", "RGBA", "RGB", "P", "RGB")[n] if ds == "ov_test" else "RGB")
            rows.append((f if ds == "ov_test" else f.removesuffix(".jpg").lstrip("0"), f, sha_file(d / f)))
        fake[ds] = rows
    ov_s, xm_s = {r[2] for r in fake["ov_test"]}, {r[2] for r in fake["xm_test2500"]}
    ext_saved = dict(OV_EXT)
    OV_EXT.clear()
    OV_EXT.update({"JPG": 1, "png": 2, "jpeg": 1, "jpg": 1})
    lists2 = {**lists, "refuse": {"openviic_files": lists["refuse"]["openviic_files"] + [r[1] for r in fake[
        "ov_test"]], "image_sha256": lists["refuse"]["image_sha256"] + sorted(ov_s | xm_s)},
              "sets": {**lists["sets"], "xm_test2500": [list(r) for r in fake["xm_test2500"]]}}
    globals()["ov_rows"] = lambda _l: fake["ov_test"]
    globals()["xm_rows"] = lambda _l: fake["xm_test2500"]
    C.manifest = lambda ds, _l: fake["e4_dev299"] if ds == "ktvic_dev299" else saved[2](ds, _l)
    (tmp / "repo").mkdir()
    try:
        for block, ds in (("e4", "e4_dev299"), ("ov", "ov_test"), ("xm", "xm_test2500")):
            data = tmp / f"ncs_{block}"
            for rel in MEMORY:
                (data / rel).parent.mkdir(parents=True, exist_ok=True)
            mem_saved = dict(MEMORY)
            for rel in MEMORY:
                (data / rel).write_text("{}")
                MEMORY[rel] = sha_file(data / rel)
            top = data / "datasets" / (E4_DIR if block == "e4" else SETS[ds]["dir"])
            shutil.copytree(tmp / "src" / ds, top / "images")
            if block == "ov":
                (top / SETS[ds]["ann"]).write_text(json.dumps({r[0]: {"captions": ["w1"]} for r in fake[ds]}))
            if block == "xm":
                _dump(top / SETS[ds]["ann"], {"release_sha256": XM_VI_FULL, "images": [{"id": r[0]} for r in fake[ds]],
                                              "annotations": [{"image_id": r[0], "caption": "w1"} for r in fake[ds]]})
            rec = check_host(block, lists2, data, repo=tmp / "repo")
            assert rec["refused_present"] == 0 and rec["folder"]["files"] == len(fake[ds]), block
            if block == "ov":
                assert rec["folder"]["extensions"] == OV_EXT and rec["folder"]["ann_keys"] == 5
                assert references_t("ov_test", lists2, data)[fake[ds][0][0]] == ["w1"]
            probes = [("stray file", lambda: (top / "images/other.jpg").write_bytes(b"x")),
                      ("stray non-image file", lambda: (top / "notes.txt").write_text("x")),
                      ("second folder", lambda: (data / "datasets" / (E4_DIR if block != "e4" else "c_ov_test"))
                       .mkdir()),
                      ("xm3600_en folder", lambda: (data / "datasets/xm3600_en").mkdir()),
                      ("oiv7 labels", lambda: (data / "oiv7_labels.json").write_text("{}")),
                      ("test_data.json", lambda: (data / "datasets/ktvic/test_data.json").write_text("{}")),
                      ("memory file changed", lambda: (data / next(iter(MEMORY))).write_text("[]")),
                      ("B-raw twin by name", lambda: write_img(data / "datasets/openviic/00000013129.jpg", "RGB"))]
            if block == "ov":
                f0 = fake[ds][0][1]
                probes += [("case rewritten", lambda: (top / "images" / f0).rename(top / "images" / f0.lower())),
                           ("test image outside its folder", lambda: shutil.copy(top / "images" / f0,
                                                                                  data / "datasets" / f0)),
                           ("annotation keys", lambda: (top / SETS[ds]["ann"]).write_text("{}"))]
            if block == "xm":
                probes += [("English refs", lambda: _dump(top / SETS[ds]["ann"], {"release_sha256": "0" * 64,
                                                                                   "images": [], "annotations": []})),
                           ("OV-test image in the XM block", lambda: shutil.copy(tmp / "src/ov_test" / fake[
                               "ov_test"][1][1], data / "datasets/ktvic_x.png"))]
            if block == "e4":
                assert "00000001008.jpg" in lists2["refuse"]["openviic_files"], "a real dev299 / OpenViIC name clash"
                probes += [("a refused OpenViIC name outside the folder", lambda: shutil.copy(
                    top / "images/00000001008.jpg", data / "datasets/00000001008.jpg")),
                           ("a refused image", lambda: shutil.copy(tmp / "src/xm_test2500/x1.jpg",
                                                                    data / "datasets/y.jpg"))]
            for name, make in probes:
                snap = tmp / "snap"
                shutil.copytree(data, snap)
                make()
                assert C.refuses(lambda: check_host(block, lists2, data, repo=tmp / "repo")), f"{block}: {name}"
                shutil.rmtree(data)
                snap.rename(data)
            MEMORY.update(mem_saved)
    finally:
        globals()["ov_rows"], globals()["xm_rows"], C.manifest = saved
        OV_EXT.clear()
        OV_EXT.update(ext_saved)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("runs")
    p.add_argument("--set", choices=sorted(SETS), required=True)
    p.add_argument("--model", choices=C.MODELS)
    p.add_argument("--arm", nargs="+", choices=MAIN, default=list(MAIN))
    p = sub.add_parser("check-host")
    p.add_argument("--block", choices=("e4", "ov", "xm"), required=True)
    p.add_argument("--lists", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    for name in ("embed", "exemplars"):
        p = sub.add_parser(name)
        p.add_argument("--set", choices=sorted(SETS), required=True)
        p.add_argument("--lists", type=Path, required=True)
        p.add_argument("--emb1", type=Path, required=True)
        p.add_argument("--out", type=Path, required=True)
        if name == "embed":
            p.add_argument("--snapshot", type=Path, required=True)
            p.add_argument("--revision", required=True)
        else:
            p.add_argument("--emb", type=Path, required=True)
    p = sub.add_parser("decode")
    p.add_argument("--run-ids", nargs="+", required=True)
    for k in ("snapshot", "lists", "exemplars", "out-dir"):
        p.add_argument(f"--{k}", type=Path, required=True)
    p = sub.add_parser("items")
    p.add_argument("--set", choices=sorted(SETS), required=True)
    p.add_argument("--runs", nargs="+", type=Path, required=True)
    for k in ("zs", "lists", "out"):
        p.add_argument(f"--{k}", type=Path, required=True)
    p = sub.add_parser("verify")
    p.add_argument("--set", choices=sorted(SETS), required=True)
    for k in ("items", "lists", "snapshot", "out"):
        p.add_argument(f"--{k}", type=Path, required=True)
    p = sub.add_parser("e4")
    p.add_argument("--model", choices=C.MODELS, required=True)
    for k in ("snapshot", "lists", "stage1", "out-dir"):
        p.add_argument(f"--{k}", type=Path, required=True)
    p = sub.add_parser("xm-subset")
    for k in ("lists", "xm-full", "out"):
        p.add_argument(f"--{k}", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    def host():
        rec = check_host(a.block, C.load_lists(a.lists))
        out_ok(a.out).write_text(json.dumps(rec) + "\n", encoding="utf-8")

    handlers = {
        "runs": lambda: print(" ".join(spec_t(S2.frozen(), a.set, m, arm)["run_id"]
                                       for m in ([a.model] if a.model else C.MODELS) for arm in a.arm)),
        "check-host": host, "embed": lambda: cmd_embed(a), "exemplars": lambda: cmd_exemplars(a),
        "decode": lambda: decode_runs(a.run_ids, a.snapshot, a.lists, a.exemplars, a.out_dir),
        "items": lambda: cmd_items(a), "verify": lambda: cmd_verify(a), "e4": lambda: cmd_e4(a),
        "xm-subset": lambda: cmd_xm_subset(a),
    }
    handlers.get(a.cmd, lambda: ap.error("mode?"))()


if __name__ == "__main__":
    main()
