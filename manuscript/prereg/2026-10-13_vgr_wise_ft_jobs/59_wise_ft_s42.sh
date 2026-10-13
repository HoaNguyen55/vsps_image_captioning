cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -e
# Judge D10 (iii) + User decision U-001: VGR Step 0 (WiSE-FT weight-space interpolation on fuse2_s42 at alpha in {0.5, 0.75}).
# Because fuse2_s42 is a LoRA adapter with r=16, lora_alpha=32, bias="none", and modules_to_save=null,
# W(alpha) = W_0 + alpha * (lora_alpha_0 / r) * B * A is exact when lora_alpha is set to alpha * 32 (16 for 0.5, 24 for 0.75),
# requiring zero edits to frozen scripts/evaluate.py.

echo "a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236  scripts/evaluate.py" | sha256sum -c -
echo "6b711280d70b780d596414896d832738da58f1b079015dee888605d1ba350adc  scripts/object_prf.py" | sha256sum -c -
echo "278d15b97e3eeb9496a0282bb91deb365117becf24d174fbb1e0507203b12ea4  data/uitviic/instance_gold.json" | sha256sum -c -
echo "4dd674ab85ca2bb957594460cde28916ce6c643bf3e08a8e6d7489ccd643d857  $NCS_DATA/runs/fuse2_s42/adapter_model.safetensors" | sha256sum -c -
echo "93f042284aea64fcdf831590c592a7459849632dcb3ee4448b379177b7a298c5  $NCS_DATA/runs/fuse2_s42/adapter_config.json" | sha256sum -c -
grep -q "$(sha256sum manuscript/prereg/2026-10-13_vgr_wise_ft_jobs/59_wise_ft_s42.sh | cut -c1-64)" manuscript/prereg/2026-10-13_vgr_wise_ft.md

python - <<'PY'
import json, os
from pathlib import Path

runs = Path(os.environ["NCS_DATA"]) / "runs"
base_dir = runs / "fuse2_s42"
cfg0 = json.loads((base_dir / "adapter_config.json").read_text(encoding="utf-8"))
assert cfg0["r"] == 16 and cfg0["lora_alpha"] == 32 and cfg0["bias"] == "none" and cfg0["modules_to_save"] is None

for tag, alpha, lora_alpha in (("fuse2_s42_wise05", 0.5, 16), ("fuse2_s42_wise075", 0.75, 24)):
    d = runs / tag
    d.mkdir(parents=True, exist_ok=True)
    sf = d / "adapter_model.safetensors"
    if sf.exists() or sf.is_symlink():
        sf.unlink()
    sf.symlink_to(base_dir / "adapter_model.safetensors")
    cfg = dict(cfg0)
    cfg["lora_alpha"] = lora_alpha
    (d / "adapter_config.json").write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    assert cfg["lora_alpha"] / cfg["r"] == alpha * (cfg0["lora_alpha"] / cfg0["r"])
    print(f"Prepared {tag}: alpha={alpha}, lora_alpha={lora_alpha}, r={cfg['r']}")
PY

# 1. Dev selection split: UIT-ViIC val (924 COCO-2014 images, short mode).
export NCS_DATASET=uitviic
python -c "import sys; sys.path.insert(0, 'scripts'); from evaluate import references; n = len(references('val_data.json')); assert n == 924, n"
OV=$NCS_DATA/results/uitviic_val; mkdir -p $OV
for m in fuse2_s42 fuse2_s42_wise075 fuse2_s42_wise05; do
  [ -s $OV/uitviic_val_${m}-short.json ] || timeout 5400 python scripts/evaluate.py --model qwen2.5-vl-7b \
    --adapter $NCS_DATA/runs/$m --split val_data.json --prompt short \
    --name uitviic_val_${m}-short --out $OV/uitviic_val_${m}-short.json
done
python scripts/object_prf.py --results $OV --split val_data.json --mode short \
  --instance-gold data/uitviic/instance_gold.json --vs uitviic_val_fuse2_s42 | tee $OV/object_prf-short.txt

# 2. KTVIC test (558 images, short and detailed modes) for CIDEr-D guard (>= 140.7) and in-domain retention.
unset NCS_DATASET
python -c "import sys; sys.path.insert(0, 'scripts'); from evaluate import references; n = len(references('test_data.json')); assert n == 558, n"
for m in fuse2_s42_wise075 fuse2_s42_wise05; do
  for p in short detailed; do
    [ -s $NCS_DATA/results/${m}-${p}.json ] || timeout 5400 python scripts/evaluate.py --model qwen2.5-vl-7b \
      --adapter $NCS_DATA/runs/$m --split test_data.json --prompt $p \
      --name ${m}-${p} --out $NCS_DATA/results/${m}-${p}.json
  done
