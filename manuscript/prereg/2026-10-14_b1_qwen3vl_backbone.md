# Pre-Registration: `B1` Second Backbone (`Qwen/Qwen3-VL-8B-Instruct`) on the Count-Driven Precision-Recall Frontier

- **Preregistration ID**: `2026-10-14_b1_qwen3vl_backbone`
- **Status**: `frozen_2026-10-14_before_any_B1_ktvic_output_exists`
- **Companion Machine-Readable Predictions**: `manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json`
- **Staged Job Script**: `manuscript/prereg/2026-10-14_b1_jobs/61_b1_qwen3vl_guard_and_gate.sh`
- **Authority**: Judge decisions `PD-5 Q1`, `PD-5 Q2`, `PD-2`, and `D17`.

---

## 1. Scientific Objective & Scope

This document pre-registers the **second-backbone (`B1`) experiment** transferring our primary `P1` supervision recipe from `Qwen/Qwen2.5-VL-7B-Instruct` to `Qwen/Qwen3-VL-8B-Instruct` (Apache-2.0 licence) **before any `B1` KTVIC output exists**.

Specifically, we test whether the count-driven precision-recall frontier $\hat{P}_0(M), \hat{R}_0(M)$ established on `Qwen/Qwen2.5-VL-7B-Instruct` (`manuscript/prereg/2026-10-12_ladder_predictions.json`) predicts the object precision and recall of `Qwen/Qwen3-VL-8B-Instruct` at its own generated mention count $M_{\text{B1}}$ on `ktvic_test` ($n = 558$) **with zero parameter refitting**, or whether changing the VLM backbone shifts the baseline precision intercept $a_P$.

---

## 2. Pinned Backbone, Weights, Vision Budget, and Virtual Environment

- **Backbone Hub ID**: `Qwen/Qwen3-VL-8B-Instruct`
- **Pinned Revision**: `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b`
- **Licence**: `Apache-2.0` (open weights, non-gated; `17,545,915,883` bytes across 4 safetensors shards)
- **Snapshot Path**: `/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd`
- **Checksum Manifest**: `/root/ncs-data/models/Qwen3-VL-8B-Instruct-0c351dd/SHA256SUMS` (`sha256 = dc7bd4a45eb3c56e00c56f68cd937871258b679b741949bd38a383950ffc52d8`)
- **Isolated Virtual Environment**: `/root/venv-qwen3vl` (Python `3.10.12`, `torch==2.5.1+cu121`, `torchvision==0.20.1+cu121`, `transformers==4.57.6`, `accelerate==1.15.0`; `/root/vsps/.venv` is never modified)
- **Pinned Environment Freeze**: `/root/venv-qwen3vl/FREEZE.txt` (`sha256 = bf152944ea4389f609207c5f9589c214b2ff6a4ae3b2e2a9c877e64a57fbe605`)
- **Architecture & Vision Token Budget**:
  - Model class: `Qwen3VLForConditionalGeneration`, Processor class: `Qwen2VLImageProcessorFast`
  - Patch geometry: `patch_size = 16`, `merge_size = 2` (`1024` pixels/token vs `784` pixels/token in `Qwen/Qwen2.5-VL-7B-Instruct`)
  - Evaluation vision budget: `256` to `1024` vision tokens (`min_pixels = 262144`, `max_pixels = 1048576`)
  - 4-bit NF4 LoRA SFT vision budget: `256` to `512` vision tokens (`min_pixels = 262144`, `max_pixels = 524288`)

### Pinned Weight Shards (`Qwen/Qwen3-VL-8B-Instruct`)

| Shard | Size (bytes) | SHA-256 |
|---|---:|---|
| `model-00001-of-00004.safetensors` | 4,902,275,944 | `d5d0aef0eb170fc7453a296c43c0849a56f510555d3588e4fd662bb35490aefa` |
| `model-00002-of-00004.safetensors` | 4,915,962,496 | `8be88fb5501e4d5719a6d4cc212e6a13480330e74f3e8c77daa1a68f199106b5` |
| `model-00003-of-00004.safetensors` | 4,999,831,048 | `83de00eafe6e0d57ccd009dbcf71c9974d74df2f016c27afb7e95aafd16b2192` |
| `model-00004-of-00004.safetensors` | 2,716,270,024 | `0a88b98e9f96270973f567e6a2c103ede6ccdf915ca3075e21c755604d0377a5` |

