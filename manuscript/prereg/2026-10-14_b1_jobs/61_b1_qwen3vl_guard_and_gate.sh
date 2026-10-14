#!/usr/bin/env bash
cd /root/vsps && . /root/venv-qwen3vl/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PYTHONPATH="/root/vsps:/root/vsps/.venv/lib/python3.10/site-packages:${PYTHONPATH:-}"
set -euo pipefail
# Judge PD-5 Q1 & Q2, PD-2, D17: B1 Second-Backbone (Qwen/Qwen3-VL-8B-Instruct) Step 1 dev300 zero-shot guard
# and Step 2 1-seed P1 gate on train_nodev (train minus dev300, 3,469 images, seed 42, --loss-mask assistant).
# Pre-registered in manuscript/prereg/2026-10-14_b1_qwen3vl_backbone.md and
# manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json before any B1 KTVIC output exists.
# Records "machine_id": $(hostname) in every output JSON (PD-5 Q2).

PREREG_JSON=manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json
PREREG_MD=manuscript/prereg/2026-10-14_b1_qwen3vl_backbone.md
W=$NCS_DATA/models/Qwen3-VL-8B-Instruct-0c351dd
O=$NCS_DATA/results/b1_qwen3vl
RUN_DIR=$NCS_DATA/runs/b1_qwen3vl_p1_nodev_s42
SFT_DIR=$NCS_DATA/gold_b1_nodev/base
MACHINE_ID="$(hostname)"
mkdir -p "$O" "$SFT_DIR"

# 0. Preconditions: verify instrument hashes, venv freeze, and weight shards against the preregistration.
for f in scripts/train_stage2.py scripts/evaluate.py scripts/object_prf.py scripts/prereg_ladder_check.py \
         scripts/abs_halluc.py scripts/ktvic_dev_split.py scripts/build_gold_sft.py \
         rescap/vlm/base.py rescap/vlm/mock.py rescap/vi/lexicon.py \
         data/splits/ktvic_train_minus_dev300.txt \
         /root/venv-qwen3vl/FREEZE.txt "$W/SHA256SUMS"; do
  grep -q "$(sha256sum "$f" | cut -c1-64)" "$PREREG_JSON" || { echo "sha256 mismatch vs $PREREG_JSON: $f"; exit 1; }
done

CHAIR_SHA="$(sha256sum rescap/chair.py | cut -c1-64)"
if [ "$CHAIR_SHA" != "fd1d012398cae5d1984bb4effdf18919e157f1c770b8a13adbb070a8b659ec6b" ] && \
   [ "$CHAIR_SHA" != "e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3" ]; then
  echo "unexpected rescap/chair.py sha256: $CHAIR_SHA"
  exit 1
fi

(cd "$W" && timeout 30m sha256sum -c SHA256SUMS)
python scripts/ktvic_dev_split.py --verify --json-dir "$NCS_DATA/datasets/ktvic_dev"

# 1. Step 1 (~0.2 GPU-h): Zero-shot dev300 guard (short & detailed on 300 KTVIC dev300 images).
timeout 1h python - "$W" "$O" "$MACHINE_ID" "$PREREG_JSON" <<'PY'
import json
import os
import sys
import time
import unicodedata
from pathlib import Path
import torch
from PIL import Image
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration

sys.path.insert(0, "/root/vsps")
sys.path.insert(0, "/root/vsps/scripts")
import evaluate as ev
import object_prf as op
from abs_halluc import CJK
from rescap.vlm.base import dtype_kwarg
from rescap.vlm.mock import looks_vietnamese
from s0_screen import norm_tone

weights, out_dir, machine_id, prereg_path = sys.argv[1:5]
out_path = Path(out_dir)
prereg = json.loads(Path(prereg_path).read_text(encoding="utf-8"))
guard_cfg = prereg["step1_zeroshot_dev300_guard"]

dev_dir = Path(os.environ["NCS_DATA"]) / "datasets" / "ktvic_dev"
dev_data = json.loads((dev_dir / "dev_data.json").read_text(encoding="utf-8"))
names = {str(img.get("id", img.get("image_id"))): img.get("file_name") or img.get("filename")
         for img in dev_data["images"]}
refs: dict[str, list[str]] = {}
for ann in dev_data["annotations"]:
    if ann.get("caption"):
        refs.setdefault(str(ann["image_id"]), []).append(ann["caption"])
image_ids = sorted(names.keys(), key=lambda x: int(x) if x.isdigit() else x)
assert len(image_ids) == 300, len(image_ids)

