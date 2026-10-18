# 4 A controlled system and its protocol

<!-- Draft 2026-10-15. Training recipe shared with the FAIR 2026 conference version (cited, not re-claimed). -->

## 4.1 Systems

All systems share one backbone, Qwen2.5-VL-7B, and one fine-tuning recipe, the QLoRA recipe of the FAIR conference version (4-bit NF4, LoRA rank 16, α 32, learning rate 10⁻⁴, effective batch 8, two epochs, 512 visual tokens)<!-- src: literature: FAIR 2026 §IV-B (recipe as published) -->. Two prompts are used, a *short* prompt (one sentence) and a *detailed* prompt. Decoding is greedy unless stated. Systems differ only in their training targets or loss mask:

| System | Training targets per training image | Loss |
|---|---|---|
| Zero-shot | none | — |
| P1 | the first reference in file order, short prompt | prompt and response (legacy mask) |
| **P1-R (response-only P1; main system)** | as P1 | response tokens only |
| P1-4ep | as P1, four epochs (compute control) | legacy mask |
| cons | the most *consensual* reference (naming the most objects that another reference also names), short prompt | legacy |
| multiref | all five references as separate short rows | legacy |
| fuse2 | P1's short row, plus one detailed-prompt row joining the consensual reference and the reference that adds the most new objects, each closed with a period | legacy |
| unf2 | the two fused references as two separate short rows (control for concatenation) | legacy |
| rnd2 | as fuse2, but the second reference is drawn at random (control for greedy selection) | legacy |

P1-R is the system we report as our KTVIC baseline. It is P1 with the loss restricted to the response tokens: under the legacy mask the instruction text and the assistant header stay in the loss. The fusion targets are built from human references only. Every object in a fused target was written by an annotator, and the greedy step stops when no reference adds a new object.

The P1 short target uses slot 0 of the single-writer sequence. Slot 0 is the first caption typed and names fewer objects than later slots, so P1-family counts are lower than those of systems trained on consensual or fused targets. We disclose this whenever the two are compared.

## 4.2 Protocol card

Every KTVIC score in this paper uses the following protocol unless a section says otherwise.

| Item | Setting |
|---|---|
| Test set | KTVIC official test, 558 images, 5 references each |
| Segmenter | RDRSegmenter, VnCoreNLP 1.2 (jar SHA-256 recorded in the release); the same segmenter on candidates and references |
| n-gram metrics | pycocoevalcap: BLEU-4, ROUGE-L, CIDEr-D, all ×100 |
| Punctuation | none removed or added; candidates and references scored as written (Section 3.3 reports the stripped variant) |
| Decoding | greedy, one caption per image per prompt |
| Object matcher | v2 (tone-normalised); v1 and v3 as sensitivity |
| Object P / R / F1 | precision micro-averaged over mentions; recall macro-averaged over images with non-empty gold; F1 their harmonic mean; gold = union of the image's references |
| Uncertainty | paired bootstrap over images; image-clustered when seeds are pooled |
| Seeds | 42, 43, 44 |

Scoring runs as a separate process from generation. The committed result files, their SHA-256 values and the scorer version are released.

## 4.3 Registered supervision ladder: design

The ladder asks whether changing the training *targets*, while keeping backbone, recipe and decoding fixed, moves a system off the precision–count frontier of P1, or only along it. Its predictions were frozen and committed on 2026-10-12 (commit 1b5d16b), before any ladder output existed (`manuscript/prereg/2026-10-12_ladder_predictions.json`).

**Frozen anchors.** The frontier is anchored on P1 over three seeds: mean mentioned classes per caption M₁ = 1.7826, precision 78.5188, recall 41.8507, and a precision–count exponent b = 0.7468<!-- src: manuscript/prereg/2026-10-12_ladder_predictions.json :: anchors.frontier.M1 ; P1 ; R1 ; b -->. A run's *frontier residual* is its observed precision minus the precision the frontier predicts at its count.

**Targets.** The recipes change the number of objects per training target: P1's targets carry 1.618 objects per row and cons's 2.033<!-- src: manuscript/prereg/2026-10-12_ladder_predictions.json :: training_targets.p1-short.objects_per_row ; training_targets.cons-short.objects_per_row -->. The implied reference-support thresholds are 0.505 and 0.352<!-- src: manuscript/prereg/2026-10-12_ladder_predictions.json :: training_targets.p1-short.tau ; training_targets.cons-short.tau -->.

**Two models.** Under *L*, a fine-tuned model's count follows the length of its targets and its precision follows one learner frontier. Changing targets then moves a run along the frontier, and residuals are zero. Under *T*, an ideal learner thresholds each object's reference support at the target's implicit threshold. Counts then follow the thresholds and can fall below the target length. The registration gives, for each run, intervals for M, precision and recall, and *L* vs *T* discriminators.

**Registered joint criterion.** The mean frontier residual over all landed runs must have a 95% CI containing 0, with its point in [−0.8, +0.8].

