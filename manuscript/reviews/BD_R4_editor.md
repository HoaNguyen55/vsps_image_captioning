# Paper B+D review: R4, handling editor (Language Resources and Evaluation)

All judgements in this file are AI opinion (generated reviewer), not human peer review. Written 2026-10-29. No edits, commits or GPU use were made for this review.

Manuscript: "What Training-Data Gains Measure on a Vietnamese Captioning Benchmark: Two Reference Panels, a Validity Audit of KTVIC and an Open Evaluation Kit" (manuscript/journal_draft_B, merged B+D draft).

| Novelty | Correctness | Contribution | Clarity | Recommendation | Confidence |
|---|---|---|---|---|---|
| 3 | 3 | 3 | 2 | major revision | 4 |

## Summary (AI opinion)

The merged B+D manuscript makes three main claims, each reported carefully and with heavy hedging. (1) A KTVIC audit: single-writer references, a punctuation hazard in the scoring pipeline, segmentation sensitivity, matcher versions and image overlap. (2) A protocol card and an evaluation kit. (3) A development-only two-panel study of training-data gains: B-1 PASS +9.61 per doubling; D0 GO with gap +9.87; B-R1 ASYMMETRIC. Every D0, B-R1, matched and B-1 number I checked matches the decided JSONs, and the hashes in the text match the files. The failed final-system test is still reported in §1 and §5.1, and no positive transfer claim is made. The problems are in wording and design, not arithmetic. The abstract generalises the forward-direction result to both directions. The reverse null is written up as "no measurable gain" although that test was underpowered. The CIs ignore seed variance. All the two-panel evidence is repeated reuse of the same 187 dev images, with no held-out confirmation. Section 5.1 does not mention that an exploratory KTVIC-test look at MBR came before the registration. The manuscript reads as two papers, the novelty positioning misses English work on cross-style and cross-domain captioning, and the internal jargon is heavy. Recommendation: major revision.

## Major issues

