#!/usr/bin/env python3
"""Local Operator Image Staging Script for DrivingVQA Pilot v4 (CC-104 F5, CC-104a W7, CC-104b ruling 5 (b), PI-1026c).

Runs on the operator's local staging workstation BEFORE copying `/root/dvqa_pilot` to M4:
  1. Pins Hugging Face dataset repo `EPFL-DrivingVQA/DrivingVQA` at revision
     `02ce870cfe037b93cc034034cd747a7eecdd455c`.
  2. Downloads `train.json` (sha256 `4a204e3f...`) ONLY via
     `huggingface_hub.hf_hub_download(..., filename="train.json", revision=...)`.
     `snapshot_download` is STRICTLY FORBIDDEN because the repository root contains `test.json`.
  3. Reads ONLY the 22-byte ZIP End-of-Central-Directory record (no comment allowed, CD must end where the
     EOCD starts) and the Central Directory of `images.zip` (`826,036,403` bytes, LFS sha256 `fcf5111b...`)
     via HTTP Range requests, then fetches ONLY the byte ranges of the `img_filename` entries listed in
     `--ids-tsv` (default `manuscript/ken/drivingvqa_train3142_ids.tsv`, all 3,142 train ids). Every request
     requires HTTP 206 and a matching Content-Range before read() (W7). Requests are sequential.
  4. Every extracted image is checked against the CRC-32 and size in the Central Directory and against all
     8,179 forbidden test image SHA-256s.

Modes:
  --mode manifest : fetch, check CRC/size/forbidden, write `--manifest-out` (img_filename<TAB>sha256, sorted).
                    The rows for the dev1000 names must equal the committed dev1000 manifest (ddc41513...).
  --mode range    : fetch and require every image SHA-256 to match `--expected-sha-tsv` (pinned).
  --mode verify   : no network; re-hash `--dest-dir` against the pinned `--expected-sha-tsv`.
  --reuse-dir DIR : in manifest/range mode, an image already in DIR is copied instead of fetched only if its
                    SHA-256 matches the pinned sha list given by `--reuse-sha-tsv` (manifest mode: the dev1000
                    manifest ddc41513...; range mode: `--expected-sha-tsv`) AND its CRC-32 and size match the CD.

Usage:
  python3 scripts/ken_dvqa_pilot/stage_images.py --selftest
  python3 scripts/ken_dvqa_pilot/stage_images.py --mode manifest --dest-dir /tmp/dvqa_pilot_stage \
      --manifest-out manuscript/ken/dvqa_train3142_image_sha256.tsv
  python3 scripts/ken_dvqa_pilot/stage_images.py --mode verify --dest-dir /tmp/dvqa_pilot_stage
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
IDS_TSV = ROOT / HC.TRAIN3142_IDS_REL
TRAIN3142_IMAGE_SHA256_TSV = HC.DEFAULT_IMAGE_SHA_TSV
TRAIN3142_IMAGE_SHA256_TSV_PIN = HC.IMAGE_SHA_TSV_PIN
TRAIN3142_DISTINCT_IMAGE_SHAS = 3133
DEV1000_IMAGE_SHA256_TSV = ROOT / "manuscript/ken/dvqa_dev1000_image_sha256.tsv"
DEV1000_IMAGE_SHA256_TSV_PIN = "ddc41513f02d5171fedc1a86146f9c708f87e09d7e88ddde83434bb7f1ef3289"
EOCD_LEN = 22


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pinned_image_sha256_map(manifest_path: Path, expected_pin: str, expected_n: int) -> dict[str, str]:
    if not manifest_path.is_file():
        raise SystemExit(f"REFUSED: missing per-image SHA-256 manifest {manifest_path}")
    if sha256_file(manifest_path) != expected_pin:
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
    if len(out) != expected_n:
        raise SystemExit(f"REFUSED: expected {expected_n:,} rows in {manifest_path}, got {len(out)}")
    return out


def format_sha_manifest(sha_map: dict[str, str]) -> str:
    return "".join(f"{k}\t{v}\n" for k, v in sorted(sha_map.items()))


def http_fetch_byte_range(
    url: str,
    start: int,
    end_inclusive: int,
    timeout: int = 60,
    urlopen_fn: Callable | None = None,
) -> bytes:
    """CC-104a W7: Fetch inclusive byte range [start, end_inclusive] via HTTP Range header.
    Requires HTTP status 206 and a matching Content-Range header BEFORE calling read(); refuses otherwise."""
    import re as _re

    req = urllib.request.Request(
        url,
        headers={
            "Range": f"bytes={start}-{end_inclusive}",
            "User-Agent": "vsps-dvqa-operator-stage/1.0",
        },
    )
    opener = urlopen_fn or urllib.request.urlopen
    with opener(req, timeout=timeout) as resp:
        status = getattr(resp, "status", None)
        if status is None and hasattr(resp, "getcode"):
            status = resp.getcode()
        if status != 206:
            raise SystemExit(f"REFUSED (W7): HTTP Range {start}-{end_inclusive} returned status {status} != 206")
        hdrs = getattr(resp, "headers", None) or {}
        content_range = str(hdrs.get("Content-Range", "") or hdrs.get("content-range", "")).strip()
        if not _re.match(rf"^bytes\s+{start}-{end_inclusive}/(?:\d+|\*)\s*$", content_range, flags=_re.IGNORECASE):
            raise SystemExit(
                f"REFUSED (W7): HTTP Content-Range mismatch for {start}-{end_inclusive}: got {content_range!r}"
            )
        data = resp.read()
    expected_len = end_inclusive - start + 1
    if len(data) != expected_len:
        raise SystemExit(f"REFUSED: HTTP Range {start}-{end_inclusive} returned {len(data)} bytes != {expected_len}")
    return data


def extract_listed_images_via_range_fn(
    total_size: int,
    fetch_range: Callable[[int, int], bytes],
    dest_dvqa_dir: Path,
    listed_names: list[str],
    forbidden_shas: set[str],
    expected_sha_map: dict[str, str] | None = None,
    reuse_dir: Path | None = None,
    reuse_sha_map: dict[str, str] | None = None,
) -> dict:
    """Read ONLY the 22-byte EOCD, the Central Directory and the listed entries via `fetch_range(start, end)`:
    per entry the 30-byte local header, then exactly `name + extra + comp_size` (W7, no +256 overrun).
    CC-104b ruling 5 (b): the EOCD read is exactly 22 bytes; a ZIP comment, or a CD that does not end where
    the EOCD starts, is refused, so no byte outside the CD and the listed entries is ever fetched.
    `expected_sha_map=None` is manifest mode: images are checked by CD CRC-32/size and the forbidden set only."""
    if total_size < EOCD_LEN:
        raise SystemExit("REFUSED: archive smaller than a ZIP EOCD record")
    tail = fetch_range(total_size - EOCD_LEN, total_size - 1)
    if len(tail) != EOCD_LEN or tail[:4] != b"PK\x05\x06":
        raise SystemExit("REFUSED: ZIP End-of-Central-Directory not in the last 22 bytes (comment or ZIP64)")
    _sig, _disk, _cd_disk, _entries_disk, total_entries, cd_size, cd_offset, comment_len = struct.unpack(
        "<4sHHHHIIH", tail
    )
    if comment_len != 0 or cd_offset + cd_size != total_size - EOCD_LEN:
        raise SystemExit("REFUSED: ZIP Central Directory does not end at the EOCD")

    wanted = set(listed_names)
    cd_bytes = fetch_range(cd_offset, cd_offset + cd_size - 1)
    pos = 0
    cd_entries: dict[str, tuple[int, int, int, int, int]] = {}
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
            crc32,
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
        if name in wanted:
            cd_entries[name] = (local_header_offset, comp_size, uncomp_size, comp_method, crc32)
        pos += 46 + name_len + extra_len + comment_len

    missing_in_cd = sorted(wanted - set(cd_entries.keys()))
    if missing_in_cd:
        raise SystemExit(f"REFUSED: {len(missing_in_cd)} expected entries missing from ZIP CD: {missing_in_cd[:3]}")

    img_dir = dest_dvqa_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    extracted_shas: dict[str, str] = {}
    total_payload_bytes_fetched = 0
    reused_count = 0

    for rel_path in sorted(wanted):
        lh_off, comp_size, uncomp_size, comp_method, crc32 = cd_entries[rel_path]
        raw_bytes = None
        reuse_file = reuse_dir / rel_path if reuse_dir is not None else None
        if reuse_file is not None and reuse_sha_map and rel_path in reuse_sha_map and reuse_file.is_file():
            cand = reuse_file.read_bytes()
            if (
                hashlib.sha256(cand).hexdigest() == reuse_sha_map[rel_path]
                and len(cand) == uncomp_size
                and zlib.crc32(cand) == crc32
            ):
                raw_bytes = cand
                reused_count += 1
        if raw_bytes is None:
            # CC-104a W7: Read the 30-byte local header, then exactly name+extra+comp_size, no +256 overrun
            lh_bytes = fetch_range(lh_off, lh_off + 29)
            total_payload_bytes_fetched += len(lh_bytes)
            if len(lh_bytes) != 30 or lh_bytes[:4] != b"PK\x03\x04":
                raise SystemExit(f"REFUSED: invalid ZIP local file header for {rel_path}")
            lf_name_len, lf_extra_len = struct.unpack("<HH", lh_bytes[26:30])
            body_len = lf_name_len + lf_extra_len + comp_size
            body_bytes = fetch_range(lh_off + 30, lh_off + 30 + body_len - 1)
            total_payload_bytes_fetched += len(body_bytes)
            if len(body_bytes) != body_len:
                raise SystemExit(f"REFUSED: truncated ZIP entry body for {rel_path}")
            comp_payload = body_bytes[lf_name_len + lf_extra_len :]
            if comp_method == 0:
                raw_bytes = comp_payload
            elif comp_method == 8:
                raw_bytes = zlib.decompress(comp_payload, -15)
            else:
                raise SystemExit(f"REFUSED: unsupported ZIP compression method {comp_method} for {rel_path}")
            if len(raw_bytes) != uncomp_size:
                raise SystemExit(f"REFUSED: uncompressed size mismatch for {rel_path}")
            if zlib.crc32(raw_bytes) != crc32:
                raise SystemExit(f"REFUSED: CRC-32 mismatch against the ZIP CD for {rel_path}")

        got_sha = hashlib.sha256(raw_bytes).hexdigest()
        if expected_sha_map is not None and got_sha != expected_sha_map.get(rel_path):
            raise SystemExit(
                f"REFUSED: per-image SHA-256 mismatch for {rel_path}: got {got_sha}, expected {expected_sha_map.get(rel_path)}"
            )
        if got_sha in forbidden_shas:
            raise SystemExit(f"REFUSED: {rel_path} SHA-256 {got_sha} is in forbidden test set")

        out_file = dest_dvqa_dir / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_bytes(raw_bytes)
        extracted_shas[rel_path] = got_sha

    return {
        "mode": "http_range" if expected_sha_map is not None else "manifest",
        "extracted_count": len(extracted_shas),
        "reused_count": reused_count,
        "fetched_count": len(extracted_shas) - reused_count,
        "distinct_sha256_count": len(set(extracted_shas.values())),
        "total_cd_entries_scanned": int(total_entries),
        "total_payload_bytes_fetched": int(total_payload_bytes_fetched),
        "total_extracted_bytes": sum((dest_dvqa_dir / k).stat().st_size for k in extracted_shas),
        "dest_dvqa_dir": dest_dvqa_dir.as_posix(),
        "sha_map": extracted_shas,
    }


def verify_staged_dir(dest_dvqa_dir: Path, expected_sha_map: dict[str, str], forbidden_shas: set[str]) -> dict:
    """No network: the staged images/ folder holds exactly the expected names with the expected SHA-256s."""
    img_dir = dest_dvqa_dir / "images"
    staged = sorted(p.relative_to(dest_dvqa_dir).as_posix() for p in img_dir.rglob("*") if p.is_file())
    if staged != sorted(expected_sha_map):
        extra = sorted(set(staged) - set(expected_sha_map))
        missing = sorted(set(expected_sha_map) - set(staged))
        raise SystemExit(f"REFUSED: staged names differ: {len(missing)} missing {missing[:3]}, {len(extra)} extra {extra[:3]}")
    got = {rel: sha256_file(dest_dvqa_dir / rel) for rel in staged}
    bad = [rel for rel in staged if got[rel] != expected_sha_map[rel]]
    if bad:
        raise SystemExit(f"REFUSED: {len(bad)} staged images differ from the pinned SHA-256s: {bad[:3]}")
    hits = sorted(set(got.values()) & forbidden_shas)
    if hits:
        raise SystemExit(f"REFUSED: {len(hits)} staged images have a forbidden test SHA-256")
    if any(p.name == "test.json" for p in dest_dvqa_dir.rglob("*")):
        raise SystemExit("REFUSED: test.json present under the staging directory")
    return {
        "mode": "verify",
        "verified_count": len(staged),
        "distinct_sha256_count": len(set(got.values())),
        "total_bytes": sum((dest_dvqa_dir / rel).stat().st_size for rel in staged),
        "train_json_sha256": sha256_file(dest_dvqa_dir / "train.json") if (dest_dvqa_dir / "train.json").is_file() else None,
    }


def dev1000_rows_match(sha_map: dict[str, str]) -> bool:
    """Manifest-mode cross-check: the dev1000 rows of the new list equal the committed ddc41513 manifest bytes."""
    dev_map = load_pinned_image_sha256_map(DEV1000_IMAGE_SHA256_TSV, DEV1000_IMAGE_SHA256_TSV_PIN, 1000)
    sub = {k: sha_map[k] for k in dev_map if k in sha_map}
    return format_sha_manifest(sub) == DEV1000_IMAGE_SHA256_TSV.read_text(encoding="utf-8")


def stage_from_hf(
    mode: str,
    dest_dvqa_dir: Path,
    ids_tsv: Path,
    expected_sha_tsv: Path,
    manifest_out: Path | None = None,
    reuse_dir: Path | None = None,
) -> dict:
    """Operator local staging entry point. train.json via `hf_hub_download` ONLY (never `snapshot_download`,
    never `test.json`); images only by HTTP Range from `HF_IMAGES_ZIP_RESOLVE_URL`."""
    from huggingface_hub import hf_hub_download

    if sha256_file(ids_tsv) != HC.PINS[HC.TRAIN3142_IDS_REL]:
        raise SystemExit(f"REFUSED: id list {ids_tsv} does not match the pinned train3142 sha")
    listed = HC.load_expected_train_images(ids_tsv)
    forbidden_shas = HC.load_forbidden_sha256_set(ROOT)
    if mode == "manifest":
        if manifest_out is None:
            raise SystemExit("REFUSED: --manifest-out is required in manifest mode")
        expected_sha_map = None
        reuse_sha_map = load_pinned_image_sha256_map(DEV1000_IMAGE_SHA256_TSV, DEV1000_IMAGE_SHA256_TSV_PIN, 1000)
    else:
        expected_sha_map = load_pinned_image_sha256_map(expected_sha_tsv, TRAIN3142_IMAGE_SHA256_TSV_PIN, HC.N_TRAIN)
        if sorted(expected_sha_map) != listed:
            raise SystemExit("REFUSED: expected-sha TSV names differ from the id list")
        reuse_sha_map = expected_sha_map
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

        res = extract_listed_images_via_range_fn(
            total_size=IMAGES_ZIP_SIZE_BYTES,
            fetch_range=lambda s, e: http_fetch_byte_range(HF_IMAGES_ZIP_RESOLVE_URL, s, e),
            dest_dvqa_dir=dest_dvqa_dir,
            listed_names=listed,
            forbidden_shas=forbidden_shas,
            expected_sha_map=expected_sha_map,
            reuse_dir=reuse_dir,
            reuse_sha_map=reuse_sha_map,
        )

    sha_map = res.pop("sha_map")
    out = {
        "status": "OK",
        "hf_dataset_repo": HF_DATASET_REPO,
        "hf_dataset_revision": HF_DATASET_REVISION,
        "train_json_sha256": TRAIN_JSON_SHA256,
        "images_zip_lfs_sha256": IMAGES_ZIP_LFS_SHA256,
        "ids_tsv_sha256": sha256_file(ids_tsv),
        **res,
    }
    if mode == "manifest":
        if not dev1000_rows_match(sha_map):
            raise SystemExit("REFUSED: dev1000 rows of the new manifest differ from the committed ddc41513 manifest")
        text = format_sha_manifest(sha_map)
        manifest_out.write_text(text, encoding="utf-8")
        out["manifest_out"] = manifest_out.as_posix()
        out["manifest_sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        out["dev1000_rows_match_ddc41513"] = True
    return out


def selftest() -> None:
    import json

    HC.verify_repo_pins(ROOT)
    expected_rels = HC.load_expected_train_images()
    forbidden_shas = HC.load_forbidden_sha256_set(ROOT)
    pin_map = load_pinned_image_sha256_map(TRAIN3142_IMAGE_SHA256_TSV, TRAIN3142_IMAGE_SHA256_TSV_PIN, HC.N_TRAIN)

    # 1. The pinned train3142 image list: names equal the id list, distinct-sha count pinned, no forbidden hash,
    #    and its dev1000 rows equal the committed ddc41513 manifest byte for byte.
    assert sorted(pin_map.keys()) == expected_rels
    assert len(set(pin_map.values())) == TRAIN3142_DISTINCT_IMAGE_SHAS
    assert pin_map["images/2754.jpg"] == pin_map["images/2776.jpg"]
    assert len(set(pin_map.values()) & forbidden_shas) == 0
    assert dev1000_rows_match(pin_map)

    # 1b. CC-104a W7: Verify http_fetch_byte_range requires status 206 and matching Content-Range BEFORE read()
    class _MockResp:
        def __init__(self, status: int, content_range: str, payload: bytes, forbid_read: bool = False):
            self.status = status
            self.headers = {"Content-Range": content_range}
            self._payload = payload
            self._forbid_read = forbid_read

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

        def read(self) -> bytes:
            if self._forbid_read:
                raise AssertionError("read() must not be called when status != 206 or Content-Range mismatches")
            return self._payload

    # Mock returns 200 -> selftest asserts refusal before read()
    try:
        http_fetch_byte_range(
            "https://example.invalid/images.zip",
            0,
            29,
            urlopen_fn=lambda _req, timeout=60: _MockResp(200, "bytes 0-29/1000", b"x" * 30, forbid_read=True),
        )
        raise AssertionError("Expected SystemExit when HTTP status is 200 instead of 206")
    except SystemExit as exc:
        assert "206" in str(exc)

    # Mock returns 206 with mismatched Content-Range -> selftest asserts refusal before read()
    try:
        http_fetch_byte_range(
            "https://example.invalid/images.zip",
            0,
            29,
            urlopen_fn=lambda _req, timeout=60: _MockResp(206, "bytes 0-999/1000", b"x" * 30, forbid_read=True),
        )
        raise AssertionError("Expected SystemExit when Content-Range does not match requested range")
    except SystemExit as exc:
        assert "Content-Range" in str(exc)

    # Mock returns 206 with matching Content-Range -> succeeds
    ok_bytes = http_fetch_byte_range(
        "https://example.invalid/images.zip",
        10,
        19,
        urlopen_fn=lambda _req, timeout=60: _MockResp(206, "bytes 10-19/1000", b"0123456789", forbid_read=False),
    )
    assert ok_bytes == b"0123456789"

    # 2. HTTP-Range selective extraction on a synthetic archive with unlisted entries first and last.
    #    CC-104b ruling 5 (b): the unlisted payloads appear in NO fetched chunk (EOCD and CD reads included).
    sub_keys = expected_rels[:5]
    synth_map: dict[str, str] = {}
    unlisted_marker_start = b"UNLISTED_FORBIDDEN_TEST_IMAGE_START_" * 2000
    unlisted_marker_after = b"UNLISTED_FORBIDDEN_TEST_IMAGE_AFTER_" * 2000
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        def build_zip(path: Path, comment: bytes = b"") -> bytes:
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("images/9998_unlisted_test.jpg", unlisted_marker_start, compress_type=zipfile.ZIP_STORED)
                for i, k in enumerate(sub_keys):
                    payload = f"synth_bytes_for_{k}".encode("utf-8") * 8
                    synth_map[k] = hashlib.sha256(payload).hexdigest()
                    # entry 0 is STORED so the CRC test below can flip one payload byte
                    zf.writestr(k, payload, compress_type=zipfile.ZIP_STORED if i == 0 else zipfile.ZIP_DEFLATED)
                zf.writestr("images/9999_unlisted_test.jpg", unlisted_marker_after, compress_type=zipfile.ZIP_STORED)
                zf.comment = comment
            return path.read_bytes()

        raw_zip_bytes = build_zip(tmp_path / "images.zip")

        def make_fetch(blob: bytes, log: list[bytes]):
            def _fetch(start: int, end_inclusive: int) -> bytes:
                chunk = blob[start : end_inclusive + 1]
                log.append(chunk)
                return chunk
            return _fetch

        def assert_no_unlisted(chunks: list[bytes]) -> None:
            for c in chunks:
                assert b"UNLISTED_FORBIDDEN_TEST_IMAGE_START_" not in c
                assert b"UNLISTED_FORBIDDEN_TEST_IMAGE_AFTER_" not in c, "W7/(b) violation: a read overran into an unlisted entry"

        # 2a. range mode with expected shas
        chunks_a: list[bytes] = []
        res_a = extract_listed_images_via_range_fn(
            len(raw_zip_bytes), make_fetch(raw_zip_bytes, chunks_a), tmp_path / "dest_a", sub_keys,
            forbidden_shas, expected_sha_map=synth_map,
        )
        assert res_a["extracted_count"] == 5 and len(chunks_a) == 2 + 2 * len(sub_keys)
        assert len(chunks_a[0]) == EOCD_LEN
        assert_no_unlisted(chunks_a)
        assert not (tmp_path / "dest_a/images/9998_unlisted_test.jpg").exists()
        assert not (tmp_path / "dest_a/images/9999_unlisted_test.jpg").exists()

        # 2b. manifest mode (no expected shas) returns the same sha map
        chunks_b: list[bytes] = []
        res_b = extract_listed_images_via_range_fn(
            len(raw_zip_bytes), make_fetch(raw_zip_bytes, chunks_b), tmp_path / "dest_b", sub_keys, forbidden_shas,
        )
        assert res_b["sha_map"] == synth_map and res_b["mode"] == "manifest"
        assert_no_unlisted(chunks_b)

        # 2c. reuse: a matching file is copied (2 fewer reads); a corrupted one is fetched again
        reuse_dir = tmp_path / "reuse"
        (reuse_dir / "images").mkdir(parents=True)
        shutil.copy2(tmp_path / "dest_a" / sub_keys[1], reuse_dir / sub_keys[1])
        (reuse_dir / sub_keys[2]).write_bytes(b"corrupted")
        chunks_c: list[bytes] = []
        res_c = extract_listed_images_via_range_fn(
            len(raw_zip_bytes), make_fetch(raw_zip_bytes, chunks_c), tmp_path / "dest_c", sub_keys, forbidden_shas,
            expected_sha_map=synth_map, reuse_dir=reuse_dir, reuse_sha_map=synth_map,
        )
        assert res_c["reused_count"] == 1 and len(chunks_c) == 2 + 2 * (len(sub_keys) - 1)
        assert res_c["sha_map"] == synth_map

        # 2d. a forbidden sha is refused
        try:
            extract_listed_images_via_range_fn(
                len(raw_zip_bytes), make_fetch(raw_zip_bytes, []), tmp_path / "dest_d", sub_keys,
                forbidden_shas | {synth_map[sub_keys[3]]},
            )
            raise AssertionError("Expected SystemExit on a forbidden sha")
        except SystemExit as exc:
            assert "forbidden" in str(exc)

        # 2e. CRC-32 mismatch (one flipped payload byte in the STORED entry) is refused
        p0 = f"synth_bytes_for_{sub_keys[0]}".encode("utf-8") * 8
        at = raw_zip_bytes.index(p0)
        flipped = raw_zip_bytes[:at] + bytes([p0[0] ^ 1]) + raw_zip_bytes[at + 1 :]
        try:
            extract_listed_images_via_range_fn(
                len(flipped), make_fetch(flipped, []), tmp_path / "dest_e", sub_keys, forbidden_shas,
            )
            raise AssertionError("Expected SystemExit on a CRC-32 mismatch")
        except SystemExit as exc:
            assert "CRC-32" in str(exc)

        # 2f. CC-104b (b): a ZIP comment moves the EOCD out of the last 22 bytes -> refused, nothing else read
        commented = build_zip(tmp_path / "images_c.zip", comment=b"x" * 40)
        chunks_f: list[bytes] = []
        try:
            extract_listed_images_via_range_fn(
                len(commented), make_fetch(commented, chunks_f), tmp_path / "dest_f", sub_keys, forbidden_shas,
            )
            raise AssertionError("Expected SystemExit on a ZIP comment")
        except SystemExit as exc:
            assert "End-of-Central-Directory" in str(exc)
        assert len(chunks_f) == 1

        # 2g. verify mode: passes on dest_a, refuses an extra file and a changed file
        (tmp_path / "dest_a/train.json").write_text("{}", encoding="utf-8")
        assert verify_staged_dir(tmp_path / "dest_a", synth_map, forbidden_shas)["verified_count"] == 5
        (tmp_path / "dest_a/images/extra.jpg").write_bytes(b"x")
        try:
            verify_staged_dir(tmp_path / "dest_a", synth_map, forbidden_shas)
            raise AssertionError("Expected SystemExit on an extra staged file")
        except SystemExit as exc:
            assert "extra" in str(exc)
        (tmp_path / "dest_a/images/extra.jpg").unlink()
        (tmp_path / "dest_a" / sub_keys[4]).write_bytes(b"changed")
        try:
            verify_staged_dir(tmp_path / "dest_a", synth_map, forbidden_shas)
            raise AssertionError("Expected SystemExit on a changed staged file")
        except SystemExit as exc:
            assert "differ" in str(exc)

    print(json.dumps({
        "script": "stage_images.py",
        "selftest": "OK",
        "default_mode": "range",
        "hf_revision_pin": HF_DATASET_REVISION,
        "images_zip_lfs_sha256_pin": IMAGES_ZIP_LFS_SHA256,
        "train3142_image_sha256_tsv_sha256": TRAIN3142_IMAGE_SHA256_TSV_PIN,
        "train3142_distinct_image_shas": len(set(pin_map.values())),
    }, sort_keys=True))


def main() -> None:
    import json

    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mode", choices=["manifest", "range", "verify"], default="range")
    ap.add_argument("--dest-dir", type=Path, default=Path("/tmp/dvqa_pilot_stage"))
    ap.add_argument("--ids-tsv", type=Path, default=IDS_TSV)
    ap.add_argument("--expected-sha-tsv", type=Path, default=TRAIN3142_IMAGE_SHA256_TSV)
    ap.add_argument("--manifest-out", type=Path, default=None)
    ap.add_argument("--reuse-dir", type=Path, default=None)
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    if args.mode == "verify":
        expected = load_pinned_image_sha256_map(args.expected_sha_tsv, TRAIN3142_IMAGE_SHA256_TSV_PIN, HC.N_TRAIN)
        if sorted(expected) != HC.load_expected_train_images(args.ids_tsv):
            raise SystemExit("REFUSED: expected-sha TSV names differ from the id list")
        res = verify_staged_dir(args.dest_dir, expected, HC.load_forbidden_sha256_set(ROOT))
    else:
        res = stage_from_hf(args.mode, args.dest_dir, args.ids_tsv, args.expected_sha_tsv,
                            manifest_out=args.manifest_out, reuse_dir=args.reuse_dir)
    print(json.dumps(res, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
