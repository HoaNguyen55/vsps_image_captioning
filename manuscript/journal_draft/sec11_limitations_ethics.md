# 11 Limitations and ethics

## 11.1 Limitations

**Table 11.1.** Tests without a row in another table (full ledger: Supplementary S4).<!-- src: labels from .session_backup/2026-10-18/paperA_tasks/A4.4/tests_status.tsv (sha256 546e7b406ca5) :: status of XM_N1 (gold sizes), XM_N2, B3, E1_A (K1, K3, K4), X1_PB, L6_N9, Q2_LONGCAP, G2_POLARIS, G3_DOCCI, Q4_VAPR; CapArena (Q3) has no row there and no prereg: git show -s 7254a39 ("Q3 CapArena dropped for lack of a licence"); verdicts per row -->

| Test | Label | Verdict | Section |
|---|---|---|---|
| XM3600 gold sizes | registered | 14 of 15 reproduced<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: prereg_comparisons[1..15].in_interval_or_pass (14 IN; prereg_comparisons[6] OUT) --> | S7 |
| XM3600 adjacency | post hoc | at or below null<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: n2_reference_adjacency_verification.full_3600_150_3ref_images.{adjacent_share = 0.5333, bootstrap_ci95_b5000 = [0.4141, 0.6471], exchangeable_null_for_K3 = 0.6667} --> | 7.5 |
| Large reference sets | registered | not run | 7.7 |
| Re-scoring: fidelity check | post hoc | PASS<!-- src: .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json :: fidelity_K1.passes_K1 = True --> | 6.1 |
| Re-scoring: withdrawal rule | post hoc | control-dependent<!-- src: same :: overview_15_pairs.k4_en_verdict_prefix = NOT_TRIGGERED, k4_en_verdict_sent_tieavg = NOT_TRIGGERED, k4_en_verdict_random_subset = TRIGGERED --> | 6.2 |
| Re-scoring: positive control | post hoc | FAIL: underpowered, 2 of 8<!-- src: same :: controls_K2_K3.registered_k3_en_summary.verdict = FAIL_UNDERPOWERED_ON_2_OF_8_BASELINES_AT_N500, n_baselines = 8 --> | 6.3 |
| Count vs length | pre-specified | FAIL (claim withdrawn)<!-- src: same :: x1_pb_english.summary.x1_pb_verdict = KILL_CI_CONTAINS_0 --> | 6.3 |
| Checkpoint leaderboard | registered | not scored: fidelity failed<!-- src: .session_backup/2026-10-19/n9_kf_disclosure/kf_local.json (sha256 9b62eb04) :: K_F.verdict = FAIL; .session_backup/2026-10-13/decisions/PD-15.txt item 3 --> | 6.4 |
| LongCap-Arena | registered | MIXED<!-- src: .session_backup/2026-10-15/r13_human/q2_longcap_arena.json :: verdict = MIXED --> | 8.1 |
| CapArena | not registered | dropped: no licence<!-- src: .session_backup/2026-10-15/r13_data/licence_check_2026-10-15.json :: CapArena.status = DROPPED_NO_LICENCE --> | 8.1 |
| Polaris-COCO | pre-specified | PASS<!-- src: .session_backup/2026-10-14/r12_verify/h1_g3_registered_supplement_v2.json :: registered_G2.verdict = PASS --> | 8.3 |
| DOCCI-Critique | pre-specified | MIXED<!-- src: same :: registered_G3.verdict = MIXED --> | 8.4 |
| VaPR count control | registered | PASS<!-- src: .session_backup/2026-10-15/r13_human/q4_vapr_count_control.json :: verdict = PASS --> | 9 |

**Scope of the confirmatory evidence.** Section 1 states the claim and its support. In the XM3600 test two of five predictions failed<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: prereg_comparisons[16..20].in_interval_or_pass = PASS, FAIL, PASS, PASS, FAIL -->; cv295 is a replication on discovery images, and the UIT-ViIC pass is not counted. Because the reference golds are nested, their ordering would also arise under random missingness, so the evidence supports the pattern, not the propensity model (Section 4.2). COCO-2500's predictions were pre-specified and never committed<!-- src: manuscript/prereg/2026-10-18_never_committed_frozen_files.json :: files[2] (L1_COCO).mtime_utc = 2026-10-14T07:22:14Z, in_any_git_commit = false -->; UIT-ViIC was scored before any prediction was written. The large-reference-set test is registered, not run (Section 7.7). Count-controlled nulls at 500 images are nulls at this sample size (Section 6.3).<!-- src (A6.3 merge, VERIFIED): '500' (E1 nominal image count in the K3 verdict code) = .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json :: controls_K2_K3.registered_k3_en_summary.verdict (number in string) --><!-- A7.3 v2: s10.19 (old §10.5) merged here; its X1 clause is carried by s11.08 below; full s11.03 text in Supplementary S4. -->

