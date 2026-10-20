# 11 Limitations and ethics

## 11.1 Limitations

**Tab. 7** Frozen tests without a row in another table (full ledger: Supplementary S4).<!-- src: labels from .session_backup/2026-10-18/paperA_tasks/A4.4/tests_status.tsv (sha256 546e7b406ca5) :: status of XM_N1 (gold sizes), XM_N2, B3, E1_A (K1, K3, K4), X1_PB, L6_N9, Q2_LONGCAP, G2_POLARIS, G3_DOCCI, Q4_VAPR; CapArena (Q3) has no row there and no prereg: git show -s 7254a39 ("Q3 CapArena dropped for lack of a licence"); verdicts per row -->

| Test | Label | Verdict | Section |
|---|---|---|---|
| XM3600 gold sizes | registered | 14 of 15 reproduced<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: prereg_comparisons[1..15].in_interval_or_pass (14 IN; prereg_comparisons[6] OUT) --> | 7.5 |
| XM3600 adjacency (N2-XM) | post hoc | at or below null<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: n2_reference_adjacency_verification.full_3600_150_3ref_images.{adjacent_share = 0.5333, bootstrap_ci95_b5000 = [0.4141, 0.6471], exchangeable_null_for_K3 = 0.6667} --> | 7.5 |
| Large reference sets (B3) | registered | pending | 7.7 |
| E1 fidelity (K1) | post hoc | PASS<!-- src: .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json :: fidelity_K1.passes_K1 = True --> | 6.1 |
| E1 stopping rule (K4) | post hoc | control-dependent<!-- src: same :: overview_15_pairs.k4_en_verdict_prefix = NOT_TRIGGERED, k4_en_verdict_sent_tieavg = NOT_TRIGGERED, k4_en_verdict_random_subset = TRIGGERED --> | 6.2 |
| E1 positive control (K3) | post hoc | FAIL: underpowered, 2 of 8<!-- src: same :: controls_K2_K3.registered_k3_en_summary.verdict = FAIL_UNDERPOWERED_ON_2_OF_8_BASELINES_AT_N500, n_baselines = 8 --> | 6.3 |
| Count vs length (X1 P-B) | frozen locally | FAIL (claim killed)<!-- src: same :: x1_pb_english.summary.x1_pb_verdict = KILL_CI_CONTAINS_0 --> | 6.3 |
| Training checkpoints (N9) | registered | not scored: fidelity failed<!-- src: .session_backup/2026-10-19/n9_kf_disclosure/kf_local.json (sha256 9b62eb04) :: K_F.verdict = FAIL; .session_backup/2026-10-13/decisions/PD-15.txt item 3 --> | 6.4 |
| LongCap-Arena (Q2) | registered | MIXED<!-- src: .session_backup/2026-10-15/r13_human/q2_longcap_arena.json :: verdict = MIXED --> | 8.1 |
| CapArena (Q3) | not registered | dropped: no licence<!-- src: .session_backup/2026-10-15/r13_data/licence_check_2026-10-15.json :: CapArena.status = DROPPED_NO_LICENCE --> | 8.1 |
| Polaris-COCO (G2) | frozen locally | PASS<!-- src: .session_backup/2026-10-14/r12_verify/h1_g3_registered_supplement_v2.json :: registered_G2.verdict = PASS --> | 8.3 |
| DOCCI-Critique (G3) | frozen locally | MIXED<!-- src: same :: registered_G3.verdict = MIXED --> | 8.4 |
| VaPR count control (Q4) | registered | PASS<!-- src: .session_backup/2026-10-15/r13_human/q4_vapr_count_control.json :: verdict = PASS --> | 9 |

**Scope of the confirmatory evidence.** The registered evidence on the verbosity sign is the out-of-sample XM3600 test (Section 7.5): it confirms the ordering by gold completeness and the positive large-gold endpoint, and two of its five predictions failed<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: prereg_comparisons[16..20].in_interval_or_pass = PASS, FAIL, PASS, PASS, FAIL -->. COCO-2500 shows the same pattern, but its predictions were frozen locally (file timestamp 2026-10-14 07:22Z, never committed), so it is exploratory<!-- src: manuscript/prereg/2026-10-18_never_committed_frozen_files.json :: files[2] (L1_COCO).mtime_utc = 2026-10-14T07:22:14Z, in_any_git_commit = false -->; UIT-ViIC was scored before any prediction was written. The one-reference sign is observed, not predicted (Section 4.3). The sign with several references is not predicted by the theory: the positive all-references prediction failed on XM3600 and on two English LVLM families (frozen locally), and the paper does not locate the crossing in advance. The "sign agreement" with a fitted $M^*$ is a goodness-of-fit check, not a prediction. The second-backbone and large-$k$ tests are pending (Sections 7.6–7.7). Count-controlled nulls at 500 images are nulls at this sample size (Section 6.3).<!-- src (A6.3 merge, VERIFIED): '500' (E1 nominal image count in the K3 verdict code) = .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json :: controls_K2_K3.registered_k3_en_summary.verdict (number in string) --><!-- A7.3 v2: s10.19 (old §10.5) merged here; its X1 clause is carried by s11.08 below; full s11.03 text in Supplementary S4. -->

