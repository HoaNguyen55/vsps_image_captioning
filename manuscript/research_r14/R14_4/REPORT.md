# R14-4: data and model levers for KTVIC / UIT-ViIC (CIDEr, object F1, CHAIR_i)

2026-10-15. CPU only: nice 19, 1 thread, peak RSS 0.86 GB. No weights downloaded, no git commit, no new labels.

The CPU scripts are in the session scratchpad, to be copied here:
- `coverage.py` and `coverage.out`
- `soup_proxy.py` and `soup_proxy.out`
- `sports_pool.py` and `sports_pool.out`

This report builds on R6-B5 (backbone and recipe), R9-C6 (multitask data), R9-C7 (resolution) and R9-C8 (backbone). Their numbers are cited, not recomputed.

## 0. Bottom line

1. **We are not capacity-limited, and not limited by KTVIC caption text.**
   - Four epochs overfit: CIDEr −6.7 and F1 −2.9 against the same seed at two epochs.
   - Training on five references per image raised the targets' test n-gram coverage from 68.4% to 84.0%, yet CIDEr moved −1.1.
   - The 32–38 point gap to a held-out human caption (181.5) is phrasing consensus, not recognition (B5 §5, C8 §0).
2. Backbone size, LoRA rank, full fine-tuning, vision-tower unfreezing and resolution are each worth at most about +2 CIDEr on KTVIC. None is a primary lever.
3. **Ranked proposals:**
   - (A) Seed consensus (delta-space soup, MBR fallback): +1 to +3 KTVIC CIDEr, about 4.3 GPU-h.
   - (C) Image data-scaling probe: about 1.8 GPU-h. It gates every external-data spend.
   - (B) UIT-ViIC translate-train plus a joint, dataset-tagged model: UIT-ViIC +2 to +5 CIDEr, KTVIC ±1, about 8 GPU-h to screen.
4. Not proposed: training Qwen2.5-VL-32B (does not fit 24 GB), synthetic captions from a stronger VLM for KTVIC, curriculum or style-matched SFT, and WiSE-FT as a KTVIC lever.
   - Synthetic captions bring style drift and raise hallucination when distilled into ≤7B models (KnowAda 2411.09018).
   - Curriculum and style matching are what P1 already does. The `cons` target gave 147.09 against a legacy mean of 145.8, within noise.
   - WiSE-FT moves outputs toward the zero-shot CIDEr of 29. It stays a COCO lever (job 59).

## 1. Own logs: data-limited or capacity-limited?

No log holds dev CIDEr. The `*metrics.jsonl` files have train loss only, and `p1dev_s42` is the only dev300 run (CIDEr 144.33, CHAIR_i 0.233). The rows below are existing test runs, read only for diagnosis; nothing was selected on them.

| run | epochs | last-epoch mean train loss / token acc | test CIDEr | short object P / R / F1 (v2) |
|---|---|---|---|---|
| P1 legacy, seeds 42/43/44 | 2 | 0.370 / 0.90 (from the p1ep4 log, epoch 2) | 149.79 / 143.92 / 143.70 | – |
| P1-4ep s42 | 4 | 0.230 / 0.946 | **143.10** | 77.57 / 39.77 / **52.58** |
| cons s42 | 2 | 0.380 / 0.90 | 147.09 | – |
| P1-R (p1assist), 3 seeds | 2 | – | 148.66 / 148.06 / 147.96 (SD 0.38) | 78.76 / 42.86 / **55.51** (s42) |
| multiref (mr5assist) s42 | 2 | – | 147.55 | – |

- P1-4ep loss by epoch: 0.556, 0.370, 0.300, 0.230.
- After epoch 2, train loss falls 38% while held-out CIDEr and F1 fall. The 7B LM fits more than generalises, so it is not capacity-limited.

**N-gram coverage proxy (`coverage.py`).** IDF-weighted share of test-reference syllable 1–4-grams found in the training captions, with 5 random image subsets per size:

| share of train images | KTVIC images | KTVIC 1–4-gram | KTVIC 4-gram | UIT-ViIC images | UIT-ViIC 1–4-gram | UIT-ViIC 4-gram |
|---|---|---|---|---|---|---|
| 1/8 | 471 | 65.4% | 44.0% | 336 | 72.9% | 59.9% |
| 1/4 | 942 | 72.7% | 53.2% | 673 | 78.1% | 66.6% |
| 1/2 | 1,884 | 79.0% | 61.8% | 1,347 | 82.3% | 72.4% |
| all | 3,769 | 84.0% | 69.5% | 2,695 | 86.3% | 77.9% |

