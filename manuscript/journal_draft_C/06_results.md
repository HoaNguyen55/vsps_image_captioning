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

The copy baselines, which use no model, score 22.73 (NN-top1), 26.17 (NN-consensus, k = 4) and 28.96 (k = 8) on OV-test, and 13.96, 14.61 and 15.39 on XM-test2500. Every other registered per-run row is in Tables S1–S4.

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

**P1: PASS.** Retrieved examples beat random examples on the OpenViIC test by +4.49 [3.52, 5.57] stripped CIDEr-D points, pooled over the two backbones. The effect is **carried mainly by Qwen2.5-VL and not detected for InternVL3** (the registered scope sentence). Rule L does not fire on the primary set: mean caption length was 18.47 syllables for `ret` against 17.20 for `rand` (Qwen2.5-VL) and 17.02 against 17.72 (InternVL3). On the full 2,001 images the pooled difference is +4.46 [3.45, 5.38], with the same scope. The primary set decides.

**P1b.** For Qwen2.5-VL the per-backbone difference is +8.33 [7.01, 9.76], above the SESOI, so the registered P1b prediction is confirmed. For InternVL3 at its frozen τ = 0.10 it is +0.66 [−0.68, 1.99], a CI that includes zero. This row carries no prediction. Because InternVL3's registered arm includes the deletion step, the registered secondary without it is shown in Table 9: at τ = −∞ InternVL3's `ret` − `rand` on OV-test is +3.71 [2.29, 5.14], detected, while on COCO it is −1.05 [−2.22, 0.08], not detected (Section 8.2). It changes no verdict.

**P2: PASS for Qwen2.5-VL and PASS for InternVL3** (both: passed). Against each model's own zero-shot captions, `ret` changed count-matched object precision by +5.41 [3.88, 7.01] points for Qwen2.5-VL and +1.57 [0.65, 2.51] for InternVL3. Both lower bounds lie above the −1.0 floor and also above zero. On OpenViIC test, then, we find no object-precision cost relative to zero-shot from the full in-context prompt, for either backbone. P2 does not compare `ret` with `rand`. *Descriptive, post hoc:* the difference between the registered `ret` and `rand` ΔP_cm values (Table S1) is +2.59 for Qwen2.5-VL (5.41 − 2.82) and +0.17 for InternVL3 (1.57 − 1.40); it has no CI and is not a count-matched comparison, because the matched counts differ between runs.

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

**XM-a: FAIL. The gain was not detected out of domain (XM3600).** The pooled difference is +0.70 [−0.45, 1.97]: the point estimate is above zero, but the CI includes zero. Under the registered rule this point is a descriptive number only. Without the three-reference images the difference is +0.82 [−0.45, 2.11], which changes nothing. Per backbone (reported rows, unadjusted CIs, no registered rule), Qwen2.5-VL gave +3.15 [1.50, 4.93] and InternVL3 at its frozen τ −1.75 [−3.35, −0.09]. Rule L is defined on the 1,941; on XM-test2500 the length gaps are reported only (0.062 and 0.028).

**XM-b: PASS under its own rule; the XM prediction is not confirmed.** Pooled over mentions and backbones, verified object precision of `ret` against `zs` changed by +0.59 [−0.31, 1.54] points, with the lower bound above the −1.0 floor. The registered XM prediction is the conjunction of XM-a and XM-b, so it is **not confirmed**. We make no claim that the gain transfers to XM3600, and no claim that retrieval keeps object precision there; for Qwen2.5-VL the count-matched row's lower bound (−1.20) lies below the −1.0 value used on OpenViIC.

The memory holds no XM3600 captions (source-dataset share 0.000), so XM-test2500 tests retrieval from a memory in another domain and reference style.

### 6.4 Controls: zero-shot, fixed examples and copy baselines

Table S5 gives every control row with its CI on all four scored sets.

**S-zf.** The registered expectation for `ret` − `zs` was about +10.0 pooled, and S-zf has no pass label. The observed value was +14.30 [13.38, 15.24] on OV-test and +11.99 [10.68, 13.34] on XM-test2500. The `rand` − `zs` comparison is descriptive and post hoc (Table 6; no registered contrast or CI): random examples from the same memory already score well above zero-shot for both backbones on both sets.

