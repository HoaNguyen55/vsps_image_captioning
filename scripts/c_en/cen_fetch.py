#!/usr/bin/env python3
"""C-EN (Paper C, English arm): the pinned id/url lists and the per-image fetcher with an in-memory sha256 and the
CC-113 W4 refusal. Prereg manuscript/prereg/2026-10-27_c_en/PREREG.md; CC-107 W3, CC-113 W3/W4/W8/W9, CC-115 W4,
PI-1026i, PI-1026r, PI-1026s.

  python3 scripts/c_en/cen_fetch.py --selftest                                 CPU, synthetic bytes, no network
  python3 scripts/c_en/cen_fetch.py lists                                      laptop, CPU: the three COCO lists
  python3 scripts/c_en/cen_fetch.py nocaps-list --captions F --vg1000 F        laptop, CPU: the NoCaps lists
  python3 scripts/c_en/cen_fetch.py fetch --set S --expect-head H [--workers N]                             M3

Order on M3 (fail closed): coco_test, coco_kval, nocaps_val are fetched hash-only (bytes hashed in memory, never
written; no decode); memory starts only after all three sha records are complete, and refuses every image whose
sha256 is in one of them or in exclusion.json image_sha256. Memory images are written by tmp + os.replace only after
their sha256 passed. The list producers parse the caption fields of their inputs through the JSON loader but never
use, print or write them; every output line is ids, file names, urls, licence or domain labels and sha256 only.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDIR = "manuscript/prereg/2026-10-27_c_en"
SUMS = f"{PDIR}/SHA256SUMS"
INPUTS = {  # CC-113 W3: producer inputs, by sha256
    "karpathy": ("data/datasets/karpathy/dataset_coco.json",
                 "2fd999220673258012acfb411a4e7e66af7d488050b2519b0badcc49b7600b8d"),
    "inst_train": ("data/datasets/coco_probe/annotations/instances_train2014.json",
                   "777ef504abfeba349930485bb32ecd5b6529129a3e010f7852e1437cb049b732"),
    "inst_val": ("data/datasets/coco_probe/annotations/instances_val2014.json",
                 "e1b4d1bc54906827b1a029981b1c77f2088bd4462569b7615db7929070c3ab47"),
    "exclusion": ("manuscript/prereg/2026-10-21_dev_pools/exclusion.json",
                  "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f"),
}
NOCAPS_CAPTIONS_SHA256 = "2e8071fcd1fa512ce119b56c6fe6af2fc2105f25f0fffafe7032c8c9217c32f6"  # vg-mamf R11 protocol
NOCAPS_DRIVE_ID = "1zrsLhT94nazJ5h-LleHsU4AojHBqpcA0"  # nocaps.org/download "Validation Set Captions"
NOCAPS_DOMAINS = {"in-domain": 417, "near-domain": 2670, "out-domain": 1413}  # the artifact's labels (R11 protocol)
VG1000_SHA256 = "a21e1138b5ba15b4426933df763f806e6e22c02ef0b4b16ffe42ad8985db086f"  # nocaps_val_stratified_n1000.json
COCO_URL = "http://images.cocodataset.org/{filepath}/{file}"  # equals instances coco_url (asserted by `lists`)
OI_URL = "https://open-images-dataset.s3.amazonaws.com/validation/{file}"  # the NoCaps coco_url bucket returns 403
SETS = {"coco_test": ("cen_coco_test.tsv", 5000), "coco_kval": ("cen_coco_kval.tsv", 5000),
        "nocaps_val": ("cen_nocaps_val.tsv", 4500), "memory": ("cen_memory_allowed.tsv", 112322)}
TEST_SIDE = ("coco_test", "coco_kval", "nocaps_val")
HEADER = {"coco": "#id\tfile\turl\tlicence", "nocaps": "#id\tfile\turl\tdomain"}
REC_DIR = Path("/root/outputs/c_en/fetch")  # every fetch record on M3
STAGE_DIR = Path("/root/ncs-data/datasets")
MEM_DIR = STAGE_DIR / "cen_memory/images"  # the memory images; a test-side set only under cen_<set>/images, by `--stage`
LINE_OK = re.compile(r"^[0-9]+\t[0-9a-zA-Z_]+\.jpg\thttps?://[a-zA-Z0-9./_-]+\.jpg\t[a-z0-9-]+$")
OPEN = urllib.request.urlopen  # replaced by the selftest
HEAD_AT_RUN = ""  # set by host_ok; written into every done marker (CC-120 N3)


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def pinned(key: str) -> Path:
    rel, want = INPUTS[key]
    p = ROOT / rel
    if sha_file(p) != want:
        raise SystemExit(f"{rel}: sha256 differs from the CC-113 W3 pin {want[:8]}")
    return p


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ------------------------------------------------------------------------------------------------ lists (laptop)
def coco_lists(kar: list[dict], inst: dict[int, dict], licences: set[int], ex: dict) -> tuple[dict, dict]:
    """{set: rows} for memory, coco_test, coco_kval, and the record. Only split, cocoid, filepath and filename of the
    Karpathy rows and id, file_name, coco_url and license of the instances rows are read."""
    ex_ids = {int(x) for v in ex["ids"]["coco"].values() for x in v}
    by = {s: sorted((i for i in kar if i["split"] in s), key=lambda i: i["cocoid"])
          for s in (("train", "restval"), ("test",), ("val",))}
    rows = {}
    for name, split in (("memory", ("train", "restval")), ("coco_test", ("test",)), ("coco_kval", ("val",))):
        out = []
        for i in by[split]:
            cid, im = i["cocoid"], inst.get(i["cocoid"])
            url = COCO_URL.format(filepath=i["filepath"], file=i["filename"])
            if im is None or im["file_name"] != i["filename"] or im["coco_url"] != url:
                raise SystemExit(f"cocoid {cid}: Karpathy row and instances row disagree on file or coco_url")
            if im["license"] not in licences:
                raise SystemExit(f"cocoid {cid}: licence id {im['license']} is not in the instances licence table")
            if name == "memory" and cid in ex_ids:
                continue  # PI-1026i: the 965 refused ids stay out
            out.append((cid, i["filename"], url, str(im["license"])))
        rows[name] = out
    ids = {k: {r[0] for r in v} for k, v in rows.items()}
    n_cand = len(by[("train", "restval")])
    test_ex = {int(x) for x in ex["ids"]["coco"]["coco_karpathy_test"]}
    if (ids["memory"] & (ids["coco_test"] | ids["coco_kval"]) or ids["coco_test"] & ids["coco_kval"]
            or ids["coco_test"] != test_ex):
        raise SystemExit("the memory, Karpathy test and Karpathy val ids are not disjoint, or test != exclusion's")
    rec = {"candidates_train_restval": n_cand, "refused_ids_in_candidates": n_cand - len(rows["memory"]),
           "counts": {k: len(v) for k, v in rows.items()},
           "refused_by_list": {n: len({int(x) for x in v} & {i["cocoid"] for i in by[("train", "restval")]})
                               for n, v in ex["ids"]["coco"].items()},
           "test_side_ids_in_exclusion": {s: {n: len({int(x) for x in v} & ids[s]) for n, v in ex["ids"]["coco"].items()}
                                          for s in ("coco_test", "coco_kval")},
           "licence_counts": {k: dict(sorted(Counter(r[3] for r in v).items())) for k, v in rows.items()}}
    return rows, rec


def nocaps_lists(cap: dict, vg: dict) -> tuple[list, list[int], dict]:
    """NoCaps val rows from the captions file's `images` key only (id, file_name, open_images_id, domain), and the
    vg-mamf 1,000 ids (image_id, open_images_id). The `annotations` key is never read."""
    rows = []
    for im in cap["images"]:
        oid, f = str(im["open_images_id"]), im["file_name"]
        if not re.fullmatch(r"[0-9a-f]{16}", oid) or f != f"{oid}.jpg":
            raise SystemExit(f"NoCaps image {im['id']}: file name is not <open_images_id>.jpg")
        rows.append((int(im["id"]), f, OI_URL.format(file=f), im["domain"]))
    rows.sort()
    dom = dict(Counter(r[3] for r in rows))
    if len(rows) != 4500 or len({r[0] for r in rows}) != 4500 or dom != NOCAPS_DOMAINS:
        raise SystemExit(f"NoCaps val: {len(rows)} images, domains {dom}; not 4,500 / {NOCAPS_DOMAINS}")
    oid = {r[0]: r[1] for r in rows}
    vg_ids = sorted(int(r["image_id"]) for r in vg["results"])
    if (len(set(vg_ids)) != 1000 or any(f"{r['open_images_id']}.jpg" != oid.get(int(r["image_id"]))
                                         for r in vg["results"])):
        raise SystemExit("vg-mamf cohort: not 1,000 NoCaps val ids with matching open_images_id")
    return rows, vg_ids, {"counts": {"nocaps_val": 4500, "vg1000": 1000}, "domains": dom}


def write_tsv(path: Path, kind: str, rows: list) -> str:
    lines = [HEADER[kind]] + ["\t".join(map(str, r)) for r in rows]
    if not all(LINE_OK.match(x) for x in lines[1:]):
        raise SystemExit(f"{path.name}: a line is not id/file/url/label only")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return sha_file(path)


def cmd_lists(out: Path) -> None:
    kar = json.loads(pinned("karpathy").read_text(encoding="utf-8"))["images"]
    inst, licences = {}, set()
    for k in ("inst_train", "inst_val"):
        d = json.loads(pinned(k).read_text(encoding="utf-8"))
        inst |= {im["id"]: im for im in d["images"]}
        licences |= {lic["id"] for lic in d["licenses"]}
    rows, rec = coco_lists(kar, inst, licences, json.loads(pinned("exclusion").read_text(encoding="utf-8")))
    if rec["counts"] != {"memory": 112322, "coco_test": 5000, "coco_kval": 5000} or rec["candidates_train_restval"] \
            != 113287 or rec["refused_ids_in_candidates"] != 965:
        raise SystemExit(f"counts {rec['counts']} are not 112,322 / 5,000 / 5,000 (113,287 - 965)")
    out.mkdir(parents=True, exist_ok=True)
    rec["sha256"] = {SETS[k][0]: write_tsv(out / SETS[k][0], "coco", v) for k, v in rows.items()}
    rec |= {"inputs_sha256": {k: v[1] for k, v in INPUTS.items()}, "utc": utc(),
            "note": "caption fields parsed by the JSON loader, never used, printed or written"}
    (out / "lists_record_coco.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"counts": rec["counts"], "sha256": rec["sha256"]}))


def cmd_nocaps_list(captions: Path, vg1000: Path, out: Path) -> None:
    if sha_file(captions) != NOCAPS_CAPTIONS_SHA256 or sha_file(vg1000) != VG1000_SHA256:
        raise SystemExit("the NoCaps captions file or the vg-mamf cohort file differs from its pin; to the judge")
    rows, vg_ids, rec = nocaps_lists(json.loads(captions.read_text(encoding="utf-8")),
                                     json.loads(vg1000.read_text(encoding="utf-8")))
    out.mkdir(parents=True, exist_ok=True)
    (out / "cen_nocaps_vg1000.txt").write_text("".join(f"{i}\n" for i in vg_ids), encoding="utf-8")
    rec["sha256"] = {SETS["nocaps_val"][0]: write_tsv(out / SETS["nocaps_val"][0], "nocaps", rows),
                     "cen_nocaps_vg1000.txt": sha_file(out / "cen_nocaps_vg1000.txt")}
    rec |= {"inputs_sha256": {"nocaps_val_4500_captions.json": NOCAPS_CAPTIONS_SHA256,
                              "nocaps_val_stratified_n1000.json": VG1000_SHA256}, "utc": utc(),
            "note": "only the captions file's `images` key was read; caption fields never used, printed or written"}
    (out / "lists_record_nocaps.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"counts": rec["counts"], "domains": rec["domains"], "sha256": rec["sha256"]}))


# ------------------------------------------------------------------------------------------------ fetch (M3)
def host_ok(expect_head: str, mid_file: Path = Path("/root/.vsps_machine_id")) -> None:
    """M3 only, at the committed HEAD with a clean tracked tree, the prereg folder's SHA256SUMS verifying."""
    mid = mid_file.read_text().strip().lower() if mid_file.is_file() else ""
    if mid != "m3":
        raise SystemExit(f"REFUSED: {mid_file} is {mid or 'missing'!r}, not m3")
    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    clean = subprocess.run(["git", "-C", str(ROOT), "diff", "--quiet", "HEAD", "--"]).returncode == 0
    if head != expect_head or not clean:
        raise SystemExit(f"REFUSED: HEAD {head[:8]} is not {expect_head[:8]}, or tracked files differ from HEAD")
    global HEAD_AT_RUN
    HEAD_AT_RUN = head


