## 6. Results

All test numbers come from the three decision files and their ledgers. All differences are paired with 95% bootstrap CIs. Units:
- P1, P1b, XM-a and every CIDEr-D difference are in stripped CIDEr-D points;
- P2 is in count-matched precision points;
- XM-b is in verified-precision points.

### 6.1 Absolute scores

**Table 5. Stripped CIDEr-D (×100) per arm, each backbone at its frozen τ.**

| set | backbone (τ) | `ret` | `rand` | `fix` | `zs` |
|---|---|---|---|---|---|
| OV-test primary | Qwen2.5-VL (−∞) | {{L1941:ct_qwen25vl_7b_ov_test-ret-k8-first-T1@-inf:cider_s|p}} | {{L1941:ct_qwen25vl_7b_ov_test-rand-k8-T1@-inf:cider_s|p}} | {{L1941:ct_qwen25vl_7b_ov_test-fix-k8-T1@-inf:cider_s|p}} | {{L1941:ct_qwen25vl_7b_ov_test-zs@-inf:cider_s|p}} |
| OV-test primary | InternVL3 ({{FC:models.internvl3_8b.tau|raw}}) | {{L1941:ct_internvl3_8b_ov_test-ret-k4-last-T2@0.10:cider_s|p}} | {{L1941:ct_internvl3_8b_ov_test-rand-k4-T2@0.10:cider_s|p}} | {{L1941:ct_internvl3_8b_ov_test-fix-k4-T2@0.10:cider_s|p}} | {{L1941:ct_internvl3_8b_ov_test-zs@-inf:cider_s|p}} |
| XM-test2500 | Qwen2.5-VL (−∞) | {{L2500:ct_qwen25vl_7b_xm_test2500-ret-k8-first-T1@-inf:cider_s|p}} | {{L2500:ct_qwen25vl_7b_xm_test2500-rand-k8-T1@-inf:cider_s|p}} | {{L2500:ct_qwen25vl_7b_xm_test2500-fix-k8-T1@-inf:cider_s|p}} | {{L2500:ct_qwen25vl_7b_xm_test2500-zs@-inf:cider_s|p}} |
| XM-test2500 | InternVL3 ({{FC:models.internvl3_8b.tau|raw}}) | {{L2500:ct_internvl3_8b_xm_test2500-ret-k4-last-T2@0.10:cider_s|p}} | {{L2500:ct_internvl3_8b_xm_test2500-rand-k4-T2@0.10:cider_s|p}} | {{L2500:ct_internvl3_8b_xm_test2500-fix-k4-T2@0.10:cider_s|p}} | {{L2500:ct_internvl3_8b_xm_test2500-zs@-inf:cider_s|p}} |

The copy baselines, which use no model, score {{L1941:ct_nn_ov_test-top1@-inf:cider_s|p}} (NN-top1), {{L1941:ct_nn_ov_test-cons-k4@-inf:cider_s|p}} (NN-consensus, k = 4) and {{L1941:ct_nn_ov_test-cons-k8@-inf:cider_s|p}} (k = 8) on OV-test, and {{L2500:ct_nn_xm_test2500-top1@-inf:cider_s|p}}, {{L2500:ct_nn_xm_test2500-cons-k4@-inf:cider_s|p}} and {{L2500:ct_nn_xm_test2500-cons-k8@-inf:cider_s|p}} on XM-test2500. Every other registered per-run row (as-written and PTB CIDEr-D, CHAIR_i, mentions, copy and deletion rates) is in Tables S1–S4.

### 6.2 In domain: OpenViIC test

**Table 6 (main). Registered OpenViIC test results: the primary set and the full set side by side.**

