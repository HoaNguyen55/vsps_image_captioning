#!/usr/bin/env python
"""Paper B, B-2 (DESCRIPTIVE ONLY): external Vietnamese captioning systems scored under the kit-B protocol columns.
Prereg manuscript/prereg/2026-10-28_b2_external/PREREG.md (CC-126 W13; PI-1026af; CC-130 twins).

No verdict, no ranking, no group system, no comparison with the group's registered numbers. Every system is scored
once on the one split it reports on; a KTVIC-test row is that system's one look. No caption is printed or written
outside the preds files under .session_backup/ (laptop) or /root/outputs/b2_external/ (M3).

  python scripts/b2_external/b2.py --selftest                                   CPU, synthetic data only
  python scripts/b2_external/b2.py fetch --out DIR                              laptop: class-(a) files at pinned commits
  python scripts/b2_external/b2.py gate --fetched DIR --data D --out gate.json  laptop: structure gate, counts only
  python scripts/b2_external/b2.py lists --data D --cen DIR --out DIR           laptop: image lists for M3 (no captions)
  python scripts/b2_external/b2.py hf-fetch --sid S --dest DIR                  M3 CPU: pinned snapshot, sha-checked
  python scripts/b2_external/b2.py uit-fetch --list F --dest DIR                M3 CPU: UIT-ViIC test images by coco_url
  python scripts/b2_external/b2.py guard --head H | left --used F --marker M                        M3
  python scripts/b2_external/b2.py smoke-fetch --dest DIR                       M3 CPU: the pinned UIT-ViIC train smoke image
  python scripts/b2_external/b2.py smoke --sid S --snap DIR [--tok DIR] --img2 F --out F          M3 GPU, no test image
  python scripts/b2_external/b2.py decode --sid S --snap DIR [--tok DIR] --images DIR --list F --out F   M3 GPU
  python scripts/b2_external/b2.py score --data D --fetched DIR --gate F --preds DIR --vnc DIR --thesis DIR
                                         --pilot F --out DIR                    laptop CPU, once
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUTPUTS = Path("/root/outputs")
LOCK = OUTPUTS / "b2_external/RUNNING"
SOFT_S, HARD_S, MIN_STEP_S = int(2.5 * 3600), 3 * 3600, 60
TWINS_TEST = {"1335", "507"}  # KTVIC test ids byte-identical to train 3589 / 7511 (CC-130)
PERMISSIVE = {"MIT", "BSD-3-Clause", "Apache-2.0"}
REFCOPY_MAX = 0.5
SETS = {"ktvic": 558, "uitviic": 231, "openviic": 2001}

# ------------------------------------------------------------------------------------------- the fixed system list
# Class (a): published per-image outputs on GitHub, pinned commit + git blob sha1. Class (b): HF checkpoints, pinned
# revision; weights by LFS sha256, small files by git blob sha1. ids: K<n> = Ken K15-2 §2.3 row n; X<n> = B-2 additions.
A_SYSTEMS = [
    {"sid": "K2", "source": "SuperCoolGuy855", "name": "CLIP + mT5 (KTVIC)", "set": "ktvic", "licence": None,
     "ktvic_train": True, "repo": "SuperCoolGuy855/CLIP_mT5_Image_captioning",
     "commit": "d786f6d7f2a7149ff8ed18021d4fab30bec39f9a",
     "files": {"results.xlsx": "e8352f8731ba9d86124dd6f16f4c3db4018b00af"}},
    {"sid": "X1", "source": "trannam710", "name": "Show, Attend and Tell (UIT-ViIC)", "set": "uitviic",
     "licence": "MIT", "ktvic_train": False, "repo": "trannam710/NIC-with-Soft-Attention",
     "commit": "06601183a2103544eb8a96ccda1ad1caac204526",
     "files": {"caption_results.json": "a72cdf1a0225b51c92ba1d327faefb5722c74f51"}},
    {"sid": "X2", "source": "trannam710", "name": "Meshed-Memory Transformer (UIT-ViIC)", "set": "uitviic",
     "licence": "BSD-3-Clause", "ktvic_train": False, "repo": "trannam710/Meshed-Memory-Transformer",
     "commit": "610980129fef563917001ad239be03e8e3e188ed",
     "files": {"caption_results.json": "b9273f0e1827e6fa91d6958409a3f0ebe08aa9ea"}},
    {"sid": "X3", "source": "vanngthi", "name": "ViECap (UIT-ViIC; variants original, detect)", "set": "uitviic",
     "licence": None, "ktvic_train": False, "repo": "vanngthi/ViECAP-Image-Captioning-Vietnamese",
     "commit": "fd71ca596aeb4ba21088cb3ddb450eee33d0c7cf",
     "files": {"annotations/uit_viic_original_pred.json": "3bbcd392ac57feebde836076407b90981f13ad7f",
               "annotations/uit_viic_detect_pred.json": "8b171c86be40c9fec6f72c50ab7e8ca7c74efb9f"}},
] + [
    {"sid": f"X4{k}", "source": "loc110504", "name": f"{m} (UIT)", "set": "uitviic", "licence": "MIT",
     "ktvic_train": False, "repo": "loc110504/VietnameseSportImageCaptioning",
     "commit": "6d8132e4ba809aaf0624d106f5ab3b6c1bba6af2",
     "files": {f"notebooks/4_models/generated_captions/{m}/uit_generated_captions.txt": b}}
    for k, m, b in (("a", "cnn_lstm", "6b786afbb5db254a101845d5e202a0e6f5e4f0f3"),
                    ("b", "cnn_lstm_attention", "f50d655eefa202c4198a0224415cc353cd47c273"),
                    ("c", "cnn_t5", "aa132bf647698bff6277e84cd03e26d7cea28ce6"),
                    ("d", "qwen2", "671928f146c27318bc02ef44de169e1d9017dd11"),
                    ("e", "vit_t5", "34cd277975587b5adcf8b98d56402221198acc17"))]
B_SYSTEMS = [  # priority order (PREREG §2.2): reported score on the split first, then smaller download
    {"sid": "K5", "source": "thuanan", "name": "SmolVLM2-500M-vi-stage1", "set": "uitviic", "licence": "Apache-2.0",
     "ktvic_train": False, "kind": "smolvlm", "hf": "thuanan/SmolVLM2-500M-vi-stage1",
     "rev": "5046708822ca7529c19e0dd069608b93a5a24685",
     "files": {"chat_template.json": "1d342e4f070c962a14ba4ece4e06212bc70d8e36",
               "config.json": "79a9135da412597b3e643f2332c060e725e326e2",
               "generation_config.json": "b7236b8d1cab49a5f454002023ce230c6124c570",
               "merges.txt": "5b8def9005c2607860e1e543c7defab973f53a3f",
               "model.safetensors": "4cd9de15fec79964cca50da00a6d732136b258344a2f8a8d7d41b4066dba8915",
               "preprocessor_config.json": "bf7669a38692ad141d333db3be18bd55cb6e2c59",
               "processor_config.json": "83df8c48da1f41e1a9129a4bc2aba000eb2b529f",
               "special_tokens_map.json": "2b5aee28d56c0e9d89ff6bc70818fba986a90ca9",
               "tokenizer.json": "4e9a7359902d2047ef894bde3d1bc30af9661283",
               "tokenizer_config.json": "35423e8174790cd7fd17c0d2ba160babf85c1b0b",
               "vocab.json": "3a30ee5a7f29cfd747e7665c3c87d821af1b783a"}},
    {"sid": "K1", "source": "Skyler215", "name": "Swin-BART (KTVIC by model name only; card: unknown dataset)", "set": "ktvic", "licence": None,
     "ktvic_train": True, "kind": "ved", "hf": "Skyler215/Swin_BART_KTVIC",
     "rev": "20044ae681d19f939bba779292591081957da090",
     "files": {"config.json": "cc1970f0a7b498ca824da974d3aafc927bd6a1fe",
               "generation_config.json": "4437cce53d56d3e73e4871d067400f6c524aeb39",
               "model.safetensors": "de6bceed925864986ee3df40f161937a9542db6d2d8c55c1f3a2b8f3ebbd23c8",
               "preprocessor_config.json": "c51f9953abca17af652063d4d341ede2cfda7397"},
     "tok": {"hf": "vinai/bartpho-syllable", "rev": "36eee8b4d648dd99da56462edcda3c5c97f7f3de",
             "files": {"config.json": "bc6ce69ed1fa72904a96ebf71302dd97b5ccc04c",
                       "dict.txt": "105fa545a4bdfdea381cabae659aa1b72f79700e",
                       "tokenizer.json": "9bb659f0ee7adf8ae37c37123c5cfec648a41060cf1abd1d1139adc2c1e731b9"}}},
    {"sid": "K6", "source": "nviquang", "name": "Vie-BLIP (UIT-OpenViIC)", "set": "openviic", "licence": "other",
     "ktvic_train": False, "kind": "blip", "hf": "nviquang/Vie-BLIP",
     "rev": "1ffe73cf6a1340c0c7b31f5fdd30a8d95d42acc0",
     "files": {"added_tokens.json": "1f6ddcea4cb4f94f751b1315127d0d24ac2a17c8",
               "bpe.codes": "b9a70c1a314ef0c6d97dffd98b34a1c60b988a6e",
               "config.json": "aaa65e55a45bb5d46e5b47dc61c26fb9e8a3877b",
               "generation_config.json": "b929d1a3c87f3d5e10ebbd4d680c740ed6f57296",
               "model.safetensors": "350aa9b818f3c378df96b1667e7b157276690b545c3b1411e6b6b81916e2a05c",
               "processor_config.json": "5cc876965ffbce60e2c2900ec69f1f342c87e9e7",
               "tokenizer_config.json": "3492ca20f417e71c40b72c624e2283ae01d1fd05",
               "vocab.txt": "0dbdec11459dd9d1f6e985bf6c58dbcf6adaeabd"}},
]
SYSTEMS = {s["sid"]: s for s in A_SYSTEMS + B_SYSTEMS}
SMOL_PROMPT = "Mô tả bức ảnh này."  # the model card's usage prompt (rev 50467088)
BLIP_GEN = {"max_length": 64, "num_beams": 5, "early_stopping": True, "no_repeat_ngram_size": 3,
            "repetition_penalty": 1.5}  # the model card's usage example (rev 1ffe73cf)
# Second smoke input (B-2 Amendment 1, CC-138 W2): the UIT-ViIC TRAIN image with the smallest id whose sha256 is in no
# test-side list (checked on the laptop 2026-10-28: 0 hits in 22,260 + the three B-2 lists); M3 re-checks the sha.
COCO_URL = "http://images.cocodataset.org/{filepath}/{file}"  # as in scripts/c_en/cen_fetch.py
SMOKE_IMG = {"id": 368, "file": "000000000368.jpg", "url": COCO_URL.format(filepath="train2017", file="000000000368.jpg"),
             "sha256": "58b0179921d415ca01b697255d473955e52559123e4a4b565e4d009dbb6c5f17"}
TRUNC = {"00000000768.jpg", "00000001010.jpg", "00000005095.jpg"}  # OpenViIC test, truncated in the release (CC-082 T6)
NOT_RUNNABLE = "not runnable: empty output under the registered recipe (transformers 4.57.6)"  # CC-138 W3 (c)


# ------------------------------------------------------------------------------------------------------ hashing
def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def file_ok(p: Path, pin: str) -> bool:
    """A 64-hex pin is an LFS sha256, a 40-hex pin a git blob sha1."""
    return sha_file(p) == pin if len(pin) == 64 else git_blob(p.read_bytes()) == pin


# ------------------------------------------------------------------------------------------- ids, parse, gate
def norm_id(x) -> str:
    s = os.path.basename(str(x).strip())
    s = re.sub(r"\.(jpe?g|png)$", "", s, flags=re.I)
    return str(int(s)) if s.isdigit() else s


def load_refs(name: str, data: Path) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Official test references (raw) by canonical id, and an alias map (id or file name -> canonical id)."""
    if name == "openviic":
        d = json.loads((data / "openviic/uit-openviic-annotation-test.json").read_text(encoding="utf-8"))
        refs = {k: [c.strip() for c in v["captions"] if c and c.strip()] for k, v in d.items()}
        alias = {norm_id(k): k for k in d}
    else:
        d = json.loads((data / f"{name}/test_data.json").read_text(encoding="utf-8"))
        refs = {}
        for a in d["annotations"]:
            if a.get("caption") and a["caption"].strip():
                refs.setdefault(str(a["image_id"]), []).append(a["caption"].strip())
        alias = {}
        for im in d["images"]:
            alias[norm_id(im["id"])] = str(im["id"])
            alias[norm_id(im.get("filename") or im.get("file_name"))] = str(im["id"])
    if len(refs) != SETS[name]:
        raise SystemExit(f"REFUSED: {name} test has {len(refs)} images, not {SETS[name]}")
    return refs, alias


