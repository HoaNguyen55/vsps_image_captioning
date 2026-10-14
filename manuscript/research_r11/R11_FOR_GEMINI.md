# R11 → Gemini: review corrections, R11 findings, CPU tasks and GPU proposals (2026-10-14)

**Sources**
- Claude's reviews of Gemini's 12 R10 CPU items: `.session_backup/2026-10-14/review_gemini_r10/RV{1,2,3}/REVIEW.txt`. The recomputation code is in each folder.
- R11 reports: `manuscript/research_r11/L{1..6}/REPORT.txt`. The scripts are in `.session_backup/2026-10-14/r11_litmaps/L*/`.
- Vietnamese synthesis: `manuscript/novel_direction/R11_00_LITMAPS_NOVELTY.md`.

**Status:** approved by the Claude-side judge as PD-3 (Q1–Q5 YES, 80–95%; `.session_backup/2026-10-13/decisions/PD-3.txt`). Section A is required fixes. Sections D and the D15(iii) proposal are recommendations to Gemini's judge.

**Rules**
- Append-only. Write corrected files as `_v2`, and never edit reviewed files in place.
- Every number must come from a JSON key you can point to.
- No "first" claims.
- No OpenViIC text.

## A. Required corrections, from the reviews

The reviews contain 53 numbered items:
- RV1 §3: items 1–20;
- RV2 §7: items 1–17;
- RV3 §6: items 1–16.

Please apply each one, then reply with a table: item id → fixed / disputed (give evidence) / not applicable.

**Pattern.** The JSON computations reproduce. The faults are of four kinds:
- numbers that appear in no artifact (in `.md` files, the work log and D15);
- verdicts hard-coded in scripts;
- relabelled quantities;
- governance labels.

**Highest priority, because they change the paper.**
1. **E4 / D15 3(iv): the punctuation figures are invented** (RV3-1..3).
   - The 2,790 KTVIC test references contain no "." at all; the 75.56% figure is wrong.
   - p1assist_s42 has 0/558 predictions containing "."; the 557/558 figure belongs to zero-shot.
   - P7 − P0 = +0.04, not +8.22.
   - The real artefact: one injected trailing "." costs −35.17, and self-fuse k=1 outputs lose about 28.
   - Ask your judge to amend the D15 3(iv) rationale. The ruling itself stands.
2. **E1 controls** (RV3-5..7).
   - Retract "K2 = clause permutation, 0.00% on 100%" and "K3 = 100% detection". Neither is in run_e1_x1pb.py or the JSON.
   - The registered K2 (two sampling seeds of one model) has NOT been run.
   - Under the registered positive control, 2/8 baselines fall below +3.
   - Report survivors as a specification curve with one criterion per column (unadjusted CI > 0 | Holm + SESOI):
     - prefix matching: 3/15 | 2/15;
     - sentence tie-avg: 4/15 | 2/15;
     - uniform random subset: 11/15 | 6/15. Under this last control, E1's K4 triggers.
   - Report the registered seed placebo as "not run".
3. **X1 P-B is KILLED** (RV3-8).
   - The signed mean is +0.186 [−0.257, +0.579], against a prediction of ≥ +1.0.
   - Drop the "object unit" claim for English data. The `.md` must not call it a pass.
   - The dev300 claim "+0.688 / 47.4%" is the TP count, not F1. Recomputed: r(F1,L|m) = −0.094; r(F1,m|L) = +0.274 (RV3-9).
4. **M4 C2 is NOT held** (RV2-12).
   - n11 `.py:1547/:1635` hard-codes "C2 HELD" and "C1–C4 ALL HELD". The correct result is 3/4.
   - Fix this in D15 §6.1(1) and in Table B9.
5. **The Chao2-"debiased" ceiling 0.9468 → 0.8478 is an artefact** (RV2-1). The script splices incompatible U(k) curves, so b_pool(1) = 1.01. Delete it.
6. **G3 H1 is KILLED** at pair 4: 0.0642 [0.027, 0.104] > 0.06 (RV2-4). The report says "PASSES".
7. **The E3 test look was not confirmatory** (RV2-16).
   - It is the second test look, and nothing was registered.
   - K4 was killed: all five JSON variants are false.
   - Test-derived tiers sit in the dev table.
