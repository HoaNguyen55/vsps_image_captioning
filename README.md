# VSPS — Verified Structured Proposition Synthesis for Vietnamese Image Captioning

Code and data accompanying the paper *"A Method for Reducing Hallucinations in Detailed
Vietnamese Image Captioning Using Supervision from Verified Propositions"* (FAIR 2026).

VSPS reduces object hallucination by verifying typed visual propositions **during
training-data construction**: propositions are generated from each training image,
verified into three states (SUPPORTED / UNCERTAIN / REJECTED), neutralized or excluded
when under-evidenced, and rendered into supervision for QLoRA SFT. The deployed model
generates captions in a **single pass** — no verifier, retrieval, or post-editing at
inference time.

The whole pipeline is reproducible **step by step**: each step below is one standalone
shell command whose printed numbers can be checked against the tables in the paper.

## 0. Hardware requirements

| Step | GPU | Notes |
|---|---|---|
| Smoke test, scoring, figures | none | CPU-only |
| Inference (Phase 2), latency | 1× 24 GB (RTX 3090/4090) | 4-bit NF4 |
| Fine-tuning (Phase 1b) | 1× 24 GB | QLoRA r=16 |
| Regenerating Phase-1a records | 1× 24 GB, ~30 h | **shipped** in `data/stage1_records/` — can be skipped |

## 1. Environment

Requires **Python 3.10–3.12** (with the `venv` module), a JDK (for VnCoreNLP), and
`git`. `setup.sh` refuses newer Pythons: the pinned torch-cu121 wheel line stops at
Python 3.12.

```bash
bash setup.sh          # venv + torch cu121 + pinned transformers==4.51.3 + VnCoreNLP
source .venv/bin/activate && export NCS_DATA=$PWD/ncs-data
bash get_data.sh       # KTVIC images + annotations (see notes inside the script)
python scripts/smoke_test.py   # PASS 4/4 = environment is correct (no GPU needed)
```

Two pins are **mandatory**: `transformers==4.51.3` and `trl==0.19.1`. Newer releases
change how Qwen2.5-VL handles `cache_position`/M-RoPE and change the trainer signature;
the adapter still loads but inference goes wrong *silently*.
`scripts/verify_environment.py` checks everything before any long run.

## 2. Layout

```
rescap/            core library
  pipeline/generate.py   proposition generation (typed, atomic) from an image
  pipeline/verify.py     dual-query verification, K = 5 repeated decoding runs, 3 states + lower-only ceilings
  pipeline/select.py     budgeted redundancy-aware selection (default budget 9)
  pipeline/realize.py    rendering: template path / constrained-LM path
  chair.py               CHAIR-vi (object matching over VnCoreNLP word segmentation)
scripts/           every experiment in the paper — one file per experiment
data/
  stage1_records/  3,700 verified Phase-1a records, one per training image (27 MB packed)
  supervision/     pre-built supervision store (sft.jsonl) — ready to train on
  coco_probe/      COCO manifests + the frozen Vietnamese→COCO object dictionary
  annotations/     human audit of the verifier: the 244-proposition machine-Supported sample
                   (audit_supported_sample.json) and its verdicts (audit/tn.json); the round-2
                   sample (audit_round2_sample.json) and the 12 verdicts collected so far (audit/tn_dot2.json)
  results/         raw numbers behind every table in the paper, including the test-split
                   predictions of the main system (main_s42/s43/s44-*.preds.json), the three
                   controlled variants (vsps_base/clean/neutral-detailed.preds.json), VCD, and
                   the untrained pipeline (vsps-*.preds.json); the full 5,000-image COCO-2014
                   Karpathy-test predictions (coco5000/: zero-shot + VSPS, coco5000_vcd/: VCD)
                   with their CHAIR scores (coco5000_scores*.json)
  screening/, stress50/, vram/   auxiliary experiment data
```

## 3. Reproduction, phase by phase

### Phase 1a — generate + verify propositions (optional, ~30 GPU-hours; results shipped)

```bash
tar -xzf data/stage1_records/stage1_records.tar.gz -C $NCS_DATA   # shipped records -> $NCS_DATA/stage1
# OR regenerate them from scratch:
# python scripts/generate_stage1.py --source train_data.json --out $NCS_DATA/stage1   # generation + dual-query verification + ceilings
python scripts/person_uncap.py --in $NCS_DATA/stage1 --out $NCS_DATA/stage1_final   # offline neutralization (un-capping)
```

