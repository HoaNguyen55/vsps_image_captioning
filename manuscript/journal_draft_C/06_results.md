## 6. Results

All test numbers come from the three decision files and their ledgers. Section 6.8 is the exception: it uses development data only and is labelled as such. All differences are paired with 95% bootstrap CIs. Units:
- P1, P1b, XM-a and every CIDEr-D difference are in stripped CIDEr-D points;
- P2 is in count-matched precision points;
- XM-b is in verified-precision points.

### 6.1 Absolute scores

**Table 6. Stripped CIDEr-D (×100) per arm, each backbone at its frozen τ.**

| set | backbone (τ) | `ret` | `rand` | `fix` | `zs` |
|---|---|---|---|---|---|
| OV-test primary | Qwen2.5-VL (−∞) | 39.81 | 31.48 | 33.48 | 20.05 |
| OV-test primary | InternVL3 (0.10) | 33.62 | 32.96 | 33.01 | 24.77 |
| XM-test2500 | Qwen2.5-VL (−∞) | 57.70 | 54.56 | 51.83 | 43.74 |
| XM-test2500 | InternVL3 (0.10) | 52.85 | 54.59 | 53.65 | 42.84 |

The copy baselines, which use no model, score 22.73 (NN-top1), 26.17 (NN-consensus, k = 4) and 28.96 (k = 8) on OV-test, and 13.96, 14.61 and 15.39 on XM-test2500. Every other registered per-run row (as-written and PTB CIDEr-D, CHAIR_i, mentions, copy and deletion rates) is in Tables S1–S4.

### 6.2 In domain: OpenViIC test

**Table 7 (main). Registered OpenViIC test results: the primary set and the full set side by side.**

| row | OV-test primary (1,941) | verdict | OV-test full (2,001), registered sensitivity |
|---|---|---|---|
| **P1**, pooled `ret` − `rand` | **+4.49 [3.52, 5.57]** | **PASS** | +4.46 [3.45, 5.38] |
| P1b, Qwen2.5-VL | +8.33 [7.01, 9.76] | confirmed (point > +2.0) | +8.29 [6.99, 9.59] |
| P1b, InternVL3 (τ = 0.10) | +0.66 [−0.68, 1.99] | reported only | +0.63 [−0.73, 1.86] |
| **P2**, Qwen2.5-VL, ΔP_cm vs `zs` | **+5.41 [3.88, 7.01]** | **PASS** (lower bound > −1.0) | +5.34 [3.88, 6.87] |
| **P2**, InternVL3, ΔP_cm vs `zs` | **+1.57 [0.65, 2.51]** | **PASS** (lower bound > −1.0) | +1.35 [0.44, 2.27] |
| length gap, Qwen2.5-VL (\|ret − rand\| / rand) | 0.074 | L does not fire (≤ 0.10) | 0.076 |
| length gap, InternVL3 | 0.039 | L does not fire | 0.042 |

Scope sentence for every pooled P1 number in this table (registered mapping, Table 5): **carried mainly by Qwen2.5-VL; not detected for InternVL3**.<!-- scope row: qwen_main_internvl_not_detected -->

**P1: PASS.** Retrieved examples beat random examples on the OpenViIC test by +4.49 [3.52, 5.57] stripped CIDEr-D points, pooled over the two backbones. The effect is **carried mainly by Qwen2.5-VL and not detected for InternVL3** (the registered scope sentence). Rule L does not fire on the primary set. Mean caption length was:
- Qwen2.5-VL: 18.47 syllables for `ret` against 17.20 for `rand`;
- InternVL3: 17.02 against 17.72.

On the full 2,001 images the pooled difference is +4.46 [3.45, 5.38], again carried mainly by Qwen2.5-VL and not detected for InternVL3. The primary set decides.

**P1b.** For Qwen2.5-VL the per-backbone difference is +8.33 [7.01, 9.76], above the SESOI, so the registered P1b prediction is confirmed. For InternVL3 at its frozen τ = 0.10 it is +0.66 [−0.68, 1.99], a CI that includes zero. This row carries no prediction. Because InternVL3's registered arm includes the deletion step, the registered secondary without it is shown here too, labelled secondary (Table 13): at τ = −∞ InternVL3's `ret` − `rand` on OV-test is +3.71 [2.29, 5.14], detected, while on COCO it is −1.05 [−2.22, 0.08], not detected (Section 8.2). It changes no verdict.

