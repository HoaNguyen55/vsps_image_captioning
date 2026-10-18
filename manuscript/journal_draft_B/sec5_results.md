# 5 Results

<!-- Draft 2026-10-15. Object scores use matcher v2. "pp" = percentage points of the metric. -->

## 5.1 The controlled system on KTVIC

P1-R scores a word-level CIDEr-D of 148.66, 148.06 and 147.96 on seeds 42, 43 and 44<!-- src: .session_backup/2026-10-15/paperA_keys/cider_3seed_mean.json :: per_seed|data/results/p1assist_s42-short.json|CIDEr_x100 ; per_seed|data/results/p1assist_s43-short.json|CIDEr_x100 ; per_seed|data/results/p1assist_s44-short.json|CIDEr_x100 -->: mean 148.23, SD 0.38<!-- src: .session_backup/2026-10-15/paperA_keys/cider_3seed_mean.json :: mean ; sd_sample_ddof1 -->. BLEU-4 is 45.88 and 45.63 on seeds 42 and 43, and ROUGE-L 64.57 on seed 42<!-- src: .session_backup/2026-10-15/paperA_keys/cider_3seed_g1_rescore_check.json :: per_seed|p1assist_s42-short|rescored_BLEU4_x100 ; per_seed|p1assist_s43-short|rescored_BLEU4_x100 ; per_seed|p1assist_s42-short|rescored_ROUGEL_x100 -->.

**Table 5.1.** Three-seed means on KTVIC test (558 images). M = mentioned classes per caption. The residual is object F1 minus the frontier's prediction at the system's M.

| System (prompt) | CIDEr-D | M | object F1 | frontier residual F1 |
|---|---|---|---|---|
| P1 (short) | 145.8 | 1.7825 | 54.6 | anchor |
| P1-R (short) | 148.23 | 1.7856 | 55.44 | 0.81 |
| fuse2 (short) | 143.7 | 2.0878 | 58.1 | 0.64 |
| fuse2 (detailed) | 22.4 | 3.2115 | 64.24 | −0.42 |

<!-- src: .session_backup/2026-10-13/r9_synthesis/PD2_BLOCKER5_9_TABLES.json :: table_b5a_frontier_residuals|v2|seed_groups|{p1_3seed-short,p1assist_3seed-short,fuse2_3seed-short,fuse2_3seed-detailed}|ngrams_mean|CIDEr ; |ktvic_558|m ; |ktvic_558|F1 ; |ktvic_558|res_F1 ; P1-R CIDEr-D from .session_backup/2026-10-15/paperA_keys/cider_3seed_mean.json :: mean -->

Three readings follow.

- **CIDEr and object F1 rank systems differently.** fuse2 names more objects and has higher object F1 than P1-R, but lower CIDEr-D. In detailed mode its CIDEr-D collapses to 22.4 while its object F1 is the highest in the table: CIDEr rewards matching the short, unpunctuated reference template, not describing more of the image.
- **No system leaves the frontier.** All residuals are within one point of zero. The gains in object F1 come from naming more objects, at the precision the frontier predicts for that count (Section 5.2).
- **The response-only mask is not a tested improvement.** P1-R's mean is above P1's three-seed mean of 145.8, but P1's seed 42 scored 149.79 under the same scorer (the value the FAIR version reported as 149.8)<!-- src: data/results/p1-gold-short.json :: results[0].scores_scaled_x100.CIDEr -->. We report P1-R as a strong, stable baseline and make no claim that the mask helps.

We report no comparison with other Vietnamese systems as a ranking. GRIT's 136.0 and later systems were scored under protocols that differ in segmenter, scale or punctuation (Section 3.4), and protocol-matched rescoring is **PENDING**.

## 5.2 Supervision ladder

Table 5.2 lists every landed run against its frozen intervals.

**Table 5.2.** Ladder runs on KTVIC test, matcher v2. Intervals in brackets are the registered [low, high]. "In" means inside all three registered intervals.

| Run | M | P | R | In? | frontier residual P [95% CI] |
|---|---|---|---|---|---|
| 54 P1-4ep (short) | 1.7258 | 77.5701 | 39.772 | yes | −1.5946 [−3.4578, 0.2019] |
| 55 cons (short) | 2.0735 | **77.0095** [72.8, 76.7] | 47.5311 | **no (P out)** | 1.4397 [−0.0688, 2.8764] |
| fuse2 s43 (detailed) | **3.2545** [ , 3.254] | 66.9604 | 62.4452 | **no (M out)** | −0.4574 |
| fuse2 s44 (detailed) | 3.2258 | 66.7222 | 60.9353 | yes | −0.8467 |
| fuse2 s43 (short) | 2.1093 | 75.446 | 47.5978 | yes | 0.2034 |
| fuse2 s44 (short) | 2.0627 | 75.6733 | 46.7868 | yes | 0.0039 |
| 56 multiref, 57 rnd2, 58 unf2 | PENDING | | | | |

