# 02 — Claim / proposition decomposition and verification (overlap focus: C1, C2, C4)

Agent 02. Searched: OpenAlex title search, Crossref DOI lookups, arXiv abstract/HTML pages, web search (2024–2026).
"Verified" below means I opened the arXiv abstract or HTML page, or confirmed the DOI through Crossref or OpenAlex, in this pass. Items taken from Q2_LITERATURE.md without re-opening them are marked *(from Q2 scan)*.
Scopus note: IEEE/CVF CVPR/ICCV proceedings, IEEE ICASSP, AAAI, and Springer LNCS (ECCV) are normally Scopus-indexed. ACL Anthology venues are indexed only in part, so check those per item. arXiv-only means no peer-reviewed venue was found.

Current state of the paper: VSPS cites FaithScore [4], CapMAS [10], KnowAda [12], LURE [14], Woodpecker [15] and CCCaption [18]. It does **not** cite RLAIF-V, HalluciDoctor, Visual Fact Checker, Image Textualization, FGAIF, HSA-DPO, SENTINEL, FeedQuill/DCScore, DSG or ClaimDiff-RL. HalluciDoctor and RLAIF-V are the two most likely reviewer objections.

---

## A. Verification used to build SFT / instruction data (C1 core)

### A1. HalluciDoctor: Mitigating Hallucinatory Toxicity in Visual Instruction Data
- Q. Yu, J. Li, L. Wei, L. Pang, et al. CVPR 2024 (IEEE/CVF, Scopus). DOI 10.1109/CVPR52733.2024.01230; arXiv:2311.13614. I confirmed the DOI via OpenAlex and read the method in the HTML.
- **Method:** A textual scene-graph parser splits each GPT-4 instruction-data description into **object, attribute and relation "answer chunks"**. ChatGPT writes one question per chunk. Several MLLM experts (BLIP-2, InstructBLIP, MiniGPT-4) answer each question. BEM consistency is averaged across experts, and a chunk with ConScore < 0.5 is treated as hallucinatory and removed by ChatGPT. The cleaned data (LLaVA+) is then used to **instruction-tune** MiniGPT-4 and mPLUG-Owl. A further step adds counterfactual instruction expansion.
- **Overlap:**
  - **C1: HIGH.** It uses fine-grained verification of typed units to clean SFT data, with a standard fine-tuning loss.
  - C2: low. The verdict is binary (keep or remove) and comes from a soft similarity threshold. There is no "not visible ≠ false" state.
  - C4: medium. It uses typed chunks, but the cleaned text is an LLM rewrite of the original description, so no span is traceable to a verdict.
- **VSPS distinguishing point:** HalluciDoctor cleans existing human/GPT-4 instruction text. VSPS generates candidate propositions for the image itself, without gold captions, and keeps a separate UNCERTAIN state. That state triggers neutralization (C3) instead of deletion. VSPS also renders the target only from verified propositions, so every span traces back to one, whereas HalluciDoctor rewrites the original prose.
- **Recommendation:** **Must cite and contrast.** This is the oldest peer-reviewed "verify fine-grained units, then clean SFT data" precedent.

### A2. KnowAda: Bridging the Visual Gap: Fine-Tuning Multimodal Models with Knowledge-Adapted Captions *(from Q2 scan, already cited as [12])*
- M. Yanuka et al. NAACL 2025. arXiv:2411.09018. I confirmed the abstract via web search in this pass.
- **Method:** KnowAda generates questions from each caption and probes the target VLM with them. Details the model fails on are rewritten out of the caption, and the model is fine-tuned on the adapted captions. A threshold controls the precision/recall trade-off. Captions are decomposed into propositions for evaluation.
- **Overlap:**
  - **C1: HIGH.** It is data-level SFT-target adaptation that reduces hallucination.
  - C2: low. Its criterion is "the model doesn't know this," not a judgement of visual evidence.
  - C4: low.
- **VSPS distinguishing point:** KnowAda uses the student model's knowledge as the filter. VSPS uses a verifier's judgement of visual evidence and keeps a three-state verdict. KnowAda removes unknown details, while VSPS neutralizes uncertain ones. VSPS also builds targets from propositions rather than editing gold captions.
- **Recommendation:** Must cite and contrast (already done; keep it).

