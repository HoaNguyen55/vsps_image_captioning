# 5 Reference exchangeability

Section 4 assumed (A1): the references of an image are exchangeable draws from independent writers. The same assumption sits under every analysis that varies the number of references: reference-count curves of a metric, leave-one-reference-out "human ceilings", inter-annotator agreement, rater-equivalence units (Resnick et al.) and species-richness estimates of gold completeness (Chao2). Caption datasets rarely document whether it holds. This section gives a cheap diagnostic, applies it to four caption corpora, and shows what changes when it fails.

## 5.1 Diagnostics

For an image with $K = 5$ references in file order, call an object class a *doubleton* if exactly two references name it. Under (A1), the pair of references that name a doubleton is a uniformly random pair, so the probability that the two are adjacent in file order is the number of adjacent pairs over the number of pairs,
$$p_{\text{adj}}^{\,0} = \frac{K-1}{\binom{K}{2}} = \frac{4}{10} = 0.40 .$$
The **adjacent-doubleton share** is the observed fraction of doubletons named by adjacent references, pooled over images, with an image-bootstrap interval. Two companion statistics separate the mechanisms that can raise it:

- the **lag-1 Jaccard excess**: mean Jaccard similarity of the object sets of references at lag 1 minus the mean at lags 2–4 (0 under (A1));
- **slot profiles**: mentions per reference and the frontier exponent $b(1)$ computed from each reference slot alone (flat under (A1)).

A writer who types all references of an image in sequence produces a high adjacent share and a positive lag-1 excess (each caption echoes the previous one). References sorted by length produce a position gradient in mentions and a smaller adjacency excess. Independent writers produce neither.

## 5.2 Results across corpora

Table 5.1 reports the adjacent-doubleton share. All values use the same code; objects are extracted with the Vietnamese lexicon matcher for Vietnamese references and the COCO-80 matcher for English ones.

**Table 5.1.** Adjacent-doubleton share (null 0.40 under exchangeability). 95% image-bootstrap intervals.

| Corpus | References | Images | Share [95% CI] | Lag-1 Jaccard excess [95% CI] |
|---|---|---|---|---|
| COCO (Karpathy test), EN | independent crowd workers | 2,441 | 0.402 [0.361, 0.441]<!-- src: .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B2_L2_exchangeability.datasets.coco_en_test_coco80.adjacent_share, .adjacent_share_ci95 --> | −0.001 [−0.009, +0.006]<!-- src: same :: coco_en_test_coco80.jac_lag1_minus_mean_lag2to4, .jac_diff_ci95 --> |
| UIT-ViIC (all splits), VI | independent annotators | 3,842 | 0.384 [0.366, 0.403]<!-- src: same :: uitviic_vi_all_objects_in.adjacent_share, .adjacent_share_ci95 --> | −0.008 [−0.015, −0.002]<!-- src: same :: uitviic_vi_all_objects_in.jac_lag1_minus_mean_lag2to4, .jac_diff_ci95 --> |
| UIT-ViIC images, COCO EN references | independent crowd workers | 3,850 | 0.406 [0.380, 0.429]<!-- src: same :: uitviic_images_coco_en_refs_coco80.adjacent_share, .adjacent_share_ci95 --> | +0.005 [−0.001, +0.011]<!-- src: same :: uitviic_images_coco_en_refs_coco80.jac_lag1_minus_mean_lag2to4, .jac_diff_ci95 --> |
| Flickr30k (Entities chains) | independent; file order sorted by length [TODO: trace length-by-position numbers] | 31,783 | 0.483 [0.478, 0.488]<!-- src: same :: flickr30k_entities_chains_visual.adjacent_share, .adjacent_share_ci95 --> | +0.055 [+0.053, +0.056]<!-- src: same :: flickr30k_entities_chains_visual.jac_lag1_minus_mean_lag2to4, .jac_diff_ci95 --> |
| UIT-OpenViIC, test-image panel (aggregates only), images with ≥5 refs, first five | — [TODO: check OpenViIC annotation protocol] | 425 | 0.428 [0.385, 0.470]<!-- src: same :: openviic_panel_first5_objects_in.adjacent_share, .adjacent_share_ci95 --> | +0.002 [−0.014, +0.018]<!-- src: same :: openviic_panel_first5_objects_in.jac_lag1_minus_mean_lag2to4, .jac_diff_ci95 --> |
| Flickr30k captions, COCO-80 matcher | independent | 31,783 | 0.454 [0.440, 0.466]<!-- src: .session_backup/2026-10-14/r11_verify/c3_n2_exchangeability_all_datasets.json :: k5_exchangeability_audit.flickr30k_captions_coco80.adjacent_share, .adjacent_share_ci95 --> | — |
| UIT-OpenViIC, test-image panel, images with exactly 5 refs (aggregates only) | — | 251 | 0.461 [0.401, 0.519]<!-- src: c1_b1_b6_reproduction.json :: B2_L2_exchangeability.datasets.openviic_panel_exact5_objects_in.adjacent_share, .adjacent_share_ci95 --> | +0.010 [−0.013, +0.029]<!-- src: same :: openviic_panel_exact5_objects_in.jac_lag1_minus_mean_lag2to4, .jac_diff_ci95 --> |
| UIT-OpenViIC, full test split, exactly 5 refs (aggregates only) | — | 1,997 | 0.477 [0.458, 0.498]<!-- src: c3_n2_exchangeability_all_datasets.json :: k5_exchangeability_audit.openviic_full_test_exact5_objects_in.adjacent_share, .adjacent_share_ci95 --> | — |