<!-- src: .session_backup/2026-10-14/r12_verify/c9_55_ladder_cons_s42_evaluation.json :: prereg_ladder_check.all_6_landed_ladder_runs.{p1ep4_s42-short,cons_s42-short,fuse2_s43-detailed,fuse2_s44-detailed,fuse2_s43-short,fuse2_s44-short}.observed_v2_tone_norm.{M,P,R} ; .prereg_intervals ; .in_prereg_interval ; .frontier_residual_P_v2_pp ; .frontier_residual_ci95_v2_pp -->

**Run 55 misses.** Consensus targets produce precision 77.0095, above the registered interval [72.8, 76.7]<!-- src: .session_backup/2026-10-14/r12_verify/c9_55_ladder_cons_s42_evaluation.json :: prereg_ladder_check.all_6_landed_ladder_runs.cons_s42-short.observed_v2_tone_norm.P ; prereg_intervals.P[1] ; prereg_intervals.P[2] -->. Its frontier residual of 1.4397 has a CI that includes zero, [−0.0688, 2.8764]<!-- src: same file :: prereg_ladder_check.all_6_landed_ladder_runs.cons_s42-short.frontier_residual_P_v2_pp ; frontier_residual_ci95_v2_pp -->. Its own equivalence test fails at both bounds: p = 0.7323 at ±1.0 and p = 0.2478 at ±2.0<!-- src: same file :: prereg_ladder_check.all_6_landed_ladder_runs.cons_s42-short.tost_v2.tost_pm_1_0p.p_tost ; tost_pm_2_0p.p_tost -->. One seed of cons cannot separate a real precision gain of one to three points from noise, so we report the run as a registered miss on P, neither a confirmation nor a refutation of frontier invariance. Its CIDEr-D is 147.09<!-- src: same file :: system_summaries.cons_s42-short.scores_scaled_x100.CIDEr -->.

**fuse2 seed 43 (detailed) misses narrowly.** Its count, 3.2545, exceeds the registered upper bound of 3.254<!-- src: same file :: prereg_ladder_check.all_6_landed_ladder_runs.fuse2_s43-detailed.observed_v2_tone_norm.M ; prereg_intervals.M[2] -->. We count it as a miss, so four of the six landed runs are inside all three intervals.

**Pooled frontier invariance.** Over the six landed runs (two ladder steps and four fuse2 seed replications), the mean frontier residual is −0.2086 pp [−1.1403, 0.7604]<!-- src: same file :: prereg_ladder_check.joint_frontier_invariance_6_landed_runs.n_landed_runs ; mean_residual_P_pp ; ci95_pp -->.

- *Registered criterion:* the CI contains 0 and the point lies in [−0.8, +0.8]. **It passes.** This criterion only fails to reject; on its own it does not show equivalence.
- *Post-registration TOST (disclosed in Section 4.3):* the 90% CI [−0.9877, 0.5659] lies inside ±1.0, p = 0.048; inside ±2.0, p = 0.001<!-- src: same file :: prereg_ladder_check.joint_frontier_invariance_6_landed_runs.tost_summary.ci90_pp ; tost_pm_1_0p.p_tost ; tost_pm_2_0p.p_tost -->. The pooled residual is equivalent to zero within ±1.0 point. The ±1.0 result sits at the edge of significance, and the minimum effect detectable with 80% power is 1.362<!-- src: same file :: prereg_ladder_check.joint_frontier_invariance_6_landed_runs.tost_summary.mde_80pct_power_alpha05_pp -->. The three pending runs will decide whether it holds.

