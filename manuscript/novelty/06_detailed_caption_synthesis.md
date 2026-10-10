# 06: Detailed / dense caption synthesis from structured or verified elements

Agent 06. Focus: overlap with **C1** (verification controls the quality of SFT supervision data, offline only, plain SFT loss) and **C4** (typed atomic propositions, then budgeted selection, then template or constrained-LM rendering with span ← proposition ← verdict traceability).
Verification: every arXiv ID was resolved through the arXiv export API (title and authors match). Venues and DOIs come from OpenAlex, the arXiv comment field, or CVF open-access pages. Checked 2026-10-10.

Already cited in the v9 draft: Lee et al. [10] (CapMAS), ReflectCAP [11], KnowAda [12], CCCaption [18]. All other papers below are **not** currently cited.

---

## A. Caption-data engines that fuse experts and verify (closest to C1)

### A1. Visual Fact Checker: Enabling High-Fidelity Detailed Caption Generation (VFC)
- Y. Ge, X. Zeng, J. S. Huffman, T.-Y. Lin, et al. CVPR 2024 (IEEE/CVF, Scopus). DOI 10.1109/CVPR52733.2024.01331; arXiv:2404.19752.
- Method: training-free, three steps. Several captioners write drafts. An LLM fact-checks them by calling object detection and VQA tools. An LLM then writes the final caption from the checked results. The authors present it as a way to produce high-fidelity captions, including for dataset building.
- Overlap: C1 **medium** (generate, verify, re-caption is the same skeleton; the paper positions it as a test-time or captioning pipeline, not as SFT supervision whose quality is controlled per proposition). C4 **medium** (an LLM composes from verified items, but there are no typed propositions, no budget, and no span-level trace). C2 low (binary keep or drop, no UNCERTAIN state).
- Distinguishing point: VFC runs its multi-model pipeline every time it writes a caption and keeps no explicit verdict per claim. VSPS stores a three-state verdict for each typed proposition, renders the selected propositions under a budget with span-level traceability, and distils the result into a single-pass model.
- Recommendation: **must cite & contrast**. Not in the v9 draft, although Q2_LITERATURE flags it as "key".

### A2. Image Textualization (IT): An Automatic Framework for Creating Accurate and Detailed Image Descriptions
- R. Pi, J. Zhang, J. Zhang, R. Pan, et al. NeurIPS 2024 Datasets & Benchmarks. The NeurIPS version is titled "...for Generating Rich and Detailed Image Descriptions", DOI 10.52202/079017-3433 (OpenAlex); arXiv:2406.07502.
- Method: an MLLM writes a holistic caption. Vision experts (detection, dense captioning, depth) extract object-level facts, flag and remove hallucinated objects, and add verified details. An LLM recaptions from these. The resulting data are used to fine-tune MLLMs, and the paper reports fewer hallucinations after fine-tuning.
- Overlap: C1 **HIGH** (verifying, then repairing captions, then using them as SFT training data to reduce hallucination is the same data-level thesis). C4 medium (an LLM rewrites from structured expert outputs, but nothing is typed per proposition, there is no budget, and there is no traceability). C2 none (binary object filter).
- Distinguishing point: IT checks objects with detectors and keeps or deletes each one. VSPS verifies typed propositions (attribute, action, count, relation, not only objects) with dual yes/no queries and K=5 votes, and keeps an UNCERTAIN state that is neutralized rather than deleted. Its output is rendered so that every span is traceable. IT is English only and has no mechanism like gender neutralization.
- Recommendation: **must cite & contrast** (the closest unmentioned C1 precedent).

### A3. Benchmarking and Improving Detail Image Caption (CAPTURE + data-construction pipeline)
- H. Dong, J. Li, B. Wu, J. Wang, et al. arXiv:2405.19092 (v4). No peer-reviewed venue confirmed.
- Method: the CAPTURE metric extracts objects, attributes and relations (scene-graph style) to evaluate detailed captions. The paper also proposes a five-stage data-synthesis pipeline (holistic caption, then region/object captions, then hallucination filtering, then merging) and shows that SFT on the synthesized data improves detailed captioning.
- Overlap: C1 medium-HIGH (filters hallucinated elements in synthesized SFT data). C4 medium (decomposes into object, attribute and relation elements, but an LLM merges them freely with no trace). C5 low (an evaluation of the CAPTURE type, English only).
- Distinguishing point: same as for A2. Filtering is binary, and the merge is free-form LLM generation without a span ← proposition ← verdict trace or a budget.
- Recommendation: **should cite**.