def load_list(name: str, root: Path = ROOT) -> list[tuple[int, str, str, str]]:
    """A set's pinned list: its line in the prereg SHA256SUMS must verify; n distinct ids; every url by the rule."""
    rel = f"{PDIR}/{SETS[name][0]}"
    sums = dict(reversed(x.split(maxsplit=1)) for x in (root / SUMS).read_text().splitlines() if x)
    if sums.get(rel) is None or sha_file(root / rel) != sums[rel]:
        raise SystemExit(f"{rel}: not in {SUMS}, or its sha256 differs")
    rows = [(int(i), f, u, x) for i, f, u, x in (ln.split("\t") for ln in
                                                   (root / rel).read_text(encoding="utf-8").splitlines()[1:])]
    if len(rows) != SETS[name][1] or len({r[0] for r in rows}) != len(rows):
        raise SystemExit(f"{rel}: not {SETS[name][1]} distinct ids")
    for r in rows:
        url_ok(name, r)
    return rows


def url_ok(name: str, row: tuple) -> str:
    """CC-113 W4: the url is rebuilt from the row's own id and file; anything else is refused before any request."""
    cid, f, url, _x = row
    if name == "nocaps_val":
        want = OI_URL.format(file=f)
        ok = re.fullmatch(r"[0-9a-f]{16}\.jpg", f) is not None
    else:
        part = f.split("_")[1] if f.count("_") == 2 else ""
        want = COCO_URL.format(filepath=part, file=f)
        ok = part in ("train2014", "val2014") and f == f"COCO_{part}_{cid:012d}.jpg"
    if not ok or url != want:
        raise SystemExit(f"REFUSED: id {cid}: url is not the pinned rule's")
    return url


