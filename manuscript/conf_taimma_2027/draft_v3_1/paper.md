<!--
DRAFT v3 (CUT PROPOSAL, not ruled): conference version of Paper C (scope S1 of WRITING_PLAN_C_TAIMMA_v1.md), for TAIMMA 2027, Springer LNCS format.
Made from draft v2.1 (paper.md sha256 f65f53ab...) after the LNCS build of 15 Nov 2026 gave 19 pages against a limit of 15.
Every removed or changed unit is listed with its OLD text in REVISION_NOTES_V3.md, so that each can be put back singly. No number was changed.
LENGTH WARNING (plan item A16): the venue limit for a full paper is 12 to 15 pages. The page estimate of this draft is in PAGE_BUDGET.md; it is an estimate from the measured pages of v2.1, not a build.
Table labels were renumbered after three tables were removed: markers T4, T5, T6, T7 now carry the printed labels Table 1 to Table 4.
Every number is keyed in number_manifest_TAIMMA.tsv. No data-set caption appears anywhere in this draft.
Sections 5 and 7: to re-check after 16 Nov 05:00Z (CC-392 N12). Two units wait for that re-check and are byte-unchanged from v2.1: C26 (the dagger note of the per-arm table and S5-09) and C44 (S7-L06) (CC-399 G2).
-->

# Do Retrieved Examples Beat Random Ones? A Preregistered Test of In-Context Vietnamese Image Captioning

<!-- p:AUTH -->[AUTHORS: to be set by the PI]

## Abstract

<!-- p:ABS-01 -->Retrieval in-context captioning places the captions of similar memory images in a multimodal model's prompt. It needs no training, which suits low-resource languages such as Vietnamese, but a gain over zero-shot prompting may come from any in-domain caption, not from retrieval. This preregistered study, with one look per test set, compares retrieved example captions with an equal number of random captions from the same memory, for two open models reported separately. On OpenViIC test, retrieved examples beat random ones by +4.49 [3.52, 5.57] stripped CIDEr-D points pooled (95% bootstrap CI; registered PASS), with the registered scope "carried mainly by Qwen2.5-VL; not detected for InternVL3". There, the change in count-matched object precision against zero-shot stayed above the registered floor for both models (PASS). On XM3600 Vietnamese, outside the memory's source, the gain was not detected: +0.70 [−0.45, 1.97], a registered FAIL under a rule that required a CI above zero. In English, with the frozen configurations, the COCO Karpathy test passed (+3.08 [2.08, 4.03] PTB CIDEr-D points; PASS), although InternVL3's reported row there is below zero. On NoCaps the point, +1.73 [0.94, 2.50], lay below the registered +2.0 (FAIL). No transfer claim is made in either language. Crediting a gain to retrieval requires a random-example control at equal k and results per model.

## Keywords

<!-- p:KW -->Image captioning · In-context examples · Retrieval augmentation · Vietnamese · Preregistration

## 1 Introduction

<!-- p:S1-01 -->Open multimodal large language models (MLLMs) can caption images in Vietnamese with no task training, but their zero-shot captions score far below fine-tuned systems: the best fine-tuned baseline in the UIT-OpenViIC data set paper reports 75.58 CIDEr on its test set [@Bui2023OpenViIC], a published number, not comparable with this study's scorer. Vietnamese captioning is low-resource: the public general-domain caption sets are few and far smaller than English sets such as COCO, and each has its own domain and reference style [@Pham2024KTVIC; @Bui2023OpenViIC]. A method that uses the little in-language data that exists, without training on it, is therefore attractive.

<!-- p:S1-02 -->Retrieval in-context captioning is such a method: the captions of a query image's nearest memory images are placed in the prompt as text examples. Method papers report large CIDEr gains from such examples [@Ramos2023LMCap; @Rebelo2025RSCap]. A gain over zero-shot prompting can, however, reflect two effects: *retrieval* (the examples describe similar images) or *in-domain style* (the examples merely show how the data set's captions are written). If only style matters, a cheaper prompt with random or fixed examples would do as well. Analyses of this question exist for English and for multilingual news captioning (Sect. 2). As far as those papers state, none preregisters its contrasts or reports confidence intervals on the captioning score, and none covers Vietnamese.

<!-- p:S1-03 -->This study measures the first effect against the second. Two open MLLMs caption each image under four prompts: retrieved examples (`ret`), the same number k of random examples from the same memory (`rand`), one fixed example set (`fix`) and zero-shot (`zs`). Configurations were frozen on development data in two registered stages. Each test set was then decoded, scored and decided once, under estimands, thresholds and failure wordings fixed in advance.

<!-- p:S1-04 -->The study proposes no new method. It contributes:

- <!-- p:S1-05 -->**A registered evaluation design** for Vietnamese captioning with training-free MLLMs and text-only example captions. Its random control uses the same k and the same memory as retrieval, results are given for each backbone, and each of the four test sets got a single look under rules written beforehand.
- <!-- p:S1-06 -->**In the memory's source, in two languages.** The registered primary passed on OpenViIC test (+4.49 [3.52, 5.57] stripped CIDEr-D points; P1 PASS) and on the COCO Karpathy test (P1-EN PASS). Under the registered scope sentence the Vietnamese gain is "carried mainly by Qwen2.5-VL; not detected for InternVL3". On COCO, InternVL3's row is below zero (a reported row; no English scope sentence was registered). On OpenViIC test, the change in count-matched object precision against each model's own zero-shot captions stayed above the registered floor for both models (P2 PASS).
- <!-- p:S1-07 -->**Outside the memory's source.** On XM3600 Vietnamese the gain was not detected: +0.70 [−0.45, 1.97], a FAIL under a rule that required a CI above zero. On NoCaps val the interval clears zero, but the point, +1.73 [0.94, 2.50], falls short of the registered +2.0 (FAIL). No transfer claim is made in either language.

## 2 Related work

<!-- p:S2-02 -->**The random control exists.** For trained retrieval-augmented captioners, one study evaluates a variant that reads a random caption from the datastore [@Ramos2023EXTRA], and another gives a trained captioner, at the same k, captions retrieved for a different image [@Li2024RetrievalRobustness]. Studies of in-context selection compare similarity-chosen with random examples, mostly in English and with example images [@Yang2023ICLConfig; @Li2025UnveilingICL].

<!-- p:S2-03 -->**The English precedent.** OpenFlamingo reports that retrieved image-caption examples beat random ones on COCO, and that on Flickr30K they scored lower at the smaller shot counts it reports [@Awadalla2023OpenFlamingo]. Our COCO result therefore repeats a pattern already known for English, under other conditions (example captions as text only, configurations frozen in another language, a single look). It is not a new English finding.

<!-- p:S2-04 -->**Closest multilingual and Vietnamese work.** A training-free multilingual study for remote sensing retrieves in-context examples, with neither an equal-k random control nor a registered test [@Rebelo2025RSCap]. The news-captioning benchmark MUNIChus compares random with similarity-retrieved examples at equal k in several languages that do not include Vietnamese, and reports point scores [@Chen2026MUNIChus]. Two multilingual retrieval-augmented captioners list Vietnamese among their languages, one of them training-free, and neither has a random control [@Ramos2023LMCap; @Ibrahim2025CONCAP].

<!-- p:S2-05 -->**What differs here.** Five earlier analyses have a random control at equal shots or equal k, four on English caption data [@Yang2023ICLConfig; @Li2024RetrievalRobustness; @Baldassini2024MICL; @Li2025UnveilingICL] and one multilingual without Vietnamese [@Chen2026MUNIChus]. A search of each paper's full text found no statement of a registered one-look test and no CI on the captioning score. This study is an analysis of training-free Vietnamese captioning with an equal-k random control from the same memory, beside a fixed-example control; paired bootstrap CIs for every row, per backbone; and a preregistered test with one look per set. No priority claim is made for retrieval in-context captioning, for the random control or for the registered design.

## 3 Method

<!-- p:S3-01 -->**Memory.** The Vietnamese memory joins the KTVIC training images outside a development carve [@Pham2024KTVIC] with the UIT-OpenViIC training images [@Bui2023OpenViIC]: 3,469 + 9,088 = 12,557 candidates. A pre-specified filter excluded 2,056 of them: unreadable files and images identical or near-duplicate to an evaluation image. The remaining 10,501 images form 8,190 clusters under a pre-specified visual-similarity rule [@Pizzi2022SSCD]; a cluster is shown at most once per query, through one caption.

<!-- p:S3-02 -->**Arms.** Images are embedded with SigLIP2 [@Tschannen2025SigLIP2]. A cluster whose cosine to the query is at least 0.92 is shown to that query in no arm (the near cut). The arms share one prompt template and differ only in its example block:

- `ret`: the k eligible clusters with the highest cosine to the query;
- `rand`: k eligible clusters drawn for that query by a seeded generator;
- `fix`: one set of k clusters, drawn once per test set and shown to every image;
- `zs`: no examples (zero-shot).

<!-- p:S3-03 -->**Prompt and decoding.** The prompt follows the image: a fixed Vietnamese header saying that the captions below belong to other images and only show how to write, k numbered example lines, and a tail asking for one short Vietnamese sentence in the examples' style. Tail T1 also asks for only what is visible; tail T2 does not. "Order" places the most similar example first, or last, next to the instruction. The template contains no data-set caption. Decoding is greedy, with at most 60 new tokens, for Qwen2.5-VL-7B-Instruct [@Bai2025Qwen25VL] and InternVL3-8B [@Zhu2025InternVL3].