### A4. DenseFusion-1M: Merging Vision Experts for Comprehensive Multimodal Perception
- X. Li, F. Zhang, H. Diao, Y. Wang, et al. NeurIPS 2024 (D&B). DOI 10.52202/079017-0588; arXiv:2407.08303.
- Method: "Perceptual Fusion" feeds outputs from several vision experts (detection, OCR, tags) as priors to an MLLM caption engine. The engine produces 1M hyper-detailed captions, which are used for MLLM training.
- Overlap: C1 low-medium (the goal is better SFT captions, but quality comes from expert priors rather than from verifying each claim). C4 low.
- Distinguishing point: the experts add content, but no claim is verified or rejected, and nothing is traceable.
- Recommendation: should cite (one line in a group).

### A5. CapsFusion: Rethinking Image-Text Data at Scale
- Q. Yu, Q. Sun, X. Zhang, Y. Cui, et al. CVPR 2024. DOI 10.1109/CVPR52733.2024.01330; arXiv:2310.20550.
- Method: an LLM (later distilled) fuses the web alt-text with a synthetic caption to fix knowledge loss and caption collapse in pre-training data.
- Overlap: C1 low (a data-quality motive, but no visual verification). C4 none.
- Recommendation: optional.

### A6. FuseCap: Leveraging Large Language Models for Enriched Fused Image Captions
- N. Rotstein, D. Bensaid, S. Brody, R. Ganz, et al. WACV 2024 (IEEE). DOI 10.1109/WACV57701.2024.00559; arXiv:2305.17718.
- Method: outputs from frozen experts (detector, attribute recognizer, OCR) are fused into captions by an LLM, giving 12M enriched training pairs.
- Overlap: C1 low, C4 low-medium (structured expert outputs are rendered by an LLM, but are not verified and not traceable).
- Recommendation: optional (cite in a group with A4 and A5).

### A7. ShareGPT4V: Improving Large Multi-Modal Models with Better Captions
- L. Chen, J. Li, X. Dong, P. Zhang, et al. ECCV 2024 (Springer LNCS, Scopus). DOI 10.1007/978-3-031-72643-9_22; arXiv:2311.12793.
- Method: GPT-4V writes 100K detailed captions; a Share-Captioner extends them to 1.2M; these are used for pre-training and SFT.
- Overlap: C1 low (better SFT captions, but no verification). C4 none.
- Recommendation: should cite as the standard "SFT on detailed synthetic captions" baseline idea.

### A8. From Pixels to Prose: A Large Dataset of Dense Image Captions (PixelProse)
- V. Singla, K. Yue, S. Paul, R. Shirkavand, et al. arXiv:2406.10328. No peer-reviewed venue confirmed.
- Method: 16M dense captions written by a VLM (Gemini), with safety, PII and watermark filtering and metadata.
- Overlap: C1 low (filtering is for safety, not for factual verification). C4 none.
- Recommendation: optional.

### A9. What If We Recaption Billions of Web Images with LLaMA-3? (Recap-DataComp-1B)
- X. Li, H. Tu, M. Hui, Z. Wang, et al. ICML 2024 per Semantic Scholar (venue not cross-checked); arXiv:2406.08478.
- Method: a LLaVA-LLaMA-3 recaptioner relabels 1.3B images.
- Overlap: none to low. Recommendation: optional.