<!-- Further rows for Appendix E (all c3_n2_exchangeability_all_datasets.json :: k5_exchangeability_audit.*): UIT-ViIC VI train/val/test 0.3833/0.3851/0.3822; UIT-ViIC EN refs train/val/test 0.415/0.341/0.5412 [0.4359, 0.6484] (231 images); OpenViIC panel train exact5 0.4397, first5 0.4141; OpenViIC full train exact5 0.4543, first5 0.3974; OpenViIC full dev 0.4102. Single-writer corpus rows are reported in the companion paper (Paper B owns the KTVIC audit; PD-6 Q1(a)). -->

The two independent-annotator caption sets with a documented protocol, COCO and UIT-ViIC, sit at the null in both statistics. Three groups of rows sit above it, and we read each on its own terms.

- **Flickr30k** is above the null under both object extractors (0.483 with Entities chains, 0.454 with the COCO-80 matcher) and has a positive lag-1 Jaccard excess. Flickr30k's captions come from independent crowd workers, so the excess points to a non-random file order rather than to shared writers; a length ordering of the five captions would produce it (TODO: trace mean caption length by file position before stating this as fact). The diagnostic flags an ordering artefact, which matters for any first-$k$ analysis but not for random-$k$ analyses.
- **UIT-OpenViIC** is near the null on the panel subset used elsewhere (0.428 for the first five of ≥5 references, lag-1 excess +0.002) and moderately above it on the exactly-five subsets (0.461 on 251 panel images; 0.477 on 1,997 full-test images), without a clear lag-1 Jaccard excess where that statistic is available. We do not know OpenViIC's caption-entry protocol in enough detail to explain the difference between subsets (TODO: read the OpenViIC paper's annotation section). We report these values and draw no conclusion from them beyond this: OpenViIC references should not be assumed fully exchangeable in file order, and random-$k$ subsets should be used with them.
- **UIT-ViIC English references, test split only** (0.541 [0.436, 0.648] on 231 images) are above the null while the train and validation splits (0.415, 0.341) and the pooled value (0.406) are not<!-- src: c3_n2_exchangeability_all_datasets.json :: k5_exchangeability_audit.uitviic_en_{test,train,val,all}_coco80.adjacent_share -->. With several dozen corpus–split rows in the audit (Appendix E), one small-split excursion of this size is not surprising; we treat the pooled value as the estimate.

A corpus in which one writer enters all references of an image in sequence shows a strong adjacency excess and a large lag-1 Jaccard excess; that case, and its consequences for one Vietnamese benchmark, is analysed in the companion paper (Paper B, under review). On XM3600 (150 images with three Vietnamese references; exchangeable null 2/3), the registered adjacency check passed with no excess (Section 7.5).

