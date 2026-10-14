# R10 → Gemini: claims to verify and pilot specs

2026-10-14. Synthesis of the 20 R10 reports (E1–E6, G1–G3, M1–M7, V1–V3, X1).

**Sources**
- Reports: `manuscript/research_r10/<ID>/REPORT.txt`. Scripts and outputs: `.session_backup/2026-10-14/research_r10/<ID>/` (git-excluded). E1's downloads (`E1/dl/`, 248 MB, untrusted) were not copied; re-download them.
- Brief and decision: `manuscript/research_r10/CONTEXT_R10.md` and `.session_backup/2026-10-13/decisions/PD-2.txt`.
- 35_e outcome: `data/results/rl/` (commit C-029) and `.session_backup/2026-10-13/decisions/D14.txt`.
- Vietnamese synthesis for the judge: `manuscript/novel_direction/R10_00_HUONG_NGHIEN_CUU_MOI.md`.

**Conventions**
- `[MODEL]` = a model-generated signal (sample votes, grounding boxes, P(có), probe scores, agent-drafted lexical tables). It may only be used inside a method. It is never evidence or a label.
- `[UNVERIFIED]` = not independently checked.
- `[SYNTH]` = an inference by the synthesis agent, not a measurement.
- No "first" claims anywhere.
- Never write OpenViIC caption text to any file; aggregates only (U-002).
- Priorities:
  - P0: blocks endpoints or other pilots.
  - P1: numbers that will enter the paper, or that decide a novelty rating.
  - P2: citations.
  - P3: minor.

**Status updates since the reports were written**
- **35_e (CN-RLOO, CIDEr-only RL) is closed** (D14, YES 99%). Pre-registered negative N11.
  - Verdict KILL, not clean.
  - dev CIDEr-D 144.33 → 145.90: +1.57 [−6.26, +9.55].
  - Copy guard G4 failed: 1.00 → 1.70 → 1.60 → 2.25%, against a limit of 1.33%.
  - Panel CIDEr −0.5 [−3.7, +2.6].
  - Paired vs P1_dev: dF1 +1.77 [−0.52, +4.08]; d(frontier residual) +1.46 [−0.80, +3.64]; mentions 1.7633 → 1.7933.
  - 35_f and 35_g exited with 0 GPU-h. Total RL spend 3.79 GPU-h, as reported by the coordinator; D14 lists 3.153 GPU-h for the training run alone.
  - **No further RL runs** (D14 binding condition 1).
- **X1 landed last and is integrated.** All 20 reports are in.

---

## (A) CLAIMS TO VERIFY

Claims from every report's §5 are consolidated and deduplicated below. Format: **ID [priority]**, then source reports, then the check and how to do it.

### A0. Already verified by the synthesis agent (re-confirm cheaply; these change other claims)

- **S-1 [P0] The UPE kill-2 numbers are computed on OpenViIC-PANEL gold, not KTVIC gold.**
  - Sources: CONTEXT §2; PD-2 Q1; M6 §1 H5 and §5.3; V1 F-3; E6 §3.4.
  - Evidence: in `data/results/upe/test/upe_mbr_ktvic_test.json`, `p1assist_s4{2,3,4}.vs_count` holds only `panel_obj` and `panel_cider`. The F1 deltas +0.0712, +0.0326 and +0.1741 sit under `panel_obj.F1`. There is no `obj_ktvic` block under `vs_count`.
  - Consequence:
    - M6 H5 ("A ≈ +0.07") and V1 F-3 ("within ±0.3 of +0.07/+0.03/+0.17 under v3") compare against a panel-gold number.
    - The KTVIC-gold UPE − COUNT delta on test has never been computed. Compute it in C2.
- **S-2 [P0] The count-frontier constants were fitted on KTVIC TEST.**
  - Source: M4 §3b(v), §5.6.
  - Evidence: `manuscript/prereg/2026-10-12_ladder_predictions.json`, field `metric`: "object_prf.py ktvic_block vs the union of the 5 test references, 558 images". Anchors: M1 1.7826, TP1 1.3996, b 0.7468, c0 5.4859, c1 25.9815.
  - Rule to log: no test-fitted constant may enter a training objective, or a selection rule tuned on dev.
- **S-3 [P1] 35_e numbers as listed above.**
  - Sources: D14; `data/results/rl/g1_cn_v3_s42/gate.json` (keys `verdict`, `clean_kill`, `dev_gain_x100_mean_lo_hi`, `guards`, `exact_copy_trajectory_per_block`, `mentions_per_caption`, `chair_i`); `panel.json` (`delta_vs_first_x100`); `summary.json`.
- **S-4 [P1] M4's registered predictions for 35_e held** (M4 §4a; written before the verdict).
  - C1 mentions ∈ [1.65, 1.90] → 1.793.
  - C2 ∈ [−1.5, +2.0] with CI covering 0 → d(residual) +1.46 [−0.80, +3.64].
    - M4 defined C2 on its own `cm` endpoint (vote-top-k control on G0 rollouts), which is NOT computed yet. Close it in C3.
  - C3 raw dev object F1 ∈ [53.1, 56.6] → 56.34 (v2; D14).
  - C4 captions naming no class ≤ 15/300 → **12/300**.
    - The synthesis agent computed this with `rescap.chair.objects_in` on `data/results/rl/g1_cn_v3_s42-dev300-short.preds.json`.
    - The same code gives 9/300 and 1.7633 for P1_dev, matching M4 §3a and gate.json.
  - C5 (test) is N/A: no test decode is allowed (D14).
- **S-5 [P1] The P1_dev recall gap 43.13 vs 43.07 is the matcher version** (M3 §5.1, M7 §5.3).
  - D14 lists P1_dev dev300 as 74.29 / 43.07 / 54.53 under v1 (raw_tone) and 74.29 / 43.13 / 54.57 under v2.
  - The residual gap (+0.17 vs +0.13) follows from the same source.

### A1. Instruments and endpoint integrity [P0]

- **A-01 Matcher identity and drift.**
  - Sources: M6 §5.1; G3 §5.1; V1 §5.5; E3 §5.1.
  - Check which rescap/chair.py each landed number used: frozen fd1d0123 (= v1), or working-tree e47d249a (v2, since a0accb5).
  - PLAN-F1 reproduces (58.95 at m 2.6267) only with fd1d0123. v2 gives 58.97 at m 2.6233.
  - Then explain the two remaining 0.08 gaps:
    - human 1v4 P 85.25 vs 85.33 (G3 says matcher; V1 says pooling);
    - within F1 60.43 vs 60.50 (E3 says pooling vs fold-averaging).
  - How: rerun `scripts/human_parity.py` with RESCAP_RAW_TONE=1, then unset; compare with `data/results/human_parity.json`.
- **A-02 Three definitions of "same object"** (V1 §1(c), §5.2).
  - Check that `canonical()` is applied in `rescap/chair.py` L213/L258 and in `scripts/upe_mbr.py` L100.
  - Check that it is NOT applied in `scripts/object_prf.py` ktvic_block or in `scripts/prereg_ladder_check.py` L158/L166.
  - How: read those lines. Run "một toà nhà" and "một ngôi nhà" through each path.
- **A-03 The same-count control is under-specified.**
  - Sources: M2 §0, §4.1, §5.1; X1 §3a, §5.1; M1 §3a; M4 §4c; M5 §1.
  - Deterministic variants at PLAN-F1 k_i (m 2.627, matcher v1): RAW(v,g,lp) 58.87, NOPRIOR(v,g) 59.52, POOL13 59.90. Source: `data/results/planf1/dev_plan_critique.json` key `2_matched_count_controls`.
  - Tie-averaged: (v,g) 59.22, (s13,g) 59.60. Random-tie 95% band [58.74, 59.70]. Ties decide 7.4% of selected slots (`X1/x1_ties.json`).
  - M1's POOL-VOTE (12v+g) is 59.37 under v2. Is the 0.53 gap to POOL13 matcher or tie-break? Check.
  - How: rerun `M2/m2_salience.py` (RESCAP_RAW_TONE=1), `X1/x1_ties.py`, `M1/m1_headroom.py`.
