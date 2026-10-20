# Supplementary S2 (part): matcher and label-map sensitivity

<!-- All numbers: .session_backup/2026-10-18/paperA_tasks/A8.4/sensitivity.json (sha256 969797ae99b7), label "post hoc sensitivity, not a registered test"; VERIFIED in manuscript/verification/paperA/A8.4.json. "nodes" = one English matcher (the E1 CHAIR rules, e1_chair_count.nodes) used for the reference gold in place of score_coco_probe.en_classes. -->

This is a post-hoc sensitivity analysis, not a registered test. We re-ran every analysis in this paper that uses an English reference gold with one English matcher throughout: the CHAIR rules that score the English captions of Section 6 replace the reference-side extractor. We also re-ran the XM3600 analyses without the five doubtful Open Images mappings.

**Reproduction.** Run with the original matcher and map, the copied code reproduces the cited values exactly (34 of 34 comparisons)<!-- src: sensitivity.json :: reproduction_with_original_matcher_or_map.{all_equal = true, n_checks = 34} -->.

**No headline change.** No verdict, ordering, endpoint or sign changes in 55 checks<!-- src: sensitivity.json :: answer.{any_headline_change = false, headline_checks_evaluated = 55, headline_changes = []} -->.

**Small shifts in the values:**
- COCO-2500 slopes: one reference −4.28 to −4.92, five references 11.08 to 10.87<!-- src: sensitivity.json :: coco2500_frontier.values.refs1_randk.slope.{original,swapped.nodes}.value; coco2500_frontier.values.refs5_randk.slope.{original,swapped.nodes}.value -->.
- Micro-F1 slope at one reference: −1.84 to −2.31<!-- src: sensitivity.json :: coco2500_theory_checks.values.coco2500.T2_microF1_randk.1.slope.swapped.nodes.value -->.
- $\Lambda_U(1)$: 0.047 to 0.017, with its interval still including 0, [−0.055, 0.094]<!-- src: sensitivity.json :: coco2500_lambda_U_split.values.Lambda_U.refs1_randk.swapped.nodes.value; coco2500_lambda_U_bootstrap.values.gold.refs1_randk.Lambda_U.ci.swapped.nodes.value = [-0.0547, 0.0939] -->.
- b-channel shares: 0.613 to 0.634 and 0.709 to 0.717<!-- src: sensitivity.json :: coco2500_lambda_U_split.values.b_channel_share_U.{coco_randk,coco_refs1_to_inst}.swapped.nodes.value -->.
- Adjacent-doubleton shares of Section 5: by at most 0.015<!-- src: sensitivity.json :: exchangeability_english_rows.values.uitviic_en_test_coco80.adjacent_share.delta_swapped_minus_original.nodes = -0.0149 (largest absolute shift) -->.
- XM3600 OIV7 slope: 19.32 to 19.25 with the doubtful links dropped, and to 21.60 with the doubtful entries dropped<!-- src: sensitivity.json :: xm3600_oiv7_map.values.oiv7_verified.slope_F1_per_logM.swapped.{oiv7_drop_pos,oiv7_drop_entry}.value -->.

**Two descriptive statements change:**
- the gap between the first-k and random-k one-reference slopes grows from 0.07 to 0.15;
- the share of bootstrap replicates in which $\Lambda_U(1)$ and the one-reference slope have opposite signs falls from 0.88 to 0.68 (Section 4.3)<!-- src: sensitivity.json :: answer.other_changes[0] (firstk_randk_gap 0.07 -> 0.15), answer.other_changes[1] (opposite_sign_share_k1 0.8815 -> 0.6805) -->.

**Registered gold-size checks.** The registered XM3600 gold-size checks compare with values frozen under the original map, so dropping mappings moves them by construction. They were reproduced for 14 of 15 values originally, and for 10 or 9 of 15 after the drops<!-- src: sensitivity.json :: answer.other_changes[2,3] (gold_size_checks_in 14/15 -> 10/15 and 9/15) -->.