- Coverage grows about +5 points per doubling and has not saturated.
- But multiref is the counter-test. Slot-0-only targets (P1) cover 68.4%; all five references cover 84.0%, about three doublings' worth. CIDEr still went 148.66 → 147.55. Greedy decoding emits the modal phrasing, so more phrasing breadth does not reach the 1-best caption.
- Whether new *images* help is unknown. Proposal C measures it.
- **Joint training transfers little phrasing.** UIT-ViIC train adds +0.4 points to KTVIC-test coverage (84.0 → 84.4). KTVIC adds +1.3 to UIT-ViIC (86.3 → 87.6).
- **The styles conflict.** 57% of KTVIC captions start with "có"; UIT-ViIC captions start with "một" (37%). Cross-corpus transfer is weak: KTVIC→UIT-ViIC scores 41.7 against 132.07 in-domain.
- So joint training is a UIT-ViIC and one-model convenience lever, and it needs a dataset tag.

**Seed-consensus proxy (`soup_proxy.py`).** Stdlib syllable-level CIDEr-D, read as paired deltas only. MBR, the medoid of the 3 seeds' greedy captions, minus the seed mean:
- P1-R seeds: **+3.05 [+1.03, +5.11]**. Seeds score 164.4 / 164.2 / 164.4 at syllable level, and all three agree on only 31.9% of images.
- Legacy seeds: +3.33 [+1.31, +5.41], matching B5's word-level +2.79.
- The response-only mask removed the score spread, not the caption disagreement.

## 2. Levers: feasibility on one 3090, licence, Vietnamese evidence, expected effect

Primary pages were checked for every ID below. Memory figures are from C8/B5 estimates (±1.5 GB) or our own measurement.

| lever / model | fits 24 GB? | licence | Vietnamese evidence | expected KTVIC effect |
|---|---|---|---|---|
| Qwen2.5-VL-32B-Instruct (33.45B; tech report 2502.13923) | QLoRA training: no. NF4 weights ≈18 GB plus activations for 64 layers × 5120 hidden (≈3.3× the 7B), against a measured 7B peak of 11.7–12.7 GB. 4-bit inference only, about 20–22 GB. | apache-2.0 | none on card | n/a for training; teacher only |
| InternVL3-8B / 14B (2504.10479) | 8B: 11.4–14.0 GB. 14B (15.1B): est. ≈17–19 GB at 1 tile. | 8B: apache-2.0 in metadata, "MIT" in card text. 14B: apache-2.0. | MTVQA 30.2 (8B) | CIDEr 0 to +2 |
| InternVL3.5-8B (2508.18265) | 12.0–14.8 GB | apache-2.0 | MTVQA 35.2 | 0 to +2 |
| Vintern-1B-v3_5 / Vintern-3B-R-beta (2408.12480) | yes (3B ≈10.8 GB); full fine-tuning feasible for 1B only | mit. Vintern-3B-beta states no licence. | vi-MTVQA 37.4 (1B), 41.29 (3B-beta) | ≤0; weaker perceivers. **Leakage:** trained on OpenViVQA-derived data, which shares the image pool with KTVIC test (401 of 558 test images are in the OpenViIC train pool). Hash-check before any use. |
| MiniCPM-V 2.6 (2408.01800) / V-4 / V-4.5 (2509.18154) | 13.2 GB (4.5) | 2.6: MiniCPM licence, gated. 4 and 4.5: apache-2.0. | none | 0 to +2. MiniCPM-V 4 needs 3.48 tokens per syllable; exclude it. |
| Gemma-3-12B / 27B (2503.19786) | 12B: 14.5–17.9 GB. 27B: no. | Gemma terms, gated | "140+ languages"; Vietnamese not named | ≈0. Fine-tuned COCO CIDEr is 143/143/144 for 4B/12B/27B. |
| Qwen3-VL-8B | yes | apache-2.0 | – | already failed our guard (3% CJK) |
| Full fine-tuning (7B) | no: bf16 weights 16.6 GB plus gradients and optimizer | – | – | LoRA learns less but forgets less (2405.09673); QLoRA matches 16-bit (2305.14314) |
| LoRA rank, alpha, DoRA, rsLoRA (2402.09353, 2312.03732) | yes | – | – | ≤+1; DoRA on COCO captions +0.6 |
| Vision-tower unfreezing | yes, but needs gradient hooks | – | – | ≤±0.3 average in a controlled MLLM study (2406.05130); C8: misses are mention policy, not perception |
| Resolution 2048 (job 60, queued) | yes | – | – | preregistered ΔR ∈ [−1, +1]. The 512-token cap already covers 281/558 test images natively. |
| Joint KTVIC + UIT-ViIC | yes | – | coverage +0.4 / +1.3 points | KTVIC ±1. UIT-ViIC near in-domain 132; one model for both. |
| Translated COCO | yes | VinAI Translate en2vi: AGPL-3.0. NLLB-200: CC-BY-NC-4.0. | weak (see below) | KTVIC ≈0 (third style). UIT-ViIC +2 to +5 as a pre-stage. |
| Synthetic captions from a stronger VLM | 32B inference only | – | none | KTVIC ≤0 (style, hallucination); not proposed |
| Soups, WiSE-FT, seed ensembles (2203.05482, 2109.01903, LoRA Soups 2410.13025) | yes | – | own proxy +3.05 | +1 to +3 CIDEr |

