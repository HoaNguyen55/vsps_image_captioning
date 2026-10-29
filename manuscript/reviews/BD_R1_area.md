# Paper B+D review: R1, senior area expert (Language Resources and Evaluation)

All judgements in this file are AI opinion (generated reviewer), not human peer review. Written 2026-10-29. No edits, commits or GPU use were made for this review.

Manuscript: "What Training-Data Gains Measure on a Vietnamese Captioning Benchmark: Two Reference Panels, a Validity Audit of KTVIC and an Open Evaluation Kit" (merged B+D draft, manuscript/journal_draft_B).

| Novelty | Correctness | Contribution | Clarity | Recommendation | Confidence |
|---|---|---|---|---|---|
| 3 | 4 | 3 | 3 | major revision | 4 |

## Summary (AI opinion)

A merged resource-and-evaluation paper: an audit of KTVIC (single-writer references, punctuation hazard, segmentation sensitivity, matcher versions, image overlap with UIT-OpenViIC), a protocol card, an open evaluation kit, and new development-only two-panel studies of training-set-size gains (B-1 PASS +9.61 [7.18, 12.36]; D0 GO, gap +9.87 [6.71, 13.35]; B-R1 ASYMMETRIC). Every D0, B-R1, matched-design, re-read and B-1 number I checked matches its decided JSON exactly, and every cited SHA-256 prefix matches the file on disk. The required checks pass: the registered final-system FAIL is still in §1 and in full in §5.1, and no OpenViIC→KTVIC transfer claim is made. The main problems are in the wording. Some abstract, conclusion and cover-letter sentences go beyond the reverse-direction evidence. One CI is described as "more than half" although its lower bound is below 50%. Several statements went stale after the merge. Related work misses close same-image, two-panel precedents (Multi30K, COCO-CN, van Miltenburg et al. 2017, Frank et al. 2018, Yi et al. 2020). The title and headline rest on development-only evidence from 187 images and one backbone.

## Major issues

