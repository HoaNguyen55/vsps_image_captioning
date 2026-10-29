## 8. English comparison: COCO Karpathy test and NoCaps val

This section reports the English arm. It is a separate registration that carries the Vietnamese design over to English with no English tuning. Every number comes from its two decision files and its run logs. English results are reported within English only. No cross-language difference is computed, and no Vietnamese claim of Sections 6 and 7 changes in their light.

### 8.1 Registration

**What was carried over.** The English registration fixed every design choice from the Vietnamese one: the frozen configurations of Table 2 (k, order, τ, the two backbones and their pinned snapshots), greedy decoding with 60 new tokens, the retrieval near cut and near-duplicate rule of Section 3.1, the seeded `rand` draw, and the deletion step with its zero-shot fallback. The prompt header, example line and tails are direct English translations, pinned by hash. Only `ret`, `rand` and `zs` were decoded per backbone. There was no `fix` arm, no English development set and no English tuning of any kind.

**Scorer.** The English decision column is PTB-tokenised CIDEr-D (×100) from pycocoevalcap 1.2 [@Chen2015COCOCaptions], with document frequencies over each scored set's own references. The Vietnamese decision column (Section 3.6) is stripped CIDEr-D on word-segmented text (RDRSegmenter word tokens). The two columns are not on one scale, which is one reason no cross-language difference is computed.

**Registered rules.** Both sets use the Vietnamese P1 rule: PASS if the pooled `ret` − `rand` point is above the SESOI of +2.0 **and** the 95% CI lower bound is above zero. Each set is decoded once, scored once and decided once. Applying this one rule to NoCaps as well was fixed after the Vietnamese XM-a result was known. It is stricter than the XM-a rule, which asked only for a CI lower bound above zero (Table 4), so the two out-of-source results answer different rules. The SESOI of +2.0 was carried over numerically and was not recalibrated for the PTB-tokenised English scale; because English scores are higher, it is relatively more lenient on COCO (Section 5.4).

**Table 10. Registered English predictions.**

| name | set | estimand | rule |
|---|---|---|---|
| **P1-EN** (primary) | COCO Karpathy test, full 5,000 [@Lin2014COCO; @Karpathy2015Split] | mean pooled Δ_i (PTB CIDEr-D) | point > +2.0 and CI lower bound > 0; length rule L as in Table 4 |
| **S-NC** (secondary, fixed order) | NoCaps val, full 4,500 [@Agrawal2019NoCaps] | mean pooled Δ_i | the same rule |
| sensitivity | NoCaps val without the 1,000 images decoded earlier (3,500) | the same | reported beside S-NC, never replacing it |

The claim "the gain transfers to NoCaps val" needed both P1-EN and S-NC to pass. The NoCaps block was decoded and decided whatever P1-EN showed. Per-backbone rows, `ret` − `zs` and `rand` − `zs`, and the per-domain NoCaps rows are reported without a rule. As in Table 9, InternVL3's `ret` − `rand` at τ = −∞ is a registered secondary, labelled "detected" only when its CI lower bound is above zero, and no gate reads it.

**References and memory.** COCO uses the first 5 references of each image in Karpathy order; NoCaps uses all released references. The memory is COCO Karpathy train and restval after removing ids reserved for companion studies, byte copies and near-duplicates of the English evaluation sets: 112,255 images in 111,927 clusters (counts at each step in the supplement). The memory is therefore in the COCO domain by construction. NoCaps val images come from Open Images, and the set's own labels split them into in-domain (417 images, only COCO classes), near-domain (2,670) and out-domain (1,413, no COCO classes) [@Agrawal2019NoCaps].

### 8.2 COCO Karpathy test: P1-EN PASS

**Table 11. Registered and reported English results (PTB CIDEr-D, paired 95% bootstrap CIs, B = 2,000).**

