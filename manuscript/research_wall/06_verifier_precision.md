# 06 — Verifier precision (VLM-as-judge reliability, yes-bias, calibration, ensembles, detectors, thresholds)

Agent 06, 2026-10-10. Angle: lift the precision of the SUPPORTED verdict above the audited 63.1%.
Already covered elsewhere and not repeated here: UNIHD/MHaluBench, HQM, UHP, POPE, NegBench/NegVQA/NOPE, SelfCheckGPT, VL-Uncertainty, LogicCheckGPT, ConBench (novelty/07); conformal factuality, verbalized object confidence (novelty/03); RLAIF-V, FGAIF, HalluciDoctor (novelty/02).

## 0. Repo state that shapes the recommendations

- `rescap/pipeline/verify.py`: three-state rule, direct plus negated probe (`acquiescent = direct.affirms and negated.affirms` → C = 0.50 → UNCERTAIN), score S = 0.6·V + 0.2·M + 0.2·G, gates E / S / C.
- `Thresholds` defaults are **UNTUNED** (`decision_rule_version = "v1.0-doc07-UNTUNED"`, E 0.35, S_lo 0.35, S_hi 0.70, C_lo 0.20, C_hi 0.60), and `per_type_thresholds` is empty. The paper therefore runs a hand-set rule with no dev-split tuning.
- `rescap/vlm/vintern.py`: `supports_logprobs = False`. Confidence comes only from K = 5 sampled generations at T ≥ 0.7 (`base.py`), so V takes just the values {0, .2, ..., 1}. That is coarse, it costs 5x, and it is the main reason for ~80 s/image.
- Human audit by type (`data/annotations/audit/tn.json`, 244 machine-SUPPORTED items):

  | type | n | human SUPPORTED | human REJECTED | human UNCERTAIN |
  |---|---|---|---|---|
  | entity | 81 | 54 (66.7%) | **22 (27.2%)** | 5 |
  | attribute | 64 | 40 (62.5%) | 14 (21.9%) | 10 |
  | action | 58 | 38 (65.5%) | 14 (24.1%) | 6 |
  | counting | 34 | 19 (55.9%) | 9 (26.5%) | 6 |
  | relation | 7 | 3 | 3 | 1 |

  Entity existence produces the most false SUPPORTED verdicts in absolute terms (22 of 62). Yes-bias on object existence is the textbook failure for that type, so it is also the cheapest type to fix.
- A round-2 sample of machine REJECTED/UNCERTAIN items exists (`audit_round2_sample.json`, only 12 verdicts so far). Without it, recall cannot be estimated, and the threshold trade-off cannot be drawn.

## (a) Papers

