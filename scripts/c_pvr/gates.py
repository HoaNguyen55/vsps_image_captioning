#!/usr/bin/env python3
"""C-PVR-T1 gates G-A and G-C2 (Paper C, PVR). Prereg manuscript/prereg/2026-11-02_c_pvr_tier1/PREREG_DRAFT_v1_2.md
(8282874) as amended by AMENDMENT_CC222 v1.1 (entry point, inputs, custody, G-C2 rule). Stdlib only, no repo import,
no network code: every download is a curl line of the amendment; this file reads local files and stdin only.

    python3 -I scripts/c_pvr/gates.py selftest                 CPU: synthetic fixtures, sockets raise; sha checks of the
                                                               pinned real files; schema of the registered provenance
    python3 -I scripts/c_pvr/gates.py gate-a step0             real pinned id files, after GO, before any download
    python3 -I scripts/c_pvr/gates.py gate-a pin               step-3 size/first-byte/md5/header check, prints shas
    python3 -I scripts/c_pvr/gates.py gate-a schema --info-sha H   CC-227: key names/types/lengths only, writes nothing
    python3 -I scripts/c_pvr/gates.py gate-a join --info-sha H --oi-sha H   ids only; counts first, ids last, once
    python3 -I scripts/c_pvr/gates.py gate-a verify            offline rerun; must reproduce ga_remaining_ids.txt
    curl ... | python3 -I scripts/c_pvr/gates.py gate-c2 scan --file KEY    one pinned SFT list from stdin
    python3 -I scripts/c_pvr/gates.py gate-c2 join [--prefix-map P]          verify, then G_C2_record.json

Label on every output: TIER 1 / DEV-EXPLORE (C-PVR-T1). No caption, label, question or answer field is accessed,
printed or written: NoCaps-test image info is checked for its key schema and only ids are taken; the OI test list is an
image-metadata file (no label column); SFT lists are scanned for image references, 16-hex tokens, Flickr photo ids,
key-name counts and three dataset names only.

PINS-B (B) adds G-B, the one test-gold read, and its loader parity (CC-239 design GO; PINS_B_DRAFT_v1_1.md):
    python3 -I -B scripts/c_pvr/gates.py parity --gates-sha H                 prereg §3.3 parity on A's spent XM3600 rows
    python3 -I -B scripts/c_pvr/gates.py gate-b --gates-sha H --pause-tag T   G-B once (prereg §8.2, §9.3-9.6)
gate-b reads the OIV7 val/test human-label streams, filtered in memory to ga_remaining_ids.txt; that is the one
exception to the no-label rule above. Stated override of the 'no network code' sentence (Q-B4): gate-b starts
/usr/bin/curl as a subprocess with the pinned argv CURL_HEAD / CURL_STREAM, so the code closure is this file plus that
binary (W8). No other subcommand has a network path. The selftest and gates_mutants.py run only under
`unshare -rnm` with a private tmpfs on /dev/shm and HOME on ext4 scratch (W3).
"""
from __future__ import annotations

import argparse
import base64
import csv
import fcntl
import hashlib
import io
import json
import os
import re
import shutil
import signal
import socket
import stat
import subprocess
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime
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
INFO_TOP_STR = {"type"}  # CC-227: COCO caption toolkit key (tylin/coco-caption loadRes copies it); short str only
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
    extra = set(d) - INFO_TOP if isinstance(d, dict) else None
    if (extra is None or "images" not in d or not extra <= INFO_TOP_STR
            or any(not isinstance(d[k], str) or len(d[k]) > 64 for k in extra)):
        fault(f"{p}: top-level keys {sorted(d) if isinstance(d, dict) else type(d)} outside {sorted(INFO_TOP)}"
              f" + str-valued {sorted(INFO_TOP_STR)}")
    ims = d["images"]
    if any(not set(im) <= INFO_IMG for im in ims):
        fault(f"{p}: an image record has a key outside {sorted(INFO_IMG)}")
    oid = [im["open_images_id"] for im in ims]
    n = N["test"]
    if (len(ims) != n or len(set(oid)) != n or len({im["id"] for im in ims}) != n
            or any(not HEX16.fullmatch(o) or im["file_name"] != o + ".jpg" for o, im in zip(oid, ims))):
        fault(f"{p}: not {n} unique 16-hex open_images_id with file_name = id + .jpg")
    return oid


def info_schema(p: Path, info_sha: str) -> dict:
    """CC-227 dry check: key names, value type names and lengths only. No value is printed; nothing is written."""
    b = refuse(p).read_bytes()
    if sha_bytes(b) != info_sha:
        fault(f"{p.name}: sha256 differs from the one logged at download ({info_sha[:8]})")
    d = json.loads(b)

    def shape(v):
        return {"type": type(v).__name__, **({"len": len(v)} if isinstance(v, (str, list, dict)) else {})}

    ims = d.get("images") if isinstance(d, dict) else None
    recs = ims if isinstance(ims, list) and all(isinstance(im, dict) for im in ims) else []
    return {"top": {k: shape(v) for k, v in d.items()} if isinstance(d, dict) else {"<root>": shape(d)},
            "image_keys": sorted({k for im in recs for k in im}),
            "n_images": len(ims) if isinstance(ims, list) else None}


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


# ------------------------------------------------------------------------------------------------ G-B (PINS-B)
T0 = time.time()  # W6: process start (module import precedes argv parsing); the pause line must be stamped before it
PINS_B = {  # PINS-B §1.2 (prereg §2.3, §3.3, §9.6); gate-b and parity FAULT on any mismatch
    "map": ("data/xm3600/vi_oiv7_map.json", "27f2b1ca3f2bf47d43c8f00e8409472c8d571eb720d47b8107a1c77bd208d16a"),
    "desc": ("data/datasets/xm3600/oiv7/oidv7-class-descriptions.csv",
             "84a4373a0efb7fd6d93fe19b0e7ceb6c1b855c233d13b9b78a9a33655c9fdce3"),
    "md5_val": ("data/datasets/xm3600/oiv7/full-val.md5",
                "5770ed7c94cb6ae9ebd5e8746a95382d6475d0887c87ad4c05afa664ec840d8a"),
    "md5_test": ("data/datasets/xm3600/oiv7/full-test.md5",
                 "2eebd937f99edec5267abd697f1b839d9846fc4ba4fd070d833b048bbc9ace54"),
    "md5_train": ("data/datasets/xm3600/oiv7/full-train.md5",
                  "e1af682181bcbbdfea6c76fb083e90481aa834efa1138efde869c1cc21e40de0"),
    "fetch": ("data/datasets/xm3600/oiv7/fetch.sh", "75c22a0814037cee2bf328101aefdb3852a499c3e65fcdb1707e8fa2992f6c07"),
    "manifest": ("data/xm3600/manifest.json", "263015f9dc46ebe2cea80055e04ed39baf80a356f4e027cd3756464279135bef"),
    "ga_rem": (f"{PDIR}/ga_remaining_ids.txt", "3feccabc6da972396482faf0d2ae81296277e665ce094368019a3913c2fcbd24"),
}
A12 = {  # parity inputs (A's spent XM3600 dev gold, A12); opened only through allow_read, never through sha_file
    "train": ("data/datasets/xm3600/oiv7/xm3600-train-annotations-human-imagelabels.csv",
              "779afb19a4c3c25f100f871e92bbe8e937d6fa7f20ea75c4d0f7a23953056e76"),
    "val": ("data/datasets/xm3600/oiv7/xm3600-val-annotations-human-imagelabels.csv",
            "b7967190d6b05d6c97d38fe238046091905aabfe5bd268df4efe1c2a9a3db9d0"),
    "test": ("data/datasets/xm3600/oiv7/xm3600-test-annotations-human-imagelabels.csv",
             "06567dd986bf571db62d69af5abec0973a37f2552b1e00c50147cf490f72c19a"),
}
WANT_B = {  # manifest 263015f9 coverage (prereg §3.3 targets; CC-239 Ruling 4 (c)-(d))
    "mapped_classes": 69, "mapped_classes_with_a_verified_label_on_xm3600": 68,
    "images_with_any_verified_label": 2584, "images_with_a_verified_label_on_a_mapped_class": 2119,
    "image_class_pairs": {"present": 4453, "absent": 8276},
    "verified_labels": {"positive": 19052, "negative": 10700, "conflicting": 0,
                        "rows_per_oi_split": {"train": 1222, "val": 6623, "test": 21907}}}
GB_REMAINING = 10496  # ga_counts.json f7036396 "remaining"; the coverage denominator
OI_SPLITS = ("train", "val", "test")
LABEL_HEADER = ["ImageID", "Source", "LabelName", "Confidence"]
OI_LABEL_URL = "https://storage.googleapis.com/openimages/v7/oidv7-{s}-annotations-human-imagelabels.csv"
CURL_STREAM = ("/usr/bin/curl", "-q", "-sS", "--fail", "-L", "--proto", "=https", "--proto-redir", "=https",
               "--max-redirs", "3", "-A", "vsps-research")  # Q-B4: + URL; body to stdout; -q first (no curlrc)
