# Paper A review: Reviewer R2 (methods and statistics)

All judgements are AI opinion (a generated reviewer, not a human referee). Copied verbatim in substance from the review panel output of 2026-10-29.

**Scores (1-5):** novelty 3, correctness 3, contribution 3, clarity 2.5. **Recommendation:** major revision. **Confidence:** 4/5.

## Summary

This is a carefully registered measurement audit. Every PASCAL-50S number in the manuscript matches the decide files (p50_decide.json, sha 0da4cab9; p50x_decide.json, sha 75e152d2). The registration commit (353437f, 00:49:49Z) came before the run start (00:51:22Z). The P50-A4 FAIL is reported in Section 7.4 with the prereg's branch text 9.2, and it also appears in Table 1, Section 9.1 and the conclusion.

Several problems remain:

- The limitations section still says the PASCAL-50S test was "registered, not run" (sec11:9) and that the ordering "passed on both backbones" (sec11:21).
- Two departures from the registration are not disclosed:
  - PREREG §6 says the caption-file hashes must leave the machine, but they were never exported.
  - The reference file's structure was checked on a laptop before the commit.
- Part 2 of P50-A4 assumes the VOC labels are more complete than the 50-reference gold on the 20 VOC classes, and that premise is never shown.
- System-level uncertainty on PASCAL is not discussed. The slope is fitted over 14 runs that form short and detailed clusters, and the per-model slopes vary widely.
- Feng et al. (2024, arXiv 2406.12663), a directly relevant prior critique of object-hallucination metrics, is not cited.

X4 in the abstract is acceptable as a PASS headline, with three changes:

- label it consistently ("companion" or "co-primary", not "secondary");
- drop the "Holm-corrected" wording, since Holm over one test adjusts nothing;
- report p ≤ 0.001.

## Major issues

**M1. Stale and contradictory statement about the PASCAL-50S test.**

- sec11_limitations_ethics.md:9 says "the large-reference-set test is registered, not run (Section 7.4)". Section 7.4 reports a scored test with a FAIL verdict (p50_decide.json, status SCORED).
- Requested change: replace the sentence with one saying that the test was scored once, that its primary compound P50-A4 FAILED at the label step (−2.29 [−5.15, +0.61]), and that its secondary P50-O2 PASSED.

**M2. The ordering claim is overstated in the limitations and in the contributions.**

- sec11_limitations_ethics.md:21 says "the claim rests on the ordering, which passed on both backbones".
- sec11:23 (external validity) never mentions that the ordering failed on the English PASCAL-50S family of seven LVLMs.
- sec1_introduction.md:27 (contribution 1) lists only the PASCAL-50S O2 PASS.
- Requested change:
  - add to sec11:21/23 that the registered out-of-sample ordering did not replicate on PASCAL-50S at the label step;
  - rewrite contribution 1 so that it states that the registered primary PASCAL-50S ordering (P50-A4) failed, with the O2 PASS given as secondary.

**M3. An undisclosed departure from the registration, and outputs that cannot be audited.**

- PREREG 2026-10-28_pascal50s/PREREG.md §6 (l.336) says that for a decode file with at least one 8-gram hit, "Only its sha256 and the aggregates leave".
- The committed job (scripts/pascal50s/p50_job.sh:167-169) copies the .sha256 only when rc = 0.
- All 14 files had hits: EVENTS at 05:54Z, and between 18 and 419 hits per file in data/results/p50/ngram_p50_*.preds.json. No output hash therefore exists.
- sec11_limitations_ethics.md:34 and supplementary.md:637 state "no hash of them was kept" as a plain fact, not as a departure.
- Requested change:
  - label this a departure from PREREG §6, in Section 7.4 and in the S4 deviation list;
  - report the per-file 8-gram hit counts, which are aggregate counts already in the repository;
  - explain what the counts mean for pretraining exposure: generic 8-grams versus possible memorisation of PASCAL captions. The short captions of LLaVA-1.5 and SmolVLM2 have 353 and 419 hits.

**M4. Undisclosed pre-commit structure check.**