### A3. Image Textualization: An Automatic Framework for Creating Accurate and Detailed Image Descriptions
- R. Pi, J. Zhang, J. Zhang, R. Pan, Z. Chen, T. Zhang. arXiv:2406.07502 (2024). I opened the abstract and HTML. No venue is shown on arXiv or in OpenAlex.
- **Method:**
  1. An MLLM writes a reference description.
  2. An LLM extracts object phrases. Grounding DINO checks each one, and phrases it cannot find are tagged "Hallucination." A dense captioner, SAM and a depth model add object-level facts as text.
  3. A text-only LLM recaptions from these textualized facts.
  The resulting descriptions are used to fine-tune LLaVA-7B.
- **Overlap:**
  - **C1: medium-high.** It is verified, generated captions used as SFT data.
  - C2: low. The verdict is binary and comes from detector presence.
  - **C4: medium.** The caption is rendered from a structured fact layer without the image, which is similar to VSPS's renderer. There is no per-span traceability, and the facts are untyped.
- **VSPS distinguishing point:** VSPS verifies at the proposition level across five types (entity, attribute, action, count, relation), not just object existence. It uses three states, and its renderer is template- or constrained-LM-based with span-to-proposition tracing.
- **Recommendation:** Should cite.

### A4. Visually Dehallucinative Instruction Generation (CAP2QA)
- S. Cha, J. Lee, Y. Lee, C. Yang. ICASSP 2024 (IEEE, Scopus). arXiv:2402.08348. I opened the abstract, whose comments say "Accepted at ICASSP 2024."
- **Method:** It generates visual-instruction QA pairs that are constrained to the content of human-annotated captions, which reduces hallucination in instruction-tuned models.
- **Overlap:** C1 low-medium (grounded SFT data, but only through scope restriction, with no verification). C2: none. C4: none.
- **Distinguishing point:** VSPS verifies against the image instead of trusting gold captions, and does not use gold captions at all.
- **Recommendation:** Optional.

## B. Claim decomposition + AI verification feeding preference or RL rewards (C1 contrast, C2, C4)

### B1. RLAIF-V: Open-Source AI Feedback Leads to Super GPT-4V Trustworthiness
- T. Yu, H. Zhang, Q. Li, Q. Xu, et al. CVPR 2025 (IEEE/CVF, Scopus). DOI 10.1109/CVPR52734.2025.01861; arXiv:2405.17220. I confirmed the DOI via OpenAlex and read the method in the HTML.
- **Method:** "Divide-and-conquer" feedback:
  1. An LLM splits each response into atomic claims.
  2. Each claim becomes a polar yes/no question.
  3. An open-source MLLM labeler outputs (p_yes, p_no), and a claim is rejected if p_no > p_yes.
  4. The response score is minus the number of rejected claims.
  5. Preference pairs are built from these scores, length-matched, and trained with iterative DPO.
- **Overlap:**
  - **C1: medium.** The verification-to-training-data pipeline is the same, but the output is DPO preference pairs, not SFT targets.
  - **C2: medium.** It also uses yes/no claim queries to a VLM. However, it has one affirmative query, a binary verdict from a single forward pass, and no UNCERTAIN state, negated query or sampling.
  - C4: low. Its claims are untyped free text.
- **VSPS distinguishing point:**
  - RLAIF-V turns claim verdicts into a ranking signal over whole responses. VSPS turns them into the content of the target itself, through selection and rendering, and trains with plain SFT.
  - VSPS's dual affirmative + negated queries with K=5 sampled answers produce a three-way verdict. RLAIF-V uses a p_yes vs p_no argmax.
- **Recommendation:** **Must cite and contrast.** It is the closest claim-level AI-feedback method, and reviewers will name it.

