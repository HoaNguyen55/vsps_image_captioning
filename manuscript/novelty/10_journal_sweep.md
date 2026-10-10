# 10 — Journal-side sweep (2024–2026): captioning / LVLM hallucination, faithfulness, verified supervision

Agent 10 of 10. Scope: journal articles only. Conference papers are covered by agents 01–09.

## Method

- **OpenAlex**, filtered to `type:article` and `primary_location.source.type:journal`, published 2024-01-01 or later. I ran 28 free-text searches, 26 title searches (`title.search`) and 8 title+abstract searches (`title_and_abstract.search`). Terms combined: hallucination(s), object hallucination, vision-language, LVLM(s), MLLM(s), multimodal, caption, detailed/dense/descriptive caption, faithful(ness), factual(ity), grounded, verification, atomic, propositions, fine-grained, preference optimization, instruction data, uncertainty, gender, Vietnamese, trustworthy.
- **Crossref**: 16 `query.bibliographic` searches over journal articles from 2024 onward.
- **Semantic Scholar**: 6 searches with `publicationTypes=JournalArticle`. Most were rate-limited (HTTP 429).
- **Web**: 7 general web searches, aimed at IEEE Xplore, ScienceDirect and SpringerLink content.
- **Filtering**: I kept only items whose venue is one of the journals in the brief, or another clearly peer-reviewed indexed journal, and dropped medical, remote-sensing and psychiatry hits. For every paper reviewed below I opened its OpenAlex or Crossref record to confirm the DOI and venue. Abstracts come from OpenAlex. Where no abstract was available, the paper is rated from its title only and marked that way.
- **Indexing**: the IEEE Transactions titles, IEEE Access, the Elsevier titles (PR, PRL, ESWA, KBS, Neurocomputing, InfFus, IPM, IVC, JVCIR, SPIC), the Springer titles (IJCV, Multimedia Systems, NCA, SCIS) and ACM TOMM/TALLIP are all Scopus-indexed. Discover AI (Springer, open access, launched 2021) is listed with Scopus status not confirmed.

**Bottom line: no journal paper rates HIGH against any claim C1–C5.** Journal work in 2024–2026 is dominated by training-free decoding, attention, or contrastive-decoding fixes (roughly 70% of hits) and by DPO/RL variants. None of the journal papers found does the following together: proposition-level, three-state verification used to build SFT targets; neutralization of under-evidenced components; or Vietnamese detailed-caption hallucination evaluation.

---

## A. Data-level / verified-supervision papers (closest to C1/C2)

### A1. HELTA: Hallucination Elimination and Text Annotation Framework for Large Vision-Language Models in Traffic Scenarios
- **Authors / venue**: J. Fan, J. Wu, H. Chu, Q. Ge, B. Gao. *IEEE Trans. Intelligent Transportation Systems* 2025 (IEEE, Scopus). DOI: 10.1109/TITS.2025.3625700.
- **Method**: A training-free annotation pipeline that "employs a cross-checking mechanism to filter entities" and adds detected critical objects, so that "hallucination-free" descriptive datasets can be generated offline (CODA_desc, nuScenes_desc). It is evaluated on POPE.
- **Overlap**:
  - C1: **medium**. Like VSPS, it uses offline verification to build cleaner description data.
  - C2: low. Its cross-check is binary, with no UNCERTAIN state.
  - C3: none.
  - C4: low. It filters at entity level only and has no typed propositions or rendering.
  - C5: none.
- **How VSPS differs**: HELTA filters entities for a domain dataset. VSPS verifies typed propositions with a three-state verdict and dual-polarity K=5 voting, neutralizes UNCERTAIN components, then trains a single-pass captioner with standard SFT and measures the effect on CHAIR.
- **Recommendation**: **should cite** (journal precedent for offline verified description data).

