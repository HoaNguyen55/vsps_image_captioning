# 01: Generate-verify-refine and tool-augmented captioning with recall up and hallucination not worse

Checked 2026-10-11. Every number below was copied from the arXiv PDF (pdftotext) of the paper named, with the table number given. Venues come from the PDF header or the ACL Anthology unless marked UNVERIFIED. This report extends `research_wall/01`, `03`, `06` and `09`. VFC, Woodpecker, HalluciDoctor, CapsFusion and Altogether are already listed there, so here they are only checked for two-sided (precision plus recall) evidence.

## Key finding

The papers fall into two groups.

- **Subtractive post-hoc correctors** (Woodpecker, LURE, HalluciDoctor) delete or replace claims after generation. They reliably cut CHAIR. When an independent paper measures recall or coverage, they lose it, or the result is unclear.
- **Methods that add evidence during generation** (MARINE, HALC, DeGF, REVERSE at a mild threshold) feed detector or feedback signals into decoding. These are the ones with measured Pareto gains: CHAIR down and Recall or Cover up in the same table.

This matches the VSPS diagnosis. A 3-state verifier used as a pure filter can only lose recall. Recall has to come back through an additive grounding source at the proposal or decoding stage.

## Methods with both sides measured (ranked)

### 1. MARINE: Mitigating Object Hallucination in LVLMs via Image-Grounded Guidance
- L. Zhao, Y. Deng, W. Zhang, Q. Gu. **ICML 2025** (PMLR 267). Paper: https://arxiv.org/abs/2402.08680. Code: https://github.com/Linxi-ZHAO/MARINE
- **What it does:** training-free. Detectors (DETR at threshold 0.95, RAM++ at 0.68) produce an object list. That list is fed back as a guidance prompt, and the logits are mixed classifier-free-guidance style with a guidance strength of 0.7.
- **Table 1 (COCO CHAIR, R = object recall), Greedy → MARINE:**
  - LLaVA: CHAIR_s 26.6 → 17.8, CHAIR_i 10.5 → 7.2, R 47.4 → 50.8
  - LLaVA-1.5: 8.8 → 6.2, 4.6 → 3.0, R 41.1 → 44.3
  - mPLUG-Owl2: 6.2 → 4.2, 3.4 → 2.3, R 38.8 → 41.4
  - InstructBLIP: 5.0 → 2.2, 3.2 → 1.3, R 33.2 → 36.3
  - Average: 11.0 → 8.4, 5.2 → 3.7, R 40.3 → 44.5
- **Table 2 (POPE adversarial, average):** accuracy 73.2 → 79.9, F1 77.9 → 80.4.
- **Table 3 (GPT-4V judge, 0-10 scale), image captioning on mPLUG-Owl2:** accuracy 7.97 → 8.63, detail 5.74 → 6.19. On LLaVA, accuracy went 5.27 → 6.11 while detail went 4.39 → 4.36, so detail was flat.
- **Trade-off check:**
  - On MiniGPT-v2, recall rose (41.1 → 49.7) but CHAIR_s worsened (8.2 → 11.8) and CHAIR_i worsened (4.2 → 4.9). The gain is not Pareto on every backbone.
  - Latency is ×1.98 versus greedy (Table 5).
  - In the same Table 1, Woodpecker lowers average recall (40.3 → 38.0) and LURE raises recall but triples CHAIR_s (36.2). This is independent evidence that post-hoc correctors do not reach Pareto gains.
- **Cost:** two forward passes per token plus small detectors. It fits a 7B model on one 3090. Porting from LLaVA-style models to Qwen2.5-VL is required, since Qwen2.5-VL is not in the released code. This porting is UNVERIFIED effort.
- **VSPS mapping:** proposal stage. Condition the Qwen proposer on detector or tagger objects (Florence-2 or OWLv2 instead of DETR, which has no Vietnamese-specific objects) so that it proposes objects it would otherwise miss. The Vintern verifier then filters them.

### 2. DeGF: Self-Correcting Decoding with Generative Feedback
- C. Zhang, Z. Wan, Z. Kan, M. Q. Ma, S. Stepputtis, D. Ramanan, R. Salakhutdinov, L.-P. Morency, K. Sycara, Y. Xie. **ICLR 2025**. Paper: https://arxiv.org/abs/2502.06130. Code: https://github.com/zhangce01/DeGF
- **What it does:** a generate → render → verify-and-correct loop. The model writes an initial response, Stable Diffusion 1.5 renders an image from it, and decoding is then corrected token by token. Contrastive or complementary decoding is chosen by the distance between the real and rendered images.
- **Table 2 (CHAIR, 64 new tokens), Regular → DeGF:**

  | Model | CHAIR_s | CHAIR_i | Recall | Length |
  |---|---|---|---|---|
  | LLaVA-1.5 | 26.2 → 18.4 | 9.4 → 6.1 | 58.5 → 62.7 | 53.4 → 54.1 |
  | InstructBLIP | 31.2 → 24.0 | 11.1 → 7.7 | 59.0 → 67.2 | 53.6 → 55.5 |