| row | OV-test primary ({{PL:ov_test_primary1941.txt|i}}) | verdict | OV-test full ({{PL:ov_test_files.tsv|i}}), registered sensitivity |
|---|---|---|---|
| **P1**, pooled `ret` − `rand` | **{{OV:P1|e}}** | **{{OV:P1.passed|v:pass}}** | {{OV:sensitivity.ov_test_2001|e}} |
| P1b, Qwen2.5-VL | {{OV:P1b.qwen25vl_7b|e}} | {{OV:P1b.qwen25vl_7b.confirmed|v:conf}} (point > +{{OV:SESOI|f1}}) | {{OV:sets.ov_test_2001.detail.per_model.qwen25vl_7b.vs_rand|e}} |
| P1b, InternVL3 (τ = {{FC:models.internvl3_8b.tau|raw}}) | {{OV:P1b.internvl3_8b|e}} | reported only | {{OV:sets.ov_test_2001.detail.per_model.internvl3_8b.vs_rand|e}} |
| **P2**, Qwen2.5-VL, ΔP_cm vs `zs` | **{{OV:P2.qwen25vl_7b|e}}** | **{{OV:P2.qwen25vl_7b.passed|v:pass}}** (lower bound > {{C:pcm_floor|f1}}) | {{OV:sets.ov_test_2001.detail.per_model.qwen25vl_7b.pcm_vs_zs|e}} |
| **P2**, InternVL3, ΔP_cm vs `zs` | **{{OV:P2.internvl3_8b|e}}** | **{{OV:P2.internvl3_8b.passed|v:pass}}** (lower bound > {{C:pcm_floor|f1}}) | {{OV:sets.ov_test_2001.detail.per_model.internvl3_8b.pcm_vs_zs|e}} |
| length gap, Qwen2.5-VL (\|ret − rand\| / rand) | {{OV:P1.length.qwen25vl_7b.rel_gap|f3}} | L {{OV:P1.L|v:fires}} (≤ {{C:len_rule|p}}) | {{OV:sets.ov_test_2001.detail.per_model.qwen25vl_7b.length.rel_gap|f3}} |
| length gap, InternVL3 | {{OV:P1.length.internvl3_8b.rel_gap|f3}} | L {{OV:P1.L|v:fires}} | {{OV:sets.ov_test_2001.detail.per_model.internvl3_8b.length.rel_gap|f3}} |

Scope sentence for every pooled P1 number in this table (registered mapping, Table 4): **{{OV:scope.sentence|vw}}**.<!-- scope row: {{OV:scope.row|vw}} -->

**P1: {{OV:P1.passed|v:pass}}.** Retrieved examples beat random examples on the OpenViIC test by {{OV:P1|e}} stripped CIDEr-D points, pooled over the two backbones. The effect is **carried mainly by Qwen2.5-VL and not detected for InternVL3** (the registered scope sentence). Rule L {{OV:P1.L|v:fires}} on the primary set. Mean caption length was:
- Qwen2.5-VL: {{OV:P1.length.qwen25vl_7b.ret|p}} syllables for `ret` against {{OV:P1.length.qwen25vl_7b.rand|p}} for `rand`;
- InternVL3: {{OV:P1.length.internvl3_8b.ret|p}} against {{OV:P1.length.internvl3_8b.rand|p}}.

On the full {{PL:ov_test_files.tsv|i}} images the pooled difference is {{OV:sensitivity.ov_test_2001|e}}, again carried mainly by Qwen2.5-VL and not detected for InternVL3. The primary set decides.

**P1b.** For Qwen2.5-VL the per-backbone difference is {{OV:P1b.qwen25vl_7b|e}}, above the SESOI, so the registered P1b prediction is {{OV:P1b.qwen25vl_7b.confirmed|v:conf}}. For InternVL3 at its frozen τ = {{FC:models.internvl3_8b.tau|raw}} it is {{OV:P1b.internvl3_8b|e}}, a CI that includes zero. This row carries no prediction.

**P2: {{OV:P2.qwen25vl_7b.passed|v:pass}} for Qwen2.5-VL and {{OV:P2.internvl3_8b.passed|v:pass}} for InternVL3** (both: {{OV:P2.passed_both|v:passed}}). Against each model's own zero-shot captions, `ret` changed count-matched object precision by {{OV:P2.qwen25vl_7b|e}} points for Qwen2.5-VL and {{OV:P2.internvl3_8b|e}} for InternVL3. Both lower bounds lie above the {{C:pcm_floor|f1}} floor and also above zero. On OpenViIC test, then, we find no object-precision cost from retrieved examples for either backbone. This statement is limited to OpenViIC test.

### 6.3 Out of domain: XM3600 Vietnamese

**Table 7. Registered XM-test2500 results.**

