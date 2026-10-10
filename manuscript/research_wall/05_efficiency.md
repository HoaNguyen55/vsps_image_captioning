# 05: Efficiency (cheaper verification, training and inference on one RTX 3090)

Agent 05, 2026-10-10. Angle: making verification and SFT cheaper, and how to report cost. VQAScore (P(yes) scoring) is already covered in `../novelty/07_vqa_verification_consistency.md` A3, so it is only referenced here and not listed again.

## 0. Where the time goes in the repo now (read from code)

**Verification (`rescap/pipeline/verify.py` -> `rescap/vlm/base.py` -> `rescap/vlm/vintern.py`)**
- `run_probe()` (verify.py ~L1430) asks each claim, and its negation when `contradiction_detection` is on, through `model.probe_yes_no(image, prompt, k=config.probe_k)`. A logged run shows `"probe_calls": 102` per image. With K=5 that is about 510 short generations per image, so 80 s/image works out to about 0.78 s per probe call.
- `VinternAdapter._generate_many()` already batches the K samples through `batch_chat`. But it does `batched = torch.cat([tiles] * n)`, so **InternViT runs K=5 times on identical tiles for every probe**. The ~1.8k-token prefill (6 tiles + thumbnail, about 256 tokens each, `max_tiles=6`) is also repeated 5x per probe and about 100x per image. `_pixel_values()` re-tiles the image on every call.
- `VinternAdapter.supports_logprobs = False`, because `chat()` returns only text. That is the only reason K=5 self-consistency exists (see the base.py docstring, "doc 08 §8.2"). The polarity decision is read from the **first token** ("có"/"không"). That token is available as a logit from one prefill, without any sampling.

**SFT (`scripts/train_stage2.py`)**
- NF4 4-bit with double quantisation, `attn_implementation="sdpa"`, `per_device_train_batch_size=1`, `gradient_accumulation_steps=8`, gradient checkpointing on, 512 vision tokens on 24 GB. LoRA r=16, alpha=32, on language-side q/k/v/o/gate/up/down only (the vision tower is frozen, which is correct).
- The cross-entropy step materialises full 152k-vocabulary logits in fp32. The collator re-opens and re-processes images every step, which is cheap next to the forward pass.
- 7.3 s/it × 1,800 steps is about 3.6 h. One "it" is 8 micro-batches, so about 0.9 s per example.

## (a) Papers