**Disclosed later additions.** An interpretation addendum (`manuscript/prereg/2026-10-14_ladder_interpretation_addendum.md`) added two-one-sided equivalence tests (TOST) with bounds ±1.0 and ±2.0 precision points, per run and pooled. It was committed on 2026-10-14 at 23:38 (+07, commit 4ccbee3), *after* the outputs of runs 54 (P1-4ep) and 55 (cons) existed. The TOST results are therefore post-registration analyses, and we label them so. The addendum also records that KTVIC's single-writer design makes *T*'s binomial assumption false. Outcomes near *T* are reported but not read as support for it, and multiref tests within-writer paraphrase diversity rather than between-annotator variance.

**Runs.** 54 P1-4ep; 55 cons; 56 multiref; 57 rnd2; 58 unf2; plus fuse2 seeds 43 and 44 (short and detailed) as replications of an anchor recipe. Runs 56–58 were lost to a machine failure and are being rerun: **PENDING**.

## 4.4 Second backbone (B1): design

To test whether the frontier and the audit findings depend on the backbone, we registered a second backbone, Qwen3-VL-8B-Instruct, on 2026-10-14 (commit 16795cd), before any of its KTVIC outputs existed (`manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json`). The protocol has three steps, each with a gate.

1. *Step 1, zero-shot language guard on dev300* (about 0.2 GPU-h)<!-- src: manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json :: step1_zeroshot_dev300_guard.estimated_gpu_hours -->. Short captions must be at least 0.98 Vietnamese, with a CJK-character rate of at most 0.02 (0.05 for detailed captions)<!-- src: manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json :: step1_zeroshot_dev300_guard.thresholds.short.vietnamese_share_min ; thresholds.short.cjk_rate_max ; thresholds.detailed.cjk_rate_max -->.
2. *Step 2, one seed* trained on the 3,469 non-dev training images (about 1.8 GPU-h)<!-- src: manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json :: step2_1seed_gate_train_nodev.train_examples ; estimated_gpu_hours -->. Seeds 43 and 44 run only if dev300 output is at least 0.99 Vietnamese with a CJK rate of at most 0.01<!-- src: manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json :: step2_1seed_gate_train_nodev.promotion_gate_to_s43_s44.dev300_vietnamese_share_min ; dev300_cjk_rate_max -->. If the gate fails, B1 stops at one seed and is reported as a boundary condition (PD-6 Q4(b)).
3. *Frontier prediction*: the primary endpoint is equivalence of B1's frontier residual to zero within ±2.0 points<!-- src: manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json :: frozen_frontier_predictions.primary_endpoint_pd2.equivalence_margin_pp -->. The full three-seed budget is 7.0–8.0 GPU-h<!-- src: manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json :: step2_1seed_gate_train_nodev.full_3seed_budget_gpu_hours_min ; full_3seed_budget_gpu_hours_max -->.

**Outcome (pre-registered boundary result): B1 aborted per prereg; 3B fallback run.** Qwen3-VL-8B-Instruct failed the Step 1 guard on dev300. Short captions had a CJK rate of 0.03 (9 of 300), above the maximum of 0.02. Detailed captions had 5.11 mentioned classes per caption, above the registered maximum of 3.5. The Vietnamese share was 1.0 in both modes<!-- src: data/results/b1_qwen3vl/step1_dev300_guard.json :: modes.short.cjk_rate ; modes.short.cjk_count ; modes.detailed.matcher_v2.mentions_per_caption ; modes.short.vietnamese_share ; modes.detailed.vietnamese_share ; pass ; manuscript/prereg/2026-10-14_b1_qwen3vl_predictions.json :: step1_zeroshot_dev300_guard.thresholds.detailed.mentions_per_caption_max -->. As the registration requires, Step 2 was not run. The fallback is Qwen2.5-VL-3B: the same family, tokenizer and recipe at a smaller scale. This paper therefore covers **two model scales of one family (7B, 3B)**, not two backbones. The 3B runs are **PENDING**. A Qwen3-VL "post-guard" run under its own new pre-registration is optional and **PENDING**.

*Calibration note (post hoc).* The detailed-mode maximum of 3.5 was set without checking it against our own backbone: Qwen2.5-VL-7B zero-shot detailed captions on KTVIC test have 6.54 mentioned classes per caption<!-- src: .session_backup/2026-10-13/r10_cpu/v1_v3_unified_v3_audit_v3.json :: part1_unified_v3_sensitivity.ktvic_test558_systems.zeroshot-detailed.v1.M -->. The guard was stricter than our main backbone would itself have passed. We report the abort as registered and do not reinterpret it.

## 4.5 Reproducibility gates

Two checks guard the main number.

**Second machine.** A second machine checked out the repository at a fixed commit, rescored the committed P1-R seed-42 predictions, and reproduced the committed result file byte for byte. Its CIDEr-D, 148.66, equals the committed value<!-- src: .session_backup/2026-10-14/r12_verify/g1_repro_gate_machine2.json :: metric_comparisons.CIDEr.rescored_value -->.

**Live segmenter.** All three P1-R seeds were rescored with a live VnCoreNLP 1.2 run. CIDEr-D, BLEU-4 and ROUGE-L match the committed files with an absolute difference of 0.0 on every seed<!-- src: .session_backup/2026-10-15/paperA_keys/cider_3seed_g1_rescore_check.json :: per_seed|p1assist_s42-short|CIDEr_abs_diff (and the same key for s43, s44) -->.

Before any experiment ran, the freeze date was set to 2026-11-15 (D18): a job not finished by then is dropped or moved to a list of reviewer-requested runs.