### B2. FGAIF: Aligning Large Vision-Language Models with Fine-grained AI Feedback
- L. Jing, X. Du (the FaithScore authors). arXiv:2404.05046 (2024). I opened the abstract. No venue is listed on arXiv or in OpenAlex.
- **Method:** AI tools label the hallucination type of each response segment: object existence, attribute or relation. Three type-specific reward models are trained on these labels, and their dense segment-level rewards are used in PPO.
- **Overlap:** C1 low (RL, not SFT data). C2 low (binary). **C4 medium** (typed fine-grained units: object, attribute, relation).
- **Distinguishing point:** VSPS uses typed propositions as the building blocks of supervision, not as reward channels. Its types also include count and action.
- **Recommendation:** Should cite.

### B3. Detecting and Mitigating Hallucination in LVLMs via Fine-Grained AI Feedback (HSA-DPO)
- W. Xiao, Z. Huang, L. Gan, W. He, et al. AAAI 2025 (Scopus). DOI 10.1609/aaai.v39i24.34744 (confirmed via Crossref); arXiv:2404.14233.
- **Method:** A sentence-level hallucination detector for object, attribute and relation errors is trained on annotations from proprietary models. A detect-then-rewrite pipeline then builds preference pairs, which are trained with severity-aware DPO.
- **Overlap:** C1 low-medium (verification → data, but preference data). C2 low. C4 low.
- **Distinguishing point:** HSA-DPO works at sentence level with a binary verdict and DPO. VSPS works at proposition level with three states and SFT.
- **Recommendation:** Should cite.

### B4. Mitigating Object Hallucinations via Sentence-Level Early Intervention (SENTINEL)
- S. Peng, S. Yang, L. Jiang, Z. Tian. ICCV 2025 (IEEE/CVF, Scopus). DOI 10.1109/ICCV51701.2025.00067 (confirmed via Crossref); arXiv:2507.12455. I read the method in the HTML.
- **Method:** Each object in sampled outputs is checked by two open-vocabulary detectors, GroundingDINO and YOLO-World. An object is **hallucinated** if both confirm it is absent, **factual** if both confirm it is present, and **uncertain** if they conflict. The paper states: "we ignore uncertain objects." Sentence-level preference pairs are trained with C-DPO.
- **Overlap:**
  - **C2: medium-high.** It explicitly uses a three-way verdict, with a disagreement-based "uncertain" state that is excluded from the training signal. This is the closest precedent for VSPS's "a split vote closes the evidence gate."
  - C1: medium (offline verification → training data, but DPO).
  - C4: low (objects only).
- **Distinguishing point:**
  - SENTINEL's uncertain state comes from two detectors disagreeing, covers object existence only, and is simply dropped.
  - VSPS's UNCERTAIN state comes from agreement across K=5 samples of affirmative and negated queries, and covers attributes, actions, counts and relations.
  - VSPS uses the UNCERTAIN state constructively by neutralizing the proposition to its verifiable part (C3) instead of dropping it, and the target is SFT supervision.
- **Recommendation:** **Must cite and contrast for C2.** VSPS cannot claim that a three-state verdict for training-data construction is new on its own.

### B5. Painting with Words (DCScore / DeCapBench / FeedQuill)
- Q. Ye, X. Zeng, F. Li, C. Li, H. Fan. ICLR 2025 (per the arXiv comments; not Scopus-indexed as a proceedings volume). arXiv:2503.07906. I read FeedQuill in the HTML.
- **Method:** An LLM decomposes responses into "self-sufficient and verifiable" primitive units. An ensemble of open VLMs (InternVL-2, LLaVA-NeXT) answers a yes/no question for each unit. The fraction of units judged correct becomes the preference score, which trains reward models that are then used in PPO. DCScore applies the same units as a precision/recall evaluation metric.
- **Overlap:** C1 medium. C2 medium (yes/no with multiple verifiers, but a binary verdict). C4 low-medium.
- **Distinguishing point:** VSPS uses sampled affirmative and negated queries with an explicit uncertain state. It builds SFT targets rather than PPO rewards.
- **Recommendation:** Should cite. DCScore is also a candidate evaluation metric.