done

# 3. Compute the pre-registered VGR Step-0 decision and futility gate (D10 (iii)).
python - <<'PY'
import json, os, sys
from pathlib import Path

sys.path.insert(0, "scripts")
import object_prf as op
import score_coco_probe as sc
from evaluate import references

ncs = Path(os.environ["NCS_DATA"])
ov = ncs / "results" / "uitviic_val"
vi_terms = sc.load_vi_terms()
inst = json.loads(Path("data/uitviic/instance_gold.json").read_text(encoding="utf-8"))
os.environ["NCS_DATASET"] = "uitviic"
refs_val = references("val_data.json")
gold_inst_only = {k: set(inst[k]["coco"]) for k in refs_val}
gold_inst_ref = {k: set(inst[k]["coco"]).union(*[sc.vi_objects(r, vi_terms) for r in rs]) for k, rs in refs_val.items()}

def eval_val(tag, gold_map):
    preds = op._preds(ov / f"uitviic_val_{tag}-short.preds.json")
    rows = {k: op.image_counts(sc.vi_objects(cap, vi_terms), gold_map.get(k, set()), lambda c: {c}) for k, cap in preds.items()}
    return rows, op.scores(list(rows.values()))

def ktvic_cider(tag):
    d = json.loads((ncs / "results" / f"{tag}-short.json").read_text(encoding="utf-8"))
    for r in d["results"]:
        if r["tokenization"] == "word-level":
            return float(r["scores_scaled_x100"]["CIDEr"])
    raise RuntimeError(f"missing word-level CIDEr in {tag}")

base_rows_io, base_s_io = eval_val("fuse2_s42", gold_inst_only)
base_rows_ir, base_s_ir = eval_val("fuse2_s42", gold_inst_ref)
ids = sorted(base_rows_io.keys())

candidates = {}
for tag, alpha in (("fuse2_s42_wise075", 0.75), ("fuse2_s42_wise05", 0.5)):
    r_io, s_io = eval_val(tag, gold_inst_only)
    r_ir, s_ir = eval_val(tag, gold_inst_ref)
    d_io = op.paired([base_rows_io[i] for i in ids], [r_io[i] for i in ids])
    d_ir = op.paired([base_rows_ir[i] for i in ids], [r_ir[i] for i in ids])
    cider = ktvic_cider(tag)
    candidates[str(alpha)] = {
        "adapter": tag,
        "alpha": alpha,
        "uitviic_val_instances_only": s_io,
        "uitviic_val_instances_plus_refs": s_ir,
        "delta_vs_fuse2_instances_only": {k: {"point": pt, "ci95": [lo, hi], "p": p} for k, (pt, lo, hi, p) in d_io.items()},
        "delta_vs_fuse2_instances_plus_refs": {k: {"point": pt, "ci95": [lo, hi], "p": p} for k, (pt, lo, hi, p) in d_ir.items()},
        "ktvic_test_short_cider": cider,
        "ktvic_cider_guard_pass": cider >= 140.7,
    }

# Alpha selection on UIT-ViIC val: pick alpha in {0.5, 0.75} with highest instance-only F1 on UIT-ViIC val
# (preferring KTVIC CIDEr >= 140.7 if any passes; ties broken toward 0.75).
passing = [v for v in candidates.values() if v["ktvic_cider_guard_pass"]]
pool = passing if passing else list(candidates.values())
chosen = max(pool, key=lambda v: (round(v["uitviic_val_instances_only"]["F1"], 4), v["alpha"]))
df1_io = chosen["delta_vs_fuse2_instances_only"]["F1"]["point"]
df1_ir = chosen["delta_vs_fuse2_instances_plus_refs"]["F1"]["point"]
futile = bool(chosen["ktvic_cider_guard_pass"] and (df1_io >= 3.5 or df1_ir >= 3.5))

out = {
    "baseline_fuse2_s42": {
        "uitviic_val_instances_only": base_s_io,
        "uitviic_val_instances_plus_refs": base_s_ir,
        "ktvic_test_short_cider": ktvic_cider("fuse2_s42"),
    },
    "candidates": candidates,
    "chosen_alpha": chosen["alpha"],
    "chosen_adapter": chosen["adapter"],
    "futile_for_vgr_sft": futile,
    "rule": "Skip VGR SFT if dev-chosen WiSE point gains >= +3.5 short instance F1 over fuse2_s42 on UIT-ViIC val at KTVIC short CIDEr >= 140.7 (D10 (iii)).",
}
gate_path = ncs / "results" / "wise_ft_gate.json"
gate_path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, indent=2))
PY
