cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -e
# Judge D9 (ii) + (iii), steps A and B of the UPE-MBR test, pre-registered in manuscript/prereg/2026-10-13_upe_mbr.md
# (committed through the gatekeeper before this job is queued).
# A (GPU, ~0.6 GPU-h): P1_dev (35_a, trained on train minus dev300) samples the 300 dev images with the committed
#   sampler: short prompt, 6 samples at T 0.5 and at T 0.8, top_p 0.95, seed 42 (35_lenmatch's test-pool settings).
# B (CPU, a few minutes): scripts/upe_mbr.py choose-t applies the pre-registered T* rule and the F4 temperature reading,
#   and writes /root/r8/upe_temperature.txt, which steps C and D (n3) read after it is copied there.
# No test image is decoded or scored here.
python scripts/ktvic_dev_split.py --verify
echo "e1af906906175ee46aa7ad52600af893  data/splits/ktvic_dev300.txt" | md5sum -c -
echo "74039582f96ed2b2f4d3638e50dd4de6  scripts/e5_sample.py" | md5sum -c -
grep -q "$(sha256sum scripts/upe_mbr.py | cut -c1-64)" manuscript/prereg/2026-10-13_upe_mbr.md
R=p1dev_s42; S=$NCS_DATA/samples; O=/root/r8; mkdir -p $S $O
[ -s $NCS_DATA/runs/$R/adapter_model.safetensors ] || { echo "missing adapter $R (35_a)"; exit 1; }
[ -s $NCS_DATA/rl/$R-dev300-short.preds.json ] || { echo "missing dev greedy of $R (35_a)"; exit 1; }
for T in 0.5 0.8; do
  python scripts/e5_sample.py --adapter $NCS_DATA/runs/$R --split train_data.json \
    --images-file data/splits/ktvic_dev300.txt --limit 0 --prompt short --n 6 --temperature $T --top-p 0.95 \
    --out $S/$R-dev300-short-T$T.jsonl
done
python - $S/$R-dev300-short-T0.5.jsonl $S/$R-dev300-short-T0.8.jsonl <<'PY'
import json, sys
dev = sorted(open("data/splits/ktvic_dev300.txt", encoding="utf-8").read().split())
for f in sys.argv[1:]:
    rows = [json.loads(line) for line in open(f, encoding="utf-8")]
    assert sorted(r["image_id"] for r in rows) == dev and all(len(r["samples"]) == 6 for r in rows), f
    print(f, "OK: 300 dev images x 6 samples")
PY
nice -n 10 python scripts/upe_mbr.py choose-t --greedy $NCS_DATA/rl/$R-dev300-short.preds.json \
  --samples 0.5=$S/$R-dev300-short-T0.5.jsonl 0.8=$S/$R-dev300-short-T0.8.jsonl \
  --out $O/upe_choose_t.json --t-file $O/upe_temperature.txt > $O/upe_choose_t.log 2>&1 || echo "WARN step B exit $?"
echo "T* = $(cat $O/upe_temperature.txt 2>/dev/null || echo 'missing: rerun the step B command')"