### A2. Woodpecker: Hallucination Correction for Multimodal Large Language Models
- **Authors / venue**: S. Yin et al. *Science China Information Sciences* 67(12), 2024 (Springer, Scopus). DOI: 10.1007/s11432-024-4251-x. Already in v7 and in Q2_LITERATURE.
- **Method**: Post-hoc pipeline: extract key concepts, generate questions, validate them with an expert detector and VQA, then rewrite the response.
- **Overlap**:
  - C1: medium. The verification pipeline is similar, but it runs post hoc, at every inference.
  - C2: low. Binary validation, single answers.
  - C4: medium. It extracts claims and rewrites the output.
  - C3, C5: none.
- **How VSPS differs**: VSPS verifies offline only and the deployed model makes a single pass. VSPS has three states, dual-polarity voting and neutralization.
- **Recommendation**: **must cite & contrast** (already cited).

### A3. Mitigating Hallucinations in LVLMs via Asking Questions (AQAH)
- **Title**: Asking Questions to Alleviate Object Hallucination in Large Vision-Language Models.
- **Authors / venue**: C. Bi, T. Dang, S. Wang, F. Cao, Q. Huang. *IEEE TCSVT* 2025 (IEEE, Scopus). DOI: 10.1109/TCSVT.2025.3618949.
- **Method**: Compares multiple sampled generations to locate "uncertain information", asks questions about it (using a small trained question generator), and adds the answers to the prompt for regeneration.
- **Overlap**:
  - C2: **medium**. It uses sample disagreement to flag uncertainty and then targeted questions.
  - C1: low. It runs at inference time; no SFT data is built.
  - C3, C4, C5: none.
- **How VSPS differs**: In VSPS, disagreement among K=5 answers to both affirmative and negated queries is an offline evidence gate that yields an explicit UNCERTAIN verdict, and that verdict shapes the training targets. There are no extra inference passes.
- **Recommendation**: **should cite** (closest journal analogue for "sampling disagreement → uncertainty → question").

### A4. Mitigating Multimodal Hallucination Through Effective and Perception-Aware Granularity Alignment (EPAlign)
- **Authors / venue**: Z. Zhang, J. Lin, Y. Zhang, R. Xia, C. Zhou. *IEEE/ACM Trans. Audio, Speech & Language Processing* 2026 (IEEE, Scopus). DOI: 10.1109/TASLPRO.2026.3703183.
- **Method**: Shows that a granularity mismatch between training-stage data causes "ungrounded extrapolation" when coarse visual information meets fine-grained text. Aligns training data to a perception-appropriate granularity.
- **Overlap**:
  - C1: **medium**. It is a data-level argument that over-detailed supervision beyond what the model perceives causes hallucination, which is the same motivation as VSPS's cautious supervision.
  - C2–C5: none.
- **How VSPS differs**: EPAlign tunes the granularity of the whole dataset. VSPS decides per proposition, from visual evidence, what to keep, drop, or neutralize.
- **Recommendation**: **should cite** (supports the motivation; journal counterpart of "Less is More" and KnowAda).

### A5. REVERIE+: Generalized Reflective Instruction Tuning for Hallucination Mitigation in Advanced VLMs
- **Authors / venue**: M. Bi, J. Zhang, X. Wang, X. Jiang, Y. Lu, P. Wang. *IJCV* 2026 (Springer, Scopus). DOI: 10.1007/s11263-026-02945-6. The abstract is elided by the publisher, so this is rated from the title and the ECCV 2024 REVERIE version.
- **Method**: Instruction tuning on data enriched with rationales and reflections to reduce hallucination. This is the journal extension of REVERIE.
- **Overlap**:
  - C1: low–medium. It is an SFT-data intervention, but it adds rationales rather than verifying or filtering targets.
  - Others: none.
- **How VSPS differs**: VSPS removes or neutralizes unsupported content in the targets and does not add reasoning text.
- **Recommendation**: optional / should cite (it is the IJCV version, so cite it alongside or instead of ECCV REVERIE).

