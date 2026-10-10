# 07 — VQA / yes-no verification, negated probes, self-consistency (overlap vs. C2, plus C1/C4)

Agent 07. Searched in Oct 2026 via web search plus arXiv, ACL Anthology, CVF, PMLR and NeurIPS pages. Papers already in `Q2_LITERATURE.md` (POPE, TIFA, DSG, RLAIF-V, HalluciDoctor, VFC) appear here only for their C2-specific contrast.

The C2 mechanism under test, from the paper text (Sec. III-A2):
- Each proposition becomes two queries: an affirmative one (Q+) and a negated one (Q-). Each is sampled K=5 times. Γ takes the majority polarity and agreement of the five answers, and Φ combines the two branches into support, counter-evidence and an evidence gate.
- A split in the affirmative branch, or "yes" to both queries (acquiescence), gives UNCERTAIN. A stable "no" to Q+, or a "yes" to Q- alone, gives REJECTED.
- For colour propositions, a second model (the generator) is also asked. If it disagrees, the verdict is lowered to UNCERTAIN.
- Ceiling rules can only lower a verdict.
- An evidence record is stored and reused offline (C3).

---

## A. Verifier-style QG/VQA (claim → question → VQA answer)

### A1. TIFA: Accurate and Interpretable Text-to-Image Faithfulness Evaluation with Question Answering
- Hu, Liu, Kasai, Wang, Ostendorf, Krishna, Smith. **ICCV 2023** (IEEE/CVF; Scopus-indexed). arXiv:2303.11897 (abstract page opened).
- **Method:** An LLM generates QA pairs from a text prompt. A VQA model answers them on the image, and the accuracy is the faithfulness score.
- **Overlap:**
  - C2 low: binary correct/incorrect, single answer, no negation, no abstain state.
  - C4 low: questions are generated per prompt rather than as typed propositions.
  - C1 none: evaluation only.
- **Distinguishing point:** VSPS uses QG/VQA as a three-state data filter for training supervision, not as a T2I metric. It also adds a negated twin query and sampling stability.
- **Recommendation:** should cite (already in RW).

### A2. Davidsonian Scene Graph (DSG): Improving Reliability in Fine-grained Evaluation for Text-to-Image Generation
- Cho et al. **ICLR 2024**. arXiv:2310.18235 (confirmed; ICLR poster 18963).
- **Method:** Atomic, unique questions arranged in a dependency DAG. A child question is skipped or invalidated when its parent fails, which is meant to avoid inconsistent VQA answers.
- **Overlap:**
  - C4 medium: atomic typed propositions with entity → attribute/relation dependency, the same as VSPS's entity registry.
  - C2 low: binary answers, one sample, no negation, no UNCERTAIN state.
- **Distinguishing point:** DSG handles answer inconsistency structurally, through parent–child gating. VSPS handles it statistically (K-sample split → UNCERTAIN) and logically (affirmative/negated contradiction → UNCERTAIN). VSPS also feeds the verdicts into SFT data.
- **Recommendation:** must cite & contrast (C4).

### A3. VQAScore: Evaluating Text-to-Visual Generation with Image-to-Text Generation
- Lin, Pathak, Li, et al. (CMU/Meta). **ECCV 2024** (Springer LNCS; Scopus-indexed). arXiv:2404.01291 (confirmed via ECVA and arXiv).
- **Method:** P("Yes" | image, "Does this figure show {text}?") from a VQA model gives one continuous alignment score.
- **Overlap:**
  - C2 low: a single affirmative yes-probability per text, with no negated query, no sampling and no three-way decision. It is exposed to the yes-bias that VSPS explicitly guards against.
- **Distinguishing point:** VSPS does not trust a raw "yes". It requires the negated query not to also be answered "yes", and it requires decisive, stable sampled answers.
- **Recommendation:** should cite (one sentence in RW, as the canonical "P(yes) as verifier").

