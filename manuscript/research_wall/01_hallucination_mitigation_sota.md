# 01: Hallucination-mitigation SOTA for LVLM captioning (2025-2026)

Agent 01, written 2026-10-10. Angle: training-free decoding (successors of VCD, OPERA and DoLa), attention and visual-token re-weighting, activation steering, ICD/M3ID-style contrast, and lightweight training. For each method the question is whether a Q2 reviewer will expect it as a baseline, whether it runs on **Qwen2.5-VL-7B on one RTX 3090**, and whether it can be **stacked on top of the VSPS checkpoint** at inference.

Verification: every arXiv ID below was resolved with the arXiv API on 2026-10-10 (title, first author, date and comment field). Venue tags come from the arXiv comment or journal_ref unless noted. "Qwen2.5-VL code" means a Qwen2.5-VL path exists in the official repo (checked via the GitHub tree or README). It does not mean the paper merely reports Qwen2.5-VL numbers. Numbers are quoted from the paper's own tables (arXiv HTML) and are not comparable across papers: max tokens, prompts and CHAIR setups differ.

Already covered elsewhere and not repeated here: HALVA, RLAIF-V, HSA-DPO, OPA-DPO, CLAIM (cross-lingual attention), VECD (TMM 2026), and the VCD/OPERA/LURE/Woodpecker rows in `../Q2_LITERATURE.md`.

**What the repo already has.** `scripts/baselines.py` implements VCD (α=1, β=0.1, T=500) with a manual step-wise logits loop on HF Qwen2.5-VL, plus Self-Correction. The v10 Table III shows VCD barely moves KTVIC: P/R/F1 31.9/55.9/40.6 vs zero-shot 31.6/57.1/40.7, and hallucinated objects drop by about 3%.

---

## (a) Papers

### A. Classic baselines (2024-early 2025): reviewers still list these