**P2: PASS for Qwen2.5-VL and PASS for InternVL3** (both: passed). Against each model's own zero-shot captions, `ret` changed count-matched object precision by +5.41 [3.88, 7.01] points for Qwen2.5-VL and +1.57 [0.65, 2.51] for InternVL3. Both lower bounds lie above the −1.0 floor and also above zero. On OpenViIC test, then, we find no object-precision cost relative to zero-shot from the full in-context prompt, for either backbone. This statement is limited to OpenViIC test, and P2 does not compare `ret` with `rand`. *Descriptive, post hoc:* the difference between the registered `ret` and `rand` ΔP_cm values (Table S1) is +2.59 for Qwen2.5-VL (5.41 − 2.82) and +0.17 for InternVL3 (1.57 − 1.40). This is a difference of two values against `zs`, with no CI, and not a count-matched `ret`-against-`rand` comparison, because the matched counts differ between runs.

### 6.3 Out of domain: XM3600 Vietnamese

**Table 8. Registered XM-test2500 results.**

| row | XM-test2500 (2,500) | verdict | without three-reference images (2,392), registered sensitivity |
|---|---|---|---|
| **XM-a**, pooled `ret` − `rand` | **+0.70 [−0.45, 1.97]** | **FAIL** (CI includes 0) | +0.82 [−0.45, 2.11] |
| per backbone, Qwen2.5-VL | +3.15 [1.50, 4.93] | reported row, no registered rule, unadjusted CI | +3.39 [1.55, 5.16] |
| per backbone, InternVL3 (τ = 0.10) | −1.75 [−3.35, −0.09] | reported row, no registered rule, unadjusted CI | −1.74 [−3.39, 0.01] |
| **XM-b**, Δ verified precision `ret` vs `zs`, pooled | **+0.59 [−0.31, 1.54]** | **PASS** (lower bound > −1.0) | +0.57 [−0.41, 1.56] (PASS) |
| **XM prediction** (XM-a ∧ XM-b) | | **not confirmed** (XM-a FAIL) | |
| ΔP_cm vs `zs`, Qwen2.5-VL (reported row, no XM rule) | +0.12 [−1.20, 1.49] | | +0.19 [−1.19, 1.55] |
| ΔP_cm vs `zs`, InternVL3 (reported row, no XM rule) | +0.13 [−0.83, 1.03] | | +0.13 [−0.81, 1.06] |

**XM-a: FAIL. The gain was not detected out of domain (XM3600).** The pooled difference is +0.70 [−0.45, 1.97]: the point estimate is above zero, but the CI includes zero. Under the registered rule this point is a descriptive number only, and nothing about it is confirmed. Without the three-reference images the difference is +0.82 [−0.45, 2.11], which changes nothing.

**Per backbone** (reported rows; no per-backbone XM3600 rule was registered). Qwen2.5-VL: +3.15 [1.50, 4.93] (unadjusted CI). InternVL3 at its frozen τ: −1.75 [−3.35, −0.09] (per-backbone reported row, no registered rule, unadjusted CI; 2,392-image sensitivity −1.74 [−3.39, 0.01]). Rule L is defined on the 1,941; on XM-test2500 the length gaps are reported only (0.062 and 0.028).

**XM-b: PASS under its own rule; the XM prediction is not confirmed.** Pooled over mentions and backbones, verified object precision of `ret` against `zs` changed by +0.59 [−0.31, 1.54] points, with the lower bound above the −1.0 floor. The registered XM prediction is the conjunction of XM-a and XM-b. Since XM-a is FAIL, the prediction is **not confirmed**.

We therefore make no claim that the gain transfers to XM3600, and no claim that retrieval keeps object precision there. The count-matched rows on XM3600 are reported with no rule attached. For Qwen2.5-VL that row's lower bound (−1.20) lies below the −1.0 value used on OpenViIC.

The memory holds no XM3600 captions: the source-dataset share of shown examples is 0.000 for both backbones. XM-test2500 is therefore a test of retrieval from a memory in another domain and another reference style. It is not a test of in-domain retrieval on a second dataset.