<!-- p:S3-04 -->**Neighbour-only objects and the deletion step.** An object class is *neighbour-only* when the object matcher finds it in the caption and in at least one shown example, but not in the same model's zero-shot caption. A second model, the verifier, scores each such class as the probability of "yes" to a yes/no question with the image minus that without it; a class scoring below a threshold τ is rejected. The caption is split at commas, conjunctions and locative words, and each part naming a rejected class is dropped; if the subject part is hit or the result is malformed, the zero-shot caption is used. At τ = −∞ nothing is rejected.

<!-- p:S3-05 -->**Frozen configurations.** Development stage A chose one configuration per backbone by a rule written before any output: the highest stripped CIDEr-D among its `ret` runs on the KTVIC carve that met three pre-set conditions, one of them a floor on the object-precision change against zero-shot. The frozen configurations are: Qwen2.5-VL-7B, k = 8, order first, tail T1, τ = −∞ (no deletion), no verifier at test; InternVL3-8B, k = 4, order last, tail T2, τ = 0.10, verifier at test Qwen3-VL-8B-Instruct. `rand` and `fix` run at the picked k, tail and τ, so `ret` − `rand` is measured at a configuration selected on the `ret` score. Nothing was changed for the test or for English. InternVL3's `ret`, `rand` and `fix` captions pass through the deletion step at τ = 0.10, so the step is part of InternVL3's registered estimand; Qwen2.5-VL's captions are scored as decoded. The step stayed, with τ as fixed at stage A, although at stage B the guard hypothesis H_G was not passed: it needed a neighbour-only precision change with a CI above zero and a stripped CIDEr-D cost within a registered bound, and the cost, −4.01, lay outside that bound (pooled precision change +2.91 [0.46, 5.31] points). No guard claim is made.

<!-- p:S3-06 -->**Scoring.** Vietnamese candidates and references are lower-cased and segmented into words with RDRSegmenter [@Nguyen2018VnCoreNLP; @Vu2018VnCoreNLP]. CIDEr-D [@Vedantam2015CIDEr] takes its document frequencies from the references of the scored set and is given in points (the score times one hundred). Decisions use *stripped* CIDEr-D, computed after trailing punctuation tokens are dropped from both candidates and references; an arm can then gain nothing from a final period alone.

<!-- p:S3-07 -->**Count-matched object precision** is the instrument of a companion manuscript by the same group (the object-precision study, in preparation), defined here because the object-precision prediction P2 uses it. For image i, let M_i(run) and M_i(zs) be the distinct object classes matched, in order of first mention, in the run's caption and in the same model's zero-shot caption, and let k_i = min(|M_i(run)|, |M_i(zs)|). tp_cm counts how many of the first k_i classes of the run's caption the gold supports; tp_cm,zs counts the same for the zero-shot caption. Then ΔP_cm = (Σ tp_cm − Σ tp_cm,zs) / Σ k_i, in percentage points. The equal number of mentions keeps a longer caption from being penalised for naming more objects. The gold of an image is the union of the classes that the same manuscript's tone-normalised Vietnamese matcher finds in its references; CHAIR_i [@Rohrbach2018CHAIR] uses the same gold. Verified precision on XM3600 (XM-b) counts all mentions against the released human-verified Open Images labels [@Kuznetsova2020OpenImages].

## 4 Data and registered plan

<!-- p:S4-01 -->**Data.** The study uses only public data sets, with the references and labels their authors released; nothing was annotated for it, and gold never comes from a model output. The primary OpenViIC test set (OV-test primary, 1,941 images) is the full test split of 2,001 images minus 60 images that a pre-specified filter, fixed before any test output, matched to the KTVIC development carve. The 3,600 XM3600 images [@Thapliyal2022XM3600] were split before any output of this study existed: 600 were set aside as the evaluation subset of the companion manuscript, and the rest were ordered by a hash of their bytes. The first 500 form XM-dev500, a secondary set of stage B, and the other 2,500 form XM-test2500, with 5,108 Vietnamese references; no full-XM3600 result is therefore reported. The Vietnamese memory holds no XM3600 caption, so XM-test2500 lies outside the memory's source.

<!-- p:S4-02 -->**Three stages.** Each stage was committed before its data were decoded. Stage A, exploratory, chose the configurations of Sect. 3 on a KTVIC development carve and checked them on one half of the OpenViIC development set (OV-dev-A, 911 images; the halves follow a hash order and passed the filter of Sect. 3). Stage B gave one look at the other half (OV-dev-B, 925 images) under a gate: pooled `ret` − `rand` with a CI above zero and a point of at least +4.0. The gate returned PASS, with +6.04 [4.54, 7.58]; it is a development result and sets nothing at test. The test registration was committed after that result and before any test output existed. The English registration came later (Sect. 6).

