cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data
set -eo pipefail
# B-F1 (Paper B, PD-22 option (A)): the single final KTVIC test look of P1 + the S1 seed-consensus MBR-3, registered in
# manuscript/prereg/2026-10-20_b_f1_final_stack.{md,json}; the instrument addendum
# manuscript/prereg/2026-10-20_b_f1_instrument.json pins this file and scripts/b_f1/score_b_f1.py.
# Decode only, all three on this one host (one GPU, >= 24 GB; CC-042): the S1 members p1dev_s42 p1dev_s43 p1dev_s44
# on the 558 KTVIC test images with S1's greedy short-prompt settings (scripts/evaluate.py, bf16, its defaults). evaluate.py gets a copy of test_data.json holding only its images
# list, so it writes predictions and scores nothing. `score_b_f1.py check` first verifies the commit, the adapters, the
# base snapshot, the venv, the card, the machine and every test image, and writes that copy; `stamp` writes each
# decode's .sha256 sidecar and provenance. Nobody reads a prediction before `score_b_f1.py run` scores them once from
# the committed copy. About 0.67 GPU-h. Results: /root/outputs/b_f1_ktvic_test (backed up). A decode whose predictions exist is
# skipped and nothing is overwritten; a failure stops the job and goes back to the judge (no re-decode after any output
# has been read).
export HF_HUB_OFFLINE=1 B_F1_JOB_SHA256="$(sha256sum "$0" | cut -c1-64)"
unset NCS_DATASET
PRE=manuscript/prereg/2026-10-20_b_f1_final_stack
ADD=manuscript/prereg/2026-10-20_b_f1_instrument.json
SC=scripts/b_f1/score_b_f1.py
FIX="scripts/evaluate.py scripts/checkpoint_resume_hook.py scripts/queue/check_g1_pass.py data/lb/sets/ktvic_test.tsv"
git ls-files --error-unmatch $PRE.md $PRE.json $ADD $SC $FIX > /dev/null
git diff --quiet HEAD -- $PRE.md $PRE.json $ADD $SC $FIX
sha256sum -c - <<EOF
60a5cf68e9d52a3ca1589b54ed5ac73b44ba803bb1807a5862d0ae41201364c9  $PRE.json
30256ebd2f6353adb157f53d6aa40ea76e06288ae73afa0123d066ffde0c731d  $PRE.md
9c57cc9771d6da84f56534004ebd60c72acd1103ca7c63a741c2f482881304aa  $SC
a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236  scripts/evaluate.py
05466ef5ed3bef2b732ccd01f530a8c977c4c822ef8619b0238f562fb11e5895  scripts/checkpoint_resume_hook.py
39fe181f38bd57a7de32111745bc91de6d684f89c1a931b805da80fe85e104bc  scripts/queue/check_g1_pass.py
456243c0cfc82b0c3cc4ad52c694e11b4d9702f3ca14cd8103c3a82cd74a90eb  data/lb/sets/ktvic_test.tsv
EOF
grep -q "$B_F1_JOB_SHA256" $ADD  # this queue file is byte-identical to the committed job
python scripts/queue/check_g1_pass.py
O=/root/outputs/b_f1_ktvic_test; mkdir -p $O
V=$O/ktvic_test_images_only.json
C=$O/check.json; n=2; while [ -e $C ]; do C=$O/check_v$n.json; n=$((n + 1)); done
python $SC check $C --view $V
for M in p1dev_s42 p1dev_s43 p1dev_s44; do
  N=$M-test-short
  [ -e $O/$N.preds.json ] || timeout 3600 python scripts/evaluate.py --model qwen2.5-vl-7b --adapter $NCS_DATA/runs/$M \
    --split $V --prompt short --name $N --out $O/$N.json >> $O/$N.log 2>&1
  [ -e $O/$N.provenance.json ] || python $SC stamp $O $N $M --view $V --check $C
done
S=$O/SHA256SUMS; n=2; while [ -e $S ]; do S=$O/SHA256SUMS_v$n; n=$((n + 1)); done
(cd $O && find . -maxdepth 1 -type f ! -name 'SHA256SUMS*' -printf '%f\n' | sort | xargs sha256sum) > $S
echo "B-F1 decode done: $(ls $O/*.preds.json | wc -l) prediction files, checksums in $S; nothing is scored here"