PNG_OK = {320612}  # CC-122: the COCO host serves this restval id as a PNG body under .jpg (200, 302,086 B)


def get(url: str, tries: int = 3, png: bool = False) -> tuple[bytes | None, str]:
    err = ""
    for a in range(tries):
        try:
            with OPEN(url, timeout=60) as r:
                b, final, status = r.read(), r.geturl(), r.status
            if final != url or status != 200:  # CC-120 W2: no redirect, no other status
                err = f"status {status}" if final == url else "redirected"
            elif not (b.startswith(b"\xff\xd8") or (png and b.startswith(b"\x89PNG\r\n\x1a\n"))):  # JPEG SOI; PNG by id
                err = "not a JPEG body"
            else:
                return b, ""
        except Exception as e:  # network errors are recorded and retried; a rerun resumes
            err = type(e).__name__
        time.sleep(2 ** a * 0.01 if OPEN is not urllib.request.urlopen else 2 ** a)
    return None, err


REC_LINE = {"sha256": re.compile(r"^\d+\t\S+\.jpg\t[0-9a-f]{64}\t\d+$"), "refused": re.compile(r"^\d+\t[0-9a-f]{64}$")}


def read_rec(p: Path) -> dict[int, tuple]:
    """A sha or refused record: every line matches its pattern and the file ends in a newline, else STOP (CC-120
    W1: a torn line is never read as done)."""
    if not p.exists():
        return {}
    text = p.read_text()
    pat = REC_LINE[p.name.rsplit(".", 2)[-2]]
    if text and (not text.endswith("\n") or not all(pat.match(x) for x in text[:-1].split("\n"))):
        raise SystemExit(f"STOP: {p.name} has a torn or malformed line; to the judge")
    return {int(x.split("\t")[0]): tuple(x.split("\t")) for x in text.splitlines()}