- **M1.** The abstract generalises beyond the evidence and mixes two image sets (manuscript/journal_draft_B/outline_B.md:8). (a) 'Training-data gains thus register mainly on the panel whose captions were used for training' is stated for both directions. Only the KTVIC-trained direction supports it: D0 g = +9.87 [6.71, 13.35]. In the reverse direction g_R = +1.69 [-0.72, 3.91] (b_r1_decide.json primary.g_R_ci95), and the CI includes 0. B-R1 RULE.md §5 clause 5 itself defines ASYMMETRIC as an approximate-equivalence reading of the reverse direction. (b) '+9.61 [7.18, 12.36]' is on all 300 dev300 images (B-1 decide.json bootstrap.n_images = 300), while '+10.59 / +0.72' are on the 187-image subset. The phrase 'Scored on the same 187 images' suggests otherwise. Requested change: scope the sentence to KTVIC-trained adapters, for example 'Gains from more KTVIC captions register mainly on KTVIC's own references'. Name both image sets (300 and 187). Add the reverse gap g_R with its CI to the abstract.
- **M2.** The reverse-direction null is written up as a finding about KTVIC (sec8_conclusion.md:5 'the reverse direction shows no measurable gain on KTVIC references'; cover_letter_B.md:14 same wording; sec1_intro.md:16; sec6_discussion.md:21; outline_B.md:8). The other-panel slope is b_K^R = +1.29 [-1.23, 3.75]. Its upper bound exceeds the own-panel slope (+2.98). The stated pre-run MDE for this slope was 5.77 (RULE.md §5 power table). Without the length penalty it is +2.47 [-0.19, 5.19] (co_primary_sigma_inf.reverse.b_K_ci95). §5.5 (sec5_results.md:78) states this correctly ('cannot tell a KTVIC slope equal to the own-panel slope from a KTVIC slope of zero'), but the summary sentences drop it. Requested change: wherever the reverse KTVIC slope is summarised, say that it is not distinguishable from zero and not distinguishable from the own-panel slope (the design had low power for it). Delete 'no measurable gain' from the conclusion and the cover letter.
- **M3.** The CIs cover image sampling only, so training-run (seed) variance is left out, and this matters most in the reverse direction, which has two seeds (sec5_results.md:64, :74-76). The slopes are fixed-effects fits, and the bootstrap resamples images with the adapters held fixed. D0 reports per-seed slopes (d0_decide.json primary.per_seed_b_K/b_O); b_r1_decide.json reports none. Mean hypothesis syllables for r1_s43 are not monotone in N (17.41, 17.81, 16.24), which hints at run-to-run variation. Requested change (CPU only, no GPU, no new labels): report the per-seed reverse slopes and gaps from the existing outputs as a descriptive row. State in §5.4 and §5.5 that the CIs cover image sampling only. Alternatively, add a descriptive seed-and-image two-stage bootstrap, labelled post hoc.
- **M4.** The development evidence is reused, and nothing confirms it on held-out data (sec5_results.md:57, :64, :68, :74, :89). B-1, D0, the masked re-read, B-R1 and the matched-design row all score the same 15 forward adapters on the same 187 dev300 images. D0 is described as 'fixed before any of its scores were computed'. However, D0's KTVIC side reuses B-1 adapters whose KTVIC dev slope (+9.61 on 300 images) was already decided and pinned in D0 RULE.md §1. Given SESOI = 1.0, GO was close to certain unless b_O was near b_K, so b_O is the only informative half. B-1 itself replicates an earlier single-seed dev estimate (S5 +9.40, supplementary_B.md S7), which §5.4 does not say. Requested change: (i) in §5.4, say that the KTVIC slope was known before D0 and that D0's information is in b_O and the gap; (ii) say in §5.4 that B-1 confirms the S5 pilot; (iii) state in the abstract and §1 that the headline rests on development data under tiers 1-2 of the three-tier method, with no single held-out look, and that it is a hypothesis for confirmation. If the authors want confirmation, it should be a newly registered single look on data no adapter has been tuned or read on. Reusing KTVIC test is not allowed: it is closed.
- **M5.** Section 5.1 should list every KTVIC-test look related to MBR (sec5_results.md:25). The main text names only the registered B-F1 FAIL (-0.39 [-2.44, +1.67]) and 'a post hoc row computed after a later, disclosed lift of that closure'. The B-F1 registration itself records that an exploratory test-set MBR proxy over the three P1-R seeds, +3.05 [+1.03, +5.11], was seen before registration (manuscript/prereg/2026-10-20_b_f1_final_stack.md:71, :74, :91; commit d6cb2c7 on 2026-10-20). The supplement then reports a post hoc full-train row of +3.14 [+1.11, +5.16] (supplementary_B.md:289). The registered test used different members (P1-dev seeds), and its result was FAIL, so I see no bias toward a PASS. Under a one-look-per-test-set standard, however, a reader needs all three looks in the main text. Requested change: add one sentence to §5.1 listing (a) the exploratory proxy before registration, which was not used to choose the variant; (b) the registered look (FAIL); and (c) the post hoc row (no verdict). Also state that KTVIC test has been scored for about 79 systems in the ranking audit, so in this paper it supports audit and description, not method claims.
- **M6.** Framing and structure: the manuscript reads as two papers (outline_B.md:5, :8; sec1_intro.md:5, :9, :18-23; supplementary_B.md:5). The title and abstract now lead with 'what training-data gains measure', a development-only, single-backbone result in §5.4-5.5. §1:9 still says 'Our answer is a protocol card and an evaluation kit', and about 70% of the main text is the audit. The supplement header still says the main text reports only the audit, card and kit. For LRE, the editor needs one clear contribution statement. Requested change: choose one spine. Option (a): keep the training-gain headline, move the two-panel study directly after the data section, and present the audit findings as the explanation. Option (b): restore the audit-and-kit title and present §5.4-5.5 as one supporting study. Then align the title, abstract, §1 contributions, §8 and the supplement header with that choice.
- **M7.** The novelty positioning leaves out closely related English work, and the incremental nature of several audit items is understated (sec2_related.md:13-19, Table 2.1 at :21-32). Searches on arXiv returned prior work showing that captioners score much lower against the references of another style or domain (Chen et al. 2017, 'Show, Adapt and Tell', arXiv 1705.00930; Dessì et al. 2023, 'Cross-Domain Image Captioning with Discriminative Finetuning', arXiv 2304.01662). They also returned work showing that reference-based metrics reward the training-reference style (Kornblith et al. 2023, 'Guiding Image Captioning Models Toward More Specific Captions', arXiv 2307.16686). None of the three appears in paperB.bib. OpenAlex and Semantic Scholar were rate-limited during this review, so the search was not exhaustive. The authors should also check English same-image second caption sets as prior designs, for example nocaps and Localized Narratives on COCO/Flickr30k images. Several audit items are also incremental. The 401-image overlap was reported earlier by Tran et al. 2026. The exchangeability statistic is defined in the companion paper. The punctuation effect is a pipeline property: it vanishes under PTB-style removal. Sensitivity of Vietnamese CIDEr to segmentation is expected. Requested change: cite and discuss these works. State the novelty delta precisely: the same images, two human panels, a dose-response in both training directions, in a low-resource language. State that the qualitative effect (fine-tuning on one reference style raises scores against that style) is known. Make no 'first' claim.