**Translated-COCO evidence:**
- XM3600 (2205.12522): Vietnamese CIDEr 0.18–0.19 when trained on machine-translated COCO only.
- UIT-ViIC paper (2002.00175): human Vietnamese captions reach val CIDEr-D 1.005 against 0.578 for a Google-translated set, with different references.
- COCO-CN (1805.08661): machine-translate first, then fine-tune on human captions, works best. No number was pulled.

**Published Vietnamese baselines:**
- KTVIC GRIT: CIDEr 136.0, BLEU-4 40.6 (2401.08100, segmented captions). Our 148.2 is comparable only under the same tokenisation.
- No published VLM or LoRA CIDEr exists on KTVIC or UIT-ViIC, and no Vietnamese VLM card reports captioning CIDEr. Expected gains therefore rest on our own proxies and cross-language evidence.

**Leakage facts:**
- UIT-ViIC images are COCO train2017 images.
- `dinhanhx/coco-2017-vi` merges UIT-ViIC into its train file. Any translated-COCO or ShareGPT4V-COCO set must exclude UIT-ViIC val and test by COCO id.
- The leak-free sports pool (`sports_pool.py`) is Karpathy train+restval, minus UIT-ViIC val/test, minus the 2,441-image probe, with ≥3 of 5 English captions naming a sport: **19,407 images, 2,262 of them already in UIT-ViIC train**. POPE-500 ids must also be removed; they were not checked here.

## 3. Proposals

### A. Seed consensus on P1-R (delta-space soup; MBR fallback)

**Mechanism**
- Uniform soup of the adapters in delta space: `add_weighted_adapter([...], [1/3]*3, combination_type="cat")`. Never use factor averaging; seed deltas have cosine 0.30.
- Fallback: MBR medoid over the 3 seeds' greedy captions.
- There are no free hyper-parameters, and the norm-preserving variant is excluded, so nothing is tuned.

**GPU-h on one 3090: about 4.3**
- Train `p1dev_s43` and `p1dev_s44` (train minus dev300, assistant mask, 2 epochs): 3.6.
- dev300 evaluation of the soup and MBR: 0.2.
- Test evaluation of the soup of the existing `p1assist_s42/43/44`, short and detailed: 0.5.

**dev300 selection**
- Compare the soup of `p1dev_s42/43/44` with MBR against the member mean.
- Carry the better one to test only if it is ≥ +1.0 CIDEr.

**Prereg sketch: frozen predictions (test, against the member mean, paired bootstrap B=5000)**
- CIDEr +1.0 to +3.0 (central +2.0).
- B-4 +0.5 to +1.0.
- F1 −1.0 to +1.5.
- CHAIR_i −1.0 to +0.5 pp.
- Mentions per caption within ±0.10.

**Kill rules**
- K1: on dev300, both soup and MBR are below the member mean + 1.0 CIDEr.
- K2: CHAIR_i is more than 1.0 pp above the member mean.
- K3: a test F1 drop whose CI excludes 0 is reported as a negative.

**Relation to earlier work**
- SeedLoRA (ICML 2025) and model soups. This is engineering, with no novelty claimed.
- The killed UPE-MBR was object-consensus over samples from one model; this is consensus across independently trained seeds. Disclose the relation.

