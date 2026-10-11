# 01. Novelty check: Cross-Lingual Witnesses (XWit)

Date: 2026-10-11. Scope: the core idea of `00_DE_XUAT.md`. Agreement between one VLM's outputs in several languages (or translation round-trips) serves as evidence that a mentioned object is real, and a high-resource language is used to raise recall for Vietnamese. Papers already covered in `research_wall/10_cross_lingual_hallucination.md` (M²CQA, Hinck, MM-JudgeBench, DEJIMA, ...) are only mentioned again where they bear on overlap. Sources were arXiv abstract and HTML pages, ACL Anthology and CVF, plus web search. Every paper marked "opened" had its abstract or method section read. The rest come from search snippets and are marked as such.

Contributions under test (from §2 of the proposal):
- **C1** ρ, the cross-lingual hallucination correlation, used to split hallucinations into perceptual and linguistic without labels.
- **C2** The operating-point proposition (ROC dominance implies higher recall at precision ≥ p₀), plus the F*/2 threshold rule.
- **C3** XWit: a fused score built from the number of language witnesses, the Vintern logit and per-language co-occurrence priors.
- **C4** Distillation into a single-pass Vietnamese SFT model.
- **C5** A Vietnamese POPE/CHAIR benchmark built on the 300-image human gold set.

## 1. Close papers

### Text LLMs: cross-lingual agreement as a hallucination or uncertainty signal

**T1. Rowen** (Ding, Pang, Wei, Shen, Cheng). arXiv:2402.10612, SIGIR-AP 2025. https://arxiv.org/abs/2402.10612 (opened, method read)
- *Rowen-CL* paraphrases a question k=6 times, translates the paraphrases EN→ZH, and has an LLM judge whether each English and Chinese answer pair agrees. The average agreement is the consistency score.
- A score below a threshold (0.6 was best) is treated as a likely hallucination and triggers retrieval.
- EN–ZH works better than EN–FR or EN–DE. The authors' explanation is that the languages are more distant, so the errors are less correlated.
- **This is the "cross-lingual disagreement means hallucination" principle, already published.**
- Overlap: C1 partial (it assumes the errors are decorrelated but never measures that), C3 partial (same principle, used as a trigger). C2, C4 and C5: none.

**T2. Teaching LLMs to Abstain across Languages via Multilingual Feedback** (Feng, Shi, Wang, ... Tsvetkov). EMNLP 2024. https://aclanthology.org/2024.emnlp-main.239 (abstract opened)
- The model critiques its own answer in related languages (e.g. Bengali checked through Hindi, Marathi and Nepali) and abstains when the critiques reveal a knowledge gap.
- This raises abstention accuracy for low-resource languages by up to 9.2%.
- **This is "use other languages to decide whether to trust a low-resource answer"**, i.e. abstention, the precision side.
- Overlap: C3 partial, C1 none, C4 none.

**T3. Cross-Lingual Consistency (CLC) inference framework** (Yu, Li, et al.). arXiv:2504.01857, 2025. https://arxiv.org/abs/2504.01857 (search snippet plus abstract)
- Majority vote over reasoning paths written in up to 11 languages. It beats monolingual self-consistency by 4–18 points on CMATH and MGSM.
- Its stated mechanism is that voting across languages "neutralizes linguistic biases", which is H1/H2 for text.
- Overlap: C3 partial; it also pre-empts H2 ("cross-lingual beats K same-language samples") for text QA.

**T4. CALM** (Wang, Fan, Wang, Fung, Ji). NAACL 2025. https://arxiv.org/abs/2501.18457 (abstract opened)
- Samples answers in several languages, takes the cross-lingual majority answer as the positive and the others as negatives, then runs DPO.
- **This is distilling a cross-lingual-agreement signal back into one model.**
- Overlap: C4 partial, C3 partial.

**T5. Cross-Lingual Consistency of Factual Knowledge in Multilingual LMs** (Qi, Fernández, Bisazza). EMNLP 2023. https://aclanthology.org/2023.emnlp-main.658 (abstract)
- Proposes the RankC metric. Consistency does not grow with model size, and knowledge edited in English transfers only to languages with high RankC.
- It measures consistency of *knowledge*, not correlation of *errors*, and has no vision.
- Overlap: C1 partial (closest metric precedent to cite and contrast). Other contributions: none.

**T6. Related text work (snippets only).** Xing et al. arXiv:2407.01358 (LASER cosine across languages); CrossHallu arXiv:2607.04029 (internal-state probes degrade EN↔AR). Overlap: low.

### VLMs: multilingual hallucination, with English as the reference

