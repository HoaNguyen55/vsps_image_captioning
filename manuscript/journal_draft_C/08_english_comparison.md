## 8. English comparison: COCO Karpathy test and NoCaps val

This section reports the English arm. It is a separate registration that carries the Vietnamese design over to English with no English tuning. Every number comes from its two decision files and its run logs. English results are reported within English only. No cross-language difference is computed, and no Vietnamese claim of Sections 6 and 7 changes in their light.

### 8.1 Registration

**What was carried over.** The English registration fixed every design choice from the Vietnamese one:
- the frozen configurations of Table 2 (k, order, τ, the two backbones and their pinned snapshots);
- greedy decoding with 60 new tokens;
- the retrieval near cut and the near-duplicate rule of Section 3.1;
- the seeded `rand` draw;
- the deletion step with its zero-shot fallback.

The prompt header, example line and tails T1 and T2 are direct English translations, pinned by hash. Only three arms were decoded per backbone: `ret`, `rand` and `zs`. There was no `fix` arm, no English development set and no English tuning of any kind.

**Scorer.** The English decision column is PTB-tokenised CIDEr-D (×100) from pycocoevalcap 1.2 [@Chen2015COCOCaptions], with document frequencies taken over each scored set's own references. The Vietnamese decision column (Section 3.6) is stripped CIDEr-D on word-segmented text (RDRSegmenter word tokens). The two columns are not on one scale, which is one reason no cross-language difference is computed.

**Registered rules.** Both sets use the Vietnamese P1 rule: PASS if the pooled `ret` − `rand` point is above the SESOI of +2.0 **and** the 95% CI lower bound is above zero. Each set is decoded once, scored once and decided once. Applying this one rule to NoCaps as well was fixed after the Vietnamese XM-a result was known. It is stricter than the XM-a rule, which asked only for a CI lower bound above zero (Table 4). The two out-of-source results therefore answer different rules. The SESOI of +2.0 was carried over numerically from the Vietnamese registration and was not recalibrated for the PTB-tokenised English scale; because English scores are higher, it is relatively more lenient on COCO (Section 5.4).

**Table 16. Registered English predictions.**

| name | set | estimand | rule |
|---|---|---|---|
| **P1-EN** (primary) | COCO Karpathy test, full 5,000 [@Lin2014COCO; @Karpathy2015Split] | mean pooled Δ_i (PTB CIDEr-D) | point > +2.0 and CI lower bound > 0; length rule L as in Table 4 |
| **S-NC** (secondary, fixed order) | NoCaps val, full 4,500 [@Agrawal2019NoCaps] | mean pooled Δ_i | the same rule |
| sensitivity | NoCaps val without the 1,000 images decoded earlier (3,500) | the same | reported beside S-NC, never replacing it |

The claim "the gain transfers to NoCaps val" needed both P1-EN and S-NC to pass. The NoCaps block was decoded and decided whatever P1-EN showed. Three kinds of row are reported without a rule: per-backbone rows, `ret` − `zs` and `rand` − `zs` (descriptive), and the per-domain NoCaps rows. As in Table 13, InternVL3's `ret` − `rand` at τ = −∞ is a registered secondary under its own key. It is labelled "detected" only when its CI lower bound is above zero, and no gate reads it.

**References and memory.**
- **COCO references.** The first 5 references of each image, in Karpathy order. 10 of the 5,000 images have a sixth reference, which is not used.
- **NoCaps references.** All references as released.
- **Memory.** COCO Karpathy train and restval, 113,287 candidates. Removing 965 ids reserved for companion studies' test sets leaves 112,322. The fetch then recorded 112,320, after refusing 2 images that are byte copies of a Karpathy test image. Two more filters followed:
  - near-duplicate drops against Karpathy test (28), NoCaps val (15) and Karpathy val (23), 65 distinct images because one image can match more than one set, left 112,255 images;
  - clustering under the rule of Section 3.1 gave 111,927 clusters.
- **Shown captions.** Each cluster shows the first reference of its smallest-id member.

The memory is therefore in the COCO domain by construction. NoCaps val is not in that domain in the same way: its images come from Open Images, and the set's own labels split them into in-domain (417 images, only COCO classes), near-domain (2,670) and out-domain (1,413, no COCO classes) [@Agrawal2019NoCaps].

### 8.2 COCO Karpathy test: P1-EN PASS