**L vs T.** P1-4ep's count of 1.7258 stays above *L*'s floor of 1.63 and far from *T*'s predicted 1.24<!-- src: same file :: prereg_ladder_check.all_6_landed_ladder_runs.p1ep4_s42-short.observed_v2_tone_norm.M ; h6_p4_discrimination.p1ep4_s42_short_L_vs_T.L_threshold_min_M ; T_ideal_count_test -->. cons's count ratio to the P1 anchor, 1.1632, lies inside *L*'s registered interval [1.153, 1.277], against *T*'s 1.467<!-- src: same file :: h6_p4_discrimination.cons_s42_short_L_vs_T.M_ratio_vs_P1_anchor_M1 ; prereg_L_interval_M_ratio ; T_model_M_ratio_vs_P1 -->. Both registered discriminators favour *L*. Under the addendum, this means only that counts follow target length; *T* was already inconsistent with P1's count before the ladder ran. Against fuse2, cons differs by −0.0179 in count and 1.2597 pp in precision, inside the registered no-bleed-over bounds<!-- src: same file :: h6_p4_discrimination.cons_s42_vs_fuse2_s42_bleed_over_test.dM_cons_minus_fuse2 ; dP_cons_minus_fuse2_pp -->.

**What the ladder says about the system.** Within one backbone and one recipe, choosing different human references as targets moves the system along a single precision–count frontier: more objects at lower precision, at the rate the frontier predicts. No target-curation recipe we registered buys precision at equal count. If this is the fine-tuned model's behaviour, then "improving" a KTVIC system by its object scores without matching counts mostly changes how much it says.

## 5.3 Transfer to UIT-ViIC

**Cross-dataset transfer (52_a).** On the 231 UIT-ViIC test images (short prompt), the KTVIC-trained P1 scores CIDEr-D 41.71 and fuse2 38.52, against 32.99 for zero-shot<!-- src: data/results/uitviic/uitviic_p1_s43-short.json :: results[0].scores_scaled_x100.CIDEr ; data/results/uitviic/uitviic_fuse2_s42-short.json :: same ; data/results/uitviic/uitviic_zeroshot-short.json :: same -->. Systems trained in-domain on UIT-ViIC (52_b) score 132.07 (P1) and 117.70 (fuse2)<!-- src: data/results/uitviic_ind_test/uitviic_p1_s42-short.json :: results[0].scores_scaled_x100.CIDEr ; data/results/uitviic_ind_test/uitviic_fuse2_s42-short.json :: same -->. KTVIC's template transfers poorly in n-gram terms. Part of that is punctuation (Section 3.3).

**In-domain replication of the fusion effect.** On UIT-ViIC, COCO instance annotations give a gold that no caption writer produced. Against it, in-domain fuse2 raises object F1 over in-domain P1 by +6.67 pp [4.63, 8.75] (test, short)<!-- src: .session_backup/2026-10-14/uitviic_52a_52b_comparison.json :: test.short.fuse2_minus_p1_paired_b5000.inst_only_norm.F1[0] ; [1] ; [2] -->. The fusion gain on KTVIC is not an artifact of scoring against the same references the targets came from.

**Gold changes the sign of the count effect.** Across the ten UIT-ViIC systems (transfer and in-domain, short and detailed), we fit the slope of object F1 on log mentions per image under three golds:

- one reference: −15.90;
- the union of five references: 4.80;
- COCO instance labels: 37.52<!-- src: .session_backup/2026-10-15/paperA_keys/uitviic_paired_diffs.json :: coco80.all_10.ref1_first.slope ; refs_all.slope ; inst.slope -->.

The gold-completeness ordering of the verbosity slope on UIT-ViIC is reported in the companion paper (Paper A); we do not restate its numbers here.

These slopes are exploratory. They were computed before any frozen prediction existed and use the COCO-80 matcher. With the Vietnamese matcher, the five-reference slope keeps its negative sign (companion paper, Section 11.1). The companion paper develops the general claim; here the result shows that the conclusions one draws about Vietnamese systems depend on which gold is used.

**References vs instance labels on UIT-ViIC.** Across the ten systems, a gain in object agreement with the references (A) carries over to a gain against COCO instance labels (I) with slope κ = 0.878 [0.457, 1.171]<!-- src: .session_backup/2026-10-14/r12_verify/h3_p1_uitviic_two_panel.json :: verdict_summary.kappa_lin_A_to_I_estimators.cross_system_10sys_rho_ols_test -->. Within one system's sample pool, choosing captions by agreement with two references and scoring the held-out references and instance labels, the transfer after partialling out count is 0.010 [−0.106, 0.131]<!-- src: same file :: verdict_summary.kappa_lin_A_to_I_estimators.within_pool_S_A01_H_A234_T_I_count_partialled_pooled_1155 -->. Differences between trained systems carry over to a gold no caption writer produced; reranking samples within a pool by reference agreement carries over nothing beyond count.

**Leakage rule.** Every POPE-500 evaluation of a UIT-ViIC-trained adapter excludes all 21 UIT-ViIC training images in POPE-500 (Section 3.6). Such evaluations are **PENDING**.