- **A-04 Paraphrase chain in KTVIC reference order.**
  - Sources: E6 §3.3; G3 §5.9; G2 §3b caveat; M3 §3e.
  - Measure the similarity of adjacent vs non-adjacent refs. Then recompute:
    - G2's b(k) over random subsets (G2-C);
    - G3's b_pool(5) with non-adjacent subsets only;
    - M3's split-annotator check with refs {0,1} → {3,4}. M3 used {2,3,4}, and ref 2 is adjacent to ref 1.
- **A-05 Provenance of the "MBR" files.**
  - Sources: G1 §5.5; G2 §3d, §5.5; E5 §3b; V3 §5.3; X1 §3c.
  - Which rule produced p1_s43mbr-short, fuse2_s42mbr-short and fuse2_s42selffuse-two? UPE-MBR saved no per-image preds.
  - How: job logs under `data/results/upe/` and the queue scripts. Then dump the UPE/COUNT/LEX per-image selections with the G1 §4A.3 wrapper, writing OUTSIDE `data/results/`.
- **A-06 Identity of the dev300 greedy file.**
  - Sources: G2 §5.4; M1–M3, M5, M7 inputs.
  - Check that sha256 1e183383e91daf32… holds for `data/results/rl/p1dev_s42-dev300-short.preds.json` (now committed, D14 item 10), for `.session_backup/machines/n2/ncs-data/rl/p1dev_s42-dev300-short.preds.json`, and for the "greedy" hash in `data/results/upe/upe_choose_t.json`.
  - Also check the sample files: T0.5 876a1d42…, T0.8 60ebd640….
- **A-07 Residual unit and the "envelope".**
  - Sources: G2 §3c; X1 §3b, §5.2; E6 §3.1.
  - G2: tags_fuse2-detailed sits +1.75 P ABOVE the frontier, with the CI excluding 0.
  - X1: 0 of 85 runs have a residual CI (F1) above 0.
  - E6: the same system has ρ_A +2.4 [−1.2, +5.5] (%TP).
  - How: recompute that system's residual in F1, P and %TP with one shared image bootstrap.
- **A-08 Two vs one regime in M4's endpoints** (M4 §4c; PD-2 binding definitions).
  - M4's dev primary (cm, a per-image vote control) differs from PD-2's training endpoint (frontier residual). Only relevant if the RL branch reopens.

### A2. Reproduce report numbers [P1]

Run each report's scripts with `nice -n 19 env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1`, one job at a time.

- **A-10 E1** (E1 §5.1–5.3, 5.10).
  - Rerun `E1/e1_chair_count.py` (seed 0, 1,000 bootstraps). Reproduce the §3c table (3/15 MCP survivors; mean dP +3.4 → +0.6).
  - Reproduce the §3b fidelity vs LiM Table 1 (arXiv 2402.14545): within 0.6.
  - Check that r6-ours-cap.jsonl == r5-ours-inst.jsonl (sha256 7a7e2775127249dc…).
  - Check the SumGD (2410.13321) Table 7 transcription, and that b = 0.75/0.55/0.59 recompute.
  - OPERA's release has LLaVA-1.5 greedy CHAIR_i 12.60 vs OPERA 12.67. Compare with the OPERA paper and its decoding settings.
- **A-11 E2** (E2 §5.1, 5.9).
  - Rerun `E2/e2_pilot.py` and `e2_ablation.py`. Raw P must match `second_panel.json` within 0.1 (p1-gold-short 77.94 vs 77.88).
  - Check the panel-sensitivity assumption (system ref-false objects confirmed at the human rate, 58.78%). E6 §3.6 and V2 §3A suggest the panel is conservative, so E2's "hallucination" remainder is an upper bound.
- **A-12 E3** (E3 §5.1–5.5).
  - Check md5 9c27888568afaad9410d210fc9b0217e.
  - L0 test cross5 44.96; within 60.43.
  - Gaps and κ on both splits; L3's null is about 75.
  - τ(π_c, u_c) −0.04 (dev300) and −0.26 (test).
  - "dù" has 14 OpenViIC mentions on dev300 (run with DIALECT = {}).
  - System table: τ 0.546 → 0.669 (C80); home advantage 9.79 → 2.79; zero-shot-detailed rank 40/10 → 55/53.
- **A-13 E4** (E4 §5.1–5.7, 5.9).
  - `protocol_pilot.py --check`.
  - 164.25 = mean(164.32, 164.11, 164.31) with official pycocoevalcap 1.2 and py_vncorenlp (E4 S1).
  - RDR(caption) == segment_caption on 2790/2790 refs.
  - VnCoreNLP rewrites old-style tone placement.
  - cider_scorer IDF = log N − log max(1, df).
  - The COCO PTB tokenizer removes punctuation.
  - Legacy T3 numbers 21.8/36.8 (bug), 48.9/72.9 (word), 52.9/79.1 (syllable).
  - Repo "syllable (whitespace)" rows used punct=glued.
  - P12 survives capping at 5 refs (K2).
- **A-14 E5** (E5 §5.3, 5.8).
  - `kstar.py --B 2000`. Point estimates must be exact; CIs within ±0.01.
  - The identity assert in `_check`.
  - Chao-Jost C(5) = 89.4% and C(10) = 98.0%, against iNEXT `incidence_freq` with T = 5, Q = 717, 566, 361, 220, 210.
- **A-15 E6** (E6 §5.1–5.7).
  - `map2d.py` reproduces `tone_norm/second_panel.json` (max |diff| 0.00).
  - Frontier A reproduces the prereg constants. The I-frontier, TP = exp(−0.1723) M^0.899, is NOT pre-registered.
  - Family split by filename prefix: confirm legacy stem provenance, and that vcd and tags_zeroshot are training-free.
  - bon_dev has no CIs.
  - The COCO count-collapse reading (M = true/P) is derived, not recomputed.
  - UIT-ViIC P1 88.6 vs zero-shot 99.2 is single-seed on 231 images.
  - The R8 CIDEr oracle numbers (+44.7/+0.07; −25.9/+24.9; +22.3/+13.8) come from the R8 T1/T2 reports and have no raw files.
- **A-16 G1** (G1 §5.1–5.3, 5.7, 5.8).
  - `g1_tuples.py demo | extract | fit ladder|clean|all`.
  - Anchor object b 0.747.
  - zeroshot-short object residual −29.7% [−33.2, −26.2].
  - pyvi 0.1.1 tags are identical.
  - The 9 CJK-heavy exclusions match `data/results/cjk_rate.json` (> 5%).
  - G1 §0 calls self-fusion a pure object count shift, but §3c gives fuse2_s42selffuse object −6.7 [−9.7, −3.7]. Fix the wording.
- **A-17 G2** (G2 §5.1–5.3, 5.6, 5.7, 5.9).
  - `g2_frontier.py`: b_anc 0.7468; ladder b_ols 0.703; refs1..5 curve; COCO inst 0.846; UIT inst 0.943.
  - The COCO ref gold equals score_coco_probe's gold.
  - Temperature of `samples/fuse2_s42-test-short.jsonl` (assumed 0.8).
  - Legacy −25 to −46 P is a style or leakage effect, not a key mismatch.
  - The above-frontier vote thresholds are seed-dependent.
  - Check the algebra b = p_marg/P, and that F1 rises with M iff p_marg > F1/2.
- **A-18 G3** (G3 §5.1–5.7).
  - U(k) test 1.743 / 2.577 / 3.101 / 3.460 / 3.717.
  - b_sys(h) 0.561 / 0.640 / 0.689 / 0.723 / 0.747; b_pool(h) 0.727 / 0.824 / 0.881 / 0.922 / 0.947.
  - s1 0.892, D 0.194, RMSE 0.78 P; the h ≤ 4 fit predicts b(5) 0.756.
  - Annotator-only b ∈ [0.87, 0.96].
  - α_pos 0.251 / 0.277 / 0.264 (fuse2-det), 0.271 (e5); human positions are flat.
  - OLS b 0.728 over 32 runs.
  - Truncation P 74.8–75.5 < 78.5.
- **A-19 M1** (M1 §5.2–5.5).
  - `m1_headroom.py` under v2, and rawtone/ under v1 (plan − RAW +0.08 [−0.74, +0.91]).
  - Qwen2.5-VL boxes are absolute pixels of the resized input; Qwen3-VL uses 0–1000.
  - `probe_existence.ask` P(có) tokenisation works with the current transformers.
  - Measure GPU-h on the dry run.