### 6.4 Controls: zero-shot, fixed examples and copy baselines

**Table 9. S-zf and copy baselines (`ret` minus the named comparison), primary scored sets.**

| comparison | OV-test, pooled | OV Qwen2.5-VL | OV InternVL3 | XM, pooled | XM Qwen2.5-VL | XM InternVL3 |
|---|---|---|---|---|---|---|
| vs `zs` | +14.30 [13.38, 15.24] | +19.76 [18.33, 21.10] | +8.85 [7.76, 9.98] | +11.99 [10.68, 13.34] | +13.96 [12.09, 15.87] | +10.01 [8.41, 11.62] |
| vs `fix` | +3.47 [2.54, 4.41] | +6.33 [5.02, 7.72] | +0.61 [−0.68, 1.87] | +2.53 [1.32, 3.80] | +5.87 [4.14, 7.65] | −0.81 [−2.41, 0.76] |
| vs NN-top1 | +13.98 [12.63, 15.38] | +17.08 [15.57, 18.72] | +10.89 [9.31, 12.51] | +41.32 [39.52, 43.08] | +43.75 [41.59, 46.04] | +38.89 [36.95, 40.83] |
| vs NN-consensus | +9.15 [7.84, 10.47] | +10.85 [9.22, 12.47] | +7.45 [5.90, 9.05] | +40.28 [38.50, 42.08] | +42.32 [40.17, 44.62] | +38.24 [36.25, 40.28] |

**S-zf.** The registered expectation for `ret` − `zs` was about +10.0 pooled, and S-zf has no pass label. The observed value was +14.30 [13.38, 15.24] on OV-test and +11.99 [10.68, 13.34] on XM-test2500.

The `rand` − `zs` comparison is descriptive and post hoc (Table 6; no registered contrast or CI): random examples from the same memory already score well above zero-shot for both backbones on both sets. The registered rows behind this are S-zf `ret` − `zs` +14.30 [13.38, 15.24] against P1 `ret` − `rand` +4.49 [3.52, 5.57] on OV-test.

Against fixed examples, Qwen2.5-VL gained on both sets. InternVL3's difference had a CI that includes zero on both sets: +0.61 [−0.68, 1.87] on OV-test and −0.81 [−2.41, 0.76] on XM-test2500.

**Copy baselines.** Both backbones with retrieved examples score well above the captions they could have copied, on both sets. The model is therefore not simply returning its neighbours' captions. The near-verbatim copy share of `ret` captions on OV-test was 0.015 for Qwen2.5-VL and 0.002 for InternVL3.

### 6.5 PTB column, dose-response and style

**PTB-tokenised CIDEr-D.** The pooled `ret` − `rand` was:
- OV-test: +4.91 [3.93, 6.00] (Qwen2.5-VL +9.31 [7.94, 10.80], InternVL3 +0.51 [−0.81, 1.87]);
- XM-test2500: +0.60 [−0.54, 1.85] (Qwen2.5-VL +3.17 [1.50, 4.99], InternVL3 −1.97 [−3.59, −0.31]).

The PTB column agrees in sign and scope with the stripped column on both sets.

**Table 10. Dose-response: pooled `ret` − `rand` within tertiles of the query's nearest eligible-cluster cosine (cuts per scored set).**

| set | cuts | low | mid | high |
|---|---|---|---|---|
| OV-test primary | 0.802, 0.865 | +4.40 [2.84, 6.03] (n = 647) | +2.95 [1.14, 4.79] | +6.13 [4.36, 7.87] |
| XM-test2500 | 0.624, 0.680 | +1.64 [−0.31, 3.69] (n = 833) | +2.28 [0.13, 4.48] | −1.82 [−3.96, 0.27] (n = 834) |

The OV-test tertiles show no monotone pattern. The XM-test2500 cosine cuts lie well below the OV-test cuts, which is consistent with a memory from another domain. The XM-test2500 high tertile has the lowest point estimate. These rows are reported and non-gating; Section 8.4 uses them only as a limit on a post-hoc reading.

**Table 11. Style report and source-dataset share, OV-test primary.**

