# Paper A review: Reviewer R3 (evaluation-metrics specialist)

All judgements are AI opinion (a generated reviewer, not a human referee). Copied verbatim in substance from the review panel output of 2026-10-29.

**Scores (1-5):** novelty 3, correctness 3, contribution 3, clarity 2. **Recommendation:** major revision. **Confidence:** 4/5.

## Summary

This is a registered measurement audit of object-level hallucination scores (object F1 / CHAIR) that treats gold completeness as the experimental factor. I checked every number I traced against the decide files and the preregistrations, and they match exactly:

- XM3600: −8.99 / −2.43 / +19.32.
- G2B xm600: +5.89 / +20.10 on n = 537.
- Bracket: +1.97 [−0.44, +4.01].
- P50-A4: part 1 +37.16 PASS; part 2 −2.29 [−5.15, +0.61] FAIL.
- P50-O2: all five steps PASS.
- X4: −31.38 vs [−14.97, −12.12], and −20.99 vs [−9.28, −6.87].
- X5: NOT_EVALUABLE, with 1,782 < 2 × 1,039.6.

I also confirmed that the registration commit 353437f (00:49:49Z, carrying PREREG.md, RULE.md, p50.py and p50x.py) precedes the first output at 00:51:22Z. Registration discipline and the reporting of FAILs are unusually good.

My main concerns are interpretive:

1. The reference-rung results that headline the abstract and title (P50-O2, P50-A4 part 1) are, by the authors' own Section 4.2, expected under nesting even with completely random missingness. The one non-nested, risky step (label gold above all references) passes on XM3600 only under the favourable verified-precision rule. It fails on PASCAL-50S, where the labels are exhaustive on their 20 classes. The paper never puts these two findings together.
2. The limitations section is stale: it says the PASCAL-50S test is "registered, not run".
3. The reading of X4 ignores the object-importance and reporting-bias literature, which already shows that naming is non-uniform.
4. The abstract tags the PASCAL secondary PASS but leaves the PASCAL primary unlabelled, and its "reported in full" list is incomplete.
5. For an SPIC readership the text is very dense with registration jargon.

## Major issues

**M1. Stale and contradictory limitation statement.**

- manuscript/journal_draft/sec11_limitations_ethics.md:9 says "the large-reference-set test is registered, not run (Section 7.4)".
- Section 7.4 (sec7_verbosity_sign.md:86-99) reports the test as run, with a FAIL (data/results/p50/p50_decide.json, sha 0da4cab90fe9, analysis_set.P50-A4.verdict = FAIL).
- The same paragraph and sec11:21 ("the claim rests on the ordering, which passed on both backbones") omit the PASCAL-50S failure.
- sec11:23 (external validity) does not mention the seven PASCAL-50S LVLMs.
- Requested change:
  - rewrite sec11:9 to say that the PASCAL-50S replication ran and failed at its label-gold step (−2.29 [−5.15, +0.61]);
  - in sec11:21, add that the ordering did not replicate on PASCAL-50S;
  - in sec11:23, add the seven-LVLM PASCAL family.

**M2. The near-mechanical part is headlined, and the risky part is never brought together.**

- Section 4.2 (sec4_theory.md:25) states that nested reference golds order the slopes "even if objects are missing from references completely at random". P50-O2 and P50-A4 part 1 are therefore expected outcomes.
- Yet the title ("More References, Larger Verbosity Reward") and abstract_A.md:9 present them as the PASCAL-50S evidence.
- The only non-nested step (label gold above all references) behaves as follows:
  - It passes on XM3600 under verified precision (sec3_measurement_setup.md:13).
  - On xm600 it drops to +1.97 [−0.44, +4.01] when unverifiable mentions count as errors (bracket_result.json).
  - On PASCAL-50S, where the VOC labels are exhaustive on V20 and no mention is excluded, it fails: +7.45 under VOC labels vs +9.74 with 50 references (Table S7.P1, supplementary.md:607-617).
