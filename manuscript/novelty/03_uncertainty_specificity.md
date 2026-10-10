# 03 — Uncertainty-aware captioning, abstention, hedging, controllable specificity

Agent 03. Focus: overlap with C2 (three-state SUPPORTED/UNCERTAIN/REJECTED verification) and especially C3 (neutralization: an UNCERTAIN proposition is reduced to its still-verifiable part, for example "người phụ nữ" → "người").
Every entry below was confirmed on arXiv, the proceedings, or IEEE Xplore on 2026-10-10. Items not in Q2_LITERATURE.md are marked NEW.

## A. Specificity back-off / "less specific when unsure" (main C3 risk)

### A1. Conformal Linguistic Calibration: Trading-off between Factuality and Specificity — NEW
- Authors: Zhengping Jiang, Anqi Liu, Benjamin Van Durme
- Venue: NeurIPS 2025 main track (papers.neurips.cc, hash bce2501dd4edbc5d5757a1453757e883). Not IEEE, Elsevier, Springer or ACM. NeurIPS proceedings are Scopus-indexed.
- Link: arXiv:2502.19110
- Method: Treats linguistic calibration as answer-set prediction. Samples about 100 answers, clusters them into nested sets, and has GPT-4o write a less specific claim per set (e.g., "played 10 ODIs" becomes "played a positive-integer number of ODIs"). Picks the back-off level conformally (LTT), then SFT/DPO/ORPO-tunes Llama-3-8B to rewrite claims to the calibrated specificity. Text-only QA.
- Overlap: **C3 HIGH (conceptual)**. It is the same principle: an uncertain claim is rewritten to a less specific but still true claim, and the rewrites become SFT data. **C2 low**. **C1 medium**: the rewrites are fine-tuning targets.
- VSPS distinction: Multimodal and visual-evidence-driven. The uncertainty comes from dual affirmative/negated VQA votes on the image, not answer-set clustering over parametric knowledge. Back-off is a deterministic, typed operation (drop the under-evidenced component of a proposition, e.g. gender in a Vietnamese person noun), recovered offline from stored evidence with no LLM rewriter. It applies to captions, not QA answers. There is no conformal guarantee, and VSPS should not imply one.
- Recommendation: **must cite & contrast**.

### A2. Language Models with Conformal Factuality Guarantees — NEW
- Authors: Christopher Mohri, Tatsunori Hashimoto
- Venue: ICML 2024, PMLR 235:36029–36047. Not one of the four publishers; PMLR is Scopus-indexed.
- Link: arXiv:2402.10978
- Method: Frames conformal prediction for LMs as a back-off procedure that makes outputs progressively less specific until correctness holds with high probability. Black-box; tested on FActScore, NQ and MATH. In practice the back-off removes sub-claims.
- Overlap: **C3 medium** (the "back off to less specific" framing). **C1 low**: it works at inference, not on training data.
- VSPS distinction: It is a deployment-time filter with a statistical guarantee. VSPS reduces specificity offline in the supervision data, and the deployed model is single-pass.
- Recommendation: **should cite**, alongside A1.

### A3. Hedging Your Bets: Optimizing Accuracy-Specificity Trade-offs in Large Scale Visual Recognition (seminal)
- Authors: Jia Deng, Jonathan Krause, Alexander C. Berg, Li Fei-Fei
- Venue: CVPR 2012, IEEE, Scopus-indexed. DOI 10.1109/CVPR.2012.6248086 (IEEE Xplore doc 6248086).
- Method: The classifier backs off to a broader node in the WordNet hierarchy when uncertain (the DARTS algorithm), maximising information gain under an accuracy target.
- Overlap: **C3 medium**. This is the canonical visual hypernym back-off: "người" works as a hypernym of "người phụ nữ".
- VSPS distinction: Deng et al. back off a single classification label using a classifier's posteriors. VSPS backs off one component of a caption proposition, gated by VQA evidence, and uses the result to train a generator.
- Recommendation: **should cite**. It is good lineage and helps frame neutralization as accuracy-specificity hedging.

