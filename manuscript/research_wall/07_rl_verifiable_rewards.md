# 07: RL and verifiable rewards for captioning (2025-H2 / 2026)

Agent 07, 2026-10-10. Scope: GRPO/RLVR for captions, QA-derived rewards, precision/recall (hallucination/omission) rewards, self-correction RL, and length/hedge control. Also a feasibility and collision check for a small **VSPS-GRPO** stage on one RTX 3090.

**Not repeated here.** These are covered in `../novelty/08_preference_rl_captioning.md`: RLAIF-V, HSA-DPO, FGAIF, SENTINEL, AVES-DPO, OSCAR, OPA-DPO, nSFT, CCCaption, VES-RFT, ClaimDiff-RL, VCap, RubiCap, CapRL, CuRe, COPO, SAVOR, SEED, REVERSE. I add new facts about them only where they matter (ClaimDiff-RL hedge penalty, CCCaption reward drift, CapRL++).

**How I verified.** Every arXiv ID was resolved through the arXiv export API (title, authors, date, comment field). For BalCapRL, SC-Captioner and ClaimDiff-RL I also opened the arXiv HTML full text. For the AAAI paper I opened the AAAI OJS page. Venues come from the arXiv comment field unless marked otherwise. I did not check Scopus/Q-ranks per paper; "Scopus" marks venues that are normally indexed.

---

## (a) Papers