<!-- p:S4-03 -->**Estimands and rules.** For backbone m and image i, Δ_m,i is the score of `ret` minus that of `rand`, each at m's frozen configuration, and the pooled Δ_i is the mean of the two backbones' differences. A pooled number is thus an average over two pairs of backbone and configuration, which differ in k, order, tail and τ. It does not estimate the effect for a typical model, and each pooled number is shown with its per-backbone rows. The smallest effect size of interest (SESOI) is +2.0 points, a planning value set before any stage-B output; it equals the stage-A value; the stage-B registration states that it was not derived from the stage-A pilot or any stage-A number, and no calibration is recorded. The floors of P2 and XM-b and the threshold of rule L were also fixed before any stage-B output, and no derivation of them is recorded. Table 1 lists each registered prediction with its rule. The scope sentence that accompanies pooled P1 numbers was selected, by a mapping fixed before the test, from the P1b outcome. The wording for a failed XM-a was also registered: "the gain was not detected out of domain (XM3600)".

<!-- p:T4 -->**Table 1.** Registered predictions and decision rules. Δ is `ret` − `rand`; "lower bound" is that of the CI of Sect. 4. Registered sensitivities are reported beside a prediction and never replace it: all 2,001 OpenViIC test images; XM-test2500 without the 108 three-reference images (2,392); NoCaps val without the images decoded earlier by another study of the group (3,500).

| name | estimand and set: rule |
|---|---|
| **P1** (primary) | mean pooled Δ_i, stripped CIDEr-D, on OV-test primary: PASS if the point is above +2.0 and the lower bound is above zero |
| rule L | per backbone, relative gap in mean caption length between `ret` and `rand`, on OV-test primary and on the COCO Karpathy test: if above 0.10 for either backbone, a PASS is recorded as "not separated from length" |
| P1b (non-gating) | per-backbone mean Δ_m,i, on OV-test primary: Qwen2.5-VL: "confirmed" if the point is above +2.0; InternVL3: reported only. P1b selects the scope sentence |
| **P2** | per backbone, ΔP_cm of `ret` against `zs`, on OV-test primary: PASS if, for each backbone, the lower bound is above −1.0 |
| **XM-a** | mean pooled Δ_i, stripped CIDEr-D, on XM-test2500: PASS if the lower bound is above zero; a positive point with a CI that includes zero is printed as a descriptive number only |
| **XM-b** | change in verified object precision of `ret` against `zs`, pooled, on XM-test2500: PASS if the lower bound is above −1.0 |
| XM prediction | XM-a and XM-b, on XM-test2500: "confirmed" only if both pass; otherwise "not confirmed" |
| **P1-EN** (primary) | English: mean pooled Δ_i, PTB CIDEr-D, on the COCO Karpathy test: the P1 rule, with rule L |
| **S-NC** (secondary) | English, fixed order: mean pooled Δ_i, PTB CIDEr-D, on NoCaps val: the P1 rule; the transfer claim needs P1-EN and S-NC |
| secondary, InternVL3 at τ = −∞ | per-backbone mean Δ without the deletion step, on every test set: labelled "detected" when the lower bound is above zero; read by no gate |

<!-- p:S4-04 -->**Uncertainty.** CIs come from a paired bootstrap over images, with B = 2,000 resamples and percentile 95% bounds. For a pooled statistic the per-image differences are first averaged over the backbones; for a ratio statistic numerator and denominator are resampled together. Only images are resampled. Each image has one seeded `rand` draw, and document frequencies come from the full scored set, so the CIs describe image-sampling uncertainty conditional on both. Variation from other random draws, or from run to run, is not in them. P1 is the single primary test of the Vietnamese registration, and P1-EN that of the English one, where S-NC is gated after it in a fixed order. P2 is an intersection–union test over the two backbones, and the XM prediction is a conjunction. All other rows carry unadjusted CIs and no family-wise claim, and no error rate is claimed across the two registrations or over the four test sets together. No p-value is reported, because the registered rules are CI-based.

<!-- p:S4-05 -->**One look.** Every test set went through decoding, scoring and the decision step exactly once, at the frozen configuration, and each decision file carries its time. During the runs only counts, times, GPU seconds and return codes were watched.

## 5 Results in Vietnamese

<!-- p:S5-01 -->All differences are paired, with the CIs of Sect. 4. CIDEr-D differences are in stripped CIDEr-D points, P2 in count-matched precision points and XM-b in verified-precision points.

<!-- p:T5 -->**Table 2.** Stripped CIDEr-D per arm on the two Vietnamese test sets, each backbone at its frozen τ.

