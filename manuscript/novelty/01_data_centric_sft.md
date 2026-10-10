# 01: Data-centric SFT hallucination mitigation (overlap with C1, C4)

Agent 01. Searched 2026-10-10 with 23 distinct web queries (arXiv, ACL Anthology, CVF/AAAI pages, NeurIPS proceedings). Every entry below has an abstract page that was opened or confirmed in a search result. Papers already verified in `Q2_LITERATURE.md` (HalluciDoctor, LRV, ReCaption, KnowAda, Less-is-More, HACL, RLAIF-V) are not re-described at length here. They are re-rated only against C1/C4.

Venue legend: CVPR/ICCV = IEEE/CVF (on IEEE Xplore, Scopus-indexed). ACL/EMNLP/NAACL = ACL Anthology (Scopus-indexed). AAAI = AAAI Press (Scopus). NeurIPS/ICLR/ICML = Scopus-indexed proceedings (no publisher DOI for ICLR). MMM = Springer LNCS (Scopus). Information Sciences = Elsevier (Scopus Q1).

## A. Core data-cleaning / rewriting precedents (must contrast for C1)

### A1. HalluciDoctor: Mitigating Hallucinatory Toxicity in Visual Instruction Data
- Q. Yu, J. Li, L. Wei, L. Pang, W. Ye, B. Qin, S. Tang, Q. Tian, Y. Zhuang. CVPR 2024 (IEEE/CVF). arXiv:2311.13614 (confirmed).
- Method: answer-chunk extraction, then cross-checking consistency across several MLLMs. Chunks below a 0.5 consistency score are deleted, and ChatGPT removes the hallucinated phrases while keeping sentence structure. The result is the LLaVA+/LLaVA++ dataset. A counterfactual expansion step also rebalances object co-occurrence. Then plain re-training.
- Overlap: C1 **HIGH**. Both detect, clean, and retrain on SFT data with a standard loss and no inference cost. C4 low (chunks are not typed, and an LLM edits free text). C2 medium (binary consistency, no UNCERTAIN state, no negated query).
- Distinguishing point: VSPS keeps a three-state verdict. It does not delete UNCERTAIN content: it neutralizes it (C3). Its unit is a typed proposition, and it re-renders the caption from verdicts instead of having an LLM edit text, so every output span traces to a proposition.
- Recommendation: **must cite & contrast**.

### A2. LRV-Instruction: Mitigating Hallucination in LMMs via Robust Instruction Tuning
- F. Liu, K. Lin, L. Li, J. Wang, Y. Yacoob, L. Wang. ICLR 2024. arXiv:2306.14565.
- Method: GPT-4-generated instructions, including negative instructions about absent objects, used for SFT.
- Overlap: C1 medium (fixes hallucination through SFT data, but by adding negatives, not by verifying positives). C4 none.
- Distinguishing point: VSPS filters and verifies the positive caption content of the existing supervision. It adds no negative questions.
- Recommendation: must cite & contrast.

### A3. ReCaption: Mitigating Fine-Grained Hallucination by Fine-Tuning LVLMs with Caption Rewrites
- L. Wang, J. He, S. Li, N. Liu, E.-P. Lim. MMM 2024 (Springer LNCS, Scopus). arXiv:2312.01701.
- Method: ChatGPT rewrites captions for diversity, and the LVLM is fine-tuned on the rewrites.
- Overlap: C1 medium (caption-level SFT data rewriting, but with no image-grounded verification). C4 low.
- Distinguishing point: VSPS rewrites only through image-verified propositions. ReCaption's rewrites are text-only paraphrases.
- Recommendation: should cite.