| # | Paper | Venue | ID / code | Method (1 line) | Qwen2.5-VL code? | Relevance | Action |
|---|---|---|---|---|---|---|---|
| A1 | **VCD**: Mitigating Object Hallucinations in LVLMs through Visual Contrastive Decoding. S. Leng et al. | CVPR 2024 (IEEE) | arXiv:2311.16922; github.com/DAMO-NLP-SG/VCD (Qwen-VL only) | Contrast logits on the clean image vs a diffusion-noised image | Own impl. in `scripts/baselines.py` | baseline (have) | Keep. Cite A20 to explain why its gain on Qwen2.5-VL is small |
| A2 | **OPERA**: Over-Trust Penalty and Retrospection-Allocation. Q. Huang et al. | CVPR 2024 | arXiv:2311.17911; github.com/shikiw/OPERA (LLaVA-1.5) | Beam search with a penalty on "anchor-token" attention patterns and rollback | No. SAKED (B6) reports it "cannot be applied to Qwen2.5VL … due to architectural constraints", while ResDec (B5) does report OPERA on Qwen2.5-VL-7B | must-compare (commonly asked) | If the port is too costly, cite B5's Qwen2.5-VL OPERA number and state the limitation |
| A3 | **DoLa**: Decoding by Contrasting Layers. Y.-S. Chuang et al. | ICLR 2024 | arXiv:2309.03883; github.com/voidism/DoLa | Contrast final-layer logits with early-layer logits | HF `generate(dola_layers=…)` exists for decoder LMs. Not verified on Qwen2.5-VL (newer transformers versions moved it to a hub `custom_generate`) | baseline (cheap) | Try it. Note that B5 and B6 report DoLa *worsening* CHAIR on Qwen2.5-VL (B6: CHAIR_s 40.0 → 41.2) |
| A4 | **ICD**: Instruction Contrastive Decoding. X. Wang et al. | Findings ACL 2024 | arXiv:2403.18715 | Contrast against a "disturbance" system instruction | Trivial in our step loop | baseline (cheap) | Add as `--method icd` |
| A5 | **M3ID**: Multi-Modal Hallucination Control by Visual Information Grounding. A. Favero et al. | CVPR 2024 | arXiv:2403.14003 | Contrast with the image-free distribution, with weight growing over the generated length | Trivial in our step loop (text-only branch) | baseline (cheap) | Add as `--method m3id`. It targets long-caption drift, which is exactly the detailed-caption regime |
| A6 | **PAI**: Paying More Attention to Image. S. Liu et al. | ECCV 2024 (per official repo) | arXiv:2407.21771; github.com/LALBJ/PAI | Amplify attention to image tokens, plus contrast with the text-only logits | No | must-compare (most-cited attention baseline) | Port by patching the Qwen2.5-VL attention. Medium effort |
| A7 | **HALC**: Adaptive Focal-Contrast Decoding. Z. Chen et al. | ICML 2024 | arXiv:2403.00425; github.com/BillChan226/HALC | Grounding-based focal contrast plus beam | No. Needs a detector, which is heavy | cite only | — |
| A8 | **DAMRO**: Attention Mechanism to Reduce Object Hallucination. X. Gong et al. | EMNLP 2024 | arXiv:2410.04514 | Removes ViT outlier ("sink") tokens via contrast | No | cite | — |
| A9 | **VTI**: Reducing Hallucinations in LVLMs via Latent Space Steering. S. Liu, H. Ye, J. Zou | ICLR 2025 (proceedings page confirmed) | arXiv:2410.15778; github.com/shengliu66/VTI (LLaVA) | Pre-computed visual and textual steering vectors added to hidden states | No, but the port is easy (forward hooks) | baseline (steering family) | Candidate stackable baseline (see d4) |
| A10 | **SID**: Self-Introspective Decoding. F. Huo et al. | ICLR 2025 | arXiv:2408.02032 | Contrast with a pass that keeps only the least-informative visual tokens | No (A20 re-implements it on Qwen2.5-VL) | cite | — |
| A11 | **DeCo**: Dynamic Correction Decoding ("MLLM can see?"). C. Wang et al. | ICLR 2025 | arXiv:2410.11779; github.com/zjunlp/Deco | Mixes early-layer knowledge into the final logits | No Qwen path in the README. B6 reports DeCo on Qwen2.5-VL with ≈0 gain | cite | — |
| A12 | **MemVR**: Look Twice Before You Answer, Memory-Space Visual Retracing. X. Zou et al. | ICML 2025 | arXiv:2410.03577; github.com/1zhou-Wang/MemVR (Qwen-VL-Chat) | Re-injects visual tokens as FFN "key-value memory" when uncertainty is high | No (Qwen-VL v1 only) | baseline (efficient family) | Optional |
| A13 | **ICT**: Image-Object Cross-Level Trusted Intervention. J. Chen et al. | CVPR 2025 (venue from memory; arXiv comment blank, *unconfirmed*) | arXiv:2411.15268; github.com/THU-BPM/ICT | Activation shift on heads that encode image- and object-level trust | No | cite | — |
| A14 | **Nullu**: HalluSpace Projection. L. Yang et al. | CVPR 2025 | arXiv:2412.13817; github.com/Ziwei-Zheng/Nullu | Projects MLP weights onto the null space of a "HalluSpace" computed from truthful/hallucinated pairs | No (LLaVA, mPLUG, Qwen-VL-Chat) | cite; technique-to-borrow | It is a *weight edit*: zero inference cost, and can be applied to the merged VSPS weights |
| A15 | **AGLA**: Assembly of Global and Local Attention. W. An et al. | CVPR 2025 | arXiv:2406.12718 | Ensembles logits from the global image and a prompt-relevant masked local view | No | cite | — |
| A16 | **VASparse**: Visual-Aware Token Sparsification. X. Zhuang et al. | CVPR 2025 | arXiv:2501.06553 | Sparsifies visual tokens plus a sink penalty. Efficiency-oriented | No | cite | — |
| A17 | **ClearSight / VAF**: Visual Signal Enhancement. H. Yin et al. | arXiv 2025 (CVPR 2025 from memory, *unconfirmed*) | arXiv:2503.13107; github.com/ustc-hyin/ClearSight | Boosts attention to visual tokens in middle layers. No contrastive pass | No | cite | — |
| A18 | **DeGF**: Self-Correcting Decoding with Generative Feedback. C. Zhang et al. | ICLR 2025 | arXiv:2502.06130 | A text-to-image model renders the draft, and the render is used as contrast/feedback | No. Too heavy for a 3090 | cite | — |
| A19 | **TruthPrInt**: Latent Truthful-Guided Pre-Intervention. J. Duan et al. | ICCV 2025 | arXiv:2503.10602 | Learns a "truthful direction" in hidden states and intervenes before decoding | No | cite | — |

