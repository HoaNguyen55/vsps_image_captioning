# A3: merging, ensembling and test-time compute as a precision–recall dial (round 2)

**Question.** We have adapters trained on different target policies: P1 is precise with low recall; fuse2 has high recall with lower precision. Can weight merging or test-time compute reach fuse2-level recall at P1-level precision? That would be a Pareto gain, not a move along the trade-off.

**Data.** KTVIC test (558 images, 5 references each), existing greedy predictions only. Object P/R/F1 is computed exactly as in `scripts/object_prf.py`. CIs are paired bootstraps over images, B = 2000 unless stated.

---

## 0. Bottom line

1. **A committee of differently trained adapters does close part of the gap, at equal object count.** It uses 5 adapters (P1 s42/s43, fuse2, E5, E5-DPO) × 2 prompts = 10 greedy captions per image.
   - **Detailed mode.** Extractive sentence cover (objects named by ≥3 of 10; ≤2 member sentences) gives **P 72.7 / R 60.8**, against fuse2's 68.0 / 61.2.
     - That is fuse2's recall (dR −0.4 [−1.9, +1.1]) at **+4.7 P [+3.2, +6.3]**, i.e. 46% of the 10.3-point precision gap to P1.
     - Against the per-image P1/fuse2 mixture with the same object count: +3.5 P [+2.3, +4.9] and +3.0 R [+1.8, +4.2].
     - Against the best mixture of any two single members (the strict hull): +2.5 P [+1.1, +3.7].
   - **Short mode.** Object-F1 MBR over the same 10 captions gives **P 79.2 / R 47.4**, against P1 77.9 / 41.4 and fuse2 75.7 / 47.1.
     - Recall equals fuse2's (dR +0.3 [−1.2, +1.6]); precision is not below P1's (dP +1.3 [−0.9, +3.4]).
     - CIDEr 150.3 (P1 149.8, fuse2 143.9); CHAIR_i 18.3 (P1 19.2, fuse2 21.9).
     - Over the strict hull: +2.9 P [+1.4, +4.2].
2. **Two endpoints are not enough.** Every rule built only from P1 and fuse2 outputs (votes, MBR, second-sentence verification) gains +0.6 to +0.9 P over the strict member hull, with CIs spanning 0. At fuse2's count the set-level vote is +0.1 P [−0.6, +1.0] over the chord.
   - The gain needs target-policy diversity whose errors decorrelate. Reference-false-mention Jaccard: P1 seeds 0.53; P1 vs fuse2 0.24; within the fuse2 family 0.42.
   - In detailed mode it comes from the fuse2 family (fuse2, E5, E5-DPO), not from seeds or from using two prompts.
3. **Weight-space prediction: P1↔fuse2 interpolation is a trade-off knob, not a Pareto tool.** The CPU geometry shows:
   - Every run has its own random LoRA A (factor cosine ≈ 0.00).
   - The ΔW cosine is 0.31 between fuse2 seeds and 0.04 between different policies.
   - A plain midpoint therefore keeps only 0.72–0.81 of the update norm, i.e. it is pulled toward zero-shot.
   - The output ensemble of the same two endpoints, which in the literature upper-bounds the weight soup (rewarded soups), is on the hull.
   - **Predicted:** mixture excess ≤ +1.5 P; Pareto probability ≈ 0.2.
4. **Novelty is low for every merge except one.**
   - P1↔fuse2 interpolation is rewarded soups, which already ran on COCO captioning with a BLEU (precision) vs ROUGE (recall) motivation and found ensembling better than weight interpolation.
   - Seed soups are model soups / DiWA; α > 1 is ExPO / task arithmetic; TIES/DARE are direct applications; scaling one adapter toward the base is WiSE-FT.
   - The one variant with no captioning precedent found is the **cross-dataset coverage analogy**: UIT-ViIC P1 + λ(KTVIC fuse2 − KTVIC P1), scored against COCO instance labels. The human ceiling there is +16.2 instance recall at about 99% instance precision.
5. **The defensible novelty is the test, not the committee.**
   - Equal-object-count comparison against a mixture chord or member hull: no captioning ensemble or merging paper evaluates at matched object count.
   - Object-set F_β as the MBR utility: unused in captioning; nearest is Smatch-MBR and Graphene for AMR.
   - Variant committees vs sample committees for captioning hallucination: not studied.

---

## 1. The decision test (used for every number below)

Systems with different lengths cannot be ranked by P or R alone: naming fewer objects buys precision. For two systems A (P1) and B (fuse2), flipping a coin per image between them achieves every point in between. With mixing weight a:

- TP and the mention count M are linear in a;
- R (a macro mean over images) is linear in a;
- P = TP/M is not linear. This is the Davis & Goadrich (2006) non-linearity of PR space.

For a candidate C with total mentions M_C, `score_frontier.py` reports three tests:

- **mix:** C's (dP, dR) over that mixture at the same M_C. Anything at or below it is a trade-off, not a gain.
- **line:** C's dP over the straight P–R segment at C's recall. This is stricter when fuse2 names more objects.
- **hull** (`hull_check.py`): C's dP over the best mixture of any two single members at M_C. This is the strict null for committees.

All are bootstrapped with C and the baselines on the same resampled images.

**The gap.**

| Mode | P1 | fuse2 |
|---|---|---|
| Detailed | 78.3 / 42.7, 1.83 objects | 68.0 / 61.2, 3.15 objects |
| Short | 77.9 / 41.4, 1.80 objects | 75.7 / 47.1, 2.09 objects |

Two single-system checks:
- Truncating fuse2-detailed to its first sentence gives 76.2 / 46.9 at 2.07 objects, on the chord (mix +0.7 P [−1.2, +2.7]).
- At equal count, fuse2's first-k objects are less precise than P1's: first 2 objects give 74.3 / 44.2 at 1.88, vs P1-detailed 78.3 / 42.7 at 1.83.

---

## 2. CPU pilot 1: output-space committees

Script: `pilot_committee.py`; output `pilot_committee.txt`.

**Members.** 7 systems × {short, detailed}:
- p1-gold (P1 s42)
- p1_s43
- fuse2_s42
- tags_fuse2_s42 (Grounding-DINO tags in the prompt)
- e5_s42 (SFT continued from fuse2 on rejection-sampled train captions)
- e5dpo_s42 (DPO from e5)
- zeroshot

**Committees.**

| Name | Members |
|---|---|
| FT10 | 5 fine-tuned adapters (P1 s42/s43, fuse2, E5, E5-DPO) × 2 prompts, no tags, no zero-shot |
| NOTAGS12 | FT10 + zero-shot |
| ALL14 | everything |
| PF4 | P1 and fuse2 × 2 prompts (the output analogue of merging the two endpoints) |
| PF6 | PF4 + P1 s43 |

### 2.1 Does agreement rank objects?

Candidates are pooled per image; the label is whether any of the 5 references names the object.

| Committee | AUROC of vote count |
|---|---|
| ALL14 | 0.838 |
| NOTAGS12 | 0.836 |
| FT10 | 0.756 |
| PF4 | 0.704 |
| P1 seeds × 2 prompts | 0.703 |

- For FT10, P(in gold | votes) rises from 29% (1 vote) to 91% (10 votes).
- A cross-fitted logistic stacker (member indicators, mention rank, vote count; 2 image folds) reaches AUROC 0.760 vs 0.756 for raw votes, and gives the same equal-count gains. Smarter weighting buys nothing.

### 2.2 Set level: which objects can a vote select at equal count?

This is an upper bound: the selected set is not yet a caption. "Total" means the same total object count as the baseline, allocated across images by votes.

| Committee | At fuse2-det total (3.15/img): P / R | mix dP / dR | At P1-short total (1.80/img): P / R | mix dP / dR |
|---|---|---|---|---|
| PF4 (P1 + fuse2) | 68.1 / 61.8 | +0.1 [−0.6, 1.0] / +0.6 [0.1, 1.4] | 79.8 / 42.5 | +1.9 [0.9, 2.9] / +1.1 [0.5, 1.6] |
| PF6 (+ P1 s43) | 68.5 / 62.2 | +0.5 [−0.4, 1.6] / +1.0 [0.3, 2.0] | 80.5 / 43.2 | +2.6 [1.3, 3.7] / +1.8 [1.0, 2.6] |
| P1 seeds × 2 prompts | cannot reach 3.15 | (−0.4 at 2.30) | 79.3 / 42.5 | +1.4 [0.2, 2.4] / +1.1 [0.3, 1.8] |
| fuse2 alone, 2 prompts | = fuse2 | 0 | 79.1 / 43.3 | +1.2 [−1.1, 3.2] / +1.9 [0.5, 3.3] |
| fuse2 family (fuse2, E5, E5-DPO) × 2 | 70.3 / 63.7 | **+2.3 [1.4, 3.5] / +2.5 [1.7, 3.5]** | 81.0 / 44.1 | +3.1 [0.7, 5.3] / +2.7 [1.2, 4.0] |
| FT, detailed prompt only (5 adapters) | 70.9 / 64.2 | **+3.0 [2.1, 4.1] / +3.0 [2.2, 4.1]** | 81.4 / 44.0 | +3.5 [1.9, 4.9] / +2.6 [1.6, 3.5] |
| FT, short prompt only (5 adapters) | 66.8 / 60.4 | −1.2 [−2.7, 0.5] / −0.8 | 80.9 / 43.8 | +3.0 [1.0, 4.7] / +2.4 [1.2, 3.5] |
| FT10 | 70.6 / 63.8 | +2.6 [1.5, 4.0] / +2.6 [1.7, 3.8] | 81.6 / 44.2 | +3.7 [1.7, 5.3] / +2.8 [1.6, 3.9] |
| NOTAGS12 | 70.6 / 63.6 | +2.7 [1.6, 4.0] / +2.5 [1.4, 3.8] | 82.6 / 44.5 | +4.7 [2.7, 6.3] / +3.0 [1.9, 4.1] |
| ALL14 | 70.6 / 63.6 | +2.7 [1.5, 4.1] / +2.4 [1.3, 3.8] | 82.3 / 44.4 | +4.4 [2.6, 6.0] / +3.0 [1.8, 4.1] |

