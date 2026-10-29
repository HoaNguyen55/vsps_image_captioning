# Paper A review: Reviewer R4 (handling editor)

All judgements are AI opinion, written by an AI reviewer for the authors' internal revision; this is not a report from a human referee. The content follows the review panel output of 2026-10-29 in substance.

**Scores (1-5):** novelty 3, correctness 4, contribution 3, clarity 2. **Recommendation:** major revision. **Confidence:** 4/5.

## Summary

Handling-editor review of Paper A for Signal Processing: Image Communication: "More References, Larger Verbosity Reward: A Registered Audit of Object Hallucination Metrics Under Incomplete Gold".

The paper treats the gold set as an experimental factor and asks how the verbosity reward of object F1 (its slope on ln M) depends on how complete the gold is. It reports a registration ledger of more than 30 predictions, failures included.

All PASCAL-50S numbers in the abstract, Section 7.4, Section 7.6, Table 1 and Supplementary S7 match two decide files:

- `data/results/p50/p50_decide.json` (sha256 0da4cab90fe9…, checked with sha256sum);
- `p50x_decide.json` (75e152d266a4…).

This includes the sensitivity values over all 1,000 images. The registrations were committed at 00:49Z, before the first output at 00:51Z.

Main problems:

1. A stale sentence in Limitations still says the PASCAL test was "registered, not run", which contradicts the reported A4 FAIL.
2. An `[AUTHOR TO CONFIRM]` placeholder appears in the visible text.
3. The abstract's PASCAL sentence reads as a successful replication. The failure of the primary prediction (P50-A4) appears only in a later list of failures.
4. Feng et al. 2024 (arXiv 2406.12663) is missing from the related work, although the authors' own companion RULE names it as prior art.
5. Only 997 of the 1,000 images were analysed, and the p-value sits at the floor of the 1,000-replicate null. Neither is worded correctly.
6. The PASCAL results cannot be audited per image and have no system-level robustness check.
7. Fit with the journal, and the reading burden.

On the two questions asked:

- X4 may stay in the abstract if it is labelled correctly. It is the only registered test that can tell salience-driven missingness from random missingness.
- The A4 FAIL is reported adequately in the body (§7.4, Table 1 A24, §9.1, §9.5, cover letter). It is not reported adequately in its abstract placement, in the highlights, or in Limitations §10.1.

## Major issues

### M1. The A4 FAIL is contradicted in Limitations

`manuscript/journal_draft/sec11_limitations_ethics.md:9` says: "the large-reference-set test is registered, not run (Section 7.4)". The test was run on 2026-10-29 (`data/results/p50/EVENTS`), and its primary prediction P50-A4 FAILED (`p50_decide.json :: analysis_set.P50-A4.verdict = FAIL`).

Requested changes:

- Replace the clause with: "the registered PASCAL-50S replication (Section 7.4) failed at its label-gold step (50 references < VOC labels, −2.29 [−5.15, +0.61]), so the ordering claim rests on XM3600 and the second backbone."
- At `sec11_limitations_ethics.md:21`, after "the claim rests on the ordering, which passed on both backbones", add "and failed its label-gold step on PASCAL-50S".
- At `sec11_limitations_ethics.md:19` (exposure) and `:23` (external validity), add PASCAL-50S, whose images and captions have been public since 2008–2015, and its seven models.

### M2. Unresolved placeholder in the submission text

`sec11_limitations_ethics.md:33` contains "[AUTHOR TO CONFIRM: Polaris BSD; DOCCI-Critique CC BY 4.0]" in the visible text. This blocks submission.

Requested change: confirm each licence on its primary release page and write the confirmed licence names. If a licence cannot be confirmed, say that it is unverified and that only aggregates are reported.

### M3. Abstract: the failed PASCAL primary sits behind its secondaries

`abstract_A.md:9` reads: "On PASCAL-50S, with seven public LVLMs, the slope rose at every added reference from one to 50 (registered), and in a registered secondary test reference gold lowered it beyond a size-matched random-deletion null…".

- P50-O2 is a registered SECONDARY test on the COCO-80 vocabulary (`PREREG.md` l.227), yet it is labelled only "(registered)".
- The failed PRIMARY (P50-A4) appears only later, as "the label-gold part of the PASCAL-50S replication", inside a list of failures.
- A reader will therefore take the PASCAL sentence as a successful replication.