### B. 2025-H2 / 2026 methods (new ground)

| # | Paper | Venue | ID / code | Method (1 line) | Qwen2.5-VL evidence | Relevance | Action |
|---|---|---|---|---|---|---|---|
| B1 | **SPIN**: Mitigating Hallucinations in VLMs through Image-Guided Head Suppression. S. Sarkar et al. | arXiv 2025 (v2 Oct 2025; venue not stated) | arXiv:2505.16411; github.com/YUECHE77/SPIN (LLaVA, Qwen-VL v1) | For each query token, keep the top-K heads by image attention and suppress the rest in layers 1-16 | Paper Table 12, **Qwen2.5-VL-7B greedy: CHAIR_s 34.8 → 28.6, CHAIR_i 7.9 → 7.0, F1 75.7 → 74.0**. Throughput 1.8× vs alternatives | **baseline + stackable** | Best single-pass candidate for Table III. Port the head-mask to `Qwen2_5_VLAttention` |
| B2 | **ONLY**: One-Layer Intervention Sufficiently Mitigates Hallucinations in LVLMs. Z. Wan et al. | ICCV 2025 (IEEE; DOI 10.1109/ICCV51701.2025.00309 per CVF listing found via search) | arXiv:2507.00898; github.com/zifuwan/ONLY (LLaVA, Qwen-VL v1) | Text-to-visual entropy ratio selects heads in one layer. The enhanced logits are mixed with the original. 1.07× time | No Qwen2.5-VL numbers found | **must-compare** (2025 efficient SOTA, IEEE venue) | Port with one layer hook. Report latency against VCD |
| B3 | **VISTA**: The Hidden Life of Tokens, Visual Information Steering with Token-logit Augmentation. Z. Li et al. | ICML 2025 (PMLR v267) | arXiv:2502.03628; github.com/LzVv123456/VISTA (LLaVA-1.5) | Visual steering vector computed per-input + early-layer logit augmentation. About 40% less hallucination on open-ended generation | Not on Qwen2.5-VL | baseline (steering SOTA, frequently compared) | Optional port (hooks only) |
| B4 | **MaskCD**: Image Head Masked Contrastive Decoding. J. Deng et al. | Findings EMNLP 2025 | arXiv:2510.02790; github.com/Deng-Jingyuan/MaskCD | The amateur pass masks "image heads" instead of noising the image | LLaVA-1.5, Qwen-VL | cite | Drop-in replacement for the VCD amateur in our loop (low effort) |
| B5 | **ResDec**: Residual Decoding, History-Aware Residual Guidance. X. Chen et al. | CVPR 2026 (arXiv comment) | arXiv:2602.01047; no code found | Uses history of token-logit evolution to correct language-prior bias | **Qwen2.5-VL-7B, 128 tokens: Regular 30.6/8.4 (CHAIR_s/CHAIR_i), OPERA 28.4/7.6, ICD 30.9/8.3, VCD 27.9/7.8, DoLa 28.2/8.9, ResDec 25.8/6.8** | must-cite (gives a ready Qwen2.5-VL baseline table) | Cite as external evidence that CD gains on Qwen2.5-VL are 1-3 pts CHAIR_s |
| B6 | **SAKED**: Stability-Aware Knowledge Enhanced Decoding. Z. Li et al. | arXiv 2026 (Feb) | arXiv:2602.09825; no code found | Layer-wise knowledge-stability score; contrasts the most-stable and least-stable layers | **Qwen2.5-VL (7B-scale): Greedy 40.0/9.8 (CHAIR_s/CHAIR_i), Beam 36.0/8.4, DoLa 41.2/11.0, DeCo 38.8/9.4, SAKED 32.2/7.6**. AMBER Hal-Rate 16.1 → 14.4 | cite; evidence | **Beam alone gives −4 CHAIR_s on Qwen2.5-VL**, so run it as a free ablation |
| B7 | **ACG**: Attention-space Contrastive Guidance. Y. Jo et al. | CVPR 2026 Findings | arXiv:2601.13707 | Image-conditioned and approximate text-only attention paths inside **one** forward pass, plus orthogonal projection. Up to 2× faster than multi-pass CD | No Qwen2.5-VL found | baseline-to-watch | Single-pass contrast is the right efficiency story against our 2-pass VCD |
| B8 | **DMAS**: Dynamic Multimodal Activation Steering. J. Yin et al. | ICLR 2026 (arXiv comment + ICLR virtual poster) | arXiv:2602.21704 | Database of truthfulness steering vectors keyed by semantics, plus visual-perception vectors on selected heads | Mentions Qwen2.5-VL and InternVL3 | cite (2026 steering SOTA) | — |
| B9 | **AFTER**: Adaptive Factual-Guided Activation Editing. T. Wang et al. | ICLR 2026 (journal_ref) | arXiv:2601.01957; code "will be released" | Factual-text-guided steering plus a query-adaptive offset estimator. Up to 16.3% less AMBER hallucination | Three LVLMs, not identified as Qwen2.5-VL | cite | Its idea of "factual text as steering guidance" mirrors VSPS's verified propositions (see d6) |
| B10 | **CAST**: Caption-Guided Visual Attention Steering. Q. Li et al. | arXiv 2026 (May) | arXiv:2605.04641; no code found | SVM probe finds heads sensitive to caption queries (K=100). Adds α·(mean shift) to those heads. ~1.0× latency | **Qwen2.5-VL-7B: CHAIR_s 37.2 → 32.6, CHAIR_i 8.7 → 8.0** | technique-to-borrow | Probe data = 1k images × {caption, non-caption} queries, cheap on a 3090 |
| B11 | **LTS-FS**: Locate-then-Sparsify, Attribution-Guided Sparse Feature Steering. T. Dang et al. | CVPR 2026 | arXiv:2603.16284; github.com/huttersadan/LTS-FS (Qwen-VL-Chat VTI) | Causal-intervention attribution per layer sets the steering strength per layer (fixes uniform VTI/Nullu) | Mentions Qwen2/2.5-VL | cite | — |
| B12 | **AIMS**: Adaptive Multi-Context Steering. S. Ma et al. | arXiv 2026 (8 Oct) | arXiv:2610.11907; **github.com/VisionXLab/AIMS has a `qwen2_5vl/` patch + CHAIR/AMBER scripts** (3B in the README; also Qwen3.5-9B) | Head-wise steering of the query vector using visual, prefilled-text and generated-context prototypes. No extra pass | Qwen2.5-VL-3B main results | **runnable baseline today** | The only 2026 method with drop-in Qwen2.5-VL code. Try it on 7B (path change) |
| B13 | **CHASD**: Language Increment-Calibrated Contrastive Decoding. X. Huang et al. | arXiv 2026 (May) | arXiv:2605.23344 | Contrast runs **only** when next-token max-prob < threshold, using a localized perturbation of salient visual tokens | Qwen2.5-VL listed | technique-to-borrow | A confidence gate on our VCD cuts its 2× cost (see d3) |
| B14 | **VGD**: Hallucinations Leave a Grounding Signature, Verifier-Guided Decoding for Selective Object Correction. L. Yang et al. | arXiv 2026 (Jul) | arXiv:2607.27823; no code found | ℓ1-logistic verifier on per-head signed attention at each **object mention**. On high risk: roll back the KV cache, ban the object + synonyms, regenerate | Qwen2-VL-7B: CHAIR_i/CHAIR_s 8.6/27.4 → 4.7/15.8 at **unchanged length (86)**. AMBER Cover 68.4 → 55.6 @rec90 | **technique-to-borrow (best fit)**; overlap low | See d1 |
| B15 | **HaloProbe**: Bayesian Detection and Mitigation of Object Hallucinations. R. Zohrabi et al. | arXiv 2026 (Apr) | arXiv:2604.06165 | Token-level hallucination posterior that factors in position and repetition confounders (shows attention statistics suffer Simpson's paradox). Used as an external scorer to guide decoding | Qwen3-VL, InternVL3.5 | technique-to-borrow | Use its confounders (position, repetition) as features in d1 |
| B16 | **SADT / HARM+VEED**: Put Logit-Lens over Visual Attention to Detect and Mitigate LVLM Object Hallucination. Z. Wang et al. | CVPR 2026 Highlight | arXiv:2608.07302; github.com/wzczc/SADT ("code will be available") | Logit-lens decoding of high-attention regions detects hallucinated objects, then masks regions or does evidence-enhanced decoding | LLaVA-1.5, Qwen2-VL | cite | — |
| B17 | **GIFT**: Capturing Gaze Shifts for Guidance, Cross-Modal Fusion Enhancement. Z. Qi et al. | ICML 2026 | arXiv:2510.22067; github.com/amazon-science/GIFT | Saliency map from positive attention shifts while reading the query; amplifies salient visual and query tokens | Qwen2-VL-7B, Qwen3-VL-8B | cite | — |
| B18 | **MGAP**: Uncertainty-Aware Subspace Rectification. Y. Zhuang et al. | ICML 2026 | arXiv:2606.09859; github.com/ZJU-OmniAI/MGAP | SVD language-prior subspace from blind (image-free) hidden states; gated projection removes it | Qwen3-VL-8B | cite | — |
| B19 | **QK Product Steering**: Spectral QK-weight steering. K. Tiwari et al. | COLM 2026 workshop | arXiv:2606.20419 | One-time weight edit of dominant symmetric QK modes; zero inference cost | Qwen2.5-VL-7B CHAIR_s 31.44 → 28.56 (−4% avg relative) | cite | Weight edit, stackable |
| B20 | Others, cite only if space allows: DCLA (arXiv:2505.12343, layer aggregation, Qwen2.5-VL MME +42.6); MRFD (EMNLP 2025, arXiv:2508.10264, multi-region JSD fusion, multi-pass); AIR (CVPR 2026 Findings, arXiv:2603.24058, github.com/Ice-wave/AIR); PADE (arXiv:2602.15556); region-aware recalibration (arXiv:2605.24957); FADE (arXiv:2606.29431, FFN attenuation, LLaVA-family only); OSGA (arXiv:2601.23041, one-shot steering vector); per-instance disentangled subspaces (BMVC 2026, arXiv:2608.09344) | | | | | cite-only | — |

### C. Evidence on how robust these baselines are

| # | Paper | Venue | ID / code | Finding | Relevance |
|---|---|---|---|---|---|
| A20 | **Rethinking the Effectiveness of Contrastive Decoding in Mitigating Hallucinations in MLLMs**. A. Bendre, G. Gupta, S. Modi, K. Grover, C. Aggarwal | NeurIPS 2026 Workshop VLM4RWD (per repo; **no arXiv ID found**) | github.com/Aurnawr/Rethinking-CD | **Qwen2.5-VL-7B CHAIR (500 COCO): Sample 31.2/10.4, VCD 28.8/8.9, SID 29.6/9.9, APC-only 23.5/7.5, Greedy 22.8/7.3 (CHAIR_s/CHAIR_i)**. Greedy beats every CD method on every model. The CD "gain" comes from the plausibility constraint pushing generation toward greedy, and the contrast amplifies hallucinated tokens more often than it suppresses them. Runs on a single 24 GB L4 | **Key defence**: our VCD ≈ zero-shot result (v10 Table III) is the expected outcome, not a bug. Cite it, and report greedy as the reference (we already decode greedily) |
| A21 | **Delve into Visual Contrastive Decoding for Hallucination Mitigation of LVLMs**. Y.-L. Lee, Y.-H. Tsai, W.-C. Chiu | arXiv 2024 | arXiv:2412.06775; github.com/YiLunLee/VCD_Analysis | The effect of contrastive samples "varies a lot across LVLMs and benchmarks" | Supports the same point |

### D. Lightweight training (borrowable into VSPS's SFT)

| # | Paper | Venue | ID / code | Method | Relevance | Action |
|---|---|---|---|---|---|---|
| D1 | **REVERSE**: Generate, but Verify, Retrospective Resampling. T.-H. Wu et al. | NeurIPS 2025 | arXiv:2504.13169; github.com/tsunghan-wu/reverse_vlm; HF `tsunghanwu/reverse_qwen25_vl` (3B) + `reverse-instruct-1.3m` | Trains with `<SPAN>…</CN>` / `</UN>` tags marking confident vs unconfident phrases. At inference, an `</UN>` probability above τ triggers backtracking and resampling | **Overlap medium**: phrase-level confident/unconfident labels in the SFT targets, close to VSPS's SUPPORTED/UNCERTAIN, but REVERSE resamples at inference and VSPS neutralizes in the data. Qwen2.5-VL-3B: CHAIR_i/CHAIR_s 12.2/45.8 → 10.5/39.4, AMBER Cover 51.7 → 51.5. Correction costs up to ~3× tokens | **Must-cite & contrast**. A public Qwen2.5-VL checkpoint makes it runnable as a COCO baseline (English) |
| D2 | **Reducing Object Hallucination in LVLMs via Emphasizing Image-negative Tokens**. M. Shen et al. | arXiv 2026 (May) | arXiv:2605.21300 | Labels each response token image-positive, invariant or negative by its logit change between a clean and a noisy image, reweights the SFT loss per token, and filters hallucination-prone samples. No inference cost | LLaVA-v1.5 + LoRA; technique-to-borrow | See d5 |
| D3 | **Language Bias in LVLMs: From In-Depth Analysis to Simple and Effective Mitigation (LBR/LBP)**. Y. Chen et al. | ICML 2026 | arXiv:2605.25036; github.com/lab-klc/LVLM-Language-Bias | A language-bias regularizer in instruction tuning (LBR) and a bias penalty in DPO (LBP) | technique-to-borrow | LBR could be added to the QLoRA loss |
| D4 | **ViHallu**: See Different, Think Better, Visual Variations. Z. Dai et al. | ACM MM 2025 (ACM) | arXiv:2507.22003; github.com/oliviadzy/ViHallu | Fine-tunes on edited image variations with matched instructions | low overlap | cite |

---

## (b) Overlap risks (max 5)

1. **REVERSE (D1), medium.** Phrase-level "confident vs unconfident" supervision written into the SFT targets. A reviewer may say "VSPS's UNCERTAIN = REVERSE's `</UN>`." Distinguish VSPS in three ways. Its labels come from an *external offline verifier* with dual polarity and K=5 voting. UNCERTAIN content is *neutralized into a still-true statement*, not flagged for resampling. Deployment is strictly single-pass with no backtracking.
2. **VGD (B14), low-medium.** "Object-level verifier → selective correction" is the inference-time twin of VSPS's training-time verify-then-select. Frame it as complementary (see d1), not as a competitor.
3. **AFTER (B9), low.** Uses "factual textual semantics" to guide activation editing. It sounds similar to "verified propositions", but it uses steering vectors, not SFT targets. Mention it in one sentence.
4. No 2025-2026 decoding or steering paper found that targets Vietnamese, gender attribution, or proposition-typed supervision. CLAIM (ACL 2025, already covered) remains the only multilingual decoding method.
5. Not a reviewer-overlap risk but a positioning risk. Most 2026 papers report on LLaVA-1.5. Qwen2.5-VL baselines are scarce and inconsistent: vanilla CHAIR_s ranges from 22.8 (A20) to 40.0 (B6) depending on prompt and length. Never mix their numbers with ours. Re-run on our harness or cite the trend only.

## (c) Must-compare baselines / must-cite (max 5)

1. **SPIN (B1) or ONLY (B2)**: one single-pass attention/head method with near-zero overhead. SPIN has published Qwen2.5-VL-7B numbers; ONLY has an ICCV/IEEE venue. Pick one to run, cite both.
2. **PAI (A6)**: the attention-amplification baseline almost every 2025-26 paper lists. If it is not run, a reviewer will ask for it.
3. **OPERA (A2) + DoLa (A3) + ICD (A4)**: run the cheap ones (DoLa, ICD, and M3ID) in `scripts/baselines.py`. For OPERA, cite B5's Qwen2.5-VL number and the B6 statement about architectural constraints.
4. **Rethinking-CD (A20) + ResDec/SAKED tables (B5, B6)**: cite them to pre-empt "your VCD is weak". Training-free CD moves Qwen2.5-VL CHAIR_s by only 1-3 points and can be worse than greedy.
5. **REVERSE (D1)**: closest training-plus-verification method with a public Qwen2.5-VL checkpoint. Run it on COCO-English, or at least cite and contrast it.

## (d) Actionable improvements for VSPS (ranked by expected gain/cost)

GPU notes for all items: Qwen2.5-VL-7B in bf16 is about 16-17 GB of weights, so it fits a 24 GB 3090 for batch-1 inference. Methods that read attention need `attn_implementation="eager"`; cap `max_pixels` (e.g. 512×28×28) to keep the eager attention maps within memory. Cost figures below are estimates, not measurements.

**d1. Recall knob + selective object verifier at inference (VGD/HaloProbe-style). Best gain/cost; targets R ≥ 55 with F1 > 40.7.**
- *Change.* Retrain VSPS with a larger budget (more propositions per caption, e.g. 9 → 14 in `rescap/pipeline/select.py`) to push recall back toward zero-shot. Then cut hallucination at inference with a tiny probe. Add `scripts/train_mention_probe.py`: run the VSPS checkpoint on about 1-2k *training* images; at every object-lexicon mention token (reuse `rescap/chair.py` / `rescap/vi/lexicon.py`), log per-head image-attention mass, sink attention, token prob/entropy, position and repetition (B15 confounders). Label each mention by our existing gold/CHAIR matcher, or by the Vintern verdicts already cached. Fit an ℓ1 logistic regression (sklearn). At inference (`rescap/vlm/qwen_vl.py`), add a custom loop: when a mention scores above threshold, roll back to the mention start, ban that lemma and its synonyms (`bad_words_ids`), and continue.
- *Effect.* VGD reports CHAIR_s −42% relative at unchanged length on Qwen2-VL, with coverage partly kept (68 → 56 Cover @rec90). Combined with a higher-budget model, this is the most plausible route to lifting R while holding precision. It also adds a natural "the verifier signal is reused at test time" story.
- *Cost.* Probe data takes about 1-2 GPU-h; fitting takes seconds. Inference is roughly 1.2-1.6× greedy (VGD: 1.61× on LLaVA). Retraining is one QLoRA run.
- *Risk.* Medium. Vietnamese multi-syllable object mentions need span-to-token alignment (the lexicon matcher already handles syllables). VSPS is no longer purely "single-pass", so report both modes.

**d2. Single-pass head intervention stacked on VSPS (SPIN / ONLY / CAST). Cheap, and serves as both baseline and add-on.**
- *Change.* Add a `--intervene {spin,only}` flag in `rescap/vlm/qwen_vl.py` that monkey-patches `Qwen2_5_VLAttention.forward`. SPIN keeps the top-K heads by image-attention per query token in layers 1-16 (paper: r=0.02, α=0); ONLY works in a single layer. Run it on zero-shot (as a baseline) **and** on the VSPS checkpoint (stacking).
- *Effect.* SPIN on Qwen2.5-VL-7B: CHAIR_s −6.2 points with F1 −1.7. Expect a similar relative CHAIR drop on top of VSPS, with a small recall cost. It also gives Table III a 2025 baseline that is not CD.
- *Cost.* About 1 day of engineering. Inference ≈1.0-1.1× greedy (eager attention is slower than SDPA). Under 1 GPU-h for the KTVIC test set.
- *Risk.* Low-medium. Head counts and GQA layout differ from LLaVA, so tune K on val only.

**d3. Cheap decoding baselines + beam ablation in the existing loop.**
- *Change.* In `scripts/baselines.py`, add `--method {icd,m3id,maskcd,beam}`, reusing `stream_state`/`step_logits`. ICD swaps the prompt; M3ID uses an image-free branch with a length-growing weight; MaskCD masks image heads as the amateur. Add a CHASD-style gate to VCD: only contrast when max-prob < τ. For beam, just `num_beams=3` on zero-shot and VSPS. Time each with `scripts/measure_latency.py`.
- *Effect.* Rounds out Table III with 4-5 baselines at almost no cost, plus a "VSPS + beam" row. SAKED shows beam alone gives −4 CHAIR_s on Qwen2.5-VL. The gate also answers the "2 passes/image" cost criticism of VCD.
- *Cost.* Half a day of engineering; about 1-2 GPU-h per method on KTVIC test.
- *Risk.* Low. Expect small gains, consistent with A20, which is fine as a negative baseline.

**d4. Zero-cost weight/steering edit on the merged VSPS model (VTI / Nullu / QK-steering style).**
- *Change.* Add `scripts/steer_vectors.py`. On about 500 train images, compute the mean hidden-state difference between the VSPS model's activations on *SUPPORTED-only* rendered captions and on raw zero-shot captions that contain REJECTED propositions. The VSPS pipeline already produces both. Add the vector via a forward hook (VTI-style), or project it out of the MLP weights (Nullu-style).
- *Effect.* Uncertain, likely small (literature: −4 to −15% relative CHAIR). It is novel in using verifier-labelled pairs from our own pipeline as steering data, which gives a neat "propositions supervise both weights and activations" angle.
- *Cost.* About 1 GPU-h. Zero inference overhead.
- *Risk.* Medium, from the usual steering fragility. Hooks on top of a QLoRA adapter need the adapter merged first.

**d5. Visual-dependence token weighting in the SFT loss (D2), optionally weighted by verdict.**
- *Change.* In `scripts/train_stage2.py`, precompute per-token visual dependence on the training captions: one extra forward pass with a noised image, cached to disk. Up-weight image-positive tokens and down-weight invariant ones. The cheaper variant reuses the span→proposition trace: weight tokens in SUPPORTED entity/count spans higher (e.g. 1.5×) than template glue.
- *Effect.* Targets recall: more gradient on content tokens should raise object mentions without adding unverified content. D2 reports lower hallucination at unchanged length on LLaVA. Expected change on our metrics is unknown.
- *Cost.* The precompute takes about the time of one inference pass over the training set (a few GPU-h on a 3090), or zero for the trace-weight variant. Training cost is unchanged.
- *Risk.* Medium. Changing the loss affects every ablation comparison, so run it as a separate row.

**d6. Run AIMS and REVERSE as off-the-shelf external baselines (COCO-Vietnamese and English COCO).**
- *Change.* Clone VisionXLab/AIMS and point `qwen2_5vl_chair.py` at Qwen2.5-VL-7B with our Vietnamese prompt. Run `tsunghanwu/reverse_qwen25_vl` (3B) on English COCO only, labelled as a different backbone size.
- *Effect.* Gives one 2026 steering baseline and one training+verification baseline with real code, which closes the "no recent baselines" gap.
- *Cost.* About 2-4 GPU-h each.
- *Risk.* AIMS was released 2 days ago (0 stars) and REVERSE is a 3B English model, so state these caveats explicitly.

## (e) Watch queries (re-run monthly)

1. arXiv listing (cs.CV + cs.CL), API: `search_query=abs:hallucination AND abs:(decoding OR steering OR intervention) AND abs:("Qwen2.5-VL" OR "Qwen3-VL")&sortBy=submittedDate`
2. Semantic Scholar: `training-free object hallucination mitigation large vision-language models CHAIR AMBER` (filter year ≥ 2026, sort by citation count, to see which 2026 methods become the de-facto baselines)
3. Google Scholar alert: `"object hallucination" ("contrastive decoding" OR "attention head" OR "activation steering") "Qwen2.5-VL"`
4. Google Scholar alert: `hallucination detection "object mention" verifier rollback OR backtracking decoding vision-language` (tracks VGD/REVERSE-style selective correction, which is d1)
5. OpenAlex: `title_and_abstract.search:hallucination vision-language decoding` with `from_publication_date:2026-01-01`, filtered by venue to IEEE TMM, TCSVT, TIP, Pattern Recognition, ACM TOMM and TALLIP (the journal-version competitors)
6. GitHub search: `hallucination qwen2.5-vl` and `contrastive decoding qwen2_5_vl`, sorted by recently updated (new runnable code)

## Unverified

- Venues of ICT (A13) and ClearSight (A17) as CVPR 2025 are from memory; their arXiv comments are blank.
- ONLY's DOI comes from a search-result snippet of the CVF listing; the DOI page itself was not opened.
- Whether HF `generate(dola_layers=…)` runs on Qwen2.5-VL in the installed transformers version.
- Whether the OPERA port to Qwen2.5-VL is feasible. B5 reports OPERA numbers on Qwen2.5-VL-7B while B6 says it is inapplicable, so the claims conflict.
- A20 has no arXiv ID; the workshop acceptance claim comes only from its README.