### A4. FaithScore: Fine-grained Evaluations of Hallucinations in Large Vision-Language Models
- Jing, Li, Chen, Du. **Findings of EMNLP 2024** (ACL Anthology 2024.findings-emnlp.290; Scopus-indexed via ACL). arXiv:2311.01477 (confirmed).
- **Method:** Identifies descriptive sub-sentences, decomposes them into atomic facts (entity, count, colour, relation, attribute and others), and verifies each fact with a visual-entailment / VQA model. The score is the fraction of facts verified.
- **Overlap:**
  - C4 medium-HIGH: the typed atomic-fact taxonomy closely parallels VSPS's entity / attribute / action / count / relation types.
  - C2 low: binary entailment, no UNCERTAIN state, no negation or sampling.
  - C1 none: metric only.
- **Distinguishing point:** FaithScore scores outputs after the fact. VSPS verifies propositions before training, with three states, and turns the verdicts into supervision.
- **Recommendation:** must cite & contrast (it is the closest "typed atomic fact + VQA verifier" prior and is not in Q2_LITERATURE).

### A5. Woodpecker: Hallucination Correction for Multimodal Large Language Models
- Yin, Fu, et al. arXiv:2310.16045 (confirmed). It is often cited as published in *Science China Information Sciences* 2024 (Springer; Scopus). I did not open that venue page, so verify before citing the journal.
- **Method:** Training-free post-hoc pipeline: key-concept extraction → question formulation → visual knowledge validation (Grounding DINO for existence/counts, BLIP-2 VQA for attributes) → claim generation → LLM rewrite of the output.
- **Overlap:**
  - C2 low-medium: VQA validation of extracted claims, but single-shot with no negated twin query and no UNCERTAIN state.
  - C1 low: post-hoc output correction, the opposite of VSPS's data-level placement.
- **Distinguishing point:** VSPS verifies only offline on training data, and the deployed model is single-pass. Woodpecker runs a multi-model pipeline at every inference.
- **Recommendation:** must cite & contrast (canonical post-hoc baseline for the C1 argument).

### A6. Unified Hallucination Detection for Multimodal LLMs (UNIHD / MHaluBench)
- Chen et al. ICLR 2024 Workshop. Extended version in **ACL 2024** (main). arXiv:2402.03190 (confirmed). I did not open the ACL page; venue as reported.
- **Method:** Claim extraction → LLM writes per-claim queries → tools (detector, attribute VQA, OCR, web search) → an MLLM judges each claim hallucinated or not, with a rationale.
- **Overlap:**
  - C2 low-medium: claim-level verification aggregated from several tools, with binary labels.
  - C1 none: detection only.
- **Distinguishing point:** No negated query, no sampling-stability gate, no abstain state. Its output is a detector score rather than training data.
- **Recommendation:** should cite.

### A7. CapMAS: Toward Robust Hyper-Detailed Image Captioning: A Multiagent Approach and Dual Evaluation Metrics for Factuality and Coverage
- Lee, Yoon, Bui, Shi, Yoon. **ICML 2025** (PMLR v267, lee25aj; Scopus-indexed). arXiv:2412.15484 (confirmed).
- **Method:** An LLM decomposes a detailed caption into atomic claims. An MLLM scores each claim by its True/False token probabilities against a threshold, and an LLM rewrites the caption from the claims judged true. The paper also proposes factuality and coverage metrics.
- **Overlap:**
  - C4 medium: atomic-claim decomposition of detailed captions, re-rendered from the verified claims.
  - C2 low-medium: a binary threshold, with no UNCERTAIN state and no negated or sampled check.
  - C1 low: inference-time correction, not data-level.
- **Distinguishing point:**
  - VSPS keeps a third state and neutralizes instead of deleting (C3).
  - It runs offline to build SFT targets, so there is no multi-agent pipeline at deployment.
  - Its renderer is template/constrained, so each span traces to a proposition, whereas CapMAS uses free LLM rewriting.
- **Recommendation:** must cite & contrast (closest detailed-captioning claim-verification work, 2025).

### A8. Visual Fact Checker (VFC): Enabling High-Fidelity Detailed Caption Generation
- Ge, Zeng, Huffman, Lin, Liu, Cui (NVIDIA). **CVPR 2024**, pp. 14033–14042 (IEEE/CVF). arXiv:2404.19752 (confirmed).
- **Method:** Several captioners propose drafts. An LLM verifies them with a detector and VQA (LLaVA-1.5), then fuses the drafts into a final caption.
- **Overlap:**
  - C2 low-medium: multi-model proposal plus VQA verification, without a three-state outcome or a negated/sampled gate.
  - C1 low: an inference pipeline (though usable to produce data).
