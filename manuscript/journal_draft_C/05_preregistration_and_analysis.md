## 5. Preregistration and analysis plan

**Box 1. Glossary of terms used from here on.**

| term | meaning |
|---|---|
| `ret`, `rand`, `fix`, `zs` | retrieved examples; random examples at equal k from the same memory; one fixed example set for all images; zero-shot (Section 3.2) |
| stage A, stage B | development stages: configuration choice (KTVIC dev299, OV-dev-A) and a one-look gate (OV-dev-B, XM-dev500) |
| OV-test primary, XM-test2500 | the Vietnamese test sets (Table 3) |
| P1, P1b, P2, XM-a, XM-b | registered Vietnamese predictions (Table 4) |
| P1-EN, S-NC | registered English predictions (Table 16) |
| SESOI | smallest effect size of interest, +2.0 CIDEr-D points |
| stripped CIDEr-D | CIDEr-D with trailing punctuation tokens removed (Section 3.6) |
| ΔP_cm | change in count-matched object precision against the same model's zero-shot caption (Table 4) |
| neighbour-only object | an object named in the caption, absent from the zero-shot caption, and present in a shown example (Section 3.4) |
| τ | deletion threshold of the post-decode step (Section 3.4); τ = −∞ means no deletion |
| H_G | the stage-B guard hypothesis, a registered negative (Section 6.7) |
| AB-τ, AB-K, AB-M | development-only ablations of τ, k and memory size (Section 6.8) |
| detected | a reported row whose 95% CI lower bound is above zero; never a verdict |

### 5.1 Three stages

| stage | data | what it fixed or tested | status |
|---|---|---|---|
| A (exploratory) | KTVIC dev299, OV-dev-A | one configuration per backbone (Section 3.5), chosen by a rule written before any output | design note committed before any output; reported in the "all configurations tried" supplement (Tables S10–S11) |
| B (one look) | OV-dev-B, XM-dev500 | a gate on OV-dev-B: pooled `ret` − `rand` with CI lower bound > 0 and point ≥ +4.0 (twice the SESOI), plus the guard hypothesis H_G | prereg committed before any dev-B image was decoded; gate PASS, H_G not passed |
| test (one look per set) | OV-test, XM-test2500 | P1, P1b, P2, XM-a, XM-b and the named secondaries below | prereg and test code committed, and the test code checked, before any test image or test reference reached the GPU server |

The test registration was committed after the stage-B result was known and before any test output existed. Nothing in it was set from a test set: the SESOI and every threshold come from the stage-B registration or from the plan written before stage A.

**One look in practice.** Each test set was decoded once and scored once with the frozen configuration, and each set's decision script ran once. During the runs nobody read a test caption, ledger row, score or partial decision output; monitoring used only counts, times, GPU seconds and return codes. Each decision file records the sha256 of every ledger it read.

**Order.** The OpenViIC block ran first, then the XM3600 block. The XM3600 block was pre-committed to run whatever the OpenViIC verdict. Verified precision was scored offline, once, after the XM3600 block.

### 5.2 Estimands and decision rules

For backbone m and image i, let Δ_m,i be the stripped CIDEr-D of `ret` minus that of `rand`, each at m's frozen configuration. The pooled difference is Δ_i = ½(Δ_qwen,i + Δ_internvl,i). SESOI = +2.0 stripped CIDEr-D points.

The pooled estimand averages two backbone-plus-configuration pairs that differ in k, order, prompt tail and τ (Table 2). It is not an estimate of the effect for a typical MLLM, and every pooled number is printed beside its two per-backbone rows.

**Where the SESOI came from.** The value +2.0 was set at stage 2, before any stage-B output, as a planning value suggested in the study's design notes; it equals the value used at stage 1 (stage-2 registration, §7.1). The stage-2 registration states that it was not derived from the stage-A pilot or from any stage-1 number, and no calibration of it is recorded. The English arm carried the same +2.0 over numerically, without recalibration to the PTB-tokenised scale (Section 8.1). Descriptive context for its size, added post hoc, is in Section 5.4.