- **Table C1 (128 tokens), LLaVA-1.5:** CHAIR_s 55.0 → 48.8, CHAIR_i 16.3 → 14.6, Recall 71.9 → 76.0, Length 97.3 → 96.4.
- **Independent rows in the same Table 2:**
  - HALC on LLaVA-1.5 is also Pareto: CHAIR 21.7 / 7.1, Recall 63.4.
  - Woodpecker is not: Recall 60.8 but Length 49.7, versus 53.4 for Regular.
- **Trade-off check:**
  - Length dips slightly at 128 tokens (97.3 → 96.4) and at 256 tokens (Table C2).
  - Latency is ×4.04 and peak memory 19,119 MB on LLaVA-1.5-7B on an RTX A6000 Ada (Table 7).
- **Cost:** feasible on a 3090 for a 7B model. Qwen2.5-VL-7B has more image tokens, so its memory headroom is UNVERIFIED. Running the VLM in 4-bit or offloading SD between stages would probably be needed.
- **VSPS mapping:** decoding or proposal. Use it as an alternative recall-preserving proposer. The T2I step is expensive, and its value for Vietnamese scenes is unknown.

### 3. REVERSE: Generate, but Verify (Retrospective Resampling)
- T.-H. Wu, H. Lee, J. Ge, J. E. Gonzalez, T. Darrell, D. M. Chan. **NeurIPS 2025**. Paper: https://arxiv.org/abs/2504.13169. Code (MIT): https://github.com/tsunghan-wu/reverse_vlm
- **What it does:** the VLM is trained with hallucination-aware training to emit confidence tokens. At inference, a span whose "unconfident" probability exceeds τ is backtracked and resampled.
- **Table 1, LLaVA-v1.5-7B, None → REVERSE (τ = 0.003):**
  - CHAIR-MSCOCO: CHAIR_i 15.4 → 10.3, CHAIR_s 50.0 → 37.0
  - AMBER-G: CHAIR 7.8 → 6.0, Cover 51.0 → 52.2, Hall 36.4 → 30.4, Cog 4.2 → 3.0
  - LLaVA-MORE-8B on AMBER-G: CHAIR 7.8 → 6.5, Cover 53.1 → 54.8
- **Trade-off check:**
  - τ is a hard knob. At τ = 0.0003, Cover collapses to 26.9 (LLaVA-1.5) and 38.9 (LLaVA-MORE).
  - On Qwen2.5-VL-FT-3B, Cover falls slightly (51.7 → 51.5) while CHAIR improves (7.7 → 7.5).
  - Woodpecker in the same table loses coverage: 51.0 → 48.9 on LLaVA-1.5 and 53.1 → 50.7 on LLaVA-MORE.
- **Cost:** requires training on the authors' hallucination-aware data. Training cost was not checked. A QLoRA variant on a 3090 is plausible but UNVERIFIED.
- **VSPS mapping:** training plus decoding. Train the SFT model to tag low-confidence spans, so the UNCERTAIN state is learned rather than thresholded. A mild τ keeps coverage, which is exactly the threshold issue VSPS has (about 41% of entities UNCERTAIN).

### 4. HALC: Object Hallucination Reduction via Adaptive Focal-Contrast Decoding
- Z. Chen, Z. Zhao, H. Luo, H. Yao, B. Li, J. Zhou. **ICML 2024** (PMLR 235). Paper: https://arxiv.org/abs/2403.00425. Code: https://github.com/BillChan226/HALC
- **What it does:** a detect-then-describe decoder. An open-vocabulary detector grounds the current object token (the paper names Grounding DINO or OWLv2). Focal views are contrasted, and a visually matched beam search is used.
- **Own evidence, Table 1 (COCO CHAIR plus BLEU), Greedy → HALC:**
  - LLaVA-1.5: CHAIR_s 20.80 → 13.80, CHAIR_i 6.77 → 5.50, BLEU 15.93 → 16.10
  - MiniGPT-4: 30.87 → 17.80, 12.33 → 8.10, BLEU 14.33 → 14.91
  - The paper reports BLEU only and no recall.
