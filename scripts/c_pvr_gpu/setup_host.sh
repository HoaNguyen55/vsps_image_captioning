#!/bin/bash
# Paper C tier-1 GPU-host setup (plan S10/S12; DRAFT, not judge-read). Idempotent: every step checks its own result
# and is skipped when already done. Run by the coordinator on the rented host after the code read, from the repo copy:
#     bash scripts/c_pvr_gpu/setup_host.sh [STAGE]          (no HF token: no pinned model is gated)
#     printf '%s\n' "$TOKEN" | C_PVR_GATED=1 bash scripts/c_pvr_gpu/setup_host.sh     (only if a gated pin appears)
# STAGE (CC-280 AD2, the E-G order): main = GPU check + main venv + tmpfs; siglip = the SigLIP2 snapshot at e8e48729
# (c_pvr_embed.py fetch, E-G only); rest = EN venv + mBLIP + S9 helpers + Q-LLAVA files. Default all = main + rest
# (HC-n: no SigLIP2). E-G runs main, siglip (image push in parallel), the embed, then rest.
# Main venv (CC-280 AM1): the m9 hashed closure requirements_c_pvr_gpu.host.lock (966eb327, pulled from m9's
# gpu_lock_d584787b) installed with --require-hashes --no-deps plus the cu124 index, as the EN venv; its freeze must
# equal m9's 9a074530, else STOP (the R-P6 reader rules). The venv name follows the installed file (LK = 966eb327).
# The token is read from stdin into the environment of the download process only: never argv, never a file, never
# logged. The log holds step names, package pins, repo ids, revisions and sha256 values only; no host, IP or port.
# Downloads: only the pins of PINS-A v1.4 (mBLIP @ MBLIP["revision"], safetensors only, W10) and the S9 v2 helper
# files (c3abb246, cbb24e6: M-CLIP, XLM-R config/tokenizer only, XGLM-2.9B) and the Q-LLAVA files (c_pvr.py EN_MODELS:
# llava-v1.5-7b, its CLIP tower, the LLaVA code files from GitHub raw at c121f043), each file by name at its pinned
# revision, then checked by LFS sha256 / git-blob SHA-1 (S9 §8.1). Repos loaded BY NAME offline (BY_NAME: XLM-R, the
# CLIP tower) get refs/main = the pin, checked (CC-272 N1). Two venvs: the main lock, and the LLaVA lock (EN arms only).
# Never rents or deletes a machine.
set -euo pipefail
STAGE=${1:-all}
case "$STAGE" in main|siglip|rest|all) ;; *) echo "usage: setup_host.sh [main|siglip|rest|all]"; exit 2;; esac
cd "$(dirname "$0")/../.."
LOCK=scripts/c_pvr_gpu/requirements_c_pvr_gpu.host.lock; LK=$(sha256sum $LOCK | cut -c1-8)   # a lock edit = a new venv
M9_FREEZE=9a0745307b3b8d7c4e4c195bc78e2e1a9a52eb5046fd6f438c6402802fe9c09f   # OPS-1106c-m9-setup-ok (LOG l.1669)
V=$HOME/venvs/c_pvr_gpu_$LK; PY=$V/bin/python; X=scripts/c_pvr_gpu/c_pvr_gpu.py
LOCKE=scripts/c_pvr_gpu/requirements_c_pvr_llava.lock; LKE=$(sha256sum $LOCKE | cut -c1-8)
VE=$HOME/venvs/c_pvr_llava_$LKE; PYE=$VE/bin/python
O=$HOME/c_pvr_out; L=$O/logs/setup.log; GL=$O/gpu_lock_$LK; GLE=$O/gpu_lock_llava_$LKE
export HF_HOME=$HOME/c_pvr_models/hf HF_HUB_DISABLE_TELEMETRY=1
mkdir -p "$O/logs" "$GL" "$GLE" "$HF_HOME"
say() { echo "$(date -u +%FT%TZ) $*" >> "$L"; echo "$*"; }
stop() { say "SETUP STOP $*"; exit 1; }

# ---------------------------------------------------------------- host facts (names only)
if [ "$STAGE" = main ] || [ "$STAGE" = all ]; then
GPU=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader)
[ "$(echo "$GPU" | wc -l)" = 1 ] || stop "not exactly one GPU"
echo "$GPU" | grep -Eq 'RTX 3090( Ti)?, 24' || stop "GPU is not one RTX 3090 / 3090 Ti 24 GB"
say "gpu ok: $GPU"

# ---------------------------------------------------------------- venv and the GPU lock
[ -x "$PY" ] || { python3.12 -m venv "$V"; say "venv created"; }
if [ ! -s "$GL/freeze.sha256" ]; then
  "$PY" -m pip install -q --no-input --require-hashes --no-deps --extra-index-url https://download.pytorch.org/whl/cu124 \
    --report "$GL/pip_report.json" -r $LOCK 2>> "$L" || stop "pip install from the hashed closure"
  "$PY" -I - "$GL/pip_report.json" > "$GL/requirements_c_pvr_gpu.host.lock" <<'EOF'
import json, sys
for it in json.load(open(sys.argv[1]))["install"]:
    m, h = it["metadata"], it["download_info"].get("archive_info", {}).get("hashes", {})
    print(f'{m["name"]}=={m["version"]} --hash=sha256:{h.get("sha256", "MISSING")}')