## Minor issues

- **m1.** 'Validated' is used inconsistently. sec1_intro.md:21 ('meets the bar fixed in advance for calling the kit validated') and sec3_data_and_audit.md:80 ('so the kit is validated on external systems in the registered sense') keep the word. sec8_conclusion.md:7 and cover_letter_B.md:15 removed it on purpose. Use one wording throughout, preferably the sec8 one, which does not use 'validated'.
- **m2.** Priority wording attributed to other authors: sec1_intro.md:14 ('Tran et al. (2026) first reported'), sec2_related.md:9 ('were the first to report') and sec3_data_and_audit.md:64 ('were the first to report this count'). This priority cannot be verified exhaustively. Write 'reported' instead.
- **m3.** sec1_intro.md:14 still says 'nearly vanishes' for the fusion precision cost (−2.21 to −0.25 [−2.43, 1.96], one contrast at one seed), although that phrase was removed elsewhere. Replace it with the numbers or with 'is not distinguishable from zero on the second panel'.
- **m4.** outline_B.md:8: in 'No reference ends with a period, which costs 35.17 CIDEr-D points' the causal direction is unclear. Rephrase: 'appending a period to the outputs of a system that never punctuates costs 35.17 points in a pipeline without PTB punctuation removal, and nothing with it'.
- **m5.** Text that describes the process rather than the science should be cut: sec5_results.md:78 ('The scored file names this case only by its reason string. Its sub-label was added afterwards in the decision log...'), sec5_results.md:64 ('(D0)', 'D0 GO'), sec6_discussion.md:21 ('D0 GO'), and labels such as 'registered sense', 'kit_b' and 'O5b'. Use descriptive names, and move the provenance to the supplement.
- **m6.** sec5_results.md:80 uses test-image caption lengths (17.53 against 12.12 syllables) to describe the 187 dev images. d0_decide.json gives the dev values for the selected references (17.09 against 12.80). Use these.
- **m7.** CIDEr-D document frequencies are built for each panel from only 187 images (D0 RULE.md §3). Add one sentence on the resulting noisy IDF and on whether slopes are comparable across panels with different document frequencies. The log-scale companion helps with level differences, not with IDF differences.
- **m8.** sec5_results.md:57 says 'The gain is large and the same across seeds', and the abstract says 'the same slope across three seeds'. Write 'similar (9.50, 9.62, 9.71)'.
- **m9.** sec4_system.md:7 says 'Systems differ only in their training targets or loss mask'. The training-set-size adapters also differ in training images and set size, and they use the response-only mask on 3,469-image subsets. Say in §5.4 which Table 4.1 recipe they use.
- **m10.** Table 5.1 (sec5_results.md:11-16) mixes precisions (145.8 and 148.23; 54.6 and 55.44). Use two decimals throughout.
- **m11.** sec6_discussion.md:14 and sec8_conclusion.md:7 compare protocol-sensitivity magnitudes with the gap to GRIT's 136.0 under an unmatched protocol. That invites the leaderboard reading the paper disclaims. Make the comparison only in relative terms, or drop it.
- **m12.** Table 2.1 (sec2_related.md:29) records 'Training-data curve: no' for Bromonschenkel et al. (2026). The source comment says this rests on the abstract and a full-text read by an earlier agent. The arXiv abstract (2602.00393) does not mention a scaling curve, which agrees with the entry. The writer should still re-read the full text before relying on the table.
- **m13.** The supplement header (supplementary_B.md:5) and section map should mention §5.4-5.5 and the D-side registrations after the merge.
- **m14.** The main text runs to about 13.4k words, plus a 12.3k-word supplement. Check this against the LRE length guidance and the 25-page target mentioned in sec7 comments. The candidates for moving to the supplement are the provenance-heavy passages in §3.3 (baseline-output licensing), §3.6 (near-twin scans) and §5.5 (descriptive rows).