- Requested change (AI opinion; no new analysis):
  - In §9.1 (sec10_discussion.md:7), add a short synthesis paragraph stating that every test of the label-over-reference step under a non-favourable precision rule is weak or failed.
  - Add one clause to the abstract saying that the rise across reference rungs is expected under nesting.
  - Consider a title that does not lead with the mechanically expected result.

**M3. Abstract framing of PASCAL-50S, and whether X4 is acceptable in the abstract.**

In my AI opinion, X4 in the abstract is acceptable: it is a registered PASS that survives Holm, and the binding rules allow a PASS headline. Three defects in abstract_A.md:9 need fixing:

- (a) P50-O2 is tagged only "(registered)", although it is secondary (PREREG §3.6; Table 1 row A24a, sec1_introduction.md:68). Readers will take it for the PASCAL primary.
- (b) The failure sentence says "the label-gold part of the PASCAL-50S replication" without saying that this was the registered primary PASCAL-50S test.
- (c) "Registered failures are reported in full:" is followed by a list of three items, but Table 1 has nine FAIL rows (A2, A5, A10, A14, A15, A18, A19, A21, A24).

Requested minimal edit:

- write "registered secondary" for O2;
- write "the registered primary PASCAL-50S test (ordering through VOC labels) failed at its label-gold step";
- replace "reported in full:" with "Nine registered predictions failed (Table 1), including …";
- apply the same "secondary" label in the introduction at sec1_introduction.md:9 ("registered PASS").

The A4 FAIL itself is reported adequately in §7.4 (sec7_verbosity_sign.md:90-97, with the prereg §9.2 branch text verbatim), in Table 1 row A24 (sec1_introduction.md:67), in §9.1 and in the Conclusion. No change is needed there.

**M4. A4 part 2 assumes, without measuring, that the VOC labels are more complete than 50 references.**

- The PASCAL-50S label rung and the 50-reference gold are not nested: refs50∩V20 is not guaranteed to be a subset of the VOC labels.
- The data suggest that the 50-reference V20 gold may already rival the VOC labels. The V20 slope climbs from +1.49 at k = 20 to +9.74 at k = 50, above the VOC-label slope of +7.45 (supplementary.md, Table S7.P1).
- The VOC labels also include difficult and truncated objects that no writer names (PREREG §4.1).
- The reading "more complete gold → larger slope" is therefore untested at this step.
- Requested change: no re-analysis, since that would be a second look and the captions are deleted. Instead, add a disclosed-limitation sentence to §7.4 (sec7_verbosity_sign.md:99) and §10.1. It should state that:
  - the completeness order of the VOC labels versus 50 references was assumed, not measured;
  - the FAIL may reflect a gold that is not more complete, rather than a more complete gold without a larger slope.

**M5. The interpretation of X4 omits prior art on naming propensity and reporting bias.**

- X4's null (RULE.md §3.1) is a SCAR-type uniform deletion. A PASS therefore rejects random missingness and shows non-uniform naming propensity, which assumption (A2) already posits (sec4_theory.md:15).
- The paper reads it as "which objects annotators name mattering" (abstract_A.md:9; sec7_verbosity_sign.md:139).
- Non-uniform object naming is established in prior work that the manuscript does not cite, although the companion prior-art note lists Berg et al. All three works below were verified on Crossref:
  - Spain and Perona, "Measuring and Predicting Object Importance", IJCV 2010, DOI 10.1007/s11263-010-0376-0;
  - Berg et al., "Understanding and predicting importance in images", CVPR 2012, DOI 10.1109/cvpr.2012.6248100;
  - Misra et al., "Seeing through the Human Reporting Bias", CVPR 2016, DOI 10.1109/cvpr.2016.320.
- The "naming propensity" π of Section 4.1 is essentially Spain and Perona's object importance.
- Requested change:
  - cite these works in §2 and §4.1;
  - in §7.6 (sec7_verbosity_sign.md:139-141), say that X4 quantifies a known reporting bias against a size-matched null on a 50-reference gold, which is the addition the authors already scope (RULE §8);
  - keep the no-"first" wording.

