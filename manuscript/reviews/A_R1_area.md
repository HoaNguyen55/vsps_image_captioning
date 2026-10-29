# Paper A review: Reviewer R1 (senior area expert)

All judgements are AI opinion (a simulated reviewer, not a human referee). Copied verbatim in substance from the review panel output of 2026-10-29.

**Scores (1-5):** novelty 3, correctness 3, contribution 3, clarity 2. **Recommendation:** major revision. **Confidence:** 4/5.

## Summary

This is a carefully registered measurement audit of object-level hallucination scores (CHAIR, object F1). It treats gold completeness as an experimental factor and reports every registered verdict, failures included. Every PASCAL-50S number I checked matches the decided files:

- P50-A4 is FAIL: part 2 is −2.29 [−5.15, +0.61].
- P50-O2 is PASS at all five steps.
- X4 is PASS: the observed slopes −31.38 and −20.99 fall outside the null ranges [−14.97, −12.12] and [−9.28, −6.87].
- X5 is NOT_EVALUABLE, because 1,782 < 2 × 1,039.6.

The file hashes match (0da4cab90fe9 / 75e152d266a4). Both registrations were committed at 00:49:49Z, before the run started at 00:51:22Z. Spot checks of the XM3600 and second-backbone numbers (+5.89, +20.10, +1.97 [−0.44, +4.01], n = 537) also match.

The main weaknesses lie in what the evidence licenses, not in the arithmetic:

- The confirmatory ordering is close to mechanical for nested reference golds, as sec4:25 admits.
- The part that carries risk, the label-gold leg, gives mixed results. It depends on the verified-precision rule, the reference signs rest on one verbose system, and it FAILED as the primary PASCAL-50S replication.
- The inference is conditional on 6–14 systems that form short-versus-detailed clusters.

The A4 FAIL is reported adequately in §7.4, Table 1, §9.1, §9.5 and the cover letter. It is under-weighted in the abstract and in contribution 1, and the Limitations section still says the test was "not run". The X4 sentence in the abstract is acceptable: it was registered before any output, it is secondary, it survives Holm, and it is hedged. It needs only a more precise rewording. Every fix is textual; none needs new labels, new looks or GPU time.

## Major issues

**M1. The abstract under-weights the failure of the registered primary PASCAL-50S test (abstract_A.md:9).**

- The problem:
  - The PASCAL sentence opens with the secondary P50-O2 PASS, labelled only "(registered)", and then gives the X4 PASS.
  - The FAIL comes later, only as "the label-gold part of the PASCAL-50S replication" in a list.
  - It is never identified as the primary prediction (P50-A4, PREREG §3.5 l.225), and it carries no number.
  - The cover letter (cover_letter_A.md:10) and §9.1 (sec10_discussion.md:7) are more candid than the abstract.
- Requested change:
  - Keep the PASS headline, which is allowed, but state briefly that "the primary registered PASCAL-50S replication failed on its label-gold part (VOC labels vs 50 references: −2.29 [−5.15, +0.61])".
  - Relabel O2 as "registered secondary".
  - Scope the first claim sentence ("more complete gold raises the verbosity reward") so that it agrees with sec10_discussion.md:7. That passage says the claim "does not extend to a 50-reference gold against 20-class labels".
  - Trim elsewhere to stay within the 240-word target.

**M2. The confirmatory claim is largely expected by construction, and the part that carries risk gives mixed results (sec4_theory.md:25, sec11_limitations_ethics.md:9, sec1_introduction.md:9,27).**

- The problem:
  - The paper concedes that nested reference golds order the slopes even under SCAR, through the Ḡ-channel. P50-O2 and G2B-O2 are therefore low-risk tests, yet the title ("More References, Larger Verbosity Reward") and contribution 1 lean on them.
  - The non-trivial leg, label gold above all references, holds on XM3600 only under verified precision. It is fragile in three places:
    - On the second backbone the bracket lower bound is +1.97 [−0.44, +4.01] (bracket_result.json, sets.xm600.slopes.lower; verified).
    - The reference signs flip without one verbose system (Table 7.3).
    - It FAILED on PASCAL-50S.
- Requested change:
  - In §1, §9.1 and the abstract, separate the part that is expected by construction (the reference rungs) from the risky part (label gold).
  - Tally the label-gold leg honestly: PASS on XM3600 under verified precision; PASS on the second backbone, but the post hoc lower bound includes 0; FAIL on PASCAL-50S.
  - Present X4 as the one PASCAL result that SCAR does not predict. Scope it to reference gold, since X5 was not evaluable.
  - Consider a title that does not state the near-mechanical part as the finding.

