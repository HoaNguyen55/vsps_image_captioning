# 10 Discussion and recommendations

## 10.1 What the results say together

The paper's claims are about the instrument. The concern that hallucination gains can come from saying less was raised before us (Fazli et al., 2026; Sandhu et al., 2026; Long et al., 2026; Nguyen et al., 2026; Section 2); what this paper adds is a pre-registered, per-image count-matched measurement of it, the gold-completeness ordering of the verbosity sign, an exchangeability check for references, and a count audit of preference data. An object-level score responds to three properties of the measurement that are separate from object choice: how many objects a caption names, how complete the gold is, and whether the references behind the gold are exchangeable. Each changes conclusions in practice.

- **Count.** Most published precision gains of decoding methods are not significant once both captions name the same number of objects per image under an order-preserving control; how many survive depends on the control, from 2 to 6 of 15 (Section 6). The registered placebo that decides between the controls is pending, so the paper states the curve, not one number.
- **Gold completeness.** The slope of object F1 on the number of mentioned objects rises with gold completeness in every completed test, never crosses back, and is negative with one reference and positive with instance labels. The sign with several references is not predicted by the theory: frozen predictions of a positive all-references slope failed on two English LVLM families and on XM3600, it was positive on COCO-2500, and on UIT-ViIC it depends on the matcher (Section 7). Raw F1 can rank the same two systems in opposite orders under two common golds.
- **Exchangeability.** Reference-count analyses assume exchangeable references; a cheap adjacency statistic separates corpora where the assumption holds from corpora where it does not (Section 5).

The human evidence (Section 8) supports the existence of the count confound: on long captions, human judgments penalize naming more objects (LongCap-Arena, registered). It also supports complete gold and matched count as conditions for a valid comparison on short COCO captions (registered on Polaris). It does not show that count-matched precision tracks human judgments better than raw precision: that registered prediction failed on THumB, Composite and LongCap-Arena and was inconclusive on DOCCI-Critique. This is a finding about what count control is for: attribution, not a better quality score. We therefore make no claim about what humans prefer, and the recommendations below concern reporting, not a new metric.

## 10.2 The two-column reporting standard

Every object-level claim of the form "method S hallucinates less than B" should report two columns (Section 3.7):

1. **Raw score,** with the gold and the matcher named, and the mean number of mentioned objects per image $M$ for both systems next to it.
2. **One count-controlled difference, declared before scoring:** the per-image matched-count difference with a paired, image-clustered interval for decoding and selection methods (matched prefix unless the seed placebo of Section 6.3 selects another control), or the frontier residual at the system's own count for training-time methods. Other controls go into an appendix specification curve.

The second column answers a different question from the first. It says whether a difference survives when count is held fixed; it does not say which caption is better. A method that names fewer objects with an unchanged ranking of candidates will show a raw gain and a null second column, which is an accurate description of what it does.

## 10.3 Checklist

For papers that report object-level hallucination scores:

1. **Name the gold and the matcher,** and report $M$ for every system. State whether the gold comes from references, instance labels or both, and how many references.
2. **Pre-declare the count control** and report its interval. Report the specification curve over the other registered controls in an appendix. Run a seed placebo for the control before using it as the primary column.
3. **Do not compare F1 across verbosity regimes under incomplete gold** without saying which side of the F1 optimum the systems sit on. Under one-reference gold, F1 rewards terseness; under instance gold, it rewards verbosity; with several references, the sign depends on the systems and the dataset, and no current theory, ours included, predicts it (Section 7).
4. **Vary references with random subsets,** never in file order, and report the adjacency statistic of Section 5 before calling a dataset's references "annotators". Do not report leave-one-reference-out "human ceilings" or species-richness completeness estimates on corpora that fail it.
5. **For human-validity claims,** report agreement separately on count-equal and count-differing pairs, and do not present a count-controlled score as a better quality measure without a registered test.
6. **For preference data,** report the distribution of the object-count difference between chosen and rejected responses, not only the length difference (Section 9).
7. **Register predictions in version control before the outputs exist,** and label every look that was not registered as exploratory. Where a registration was committed after a result, say so (as we do in Sections 7.5 and 8).

## 10.4 What this paper does not show

It does not show that any published method fails to reduce hallucination: count-controlled nulls at 500 images are nulls at that sample size (Section 6.3). It does not show that object count is a better control unit than word length on English LVLM outputs; that registered test failed. It does not locate the crossing point of the verbosity sign in advance; the frozen out-of-regime test on English LVLMs failed on location, and on XM3600 the registered prediction that 2–3 references already give a positive slope failed (1 of 3 out-of-sample sign predictions; below the registered demotion threshold of 2). It does not show that humans prefer count-controlled scores. The Vietnamese motivating case (the controlled baseline, the pre-registered negative results of the methods we tried, and the audit of the KTVIC references) is reported in the companion paper (Paper B, under review).

## 10.5 Open items before submission

[PENDING items that change text in this section when they land: E1 K2 placebo (primary control in 10.2 item 2), N9 (Section 6.4; the conditional kill of Section 9), G2-B (Section 7.6), B3 (Section 7.7).]
