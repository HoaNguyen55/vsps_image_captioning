# 8 Experiments III: what human judgments support

This section asks which metric properties line up with existing human judgments. We collected no new annotation and use no model-produced labels as evidence. The five public sets, in order of how firmly their predictions were fixed, are LongCap-Arena, THumB 1.0 and the Composite set, Polaris-COCO and DOCCI-Critique (14 VLMs). Nothing below shows that a count-controlled score is what humans want.<!-- src (A6.3 merge, VERIFIED): '14' (DOCCI VLMs) = .session_backup/2026-10-14/r12_verify/h1_g3_registered_supplement_v2.json :: registered_G3.data_summary.n_vlms -->

**Unit and statistic.** The unit is a pair of captions of the same image. The agreement $\mathrm{acc}(X \to H)$ of a score $X$ with a judgment $H$ is the share of concordant pairs among pairs where both differ; "count-differing" pairs name different numbers of COCO classes. Intervals: 2,000-draw image bootstrap.

**Registration.** Every result carries its label. LongCap-Arena is registered: its pre-registration was committed and pushed before the first output. THumB and Composite are frozen locally: the predictions were written and hashed before any human statistic but never committed. Polaris and DOCCI-Critique are frozen locally but committed after the first results file (by 22 minutes), so we treat them as exploratory, although their pre-specified rules are reported as written. Times are in Tab. 7 and Supplementary S4.<!-- src: .session_backup/2026-10-18/paperA_tasks/A4.4/tests_status.tsv :: Q2_LONGCAP REGISTERED (t_commit 2026-10-15T02:50:04Z, t_out 05:59:16Z; GitHub server-side push 02:50:10Z per .session_backup/2026-10-18/github_activity/q2_activity_20261018T1955Z.json :: push id 46544934992), H1_TC LOCALLY_FROZEN (manuscript/prereg/2026-10-18_never_committed_frozen_files.json :: files[0], mtime 2026-10-14T12:52:33Z, never committed), G2_POLARIS and G3_DOCCI LOCALLY_FROZEN (.session_backup/2026-10-18/paperA_tasks/A4.2/prereg_ledger_v2.tsv :: row 33, first_result_minus_registration -22m09s; VERIFIED in manuscript/verification/paperA/A4.2_v2.json; ruling D-W13-6) -->

## 8.1 LongCap-Arena: long captions, mixed result (registered)

The pre-registration (7254a39) was committed before the results file was written<!-- src: git show -s 7254a39 (2026-10-15 02:50Z); .session_backup/2026-10-15/r13_human/q2_longcap_arena.json :: prereg_json_sha256, script_sha_matches_prereg = true, input_sha_mismatch_vs_prereg = {} -->. The CapArena test was dropped because no licence statement for its human battles could be found<!-- src: .session_backup/2026-10-15/r13_data/licence_check_2026-10-15.json :: CapArena.status = DROPPED_NO_LICENCE -->.

LongCap-Arena (Matsuda et al., 2025; BSD-3-Clause) gives human Relevance ratings for 5,109 long captions of 5,109 images<!-- src: .session_backup/2026-10-15/r13_human/q2_longcap_arena.json :: data_summary.{n_captions,n_images}; cite: arXiv 2509.25818, EMNLP 2025 per arXiv comment; about 100 words per caption (data_summary.mean_words) -->. The registered COCO-80 matcher finds 1.23 classes per caption on average (median 1)<!-- src: same :: data_summary.{mean_M,median_M} -->, so it measures only a small part of each caption.

**Declared design changes.** With one caption per image and no system labels, the pre-registration adapted the three tests before any look (Supplementary S8).

The registered verdict is **MIXED**: one of three predictions held, and both kill rules fired<!-- src: same :: verdict = MIXED, n_primary_pass = 1, test_ii_delta_tau.kill_rule_fired = true, test_iii_count_equal_vs_differing.kill_rule_fired = true -->.