**What the sign is about.** The verbosity sign is a property of the metric and its gold, not a statement about human preference: judges were near count-neutral (Section 8.2), and we do not claim that complete gold "recovers" their preference.

**Human-judgment regime.** THumB and Composite hold short English COCO captions from pre-LVLM systems; Composite has one crowd rater per item. For long LVLM descriptions, LongCap-Arena (registered) and DOCCI-Critique (exploratory) are both MIXED (Sections 8.1 and 8.4), and on both the COCO-80 matcher finds only one or two classes per caption. The Polaris/DOCCI pre-registration was frozen locally but committed after the first output, so both are exploratory<!-- src: .session_backup/2026-10-18/paperA_tasks/A4.4/tests_status.tsv :: G2_POLARIS, G3_DOCCI status LOCALLY_FROZEN (t_disk 2026-10-14T15:37:51Z, t_out 2026-10-14T16:25:48Z, t_commit 2026-10-14T16:47:58Z); times in Supplementary S4 -->. The seed placebo that admitted the matched prefix used one model (Section 6.3).<!-- src: .session_backup/2026-10-13/decisions/PD-15.txt :: "K2 HELD with C* = matched_prefix"; two sampling seeds of one model per Section 6.3 -->

**Systems and backbones.** The COCO-2500 frontier family comes from one backbone family (Qwen2.5-VL-7B); assumption (A3) holds only within a family. The English LVLM outputs add seven backbones but only decoding variants; training-based methods (N9) were not scored (Section 6.4).

**Vocabulary.** Instance gold is limited to COCO-80, so "complete" gold is complete only for that vocabulary; human agreement under it is an upper bound for this vocabulary.

**Count is not the only confound.** Prediction X1, that count is a better control unit than length, failed (frozen locally).

## 11.2 Data, licences and leakage

**UIT-OpenViIC.** Its licence terms record non-commercial research use but no explicit permission for per-image panels, so this paper and its release contain only aggregate statistics of it (Table 5.1 and Supplementary S5). TODO: written confirmation from the authors (PD-2 Q4).

**KTVIC–OpenViIC overlap.** The corpora share an image pool (overlap: companion paper); no model here is trained on OpenViIC, and the OpenViIC panel rows (Supplementary S5) are on KTVIC test images.<!-- PD-6 (A6.2 F027–F029, REMOVE_NUMBERS): the overlap counts are Paper B rows (number_manifest.tsv, A_32_leakage_disclosure.*, paper = B) and are not printed in Paper A. -->

**Other overlaps.** Some UIT-ViIC training images are in COCO-2500 and POPE-500; no UIT-ViIC-trained adapter is scored on those sets.<!-- PD-6 (A6.2 F030–F034, REMOVE_NUMBERS): the overlap counts are Paper B rows (number_manifest.tsv, A_21_m3_checks.uitviic_overlap.*, paper = B). The qualitative pointer is kept because Paper A still scores UIT-ViIC-trained systems (Section 7.3, all_10 group). -->

**Licences of human-judgment data.** THumB 1.0 and Composite ship without a licence file; we report aggregates only and do not redistribute ratings. TODO: confirm the Polaris (BSD) and DOCCI-Critique (CC BY 4.0) licences.

**Contamination.** COCO images are likely in the pre-training data of the backbones we score, including UIT-ViIC test, whose images all come from COCO train2017<!-- src: .session_backup/2026-10-18/paperA_tasks/P2/MANIFEST.json (sha256 2ba055342c90) :: numbers[29] datasets.uv231.coco_url_split = {train2017: 231} (source data/datasets/uitviic/test_data.json, images[].coco_url folder); VERIFIED in manuscript/verification/paperA/P2.json; label per judge CC-024 (G2-B prereg 0932ba1) -->; XM3600's images come from Open Images, so exposure is possible there too. This matters more for absolute truthfulness than for the measurement properties studied here, which are computed on fixed outputs.

## 11.3 Broader impact

Count-controlled reporting can make some published improvements look smaller. We do not aim to discredit specific methods: several gains stay significant under some controls and not others, and we report the full specification curve so readers can judge. The tools could be used selectively for or against a method; a pre-declared control guards against that.