| set | backbone (τ) | `ret` | `rand` | `fix` † | `zs` |
|---|---|---|---|---|---|
| OV-test primary | Qwen2.5-VL (−∞) | 39.81 | 31.48 | 33.48 | 20.05 |
| OV-test primary | InternVL3 (0.10) | 33.62 | 32.96 | 33.01 | 24.77 |
| XM-test2500 | Qwen2.5-VL (−∞) | 57.70 | 54.56 | 51.83 | 43.74 |
| XM-test2500 | InternVL3 (0.10) | 52.85 | 54.59 | 53.65 | 42.84 |

† Every `fix` row is conditional on the realised fixed set.

<!-- p:T6 -->**Table 3.** Registered Vietnamese results: estimate with its 95% CI, the label as registered, and the registered sensitivity. Scope of every pooled P1 number, as registered: "carried mainly by Qwen2.5-VL; not detected for InternVL3". Rows marked "reported" have no registered rule and unadjusted CIs.

| row | estimate [CI] | label | registered sensitivity |
|---|---|---|---|
| *OpenViIC test, primary set (1,941 images)* | | | *all 2,001 images* |
| **P1**, pooled `ret` − `rand` | **+4.49 [3.52, 5.57]** | **PASS** | +4.46 [3.45, 5.38] |
| P1b, Qwen2.5-VL | +8.33 [7.01, 9.76] | confirmed | +8.29 [6.99, 9.59] |
| P1b, InternVL3 (τ = 0.10) | +0.66 [−0.68, 1.99] | reported only | +0.63 [−0.73, 1.86] |
| secondary, InternVL3 at τ = −∞ | +3.71 [2.29, 5.14] | detected | +3.68 [2.20, 5.05], detected |
| **P2**, Qwen2.5-VL, ΔP_cm against `zs` | **+5.41 [3.88, 7.01]** | **PASS** | +5.34 [3.88, 6.87] |
| **P2**, InternVL3, ΔP_cm against `zs` | **+1.57 [0.65, 2.51]** | **PASS** (both: passed) | +1.35 [0.44, 2.27] |
| rule L, length gap, Qwen2.5-VL / InternVL3 | 0.074 / 0.039 | does not fire | 0.076 / 0.042 |
| *XM-test2500 (2,500 images)* | | | *2,392 images* |
| **XM-a**, pooled `ret` − `rand` | **+0.70 [−0.45, 1.97]** | **FAIL** | +0.82 [−0.45, 2.11] |
| reported, Qwen2.5-VL | +3.15 [1.50, 4.93] | – | – |
| reported, InternVL3 (τ = 0.10) | −1.75 [−3.35, −0.09] | – | – |
| secondary, InternVL3 at τ = −∞ | +0.18 [−1.36, 1.81] | not detected | +0.19 [−1.41, 1.79], not detected |
| **XM-b**, change in verified precision against `zs` | **+0.59 [−0.31, 1.54]** | **PASS** | +0.57 [−0.41, 1.56], PASS |
| **XM prediction** (XM-a and XM-b) | – | **not confirmed** | – |

### 5.1 In the memory's source: OpenViIC test

<!-- p:S5-02 -->**P1: PASS.** On the primary set, retrieved examples scored +4.49 [3.52, 5.57] points above random examples, pooled over the two backbones (Table 3), with the registered scope: "carried mainly by Qwen2.5-VL; not detected for InternVL3". Qwen2.5-VL's row is +8.33 [7.01, 9.76] (P1b: confirmed). InternVL3's row at its frozen τ = 0.10 is +0.66 [−0.68, 1.99]; the CI includes zero, and the row is reported only. Rule L does not fire. The registered sensitivity on all 2,001 images gives the same reading for every row.

<!-- p:S5-03 -->**P2: PASS for both backbones.** Against each model's own zero-shot captions, the retrieval prompt changed count-matched object precision by +5.41 [3.88, 7.01] points for Qwen2.5-VL and by +1.57 [0.65, 2.51] for InternVL3; both lower bounds lie above the −1.0 floor. On OpenViIC test we therefore find no object-precision cost of the full in-context prompt relative to zero-shot. P2 does not compare `ret` with `rand`.

<!-- p:S5-04 -->**InternVL3 without the deletion step.** The registered secondary at τ = −∞ is +3.71 [2.29, 5.14] on the primary set and +3.68 [2.20, 5.05] on all 2,001 images, detected on both, and not detected on XM-test2500 (Table 3); it changes no verdict and no scope sentence. With the frozen step, a share 0.351 of InternVL3's `ret` captions on this set fell back to the zero-shot caption. Stripped CIDEr-D was 33.62, against 39.50 for the same decodes without the step; CHAIR_i was 0.254 against 0.237; the count-matched change against `zs` was +1.57 against +5.80. The step lowered CIDEr-D and improved neither object measure.

