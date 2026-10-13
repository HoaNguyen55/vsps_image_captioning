cd /root/vsps && . /root/venv-qwen3vl/bin/activate && export NCS_DATA=/root/ncs-data
set -euo pipefail
# Judge D10 (iii), S0 zero-shot object-truth screen for Qwen/Qwen3-VL-8B-Instruct, pre-registered in
# manuscript/prereg/2026-10-13_s0_qwen3vl.md (committed through the gatekeeper before this job is queued).
# Runs in /root/venv-qwen3vl (transformers==4.57.6; /root/vsps/.venv is never touched).
# 1. Verify instrument, FREEZE.txt, and SHA256SUMS hashes against the prereg; verify shards; run CPU preflight.
# 2. Decode COCO probe short (2,500 images), COCO probe detailed (1,000-image seed-0 subset), and POPE-vi (5,127 qs).
# 3. Verify line counts (2,500 / 1,000 / 5,127), score POPE-vi, and compute the pre-registered PASS/KILL verdict.
PREREG=manuscript/prereg/2026-10-13_s0_qwen3vl.md
W=$NCS_DATA/models/Qwen3-VL-8B-Instruct-0c351dd
IMG=$NCS_DATA/datasets/coco_probe/val2014
O=$NCS_DATA/results/s0_qwen3vl
mkdir -p "$O/pope_vi"

for f in scripts/s0_screen.py scripts/coco_probe.py scripts/pope_vi.py scripts/object_prf.py \
         scripts/score_coco_probe.py scripts/abs_halluc.py scripts/evaluate.py \
         rescap/chair.py rescap/vlm/base.py rescap/vlm/mock.py rescap/vi/lexicon.py \
         data/coco_probe/manifest.json data/coco_probe/manifest_s0_detailed1000.json \
         data/coco_probe/probe_val2017_ids.txt data/coco_probe/coco80_vi.json \
         data/coco_probe/chair_synonyms.txt \
         /root/venv-qwen3vl/FREEZE.txt "$W/SHA256SUMS"; do
  grep -q "$(sha256sum "$f" | cut -c1-64)" "$PREREG" || { echo "sha256 mismatch vs prereg: $f"; exit 1; }
done

(cd "$W" && timeout 30m sha256sum -c SHA256SUMS)

python scripts/s0_screen.py preflight --model qwen3-vl-8b --weights "$W" --images-dir "$IMG" \
  --out "$O/preflight.json"

timeout 3h python scripts/coco_probe.py --model qwen3-vl-8b --weights "$W" --name qwen3vl8b_zs \
  --modes short --manifest data/coco_probe/manifest.json --images-dir "$IMG" --out-dir "$O"

timeout 4h python scripts/coco_probe.py --model qwen3-vl-8b --weights "$W" --name qwen3vl8b_zs \
  --modes detailed --manifest data/coco_probe/manifest_s0_detailed1000.json --images-dir "$IMG" --out-dir "$O"

timeout 2h python scripts/pope_vi.py --model qwen3-vl-8b --weights "$W" --name qwen3vl8b_zs \
  --langs vi --images-dir "$IMG" --out-dir "$O/pope_vi"

test "$(wc -l < "$O/qwen3vl8b_zs-short.shard0of1.jsonl")" -eq 2500
test "$(wc -l < "$O/qwen3vl8b_zs-detailed.shard0of1.jsonl")" -eq 1000
test "$(wc -l < "$O/pope_vi/qwen3vl8b_zs-vi.jsonl")" -eq 5127

python scripts/pope_vi.py --score --out-dir "$O/pope_vi"

nice -n 10 python scripts/s0_screen.py verdict \
  --base-coco-dir data/results/coco5000 \
  --cand-coco-dir "$O" \
  --base-name zeroshot --cand-name qwen3vl8b_zs \
  --base-pope "$NCS_DATA/results/pope_vi/zeroshot-vi.jsonl" \
  --cand-pope "$O/pope_vi/qwen3vl8b_zs-vi.jsonl" \
  --out "$O/s0_verdict.json"