**M3. Inference is conditional on a handful of clustered systems, and the abstract does not say so (abstract_A.md:9; sec7_verbosity_sign.md:65,114; sec3_measurement_setup.md:51).**

- The problem:
  - All intervals come from an image bootstrap with the systems held fixed.
  - XM3600 has 6 systems. One names 4.29 objects per caption, against 1.08–1.79 for the rest (bracket_result.json, per_system). Its system-jackknife intervals are [−52.29, +34.31] and [−47.88, +43.02].
  - On the second backbone, the xm600 M values cluster at about 1.49 and 3.93, because 99.7% of detailed captions hit the cap. The slope is therefore a two-cluster contrast.
  - The 14 PASCAL runs are 7 short/detailed pairs. The per-model PAIR_m values (supplementary.md, table after S7.P1) show negative VOC-label slopes for LLaVA-1.5-7B (−1.05) and LLaVA-OV-7B (−0.32).
- Requested change:
  - Add "conditional on the systems scored" to the interval statement in the abstract.
  - In §7.4, add one sentence reporting the per-model heterogeneity already in the decided file. Keep it descriptive, with no verdict.
  - In §10.1, state that the slope is in effect a short-versus-detailed contrast in every registered family, not only on the second backbone.

**M4. The premise of P50-A4 is not discussed, and no reading of the FAIL is offered (sec7_verbosity_sign.md:99; sec3_measurement_setup.md:13).**

- The problem:
  - P50-A4 assumes that the VOC labels are more complete than 50 references on V20. Yet on V20 the 50-reference slope (+9.74 [+7.29, +12.12]) exceeds the VOC-label slope (+7.45 [+4.98, +9.94]).
  - §3.1 already concedes that label gold need not contain reference gold. With 50 writers, the reference consensus restricted to the 20 classes may be as complete as the 20-class VOC annotation, or more complete. It can also include matcher hits on objects VOC did not annotate.
  - §7.4 lists only the "person" imbalance and the "aeroplane" matcher gap, and says neither was tested.
- Requested change:
  - Add one sentence that names this obvious alternative reading as untested. No re-scoring and no second look are involved.
  - Optionally, add output-free gold sizes per rung on V20 (Σ|refs50∩V20| vs Σ|voc20| = 1,782), labelled post hoc. These need no model outputs, so they are not a look at the test set. Omit them if the data-handling rule forbids re-staging the references.

**M5. The Limitations section contradicts the results (sec11_limitations_ethics.md:9,21).**

- The problem:
  - Line 9 still says "the large-reference-set test is registered, not run (Section 7.4)". It was run, and its primary prediction failed.
  - Line 21 says "the claim rests on the ordering, which passed on both backbones" without noting the failed PASCAL replication.
- Requested change:
  - Replace line 9 with "the large-reference-set test on PASCAL-50S was run once; its primary prediction failed on the label-gold part (Section 7.4)".
  - Add the same qualification to line 21.

**M6. The PASCAL-50S verdicts cannot be audited (sec11_limitations_ethics.md:34; sec7_verbosity_sign.md:88).**

- The problem:
  - All 14 caption files were deleted under the 8-gram rule, and no per-file hash was kept. The primary FAIL and both PASSes therefore rest on aggregate decide files that cannot be re-derived without re-decoding.
  - That is acceptable under the data licences, but a journal reader must see it where the result is reported, not only in §10.2.
- Requested change:
  - In §7.4, add one sentence stating that the per-image outputs were deleted under the registered data rule, and that the decide files, EVENTS log, evaluator hashes and job are in the deposit.
  - In Supplementary S4, disclose the off-protocol laptop refcheck of the pascal50S.json structure (RULE §0 l.12; accepted as a disclosed deviation under CC-159 ruling 6). It is not mentioned anywhere in supplementary*.md.

**M7. Clarity and length for an SPIC readership (sec1_introduction.md:36-76; throughout).**

- The problem:
  - The paper runs to about 13–14k words, with a 40-row ledger.
  - Internal codes reduce readability: cv295, uv231, xm600, s75, A-N2, P50-A4, X4, "rung", "family ALL", G2B-O1.
  - One raw evaluator token is printed as a verdict ("PASS_DRHO113_MIXED_MCP_CI_INCLUDES_1", sec1_introduction.md:47).
  - Two supplements (supplementary.md, supplementary_SPIC.md) duplicate content, which risks divergence.
  - The core message is diluted by the count-control and preference sections, which carry no confirmatory claim.