**Fixed examples.** Pooled `ret` − `fix` was +3.47 [2.54, 4.41] on OV-test and +2.53 [1.32, 3.80] on XM-test2500. Qwen2.5-VL gained on both sets (+6.33 [5.02, 7.72] and +5.87 [4.14, 7.65]); InternVL3's CI included zero on both (+0.61 [−0.68, 1.87] and −0.81 [−2.41, 0.76]).

**Copy baselines.** Pooled `ret` exceeded NN-top1 by +13.98 [12.63, 15.38] and NN-consensus by +9.15 [7.84, 10.47] on OV-test, and by +41.32 [39.52, 43.08] and +40.28 [38.50, 42.08] on XM-test2500, for both backbones. The model is therefore not simply returning its neighbours' captions. The near-verbatim copy share of `ret` captions on OV-test was 0.015 for Qwen2.5-VL and 0.002 for InternVL3.

### 6.5 PTB column, dose-response and style

**PTB-tokenised CIDEr-D.** The pooled `ret` − `rand` was +4.91 [3.93, 6.00] on OV-test and +0.60 [−0.54, 1.85] on XM-test2500, in sign and scope the same as the stripped column (per-backbone rows in Table S5).

**Dose-response** (Table S7, tertiles of the query's nearest eligible-cluster cosine). The OV-test tertiles show no monotone pattern: +4.40 [2.84, 6.03], +2.95 [1.14, 4.79] and +6.13 [4.36, 7.87]. On XM-test2500 the cuts (0.624, 0.680) lie well below those of OV-test (0.802, 0.865), consistent with a memory from another domain, and the high tertile has the lowest point (+1.64 [−0.31, 3.69], +2.28 [0.13, 4.48], −1.82 [−3.96, 0.27]). These rows are non-gating; Section 8.4 uses them only as a limit on a post-hoc reading.

**Style** (Table S6). The share of shown examples from a cluster with an OpenViIC member is near one for every arm (0.994–1.000 on OV-test), so `rand` and `fix` also show in-domain captions, as the design intends. Length, final punctuation and opening share per arm are in Table S6.

### 6.6 Neighbour-only objects and the deletion step

**Neighbour-only object precision** (a named secondary; Section 3.4; Table S8) on OV-test, against reference gold, was 73.41 [71.27, 75.34] for Qwen2.5-VL (1,933 mentions), 77.44 [70.99, 84.02] for InternVL3 (164 mentions) and 73.72 [71.72, 75.64] pooled. On XM-test2500, against the verified Open Images labels, it was 92.82 [89.03, 96.28] for Qwen2.5-VL (195 mentions), 16/16 verified for InternVL3 (CI not informative) and 93.36 [89.87, 96.59] pooled.

**What the deletion step did to InternVL3.** At τ = 0.10 on OV-test, `ret` had 0.636 classes rejected per image; 0.122 of captions were edited and 0.351 fell back to the zero-shot caption. Its stripped CIDEr-D was 33.62, against 39.50 for the same decodes with no deletion (both rows registered); for `rand`, 32.96 and 35.80. The step also did worse than no deletion on the object measures (Table S1): CHAIR_i 0.254 against 0.237, and ΔP_cm against `zs` +1.57 against +5.80. On this test set the frozen step lowered CIDEr-D without improving either object measure.

### 6.7 The guard, stage B, and the secondary motivated by stage B

**The guard is a registered negative.** At stage B the guard hypothesis H_G was not passed (stage-B decision file, `ov_dev_b.H_G.passed`): pooled precision change +2.91 [0.46, 5.31], at a stripped CIDEr-D cost of −4.01. There is no test guard claim. InternVL3's τ = 0.10 was chosen on KTVIC dev299 and kept unchanged. The stage-B gate passed on OV-dev-B, pooled `ret` − `rand` +6.04 [4.54, 7.58]; the per-backbone rows, XM-dev500 and a decomposition of InternVL3's contrast by deletion step are in Tables S16–S17 (development data; they set nothing at test).

**Table 9. Secondary, motivated by stage B (post hoc at stage B, pre-specified at test): InternVL3 `ret` − `rand` at τ = −∞. The τ = 0.10 column holds per-backbone reported rows with unadjusted CIs.**

| set | InternVL3, registered τ = 0.10 (shown first) | InternVL3, τ = −∞ (secondary) | label |
|---|---|---|---|
| OV-test primary | +0.66 [−0.68, 1.99] | +3.71 [2.29, 5.14] | detected |
| OV-test full | +0.63 [−0.73, 1.86] | +3.68 [2.20, 5.05] | detected |
| XM-test2500 | −1.75 [−3.35, −0.09] | +0.18 [−1.36, 1.81] | not detected |
| XM-test2500 without three-reference images | −1.74 [−3.39, 0.01] | +0.19 [−1.41, 1.79] | not detected |

This row changes no verdict and no scope sentence. On OV-test, the same decodes without the deletion step show a detected `ret` − `rand` difference for InternVL3; on XM-test2500 they do not.

### 6.8 A development-set diagnostic of the backbone dependence

> **Development data only (OV-dev-B, 925 images): a mechanism analysis, non-confirmatory.** The three ablations were registered after the test and run once on the stage-B set. They change no verdict of Sections 6.2–6.7 or of Section 8, and they enter neither the abstract nor the contributions.

Three ablations ask why the in-domain gain is carried by Qwen2.5-VL and not detected for InternVL3. They hold both backbones at their frozen configurations (Table 2) and vary one factor each: the deletion threshold (AB-τ, InternVL3 only), the number of examples k (AB-K) and the memory size (AB-M). The set is not fresh, two of the six τ points were published before AB-τ was registered, and the k prediction is labelled "shaped by stage-A dev299 selection"; the supplement gives these disclosures in full and every row (Table S14).

**The deletion step taxes retrieved examples more than random ones (P-τ: HOLDS).** InternVL3's contrast falls as τ rises: +5.36 [3.53, 7.12] with no deletion, +2.41 [0.57, 4.26] at its frozen τ = 0.10, and +1.45 [−0.35, 3.25] when every candidate class is rejected. Retrieved examples introduce more neighbour-only objects (0.340 of the classes in InternVL3's `ret` captions, against 0.152 with `rand`), so at τ = 0.10 the step reverts 0.344 of `ret` captions to zero-shot against 0.182 of `rand` captions. Before deletion those objects had a reference-gold precision of 77.31 (714 mentions) for `ret`: much of what the step removes is supported by the references.

