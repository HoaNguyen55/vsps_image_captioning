#!/usr/bin/env python3
"""M4 Host Hygiene, Machine-Identity & Test-Isolation Check for DrivingVQA Pilot (CC-104 F5, F10, R4, R6; W3, W4).

Runs on M4 on CPU before any GPU timer or model load. Refuses to start if:
  1. The host is M3 (detected via `VSPS_MACHINE_ID`, `/root/.vsps_machine_id`, `/root/outputs/claude_ops/m3_rebuild_*.log`,
     missing `/root/outputs/claude_ops/m4_rebuild_*.log` when `--require-m4-marker` is set, or forbidden GPU UUID);
  2. Any of the 4 pinned files (the train3142 id list and the 3 prereg exclusion files) or the image
     manifest `manuscript/ken/dvqa_train3142_image_sha256.tsv` fails its SHA-256 check;
  3. The pilot image directory does not contain the exact 3,142 image files listed in
     `drivingvqa_train3142_ids.tsv`, or any staged image's SHA-256 differs from `dvqa_train3142_image_sha256.tsv`;
  4. Any other image file (.jpg, .jpeg, .png, .webp, .bmp) exists under `--scan-root` (/root)
     outside the pilot image folder and the explicit system/venv/model-cache allowlist (`ALLOWLIST_SCAN_SKIP_REL_DIRS`);
  5. Any image SHA-256 overlaps `exclusion.json` (`image_sha256`), `lists.json` (`refuse.image_sha256`),
     or `ov_test_files.tsv` (8,179 forbidden test image hashes);
  6. Any file under `--scan-root` or `--dvqa-dir` matches `test.json`, `c_test*`, or `ct_*`
     (v4, CC-104b ruling 5: git-tracked files are exempt only under the repo base, and only `<repo>/.git/` is skipped);
  7. `train.json` in `--dvqa-dir` differs from pinned SHA-256 `4a204e3f...`.

Usage:
  python3 scripts/ken_dvqa_pilot/host_check.py --selftest
  python3 scripts/ken_dvqa_pilot/host_check.py --dvqa-dir /root/dvqa_pilot --scan-root /root --image-sha-tsv manuscript/ken/dvqa_train3142_image_sha256.tsv --require-m4-marker --out .session_backup/2026-10-26/dvqa_pilot/host_check.json
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

# v4: the image manifest is pinned on its own (IMAGE_SHA_TSV_PIN) so stage_images.py manifest mode can load the
# forbidden-hash set before that manifest exists.
PREREG_PINS = {
    "manuscript/prereg/2026-10-21_dev_pools/exclusion.json":
        "c52a96d18925b974878ae1a970c3f9133fb3482216676fd41871eeabb68cc77f",
    "manuscript/prereg/2026-10-22_c_stage1/lists.json":
        "5c479f03e8be544f4cd12b5d997b5dc92b6c622df061760cd02f6ba82f6b4371",
    "manuscript/prereg/2026-10-25_c_test/ov_test_files.tsv":
        "99d4fc49cc8283d1555d37b975cca5a32598ea0ec571d8bef8cf811df2c33695",
}
TRAIN3142_IDS_REL = "manuscript/ken/drivingvqa_train3142_ids.tsv"
N_TRAIN = 3142
PINS = {
    TRAIN3142_IDS_REL: "39219d099ea25ccb79ce7bae13aa61b7198b9409bd468a6075b2e0b4809afc45",
    **PREREG_PINS,
}
DEFAULT_IMAGE_SHA_TSV = ROOT / "manuscript/ken/dvqa_train3142_image_sha256.tsv"
IMAGE_SHA_TSV_PIN = "7734bb326ece11cc423865ea6e83ff37986daf6fdb467ab4ea181bfcc1970708"
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

# CC-104a W4: narrow .cache/huggingface/hub to hub/models--*
ALLOWLIST_SCAN_SKIP_REL_DIRS = (
    "vsps/.venv",
    "vsps/.git",
    "venv-lb",
    "venv-c1score",
    ".cache/huggingface/hub/models--*",
    "hub/models--*",
    ".cache/pip",
    "ncs-data/models",
    "ncs-data/vncorenlp",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_repo_pins(repo_root: Path = ROOT, pins: dict[str, str] = PINS) -> dict[str, str]:
    verified: dict[str, str] = {}
    for rel, expected_sha in sorted(pins.items()):
        p = repo_root / rel
        if not p.is_file():
            raise SystemExit(f"REFUSED: missing pinned file {p}")
        got = sha256_file(p)
        if got != expected_sha:
            raise SystemExit(f"REFUSED: SHA-256 mismatch for {rel}: got {got}, expected {expected_sha}")
        verified[rel] = got
    return verified


def load_expected_train_images(tsv_path: Path = ROOT / TRAIN3142_IDS_REL, n: int = N_TRAIN) -> list[str]:
    lines = tsv_path.read_text(encoding="utf-8").splitlines()[1:]
    rels = [line.split("\t")[1].strip() for line in lines if line.strip()]
    if len(rels) != n or len(set(rels)) != n:
        raise SystemExit(f"REFUSED: expected {n:,} distinct image filenames in {tsv_path}, got {len(set(rels))}")
    return sorted(rels)


def load_forbidden_sha256_set(repo_root: Path = ROOT) -> set[str]:
    verify_repo_pins(repo_root, PREREG_PINS)
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
    """CC-104a W2: Remove m3_rebuild/m4_rebuild marker logic. Require `/root/.vsps_machine_id` == 'm4';
    refuse 'm3' or missing. Optional M3 GPU-UUID refusal stays."""
    _ = require_m4_marker
    problems: list[str] = []
    env_mid = os.environ.get("VSPS_MACHINE_ID", "").strip().lower()
    if env_mid == "m3":
        problems.append("machine_id_env_is_m3")

    mid_file = scan_root / ".vsps_machine_id"
    if not mid_file.is_file():
        problems.append(f"missing_machine_id_file:{mid_file.as_posix()}")
    else:
        val = mid_file.read_text(encoding="utf-8").strip().lower()
        if val != "m4":
            problems.append(f"machine_id_file_not_m4:{val}")

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
    for prefix in ALLOWLIST_SCAN_SKIP_REL_DIRS:
        if prefix.endswith("*"):
            stem = prefix[:-1]
            if rel.startswith(stem):
                rest = rel[len(stem):]
                if rest and not rest.startswith("/"):
                    return True
        elif rel == prefix or rel.startswith(prefix + "/"):
            return True
    return False


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

    # 0. Check M4 vs M3 host identity (CC-104a W2)
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
                if name not in pin_map
                or (f"images/{name}" in staged_sha_map and staged_sha_map[f"images/{name}"] != pin_map[name])
            ]
            if sha_mismatches:
                problems.append(f"image_sha_manifest_mismatch:{len(sha_mismatches)}:e.g.{sha_mismatches[:3]}")

    # 3. CC-104a W3 & W4:
    # - Exempt git-tracked files (`git -C ROOT ls-files`) from the forbidden-name test; untracked files are still tested.
    # - Run the name test, datasets--*DrivingVQA* test, and *.zip outside models--* test BEFORE any allowlist skip.
    # - Images are still scanned everywhere outside pilot_img_dir and the narrowed allowlist.
    stray_images: list[str] = []
    forbidden_files: list[str] = []
    skip_resolved = repo_root_to_skip.resolve() if repo_root_to_skip and repo_root_to_skip.exists() else None
    vsps_under_scan = (scan_root / "vsps").resolve() if (scan_root / "vsps").exists() else None

    # CC-104b ruling 5 (c): the tracked exemption applies only under the repo base (ROOT or /root/vsps),
    # never to a copy of a tracked path elsewhere under scan_root.
    git_tracked_rels: set[str] = set()
    git_ls_cache: dict[str, set[str]] = getattr(run_host_check, "_git_ls_cache", {})
    setattr(run_host_check, "_git_ls_cache", git_ls_cache)
    for git_cand in (skip_resolved, vsps_under_scan):
        if git_cand is not None and (git_cand / ".git").exists():
            cand_key = str(git_cand)
            if cand_key not in git_ls_cache:
                try:
                    ls_out = subprocess.check_output(
                        ["git", "-C", cand_key, "ls-files"],
                        text=True,
                        stderr=subprocess.DEVNULL,
                        timeout=10,
                    )
                    git_ls_cache[cand_key] = {ln.strip() for ln in ls_out.splitlines() if ln.strip()}
                except Exception:
                    git_ls_cache[cand_key] = set()
            git_tracked_rels |= git_ls_cache[cand_key]

    repo_bases = [b for b in (skip_resolved, vsps_under_scan) if b is not None]
    # CC-104b ruling 5 (d): skip only <repo>/.git/, not every directory named .git
    repo_git_dirs = [b / ".git" for b in repo_bases]
    for root_to_walk in sorted({scan_root, dvqa_dir}):
        if not root_to_walk.exists():
            continue
        for p in sorted(root_to_walk.rglob("*")):
            if not p.is_file():
                continue
            p_posix = p.as_posix()
            rp = p.resolve()
            rp_posix = rp.as_posix()
            if any(g in p.parents or g in rp.parents for g in repo_git_dirs):
                continue
            low_posix = p_posix.lower()
            low_rp_posix = rp_posix.lower()

            # W4: Run name test, datasets--*DrivingVQA* refusal, and *.zip outside models--* refusal BEFORE allowlist skip
            has_dvqa_ds_cache = (
                ("datasets--" in low_posix and "drivingvqa" in low_posix)
                or ("datasets--" in low_rp_posix and "drivingvqa" in low_rp_posix)
            )
            in_models_cache = ("/models--" in p_posix) or ("/models--" in rp_posix)
            is_zip_outside_models = (rp.suffix.lower() == ".zip") and not in_models_cache
            is_tracked = any(
                (base in rp.parents and rp.relative_to(base).as_posix() in git_tracked_rels)
                or (base in p.parents and p.relative_to(base).as_posix() in git_tracked_rels)
                for base in repo_bases
            )
            is_bad_name = (not is_tracked) and is_forbidden_filename(rp.name)

            if has_dvqa_ds_cache or is_zip_outside_models or is_bad_name:
                forbidden_files.append(rp_posix)

            if is_in_allowlisted_skip_dir(p, scan_root) or is_in_allowlisted_skip_dir(rp, scan_root):
                continue

            if rp.suffix.lower() in IMAGE_EXTS:
                if pilot_img_dir not in rp.parents:
                    stray_images.append(rp_posix)
                    h_other = sha256_file(rp)
                    if h_other in forbidden_shas:
                        forbidden_sha_hits.append(f"{rp_posix}:{h_other[:12]}")

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
    expected_rels = load_expected_train_images()
    forbidden_shas = load_forbidden_sha256_set(ROOT)
    assert len(verified_pins) == 4
    assert len(expected_rels) == N_TRAIN
    assert len(forbidden_shas) == 8179
    # v4: the pinned image manifest lists exactly the 3,142 train images, none with a forbidden hash
    assert sha256_file(DEFAULT_IMAGE_SHA_TSV) == IMAGE_SHA_TSV_PIN
    manifest_rows = [ln.split("\t") for ln in DEFAULT_IMAGE_SHA_TSV.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert [r[0] for r in manifest_rows] == expected_rels
    assert not ({r[1] for r in manifest_rows} & forbidden_shas)

    sub_expected = expected_rels[:5]
    sample_forbidden_sha = sorted(forbidden_shas)[0]

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scan_root = tmp_path / "root"
        dvqa_dir = scan_root / "dvqa_pilot"
        img_dir = dvqa_dir / "images"
        img_dir.mkdir(parents=True)
        (dvqa_dir / "train.json").write_text("{}", encoding="utf-8")

        # CC-104a W2: Both m3_rebuild and m4_rebuild marker logs present under outputs/claude_ops + .vsps_machine_id == 'm4' -> pass
        ops_dir = scan_root / "outputs/claude_ops"
        ops_dir.mkdir(parents=True)
        (ops_dir / "m3_rebuild_2026-10-26.log").write_text("M3 rebuild mirror\n", encoding="utf-8")
        (ops_dir / "m4_rebuild_2026-10-26.log").write_text("M4 rebuild ok\n", encoding="utf-8")
        mid_file = scan_root / ".vsps_machine_id"
        mid_file.write_text("m4\n", encoding="utf-8")

        # CC-104a W3: git-tracked *_test.json and oiv7_labels.json under vsps/ must be exempted and pass
        for tracked_rel in (
            "data/dedup/ktvic_dup_train_test.json",
            "data/results/upe/test/upe_mbr_ktvic_test.json",
            "data/xm3600/oiv7_labels.json",
        ):
            tf = scan_root / "vsps" / tracked_rel
            tf.parent.mkdir(parents=True, exist_ok=True)
            tf.write_text("{}", encoding="utf-8")

        # CC-104a W4: allowlisted venv icon and hub/models--* icon pass
        venv_img = scan_root / "venv-lb/lib/python3.10/site-packages/pkg_icon.png"
        venv_img.parent.mkdir(parents=True)
        venv_img.write_text("allowlisted_venv_icon", encoding="utf-8")
        hub_model_img = scan_root / ".cache/huggingface/hub/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/cc59/asset.png"
        hub_model_img.parent.mkdir(parents=True)
        hub_model_img.write_text("allowlisted_model_icon", encoding="utf-8")

        manifest_lines: list[str] = []
        for rel in sub_expected:
            f_img = img_dir / Path(rel).name
            f_img.write_text(f"clean_image_{rel}", encoding="utf-8")
            manifest_lines.append(f"{rel}\t{sha256_file(f_img)}")

        synth_manifest = tmp_path / "sub_image_sha256.tsv"
        synth_manifest.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

        # 1. Clean configuration passes with marker logs present + machine_id == 'm4' + tracked *_test.json + hub/models--*
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

        # 2. CC-104a W2: machine_id == 'm3' -> refused; missing .vsps_machine_id -> refused
        mid_file.write_text("m3\n", encoding="utf-8")
        res_m3 = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas,
            image_sha_manifest=synth_manifest,
            require_train_json_sha=False,
            require_image_manifest_pin=False,
        )
        assert res_m3["ok"] is False and any("machine_id_file_not_m4" in p for p in res_m3["problems"])

        mid_file.unlink()
        res_missing_mid = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas,
            image_sha_manifest=synth_manifest,
            require_train_json_sha=False,
            require_image_manifest_pin=False,
        )
        assert res_missing_mid["ok"] is False and any("missing_machine_id_file" in p for p in res_missing_mid["problems"])
        mid_file.write_text("m4\n", encoding="utf-8")

        # 3. CC-104a W3: untracked /root/x/test.json refused
        untracked_test = scan_root / "x/test.json"
        untracked_test.parent.mkdir(parents=True, exist_ok=True)
        untracked_test.write_text("{}", encoding="utf-8")
        res_untracked = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas,
            image_sha_manifest=synth_manifest,
            require_train_json_sha=False,
            require_image_manifest_pin=False,
        )
        assert res_untracked["ok"] is False and res_untracked["forbidden_filename_count"] == 1
        untracked_test.unlink()

        # 4. CC-104a W4: hub/datasets--EPFL-DrivingVQA--DrivingVQA/.../test.json refused; /root/x/images.zip refused
        dvqa_hub_test = scan_root / ".cache/huggingface/hub/datasets--EPFL-DrivingVQA--DrivingVQA/snapshots/02ce/test.json"
        dvqa_hub_test.parent.mkdir(parents=True, exist_ok=True)
        dvqa_hub_test.write_text("{}", encoding="utf-8")
        res_dvqa_hub = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas,
            image_sha_manifest=synth_manifest,
            require_train_json_sha=False,
            require_image_manifest_pin=False,
        )
        assert res_dvqa_hub["ok"] is False and res_dvqa_hub["forbidden_filename_count"] >= 1
        dvqa_hub_test.unlink()

        bad_zip = scan_root / "x/images.zip"
        bad_zip.write_text("zip_payload", encoding="utf-8")
        res_bad_zip = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas,
            image_sha_manifest=synth_manifest,
            require_train_json_sha=False,
            require_image_manifest_pin=False,
        )
        assert res_bad_zip["ok"] is False and res_bad_zip["forbidden_filename_count"] == 1
        bad_zip.unlink()

        # 5. Refusal of an unlisted image in pilot folder
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

        # 6. Refusal of a stray image in /root outside pilot folder and outside allowlist
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

        # 7. Refusal of test-like filenames (test.json, ct_test.json, c_test_run.json)
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

        # 8. Refusal of an image whose SHA-256 is in the forbidden set
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

        # 9b. CC-104b ruling 5 (c): an untracked copy of a tracked path outside the repo base is refused
        copy_of_tracked = scan_root / "data/dedup/ktvic_dup_train_test.json"
        copy_of_tracked.parent.mkdir(parents=True, exist_ok=True)
        copy_of_tracked.write_text("{}", encoding="utf-8")
        res_copy = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas,
            image_sha_manifest=synth_manifest,
            require_train_json_sha=False,
            require_image_manifest_pin=False,
        )
        assert res_copy["ok"] is False and res_copy["forbidden_filename_count"] == 1
        copy_of_tracked.unlink()

        # 9c. CC-104b ruling 5 (d): files inside a .git directory other than <repo>/.git/ are tested;
        # <repo>/.git/ (here /root/vsps/.git) is still skipped
        other_git = scan_root / "x/.git"
        other_git.mkdir(parents=True, exist_ok=True)
        for name in ("foo.jpg", "images.zip", "test.json"):
            (other_git / name).write_text("x", encoding="utf-8")
        repo_git_obj = scan_root / "vsps/.git/objects/test.json"
        repo_git_obj.parent.mkdir(parents=True, exist_ok=True)
        repo_git_obj.write_text("x", encoding="utf-8")
        res_git = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas,
            image_sha_manifest=synth_manifest,
            require_train_json_sha=False,
            require_image_manifest_pin=False,
        )
        assert res_git["ok"] is False
        assert res_git["forbidden_filename_count"] == 2 and res_git["stray_images_outside_pilot_count"] == 1, res_git
        for name in ("foo.jpg", "images.zip", "test.json"):
            (other_git / name).unlink()
        repo_git_obj.unlink()

        # 9. CC-104a W10 preflight check with an empty dvqa_pilot folder -> only missing_* problems
        for f_img in list(img_dir.glob("*")):
            f_img.unlink()
        img_dir.rmdir()
        (dvqa_dir / "train.json").unlink()
        res_empty = run_host_check(
            dvqa_dir,
            scan_root,
            sub_expected,
            forbidden_shas,
            image_sha_manifest=synth_manifest,
            require_train_json_sha=True,
            require_image_manifest_pin=False,
        )
        assert res_empty["ok"] is False
        assert all(p.startswith("missing_") for p in res_empty["problems"]), f"W10 empty check had non-missing problem: {res_empty['problems']}"

    print(json.dumps({
        "script": "host_check.py",
        "selftest": "OK",
        "verified_pins_count": len(verified_pins),
        "train3142_expected_images": len(expected_rels),
        "image_sha_tsv_pin": IMAGE_SHA_TSV_PIN,
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
    expected_rels = load_expected_train_images()
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