- **Independent evidence:** DeGF Table 2 (LLaVA-1.5) gives CHAIR_s 26.2 → 21.7, CHAIR_i 9.4 → 7.1, Recall 58.5 → 63.4, Length 53.4 → 53.4.
- **Trade-off check:** latency is ×6.51 and memory 23,084 MB (DeGF Table 7). That is borderline on 24 GB with LLaVA-7B and likely over the limit with Qwen2.5-VL-7B unless quantized.
- **VSPS mapping:** decoding or proposal. Detector-grounded token selection.

### 5. Woodpecker: Hallucination Correction for MLLMs
- S. Yin, C. Fu, S. Zhao et al. arXiv 2310.16045, v2 Dec 2024. The journal version in Science China Information Sciences 2024 is UNVERIFIED (the search did not confirm it). Paper: https://arxiv.org/abs/2310.16045. Code: https://github.com/BradyFU/Woodpecker
- **Own evidence, Table 3 (GPT-4V judge, LLaVA-QA90, 0-10), accuracy / detailedness:**
  - LLaVA: 7.1 / 7.1 → 7.8 / 8.6
  - MiniGPT-4: 7.0 / 6.4 → 8.2 / 8.8
  - Otter: 7.0 / 6.7 → 8.5 / 8.8
  - Detail rises because detector boxes and counts are added to the text.
- **Trade-off check:**
  - POPE recall falls on LLaVA: 84.00 → 78.67 (random, Table 1).
  - Three independent re-runs show losses in coverage or length: MARINE Table 1 (average recall 40.3 → 38.0), DeGF Table 2 (length 53.4 → 49.7) and REVERSE Table 1 (AMBER Cover 51.0 → 48.9).
  - The original study needs the GPT-3.5 API, and its GPT-4V evaluation used only LLaVA-QA90.
- **VSPS mapping:** verification and rendering. Woodpecker is the closest analogue to VSPS, and it shows the same recall loss. Cite it as precedent for the problem, not as a fix.

## Methods with weaker or one-sided evidence

| Method | Venue / link | What it measures | Trade-off check | VSPS use |
|---|---|---|---|---|
| **Dentist** (TMLR 10/2024) https://arxiv.org/abs/2409.16494, code github.com/CYandYue/Dentist | Classifies query type, then verifies and corrects in a loop | Table 2 (GPT-4V, LLaVA-QA90): LLaVA accuracy 6.0 → 6.6, detailedness 5.3 → 5.8, both up. Table 3: CHAIR_s 84.0 → 75.2 and CHAIR_i 23.4 → 17.1 on LLaVA | No object recall measured with CHAIR. Uses the GPT-3.5 API | verification |
| **LURE** (ICLR 2024) https://arxiv.org/abs/2310.00754, code github.com/YiyangZhou/LURE | Revisor trained on co-occurrence, uncertainty and position perturbations | Table 1: LLaVA CHAIR_s 54.0 → 27.1, CHAIR_i 11.3 → 6.4 | Table 17: correct objects reduced by 0.68-2.72%, LLaVA length 102.8 → 96.39 words. MARINE's re-run gives recall 55.2 but CHAIR_s 36.2. Not Pareto | rendering or revisor |
| **HalluciDoctor** (CVPR 2024) https://arxiv.org/abs/2311.13614, code github.com/Yuqifan1117/HalluciDoctor | Cross-checking of instruction data plus counterfactual expansion | Table 2: MiniGPT-4 instance-level CHAIR_obj 12.0 → 5.7 (LLaVA → LLaVA++) | Table 1: data length 96.1 → 87.8. Detailedness appears only in Fig. 3 as bars, so the numbers are not readable | training-data cleaning |
| **VFC** (CVPR 2024) https://arxiv.org/abs/2404.19752 | Multiple captioners → LLM fact-check with detector and VQA → rewrite | Table 2: CLIP-Score 32.90 vs LLaVA-1.5 32.08. Table 4 ablation: without fact check 32.41 | No precision or recall metric at all; human and GPT-4V results are aggregate win rates only. No official code found | proposal fusion |
| **ImageInWords** (EMNLP 2024, 2024.emnlp-main.6) https://aclanthology.org/2024.emnlp-main.6 | Human-in-the-loop dense captions | Human side-by-side, Table 2: IIW data beats DCI and DOCCI on comprehensiveness (+61%, +42%) and hallucination (+42%, +35% lower) | §5.1 / Table 3: a PaLI-5B fine-tuned on IIW shows a "small hallucination trade-off (-9, -7)%" versus the DCI and DOCCI models. Data is Pareto, the trained model is not | SFT target style |
| **Volcano** (NAACL 2024) https://arxiv.org/abs/2311.07362, code github.com/kaistAI/Volcano | Self-feedback revision, 3 iterations | Table 1 vs LLaVA-1.5-7B: MMHal score 2.42 → 2.6, hallucination rate 0.55 → 0.49, GAVIE accuracy 6.42 → 6.52, relevancy 8.2 → 8.4 | QA benchmarks only, no caption coverage metric | verification |
| **Pelican** (arXiv 2407.02352; EMNLP 2024 is UNVERIFIED) | Claim decomposition plus program-of-thought tool checks | Table 1: LLaVA-1.5 MMHal 2.02 → 2.27, GAVIE accuracy 5.64 → 6.51 | QA benchmarks only. On LLaVA-v1.6, GAVIE relevancy 7.8 → 7.5 and MMHal 3.24 → 3.04 got worse | verification |
| **LogicCheckGPT** (arXiv 2402.11622; Findings of ACL 2024 is UNVERIFIED) https://github.com/Hyperwjf/LogicCheckGPT | Logical closed-loop probing questions | POPE only (Table 1) | Not a caption coverage metric | verifier probes |
| **ReCaption** (MMM 2024, DOI 10.1007/978-3-031-53302-0_3) https://arxiv.org/abs/2312.01701 | ChatGPT rewrites captions, then fine-tune | POPE and FGHE accuracy, precision, recall and F1 (Table 2) | Discriminative probes only, no caption recall | SFT data |
| **CapsFusion** (CVPR 2024), **Altogether** (EMNLP 2024) | Caption fusion and alt-text re-alignment | CIDEr, CLIP-Score, human preference (already in wall 09) | No CHAIR-plus-coverage pair found in the tables | rendering style |
| **Generating Accurate and Detailed Captions for High-Resolution Images** (arXiv 2510.27164, already in wall 03) | VLM → LLM co-occurrence prediction → detector verification | Table 1 LMM score: LLaVA-1.5 0.6785 → 0.7304. Table 2: POPE on captions | Not peer-reviewed. Judge-based scoring | proposal |

