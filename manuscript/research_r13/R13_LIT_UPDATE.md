# R13: Literature update for Paper A and Paper B (window 2025-06 to 2026-10-15)

Date: 2026-10-15. Inputs: `journal_draft/outline.md`, `journal_draft/paperB_outline.md`, `journal_draft/sec2_related_work.md`, `novel_direction/R11_00_LITMAPS_NOVELTY.md`, `research_r11/litmaps_scoopwatch_top20.bib`.

## Verification method

- **arXiv IDs:** checked on export.arxiv.org (`id_list` query: title, first author, first-version date, latest version, comment). Requests were spaced 3.5 s apart.
- **ACL Anthology:** checked on the anthology page (title, date, DOI).
- **Journal and proceedings papers:** checked on the api.crossref.org DOI record. This verifies metadata only; for HDUCap and ViG the abstract was not available, so the content is **not read**.
- **Venues:** a venue taken from an arXiv comment is marked "(arXiv comment)".
- **Sources used:** Semantic Scholar 4 calls; OpenAlex 0 calls.
- **Missing papers:** none. Every entry below resolved on its primary page. Nothing is marked [UNVERIFIED] except the venue notes listed at the end.

Relevance codes: **C** = cite; **CMP** = compare against; **T** = threat; **S** = supports.
Section references follow `outline.md` (Paper A §1–§11) and `paperB_outline.md` (Paper B §1–§10).

---

## Paper A: measurement validity of object-hallucination metrics (33 entries)

### A1. Length, count and "saying less" as a confound (closest to Contribution 1, §6)

| # | ID / venue / date | One-line finding | Rel. | Affects |
|---|---|---|---|---|
| 1 | arXiv 2609.01888 (Fazli et al.), 2026-09-01 | Re-evaluates 6 inference-time mitigation methods × 3 LVLMs × 4 benchmarks; lower hallucination usually comes with lower object recall, coverage or detail. Concludes that protocols "overestimate progress by rewarding conservative generation". | **T**/C | §1 motivation, §2 "Length and count", §6, §10 |
| 2 | arXiv 2608.24966 (Sandhu et al.), workshop (arXiv comment), 2026-08-25 | Head-targeted fix on LLaVA-1.5: CHAIR_i 0.156→0.096, but caption length 61.1→29.6 words and recall 0.78→0.70. Under fixed token budgets (64–128), SPIN and VCD do not reduce hallucination consistently. | T/CMP | §2 "Length and count", §6 (the E1 finding that gains shrink under control) |
| 3 | arXiv 2610.14976 (Nguyen et al.), IEEE Access 2026 (arXiv comment), 2026-10-10 | RL on NLP metrics: a CHAIR-only reward is hacked by naming fewer objects. Proposes an Object Consistency Score (correctness + coverage) as the reward. | C/S | §1, §2, §10 (Goodhart) |
| 4 | arXiv 2609.35294 (Long et al.), 2026-09-28 *(scoop-watch)* | On-policy RL falls into a "saying less" shortcut. The DOPA dataset annotates presence and absence densely so that valid claims can be rewarded. | T/C | §2, §4/§7 (gold completeness as the enabling condition), §9 |
| 5 | arXiv 2601.13707 (Jo et al.), CVPR 2026 Findings (arXiv comment) | Reports CHAIR at max_new_tokens 64 and 128 "to disentangle caption length". This is token-level control, not object-count control. | S | §2 (current practice), §3 (why per-image count matching is needed) |
| 6 | arXiv 2504.13169 REVERSE (Wu et al.), NeurIPS 2025 | Notes that the EOS method scores well on AMBER-G "likely because it encourages more concise captions". | S | §2, §6 |
| 7 | arXiv 2608.12746 DSCC (Bu et al.), 2026-08 | Under one protocol, decoding-time gains are "confined to short captions". With SFT on detail-rich data, more than 40% of captions still name absent objects. | CMP | §6, §7 (LVLM families) |
| 8 | arXiv 2410.13321 SumGD → **Findings of NAACL 2025** (doi 10.18653/v1/2025.findings-naacl.235) | Venue update. §2 currently cites it as "Min et al., 2024; arXiv". | C (fix) | §2 "Length and count" |
| 9 | arXiv 2609.38979 CORAL (Liu et al.), NeurIPS 2026 (arXiv comment) | FDR control of hallucinated objects at the image level using mirror statistics. A precision-type guarantee, with no count control. | CMP | §3 (contrast: precision guarantees vs count-matched comparison) |
| 10 | arXiv 2508.08285 (Janiak et al.), EMNLP 2025 (doi 10.18653/v1/2025.emnlp-main.1761) | Text LLMs: ROUGE-based hallucination evaluation is misleading, and simple response-length heuristics rival detectors. | S | §1, §2 (length confound outside captioning) |

