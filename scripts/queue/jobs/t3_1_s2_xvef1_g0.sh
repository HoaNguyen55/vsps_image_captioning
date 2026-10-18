cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 PYTHONUNBUFFERED=1
set -euo pipefail
# Tier-3 T3.1 / S2 (PD-9 Q1, Q7), pre-registered in manuscript/prereg/2026-10-18_tier3_S2.{md,json} (commit a68fb66);
# the instrument addendum manuscript/prereg/2026-10-18_tier3_S2_instrument.json pins this file and scripts/xv_ef1.py.
# GPU: InternVL3-8B at its registered revision 853e3a79, a scorer only (nothing is generated), gives P(yes) for the
# 1,306 N13 (image, class) items with and without the image: 2,612 one-step forward passes, about 0.5 GPU-h. The model
# is downloaded only if it is not in the HF cache; its four shards and README are sha-checked before it is loaded.
# CPU: gate G0, then the dev readout only if G0 passes. dev300 only: no test image, reference or prediction is read.
# Needs scikit-learn (knn_prior_eval), torchvision, timm and einops in the venv, and data/ktvic_openviic_refs.json
# (read only; xv_ef1.py checks its sha256 before anything runs). Results: /root/outputs/t3_1_s2_xvef1_g0 (backed up).
# A stopped job resumes from its cache; no output is overwritten (a second result file is written as _v2).
J=t3_1_s2_xvef1_g0; O=/root/outputs/$J; S=/root/outputs/sha256/$J.sha256
A=manuscript/prereg/2026-10-18_tier3_S2_instrument.json; F="$A scripts/xv_ef1.py scripts/queue/jobs/$J.sh"
git ls-files --error-unmatch $F > /dev/null  # all three are committed
git diff --quiet HEAD -- $F                   # and unmodified at HEAD
H=$(sha256sum "$0" | cut -c1-64)
grep -q "$H" $A                               # the queued copy is the pinned job file (xv_ef1.py checks its own pin)
python scripts/queue/check_g1_pass.py
python -c "import einops, sklearn, timm, torchvision"
mkdir -p $O /root/outputs/sha256
python scripts/xv_ef1.py score --out $O
sha256sum $O/p_v.jsonl | tee -a $S >> $O/$J.sha256  # the cache's sha256, recorded before any AUROC (prereg §5)
nice -n 10 python scripts/xv_ef1.py analyse --cache $O/p_v.jsonl --sha-file $O/$J.sha256 --out $O
sha256sum $O/*.json | tee -a $S >> $O/$J.sha256
