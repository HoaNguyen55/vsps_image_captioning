cd /root/vsps && . /root/venv-qwen3vl/bin/activate && export NCS_DATA=/root/ncs-data
set -eo pipefail
# GPU_JOB_PLAN_v1 M2 #7: G2-B extended, the Qwen3-VL-8B-Instruct zero-shot ladder of Paper A Section 7.6, registered in
# manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.{md,json} (committed in 0932ba1 before any G2-B output; D-W13-6).
# 23 decodes with scripts/g2b/decode_qwen3vl.py, which reads every setting from the prereg JSON (runs, decode block,
# design constants, model pins). Its --check-inputs step checks the package versions, the snapshot's SHA256SUMS, the
# pinned id lists and dataset files and the prompts, and writes the per-set image sha256 lists that every run re-checks.
# Decode only: scripts/g2b/score_g2b.py, committed with this job before any output, scores the decodes later (its
# fidelity self-check is data/results/g2b/selfcheck.json); nobody scores or reads the decodes before then.
# Separate venv /root/venv-qwen3vl: torch, torchvision, transformers and accelerate must have the registered versions
# (the decoder compares them with the prereg); the main .venv is not used.
# The checks below stop the job unless the decoder, the scorer, its self-check, the prereg pair, the CV295 image
# manifest and the id lists are tracked, unchanged against HEAD and at their sha256. The CV295 images are checked
# against data/coco_probe/cv295_val2014.sha256 (official val2014.zip bytes), the model files against SHA256SUMS.
# A run whose output exists is skipped; an interrupted run resumes from its .partial.jsonl.
export HF_HUB_OFFLINE=1 VSPS_MACHINE_ID="$(hostname)" VSPS_JOB_SHA256="$(sha256sum "$0" | cut -c1-64)"
DEC=scripts/g2b/decode_qwen3vl.py
SCO=scripts/g2b/score_g2b.py
CHK=data/results/g2b/selfcheck.json
PRE=manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder
MAN=data/coco_probe/cv295_val2014.sha256
IDS="data/coco_probe/probe_val2017_ids.txt data/coco_probe/manifest.json data/xm3600_subset.txt"
git ls-files --error-unmatch $DEC $SCO $CHK $PRE.md $PRE.json $MAN $IDS > /dev/null
git diff --quiet HEAD -- $DEC $SCO $CHK $PRE.md $PRE.json $MAN $IDS
sha256sum -c - <<EOF
8a855ef483c933621776099b6f9de3b60c4fbfaaf706bb40c74e7d84d9dfb5e5  $DEC
66c665c7a71d3b97abbf89fd5bf13871910449ad1c053ff5fb0b18663e3e7ae5  $SCO
e29f0a4f8078e72d334f2b421b9e703bd788606ba02c96f7232fe8bc96bc5acc  $CHK
2e6b3e87114478f7664a02b3c1b04eaca8dc7a24337dc1ce0293dbc4a0d2608b  $PRE.md
c506bc777b483f5097561d2894a535f33e5e9e27745af07c0f979fbac5560055  $PRE.json
5aee7a6b1d357444294ffc0bc4e183ed6b26f6bd5b24217cecce6af3da62c0e8  $MAN
EOF
W=$NCS_DATA/models/Qwen3-VL-8B-Instruct-0c351dd
(cd $W && timeout 30m sha256sum -c --quiet SHA256SUMS)
(cd $NCS_DATA/datasets/coco_probe/val2014 && sha256sum -c --quiet /root/vsps/$MAN)
VSPS_VENV_FREEZE_SHA256="$(pip freeze | sha256sum | cut -c1-64)"
export VSPS_VENV_FREEZE_SHA256
python $DEC --selftest
O=/root/outputs/g2b_qwen3vl; mkdir -p $O
python $DEC --check-inputs --snapshot $W --out-dir $O
RUNS="$(python $DEC --list-runs)"
for R in $RUNS; do
  [ -e $O/$R.preds.json ] || [ -e $O/$R.samples.jsonl ] || timeout 7200 python $DEC --run-id $R --snapshot $W --out-dir $O
done
ls -la $O