DOCCI (https://arxiv.org/abs/2404.19753) is a human dataset with no verification pipeline, so it is out of scope here.

## Implications for VSPS

1. **Pareto gains come from adding grounded objects, not from stricter filtering.** MARINE and HALC add detector objects *into generation*. Woodpecker and LURE only remove or rewrite, and their recall drops in independent re-runs. VSPS currently does the latter: Qwen proposes, then Vintern filters. The fix is to make the *proposer* detector-conditioned, MARINE-style. Concretely: run a Florence-2 or OWLv2 object list, add it to the Qwen proposal prompt or apply guidance, raise the entity cap, and keep Vintern as the precision gate.
2. **The verifier threshold is the trade-off knob.** REVERSE shows this directly: τ = 0.003 gives a Pareto gain (Cover 51.0 → 52.2), while τ = 0.0003 halves coverage. Calibrating Vintern's UNCERTAIN band, which the logit-verifier commit already moves toward, is the VSPS version of choosing τ.
3. **Report numbers the way MARINE and DeGF do:** CHAIR_s, CHAIR_i, Recall and Length side by side, plus AMBER Cover (REVERSE). That reporting style is what makes a "no trade-off" claim credible.

## Top picks for VSPS

1. **MARINE (ICML 2025):** detector-guided generation. Average over 5 LVLMs: CHAIR_i 5.2 → 3.7 and Recall 40.3 → 44.5 (Table 1). Training-free and fits a 3090.
2. **DeGF (ICLR 2025):** generate → T2I → self-correct. LLaVA-1.5: CHAIR_s 26.2 → 18.4 and Recall 58.5 → 62.7 at equal length (Table 2). Peak memory 19 GB.
3. **REVERSE (NeurIPS 2025):** learned uncertainty tokens plus resampling. AMBER CHAIR 7.8 → 6.0 and Cover 51.0 → 52.2 at τ = 0.003; coverage collapses at strict τ (Table 1).
4. **HALC (ICML 2024):** OWLv2 / Grounding DINO grounded decoding. Independently Pareto in DeGF Table 2: CHAIR_s 26.2 → 21.7 and Recall 58.5 → 63.4. Uses 23 GB.
5. **Woodpecker (arXiv 2310.16045) as a cautionary baseline:** GPT-4V accuracy and detail both up in its own Table 3, but three independent re-runs show recall, Cover or length losses. It is the closest analogue to the current VSPS filter design.