def refused_shas(rec_dir: Path, ex: dict, lists: dict[str, list]) -> set[str]:
    """Memory gate (fail closed): every test-side record complete and unchanged since its done marker."""
    out = {h for v in ex["image_sha256"].values() for h in v}
    for s in TEST_SIDE:
        rec, done = rec_dir / f"{s}.sha256.tsv", rec_dir / f"{s}.done.json"
        if not done.exists() or json.loads(done.read_text())["record_sha256"] != sha_file(rec):
            raise SystemExit(f"REFUSED: the {s} sha record is not complete; the memory fetch waits for it")
        got = read_rec(rec)
        if set(got) != {r[0] for r in lists[s]}:
            raise SystemExit(f"REFUSED: the {s} sha record does not cover its {SETS[s][1]} ids")
        out |= {v[2] for v in got.values()}
    return out


def run_fetch(name: str, rows: list, rec_dir: Path, out_dir: Path | None, refuse: set[str], workers: int,
              lists: dict[str, list]) -> dict:
    """Fetch one set. Hash-only unless out_dir is given (memory). Records: <set>.sha256.tsv (id, file, sha256, bytes),
    <set>.refused.tsv (id, sha256), <set>.failed.tsv (id, error class), and <set>.done.json once complete."""
    if (name == "memory") != (out_dir is not None):
        raise SystemExit("only the memory set writes images; every test-side set is hash-only")
    if name == "memory":
        bad = {r[0] for r in rows} & {r[0] for s in TEST_SIDE if s != "nocaps_val" for r in lists[s]}
        if bad:
            raise SystemExit(f"REFUSED: {len(bad)} Karpathy test/val id(s) in the memory list")
    rec_dir.mkdir(parents=True, exist_ok=True)
    rec_p, ref_p, fail_p = (rec_dir / f"{name}.{k}.tsv" for k in ("sha256", "refused", "failed"))
    want = {r[0]: r for r in rows}
    done, refd = read_rec(rec_p), read_rec(ref_p)
    if out_dir is not None:  # resume: every file on disk must be a recorded list file at its recorded sha
        out_dir.mkdir(parents=True, exist_ok=True)
        files = {r[1]: r[0] for r in rows}
        for p in out_dir.iterdir():
            cid = files.get(p.name)
            if p.name.startswith(".tmp_") and p.name[5:] in files:
                p.unlink()  # an interrupted write of a list file; its id is not recorded and is fetched again
            elif cid is None or cid not in done or sha_file(p) != done[cid][2]:
                raise SystemExit(f"STOP (CC-113 W8): {p.name} is on disk but not a recorded list file; to the judge")
        if any(not (out_dir / v[1]).exists() for v in done.values()):
            raise SystemExit("STOP: a recorded memory file is missing on disk; to the judge")
    todo = [r for r in rows if r[0] not in done and r[0] not in refd]
    fail_p.unlink(missing_ok=True)
    failed = 0

    def one(r):
        return r, *get(url_ok(name, r), png=name == "memory" and r[0] in PNG_OK)

    with cf.ThreadPoolExecutor(workers) as pool, open(rec_p, "a") as rec, open(ref_p, "a") as rf:
        for lo in range(0, len(todo), 512):
            for r, b, err in pool.map(one, todo[lo:lo + 512]):
                if b is None:
                    failed += 1
                    with open(fail_p, "a") as ff:
                        ff.write(f"{r[0]}\t{err}\n")
                    continue
                h = sha_bytes(b)
                if h in refuse:  # never written: a byte copy of a refused or test-side image
                    rf.write(f"{r[0]}\t{h}\n")
                    rf.flush()
                    continue
                if out_dir is not None:
                    tmp = out_dir / f".tmp_{r[1]}"
                    tmp.write_bytes(b)
                    os.replace(tmp, out_dir / r[1])
                rec.write(f"{r[0]}\t{r[1]}\t{h}\t{len(b)}\n")
                rec.flush()
            print(f"{utc()} {name}: {min(lo + 512, len(todo))}/{len(todo)} this run, {failed} failed", flush=True)
    done, refd = read_rec(rec_p), read_rec(ref_p)
    if set(done) | set(refd) != set(want) or set(done) & set(refd):
        return {"set": name, "complete": False, "recorded": len(done), "refused": len(refd), "failed": failed}
    if name != "memory" and refd:
        raise SystemExit(f"STOP: a test-side set refused {len(refd)} image(s); to the judge")
    marker = {"set": name, "n": len(want), "recorded": len(done), "refused": len(refd),
              "distinct_sha256": len({v[2] for v in done.values()}), "bytes": sum(int(v[3]) for v in done.values()),
              "record_sha256": sha_file(rec_p), "refused_sha256": sha_file(ref_p), "stored": out_dir is not None,
              "head": HEAD_AT_RUN, "utc": utc()}
    (rec_dir / f"{name}.done.json").write_text(json.dumps(marker) + "\n")
    return {**marker, "complete": True}


RECORD_PINS = {  # CC-121 W2: the hash-only records as completed at 780ac71 (PREREG §11)
    "coco_test": "614afa1b7cf63bde693fc9692b1699d47ba527d396b7a1216d031b1d50018fdf",
    "coco_kval": "8c93f306f24588fb6e66eed0a8ba2ba97e61adf901ddf5ab614b37d5b677ee1c",
    "nocaps_val": "fbbcd21ccd8e036e5d1a94bb0fa143538882ceec62ba76a1e9104d31f321cb33"}