**Table 17. Registered and reported English results (PTB CIDEr-D, paired 95% bootstrap CIs, B = 2,000).**

| row | COCO Karpathy test (5,000) | NoCaps val (4,500) | NoCaps val without the earlier 1,000 (3,500) |
|---|---|---|---|
| **pooled `ret` − `rand`** | **+3.08 [2.08, 4.03]** | **+1.73 [0.94, 2.50]** | +1.62 [0.66, 2.52] |
| verdict | **P1-EN PASS** | **S-NC FAIL** (point below +2.0) | FAIL |
| Qwen2.5-VL `ret` − `rand` (reported) | +7.80 [6.40, 9.17] | +2.83 [1.69, 3.98] | +2.35 [0.96, 3.73] |
| InternVL3 `ret` − `rand`, τ = 0.10 (reported) | −1.64 [−2.79, −0.49] | +0.62 [−0.37, 1.62] | +0.89 [−0.34, 2.00] |
| InternVL3 `ret` − `rand`, τ = −∞ (registered secondary) | −1.05 [−2.22, 0.08], not detected | +1.00 [−0.01, 2.01], not detected | +1.09 [−0.12, 2.21], not detected |
| pooled `ret` − `zs` (descriptive) | +21.89 [20.90, 22.88] | +19.05 [18.18, 19.95] | +19.04 [18.00, 20.05] |
| length gap \|ret − rand\| / rand, Qwen2.5-VL / InternVL3 | 0.019 / 0.019 (L does not fire) | 0.008 / 0.018 (reported) | 0.007 / 0.018 |

**P1-EN: PASS.** On the full COCO Karpathy test, retrieved examples beat random examples from the same memory by +3.08 [2.08, 4.03] PTB CIDEr-D points, pooled over the two backbones. The point is above the SESOI and the CI is above zero. Rule L does not fire. Mean caption length in PTB tokens was:
- Qwen2.5-VL: 11.37 (`ret`) against 11.16 (`rand`);
- InternVL3: 12.47 against 12.72.

**Per backbone** (reported rows, unadjusted CIs, no registered rule). The pooled gain is carried by Qwen2.5-VL: +7.80 [6.40, 9.17]. For InternVL3 at its frozen τ = 0.10 the row is −1.64 [−2.79, −0.49], a CI wholly below zero: on COCO, InternVL3's captions with retrieved examples scored *lower* than with random ones. Without the deletion step (τ = −∞, the registered secondary) the row is −1.05 [−2.22, 0.08], not detected. On COCO, then, the deletion step does not account for InternVL3's missing gain. Section 6.8 returns to this. No English scope sentence was registered, so "carried by Qwen2.5-VL" is a descriptive reading of the reported rows, not a registered scope. A score below the random-example control is not new: with interleaved image-caption examples, OpenFlamingo-9B scored lower with retrieved than with random examples on Flickr-30K at 0 and 4 shots [@Awadalla2023OpenFlamingo].

**Against zero-shot** (descriptive rows). Pooled `ret` − `zs` is +21.89 [20.90, 22.88]. Per backbone, `rand` − `zs` is +29.50 [28.27, 30.79] and `ret` − `zs` +37.30 [35.80, 38.75] for Qwen2.5-VL. For InternVL3 the same two rows are +8.13 [7.03, 9.21] and +6.49 [5.27, 7.70]. *Post-hoc remark, not registered and not a claim:* for Qwen2.5-VL, random examples from the memory already account for most of its gain over zero-shot. Supplement Table S13 holds every per-backbone row.

### 8.3 NoCaps val: S-NC FAIL

**S-NC: FAIL.** On the full NoCaps validation set, pooled `ret` − `rand` was +1.73 [0.94, 2.50]. The CI lies above zero, but the point is below the registered SESOI of +2.0, so the registered rule fails. **The claim that the gain transfers to NoCaps val is not made.** The CI is above zero but the point is below the registered +2.0. Under the XM-a rule (lower bound above zero only) it would have passed, but the rule registered for NoCaps is the P1 rule, chosen after XM-a was known (Section 8.1). The sensitivity without the 1,000 images decoded earlier by another study of the group is +1.62 [0.66, 2.52]. It also fails, which changes nothing.

Per backbone (reported rows), Qwen2.5-VL gave +2.83 [1.69, 3.98] and InternVL3 +0.62 [−0.37, 1.62].