### A2. Detailed and dense caption evaluation, precision/recall, LLM judges

| # | ID / venue / date | One-line finding | Rel. | Affects |
|---|---|---|---|---|
| 11 | arXiv 2503.12329 CapArena, Findings of ACL 2025 (2025.findings-acl.724) | 6,000+ human pairwise battles. Output length alone agrees with humans at the caption level but not at the model level; metric biases flip model rankings. | CMP/S | §8 (another human set; length vs count), §2 |
| 12 | arXiv 2502.14914 CAPability, NeurIPS 2025 D&B | Caption precision, recall and F1 per visual dimension, plus a "know but cannot tell" gap. | C/CMP | §2, §7 (P/R framing) |
| 13 | arXiv 2509.25818 VELA + LongCap-Arena, EMNLP 2025 | 7,805 images and 32,246 human judgments (Descriptiveness, Relevance, Fluency) of long captions. | S (new data) | §8 (candidate human-validity set) |
| 14 | arXiv 2412.15484 CapMAS, ICML 2025 (arXiv comment) | Dual factuality and coverage metrics for hyper-detailed captions; existing detectors fail on long captions. | C | §2 |
| 15 | arXiv 2507.19262 OVFact, 2025-07 | Reference-free open-vocabulary factuality that scores recall and precision together; agrees better with humans. | CMP | §2, §8 |
| 16 | arXiv 2604.05623 DetailVerifyBench, 2026-04 | 1,000 images, captions of 200+ words, token-level hallucination labels in 5 domains. | S (data) | §8 (possible precision-only human gold) |
| 17 | arXiv 2608.11074 CapProbe, 2026-08 | Dense, region-aligned QA (74 questions per image) for detailed caption evaluation; judge-dependent scoring. | C | §2 |
| 18 | arXiv 2509.03897 SPECS, EMNLP 2025 (doi 10.18653/v1/2025.emnlp-main.477) | Reference-free CLIP metric for long captions that rewards correct detail and penalises wrong detail. | C | §2 |
| 19 | arXiv 2606.29997 Rigel (Koyama et al.), 2026-06 | Learned caption metric with a distilled scoring head; reports more than 10 points better on ActivityNet-Fact. | C | §2 |
| 20 | arXiv 2604.11589 Philautia-Eval (Koyama et al.), 2026-04 | MLLM judges show self-preference and family-preference bias across 1.29M caption-score pairs. | S | §8, §11 (LLM-judge validity) |
| 21 | arXiv 2604.25235 (Kumar et al.), 2026-04 | Conformal intervals show that VLM judges "can rank but cannot score"; uncertainty depends on the task. | S | §8, §10 |
| 22 | arXiv 2511.04754, INLG 2025 (2025.inlg-main.22) | In captioning diversity, the choice of scorer can invert conclusions, so they argue for reporting several scorers. | S | §10 (two-column standard, specification curve) |
| 23 | arXiv 2607.23235 (Tang et al.), 2026-07 | Reconstruction-based, reference-free caption evaluation, motivated by references reflecting annotator intent. | C | §2, §5 |
| 24 | arXiv 2511.21025 CaptionQA, 2025-11 | Utility-based caption evaluation through downstream QA. | C (low) | §2 |

### A3. Gold completeness and label quality

| # | ID / venue / date | One-line finding | Rel. | Affects |
|---|---|---|---|---|
| 25 | arXiv 2609.21822 (Penquitt et al.), 2026-09 | Re-annotation adds up to +40% objects on COCO and +60% on KITTI; missing labels are the main error. Scores are sensitive to this, but rankings are "largely stable". | S/CMP | §4, §7 (an extra, more complete gold point), §2 "Gold quality" |
| 26 | arXiv 2608.30653 (Min et al.), CVPR 2026 (arXiv comment) | Multi-image object-hallucination benchmark that uses the COCO-ReM re-annotation to cut false negatives caused by missing COCO labels. | S | §2, §7 |
| 27 | arXiv 2610.08026 (Valjakka et al.), NeurIPS 2026 E&D (arXiv comment) | Automated hallucination labellers mix reference faithfulness with factual correctness and have directional error biases (text QA). | S | §1, §8 (what the gold measures) |
| 28 | arXiv 2507.19024 survey (Chen et al.), 2025-07, v2 2026-01 | Survey of multimodal hallucination evaluation benchmarks and detectors. | C | §2 |