**M6. System-level uncertainty and the token cap on PASCAL-50S are not disclosed in §7.4.**

- The PASCAL-50S slopes are OLS fits over 14 runs (7 models × short/detailed), with an image bootstrap that holds the systems fixed (sec3_measurement_setup.md:51).
- The V20 mention counts span only 1.12–2.24 (p50_decide.json, analysis_set.M.V20).
- Prereg §10 item 2 warns that the detailed captions hit the 160-token cap. That makes the slope close to a short-versus-detailed contrast, as §7.3 already discloses for G2-B.
- On XM3600, the reference-gold signs flipped when one verbose system was dropped (Table 7.3).
- For PASCAL-50S no leave-one-out is possible: the decide file stores no per-run F1, and the captions were deleted.
- Requested change: do not recompute, since that would be a second look. Instead, add a stated limitation to §7.4 and mirror it in sec11:21. It should say that:
  - the intervals condition on the 14 runs;
  - the slope is largely a short-versus-detailed contrast under the cap;
  - system-level robustness could not be assessed, because the outputs were deleted under the registered data rule.

**M7. Clarity for the SPIC readership.**

- The main text is dominated by registration bookkeeping:
  - a ~40-row ledger in the Introduction (sec1_introduction.md:36-76);
  - internal IDs such as N1-XM-4, G2B-O1, LBA-P2, cv295, uv231, xm600 and s75;
  - repeated status qualifiers in nearly every sentence.
- A Q2 signal-processing reader cannot easily see the three scientific findings.
- Requested change:
  - move Table 1 to a Methods subsection or the Supplement, and keep a five-line summary table (confirmatory / secondary / failed) in the Introduction;
  - replace the set codes with descriptive names in the main text;
  - add a single schematic figure for the gold ladder. The planned Fig. 1 schematic (outline.md:99) does not appear in the section files.

## Minor issues

- **m1.** sec7_verbosity_sign.md:139: "On 1,000 PASCAL-50S images" should be "On the 997-image analysis set (of 1,000)", as in p50x_decide.json (n_images = 997) and §7.4.
- **m2.** sec7_verbosity_sign.md:133-134: p = 0.001 is the smallest p attainable with R = 1000 (1/1001; RULE §4). Report it as "p ≤ 0.001 (minimum attainable with 1,000 replicates)".
- **m3.** The tier label for X4 conflicts. RULE.md:73-74 labels X4 and X5 "co-primary" within the companion family, while sec7_verbosity_sign.md:129-131 and Table 1 row A24b (sec1_introduction.md:69) call X4 "secondary". Add one sentence explaining that X4 is co-primary within the companion family but secondary to P50-A4 at the level of the paper (per the CC-159 placement).
- **m4.** Abstract length: the abstract paragraph (abstract_A.md:9) is 244 words by wc -w, above the ≤240 target in the file's own comment (abstract_A.md:3). The M3 edits must keep it within SPIC's limit; trim elsewhere, for example the LongCap clause.
- **m5.** Disclose in §7.4 or S7 the prereg §0 deviation: pascal50S.json was fetched once on the laptop for a structure-only refcheck before the commit (PREREG §0; RULE §0). The prereg discloses it, but the paper does not.
- **m6.** Reference panel note (sec7_verbosity_sign.md:88). It is unknown whether the 5 original UIUC captions are among the 50 PASCAL-50S references (RULE §0). Since §5 makes exchangeability (A1) a central assumption, state this in §7.4, and say that no adjacency check was registered for PASCAL-50S (PREREG §3.6, "no N2-type verdict check").
- **m7.** sec11_limitations_ethics.md:33 contains the placeholder "[AUTHOR TO CONFIRM: Polaris BSD; DOCCI-Critique CC BY 4.0]". Resolve it before submission.
- **m8.** The supplementary table of PASCAL-50S per-model slopes (supplementary.md) mixes vocabularies: refs1/refs50 on COCO-80, VOC labels on V20. A reader therefore cannot compare A4 part 2 per model. Label the columns clearly as different vocabularies, or say that refs50|V20 per model was not stored. Do not add new numbers computed from PASCAL outputs.
- **m9.** The 8-gram rule deleted all 14 PASCAL-50S caption files with no hash kept (sec11_limitations_ethics.md:34). Add one sentence on what the 8-gram overlap does and does not imply about pretraining exposure: such overlap can arise from generic phrases, and the share of captions that overlapped is unknown.
- **m10.** Highlight 1 (highlights_A.md:5), "follow gold completeness in two of three registered tests", is honest, but "tests" is ambiguous because G2B and XM3600 share images. Consider "on XM3600 with two backbones, not on PASCAL-50S".
- **m11.** File and section numbering do not match: sec10_discussion.md holds §9, sec11 holds §10, and sec9_preference_audit.md is an empty stub. This is harmless for the build but error-prone for revision pointers. Rename the files or add a map in outline.md.
- **m12.** sec3_measurement_setup.md:47 gives B = 5000 as the default, while P50 uses B = 1000 (PREREG §3.3). State the B for each registered test in the table captions (Table 7.2 and §7.4).