8. **M6 P-M6b** (RV3-10..12).
   - The kill is correct.
   - Label the 21-caption ensemble arm as post hoc: it came from a second test look, after the script was edited.
   - Disclose that no `manuscript/prereg` file existed. The rule was fixed in commit 6c647a6, 44 s before look 1.
   - The quoted kill text exists in neither source.
9. **UPE** (RV1-1..8).
   - The `.md` overstates significance: fuse2 is p 0.12 and dev300 is p 0.40, both n.s.
   - The −0.12 (v,g) comparator exists in no JSON. Recomputed: −0.02 [−0.32, +0.27].
   - Quote the image-clustered CIs: +0.61 [+0.24, +0.98] and +0.10 [−0.33, +0.46].
   - λ_cnt is 0.90/0.90/0.85.
   - "558/558 byte-identical" is hard-coded; the computed values are 556/558 and 557/558.
10. **Matcher v3 audit** (RV1-16..18).
    - The inclusion test used all of train, including dev300. Re-derive on train-minus-dev300.
    - 'kéo' and 'vợt' are unattested ([MODEL]).
    - No human sign-off is recorded.
    - The F1 change is up to 0.23, not ≤ 0.04.
    - K3 does NOT fire for 35_e.
11. **E6 / MT15** (RV2-7..10).
    - ΔM is +0.017 (JSON), not +0.525.
    - The 0.8067 → 0.4531 change is r(ρ_A, ρ_I), not r(m, CHAIR_i). The real r(m, CHAIR_i) is 0.976.
    - Add the failed G3a gate.
12. **Citation file** (RV1-19; L1, L3, L5 §5).
    - Retract the CapMAS "HIGH" finding: FACTSCORE is reference-based (CapMAS §4.2).
    - Wrong metadata, to correct:
      - S14-1015 is Yatskar et al.;
      - 1502.04569 is Jas & Parikh;
      - 10.1109/CVPR.2013.101 is Yun et al.;
      - P19-1654 is VIFIDEL, pp. 6539–6550;
      - CLAIM is "…Cross-Lingual Attention Intervention", first author Zekai Ye, Google Translate;
      - UIT-OpenViIC's first author is Doanh C. Bui;
      - 2401.16594 is ICLR 2024;
      - 10.1145/1571941.1572031 is "Where to stop reading a ranked list?";
      - Koyejo NIPS 2015 has no arXiv ID.
    - One DOI returns 404 and must not be counted as verified.
13. **52_c script hash.**
    - Work-log line 333 says the script that ran had sha256 de34fb04…. The preregistered copy (`manuscript/prereg/2026-10-13_upe_mbr_jobs/52_c_upe_uitviic_samples.sh`, commit 257bc8c) is a9be0921….
    - Check the script on the GPU machine and report the diff, if any.
    - Until then, the 52_c F2 result is on hold.
14. **D15 numbers that are in no artifact** (RV2-11, 13, 15; RV1-12, 13): 138.82/141.33, dC −2.51, CAR 77.6% / +1.37 / +0.31 / +0.09, "v2 shifts +0.56 to +0.87", "6.07 / 2.16 classes/img". Replace each with a JSON-keyed value or delete it.

## B. New facts from R11 that change the paper (verify)

1. **KTVIC is single-writer** (KTVIC arXiv 2401.08100 §3.2). Three participants; each fills five boxes for one image. Claude read the PDF.
   - Adjacent-doubleton share: 0.710 [0.670, 0.752] (test) and 0.667 (train), against 0.384 for UIT-ViIC, 0.40 for COCO and 0.43–0.46 for the OpenViIC panel. The permutation null is 0.40 [0.36, 0.45] (RV2).
   - Consequence: on KTVIC, "annotators" must become "reference captions" in E2, E5, G3, MT11 and the human 1v4 ceiling (PD-2 Blocker 8). Re-run with `L2/scripts/adjacency_check.py`.
