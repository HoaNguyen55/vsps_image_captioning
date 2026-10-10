# 04 — Gender bias and gender-neutral person references in captioning and VLMs

Agent 04. Scope: gender bias and gender-neutral person references in image captioning and VLMs, 2017–2026. The focus is overlap with **C3** (neutralizing UNCERTAIN gendered person nouns) and **C5** (the unsupported-gender-attribution metric).

**Method.** I ran 28 web queries and opened arXiv, ACL Anthology, CVF and publisher pages to confirm details. Checked against the VSPS v9 text (`FAIR_28.08.26_v9_EN_IEEE.pdf`): the paper's C3/C5 definitions are in §III (the neutralization operator N, the A(p_i) condition) and §IV (the 50-image challenge set, 46.9% → 4.1%).

Indexing notes: CVF/ICCV/CVPR papers are IEEE (Xplore, Scopus-indexed). ACL Anthology venues (EMNLP, NAACL, EACL, ACL) are Scopus-indexed in most years. ACM MM and WWW are ACM (Scopus-indexed). IEICE Trans. Inf. & Syst. is Scopus-indexed.

## VSPS positions being tested

- **C3.** UNCERTAIN propositions whose only uncertainty source is a gendered Vietnamese person noun (e.g., người phụ nữ / cậu bé) are rewritten to a neutral noun (người). This happens offline on the **SFT supervision data**. It reuses stored unanimous evidence (5/5) and never re-queries a model. The deployed model is single-pass.
- **C5.** The "unsupported gender attribution" metric is the share of captions using a gendered person noun that **no reference caption of the image uses**. It is explicitly *not* accuracy against visual gender. It is computed on a 50-image challenge set in Vietnamese.

---

## Papers (verified)

### 1. Women also Snowboard: Overcoming Bias in Captioning Models (Equalizer)
- **Authors:** Kaylee Burns\*, Lisa Anne Hendricks\*, Kate Saenko, Trevor Darrell, Anna Rohrbach
- **Venue:** ECCV 2018 (Springer LNCS; Scopus-indexed)
- **Link:** arXiv:1803.09797 (opened; full text read on ar5iv); CVF open-access page confirmed.
- **Method:**
  - Equalizer adds two training losses. The Appearance Confusion Loss enforces equal gender probability when the person is masked. The Confident Loss rewards confident gender words when person evidence is present.
  - The model is reported to output "person" when it is unsure.
- **Evaluation:**
  - Ground-truth gender is derived **from reference captions**: an image is "man" if at least one reference says man and none says woman, and vice versa.
  - Metrics are error (man↔woman), "Other" (neutral word), gender ratio Δ, and outcome divergence.
- **Overlap:**
  - C3 **medium-HIGH (conceptual).** It is the canonical precedent for "say *person* when gender evidence is weak." But the mechanism is a model-side loss on COCO-era LSTM captioners. There is no verification, no data-level rewriting and no per-proposition evidence.
  - C5 **medium.** It is reference-caption-derived gender labelling, as in VSPS. But Burns *discards* images whose references are neutral or mixed and scores man↔woman confusions. VSPS counts a gendered noun as unsupported whenever **no** reference uses one, so it penalizes asserting gender when annotators stayed neutral.
- **Distinguishing point:** VSPS gets "person when unsure" from **verified-evidence-driven rewriting of SFT targets** rather than a training loss. Its metric is reference-*support* based (a gendered noun absent from every reference), not man/woman error on gender-labelled images.
- **Recommendation:** **must cite & contrast** (already in the Q2 scan; keep it).

### 2. Exposing and Correcting the Gender Bias in Image Captioning Datasets and Models
- **Authors:** Shruti Bhargava (advisor D. A. Forsyth)
- **Venue:** UIUC MS thesis 2019; arXiv:1912.00578 (opened). Not peer-reviewed as a conference paper. A related arXiv 2023 note by L. Aggarwal & S. Bhargava, arXiv:2305.01888, has no venue.
- **Method:**
  - Captioning is decoupled into a **gender-neutral captioner**, trained on COCO captions with gendered words mapped to person / youngster.
  - A ResNet-50 then classifies the person crop as male / female / **indeterminate**. "person" is substituted with man/woman, or **kept as "person" if the class is indeterminate**.