- **M1 (AI opinion)** The abstract generalises the two-panel result beyond the reverse-direction evidence. outline_B.md:8 says 'Training-data gains thus register mainly on the panel whose captions were used for training.' Forward this holds: g = +9.87 [6.71, 13.35] (d0_decide.json primary.g). In reverse, the own-minus-other gap g_R = +1.69 [-0.72, 3.91] and +2.64% [-1.38, 6.28] on the log scale (b_r1_decide.json primary.g_R, g_rel_R_ci95); both include 0. The abstract also reports only that the reverse KTVIC slope is 'not distinguishable from zero' and leaves out that the reverse gap is not distinguishable either. Requested change: scope the sentence to KTVIC-trained gains, e.g. 'Gains from KTVIC training data register mainly on KTVIC's own references; in the reverse direction the OpenViIC panel registers a smaller gain (+2.98), and the reverse own-minus-other gap is not distinguishable from zero.' Make the same change in sec6_discussion.md:21 if needed.
- **M2 (AI opinion)** Absence of evidence is stated as evidence of absence. sec8_conclusion.md:5 and cover_letter_B.md:14 say the reverse direction 'shows no measurable gain on KTVIC references'. The decided value is b_K^R = +1.29 [-1.23, 3.75]. Without the length penalty it is +2.47 [-0.19, 5.19] (b_r1_decide.json co_primary_sigma_inf.reverse). §5.5 itself (sec5_results.md:78) concedes that the 4.93 margin cannot tell this slope from the own-panel slope. Requested change: replace with 'their gain against KTVIC references is not distinguishable from zero (+1.29 [-1.23, 3.75]); whether it reaches KTVIC references is not established', as §5.5 already words it.
- **M3 (AI opinion)** The title and headline rest on development-only, single-backbone evidence. title_page_B.md:5 and sec1_intro.md:5 make 'what training-data gains measure' the headline, but D0 and B-R1 use 187 dev300 images, one backbone and two reverse seeds. B-1 confirms a prior single-seed dev observation (+9.40; supplementary_B.md:286), and its PASS bar (CI_lo > +1) was low given that observation. The test-set panel (555 images) is closed, so the finding cannot be confirmed in this paper under the one-look rule. Requested change: (a) put 'development data' or 'a development study' into the title or subtitle, or make the audit and kit the title lead with the two-panel study as a subtitle; (b) say in sec5_results.md:57 that B-1 is the registered three-seed confirmation of an earlier single-seed dev result (S6, +9.40) and that its PASS threshold was set below that result; (c) in §8 and the abstract, state that confirmation on the test panel is left to a future single registered look.
- **M4 (AI opinion)** Related work and Table 2.1 omit close prior work on same-image, multi-panel captions, so the novelty positioning is incomplete. sec2_related.md:19 and Table 2.1 (sec2_related.md:21-32) list Bromonschenkel et al. (2026) as the closest study. I verified these omitted works on Crossref: Multi30K (Elliott et al., 2016, doi 10.18653/v1/W16-3210), with independent German descriptions and translations of the same Flickr30K images; van Miltenburg et al. (2017, doi 10.18653/v1/W17-3503), cross-linguistic descriptions of the same images; Frank, Elliott and Specia (2018, NLE, doi 10.1017/S1351324918000074); COCO-CN (Li et al., 2019, IEEE TMM, doi 10.1109/TMM.2019.2896494), with human-written and machine-translated captions of the same COCO images used for training and testing; Yi et al. (2020, ACL, doi 10.18653/v1/2020.acl-main.93), on inter-reference variance in caption evaluation. Chen et al. (2017, Show, Adapt and Tell) on dataset-specific caption style across domains is also relevant. Requested change: discuss these in §2 and add rows to Table 2.1. The distinctive element appears to be a training-set-size slope against two same-language human panels in both training directions; state that narrowly. The paper correctly makes no 'first' claim for it; keep it that way.
- **M5 (AI opinion)** The single-writer statistic is mis-described. sec5_results.md:45 quotes 55.12% [49.38, 61.05] and then says 'More than half of what KTVIC scores as hallucinated ... is in another panel's captions'. sec6_discussion.md:21 and sec8_conclusion.md:5 repeat 'more than half'. The CI lower bound is below 50%, so 'more than half' is not supported at the 95% level. Requested change: say 'about half (55.12% [49.38, 61.05]; one contrast, one seed)' in all three places.
- **M6 (AI opinion)** A known alternative mechanism for D0 is missing. sec5_results.md:80 offers reference homogeneity as the hypothesis, and sec3_data_and_audit.md:19 notes that KTVIC has three annotators in total. Training captions and dev300 references were therefore written by the same small pool, which is exactly the annotator-recognition setting of Geva et al. (2019, already cited at sec2_related.md:19). Requested change: name annotator-identity learning beside homogeneity as an equally live, untested explanation. If per-image annotator IDs are recoverable from the released data, describe (do not run as a new test) how a writer-held-out split would separate the two. Run no new labelling.
- **M7 (AI opinion)** The protocol card does not describe the protocol behind the paper's new headline. Table 4.2 (sec4_system.md:32-42) specifies the 558-image test protocol only. D0 and B-R1 score 187 dev images with k = min(5, available) references per panel (mean 4.42) and CIDEr-D IDF computed over a small, panel-specific reference set, so the two panels are scored with different IDF tables. Requested change: add a 'two-panel dev' column or note to Table 4.2 (images, k rule, IDF corpus, sigma for the co-primary). State in §5.4 whether IDF is computed per panel over the 187 images and why slopes are comparable across panels. An IDF sensitivity on the existing dev outputs is optional, CPU-only and labelled post hoc.
- **M8 (AI opinion)** Statements made stale by the merge now contradict §5.4-5.5. sec4_system.md:20 says only the supplement's levers and final test used the dev300 carve and that the protocol findings come from 3,769-image systems; §5.4-5.5 now use dev300 and 3,469-image nested subsets. sec3_data_and_audit.md:66 says the leakage test 'could not be evaluated, because no OpenViIC-trained run exists'; six OpenViIC-trained dev adapters now exist (sec3_data_and_audit.md:66 itself and §5.5). Requested change: update both sentences. In sec3 say that the six adapters are dev-only and never decoded on a test split, so the registered leakage test is still not evaluable.

## Minor issues