**V1. MHR** (Qu, Song, Wei, Dong, Cheng). ACM TOMM 2026, doi:10.1145/3797025, arXiv:2408.00550. https://arxiv.org/html/2408.00550 (method §III-B read)
- For each non-English query it samples N=20 responses and machine-translates them to English. It scores each against the English non-hallucinated and hallucinated answers (CE loss or BLEU), then builds DPO pairs: the closest to the English correct answer is preferred, the farthest is rejected.
- Covers 13 languages; Vietnamese is not among them.
- **This is "cross-lingual alignment to English as a hallucination label for training data", plus distillation.** It is the closest VLM scoop.
- Overlap: C3 partial–high (cross-lingual agreement is used as the hallucination signal, but at response level and with English as the oracle rather than as one witness), C4 partial (it distills via DPO), C1 none, C5 partial (it translates POPE/AMBER, without vi).

**V2. CLAIM** (Ye, Li, Feng, Qin, ... Qin). ACL 2025. https://arxiv.org/abs/2506.11073 (abstract)
- Finds language-specific cross-modal attention heads and estimates EN→target "language shift vectors". At inference it pushes non-English attention toward the English pattern (+13.56% POPE on average).
- **This is "borrow the high-resource language to fix the low-resource one"**, done inside the model.
- Overlap: the recall-borrowing framing is partial. Its mechanism differs (attention, not output agreement). C1/C3/C4: none or low.

**V3. Ye, Santy, Hwang, Zhang, Krishna, "Semantic and Expressive Variations in Image Captions Across Languages"**. CVPR 2025, arXiv:2310.14356. https://arxiv.org/abs/2310.14356 (abstract)
- Human multilingual caption sets cover about 22–30% more objects than monolingual ones, and LLaVA prompted in different languages "describes different parts of the image".
- **This pre-empts the "borrow recall from other languages" observation** and is a direct confounder for C1: disagreement across languages may be legitimate differences in *salience*, not hallucination.
- Overlap: C1 partial (confound), C3 partial (the recall motivation).

**V4. Buettner, Emmerson, Kovashka, Multimodal Recaptioning for Perceptual Diversity Across Languages**. IJCNLP-AACL 2025, arXiv:2504.14359 (abstract)
- Captions in different languages mention different objects (e.g. Japanese mentions sunglasses more often), and translated English captions carry English perceptual bias.
- Same confound as V3. Overlap: C1 low–partial.

**V5. Raihan & Chowdhury, "Causal Localization of the English Pivot in LLaVA"**. MeLLM 2026 workshop, https://aclanthology.org/2026.mellm-1.25/ (snippet)
- Non-English visual queries pass through an English-biased bottleneck in layers 5–17.
- **This is evidence against independence of the witnesses.** If every language goes through an English latent, language-prior errors are shared across languages, so a high ρ cannot be read as "perceptual".
- Overlap: none, but it is a threat to the identifiability of C1.

**V6. Traveling Across Languages (KnowRecall / VisRecall)**. arXiv:2505.15075, 2025 (snippet)
- Cross-lingual consistency benchmark for MLLMs on landmark VQA and image-free description, 15 and 9 languages.
- Treats consistency as the evaluation target, not as evidence. Overlap: C1 low.

**V7. M²CQA / CFHR** (Mousi et al.). Findings ACL 2026, arXiv:2602.05437. Already in research_wall/10.
- Per-language hallucination rates only, no correlation across languages. Overlap: C1 low.

**V8. Attribution of VLM hallucination to language prior vs perception**
- VCD (Leng et al., CVPR 2024) uses visual noise to expose priors.
- LURE (Zhou et al., ICLR 2024) attributes hallucinations to co-occurrence, uncertainty and position.
- HalLoc (Park et al., CVPR 2025) defines a "language-prior" hallucination type via the question alone.
- Causal-HalBench (arXiv:2511.10268) treats co-occurrence as a confounder.
- ROPE (Chen et al., NeurIPS 2024) finds the visual modality contributes less than 20% in multi-object hallucination.
- The decomposition idea itself is old. Every existing operationalisation uses image ablation, noise or co-occurrence statistics; none uses language variation.
- Overlap: C1 partial on the concept, none on the instrument.

**V9. VL-Uncertainty** (arXiv:2411.11919): prompt-perturbation consistency, no language perturbation. Overlap: C3 low.

### Theory

**C2 prior art.**
- Davis & Goadrich, ICML 2006: a curve dominates in ROC space iff it dominates in PR space.
- Lipton, Elkan, Naryanaswamy, ECML-PKDD 2014: the F1-optimal threshold on a calibrated score equals F*/2.
- The Neyman–Pearson corollary (fix precision ≥ p₀, then the dominating score has recall ≥ the old one) follows in two lines from Davis & Goadrich.
- **C2 is scooped as theory.** It is still useful as a framing lemma with citations.

