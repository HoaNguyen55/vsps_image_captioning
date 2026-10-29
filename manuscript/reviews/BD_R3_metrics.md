# Paper B+D review: R3, evaluation-metrics specialist (Language Resources and Evaluation)

All judgements in this file are AI opinion (generated reviewer), not human peer review. Written 2026-10-29. No edits, commits or GPU use were made for this review.

Manuscript: "What Training-Data Gains Measure on a Vietnamese Captioning Benchmark: Two Reference Panels, a Validity Audit of KTVIC and an Open Evaluation Kit".

| Novelty | Correctness | Contribution | Clarity | Recommendation | Confidence |
|---|---|---|---|---|---|
| 3 | 3 | 3 | 3 | major revision | 4 |

Area-chair note (2026-10-29): this report states that the paper "makes no unverified 'first' claims" about the 401-image overlap. That is not correct: 'first reported' / 'were the first to report' appears at sec1_intro.md:14, sec2_related.md:9, sec3_data_and_audit.md:64 and cover_letter_B.md:13 (checked by grep). R1, R2 and R4 flag it. The per-seed reverse slopes quoted below were derived by this reviewer from figs/fig_values_B.json; they are not in any decided file and must be recomputed and logged as post hoc before they enter the paper.

## Summary (AI opinion)

This is the merged B+D LRE manuscript: an audit of KTVIC (single writer, punctuation, segmentation, matcher, image overlap), a protocol card and kit, and dev-only two-panel training-data studies (B-1 PASS +9.61; D0 GO with gap +9.87; B-R1 ASYMMETRIC). Every two-panel number I checked matches the decided files byte for byte (d0_decide 15dd925f, b_r1_decide a6627047, b_r1_matched fa58ab8c, d0_reread 7853ab4a, B-1 decide b44a76fe, rules 72345e1c/e7c50fbc). The failed final-system test is still reported in §1:25, §5.1:25, §7.1:9 and §8:9. The forward finding is solid and stable across seeds. The reverse-direction reading is overstated in the abstract, conclusion and cover letter. Per-seed reverse slopes I derived from figs/fig_values_B.json show that "not distinguishable from zero" rests on seed 42 alone: b_K^R is −1.37 on seed 42 and +3.94 on seed 43. Seed variance is absent from every two-panel CI. Prior-art positioning lacks Freitag et al. 2020. Recommendation: major revision. Most fixes are wording plus CPU-only descriptive checks on existing predictions.

## Major issues