## Full report

Reviewer report: evaluation-metrics specialist (caption metrics, hallucination metrics, reference panels, benchmark validity). Every judgement below is AI opinion.

Manuscript: "More References, Larger Verbosity Reward: A Registered Audit of Object Hallucination Metrics Under Incomplete Gold", submitted to Signal Processing: Image Communication.

### 1. Summary of the submission

The paper argues that the verbosity reward of object F1 depends on how complete the gold is. That reward is the OLS slope of object F1 (in points) on ln M, the log number of mentioned objects, computed across a family of systems. The registered confirmatory claim is that the slope is ordered: one reference < all references < label gold. The authors test this on:

- 600 XM3600 images with Vietnamese references and human-verified OIV7 labels, using Qwen2.5-VL systems;
- a second backbone, Qwen3-VL-8B, on 537 of the same images;
- a new registered replication on PASCAL-50S (997 of 1,000 images, 50 references each, VOC2008 labels on 20 classes, seven public LVLMs).

On PASCAL-50S, the primary ordering test (P50-A4) FAILED at its label-gold step. The secondary tests passed:

- the rise at every added reference (P50-O2);
- a companion test (X4) showing that real one- and five-reference golds give a lower slope than a size-matched random-deletion null.

Further parts cover:

- per-image count-matched controls (all post hoc or not confirmatory);
- a reference-exchangeability diagnostic;
- human-judgment tests (mixed);
- a preference-data audit.

### 2. Verification performed

**Numbers against sources.**

- The XM3600 slopes −8.99 [−10.89, −6.99], −2.43 [−4.63, −0.30] and +19.32 [+17.43, +21.13], and the N1-XM-1..5 verdicts PASS/FAIL/PASS/PASS/FAIL, match .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json.
- G2B xm600 (n = 537): +5.89 [+4.76, +6.87] and +20.10 [+17.39, +23.05], both PASS, in data/results/g2b/g2b_score.json.
- The bracket lower bound on xm600, +1.97 [−0.44, +4.01], matches data/results/n_f1/bracket_result.json.
- The PASCAL-50S values match data/results/p50/p50_decide.json (sha256 0da4cab90fe9…, reproduced) and p50x_decide.json (75e152d266a4…, reproduced):
  - P50-A4: part 1 +37.16 [+35.07, +39.09] PASS; part 2 −2.29 [−5.15, +0.61] FAIL.
  - P50-O2: all five steps PASS.
  - X4: refs1 −31.38 against a null of [−14.97, −12.12], refs5 −20.99 against [−9.28, −6.87]; PASS after Holm.
  - X5: NOT_EVALUABLE (Σ|voc20| = 1,782 < 2 × 1,039.6).

