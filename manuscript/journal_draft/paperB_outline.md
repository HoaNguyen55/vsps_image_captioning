# Paper B: outline (Vietnamese image captioning: a controlled system and a dataset-validity audit)

Date: 2026-10-15. Plan: `.session_backup/2026-10-14/two_paper/PLAN_2PAPERS.md`. Draft due 2026-12-20; submit by 2027-01-25.
Venue: JVCIR or ACM TALLIP if a method wins under count control; otherwise a resource/audit framing for Language Resources & Evaluation or TALLIP [quartiles UNVERIFIED].
Overlap rules: disjoint primary claims with Paper A; each paper cites the other as under review; ≥ 30% new content over FAIR 2026, with the FAIR version disclosed. A number may be primary in only one paper.

Same number rules as Paper A: only traced numbers; each with `<!-- src: path :: key -->`; no OpenViIC caption text; untraceable values (see Paper A `results_plan.md`, "Do-not-use list") never appear.

## Working title options

1. A Controlled Baseline and a Validity Audit for Vietnamese Image Captioning
2. What KTVIC Measures: Single-Writer References, Punctuation and Matchers in Vietnamese Captioning Evaluation

## Sections

1. **Introduction.** Vietnamese captioning benchmarks (KTVIC, UIT-ViIC, UIT-OpenViIC); why reported CIDEr differences are hard to compare; contributions. Points to Paper A for the general count/gold theory.
2. **Related work.** Vietnamese captioning systems and datasets (GRIT 136.0, ViG, HDUCap — protocols to be extracted, PD-2 blockers 1–2); Qwen2.5-VL adaptation; reference-based metrics and protocol signatures (sacreBLEU, SacreEOS).
3. **Controlled baseline.** Response-only P1 recipe on Qwen2.5-VL-7B; protocol card (segmenter, CIDEr variant, ×100, punctuation handling).
4. **Ladder: frontier invariance across training recipes** (pre-registered `manuscript/prereg/2026-10-12_ladder_predictions.json`, commit 1b5d16b; interpretation addendum `2026-10-14_ladder_interpretation_addendum.md`, uncommitted).
5. **Second backbone (B1) and transfer to UIT-ViIC.**
6. **KTVIC dataset audit.** (a) single-writer references; (b) no punctuation in references and the CIDEr cost of one period; (c) matcher versions v1/v2/v3; (d) KTVIC–OpenViIC image overlap.
7. **Two caption panels disagree (C3).** KTVIC references vs an independent OpenViIC panel on the same test images (aggregates only); linear gate $L = \Delta\rho_I - 0.35\,\Delta\rho_A$.
8. **Evidence-adding method.** Text-kNN prior (P1 test vs both controls + panel gate), then M3 count-matched DPO if the probe AUROC gate passes.
9. **Pre-registered negatives** (11 families; one table + supplement).
10. **Limitations, licences and ethics** (OpenViIC aggregates only; KTVIC no licence file; AI-agent provenance rules as in Paper A §11.3).

## Traced numbers already available

### §3 Baseline
| Quantity | Value | Source |
|---|---|---|
| KTVIC test word-level CIDEr, P1 (p1assist) short, seeds 42/43/44 | 148.66 / 148.06 / 147.96 | `data/results/p1assist_s{42,43,44}-short.json :: results[0].scores_scaled_x100.CIDEr` |
| mean (SD) over 3 seeds | 148.23 (0.38) | computed from the three keys above (TODO: write to a JSON key) |
| segmenter | rdrsegmenter (VnCoreNLP-1.2) | same files :: `results[0].segmenter` |
Pending: protocol-matched comparison with GRIT 136.0 / ViG / HDUCap (PD-2 blockers 1–2). No SOTA claim.

### §4 Ladder
| Quantity | Value | Source |
|---|---|---|
| 54_p1_4ep_s42 short: M / P / R | 1.7258 / 77.5701 / 39.772 (all inside the frozen intervals) | `.session_backup/2026-10-14/r11_verify/c7_54_p1_4ep_s42_evaluation.json :: system_summaries.p1ep4_s42-short.ktvic_5ref_object_prf_raw.{M,P_micro,R_macro}` |
| its frontier residual P | −1.5946 pp [−3.4578, +0.2019] | same :: `prereg_ladder_check_v4.p1ep4_s42_short.frontier_residual_P_pp`, `_ci95_pp` |
| joint residual, 5 landed runs | −0.5383 pp [−1.5477, +0.5362] | same :: `prereg_ladder_check_v4.joint_frontier_invariance_5_landed_runs.mean_residual_P_pp`, `.ci95_pp` |
Pending: 55_multiref_s42, 58_unf2_s42, 56_cons_s42, 57_rnd2_s42 (machine 1). Note (H6 §1d): T is already refuted on count; the ladder now tests frontier invariance across recipes; rnd2 does not discriminate L from T.