### A4. Towards Statistical Factuality Guarantee for Large Vision-Language Models (ConfLVLM) — NEW
- Authors: Zhuohang Li, Chao Yan, Nicholas J. Jackson, Wendi Cui, Bo Li, Jiaxin Zhang, Bradley A. Malin
- Venue: EMNLP 2025 main (ACL Anthology 2025.emnlp-main.576). ACL, not one of the four publishers; Scopus-indexed.
- Link: arXiv:2502.20560
- Method: Decomposes LVLM scene descriptions into claims, tests each claim against an uncertainty score with a conformal hypothesis test, and removes the unreliable ones. Reports LLaVA-1.5 claim error falling from 87.8% to 10.0%.
- Overlap: **C2 medium** (claim-level uncertainty gating on images). **C3 low**: claims are dropped, not reduced. **C1 low**: it runs at inference.
- VSPS distinction: ConfLVLM is a binary keep/drop filter at deployment. VSPS keeps a three-way verdict, reduces UNCERTAIN claims instead of deleting them, and trains the gated data into the model so no filter is needed at inference.
- Recommendation: **must cite & contrast**. It is the closest multimodal "uncertain-claim gating" work.

## B. Controllable specificity in detailed captioning

### B1. HallE-Control: Controlling Object Hallucination in Large Multimodal Models (earlier version: "HallE-Switch")
- Authors: Bohan Zhai, Shijia Yang, Chenfeng Xu, Sheng Shen, Kurt Keutzer, Chunyuan Li, Manling Li
- Venue: arXiv only (v3, 28 Mar 2024); no venue listed.
- Link: arXiv:2310.01779
- Method: RAM splits COCO objects into "grounded" and "omitted". GPT-4 writes captions from grounded objects only (ε = −1), and omitted or imagined objects are wrapped in brackets in parametric captions (ε = +1). A scalar ε in [−1, 1] steers the output through one learned linear projection. The paper also introduces CCEval and reports 44% less hallucination than LLaVA-7B.
- Overlap: **C1 medium**: verifier-curated SFT captions restricted to grounded content. **C2 low**: grounded vs. not, binary, from a detector. **C3 low-medium**: it marks or omits uncertain objects but never reduces an object's specificity.
- VSPS distinction: The unit is the object, detection is binary, and the work targets existence only. VSPS verifies typed propositions (attribute, action, count, relation) with three states. It neutralizes the specific component instead of bracketing or dropping the whole object, and needs no inference-time control knob.
- Recommendation: **must cite & contrast**. It is already in Q2_LITERATURE as RW.

### B2. Analyzing and Mitigating Object Hallucination in Large Vision-Language Models (LURE)
- Authors: Yiyang Zhou, Chenhang Cui, Jaehong Yoon, Linjun Zhang, Zhun Deng, Chelsea Finn, Mohit Bansal, Huaxiu Yao
- Venue: ICLR 2024 (from the arXiv comments field). OpenReview, not one of the four publishers.
- Link: arXiv:2310.00754
- Method: A post-hoc revisor. Training data replaces high-uncertainty or late-position object tokens with "[IDK]". At inference the revisor either fills each [IDK] with a fitting object or removes it.
- Overlap: **C3 medium**: an uncertainty-triggered placeholder followed by rewriting is the nearest captioning analogue of neutralization. **C1 low**: it corrects outputs post hoc, which VSPS explicitly contrasts against. **C2 low**: uncertainty is token entropy, not visual verification.
- VSPS distinction: LURE runs as a second model at inference and decides by token entropy. VSPS decides by verified visual evidence, applies the result in the training data, and keeps the still-verifiable part ("người") instead of a blank to re-fill.
- Recommendation: **should cite**. It covers uncertainty-driven masking.

## C. Abstention / "I don't know" for VLMs (C2 framing: "not visible ≠ false")

### C1. Reliable Visual Question Answering: Abstain Rather Than Answer Incorrectly (seminal)
- Authors: Spencer Whitehead, Suzanne Petryk, Vedaad Shakib, Joseph Gonzalez, Trevor Darrell, Anna Rohrbach, Marcus Rohrbach
- Venue: ECCV 2022 (Springer LNCS, Scopus-indexed).
- Link: arXiv:2204.13631
- Method: Selective VQA with coverage-at-risk evaluation and a learned selection function.
- Overlap: **C2 low**. Abstention is the response-level analogue of UNCERTAIN.
- VSPS distinction: VSPS abstains per proposition inside a caption, offline, and reduces specificity rather than refusing.
- Recommendation: optional. Cite as background for "abstain vs. guess".