| row | XM-test2500 ({{CHAIN:xm_staged|i}}) | verdict | without three-reference images ({{L2392:ct_qwen25vl_7b_xm_test2500-ret-k8-first-T1@-inf:n|i}}), registered sensitivity |
|---|---|---|---|
| **XM-a**, pooled `ret` − `rand` | **{{XM:XM_a|e}}** | **{{XM:XM_a.passed|v:pass}}** (CI includes 0) | {{XM:sensitivity.xm_test2392|e}} |
| per backbone, Qwen2.5-VL | {{XM:per_model.qwen25vl_7b|e}} | reported row, no registered rule, unadjusted CI | {{XM:sets.xm_test2392.detail.per_model.qwen25vl_7b.vs_rand|e}} |
| per backbone, InternVL3 (τ = {{FC:models.internvl3_8b.tau|raw}}) | {{XM:per_model.internvl3_8b|e}} | reported row, no registered rule, unadjusted CI | {{XM:sets.xm_test2392.detail.per_model.internvl3_8b.vs_rand|e}} |
| **XM-b**, Δ verified precision `ret` vs `zs`, pooled | **{{XMB:XM_b|e}}** | **{{XMB:XM_b.passed|v:pass}}** (lower bound > {{C:vp_floor|f1}}) | {{XMB:XM_b_sensitivity.xm_test2392|e}} ({{XMB:XM_b_sensitivity.xm_test2392.passed|v:pass}}) |
| **XM prediction** (XM-a ∧ XM-b) | | **{{XMB:XM_prediction|vw}}** (XM-a {{XMB:XM_a_read.passed|v:pass}}) | |
| ΔP_cm vs `zs`, Qwen2.5-VL (reported row, no XM rule) | {{XM:sets.xm_test2500.detail.per_model.qwen25vl_7b.pcm_vs_zs|e}} | | {{XM:sets.xm_test2392.detail.per_model.qwen25vl_7b.pcm_vs_zs|e}} |
| ΔP_cm vs `zs`, InternVL3 (reported row, no XM rule) | {{XM:sets.xm_test2500.detail.per_model.internvl3_8b.pcm_vs_zs|e}} | | {{XM:sets.xm_test2392.detail.per_model.internvl3_8b.pcm_vs_zs|e}} |

**XM-a: {{XM:XM_a.passed|v:pass}}. The gain was not detected out of domain (XM3600).** The pooled difference is {{XM:XM_a|e}}: the point estimate is above zero, but the CI includes zero. Under the registered rule this point is a descriptive number only, and nothing about it is confirmed. Without the three-reference images the difference is {{XM:sensitivity.xm_test2392|e}}, which changes nothing.

**Per backbone** (reported rows; no per-backbone XM3600 rule was registered). Qwen2.5-VL: {{XM:per_model.qwen25vl_7b|e}} (unadjusted CI). InternVL3 at its frozen τ: {{XM:per_model.internvl3_8b|e}} (per-backbone reported row, no registered rule, unadjusted CI; {{L2392:ct_qwen25vl_7b_xm_test2500-ret-k8-first-T1@-inf:n|i}}-image sensitivity {{XM:sets.xm_test2392.detail.per_model.internvl3_8b.vs_rand|e}}). Rule L is defined on the {{PL:ov_test_primary1941.txt|i}}; on XM-test2500 the length gaps are reported only ({{XM:sets.xm_test2500.detail.per_model.qwen25vl_7b.length.rel_gap|f3}} and {{XM:sets.xm_test2500.detail.per_model.internvl3_8b.length.rel_gap|f3}}).

**XM-b: {{XMB:XM_b.passed|v:pass}} under its own rule; the XM prediction is {{XMB:XM_prediction|vw}}.** Pooled over mentions and backbones, verified object precision of `ret` against `zs` changed by {{XMB:XM_b|e}} points, with the lower bound above the {{C:vp_floor|f1}} floor. The registered XM prediction is the conjunction of XM-a and XM-b. Since XM-a is {{XMB:XM_a_read.passed|v:pass}}, the prediction is **{{XMB:XM_prediction|vw}}**.