| # | Paper | Venue / year | Link (opened) | Method (1–2 sentences) | Relevance | Action for VSPS |
|---|---|---|---|---|---|---|
| 1 | **System-Mediated Attention Imbalances Make Vision-Language Models Say Yes** — T. T. Chan, V. Suresh, A. Saha, M. Hahn, V. Demberg | Findings of ACL 2026 (arXiv 2601.12430, Jan 2026) | https://arxiv.org/abs/2601.12430 | Attributes yes-bias to attention drawn onto the system-prompt tokens. Moving attention from system tokens to image/text tokens strongly suppresses yes-bias on binary tasks. | technique-to-borrow; must-cite for the yes-bias claim | Cite it as the 2026 mechanism behind VSPS's acquiescence check. Cheap test: run Vintern with an empty or minimal system prompt and compare the yes-rate on the negated probes. |
| 2 | **Debiasing Multimodal Large Language Models via Penalization of Language Priors** — Y.-F. Zhang et al. | arXiv 2403.05262 (v3) | https://arxiv.org/abs/2403.05262 | "Post-Hoc Debias" is an affine calibration of answer scores, chosen so that an image-free (blank/noise) input gives uniform answer scores. Also proposes visual-debias decoding. | technique-to-borrow (high) | Ask every probe a second time on a blank image and subtract the blank-image P(yes) (or yes-rate) per proposition. Large yes-rates on the blank image flag language-prior SUPPORTED verdicts. |
| 3 | **VaPR — Vision-language Preference alignment for Reasoning** | arXiv 2510.01700 (Oct 2025) | https://arxiv.org/abs/2510.01700 | Reports that LLaVA-1.5, Qwen2-VL and Qwen2.5-VL all favour "Yes" on NaturalBench even when "No" is correct, and mitigates this with preference data. | evidence (Qwen2.5-VL yes-bias) | Cite it when arguing that Qwen2.5-VL is also not a neutral second verifier. Its probes need the same negation control. |
| 4 | **Analyzing and Mitigating Object Hallucination: A Training Bias Perspective** (POPEv2, Obliviate) — Y. Li, K. Zhou, W. X. Zhao, L. Fang, J.-R. Wen | arXiv 2508.04567 (Aug 2025) | https://arxiv.org/abs/2508.04567 | Counterfactual masked-object images show LVLMs answer "Yes" about masked objects, especially on images seen during training. Probing places the bias in the LM head, and fine-tuning about 2% of parameters (LM head only) reduces it. | technique-to-borrow; warning | KTVIC/COCO images may sit in Vintern's training data, so its existence answers can be memorised. Add a masked-object counterfactual probe (inpaint or black-box the bbox, then re-ask) for entity props. |
| 5 | **Seeing is Believing, but How Much? A Comprehensive Analysis of Verbalized Calibration in VLMs** — W. Xuan, Q. Zeng, H. Qi, J. Wang, N. Yokoya | EMNLP 2025 main (ACL Anthology 2025.emnlp-main.74; arXiv 2505.20236) | https://aclanthology.org/2025.emnlp-main.74 | Large study showing VLM verbalized confidence is poorly calibrated. Proposes two-stage Visual Confidence-Aware Prompting. | must-cite (why VSPS does not trust verbalized confidence) | Justify agreement-based or logit-based confidence over verbalized confidence. Do not add a verbalized-confidence channel. |
| 6 | **HalLoc: Token-level Localization of Hallucinations for Vision Language Models** — E. Park, M. Kim, G. Kim | CVPR 2025 (arXiv 2506.10286) | https://arxiv.org/abs/2506.10286 | 150K token-level annotated samples (object/attribute/relation/scene types, probabilistic labels). HalLocalizer is a light VisualBERT plus 4 type heads, reading text or VLM hidden states. | technique-to-borrow; baseline-to-compare (detector) | Its type split matches VSPS's typed propositions. Run HalLocalizer (English, through MT) as an independent second verifier on the audited 244 items, or cite it as a learned-detector baseline. |
| 7 | **Detecting and Preventing Hallucinations in LVLMs** (M-HalDetect) — A. Gunjal, J. Yin, E. Bas | AAAI 2024, DOI 10.1609/aaai.v38i16.29771 (arXiv 2308.06394) | https://arxiv.org/abs/2308.06394 | 16k fine-grained annotations (objects, descriptions, relations). Trains reward models for best-of-n rejection sampling (−55% hallucination on InstructBLIP) and FDPO. | baseline-to-compare; benchmark | If a learned detector is added, report its accuracy on M-HalDetect to place VSPS's verifier against published numbers. |
| 8 | **Evaluation and Analysis of Hallucination in LVLMs** (HaELM) — J. Wang et al. | arXiv 2308.15126 (2023) | https://arxiv.org/abs/2308.15126 | Text-only LLM fine-tuned as a hallucination judge, reaching about 95% of ChatGPT (61.0 vs 64.0 accuracy). | must-cite (historic); low technical value | Cite it as the first LLM-as-hallucination-judge, and as evidence that judges reach only ~60% accuracy. That is the same order as VSPS's 63.1%, which helps frame the audit honestly. |
| 9 | **Unblocking Fine-Grained Evaluation of Detailed Captions: An Explaining AutoRater and Critic-and-Revise Pipeline** (DOCCI-Critique, VNLI-Critique) — B. Gordon, Y. Bitton, ..., I. Szpektor | arXiv 2506.07631 (Jun 2025) | https://arxiv.org/abs/2506.07631 | 10,216 sentence-level human factuality labels over 1,400 paragraph captions from 14 VLMs. VNLI-Critique is a sentence-level factuality classifier with critiques. It reports SOTA on M-HalDetect, and the AutoRater reaches Spearman 0.98 with humans. | overlap low–medium (critic-and-revise ≈ verify-then-rewrite); baseline-to-compare | Cite it in related work. Its sentence-level critic is the closest modern analogue of the VSPS verifier. Model size and weight release are not stated, so check before planning to use it. |
| 10 | **HalDec-Bench: Benchmarking Hallucination Detector in Image Captioning** — K. Saito, R. Shinoda, S. Tanaka, T. Hirasawa, F. Okura, Y. Ushiku | arXiv 2511.20515 (v4 Mar 2026; 2603.15253 is a withdrawn duplicate) | https://arxiv.org/abs/2511.20515 | Benchmarks VLMs used as caption-hallucination detectors, with segment-level human labels. Finding: detectors call early-position sentences correct regardless of truth, and strong VLM filters substantially reduce dataset noise. | HIGH relevance to framing (VLM-as-filter for caption data); overlap low–medium | Check whether VSPS verdicts depend on position. Propositions come from candidate captions, so measure SUPPORTED-rate vs. source-sentence index. Cite it as support for "VLM filter → cleaner SFT data". |
| 11 | **VL-RewardBench: A Challenging Benchmark for Vision-Language Generative Reward Models** — L. Li et al. | CVPR 2025 (arXiv 2411.17451) | https://arxiv.org/abs/2411.17451 | 1,250 hard human-verified items (general, hallucination, reasoning). GPT-4o reaches only 65.4%, and Qwen2-VL-72B is near chance. Failures are mainly in perception. Training a 7B judge adds 14.7%. | must-cite (VLM judges are unreliable) | Use it to put 63.1% in context: even frontier judges sit around 65% on hard items. Argue that the measured hallucination drop does not depend on the verifier (CHAIR uses the references). |
| 12 | **Multimodal RewardBench** — M. Yasunaga, L. Zettlemoyer, M. Ghazvininejad | arXiv 2502.14191 (Feb 2025) | https://arxiv.org/abs/2502.14191 | 5,211 expert-annotated preference triplets in 6 domains. The best judges (Gemini 1.5 Pro, Claude 3.5 Sonnet) reach about 72%. | must-cite (judge ceiling) | Same use as row 11. |
| 13 | **LLaVA-Critic: Learning to Evaluate Multimodal Models** — T. Xiong et al. | CVPR 2025 (arXiv 2410.02712) | https://arxiv.org/abs/2410.02712 | Open LMM trained as a generalist judge (pointwise and pairwise), on par with GPT judges. Also used for preference reward. | baseline-to-compare (open judge) | Candidate second verifier (7B, 4-bit fits a 3090). English-centric, so translate propositions to EN with a template. Use it only on SUPPORTED candidates (row 6 of section d). |
| 14 | **Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models** (PoLL) — P. Verga et al. (Cohere) | arXiv 2404.18796 (2024) | https://arxiv.org/abs/2404.18796 | A panel of small judges from different model families beats one large judge, with less intra-model bias and more than 7x lower cost. | technique-to-borrow | Basis for heterogeneous verifier agreement (Vintern-1B + Qwen2.5-VL-3B / Vintern-3B), which the paper already lists as future work. |
| 15 | **MLLMs Know Where to Look: Training-free Perception of Small Visual Details** (ViCrop) — J. Zhang, M. Khayatkhoei, P. Chhikara, F. Ilievski | ICLR 2025 (arXiv 2502.17422) | https://arxiv.org/abs/2502.17422 | Accuracy depends causally on object size. The model's own attention or gradients localize the region even when it answers wrongly, and cropping that region and concatenating it with the global view raises accuracy without training. | technique-to-borrow | Region-cropped verification for attribute/action/count props whose subject has a bbox. Grounding is already a signal (G), so reuse the box to feed a crop together with the full image. |
| 16 | **UniProbe: A Learnable Token-Level Hallucination Detector for Large VLMs using Multi-Structural Internal Representations** — D. Samuel, G. Bar-Shalom, F. Frasca, E. Fetaya, Y. Ziser, G. Chechik, H. Maron | arXiv 2608.10835 (Aug 2026) | https://arxiv.org/abs/2608.10835 | Small detector (GNN + ViT + GRU) over the attention graph of a frozen LVLM, run in a single pass. Streaming resampling cuts object hallucination by up to 55% at 1.06x latency. | watch; technique (future) | Too heavy to adopt now. Cite it as the 2026 trend from sampling-based to probe-based detectors. |
| 17 | **HaloProbe: Bayesian Detection and Mitigation of Object Hallucinations in VLMs** — R. Zohrabi, H. Hasani, A. Gupta, M. Soleymani Baghshah, A. Rohrbach, M. Rohrbach | arXiv 2604.06165 (Apr 2026) | https://arxiv.org/abs/2604.06165 | Shows that attention-based hallucination signals are confounded by token position and repetition (a Simpson's paradox). A Bayesian probe that factors out description statistics guides decoding. | watch; warning | If VSPS ever adds an attention signal, control for position and repetition. This also matches HalDec-Bench's position bias. |
| 18 | **IntroConformal: Conformal Factuality Guarantees for LVLMs via Introspective Signals** — Md. Atabuzzaman, C. Alexander, C. Thomas | EMNLP 2026 (arXiv 2609.01375, Sep 2026) | https://arxiv.org/abs/2609.01375 | Training-free conformal risk control over claim-level factuality. Uses hidden-state layer-wise stability plus the model's own verification probability, with no external verifier. | **overlap medium** (claim filtering with a calibrated threshold); must-cite | Contrast: VSPS uses an external small verifier, three states, and builds SFT data (not inference-time abstention). Borrow the CRC recipe for choosing θ_S^hi (row 2 of section d). |
| 19 | **Noisy but Valid: Robust Statistical Evaluation of LLMs with Imperfect Judges** — C. Feng, M. Shen, A. Balashankar, C. Gerner-Beuerle, M. R. D. Rodrigues | ICLR 2026 (arXiv 2601.20913) | https://arxiv.org/abs/2601.20913 | A small human calibration set estimates the judge's TPR/FPR, and a variance-corrected threshold on the large judge-labelled set gives finite-sample Type-I control. | technique-to-borrow (reporting) | Use the 244 + round-2 human labels to estimate Vintern's TPR/FPR per type. Then report a corrected estimate of the true-SUPPORTED share in the full 9-prop training budget, not the raw 63.1%. |
| 20 | **Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control** — A. N. Angelopoulos, S. Bates, E. Candès, M. I. Jordan, L. Lei | arXiv 2110.01052 (Ann. Appl. Stat. 2025) | https://arxiv.org/abs/2110.01052 | Threshold selection as multiple testing along a fixed monotone path, which gives finite-sample guarantees such as false-discovery or precision control. | technique-to-borrow | The textbook method for choosing θ_S^hi so that precision(SUPPORTED) ≥ target with probability 1−δ from ~300 labels. |

