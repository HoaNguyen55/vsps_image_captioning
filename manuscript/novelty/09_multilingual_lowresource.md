# 09 — Multilingual / low-resource hallucination (focus C5, C3)

Search date: 2026-10-10. Sources: arXiv abstract/HTML pages, ACL Anthology, CVF Open Access, IJCAI proceedings PDF (opened). Already in Q2_LITERATURE.md §1D/1E and **not re-verified beyond what is new**: UIT-ViIC, UIT-OpenViIC, KTVIC, Vintern-1B, LaVy, ViExam/VMMU, DSC2025 ViHallu, Women also Snowboard, Hirota 2024 (descriptive richness → bias), BioPro. Qu et al. (MHR) and CLAIM were re-opened to check language lists and metrics. That check matters for C5.

**Bottom line:** no paper found that (a) evaluates hallucination in Vietnamese **detailed captioning** with CHAIR or a similar metric, (b) builds a Vietnamese object lexicon for CHAIR, (c) measures unsupported gender attribution in a non-English language with grammatical gender-marked person nouns, or (d) neutralizes under-evidenced attributes in non-English SFT data. Multilingual LVLM hallucination work is almost entirely **POPE/MME (yes/no probing)**. None of it covers Vietnamese, and none of it is captioning-level. **No HIGH overlap.**

---

## A. Multilingual LVLM hallucination: mitigation

### A1. Mitigating Multilingual Hallucination in Large Vision-Language Models (MHR)
- Authors: X. Qu, M. Sun, W. Wei, J. Dong, et al.
- Venue: ACM Trans. Multimedia Computing, Communications and Applications (TOMM) 2026 (**ACM, Scopus-indexed**). arXiv:2408.00550 (opened). DOI 10.1145/3797025 resolves to dl.acm.org; the page returned 403, so details are taken from Q2_LITERATURE.
- Method: two stages. Multilingual SFT, then DPO on "hallucination-aware" pairs. Pairs come from 20 sampled non-English responses per query, translated back to English and ranked by cross-entropy against English hallucinated and non-hallucinated references (K=3).
- Languages: English plus ru, de, zh, ja, fr, es, pt, uk, bg, tr, ar, ko. **Vietnamese not included.** Benchmarks: POPE-MUL, MME-MUL, AMBER-MUL. CHAIR appears only inside AMBER. No captioning-specific benchmark, no gender analysis.
- Overlap: C1 **medium**. It also improves training data for non-English hallucination, but through preference pairs ranked against **English reference answers**, not per-proposition visual verification. C5 **low–medium** (multilingual hallucination evaluation exists, but not Vietnamese and not detailed captions). C2/C3/C4 none.
- VSPS distinction: verifies each atomic proposition against the image with three states, needs no English reference answer, uses SFT only (no DPO), and evaluates Vietnamese detailed captions with CHAIR and a gender metric.
- Recommendation: **must cite & contrast** (closest multilingual mitigation work).

### A2. CLAIM: Mitigating Multilingual Object Hallucination in LVLMs with Cross-Lingual Attention Intervention
- Authors: Z. Ye, Q. Li, X. Feng, L. Qin, et al.
- Venue: ACL 2025 (long), pp. 13080–13094 (**ACL Anthology; Scopus-indexed proceedings**). arXiv:2506.11073 (opened); DOI 10.18653/v1/2025.acl-long.640.
- Method: training-free. It probes for language-specific cross-modal attention heads, estimates an English→target "language shift vector", and adds that vector to the head outputs at inference.
- Languages: zh, es, ru, pt, bg, hi, de. **No Vietnamese.** Benchmarks: POPE and the MME hallucination subsets (including colour). No CHAIR, no captioning.
- Overlap: C1 **low** (decoding-time and intervention-based, the opposite design choice). C5 **low**.
- VSPS distinction: data-level, the deployed model runs single-pass with no inference-time intervention, and the evaluation is on generative captions rather than yes/no probes.
- Recommendation: **should cite** as the decoding/intervention contrast. It could also serve as an optional baseline if it ports to Qwen2.5-VL.

