# 5 Reference exchangeability

Section 4 assumed (A1): an image's references are exchangeable draws from independent writers. Every analysis that varies the number of references rests on it, from reference-count curves to "human ceilings" and completeness estimates, yet caption datasets rarely document it.

## 5.1 Diagnostics

For an image with $K = 5$ references in a fixed order, call an object class a *doubleton* if exactly two references name it. The order is the one each release defines:
- COCO-style files (COCO, UIT-ViIC): references ordered by annotation id;
- Flickr30k: the caption-file line order;
- UIT-OpenViIC: the order of the released list.<!-- code: .session_backup/2026-10-14/r11_litmaps/L2/scripts/adjacency_check.py coco_style(path, extract, order='id') sorts each image's captions by annotation id; flickr_entities() uses file line order; openviic_panel() keeps list order; called by .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.py run_b2 -->

Under (A1), the pair of references that name a doubleton is a uniformly random pair, so they are adjacent with probability
$$p_{\text{adj}}^{\,0} = \frac{K-1}{\binom{K}{2}} = \frac{4}{10} = 0.40 .$$
The **adjacent-doubleton share** is the observed fraction of doubletons named by adjacent references, pooled over images, with an image-bootstrap interval; it depends on the order chosen (Supplementary S5). Two companion statistics separate the mechanisms that can raise it:

- the **lag-1 Jaccard excess**: mean Jaccard similarity of the object sets of references at lag 1 minus the mean at lags 2–4 (0 under (A1));
- **slot profiles**: mentions per reference and the frontier exponent $b(1)$ computed from each reference slot alone (flat under (A1)).

A writer who types all references of an image in sequence raises both statistics; length-sorted references produce a position gradient; independent writers produce neither.

## 5.2 Results across corpora

Table 5.1 reports the share; the full corpus–split audit is in Supplementary S5.

**Table 5.1.** Adjacent-doubleton share (exchangeable null 0.40; 95% image-bootstrap intervals).<!-- src (A6.3 merge, VERIFIED): '0.40' (K=5 exchangeable null) = .session_backup/2026-10-14/r11_verify/c3_n2_exchangeability_all_datasets.json :: k5_exchangeability_audit.{flickr30k_captions_coco80,openviic_full_test_exact5_objects_in}.adjacent_share_null (min,max) -->

| Corpus | References | Images | Share | Lag-1 Jaccard excess |
|---|---|---|---|---|
| COCO (Karpathy test), EN | independent | 2,441 | 0.402 [0.361, 0.441]<!-- src: .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B2_L2_exchangeability.datasets.coco_en_test_coco80.adjacent_share, .adjacent_share_ci95 --> | −0.001 [−0.009, +0.006]<!-- src: same :: coco_en_test_coco80.jac_lag1_minus_mean_lag2to4, .jac_diff_ci95 --><!-- src (A6.3 merge, VERIFIED): '2,441' (COCO EN images) = .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B2_L2_exchangeability.datasets.coco_en_test_coco80.images --> |
| UIT-ViIC (all splits), VI | independent | 3,842 | 0.384 [0.366, 0.403]<!-- src: same :: uitviic_vi_all_objects_in.adjacent_share, .adjacent_share_ci95 --> | −0.008 [−0.015, −0.002]<!-- src: same :: uitviic_vi_all_objects_in.jac_lag1_minus_mean_lag2to4, .jac_diff_ci95 --><!-- src (A6.3 merge, VERIFIED): '3,842' (UIT-ViIC VI images) = .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B2_L2_exchangeability.datasets.uitviic_vi_all_objects_in.images --> |
| Flickr30k (Entities chains; Plummer et al., 2015<!-- cite: plummer2015flickr30k (A5.2 v3); arXiv 1505.04870, 'Flickr30k Entities: Collecting Region-to-Phrase Correspondences for Richer Image-to-Sentence Models', verified 2026-10-18 via export.arxiv.org -->) | independent; file order by length? [TODO: trace length-by-position numbers] | 31,783 | 0.483 [0.478, 0.488]<!-- src: same :: flickr30k_entities_chains_visual.adjacent_share, .adjacent_share_ci95 --> | +0.055 [+0.053, +0.056]<!-- src: same :: flickr30k_entities_chains_visual.jac_lag1_minus_mean_lag2to4, .jac_diff_ci95 --><!-- src (A6.3 merge, VERIFIED): '31,783' (Flickr30k Entities images) = .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B2_L2_exchangeability.datasets.flickr30k_entities_chains_visual.images --> |
| UIT-OpenViIC panel, first five refs (aggregates) | — [TODO: check OpenViIC annotation protocol] | 425 | 0.428 [0.385, 0.470]<!-- src: same :: openviic_panel_first5_objects_in.adjacent_share, .adjacent_share_ci95 --> | +0.002 [−0.014, +0.018]<!-- src: same :: openviic_panel_first5_objects_in.jac_lag1_minus_mean_lag2to4, .jac_diff_ci95 --><!-- src (A6.3 merge, VERIFIED): '425' (OpenViIC panel first5 images) = .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B2_L2_exchangeability.datasets.openviic_panel_first5_objects_in.images --> |
| UIT-OpenViIC full test, exactly 5 refs (aggregates) | — | 1,997 | 0.477 [0.458, 0.498]<!-- src: c3_n2_exchangeability_all_datasets.json :: k5_exchangeability_audit.openviic_full_test_exact5_objects_in.adjacent_share, .adjacent_share_ci95 --> | —<!-- src (A6.3 merge, VERIFIED): '1,997' (OpenViIC full test exact5 images) = .session_backup/2026-10-14/r11_verify/c3_n2_exchangeability_all_datasets.json :: k5_exchangeability_audit.openviic_full_test_exact5_objects_in.images --> |

