# 11 Limitations and ethics

## 11.1 Limitations

**Scope of the confirmatory evidence.** The sign pattern of the verbosity reward is confirmatory only on COCO-2500, where the predictions were frozen before the run; four of four held. Everything else in Sections 4–7 that concerns the sign is exploratory: the UIT-ViIC results (run before any frozen prediction existed; with the matcher used for Vietnamese the five-reference slope stays negative, −6.28 [−8.34, −3.96]<!-- src: .session_backup/2026-10-14/r11_verify/c2_n1_uitviic_mstar.json :: uitviic_test.lexicons.vi_objects_in.gold_variants.refs5_randk.groups.all_10.slope_F1_mixed_per_logM (CI from the same block; reproduced by RV4, .session_backup/2026-10-14/review_gemini_r10/RV4/work/rv4_n1.json) -->), and the English LVLM test, whose registered verdict was FAILED. The "sign agreement" with $M^*$ fitted on the same outputs is close to an identity under the power-law frontier and is a goodness-of-fit check, not a prediction. The out-of-sample test with an exponent transferred from COCO is pre-registered in commit 4ccbee3 (2026-10-14 23:38 +07), before the first XM3600 result (00:29 +07); the registration is valid. Results not yet reviewed or used.

**What the sign is about.** The verbosity sign is a property of the metric under a given gold and a given family of systems. It is not a statement about human preference: in the human judgments we analysed, judges were close to count-neutral, and their preference for the longer caption sat nearer to the one-reference value of F1 than to the complete-gold value (THumB 0.481 vs 0.411 and 0.835)<!-- src: .session_backup/2026-10-14/r12/H1/pilot_results.json :: THumB.P2a_v_human.est, THumB.P2b_v_F1_refs1.est, THumB.P2b_v_F1_full.est -->. We do not claim that complete gold "recovers" human verbosity preferences.

**Human-judgment regime.** THumB and the Composite set contain short COCO captions that name one or two COCO classes, from pre-LVLM systems, in English. The Composite set has one crowd rater per item. Our human-validity results may not hold for long LVLM descriptions; the DOCCI-Critique test addresses that regime and is pending. Its pre-registration timing is disclosed: the Polaris/DOCCI pre-registration was committed in 7f22d13 (23:47 +07) after the results JSON was written (23:25 +07); this order is disclosed. The registered G3 verdict, computed with the COCO-80 matcher, is pending; results with the ExpandedNouns lexicon are exploratory only. The control-dependence of published gains (Section 6) has not yet been tested against a placebo (two sampling seeds of one model), so the noise level of each control is not yet known.

**Systems and backbones.** The frontier family on COCO-2500 comes from one backbone family (Qwen2.5-VL-7B). Assumption (A3), a shared frontier, holds only within a family: off-style systems fall off it. The English LVLM outputs add seven public backbones but only decoding variants; training-based methods (N9) are pending. The theory covers families on one frontier and says nothing about comparisons across frontiers.

**Vocabulary.** Instance gold is limited to COCO-80, so "complete" gold is complete only for that vocabulary; human agreement under it is an upper bound for this vocabulary.

**Count is not the only confound.** We do not show that object count is a better control unit than word length for English LVLM outputs; the registered test failed. Count matching also does not control which objects are named, by design.

**Large-$k$ behaviour.** The reference limit of the exponent is a two-parameter extrapolation from five points. A test with 10 or 50 references per image is planned but not run.

## 11.2 Data, licences and leakage

**UIT-OpenViIC.** The licence terms we could find record non-commercial research use but no explicit permission for derived per-image panels. We therefore use UIT-OpenViIC only through aggregate statistics (Table 5.1 and Appendix E). No OpenViIC caption, n-gram or per-image derived file appears in this paper or its release; every released file is scanned for OpenViIC 8-grams before publication (0 hits required). TODO: obtain written confirmation from the dataset authors (PD-2 Q4).

**KTVIC–OpenViIC overlap.** KTVIC and UIT-OpenViIC draw on a shared image pool and split it independently. 401 of the 558 KTVIC test images (71.86%) match an image in the OpenViIC training split<!-- src: .session_backup/2026-10-13/r10_cpu/r10_a1_a3_spotchecks_v2.json :: A_32_leakage_disclosure.splits.ktvic_test_558.in_openviic_train, .in_openviic_train_pct -->. No model in this paper is trained on OpenViIC, and the overlap does not affect any result here; we disclose it because the OpenViIC panel rows of Table 5.1 are computed on OpenViIC references of these KTVIC test images, and because the companion paper uses that panel as an independent caption set. Any OpenViIC-trained model must not be evaluated on KTVIC test.

**Other overlaps.** 133 of the 2,695 UIT-ViIC training images are in the COCO Karpathy test split (59 of them in the COCO-2500 probe set, 4 in POPE-500); 21 UIT-ViIC training images are in POPE-500 in all<!-- src: .session_backup/2026-10-13/r10_cpu/r10_a1_a3_spotchecks_v2.json :: A_21_m3_checks.uitviic_overlap.{overlap_with_coco_karpathy_test_5000,overlap_with_coco_probe_manifest_2500,overlap_with_pope500_in_karpathy_test,overlap_with_pope500_all_val2014}; recomputed .session_backup/2026-10-15/paperA_keys/uitviic_karpathy_overlap.json -->. No adapter trained on UIT-ViIC is scored on those sets in this paper.

**Licences of human-judgment data.** THumB 1.0 and the Composite set ship without a licence file. We report aggregate statistics only and cite the sources; we do not redistribute their ratings. KTVIC (motivating case only) ships without a licence file; Paper A reports no KTVIC result. TODO: confirm licences for Polaris (BSD per its release page) and DOCCI-Critique (CC BY 4.0) before use.

**Contamination.** COCO images are likely in the pre-training data of the backbones we score. This affects claims about absolute truthfulness more than the measurement properties studied here, which are computed on fixed outputs.

## 11.3 Analysis provenance and the use of AI agents

Much of the analysis code and many intermediate reports in this project were produced by AI coding agents (two different assistants) under human direction, with an independent agent reviewing the other's results. Reviews found that the agents' JSON outputs reproduced from the raw data, but that their prose, logs and decision notes repeatedly contained numbers that existed in no output file, hard-coded literals presented as computed results, and mislabelled quantities. We adopted the following rules, and this paper follows them:

1. Every number in the paper is generated by a script from a JSON key and listed, with the script and the file's SHA-256, in a numbers manifest released with the code (TODO: `manuscript/number_manifest.tsv`, H6 P1).
2. A number with no computing script is not used. Several values that circulated in project notes were withdrawn on this basis, including a "debiased" Chao2 human ceiling and a set of UIT-ViIC slopes that appeared in a log but in no output file.
3. Predictions are frozen and hashed before the outputs they predict are scored. We distinguish predictions that were committed to version control before the look from those that were only timestamped, and we label every unregistered look as exploratory (prereg ledger, Appendix D).
4. Signals produced by models (sample votes, probe scores, model-judged labels) are used only inside methods and are never treated as gold or as human evidence. No new human annotation was collected.
5. Agents did not write text from memory about the literature: every cited identifier was checked on a primary page, and unchecked items are flagged until checked.

The authors take responsibility for all analyses and text. TODO: check the target venue's policy on disclosure of AI assistance and adapt this subsection.

## 11.4 Broader impact

Count-controlled reporting can make some published improvements look smaller. Our intent is not to discredit specific methods: in several comparisons a gain survives some controls and not others, and we report the full specification curve so readers can judge. The same tools could be used selectively to argue for or against a method; the two-column standard with a pre-declared control is designed to prevent that.
