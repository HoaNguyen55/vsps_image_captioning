cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -eo pipefail
# GPU_JOB_PLAN_v1 M2 #6: N9 count-matched leaderboard, registered in
# manuscript/prereg/2026-10-18_n9_count_matched_leaderboard.{md,json} (L6 D1; committed in b8b2500 before any N9 output).
# Eight greedy CHAIR-500 decodes with scripts/lvlm/decode_llava.py, one per run of prereg §1, with the §2 settings:
# the base first, then the six methods, then the POVID full-merge sensitivity run. Decode only. Judge rule CC-018:
# nobody scores, CHAIR-checks or reads these outputs before the analysis script is committed through the gate.
# The checks below stop the job unless the harness, the id list, the image manifest and the prereg pair are tracked,
# unchanged against HEAD and at their registered sha256; the images are checked against the official-bytes manifest.
# A run whose output exists is skipped; an interrupted run resumes from its .partial.jsonl. Batch size as m2_05.
export HF_HUB_OFFLINE=1 VSPS_MACHINE_ID="$(hostname)"   # models load from the prefetched, revision-pinned snapshots
DL=scripts/lvlm/decode_llava.py
IDS=data/coco_probe/chair500_ids.txt
MAN=data/coco_probe/chair500_val2014.sha256
PRE=manuscript/prereg/2026-10-18_n9_count_matched_leaderboard
git ls-files --error-unmatch $DL $IDS $MAN $PRE.md $PRE.json > /dev/null
git diff --quiet HEAD -- $DL $IDS $MAN $PRE.md $PRE.json
sha256sum -c - <<EOF
522bfc1694e21d85ec8335d1ce6e3d9ee401c671da7fc304ec8b4d48c3063561  $DL
00c8458c9fbb19c6f21fcfb82cdac617842c0570e874e1540b19f52fab70f6ee  $IDS
7e244a486e3760f083f916903635f319423aaef57e5d06a566a365a92d77d4f0  $PRE.md
2b232bd3a9e6663a35f3a33da6a1a3f2b9e7530dec44a1d84b08521df0cb6381  $PRE.json
EOF
IMG=$NCS_DATA/datasets/coco_chair500
(cd $IMG && sha256sum -c --quiet /root/vsps/$MAN)
python $DL --selftest
O=$NCS_DATA/results/n9_leaderboard; mkdir -p $O
B=liuhaotian/llava-v1.5-7b@4481d270cc22fd5c4d1bb5df129622006ccd9234
V=openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1
P1=YiyangAiLab/llava_POVID_stage_one_lora@d6c79d54be16246404f910a4453eb64b8b31af25
P2=YiyangAiLab/llava_POVID_stage_two_lora@bdb48949e04cf7605a606b7159726ac161f96b25
run() {  # $1 label, $2 --base repo@rev, then the run's --lora / --drop-vision-lora flags (prereg §2 order)
  [ -e $O/$1.json ] || timeout 7200 python $DL --label $1 --out $O/$1.json --image-ids $IDS --image-dir $IMG \
    --base $2 --vision $V "${@:3}" --max-new-tokens 512 --batch-size ${N9_BATCH_SIZE:-8}
}
run n9_base $B
run n9_povid $B --lora $P1 --lora $P2 --drop-vision-lora
run n9_rlaifv openbmb/RLAIF-V-7B@90e8e7338297c7ee753ae706b1571d46225c5c19
run n9_chairdpo aimagelab/CHAIR-DPO_LLaVA-1.5-7B@bd9ab77aa0f9183ad1a30e4cc8cecc2cd2b175b8
run n9_sentinel $B --lora psp-dada/LLaVA-v1.5-7B-SENTINEL@016b6dced6c24bd26b3736a8cab23ea874dca7c7
run n9_hadpo $B --lora juliozhao/hadpo-llava-1.5@72b1bcf8d86e60937e1df1ca1386d1c97bf95eb1
run n9_opadpo $B --lora zhyang2226/opadpo-lora_llava-v1.5-7b@f589492241ddfaf195cdedd20781edfa8d072717
run n9_povid_fullmerge $B --lora $P1 --lora $P2
ls -la $O