We therefore make no claim that the gain transfers to XM3600, and no claim that retrieval keeps object precision there. The count-matched rows on XM3600 are reported with no rule attached. For Qwen2.5-VL that row's lower bound ({{XM:sets.xm_test2500.detail.per_model.qwen25vl_7b.pcm_vs_zs.lo|p}}) lies below the {{C:pcm_floor|f1}} value used on OpenViIC.

The memory holds no XM3600 captions: the source-dataset share of shown examples is {{XM:sets.xm_test2500.detail.per_model.qwen25vl_7b.src_share.ret|f3}} for both backbones. XM-test2500 is therefore a test of retrieval from a memory in another domain and another reference style. It is not a test of in-domain retrieval on a second dataset.

### 6.4 Controls: zero-shot, fixed examples and copy baselines

**Table 8. S-zf and copy baselines (`ret` minus the named comparison), primary scored sets.**

| comparison | OV-test, pooled | OV Qwen2.5-VL | OV InternVL3 | XM, pooled | XM Qwen2.5-VL | XM InternVL3 |
|---|---|---|---|---|---|---|
| vs `zs` | {{OV:S_zf.pooled_vs_zs|e}} | {{OV:S_zf.per_model.qwen25vl_7b.vs_zs|e}} | {{OV:S_zf.per_model.internvl3_8b.vs_zs|e}} | {{XM:S_zf.pooled_vs_zs|e}} | {{XM:S_zf.per_model.qwen25vl_7b.vs_zs|e}} | {{XM:S_zf.per_model.internvl3_8b.vs_zs|e}} |
| vs `fix` | {{OV:S_zf.pooled_vs_fix|e}} | {{OV:S_zf.per_model.qwen25vl_7b.vs_fix|e}} | {{OV:S_zf.per_model.internvl3_8b.vs_fix|e}} | {{XM:S_zf.pooled_vs_fix|e}} | {{XM:S_zf.per_model.qwen25vl_7b.vs_fix|e}} | {{XM:S_zf.per_model.internvl3_8b.vs_fix|e}} |
| vs NN-top1 | {{OV:sets.ov_test_1941.nn.vs_nn_top1.pooled|e}} | {{OV:sets.ov_test_1941.nn.vs_nn_top1.qwen25vl_7b|e}} | {{OV:sets.ov_test_1941.nn.vs_nn_top1.internvl3_8b|e}} | {{XM:sets.xm_test2500.nn.vs_nn_top1.pooled|e}} | {{XM:sets.xm_test2500.nn.vs_nn_top1.qwen25vl_7b|e}} | {{XM:sets.xm_test2500.nn.vs_nn_top1.internvl3_8b|e}} |
| vs NN-consensus | {{OV:sets.ov_test_1941.nn.vs_nn_cons.pooled|e}} | {{OV:sets.ov_test_1941.nn.vs_nn_cons.qwen25vl_7b|e}} | {{OV:sets.ov_test_1941.nn.vs_nn_cons.internvl3_8b|e}} | {{XM:sets.xm_test2500.nn.vs_nn_cons.pooled|e}} | {{XM:sets.xm_test2500.nn.vs_nn_cons.qwen25vl_7b|e}} | {{XM:sets.xm_test2500.nn.vs_nn_cons.internvl3_8b|e}} |

**S-zf.** The registered expectation for `ret` − `zs` was about +{{C:s_zf_expected|f1}} pooled, and S-zf has no pass label. The observed value was {{OV:S_zf.pooled_vs_zs|e}} on OV-test and {{XM:S_zf.pooled_vs_zs|e}} on XM-test2500.

The `rand` − `zs` comparison is descriptive and post hoc (Table 5; no registered contrast or CI): random examples from the same memory already score well above zero-shot for both backbones on both sets. The registered rows behind this are S-zf `ret` − `zs` {{OV:S_zf.pooled_vs_zs|e}} against P1 `ret` − `rand` {{OV:P1|e}} on OV-test.

Against fixed examples, Qwen2.5-VL gained on both sets. InternVL3's difference had a CI that includes zero on both sets: {{OV:S_zf.per_model.internvl3_8b.vs_fix|e}} on OV-test and {{XM:S_zf.per_model.internvl3_8b.vs_fix|e}} on XM-test2500.