## (b) Overlap risks (max 5)

1. **IntroConformal (EMNLP 2026)**: claim-level LVLM factuality filtering with conformal guarantees. Medium. VSPS differs on four points: an external small Vietnamese verifier, an explicit UNCERTAIN state with neutralization, use for SFT data rather than inference-time abstention, and Vietnamese. Add one sentence to related work.
2. **DOCCI-Critique / VNLI-Critique (2025)**: sentence-level critic, then revise, for detailed captions. Low–medium. Their revise step is inference-time correction, while VSPS rebuilds training targets from typed atomic propositions.
3. **HalDec-Bench (2025-26)**: argues that a strong VLM can filter caption data to cut noise, which is close to VSPS's premise. Low (benchmark only, no typed props, no SFT). Cite it as supporting evidence.
4. **M-HalDetect reward-model rejection sampling**: filtering by a learned detector. Low. It ranks whole responses, not propositions.
5. No paper found that combines dual affirm/negate probes, a three-state verdict and supervision-data construction in a low-resource language. The novelty claim holds against this angle.

## (c) Must-compare baselines / must-cite (max 5)

1. **VL-RewardBench** + **Multimodal RewardBench**: cite them so the 63.1% audit precision reads as the norm (frontier judges reach ~65–72%) and not as a defect.
2. **System-Mediated Attention Imbalances … Say Yes** (Findings ACL 2026) + **VaPR**: 2025-26 evidence for yes-bias, which motivates the negated probe.
3. **Post-Hoc Debias / blank-image calibration** (2403.05262): cheapest baseline calibrator. A reviewer can ask "why not blank-image calibration?", so run it.
4. **HalLoc (CVPR 2025)** or **M-HalDetect** reward model: one learned detector as an alternative verifier on the 244 audited items.
5. **IntroConformal (EMNLP 2026)** / **Learn then Test**: cite for principled threshold choice. The current thresholds are untuned, and a TALLIP reviewer will spot `UNTUNED`.

