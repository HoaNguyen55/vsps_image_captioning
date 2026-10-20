# Paper A: results plan and number status

Date: 2026-10-15 (updated after drafting §6–§10). For each planned table and figure: what exists (file + JSON key), what is pending, and what decides the text.
Abbreviations: `C1J` = `.session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json`; `H4J` = `.session_backup/2026-10-14/r12/H4/out/h4_check.json`; `H3J` = `.session_backup/2026-10-14/r12/H3/out/n1_results.json`; `H1J` = `.session_backup/2026-10-14/r12/H1/pilot_results.json` (reproduction: `.session_backup/2026-10-14/r12_verify/h1_pilot_repro.json`); `E1J` = `.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json`; `C2J` = `.session_backup/2026-10-14/r11_verify/c2_n1_uitviic_mstar.json`; `C6J` = `.session_backup/2026-10-14/r11_verify/c6_n3_rlaifv_rlhfv_audit.json`.

Status legend: **READY** (all numbers traced) · **PARTIAL** · **PENDING** (needs a run) · **BLOCKED** (needs a decision or a fix first).

## Do-not-use list (withdrawn or untraceable)

| Value | Why | Source of the ruling |
|---|---|---|
| UIT-ViIC slopes −9.94 → +12.14 → +22.87, M* 1.97/3.06/4.50, key `FT_pooled_3sys` | in no artifact | RV4 item 1a; D17 §1(g) C2 |
| md table −18.30 / +9.11 / +17.45 (UIT-ViIC) | contradicts its own JSON | RV4 item 1a |
| Chao2 "debiased" human ceiling 0.9468 → 0.848 | script bug (b_pool(1) = 1.01) | R10_00 correction box; R11_00 §6.6 |
| Chao2 0.7325 [0.7131, 0.7519]; LOO ceiling F1 0.7072 (P 0.9317, R 0.5698); "70.7% vs 61.5%" | hard-coded literals | H6 §1a(v); D17 §1(b) |
| C4 log values −0.0431, −0.5841, −0.5690, −4.6143, etc. | in no artifact | RV4 item 2a |
| UPE vs (v,g) "−0.12 [−0.29, +0.06]" | not reproduced | RV1 item 2 |
| E4 75.56% / 99.82% / +8.22 | wrong | R11_00 §6.2 |
| "count beats length" on English | X1 P-B killed | E1J `x1_pb_english.summary.x1_pb_verdict` = KILL_CI_CONTAINS_0 |
| "N1 replicated on UIT-ViIC" | post hoc; 5-ref sign depends on matcher | PD-4 Q1; RV4 1d |
| Any number from Gemini prose/logs/D-files without a JSON key | reliability pattern | CONTEXT_R12 §3; D17 binding cond. 2 |

## Tables

### Tab. 2 — E1 specification curve (15 published decoding comparisons) — PARTIAL (text §6; K2 placebo pending)