**What the CIs condition on.** Each image has one seeded `rand` assignment, and CIDEr-D document frequencies come from the full scored set. The bootstrap resamples images only, so the CIs cover image-sampling uncertainty conditional on that one `rand` draw and on the full-set document frequencies, a standard approximation. Variation from drawing other random examples is not in the CIs, and every claim is limited accordingly.

**Table 4. Registered predictions and decision rules.**

| name | estimand | set | rule |
|---|---|---|---|
| **P1 (primary)** | mean of pooled Δ_i | OV-test primary (1,941) | PASS if the point estimate is > +2.0 **and** the 95% CI lower bound is > 0 |
| length rule L | per backbone, \|len_ret − len_rand\| / len_rand on the primary set (mean syllables) | OV-test primary | if > 0.10 for either backbone, P1 is recorded as "PASS, not separated from length" |
| P1b (non-gating) | per-backbone mean of Δ_m,i | OV-test primary | Qwen2.5-VL: "confirmed" if the point is > +2.0; InternVL3: reported only, with no prediction. P1b selects the scope sentence (Table 5) |
| **P2** | per backbone, ΔP_cm of `ret` against `zs` = 100 · (Σ tp_cm − Σ tp_cm,zs) / Σ k_cm | OV-test primary | for **each** backbone, 95% CI lower bound > −1.0 |
| XM-a | mean of pooled Δ_i | XM-test2500 | 95% CI lower bound > 0. A positive point with a CI that includes 0 is printed as a descriptive number only |
| XM-b | Δ verified object precision of `ret` against `zs`, pooled over mentions and backbones | XM-test2500 | 95% CI lower bound > −1.0 |
| XM prediction | XM-a ∧ XM-b | XM-test2500 | "confirmed" only if both pass; otherwise "not confirmed" |

For P2, k_i = min(|M_i(run)|, |M_i(zs)|) over distinct classes in order of mention, and tp counts the first k_i classes that the gold supports.

Registered sensitivities, reported beside each prediction and never replacing it:
- for P1, P1b and P2, the full OV-test (2,001);
- for XM-a and XM-b, XM-test2500 without the three-reference images (2,392).

**Table 5. Scope sentence, fixed before the test and applied only if P1 passes.**

| P1b outcome | sentence placed beside every pooled number |
|---|---|
| Qwen point > +2.0, InternVL3 CI lower bound ≤ 0 | "carried mainly by Qwen2.5-VL; not detected for InternVL3" |
| Qwen point > +2.0, InternVL3 lower bound > 0, InternVL3 point < Qwen point | "carried mainly by Qwen2.5-VL; smaller for InternVL3" |
| Qwen point > +2.0, InternVL3 lower bound > 0, InternVL3 point ≥ Qwen point | "present for both backbones" |
| Qwen point ≤ +2.0, InternVL3 point > +2.0 and lower bound > 0 | "carried mainly by InternVL3; not at the SESOI for Qwen2.5-VL" |
| Qwen point ≤ +2.0, any other InternVL3 outcome | "not carried by either backbone at the SESOI" |

**Claims and their gates.**
- "Retrieved examples beat random examples on OpenViIC test" needs P1 to pass and rule L not to fire.
- "No object-precision cost" for backbone m needs P2 to pass for m, and applies to OpenViIC test only. The cost is measured relative to zero-shot, from the full in-context prompt; P2 does not compare `ret` with `rand`.
- "The gain transfers to XM3600 Vietnamese" needs XM-a to pass.
- "The registered XM prediction is confirmed" needs both XM-a and XM-b to pass.
- No guard claim is allowed: the guard failed at stage B and is a registered negative.

**Registered wording for failures.**
- A failed XM-a is reported as "the gain was not detected out of domain (XM3600)", with the CI.
- A failed P1 would have been reported as "the dev-B gain did not replicate on OV-test", with no post-hoc analysis in its place.

### 5.3 Secondaries (named, non-gating)