| row | COCO Karpathy test (5,000) | NoCaps val (4,500) | NoCaps val without the earlier 1,000 (3,500) |
|---|---|---|---|
| **pooled `ret` − `rand`** | **+3.08 [2.08, 4.03]** | **+1.73 [0.94, 2.50]** | +1.62 [0.66, 2.52] |
| verdict | **P1-EN PASS** | **S-NC FAIL** (point below +2.0) | FAIL |
| Qwen2.5-VL `ret` − `rand` (reported) | +7.80 [6.40, 9.17] | +2.83 [1.69, 3.98] | +2.35 [0.96, 3.73] |
| InternVL3 `ret` − `rand`, τ = 0.10 (reported) | −1.64 [−2.79, −0.49] | +0.62 [−0.37, 1.62] | +0.89 [−0.34, 2.00] |
| InternVL3 `ret` − `rand`, τ = −∞ (registered secondary) | −1.05 [−2.22, 0.08], not detected | +1.00 [−0.01, 2.01], not detected | +1.09 [−0.12, 2.21], not detected |
| pooled `ret` − `zs` (descriptive) | +21.89 [20.90, 22.88] | +19.05 [18.18, 19.95] | +19.04 [18.00, 20.05] |
| length gap \|ret − rand\| / rand, Qwen2.5-VL / InternVL3 | 0.019 / 0.019 (L does not fire) | 0.008 / 0.018 (reported) | 0.007 / 0.018 |

**P1-EN: PASS.** On the full COCO Karpathy test, retrieved examples beat random examples from the same memory by +3.08 [2.08, 4.03] PTB CIDEr-D points, pooled over the two backbones. The point is above the SESOI and the CI is above zero. Rule L does not fire: mean caption length in PTB tokens was 11.37 (`ret`) against 11.16 (`rand`) for Qwen2.5-VL and 12.47 against 12.72 for InternVL3.

**Per backbone** (reported rows, unadjusted CIs, no registered rule). The pooled gain is carried by Qwen2.5-VL: +7.80 [6.40, 9.17]. For InternVL3 at its frozen τ = 0.10 the row is −1.64 [−2.79, −0.49], a CI wholly below zero: on COCO, InternVL3's captions with retrieved examples scored *lower* than with random ones. Without the deletion step (τ = −∞, the registered secondary) the row is −1.05 [−2.22, 0.08], not detected, so on COCO the deletion step does not account for InternVL3's missing gain. No English scope sentence was registered, so "carried by Qwen2.5-VL" is a descriptive reading of the reported rows. A score below the random-example control is not new: OpenFlamingo-9B scored lower with retrieved than with random examples on Flickr-30K at 0 and 4 shots [@Awadalla2023OpenFlamingo].

**Against zero-shot** (descriptive rows; Table S13). For Qwen2.5-VL, `rand` − `zs` is +29.50 [28.27, 30.79] and `ret` − `zs` +37.30 [35.80, 38.75]; for InternVL3, +8.13 [7.03, 9.21] and +6.49 [5.27, 7.70]. *Post-hoc remark, not a claim:* for Qwen2.5-VL, random examples from the memory already account for most of its gain over zero-shot.

### 8.3 NoCaps val: S-NC FAIL

**S-NC: FAIL.** On the full NoCaps validation set, pooled `ret` − `rand` was +1.73 [0.94, 2.50]. The CI lies above zero, but the point is below the registered SESOI of +2.0, so the registered rule fails. **The claim that the gain transfers to NoCaps val is not made.** Under the XM-a rule (lower bound above zero only) it would have passed, but the rule registered for NoCaps is the P1 rule, chosen after XM-a was known (Section 8.1). The sensitivity without the 1,000 images decoded earlier by another study of the group is +1.62 [0.66, 2.52] and also fails. Per backbone (reported rows), Qwen2.5-VL gave +2.83 [1.69, 3.98] and InternVL3 +0.62 [−0.37, 1.62].

**Table 12. NoCaps val by the set's own domain label (pooled `ret` − `rand`; reported, non-gating; each domain on its own bootstrap matrix).**

| domain | images | pooled `ret` − `rand` |
|---|---|---|
| in-domain (only COCO classes) | 417 | +4.64 [1.85, 7.36] |
| near-domain | 2,670 | +1.96 [0.85, 2.99] |
| out-domain (no COCO classes) | 1,413 | +0.43 [−0.85, 1.73] |

The point estimate falls from in-domain to out-domain images; the intervals overlap and no trend test was registered.

### 8.4 Reading the English results beside the Vietnamese ones

This subsection is descriptive and post hoc. It computes no cross-language difference and changes no verdict.

![`ret` − `rand` on the four scored sets, per backbone and pooled, with paired 95% bootstrap CIs (values from Tables 7, 8 and 11; InternVL3 at its frozen τ = 0.10). Pooled rows are the registered estimands (P1, XM-a, P1-EN, S-NC); per-backbone rows are reported rows. Vietnamese sets use stripped CIDEr-D and English sets PTB CIDEr-D, in separate panels; no cross-language difference is computed. Solid line: zero; dashed line: the registered +2.0, a different quantity on each scale.](fig1_ret_minus_rand.svg)