| # | Paper (authors) | Venue / ID | Method (1–2 sent.) | Relevance | Action for VSPS |
|---|---|---|---|---|---|
| 1 | **BalCapRL: A Balanced Framework for RL-Based MLLM Image Captioning** (S. Ye, V. Saveris, Y. Qian, J. Hu et al.) | arXiv:2605.07394 (2026, no venue) | Three continuous rewards, computed per rollout by GPT-4o-mini: precision (fraction of atomic assertions that are visually verifiable and "pointable"), recall (coverage of reference units) and linguistic quality. They are combined with **c-GDPO**, which normalizes each reward per group, plus **length-conditional reward masking**: the linguistic reward is zeroed unless 0.5 ≤ len_pred/len_ref ≤ 2. Uses G=8, 8×B200 GPUs, and 24–46 h on Qwen2.5-VL-3B/7B. | **Overlap medium–HIGH** for any "precision+recall reward" claim. Technique to borrow. | Copy per-reward group normalization and the length mask into a VSPS-GRPO stage. Cite it as the closest precision/recall RL design. |
| 2 | **GDPO: Group reward-Decoupled Normalization Policy Optimization for Multi-reward RL Optimization** (S.-Y. Liu, X. Dong, X. Lu, S. Diao et al., NVIDIA) | arXiv:2601.05242. ICML 2026 per the ICML virtual poster page 63333 seen in search (arXiv comment says "NVIDIA-Tech Report") | Shows that GRPO on a *summed* multi-reward collapses distinct reward combinations into identical advantages. GDPO normalizes each reward within the group, then aggregates. | Technique to borrow (about 5 lines of code). | Normalize precision, recall and gender rewards separately, then add them. |
| 3 | **SC-Captioner: Improving Image Captioning with Self-Correction by Reinforcement Learning** (L. Zhang, X. Zeng, K. Li, G. Yu, T. Chen) | ICCV 2025 (IEEE/CVF, Scopus). arXiv:2508.06125 | Two-turn setup: caption → self-corrected caption. The reward parses both into object/attribute/relation sets (FACTUAL) and matches the added and removed elements against the reference, giving a *correctness bonus* for right edits and a *mistake punishment* for wrong ones. Uses policy gradient with KL and LoRA on Qwen2-VL-7B and LLaVA-1.5-7B. On DOCCI500 it beats SFT+DPO (CAPTURE 63.34 vs 62.51). Also releases RefinedCaps (6.5K COCO). | Overlap low: two passes at inference, reference-matched rewards. Baseline for "RL beats DPO". | Cite in §IV-9: an independent report that set-difference RL beats DPO for captions, consistent with VSPS's DPO failure. |
| 4 | **Re³Cap: Retrieval-Guided Refinement for Image Captioning Enhancement via RL** (H. Jia, S. Dong, Z. Sun, J. Zheng et al.) | EMNLP 2026 Main (per arXiv comment; ACL, Scopus). arXiv:2608.21305 | A Caption Refinement Suggester and a Caption Quality Assessor use multimodal retrieval to flag hallucinations and omissions during RL. Reports +8.64% relation reasoning over GRPO on COCO-LN500. | Overlap low. | Optional citation. |
| 5 | **Cross-modal Identity Mapping (CIM): Minimizing Information Loss in Modality Conversion via RL** (H. Jia, S. Dong, X. Dong, Z. Sun et al.) | CVPR 2026 (per arXiv comment; IEEE, Scopus). arXiv:2603.01696 | The RL reward is the similarity between the input image and images retrieved by text search using the caption. No annotations needed. | Overlap low. Reference-free omission signal. | Optional citation. Not usable for Vietnamese without a vi text→image retriever. |
| 6 | **A Glance Is All You Need: Single-Pass Fine-Grained Image Captioning with SimLoss** (S. Jain, R. Barkur, V. G, R. Rossi et al.) | arXiv:2609.00591 (2026) | InfoNCE between the projected hidden state and a frozen image embedding. Comes in a differentiable variant (FFT) and a GRPO variant with black-box reward. FFT gets the best precision; GRPO gets the best recall. Claims to roughly match a multi-stage verify-and-rewrite pipeline at about 20× lower latency. | **Overlap medium on the framing** "single-pass instead of multi-stage verification". Baseline candidate. | Must-cite for the single-pass argument. It compares *against* multi-stage verification pipelines, exactly what a reviewer will cast VSPS as. |
| 7 | **SD-GRPO: Verifiable Segment Decomposition for Long-Form Vision-Language Generation** (H. Kim, S. Lee, H. Yun, J. Park et al.) | arXiv:2606.09871 (2026) | Z-normalizes *per-segment* verifiable rewards across the rollout group, so each segment gets its own advantage instead of one scalar. Shows that rollout-level credit misattribution grows with output length. | Technique to borrow. | VSPS outputs already split into proposition-traceable sentences. Per-sentence advantages are natural for "this sentence names a REJECTED object". Use as phase-2 credit assignment. |
| 8 | **Controllable Image Captioning with Prompt-Conditioned Scene Rewards (FoCUS)** (J. Hyun, T. Kim, H. Kim) | EMNLP 2026 Main (per arXiv comment). arXiv:2609.00709 | GRPO with scene-graph-aligned component scores (object/attribute/relation), weighted per control prompt and including negative weights. Uses a stricter object-validity threshold and reasoning-based verification. Introduces the SCoPE benchmark with Include/Avoid constraints. | Overlap low–medium (typed component rewards). | Its "Avoid" negative weights are analogous to penalizing REJECTED propositions. Optional citation. |
| 9 | **Momentum-Coupled Rubric Adaptation for Detailed Image Captioning (MoCo Rubric)** (Z. Ji, L. Jin, S. Wang, J. Lu et al.) | arXiv:2609.36893 (29 Sep 2026) | One shared-parameter VLM plays policy, rubric generator and rubric judge. Only the policy gets GRPO updates; the judge and generator follow it through an EMA momentum model. | Overlap low. | Watch only. Shows the field moving to self-judging online rubrics, which is the opposite of VSPS's frozen offline verdicts. |
| 10 | **CapRL++: Unified RLVR for Dense Image and Video Captioning** (P. Yang, L. Xing, X. Dong, Y. Zang et al.) | arXiv:2606.09393 (2026). Extends CapRL (ICLR 2026) | Reward is the accuracy of a vision-free LLM answering MCQs from the caption alone. Covers more than 20 image and video benchmarks. Compact models are reported comparable to Qwen2.5-VL-72B on Prism. The abstract explicitly frames SFT as the limitation. | Overlap low. **Must-cite for positioning**, since it argues SFT memorizes. | Answer the argument in the related-work section: SFT on *verified* targets versus SFT on gold. |
| 11 | **The Devil is in the EOS: Sequence Training for Detailed Image Captioning** (A. Mohamed, Y. Kementchedjhieva) | COLM 2025 (per arXiv comment). arXiv:2507.20077 | Cross-entropy training biases the model toward an early EOS. An unsupervised sequence-training step debiases EOS, which gives longer, more detailed captions, with a hallucination increase the authors call expected. | Technique to borrow for recall. | Cheap recall lever for the SFT model (R 37.1). Pair it with the VSPS precision guard. See (d)-2. |
| 12 | **Ground What You See: Hallucination-Resistant MLLMs via Caption Feedback, Diversity-Aware Sampling, and Conflict Regularization** (M. Pan, W. Gan, J. Chen, W. Zhang, S. Bing, J. Yin, X. Zhang) | AAAI 2026, vol. 40(10), pp. 8242–8250. DOI 10.1609/aaai.v40i10.37772 (OJS page opened) | The model first describes the image and is rewarded by how well it answers from that description alone. Adds reward-variance-aware sampling and an NTK-similarity InfoNCE regularizer. Argues that GRPO can *increase* hallucination under sparse supervision. | Overlap low. Supports the "GRPO can raise hallucination" caveat. | Cite as a risk statement for any VSPS-GRPO stage. |
| 13 | **ViCrit: A Verifiable RL Proxy Task for Visual Perception in VLMs** (X. Wang, Z. Yang, C. Feng, Y. Liang et al.) | arXiv:2506.10128 (2025; venue not confirmed) | RL task: find the single subtle hallucinated span injected into a 200-word human caption, with an exact-match reward. Transfers to perception benchmarks. | Technique to borrow for the **verifier** side. | VSPS REJECTED propositions are free "injected hallucinations". A ViCrit-style task could RL-tune Vintern-1B to raise verifier precision (63.1%). Note only. |
| 14 | **Same Reward, Different Skills: When Multimodal RL Learns to Look** (H. Ye, X. Jiang, Q. Chen, B. Wang et al.) | arXiv:2610.01908 (1 Oct 2026) | RLVR gains on VLM benchmarks largely survive training on blind (gray-canvas) images. The authors propose "visual resolvability": the reward must require the image. | Risk evidence. | Any VSPS-GRPO result must include a gray-image control run, or a reviewer can say the gain is a language prior. |
| 15 | **DetailVerifyBench: A Benchmark for Dense Hallucination Localization in Long Image Captions** (X. Wang, Y. Zhang, X. Zhang, H. Yan et al.) | arXiv:2604.05623 (2026) | 1,000 images with span-level hallucination labels in long captions. | Metric/benchmark (English). | Could externally test the Vintern verifier's span-level precision (via translation). Low priority. |
| 16 | **CycleCap: Improving VLMs Captioning via Self-Supervised Cycle Consistency Fine-Tuning** (M. Krestenitis, C. Tzelepis, K. Ioannidis, S. Vrochidis et al.) | arXiv:2603.18282 (2026) | Reward from image→caption→text-to-image reconstruction similarity. | Low. | Optional. Needs a text-to-image model, too expensive on one 3090. |