| backbone | arm | mean syllables | ends in punctuation | top-3 opening share | source-dataset share |
|---|---|---|---|---|---|
| Qwen2.5-VL | `ret` | 18.47 | 0.994 | 0.350 | 0.996 |
| Qwen2.5-VL | `rand` | 17.20 | 0.997 | 0.357 | 0.995 |
| Qwen2.5-VL | `fix` | 18.20 | 0.995 | 0.417 | 1.000 |
| InternVL3 | `ret` | 17.02 | 0.880 | 0.154 | 0.996 |
| InternVL3 | `rand` | 17.72 | 0.869 | 0.176 | 0.994 |
| InternVL3 | `fix` | 17.94 | 0.778 | 0.205 | 1.000 |

The source-dataset share is the share of shown examples that come from a cluster with an OpenViIC member. It is near one for every arm, so `rand` and `fix` also show in-domain captions, as the design intends. The XM-test2500 style rows, and the rows for the full OV-test and the 2,392-image XM sensitivity, are in Table S6.

### 6.6 Neighbour-only objects and the deletion step

**Neighbour-only object precision** is the precision of the objects that a caption takes only from its examples (Section 3.4). It is a named secondary and not a co-primary.

On OV-test, scored against reference gold, it was:
- Qwen2.5-VL: 73.41 [71.27, 75.34], over 1,933 mentions, with 0.630 of images having at least one;
- InternVL3: 77.44 [70.99, 84.02], over 164 mentions, with a share of 0.079;
- pooled: 73.72 [71.72, 75.64].

On XM-test2500, scored offline against the verified Open Images labels, it was:
- Qwen2.5-VL: 92.82 [89.03, 96.28], over 195 mentions;
- InternVL3: 100.00, that is 16/16 verified; the CI is not informative (16 mentions);
- pooled: 93.36 [89.87, 96.59].

The InternVL3 counts are much smaller than Qwen2.5-VL's. This is consistent with its registered captions having already passed the deletion step.

**What the deletion step did to InternVL3.** At InternVL3's frozen τ = 0.10 on OV-test, `ret` had 0.636 classes rejected per image. 0.122 of captions were edited by deletion and 0.351 fell back to the zero-shot caption. Its stripped CIDEr-D was 33.62, against 39.50 for the same decodes with no deletion (both rows registered). For `rand` the corresponding values were 32.96 and 35.80. On the other registered measures the step also did worse than no deletion for `ret` on OV-test (Table S1): CHAIR_i 0.254 against 0.237, and ΔP_cm against `zs` +1.57 against +5.80. On this test set the frozen step therefore lowered CIDEr-D without improving either object measure.

### 6.7 The guard, stage B, and the secondary motivated by stage B

**The guard is a registered negative.** At stage B the guard hypothesis H_G was not passed (stage-B decision file, `ov_dev_b.H_G.passed`). The pooled precision change was +2.91 [0.46, 5.31], with a stripped CIDEr-D cost (`ret` at τ_G minus `ret` at −∞, pooled) of −4.01. For InternVL3, the count of neighbour-only mentions went from 714 to 80. There is no test hypothesis about the guard and no test guard claim. InternVL3's τ = 0.10 was chosen on KTVIC dev299 and kept unchanged.

**Table 12. Stage B results, for the reader only; they set nothing at test.**

| row | OV-dev-B (925) | XM-dev500 (500) |
|---|---|---|
| pooled `ret` − `rand` | +6.04 [4.54, 7.58] (gate PASS) | +1.46 [−1.07, 4.17] |
| Qwen2.5-VL | +9.67 [7.68, 11.72] | +4.44 [0.98, 7.85] |
| InternVL3 (τ = 0.10) | +2.41 [0.57, 4.26] | −1.52 [−5.41, 2.51] |

**Table 13. Secondary, motivated by stage B (post hoc at stage B, pre-specified at test): InternVL3 `ret` − `rand` at τ = −∞. The τ = 0.10 column holds per-backbone reported rows with unadjusted CIs.**

| set | InternVL3, registered τ = 0.10 (shown first) | InternVL3, τ = −∞ (secondary) | label |
|---|---|---|---|
| OV-test primary | +0.66 [−0.68, 1.99] | +3.71 [2.29, 5.14] | detected |
| OV-test full | +0.63 [−0.73, 1.86] | +3.68 [2.20, 5.05] | detected |
| XM-test2500 | −1.75 [−3.35, −0.09] | +0.18 [−1.36, 1.81] | not detected |
| XM-test2500 without three-reference images | −1.74 [−3.39, 0.01] | +0.19 [−1.41, 1.79] | not detected |

