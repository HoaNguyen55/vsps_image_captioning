# A1 — A principled objective for learning from multiple partial human references

Round-2 novelty research, direction A1. Date 2026-10-12. Every number below comes from existing data and existing
labels:
- KTVIC and UIT-ViIC human captions;
- COCO-2014 instance labels;
- existing KTVIC-test predictions in `data/results`;
- frozen open_clip ViT-B/32 image embeddings, computed locally on CPU.

No AI-made labels are used as evidence. Scripts and raw outputs are next to this file (section 9).

## 0. Summary

1. **Theory (a principled account of fusion).** Treat each caption as a draw from an annotator mention process with
   per-image propensity pi_o(x).
   - A target policy T has an inclusion function g_T(c), where c is the number of annotators naming o.
   - An MLE learner estimates m(o|x) = E[g_T(C)|x]. Greedy decoding roughly keeps o when m > 1/2, so each policy
     fixes an implicit threshold tau_T on pi.
   - The thresholds are 0.5 for single-caption and multi-reference SFT, 1 - 2^(-1/k) for the union of k random
     captions (0.29 at k = 2, 0.21 at k = 3), and 0.13 for the union of all 5.
   - The F1-optimal threshold for an h-annotator gold solves 1 - (1 - tau)^h = F*/2 (Lipton et al. 2014).

   This explains, with no fitted parameter, why P1 has low recall and why fusion helps. It also predicts
   **frontier invariance**: for an ideal learner, a target policy only moves the operating point. Precision at
   equal recall is a property of how well the learner estimates pi.
2. **Target-level pilot (leakage-free, 3-build / 2-held-out, both datasets): the Bayes decision is approximately
   fusion.**
   - Agreement-attested fusion collapses to the consensus caption: dF1 = -4.8 [-5.4, -4.2] on KTVIC and
     -6.9 [-7.6, -6.3] on UIT-ViIC.
   - Singletons are corroborated 46% of the time (KTVIC). That is above F*/2 ≈ 34%, so the Bayes rule keeps them.
   - A Bayes-decision dial uses a mention model cross-fitted on held-out annotators of other images. Its best
     lambda is 0.35 ≈ F*/2, as the theory predicts.
   - On the detailed row the dial beats fuse2 by only +0.6 P [+0.3, +1.0] at fuse2's recall on KTVIC and +0.3
     [+0.1, +0.6] on UIT-ViIC. No text-only feature ranks singleton mentions well: AUROC 0.57 on KTVIC, 0.65 on
     UIT-ViIC.
   - On the short row, choosing one caption by learned expected utility beats `consensual()` by +0.7 P [+0.1, +1.3]
     on KTVIC and +2.8 P [+2.1, +3.5] on UIT-ViIC, at matched recall.
3. **Precision against UIT-ViIC instance labels.** Every target keeps 99.0% instance precision, while fusion raises
   instance recall from 30.3 (P1) to 48.7 (fuse2). Fused targets lose 5.7 P against held-out annotators; that drop is
   mention-worthiness (reporting bias), not falsehood. Caveat: UIT-ViIC annotators were shown COCO category hints.
4. **Where the 12-point model-vs-human gap is.** On KTVIC test (1v4, existing predictions), P(mention | s supporting
   annotators) is human-like for s >= 1. The gap is entirely in *unsupported* mentions:

   | | unsupported mentions per caption |
   |---|---|
   | one human | 0.26 |
   | P1-short | 0.45 |
   | fuse2-short | 0.57 |

   About 75% of the excess are scene-default nouns. *đường* (road) appears 4× as often as in a human caption, and
   *quầy hàng* (stall) 2.6×. About 25% are naming variants.
5. **The headroom is at the object level.** A per-image agreement vote over 3 annotators is more precise than one
   annotator at the same recall: +7.0 P [+6.4, +7.6] on KTVIC and +3.3 [+2.6, +3.9] on UIT-ViIC. One human is
   not the ceiling. The 12-point gap is the learner's failure to estimate pi from pixels.
6. **Learner-level CPU proxy** (a linear model on frozen CLIP ViT-B/32 features, predicting what each target
   names).
   - Operating points follow the predicted tau order on both datasets.
   - On KTVIC, agreement-weighted labels that use all annotators beat a single deterministic caption at matched
     recall. Bagged consensus vs consensus: +1.4 mP [0.9, 1.8] cross-fit and +2.1 [1.1, 3.2] on test.
     Multi-reference vs consensus: +2.3 to +2.9. At one human's recall, the learner's precision rises by
     +3.3 [1.3, 4.9].
   - At the union level the gain is small: all-pairs unions vs fuse2 +0.7 [0.2, 1.2]; bagged fusion +0.4 (n.s.).
   - UIT-ViIC (6 classes, annotators shown category hints) goes the other way, -1.2 to -1.6.
7. **Ideas** (section 7):
   - (1) annotator-resampled, agreement-weighted rows (ART), whose clearest lever is the short row; about 7.4 GPU-h;
   - (2) implicit-threshold calibration, i.e. the decision-theoretic objective plus Bayes-decision selection, whose
     main test runs on the queued ladder at 0 GPU-h.

   Negatives: agreement-attested fusion, agreement-weighted token targets, and bagged fusion as a union-level
   precision lever.

## 1. Question

Greedy fusion (the consensus caption plus the caption adding the most new objects) is a heuristic. What training
target or loss makes a captioner learn the union of what annotators see while staying as precise as one human?

The measured gap is about 12 precision points at equal recall. Against the same 4 held-out annotators on KTVIC test:

| | P | R |
|---|---|---|
| one human | 85.3 | 46.9 |
| fuse2-short | 72.9 | 48.5 |

## 2. Theory: inclusion functions, implicit thresholds, Bayes decision

**Mention model.** For image x and object class o, let pi_o(x) be the probability that a random annotator names o.
Assuming conditional independence, an h-annotator panel names o with probability q_o^(h) = 1 - (1 - pi_o)^h.

This is the human-agreement model of Chen et al. 2015 (COCO Captions, arXiv 1504.00325, Sec. 4.2), with one
difference. Their model has an image-independent p per word, and they show that human (precision, recall) points then
lie on one curve. We keep image-level saliency pi_o(x).

**Bayes decision.** For calibrated q, the F1-optimal decision keeps {o : q_o >= F*/2} (Lipton, Elkan &
Narayanaswamy 2014, arXiv 1402.1892; Jansche 2007; Ye et al. ICML 2012). Our object metric mixes a micro-averaged P
with a macro-averaged R, so the rule is approximate. Empirical check:

| | best lambda of the offline dial | F*/2 |
|---|---|---|
| KTVIC | 0.35 | 0.34 (F* = 68.3) |
| UIT-ViIC | 0.35–0.425 | 0.37 |

**Inclusion functions.** Let g_T(c) be the probability that the target names o when c of the K = 5 captions do.
The MLE population optimum gives m(o|x) = E[g_T(C)|x], with C ~ Bin(K, pi_o(x)).