### B6. ClaimDiff-RL: Fine-Grained Caption Reinforcement Learning through Visual Claim Comparison
- T. Li, X. Shen, Y. Ma, R. Guo, et al. arXiv:2605.20278 (May 2026, arXiv only). I opened the abstract and HTML.
- **Method:** A multimodal judge (Gemini-3-Pro-preview) lists the claim-level differences between an actor caption and a reference caption, verifies each against the image, and assigns error types and severities. These claim-level statistics form an RL reward that balances faithfulness against coverage. A regex hedge penalty discourages over-hedging. Its diagnostic protocol labels claims **verified / false / ambiguous**, with "ambiguous: cannot determine from image," and ambiguous claims are "conservatively treated as non-hallucinations."
- **Overlap:** C2 medium (a three-way verdict that includes "cannot determine," but used only for evaluation and counted as not-hallucinated). C1 low (RL). C4 low.
- **Distinguishing point:** VSPS keeps UNCERTAIN content out of the supervision, or neutralizes it. ClaimDiff-RL counts it as acceptable. The paper also reports that holistic rewards cut hallucination by under-captioning, which supports VSPS's recall-aware framing.
- **Recommendation:** Should cite. It is the 2026 RL counterpart, alongside CCCaption [18].

### B7. ViGoR: Improving Visual Grounding of LVLMs with Fine-Grained Reward Modeling
- S. Yan, M. Bai, W. Chen, X. Zhou, et al. ECCV 2024, LNCS (Springer, Scopus). DOI 10.1007/978-3-031-73030-6_3 (via OpenAlex); arXiv:2402.06118.
- **Method:** Fine-grained human feedback plus automatic detector-based feedback trains a reward model for grounding. The model is then fine-tuned with that reward.
- **Overlap:** C1 low. C2 none. C4 low.
- **Recommendation:** Optional.

### B8. ESREAL: Exploiting Semantic Reconstruction to Mitigate Hallucinations in VLMs
- M. Kim et al. arXiv:2403.16167 (2024). The record was confirmed via OpenAlex. Its venue (I believe ECCV 2024) was **not confirmed** in this pass.
- **Method:** The image is reconstructed from the generated caption, and token-level hallucination penalties are computed by comparing regions. These penalties drive RL.
- **Overlap:** low on C1, C2 and C4.
- **Recommendation:** Optional.

### B9. A Topic-level Self-Correctional Approach to Mitigate Hallucinations in MLLMs (TPO)
- L. He et al. arXiv:2411.17265. It was later extended as "Systematic Reward Gap Optimization for Mitigating VLM Hallucinations" (TPR), listed as a NeurIPS 2025 poster. Both were confirmed via web search; I did not open the PDF.
- **Method:** Responses are decomposed into topics or claims. Each topic is replaced with the model's own best or worst resampled alternatives, which builds contrastive preference pairs for DPO.
- **Overlap:** C1 low-medium. C2 low. C4 low.
- **Recommendation:** Optional.

## C. Training-free decompose → verify → rewrite pipelines (C1 contrast: VSPS moves this offline into data)

### C1-a. Visual Fact Checker (VFC): Enabling High-Fidelity Detailed Caption Generation
- Y. Ge, X. Zeng, J. S. Huffman, T.-Y. Lin, et al. CVPR 2024 (IEEE/CVF, Scopus). DOI 10.1109/CVPR52733.2024.01331 (via OpenAlex); arXiv:2404.19752.
- **Method:** Training-free. Multiple captioners propose captions. An LLM extracts objects and attributes and checks them with a detector and VQA tools, and undetected objects are removed. An LLM then writes the final caption.
- **Overlap:** C1 medium (it is the same pipeline VSPS uses offline). C2 low (binary, detector-based). C4 medium (verified facts are rendered by an LLM).
- **Distinguishing point:** VFC runs the full multi-model pipeline at inference time. VSPS runs it once offline to build supervision and deploys a single-pass model. VSPS also adds three states and span traceability.
- **Recommendation:** **Must cite.** It is the most obvious prior art for "proposition-checked detailed captions."

