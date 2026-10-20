# 8 Limitations and ethics

<!-- Draft 2026-10-15. -->

## 8.1 Limitations

**One model family.** All results come from Qwen2.5-VL with one QLoRA recipe. The registered second backbone (Qwen3-VL-8B-Instruct) failed its Step 1 guard and was aborted per the registration (Section 4.4). The 3B fallback adds scale, not diversity, and is **PENDING**. We claim two model scales of one family (7B, 3B), not two backbones.

**Ladder limits.** Runs 56–58 were rerun after a machine failure and scored once by the registered check. Six of the ten landed runs fall inside all their registered intervals<!-- src: .session_backup/2026-10-18/ladder_check/final/stdout.txt :: lines 1-10 (rule: a run is inside when its line has no OUT; 6 of 10) -->, four of the ten are seed replications of one recipe, and each ladder step has one seed. The registered frontier-invariance H0 is not met: its pooled part is met, but its per-run part is not (8 of 10 runs within ±1.0)<!-- verbatim, judge PD-20 ; src: manuscript/prereg/2026-10-12_frontier_invariance_V4.txt:233-236 (rule; per-run clause l.235, pooled clause l.236) ; .session_backup/2026-10-18/ladder_check/final/stdout.txt :: line 11 (95% CI) ; lines 1-10 (per-run points; |point| <= 1.0 on 8 of 10) ; line 1 (p1ep4_s42-short −1.59) ; line 3 (cons_s42-short +1.44) ; manuscript/verification/paperA/LADDER_CHECK_final.json :: rows[0].items.C2.evidence (−0.007) -->. The TOST at ±0.8, added after the first ladder output, fails on the six runs landed before the reruns (Section 5.2). A registered weight-interpolation control, WiSE-FT (run 59), has run, but four of its registered reporting items are **PENDING** (Section 6.6). Its registered α* rule filters on a KTVIC test guard, which conflicts with our rule that no hyperparameter is chosen on KTVIC test; here the guard did not bind.

**Single seeds for some runs.** Each ladder step, cons included, has one seed. A miss of one to three precision points cannot be separated from seed noise.

**No human judgments.** We collected no new human annotation. The OpenViIC panel is a second set of captions, not ground truth. The within-writer leave-one-out figures are not a human ceiling. Model-generated signals (sample votes, kNN priors, model-drafted matcher rules) serve only inside methods and never as evidence.

**B-N3: NOT_RUN.** The prior FAIR-2026 ratings (2 raters, 150 captions) exceeded our pre-set agreement gate (identical scores on 71–87% of captions per scale, against a threshold of 50%), so, as fixed in advance, no criterion analysis was run.<!-- verbatim, judge PD-21b ; src: .session_backup/2026-10-19/HL_human_labels/b_n3_quality_gate.json :: per_scale (identical_share min and max) ; n_items ; rule ; STOP ; inputs_sha256 (2 rater files) -->

**Matcher v3 is unattested.** Its rules were drafted by an AI model and have no human sign-off. No conclusion in this paper depends on it.

**Exploratory and post hoc analyses.** The following are exploratory or post hoc under the registration labels of Section 6, and are labelled so where they appear: the UIT-ViIC slope differences, the second P-M6b look, the 35_e count-matched endpoint, the kNN-prior test (locally frozen), the PLAN-F1 dev300 critique, the EV-RANK ranking concordance and all TOST results.

**Comparators.** No published Vietnamese system has been rescored under our protocol. HDUCap and ViG could not be read in full (Section 2). We therefore make no ranking claim.

