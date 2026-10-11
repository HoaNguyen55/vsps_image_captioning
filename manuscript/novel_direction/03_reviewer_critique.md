# Reviewer critique: Cross-Lingual Witnesses (XWit), proposal v0

*Stance: IEEE TMM / TPAMI reviewer. Note: `data/object_gold/` holds a 300-image test sample and tool, but no annotations.*

## 1. The eight strongest objections

**O1. The perception/prior dichotomy cannot be identified from cross-lingual agreement.** Co-occurrence priors come from the world, not from one language: a table goes with plates in Vietnamese, English and Chinese text alike. All three languages also share one Qwen2.5 LM. A hallucination that all languages agree on can therefore be a prior, so low ρ does not show "linguistic origin" and high ρ does not show "perceptual origin". Contribution 1's "decomposition without labels" is an unsupported identification claim.
*Control:* (a) Run a blind-prior probe per language: the same prompt with a uniform grey image, plus text-only object completion given the gold object list minus one. This measures each language's prior directly. (b) Build a counterfactual subset: 100 images with one inpainted-out object that co-occurs strongly with the scene (plate, chair, helmet). Measure per-language hallucination of the removed object. Perceptual errors should persist across languages; prior errors should track (a). Without (b), drop the decomposition claim.

**O2. "Language" is confounded with prompt diversity, decoding entropy and caption length.** v2 already shows that more words buy recall and cost precision (zero-shot runs 117 words at P 31.6). English captions will be longer, so English recall may be a length effect, and lower cross-lingual correlation may just reflect a different prompt string.
*Control:* add the same-language paraphrase arm (4 Vietnamese prompts written to elicit the same content) and the within-language sampling arm (K samples, same temperature). Match on length: report every comparison both raw and with each caption truncated to its first M lexicon mentions, where M is the median Vietnamese count. Language counts as a source only if cross-lingual beats paraphrase-vi under length matching.

**O3. Lexicon mapping error correlates with language, so it biases ρ downward.** The 113-entry lexicon was built for Vietnamese. Hand translations into en/zh will not line up in granularity. `xe` covers car, motorbike and bicycle; `người` vs man/woman interacts with gender neutralisation (47.6% gendered gold); Chinese needs a segmenter. Each mapping miss looks like disagreement, which deflates ρ_cross and makes H1 look supported by construction.
*Control:* (a) Use two independent mapping pipelines, direct per-language lexicons and MT-to-Vietnamese followed by the single Vietnamese lexicon, and report H1 under both. (b) Human-audit 200 extracted mentions per language. Reject H1 support if per-language extraction F1 differs by more than 5 points. (c) Also report ρ on classes mapped 1:1 in all languages.

**O4. The gold is reference-derived and its missing labels are not random.** Leave-one-out human recall on KTVIC is 46.9 (§0). Roughly half of the true objects are absent from gold, and the absent ones are background objects, exactly what English witnesses would add. Against this gold, "borrowed recall" gets scored as hallucination, and AUROC (H2/H3) is estimated with heavily corrupted negatives. The bias direction depends on which objects each language mentions, so neither the sign nor the size of Δ is trustworthy.
*Control:* H2, H3 and H4 must be measured on the exhaustive human gold (B1, 300 images, two annotators, κ reported). The sample and tool exist with nothing annotated: B1 is a prerequisite, not a week-8 item. KTVIC reference metrics stay as a secondary column only.

**O5. "Borrowing English recall" is an ensemble, and the paper must beat equal-budget ensembles.** Counting witnesses is majority voting over L×K generations. Self-consistency, cross-model and cross-question checking (SAC3), and cross-lingual consistency of LMs (Qi et al., EMNLP 2023) all exist. Most of the recall gain will come from the *candidate pool* (the union of mentions), not from the *score*. The Neyman–Pearson argument in contribution 2 compares ROCs over a fixed candidate set, but XWit changes that set. "ROC dominance implies PR dominance" is textbook (Davis and Goadrich 2006), not a contribution.
*Control:* split the effect into a pool effect and a scoring effect. (i) Use one pool, the union of all arms, and compare scores: witness count vs. same-language vote at an equal number of generations vs. Vintern logit alone. (ii) Use one score and compare pools. Baselines at equal compute: 12 vi samples, 12 vi paraphrases, Qwen-vi plus a second VLM family in vi. If the cross-model ensemble matches or beats cross-lingual, the paper is about ensembling.

**O6. Translationese, and a missing baseline that may win outright.** The obvious competitor is translate-test: caption in English with Qwen, machine-translate into Vietnamese, then verify with Vintern. If that pipeline matches XWit, the witness machinery is unnecessary. English-only objects must pass a renderer that already loses about 7 recall points and emits errors (`Cái mũ này đang đạp xe`). Human fluency is already the weak column (3.17).
*Control:* add an EN→VI translate-test baseline with and without the Vintern filter. Have native speakers rate fluency and naturalness blind on 100 captions per system.

**O7. The distilled single-pass model may not inherit the ensemble's gain.** The ROC improvement exists only at the ensemble's inference. What the student sees is a rendered target caption. v2 shows that the student reproduces target recall (proxy R 42.4 → test 42.2) but loses precision (40.6 → 38.1). H4 needs P ≥ 41.5 and R > 36.7. A target that is only marginally above the current curve will land on it after the precision slippage.
*Control:* before any training, require the XWit *targets* to dominate the v2/v3 targets on the train proxy by at least 2 points F1 with P ≥ 40.6. Then 3 seeds, paired image-level bootstrap. Add an upper-bound arm, XWit run at inference (no distillation), to quantify the inheritance gap.