### A10. Enhancing Descriptive Captions with Visual Attributes for Multimodal Perception (EDC)
- Y. Sun, J. Hao, K. Zhu, J.-J. Liu, et al. CVPR 2026 (CVF open-access PDF found); arXiv:2412.14233.
- Method: off-the-shelf specialists (depth, emotion, fine-grained category, HOI, relative location) extract object attributes and relations. An LLM first writes region captions from the attributes, then a whole-image caption with the relations. When the LLM conflicts with a specialist, the specialist wins. The captions are used for LMM training.
- Overlap: C4 **medium** (typed attribute and relation elements are rendered into a caption). C1 low-medium (specialists override, but nothing is verified or kept with a verdict).
- Distinguishing point: in EDC, specialist outputs are trusted inputs. In VSPS, every typed proposition is generated, then verified under three states, then selected under a budget. Rendering is constrained so that each span maps to a proposition and its verdict, and under-evidenced content is neutralized rather than added.
- Recommendation: **should cite** (a recent CVPR 2026 C4 neighbour).

### A11. Generating Accurate and Detailed Captions for High-Resolution Images
- H. Lee, G. Seo, K. Lee, D. Kim, et al. arXiv:2510.27164 (archival release; work done in 2024). No venue.
- Method: a VLM caption is passed to an LLM, which proposes likely co-occurring objects; a detector verifies them; region captions are added and undetected objects are removed.
- Overlap: C1 low-medium (verify and repair, but at test time). C4 low. Recommendation: optional.

## B. Decompose, verify, correct for detailed captions (C1 and C4 on the post-hoc side)

### B1. Toward Robust Hyper-Detailed Image Captioning: A Multiagent Approach and Dual Evaluation Metrics for Factuality and Coverage (CapMAS)
- S. Lee, S. Yoon, T. Bui, J. Shi, et al. ICML 2025 (PMLR); arXiv:2412.15484. Already cited as [10].
- Method: an LLM decomposes a detailed caption into atomic propositions, an MLLM checks each one against the image, and the LLM revises the caption. The paper also defines factuality and coverage metrics.
- Overlap: C4 **HIGH** on decomposition (atomic propositions verified one by one), but low on rendering (free LLM revision with no budget and no trace). C1 medium (CapMAS corrects outputs post hoc at inference; VSPS uses the same idea to build SFT data). C2 low (binary true/false score with a threshold).
- Distinguishing point: VSPS runs proposition verification once, offline, to build supervision, and the deployed model is single-pass. Verdicts have three states, with neutralization. The output is generated from typed propositions rather than by editing a free-text caption.
- Recommendation: **must cite & contrast**. The draft already cites it; make the "post hoc at inference vs. offline supervision" contrast explicit.

### B2. ReflectCAP: Detailed Image Captioning with Reflective Memory
- K. Min, M. Kim, K. Lee, S. Yoon, et al. Springer LNCS 2026, DOI 10.1007/978-3-032-37556-8_27 (OpenAlex); arXiv:2604.12357. Already cited as [11].
- Method: a multi-agent pipeline profiles what a target LVLM habitually hallucinates or omits, and distils this into "Structured Reflection Notes" that steer captioning at inference.
- Overlap: C1 low (guidance at inference time, no SFT). C4 low.
- Recommendation: should cite (already done). Update the reference to the LNCS DOI.

### B3. Unblocking Fine-Grained Evaluation of Detailed Captions: An Explaining AutoRater and Critic-and-Revise Pipeline (DOCCI-Critique)
- B. Gordon, Y. Bitton, A. Marzoca, Y. Onoe, et al. arXiv:2506.07631. No venue confirmed.
- Method: a benchmark of sentence-level factuality labels on DOCCI, an explaining autorater, and a critic-and-revise LLM pipeline that fixes flagged sentences.
- Overlap: C1 low (revision at test time), C4 low. Recommendation: optional.

### B4. CCCaption: Dual-Reward Reinforcement Learning for Complete and Correct Image Captioning
- Z. Tang, L. Wang, J. Qi, W. Jiang, et al. CVPR 2026; arXiv:2602.21655. Already cited as [18].
- Method: LVLMs break the image into visual queries, which give a completeness reward. A correctness penalty comes from validating decomposed sub-caption claims. Both drive RL on a dedicated corpus.
- Overlap: C1 **medium** (the same "decompose and verify claims at training time" idea, expressed as an RL reward rather than as SFT data). C4 low.
- Distinguishing point: VSPS changes the data (verified, rendered targets with a standard SFT loss), with no reward model and no RL. It is also the only one of the two with an explicit UNCERTAIN state.
- Recommendation: must cite & contrast (already done).