### A3. MELLA: Bridging Linguistic Capability and Cultural Groundedness for Low-Resource Language MLLMs
- Authors: Y. Gao, J. Fei, N. Chen, R. Chen, G. Yan, Y. Lan, B. Shi.
- Venue: IJCAI 2026 (proceedings paper 0125, PDF opened). arXiv:2508.05502 (opened). IJCAI proceedings are Scopus-indexed.
- Method: dual-source SFT dataset for 8 low-resource languages, **including Vietnamese** (ar, cs, hu, ko, ru, sr, th, vi). It combines native web alt-text for cultural grounding with MLLM-generated English detailed descriptions **machine-translated** into the target language. Its claim is that this reduces "cultural hallucination", which it defines as culturally thin descriptions that miss specific entities.
- Overlap: C1 **low–medium**. It is SFT-data curation for low-resource detailed descriptions including Vietnamese, but it has **no proposition-level verification**: alt-texts are unverified, and generated descriptions are translated rather than checked. Its "hallucination" means missing cultural entities, not unsupported content. C5 **low** (no CHAIR, no gender metric). C3 none.
- VSPS distinction: VSPS targets **unsupported content** (precision) rather than cultural coverage (recall), and verifies every supervision proposition. MELLA's pipeline (translated detailed descriptions) is exactly the kind of unverified supervision VSPS argues against.
- Recommendation: **should cite**. It is the only 2025–26 low-resource detailed-description SFT dataset found that contains Vietnamese, and it makes a useful contrast.

### A4. PALO: A Polyglot Large Multimodal Model for 5B People
- Authors: M. Maaz, H. Rasheed, A. Shaker, et al.
- Venue: WACV 2025 (per authors; not re-verified), arXiv:2402.14818 (search result).
- Method: translates LLaVA-Instruct-150K into 10 languages (including ar, hi). Native-speaker review covers only a subset.
- Overlap: C1 low (translated instruction data, no hallucination control). C5 none.
- Recommendation: optional. Cite as an example of translated supervision without verification.

## B. Multilingual LVLM hallucination: benchmarks / detection

### B1. Can Humans Dream of Electric Sheep? Human-Written Samples for Fine-Grained V&L Hallucination Benchmarking (SHEEP)
- Authors: T. Mickus, C. Savelli, E. Calò, … , J. Tiedemann, R. Vázquez.
- Venue: arXiv:2608.01021 (Aug 2026, preprint, opened).
- Content: span-level hallucination labels on 1,600 human-written and 18,400 model-generated V&L outputs in **zh, en, fr, it**. Prompts come from HaloQuest/VISAGE and were machine-translated.
- Overlap: C5 **low–medium**. It is a multilingual, fine-grained (span-level) hallucination annotation, but for detection in 4 languages, not Vietnamese, and not CHAIR-style captioning. C2 low (the span taxonomy has no "not visible ≠ false" state).
- Recommendation: **should cite** as the most recent multilingual fine-grained hallucination benchmark. VSPS can note that Vietnamese is absent.

### B2. Overview of SHROOM-Visions 2026: A Shared Task on Hallucination Detection in LVLMs
- Authors: R. Vázquez, A. Sinha, C. Li, … , T. Mickus.
- Venue: UncertaiNLP Workshop @ EMNLP 2026. arXiv:2608.25662 (opened). The ACL workshop is likely Scopus-indexed (not confirmed).
- Content: shared task on SHEEP. 27 teams, 5-class span taxonomy, languages zh/en/fr/it.
- Overlap: C5 low. Recommendation: optional (cite together with B1).