**What the sign is about.** The verbosity sign is a property of the metric and its gold, not of human preference: on short COCO captions judges were near count-neutral (Section 8.2).

**Human-judgment regime.** THumB and Composite hold short English COCO captions from pre-LVLM systems; Composite has one crowd rater per item. For long LVLM descriptions, LongCap-Arena (registered) and DOCCI-Critique (exploratory) are both MIXED, and on both the COCO-80 matcher finds only one or two classes per caption. Polaris and DOCCI-Critique are exploratory (committed after the first output)<!-- src: .session_backup/2026-10-18/paperA_tasks/A4.4/tests_status.tsv :: G2_POLARIS, G3_DOCCI status LOCALLY_FROZEN (t_disk 2026-10-14T15:37:51Z, t_out 2026-10-14T16:25:48Z, t_commit 2026-10-14T16:47:58Z); times in Supplementary S4 -->. The seed placebo used one model and ran in the harness that failed its fidelity check, so it supports no count-control claim (Section 6.3).<!-- src: .session_backup/2026-10-13/decisions/PD-15.txt :: "K2 HELD with C* = matched_prefix"; two sampling seeds of one model per Section 6.3 -->

**Systems and backbones.** The COCO-2500 family uses one backbone (Qwen2.5-VL-7B), and the second backbone is from the same Qwen-VL family; (A3) holds only within a family; the English LVLM outputs add seven backbones but only decoding variants; the training-based checkpoint leaderboard was not scored (Section 6.4). The second-backbone test caps detailed captions at 160 new tokens (Section 7.6).

**System-level sensitivity.** Leave-one-system-out, system-jackknife and within-prompt slopes were computed after review (post hoc; Section 7.8): the label-gold sign survives every drop, and the XM3600 reference-gold sign rests on one verbose system.<!-- CC-088 A-1: was "Leave-one-system-out and within-prompt slopes were not computed" --> **Untested sensitivity.** The Vietnamese lexicon was not perturbed (Supplementary S2 changes the English matcher and the XM3600 label map only), so its effect on the Vietnamese-output results is untested.<!-- PD-29 (c): R1-M1 and R1-M4 kept disclosed as untested sensitivities -->

**Vocabulary.** Instance gold is limited to COCO-80, so "complete" gold is complete only for that vocabulary, and human agreement under it is an upper bound for it.

**Count is not the only confound.** The pre-specified prediction that count is a better control unit than length failed (Section 6.3).

## 11.2 Data, licences and leakage

**UIT-OpenViIC.** Its licence terms record non-commercial research use but no explicit permission for per-image panels, so this paper and its release contain only aggregate statistics of it (Table 5.1 and Supplementary S5).<!-- PD-2 Q4: written confirmation from the OpenViIC authors not obtained -->

**KTVIC–OpenViIC overlap.** The corpora share an image pool (overlap: details withheld for anonymized review)<!-- CP-089 F1/F2 -->; no model here is trained on OpenViIC, and the OpenViIC panel rows (Supplementary S5) are on KTVIC test images.<!-- PD-6 (A6.2 F027–F029, REMOVE_NUMBERS): the overlap counts are Paper B rows (number_manifest.tsv, A_32_leakage_disclosure.*, paper = B) and are not printed in Paper A. -->

**Other overlaps.** Some UIT-ViIC training images are in COCO-2500 and POPE-500; no UIT-ViIC-trained adapter is scored on those sets.<!-- PD-6 (A6.2 F030–F034, REMOVE_NUMBERS): the overlap counts are Paper B rows (number_manifest.tsv, A_21_m3_checks.uitviic_overlap.*, paper = B). The qualitative pointer is kept because Paper A still scores UIT-ViIC-trained systems (Section 7.3, all_10 group). -->

**Licences of human-judgment data.** THumB 1.0 and Composite ship without a licence file; we report aggregates only and do not redistribute ratings. Polaris and DOCCI-Critique are used under their release licences [AUTHOR TO CONFIRM: Polaris BSD; DOCCI-Critique CC BY 4.0]; M-HalDetect is CC BY-NC 4.0 and used for research only.

**Contamination.** COCO images are likely in the pre-training data of the backbones we score, including UIT-ViIC test, whose images all come from COCO train2017<!-- src: .session_backup/2026-10-18/paperA_tasks/P2/MANIFEST.json (sha256 2ba055342c90) :: numbers[29] datasets.uv231.coco_url_split = {train2017: 231} (source data/datasets/uitviic/test_data.json, images[].coco_url folder); VERIFIED in manuscript/verification/paperA/P2.json; label per judge CC-024 (G2-B prereg 0932ba1) -->; XM3600's images come from Open Images, so exposure is possible there too. The measurement properties are computed on fixed outputs, but exposure could change which objects a model names late, and so the salience order; we do not test this.

## 11.3 Broader impact

Count-controlled reporting can make some published improvements look smaller. We do not aim to discredit specific methods, and we report the full specification curve; a pre-declared control guards against selective use of the tools.