### B5. Bridging the Visual Gap: Fine-Tuning Multimodal Models with Knowledge-Adapted Captions (KnowAda)
- M. Yanuka, A. Ben Kish, Y. Bitton, I. Szpektor, et al. NAACL 2025 (ACL Anthology, long paper, pp. 10497–10518). DOI 10.18653/v1/2025.naacl-long.527; arXiv:2411.09018. Already cited as [12].
- Method: probes the VLM with questions about each caption to find details it cannot see, and rewrites those parts of the dense SFT captions so they fit the model's visual knowledge. Evaluation uses Decomposed NLI over propositions.
- Overlap: C1 **HIGH** (a data-centric change to SFT captions that reduces hallucination while keeping descriptiveness: the same thesis). C4 low-medium (propositions are used for evaluation, not for building targets). C2 low.
- Distinguishing point: KnowAda adapts **existing human captions** to the *student model's* knowledge, and its notion of "unknown" is model-relative. VSPS builds targets **from scratch without gold captions**, with an external verifier deciding image-relative support in three states. UNCERTAIN content is neutralized (gender) rather than removed, and the output is a traceable rendering from typed propositions.
- Recommendation: **must cite & contrast** (already done in RW; the draft calls it "closest"; keep the contrast sharp).

### B6. HalluciDoctor: Mitigating Hallucinatory Toxicity in Visual Instruction Data
- Q. Yu, J. Li, L. Wei, L. Pang, et al. CVPR 2024. DOI 10.1109/CVPR52733.2024.01230; arXiv:2311.13614.
- Method: extracts object, attribute and relation answer chunks from machine-generated instruction data, cross-checks them with several VQA answers (a consistency vote), removes hallucinated chunks, and then counterfactually expands the data. MLLMs are fine-tuned on the cleaned data.
- Overlap: C1 **HIGH** (offline verification of fine-grained claims cleans the SFT data, then standard SFT). C2 medium (agreement across multiple answers resembles VSPS's K-sampled vote, but the outcome is binary: delete). C4 low (deletes from existing text rather than rendering from propositions).
- Distinguishing point: HalluciDoctor *deletes* hallucinated spans from existing instruction data. VSPS *builds* detailed caption targets from typed propositions, with a third UNCERTAIN state, neutralization, budgeted selection and span traceability. VSPS also targets Vietnamese captioning, not instruction data.
- Recommendation: **must cite & contrast** (not in the draft; the most direct C1 precedent at CVPR).

### B7. Mitigating Fine-Grained Hallucination by Fine-Tuning Large Vision-Language Models with Caption Rewrites (ReCaption)
- L. Wang, J. He, S. Li, N. Liu, et al. MMM 2024 (Springer LNCS, Scopus). DOI 10.1007/978-3-031-53302-0_3; arXiv:2312.01701.
- Method: ChatGPT rewrites captions, and LVLMs are fine-tuned on the rewrites to reduce fine-grained hallucination. There is no explicit verification.
- Overlap: C1 low-medium (fixes hallucination at the data level through SFT, but without verification). Recommendation: should cite (one line).

## C. Structured / scene-graph representations and grounded rendering (C4)

### C1'. Graph-Based Captioning (GBC): Enhancing Visual Descriptions by Interconnecting Region Captions
- Y.-G. Hsieh, C.-Y. Hsieh, S.-Y. Yeh, L. Béthune, et al. arXiv:2407.06723. No venue confirmed.
- Method: annotates images as labelled graphs (entity, composition and relation nodes, each holding text), produced automatically with MLLMs and detectors; GBC10M dataset.
- Overlap: C4 medium (typed structured units, but these are the annotation itself, not verified, and not rendered into a single target). C1 low. Recommendation: should cite.

### C2'. Panoptic Captioning: An Equivalence Bridge for Image and Text
- K.-Y. Lin, H. Wang, W. Ren, K. Han. NeurIPS 2025. DOI 10.52202/085713-2631; arXiv:2505.16334.
- Method: defines captions that list every entity with its semantic tag, location, attributes and relations, plus a global state. Proposes a data engine and an entity-aware evaluation.
- Overlap: C4 low-medium (typed entity, attribute and relation slots). C1 low. Recommendation: optional.

### C3'. Visual Clues: Bridging Vision and Language Foundations for Image Paragraph Captioning
- Y. Xie, L. Zhou, X. Dai, L. Yuan, et al. NeurIPS 2022. DOI 10.52202/068431-1257; arXiv:2206.01843.
- Method: a vision foundation model builds structured "visual clues" (tags, object attributes and locations, captions). An LLM writes several paragraphs from them, and the vision model re-verifies the candidates to pick the best-aligned one.
- Overlap: C4 **medium** (structured elements are rendered by an LLM, then verified; an early precursor). C1 low (no training). Its verification scores whole paragraphs, not propositions.
- Recommendation: should cite as a seminal precursor of "render from structured elements, then verify".

### C4'. Neural Baby Talk
- J. Lu, J. Yang, D. Batra, D. Parikh. CVPR 2018. DOI 10.1109/CVPR.2018.00754; arXiv:1803.09845.
- Method: generates a sentence template with slots that are filled by detector-grounded region words. Every visual word is tied to a detection.
- Overlap: C4 medium (template rendering where visual words are traceable to grounded evidence; the seminal precursor of slot-grounded rendering). Not a 2023–2026 paper, but its overlap is medium.
- Distinguishing point: in NBT the grounding is a detection, not a verified proposition with a verdict. It covers only short captions and does not use the output as supervision for an MLLM.
- Recommendation: should cite (for the traceable template path).

### C5'. GLaMM: Pixel Grounding Large Multimodal Model
- H. Rasheed, M. Maaz, S. S. Mullappilly, A. Shaker, et al. CVPR 2024. DOI 10.1109/CVPR52733.2024.01236; arXiv:2311.03356.
- Method: grounded conversation generation, where caption phrases are interleaved with segmentation masks. Its GranD data come from an automated multi-level annotation pipeline.
- Overlap: C4 low-medium (phrase-level traceability, but to pixels, not to verified propositions). C1 low. Recommendation: optional.

### C6'. The All-Seeing Project V2: Towards General Relation Comprehension of the Open World (ASMv2)
- W. Wang, Y. Ren, H. Luo, T. Li, et al. ECCV 2024 (Springer LNCS). DOI 10.1007/978-3-031-73414-4_27; arXiv:2402.19474.
- Method: the "Relation Conversation" format links text to object boxes and relation predicates. Includes the AS-V2 dataset and the CRPE relation-hallucination benchmark.
- Overlap: C4 low-medium (structured relation-grounded text), C1 low. Useful contrast: VSPS caps spatial relations at UNCERTAIN because it has no boxes, while ASMv2 supplies boxes. Recommendation: optional (cite if the relation cap is discussed).

### C7'. Davidsonian Scene Graph (DSG)
- J. Cho, Y. Hu, R. Garg, P. Anderson, et al. ICLR 2024; arXiv:2310.18235.
- Method: atomic, typed (entity, attribute, relation, global), dependency-aware questions for VQA-based verification in text-to-image evaluation.
- Overlap: C4 medium on the *typing and dependency* of propositions (justifies VSPS's typed propositions and the parent-entity gate). It is an evaluation method, not a generation method. Recommendation: should cite (Q2_LITERATURE already lists it).

## D. Human-written detailed-description datasets (context only)

- **DOCCI**, Y. Onoe et al., ECCV 2024, DOI 10.1007/978-3-031-73027-6_17, arXiv:2404.19753. Overlap none; optional (as a possible English evaluation set).
- **ImageInWords (IIW)**, R. Garg et al., EMNLP 2024, DOI 10.18653/v1/2024.emnlp-main.6, arXiv:2405.02793. Uses human-in-the-loop sequential, object-first annotation; C4 low (object-then-image composition is conceptually similar). Optional.
- **DCI (Densely Captioned Images)**, J. Urbanek et al., arXiv:2312.08578 (CVPR 2024, venue not cross-checked). Overlap none; optional.

## E. Detailed-caption evaluation that decomposes into facts (C5-adjacent, low overlap here)

- **DeCapBench / DCScore + FeedQuill**, Q. Ye et al., ICLR 2025, arXiv:2503.07906. Primitive information units, plus preference optimization from fine-grained feedback. C1 low-medium (feedback is for DPO, not SFT data). Should cite (relevant to the DPO negative result).
- **CompreCap**, F. Lu et al., CVPR 2025, DOI 10.1109/CVPR52734.2025.01827, arXiv:2412.08614. Directed scene-graph benchmark for comprehensive captioning. Optional.
- **CapProbe**, M. Huang et al., arXiv:2608.11074. Dense region QA evaluation with an explicit "Uncertain" option for the judge. C2 low; optional.
- **DetailVerifyBench**, X. Wang et al., arXiv:2604.05623. Token-level hallucination localization in long captions. Optional.
- **A Glance Is All You Need (SimLoss)**, S. Jain et al., arXiv:2609.00591. Single-pass detailed captioning with an embedding-space InfoNCE loss, presented as an alternative to multi-stage decompose-verify-rewrite pipelines. C1 low: it adds a loss term, whereas VSPS uses the plain SFT loss. Optional, but it is a good foil for the "single pass at deployment" argument.

## Unverified / not found
- No paper found that renders captions **from verified typed propositions** with an explicit **span ← proposition ← verdict** trace, plus budgeted selection. Searches covered scene-graph-to-caption, fact-to-text, traceable captioning and structured captions for 2023–2026.
- No paper found with a three-state (SUPPORTED/UNCERTAIN/REJECTED) verdict used to build caption supervision. CapProbe's "Uncertain" option belongs to an evaluation judge, not to supervision.

---

## Highest-overlap risks
1. **HalluciDoctor** (CVPR 2024): offline cross-checking of object, attribute and relation claims by multi-answer VQA consistency, then SFT on the cleaned data. A HIGH C1 overlap that the draft does not cite. Contrast: deletion from existing text vs. constructive rendering from typed propositions; binary vs. three-state with neutralization.
2. **Image Textualization** (NeurIPS 2024 D&B): verifying with vision experts, then removing hallucinations, then recaptioning, then SFT reduces hallucination. HIGH on C1 and not cited. Contrast: object-only binary filtering vs. typed propositions with UNCERTAIN handling and traceable rendering.
3. **KnowAda** (NAACL 2025, cited [12]): data-centric adaptation of SFT captions. HIGH on C1. Contrast: model-relative knowledge vs. image-relative three-state verification; gold-caption editing vs. gold-free construction.
4. **CapMAS / Lee et al.** (ICML 2025, cited [10]): atomic-proposition decomposition plus per-proposition MLLM verification. HIGH on the decomposition half of C4. Contrast: correction at inference vs. offline supervision; free revision vs. budgeted, traceable rendering.
5. **Visual Fact Checker** (CVPR 2024) and **EDC** (CVPR 2026): compose detailed captions from tool- or specialist-verified elements. Medium on C1 and C4, neither cited. Contrast: no per-claim verdict store, no budget, no span trace, and an inference-time pipeline (VFC).

## Suggested novelty statement (topic 06)
"Caption-data engines such as Image Textualization, Visual Fact Checker and HalluciDoctor verify claims with vision experts or VQA consistency, but they keep or delete each claim and then let an LLM rewrite freely. VSPS instead builds each supervision caption only from typed propositions carrying a three-state verdict, selected under a budget and rendered so that every span traces to its proposition and verdict. Uncertain content is neutralized rather than discarded, and verification runs once offline, so the deployed model stays single-pass and is trained with a standard SFT loss."