- **m1** sec1_intro.md:14 still says the precision cost 'nearly vanishes' against the second panel. The edit log in outline_B.md:15 says this phrase was removed after CC-126 W3. The panel CI, -0.25 [-2.43, 1.96], contains KTVIC's -2.21 (sec5_results.md:45). Replace with 'is smaller and not distinguishable from zero against the second panel (one contrast, one seed)'.
- **m2** Unverified priority wording: 'first reported' / 'were the first to report' the 401-image overlap (sec1_intro.md:14, sec2_related.md:9, sec3_data_and_audit.md:64, cover_letter_B.md:13). Unless it is shown that no earlier source, including Bui et al. (2023), reported the overlap, write 'reported by Tran et al. (2026)'.
- **m3** outline_B.md:8 says the model 'reliably improves'. What is measured is a rise in KTVIC dev CIDEr-D, which is the very thing the paper questions. Write 'raises its KTVIC CIDEr-D'.
- **m4** outline_B.md:8: 'Scored on the same 187 images' has no antecedent, since the previous sentence is about dev300 (300 images). Write 'On the 187 development images that also have UIT-OpenViIC captions'.
- **m5** sec3_data_and_audit.md:11 points the UIT-ViIC in-domain replication to Section 5.3. It is in Section 5.2 (sec5_results.md:33). Fix the cross-reference.
- **m6** The CIs in §5.4-5.5 are image-bootstrap only, with seeds as fixed effects, so training randomness is not propagated. B-R1's RULE (lines 75-77) argues that the image bootstrap dominates. State this in one sentence in §5.4 with the per-seed spread (forward 9.94-11.05 for b_K; d0_decide.json primary.per_seed_b_K).
- **m7** The smallest gap of interest (4.93 = 0.5 x the D0 point estimate) depends on the data. Say so where ASYMMETRIC is introduced (sec5_results.md:78), so readers do not take 'ASYMMETRIC' as a registered equivalence result with an a-priori margin.
- **m8** sec6_discussion.md:9 attributes the 28.98 -> 140s rise to 'template match'. That rise mixes task adaptation with template match. Say so, or attribute only the period-strip part (28.98 -> 33.30).
- **m9** The internal labels 'O5b', 'D0', 'B-R1' and 'P1 SESOI' leak into prose and the manifest (sec5_results.md:78 mentions a sub-label added in a decision log). Explain once, plainly, that the outcome sub-label was added after scoring as a recorded deviation, and drop internal codes from the reader-facing text.
- **m10** The §5.2 heading 'Transfer to UIT-ViIC' (sec5_results.md:29) is about scoring KTVIC-trained models on UIT-ViIC cross-dataset. It is not the banned claim that OpenViIC-trained gains transfer to KTVIC references. Keep it, but consider 'Cross-dataset scoring on UIT-ViIC' so it is not read near §5.5.
- **m11** Clarity: the main text is dense with hedges, post hoc rows and parenthetical provenance. Moving the descriptive rows in §5.5 (sec5_results.md:82-94) to a table, and keeping only the matched-design row and the length-penalty co-primary in prose, would make §5.5 much easier to read. Figures 5.1 and 5.2 are useful; label in Fig. 5.2 that the reverse direction uses three sizes and two seeds.
- **m12** The cover letter is dated 'draft 2026-10-21' (cover_letter_B.md:1) but describes the 10-29 merge. Its line 27 says the dataset authors confirmed use in writing, while outline_B.md:72 still lists the dataset terms as [AUTHOR TO PROVIDE]. Reconcile them before submission.
- **m13** sec7_limitations_ethics.md:16 is a good limitations paragraph. Add the annotator-identity alternative (M6) and the data-dependent margin (m7) there, too.

## Full report

Review for Language Resources and Evaluation. All judgements below are the reviewer's AI opinion.

### 1. Summary

The paper audits KTVIC, the main Vietnamese image-captioning benchmark. Its findings are:
- Each image's five references come from one writer (adjacent-slot share 0.7102 against 0.40 under exchangeability, with a slot-rate-preserving null).
- No reference ends with a period. Under a word-segmenter pipeline without PTB punctuation removal, one appended period costs 35.17 CIDEr-D points; with PTB-style removal it costs nothing.
- Segmentation moves scores by 15.64 points.
- The object matcher is undocumented.
- 401 of the 558 test images are in UIT-OpenViIC's training split.

It proposes a protocol card and releases an open kit. The merge adds a development-only study of training-set-size gains:
- B-1: +9.61 [7.18, 12.36] CIDEr-D per doubling, PASS.
- D0: scored against two caption panels of the same 187 dev images, the gain is +10.59 against KTVIC and +0.72 against OpenViIC; gap +9.87 [6.71, 13.35], GO.
- B-R1 (reverse direction): adapters trained on OpenViIC captions gain +2.98 on their own panel and +1.29 [-1.23, 3.75] on KTVIC; ASYMMETRIC.

### 2. Verification performed

