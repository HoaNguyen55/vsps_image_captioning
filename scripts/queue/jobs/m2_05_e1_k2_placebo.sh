cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -eo pipefail
# GPU_JOB_PLAN_v1 M2 #5: E1 K2 seed placebo, registered in manuscript/prereg/2026-10-18_e1_k2_placebo_addendum.md
# (parent: manuscript/research_r10/E1/REPORT.txt §4 K2). Two sampling seeds of LLaVA-1.5-7B on the CHAIR-500 ids,
# decoded by scripts/lvlm/decode_llava.py with exactly the addendum §1 settings. Decode only: the committed scorer
# scores K2 later (N9 prereg §8). Rule D-W13-6: no K2 output before the addendum is committed; the checks below stop
# the job unless the addendum, the harness and the id list are tracked, unchanged against HEAD and at their sha256.
# The images are COCO val2014 files, checked against data/coco_probe/chair500_val2014.sha256 (official bytes).
# A run whose output exists is skipped; an interrupted run resumes from its .partial.jsonl (same batches, same seeds).
# Batch size: 8 unless N9_BATCH_SIZE is set; if 8 does not fit, set N9_BATCH_SIZE=4 for this job AND m2_06 (prereg §2).
export HF_HUB_OFFLINE=1 VSPS_MACHINE_ID="$(hostname)"   # models load from the prefetched, revision-pinned snapshots
DL=scripts/lvlm/decode_llava.py
IDS=data/coco_probe/chair500_ids.txt
MAN=data/coco_probe/chair500_val2014.sha256
ADD=manuscript/prereg/2026-10-18_e1_k2_placebo_addendum.md
git ls-files --error-unmatch $DL $IDS $MAN $ADD > /dev/null
git diff --quiet HEAD -- $DL $IDS $MAN $ADD
sha256sum -c - <<EOF
522bfc1694e21d85ec8335d1ce6e3d9ee401c671da7fc304ec8b4d48c3063561  $DL
00c8458c9fbb19c6f21fcfb82cdac617842c0570e874e1540b19f52fab70f6ee  $IDS
c6238a7c766bf2f331a1c5ae197c2f06765a8e122dcb70d52a97896c42f8d920  $ADD
EOF
IMG=$NCS_DATA/datasets/coco_chair500
(cd $IMG && sha256sum -c --quiet /root/vsps/$MAN)
python $DL --selftest
O=$NCS_DATA/results/e1_k2_placebo; mkdir -p $O
B=liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234
V=openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1
for S in 1 2; do
  [ -e $O/k2_seed$S.json ] || timeout 7200 python $DL --label k2_seed$S --out $O/k2_seed$S.json --image-ids $IDS --image-dir $IMG \
    --base $B --vision $V --do-sample --temperature 1.0 --top-p 1.0 --top-k 0 --seed $S \
    --max-new-tokens 512 --batch-size ${N9_BATCH_SIZE:-8}
done
ls -la $O