- **A-20 M2** (M2 §5.1–5.4, 5.9, 5.10).
  - `m2_salience.py`: plan sha256 58ecef13…; controls 58.87 / 59.52 / 59.90.
  - The conclusion still holds under matcher v2 (not run).
  - P1_dev SFT uses the first reference only (`scripts/build_gold_sft.py`). This is the H2 premise.
  - Re-check the lexical-family grouping, about 25% (claim 9).
  - Boundary-restricted AUC (claim 10).
- **A-21 M3** (M3 §5.2–5.6).
  - UIT-ViIC overlap 133 Karpathy test / 59 manifest; 2,562 kept ids.
  - E5-DPO pairs: 24.4% count-matched, dk −0.22. 22_e5_dpo used the defaults (β 0.1, lr 5e-6).
  - Timing bases from `queue.log` (36_z; 22_e5_dpo).
  - `train_stage2.run_dpo` uses the legacy mask; prompt tokens cancel in the margin; the anchor CE needs `assistant_only=True`.
  - The invariance algebra (§1); `ref_sft` = π_SFT of the start adapter.
- **A-22 M4** (M4 §5.1–5.4, 5.7, 5.8).
  - G0 hashes f71aff0c… / d5898fe4….
  - `m4_pilot.py`: within-image slope 0.479 [0.436, 0.525] vs price 0.586; count-gradient table; object-free rollouts 10.0% / 14.0%.
  - The CIDEr-D proxy vs RDRSegmenter on 100 rollouts.
  - The rloo identity on a GPU dry run.
  - mr5assist residual +0.25 [−2.10, +2.54], recomputed from preds.
  - P1_dev stats: now confirmed by D14 and S-4.
- **A-23 M5** (M5 §5.1–5.7, 5.10).
  - `m5_check.py`, `m5_prefix.py`, `m5_pool7.py`:
    - bucket counts;
    - 71.0% vs 50.6 / 44.0 / 34.0%;
    - allocation deltas.
  - `uniform_alloc` matches the total exactly; k = 4 shortfall.
  - The frontier is valid only for M ∈ [1.76, 3.15].
  - mr5assist M.
  - The PLAN-F1 decomposition with plan_dev.json.
  - The evaluate.py prompt suffix reaches generation.
  - The builder sha256 is stable across Python versions.
  - Throughput 7.2–7.5 s per step.
  - M5 §0 says "even oracle counts only reach the frontier", using k_i = min(|G_i|, 4). M6 §3c shows gold-size allocation is worse than uniform (−2.58 [−4.45, −0.69]), so this sentence needs rewording.
- **A-24 M6** (M6 §5.2–5.5, 5.7, 5.8).
  - `m6_alloc.py` (about 5 s; it asserts the plan reproduction and UPE hash 1380ad20).
  - CAR terms for UPE: C +0.92, B +0.62, A +0.14. Re-run with Shapley averaging over the 6 orders (X1 §2d).
  - T0.8 slot residual −4.32.
  - The knapsack writes only existing captions.
  - The test greedy preds and adapters for p1assist_s4X exist on n2.
  - Global-vote set at greedy B: dev-anchored +1.84 [+0.34, +3.33], but official +1.97 [−1.25, +5.00]. That CI includes 0.
- **A-25 M7** (M7 §5.1–5.5, 5.8).
  - `hedge_count.py`: KTVIC test has 0/2,790 hedged captions. Check the "hoặc" senses by hand on KTVIC/XM3600 only, never OpenViIC text.
  - `hedge_precision.py`: check the scope rule on 30 zero-shot COCO captions; fix the double-counted asserted n.
  - Independent derivations: the H1 proof, the H2 thresholds, and FP+FN = Brier on a fixed universe.
  - The 58.1% zero-shot-detailed hedge rate, with and without "hoặc".
- **A-26 V1** (V1 §5.1, 5.3, 5.4, 5.6, 5.9).
  - objects_in outputs on the listed examples.
  - Count the training lists carrying a classifier cây/quả, or cửa from cửa hàng (objects_in builds SFT/DPO targets).
  - Rerun `rescore.py`, `validate.py`, `coverage.py`, `discover.py`. These need pyvi, so run without -I.
  - Check that the COCO mapping is acceptable.
  - CHAIR_i under v3 (not computed).
  - V1 F-3 must use the same gold as the original measurement, which is the panel (S-1).
- **A-27 V2** (V2 §5.1, 5.8, 5.11).
  - `pilot_v2.py`, `pilot_v2b.py`.
  - s/item for pope_vi on the 3090.
  - Whether XM3600 captions for P1 and fuse2 exist.
  - COCO-2500 ∩ POPE-500 = 32 images.
- **A-28 V3** (V3 §5.1–5.7, 5.9).
  - `taxonomy.py` output sha256 450f6c91….
  - Invisible-instance shares.
  - MBR fragment and CJK diffs.
  - HYPERNYMS lacks cô gái, chàng trai, cậu bé, cô bé, em bé, đứa trẻ, học sinh, so `_gold_objects()` never adds người.
  - Zero-shot detailed: 50.2% end without final punctuation. Check max_new_tokens.
  - P1's detailed prompt yields short outputs (also G1 §3a).
  - Register flags vs legitimate KTVIC phrasing.
- **A-29 X1** (X1 §5.1–5.3).
  - `x1_ties.json`: tie-averaged and deterministic values (see A-03).
  - `x1_envelope_length.txt`:
    - max residual +1.58; 0 CIs > 0; 32 runs below −20; R² 0.85 (44 runs);
    - R²: P~log m 0.960 vs P~log length 0.826;
    - length-controlled +2.60 / +1.95 / +2.68 / +0.20 vs count-controlled −0.14 / −0.76 / +0.49 / −1.33.
  - Re-run with RDRSegmenter words instead of whitespace syllables; the ordering should hold.
- **A-30 35_e post-hoc closure** (M4 C2; E6 H4; V3 H4; S-3, S-4).
  - Compute M4's `cm` for 35_e vs P1_dev with `M4/m4_endpoint.py` (sha256 6d8e7ed1…) on the G0 dev300 rollouts.
  - Compute E6's count-matched ρ_I on the dev panel. H4 predicts [−1.5, +1.5]. The KTVIC-CIDEr premise is not met (+1.57 n.s.), so H4 can only be "consistent".
  - Compute V3's form-class paired CIs (fragments rose 9 → 12).
  - Label all of this post-hoc.

### A3. Data, provenance and licence [P1]

- **A-31 Licences.**
  - OpenViIC terms and author confirmation (PD-2 Q4).
  - KTVIC and UIT-ViIC terms for releasing derived item lists (V2 §5.9).
  - Until settled: aggregates only, no panel-derived per-image files.
- **A-32 Leakage disclosure.**
  - 401 of the 558 KTVIC test images are in OpenViIC train (PD-2 blocker 8).
  - This affects every panel analysis: E2, E3, E4 P12, E5, E6, M1 bound, D14 panel.
- **A-33 Test-look ledger.** One disclosure table for the paper:
  - E3: one exploratory test look, script frozen.
  - V1: rule discovery on TEST refs; re-derive the tables on train-minus-dev300.
  - E6: I-frontier fitted on test.
  - G1: tuple frontiers fitted on test outputs.
  - X1 §3b–3c: post-hoc on test tables.
  - Descriptive reads: E2, E4, E5, G2, V3, M7.
  - Dev only: M1–M6.
- **A-34 Timestamps for the 35_e predictions.**
  - E6 H4, V3 H4, G1 H1 and G3 H4 appear in reports with mtimes 08:51–08:59 +07 (01:51–01:59 UTC). The verdict existed by 03:19 UTC, when 35_f/35_g exited.
  - None were filed in `manuscript/prereg/`. Describe them as "timestamped predictions", not pre-registrations.
  - M4 §4a declares its own block as a pre-registration.

### A4. Citations, IDs and novelty searches [P2; P1 where marked]