- Requested change:
  - Give the ledger plain-language test names and move the IDs to a column.
  - Replace raw evaluator strings with verdict words.
  - Keep a single supplement.
  - Consider moving §6 and §8.3–8.4 to the supplement so that the paper centres on RQ1.

## Minor issues

- **m1.** sec7_verbosity_sign.md:139 says "On 1,000 PASCAL-50S images". Write "on the 997-image analysis set" (p50x_decide.json, n_images = 997).
- **m2.** sec7_verbosity_sign.md:133-134: p = 0.001 is the smallest value attainable with R = 1,000. Write "p ≤ 0.001" or "below every null replicate".
- **m3.** sec7_verbosity_sign.md:135: "so the null could barely move" is the registration's rationale (RULE l.76), not an observed fact. The evaluator printed a null range of [−16.05, −12.26] for X5. Write only that the pre-written evaluability condition (Σ|voc20| ≥ 2Σk) was not met (1,782 < 2,079.2) and that X5 carries no result.
- **m4.** abstract_A.md:9 (X4 clause): the X4 mention is acceptable, but make its referent precise. "Reference gold lowered it beyond a null" is ambiguous. Suggested wording: "the slope under one- and five-reference gold lay below the 95% range of a size-matched random-deletion null drawn from the 50-reference consensus (registered secondary)".
- **m5.** sec7_verbosity_sign.md:88 says "before the first output (00:51Z)". In EVENTS, 00:51:22Z is the run start, not the first output. Write "before the run started".
- **m6.** figs/CAPTIONS.md:5 has stale cross-references. The second-backbone sets are now in Section 7.3 (the caption says 7.6, which is now the X4 section), and the bracket is in Section 7.2 (the caption says 7.5). Consider adding a PASCAL-50S row to Table 7.1 and Fig. 2 (1 reference, 50 references, VOC labels on V20), copied from P50-NS.
- **m7.** sec3_measurement_setup.md:9 says "Analyses that vary k use at most the first five references". This contradicts §7.4, which draws random k up to 50. Add the PASCAL-50S exception.
- **m8.** sec1_introduction.md:27 (contribution 1): state that the PASCAL-50S primary replication failed, in the same sentence that cites its secondary PASS.
- **m9.** Novelty and positioning (sec2_related_work.md:14,34; sec7_verbosity_sign.md:141).
  - Misra et al. (2016), "Seeing through the Human Reporting Bias" (CVPR, doi 10.1109/CVPR.2016.320, verified on Crossref), bears directly on X4 and on assumption A2 (which present objects people name). It is absent from paperA.bib and should be cited and discussed.
  - Also consider the following works, verified to exist on Crossref. I have not read them, so cite them only after reading:
    - Dai et al. 2023, "Plausible May Not Be Faithful" (EACL, 10.18653/v1/2023.eacl-main.156);
    - Biten et al. 2022, "Let there be a clock on the beach" (WACV, 10.1109/WACV51458.2022.00253);
    - Lovenia et al. 2024, NOPE (10.18653/v1/2024.alvr-1.4).
  - Berg et al. 2012, listed in the companion prior_art_W3, was not verified by me.
  - The novelty search was partial: OpenAlex and Semantic Scholar were rate-limited, so only Crossref and arXiv were queried.
  - Keep the no-"first" wording.
- **m10.** abstract_A.md:9 runs to 244 words, against the file's own ≤ 240 target (l.3 comment). Check the SPIC limit at submission.
- **m11.** sec11_limitations_ethics.md:33 still contains "[AUTHOR TO CONFIRM: Polaris BSD; DOCCI-Critique CC BY 4.0]", and title_page_A.md and cover_letter_A.md have address placeholders. Resolve these before submission (administrative, low priority).
- **m12.** sec4_theory.md:23, Proposition 1(d): note that on PASCAL-50S the COCO-80 slope stays non-positive up to k = 50 (−0.83 [−2.58, +1.07]), while on V20 it changes sign between k = 10 and k = 50. This illustrates that the crossing location is not predicted, as §4 already says.
- **m13.** The title (title_page_A.md:5; abstract_A.md:5) differs from the "chosen title" recorded in outline.md:24. Record the final choice, and keep it consistent across the title page, abstract and cover letter.
- **m14.** Table 1 (sec1_introduction.md:67-71): add the effect and interval to the A24 row (−2.29 [−5.15, +0.61]). Mark A24a and A24b as "secondary" in the Verdict column as well, so the FAIL/PASS asymmetry reads at a glance.

## Full report

REVIEW REPORT. AI opinion: a simulated expert review, not a human referee's report.