**XM3600 decomposition is partial.** On XM3600, appending a period to the fine-tuned outputs raises CIDEr-D by +2.71 (P1) and +2.75 (fusion)<!-- src: .session_backup/2026-10-18/cpu_audit_r15/xm3600_period_cider_decomposition_v1.json :: cross_system_drop_decompositions_token_level.p1_s43_short_vs_zeroshot_short.drop_decomposition.by_append_period_to_ft_pred.cider_shift_x100.est ; cross_system_drop_decompositions_token_level.fuse2_s42_short_vs_zeroshot_short.drop_decomposition.by_append_period_to_ft_pred.cider_shift_x100.est -->, but both systems still score below the zero-shot backbone (Section 3.3). We measure the period's effect in absolute points only. The rest of the drop is not decomposed, so we do not attribute it to template or content.

## 8.2 Data, licences and release

We use KTVIC as publicly released by its authors (Pham et al., 2024) and the other datasets under their published terms. We redistribute no images or reference captions; we release code, matchers, split/image IDs and aggregate scores, and readers obtain the data from the original sources.

**UIT-OpenViIC** is used only through aggregate statistics. No OpenViIC caption, n-gram or per-image derived file appears in this paper or its release. Every released file is scanned for 8-gram overlap with OpenViIC captions before publication, and the scan must find none.

**Leakage rules.** 401 of the 558 KTVIC test images are in OpenViIC's training split. No model here is trained on OpenViIC, and an OpenViIC-trained model must not be evaluated on KTVIC test. Any UIT-ViIC-trained adapter is scored on POPE-500 with all 21 UIT-ViIC training images excluded, and on the COCO probe without its 59 (Section 3.6). ViCLIP-OT is trained on UIT-OpenViIC, so the same overlap applies to it, and it is never used as an evaluator on KTVIC test.

**People in images.** Captions describe everyday scenes with people. No identity recognition is performed. Matcher rules for role and gender nouns are documented so that their effect on scores can be inspected.

## 8.3 Relation to the conference version and the companion paper

A conference version of part of this work appeared at FAIR 2026 ("A Method for Reducing Hallucinations in Detailed Vietnamese Image Captioning Using Supervision from Verified Propositions"). That paper's contribution, VSPS supervision from verified propositions, is not a contribution of this paper. What we reuse from it is the KTVIC/COCO setup, the QLoRA recipe and the P1 control. P1's seed-42 score (149.8 there, 149.79 here under the same scorer) serves only as a reference point. `new_vs_FAIR.md` itemises the overlap. A companion paper on object-count confounding in hallucination metrics is under review. It uses KTVIC only as a motivating example, and no number is a primary result in both papers.

## 8.4 Analysis provenance and the use of AI agents

Much of the analysis code and many intermediate reports were produced by AI coding agents (two different assistants) under human direction, with one agent reviewing the other's results. Reviews found that the agents' JSON outputs reproduced from raw data, but that their prose and logs sometimes contained numbers that existed in no output file, or that disagreed with the JSON. This draft follows the rules of the companion paper:

1. Every number is read from a JSON key and listed with its file hash in `number_manifest_B.tsv`.
2. A number with no computing source is not used. For example, a zero-shot CIDEr of 34.33 that came from a re-implemented scorer is replaced by the committed scorer's 28.98.
3. Every test carries one of four registration labels, computed from commit, push, file and output times (Section 6). The REGISTERED tests had their predictions committed before the outputs they predict: the ladder's H0 and interval predictions, UPE-MBR, the RL gate, P-M6b (look 1), B1 and the WiSE-FT gate. The ladder TOST, the EV-RANK concordance and the PLAN-F1 critique are POST_HOC. The kNN-prior test and the M4 C2 prediction are LOCALLY_FROZEN. All five are treated as exploratory<!-- src: .session_backup/2026-10-18/paperA_tasks/A4.4/reconcile.tsv :: row 449 ; tests_status.tsv (all B tests) -->.
4. Model-generated signals are never gold or human evidence. No new human annotation was collected.
5. Every cited identifier is checked on a primary page, and unread papers are cited without their numbers.

The authors take responsibility for all analyses and text. TODO: adapt this subsection to the target venue's policy on AI assistance.