- **Distinguishing point:** VSPS's verdict is per proposition, with an explicit evidence record and a monotone ceiling. The deployed model is single-pass.
- **Recommendation:** must cite (already listed).

### A9. RLAIF-V: Open-Source AI Feedback Leads to Super GPT-4V Trustworthiness
- Yu et al. **CVPR 2025** (IEEE/CVF). arXiv:2405.17220 (confirmed).
- **Method:** "Divide-and-conquer" feedback: each sampled response is split into atomic claims, each claim is converted to a yes/no question, and an open MLLM scores it. The response score comes from the number of rejected claims and is used for DPO preference pairs.
- **Overlap:**
  - C2 medium: the claim → yes/no question → open-MLLM answer pipeline is the same front end as VSPS's verifier.
  - C1 medium: the verification shapes training data, but as preference pairs, not SFT targets.
- **Distinguishing point:**
  - RLAIF-V uses one affirmative question per claim, is binary, and simply counts rejections.
  - VSPS adds a negated twin, K-sample stability and acquiescence-to-UNCERTAIN, so "not visible" is not counted as wrong.
  - VSPS uses standard SFT, and the paper reports a negative DPO result.
- **Recommendation:** must cite & contrast (state the C2 differences explicitly).

## B. Data-level cross-checking (multi-model consistency)

### B1. HalluciDoctor: Mitigating Hallucinatory Toxicity in Visual Instruction Data
- Yu et al. **CVPR 2024**, pp. 12944–12953, DOI 10.1109/CVPR52733.2024.01230 (IEEE; Scopus). arXiv:2311.13614 (confirmed).
- **Method:**
  - Answer chunks are extracted from instruction data, and questions are generated for each chunk.
  - **Several other MLLMs answer them.** A BEM consistency score below a threshold flags the chunk as hallucinatory, and it is removed to give LLaVA+.
  - Counterfactual instruction expansion is applied as well.
- **Overlap:**
  - C1 HIGH: verification-based cleaning of SFT data, the same placement as VSPS.
  - C2 medium: multi-model cross-checking with a consistency threshold, which parallels VSPS's colour cross-check and agreement score.
- **Distinguishing point:**
  - HalluciDoctor's outcome is binary keep/delete. It has no UNCERTAIN state, no negated query (so acquiescence is not detected), and no within-model sampling stability.
  - Uncertain chunks are deleted rather than neutralized (C3).
  - It edits existing human/GPT instruction text, while VSPS builds supervision from verified propositions and renders it.
- **Recommendation:** must cite & contrast. Highest-overlap paper for C1+C2.

### B2. OmniHallu: Unified Hallucination Detection for Cross-Modal Comprehension and Generation in MLLMs
- arXiv:2609.11244 (Sept 2026 preprint; found via search, abstract snippet only, full text not opened).
- **Method:** Claims are routed to expert panels. Attribute, relation and event claims are judged by an ensemble of three MLLMs.
- **Overlap:** C2 low-medium, through multi-model cross-checking. It is detection only.
- **Recommendation:** optional (very recent preprint; verify before citing).

## C. Negation, polarity and yes-bias (acquiescence) as a verifier failure mode

### C1. Measuring the Measurers: Quality Evaluation of Hallucination Benchmarks for LVLMs (HQM)
- Bei Yan, Jie Zhang, Zheng Yuan, Shiguang Shan, Xilin Chen. arXiv:2406.17115 (v1 June 2024, v3 Feb 2026). No peer-reviewed venue listed on arXiv. HTML opened.
- **Method:** Benchmark-quality framework. For parallel-forms reliability, "yes-or-no questions are rewritten into negative forms with opposite ground truth answers". The paper reports models with **"significant acquiescence bias, i.e., the tendency to answer 'yes'"** (MiniGPT4-LLaMa-2, Otter) and others with dissent bias.
- **Overlap:**
  - C2 medium-HIGH on the idea level: affirmative + negated yes/no pairs are used specifically to expose acquiescence, using the same term.
  - It differs in purpose: it diagnoses benchmarks, not a per-claim verdict and not data filtering.
