#!/usr/bin/env python3
"""Enforce and execute Gate G-1 PASS in code before any GPU queue job runs.

Tightened per Claude 2026-10-15 00:42 UTC (#2 & #3):
- Only accepts a `g1_gate_<host>*.json` file with `verdict == "PASS"` if:
  1. `git_head_sha` matches the machine's current `git -C /root/vsps rev-parse HEAD`
  2. `checkpoint_resume_hook_sha256` matches the current SHA-256 of `scripts/checkpoint_resume_hook.py`
  3. `sitecustomize_symlink_target` matches the active venv's `sitecustomize.py` symlink target
  4. `segmenter == "rdrsegmenter"`
  5. `chair_v1_raw_tone.byte_exact_json_match_vs_committed is True`
  6. `chair_v1_raw_tone.exact_match_vs_committed is True`
  7. `max_metric_abs_diff == 0`
  8. `n_adapters_verified >= 23`
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


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _current_machine_state(repo: Path) -> dict[str, str | None]:
    head_sha = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()
    hook_path = repo / "scripts/checkpoint_resume_hook.py"
    hook_sha = _sha256(hook_path)
    site_venv = repo / ".venv/lib/python3.10/site-packages/sitecustomize.py"
    site_target = os.readlink(site_venv) if site_venv.is_symlink() else None
    return {
        "head_sha": head_sha,
        "hook_sha": hook_sha,
        "site_venv": str(site_venv),
        "site_target": site_target,
    }


def verify_g1_gate(
    repo: Path = DEFAULT_REPO,
    out_dir: Path = DEFAULT_OUT,
    host: str | None = None,
) -> tuple[bool, dict[str, object]]:
    host = host or socket.gethostname()
    state = _current_machine_state(repo)
    expected_target = str(repo / "scripts/checkpoint_resume_hook.py")
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
        ok = (
            d.get("verdict") == "PASS"
            and d.get("machine_id") == host
            and d.get("segmenter") == "rdrsegmenter"
            and d.get("git_head_sha") == state["head_sha"]
            and d.get("checkpoint_resume_hook_sha256") == state["hook_sha"]
            and d.get("sitecustomize_symlink_target") == state["site_target"]
            and state["site_target"] == expected_target
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
                    "n_adapters_verified": d.get("n_adapters_verified"),
                    "sha256": _sha256(p),
                }
            )
    if not matched:
        return False, {
            "host": host,
            "current_head_sha": state["head_sha"],
            "current_hook_sha256": state["hook_sha"],
            "current_sitecustomize_target": state["site_target"],
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

    adapters = sorted(
        p
        for p in list(ncs.glob("runs/**/adapter_model.safetensors"))
        + list(ncs.glob("rl/**/adapter_model.safetensors"))
        if "multiref_s42" not in str(p)
    )
    adapter_hashes = {str(p.relative_to(ncs).parent): _sha256(p) for p in adapters}

    expected_target = str(repo / "scripts/checkpoint_resume_hook.py")
    gate_ok = (
        max_metric_diff == 0
        and chair_v1_exact
        and byte_exact_v1
        and got_v1["results"][0]["segmenter"] == "rdrsegmenter"
        and state["site_target"] == expected_target
        and len(adapter_hashes) >= MIN_ADAPTERS
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
        "sitecustomize_symlink": state["site_venv"],
        "sitecustomize_symlink_target": state["site_target"],
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
        "adapter_sha256": adapter_hashes,
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
    print(json.dumps({"status": "ok", "file": str(Path(__file__).name), "sha256": _sha256(Path(__file__))}))
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
        f"sha256={info['sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