### C1-b. Toward Robust Hyper-Detailed Image Captioning (CapMAS) *(from Q2 scan, already cited as [10])*
- S. Lee et al. ICML 2025. arXiv:2412.15484.
- **Method:** Captions are split into atomic propositions. An MLLM probes each one as True/False, using the probability gap between the two answers. A multi-agent rewrite follows, and the paper adds factuality and coverage metrics.
- **Overlap:** C1 low (training-free). C2 medium (proposition-level true/false scoring). C4 medium.
- **Recommendation:** Already cited. Sharpen the contrast: CapMAS is inference-time with a binary/continuous score, whereas VSPS is data-level with three states.

### C1-c. Woodpecker: Hallucination Correction for MLLMs *(from Q2 scan, already cited as [15])*
- S. Yin et al. Sci. China Inf. Sci. 67(12), 2024 (Springer, Scopus). DOI 10.1007/s11432-024-4251-x.
- **Method:** Key-concept extraction, then question formulation for counts and attributes, then validation with GroundingDINO and BLIP-2 VQA, then visual-claim generation and correction.
- **Overlap:** C1 low (post hoc). C2 low. C4 medium (typed checks for existence, count and attribute).
- **Recommendation:** Already cited. Keep it.

### C1-d. Generating Accurate and Detailed Captions for High-Resolution Images
- H. Lee, G. Seo, K. Lee, D. Kim, K. Song, J. Jung. arXiv:2510.27164 (2025, archival release of 2024 work; arXiv only).
- **Method:** VLM caption → LLM object and co-occurrence prediction → detector verification → removal of undetected objects and region captioning of missed ones. Training-free.
- **Overlap:** low.
- **Recommendation:** Optional.

### C1-e. Semantic-Spatial Agreement Verification (SSAV)
- Z. Ren et al. arXiv:2609.17269 (Sept 2026, arXiv only).
- **Method:** Training-free verification of object claims that fuses multi-prompt semantic agreement with spatial region evidence.
- **Overlap:** C2 low-medium (agreement over multiple prompts, at inference time only).
- **Recommendation:** Optional.

## D. Atomic-fact representations and verification for evaluation (C4 typing precedent)

### D1. FaithScore *(already cited as [4])*
- L. Jing, R. Li, Y. Chen, X. Du. Findings of EMNLP 2024. DOI 10.18653/v1/2024.findings-emnlp.290 (via OpenAlex).
- **Method:** It identifies descriptive sentences, decomposes them into **typed atomic facts** (entity, count, colour, relation, other attribute), and verifies each with a visual-entailment model.
- **Overlap:** **C4 medium-high on the typing itself.** The VSPS types are essentially the FaithScore and DSG taxonomies. C1: none (evaluation only).
- **Distinguishing point:** VSPS uses the typed units as the unit of supervision and rendering, not of scoring.
- **Recommendation:** Already cited. State explicitly that the proposition types follow FaithScore/DSG-style atomic facts, and do not claim the typing as new.

### D2. Davidsonian Scene Graph (DSG) *(from Q2 scan)*
- J. Cho et al. ICLR 2024. arXiv:2310.18235 (confirmed via OpenAlex).
- **Method:** Atomic, dependency-aware tuples (entity, attribute, relation, global) are turned into VQA questions. Parent-child dependencies skip questions about children when the parent fails.
- **Overlap:** C4 medium. Its entity registry and dependency gating resemble VSPS ceiling rules, under which a verdict may only be lowered.
- **Recommendation:** Should cite.

### D3. FIHA: Automated Fine-grained Hallucination Evaluations in LVLMs with Davidson Scene Graphs
- B. Yan, Z. Zhang, L. Jing, E. Hossain, et al. Findings of ACL 2025. DOI 10.18653/v1/2025.findings-acl.622 (via OpenAlex); arXiv:2409.13612.
- **Method:** Builds hallucination QA from DSG-structured image facts (objects, attributes, relations). Evaluation only.
- **Overlap:** C4 low-medium.
- **Recommendation:** Optional.

### D4. UNIHD (Unified Hallucination Detection for MLLMs)
- X. Chen et al. ACL 2024. DOI 10.18653/v1/2024.acl-long.178 (via OpenAlex).
- **Method:** Claim extraction, then tool-based verification (detector, OCR, search) for detection.
- **Overlap:** C2 low. C4 low-medium.
- **Recommendation:** Optional.