## (d) Actionable improvements, ranked by expected gain / cost

1. **Tune thresholds per type on human labels, and report precision with a CI (Learn-then-Test style).**
   - What: finish the round-2 audit, so that about 150 machine-UNCERTAIN/REJECTED items join the 244 SUPPORTED (stratified by type). Write `scripts/tune_thresholds.py`: grid over (S_hi, C_hi) per type, keep the configs whose Clopper-Pearson lower bound on precision(SUPPORTED) ≥ target (e.g. 0.75), and among them maximise yield. Fill `VerificationConfig.per_type_thresholds` and bump `decision_rule_version` to `v1.1-dev-tuned`.
   - Effect: removes the "untuned" weakness. Precision of SUPPORTED is expected to rise to ~70–75% on counting/entity, at a cost of fewer SUPPORTED props, so recall may fall unless item 3 adds signal. The audit sample is reused, so the tuned thresholds must be evaluated on a held-out half (split by image).
   - GPU: 0. Verdicts only need re-deciding from cached probe records, assuming `replay.py` covers that, which it appears to.
   - Risk: about 400 labels is little for 5 types × 2 thresholds. Use one shared offset plus a counting/relation override instead of a full per-type grid.

2. **Replace K = 5 sampling with single-pass P(yes)/P(no) logits in Vintern.**
   - What: in `rescap/vlm/vintern.py`, bypass `.chat()` and run one forward pass through `model.language_model`. Read the next-token logits for the tokens "Có"/"Không" (and "Yes"/"No"), set `supports_logprobs = True`, and return the softmax over the pair.
   - Effect: a continuous V in place of the 6-level agreement fraction, which makes threshold tuning (item 1) meaningful. **Cost drops ~5x** (one forward pass with one generated token, versus 5 sampled generations), roughly 80 s/img down to about 15–20 s/img. Continuous scores usually rank better than sampled votes.
   - GPU: small engineering; re-verification runs at roughly 1/5 of the original time.
   - Risk: Vintern's chat template has to be reproduced exactly. Validate on 50 items that argmax(logit) equals the greedy chat answer.

