#!/usr/bin/env bash
# VSPS-J E1+E2 GPU block (manuscript/prereg/2026-10-31_vsps_j_e1e2/PREREG.md section 7). Run from the staged repo copy.
#   PY=<venv python> bash scripts/vsps_j_e1e2/e1e2_job.sh --selftest         pins + CPU selftest only
#   PY=<venv python> KT_IMAGES=<KTVIC images of the 3,700 records> UIT_IMAGES=<empty dir> STAGE=<empty dir> \
#       OUT=<the ONE OUT folder of this block, outside the repo> bash scripts/vsps_j_e1e2/e1e2_job.sh
# Sub-job exit codes are e1e2.py's: 0 DONE, 2 FAULT, 3 PROJECTION_STOP, 4 CAP_STOP, 5 FAILURES (E1a, no marker).
set -euo pipefail
cd "$(dirname "$0")/../.."
VREV=b98f263eab246eb5269ade64edbdca8a887dc44d
QREV=cc594898137f460bfe9f0759e9844b3ce807cfb5
PDIR=manuscript/prereg/2026-10-31_vsps_j_e1e2
: "${PY:?set PY to the venv python}"
(cd scripts/vsps_j_e1e2 && sha256sum -c --quiet SHA256SUMS)
(cd scripts/vsps_j_m0 && sha256sum -c --quiet SHA256SUMS)
(cd scripts/vsps_h1 && sha256sum -c --quiet SHA256SUMS)
(cd "$PDIR" && sha256sum -c --quiet SHA256SUMS)
"$PY" -I - <<'EOF_PIN'
import einops, numpy, PIL, timm, torch, torchvision, transformers
import accelerate, qwen_vl_utils  # noqa: F401  Qwen2.5-VL generator (device_map, vision input); versions in pip_freeze
want = {transformers: "4.51.3", torch: "2.15.0", torchvision: "0.29.2", numpy: "2.5.4", PIL: "13.0.0",
        timm: "1.0.30", einops: "0.8.2"}  # M0 env; +cuXXX / +cpu build suffixes allowed on torch and torchvision
bad = {m.__name__: m.__version__ for m, v in want.items() if m.__version__.split("+")[0] != v}
assert not bad, f"environment differs from PREREG section 7: {bad}"
EOF_PIN
"$PY" -I scripts/vsps_j_e1e2/e1e2.py selftest
[ "${1:-}" = "--selftest" ] && exit 0
: "${KT_IMAGES:?}" "${UIT_IMAGES:?}" "${STAGE:?}" "${OUT:?}"
[ -z "${QWEN_MAX_PIXELS:-}" ] || { echo "QWEN_MAX_PIXELS must be unset"; exit 2; }
mkdir -p "$OUT" "$UIT_IMAGES" "$STAGE/datasets/ktvic"
OUT=$(cd "$OUT" && pwd)
"$PY" -m pip freeze > "$OUT/pip_freeze.txt"
HUB=${HF_HOME:-$HOME/.cache/huggingface}/hub
for spec in "5CD-AI/Vintern-1B-v3_5 $VREV" "Qwen/Qwen2.5-VL-7B-Instruct $QREV"; do
    set -- $spec
    dir="$HUB/models--${1/\//--}"
    [ -d "$dir/snapshots/$2" ] || HF_HUB_DISABLE_TELEMETRY=1 "$PY" -I -c \
        "from huggingface_hub import snapshot_download as s; s('$1', revision='$2')"
    mkdir -p "$dir/refs" && printf %s "$2" > "$dir/refs/main"   # remote code and offline loads resolve refs/main
done
"$PY" -I scripts/vsps_j_e1e2/e1e2.py fetchlist > "$OUT/fetch_e1a.txt"   # from the pinned test_data.json
while read -r n u; do
    [ -s "$UIT_IMAGES/$n" ] || curl -sfL --retry 3 -o "$UIT_IMAGES/$n" "$u"
done < "$OUT/fetch_e1a.txt"
(cd "$UIT_IMAGES" && cut -d' ' -f1 "$OUT/fetch_e1a.txt" | xargs sha256sum) > "$OUT/uit_images.sha256"
[ "$(wc -l < "$OUT/uit_images.sha256")" = 231 ]
cp data/datasets/uitviic/test_data.json "$STAGE/datasets/ktvic/uitviic_test.json"
ln -sfn "$(cd "$UIT_IMAGES" && pwd)" "$STAGE/datasets/ktvic/images"
export HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1
rc_b=0
"$PY" -I scripts/vsps_j_e1e2/e1e2.py e1b --images "$KT_IMAGES" \
    --model "$HUB/models--5CD-AI--Vintern-1B-v3_5/snapshots/$VREV" --out "$OUT" || rc_b=$?
[ -f "$OUT/e1b/probes.jsonl" ] && (cd "$OUT/e1b" && sha256sum probes.jsonl > probes.jsonl.sha256)
echo "e1b exit $rc_b"
rc_a=0
NCS_DATA="$STAGE" "$PY" -I scripts/vsps_j_e1e2/e1e2.py e1a --model "$HUB/models--5CD-AI--Vintern-1B-v3_5/snapshots/$VREV" \
    --qwen "$HUB/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/$QREV" --out "$OUT" || rc_a=$?
[ -f "$OUT/e1a/probes.jsonl" ] && (cd "$OUT/e1a" && sha256sum probes.jsonl > probes.jsonl.sha256)
echo "e1a exit $rc_a"
exit $(( rc_b > rc_a ? rc_b : rc_a ))