### A4. Preference data (§9)

| # | ID / venue / date | One-line finding | Rel. | Affects |
|---|---|---|---|---|
| 29 | arXiv 2510.01700 VaPR, 2025-10 | Synthetic LVLM preference data carries "stylistic and length biases"; builds 30K hard negatives matched for length and style. | **T(low)**/S | §9 (precedent: a length channel is known, so claim only the *count* channel and the finding that length matching does not remove it) |
| 30 | arXiv 2411.10436 HDPO, 2024-11 | Rewrites over-long ShareGPT4V positives to the length of the negatives to counter length bias. | S | §9 |
| 31 | arXiv 2604.21911 (Khayatan et al.), 2026-04 | Their augmentation causes length-bias reward hacking toward very terse or very verbose output. | S | §9, §10 |
| 32 | arXiv 2507.12455 SENTINEL, v3 2026-05-22 | Audited preference set; a new arXiv version exists. Re-check that the audited release matches v3. | C (check) | §9, Tab. 6 |
| 33 | arXiv 2404.14233 HSA-DPO (v2 2025-01) and arXiv 2602.10425 HII-DPO (2026-02) | HSA-DPO: the source of an audited set. HII-DPO: shared-prefix pairs because full-length rejected responses contain correct content. | C | §9 |

---

## Paper B: Vietnamese image captioning (20 entries)

| # | ID / venue / date | One-line finding | Rel. | Affects |
|---|---|---|---|---|
| 1 | **UIT-OpenViIC, Signal Processing: Image Communication 140:117430 (2026)**, doi 10.1016/j.image.2025.117430 | Journal version of OpenViIC. Cite it instead of arXiv 2305.04166 in both papers. | C (fix) | B §1, §2, §6(d), §7; A §2 "Vietnamese captioning data" |
| 2 | **HDUCap, JVCIR 121:104963 (2026-11)**, doi 10.1016/j.jvcir.2026.104963 | New Vietnamese dataset plus a spatially-aware transformer (Crossref metadata; content not read). JVCIR is also a target venue for Paper B. | CMP/T(med) | B §2 comparator; PD-2 blocker 2 (protocol extraction) |
| 3 | **ViG, MAPR 2026 pp. 652–657**, doi 10.1109/mapr72750.2026.11685699 | Grounded adaptation of transformers for low-resource Vietnamese captioning (metadata only). | CMP | B §2, §3 comparator table |
| 4 | 30VNFoods captioning, LNNS 2025 pp. 81–87, doi 10.1007/978-3-032-05994-9_8 | Domain-specific Vietnamese food captioning. | C (low) | B §2 |
| 5 | J. Sci. Tech. HaUI 61 (2025-11), doi 10.57001/huih5804.2025.414 | Vietnamese traffic-scene captioning with a multimodal transformer. | C (low) | B §2 |
| 6 | arXiv 2602.22678 ViCLIP-OT, 2026-02 | Vietnamese CLIP trained and evaluated on UIT-OpenViIC, **KTVIC** and XM3600. It could serve as a reference-free scorer, but it is trained on KTVIC. | S/CMP | B §6 (reference-free check), §10 (leakage note) |
| 7 | arXiv 2502.06600, Findings of NAACL 2025 | Multilingual CLIPScore variants keep human correlation across languages. | S | B §2, §6 (a reference-free score is immune to the punctuation and single-writer artefacts) |
| 8 | arXiv 2409.16646, NAACL 2025 (doi 10.18653/v1/2025.naacl-long.478) | In 31 languages, Vietnamese included, languages that are closer mention more of the same entities. Who writes the description changes the content. | S | B §6(a), §7 ("two panels disagree") |
| 9 | arXiv 2604.27712 ViTextCaps, 2026-04 *(scoop-watch)* | No new version. Its claim that segmentation changes Vietnamese CIDEr still stands. | C | B §6(c) |
| 10 | arXiv 2607.02259 BamiBERT (Dat Quoc Nguyen et al.), 2026-07 | A Vietnamese encoder that works on raw text, removing the need for word segmentation. It comes from the RDRSegmenter/PhoBERT group. | S | B §3 protocol card, §6(c) segmenter discussion |
| 11 | arXiv 2508.13680 VMMU, v5 2026-09 | Vietnamese multimodal reasoning benchmark; VLMs read Vietnamese text well but still fail at reasoning. | C | B §2, §5 (choosing the B1 backbone) |
| 12 | arXiv 2509.24739, NeurIPS 2025 D&B (arXiv comment) | Vietnamese PET/CT report generation dataset; Vietnamese generation from images in the medical domain. | C | B §2 |
| 13 | arXiv 2603.15513 ViX-Ray, 2026-03 | Vietnamese chest X-ray VLM dataset. | C (low) | B §2 |
| 14 | arXiv 2510.20381 VLSP 2025 MLQA-TSR | The only multimodal VLSP 2025 shared task found; it is legal QA, not captioning. | C | B §1 (no recent Vietnamese captioning shared task was found) |
| 15 | arXiv 2601.04711 DSC2025 ViHallu, 2026-01 | Hallucination detection for Vietnamese text LLMs only; no Vietnamese visual-hallucination benchmark was found. | C | B §2, A §2 |
| 16 | arXiv 2603.09689 AutoViVQA; arXiv 2512.12424 ViInfographicVQA | Recent Vietnamese VQA resources (automatic construction; infographics). | C (low) | B §2 |
| 17 | arXiv 2602.00393, JBCS (arXiv comment), 2026-01 | Brazilian Portuguese captioning compared on native vs translated Flickr30K references. | S | B §6 (another low-resource reference-validity audit) |
| 18 | arXiv 2507.20411 CONCAP, COLM 2025 | Multilingual retrieval-augmented captioning; captions translated from English introduce linguistic bias. | C | B §2, A §7 (XM3600) |
| 19 | arXiv 2511.04754, INLG 2025 | One scorer can invert caption-level conclusions. | S | B §6(c) matcher v1/v2/v3 framing |
| 20 | arXiv 2603.10613 MUNIChus, LREC 2026 *(R11)* | No change. | C | B §2 |

