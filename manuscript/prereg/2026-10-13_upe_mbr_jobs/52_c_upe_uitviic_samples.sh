cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -e
# Judge D9 (ii), steps D and F of the UPE-MBR test, pre-registered in manuscript/prereg/2026-10-13_upe_mbr.md.
# D (GPU, ~1.2 GPU-h): UIT-ViIC val + test samples (924 + 231 COCO-2014 images) of 52_a's P1 adapter at T* from step B:
#   committed sampler, short prompt, 6 samples, top_p 0.95, seed 42.
#   The adapter is uitviic_p1_s42 with the LEGACY loss mask: 52_a's train_stage2 call has no --loss-mask assistant.
#   F2 compares UPE with the same adapter's greedy caption, so the mask does not enter the contrast.
# F (CPU): the pre-registered scoring of F2 against COCO instance labels and its kill rule (scripts/upe_mbr.py uitviic).
export NCS_DATASET=uitviic
F=/root/r8/upe_temperature.txt
[ -s $F ] || { echo "missing $F: run step B on n2 and copy the file here"; exit 1; }
T=$(cat $F)
case "$T" in 0.5|0.8) ;; *) echo "bad T* '$T' in $F"; exit 1 ;; esac
echo "74039582f96ed2b2f4d3638e50dd4de6  scripts/e5_sample.py" | md5sum -c -
grep -q "$(sha256sum scripts/upe_mbr.py | cut -c1-64)" manuscript/prereg/2026-10-13_upe_mbr.md
R=uitviic_p1_s42; A=$NCS_DATA/runs/$R; S=$NCS_DATA/samples; mkdir -p $S
[ -s $A/adapter_model.safetensors ] || { echo "missing adapter $A (52_a)"; exit 1; }
for s in test val; do
  [ -s $NCS_DATA/results/uitviic_ind_$s/$R-short.preds.json ] || { echo "missing greedy $R $s (52_a)"; exit 1; }
done
for s in test val; do
  python scripts/e5_sample.py --adapter $A --split ${s}_data.json --limit 0 --prompt short --n 6 --temperature $T \
    --top-p 0.95 --out $S/$R-$s-short-T$T.jsonl
done
python - $S/$R-test-short-T$T.jsonl $S/$R-val-short-T$T.jsonl <<'PY'
import json, sys
sys.path.insert(0, "scripts")
from evaluate import references
for f, split in zip(sys.argv[1:], ("test", "val")):
    ids = sorted(references(f"{split}_data.json"))
    rows = [json.loads(line) for line in open(f, encoding="utf-8")]
    assert sorted(r["image_id"] for r in rows) == ids and all(len(r["samples"]) == 6 for r in rows), f
    print(f, f"OK: {len(ids)} {split} images x 6 samples")
PY
A="--split test $NCS_DATA/results/uitviic_ind_test/$R-short.preds.json $S/$R-test-short-T$T.jsonl"
A="$A --split val $NCS_DATA/results/uitviic_ind_val/$R-short.preds.json $S/$R-val-short-T$T.jsonl"
nice -n 10 timeout 7200 python scripts/upe_mbr.py uitviic $A --out $NCS_DATA/results/upe_mbr_uitviic.json \
  > $NCS_DATA/results/upe_mbr_uitviic.log 2>&1 || echo "WARN step F exit $?"
tail -8 $NCS_DATA/results/upe_mbr_uitviic.log