### A6. Mitigating Low-Level Visual Hallucinations Requires Self-Awareness: Database, Model, and Training Strategy
- **Authors / venue**: Y. Sun, X. Min, Z. Zhang, Y. Gao, Y. Cao, G. Zhai. *IEEE TCSVT* 2025. DOI: 10.1109/TCSVT.2025.3619558.
- **Method**: Builds the HLPU instruction database (about 200K QA pairs) for low-level and image-quality hallucination, plus a self-awareness training strategy.
- **Overlap**:
  - C1: low (instruction-data level, different task).
  - C2: low (the "self-awareness" notion is related to knowing what is not visible).
- **Recommendation**: optional.

### A7. Mitigating Multilingual Hallucination in Large Vision-Language Models (MHR)
- **Authors / venue**: X. Qu, M. Song, W. Wei, D. Liu, J. Dong, Y. Cheng. *ACM TOMM* 2026 (ACM, Scopus). DOI: 10.1145/3797025.
- **Method**: States that hallucination is worse for non-English queries. Two stages: multilingual SFT, then hallucination-aware preference alignment across high- and low-resource languages. Described as "the first attempt" at multilingual LVLM hallucination.
- **Overlap**:
  - C5: **medium**. It is the journal precedent for non-English LVLM hallucination.
  - C1: low. Its preference data is not proposition-verified.
  - C2–C4: none.
- **How VSPS differs**: VSPS targets Vietnamese *detailed captioning* specifically, using CHAIR on KTVIC with a Vietnamese object lexicon and a gender-attribution metric. MHR mostly reports QA-style benchmarks; check whether its language set includes Vietnamese before claiming "first for Vietnamese".
- **Recommendation**: **must cite & contrast** for C5.

---

## B. RL / preference journal papers (C1 contrast only)

### B1. Metric-Driven Reinforcement Learning for Object Hallucination Reduction in LVLM-Based Image Captioning
- **Authors / venue**: T. Nguyen, H. S. Yoon, T. M. Luu, E. Yoon, C. D. Yoo. *IEEE Access* 2026 (IEEE, Scopus). DOI: 10.1109/ACCESS.2026.3723028.
- **Method**: PPO adapters on a frozen InstructBLIP with an Object Consistency Score (correctness plus coverage) and KL regularization. Reports up to 41% hallucination reduction on CHAIR.
- **Overlap**:
  - C1: low–medium. Same goal and metric (captioning, CHAIR), but it uses an RL reward rather than verified SFT data.
  - C5: low (English).
- **How VSPS differs**: VSPS needs no reward model or RL loop. It uses standard SFT on verified targets and adds UNCERTAIN handling.
- **Recommendation**: **should cite** (a 2026 journal paper with the same task and metric, likely to come up in review).

### B2. VGL-DPO: Vision-Guided Lexical Direct Preference Optimization for Mitigating Hallucination in MLLMs
- **Authors / venue**: S. Li, F. H. Wang, S. Qin, R. Duan, H. Cheng, L. Ye. *ACM TOMM* 2026. DOI: 10.1145/3796715.
- **Method**: Token-weighted DPO, with weights set by each word's visual relevance.
- **Overlap**: C1 low (preference loss, not data verification).
- **Recommendation**: optional.

### B3. Hallucination-resistant multimodal content generation through knowledge graph-based reinforcement learning
- **Authors / venue**: L. Zeng, X. Lin, S. Yu. *Information Fusion* 2025 (Elsevier). DOI: 10.1016/j.inffus.2025.103783.
- **Method / overlap**: KG-reward RL, rated from the title only (no abstract retrieved). Low overlap.
- **Recommendation**: optional.

### B4. A unified framework for early childhood image captioning via knowledge-grounded metrics and process-level reinforcement
- **Authors / venue**: Z. Wang et al. *Engineering Applications of AI* 2026 (Elsevier). DOI: 10.1016/j.engappai.2026.116162.
- **Method**: KG-constrained metric for catching material-level hallucination, plus knowledge injection, CoT and process RL in a domain-specific captioner.
- **Overlap**: C5 low (a domain-specific hallucination metric for captions); C1 low.
- **Recommendation**: optional.

