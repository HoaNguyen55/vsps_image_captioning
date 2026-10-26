#!/usr/bin/env python3
"""M4 Host Hygiene, Machine-Identity & Test-Isolation Check for DrivingVQA Pilot (CC-104 F5, F10, R4, R6; W3, W4).

Runs on M4 on CPU before any GPU timer or model load. Refuses to start if:
  1. The host is M3 (detected via `VSPS_MACHINE_ID`, `/root/.vsps_machine_id`, `/root/outputs/claude_ops/m3_rebuild_*.log`,
     missing `/root/outputs/claude_ops/m4_rebuild_*.log` when `--require-m4-marker` is set, or forbidden GPU UUID);
  2. Any of the 7 pinned manifests or prereg exclusion files fails its SHA-256 check (including
     `manuscript/ken/dvqa_dev1000_image_sha256.tsv`, sha256 `ddc41513...`);
  3. The pilot image directory does not contain the exact 1,000 image files listed in
     `drivingvqa_dev1000_ids.tsv`, or any staged image's SHA-256 differs from `dvqa_dev1000_image_sha256.tsv`;
  4. Any other image file (.jpg, .jpeg, .png, .webp, .bmp) exists under `--scan-root` (/root)
     outside the pilot image folder and the explicit system/venv/model-cache allowlist (`ALLOWLIST_SCAN_SKIP_REL_DIRS`);
  5. Any image SHA-256 overlaps `exclusion.json` (`image_sha256`), `lists.json` (`refuse.image_sha256`),
     or `ov_test_files.tsv` (8,179 forbidden test image hashes);
  6. Any file under `--scan-root` or `--dvqa-dir` matches `test.json`, `c_test*`, or `ct_*`;
  7. `train.json` in `--dvqa-dir` differs from pinned SHA-256 `4a204e3f...`.

Usage:
  python3 scripts/ken_dvqa_pilot/host_check.py --selftest
  python3 scripts/ken_dvqa_pilot/host_check.py --dvqa-dir /root/dvqa_pilot --scan-root /root --image-sha-tsv manuscript/ken/dvqa_dev1000_image_sha256.tsv --require-m4-marker --out .session_backup/2026-10-26/dvqa_pilot/host_check.json
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = next(
    (p for p in HERE.parents if (p / "manuscript/prereg/2026-10-22_c_stage1/lists.json").exists()),
    HERE.parents[2],
)

PINS = {
    "manuscript/ken/drivingvqa_dev500_ids.tsv":
        "9896af1186ddd6a5806095ba696851b5aef512079f5d0813cff3f7f4fae9c4ce",
    "manuscript/ken/drivingvqa_dev500b_ids.tsv":
        "86cc908cdf3e8622086caafd44572edf6ad35ef13ad0bdb8150bf393f3c30d54",
    "manuscript/ken/drivingvqa_dev1000_ids.tsv":
        "636e04775153ef9cb879a7620d195fcaa7e86894ead73b008c8f95b47e268dec",
    "manuscript/ken/dvqa_dev1000_image_sha256.tsv":
        "ddc41513f02d5171fedc1a86146f9c708f87e09d7e88ddde83434bb7f1ef3289",
    "manuscript/prereg/2026-10-21_dev_pools/exclusion.json":
        "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f",
    "manuscript/prereg/2026-10-22_c_stage1/lists.json":
        "5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371",
    "manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv":
        "99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695",
}
DEFAULT_IMAGE_SHA_TSV = ROOT / "manuscript/ken/dvqa_dev1000_image_sha256.tsv"
IMAGE_SHA_TSV_PIN = "ddc41513f02d5171fedc1a86146f9c708f87e09d7e88ddde83434bb7f1ef3289"
TRAIN_JSON_SHA256 = "4a204e3fa7516db313ceeb91ac989919979e31da20e484bc5f4018c261bd483d"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
FORBIDDEN_NAME_PATTERNS = (
    "test.json",
    "*_test.json",
    "c_test*",
    "ct_*",
    "uit-openviic-annotation-test.json",
    "oiv7_labels.json",
)

# REVIEW_KEN_BATCH8 W4: explicit allowlist of non-dataset system/venv/model-cache directories under /root
# skipped during the stray-image scan so Python site-packages or HF model repo icons do not cause false stops.
ALLOWLIST_SCAN_SKIP_REL_DIRS = (
    "vsps/.venv",
    "vsps/.git",
    "venv-lb",
    "venv-c1score",
    ".cache/huggingface/hub",
    ".cache/pip",
    "ncs-data/models",
    "ncs-data/vncorenlp",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_repo_pins(repo_root: Path = ROOT) -> dict[str, str]:
    verified: dict[str, str] = {}
    for rel, expected_sha in sorted(PINS.items()):
        p = repo_root / rel
        if not p.is_file():
            raise SystemExit(f"REFUSED: missing pinned file {p}")
        got = sha256_file(p)
        if got != expected_sha:
            raise SystemExit(f"REFUSED: SHA-256 mismatch for {rel}: got {got}, expected {expected_sha}")
        verified[rel] = got
    return verified


def load_expected_dev1000_images(repo_root: Path = ROOT) -> list[str]:
    tsv_path = repo_root / "manuscript/ken/drivingvqa_dev1000_ids.tsv"
    lines = tsv_path.read_text(encoding="utf-8").splitlines()[1:]
    rels = [line.split("\t")[1].strip() for line in lines if line.strip()]
    if len(rels) != 1000 or len(set(rels)) != 1000:
        raise SystemExit(f"REFUSED: expected 1,000 distinct image filenames in {tsv_path}, got {len(set(rels))}")
    return sorted(rels)


def load_forbidden_sha256_set(repo_root: Path = ROOT) -> set[str]:
    verify_repo_pins(repo_root)
    excl = json.loads((repo_root / "manuscript/prereg/2026-10-21_dev_pools/exclusion.json").read_text(encoding="utf-8"))
    lists = json.loads((repo_root / "manuscript/prereg/2026-10-22_c_stage1/lists.json").read_text(encoding="utf-8"))
    ov_tsv = (repo_root / "manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv").read_text(encoding="utf-8")

    forbidden: set[str] = set()
    for group_shas in excl.get("image_sha256", {}).values():
        forbidden.update(group_shas)
    forbidden.update(lists.get("refuse", {}).get("image_sha256", []))
    for r in lists.get("sets", {}).get("xm_test2500", []):
        if len(r) >= 3:
            forbidden.add(r[2])
    for line in ov_tsv.splitlines():
        parts = line.strip().split("\t")
        if len(parts) >= 2:
            forbidden.add(parts[1])
    return forbidden


def is_forbidden_filename(name: str) -> bool:
    low = name.lower()
    return any(fnmatch.fnmatch(low, pat.lower()) for pat in FORBIDDEN_NAME_PATTERNS)


def check_m4_not_m3_identity(
    scan_root: Path,
    require_m4_marker: bool = False,
    forbid_gpu_uuid: str | None = None,
) -> list[str]:
    """REVIEW_KEN_BATCH8 W4: verify host is M4 and never M3 using rebuild marker files, machine-id file/env,
    and optional GPU UUID check (since rental hostnames are not 'm3')."""
    problems: list[str] = []
    env_mid = os.environ.get("VSPS_MACHINE_ID", "").strip().lower()
    if env_mid == "m3":
        problems.append("machine_id_env_is_m3")

    mid_file = scan_root / ".vsps_machine_id"
    if mid_file.is_file():
        val = mid_file.read_text(encoding="utf-8").strip().lower()
        if val == "m3":
            problems.append("machine_id_file_is_m3")

    ops_dir = scan_root / "outputs/claude_ops"
    m3_logs = sorted(ops_dir.glob("m3_rebuild_*.log")) if ops_dir.is_dir() else []
    m4_logs = sorted(ops_dir.glob("m4_rebuild_*.log")) if ops_dir.is_dir() else []
    if m3_logs:
        problems.append(f"m3_rebuild_marker_present:{m3_logs[0].name}")
    if require_m4_marker and not m4_logs:
        problems.append(f"missing_m4_rebuild_marker_in:{ops_dir.as_posix()}")

    uuid_to_forbid = (forbid_gpu_uuid or os.environ.get("VSPS_M3_GPU_UUID", "")).strip()
    if uuid_to_forbid:
        try:
            out = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=uuid", "--format=csv,noheader"],
                text=True,
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
            gpu_uuids = [line.strip() for line in out.splitlines() if line.strip()]
            if uuid_to_forbid in gpu_uuids:
                problems.append(f"forbidden_m3_gpu_uuid_detected:{uuid_to_forbid}")
        except Exception:
            pass

    return problems


def is_in_allowlisted_skip_dir(file_path: Path, scan_root: Path) -> bool:
    if scan_root not in file_path.parents:
        return False
    rel = file_path.relative_to(scan_root).as_posix()
    return any(rel == prefix or rel.startswith(prefix + "/") for prefix in ALLOWLIST_SCAN_SKIP_REL_DIRS)


def run_host_check(
    dvqa_dir: Path,
    scan_root: Path,
    expected_rel_images: list[str],
    forbidden_shas: set[str],
    image_sha_manifest: Path | None = DEFAULT_IMAGE_SHA_TSV,
    require_train_json_sha: bool = True,
    require_image_manifest_pin: bool = True,
    require_m4_marker: bool = False,
    forbid_gpu_uuid: str | None = None,
    repo_root_to_skip: Path | None = ROOT,
) -> dict:
    problems: list[str] = []
    dvqa_dir = dvqa_dir.resolve()
    scan_root = scan_root.resolve()
    pilot_img_dir = (dvqa_dir / "images").resolve()

    # 0. Check M4 vs M3 host identity (W4)
    problems.extend(
        check_m4_not_m3_identity(
            scan_root=scan_root,
            require_m4_marker=require_m4_marker,
            forbid_gpu_uuid=forbid_gpu_uuid,
        )
    )

    # 1. Check train.json and absence of test.json in dvqa_dir
    train_json = dvqa_dir / "train.json"
    if not train_json.is_file():
        problems.append(f"missing_train_json:{train_json}")
        train_sha = None
    else:
        train_sha = sha256_file(train_json)
        if require_train_json_sha and train_sha != TRAIN_JSON_SHA256:
            problems.append(f"train_json_sha256_mismatch:{train_sha}")

    if not pilot_img_dir.is_dir():
        problems.append(f"missing_pilot_img_dir:{pilot_img_dir}")
        staged_files: list[Path] = []
    else:
        staged_files = sorted([p for p in pilot_img_dir.rglob("*") if p.is_file()])

    expected_basenames = sorted(Path(r).name for r in expected_rel_images)
    expected_set = set(expected_basenames)
    staged_basenames = sorted(p.name for p in staged_files)
    staged_set = set(staged_basenames)

    missing_imgs = sorted(expected_set - staged_set)
    unlisted_imgs = sorted(staged_set - expected_set)
    if missing_imgs:
        problems.append(f"missing_pilot_images:{len(missing_imgs)}:e.g.{missing_imgs[:3]}")
    if unlisted_imgs:
        problems.append(f"unlisted_pilot_images:{len(unlisted_imgs)}:e.g.{unlisted_imgs[:3]}")
    if len(staged_files) != len(staged_set):
        problems.append("duplicate_basenames_in_pilot_img_dir")

    # 2. Compute SHA-256 of every staged image and check against forbidden_shas and image_sha_manifest (W3 / F5)
    staged_sha_map: dict[str, str] = {}
    forbidden_sha_hits: list[str] = []
    for p in staged_files:
        h = sha256_file(p)
        staged_sha_map[f"images/{p.name}"] = h
        if h in forbidden_shas:
            forbidden_sha_hits.append(f"{p.name}:{h[:12]}")

    if image_sha_manifest is not None:
        if not image_sha_manifest.is_file():
            problems.append(f"missing_image_sha_manifest:{image_sha_manifest}")
        else:
            if require_image_manifest_pin and sha256_file(image_sha_manifest) != IMAGE_SHA_TSV_PIN:
                problems.append(f"image_sha_manifest_pin_mismatch:{sha256_file(image_sha_manifest)}")
            pin_map: dict[str, str] = {}
            for line in image_sha_manifest.read_text(encoding="utf-8").splitlines():
                if not line.strip() or line.startswith("img_filename"):
                    continue
                parts = line.split("\t")
                if len(parts) >= 2:
                    pin_map[Path(parts[0].strip()).name] = parts[1].strip()
            sha_mismatches = [
                name for name in expected_basenames
                if name not in pin_map or staged_sha_map.get(f"images/{name}") != pin_map[name]
            ]
            if sha_mismatches:
                problems.append(f"image_sha_manifest_mismatch:{len(sha_mismatches)}:e.g.{sha_mismatches[:3]}")

    # 3. Scan scan_root (/root) for any stray images outside pilot_img_dir (skipping allowlisted venv/cache dirs)
    # and any forbidden test filenames (W4)
    stray_images: list[str] = []
    forbidden_files: list[str] = []
    skip_resolved = repo_root_to_skip.resolve() if repo_root_to_skip and repo_root_to_skip.exists() else None

    for root_to_walk in sorted({scan_root, dvqa_dir}):
        if not root_to_walk.exists():
            continue
        for p in sorted(root_to_walk.rglob("*")):
            if not p.is_file():
                continue
            if is_in_allowlisted_skip_dir(p, scan_root):
                continue
            rp = p.resolve()
            if is_in_allowlisted_skip_dir(rp, scan_root):
                continue
            # If repo_root lies inside scan_root, skip its tracked prereg/c_test folder during name pattern scan
            if skip_resolved is not None and skip_resolved in rp.parents:
                rel_repo = rp.relative_to(skip_resolved).as_posix()
                if rel_repo.startswith(("manuscript/prereg/", "scripts/c_test/", ".git/")):
                    continue
            if is_forbidden_filename(rp.name):
                forbidden_files.append(rp.as_posix())
            if rp.suffix.lower() in IMAGE_EXTS:
                if pilot_img_dir not in rp.parents:
                    stray_images.append(rp.as_posix())
                    h_other = sha256_file(rp)
                    if h_other in forbidden_shas:
                        forbidden_sha_hits.append(f"{rp.as_posix()}:{h_other[:12]}")

    if stray_images:
        problems.append(f"stray_images_outside_pilot:{len(stray_images)}:e.g.{stray_images[:3]}")
    if forbidden_files:
        problems.append(f"forbidden_filenames:{len(forbidden_files)}:e.g.{forbidden_files[:3]}")
    if forbidden_sha_hits:
        problems.append(f"forbidden_sha256_hits:{len(forbidden_sha_hits)}:e.g.{forbidden_sha_hits[:3]}")

    staged_manifest_sha256 = hashlib.sha256(
        ("\n".join(f"{k}\t{v}" for k, v in sorted(staged_sha_map.items())) + "\n").encode("utf-8")
    ).hexdigest()

    return {
        "schema": "vsps.ken_dvqa_host_check.v2",
        "ok": len(problems) == 0,
        "dvqa_dir": dvqa_dir.as_posix(),
        "scan_root": scan_root.as_posix(),
        "allowlist_scan_skip_rel_dirs": list(ALLOWLIST_SCAN_SKIP_REL_DIRS),
        "train_json_sha256": train_sha,
        "expected_image_count": len(expected_basenames),
        "staged_image_count": len(staged_files),
        "missing_image_count": len(missing_imgs),
        "unlisted_image_count": len(unlisted_imgs),
        "stray_images_outside_pilot_count": len(stray_images),
        "forbidden_filename_count": len(forbidden_files),
        "forbidden_sha256_hit_count": len(forbidden_sha_hits),
        "staged_image_sha256_table_digest": staged_manifest_sha256,
        "problems": problems,
    }


def selftest() -> None:
    verified_pins = verify_repo_pins(ROOT)
    expected_rels = load_expected_dev1000_images(ROOT)
    forbidden_shas = load_forbidden_sha256_set(ROOT)
    assert len( verified_pins) == 7
    assert len(expected_rels) == 1000
    assert len(forbidden_shas) > 4000

    sub_expected = expected_rels[:5]
    sample_forbidden_sha = sorted(forbidden_shas)[0]

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scan_root = tmp_path / "root"
        dvqa_dir = scan_root / "dvqa_pilot"
        img_dir = dvqa_dir / "images"
        img_dir.mkdir(parents=True)
        (dvqa_dir / "train.json").write_text("{}", encoding="utf-8")

        # Create M4 rebuild marker file (W4)
        ops_dir = scan_root / "outputs/claude_ops"
        ops_dir.mkdir(parents=True)
        m4_marker = ops_dir / "m4_rebuild_2026-10-26.log"
        m4_marker.write_text("M4 rebuild ok\n", encoding="utf-8")

        # Create an image inside an allowlisted venv path under /root to verify W4 allowlist
        venv_img = scan_root / "venv-lb/lib/python3.10/site-packages/pkg_icon.png"
        venv_img.parent.mkdir(parents=True)
        venv_img.write_text("allowlisted_venv_icon", encoding="utf-8")

        manifest_lines: list[str] = []
        for rel in sub_expected:
            f_img = img_dir / Path(rel).name
            f_img.write_text(f"clean_image_{rel}", encoding="utf-8")
            manifest_lines.append(f"{rel}\t{sha256_file(f_img)}")

        synth_manifest = tmp_path / "sub_image_sha256.tsv"
        synth_manifest.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

        # 1. Clean configuration passes with M4 marker, allowlisted venv icon, and per-image sha256 check
        res_ok = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas,
            image_sha_manifest=synth_manifest,
            require_train_json_sha=False,
            require_image_manifest_pin=False,
            require_m4_marker=True,
        )
        assert res_ok["ok"] is True, f"Expected clean host check to pass: {res_ok}"

        # 2. Refusal when M3 marker is present and M4 marker is absent (W4)
        m4_marker.unlink()
        m3_marker = ops_dir / "m3_rebuild_2026-10-26.log"
        m3_marker.write_text("M3 rebuild\n", encoding="utf-8")
        res_m3 = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas,
            image_sha_manifest=synth_manifest,
            require_train_json_sha=False,
            require_image_manifest_pin=False,
            require_m4_marker=True,
        )
        assert res_m3["ok"] is False and any("m3_rebuild_marker" in p for p in res_m3["problems"])
        m3_marker.unlink()
        m4_marker.write_text("M4 rebuild ok\n", encoding="utf-8")

        # 3. Refusal of an unlisted image in pilot folder
        unlisted_file = img_dir / "9999.jpg"
        unlisted_file.write_text("unlisted_test_image", encoding="utf-8")
        res_unlisted = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas,
            image_sha_manifest=synth_manifest,
            require_train_json_sha=False,
            require_image_manifest_pin=False,
        )
        assert res_unlisted["ok"] is False and res_unlisted["unlisted_image_count"] == 1
        unlisted_file.unlink()

        # 4. Refusal of a stray image in /root outside pilot folder and outside allowlist
        stray_file = scan_root / "stray_image.jpg"
        stray_file.write_text("stray", encoding="utf-8")
        res_stray = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas,
            image_sha_manifest=synth_manifest,
            require_train_json_sha=False,
            require_image_manifest_pin=False,
        )
        assert res_stray["ok"] is False and res_stray["stray_images_outside_pilot_count"] == 1
        stray_file.unlink()

        # 5. Refusal of test-like filenames (test.json, ct_test.json, c_test_run.json)
        for bad_name in ("test.json", "ct_test.json", "c_test_run.json"):
            bad_path = scan_root / bad_name
            bad_path.write_text("{}", encoding="utf-8")
            res_bad_name = run_host_check(
                dvqa_dir,
                scan_root,
                sub_expected,
                forbidden_shas,
                image_sha_manifest=synth_manifest,
                require_train_json_sha=False,
                require_image_manifest_pin=False,
            )
            assert res_bad_name["ok"] is False and res_bad_name["forbidden_filename_count"] == 1
            bad_path.unlink()

        # 6. Refusal of an image whose SHA-256 is in the forbidden set
        target_img = img_dir / Path(sub_expected[0]).name
        target_sha = sha256_file(target_img)
        res_bad_sha = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas | {target_sha},
            image_sha_manifest=synth_manifest,
            require_train_json_sha=False,
            require_image_manifest_pin=False,
        )
        assert res_bad_sha["ok"] is False and res_bad_sha["forbidden_sha256_hit_count"] == 1

    print(json.dumps({
        "script": "host_check.py",
        "selftest": "OK",
        "verified_pins_count": len(verified_pins),
        "dev1000_expected_images": len(expected_rels),
        "forbidden_sha256_count": len(forbidden_shas),
        "sample_forbidden_sha256_prefix": sample_forbidden_sha[:16],
    }, sort_keys=True))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--dvqa-dir", type=Path, default=Path("/root/dvqa_pilot"))
    ap.add_argument("--scan-root", type=Path, default=Path("/root"))
    ap.add_argument("--image-sha-tsv", type=Path, default=DEFAULT_IMAGE_SHA_TSV)
    ap.add_argument("--require-m4-marker", action="store_true")
    ap.add_argument("--forbid-gpu-uuid", type=str, default=None)
    ap.add_argument("--out", type=Path, default=Path(".session_backup/2026-10-26/dvqa_pilot/host_check.json"))
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    verify_repo_pins(ROOT)
    expected_rels = load_expected_dev1000_images(ROOT)
    forbidden_shas = load_forbidden_sha256_set(ROOT)
    res = run_host_check(
        dvqa_dir=args.dvqa_dir,
        scan_root=args.scan_root,
        expected_rel_images=expected_rels,
        forbidden_shas=forbidden_shas,
        image_sha_manifest=args.image_sha_tsv,
        require_train_json_sha=True,
        require_image_manifest_pin=True,
        require_m4_marker=args.require_m4_marker,
        forbid_gpu_uuid=args.forbid_gpu_uuid,
    )
    out_text = json.dumps(res, indent=2, sort_keys=True) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(out_text, encoding="utf-8")
    print(out_text, end="")
    if not res["ok"]:
        raise SystemExit("REFUSED: M4 host_check failed; see problems list above")


if __name__ == "__main__":
    main()