---

## Scoop-watch list (20 papers from `litmaps_scoopwatch_top20.bib`)

- **arXiv versions after R11 (2026-10-14):** none of the 19 arXiv papers has a new version. Latest versions: RLAIF-V v3 (2025-10-29); THRONE v2 (2025-04); HALVA v3 (ICLR 2025); RePOPE v1; 2508.20181 v1 (BMVC 2025); 2609.35294 v1; 2604.27712 v1; KTVIC v1.
- **Journal version:** UIT-OpenViIC now has one (SPIC 2026). Update the citation.
- **LeHaCE:** Semantic Scholar shows 4 citations and no 2025+ citing paper.
- **RePOPE:** its 2025–26 citers (2608.30653, 2603.17662 FINER, 2606.06890, 2508.02645) concern VQA probing, attribution or benchmark variance. None does count or gold-completeness analysis of captions.
- **HallE-Control:** its 2025–26 citers are mitigation methods, a survey and CaptionQA. None matches per-image count matching.

## SCOOP RISK (ranked)

**HIGH (framing, not method)**
- **2609.01888, "Does Playing it Safe Count as Faithfulness?"**
  - Overlap: it makes Paper A's motivating argument (mitigation gains are partly conservative generation) on 6 methods.
  - Difference: no per-image count matching, no specification curve over controls, no CAR decomposition, no gold-indexed sign or exchangeability, no preference-data audit.
  - Action: cite it in §1 and §2, and recast Contribution 1 as "a count-matched, pre-registered quantification of a concern raised by Fazli et al. (2026) and Sandhu et al. (2026)". Do not say that the concern itself is ours.

**MEDIUM**
- **2608.24966**
  - Overlap: fixed-token-budget controls already show SPIN/VCD gains are not robust.
  - Our difference: object-count control (not tokens), 15 published pairs, Holm + SESOI.
  - Action: cite in §2 and §6.
- **2609.35294 (scoop-watch)**
  - Overlap: dense presence/absence gold is used to reward valid claims. This is the RL-side counterpart of our gold-completeness argument, but it has no sign theory.
  - Action: cite in §4 and §7 as consistent evidence.