### A4. KnowAda: Bridging the Visual Gap: Fine-Tuning Multimodal Models with Knowledge-Adapted Captions
- M. Yanuka, A. Ben Kish, Y. Bitton, I. Szpektor, R. Giryes. NAACL 2025 (long), pp. 10497–10518. arXiv:2411.09018 (confirmed).
- Method: probes the target VLM with visual questions about each caption detail. Details the model "does not know" are removed or rewritten, and the model is then SFT-ed on the adapted dense captions. Introduces DNLI, a proposition-level metric. Reports that simply simplifying captions or standard curation does not help.
- Overlap: C1 **HIGH**. It is the closest conceptual twin: per-detail VQA probing that edits dense-caption SFT targets, then a standard SFT loss. C4 medium (decomposes captions into propositions for evaluation, but the training captions are LLM-edited free text). C2 low/medium (its criterion is the student model's own knowledge, binary keep/drop).
- Distinguishing point: KnowAda adapts captions to what the student model knows. VSPS verifies against image evidence with a separate verifier, using dual affirmative and negated queries and K=5 votes, with an explicit UNCERTAIN state. VSPS neutralizes uncertain content instead of dropping it, and renders from typed propositions. KnowAda is English-only; VSPS targets Vietnamese.
- Recommendation: **must cite & contrast**. A baseline is also advisable.

### A5. Image Textualization (IT): An Automatic Framework for Creating Accurate and Detailed Image Descriptions
- R. Pi, J. Zhang, J. Zhang, R. Pan, Z. Chen, T. Zhang. NeurIPS 2024 Datasets & Benchmarks. The proceedings title reads "...for Generating Rich and Detailed Image Descriptions". arXiv:2406.07502 (opened).
- Method: an MLLM draft caption is checked by an LLM object extractor plus an open-set detector (GroundingDINO). Objects the detector cannot find are removed as hallucinations, and dense-captioner facts are added. An LLM writes the final description, and LLaVA-7B is SFT-ed on it, giving longer captions with less hallucination.
- Overlap: C1 **HIGH** for the object type (offline verification of SFT captions, then standard SFT). C4 low/medium (object-level facts, LLM rendering, not span-traceable). C2 low (binary detector check).
- Distinguishing point: IT verifies object existence only, with a detector, in binary. VSPS verifies five proposition types with VQA dual queries and three states, and renders with traceable templates or constrained-LM rendering.
- Recommendation: **must cite & contrast**.

### A6. VIGC: Visual Instruction Generation and Correction
- B. Wang, F. Wu, X. Han, et al. AAAI 2024. arXiv:2308.12714 (confirmed). AAAI OJS article 28338.
- Method: an MLLM generates instruction data (VIG), and an iterative correction module (VIC) updates answers to reduce hallucination. The data is used for SFT.
- Overlap: C1 medium (data-level hallucination reduction, but the correction is generative and iterative, with no explicit verification verdict). C4 none.
- Distinguishing point: VSPS uses explicit verification per proposition with stored evidence, not iterative regeneration.
- Recommendation: should cite.

### A7. DFTG: Prescribing the Right Remedy: Mitigating Hallucinations in LVLMs via Targeted Instruction Tuning
- R. Hu, Y. Tu, S. Wei, D. Lu, J. Sang. *Information Sciences* (Elsevier, Scopus Q1), 2025. arXiv:2404.10332 (opened).
- Method: diagnoses each model's specific hallucinations, then generates instruction data targeted at them.
- Overlap: C1 medium (model-specific SFT data generation). C4 none.
- Distinguishing point: DFTG generates new targeted QA data. VSPS cleans the caption supervision itself.
- Recommendation: should cite. It is useful as an Elsevier journal reference in the extension.

## B. Data-side work with verification or decomposition (C1/C4 adjacent)

### B1. HallE-Control (formerly HallE-Switch): Controlling Object Hallucination in Large Multimodal Models
- B. Zhai, S. Yang, C. Xu, S. Shen, K. Keutzer, C. Li, M. Li. arXiv:2310.01779 (opened; no journal-ref on arXiv, so the venue is unverified).
- Method: attributes hallucination to descriptions that are finer-grained than the vision module can verify. Trains on "contextual-only", detector-grounded object data versus data with parametric objects, plus a control vector. Reports 44% less hallucination than LLaVA-7B.
- Overlap: C1 medium (grounded-only SFT data is a core ingredient). It also motivates "not visible" content. C4 low.
- Distinguishing point: HallE adds a control embedding and trains on both regimes. VSPS uses one standard SFT on verified data, with no architectural change.
- Recommendation: should cite.

### B2. REVERSE: Generate, but Verify: Reducing Hallucination in VLMs with Retrospective Resampling
- T.-H. Wu, H. Lee, J. Ge, J. E. Gonzalez, T. Darrell, D. M. Chan. NeurIPS 2025. arXiv:2504.13169 (opened).
- Method: 1.3M semi-synthetic samples with phrase-level hallucination tags (special tokens) for hallucination-aware training. At inference, the model backtracks and resamples.
- Overlap: C1 low/medium (data-level phrase tagging, but it adds an inference-time loop and a modified vocabulary, so it is not single-pass). C4 low.
- Distinguishing point: the VSPS deployed model is single-pass, with no special tokens and no resampling.
- Recommendation: should cite as a contrast to "verification at inference".

### B3. CapMAS: Toward Robust Hyper-Detailed Image Captioning: A Multiagent Approach and Dual Evaluation Metrics
- S. Lee, S. Yoon, T. Bui, J. Shi, S. Yoon. ICML 2025. arXiv:2412.15484 (opened).
- Method: an LLM decomposes a detailed caption into atomic propositions, an MLLM scores True/False per proposition, and an LLM revises the caption. Training-free and post hoc.
- Overlap: C1 low (post hoc, not data). C4 **medium** (atomic propositions, then verify, then re-write is structurally the same chain as VSPS's typed propositions, verification, and rendering). C2 medium (probability threshold, binary).
- Distinguishing point: VSPS moves this chain offline into SFT-target construction, so it costs nothing at deployment. It types propositions, keeps three states, and renders via template or constrained LM rather than free LLM revision.
- Recommendation: **must cite & contrast**.

### B4. Visual Fact Checker (VFC): Enabling High-Fidelity Detailed Caption Generation
- Y. Ge, X. Zeng, J. S. Huffman, T.-Y. Lin, M.-Y. Liu, Y. Cui. CVPR 2024 (IEEE/CVF), pp. 14033–14042. arXiv:2404.19752.
- Method: drafts captions, then an LLM fact-checks them with a detector and VQA, and an LLM writes the final caption. Training-free.
- Overlap: C1 low (it is a captioning pipeline, though usable as a data generator). C4 medium (verify-then-compose).
- Distinguishing point: VSPS distils the verified output into a single-pass student. It types and traces propositions, and uses three states.
- Recommendation: should cite (already in Q2 as must-cite).

### B5. From Descriptive Richness to Bias: Unveiling the Dark Side of Generative Image Caption Enrichment
- Y. Hirota, R. Hachiuma, C.-H. H. Yang, Y. Nakashima. EMNLP 2024, pp. 17807–17816. DOI 10.18653/v1/2024.emnlp-main.986 (opened).
- Method/finding: LLM-enriched captions carry more gender bias and hallucination. Models trained on them amplify gender bias by 30.9% and hallucination by 59.5%.
- Overlap: C1 low (an analysis, not a method). It **directly supports C3 and C5**: enriched SFT captions inject unsupported gender, which is the failure VSPS neutralizes and measures.
- Distinguishing point: VSPS supplies the remedy that Hirota et al. only diagnose.
- Recommendation: **should cite** as motivation for C3/C5. It is a strong fit.

### B6. GVF: Grounded Visual Factualization: Factual Anchor-Based Finetuning for Enhancing MLLM Factual Consistency
- F. Morbiato, L. Romano, A. Persona. arXiv:2511.10671, Nov 2025 (confirmed; arXiv only).
- Method: augments SFT data with structured factual anchors (e.g. "[FACT: COUNT=2]") for 8 hallucination types, plus a factual-consistency loss.
- Overlap: C1 low/medium (data-level, but adds a loss term, whereas VSPS uses a standard loss). C4 low/medium (typed facts are used as auxiliary anchors, not as the source of the caption).
- Recommendation: optional.

### B7. Online Self-Calibration Against Hallucination in VLMs (OSCAR)
- M. Chen, C. Yang, H. Zhu, D. Wu, Z. Lin, Q. Si. IJCAI 2026 (arXiv comments). arXiv:2605.00323 (opened).
- Method: names a "Supervision-Perception Mismatch" (distilled fine-grained supervision exceeds what the student can perceive) and a "Generative-Discriminative Gap". Uses MCTS plus a dual-granularity reward, then DPO.
- Overlap: C1 low (preference/online, not SFT data cleaning). Its diagnosis supports the VSPS motivation, as Less-is-More and KnowAda do.
- Recommendation: should cite as recent support for "supervision exceeding perception".

### B8. AVES-DPO: Aligning with Your Own Voice: Self-Corrected Preference Learning for Hallucination Mitigation in LVLMs
- B. Lim, J. Yun, J. Kwon, K. Kim, Y. Kim. ACL 2026 (arXiv comments). arXiv:2604.24395 (opened).
- Method: consensus-based verification flags hallucinations, and the model self-corrects, producing in-distribution DPO pairs.
- Overlap: C1 low/medium (consensus verification builds training data, but for DPO). C2 low.
- Recommendation: optional. Group it under "verification → preference data".

### B9. Antidote (CVPR 2025): Y. Wu et al. arXiv:2504.20468 (opened)
- Synthetic data plus preference optimization for counterfactual-presupposition questions.
- Overlap: C1 low.
- Recommendation: optional.

### B10. HACL (CVPR 2024; arXiv:2312.06968) and Less is More (ACL 2024; arXiv:2402.14545)
- These are covered in Q2. HACL: C1 low (contrastive representation loss, not data cleaning). Less is More: C1 low as a method, but key motivation (over-detailed targets cause hallucination).
- Recommendation: cite as in Q2.

### B11. SimLoss: A Glance Is All You Need: Single-Pass Fine-Grained Image Captioning with SimLoss
- S. Jain, R. Barkur, V. G, R. Rossi, F. Dernoncourt, et al. (Adobe). arXiv:2609.00591, Sep 2026 (opened).
- Method: an InfoNCE hidden-state/image-embedding loss lets a single-pass captioner approach a multi-stage generate→decompose→verify→rewrite pipeline about 20× faster.
- Overlap: C1 low (it explicitly avoids pseudo-captions from the multi-stage pipeline and adds a loss term). It shares the single-pass deployment motivation.
- Distinguishing point: VSPS achieves single-pass deployment through verified data with standard SFT, not an extra loss.
- Recommendation: optional. It is very recent and a good foil for "no extra loss term".

## C. Searched with no direct match found
- An exact VSPS-style recipe (typed propositions, then multi-query VQA verification with an UNCERTAIN state, then deterministic/template rendering, then standard SFT of a single-pass captioner) did not appear in any of the 23 queries. Queries included "verifier-filtered dense captions SFT", "template caption from verified attributes", "hedged / not-visible supervision", and "gender-neutral caption synthesis".
- Nearest template-side works: FIHA (arXiv:2409.13612; LLM-free template Q&A for *evaluation*) and EDC (arXiv:2412.14233; an LLM converts structured attributes into captions). Neither trains a captioner on traceable template output. Both were seen only in search snippets.
- Vietnamese: LaVy (arXiv:2404.07922) trains on MT-translated LLaVA data refined by Gemini, with no hallucination filtering. AutoViVQA (arXiv:2603.09689) uses multi-model majority-vote filtering for a VQA dataset. Neither cleans caption supervision. The C5 "first Vietnamese" framing is not threatened by this topic.

## Unverified
- HallE-Control venue (no journal-ref on arXiv; it may have appeared at a 2024 workshop or conference). Cite as arXiv.
- "Exposing Hallucinations to Suppress Them" (arXiv:2509.21997), ViHallu-Instruction, and SEV-Cap (a community page) were seen only in snippets and not opened. Do not cite without checking.

## Highest-overlap risks
1. **KnowAda (NAACL 2025)**: per-detail VQA probing edits dense-caption SFT targets. It is the closest to C1. Contrast with student-knowledge vs image-evidence verification, three states plus neutralization vs drop, and traceable rendering.
2. **HalluciDoctor (CVPR 2024)**: detect, remove hallucinated spans, retrain. Contrast with the binary consistency check plus LLM deletion.
3. **Image Textualization (NeurIPS 2024 D&B)**: detector-verified objects form detailed SFT captions. Contrast with an object-only binary check and LLM rendering.
4. **CapMAS (ICML 2025)**: atomic propositions, then MLLM verification, then rewrite (the C4 chain). Contrast with post hoc vs offline-SFT, typed propositions, and three states.
5. **VFC (CVPR 2024) / REVERSE (NeurIPS 2025)**: verification at inference. VSPS needs to state "verification only offline; deployed model single-pass" explicitly.

## Suggested novelty statement
"Prior data-centric methods clean SFT data by deleting spans that fail a binary consistency or detector check (HalluciDoctor, Image Textualization), or by adapting captions to what the student model already knows (KnowAda). VSPS instead verifies each typed atomic proposition against image evidence with a three-state verdict. It neutralizes, rather than discards, under-evidenced content, and re-renders the supervision so that every output span traces to a verified proposition. All verification happens offline, so the deployed captioner is a standard single-pass model trained with an unmodified SFT loss."