Requested change (AI opinion: a PASS headline is fine, but the FAIL must be stated in the same sentence):

> "On PASCAL-50S (seven public LVLMs), the registered primary replication failed at its label-gold step (50 references vs VOC labels: −2.29 [−5.15, +0.61]), while the slope rose at every added reference from one to 50 (registered secondary) and, in a registered companion test, one- and five-reference gold lowered it below a size-matched random-deletion null."

Then remove the PASCAL item from the later list of failures to stay within the word limit. The current count by `wc -w` is 244, against the file's own ≤240 note; check the limit in the SPIC Guide for Authors.

### M4. X4: label, image count, p-value and tie to theory

- **(a) Label.** `manuscript/prereg/2026-10-29_a_companion/RULE.md` §3.2 (l.73) registers X4 as "co-primary" in the companion confirmatory family {X4, X5}. The manuscript calls it "secondary" in `sec1_introduction.md:69` (Table 1 row A24b), `sec7_verbosity_sign.md:129-131` and the abstract. Downgrading is conservative, but the label must match the registration. Write: "co-primary in its registered companion family; secondary to the paper's confirmatory claim".
- **(b) Image count.** `sec7_verbosity_sign.md:139` says "On 1,000 PASCAL-50S images", but the analysis set has 997 (`p50x_decide.json :: n_images = 997`). The 1,000 came from the RULE §7 branch-text template. Write 997.
- **(c) p-value.** `sec7_verbosity_sign.md:133-134` report p = 0.001. With R = 1000, p = 1/1001 is the smallest attainable value. Write "p ≤ 0.001 (the floor at R = 1000)".
- **(d) Tie to theory.** `sec4_theory.md:25` concedes that the ordering of nested reference golds is expected even if objects are missing completely at random (SCAR). X4 is the only registered test here that can reject uniform deletion. Requested changes:
  - Add one sentence in §7.6 linking the X4 PASS to the b-channel of §4.2, worded as "consistent with".
  - State that the null is conditional on the 14 fixed runs (7 models × short/detailed).
  - State that the direction was set beforehand: 8/8 exploratory cells, and a dev analog where all 4 cells gave p = 0.001 (RULE §3.2, §9). The PASS was therefore a strongly anticipated confirmation.
- **(e) Units.** At `sec7_verbosity_sign.md:135`, the "1,782 classes" are summed over images, so call them "image–class pairs".

### M5. PASCAL-50S: system dependence and auditability

- §7.5 shows that on XM3600 the signs under reference gold rest on one verbose system.
- The PASCAL slopes (14 runs, in effect a short-vs-detailed contrast) get no leave-one-model-out check.
- That check cannot be computed now. The 14 caption files were deleted under the 8-gram rule, with no hash kept (`sec11_limitations_ethics.md:35`; Supplementary S7, "Compute and data handling").
- The PAIR_m table (`supplementary.md:620-631`) shows all 7 models negative at one reference. The 50-reference COCO-80 slope has mixed signs (−9.71 to +10.80), and the VOC-label slope is negative for LLaVA-1.5 and LLaVA-OV.

Requested changes (no new GPU run):

- Add to §10.1 (Statistical conclusion validity, `sec11_limitations_ethics.md:21`) that the PASCAL intervals hold the systems fixed, and that a system-level check is impossible because the outputs were deleted.
- In §7.4 (`sec7_verbosity_sign.md:99`), cite the sign heterogeneity in PAIR_m in one sentence.
- Report whether the PASCAL detailed captions hit a token cap, as §7.3 does for the same model set, or state that this was not recorded.

### M6. Related work misses the nearest prior art; novelty is hard to see

Feng et al. 2024, "Do More Details Always Introduce More Hallucinations in LVLM-based Image Captioning?" (arXiv 2406.12663, verified via export.arxiv.org), argues that CHAIR misjudges detailed captions and that language ground truth is lossy. The authors' own `RULE.md` §8 names it as prior work showing that caption-only gold inflates hallucination scores. It is absent from `paperA.bib` and from sec2.

Also add:

- Rohrbach et al. 2018's own finding that one annotation source raises measured hallucination (`sec2_related_work.md:6` currently describes CHAIR without it);
- Amirloo et al. 2024 (arXiv 2407.02477), on the CHAIR–recall trade-off and the noise of CHAIR and Object HalBench;
- Chen et al. 2026 (arXiv 2605.25036, verified), which notes that CHAIR penalises correctly named but unannotated objects.

Requested changes:

- Add these to `sec2_related_work.md:6` and Table 2.1.
- Sharpen the positioning at `sec2_related_work.md:34`. Prior work already knows that incomplete gold inflates hallucination. What this paper adds is gold completeness as a controlled factor that can set the SIGN of F1's verbosity reward, plus the size-matched deletion null.
- No "first" claim appears in the visible text (checked with grep); keep it that way.

Search caveat: Semantic Scholar and OpenAlex were rate-limited or blocked in this environment, so the literature check relied on web search and arXiv only.

### M7. Journal fit and reading burden (editor-level)

- The cover letter (`cover_letter_A.md:14`) places the paper under "multimedia quality assessment and measures".
- The link to SPIC's readership in signal processing and image communication is argued only in §9.4 (`sec10_discussion.md`, "Object metrics as quality-assessment measures").
- The main text is about 12,900 words and dense with registry identifiers (G2B-P3b, A-N1, cv295, uv231, X-22, PAIR_m…).
- Two supplements of different scope exist (`supplementary.md` and `supplementary_SPIC.md`), so it is unclear which one is submitted.

Requested changes:

- Name the one supplement to be submitted.
- Move identifier-level material out of Sections 1 and 7. Keep Table 1 with plain-language test names, and move the registry IDs to a column or to the supplement.
- Add a short paragraph to the Introduction that ties the result to image-communication quality assessment (the dependence of quality measures on the reference set).
- Consider whether a captioning or multimedia-evaluation venue fits better.
- State the confirmatory base plainly where the contribution is claimed (`sec1_introduction.md:27`): 600 XM3600 images, two of five predictions failed, and the PASCAL primary failed.

## Minor issues