Reading the table:

- **Leave one system out of FT10** (fuse2-det total): the gain stays at +1.8 to +2.7 P. Dropping E5-DPO costs the most (+2.6 → +1.8). No single member drives it.
- **Ranking vs allocation.** Matching the object count per image instead of in total roughly halves the gain. FT10 vs fuse2-det: +1.2 P [0.2, 2.2] per image vs +2.6 total. FT10 vs P1-short: +2.6 vs +3.7. So about a third to a half of the gain is deciding how many objects each image gets, and the rest is which objects.
- **Error overlap** (Jaccard of reference-false mentions vs reference-true mentions; `pilot_verify.py`):

  | Pair type | FP Jaccard | TP Jaccard |
  |---|---|---|
  | P1 seeds, same prompt | 0.53 | 0.83 |
  | fuse2 family, same prompt | 0.42 | 0.72 |
  | Same adapter, other prompt | 0.43 | 0.69 |
  | P1 vs fuse2 | 0.24 | 0.58 |
  | Zero-shot vs anyone | 0.08–0.10 | 0.37–0.43 |

  Target-policy diversity decorrelates errors about twice as much as seeds, but P1 and fuse2 also share fewer true objects. Hence PF4 does little at fuse2's count.

### 2.3 Realized captions

Realized captions are verbatim member sentences (no rewriting), re-scored with `objects_in`. CIDEr is word-level (RDRSegmenter, `evaluate.py`), scored on n3.

| Caption | P / R / F1 | obj | syl | CIDEr | CHAIR_i | vs fuse2 (dP, dR) | mix dP / dR | line dP | hull dP |
|---|---|---|---|---|---|---|---|---|---|
| P1-detailed | 78.3 / 42.7 / 55.3 | 1.83 | 12.2 | 146.2 | 19.5 | | | | |
| fuse2-detailed | 68.0 / 61.2 / 64.4 | 3.15 | 24.0 | 23.9 | 29.0 | | | | |
| **cover FT10, ≥3 votes, ≤2 sentences** | **72.7 / 60.8 / 66.2** | 2.91 | 17.4 | 72.0 | 24.3 | +4.7 [3.2, 6.3], −0.4 [−1.9, 1.1] | +3.5 [2.3, 4.9] / +3.0 [1.8, 4.2] | +4.5 [2.5, 5.9] | **+2.5 [1.1, 3.7]** |
| cover FT10, ≥4 votes | 75.6 / 54.1 / 63.1 | 2.46 | 14.6 | 94.3 | 21.5 | +7.7, −7.1 | +3.6 [2.3, 5.0] / +2.7 [1.6, 3.8] | +3.7 [1.9, 5.6] | +2.7 [1.3, 3.8] |
| MBR F0.5, NOTAGS12 pool, detailed candidates | 80.0 / 46.3 / 58.6 | 1.95 | 14.1 | 129.9 | 16.9 | vs P1: +1.6 [−0.3, 3.5], +3.6 [2.0, 5.1] | +3.2 [1.6, 4.8] / +1.9 [0.7, 3.1] | +3.6 [1.5, 5.8] | +2.4 [0.8, 3.8] |
| MBR F2, NOTAGS12 | 70.6 / 61.2 / 65.6 | 3.05 | 21.3 | 58.2 | 26.1 | +2.7 [1.2, 4.2], 0.0 [−1.6, 1.6] | +2.2 [0.9, 3.5] / +1.4 [0.1, 2.7] | n/a | +1.2 [−0.2, 2.3] |
| cover PF4, ≥2 votes (P1 + fuse2 only) | 74.2 / 52.4 / 61.5 | 2.41 | 14.1 | 95.0 | 23.2 | +6.2, −8.7 | +1.8 [0.6, 3.1] / +1.6 [0.7, 2.6] | +1.3 [−0.3, 3.2] | +0.9 [−0.6, 2.4] |
| fuse2-det, second sentence kept only if P1-short names its new objects | 74.7 / 50.7 / 60.4 | 2.30 | 13.9 | 101.3 | 22.6 | +6.8, −10.5 | +1.5 [0.1, 3.0] / +1.4 [0.2, 2.5] | +0.9 [−1.2, 2.9] | +0.6 [−1.1, 2.1] |
| *Short mode* | | | | | | | | | |
| P1-short | 77.9 / 41.4 / 54.1 | 1.80 | 12.0 | 149.8 | 19.2 | | | | |
| fuse2-short | 75.7 / 47.1 / 58.1 | 2.09 | 12.4 | 143.9 | 21.9 | | | | |
| **MBR F1, FT10 pool, short candidates** | **79.2 / 47.4 / 59.3** | 2.03 | 12.3 | **150.3** | **18.3** | +3.5 [1.6, 5.3], +0.3 [−1.2, 1.6]; vs P1 +1.3 [−0.9, 3.4], +6.0 [4.6, 7.4] | +3.0 [1.5, 4.6] / +1.5 [0.4, 2.7] | n/a (R > fuse2) | **+2.9 [1.4, 4.2]** |
| MBR F1, PF4 pool | 78.3 / 43.9 / 56.3 | 1.89 | 12.1 | 152.2 | 19.0 | +2.6, −3.2 | +1.2 [0.1, 2.4] / +0.6 [−0.1, 1.3] | +1.3 [−0.0, 3.1] | +0.9 [−0.8, 2.0] |

