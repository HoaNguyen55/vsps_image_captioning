# 10 Discussion and implications

## 10.1 What the results say together

The paper's claims are about the instrument: an object-level score responds to gold completeness, object count and reference exchangeability, separately from object choice. The concern that gains come from saying less is not new (Section 2).

- **Gold completeness.** On XM3600 (registered), F1's verbosity slope is ordered by gold completeness and positive under complete gold, but two of five registered predictions failed, on the all-references slope, without triggering demotion (Section 7.5).<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: prereg_comparisons[16..20].in_interval_or_pass = PASS, FAIL, PASS, PASS, FAIL; .session_backup/2026-10-18/paperA_tasks/A4.1/MANIFEST.json :: verdicts[14] = NOT_FIRED; sentence per manuscript/paperA_plan/CONFIRMATION_MAP.md (cbed6db) §2 --> A second-backbone test is pending; the multi-reference sign is not predicted by the theory.
- **Count.** The registered leaderboard failed its fidelity check and was not scored (Section 6.4), so no confirmatory count-control claim is made; the seed placebo admitted the matched prefix (Section 6.3).<!-- src: .session_backup/2026-10-13/decisions/PD-15.txt :: items 1-2; sentence per manuscript/paperA_plan/CONFIRMATION_MAP.md (cbed6db) §3 NOT-TESTABLE --> E1 is post hoc.
- **Exchangeability.** An adjacency statistic tests reference exchangeability (Section 5).

Human evidence (Section 8) supports the confound: long-caption judgments penalize naming more objects (registered). Count-matched precision does not track humans better: it failed on THumB and Composite (frozen locally) and LongCap-Arena, and DOCCI-Critique's G3-(ii) held with an interval including 0.

We report a count-controlled column for construct validity, not agreement with humans: count moves the score mechanically, so a comparison that leaves it free cannot attribute a difference to object choice (Section 3.7).

## 10.2 Implications for practice: the two-column reporting standard

Every object-level claim of the form "method S hallucinates less than B" should report two columns (Section 3.7):

1. **Raw score,** with gold, matcher and $M$ named.
2. **One pre-declared count-controlled difference:** the per-image matched-count difference with a paired interval (the matched prefix, admitted by the Section 6.3 placebo), or the frontier residual for training-time methods; other controls go into a specification curve.

The second column says whether a difference remains when count is held fixed, not which caption is better: a method that names fewer objects with an unchanged ranking of candidates shows a raw gain and a null second column.

## 10.3 Implications for practice: a checklist

For papers that report object-level hallucination scores:

1. **Name the gold and the matcher,** and report $M$ for every system.
2. **Do not compare F1 across verbosity regimes under incomplete gold** without locating the systems relative to the F1 optimum: the sign with several references is not predicted by any current theory (Section 7).
3. **Pre-declare the count control,** calibrate it with a seed placebo, and report its interval, with other controls in a specification curve.
4. **Vary references with random subsets,** not file order, and report the adjacency statistic (Section 5).
5. **For human-validity claims,** report count-equal and count-differing pairs separately; do not call a count-controlled score a better quality measure without a registered test.
6. **For preference data,** report the object-count difference of chosen and rejected responses, not only length (Section 9).
7. **Commit predictions before the outputs exist,** and label predictions frozen locally but never committed, or committed after a result, as exploratory.

## 10.4 Implications for research

Three lines of research follow.
- **Metric theory.** The sign result applies to any object-, attribute- or relation-level score with reference-built gold; a predictor of where the sign changes is still missing (Section 4.3).
- **Gold construction.** Benchmark builders can report gold completeness and reference exchangeability; denser labels move an evaluation toward the large-gold regime.
- **Mitigation and training.** Methods that claim better object choice need a count-controlled evaluation, and preference data can be audited for the count channel (Section 9).

A score that removes the count confound and also tracks human judgments better remains an open problem: matching on count alone does not provide it (Section 8).

## 10.5 Conclusion

Object-level hallucination scores measure the gold and the number of objects a caption names, not only object choice. In a registered out-of-sample test on XM3600, F1's verbosity reward is ordered by gold completeness and positive under complete gold, but two of its five registered predictions failed<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: prereg_comparisons[16..20].in_interval_or_pass = PASS, FAIL, PASS, PASS, FAIL (N1-XM-2 and N1-XM-5 FAIL); qualifier per manuscript/paperA_plan/CONFIRMATION_MAP.md (cbed6db) §2 --> (N1-XM-2 and N1-XM-5, on the all-references slope). The multi-reference sign and the crossing point are not predicted; a second-backbone test is pending. The registered count-matched leaderboard failed its fidelity check and was not scored, so we make no confirmatory count-control claim; the registered seed placebo found the matched prefix admissible. Human judgments penalize object count on long captions, but count-matched precision does not track them better than raw precision, so count control is a control for a confound, justified by construct validity. Papers comparing object-level scores should report the raw score next to one pre-declared count-controlled score, name their gold and check reference exchangeability.

## 10.6 Open items before submission

[PENDING items that change text in this section when they land: B3 (Section 7.7). G2-B, A-N1 and A-N2 landed 2026-10-20 (Section 7.6); this section's wording still needs the writer pass.]<!-- Resolved in the cut pass: the E1 K2 placebo (HELD; matched prefix admissible) and N9 (fidelity check failed, not scored); .session_backup/2026-10-13/decisions/PD-15.txt -->