Manuscript: "More References, Larger Verbosity Reward: A Registered Audit of Object Hallucination Metrics Under Incomplete Gold". Target: Signal Processing: Image Communication.

### 1. Summary of the submission

The paper asks when object-level hallucination scores (CHAIR, object P/R/F1) can support a comparison between two captioning or LVLM systems. It varies the gold as an experimental factor: 1..k references, all references, instance labels, or verified labels.

Its one confirmatory claim is that the OLS slope of object F1 on ln M (mentions per image) is ordered by gold completeness. That claim rests on two registered tests:

- an XM3600-vi test (600 images, 6 Qwen-based systems);
- a second-backbone test (Qwen3-VL-8B, 537 of the same images).

A registered PASCAL-50S study (1,000 images, 50 references, 7 public LVLMs, 14 runs) adds three things:

- a primary replication of the ordering (P50-A4);
- a secondary ladder test (P50-O2);
- a companion mechanism test against a size-matched random-deletion null (X4/X5).

Further material covers a descriptive propensity decomposition, a reference-exchangeability diagnostic, post hoc count-matched re-scoring of 15 published comparisons, and registered tests on human judgments and preference data. Every verdict is listed in a registration ledger, failures included (9 FAILs).

### 2. Verification performed by this reviewer

- p50_decide.json (sha256 0da4cab90fe9…) and p50x_decide.json (75e152d266a4…) match the hashes cited in the text and in SHA256SUMS.
- Every PASCAL-50S value in §7.4, §7.6 and Supplementary S7 matches the decided files:
  - P50-A4: part 1 +37.16 [+35.07, +39.09] PASS; part 2 −2.29 [−5.15, +0.61] FAIL; compound FAIL; Holm p 0.939.
  - P50-O2: all five steps PASS.
  - X4: −31.38 against the null [−14.97, −12.12], and −20.99 against [−9.28, −6.87]; PASS; Holm within the companion family, X4 alone.
  - X5: NOT_EVALUABLE, 1,782 < 2 × 1,039.6.
  - Analysis set: 997 images, 7 models, 14 runs.
- The registration commit 353437f is dated 00:49:49Z, and the EVENTS run start is 00:51:22Z. The registration therefore precedes any output.
- Spot checks of XM3600 and the second backbone match:
  - g2b_score.json G2B-O1: +5.89 [+4.76, +6.87] and +20.10 [+17.39, +23.05], n = 537;
  - bracket_result.json xm600 lower bound: +1.97 [−0.44, +4.01];
  - s75 lower bound: +5.83 [+3.82, +7.82].
- The P50 branch text of §9.2 was inserted essentially verbatim in §7.4 (sec7:97).
- The prior-art search used Crossref and arXiv only. OpenAlex and Semantic Scholar were rate-limited, so the novelty search is partial.

### 3. Assessment by criterion

**NOVELTY: 3/5.**

- New framing:
  - the gold is treated as the factor;
  - each caption is matched once and scored against nested golds;
  - the size-matched random-deletion null (X4) separates "which objects" from "how many".
- Most of the underlying phenomenon has known precedents:
  - caption-only gold inflates hallucination (Rohrbach et al. 2018, acknowledged);
  - pool bias in IR (Buckley and Voorhees 2004; Zobel 1998; Sakai 2007);
  - label completeness changes rankings (ImageNet ReaL; RePOPE).
- The paper concedes (sec4:25) that the ordering of nested reference golds is expected even under SCAR, so the confirmatory finding is partly expected by construction.
- The genuinely informative pieces are the label-gold leg and X4.
- Reporting bias in what people name (Misra et al. 2016, CVPR) is directly relevant to X4 and A2, and it is not cited.
- The paper correctly avoids "first" claims.

**CORRECTNESS: 3/5.**

The registration discipline is exemplary: commit before output, pre-written branch texts, one look, and verdicts copied from decide files. Every number I checked is correct. The problems are in inference and consistency:

- (a) The intervals are conditional on 6–14 systems that form short-versus-detailed clusters:
  - the XM3600 system-jackknife intervals span zero;
  - the reference signs flip without one verbose system;
  - on PASCAL-50S, two of the seven models have negative per-model VOC-label slopes;
  - the abstract does not state this conditioning.
- (b) The label-gold leg gives mixed results across its three tests, but the abstract and §1 present the ordering as holding.
- (c) The premise of P50-A4, that the VOC labels are more complete than 50 references on V20, is untested and is not discussed as a reading of the FAIL.
- (d) Some statements are stale or contradictory:
  - Limitations l.9 says the PASCAL test was "registered, not run";
  - §7.6 says 1,000 images instead of 997;
  - the X5 gloss goes beyond the data;
  - the figure-caption cross-references are wrong.