None of these can turn a failed prediction into a pass, and none enters the title, the abstract or the contributions:
- S-zf, `ret` against `zs` and against `fix`, with an expected size against `zs` of about +10.0 pooled, stated before the test and given no pass label;
- the NN-top1 and NN-consensus baselines;
- the PTB-tokenised column;
- the cosine-tertile dose-response (cuts per scored set, from that set's query cosines);
- the style report and the source-dataset share of shown examples;
- neighbour-only object precision;
- every pooled number printed next to its two per-backbone values.

**One secondary is motivated by stage B: per-backbone `ret` − `rand` at τ = −∞.** It is post hoc at stage B and was pre-specified for the test. Only the InternVL3 row is new, because Qwen2.5-VL's frozen τ is already −∞. It has no pooled form, is labelled "detected" when its CI lower bound is > 0, is read by no gate or scope rule, and is always printed after InternVL3's registered τ = 0.10 result.

### 5.4 Uncertainty and multiplicity

- **Bootstrap.** All CIs are paired image bootstraps with B = 2,000 resamples and percentile 95% intervals.
- **Index matrices.** Each scored set draws one index matrix from a fresh generator with seed 0, used by every CI on that set: 1,941, 2,001, 2,500 and 2,392 images. The matrices are drawn independently, so one set's matrix is not a subset of another's.
- **Pooling and ratios.** Pooled statistics average the per-image differences over backbones before resampling. For ratio statistics (ΔP_cm, verified precision, neighbour-only precision), numerator and denominator are resampled together.
- **Multiplicity.** P1 is the single primary test, so no adjustment is needed. P2 is an intersection–union test over the two backbones. The XM3600 prediction is a conjunction of XM-a and XM-b, and in the separate English registration S-NC was gated in a fixed order after P1-EN. Everything else is secondary, reported with unadjusted CIs, with no family-wise claim.
- **p-values.** None are reported. The registrations fixed CI-based rules, and a p-value added now would be post hoc and change no verdict.

**Power and precision (the power note is registered; the other rows are descriptive and post hoc).** The stage-2 registration stated the power of the stage-B gate G1 (point ≥ +4.0, lower bound > 0): at a standard error of about 1.85 per backbone, the chance of passing G1 was about 50% if the true pooled difference were +4. No separate power statement was registered for P1. The achieved 95% CI half-widths of the registered pooled estimands, from the decision files, were 1.02 (P1), 1.21 (XM-a), 0.97 (P1-EN) and 0.78 (S-NC). For scale, the SESOI is about 6.2% of the pooled `rand` score on OV-test, 3.7% on XM-test2500 and 2.3% on both COCO and NoCaps; the observed pooled difference is about 13.9% of `rand` for P1, 1.3% for XM-a, 3.5% for P1-EN and 2.0% for S-NC. On COCO, where scores are higher, the same +2.0 is therefore relatively more lenient. XM-a's upper bound (1.97) lies just below +2.0.

**Monte Carlo error of the bootstrap (post hoc, approximate).** Percentile endpoints at B = 2,000 carry Monte Carlo error. Under a normal approximation to each bootstrap distribution, the standard error of a 2.5% or 97.5% endpoint is about 0.06 bootstrap standard errors, which is at most about 0.05 CIDEr-D or precision points for every registered row. The registered bound closest to its threshold is XM-a's lower bound (−0.45 against 0), about twelve such standard errors away, so no verdict depends on this error.

### 5.5 Budget

The test had a hard cap of 20 GPU-hours on one 24 GB GPU, against an estimated upper bound of 13.7. A cap stop would have been final for the set concerned. The cap was not reached (Section 6.9).

### 5.6 Two later registrations

Two further studies were registered after the Vietnamese test. Each has its own registration file, committed before any of its outputs existed, and neither amends the test registration above.
- **The English arm (Section 8)** carries Table 2 and the P1 rule over to the COCO Karpathy test and NoCaps val, with one look per set.
- **The mechanism ablations (Section 6.8)** vary τ, k and the memory size on OV-dev-B, one look, under the label "development set, non-confirmatory". The registration fixed in advance the condition under which Section 6.8 may say that the ablations explain the backbone dependence: the τ prediction's first two parts hold, and the memory prediction is not fully failed. The condition held, but Section 6.8 uses weaker wording, because the ablations do not isolate a property of the backbone.

