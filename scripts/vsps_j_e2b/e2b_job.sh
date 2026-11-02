#!/usr/bin/env bash
# VSPS-J E2b unscored rate run (PREREG_DRAFT.md section 6). M8 (the PI-1101r RTX 4090) only, ALONE on the GPU.
#   PY=/root/venv-lb/bin/python bash scripts/vsps_j_e2b/e2b_job.sh --selftest      pins + CPU selftest only
#   PY=... HF_TOKEN=<Aya gated read token, never logged> DATA=<dir with val_raw.json> IMAGES=<the plan's 171 images> \
#     bash scripts/vsps_j_e2b/e2b_job.sh rate
#   PY=... DATA=... IMAGES=<the probe images after the W25 drops> RATE=<pulled rate.json> CELL=<cand>_<form>_<lang> \
#     [RES=<vi res.json, EN only>] [RERUN_OF=<archived faulted folder of this cell> | LOST_RUN=<OPS id>] \
#     bash scripts/vsps_j_e2b/e2b_job.sh probe
# probe (tier 1b-i, AMENDMENT_1 D10): OUT /root/e2b_probe/<cell>, the cap from the fixed CAPS table (never typed), no
# HF_TOKEN (every kept cell is ungated), a 30 s nvidia-smi logger beside the run, a per-cell OUT_MANIFEST.
# OUT is fixed at /root/e2b_rate (launch precondition: the laptop's M8 backup pull excludes /e2b_rate/).
# Snapshots go to /root/.cache/e2b_hub (inside the pull's .cache/ exclude). The cap clock (3.0 GPU-h) starts at
# launch.json, written by e2b.py before the first snapshot fetch, so downloads count.
# Exit codes are e2b.py's: 0 DONE, 2 FAULT (rate; probe: non-finite mass), 3 PROJECTION_STOP, 4 CAP_STOP,
# 5 ENV_FAULT, 6 PIN_FAULT, 7 TOKEN_FAULT, 8 EN_SMOKE_FAULT (probe; AMENDMENT_1 D1).
set -euo pipefail
cd "$(dirname "$0")/../.."
LB_FREEZE=685ffe2a0100ce2489cccd77313d366fb1dce4455871a9d82f65aa139fa85784   # setup_gpu.sh H_LB (transformers 4.57.6)
PDIR=manuscript/prereg/2026-11-01_vsps_j_e2b_tier1
OUT=/root/e2b_rate
HUB=/root/.cache/e2b_hub
SUB=${1:?usage: e2b_job.sh --selftest | rate}
case "$SUB" in --selftest|rate|probe) ;; *) echo "unknown sub-job $SUB"; exit 2 ;; esac
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
: "${DATA:?}" "${IMAGES:?}"
for d in "$DATA" "$IMAGES"; do   # staged inputs sit inside the backup pull's .cache/ exclude
    case "$(cd "$d" && pwd)/" in /root/.cache/*) ;; *) echo "stage DATA and IMAGES under /root/.cache/"; exit 2 ;; esac
done
nvidia-smi --query-gpu=name --format=csv,noheader | grep -q "RTX 4090" || { echo "not an RTX 4090"; exit 2; }
if [ "$SUB" = probe ]; then   # D10: tier 1b-i, one cell per call
    : "${CELL:?CELL=<cand>_<form>_<lang>}" "${RATE:?RATE=<pulled rate.json>}"
    unset HF_TOKEN   # NB-4: every kept cell is ungated; no token in the probe environment
    declare -A CAPS=([qwen25vl_7b_FA]=0.7 [internvl3_8b_FA]=2.3 [qwen3vl_8b_FA]=0.6 [qwen3vl_8b_FB]=0.6)  # AMENDMENT_1 §C
    lang=${CELL##*_}; cf=${CELL%_*}; form=${cf##*_}; cand=${cf%_*}
    cap=${CAPS[$cf]:-}; [ -n "$cap" ] || { echo "REFUSED: $cf is not a kept 1b-i cell"; exit 2; }
    [ "$lang" = vi ] || [ -n "${RES:-}" ] || { echo "REFUSED: the EN frame needs RES (the vi winner)"; exit 2; }
    [ "$(sha256sum < "$RATE" | cut -c1-64)" = a57179187068127522d09d1e98cd7b651220fe5417e69c87d1d58495b844ae91 ] \
        || { echo "RATE is not the pulled rate.json"; exit 2; }
    POUT=/root/e2b_probe
    mkdir -p "$POUT" "$HUB"
    nvidia-smi --query-gpu=timestamp,memory.used,utilization.gpu --format=csv -l 30 >> "$POUT/${CELL}_smi.log" &
    SMI=$!
    rc=0
    HF_HUB_DISABLE_TELEMETRY=1 "$PY" -I scripts/vsps_j_e2b/e2b.py probe --cand "$cand" --form "$form" --lang "$lang" \
        --data "$DATA" --images "$IMAGES" --out "$POUT" --hub "$HUB" --cap-h "$cap" --rate "$RATE" \
        ${RES:+--res "$RES"} ${RERUN_OF:+--rerun-of "$RERUN_OF"} ${LOST_RUN:+--lost-run "$LOST_RUN"} || rc=$?
    kill "$SMI" 2>/dev/null || true
    [ ! -d "$POUT/$CELL" ] || (cd "$POUT/$CELL" && find . -type f ! -name OUT_MANIFEST.sha256 -print0 | sort -z \
        | xargs -0 sha256sum > OUT_MANIFEST.sha256)
    echo "probe $CELL exit $rc"
    exit "$rc"
fi
: "${HF_TOKEN:?Aya-Vision-8B is gated}"
[ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ] || { echo "GPU not idle at launch"; exit 2; }
mkdir -p "$OUT" "$HUB"
"$PY" -m pip freeze > "$OUT/pip_freeze_rate.txt"
rc=0
HF_HUB_DISABLE_TELEMETRY=1 "$PY" -I scripts/vsps_j_e2b/e2b.py rate --data "$DATA" --images "$IMAGES" --out "$OUT" \
    --hub "$HUB" --with-qwen3 || rc=$?
(cd "$OUT" && find . -type f ! -name OUT_MANIFEST.sha256 -print0 | sort -z | xargs -0 sha256sum > OUT_MANIFEST.sha256)
echo "rate exit $rc"
exit "$rc"