- **Distinguishing point:** VSPS turns the affirmative/negated contradiction into a per-proposition decision rule (both "yes" → UNCERTAIN) and uses it to gate training data.
- **Recommendation:** must cite. It is the best precedent for the "acquiescence" wording, and VSPS should credit the paired-negation diagnostic rather than imply it invented it.

### C2. UHP Detection: LVLMs have their Unique Hallucination Pattern in the Consistency Space
- Ezzati, Rezaee, Kariminia, Yousefi, Mohammadjafari Mamaqani, Samimi, Rohban. arXiv:2608.03817 (Aug 2026 preprint; abstract opened).
- **Method:** Black-box hallucination detection over two consistency axes: perturbation modality (image vs. text) and **logical polarity (statement vs. its negation)**. Within- and between-group consistency features train a light classifier, evaluated on AMBER and PhD.
- **Overlap:**
  - C2 medium-HIGH on mechanism: statement-vs-negation consistency used as a hallucination signal.
  - Differences: it is a learned classifier for detection, not a rule-based three-state verdict, and not used to build training data.
- **Distinguishing point:** VSPS's Φ is a transparent, rule-based combiner with an abstain state. Its verdicts are monotone (ceilings only lower them) and are stored as evidence records for offline neutralization and SFT data construction.
- **Recommendation:** must cite & contrast if the journal version is written after Aug 2026. It is concurrent work and should be framed that way.

### C3. HallusionBench
- Guan et al. **CVPR 2024** (IEEE/CVF). arXiv:2310.14566 (confirmed).
- **Method:** Diagnostic suite with control-pair questions. It includes a Yes/No Bias Test (predicted vs. actual yes-rate) and a false-positive ratio.
- **Overlap:** C2 low: it measures yes-bias but does not use paired probes as a verifier.
- **Recommendation:** should cite (evidence that yes-bias is real).

### C4. POPE: Evaluating Object Hallucination in Large Vision-Language Models
- Li et al. **EMNLP 2023**. DOI 10.18653/v1/2023.emnlp-main.20. Already in Q2_LITERATURE.
- **Method:** Yes/no object-existence probing. It reports the "yes ratio" as a bias indicator.
- **Overlap:** C2 low: probing used for evaluation, not as a gating verifier.
- **Distinguishing point:** VSPS generalizes POPE-style probing from objects to all proposition types and adds a negated twin plus K-sample stability.
- **Recommendation:** must cite (already planned).

### C5. Vision-Language Models Do Not Understand Negation (NegBench)
- Alhamoud et al. **CVPR 2025** (IEEE/CVF). arXiv:2501.09425 (confirmed via CVF open access).
- **Overlap:** C2 low. It documents "affirmation bias" on negated statements, mainly for CLIP-like models.
- **Recommendation:** should cite. It is a caveat VSPS must address: negated Vietnamese queries ("Có phải KHÔNG có…") may themselves be misread. Treating "yes to both" as UNCERTAIN rather than REJECTED is the right conservative response to this failure mode.

### C6. NegVQA: Can Vision Language Models Understand Negation?
- Zhang, Su, Liu, Yeung-Levy. **Findings of ACL 2025** (ACL Anthology 2025.findings-acl.191). arXiv:2505.22946 (confirmed).
- **Method:** 7,379 negated two-choice VQA questions. 20 VLMs show large drops on them, with a U-shaped scaling trend.
- **Overlap:** C2 low. It shows that the negated branch is a noisy signal.
- **Recommendation:** should cite. Together with NegBench it justifies why VSPS lets the negated branch only lower confidence (to UNCERTAIN) and never alone yield SUPPORTED.

### C7. Negative Object Presence Evaluation (NOPE)
- Lovenia et al. arXiv:2310.05338 (confirmed exists). Reported venue: ALVR workshop at ACL 2024. Not verified, so treat it as a preprint.
- **Overlap:** C2 low: negative-presence VQA evaluation.
- **Recommendation:** optional.

## D. Sampling agreement / uncertainty (SelfCheckGPT / semantic-entropy family for VLMs)