## 5.3 What fails when references are not exchangeable

Dependence among an image's references violates (A1) in two ways, with different consequences (H4 §1a).

**Positive dependence shrinks the gold.** For positively associated indicators, $P(o \notin G_k) \ge (1-\pi)^k$ (Esary, Proschan and Walkup, 1967, Ann. Math. Statist. 38(5):1466–1474, DOI 10.1214/aoms/1177698701) [UNVERIFIED: bibliographic data verified via Crossref; the location of the product inequality in the paper not checked, the publisher full text is behind a bot challenge], so coverage and $\bar G(k)$ grow more slowly than under independence. For a lag-1 chain with autocorrelation $\rho$, $c_k(\pi) = 1-(1-\pi)\big(1-(1-\rho)\pi\big)^{k-1} \approx k_{\text{eff}}\,\pi$ for small $\pi$, with $k_{\text{eff}} = 1 + (k-1)(1-\rho)$: $k$ captions from one writer act like $k_{\text{eff}} < k$ independent ones. The chain kernel is still reverse-rule of order 2 (checked numerically for $\rho \in \{0.2, 0.5, 0.8\}$), so Proposition 1 holds in $k_{\text{eff}}$ and the crossing moves to larger $k$. The chain model predicts that dependence acts on the gold size to first order and on the exponent only to second order.

**Slot non-stationarity changes the exponent.** If a writer names different kinds of objects in an early and a later caption (a headline caption first, details later), the reference slot matters even at $k = 1$, and the first-$k$ and random-$k$ designs give different exponents and slopes.

**The exchangeable baseline.** On COCO both effects are absent, as (A1) predicts. An adjacent pair of references is worth $k_{\text{eff}} = 1.98$ [1.943, 2.017] independent references<!-- src: .session_backup/2026-10-14/r12/H4/out/h4_check.json :: coco2500.T3.k_eff_adjacent_pair_slots2to5.point/.ci -->; adjacent and non-adjacent pairs give the same gold size ($\Delta\bar G$ −0.000 [−0.009, +0.008]) and exponent ($\Delta b$ −0.002 [−0.007, +0.003])<!-- src: same :: coco2500.T3.lag1_minus_lag2plus_all.Gbar.point/.ci, .b.point/.ci -->; the five single-slot exponents lie between 0.475 and 0.489, and slot 1 differs from the mean of slots 2–5 by −0.003 [−0.018, +0.012]<!-- src: same :: coco2500.gold.s1..s5.b; coco2500.T3.slot1_minus_slots2to5.b.point/.ci -->. First-$k$ and random-$k$ one-reference slopes agree to within 0.07 (−4.21 vs −4.28)<!-- src: .session_backup/2026-10-14/r11_verify/c1_b1_b6_reproduction.json :: B1_L1_mstar_and_stopping.check_coco_gold.refs1_firstk.slope, refs1_randk.slope -->. The single-writer case, where both effects appear and the one-reference sign depends on the slot, is reported in the companion paper.

**Consequences for reporting.**
1. $k$-reference curves should use random-$k$ subsets over all slots, never file order, unless the adjacency statistic is at the null. A one-reference sign computed from one slot of a non-exchangeable corpus is not a property of the metric.
2. A leave-one-reference-out score on single-writer data measures within-writer consistency, not human agreement; it should not be called a human ceiling.
3. Completeness estimators that treat references as independent sampling occasions (Chao2, Good–Turing) give within-writer bounds at best on such data. Paper A reports no Chao-type completeness estimate. <!-- Values withdrawn and NOT used: Chao2 0.848 "debiased ceiling" (R10 correction box; RV2), 0.7325 and LOO 0.7072 (hard-coded literals; H6 §1a(v), D17 §1(b)). -->
4. Rater-equivalence units (Resnick et al.) are defined only where references come from distinct raters.

Before a dataset's references are called "annotators" in any analysis, its adjacency statistic should be reported. The test costs seconds on CPU and needs no labels beyond the references themselves.