**Table 18. NoCaps val by the set's own domain label (pooled `ret` − `rand`; reported, non-gating; each domain on its own bootstrap matrix).**

| domain | images | pooled `ret` − `rand` |
|---|---|---|
| in-domain (only COCO classes) | 417 | +4.64 [1.85, 7.36] |
| near-domain | 2,670 | +1.96 [0.85, 2.99] |
| out-domain (no COCO classes) | 1,413 | +0.43 [−0.85, 1.73] |

The point estimate falls from the in-domain images to the out-domain images. The in-domain CI lies above zero, while the out-domain CI includes zero. The three intervals overlap, no trend test was registered, and the rows are not tested here.

### 8.4 Reading the English results beside the Vietnamese ones

This subsection is descriptive and post hoc. It computes no cross-language difference and changes no verdict.

![`ret` − `rand` on the four scored sets, per backbone and pooled, with paired 95% bootstrap CIs (values from Tables 7, 8 and 17; InternVL3 at its frozen τ = 0.10). The pooled rows are the registered estimands (P1, XM-a, P1-EN, S-NC); the per-backbone rows are reported rows with no registered rule. The Vietnamese sets are scored with stripped CIDEr-D and the English sets with PTB CIDEr-D, so the panels are read within each language and no cross-language difference is computed. The two languages are drawn in separate panels. Solid line: zero; dashed line: the registered threshold of +2.0, which is a different quantity on each scale.](fig1_ret_minus_rand.svg)

<!-- Figure 1 made by the scratchpad script fig1_forest.py from manifest values only (C pass 3). -->

**The registered verdicts in each language** (Figure 1). In each language the registered in-domain prediction passed: P1 on OpenViIC test (+4.49 [3.52, 5.57], stripped CIDEr-D) and P1-EN on COCO Karpathy test (+3.08 [2.08, 4.03], PTB CIDEr-D). In each language the registered prediction on a set outside the memory's source did not pass, but the two failures differ. On XM3600 Vietnamese the gain was not detected (XM-a FAIL, CI including zero). On NoCaps val the CI lies above zero and the point is below the SESOI, under a rule stricter than XM-a's (S-NC FAIL). Within each language the in-domain gain is carried by Qwen2.5-VL. The InternVL3 rows differ between the languages: not detected on OpenViIC test, and below zero on COCO.

**A post-hoc question: does retrieval help mainly when the memory covers the target domain?** The Vietnamese memory holds no XM3600 captions (Section 6.3), and the pooled gain was not detected there. The English memory is COCO, and on NoCaps the point estimate is largest for the images whose objects are all COCO classes (+4.64 [1.85, 7.36]) and smallest for those with none (+0.43 [−0.85, 1.73]). Both observations are compatible with the hypothesis that retrieved examples beat random ones when the memory holds captions of images like the query, and that the advantage fades as the target moves out of the memory's domain. A text-only retrieval stage in a different pipeline, for Indigenous languages of the Americas, also helped only with large in-domain corpora [@Dhawan2026Gators]. The hypothesis was not registered and is not tested here. Three observations limit it:
1. **The domain split has overlapping CIs.** The three NoCaps domains were reported, not compared, and their intervals overlap.
2. **Image-level similarity did not order the gain.** Within OpenViIC test the gain did not rise monotonically with the query's nearest-neighbour cosine (Table 10). Within XM-test2500 the high-cosine tertile had the lowest point, which cuts against the hypothesis. If coverage matters, it shows at the level of the domain, not of the single nearest neighbour.
3. **For Qwen2.5-VL the gain shrinks rather than vanishes.** Its out-of-source rows stay above zero: +3.15 [1.50, 4.93] on XM-test2500 and +2.83 [1.69, 3.98] on NoCaps val (reported rows). The pooled failures also reflect InternVL3's rows.

The development-set memory-size ablation of Section 6.8 is consistent with this reading: there, a smaller in-domain memory gave a smaller gain. It is dev evidence and does not test the English rows.

### 8.5 Disclosures for the English arm

