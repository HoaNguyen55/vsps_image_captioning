#!/usr/bin/env python3
"""Local Operator Image Staging Script for DrivingVQA Pilot (CC-104 F5 & REVIEW_KEN_BATCH8 W3).

Runs on the operator's local staging workstation BEFORE copying `/root/dvqa_pilot` to M4:
  1. Pins Hugging Face dataset repo `EPFL-DrivingVQA/DrivingVQA` at revision
     `02ce870cfe037b93cc034034cd747a7eecdd455c`.
  2. Downloads `train.json` (sha256 `4a204e3f...`) ONLY via
     `huggingface_hub.hf_hub_download(..., filename="train.json", revision=...)`.
     `snapshot_download` is STRICTLY FORBIDDEN because the repository root contains `test.json`.
  3. Primary staging mode (`--mode range`, default per REVIEW_KEN_BATCH8 W3a):
     Reads ONLY the ZIP End-of-Central-Directory + Central Directory of `images.zip`
     (`826,036,403` bytes, LFS sha256 `fcf5111b...`) via HTTP Range requests, and then fetches
     ONLY the 1,000 byte ranges for the 1,000 `img_filename` entries listed in
     `manuscript/ken/drivingvqa_dev1000_ids.tsv` (sha256 `636e0477...`), verifying every extracted
     file against `manuscript/ken/dvqa_dev1000_image_sha256.tsv` (sha256 `ddc41513...`) and against
     all 8,179 forbidden test image SHA-256s. Thus NO test image bytes are ever downloaded.
  4. Optional fallback (`--from-local-zip`): extracts only the 1,000 listed entries from a local zip
     and deletes the zip in a `finally:` block.

Usage:
  python3 scripts/ken_dvqa_pilot/stage_images.py --selftest
  python3 scripts/ken_dvqa_pilot/stage_images.py --dest-dir /tmp/dvqa_pilot_stage
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import struct
from pathlib import Path
import sys
import tempfile
from typing import Callable
import urllib.request
import zipfile
import zlib

HERE = Path(__file__).resolve().parent
ROOT = next(
    (p for p in HERE.parents if (p / "manuscript/prereg/2026-10-22_c_stage1/lists.json").exists()),
    HERE.parents[2],
)
sys.path.insert(0, str(HERE))
import host_check as HC  # noqa: E402

HF_DATASET_REPO = "EPFL-DrivingVQA/DrivingVQA"
HF_DATASET_REVISION = "02ce870cfe037b93cc034034cd747a7eecdd455c"
HF_IMAGES_ZIP_RESOLVE_URL = (
    f"https://huggingface.co/datasets/{HF_DATASET_REPO}/resolve/{HF_DATASET_REVISION}/images.zip"
)
TRAIN_JSON_SHA256 = "4a204e3fa7516db313ceeb91ac989919979e31da20e484bc5f4018c261bd483d"
IMAGES_ZIP_LFS_SHA256 = "fcf5111beba0af64cd444a664e3bdcd46ed2aed05f26ec584f181208dd57c60a"
IMAGES_ZIP_SIZE_BYTES = 826036403
DEV1000_IMAGE_SHA256_TSV = ROOT / "manuscript/ken/dvqa_dev1000_image_sha256.tsv"
DEV1000_IMAGE_SHA256_TSV_PIN = "ddc41513f02d5171fedc1a86146f9c708f87e09d7e88ddde83434bb7f1ef3289"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pinned_image_sha256_map(manifest_path: Path = DEV1000_IMAGE_SHA256_TSV) -> dict[str, str]:
    if not manifest_path.is_file():
        raise SystemExit(f"REFUSED: missing per-image SHA-256 manifest {manifest_path}")
    if sha256_file(manifest_path) != DEV1000_IMAGE_SHA256_TSV_PIN:
        raise SystemExit(f"REFUSED: SHA-256 mismatch for {manifest_path}")
    out: dict[str, str] = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            raise SystemExit(f"REFUSED: malformed row in {manifest_path}: {line}")
        out[parts[0].strip()] = parts[1].strip()
    if len(out) != 1000:
        raise SystemExit(f"REFUSED: expected 1,000 rows in {manifest_path}, got {len(out)}")
    return out


def http_fetch_byte_range(url: str, start: int, end_inclusive: int, timeout: int = 60) -> bytes:
    """Fetch inclusive byte range [start, end_inclusive] via HTTP Range header."""
    req = urllib.request.Request(
        url,
        headers={
            "Range": f"bytes={start}-{end_inclusive}",
            "User-Agent": "vsps-dvqa-operator-stage/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    expected_len = end_inclusive - start + 1
    if len(data) != expected_len:
        raise SystemExit(f"REFUSED: HTTP Range {start}-{end_inclusive} returned {len(data)} bytes != {expected_len}")
    return data


def extract_listed_images_via_range_fn(
    total_size: int,
    fetch_range: Callable[[int, int], bytes],
    dest_dvqa_dir: Path,
    expected_sha_map: dict[str, str],
    forbidden_shas: set[str],
) -> dict:
    """REVIEW_KEN_BATCH8 W3a: Read ONLY the Central Directory and the exact listed entries in `expected_sha_map`
    via `fetch_range(start, end_inclusive)`, without ever reading unlisted (test) entries."""
    tail_len = min(total_size, 65557)
    tail_start = total_size - tail_len
    tail = fetch_range(tail_start, total_size - 1)
    eocd_pos = tail.rfind(b"PK\x05\x06")
    if eocd_pos < 0:
        raise SystemExit("REFUSED: ZIP End-of-Central-Directory signature not found")
    _sig, _disk, _cd_disk, _entries_disk, total_entries, cd_size, cd_offset, _comment_len = struct.unpack(
        "<4sHHHHIIH", tail[eocd_pos : eocd_pos + 22]
    )

    cd_bytes = fetch_range(cd_offset, cd_offset + cd_size - 1)
    pos = 0
    cd_entries: dict[str, tuple[int, int, int, int]] = {}
    for _ in range(total_entries):
        if pos + 46 > len(cd_bytes) or cd_bytes[pos : pos + 4] != b"PK\x01\x02":
            raise SystemExit("REFUSED: malformed ZIP Central Directory header")
        (
            _csig,
            _ver_made,
            _ver_need,
            _flags,
            comp_method,
            _mod_time,
            _mod_date,
            _crc32,
            comp_size,
            uncomp_size,
            name_len,
            extra_len,
            comment_len,
            _disk_start,
            _int_attr,
            _ext_attr,
            local_header_offset,
        ) = struct.unpack("<4sHHHHHHIIIHHHHHII", cd_bytes[pos : pos + 46])
        name_bytes = cd_bytes[pos + 46 : pos + 46 + name_len]
        name = name_bytes.decode("utf-8", errors="replace")
        if name in expected_sha_map:
            cd_entries[name] = (local_header_offset, comp_size, uncomp_size, comp_method)
        pos += 46 + name_len + extra_len + comment_len

    missing_in_cd = sorted(set(expected_sha_map.keys()) - set(cd_entries.keys()))
    if missing_in_cd:
        raise SystemExit(f"REFUSED: {len(missing_in_cd)} expected entries missing from ZIP CD: {missing_in_cd[:3]}")

    img_dir = dest_dvqa_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    extracted_shas: dict[str, str] = {}
    total_payload_bytes_fetched = 0

    for rel_path, exp_sha in sorted(expected_sha_map.items()):
        lh_off, comp_size, uncomp_size, comp_method = cd_entries[rel_path]
        # Fetch local file header (30 bytes + name + up to 256 extra bytes) + compressed payload in one Range call
        span_end = min(total_size - 1, lh_off + 30 + len(rel_path.encode("utf-8")) + 256 + comp_size - 1)
        chunk = fetch_range(lh_off, span_end)
        total_payload_bytes_fetched += len(chunk)
        if len(chunk) < 30 or chunk[:4] != b"PK\x03\x04":
            raise SystemExit(f"REFUSED: invalid ZIP local file header for {rel_path}")
        lf_name_len, lf_extra_len = struct.unpack("<HH", chunk[26:30])
        data_start = 30 + lf_name_len + lf_extra_len
        data_end = data_start + comp_size
        if data_end > len(chunk):
            chunk = fetch_range(lh_off, lh_off + data_end - 1)
        comp_payload = chunk[data_start:data_end]
        if comp_method == 0:
            raw_bytes = comp_payload
        elif comp_method == 8:
            raw_bytes = zlib.decompress(comp_payload, -15)
        else:
            raise SystemExit(f"REFUSED: unsupported ZIP compression method {comp_method} for {rel_path}")
        if len(raw_bytes) != uncomp_size:
            raise SystemExit(f"REFUSED: uncompressed size mismatch for {rel_path}")

        got_sha = hashlib.sha256(raw_bytes).hexdigest()
        if got_sha != exp_sha:
            raise SystemExit(f"REFUSED: per-image SHA-256 mismatch for {rel_path}: got {got_sha}, expected {exp_sha}")
        if got_sha in forbidden_shas:
            raise SystemExit(f"REFUSED: {rel_path} SHA-256 {got_sha} is in forbidden test set")

        out_file = dest_dvqa_dir / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_bytes(raw_bytes)
        extracted_shas[rel_path] = got_sha

    return {
        "mode": "http_range",
        "extracted_count": len(extracted_shas),
        "distinct_sha256_count": len(set(extracted_shas.values())),
        "total_cd_entries_scanned": int(total_entries),
        "total_payload_bytes_fetched": int(total_payload_bytes_fetched),
        "dest_dvqa_dir": dest_dvqa_dir.as_posix(),
    }


def extract_listed_images_from_zip(
    zip_path: Path,
    dest_dvqa_dir: Path,
    expected_sha_map: dict[str, str],
    forbidden_shas: set[str],
    verify_zip_sha: bool = True,
    delete_zip_after: bool = True,
) -> dict:
    """Fallback local-zip extractor: extracts ONLY `expected_sha_map` and deletes `zip_path` in `finally:`."""
    try:
        if not zip_path.is_file():
            raise SystemExit(f"REFUSED: missing zip archive {zip_path}")
        if verify_zip_sha:
            got_zip_sha = sha256_file(zip_path)
            if got_zip_sha != IMAGES_ZIP_LFS_SHA256:
                raise SystemExit(
                    f"REFUSED: images.zip SHA-256 mismatch: got {got_zip_sha}, expected {IMAGES_ZIP_LFS_SHA256}"
                )

        img_dir = dest_dvqa_dir / "images"
        img_dir.mkdir(parents=True, exist_ok=True)

        extracted_shas: dict[str, str] = {}
        with zipfile.ZipFile(zip_path, "r") as zf:
            names_in_zip = set(zf.namelist())
            for rel_path, exp_sha in sorted(expected_sha_map.items()):
                if rel_path not in names_in_zip:
                    raise SystemExit(f"REFUSED: expected entry {rel_path} missing from {zip_path}")
                data = zf.read(rel_path)
                got_sha = hashlib.sha256(data).hexdigest()
                if got_sha != exp_sha:
                    raise SystemExit(
                        f"REFUSED: per-image SHA-256 mismatch for {rel_path}: got {got_sha}, expected {exp_sha}"
                    )
                if got_sha in forbidden_shas:
                    raise SystemExit(f"REFUSED: {rel_path} SHA-256 {got_sha} is in forbidden test set")
                out_file = dest_dvqa_dir / rel_path
                out_file.parent.mkdir(parents=True, exist_ok=True)
                out_file.write_bytes(data)
                extracted_shas[rel_path] = got_sha

        return {
            "mode": "local_zip_fallback",
            "extracted_count": len(extracted_shas),
            "distinct_sha256_count": len(set(extracted_shas.values())),
            "dest_dvqa_dir": dest_dvqa_dir.as_posix(),
        }
    finally:
        if delete_zip_after and zip_path.exists():
            zip_path.unlink()


def stage_from_hf(
    dest_dvqa_dir: Path,
    from_local_zip: Path | None = None,
    manifest_out: Path | None = None,
) -> dict:
    """Operator local staging entry point:
    - Downloads `train.json` via `hf_hub_download` ONLY (never `snapshot_download`, never `test.json`).
    - By default (`from_local_zip is None`), streams ONLY the 1,000 `dev1000` entries via HTTP Range from
      `HF_IMAGES_ZIP_RESOLVE_URL` so zero test images are ever downloaded (REVIEW_KEN_BATCH8 W3a).
    """
    from huggingface_hub import hf_hub_download

    HC.verify_repo_pins(ROOT)
    expected_sha_map = load_pinned_image_sha256_map(DEV1000_IMAGE_SHA256_TSV)
    forbidden_shas = HC.load_forbidden_sha256_set(ROOT)
    dest_dvqa_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="dvqa_stage_") as tmp_dl:
        tmp_dl_path = Path(tmp_dl)
        train_dl = Path(
            hf_hub_download(
                repo_id=HF_DATASET_REPO,
                repo_type="dataset",
                filename="train.json",
                revision=HF_DATASET_REVISION,
                local_dir=tmp_dl_path,
                cache_dir=tmp_dl_path / "hf_cache",
            )
        )
        if sha256_file(train_dl) != TRAIN_JSON_SHA256:
            raise SystemExit("REFUSED: downloaded train.json failed SHA-256 verification")
        shutil.copy2(train_dl, dest_dvqa_dir / "train.json")

        if from_local_zip is not None:
            res = extract_listed_images_from_zip(
                zip_path=from_local_zip,
                dest_dvqa_dir=dest_dvqa_dir,
                expected_sha_map=expected_sha_map,
                forbidden_shas=forbidden_shas,
                verify_zip_sha=True,
                delete_zip_after=True,
            )
        else:
            res = extract_listed_images_via_range_fn(
                total_size=IMAGES_ZIP_SIZE_BYTES,
                fetch_range=lambda s, e: http_fetch_byte_range(HF_IMAGES_ZIP_RESOLVE_URL, s, e),
                dest_dvqa_dir=dest_dvqa_dir,
                expected_sha_map=expected_sha_map,
                forbidden_shas=forbidden_shas,
            )

    if manifest_out is not None and manifest_out.resolve() != DEV1000_IMAGE_SHA256_TSV.resolve():
        shutil.copy2(DEV1000_IMAGE_SHA256_TSV, manifest_out)

    return {
        "status": "OK",
        "hf_dataset_repo": HF_DATASET_REPO,
        "hf_dataset_revision": HF_DATASET_REVISION,
        "train_json_sha256": TRAIN_JSON_SHA256,
        "images_zip_lfs_sha256": IMAGES_ZIP_LFS_SHA256,
        "dev1000_image_sha256_tsv_sha256": DEV1000_IMAGE_SHA256_TSV_PIN,
        **res,
    }


def selftest() -> None:
    import json

    HC.verify_repo_pins(ROOT)
    expected_rels = HC.load_expected_dev1000_images(ROOT)
    forbidden_shas = HC.load_forbidden_sha256_set(ROOT)
    pin_map = load_pinned_image_sha256_map(DEV1000_IMAGE_SHA256_TSV)

    # 1. Verify exact key match between drivingvqa_dev1000_ids.tsv and dvqa_dev1000_image_sha256.tsv
    assert sorted(pin_map.keys()) == expected_rels
    assert len(pin_map) == 1000
    # Upstream DrivingVQA has 999 distinct SHA-256s across the 1,000 dev1000 images (images/2754.jpg == images/2776.jpg)
    assert len(set(pin_map.values())) == 999
    assert pin_map["images/2754.jpg"] == pin_map["images/2776.jpg"]
    assert len(set(pin_map.values()) & forbidden_shas) == 0

    # 2. Test HTTP-Range selective extraction on an in-memory synthetic archive (>70 KB) containing 5 listed + 1 unlisted test entry
    sub_keys = expected_rels[:5]
    synth_map: dict[str, str] = {}
    unlisted_marker = b"UNLISTED_FORBIDDEN_TEST_IMAGE_PAYLOAD_" * 2000
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        zip_path = tmp_path / "images.zip"
        dest_range_dir = tmp_path / "dvqa_pilot_range"
        dest_zip_dir = tmp_path / "dvqa_pilot_zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            # Put a >70 KB uncompressed unlisted test entry FIRST in the zip so we prove the Range reader skips its byte range
            zf.writestr("images/9999_unlisted_test.jpg", unlisted_marker, compress_type=zipfile.ZIP_STORED)
            for k in sub_keys:
                payload = f"synth_bytes_for_{k}".encode("utf-8") * 8
                synth_map[k] = hashlib.sha256(payload).hexdigest()
                zf.writestr(k, payload, compress_type=zipfile.ZIP_DEFLATED)

        raw_zip_bytes = zip_path.read_bytes()
        fetched_chunks: list[bytes] = []

        def mock_fetch_range(start: int, end_inclusive: int) -> bytes:
            chunk = raw_zip_bytes[start : end_inclusive + 1]
            fetched_chunks.append(chunk)
            return chunk

        res_range = extract_listed_images_via_range_fn(
            total_size=len(raw_zip_bytes),
            fetch_range=mock_fetch_range,
            dest_dvqa_dir=dest_range_dir,
            expected_sha_map=synth_map,
            forbidden_shas=forbidden_shas,
        )
        assert res_range["extracted_count"] == 5
        # Verify the unlisted entry's local header at offset 0 was NEVER fetched by the Range reader
        assert not any(c.startswith(b"PK\x03\x04") and b"9999_unlisted_test.jpg" in c[:80] for c in fetched_chunks)
        assert not (dest_range_dir / "images/9999_unlisted_test.jpg").exists()

        # 3. Also test fallback local-zip extraction and automatic zip deletion
        res_zip = extract_listed_images_from_zip(
            zip_path=zip_path,
            dest_dvqa_dir=dest_zip_dir,
            expected_sha_map=synth_map,
            forbidden_shas=forbidden_shas,
            verify_zip_sha=False,
            delete_zip_after=True,
        )
        assert res_zip["extracted_count"] == 5
        assert not zip_path.exists(), "Synthetic zip must be unlinked after extraction"

    print(json.dumps({
        "script": "stage_images.py",
        "selftest": "OK",
        "default_mode": "http_range",
        "hf_revision_pin": HF_DATASET_REVISION,
        "images_zip_lfs_sha256_pin": IMAGES_ZIP_LFS_SHA256,
        "dev1000_image_sha256_tsv_sha256": DEV1000_IMAGE_SHA256_TSV_PIN,
        "dev1000_distinct_image_shas": len(set(pin_map.values())),
    }, sort_keys=True))


def main() -> None:
    import json

    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--dest-dir", type=Path, default=Path("/tmp/dvqa_pilot_stage"))
    ap.add_argument("--from-local-zip", type=Path, default=None)
    ap.add_argument("--manifest-out", type=Path, default=DEV1000_IMAGE_SHA256_TSV)
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    res = stage_from_hf(args.dest_dir, from_local_zip=args.from_local_zip, manifest_out=args.manifest_out)
    print(json.dumps(res, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
