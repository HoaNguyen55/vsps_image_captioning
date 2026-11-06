#!/bin/bash
# Paper C tier-1 GPU-host setup (plan S10/S12; DRAFT, not judge-read). Idempotent: every step checks its own result
# and is skipped when already done. Run by the coordinator on the rented host after the code read, from the repo copy:
#     bash scripts/c_pvr_gpu/setup_host.sh                 (no HF token: no pinned model is gated)
#     printf '%s\n' "$TOKEN" | C_PVR_GATED=1 bash scripts/c_pvr_gpu/setup_host.sh     (only if a gated pin appears)
# The token is read from stdin into the environment of the download process only: never argv, never a file, never
# logged. The log holds step names, package pins, repo ids, revisions and sha256 values only; no host, IP or port.
# Downloads: only the pins of PINS-A v1.4 (mBLIP @ MBLIP["revision"], safetensors only, W10) and the S9 v2 helper
# files (c3abb246, cbb24e6: M-CLIP, XLM-R config/tokenizer only, XGLM-2.9B), each file by name at its pinned revision,
# then checked by LFS sha256 / git-blob SHA-1 (S9 §8.1). LLaVA stays PENDING (Q-LLAVA). Never rents or deletes a machine.
set -euo pipefail
cd "$(dirname "$0")/../.."
LOCK=scripts/c_pvr_gpu/requirements_c_pvr_gpu.lock; LK=$(sha256sum $LOCK | cut -c1-8)   # a lock edit = a new venv
V=$HOME/venvs/c_pvr_gpu_$LK; PY=$V/bin/python; X=scripts/c_pvr_gpu/c_pvr_gpu.py
O=$HOME/c_pvr_out; L=$O/logs/setup.log; GL=$O/gpu_lock_$LK
export HF_HOME=$HOME/c_pvr_models/hf HF_HUB_DISABLE_TELEMETRY=1
mkdir -p "$O/logs" "$GL" "$HF_HOME"
say() { echo "$(date -u +%FT%TZ) $*" >> "$L"; echo "$*"; }
stop() { say "SETUP STOP $*"; exit 1; }

# ---------------------------------------------------------------- host facts (names only)
GPU=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader)
[ "$(echo "$GPU" | wc -l)" = 1 ] || stop "not exactly one GPU"
echo "$GPU" | grep -Eq 'RTX 3090( Ti)?, 24' || stop "GPU is not one RTX 3090 / 3090 Ti 24 GB"
say "gpu ok: $GPU"

# ---------------------------------------------------------------- venv and the GPU lock
[ -x "$PY" ] || { python3.12 -m venv "$V"; say "venv created"; }
if [ ! -s "$GL/freeze.sha256" ]; then
  "$PY" -m pip install -q --no-input --report "$GL/pip_report.json" -r $LOCK \
    2>> "$L" || stop "pip install from the lock"
  "$PY" -I - "$GL/pip_report.json" > "$GL/requirements_c_pvr_gpu.host.lock" <<'EOF'
import json, sys
for it in json.load(open(sys.argv[1]))["install"]:
    m, h = it["metadata"], it["download_info"].get("archive_info", {}).get("hashes", {})
    print(f'{m["name"]}=={m["version"]} --hash=sha256:{h.get("sha256", "MISSING")}')
EOF
  "$PY" -m pip freeze | sha256sum | cut -c1-64 > "$GL/freeze.sha256"
  say "gpu lock written: host.lock $(sha256sum "$GL/requirements_c_pvr_gpu.host.lock" | cut -c1-64) freeze $(cat "$GL/freeze.sha256")"
fi
NOW=$("$PY" -m pip freeze | sha256sum | cut -c1-64)
[ "$NOW" = "$(cat "$GL/freeze.sha256")" ] || stop "venv freeze $NOW differs from the recorded first build"
say "venv ok: lock $LK freeze $NOW (c_pvr_job.sh FREEZE_SHA is set from this by a diff read)"
"$PY" -I -c "import torch; assert torch.cuda.is_available(); print('torch', torch.__version__, 'cuda', torch.version.cuda)" \
  | tee -a "$L" || stop "torch cannot see the GPU"

# ---------------------------------------------------------------- pinned models (revision + sha), no gated pin today
if [ "${C_PVR_GATED:-0}" = 1 ]; then IFS= read -r -s HF_TOKEN; export HF_TOKEN; fi
"$PY" -I -B - <<'EOF' >> "$L" 2>&1 || stop "mBLIP download or sha check"
import os, sys
sys.path.insert(0, "scripts/c_pvr_gpu")
import c_pvr_gpu as G
G.load()
from huggingface_hub import snapshot_download
m = G.CP.MBLIP
snap = snapshot_download(m["repo"], revision=m["revision"], allow_patterns=["*.json", "*.safetensors", "*.txt"])
open(os.path.expanduser("~/c_pvr_out/mblip_snapshot.path"), "w").write(snap + "\n")
bad = [f for f, h in m["files"].items() if G.CP.sha_file(G.Path(snap) / f) != h]
assert not bad, bad
assert not any(f.endswith(".bin") for f in os.listdir(snap)), "pickle weights present (W10)"
print("mblip ok", m["repo"], m["revision"], " ".join(h[:8] for h in m["files"].values()))
EOF
"$PY" -I -B - <<'EOF' >> "$L" 2>&1 || stop "S9 helper download or pin check"
import sys
sys.path.insert(0, "scripts/c_pvr_gpu")
import c_pvr_gpu as G
G.load()
from huggingface_hub import snapshot_download
for name, (repo, rev, files) in G.CP.HELPERS.items():
    snap = snapshot_download(repo, revision=rev, allow_patterns=sorted(files))
    G.helper_check(G.Path(snap), name)
    open(G.Path.home() / "c_pvr_out" / f"{name}_snapshot.path", "w").write(snap + "\n")
    print("helper ok", name, repo, rev, " ".join(v[:8] for _, v in files.values()))
EOF
unset HF_TOKEN
say "model pins EN: PENDING (Q-LLAVA); not downloaded"

# ---------------------------------------------------------------- tmpfs for images and datastore material (host v3 §4.2)
HC=/dev/shm/c_pvr_hc
[ -d $HC ] || mkdir -m 700 $HC
[ "$(stat -c %a $HC)" = 700 ] || stop "$HC is not mode 0700"
say "SETUP OK"