### B3. Multilingual Training and Evaluation Resources for Vision-Language Models (Multi-PixMo, Multi-POPE)
- Authors: D. Baiamonte, E. Fano, M. Gabburo, S. Simonazzi, L. Rigutini, A. Zugarini.
- Venue: arXiv:2604.18347 (Apr 2026, preprint, opened).
- Content: translated POPE/MME/MMBench/ScienceQA/AI2D in fr/de/it/es, plus a regenerated multilingual training corpus. **No Vietnamese.**
- Overlap: C5 low. It is another translated-probe benchmark (translated evaluation, like VSPS's COCO-in-Vietnamese, but for yes/no POPE rather than generated captions). Recommendation: optional.

### B4. KOFFVQA (Korean free-form VQA with a hallucination category)
- arXiv:2503.23730 (search result only; venue not checked). Korean VQA with a hallucination sub-score, not captioning. Overlap C5 low. Optional.

### B5. ThaiOCRBench
- IJCNLP-AACL 2025 (ACL Anthology 2025.ijcnlp-long.89, search result). Thai text-rich VQA. Error analysis names hallucination, but the benchmark is not a captioning hallucination metric. Overlap none–low. Optional (only if the paper argues "SEA languages lack hallucination benchmarks").

### B6. HalDec-Bench: Benchmarking Hallucination Detector in Image Captioning
- Authors: K. Saito, R. Shinoda, S. Tanaka, T. Hirasawa, F. Okura, Y. Ushiku.
- arXiv:2603.15253 (opened). **v2 (24 Mar 2026) is marked withdrawn**, so cite with caution. Caption-level, segment-labelled detector benchmark; the caption language is not stated (most likely English). Relevant to C2 rather than this topic. Optional.

## C. Multilingual factuality (text-only, for C2/C5 framing)

### C1. An Analysis of Multilingual FActScore
- Authors: K. T. Vu, M. Krumdick, V. Reddy, F. Dernoncourt, V. D. Lai.
- EMNLP 2024 (ACL Anthology 2024.emnlp-main.247; arXiv:2406.19415, opened).
- Finding: atomic-fact verification pipelines degrade in medium- and low-resource languages. The extractor, the verifier and knowledge-source coverage all fail.
- Overlap: C2/C5 low (text-only), but it **supports a VSPS design choice**: verifying with yes/no queries against the image avoids relying on a weak low-resource knowledge source or verifier. Recommendation: optional / should cite if the paper defends "proposition verification works in Vietnamese".

### C2. Multi-FAct: Assessing Factuality of Multilingual LLMs using FActScore
- S. Shafayat, E. Kim, J. Oh, A. Oh. arXiv:2402.18045 (opened). The search snippet said COLM 2024 (not re-confirmed). Text-only. Optional.

### C3. Poly-FEVER
- arXiv:2503.16541 (opened). 11-language claim verification for text LLMs. None for VSPS. Skip.

## D. Language-specific grammatical issues (gender, colour) — supports C3 and the colour cross-check

### D1. Model-Agnostic Gender Debiased Image Captioning (LIBRA)
- Y. Hirota, Y. Nakashima, N. Garcia. CVPR 2023, pp. 15191–15200 (**IEEE/CVF, Scopus-indexed**; CVF Open Access page confirmed in search). arXiv:2304.03693.
- Method: a post-hoc caption editor trained on synthetically biased captions. It corrects gender misclassification and stereotyped words without retraining the captioner.
- Overlap: C3 **medium (conceptually)**. Rewriting gendered words in captions is close to neutralization, but LIBRA is learned, post hoc, English-only, and corrects gender rather than abstaining from it. VSPS neutralizes in **supervision data**, uses **evidence** (a split vote among verifiers) rather than a learned classifier, and handles Vietnamese person nouns.
- Recommendation: **should cite & contrast** in the C3 paragraph. It is not in Q2_LITERATURE §1E.

### D2. Mitigating Gender Bias in Captioning Systems (GAIC)
- R. Tang, M. Du, Y. Li, Z. Liu, N. Zou, X. Hu. arXiv:2006.08315 (search result). Published at WWW 2021 per the authors (not re-verified).
- Method: attention guidance toward the person, plus COCO-GB splits. Notes that BLEU/CIDEr are insensitive to gender errors.
- Overlap: C3 low, C5 low–medium (its gender-error metric is an English precedent for VSPS's unsupported-gender-attribution metric). Recommendation: should cite next to Burns/Hendricks when introducing the gender metric.

### D3. Breaking Language Barriers or Reinforcing Bias? Gender and Racial Disparities in Multilingual Contrastive VLMs
- Z. Al Sahili et al. arXiv:2505.14160 (search result). Multilingual CLIP audit across 10 languages: gender skew is stronger than in English, and strongest in languages with heavy grammatical gender marking. Retrieval, not captioning.
- Overlap: C3 low. Supporting evidence that non-English outputs carry extra gender risk. Optional.

### D4. Beyond Content: How Grammatical Gender Shapes Visual Representation in Text-to-Image Models
- Saeed et al. Findings of EMNLP 2025 (ACL Anthology 2025.findings-emnlp.1343; arXiv:2508.03199, search result). Text-to-image direction. Overlap none–low. Optional.

### D5. Color Names in Vision-Language Models
- A. Gomez-Villa, P. Hernández-Cámara, M. A. Butt, V. Laparra, J. Malo, J. Vazquez-Corral. arXiv:2509.22524 (Sep 2025, preprint, opened).
- Finding: VLMs name prototypical colours well but non-prototypical ones poorly. The cross-lingual analysis covers 9 languages (the list was not visible in the abstract, so Vietnamese is unconfirmed), and the vocabulary is strongly skewed toward English and Chinese.
- Overlap: C2 colour cross-check **low**. It supports the claim that colour attributes are unreliable and need a second check. No paper found that addresses the Vietnamese "xanh" (blue/green) ambiguity in captioning or VLMs.
- Recommendation: optional / should cite if the paper justifies the colour cross-check or the "xanh" handling.

### D6. Vietnamese gender-neutral nouns ("người") in MT/captioning
- No peer-reviewed study found. Only Korean (Cho et al., GeBNLP 2019, W19-3824, a TGBI metric for gender-neutral pronouns) and generic gender-neutral MT work exist. **Gap VSPS can claim.**

## E. Vietnamese-specific (new items not in Q2_LITERATURE)

- **AutoViVQA** (N. A. Tuong et al., arXiv:2603.09689, opened). An automatically constructed Vietnamese VQA dataset. Not about hallucination. Optional, as evidence that Vietnamese multimodal data is increasingly LLM-generated (which motivates verification).
- **ViCLIP-OT** (arXiv:2602.22678, search result). Vietnamese retrieval, evaluated on KTVIC/UIT-OpenViIC. Not about hallucination. Optional.
- No Vietnamese LVLM **hallucination** benchmark found (re-confirmed, consistent with Q2_LITERATURE on ViHallu being text-only).

## Unverified / not found
- "MHumanEval"-style multilingual LVLM hallucination benchmark: **not found**; do not cite.
- A CHAIR adaptation to Chinese, Japanese or any other non-English language with a native object lexicon: **not found**. MHR's AMBER-MUL runs CHAIR inside AMBER on translated prompts; I could not confirm whether its object matching is done in the target language or after translation back to English.
- PALO venue (WACV 2025) and GAIC venue (WWW 2021): from memory or authors' pages, not opened.
- Multi-FAct venue (COLM 2024): from a search snippet only.

---

## Highest-overlap risks
1. **Qu et al., MHR (ACM TOMM 2026)**: C1 medium. A reviewer may say non-English hallucination mitigation via data/preferences already exists. Contrast: English-reference ranking + DPO on yes/no probes vs. per-proposition visual verification + SFT on Vietnamese detailed captions.
2. **MELLA (IJCAI 2026)**: C1 low–medium. A low-resource detailed-description SFT set that **includes Vietnamese**. Contrast: its supervision is translated and unverified, and it targets cultural recall rather than unsupported-content precision.
3. **LIBRA, Hirota et al. (CVPR 2023)**: C3 medium (conceptual). Gendered-word editing in captions. Contrast: post hoc, learned, English vs. evidence-gated neutralization of supervision data in Vietnamese.
4. **SHEEP / SHROOM-Visions 2026**: C5 low–medium. A multilingual fine-grained hallucination benchmark. Contrast: 4 high-resource languages, detection only, no Vietnamese, no CHAIR.
5. **CLAIM (ACL 2025)**: C5 low. Multilingual POPE/MME. Contrast: inference-time intervention, yes/no probes, no Vietnamese.

## Suggested novelty statement (topic 09)
"Existing multilingual LVLM hallucination studies [Qu et al.; CLAIM; SHEEP] evaluate translated yes/no probes or span detection in high-resource languages and do not cover Vietnamese, and low-resource caption datasets such as MELLA translate generated descriptions without verifying them. To our knowledge, VSPS is the first work to measure and reduce hallucination in Vietnamese detailed captioning: it evaluates with CHAIR over a Vietnamese object lexicon, measures unsupported gender attribution for gender-marked Vietnamese person nouns, and neutralizes under-evidenced gender in the supervision data rather than editing outputs post hoc (cf. LIBRA)."
