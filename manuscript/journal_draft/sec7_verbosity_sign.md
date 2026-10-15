# 7 Experiments II: the sign of the verbosity reward across golds

Section 4 predicts that the slope of object F1 on $\ln M$ across a family of systems rises with gold completeness and changes sign at most once, from negative to positive. It does not predict where the crossing lies. This section tests the prediction on fixed outputs. Evidence has three grades, and every row of Table 7.1 carries its grade: **confirmatory** (predictions frozen before the outputs were scored), **failed frozen test** (predictions frozen, and they failed), and **exploratory** (no prediction existed before the look). XM3600 is a frozen out-of-sample test with mixed outcomes (Section 7.5). Two further tests are frozen and pending (a second backbone and large-$k$ reference sets).

The statistic is the one of Section 3.6: the ordinary least squares slope of F1 (points) on $\ln M$ across the systems of one family, with an image-bootstrap interval, for $k$-reference golds built from random $k$-subsets ("random-$k$"), instance labels, and instance labels plus references. Every row reports mixed F1 (Section 3.1); Section 4.5 reports micro-F1 for COCO-2500, with the same sign pattern.

**Table 7.1** (paper Tab. 4). Slope of F1 on $\ln M$ by gold. 95% image-bootstrap intervals.

| Family (systems; mention range) | Grade | 1 ref | 5 refs | Instance | Source |
|---|---|---|---|---|---|
| COCO-2500, Vietnamese outputs, COCO-80 (9; $M$ 0.84–2.14) | confirmatory | −4.28 [−5.91, −2.45] | +11.08 [+9.76, +12.43] | +22.41 [+21.27, +23.48] | C1J `check_coco_gold.*` |
| English LVLMs, OPERA release (9; $M$ 2.18–3.29) | failed frozen test | −35.18 [−40.38, −30.87] | −29.57 [−32.69, −26.37] | +4.24 [−0.09, +8.51] | H3J `families.F-B.gold.*` |
| English LVLMs, Less-is-More release (11; $M$ 2.19–3.37) | failed frozen test | −31.89 [−36.60, −27.21] | −22.86 [−26.71, −18.53] | +6.91 [+2.16, +11.17] | H3J `families.F-C.gold.*` |
| UIT-ViIC test, COCO-80 lexicon (10; $M$ 1.07–2.29) | exploratory | −13.97 [−19.24, −8.01] | +4.80 [−0.57, +9.67] | +37.52 [+34.56, +40.08] | C2J `coco80.*.all_10` |
| UIT-ViIC test, Vietnamese reference lexicon (10; $M$ 1.59–6.94) | exploratory | −17.25 [−20.04, −14.53] | −6.28 [−8.31, −4.29] | +7.66 [+5.78, +9.58] | C2J `vi_objects_in.*.all_10` |
| XM3600-vi, Vietnamese reference lexicon (6; $M$ 1.08–4.29); 5-ref column = all 2–3 refs, instance column = OIV7 verified labels | frozen out-of-sample; 1 of 3 sign predictions failed | −8.99 [−10.89, −6.99] | −2.43 [−4.63, −0.30] (2–3 refs) | +19.32 [+17.43, +21.13] (OIV7) | XMJ `n1_f1_vs_logM_slopes.*` |
| Second backbone, Qwen3-VL-8B zero-shot (G2-B) | frozen, pending | [PENDING] | [PENDING] | [PENDING] | Section 7.6 |

<!-- src rows: COCO-2500: .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B1_L1_mstar_and_stopping.check_coco_gold.{refs1_randk,refs5_randk,inst}.{slope,slope_ci,M_range}.
F-B / F-C: .session_backup/2026-10-14/r12/H3/out/n1_results.json :: families.{F-B,F-C}.gold.{refs1_randk,refs5_randk,inst}.{slope,slope_ci,M_range}.
UIT-ViIC: .session_backup/2026-10-14/r11_verify/c2_n1_uitviic_mstar.json :: uitviic_test.lexicons.{coco80,vi_objects_in}.gold_variants.{refs1_randk,refs5_randk,inst_only}.groups.all_10.{slope_F1_mixed_per_logM,slope_F1_mixed_ci95,M_range}.
XM3600 (XMJ): .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json (sha256 0b2b3aa5e1a3) :: matcher_v2_tone_normalised.n1_f1_vs_logM_slopes.{refs1_randk,refs_all,oiv7_verified}.{slope_F1_per_logM,slope_ci95_b500,M_range}. The vi_objects_in 5-ref interval is the refs5_randk key ([-8.31,-4.29]); the [-8.34,-3.96] quoted in earlier drafts is the refs5_firstk key of the same file (same gold at K=5, different bootstrap draws). -->