- **2610.14976**
  - Overlap: "CHAIR is gamed by fewer objects" appears again, now in an RL reward. A method paper, not a measurement paper.
- **HDUCap (JVCIR 2026, Paper B)**
  - Overlap: a new Vietnamese benchmark and SOTA claim in Paper B's target journal. Reviewers will expect a protocol-matched comparison.
  - The paper has not been read, so whether it audits KTVIC is unknown. **Read it before 2026-11-01.**

**LOW**
- **VaPR:** reports a length bias in preference data, not a count channel.
- **CapArena:** length agrees with humans at the caption level, which supports §8.
- **2609.21822 and COCO-ReM:** incomplete gold changes scores, but these are detection and VQA settings.
- **Not found anywhere:** the gold-indexed verbosity sign flip (single crossing in k), the adjacent-doubleton exchangeability statistic, the single-writer KTVIC audit, the KTVIC punctuation CIDEr cost, the count channel in DPO data.

## NEW IDEAS (no new annotation; feasible before 2026-11-15)

1. **LongCap-Arena as a fourth human-validity test (A §8).**
   - Data: VELA's 32,246 judgments (Descriptiveness and Relevance).
   - Test: does object precision under complete gold track Relevance, and do object metrics agree with humans more on count-matched pairs?
   - Process: pre-register before the first look; check the licence first.
   - Cost: about 1 CPU-day (English matcher v2 on long captions) plus 0.5 day for the prereg.
2. **CapArena battles as a length-vs-count split (A §8).**
   - Test: compare agreement of CHAIR and F1 with the human winner on count-equal vs count-differing pairs. This is a direct replication of Tab. 5 on 6,000+ independent battles.
   - Cost: about 1 CPU-day.
3. **Extend E1 with 2025–26 methods (A §6).**
   - Methods: SPIN/VCD as re-run by 2608.24966, ACG (2601.13707), REVERSE (2504.13169).
   - Option 1: re-score their released captions at matched object count. Cost: 0.5 CPU-day if outputs are public.
   - Option 2: regenerate the 500-image CHAIR outputs from official code. Cost: about 4–8 GPU-h per method.
   - Report it as an addendum to the specification curve, not as a new confirmatory test.
4. **A "super-complete" gold point (A §7, Fig. 2).**
   - Gold: add the COCO-ReM or 2609.21822 re-annotation (+~40% objects) as gold level k = inst+.
   - Prediction: freeze it first (the slope rises further).
   - Cost: 0.5 CPU-day once the label licence is confirmed.
5. **Positive control for the preference audit (A §9).**
   - Data: VaPR (30K pairs, length- and style-matched).
   - Prediction: the count channel shrinks but is not zero.
   - Cost: about 3 CPU-h.
6. **Reference-free sensitivity check (B §6).**
   - Run multilingual CLIPScore (2502.06600) and, where available, ViCLIP-OT on P1 outputs with and without a final ".".
   - Expected: a near-zero change, which shows the −35 CIDEr cost is a property of the references.
   - Caveat: ViCLIP-OT was trained on KTVIC, so report it as sensitivity only.
   - Cost: about 1 GPU-h plus 0.5 day.
7. **Protocol-signature table for comparators (B §2, §3).**
   - Extract segmenter, CIDEr variant, punctuation handling and the ×100 convention from HDUCap (JVCIR), ViG (MAPR), the OpenViIC journal version and ViTextCaps.
   - This closes PD-2 blockers 1–2.
   - Cost: about 0.5–1 day of reading; JVCIR access goes through the TDMU library.
8. **Writing-only fixes.**
   - Cite SumGD as Findings of NAACL 2025 and OpenViIC as SPIC 2026.
   - Frame the two-column standard with 2511.04754 ("different scorers change the story") and 2604.25235 ("rank but cannot score").
   - Cost: under 1 h.

## Open items / unverifiable venue notes

- Venues marked "(arXiv comment)" are as stated by the authors on arXiv and were not checked on the venue page.
- The venues of VaPR, HSA-DPO, RLAIF-V and DOCCI-Critique (2506.07631) were not found on primary pages: [UNVERIFIED venue]; cite them as arXiv.
- Semantic Scholar lists 2507.19024 as IJCV: [UNVERIFIED venue].
- HDUCap and ViG were verified as Crossref records only; read the full text before citing any specific claim.
- The OSACT 2026 Arabic captioning paper (2026.osact-1.6) was found but its abstract could not be read. It was left out.