**k and memory size (P-K and P-M: HOLD).** Qwen2.5-VL's contrast grows with k, from +6.41 [4.46, 8.49] at k = 2 to +9.67 [7.68, 11.72] at k = 8; InternVL3's stays between +1.93 and +2.41 after deletion, so its k rows cannot separate uptake from deletion. Shrinking the memory to 10% of its clusters lowered the pooled contrast by −2.83 [−4.18, −1.58], a pattern carried by Qwen2.5-VL.

**What the ablations show, and what they do not.** The registration allowed this section to say that the ablations explain the backbone dependence, and its condition held; that permission is not used, because the ablations do not isolate a property of the backbone. On OV-dev-B only, the frozen deletion step accounts for about 2.95 of InternVL3's `ret` − `rand` shortfall (+5.36 → +2.41). Even without the step InternVL3's contrast stays below Qwen2.5-VL's +9.67 [7.68, 11.72], under configurations that differ in k, order and tail, so the ablations are consistent with, but do not establish, a backbone account. The account does not carry beyond in-domain Vietnamese: InternVL3's registered τ = −∞ secondary is detected on OV-test (+3.71 [2.29, 5.14], Table 9) but not on XM-test2500 (+0.18 [−1.36, 1.81]), COCO (−1.05 [−2.22, 0.08]) or NoCaps (+1.00 [−0.01, 2.01]).

*Post-hoc remark (not registered, not a claim).* On OV-dev-B, `rand` − `zs` is +8.91 [7.70, 10.16] pooled: seeing any in-domain captions explains a large part of the gain over zero-shot, and retrieval adds to it mainly for Qwen2.5-VL.

### 6.9 Compute

The test used 9.59 GPU-hours of the 20 GPU-hour cap on one 24 GB GPU (OpenViIC block 4.61, XM3600 block 4.90, pre-test decode-parity checks 0.08). Verified precision and all decision steps ran on CPU. The development stages used 6.84 and 4.91 GPU-hours under a separate cap.