**When the registration was written.** The English arm was committed on the Vietnamese test day, after the OpenViIC test block had started and before the first decision file existed (Section 7.4). Its registration was drafted after all three Vietnamese decision files existed and after their headline numbers had been read. Its sets, SESOI, arms and carried-over configuration had been fixed in an earlier ruling, before any Vietnamese verdict. The decision to apply the P1 rule to NoCaps as well, rather than XM-a's lower-bound-only rule, was fixed after the XM-a result was known (Section 8.1). The registration, its pinned lists and its code were committed before any English image was decoded, embedded or scored.

**One look per set.** The COCO block ran first and was decided before the NoCaps block; each set was decoded, scored and decided once, at unchanged English code and registration paths. Run details, one pre-decode amendment and a smoke test on memory images are in the supplement ("Test-run operations"); the InternVL3 deletion counts are in Table S13.

**The English deletion step is a port.** InternVL3's τ = 0.10 was selected on Vietnamese development data with the Vietnamese object matcher. The English side instead uses the companion object-precision study's COCO-80 matcher, which shares 24 of its 80 classes with the 112-class Vietnamese verifier map. The class phrase is a mechanical article plus class name, and a few phrases are ungrammatical (plural class names after "a"). The calibration of the step is untested in English. The τ = −∞ row is therefore printed beside every τ = 0.10 row.

**NoCaps image source.** The NoCaps image proxy no longer serves the files. Each image was fetched by its official Open Images id from the Open Images validation bucket, so its bytes or resolution may differ from the copy the proxy served.

**Earlier contact with the English sets.** None of the following outputs is reused here, and no design choice follows from them:
1. The companion object-precision study scored 9 Vietnamese-output systems on the full Karpathy test, all Qwen2.5-VL-7B variants. None is a `ret` or `rand` arm. That study also used the references of 2,441 of these images.
2. An earlier English zero-shot decode by both backbones, with the same zero-shot prompt and decoding, covers 295 of the 5,000 Karpathy test images. Its object precision and recall were seen; its CIDEr-D was not. These are, in effect, the `zs` arm on those images, and `zs` gates nothing.
3. Another study of the group decoded and scored Qwen-model outputs on a stratified 1,000 NoCaps val images. The 3,500-image sensitivity excludes them.
4. The 163-image reference exposure of Section 7.2 touches 133 Karpathy test images. Only gold references were read, in aggregate, and no image is dropped.
5. Karpathy val features are used only to protect it, and no model output of this study exists on it. The evaluation sets of the companion object-precision study include 130 Karpathy-val ids; none of that study's outputs is reused or scored here.
6. The memory includes a 2,402-image pool that another study of the group uses. These images are kept and disclosed.

**Compute.** The two test blocks used 6.33 GPU-hours (COCO, 22,797 s) and 6.88 GPU-hours (NoCaps, 24,779 s), together 13.22 of the 25 GPU-hour test cap, on one 24 GB GPU.

### 8.6 Context from published systems (no ordering implied)

Table 19 prints numbers that other papers report on the benchmarks of this study beside this study's own runs, as context for the absolute level of a training-free prompt. It is not a ranking, and no claim of this study rests on it. The published numbers are copied from each paper's table and were not re-run. Scorers, tokenisation, document-frequency sets, memories, image subsets and, for Vietnamese, word segmentation differ between papers, and no test set of this study was re-scored with a published scorer, which would be a second look.

**Inclusion rule.** English sets: every system discussed in Section 2 that reports a score on the set. XM3600 Vietnamese: every system in the Vietnamese column of the two cited tables (LMCap Tab. 6 and CONCAP Tab. 10), except the cited paper's own ablation variants. OpenViIC test: the best of the eight baselines in the dataset paper, the only published numbers we found.

**Table 19. Published CIDEr scores (block A) and this study's runs (block B). No ordering is implied.** Settings: "trained" = the captioner is trained on captions; "text-only" = trained on text alone; "training-free" = no training. "Images" is the evaluated image set.

*Block A. Published systems (copied from the cited tables, not re-run; CIDEr as reported, ×100).*

