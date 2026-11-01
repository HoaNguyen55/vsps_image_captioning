#!/usr/bin/env bash
# VSPS-J E2b unscored rate run (PREREG_DRAFT.md section 6). M8 (the PI-1101r RTX 4090) only, ALONE on the GPU.
#   PY=/root/venv-lb/bin/python bash scripts/vsps_j_e2b/e2b_job.sh --selftest      pins + CPU selftest only
#   PY=... HF_TOKEN=<Aya gated read token, never logged> DATA=<dir with val_raw.json> IMAGES=<the plan's 171 images> \
#     bash scripts/vsps_j_e2b/e2b_job.sh rate
# OUT is fixed at /root/e2b_rate (launch precondition: the laptop's M8 backup pull excludes /e2b_rate/).
# Snapshots go to /root/.cache/e2b_hub (inside the pull's .cache/ exclude). The cap clock (3.0 GPU-h) starts at
# launch.json, written by e2b.py before the first snapshot fetch, so downloads count.
# Exit codes are e2b.py's: 0 DONE, 2 FAULT, 4 CAP_STOP.
set -euo pipefail
cd "$(dirname "$0")/../.."
LB_FREEZE=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784   # setup_gpu.sh H_LB (transformers 4.57.6)
PDIR=manuscript/prereg/2026-11-01_vsps_j_e2b_tier1
OUT=/root/e2b_rate
HUB=/root/.cache/e2b_hub
SUB=${1:?usage: e2b_job.sh --selftest | rate}
case "$SUB" in --selftest|rate) ;; *) echo "unknown sub-job $SUB"; exit 2 ;; esac
: "${PY:?set PY to the venv-lb python}"
(cd scripts/vsps_j_e2b && sha256sum -c --quiet SHA256SUMS)
(cd scripts/vsps_j_m0 && sha256sum -c --quiet SHA256SUMS)
(cd "$PDIR" && sha256sum -c --quiet SHA256SUMS)
sha256sum -c --quiet <<'EOF_LB'
e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4  scripts/lb/decode_hf_vlm.py
8a855ef483c933621776099b6f9de3b60c4fbfaaf706bb40c74e7d84d9dfb5e5  scripts/g2b/decode_qwen3vl.py
e8fee5bc5b729534af67c6e462a27f0d83ba611f18ff8e3f2717b11eb393ae93  rescap/vlm/base.py
EOF_LB
[ "$("$PY" -m pip freeze | sha256sum | cut -c1-64)" = "$LB_FREEZE" ] || { echo "venv-lb freeze differs"; exit 2; }
"$PY" -I scripts/vsps_j_e2b/e2b.py selftest
[ "$SUB" = "--selftest" ] && exit 0
: "${DATA:?}" "${IMAGES:?}" "${HF_TOKEN:?Aya-Vision-8B is gated}"
for d in "$DATA" "$IMAGES"; do   # staged inputs sit inside the backup pull's .cache/ exclude
    case "$(cd "$d" && pwd)/" in /root/.cache/*) ;; *) echo "stage DATA and IMAGES under /root/.cache/"; exit 2 ;; esac
done
nvidia-smi --query-gpu=name --format=csv,noheader | grep -q "RTX 4090" || { echo "not an RTX 4090"; exit 2; }
[ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ] || { echo "GPU not idle at launch"; exit 2; }
mkdir -p "$OUT" "$HUB"
"$PY" -m pip freeze > "$OUT/pip_freeze_rate.txt"
rc=0
HF_HUB_DISABLE_TELEMETRY=1 "$PY" -I scripts/vsps_j_e2b/e2b.py rate --data "$DATA" --images "$IMAGES" --out "$OUT" \
    --hub "$HUB" --with-qwen3 || rc=$?
(cd "$OUT" && find . -type f ! -name OUT_MANIFEST.sha256 -print0 | sort -z | xargs -0 sha256sum > OUT_MANIFEST.sha256)
echo "rate exit $rc"
exit "$rc"