**CONTRIBUTION: 3/5.**

- The paper is practically useful for the community:
  - report the gold, the matcher and M;
  - avoid comparing F1 across verbosity regimes under incomplete gold;
  - use random-k subsets and check exchangeability;
  - audit count imbalance in preference data.
- The registered ledger and the numbers manifest are a model of transparent reporting.
- Four things limit the scientific weight:
  - the confirmatory result is close to mechanical for reference golds;
  - the label-gold leg fails out of sample;
  - no count-control claim is confirmatory;
  - the human-validity evidence is mixed or negative.
- Fit with SPIC (image communication and quality-assessment measures) is plausible through the angle of quality-measure validity (González-Chávez et al. 2024 in SPIC), but the paper reads as an NLP evaluation study.

**CLARITY: 2/5.**

- The prose is careful and hedged.
- The paper is long and dense with internal identifiers (cv295, uv231, xm600, s75, A-N2, P50-A4, X4, "rung", "family ALL").
- The 40-row ledger interrupts the introduction, and one raw evaluator token is printed as a verdict.
- Two supplement files duplicate content.
- The key message is diluted by sections that carry no confirmatory claim.

### 4. Specific questions from the editor

**(i) Is X4 in the abstract acceptable?** Yes.

- X4 was registered in the companion RULE, committed jointly with P50 before any output.
- It is labelled secondary, and it survives Holm (X5 left the family as NOT_EVALUABLE).
- Its wording ("consistent with …") follows the pre-written branch text.
- Arguably it is the most informative PASCAL result: random missingness (SCAR) does not predict it, whereas the Ḡ-channel alone predicts P50-O2.

Two requests:

- Make the referent precise: the slope under one- and five-reference gold lay below the null's 95% range.
- Keep it scoped to reference gold, since the label-gold analog (X5) carries no result.

**(ii) Is the A4 FAIL reported adequately?**

In the body, yes: §7.4 gives the value, the interval, the rule and the branch text, and the FAIL also appears in Table 1 row A24, §9.1, §9.5 and the cover letter. The gaps are:

- The abstract does not identify it as the primary registered prediction and gives no number, while the two secondary PASSes lead.
- Contribution 1 omits it.
- Limitations l.9 still says the test was not run.
- §7.4 does not name the most obvious alternative reading: that 50 references may be at least as complete as the 20-class VOC labels on V20.

All of these can be fixed in the text alone (see M1, M4, M5, m8, m14), without hiding the FAIL or adding a test.

### 5. Major issues

Numbered M1–M7 above:

- M1: the abstract's framing of the PASCAL-50S primary FAIL.
- M2: the confirmatory ordering is expected by construction for reference rungs; tally the label-gold leg honestly and reconsider the title.
- M3: inference is conditional on a few clustered systems; state this and report the per-model heterogeneity.
- M4: the untested premise of P50-A4 and its alternative reading.
- M5: the Limitations section contradicts the results.
- M6: the PASCAL verdicts cannot be audited; also disclose the laptop refcheck deviation.
- M7: clarity, length and internal codes.

### 6. Minor issues

Numbered m1–m14 above:

- n = 997 vs 1,000;
- the p ≤ 0.001 floor;
- the X5 gloss;
- the precision of the X4 wording;
- run start vs first output;
- stale figure cross-references;
- the five-reference statement in §3.1;
- contribution 1;
- missing prior art (Misra 2016 and others, verified on Crossref);
- abstract length;
- leftover placeholders;
- the crossing location on PASCAL;
- title consistency;
- the ledger row for A24.

### 7. Constraints respected in these requests

- None of the requested changes needs new human gold labels, AI-generated labels, a second look at any test set, GPU time, or caption text from OpenViIC, KTVIC or UIT-ViIC.
- The optional V20 gold-size count in M4 is output-free and would have to be labelled post hoc. Drop it if the registered data rule forbids re-staging the PASCAL-50S references.
- Registered FAILs stay in the text, stated briefly. A PASS headline remains allowed.

### 8. Recommendation

Major revision. The registration and provenance machinery is strong, and the numbers are correct. The required revision is about calibrating claims, chiefly:

- the abstract and the contributions;
- the system-conditional nature of the slopes;
- the status of the label-gold leg after the PASCAL-50S FAIL;
- internal consistency.

Reviewer confidence: 4/5.