| Quantity | Value | Source |
|---|---|---|
| comparisons | 15 | E1J `overview_15_pairs.n_pairs` |
| raw precision gain significant | 12/15 | E1J `overview_15_pairs.raw_dP_sig_pos` |
| MCP prefix (protocol primary; post hoc): unadjusted / Holm+SESOI | 3/15 / 2/15 | E1J `overview_15_pairs.mcp_prefix_sig_pos_unadj`, `.mcp_prefix_survives_holm` |
| sentence tie-avg: unadjusted / Holm+SESOI | 4/15 / 2/15 | E1J `.mcp_sent_tieavg_sig_pos_unadj`, `.mcp_sent_tieavg_survives_holm` |
| uniform random subset: unadjusted / Holm+SESOI | 11/15 / 6/15 | E1J `.mcp_rand_exact_sig_pos_unadj`, `.mcp_rand_exact_survives_holm` |
| significant reversal (MCP prefix, unadjusted) | 1/15 | E1J `.mcp_prefix_sig_neg_unadj` |
| mean ΔP: raw / prefix / sent tie-avg / random | 3.407 / 0.621 / 0.652 / 2.764 | E1J `.mean_dP_raw`, `.mean_dP_MCP_prefix`, `.mean_dP_MCP_sent_tieavg`, `.mean_dP_MCP_rand_exact` |
| share of raw gain explained by count + allocation (descriptive; shared baselines) | 81.8% (prefix), 80.9% (sent) | E1J `.pct_gain_explained_by_count_and_alloc_prefix`, `_sent_tieavg` |
| K4 verdict by control | NOT_TRIGGERED (prefix, sent), TRIGGERED (random) | E1J `.k4_en_verdict_*` |
| K3 positive control (drop-1, ≥ +3 P) | 6/8 point, 3/8 CI lower bound | E1J `controls_K2_K3.registered_k3_en_summary.point_ge_3_count`, `.ci_lo_ge_3_count` |
| per-pair rows | 15 rows; §6.2 quotes 3 pairs (InstructBLIP vs greedy, MiniGPT-v2 r12, Shikra vs beam5/greedy) | E1J `pairs_15.*` (TODO: Appendix C table generator, with per-pair MDE) |
| X1 P-B (count vs length), signed | +0.186 [−0.257, +0.579] → KILL | E1J `x1_pb_english.summary.kill_rule_assessment_v2.PB_signed_mean_15pairs_est/_ci95` |

Pending: **E1 K2 seed placebo** (2 sampling seeds of LLaVA-1.5-7B on CHAIR-500; ~0.5–1 GPU-h; in the N9 harness). It decides which control is primary (|ΔP| ≤ 0.5 and CI ∋ 0). Note: the random-subset control fails its own two-seed check in 2/8 rows (key confirmed: E1J `controls_K2_K3.placebos_K2.two_seed_random_subset.<baseline>.passes_K2`, 6 true of 8). The self-swap substitute placebo passes 15/15 but is null by construction (`substitute_placebos_metadata.is_registered_two_seed_placebo` = False). `.session_backup/2026-10-14/r12_verify/n9_e1_k2_seed_placebo.json` is a KTVIC multi-seed band (Paper B data), NOT the registered English K2 placebo. Text: §6.2–6.3. Pending: K3 action "enlarge to 2,000 images" (a rule of the post hoc E1 protocol, not taken). Text rule: always report the curve, never one number.

### Tab. 3 — N9 count-matched leaderboard of training-based methods — PENDING

9 public LLaVA-1.5-7B checkpoints (POVID, RLAIF-V, HALVA, CHAIR-DPO, SENTINEL, HA-DPO, HSA-DPO, OPA-DPO, …) on CHAIR-500, scored raw / MCP / tie-avg / CAR. ~6 GPU-h, machine 1 after the ladder. Prereg must be committed first (L6 §3 D1 predictions; checkpoint revisions and licences; primary control by the placebo rule). No numbers exist.

### Tab. 4 — verbosity slope by gold — PARTIAL (text §7; XM3600 done; G2-B, B3 pending)

