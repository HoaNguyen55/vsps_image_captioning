# 02 — Evaluating detailed captions, 2024–2026 (metrics a Q2 reviewer expects)

Agent 02, 2026-10-10. Angle: evaluation of detailed and dense captions beyond CHAIR and object P/R/F1, which metrics carry over to Vietnamese, and how recall should be measured against the exhaustive gold in `../OBJECT_GOLD_PROTOCOL.md`.

Already covered elsewhere, so only *new facts* are added here: CAPTURE, DCScore/DeCapBench, CompreCap, CapArena, AMBER, ALOHa, DOCCI, CLAIR, FaithScore, PAC-S++, CapProbe, ClaimDiff-RL, RubiCap (see `../novelty/02,06,07,08,10` and `../Q2_LITERATURE.md`). For those, this file adds the exact metric definitions, which affect how VSPS should score recall.

"Opened" means I opened the arXiv abstract or HTML page (or the ACL Anthology page) on 2026-10-10.

## (a) Papers

### A. New 2025-H2 / 2026 items, not in earlier files

| # | Paper | Venue / year | Link (opened) | Method (1–2 sentences) | Relevance to VSPS | Action |
|---|---|---|---|---|---|---|
| A1 | **CAPEval: A Decoupled Caption Evaluation across Understanding and Generation.** Z. Liu, H. Wang, Z. Zhang | arXiv, Aug 2026 (no venue) | arXiv:2608.02589 | Scores each caption on two separate axes: **Coverage**, the share of human-verified atomic checklist items from a ground-truth caption that the caption covers, and **Precision**, the share of the caption's claims that are correct. Across 10 captioners, coverage predicts downstream understanding and precision predicts downstream generation. | metric/benchmark; overlap none | Cite it as 2026 support for reporting P and R separately and *not* a single scalar. This directly backs the VSPS framing "precision up, recall is the open problem". |
| A2 | **PoSh: Using Scene Graphs to Guide LLMs-as-a-Judge for Detailed Image Descriptions.** A. Ananthram, E. Stengel-Eskin, …, M. Bansal, K. McKeown | **ICLR 2026** | arXiv:2510.19060; code github.com/amith-ananthram/posh | Builds a scene graph from the reference, has an LLM judge verify each graph element against the candidate through QA, and aggregates scores that localize errors to text spans. It beats open-weight alternatives on DOCENT (+0.05 Spearman ρ) and also works on CapArena. | metric; overlap none (evaluation only) | Most likely "modern judge metric" a reviewer will name. English-only. A Vietnamese port means swapping the parser and judge. See D4. |
| A3 | **VELA: An LLM-Hybrid-as-a-Judge Approach for Evaluating Long Image Captions** + **LongCap-Arena**. K. Matsuda, Y. Wada, S. Hirano, S. Otsuki, K. Sugiura | **EMNLP 2025 main** (ACL Anthology 2025.emnlp-main.438) | arXiv:2509.25818 | A fast hybrid metric (no autoregressive judge, late visual fusion) for long captions. LongCap-Arena has 7,805 images and 32,246 human judgments on Descriptiveness, Relevance and Fluency. | metric; overlap none | Cite as the efficient alternative to a GPT-4o judge. It is not usable for Vietnamese as is. |
| A4 | **HalDec-Bench: Benchmarking Hallucination Detector in Image Captioning.** K. Saito, R. Shinoda, S. Tanaka, T. Hirasawa, F. Okura, Y. Ushiku | arXiv, Nov 2025, v4 Mar 2026 (2603.15253 is an accidental duplicate) | arXiv:2511.20515 | Human segment-level hallucination labels on captions from many VLMs, used to benchmark VLMs *as hallucination detectors*. Finding: detectors tend to accept the **first sentences** of a response as correct whether they are or not. | technique-to-borrow (verifier audit); overlap low | Check the VSPS verifier for position bias. Its propositions come from captions and are verified one at a time, which should make it immune, and showing that is cheap evidence for the 63.1% audit discussion. |
| A5 | **DetailVerifyBench: A Benchmark for Dense Hallucination Localization in Long Image Captions.** X. Wang, Y. Zhang, …, Z. Ma | arXiv, Apr 2026 | arXiv:2604.05623 | 1,000 images in 5 domains, captions over 200 words, token-level labels for several hallucination types. P/R/F1 at token and sentence level (from the search snippet; the abstract page does not list the metrics). | benchmark; overlap none | Cite as evidence that span-level hallucination localization is now standard. VSPS's span → proposition trace is the training-side counterpart. |
| A6 | **Overview of SHROOM-Visions 2026: A Shared Task on Hallucination Detection in LVLMs.** R. Vázquez, …, T. Mickus | UncertaiNLP Workshop @ **EMNLP 2026** | arXiv:2608.25662 | Multilingual span-level hallucination detection (zh, en, fr, it; **no Vietnamese**) with a 5-class taxonomy, scored by character-level correlation and IoU. The best systems reach about 0.51 IoU. | metric; overlap none | Cite in the multilingual-evaluation gap: even the 2026 multilingual shared task skips Vietnamese. |
| A7 | **OVFact: Measuring and Improving Open-Vocabulary Factuality for Long Caption Models.** M. Wysoczańska, S. Buch, A. Arnab, C. Schmid | arXiv, Jul 2025 | arXiv:2507.19262 | A reference-free metric that uses open-vocabulary grounding and tool-based verification to score descriptiveness (recall) and factual precision together. Filtering pretraining data with OVFact gives a 2.5–5× smaller set with better precision and no loss of descriptiveness. | **overlap low–medium** (C1: data filtering by factuality) + metric | Cite in the data-centric paragraph. It filters whole captions; VSPS builds targets from verified propositions. |
| A8 | **CAPability: A Comprehensive Visual Caption Benchmark for Evaluating Both Correctness and Thoroughness.** Z. Liu, C.-W. Xie, …, H. Xie | **NeurIPS 2025** (D&B) | arXiv:2502.14914; HF lntzm/CAPability | About 11K human-annotated images and videos, 12 dimensions; *precision* and *hit* (thoroughness) per dimension. Its **"know but cannot tell"** metric turns annotations into QA and counts facts the model answers correctly but omits from its caption. It argues that exhaustive annotation is infeasible and annotates one element per dimension. | metric (recall side) | (i) The "know-but-cannot-tell" gap is exactly the VSPS recall diagnosis (zero-shot R 57 vs SFT R 37). See D3. (ii) Cite as the counterpoint that VSPS's gold is exhaustive only *within a closed 101-class lexicon*. |
| A9 | **Image Captioning Evaluation in the Age of Multimodal LLMs: Challenges and Future Perspectives.** S. Sarto, M. Cornia, R. Cucchiara | **IJCAI 2025** (survey track) | arXiv:2503.14604 | A survey of caption metrics, judged on human correlation, ranking accuracy and hallucination sensitivity, including how they behave on long MLLM captions. | must-cite survey | One-line cite in the evaluation section to justify the metric choice. |
| A10 | **Object Detection Benchmarks are Incomplete: The Role of Label Errors and Annotation Uncertainty.** S. Penquitt, …, L. Schmarje | arXiv, Sep 2026 | arXiv:2609.21822 | Re-annotation adds up to **+40% objects on COCO** (+60% KITTI). The missing objects are mostly small, occluded or dense. Scores shift, but rankings stay largely stable. | supports the gold protocol | Cite in the "why an exhaustive gold" paragraph: COCO-derived CHAIR/recall golds under-count objects. Also report whether the *ranking* of systems changes between reference-gold and exhaustive-gold. |
| A11 | **How Reliable is Multilingual LLM-as-a-Judge?** X. Fu, W. Liu | **Findings EMNLP 2025** (2025.findings-emnlp.587) | ACL Anthology page | Covers 25 languages. Cross-language judge consistency is low (Fleiss κ ≈ 0.3) and worst for low-resource languages; scale and multilingual training do not fix it. | caveat for any Vietnamese judge | Cite whenever VSPS uses a VLM/LLM judge on Vietnamese text, and pair the judge with human agreement on a subset. |
| A12 | **Evaluation of Multilingual Image Captioning: How far can we get with CLIP models?** G. Gomes, C. Zerva, B. Martins | **Findings NAACL 2025** | arXiv:2502.06600 | Multilingual CLIPScore variants, including one fine-tuned on human judgments, evaluated on 9 languages. The abstract does not say whether Vietnamese is included. | metric (cheap reference-free) | Optional. A multilingual CLIP-S is weak on detail and hallucination, so cite only to explain why VSPS does not use it as the main metric. |
| A13 | **AuroraCap / VDC benchmark** (VDCscore). W. Chai, E. Song, Y. Du, C. Meng, V. Madhavan et al. | **ICLR 2025** | arXiv:2410.03051 | Video detailed captions. VDCscore splits a long caption into short QA pairs answered by an LLM. | metric (video) | Low relevance; cite only if the related work enumerates QA-based coverage metrics. |