**Registration timing.**

- git shows commit 353437f at 2026-10-29T00:49:49Z. It contains PREREG.md, RULE.md, p50.py, p50x.py and p50_job.sh.
- EVENTS records the first decode at 00:51:22Z.
- P50-A4, P50-O2 and X4 were therefore genuinely registered before the look. The §9.2 failure text was written before the look and is inserted verbatim.
- The numbers manifest has 131 P50 rows.

**Novelty searches.**

- I searched Crossref and arXiv. OpenAlex was over its daily budget and Semantic Scholar returned HTTP 429, so search coverage is partial.
- I found no prior work that varies the gold within one experiment as a factor for the sign of the object-F1 verbosity slope.
- I did find directly relevant work on object importance and reporting bias that the paper does not cite (Spain and Perona 2010; Berg et al. 2012; Misra et al. 2016).

### 3. Assessment by criterion

**NOVELTY: 3/5.** Treating the gold as an experimental factor for the verbosity reward of object-level scores is a useful framing. The size-matched random-deletion null on a 50-reference gold is a clean design. Novelty is limited in three ways:

- By the authors' own Section 4.2, the ordering of the reference rungs is expected under nesting even with random missingness.
- Non-uniform object naming, which X4 detects, is established in the object-importance and reporting-bias literature (M5).
- The count-control line is close to LeHaCE and CCEval, and it is not confirmatory.

The paper rightly avoids "first" claims.

**CORRECTNESS: 3/5.** Every number I traced matches its source. Registration timing checks out, failures are reported, and multiplicity follows the registrations. Three problems keep the score from being higher:

- A stale, contradictory statement in Limitations says the PASCAL-50S test was "registered, not run" (M1).
- The interpretive synthesis is missing. The risky, non-nested step of label gold over references holds only under the favourable verified-precision rule and fails on PASCAL-50S, where the labels are exhaustive. The paper never states these together (M2).
- An unmeasured completeness assumption sits behind A4 part 2 (M4), and system-level uncertainty on PASCAL-50S is not stated (M6).

**CONTRIBUTION: 3/5.** For SPIC, the practical message has real value for anyone who reports CHAIR or object F1: report the gold, the matcher and M. The checklist (§9.3) and the audit of counts in preference data are also useful. However, the confirmatory scientific claim rests on one Qwen family and 600 images, and it did not replicate at the label step on the one dataset with exhaustive labels. That bounds its generality.

**CLARITY: 2/5.** Individual sentences are precise, but the main text is overloaded with registration bookkeeping, internal codes and status qualifiers. The Introduction carries a ~40-row ledger, and no schematic figure explains the gold ladder (M7). A reader from image communication will struggle to extract the three findings.

### 4. The two questions put to this reviewer

**(a) Is X4 in the abstract acceptable?** In my AI opinion, yes. It is a registered companion test that survived Holm, the abstract labels it "registered secondary", and the wording "consistent with …" avoids a causal claim. Two changes are needed: O2 must also be labelled secondary, and the reading of X4 should acknowledge the prior reporting-bias work (M3, M5).

**(b) Is the A4 FAIL reported adequately?**

- In the body, yes. §7.4 inserts the preregistered failure branch verbatim, and Table 1 row A24, §9.1 and the Conclusion all carry it.
- In the abstract, not fully. The abstract never says that A4 was the primary PASCAL-50S test, and its "reported in full" list covers 3 of the 9 FAIL rows (M3).

The fix is a few words and keeps the PASS headline that the rules allow.

### 5. Recommendation

Major revision. The changes I request are textual: disclosures, synthesis, citations and restructuring. None needs new human labels or a second look at any test set.

I deliberately do not request any re-analysis of the PASCAL-50S outputs (leave-one-out, a matcher fix, per-model V20 ladders). That would be a second look, and the outputs were deleted under the registered data rule. These points should appear as stated limitations instead.

Major and minor issues are listed above, each with a file:line pointer and a concrete requested change.