The two independent-annotator caption sets with a documented protocol, COCO and UIT-ViIC, sit at the null in both statistics. Three groups of rows sit above it, and we read each on its own terms.

- **Flickr30k** is above the null under both extractors (0.483 with Entities chains, 0.454 with the COCO-80 matcher) and has a positive lag-1 excess. Its captions come from independent workers, so the excess points to a non-random file order, perhaps by length (TODO: trace mean caption length by file position); it matters for first-$k$ analyses, not random-$k$ ones.<!-- src (A6.3 merge, VERIFIED): '0.483' (Flickr30k Entities adjacency) = .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B2_L2_exchangeability.datasets.flickr30k_entities_chains_visual.adjacent_share; '0.454' (Flickr30k COCO-80 adjacency) = .session_backup/2026-10-14/r11_verify/c3_n2_exchangeability_all_datasets.json :: k5_exchangeability_audit.flickr30k_captions_coco80.adjacent_share -->
- **UIT-OpenViIC** is near the null on the panel subset (0.428) and moderately above it on the full-test exactly-five subset (0.477; Supplementary S5). Its caption-entry protocol is not documented well enough to explain this (TODO: read the OpenViIC paper's annotation section), so random-$k$ subsets should be used.<!-- src (A6.3 merge, VERIFIED): '0.428' (OpenViIC panel first5 adjacency) = .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B2_L2_exchangeability.datasets.openviic_panel_first5_objects_in.adjacent_share; '0.477' (OpenViIC full test exact5 adjacency) = .session_backup/2026-10-14/r11_verify/c3_n2_exchangeability_all_datasets.json :: k5_exchangeability_audit.openviic_full_test_exact5_objects_in.adjacent_share; the UIT-ViIC EN test-split excursion and the panel exact-5 row are in Supplementary S5 -->

A single-writer corpus shows a strong adjacency excess (companion paper). On XM3600 the adjacency check found no excess (post hoc; Section 7.5)<!-- src: .session_backup/2026-10-18/paperA_tasks/A4.4/tests_status.tsv :: XM_N2 status POST_HOC (the prereg quotes the test's own result, adjacent_share 0.5333) -->.

## 5.3 What fails when references are not exchangeable

Dependence among an image's references violates (A1) in two ways, with different consequences (H4 §1a).

**Positive dependence shrinks the gold.** Positively associated references cover fewer objects, so $\bar G(k)$ grows more slowly: $k$ captions from one writer act like $k_{\text{eff}} < k$ independent ones, Proposition 1 holds in $k_{\text{eff}}$, and the crossing moves to larger $k$ (Supplementary S1).

**Slot non-stationarity changes the exponent.** If a writer names different kinds of objects in an early and a later caption (a headline caption first, details later), the reference slot matters even at $k = 1$, and the first-$k$ and random-$k$ designs give different exponents and slopes.

**The exchangeable baseline.** On COCO both effects are absent: an adjacent pair of references is worth $k_{\text{eff}} = 1.98$ [1.943, 2.017] independent references<!-- src: .session_backup/2026-10-14/r12/H4/out/h4_check.json :: coco2500.T3.k_eff_adjacent_pair_slots2to5.point/.ci -->, and the first-$k$ and random-$k$ one-reference slopes agree (−4.21 vs −4.28)<!-- src: .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B1_L1_mstar_and_stopping.check_coco_gold.refs1_firstk.slope, refs1_randk.slope -->.

**Consequences for reporting.**
1. $k$-reference curves should use random-$k$ subsets over all slots, never file order, unless the adjacency statistic is at the null. A one-reference sign computed from one slot of a non-exchangeable corpus is not a property of the metric.
2. A leave-one-reference-out score on single-writer data measures within-writer consistency, not human agreement; it should not be called a human ceiling.
3. Completeness estimators that treat references as independent sampling occasions (Chao2, Good–Turing) give within-writer bounds at best on such data. Paper A reports no Chao-type completeness estimate. <!-- Values withdrawn and NOT used: Chao2 0.848 "debiased ceiling" (R10 correction box; RV2), 0.7325 and LOO 0.7072 (hard-coded literals; H6 §1a(v), D17 §1(b)). -->
4. Rater-equivalence units (Resnick et al.) are defined only where references come from distinct raters.