EOF
  "$PY" -m pip freeze | sha256sum | cut -c1-64 > "$GL/freeze.sha256"
  say "gpu lock written: host.lock $(sha256sum "$GL/requirements_c_pvr_gpu.host.lock" | cut -c1-64) freeze $(cat "$GL/freeze.sha256")"
fi
[ "$(LC_ALL=C sort $LOCK)" = "$(LC_ALL=C sort "$GL/requirements_c_pvr_gpu.host.lock")" ] || stop "installed closure differs from $LOCK"
NOW=$("$PY" -m pip freeze | sha256sum | cut -c1-64)
[ "$NOW" = "$(cat "$GL/freeze.sha256")" ] || stop "venv freeze $NOW differs from the recorded first build"
[ "$NOW" = "$M9_FREEZE" ] || stop "venv freeze $NOW differs from m9's ${M9_FREEZE:0:8} (CC-280 AM1): STOP, the R-P6 reader rules"
say "venv ok: lock $LK freeze $NOW (c_pvr_job.sh FREEZE_SHA is set from this by a diff read)"
"$PY" -I -c "import torch; assert torch.cuda.is_available(); print('torch', torch.__version__, 'cuda', torch.version.cuda)" \
  | tee -a "$L" || stop "torch cannot see the GPU"
HC=/dev/shm/c_pvr_hc   # host v3 §4.2: images and datastore material in tmpfs only
[ -d $HC ] || mkdir -m 700 $HC
[ "$(stat -c %a $HC)" = 700 ] || stop "$HC is not mode 0700"
say "SETUP main OK"
fi

# ---------------------------------------------------------------- SigLIP2 (E-G embed only; CC-280 AM5 / AD2 step 2)
if [ "$STAGE" = siglip ]; then
  [ -x "$PY" ] || stop "run stage main first"
  "$PY" -I -B scripts/c_pvr_gpu/c_pvr_embed.py fetch --out "$O" >> "$L" 2>&1 || stop "SigLIP2 download or sha check"
  say "SETUP siglip OK $(cat "$O/siglip2_snapshot.path")"
  exit 0
fi
[ "$STAGE" = main ] && exit 0

# ---------------------------------------------------------------- the EN venv (Q-LLAVA): full hashed closure, no resolver
[ -x "$PYE" ] || { python3.12 -m venv "$VE"; say "EN venv created"; }
if [ ! -s "$GLE/freeze.sha256" ]; then
  "$PYE" -m pip install -q --no-input --require-hashes --no-deps -r $LOCKE 2>> "$L" || stop "pip install from the LLaVA lock"
  "$PYE" -m pip freeze | sha256sum | cut -c1-64 > "$GLE/freeze.sha256"
  say "EN lock installed: freeze $(cat "$GLE/freeze.sha256")"
fi
NOWE=$("$PYE" -m pip freeze | sha256sum | cut -c1-64)
[ "$NOWE" = "$(cat "$GLE/freeze.sha256")" ] || stop "EN venv freeze $NOWE differs from the recorded first build"
say "EN venv ok: lock $LKE freeze $NOWE (c_pvr_job.sh FREEZE_SHA_EN is set from this by a diff read)"
"$PYE" -I -c "import torch, transformers, accelerate, sentencepiece, google.protobuf
assert torch.__version__ == '2.6.0+cu124' and transformers.__version__ == '4.37.2' and torch.cuda.is_available()
print('EN venv torch', torch.__version__, 'transformers', transformers.__version__)" | tee -a "$L" || stop "EN venv imports"

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
"$PY" -I -B - <<'EOF' >> "$L" 2>&1 || stop "Q-LLAVA download, pin check or refs/main"
import os, sys, urllib.request
sys.path.insert(0, "scripts/c_pvr_gpu")
import c_pvr_gpu as G
G.load()
from huggingface_hub import snapshot_download
for name, (repo, rev, files) in G.CP.EN_MODELS.items():
    if name == "llava_code":  # GitHub raw at the pinned commit, every file re-fetched, then blob-checked below
        snap = G.Path.home() / "c_pvr_models" / f"llava_code_{rev[:8]}"
        for f in files:
            (snap / f).parent.mkdir(parents=True, exist_ok=True)
            req = urllib.request.Request(f"https://raw.githubusercontent.com/{repo}/{rev}/{f}",
                                         headers={"User-Agent": "vsps-research"})
            (snap / f).write_bytes(urllib.request.urlopen(req, timeout=60).read())
    else:
        snap = snapshot_download(repo, revision=rev, allow_patterns=sorted(files))
    G.helper_check(G.Path(snap), name)
    open(G.Path.home() / "c_pvr_out" / f"{name}_snapshot.path", "w").write(f"{snap}\n")
    print("en ok", name, repo, rev, " ".join(v[:8] for _, v in files.values()))
for name in G.BY_NAME:  # CC-272 N1: refs/main = the pin, then every pinned file resolves BY NAME to that snapshot
    G.write_ref(G.Path(os.environ["HF_HOME"]) / "hub", name)
    print("refs/main ok", name, G.spec(name)[1])
EOF
unset HF_TOKEN
say "SETUP OK"