**Copy baselines.** Both backbones with retrieved examples score well above the captions they could have copied, on both sets. The model is therefore not simply returning its neighbours' captions. The near-verbatim copy share of `ret` captions on OV-test was {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.verbatim_share|f3}} for Qwen2.5-VL and {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.verbatim_share|f3}} for InternVL3.

### 6.5 PTB column, dose-response and style

**PTB-tokenised CIDEr-D.** The pooled `ret` − `rand` was:
- OV-test: {{OV:sets.ov_test_1941.pooled_ptb_vs_rand|e}} (Qwen2.5-VL {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.ptb_vs_rand|e}}, InternVL3 {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.ptb_vs_rand|e}});
- XM-test2500: {{XM:ptb|e}} (Qwen2.5-VL {{XM:sets.xm_test2500.detail.per_model.qwen25vl_7b.ptb_vs_rand|e}}, InternVL3 {{XM:sets.xm_test2500.detail.per_model.internvl3_8b.ptb_vs_rand|e}}).

The PTB column agrees in sign and scope with the stripped column on both sets.

**Table 9. Dose-response: pooled `ret` − `rand` within tertiles of the query's nearest eligible-cluster cosine (cuts per scored set).**

| set | cuts | low | mid | high |
|---|---|---|---|---|
| OV-test primary | {{OV:sets.ov_test_1941.dose_response.cuts.0|f3}}, {{OV:sets.ov_test_1941.dose_response.cuts.1|f3}} | {{OV:sets.ov_test_1941.dose_response.low|e}} (n = {{OV:sets.ov_test_1941.dose_response.low.n|i}}) | {{OV:sets.ov_test_1941.dose_response.mid|e}} | {{OV:sets.ov_test_1941.dose_response.high|e}} |
| XM-test2500 | {{XM:sets.xm_test2500.dose_response.cuts.0|f3}}, {{XM:sets.xm_test2500.dose_response.cuts.1|f3}} | {{XM:sets.xm_test2500.dose_response.low|e}} (n = {{XM:sets.xm_test2500.dose_response.low.n|i}}) | {{XM:sets.xm_test2500.dose_response.mid|e}} | {{XM:sets.xm_test2500.dose_response.high|e}} (n = {{XM:sets.xm_test2500.dose_response.high.n|i}}) |

The OV-test tertiles show no monotone pattern. The XM-test2500 cosine cuts lie well below the OV-test cuts, which is consistent with a memory from another domain. The XM-test2500 high tertile has the lowest point estimate. This row is reported, non-gating, and is not interpreted further.

**Table 10. Style report and source-dataset share, OV-test primary.**

| backbone | arm | mean syllables | ends in punctuation | top-3 opening share | source-dataset share |
|---|---|---|---|---|---|
| Qwen2.5-VL | `ret` | {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.style.ret.mean_syllables|p}} | {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.style.ret.ends_punct|f3}} | {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.style.ret.top3_open_share|f3}} | {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.src_share.ret|f3}} |
| Qwen2.5-VL | `rand` | {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.style.rand.mean_syllables|p}} | {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.style.rand.ends_punct|f3}} | {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.style.rand.top3_open_share|f3}} | {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.src_share.rand|f3}} |
| Qwen2.5-VL | `fix` | {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.style.fix.mean_syllables|p}} | {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.style.fix.ends_punct|f3}} | {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.style.fix.top3_open_share|f3}} | {{OV:sets.ov_test_1941.detail.per_model.qwen25vl_7b.src_share.fix|f3}} |
| InternVL3 | `ret` | {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.style.ret.mean_syllables|p}} | {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.style.ret.ends_punct|f3}} | {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.style.ret.top3_open_share|f3}} | {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.src_share.ret|f3}} |
| InternVL3 | `rand` | {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.style.rand.mean_syllables|p}} | {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.style.rand.ends_punct|f3}} | {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.style.rand.top3_open_share|f3}} | {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.src_share.rand|f3}} |
| InternVL3 | `fix` | {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.style.fix.mean_syllables|p}} | {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.style.fix.ends_punct|f3}} | {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.style.fix.top3_open_share|f3}} | {{OV:sets.ov_test_1941.detail.per_model.internvl3_8b.src_share.fix|f3}} |