## Full report

Handling editor report: Language Resources and Evaluation (AI opinion; not expert-validated).

### 1. Summary of the submission

The paper uses a fixed Qwen2.5-VL-7B QLoRA fine-tune as the measuring instrument for an audit of the Vietnamese KTVIC captioning benchmark. It reports five findings about KTVIC:
- The five references of an image come from one writer (adjacent-slot share 0.7102 against 0.40 under exchangeability; 0.45 under a slot-rate-preserving null).
- No reference ends with a period. Under a word-segmenter pipeline without PTB punctuation removal, appending one period costs 35.17 CIDEr-D; with removal it costs nothing.
- Segmentation moves the score by 15.64 points.
- Object scores depend on an undocumented matcher.
- 401 of the 558 test images appear in UIT-OpenViIC's training split.

The paper releases a protocol card and a code-only kit, which the authors ran on three external checkpoints. After the merge, the headline is a development-only two-panel study:
- Each doubling of KTVIC training data raises dev CIDEr-D by +9.61 [7.18, 12.36] (registered PASS).
- On the 187 dev images that also have OpenViIC captions, the gain is +10.59 against KTVIC references and +0.72 [−0.83, 2.36] against OpenViIC (registered D0 GO; gap +9.87 [6.71, 13.35]).
- Adapters trained on OpenViIC captions gain +2.98 [0.94, 4.88] on their own panel and +1.29 [−1.23, 3.75] on KTVIC (registered outcome ASYMMETRIC).

### 2. Verification performed

I read the abstract and outline, §1-§8, the cover letter, the title page, the supplement header, the S7 section, the related-work table, the number-manifest rows for the D-side numbers and the bib key list. I checked the decided files directly:
- d0_decide.json: sha256 15dd925f…, as cited.
- b_r1_decide.json: a6627047…, as cited.
- b_r1_matched.json: fa58ab8c…, as cited.
- d0_reread.json: 7853ab4a….
- The B-1 decide.json: b44a76fe….
- The d_extrap result.

Every number quoted in §5.4-§5.5, §6.2, §8 and the abstract matches these files at the displayed precision. This covers:
- b_K, b_O, g and g_rel with their CIs;
- the L1/L5 means;
- mean k = 4.42;
- the 4-gram Jaccard of 0.019;
- the object slopes;
- the reverse slopes, gap, σ=∞ rows and style check (16.76 vs 11.73);
- the minus-twins rows, the crossover, the length slopes and the matched-design rows;
- the B-1 per-seed slopes (9.50, 9.62, 9.71) and the minus-2004 row;
- the extrapolation result: +1.93 [−6.65, +11.05], with all three forms INCONCLUSIVE.

I read both RULE.md files. The B-R1 rule fixes its outcome clauses, its SESOI (4.934 = 0.5·g from D0) and its power table before the run. The manuscript reports these faithfully.