- **M1.** The reverse direction is generalised into a symmetric claim. outline_B.md:8 says 'Training-data gains thus register mainly on the panel whose captions were used for training', but the reverse own-minus-other gap is g_R = +1.69 [−0.72, 3.91] (b_r1_decide.json primary.g_R_ci95), so only the forward direction supports the claim. The registered meaning of ASYMMETRIC (b_r1 RULE.md:131-134) is an equivalence reading: OpenViIC-trained adapters gain on KTVIC references about as much as on OpenViIC references. That is the opposite emphasis. Requested change: restrict the sentence to 'KTVIC training-data gains register mainly on KTVIC's own references' at outline_B.md:8, sec1_intro.md:16 and sec6_discussion.md:21, and reuse §5.5's own wording ('whether OpenViIC-trained gains also reach KTVIC references is not established', sec5_results.md:80).
- **M2.** The text makes a negative transfer claim the test cannot support. cover_letter_B.md:14 and sec8_conclusion.md:5 say 'the reverse direction shows no measurable gain on KTVIC references'. The evidence: b_K^R = +1.29 [−1.23, 3.75]; without the length penalty it is +2.47 [−0.19, 5.19] (b_r1_decide.json co_primary_sigma_inf.reverse); the pre-run MDE80 for b_K was 5.77, larger than the own-panel slope of 2.98 (RULE.md §5 power table); and the per-seed reverse slopes (my derivation from figs/fig_values_B.json, descriptive) are b_K^R = −1.37 (seed 42) and +3.94 (seed 43) against b_O^R = 2.16 and 3.80. On seed 43 the two panels gain equally. Requested change: replace the sentence with 'the reverse gain against KTVIC references is +1.29 [−1.23, 3.75], not distinguishable from zero and not shown to be absent', and add the per-seed reverse slopes to §5.5.
- **M3.** Seed and training-run variance is missing from every two-panel CI. The D0 and B-R1 CIs resample images only, with the adapters fixed (d0 RULE.md:70-72, b_r1 RULE.md:86-87), and the nested training subsets are one draw of one order. Forward per-seed slopes are tight (b_K 9.94/10.77/11.05; gaps 9.13/9.95/10.53), so D0 survives. The reverse per-seed gaps are +3.53 and −0.14, so the B-R1 CI understates uncertainty a great deal. Requested change: in sec5_results.md:64 and :74, state that the CIs are conditional on the trained adapters and the subset draw. Report per-seed slopes and gaps for both directions, plus a descriptive seed-level interval like B-1's t_interval_95, labelled post hoc. With two reverse seeds, say plainly that the reverse direction cannot estimate seed variance. No GPU is needed.
- **M4.** The D0 pre-specification is only partial on the KTVIC side. sec5_results.md:64 says the comparison 'was fixed before any of its scores were computed'. But the 15 adapters' dev300 CIDEr-D against KTVIC references was already decided and known from B-1 (b_K on 300 images, PASS +9.61), and D0's reproduction gate re-reads it (d0 RULE.md:111-113). Only the OpenViIC-panel side was unseen. Requested change: add one sentence saying that the KTVIC-panel slope was predictable from the decided B-1 result, that the new information in D0 is b_O and the gap, and that D0 is a dev-explore study in the three-tier sense with no dev-confirm or test tier.
- **M5.** Headline wording conflicts with the paper's own finding. outline_B.md:8 says 'more KTVIC training data reliably improves a fine-tuned Qwen2.5-VL-7B model', and sec1_intro.md:5 says 'improves the system reliably'. D0 shows the gain is mainly agreement with KTVIC references (+0.72 [−0.83, 2.36] on the second panel), and the registered extrapolation test was INCONCLUSIVE (sec5_results.md:57). Requested change: write 'raises CIDEr-D against KTVIC references by +9.61 [7.18, 12.36] per doubling (development data, one backbone)', and drop 'reliably' and 'improves the model'.
- **M6.** The metric dependence of the slope comparison is untested. Each panel has its own CIDEr-D document frequencies, built from only 187 images (d0 RULE.md:56-57), and the panels differ in level (about 102-147 vs about 50-67), length (12.8 vs 17.1 syllables), k (mean 4.42) and n-gram homogeneity (bigram Jaccard 0.18 vs 0.08). The log-scale g_rel and the sigma=inf row help, but the claim 'gains register on panel X' is shown for one consensus metric whose IDF weighting rewards homogeneous panels by construction. Requested change: add a post hoc, descriptive, dev-only row in §5.4/§5.5 that recomputes the forward and reverse gaps with metrics that do not use per-panel IDF (BLEU-4, ROUGE-L, chrF, and CIDEr-D with df pooled over both panels). This is CPU-only on existing dev predictions, and the decided verdicts stay unchanged. State the 187-image per-panel df in the main text at sec5_results.md:64; it is currently only in RULE.md.
- **M7.** Novelty positioning is missing key prior art and overstates the design's novelty. Freitag, Grangier and Caswell (2020), 'BLEU might be Guilty but References are not Innocent' (EMNLP; doi 10.18653/v1/2020.emnlp-main.5, verified on Crossref), shows that the reference set's style drives metric scores and system rankings. It is not in paperB.bib. Multi30K (Elliott et al., 2016) provides two independently produced caption sets for the same images. Kornblith et al. 2023 (arXiv 2307.16686) shows that reference-based captioning metrics penalise departures from the reference style. Bromonschenkel et al. (2026), already in Table 2.1 (sec2_related.md:29), already uses the train-on-one-panel, test-on-the-other design on the same images. Requested change: cite Freitag 2020 (plus Multi30K/Kornblith where relevant), and state in sec2_related.md:21-32 and sec1_intro.md:23 that the contribution is the training-set-size curve in both directions in a Vietnamese low-resource setting, not the two-panel design itself.