<!-- p:S5-05 -->*Post hoc (not registered; no verdict).* After the test, a broader image-similarity rule than the registered filter was applied to the examples shown. It flags 12 of the 1,941 primary queries as having a near-copy of the query image among their `ret` examples (9 of them at the first rank), and 0 queries in `rand`. Without the 12 queries the pooled difference is +4.47 [3.44, 5.41] on 1,929 queries (per-image scores as stored; document frequencies not recomputed), and the P2 rows are +5.34 [3.87, 6.82] for Qwen2.5-VL and +1.61 [0.68, 2.56] for InternVL3. P1 and P2 stand as registered.

### 5.2 Outside the memory's source: XM3600 Vietnamese

<!-- p:S5-06 -->**XM-a: FAIL. The gain was not detected out of domain (XM3600).** The pooled difference is +0.70 [−0.45, 1.97]. The point is above zero, but the rule required a CI above zero and the CI includes zero. Under the registered rule this point is a descriptive number only. The registered sensitivity on 2,392 images is +0.82 [−0.45, 2.11]. Per backbone (reported rows, no registered rule), Qwen2.5-VL gave +3.15 [1.50, 4.93] and InternVL3 at τ = 0.10 gave −1.75 [−3.35, −0.09].

<!-- p:S5-07 -->**XM-b: PASS under its own rule.** Verified object precision of `ret` against `zs` changed by +0.59 [−0.31, 1.54] points. The registered XM prediction needs both XM-a and XM-b, so it is **not confirmed**. We make no transfer claim, and no claim that retrieval keeps object precision on XM3600. The count-matched rows there, which no XM rule reads, are +0.12 [−1.20, 1.49] for Qwen2.5-VL and +0.13 [−0.83, 1.03] for InternVL3; the first lower bound is below the −1.0 used on OpenViIC.

### 5.3 Controls

<!-- p:S5-08 -->**Zero-shot.** The control S-zf, pooled `ret` − `zs`, was registered with an expected size of about +10.0 and no pass label. It is +14.30 [13.38, 15.24] on OV-test and +11.99 [10.68, 13.34] on XM-test2500. A descriptive, post hoc reading of Table 2, with no registered contrast and no CI: random examples from the same memory already score well above zero-shot, for both backbones on both sets.

<!-- p:S5-09 -->**Fixed examples (†: conditional on the realised fixed set).** Pooled `ret` − `fix` is +3.47 [2.54, 4.41] on OV-test and +2.53 [1.32, 3.80] on XM-test2500. For Qwen2.5-VL it is +6.33 [5.02, 7.72] and +5.87 [4.14, 7.65]; for InternVL3 it is +0.61 [−0.68, 1.87] and −0.81 [−2.41, 0.76], two CIs that include zero.

## 6 English comparison

<!-- p:S6-01 -->A separate registration carried the design to English with no English tuning: the frozen configurations of Sect. 3 and the deletion step, with translated prompts and the arms `ret`, `rand` and `zs`. It was written after the Vietnamese verdicts were known and committed before any English image was decoded for this arm; the P1 rule was chosen for NoCaps after the XM-a result (Sect. 7). The decision column is PTB-tokenised CIDEr-D [@Chen2015COCOCaptions], a different scale from the Vietnamese column. The memory is COCO training data [@Lin2014COCO; @Karpathy2015Split], the Karpathy train and restval images after the filter rules of Sect. 3: 112,255 images in 111,927 clusters. The COCO Karpathy test (the full split, 5,000 images) therefore lies in the memory's source and NoCaps val (the full split, 4,500 images) [@Agrawal2019NoCaps] outside it.

<!-- p:T7 -->**Table 4.** Registered and reported English results: pooled and per-backbone `ret` − `rand` in PTB CIDEr-D points with CIs as in Sect. 4. "Reported" rows have no registered rule.

| row | COCO Karpathy test (5,000) | NoCaps val (4,500) | NoCaps val, registered sensitivity (3,500) |
|---|---|---|---|
| **pooled `ret` − `rand`** | **+3.08 [2.08, 4.03]** | **+1.73 [0.94, 2.50]** | +1.62 [0.66, 2.52] |
| label | **P1-EN: PASS** | **S-NC: FAIL** | FAIL |
| reported, Qwen2.5-VL | +7.80 [6.40, 9.17] | +2.83 [1.69, 3.98] | – |
| reported, InternVL3 (τ = 0.10) | −1.64 [−2.79, −0.49] | +0.62 [−0.37, 1.62] | – |
| secondary, InternVL3 at τ = −∞ | −1.05 [−2.22, 0.08], not detected | +1.00 [−0.01, 2.01], not detected | +1.09 [−0.12, 2.21], not detected |
| rule L, length gap, Qwen2.5-VL / InternVL3 | 0.019 / 0.019, does not fire | – | – |