## 7.1 COCO-2500: confirmatory

Nine Vietnamese caption systems on 2,500 COCO images (Section 4.5) were scored against English references and COCO instance labels after four predictions had been written down (`check_coco_PREDICTIONS.txt`, timestamped before the run; not committed to version control). All four held<!-- src: .session_backup/2026-10-14/r11_litmaps/L1/check_coco_PREDICTIONS.txt; values below from .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B1_L1_mstar_and_stopping.* -->:

- **P1, order.** slope(1 ref) < slope(5 refs) < slope(instance): −4.28 < +11.08 < +22.41. The slope also rises at every step $k \to k+1$ (−4.28, +2.82, +6.69, +9.16, +11.08)<!-- src: same :: check_coco_gold.{refs1..refs5}_randk.slope -->.
- **P2, instance gold.** The slope is positive with an interval above 0 ([+21.27, +23.48]).
- **P3, one reference.** The micro-F1 optimum $M^*_{\text{micro}} = 1.41$ lies below the family's largest $M$ (2.14), and the slope is negative<!-- src: same :: check_coco_gold.refs1_randk.Mstar_micro, .M_range, .slope -->.
- **P4, sign agreement.** For every gold variant, the sign of the slope equals the sign of $M^*_{\text{mixed}}$ minus the family's median $M$; this holds for 12 of 12 variants<!-- src: same :: check_coco_sign_agree_mixed = "12/12" -->. Because $M^*$ is computed from the same outputs, P4 is a goodness-of-fit check of the power-law frontier rather than a prediction (Section 11.1).

The reproduction of the original run agrees to the second decimal on every slope<!-- src: same :: check_coco_max_abs_diff = 0.0 -->. One sign change, from negative to positive, between one and two references, is what Proposition 1(d) allows and nothing more.

## 7.2 English LVLM outputs: a frozen test that failed

Before scoring, we froze predictions for the public CHAIR outputs of the two English release families used in Section 6 (`N1_PREDICTIONS.txt`, timestamped and hashed, not committed)<!-- src: .session_backup/2026-10-14/r12/H3/N1_PREDICTIONS.txt -->. These systems name more objects than the COCO-2500 family (median $M$ 3.13 and 3.03)<!-- src: .session_backup/2026-10-14/r12/H3/out/n1_results.json :: families.{F-B,F-C}.gold.refs1_randk.median_M -->, so the five-reference prediction was the risky one. Outcomes by registered prediction:

- **P1 (one reference, slope < 0): held** in both families.
- **P2 (five references, slope > 0): failed** in both families (−29.57 and −22.86, intervals well below 0).
- **P3 (instance gold, slope > 0 with interval above 0): held** for the Less-is-More family (+6.91 [+2.16, +11.17]) and **failed** for the OPERA family, whose interval touches 0 (+4.24 [−0.09, +8.51]).
- **P4 (order) and P6 (rise at every step $k \to k+1$): held** in both families: −35.18, −33.87, −32.49, −30.59, −29.57 and −31.89, −29.48, −27.10, −24.63, −22.86<!-- src: same :: families.{F-B,F-C}.gold.{refs1..refs5}_randk.slope -->.

The registered verdict is FAILED. What failed is the location of the crossing, not its direction: the slope rises monotonically with completeness in each family and never crosses back, as Proposition 1 requires, but five references are not enough to turn it positive for systems at $M \approx 3$. The in-sample exponent explains why. With one and five references it is 0.112 and 0.203 in the OPERA family and 0.153 and 0.282 in the Less-is-More family<!-- src: same :: families.{F-B,F-C}.gold.{refs1_randk,refs5_randk}.b -->, against 0.479 and 0.643 on COCO-2500<!-- src: .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B1_L1_mstar_and_stopping.check_coco_gold.{refs1_randk,refs5_randk}.b -->: the marginal mention of a long LVLM caption is far less often named by any reference than the marginal mention of a short caption, so reference gold stays incomplete relative to these systems for longer. An exponent fitted on short-caption systems does not transfer to verbose ones (Section 4.5, "What the proposition does not predict").