CURL_HEAD = ("/usr/bin/curl", "-q", "-sS", "-I", "--fail", "--proto", "=https")  # Q-B12: + URL; headers only
CURL_ENV = {"PATH": "/usr/bin:/bin"}  # no *_proxy, no HOME
SHM_GB, LOCK_GB = Path("/dev/shm/c_pvr_gb"), Path("/dev/shm/c_pvr_gb.lock")
GB_LOG = ".session_backup/2026-10-13/decisions/LOG.md"
STAMP = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d(?::\d\d)?)Z")
GB_SIGS = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)  # W10 (e): SIGHUP with SIGTERM/SIGINT
GB_RC = {"tenancy": 40, "head": 41, "md5": 42, "curl": 43, "header": 44, "val_row": 45, "label_row": 46,
         "integrity": 47, "write": 48, "signal": 49, "internal": 50}  # Q-B11: rc after the start marker; no text
GB_KEYS = {"label", "utc", "gates_sha256", "ga_remaining_sha256", "n_e_gb", "present_pairs", "absent_pairs",
           "coverage_share", "remaining", "streams", "inputs", "sealed_sha256"}  # prereg §9.3: nothing else
GB_STREAM_KEYS = {"sha256", "md5", "bucket_md5", "record_md5", "filtered_sha256", "bytes"}
FLICKR_W3 = ("513d6796c322ced5", "821f75f1f4061c79", "bfdd3df591001b36", "c32ddd2ae971e5b5")  # G_C2_record 767998f8


class GBAbort(Exception):
    """W2: carries a fixed code from GB_RC only, never a row or field value."""

    def __init__(self, code: str):
        super().__init__(code if code in GB_RC else "internal")
        self.code = self.args[0]


def n_e_power(n_e_gb: int, w25_flagged: int, lost: int) -> int:
    """prereg §5.6 plus the Q-B7 term (CC-239): all 4 Flickr-excluded ids leave n_e_power (conservative; the exact
    0-4 drop is computed only at the tier-3 open). Tier-2 arithmetic: G-B itself prints no fifth number."""
    return n_e_gb - w25_flagged - lost - len(FLICKR_W3)


def allow_read(p, allowed: dict) -> bytes:
    """Q-B8 scoped allow: the resolved path must be a key of `allowed` (the 3 pinned A12 files for parity, or the 2
    tmpfs files gate-b wrote) and the bytes must hash to its value. BARRED, refuse() and sha_file() are unchanged."""
    rp = Path(p).resolve()
    if rp not in allowed:
        raise GBAbort("integrity")
    b = rp.read_bytes()
    if sha_bytes(b) != allowed[rp]:
        raise GBAbort("integrity")
    return b


def load_labels(ids, csv_paths, allowed: dict):
    """prereg §3.3: stdlib port of xm3600_oiv7.py cmd_build l.106-119 (9a79403f). pos = MIDs seen only with
    Confidence 1, neg = only with 0, mixed = neither (counted as conflicting). Returns (labels, conflicts, rows per
    file). W2: a bad header, a foreign id or a bad field raises GBAbort with a code only."""
    seen, rows = {}, []
    for p in csv_paths:
        n = 0
        try:
            rd = csv.DictReader(io.StringIO(allow_read(p, allowed).decode("utf-8"), newline=""))
            if rd.fieldnames != LABEL_HEADER:
                raise GBAbort("header")
            for r in rd:
                img, mid, conf = r["ImageID"], r["LabelName"], int(float(r["Confidence"]))
                if img not in ids:
                    raise GBAbort("label_row")
                seen.setdefault(img, {}).setdefault(mid, set()).add(conf)
                n += 1
        except (csv.Error, ValueError, TypeError, KeyError):
            raise GBAbort("label_row") from None
        rows.append(n)
    labels, conflicts = {}, 0
    for img in sorted(seen):
        conflicts += sum(len(v) > 1 for v in seen[img].values())
        labels[img] = {"pos": sorted(m for m, v in seen[img].items() if v == {1}),
                       "neg": sorted(m for m, v in seen[img].items() if v == {0})}
    return labels, conflicts, rows


def resolve_map(desc_csv: Path, map_json: Path) -> dict:
    """xm3600_oiv7.py resolve_map l.60-75: display names to MIDs; a name not present exactly once FAULTs."""
    mids: dict[str, list] = {}
    with open(refuse(desc_csv), encoding="utf-8") as f:
        for mid, name in csv.reader(f):
            mids.setdefault(name, []).append(mid)
    raw = json.loads(refuse(map_json).read_text(encoding="utf-8"))
    out = {}
    for c, v in raw.items():
        if c.startswith("_"):
            continue
        bad = [n for n in v["pos"] + v["neg"] if len(mids.get(n, [])) != 1]
        if bad:
            fault(f"{Path(map_json).name}: {c!r} names {bad}, not exactly one OIV7 class each")
        out[c] = {k: {mids[n][0] for n in v[k]} for k in ("pos", "neg")}
    return out


def status(c_map: dict, pos: set, neg: set) -> str:
    if c_map["pos"] & pos:
        return "present"
    return "absent" if c_map["neg"] & neg else "unknown"


def statuses(vmap: dict, labels: dict) -> dict:
    """xm3600_oiv7.py l.84-93: {image: {class: present|absent}}; unknown omitted, images with none omitted."""
    out = {}
    for img, lab in labels.items():
        pos, neg = set(lab["pos"]), set(lab["neg"])
        s = {c: st for c, m in vmap.items() if (st := status(m, pos, neg)) != "unknown"}
        if s:
            out[img] = s
    return out


def coverage_b(vmap: dict, labels: dict, conflicts: int, rows: list) -> tuple[dict, dict]:
    """The manifest `coverage` aggregates of cmd_build l.157-166, and pairs_per_class (compared in memory only)."""
    st = statuses(vmap, labels)
    per_class = Counter(c for s in st.values() for c in s)
    cov = {"mapped_classes": len(vmap), "mapped_classes_with_a_verified_label_on_xm3600": len(per_class),
           "images_with_any_verified_label": len(labels), "images_with_a_verified_label_on_a_mapped_class": len(st),
           "image_class_pairs": {"present": sum(v == "present" for s in st.values() for v in s.values()),
                                 "absent": sum(v == "absent" for s in st.values() for v in s.values())},
           "verified_labels": {"positive": sum(len(v["pos"]) for v in labels.values()),
                               "negative": sum(len(v["neg"]) for v in labels.values()), "conflicting": conflicts,
                               "rows_per_oi_split": dict(zip(OI_SPLITS, rows))}}
    ppc = {c: {"present": sum(s.get(c) == "present" for s in st.values()),
               "absent": sum(s.get(c) == "absent" for s in st.values())} for c in per_class}
    return cov, ppc


def parity(root: Path, pins: dict = PINS, pins_b: dict = PINS_B, a12: dict = A12, want: dict = WANT_B) -> dict:
    """prereg §3.3 / CC-239 Ruling 4: the loader on the 3 A12 files and the 3,600 XM3600 ids must reproduce manifest
    263015f9 exactly, compared with the registered constants AND with the sha-pinned manifest. Aggregates only."""
    for k in ("map", "desc", "manifest"):
        pinned(root, k, pins_b)
    ids = set(pinned(root, "xm_src", pins).read_text().split())
    allowed = {(root / p).resolve(): s for p, s in a12.values()}
    labels, conflicts, rows = load_labels(ids, [root / a12[s][0] for s in OI_SPLITS], allowed)
    vmap = resolve_map(root / pins_b["desc"][0], root / pins_b["map"][0])
    cov, ppc = coverage_b(vmap, labels, conflicts, rows)
    man = json.loads((root / pins_b["manifest"][0]).read_text(encoding="utf-8"))["coverage"]
    bad = sorted(k for k in want if cov[k] != want[k] or cov[k] != man.get(k))
    if bad or ppc != man.get("pairs_per_class"):
        fault(f"parity: {bad or ['pairs_per_class']} differ from the manifest / registered targets; G-B does not run")
    return {**cov, "pairs_per_class_equal": len(ppc)}


def bucket_md5(head: bytes) -> tuple[str, int]:
    """G24: the x-goog-hash md5 (base64; one header per hash or comma-joined) as hex, and Content-Length. Exactly one
    of each, else HEAD FAULT (a composite object carries no md5)."""
    md5s, lens = [], []
    for ln in head.decode("latin-1").split("\n"):
        k, _, v = ln.partition(":")
        if k.strip().lower() == "x-goog-hash":
            md5s += [x.strip()[4:] for x in v.split(",") if x.strip().startswith("md5=")]
        elif k.strip().lower() == "content-length":
            lens.append(v.strip())
    if len(md5s) != 1 or len(lens) != 1 or not lens[0].isdigit():
        raise GBAbort("head")
    try:
        raw = base64.b64decode(md5s[0], validate=True)
    except ValueError:
        raise GBAbort("head") from None
    if len(raw) != 16:
        raise GBAbort("head")
    return raw.hex(), int(lens[0])


def record_md5(p: Path) -> str:
    """full-{val,test}.md5: one line '<md5 hex>  -' (curl | md5sum)."""
    tok = p.read_text().split()
    if len(tok) != 2 or tok[1] != "-" or not re.fullmatch(r"[0-9a-f]{32}", tok[0]):
        fault(f"{p.name}: not one '<md5>  -' line")
    return tok[0]


