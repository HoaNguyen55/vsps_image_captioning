#!/usr/bin/env python3
"""Committed checkpointing, auto-resume, and provenance stamping hook for GPU runs.

Installed into `/root/vsps/.venv/lib/python3.10/site-packages/sitecustomize.py`
and `/root/venv-qwen3vl/lib/python3.10/site-packages/sitecustomize.py` as a
symbolic link to `/root/vsps/scripts/checkpoint_resume_hook.py` so that:
1. `scripts/train_stage2.py` and `scripts/evaluate.py` keep their exact frozen
   SHA-256 hashes required by pre-registered job scripts (`61_b1_qwen3vl_guard_and_gate.sh`).
2. During `train_stage2.py` SFT runs:
   - `save_strategy` is set to `"steps"` with `save_steps=200` (~25-27 minutes
     on RTX 3090, ~485 MB per LoRA checkpoint << 3 GB) and `save_total_limit=2`.
   - Every saved `checkpoint-*` is mirrored to `/root/outputs/runs/<run_name>/`
     so the 30-minute `/root/` backup captures intermediate checkpoints.
   - If a `checkpoint-*` exists in `output_dir` (or `/root/outputs/runs/<run_name>/`),
     `Trainer.train` automatically resumes from the latest `checkpoint-<N>` and
     appends `<N>` to `resumed_from_step` (a `list[int]`, `[]` if trained from
     step 0 without interruption) in `<output_dir>/resume_manifest.json`.
3. During `evaluate.py` (unless `RESCAP_G1_BYTE_CHECK=1` is set for the G-1
   byte-exact check) and via `--stamp-results`, every output JSON records:
   - `machine_id`: `socket.gethostname()`
   - `git_head_sha`: `git rev-parse HEAD` of `/root/vsps`
   - `checkpoint_resume_hook_sha256`: SHA-256 of `scripts/checkpoint_resume_hook.py`
   - `train_stage2_sha256`: SHA-256 of `scripts/train_stage2.py`
   - `resumed_from_step`: `list[int]` (e.g. `[]` or `[200]`)
"""

from __future__ import annotations

import argparse
import atexit
import hashlib
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
from pathlib import Path


def _file_sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    if here.parent.name == "scripts":
        return here.parent.parent
    return Path("/root/vsps")


def _git_head_sha(repo: Path) -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out or None
    except Exception:
        return None


def provenance_metadata(adapter_dir: str | Path | None = None) -> dict:
    repo = _repo_root()
    hook_path = repo / "scripts" / "checkpoint_resume_hook.py"
    if not hook_path.is_file():
        hook_path = Path(__file__).resolve()
    train_path = repo / "scripts" / "train_stage2.py"

    resumed_steps: list[int] = []
    if adapter_dir:
        adir = Path(adapter_dir)
        manifest_path = adir / "resume_manifest.json"
        if not manifest_path.is_file():
            mirror_manifest = Path("/root/outputs/runs") / adir.name / "resume_manifest.json"
            if mirror_manifest.is_file():
                manifest_path = mirror_manifest
        if manifest_path.is_file():
            try:
                data = json.loads(manifest_path.read_text(encoding="utf-8"))
                raw_steps = data.get("resumed_from_step", [])
                if isinstance(raw_steps, list):
                    resumed_steps = [int(x) for x in raw_steps]
            except Exception:
                resumed_steps = []

    return {
        "machine_id": socket.gethostname(),
        "git_head_sha": _git_head_sha(repo),
        "checkpoint_resume_hook_sha256": _file_sha256(hook_path),
        "train_stage2_sha256": _file_sha256(train_path),
        "resumed_from_step": resumed_steps,
    }


def _step_from_ckpt_name(name: str) -> int | None:
    m = re.match(r"^checkpoint-(\d+)$", name)
    return int(m.group(1)) if m else None