| Row | Status | Values (slope of F1 on ln M, 95% CI) | Source |
|---|---|---|---|
| COCO-2500, 9 systems, **exploratory** (frozen locally 2026-10-14 07:22Z, never committed) | READY | refs1 −4.28 [−5.91, −2.45]; refs2 +2.82; refs3 +6.69; refs4 +9.16; refs5 +11.08 [+9.76, +12.43]; inst +22.41 [+21.27, +23.48]; inst+refs5 +24.16 [+23.10, +25.06] | C1J `B1_L1_mstar_and_stopping.check_coco_gold.<gold>.slope/.slope_ci`; frozen file `.session_backup/2026-10-14/r11_litmaps/L1/check_coco_PREDICTIONS.txt` |
| COCO-2500 micro-F1 | READY | −1.84 [−3.14, −0.55]; +5.78; +9.96; +12.71; +14.69 | H4J `coco2500.T2_microF1_randk.{1..5}.slope` |
| English LVLM F-B (OPERA, 9 systems), **frozen locally (12:43Z, never committed), FAILED; exploratory** | READY | refs1 −35.18 [−40.38, −30.87]; refs5 −29.57 [−32.69, −26.37]; inst +4.24 [−0.09, +8.51] | H3J `families.F-B.gold.*`; frozen `.session_backup/2026-10-14/r12/H3/N1_PREDICTIONS.txt` |
| English LVLM F-C (LiM, 11 systems), frozen locally (never committed); exploratory | READY | refs1 −31.89 [−36.60, −27.21]; refs5 −22.86 [−26.71, −18.53]; inst +6.91 [+2.16, +11.17] | H3J `families.F-C.gold.*` |
| KTVIC 36 FT, random-k — **Paper B owns (PD-6); not in A** | moved | −3.32 [−6.19, −0.48]; +3.77; +8.42; +11.94; +14.15 | C1J `check_mstar_gold.k{1..5}_randk.ft.slope_F1_per_logM` |
| KTVIC slot-1 diagnostic (first-k) — **Paper B owns; not in A** | moved | −10.65 [−13.87, −7.28] | C1J `check_mstar_gold.k1_firstk.ft` |
| UIT-ViIC test, 10 systems, exploratory, COCO-80 lexicon | READY | refs1(first) −15.90 [−20.69, −10.72]; refs5 +4.80 (CI touches 0); inst +37.52 | C2J `uitviic_test.lexicons.coco80.gold_variants.{refs1_firstk,refs5_randk,inst_only}.groups.all_10.slope_F1_mixed_per_logM` (+ `_ci95`) |
| UIT-ViIC, vi_objects_in lexicon | READY | refs1 (random) −17.25 [−20.04, −14.53]; refs5 −6.28 [−8.31, −4.29] (no flip); inst +7.66 [+5.78, +9.58]. CORRECTED 2026-10-15: [−8.34, −3.96] is the `refs5_firstk` key, not `refs5_randk` (same gold at K=5, different bootstrap draws); sec11 §11.1 still quotes [−8.34, −3.96] against the randk key | C2J `uitviic_test.lexicons.vi_objects_in...all_10` |
| UIT-ViIC paired differences | READY via RV4 | refs5 − refs1 +20.70 [16.35, 25.00]; inst − refs5 +32.72 [28.01, 37.27] (coco80, all_10) | `.session_backup/2026-10-15/paperA_keys/uitviic_paired_diffs.json :: coco80.all_10.{diff_refsall_minus_ref1first,diff_inst_minus_refsall}` (= RV4 `rv4_n1.json`, same keys) |
| **XM3600** (600 images, 2–3 VI refs, OIV7 verified labels), out-of-sample with b transferred from COCO | **READY — mixed** (6/6 systems): refs1_randk −8.99 [−10.89, −6.99] (N1-XM-1 PASS); refs_all −2.43 [−4.63, −0.30] (N1-XM-2 FAIL, >0 predicted); OIV7 +19.32 [+17.43, +21.13] (N1-XM-3 PASS); ordering PASS; N1-XM-5 FAIL (3/4 in-sample, 2/4 transferred-b); GBAR 14/15 IN (refs1_randk Gbar_nonempty OUT); N2-XM-FULL150 PASS (post hoc). Kill rule (registered; prereg .md line 64, ≥2 of 3 out-of-sample failures demote N1): 1/3 failed → N1 stays core. C3-XM-PANEL (Paper B) MIXED: no primary estimator registered; vi113→en80 κ CIs < 1, vi80→en80 CIs include 1. Interim +11.13 (3 short systems) withdrawn from text. PROVENANCE: the six XM3600 result JSONs were rewritten in place by Gemini to add provenance after the interim run (e.g. zeroshot-short now sha256 98b56686, zeroshot-detailed 7afd233e); manifest uses the current shas recorded in `landed_result_files` | `.session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json` (0b2b3aa5e1a3) `matcher_v2_tone_normalised.n1_f1_vs_logM_slopes.*`, `prereg_comparisons[*]`; result files `data/results/xm3600/*.json` |

