#!/usr/bin/env bash
# O31 self-tests + mutants. Synthetic fixtures only. PY = a python with numpy (laptop: ~/.venvs/c_stage1_lists;
# host: the O31 venv). VSPS_REPO = the repo snapshot holding the REUSED files (sha-checked on import).
set -euo pipefail
cd "$(dirname "$0")"
PY="${PY:-$HOME/.venvs/c_stage1_lists/bin/python}"
export VSPS_REPO="${VSPS_REPO:-/mnt/d/vsps_image_captioning}"
sha256sum -c SHA256SUMS --quiet
"$PY" -I -B test_o31.py
"$PY" -I -B mutants.py