| # | Paper | Venue / year | ID (opened) | Method (1–2 sentences) | Relevance to VSPS | Action |
|---|---|---|---|---|---|---|
| 1 | **HALP: Detecting Hallucinations in Vision-Language Models without Generating a Single Token**. Kogilathota, Vallabha E G, Sun, Zhou | EACL 2026 (ACL Anthology) | arXiv:2603.05465 | Lightweight probes on internal states (visual features, vision tokens in the decoder, query-token states) across 8 VLMs predict hallucination risk before any token is generated; AUROC up to 0.93. | technique-to-borrow (verifier cost); overlap low | Supports "one forward per proposition, no sampling." Cite it as the motivation for the logit verifier (I1). |
| 2 | **The First Token Knows: Single-Decode Confidence for Hallucination Detection**. Gabriel, Wang | arXiv 2026 (CEUR-WS Vol-4254 version also exists) | arXiv:2605.05166 | First-token top-K normalised-entropy confidence from one greedy decode matches or beats sampling-based semantic self-consistency (mean AUROC 0.820 vs 0.793). | technique-to-borrow; text-only QA, so a transfer claim must be tested | Direct evidence that K=5 sampling can be replaced by a first-token distribution. Use it to justify the I1 ablation. |
| 3 | **An Image is Worth 1/2 Tokens After Layer 2 (FastV)**. Chen, Zhao, Liu, Bai, Lin, Zhou, Chang | ECCV 2024 (Springer LNCS) | arXiv:2403.06764 | Drops low-attention visual tokens after layer 2 of the LLM; 45% FLOPs reduction on LLaVA-1.5-13B with little accuracy loss. | technique (inference); risky for small-object recall | Optional for the verifier only. Do not apply to the captioner (see #6, #7). |
| 4 | **SparseVLM: Visual Token Sparsification for Efficient Vision-Language Model Inference**. Zhang, Fan, … Keutzer, S. Zhang | ICML 2025 (PMLR 267) | arXiv:2410.04417 | Training-free, text-guided visual-token pruning with per-layer rank-based ratios and token recycling; 54% FLOPs cut at 97% accuracy on LLaVA. | technique; text-guided suits question-conditioned probes | Text-conditioned pruning fits verification, where the query names the object. Cite it if the journal includes an efficient-verifier ablation. |
| 5 | **VisionZip: Longer is Better but Not Necessary in Vision Language Models**. S. Yang et al. | CVPR 2025 | arXiv:2412.04467 | Keeps a compact set of informative visual tokens before the LLM; 8× faster prefill on LLaVA-NeXT. | technique; must-cite in an efficiency paragraph | Cite it as the representative pre-LLM compression method. Low priority to implement (Vintern has only ~1.8k tokens). |
| 6 | **AgilePruner: An Empirical Study of Attention and Diversity for Adaptive Visual Token Pruning in LVLMs**. Baek, Song, Kim, Kong | ICLR 2026 | arXiv:2603.01236 | Diversity-oriented pruning retains less effective diversity than intended. On CHAIR, the retained diversity correlates with **more** hallucination than attention-based pruning; proposes adaptive pruning. | metric/benchmark (CHAIR under pruning); caution | If any pruning is used, report CHAIR and recall with and without it. Attention-based pruning gives conservative, lower-recall captions, the opposite of the R≥55 target. |
| 7 | **VASparse: Towards Efficient Visual Hallucination Mitigation via Visual-Aware Token Sparsification** | arXiv 2025 (search snippet only, not opened) | arXiv:2501.06553 | Reports that vision-agnostic sparsification worsens visual hallucination and proposes visual-aware sparsification. | caution | Cite it with #6: naive pruning can increase CHAIR. |
| 8 | **HiPrune** (training-free hierarchical-attention pruning); **ResPrune** (text-conditioned; 98.4% relative performance at 66.7% pruning on Qwen2.5-VL-7B, and notes that all methods retain less on Qwen2.5-VL than on LLaVA) | arXiv 2508.00553 (2025); arXiv 2603.21105 (2026) | search snippets | Training-free pruning evaluated on Qwen2.5-VL. | baseline evidence for "pruning on Qwen2.5-VL is lossy" | Do not prune the Qwen2.5-VL captioner, whose 512-token budget is already tight. A one-line citation is enough. |
| 9 | **Liger Kernel: Efficient Triton Kernels for LLM Training**. Hsu et al. (LinkedIn) | arXiv 2024 | arXiv:2410.10989 | Fused RMSNorm/RoPE/SwiGLU/FusedLinearCrossEntropy kernels; about +20% throughput and about −60% memory versus HF. | technique-to-borrow (SFT) | I3: one flag in `SFTConfig`. |
| 10 | **Which LoRA? An Empirical Study on the Effectiveness of LoRA Techniques During Multilingual Instruction Tuning**. Wijewardhana, Reyes, Ranathunga | arXiv, Jun 2026 | arXiv:2606.10428 | Basic LoRA vs four variants across diverse languages: "no significant advantage" for the complex variants. | must-cite (justifies keeping plain LoRA) | Use it to pre-empt "why not DoRA/PiSSA?" without spending GPU-days. |
| 11 | **PiSSA: Principal Singular Values and Singular Vectors Adaptation of LLMs**. Meng, Wang, Zhang | NeurIPS 2024 | arXiv:2404.02948 | Initialises the adapter from the principal SVD components and freezes the residual; faster convergence than LoRA in their tests. | optional ablation | Only if a reviewer asks. In PEFT it is `init_lora_weights="pissa_niter_4"`, but with 4-bit it needs the QPiSSA path. |
| 12 | **DoRA: Weight-Decomposed Low-Rank Adaptation**. S.-Y. Liu et al. | ICML 2024 (venue from a secondary source; confirm) | arXiv:2402.09353 | Splits the update into magnitude and direction (LoRA on direction). | optional; slower per step than LoRA | Do not adopt for cost reasons. Cite #10 instead. |
| 13 | **Dissecting the Runtime Performance of the Training, Fine-tuning, and Inference of LLMs** | arXiv 2023 | arXiv:2311.03687 | Benchmarks find LoRA has about 2× the throughput of QLoRA, because of quant/dequant overhead, at about 2× the memory. | cost-reporting evidence | Explains why QLoRA is slow on the 3090 and supports the bf16-LoRA control (`--no-4bit`). |
| 14 | **SmolVLM: Redefining small and efficient multimodal models**. Marafioti et al. (HF) | arXiv 2025 | arXiv:2504.05299 | A 256M–2.2B VLM family; 2.2B rivals VLMs that use twice the memory. | small-captioner baseline (English-centric) | A low-priority student candidate. For Vietnamese, prefer Qwen2.5-VL-3B or Vintern-3B (I6). |
| 15 | **MPIC: position-independent multimodal context caching** | arXiv 2025 | arXiv:2502.01960 | Caches multimodal KV on disk, independent of position; up to 54% lower response time. | technique (verification serving) | Not needed. Plain prefix caching covers VSPS, because every probe of one image shares the same image prefix. |

**Standard references (IDs from memory, not re-opened this session; verify before citing):** vLLM / PagedAttention (Kwon et al., SOSP 2023, arXiv:2309.06180); SGLang / RadixAttention (Zheng et al., NeurIPS 2024, arXiv:2312.07104); FlashAttention-2 (Dao, ICLR 2024, arXiv:2307.08691); QLoRA (Dettmers et al., NeurIPS 2023, arXiv:2305.14314, opened); Strubell et al., "Energy and Policy Considerations for Deep Learning in NLP" (ACL 2019, arXiv:1906.02243); Dodge et al., "Show Your Work" (EMNLP 2019, arXiv:1909.03004); Unsloth (software, no paper; its Qwen2.5-VL speed claims are project claims only).

**Unverified:** a CVPR 2026 poster on "When Token Pruning is Worse than Random" (DART/DivPrune with random pruning keeps about 94–97% of Qwen2.5-VL-7B at 50% pruning); arXiv ID not confirmed. Unsloth's "1.5–2× faster" figure is for vision RL, not SFT.

## (b) Overlap risks (max 5)

1. **None HIGH.** No 2025–2026 paper found does offline proposition verification for *training-data* construction with an efficiency focus.
2. **Low:** HALP (#1) and The First Token Knows (#2) occupy "cheap single-pass hallucination signals." If VSPS switches to logit verification it should cite both and frame its contribution as the three-state decision plus dual-polarity, not the cheap score itself.
3. **Low:** VQAScore (novelty/07 A3) already established P(yes) as a VLM scoring primitive. Do not claim P(yes) verification as new.

## (c) Must-compare / must-cite (max 5)

1. HALP (EACL 2026) and The First Token Knows (2026): single-pass confidence replacing sampling. Cite them in the verifier-cost paragraph.
2. Which LoRA? (2026): justifies plain LoRA over DoRA/PiSSA in a multilingual setting.
3. QLoRA plus the runtime-dissection paper (#13): justify the 4-bit choice and its speed cost honestly.
4. FastV / SparseVLM / VisionZip, with AgilePruner as the caution: one sentence on why the captioner's visual tokens are not pruned (recall target).
5. Strubell 2019 / Dodge 2019: the basis of the compute-reporting table.

## (d) Actionable improvements, ranked by expected gain/cost

The speed-ups below are **estimates** derived from the call structure above. Measure each one with `scripts/measure_latency.py`-style timing on 20 images before claiming it.

**I1. Logit-based three-state verification: one prefill per query, P(có) vs P(không) from the first-token logits, replacing K=5 sampling.** *Best idea.*
- Repo: in `rescap/vlm/vintern.py`, add a `_yes_no_logits(image, prompts)` path and set `supports_logprobs=True` for it. Build the InternVL query the way `chat()` does (template plus `IMG_CONTEXT` tokens), call `self._model.generate(pixel_values=..., input_ids=..., max_new_tokens=1, output_scores=True, return_dict_in_generate=True)`, and read softmax over the token ids of "có"/"Có" vs "không"/"Không". The remote `generate` forwards kwargs to `language_model.generate`; check this in the cached `modeling_internvl_chat.py`. In `rescap/vlm/base.py`, `probe_yes_no` gets a `ConfidenceMethod.TOKEN_PROB` branch. In `rescap/pipeline/verify.py`, `VerificationConfig` needs a `confidence_method` switch and recalibrated thresholds. The base.py docstring already warns that TOKEN_PROB and SELF_CONSISTENCY confidences are not comparable. INCONCLUSIVE becomes "P(có)+P(không) < τ_mass" or |margin| < τ, and acquiescence becomes "both direct and negated have P(có) > 0.5."
- Effect: cost drops from about 5 × (prefill + ~8 decode steps) to 1 prefill per query. The estimate is **5–10× on verification, 80 s to about 8–16 s/image**. It also gives a **continuous score**, so thresholds can be swept on the 600-proposition human audit to push SUPPORTED precision above 63.1%. That is a precision gain, not only a cost gain. It is deterministic, which also removes seed variance from the labels.
- GPU: about 1 h to implement and validate on the audit set. Re-verifying KTVIC train is then about 1/5–1/10 of the original run.
- Risk: medium. Labels change, so SFT must be re-run, and the paper must show agreement (Cohen's κ) between K=5 and logit verdicts on the audit set. Keep K=5 as the reported main configuration if κ is high and present logits as the efficient variant. If logits win on audit precision, switch.

**I2. Encode the image once per image, not once per probe sample.**
- Repo: in `vintern.py`, cache `pixel_values` per image (key: `id(image)` or the file path) instead of calling `_pixel_values()` per probe. Stop the K-fold `torch.cat([tiles] * n)` re-encoding by computing `vit_embeds = self._model.extract_feature(tiles)` once and passing `visual_features=` repeated across the batch, if the remote `generate` accepts it (InternVL2.5 code does; verify for Vintern-1B-v3_5). Pure engineering: outputs are identical.
- Effect: removes the 4/5 redundant InternViT passes per probe and about 100 redundant tilings per image. Estimated **1.3–2×** on its own. It stacks with I1, where the image is encoded once for ~100 queries.
- GPU: minutes. Risk: low. Regression test: same verdicts under fixed seeds on 5 images.

**I3. Batch all probes of an image into one forward (with I1), or serve Vintern through vLLM with prefix caching.**
- Repo: restructure the per-proposition loop in `verify.py` (L~2233) into collect all queries, then score them in one batch, then decide. The `batch_probe()` hook in base.py already exists for this. In-process HF with left padding is the lazy option. vLLM (`LLM(model="5CD-AI/Vintern-1B-v3_5", trust_remote_code=True, enable_prefix_caching=True)`, `SamplingParams(max_tokens=1, logprobs=20)`) shares the image-prefix KV across the ~100 queries automatically. KV for 100 × ~1.9k tokens on Qwen2-0.5B is about 2 GB, so it fits easily.
- Effect: with I1+I2, estimated **2–5 s/image (15–40×)**. Full KTVIC train re-verification goes from days to a few hours.
- GPU: half a day to port. Risk: medium. vLLM support for this exact checkpoint is unconfirmed (it is the InternVLChatModel architecture, so likely), and vLLM on WSL2 needs a working CUDA setup. Fall back to the HF batch.

**I4. Cheaper SFT: Liger kernel plus a larger micro-batch.**
- Repo, `scripts/train_stage2.py` `run_sft()`: add `use_liger_kernel=True` to `SFTConfig` (or `from liger_kernel.transformers import apply_liger_kernel_to_qwen2_5_vl; apply_liger_kernel_to_qwen2_5_vl()` before `from_pretrained`). FusedLinearCrossEntropy avoids the fp32 152k-vocabulary logits. Spend the freed memory on `per_device_train_batch_size=2, gradient_accumulation_steps=4` (same effective batch of 8, so the comparison stays fair) with `group_by_length=True`. Optionally install `flash-attn` and set `attn_implementation="flash_attention_2"`, which the 3090 (Ampere) supports. `qwen_vl.py` already probes for it, and `train_stage2.py` hard-codes `sdpa`.
- Effect: estimated **1.2–1.5× (3.6 h to about 2.5–3 h)** per run. No effect on quality, because the effective batch and LR are unchanged.
- GPU: one 50-step smoke run per change, about 10 min. Risk: low to medium (Liger version vs transformers 4.51.3 pin; check that the loss curve matches the old `metrics.jsonl` over the first 100 steps).

**I5. Stop training on wasted steps: early stopping on a small validation CHAIR/recall set.**
- Repo: `save_strategy="steps", save_steps=300`, plus a script that scores each checkpoint on 100 val images (reuse `scripts/evaluate.py`).
- Effect: if the recall/CHAIR curve plateaus before 1,800 steps (check the existing `metrics.jsonl` loss curve), runs can be cut 30–50%. It also gives the journal a "recall vs steps" figure, which bears on the recall drop (57.1 to 37.1). Recall falling with steps would show the template supervision over-trains brevity.
- GPU: about 0.5 h of eval per run. Risk: low.

**I6. Faster inference for evaluation: merged adapter plus vLLM for Qwen2.5-VL-7B; optional 3B student.**
- Repo: `scripts/coco_probe.py` already measured 11.8 s/image unmerged vs about 5.8 s merged. Merge with `merge_and_unload()` once, then run vLLM (Qwen2.5-VL is supported; AWQ or bf16 with `max_model_len` ~4k fits on 24 GB) with batched requests. Expected throughput is roughly 1 s/image or better, so 5,000 COCO images take about 1–2 h instead of about 8 h. A `--backend vllm` flag in `scripts/evaluate.py` is the minimal change.
- 3B student: the same SFT recipe on Qwen2.5-VL-3B-Instruct gives about 2× cheaper SFT and inference and answers the likely reviewer question "does VSPS depend on the 7B?" Run it only after I1–I5.
- Risk: vLLM greedy outputs can differ slightly from HF. Re-score one model both ways and report the CHAIR difference.

**I7. Tile budget for the verifier (`max_tiles`) as a cost/precision ablation.**
- Repo: `VinternAdapter(max_tiles=...)` is already a parameter. Run {1 (thumbnail only), 2, 6} on the human-audit images.
- Effect: going from 7 to 3 image blocks cuts prefill about 2×, but small objects may move to UNCERTAIN, which lowers supervision recall. Report it, and expect to keep 6.
- GPU: about 1 h. Risk: low (ablation only).

**Not recommended:** DoRA/PiSSA swaps (cost with no evidence of gain, see #10); FastV-style pruning of the Qwen2.5-VL captioner (works against the R≥55 target, see #6–#8); Unsloth (claims are not peer-reviewed and it patches the model, which hurts reproducibility of a journal artefact).

**How to report cost in the journal (one table plus one sentence).** Columns: stage | model | precision (NF4/bf16) | GPU | wall-clock | GPU-hours | per-unit cost (s/image or s/step) | one-time vs per-inference. Rows: proposition generation, verification (K=5, and logit if I1 is adopted), rendering (CPU), SFT, inference (HF vs vLLM). Add energy ≈ GPU-h × measured average board power (log `nvidia-smi --query-gpu=power.draw --format=csv -l 5` during runs; do not assume TDP). State the key point: **all verification cost is offline and amortised; inference is a single pass with zero verifier overhead**, compared with decoding-time methods. This follows Strubell 2019 / Dodge 2019 practice.

## (e) Watch queries (re-run monthly)

1. arXiv listing (cs.CV + cs.CL): `abs:(hallucination AND (single forward OR "without generating" OR logit OR "first token")) AND abs:(vision-language)`
2. Semantic Scholar: `efficient VQA verification yes/no probability vision-language 2026`
3. Google Scholar alert: `"visual token pruning" hallucination CHAIR`
4. Google Scholar alert: `"Qwen2.5-VL" QLoRA OR LoRA fine-tuning efficiency captioning`
5. OpenAlex search (`/works?search=`): `low-resource image captioning compute cost GPU hours`, filtered `from_publication_date:2026-01-01`
6. arXiv listing: `ti:(LoRA) AND abs:(multilingual OR low-resource) AND abs:(variant OR comparison)`
