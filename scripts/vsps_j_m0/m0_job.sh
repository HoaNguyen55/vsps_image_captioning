#!/usr/bin/env bash
# VSPS-J M0 GPU job (manuscript/prereg/2026-10-31_vsps_j_m0/PREREG.md section 8). Run from the staged repo copy.
#   PY=<venv python> bash scripts/vsps_j_m0/m0_job.sh --selftest      pins + CPU selftest only
#   PY=<venv python> DATA=<dir with val_raw.json, train_raw.json> IMAGES=<dir> OUT=<dir outside the repo> \
#       bash scripts/vsps_j_m0/m0_job.sh
# Exit codes are m0.py's: 0 DONE, 2 FAULT, 3 PROJECTION_STOP, 4 CAP_STOP.
set -euo pipefail
cd "$(dirname "$0")/../.."
REV=b98f263eab246eb5269ade64edbdca8a887dc44d
PDIR=manuscript/prereg/2026-10-31_vsps_j_m0
: "${PY:?set PY to the venv python}"
(cd scripts/vsps_j_m0 && sha256sum -c --quiet SHA256SUMS)
(cd "$PDIR" && sha256sum -c --quiet SHA256SUMS)
"$PY" -I - <<'EOF_PIN'
import einops, numpy, PIL, timm, torch, torchvision, transformers
want = {transformers: "4.51.3", torch: "2.15.0", torchvision: "0.29.2", numpy: "2.5.4", PIL: "13.0.0",
        timm: "1.0.30", einops: "0.8.2"}  # +cuXXX / +cpu build suffixes allowed on torch and torchvision
bad = {m.__name__: m.__version__ for m, v in want.items() if m.__version__.split("+")[0] != v}
assert not bad, f"environment differs from PREREG section 1: {bad}"
EOF_PIN
"$PY" -I scripts/vsps_j_m0/m0.py selftest
[ "${1:-}" = "--selftest" ] && exit 0
: "${DATA:?}" "${IMAGES:?}" "${OUT:?}"
mkdir -p "$OUT" "$IMAGES"
"$PY" -m pip freeze > "$OUT/pip_freeze.txt"
HUB=${HF_HOME:-$HOME/.cache/huggingface}/hub/models--5CD-AI--Vintern-1B-v3_5
[ -d "$HUB/snapshots/$REV" ] || HF_HUB_DISABLE_TELEMETRY=1 "$PY" -I -c \
    "from huggingface_hub import snapshot_download as s; s('5CD-AI/Vintern-1B-v3_5', revision='$REV')"
mkdir -p "$HUB/refs" && printf %s "$REV" > "$HUB/refs/main"   # the remote code resolves through refs/main
while read -r n; do
    [ -s "$IMAGES/$n" ] || curl -sfL --retry 3 -o "$IMAGES/$n" "http://images.cocodataset.org/val2014/$n"
done < "$PDIR/fetch_images.txt"
(cd "$IMAGES" && xargs sha256sum < "$OLDPWD/$PDIR/fetch_images.txt") > "$OUT/images.sha256"
[ "$(wc -l < "$OUT/images.sha256")" = "$(wc -l < "$PDIR/fetch_images.txt")" ]
rc=0
HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 "$PY" -I scripts/vsps_j_m0/m0.py probe --data "$DATA" --images "$IMAGES" \
    --model "$HUB/snapshots/$REV" --out "$OUT" --device cuda || rc=$?
[ -f "$OUT/probes.jsonl" ] && sha256sum "$OUT/probes.jsonl" > "$OUT/probes.jsonl.sha256"
echo "m0 probe exit $rc"
exit "$rc"