<!-- p:S6-02 -->**P1-EN: PASS.** On the COCO Karpathy test, pooled `ret` − `rand` is +3.08 [2.08, 4.03] PTB CIDEr-D points (Table 4), and rule L does not fire. Per backbone (reported rows, no registered rule), Qwen2.5-VL gave +7.80 [6.40, 9.17] and InternVL3 at τ = 0.10 gave −1.64 [−2.79, −0.49], a CI wholly below zero. *Post hoc (no verdict):* the broader similarity rule of Sect. 5.1 flags 1 of the 5,000 queries; without it the pooled difference is +3.07 [2.08, 4.06] on 4,999 queries.

<!-- p:S6-03 -->**S-NC: FAIL.** On NoCaps val, pooled `ret` − `rand` is +1.73 [0.94, 2.50]. The CI lies above zero, but the point is below the registered +2.0, so the rule fails. The claim that the gain transfers to NoCaps is not made. The registered sensitivity on 3,500 images, +1.62 [0.66, 2.52], is also a FAIL. InternVL3 at τ = −∞ is not detected on COCO or on either NoCaps set (Table 4).

<!-- p:S6-04 -->**Both languages side by side (post hoc; no verdict).** In Table 3 and Table 4 the registered retrieved-against-random predictions passed only where the memory and the test set share a source. Memory source and test set changed together, and Qwen2.5-VL's out-of-source rows stayed above zero, so this is an observation and not a tested cause. No cross-language difference is computed.

## 7 Disclosures and limitations

<!-- p:S7-01 -->**Disclosures.** None of the following changed a configuration, threshold, metric, set or rule after a test output existed.

- <!-- p:S7-D01 -->*Exclusions.* The primary OpenViIC set leaves out 60 images by a pre-specified filter; the full set is printed beside it.
- <!-- p:S7-D02 -->*Earlier contact.* To pin lists, CPU scripts read test-image bytes, annotation keys and reference counts; no caption was used and no model output was computed. Another study had decoded some XM-dev500 images zero-shot (stage B only). In English, a companion study had scored on the COCO Karpathy test, part of that test had been decoded zero-shot earlier, and another study had decoded the NoCaps images that the registered 3,500-image sensitivity removes; none of those outputs is re-used, and no design choice follows from them.
- <!-- p:S7-D03 -->*Timing of the English arm.* It was decided on the Vietnamese test day and registered after the Vietnamese verdicts were known, before any English image was decoded for this arm. Its NoCaps rule, the P1 rule, was fixed after XM-a was known and is stricter than the XM-a rule, so the two out-of-source results answer different rules.
- <!-- p:S7-D04 -->*English SESOI.* The +2.0 was carried over numerically, without recalibration to the PTB scale; because English scores are higher, it is relatively more lenient on COCO.
- <!-- p:S7-D05 -->*English deletion step.* It is a port with another object matcher, and its calibration is untested in English; this is why every τ = −∞ row is printed.
- <!-- p:S7-D06 -->*NoCaps images* were fetched by their Open Images ids, so bytes or resolution may differ.
- <!-- p:S7-D07 -->*English per-backbone row.* The abstract and the contributions quote InternVL3's COCO row as a reported row. The English registration has no bar on this, and the pooled number alone would overstate the effect.
- <!-- p:S7-D08 -->*Post hoc rows.* The rows without the flagged queries (OpenViIC test, COCO) are labelled and carry no verdict.
- <!-- p:S7-D09 -->*Re-use after the look.* An exploratory filtering diagnostic of the same project later re-used test images in a development role; it produced exploratory rows only.
- <!-- p:S7-D10 -->*Operational deviations.* Those of the test runs (a parity check repeated before the test, a code copy pinned at the test commit, a fixed retry rule for truncated image files) changed no configuration, threshold, set or rule.
- <!-- p:S7-D12 -->*Not reported here.* Registered secondaries, none a verdict: the cosine dose-response, the style report, the source share of shown examples, neighbour-only object precision, the copy baselines and the PTB-tokenised column of the Vietnamese sets. Also not printed: the English score of each arm and the NoCaps rows by domain label. Later registrations: a Flickr30K baseline comparison, development ablations, a development attribution analysis, and an exploratory filtering diagnostic that ended by its registered stop rules.

<!-- p:S7-02 -->**Limitations.**

