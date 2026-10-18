# 6 Pre-registered and controlled negatives

<!-- Draft 2026-10-15. Registration status is stated per family. "Registered" = a prediction or gate committed to version control before the look; commit hashes given. Object scores use matcher v2. -->

Every lever below looked like a gain under raw scores, and each fails its registered gate or a count-controlled comparison. We report them because a reader who sees only raw CIDEr or raw object F1 would draw the opposite conclusion. Table 6.1 summarises; the paragraphs give the numbers.

**Table 6.1.** Negative results on KTVIC.

| Family | Registration | Test | Outcome |
|---|---|---|---|
| Text-kNN prior on sample pools | registered (`2026-10-14_knn_prior.md`, 4ccbee3) | ΔF1 ≥ 0.5 with CI > 0 vs two count-matched controls, plus panel gate | KILL |
| UPE-MBR object-consensus reranking | registered (`2026-10-13_upe_mbr.md`, 257bc8c) | kill 2: panel ΔF1 vs COUNT on 3/3 seeds | KILL |
| CIDEr-only RL (CN-RLOO, run 35_e) | registered gate v2 (`2026-10-13_rl_gate_v2.md`, 7dd2151) | dev CIDEr gain ≥ 3.0 and guards | KILL, not clean |
| P-M6b global-vote selection | rule committed 44 s before the first look; no pre-registration file | ΔF1 ≥ 0.8 on pooled seeds | KILL (exploratory status) |
| PLAN-F1 object planning | registered (`2026-10-13_plan_f1.md`, ee583c7) | count-matched controls on dev300 | no gain beyond count |
| Self-fuse k = 2 | not separately registered; scored against the frozen frontier | frontier residual | below frontier |
| E5 RFT, E5 DPO, MR5 multi-reference, P1 loss mask, object tags | frozen frontier (1b5d16b) as the yardstick | frontier residual F1 | no residual gain |

## 6.1 Text-kNN prior

The prior scores each candidate object by how often captions of visually similar training images mention it. Candidates are then selected from a pool of greedy and sampled captions. On dev300 the prior separates correct from incorrect objects within cells of equal vote and generation count with AUROC 0.6142<!-- src: .session_backup/2026-10-14/r12_verify/knn_prior_test_eval.json :: dev_fit_and_h5_verification.h5_claim1_reproduction.knn13_k10_within_vg_cell_auc -->. On test this falls to 0.5806 against KTVIC gold and 0.5395 against the OpenViIC panel<!-- src: same file :: test_eval.mean_within_cell_auc_3seed.ktvic_gold ; openviic_panel_gold -->.

The registered smallest effect of interest was ΔF1 = 0.5<!-- src: same file :: test_eval.primary_pooled_3seed_planf1_k.gate_evaluation.sesoi_dF1 -->. Pooled over three seeds, the prior beats the tie-averaged (v, g) control by +0.03 [−0.41, 0.46] and the POOL-VOTE control by +0.31 [−0.13, 0.75] (Holm p = 0.4295)<!-- src: same file :: test_eval.primary_pooled_3seed_planf1_k.vs_tie_avg.F1_vec ; vs_POOL_VOTE.F1_vec ; vs_POOL_VOTE.F1.p_holm -->. The panel gate also fails, L = +0.10 [−0.18, 0.37]<!-- src: same file :: test_eval.primary_pooled_3seed_planf1_k.b5_panel_gate_vs_tie_avg.L_contrast_555 -->. The registered verdict is KILL.

*Disclosure:* 42 of the 497 images in an earlier probe set used to develop the prior also belong to dev300<!-- src: same file :: dev_fit_and_h5_verification.h5_claim4_verification.overlap_count_with_dev300 ; e2_stage1_top500_nonempty_images -->. The dev AUROC is therefore optimistic. The test verdict does not depend on it.

Under the switch rule (D18 §5.2), this KILL moves the paper to the resource-and-audit framing. The gated alternative, M3 count-matched DPO, runs only if EV-RANK clears a within-cell AUROC of 0.58; it is **PENDING** and was not run.

## 6.2 UPE-MBR (object-consensus reranking)

UPE-MBR picks, among a system's sampled captions, the one whose objects other samples most often confirm. Against greedy decoding it looks like a clear gain: OpenViIC-panel object F1 +1.91 [1.45, 2.35] and CIDEr-D +2.34<!-- src: data/results/upe/test/upe_mbr_ktvic_test.json :: pooled.panel_obj_vs_greedy.F1 ; pooled.cider_vs_greedy[0] -->. The registered kill rule 2 compares UPE with a COUNT reranker that picks the sample with the same number of objects. Against it, the panel ΔF1 is +0.07 [−0.59, 0.65], +0.03 [−0.73, 0.70] and +0.17 [−0.24, 0.60] on seeds 42, 43 and 44<!-- src: data/results/upe/test/upe_mbr_ktvic_test.json :: p1assist_s42.vs_count.panel_obj.F1 ; p1assist_s43.vs_count.panel_obj.F1 ; p1assist_s44.vs_count.panel_obj.F1 -->. All three CIs contain zero, so kill 2 fires on 3/3 seeds. Against the (v, g) tie-averaged pool control at its own count, UPE's corpus F1 difference is −0.02 [−0.356, +0.324] (Section 5.4). The gain over greedy is the gain from naming more objects.

## 6.3 CIDEr-only reinforcement learning (run 35_e)

