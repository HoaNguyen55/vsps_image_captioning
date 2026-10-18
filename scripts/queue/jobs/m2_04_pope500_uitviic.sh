cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -e
# GPU_JOB_PLAN_v1 M2 #4: POPE-500 (scripts/pope_vi.py, committed) for the UIT-ViIC-trained adapters, vi + en, greedy.
# CC-005: when scoring a UIT-ViIC-trained adapter, the 21 POPE images that are UIT-ViIC train images are excluded.
# Generation covers all 500 images (pope_vi.py has no image filter and is not modified); the exclusion is applied at
# scoring by scripts/pope_score_excl21.py (committed), which reuses pope_vi.parse/metrics/load and recomputes the
# 21 ids. Comparators: the committed zero-shot / p1_s43 / fuse2_s42 POPE outputs, rescored on the same 479 images.
SC=scripts/pope_score_excl21.py
echo "0e2c117358883bfbde163eb13911b666793a105afb297a595ab9896d252818be  $SC" | sha256sum -c -
O=$NCS_DATA/results/pope_vi_uitviic
for R in uitviic_p1_s42 uitviic_fuse2_s42; do
  python scripts/pope_vi.py --images-dir $NCS_DATA/datasets/coco_probe/val2014 --out-dir $O --adapter $NCS_DATA/runs/$R --name $R
done
ARGS="--repo /root/vsps --data-dir $NCS_DATA/datasets/pope --uitviic-train $NCS_DATA/datasets/uitviic/train_data.json"
[ -e $O/scores_excl21_uitviic.json ] || python $SC $ARGS --out $O/scores_excl21_uitviic.json \
  $O/uitviic_p1_s42-vi.jsonl $O/uitviic_p1_s42-en.jsonl $O/uitviic_fuse2_s42-vi.jsonl $O/uitviic_fuse2_s42-en.jsonl
[ -e $O/scores_excl21_comparators.json ] || python $SC $ARGS --out $O/scores_excl21_comparators.json data/results/pope_vi/*.jsonl
ls -la $O