**Extra facts on already-covered papers that matter here:**
- **ClaimDiff-RL** (arXiv:2605.20278; full text opened) uses GRPO with G=8, Qwen3-VL-32B, 4×8 H100 and a Gemini-3-Pro judge. Two details matter for VSPS:
  - It reports that holistic scalar rewards "can be optimized by saying less": hallucination falls because omissions rise and responses get sharply shorter.
  - It applies an **ambiguity penalty** R ← R·exp(−0.1·max(0, n_amb − n_free)), allowing one hedge per 90 words. That is a ready-made guard against the hedge saturation VSPS saw under DPO.
- **CCCaption** (CVPR 2026, ref [18]): with an unconstrained completeness reward, correctness drops in later training while the reward keeps rising. They keep the hybrid weight low (α=0.05). This is a documented recall-reward hacking curve.

## (b) Overlap risks (max 5)

1. **"Precision + recall reward over atomic claims" is taken.** BalCapRL (2026), CuRe (2026, video), CCCaption (CVPR 2026) and ClaimDiff-RL (2026) already do it, and OraPO does it for radiology. A VSPS-GRPO stage **must not** be sold as a new reward idea. What is still new:
   - the reward is a **lookup into an offline, cached three-state verdict table**, so there is no judge in the loop and no reward-model or API cost;
   - **UNCERTAIN is neutral-but-allowed-only-in-neutralized-form** (gender);
   - it runs on Vietnamese, on one consumer GPU.
2. **SimLoss (2026)** directly claims that single-pass training matches multi-stage verify-and-rewrite pipelines at about 20× lower latency. A reviewer can file VSPS's offline pipeline (~80 s/image) under "multi-stage". The counter: VSPS's cost is paid once on training data, and inference is already single-pass.
3. **CapRL / CapRL++** frame SFT as memorization and RLVR as the fix, at ICLR 2026 and in follow-up work. An SFT-only Q2 paper in 2026 must answer this explicitly, either with the GRPO add-on in (d)-1 as an ablation or with the nSFT argument from ../novelty/08.
4. **ClaimDiff-RL's hedge penalty plus the judge treating hedging as error** means someone has already identified hedging as reward hacking in caption RL. VSPS's "hedge saturation" negative result (DPO) stays novel for *preference pairs*, but should cite this as the RL-side analogue.
5. **SC-Captioner (ICCV 2025)** already reports RL beating DPO for captioning with set-difference rewards over object/attribute/relation. This is supportive, not competing, but cite it so the DPO negative result doesn't look isolated.