| policy | g_T(c) | m(o\|x) | implicit tau (m = 1/2) |
|---|---|---|---|
| P1, or multiref (every caption a row) | c/K per row | pi | 0.50 |
| union of k random captions (every k-subset a row) | 1 - C(K-c,k)/C(K,k) | 1 - (1-pi)^k | 0.29 (k = 2), 0.21 (k = 3) |
| union of all K | 1[c >= 1] | 1 - (1-pi)^K | 0.13 |
| majority of K | 1[c >= 3] | P(Bin(K,pi) >= 3) | 0.50 |

The F1-optimal tau* for an h-panel is 1 - (1 - F*/2)^(1/h). With F* ≈ 0.6 that is 0.16 for h = 2, 0.085 for h = 4,
and 0.069 for h = 5. Single-reference MLE (tau = 0.5) is far too conservative, which is P1's low recall; fusion
lowers tau.

On 5 captions, the all-k-subset unions realise per-image vote rules: k = 1 keeps c >= 3, k = 2 keeps c >= 2, and
k = 3 keeps c >= 1.

**Frontier invariance.** For an ideal learner that knows pi_o(x), every monotone policy outputs
{o : pi_o(x) > tau_T}, so all policies sit on one precision-recall frontier and the target only picks the point.

This is exact for *separable* policies (single captions, unions of random subsets), whose inclusion depends only on c,
because E[g(C)|x] is then monotone in pi by stochastic dominance. It is approximate for greedy fusion and consensus,
whose inclusion also depends on the image's other objects.

Precision at equal recall can improve in only two ways:
- a better estimate of pi: lower-variance targets, more annotators per row, or extra visual evidence. For example,
  detector tags (tags_fuse2-short) gain +2.2 P at about equal R;
- object-level selection, which caption-level targets cannot express.

Pilot C below checks this per image. Bagged and deterministic fusion of the same 4 captions lie on the same frontier:
dP at matched recall is -0.09 [-0.29, +0.12].

**Limit of the set view.** A captioner is not a set-wise thresholder. At a template slot ("đang đi trên ...") greedy
decoding fills the slot with the arg-max noun even when that noun is uncertain. That predicts where unsupported
mentions come from, and Pilot B confirms it.

## 3. Pilot A — target constructions, leakage-free offline protocol (`pilot_targets.py`)

**Protocol.** The `common` protocol of `human_parity.py offline`, with two additions: new targets built only from the
3 kept captions, and the mention models for q cross-fitted over 5 image folds. Each target is built from 3 captions
and scored against the union of the other 2, over all 10 splits. Metrics are fold-averaged object_prf P/R/F1, with
95% CIs from resampling images (B = 2000; B = 1000 for the single-caption dial) and paired deltas.
- KTVIC: 3,769 train images, 113-class lexicon.
- UIT-ViIC: the 2,687 train images with exactly 5 captions; 80 COCO classes in Vietnamese
  (`score_coco_probe.vi_classes`), plus COCO-2014 instance labels.

The baselines reproduce `data/results/policy_offline.json` exactly:

| policy | P | R | F1 |
|---|---|---|---|
| p1 | 71.8 | 52.4 | 60.6 |
| cons | 71.0 | 56.5 | 62.9 |
| fuse2 | 62.9 | 73.5 | 67.7 |
| rnd2 | 64.9 | 66.6 | 65.7 |
| unf2 | 67.8 | 57.1 | 61.9 |
| multiref | 69.5 | 51.2 | 58.9 |

### 3a. Fixed constructions (P / R / F1; dF1 vs fuse2 [95% CI])

| target | KTVIC | dF1 | UIT-ViIC | dF1 |
|---|---|---|---|---|
| p1 | 71.8 / 52.4 / 60.6 | -7.2 [-7.7,-6.6] | 76.1 / 52.6 / 62.2 | -12.4 [-13.3,-11.6] |
| cons | 71.0 / 56.5 / 62.9 | -4.9 [-5.5,-4.3] | 75.4 / 61.4 / 67.7 | -6.9 [-7.6,-6.3] |
| **fuse2** | 62.9 / 73.5 / 67.7 | — | 70.4 / 79.4 / 74.6 | — |
| all3 (= greedy fuse3) | 61.2 / 76.6 / 68.0 | +0.3 [+0.1,+0.4] | 70.1 / 80.1 / 74.7 | +0.1 [0.0,+0.2] |
| agreement-attested fusion (any / majority / all corroborated) | 71.0 / 56.6 / 62.9 | -4.8 [-5.4,-4.2] | 75.4 / 61.4 / 67.7 | -6.9 [-7.6,-6.3] |
| oracle subset (peeks at the held-out gold) | 84.3 / 76.3 / 80.1 | +12.4 | 84.8 / 80.1 / 82.4 | +7.8 |

**Why agreement-attested fusion collapses.** It adds the partner caption only when the third kept caption
corroborates the partner's new objects. That almost never happens, because objects named by 2 of the 3 kept captions
are already in the consensus caption (29,800 of 29,970 on KTVIC). The rule therefore *is* the consensus caption.

**Corroboration rates.** On KTVIC, the 2 held-out annotators corroborate an object of the build union at these rates:

| c (of 3 build captions) | rate | n |
|---|---|---|
| 1 | 0.462 | 56,307 |
| 2 | 0.670 | 29,970 |
| 3 | 0.909 | 22,847 |

Singletons sit above F*/2, so keeping them is Bayes-correct. Singleton rates do vary by class: *mũ* (hat) 0.18,
*nón* 0.16 and *túi* (bag) 0.31 sit below F*/2, while *thuyền* (boat) 0.66 and *căn phòng* (room) 0.59 sit well
above it. But a whole caption can only be kept or dropped, so this variation buys little.

### 3b. Bayes-decision dial: the subset of kept captions maximising sum_o (q_o - lambda)

q_o is the posterior predictive probability that the held-out panel names o. It comes from a model fitted on the
other 4/5 of images:

| q model | what it is |
|---|---|
| cnt | rate by agreement count |
| cls | class × count empirical Bayes |
| bb | per-class zero-truncated beta-binomial on 5-caption counts; posterior predictive for a 2-panel |
| lr | logistic regression on agreement count, class encoding, naming relation (vaguer / more specific / sibling), position, caption size, Dawid–Skene-style namer reliability (share of the namer caption's *other* objects that another annotator names), and namer length |

Singleton AUROC (c = 1 objects):

| | cnt | cls | bb | lr |
|---|---|---|---|---|
| KTVIC | 0.49 | 0.56 | 0.56 | 0.57 |
| UIT-ViIC | 0.49 | 0.56 | 0.56 | 0.65 |

KTVIC dials. "Consensus first" forces the consensus caption into the target; "any subset" does not.

| dial | best lambda | P / R / F1 at best | dP at fuse2's R | dR at fuse2's P |
|---|---|---|---|---|
| cnt | 0.00 (= all3) | 61.2 / 76.6 / 68.0 | -0.14 [-0.37,+0.08] | -0.28 [-0.78,+0.16] |
| cls | 0.35 | 62.1 / 75.7 / 68.2 | +0.23 [-0.07,+0.55] | +0.70 [-0.24,+1.39] |
| bb | 0.375 | 62.2 / 75.5 / 68.2 | +0.32 [-0.00,+0.65] | +0.61 [-0.01,+1.19] |
| lr, consensus first | 0.35 | 62.4 / 75.4 / 68.2 | +0.35 [+0.04,+0.68] | +0.90 [+0.11,+1.62] |
| lr, any subset | 0.35 | 62.7 / 75.1 / 68.3 | **+0.61 [+0.27,+0.96]** | +1.29 [+0.69,+1.81] |

UIT-ViIC, lr with any subset: best lambda 0.35, 70.6 / 79.6 / 74.8. Its dP at fuse2's R is +0.32 [+0.10,+0.56].
Instance precision at fuse2's recall is 99.17 against 98.98, a difference of +0.19 [+0.10,+0.30].

**Short row (choose ONE caption, `bo_*_single`).** dP at the baseline's recall:

| | vs `consensual()` at its R | vs P1 (file order) at its R |
|---|---|---|
| KTVIC, lr | +0.72 [+0.12,+1.32] | +2.41 [+1.53,+3.37] |
| KTVIC, cls | +0.60 [+0.04,+1.14] | +2.19 [+1.14,+3.21] |
| UIT-ViIC, lr | **+2.81 [+2.12,+3.51]** | +4.46 [+3.63,+5.33] |
| UIT-ViIC, cls | +1.90 [+1.31,+2.47] | +2.99 [+2.04,+3.82] |

**Agreement-weighted token targets**, read as expected object sets (each object kept with weight q), raise weighted
precision. For example, KTVIC soft_fuse2_lr has P 68.6 against 62.9, but its expected recall collapses to 51.6.
A decoder that imitates the string still emits a down-weighted object, so this reading is only an upper bound on
what weighting can buy. Nagasawa et al. 2021 (Weighted Caption Smoothing) already train with position-aligned,
validity-weighted soft token targets, so this direction is also not new.

**Verdict on target-level selection.** With text-only evidence, the best Bayes target is greedy fusion plus at most
0.6 P on the detailed row, and plus 0.7 P (KTVIC) to 2.8 P (UIT-ViIC) on the short row. The oracle shows large
headroom (+21 P), but that headroom lies in image content that no annotator-text feature predicts.

### 3c. UIT-ViIC: precision against COCO instance labels (presence)

| target | P_inst | R_inst | P (instance ∪ held-out refs) |
|---|---|---|---|
| p1 | 98.98 | 30.3 | 99.69 |
| cons | 99.05 | 35.7 | 99.76 |
| fuse2 | 98.98 | 48.7 | 99.58 |
| all3 | 98.95 | 49.2 | 99.56 |
| lr single-caption dial, lambda = 0 | 99.20 | 46.6 | — |

Fusion adds 18 points of instance recall at an unchanged 99% instance precision. Its 5.7-point precision drop against
held-out annotators (76.1 to 70.4) is a reference-metric artefact (mention-worthiness), not hallucination.

Caveat: the UIT-ViIC tool showed COCO category hints and the English COCO captions (Lam et al. 2020, Sec. 3.1). Human
mentions of COCO classes are therefore not independent of the instance labels, and 99% is an upper-end figure.

## 4. Pilot B — where the model-vs-human gap is (`mention_curves.py`, `unsupported.py`; existing test predictions)

KTVIC test, 1v4 folds. s is the number of the other 4 captions that name o.

| system | P(m\|s=1) | s=2 | s=3 | s=4 | unsupported (s=0) / caption | mentions / caption | P vs 4 |
|---|---|---|---|---|---|---|---|
| one human | 0.283 | 0.389 | 0.549 | 0.827 | **0.26** | 1.74 | 85.3 |
| p1-gold-short | 0.234 | 0.379 | 0.544 | 0.716 | 0.45 | 1.80 | 75.2 |
| p1_s43-short | 0.226 | 0.381 | 0.544 | 0.720 | 0.42 | 1.76 | 76.2 |
| fuse2_s42-short | 0.280 | 0.436 | 0.598 | 0.761 | 0.57 | 2.09 | 72.9 |
| tags_fuse2_s42-short | 0.279 | 0.427 | 0.591 | 0.773 | 0.51 | 2.02 | 75.0 |
| p1-gold-detailed | 0.246 | 0.392 | 0.546 | 0.713 | 0.45 | 1.83 | 75.5 |
| fuse2_s42-detailed | 0.452 | 0.609 | 0.714 | 0.825 | 1.11 | 3.15 | 64.7 |
| zeroshot-short | 0.221 | 0.325 | 0.387 | 0.487 | 1.08 | 2.17 | 50.0 |

The trained models' recall over supported objects is human-like; fuse2 is even above the human at s = 1–3. The
precision gap is the extra unsupported mentions: +0.19 per caption for P1 and +0.31 for fuse2-short.

Unsupported mentions per caption, by naming relation to the supported objects:

| | unrelated | vaguer name | more specific | sibling |
|---|---|---|---|---|
| human | 0.211 | 0.014 | 0.022 | 0.010 |
| P1 | 0.344 | 0.048 | 0.034 | 0.019 |
| fuse2-short | 0.448 | 0.043 | 0.049 | 0.027 |

Top unsupported classes, per caption:

| class | P1 | human |
|---|---|---|
| *người* (person) | 0.055 | 0.026 |
| *đường* (road) | 0.048 | 0.012 |
| *quầy hàng* (stall) | 0.044 | 0.017 |
| *phụ nữ* (woman) | 0.035 | 0.016 |
| *đàn ông* (man) | 0.033 | 0.009 |

These are scene-default and template-slot fillers ("trên đường", "bên quầy hàng"), the language-prior hallucination
of Rohrbach et al. 2018 (arXiv 1809.02156).

fuse2-short has *more* unsupported mentions than P1 (0.57 against 0.45), even though its short row is a single human
caption. That is consistent with idiosyncratic partner content from the fused detailed rows bleeding into the shared
adapter.

### 4b. Do fused training targets teach the unsupported mentions? (`bleed.py`)

The test runs per class o over 93 KTVIC classes and compares two quantities:
- x_o: the extra singleton content (named by 1 of 5 captions) that fuse2's training targets carry relative to P1's,
  per 1,000 train images;
- y_o: the extra unsupported test mentions of fuse2 relative to P1, per 1,000 test captions, on the 1v4 folds.

| comparison | Spearman (permutation p) | partial Spearman controlling for class frequency (p) | x_o normalised by class frequency |
|---|---|---|---|
| fuse2-short vs P1-short | +0.43 (0.0005) | +0.21 (0.044) | -0.02 |
| fuse2-detailed vs P1-detailed | +0.76 (0.0005) | +0.35 (0.0015) | -0.13 |

**What it shows.** The classes that fused targets add as singletons are the classes the fused model over-mentions
without support at test:

| class | extra singletons in training (per 1,000 images) | extra unsupported mentions, detailed (per 1,000 captions) |
|---|---|---|
| *người* | +69 | +76 |
| *áo* | +69 | +81 |
| *phụ nữ* | +38 | +54 |
| *đàn ông* | +34 | +32 |

The link survives controlling for class frequency, but it is carried by the absolute amount of singleton content in
frequent classes rather than by each class's singleton share. Read it as **consistent with bleed-over, not proof of
it**.

**Size of the singleton content.**
- On KTVIC, 30.5% of fuse2's target objects are singletons, against 7.6% for the consensus caption and 16.5% for P1.
- fuse2 includes 70% of all singleton objects deterministically. Bagging over 3-of-5 annotator subsets brings that to
  0.51, and over 4-of-5 subsets to 0.60. Objects named twice go from 0.95 to 0.83 / 0.91.
- On UIT-ViIC the singleton inclusion rates are 0.91 (fuse2), 0.58 (3-of-5) and 0.75 (4-of-5).

## 5. Pilot C — the "average annotator" is more precise than one annotator at equal recall (`vote_frontier.py`)

Same 3-build / 2-held-out protocol. Per-image vote rules on the 3 kept captions (keep objects with c >= m) are
compared with a single caption (the expected row):

| | KTVIC P / R / F1 | UIT-ViIC P / R / F1 |
|---|---|---|
| single caption | 69.5 / 51.2 / 58.9 | 76.1 / 53.0 / 62.5 |
| vote c >= 1 (union) | 61.2 / 76.7 / 68.0 | 70.1 / 80.1 / 74.7 |
| vote c >= 2 | 77.4 / 49.7 / 60.5 | 79.9 / 51.5 / 62.6 |
| vote c >= 3 | 91.2 / 27.2 / 41.8 | 91.3 / 27.3 / 42.1 |
| **vote frontier at the single caption's R: dP** | **+7.00 [+6.42, +7.63]** | **+3.26 [+2.61, +3.93]** |

Leave-one-annotator-out variant (`bag_offline.py`; 4 kept, gold = the 1 held-out caption) on KTVIC:

| | P | R |
|---|---|---|
| deterministic fusion of the 4 | 44.5 | 80.2 |
| single caption | 53.3 | 55.2 |
| vote >= 2 | 55.6 | 64.3 |
| vote >= 3 | 70.6 | 44.4 |

At the single caption's recall the vote frontier is about +9 P. Bagged fusion (share of the 4 fused 3-subset targets
>= t) lies *on* the deterministic-fusion frontier: dP at fusion's recall is -0.09 [-0.29, +0.12] on KTVIC and
-0.03 [-0.13, +0.07] on UIT-ViIC. Per image, re-weighting the same counts cannot move the frontier, as frontier
invariance predicts.