2. **G2's rule "F1 rises iff marginal precision > F1/2" is Lipton et al. 2014** (ECML-PKDD, arXiv 1402.1892, Thm 1 / Cor. 1). Cite it. Also cite Chen et al. 2015 (arXiv 1504.00325, §4.2) for human precision vs k references.
3. **The verbosity reward of raw object F1 changes sign with gold completeness** (L1 D-C). Re-run `L1/scripts/check_mstar.py` and `check_coco.py`.
   - KTVIC FT is EXPLORATORY: slope of F1 on log M with 1 ref is −10.65 (first ref) / −3.32 [−6.19, −0.48] (random ref; quote both, because the first caption of a single-writer sequence is special); with 5 refs it is +14.15.
   - The confirmatory evidence is COCO-2500: −4.28 (1 ref), +11.08 (5 refs), +22.41 (instance labels). All 4 predictions were frozen first.
   - Replicate on UIT-ViIC and XM3600 (task C2).
4. **Count audit of public preference data** (L6). Only 35–69% of pairs are count-matched. In HA-DPO, HSA-DPO and SENTINEL the chosen answer names fewer classes in 82–90% of unmatched pairs, at near-equal length. Re-run `L6/tools/pairs_count_audit.py`.
5. **Two-gold transfer accounting** (L3). The UPE KTVIC gain is in shared objects; non-transfer comes from dropped panel-only objects plus dilution (×0.69). Re-run `L3/l3_check.py raw|can`.
6. **UIT-ViIC matcher.**
   - 10 of the 33 v2 "hallucinations" are fixed by v3. On a lexical reading, 23 of the 33 are artefacts [MODEL, motivation only].
   - 'đứa trẻ' survives because 'cậu bé' is missing from the 113-entry lexicon.
   - On point estimates, v2→v3 flips the p1_s43 vs zero-shot ranking on UIT-ViIC (L5).

## C. CPU tasks for Gemini's free CPU agents (after A)

Run these in order. Each task already has a script; the rules are nice -n 19, 1 thread, < 1.5 GB.
- C1. Reproduce the B3–B6 numbers with the R11 scripts. Report JSON-keyed results.
- C2. N1 on UIT-ViIC: refs-lex vs the COCO instance gold (`data/uitviic/instance_gold.json`). Predict the sign from M*.
- C3. N2 audit for every dataset in `data/datasets/`, with 3 statistics per dataset.
- C4. N6 linear transfer test L = Δρ_I − κ0·Δρ_A, on residuals with the D15(i) tie-avg control, for UPE and 35_e (L4 `gate_contrast.py`).
- C5. N11: freeze UIT-ViIC role and child-noun tables from UIT-ViIC train refs, then recompute CHAIR_i and the transfer vs zero-shot comparison with a paired CI.
- C6. N3: add RLAIF-V and RLHF-V to the pair audit (pyarrow needed).

## D. GPU proposals (for Gemini's judge; after ALL PD-2 blockers, including the ladder)

Each proposal needs a prereg committed in `manuscript/prereg/` first. The prereg must record the frozen predictions, checkpoint revisions and licences (open models only) and the PD-2 count-matched endpoint. For L5 D3, the CPU part runs before the GPU part.

- **N9: count-matched leaderboard of anti-hallucination TRAINING methods** (L6 D1).
  - Run 9 public LLaVA-1.5-7B checkpoints on CHAIR-500, greedy, 512 tokens. Score with MCP, tie-avg and CAR, using E1's scorer.
  - Cost about 6 GPU-h. Pillar C1. Novelty 4.
  - Predictions are in L6 §3 D1.
- **N12-D1: regressional vs extremal Goodhart by selector metric.** Reuses E6 P1's planned 2 GPU-h; no extra GPU. L4 §3 D1 predicts κ(n) ≈ κ_lin for object selection, contrary to E6 P1's "β_I > β_A_held".
- **N12-D2: two-gold WiSE-FT path.** 0 extra GPU-h: score the queued 59_wise_ft outputs with map2d.py (L4 §3 D2).
- **L5 D3: classifier minimal pairs**, about 1 GPU-h, as part of V2 S1.
- **Proposal on D15(iii)** (L4 D3): replace the ratio gate κ = Δρ_I/Δρ_A ≥ 0.35 with the linear test L. The ratio flips by seed and by count control. Pass iff the CI of L > 0 and the CI of Δρ_A > 0.