- **Overlap:** C3 **medium.** "Neutral by default, gender only with visual evidence, else stay neutral" is close in spirit. But its neutralization is blanket, applied to all training captions. Gender is re-inserted by a separate classifier at inference, with no per-claim verification, no uncertainty from sampled VQA and no Vietnamese.
- **Distinguishing point:** VSPS neutralizes **only** propositions whose gender is UNCERTAIN under stored verifier evidence. It keeps verified gender (VSPS still uses a gendered noun in 64% of challenge captions whose references do). It needs no extra classifier at deployment.
- **Recommendation:** should cite (as the decoupling precedent; mark it as a thesis or preprint).

### 3. Mitigating Gender Bias in Captioning Systems (GAIC, COCO-GB)
- **Authors:** Ruixiang Tang, Mengnan Du, Yuening Li, Zirui Liu, Na Zou, Xia Hu
- **Venue:** WWW 2021 (ACM, pp. 633–645; Scopus-indexed)
- **Link:** arXiv:2006.08315 (confirmed)
- **Method:** It builds the COCO-GB v1/v2 splits (gender-balanced or shifted gender–context) and adds attention guidance toward person regions. Human annotators label male / female / **gender-neutral** (blurry or ambiguous).
- **Overlap:**
  - C3 low-medium. It also admits a neutral class when the image is ambiguous, but it is a model-side attention fix.
  - C5 low-medium. Its metric is gender prediction error against human labels.
- **Distinguishing point:** VSPS gets no gender labels from humans. It acts on SFT data, and its metric is reference-support based.
- **Recommendation:** should cite.

### 4. Quantifying Societal Bias Amplification in Image Captioning (LIC)
- **Authors:** Yusuke Hirota, Yuta Nakashima, Noa Garcia
- **Venue:** CVPR 2022, pp. 13450–13459 (IEEE; DOI 10.1109/CVPR52688.2022.01309; Scopus)
- **Link:** arXiv:2203.15395 (confirmed)
- **Extended version:** "Societal Bias in Image Captioning: Identifying and Measuring Bias Amplification," IEICE Trans. Inf. & Syst., 2025 (lab listing confirmed; vol/pages not confirmed).
- **Method:** LIC trains a classifier to predict gender from **masked** captions. It compares the classifier's accuracy on model captions with its accuracy on human captions. It also shows that methods that only fix gender-word prediction can amplify contextual bias.
- **Overlap:** C5 **low-medium.** It is the standard captioning bias metric, but it measures stereotyped *context* (gender words masked), not whether the gender word is supported. It needs gender-annotated COCO subsets.
- **Distinguishing point:** The VSPS metric measures **gender assertion unsupported by any reference** (a hallucination-style measure), not bias amplification. It is computable on KTVIC in Vietnamese without gender labels.
- **Recommendation:** must cite (to position C5 as complementary to LIC). Ideally also report or argue why LIC is not used, e.g., there is no Vietnamese gender classifier and no gender annotations on KTVIC.

### 5. Model-Agnostic Gender Debiased Image Captioning (LIBRA)
- **Authors:** Yusuke Hirota, Yuta Nakashima, Noa Garcia
- **Venue:** CVPR 2023, pp. 15191–15200 (IEEE; Scopus)
- **Link:** arXiv:2304.03693 (confirmed)
- **Extended version:** "Mitigating Gender Bias in Captioning Systems," IEICE Trans. Inf. & Syst., 2025 (lab listing confirmed; same title as Tang et al.).
- **Method:**
  - A caption *editor* is trained on synthetically biased captions (gender swapped, stereotypical words injected).
  - It post-hoc corrects gender misclassification and replaces stereotypical words with neutral ones.
  - It uses a gender filter on the synthetic data.