---

## C. Post-hoc / decoding / inference-time journal papers (C1 contrast: "at decoding")

These are all training-free or inference-time methods, so their overlap with C1 is **none–low**. They confirm the journal literature is decoding-heavy, which supports VSPS's "data-level, single-pass" framing. Cite one or two as representatives.

| Title | Venue / year | DOI | Note |
|---|---|---|---|
| Real-time hallucination correction in VLMs using dynamic knowledge graph verification (CMVKG-Guard). Q.-V. Dang et al. | Discover Artificial Intelligence 2026 (Springer OA; Scopus not confirmed) | 10.1007/s44163-026-01778-z | Token-level verification against a per-inference KG (Wikidata, ConceptNet). Reports −84% CHAIR. Verification happens at decoding, the opposite of VSPS. C1 low. Vietnamese author group but English evaluation. |
| Mitigating Hallucinations in LVLMs via Reasoning Uncertainty-Guided Refinement (RUR). S. Li, X. Xu, …, H. T. Shen | IEEE TMM 2025 | 10.1109/TMM.2025.3599076 | Token/sentence-level uncertainty from Subjective Logic, used for refinement. C2 low: uncertainty here is internal, not evidence-based. |
| Visual Evidence-Aware for Object Hallucinations Rectification in LLM-Based Video Captioning. Y. Wang et al. | IEEE TCSVT 2025 | 10.1109/TCSVT.2025.3613993 | Diagnoses and corrects objects during decoding, and restores content rather than only removing it. C1 low; C3 low (correct vs. neutralize). |
| Boosting Faithful Multi-Modal LLMs via Complementary Visual Grounding (CVG). Z. Fu, Z. Mao, L. Zhang, Y. Zhang | IEEE TIP 2025 | 10.1109/TIP.2025.3644140 | Architecture-internal; explicitly avoids "extensive data curation". Useful contrast sentence. |
| Mitigating Hallucinations in LVLMs via Visual-Enhanced Contrastive Decoding (VECD). P. Qiang et al. | IEEE TMM 2026 | 10.1109/TMM.2026.3651099 | VCD variant. Natural journal companion to the VCD baseline VSPS already uses. |
| Mitigating Hallucinations in LVLMs with Fine-grained Cross-modal Attention. Z. Wen et al. | IEEE TMM 2026 | 10.1109/TMM.2026.3736511 | Title only. Attention method. |
| Evaluating and Mitigating Relationship Hallucinations in LVLMs (R-Bench, RA²M). M. Wu, …, R. Ji | IEEE TPAMI 2026 | 10.1109/TPAMI.2026.3656175 | Relation hallucination benchmark plus region-aware alignment. C4 low: VSPS's relation propositions could be tested on R-Bench. Should cite for the relation type. |
| Alleviating Hallucination in LVLMs with Active Retrieval Augmentation (ARA). X. Qu et al. | ACM TOMM 2025 | 10.1145/3742434 | Retrieval-augmented. Low overlap. |
| Enhancing Image Captioning through Bridging Image-Text Gap and Reducing Hallucinations (VTSRC). Z. Wang et al. | ACM TOMM 2025 | 10.1145/3776746 | Non-autoregressive captioner with visual-uncertainty contrast. Low overlap. |
| Mitigating hallucinations in image captioning via frequency perturbation entropy. L. Pan et al. | ESWA 2026 | 10.1016/j.eswa.2026.132544 | Title only. Captioning-specific. Likely a decoding/perturbation method. |
| Training-free counterfactual hallucination mitigation for LVLMs. X. Li et al. | Multimedia Systems 2026 | 10.1007/s00530-026-02577-3 | Title only. Low overlap. |
| Training-free and zero-shot regeneration for hallucination mitigation in MLLMs. D. Zhang et al. | ESWA 2026 | 10.1016/j.eswa.2026.131102 | Title only. Low overlap. |
| Mitigating hallucination in MLLMs via cross-layer visual anchors. C. Yang et al. | Pattern Recognition 2026 | 10.1016/j.patcog.2026.114380 | Title only. Low overlap. |
| STAR: object-centric prompting with detector priors. J. B. Ma, H. G. Han | Pattern Recognition Letters 2026 | 10.1016/j.patrec.2026.08.013 | Detector evidence goes into the prompt, with local verification of low-confidence regions at inference. Low overlap. |
| GLINT, global–local fusion with attention intervention. P. Zhao et al. | IPM 2026 | 10.1016/j.ipm.2026.104850 | Low overlap. |
| ALD2, adaptive layer-wise denoising decoding. Y. Zhou et al. | IPM 2026 | 10.1016/j.ipm.2026.104869 | Low overlap. |
| CoSE, connectivity-oriented semantic enhancement. Y. Hu et al. | Information Fusion 2026 | 10.1016/j.inffus.2026.104478 | Low overlap. |
| Attention Reallocation (zero-cost, controllable). C. Tu et al. | IJCV 2025 | 10.1007/s11263-025-02607-z | Controllable hallucination/recall trade-off at inference. Contrasts with VSPS's caution set at training time. |
| Sarah: hallucination detection via uncertainty quantification. F. Yue et al. | Image and Vision Computing 2026 | 10.1016/j.imavis.2026.105938 | Title only. Detection, not mitigation. Low overlap. |
| FaithViP: hallucination benchmark with synthetic visual prompts. Y. Gao et al. | IEEE TCSVT 2026 | 10.1109/TCSVT.2026.3708848 | Benchmark. Low overlap. |