ID_KEYS = ("image_id", "id", "img_id", "image", "file_name", "filename", "image_name", "img")
CAP_KEYS = ("caption", "pred", "prediction", "predicted", "generated", "generated_caption", "text", "output",
            "hypothesis")


class Ambiguous(ValueError):
    """A record with more than one caption key: excluded, never resolved (CC-132 W2a)."""


def first(d: dict, keys):
    low = {str(k).lower(): k for k in d}
    hits = [k for k in keys if k in low]
    if keys is CAP_KEYS and len(hits) > 1:
        raise Ambiguous("more than one caption key")
    if not hits:
        raise KeyError(keys)
    return d[low[hits[0]]]


def as_text(v) -> str:
    if isinstance(v, list):
        v = v[0] if v else ""
    if isinstance(v, dict):
        v = first(v, CAP_KEYS)
    if not isinstance(v, str):
        raise ValueError("caption is not a string")
    return v


def parse(path: Path) -> list[tuple[str, str]]:
    """The registered parser (PREREG §3.1). Raises ValueError/KeyError on anything else: never aligned by position."""
    suf = path.suffix.lower()
    if suf == ".json":
        d = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(d, dict) and isinstance(d.get("annotations"), list):
            d = d["annotations"]
        if isinstance(d, list):
            return [(str(first(r, ID_KEYS)), as_text(first(r, CAP_KEYS))) for r in d]
        return [(str(k), as_text(v)) for k, v in d.items()]
    if suf in (".txt", ".tsv", ".csv"):
        out = []
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
            if line.strip():
                m = re.match(r"\s*([^\t,\s]+)[\t,\s](.*)$", line)  # the first tab, comma or space (CC-132 W2b)
                if m is None:
                    raise ValueError("a line without a separator")
                if n == 0 and m.group(1).lower() in ID_KEYS:
                    continue  # one header line
                out.append((m.group(1), m.group(2).strip()))
        return out
    if suf == ".xlsx":
        import openpyxl
        rows = list(openpyxl.load_workbook(path, read_only=True).worksheets[0].iter_rows(values_only=True))
        head = {str(h).strip().lower(): n for n, h in enumerate(rows[0]) if h is not None}
        if sum(k in head for k in CAP_KEYS) > 1:
            raise Ambiguous("more than one caption column")
        ci, cc = [next(head[k] for k in keys if k in head) for keys in (ID_KEYS, CAP_KEYS)]
        return [(str(r[ci]), as_text(r[cc] or "")) for r in rows[1:] if r[ci] is not None]
    raise ValueError(f"no registered parser for {suf}")


def canon(t: str) -> str:
    """For the reference-copy test: underscores to spaces, every punctuation character removed, lower-cased,
    whitespace collapsed (CC-132 W2c)."""
    return " ".join(re.sub(r"[^\w\s]", " ", t.replace("_", " ")).lower().split())