### C2. Visually Dehallucinative Instruction Generation: Know What You Don't Know (IDK-Instructions) — NEW
- Authors: Sungguk Cha, Jusung Lee, Younghyun Lee, Cheoljong Yang
- Venue: arXiv:2402.09717 (Feb 2024); no venue listed.
- Method: Defines "I Know" hallucination, builds VQAv2-IDK, and generates instruction data that teaches the model to answer "I don't know" on unanswerable visual questions.
- Overlap: **C1 low-medium**: it changes the instruction data to encode uncertainty. **C2 low**.
- VSPS distinction: It works on question-level refusal in VQA. VSPS handles proposition-level reduction in long captions and does not output a refusal string.
- Recommendation: optional / should cite.

### C3. Delineating Knowledge Boundaries for Honest Large Vision-Language Models (Visual-Idk) — NEW
- Authors: Junru Song, Yimeng Hu, Yijing Chen, Huining Li, Qian Li, Lizhen Cui, Yuntao Du
- Venue: arXiv:2604.26419 (29 Apr 2026), preprint.
- Method: Uses multi-sample consistency probing to split facts into known and unknown, then SFT plus DPO/ORPO to refuse beyond the knowledge boundary. Truthful Rate rises from 57.9% to 67.3%.
- Overlap: **C2 medium**: multi-sample consistency to separate certain from uncertain, close to K = 5 sampled votes. **C1 medium**: the uncertainty-labelled data is used for SFT.
- VSPS distinction: Visual-Idk probes the model's own knowledge for QA refusal. VSPS uses an external verifier on image evidence with dual affirmative and negated queries, and neutralizes inside captions instead of refusing.
- Recommendation: **should cite** (very recent).

### C4. R-Tuning: Instructing Large Language Models to Say "I Don't Know" — NEW
- Authors: Hanning Zhang, Shizhe Diao, Yong Lin, Yi R. Fung, Qing Lian, Xingyao Wang, Yangyi Chen, Heng Ji, Tong Zhang
- Venue: NAACL 2024 (ACL Anthology, Scopus-indexed).
- Link: arXiv:2311.09677
- Method: Splits SFT data into certain and uncertain by comparing model predictions with labels. It appends uncertainty expressions, or with R-Tuning-R replaces the labels, for uncertain items.
- Overlap: **C1 medium** (uncertainty-aware SFT data construction). **C3 low-medium**: R-Tuning-R replaces the uncertain target.
- VSPS distinction: R-Tuning is text-only and measures uncertainty against the model's own knowledge. VSPS measures it against visual evidence per proposition, and reduces the target instead of replacing it with "I'm unsure".
- Recommendation: **should cite**. It is the canonical precedent for uncertainty-aware SFT data.

### C5. UNK-VQA: A Dataset and a Probe into the Abstention Ability of Multi-modal Large Models
- Authors: Yangyang Guo, Fangkai Jiao, Zhiqi Shen, Liqiang Nie, Mohan Kankanhalli
- Venue: arXiv:2310.10942, v6 Aug 2024. The authors frame it for TPAMI (IEEE); I could not confirm publication.
- Method: Perturbs images or questions so the answer becomes unknowable, then benchmarks MLLM abstention.
- Overlap: **C2 low**.
- Recommendation: optional.

## D. Calibrated / verbalized confidence and hedging (C2/C3 alternatives VSPS did not take)

### D1. Linguistic Calibration of Long-Form Generations — NEW
- Authors: Neil Band, Xuechen Li, Tengyu Ma, Tatsunori Hashimoto
- Venue: ICML 2024, PMLR 235.
- Link: arXiv:2404.00474
- Method: SFT followed by RL so that long-form text carries calibrated confidence statements, i.e. hedges.
- Overlap: **C3 low-medium**: it is the "hedge" alternative to neutralization.
- VSPS distinction: VSPS deliberately removes the uncertain detail instead of hedging it, which keeps the caption declarative and keeps CHAIR-style metrics meaningful.
- Recommendation: **should cite** to justify neutralization over hedging.

### D2. Object-Level Verbalized Confidence Calibration in Vision-Language Models via Semantic Perturbation (CSP) — NEW
- Authors: Yunpu Zhao, Rui Zhang, Junbin Xiao, Ruibo Hou, Jiaming Guo, Zihao Zhang, Yifan Hao, Yunji Chen
- Venue: arXiv:2504.14848 (Apr 2025), preprint.
- Method: Adds Gaussian noise to object regions to build confidence-labelled data, then trains with SFT followed by preference optimization so that verbalized confidence matches correctness.
- Overlap: **C2 low-medium**: object-level uncertainty labels used in training data.
- VSPS distinction: CSP outputs a confidence; VSPS changes the content.
- Recommendation: optional.

## E. Gender as the main neutralization case (C3; probably also covered by another agent)