Mandated checks:
- (a) The failed final-system test is still reported: in §1 ('the single pre-registered test of the final system failed (Section 5.1)', sec1_intro.md:25), in full in §5.1 (−0.39 [−2.44, +1.67], FAIL, sec5_results.md:25), and again in §7.1 and §8. Leaving it out of the abstract is acceptable.
- (b) No claim is made that OpenViIC-trained gains transfer to KTVIC references. §1:29 explicitly disclaims one. The one overreach goes the other way: the reverse null is presented as a finding (M2).

Related-work searches covered arXiv (several queries) and arXiv ID look-ups. OpenAlex and Semantic Scholar returned rate-limit errors, so the novelty search is incomplete; no personal e-mail was sent with any request. The arXiv abstract of Bromonschenkel et al. (2602.00393) agrees with how the paper describes it: cross-context training and testing on native vs translated Flickr30K captions, with no mention of a data-scaling curve.

### 3. Assessment by criterion

**NOVELTY: 3/5.** The most original element is the two-panel design. The same images are scored against two human caption panels, and a dose-response in training-set size is measured in both training directions, in a low-resource language. The closest prior design, Bromonschenkel et al. 2026, crosses native and machine-translated captions without a scaling curve, as the paper states. However:
- The qualitative effect, that fine-tuning on one reference style mainly raises scores against that style, is well known in English captioning: cross-domain captioning (Chen et al. 2017; Dessì et al. 2023) and the specificity analysis of Kornblith et al. 2023. None of these is cited.
- Several audit components are incremental. The 401-image overlap was reported earlier by Tran et al. 2026. The exchangeability statistic is defined in the companion paper. The punctuation effect is a pipeline property that disappears with PTB-style removal. Segmentation sensitivity is expected for Vietnamese.

The paper avoids priority claims about itself, but the novelty delta should be stated against the English literature (M7).

**CORRECTNESS: 3/5.** The numbers are reliable and traceable, and the hedging is unusually thorough. The deductions are for:
- the abstract generalising a forward-only result to both directions (M1);
- the reverse null being summarised as 'no measurable gain' when the test had low power for it (M2);
- CIs that ignore seed variance (M3);
- the KTVIC side of D0 having been known before D0 was 'fixed' (M4);
- §5.1 not listing the exploratory MBR test-set look made before registration (M5).

All of these can be fixed in the text or with CPU re-analyses. None needs GPU work or new labels.

**CONTRIBUTION: 3/5.** For LRE, the protocol card, the documented punctuation and segmentation hazards, the overlap disclosure and an open audit kit are useful practical resources for Vietnamese captioning evaluation. The two-panel result is an informative warning that KTVIC gains largely measure agreement with one writer. However, it is development-only, uses one backbone, and confounds writer with protocol (as the authors acknowledge). The kit has so far been run only by its authors.

**CLARITY: 2/5.** The prose is careful but dense. The manuscript reads as two papers with different spines (M6). Internal labels ('D0 GO', 'registered sense', 'O5b', 'kit_b', 'fuse2', 'P1-R') and passages about provenance and procedure in the main text make it hard to follow. Figures 5.1 and 5.2 help, and §5.4-5.5 should lean on them more.

### 4. Constraints the revision must keep

- No new human gold labels; AI-generated signals are not evidence.
- No further KTVIC-test look. Any confirmation of the two-panel finding must be a newly registered single look on unseen data, after the dev-explore and dev-confirm rehearsal stages.
- The registered FAILs stay in the text.
- No caption text from OpenViIC, KTVIC or UIT-ViIC in repository files.
- No 'first' claims.

### 5. Recommendation

Major revision. The empirical core is sound and transparently documented. The required changes are mostly about scoping and framing, plus two or three descriptive CPU re-analyses. Once M1-M3 are fixed and the paper commits to one framing (M6), I expect it to be within scope and of interest to LRE readers working on low-resource evaluation resources.

(All judgements above are AI opinion.)