`generate_stage1.py` runs steps (1)–(2) of the paper's Fig. 2 and stores the evidence
record of every proposition. The shipped records are the output of this step, i.e.
**before** neutralization (461 images without any SUPPORTED proposition), so
`person_uncap.py` must be run on them too. `person_uncap.py` is step (3), the main system's
neutralization: it recovers UNCERTAIN person propositions **offline from the stored
evidence** (τ = 0.9, no model call; recovers 11,769 propositions on 2,351 images and
leaves 83 images without any SUPPORTED proposition — printed at the end of the run).
Relation propositions are never neutralized; `relation_audit.py` measures how many
SUPPORTED relations still reach the detailed supervision (2.0% of selected propositions,
`data/results/relation_audit.json`):

```bash
python scripts/relation_audit.py --in $NCS_DATA/stage1_final
``` `person_backoff.py` is the alternative that re-queries
the verifier with the neutral noun; it was explored but is not part of the main system.

### Phase 1b — build supervision + fine-tune (QLoRA, ~2 h per run on an RTX 4090)

```bash
# step (4): selection (budget 9) + template rendering; variant B = uncertain content excluded
python scripts/build_dpo_data.py --in $NCS_DATA/stage1_final --out $NCS_DATA/supervision \
    --budget 9 --detailed-variant B --style-variation --clean-props   # writes sft.jsonl (and dpo.jsonl)
# or use the shipped store data/supervision/sft.jsonl directly (it also contains the 650
# constrained-LM detailed examples, rendered with the constrained_lm path of
# rescap/pipeline/realize.py as in scripts/constrained_lm_pilot.py)
python scripts/train_stage2.py --stage sft --data data/supervision --out $NCS_DATA/runs/sft \
    --epochs 2 --seed 42
# controls: --no-4bit (bf16 LoRA, no quantization) or --use-8bit
```

The main system of the paper is **SFT-only** (7,177 examples: 3,617 short + 3,560
detailed, two modes sharing one adapter; seeds 42/43/44). The shipped store has been
verified record by record: no empty responses, the 3,560 detailed examples split into
2,910 template-rendered + 650 constrained-LM-rendered (the `renderer` field), and all
3,617 images belong to the KTVIC train split — the 558-image test split never
contributes supervision.

### Phase 2 — single-pass inference + scoring (558-image KTVIC test split)

```bash
python scripts/evaluate.py --model qwen2.5-vl-7b --adapter $NCS_DATA/runs/sft \
    --prompt detailed --name main_s42-detailed      # also --prompt short
python scripts/score_ci.py --a data/results/zeroshot-detailed.preds.json --name-a zero-shot \
    --b data/results/main_s42-detailed.preds.json --name-b VSPS      # paired bootstrap, 5,000 rounds, seed 42
```

