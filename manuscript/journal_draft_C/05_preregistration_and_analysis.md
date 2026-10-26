## 5. Preregistration and analysis plan

### 5.1 Three stages

| stage | data | what it fixed or tested | status |
|---|---|---|---|
| A (exploratory) | KTVIC dev299, OV-dev-A | one configuration per backbone (Section 3.5), chosen by a rule written before any output | design note committed before any output; reported in an "all configurations tried" appendix |
| B (one look) | OV-dev-B, XM-dev500 | a gate on OV-dev-B: pooled `ret` − `rand` with CI lower bound > 0 and point ≥ +4.0 (twice the SESOI), plus the guard hypothesis H_G | prereg committed before any dev-B image was decoded; gate PASS, H_G not passed |
| test (one look per set) | OV-test, XM-test2500 | P1, P1b, P2, XM-a, XM-b and the named secondaries below | prereg and test code committed, and the test code checked, before any test image or test reference reached the decoding machine |

The test registration was committed after the stage-B result was known and before any test output existed. Nothing in it was set from a test set: the SESOI and every threshold come from the stage-B registration or from the plan written before stage A.

**One look in practice.** Each test set was decoded once and scored once with the frozen configuration, and each set's decision script ran once. During the runs nobody read a test caption, ledger row, score or partial decision output; monitoring used only counts, times, GPU seconds and return codes. Each decision file records the sha256 of every ledger it read.

**Order.** The OpenViIC block ran first, then the XM3600 block. The XM3600 block was pre-committed to run whatever the OpenViIC verdict. Verified precision was scored offline, once, after the XM3600 block.

### 5.2 Estimands and decision rules

For backbone m and image i, let Δ_m,i be the stripped CIDEr-D of `ret` minus that of `rand`, each at m's frozen configuration. The pooled difference is Δ_i = ½(Δ_qwen,i + Δ_internvl,i). SESOI = +2.0 stripped CIDEr-D points.

**Table 3. Registered predictions and decision rules.**

| name | estimand | set | rule |
|---|---|---|---|
| **P1 (primary)** | mean of pooled Δ_i | OV-test primary (1,941) | PASS if the point estimate is > +2.0 **and** the 95% CI lower bound is > 0 |
| length rule L | per backbone, \|len_ret − len_rand\| / len_rand on the primary set (mean syllables) | OV-test primary | if > 0.10 for either backbone, P1 is recorded as "PASS, not separated from length" |
| P1b (non-gating) | per-backbone mean of Δ_m,i | OV-test primary | Qwen2.5-VL: "confirmed" if the point is > +2.0; InternVL3: reported only, with no prediction. P1b selects the scope sentence (Table 4) |
| **P2** | per backbone, ΔP_cm of `ret` against `zs` = 100 · (Σ tp_cm − Σ tp_cm,zs) / Σ k_cm | OV-test primary | for **each** backbone, 95% CI lower bound > −1.0 |
| XM-a | mean of pooled Δ_i | XM-test2500 | 95% CI lower bound > 0. A positive point with a CI that includes 0 is printed as a descriptive number only |
| XM-b | Δ verified object precision of `ret` against `zs`, pooled over mentions and backbones | XM-test2500 | 95% CI lower bound > −1.0 |
| XM prediction | XM-a ∧ XM-b | XM-test2500 | "confirmed" only if both pass; otherwise "not confirmed" |

For P2, k_i = min(|M_i(run)|, |M_i(zs)|) over distinct classes in order of mention, and tp counts the first k_i classes that the gold supports.

Registered sensitivities, reported beside each prediction and never replacing it:
- for P1, P1b and P2, the full OV-test (2,001);
- for XM-a and XM-b, XM-test2500 without the three-reference images (2,392).

**Table 4. Scope sentence, fixed before the test and applied only if P1 passes.**

| P1b outcome | sentence placed beside every pooled number |
|---|---|
| Qwen point > +2.0, InternVL3 CI lower bound ≤ 0 | "carried mainly by Qwen2.5-VL; not detected for InternVL3" |
| Qwen point > +2.0, InternVL3 lower bound > 0, InternVL3 point < Qwen point | "carried mainly by Qwen2.5-VL; smaller for InternVL3" |
| Qwen point > +2.0, InternVL3 lower bound > 0, InternVL3 point ≥ Qwen point | "present for both backbones" |
| Qwen point ≤ +2.0, InternVL3 point > +2.0 and lower bound > 0 | "carried mainly by InternVL3; not at the SESOI for Qwen2.5-VL" |
| Qwen point ≤ +2.0, any other InternVL3 outcome | "not carried by either backbone at the SESOI" |

**Claims and their gates.**
- "Retrieved examples beat random examples on OpenViIC test" needs P1 to pass and rule L not to fire.
- "No object-precision cost" for backbone m needs P2 to pass for m, and applies to OpenViIC test only.
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
- **Multiplicity.** P1 is the single primary test, so no adjustment is needed. P2 is an intersection–union test over the two backbones. Everything else is secondary, reported with unadjusted CIs, with no family-wise claim.

### 5.5 Budget

The test had a hard cap of 20 GPU-hours on one 24 GB GPU, against an estimated upper bound of 13.7. A cap stop would have been final for the set concerned. The cap was not reached (Section 6.8).
