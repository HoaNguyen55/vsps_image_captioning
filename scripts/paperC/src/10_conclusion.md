## 10. Conclusion

We asked whether retrieved example captions help two open MLLMs caption Vietnamese images more than random captions from the same memory. We answered with a preregistered study, one look per test set.

**In domain.** On the OpenViIC test, retrieval beat random examples by {{OV:P1|e}} stripped CIDEr-D points pooled, P1 {{OV:P1.passed|v:pass}}. The gain is carried mainly by Qwen2.5-VL and was not detected for InternVL3. On OpenViIC test, neither model lost count-matched object precision against its own zero-shot captions.

**Out of domain.** On XM3600 Vietnamese the gain was not detected ({{XM:XM_a|e}}), and the registered XM3600 prediction is {{XMB:XM_prediction|vw}}.

**Controls.** In domain, the registered S-zf row puts `ret` − `zs` at {{OV:S_zf.pooled_vs_zs|e}}, against P1's `ret` − `rand` of {{OV:P1|e}}. (The `rand` − `zs` comparison itself is descriptive and post hoc, from Table 5.) The per-backbone `ret` − `rand` rows are model-dependent: on OpenViIC test, the CI is above zero for Qwen2.5-VL and includes zero for InternVL3. A random-example control at equal k, drawn from the same memory, is needed before a gain over zero-shot is attributed to retrieval.

**Data and code availability.** We release the registrations, the test code, the decision files, the per-image score ledgers, image ids and hashes. No caption from any dataset and no model caption is released. [Repository link withheld for anonymous review.]
