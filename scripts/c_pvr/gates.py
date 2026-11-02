#!/usr/bin/env python3
"""C-PVR-T1 gates G-A and G-C2 (Paper C, PVR). Prereg manuscript/prereg/2026-11-02_c_pvr_tier1/PREREG_DRAFT_v1_2.md
(8282874) as amended by AMENDMENT_CC222 v1.1 (entry point, inputs, custody, G-C2 rule). Stdlib only, no repo import,
no network code: every download is a curl line of the amendment; this file reads local files and stdin only.

    python3 -I scripts/c_pvr/gates.py selftest                 CPU: synthetic fixtures, sockets raise; sha checks of the
                                                               pinned real files; schema of the registered provenance
    python3 -I scripts/c_pvr/gates.py gate-a step0             real pinned id files, after GO, before any download
    python3 -I scripts/c_pvr/gates.py gate-a pin               step-3 size/first-byte/md5/header check, prints shas
    python3 -I scripts/c_pvr/gates.py gate-a join --info-sha H --oi-sha H   ids only; counts first, ids last, once
    python3 -I scripts/c_pvr/gates.py gate-a verify            offline rerun; must reproduce ga_remaining_ids.txt
    curl ... | python3 -I scripts/c_pvr/gates.py gate-c2 scan --file KEY    one pinned SFT list from stdin
    python3 -I scripts/c_pvr/gates.py gate-c2 join [--prefix-map P]          verify, then G_C2_record.json

Label on every output: TIER 1 / DEV-EXPLORE (C-PVR-T1). No caption, label, question or answer field is accessed,
printed or written: NoCaps-test image info is checked for its key schema and only ids are taken; the OI test list is an
image-metadata file (no label column); SFT lists are scanned for image references, 16-hex tokens, Flickr photo ids,
key-name counts and three dataset names only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import shutil
import socket
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDIR = "manuscript/prereg/2026-11-02_c_pvr_tier1"
LABEL = "TIER 1 / DEV-EXPLORE (C-PVR-T1)"
SEALED = Path.home() / ".vsps_sealed" / "c_pvr"  # WSL ext4 home; never /mnt/d, data/, the repo or a backup path
GA, GC2 = SEALED / "ga", SEALED / "gc2"

PINS = {  # key -> (repo path, sha256); prereg §2.2-2.3, C-EN SHA256SUMS l.5, CC-221a
    "xm_src": ("data/datasets/xm3600/oiv7/xm3600_ids.txt",
               "1bd00f466afc196ab51a6b86d3c1a5b6ea1e553393362b98199aa892287e1922"),
    "xm_attr": ("data/datasets/xm3600/raw/image_attributions.csv",
                "288de413d25e9c70dadfd42ee59256aa1082673e615d0eda02c3875fe2b36ecd"),
    "oiv7_val": ("manuscript/prereg/2026-10-28_w25_neardup/oiv7_val_ids.txt",
                 "4b7a1813487dc5d74a5bd4aca7c36d0f6d2d3042d9cc6cf4091180dc473eabb0"),
    "xm456": ("manuscript/prereg/2026-10-28_w25_neardup/xm3600_in_oiv7_val_ids.txt",
              "54966ca78ce310201c091282603c9398155b8b05aaae9eb4cdf0abed88e6c5ef"),
    "noc_val": ("manuscript/prereg/2026-10-27_c_en/cen_nocaps_val.tsv",
                "6add90eb421523cdd65f47a8f9789f9342421b2b28169dc013f863f1edd0dfac"),
    "gc1": (f"{PDIR}/G_C1_record.json", "1f65b2aea02583aecf4891193ded375951da6c28d3dce61391dc37578924e33b"),
    "prov": (f"{PDIR}/g_c2_provenance.json", "e242623fdcd984a5ddcb21732f2ff5adeb65cc23c50e64af9ae1b28cd4c7819b"),  # W3: registered before any scan
}
N = {"xm": 3600, "xm_split": {"test": 1399, "validation": 456, "train": 1745}, "oiv7": 41620, "xm456": 456,
     "l2p1": 41164, "l2p1_q11": 36707, "val": 4500, "val_xm": 43, "test": 10600}  # manifest l.303-306, RULE l.19
# Custody inputs (amendment §3): byte size and, where the host publishes one, the hash, known before download.
INFO = {"name": "nocaps_test_image_info.json", "size": 3069304}  # Drive 1y8rBQZp5jsKS-eO2xmFPeJr8Rz-ShQst
OIL = {"name": "test-images-with-rotation.csv", "size": 45227339,
       "md5": "d832feb775b3cb78077bf8ae350adce5"}  # x-goog-hash md5=2DL+t3Wzy3gHe/iuNQrc5Q==
OI_HEADER = ["ImageID", "Subset", "OriginalURL", "OriginalLandingURL", "License", "AuthorProfileURL", "Author",
             "Title", "OriginalSize", "OriginalMD5", "Thumbnail300KURL", "Rotation"]
OI_TEST_URL = "https://open-images-dataset.s3.amazonaws.com/test/{file}"  # CC-220 B3; c_pvr.py w25 must equal it
INFO_TOP = {"images", "licenses", "info"}
INFO_IMG = {"id", "open_images_id", "height", "width", "coco_url", "file_name", "license", "date_captured"}
VAL_HEADER = "#id\tfile\turl\tdomain"
VAL_LINE = re.compile(r"^[0-9]+\t[0-9a-f]{16}\.jpg\thttps?://[a-zA-Z0-9./_-]+\.jpg\t[a-z0-9-]+$")
HEX16 = re.compile(r"[0-9a-f]{16}")
BARRED = re.compile(r"annotations|labels|captions|/dev/shm/c_pvr_gb", re.I)  # CC-220 B2, CC-221 B1(iii)/(iv)

HF = "https://huggingface.co/datasets"
MB = f"{HF}/Gregor/mblip-train/resolve/123e944ed13e5108285e70b58983def207301754"
SFT = {  # amendment §5.1: url, size, sha256 (= HF LFS oid at the pinned revision), image key, record key (W5)
    "mblip_mix_v1": {"url": f"{MB}/task_mix_mt.json", "size": 747734272, "key": "image_id", "record_key": "context",
                     "sha256": "72c60ff988e367499cb7e97e08a01a7a17f23642ce7c7d69282e4dfd4e4353ef"},
    "mblip_mix_v2": {"url": f"{MB}/task_mix_v2_mt.json", "size": 962641896, "key": "image_id",
                     "record_key": "context",
                     "sha256": "4dfe4ab0e1629118b8f73ae191720435f19e25267e6d6d975fcc32764c4b149d"},
    "mblip_capfilt_raw": {"url": f"{MB}/blip_captions/ccs_synthetic_filtered_large_2273005_raw.json",
                          "size": 506886927, "key": "jpg", "record_key": "caption", "extra_keys": ("url",),
                          "flickr_min": 1,
                          "sha256": "23229e1e500ceb826fcd865f4b2138dda57203b444137dbe4a132c155a78e01a"},
    "llava_mix665k": {"url": f"{HF}/liuhaotian/LLaVA-Instruct-150K/resolve/9d451dc7629cfe0469f6ae4432b765cd603d5fcb/"
                             "llava_v1_5_mix665k.json", "size": 1029887963, "key": "image", "record_key": "id",
                      "sha256": "ce959ce6e23073ee1cd1a8a2ef1c633768c10d4174327b8b2dc7113b91af6cf8"},
    "pangeains": {"url": f"{HF}/neulab/PangeaInstruct/resolve/d0819917abe1cae38c008de0ca172f885f1f26a4/"
                         "PangeaIns.json", "size": 12022821567, "key": "image", "record_key": "id",
                  "n_records": 6450624,  # S18: "PangeaIns.json (# samples: 6450624)"
                  "sha256": "40481cd8b2f33233c6889e1135ea129dbebc9917ad0eacfbda511b94b72e49ce"},
}
MODELS = {  # G-C1 CLEAN-candidates on NoCaps test (record stop_check, llava_handling); all under the census rule
    "Gregor/mblip-bloomz-7b": (("mblip_mix_v1", "mblip_mix_v2", "mblip_capfilt_raw"), True, "VI"),
    "Gregor/mblip-mt0-xl": (("mblip_mix_v1", "mblip_mix_v2", "mblip_capfilt_raw"), True, "VI"),
    "neulab/Pangea-7B": (("pangeains",), True, "VI"),
    "liuhaotian/llava-v1.5-7b": (("llava_mix665k",), True, "EN"),
}
VI_SETS = {"openvivqa_dev": "openvivqa", "vitextcaps_test": "vitextcaps", "viecap4h_private_test": "viecap"}
VI_DEFERRED = {"vitextcaps_test", "viecap4h_private_test"}  # conditional sets: own amendment when released (N12)
ORIGINS = ("OI", "non-OI", "web", "undetermined")
CAPFILT_RULE = "image"  # [registered default, Q-FLICKR]: a Flickr-photo match leaves that image, count only


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def fault(msg: str):
    raise SystemExit(f"FAULT: {msg}")


def refuse(p) -> Path:
    if BARRED.search(str(p)):
        raise SystemExit(f"REFUSED: {p} (annotations/labels/captions paths are never an id source)")
    return Path(p)


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with open(refuse(p), "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def pinned(root: Path, key: str, pins: dict) -> Path:
    p = root / pins[key][0]
    if sha_file(p) != pins[key][1]:
        fault(f"{pins[key][0]} differs from its pin {pins[key][1][:8]}")
    return p


def write_once(p: Path, data: bytes, mode: int = 0o444) -> str:
    """tmp + os.replace; refuses an existing file (one write)."""
    if p.exists():
        raise SystemExit(f"REFUSED: {p} exists (one write only)")
    with tempfile.NamedTemporaryFile(dir=p.parent, delete=False) as t:
        t.write(data)
    os.chmod(t.name, mode)
    os.replace(t.name, p)
    return sha_bytes(data)


def access_log(sealed: Path, action: str, path, sha: str) -> None:
    with open(sealed / "ACCESS_LOG.tsv", "a") as f:
        f.write(f"{utc()}\tgates.py\t{action}\t{path}\t{sha}\n")


def jdump(o) -> bytes:
    return (json.dumps(o, sort_keys=True, indent=1, ensure_ascii=True) + "\n").encode()


def ids_bytes(ids) -> bytes:
    return "".join(f"{i}\n" for i in sorted(ids)).encode()


# ------------------------------------------------------------------------------------------------ G-A
def step0(root: Path, pins: dict = PINS) -> dict:
    """Prereg §2.2 asserts (a)-(d) (W10) and the ids-only NoCaps val source (CC-221 B1(iv)/B2)."""
    xm = pinned(root, "xm_src", pins).read_text().split()
    if len(xm) != N["xm"] or len(set(xm)) != N["xm"] or not all(HEX16.fullmatch(i) for i in xm):
        fault("(a) xm3600_ids.txt is not 3,600 unique 16-hex ids")
    with open(pinned(root, "xm_attr", pins), encoding="utf-8", newline="") as f:
        sub = {r["ImageID"]: r["Subset"] for r in csv.DictReader(f)}  # ImageID and Subset only (xm3600_oiv7 l.103)
    if set(sub) != set(xm) or dict(Counter(sub.values())) != N["xm_split"]:
        fault("(b) XM3600 OI split counts are not test 1,399 / validation 456 / train 1,745")
    val7 = pinned(root, "oiv7_val", pins).read_text().split()
    x456 = set(pinned(root, "xm456", pins).read_text().split())
    if len(set(val7)) != N["oiv7"] or len(val7) != N["oiv7"] or len(x456) != N["xm456"]:
        fault("OIV7 val list is not 41,620 ids or the XM list is not 456")
    if not x456 <= set(xm):
        fault("(c) an id of 54966ca7 is not in the 3,600-id list")
    if x456 != set(xm) & set(val7):
        fault("(d) the 456 differ from the 3,600-id list intersected with 4b7a1813")
    val = noc_val_ids(pinned(root, "noc_val", pins))
    if not val <= set(val7) or len(val & x456) != N["val_xm"]:
        fault("NoCaps val is not inside OIV7 val, or its XM3600 overlap is not 43")
    l2p1 = set(val7) - x456
    l2p1_q11 = l2p1 - (val - x456)
    if len(l2p1) != N["l2p1"] or len(l2p1_q11) != N["l2p1_q11"]:
        fault("L2-P1 bases are not 41,164 / 36,707")
    return {"xm": set(xm), "xm_split": sub, "oiv7": set(val7), "val": val, "l2p1": l2p1, "l2p1_q11": l2p1_q11}


def noc_val_ids(p: Path) -> set[str]:
    """Schema-only: header and every row match id/file/url/domain (no field can hold a caption); OI id = file[:-4]."""
    lines = refuse(p).read_text(encoding="utf-8").split("\n")
    if lines[0] != VAL_HEADER or lines[-1] != "" or not all(VAL_LINE.match(x) for x in lines[1:-1]):
        fault(f"{p}: not the ids-only schema {VAL_HEADER!r}")
    ids = {x.split("\t")[1][:-4] for x in lines[1:-1]}
    if len(ids) != N["val"] or len(lines) - 2 != N["val"]:
        fault(f"{p}: not 4,500 unique OI ids")
    return ids


def info_ids(p: Path, strict: bool = True) -> list[str]:
    """NoCaps test image info: key schema only (no 'annotations' key, image keys within the documented set);
    returns the OI ids. No other key is accessed."""
    b = refuse(p).read_bytes()
    if strict and len(b) != INFO["size"]:
        fault(f"{p}: {len(b)} B, not {INFO['size']}")
    d = json.loads(b)
    if not isinstance(d, dict) or not set(d) <= INFO_TOP or "images" not in d:
        fault(f"{p}: top-level keys {sorted(d) if isinstance(d, dict) else type(d)} outside {sorted(INFO_TOP)}")
    ims = d["images"]
    if any(not set(im) <= INFO_IMG for im in ims):
        fault(f"{p}: an image record has a key outside {sorted(INFO_IMG)}")
    oid = [im["open_images_id"] for im in ims]
    n = N["test"]
    if (len(ims) != n or len(set(oid)) != n or len({im["id"] for im in ims}) != n
            or any(not HEX16.fullmatch(o) or im["file_name"] != o + ".jpg" for o, im in zip(oid, ims))):
        fault(f"{p}: not {n} unique 16-hex open_images_id with file_name = id + .jpg")
    return oid


def oi_rows(p: Path, strict: bool = True):
    """The official OI test image list: md5 = bucket md5, exact 12-column header (no label column), Subset = test."""
    if strict and (sha_file(p, "md5") != OIL["md5"] or p.stat().st_size != OIL["size"]):
        fault(f"{p}: md5/size differ from the bucket's {OIL['md5'][:8]} / {OIL['size']}")
    with open(refuse(p), encoding="utf-8", newline="") as f:
        rd = csv.reader(f)
        if next(rd) != OI_HEADER:
            fault(f"{p}: header is not the 12-column image-list header")
        for r in rd:
            if len(r) != len(OI_HEADER) or r[1] != "test" or not HEX16.fullmatch(r[0]):
                fault(f"{p}: a row is not a 16-hex test ImageID")
            yield r


def ga_compute(root: Path, ga: Path, pins: dict = PINS, strict: bool = True):
    s = step0(root, pins)
    test = info_ids(ga / INFO["name"], strict)
    oi_test = {r[0] for r in oi_rows(ga / OIL["name"], strict)}
    t = set(test)
    if oi_test & s["oiv7"]:
        fault("the OI test list shares an id with OIV7 val")
    other = t - oi_test
    if other:
        fault(f"{len(other)} NoCaps-test ids are not in the official OI test list (nocaps.org: sourced from OI test)")
    xm_hit = t & s["xm"]
    removed = xm_hit | (t & s["oiv7"]) | (t & s["val"])
    remaining = t - removed
    counts = {
        "label": LABEL, "nocaps_test": len(t), "in_oi_test": len(t & oi_test), "in_oiv7_val": len(t & s["oiv7"]),
        "other": len(other), "oi_test_list_n": len(oi_test),
        "x_l2p1_41164": len(t & s["l2p1"]), "x_l2p1_36707": len(t & s["l2p1_q11"]),
        "x_xm3600_3600": len(xm_hit), "x_xm3600_by_split": dict(sorted(Counter(s["xm_split"][i] for i in xm_hit).items())),
        "xm_expected_by_chance": round(N["xm_split"]["test"] * len(t) / len(oi_test), 1),
        "x_nocaps_val": len(t & s["val"]), "removed": len(removed), "remaining": len(remaining),
    }
    return ids_bytes(remaining), counts


def gate_a_join(root: Path, ga: Path, info_sha: str, oi_sha: str, pins: dict = PINS, strict: bool = True,
                gates_sha: str | None = None) -> dict:
    """W1: refuses if either output exists; on any FAULT nothing is written (inputs kept; amendment §4.2). Order:
    xm3600 copy, ga_counts.json (carries ga_remaining_sha256), then ga_remaining_ids.txt last as the commit marker."""
    out = root / PDIR
    for name in ("ga_remaining_ids.txt", "ga_counts.json"):
        if (out / name).exists():
            raise SystemExit(f"REFUSED: {name} exists; G-A writes once (use verify; a partial write goes to a ruling)")
    for name, want in ((INFO["name"], info_sha), (OIL["name"], oi_sha)):
        if sha_file(ga / name) != want:
            fault(f"{name}: sha256 differs from the one logged at download ({want[:8]})")
    rem, counts = ga_compute(root, ga, pins, strict)  # any FAULT here stops before a file is written
    xm_copy = out / "xm3600_all_ids.txt"
    if not xm_copy.exists():
        shutil.copyfile(root / pins["xm_src"][0], xm_copy)
    if sha_file(xm_copy) != pins["xm_src"][1]:
        fault("xm3600_all_ids.txt copy differs from 1bd00f46")
    counts.update({"utc": utc(), "gates_sha256": gates_sha or sha_file(Path(__file__)),
                   "inputs": {INFO["name"]: info_sha, OIL["name"]: oi_sha, "xm3600_all_ids.txt": pins["xm_src"][1],
                              **{pins[k][0]: pins[k][1] for k in ("xm_attr", "oiv7_val", "xm456", "noc_val")}},
                   "ga_remaining_sha256": sha_bytes(rem)})
    write_once(out / "ga_counts.json", jdump(counts))
    write_once(out / "ga_remaining_ids.txt", rem)  # last: its presence marks a complete G-A
    access_log(ga.parent, "gate-a join", ga, sha_bytes(rem))
    return counts


def gate_a_verify(root: Path, ga: Path, pins: dict = PINS, strict: bool = True) -> str:
    """CC-221 B1(v)/B4: any later gates.py must reproduce ga_remaining_ids.txt byte for byte from the kept inputs."""
    out = root / PDIR
    if not (out / "ga_counts.json").exists() or not (out / "ga_remaining_ids.txt").exists():
        fault("G-A is absent or partial (ga_counts.json without ga_remaining_ids.txt); goes to a ruling")
    rec = json.loads((out / "ga_counts.json").read_text())
    for name in (INFO["name"], OIL["name"]):
        if sha_file(ga / name) != rec["inputs"][name]:
            fault(f"{name} changed since G-A")
    rem, _ = ga_compute(root, ga, pins, strict)
    if sha_bytes(rem) != rec["ga_remaining_sha256"] or sha_file(out / "ga_remaining_ids.txt") != sha_bytes(rem):
        fault("this gates.py does not reproduce ga_remaining_ids.txt; G-B does not run")
    return sha_bytes(rem)


def gate_a_pin(ga: Path, strict: bool = True) -> dict:
    """N5: the step-3 check before the shas are logged. NoCaps test info: size 3,069,304 B and first byte '{'
    (no parse). OI list: bucket md5, size and the exact header line (no data row read). A failed file is discarded."""
    ip, op = ga / INFO["name"], ga / OIL["name"]
    with open(refuse(ip), "rb") as f:
        first = f.read(1)
    if first != b"{" or (strict and ip.stat().st_size != INFO["size"]):
        fault(f"{ip.name}: first byte {first!r} / {ip.stat().st_size} B; discard it and download again")
    if strict and (sha_file(op, "md5") != OIL["md5"] or op.stat().st_size != OIL["size"]):
        fault(f"{op.name}: md5/size differ from the bucket's {OIL['md5'][:8]} / {OIL['size']}; discard it")
    with open(refuse(op), encoding="utf-8", newline="") as f:
        if next(csv.reader(f)) != OI_HEADER:
            fault(f"{op.name}: header is not the 12-column image-list header")
    return {n: {"sha256": sha_file(ga / n), "md5": sha_file(ga / n, "md5"), "bytes": (ga / n).stat().st_size}
            for n in (INFO["name"], OIL["name"])}


# ------------------------------------------------------------------------------------------------ G-C2
HEX_RX = re.compile(rb"(?<![0-9a-fA-F])[0-9a-fA-F]{16}(?![0-9a-fA-F])")  # W7: any case, lowercased before the join
VI_RX = re.compile(rb"(?i)open[_-]?vivqa|vi[_-]?textcaps|viet?cap")  # N12 variants
SEP = rb"(?:\\?/|%2[Ff])"  # '/', the JSON-escaped '\/' (W6) or the percent-encoded '%2F' (CC-222r2 W1)
FHOST_RX = re.compile(rb"(?i)static\.?flickr\.com")  # raw static-image host count (parse-rate denominator)
FLICKR_RX = re.compile(rb"(?i)static\.?flickr\.com" + SEP + rb"(?:\d+" + SEP + rb"){0,2}(\d+)[_.]"
                       rb"|flickr\.com" + SEP + rb"photos" + SEP + rb"[^/\\\"\s%]+" + SEP + rb"(\d+)")
FLICKR_FLOOR = 0.90  # CC-222r2 W1 [proposal, registered now]: parsed / host on a file with a positive control
KEY_RX = re.compile(rb'"((?:[^"\\]|\\.){0,256})"\s*:')  # every JSON key name (W5 / CC-222r2 W3)
IMGLIKE = re.compile(r"(?i)image|img|photo|file|url|jpg")  # a key whose name CONTAINS one of these, any punctuation
STR = rb'"(?:[^"\\]|\\.){0,2048}"'
TAIL = 1 << 20  # > the longest match any pattern can make (128 x 2 KB list), so a match before the cut is complete
MAX_TRANSPORT = 3  # W8: a transport FAULT (bytes not the pinned ones) may be retried; the 3rd closes the file


def vi_norm(tok: str) -> str:
    t = re.sub(r"[_-]", "", tok.lower())
    return "openvivqa" if t.startswith("open") else "vitextcaps" if t.startswith("vitext") else "viecap"


def scan_stream(read, key: str, record_key: str, chunk: int = 1 << 22, tail: int = TAIL) -> dict:
    """One pass over a JSON byte stream. Kept: image references under `key` (census), every 16-hex token, Flickr
    photo ids, the VI dataset names, and counts of records, image-like key names and Flickr hosts. Chunked with a
    TAIL overlap: matches starting before the cut are complete and handled once; the next pass starts at the cut
    with one byte of look-behind context. A value is a string, an integer, a list of up to 128 strings, or null.
    Never raises on content: the caller checks the counts after the sha (content vs transport FAULT, W8)."""
    k = re.escape(key.encode())
    rxs = {"key": re.compile(rb'"' + k + rb'"\s*:'),
           "img": re.compile(rb'"' + k + rb'"\s*:\s*(\[\s*(?:' + STR + rb'\s*,?\s*){0,128}\]|' + STR + rb'|-?\d+|null)'),
           "rec": re.compile(rb'"' + re.escape(record_key.encode()) + rb'"\s*:'), "like": KEY_RX,
           "hex": HEX_RX, "vi": VI_RX, "flickr": FLICKR_RX, "fhost": FHOST_RX}
    c = Counter()
    hexes, flickr, vi, census, like = set(), set(), Counter(), Counter(), Counter()
    buf, start, eof = b"", 0, False
    while not eof:
        b = read(chunk)
        eof = not b
        buf += b
        cut = len(buf) if eof else len(buf) - tail
        if cut <= start:
            continue
        for name, rx in rxs.items():
            for m in rx.finditer(buf, start):
                if m.start() >= cut:
                    break
                c[name] += 1
                if name == "img":
                    try:
                        v = json.loads(m.group(1))
                    except ValueError:
                        c["bad_value"] += 1
                        continue
                    c["null"] += v is None
                    for p in (v if isinstance(v, list) else [] if v is None else [v]):
                        c["img_refs"] += 1
                        census[census_key(str(p))] += 1
                elif name == "hex":
                    hexes.add(m.group().decode().lower())
                elif name == "vi":
                    vi[vi_norm(m.group().decode())] += 1
                elif name == "like":
                    try:
                        kname = json.loads(b'"' + m.group(1) + b'"')
                    except ValueError:
                        kname = "<undecodable key>"  # counted: unpinned, so UNCHECKABLE for a census model
                    if kname == "<undecodable key>" or IMGLIKE.search(kname):
                        like[kname] += 1
                elif name == "flickr":
                    c["flickr_static"] += m.group(1) is not None
                    flickr.add((m.group(1) or m.group(2)).decode())
        keep = cut - 1  # one byte of look-behind context
        buf, start = buf[keep:], 1  # rescan starts at the old cut: each match is handled once
    return {"hex16": sorted(hexes), "flickr": sorted(flickr), "vi_tokens": dict(sorted(vi.items())),
            "census": dict(sorted(census.items())), "image_like_keys": dict(sorted(like.items())),
            "n_key": c["key"], "n_values": c["img"], "n_bad_value": c["bad_value"], "n_null": c["null"],
            "n_img_refs": c["img_refs"], "n_records": c["rec"], "n_flickr_host": c["fhost"],
            "n_flickr_static": c["flickr_static"],
            "n_flickr_host_unparsed": max(0, c["fhost"] - c["flickr_static"])}  # unknown, disclosed


def census_key(path: str) -> str:
    """W4, extended (amendment §5.2): the FULL directory path with every digit masked to '#' (length kept, so 8-digit
    and 10-digit names stay apart); a bare file name is keyed '~' + its digit-masked stem. Class: hex16/digits/other."""
    d, _, f = path.rpartition("/")
    stem = f.rsplit(".", 1)[0]
    key = re.sub(r"[0-9]", "#", d) if d else "~" + re.sub(r"[0-9]", "#", stem)
    if d and key.startswith("~"):  # W8: a directory named '~...' never equals a bare-name key
        key = "./" + key
    cls = "hex16" if HEX16.fullmatch(stem.lower()) else "digits" if stem.isdigit() else "other"
    return key + "|" + cls


def content_faults(rec: dict, spec: dict) -> list[str]:
    """Checks on bytes whose sha equals the pin: final on first occurrence (W5, W6, W8)."""
    out = []
    if rec["n_key"] == 0:
        out.append(f"no '{spec['key']}' key at all (n_key == 0)")
    if rec["n_values"] != rec["n_key"] or rec["n_bad_value"]:
        out.append(f"{rec['n_key']} '{spec['key']}' keys but {rec['n_values'] - rec['n_bad_value']} parsed values")
    if spec.get("flickr_min", 0):  # CC-222r2 W1: only a file with a positive control can FAULT on Flickr forms
        if rec["n_flickr_static"] < spec["flickr_min"]:
            out.append(f"positive control: {rec['n_flickr_static']} Flickr ids, at least {spec['flickr_min']} required")
        elif rec["n_flickr_static"] < FLICKR_FLOOR * rec["n_flickr_host"]:
            out.append(f"parse rate {rec['n_flickr_static']}/{rec['n_flickr_host']} below the floor {FLICKR_FLOOR}")
    return out


def _logged_faults(gc2: Path, key: str) -> Counter:
    """W7 (CC-222r2): every FAULT attempt is mirrored in ACCESS_LOG.tsv; the count there cannot be reset silently."""
    log = gc2.parent / "ACCESS_LOG.tsv"
    lines = log.read_text().splitlines() if log.exists() else []
    return Counter(x.split("\t")[2].rsplit(" ", 1)[-1] for x in lines
                   if x.split("\t")[2:4] and x.split("\t")[2].startswith("gate-c2 FAULT") and x.split("\t")[3] == key)


def fault_state(gc2: Path, key: str) -> tuple[list, bool]:
    p = gc2 / f"{key}.fault.json"
    att = json.loads(p.read_text())["attempts"] if p.exists() else []
    logged = _logged_faults(gc2, key)
    if logged["content"] > sum(a["kind"] == "content" for a in att) or \
            logged["transport"] > sum(a["kind"] == "transport" for a in att):
        fault(f"{key}.fault.json holds fewer attempts than ACCESS_LOG.tsv (reset?); goes to a ruling")
    closed = any(a["kind"] == "content" for a in att) or sum(a["kind"] == "transport" for a in att) >= MAX_TRANSPORT
    return att, closed


def _log_fault(gc2: Path, key: str, kind: str, msg: str) -> None:
    att, _ = fault_state(gc2, key)
    att.append({"utc": utc(), "kind": kind, "msg": msg})
    p = gc2 / f"{key}.fault.json"
    tmp = p.with_suffix(".tmp")
    tmp.write_bytes(jdump({"label": LABEL, "file": key, "attempts": att}))
    os.replace(tmp, p)
    access_log(gc2.parent, f"gate-c2 FAULT {kind}", key, f"attempt {len(att)}")
    fault(f"{key}: {kind} FAULT, attempt {len(att)}: {msg}")


def gate_c2_scan(key: str, stream, gc2: Path, prov: dict, sft: dict = SFT) -> dict:
    spec = sft[key]
    out = gc2 / f"{key}.scan.json"
    if out.exists():
        raise SystemExit(f"REFUSED: {out} exists (one scan per pinned file)")
    if doc_decided(prov, key):
        raise SystemExit(f"REFUSED: {key} is decided by the registered provenance (undetermined components); no scan")
    att, closed = fault_state(gc2, key)
    if closed:
        raise SystemExit(f"REFUSED: {key} is closed by FAULT after {len(att)} attempt(s); its models are UNCHECKABLE")
    h, n = hashlib.sha256(), [0]

    def read(k: int) -> bytes:
        b = stream.read(k)
        h.update(b)
        n[0] += len(b)
        return b

    try:
        rec = scan_stream(read, spec["key"], spec["record_key"])
    except OSError as e:
        _log_fault(gc2, key, "transport", f"read error {type(e).__name__}")
    if n[0] != spec["size"] or h.hexdigest() != spec["sha256"]:
        _log_fault(gc2, key, "transport", f"{n[0]} B sha {h.hexdigest()[:8]}, pinned {spec['size']} B "
                                          f"{spec['sha256'][:8]}; no record written")
    bad = content_faults(rec, spec)
    if bad:
        _log_fault(gc2, key, "content", "; ".join(bad))
    rec.update({"label": LABEL, "file": key, "url": spec["url"], "sha256": spec["sha256"], "size": spec["size"],
                "utc": utc(), "gates_sha256": sha_file(Path(__file__)), "transport_retries": len(att)})
    write_once(out, jdump(rec))
    return rec


def valid_scan(p: Path, key: str, spec: dict) -> dict:
    """CC-222r2 W2: a scan record is used only if it is what the pinned scanner wrote for the pinned bytes: label,
    file, sha256, size and url equal SFT[key]; gates_sha256 equals the running gates.py; write-once mode 0444.
    Anything else is a FAULT and never counts toward CLEAN."""
    if p.stat().st_mode & 0o222:
        fault(f"{p.name}: writable; not a write-once scan record")
    r = json.loads(p.read_text())
    want = {"label": LABEL, "file": key, "sha256": spec["sha256"], "size": spec["size"], "url": spec["url"],
            "gates_sha256": sha_file(Path(__file__))}
    bad = sorted(k for k, v in want.items() if r.get(k) != v)
    if bad:
        fault(f"{p.name}: {', '.join(bad)} differ from the pinned scan; record refused")
    return r


MAP_BARRED = re.compile(r"(?i)^(?:\./)?(?:flickr|xm3600)(?:/|$)|^~[#a-f]{16}$")  # CC-222r2 W5


def load_prov(root: Path, pins: dict = PINS, map_path: Path | None = None) -> dict:
    """W3: the provenance table is pinned by sha (origins frozen). Schema: origin in ORIGINS; every component cites
    at least one registered source (url, utc, sha256); 'web' names its crawl. The optional post-census map may only
    add prefixes onto registered components and never re-map a registered prefix."""
    prov = json.loads(pinned(root, "prov", pins).read_text())
    src = prov["sources"]
    if any(not {"url", "utc", "sha256"} <= set(v) for v in src.values()):
        fault("provenance source without url/utc/sha256")
    for f, t in prov["files"].items():
        for name, comp in t["components"].items():
            if comp.get("origin") not in ORIGINS:
                fault(f"provenance {f}/{name}: origin outside {ORIGINS}")
            if not comp.get("cites") or any(ci.split()[0] not in src for ci in comp["cites"]):
                fault(f"provenance {f}/{name}: no cite, or a cite to an unregistered source")
            if comp["origin"] == "web" and not comp.get("crawl"):
                fault(f"provenance {f}/{name}: 'web' without a named web crawl")
        if any(c not in t["components"] for c in t["prefixes"].values()):
            fault(f"provenance {f}: a prefix maps to an unregistered component")
    if map_path is not None:
        extra = json.loads(refuse(map_path).read_bytes())["files"]
        for f, mp in extra.items():
            t = prov["files"].get(f)
            if t is None or any(c not in t["components"] for c in mp.values()):
                fault(f"prefix map {f}: maps onto a component that is not registered")
            if set(mp) & set(t["prefixes"]):
                fault(f"prefix map {f}: re-maps a registered prefix")
            if any(MAP_BARRED.search(k) for k in mp):
                fault(f"prefix map {f}: a flickr/, xm3600/ or bare-hex key may never be mapped (W2)")
            t["prefixes"] = {**t["prefixes"], **mp}
    return prov


def ptab(prov: dict, f: str) -> dict:
    if f not in prov["files"]:
        fault(f"no registered provenance for {f}")
    return prov["files"][f]


def doc_decided(prov: dict, f: str) -> list[str]:
    """Registered rule: an image-bearing component of undetermined origin cannot become CLEAN, so the file is
    decided by documentation (its models UNCHECKABLE on nocaps_test) and is not scanned."""
    comps = ptab(prov, f)["components"]
    return [f"{f}/{n}: image-bearing component of undetermined origin (decided by documentation)"
            for n, c in sorted(comps.items()) if c["origin"] == "undetermined" and c.get("image_bearing", True)]


def landing_ids(rows, keep: set[str]) -> dict[str, set[str]]:
    """N6: Flickr photo id -> SET of kept OI test ids, from OriginalLandingURL, else OriginalURL (image metadata)."""
    out: dict[str, set[str]] = {}
    for r in rows:
        if r[0] in keep:
            m = FLICKR_RX.search(r[3].encode()) or FLICKR_RX.search(r[2].encode())
            if m:
                out.setdefault((m.group(1) or m.group(2)).decode(), set()).add(r[0])
    return out


def eval_census(census: dict, table: dict) -> tuple[list[str], list[str]]:
    """W7 (CC-221a l.187, verbatim): 'an OI-sourced subset with no recoverable OI id = UNCHECKABLE for NoCaps test'.
    Longest registered prefix wins (a '~' key matches only itself). Per component: mixed hex16/non-hex16 stems ->
    UNCHECKABLE; no hex16 stem and origin OI or undetermined -> UNCHECKABLE; a census key without a prefix ->
    UNCHECKABLE; all refs hex16 -> joinable (the join decides); web -> unknown, disclosed."""
    comps, prefixes = table.get("components", {}), table.get("prefixes", {})
    agg, reasons, web = {}, [], []
    for ck, n in census.items():
        d, cls = ck.rsplit("|", 1)
        hit = [p for p in prefixes if d == p or d.startswith(p + "/")]  # dir keys never start with '~' (W8)
        if not hit:
            reasons.append(f"{d or '<empty>'}: no provenance prefix")
            continue
        agg.setdefault(prefixes[max(hit, key=len)], Counter())[cls] += n
    for comp, cnt in sorted(agg.items()):
        n, nh, origin = sum(cnt.values()), cnt["hex16"], comps[comp]["origin"]
        if 0 < nh < n:
            reasons.append(f"{comp}: {n - nh} of {n} refs have no recoverable OI id (mixed)")
        elif nh == 0 and origin in ("OI", "undetermined"):
            reasons.append(f"{comp}: origin {origin}, no recoverable OI id")
        elif nh == 0 and origin == "web":
            web.append(comp)
    return reasons, web


def gate_c2_join(root: Path, gc2: Path, ga: Path, map_path: Path | None = None, pins: dict = PINS,
                 models: dict = MODELS, sft: dict = SFT, strict: bool = True) -> dict:
    out = root / PDIR
    rem_sha = gate_a_verify(root, ga, pins, strict)  # W9: the join runs only on a reproduced G-A
    prov = load_prov(root, pins, map_path)
    gc1 = json.loads(pinned(root, "gc1", pins).read_text())
    st = {(e["model"], e["set"]): e["status"] for e in gc1["entries"]}
    for m in models:
        if st.get((m, "nocaps_test")) != "CLEAN-candidate":
            fault(f"{m} is not CLEAN-candidate on nocaps_test in the G-C1 record")
    rem = set((out / "ga_remaining_ids.txt").read_text().split())
    flickr_of = landing_ids(oi_rows(ga / OIL["name"], strict), rem)
    scans, notes = {}, []
    for f in sorted({f for fs, _, _ in models.values() for f in fs}):
        p = gc2 / f"{f}.scan.json"
        att, closed = fault_state(gc2, f)
        if doc_decided(prov, f):
            scans[f] = {"decided": doc_decided(prov, f)}
        elif p.exists():
            scans[f] = valid_scan(p, f, sft[f])
        elif closed:
            scans[f] = {"fault": f"scan FAULT after {len(att)} attempt(s): {att[-1]['msg']}"}
            notes.append(f"FAULT {f}: {scans[f]['fault']} -> its models UNCHECKABLE on nocaps_test; join continues")
        else:
            raise SystemExit(f"REFUSED: no scan record for {f} and its FAULT record is not closed; run or retry the scan")
    rec = {"label": LABEL, "utc": utc(), "gates_sha256": sha_file(Path(__file__)), "capfilt_rule": CAPFILT_RULE,
           "inputs": {"ga_remaining_ids.txt": rem_sha, "G_C1_record.json": pins["gc1"][1],
                      "g_c2_provenance.json": pins["prov"][1],
                      **({"prefix_map": sha_file(map_path)} if map_path else {}),
                      **{f"{f}.scan.json": sha_file(gc2 / f"{f}.scan.json") for f in scans
                         if (gc2 / f"{f}.scan.json").exists()}},
           "notes": notes, "models": {}}
    excl = set()
    for m, (files, census_rule, role) in models.items():
        hits, fl, vi, reasons, web = set(), set(), Counter(), [], []
        for f in files:
            s = scans[f]
            if "decided" in s or "fault" in s:
                reasons += s.get("decided", []) + ([s["fault"]] if "fault" in s else [])
                continue
            hits |= rem & set(s["hex16"])
            fl |= {i for x in s["flickr"] for i in flickr_of.get(x, ())}
            vi.update(s["vi_tokens"])
            if census_rule:
                r, w = eval_census(s["census"], ptab(prov, f))
                reasons += r
                web += w
                extra = {k for k, v in s["image_like_keys"].items()
                         if v and k not in {sft[f]["key"], *sft[f].get("extra_keys", ())}}
                reasons += [f"{f}: unpinned image-like key '{k}' present" for k in sorted(extra)]
                want = sft[f].get("n_records")
                if want is not None and s["n_records"] != want:
                    reasons.append(f"{f}: {s['n_records']} records, documented {want}")
        noc = "HIT" if hits else "UNCHECKABLE" if reasons else "CLEAN"  # N9: a HIT is final
        sets = {"nocaps_test": noc}
        for vs, tok in VI_SETS.items():
            if role == "EN":
                sets[vs] = "N/A"  # CC-221a Ruling 7: EN benchmark only, never CLEAN on a VI set
            elif vs in VI_DEFERRED:
                sets[vs] = "DEFERRED"  # N12: conditional sets get their own amendment when released
            elif st.get((m, vs)) != "CLEAN-candidate":
                sets[vs] = "UNCHECKABLE"
            else:  # docs-only rule (§5.4): name check here; the reverse check is the pre-PINS-A desk step
                sets[vs] = "UNCHECKABLE" if vi.get(tok, 0) else "CLEAN"
        if CAPFILT_RULE == "model" and fl and noc == "CLEAN":
            sets["nocaps_test"] = "HIT"
        if sets["nocaps_test"] == "CLEAN":
            excl |= fl  # upper bound; PINS-A keeps the matches of the models it pins (N7)
        rec["models"][m] = {"status": sets, "hex16_hits": sorted(hits), "flickr_matched_ids": sorted(fl),
                            "unchecked_reasons": reasons, "web_scale_components": sorted(set(web)),
                            "vi_tokens": dict(vi), "web_scale_pretraining": "unknown (disclosed)"}
    rec["flickr_image_exclusions"] = sorted(excl) if CAPFILT_RULE == "image" else []
    write_once(out / "G_C2_record.json", jdump(rec))
    for n in notes:
        print(n, file=sys.stderr)
    return rec


# ------------------------------------------------------------------------------------------------ selftest
def _must(tag: str, fn, *a, **k) -> None:
    try:
        fn(*a, **k)
    except SystemExit as e:
        if tag not in str(e):
            raise AssertionError(f"expected {tag!r}, got {e}") from None
        return
    raise AssertionError(f"guard did not fire: expected {tag!r}")


def _hexid(rng) -> str:
    return "%016x" % rng.getrandbits(64)


def _ph(k: int) -> int:
    """Synthetic Flickr photo id of OI-test row k; rows 2000 and 2001 share one photo (N6)."""
    return 777777 if k in (2000, 2001) else 900000 + k


def _fixture(base: Path, rng):
    """Synthetic files at the registered sizes: (pins, ga dir, expected remaining, OI test ids, test info)."""
    oi_test = sorted({_hexid(rng) for _ in range(20000)})
    oiv7 = sorted({_hexid(rng) for _ in range(N["oiv7"] + 50)})[:N["oiv7"]]
    train = [_hexid(rng) for _ in range(N["xm_split"]["train"])]
    xm = oi_test[:1399] + oiv7[:456] + train
    val = oiv7[413:413 + N["val"]]  # 43 of the 456 XM ids inside NoCaps val
    test = oi_test[1300:1300 + N["test"]]  # 99 XM test ids inside NoCaps test
    files = {
        "xm_src": "".join(f"{i}\n" for i in xm),
        "xm_attr": "ImageID,Subset,OriginalURL\n" + "".join(
            f"{i},{s},http://x\n" for i, s in zip(xm, ["test"] * 1399 + ["validation"] * 456 + ["train"] * 1745)),
        "oiv7_val": "".join(f"{i}\n" for i in oiv7),
        "xm456": "".join(f"{i}\n" for i in oiv7[:456]),
        "noc_val": VAL_HEADER + "\n" + "".join(
            f"{k}\t{i}.jpg\thttps://s3.amazonaws.com/nocaps/val/{i}.jpg\tnear-domain\n" for k, i in enumerate(val)),
        "gc1": "{}",
        "prov": "{}",
    }
    pins = {}
    for key, txt in files.items():
        p = base / "repo" / PINS[key][0]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(txt)
        pins[key] = (PINS[key][0], sha_file(p))
    (base / "repo" / PDIR).mkdir(parents=True, exist_ok=True)
    ga = base / "sealed" / "ga"
    ga.mkdir(parents=True)
    info = {"images": [{"id": k, "open_images_id": i, "file_name": i + ".jpg", "height": 1, "width": 1,
                        "coco_url": f"https://s3.amazonaws.com/nocaps/test/{i}.jpg", "license": 0,
                        "date_captured": "x"} for k, i in enumerate(test)], "licenses": [], "info": {}}
    (ga / INFO["name"]).write_text(json.dumps(info))
    rows = [",".join(OI_HEADER)] + [
        f"{i},test,https://c5.staticflickr.com/1/125/{_ph(k)}_ab_o.jpg,"
        f"{'' if k % 2 else f'https://www.flickr.com/photos/u/{_ph(k)}'},l,a,b,t,1,m,u,0"
        for k, i in enumerate(oi_test)]  # odd rows: no landing URL, so the OriginalURL fallback must match
    (ga / OIL["name"]).write_text("\n".join(rows) + "\n")
    expected = sorted(set(test) - set(xm))
    return pins, ga, expected, oi_test, info


def _st_step0(root: Path, pins: dict) -> None:
    # W10: each step-0 guard broken once
    for key, bad, tag in (("xm_src", lambda t: t.replace(t[:16], t[16:32], 1), "(a)"),
                          ("xm_attr", lambda t: t.replace(",train,", ",test,", 1), "(b)"),
                          ("xm456", lambda t: t[:-17] + "ffffffffffffffff\n", "(c)"),
                          ("noc_val", lambda t: t.replace("\tnear-domain\n", "\tnear-domain\tA dog.\n", 1),
                           "ids-only schema"),
                          ("noc_val", lambda t: t.replace("#id\tfile", "#id\tcaption", 1), "ids-only schema")):
        p = root / pins[key][0]
        orig = p.read_text()
        p.write_text(bad(orig))
        bad_pins = {**pins, key: (pins[key][0], sha_file(p))}
        _must(tag, step0, root, bad_pins)
        _must("differs from its pin", step0, root, pins)
        p.write_text(orig)
    p = root / pins["oiv7_val"][0]  # (d): an XM id dropped from OIV7 val breaks 456 == 3,600 ∩ OIV7
    orig = p.read_text()
    p.write_text(orig.replace(orig.split()[0], "0" * 16, 1))
    _must("(d)", step0, root, {**pins, "oiv7_val": (pins["oiv7_val"][0], sha_file(p))})
    p.write_text(orig)


def _st_ga(root: Path, ga: Path, pins: dict, expected: list, oi_test: list, info: dict) -> None:
    # G-A: one write, write order (W1), counts, determinism, verify, tamper
    out = root / PDIR
    isha, osha = sha_file(ga / INFO["name"]), sha_file(ga / OIL["name"])
    (out / "ga_counts.json").write_text("{}")  # stale counts file from an earlier attempt
    _must("ga_counts.json exists; G-A writes once", gate_a_join, root, ga, isha, osha, pins, strict=False, gates_sha="t")
    (out / "ga_counts.json").unlink()
    _must("logged at download", gate_a_join, root, ga, "0" * 64, osha, pins, strict=False, gates_sha="t")
    assert not (out / "ga_counts.json").exists() and not (out / "ga_remaining_ids.txt").exists()
    real_write, calls = write_once, []

    def crash_after_first(path, data, mode=0o444):  # a crash between the two writes
        if calls:
            raise OSError("simulated crash")
        calls.append(path)
        return real_write(path, data, mode)

    globals()["write_once"] = crash_after_first
    try:
        gate_a_join(root, ga, isha, osha, pins, strict=False, gates_sha="t")
        raise AssertionError("the simulated crash did not happen")
    except OSError as e:
        assert "simulated crash" in str(e), e
    finally:
        globals()["write_once"] = real_write
    assert calls == [out / "ga_counts.json"] and not (out / "ga_remaining_ids.txt").exists(), "ids are written last"
    _must("absent or partial", gate_a_verify, root, ga, pins, strict=False)
    _must("ga_counts.json exists; G-A writes once", gate_a_join, root, ga, isha, osha, pins, strict=False, gates_sha="t")
    (out / "ga_counts.json").chmod(0o644)
    (out / "ga_counts.json").unlink()  # the selftest clears it; a real partial write goes to a ruling
    c = gate_a_join(root, ga, isha, osha, pins, strict=False, gates_sha="t")
    assert c["remaining"] == len(expected) == N["test"] - 99 and c["x_xm3600_3600"] == 99, c
    assert c["x_l2p1_41164"] == c["x_l2p1_36707"] == c["x_nocaps_val"] == c["in_oiv7_val"] == 0
    assert c["x_xm3600_by_split"] == {"test": 99} and c["oi_test_list_n"] == len(oi_test)
    rem_p = out / "ga_remaining_ids.txt"
    assert rem_p.read_bytes() == ids_bytes(expected) and rem_p.read_bytes().endswith(b"\n")
    assert json.loads((out / "ga_counts.json").read_text())["ga_remaining_sha256"] == sha_bytes(ids_bytes(expected))
    assert (out / "xm3600_all_ids.txt").read_bytes() == (root / pins["xm_src"][0]).read_bytes()
    _must("writes once", gate_a_join, root, ga, isha, osha, pins, strict=False, gates_sha="t")
    assert gate_a_verify(root, ga, pins, strict=False) == sha_bytes(ids_bytes(expected))
    assert ga_compute(root, ga, pins, strict=False)[0] == ga_compute(root, ga, pins, strict=False)[0]
    keep = rem_p.read_bytes()  # partial write: counts present, ids absent
    rem_p.chmod(0o644)
    rem_p.unlink()
    _must("absent or partial", gate_a_verify, root, ga, pins, strict=False)
    _must("ga_counts.json exists; G-A writes once", gate_a_join, root, ga, isha, osha, pins, strict=False, gates_sha="t")
    rem_p.write_bytes(keep[17:])
    _must("does not reproduce", gate_a_verify, root, ga, pins, strict=False)
    rem_p.write_bytes(keep)
    assert gate_a_verify(root, ga, pins, strict=False) == sha_bytes(keep)
    # step-3 pin check (N5): first byte and header, nothing parsed beyond them
    assert set(gate_a_pin(ga, strict=False)) == {INFO["name"], OIL["name"]}
    ip, op = ga / INFO["name"], ga / OIL["name"]
    good_info, good_oi = ip.read_bytes(), op.read_bytes()
    ip.write_bytes(b"<html>interstitial</html>")
    _must("discard it", gate_a_pin, ga, False)
    ip.write_bytes(good_info)
    _must("B; discard it", gate_a_pin, ga, True)  # strict: the 3,069,304 B size
    # input-file guards (each FAULTs before any id is used)
    for d, tag in (({**info, "annotations": [{"caption": "x"}]}, "top-level keys"),
                   ({**info, "images": info["images"][:-1]}, "unique 16-hex"),
                   ({**info, "images": [{**info["images"][0], "caption": "x"}] + info["images"][1:]},
                    "outside")):
        ip.write_text(json.dumps(d))
        _must(tag, info_ids, ip, False)
    ip.write_bytes(good_info)
    _must("md5/size", oi_rows(op).__next__)
    op.write_text(good_oi.decode().replace("ImageID,Subset", "ImageID,LabelName", 1))
    _must("12-column", list, oi_rows(op, False))
    op.write_text(good_oi.decode().replace(",test,", ",train,", 1))
    _must("16-hex test ImageID", list, oi_rows(op, False))
    oiv7_id = (root / pins["oiv7_val"][0]).read_text().split()[999]  # N1: an OIV7 val id inside the OI test list
    op.write_text(good_oi.decode() + f"{oiv7_id},test,u,,l,a,b,t,1,m,u,0\n")
    _must("shares an id with OIV7 val", ga_compute, root, ga, pins, strict=False)
    op.write_bytes(good_oi)
    ip.write_text(json.dumps({**info, "images": info["images"][:-1] + [
        {**info["images"][-1], "open_images_id": "f" * 16, "file_name": "f" * 16 + ".jpg"}]}))
    _must("not in the official OI test list", ga_compute, root, ga, pins, strict=False)
    ip.write_bytes(good_info)
    for bad in ("x/oidv7-test-annotations-human-imagelabels.csv", "data/datasets/nocaps/nocaps_val_4500_captions.json",
                "/dev/shm/c_pvr_gb/filtered-test.csv", "oi-test-labels.csv"):
        _must("REFUSED", refuse, bad)


def _st_scanner(rng) -> None:
    """Chunk-edge exactness, value forms, census keys, W5/W6/W7 counts, N12 name variants."""
    ids = [_hexid(rng) for _ in range(3000)]
    parts = []
    for k, i in enumerate(ids):
        hx = i.upper() if k % 5 == 1 else i  # W7: upper-case ids must still be found, lower-cased
        img = (f'"textvqa/train_images/{hx}.jpg"' if k % 3 else
               f'["coco/train2017/{k:012d}.jpg", "vg/VG_100K/{k}.jpg"]')
        fl = (f"http:\\/\\/farm3.static.flickr.com\\/12\\/{k}_x.jpg" if k % 2 else
              f"https://c5.staticflickr.com/1/125/{k}_ab_o.jpg")  # W6: escaped and two-segment forms
        parts.append(f'{{"id": "{k}", "image": {img}, "conversations": [{{"value": "a \\"image\\": {i}0 '
                     f'{i[:15]} OpenViVQA {fl}"}}]}}')
    parts += ['{"id": "t", "image": null, "conversations": []}',
              '{"id": "n", "image": 1234567, "conversations": []}',
              '{"id": "m", "image": [' + ", ".join(f'"multi/img/{j}.jpg"' for j in range(20)) + ']}',
              '{"id": "v", "value": "Open_ViVQA vi-textcaps VietCap"}',
              '{"id": "q", "bad\\x": 0}',
              '{"id": "p", "image-path": 1, "Image URL": 2, "img.url": 3, "Image_File": 4, "ph\\u006fto id": 5}']
    blob = ("[" + ", ".join(parts) + "]").encode()
    one = scan_stream(io.BytesIO(blob).read, "image", "id", chunk=len(blob) + 1)
    for ch in (4099, 65537, 300001):  # small tail: many chunk edges inside a 0.8 MB blob
        assert scan_stream(io.BytesIO(blob).read, "image", "id", chunk=ch, tail=4096) == one, ch
    long = '{"id": "L", "image": [' + ", ".join(f'"long/{"x" * 1500}/{j}.jpg"' for j in range(128)) + ']}'
    big = b"[" + b", ".join([blob[1:-1], long.encode(), blob[1:-1], blob[1:-1]]) + b"]"  # N1: one 190 KB match
    full = scan_stream(io.BytesIO(big).read, "image", "id", chunk=len(big) + 1)
    assert scan_stream(io.BytesIO(big).read, "image", "id", chunk=65537) == full  # edges at the registered TAIL
    assert full["n_values"] == full["n_key"] == 3 * 3003 + 1 and full["n_records"] == 3 * 3006 + 1
    assert set(one["hex16"]) == {i for k, i in enumerate(ids) if k % 3}, "hex16: any case, 15/17-hex runs skipped"
    assert one["n_key"] == one["n_values"] == one["n_records"] - 3 == 3003 and one["n_null"] == 1
    assert one["n_img_refs"] == 2000 + 2 * 1000 + 1 + 20
    assert one["vi_tokens"] == {"openvivqa": 3001, "vitextcaps": 1, "viecap": 1}
    assert one["n_flickr_host"] == one["n_flickr_static"] == 3000 and len(one["flickr"]) == 3000
    assert one["n_flickr_host_unparsed"] == 0
    assert one["census"] == {"textvqa/train_images|hex16": 2000, "coco/train####|digits": 1000,
                             "vg/VG_###K|digits": 1000, "~#######|digits": 1, "multi/img|digits": 20}
    assert one["image_like_keys"] == {"image": 3003, "image-path": 1, "Image URL": 1, "img.url": 1, "Image_File": 1,
                                      "photo id": 1, "<undecodable key>": 1}, one["image_like_keys"]  # CC-222r2 W3: any punctuation
    spec = {"key": "image", "flickr_min": 1}
    assert content_faults(one, spec) == []
    # CC-222r2 W1: benign host forms never close a file; the positive control and the floor do
    good_fl = [f"http://static.flickr.com/{j}/{50 + j}_ab.jpg" for j in range(20)]
    benign = ["https://farm1.staticflickr.com/7/buddyicons/12345@N00.jpg",
              "https://combo.staticflickr.com/pw/images/favicon.ico",
              "http%3A%2F%2Ffarm4.static.flickr.com%2F3%2F777001_ab.jpg",
              "http://static.flickr.com/777002_x.jpg"]
    blob2 = json.dumps([{"id": j, "image": f"a/{j}.jpg", "u": u} for j, u in enumerate(good_fl + benign)]).encode()
    r2 = scan_stream(io.BytesIO(blob2).read, "image", "id")
    assert content_faults(r2, spec) == [] and r2["n_flickr_host_unparsed"] == 2, r2
    assert {"777001", "777002"} <= set(r2["flickr"]), "percent-encoded and server-less forms are parsed"
    low = json.dumps([{"id": j, "image": "a.jpg", "u": u} for j, u in enumerate(good_fl[:2] + benign[:1] * 8)])
    assert "below the floor" in content_faults(scan_stream(io.BytesIO(low.encode()).read, "image", "id"), spec)[0]
    zero = scan_stream(io.BytesIO(b'[{"id": 1, "image": "a/b.jpg", "u": "static.flickr.com/x.jpg"}]').read,
                       "image", "id")
    assert "positive control" in content_faults(zero, spec)[0]
    assert content_faults(zero, {"key": "image"}) == [], "no positive control: unparsed forms are only disclosed"
    assert "n_key == 0" in content_faults(scan_stream(io.BytesIO(b'[{"id": 1}]').read, "image", "id"), spec)[0]
    # census keys (W4 + extension): nested, xm3600-style, bare hex, bare 8-digit, ImageNet synset dir
    assert census_key("general/cambrian/images/textvqa/" + ids[0] + ".jpg") == \
        "general/cambrian/images/textvqa|hex16"
    assert census_key("00515760.jpg") == "~########|digits" and census_key("1000092795.jpg") == "~##########|digits"
    assert census_key("n01440764/n01440764_10026.JPEG") == "n########|other"
    assert census_key(ids[1].upper() + ".jpg").endswith("|hex16") and census_key(ids[1] + ".jpg").startswith("~")
    assert census_key("~12345678/a.jpg") == "./~########|other", "W8: a '~' directory never equals a bare key"


def _prov_fixture() -> dict:
    src = {"X": {"url": "u", "utc": "t", "sha256": "0" * 64}}
    comp = lambda o, **k: {"origin": o, "cites": ["X l.1"], **k}  # noqa: E731
    return {"sources": src, "files": {
        "a": {"components": {"coco": comp("non-OI")}, "prefixes": {"coco/train####": "coco"}},
        "b": {"components": {"tv": comp("OI"), "sg": comp("non-OI"), "laion": comp("web", crawl="LAION")},
              "prefixes": {"textvqa/train_images": "tv", "sharegpt4v": "sg", "laion": "laion"}},
        "l": {"components": {"coco": comp("non-OI")}, "prefixes": {"coco/train####": "coco"}},
        "d": {"components": {"u": comp("undetermined", image_bearing=True)}, "prefixes": {}},
        "f": {"components": {"coco": comp("non-OI")}, "prefixes": {"coco/train####": "coco"}},
        "c": {"components": {"coco": comp("non-OI")}, "prefixes": {"coco/train####": "coco"}},
        "r": {"components": {"coco": comp("non-OI")}, "prefixes": {"coco/train####": "coco"}},
        "n": {"components": {"cam": comp("non-OI"), "tv": comp("OI")},
              "prefixes": {"general/cambrian/images": "cam", "general/cambrian/images/textvqa": "tv"}}}}


def _st_c2(base: Path, ga: Path, pins: dict, expected: list, oi_test: list, rng) -> None:
    root = base / "repo"
    rem_p = root / PDIR / "ga_remaining_ids.txt"
    _st_scanner(rng)
    # provenance: pin, schema, post-census map (W3)
    pv = root / pins["prov"][0]
    good = _prov_fixture()
    for bad, tag in ((lambda d: d["files"]["a"]["components"]["coco"].update(origin="maybe"), "origin outside"),
                     (lambda d: d["files"]["a"]["components"]["coco"].update(cites=["Z l.1"]), "unregistered source"),
                     (lambda d: d["files"]["b"]["components"]["laion"].pop("crawl"), "without a named web crawl"),
                     (lambda d: d["files"]["a"]["prefixes"].update(x="nope"), "unregistered component"),
                     (lambda d: d["sources"]["X"].pop("sha256"), "url/utc/sha256")):
        d = json.loads(json.dumps(good))
        bad(d)
        pv.write_text(json.dumps(d))
        _must(tag, load_prov, root, {**pins, "prov": (pins["prov"][0], sha_file(pv))})
    pv.write_text(json.dumps(good))
    pins2 = {**pins, "prov": (pins["prov"][0], sha_file(pv))}
    _must("differs from its pin", load_prov, root, pins)
    mp = base / "map.json"
    mp.write_text(json.dumps({"files": {"a": {"coco/val####": "ghost"}}}))
    _must("not registered", load_prov, root, pins2, mp)
    mp.write_text(json.dumps({"files": {"a": {"coco/train####": "coco"}}}))
    _must("re-maps", load_prov, root, pins2, mp)
    for barred in ("flickr", "flickr/x", "xm3600/images", "./xm3600", "~##ab#cd##ef##a##"):
        mp.write_text(json.dumps({"files": {"a": {barred: "coco"}}}))
        _must("may never be mapped", load_prov, root, pins2, mp)
    mp.write_text(json.dumps({"files": {"a": {"coco/val####": "coco", "flickr30k_like": "coco"}}}))
    assert load_prov(root, pins2, mp)["files"]["a"]["prefixes"]["coco/val####"] == "coco"
    prov = load_prov(root, pins2)
    # W7 census rule, longest prefix (W4), unmapped xm3600-style keys
    nb = prov["files"]["n"]
    assert eval_census({"general/cambrian/images/textvqa|hex16": 5, "general/cambrian/images/coco|digits": 3},
                       nb) == ([], [])
    assert eval_census({"general/cambrian/images/textvqa|other": 5}, nb)[0] == ["tv: origin OI, no recoverable OI id"]
    tb = prov["files"]["b"]
    r, w = eval_census({"textvqa/train_images|hex16": 3, "textvqa/train_images|other": 1, "laion/#|digits": 2,
                        "xm3600/images|hex16": 4, "~##ab#cd##ef##a#|hex16": 1}, tb)
    assert w == ["laion"] and "tv: 1 of 4 refs have no recoverable OI id (mixed)" in r
    assert "xm3600/images: no provenance prefix" in r and "~##ab#cd##ef##a#: no provenance prefix" in r
    assert eval_census({"sharegpt4v/x|other": 1}, tb) == ([], [])
    tilde = {"components": {"cf": {"origin": "web"}}, "prefixes": {"~########": "cf"}}
    assert eval_census({"~########|digits": 2}, tilde) == ([], ["cf"])
    assert eval_census({"./~########|other": 2}, tilde)[0] == ["./~########: no provenance prefix"]
    und = {"components": {"u": {"origin": "undetermined"}}, "prefixes": {"x": "u"}}
    assert eval_census({"x/y|other": 5}, und)[0] == ["u: origin undetermined, no recoverable OI id"]
    assert doc_decided(prov, "d") and not doc_decided(prov, "a")
    # scans: record, one scan, transport retries, content FAULT final, doc-decided refusal (W8)
    gc2 = base / "sealed" / "gc2"
    gc2.mkdir()
    ok = b'[{"id": 1, "image": "coco/train2017/000000000001.jpg"}]'
    sft = {"a": {"url": "u", "size": len(ok), "sha256": sha_bytes(ok), "key": "image", "record_key": "id"},
           "f": {"url": "u", "size": len(ok), "sha256": "0" * 64, "key": "image", "record_key": "id"},
           "c": {"url": "u", "size": 11, "sha256": sha_bytes(b'[{"id": 1}]'), "key": "image", "record_key": "id"},
           "d": {"url": "u", "size": 1, "sha256": "0" * 64, "key": "image", "record_key": "id"}}
    gate_c2_scan("a", io.BytesIO(ok), gc2, prov, sft)
    _must("one scan", gate_c2_scan, "a", io.BytesIO(ok), gc2, prov, sft)
    for k in range(MAX_TRANSPORT):
        _must(f"transport FAULT, attempt {k + 1}", gate_c2_scan, "f", io.BytesIO(ok), gc2, prov, sft)
    _must("closed by FAULT after 3", gate_c2_scan, "f", io.BytesIO(ok), gc2, prov, sft)
    assert _logged_faults(gc2, "f") == Counter({"transport": 3}), "W7: each attempt is in ACCESS_LOG.tsv"
    sft["r"] = sft["f"]
    _must("transport FAULT, attempt 1", gate_c2_scan, "r", io.BytesIO(ok), gc2, prov, sft)
    (gc2 / "r.fault.json").unlink()  # a silent reset of the attempt count
    _must("fewer attempts than ACCESS_LOG", gate_c2_scan, "r", io.BytesIO(ok), gc2, prov, sft)
    del sft["r"]
    assert not (gc2 / "f.scan.json").exists()
    _must("content FAULT, attempt 1", gate_c2_scan, "c", io.BytesIO(b'[{"id": 1}]'), gc2, prov, sft)
    _must("closed by FAULT after 1", gate_c2_scan, "c", io.BytesIO(b'[{"id": 1}]'), gc2, prov, sft)
    _must("decided by the registered provenance", gate_c2_scan, "d", io.BytesIO(ok), gc2, prov, sft)
    _st_c2_join(base, ga, {**pins, "prov": pins2["prov"]}, expected, oi_test, sft)


def _st_c2_join(base: Path, ga: Path, pins: dict, expected: list, oi_test: list, sft: dict) -> None:
    """Join: W9 verify, statuses, HIT final, W5 keys and record count, W8 continuation, deferred VI sets."""
    root, gc2 = base / "repo", base / "sealed" / "gc2"
    rem_p, pv = root / PDIR / "ga_remaining_ids.txt", root / pins["prov"][0]
    pins2 = dict(pins)
    gc1 = {"entries": [{"model": m, "set": s, "status": "CLEAN-candidate"} for m in ("A", "B", "L", "D", "F", "K", "X")
                       for s in ("nocaps_test", *VI_SETS)]}
    gp = root / pins["gc1"][0]
    gp.write_text(json.dumps(gc1))
    pins2["gc1"] = (pins["gc1"][0], sha_file(gp))
    hit_id = expected[5]
    kof = {i: k for k, i in enumerate(oi_test)}
    ev = next(i for i in expected[6:] if kof[i] % 2 == 0 and kof[i] not in (2000, 2001))
    od = next(i for i in expected[6:] if kof[i] % 2 and kof[i] not in (2000, 2001))
    twin = sorted(oi_test[2000:2002])
    gsha = sha_file(Path(__file__))
    base_rec = {"hex16": [], "flickr": [], "vi_tokens": {}, "census": {}, "image_like_keys": {"image": 1},
                "n_records": 1, "label": LABEL, "gates_sha256": gsha}
    recs = {"a": {**base_rec, "hex16": [hit_id], "census": {"coco/train####|digits": 1, "zzz|other": 1},
                  "vi_tokens": {"openvivqa": 1}},
            "b": {**base_rec, "flickr": [str(_ph(kof[ev])), str(_ph(kof[od])), "777777"], "vi_tokens": {"viecap": 2},
                  "census": {"textvqa/train_images|hex16": 3, "sharegpt4v/x|other": 1}},
            "l": {**base_rec, "census": {"coco/train####|digits": 4}},
            "k": {**base_rec, "census": {"coco/train####|digits": 4}, "image_like_keys": {"image": 4, "file_name": 2},
                  "n_records": 9}}
    for f in "blk":
        sft[f] = {"url": f"u/{f}", "size": 7, "sha256": f * 64, "key": "image", "record_key": "id"}
    sft["k"]["n_records"] = 4
    sft["a"] = {**sft["a"], "url": "u/a", "size": 7, "sha256": "a" * 64}

    def put(f: str, **over) -> Path:  # a record as the scanner writes it: validated fields, write-once mode
        rp = gc2 / f"{f}.scan.json"
        if rp.exists():
            rp.chmod(0o644)
        rp.write_text(json.dumps({**recs[f], "file": f, "url": sft[f]["url"], "size": sft[f]["size"],
                                  "sha256": sft[f]["sha256"], **over}))
        rp.chmod(0o444)
        return rp

    for f in recs:
        put(f)
    prov_d = json.loads(pv.read_text())
    prov_d["files"]["k"] = prov_d["files"]["l"]
    pv.write_text(json.dumps(prov_d))
    pins2["prov"] = (pins["prov"][0], sha_file(pv))
    models = {"A": (("a",), True, "VI"), "B": (("b",), False, "VI"), "L": (("l",), True, "EN"),
              "D": (("d",), True, "VI"), "F": (("f",), True, "VI"), "K": (("k",), True, "VI")}
    rem_p.chmod(0o644)
    keep = rem_p.read_bytes()
    rem_p.write_bytes(keep[17:])
    _must("does not reproduce", gate_c2_join, root, gc2, ga, None, pins2, models, sft, strict=False)
    rem_p.write_bytes(keep)
    _must("no registered provenance for x", gate_c2_join, root, gc2, ga, None, pins2, {**models, "X": (("x",), True, "VI")},
          sft, strict=False)
    for over, tag in (({"sha256": "e" * 64}, "sha256 differ"), ({"file": "l"}, "file differ"),
                      ({"gates_sha256": "0" * 64}, "gates_sha256 differ"), ({"label": "x"}, "label differ"),
                      ({"url": "v"}, "url differ"), ({"size": 8}, "size differ")):
        put("b", **over)  # CC-222r2 W2: a forged or stale record is refused, never counted toward CLEAN
        _must(tag, gate_c2_join, root, gc2, ga, None, pins2, models, sft, strict=False)
    put("b").chmod(0o644)
    _must("writable", gate_c2_join, root, gc2, ga, None, pins2, models, sft, strict=False)
    put("b")
    out = gate_c2_join(root, gc2, ga, None, pins2, models, sft, strict=False)
    m = out["models"]
    assert m["A"]["status"]["nocaps_test"] == "HIT" and m["A"]["unchecked_reasons"], "a HIT is final (N9)"
    assert m["B"]["status"]["nocaps_test"] == "CLEAN" and m["B"]["status"]["openvivqa_dev"] == "CLEAN"
    assert m["B"]["status"]["vitextcaps_test"] == m["B"]["status"]["viecap4h_private_test"] == "DEFERRED"
    assert out["flickr_image_exclusions"] == sorted([ev, od, *twin]) == m["B"]["flickr_matched_ids"], "N6: a set"
    assert m["A"]["status"]["openvivqa_dev"] == "UNCHECKABLE", "a VI-set name in the lists"
    assert m["L"]["status"] == {"nocaps_test": "CLEAN", "openvivqa_dev": "N/A", "vitextcaps_test": "N/A",
                                "viecap4h_private_test": "N/A"}
    assert m["D"]["status"]["nocaps_test"] == "UNCHECKABLE" and "documentation" in m["D"]["unchecked_reasons"][0]
    assert m["F"]["status"]["nocaps_test"] == "UNCHECKABLE" and out["notes"], "W8: the join continues"
    assert m["K"]["status"]["nocaps_test"] == "UNCHECKABLE"
    assert any("file_name" in x for x in m["K"]["unchecked_reasons"])
    assert any("9 records, documented 4" in x for x in m["K"]["unchecked_reasons"])
    _must("one write", gate_c2_join, root, gc2, ga, None, pins2, models, sft, strict=False)
    (root / PDIR / "G_C2_record.json").unlink()
    _must("not CLEAN-candidate", gate_c2_join, root, gc2, ga, None, pins2, {"Z": (("a",), True, "VI")}, sft,
          strict=False)


def selftest() -> None:
    import random
    import urllib.request

    def no_net(*a, **k):
        raise OSError("selftest: network disabled")

    socket.socket, socket.create_connection = no_net, no_net  # type: ignore[assignment,misc]
    try:
        urllib.request.urlopen("http://example.invalid/", timeout=1)
    except OSError as e:
        assert "selftest: network disabled" in str(e), e
    else:
        raise AssertionError("a socket opened")
    rng = random.Random(20261102)
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        pins, ga, expected, oi_test, info = _fixture(base, rng)
        root = base / "repo"
        s0 = step0(root, pins)
        assert len(s0["l2p1"]) == 41164 and len(s0["l2p1_q11"]) == 36707
        _st_step0(root, pins)
        _st_ga(root, ga, pins, expected, oi_test, info)
        _st_c2(base, ga, pins, expected, oi_test, rng)
    # the real pinned id files, sha only (W10 reading: the parse itself is G-A step 0, after the CC-222 GO)
    real = {k: (ROOT / p).exists() and sha_file(ROOT / p) == s for k, (p, s) in PINS.items()}
    print("real pins (sha only):", " ".join(f"{k}={'OK' if v else 'MISMATCH'}" for k, v in real.items()))
    if not all(real.values()):
        fault("a pinned real file is missing or differs")
    prov = load_prov(ROOT)  # the registered table passes its own schema; Pangea is decided by documentation
    if set(prov["files"]) != set(SFT) or not doc_decided(prov, "pangeains") or \
            any(doc_decided(prov, f) for f in SFT if f != "pangeains"):
        fault("registered provenance: unexpected documentation-decided set")
    print("registered provenance: schema ok;", len(doc_decided(prov, "pangeains")),
          "undetermined image-bearing Pangea components -> pangeains decided by documentation, not scanned")
    print(f"selftest ok  {LABEL}  gates.py {sha_file(Path(__file__))}")


# ------------------------------------------------------------------------------------------------ cli
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    a = sp.add_parser("gate-a")
    a.add_argument("phase", choices=("step0", "pin", "join", "verify"))
    a.add_argument("--info-sha")
    a.add_argument("--oi-sha")
    c = sp.add_parser("gate-c2")
    c.add_argument("phase", choices=("scan", "join"))
    c.add_argument("--file", choices=sorted(SFT))
    c.add_argument("--prefix-map", help="post-census map (one-judge read); may only add prefixes")
    x = ap.parse_args()
    if x.cmd == "selftest":
        return selftest()
    if str(SEALED.resolve()).startswith("/mnt/"):
        fault(f"{SEALED} must sit on the WSL ext4 home")
    if x.cmd == "gate-a" and x.phase == "step0":  # N4: real pinned files, after GO, before any download
        s0 = step0(ROOT)
        print(json.dumps({k: len(v) for k, v in s0.items()}, sort_keys=True))
    elif x.cmd == "gate-a" and x.phase == "pin":  # N5: step-3 check, then the shas for the LOG line
        print(json.dumps(gate_a_pin(GA), indent=1, sort_keys=True))
    elif x.cmd == "gate-a" and x.phase == "join":
        if not (x.info_sha and x.oi_sha):
            ap.error("join needs --info-sha and --oi-sha (the shas logged at download)")
        print(json.dumps(gate_a_join(ROOT, GA, x.info_sha, x.oi_sha), indent=1, sort_keys=True))
    elif x.cmd == "gate-a":
        print("ga_remaining_ids.txt reproduced", gate_a_verify(ROOT, GA))
    elif x.phase == "scan":
        GC2.mkdir(mode=0o700, parents=True, exist_ok=True)
        r = gate_c2_scan(x.file, sys.stdin.buffer, GC2, load_prov(ROOT))
        print(json.dumps({k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in r.items()}))
    else:
        r = gate_c2_join(ROOT, GC2, GA, Path(x.prefix_map) if x.prefix_map else None)
        print(json.dumps({m: v["status"] for m, v in r["models"].items()}, indent=1),
              "flickr image exclusions:", len(r["flickr_image_exclusions"]))


if __name__ == "__main__":
    main()