<!-- Figure 1 made by the scratchpad script fig1_forest.py from manifest values only (C pass 3). -->

**The registered verdicts in each language** (Figure 1). In each language the registered in-domain prediction passed: P1 on OpenViIC test (+4.49 [3.52, 5.57], stripped CIDEr-D) and P1-EN on COCO Karpathy test (+3.08 [2.08, 4.03], PTB CIDEr-D). In each language the registered prediction on a set outside the memory's source did not pass, but the two failures differ: on XM3600 Vietnamese the gain was not detected (XM-a FAIL, CI including zero); on NoCaps val the CI lies above zero and the point is below the SESOI, under a stricter rule (S-NC FAIL). Within each language the in-domain gain is carried by Qwen2.5-VL. The InternVL3 rows differ between the languages: not detected on OpenViIC test, and below zero on COCO.

**A post-hoc question: does retrieval help mainly when the memory covers the target domain?** The Vietnamese memory holds no XM3600 captions, and the pooled gain was not detected there. The English memory is COCO, and on NoCaps the point estimate is largest for the images whose objects are all COCO classes and smallest for those with none (Table 12). Both observations are compatible with the hypothesis that retrieved examples beat random ones when the memory holds captions of images like the query. A text-only retrieval stage in a different pipeline, for Indigenous languages of the Americas, also helped only with large in-domain corpora [@Dhawan2026Gators]. The hypothesis was not registered and is not tested here. Three observations limit it:
1. **The domain split has overlapping CIs.** The three NoCaps domains were reported, not compared.
2. **Image-level similarity did not order the gain.** Within OpenViIC test the gain did not rise monotonically with the nearest-neighbour cosine, and within XM-test2500 the high-cosine tertile had the lowest point (Section 6.5).
3. **For Qwen2.5-VL the gain shrinks rather than vanishes.** Its out-of-source rows stay above zero: +3.15 [1.50, 4.93] on XM-test2500 and +2.83 [1.69, 3.98] on NoCaps val (reported rows). The pooled failures also reflect InternVL3's rows.

The development-set memory-size ablation of Section 6.8 is consistent with this reading (a smaller in-domain memory gave a smaller gain); it is dev evidence and does not test the English rows.

### 8.5 Disclosures for the English arm

**When the registration was written.** The registration was drafted after the three Vietnamese decision files had been read (Section 7.4), but its sets, SESOI, arms and configuration had been fixed in an earlier ruling, before any Vietnamese verdict; only the NoCaps rule followed XM-a. It was committed before any English image was decoded, embedded or scored, and each set was decided once (supplement, "Test-run operations").

**The English deletion step is a port.** InternVL3's τ = 0.10 was selected on Vietnamese development data with the Vietnamese object matcher. The English side uses the companion object-precision study's COCO-80 matcher, which shares 24 of its 80 classes with the 112-class Vietnamese verifier map, and a mechanical class phrase. Its calibration is untested in English, so the τ = −∞ row is printed beside every τ = 0.10 row.

**Image source and earlier contact.** NoCaps images were fetched by their official Open Images ids from the Open Images validation bucket, because the NoCaps proxy no longer serves them; bytes or resolution may differ. Earlier contact with the English sets (a companion study's scoring on the Karpathy test, an earlier zero-shot decode of 295 Karpathy test images, another study's 1,000 NoCaps images, and the 133 Karpathy test images in the UIT-ViIC pre-check of Section 7.2) is listed in the supplement. None of those outputs is reused here, and no design choice follows from them.

**Compute.** The two test blocks used 6.33 (COCO) and 6.88 (NoCaps) GPU-hours, together 13.22 of the 25 GPU-hour test cap, on one 24 GB GPU.

### 8.6 Context from published systems (no ordering implied)

Table S15 prints the CIDEr scores that other papers report on the benchmarks of this study beside this study's own runs, with its inclusion rule and each system's setting and data. It is not a ranking: scorers, tokenisation, document-frequency sets, memories, image subsets and, for Vietnamese, word segmentation differ between papers, and no test set of this study was re-scored with a published scorer. The one reading it supports is that a training-free prompt remains far below a fine-tuned system on OpenViIC test (best published baseline 75.58 CIDEr [@Bui2023OpenViIC]), which is the gap that motivates retrieval (Section 1).