### §5 Second backbone and UIT-ViIC
Pending: B1 (InternVL3-8B or Qwen3-VL-8B; repro gate G-1 first; 3 seeds), B2 scoring on KTVIC / UIT-ViIC / COCO-2500 with v1 and v2 matchers, excluding the 133 UIT-ViIC-train/Karpathy-test images (R11_00 §6; TODO: key). UIT-ViIC transfer numbers from 52_a/52_b: TODO trace (`data/results/uitviic*`); 52_c F2 on hold until the GPU-side script diff is resolved (sha256 now matches the prereg, RV4 2c — TODO: lift the hold formally).

### §6 KTVIC audit
| Quantity | Value | Source |
|---|---|---|
| adjacent-doubleton share, test / train / dev300 (null 0.40) | 0.7102 [0.6696, 0.7518] / 0.6673 [0.6499, 0.6852] / 0.631 [0.5649, 0.6962] | `.session_backup/2026-10-14/r11_verify/c3_n2_exchangeability_all_datasets.json :: k5_exchangeability_audit.ktvic_{test,train,dev300}_objects_in.adjacent_share, _ci95` |
| lag-1 Jaccard excess (test) | 0.135 [0.118, 0.154] | `.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B2_L2_exchangeability.datasets.ktvic_test_objects_in.jac_lag1_minus_mean_lag2to4` |
| slot-wise b(1), slots 1–5 | 0.403 / 0.469 / 0.567 / 0.633 / 0.618; slot 1 − mean(2–5) −0.169 [−0.225, −0.107] | `.session_backup/2026-10-14/r12/H4/out/h4_check.json :: ktvic_ft.gold.s{1..5}.b; ktvic_ft.T3.slot1_minus_slots2to5.b` |
| k_eff of an adjacent pair | 1.755 [1.719, 1.794] (COCO 1.98) | same :: `ktvic_ft.T3.k_eff_adjacent_pair_slots2to5` |
| reference leave-one-out (within-writer, NOT a human ceiling) P / R / F1 | 85.33 / 46.90 / 60.50 | `data/results/human_parity.json :: 1v4.human.{P,R,F1}` |
| references ending with "." (test / train) | 0 / 2,790; 0 / 18,845 | c1 JSON :: `B5_L5_cider_punct_and_uitviic_chair.ktvic_period_audit.*` |
| P1 short outputs with "." / zero-shot short | 0 / 557 of 558 | same :: `p1assist_s42_short_ending_period`, `zeroshot_short_ending_period` |
| CIDEr-D cost of appending "." to P1 outputs, k = 5 refs | −35.17 (−23.66%) from 148.66 | `.session_backup/2026-10-14/r11_verify/c8_l5_d1_d3a_cpu_audit.json :: l5_d1_punct_idf_law.ktvic_test_k1_to_k5_curves.p1assist_s42-short.first_k.k=5.{d_abs,d_rel_pct,cider_strip}` |
| same at k = 1 | −36.17 (−16.73%) | same :: `...first_k.k=1.{d_abs,d_rel_pct}` |
| UIT-ViIC (refs end with "."): appending "." raises CIDEr, KTVIC-transfer P1 | +1.29 [+0.85, +1.77] | same :: `l5_d1_punct_idf_law.uitviic_test_append_period_effect.ktvic_transfer_p1_s43-short.d_abs_add_minus_strip, d_abs_ci95` |
| zero-shot CIDEr raw vs period stripped | 34.33 → 38.02 (+10.74%) | c1 JSON :: `ktvic_period_audit.zeroshot_short_cider_{raw,strip_period,rel_gain_pct}` |
| UIT-ViIC CHAIR_i, matcher v2 → v3 (role/child) | transfer P1 30.02 → 21.39; zero-shot 27.12 → 26.01 (ranking flips; paired CI TODO) | `.session_backup/2026-10-14/r11_verify/c5_n11_uitviic_role_child_audit.json :: uitviic_test.{v2,v3_role_child}.{transfer_p1_s43-short,zeroshot-short}.CHAIR_i` |
| CJK/Vietnamese segmentation: char minus word-token object recall gap, vi | +7.20 pp [+6.48, +7.96] | c8 JSON :: `l5_d3a_xm3600_classifier_fusion_audit` (TODO: exact key) |
| KTVIC test images in OpenViIC train | 401 / 558 (71.86%) | `.session_backup/2026-10-13/r10_cpu/r10_a1_a3_spotchecks_v2.json :: A_32_leakage_disclosure.splits.ktvic_test_558.in_openviic_train, _pct` |
| Chao2 completeness (within-writer sensitivity bound only) | standard 0.8509 [0.8282, 0.8713]; non-adjacent 0.7338 [0.6897, 0.7739] | `.session_backup/2026-10-13/r10_cpu/g2_g3_mt9_verification_v2.json` (TODO: exact keys; values per D17 §1(b), verify) |
Matcher v3 lacks human sign-off ([MODEL] lexicon); v2 stays primary.