An estimate of pi from only 3 annotators, thresholded per image, therefore beats one human at the human's recall
(this is "precision at human recall", Chen et al. 2015, with image-level saliency). The 12-point gap is not a ceiling
problem. It is the learner failing to estimate pi from pixels. The only lever a training target has is the
signal-to-noise of the agreement information it shows the learner across images. That is what Pilot D tests.

## 6. Pilot D — proxy learner: does the target change what a learner can do? (`proxy_learner.py`)

**Why.** Pilots A–C show that a target can only move the operating point *per image*. Whether lower-variance,
multi-annotator targets give a *learner* a better frontier across images is a question about generalisation. It
cannot be answered offline without a learner, so this pilot builds a CPU stand-in.

**Setup.**
- Features: frozen open_clip ViT-B/32 (laion2b_s34b_b79k) image embeddings, computed locally on CPU and standardised.
  The planned ViT-H run on n3 was stopped after n3 crashed at 08:09 UTC, under the coordinator's resource rule.
- Learner: one multi-output logistic regression, soft-label BCE + L2, trained with L-BFGS. It predicts
  P(o in TARGET | image), which is the quantity an MLE captioner learns. Classes with >= 30 positive training images
  are kept: 56 on KTVIC, 6 on UIT-ViIC.
- Regularisation: alpha is chosen per construction on its own 20% validation split from the grid 0.01–3. Every
  choice is interior (0.03–0.3).
- Evaluation is always on images the learner never saw:
  - KTVIC test (558): 1v4 folds as in human parity, and against all 5 references;
  - KTVIC train cross-fitted (5 folds, 3,769 images) against all 5 references;
  - UIT-ViIC train cross-fitted (2,687 images) against 5 references and against COCO instances.
- Frontier summary: mP is the mean precision at R = 30/40/50/60, interpolated along a 109-point threshold sweep.
  Paired bootstrap over images, B = 1000.
- Prior-only control: the same pipeline on random features. Constructions differ there by at most 1.2 mP, so the
  "net" numbers subtract it.

**Results** (cf = cross-fitted train; "d mP" is paired against fuse2):

| construction | KTVIC cf R at t=.5 | P at t=.5 | mP | d mP vs fuse2 [95% CI] | KTVIC test 1v4 mP | learner P at the human's R (1v4) | UIT cf R at t=.5 | UIT mP | UIT d mP vs fuse2 | UIT instance mP |
|---|---|---|---|---|---|---|---|---|---|---|
| p1 | 18.1 | 82.2 | 60.8 | -3.20 [-3.92, -2.35] | 61.9 | 59.5 | 36.1 | 94.7 | -2.54 [-3.15, -2.01] | 99.2 |
| multiref (c/5, every caption a row) | 14.3 | 84.5 | 64.7 | **+0.64 [+0.10, +1.19]** | 64.8 | 62.8 | 36.0 | 95.0 | -2.20 [-2.74, -1.67] | 99.5 |
| majority (c >= 3) | 14.8 | 83.9 | 60.7 | -3.32 [-4.09, -2.49] | 62.2 | 60.8 | 33.2 | 93.1 | -4.15 [-4.92, -3.43] | 98.8 |
| bagged consensus (3-of-5) | 19.0 | 82.8 | 63.7 | -0.33 [-0.95, +0.31] | 64.3 | 63.6 | 48.7 | 94.6 | -2.66 [-3.28, -2.10] | 99.6 |
| cons | 23.3 | 77.5 | 62.3 | -1.70 [-2.37, -1.05] | 62.3 | 60.3 | 66.6 | 96.2 | -1.03 [-1.46, -0.65] | 99.7 |
| uok2 (every 2-subset union a row) | 26.6 | 78.0 | 64.7 | **+0.71 [+0.21, +1.22]** | 65.2 | 64.1 | 64.5 | 96.1 | -1.11 [-1.55, -0.68] | 99.8 |
| rnd2 | 28.8 | 73.9 | 62.7 | -1.30 [-1.90, -0.66] | 63.6 | 62.3 | 71.3 | 96.9 | -0.36 [-0.70, -0.05] | 99.7 |
| **fuse2** | 30.4 | 74.7 | 64.0 | — | 64.4 | 63.6 | 80.7 | 97.2 | — | 99.9 |
| bagged fusion (3-of-5) | 30.7 | 74.8 | 64.4 | +0.37 [-0.10, +0.82] | 65.1 | 64.2 | 73.8 | 96.8 | -0.46 [-0.76, -0.14] | 99.9 |
| uok3 | 33.5 | 72.7 | 64.3 | +0.31 [-0.15, +0.81] | 65.0 | 63.8 | 74.5 | 96.8 | -0.43 [-0.72, -0.10] | 99.9 |
| bagged fusion (4-of-5) | 34.1 | 72.5 | 64.0 | -0.02 [-0.44, +0.41] | 65.1 | 64.0 | 78.3 | 97.1 | -0.16 [-0.36, +0.04] | 99.9 |
| union of all 5 | 35.4 | 70.6 | 63.6 | -0.39 [-0.74, -0.00] | 64.5 | 63.1 | 81.3 | 97.6 | +0.33 [+0.14, +0.53] | 99.9 |