The practical consequence is the one that motivates the paper: under five-reference gold, raw object F1 penalizes the more verbose of two LVLMs; under instance gold it rewards it. The two golds can rank the same pair of systems in opposite orders.

## 7.3 UIT-ViIC: exploratory

UIT-ViIC test (231 COCO sports images, five Vietnamese references written by independent annotators; Section 5) was scored before any prediction was frozen, so every number here is exploratory. Ten Vietnamese systems were scored with two matchers. With the COCO-80 lexicon (the matcher used for English outputs), the slope rises from −13.97 with one random reference to +4.80 with five, whose interval includes 0, and to +37.52 with instance labels (Table 7.1). The paired differences are clear: five references minus the first reference +20.70 [+16.35, +25.00], instance minus five references +32.72 [+28.01, +37.27]<!-- src: .session_backup/2026-10-15/paperA_keys/uitviic_paired_diffs.json :: coco80.all_10.diff_refsall_minus_ref1first, coco80.all_10.diff_inst_minus_refsall (one-reference arm = first reference; the random-k arm is not differenced in this file) -->. With the Vietnamese reference lexicon, the slope also rises (−17.25, −6.28, +7.66) but stays negative at five references<!-- src: .session_backup/2026-10-14/r11_verify/c2_n1_uitviic_mstar.json :: uitviic_test.lexicons.vi_objects_in.gold_variants.{refs1_randk,refs5_randk,inst_only}.groups.all_10.slope_F1_mixed_per_logM, slope_F1_mixed_ci95 -->.

We therefore do not claim that the sign flip between one and five references replicates on UIT-ViIC. What UIT-ViIC shows, under both matchers, is the ordering (one reference < five references < instance labels) and a negative one-reference slope; the five-reference sign depends on the matcher, because the two lexicons give different gold sizes and different mention counts (median $M$ 1.39 versus 1.99)<!-- src: same :: uitviic_test.lexicons.{coco80,vi_objects_in}.gold_variants.refs1_randk.groups.all_10.median_M -->. The exponent rises with $k$ under both lexicons, with one dip of −0.003 inside its interval (Section 4.5).

## 7.4 Summary of the completed tests

In every completed test, including XM3600, the slope rises with gold completeness and does not cross back; where references can be added one at a time, it rises at every added reference. In every completed test the one-reference slope is negative and the instance-gold slope is positive or, in one family, has an interval touching 0. The multi-reference sign is positive for short captions with five references (COCO-2500), negative for long English LVLM captions with five references, matcher-dependent on UIT-ViIC, and negative on XM3600 with 2–3 references. The sign of the verbosity reward is therefore a property of the metric under a given gold, relative to the verbosity of the systems compared; it is not a fixed property of "five-reference gold", and it is not a statement about human preference (Section 8).

## 7.5 XM3600: out-of-sample test with a transferred exponent (frozen; mixed outcome)

**Design.** XM3600 (Thapliyal et al., 2022 [CITE: verify]) gives 2–3 Vietnamese references per image and, through Open Images V7, human-verified positive and negative image labels (OIV7). We evaluate six systems on 600 images: Qwen2.5-VL-7B zero-shot and two Vietnamese caption adapters of the same backbone (from the companion paper), each with a short and a detailed prompt. The exponent is not refitted: we transfer $b$ from COCO-2500 (0.479 for one reference, 0.549 for the union of the 2–3 references, using the two-reference value, and 0.846 for instance-type labels) and predict the sign of each slope from $M^*_{\text{micro}} = b\,\bar G/(1-b)$ and the XM3600 gold sizes. The predictions, the evaluation code and the hashes of 11 input files were committed in 4ccbee3 (2026-10-14 23:38 +07), before the first XM3600 output existed (00:29 +07); the registration is valid<!-- src: manuscript/prereg/2026-10-14_xm3600_predictions.json (sha256 5d0134bfded0); manuscript/prereg/2026-10-14_xm3600_predictions.md; git show -s 4ccbee3 -->.