---

## D. Surveys (journal) — cite one for framing

- **Hallucinations of large multimodal models: Problem and countermeasures.** S. Sun, Z. Lin, X. Wu. *Information Fusion* 2025. DOI 10.1016/j.inffus.2025.102970. Should cite.
- **A Survey of Multimodal Hallucination Evaluation and Detection.** Z. Chen et al. *IJCV* 2026. DOI 10.1007/s11263-026-02756-9. This is the journal version of arXiv 2507.19024, which covers M-HalDetect and FaithScore-style atomic checks. Should cite for the C5 metric framing.

## E. Gender (C3) and Vietnamese captioning (C5 context) — journal side

### E1. Mitigating Gender Bias Amplification in Image Captioning (LIBRA)
- **Authors / venue**: Y. Hirota, Y. Nakashima, N. García. *IEICE Trans. Information and Systems* 2025 (Scopus). DOI 10.1587/transinf.2024EDP7164.
- **Method**: Learns from synthetically biased samples to correct gender misclassification and stereotypical words.
- **Overlap**: C3 low–medium. It addresses the same failure (unsupported gender), but by debiasing a model rather than neutralizing training targets based on visual evidence.
- **How VSPS differs**: VSPS gates gender by evidence and backs off to "người" only when the evidence is not unanimous, so gender is kept when it is visible. Neutralization is a by-product of verification, not a fairness objective.
- **Recommendation**: should cite. Agent 04 covers the conference line, including Equalizer/ECCV 2018 and GAIC.

### E2. Vietnamese captioning and VLM journals
None of these address hallucination, so C5 overlap is **none**. They are context for "first hallucination evaluation of Vietnamese detailed captioning".

| Paper | Venue / DOI | Recommendation |
|---|---|---|
| UIT-OpenViIC: open-domain Vietnamese captioning benchmark. D. C. Bui et al. | Signal Processing: Image Communication 2025; DOI 10.1016/j.image.2025.117430 | Should cite: Vietnamese benchmark, n-gram metrics only. |
| Benchmarking Vietnamese image captioning: a spatially-aware transformer and the HDUCap dataset. A. C. Hoang et al. | JVCIR 2026; DOI 10.1016/j.jvcir.2026.104963 | Should cite: newest Vietnamese captioning journal paper, no hallucination metric. |
| A Novel Pretrained General-purpose Vision Language Model for the Vietnamese Language. Đ. N. Vũ et al. | ACM TALLIP 2024; DOI 10.1145/3654796 | Optional (Vietnamese VLM). |
| ViTextVQA. Q. V. Nguyen et al. | ESWA 2025; DOI 10.1016/j.eswa.2025.130839 | Optional. |