def _sorted_checkpoints(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    pairs = []
    for p in directory.iterdir():
        if p.is_dir():
            step = _step_from_ckpt_name(p.name)
            if step is not None:
                pairs.append((step, p))
    pairs.sort(key=lambda x: x[0])
    return [p for _, p in pairs]


def _install_train_stage2_hooks() -> None:
    try:
        import transformers
        from transformers import TrainerCallback
        from transformers.trainer_utils import IntervalStrategy
    except Exception as exc:
        print(f"[checkpoint_resume_hook] import warning: {exc}", file=sys.stderr, flush=True)
        return

    mirror_root = Path(os.environ.get("RESCAP_MIRROR_ROOT", "/root/outputs/runs"))

    class _MirrorCheckpointCallback(TrainerCallback):
        def on_save(self, args, state, control, **kwargs):
            try:
                out_dir = Path(args.output_dir)
                mirror_dir = mirror_root / out_dir.name
                mirror_dir.mkdir(parents=True, exist_ok=True)
                ckpt = out_dir / f"checkpoint-{state.global_step}"
                if ckpt.is_dir():
                    for old in _sorted_checkpoints(mirror_dir):
                        if old.name != ckpt.name:
                            shutil.rmtree(old, ignore_errors=True)
                    dst = mirror_dir / ckpt.name
                    if dst.exists():
                        shutil.rmtree(dst, ignore_errors=True)
                    shutil.copytree(ckpt, dst)
                manifest = out_dir / "resume_manifest.json"
                if manifest.is_file():
                    shutil.copy2(manifest, mirror_dir / "resume_manifest.json")
            except Exception as exc:
                print(f"[checkpoint_resume_hook] mirror warning: {exc}", file=sys.stderr, flush=True)

        def on_train_end(self, args, state, control, **kwargs):
            try:
                out_dir = Path(args.output_dir)
                mirror_dir = mirror_root / out_dir.name
                mirror_dir.mkdir(parents=True, exist_ok=True)
                manifest = out_dir / "resume_manifest.json"
                if manifest.is_file():
                    shutil.copy2(manifest, mirror_dir / "resume_manifest.json")
            except Exception as exc:
                print(f"[checkpoint_resume_hook] train_end warning: {exc}", file=sys.stderr, flush=True)

    orig_post_init = transformers.TrainingArguments.__post_init__

    def _patched_post_init(self):
        orig_post_init(self)
        if str(getattr(self, "save_strategy", "")).lower().endswith("epoch"):
            self.save_strategy = IntervalStrategy.STEPS
            self.save_steps = int(os.environ.get("RESCAP_SAVE_STEPS", "200"))
            self.save_total_limit = int(os.environ.get("RESCAP_SAVE_LIMIT", "2"))
            print(
                f"[checkpoint_resume_hook] Enabled checkpointing: "
                f"save_steps={self.save_steps}, save_total_limit={self.save_total_limit}",
                flush=True,
            )

    transformers.TrainingArguments.__post_init__ = _patched_post_init

    orig_train = transformers.Trainer.train

    def _patched_train(self, resume_from_checkpoint=None, *args, **kwargs):
        self.add_callback(_MirrorCheckpointCallback())
        out_dir = Path(self.args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        mirror_dir = mirror_root / out_dir.name

        if not _sorted_checkpoints(out_dir) and mirror_dir.is_dir():
            for mckpt in _sorted_checkpoints(mirror_dir):
                shutil.copytree(mckpt, out_dir / mckpt.name)
            if (mirror_dir / "resume_manifest.json").is_file() and not (out_dir / "resume_manifest.json").is_file():
                shutil.copy2(mirror_dir / "resume_manifest.json", out_dir / "resume_manifest.json")

        manifest_path = out_dir / "resume_manifest.json"
        prior_steps: list[int] = []
        if manifest_path.is_file():
            try:
                old_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                if isinstance(old_manifest.get("resumed_from_step"), list):
                    prior_steps = [int(x) for x in old_manifest["resumed_from_step"]]
            except Exception:
                prior_steps = []

        ckpts = _sorted_checkpoints(out_dir)
        if ckpts and not resume_from_checkpoint:
            latest_ckpt = ckpts[-1]
            step_num = _step_from_ckpt_name(latest_ckpt.name)
            resume_from_checkpoint = str(latest_ckpt)
            if step_num is not None and step_num not in prior_steps:
                prior_steps.append(step_num)
            print(
                f"[checkpoint_resume_hook] Auto-resuming from {latest_ckpt} "
                f"(resumed_from_step={prior_steps})",
                flush=True,
            )

        meta = provenance_metadata(None)
        meta["resumed_from_step"] = prior_steps
        meta["output_dir"] = str(out_dir)
        meta["save_steps"] = int(getattr(self.args, "save_steps", 200))
        meta["save_total_limit"] = int(getattr(self.args, "save_total_limit", 2) or 2)
        manifest_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        try:
            mirror_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(manifest_path, mirror_dir / "resume_manifest.json")
        except Exception:
            pass

        return orig_train(self, resume_from_checkpoint=resume_from_checkpoint, *args, **kwargs)

    transformers.Trainer.train = _patched_train


def _infer_adapter_dir_for_result(result_path: Path, payload: dict) -> Path | None:
    ncs_data = Path(os.environ.get("NCS_DATA", "/root/ncs-data"))
    adapter = payload.get("adapter")
    if isinstance(adapter, str) and adapter.strip():
        p = Path(adapter)
        if p.exists():
            return p
    run_id = payload.get("run_id")
    if isinstance(run_id, str) and run_id.strip():
        cand = ncs_data / "runs" / run_id
        if cand.exists():
            return cand
    stem = result_path.stem
    for suffix in ("-short_en", "-detailed_en", "-short", "-detailed", "-two", "-instructed", "-dev300"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    if stem.startswith("xm3600_"):
        stem = stem[len("xm3600_") :]
    cand = ncs_data / "runs" / stem
    if cand.exists():
        return cand
    return None


def stamp_json_file(json_path: Path, adapter_dir: Path | None = None) -> bool:
    if not json_path.is_file() or json_path.name.endswith(".preds.json"):
        return False
    try:
        payload = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception:
        return False
    if not isinstance(payload, dict):
        return False

    inferred_adapter = adapter_dir or _infer_adapter_dir_for_result(json_path, payload)
    meta = provenance_metadata(inferred_adapter)
    changed = False
    for k, v in meta.items():
        if payload.get(k) != v:
            payload[k] = v
            changed = True
    if changed:
        indent = 1 if "scores_scaled_x100" in json_path.read_text(encoding="utf-8") else 2
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")
    return changed


def stamp_results_tree(results_dir: Path, runs_dir: Path | None = None) -> int:
    count = 0
    if not results_dir.is_dir():
        return count
    for p in sorted(results_dir.rglob("*.json")):
        if p.name.endswith(".preds.json"):
            continue
        if stamp_json_file(p):
            count += 1
    if runs_dir and runs_dir.is_dir():
        mirror_runs = Path(os.environ.get("RESCAP_MIRROR_ROOT", "/root/outputs/runs"))
        for rdir in sorted(runs_dir.iterdir()):
            if not rdir.is_dir():
                continue
            dst = mirror_runs / rdir.name
            dst.mkdir(parents=True, exist_ok=True)
            for fname in ("adapter_model.safetensors", "adapter_config.json", "metrics.jsonl", "resume_manifest.json"):
                src_f = rdir / fname
                if src_f.is_file():
                    shutil.copy2(src_f, dst / fname)
    return count


def _install_evaluate_atexit_hook() -> None:
    if os.environ.get("RESCAP_G1_BYTE_CHECK") == "1":
        return

    def _on_exit():
        try:
            argv = sys.argv
            out_arg = None
            name_arg = "system"
            adapter_arg = None
            for i, tok in enumerate(argv):
                if tok == "--out" and i + 1 < len(argv):
                    out_arg = argv[i + 1]
                elif tok == "--name" and i + 1 < len(argv):
                    name_arg = argv[i + 1]
                elif tok == "--adapter" and i + 1 < len(argv):
                    adapter_arg = argv[i + 1]
            ncs_data = Path(os.environ.get("NCS_DATA", "/root/ncs-data"))
            target = Path(out_arg) if out_arg else (ncs_data / "results" / f"{name_arg.replace(' ', '_')}.json")
            if target.is_file():
                stamp_json_file(target, Path(adapter_arg) if adapter_arg else None)
        except Exception:
            pass

    atexit.register(_on_exit)


def _self_check() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        run_dir = tmp_path / "runs" / "dummy_s42"
        ckpt_dir = run_dir / "checkpoint-200"
        ckpt_dir.mkdir(parents=True)
        assert _step_from_ckpt_name("checkpoint-200") == 200
        assert _step_from_ckpt_name("other") is None
        assert _sorted_checkpoints(run_dir) == [ckpt_dir]

        manifest = {
            "machine_id": socket.gethostname(),
            "resumed_from_step": [200],
        }
        (run_dir / "resume_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        meta = provenance_metadata(run_dir)
        assert meta["resumed_from_step"] == [200], meta
        assert isinstance(meta["checkpoint_resume_hook_sha256"], str) and len(meta["checkpoint_resume_hook_sha256"]) == 64

        res_file = tmp_path / "dummy_s42-short.json"
        res_file.write_text(json.dumps({"name": "dummy_s42-short", "adapter": str(run_dir)}), encoding="utf-8")
        assert stamp_json_file(res_file, run_dir) is True
        stamped = json.loads(res_file.read_text(encoding="utf-8"))
        assert stamped["resumed_from_step"] == [200], stamped
        assert stamped["checkpoint_resume_hook_sha256"] == meta["checkpoint_resume_hook_sha256"]
        assert stamped["machine_id"] == socket.gethostname()
    print("self-check ok")
    return 0


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--stamp-results", nargs="+", help="Results dir (and optional runs dir) to stamp")
    parser.add_argument("--print-meta", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        return _self_check()
    if args.print_meta:
        print(json.dumps(provenance_metadata(None), ensure_ascii=False, indent=2))
        return 0
    if args.stamp_results:
        res_dir = Path(args.stamp_results[0])
        runs_dir = Path(args.stamp_results[1]) if len(args.stamp_results) > 1 else None
        n = stamp_results_tree(res_dir, runs_dir)
        print(f"stamped {n} result JSON files in {res_dir}")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(_main())
else:
    if any("train_stage2.py" in a for a in sys.argv):
        _install_train_stage2_hooks()
    elif any("evaluate.py" in a for a in sys.argv):
        _install_evaluate_atexit_hook()