### E1. Women also Snowboard: Overcoming Bias in Captioning Models (Equalizer) (seminal)
- Authors: Kaylee Burns, Lisa Anne Hendricks, Kate Saenko, Trevor Darrell, Anna Rohrbach
- Venue: ECCV 2018 (Springer, Scopus-indexed).
- Link: arXiv:1803.09797
- Method: Appearance-confusion and confident losses make the captioner output "person" when gender evidence is occluded and a gendered word when it is visible.
- Overlap: **C3 medium-HIGH for the gender case specifically**. It is the same outcome ("person" when gender is not evidenced).
- VSPS distinction: Equalizer needs person segmentation masks and adds loss terms at training time. VSPS uses standard SFT with no extra loss term and decides by verifier evidence per proposition. It generalises to any droppable component and works on Vietnamese person nouns, where gender is lexicalised in the head noun ("người phụ nữ" vs. "người").
- Recommendation: **must cite & contrast**. It is already in Q2_LITERATURE §1E.

### E2. From Descriptive Richness to Bias: Unveiling the Dark Side of Generative Image Caption Enrichment — NEW
- Authors: Yusuke Hirota, Ryo Hachiuma, Chao-Han Huck Yang, Yuta Nakashima
- Venue: arXiv:2406.13912 (Jun 2024). The venue is unconfirmed on the arXiv page.
- Method: Shows that LLM-enriched detailed captions increase gender bias and hallucination, and that models trained on them amplify both (about +30.9% bias, +59.5% hallucination).
- Overlap: none on method. It motivates C3 and C5: detailed captions amplify unsupported gender.
- Recommendation: **should cite** as motivation.

## Unverified / not reported
- "HallE-Switch: Rethinking and Controlling Object Existence Hallucinations…" appears to be the v1 title of B1, but the arXiv page shows only the v3 title.
- Utrecht MSc thesis "Using Vision and Language models for Uncertainty-Aware Image Captioning" (hedging phrases plus BLIP-2 fine-tuning): it is a student thesis, not peer-reviewed, and I did not open it. Optional at most.
- "Certainly Uncertain" (ICLR 2025): an epistemic/aleatoric VQA benchmark. I did not open the proceedings page to confirm the authors.
- "Steering the Verifiability of Multimodal AI Hallucinations" (arXiv:2604.06714): the abstract has no "Uncertain" label. It is about obvious vs. elusive hallucinations; no overlap.

## Conclusion: nothing found that combines VSPS's C2 and C3
I found no paper that combines all four of the following:
- (a) a three-state visual verdict where UNCERTAIN is distinct from REJECTED;
- (b) reducing an uncertain proposition to a less specific, still-verifiable proposition instead of deleting, hedging or refusing;
- (c) doing this offline in SFT supervision for an image captioner;
- (d) recovering the reduced form from stored evidence without re-querying.

The ideas exist separately:
- specificity back-off: text-only (A1, A2) or classification (A3);
- uncertain-claim gating: inference-time (A4);
- uncertainty-aware SFT: QA refusal (C2–C4);
- gender neutralization: loss-based (E1).

## Highest-overlap risks
1. **Conformal Linguistic Calibration (Jiang et al., NeurIPS 2025)**: the same "reduce specificity of uncertain claims and train on the rewrites" principle (text-only). C3 HIGH.
2. **Women also Snowboard / Equalizer (Burns et al., ECCV 2018)**: the same outcome for the gender case ("person" when unsure). C3 medium-HIGH.
3. **ConfLVLM (Li et al., EMNLP 2025)**: claim-level uncertainty gating of LVLM descriptions. C2 medium.
4. **HallE-Control (Zhai et al., arXiv 2023/24)**: verifier-curated, grounded-only SFT captions for detailed captioning. C1 medium.
5. **LURE (Zhou et al., ICLR 2024)**: uncertainty-triggered [IDK] masking and rewriting of caption objects. C3 medium.

## Suggested novelty statement
"Prior work reduces the specificity of uncertain claims for text-only QA at inference or via an LLM rewriter (conformal factuality; conformal linguistic calibration), or gates LVLM claims by deletion at deployment. VSPS instead assigns a three-state visual verdict to each typed proposition and, for UNCERTAIN ones, deterministically removes only the under-evidenced component (e.g., the gender in a Vietnamese person noun), recovered offline from stored verifier evidence. The resulting captions are used as plain SFT targets, so the deployed captioner abstains from unsupported detail without hedging, refusing or an inference-time filter."