The source-dataset share is the share of shown examples that come from a cluster with an OpenViIC member. It is near one for every arm, so `rand` and `fix` also show in-domain captions, as the design intends. The XM-test2500 style rows, and the rows for the full OV-test and the 2,392-image XM sensitivity, are in Table S6.

### 6.6 Neighbour-only objects and the deletion step

**Neighbour-only object precision** is the precision of the objects that a caption takes only from its examples (Section 3.4). It is a named secondary and not a co-primary.

On OV-test, scored against reference gold, it was:
- Qwen2.5-VL: {{OV:sets.ov_test_1941.S3.per_model.qwen25vl_7b|eu}}, over {{OV:sets.ov_test_1941.S3.per_model.qwen25vl_7b.sum_m|i}} mentions, with {{OV:sets.ov_test_1941.S3.per_model.qwen25vl_7b.share_m_pos|f3}} of images having at least one;
- InternVL3: {{OV:sets.ov_test_1941.S3.per_model.internvl3_8b|eu}}, over {{OV:sets.ov_test_1941.S3.per_model.internvl3_8b.sum_m|i}} mentions, with a share of {{OV:sets.ov_test_1941.S3.per_model.internvl3_8b.share_m_pos|f3}};
- pooled: {{OV:sets.ov_test_1941.S3.pooled|eu}}.

On XM-test2500, scored offline against the verified Open Images labels, it was:
- Qwen2.5-VL: {{XMB:S3_verified.xm_test2500.per_model.qwen25vl_7b|eu}}, over {{XMB:S3_verified.xm_test2500.per_model.qwen25vl_7b.sum_m|i}} mentions;
- InternVL3: {{XMB:S3_verified.xm_test2500.per_model.internvl3_8b.np|p}}, that is {{XMB:S3_verified.xm_test2500.per_model.internvl3_8b.sum_m|i}}/{{XMB:S3_verified.xm_test2500.per_model.internvl3_8b.sum_m|i}} verified; the CI is not informative ({{XMB:S3_verified.xm_test2500.per_model.internvl3_8b.sum_m|i}} mentions);
- pooled: {{XMB:S3_verified.xm_test2500.pooled|eu}}.

The InternVL3 counts are much smaller than Qwen2.5-VL's. This is consistent with its registered captions having already passed the deletion step.

**What the deletion step did to InternVL3.** At InternVL3's frozen τ = {{FC:models.internvl3_8b.tau|raw}} on OV-test, `ret` had {{L1941:ct_internvl3_8b_ov_test-ret-k4-last-T2@0.10:rejected_per_image|f3}} classes rejected per image. {{L1941:ct_internvl3_8b_ov_test-ret-k4-last-T2@0.10:deleted_rate|f3}} of captions were edited by deletion and {{L1941:ct_internvl3_8b_ov_test-ret-k4-last-T2@0.10:fallback_rate|f3}} fell back to the zero-shot caption. Its stripped CIDEr-D was {{L1941:ct_internvl3_8b_ov_test-ret-k4-last-T2@0.10:cider_s|p}}, against {{L1941:ct_internvl3_8b_ov_test-ret-k4-last-T2@-inf:cider_s|p}} for the same decodes with no deletion (both rows registered). For `rand` the corresponding values were {{L1941:ct_internvl3_8b_ov_test-rand-k4-T2@0.10:cider_s|p}} and {{L1941:ct_internvl3_8b_ov_test-rand-k4-T2@-inf:cider_s|p}}.

### 6.7 The guard, stage B, and the secondary motivated by stage B

**The guard is a registered negative.** At stage B the guard hypothesis H_G was {{DF:ov_dev_b.H_G.passed|v:passed}} (stage-B decision file, `ov_dev_b.H_G.passed`). The pooled precision change was {{DF:ov_dev_b.H_G.pooled|e}}, with a stripped CIDEr-D cost (`ret` at τ_G minus `ret` at −∞, pooled) of {{DF:ov_dev_b.H_G.cost|p}}. For InternVL3, the count of neighbour-only mentions went from {{DF:ov_dev_b.H_G.per_model.internvl3_8b.at_-inf.sum_m|i}} to {{DF:ov_dev_b.H_G.per_model.internvl3_8b.at_tau_G.sum_m|i}}. There is no test hypothesis about the guard and no test guard claim. InternVL3's τ = {{FC:models.internvl3_8b.tau|raw}} was chosen on KTVIC dev299 and kept unchanged.