def gb_filter(read, keep: set, out, chunk: int = 1 << 16) -> dict:
    """W5, one pass: sha256 and md5 over the raw bytes; keeps record 1 (the header) and each record whose bytes
    before the first comma are in `keep` (fetch.sh awk -F, $1). Records split on newline across any read boundary;
    a kept record is written with a newline (awk ORS), so a last record without one gains it and a CR stays."""
    h, m, fh = hashlib.sha256(), hashlib.md5(), hashlib.sha256()
    cnt = {"bytes": 0, "kept": 0, "first": True}
    buf = b""

    def emit(rec: bytes) -> None:
        if cnt["first"]:
            cnt["first"] = False
            if rec.rstrip(b"\r").decode("latin-1") != ",".join(LABEL_HEADER):
                raise GBAbort("header")
        elif rec.split(b",", 1)[0] in keep:
            cnt["kept"] += 1
        else:
            return
        out.write(rec + b"\n")
        fh.update(rec + b"\n")

    while True:
        b = read(chunk)
        if not b:
            break
        h.update(b)
        m.update(b)
        cnt["bytes"] += len(b)
        *recs, buf = (buf + b).split(b"\n")
        for r in recs:
            emit(r)
    if buf:
        emit(buf)
    if cnt["first"]:
        raise GBAbort("header")
    return {"sha256": h.hexdigest(), "md5": m.hexdigest(), "bytes": cnt["bytes"], "kept": cnt["kept"],
            "filtered_sha256": fh.hexdigest()}


def write_new(p: Path, data: bytes, mode: int, check_mode: bool = False) -> str:
    """W4: tmp -> fsync(file) -> chmod -> os.link (atomic; fails if p exists) -> fsync(dir) -> unlink tmp, then
    re-read and compare the sha (and stat the mode where chmod is reliable, i.e. the ext4 sealed dir)."""
    tmp = p.with_name(f".{p.name}.{os.getpid()}.tmp")
    try:
        with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, mode)
        try:
            os.link(tmp, p)
            dfd = os.open(p.parent, os.O_RDONLY)
            try:
                os.fsync(dfd)
            finally:
                os.close(dfd)
        finally:
            os.unlink(tmp)
        if sha_bytes(p.read_bytes()) != sha_bytes(data) or (check_mode and p.stat().st_mode & 0o777 != mode):
            raise GBAbort("write")
    except OSError:
        raise GBAbort("write") from None
    return sha_bytes(data)


def access_log_sync(sealed: Path, action: str, path, sha: str) -> None:
    """W4: an ACCESS_LOG.tsv row (same format as access_log, which stays unchanged) followed by fsync."""
    with open(sealed / "ACCESS_LOG.tsv", "a") as f:
        f.write(f"{utc()}\tgates.py\t{action}\t{path}\t{sha}\n")
        f.flush()
        os.fsync(f.fileno())


def pause_ok(log: Path, tag: str, t0: float) -> str | None:
    """W6 (prereg §8.2 step 1): the OPS tag, as a whole token, is in exactly one LOG line; that line starts with a
    date -u stamp earlier than t0 and names G-B and the pause. Returns the reason it fails, or None."""
    if not re.fullmatch(r"OPS-[0-9A-Za-z][0-9A-Za-z-]*", tag):
        return "--pause-tag is not an OPS-... token"
    rx = re.compile(r"(?<![\w-])" + re.escape(tag) + r"(?![\w-])")
    hits = [x for x in log.read_text(encoding="utf-8").splitlines() if rx.search(x)]
    if len(hits) != 1:
        return f"the pause tag is in {len(hits)} LOG lines, not exactly one"
    m = STAMP.match(hits[0])
    if not m or datetime.fromisoformat(m.group(1) + "+00:00").timestamp() >= t0:
        return "the pause line has no date -u stamp earlier than this process"
    if "G-B" not in hits[0] or not re.search(r"(?i)\bpause", hits[0]):
        return "the pause line does not name G-B and the pause"
    return None


def foreign_jobs(proc: Path, me: int) -> int:
    """W6: live processes with a *_job.sh argument, from <proc>/<pid>/cmdline; this process excluded by pid."""
    n = 0
    for d in proc.iterdir():
        if not d.name.isdigit() or int(d.name) == me:
            continue
        try:
            argv = (d / "cmdline").read_bytes().split(b"\0")
        except OSError:
            continue  # exited during the scan
        n += any(a.rstrip().endswith(b"_job.sh") for a in argv)
    return n


def tenancy(env: dict, tag: str, lockfd: int | None = None) -> str | None:
    """prereg §8.2 steps 1-4, re-checked before and after each stream and before the read (W6)."""
    why = pause_ok(env["log"], tag, env["t0"])
    if why:
        return why
    if foreign_jobs(env["proc"], os.getpid()):
        return "a foreign *_job.sh process is live"
    if not env["backup"].is_file() or b"/dev/shm" in env["backup"].read_bytes():
        return "gpu_backup.sh is missing or names /dev/shm"
    if lockfd is not None:
        try:
            a, b, s = os.fstat(lockfd), os.lstat(env["lock"]), os.lstat(env["shm"])
        except OSError:
            return "the lock file or the tmpfs dir is gone"
        if (a.st_dev, a.st_ino) != (b.st_dev, b.st_ino):
            return "the lock file was replaced"
        if not stat.S_ISDIR(s.st_mode) or s.st_mode & 0o777 != 0o700 or s.st_uid != os.getuid():
            return "the tmpfs dir is not a mode-0700 dir of this uid"
    return None


def gb_refuse(env: dict) -> None:
    """One-run rule (prereg §9.3, §9.6; W1): refuses on gb_counts.json, the sealed file, the start marker, a
    'gate-b start' ACCESS_LOG row or the tmpfs dir. Removing a marker is a re-download: own ruling at 92."""
    sealed = env["sealed"]
    if str(sealed.resolve()).startswith("/mnt/") or not sealed.is_dir() or sealed.stat().st_mode & 0o077:
        fault(f"{sealed} must be a mode-0700 dir on the WSL ext4 home")
    for p in (env["out"] / "gb_counts.json", sealed / "gb_intermediate.json", sealed / "gb_start", env["shm"]):
        if os.path.lexists(p):
            raise SystemExit(f"REFUSED: {p} exists; G-B runs once (a re-run is a re-download, §9.6)")
    log = sealed / "ACCESS_LOG.tsv"
    if log.exists() and any(x.split("\t")[2:3] == ["gate-b start"] for x in log.read_text().splitlines()):
        raise SystemExit("REFUSED: ACCESS_LOG.tsv holds a 'gate-b start' row; G-B runs once (§9.6)")


def gb_integrity(env: dict, gates_sha: str, pins_b: dict) -> None:
    """Q-B5: --gates-sha equals sha256 of this file and the single SHA256SUMS gates.py line; every SUMS line and every
    PINS-B pin verifies."""
    root = env["root"]
    if sha_file(Path(__file__)) != gates_sha:
        fault("--gates-sha differs from sha256 of this gates.py (Q-B5)")
    lines = (root / "scripts/c_pvr/SHA256SUMS").read_text().splitlines()
    if not all(re.fullmatch(r"[0-9a-f]{64}  \S+", x) for x in lines):
        fault("SHA256SUMS has a malformed line")
    own = [x.split()[0] for x in lines if x.split()[1] == "scripts/c_pvr/gates.py"]
    if own != [gates_sha]:
        fault("SHA256SUMS has no single gates.py line equal to --gates-sha")
    bad = [x.split()[1] for x in lines if sha_file(root / x.split()[1]) != x.split()[0]]
    if bad:
        fault(f"SHA256SUMS: {len(bad)} line(s) do not verify")
    for k in pins_b:
        pinned(root, k, pins_b)


def sealed_bytes(st: dict) -> bytes:
    """prereg §9.4: sorted keys, fixed separators, sorted class lists; ids with >= 1 known mapped class only."""
    d = {i: {"absent": sorted(c for c, v in s.items() if v == "absent"),
             "present": sorted(c for c, v in s.items() if v == "present")} for i, s in st.items()}
    return (json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def gb_counts_ok(rec: dict) -> None:
    """prereg §9.3 / G10: exactly the registered keys; pairs_per_class, labels, per-image lists and row counts are
    barred by name because no other key may be emitted."""
    if set(rec) != GB_KEYS or set(rec["streams"]) != {"val", "test"} or any(
            set(v) != GB_STREAM_KEYS for v in rec["streams"].values()) or not all(
            re.fullmatch(r"[0-9a-f]{64}", v) for v in rec["inputs"].values()):
        raise GBAbort("internal")


def _gb_signal(signum, frame):
    raise GBAbort("signal")


def _gb_cleanup(env: dict, procs: list, written: dict, sealed: Path) -> None:
    """Kills a live curl, then unlinks every tmpfs file (an 'gate-b unlink' row with its sha each) and the dir."""
    for p in procs:
        if p.poll() is None:
            p.kill()
            p.wait()
    if os.path.lexists(env["shm"]):
        for f in sorted(env["shm"].iterdir()):
            sha = written.get(f) or sha_bytes(f.read_bytes())
            f.unlink()
            access_log_sync(sealed, "gate-b unlink", f, sha)
        env["shm"].rmdir()


def curl_run(argv):
    """Q-B4: the only process gates.py starts. stdin and stderr closed, PATH-only env, stdout piped."""
    return subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            env=CURL_ENV)


