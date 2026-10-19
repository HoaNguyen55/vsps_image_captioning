# A-N1 design note: object metrics under incomplete gold, ported from IR

Written 2026-10-19 (UTC) by task agent A-N1, before any stage-1 computation. Every symbol below is computed by
`measures.py` (in this folder) from the per-image mention sets and gold sets of `scripts/g2b/score_g2b.py`, which it
imports unchanged.

## 1. The correspondence

| IR (ad hoc retrieval) | Object hallucination metric |
|---|---|
| topic (query) | image i |
| retrieved set of a run | mention set m_xi of system x (`score_g2b.mentions`, registered matcher and lexicon) |
| judged relevant document | a class in the gold positives G_i^g of gold level g |
| judged non-relevant document | a class in the verified negatives N_i |
| unjudged document | a mentioned class in neither G_i^g nor N_i |
| trec_eval convention (unjudged = non-relevant) | raw object precision \|m ∩ G\| / \|m\| |

Gold sources, as registered in `manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.json` (`golds`):
- k = 1..K human references give positives only. A class that no reference names is unjudged. It is not a negative.
- COCO-80 instance annotations are exhaustive over the 80 classes of the coco80 lexicon. Present classes are positives;
  the other classes of the 80, U80 \ inst_i, are verified negatives.
- On XM3600, the Open Images V7 human-verified image-level labels give verified positives (status `present`) and verified
  negatives (status `absent`) on the mapped lexicon classes (`xm3600_oiv7.statuses`). Mentions of other classes are unjudged.

## 2. Definitions

Gold levels L = (one_ref, all_refs, complete), read from `golds.<set>.{one_ref, all_refs, complete}` of the prereg:
refs1_randk (S = n_random_subsets random draws), refs_all, and inst or oiv7_verified. G_is^g is the positive set of image i
in draw s at level g. N_i is the verified-negative set of the complete gold: U80 \ inst_i for coco80, the `absent` classes
for OIV7. **N_i is the same at every level**: it is the negative judgment the evaluator holds, whatever the positives.

**Judged pool.** J_is^g = G_is^g ∪ (N_i \ G_is^g). If a reference names a class that the complete gold marks absent, the
class counts as a positive at that level (D6). The unjudged mentions are m_xi \ J_is^g.

All measures keep the registered aggregation (`score_g2b.scores`, `check_mstar.prf`): precision is micro over images,
recall is macro over the images with non-empty positives, w are the image weights (1 for the point estimate, a bootstrap
draw for a replicate), and each value is computed per draw s and then averaged over s. M_x = Σ_i w_i |m_xi| / Σ_i w_i.

- **F1 (baseline).** The registered mixed F1: P = Σ w |m∩G| / Σ w |m|; R = Σ_{G≠∅} w |m∩G|/|G| / Σ_{G≠∅} w;
  F = 2PR/(P+R). At oiv7_verified it is the registered OIV7 F1_pos.
- **cF1 (condensed F1; Sakai 2007).** Unjudged mentions are removed before precision is computed:
  P^c = Σ w |m∩G| / Σ w |m∩J|. Recall is unchanged, because an unjudged mention is in neither the numerator nor the
  denominator of recall: R^c = R. F^c = 2 P^c R / (P^c + R).