- <!-- p:S7-L01 -->*Two backbones.* The gain is carried mainly by one of them, and the study cannot say which property of a model predicts it.
- <!-- p:S7-L02 -->*Out of the memory's source* both registered predictions failed. Memory source and test set changed together, so the source match is confounded with the test set (Sect. 6).
- <!-- p:S7-L03 -->*Reference-based metric.* CIDEr-D rewards the wording of the references, and the study has no human judgments.
- <!-- p:S7-L04 -->*Object gold.* On OpenViIC the gold is the union of the references, so a correct object that no reference names counts as an error; on XM3600 the verified labels cover the mapped classes only. No object-precision prediction was registered in English.
- <!-- p:S7-L05 -->*One look, one random draw.* Each test set was decoded once, greedily, with one `rand` draw per image.
- <!-- p:S7-L06 -->*Batch composition.* The results are results of the systems as run, in fixed batches. A per-image difference between arms decoded in batches can contain a batch-mate term, and the image bootstrap does not model the coupling of images within a batch slice. A check before the test re-decoded the same development images in the same batches and gave 52/52 identical captions per backbone; it shows run-to-run parity only. A later development check (development, non-confirmatory) decoded 50 items one at a time: 42/50 captions were identical for Qwen2.5-VL and 37/50 for InternVL3. That check rests on string identity; no score was compared.
- <!-- p:S7-L07 -->*Training data.* The backbones' training data are not fully disclosed [@Bai2025Qwen25VL; @Zhu2025InternVL3; @Chen2024InternVL25], and COCO or Open Images data may have been seen. The equal-k `rand` control removes contamination shared by `ret` and `rand`, not contamination that interacts with retrieval.

<!-- p:S7-03 -->**Compute.** The Vietnamese test used 9.59 GPU-hours of a 20-hour cap and the English test 13.22 of a 25-hour cap, each on one 24 GB GPU.

## 8 Conclusion

<!-- p:S8-01 -->In a preregistered one-look test, retrieved example captions beat an equal number of random ones from the same memory where memory and test set share a source: by +4.49 [3.52, 5.57] stripped CIDEr-D points on OpenViIC test (P1 PASS; "carried mainly by Qwen2.5-VL; not detected for InternVL3") and by +3.08 [2.08, 4.03] PTB CIDEr-D points on the COCO Karpathy test (P1-EN PASS; InternVL3's reported row is below zero). On OpenViIC test, the change in count-matched object precision against zero-shot stayed above the registered floor for both models (P2 PASS).

<!-- p:S8-02 -->Outside the memory's source the registered predictions failed. On XM3600 Vietnamese the gain was not detected: +0.70 [−0.45, 1.97], a FAIL under a rule that required a CI above zero, and the XM prediction is not confirmed. On NoCaps val the point, +1.73 [0.94, 2.50], is below the registered +2.0 (FAIL; the registered sensitivity also fails). No transfer claim is made.

<!-- p:S8-03 -->Descriptively, random in-domain examples already score well above zero-shot (Sect. 5.3). Crediting a gain over zero-shot to retrieval needs a random-example control at equal k from the same memory, the result for each backbone, and a check of whether the memory's captions share the target set's source (here an observation, not a tested cause; Sect. 6).

## Ethics and data statement

<!-- p:DECL-01 -->The study uses existing public data sets only, with their released references and labels. No new annotation was made and no human participants were involved. Captions are read at run time, placed only in prompts, and never redistributed. [PI: confirm or drop a sentence on the agreement of the KTVIC and UIT-OpenViIC authors to this use.]

<!-- p:DECL-02 -->Data sets, in short form (source; language; role here). KTVIC [@Pham2024KTVIC]; Vietnamese; memory and stage A. UIT-OpenViIC [@Bui2023OpenViIC]; Vietnamese; memory, development and test. XM3600 [@Thapliyal2022XM3600]; Vietnamese references; development and test. COCO with the Karpathy splits [@Lin2014COCO; @Karpathy2015Split]; English; memory and test. NoCaps val [@Agrawal2019NoCaps]; English; test. Open Images human-verified labels [@Kuznetsova2020OpenImages]; object gold for XM-b. Licence of each set: [PI: one entry per set, as documented by its authors; where nothing is documented, write "not reported by the dataset authors"].

## Data and code availability

<!-- p:DECL-03 -->The registrations with their pinned lists, the test code, the decision files, and the scores, image ids and hashes are available from the authors on request. No caption from any data set, no model caption and no per-image record is released. [PI: decision D9; a public archive with a DOI would replace the first sentence.]

## Acknowledgments

<!-- p:DECL-04 -->[PI: acknowledgments and funding sentence.]

## Disclosure of Interests

<!-- p:DECL-05 -->[PI: statement of the authors' competing interests.]

## References

<!-- Built by pandoc citeproc from paperC.bib (Paper C repo, read-only), numeric LNCS style at build time. The keys used are listed in CHECKS.md. -->
