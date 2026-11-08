#!/bin/bash
# B-PA1-T1 HB-T1 host setup (B_RUN_DOC_v1 §6 step 4-5; C's setup_host.sh as template; DRAFT, not read). Idempotent: each
# stage checks its own result. Run by the coordinator on the host from the sparse repo copy, after host prep (§6 step 2):
#     bash scripts/b_pa1/b_pa1_setup_host.sh main|weights|sscd|all          (no token: ungated pins only)
#     ssh ... 'cd ~/b_pa1_repo && bash scripts/b_pa1/b_pa1_setup_host.sh gated' < ~/.cache/huggingface/token
# main    = one 3090 check; venvs main + legacy from the hashed locks (--require-hashes --no-deps, C's AM1 form), each
#           first-build pip-freeze sha written once to ~/b_pa1_out/freeze_<venv>.sha256 for the R2 pin line, later
#           builds compared; the W venv from requirements_b_pa1_w.txt (= cenfeat_venv_freeze.txt 1a639a50; R5 §D.2) and
#           its freeze compared with 1a639a50 (a mismatch is the operator FAULT of R5 §D.2: block W runs on the laptop).
# weights = every registry model with download true and gated false, by revision, only its pinned files, then every
#           file checked (LFS sha256 / git-blob SHA-1) and no unpinned pickle (b_pa1_gpu.Models.snap); refs/main of
#           xlm-roberta-large = its pin (open_clip loads it BY NAME offline; as C's write_ref, CC-272 N1).
# gated   = the same for the gated pins (both Gemma models); the HF token is read from stdin into the environment of the
#           download process only: never argv, never a file, never logged.
# sscd    = the SSCD file pushed from the laptop checked against w25.SSCD_SHA.
# The log holds stage names, versions, repo ids, revisions and short shas only; no host, IP or port. Never rents or
# deletes a machine and never creates /dev/shm/b_pa1_hb (the first push does, run doc §6 step 8).
set -euo pipefail
STAGE=${1:-all}
case "$STAGE" in main|weights|gated|sscd|all) ;; *) echo "usage: b_pa1_setup_host.sh [main|weights|gated|sscd|all]"; exit 2;; esac
cd "$(dirname "$0")/../.."
B=scripts/b_pa1; X=$B/b_pa1_gpu.py
W_FREEZE=1a639a50adf550c50c6dfe284146e279b2a2bf2a716ade743e9eb357ccbf0778
O=$HOME/b_pa1_out; L=$O/logs/setup.log
export HF_HOME=$HOME/b_pa1_models/hf HF_HUB_DISABLE_TELEMETRY=1 B_PA1_OUT=$O PIP_NO_CACHE_DIR=1   # CC-295r2 N-d: no pip wheel cache on disk
mkdir -p "$O/logs" "$O/snaps" "$O/in" "$HF_HOME"
say() { echo "$(date -u +%FT%TZ) $*" >> "$L"; echo "$*"; }
stop() { say "SETUP STOP $*"; exit 1; }
LKM=$(sha256sum $B/requirements_b_pa1_main.lock | cut -c1-8); PYM=$HOME/venvs/b_pa1_main_$LKM/bin/python

venv() {  # name lock -> a venv from the full hashed closure; its first-build freeze is recorded once, later compared
  local name=$1 lock=$2 lk V P F
  lk=$(sha256sum "$lock" | cut -c1-8); V=$HOME/venvs/b_pa1_${name}_$lk; P=$V/bin/python
  [ -x "$P" ] || { python3.12 -m venv "$V"; say "venv $name created"; }
  if [ ! -s "$O/freeze_$name.sha256" ]; then
    "$P" -m pip install -q --no-input --require-hashes --no-deps --extra-index-url https://download.pytorch.org/whl/cu124 \
      -r "$lock" 2>> "$L" || stop "pip install $name from the hashed closure"
    "$P" -m pip freeze | sha256sum | cut -c1-64 > "$O/freeze_$name.sha256"
  fi
  F=$("$P" -m pip freeze | sha256sum | cut -c1-64)
  [ "$F" = "$(cat "$O/freeze_$name.sha256")" ] || stop "$name venv freeze $F differs from its first build"
  "$P" -I -c "import torch, transformers, timm, einops, sentencepiece, PIL
assert torch.cuda.is_available() and torch.__version__ == '2.6.0+cu124'
print('$name lock $lk freeze ${F:0:8} torch', torch.__version__, 'cuda', torch.version.cuda, 'transformers', transformers.__version__)" \
    | tee -a "$L" || stop "$name venv imports or CUDA"
}