KTVIC (arXiv 2401.08100) still shows as a preprint only in OpenAlex; no journal version was found.

## F. Other journal items checked and judged not relevant
- **ExCap** (KBS 2026, 10.1016/j.knosys.2026.116639): zero-shot entity captioning; "faithful" refers to synthetic image–text alignment.
- **GroundCap** (Pattern Recognition 2026, 10.1016/j.patcog.2026.113703): grounded captioning dataset (ID-linked objects and actions). Could be RW for C4 traceability.
- **Weakly-supervised grounded captioning**: Applied Intelligence 2024 (10.1007/s10489-024-05389-y) and KBS 2024 (10.1016/j.knosys.2024.111433).
- **Celona et al.** (NCA 2025, 10.1007/s00521-025-11672-x): LLM fusion of multiple captions for descriptiveness, with no verification.
- **PAC-S++** (IJCV 2025, 10.1007/s11263-025-02535-y): evaluation and training metric; optional as an extra caption metric.

## Unverified
- I found no TPAMI/TIP/TNNLS/TAI journal extensions of HalluciDoctor, RLAIF-V, HALVA, LURE or KnowAda. They may exist after OpenAlex's indexing lag; re-check on IEEE Xplore before submission.
- The method details of ESWA 2026 Pan et al., IVC 2026 Sarah, IJCV 2026 REVERIE+, TMM 2026 Wen et al., InfFus 2025 Zeng et al., and Multimedia Systems 2026 Li et al. are inferred from titles only. Their abstracts were elided or could not be fetched (ScienceDirect and Springer returned 403 or a login redirect).
- I did not confirm whether MHR (TOMM 2026) includes Vietnamese among its languages.

---

## Highest-overlap risks
1. **HELTA (IEEE T-ITS 2025)**: offline cross-checked, "hallucination-free" description data. Medium overlap with C1. VSPS must say what it adds: typed propositions, a three-state verdict, neutralization, and SFT of a single-pass captioner.
2. **AQAH (IEEE TCSVT 2025)**: sample disagreement → uncertain info → targeted questions. Medium overlap with C2. Contrast: inference-time regeneration vs. an offline evidence gate that yields an UNCERTAIN verdict.
3. **MHR (ACM TOMM 2026)**: multilingual LVLM hallucination, claimed as "first attempt". Medium overlap with C5. VSPS should narrow its claim to *Vietnamese detailed captioning* with CHAIR, a Vietnamese lexicon and a gender metric.
4. **EPAlign (IEEE TASLP 2026)**: over-detailed training data causes hallucination. Medium overlap with the C1 motivation; cite as support, contrast global vs. per-proposition control.
5. **Woodpecker (SCIS 2024)**: the same verify-then-rewrite chain, but post hoc. Already cited; keep the contrast explicit.

## Suggested novelty statement (journal-side)
"Journal work on LVLM hallucination in 2024–2026 mostly intervenes at decoding or attention (e.g., VECD, RUR, CVG) or through RL/DPO objectives (e.g., metric-driven PPO, VGL-DPO). Data-level efforts either filter entities with binary cross-checks (HELTA) or tune overall data granularity (EPAlign). VSPS instead verifies each typed proposition offline with a three-state, dual-polarity voting verdict that separates *not visible* from *false*. It neutralizes rather than discards under-evidenced components and trains a single-pass captioner with standard SFT. To our knowledge, it is also the first hallucination evaluation of Vietnamese detailed captioning, using CHAIR with a Vietnamese object lexicon and an unsupported-gender metric."