One human on the same 56 classes (1v4) scores P 85.4 / R 47.1. The linear CLIP learner reaches about 60–64 P at
that recall: a weak learner, as intended for a stand-in.

**What the proxy shows.**

1. **The implicit-threshold theory predicts the learner's operating points, on both datasets.** Recall at t = 0.5
   orders the constructions exactly as tau orders them:

   | tau ≈ 0.5 | middle | tau ≈ 0.2–0.29 | tau ≈ 0.13 |
   |---|---|---|---|
   | multiref ≈ majority ≈ p1 | bagged consensus < cons | uok2 < rnd2 < fuse2 ≈ bagged fusion (3-of-5) < uok3 ≈ bagged fusion (4-of-5) | union of all 5 |

   The best-F1 threshold of union-trained learners is about 0.28 (KTVIC) and 0.39 (UIT-ViIC), close to their F*/2.
2. **On KTVIC the frontier is set by how much annotator information a label carries.**
   - Deterministic single-caption labels lie 1.7–3.3 mP below fuse2: p1 -3.2, cons -1.7, majority -3.3.
   - Labels that use all 5 annotators with agreement weights reach or beat it: multiref +0.64 [+0.10, +1.19], uok2
     +0.71 [+0.21, +1.22], bagged consensus -0.33, bagged fusion +0.37 [-0.10, +0.82].
   - Net of the prior-only control: multiref - p1 = +3.0 mP and bagged consensus - cons = +1.4 mP. These are the
     largest effects in the pilot, and they sit at the *short-row* operating point.
   - At one human's recall on test (1v4), the learner's precision is 63.6 for bagged consensus against 60.3 for cons
     and 59.5 for P1.
3. **At the union operating point the gain is small and dataset-dependent.**
   - KTVIC: uok2 +0.71, bagged fusion +0.37 (n.s.).
   - UIT-ViIC: soft constructions are *worse* (-0.4 to -1.1). Hard union labels are best there (+0.33). UIT-ViIC
     annotators saw COCO category hints, so their union is close to instance presence, and agreement weights add
     salience noise that 6 COCO classes cannot use.
   - Against COCO instances every construction scores 99–100 mP. The learners do not differ in presence precision.
4. **Reading.**
   - Greedy fusion is close to the best *union-level* target for a learner as well (within +0.7 mP).
   - The lever that clearly moves a learner's precision at equal recall is training the *single-sentence* row on
     agreement-weighted, all-annotator labels rather than one deterministic caption.
   - Caveats: this is a linear stand-in on global CLIP features. A 7B VLM may need the variance reduction less (it
     can memorise more), or benefit more (it is far stronger at the object level). Only a GPU run decides.

**Paired short-row contrasts against the consensus caption** (`--base cons`):

| | KTVIC cross-fit d mP | KTVIC test 1v4 d mP | KTVIC test vs 5 d mP | learner P at the human's R (1v4), d vs cons | UIT-ViIC cross-fit, refs / instances |
|---|---|---|---|---|---|
| bagged consensus - cons | **+1.36 [+0.94, +1.83]** | **+2.06 [+1.09, +3.20]** | +2.15 [+1.07, +3.32] | **+3.27 [+1.31, +4.86]** | -1.64 [-2.02, -1.25] / -0.08 [-0.17, 0.00] |
| multiref - cons | +2.34 [+1.82, +2.85] | +2.56 [+1.45, +3.95] | +2.93 [+1.62, +4.19] | +2.49 [+0.35, +4.90] | -1.17 [-1.51, -0.80] / -0.19 [-0.31, -0.10] |
| p1 - cons | -1.50 [-2.24, -0.77] | -0.40 [-2.00, +1.41] | -0.37 [-2.06, +1.43] | -0.78 [-3.66, +1.32] | -1.51 [-1.90, -1.14] / -0.47 [-0.63, -0.32] |

The prior-only control gives bagged consensus - cons ≈ 0.0 and multiref - cons ≈ +0.1–0.2, so the KTVIC gains are
learned, not class-prior artefacts.

The sign flips on UIT-ViIC: 6 near-ceiling classes, annotators shown COCO hints, with mention close to presence. KTVIC
(56 classes, free daily-life descriptions) is the representative case, but the effect is not universal.

## 7. Ideas (at most two), each with pilot numbers, cost and kill criterion

### Idea 1 — Annotator-resampled, agreement-weighted training rows (ART)

**Mechanism.** Every epoch, draw a fresh 3-of-5 annotator subset S per image. Build the short row as
`consensual(S)` and the detailed row as `fused(S, 2)`. In expectation the learner then sees each human caption, and
each union, with agreement-proportional weight:
- the conditional expectation of the selection rule given all 5 captions (a Rao–Blackwellised target);
- singleton inclusion drops from 0.70 to 0.51 while objects named by two or more annotators stay at 0.83–1.0.

The subset size s is a principled operating-point dial (s = 5 recovers fuse2), with tau_s from section 2.

**Closest prior and delta.**
- Nagasawa et al. 2021 (VBCS) samples ONE reference per epoch, weighted by n-gram validity, and is the closest prior.
  ART's short row is an object-agreement variant of it.
- Zheng et al. 2018 ("Sample One", "Shuffle") and soft crowd labels (Peterson 2019; Uma 2020) are classification or
  single-reference analogues.
- New in ART: union-level rows recomputed per annotator subset; the derivation of the operating point from s; and
  evaluation by precision at human recall against held-out annotators and against COCO instances.
- Novelty is incremental for the short row and moderate for resampled unions.

**Pilot evidence.**
- Per image (an ideal learner) there is no frontier change: -0.09 [-0.29, +0.12]. That is the theory's prediction,
  and it means the gain can only come from generalisation.
