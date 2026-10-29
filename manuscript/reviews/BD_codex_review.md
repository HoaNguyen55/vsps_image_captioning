# External review — journal_draft_B

## Scores (1–5)

- Novelty: 3/5
- Correctness: 3/5
- Contribution: 3/5
- Clarity: 4/5
- Recommendation: **Major revision**

## Numbered major issues

1. **The central two-panel interpretation is not causally identified.** The manuscript appropriately acknowledges that panel independence is unknown, that panel protocols and caption lengths differ, and that the training directions use overlapping but non-identical images. The forward and reverse slopes therefore cannot isolate a writer/reference-panel effect from other panel and training-design differences. Frame the results strictly as panel-specific score associations, and strengthen the design or narrow the explanatory claims. [sec5_results.md:64-65, 70-73; sec7_limitations_ethics.md:16]

2. **The core scaling evidence is limited to one model family and development data.** The KTVIC scaling result is trained at nested sizes with three seeds, but the two-panel experiment is on only 187 development images; the reverse direction has two seeds, and the paper says writer and protocol cannot be separated. The test-set result for the proposed final system is a registered failure. These constraints substantially limit generalization beyond this controlled setup; make this boundary prominent wherever the gain is presented as the main finding. [sec5_results.md:57, 64-65, 69-73; sec5_results.md:25; sec7_limitations_ethics.md:7, 16]

3. **The reusable kit is not yet independently usable from the manuscript.** The Zenodo DOI remains a placeholder, and the archive contents are described as a future deposit. As the kit is a principal contribution, provide a resolvable archive/repository and versioned instructions before acceptance, and ensure the archive matches the stated contents. [sec3_data_and_audit.md:74-78, 82; sec7_limitations_ethics.md:28]

4. **The benchmark-validity audit sometimes overreaches from association to mechanism.** The observed adjacency statistic is consistent with a single-writer process, but the text itself notes that the statistic is not specific to single writers and that the inference relies on KTVIC's documented interface. Likewise, the large punctuation effect is explicitly conditional on a scorer retaining punctuation; public baseline code removes punctuation, and the published-score pipeline is unknown. Keep causal/mechanistic language tightly aligned with these qualifications in the abstract and conclusions. [sec3_data_and_audit.md:19-21, 32-38; sec8_conclusion.md:5-7]

## Numbered minor issues

1. The paper invokes a 2026 conference version and says that the protocol, recipe, and P1 control are reused, but a full bibliographic entry is still pending. Complete the citation and make the distinction between reused and new material easy to verify. [sec7_limitations_ethics.md:38; sec4_system.md:3; STATUS.md:27]

2. Clarify the term “validated on external systems”: the manuscript defines it as an author-run test on three third-party checkpoints and explicitly says no outside group has run the kit. Consider using “tested on external checkpoints” in the abstract-level summary to avoid implying independent validation. [sec3_data_and_audit.md:80; sec7_limitations_ethics.md:24]

3. The limitations state that no new human judgments were collected, which appropriately limits claims about caption quality. Keep that distinction visible when discussing “better descriptions” and object support from a second caption panel. [sec7_limitations_ethics.md:11, 16; sec5_results.md:45]

4. Explain briefly in the main text why the exchangeability statistic counts object doubletons and uses adjacent slots; the reported result is central, while methodological detail is partly relegated to the supplement. [sec3_data_and_audit.md:19-21]

5. The opening and conclusion foreground precise score changes, but readers may miss that these refer to CIDEr-D ×100 under P0 and that a post hoc PTB-style row changes the punctuation result. Keep the protocol condition adjacent to each headline number. [sec1_intro.md:5, 12, 16; sec3_data_and_audit.md:34-38; sec8_conclusion.md:5]

## Overall assessment

This is a clear, careful audit/resource manuscript with a useful Vietnamese evaluation protocol and a potentially valuable two-panel scaling analysis. Its strongest contribution is the practical protocol and dataset audit; its broadest novelty claim is less secure because the critical panel comparison is small, development-only, directionally asymmetric, and confounded by panel protocol and length. I would reconsider after the authors narrow interpretation, clarify generalizability, and make the evaluation kit available as a stable, citable artifact.
