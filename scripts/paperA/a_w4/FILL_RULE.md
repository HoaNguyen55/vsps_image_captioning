# W4 fill rule (Paper A, CP-111 W4; written and committed before any M3 output)

**Rule.**
- **r4 is the reported COCO row.** r4 (9 systems × 5,000 Karpathy-test images) replaces r0 (9 × 2,500) in every reported COCO cell, as computed, whatever it shows. Its label is "exploratory; post hoc full-split extension (PI-1026c)".
- **What r0 keeps.** r0 stays only as:
  - (i) the discovery row (the set on which the COCO predictions were pre-specified and on which cv295 was drawn);
  - (ii) the source of the registered XM3600 prior b = 0.549 and M* = 1.471 (4ccbee3). §7.5 and its verdicts do not change.
- **Name.** The r4 row is called **COCO-5000** in the text. "COCO-2500" survives only in the r0 roles above.
- **Branches.** Each branch below is decided by the stated key, with no judgment after reading. A frozen config, a prereg and a ruling are never edited.
- **Things that do not change.** The abstract and Amendment 8 are not changed, except through the Amendment 9 rule at the end.
- **Date.** If W4 has not landed by 11-03, A's experiment freeze slips by up to one week and this rule still applies; neither r0 nor a 5-system row becomes the headline (PI-1026f Q2, LOG l.460).
- **Parity-fail path.** If the r4 adapter rows come from it (PI-1026f Q1), the same rule applies. The text adds one disclosure sentence giving the per-run seed-42 mismatch counts that `w4_merge.py full` printed.

**Sources (all aggregates; produced by the commands in `W4_TOPUP_NOTE.md` "Re-score (r4)"; folder `.session_backup/2026-10-26/a_full5000/out/`):**

| Tag | File | What |
|---|---|---|
| C | `r4_full5000_all9.json` | check_coco_full: `gold.<g>.{slope, slope_ci, b, M_range, median_M, Mstar_micro, Mstar_mixed}`, `U`, `tables` |
| H | `h4_r4_full5000_all9.json` | h4 analyse: `T2_microF1_randk.<k>.{slope, slope_ci, Mstar_micro}`, `T2_identity_b_randk`, `median_M`, `T3.k_eff_adjacent_pair_slots2to5`, `T2_profile`, `T2_share_draws_r_monotone_n1to5` |
| B | `a33_r4_full5000_all9.json` | A3.3 bootstrap, re-run (B = 2,000, seed 20261018): `bootstrap.gold.<g>.{Lambda_U, b, U}`, `bootstrap.shares.<c>.b_channel_share`, `bootstrap.refs1_randk_share_of_replicates_with_opposite_signs` |
| F | `cf_r4_full5000_all9.json` | closed form: `coco_free_D`, `coco_D_from_inst+refs` |
| S | `w4_summary.json` | `cells.r4_full5000_all9.{P1_holds, P1_rises_every_step_and_to_inst, P2_inst_ci_above_0, P3_refs1, P4_sign_agree_mixed, P4_holds, kill_fires, channel_share, system_robustness.<col>}` (`<col>` = "1 ref", "5 refs", "label gold") |
| X | `exch_full.json` (W3, already computed) | `manifest_full5000.json.*`: COCO exchangeability on 4,867 images (images and references only; no system enters) |

Rounding follows the r0 text: slopes 2 dp, b and Λ 3 dp, shares in whole percent with the CI to 1 dp in percent, M 2 dp.

## Pre-written branches (CP-111 ruling 7)

**(d) Part (d), sec4.3; Supplementary s4.26 copy.** Let `s_k = H.T2_microF1_randk.<k>.slope` for k = 1..5 and `ci_1 = H.T2_microF1_randk.1.slope_ci`.
- **D1, holds:** s_1 < 0, ci_1[1] < 0, s_2..s_5 > 0 and s_1 < s_2 < … < s_5.
  - Keep the sentence with r4 values: "On COCO-5000 the micro-F1-on-$\ln M$ slope is s_1 [ci_1] at k=1, then s_2 … s_5 for k=2..5. The slope rises monotonically with completeness and changes sign once, from negative to positive; …".