PREREG = f"{PDIR}/PREREG.md"


def prereg_committed(root: Path = ROOT) -> None:
    """CC-121 W9: --stage only after the C-EN prereg is committed: PREREG.md in HEAD and at its SHA256SUMS line."""
    inside = subprocess.run(["git", "-C", str(root), "cat-file", "-e", f"HEAD:{PREREG}"], capture_output=True)
    sums = root / SUMS
    line = dict(reversed(x.split(maxsplit=1)) for x in sums.read_text().splitlines() if x) if sums.exists() else {}
    if inside.returncode != 0 or line.get(PREREG) is None or sha_file(root / PREREG) != line[PREREG]:
        raise SystemExit("REFUSED (CC-121 W9): the C-EN prereg is not committed; no test set is staged before it")


GRL_RUNNING = Path("/root/outputs/grl_pilot/RUNNING")  # CC-124 r3: no --stage while a G-RL pilot holds M3


def no_pilot(flag: Path = GRL_RUNNING) -> None:
    try:
        running = flag.exists()
    except OSError:  # the laptop cannot traverse /root: no pilot lock is visible here
        running = False
    if running:
        raise SystemExit(f"REFUSED (CC-124 r3): {flag} exists; no test set is staged while a G-RL pilot runs")


def run_stage(name: str, rows: list, rec_dir: Path, out_dir: Path, workers: int, gate=prereg_committed,
              pins: dict[str, str] = RECORD_PINS) -> dict:
    """Stage a test-side set for one block (features, then decode): only after the prereg commit, against a record
    at its pinned sha; every image is fetched again and written only if its sha256 equals the record; anything else on
    disk or any other sha is a STOP. Resumable."""
    gate()
    done_p, rec_p = rec_dir / f"{name}.done.json", rec_dir / f"{name}.sha256.tsv"
    if name not in TEST_SIDE or not done_p.exists() or json.loads(done_p.read_text())["record_sha256"] != sha_file(rec_p):
        raise SystemExit(f"REFUSED: {name} has no complete hash-only record to stage against")
    if sha_file(rec_p) != pins[name]:
        raise SystemExit(f"REFUSED (CC-121 W2): the {name} record is not at its pinned sha {pins[name][:8]}")
    want = {int(k): v[2] for k, v in read_rec(rec_p).items()}
    files = {r[1]: r[0] for r in rows}
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in out_dir.iterdir():
        if p.name.startswith(".tmp_") and p.name[5:] in files:
            p.unlink()
        elif p.name not in files or sha_file(p) != want[files[p.name]]:
            raise SystemExit(f"STOP: {p.name} in {out_dir.name} is not a {name} file at its recorded sha; to the judge")
    todo = [r for r in rows if not (out_dir / r[1]).exists()]
    failed = 0
    with cf.ThreadPoolExecutor(workers) as pool:
        for lo in range(0, len(todo), 512):
            for r, b, _err in pool.map(lambda r: (r, *get(url_ok(name, r))), todo[lo:lo + 512]):
                if b is None:
                    failed += 1
                    continue
                if sha_bytes(b) != want[r[0]]:
                    raise SystemExit(f"STOP: id {r[0]} arrived with another sha256 than its record; to the judge")
                tmp = out_dir / f".tmp_{r[1]}"
                tmp.write_bytes(b)
                os.replace(tmp, out_dir / r[1])
    n = sum(1 for _p in out_dir.iterdir())
    return {"set": name, "staged": n, "n": len(rows), "failed": failed, "complete": n == len(rows), "utc": utc()}


def cmd_fetch(a) -> None:
    host_ok(a.expect_head)
    lists = {s: load_list(s) for s in (SETS if a.set == "memory" else (a.set,))}  # memory needs all four
    ex = json.loads((ROOT / INPUTS["exclusion"][0]).read_text(encoding="utf-8"))
    if sha_file(ROOT / INPUTS["exclusion"][0]) != INPUTS["exclusion"][1]:
        raise SystemExit("exclusion.json differs from c52a96d1")
    if a.stage:
        if a.set == "memory":
            raise SystemExit("--stage is for a test-side set only")
        no_pilot()
        res = run_stage(a.set, lists[a.set], REC_DIR, STAGE_DIR / f"cen_{a.set}" / "images", a.workers)
        print(json.dumps(res))
        if not res["complete"]:
            raise SystemExit(f"{a.set}: staging incomplete ({res['failed']} failed); run again to resume")
        return
    if (REC_DIR / f"{a.set}.done.json").exists():
        raise SystemExit(f"{a.set} is complete; it is fetched once")
    if a.set == "memory" and {r[0] for r in lists["memory"]} & {int(x) for v in ex["ids"]["coco"].values()
                                                                 for x in v}:
        raise SystemExit("REFUSED: an exclusion.json coco id is in the memory list")
    refuse = refused_shas(REC_DIR, ex, lists) if a.set == "memory" else set()
    res = run_fetch(a.set, lists[a.set], REC_DIR, MEM_DIR if a.set == "memory" else None, refuse, a.workers, lists)
    print(json.dumps(res))
    if not res["complete"]:
        raise SystemExit(f"{a.set}: incomplete ({res['failed']} failed); run again to resume")