## (c) Must-compare baselines / must-cite (max 5)

1. **BalCapRL** (arXiv:2605.07394): closest precision/recall/length design. Cite it, and borrow c-GDPO and length masking.
2. **CapRL / CapRL++** (ICLR 2026; arXiv:2606.09393): the RLVR-for-captioning reference point. If any RL row is added, it is the expected comparison (their released CapRL-3B checkpoint can be run zero-shot and translated, or prompted in Vietnamese, as an "RL-trained captioner" baseline at inference cost only).
3. **SimLoss** (arXiv:2609.00591): single-pass vs multi-stage framing.
4. **SC-Captioner** (ICCV 2025): RL > DPO evidence for §IV-9.
5. **GDPO** (arXiv:2601.05242 / ICML 2026): must-cite if a multi-reward GRPO stage is added.

## (d) Actionable improvements, ranked by expected gain / cost

### 1. VSPS-GRPO: short GRPO stage with an offline verdict-lookup reward (feasible, best idea)

**Feasibility on one RTX 3090 (24 GB):** yes, with conditions.
- **Library.** The pinned `trl==0.19.1` GRPOTrainer has **no image support** (I grepped `trl/trainer/grpo_trainer.py` at tag v0.19.1: zero `pixel_values`/`image` hits; v0.20.0 has them). The README warns that version drift silently disables adapters. So **do not bump TRL**. Add `--stage grpo` to `scripts/train_stage2.py`, reusing its existing `build_model`, `to_chat`, `image_for` and `sequence_logprob` (already used by the custom DPO loop).
- **Loop.** About 120 lines: for each image, sample G=4 captions with `model.generate(do_sample=True, temperature=1.0, max_new_tokens=160)`, then score them with the reward below. The advantage is computed per reward as (r − mean)/std (GDPO), then summed with weights. The loss is −A·mean token logprob of the completion, on-policy with a single update, so the old-policy ratio is 1 and no clipping state is needed. Use β=0 (no reference model; Dr.GRPO/BalCapRL also drop KL), or get the KL reference for free with `model.disable_adapter()`.
- **Memory.** The measured 4-bit/512-vision-token inference peak is 7.7 GB at 0.87 s/image (`data/vram/vram_4-bit-512vt_cap_12GB.json`). Backward over 4 completions of about 200 tokens with gradient checkpointing comes to an estimated 12–16 GB. Compute logprobs **only on completion tokens**: full-sequence fp32 logits over the 152k vocab would add about 2 GB.
- **Time.** About 10–15 s per image step (4 sampled rollouts plus 1 backward). That is 2,000 KTVIC train images in about 6–8 h, an overnight run. This is my estimate, not measured.
- **No Vintern in the loop.** Online verification at about 80 s/image is impossible. The reward only *reads* the shipped `data/stage1_records` verdicts.

**Reward**, per rollout c and image i, with S/U/X the SUPPORTED/UNCERTAIN/REJECTED entity classes mapped to the 113-entry lexicon and G the train-reference gold objects:
- Mentioned objects: M = `rescap.chair.objects_in(c)`.
- Allowed set: A = S ∪ G. Forbidden set: F = X \ G. Using the gold softens the verifier's 63.1% SUPPORTED precision.
- Precision term: r_P = (|M∩A| − λ|M∩F|) / max(|M|, 1), with λ=1. Objects outside the pool count as unverified (0).
- Recall term: r_R = |M∩A| / |A|.
- Gender term: r_G = −1 if `gender_invention` fires on a person whose gender proposition is not SUPPORTED, else 0. This is the UNCERTAIN→neutralized rule as a reward.
- Guards, which multiply the total:
  - 0 if any CJK or non-Latin-Vietnamese characters (the DPO run had 41% CJK leakage);
  - the ClaimDiff-RL ambiguity factor exp(−0.1·max(0, n_hedge − 1)) over "có vẻ / có thể / dường như" (stops the DPO hedge saturation);
  - the BalCapRL length mask 0.5 ≤ len/len_sft_target ≤ 2;
  - 0 if a 4-gram repeats 3 or more times.
- Weights to start with: w_P=0.4, w_R=0.4, w_G=0.2, each GDPO-normalized.
- Put the reward in a new file `rescap/pipeline/reward.py`. It is pure Python, about 60 lines, with one `assert` self-check.