- **A-40 [P1] LeHaCE** (X1 §2b #1): NeurIPS 2024, DOI 10.52202/079017-3538, no arXiv. This is the closest scoop for the count-control package.
  - Confirm: word length, per-model linear curves, a CHAIR-type rate, no recall/F1. X1 read only the slides and abstract.
  - Add it to E1, G2 and E6 related work.
  - Run a "cited by" sweep of LeHaCE and CCEval for count-matched follow-ups (X1 §5.9).
- **A-41 [P1] Rater equivalence, arXiv 2106.01254** (Resnick et al.; v3 dated 2026-04-22).
  - Do v2/v3 cover extrapolation beyond the panel, or target-panel-size stability? If yes, E5 novelty drops to LOW (E5 §5.1).
  - arXiv 2601.19435: GPT-5 judge rater equivalence ≈ 2 (E5 §5.2).
- **A-42 [P1] VGD arXiv 2607.27823, "@rec90"** (E1 §5.5).
  - X1 §2b reads it as a recall-retention operating point "without shortening captions" [UNVERIFIED].
  - If it is recall-matched, add it to related work and lower E1 novelty to low-moderate.
- **A-43 [P1] HallE-Control / CCEval, 2310.01779v3** (E1 §5.4; X1 §5.5; M3 §5.7).
  - Quote check: "we do not strictly enforce consistent constraints (same coverage, average length, and average objects)".
  - Average objects 8.04–9.28 (Sec. 3 / Table 2).
- **A-44 [P1] Frontier-law novelty** (G1 §5.4; G2 §5.8; G3 §2 scan; X1 §5.9).
  - Search Semantic Scholar and Google Scholar for: "scaling law" + caption length + hallucination; precision–count power law; "SPICE subcategory length bias"; 2025–26 count- or length-indexed hallucination laws.
  - Also the two X1 queries that did not run: CHAIR gold incompleteness; KTVIC 2025–26 papers.
- **A-45 [P1] Two-panel invariance novelty** (E3 §5.9): Flickr30k vs COCO re-captioning, nocaps, DOCCI; "annotation guideline" + hallucination metric.
- **A-46 [P1] Count-matched preference pairs** (M3 §5.8): rerun the scoop on Semantic Scholar (M3 used 7 web queries).
- **A-47 E6 related work is missing.** E6 §2 contains an unfilled "<<REFS>>" placeholder. Supply and verify:
  - ImageNet ReaL (Beyer et al. 2020, arXiv 2006.07159; X1 lists the ID as checked);
  - effective robustness (Taori et al. 2020, arXiv 2007.00644 [UNVERIFIED, from memory]);
  - reward-model over-optimisation (Gao, Schulman, Hilton 2022, arXiv 2210.10760 [UNVERIFIED, from memory]), which is the source of E6 P1's best-of-n form d = sqrt(log n − (n−1)/n).
- **A-48 Spain & Perona and Berg et al.** (E2 §5.6; G3 §5.8; M1 §5.1; M2 §5.5–5.6).
  - Spain & Perona: IJCV 91 (2011) pages (59–76?) and DOI; does "importance" mean "named first" or "named at all"? ECCV 2008 DOI 10.1007/978-3-540-88682-2_40.
  - Berg et al., CVPR 2012: DOI 10.1109/CVPR.2012.6248100; importance = what people describe; features.
- **A-49 Capture-recapture and coverage** (E2 §5.2–5.7; E5 §5.3–5.4; G3 §5.8).
  - Dawid & Skene 1979, DOI 10.2307/2346806.
  - Chao 1987, DOI 10.2307/2531532.
  - Holzmann, Munk & Zucchini 2006: pages and DOI.
  - Keenan, Smeaton & Keogh 2001, JASIST 52(7):570–574: title and content.
  - Chao & Jost 2012, Ecology 93:2533–2547.
  - Chao et al. 2014, DOI 10.1890/13-0133.1.
  - iNEXT, DOI 10.1111/2041-210X.12613.
  - The source sentence of the "extrapolate ≤ 2× the sample" rule (Colwell et al. 2012?).
  - Novelty search: "capture-recapture / Lincoln-Petersen / mark-recapture" + caption / reference; "Dawid-Skene" + caption.
- **A-50 Human parity and annotator equivalence** (E5 §5.5–5.6).
  - Läubli et al., D18-1512 / 1808.07048.
  - Toral et al., 1808.10432.
  - Hassan et al., 1803.05567.
  - Xiong et al., 1610.05256.
  - Snow et al. 2008, D08-1027: the "non-experts per expert" figure.
- **A-51 Metric and protocol** (E4 §5.8; E5 §5.7).
  - P11-2028; W18-6319 / 1804.08771; 10.18653/v1/2023.acl-long.107; 2106.15195; 2109.13701; 2004.06063; 1504.00325; 1411.5726; TIGEr 1909.02050; STADS 1803.02130; Pyramid N04-1019 (X1 lists it).
  - [UNVERIFIED]: 2202.06935; the MeCab/jieba evaluation protocols of STAIR, COCO-CN and AI Challenger.
- **A-52 Captioning and hallucination benchmarks** (E3 §5.6–5.8; G1 §5.6; G2 §5.8; V3 §5.8; V2 §5.5).
  - CAPTURE 2405.19092: which three matching stages?
  - 2412.15484: the venue (ICML 2025, PMLR 267:33815–33832?), and the "Spearman 67.9 → 18.3" claim. Locate the table or drop the claim.
  - CompreCap 2412.08614 (CVPR 2025).
  - THRONE and VALOR-EVAL venues.
  - SC-Captioner 2508.06125: content.
  - AMBER 2311.07397: Cover, and the images shared between tasks.
  - CHAIR 1809.02156; SPICE 1607.08822.
  - Taxonomy refs: 1704.04198, 1705.01359, 2406.16449, 2310.14566, 2406.20052, 2407.02333. Check that 2404.18930 really uses a category/attribute/relation taxonomy before citing it.
  - Buckland & Gey 1994: pages.
- **A-53 Multilingual and Vietnamese benchmarks** (V2 §5.2–5.7; V3 §5.8; X1 §5.8).
  - MHR 2408.00550: 13 languages, no Vietnamese, GPT-3.5 translation.
  - CLAIM 2506.11073: language list and translation method.
  - PatchGate 2608.21819: does the full text have a per-object probe-vs-caption analysis by size? If yes, V2's (c) novelty drops to low. Also cited by M2.
  - ProCap 2607.21022.
  - Any 2025–26 Vietnamese visual-hallucination or POPE work (VLSP 2025, Vintern, LaVy).
  - IDs: POPE 2305.10355, MME 2306.13394, XM3600 2205.12522, Open Images 1811.00982, UIT-ViIC 2002.00175, KTVIC 2401.08100 (and its institution), UIT-OpenViIC 2305.04166, ViHallu 2601.04711.
- **A-54 Grounding and verification** (M1 §5.1, §5.6).
  - 2310.16045, 2403.00425, 2303.05499, 2510.27164, 2306.14824, 2306.15195, 2404.13013, 2502.13923, 1803.09845, 1811.10652, 1704.07434, 2411.16724, 2503.06287, LURE 2310.00754.
  - Re-search "matched-count evaluation of grounding verification".
- **A-55 Salience and content selection** (M2 §5.7): Yatskar S14-1015; Yun CVPR 2013 (10.1109/CVPR.2013.101); Jas & Parikh 1502.04569; VIFIDEL P19-1654; Borgeaud & Emerson 1908.06288.
- **A-56 Preference optimisation** (M3 §5.7).
  - HALVA 2405.18654 (ICLR 2025; Cover 51.0 → 53.0; CHAIR 7.8 → 6.6).
  - CHAIR-DPO 2508.20181 (BMVC 2025); RLHF-V 2312.00849 (CVPR 2024); mDPO 2406.11839 (EMNLP 2024); SimPO 2405.14734; R-DPO 2403.19159; KTO 2402.01306; Razin et al. 2410.08847.
  - Venues unknown: HA-DPO 2311.16839, POVID 2402.11411, RPO 2404.19733.
  - [UNVERIFIED]: HII-DPO 2602.10425, OPA-DPO 2501.09695, SamPO 2406.10957.
- **A-57 RL rewards** (M4 §5.5, §5.9).
  - Stratified GRPO 2510.06214: ICML 2026 status, and whether it already states the CS identity. If so, cite it as theirs.
  - ODIN 2402.07319; 2409.17407; 2404.04475; 2310.03716.
  - PS-NOC 2109.05115: the figures disagree, 85.9/34.1 vs 75.8/26.6.
  - BalCapRL 2605.07394: venue.
  - [UNVERIFIED]: ClaimDiff-RL 2605.20278, RubiCap 2603.09160, Re3Cap 2608.21305, 2507.20077.
- **A-58 Count and length control in captioning** (M5 §5.8–5.9).
  - 2101.08000: noun-count control. Read the method section and any object-precision result; this sets M5's method novelty.
  - REVERSE 2504.13169; NumCap DOI 10.1145/3576927.
  - LaBERT 2007.09580; 2005.14386; ASG 2003.00387; 2212.01803; CaptionSmiths 2507.01409; 1609.09552.
- **A-59 Allocation and F-measure theory** (M6 §5.6; X1 §5.7).
  - Arampatzis et al. 2009, DOI 10.1145/1571941.1572031.
  - Lipton et al. 1402.1892 (author spelling).
  - Koyejo et al., NeurIPS 2015 (no ID checked): does it treat mixed micro-P / instance-R?
  - Schultheis et al. 2401.16594: scope of the at-k budget.
  - Choppy 2004.13012.
  - Abadie & Imbens 2006: wording on tied matches.
- **A-60 Hedging** (M7 §5.6–5.7).
  - LURE's [IDK] masking.
  - 2504.14848; 2505.20236 (EMNLP 2025).
  - ALOHa 2404.02904: its "possibly" / "chair or table" example.
  - Facebook's "Image may contain" wording; MacLeod DOI 10.1145/3025453.3025814; Murphy 1973.
  - Deeper search: hedge / epistemic / uncertainty + captioning + proper scoring.
- **A-61 Extractor** (V1 §5.7–5.8).
  - W09-3035: title.
  - Dao 2012; Tran 2019.
  - Search the ACL Anthology, VLSP and arXiv 2023–26 for a prior Vietnamese CHAIR-style extractor.
- **A-62 X1 snippet-only items** (X1 §5.6, §2b).
  - SumGD's 64/128/256/512-token settings.
  - 2608.28058: CHAIR per 100 tokens.
  - RoSE: length-normalised ACU.
  - New 2024–26 references to check: DatologyAI 2606.25432, OVFact 2507.19262, CapProbe 2608.11074, SPARC 2502.01419, HaloProbe 2604.06165, DetailVerifyBench 2604.05623, Mohamed et al. 2507.20077, Zheng et al. 2510.20229. X1 reads 2510.20229 as "length is not the cause; context reliance is", which answers E1 §5.9 [UNVERIFIED].
- **A-63 [P3] Lexical questions.** Does a bench count as "ghế" for Vietnamese speakers (V2 §5.10)? The North/South dialect reading of ô/dù is a hypothesis; annotator origin is undocumented (E3 §5.8).

---

## (B) PILOT SPECS

### B0. Judge decisions needed before the pilots (no compute)

1. **Control definition** (A-03).
   - Primary: tie-averaged (v,g), which keeps PD-2's wording.
   - Robustness: the tie-averaged family {v, (v,g), s_N, (s_N,g)} (X1 P-A).
   - A claim must have a paired CI > 0 against both.
   - Never take a max over deterministic tie-breakers.
2. **Endpoint for allocation methods** (M6).
   - Add a TOTAL-count-matched endpoint (paired dF1 vs greedy at Δm = 0), plus the CAR B term with Shapley averaging.
   - By construction, the per-image PD-2 control cannot see allocation (+0.09 for M6's knapsack).
3. **Truth-side co-primary for reference-reading training methods** (E6): M3, and M4 if reopened.
   - Count-matched ρ_I on the OpenViIC panel. dev300 has the panel for 296/300 images.
   - Instance precision on COCO / UIT-ViIC.
   - [SYNTH] Proposal: test Δρ_I > 0 with LB > 0; dev κ = Δρ_I/Δρ_A ≥ 0.35.
4. **Guards.**
   - CIDEr guards are evaluated under P0 and under P7 (punctuation stripped; E4). Pre-register which one binds.
   - Add a G4-style copy-rate guard to M3: 35_e failed G4 on the same 1,000 train images.
5. **Scope of D14.** Does "no further RL runs" cover DPO (M3)?
6. **G2-B vs PD-2 Q5.** G2-B runs Qwen3-VL-8B zero-shot on COCO-2500, which PD-2 Q5 rejected for S0. G2's endpoint is Δb, not a level.
7. **Matcher.**
   - v2 stays primary.
   - One unified v3 (V1 + V3 + E3 L1) is a sensitivity analysis.
   - Every prereg pins the rescap hash.

### B-CPU. Run these first, in this order

Global rules:
- Run with `nice -n 19 env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1`.
- Stay under 1.5 GB RAM on the shared laptop. V3 P-A needs about 3 GB, so run it on the cluster CPU.
- One job at a time.
- Repo writes go only through the gatekeeper.
- Script paths below are relative to `.session_backup/2026-10-14/research_r10/`.

**C1. Pin the instruments**
- Sources: V1 §4 step 2; M6 §5.1; X1 P-A; M2 §4.1.
- Data:
  - dev300 pool: greedy `data/results/rl/p1dev_s42-dev300-short.preds.json` (1e183383…), plus `data/results/upe/p1dev_s42-dev300-short-T{0.5,0.8}.jsonl`.
  - Test pools: `data/results/upe/test/p1assist_s4{2,3,4}-test-short-T0.5.jsonl` plus greedy preds.
- Scripts:
  - `X1/x1_ties.py` exists and runs in 21 s. It has no asserts, but it reproduces M2's deterministic numbers exactly.
  - `M2/m2_salience.py` exists and reproduces dev_plan_critique.json.
  - NOT written:
    - the test-pool generalisation (~40 lines; s7 = 6v + g);
    - the V1 step 2 gatekeeper edit (`RESCAP_EXTRACTOR` switch, single canonicalisation).
- Compute: ~0.3 CPU-h; 0 GPU-h.
- Prereg: the B0.1 control; matcher hashes fd1d0123 (v1) and e47d249a (v2) recorded; v2 primary.
- Endpoint: none (instrument).
- Kill: if the tie-averaged family spans > 0.5 F1 on the test pools, report the full specification curve, not one control (X1 P-A.3).
- Test policy: test pools are read only to recompute controls for claims already registered (UPE kill-2).

**C2. CAR audit with Shapley; UPE − COUNT on KTVIC gold** (resolves the UPE "pure count shift" conflict)
- Sources: M6 P-M6a; X1 §2d.
- Data:
  - dev300 pool.
  - UPE test pools and greedy preds (hashes under `inputs` in `upe_mbr_ktvic_test.json`).
  - Frozen rescap (`M6/frozen/rescap`, from `git archive ee583c7`).
- Scripts:
  - `M6/m6_alloc.py` exists, is deterministic, and asserts the PLAN reproduction and UPE hash.
  - NOT written:
    - the repo port `scripts/car_decomp.py` (sections 0–3 and 7);
    - Shapley averaging over 6 orders (~30 lines);
    - the test loader (V = 7-caption vote);
    - the UPE selection dump (shared with C9).
- Compute: ~0.3 CPU-h.
- Prereg: descriptive. Fix the matcher, the Shapley averaging, and both golds (KTVIC 5-ref union; OpenViIC panel aggregates).
- Endpoint: terms A–D with 95% CIs pooled over 3 seeds, plus the KTVIC-gold UPE − COUNT dF1 (missing from the JSON, S-1).
- Kill: none. If the Shapley B or D term has a CI excluding 0 on test, reword "UPE is a pure count shift" to: "no gain over the same-count vote control; its gain over greedy is count + allocation (+ vote re-ranking)".
- Test policy: existing test samples; no tuning.

**C3. 35_e post-hoc scoring** (dev only; label everything "post-hoc, after verdict")
- Sources: M4 C2; E6 H4; V3 H4; G1; G3; E5 S5; M6.
- Data:
  - `data/results/rl/g1_cn_v3_s42-dev300-short.preds.json` and `p1dev_s42-dev300-short.preds.json` (hashes in D14).
  - G0 dev300 rollouts `rl/g0/dev300.jsonl` (f71aff0c…, on n2).
  - The dev panel aggregates (296 images).
- Scripts, all of which exist:
  - `M4/m4_endpoint.py` (sha256 6d8e7ed1…; no self-check);
  - `E6/map2d.py` (needs a dev300 mode);
  - `G1/g1_tuples.py` (demo asserts pass);
  - the G3 scripts;
  - `E5/kstar.py` (dev mode = E5 S2);
  - `V3/taxonomy.py` (dev mode = V3 P-C);
  - `M6/m6_alloc.py`.
- Compute: ~0.4 CPU-h.
- Prereg: none possible now. Only M4 C1–C4 were registered before the output.
- Endpoints:
  - M4 C2 `cm` ∈ [−1.5, +2.0] with the CI covering 0;
  - E6 H4 count-matched ρ_I ∈ [−1.5, +1.5];
  - V3 H4 form-class paired CIs;
  - CAR terms vs P1_dev.
- Test policy: no test decode exists or is allowed (D14).

**C4. Frontier theory checks**
- Sources: G3 A–D; G2 A, C.
- Data:
  - KTVIC test/train refs; `data/results/*.preds.json`; `human_parity.json`.
  - COCO-2500 probe and coco_transfer preds.
  - OpenViIC panel: runtime aggregates only.
- Scripts:
  - `G3/annot_stats.py`, `sys_stats.py`, `frontier_models.py`, `gold_size.py`, `decomp_fit.py` exist. Only annot_stats has an assert. The bootstrap is NOT written.
  - `G2/g2_frontier.py` exists; its reproduction checks pass; ROOT is hard-coded. G2-C (random k-subsets, LOO, jackknife) is NOT written.
- Compute: ~0.6–0.8 CPU-h.
- Prereg:
  - G3 B: D(h) per pair with B = 1000. Pairs: p1assist s42–44 → e5_s42-det; mr5assist_s42-short → tags_fuse2_s42-det; p1mask_s42 → fuse2_s43/s44-det; each landed ladder run vs the P1 anchors.
  - G2-C: b(k) averaged over 20 random k-subsets per image.
- Endpoints: D(h) with CI, reported next to every frontier residual; paired Δb with CI.
- Kill:
  - G3 H1: max_h D − min_h D > 0.06 (CI excl. 0), or 2-parameter RMSE > 1.5 P.
  - G2 K1: the completeness law fails on ≥ 2 datasets.
  - G2 K3: RMSE > 3 P within a style-matched family → report the frontier only as a local linearisation.
- Test policy: already-read test outputs; descriptive.

**C5. E1 Phase A (+ A2 harvest) and X1 P-B**
- Data:
  - COCO `annotations_trainval2014.zip` (241 MB).
  - OPERA `log/chair_eval_results/*/{greedy,beam5,ours}.jsonl` (12 files).
  - LiM `CHAIR-eval/data/Table1-results/r1..r12` plus chair-500; exclude r6.
  - `data/coco_probe/chair_synonyms.txt`.
  - The downloads in `E1/dl/` are untrusted. Never put them on sys.path; run with `-I`.
- Scripts:
  - `E1/e1_chair_count.py` exists. It has no asserts; its fidelity check reproduces LiM Table 1 within 0.6.
  - NOT written (~30 lines): 2,000 bootstraps, Holm, a placebo (two sampling seeds of one model; [SYNTH] the released files are greedy/beam, so this may need Phase B outputs), and a positive control (baseline minus its first hallucinated class; uses GT; power check only).
  - X1 P-B regression: NOT written; it reuses e1_chair_count.py.
  - A2: GitHub tree scan of HALC, DeCo, PAI, SID, VTI, Nullu, MemVR, AGLA, ICT, SumGD, MARINE, VGD, and HF datasets.
- Compute: ~1.6 CPU-h (0.1 per rerun; 1.0 for harvesting; 0.5 for P-B).
- Prereg:
  - E1 primary: dP_MCP with Holm and SESOI +1.0. Secondary: TRF and the three-part split.
  - [SYNTH] Add TRF and a tie-averaged random-subset control next to MCP, because MCP's truncation bias favours the truncated side (X1 §2d, §6).
  - X1 P-B: α_len − α_cnt averaged over the 15 pairs (B = 2000); prediction ≥ +1.0 P.
- Kill:
  - E1 K1: fidelity off by > 1.0 CHAIR_i or > 1.5 CHAIR_s on > 20% of rows.
  - E1 K2: placebo |dP_MCP| > 1.0.
  - E1 K3: positive control < +3.
  - E1 K4: more than 1/3 of decoding pairs survive → change the headline.
  - X1 P-B: |α_len − α_cnt| < 0.5 P, or α_cnt > α_len → drop the "object unit" claim.
- Test policy: public data only.

**C6. E6 P0 and P2**
- Data:
  - map2d: 73 KTVIC-test systems × 555 images.
  - bon_dev: dev300 P1 s42, 6 samples at T0.5.
  - P2: the Karpathy split and instances_val2014 (`~/ncs-data`); `data/results/uitviic`; `coco_transfer`.
- Scripts:
  - `E6/map2d.py` and `E6/bon_dev.py` exist and reproduce second_panel.json.
  - P0 additions are NOT written: paired CIs with B = 2000 and shared subset draws; a count-matched selection control (a random pick among samples whose M equals the oracle pick's M).
  - P2 uses the repo's `scripts/two_gold_audit.py --blocks uitviic_models coco_models` and writes to a NEW file.
- Compute: ~0.3 CPU-h. P2 needs ~0.3 GPU-h for the 924 UIT-ViIC val images; otherwise declare a deviation from gates G3′/job36.
- Prereg: P2 is already registered (G3′/job36).
- Endpoints:
  - P0: κ (object, CIDEr) with CIs, under count-matched selection.
  - P2: a third tier on COCO (split the 5 refs 3/2 into A and I; use instances as T). Does ρ_I track ρ_T better than ρ_A does?
- Kill (applies to the later P1): object κ16 ≥ 0.70 → drop the 2-D framing; count-matched dF1_A_held CI includes 0 → report the population regime only.
- Test policy: descriptive on already-read outputs. The I-frontier is exploratory.

**C7. E3 steps 0–3**
- Data: KTVIC train/test; dev300 split; `data/ktvic_openviic_refs.json` (evaluation only); 73 preds files.
- Scripts:
  - `E3/e3_pilot.py` (frozen, md5 9c278885…; sanity asserts) and `e3_tiers.py` exist.
  - Step 2 (count-matched endpoints A/B) is NOT written.
- Compute: ~0.5 CPU-h.
- Prereg:
  - Choose the tier lists (THING; THING-noclothing) on dev300 by highest κ with nullW ≤ L0 + 15. One tier only.
  - Test predictions: κ(tier) − κ(L0) ≥ 0.10, and gap ≤ 0.5 × the L0 gap.
- Endpoints:
  - A: Kendall τ of residuals across the two golds.
  - B: FT-minus-ZS home advantage on residuals.
  - Step 3: human-side κ and gap under the tier (one confirmatory test look).
- Kill: K1–K5 (E3 §4).
- Test policy: one confirmatory look after the prereg. Disclose the earlier exploratory look.

**C8. E4 S1–S4**
- Data: 24 repo `*-short.preds.json` plus 2 legacy baselines; VnCoreNLP 1.2.
- Scripts:
  - `E4/protocol_pilot.py` exists; `--check` reproduces the committed p1-gold-short exactly.
  - NOT written: the S2 extensions; S4 `scripts/protocol_card.py` (gatekeeper).
- Compute: ~1.5 CPU-h.
- Prereg PR1–PR4: stress set S = {P1, P2, P3, P5, P7, P8, P9, P11}; endpoints τ-b and significant reversals; detailed-mode predictions; reporting rule R1–R4.
- [SYNTH] Also compute every method's CIDEr guard (M3 G2, M6c) under P0 and P7.
- Kill:
  - K1: > 0.05 CIDEr difference from official.
  - K2: P12 capped at 5 refs gives τ_FT ≥ 0.8 on all 3 seeds.
  - K3: protocol-dependent comparisons are reported as such.
- Test policy: fixed outputs; evaluation only.

**C9. G1 A1–A4 (B optional)**
- Data:
  - preds and test refs;
  - UPE samples `data/results/upe/test/*-T0.5.jsonl`;
  - for B: Visual Genome v1.4 (~1.5 GB).
- Scripts:
  - `G1/g1_tuples.py` exists; its demo asserts pass.
  - NOT written: the UPE wrapper (~20 lines; writes outside `data/results`; shared with C2); B's frozen EN mapping dictionary.
- Compute: ~0.5 CPU-h for A; ~2 CPU-h for B.
- Prereg: freeze the g1_tuples.py sha256, lexicon choices, anchors and per-type frontiers in `manuscript/prereg/<date>_tuple_frontier.json`.
- Endpoint:
  - Relative-TP residual at the run's own tuple count; rel_s and rel_u are primary.
  - For selection methods: paired relation-F1 vs the COUNT control at matched relation count.
- Kill:
  - H1: ≥ 2 runs with |rel_s residual| > 10% and CI excluding 0, or the joint-mean CI excluding 0.
  - H5: the UPE relation residual CI contains 0 on all 3 seeds.
  - A4: the pyvi→VnCoreNLP POS swap moves any ladder exponent by > 0.10.
  - B: H4 shrink < 20%.
- Test policy: the frontiers were fitted on test outputs; disclose this. 35_e has no test decode.

**C10. Unified matcher v3 sensitivity** (V1 + V3 P-B + E3 L1; plus V3 P-A and P-C)
- Data:
  - train-minus-dev300 refs, for deriving the tables;
  - `data/uitviic/instance_gold.json`;
  - COCO instances (P-A, ~3 GB; cluster CPU).
- Scripts:
  - V1: `rescore.py` (`_check()`), `validate.py`, `coverage.py`, `discover.py`. pyvi lives in user site-packages, so run without -I.
  - V3: `taxonomy.py` (asserts; script sha 05992fde…).
  - NOT written: V3's `--refs uitviic` (P-A).
- Compute: ~1.5 CPU-h.
- Prereg:
  - The sha256 of the v3 tables, re-derived on train-minus-dev300. The tables are agent-drafted [MODEL]; each entry needs a human sign-off against a dictionary sense.
  - Predictions: V1 F-1..F-6; V3 H1–H4.
  - "v2 stays PRIMARY".
- Endpoint:
  - V1 F-3: count-control robustness on the SAME gold as the original numbers (panel, S-1).
  - V3 P-A: strict count-flag precision against COCO instance counts.
- Kill:
  - V1: the per-rule drop rules; F-3 flips → STOP and reword "no method survives count control".
  - V3 K1: strict precision < 0.50. K2: |dP| < 0.2 pp. K3: form diffs < 0.5 pp.
- Test policy: v3 test rescoring is a sensitivity analysis after the prereg.

**C11. E5, E2 and M7 analyses**
- E5, S0–S5:
  - `E5/kstar.py` (identity assert), B = 2000.
  - Robustness: v1, hypernym credit, macro, leave-annotator-5-out, dev300.
  - S3: self-pool "samples per annotator".
  - S4: COCO recompute.
  - S5: landed runs, including 35_e on dev.
  - Kill: K1–K5. Compute: ~0.3 CPU-h.
- E2, steps 1–4:
  - `E2/e2_pilot.py` (its `_check()` simulation passes) and `e2_ablation.py`.
  - Bootstrap B = 1000.
  - Robustness: synonym-merged; hypernym-closed; K = 2/3/4 and beta-binomial; matcher v2.
  - Prereg endpoints E1–E3. Kill: K1–K3. Compute: ~0.5 CPU-h.
- M7, C1–C2:
  - `hedge_eval_test.py` (~25 lines from `M7/hedge_eval.py`) is NOT written.
  - Brier and Murphy decomposition over the FIXED 113-class universe.
  - C2: realise the hedges as text; rescore with a hedge-aware matcher; CIDEr style tax (E4 protocol).
  - Prereg in `manuscript/prereg/<date>_hedge_m7.md`: lexicon and scope rule; h = 0.5; thresholds 0.25/0.75; q table from dev300 T0.5 samples only [MODEL].
  - Endpoints E1–E4. Kill: K1–K3. Compute: ~0.6 CPU-h. Test: KTVIC test pools for 3 seeds, after the prereg.

**C12. P-M6b: set-level allocation on test** (0 GPU; needs B0.2 first)
- Data: test pools p1assist_s4{2,3,4}: greedy plus 6 × T0.5 (a 7-caption vote).
- Scripts: from `M6/m6_alloc.py`. The test adaptation is NOT written.
- Prereg:
  - Rule: global top-B by 7-caption vote; ties by the greedy flag, then the train-prior logit.
  - B = each seed's own greedy total.
  - The transductive B is disclosed.
- Primary endpoint: pooled paired dF1 vs greedy at Δm = 0 (object_prf.paired, n = 5000). Dev reference: +1.52 [+0.09, +2.95].
- Kill: pooled dF1 < +0.8, or CI includes 0.
- Secondary: CAR B > 0; residual vs the official frontier.
- Test policy: confirmatory; the rule is frozen from dev.

### B-GPU. Run after B0 rulings; interleave with PD-2 blockers 3–5 as the judge decides

**G-1. M3 CM-DPO, stage 1**
- Compute: 4.2 GPU-h; 0.2 CPU-h. The full programme is ~33 GPU-h.
- P(pass): T1 on test ~25–30% (M3 §0).
- Data:
  - The first 1,000 KTVIC train images in seed-42 order (`M3/out/ktvic_rl1000_ids.txt`). These are the same images 35_e used.
  - Start adapter `$NCS_DATA/runs/p1dev_s42`.
  - dev300.
- Scripts:
  - `M3/cm_pairs.py`: self-check passes; smoke run gave 600 pairs on 177 images.
  - `m3_pilot.py` and `m3_pairs.py` (CPU).
  - `scripts/e5_sample.py` and `evaluate.py` exist.
  - NOT done: the `scripts/train_stage2.py` edit (~12 lines: `--anchor-sft ALPHA`; `image_for()` reads `image_root`), via the gatekeeper.
- Commands: M3 §4.
  - Sample 6 at T0.5 and 6 at T0.8 (top-p 0.95, seed 42), then merge.
  - `cm_pairs.py --mode cm` (CAP 4; |dsyl| ≤ 2; drop copies with m ≥ 0.90; drop CJK and fragments; matcher v2).
  - A 20-pair dry run (≤ 22 GB).
  - DPO: β 0.1, lr 5e-6, 1 epoch, grad-accum 8, α 1.0.
  - dev300 eval.
- Prereg: the frozen settings and hashes. [SYNTH] Proposed additions:
  - panel Δρ_I co-primary (B0.3);
  - a G4-style copy-rate guard (B0.4);
  - CIDEr guard under P0 and P7;
  - the split-annotator re-check with {0,1} → {3,4}.
- Primary endpoint: d-res = [F1 − F̂1(m)]_CM-DPO − [F1 − F̂1(m)]_P1dev on dev300, with the official frontier fixed (B 2000, rng 0).
- Guards:
  - G1: |dm| ≤ 0.20.
  - G2: CIDEr-D ≥ 141.33.
  - G3: ≤ 1 caption in 300 with CJK.
  - G4: syllables ∈ [10.69, 13.06].
  - G5: fragments ≤ 15.
- Kill:
  - PASS: d-res ≥ +1.5, LB > 0, all guards pass.
  - GREY: +0.5 ≤ d-res < +1.5, or ≥ +1.5 with LB ≤ 0. Continue to stage 2 with C2 only.
  - Anything else is a KILL. Any guard failure is a kill.
- Test policy: stage 3 is one pre-registered KTVIC test look.
  - T1: the pooled 3-seed residual > 0 with CI excluding 0. This needs about +2.3, because p1assist_3seed already sits at +0.81 [−1.41, +3.00].
  - T2: attribution vs p1assist and vs C2.
- Condition: B0.5 (D14 scope).

**G-2. M1 grounding screen** (dev300)
- Compute: 1.0–1.3 GPU-h; worst case ~6.6.
- P(pass): ~20%.
- Data:
  - dev300 images;
  - P1_dev greedy (1e183383…);
  - samples T0.5 (876a1d42…) and T0.8 (60ebd640…).
- Scripts:
  - `M1/m1_ground.py` (GPU; step 1 dry run on 2 images checks the box convention);
  - `M1/m1_headroom.py` (CPU);
  - `M1/m1_selfcheck.py`: "selfcheck OK".
  - M2's G-SAL features (box area, centre distance, #boxes, box flag) are already M1's GEOMETRY_ONLY arm. Do not run M2 separately.
- Prereg: `manuscript/prereg/2026-10-1x_m1_grounding.md`, with:
  - hashes and matcher v2;
  - the G0 instrument check: has_box ≥ 0.85 on in-union items and ≥ 0.95 parsed. One fallback with a 113-entry English gloss table [MODEL], +1.0 GPU-h.
  - The control is tie-averaged (B0.1) instead of POOL-VOTE.
  - Model signals [MODEL]: P(có), boxes, attention.
- Primary endpoint: GROUND_ALL vs the control at PLAN-F1 k_i: dF1 ≥ +1.0 with LB > 0, AND dF1 > 0 at greedy k_i and top-3.
- Kill:
  - K1 fails → stop: no stage 1b, no test.
  - K2: "salience" wording only if GEOMETRY_ONLY's LB > 0.
- Test policy: stage 3 only after K1 passes.

**G-3. M6 P-M6c: knapsack captions on test** (conditional)
- Compute: 1.7 GPU-h.
- Conditions: the judge accepts B0.2, and C12 passes.
- Data:
  - p1assist_s4X adapters (n2);
  - new 6 × T0.8 test samples per seed via `scripts/e5_sample.py --n 6 --temperature 0.8 --top-p 0.95`;
  - the existing T0.5 samples.
- Scripts: `plan_f1.py fit` (calibrator weights in the prereg); the knapsack from `M6/m6_alloc.py` §3d. It is not yet standalone.
- Prereg:
  - λ is bisected to match each seed's greedy total; ties go to greedy.
  - The calibrator is fitted once on P1_dev dev300 features, using [MODEL] votes against human ref targets.
  - Disclose the transductive count match. The online variant is a frozen dev λ.
- Primary endpoint: pooled paired dF1 vs greedy at Δm = 0.
- Kill: pooled dF1 < +1.0, or CI includes 0, or CIDEr-D < greedy − 5 (evaluated under P0 and P7).
- Test policy: confirmatory; report a negative in full.

**G-4. E6 P1: the Goodhart curve** (dev300 only)
- Compute: 2.0 GPU-h; 0.3 CPU-h.
- Data: p1assist_s42 adapter; 16 samples per image at T0.5 and T1.0, via the `generate.py` sampling path used for `data/results/upe/p1dev_*`.
- Scripts: selectors A01, A_all, I and label-free self-MBR, built as extensions of `E6/bon_dev.py`. NOT written.
- Prereg:
  - κ16 ≤ 0.35 (object) and ≤ 0.10 (CIDEr).
  - Fitted β(A01, I) > β(A01, A_held), for gain(d) = d(α − βd) with d = sqrt(log n − (n−1)/n). The citation for this form is [UNVERIFIED]; see A-47.
- Primary endpoint: κ16 for the A01 selector at n = 16, count-matched.
- Kill: object κ16 ≥ 0.70 → report 1-D ρ_I only; count-matched d(F1_A_held) CI includes 0 → population regime only.

**G-5. G2-D (XM3600), then G2-B (backbones)**
- G2-D, 1.5 GPU-h:
  - Run the existing queue job `39_xm3600_eval.sh` and `xm3600_oiv7.py score` for P1_s43, fuse2_s42 and zero-shot, short + detailed, on `data/xm3600_subset.txt`.
  - Frontiers vs VI refs (k = 1, 2) and vs OIV7 verified labels.
  - Prediction: b_refs(k=2) ∈ [0.45, 0.60]; OIV7 b at least +0.15 higher.
- G2-B, 7–9 GPU-h, HOLD for B0.6:
  - Zero-shot backbones: Qwen2.5-VL-7B; Qwen3-VL-8B (`scripts/s0_screen.py`); one non-Qwen model that fits in ≤ 24 GB (verify its licence).
  - Each × {EN, VI} × 3 prompts, on COCO-2500 / `manifest_s0_detailed1000.json` / UIT-ViIC test.
  - Plus 6 × T0.5 samples for the one-sentence prompts.
  - Check that evaluate.py / coco_probe accept `--model` and an English prompt.
- Prereg: P1–P4, before any output lands. Kill: K1–K3 (G2 §4).

**G-6. M5: object-budget adapter** (dev300)
- Compute: 2.4 GPU-h (+0.5 for the optional prompt-only arm). Test: ~9 GPU-h for 3 seeds.
- P: frontier-beating ~10%; H0 ~75%.
- Run after C2, because CAR already gives the decomposition.
- Data: train-minus-dev300 refs, 6,938 rows (sft.jsonl sha256 c9ef2097…).
- Scripts: `M5/m5_pilot.py` (build + scorer + `check` → "check ok"), `m5_check.py`, `m5_prefix.py`, `m5_pool7.py`. Decodes use the in-process evaluate.py suffix (M5 §4).
- Prereg: builder rows and sha; suffix text; recipe; greedy decoding; m5_pilot sha; TAU 0.5; pools; official frontier.
- Primary endpoint, for the per-image k_i variant, BOTH of:
  - (a) frontier residual CI > 0;
  - (b) ranking term vs top-m_i by R (tie-averaged) at the same counts, CI > 0.
- Kill:
  - K0: count-token fidelity.
  - K1: ranking ≤ +0.5.
  - K2: CIDEr or CJK.
  - GO to test only if the K1 point estimate is ≥ +1.0.

**G-7. Evaluation expansions** (later; each has its own prereg and kill rules in its report)
- M7 G1, 1.5 GPU-h: hedge presence on COCO-2500 (P1 s43, 6 × T0.5; human instance labels). K3 decides whether vote-based hedges mean salience rather than doubt.
- G1-C, ~4 GPU-h: within-system EOS-bias dial; power law vs saturating curve by AIC.
- X1 P-C, 0.5 GPU-h: LeHaCE-style replication on dev300 (4 length instructions × 2 models).
- V2 S1–S4, 9–10 GPU-h; S5 0.5–2.5 GPU-h: ViPOPE+. The build is CPU (`vipope_build.py` and `pope_vi.py --items` are NOT written). KTVIC negatives are aggregate-only.
- E1 Phase B, 15–30 GPU-h: LLaVA-1.5-7B on LiM CHAIR-500. Run it only after A2 and X1 P-B.

**G-8. M4 CS-RLOO first look: BLOCKED (requires reopening the RL branch)**
- Compute: 4.0 GPU-h; ~22 GPU-h for the full 3+3 confirmatory.
- P(pass): ~25%.
- Blockers:
  - (i) D14 binding condition 1: "no further RL runs".
  - (ii) M4 §4a's own branching rule excludes running after a non-clean kill, because "the engine is untrusted".
  - (iii) 35_e's G4 failure. Exact reference copying rose from 1.00% to 2.25% (3.38× step 0) even with the τ = 0.90 copy mask. This must be diagnosed first.
- Scripts:
  - `M4/train_rl_obj.py` (`--self-check`). It wraps the frozen `train_rl.py` (sha256 bd5743bb…) and `rl_reward.py` (3b18b7a3…), which must still match.
  - `M4/m4_endpoint.py`; `M4/m4_pilot.py`.
- Prereg if reopened:
  - The control is 35_e (its dev outputs now exist).
  - w = 1, s_C 0.525, s_O 0.214; no `--resume`.
  - GO rules as in M4 §4c.
  - [SYNTH] Add: panel Δρ_I ≥ 0 as binding; align the dev endpoint with PD-2's training endpoint (A-08).

### Budget summary

- CPU first wave C1–C12: about 9–10 CPU-h in total, excluding the optional G1 B (~2 CPU-h).
- GPU first wave:
  - G-1 4.2 + G-2 1.0–1.3 + G-4 2.0 = 7.2–7.5 GPU-h.
  - +1.7 if G-3 runs (conditional).
  - Total 8.9–9.2 GPU-h.
- Later: G-5 (1.5 + 7–9), G-6 (2.4), G-7 (up to ~45).
- G-8 (M4) waits for a new judge decision.