- Every in-range point of the grid (k ∈ {2, 3, 4} × ≤{2, 3} sentences; β ∈ {0.5, 1, 2}) lies above the P1↔fuse2 mixture for FT10, NOTAGS12 and ALL14. The conclusion therefore does not depend on picking the best grid point.
- Detailed-mode CIDEr-D is dominated by the paper's Gaussian length penalty (fuse2 23.9), so compare it only at matched length.
- Selection rules never read test references, except the stacker, which is cross-fitted.

### 2.4 What this means for merging

- The output ensemble of only the two merge endpoints gives no significant gain over the strict member hull. Rewarded soups (2306.04488, captioning) finds that ensembling beats weight interpolation.
- So a P1↔fuse2 weight merge should be expected on or near the chord. The diversity that works (the fuse2 family, multiple policies) is the thing a soup of more adapters would have to inherit.

---

## 3. CPU pilot 2: weight-space geometry and merge tooling

Scripts: `adapter_geometry.py` computes cosines of ΔW = s·B·A exactly in r×r space. `factor_cos.py` compares raw factors. Both ran on n3 CPU.

| Pair | ΔW cosine | ‖X−Y‖ / ‖·‖ | Plain-soup norm | cos(A) | cos(B) |
|---|---|---|---|---|---|
| fuse2 s42 vs s43 (epoch 1) | 0.31 | 1.18 | 0.81 | −0.002 | −0.008 |
| fuse2 s42 epoch 1 vs 2 | 0.93 | 0.43 | 0.98 | 0.993 | 0.951 |
| fuse2 vs v3 (different targets, "seed 42") | 0.04 | 1.39 | 0.72 | 0.002 | 0.008 |

Consequences:

1. **Every run draws its own random A**, even at the same seed (the LoRA init happens before the trainer seeds), and A barely moves.
   - PEFT's `linear`/`ties`/`dare` `add_weighted_adapter` modes, which act on A and B separately, mix unrelated subspaces. Literature agrees: KnOTS 2410.19735; LoRA Soups 2410.13025; AdapterSoup 2302.07027 ("different seeds average poorly"); CoTo 2506.05713.
   - Only `cat` (exact) or dense-ΔW merges are meaningful.