---

## 3. Two-Step Gated Execution Protocol (`PD-5 Q1(b)` & `Q1(c)`)

Every output JSON produced by `manuscript/prereg/2026-10-14_b1_jobs/61_b1_qwen3vl_guard_and_gate.sh` records `"machine_id": $(hostname)` (`PD-5 Q2`).

### Step 1: Zero-Shot `dev300` Language & Pathology Guard (~`0.2` GPU-h)

Before launching SFT, `Qwen/Qwen3-VL-8B-Instruct` is decoded zero-shot (`bfloat16`, `sdpa`, greedy `do_sample=False`, `max_new_tokens = 60` for `short` and `160` for `detailed`) on KTVIC `dev300` (`dev_data.json`, $n = 300$ held-out images disjoint from `train_nodev`).

| Mode | Vietnamese Share (`looks_vietnamese`) Min | CJK Leakage (`abs_halluc.CJK`) Max | Mentions / Caption ($M$) Band | `S0` Baseline Reference (`Qwen/Qwen2.5-VL-7B-Instruct`) |
|---|---:|---:|---:|---|
| `short` | `>= 0.98` | `<= 0.02` | `[0.8, 3.5]` | Vietnamese `98.52%`, CJK `1.96%` |
| `detailed` | `>= 0.98` | `<= 0.05` | `[0.8, 3.5]` | Vietnamese `100.00%`, CJK `5.00%` |

- **Abort Rule**: Abort immediately before Step 2 SFT; record pathology in step1_dev300_guard.json and fall back to held 3B jobs 57/58 with qwen-research licence disclosure.

### Step 2: 1-Seed `P1` SFT Gate on `train_nodev` (`b1_qwen3vl_p1_nodev_s42`, ~`1.8` GPU-h; Total Step 1 + Step 2 ~`2.0` GPU-h)

If Step 1 passes, train 1 seed (`seed = 42`) on `train_nodev` (`data/splits/ktvic_train_minus_dev300.txt`, `3469` images, deterministic SFT JSONL `sha256 = 971879742e85d710fc828fa526b735d0c0b6469b4988e3d5402a26fb1b666f16`) using the exact `P1` recipe:
- **Loss mask**: `--loss-mask assistant` (response-only supervision)
- **Optimisation**: `epochs = 2.0`, `lr = 0.0001`, `batch_size = 1`, `grad_accum = 8` (effective batch `8`)
- **LoRA adapter**: language-tower projections `^(?!.*visual).*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)$`, `r = 16`, `lora_alpha = 32`, `lora_dropout = 0.05`, 4-bit NF4 double quantisation
- **Hardware & Telemetry Gates**:
  - Peak CUDA memory allocated must satisfy `peak_vram_gb <= 22.0` GB (`step2_train_s42_telemetry.json`).
  - Mean training step time (`step_time_sec`) and `machine_id` are logged.
  - Promotion to seeds `43` and `44` (full 3-seed budget `7.0` to `8.0` GPU-h) requires `dev300` Vietnamese share `>= 0.99`, `dev300` CJK rate `<= 0.01`, and `ktvic_test` `short` mention count $M_{\text{B1}} \in [1.2, 2.5]$.

---

## 4. Frozen Frontier Predictions (`zero` Refitted Parameters) & Dual-Matcher Protocol (`PD-2`, `PD-5 Q1(d)`)

All frontier predictions are fixed by the committed `Qwen/Qwen2.5-VL-7B-Instruct` anchor constants from `manuscript/prereg/2026-10-12_ladder_predictions.json` (`scripts/prereg_ladder_check.py`):

- $M_1 = 1.7826$, $\text{TP}_1 = 1.3996$, $P_1 = 78.5188$, $R_1 = 41.8507$, $b = 0.7468$, $c_0 = 5.4859$, $c_1 = 25.9815$
- Local tangent slope at $M_1$: $b_P = (1.0 - b) \cdot P_1 / M_1 = 11.1528$ pp/mention

Given any observed mention count $M_{\text{B1}}$ on `ktvic_test` ($n = 558$), the predicted frontier values are computed without refitting:

$$\widehat{\text{TP}}_0(M) = 1.3996 \cdot \left(\frac{M}{1.7826}\right)^{0.7468}, \quad \hat{P}_0(M) = \frac{100.0 \cdot \widehat{\text{TP}}_0(M)}{M}, \quad \hat{R}_0(M) = 5.4859 + 25.9815 \cdot \widehat{\text{TP}}_0(M), \quad \widehat{F_1}_0(M) = \frac{2.0 \cdot \hat{P}_0(M)\hat{R}_0(M)}{\hat{P}_0(M) + \hat{R}_0(M)}.$$

For comparison, the `Qwen/Qwen2.5-VL-7B-Instruct` observed `P1` seeds and pre-registered bands in `2026-10-12_ladder_predictions.json` are:
- `p1-gold-short` (`seed 42`): $M = 1.796$, $\text{TP} = 1.400$, $P = 77.944$, $R = 41.420$, $F_1 = 54.094$.
- `p1_s43-short` (`seed 43`): $M = 1.763$, $\text{TP} = 1.389$, $P = 78.760$, $R = 41.685$, $F_1 = 54.516$.
- `p1_s44-short` (`seed 44`): $M = 1.789$, $\text{TP} = 1.410$, $P = 78.858$, $R = 42.447$, $F_1 = 55.188$.
- `p1ep4_s42-short` (pre-registered band): $M = 1.723$ (`[1.629, 1.818]`), $P = 79.2$ (`[77.1, 81.3]`), $R = 40.9$ (`[38.5, 43.4]`), $F_1 = 54.0$.
- `fuse2_s42-detailed` (anchor): $M = 3.154$, $\text{TP} = 2.143$, $P = 67.955$, $R = 61.174$, $F_1 = 64.386$.

### Pre-Computed Frontier Evaluation Grid (`prereg_ladder_check.at(fr, M)`)

| Mention Count $M$ | $\widehat{\text{TP}}_0(M)$ | $\hat{P}_0(M)$ (%) | $\hat{R}_0(M)$ (%) | $\widehat{F_1}_0(M)$ (%) | Linear Tangent $P_0^{\text{lin}}(M)$ (%) |
|---:|---:|---:|---:|---:|---:|
| `1.4000` | `1.1685` | `83.4675` | `35.8464` | `50.1536` | `82.7859` |
| `1.6000` | `1.2911` | `80.6926` | `39.0301` | `52.6123` | `80.5553` |
| `1.7230` | `1.3645` | `79.1935` | `40.9378` | `53.9744` | `79.1835` |
| `1.7630` | `1.3881` | `78.7346` | `41.5506` | `54.3952` | `78.7374` |
| `1.7826` | `1.3996` | `78.5145` | `41.8496` | `54.5977` | `78.5188` |
| `1.7890` | `1.4034` | `78.4433` | `41.9471` | `54.6633` | `78.4474` |
| `1.7960` | `1.4074` | `78.3658` | `42.0536` | `54.7347` | `78.3694` |
| `2.0910` | `1.5767` | `75.4055` | `46.4517` | `57.4888` | `75.0793` |
| `2.5820` | `1.8457` | `71.4841` | `53.4405` | `61.1592` | `69.6033` |
| `3.1540` | `2.1432` | `67.9524` | `61.1700` | `64.3831` | `63.2239` |

### Primary Endpoint (`PD-2`) & Dual-Matcher Side-by-Side Scoring (`PD-5 Q1(d)`)

- **Primary Endpoint**: Frontier precision residual at `B1`'s own mention count $M_{\text{B1}}$ on `ktvic_test` (`short`):
  $$\Delta P_{\text{front}} = P(\text{B1}) - \hat{P}_0(M_{\text{B1}})$$
  evaluated with `10,000` paired image-level bootstrap resamples (`0.95` CI, equivalence margin $\pm 2.0$ pp).
- **Dual-Matcher Reporting**: Every `B1` caption file is scored side by side under:
  1. **Matcher `v1` (`RESCAP_RAW_TONE=1`)**: frozen `ba351f8` NFC semantics (`rescap/chair.py` `sha256 = fd1d012398cae5d1984bb4effdf18919e157f1c770b8a13adbb070a8b659ec6b`).
  2. **Matcher `v2` (`RESCAP_RAW_TONE=0`)**: tone-normalised NFC + open-syllable `oa/oe/uy` normalisation (`rescap/chair.py` `sha256 = e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3`).

---

## 5. Pre-Registered Two-Outcomes Interpretation Protocol (`PD-5 Q1(a)`)