- PREREG §0 l.35 and RULE §0 record that pascal50S.json was fetched and refchecked on a laptop before the §11 commit.
- The check printed counts only, but the companion rules were written knowing that every image has 50 references.
- This departs from PREREG §6 ("on M3 only") and §11 ("before any data step").
- The manuscript never mentions it: a grep for "refcheck" or "laptop" in sec7 and the supplement finds nothing.
- Requested change: add one sentence to Section 7.4 or S4 disclosing it as an accepted deviation, with no change of verdict.

**M5. The completeness premise behind P50-A4 part 2 is not shown.**

- The registered ordering assumes that the VOC labels (voc20) are a more complete gold than refs50∩V20 on the 20 VOC classes.
- The numbers point the other way: on V20 the 50-reference slope (+9.74 [+7.29, +12.12]) is already above the label slope (+7.45 [+4.98, +9.94]) (supplementary.md, Table S7.P1).
- The only stored size aggregate is X5's Σ|voc20| = 1,782 classes over 997 images, about 1.8 per image (p50x_decide.json, X5).
- sec7_verbosity_sign.md:99 offers only the "person"-dominance and "aeroplane" explanations, and says neither was tested.
- Requested change:
  - if a stored aggregate gives Σ|refs50∩V20|, Σ|voc20| and the two set differences on the analysis set, report them; if not, say they were not retained;
  - in either case, add without a verdict that the FAIL may mean the label rung is not more complete than a 50-reference gold on a 20-class vocabulary, which limits what the FAIL says about the ordering claim;
  - do not re-score anything.

**M6. Uncertainty about systems and design is not stated for PASCAL-50S.**

- The intervals come from an image bootstrap over a fixed set of 14 runs.
- The V20 mention counts M form two clusters: short around 1.12-1.35 and detailed around 1.6-2.24 (p50_decide.json, analysis_set.M).
- PREREG §10 risk 2 says Qwen3-VL detailed captions hit the 160-token cap.
- The per-model contrasts vary widely. The voc20|V20 slope runs from −1.05 to +14.75 and is negative for both LLaVA models (PAIR_m).
- The leave-one-system-out jackknife of Section 7.5 was not extended to PASCAL-50S. It now cannot be, because only M per run was retained and the outputs were deleted.
- Requested change: in sec7_verbosity_sign.md:88-99, state that:
  - the slope is essentially a short-versus-detailed contrast across seven models;
  - cap hits apply;
  - the per-model spread is as above;
  - no system-level interval exists for PASCAL-50S.

  Repeat this in sec11:21.

**M7. X4 in the abstract. In my AI opinion it is acceptable as a PASS headline, but it needs these edits.**

- (a) The label is inconsistent. RULE.md §3.2 calls X4 "co-primary" within the companion family, while abstract_A.md:9, sec1_introduction.md:69 and sec7:131 call it "secondary". Use "a registered companion test" everywhere, or explain both labels once.
- (b) "PASS (Holm, X4 alone)" (sec1:69) and "Holm over the companion family" (sec7:136,139) imply a correction that does nothing for a single test once X5 is NOT_EVALUABLE. Say that no multiplicity adjustment applied, and cite the descriptive family-wise Holm reading (supplementary.md:633) as the meaningful one.
- (c) p = 0.001 is the floor 1/(R+1) of the 1,000-replicate null. Report it as p ≤ 0.001. Also say that the null holds the images and runs fixed, so the p-value describes gold randomisation, not sampling of images or systems.
- (d) X4 was a low-risk test: its direction was set by 8/8 exploratory cells and 4/4 dev cells at p = 0.001 (RULE §3.2 and §9). Say so briefly.

**M8. The abstract signals the A4 FAIL too weakly relative to the secondary PASS. In my AI opinion it is borderline adequate.**

- abstract_A.md:9 reports the O2 PASS as "(registered)" and gives X4 a full sentence.
- The primary PASCAL-50S verdict appears only later, in a list, as "the label-gold part of the PASCAL-50S replication".
- A PASS headline is permitted, but the FAIL should be identifiable as the primary verdict.
- Requested change, in 12 words or fewer: "the registered primary PASCAL-50S ordering failed at its label step (50 references vs VOC labels)", with O2 marked as secondary.
- Scope the opening claim "more complete gold raises the verbosity reward" to "on XM3600 and its second backbone", because label gold lowered the slope on PASCAL-50S.

**M9. A directly relevant prior critique is missing from the related work.**