I checked every main-text number in §5.4-5.5 against the decided files:
- manuscript/prereg/2026-10-29_b_d0/d0_decide.json (sha256 15dd925f, matches)
- manuscript/prereg/2026-10-29_b_r1/b_r1_decide.json (a6627047, matches, identical to .session_backup/2026-10-29/b_r1/decide.json)
- b_r1_matched.json (fa58ab8c)
- d0_reread.json (7853ab4a)
- the B-1 decide.json (b44a76fe)
- the B-1 and d_extrap PREREG files (ee91c152, 95bbf4cb) and the d_extrap output (f0eb2b9e)

All points and CIs match at the displayed precision, including the sigma = inf co-primary, the minus-twins rows, the crossover, the length slopes and the matched-design asymmetry. The manuscript cites the right outcome strings: ASYMMETRIC with reason gap_below_p1_sesoi, and P1_SESOI 4.934. The registered final-system FAIL (-0.39 [-2.44, +1.67]) is stated in §1 (sec1_intro.md:25, pointer and verdict) and in full in §5.1 (sec5_results.md:25), and it is repeated in §7.1 and §8. The abstract leaves it out, which the PASS-headline rule allows. No sentence claims that OpenViIC-trained gains reach KTVIC references, and no 'first' claim is made for the two-panel study. Related work was checked on Crossref (OpenAlex returned HTTP 429). Bromonschenkel et al. (2026, JBCS) exists as cited.

### 3. Novelty (3/5)

The KTVIC audit is a careful, useful resource contribution. Single-writer adjacency, the pipeline-dependent period cost, segmentation sensitivity and the cross-dataset overlap are concrete and new for Vietnamese. Their general ideas have precedents: metric signatures (sacreBLEU), punctuation sensitivity (Jwalapuram 2023), annotator bias (Geva et al. 2019). The two-panel study is the most original part: a training-set-size slope scored against two same-language human panels in both training directions. Related work omits close precedents in which the same images carry two caption sets, including cross-training: Multi30K (Elliott et al. 2016), van Miltenburg et al. 2017, Frank et al. 2018 (NLE), COCO-CN (Li et al. 2019) and Yi et al. 2020 on inter-reference variance. Novelty must be stated against these (Major M4).

### 4. Correctness (4/5)

The numbers are right and carefully traced, and the registration status is disclosed honestly throughout. The problems are in wording:
- the abstract generalises 'gains register mainly on the trained panel' to both directions, but the reverse gap is not significant (M1);
- 'no measurable gain' treats a non-significant slope as absent (M2);
- 'more than half' is not supported by a CI whose lower bound is 49.38% (M5);
- 'nearly vanishes' survives in §1 although the edit log says it was removed (m1);
- an unverified 'first reported' attribution (m2).

The design limits are serious: dev-only, 187 images, one backbone, two reverse seeds, a data-dependent equivalence margin and image-only bootstrap. They are mostly disclosed, but they should shape the title and headline more strongly (M3). Annotator-identity learning is a live alternative mechanism that the paper does not discuss (M6). The two-panel scoring protocol, including the k rule and the IDF corpus, is not on the protocol card (M7). Two statements became stale with the merge (M8).

### 5. Contribution (3/5)

For LRE the audit, the protocol card and the kit are a solid, practical contribution to Vietnamese captioning evaluation. The kit has been run on three external systems, though only by the authors, as is disclosed. The two-panel study makes a scientifically interesting point: a stable KTVIC gain is largely agreement with KTVIC's own writer. Its weight is limited by dev-only, single-backbone evidence and by the absence of a test confirmation, which the closed test set rules out within this paper.

### 6. Clarity (3/5)

The structure is logical and the claims are hedged with care. But the merged paper has two headlines (the audit-and-kit, and the training-gain study), and §5.4-5.5 are very dense with descriptive rows, post hoc labels and internal codes. Several cross-references and dates are stale (m5, m12). Tables 2.1, 4.2 and 5.1 and Figures 5.1-5.2 help. A table for the §5.5 descriptive rows would help most.

### 7. Recommendation: major revision

The core numbers are sound and the transparency is exemplary. The required revisions are reframing and positioning: scope the headline to the forward direction and to development data, correct four overclaiming phrases, add the missing same-image multi-panel literature, document the two-panel scoring protocol, and fix the stale statements. None needs new GPU runs, new labels or another look at the test set.

Binding-rule note for the revise step: no new human gold labels; AI-generated labels are not evidence; no second KTVIC test look; keep the FAIL in §1 and §5.1; make no 'first' claims without verified prior art; add no caption text from KTVIC, OpenViIC or UIT-ViIC; make no commits and use no GPU. Any optional IDF sensitivity (M7) is CPU-only on existing dev outputs and labelled post hoc and descriptive.