This row changes no verdict and no scope sentence. InternVL3's registered result is the τ = 0.10 column. On OV-test, the same decodes without the deletion step show a detected `ret` − `rand` difference for InternVL3. On XM-test2500 they do not.

**Table 14. Stage-B decomposition of InternVL3's contrast (post hoc, development data only; not a test result).** Recomputed on CPU from the stage-B ledger with the registered bootstrap. The τ = 0.10 column reproduces the stage-B decision file exactly, and the build asserts it.

| set | `ret` − `rand` at τ = 0.10 (registered) | `ret` − `rand` at τ = −∞ | `ret`: τ = 0.10 minus τ = −∞ | `rand`: τ = 0.10 minus τ = −∞ |
|---|---|---|---|---|
| OV-dev-B (925) | +2.41 [0.57, 4.26] | +5.36 [3.53, 7.12] | −5.43 [−6.76, −4.08] | −2.48 [−3.44, −1.51] |
| XM-dev500 (500) | −1.52 [−5.41, 2.51] | +1.54 [−2.12, 5.25] | −5.08 [−7.64, −2.77] | −2.02 [−3.26, −0.85] |

At stage B, the deletion step lowered InternVL3's `ret` scores more than its `rand` scores on both development sets. This is a description of development data and is not tested here.

### 6.8 A development-set diagnostic of the backbone dependence

> **Development data only (OV-dev-B, 925 images): a mechanism analysis, non-confirmatory.** The three ablations below were registered on their own, after the test, and run once on the stage-B set. They change no verdict of Sections 6.2–6.7 or of Section 8. They reinterpret neither P1b for InternVL3, nor XM-a, nor the guard negative. They enter neither the abstract nor the contributions.

The registered results leave one question open: why is the in-domain gain carried by Qwen2.5-VL and not detected for InternVL3? Three ablations address it on OV-dev-B. Each holds both backbones at their frozen configurations (Table 2) and varies one factor:
- **AB-τ**, the deletion threshold, for InternVL3 only;
- **AB-K**, the number of examples k;
- **AB-M**, the memory size.

The scorer, the stripped CIDEr-D column and the paired bootstrap (B = 2,000, one index matrix) are those of stage B. Before any new decode, the job reproduced the four published stage-B rows (Tables 12 and 14). Its run details are in the supplement (Table S14).

Three disclosures bound what this section shows:
1. **The set is not fresh.** OV-dev-B is the set of the stage-B gate, so its stage-B rows were known.
2. **Two of the six τ points were known.** The τ = −∞ and τ = 0.10 points of AB-τ, and the deletion costs at τ = 0.10, were published in Table 14 before AB-τ was registered. Only the four other points are new.
3. **The k prediction is not blind.** Stage A chose Qwen2.5-VL's k = 8 on KTVIC dev299, so the registered k prediction carries the label "shaped by stage-A dev299 selection".

**Table 15. AB-τ: InternVL3 `ret` − `rand` on OV-dev-B at each deletion threshold (stage-B decodes, re-scored on CPU). Registered prediction P-τ: HOLDS.**

| τ | `ret` − `rand` | deletion cost on `ret` (vs τ = −∞) | deletion cost on `rand` | `ret` captions that fall back to zero-shot | `rand` captions that fall back |
|---|---|---|---|---|---|
| −∞ (no deletion) | +5.36 [3.53, 7.12] | — | — | 0.000 | 0.000 |
| 0.00 | +4.75 [2.96, 6.62] | −0.81 [−1.39, −0.32] | −0.21 [−0.50, 0.07] | 0.063 | 0.034 |
| **0.10 (frozen)** | **+2.41 [0.57, 4.26]** | −5.43 [−6.76, −4.08] | −2.48 [−3.44, −1.51] | 0.344 | 0.182 |
| 0.20 | +2.15 [0.35, 3.97] | −5.83 [−7.19, −4.49] | −2.63 [−3.61, −1.63] | 0.362 | 0.187 |
| 0.30 | +1.90 [0.07, 3.74] | −6.04 [−7.44, −4.72] | −2.59 [−3.58, −1.59] | 0.383 | 0.187 |
| +∞ (every neighbour-only class rejected) | +1.45 [−0.35, 3.25] | | | 0.389 | 0.186 |