- Feng, Tang, Zhang and Xu (2024), "Do More Details Always Introduce More Hallucinations in LVLM-based Image Captioning?" (arXiv 2406.12663, checked on export.arxiv.org), argue that existing object-hallucination metrics have technical flaws that distort the more-details/more-hallucination conclusion. They propose CLIP-Precision, CLIP-Recall and CLIP-F1.
- The authors' own RULE.md §8 lists this paper, but it appears neither in sec2_related_work.md nor in paperA.bib.
- Requested change:
  - cite it in sec2_related_work.md:10 or :12, and add it to Table 2.1;
  - explain how a registered slope audit that treats the gold as a factor differs from replacing the metric;
  - also position the paper against the finding of Vedantam et al. (2015) that agreement with humans grows with the number of references. At present that paper is cited only as a data source.

## Minor issues

- **m1.** sec7_verbosity_sign.md:139 reads "On 1,000 PASCAL-50S images". The analysis set is 997 images (p50_decide.json, n_images). Change it to "997 of 1,000".
- **m2.** "Rise at every added reference" (abstract_A.md:9, sec1:9, sec1:27, sec7:94) overstates the grid. The rungs were k = 1, 2, 5, 10, 20, 50, so write "at every registered rung (k = 1, 2, 5, 10, 20, 50)".
- **m3.** sec3_measurement_setup.md:9 says "Analyses that vary k use at most the first five references". This contradicts PASCAL-50S, which uses k up to 50 with random draws (default_rng(1), r = 20). Add the PASCAL-50S exception.
- **m4.** Title and abstract terminology. With reference gold the slopes are mostly negative: on COCO-80 the slope is −31.38 at one reference and still −0.83 [−2.58, +1.07] at 50 references. "Larger verbosity reward" therefore often means "smaller verbosity penalty". Define "reward" once in the abstract as the signed slope, or use "verbosity slope" in the title.
- **m5.** supplementary.md:620-631 (PAIR_m table): the column "50 refs, COCO-80" sits beside "VOC labels, V20", which invites a cross-vocabulary comparison. Add a note that the two columns use different vocabularies, so their difference is not the A4 part-2 contrast, and that each entry is a two-run contrast.
- **m6.** Linking X4 to Section 4. sec4_theory.md:25 states that the nested-reference ordering is expected even under SCAR (missing completely at random), so O2 cannot distinguish the propensity model from random missingness. X4's size-matched null is exactly a SCAR null, which makes X4 the only registered test here that probes the b-channel. Say this in sec7:139 and sec10_discussion.md:7. It strengthens the contribution and explains why O2 is a low-risk prediction.
- **m7.** sec7_verbosity_sign.md:92 does well to give both the three-level rule and the original point criterion. Also give the family-wise one-sided p for P50-A4 (0.939, supplementary.md:633) in the main text, so that readers see the FAIL is not close.
- **m8.** The abstract paragraph is 244 words by wc -w, above the ≤240 target in its own header comment (abstract_A.md:3). Trim it, for example by shortening the X4 sentence as in M7.
- **m9.** Multiplicity across Table 1. About 35 registered rows carry uncorrected intervals (sec3_measurement_setup.md:47, sec11:21). Next to "Nine registered predictions failed" (sec1:9), report the expected number of false PASSes under the global null, or a family-wise reading of the confirmatory rows.
- **m10.** Section numbering differs from the file names: sec10_discussion.md is "# 9", and sec11_limitations_ethics.md is "# 10". sec9_preference_audit.md and appB_matcher_sensitivity.md are empty stubs. Remove the stubs from the submission package, and check every "Section N" cross-reference against the final numbering.
- **m11.** Internal IDs (CC-xxx, PI-xxx, W-numbers, A24a-d, P50-NS) appear in reader-facing tables and text, for example sec1 Table 1 and supplementary.md:603-637. Keep the registration IDs and move the governance IDs to the provenance file.
- **m12.** sec7_verbosity_sign.md:97 says the PASCAL images "may be in the pretraining data". Support this with the 8-gram hit counts (M3). Avoid implying that the 8-gram check is a contamination test, since PREREG §6 states "A hit is not a verdict input".
- **m13.** sec7_verbosity_sign.md:135 (X5) rightly gives no X5 observed or null value as evidence. Keep it that way, and say once that X5's observed value was printed but carries no result.