- **Overlap:** C3 **medium**, since it is output-text rewriting toward neutral wording. C1 low-medium, since it is a post-hoc output corrector.
- **Distinguishing point:** LIBRA is a **post-hoc output editor** that runs at inference and is learned from synthetic bias. VSPS rewrites **supervision data offline** from verifier evidence, and the deployed model is single-pass with no editor.
- **Recommendation:** must cite & contrast. It is the clearest example of "gender-neutral rewriting of captions" at the output side.

### 6. From Descriptive Richness to Bias: Unveiling the Dark Side of Generative Image Caption Enrichment
- **Authors:** Yusuke Hirota, Ryo Hachiuma, Chao-Han Huck Yang, Yuta Nakashima
- **Venue:** EMNLP 2024 (main), ACL Anthology 2024.emnlp-main.986 (Scopus)
- **Link:** arXiv:2406.13912 (opened)
- **Method:**
  - An analysis paper. LLM-enriched (detailed) captions such as ShareGPT4V, FuseCap and CapsFusion increase gender bias, and models trained on them amplify it: about +30.9% gender bias and +59.5% hallucination.
  - Metrics are gender error (woman↔man vs. the image's gender label), recall disparity, LIC and CHAIR.
  - It proposes no technical mitigation; it suggests human-in-the-loop oversight.
- **Overlap:**
  - C3 none as a method; strong *motivation* support.
  - C5 low-medium. Its gender error needs gender labels. It notes enriched captions "describe a gender that does not exist," but does not quantify that as a metric.
- **Distinguishing point:** VSPS is a concrete data-level remedy for exactly the "detail → gender + hallucination" problem this paper identifies. It quantifies unsupported gender directly.
- **Recommendation:** must cite (key motivation).

### 7. LOTUS: A Leaderboard for Detailed Image Captioning from Quality to Societal Bias and User Preferences
- **Authors:** Yusuke Hirota, Boyi Li, Ryo Hachiuma, Yueh-Hua Wu, Boris Ivanovic, Yuta Nakashima, Marco Pavone, Yejin Choi, Yu-Chiang Frank Wang, Chao-Han Huck Yang
- **Venue:** ACL 2025 Industry Track, pp. 295–309, DOI 10.18653/v1/2025.acl-industry.22
- **Link:** arXiv:2507.19362 (opened HTML)
- **Method:**
  - A detailed-caption leaderboard. Gender bias is measured as (a) the woman-vs-man performance disparity of each quality or hallucination metric (CLIP-S, CapScore, CHAIR_s, FaithScore, …) and (b) a gender representation gap |Δ| between female-term rate on woman images and male-term rate on man images.
  - It finds that caption detail correlates with bias risk.
- **Overlap:** C5 **medium.** It is the closest existing *detailed-caption* gender evaluation, but it needs binary gender image labels, is English-only, and measures disparity rather than unsupported assertion.
- **Distinguishing point:** VSPS measures gender words **not licensed by any reference**, in Vietnamese, without gender labels. Its result (4.1% unsupported, while gendered nouns are still used in 64% of reference-gendered cases) speaks to faithfulness, not parity.
- **Recommendation:** must cite (2025, detailed captioning, the same Hirota line).

### 8. BioPro: Towards Difference-Aware Gender Fairness for Vision-Language Models
- **Authors:** Yujie Lin, Jiayao Ma, Qingguo Hu, Wenbo Li, Genji Li, Derek Wong, Jinsong Su
- **Venue:** ACM Multimedia 2026 (per the arXiv comment; ACM, Scopus)
- **Link:** arXiv:2512.00807 (v1 Nov 2025, v2 Jul 2026; opened)
- **Method:**
  - Training-free. It finds a low-dimensional gender subspace via counterfactual embeddings and projects it out in "neutral" contexts, while preserving gender where it is explicit.
  - For captioning (LLaVA-1.5 / LLaVA-NeXT), the bias metric is the **share of captions containing gendered words** on COCO images labelled **"unsure gender"** (Zhao et al. 2021 annotations), with METEOR and CLIP-S for quality.
- **Overlap:**
  - C3 **medium**: "neutral when unsure, keep gender when explicit" is the same goal.
  - C5 **medium-HIGH**: a gendered-word rate on gender-ambiguous images is functionally close to "gendered noun when not supported."
- **Distinguishing point:**
  - BioPro is an **inference-time embedding projection**, and "unsure" comes from human gender annotations.
  - VSPS rewrites supervision text from per-proposition verifier evidence (SFT, no inference-time intervention). It defines support by **reference captions** (no gender annotations needed), works in Vietnamese, and targets detailed multi-proposition captions.
- **Recommendation:** must cite & contrast (closest recent work on both C3 and C5). Consider citing BioPro's gendered-word rate as the English analogue of the VSPS metric.

### 9. Think Before You Act: A Two-Stage Framework for Mitigating Gender Bias Towards Vision-Language Tasks (GAMA)
- **Authors:** Yunqi Zhang, Songda Li, Chunyuan Deng, Luyi Wang, Hui Zhao
- **Venue:** NAACL 2024 (long), pp. 773–791, DOI 10.18653/v1/2024.naacl-long.44 (opened)
- **Link:** arXiv:2405.16860
- **Method:** It frames gender bias as **object hallucination** (relying on object–gender co-occurrence). Stage 1 generates a **gender-obfuscated** narrative of the image. Stage 2 answers the task (including captioning) conditioned on that narrative and re-examines gender.
- **Overlap:** C3 **medium**, since it uses gender-obfuscated intermediate text and links gender bias to hallucination. C1 low, since it runs at inference in two stages.
- **Distinguishing point:** GAMA neutralizes gender in an **inference-time intermediate narrative** and needs two passes. VSPS neutralizes only UNCERTAIN gender in **training targets**, with a single-pass deployed model.
- **Recommendation:** should cite. It supports the "gender = hallucination" framing VSPS uses.

### 10. Masking Latent Gender Knowledge for Debiasing Image Captioning
- **Authors:** Fan Yang, Shalini Ghosh, Emre Barut, Kechen Qin, Prashan Wanigasekara, Chengwei Su, Weitong Ruan, Rahul Gupta
- **Venue:** TrustNLP @ NAACL 2024, pp. 227–238, DOI 10.18653/v1/2024.trustnlp-1.19 (opened)
- **Method:** An adversarially trained linear mask on a frozen captioner removes gender knowledge. It replaces more than 99% of gender words with neutral ones, at about −1.4 BLEU-4.
- **Overlap:** C3 medium-low. It is a blanket gender-neutralization of outputs, unconditioned on evidence.
- **Distinguishing point:** VSPS is selective. It neutralizes only when gender is unverified and keeps verified gender, so it is not blanket erasure.
- **Recommendation:** should cite (the contrast: selective vs. blanket neutralization).

### 11. Defining and Quantifying Visual Hallucinations in Vision-Language Models
- **Authors:** Vipula Rawte, Aryan Mishra, Amit Sheth, Amitava Das
- **Venue:** TrustNLP @ NAACL 2025, pp. 501–510, DOI 10.18653/v1/2025.trustnlp-main.32 (ACL Anthology confirmed)
- **Method:**
  - An eight-category captioning-hallucination taxonomy that includes **"Gender Anomaly."** It comes with the human-annotated VHILT dataset (2,000 captions from 8 VLMs).
  - The VHVI index ranks VLMs.
- **Overlap:** C5 low-medium. It treats wrong gender as a hallucination category, but uses human category labels and gives no reference-support metric. (I did not open the operational definition.)
- **Distinguishing point:** VSPS gives an automatic, reference-based rate for unsupported gender, plus a mitigation.
- **Recommendation:** should cite (precedent for "gender as hallucination").

### 12. Understanding and Evaluating Racial Biases in Image Captioning
- **Authors:** Dora Zhao, Angelina Wang, Olga Russakovsky
- **Venue:** ICCV 2021, pp. 14830–14840, DOI 10.1109/ICCV48922.2021.01456 (IEEE)
- **Link:** arXiv:2106.08503 (confirmed)
- **Method:** It provides perceived-gender (incl. **unsure**) and skin-tone annotations for 28,315 people in COCO-2014 val. The paper argues that caption-derived gender labels are unreliable.
- **Overlap:** C5 low-medium. It is the annotation resource BioPro relies on, and it critiques caption-derived gender labels, which VSPS also uses.
- **Distinguishing point / risk:** A reviewer could object that reference captions are a weak proxy for gender evidence. VSPS already says the metric "is not accuracy against visual gender." Cite Zhao et al. when stating that limitation. A cheap robustness check is possible because VSPS also evaluates COCO-2014: compute the same metric on the Zhao "unsure" subset.
- **Recommendation:** should cite.

### 13. Vision-Language Models Suppress Female Representations Under Ambiguous Input
- **Authors:** Arnau Marin-Llobet, Simon Henniger, Mahzarin R. Banaji
- **Venue:** EMNLP 2026 (accepted, per the arXiv comment)
- **Link:** arXiv:2605.31556 (opened)
- **Method:** Uses more than 800 gender-ambiguous images across 15 occupations and 4 VLMs. Outputs default to male under ambiguity, while internal states encode female associations. It proposes the LALS probing metric.
- **Overlap:** C3/C5 low. It is measurement only, but it is fresh evidence that VLMs **assert gender on ambiguous images**, which motivates C3.
- **Recommendation:** optional (good 2026 motivation cite).

### 14. Revealing Gender Bias in Language Models through Fashion Image Captioning
- **Authors:** Maria Villalba-Oses, Victoria Muñoz-Garcia, Juan Pablo Consuegra-Ayala
- **Venue:** RANLP 2025, pp. 1333–1340, DOI 10.26615/978-954-452-098-4-155 (ACL Anthology 2025.ranlp-1.155)
- **Method:** On gender-cue-free fashion images, GPT-4o and Grok often assign a gender, while Copilot more often stays neutral.
- **Overlap:** C5 low. It is gender assignment under ambiguity, measured by human annotation.
- **Recommendation:** optional.

### 15. Gender Bias in Vision-Language In-Context Learning (VL-BICLE)
- **Authors:** Tong Xiang, Yuta Nakashima, Noa Garcia
- **Venue:** arXiv:2609.27682 (Sep 2026; "ECCV 2026 submission" per comment; opened). A preprint.
- **Method:** Gendered in-context demos shift LVLM captioning bias. The mitigation swaps in synthetic in-context images.
- **Overlap:** low.
- **Recommendation:** optional.

### 16. Other verified works, low overlap (optional or background)

| Work | Venue | What it is | Overlap |
|---|---|---|---|
| Men Also Like Shopping (J. Zhao, T. Wang, M. Yatskar, V. Ordonez, K.-W. Chang) | EMNLP 2017, DOI 10.18653/v1/D17-1323 | Origin of "bias amplification." | Low; background only |
| VisoGender (S. M. Hall et al.) | NeurIPS 2023 D&B, arXiv:2306.12424 | Pronoun-resolution and retrieval gender-bias benchmark; finds captioners less biased than CLIP-style encoders. | Low |
| GenderBias-VL (Xiao et al., Beihang/Shanghai AI Lab) | arXiv:2407.00600; journal 2025 (journal name not confirmed) | Occupation counterfactual VQA benchmark for LVLMs. | Low |
| Examining Gender and Racial Bias in LVLMs Using a Novel Dataset of Parallel Images (PAIRS) (K. Fraser, S. Kiritchenko) | EACL 2024, ACL Anthology 2024.eacl-long.41 | Parallel-image dataset showing LVLM outputs differ by depicted gender and race. | Low |
| Revealing and Reducing Gender Biases in VLAs (L. Girrbach et al.) | ICLR 2025, arXiv:2410.19314 | Trait and occupation bias in 22 VLAs; fine-tuning debiasing. | Low |
| Balancing the Picture (B. Smith et al.) | NeurIPS 2023 workshop, arXiv:2305.15407 | Gender-edited synthetic contrast sets; caption gender neutralization via word-pair map. | Low |
| Are Gender-Neutral Queries Really Gender-Neutral? (J. Wang, Y. Liu, X. E. Wang) | EMNLP 2021, arXiv:2109.05433 | Rewrites captions man → person for neutral image-search queries. | Low; a lexical precedent for "neutral rewriting" |
| Breaking Language Barriers or Reinforcing Bias? (Al Sahili, Patras, Purver) | arXiv:2505.14160 (2025) | Multilingual CLIP shows **more** gender bias than English, including leakage into gender-neutral languages. | Low; supports the non-English motivation for C5 |

**Non-English captioning gender (Vietnamese, Chinese, Japanese).** Four targeted queries found **no** paper on gender bias or gender-neutral references in Vietnamese, Chinese or Japanese image captioning. Multilingual gender-bias work covers only CLIP retrieval (2505.14160) and text-to-image generation (MAGBIG, ACL 2025). This gap supports C5's Vietnamese framing.

## Unverified
- MAGBIG (Friedrich et al., "Multilingual Text-to-Image Generation Magnifies Gender Stereotypes," arXiv:2401.16092; ACL 2025 per search summary). I did not open the ACL page. It is text-to-image, so low relevance.
- GenderBias-VL journal venue (2025): the journal name was not confirmed.
- The IEICE 2025 journal versions of LIC and LIBRA: lab listings were confirmed, but volume and pages were not.

---

## Highest-overlap risks

1. **BioPro (ACM MM 2026, arXiv:2512.00807).** It has the same "neutral when unsure, keep gender when explicit" goal (C3). Its caption metric is the share of gendered words on gender-unsure images, which is close to C5. Contrast: inference-time embedding projection and human gender labels, vs. evidence-driven SFT-data rewriting and reference-support labelling in Vietnamese.
2. **Women also Snowboard / Equalizer (ECCV 2018).** It is the canonical source of "say *person* when gender evidence is weak" and of reference-caption-derived gender labels. Reviewers will treat C3 as an instance of this idea, so the novelty must be the mechanism: selective, verifier-gated, offline, data-level.
3. **LIBRA (CVPR 2023; IEICE 2025).** It rewrites captions to correct gender and neutralize stereotyped words. Contrast: post-hoc output editor vs. offline supervision rewriting with a single-pass deployed model.
4. **Bhargava 2019 (arXiv:1912.00578).** It uses neutral captions plus a male/female/indeterminate classifier that keeps "person" when indeterminate. Contrast: blanket neutralization plus a separate classifier at inference, vs. selective neutralization of only UNCERTAIN propositions.
5. **LOTUS (ACL 2025) and From Descriptive Richness to Bias (EMNLP 2024).** They already establish gender evaluation for *detailed* captions and the detail↔gender↔hallucination link. C5 cannot claim to be the first gender evaluation of detailed captions. It can claim to be the first *Vietnamese*, label-free, reference-support-based unsupported-gender metric.

No paper found combines: (a) verifier-gated, per-proposition gender neutralization of **training data**, (b) a three-state "not visible ≠ false" distinction applied to gender, and (c) Vietnamese gendered person nouns. No overlap is HIGH on C3 or C5 as stated, but several are medium or medium-high on the underlying idea.

## Suggested novelty statement

"Prior work makes captioners say *person* when gender evidence is weak through training losses [Burns 2018], post-hoc caption editing [LIBRA], inference-time debiasing [GAMA, BioPro], or blanket gender removal [Bhargava 2019; Yang 2024]. VSPS instead neutralizes gender **selectively in the supervision data**: only propositions whose gender a verifier leaves UNCERTAIN are rewritten (người phụ nữ → người), using stored evidence. Verified gender is kept, and the deployed model needs no extra component. Unlike gender metrics that need gender-labelled images [LIC, LOTUS, BioPro], our unsupported-gender-attribution rate is computed against reference captions, which makes it, to our knowledge, the first such measure for Vietnamese captioning."