**O8. Cost, and an understated Exp-0 budget.** 558 images × 3 languages × 4 = 6,696 detailed generations (about 117 words each) at several seconds per caption on a 3090 with HF `generate`: roughly 5–10 GPU-hours, not 1–2. Full supervision means about 3,700 train images × 12 generations plus Vintern logit passes and a Stage-1 rerun (§6 says every recall lever already requires one). Exp-0 is also planned on the **558 test images**, and fitting f or choosing thresholds there contaminates test.
*Control:* measure throughput (captions/s) on 50 images before committing. Run Exp-0 on the 300 B1 images, keep f fitting and threshold selection on a train/val split, and touch test once.

## 2. Feasibility on one RTX 3090 in about 8 weeks

Exp-0 fits (Qwen2.5-VL-7B bf16 about 17 GB; InternVL2.5-8B loaded separately). The full chain does not fit in 8 weeks at this bar: B1 needs 1–2 weeks of human annotation and gates everything; Stage-1 must be rerun with the T0.5 verifier anyway and witnesses multiply captioning cost about 12×; about 10 SFT runs at half a GPU-day each; and the renderer fix (§6) must land first or any witness gain is lost at rendering.

Realistic plan: weeks 1–2 B1 + Exp-0; week 3 go/no-go; weeks 4–6 train-set witnesses + Stage-1 rerun; weeks 7–8 3 seeds, one ablation set, human evaluation. If Exp-0 is ambiguous, stop.

## 3. Minimal Exp-0 that would convince me

**Images.** The 300 B1 images (stratified sample in `data/object_gold/sample.json`), with exhaustive human gold annotated *before* any analysis. Analysis code and thresholds pre-registered before generation.

**Arms.** Every arm has 4 generations per image, T = 0.7, top-p 0.9, the same max-new-tokens, and the same "describe in detail" intent. Every caption is mapped to the Vietnamese lexicon by both pipelines from O3.

| arm | model | language | prompt | role |
|---|---|---|---|---|
| A | Qwen2.5-VL-7B | vi | fixed | within-language sampling |
| B | Qwen2.5-VL-7B | vi | 4 paraphrases | prompt diversity, same language |
| C | Qwen2.5-VL-7B | vi, en, zh, + vi again | fixed per language | cross-lingual (4 = 3 languages + 1 vi, size-matched) |
| D | InternVL2.5-8B | vi ×2, en ×2 | fixed | second family; cross-model vs cross-lingual |
| E | Qwen2.5-VL-7B | vi, en, zh | grey image | blind language prior (O1) |
| F | Qwen2.5-VL-7B | en → MT vi | fixed | translate-test baseline (O6) |

Arms A–D give the same number of witnesses per image. Total: about 300 × 26 ≈ 8k generations, roughly 6–10 GPU-hours.

**Measures.**
- *Hallucination dependence.* For each pair of generations (g, g′) of the same image, take the indicators "object o hallucinated in g" over the union of hallucinated objects. Use Cohen's κ, not raw ρ, since base rates differ by language. Compare κ_A, κ_B, κ_C and κ_D.
- *Discrimination.* Object-level AUROC and AUPRC of the witness count (0–4) against B1 gold, over the shared union pool (O5), for A, B, C and D, then with the Vintern logit added (logistic regression, 5-fold CV over images).
- *Pool effect.* Union recall on B1 for each arm, raw and at matched mention count M.

**Statistics.** The unit is the image. Use a paired cluster bootstrap over images (10,000 resamples) for every Δκ and ΔAUROC, with 95% CIs and Holm correction across the 3 primary contrasts.

**Sample size.** About 300 images × about 4 hallucinations × 4 generations gives more than 4,000 hallucination events, enough to resolve Δκ ≈ 0.05 and ΔAUROC ≈ 0.02 (confirm SE with a 50-image pilot).

**Primary contrasts and pre-registered decisions.**
1. κ_C < κ_B, under both mappings and under length matching (H1, against the *paraphrase* control, not only against sampling).
2. AUROC_C − AUROC_B ≥ 0.03 with the CI excluding 0 (H2 as stated, a 0.02 margin, is too lenient for a paper claim).
3. AUROC_C ≥ AUROC_D. If cross-model wins, reframe the paper as cross-model witnesses and drop "language".

Stop rule: if 1 or 2 fails, stop; a negative ρ is a workshop note, not the Q2 contribution.

## 4. Verdict

**Not accept-worthy as proposed.** In its current form XWit is a voting ensemble over prompt variants, evaluated against a gold that penalises the very recall it claims to borrow. Its causal story is unidentified, its theory textbook, and its plausible gain is pool enlargement, which any ensemble or translate-test baseline also gets.

**What would upgrade it to a credible TMM submission:**
1. Exhaustive human gold (B1) with κ, used as the primary metric for all object claims.
2. Exp-0 passes contrasts 1–3 against the paraphrase and second-family controls, under both lexicon mappings and length matching.
3. The counterfactual inpainting subset and the blind-prior probe give an actual causal decomposition.
4. XWit beats translate-test and equal-compute ensembles, with the pool and scoring effects reported separately.
5. The distilled student, over 3 seeds and a paired bootstrap, meets P ≥ VSPS and R > VSPS on B1 *and* beats zero-shot on F1 and on human-rated faithfulness, with the inheritance gap reported.
6. Contribution 2 is dropped or demoted to a remark. If kept, it must handle a changing candidate pool.