## Minor issues

- **m1.** The paper has two competing headlines. sec1_intro.md:5 calls the training-data gain the 'main finding', while sec1_intro.md:9 says 'Our answer is a protocol card and an evaluation kit', and the contributions list (sec1:20-23) puts the two-panel test last. Pick one thesis consistent with the new title and order the contributions to match.
- **m2.** The section title in sec5_results.md:1, 'The audit applied to the controlled system', does not cover §5.4-5.5. Retitle, or split §5.4-5.5 into their own section.
- **m3.** The CIDEr-D gain evidence is discussed under sec6_discussion.md:21, '§6.2 Object scores need count control…'. Give it its own subsection, e.g. '6.x What a training-data gain on KTVIC measures'.
- **m4.** The protocol card at sec4_system.md:37 (P0: no punctuation removed) differs from the dev two-panel scorer, which strips trailing punctuation tokens from hypotheses (scripts/b_d0/d0.py:203; d0 RULE.md:25). State the dev scorer's protocol in sec5_results.md:64. My check: 0% of KTVIC train (18,845) and OpenViIC train (41,238) captions end with a period, so this is not a confound, but it must be declared.
- **m5.** Table 4.1 (sec4_system.md:9-16) has no rows for the B-1 and B-R1 adapters (first caption, 3,469-image pool, assistant-only loss, k=1 OpenViIC caption for reverse). Add them.
- **m6.** The abstract gives +10.59 without its CI (outline_B.md:8). Add [7.43, 13.81], or drop the number and keep the gap +9.87 [6.71, 13.35].
- **m7.** sec5_results.md:57 gives 'Object F1 against KTVIC gold rises by +1.19' without naming the matcher. Name it (B-1 exact matcher vs v2), since §5.4:70 shows v2 has no slope.
- **m8.** sec5_results.md:57 reports 'registered verdict PASS', but the decided outcome label is FUND_EXTERNAL_IMAGE_DATA (b1 decide.json P-B1.outcome). Mention the registered outcome name or explain the mapping.
- **m9.** The UIT-OpenViIC citation is inconsistent: Bui et al. 2026 (sec1_intro.md:5, sec3:84) vs 2023 (sec1:7, sec2_related.md:5,19,26). paperB.bib:36 and :48 hold both the preprint and the journal entry. Cite the journal version throughout.
- **m10.** Wrong cross-reference: sec3_data_and_audit.md:11 says 'in-domain replication (Section 5.3)'; it is §5.2.
- **m11.** Typo: sec2_related.md:5 is missing a period after '(exposure caveat: Section 3.1)'.
- **m12.** sec1_intro.md:12 and sec3_data_and_audit.md:34 say 'Vietnamese pipelines replace [the PTB tokenizer] … and drop that removal' without a source, while the paper itself says the public KTVIC baseline code uses PTB. Either cite the pipelines that do this or rephrase as 'a pipeline that replaces…'.
- **m13.** sec3_data_and_audit.md:86 says no 'ID lists' are released, but the kit ships pre-registration files that list the 187 dev300 ids (d0 RULE.md:34-43) and r1_lists.json. Reconcile the statement.
- **m14.** The supplement section map (supplementary_B.md:7) does not list B-1, D-α, D0 and B-R1 with their verdicts. Add them so that every registered result has one verdict line.
- **m15.** Readability: §5.4-5.5 carry many procedural details (hash rules, id-set hashes, k rule) and symbol-heavy notation (b_O^R, g_R). Move the procedure to a supplement subsection and keep in the main text one table: per direction, own/other slope, gap, log-scale gap, sigma=inf gap, and per-seed values.
- **m16.** Figure 5.2 uses blue/orange only. Add marker shapes for the panels so it reads in greyscale, and give CIs or per-seed lines in the legend.
- **m17.** The main text runs about 13,500 words plus a supplement of about 117 KB. LRE has no strict limit, but trimming §3 (3,876 words) and §5.3 would help the merged narrative.

## Full report

REVIEW REPORT. Language Resources and Evaluation. Reviewer role: evaluation-metrics specialist. All judgements below are AI opinion, not expert-validated.