2. **A plain average of near-orthogonal updates shrinks the update to 0.72–0.81 of its norm**, pulling the model toward zero-shot (WARP 2406.16768, Model Stock 2403.19522). This is why stage A2 includes a WiSE-FT control and stage C a norm-matched soup.
3. **E5 and E5-DPO were continued from the fuse2 adapter** (queue files `21_e5_train.sh`, `22_e5_dpo.sh`), so they share fuse2's A. A fuse2-family soup is in the near-linear regime where soups approximate ensembles. It is the only soup whose output-space analogue shows a gain (+2.3 P / +2.5 R).
4. **Tooling verified.**
   - `merge_lora.py` builds exact rank-sum adapters (A' = [w_i s_i A_i], B' = [B_i], lora_alpha = r'), the same thing PEFT 0.21.2 `cat` does, from state dicts alone, with no base model needed.
   - An end-to-end test (`test_merge_e2e.py`: tiny Qwen2, PEFT save → merge → `PeftModel.from_pretrained`) matches the dense manual merge to 9e-8 in logits, at α = 0.5 and at α = 1.25.
   - On the real 7B adapters (fuse2 + v3 at 0.5/0.5): the merged norm is 17.28 = 0.72 × 24.0 and the cosine with each parent is 0.72, as predicted. `--scale auto` restores 24.0 (×1.389).
   - Dense TIES (`--method ties`, top 30%, sign election, re-factorised by randomized SVD to rank 32) is CPU-heavy: still running after 12 min on n3 (16 cores at load 24, nice 19). Budget about an hour of CPU, or run it on the GPU node before stage D.

## 4. CPU pilot 3: ceiling for the cross-dataset coverage analogy

Script: `uit_ceiling.py`. On UIT-ViIC with COCO-2014 instance labels (human, not reference-derived; 80 classes in Vietnamese via `score_coco_probe.vi_classes`), compare human targets: the first caption (P1 target) vs the fuse2 target built from captions 1–3.

| Split | P1 target P_inst / R_inst | fuse2 target P_inst / R_inst | dR_inst [95% CI] | dP_inst |
|---|---|---|---|---|
| train (2,692) | 99.0 / 30.0 | 99.0 / 49.0 | +19.0 [18.2, 19.9] | +0.0 |
| val (924) | 98.8 / 31.0 | 98.7 / 47.1 | +16.2 [14.8, 17.5] | −0.1 [−0.6, 0.4] |
| test (231) | 99.6 / 30.9 | 99.5 / 47.2 | +16.3 [13.8, 18.9] | −0.1 [−0.8, 0.4] |

Against instance labels, fusion's recall is real and costs no precision: humans do not invent COCO-class objects. A coverage vector that transfers even 25% of this (+4 R_inst) to a single-reference model, at no P_inst cost, would be new evidence that coverage is a dataset-independent skill direction.

---

## 5. Literature

Full texts were read for the papers marked [r], by me or by two literature sub-agents. arXiv DOIs are 10.48550/arXiv.<id>.

**Weight space**
- **Model soups** [r] 2203.05482 (ICML'22): uniform/greedy soups of full fine-tunes from one init. Seed-only pairs differ by small angles and give small gains.
- **WiSE-FT** [r] 2109.01903 (CVPR'22): (1−α)θ0 + αθft between zero-shot and fine-tuned, at or above the chord (α = 0.5 recommended). Needs a shared init.
- **Task arithmetic** [r] 2212.04089 (ICLR'23): τ = θft − θpre; negation, addition, analogies τC + (τB − τA); λ tuned on validation.
- **TIES** [r] 2306.01708 (NeurIPS'23): trim 20%, elect sign, disjoint mean; +1.5 over task arithmetic on 8 ViT tasks.
- **DARE** [r] 2311.03099 (ICML'24): drop and rescale; relies on tiny, redundant deltas.
- **Rewarded soups** [r, captioning section re-read by me] 2306.04488 (NeurIPS'23):
  - ExpansionNetv2 on COCO, one self-critical RL run per reward (BLEU1/BLEU4/ROUGE/METEOR/CIDEr), weights interpolated.
  - Motivation: "shorter descriptions with higher precision can increase BLEU but decrease ROUGE due to reduced recall".
  - Fronts approximate MORL scalarisation. "Ensembling performs better, but … its inference cost is doubled." Seed soups mostly reduce variance.
- **ExPO** [r] 2404.16792: θ1 + α(θ1 − θ0); interpolations lie between the endpoints, with no bulge.
- **DeRa** [r] 2402.02992 (ICML'24): logit mixing equals a KL strength; the weight-space version pays a penalty.
- **LoraHub** [r] 2307.13269: factor merging with cross terms.
- **LoRA Soups / CAT** [r] 2410.13025: exact concatenation; "linear merging … involves additional cross-terms".
- **KnOTS** [r] 2410.19735 (ICLR'25): LoRA updates are poorly aligned; SVD alignment.
- **Personalized soups** [r] 2310.11564.
- **UnIVAL** [r] 2307.16184: interpolation across multimodal tasks including captioning; 0.8·cap + 0.2·VQA gives CIDEr 138.26 vs 136.10.
- **CLP** [r] 2407.15762: merging without training "provably fails" when optima are misaligned. Also Panacea 2402.02030 [r], MOD 2406.18853 [r], DPA 2402.18571 [r].
- **WARP** [r] 2406.16768 and **Model Stock** 2403.19522: interpolation pulls toward the init as updates become orthogonal.
- Caption hallucination and detail: **Nullu** [r] 2412.13817 (CVPR'25, a weight edit that removes a "HalluSpace"); **HallE-Control** [r] 2310.01779 (a trained knob; CHAIR_i 26.6 → 20.9).
- Related merges: **long-to-short merging** [r] 2503.20641 (reasoning ~50% shorter); **IterIS** 2411.15231 (style LoRA merging on BLIP/SentiCap).

**Test time**
- **Consensus reranking:** Devlin et al. [r] 1505.04467 (kNN captions; mean BLEU/CIDEr consensus); m-RNN [r] 1412.6632 (CIDEr 0.819 → 0.917).
- **ECO** [r] 2405.01028: CIDEr consensus plus CLIP among about 60 candidates; 218.47 / 220.53; no object metrics.
- **IC3** [r] 2302.01328 (EMNLP'23): samples plus LLM fusion. Noun recall against the union of references: BLIP 0.266 → 0.353. CIDEr collapses (OFA 1.323 → 0.495). Recall only. K ablation: 0.258 / 0.346 / 0.368 for K = 1 / 10 / 100.
- **MBR for captioning (BLIP-2):** MBMBR [r] 2311.05263, DMBR [r] 2401.05054, AMBR [r] 2401.02749. Utilities are BERTScore or CLIP; no object utility.
- **CBDT** [r] 2509.12677 (EMNLP'25): MBR plus case-based scores; BLEU 25.6 → 26.0.
- **SelfVal** [r] 2601.22451: Best-of-N by object confidence from one model.
  - LLaVA-1.5: CHAIR_I 15.4 → 7.3.
  - **On Qwen2.5-VL-7B, F1 drops** (74.4 → 72.7 / 70.6). Recall falls as N grows (77.1 → 70.4).
- **ConSUM** [r] 2605.29336: summarisation, consensus plus factuality.
- **Atomic Self-Consistency** [r] 2405.13131: a cluster-support threshold Θ as a P/R knob; answers 101 vs 65 words, so not length-matched.
- **ATED** [r] 2510.18321: token-level multi-LVLM ensemble; CHAIR_I gets worse.
- **LoRA ensembles** [r] 2310.00035: multiple-choice QA only.
- **Graphene** [r] 2110.09131 (NeurIPS'21): k-of-m voting over AMR graphs. Heterogeneous parsers (86.26 Smatch) beat 4 seeds (84.78). This is the nearest structural analogue of the object vote.
- **UA-MBR** [r] 2503.05318 (ICLR'25, text): an ensemble of 4 fine-tuned models beats single-model MBR; gains track diversity.
- **MBSE** 2112.07790: Smatch, a set-F measure, as an MBR utility.
- **Length-matched evaluation is rare:**
  - Less-is-More [r] 2402.14545 (single model, truncation baselines).
  - MOCHa [r] 2312.03631 claims a Pareto frontier while length falls 20.4 → 9.7 words.
  - Sandhu et al. 2608.24966 call length matching "the most important missing control".
  - Bianco/Celona 2306.11593 fuse captions from 5 captioners but lengthen them (9.81 → 13.10 tokens).

**Scoop searches.** 13 ran before the shared session quota was exhausted: 3 merging, 9 test-time, 1 by me. They are listed in the sub-agents' notes (summarised here). No hits for:
- merging and caption hallucination / CHAIR;
- a task-vector analogy for captioning coverage (my search: closest are 2507.04380, explanation vectors on image classifiers, and IterIS);
- an object-voting committee of fine-tuned captioners;
- object-F MBR in captioning;
- matched-object-count evaluation of ensembles.

8 planned merging-side and 7 test-time-side searches could not run (quota). Those topics were covered only by direct reads of known papers, so "no scoop" there is **unverified**.

---

## 6. Idea 1: policy-diverse object committee, judged by an equal-count Pareto test

**Mechanism.**
- Caption each image with K adapters that differ in how the 5 references were turned into targets (P1 seeds, fuse2, the queued ladder, E5 variants), under both prompts.
- Keep objects named by ≥k of the outputs and emit ≤2 member sentences that contain only agreed objects (extractive). Alternatively, pick the member caption with the best object-set F_β utility (MBR).
- Report every operating point at equal object count against the mixture and the member hull.

**Closest prior and delta.**
- Prior: Graphene (k-of-m voting, AMR), ASC (Θ knob, QA), ROVER / Gillick & Favre (concept coverage), SelfVal (single model, object confidence; fails on Qwen2.5-VL F1), IC3 (single-model samples, recall only), UA-MBR (fine-tuned ensemble, text).
- Delta:
  - (i) committee members differ only in reference→target policy;
  - (ii) object-set F_β MBR utility (new in captioning);
  - (iii) the equal-count mixture/hull test, since no captioning ensemble has been evaluated at matched object count.
- Method novelty: low. Evaluation novelty: moderate.

**Pilot (sections 2.2–2.3).**
- Detailed: P 72.7 / R 60.8 vs fuse2 68.0 / 61.2; hull +2.5 P [1.1, 3.7]; 46% of the precision gap closed at fuse2's recall.
- Short: 79.2 / 47.4 dominates both endpoints; CIDEr 150.3, CHAIR_i 18.3; hull +2.9 P [1.4, 4.2].
- Two-endpoint committees: not significant over the hull.

**GPU-h.** 0 on KTVIC: the predictions exist, and the queued seed and ladder runs add members for free. `committee_samples.py` runs the variant-vs-sample comparison at equal N as soon as job 35 lands (6 short samples per image for p1_s43 and fuse2_s42).

**Kill criteria.**
- (a) With the ladder adapters added and the rule pre-registered (FT members, k = 3 of 10, ≤2 sentences; short MBR β = 1), the hull excess at equal count is < +1.5 P.
- (b) On UIT-ViIC or COCO with instance labels (jobs 36/38/59 provide P1 + fuse2 + zero-shot members), the mix excess is < +1.0 P_inst. The gain would then be reference convention.
- (c) A sample committee of fuse2 matches the variant committee at equal N. The mechanism would then be sampling, not policy diversity.

**Confidence.**
- 0.75 that the KTVIC gain holds with the ladder.
- 0.4 that it survives instance gold at a useful size.
- Sell it as analysis plus evaluation protocol, not as a method. It costs 10× inference.

## 7. Idea 2: coverage arithmetic between reference policies, with a cross-dataset analogy test

**Mechanism.**
- Exact rank-sum LoRA merges along the coverage direction: ΔW(α) = (1−α)ΔW_P1 + αΔW_fuse2, α ∈ {0.25, 0.5, 0.75, 1.25}.
- Controls: WiSE-FT (0.5·ΔW_fuse2), seed soups, a fuse2-family soup, TIES.
- The analogy **ΔW_UIT-P1 + λ(ΔW_KTVIC-fuse2 − ΔW_KTVIC-P1)**: transfer coverage learned from multiple partial references to a model trained on ONE reference per image in another dataset. Score it against COCO instance labels, with a seed-difference control vector of matching structure.

**Closest prior and delta.**
- Interpolation: rewarded soups (captioning; ensembling better), WiSE-FT, model soups.
- α > 1: ExPO / task arithmetic. TIES/DARE: direct applications.
- Analogy: task analogies (Ilharco 2023, Section 5). No captioning analogue found; this is partly unverified because of the search quota.
- Delta: the merge axis is how references became targets; the readout is the equal-count object frontier plus instance labels.
- Only the analogy is new as an experiment.

**Pilot.**
- Geometry (section 3): independent A per run; seed cosine 0.31; policy cosine 0.04; midpoint keeps 0.72–0.81 of the norm.
- Output proxy: two-endpoint ensembles are on the hull. **Prediction:** interpolation mix excess ≤ +1.5 P, Pareto probability about 0.2.
- Analogy ceiling: +16.2 R_inst [14.8, 17.5] at P_inst 98.7.

**GPU-h** (section 8): about 9.1 total, with gates.

**Kill criteria.**
- A1: mix excess of mix_a0.50 < +1.0 P in both modes → interpolation is only a length/coverage knob (useful for matched-length CIDEr; claim nothing).
- B: ana_l1.00 on UIT val has dR_inst < +2, or ctl_seed moves R_inst as much → kill.
- C: soups ≤ best member, and the family soup's mix excess < +1.5 P → soups reduce variance only.

**Confidence.**
- A1 Pareto: 0.2.
- B success (≥ +4 R_inst, ≥ −1 P_inst, null control): 0.35.
- C1 family soup ≥ +1.5 P over the mix: 0.3.

## 8. GPU job spec

Files are in `jobs/`. All use `scripts/evaluate.py` unchanged: bf16 base like every existing evaluation, greedy decoding, 512 vision tokens. Each stage prints its gate.

Preconditions:
- The A3 scripts are under `/root/r2/A3` on the GPU node. They are already on n3; copy them to n2 if the P1 adapters live there.
- Each adapter directory needs only `adapter_config.json` and `adapter_model.safetensors` (about 80 MB).

| Job | What | Evals | GPU-h |
|---|---|---|---|
| `a3_A1_mix050.sh` | Midpoint P1⊕fuse2, exact cat merge rank 32 (prints the ΔW cosine of P1 vs fuse2) | 1 adapter × 2 modes × 558 | 0.7 |
| `a3_A2_mixgrid.sh` | α ∈ {0.25, 0.75, 1.25}; WiSE-FT control `wise_f2_0.50` | 4 × 2 × 558 | 2.7 |
| `a3_B_uit_analogy.sh` | `ana_l1.00`, `ctl_seed` on UIT test + val; `ana_l0.50` on test; instance-gold frontier and object_prf | (231 + 924) × 2 × 2 + 231 × 2 | 3.0 |
| `a3_C_seed_soups.sh` | C1 fuse2-family soup (fuse2 + E5 + E5-DPO); C2 fuse2 seed soup plain and norm-matched, P1 seed soup (skips cleanly if seeds missing) | 4 × 2 × 558 | 2.7 |
| `a3_D_ties.sh` (optional) | Dense TIES (density 0.3), randomized-SVD rank 32 | 1 × 2 × 558 | 0.7 |

- **Budget:** 9.1 GPU-h for A–C (9.8 with D), at about 20 min per KTVIC evaluation per mode on a 3090.
- **Order and gates:** run A1 first. Run B regardless (it answers a different question). Run D only if A1 shows a Pareto gain.
- **Merging itself** is CPU and takes seconds for cat merges. Dense TIES takes over 12 min of CPU on a busy node (section 3).

**Novelty of each merging variant for captioning:**
- WiSE-FT = `wise_f2_0.50` (one adapter scaled toward the base): not novel.
- Seed soups = model soups / DiWA: not novel.
- P1↔fuse2 interpolation = rewarded soups' captioning interpolation with SFT target policies instead of RL rewards: not novel (empirical delta only).
- α = 1.25 = ExPO / task arithmetic: not novel.
- Fuse2-family soup = checkpoint/trajectory averaging (SWA/LAWA-like): not novel.
- TIES/DARE: direct application. DARE is not run: on a dense ΔW it is undone by the rank truncation, and on factors it is invalid here.
- **Coverage analogy (UIT P1 + KTVIC τ_cov)**: no precedent found; the only variant whose outcome would be new evidence.

## 9. Caveats

- **Gold.** KTVIC gold is the union of references. Precision gains may partly be reference naming conventions; a round-1 analysis against AI-silver annotations (analysis only, not evidence) suggested this. The instance-label checks (kill criteria 6b and 7B) are therefore mandatory before any precision claim.
- **Extra compute in members.** E5 and E5-DPO carry extra training (RFT and DPO on train images), and the detailed-mode gain depends on them (−0.8 P without E5-DPO). The ladder and seeds will tell whether ordinary policy variants suffice.
- **Cost.** The committee costs K× inference: 10 generations per image in the headline setting, 5 with detailed-only members.
- **Search coverage.** The search quota cut the scoop searches short (13 run); unverified topics are listed in section 5.

## 10. Files (all under research_r2/A3/)

| File | Contents |
|---|---|
| `pilot_committee.py` / `.txt` | Committee pilot: baselines, AUROC, set level, realized, stacker, ablations |
| `pilot_verify.py` / `.txt` | Second-sentence verification and error overlap |
| `hull_check.py` / `.txt` | Strict member-hull null |
| `export_committee_preds.py`, `committee_preds/` | Realized captions; frontier and CIDEr results are in `/root/r2/A3/committee_preds` on n3 |
| `score_frontier.py` | mix / line / instance-gold frontier for any results directory |
| `committee_samples.py` | Variant vs sample committee (waits for job 35) |
| `adapter_geometry.py`, `factor_cos.py` | ΔW and factor cosines (n3 outputs in `/root/r2/A3/geometry.txt`, `factor_cos.txt`) |
| `merge_lora.py`, `test_merge_e2e.py` | Exact merge tool and its end-to-end PEFT test |
| `uit_ceiling.py` / `.txt` | UIT-ViIC instance-label ceiling for the analogy |
| `cider_table.py` | CIDEr/CHAIR from evaluate.py JSON |
| `jobs/a3_*.sh` | GPU job spec |