- CPU proxy learner on KTVIC:

  | row | contrast | d mP (cross-fit) | d mP (test 1v4) | d P at one human's recall |
  |---|---|---|---|---|
  | short | bagged consensus vs cons | +1.36 [+0.94, +1.83] | +2.06 [+1.09, +3.20] | +3.27 [+1.31, +4.86] |
  | detailed | bagged fusion vs fuse2 | +0.37 [-0.10, +0.82] | +0.67 [-0.36, +1.89] | — |
  | detailed | uok2 (all pair-unions) vs fuse2 | +0.71 [+0.21, +1.22] | — | — |

- UIT-ViIC proxy: the short row is -1.64 and the detailed row -0.46 (both CIs exclude 0); instance precision is
  unchanged.
- Mechanism support: the classes that fuse2's training targets add as singletons are the classes fuse2 over-mentions
  without support at test (partial Spearman +0.21 / +0.35 controlling for frequency).

**GPU.**
- Implementation: add a `--bag-subsets 3` option to `build_gold_sft.py`. It materialises 2 epoch-draws per image
  (rows and steps identical to fuse2) into `sft.jsonl`, then `train_stage2 --epochs 1`.
- KTVIC: about 3.6 GPU-h of SFT plus 0.7 of eval. UIT-ViIC in-domain: about 2.6 plus 0.5. Total about 7.4 GPU-h.
- Optional isolation run (short row bagged, fuse2 detailed rows kept): +4.3 GPU-h.

**Kill criterion (pre-registered).** ART's short mode should land between P1-short and fuse2-short in recall,
because bagged consensus has a higher implicit threshold. So it is compared with the frontier, not with a single point:
on KTVIC test (1v4 parity), its precision must lie at least +1.5 above the line through P1-short (s42/s43/s44) and
fuse2-short (s42/s43/s44), at its own recall, with a paired CI excluding 0.

Kill if that fails, *or* if unsupported mentions per caption do not fall below 0.52 (fuse2-short: 0.57). Also kill if
UIT-ViIC in-domain instance precision drops by more than 1 point.

**Confidence.** Low to moderate. The proxy is a linear stand-in, the UIT-ViIC sign is negative, and a 7B QLoRA model
trained for 2 epochs may memorise per-image targets regardless.

### Idea 2 — Implicit-threshold calibration: a decision-theoretic multi-reference objective, tested for free on the queued ladder

**Mechanism.** The analytic inclusion function of each target policy gives its implicit threshold tau_T on the
annotator mention propensity. The evaluation gold of h annotators fixes the F1-optimal tau* = 1 - (1 - F*/2)^(1/h).
Two consequences:
- The target family is chosen by matching tau_T to tau*, e.g. unions of k resampled captions with
  k* = argmin_k |1 - 2^(-1/k) - tau*|, instead of a hand-picked fusion rule.
- Where a deterministic choice is needed, the Bayes-decision rule picks the human-caption subset maximising
  sum_o (q_o - F*/2), with q_o from a mention model cross-fitted on held-out annotators of other images.

Consensus selection (h = 1) and greedy fusion (q uniform) are special cases.

**Closest prior and delta.**
- Chen et al. 2015 (COCO Captions, Sec. 4.2): an independent-annotator mention model and Precision at Human Recall,
  but with image-independent p and no link to training targets.
- Lipton et al. 2014: the F*/2 threshold.
- MBR fine-tuning (Finkelstein et al. 2024) distils a decision rule over *model samples*.
- Delta: the inclusion-function / implicit-threshold account of *training targets*, its frontier-invariance
  corollary, and cross-fitted Bayes selection over unions of *human* captions. No prior work was found in 14 searches.

**Pilot evidence.**

| check | result |
|---|---|
| best lambda of the offline Bayes dial vs F*/2 | 0.35 vs 0.34 (KTVIC); 0.35–0.425 vs 0.37 (UIT-ViIC) |
| learner operating points follow tau_T | yes, on both datasets (section 6) |
| agreement-gated fusion (predicted Bayes-suboptimal) | -4.8 / -6.9 F1 |
| Bayes selection, detailed row, dP at fuse2's R | +0.61 [+0.27, +0.96] KTVIC; +0.32 [+0.10, +0.56] UIT-ViIC |
| Bayes selection, short row, dP at consensus's R | +0.72 [+0.12, +1.32] KTVIC; +2.81 [+2.12, +3.51] UIT-ViIC (unchanged without the reliability features) |

Combined with the oracle's +21 P, this shows that greedy fusion is within about 0.6 P of the best caption-level
target that text can identify.

**GPU.** 0 for the theory test, which runs on the queued ladder (section 7a). An optional Bayes-decision short-row
run costs about 4.3 GPU-h on KTVIC plus 3.1 on UIT-ViIC.

**Kill criterion.** Kill the theory claim if, on the trained ladder, the observed recall order disagrees with the
tau order {p1, multiref} <= {cons, unf2} < rnd2 < fuse2 (Kendall tau-b < 0.6, ties as stated), or if multiref's
recall exceeds cons's. Kill the Bayes short row if the trained short mode does not beat the cons model
at matched recall by at least +1 P (KTVIC) or +2 P (UIT-ViIC).

**Confidence.** High that the theory and its operating-point predictions hold (they already do in two proxy learners
and the offline dials). Low that the Bayes selection rule alone yields a visible gain on KTVIC.

### What did not survive

- **Agreement-attested fusion** (both datasets). It collapses to the consensus caption.
- **Agreement-weighted token targets.** The expected-set reading caps recall, and Nagasawa 2021 WCS is prior art.
- **Bagged fusion as a union-level precision lever.** It is per-image frontier-neutral, adds at most +0.4–0.7 mP in
  the KTVIC proxy, and is negative on UIT-ViIC.
- **Learned mention models as a route to object-level selection.** Singleton AUROC is only 0.57–0.65, against oracle
  headroom of +21 P. Text cannot identify which singleton mentions are mention-worthy.

### 7a. Zero-GPU, pre-registered predictions for the queued target-policy ladder

These follow from the implicit-threshold theory (section 2). They can be checked as soon as the ladder's predictions
land; `human_parity.py rank` already has the plumbing.

1. **Operating points follow the implicit threshold.** Recall on test (vs the 5 references) should rank
   {p1, multiref} <= {cons, unf2} < rnd2 < fuse2. P1 and multiref share tau = 0.5, but in the proxy multiref sits
   about 4 recall points lower: lower-variance soft labels push fewer objects over 1/2. So expect
   multiref <= p1 in recall.
2. **The variance channel.** At equal recall, multiref (5 captions per image) should be more precise than P1
   (1 caption per image). The test is P at P1's recall, interpolated between multiref and the cons/unf2 points.
   - Positive: the learner benefits from more annotators per image, which is the mechanism behind RB-Fuse.
   - Null: RB-Fuse's premise is weakened.
3. **Bleed-over.** cons_s42 (consensus rows only) should have fewer unsupported mentions per caption than
   fuse2_s42-short (0.57). If so, the fused detailed rows are what teach the shared adapter to name low-agreement
   scene objects. `mention_curves.py` and `unsupported.py` run unchanged on any `*-short.preds.json`.

