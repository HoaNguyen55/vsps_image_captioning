## 10. Conclusion

We asked whether retrieved example captions help two open MLLMs caption Vietnamese images more than random captions from the same memory. We answered with a preregistered study, one look per test set.

**In domain.** On the OpenViIC test, retrieval beat random examples by +4.49 [3.52, 5.57] stripped CIDEr-D points pooled, P1 PASS. The gain is carried mainly by Qwen2.5-VL and was not detected for InternVL3. On OpenViIC test, neither model lost count-matched object precision against its own zero-shot captions.

**Out of domain.** On XM3600 Vietnamese the gain was not detected (+0.70 [−0.45, 1.97]), and the registered XM3600 prediction is not confirmed.

**Controls.** In domain, the registered S-zf row puts `ret` − `zs` at +14.30 [13.38, 15.24], against P1's `ret` − `rand` of +4.49 [3.52, 5.57]. (The `rand` − `zs` comparison itself is descriptive and post hoc, from Table 5.) The per-backbone `ret` − `rand` rows are model-dependent: on OpenViIC test, the CI is above zero for Qwen2.5-VL and includes zero for InternVL3. A random-example control at equal k, drawn from the same memory, is needed before a gain over zero-shot is attributed to retrieval.

**Data and code availability.** We release the registrations, the test code, the decision files, the per-image score ledgers, image ids and hashes. No caption from any dataset and no model caption is released. [Repository link withheld for anonymous review.]