## 5.4 Two caption panels disagree (C3)

The 555 KTVIC test images that also have UIT-OpenViIC captions let us score the same outputs against two independent caption panels: KTVIC's single-writer references and OpenViIC's references. **OpenViIC enters only as aggregate scores.** The OpenViIC panel is larger, with 5.39 captions per image, and names more classes: 6.0 per image against KTVIC's 3.72, and 7.05 for the union<!-- src: data/results/second_panel.json :: panel_sizes.openviic_captions_per_image ; openviic_classes_per_image ; ktvic_classes_per_image ; union_classes_per_image -->.

**Agreement on fusion.** fuse2 minus P1 (short, seed 42) in object F1 is +3.99 pp [1.95, 5.99] against KTVIC and +4.51 pp [2.96, 6.04] against the OpenViIC panel<!-- src: data/results/second_panel.json :: paired|fuse2_s42-short - p1-gold-short|F1_vs_ktvic|d ; ci95 ; paired|fuse2_s42-short - p1-gold-short|F1_vs_openviic|d ; ci95 -->. The precision cost KTVIC assigns, −2.21 pp, shrinks to −0.25 pp [−2.43, 1.96] on the panel<!-- src: data/results/second_panel.json :: paired|fuse2_s42-short - p1-gold-short|P_vs_ktvic|d ; P_vs_openviic|d ; P_vs_openviic|ci95 -->. Of the objects fuse2 names that no KTVIC reference names, a share of 55.12% [49.38, 61.05] is named by the OpenViIC panel<!-- src: data/results/second_panel.json :: confirm|fuse2_s42-short|exact|confirmed_share ; ci95|confirmed_share -->. More than half of what KTVIC scores as "hallucinated" for this system is in another panel's captions of the same image.

**Disagreement on reranking.** For the object-consensus reranker UPE-MBR (Section 6.2), the two panels and the two count controls tell different stories. Two comparisons must be kept apart:

- *UPE vs the (v, g) tie-averaged pool control at UPE's own per-image count* (corpus object F1, KTVIC gold, three seeds, image-clustered bootstrap): −0.02 [−0.356, +0.324]<!-- src: .session_backup/2026-10-15/paperA_keys/upe_vg_two_estimators.json :: E1_corpus_F1_UPE_minus_vg_tieavg_at_own_ki.pooled_image_clustered_B2000_seed0_pt_lo_hi -->. No gain beyond what count explains.
- *UPE vs the registered COUNT reranker*, each residualised against its own vote control (per-image Dice ×100): +0.347 [0.111, 0.599]<!-- src: .session_backup/2026-10-15/paperA_keys/upe_vg_two_estimators.json :: E2_macro_Dice_resid_UPE_minus_resid_COUNT.dA_x100_pt_lo_hi_B4000_seed7 -->. This is a different comparison: UPE minus its vote control is −0.035 [−0.281, 0.221], and COUNT minus its vote control is −0.382 [−0.707, −0.07]<!-- src: .session_backup/2026-10-15/paperA_keys/upe_vg_two_estimators.json :: bridge_macro_Dice_UPE_minus_vote_ctrl_at_own_ki_x100 ; bridge_macro_Dice_COUNT_minus_vote_ctrl_at_own_ki_x100 -->. The positive difference comes from COUNT falling below its control, not from UPE rising above its own.

The two numbers are not in conflict, and neither shows that UPE adds image evidence.

**Ranking concordance.** Across all 79 scored KTVIC systems, the CIDEr-D ranking is unrelated to the ranking by object F1 against the OpenViIC panel (Spearman ρ = −0.0088)<!-- src: .session_backup/2026-10-14/r12_verify/ev_rank_audit.json :: n_total_systems_scored ; ranking_concordance.v2.all_committed_systems.evaluators.CIDEr_D.vs_ground_truth.panel_F1.spearman_rho -->. Among short-mode systems it is 0.6202<!-- src: same file :: ranking_concordance.v2.short_mode_systems.evaluators.CIDEr_D.vs_ground_truth.panel_F1.spearman_rho -->. Object F1 against KTVIC references agrees better with the panel ranking (ρ = 0.6789 over all systems)<!-- src: same file :: ranking_concordance.v2.all_committed_systems.evaluators.ref_F1.vs_ground_truth.panel_F1.spearman_rho -->. The OpenViIC panel is a second set of captions, not ground truth. The finding is that the two panels disagree, and KTVIC CIDEr tracks neither panel's object content across caption styles.