## 8. Literature (read this session unless marked) and scoop check

Full texts read this session:
- CCCaption (arXiv 2602.21655, CVPR 2026)
- Chen et al. 2405.00485 (Findings EMNLP 2025)
- Zheng, Ma & Huang 2018 (arXiv 1808.09564, EMNLP 2018)
- Nagasawa, Watanabe & Iyatomi 2021 (ACL Anthology 2021.maiworkshop-1.6)
- Chen et al. 2015, COCO Captions (arXiv 1504.00325), Sec. 4.2
- KTVIC (arXiv 2401.08100)
- UIT-ViIC (arXiv 2002.00175)
- ViCLIP-OT (arXiv 2602.22678)

Abstract only:
- Lipton et al. 2014 (arXiv 1402.1892)
- Rodrigues & Pereira 2018 (arXiv 1709.01779)
- Phan et al. 2017, CST (arXiv 1712.09532)
- Peterson et al. 2019 (arXiv 1908.07086)
- Finkelstein et al. 2024 (arXiv 2309.10966)

Verified in round 1 (`wf/verify_*.json`), not re-read:
- Misra 2016 (arXiv 1512.06974)
- Rohrbach 2018, CHAIR (arXiv 1809.02156)
- IC3 (arXiv 2302.01328)
- Atomic Self-Consistency (arXiv 2405.13131)
- Fang 2015 (arXiv 1411.4952)
- KnowAda (arXiv 2411.09018)
- Less-is-More (arXiv 2402.14545)
- Cole 2021 (arXiv 2106.09708)
- Berg 2012 (CVPR)
- Link 2003 (Biometrics)

### 8a. Closest prior work, mechanism, and the delta that remains

**Multi-reference training**

- **Zheng, Ma & Huang, EMNLP 2018 (arXiv 1808.09564).**
  - Mechanism: compares ways to train on K references. "Sample One" picks a random reference each epoch.
    "Uniform" makes every reference its own pair. "Shuffle" is Uniform reshuffled every epoch. It then adds
    pseudo-references by traversing lattices of the references.
  - Numbers (COCO test CIDEr): First 80.7, Sample One 85.4, Shuffle 94.1, plus pseudo-references 97.1.
  - Delta: every target is a single reference or a path through the lattice. No unions, no coverage objective, and
    no precision analysis.
- **Nagasawa, Watanabe & Iyatomi, MAI 2021.**
  - Mechanism: VBCS samples one reference per epoch, with probability set by a softmax over its similarity to the
    other references. WCS builds soft token targets from the words at the same position in several references,
    weighted by validity.
  - Numbers: COCO CIDEr 111.7 to 114.3.
  - Delta: pre-empts consensus selection and agreement-weighted token targets. It has no union-level target, no
    held-out-annotator evaluation, and no annotator-subset resampling of a union construction.
- **Phan et al. 2017, CST (arXiv 1712.09532).**
  - Mechanism: RL with ground-truth captions as the samples, which is equivalent to weighted cross-entropy, with
    reference consensus as the baseline.
  - Numbers: MSR-VTT CIDEr 47.3 to 54.2.
  - Delta: sentence-level agreement weights. No unions.
- **Finkelstein et al. 2024 (arXiv 2309.10966).** MBR and QE fine-tuning: distil a decision rule over *model
  samples* into training targets. This is prior art for "train on the Bayes decision". Our hypotheses are unions of
  *human* captions, and our posterior predictive comes from a cross-fitted mention model.
- **Chen et al., Findings EMNLP 2025 (arXiv 2405.00485).** PoCa merges an LVLM's patch captions with an LLM.
  Concatenated COCO captions appear only as a VQA baseline; nothing is trained on fused targets, and precision is
  not measured.
- **CCCaption, CVPR 2026 (arXiv 2602.21655).** Treats references as incomplete. It replaces them with completeness
  and correctness rewards from MLLM-generated queries and judges (GRPO on Qwen3-VL-2B). There is no multi-reference
  or annotator modelling, and none of CHAIR, CIDEr or human-recall comparisons.
- **IC3 (arXiv 2302.01328) and Atomic Self-Consistency (arXiv 2405.13131).** Union-style aggregation of samples at
  inference. The repo's object-consensus MBR ablation is the in-house version.

**Learning from crowds and soft labels**

- **Dawid–Skene 1979 and Raykar et al., JMLR 2010.** EM over annotator confusion matrices.
  - Rodrigues & Pereira, AAAI 2018 (arXiv 1709.01779): a crowd layer, for classification, regression and sequence
    labelling.
  - Nguyen et al., ACL 2017; Rodrigues et al. 2014; Lu 2023 (arXiv 2301.01579): crowd sequence labelling.
  - Search found no learning-from-crowds method for *generation* or captioning.
  - Our model is class-level rather than annotator-level, because KTVIC's 5 captions per image come from 3
    annotators plus 2 revising reviewers, with no IDs.
- **Peterson et al., ICCV 2019 (arXiv 1908.07086); Uma et al., HCOMP 2020 and JAIR 2021.** Soft labels from crowd
  distributions improve generalisation and robustness. This is classification only, and it is the analogue of
  RB-Fuse's mechanism. Using it for union-level caption targets is the delta.
- **Perspectivist NLP survey (LRE 2024; doi 10.1007/s10579-024-09766-4).** Lists perspectivist NLG as an open topic.
  No captioning or summarisation training method was found.

**Human agreement, mention-worthiness and decision theory**

- **Chen et al. 2015, COCO Captions (arXiv 1504.00325), Sec. 4.2.**
  - Mechanism: an independent-annotator mention model P(w|o) = p with no image-level saliency. Human recall equals p
    and human precision is kp/(kp + (1-p)^k). Human points lie on one curve.
  - It proposes **Precision at Human Recall (PHR)**.
  - Our "human parity" is PHR at the object level and must cite it. Our vote frontier adds image-level saliency and
    shows the aggregate beating a single human at human recall.
- **Fang et al., CVPR 2015 (arXiv 1411.4952).** MIL word detectors trained on words in *any* caption (union labels)
  and evaluated by PHR.
- **Berg et al., CVPR 2012.** Importance = P(mentioned | present), predicted from the image.
- **Misra et al., CVPR 2016.** Presence × relevance factorisation of reporting bias.
- **Link 2003.** The zero count is not identifiable under heterogeneous detection. The beta-binomial fit here is
  zero-truncated and only ever used for objects someone named.
- **Lipton, Elkan & Narayanaswamy 2014 (arXiv 1402.1892).** The F1-optimal threshold is F*/2 for calibrated scores.
  Also Jansche 2007; Ye et al., ICML 2012; Dembczynski et al., NIPS 2011 (GFM). The repo's E4/GFM decision rules were
  null.