- **(i) Humans penalize object count: PASS.** Relevance falls by 0.024 per additional COCO class [−0.029, −0.020]<!-- src: same :: test_i_slope_rel_on_M.{beta_M,beta_M_ci_95,pass} -->.
- **(ii) Count-matched precision tracks Relevance better than raw precision: FAIL, kill rule fired.** It tracks it worse: $\Delta\tau_b$ = −0.028 [−0.036, −0.019] on the 3,413 captions that name at least one class<!-- src: same :: test_ii_delta_tau.{delta_tau,delta_tau_ci_95,n_captions_M_ge_1,pass} -->; the claim is withdrawn.
- **(iii) −CHAIR agrees with Relevance more on count-equal than on count-differing pairs: FAIL, kill rule fired.** The difference is −0.017 [−0.035, +0.0003]<!-- src: same :: test_iii_count_equal_vs_differing.{diff_ceq_minus_cdiff,diff_ci_95,pass} -->; pairing captions of different images, this is a weaker test than the within-image comparisons of Sections 8.2–8.3 (run history: Supplementary S4).

## 8.2 Short COCO captions: THumB and Composite (frozen locally; exploratory)

THumB has 500 images with 5 captions each (four systems and one human caption), 5,000 within-image pairs; the Composite set has 1,996 images and 8,348 pairs<!-- src: .session_backup/2026-10-14/r12/H1/pilot_results.json :: THumB.{n_img,n_pairs}; Composite.{n_img,n_pairs} -->. Table 8.1 gives the frozen predictions and their outcomes under the frozen rules (exploratory).<!-- src (A6.3 merge, VERIFIED): '5' (THumB captions per image) = .session_backup/2026-10-14/r12/H1/pilot_results.json :: THumB.n_cap / THumB.n_img -->

**Table 8.1** (Tab. 5). Predictions frozen locally, never committed; full gold: instances + references.

| Prediction | THumB (T) | Composite (C) | Outcome |
|---|---|---|---|
| P1a: −CHAIR beats $z$ on human precision | +0.325 [+0.247, +0.398] | +0.097 [+0.079, +0.116] | held ×2 |
| P1b: $z$ beats −CHAIR on human total | −0.190 [−0.277, −0.108] | −0.083 [−0.101, −0.065] | failed ×2 |
| P2a: humans prefer more classes (> 0.5) | 0.481 [0.429, 0.530] | 0.525 [0.506, 0.544] | failed T, held C |
| P2b: F1's longer-caption preference grows with gold (1/4/full refs), nearest humans at full | 0.41, 0.66, 0.83 | 0.54, 0.66, 0.73 | rise held; closeness failed |
| P2c: full-gold F1 beats one-reference F1 on human total | −0.018 [−0.073, +0.038] | −0.006 [−0.022, +0.010] | failed ×2; kill fired |
| P3: real errors cost more than "pseudo" ones: $\beta_{\text{PFP}} - \beta_{\text{FP}}$ | +1.07 [+0.82, +1.32] | +0.68 [+0.54, +0.81] | held T; failed C |
| P4: humans side with CHAIR on clean wins (≥ 0.75), not confounded ones (≤ 0.60) | 0.846; 16 confounded | 0.946; confounded 0.705 [0.645, 0.763] | underpowered T; failed C |
| P5: human captions rank lowest at one reference | — | — | failed |

<!-- src (all .session_backup/2026-10-14/r12/H1/pilot_results.json, sha256 224928834752):
P1a: {THumB,Composite}.P1a_acc(-CHAIR->P)-acc(z->P).{est,ci}; P1b: {THumB,Composite}.P1b_acc(z->T)-acc(-CHAIR->T).{est,ci};
P2a: {THumB,Composite}.P2a_v_human.{est,ci}; P2b: {THumB,Composite}.P2b_v_F1_{refs1,refs4,full}.est;
P2c: {THumB,Composite}.P2c_acc(F1_full->T)-acc(F1_refs1->T).{est,ci};
P3: THumB.P3_ols_P.{FP_full,PFP_refs1,PFP-FP}.{est,ci}; Composite.P3_ols_P.{PFP_refs1,PFP-FP}.{est,ci};
P4: {THumB,Composite}.P4_clean_T.{est,n_untied}; THumB.P4_confounded_T.n_untied; Composite.P4_confounded_T.{est,ci};
P5 and all outcome labels: .session_backup/2026-10-14/r12/H1/REPORT.txt §1b (thresholds from PREDICTIONS_FROZEN.txt). -->

Three findings come out of these tests; all are exploratory.