### C. Image data-scaling probe (decides whether external data is worth funding)

**Mechanism**
- Train P1-R s42 on nested random 25% and 50% subsets of train minus dev300.
- The 100% point is the existing `p1dev_s42`.
- Fit dev300 CIDEr = a + b·log2(N), and also object F1 and CHAIR_i.

**GPU-h:** 0.45 + 0.9 for training, plus 3 × 0.12 for dev evaluation, about 1.8 in total.

**Selection:** none. This is a diagnostic with a frozen decision rule.

**Frozen predictions**
- b ∈ [+1, +4] CIDEr per doubling (coverage gives +5 points per doubling, but multiref shows weak text-to-CIDEr transfer).
- F1 slope ∈ [0, +2] per doubling.

**Decision and kill rules**
- If the lower CI of b is > +1, fund external-image data: KTVIC-style rewrites of translated COCO or Flickr30k captions, disclosed as machine-translated or AI-rewritten training data.
- If b < +1, close every data-volume lever for KTVIC and report that as a finding.
- In either case, in-domain extra images (OpenViVQA, EVJVQA, OpenViIC) are forbidden because of the KTVIC test overlap.

### B. UIT-ViIC translate-train plus a joint, dataset-tagged model

**Data**
- UIT-ViIC train minus its 133 Karpathy-test images, leaving 2,562.
- About 7,500 rows from the 17.1k new sports-pool images, at a frozen 3:1 ratio to UIT-ViIC train. Use one random English caption per image, translated by VinAI Translate en2vi.
  - Its AGPL-3.0 licence applies to the tool, not to the outputs; record this. NLLB is non-commercial.
- Exclude by COCO id: UIT-ViIC val and test, Karpathy test and val, the COCO probe-2500 and POPE-500. Then run a pHash near-duplicate pass (`scripts/near_dup.py`).
- Disclose the rows as machine-translated training data. They are never used as references.

**Recipe**
- Stage 1: translated rows, 1 epoch.
- Stage 2: UIT-ViIC plus KTVIC train minus dev300, 2 epochs, with a dataset tag in the prompt.
- The tag needs a new frozen prompt variant in `evaluate.py`; that is an instrument change and must be preregistered.

**GPU-h**
- Translation about 0.5. Stage 1 about 2.0. Stage 2 about 3.0. Evaluation on UIT-ViIC val, KTVIC dev300 and test about 1.0.
- That is about 6.5 for one seed, or about 8 including a no-translation joint arm. Two more seeds if it passes: +13.

**Dev selection:** UIT-ViIC val (924 images, no Karpathy-test images) for UIT-ViIC, and KTVIC dev300 as the guard. No ratio sweep.

**Frozen predictions (against in-domain UIT-ViIC P1, test 132.07, val 128.23)**
- UIT-ViIC val CIDEr +2 to +5.
- COCO-instance F1 +0 to +3.
- CHAIR_i within ±1.5 pp.
- KTVIC dev300 CIDEr within −2 to +1 of `p1dev_s42` (144.33).
- Evidence: UIT-ViIC coverage is +4 points per doubling and unsaturated; COCO-CN's two-stage result. Translate-only CIDEr is weak (XM3600, UIT-ViIC paper), so a large gain is not expected.

**Kill rules**
- K1: UIT-ViIC val gain < +2.0, or its CI includes 0.
- K2: KTVIC dev300 below 142.3. If so, keep separate adapters; the translation stage alone may still pass.
- K3: COCO CHAIR_i up > 2 pp.
- K4: any UIT-ViIC val or test id, or near-duplicate, found in the training rows. Abort.

## 4. Ranking (expected gain × confidence ÷ GPU-h)

1. **A, seed consensus.** Headline KTVIC CIDEr +1 to +3, F1 ±1, CHAIR flat. 4.3 GPU-h. Stacks with any method. Confidence medium-high, because the proxy CI excludes 0.
2. **C, scaling probe.** No metric gain by itself, but 1.8 GPU-h decides whether any data lever (translated, synthetic or distilled) deserves the roughly 20+ GPU-h it would cost.
3. **B, translate-train plus joint model.** Helps UIT-ViIC only. 8 GPU-h screen, 21 for full seeds. Confidence low-medium given the weak published translate-train evidence.

Backbone swaps (InternVL3/3.5-8B), resolution (job 60) and WiSE-FT (job 59) stay as queued controls, not metric levers.