## Full report

Referee report: methods and statistics. Manuscript: "More References, Larger Verbosity Reward: A Registered Audit of Object Hallucination Metrics Under Incomplete Gold". Submitted to Signal Processing: Image Communication. All judgements below are AI opinion.

### 1. Summary of the submission

The paper treats the gold set as the experimental factor in object-level hallucination scores. It measures the OLS slope of object F1 on ln M (M = mentioned objects per image) across a family of systems, under golds of increasing completeness: k references, all references, and instance or verified labels.

The confirmatory claim is that this slope is ordered by gold completeness. It rests on:

- a registered XM3600 test (600 images, six Qwen2.5-VL systems);
- a registered second-backbone test (Qwen3-VL-8B, 537 of the same images).

A newly registered PASCAL-50S study (1,000 images, 50 references each, VOC2008 labels on 20 classes, seven public LVLMs, 14 runs) adds four results:

- P50-A4 (primary): FAIL. The 1-reference vs 50-reference part PASSES at +37.16 [+35.07, +39.09]; the 50-reference vs VOC-label part FAILS at −2.29 [−5.15, +0.61].
- P50-O2 (secondary): PASS at all five steps.
- X4 (companion, size-matched random-deletion null): PASS at both levels, p ≤ 0.001.
- X5: NOT_EVALUABLE.

The paper also includes post hoc count-matched re-scoring of 15 published comparisons, registered human-judgment tests, and a preference-data audit.

### 2. Verification performed

- I checked every PASCAL-50S number in sec7_verbosity_sign.md:88-139 and supplementary.md:603-637 against data/results/p50/p50_decide.json (sha 0da4cab9) and p50x_decide.json (sha 75e152d2). The items checked were:
  - the A4 parts and the O2 steps;
  - Table S7.P1 and PAIR_m;
  - the X1/X2 statistics;
  - the X4 observed values, null ranges and excesses;
  - the X5 condition (1,782 < 2 × 1,039.6);
  - the family-wise Holm p-values;
  - the all-image sensitivity analysis;
  - the GPU plan.

  All match to the reported precision.
- The registration commit 353437f (00:49:49Z) came before the job start (00:51:22Z, EVENTS), as Section 7.4 states.
- The verdict rules in PREREG §3.5-3.6 and RULE §3-5 were applied as written. A4 part 2 is FAIL because its point estimate is ≤ 0, and Section 7.4 correctly notes that the interval includes 0. Section 7.4 uses PREREG branch text 9.2 verbatim.
- The data-availability sentence required by PREREG §1.4 is present in declarations.md:19.
- The numbers manifest has P50 rows.
- Related-work searches: OpenAlex and Semantic Scholar returned HTTP 429 (rate limited), while the arXiv API and Crossref worked. They surfaced Feng et al. (2024, arXiv 2406.12663) and RePOPE (2504.15707). RePOPE is cited; Feng et al. is not (M9).
- I found no "first" claims in the abstract, highlights, Section 1, Section 2 or the cover letter.

### 3. Assessment by criterion (scores 1-5)

**NOVELTY: 3/5.**

- Strengths:
  - Treating gold completeness as a controlled factor, and registering the sign and order of a verbosity slope, is a distinctive framing.
  - The size-matched random-deletion null (X4) is a useful design element.
- Limits:
  - That incomplete or caption-derived gold inflates hallucination scores is known (Rohrbach et al., 2018, which the paper acknowledges at sec7:141).
  - That relabelling changes rankings is known from ImageNet ReaL and RePOPE.
  - Incomplete judgments are known in IR (Buckley and Voorhees; Zobel; Sakai).
  - Feng et al. (2024) argue directly that object-hallucination metrics are flawed for the more-details question, and they are not cited.

The novelty therefore lies in the registered, quantified characterisation at the level of sign, not in the phenomenon. The paper should say so.

**CORRECTNESS: 3/5.**

- Strengths:
  - The numbers are traceable and correct.
  - The registered rules were followed.
  - Failures appear in Table 1.