**The count-controlled residual is not a better quality score.** P1b failed in both sets, by a wide margin: the residual $z$ (true positives minus the frontier expectation at the caption's count) agrees with the human total less often than raw −CHAIR. Count control is an attribution tool, as Section 3.7 states, and the two-column standard keeps the raw score for that reason.

**Raw precision tracks human precision.** P1a held in both sets. On THumB, human precision falls by 1.16 points per real false positive but not for a mention only one reference omits (P3); on Composite (one crowd rater per item) such mentions cost 41.5% of a real error, and P3 failed.<!-- src (A6.3 merge, VERIFIED): '1.16' (THumB beta_FP) = .session_backup/2026-10-14/r12/H1/pilot_results.json :: THumB.P3_ols_P.FP_full.est; '41.5%' (Composite beta_PFP/beta_FP = 0.4798 / 1.1559) = .session_backup/2026-10-14/r12/H1/pilot_results.json :: Composite.P3_ols_P.PFP_refs1.est / Composite.P3_ols_P.FP_full.est (manifest row 0.415) -->

**Humans barely prefer naming more objects; full-gold F1 strongly does.** Humans prefer the caption that names more classes in 0.481 [0.429, 0.530] of count-differing pairs on THumB (P2a failed) and 0.525 [0.506, 0.544] on Composite (held)<!-- src: .session_backup/2026-10-14/r12/H1/pilot_results.json :: {THumB,Composite}.P2a_v_human.{est,ci}; labels per .session_backup/2026-10-18/paperA_tasks/A4.4/verdict_labels.tsv :: H1_P2a_Composite HELD (rule PREDICTIONS_FROZEN.txt:23) -->, while F1's preference rises from 0.41 to 0.83 on THumB as the gold is completed (P2b). P2c's kill rule fired: completing the gold does not make F1 agree better with human judgments.<!-- src (A6.3 merge, VERIFIED): '0.41' = .session_backup/2026-10-14/r12/H1/pilot_results.json :: THumB.P2b_v_F1_refs1.est; '0.83' = .session_backup/2026-10-14/r12/H1/pilot_results.json :: THumB.P2b_v_F1_full.est -->

**Exploratory (not registered).** Two patterns were not predicted: gold completeness is the largest single driver of agreement between −CHAIR and human precision on THumB (0.736 with one reference, 0.903 with full gold)<!-- src: .session_backup/2026-10-14/r12/H1/pilot_results.json :: THumB.agree.negCHAIR|{refs1,full}|P|all.est -->, and −CHAIR agrees with humans more on count-equal pairs (Supplementary S8). Polaris (Section 8.3) tests both.

## 8.3 Polaris-COCO: replication at scale (exploratory)

Polaris (Wada et al., 2024) gives overall human ratings; we use its COCO test split (2,286 images, 10,496 within-image pairs)<!-- src: .session_backup/2026-10-14/r12_verify/h1_g3_registered_supplement_v2.json :: registered_G2.{n_coco_images,n_within_image_pairs} -->. All three pre-specified predictions held and no kill rule fired (verdict PASS under the pre-specified rule); because the specification was committed after the first result, this is an exploratory replication<!-- src: same :: registered_G2.verdict = PASS; registered_G2.kill_rule_fired = False -->.

- **H-a, gold completeness.** −CHAIR agrees with the overall rating more under full gold than under one reference: +0.0606 [+0.0535, +0.0679] on all pairs<!-- src: same :: registered_G2.H_a.diff_full_minus_refs1_all.{est,ci} -->.
- **H-b, count-equal pairs.** Under full gold, agreement is higher on count-equal than on count-differing pairs: +0.025 [+0.016, +0.035]<!-- src: same :: registered_G2.H_b.diff_ceq_minus_cdiff.{est,ci} -->.
- **H-c, count-neutral humans.** The correlation of the number of named classes with the rating lies inside the pre-specified band of ±0.10 (+0.067 at caption level; Supplementary S8)<!-- src: same :: registered_G2.H_c.caption_level_pearson_spearman[0]; '±0.10' = registered_G2.H_c.description (number in string) -->.

Polaris thus replicates the two exploratory THumB/Composite patterns at larger scale, again on short COCO captions.

## 8.4 DOCCI-Critique: long paragraphs, mixed result (exploratory)

DOCCI-Critique (Gordon et al., 2025; CC BY 4.0) gives sentence-level factuality ratings for 1,398 paragraphs from 14 VLMs on 100 images<!-- src: .session_backup/2026-10-14/r12_verify/h1_g3_registered_supplement_v2.json :: registered_G3.data_summary.{n_images,n_vlms,n_paragraphs}; cite: arXiv 2506.07631; matcher COCO-80 (registered_G3.matcher) -->, the only long, LVLM-style outputs here. The verdict under the pre-specified rules (G3) is **MIXED** (exploratory, for the same reason as Polaris)<!-- src: same :: registered_G3.verdict -->.

**G3-(i), within-VLM count effect: primary fails.** The prediction required mean and median within-VLM slopes below 0 and a pooled VLM-fixed-effects slope with interval below 0. Under the primary measure (sentence-level majority) the mean slope is −0.0127 [−0.0265, +0.0007] and the pooled slope −0.0157 [−0.0286, −0.0024], but the median is +0.000371 (7 of 14 VLMs negative), so the median clause fails<!-- src: same :: registered_G3.G3_i.P_human_sent_maj.{mean_within_vlm_slope,mean_within_vlm_slope_ci_95,beta_FE,beta_FE_ci_95,median_within_vlm_slope,n_vlms_negative_slope,failed_clause,pass} -->; under the secondary measure all three clauses hold (Supplementary S8).

**G3-(ii), ranking the 14 VLMs: HELD, interval includes 0.** The matched-prefix score ranks the VLMs closer to human factuality than raw precision by +0.1538 (micro) and +0.2198 (macro), above the pre-specified +0.10, so G3-(ii) is labelled HELD, but the interval [−0.2637, +0.3077] includes 0<!-- src: same :: registered_G3.G3_ii.P_human_sent_maj.delta_tau_vs_micro.{est,ci_95}, .delta_tau_vs_macro_M_ge_1.est, .ci_excludes_zero = False; '+0.10' = manuscript/prereg/2026-10-14_h1_polaris_docci.md :: line 68 -->; with 14 systems<!-- src (precut, A6.3 merge, VERIFIED): '14' (DOCCI VLMs) = .session_backup/2026-10-14/r12_verify/h1_g3_registered_supplement_v2.json :: registered_G3.data_summary.n_vlms --> the test has little power (Supplementary S8).

**Limits specific to this set.** The COCO-80 matcher sees few objects in DOCCI paragraphs (mean 1.50 classes, median 1, against a gold of 1.36)<!-- src: same :: registered_G3.data_summary.{mean_paragraph_M,median_paragraph_M,mean_gold_classes_G} -->. A larger noun vocabulary, tried after the fact, is exploratory only and supports no claim (Supplementary S6).

## 8.4b Human span labels on COCO (A-N3, registered secondary)

A-N3 tests criterion validity against M-HalDetect human span labels (CC BY-NC 4.0, research use; the download is pinned by sha256 and not redistributed) on 3,419 COCO-2014 images and 13,997 records. Agreement between object precision and the human labels rises from one reference to all references (tau_b difference +0.057 [+0.043, +0.071], PASS) but not from all references to complete COCO-80 gold (−0.021 [−0.043, +0.002]); the second part is a FAIL under the registered rule "point ≤ 0", and its interval includes 0, so it is not a significant negative. The registered outcome is NOT_SUPPORTED. Condensed F1 agrees with the human labels better than F1 under one reference (+0.049 [+0.033, +0.064], PASS) but not detectably under all references (+0.010 [−0.002, +0.023], INCONCLUSIVE). Complete gold here is complete only within 80 classes, while the human labels are open-vocabulary; any analysis of that difference would be post hoc.<!-- src: data/results/a_n3/a_n3_run.json (sha256 7a5a614d, commit 1c153fa) :: predictions.AN3-P1.parts[0..1], AN3-P2.parts[0..1], outcome = NOT_SUPPORTED; prereg manuscript/prereg/2026-10-19_a_n3_criterion_mhaldetect.md (9f4097f); VERIFIED manuscript/verification/paperA/A_N3_run.json (48f0416b; canonical-equal re-run, CC-038b) -->

## 8.5 What the human evidence supports

Human judgments penalize object count where captions are long: LongCap-Arena Relevance falls with the number of named classes (registered), and the pooled DOCCI-Critique slope is negative (exploratory). This supports the confound that count control removes. On short COCO captions humans are close to count-neutral (exploratory).

Count-matched precision does not track human judgments better than raw precision: it agreed less often on THumB and Composite (frozen locally), tracked LongCap-Arena Relevance worse (registered), and on DOCCI-Critique met its threshold with an interval including 0. Count control attributes differences; it does not measure what humans judge.

On short captions, object metrics agree with humans more under complete gold and on count-equal pairs (exploratory); on long captions no count-equal advantage was found, and the matcher sees only one or two classes. The human results check, but do not ground, the measurement argument.