- **bpref_set (Buckley and Voorhees 2004, in the trec_eval form with min(R, N)).** For one image with R_i = |G_i|,
  N'_i = |N_i \ G_i|, TP = |m ∩ G_i| and FP = |m ∩ (N_i \ G_i)|:
  bpref_i = (TP / R_i) · (1 − E[min(K, R_i)] / min(R_i, N'_i)).
  A caption names a set, not a ranking, so the mentioned classes are taken in a uniformly random order. K is the number
  of mentioned negatives ranked above a given mentioned positive, and is uniform on {0, …, FP}. Hence
  E[min(K, R)] = FP/2 if FP ≤ R, and (R(R+1)/2 + (FP − R)R) / (FP + 1) otherwise. Unmentioned positives score 0, as
  unretrieved relevant documents do in bpref. The 2004 paper normalises by R; trec_eval uses min(R, N), as here. The two
  coincide when N'_i ≥ R_i. bpref is macro over the images with R_i > 0.
- **infAP-style (Yilmaz and Aslam 2006).** infAP treats the judged documents as a uniform random sample of the depth-k pool.
  It estimates the precision among pooled documents above rank k as (rel + ε)/(rel + nonrel + 2ε), and counts documents
  outside the pool as non-relevant. For sets, take the pool to be the union of the compared systems' mentions, so every
  mention is pooled. The infAP precision estimate is then condensed precision with ε-smoothing, and it equals P^c as
  ε → 0. A second reading takes a random fraction q of the images as fully judged and the rest as reference-only, and
  corrects the rest with ratio estimators from the judged images. That is a two-phase sampling design: its estimate is
  approximately unbiased by design, so the slope spread shrinks in expectation whatever the captions do. It would test
  the variance at a chosen q, which is a protocol question. Neither reading is a separate stage-1 candidate.

**Verbosity slope and spread.** slope_μ[g] is the OLS slope of 100·μ_x on ln M_x over the systems of the family
(`score_g2b.stat_slope`). The spread of measure μ across gold levels is the range
Range_μ = max_{g∈L} slope_μ[g] − min_{g∈L} slope_μ[g], and its ratio to F1 is ρ_μ = Range_μ / Range_F1. All quantities
are computed on the same bootstrap draw, so they are paired.

## 3. Degenerate cases

- **D1. References alone, with no verified negatives (N_i = ∅ for every image).** J = G, so P^c = 1 wherever a judged
  class is mentioned. cF1 becomes 2R/(1+R), a function of recall alone. bpref has min(R, N) = 0, so the trec_eval
  convention gives a penalty of 0 and bpref = recall. Both measures then ignore hallucination. Their slope on ln M is then that of
  a recall, which rewards every added mention and penalises none, so a spread could shrink for that reason alone. **Rule:**
  neither measure is applied to a gold level without verified negatives. Every A-N1 level carries N_i from the complete
  gold. IR's incomplete-judgment measures therefore cannot repair positives-only gold. They apply only where some
  negatives are judged.
- **D2. One image without verified negatives** (an XM3600 image with no `absent` label). Its judged mentions are all
  positives. The image is kept, as it is in the registered OIV7 precision, and the number of such images is reported.
- **D3. Complete gold over a closed lexicon (coco80).** Here J = U80 ⊇ m, nothing is unjudged, and cF1 = F1 exactly. At
  oiv7_verified the registered precision is already condensed, Σ|m∩present| / Σ|m∩(present ∪ absent)|, so cF1 is defined
  as the registered F1 there. The complete level is therefore identical under F1 and cF1. Only the reference levels move.
  On coco80, `measures.py stage1` checks this identity in code.
- **D4.** If Σ w |m∩J| = 0, then P^c = 0 (the registered convention for P when there are no mentions), and so F^c = 0.
- **D5.** An image with R_i = 0 at a level is excluded from recall and bpref at that level (the registered `has`).
- **D6.** Conflicts G ∩ N ≠ ∅ are counted as image–class pairs at all_refs and reported. The positive wins.
- **D7.** UIT-ViIC's secondary lexicon (objects_in) has no defined universe of verified negatives, so the measures are
  not applied to it. Only the primary lexicon is analysed: coco80 on COCO and UIT-ViIC, objects_in with OIV7 on XM3600.
- **D8.** A system with M_x = 0, or a family with fewer than two distinct M_x, gives an undefined slope. The prereg rule
  then makes the statistic NOT_EVALUABLE.

## 4. Prediction

Under each of cF1 and bpref_set, the range of the verbosity slope across the three gold levels is smaller than under F1:
Range_μ < Range_F1, that is, ρ_μ < 1.

The mechanism, as expected from the definitions before any data: raw coco80 precision at a reference level with
G^g ⊆ inst is P_c · (|m∩G^g| / |m∩inst|). Its second factor is the share of the system's correct mentions that the references cover, and
it falls as captions add less salient objects. Condensing removes that factor. What it leaves is
P^c = |m∩G^g| / (|m∩G^g| + FP), which still depends on the level through |m∩G^g|. Recall is unchanged. So cF1 is expected
to shrink the range but not to remove it. bpref_set charges each verified false positive in proportion to 1/R_i. R_i is
smallest at one_ref, so bpref may keep a large range. This is a reason it may fail; it is not a prediction.

The choice of the primary measure and statistic is made by the rule in `STAGE1_PLAN.md`, on stage-1 data. It is frozen in
the addendum before any G2-B output is touched (judge PD-16, item 3(a)).

## 5. References (DOIs checked against Crossref on 2026-10-19)

- Buckley, C., and Voorhees, E. M. (2004). Retrieval evaluation with incomplete information. *Proceedings of the 27th
  Annual International ACM SIGIR Conference on Research and Development in Information Retrieval*, 25–32.
  https://doi.org/10.1145/1008992.1009000
- Sakai, T. (2007). Alternatives to bpref. *Proceedings of the 30th Annual International ACM SIGIR Conference on Research
  and Development in Information Retrieval*, 71–78. https://doi.org/10.1145/1277741.1277756
- Yilmaz, E., and Aslam, J. A. (2006). Estimating average precision with incomplete and imperfect judgments.
  *Proceedings of the 15th ACM International Conference on Information and Knowledge Management (CIKM '06)*, from p. 102
  (Crossref gives the first page only). https://doi.org/10.1145/1183614.1183633
