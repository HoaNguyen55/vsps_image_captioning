cd /root/vsps && . /root/venv-lb/bin/activate && export NCS_DATA=/root/ncs-data
set -eo pipefail
# DRAFT (task LB, 2026-10-19; not committed, not queued). A-N2, a multi-LVLM leaderboard under gold completeness (Paper A Section 7), registered in manuscript/prereg/2026-10-19_a_n2_lvlm_gold_ladder.{md,json}
# (commit before any output, D-W13-6). Decode only: 32 runs of scripts/lb/decode_hf_vlm.py, which reads every
# setting from the prereg JSON. No scoring here: the scorer is committed later, before any output is scored, and
# nobody reads the decodes before then. Venv /root/venv-lb = a copy of /root/venv-qwen3vl (G2-B pins) + num2words
# (add-only, freeze recorded before queueing). The checks stop the job unless the decoder, the G2-B helper it imports,
# evaluate.py (prompts), rescap/vlm/base.py (dtype keyword), the prereg pair and the set manifests are tracked, equal to
# HEAD and at their sha256. Each model is fetched at its pinned revision (pinned files only) and checked file by file;
# every image is checked against its manifest row before it is decoded. A run whose output exists is skipped; an
# interrupted run resumes at its next unfinished batch slice. LB_MODELS="k1 k2" runs a subset (to split machines);
# LB_PRUNE=1 deletes a snapshot after its runs. GPU plan: M1, after S3 (PD-17).
# Regenerate this file with build_lb_v2.py whenever a pinned file changes.
# PRE-QUEUE CHECKLIST (operator; log each item in the machine's EVENTS log before queueing):
#  [ ] HEAD is the commit that adds this job, the prereg pair, scripts/lb/decode_hf_vlm.py and data/lb/ together
#  [ ] disk: >= 125 GB free under $NCS_DATA/models/lb for all snapshots (20 GB with LB_PRUNE=1);
#      the job re-checks this below and stops if it is short
#  [ ] venv /root/venv-lb = /root/venv-qwen3vl + num2words==0.5.14 only (add-only freeze diff); record in EVENTS the
#      torch, torchvision, transformers, accelerate and num2words versions and the pip freeze sha256 (printed below)
#  [ ] no token or credential is set: every model is ungated
export HF_HUB_OFFLINE=1 VSPS_MACHINE_ID="$(hostname)" VSPS_JOB_SHA256="$(sha256sum "$0" | cut -c1-64)"
DEC=scripts/lb/decode_hf_vlm.py
PRE=manuscript/prereg/2026-10-19_a_n2_lvlm_gold_ladder
FIX="scripts/g2b/decode_qwen3vl.py scripts/evaluate.py rescap/vlm/base.py"
SETS="data/lb/sets/cv295.tsv data/lb/sets/uitviic_test.tsv "
git ls-files --error-unmatch $DEC $PRE.md $PRE.json $FIX $SETS > /dev/null
git diff --quiet HEAD -- $DEC $PRE.md $PRE.json $FIX $SETS
sha256sum -c - <<EOF
e2de18811e2ffeb61ed72cb2399d41123e9a8f6ccd73a5ec35f778dcbe2f5ac4  $DEC
4789d998d3f5219966730e20b722dbf0adea5017bb3afc41fdd3280952f4d24b  $PRE.md
d5714e2b25e5f1d36fa42813cc5891a82d0b80a73e69fb08d940e05e2055f309  $PRE.json
16d1ddd47385aedab6422bf308b0a202846321171aa20cd481a1042829d3f4b1  data/lb/sets/cv295.tsv
dbadc28724d7a07b599325cd996084934d76e6c4c6a885e64e8de333d6a6665b  data/lb/sets/uitviic_test.tsv
8a855ef483c933621776099b6f9de3b60c4fbfaaf706bb40c74e7d84d9dfb5e5  scripts/g2b/decode_qwen3vl.py
a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236  scripts/evaluate.py
e8fee5bc5b729534af67c6e462a27f0d83ba611f18ff8e3f2717b11eb393ae93  rescap/vlm/base.py
EOF
VSPS_VENV_FREEZE_SHA256="$(pip freeze | sha256sum | cut -c1-64)"
export VSPS_VENV_FREEZE_SHA256
pip freeze | grep -i -E '^(torch|torchvision|transformers|accelerate|num2words)==' ; echo "freeze sha256 $VSPS_VENV_FREEZE_SHA256"
NEED=125; if [ "${LB_PRUNE:-0}" = 1 ]; then NEED=20; fi
mkdir -p $NCS_DATA/models/lb
AVAIL=$(df -BG --output=avail $NCS_DATA/models/lb | tail -1 | tr -dc 0-9)
if [ "$AVAIL" -lt "$NEED" ]; then echo "disk: $AVAIL GB free, $NEED GB needed"; exit 1; fi
python $DEC --selftest --prereg $PRE.json
O=/root/outputs/2026-10-19_a_n2_lvlm_gold_ladder; mkdir -p $O
for M in ${LB_MODELS:-$(python $DEC --prereg $PRE.json --models)}; do
  W=$NCS_DATA/models/lb/$M
  HF_HUB_OFFLINE=0 timeout 2h python $DEC --prereg $PRE.json --fetch $M --snapshot $W
  for R in $(python $DEC --prereg $PRE.json --list-runs --model $M); do
    [ -e $O/$R.preds.json ] || timeout 10800 python $DEC --prereg $PRE.json --run-id $R --snapshot $W --out-dir $O
  done
  if [ "${LB_PRUNE:-0}" = 1 ]; then rm -rf "$W"; fi
done
ls -la $O