### B. Already-known items: exact definitions that matter for VSPS (opened today)

- **DCScore / DeCapBench** (Q. Ye, X. Zeng, F. Li, C. Li, H. Fan; ICLR 2025; arXiv:2503.07906, HTML read). GPT-4o splits the caption into primitive units P. Human experts split the ImageInWords reference into units O, with **400 images**. Q = P∩O is the set matched by an LLM. Precision is s_p = |P_true|/|P|, where P_true are the units GPT-4o verifies against the image. **Recall is s_r = (|Q| + |P_true∖Q|) / (|O| + |P_true∖Q|)**, so a correct unit that is *missing from the reference* is added to both numerator and denominator rather than ignored. The final score averages F1 over all units and F1 over descriptive units. **This is the standard answer to "references are incomplete", and VSPS can reuse it exactly (D2).**
- **AMBER** (J. Wang et al., arXiv:2311.07397, HTML read; no venue found). There are 1,004 images annotated for "all visible objects" by several annotator groups, plus a list of *hallucinatory target objects* (absent but likely to be imagined). The metrics are CHAIR = 1 − |R∩A|/|R|, **Cover = |R∩A|/|A|**, Hal = 1[CHAIR > 0], and **Cog = |R∩H|/|R|**. The VSPS exhaustive gold *is* an AMBER-style A set for Vietnamese. AMBER's Cover is the published name for "recall against exhaustive gold", so use that name and cite it.
- **CompreCap** (F. Lu et al., CVPR 2025, arXiv:2412.08614). Images are manually segmented into semantic regions over a common-object vocabulary, then a directed scene graph is built and object coverage, attribute accuracy and relation scores are computed. The abstract does not say whether coverage is area-weighted (not verified).
- **CAPTURE** (H. Dong et al., arXiv:2405.19092, v4 Jul 2024, still no venue). Extracts objects, attributes and relations, matches them in three stages, and reports the highest expert consistency. The parser is English-only.
- **CapArena** (K. Cheng et al., Findings ACL 2025, DOI 10.18653/v1/2025.findings-acl.724). Built from 6,000+ pairwise human battles. A VLM-as-judge is the only automatic metric that ranks models like humans do. METEOR agrees at caption level but has systematic ranking bias. CapArena-Auto is reported as 94.3% (arXiv) or 93.4% (ACL version) correlation at about $4 per test. **If CapArena is cited, quote the ACL number.**