**Start point**, two arms:
- (A) the VSPS-SFT adapter (P 41.9 / R 37.1), aiming to recover recall;
- (B) zero-shot Qwen2.5-VL-7B (P 31.6 / R 57.1), aiming to raise precision while keeping R ≥ 55.

Arm B is the most direct path to the stated target (R ≥ 55, F1 > 40.7).

**Expected effect:** R up 5–15 points from the SFT start, or P up from the zero-shot start, with CHAIR held flat by the F penalty. This is a guess based on BalCapRL/CCCaption-scale gains, not measured.

**Mandatory controls:**
- the reward uses the same lexicon as CHAIR-vi and object P/R, so expect a "metric hacking" objection. Train the reward on a random half of the lexicon classes and report P/R on the held-out half as well, plus the existing human audit protocol on 50 captions;
- a gray-image control run (paper 14);
- 3 seeds (`SEEDS ?= 42 43 44` already exists).

**Risk: medium.**
- Reward hacking toward list-like captions (the linguistic quality guard is weak, since there is no LLM judge). Mitigate with the length mask and with a fluency check through the existing human eval.
- Verifier noise (S precision 63%) teaches some wrong objects. A ∪ G softens this.
- Weakens the "SFT-only" story. Present it as an *optional add-on that reuses the same verdict cache*: SFT remains the method.

### 2. EOS-debias step for recall (cheap)

From paper 11. After SFT, run their unsupervised sequence-training step, or approximately down-weight the EOS logit at decode time (`--eos-bias` in `rescap/vlm/qwen_vl.py` generate kwargs).
- Effect: longer captions and higher R. P and CHAIR will likely worsen, so pair it with the VSPS budget.
- Cost: the decode-time version is free (an inference re-run, about 0.9 s/image); their training step takes a few GPU-hours.
- Risk: hallucination rises. Report it as a recall/precision curve.

### 3. Per-sentence advantages (SD-GRPO) on top of idea 1

VSPS template captions map spans to propositions, so each sentence of a rollout can get its own r_P. The negative advantage then lands only on the sentence that named a REJECTED object.
- Effect: lower CHAIR at the same recall, and better sample efficiency on long captions.
- Cost: about 30 extra lines, the same GPU budget.
- Risk: sentence segmentation of Vietnamese sampled outputs; use the existing `rdrsegmenter` path.

### 4. ViCrit-style RL for the verifier (Vintern-1B)

Rendered SFT captions with one injected REJECTED proposition give a verifiable span-localization task. A 1B model with LoRA GRPO fits easily on a 3090.
- Effect: could raise SUPPORTED precision above 63.1%, which raises every downstream number.
- Cost: about 1 day plus re-running stage 1 (about 30 GPU-h), so it is expensive end to end.
- Risk: Vintern's yes/no head may not benefit; gains are unproven.

Skipped: online LLM judges or rubric rewards (RubiCap, MoCo Rubric, CapRL QA reward). There is no Vietnamese judge cheap enough to run on a 3090, and they would break the "no judge in the loop" distinction. Add them only if a reviewer demands a CapRL-style comparison.

## (e) Watch queries (re-run monthly)

1. arXiv API, newest first: `search_query=abs:captioning+AND+abs:GRPO&sortBy=submittedDate&sortOrder=descending` (export.arxiv.org). This surfaced papers 7–9 and 14.
2. arXiv API: `abs:caption* AND abs:"verifiable reward"`, and `abs:caption* AND abs:omission AND abs:"reinforcement learning"`.
3. Semantic Scholar: citations of CapRL (arXiv:2509.22647) and of BalCapRL (arXiv:2605.07394), sorted by date.
4. Google Scholar alert: `"image captioning" GRPO hallucination recall reward`.
5. OpenAlex: `search=caption reinforcement learning hallucination&filter=from_publication_date:2026-06-01`.
6. GitHub releases for huggingface/trl: watch for GRPO+VLM fixes (needed only if the TRL pin is ever lifted).

## Unverified

- GDPO at ICML 2026: seen in search results (icml.cc virtual poster 63333 and the NVIDIA research page), but the arXiv comment only says "NVIDIA-Tech Report". I did not open the ICML page.
- ViCrit venue: not checked.
- Unsloth claims Qwen2.5-VL-7B GRPO with 4-bit runs on a 16 GB T4 (docs.unsloth.ai, "Vision RL"). This is vendor material. I did not test it, and Unsloth would mean a new dependency, which I do not recommend; the custom loop in (d)-1 is preferred.
- All time and memory figures in (d) are estimates, except the 7.7 GB / 0.87 s inference measurement taken from the repo.