Expected numbers (main system, seed 42 — the paper's main tables): hallucinated
objects/caption **1.57** · CHAIR_s **79.2** · CHAIR_i **50.1** · objects mentioned/caption
**3.13** · short-mode CIDEr **17.3** · unsupported gender attribution **4.1%**.
Across seeds 42/43/44: 1.55 ± 0.04 · CHAIR_s 78.3 ± 0.9 · CHAIR_i 49.7 ± 0.4.
Zero-shot on the same backbone: 4.26 hallucinated objects/caption, CHAIR_s 98.0%.
Template-only variant (VSPS-Base): 1.15 hallucinated objects · CHAIR_s 70.4%.

Object precision / recall / F1 over unique classes per image (Table IV of the paper) are
reproduced from the shipped predictions with one command:

```bash
python scripts/object_prf.py                                   # KTVIC block
python scripts/object_prf.py --coco-preds data/results/coco5000        # + COCO block
```

Expected (KTVIC, detailed mode): zero-shot 31.6 / 57.1 / 40.7 · VCD 31.9 / 55.9 / 40.6 ·
P1 78.3 / 42.7 / 55.3 · P2 39.0 / 42.0 / 40.4 · Untrained VSPS 42.9 / 37.2 / 39.8 ·
VSPS-Base 39.1 / 23.3 / 29.2 · VSPS-Clean 38.6 / 23.9 / 29.5 · VSPS-Neutral 39.9 / 37.7 / 38.8 ·
VSPS seed 42 41.5 / 36.7 / 39.0 (three seeds 41.9 ± 0.5 / 37.1 ± 0.3 / 39.3 ± 0.4).
COCO-2014: zero-shot 80.5 / 63.3 / 70.9 · VSPS 88.2 / 45.9 / 60.4.

### Satellite experiments

```bash
python scripts/coco_probe.py --manifest data/coco_probe/manifest_full5000.json  # out-of-domain COCO
python scripts/score_coco_probe.py --preds-dir data/results/coco5000 \
    --manifest data/coco_probe/manifest_full5000.json --out data/results/coco5000_scores.json
                                       # expected: 0.45 → 0.17 halluc./caption (−63%), CHAIR_s 34.4% → 15.4%
python scripts/score_coco_probe.py --preds-dir data/results/coco5000_vcd \
    --manifest data/coco_probe/manifest_full5000.json --out data/results/coco5000_scores_vcd.json
                                       # expected (VCD, detailed): 0.38 halluc./caption, CHAIR_s 31.5%
python scripts/baselines.py --method vcd            # VCD baseline (CVPR'24), same backbone
python scripts/baselines.py --method selfcorrect    # Self-Correction baseline
python scripts/run_ablations.py --in $NCS_DATA/stage1   # verification ablations replayed from the stored probes
python scripts/measure_latency.py --adapter $NCS_DATA/runs/sft \
    --out latency.json                             # median 0.81 s (short) / 1.88 s (detailed) on RTX 4090
python scripts/stress50_analysis.py \
    --manifest data/stress50/stress50_manifest.json \
    --preds "zeroshot=data/results/zeroshot-detailed.preds.json" \
            "vsps=data/results/vsps-detailed.preds.json" \
    --out stress50_report.json                     # 50-image challenge set (gender/count/colour)
python scripts/agreement.py                        # Cohen's kappa (needs the annotation files, available on request)
```

The paper's COCO numbers are the full 5,000-image Karpathy test split
(`manifest_full5000.json`; predictions in `data/results/coco5000*/`, scores in
`data/results/coco5000_scores*.json`). The older `data/results/coco_*scores*.json` files
cover only the first 2,500-image half (`data/coco_probe/manifest.json`).

### Human rating of caption quality

```bash
python scripts/human_eval_sample.py      # 50 test images x (zero-shot, P2, VSPS): blinded rating_sheet.xlsx + key.json
# two annotators fill in copies of rating_sheet.xlsx (1-5: faithfulness, completeness, fluency)
python scripts/human_eval_score.py --key data/human_eval/key.json \
    --sheets rater_A.xlsx rater_B.xlsx --out data/results/human_eval.json
```

### Optional: preference-tuning exploration (negative result)

`scripts/build_dpo_data.py` (`dpo.jsonl`, 12,806 pairs) and `train_stage2.py --stage dpo --adapter <sft adapter>` reproduce the
preference-tuning experiments reported as a controlled negative result: on the 4-bit
backbone, every tested dose degraded CIDEr and leaked non-Vietnamese tokens. They are
not part of the main system.

### Figures

```bash
python scripts/plot_results.py && python scripts/plot_training.py && \
python scripts/plot_qualitative.py && python scripts/plot_phases.py
```

## 4. Number-to-file traceability

Every number in the paper traces back to a file in `data/results/`. Two independent
checks, both CPU-only and both runnable straight from this repository:

```bash
# Re-score every shipped prediction file from scratch and compare with the shipped
# summary — verified to reproduce data/results/abs_halluc_summary.json bit-for-bit:
python scripts/abs_halluc.py --results data/results --out abs_halluc_check.json

# Replay the verification rule engine over the shipped Phase-1a records
# (default --limit 50; pass --limit 3700 for the full set, ~10 min on CPU):
python scripts/validate_replay.py --in $NCS_DATA/stage1 --limit 3700
```

Known property of the replay harness: on the full 3,700 records the stored probe
samples reproduce 100.0% (381,182/381,182), while verdict reproduction is 98.3%;
the discrepancies concentrate on UNCERTAIN-adjacent, near-boundary cases
(REJECTED→SUPPORTED flips: 1 in 192,216). The harness therefore refuses (99% gate)
to let replay-derived numbers be quoted. All numbers in the paper come from the
stored verdicts and real model runs, not from the replay harness.

## 5. License & contact

Code: MIT (see `LICENSE`). KTVIC and COCO images are distributed under their own
original licenses and are not included here. Contact: see the author addresses in the
paper.