- Problems:
  - The limitations section is out of date (M1) and overstates the claim (M2).
  - Two departures from the registration are not disclosed: the hit-file hashes were not exported (M3), and the reference file was checked on a laptop before the commit (M4).
  - The A4 part-2 test depends on a completeness premise that is never shown (M5). The V20 numbers (+9.74 with 50 references vs +7.45 with labels) suggest that a 50-reference gold may already match or exceed the completeness of the VOC labels on 20 classes. That reading would change what the FAIL means without changing the verdict.
  - The uncertainty is image-only, over 14 runs that fall into short and detailed clusters, with large per-model heterogeneity and no system-level robustness check (M6).
  - X4's p-value is the 1/(R+1) floor, and it is conditional on fixed images and runs (M7c).

**CONTRIBUTION: 3/5.**

- For SPIC readers the practical messages are sound: name the gold and the matcher, report M, and do not compare F1 across verbosity regimes under incomplete gold.
- The PASCAL-50S evidence adds a monotone rise in the reference ladder up to 50 references and a mechanism result against a size-matched null.
- The monotone rise is close to expected under nested golds, as the authors themselves say at sec4:25.
- X4 is the more informative test because it probes non-SCAR missingness, and the paper underuses it (m6).
- The confirmatory scope is now narrow: XM3600 with two Qwen backbones, after the out-of-sample replication failed at the label step. The paper should state this plainly.

**CLARITY: 2.5/5.**

- The registration ledger and the source comments are exemplary for auditability.
- The reader-facing text is dense:
  - it carries internal governance IDs (m11);
  - it uses "reward" for mostly negative slopes (m4);
  - it has numbering mismatches and empty stubs (m10).
- The abstract treats the primary PASCAL-50S FAIL as a list item, while the secondary PASS and X4 get full sentences (M8).

### 4. Answers to the two specific questions (AI opinion)

**(a) Is X4 in the abstract acceptable?** Yes. It is a registered PASS, it addresses the mechanism that Section 4 says the ordering alone cannot test, and the binding rules allow a PASS headline. Required fixes:

- consistent labelling ("companion", not "secondary", given that RULE §3.2 says "co-primary");
- no "Holm-corrected" wording for a family with one member;
- p ≤ 0.001, conditional on images and runs;
- a brief note that the direction was fixed by 8/8 exploratory cells and 4/4 dev cells.

**(b) Is the A4 FAIL reported adequately?**

- Yes in Section 7.4 (verbatim branch text), Table 1 (row A24 with both parts), Section 9.1 and the conclusion.
- No in the limitations section (M1, M2) and in contribution 1 (M2).
- Borderline in the abstract (M8). Under the binding rule ("reported briefly, never hidden") the abstract passes only narrowly. A 12-word fix naming it as the primary verdict would remove any doubt.

### 5. Major issues

M1-M9, as listed above. Each comes with file:line pointers and a requested change.

### 6. Minor issues

m1-m13, as listed above.

### 7. Constraints respected in the requested changes

- No requested change needs new human labels, AI-generated labels, a second look at any test set, a re-score, a GPU run or a commit.
- M5 and M6 ask only for stored aggregates, or for a statement that they were not retained.
- M3 asks only for hit counts already in the repository; no caption text is involved.

### 8. Recommendation

Major revision. The science at the level of verdicts is sound and honestly ledgered. Most required changes are disclosures and framing edits, plus one missing citation. M3-M6, however, concern the correctness of the interpretation and must be resolved before acceptance.

### Relevant files

- /mnt/d/vsps_image_captioning/manuscript/journal_draft/abstract_A.md
- /mnt/d/vsps_image_captioning/manuscript/journal_draft/sec1_introduction.md
- /mnt/d/vsps_image_captioning/manuscript/journal_draft/sec7_verbosity_sign.md
- /mnt/d/vsps_image_captioning/manuscript/journal_draft/sec11_limitations_ethics.md
- /mnt/d/vsps_image_captioning/manuscript/journal_draft/supplementary.md
- /mnt/d/vsps_image_captioning/data/results/p50/p50_decide.json
- /mnt/d/vsps_image_captioning/data/results/p50/p50x_decide.json
- /mnt/d/vsps_image_captioning/manuscript/prereg/2026-10-28_pascal50s/PREREG.md
- /mnt/d/vsps_image_captioning/manuscript/prereg/2026-10-29_a_companion/RULE.md
- /mnt/d/vsps_image_captioning/scripts/pascal50s/p50_job.sh