### 1. Summary of the submission

The paper has three parts:
- An audit of KTVIC as a measuring instrument:
  - single-writer references (adjacent-slot share 0.7102 vs 0.40 under exchangeability);
  - the absence of sentence-final punctuation and its pipeline-dependent cost (−35.17 CIDEr-D under P0, 0 with PTB-style removal);
  - segmentation sensitivity (15.64);
  - three matcher versions;
  - image overlap with UIT-OpenViIC (401/558 in its train split).
- A protocol card and an open evaluation kit.
- From the B+D merge, development-only studies of what a training-set-size gain measures:
  - B-1: +9.61 [7.18, 12.36] CIDEr-D per doubling (PASS).
  - D0: on 187 dev images, +10.59 against KTVIC references vs +0.72 [−0.83, 2.36] against an OpenViIC panel; gap +9.87 [6.71, 13.35]; GO.
  - B-R1 (reverse, OpenViIC-caption training): own-panel slope +2.98 [0.94, 4.88], KTVIC slope +1.29 [−1.23, 3.75], gap +1.69 [−0.72, 3.91]; ASYMMETRIC.

### 2. Verification performed

- Decided files. I re-read d0_decide.json, b_r1_decide.json, b_r1_matched.json, d0_reread.json, the B-1 decide.json and both RULE.md files. All sha256 prefixes cited in the manuscript match: 15dd925f, a6627047, fa58ab8c, 7853ab4a, b44a76fe, 72345e1c, e7c50fbc and ee91c152.
- Values. Every value I checked in §5.4-5.5 and the abstract matches its source at the displayed precision:
  - B-1: 9.61 [7.18, 12.36]; per-seed slopes 9.50/9.62/9.71; minus-2004 9.61 [7.17, 12.37].
  - D0: b_K 10.59 [7.43, 13.81]; b_O 0.72 [−0.83, 2.36]; g 9.87 [6.71, 13.35]; g_rel 7.11% [3.54, 10.69]; level ranges; object slopes; mean k 4.42; 4-gram Jaccard 0.019.
  - Masked re-read: 8.92 [5.59, 12.40], n = 165.
  - B-R1: 2.98, 1.29, 1.69 and CIs; sigma=inf rows; style check 16.76 vs 11.73; asymmetry 8.18; matched-design 11.77 and 10.08; minus-twins rows; crossover 76.09; forward-recomputed CI [6.63, 13.43].
- The registered final-system FAIL (−0.39 [−2.44, +1.67]) is still reported in sec1_intro.md:25, sec5_results.md:25, sec7:9 and sec8:9. A PASS headline in the abstract is acceptable.
- Transfer claims. None of the text says that OpenViIC-trained gains reach KTVIC references. However, a negative transfer claim ('no measurable gain') appears in the cover letter and the conclusion (M2).
- Punctuation as a confound. The dev scorer strips trailing punctuation from hypotheses. I counted (counts only, no text printed) that 0% of KTVIC train (18,845) and of OpenViIC train (41,238) captions end with a period, so punctuation does not confound the two-panel comparison.
- Literature search. OpenAlex and Semantic Scholar returned rate-limit errors, so the prior-art check used Crossref and the arXiv API only. No e-mail address was sent to any service. Freitag et al. 2020 was verified on Crossref and Kornblith et al. 2023 on arXiv (2307.16686). Multi30K is cited from reviewer knowledge and was not re-verified in this session.

### 3. Assessment by criterion