**Table 11. Stage B results, for the reader only; they set nothing at test.**

| row | OV-dev-B ({{LISTS:counts.ov_dev_b|i}}) | XM-dev500 ({{LISTS:sets.xm_dev500.#len|i}}) |
|---|---|---|
| pooled `ret` − `rand` | {{DF:ov_dev_b.gate.pooled_vs_rand|e}} (gate {{DF:ov_dev_b.gate.verdict|vw}}) | {{DF:xm_dev500.S1|e}} |
| Qwen2.5-VL | {{DF:ov_dev_b.gate.per_model.qwen25vl_7b.vs_rand|e}} | {{DF:xm_dev500.detail.per_model.qwen25vl_7b.vs_rand|e}} |
| InternVL3 (τ = {{FC:models.internvl3_8b.tau|raw}}) | {{DF:ov_dev_b.gate.per_model.internvl3_8b.vs_rand|e}} | {{DF:xm_dev500.detail.per_model.internvl3_8b.vs_rand|e}} |

**Table 12. Secondary, motivated by stage B (post hoc at stage B, pre-specified at test): InternVL3 `ret` − `rand` at τ = −∞. The τ = {{FC:models.internvl3_8b.tau|raw}} column holds per-backbone reported rows with unadjusted CIs.**

| set | InternVL3, registered τ = {{FC:models.internvl3_8b.tau|raw}} (shown first) | InternVL3, τ = −∞ (secondary) | label |
|---|---|---|---|
| OV-test primary | {{OV:P1b.internvl3_8b|e}} | {{OV:secondary_devb_motivated.internvl3_neg_inf.ov_test_1941|e}} | {{OV:secondary_devb_motivated.internvl3_neg_inf.ov_test_1941.label|vw}} |
| OV-test full | {{OV:sets.ov_test_2001.detail.per_model.internvl3_8b.vs_rand|e}} | {{OV:secondary_devb_motivated.internvl3_neg_inf.ov_test_2001|e}} | {{OV:secondary_devb_motivated.internvl3_neg_inf.ov_test_2001.label|vw}} |
| XM-test2500 | {{XM:per_model.internvl3_8b|e}} | {{XM:secondary_devb_motivated.internvl3_neg_inf.xm_test2500|e}} | {{XM:secondary_devb_motivated.internvl3_neg_inf.xm_test2500.label|vw}} |
| XM-test2500 without three-reference images | {{XM:sets.xm_test2392.detail.per_model.internvl3_8b.vs_rand|e}} | {{XM:secondary_devb_motivated.internvl3_neg_inf.xm_test2392|e}} | {{XM:secondary_devb_motivated.internvl3_neg_inf.xm_test2392.label|vw}} |

This row changes no verdict and no scope sentence. InternVL3's registered result is the τ = {{FC:models.internvl3_8b.tau|raw}} column. On OV-test, the same decodes without the deletion step show a detected `ret` − `rand` difference for InternVL3. On XM-test2500 they do not.

**Table 13. Stage-B decomposition of InternVL3's contrast (post hoc, development data only; not a test result).** Recomputed on CPU from the stage-B ledger with the registered bootstrap. The τ = {{FC:models.internvl3_8b.tau|raw}} column reproduces the stage-B decision file exactly, and the build asserts it.

{{TABLE:devb}}

At stage B, the deletion step lowered InternVL3's `ret` scores more than its `rand` scores on both development sets. This is a description of development data and is not tested here.

### 6.8 Compute

The test used {{CHAIN:xm_total|p}} GPU-hours of the {{C:gpu_cap|i}} GPU-hour cap, on one 24 GB GPU:
- the OpenViIC block: {{CHAIN:ov_gpu_h|p}} GPU-hours ({{GS:3|i}} s);
- the XM3600 block: {{CHAIN:xm_gpu_h|p}} ({{GS:4|i}} s);
- the decode-parity checks before the test: {{CHAIN:e4r3_total|p}} (Section 7.1).

Verified precision and all decision steps ran on CPU. The development stages used {{C:dev_gpu_s1|p}} and {{C:dev_gpu_s2|p}} GPU-hours, under a separate development cap.
