cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
set -e
# Judge D10 (iv)(c) + User decision U-001: KTVIC 2,048-vision-token resolution control (~1 GPU-h, low priority).
# 1. Decision run: p1dev_s42 on KTVIC dev300 (dev_data.json, 300 images) at --max-vision-tokens 2048 vs existing 512 run.
#    Re-open the resolution lever only if dev300 dR >= +2.0 percentage points.
# 2. Report-only controls: p1assist_s42 and fuse2_s42 on KTVIC test (558 images) at --max-vision-tokens 2048 in short and detailed modes.
#    Main tables stay at 512 whatever the result.

echo "a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236  scripts/evaluate.py" | sha256sum -c -
echo "6b711280d70b780d596414896d832738da58f1b079015dee888605d1ba350adc  scripts/object_prf.py" | sha256sum -c -
echo "227a3312a18cf69b355c20311ff1228167b2af1436e0cb443055dfdfcd40c5c3  $NCS_DATA/runs/p1dev_s42/adapter_model.safetensors" | sha256sum -c -
echo "4efbb4e4bc6bf255369e3166f255cd8fe70ffe754eeefa8ff9e34a162d475a36  $NCS_DATA/runs/p1assist_s42/adapter_model.safetensors" | sha256sum -c -
echo "4dd674ab85ca2bb957594460cde28916ce6c643bf3e08a8e6d7489ccd643d857  $NCS_DATA/runs/fuse2_s42/adapter_model.safetensors" | sha256sum -c -
echo "1e183383e91daf32f4683fbea2bdb09d24b7deba956343ca16ef332014cba84b  $NCS_DATA/rl/p1dev_s42-dev300-short.preds.json" | sha256sum -c -
grep -q "$(sha256sum manuscript/prereg/2026-10-13_ktvic_res2048_jobs/60_ktvic_res2048.sh | cut -c1-64)" manuscript/prereg/2026-10-13_ktvic_res2048.md

O=$NCS_DATA/results/res2048; mkdir -p $O

# 1. dev300 decision run (p1dev_s42, short mode, --max-vision-tokens 2048)
python scripts/ktvic_dev_split.py --verify --json-dir $NCS_DATA/datasets/ktvic_dev
[ -s $O/p1dev_s42_vt2048-dev300-short.json ] || NCS_DATASET=ktvic_dev timeout 3600 python scripts/evaluate.py \
  --model qwen2.5-vl-7b --adapter $NCS_DATA/runs/p1dev_s42 --split dev_data.json --prompt short \
  --max-vision-tokens 2048 --name p1dev_s42_vt2048-dev300-short --out $O/p1dev_s42_vt2048-dev300-short.json

# 2. KTVIC test report-only controls (p1assist_s42 and fuse2_s42, short and detailed modes, --max-vision-tokens 2048)
unset NCS_DATASET
for m in p1assist_s42 fuse2_s42; do
  for p in short detailed; do
    [ -s $O/${m}_vt2048-${p}.json ] || timeout 5400 python scripts/evaluate.py \
      --model qwen2.5-vl-7b --adapter $NCS_DATA/runs/$m --split test_data.json --prompt $p \
      --max-vision-tokens 2048 --name ${m}_vt2048-${p} --out $O/${m}_vt2048-${p}.json
  done
done

# 3. Paired comparison (2048 vs 512) and decision rule evaluation
python - <<'PY'
import json, os, sys
from pathlib import Path

sys.path.insert(0, "scripts")
import object_prf as op
from evaluate import references
from rescap.chair import _ancestors, objects_in

ncs = Path(os.environ["NCS_DATA"])
res_dir = ncs / "results" / "res2048"

def eval_ktvic_pair(split_name, dataset_env, pred_512_path, json_512_path, pred_2048_path, json_2048_path):
    if dataset_env:
        os.environ["NCS_DATASET"] = dataset_env
    else:
        os.environ.pop("NCS_DATASET", None)
    # Reload evaluate.KTVIC via direct path
    ktvic_dir = ncs / "datasets" / (dataset_env or "ktvic")
    data = json.loads((ktvic_dir / split_name).read_text(encoding="utf-8"))
    refs = {}
    for ann in data.get("annotations", []):
        if ann.get("caption"):
            refs.setdefault(str(ann["image_id"]), []).append(ann["caption"])
    gold = {str(k): set().union(*[set(objects_in(r)) for r in rs]) for k, rs in refs.items()}
    p512 = op._preds(pred_512_path)
    p2048 = op._preds(pred_2048_path)
    ids = sorted(gold.keys())
    assert set(p512.keys()) == set(ids) and set(p2048.keys()) == set(ids)
    r512 = [op.image_counts(set(objects_in(p512[i])), gold[i], _ancestors) for i in ids]
    r2048 = [op.image_counts(set(objects_in(p2048[i])), gold[i], _ancestors) for i in ids]
    s512, s2048 = op.scores(r512), op.scores(r2048)
    d = op.paired(r512, r2048, keys=("P", "R", "F1", "P_h", "R_spec", "F1_spec"))
    j512 = json.loads(json_512_path.read_text(encoding="utf-8"))
    j2048 = json.loads(json_2048_path.read_text(encoding="utf-8"))
    c512 = next(r["scores_scaled_x100"]["CIDEr"] for r in j512["results"] if r["tokenization"] == "word-level")
    c2048 = next(r["scores_scaled_x100"]["CIDEr"] for r in j2048["results"] if r["tokenization"] == "word-level")
    return {
        "n_images": len(ids),
        "vt512": {"object_prf": s512, "cider": c512, "chair": j512["chair"]},
        "vt2048": {"object_prf": s2048, "cider": c2048, "chair": j2048["chair"]},
        "delta_2048_minus_512": {k: {"point": pt, "ci95": [lo, hi], "p": p} for k, (pt, lo, hi, p) in d.items()},
        "delta_cider": c2048 - c512,
    }

dev_res = eval_ktvic_pair(
    "dev_data.json", "ktvic_dev",
    ncs / "rl" / "p1dev_s42-dev300-short.preds.json",
    ncs / "rl" / "p1dev_s42-dev300-short.json",
    res_dir / "p1dev_s42_vt2048-dev300-short.preds.json",
    res_dir / "p1dev_s42_vt2048-dev300-short.json",
)
test_controls = {}
for m in ("p1assist_s42", "fuse2_s42"):
    for p in ("short", "detailed"):
        test_controls[f"{m}-{p}"] = eval_ktvic_pair(
            "test_data.json", None,
            ncs / "results" / f"{m}-{p}.preds.json",
            ncs / "results" / f"{m}-{p}.json",
            res_dir / f"{m}_vt2048-{p}.preds.json",
            res_dir / f"{m}_vt2048-{p}.json",
        )

dr_dev = dev_res["delta_2048_minus_512"]["R"]["point"]
out = {
    "dev300_p1dev_s42_short": dev_res,
    "reopen_resolution_lever": bool(dr_dev >= 2.0),
    "rule": "Re-open resolution lever only if p1dev_s42 dev300 dR (2048 minus 512) >= +2.0 percentage points (D10 (iv)(c)). Main tables stay at 512.",
    "ktvic_test_controls": test_controls,
}
(res_dir / "ktvic_res2048_summary.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, indent=2))
PY