### Unverified (not opened; do not cite without checking)

- PolyVis, a 12-language multimodal LLM-as-judge benchmark that includes hallucination (OpenReview PDF seen only in search; title, authors and venue not confirmed).
- Hada et al. 2024, which found LLM-evaluator agreement lower for non-English (only seen as a citation inside a search summary).
- ReconScore (arXiv:2604.22855), a reference-free remote-sensing caption metric (search snippet only).
- SPECS (EMNLP 2025), a CLIP-based long-caption metric (Underline lecture page only).

## (b) Overlap risks (max 5)

1. **OVFact (A7): low–medium.** It filters training captions with a precision/recall factuality score, which is a data-centric anti-hallucination method. The difference is that it keeps or drops whole captions, while VSPS builds targets from three-state verified propositions, neutralizes rather than drops, and traces every span. One sentence in related work is enough.
2. **CAPability "know but cannot tell" (A8): low.** If VSPS claims "the SFT model knows objects it does not say", reviewers will expect this metric's name. Cite it and do not present the phenomenon as new.
3. **AMBER Cover (B): low, naming only.** Do not present "recall against an exhaustively annotated gold" as a new metric. Present it as AMBER's Cover carried over to Vietnamese with a native lexicon. What is new is the Vietnamese lexicon, the hypernym-lenient matching and the gender-specific classes.
4. **DCScore recall (B): low, naming only.** If D2 is adopted, call it "DCScore-style recall correction" and cite it.
5. No HIGH overlap was found in this angle. All evaluation papers score outputs; none builds supervision.