3. **Blank-image (content-free) calibration for entity and attribute probes.**
   - What: in `verify.py`, after the direct probe, ask the same question on a gray 448×448 image once per proposition. This is cacheable per proposition text, because the answer does not depend on the image. Add a signal `prior_yes`, and use calibrated V' = V − prior_yes, or require V − prior_yes ≥ δ for SUPPORTED (Zhang et al. 2024, row 2).
   - Effect: targets the 22 entity and 14 attribute false SUPPORTEDs caused by language prior. My estimate is that a third to half of them have prior_yes ≥ 0.5. That is unmeasured: check on the 62 human-REJECTED items first (zero training, 1 forward pass per unique text).
   - GPU: under 10% extra time after caching (proposition texts repeat across images).
   - Risk: low. The rule is monotone and only lowers SUPPORTED to UNCERTAIN, consistent with the "ceiling may only lower" invariant.

4. **Heterogeneous second verifier, applied only to SUPPORTED candidates (cascade jury).**
   - What: add `rescap/vlm/registry.py` entries for Qwen2.5-VL-3B (or Vintern-3B-beta, Qwen2.5-3B + InternViT-300M, https://huggingface.co/5CD-AI/Vintern-3B-beta). In `verify.py`, keep SUPPORTED only if the second model also affirms the direct probe and rejects the negated one, and otherwise downgrade to UNCERTAIN (PoLL, row 14). Do not use Qwen2.5-VL-7B, the student, as a verifier: that is circular, and VaPR shows the same yes-bias.
   - Effect: precision gains from disagreement between model families. Recall falls only on SUPPORTED items, and the budgeted selection of 9 props can backfill. Expected +5–10 pts precision (estimate, test on the 244 audited items before full rerun).
   - GPU: about 6 GB in fp16 / 4-bit for 3B on the 3090. It runs only on SUPPORTED candidates, so roughly +30–50% verification time with logits (item 2).
   - Risk: Vintern-3B shares the InternViT encoder with Vintern-1B, so its errors are correlated. Prefer Qwen2.5-VL-3B for diversity.

5. **Region-cropped re-verification for attribute/action/counting with a bbox (ViCrop-style).**
   - What: where G already provides a subject bbox, re-ask the probe on the crop (expanded 1.5x) concatenated with the full image as a second tile. Vintern's dynamic tiling takes multiple tiles natively.
   - Effect: helps small subjects. Counting precision is the worst at 55.9%. Expect gains mainly on small-object attribute props.
   - GPU: one extra probe per eligible prop.
   - Risk: medium. A bad bbox can mislead the probe, so apply it only when the detector confidence is high.

6. **Position-bias and memorization diagnostics (report only).**
   - What: in `scripts/error_analysis.py`, measure SUPPORTED-rate and human-REJECTED rate by source-sentence index (HalDec-Bench) and by entity frequency. Optionally add a masked-object counterfactual for 50 entity props (POPEv2 style).
   - Effect: no metric gain, but it pre-empts reviewer questions about verifier bias.
   - GPU: negligible.
   - Risk: none.

7. **Report corrected precision under judge noise (Noisy-but-Valid / PPI).**
   - What: in `scripts/score_ci.py`, combine the per-type TPR/FPR from the human set with the type mix of the full selected set, and report the estimated true-SUPPORTED share of the training supervision with a CI.
   - Effect: a more honest and stronger headline. Relation is 2% of the selected content, so the weighted precision can differ from the raw 63.1%.
   - GPU: 0.
   - Risk: low.

## (e) Watch queries (re-run monthly)

1. arXiv listing cs.CV + cs.CL: `"yes bias" OR "acquiescence" vision-language model` (https://arxiv.org/a/ search; sort by date).
2. Semantic Scholar: `hallucination detector image captioning benchmark` (filter year ≥ 2025). Track citations of HalDec-Bench 2511.20515 and HalLoc 2506.10286.
3. Google Scholar alert: `"VLM-as-a-judge" OR "multimodal reward model" reliability hallucination`.
4. OpenAlex: `search=conformal factuality vision-language claims&filter=from_publication_date:2026-01-01`. Track citations of IntroConformal 2609.01375.
5. arXiv: `"atomic" claims verification caption "small" verifier calibration` and `Vietnamese vision-language hallucination`.
6. Hugging Face Papers: `token-level hallucination probe LVLM` (UniProbe / HaloProbe follow-ups).

## Unverified / not confirmed

- VaPR author list not opened. Cite from the arXiv page before use.
- The POPE yes-ratio effect sizes of the attention-redistribution intervention (row 1), and whether it is training-free, are not confirmed from the abstract.
- VNLI-Critique model size and weight availability are unknown.
- The Learn-then-Test journal venue (Ann. Appl. Stat.) comes from memory and was not opened. The arXiv ID is confirmed.
- All "expected effect" percentages in (d) are my estimates and have not been measured. Measure them on the 244 audited items first (zero GPU for items 1, 3, 6, 7 once probes are cached).