### Vietnamese benchmark (C5)

- Searches for Vietnamese POPE or CHAIR found nothing. Translated POPE suites (MHR POPE-MUL, Multi-POPE) skip Vietnamese.
- ViHallu (DSC2025) is text-only; the visual "ViHallu" is known only from an aggregator and was not verified.
- Consistent with `novelty/05` and `novelty/09`.

## 2. Verdict per contribution

| | Verdict | Closest prior | Why |
|---|---|---|---|
| C1 ρ and the perceptual/linguistic split | **Partial (instrument novel, interpretation contested)** | Rowen-CL, Qi 2023, Ye CVPR 2025, English-pivot 2026, VCD/HalLoc | No paper measures object-level error correlation across languages for the same image and model, so the measurement is novel. Reading ρ as "perceptual vs prior" is not identified: shared LM/English-pivot priors make prior errors correlated, and salience differences (Ye; Buettner) create disagreement without any hallucination. |
| C2 operating-point theory | **Scooped** | Davis & Goadrich 2006; Lipton et al. 2014 | Known results. Keep only as a cited lemma. |
| C3 XWit fused score | **Partial** | MHR (VLM, cross-lingual alignment as label), Rowen-CL, Feng 2024, CLC, CALM | "Cross-lingual agreement implies truth" is published for text and, for VLMs, as response-level alignment to English. Still novel: object-level witness counts on open-ended captions, fused with a calibrated verifier logit and per-language co-occurrence priors, with Vietnamese as the target and English as a witness rather than the oracle. |
| C4 distillation | **Partial** | MHR (DPO), CALM (DPO) | Distilling a cross-lingual signal into one model is done. SFT targets built at a chosen Neyman–Pearson operating point, with typed propositions, are not. |
| C5 Vietnamese POPE/CHAIR | **None found** | MHR POPE-MUL (no vi) | Still open. It is a resource contribution, not a method one. |
| "Borrow recall from a high-resource language" | **Partial** | Ye CVPR 2025, CLAIM, Hinck 2024 | The observation is known. The mechanism (a union of witnesses, verified in Vietnamese) is new in this setting. |

## 3. What remains novel and how to reposition

**Do not claim:**
- "First to use cross-lingual consistency to detect hallucination." Rowen-CL, Feng 2024 and MHR already do.
- "A new theory of the precision/recall trade-off." C2 is Davis & Goadrich plus Lipton.
- "ρ separates perceptual from linguistic hallucination." This is not identifiable without a control.

**Defensible claims:**
1. **Measurement (main contribution).** "We give the first object-level measurement of how correlated a VLM's hallucinations are across output languages on the same image, and compare it with the correlation within one language across samples."
   - Call it *language-invariant vs language-specific* error, not perceptual vs prior.
   - To support the causal reading, add two controls:
     - an **image-free** (blank or text-only) run in each language, which estimates the pure language-prior hallucinations (HalLoc/VCD style);
     - a **salience control** that scores only gold objects, so that recall differences (Ye CVPR 2025) are not counted as disagreement.
   - Test the English-pivot threat directly: if ρ_cross ≈ ρ_within, the witnesses are not independent (H1 rejected). The proposal already accepts that outcome as a finding.
2. **Method, framed as an extension.** "MHR uses response-level alignment to an English oracle to label DPO pairs. Rowen-CL and Feng 2024 use cross-lingual agreement for text QA. We turn cross-lingual agreement into *object-level evidence* for open-ended captions, combine it with a calibrated in-language verifier, and use it to *raise recall* (union of witnesses, then verify) rather than only to abstain."
   - Baselines: MHR-style alignment to English, Rowen-CL-style agreement, and K-sample self-consistency (H2).
   - CALM and MHR are the distillation baselines to cite in C4.
3. **Vietnamese resource (C5)**, unchanged, plus a ρ measurement on Vietnamese, which no prior study covers.
4. **C2** goes into a short "Analysis" paragraph citing Davis & Goadrich and Lipton, presented as an explanation of why the strict verifiers lose on F1. It should not be listed as a contribution.

**Unverified:** the English-pivot paper and CLC were seen only via snippets or abstracts; read them before citing. Search did not surface any VLM paper using caption-level cross-lingual *object* agreement, but the 2026 workshop literature is thinly indexed. Re-run `"cross-lingual" AND hallucination AND (caption OR LVLM)` on arXiv before submission.