# ------------------------------------------------------------------------------------------------ self-test (CPU)
def refuses(fn) -> bool:
    try:
        fn()
    except SystemExit as e:
        return bool(str(e))
    return False


class _Resp:
    def __init__(self, b: bytes, url: str, status: int = 200):
        self.b, self.url, self.status = b, url, status

    def geturl(self) -> str:
        return self.url

    def __enter__(self):
        return self

    def __exit__(self, *_a):
        return False

    def read(self) -> bytes:
        return self.b


def selftest() -> None:
    global OPEN
    calls: list[str] = []
    down: set[str] = set()

    def fake(url, timeout=60):
        calls.append(url)
        if url in down:
            raise OSError("down")
        body = b"\xff\xd8" + hashlib.sha256(url.encode()).digest() * 8  # synthetic bytes, no dataset content
        return {"redirect": _Resp(body, url + "?r"), "status": _Resp(body, url, 404),
                "html": _Resp(b"<html>", url), "png": _Resp(b"\x89PNG\r\n\x1a\n" + body[2:], url)
                }.get(MODE.get(url), _Resp(body, url))

    MODE: dict[str, str] = {}
    globals()["MODE"] = MODE
    saved, OPEN = OPEN, fake
    try:
        _selftest(calls, down)
    finally:
        OPEN = saved
    print("selftest ok: lists (965-style exclusion, url = instances coco_url, licence table, disjoint, NoCaps "
          "images key only, domains, vg1000), url rule refuses before any request, hash-only writes no image, memory "
          "gate needs all three complete test-side records, sha hits refused and never written, stray or changed "
          "file STOP, W1 torn record STOP, W2 redirect/status/non-JPEG refused, CC-122 X1 PNG body for memory id 320612 only (other ids, test side and --stage refused), N2 tmp, staging only after the prereg commit (W9), against the pinned record (W2), never under a G-RL pilot lock (CC-124 r3), at the recorded sha, resume makes no repeat request, failures leave the set incomplete, host check m3 + HEAD")