def gate_b(env: dict, gates_sha: str, tag: str, runner, exit_fn, pins: dict = PINS, pins_b: dict = PINS_B,
           a12: dict = A12, want: dict = WANT_B, remaining_n: int = GB_REMAINING, strict: bool = True) -> dict:
    """G-B once (prereg §9.3-9.6, §8.2; PINS-B §2.2). Before the start marker every check may FAULT with text (no
    gold has been requested). From the marker on, any failure prints nothing: the tmpfs is unlinked, an ACCESS_LOG
    row 'gate-b abort <rc>' is written and exit_fn(rc) is called with the GB_RC code (Q-B11, W1, W2)."""
    root, sealed = env["root"], env["sealed"]
    gb_refuse(env)
    gb_integrity(env, gates_sha, pins_b)
    if gate_a_verify(root, env["ga"], pins, strict=strict) != pins_b["ga_rem"][1]:  # N11, before any label byte
        fault("gate-a verify does not give the pinned ga_remaining_ids.txt; G-B does not run")
    parity(root, pins, pins_b, a12, want)  # P2 in code (W11)
    vmap = resolve_map(root / pins_b["desc"][0], root / pins_b["map"][0])
    rem = pinned(root, "ga_rem", pins_b).read_text().split()
    if len(rem) != remaining_n or len(set(rem)) != remaining_n:
        fault(f"ga_remaining_ids.txt is not {remaining_n} unique ids")
    rec_md5 = {s: record_md5(pinned(root, f"md5_{s}", pins_b)) for s in ("val", "test")}
    curl_sha = sha_file(Path(CURL_STREAM[0]))
    why = tenancy(env, tag)
    if why:
        fault(f"tenancy: {why}; G-B does not start")
    lockfd = os.open(env["lock"], os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        os.close(lockfd)
        fault("tenancy: the G-B lock is held; G-B does not start")
    marker = sealed / "gb_start"
    write_new(marker, f"{utc()}\t{gates_sha}\n".encode(), 0o400, check_mode=True)  # W1, before the first byte
    access_log_sync(sealed, "gate-b start", marker, gates_sha)
    old = {s: signal.getsignal(s) for s in GB_SIGS}
    keep = {i.encode() for i in rem}
    procs, written, code, rec = [], {}, None, {}
    try:
        for s in GB_SIGS:
            signal.signal(s, _gb_signal)
        env["shm"].mkdir(mode=0o700)
        os.chmod(env["shm"], 0o700)
        streams = {}
        for s in ("val", "test"):
            if tenancy(env, tag, lockfd):
                raise GBAbort("tenancy")
            url = OI_LABEL_URL.format(s=s)
            hp = runner(CURL_HEAD + (url,))
            procs.append(hp)
            head = hp.stdout.read()
            if hp.wait() != 0:
                raise GBAbort("head")
            bmd5, clen = bucket_md5(head)
            if bmd5 != rec_md5[s]:
                raise GBAbort("md5")
            fp = env["shm"] / f"filtered-{s}.csv"
            with open(os.open(fp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as fo:
                sp = runner(CURL_STREAM + (url,))
                procs.append(sp)
                r = gb_filter(sp.stdout.read, keep, fo)
            if sp.wait() != 0:
                raise GBAbort("curl")
            written[fp] = r["filtered_sha256"]
            if r["md5"] != bmd5 or r["md5"] != rec_md5[s]:
                raise GBAbort("md5")
            if r["bytes"] != clen:
                raise GBAbort("integrity")
            if tenancy(env, tag, lockfd):
                raise GBAbort("tenancy")
            if s == "val" and r["kept"]:
                raise GBAbort("val_row")  # Q-B6: G-A found in_oiv7_val 0
            streams[s] = {"sha256": r["sha256"], "md5": r["md5"], "bucket_md5": bmd5, "record_md5": rec_md5[s],
                          "filtered_sha256": r["filtered_sha256"], "bytes": r["bytes"]}
        if tenancy(env, tag, lockfd):
            raise GBAbort("tenancy")
        labels, _, _ = load_labels(set(rem), list(written), {f.resolve(): h for f, h in written.items()})  # one read
        st = statuses(vmap, labels)
        sealed_p = sealed / "gb_intermediate.json"
        sealed_sha = write_new(sealed_p, sealed_bytes(st), 0o400, check_mode=True)
        access_log_sync(sealed, "gate-b write", sealed_p, sealed_sha)
        n_e = len(st)
        rec = {"label": LABEL, "utc": utc(), "gates_sha256": gates_sha, "ga_remaining_sha256": pins_b["ga_rem"][1],
               "n_e_gb": n_e, "present_pairs": sum(v == "present" for x in st.values() for v in x.values()),
               "absent_pairs": sum(v == "absent" for x in st.values() for v in x.values()),
               "coverage_share": n_e / len(rem), "remaining": len(rem), "streams": streams,
               "inputs": {**dict(pins_b.values()), **dict(a12.values()), CURL_STREAM[0]: curl_sha},
               "sealed_sha256": sealed_sha}
        gb_counts_ok(rec)
        _gb_cleanup(env, procs, written, sealed)
        write_new(env["out"] / "gb_counts.json", jdump(rec), 0o444)  # last: the commit marker
    except BaseException as e:  # noqa: B036 - W2: every failure after the marker is silent
        code = GB_RC[e.code] if isinstance(e, GBAbort) else GB_RC["internal"]
    finally:
        for s in GB_SIGS:
            signal.signal(s, signal.SIG_IGN)
        try:
            _gb_cleanup(env, procs, written, sealed)
        except BaseException:  # noqa: B036
            code = code or GB_RC["internal"]
        if code is not None:
            try:
                access_log_sync(sealed, f"gate-b abort {code}", "-", gates_sha)
            except BaseException:  # noqa: B036
                pass
        for s in GB_SIGS:
            signal.signal(s, old[s])
        os.close(lockfd)
    if code is not None:
        exit_fn(code)
    return rec


def main_b(x) -> None:
    if x.cmd == "parity":
        if sha_file(Path(__file__)) != x.gates_sha:
            fault("--gates-sha differs from sha256 of this gates.py (Q-B5)")
        try:
            c = parity(ROOT)
        except GBAbort as e:
            fault(f"parity: {e.code}")
        a12s = " / ".join(f"xm3600-{s} {A12[s][1][:8]}" for s in OI_SPLITS)
        pairs, vl = c["image_class_pairs"], c["verified_labels"]
        rows = vl["rows_per_oi_split"]
        print(f"parity ok  {LABEL}  gates.py {x.gates_sha}")
        print(f"re-hash ok: {a12s}; class descriptions {PINS_B['desc'][1][:8]}; map {PINS_B['map'][1][:8]};"
              f" manifest {PINS_B['manifest'][1][:8]}")
        print(f"registered targets = constants = manifest: mapped_classes {c['mapped_classes']};"
              f" images_with_a_verified_label_on_a_mapped_class {c['images_with_a_verified_label_on_a_mapped_class']};"
              f" present {pairs['present']} / absent {pairs['absent']};"
              f" mapped_classes_with_a_verified_label_on_xm3600 {c['mapped_classes_with_a_verified_label_on_xm3600']}")
        print(f"reader checks = constants = manifest: images_with_any_verified_label"
              f" {c['images_with_any_verified_label']}; verified_labels positive {vl['positive']} / negative"
              f" {vl['negative']} / conflicting {vl['conflicting']}; rows_per_oi_split train {rows['train']} /"
              f" val {rows['val']} / test {rows['test']}")
        print(f"pairs_per_class {c['pairs_per_class_equal']}/{c['mapped_classes_with_a_verified_label_on_xm3600']}"
              " equal")
        return
    SEALED.mkdir(mode=0o700, parents=True, exist_ok=True)
    env = {"root": ROOT, "ga": GA, "sealed": SEALED, "out": ROOT / PDIR, "shm": SHM_GB, "lock": LOCK_GB,
           "log": ROOT / GB_LOG, "backup": Path.home() / ".config/vsps/gpu_backup.sh", "proc": Path("/proc"),
           "t0": T0}
    rec = gate_b(env, x.gates_sha, x.pause_tag, curl_run, os._exit)
    print(json.dumps(rec, indent=1, sort_keys=True))


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
    # CC-227: a short str 'type' (COCO caption toolkit) passes; any other shape or extra key FAULTs
    ip.write_text(json.dumps({**info, "type": "captions"}))
    assert info_ids(ip, False) == [im["open_images_id"] for im in info["images"]]
    sch = info_schema(ip, sha_file(ip))
    assert sch == {"top": {"images": {"type": "list", "len": len(info["images"])}, "licenses": {"type": "list", "len": 0},
                           "info": {"type": "dict", "len": 0}, "type": {"type": "str", "len": 8}},
                   "image_keys": sorted(INFO_IMG), "n_images": len(info["images"])}
    assert "captions" not in json.dumps(sch), "schema prints no value"
    _must("sha256 differs", info_schema, ip, "0" * 64)
    ip.write_text(json.dumps({**info, "type": "x" * 64}))  # boundary: 64 characters pass
    assert len(info_ids(ip, False)) == len(info["images"])
    for bad in ({"type": {"x": 1}}, {"type": ["captions"]}, {"type": "x" * 65}, {"type": 1}, {"foo": "x"}):
        ip.write_text(json.dumps({**info, **bad}))
        _must("top-level keys", info_ids, ip, False)
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


# ------------------------------------------------------------------------------------------------ selftest (B)
_SPAWNS: list = []


def _no_spawn(*a, **k):
    """W3 / G19: inside the selftest no process starts; the call is kept for the G15 argv/env check."""
    _SPAWNS.append((a, k))
    raise OSError("selftest: subprocess disabled")


class _GBExit(BaseException):
    def __init__(self, code: int):
        super().__init__(code)
        self.code = code


def _gb_exit(code: int):
    raise _GBExit(code)


class _FakeCurl:
    """curl stand-in fed from fixture bytes; `hook` runs before each read (a signal, a foreign job appearing)."""

    def __init__(self, data: bytes, rc: int = 0, hook=None):
        self.stdout, self._b, self.rc, self.hook = self, io.BytesIO(data), rc, hook
        self.done = self.killed = False

    def read(self, n: int = -1) -> bytes:
        if self.hook:
            self.hook()
        return self._b.read(n)

    def wait(self) -> int:
        self.done = True
        return self.rc

    def poll(self):
        return self.rc if self.done else None

    def kill(self) -> None:
        self.killed = True


def _must_gb(code: str, fn, *a, **k) -> None:
    try:
        fn(*a, **k)
    except GBAbort as e:
        if e.code != code or str(e) != code or e.args != (code,):
            raise AssertionError(f"expected GBAbort {code!r}, got {e.code!r}") from None
        return
    raise AssertionError(f"guard did not fire: expected GBAbort {code!r}")


def _silent(fn, *a, **k) -> tuple:
    """G18: fn runs with fds 1 and 2 on a temp file. Returns (the exit code or None, captured bytes, result)."""
    sys.stdout.flush()
    sys.stderr.flush()
    saved, code, res = [os.dup(1), os.dup(2)], None, None
    with tempfile.TemporaryFile() as t:
        os.dup2(t.fileno(), 1)
        os.dup2(t.fileno(), 2)
        try:
            res = fn(*a, **k)
        except _GBExit as e:
            code = e.code
        finally:
            sys.stdout.flush()
            sys.stderr.flush()
            for fd, s in zip((1, 2), saved):
                os.dup2(s, fd)
                os.close(s)
        t.seek(0)
        return code, t.read(), res


def _ref_filter(data: bytes, keep: set) -> bytes:
    """Independent W5 reference for awk -F, 'FNR==1 || ($1 in ids)': readlines over the whole buffer."""
    lines = [x[:-1] if x.endswith(b"\n") else x for x in io.BytesIO(data).readlines()]
    out = lines[:1] + [x for x in lines[1:] if re.match(rb"[^,]*", x).group() in keep]
    return b"".join(x + b"\n" for x in out)


def _head(body: bytes, joined: bool = False, extra: int = 0) -> bytes:
    b64 = base64.b64encode(hashlib.md5(body).digest()).decode()
    gh = (f"x-goog-hash: crc32c=AAAAAA==, md5={b64}\r\n" if joined else
          f"x-goog-hash: crc32c=AAAAAA==\r\nx-goog-hash: md5={b64}\r\n")
    return f"HTTP/2 200\r\ncontent-type: text/csv\r\n{gh}content-length: {len(body) + extra}\r\n\r\n".encode()


def _b_row(i: str, m: str, c) -> str:
    return f"{i},verification,/m/0{m},{c}"


def _b_world(base: Path, ga: Path, pins: dict, expected: list, rng) -> dict:
    """Synthetic (B) inputs at the PINS-B paths of the fixture repo: class descriptions, a 5-class map (+ _note and
    _skipped), A12 parity rows with a hand-counted manifest, md5 records, SUMS, LOG, gpu_backup and the two streams
    (G-B: 100 known images, 100 present / 20 absent pairs)."""
    root, d = base / "repo", base / "b"
    d.mkdir()
    xm = (root / pins["xm_src"][0]).read_text().split()[:7]
    desc = "LabelName,DisplayName\n" + "".join(
        f"/m/0{c},{n}\n" for c, n in zip("abcdefgh", ("Cat", "Dog", "Car", "Tree", "Person", "Twin", "Twin", "Spare")))
    vmap = {"_note": "n", "_skipped": ["s"], "c1": {"pos": ["Cat"], "neg": ["Cat"]},
            "c2": {"pos": ["Dog"], "neg": ["Dog", "Cat"]}, "c3": {"pos": ["Car"], "neg": ["Car"]},
            "c4": {"pos": ["Tree"], "neg": []}, "c5": {"pos": ["Person"], "neg": ["Person"]}}
    hdr = ",".join(LABEL_HEADER)
    rows12 = {"train": [_b_row(xm[0], "a", 1), _b_row(xm[0], "b", 0), _b_row(xm[1], "b", 1), _b_row(xm[1], "b", 0),
                        _b_row(xm[1], "a", 0), _b_row(xm[6], "b", 1), _b_row(xm[6], "a", 0)],
              "val": [_b_row(xm[2], "c", 1), _b_row(xm[2], "c", "1.0"), _b_row(xm[3], "h", 1)],
              "test": [_b_row(xm[4], "e", 0), _b_row(xm[4], "d", 0), _b_row(xm[5], "a", 1), _b_row(xm[5], "a", 0)]}
    want = {"mapped_classes": 5, "mapped_classes_with_a_verified_label_on_xm3600": 4,
            "images_with_any_verified_label": 7, "images_with_a_verified_label_on_a_mapped_class": 5,
            "image_class_pairs": {"present": 3, "absent": 5},
            "verified_labels": {"positive": 4, "negative": 5, "conflicting": 2,
                                "rows_per_oi_split": {"train": 7, "val": 3, "test": 4}}}  # counted by hand
    ppc = {"c1": {"present": 1, "absent": 2}, "c2": {"present": 1, "absent": 2}, "c3": {"present": 1, "absent": 0},
           "c5": {"present": 0, "absent": 1}}
    rem = expected
    other = sorted({_hexid(rng) for _ in range(300)} - set(rem))
    test = ([_b_row(i, "a", 1) for i in rem[:100]] + [_b_row(i, "b", 0) for i in rem[:20]] +
            [_b_row(i, "d", 0) for i in rem[100:150]] + [_b_row(rem[150], "a", 1), _b_row(rem[150], "a", 0)] +
            [_b_row(i, "a", 1) for i in other[:200]])
    rng.shuffle(test)
    bodies = {"val": ("\n".join([hdr] + [_b_row(i, "a", 1) for i in other[200:250]]) + "\n").encode(),
              "test": ("\n".join([hdr] + test) + "\n").encode()}
    files = {"desc": desc, "map": json.dumps(vmap), "fetch": "set -e\n", "md5_train": f"{'0' * 32}  -\n",
             "manifest": json.dumps({"coverage": {**want, "pairs_per_class": ppc, "lexicon_classes": 9}}),
             **{f"md5_{s}": f"{hashlib.md5(b).hexdigest()}  -\n" for s, b in bodies.items()}}
    pins_b = {}
    for k, (p, _) in PINS_B.items():
        if k in files:
            (root / p).parent.mkdir(parents=True, exist_ok=True)
            (root / p).write_text(files[k])
        pins_b[k] = (p, sha_file(root / p))
    a12 = {}
    for s, (p, _) in A12.items():
        (root / p).write_text("\n".join([hdr] + rows12[s]) + "\n")
        a12[s] = (p, sha_bytes((root / p).read_bytes()))
    gp = root / "scripts/c_pvr/gates.py"
    gp.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__), gp)
    (root / "scripts/c_pvr/SHA256SUMS").write_text(
        f"{sha_file(gp)}  scripts/c_pvr/gates.py\n{pins_b['map'][1]}  {pins_b['map'][0]}\n")
    log, backup = d / "LOG.md", d / "gpu_backup.sh"
    log.write_text("2026-11-01T00:00:00Z OPS-1103c-gbpause: coordinator pause of the B, MT4 and VSPS-J laptop jobs "
                   "for the G-B window.\n2026-11-01T00:01Z OPS-1103c-note: OPS-1103c-gbpause2 is another token.\n")
    backup.write_text("#!/bin/bash\nrsync -a m1:/root/ /backup/m1/\n")
    sealed = {i: {"absent": ["c2"] if k < 20 else [], "present": ["c1"]} for k, i in enumerate(rem[:100])}
    return {"root": root, "dir": d, "ga": ga, "pins": pins, "pins_b": pins_b, "a12": a12, "want": want, "rem": rem,
            "bodies": bodies, "heads": {s: _head(b) for s, b in bodies.items()}, "log": log, "backup": backup,
            "tag": "OPS-1103c-gbpause", "gsha": sha_file(Path(__file__)), "other": other,
            "sealed": (json.dumps(sealed, sort_keys=True, separators=(",", ":")) + "\n").encode()}


def _b_env(w: dict, name: str) -> dict:
    d = w["dir"] / name
    for sub in ("sealed", "out", "shm", f"proc/{os.getpid()}", "proc/1"):
        (d / sub).mkdir(mode=0o700, parents=True)
    (d / "proc" / str(os.getpid()) / "cmdline").write_bytes(b"bash\0scripts/c_pvr/c_pvr_job.sh\0")  # own pid (W6)
    (d / "proc/1/cmdline").write_bytes(b"/sbin/init\0")
    return {"root": w["root"], "ga": w["ga"], "sealed": d / "sealed", "out": d / "out", "shm": d / "shm/c_pvr_gb",
            "lock": d / "shm/c_pvr_gb.lock", "log": w["log"], "backup": w["backup"], "proc": d / "proc",
            "t0": time.time()}


def _b_runner(w: dict, events: list, bodies=None, heads=None, rc=None, hooks=None):
    bodies, heads, rc, hooks = bodies or w["bodies"], heads or w["heads"], rc or {}, hooks or {}

    def run(argv):
        argv = tuple(argv)
        s = "val" if "-val-" in argv[-1] else "test"
        kind = "head" if "-I" in argv else "body"
        fc = _FakeCurl((heads if kind == "head" else bodies)[s], rc.get((kind, s), 0), hooks.get((kind, s)))
        events.append((kind, s, argv, fc))
        return fc
    return run


def _gb_run(w: dict, env: dict, runner, gsha: str | None = None, ptag: str | None = None, **over):
    kw = {"pins_b": w["pins_b"], "a12": w["a12"], "want": w["want"], "remaining_n": len(w["rem"]), "strict": False}
    return gate_b(env, gsha or w["gsha"], ptag or w["tag"], runner, _gb_exit, w["pins"], **{**kw, **over})


def _alog(env: dict) -> list[str]:
    p = env["sealed"] / "ACCESS_LOG.tsv"
    return [x.split("\t")[2] for x in p.read_text().splitlines()] if p.exists() else []


def _b_variant(w: dict, s: str, body: bytes) -> tuple:
    """A stream body with a matching md5 record (re-pinned) and HEAD; _b_variant(w, s, w['bodies'][s]) restores."""
    p = w["root"] / PINS_B[f"md5_{s}"][0]
    p.write_text(f"{hashlib.md5(body).hexdigest()}  -\n")
    return ({**w["pins_b"], f"md5_{s}": (PINS_B[f"md5_{s}"][0], sha_file(p))}, {**w["bodies"], s: body},
            {**w["heads"], s: _head(body)})


def _gb_abort(w: dict, name: str, want: str, prep=None, **kw) -> dict:
    """One G-B run that must abort silently (Q-B11, W2) with GB_RC[want]: tmpfs gone, marker kept, abort row last."""
    env = _b_env(w, name)
    ev, over = [], {k: kw.pop(k) for k in ("pins_b",) if k in kw}
    if prep:
        kw["hooks"] = prep(env)
    old = {s: signal.getsignal(s) for s in GB_SIGS}
    code, out, _ = _silent(_gb_run, w, env, _b_runner(w, ev, **kw), **over)
    assert code == GB_RC[want] and out == b"", (name, code, len(out))
    assert not os.path.lexists(env["shm"]) and (env["sealed"] / "gb_start").stat().st_mode & 0o777 == 0o400, name
    rows = _alog(env)
    assert rows[0] == "gate-b start" and rows[-1] == f"gate-b abort {GB_RC[want]}", (name, rows)
    assert not (env["out"] / "gb_counts.json").exists() and not (env["sealed"] / "gb_intermediate.json").exists()
    assert {s: signal.getsignal(s) for s in GB_SIGS} == old, "signal handlers restored"
    return {"env": env, "events": ev, "rows": rows}


def _st_b_units(w: dict) -> None:
    """G5, G7-G10, G14-G16, G18, G20-G22, G24 and Q-B7 on their own functions."""
    import ast
    root, rem, hdr = w["root"], w["rem"], ",".join(LABEL_HEADER).encode()
    # G24: x-goog-hash md5 base64 -> hex (the OIL pair of this file), joined or split headers, composite refused
    assert bucket_md5(b"x-goog-hash: md5=2DL+t3Wzy3gHe/iuNQrc5Q==\r\ncontent-length: 7\r\n") == (OIL["md5"], 7)
    body = w["bodies"]["test"]
    assert bucket_md5(_head(body, True)) == bucket_md5(_head(body)) == (hashlib.md5(body).hexdigest(), len(body))
    for bad in (b"x-goog-hash: crc32c=AAAAAA==\r\ncontent-length: 7\r\n", b"x-goog-hash: md5=2DL+t3Wzy3gHe/iuNQrc5Q==\r\n",
                b"x-goog-hash: md5=2DL+t3Wzy3gHe/iu\r\ncontent-length: 7\r\n",
                b"x-goog-hash: md5=2DL+t3Wzy3gHe/iuNQrc5Q==, md5=2DL+t3Wzy3gHe/iuNQrc5Q==\r\ncontent-length: 7\r\n"):
        _must_gb("head", bucket_md5, bad)
    # G21 / G5: one pass over any read boundary, LF/CRLF, with and without a final newline = the reference filter
    keep = {i.encode() for i in rem[:40]}
    rows = [_b_row(i, "a", k % 2).encode() for k, i in enumerate(rem[:40] + w["other"][:40])]
    rows.append(_b_row(rem[0], "b", 0).encode())  # a kept record last: the no-final-newline case must flush it
    lf = b"\n".join([hdr] + rows) + b"\n"
    crlf = lf.replace(b"\n", b"\r\n")
    for data in (lf, lf[:-1], crlf, crlf[:-2]):
        ref = _ref_filter(data, keep)
        assert ref.count(b"\n") == 42 and ref.split(b"\n")[-2].rstrip(b"\r") == rows[-1], "header + 41 kept, last kept"
        for ch in (1, 7, 1 << 16, len(data) + 1):
            o = io.BytesIO()
            r = gb_filter(io.BytesIO(data).read, keep, o, chunk=ch)
            assert o.getvalue() == ref and r == {"sha256": sha_bytes(data), "md5": hashlib.md5(data).hexdigest(),
                                                 "bytes": len(data), "kept": 41, "filtered_sha256": sha_bytes(ref)}, ch
    _must_gb("header", gb_filter, io.BytesIO(b"ImageID,LabelName,Source,Confidence\n" + lf[len(hdr) + 1:]).read,
             keep, io.BytesIO())
    _must_gb("header", gb_filter, io.BytesIO(b"").read, keep, io.BytesIO())
    # G7: the conflict rule and present before absent; G8: once-check; G9: parity on the hand-counted fixture
    assert status({"pos": {"a"}, "neg": {"b"}}, {"a"}, {"b"}) == "present"
    assert status({"pos": {"a"}, "neg": {"b"}}, set(), {"b"}) == "absent" and status({"pos": {"a"}, "neg": set()},
                                                                                       set(), {"a"}) == "unknown"
    pb, a12 = w["pins_b"], w["a12"]
    assert parity(root, w["pins"], pb, a12, w["want"]) == {**w["want"], "pairs_per_class_equal": 4}
    want1 = json.loads(json.dumps(w["want"]))
    want1["image_class_pairs"]["present"] += 1
    _must("parity:", parity, root, w["pins"], pb, a12, want1)
    mp, desc = root / pb["map"][0], root / pb["desc"][0]
    good_map, man = mp.read_text(), root / pb["manifest"][0]
    for name in ("Twin", "Nope"):
        mp.write_text(json.dumps({**json.loads(good_map), "c6": {"pos": [name], "neg": []}}))
        _must("not exactly one OIV7 class", resolve_map, desc, mp)
    mp.write_text(good_map)
    good_man = man.read_text()
    for path in (("image_class_pairs", "absent"), ("pairs_per_class", "c3", "absent")):
        m = json.loads(good_man)
        node = m["coverage"]
        for k in path[:-1]:
            node = node[k]
        node[path[-1]] += 1
        man.write_text(json.dumps(m))
        _must("parity:", parity, root, w["pins"], {**pb, "manifest": (pb["manifest"][0], sha_file(man))}, a12, w["want"])
    man.write_text(good_man)
    # G18 / W2: a foreign id, a bad Confidence and a bad header raise a code, never the row
    lp = w["dir"] / "w2.csv"
    for txt, code in ((f"{hdr.decode()}\nffffffffffffffff,verification,/m/0a,1\n", "label_row"),
                      (f"{hdr.decode()}\n{rem[0]},verification,/m/0a,yes\n", "label_row"),
                      (f"{hdr.decode()}\n{rem[0]},verification,/m/0a\n", "label_row"),
                      (f"ImageID,Source,LabelName\n{rem[0]},verification,/m/0a\n", "header")):
        lp.write_text(txt)
        _must_gb(code, load_labels, set(rem), [lp], {lp.resolve(): sha_bytes(lp.read_bytes())})
    # G14 / Q-B8: only the exact allowed paths, after a sha check; BARRED and sha_file still refuse the A12 files
    a12p = root / a12["train"][0]
    _must_gb("integrity", allow_read, a12p, {})
    _must_gb("integrity", allow_read, a12p, {a12p.resolve(): "0" * 64})
    for p in [root / a12[s][0] for s in OI_SPLITS] + [SHM_GB / "filtered-val.csv"]:
        _must("REFUSED", sha_file, p)
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    callers: dict = {}
    for fn in tree.body:
        if isinstance(fn, ast.FunctionDef) and not fn.name.startswith("_"):
            for n in ast.walk(fn):
                if isinstance(n, ast.Call) and getattr(n.func, "id", "") in ("allow_read", "load_labels"):
                    callers.setdefault(n.func.id, set()).add(fn.name)
    assert callers == {"allow_read": {"load_labels"}, "load_labels": {"parity", "gate_b"}}, callers
    # G16: OI_TEST_URL byte-equal (c_pvr.py _st reads it by AST)
    url = [n.value.value for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") ==
           "OI_TEST_URL"]
    assert url == ["https://open-images-dataset.s3.amazonaws.com/" + "test/{file}"], url
    # G15: pinned argv (https only, -q first, no output file, no -k, no proxy); the real runner's spawn arguments
    assert list(CURL_STREAM) == ("/usr/bin/curl -q -sS --fail -L --proto =https --proto-redir =https --max-redirs 3 "
                                 "-A vsps-research").split()
    assert list(CURL_HEAD) == "/usr/bin/curl -q -sS -I --fail --proto =https".split()
    assert not {"-o", "-O", "-k", "--insecure", "--output", "-x", "--proxy", "-K", "--config"} & {*CURL_STREAM, *CURL_HEAD}
    probe = CURL_STREAM + ("https://example.invalid/x",)
    try:
        curl_run(probe)
        raise AssertionError("curl_run started a process in the selftest")
    except OSError as e:
        assert "subprocess disabled" in str(e), e
    assert _SPAWNS == [((probe,), {"stdin": subprocess.DEVNULL, "stdout": subprocess.PIPE,
                                   "stderr": subprocess.DEVNULL, "env": {"PATH": "/usr/bin:/bin"}})], _SPAWNS
    # G10: gb_counts.json holds the registered keys only
    good = {**{k: 0 for k in GB_KEYS}, "inputs": {"x": "0" * 64},
            "streams": {s: {k: 0 for k in GB_STREAM_KEYS} for s in ("val", "test")}}
    gb_counts_ok(good)
    for extra in ({"pairs_per_class": {}}, {"labels": {}}, {"rows_per_oi_split": {}}, {"kept_rows": 1},
                  {"streams": {**good["streams"], "val": {**good["streams"]["val"], "kept": 0}}},
                  {"inputs": {"x": "not a sha"}}):
        _must_gb("internal", gb_counts_ok, {**good, **extra})
    # G20 / W4: no-overwrite link, chmod and re-read checks
    wd = w["dir"] / "w4"
    wd.mkdir()
    assert write_new(wd / "a", b"abc", 0o400, check_mode=True) == sha_bytes(b"abc")
    assert (wd / "a").stat().st_mode & 0o777 == 0o400
    _must_gb("write", write_new, wd / "a", b"xyz", 0o400)
    assert (wd / "a").read_bytes() == b"abc" and sorted(x.name for x in wd.iterdir()) == ["a"], "no tmp left"
    real_chmod, real_link = os.chmod, os.link
    os.chmod = lambda *a, **k: None  # type: ignore[assignment]
    try:
        _must_gb("write", write_new, wd / "b", b"abc", 0o400, True)
    finally:
        os.chmod = real_chmod

    def torn_link(src, dst):
        real_link(src, dst)
        real_chmod(dst, 0o600)
        with open(dst, "ab") as f:
            f.write(b"!")

    os.link = torn_link  # type: ignore[assignment]
    try:
        _must_gb("write", write_new, wd / "c", b"abc", 0o400)
    finally:
        os.link = real_link
    # G22 / W6: the pause line, exactly
    lg, t0 = w["dir"] / "w6.md", time.time()
    lg.write_text(w["log"].read_text() + "2026-11-01T00:02Z OPS-1103c-min: G-B pause, minute stamp.\n"
                  "2026-11-01T00:03:00Z OPS-1103c-two: G-B pause.\n2026-11-01T00:04:00Z OPS-1103c-two: again.\n"
                  "2026-11-01T00:05:00Z OPS-1103c-nogb: pause for the window.\n"
                  "2026-11-01T00:06:00Z OPS-1103c-nop: G-B window.\nOPS-1103c-nostamp: G-B pause.\n"
                  "2026-11-01T00:07:00Z pre-OPS-1103c-tok: G-B pause.\n")
    assert pause_ok(lg, w["tag"], t0) is None and pause_ok(lg, "OPS-1103c-min", t0) is None
    for tag, tt, why in (("OPS-1103c-none", t0, "in 0 LOG lines"), ("OPS-1103c-two", t0, "in 2 LOG lines"),
                         ("OPS-1103c-gb", t0, "in 0 LOG lines"), ("OPS-1103c-tok", t0, "in 0 LOG lines"),
                         ("OPS-1103c-nostamp", t0, "no date -u stamp"),
                         (w["tag"], datetime.fromisoformat("2026-11-01T00:00:00+00:00").timestamp(), "no date -u"),
                         ("OPS-1103c-nogb", t0, "name G-B"), ("OPS-1103c-nop", t0, "name G-B"),
                         ("ops-1103c-gbpause", t0, "OPS-... token")):
        r = pause_ok(lg, tag, tt)
        assert r is not None and why in r, (tag, r)
    pd = w["dir"] / "w6proc"
    for pid, argv in ((os.getpid(), b"bash\0/x/c_pvr_job.sh\0"), (1, b"/sbin/init\0"), (7, b"")):
        (pd / str(pid)).mkdir(parents=True)
        (pd / str(pid) / "cmdline").write_bytes(argv)
    (pd / "self").mkdir()
    assert foreign_jobs(pd, os.getpid()) == 0, "own pid excluded"
    (pd / "4242").mkdir()
    (pd / "4242" / "cmdline").write_bytes(b"bash\0scripts/b_lre/b_job.sh\0")
    assert foreign_jobs(pd, os.getpid()) == 1
    # Q-B7: n_e_power subtracts the 4 Flickr ids of G_C2_record 767998f8
    assert n_e_power(100, 3, 1) == 92 and len(set(FLICKR_W3)) == 4 and all(HEX16.fullmatch(i) for i in FLICKR_W3)


def _st_b(base: Path, ga: Path, pins: dict, expected: list, rng) -> None:
    """G-B on synthetic fixtures (PINS-B §3.2 G1-G16 and CC-239 G17-G24). Never the real sealed, tmpfs or lock path."""
    w = _b_world(base, ga, pins, expected, rng)
    probe = _b_env(w, "probe")  # G19: the fixture paths are not the real ones
    assert probe["shm"] != SHM_GB and probe["lock"] != LOCK_GB and probe["sealed"] != SEALED, "W3 fixture paths"
    _st_b_units(w)
    _st_b_runs(w)
    assert len(_SPAWNS) == 1, "no G-B run spawned a process (G19)"


def _st_b_runs(w: dict) -> None:
    rem, root = w["rem"], w["root"]
    # G1 (N11) + success: gate_a_verify before the first HEAD; outputs, sealed bytes, rows, fsyncs
    events, synced = [], []
    real_verify, real_fsync = gate_a_verify, os.fsync

    def spy(*a, **k):
        events.append(("verify",))
        return real_verify(*a, **k)

    def rec_fsync(fd):
        synced.append(os.readlink(f"/proc/self/fd/{fd}"))
        real_fsync(fd)

    env = _b_env(w, "ok")
    globals()["gate_a_verify"], os.fsync = spy, rec_fsync
    try:
        code, out, rec = _silent(_gb_run, w, env, _b_runner(w, events))
    finally:
        globals()["gate_a_verify"], os.fsync = real_verify, real_fsync
    assert code is None and out == b"", (code, len(out))
    assert [e[:2] for e in events] == [("verify",), ("head", "val"), ("body", "val"), ("head", "test"),
                                       ("body", "test")], [e[:2] for e in events]
    for e in events[1:]:
        assert e[2] == (CURL_HEAD if e[0] == "head" else CURL_STREAM) + (OI_LABEL_URL.format(s=e[1]),)
    gb = json.loads((env["out"] / "gb_counts.json").read_text())
    assert gb == rec and set(gb) == GB_KEYS and gb["gates_sha256"] == w["gsha"]
    assert (gb["n_e_gb"], gb["present_pairs"], gb["absent_pairs"], gb["remaining"]) == (100, 100, 20, len(rem))
    assert gb["coverage_share"] == 100 / len(rem) and gb["ga_remaining_sha256"] == w["pins_b"]["ga_rem"][1]
    keep = {i.encode() for i in rem}
    for s, b in w["bodies"].items():
        md5 = hashlib.md5(b).hexdigest()
        assert gb["streams"][s] == {"sha256": sha_bytes(b), "md5": md5, "bucket_md5": md5, "record_md5": md5,
                                    "filtered_sha256": sha_bytes(_ref_filter(b, keep)), "bytes": len(b)}, s
    sp = env["sealed"] / "gb_intermediate.json"
    assert sp.read_bytes() == w["sealed"] and sp.stat().st_mode & 0o777 == 0o400, "G11 bytes and mode"
    assert gb["sealed_sha256"] == sha_bytes(w["sealed"]) and not os.path.lexists(env["shm"])
    lines = [x.split("\t") for x in (env["sealed"] / "ACCESS_LOG.tsv").read_text().splitlines()]
    assert [x[2] for x in lines] == ["gate-b start", "gate-b write", "gate-b unlink", "gate-b unlink"], lines
    assert [x[4] for x in lines[2:]] == [gb["streams"][s]["filtered_sha256"] for s in ("test", "val")]
    sd, od = str(env["sealed"].resolve()), str(env["out"].resolve())
    for want in (f"{sd}/.gb_start.", f"{sd}/.gb_intermediate.json.", f"{od}/.gb_counts.json.", sd, od,
                 f"{sd}/ACCESS_LOG.tsv"):
        assert any(x == want or (want.endswith(".") and x.startswith(want)) for x in synced), ("W4 fsync", want)
    # G11: determinism on a second fixture run; G2 / G17: the one-run rule
    env2 = _b_env(w, "ok2")
    assert _silent(_gb_run, w, env2, _b_runner(w, []))[0] is None
    assert (env2["sealed"] / "gb_intermediate.json").read_bytes() == w["sealed"]
    ev = []
    _must("REFUSED", _gb_run, w, env, _b_runner(w, ev))
    for name, make in (("counts", lambda e: (e["out"] / "gb_counts.json").write_text("{}")),
                       ("sealedf", lambda e: (e["sealed"] / "gb_intermediate.json").write_text("{}")),
                       ("marker", lambda e: (e["sealed"] / "gb_start").write_text("x")),
                       ("shmdir", lambda e: e["shm"].mkdir()),
                       ("row", lambda e: access_log_sync(e["sealed"], "gate-b start", "-", "x"))):
        e = _b_env(w, f"g2_{name}")
        make(e)
        _must("REFUSED", _gb_run, w, e, _b_runner(w, ev))
    # G3 (Q-B5), SUMS and pins; G1 tamper; parity in code; G12 tenancy before the start marker
    e = _b_env(w, "pre")
    sums = root / "scripts/c_pvr/SHA256SUMS"
    good_sums = sums.read_text()
    _must("--gates-sha differs", _gb_run, w, e, _b_runner(w, ev), gsha="0" * 64)
    for bad, tag in ((good_sums.replace(w["gsha"], "0" * 64), "no single gates.py line"),
                     (good_sums.replace(w["pins_b"]["map"][1], "0" * 64), "do not verify")):
        sums.write_text(bad)
        _must(tag, _gb_run, w, e, _b_runner(w, ev))
    sums.write_text(good_sums)
    _must("differs from its pin", _gb_run, w, e, _b_runner(w, ev),
          pins_b={**w["pins_b"], "fetch": (w["pins_b"]["fetch"][0], "0" * 64)})
    ip = w["ga"] / INFO["name"]
    good_info = ip.read_bytes()
    ip.write_bytes(good_info + b" ")
    _must("changed since G-A", _gb_run, w, e, _b_runner(w, ev))
    ip.write_bytes(good_info)
    want1 = json.loads(json.dumps(w["want"]))
    want1["verified_labels"]["conflicting"] -= 1
    _must("parity:", _gb_run, w, e, _b_runner(w, ev), want=want1)
    _must("unique ids", _gb_run, w, e, _b_runner(w, ev), remaining_n=len(rem) + 1)
    _must("tenancy:", _gb_run, w, e, _b_runner(w, ev), ptag="OPS-1103c-absent")
    good_bk = w["backup"].read_text()
    w["backup"].write_text(good_bk + "ls /dev/shm\n")
    _must("tenancy:", _gb_run, w, e, _b_runner(w, ev))
    w["backup"].write_text(good_bk)
    fd = os.open(e["lock"], os.O_RDWR | os.O_CREAT, 0o600)
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    try:
        _must("lock is held", _gb_run, w, e, _b_runner(w, ev))
    finally:
        os.close(fd)
    (e["proc"] / "4242").mkdir()
    (e["proc"] / "4242" / "cmdline").write_bytes(b"bash\0scripts/b_lre/b_job.sh\0")
    _must("tenancy:", _gb_run, w, e, _b_runner(w, ev))
    assert ev == [] and not (e["sealed"] / "gb_start").exists() and _alog(e) == [], "nothing before the marker"
    # aborts after the marker: rc only, nothing printed, tmpfs unlinked, abort row (Q-B11, W1, W2, G4, G6, G13)
    hb, bo = w["heads"], w["bodies"]
    r = _gb_abort(w, "a_md5head", "md5", heads={**hb, "test": _head(b"other bytes")})
    assert ("body", "test") not in [x[:2] for x in r["events"]], "Q-B12 in code: no body after a HEAD mismatch"
    assert r["rows"][1:3] == ["gate-b unlink", "gate-b abort 42"] and r["rows"].count("gate-b unlink") == 1
    composite = b"HTTP/2 200\r\nx-goog-hash: crc32c=AAAAAA==\r\ncontent-length: 5\r\n\r\n"
    r = _gb_abort(w, "a_composite", "head", heads={**hb, "val": composite})
    assert [x[:2] for x in r["events"]] == [("head", "val")]
    t = bo["test"]
    flip = t[:-2] + (b"0" if t[-2:-1] == b"1" else b"1") + b"\n"
    _gb_abort(w, "a_md5body", "md5", bodies={**bo, "test": flip})
    _gb_abort(w, "a_length", "integrity", heads={**hb, "test": _head(t, extra=1)})
    r = _gb_abort(w, "a_curl", "curl", rc={("body", "test"): 22})
    assert r["rows"].count("gate-b unlink") == 2, "both tmpfs files unlinked and logged"
    _gb_abort(w, "a_headrc", "head", rc={("head", "val"): 6})
    _gb_abort(w, "a_header", "header", bodies={**bo, "test": b"ImageID,Source,LabelName,Conf\n" + t.split(b"\n", 1)[1]})
    pb, b2, h2 = _b_variant(w, "val", bo["val"] + _b_row(rem[0], "a", 1).encode() + b"\n")
    _gb_abort(w, "a_valrow", "val_row", bodies=b2, heads=h2, pins_b=pb)
    _b_variant(w, "val", bo["val"])
    pb, b2, h2 = _b_variant(w, "test", t + f"{rem[0]},verification,/m/0a,yes\n".encode())
    _gb_abort(w, "a_conf", "label_row", bodies=b2, heads=h2, pins_b=pb)
    _b_variant(w, "test", t)

    def appear(env):
        def hook():
            (env["proc"] / "4243").mkdir(exist_ok=True)
            (env["proc"] / "4243" / "cmdline").write_bytes(b"bash\0b_job.sh\0")
        return {("body", "test"): hook}

    _gb_abort(w, "a_tenancy", "tenancy", prep=appear)
    _gb_abort(w, "a_shmmode", "tenancy", prep=lambda env: {("body", "test"): lambda: os.chmod(env["shm"], 0o755)})

    def fault_mid():
        raise SystemExit("FAULT: injected text that must never reach a stream")

    _gb_abort(w, "a_exit", "internal", hooks={("body", "test"): fault_mid})  # W2: a fault() after the marker is silent
    assert set(GB_SIGS) == {signal.SIGTERM, signal.SIGINT, signal.SIGHUP}
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):  # G13 / G23 mid-stream
        r = _gb_abort(w, f"a_sig{int(sig)}", "signal", prep=lambda env, sig=sig: {
            ("body", "test"): lambda: os.kill(os.getpid(), sig)})
        assert r["events"][-1][3].killed and r["rows"].count("gate-b unlink") == 2, sig
    ev = []
    _must("REFUSED", _gb_run, w, r["env"], _b_runner(w, ev))  # G17: a start marker bars a second run after an abort
    assert ev == []


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
    # W3 (CC-239): loopback-only network namespace, HOME (so SEALED) on ext4 scratch, never the real sealed dir
    nets = [x.split(":")[0].strip() for x in Path("/proc/self/net/dev").read_text().splitlines()[2:]]
    if nets != ["lo"] or SEALED.exists() or str(Path.home().resolve()).startswith("/mnt/"):
        fault("selftest runs only in the W3 sandbox: unshare -rnm, private /dev/shm, HOME on ext4 scratch")
    subprocess.Popen = _no_spawn  # type: ignore[assignment,misc]
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
        _st_b(base, ga, pins, expected, rng)
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
    real_b = {k: (ROOT / p).exists() and sha_file(ROOT / p) == s for k, (p, s) in PINS_B.items()}
    g = json.loads(pinned(ROOT, "g", {"g": (f"{PDIR}/G_C2_record.json",
                                             "767998f8e22aa595a01a646c8bc018b2b611a8c2136f074b67a43fbe595907cb")}).read_text())
    real_b["flickr_w3"] = sorted(g["flickr_image_exclusions"]) == list(FLICKR_W3)
    print("real (B) pins (sha only):", " ".join(f"{k}={'OK' if v else 'MISMATCH'}" for k, v in real_b.items()))
    if not all(real_b.values()):
        fault("a PINS-B real file is missing or differs")
    print(f"selftest ok  {LABEL}  gates.py {sha_file(Path(__file__))}")


