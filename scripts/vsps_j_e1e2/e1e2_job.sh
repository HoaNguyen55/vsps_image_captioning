#!/usr/bin/env bash
# VSPS-J E1+E2 GPU sub-jobs (PREREG.md section 7 as amended by AMENDMENT_1: one host block per sub-job, one OUT each).
#   PY=<venv python> bash scripts/vsps_j_e1e2/e1e2_job.sh --selftest        pins + CPU selftest only
#   E1b, rented RTX 4090 (KTVIC train only; never fetches or stages any UIT-ViIC file, never fetches Qwen):
#     PY=... KT_IMAGES=<KTVIC images of the 3,700 records> OUT=<the E1b OUT folder> bash e1e2_job.sh e1b
#   E1a, M1 only (holds the 231 UIT-ViIC test images; own HF cache, own folders):
#     PY=... HF_HOME=<E1a's own HF cache> KT_SMOKE=<the 20 KTVIC-train smoke images> UIT_IMAGES=<empty dir> \
#       STAGE=<empty dir> OUT=<the E1a OUT folder> bash e1e2_job.sh e1a
# Exit codes are e1e2.py's: 0 DONE, 2 FAULT, 3 PROJECTION_STOP, 4 CAP_STOP, 5 FAILURES (E1a, no marker).
set -euo pipefail
cd "$(dirname "$0")/../.."
VREV=b98f263eab246eb5269ade64edbdca8a887dc44d
QREV=cc594898137f460bfe9f0759e9844b3ce807cfb5
PDIR=manuscript/prereg/2026-10-31_vsps_j_e1e2
SUB=${1:?usage: e1e2_job.sh --selftest | e1b | e1a}
case "$SUB" in --selftest|e1b|e1a) ;; *) echo "unknown sub-job $SUB"; exit 2 ;; esac
: "${PY:?set PY to the venv python}"
(cd scripts/vsps_j_e1e2 && sha256sum -c --quiet SHA256SUMS)
(cd scripts/vsps_j_m0 && sha256sum -c --quiet SHA256SUMS)
(cd scripts/vsps_h1 && sha256sum -c --quiet SHA256SUMS)
(cd "$PDIR" && sha256sum -c --quiet SHA256SUMS)
"$PY" -I - "$SUB" <<'EOF_PIN'
import sys
from importlib.metadata import version
import einops, numpy, PIL, timm, torch, torchvision, transformers
want = {transformers: "4.51.3", torch: "2.15.0", torchvision: "0.29.2", numpy: "2.5.4", PIL: "13.0.0",
        timm: "1.0.30", einops: "0.8.2"}  # M0 env; +cuXXX / +cpu build suffixes allowed on torch and torchvision
bad = {m.__name__: m.__version__ for m, v in want.items() if m.__version__.split("+")[0] != v}
if sys.argv[1] == "e1a":  # Qwen2.5-VL generator; the pins used with transformers 4.51.3 on M2 (2026-10-18)
    bad.update({p: version(p) for p, v in {"accelerate": "1.15.0", "qwen-vl-utils": "0.0.14"}.items() if version(p) != v})
assert not bad, f"environment differs from PREREG section 7 / AMENDMENT_1: {bad}"
EOF_PIN
"$PY" -I scripts/vsps_j_e1e2/e1e2.py selftest
[ "$SUB" = "--selftest" ] && exit 0
: "${OUT:?}"
[ -z "${QWEN_MAX_PIXELS:-}" ] || { echo "QWEN_MAX_PIXELS must be unset"; exit 2; }
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
"$PY" -m pip freeze > "$OUT/pip_freeze_$SUB.txt"
HUB=${HF_HOME:-$HOME/.cache/huggingface}/hub
fetch() {  # repo revision
    local dir="$HUB/models--${1/\//--}"
    [ -d "$dir/snapshots/$2" ] || HF_HUB_DISABLE_TELEMETRY=1 "$PY" -I -c \
        "from huggingface_hub import snapshot_download as s; s('$1', revision='$2')"
    mkdir -p "$dir/refs" && printf %s "$2" > "$dir/refs/main"   # remote code and offline loads resolve refs/main
}
VSNAP="$HUB/models--5CD-AI--Vintern-1B-v3_5/snapshots/$VREV"
rc=0
if [ "$SUB" = e1b ]; then
    : "${KT_IMAGES:?}"
    fetch 5CD-AI/Vintern-1B-v3_5 "$VREV"
    HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 "$PY" -I scripts/vsps_j_e1e2/e1e2.py e1b --images "$KT_IMAGES" \
        --model "$VSNAP" --out "$OUT" || rc=$?
else
    : "${HF_HOME:?E1a uses its own HF cache (never the host default: refs/main is rewritten)}" "${KT_SMOKE:?}" \
      "${UIT_IMAGES:?}" "${STAGE:?}"
    mkdir -p "$UIT_IMAGES" "$STAGE/datasets/ktvic"
    fetch 5CD-AI/Vintern-1B-v3_5 "$VREV"
    fetch Qwen/Qwen2.5-VL-7B-Instruct "$QREV"
    "$PY" -I scripts/vsps_j_e1e2/e1e2.py fetchlist > "$OUT/fetch_e1a.txt"   # from the pinned test_data.json
    while read -r n u; do
        [ -s "$UIT_IMAGES/$n" ] || curl -sfL --retry 3 -o "$UIT_IMAGES/$n" "$u"
    done < "$OUT/fetch_e1a.txt"
    (cd "$UIT_IMAGES" && cut -d' ' -f1 "$OUT/fetch_e1a.txt" | xargs sha256sum) > "$OUT/uit_images.sha256"
    [ "$(wc -l < "$OUT/uit_images.sha256")" = 231 ]
    cp data/datasets/uitviic/test_data.json "$STAGE/datasets/ktvic/uitviic_test.json"
    ln -sfn "$(cd "$UIT_IMAGES" && pwd)" "$STAGE/datasets/ktvic/images"
    NCS_DATA="$STAGE" HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 "$PY" -I scripts/vsps_j_e1e2/e1e2.py e1a \
        --model "$VSNAP" --qwen "$HUB/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/$QREV" \
        --smoke-images "$KT_SMOKE" --out "$OUT" || rc=$?
fi
[ -f "$OUT/$SUB/probes.jsonl" ] && (cd "$OUT/$SUB" && sha256sum probes.jsonl > probes.jsonl.sha256)
echo "$SUB exit $rc"
exit "$rc"