Text rules: COCO is the only confirmatory row with all predictions held; XM3600 is a committed out-of-sample test reported with its failure (N1-XM-2). No KTVIC number appears in Paper A (PD-6 Q1(a); coordinator ruling 2026-10-15). Do not claim the UIT-ViIC 1→5-ref flip. Kill rule (H6 P2): if ≥ 2 XM3600 sign predictions fail, the sign result moves from "core" to "explanatory".

### Tab. 5 — human validity — READY (all four sets; text §8)

| Quantity | THumB (500 img, 2,500 caps) | Composite (1,996 img) | Source |
|---|---|---|---|
| −CHAIR vs expert P, pairwise agreement, refs1 / refs4 / full gold | 0.736 / 0.797 / 0.903 | — | H1J `THumB.agree.negCHAIR|{refs1,refs4,full}|P|all.est` |
| −CHAIR vs total, refs1 / refs4 / full | 0.627 / 0.714 / 0.793 | 0.743 / 0.838 / 0.873 | H1J `*.agree.negCHAIR|{refs1,refs4,full}|T|all.est` |
| count-equal vs count-differing pairs (−CHAIR, full, vs total) — exploratory | 0.846 vs 0.773 | 0.946 vs 0.838 (`Composite.agree.negCHAIR|full|T|{ceq,cdiff}.est`) | H1J `THumB.agree.negCHAIR|full|T|ceq.est`, `...|cdiff.est` |
| P1b residual z minus −CHAIR vs total (count-differing) | −0.190 [−0.277, −0.108] | −0.083 [−0.101, −0.065] | H1J `*.P1b_acc(z->T)-acc(-CHAIR->T)` |
| P1a −CHAIR minus z vs expert P | +0.325 [+0.247, +0.398] | +0.097 [+0.079, +0.116] | H1J `*.P1a_acc(-CHAIR->P)-acc(z->P)` |
| human preference for larger-M caption | 0.481 [0.429, 0.530] | 0.525 [0.506, 0.544] | H1J `*.P2a_v_human` |
| F1 preference for larger M: refs1 / refs4 / full | 0.41 / 0.66 / 0.83 | 0.54 / 0.66 / 0.73 | H1J `*.P2b_v_F1_{refs1,refs4,full}` |
| P3: β(FP) vs β(pseudo-FP) on expert P | −1.16 vs −0.09 (diff +1.07 [+0.82, +1.32]) | −1.16 vs −0.48 (failed) | H1J `THumB.P3_ols_P.*`, `Composite.P3_ols_P.*` |
| corr(M, total), caption level | −0.05 | −0.016 | H1J `THumB.corr_pearson_spearman.M|-|T` |
| P4 matched-count wins agree with humans | 0.846 (n 91) | 0.946 (n 928) | H1J `*.P4_clean_T` |
| Verdicts under the frozen rules (frozen locally, never committed; exploratory) | P1a held ×2; P1b failed ×2; P2c failed (kill fired); P3 held (T) / failed (C); P4 underpowered (T) / failed (C); P5 failed | | `.session_backup/2026-10-14/r12/H1/PREDICTIONS_FROZEN.txt`, H1 REPORT §1b |
| **Polaris-COCO** (G2; frozen locally before analysis, committed after the first output; exploratory) | **READY — PASS** (H-a, H-b, H-c all held; no kill). Text §8.3 | | prereg `manuscript/prereg/2026-10-14_h1_polaris_docci.md`: the Polaris/DOCCI pre-registration was committed in 7f22d13 (23:47 +07) after the results JSON was written (23:25 +07); this order is disclosed. The G3 verdict under the pre-specified rules, computed with the COCO-80 matcher, is MIXED; results with the ExpandedNouns lexicon are exploratory only |
| **DOCCI-Critique** (14 VLMs, long paragraphs) | **READY — MIXED** (G3-(i) primary FAILS: median within-VLM slope +0.000371; G3-(ii) Δτ +0.1538 micro / +0.2198 macro ≥ +0.10 but CI [−0.2637, +0.3077] ∋ 0). COCO-80 primary; ExpandedNouns exploratory, no numbers in text. G3-(ii) HELD (the rule has no CI clause); exploratory. Text §8.4 | `.session_backup/2026-10-14/r12_verify/h1_g3_registered_supplement_v2.json` (718fc3f01743) `registered_G2.*`, `registered_G3.*` | same prereg and same timing disclosure; CC BY 4.0 |

