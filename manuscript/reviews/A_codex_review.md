# External review: Signal Processing: Image Communication

## Scores (1–5)

- **Novelty: 3/5.** Treating the gold set as an experimental factor and quantifying verbosity effects is a useful measurement contribution. The incremental novelty over prior metric-validity, incomplete-judgment, and length-control work needs sharper demarcation.
- **Correctness: 3/5.** The empirical reporting is unusually candid about failed predictions and sensitivity limits. The principal ordering claim is not robust across the paper’s registered datasets, and parts of the theoretical framing exceed what is established for the reported metric.
- **Contribution: 3/5.** The audit and reporting recommendations may help evaluators, but the count-control evidence is exploratory, its planned confirmation was not run, and the proposed reporting procedure is not validated as a better measure.
- **Clarity: 2/5.** There is substantial methodological detail, but the main narrative is difficult to follow through registration IDs, nested qualifications, and changing gold/vocabulary definitions.

## Recommendation

**Major revision.** The work has a potentially publishable measurement-audit contribution, but its headline claim and theoretical interpretation should be narrowed and the reproducibility/permission record reconciled before acceptance.

## Major issues

1. **The central ordering does not replicate on the strongest external reference-set test.** PASCAL-50S supports the increase from one to 50 references, but the 50-reference-to-VOC-label component fails (−2.29, CI includes zero); the abstract and discussion must foreground that this limits the headline generalization. The second-backbone result uses the same XM3600 images, so it is a model replication, not independent image-set replication. [sec7_verbosity_sign.md:86-99] [sec10_discussion.md:5-7]

2. **The theory and primary outcome are mismatched.** Proposition 1’s closed form and single-crossing result are explicitly exact for micro-F1, whereas the primary registered tables report mixed F1 (micro precision plus image-averaged recall). The supplementary mixed-F1 condition does not establish the same monotone ordering/single-crossing result. Frame the proposition as a result for micro-F1 and distinguish it from the empirical mixed-F1 finding throughout. [sec3_measurement_setup.md:10-16] [sec4_theory.md:8-19] [supplementary_SPIC.md:30-34] [sec7_verbosity_sign.md:5-7]

3. **The reported evidence is hard to independently audit.** Key files are restricted; PASCAL-50S captions were deleted and no hashes retained, leaving only rerunning the full decode as a route to reproduce verdicts. Provide a durable reviewer-accessible package with executable scoring, per-image sufficient statistics or reproducible predictions where licensing permits, and a clear statement of what can be independently checked. [sec6_rescoring_published_methods.md:51-55] [declarations.md:17-19] [sec11_limitations_ethics.md:34]

4. **Resolve conflicting permission statements.** The limitations say written permission for UIT-OpenViIC use was not obtained, while Data availability says UIT-OpenViIC and KTVIC authors confirmed the use in writing. This is material to the legality and reproducibility of the aggregate analysis; reconcile the statements and clarify the permitted use. [sec11_limitations_ethics.md:25-29] [declarations.md:17-19]

5. **The central measurement claim depends on a consequential scoring choice.** On XM3600, verified precision excludes mentions labels cannot verify; counting them as errors makes the second-backbone label-gold slope interval include zero. Explain why this is the preferred estimand, quantify how many mentions are excluded, and state the narrower conclusion under the alternative rule in the abstract/conclusion. [sec3_measurement_setup.md:7-10] [sec7_verbosity_sign.md:16-17, 45-52] [sec11_limitations_ethics.md:9-13]

## Minor issues

1. **Sharpen novelty positioning.** The paper says no prior work fixes object count per image, but the related-work table does not systematically compare this against the closest length/count controls and gold-quality studies. State the precise difference and avoid broad “none” claims unless the search scope supports them. [sec2_related_work.md:1-34]

2. **Reduce registration-ledger load in the main text.** The many statuses, IDs, intervals, and caveats obscure the substantive result; keep a concise headline summary in the article and move the full ledger/provenance to the supplement. [sec1_introduction.md:44-77]

3. **Make metric labels consistent.** Section 7 says its rows report mixed F1, while the supplement says every Section 7 table reports both F1 variants. State exactly which tables and figures use mixed versus micro-F1. [sec7_verbosity_sign.md:5-7] [supplementary_SPIC.md:30-34]

4. **Clarify the reporting proposal’s scope.** The matched-prefix control assumes salience ordering, yet the random-subset control yields materially different conclusions and the registered leaderboard failed fidelity. The proposal should specify when each control is interpretable and avoid implying a generally validated correction. [sec3_measurement_setup.md:25-35, 45-49] [sec6_rescoring_published_methods.md:18-49]

5. **Complete submission-facing placeholders.** The manuscript still contains an author-confirmation placeholder for dataset licences and says the reviewer access link will be inserted at submission. Resolve these before submission and ensure the access path is present for reviewers. [sec11_limitations_ethics.md:33] [declarations.md:17-19]