**NOVELTY: 3/5.** The KTVIC audit is a useful, specific resource contribution: the single-writer exchangeability statistic, the pipeline-dependent punctuation hazard and the overlap disclosure. The 401-image overlap is correctly credited to Tran et al. (2026), and the paper makes no unverified 'first' claims [area-chair note: incorrect, see top]. The two-panel training study is the newest part. Its design (train on one human panel, score on another written for the same images) is anticipated by Bromonschenkel et al. (2026), whom the authors cite. The idea that reference style drives metric scores and rankings is established in MT (Freitag et al., 2020, missing) and in captioning (Kornblith et al., 2023; Multi30K's two caption sets). What is new is the training-set-size curve in both directions, in a low-resource Vietnamese setting. That is a moderate step and should be stated that way.

**CORRECTNESS: 3/5.** The numbers trace to their sources, the statistics are pre-specified, and the post hoc rows are labelled. The problems lie in inference and framing:
- (a) The abstract's 'thus' sentence generalises a forward-only result to both directions. The reverse gap's CI includes zero, and the registered ASYMMETRIC outcome is defined as an equivalence reading, i.e. similar reverse gains on both panels (M1).
- (b) The cover letter and conclusion say the reverse direction shows 'no measurable gain' on KTVIC references, a claim of absence that the pre-run MDE and the per-seed data contradict. My descriptive per-seed fit from figs/fig_values_B.json gives b_K^R = −1.37 on seed 42 and +3.94 on seed 43, against b_O^R of 2.16 and 3.80 (M2).
- (c) The CIs resample images only, so seed and subset variance is omitted. This is harmless forward (per-seed gaps 9.13 to 10.53) but material in reverse (per-seed gaps +3.53 and −0.14) (M3).
- (d) 'Fixed before any of its scores were computed' overstates D0's blindness, because the KTVIC-panel side was predictable from the decided B-1 result (M4).
- (e) 'Reliably improves the model' contradicts the paper's own finding that the gain is mostly agreement with KTVIC references (M5).
- (f) Only one IDF-weighted consensus metric with per-panel df on 187 images is tested, so it is open whether the panel-specific gain partly reflects how CIDEr rewards homogeneous panels (M6).

The forward D0 finding is robust: it survives the masked re-read, the minus-twins row, the matched design and the length-penalty-free variant.

**CONTRIBUTION: 3/5.** LRE is a good fit: a dataset audit, a reporting standard and a released kit for an under-resourced language. The practical recommendations (§6.3) are sound, and the warning that a KTVIC gain is first a gain in agreement with one writer's references is useful to the community. The contribution is limited by:
- one backbone;
- the dev-only status of the merged study, with no dev-confirm or test tier;
- the absence of any external use of the kit (acknowledged);
- the fact that the punctuation hazard applies only to pipelines that drop PTB punctuation removal, and the paper does not show that published Vietnamese pipelines do (m12).

**CLARITY: 3/5.** Writing is precise and hedged, and the numbers are traceable. After the merge the paper reads as two papers:
- the introduction names two different main answers (m1);
- the §5 title and §6.2 do not fit the new material (m2, m3);
- §5.4-5.5 are heavy with procedure and notation (m15);
- Table 4.1 lacks the adapters the headline rests on (m5);
- there are several small inconsistencies: the citation year (m9), the wrong cross-reference (m10), a typo (m11) and the 'ID lists' statement (m13).

Figures 5.1-5.2 help but should encode the panels redundantly (m16).

### 4. Recommendation: MAJOR REVISION (AI opinion)

The forward headline stands on the evidence. The required changes are:
- align every reverse-direction statement with §5.5's careful wording;
- add per-seed and seed-level uncertainty;
- disclose D0's partial blindness;
- add a CPU-only, post hoc, descriptive metric-robustness row;
- reposition novelty against Freitag 2020 and Bromonschenkel 2026.

None of these needs new human labels, GPU time or a further test-set look. All new rows must be labelled POST_HOC/DESCRIPTIVE/DEV, and the registered verdicts (B-1 PASS, D-α INCONCLUSIVE, D0 GO, B-R1 ASYMMETRIC, final test FAIL) stay unchanged and reported.

Relevant paths:
- /mnt/d/vsps_image_captioning/manuscript/journal_draft_B/ (outline_B.md, sec1-8, supplementary_B.md, cover_letter_B.md, paperB.bib, figs/fig_values_B.json)
- /mnt/d/vsps_image_captioning/manuscript/prereg/2026-10-29_b_d0/{RULE.md, d0_decide.json}
- /mnt/d/vsps_image_captioning/manuscript/prereg/2026-10-29_b_r1/{RULE.md, b_r1_decide.json, b_r1_matched.json, d0_reread.json}