**The deletion step taxes retrieved examples more than random ones.** InternVL3's contrast falls steadily as τ rises: from +5.36 [3.53, 7.12] with no deletion, to +2.41 [0.57, 4.26] at its frozen τ = 0.10, to +1.45 [−0.35, 3.25] when every candidate class is rejected (Table 15). All three parts of P-τ held. The reason is visible in the step's input. Retrieved examples introduce more neighbour-only objects than random ones do: 0.340 of the object classes in InternVL3's `ret` captions were neighbour-only, against 0.152 with `rand`. The step therefore edits or reverts more `ret` captions: at τ = 0.10, 0.344 of `ret` captions fell back to zero-shot, against 0.182 of `rand` captions. Before deletion, the neighbour-only objects of `ret` captions had a reference-gold precision of 77.31 (714 mentions), against 73.50 for `rand` (317 mentions). Much of what the step removes from `ret` captions is therefore supported by the references, and CIDEr-D falls with it.

**k and memory size (rows in Table S14).** Qwen2.5-VL's contrast grows with k, from +6.41 [4.46, 8.49] at k = 2 to +9.67 [7.68, 11.72] at k = 8 (P-K held), while InternVL3's stays between +1.93 and +2.41 at τ = 0.10, where the deletion step has already acted, so its k rows cannot separate uptake from deletion. Shrinking the memory to 10% of its clusters lowered the pooled contrast by −2.83 [−4.18, −1.58] (P-M held), a pattern carried by Qwen2.5-VL.

**What the ablations show, and what they do not.** The registration allowed this section to say that the ablations explain the backbone dependence, and its condition held (P-τ parts (i) and (ii) hold, and P-M is not failed). That permission is not used here, because the ablations do not isolate a property of the backbone. On OV-dev-B only, the frozen deletion step accounts for about 2.95 of InternVL3's `ret` − `rand` shortfall: the contrast is +5.36 [3.53, 7.12] without the step and +2.41 [0.57, 4.26] with it. The step removes more from retrieved-example captions than from random-example ones, and much of what it removes is supported by the references. Even without the step, InternVL3's contrast at its own k = 4, order and tail is below Qwen2.5-VL's +9.67 [7.68, 11.72] at k = 8, and the two configurations differ in k, order and tail, so this is not a clean contrast between the models. The ablations are consistent with, but do not establish, a backbone account, and whether InternVL3 also takes up less of the examples is not settled. This is a development-set description, not a test result, and it does not carry to every test set:
- On OV-test, InternVL3's registered secondary at τ = −∞ is detected (+3.71 [2.29, 5.14], Table 13), as the first part would lead one to expect.
- On XM-test2500 (+0.18 [−1.36, 1.81]), COCO (−1.05 [−2.22, 0.08]) and NoCaps (+1.00 [−0.01, 2.01]), it is not detected. Outside in-domain Vietnamese, removing the deletion step does not restore a gain for InternVL3.

**Post-hoc remark (not registered, not a claim).** On OV-dev-B, random in-domain examples already lift both backbones well above zero-shot. `rand` − `zs` is +10.38 [8.71, 12.00] for Qwen2.5-VL and +7.43 [6.03, 8.93] for InternVL3, and +8.91 [7.70, 10.16] pooled. Seeing any in-domain captions explains a large part of the gain over zero-shot, and retrieval adds to it mainly for Qwen2.5-VL.

Supplement Table S14 gives every row the ablations wrote.

### 6.9 Compute

The test used 9.59 GPU-hours of the 20 GPU-hour cap, on one 24 GB GPU:
- the OpenViIC block: 4.61 GPU-hours (16,597 s);
- the XM3600 block: 4.90 (17,646 s);
- the decode-parity checks before the test: 0.08 (supplement, "Test-run operations").

Verified precision and all decision steps ran on CPU. The development stages used 6.84 and 4.91 GPU-hours, under a separate development cap.