CN-RLOO fine-tunes P1 (trained without dev300) with CIDEr as the only reward. On dev300, CIDEr-D moves from 144.33 to 145.90, a gain of +1.57 [−6.26, 9.55]<!-- src: data/results/rl/g1_cn_v3_s42/gate.json :: dev_cider_evaluate_py.p1dev ; dev_cider_evaluate_py.rl ; dev_gain_x100_mean_lo_hi -->, below the registered gate of 3.0<!-- src: .session_backup/2026-10-13/r10_cpu/n11_35e_posthoc_r10_battery_v3.json :: prereg_gate_v2_summary.d14_rl_35e_gate_v2.cider_gate_threshold -->. One guard also failed: exact copies of training references rose to 2.25% in the last block, above the limit of 1.33%<!-- src: same file :: prereg_gate_v2_summary.d14_rl_35e_gate_v2.exact_copy_last_block_pct ; exact_copy_2x_step0_limit_pct -->. Because the gate and a guard failed together, the registered verdict is a KILL that is not clean: we cannot say which failure would have stopped the run alone.

A post-hoc count-matched endpoint gives +2.07 [−0.19, 4.24]<!-- src: same file :: 1_M4_cm_endpoint.m4_primary_g0_ktvic.delta_cm_x100_b5000 -->. The interval predicted for this endpoint (prediction C2 of the M4 battery) was [−1.5, +2.0]<!-- src: .session_backup/2026-10-13/r10_cpu/n11_35e_posthoc_r10_battery_v3.json :: 1_M4_cm_endpoint.m4_predictions_c1_to_c4_audit.C2_count_matched_delta_in_-1.5_+2.0_ci_contains_0.predicted_interval -->. The point estimate falls just above it, so the prediction did not hold. We report the endpoint as exploratory.

## 6.4 P-M6b global-vote selection

The P-M6b rule selects objects by a global vote across samples. The selection rule was committed 44 seconds before its first test look<!-- src: .session_backup/2026-10-14/r11_verify/m6_pm6b_arbitration_v4.json :: governance_and_prereg_timing_disclosure.test_execution_timeline_utc.look1_delay_after_commit_sec -->, with no pre-registration file, so we treat it as exploratory. Pooled over three seeds with an image-clustered bootstrap, ΔF1 = +0.65 [−0.02, 1.34]<!-- src: same file :: pm6b_gate_verdicts[3].dF1 ; dF1_ci -->. None of the 24 registered pooled rows reaches the ΔF1 ≥ 0.8 gate<!-- src: same file :: registered_pm6b_gate_summary.n_registered_pooled_rows ; n_registered_pooled_rows_passing -->. A first-look script printed "all gates pass" through a filtering bug while every table row showed a failure; the bug and the second look are recorded in the source file and disclosed here.

## 6.5 PLAN-F1 (object planning)

PLAN-F1 plans which objects to mention before writing the caption. On dev300 it raises mentioned classes per caption from 1.763 to 2.627<!-- src: data/results/planf1/dev_plan_critique.json :: 1_frontier_residual.greedy.m ; 1_frontier_residual.plan_cap3.m -->, and its frontier residual is −2.49<!-- src: same file :: 1_frontier_residual.plan_cap3.frontier_residual_F1 -->. Against a pool-vote control matched on count it gives −0.95 [−2.09, 0.18]<!-- src: same file :: 2_matched_count_controls.pool_vote_matched_13.plan_minus_control.F1 -->. Its raw F1 gain is a count shift.

## 6.6 Training and decoding levers measured against the frozen frontier

Frontier residual F1 (pp) on KTVIC test, seed 42 unless stated, with 95% CI:

| Lever | Residual F1 |
|---|---|
| self-fuse k = 2 on fuse2 | −4.21 [−6.11, −2.27] |
| self-fuse k = 2 on P1 (seed 43) | −3.84 [−5.89, −1.96] |
| E5 group-relative RFT (CIDEr + object precision reward) | −0.15 [−2.55, 2.06] |
| E5 offline DPO | −1.97 [−4.33, 0.18] |
| MR5 (all five references, response-only) | 0.25 [−2.10, 2.54] |
| P1 rerun whose loss-mask flag was a no-op (a P1 replicate; p1mask) | 0.25 [−2.17, 2.59] |
| detector-tag-conditioned fusion (fuse2 targets) | 1.55 [−0.64, 3.78] |

<!-- src: .session_backup/2026-10-13/r9_synthesis/PD2_BLOCKER5_9_TABLES.json :: table_b5a_frontier_residuals|v2|systems|{fuse2_s42selffuse-two,p1_s43selffuse-two,e5_s42-short,e5dpo_s42-short,mr5assist_s42-short,p1mask_s42-short,tags_fuse2_s42-short}|ktvic_558|frontier_prereg|res_F1 ; res_F1_ci95 -->

Self-fuse is a training-free selection that appends the sample adding the most new objects. It produces longer, two-sentence outputs and falls below the frontier: it adds objects at lower precision than the fine-tuned model would at that count. No other lever has a residual whose CI excludes zero. The FAIR version's negative result on 4-bit DPO is consistent with E5 DPO here, but it was measured on different (VSPS) data and is not repeated as a result of this paper.

## 6.7 What the negatives have in common

Each lever increased the number of mentioned objects or changed caption style. Each raw gain disappeared once the comparison was made at equal count, or against an independent panel. On KTVIC, raw object F1 and CIDEr cannot tell a better system from a more talkative or differently punctuated one. The count-matched controls can, and none of these levers passed them.