### §7 Two panels disagree (C3)
| Quantity | Value | Source |
|---|---|---|
| UPE vs registered COUNT, KTVIC 5-ref gold, 3 seeds image-clustered (F1) | +0.61 [+0.24, +0.98] | `.session_backup/2026-10-13/r10_cpu/mt2_upe_car_shapley.json :: ktvic_test.ktvic_5ref_gold_v2_raw.p1assist_3seed_image_clustered.paired_comparisons.upe_vs_cnt.F1` |
| same on the OpenViIC panel gold | +0.10 [−0.33, +0.46] | same file :: `ktvic_test.openviic_panel_gold_v2_raw.p1assist_3seed_image_clustered.paired_comparisons.upe_vs_cnt.F1` |
| UPE vs (v,g) tie-avg, set-level telescoping A term | −0.02 [−0.32, +0.27] | `.session_backup/2026-10-14/review_gemini_r10/RV1/rc2_out.txt` (TODO: JSON key, RV4 #16) |
| UPE vs COUNT under per-image Dice (D15(i) vote cm), test 3 seeds: ΔA / ΔI / L(0.35) | +0.347 [+0.111, +0.599] / +0.207 [+0.065, +0.362] / +0.086 [−0.059, +0.239] (×100 Dice) | `.session_backup/2026-10-14/r11_verify/c4_n6_linear_gate_residuals.json :: comparisons.upe_mbr_vs_cnt_3seed_image_clustered_test.d15i_vote_cm.{dA_x100,dI_x100,L_dI_minus_035dA_x100}` |
| 35_e vs P1_dev, dev300 (G0 pool), D15(i): κ / L | 0.254 / −0.177 [−1.363, +1.002] | same :: `comparisons.35e_rl_cn_v3_vs_p1dev_dev300_g0pool.d15i_vote_cm.{kappa,L_dI_minus_035dA_x100}` |
| FP mentions confirmed by the panel (test) | 0.531 | c1 JSON :: `B3_L3_two_gold_transfer.raw_summary.test_q3.panel_confirmed_share` |
Required wording: "two caption panels disagree", not "typicality vs truth" (H3: κ = 1.34 on English presence gold). r(ρ_A, ρ_I) across 36 systems is underpowered — do not report as a result. Two implementations of the D15(i) control must be named separately.

### §8 Method
| Quantity | Value | Source |
|---|---|---|
| text-kNN prior, dev300: within-(v,g)-cell AUROC | 0.614 | `.session_backup/2026-10-14/r12/H5/out/h5_cpu.json` (TODO: key) |
| ΔF1 vs (v,g) tie-avg / vs POOL-VOTE (dev300) | +1.16 [+0.02, +2.29] / +0.76 [−0.44, +1.95] | same (TODO: keys); dev only, 3 variants examined |
Pending: kNN P1 on test pools (prereg `manuscript/prereg/2026-10-14_knn_prior.md` per log — TODO: confirm it exists and is committed); EV-RANK (~1.5 GPU-h); M3 (gated on probe within-cell AUROC ≥ 0.58).

### §9 Negatives (one table)
| Family | Traced outcome | Source |
|---|---|---|
| UPE-MBR (kill 2 on 3/3 seeds, panel gold) | panel UPE − COUNT +0.07 / +0.03 / +0.17 | `data/results/upe/test/upe_mbr_ktvic_test.json :: p1assist_s4x.vs_count.panel_obj.F1` (RV1 rc1 confirms) |
| 35_e CIDEr-only RL (KILL, not clean); M4 C2 | +2.07 [−0.20, +4.27] vs registered [−1.5, +2.0] → not held | `.session_backup/2026-10-13/r10_cpu/n11_35e_posthoc_r10_battery_v2.json :: C2_count_matched_delta_in_-1.5_+2.0_ci_contains_0` (TODO: value keys) |
| M6 P-M6b on test | pooled +0.65 [−0.02, +1.34] (rule fixed 44 s before the look, no prereg file) | RV3 recomputation (TODO: JSON path) |
| PLAN-F1 (count shift) | residual −2.49 [−5.52, +0.09] | `check_claude_critique.json` per PD-2 (TODO: path) |
| self-fuse, E5 RFT, MR5, KG, … | TODO: assemble from D8/D11/D12/D14 with JSON keys | — |

## Pending runs (Paper B)
Ladder 55–57 (+58_unf2); B1 3 seeds + B2; kNN P1 test; EV-RANK → M3 (gated); 59 WiSE-FT (N12-D2 prereg first); protocol-matched comparators (CPU reading).