## (c) Must-compare / must-cite (max 5)

1. **AMBER (Cover, CHAIR, Hal, Cog).** Report all four on the 300-image exhaustive gold: *Cover* as the recall headline, *Hal* as the share of captions with ≥1 hallucination, which is easier to read than CHAIR_s, and *Cog* if D5 is done.
2. **DCScore / DeCapBench.** Cite it as the closest proposition-level metric. Report a DCScore-style P/R (D2, D4) at least on the COCO-vi side.
3. **CapArena + PoSh (ICLR 2026).** These represent the judge-based metrics. Run one pairwise VLM-judge comparison (VSPS vs zero-shot vs DPO) with a human-agreement subset (D4). Without it, a 2026 reviewer will say "only lexicon metrics".
4. **CAPEval (2026) + CAPability (NeurIPS 2025).** Cite both for the decoupled precision/coverage reporting and the "know but cannot tell" gap.
5. **Fu & Liu, Findings EMNLP 2025, + SHROOM-Visions 2026.** Use these to justify *why* the main metrics are lexicon- and human-gold-based: LLM judges are unreliable in low-resource languages, and no multilingual hallucination benchmark covers Vietnamese.

## (d) Actionable improvements for VSPS (ranked by gain/cost)

These are all evaluation changes, with no retraining. They change what the recall number *means*, which is the reviewer-facing problem at R = 37.1.

**D1. Report AMBER-style Cover/Hal plus salient vs exhaustive recall on the object gold.** Cost: 0 GPU, about 1 hour.
- What: in `scripts/object_gold_score.py`, add, per system, (i) `Hal` (share of images with ≥1 mention outside gold) and (ii) **R_salient**, which is recall over gold classes that ≥2 of the 5 KTVIC references also mention (reuse `rescap/chair.py:objects_in` on the references), next to the existing R_exhaustive. Run `scripts/score_ci.py`-style paired bootstrap on the per-image recall vector.
- Effect: the gap between the two recalls separates "omits salient objects" (a model problem) from "does not list background" (a style choice). ClaimDiff-RL and CompreCap make the same salient/complete split. It is likely to show that VSPS recall on salient objects is much closer to zero-shot than the 37 vs 57 KTVIC numbers suggest, or else make the deficit undeniable. Either way the claim gets sharper.
- Risk: the salience threshold is arbitrary, so report ≥1, ≥2 and ≥3.

**D2. DCScore-style recall correction for the KTVIC-reference recall (558 images, full test set).** Cost: 0 GPU for the lexicon version.
- What: in `scripts/object_prf.py`, for each image, add to both numerator and denominator the predicted objects that are not in the references but **are** in the exhaustive gold (on the 300 overlap images) or are SUPPORTED by the existing Vintern verifier (`rescap/pipeline/verify.py`, existence query, about 1–2 s per object on the 3090) on the rest. This is s_r = (|Q| + |P_true∖Q|)/(|O| + |P_true∖Q|).
- Effect: this removes the reference-incompleteness penalty that caps human ref #1 at R 46.9. It rewards correct extra objects, which helps zero-shot and VSPS alike, so the comparison stays fair. Expect recall to rise for all systems.
- Risk: the verifier's precision is about 63% on SUPPORTED, so use the gold-only version on the 300 images as primary and the verifier version as supplementary.

**D3. "Know but cannot tell" probe for the SFT model (CAPability).** Cost: about 1 GPU-hour.
- What: for every exhaustive-gold class that the VSPS caption omits, ask the *same* fine-tuned Qwen2.5-VL-7B the yes/no existence question in Vietnamese, using the dual affirmative + negated template in `rescap/pipeline/verify.py`. Report KCT = P(model answers "yes" correctly | omitted). About 300 images × about 5 omitted classes = 1,500 short queries, under 1 h with 4-bit inference.
- Effect: if KCT is high, the recall loss is a *verbalization/budget* effect (the 9-proposition selection and template rendering) and not a perception loss. That points straight at the fix: raise the budget or add a list-style "also visible:" span from SUPPORTED entity propositions. It is the strongest diagnostic for the recall ≥ 55 target.
- Risk: yes-bias inflates KCT, so use the dual query and count acquiescence ("yes to both") as not-known.