- **m1.** `highlights_A.md:5` says "Object F1 verbosity slopes follow gold completeness in two of three registered tests" without naming the three. No highlight mentions PASCAL-50S, although the abstract now does. Name the tests, for example "XM3600 and a second backbone; not PASCAL-50S label gold", or confirm which three are meant.
- **m2.** Fig. 2 (`figs/fig2_slope_by_gold.svg`) and `figs/VALUES.json` have no PASCAL-50S rows. The monotone k = 1→50 ladder (Table S7.P1, P50-NS in `p50_decide.json`) is the clearest picture of the paper's thesis, and it can be plotted from the existing decide file without GPU work. Add it as a panel, and mark the VOC-label point and its failed comparison.
- **m3.** `sec7_verbosity_sign.md:131` says "Take the 50 references as the complete gold". `RULE.md` §2.1 asks for the term "50-reference consensus" (written for X1's truth). For consistency, and to avoid overclaiming completeness, write "50-reference consensus (the complete gold of the registration)".
- **m4.** `sec7_verbosity_sign.md:99` discloses the "aeroplane" matcher gap and V20's dominance by "person", then says "Whether either explains the failed part was not tested." This is good; keep it. Add, as a descriptive pointer with no new test, that the per-model VOC-label slopes are negative for two of seven models (PAIR_m).
- **m5.** `sec7_verbosity_sign.md:92` explains the sign_gt_0 rule well. Also state once in the main text that the interval of part 2 includes 0. The FAIL therefore means the registered direction was not shown, not that the reverse ordering was shown.
- **m6.** The cover letter (`cover_letter_A.md:10`) reports the PASCAL failure but not the O2/X4 passes. Align it with the revised abstract so the editor sees the same balance.
- **m7.** `sec10_discussion.md:1` is headed "# 9 Discussion and conclusion" and sec11 is headed "# 10 Limitations and ethics", while the file names say 10 and 11. The empty stub files `sec9_preference_audit.md` and `appB_matcher_sensitivity.md` remain in the source set. Remove them from the build list so that no empty sections appear.
- **m8.** Section 3.6 (`sec3_measurement_setup.md`, "Statistics") says that registered tests carry uncorrected intervals. Yet Section 7.6 uses Holm for {X4, X5}, and Supplementary S7 gives a descriptive Holm reading over {P50-A4, P50-O2, X4}. Add one sentence to 3.6 naming the families where Holm applies.
- **m9.** Abstract: "reference gold lowered it beyond a size-matched random-deletion null" should be more specific: "one- and five-reference gold gave a lower slope than size-matched random deletions from the 50-reference consensus".
- **m10.** Bootstrap sizes differ across tests: B = 5000 in 3.6, but n_boot = 1000 in `p50_decide.json`. State the PASCAL B in §7.4.

## Full report

HANDLING-EDITOR REPORT (AI opinion; written by an AI reviewer for the authors' internal revision, not by a human referee).

Manuscript: "More References, Larger Verbosity Reward: A Registered Audit of Object Hallucination Metrics Under Incomplete Gold" (Paper A). Target: Signal Processing: Image Communication.

### 1. Summary

The paper asks when an object-level hallucination score (CHAIR, object P/R/F1) supports a comparison between captioning systems. It varies the gold set: one reference, several references, all references, and instance or verified labels. Its single confirmatory claim is that the slope of object F1 on ln M (mentions per image) is ordered by gold completeness.

The evidence:

- a registered out-of-sample test on 600 Vietnamese XM3600 images;
- a registered second-backbone test (Qwen3-VL-8B) on 537 of those images.

A new registered PASCAL-50S study (1,000 images, 50 references each, 7 public LVLMs, 14 runs) adds three results:

- The primary replication, P50-A4, FAILED at its label-gold step.
- The secondary test, P50-O2 ("rise at every added reference"), PASSED.
- A companion mechanism test, X4, PASSED: one- and five-reference golds give a lower slope than a size-matched random-deletion null. Its VOC-label analog, X5, was NOT EVALUABLE.

Exploratory and post hoc parts cover count-matched re-scoring of 15 published comparisons, human-judgment tests (mixed results) and the count channel in preference data.

### 2. Verification performed

- The sha256 of `data/results/p50/p50_decide.json` is 0da4cab90fe9736f…, and that of `p50x_decide.json` is 75e152d266a473b4…. Both match the manuscript's src comments and SHA256SUMS.
- Every PASCAL number in the main text and Supplementary S7 matches the decide files:
  - A4 part 1: +37.16 [+35.07, +39.09], PASS; part 2: −2.29 [−5.15, +0.61], FAIL;
  - the O2 steps;
  - the descriptive +30.56;
  - the P50-NS rungs;
  - sensitivity over all 1,000 images: +37.26 [+35.35, +39.38] and −2.37 [−5.44, +0.62];
  - X4: −31.38 vs [−14.97, −12.12], and −20.99 vs [−9.28, −6.87];
  - X5 NOT_EVALUABLE by the pre-written 2·Σk rule (1,782 < 2 × 1,039.6);
  - Holm over {X4} alone;
  - descriptive family-wise p-values 0.939, 0.001 and 0.001;
  - the per-model slopes in PAIR_m.
- The PREREG commit (353437f, 07:49 +0700 = 00:49Z) precedes the first output (00:51Z, EVENTS), so the one-look rule was respected.
- The verdict rules in PREREG l.215-218 (sign_gt_0: FAIL if the point estimate is ≤ 0) and RULE §3.2 were applied as registered.
- The manuscript does not report X5's observed value, which is correct for a test that was not evaluable.
- No "first" claim appears in the visible text.
- The related-work searches used web search plus the arXiv API. Semantic Scholar and OpenAlex were rate-limited or blocked here, so the search is incomplete.

### 3. Answers to the two specific questions

**(a) Is X4 acceptable in the abstract?** Yes, conditionally (AI opinion).

- X4 was registered before the look, Holm-corrected within its family, and passed by a wide margin.
- It is also the only registered test in the paper that can separate salience-driven missingness from missingness completely at random. Section 4.2 itself concedes that the ordering of nested reference golds is expected even under random missingness.
- The current wording is suitably hedged ("consistent with").

Conditions:

- Label it to match the registration: co-primary in the companion family, secondary to the paper's claim.
- Do not let X4, together with the secondary O2, stand in front of the failed primary P50-A4 in the same sentence (Major 3).
- Correct the 1,000 → 997 slip and the wording of the p-value floor in §7.6 (Major 4).

**(b) Is the A4 FAIL reported adequately?** In the body, yes: §7.4 gives both parts, the rule and the registered branch text, and the FAIL also appears in Table 1 row A24, §9.1, §9.5 and the cover letter. It is not yet adequate in three places:

- The abstract mentions it only inside a list of failures, after PASCAL secondaries presented as successes.
- The highlights do not mention PASCAL at all.
- Limitations §10.1 still says the test was "registered, not run" (Major 1). This directly contradicts the FAIL and is the most serious reporting defect.

### 4. Scores (AI opinion)

**NOVELTY 3/5.** Real but incremental.

Already known:

- Incomplete or caption-only gold inflates measured hallucination (Rohrbach et al. 2018; Feng et al. 2024, arXiv 2406.12663, missing from the manuscript).
- CHAIR trades off with recall (Amirloo et al. 2024, arXiv 2407.02477, also missing).
- LeHaCE and CCEval control length or means.

New in this paper:

- gold completeness treated as a controlled factor that can flip the SIGN of F1's verbosity reward;
- per-image count-matched controls applied to released outputs;
- the size-matched deletion null;
- a fully reported registration ledger.

I found no prior work that varies the number of references as an experimental factor on object-hallucination scores, subject to the search caveat above.

**CORRECTNESS 4/5.** The numbers match their sources, and the verdicts are copied, not re-judged. Failures and post hoc labels are disclosed in unusual detail. The weak points are conceded openly: the dependence on verified precision, the dependence on one verbose system, and the 160-token cap.

Deductions:

- the stale "not run" sentence;
- 997 vs 1,000;
- the X4 label mismatch;
- the wording of the p-value floor;
- no system-level robustness check for PASCAL, and the outputs were deleted, so per-image results cannot be audited.

The confirmatory claim is narrow and partly expected by construction (Section 4.2). The paper says so, which is to its credit.

**CONTRIBUTION 3/5.** The practical message for practitioners is useful: report the gold, the matcher and M per system, and pre-declare one count control. Its limits:

- The confirmatory base is one 600-image set plus a second backbone from the same family.
- Two of five XM3600 predictions failed, and the PASCAL primary failed.
- The count-control part, the most actionable for practitioners, has no confirmatory result.
- Relevance to SPIC's image-communication readership is argued only in §9.4.

**CLARITY 2/5.** The writing is precise and every number is keyed, but the paper reads like an audit ledger:

- about 12,900 words of main text;
- dense registry identifiers (G2B-P3b, A-N1, cv295, uv231, X-22, PAIR_m);
- two co-existing supplements;
- section numbers that do not match the file names;
- a visible placeholder;
- no PASCAL panel in the figures.

A non-specialist SPIC reader would struggle to extract the main finding.

### 5. Recommendation: MAJOR REVISION (AI opinion)

The PASCAL reporting is numerically sound. The revision should:

- (i) fix the internal contradictions and the placeholder (M1, M2);
- (ii) rebalance the abstract's PASCAL sentence so that the primary FAIL comes first, keeping a PASS headline elsewhere (M3);
- (iii) tidy X4's label, image count, p-value and link to theory (M4);
- (iv) state the limits on system dependence and auditability for PASCAL (M5);
- (v) add the missing nearest prior art and sharpen the positioning (M6);
- (vi) cut the reading burden and argue the fit for the journal (M7).

None of these needs new human labels, new GPU runs or a second look at any test set. Every requested change is text, a re-plot of values already in the decide files, or a stated limitation.

### 6. Binding-rule notes for the revision

- No new gold labels; AI labels are not evidence.
- PASCAL-50S has had its one look. Any new PASCAL analysis is post hoc and descriptive only, and per-image re-analysis is impossible because the outputs were deleted.
- Keep every registered FAIL visible; a PASS headline is allowed.
- No "first" claims.
- Quote no caption text from OpenViIC, KTVIC or UIT-ViIC.
- Any literature lookup uses vsps-research@example.org or no e-mail.
- This review made no edits, commits or GPU use.