### D5. Graph-Based Captioning (GBC)
- Y.-G. Hsieh, C.-Y. Hsieh, S.-Y. Yeh, et al. (Apple). arXiv:2407.06723 (2024/2025, arXiv only).
- **Method:** A labeled graph of entity, composition and relation nodes is built automatically with MLLMs and detectors (GBC10M), and used to train CLIP.
- **Overlap:** C4 low-medium (structured typed units as training data, but no verification and no rendering for SFT).
- **Recommendation:** Optional.

## E. Domain-transfer analogue

### E1. FactCheXcker: Mitigating Measurement Hallucinations in Chest X-ray Report Generation Models
- A. Heiman, X. Zhang, E. Chen, S.-E. Kim, P. Rajpurkar. CVPR 2025 (IEEE/CVF, Scopus). DOI 10.1109/CVPR52734.2025.02867 (confirmed via Crossref); arXiv:2411.18672.
- **Method:** Post hoc. It generates queries for measurement claims in reports, executes code to check them against image-derived measurements, and updates the report.
- **Overlap:** low on all claims (post hoc, medical, measurement-specific).
- **Recommendation:** Optional. Cite it only if the journal version discusses deployment cost.

## Unverified / not re-checked in this pass
- **Tri-HE**: "Unified Triplet-Level Hallucination Evaluation for LVLMs." OpenAlex lookup failed and the exact ID was not confirmed.
- **ESREAL** venue (possibly ECCV 2024): not confirmed.
- **TPO** venue: not confirmed. Only its follow-up TPR shows as a NeurIPS 2025 poster.
- **Image Textualization** venue: none found. Do not cite it as NeurIPS.
- **LogicCheckGPT** (ACL 2024, arXiv:2402.11622): relevant to the C2 negated-query probing, but taken from the Q2 scan and not re-opened. Agents covering consistency/uncertainty should check it.

---

## Highest-overlap risks
1. **HalluciDoctor (CVPR 2024): HIGH on C1.** It verifies typed object/attribute/relation units with several MLLM experts and removes failures from SFT data. VSPS must say it generates supervision from verified propositions without gold text, keeps UNCERTAIN, and neutralizes rather than removes.
2. **KnowAda (NAACL 2025): HIGH on C1** (already cited). Its filter is the model's knowledge, while VSPS's filter is visual evidence with three states.
3. **SENTINEL (ICCV 2025): medium-high on C2.** It already has a hallucinated/factual/uncertain verdict from detector disagreement, and it drops uncertain items from training. VSPS's novelty must rest on the *source* of uncertainty (sampled affirmative + negated VQA, any proposition type) and on *using* it (neutralization, C3), not on having three states.
4. **RLAIF-V (CVPR 2025): medium on C1 and C2.** It has the same atomic-claim → yes/no VLM verification → training-data loop, but for DPO with a binary verdict.
5. **Visual Fact Checker (CVPR 2024) and Image Textualization (arXiv 2024): medium on C1 and C4.** Both run verify-then-render-from-facts. VFC does it at inference time, while Image Textualization uses it as SFT data with object-only detector checks.

Other notes:
- Typed atomic facts (C4) are prior art through FaithScore and DSG. Present them as an adopted representation. The novel part is span-level traceability from rendered target to proposition and verdict.
- None of the papers found combines (i) proposition-level verification for SFT targets, (ii) a three-state verdict built from sampled affirmative + negated queries, and (iii) neutralization of uncertain propositions. The combination stays defensible, though no single component is new on its own.

## Suggested novelty statement (this topic)
"Prior work decomposes responses into atomic claims and verifies them with VLMs, but uses the verdicts either to correct outputs at inference time (Woodpecker, VFC, CapMAS), to rank responses for preference or RL training (RLAIF-V, HSA-DPO, FeedQuill, SENTINEL, ClaimDiff-RL), or to delete flagged spans from existing instruction text (HalluciDoctor, KnowAda). VSPS instead constructs the SFT target itself from typed propositions verified with a three-state verdict. Only SUPPORTED propositions and the verifiable residue of UNCERTAIN ones enter the target, and every rendered span traces back to one proposition and its verdict."