**D4. One judge-based metric with a human check (CapArena-style pairwise, PoSh-style checklist).** Cost: about 2–4 GPU-hours with a local judge, or about $5–20 of API.
- What: add `scripts/judge_pairwise.py`. On 200 KTVIC images, show a judge the image and two captions in randomized order, run both orders, and ask which has fewer errors and which covers more (two questions, so P and R stay decoupled as in CAPEval). Use Qwen2.5-VL-72B-AWQ only if it fits; on a 3090 that is not realistic, so use a **different-family** judge (InternVL3-8B or Gemini/GPT-4o via API) to avoid self-preference with the Qwen backbone. Then have one human label 50 pairs and report the judge–human Cohen κ with `scripts/agreement.py`.
- Effect: closes the "no modern metric" review comment. Fu & Liu (A11) say it must carry a human κ for Vietnamese, which this design includes.
- Risk: a low κ in Vietnamese. If so, report it as a finding and keep the lexicon metrics primary.

**D5. Add a Cog-style "hallucinatory target" check.** Cost: 0 GPU, about 2 hours.
- What: from the KTVIC training captions, mine the top co-occurring lexicon classes for each gold set, such as `xe máy` → `mũ bảo hiểm` and `bàn` → `ghế`. For each test image, H = high-co-occurrence classes that are *absent* from the exhaustive gold. Report Cog = |mentions ∩ H| / |mentions| in `object_gold_score.py`.
- Effect: shows *why* VSPS lowers CHAIR, namely by cutting co-occurrence-prior hallucinations (the mechanism LURE and HalluciDoctor describe), with a published metric name.
- Risk: H is automatic and not hand-annotated as in AMBER, so state that.

**D6. Gender attribution against the human gold, not the references.** Cost: 0 GPU.
- What: the protocol already makes annotators tick the most specific person class (`phụ nữ`, `đàn ông`, `trẻ em` vs `người`). In `object_gold_score.py`, report unsupported gender = gendered person mentions whose class is not in the gold and whose gold has only `người` or the opposite gender.
- Effect: turns the gender claim from "unsupported by references" into "unsupported by the image according to 2 annotators + adjudication". A reviewer cannot dismiss that version as reference sparsity.
- Risk: none, beyond a small n of gendered images; report counts and a CI.

**Measurement bug to fix before reporting (found while reading `object_gold_score.py:score`).** In `lenient` mode, one vague mention covers *every* gold class beneath it: the caption "người" covers `phụ nữ`, `đàn ông` and `trẻ em` at once (`covered = {y for y in g if y in m or ANCESTORS[y] & m}`). That inflates lenient recall for vague captions, which is exactly what neutralization produces, so it favors VSPS in a way a reviewer could attack. Fix: let each vague mention cover at most one gold descendant, or report `lenient` recall with vague coverage credited 0.5 or at most once, and always show `exact` beside it.

## (e) Watch queries (re-run monthly)

1. arXiv listing cs.CV + cs.CL, full-text search: `"detailed caption" AND (evaluation OR metric OR benchmark) AND (coverage OR recall OR omission)`, sorted by date. Source: arxiv.org/a search with the "submitted date" filter.
2. Semantic Scholar alerts on citations of DCScore (arXiv:2503.07906), CapArena (2503.12329), PoSh (2510.19060) and CAPEval (2608.02589). Any new metric for detailed captions will cite at least one of them.
3. Google Scholar alert: `"image caption" hallucination (Vietnamese OR multilingual OR "low-resource") evaluation`.
4. OpenAlex API: `search=caption hallucination benchmark&filter=from_publication_date:2026-01-01,type:article` for the journal versions (IJCV, TPAMI, PR, TALLIP).
5. arXiv: `"LLM-as-a-judge" AND (multilingual OR Vietnamese) AND (image OR vision OR caption)`, to track whether a Vietnamese judge-reliability paper appears, which would change D4.
6. ACL Anthology search for SHROOM-Visions follow-ups and the UncertaiNLP 2027 CFP, in case Vietnamese is added as a language.