- **Rohrbach et al. 2018, CHAIR (arXiv 1809.02156).** Language-prior object hallucination, the mechanism behind the
  scene-default unsupported mentions in Pilot B.

**Target-curation and hallucination**

- **KnowAda (arXiv 2411.09018).** Removes caption details that the VLM cannot perceive.
- **Less is More (arXiv 2402.14545).** Over-detailed targets push the EOS decision past what the model perceives.
- **CapsFusion (2310.20550), FuseCap (2305.17718), Bianco/Celona (2306.11593).** LLM fusion of model captions or
  expert outputs; precision is not controlled by annotator agreement.

**Dataset facts that change claims**

- **KTVIC (arXiv 2401.08100).** Three participants annotate, then two researchers "review and revise five captions"
  per image. Inter-annotator agreement is not reported. Do not call the 5 captions 5 independent annotators: the
  "3-build / 2-held-out" protocol holds out *captions*, not people.
- **UIT-ViIC (arXiv 2002.00175).** Five writers. The tool showed COCO category hints and, on demand, the original
  English captions. Instance-label precision of human mentions is therefore inflated, and human mentions are not
  independent of COCO.
- **ViCLIP-OT (arXiv 2602.22678).** 2,464 of 3,769 KTVIC train images and 401 of 558 KTVIC test images are SSCD
  near-duplicates of UIT-OpenViIC train images, which carry about 4.7 captions each.
  - That is a potential *independent-team* held-out gold for KTVIC targets, from an existing dataset. It needs access
    to OpenViIC and an SSCD match, so it is not done here.
  - It also contaminates any model trained on OpenViIC.

### 8b. Scoop searches (14 queries; WebSearch, plus the round-1 verified list)

1. "learning from crowds image captioning multiple annotators latent truth caption generation" (budget exhausted;
   re-run below)
2. "image captioning training target union of multiple reference captions resampled annotator subsets soft labels
   agreement". Closest hits: Nagasawa 2021; Harzig et al. 2019 (arXiv 1905.01919, soft targets for ratings);
   TCTS (arXiv 2009.14405, teacher soft labels).
3. "bootstrap resampling annotators training targets text generation multiple references bagging". Nothing relevant.
4. "vision language model fine-tuning concatenated human captions COCO five captions merged target object
   hallucination recall". KnowAda, ESREAL; no merged-human-caption SFT.
5. "learning from crowds sequence-to-sequence text generation multiple annotators latent ground truth 2023 2024".
   Only crowd sequence *labelling* (LA-SCA 2301.01579, Nguyen 2017, Rodrigues 2014/2018); CrowdWSA2019 (word-sequence
   aggregation).
6. "perspectivist natural language generation training on multiple human references disagreement summarization
   captioning". Survey and workshop CFP only.
7. "expected F1 Bayes decision object mentions image captioning minimum Bayes risk object set". AMBR (2401.02749,
   unigram-F1 utility for MBR on COCO), DCC (1511.05284), COCO Captions 2015 (expected TP/FP model).
8. "Fang et al. 2015 precision at human recall". Fang 2015 / PHR.
9. "'precision at human recall' captioning object mentions vision-language model 2024 OR 2025". No modern use of PHR
   found; 2411.17491 (LLM-judged object mention P/R).
10. "soft label smoothing from multiple reference captions agreement weighted cross-entropy image captioning
    2023-2025". Nagasawa 2021 only.
11. "KTVIC UIT-ViIC Vietnamese image captioning multiple references fusion training large vision language model".
    Nothing beyond the dataset papers and ViCLIP-OT.
12. "dense caption training data from multiple human captions per image agreement filter hallucination precision
    coverage tradeoff SFT". KnowAda, CapMAS (2412.15484), PerturboLLaVA HalFscore; no agreement-based human fusion.
13. "set-valued supervision union of reference captions multi-label objective caption generation coverage multiple
    references training objective comparison". Zheng 2018, Nagasawa 2021, RefCaptioner (2607.28509, video,
    coverage reward).
14. "Rao-Blackwellized training targets label noise expected label given all annotators lower variance soft targets
    crowdsourcing". Soft-label crowd papers (HCOMP 2020); no Rao–Blackwellised generation targets.

**Verdicts**

| claim | status | closest prior work |
|---|---|---|
| Consensus selection | SCOOPED | Nagasawa 2021; Devlin 2015 |
| Agreement-weighted token targets | SCOOPED | Nagasawa 2021 WCS; CST |
| Decision-theoretic account of multi-reference targets (implicit thresholds, F*/2, frontier invariance) | OPEN as a framing | built from Chen 2015 + Lipton 2014 |
| Union targets resampled over annotator subsets (RB-Fuse) | OPEN | soft-label crowds (classification), Zheng's Sample One (single references) |
| PHR with image-level saliency (vote frontier beats one human) | OPEN | Chen 2015 used image-independent p |

## 9. Files (all under research_r2/A1/)

| file | what it does |
|---|---|
| `explore.py` | corroboration by agreement count, naming relation and class (KTVIC train) |
| `pilot_targets.py` | Pilot A: all target constructions, Bayes-decision dials (cnt/cls/bb/lr; consensus-first, free, single caption), soft targets, oracle, UIT instance precision. Outputs `out/ktvic.json`, `out/uitviic.json` (B = 2000) and `out/ktvic_v2.json`, `out/uitviic_v2.json` (single-caption dials, B = 1000), with logs |
| `vote_frontier.py` | Pilot C: `out/vote_ktvic.json`, `out/vote_uit.json` |
| `bag_offline.py` | Pilot C, leave-one-annotator-out bagging check: `out/bag_offline_*.log` |
| `mention_curves.py`, `unsupported.py` | Pilot B: `out/mention_curves.json`, `out/unsupported.json` |
| `bleed.py` | section 4b, class-level bleed-over test |
| `make_labels.py` | Pilot D: target labels for every construction, `out/labels.json` |
| `proxy_learner.py` | Pilot D: the proxy learner (`--base`, `--only`) |
| `clip_embed_local.py` | Pilot D: local ViT-B/32 embeddings in `emb_b32_ktvic/`, `emb_b32_uit/`, using an isolated `venv/` (torch 2.5.1 CPU, open_clip 2.29). The weights are in `hf_cache/`; re-run with `HF_HOME=research_r2/A1/hf_cache` |
| `summarize_proxy.py` | Pilot D: summary tables |
| proxy outputs | `out/ktvic_proxy_b32.json`, `out/uit_proxy_b32.json`, `out/*_vscons.json`, and the prior-only control `out/prior_control_proxy.json` |
| `clip_embed_uit.py`, `chain_n3.sh` | the stopped n3 ViT-H attempt, kept for the record. n3 rebooted at 08:09 UTC; under the coordinator's rule, nothing of A1 runs there now. `/root/r2/A1` on n3 holds only small files |
| `pilot_targets.py` with `A1_NO_RELIABILITY=1` | the reliability-feature ablation: `out/ktvic_noreliab.json`, `out/uit_noreliab.json` |
