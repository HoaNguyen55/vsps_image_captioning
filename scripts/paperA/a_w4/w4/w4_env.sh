#!/usr/bin/env bash
# CP-111 W3 (d): environment record for the W4 decode, written before the parity slice.
# Run on the decode machine from the repo root with the venv active: bash scripts/paperA/a_w4/w4/w4_env.sh OUT_DIR
# Writes OUT_DIR/env.txt (creating OUT_DIR). Records no host name, address, port or GPU UUID.
set -euo pipefail
mkdir -p "${1:?usage: w4_env.sh OUT_DIR}"
out="$1/env.txt"
hub="${HF_HUB_CACHE:-${HF_HOME:-$HOME/.cache/huggingface}/hub}/models--Qwen--Qwen2.5-VL-7B-Instruct"
{
  echo "# W4 env record, $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "## repo"
  git rev-parse HEAD
  echo "uncommitted paths: $(git status --porcelain --untracked-files=no | wc -l)"
  sha256sum scripts/coco_probe.py scripts/evaluate.py
  echo "## adapters"
  sha256sum "${NCS_DATA:?NCS_DATA unset}"/runs/{fuse2_s42,p1_s43}/adapter_model.safetensors
  echo "## base model snapshot"
  echo "refs/main: $(cat "$hub/refs/main" 2>/dev/null || echo ABSENT)"
  ls "$hub/snapshots" 2>/dev/null || echo "snapshots: ABSENT"
  echo "## gpu"
  nvidia-smi -L | sed -E 's/\(UUID: [^)]*\)/(UUID redacted)/' || echo "nvidia-smi: ABSENT"
  nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv || true
  echo "## python"
  python --version
  pip freeze
} > "$out"
echo "wrote $out ($(wc -l < "$out") lines)"
