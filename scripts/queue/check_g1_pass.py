#!/usr/bin/env python3
"""Enforce and execute Gate G-1 PASS in code before any GPU queue job runs.

Tightened per Claude 2026-10-15 00:42 UTC (#2 & #3), 01:12 UTC (#1 & #3), and 01:30 UTC (#1):
- Only accepts a `g1_gate_<host>*.json` file with `verdict == "PASS"` if:
  1. `git_head_sha` matches the machine's current `git -C /root/vsps rev-parse HEAD`
  2. `checkpoint_resume_hook_sha256` matches the current SHA-256 of `scripts/checkpoint_resume_hook.py`
  3. `sitecustomize_symlink_target` matches the active venv's `sitecustomize.py` symlink target
  4. `segmenter == "rdrsegmenter"`
  5. `chair_v1_raw_tone.byte_exact_json_match_vs_committed is True`
  6. `chair_v1_raw_tone.exact_match_vs_committed is True`
  7. `max_metric_abs_diff == 0`
  8. `n_adapters_verified == 23`, `canonical_adapters_file_sha256` matches `scripts/queue/adapters_canonical.sha256`,
     and `adapter_mismatches == {}` (all 23 adapters match `scripts/queue/adapters_canonical.sha256` 100%)
  9. `data_and_weights_audit.all_ok is True` (all dataset JSON SHA-256s, image counts/manifests for
     `ktvic=4327`, `uitviic=3850`, `xm3600=3600`, and `Qwen3-VL-8B-Instruct-0c351dd/SHA256SUMS` verified)
- When `HEAD` or venv changes, `--run-g1` runs the G-1 gate and writes a new
  immutable `/root/outputs/g1_gate_<host>_v<N>.json` (`chmod 444`) without
  overwriting any prior gate file.
- Contains zero float literals in AST.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_REPO = Path("/root/vsps")
DEFAULT_NCS = Path("/root/ncs-data")
DEFAULT_OUT = Path("/root/outputs")
MIN_ADAPTERS = 23
METRIC_KEYS = ("BLEU-1", "BLEU-2", "BLEU-3", "BLEU-4", "METEOR", "ROUGE-L", "CIDEr")

CANONICAL_DATASET_JSON_SHA256 = {
    "datasets/ktvic/train_data.json": "72ee9b57c350fb5f215e1f04701c515a51e5e415240e51a77c8ce00ce6316a0f",
    "datasets/ktvic/test_data.json": "cc22ec6a8883773cb23c87ad5b64925f5a53c21982117274b53621f454e7ebbf",
    "datasets/uitviic/train_data.json": "441d22d29eb7aa12d32d49e330778a4a918c3a9413c23294a9daec92a238d110",
    "datasets/uitviic/val_data.json": "fee7d116683670ef5ce14f405594aa73bb08dd1bdbf1f2cdc3f9e01bbfa9b044",
    "datasets/uitviic/test_data.json": "54abc0fb068ad1108d7d57b21328d4d68bcf8f41aa168f80ec7c275fb4ac8214",
    "datasets/xm3600/test_data.json": "0a613214f95605ff137879f70cb84f8160172c28a650317766ac4a1d9c3b72e8",
}

CANONICAL_IMAGE_COUNTS = {
    "datasets/ktvic/images": (4327, ("datasets/ktvic/train_data.json", "datasets/ktvic/test_data.json")),
    "datasets/uitviic/images": (
        3850,
        ("datasets/uitviic/train_data.json", "datasets/uitviic/val_data.json", "datasets/uitviic/test_data.json"),
    ),
    "datasets/xm3600/images": (3600, ("datasets/xm3600/test_data.json",)),
}

QWEN3VL_SHA256SUMS_REL = "models/Qwen3-VL-8B-Instruct-0c351dd/SHA256SUMS"
QWEN3VL_SHA256SUMS_EXPECTED = "dc7bd4a45eb3c56e00c56f68cd937871258b679b741949bd38a383950ffc52d8"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_canonical_adapters(repo: Path) -> tuple[Path, str, dict[str, str]]:
    canon_path = repo / "scripts/queue/adapters_canonical.sha256"
    canon_sha = _sha256(canon_path)
    expected: dict[str, str] = {}
    for line in canon_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        sha, rel = line.strip().split(None, 1)
        key = rel.removesuffix("/adapter_model.safetensors")
        expected[key] = sha
    return canon_path, canon_sha, expected


def _audit_data_and_weights(ncs: Path, verify_weight_hashes: bool = False) -> dict[str, object]:
    json_mismatches: dict[str, dict[str, str | None]] = {}
    json_verified: dict[str, str] = {}
    for rel, exp_sha in CANONICAL_DATASET_JSON_SHA256.items():
        p = ncs / rel
        if not p.is_file():
            json_mismatches[rel] = {"expected": exp_sha, "observed": None}
        else:
            obs = _sha256(p)
            json_verified[rel] = obs
            if obs != exp_sha:
                json_mismatches[rel] = {"expected": exp_sha, "observed": obs}

    image_dirs: dict[str, dict[str, object]] = {}
    image_ok = True
    for rel_dir, (exp_count, ref_jsons) in CANONICAL_IMAGE_COUNTS.items():
        img_dir = ncs / rel_dir
        files_on_disk = {p.name for p in img_dir.iterdir() if p.is_file() and p.stat().st_size > 0} if img_dir.is_dir() else set()
        missing_refs: list[str] = []
        referenced_names: set[str] = set()
        for rj in ref_jsons:
            jp = ncs / rj
            if jp.is_file():
                data = json.loads(jp.read_text(encoding="utf-8"))
                for img in data.get("images", []):
                    fname = img.get("file_name") or img.get("filename")
                    if fname:
                        referenced_names.append(fname) if isinstance(referenced_names, list) else referenced_names.add(fname)
        missing_refs = sorted(referenced_names - files_on_disk)
        dir_pass = (len(files_on_disk) == exp_count) and (len(missing_refs) == 0)
        if not dir_pass:
            image_ok = False
        image_dirs[rel_dir] = {
            "expected_file_count": exp_count,
            "observed_nonempty_files": len(files_on_disk),
            "referenced_unique_images": len(referenced_names),
            "missing_referenced_count": len(missing_refs),
            "missing_referenced_sample": missing_refs[:10],
            "ok": dir_pass,
        }

    qwen_manifest = ncs / QWEN3VL_SHA256SUMS_REL
    qwen_dir = qwen_manifest.parent
    qwen_manifest_sha = _sha256(qwen_manifest) if qwen_manifest.is_file() else None
    qwen_missing_or_bad: list[str] = []
    qwen_files_checked = 0
    if qwen_manifest.is_file():
        for line in qwen_manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            exp_s, fname = line.strip().split(None, 1)
            fname = fname.lstrip("*./")
            fp = qwen_dir / fname
            qwen_files_checked += 1
            if not fp.is_file() or fp.stat().st_size == 0:
                qwen_missing_or_bad.append(f"{fname}:missing")
            elif verify_weight_hashes:
                obs_s = _sha256(fp)
                if obs_s != exp_s:
                    qwen_missing_or_bad.append(f"{fname}:sha_mismatch:{obs_s}")
    else:
        qwen_missing_or_bad.append("SHA256SUMS:missing")

    qwen_ok = (
        qwen_manifest_sha == QWEN3VL_SHA256SUMS_EXPECTED
        and qwen_files_checked == 14
        and len(qwen_missing_or_bad) == 0
    )
    all_ok = (len(json_mismatches) == 0) and image_ok and qwen_ok
    return {
        "dataset_json_sha256": json_verified,
        "dataset_json_mismatches": json_mismatches,
        "image_directories": image_dirs,
        "qwen3vl_weights": {
            "manifest_rel": QWEN3VL_SHA256SUMS_REL,
            "expected_manifest_sha256": QWEN3VL_SHA256SUMS_EXPECTED,
            "observed_manifest_sha256": qwen_manifest_sha,
            "files_listed": qwen_files_checked,
            "full_shard_sha256_verified": verify_weight_hashes,
            "missing_or_mismatched": qwen_missing_or_bad,
            "ok": qwen_ok,
        },
        "all_ok": all_ok,
    }


import shutil
import tempfile


def _run_checkpoint_smoke_test(repo: Path) -> dict[str, object]:
    py_bin = str(repo / ".venv/bin/python")
    with tempfile.TemporaryDirectory(prefix="g1_ckpt_smoke_") as tmp:
        tmp_path = Path(tmp)
        out_run = tmp_path / "runs" / "smoke_s42"
        mirror_root = tmp_path / "mirror_runs"
        smoke_script = tmp_path / "train_stage2.py"
        smoke_script.write_text(
            "import json, sys, torch\n"
            "from torch.utils.data import Dataset\n"
            "from transformers import Trainer, TrainingArguments\n"
            "class _TinyDS(Dataset):\n"
            "    def __len__(self): return 4\n"
            "    def __getitem__(self, i):\n"
            "        return {'x': torch.ones(2), 'labels': torch.ones(2)}\n"
            "class _TinyModel(torch.nn.Module):\n"
            "    def __init__(self):\n"
            "        super().__init__()\n"
            "        self.w = torch.nn.Linear(2, 2)\n"
            "    def forward(self, x, labels=None):\n"
            "        out = self.w(x)\n"
            "        loss = ((out - labels) ** 2).mean()\n"
            "        return {'loss': loss, 'logits': out}\n"
            "args = TrainingArguments(\n"
            "    output_dir=sys.argv[1],\n"
            "    max_steps=3,\n"
            "    per_device_train_batch_size=1,\n"
            "    save_strategy='epoch',\n"
            "    save_safetensors=False,\n"
            "    report_to='none',\n"
            "    use_cpu=True,\n"
            ")\n"
            "trainer = Trainer(model=_TinyModel(), args=args, train_dataset=_TinyDS())\n"
            "trainer.train()\n"
            "print(json.dumps({'save_strategy': str(args.save_strategy), 'save_steps': int(args.save_steps)}))\n",
            encoding="utf-8",
        )
        env = dict(
            os.environ,
            RESCAP_SAVE_STEPS="2",
            RESCAP_SAVE_LIMIT="2",
            RESCAP_MIRROR_ROOT=str(mirror_root),
            CUDA_VISIBLE_DEVICES="",
        )
        proc = subprocess.run(
            [py_bin, str(smoke_script), str(out_run)],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        ckpt_dir = out_run / "checkpoint-2"
        mirror_ckpt_dir = mirror_root / "smoke_s42" / "checkpoint-2"
        manifest_file = out_run / "resume_manifest.json"
        mirror_manifest_file = mirror_root / "smoke_s42" / "resume_manifest.json"
        hook_log_seen = "[checkpoint_resume_hook] Enabled checkpointing: save_steps=2" in (proc.stdout + proc.stderr)
        ok = (
            proc.returncode == 0
            and hook_log_seen
            and ckpt_dir.is_dir()
            and any(ckpt_dir.iterdir())
            and mirror_ckpt_dir.is_dir()
            and manifest_file.is_file()
            and mirror_manifest_file.is_file()
        )
        return {
            "returncode": proc.returncode,
            "hook_banner_observed": hook_log_seen,
            "checkpoint_2_created": ckpt_dir.is_dir(),
            "checkpoint_2_files": sorted(p.name for p in ckpt_dir.iterdir()) if ckpt_dir.is_dir() else [],
            "mirror_checkpoint_2_created": mirror_ckpt_dir.is_dir(),
            "resume_manifest_created": manifest_file.is_file(),
            "mirror_resume_manifest_created": mirror_manifest_file.is_file(),
            "ok": ok,
        }


def _current_machine_state(repo: Path) -> dict[str, str | None]:
    head_sha = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()
    hook_path = repo / "scripts/checkpoint_resume_hook.py"
    hook_sha = _sha256(hook_path)
    _, canon_sha, _ = _load_canonical_adapters(repo)
    site_venv = repo / ".venv/lib/python3.10/site-packages/sitecustomize.py"
    site_target = os.readlink(site_venv) if site_venv.is_symlink() else None
    sys_site = Path("/usr/lib/python3.10/sitecustomize.py")
    sys_site_target = os.readlink(sys_site) if sys_site.is_symlink() else None
    return {
        "head_sha": head_sha,
        "hook_sha": hook_sha,
        "canon_adapters_sha": canon_sha,
        "site_venv": str(site_venv),
        "site_target": site_target,
        "sys_site": str(sys_site),
        "sys_site_target": sys_site_target,
    }


def verify_g1_gate(
    repo: Path = DEFAULT_REPO,
    ncs: Path = DEFAULT_NCS,
    out_dir: Path = DEFAULT_OUT,
    host: str | None = None,
) -> tuple[bool, dict[str, object]]:
    host = host or socket.gethostname()
    state = _current_machine_state(repo)
    _, _, expected_adapters = _load_canonical_adapters(repo)
    expected_target = str(repo / "scripts/checkpoint_resume_hook.py")
    live_data_audit = _audit_data_and_weights(ncs, verify_weight_hashes=False)
    candidates = sorted(out_dir.glob(f"g1_gate_{host}*.json"))
    matched: list[dict[str, object]] = []
    for p in candidates:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        chair_v1 = d.get("chair_v1_raw_tone")
        if not isinstance(chair_v1, dict):
            continue
        gate_adapters = d.get("adapter_sha256")
        adapters_match_canon = isinstance(gate_adapters, dict) and all(
            gate_adapters.get(k) == v for k, v in expected_adapters.items()
        )
        gate_data_audit = d.get("data_and_weights_audit")
        gate_data_ok = isinstance(gate_data_audit, dict) and (gate_data_audit.get("all_ok") is True)
        gate_smoke = d.get("checkpoint_smoke_test")
        gate_smoke_ok = isinstance(gate_smoke, dict) and (gate_smoke.get("ok") is True)
        ok = (
            d.get("verdict") == "PASS"
            and d.get("machine_id") == host
            and d.get("segmenter") == "rdrsegmenter"
            and d.get("git_head_sha") == state["head_sha"]
            and d.get("checkpoint_resume_hook_sha256") == state["hook_sha"]
            and d.get("canonical_adapters_file_sha256") == state["canon_adapters_sha"]
            and d.get("adapter_mismatches") == {}
            and adapters_match_canon
            and gate_data_ok
            and gate_smoke_ok
            and live_data_audit["all_ok"] is True
            and d.get("sitecustomize_symlink_target") == state["site_target"]
            and state["site_target"] == expected_target
            and state["sys_site_target"] == expected_target
            and chair_v1.get("byte_exact_json_match_vs_committed") is True
            and chair_v1.get("exact_match_vs_committed") is True
            and d.get("max_metric_abs_diff") == 0
            and int(d.get("n_adapters_verified", 0)) >= MIN_ADAPTERS
        )
        if ok:
            matched.append(
                {
                    "file": p.name,
                    "path": str(p),
                    "timestamp_utc": d.get("timestamp_utc"),
                    "git_head_sha": d.get("git_head_sha"),
                    "checkpoint_resume_hook_sha256": d.get("checkpoint_resume_hook_sha256"),
                    "canonical_adapters_file_sha256": d.get("canonical_adapters_file_sha256"),
                    "checkpoint_smoke_test_ok": gate_smoke_ok,
                    "n_adapters_verified": d.get("n_adapters_verified"),
                    "sha256": _sha256(p),
                }
            )
    if not matched:
        return False, {
            "host": host,
            "current_head_sha": state["head_sha"],
            "current_hook_sha256": state["hook_sha"],
            "current_canonical_adapters_sha256": state["canon_adapters_sha"],
            "current_sitecustomize_target": state["site_target"],
            "live_data_and_weights_all_ok": live_data_audit["all_ok"],
            "candidates_checked": [p.name for p in candidates],
        }
    return True, matched[-1]


def run_g1_gate(
    repo: Path = DEFAULT_REPO,
    ncs: Path = DEFAULT_NCS,
    out_dir: Path = DEFAULT_OUT,
) -> Path:
    host = socket.gethostname()
    state = _current_machine_state(repo)
    _, canon_sha, expected_adapters = _load_canonical_adapters(repo)
    train_sha = _sha256(repo / "scripts/train_stage2.py")
    eval_sha = _sha256(repo / "scripts/evaluate.py")
    chair_sha = _sha256(repo / "rescap/chair.py")

    ref_path = repo / "data/results/p1assist_s42-short.json"
    ref_json = json.loads(ref_path.read_text(encoding="utf-8"))
    preds_path = repo / "data/results/p1assist_s42-short.preds.json"
    py_bin = str(repo / ".venv/bin/python")

    out_v1 = Path("/tmp/g1_gate_check_p1assist_s42-short.v1.json")
    env_v1 = dict(os.environ, RESCAP_RAW_TONE="1", RESCAP_G1_BYTE_CHECK="1")
    t0 = time.time()
    subprocess.run(
        [
            py_bin,
            str(repo / "scripts/evaluate.py"),
            "--predictions",
            str(preds_path),
            "--prompt",
            "short",
            "--name",
            "p1assist_s42-short",
            "--out",
            str(out_v1),
        ],
        check=True,
        env=env_v1,
    )
    elapsed_v1 = round(time.time() - t0, 3)
    got_v1 = json.loads(out_v1.read_text(encoding="utf-8"))

    out_v2 = Path("/tmp/g1_gate_check_p1assist_s42-short.v2.json")
    env_v2 = dict(os.environ, RESCAP_RAW_TONE="0", RESCAP_G1_BYTE_CHECK="1")
    subprocess.run(
        [
            py_bin,
            str(repo / "scripts/evaluate.py"),
            "--predictions",
            str(preds_path),
            "--prompt",
            "short",
            "--name",
            "p1assist_s42-short",
            "--out",
            str(out_v2),
        ],
        check=True,
        env=env_v2,
    )
    got_v2 = json.loads(out_v2.read_text(encoding="utf-8"))

    ref_sc = ref_json["results"][0]["scores_scaled_x100"]
    got_sc = got_v1["results"][0]["scores_scaled_x100"]
    metric_diffs = {k: abs(got_sc[k] - ref_sc[k]) for k in METRIC_KEYS}
    max_metric_diff = max(metric_diffs.values())

    ref_ch = ref_json["chair"]
    got_ch_v1 = got_v1["chair"]
    chair_v1_exact = (
        got_ch_v1["CHAIR_s"] == ref_ch["CHAIR_s"]
        and got_ch_v1["CHAIR_i"] == ref_ch["CHAIR_i"]
        and got_ch_v1["mentions_per_caption"] == ref_ch["mentions_per_caption"]
    )
    byte_exact_v1 = out_v1.read_bytes() == ref_path.read_bytes()

    adapter_hashes: dict[str, str] = {}
    adapter_mismatches: dict[str, dict[str, str | None]] = {}
    for key, exp_sha in sorted(expected_adapters.items()):
        ap = ncs / key / "adapter_model.safetensors"
        if not ap.is_file():
            adapter_mismatches[key] = {"expected": exp_sha, "observed": None}
        else:
            obs_sha = _sha256(ap)
            adapter_hashes[key] = obs_sha
            if obs_sha != exp_sha:
                adapter_mismatches[key] = {"expected": exp_sha, "observed": obs_sha}

    data_audit = _audit_data_and_weights(ncs, verify_weight_hashes=False)
    smoke_test = _run_checkpoint_smoke_test(repo)

    expected_target = str(repo / "scripts/checkpoint_resume_hook.py")
    gate_ok = (
        max_metric_diff == 0
        and chair_v1_exact
        and byte_exact_v1
        and got_v1["results"][0]["segmenter"] == "rdrsegmenter"
        and state["site_target"] == expected_target
        and state["sys_site_target"] == expected_target
        and len(adapter_hashes) == MIN_ADAPTERS
        and len(adapter_mismatches) == 0
        and data_audit["all_ok"] is True
        and smoke_test["ok"] is True
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    ver_idx = 2
    while (out_dir / f"g1_gate_{host}_v{ver_idx}.json").exists():
        ver_idx += 1
    out_gate = out_dir / f"g1_gate_{host}_v{ver_idx}.json"

    v1_gate = out_dir / f"g1_gate_{host}.json"
    ts_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    report = {
        "gate_version": f"v{ver_idx}",
        "machine_id": host,
        "hostname": host,
        "timestamp_utc": ts_utc,
        "v1_gate_file_preserved": str(v1_gate) if v1_gate.exists() else None,
        "v1_gate_sha256_preserved": _sha256(v1_gate) if v1_gate.exists() else None,
        "git_head_sha": state["head_sha"],
        "checkpoint_resume_hook_path": "scripts/checkpoint_resume_hook.py",
        "checkpoint_resume_hook_sha256": state["hook_sha"],
        "canonical_adapters_file": "scripts/queue/adapters_canonical.sha256",
        "canonical_adapters_file_sha256": canon_sha,
        "sitecustomize_symlink": state["site_venv"],
        "sitecustomize_symlink_target": state["site_target"],
        "sys_sitecustomize_symlink": state["sys_site"],
        "sys_sitecustomize_symlink_target": state["sys_site_target"],
        "train_stage2_sha256": train_sha,
        "evaluate_py_sha256": eval_sha,
        "chair_py_sha256": chair_sha,
        "resumed_from_step": [],
        "segmenter": got_v1["results"][0]["segmenter"],
        "elapsed_sec": elapsed_v1,
        "scores_scaled_x100": got_sc,
        "reference_scores_scaled_x100": ref_sc,
        "metric_abs_diffs": metric_diffs,
        "max_metric_abs_diff": max_metric_diff,
        "chair_v1_raw_tone": {
            "CHAIR_s": got_ch_v1["CHAIR_s"],
            "CHAIR_i": got_ch_v1["CHAIR_i"],
            "mentions_per_caption": got_ch_v1["mentions_per_caption"],
            "exact_match_vs_committed": chair_v1_exact,
            "byte_exact_json_match_vs_committed": byte_exact_v1,
        },
        "chair_v2_tone_norm": {
            "CHAIR_s": got_v2["chair"]["CHAIR_s"],
            "CHAIR_i": got_v2["chair"]["CHAIR_i"],
            "mentions_per_caption": got_v2["chair"]["mentions_per_caption"],
        },
        "n_adapters_verified": len(adapter_hashes),
        "adapter_mismatches": adapter_mismatches,
        "adapter_sha256": adapter_hashes,
        "data_and_weights_audit": data_audit,
        "checkpoint_smoke_test": smoke_test,
        "verdict": "PASS" if gate_ok else "FAIL",
    }
    out_gate.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(out_gate, 0o444)
    if not gate_ok:
        raise RuntimeError(f"G-1 gate failed: {out_gate}")
    return out_gate


def _self_check() -> int:
    src = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    floats = [
        n.value
        for n in ast.walk(tree)
        if isinstance(n, ast.Constant) and isinstance(n.value, float)
    ]
    assert not floats, f"found float literals in AST: {floats}"
    repo = Path(__file__).resolve().parents[2]
    canon_path, canon_sha, expected = _load_canonical_adapters(repo)
    assert len(expected) == MIN_ADAPTERS, len(expected)
    print(
        json.dumps(
            {
                "status": "ok",
                "file": str(Path(__file__).name),
                "sha256": _sha256(Path(__file__)),
                "canonical_adapters_file": str(canon_path.relative_to(repo)),
                "canonical_adapters_sha256": canon_sha,
                "canonical_adapters_count": len(expected),
            }
        )
    )
    return 0


def main(argv: list[str]) -> int:
    if "--self-check" in argv:
        return _self_check()
    if "--run-g1" in argv:
        out_gate = run_g1_gate()
        print(f"G1_GATE_GENERATED {out_gate} sha256={_sha256(out_gate)}")
    ok, info = verify_g1_gate()
    if not ok:
        sys.stderr.write(f"BLOCKED_BY_G1_GATE: {json.dumps(info, ensure_ascii=False)}\n")
        return 2
    print(
        f"G1_GATE_ENFORCED_OK host={socket.gethostname()} "
        f"file={info['file']} ts={info['timestamp_utc']} "
        f"head={info['git_head_sha']} hook={info['checkpoint_resume_hook_sha256']} "
        f"canon={info['canonical_adapters_file_sha256']} "
        f"sha256={info['sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