- **D2, unresolved:** s_1 < 0 but ci_1 includes 0. The rise and the k ≥ 2 signs are as in D1.
  - "… is s_1 [ci_1] at k=1, then …. The slope rises monotonically with completeness and is positive from two references on; its sign at one reference is not resolved."
- **D3, no sign change:** s_1 ≥ 0, with the rise as in D1.
  - "… is s_1 [ci_1] at k=1, then …. The slope rises monotonically with completeness; on COCO-5000 it is not negative at one reference, so no sign change is observed. The proposition allows at most one change, from negative to positive; it does not require one."
- **D4, every other outcome:** any pattern that D1-D3 do not match, for example some s_{k+1} ≤ s_k, or a monotone rise with s_1 < 0 and s_2 ≤ 0, or s_k ≤ 0 for some k ≥ 2.
  - Print the values as computed and, where the rise fails, the failing steps: "the slope does not rise from k to k+1 at …"; where a k ≥ 2 slope is not positive, name that k.
  - The Section 4.2 text is not edited by this rule. D4 goes to a CP round before commit 3.
- **The Λ paragraph after (d)**, with `L = B.bootstrap.gold.refs1_randk.Lambda_U` and `q = B.bootstrap.refs1_randk_share_of_replicates_with_opposite_signs`:
  - "at one reference Λ = L.point [L.ci] sits at the boundary" stays iff L.ci includes 0. Otherwise it reads "is positive" or "is negative", by the side of 0 on which L.ci lies.
  - "in q% of bootstrap replicates Λ_U(1) > 0 while the slope is negative": print q as computed.
  - "The negative one-reference sign is therefore an observation, not a consequence of the proposition" stays in D1 and D2 and is dropped in D3.
  - "With M* = H.T2_microF1_randk.1.Mstar_micro against a median M of H.median_M, the systems straddle the optimum" stays iff C.gold.refs1_randk.M_range[0] < M* < M_range[1]. Otherwise it reads "all systems lie below (above) the optimum".
  - "From two references on, Λ > 0 with intervals excluding 0, rising at every step" stays iff `B.bootstrap.gold.refs{2..5}_randk.Lambda_U.ci[0] > 0` and the points rise. Otherwise it names the k that fails.

**§7.8 drop-one, COCO row (sec7 Table 7.3, "Label gold", "Reference gold", "Scope"; sec11:31).** Let `R = S.cells.r4_full5000_all9.system_robustness`.
- **Table 7.3 COCO row:** "COCO-5000 (9)", with R.<col>.{slope_full, loo_min, loo_max, jackknife_t95} for the three columns.
- **G1, one-reference sign survives (R["1 ref"].loo_sign_flips = []).** Keep "The one-reference sign also survives every drop except one. On XM3600 …".
- **G2, it does not (the list is non-empty).**
  - Replace that sentence with: "The one-reference sign survives every drop except on COCO-5000 and XM3600. On COCO-5000, dropping <listed systems> changes it (leave-one-out range R["1 ref"].loo_min to R["1 ref"].loo_max, against R["1 ref"].slope_full with all nine)."
  - "Scope" then reads "… under reference gold its sign depends on the systems in the family: on COCO-5000 on <listed systems>, on XM3600 on one verbose system."
- **Jackknife list.** "The one-reference jackknife interval includes 0 on COCO-5000 (system-level correlation of F1 with ln M R["1 ref"].system_r), …": COCO-5000 is listed iff `R["1 ref"].jackknife_t95_excludes_0` is false.
- **Label gold.** "Dropping any one system never changes the sign of the label-gold slope, in any family" stays iff R["label gold"].loo_sign_flips = [].
  - Otherwise it reads "in every family except COCO-5000 (<systems>)". Amendment 9 applies.
  - "smallest leave-one-out slope +1.49, Less-is-More" changes only if R["label gold"].loo_min < 1.49.
  - COCO-5000 is in the "jackknife excludes 0" list iff `R["label gold"].jackknife_t95_excludes_0`.