Label: the gold-completeness agreement rows (THumB 0.736/0.797/0.903 vs P; 0.627/0.714/0.793 and Composite 0.743/0.838/0.873 vs total) and the ceq/cdiff rows are EXPLORATORY (H1 REPORT §1c); Polaris G2 H-a/H-b registers them. sec1 (Human validity paragraph) quotes 0.736→0.903 without the exploratory label — fix there.
Licence: THumB and Composite have no licence file — aggregates only. Frozen-prediction caveat: H1's predictions were written and hashed before any human statistic, but not git-committed: frozen locally (file timestamp 2026-10-14 12:52Z, never committed); treated as exploratory.

| **LongCap-Arena** (PD-7 Q2; prereg 7254a39) | **READY — MIXED**: (i) PASS, Relevance slope −0.024/class [−0.029, −0.020]; (ii) FAIL + kill, Δτ_b −0.028 [−0.036, −0.019]; (iii) FAIL + kill, −0.017 [−0.035, +0.0003]. Declared design changes (pooled, caption-level, across-image pairs); COCO-80 finds 1.23 classes/caption. Run history: first run crashed writing JSON (numpy bool) after test (ii); re-run unchanged via wrapper 0cd8e9a; no console statistic, partial file (data_summary + test i) overwritten. Text §8.1 | `.session_backup/2026-10-15/r13_human/q2_longcap_arena.json` (50f3a8635fce) |
| **CapArena** (PD-7 Q3) | DROPPED: no licence statement | `.session_backup/2026-10-15/r13_data/licence_check_2026-10-15.json` |

### Tab. 6 — preference-data count audit — READY (+ VaPR positive control PASS: count-matched 0.849 [0.845, 0.853] vs 0.473/0.692/0.349; `.session_backup/2026-10-15/r13_human/q4_vapr_count_control.json` 4fcea1cc1bf2; text §9)

| Dataset | pairs with objects | count-matched share | chosen names fewer, among unmatched [95% CI] | mean Δk | Source |
|---|---|---|---|---|---|
| POVID | 16,483 | 0.521 | 0.444 [0.433, 0.455] | +0.114 | C6J `summary_table_7_datasets.povid.*` |
| HA-DPO | 5,181 | 0.473 | 0.882 [0.870, 0.894] | −0.691 | C6J `.hadpo_llava15.*` |
| HSA-DPO | 8,076 | 0.692 | 0.817 [0.801, 0.832] | −0.250 | C6J `.hsadpo.*` |
| mDPO (VLFeedback) | 9,281 | 0.408 | 0.498 [0.485, 0.511] | −0.103 | C6J `.mdpo_vlfeedback.*` |
| SENTINEL | 8,600 | 0.349 | 0.897 [0.889, 0.904] | −0.736 | C6J `.sentinel_llava15_7b.*` |
| RLHF-V | 5,120 | 0.632 | 0.702 [0.681, 0.722] | −0.234 | C6J `.rlhfv.*` |
| RLAIF-V | 70,029 | 0.590 | 0.514 [0.509, 0.520] | −0.017 | C6J `.rlaifv.*` |
| length-matched (|Δwords| ≤ 2) subsets | per row | | e.g. HA-DPO 0.854, SENTINEL 0.886 | | C6J `.<ds>.abs_dwords_le_2_chosen_fewer_among_unmatched` |

