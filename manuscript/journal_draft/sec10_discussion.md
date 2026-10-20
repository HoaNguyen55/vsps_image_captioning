# 10 Discussion and implications

## 10.1 What the results say together

- **Gold completeness (confirmatory).** F1's verbosity slope is ordered by gold completeness and positive under complete gold on XM3600, where two of five registered predictions failed without triggering demotion, and with a second backbone on the same 600 images as Section 7.5 (Sections 7.5–7.6).<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: prereg_comparisons[16..20].in_interval_or_pass = PASS, FAIL, PASS, PASS, FAIL; .session_backup/2026-10-18/paperA_tasks/A4.1/MANIFEST.json :: verdicts[14] = NOT_FIRED; sentence per manuscript/paperA_plan/CONFIRMATION_MAP.md (cbed6db) §2 --> Under nested golds the ordering is also expected under random missingness, so this supports the pattern, not the propensity model.
- **Secondary registered results.** Condensed F1 is MIXED (Section 7.6) and the human span-label test is NOT_SUPPORTED (Section 8.5); the eight-LVLM test is summarized in Section 10.5.
- **Count (no confirmatory claim).** The registered leaderboard was not scored (Section 6.4), so no confirmatory count-control claim is made; the seed placebo ran in its failed harness and supports no count-control claim.<!-- src: .session_backup/2026-10-13/decisions/PD-15.txt :: items 1-2; sentence per manuscript/paperA_plan/CONFIRMATION_MAP.md (cbed6db) §3 NOT-TESTABLE -->
- **Exchangeability.** An adjacency statistic tests reference exchangeability (Section 5).

Human judgments penalize naming more objects on long captions, but count-matched precision does not track them better (Section 8); the count-controlled column rests on construct validity (Section 3.7).

## 10.2 Implications for practice: the two-column reporting standard

Every object-level claim of the form "method S hallucinates less than B" should report two columns (Section 3.7): (1) the **raw score,** with gold, matcher and $M$ named; and (2) **one pre-declared count-controlled difference:** the per-image matched-count difference with a paired interval, or the frontier residual for training-time methods, with other controls in a specification curve. We use the matched prefix; a seed placebo admitted it, but that placebo is a calibration, not validation (Section 6.3). The second column says whether a difference remains at fixed count, not which caption is better.

## 10.3 Implications for practice: a checklist

For papers that report object-level hallucination scores:

1. **Name the gold and the matcher,** and report $M$ for every system.
2. **Do not compare F1 across verbosity regimes under incomplete gold** without locating the systems relative to the F1 optimum (Section 7).
3. **Pre-declare the count control,** calibrate it with a seed placebo, and show other controls in a specification curve.
4. **Vary references with random subsets** and report the adjacency statistic (Section 5).
5. **For human-validity claims,** report count-equal and count-differing pairs separately.
6. **For preference data,** report the chosen-minus-rejected object-count difference, not only length (Section 9).
7. **Commit predictions before the outputs exist,** and label the rest exploratory.

## 10.4 Implications for research

The decomposition applies to any object-, attribute- or relation-level score with reference-built gold, but a predictor of where the sign changes is missing (Section 4.3). Benchmark builders can report gold completeness and reference exchangeability. A score that removes the count confound and also tracks human judgments better remains an open problem (Section 8).

## 10.5 Conclusion

Object-level hallucination scores respond to the gold and to the number of objects a caption names, not only to object choice. In a registered out-of-sample test on XM3600, F1's verbosity reward is ordered by gold completeness and positive under complete gold, but two of its five registered predictions failed<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: prereg_comparisons[16..20].in_interval_or_pass = PASS, FAIL, PASS, PASS, FAIL (N1-XM-2 and N1-XM-5 FAIL); qualifier per manuscript/paperA_plan/CONFIRMATION_MAP.md (cbed6db) §2 --> (the all-references sign and the sign agreement, both on the all-references gold). With a second backbone (Qwen3-VL-8B, detailed captions capped at 160 new tokens) the registered primary claims hold on the same 600 images as Section 7.5 and replicate on 295 COCO discovery images; the ordering would also arise under random missingness, and the multi-reference sign and the crossing point are not predicted. In a registered secondary test on eight public LVLMs, one-reference F1 does not rank the models as complete gold does (ranking prediction passed), but the per-model pattern failed for qwen3vl_8b on discovery images (per-model ladder prediction failed; every detailed caption of that model reached the 160-token cap), so it is not claimed for every public LVLM. The registered count-matched leaderboard failed its fidelity check and was not scored, so no count-control claim is confirmatory. Human judgments penalize object count on long captions, but count-matched precision does not track them better than raw precision: count control is a control for a confound, justified by construct validity. Papers comparing object-level scores should report the raw score next to one pre-declared count-controlled score, name their gold and check reference exchangeability.<!-- A-N2 conclusion per PD-23 (a): LBA-P1 PASS, LBA-P2 FAIL, KA2 wording, hit_max disclosure (CP-041). §10.6 "Open items" removed (PD-23 readability); B3 status in Section 7.7. -->