**Frozen predictions** (`manuscript/prereg/2026-10-14_xm3600_predictions.json`, key `a_N1_sign_predictions`):
- N1-XM-1: slope(one random reference) < 0 across the 6 systems ($M^*_{\text{micro}} = 1.471$ with transferred $b$, which the prereg expected to lie below the six systems' median $M$).
- N1-XM-2: slope(all references) > 0 ($M^*_{\text{micro}} = 2.859$). The prereg marks this as the risky test, because Section 7.2 showed that $b$ can compress on verbose outputs.
- N1-XM-3: slope(OIV7 verified) > 0 ($M^*_{\text{micro}} = 11.216$).
- N1-XM-4: slope(one reference) < slope(all references) < slope(OIV7).
- N1-XM-5: for each gold variant, sign(slope) = sign($M^*_{\text{mixed}}$ − median $M$).
- Kill rules: if 2 or more of N1-XM-1 to N1-XM-3 fail, the sign result moves from a core result to an explanatory diagnostic; if N1-XM-1 fails, the one-reference prediction has failed in a third setting and the sign-flip claim is dropped.

**Results** (all six systems landed; verdicts as computed by the registered evaluator from the prereg thresholds)<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json (sha256 0b2b3aa5e1a3) :: prereg_comparisons[16..20].{prediction_id,in_interval_or_pass,observed_value}; pending_runs = [] -->:
- **N1-XM-1: PASS.** One random reference: −8.99 [−10.89, −6.99].
- **N1-XM-2: FAIL.** All 2–3 references: −2.43 [−4.63, −0.30], where a positive slope was predicted.
- **N1-XM-3: PASS.** OIV7 verified labels: +19.32 [+17.43, +21.13].
- **N1-XM-4: PASS.** The ordering one reference < all references < OIV7 holds (−8.99 < −2.43 < +19.32).
- **N1-XM-5: FAIL.** The sign of the slope agrees with the sign of $M^*_{\text{mixed}}$ − median $M$ for 3 of 4 gold variants; the exception is the all-references gold, where the in-sample $M^*_{\text{mixed}} = 1.76$ lies above the median $M$ of 1.38 but the slope is negative. With the transferred exponent, agreement is 2 of 4.
<!-- src: same :: matcher_v2_tone_normalised.n1_f1_vs_logM_slopes.{refs1_randk,refs_all,oiv7_verified}.{slope_F1_per_logM,slope_ci95_b500}; prereg_comparisons[20].observed_value.{in_sample_Mstar_mixed_agreement_count,prior_b_Mstar_micro_agreement_count,per_gold.refs_all.Mstar_mixed_in_sample,per_gold.refs_all.median_M} -->

**Reading.** The sign of the verbosity reward flips between single-reference gold and the OIV7 verified labels, as predicted, and the slopes are ordered by gold completeness, as Proposition 1 requires. The registered prediction that the union of 2–3 references already gives a positive slope failed: on XM3600 the crossing lies at a gold more complete than the available references. The transferred exponent did not locate the crossing; the in-sample exponent for the all-references gold is 0.503, below the transferred 0.549<!-- src: same :: matcher_v2_tone_normalised.n1_f1_vs_logM_slopes.refs_all.b_in_sample; prereg b from .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B1_L1_mstar_and_stopping.check_coco_gold.refs2_randk.b -->, which repeats the lesson of Section 7.2. The one-reference pass also did not come about through the mechanism the prereg gave: the six systems' median $M$ (1.38) lies below the transferred optimum (1.471), not above it<!-- src: same :: prereg_comparisons[16].observed_value.{observed_median_M,prereg_Mstar_all_600_prior_b} -->. The registered kill rule reads: "If ≥ 2 of the 3 out-of-sample sign predictions (`N1-XM-1`, `N1-XM-2`, `N1-XM-3`) fail, `N1` is demoted from a core result to an explanatory lemma / diagnostic" (`manuscript/prereg/2026-10-14_xm3600_predictions.md`, line 64). One of the three failed, so the rule does not fire and N1 stays a core result; the second rule (drop the sign-flip claim if N1-XM-1 fails) does not fire either. What XM3600 supports is the direction and ordering of the sign change, not a prediction of where it occurs.

**Registered gold-size checks.** The prereg also froze the gold sizes $\bar G$ on the 600 images, because the transferred-$b$ predictions depend on them. Of the 15 registered gold-size values, 14 are reproduced exactly by the evaluation; one is out: the mean one-random-reference gold size over images with a non-empty gold is 1.8768 against a registered 1.8831<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: prereg_comparisons[6] (prediction_id GBAR-refs1_randk-Gbar_nonempty; prereg 1.8831, observed 1.8768, in_interval_or_pass = OUT); 14 IN: prereg_comparisons[1..15] -->. We report it as OUT. *Post hoc note (not part of the registered check, not verified by us):* the evaluator attributes the difference to the registered value being a ratio of means and the evaluated value a Monte-Carlo average over random draws. The transferred $M^*$ in N1-XM-1 uses the all-image gold size (1.6000, IN)<!-- src: same :: prereg_comparisons[5] -->, which this value does not enter.

**Exchangeability of XM3600 references.** The prereg ran the adjacency diagnostic of Section 5 before any GPU run, on the 150 XM3600 images with three Vietnamese references. With $K=3$ the exchangeable null is 2/3 (two of the three slot pairs are adjacent). The observed share is 0.533 [0.414, 0.647] (48 of 90 doubletons), at or below the null<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: n2_reference_adjacency_verification.full_3600_150_3ref_images.{adjacent_share,bootstrap_ci95_b5000,adjacent_doubletons,total_doubletons,exchangeable_null_for_K3} -->: no sign of single-writer entry. (TODO: add this row to Table 5.1 / Fig. 5 with its own null.) The XM3600 prereg also froze a test of how far count-controlled differences transfer between the Vietnamese and the English reference panels of XM3600; that two-gold analysis, and the reference-versus-OIV7 predictions of the same prereg, belong to the companion paper (Paper B, under review). The adjacency check (N2-XM-FULL150) is registered and passed.

## 7.6 A second backbone (frozen; pending)

All completed Vietnamese families use one backbone (Qwen2.5-VL-7B). G2-B repeats the frontier measurement with Qwen3-VL-8B zero-shot, on a ladder of three temperatures (0, 0.5, 0.8) × short and detailed prompts, on images outside the backbone's likely COCO training overlap: COCO val2017 (a 295-image clean subset), UIT-ViIC test and XM3600<!-- src: scope ruling .session_backup/2026-10-13/decisions/D15.txt (MT19); extension .session_backup/2026-10-14/r12/H3/REPORT.txt §2 P3 -->.

[PENDING: G2-B extended (Qwen3-VL-8B zero-shot ladder), prereg `.session_backup/2026-10-14/research_r10/G2/REPORT.txt` §4 "Pre-registration" (to be committed to `manuscript/prereg/` before any G2-B output exists).]

Frozen predictions (G2 §4; primary endpoint the paired difference in $b$ with an image-bootstrap interval):
- P1: $b(5\text{ refs}) - b(1\text{ ref}) > 0$ with interval above 0 for the new backbone; $b(\text{instance}) > b(5\text{ refs})$.
- P2: against instance gold, $|b_{\text{EN}} - b_{\text{VI}}| \le 0.05$ (interval inside ±0.05).
- P3: $|b(T{=}0.5\text{ sample family}) - b(\text{greedy prompt family})| \le 0.05$.
- P4: against instance gold, backbones differ in intercept (at least one pair more than 2 precision points apart at matched $M$) while sharing $b$ within 0.05.
- Kill rules: K1, P1 fails on 2 or more datasets: the completeness account is dropped and only "the exponent is dataset-specific" is reported; K2, P2 fails for 2 or more of 3 backbones: the exponent is reported per language; K3, power-law RMSE above 3 precision points within a style-matched family: the frontier is reported only as a local linearization. A one-reference slope of 0 or above on G2-B counts toward the N1 stop rule of Section 7.5 (H3 §3).

## 7.7 Large reference sets (frozen; pending)

Section 4.5 extrapolates the reference limit of the exponent from five points; this is labelled [MODEL] there and is not a registered prediction. B3 tests the monotonicity part of Proposition 1 beyond five references: nocaps validation (10 references per image, Open Images labels) with $k \in \{1, 2, 5, 10\}$, and PASCAL-50S (50 references per image) with $k \in \{1, 2, 5, 10, 20, 50\}$.

[PENDING: B3 large-$k$ (nocaps, PASCAL-50S), prereg `manuscript/prereg/2026-10-14_b3_licence_verification.md` (committed in ca644df; licence gate passed, aggregates only).]

Frozen prediction (B3 prereg §2.1–2.2): $b(k)$ and the F1-on-$\ln M$ slope increase monotonically in $k$ from one reference to the largest $k$, and again to the instance labels (nocaps). The adjacency diagnostic is run on both sets before the slopes are read.