if [ "$STAGE" = main ] || [ "$STAGE" = all ]; then
  GPU=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader)
  [ "$(echo "$GPU" | wc -l)" = 1 ] && echo "$GPU" | grep -Eq 'RTX 3090( Ti)?, 24' || stop "not one RTX 3090 / 3090 Ti 24 GB"
  say "gpu ok: $GPU"
  venv main $B/requirements_b_pa1_main.lock
  venv legacy $B/requirements_b_pa1_legacy.lock
  "$PYM" -I -c "import open_clip; print('open_clip', open_clip.__version__)" | tee -a "$L" || stop "open_clip in main"
  VW=$HOME/venvs/b_pa1_w
  [ -x $VW/bin/python ] || { python3.12 -m venv $VW; $VW/bin/python -m pip install -q --no-input --no-deps \
    --extra-index-url https://download.pytorch.org/whl/cpu -r $B/requirements_b_pa1_w.txt 2>> "$L" || say "W venv install failed"; }
  FW=$($VW/bin/python -m pip freeze | sha256sum | cut -c1-64)
  if [ "$FW" = $W_FREEZE ]; then say "W venv ok: freeze 1a639a50"; else say "W venv FAULT: freeze ${FW:0:8} != 1a639a50 (R5 §D.2: block W on the laptop)"; fi
  [ ! -e /dev/shm/b_pa1_hb ] || say "NOTE: /dev/shm/b_pa1_hb exists before the first push"
  say "SETUP main OK"
fi

fetch() {  # gated: false|true -> download and check every pinned file of those models
  "$PYM" -I -B - "$1" <<'EOF' >> "$L" 2>&1
import os, sys
sys.path.insert(0, "scripts/b_pa1")
import b_pa1_gpu as G
from huggingface_hub import snapshot_download
reg, gated = G.load_reg(), sys.argv[1] == "true"
M = G.Models(reg)
import shutil
need = sum(m["bytes"] for k, m in reg["models"].items() if m["download"]  # CC-295r2 N-d: ungated + gated in one check
           and not (G.O() / "snaps" / f"{k}.path").exists())  # models already fetched and checked are not counted
free = shutil.disk_usage(os.environ["HF_HOME"]).free  # CC-295 N11: the pinned bytes x 1.1 must fit before any fetch
if need * 1.1 > free:
    raise SystemExit(f"FAULT: {need / 1e9:.1f} GB to fetch x 1.1 > {free / 1e9:.1f} GB free")
print("disk ok", round(need / 1e9, 1), "GB to fetch,", round(free / 1e9, 1), "GB free")
for k, m in reg["models"].items():
    if not m["download"] or m["gated"] != gated:
        continue
    snap = snapshot_download(m["repo"], revision=m["revision"], allow_patterns=sorted(m["files"]))
    (G.O() / "snaps" / f"{k}.path").write_text(snap + "\n")
    M.snap(k)
    print("ok", k, m["repo"], m["revision"][:8], len(m["files"]), "files")
    if k == "xlmr":  # refs/main = the pin, so open_clip's BY-NAME lookup resolves to this snapshot offline
        ref = G.Path(snap).parent.parent / "refs" / "main"
        ref.parent.mkdir(exist_ok=True)
        ref.write_text(m["revision"])
        print("refs/main ok", k, m["revision"][:8])
EOF
}
if [ "$STAGE" = weights ] || [ "$STAGE" = all ]; then
  fetch false || stop "ungated download or pin check"
  say "SETUP weights OK"
fi
if [ "$STAGE" = gated ]; then
  IFS= read -r HF_TOKEN || [ -n "${HF_TOKEN:-}" ] || stop "no token on stdin"  # the token file has no final newline
  export HF_TOKEN
  fetch true || { unset HF_TOKEN; stop "gated download or pin check"; }
  unset HF_TOKEN
  say "SETUP gated OK"
fi
if [ "$STAGE" = sscd ]; then
  S=$HOME/b_pa1_models/sscd_disc_mixup.torchscript.pt
  WANT=$(sed -n 's/^SSCD_SHA = "\([0-9a-f]\{64\}\)".*/\1/p' scripts/w25/w25.py)
  [ -n "$WANT" ] && [ "$(sha256sum < "$S" | cut -c1-64)" = "$WANT" ] || stop "SSCD file differs from w25.SSCD_SHA"
  say "SETUP sscd OK ${WANT:0:8}"
fi