| benchmark | system | setting | memory / training data (see source) | images | CIDEr | source |
|---|---|---|---|---|---|---|
| COCO Karpathy test | SmallCap | trained | COCO captions | 5,000 | 119.7 | @Ramos2023SmallCap, Tab. 1 |
| COCO Karpathy test | EXTRA (cross-entropy) | trained | COCO captions | 5,000 | 120.9 | @Ramos2023EXTRA, Tab. 1 |
| COCO Karpathy test | EVCap | trained | COCO captions; Vicuna-13B language model | 5,000 | 140.1 | @Li2024EVCap, Tab. 1 |
| COCO Karpathy test | ViECap | text-only | text only | 5,000 | 92.9 | @Fei2023ViECap, Tab. 3 |
| COCO Karpathy test | MeaCap | training-free | COCO caption memory | 5,000 | 56.9 | @Zeng2024MeaCap, Tab. 2 |
| NoCaps val, overall | SmallCap | trained | COCO captions | 4,500 | 77.9 | @Ramos2023SmallCap, Tab. 8 |
| NoCaps val, overall | EVCap | trained | COCO captions; Vicuna-13B language model | 4,500 | 119.3 | @Li2024EVCap, Tab. 1 |
| NoCaps val, overall | ViECap | text-only | text only | 4,500 | 66.2 | @Fei2023ViECap, Tab. 1 |
| NoCaps val, overall | MeaCap | training-free | CC3M caption memory | 4,500 | 40.2 | @Zeng2024MeaCap, Tab. 1 |
| XM3600 Vietnamese | BB+CC (from Thapliyal et al. 2022) | trained | as in @Thapliyal2022XM3600 | XM3600, as in source | 33.6 | @Ramos2023LMCap, Tab. 6 |
| XM3600 Vietnamese | LG (from Thapliyal et al. 2022) | trained | as in @Thapliyal2022XM3600 | XM3600, as in source | 18.2 | @Ramos2023LMCap, Tab. 6 |
| XM3600 Vietnamese | LMCap | training-free; text-only generator, image used for retrieval | retrieved multilingual captions | XM3600, as in source | 26.5 | @Ramos2023LMCap, Tab. 6 |
| XM3600 Vietnamese | mBLIP | trained | multilingual, partly machine-translated data | XM3600, as in source | 35.8 | @Ibrahim2025CONCAP, Tab. 10 |
| XM3600 Vietnamese | Pangea | trained (instruction-tuned 7B MLLM) | multilingual instruction data | XM3600, as in source | 64.3 | @Ibrahim2025CONCAP, Tab. 10 |
| XM3600 Vietnamese | CONCAP | trained | retrieved captions and concepts | XM3600, as in source | 45.1 | @Ibrahim2025CONCAP, Tab. 10 |
| OpenViIC test | MDSANet, best of eight baselines | trained, CIDEr-optimised | OpenViIC train | full test | 75.58 | @Bui2023OpenViIC, Tab. II |

*Block B. This study (per-run ledger aggregates, descriptive; no task training in this study, and the backbones' training data are not fully disclosed and may include COCO, Section 9.1).*

| benchmark | system | memory | images | CIDEr column | `ret` / `rand` / `zs` |
|---|---|---|---|---|---|
| COCO Karpathy test | Qwen2.5-VL | COCO train + restval captions | 5,000 | PTB CIDEr-D | 96.36 / 88.57 / 59.06 |
| COCO Karpathy test | InternVL3 (τ = 0.10) | COCO train + restval captions | 5,000 | PTB CIDEr-D | 85.34 / 86.98 / 78.85 |
| NoCaps val, overall | Qwen2.5-VL | COCO train + restval captions | 4,500, images re-fetched from Open Images and scored locally | PTB CIDEr-D | 91.13 / 88.30 / 58.46 |
| NoCaps val, overall | InternVL3 (τ = 0.10) | COCO train + restval captions | 4,500, as above | PTB CIDEr-D | 83.73 / 83.10 / 78.30 |
| XM3600 Vietnamese | Qwen2.5-VL / InternVL3 (τ = 0.10), `ret` only | KTVIC + OpenViIC train | XM-test2500 | as-written CIDEr-D, word-segmented; **not comparable** | 59.13 / 53.47 |
| OpenViIC test | Qwen2.5-VL / InternVL3 (τ = 0.10), `ret` only | KTVIC + OpenViIC train | all 2,001 files | as-written CIDEr-D, word-segmented; **not comparable** | 33.64 / 29.70 |

The Vietnamese rows of block B are marked not comparable: they use the companion scoring kit's word-segmented as-written column on this study's image subsets, while the published rows use their own scorers on the full sets. The one reading the table supports is that a training-free prompt remains far below a fine-tuned system on OpenViIC test, which is the gap that motivates retrieval (Section 1).