**Within-prompt contrast (sec7.8 "Within one prompt and zero-shot only").** Let `P = R["1 ref"].subsets` and `Q = R["label gold"].subsets`.
- **Label-gold half.** "the label-gold slope is positive in every subset whose mention counts differ by more than 10%" stays iff every Q subset with lnM_spread > ln 1.1 has slope_full > 0. Otherwise it names the subset.
- **W1, contrast holds (P["prompt=short"].slope_full and P["prompt=detailed"].slope_full have opposite signs).** Keep: "among COCO-5000's four short-prompt systems it is <short>, among its five detailed-prompt systems <detailed>".
- **W2, same sign.** "The one-reference slope is not: on COCO-5000 it is <short> among the four short-prompt systems and <detailed> among the five detailed-prompt systems, and on XM3600 neither three-system prompt subset keeps its sign when one system is dropped."
- Add "(not stable when one system is dropped)" after a COCO-5000 subset value whose `sign_stable_under_loo` is false.

## Replacement list (CP-111 W4); every reported COCO cell, r0 → r4

| Location (2026-10-26) | Current r0 content | r4 source | Ready |
|---|---|---|---|
| sec1:5 | "On 2,500 COCO images and 9 systems": −4.28 [−5.91, −2.45], +11.08 [+9.76, +12.43], +22.41 [+21.27, +23.48] | C.gold.{refs1_randk, refs5_randk, inst}.{slope, slope_ci}; "On the 5,000 COCO Karpathy-test images and 9 systems" | yes |
| sec3:7, sec3:11 | name "COCO-2500" | "COCO-5000" | yes |
| sec3:21 | b 0.479 / 0.643 / 0.846 "on the same 9 COCO systems" | C.gold.{refs1_randk, refs5_randk, inst}.b | yes |
| sec4.3 heading and opening | "Post hoc descriptive checks on COCO-2500"; 9 systems; M 0.84–2.14; the W5 seed-42 half sentence | "COCO-5000"; C.gold.inst.M_range. The W5 half sentence is replaced by: "COCO-5000 is the full Karpathy test split (5,000 images); all nine systems were decoded on every image, four of them (the two adapters, each with both prompts) in a post hoc top-up of the 2,500 images outside the seed-42 discovery half (PI-1026c)." | yes |
| sec4.3 (a) | b(k) 0.479 → 0.643, 0.846 | C.gold.{refs1_randk, refs5_randk, inst}.b | yes |
| sec4.3 (A2) | ratios 1.86, 1.25, 0.80, 0.48, 0.26; 100% monotone; 3.20 | H.T2_profile.{n1..n5, n0_inst}.ratio_r; H.T2_share_draws_r_monotone_n1to5 | yes |
| sec4.3 (d) | −1.84 [−3.14, −0.55]; +5.78, +9.96, +12.71, +14.69 | H.T2_microF1_randk.<k>; branch (d) | yes |
| sec4.3 Λ paragraph | Λ 0.047 [−0.027, 0.122]; 88%; M* 1.26; median 1.19 | B.bootstrap.gold.refs1_randk.Lambda_U; B.…share_of_replicates_with_opposite_signs; H.T2_microF1_randk.1.Mstar_micro; H.median_M; Λ-paragraph branch | yes |
| sec4.3 Λ paragraph | "(68% with the alternative matcher)" | A8.4 swapped-matcher bootstrap on r4, printed as computed | A8.4 rule below |
| sec4.3 channel split | 61% [59.7, 62.8]; 71% [69.8, 72.1] | S.channel_share (points; on r0 they equal B's points to 3 dp, 0.613/0.709 vs 0.6127/0.7095, and must again on r4); CIs B.bootstrap.shares.<c>.b_channel_share.ci (the A3.3 bootstrap, re-run) | yes |
| sec5:48 k_eff | 1.98 [1.943, 2.017]; first-k −4.21 vs random-k −4.28 | H.T3.k_eff_adjacent_pair_slots2to5; C.gold.{refs1_firstk, refs1_randk}.slope | yes |
| sec5 COCO exchangeability row | 2,441 images | X manifest_full5000.json (4,867 images) | yes |
| sec7 Table 7.1 COCO row | label, grade, M 0.84–2.14, three slopes | "COCO-5000, Vietnamese outputs, COCO-80 (9; M C.gold.inst.M_range)"; grade "exploratory; post hoc full-split extension (PI-1026c)"; C.gold.{refs1_randk, refs5_randk, inst} | yes |
| sec7 §7.1 | P1 −4.28 … +11.08, +22.41; P2 [+21.27, +23.48]; P3 M* 1.41 < 2.14; P4 12/12 | C.gold.* and the §7.1 rule below | yes |
| sec7 §7.2:34 | "(0.479 and 0.643 on COCO-2500)" | C.gold.{refs1_randk, refs5_randk}.b, "on COCO-5000" | yes |
| sec7 Table 7.3 / §7.8 | COCO row and sentences | S.system_robustness; branches §7.8 and within-prompt | yes |
| sec7 §7.5, sec7:58 | prior b = 0.549, M* 1.471 | **unchanged** (registered prior, r0) | n/a |
| sec7:65 cv295 | "all of which are in the COCO-2500 discovery set" | **unchanged** (r0 role i) | n/a |
| appB:9, appB:12-20 | "No headline change … in 55 checks"; COCO-2500 matcher sensitivity: slopes, micro −1.84 → −2.31, Λ_U(1) "still including 0", shares; the two descriptive changes | A8.4 swapped matcher on r4; appB rule below | A8.4 rule below |
| sec4:56 channel-split sentence | "These shares are post hoc and from COCO-2500 only; there, most of the rise comes from salience-dependent missingness" | sec4:56 rule below | yes |
| supplementary:226 | "COCO-2500 shows the same ordering and endpoint (four of four predictions held)"; "COCO-2500's positive five-reference slope is a dataset-specific outcome" | supplementary:226 rule below | yes |
| Supplementary closed form (l.52) and s4.26 copy (l.299-312) | RMSE, D, 0.67, 0.20; b(k) list; (A2); (d) | F.{coco_free_D, coco_D_from_inst+refs}; C.gold.refs{1..5}_randk.b, inst.b, inst+refs5.b; H as in sec4.3 | yes |
| sec11:29, :31 | "COCO-2500 family"; system-level sensitivity sentence | "COCO-5000"; §7.8 branch outcome (G1/G2) | yes |
| sec11:43 | "Some UIT-ViIC training images are in COCO-2500" | "in COCO-5000" only; no count is printed (CP-111a ruling 7) | yes |
| outline.md contributions (l.4, 51, 52, 81, 105) | "COCO-2500" | "COCO-5000"; numbers as in sec7 | yes |
| outline.md:29, :40 (abstract row 46) | LOO wording | Amendment 9 rule below; no edit otherwise | rule |
| cover_letter_A.md:10 | row-46 wording, no COCO number | Amendment 9 rule only | rule |
| figs/VALUES.json, Fig. 2, Fig. 4 | COCO-2500 points and CIs (keys in VALUES.json; script `scripts/figures/paperA_figs.py` constants `COCO`, `COK`, `A33`) | point `COCO`/`COK` at C and `A33` at B and S, then regenerate both figures and VALUES.json | yes (path swap in the figure script) |
| figs/CAPTIONS.md:7 | "COCO-2500 (exploratory)" | "COCO-5000 (exploratory; post hoc full-split extension)" | yes |
| number_manifest.tsv | r0 rows for every replaced number | one new row per r4 number, keyed to the C/H/B/F/S/X file and key above with its sha prefix; r0 rows stay for the r0 roles (i) and (ii) | yes |

**§7.1 rule (CP-111a W3; keys as registered in `.session_backup/2026-10-14/r11_litmaps/L1/check_coco_PREDICTIONS.txt`, c7cad2b2).**
- The text says the predictions were pre-specified on COCO-2500 (the discovery half), where all four held, and reports each on COCO-5000 as held / did not hold:
  - **P1** held iff `S.P1_holds` (slope(refs1) < slope(refs5) < slope(inst), random-k).
  - **Every-step rise**, reported separately and not as P1: "the slope rises at every step k → k+1 (…) and again to instance gold (…)" stays iff `S.P1_rises_every_step_and_to_inst`. Otherwise it reads "the slope does not rise from k to k+1 at …", naming the steps.
  - **P2** held iff `S.P2_inst_ci_above_0`.
  - **P3** held iff `S.P3_refs1.holds`. Its bound is r4's own upper M, `S.P3_refs1.M_max` (= C.gold.refs1_randk.M_range[1]). This replaces r0's 2.14, and the text prints the r4 value.
  - **P4** held iff `S.P4_holds` (k = n in `S.P4_sign_agree_mixed`); print "k of n gold variants".
- **Kill condition** (P2 fails, or slope(refs1) ≥ slope(inst)), evaluated on r4 as `S.kill_fires`. If it fires, §7.1 prints the values and the outcome as computed and goes to the commit-3 CP round. Nothing else in §7.1 changes on that account.

**sec4:56 rule.** Let `sh = B.bootstrap.shares.refs1_to_refs5.b_channel_share.point`.
- "COCO-2500 only" becomes "COCO-5000 only".
- "there, most of the rise comes from salience-dependent missingness, which a uniform (SCAR) correction cannot remove" stays iff sh > 0.5.
- If sh ≤ 0.5, it reads "there, the b-channel carries <sh, %> of the rise, so salience-dependent missingness is not the larger part of it".

**supplementary:226 rule.**
- The pre-specification sentence keeps COCO-2500 in r0's role: the predictions were pre-specified (file timestamp 2026-10-14 07:22Z, never committed), so the test is exploratory.
- "(four of four predictions held)" becomes "(k of four predictions held on COCO-5000)", with k counted over the §7.1 keys `S.P1_holds`, `S.P2_inst_ci_above_0`, `S.P3_refs1.holds` and `S.P4_holds`.
- "shows the same ordering and endpoint" stays iff `S.P1_holds` and `S.P2_inst_ci_above_0`. Otherwise it names the one that fails.
- "COCO-2500's positive five-reference slope is a dataset-specific outcome" becomes "COCO-5000's …". The sentence stays iff C.gold.refs5_randk.slope > 0. Otherwise it is dropped.

**appB rule** (keys of the patched A8.4 `sensitivity.json` on r4; the r0 file is `.session_backup/2026-10-18/paperA_tasks/A8.4/sensitivity.json`).
- **appB:9.** "No headline change. No verdict, ordering, endpoint or sign changes in N checks" stays iff `answer.any_headline_change` is false, with N = `answer.headline_checks_evaluated`. Otherwise "Headline changes:" lists `answer.headline_changes` as computed.
- **appB:12-15.** The value shifts are printed as computed from the `coco2500_*` blocks (`.original` → `.swapped.nodes`). "with its interval still including 0" stays iff `coco2500_lambda_U_bootstrap.values.gold.refs1_randk.Lambda_U.ci.swapped.nodes.value` includes 0. Otherwise it reads "with its interval now excluding 0, above (below) it".
- **appB:17-20.** The descriptive changes are printed as computed from `answer.other_changes`.
- **The §4.3 '(68% with the alternative matcher)'** is printed as computed: `coco2500_lambda_U_bootstrap.values.refs1_randk_share_of_replicates_with_opposite_signs.swapped.nodes.value`.

**A8.4 copy rule (CP-111a W5 (vi)).**
- The patched copy of `a8_4_sensitivity.py` changes argv handling only (manifest, instance gold, system set and output path, as in `check_coco_full.py`). This is checked by a diff committed with it.
- It must reproduce the frozen r0 `sensitivity.json` exactly, and it is committed before the r4 re-score.
- If it does not reproduce by the commit-3 CP round:
  - the §4.3 parenthetical "(68% with the alternative matcher; Supplementary S2)" is dropped;
  - appB is labelled "matcher sensitivity on COCO-2500 (r0), not re-run on COCO-5000".

## Amendment 9 (CP-111 ruling 8)

After r4, check the COCO leave-one-out signs for one reference and for label gold:
- `S.cells.r4_full5000_all9.system_robustness["1 ref"].loo_sign_flips`
- `S.cells.r4_full5000_all9.system_robustness["label gold"].loo_sign_flips`

**If both lists are empty:** abstract row 46 (Amendment 8; outline.md:40) and outline.md:29 stand. No amendment is written.

**If either list is non-empty:**
- CONFIRMATION_MAP Amendment 9 is written, with the wording as computed, for row 46 and outline.md:29 (and cover_letter_A.md:10).
- It goes through a CP round and the gatekeeper.
- The abstract is not edited before that.