def _selftest(calls: list, down: set) -> None:
    # lists: synthetic Karpathy / instances / exclusion rows
    def k(cid, split, fp):
        return {"cocoid": cid, "split": split, "filepath": fp, "filename": f"COCO_{fp}_{cid:012d}.jpg",
                "sentences": [{"raw": "x"}]}
    kar = [k(1, "train", "train2014"), k(2, "train", "train2014"), k(3, "restval", "val2014"),
           k(4, "test", "val2014"), k(5, "val", "val2014"), k(6, "restval", "val2014")]
    inst = {i["cocoid"]: {"id": i["cocoid"], "file_name": i["filename"], "license": 4,
                          "coco_url": COCO_URL.format(filepath=i["filepath"], file=i["filename"])} for i in kar}
    ex = {"ids": {"coco": {"uitviic_test": ["2"], "coco_karpathy_test": ["4"], "pope500": ["6", "5"]}},
          "image_sha256": {"cv295": ["f" * 64]}}
    rows, rec = coco_lists(kar, inst, {4}, ex)
    assert [r[0] for r in rows["memory"]] == [1, 3] and rec["refused_ids_in_candidates"] == 2
    assert rec["test_side_ids_in_exclusion"]["coco_kval"]["pope500"] == 1 and rows["coco_test"][0][0] == 4
    assert refuses(lambda: coco_lists(kar, inst, {1}, ex)), "unknown licence id"
    assert refuses(lambda: coco_lists(kar, {**inst, 1: {**inst[1], "coco_url": "http://x/y.jpg"}}, {4}, ex))
    assert refuses(lambda: coco_lists(kar, inst, {4}, {**ex, "ids": {"coco": {"coco_karpathy_test": ["5"]}}}))
    oid = [f"{n:016x}" for n in range(4500)]
    dom = [d for d, n in NOCAPS_DOMAINS.items() for _ in range(n)]
    cap = {"images": [{"id": n, "file_name": f"{o}.jpg", "open_images_id": o, "domain": d}
                      for n, (o, d) in enumerate(zip(oid, dom))]}
    vg = {"results": [{"image_id": n, "open_images_id": oid[n]} for n in range(0, 4000, 4)]}
    nrows, vg_ids, _r = nocaps_lists(cap, vg)  # no `annotations` key exists: it is never read
    assert len(nrows) == 4500 and vg_ids[:2] == [0, 4] and nrows[0][2] == OI_URL.format(file=f"{oid[0]}.jpg")
    assert refuses(lambda: nocaps_lists({"images": cap["images"][:-1]}, vg)), "4,500 images"
    assert refuses(lambda: nocaps_lists(cap, {"results": vg["results"][:-1]})), "1,000 ids"

    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / PDIR).mkdir(parents=True)
        mem = [(i, f"COCO_train2014_{i:012d}.jpg", COCO_URL.format(filepath="train2014",
                                                                     file=f"COCO_train2014_{i:012d}.jpg"), "4")
               for i in range(10, 30)]
        sets = {"coco_test": [(4, *rows["coco_test"][0][1:])], "coco_kval": [(5, *rows["coco_kval"][0][1:])],
                "nocaps_val": nrows[:2], "memory": mem}
        lines = []
        for s, r in sets.items():
            SETS[s] = (SETS[s][0], len(r))
            h = write_tsv(t / PDIR / SETS[s][0], "nocaps" if s == "nocaps_val" else "coco", r)
            lines.append(f"{h}  {PDIR}/{SETS[s][0]}")
        (t / SUMS).write_text("\n".join(lines) + "\n")
        full = (t / SUMS).read_text()
        (t / SUMS).write_text("".join(x + "\n" for x in lines if SETS["nocaps_val"][0] not in x))
        assert load_list("coco_test", t) and refuses(lambda: load_list("nocaps_val", t)), "no NoCaps line yet"
        assert refuses(lambda: [load_list(s, t) for s in SETS]), "memory loads all four lists: refused"
        (t / SUMS).write_text(full)
        lists = {s: load_list(s, t) for s in SETS}
        assert lists["memory"] == mem
        (t / PDIR / SETS["memory"][0]).write_text(HEADER["coco"] + "\n")
        assert refuses(lambda: load_list("memory", t)), "a list that differs from SHA256SUMS"
        bad = (10, mem[0][1], "http://evil.example/x.jpg", "4")
        n0 = len(calls)
        assert refuses(lambda: url_ok("memory", bad)) and len(calls) == n0, "off-rule url: refused, no request"
        assert refuses(lambda: url_ok("memory", (11, mem[0][1], mem[0][2], "4"))), "url of another id"
        rec_dir, out = t / "rec", t / "img"
        assert refuses(lambda: refused_shas(rec_dir, ex, lists)), "memory gate: no test-side record"
        assert refuses(lambda: run_fetch("coco_test", lists["coco_test"], rec_dir, out, set(), 2, lists))
        down.add(lists["nocaps_val"][1][2])
        for s in TEST_SIDE:
            res = run_fetch(s, lists[s], rec_dir, None, set(), 2, lists)
            assert res["complete"] == (s != "nocaps_val"), s
        assert not out.exists() and not list(rec_dir.glob("*.jpg")), "hash-only writes no image"
        assert refuses(lambda: refused_shas(rec_dir, ex, lists)), "memory gate: nocaps_val incomplete"
        down.clear()
        n0 = len(calls)
        assert run_fetch("nocaps_val", lists["nocaps_val"], rec_dir, None, set(), 2, lists)["complete"]
        assert len(calls) == n0 + 1, "resume fetches only the missing id"
        st = t / "stage" / "cen_coco_test" / "images"
        pins = {s: sha_file(rec_dir / f"{s}.sha256.tsv") for s in TEST_SIDE}
        ok = lambda: None  # noqa: E731  the prereg gate, tested on its own below

        def run_stage_t(n, r, rd, o, w, gate=ok, pins=pins):
            return run_stage(n, r, rd, o, w, gate, pins)

        assert refuses(lambda: run_stage("coco_test", lists["coco_test"], rec_dir, st, 2, gate=lambda: prereg_committed(t))), \
            "W9: --stage refuses before the prereg is committed"
        assert not st.exists(), "nothing staged when the gate refuses"
        assert refuses(lambda: run_stage("coco_test", lists["coco_test"], rec_dir, st, 2, ok, {**pins, "coco_test": "0" * 64})), \
            "W2: a record not at its pin"
        assert run_stage_t("coco_test", lists["coco_test"], rec_dir, st, 2)["complete"] and len(list(st.iterdir())) == 1
        (st / lists["coco_test"][0][1]).write_bytes(b"other")
        assert refuses(lambda: run_stage_t("coco_test", lists["coco_test"], rec_dir, st, 2)), "staged file at another sha"
        (st / lists["coco_test"][0][1]).unlink()
        rec_t = rec_dir / "coco_test.sha256.tsv"
        good = rec_t.read_text()
        rec_t.write_text(good.replace(good.split("\t")[2], "0" * 64))
        assert refuses(lambda: run_stage_t("coco_test", lists["coco_test"], rec_dir, st, 2)), "record changed after done"
        rec_t.write_text(good)
        assert refuses(lambda: run_stage_t("memory", lists["memory"], rec_dir, st, 2)), "memory is never staged"
        g = t / "git"
        (g / PDIR).mkdir(parents=True)
        (g / PREREG).write_text("x\n")
        (g / SUMS).write_text(f"{sha_file(g / PREREG)}  {PREREG}\n")
        git = ["git", "-C", str(g), "-c", "user.name=selftest", "-c", "user.email=selftest@invalid"]
        subprocess.run(git[:3] + ["init", "-q"], check=True)
        assert refuses(lambda: prereg_committed(g)), "W9: no commit yet"
        subprocess.run(git + ["add", "-A"], check=True)
        subprocess.run(git + ["commit", "-qm", "t"], check=True)
        prereg_committed(g)
        (g / PREREG).write_text("changed\n")
        assert refuses(lambda: prereg_committed(g)), "W9: PREREG.md not at its SHA256SUMS line"
        refuse = refused_shas(rec_dir, ex, lists)
        for mode in ("redirect", "status", "html"):
            MODE[mem[0][2]] = mode
            assert get(mem[0][2]) == (None, {"redirect": "redirected", "status": "status 404",
                                              "html": "not a JPEG body"}[mode]), f"W2: {mode} body refused"
        MODE.clear()
        (t / "RUNNING").write_text("")
        assert refuses(lambda: no_pilot(t / "RUNNING")), "CC-124 r3: --stage refused while the pilot lock exists"
        no_pilot(t / "no_lock")

        class Raising(type(Path())):
            def exists(self, **_kw):
                raise PermissionError("not traversable")

        no_pilot(Raising("/root/outputs/grl_pilot/RUNNING"))  # unreadable path: not a lock
        hit = sha_bytes(b"\xff\xd8" + hashlib.sha256(mem[3][2].encode()).digest() * 8)
        down.add(mem[5][2])
        res = run_fetch("memory", lists["memory"], rec_dir, out, refuse | {hit}, 3, lists)
        assert not res["complete"] and res["refused"] == 1 and res["failed"] == 1
        assert not (out / mem[3][1]).exists() and (out / mem[0][1]).exists(), "a sha hit is never written"
        assert (rec_dir / "memory.refused.tsv").read_text() == f"{mem[3][0]}\t{hit}\n"
        down.clear()
        n0 = len(calls)
        res = run_fetch("memory", lists["memory"], rec_dir, out, refuse | {hit}, 3, lists)
        assert res["complete"] and res["recorded"] == 19 and len(calls) == n0 + 1, "resume: one request"
        assert all(re.fullmatch(r"[0-9]+\t\S+\.jpg\t[0-9a-f]{64}\t[0-9]+", x)
                   for x in (rec_dir / "memory.sha256.tsv").read_text().splitlines()), "ids, files, shas only"
        rec_m = rec_dir / "memory.sha256.tsv"
        good_m = rec_m.read_text()
        rec_m.write_text(good_m[:-1])
        assert refuses(lambda: read_rec(rec_m)), "W1: no trailing newline"
        rec_m.write_text(good_m + "12\tCOCO_x.jpg\tabc\n")
        assert refuses(lambda: read_rec(rec_m)), "W1: torn line"
        rec_m.write_text(good_m)
        (rec_dir / "memory.done.json").unlink()
        (out / ".tmp_other.jpg").write_bytes(b"x")
        assert refuses(lambda: run_fetch("memory", lists["memory"], rec_dir, out, refuse, 2, lists)), "N2: other tmp"
        (out / ".tmp_other.jpg").unlink()
        (out / "stray.jpg").write_bytes(b"x")
        assert refuses(lambda: run_fetch("memory", lists["memory"], rec_dir, out, refuse, 2, lists)), "stray STOP"
        (out / "stray.jpg").unlink()
        (out / mem[0][1]).write_bytes(b"changed")
        assert refuses(lambda: run_fetch("memory", lists["memory"], rec_dir, out, refuse, 2, lists)), "changed STOP"
        mid = t / "mid"
        mid.write_text("m4\n")
        assert refuses(lambda: host_ok("0" * 40, mid)), "machine id m4 refused"
        mid.write_text("M3\n")
        assert refuses(lambda: host_ok("0" * 40, mid)), "wrong HEAD refused"
        assert refuses(lambda: host_ok("0" * 40, t / "none")), "missing machine id refused"
        # CC-122 X1: a PNG body is accepted for memory id 320612 only
        def coco_row(cid, part):
            f = f"COCO_{part}_{cid:012d}.jpg"
            return (cid, f, COCO_URL.format(filepath=part, file=f), "4")
        png_id, other = coco_row(320612, "val2014"), coco_row(31, "train2014")
        for r in (png_id, other):
            MODE[r[2]] = "png"
        rd, od = t / "rec_png", t / "img_png"
        res = run_fetch("memory", [png_id, other], rd, od, set(), 2, lists)
        assert (od / png_id[1]).read_bytes().startswith(b"\x89PNG") and 320612 in read_rec(rd / "memory.sha256.tsv"), \
            "X1 (i): memory id 320612 with a PNG body is recorded"
        assert not res["complete"] and not (od / other[1]).exists() and \
            (rd / "memory.failed.tsv").read_text() == f"{other[0]}\tnot a JPEG body\n", "X1 (ii): any other id fails"
        ts = run_fetch("coco_test", [png_id], t / "rec_png_t", None, set(), 2, lists)
        assert not ts["complete"] and ts["failed"] == 1, "X1 (iii): a test-side row with a PNG body fails"
        st2 = t / "stage_png" / "images"
        MODE[lists["coco_test"][0][2]] = "png"
        sp = run_stage("coco_test", lists["coco_test"], rec_dir, st2, 2, ok, pins)
        assert not sp["complete"] and sp["failed"] == 1 and not any(st2.iterdir()), "X1 (iv): --stage refuses a PNG body"
        MODE.clear()
    for s, (f, _n) in list(SETS.items()):
        SETS[s] = (f, {"coco_test": 5000, "coco_kval": 5000, "nocaps_val": 4500, "memory": 112322}[s])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("lists")
    p.add_argument("--out-dir", type=Path, default=ROOT / PDIR)
    p = sub.add_parser("nocaps-list")
    p.add_argument("--captions", type=Path, required=True, help="nocaps_val_4500_captions.json (Drive, pinned)")
    p.add_argument("--vg1000", type=Path, required=True, help="vg-mamf nocaps_val_stratified_n1000.json (pinned)")
    p.add_argument("--out-dir", type=Path, default=ROOT / PDIR)
    p = sub.add_parser("fetch")
    p.add_argument("--set", choices=sorted(SETS), required=True)
    p.add_argument("--expect-head", required=True)
    p.add_argument("--workers", type=int, default=16)
    p.add_argument("--stage", action="store_true", help="test-side set: write cen_<set>/images, sha = its record")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd == "lists":
        return cmd_lists(a.out_dir)
    if a.cmd == "nocaps-list":
        return cmd_nocaps_list(a.captions, a.vg1000, a.out_dir)
    if a.cmd == "fetch":
        return cmd_fetch(a)
    ap.error("mode?")


if __name__ == "__main__":
    main()