def gate_file(path: Path, refs: dict[str, list[str]], alias: dict[str, str]) -> tuple[dict, dict[str, str]]:
    """Counts only. PASS iff parseable, every id maps to the official test set, the id set equals it exactly, one
    prediction per id, and fewer than REFCOPY_MAX of the predictions equal a reference of the same image."""
    rec = {"file_sha256": sha_file(path)}
    try:
        rows = parse(path)
    except Exception as e:  # any parser error is a registered exclusion (PREREG §3.1), never a repair
        why = "ambiguous caption field" if isinstance(e, Ambiguous) else f"unparseable ({type(e).__name__})"
        return {**rec, "pass": False, "reason": why}, {}
    mapped = [(alias.get(norm_id(i)), c) for i, c in rows]
    unknown = sum(m is None for m, _ in mapped)
    ids = [m for m, _ in mapped if m is not None]
    preds = dict((m, c) for m, c in mapped if m is not None)
    copies = sum(canon(preds[i]) in {canon(r) for r in refs[i]} for i in preds)
    rec.update({"rows": len(rows), "unknown_ids": unknown, "duplicate_ids": len(ids) - len(set(ids)),
                "covered": len(set(ids) & set(refs)), "test_images": len(refs),
                "empty": sum(not c.strip() for c in preds.values()),
                "refcopy_share": round(copies / max(1, len(preds)), 4)})
    reason = ("unknown ids" if unknown else "duplicate ids" if rec["duplicate_ids"]
              else "not the official test id set" if set(ids) != set(refs)
              else "looks like references" if rec["refcopy_share"] >= REFCOPY_MAX else "")
    rec.update({"pass": not reason, "reason": reason or "ok"})
    return rec, (preds if not reason else {})


# ----------------------------------------------------------------------------------------- host, lock and cap
def isolation(outputs: Path = OUTPUTS, names: list[str] | None = None, tmux: str | None = None) -> list[str]:
    tmux = os.environ.get("TMUX", "") if tmux is None else tmux
    if names is None:
        r = subprocess.run(["tmux", "ls", "-F", "#S"], capture_output=True, text=True)
        names = r.stdout.split() if r.returncode == 0 else []
    try:
        found = sorted(str(p) for p in outputs.glob("*/RUNNING"))
    except OSError:
        found = []
    bad = [] if tmux else ["not inside a tmux session"]
    return bad + [f"C-EN tmux session {n}" for n in names if n.startswith("cen")] + [f"lock {p} exists" for p in found]


def guard(head: str) -> None:
    """M3, idle GPU, committed HEAD, clean tree; C-EN clear; no other lock than B-2's own (taken by the chain)."""
    sys.path.insert(0, str(ROOT / "scripts/grl"))
    import common as K

    if K.host_ok(head) != "m3":
        raise SystemExit("REFUSED: B-2 runs on M3 only")
    K.m3_clear()
    if not LOCK.exists():
        raise SystemExit(f"REFUSED: {LOCK} (taken by b2_chain.sh stage) is missing")
    others = [x for x in isolation() if x != f"lock {LOCK} exists"]
    if others:
        raise SystemExit(f"REFUSED: {others}")


def used_seconds(used: Path, now: float | None = None) -> float:
    """`NAME start EPOCH` before a GPU step, `NAME SECONDS` after; an open start is charged to the next start or now."""
    if not used.exists():
        return 0.0
    total, open_t = 0.0, None
    for p in (x.split() for x in used.read_text().splitlines() if x.strip()):
        if len(p) == 3 and p[1] == "start":
            total += 0.0 if open_t is None else float(p[2]) - open_t
            open_t = float(p[2])
        else:
            total, open_t = total + float(p[1]), None
    return total + (0.0 if open_t is None else (time.time() if now is None else now) - open_t)


def left(used: Path, marker: Path) -> int:
    if marker.exists():
        return 0
    s = used_seconds(used)
    rest = int(HARD_S - s)
    return rest if s < SOFT_S and rest >= MIN_STEP_S else 0


# -------------------------------------------------------------------------------------------- fetch and stage
def http_get(url: str) -> bytes:
    import urllib.request

    for n in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except OSError:
            time.sleep(5 * (n + 1))
    raise SystemExit(f"fetch failed: {url}")