### D1. SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative LLMs
- Manakul, Liusie, Gales. **EMNLP 2023** (ACL Anthology 2023.emnlp-main.557). Confirmed.
- **Method:** Sample N responses. A sentence is flagged as hallucinated if the samples do not support it (BERTScore, QA, NLI, n-gram or LLM-prompt scoring).
- **Overlap:** C2 medium (concept): sampling agreement as a reliability signal. It is text-only.
- **Distinguishing point:** VSPS samples the verifier's yes/no answer to a fixed question, not the generator's free text. A split vote is a hard gate to UNCERTAIN rather than a continuous score.
- **Recommendation:** must cite. It is the canonical source of "K-sample agreement", and VSPS's gate is a discrete VQA variant of it.

### D2. VL-Uncertainty: Detecting Hallucination in LVLMs via Uncertainty Estimation
- R. Zhang, H. Zhang, Z. Zheng. arXiv:2411.11919 (confirmed). I did not confirm a peer-reviewed venue.
- **Method:**
  - Semantically equivalent perturbations of both image and prompt are applied, and answers are clustered by meaning.
  - The entropy of the clusters is the uncertainty score.
  - The paper argues that plain temperature sampling, as in semantic entropy, under-detects LVLM hallucination because models answer consistently wrong.
- **Overlap:** C2 medium. It is the closest uncertainty-from-agreement method for VLMs.
- **Distinguishing point:** VSPS uses a discrete gate on K=5 temperature samples plus a negated twin, rather than entropy over perturbations.
- **Must address this finding:** VL-Uncertainty's result implies that unanimous 5/5 agreement can still be wrong. VSPS's neutralization threshold (τ = 0.9, 5/5) relies on unanimity, so its human verifier audit (Sec. IV-E7) is the necessary counter-evidence. VSPS should say so.
- **Recommendation:** must cite & contrast.

### D3. Vision-Amplified Semantic Entropy for Hallucination Detection in Medical VQA (VASE)
- Liao et al. **MICCAI 2025** (Springer LNCS; Scopus). arXiv:2503.20504 (confirmed via MICCAI paper page listing).
- **Method:** Semantic entropy over answers under mild vs. distorted image transformations, contrasted.
- **Overlap:** C2 low-medium (sampling-based uncertainty for VQA, medical domain).
- **Recommendation:** optional.

### D4. Self-Consistency as a Free Lunch: Reducing Hallucinations in VLMs via Self-Reflection
- Han, Hao, Zhou, Li, Zheng, Deng, Yang, Chang. arXiv:2509.23236 (Sept 2025 preprint; abstract opened).
- **Method:** The model's short yes/no answers are treated as the reliable reference. Long responses that disagree with them are flagged and ranked to build preference pairs, with no external model.
- **Overlap:**
  - C1 medium: yes/no-verification-derived training data.
  - C2 low-medium: yes/no answers as a verifier.
- **Distinguishing point:** It produces preference data rather than SFT targets. Its verification is binary, with no negated or sampled gate, and it uses self-verification, whereas VSPS uses a separate verifier plus a generator cross-check for colour.
- **Recommendation:** should cite.

### D5. LogicCheckGPT: Logical Closed Loop: Uncovering Object Hallucinations in LVLMs
- Wu et al. **Findings of ACL 2024** (ACL Anthology; Scopus via ACL). arXiv:2402.11622 (confirmed). The search snippet said "ACL 2024", and the OpenReview/ACL entry shows the Findings track. Verify the exact track before citing.
- **Method:** Asks object → attribute and attribute → object questions. If the answers do not close a logical loop, the object is treated as hallucinated and removed.
- **Overlap:**
  - C2 medium: inconsistency across logically related queries as evidence of hallucination. This is close in spirit to VSPS's affirmative/negated contradiction rule.
  - C1 low: inference-time only.
- **Distinguishing point:** VSPS uses polarity duality plus sampling rather than bidirectional attribute questions. It produces a three-state verdict and acts on training data.
- **Recommendation:** must cite & contrast.

### D6. Unveiling the Tapestry of Consistency in LVLMs (ConBench)
- Y. Zhang, F. Xiao, et al. **NeurIPS 2024**, DOI 10.52202/079017-3767. arXiv:2405.14156 (confirmed).
- **Overlap:** C2 low. It shows that answers to the same fact are inconsistent across question formats and that discriminative accuracy correlates with caption consistency.
- **Recommendation:** optional, useful for motivating why one probe is not trusted.