Both outcomes are pre-registered with explicit decision rules and manuscript actions:

1. **Outcome A — Cross-Backbone Frontier Invariance Holds (`|delta_P_front| <= 2.0` pp and `0.95` CI includes `0.0`)**:
   - **Criterion**: abs(delta_P_front) <= 2.0 pp AND 95% paired bootstrap CI of delta_P_front contains 0.0 (or TOST equivalence holds within [-2.0, +2.0] pp).
   - **Scientific Claim**: Cross-backbone frontier invariance holds: the count-driven precision-recall frontier P0(M) is invariant across VLM backbones (Qwen2.5-VL-7B vs Qwen3-VL-8B) under identical P1 supervision.
   - **Manuscript Action**: Report B1 (Qwen3-VL-8B P1) on the shared frontier plot in Section 5 as cross-backbone confirmation of H1/H2/H3.
2. **Outcome B — Backbone Intercept Shift (`|delta_P_front| > 2.0` pp with `0.95` CI excluding `0.0`)**:
   - **Criterion**: abs(delta_P_front) > 2.0 pp WITH 95% paired bootstrap CI of delta_P_front excluding 0.0.
   - **Scientific Claim**: Backbone visual-language prior shifts the baseline precision intercept a_P (by delta_a_P = delta_P_front) while preserving within-backbone count-slope b(k) and gold-completeness monotonicity (H4).
   - **Manuscript Action**: Report exact backbone intercept shift delta_a_P (under both v1 and v2 matchers) and scope the paper's invariance claim to within-backbone supervision-ladder invariance.

---

## 6. Frozen Instrument Checksums

| File | SHA-256 |
|---|---|
| `scripts/train_stage2.py` | `29312ef765e3e49e5e1efefc5ad8b88fcf33c991b1a5f3a266a910ada3d1cab4` |
| `scripts/evaluate.py` | `a68d56826d90d8a409493cd6f49007e906c6cb4f5668314edb9b8e7a632e8236` |
| `scripts/object_prf.py` | `6b711280d70b780d596414896d832738da58f1b079015dee888605d1ba350adc` |
| `scripts/prereg_ladder_check.py` | `279942468d879c93ca4c5c8767b829397b58cebedd73d845496f6ead22616d19` |
| `scripts/abs_halluc.py` | `76819c8e1c439cce2c5651e50e2a86d28078c2cbb67db22bc6327401bbcfc481` |
| `scripts/ktvic_dev_split.py` | `b4adfb4c6c6538c735126f1423e8520b156ad6ec81fa3aec9efa0d8558ff7c92` |
| `scripts/build_gold_sft.py` | `18e7909f25cc5c94b194d1a4e13fe6d396b6a8debe73a354699534b1f009c60a` |
| `scripts/s0_screen.py` | `78ff783870ad0921e84d0ba57fc69ed679c80f89373aad750bf298640333d5e3` |
| `rescap/chair.py` | `e47d249ac7290070f2387d3fa8b22dac77728265ad276f55aa6520f5cbc591a3` |
| `rescap/vlm/base.py` | `e8fee5bc5b729534af67c6e462a27f0d83ba611f18ff8e3f2717b11eb393ae93` |
| `rescap/vlm/mock.py` | `33793de01b4f2790964342b1af2d4c2de18d793ae4693608283992475ed62ce7` |
| `rescap/vi/lexicon.py` | `fbc945f2247418275144ac75b893f7c51f8951b9ea42018680d433775dd79eb9` |
| `data/splits/ktvic_train_minus_dev300.txt` | `006080b455a553ca9cc5d3f514ad76bfbe67f444c9c145a5696de681a4be1a58` |
| `manuscript/prereg/2026-10-12_ladder_predictions.json` | `65dae1bc1598c6b7fc4743fd5ba9e3e25245a3a90b2e6d8ec614eeea5702ece3` |
| `manuscript/prereg/2026-10-13_s0_qwen3vl.md` | `a9c616ca06503413224466d71d674c7655da0c371a1646b3ceb2c82f86ed69b8` |
| `manuscript/prereg/2026-10-14_b1_jobs/61_b1_qwen3vl_guard_and_gate.sh` | `7d44ea6c8f20639003a53a1bb30f0e0bac5caab8be77e7800f4c7880db69c471` |