# ------------------------------------------------------------------------------------------------ cli
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("selftest")
    a = sp.add_parser("gate-a")
    a.add_argument("phase", choices=("step0", "pin", "schema", "join", "verify"))
    a.add_argument("--info-sha")
    a.add_argument("--oi-sha")
    c = sp.add_parser("gate-c2")
    c.add_argument("phase", choices=("scan", "join"))
    c.add_argument("--file", choices=sorted(SFT))
    c.add_argument("--prefix-map", help="post-census map (one-judge read); may only add prefixes")
    b = sp.add_parser("gate-b", help="G-B once (PINS-B): stream, filter, one read, sealed write, gb_counts.json")
    b.add_argument("--gates-sha", required=True)
    b.add_argument("--pause-tag", required=True)
    pa = sp.add_parser("parity", help="prereg §3.3 loader parity on A's spent XM3600 rows (PINS-B)")
    pa.add_argument("--gates-sha", required=True)
    x = ap.parse_args()
    if x.cmd == "selftest":
        return selftest()
    if str(SEALED.resolve()).startswith("/mnt/"):
        fault(f"{SEALED} must sit on the WSL ext4 home")
    if x.cmd in ("gate-b", "parity"):
        return main_b(x)
    if x.cmd == "gate-a" and x.phase == "step0":  # N4: real pinned files, after GO, before any download
        s0 = step0(ROOT)
        print(json.dumps({k: len(v) for k, v in s0.items()}, sort_keys=True))
    elif x.cmd == "gate-a" and x.phase == "pin":  # N5: step-3 check, then the shas for the LOG line
        print(json.dumps(gate_a_pin(GA), indent=1, sort_keys=True))
    elif x.cmd == "gate-a" and x.phase == "schema":  # CC-227: names/types/lengths only, writes nothing
        if not x.info_sha:
            ap.error("schema needs --info-sha (the sha logged at download)")
        print(json.dumps(info_schema(GA / INFO["name"], x.info_sha), indent=1, sort_keys=True))
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
