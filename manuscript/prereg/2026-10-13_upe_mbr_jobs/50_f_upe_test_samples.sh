cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -e
# Judge D9 (ii), steps C and E of the UPE-MBR test, pre-registered in manuscript/prereg/2026-10-13_upe_mbr.md.
# C (GPU, ~1.7 GPU-h): KTVIC test samples of the three response-only P1 seeds (p1assist_s42/s43/s44) at T* from step B:
#   committed sampler, short prompt, 6 samples, top_p 0.95, seed 42.
# E (CPU): the pre-registered scoring of F1 and F3 and the kill rules (scripts/upe_mbr.py ktvic).
# Preconditions; the job stops when one is missing:
#   - /root/r8/upe_temperature.txt, written by step B on n2 and copied here;
#   - p1assist_s42 (adapter files, checkpoints not needed) and p1assist_s42-short.preds.json, copied from n2;
#   - p1assist_s43 (50_d) and p1assist_s44 (50_e) with their greedy test predictions.
F=/root/r8/upe_temperature.txt
[ -s $F ] || { echo "missing $F: run step B on n2 and copy the file here"; exit 1; }
T=$(cat $F)
case "$T" in 0.5|0.8) ;; *) echo "bad T* '$T' in $F"; exit 1 ;; esac
echo "74039582f96ed2b2f4d3638e50dd4de6  scripts/e5_sample.py" | md5sum -c -
grep -q "$(sha256sum scripts/upe_mbr.py | cut -c1-64)" manuscript/prereg/2026-10-13_upe_mbr.md
for s in 42 43 44; do
  [ -s $NCS_DATA/runs/p1assist_s$s/adapter_model.safetensors ] || { echo "missing adapter p1assist_s$s"; exit 1; }
  [ -s $NCS_DATA/results/p1assist_s$s-short.preds.json ] || { echo "missing greedy p1assist_s$s-short"; exit 1; }
done
echo "012a1adc8f99f375faf02e85c7ef60b6  $NCS_DATA/results/p1assist_s42-short.preds.json" | md5sum -c -
S=$NCS_DATA/samples; mkdir -p $S
for s in 42 43 44; do
  python scripts/e5_sample.py --adapter $NCS_DATA/runs/p1assist_s$s --split test_data.json --limit 0 --prompt short \
    --n 6 --temperature $T --top-p 0.95 --out $S/p1assist_s$s-test-short-T$T.jsonl
done
python - $S/p1assist_s42-test-short-T$T.jsonl $S/p1assist_s43-test-short-T$T.jsonl \
  $S/p1assist_s44-test-short-T$T.jsonl <<'PY'
import json, sys
sys.path.insert(0, "scripts")
from evaluate import references
test = sorted(references("test_data.json"))
for f in sys.argv[1:]:
    rows = [json.loads(line) for line in open(f, encoding="utf-8")]
    assert sorted(r["image_id"] for r in rows) == test and all(len(r["samples"]) == 6 for r in rows), f
    print(f, f"OK: {len(test)} test images x 6 samples")
PY
A="--system p1assist_s42 $NCS_DATA/results/p1assist_s42-short.preds.json $S/p1assist_s42-test-short-T$T.jsonl"
A="$A --system p1assist_s43 $NCS_DATA/results/p1assist_s43-short.preds.json $S/p1assist_s43-test-short-T$T.jsonl"
A="$A --system p1assist_s44 $NCS_DATA/results/p1assist_s44-short.preds.json $S/p1assist_s44-test-short-T$T.jsonl"
nice -n 10 timeout 7200 python scripts/upe_mbr.py ktvic $A --out $NCS_DATA/results/upe_mbr_ktvic_test.json \
  > $NCS_DATA/results/upe_mbr_ktvic_test.log 2>&1 || echo "WARN step E exit $?"
tail -12 $NCS_DATA/results/upe_mbr_ktvic_test.log