def cmd_fetch(a) -> None:
    rec = []
    for s in A_SYSTEMS:
        for rel, blob in s["files"].items():
            url = f"https://raw.githubusercontent.com/{s['repo']}/{s['commit']}/{rel}"
            dst = a.out / s["sid"] / Path(rel).name
            data = dst.read_bytes() if dst.is_file() else http_get(url)
            if git_blob(data) != blob:
                raise SystemExit(f"STOP: {s['sid']} {rel}: blob differs from the pin")
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
            rec.append({"sid": s["sid"], "url": url, "git_blob_sha1": blob,
                        "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    (a.out / "fetch.json").write_text(json.dumps({"utc": time.strftime("%FT%TZ", time.gmtime()), "files": rec}, indent=1))
    print(f"fetched {len(rec)} files, blobs verified")


def gate_all(fetched: Path, data: Path) -> tuple[dict, dict]:
    recs, preds, cache = {}, {}, {}
    for s in A_SYSTEMS:
        if s["set"] not in cache:
            cache[s["set"]] = load_refs(s["set"], data)
        refs, alias = cache[s["set"]]
        for rel in s["files"]:
            key = s["sid"] + ("" if len(s["files"]) == 1 else ":" + Path(rel).stem)
            recs[key], preds[key] = gate_file(fetched / s["sid"] / Path(rel).name, refs, alias)
    return recs, preds


def cmd_gate(a) -> None:
    if a.out.exists():
        raise SystemExit(f"REFUSED: {a.out} exists (the gate runs once)")
    recs, _ = gate_all(a.fetched, a.data)
    a.out.write_text(json.dumps(recs, indent=1))
    for k, r in recs.items():
        print(k, "PASS" if r["pass"] else "FAIL", r["reason"])


def cmd_lists(a) -> None:
    """Per class-(b) set: id, file, sha256 (KTVIC, OpenViIC: local images) or id, file, coco_url (UIT-ViIC); no
    caption. Refuses if any local image sha is in C-EN's test-side records (the M3 mirror)."""
    cen = set()
    for p in sorted(a.cen.glob("*.sha256.tsv")):
        if not p.name.startswith("memory"):
            cen |= set(re.findall(r"\b[0-9a-f]{64}\b", p.read_text()))
    if not cen:
        raise SystemExit(f"STOP: no C-EN test-side sha records under {a.cen}")
    a.out.mkdir(parents=True, exist_ok=True)
    for name in sorted({s["set"] for s in B_SYSTEMS}):
        if name == "uitviic":
            d = json.loads((a.data / "uitviic/test_data.json").read_text(encoding="utf-8"))
            rows = [f"{im['id']}\t{im['file_name']}\t{im['coco_url']}" for im in d["images"]]
        else:
            refs, _ = load_refs(name, a.data)
            if name == "ktvic":
                d = json.loads((a.data / "ktvic/test_data.json").read_text(encoding="utf-8"))
                files = {str(im["id"]): im["filename"] for im in d["images"]}
            else:
                files = {k: k for k in refs}
            rows = []
            for i in sorted(refs):
                h = sha_file(a.data / name / "images" / files[i])
                if h in cen:
                    raise SystemExit(f"STOP: a {name} test image is in C-EN's test-side records")
                rows.append(f"{i}\t{files[i]}\t{h}")
        if len(rows) != SETS[name]:
            raise SystemExit(f"STOP: {name} list has {len(rows)} rows")
        (a.out / f"{name}.tsv").write_text("\n".join(rows) + "\n")
        print(name, len(rows), "rows;", "C-EN overlap checked on M3 (uit-fetch)" if name == "uitviic"
              else f"C-EN test-side overlap 0 of {len(cen)} record shas")


def cmd_hf_fetch(a) -> None:
    from huggingface_hub import snapshot_download

    s = SYSTEMS[a.sid]
    for part, dst in ((s, a.dest / a.sid), (s.get("tok"), a.dest / f"{a.sid}_tok")):
        if not part:
            continue
        snapshot_download(part["hf"], revision=part["rev"], allow_patterns=list(part["files"]), local_dir=dst)
        bad = [f for f, pin in part["files"].items() if not file_ok(dst / f, pin)]
        if bad:
            raise SystemExit(f"STOP: {part['hf']}@{part['rev'][:8]}: {bad} differ from the pins")
        print(part["hf"], part["rev"], f"{len(part['files'])} files verified")


def cmd_uit_fetch(a) -> None:
    sys.path.insert(0, str(ROOT / "scripts/grl"))
    import common as K

    cen = K.cen_test_shas()
    a.dest.mkdir(parents=True, exist_ok=True)
    out = []
    for line in a.list.read_text().splitlines():
        i, f, url = line.split("\t")
        if f != f"{int(i):012d}.jpg" or not url.endswith("/" + f):
            raise SystemExit(f"STOP: UIT-ViIC id {i}: file name or url breaks the release rule")
        p = a.dest / f
        data = p.read_bytes() if p.is_file() else K.fetch(url)
        h = hashlib.sha256(data).hexdigest()
        if h in cen:
            raise SystemExit("STOP: a UIT-ViIC test image is in C-EN's test-side records")
        p.write_bytes(data)
        out.append(f"{i}\t{f}\t{h}")
    (a.dest.parent / "uitviic.sha.tsv").write_text("\n".join(out) + "\n")
    print(len(out), "UIT-ViIC test images, C-EN overlap 0")


def cmd_smoke_fetch(a) -> None:
    """The pinned second smoke image (CC-138 W2) by coco_url; sha must equal the pin and lie outside C-EN's records."""
    sys.path.insert(0, str(ROOT / "scripts/grl"))
    import common as K

    p = a.dest / SMOKE_IMG["file"]
    data = p.read_bytes() if p.is_file() else K.fetch(SMOKE_IMG["url"])
    h = hashlib.sha256(data).hexdigest()
    if h != SMOKE_IMG["sha256"] or h in K.cen_test_shas():
        raise SystemExit("STOP: the smoke image differs from its pin or is in C-EN's test-side records")
    a.dest.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    print(f"smoke image {SMOKE_IMG['id']} sha verified")


# ------------------------------------------------------------------------------------------------- decode (GPU)
class LoadFail(Exception):
    """Raised only inside a registered from_pretrained call or a registered artifact check: class (c)."""


SMOKE_PHRASE = "chiếc ấm trà thạch anh tím đang hát ru bảy con sứa giấy bạc"  # author-written, not a dataset caption


def pretrained(fn, *args, **kw):
    try:
        return fn(*args, **kw)
    except Exception as e:  # a registered load error: class (c), no retry with other code (PREREG §2.3)
        raise LoadFail(f"{getattr(fn, '__qualname__', fn)}: {type(e).__name__}") from e


def load_model(fn, snap: Path, info: dict, **kw):
    """from_pretrained with output_loading_info=True (CC-132 W3): missing weights = LoadFail (no silent random
    init); unexpected keys are counted only (into `info`)."""
    m, li = pretrained(fn, snap, output_loading_info=True, **kw)
    if li.get("missing_keys"):
        raise LoadFail(f"{len(li['missing_keys'])} weights missing from the checkpoint")
    info["unexpected_keys"] = info.get("unexpected_keys", 0) + len(li.get("unexpected_keys") or [])
    return m


def declared_class(tk, snap: Path) -> None:
    """The tokenizer built must be the class the checkpoint declares (or its Fast twin), else class (c)."""
    want = json.loads((snap / "tokenizer_config.json").read_text()).get("tokenizer_class")
    if want and type(tk).__name__ not in (want, want + "Fast"):
        raise LoadFail(f"tokenizer class {type(tk).__name__} is not the declared {want}")


def _ids(*xs) -> set[int]:
    """Token ids from ints, lists of ints or None."""
    out: set[int] = set()
    for x in xs:
        out |= set(x) if isinstance(x, (list, tuple)) else set() if x is None else {int(x)}
    return out


def new_tokens(ids: list[int], start: set[int] = frozenset(), bos: set[int] = frozenset()) -> list[int]:
    """Generated ids of an encoder-decoder or BLIP generate (B-2 Amendment 1): the first id is dropped if it is the
    decoder-start / injected bos id, then one more if it is a bos id. Decoder-only outputs are sliced before."""
    ids = list(ids)
    if ids[:1] and ids[0] in start:
        ids = ids[1:]
    if ids[:1] and ids[0] in bos:
        ids = ids[1:]
    return ids


def smoke_counts(new: list[int], text: str, end: set[int], special: set[int]) -> dict:
    """W1: counts only, never the text."""
    return {"n_new_tokens": len(new), "n_special_new": sum(t in special or t in end for t in new),
            "first_new_is_eos": bool(new) and new[0] in end, "n_chars": len(text)}


def smoke_class(new: list[int], text: str, end: set[int], special: set[int]) -> tuple[str, str]:
    """W3 per input: 'stop' (ours: zero new tokens, (b) a special token other than eos, (a) text tokens decoding to
    empty), 'eos' (only eos tokens) or 'text'."""
    if not new:
        return "stop", "zero new tokens"
    if any(t in special and t not in end for t in new):
        return "stop", "(b) a special token other than eos"
    n_text = sum(t not in special and t not in end for t in new)
    if n_text and not text.strip():
        return "stop", "(a) text tokens decode to an empty string"
    return ("text", "") if n_text else ("eos", "")


def smoke_verdict(classes: list[tuple[str, str]]) -> tuple[int, str]:
    """W3 over both inputs: any (a)/(b) -> JOB STOP (rc 1); immediate eos on both -> rc 5 (class (c)); else PASS."""
    stops = [why for c, why in classes if c == "stop"]
    if stops:
        return 1, stops[0]
    return (5, NOT_RUNNABLE) if all(c == "eos" for c, _ in classes) else (0, "ok")


def captioner(s: dict, snap: Path, tok: Path | None):
    """The registered recipe per kind (PREREG §2.3): safetensors through transformers, no remote code, no pickle.
    Returns (caption function -> (text, new ids), tokenizer, load-info counts plus the end and special id sets). Only
    `pretrained` calls and the artifact checks raise LoadFail; any other error is a bug of this code and reaches the
    job as a JOB STOP."""
    import torch
    import transformers as T

    kw = {"trust_remote_code": False, "use_safetensors": True}
    info: dict = {}
    if s["kind"] == "ved":
        m = load_model(T.VisionEncoderDecoderModel.from_pretrained, snap, info, **kw).to("cuda").eval()
        proc = pretrained(T.ViTImageProcessor.from_pretrained, snap)
        tk = pretrained(T.PreTrainedTokenizerFast, tokenizer_file=str(tok / "tokenizer.json"), bos_token="<s>",
                        eos_token="</s>", pad_token="<pad>", unk_token="<unk>")
        if len(tk) != m.config.decoder.vocab_size or tk.convert_tokens_to_ids(["<s>", "<pad>", "</s>"]) != [0, 1, 2]:
            raise LoadFail("tokenizer.json does not match the decoder vocabulary or special ids")

        gc = m.generation_config
        start = _ids(m.config.decoder_start_token_id, gc.decoder_start_token_id)
        bos = _ids(tk.bos_token_id, gc.forced_bos_token_id)

        def run(img):
            out = m.generate(proc(images=img, return_tensors="pt").pixel_values.to("cuda"))[0]
            return tk.decode(out, skip_special_tokens=True), new_tokens(out.tolist(), start, bos)
    elif s["kind"] == "smolvlm":
        proc = pretrained(T.AutoProcessor.from_pretrained, snap)
        m = load_model(T.AutoModelForImageTextToText.from_pretrained, snap, info, torch_dtype=torch.bfloat16, **kw)
        m = m.to("cuda").eval()
        tk = proc.tokenizer
        declared_class(tk, snap)
        msgs = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": SMOL_PROMPT}]}]
        prompt = proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)

        def run(img):
            x = proc(text=prompt, images=[img], return_tensors="pt").to("cuda", torch.bfloat16)
            out = m.generate(**x, max_new_tokens=64, do_sample=False)[0, x["input_ids"].shape[1]:]
            return tk.decode(out, skip_special_tokens=True), out.tolist()
    elif s["kind"] == "blip":
        ip = pretrained(T.BlipImageProcessor.from_pretrained, snap)
        tk = pretrained(T.AutoTokenizer.from_pretrained, snap, trust_remote_code=False)
        declared_class(tk, snap)
        m = load_model(T.BlipForConditionalGeneration.from_pretrained, snap, info, **kw).to("cuda").eval()
        start, bos = _ids(m.config.text_config.bos_token_id), _ids(tk.bos_token_id)
        info["end"] = _ids(m.config.text_config.sep_token_id)  # BLIP's generate stops at the text sep id

        def run(img):
            px = ip(images=img, return_tensors="pt")["pixel_values"].to("cuda")
            out = m.generate(pixel_values=px, **BLIP_GEN)[0]
            return tk.decode(out, skip_special_tokens=True), new_tokens(out.tolist(), start, bos)
    else:
        raise SystemExit(f"no recipe for kind {s['kind']}")
    info["end"] = info.get("end", set()) | _ids(m.generation_config.eos_token_id, tk.eos_token_id)  # eos only, no pad
    info["special"] = set(tk.all_special_ids) | {i for i, t in getattr(tk, "added_tokens_decoder", {}).items()
                                                 if getattr(t, "special", False)}
    return run, tk, info


def write_loadfail(out_dir: Path, sid: str, e: LoadFail) -> int:
    (out_dir / f"{sid}.LOADFAIL.json").write_text(json.dumps({"sid": sid, "reason": str(e)}))
    print(f"LOADFAIL {sid}: {e}")
    return 4


def cmd_smoke(a) -> int:
    """Before any test image (PREREG §5.2, Amendment 1): load, the tokenizer round trip on an author-written phrase,
    one generate on a flat grey image and one on the pinned UIT-ViIC train image. Writes class names and token
    counts only, never the text (CC-138 W1). rc 4 = LOADFAIL; rc 5 = immediate eos on both inputs (SMOKEFAIL json,
    class (c)); a W3 (a)/(b) case or any other failure = STOP."""
    import torch
    from PIL import Image

    s = SYSTEMS[a.sid]
    if sha_file(a.img2) != SMOKE_IMG["sha256"]:
        raise SystemExit("STOP: the second smoke image differs from its pin")
    torch.manual_seed(0)
    try:
        run, tk, info = captioner(s, a.snap, a.tok)
    except LoadFail as e:
        return write_loadfail(a.out.parent, a.sid, e)
    back = tk.decode(tk(SMOKE_PHRASE, add_special_tokens=False)["input_ids"], skip_special_tokens=True)
    if canon(back) != canon(SMOKE_PHRASE):
        raise SystemExit(f"STOP: {a.sid} tokenizer round trip differs ({len(back)} chars)")
    imgs = {"grey": Image.new("RGB", (384, 384), (127, 127, 127)), "train368": Image.open(a.img2).convert("RGB")}
    per, classes = {}, []
    with torch.inference_mode():
        for k, img in imgs.items():
            text, new = run(img)
            per[k] = smoke_counts(new, text, info["end"], info["special"])
            classes.append(smoke_class(new, text, info["end"], info["special"]))
    rc, why = smoke_verdict(classes)
    rec = {"sid": a.sid, "tokenizer": type(tk).__name__, "vocab": len(tk), "round_trip": True,
           "unexpected_keys": info.get("unexpected_keys", 0), "smoke": per}
    print(json.dumps(rec))  # counts only
    if rc == 1:
        raise SystemExit(f"STOP: {a.sid} smoke, ours by CC-138 W3: {why}")
    if rc == 5:
        (a.out.parent / f"{a.sid}.SMOKEFAIL.json").write_text(json.dumps({**rec, "rc": 5, "reason": why}))
        print(f"SMOKEFAIL {a.sid}: {why}")
        return 5
    a.out.write_text(json.dumps(rec))
    print(f"smoke ok {a.sid}")
    return 0


def cmd_decode(a) -> int:
    import torch
    import transformers
    from PIL import Image

    s = SYSTEMS[a.sid]
    if a.out.exists():
        raise SystemExit(f"REFUSED: {a.out} exists (one decode per system)")
    rows = [line.split("\t") for line in a.list.read_text().splitlines() if line.strip()]
    if len(rows) != SETS[s["set"]]:
        raise SystemExit(f"STOP: {len(rows)} images, not {SETS[s['set']]}")
    torch.manual_seed(0)
    t0 = time.time()
    try:
        run, _, info = captioner(s, a.snap, a.tok)
    except LoadFail as e:
        return write_loadfail(a.out.parent, a.sid, e)
    preds, retried = {}, []
    with torch.inference_mode():
        for i, f, h in rows:
            p = a.images / f
            if sha_file(p) != h:
                raise SystemExit(f"STOP: image {f} differs from the list")
            preds[i] = run(open_rgb(p, retried))[0]
    tmp = a.out.with_suffix(".partial")
    tmp.write_text(json.dumps(preds, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, a.out)
    prov = {"sid": a.sid, "hf": s["hf"], "rev": s["rev"], "set": s["set"], "n": len(preds),
            "seconds": round(time.time() - t0), "gpu": torch.cuda.get_device_name(0), "torch": torch.__version__,
            "transformers": transformers.__version__, "preds_sha256": sha_file(a.out),
            "unexpected_keys": info.get("unexpected_keys", 0), "truncated_retried": retried,
            "prereg": "manuscript/prereg/2026-10-28_b2_external/PREREG.md"}
    (a.out.parent / f"{a.sid}.prov.json").write_text(json.dumps(prov, indent=1))
    print(f"decoded {a.sid}: {len(preds)} images")
    return 0


def open_rgb(p: Path, retried: list) -> "Image.Image":
    """Strict decode; only the 3 OpenViIC files truncated in the release (C's CC-082 T6 list) are retried once with
    PIL LOAD_TRUNCATED_IMAGES set and reset around the call (B-2 Amendment 2). Any other failure stops the job."""
    from PIL import Image, ImageFile

    if ImageFile.LOAD_TRUNCATED_IMAGES:
        raise SystemExit("STOP: LOAD_TRUNCATED_IMAGES is set outside a T6 retry")
    try:
        with Image.open(p) as im:
            return im.convert("RGB")
    except OSError:
        if p.name not in TRUNC:
            raise
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    try:
        with Image.open(p) as im:
            out = im.convert("RGB")
    finally:
        ImageFile.LOAD_TRUNCATED_IMAGES = False
    retried.append(p.name)
    return out


# ------------------------------------------------------------------------------------------------- score (CPU)
def kit():
    sys.path[:0] = [str(ROOT / "scripts/kit_b"), str(ROOT)]
    import b2_controls as BC
    import ptb_protocol as PT
    from ptb_protocol import E4
    return E4, PT, BC


def post(c: str) -> tuple[str, bool]:
    """Registered post-processing for every system: underscores to spaces (counted), whitespace collapsed."""
    return " ".join(c.replace("_", " ").split()), "_" in c


def score_set(refs: dict[str, list[str]], systems: dict[str, dict[str, str]], twins: set[str] = frozenset()) -> dict:
    """The kit-B protocol columns for every system on one test set (one RDR pass)."""
    import numpy as np
    from pyvi import ViTokenizer

    E4, PT, _ = kit()
    ids = sorted(refs)
    hyp = {k: {i: post(v[i]) for i in ids} for k, v in systems.items()}
    flat = [r for i in ids for r in refs[i]] + [hyp[k][i][0] for k in systems for i in ids]
    it = iter([x.lower() for x in E4.rdr(flat)])
    rseg = {i: [next(it) for _ in refs[i]] for i in ids}
    hseg = {k: {i: next(it) for i in ids} for k in systems}
    pv = lambda t: ViTokenizer.tokenize(t).lower()  # noqa: E731
    R = {"P0": rseg, "P0s": rseg, "PTB": {i: [PT.ptb(r) for r in rseg[i]] for i in ids},
         "SYL": {i: [r.strip().lower() for r in refs[i]] for i in ids},
         "PYVI": {i: [pv(r) for r in refs[i]] for i in ids}}
    sc = {p: E4.Cider(R[p]) for p in R}
    boot = np.random.default_rng(0).integers(0, len(ids), (2000, len(ids)))
    keep = np.array([i not in twins for i in ids])
    out = {}
    for k in systems:
        H = {"P0": hseg[k], "P0s": {i: PT.variants(hseg[k][i])["strip"] for i in ids},
             "PTB": {i: PT.ptb(hseg[k][i]) for i in ids},
             "SYL": {i: hyp[k][i][0].strip().lower() for i in ids}, "PYVI": {i: pv(hyp[k][i][0]) for i in ids}}
        row = {"n": len(ids), "underscore_captions": sum(hyp[k][i][1] for i in ids),
               "empty": sum(not hyp[k][i][0] for i in ids),
               "end_punct_share": round(sum(bool(hseg[k][i].split()) and PT.is_punct_tok(hseg[k][i].split()[-1])
                                            for i in ids) / len(ids), 4),
               **{f"tok_{x}": v for x, v in PT.token_counts([hseg[k][i] for i in ids]).items()}}
        for p in R:
            per = sc[p].per_image(H[p])
            row[f"CIDEr_{p}"] = round(float(per.mean()), 2)
            if p in ("P0", "PTB"):
                lo, hi = np.percentile(per[boot].mean(1), [2.5, 97.5])
                row[f"CIDEr_{p}_ci95"] = [round(float(lo), 2), round(float(hi), 2)]
                row[f"BLEU4_{p}"] = round(E4.bleu4(R[p], H[p]), 2)
                row[f"ROUGEL_{p}"] = round(E4.rouge_l(R[p], H[p]), 2)
                if twins and not keep.all():
                    row[f"CIDEr_{p}_minus_twins"] = round(float(per[keep].mean()), 2)
        out[k] = row
    return out


THESIS_EXPECT = {"CIDEr_P0": "P0_official_rdr", "CIDEr_SYL": "P1_syllable_raw(evaluate.py --also-syllable)",
                 "CIDEr_PYVI": "P3_pyvi_word"}


def scorer_gate(data: Path, thesis: Path, pilot: Path) -> dict:
    """The kit reproduces pilot_repro.json (f272d4b8) on the two published KTVIC baselines (not counted, not new)."""
    _, _, BC = kit()
    refs, _ = load_refs("ktvic", data)
    preds = {}
    for name, (rel, blob) in BC.THESIS["files"].items():
        p = thesis / Path(rel).name
        if git_blob(p.read_bytes()) != blob:
            raise SystemExit(f"STOP: {p} blob differs from thesis-code 1a8d105")
        preds[name] = {str(r["image_id"]): r["caption"] for r in json.loads(p.read_text(encoding="utf-8"))}
    got = score_set(refs, preds)
    want = json.loads(pilot.read_text())["protocols"]
    bad = [(n, c) for n in preds for c, proto in THESIS_EXPECT.items() if got[n][c] != want[proto]["CIDEr"][n]]
    bad += [(n, m) for n in preds for m, key in (("BLEU4_P0", "BLEU-4"), ("ROUGEL_P0", "ROUGE-L"))
            if got[n][m] != want["P0_official_rdr"][key][n]]
    if bad:
        raise SystemExit(f"STOP: scorer gate, the kit does not reproduce pilot_repro.json: {bad}")
    return {"pilot_repro_sha256": sha_file(pilot), "reproduced": sorted(THESIS_EXPECT) + ["BLEU4_P0", "ROUGEL_P0"]}


COLS = ("n", "CIDEr_P0", "CIDEr_P0_ci95", "BLEU4_P0", "ROUGEL_P0", "CIDEr_P0s", "CIDEr_PTB", "CIDEr_PTB_ci95",
        "BLEU4_PTB", "CIDEr_SYL", "CIDEr_PYVI", "end_punct_share", "tok_ptb_removed_tokens", "underscore_captions",
        "CIDEr_P0_minus_twins", "CIDEr_PTB_minus_twins")
SIGNATURE = "kitB|seg:rdr-1.2@9e2811cd|cider:D|scale:x100|punct:{as-written,final-stripped,ptb-removed}|refs:all"


def table(rows: dict, gate: dict, loadfail: dict, not_run: dict | None = None) -> str:
    """Descriptive table: rows by stable id, no rank, no group system, no comparison column."""
    head = ("**B-2 external systems (DESCRIPTIVE; CC-126 W13). No verdict, no ranking, not compared with the group's "
            f"registered numbers.** Protocol: `{SIGNATURE}`.\n\n| id | system | source | test set | licence | "
            + " | ".join(COLS) + " |\n|" + "---|" * (5 + len(COLS)) + "\n")
    body = []
    for key in sorted(rows):
        s = SYSTEMS[key.split(":")[0]]
        lic = s["licence"] if s["licence"] in PERMISSIVE else f"{s['licence'] or 'none'} (aggregates only; permission not obtained)"
        vals = [str(rows[key].get(c, "")) for c in COLS]
        body.append(f"| {key} | {s['name']} | {s['source']} | {s['set']} test | {lic} | " + " | ".join(vals) + " |")
    notes = [f"- {k}: excluded by the structure gate ({r['reason']})" for k, r in sorted(gate.items()) if not r["pass"]]
    notes += [f"- {k}: not loadable under the registered recipe (transformers 4.57.6): {r}"
              for k, r in sorted(loadfail.items())]
    notes += [f"- {k}: {r}" for k, r in sorted((not_run or {}).items())]
    twins = [k for k in rows if SYSTEMS[k.split(":")[0]]["ktvic_train"]]
    if twins:
        notes.append(f"- {', '.join(sorted(twins))}: trained on KTVIC train, which holds byte twins of KTVIC test "
                     "images 1335 (= train 3589) and 507 (= train 7511); the `_minus_twins` columns drop them (CC-130).")
    return head + "\n".join(body) + "\n\n" + "\n".join(notes) + "\n"


def counts(rows: dict) -> dict:
    sids = {k.split(":")[0] for k in rows}
    srcs = {SYSTEMS[s]["source"] for s in sids}
    return {"external_systems": len(sids), "distinct_sources": len(srcs),
            "w13_validated_sentence_allowed": len(sids) >= 3 and len(srcs) >= 3}  # CC-132 W4


def log_line(rows: dict, scores_sha: str) -> str:
    kt = sorted({k.split(":")[0] for k in rows if SYSTEMS[k.split(":")[0]]["set"] == "ktvic"})
    return (f"B2-LOOK | {time.strftime('%FT%TZ', time.gmtime())} | systems scored: {', '.join(sorted(rows))} | "
            f"KTVIC-test one look of {', '.join(kt) or 'none'} | scores.json {scores_sha}")


def cmd_score(a) -> None:
    if (a.out / "scores.json").exists():
        raise SystemExit("REFUSED: scores.json exists (one look per system)")
    sg = scorer_gate(a.data, a.thesis, a.pilot)
    gate = json.loads(a.gate.read_text())
    regate, apreds = gate_all(a.fetched, a.data)
    if regate != gate:
        raise SystemExit("STOP: the fetched files no longer give gate.json (drift since the gate)")
    by_set: dict[str, dict] = {}
    for k, p in apreds.items():
        if gate[k]["pass"] and p:
            by_set.setdefault(SYSTEMS[k.split(":")[0]]["set"], {})[k] = p
    loadfail, smokefail = {}, {}
    for s in B_SYSTEMS:
        f = a.preds / f"{s['sid']}.preds.json"
        lf = a.preds / f"{s['sid']}.LOADFAIL.json"
        if f.is_file():
            by_set.setdefault(s["set"], {})[s["sid"]] = json.loads(f.read_text(encoding="utf-8"))
        elif lf.is_file():
            loadfail[s["sid"]] = json.loads(lf.read_text())["reason"]
        elif (a.preds / f"{s['sid']}.SMOKEFAIL.json").is_file():
            smokefail[s["sid"]] = NOT_RUNNABLE  # B-2 Amendment 1, CC-138 W3 (c)
    stop = "not run (cap)" if (a.preds.parent / "CAP_STOP.json").exists() else "not run (JOB STOP)"
    not_run = {s["sid"]: stop for s in B_SYSTEMS if s["sid"] not in loadfail and s["sid"] not in smokefail
               and not (a.preds / f"{s['sid']}.preds.json").is_file()}
    rows = {}
    for name, systems in sorted(by_set.items()):
        refs, _ = load_refs(name, a.data)
        rows.update(score_set(refs, systems, TWINS_TEST if name == "ktvic" else frozenset()))
    a.out.mkdir(parents=True, exist_ok=True)
    looks = [{"sid": k, "set": SYSTEMS[k.split(":")[0]]["set"], "utc": time.strftime("%FT%TZ", time.gmtime())}
             for k in sorted(rows)]
    res = {"label": "DESCRIPTIVE B-2 (CC-126 W13)", "signature": SIGNATURE, "scorer_gate": sg, "rows": rows,
           "looks": looks, "loadfail": loadfail, "smokefail": smokefail, "not_run": not_run, **counts(rows),
           "code_sha256": sha_file(Path(__file__))}
    (a.out / "scores.json").write_text(json.dumps(res, indent=1))
    (a.out / "table.md").write_text(table(rows, gate, loadfail, {**smokefail, **not_run}), encoding="utf-8")
    print(json.dumps(counts(rows)))
    print(log_line(rows, sha_file(a.out / "scores.json")))  # the operator appends it to LOG.md (CC-132 W6)


# --------------------------------------------------------------------------------------------------- selftest
def _st_gate(t: Path, refs: dict, alias: dict) -> None:
    """Parser and every gate reason; no caption reaches a gate record."""
    (t / "a.json").write_text(json.dumps([{"image_id": i, "caption": f"mèo_con {i}."} for i in (1, 2, 3)]))
    (t / "b.json").write_text(json.dumps({"00001.jpg": ["x"], "2": {"pred": "y"}, "3": "z"}))
    (t / "c.txt").write_text("1.jpg\tmột câu\n2.jpg\thai\n3.jpg\tba, bốn\n")
    (t / "d.json").write_text(json.dumps([{"image_id": i, "caption": "q"} for i in (1, 2)]))
    (t / "e.json").write_text(json.dumps([{"image_id": i, "caption": "q"} for i in (1, 2, 3, 3)]))
    (t / "f.json").write_text(json.dumps({i: refs[i][0] for i in refs}))
    (t / "g.json").write_text(json.dumps([[1, "q"], [2, "q"], [3, "q"]]))
    (t / "h.json").write_text(json.dumps({"1": "q", "2": "q", "9": "q"}))
    (t / "l.json").write_text(json.dumps([{"image_id": i, "caption": "q", "pred": "r"} for i in (1, 2, 3)]))
    (t / "m.csv").write_text("image_id,caption\n1.jpg,một, hai\n2.jpg hai ba\n3.jpg\tba\n")
    (t / "n.json").write_text(json.dumps({"1": "Con mèo, ngồi trên ghế!", "2": "q", "3": "q"}))
    (t / "o.json").write_text(json.dumps({"1": "q", "2": "Chó... chạy", "3": "xe - đỏ"}))
    import openpyxl
    wb = openpyxl.Workbook()
    wb.active.append(["Image", "Caption"])
    for i in (1, 2, 3):
        wb.active.append([f"{i:05d}.jpg", "w"])
    wb.save(t / "i.xlsx")
    (t / "j.xlsx").write_bytes(b"")
    wb2 = openpyxl.Workbook()
    wb2.active.append(["metric", "value"])
    wb2.active.append(["BLEU-4", 0.2])
    wb2.save(t / "k.xlsx")
    want = {"a": "ok", "b": "ok", "c": "ok", "d": "not the official test id set", "e": "duplicate ids",
            "f": "looks like references", "g": "unparseable (KeyError)", "h": "unknown ids", "i": "ok",
            "k": "unparseable (StopIteration)", "l": "ambiguous caption field", "m": "ok", "n": "ok",
            "o": "looks like references"}
    ext = {"i": "xlsx", "k": "xlsx", "c": "txt", "m": "csv"}
    for k, w in want.items():
        r, p = gate_file(t / f"{k}.{ext.get(k, 'json')}", refs, alias)
        assert r["reason"] == w, (k, r)
        assert r["pass"] == (w == "ok") and bool(p) == (w == "ok"), k
        assert "mèo" not in json.dumps(r, ensure_ascii=False), "a caption leaked into a gate record"
    r, _ = gate_file(t / "j.xlsx", refs, alias)
    assert not r["pass"] and r["reason"].startswith("unparseable")
    r, p = gate_file(t / "c.txt", refs, alias)
    assert p["3"] == "ba, bốn"
    r, p = gate_file(t / "m.csv", refs, alias)
    assert p["1"] == "một, hai" and p["2"] == "hai ba" and r["rows"] == 3


def _st_score_table(refs: dict) -> None:
    """Protocol columns, twins column, table without rank or caption, counts, the LOG line."""
    # scoring: identical hyps score the maximum, underscores counted, twin column only when asked
    sysd = {"S": {"1": "con_mèo ngồi trên ghế", "2": "chó chạy", "3": "xe đỏ."}, "T": {i: "" for i in refs}}
    rows = score_set(refs, sysd, twins={"3"})
    assert rows["S"]["underscore_captions"] == 1 and rows["T"]["empty"] == 3
    assert rows["S"]["CIDEr_P0"] > rows["T"]["CIDEr_P0"] == 0.0
    assert rows["S"]["tok_ptb_removed_tokens"] == 1 and rows["S"]["CIDEr_PTB"] >= rows["S"]["CIDEr_P0"]
    assert "CIDEr_P0_minus_twins" in rows["S"] and "CIDEr_P0_minus_twins" not in score_set(refs, sysd)["S"]
    assert rows["S"]["end_punct_share"] == round(1 / 3, 4)
    # table and counts: no rank column, rows by id, no caption, licence flags, twins note
    rows2 = {"X2": rows["S"], "K1": rows["T"], "X3:uit_viic_original_pred": rows["S"]}
    md = table(rows2, {"X1": {"pass": False, "reason": "unknown ids"}}, {"K6": "OSError"})
    assert "| rank" not in md.lower() and md.index("| K1 |") < md.index("| X2 |") < md.index("| X3:")
    assert "mèo" not in md and "permission not obtained" in md and "1335" in md
    assert "not loadable under the registered recipe" in md
    assert "| K5 |" not in table(rows2, {}, {}, {"K5": "not run (cap)"}) and "K5: not run (cap)" in table(
        rows2, {}, {}, {"K5": "not run (cap)"})
    assert counts(rows2) == {"external_systems": 3, "distinct_sources": 3, "w13_validated_sentence_allowed": True}
    c = counts({"X4a": 1, "X4b": 1, "X4c": 1})
    assert c["distinct_sources"] == 1 and not c["w13_validated_sentence_allowed"]
    line = log_line({"K1": 1, "X1": 1}, "ab" * 32)
    assert "KTVIC-test one look of K1" in line and "B2-LOOK" in line


def _st_cap(t: Path) -> None:
    """Cap and lock arithmetic."""
    # cap and lock arithmetic
    used, mark = t / "gpu.tsv", t / "CAP"
    assert left(used, mark) == HARD_S
    used.write_text(f"a {SOFT_S - 1}\n")
    assert left(used, mark) == HARD_S - SOFT_S + 1
    used.write_text(f"a {SOFT_S}\n")
    assert left(used, mark) == 0
    used.write_text("a start 100\nb start 400\n")
    assert used_seconds(used, now=1000) == 900
    mark.write_text("{}")
    assert left(t / "none", mark) == 0
    (t / "o/x").mkdir(parents=True)
    (t / "o/x/RUNNING").write_text("")
    bad = isolation(t / "o", names=["cen_test", "b2"], tmux="")
    assert len(bad) == 3 and isolation(t / "none", names=[], tmux="1") == []


def _st_load() -> None:
    """Pins and the load rule: only registered calls and artifact checks become LoadFail."""
    import tempfile

    assert [s["sid"] for s in B_SYSTEMS] == ["K5", "K1", "K6"] and len(SYSTEMS) == len(A_SYSTEMS) + len(B_SYSTEMS)
    assert all(len(p) in (40, 64) for s in SYSTEMS.values() for p in s["files"].values())
    assert all(len(s.get("commit") or s.get("rev")) == 40 for s in SYSTEMS.values())
    # load rule: only registered calls and artifact checks become LoadFail
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "tokenizer_config.json").write_text(json.dumps({"tokenizer_class": "PhobertTokenizer"}))
        for name, ok in (("PhobertTokenizer", True), ("PhobertTokenizerFast", True), ("BertTokenizer", False)):
            try:
                declared_class(type(name, (), {})(), Path(td))
                assert ok, name
            except LoadFail:
                assert not ok, name
    try:
        pretrained(lambda: 1 / 0)
        raise AssertionError("pretrained did not wrap")
    except LoadFail as e:
        assert "ZeroDivisionError" in str(e)
    assert canon("Một  người_đàn ông.") == "một người đàn ông" == canon("một, người đàn... ông!")
    info: dict = {}
    assert load_model(lambda *_, **k: ("m", {"missing_keys": [], "unexpected_keys": ["x", "y"]}), Path("."), info) == "m"
    assert info["unexpected_keys"] == 2
    try:
        load_model(lambda *_, **k: ("m", {"missing_keys": ["w"]}), Path("."), info)
        raise AssertionError("missing weights did not raise")
    except LoadFail as e:
        assert "1 weights missing" in str(e)


def _st_smoke() -> None:
    """CC-138 W3 branches on synthetic token lists; W1 counts carry no text; the SMOKEFAIL note in the table."""
    end, special = {2}, {0, 1, 2, 3, 7}  # 2 = eos, 1 = pad or <|im_end|>-like, 0 = bos, 3 = unk, 7 = <image>-like
    assert new_tokens([2, 0, 11, 12, 2], start={2}, bos={0}) == [11, 12, 2]  # BART-shaped: start, bos, text, eos
    assert new_tokens([2, 2], start={2}, bos={0}) == [2] and new_tokens([11, 2]) == [11, 2]
    assert smoke_class([11, 12, 2], "x y", end, special) == ("text", "")  # (d)
    assert smoke_class([2], "", end, special) == ("eos", "")  # (c) on one input
    assert smoke_class([11, 2], "", end, special)[1].startswith("(a)")
    assert smoke_class([11, 2], "  ", end, special)[1].startswith("(a)")
    assert smoke_class([7, 2], "", end, special)[1].startswith("(b)") and smoke_class([0, 11], "x", end, special)[0] == "stop"
    assert smoke_class([1], "", end, special)[1].startswith("(b)")  # an immediate pad / <|im_end|> is ours, not (c)
    assert smoke_class([], "", end, special) == ("stop", "zero new tokens")
    assert smoke_verdict([("eos", ""), ("eos", "")]) == (5, NOT_RUNNABLE)  # (c) on both: rc 5
    assert smoke_verdict([("eos", ""), ("text", "")]) == (0, "ok") == smoke_verdict([("text", ""), ("eos", "")])
    assert smoke_verdict([("text", ""), ("stop", "(b) x")]) == (1, "(b) x")  # a bug wins over a pass
    c = smoke_counts([11, 12, 2], "mèo con", end, special)
    assert c == {"n_new_tokens": 3, "n_special_new": 1, "first_new_is_eos": False, "n_chars": 7}
    assert smoke_counts([2], "", end, special)["first_new_is_eos"] and "mèo" not in json.dumps(c, ensure_ascii=False)
    assert _ids(2, [3, 4], None) == {2, 3, 4}
    assert f"K5: {NOT_RUNNABLE}" in table({}, {}, {}, {"K5": NOT_RUNNABLE})
    assert len(SMOKE_IMG["sha256"]) == 64 and SMOKE_IMG["file"] == f"{SMOKE_IMG['id']:012d}.jpg"
    assert SMOKE_IMG["url"].endswith("/train2017/" + SMOKE_IMG["file"])


def _st_trunc(t: Path) -> None:
    """Amendment 2: only a TRUNC-named truncated file is retried, the flag is reset, anything else still raises."""
    import io

    from PIL import Image, ImageFile

    buf = io.BytesIO()
    Image.new("RGB", (64, 64), (200, 10, 10)).save(buf, "JPEG")
    cut = buf.getvalue()[:-40]
    ok, named, other = t / "ok.jpg", t / "00000000768.jpg", t / "other.jpg"
    buf.seek(0)
    ok.write_bytes(buf.getvalue())
    named.write_bytes(cut)
    other.write_bytes(cut)
    retried: list = []
    assert open_rgb(ok, retried).size == (64, 64) and retried == []
    assert open_rgb(named, retried).size == (64, 64) and retried == ["00000000768.jpg"]
    assert not ImageFile.LOAD_TRUNCATED_IMAGES
    try:
        open_rgb(other, retried)
        raise AssertionError("an unnamed truncated file must stop")
    except OSError:
        pass
    assert retried == ["00000000768.jpg"] and not ImageFile.LOAD_TRUNCATED_IMAGES


def selftest() -> None:
    import tempfile

    E4, _, _ = kit()
    E4.rdr = lambda texts: [" ".join(re.sub(r"([^\w\s])", r" \1 ", t).split()) for t in texts]  # synthetic: whitespace segmentation, no java
    assert norm_id("imgs/000000000123.jpg") == "123" and norm_id(" 7 ") == "7" and norm_id("a_b.png") == "a_b"
    assert git_blob(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
    refs = {"1": ["con mèo ngồi trên ghế", "một con mèo"], "2": ["chó chạy", "con chó chạy trên cỏ"],
            "3": ["xe đỏ", "chiếc xe màu đỏ"]}
    alias = {"1": "1", "2": "2", "3": "3"}
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        _st_gate(t, refs, alias)
        _st_cap(t)
        _st_smoke()
        _st_trunc(t)
    _st_score_table(refs)
    _st_load()
    print("selftest ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    P = lambda *n: [sub.add_parser(x) for x in n]  # noqa: E731
    fe, ga, li, hf, ui, gu, le, sm, de, sc, sf = P("fetch", "gate", "lists", "hf-fetch", "uit-fetch", "guard", "left",
                                                   "smoke", "decode", "score", "smoke-fetch")
    sf.add_argument("--dest", type=Path, required=True)
    fe.add_argument("--out", type=Path, required=True)
    for p in (ga, sc):
        p.add_argument("--fetched", type=Path, required=True)
    for p in (ga, li, sc):
        p.add_argument("--data", type=Path, required=True)
    ga.add_argument("--out", type=Path, required=True)
    li.add_argument("--cen", type=Path, required=True)
    li.add_argument("--out", type=Path, required=True)
    hf.add_argument("--sid", choices=[s["sid"] for s in B_SYSTEMS], required=True)
    hf.add_argument("--dest", type=Path, required=True)
    ui.add_argument("--list", type=Path, required=True)
    ui.add_argument("--dest", type=Path, required=True)
    gu.add_argument("--head", required=True)
    le.add_argument("--used", type=Path, required=True)
    le.add_argument("--marker", type=Path, required=True)
    for p, ks in ((sm, ("snap", "img2", "out")), (de, ("snap", "images", "list", "out"))):
        p.add_argument("--sid", choices=[s["sid"] for s in B_SYSTEMS], required=True)
        for k in ks:
            p.add_argument(f"--{k}", type=Path, required=True)
        p.add_argument("--tok", type=Path)
    for k in ("gate", "preds", "vnc", "thesis", "pilot", "out"):
        sc.add_argument(f"--{k}", type=Path, required=True)
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    if a.cmd == "score":
        E4, _, _ = kit()
        if sha_file(a.vnc / "VnCoreNLP-1.2.jar") != "9e2811cdbc2ddfc71d04be5dc36e185c88dcd1ad4d5d69e4ff2e1369dccf7793":
            raise SystemExit("STOP: VnCoreNLP jar differs from 9e2811cd")
        E4.VNC = a.vnc
    if a.cmd == "left":
        print(left(a.used, a.marker))
        return 0
    if a.cmd == "guard":
        guard(a.head)
        print("guard ok")
        return 0
    fn = {"fetch": cmd_fetch, "gate": cmd_gate, "lists": cmd_lists, "hf-fetch": cmd_hf_fetch,
          "uit-fetch": cmd_uit_fetch, "smoke-fetch": cmd_smoke_fetch, "smoke": cmd_smoke, "decode": cmd_decode, "score": cmd_score}.get(a.cmd)
    if fn is None:
        ap.error("a subcommand or --selftest is required")
    return fn(a) or 0


if __name__ == "__main__":
    sys.exit(main())