## E. "Not visible ≠ false": abstain / IDK states

### E1. Visually Dehallucinative Instruction Generation: Know What You Don't Know (IDK-Instructions, VQAv2-IDK)
- Cha et al. arXiv:2402.09717 (confirmed). I did not verify a venue.
- **Method:** Builds instruction data where the target answer is "I don't know" for unanswerable image questions.
- **Overlap:** C2 low-medium (concept): the epistemic third state in training data.
- **Distinguishing point:** VSPS does not train the model to say IDK. The UNCERTAIN state drives exclusion or neutralization of supervision content, so captions stay assertive but less specific.
- **Recommendation:** should cite.

### E2. Three-way verdict precedent (fact-checking: Supported / Refuted / NEI)
- FEVER-style NEI is standard in multimodal fact-checking, e.g. Mocheg (Yao et al., **SIGIR 2023**, ACM, DOI 10.1145/3539618.3591879, confirmed).
- Visual entailment's entailment / neutral / contradiction scheme also covers this (SNLI-VE; not re-verified here).
- **Overlap:** C2 medium on the label scheme alone. VSPS should credit it: the three-state idea itself is not new.
- **Recommendation:** should cite one (Mocheg or SNLI-VE) to anchor SUPPORTED/UNCERTAIN/REJECTED.

---

## Unverified / not cited
- "MRFD" (multi-region fusion decoding with self-consistency): appears only in a GitHub awesome-list as "soon". I could not confirm it.
- CAST (cross-modal self-consistency test): mentioned in a search summary. Paper not located.
- PDA (arXiv 2604.01010): uses verification questions about caption claims for adversarial defense. Off-topic, and I did not open it.
- Woodpecker journal venue (Sci. China Inf. Sci.) and UNIHD's ACL 2024 main-track status: plausible but not opened.

---

## Highest-overlap risks
1. **HalluciDoctor (CVPR 2024)**: HIGH on C1, medium on C2. It cleans visual instruction data by cross-checking claims with several MLLMs against a consistency threshold. VSPS must contrast as follows:
   - three-state vs. binary;
   - negated twin and acquiescence detection;
   - within-verifier K-sample stability;
   - neutralization vs. deletion;
   - rendering from propositions vs. editing existing text.
2. **RLAIF-V (CVPR 2025)**: medium on C1 and C2. It uses the same claim → yes/no question → open-MLLM verifier front end. Differences: one affirmative query, binary, counted into DPO rewards.
3. **HQM / "Measuring the Measurers" (arXiv 2406.17115)** and **UHP Detection (arXiv 2608.03817)**: affirmative + negated question pairs to expose acquiescence, and statement-vs-negation consistency as a hallucination signal. VSPS cannot claim the negated-pair idea itself. The novelty is turning it into a per-proposition rule ("yes" to both → UNCERTAIN) inside a data-construction pipeline.
4. **SelfCheckGPT (EMNLP 2023)** and **VL-Uncertainty (arXiv 2411.11919)**: sampling agreement as a hallucination signal. VL-Uncertainty additionally shows that temperature-sample agreement can be confidently wrong in LVLMs. This is a reviewer-ready objection to the 5/5-unanimity neutralization threshold, so point to the human audit (Sec. IV-E7).
5. **FaithScore (EMNLP-F 2024)**, **CapMAS (ICML 2025)** and **LogicCheckGPT (ACL-F 2024)**: typed atomic facts plus VQA verification, and logical-consistency checks. Overlap is medium on C4 and C2, but all are evaluation or inference-time tools rather than data-level.

## Suggested novelty statement (topic 07)
> Prior VQA-based verifiers (TIFA, DSG, FaithScore, RLAIF-V, HalluciDoctor) ask one affirmative question per claim and output a binary or continuous score. Paired negated probes and sampling agreement have so far been used only to *diagnose* yes-bias or to *detect* hallucinations. VSPS combines both into an explicit three-state decision per proposition: an affirmative and a negated query, K = 5 samples each, a split vote or "yes to both" (acquiescence) yielding UNCERTAIN, and ceilings that can only lower a verdict. VSPS then uses that verdict offline to decide which content enters SFT supervision, whether directly, after neutralization, or not at all, rather than to score or correct model outputs.