px = 32 * 32
model = Qwen3VLForConditionalGeneration.from_pretrained(
    weights, attn_implementation="sdpa", device_map={"": 0}, **dtype_kwarg(torch.bfloat16)
)
model.eval()
processor = AutoProcessor.from_pretrained(weights, min_pixels=256 * px, max_pixels=1024 * px)

gold_v1 = {i: set().union(*(op.objects_in(r, raw_tone=True) for r in rs)) if "raw_tone" in op.objects_in.__code__.co_varnames
           else set().union(*(op.objects_in(unicodedata.normalize("NFC", r)) for r in rs))
           for i, rs in refs.items()}
gold_v2 = {i: set().union(*(op.objects_in(norm_tone(r)) for r in rs)) for i, rs in refs.items()}

modes_out = {}
all_pass = True
for mode, max_new in (("short", 60), ("detailed", 160)):
    t0 = time.time()
    preds: dict[str, str] = {}
    prompt = ev.PROMPTS[mode]
    for iid in image_ids:
        image = Image.open(dev_dir / "images" / names[iid]).convert("RGB")
        messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": prompt}]}]
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = processor(text=[text], images=[image], return_tensors="pt").to(model.device)
        with torch.no_grad():
            ids = model.generate(**inputs, max_new_tokens=max_new, do_sample=False)
        preds[iid] = processor.batch_decode(
            ids[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True
        )[0].strip()
    elapsed = time.time() - t0
    pred_file = out_path / f"b1_qwen3vl_zs-dev300-{mode}.preds.json"
    pred_file.write_text(json.dumps({
        "machine_id": machine_id,
        "backbone": prereg["backbone"],
        "revision": prereg["revision"],
        "split": "dev300",
        "prompt_style": mode,
        "n_images": len(preds),
        "elapsed_sec": round(elapsed, 3),
        "predictions": preds,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    vi_cnt = sum(1 for c in preds.values() if looks_vietnamese(c))
    cjk_cnt = sum(1 for c in preds.values() if CJK.search(c))
    vi_share = vi_cnt / len(preds)
    cjk_rate = cjk_cnt / len(preds)

    os.environ["RESCAP_RAW_TONE"] = "1"
    sc_v1 = op.scores(op.image_counts(preds, gold_v1))
    os.environ["RESCAP_RAW_TONE"] = "0"
    preds_v2 = {k: norm_tone(v) for k, v in preds.items()}
    sc_v2 = op.scores(op.image_counts(preds_v2, gold_v2))

    m_v1 = sc_v1["mentions_per_caption"]
    m_cfg = guard_cfg["thresholds"][mode]
    mode_pass = (
        vi_share >= m_cfg["vietnamese_share_min"]
        and cjk_rate <= m_cfg["cjk_rate_max"]
        and m_cfg["mentions_per_caption_min"] <= m_v1 <= m_cfg["mentions_per_caption_max"]
    )
    all_pass = all_pass and mode_pass
    modes_out[mode] = {
        "n_images": len(preds),
        "elapsed_sec": round(elapsed, 3),
        "vietnamese_count": vi_cnt,
        "vietnamese_share": round(vi_share, 6),
        "cjk_count": cjk_cnt,
        "cjk_rate": round(cjk_rate, 6),
        "matcher_v1": sc_v1,
        "matcher_v2": sc_v2,
        "pass": mode_pass,
    }

guard_report = {
    "machine_id": machine_id,
    "step": "step1_zeroshot_dev300_guard",
    "backbone": prereg["backbone"],
    "revision": prereg["revision"],
    "modes": modes_out,
    "pass": all_pass,
}
(out_path / "step1_dev300_guard.json").write_text(
    json.dumps(guard_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
if not all_pass:
    raise SystemExit("Step 1 dev300 zero-shot guard FAILED; aborting before Step 2 SFT.")
print("Step 1 dev300 zero-shot guard PASSED.")
PY

# 2. Build deterministic 3,469-row train_nodev (train minus dev300) SFT dataset and verify sha256 + C1 disjointness.
python scripts/build_gold_sft.py --annotations "$NCS_DATA/datasets/ktvic/train_data.json" \
  --out "$SFT_DIR" --images-file data/splits/ktvic_train_minus_dev300.txt
echo "971879742e85d710fc828fa526b735d0c0b6469b4988e3d5402a26fb1b666f16  $SFT_DIR/sft.jsonl" | sha256sum -c -
python scripts/ktvic_dev_split.py --sft "$SFT_DIR/sft.jsonl"

# 3. Step 2 (~1.8 GPU-h): 1-seed P1 SFT gate (seed 42, 2 epochs, lr=1e-4, LoRA r=16, alpha=32, --loss-mask assistant).
timeout 14400 python - "$W" "$SFT_DIR" "$RUN_DIR" "$O/step2_train_s42_telemetry.json" "$MACHINE_ID" <<'PY' 2>&1 | tee "$O/train_b1_p1_nodev_s42.log"
import json
import sys
import time
from pathlib import Path
import torch
import transformers
from transformers import Qwen3VLForConditionalGeneration

sys.path.insert(0, "/root/vsps")
sys.path.insert(0, "/root/vsps/scripts")
import train_stage2 as ts2

weights, sft_dir, run_dir, telemetry_out, machine_id = sys.argv[1:6]
# Match Qwen3-VL-8B-Instruct architecture and 32x32 patch*merge token budget (256-512 vision tokens in 4-bit NF4 LoRA)
ts2.P = 32 * 32
ts2.MIN_PIXELS = 256 * ts2.P
transformers.Qwen2_5_VLForConditionalGeneration = Qwen3VLForConditionalGeneration

torch.cuda.reset_peak_memory_stats()
t0 = time.time()
sys.argv = [
    "train_stage2.py",
    "--stage", "sft",
    "--base-model", weights,
    "--data", sft_dir,
    "--out", run_dir,
    "--epochs", "2",
    "--lr", "1e-4",
    "--lora-r", "16",
    "--lora-alpha", "32",
    "--seed", "42",
    "--loss-mask", "assistant",
]
rc = ts2.main()
elapsed = time.time() - t0
peak_vram_gb = torch.cuda.max_memory_allocated() / 1e9

metrics_path = Path(run_dir) / "metrics.jsonl"
steps = 0
if metrics_path.exists():
    for line in metrics_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            if "step" in row:
                steps = max(steps, int(row["step"]))
step_time_sec = elapsed / steps if steps > 0 else None

telemetry = {
    "machine_id": machine_id,
    "run_id": "b1_qwen3vl_p1_nodev_s42",
    "base_model": weights,
    "seed": 42,
    "epochs": 2.0,
    "lr": 1e-4,
    "lora_r": 16,
    "lora_alpha": 32,
    "loss_mask": "assistant",
    "train_examples": 3469,
    "total_steps": steps,
    "elapsed_sec": round(elapsed, 3),
    "step_time_sec": round(step_time_sec, 4) if step_time_sec is not None else None,
    "peak_vram_gb": round(peak_vram_gb, 4),
    "peak_vram_gate_le_22gb": bool(peak_vram_gb <= 22.0),
}
Path(telemetry_out).write_text(json.dumps(telemetry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
if peak_vram_gb > 22.0:
    raise SystemExit(f"Peak VRAM {peak_vram_gb:.2f} GB exceeded 22.0 GB gate")
sys.exit(rc)
PY

grep -q "loss mask: assistant" "$O/train_b1_p1_nodev_s42.log"
grep -q "training set: 3469 examples" "$O/train_b1_p1_nodev_s42.log"
[ -s "$RUN_DIR/adapter_model.safetensors" ] || { echo "missing adapter $RUN_DIR/adapter_model.safetensors"; exit 1; }

# 4. Decode dev300 and ktvic_test (short & detailed) with b1_qwen3vl_p1_nodev_s42.
timeout 2h python - "$W" "$RUN_DIR" "$O" "$MACHINE_ID" <<'PY'
import json
import os
import sys
import time
from pathlib import Path
import torch
from peft import PeftModel
from PIL import Image
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration

sys.path.insert(0, "/root/vsps")
sys.path.insert(0, "/root/vsps/scripts")
import evaluate as ev
from rescap.vlm.base import dtype_kwarg

weights, adapter_dir, out_dir, machine_id = sys.argv[1:5]
out_path = Path(out_dir)
px = 32 * 32

base_model = Qwen3VLForConditionalGeneration.from_pretrained(
    weights, attn_implementation="sdpa", device_map={"": 0}, **dtype_kwarg(torch.bfloat16)
)
model = PeftModel.from_pretrained(base_model, adapter_dir)
model = model.merge_and_unload()
model.eval()
processor = AutoProcessor.from_pretrained(weights, min_pixels=256 * px, max_pixels=1024 * px)

splits = [
    ("dev300", Path(os.environ["NCS_DATA"]) / "datasets" / "ktvic_dev", "dev_data.json", 300),
    ("test", Path(os.environ["NCS_DATA"]) / "datasets" / "ktvic", "test_data.json", 558),
]

for split_tag, ds_dir, split_json, expected_n in splits:
    data = json.loads((ds_dir / split_json).read_text(encoding="utf-8"))
    names = {str(img.get("id", img.get("image_id"))): img.get("file_name") or img.get("filename")
             for img in data["images"]}
    image_ids = sorted(names.keys(), key=lambda x: int(x) if x.isdigit() else x)
    assert len(image_ids) == expected_n, (split_tag, len(image_ids), expected_n)
    for mode, max_new in (("short", 60), ("detailed", 160)):
        t0 = time.time()
        preds: dict[str, str] = {}
        prompt = ev.PROMPTS[mode]
        for iid in image_ids:
            image = Image.open(ds_dir / "images" / names[iid]).convert("RGB")
            messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": prompt}]}]
            text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = processor(text=[text], images=[image], return_tensors="pt").to(model.device)
            with torch.no_grad():
                ids = model.generate(**inputs, max_new_tokens=max_new, do_sample=False)
            preds[iid] = processor.batch_decode(
                ids[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True
            )[0].strip()
        elapsed = time.time() - t0
        stem = f"b1_qwen3vl_p1_nodev_s42-{split_tag}-{mode}" if split_tag == "dev300" else f"b1_qwen3vl_p1_nodev_s42-{mode}"
        pred_path = out_path / f"{stem}.preds.json"
        pred_path.write_text(json.dumps(preds, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        meta_path = out_path / f"{stem}.decode_meta.json"
        meta_path.write_text(json.dumps({
            "machine_id": machine_id,
            "run_id": "b1_qwen3vl_p1_nodev_s42",
            "split": split_tag,
            "prompt_style": mode,
            "n_images": len(preds),
            "elapsed_sec": round(elapsed, 3),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY

# 5. CPU scoring via evaluate.py (in /root/vsps/.venv for RDRSegmenter/JVM) + dual-matcher (v1 & v2) frontier verdict.
/root/vsps/.venv/bin/python - "$O" "$MACHINE_ID" "$PREREG_JSON" <<'PY'
import json
import os
import subprocess
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, "/root/vsps")
sys.path.insert(0, "/root/vsps/scripts")
import object_prf as op
import prereg_ladder_check as plc
from abs_halluc import CJK
from rescap.vlm.mock import looks_vietnamese
from s0_screen import norm_tone

out_dir, machine_id, prereg_path = sys.argv[1:4]
out_path = Path(out_dir)
prereg = json.loads(Path(prereg_path).read_text(encoding="utf-8"))
fr = prereg["frozen_frontier_predictions"]["frontier_anchors"]

def run_eval(preds_file: Path, split_json: str, dataset_env: str, mode: str, name: str, out_json: Path):
    env = dict(os.environ, NCS_DATASET=dataset_env, RESCAP_RAW_TONE="1")
    subprocess.run(
        [
            "/root/vsps/.venv/bin/python", "scripts/evaluate.py",
            "--predictions", str(preds_file),
            "--split", split_json,
            "--prompt", mode,
            "--name", name,
            "--out", str(out_json),
        ],
        check=True,
        env=env,
    )
    payload = json.loads(out_json.read_text(encoding="utf-8"))
    payload["machine_id"] = machine_id
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload

def dual_matcher_scores(preds: dict[str, str], refs: dict[str, list[str]]) -> dict:
    os.environ["RESCAP_RAW_TONE"] = "1"
    gold_v1 = {i: set().union(*(op.objects_in(unicodedata.normalize("NFC", r)) for r in rs)) for i, rs in refs.items()}
    cnt_v1 = op.image_counts(preds, gold_v1)
    sc_v1 = op.scores(cnt_v1)
    m_v1 = sc_v1["mentions_per_caption"]
    p0_v1, r0_v1, f10_v1 = plc.at(fr, m_v1)
    tp0_v1 = fr["TP1"] * (m_v1 / fr["M1"]) ** fr["b"]
    pred_at_m_v1 = {"TP": round(tp0_v1, 4), "P": round(p0_v1, 4), "R": round(r0_v1, 4), "F1": round(f10_v1, 4)}
    res_p_v1 = sc_v1["P"] - p0_v1
    res_r_v1 = sc_v1["R"] - r0_v1
    res_f1_v1 = sc_v1["F1"] - f10_v1

    os.environ["RESCAP_RAW_TONE"] = "0"
    gold_v2 = {i: set().union(*(op.objects_in(norm_tone(r)) for r in rs)) for i, rs in refs.items()}
    preds_v2 = {k: norm_tone(v) for k, v in preds.items()}
    cnt_v2 = op.image_counts(preds_v2, gold_v2)
    sc_v2 = op.scores(cnt_v2)
    m_v2 = sc_v2["mentions_per_caption"]
    p0_v2, r0_v2, f10_v2 = plc.at(fr, m_v2)
    tp0_v2 = fr["TP1"] * (m_v2 / fr["M1"]) ** fr["b"]
    pred_at_m_v2 = {"TP": round(tp0_v2, 4), "P": round(p0_v2, 4), "R": round(r0_v2, 4), "F1": round(f10_v2, 4)}
    res_p_v2 = sc_v2["P"] - p0_v2
    res_r_v2 = sc_v2["R"] - r0_v2
    res_f1_v2 = sc_v2["F1"] - f10_v2

    vi_share = sum(1 for c in preds.values() if looks_vietnamese(c)) / len(preds)
    cjk_rate = sum(1 for c in preds.values() if CJK.search(c)) / len(preds)
    return {
        "n_images": len(preds),
        "vietnamese_share": round(vi_share, 6),
        "cjk_rate": round(cjk_rate, 6),
        "matcher_v1": {
            "observed": sc_v1,
            "frontier_predicted_at_M": pred_at_m_v1,
            "delta_P_front_pp": round(res_p_v1, 4),
            "delta_R_front_pp": round(res_r_v1, 4),
            "delta_F1_front_pp": round(res_f1_v1, 4),
        },
        "matcher_v2": {
            "observed": sc_v2,
            "frontier_predicted_at_M": pred_at_m_v2,
            "delta_P_front_pp": round(res_p_v2, 4),
            "delta_R_front_pp": round(res_r_v2, 4),
            "delta_F1_front_pp": round(res_f1_v2, 4),
        },
    }

def load_refs(ds_dir: Path, split_json: str) -> dict[str, list[str]]:
    data = json.loads((ds_dir / split_json).read_text(encoding="utf-8"))
    refs: dict[str, list[str]] = {}
    for ann in data["annotations"]:
        if ann.get("caption"):
            refs.setdefault(str(ann["image_id"]), []).append(ann["caption"])
    return refs

ncs = Path(os.environ["NCS_DATA"])
refs_dev = load_refs(ncs / "datasets" / "ktvic_dev", "dev_data.json")
refs_test = load_refs(ncs / "datasets" / "ktvic", "test_data.json")

results = {"machine_id": machine_id, "run_id": "b1_qwen3vl_p1_nodev_s42", "splits": {"dev300": {}, "test": {}}}
for mode in ("short", "detailed"):
    dev_stem = f"b1_qwen3vl_p1_nodev_s42-dev300-{mode}"
    dev_preds_p = out_path / f"{dev_stem}.preds.json"
    dev_eval_p = out_path / f"{dev_stem}.json"
    dev_ev = run_eval(dev_preds_p, "dev_data.json", "ktvic_dev", mode, dev_stem, dev_eval_p)
    dev_preds = json.loads(dev_preds_p.read_text(encoding="utf-8"))
    results["splits"]["dev300"][mode] = {
        "evaluate_metrics": dev_ev.get("metrics", {}),
        **dual_matcher_scores(dev_preds, refs_dev),
    }

    test_stem = f"b1_qwen3vl_p1_nodev_s42-{mode}"
    test_preds_p = out_path / f"{test_stem}.preds.json"
    test_eval_p = out_path / f"{test_stem}.json"
    test_ev = run_eval(test_preds_p, "test_data.json", "ktvic", mode, test_stem, test_eval_p)
    test_preds = json.loads(test_preds_p.read_text(encoding="utf-8"))
    results["splits"]["test"][mode] = {
        "evaluate_metrics": test_ev.get("metrics", {}),
        **dual_matcher_scores(test_preds, refs_test),
    }

short_test_v1 = results["splits"]["test"]["short"]["matcher_v1"]
abs_dp = abs(short_test_v1["delta_P_front_pp"])
results["primary_endpoint_pd2"] = {
    "split": "test",
    "mode": "short",
    "M_B1_v1": round(short_test_v1["observed"]["mentions_per_caption"], 4),
    "P_B1_v1": round(short_test_v1["observed"]["P"], 4),
    "P0_hat_at_M_B1_v1": round(short_test_v1["frontier_predicted_at_M"]["P"], 4),
    "delta_P_front_v1_pp": short_test_v1["delta_P_front_pp"],
    "delta_P_front_v2_pp": results["splits"]["test"]["short"]["matcher_v2"]["delta_P_front_pp"],
    "outcome_branch": (
        "Outcome_A_cross_backbone_invariance_holds"
        if abs_dp <= 2.0
        else "Outcome_B_backbone_intercept_shift"
    ),
}

verdict_path = out_path / "step2_b1_gate_verdict.json"
verdict_path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote B1 gate verdict -> {verdict_path}")
PY