Note: RLHF-V is count-biased and RLAIF-V near-neutral (Gemini's log had this reversed; RV4 2b). Matcher: CHAIR COCO-80. The L6 D2 prediction (RLAIF-V ≥ 0.60) FAILED; RLAIF-V 0.514 is inside the kill interval [0.45, 0.55]; the conjunctive kill also needs N9 D1 (no Δk→Δm link) — PENDING N9 (§9). Status: READY (text §9).

### Tab. 7 — prereg ledger — TO COMPILE

Rows: COCO-2500 N1 (frozen locally, never committed; L1), H3 LVLM N1 (frozen locally, never committed; FAILED), H1 THumB/Composite (frozen locally, never committed), E1 (post hoc: protocol written after the pilot; K2 registered, not run), X1 P-B (frozen locally, committed after its first output; killed), XM3600 (committed 4ccbee3 23:38 +07 before first result 00:00 +07: registered), Polaris/DOCCI (committed 7f22d13 23:47 +07 after results JSON 23:25 +07: exploratory; G3 COCO-80 verdict MIXED; ExpandedNouns exploratory), N9 (registered in b8b2500). Each row: registration commit/time, first-look time, verdict. Sources: H6 P9; RV4 1b.

### Tab. 1 — notation and controls — READY (text, Section 3).

## Figures

| Fig. | Status | Data |
|---|---|---|
| 1 Schematic (terse vs verbose caption under three golds) | to draw; no numbers | — |
| 2 Slope vs gold completeness | READY for COCO-2500, English LVLM families and XM3600 | C1J `check_coco_gold.*.slope/_ci`; H3J `families.*.gold.*` |
| 3 Specification curve | READY except placebo column | E1J `overview_15_pairs.*`, `pairs_15.*` |
| 4 Λ_k and channel split | READY | H4J `T4.coco_randk.Lambda.*`, `T4.coco_refs1_to_inst.*`, `.b_channel_share` (0.677, 0.742) |
| 5 Adjacency by dataset (no KTVIC row; Paper B owns it) | READY; XM3600 3-ref row keyed (0.5333 vs null 0.6667) | C1J `B2_L2_exchangeability.datasets.*`; `.session_backup/2026-10-14/r11_verify/c3_n2_exchangeability_all_datasets.json :: k5_exchangeability_audit.*` |
| A1 Support profile r(n) | READY (COCO only) | H4J `coco2500.T2_profile.*` |
| A2 Closed-form fit | READY ([MODEL] extrapolation) | H4J `T5_closed_form.*` |

## Pending runs that feed Paper A

| Run | Feeds | Cost / machine | Gate |
|---|---|---|---|
| DOCCI-Critique human test | Tab. 5 | CPU | DONE: MIXED (prereg committed after results JSON; disclosed; treated as exploratory) |
| Polaris-COCO | Tab. 5 | CPU | DONE: PASS (same timing disclosure) |
| G2-B extended (Qwen3-VL-8B zero-shot ladder) | §7.6, Tab. 4 | ~3.9 GPU-h | prereg = G2 REPORT §4, must be committed before outputs |
| XM3600 58_z (6 of 6 systems) | Tab. 4 | machine 2 | DONE: full verdict keyed (1/3 out-of-sample sign predictions failed) |
| N9 | Tab. 3 | ~6 GPU-h, machine 1 | committed prereg |
| E1 K2 placebo | Tab. 2 primary control | ~0.5–1 GPU-h | in N9 prereg |
| B3 large-k (nocaps 10 refs, PASCAL-50S) | §4 asymptote | GPU 2–3 h | licence check |
| Numbers manifest (H6 P1) | all | CPU | before submission |

## Pending runs that belong to Paper B (listed because the user asked; Paper A only cites them)

| Run | Paper B use | Paper A use |
|---|---|---|
| Ladder 55_multiref, 58_unf2, 56_cons, 57_rnd2 | frontier invariance across recipes | none (one-line pointer) |
| B1 second backbone (3 seeds), B2 scoring | generality of baseline/frontier | if B1 fails its frozen prediction: report as boundary condition in both papers (plan kill rule) |
| kNN P1 test (vs both controls + panel gate) | evidence-adding method | Remark in §3.5 (A ≠ 0 needs new evidence) may cite the outcome |
| M3 count-matched DPO (gated) | method | none |
