# 10 Discussion and implications

## 10.1 What the results say together

- **Gold completeness (confirmatory).** F1's verbosity slope is ordered by gold completeness and positive under label gold on XM3600 and with a second backbone on xm600 (Sections 7.5–7.6).<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: prereg_comparisons[16..20].in_interval_or_pass = PASS, FAIL, PASS, PASS, FAIL; .session_backup/2026-10-18/paperA_tasks/A4.1/MANIFEST.json :: verdicts[14] = NOT_FIRED; sentence per manuscript/paperA_plan/CONFIRMATION_MAP.md (cbed6db) §2 --> Section 10.5 qualifies it.
- **Secondary registered results.** Condensed F1 is MIXED (Section 7.6) and the human span-label test is not supported (Section 8.5).
- **Count (no confirmatory claim).** The registered leaderboard was not scored (Section 6.4), and the seed placebo ran in its failed harness; neither supports a count-control claim.<!-- src: .session_backup/2026-10-13/decisions/PD-15.txt :: items 1-2; sentence per manuscript/paperA_plan/CONFIRMATION_MAP.md (cbed6db) §3 NOT-TESTABLE -->
- **Exchangeability.** An adjacency statistic tests reference exchangeability (Section 5).

The count-controlled column rests on construct validity (Section 3.7), not on human judgments (Section 8).

## 10.2 Implications for practice: the two-column reporting standard

Every object-level claim of the form "method S hallucinates less than B" should report the two columns of Section 3.7, with other controls in a specification curve. We use the matched prefix; a seed placebo admitted it, but that placebo is a calibration, not validation (Section 6.3).

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

The decomposition applies to any object-, attribute- or relation-level score with reference-built gold, but where the sign changes is not predicted (Section 4.3), and a score that removes the count confound and tracks human judgments better remains open (Section 8).

## 10.5 Conclusion

Object-level hallucination scores respond to the gold and to the number of objects a caption names, not only to object choice. In a registered out-of-sample test on XM3600, F1's verbosity reward is ordered by gold completeness and positive under human-verified labels, scored with verified precision (mentions OIV7 cannot verify are excluded), and it is positive only when unverifiable mentions are excluded; counting them as errors removes the positive slope (post hoc)<!-- src: data/results/n_f1/bracket_result.json (sha256 4796ed12) :: outcome_paper = ii, sentence_paper; per set: sets.s75.outcome_from_lower = i, sets.xm600.outcome_from_lower = ii (paper-level AND, DESIGN.md R3, CC-063); design c8bd21c; run record manuscript/prereg/2026-10-21_n_f1_bracket/run_record.json (062ab6a5); VERIFIED manuscript/verification/paperA/N_F1_bracket_run.json (60e58bfe; byte-identical re-run); CONFIRMATION_MAP Amendment 4 row 27 -->; two of its five registered predictions failed<!-- src: .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json :: prereg_comparisons[16..20].in_interval_or_pass = PASS, FAIL, PASS, PASS, FAIL (N1-XM-2 and N1-XM-5 FAIL); qualifier per manuscript/paperA_plan/CONFIRMATION_MAP.md (cbed6db) §2 --> (the all-references sign and the sign agreement, both on the all-references gold). With a second Qwen backbone (Qwen3-VL-8B, detailed captions capped at 160 new tokens; how many reached the cap is unknown) the registered primary claims hold on the same 600 XM3600 images and replicate on 295 COCO discovery images; only the reference rungs are nested, so their ordering would also arise under random missingness, and the multi-reference sign and the crossing point are not predicted. In a registered secondary test on eight public LVLMs, one-reference F1 does not rank the models as complete gold does (ranking prediction passed), but the per-model pattern failed for Qwen3-VL-8B on discovery images (in that test every detailed caption of the model reached the 160-token cap), so it is not claimed for every public LVLM. The registered count-matched leaderboard failed its fidelity check and was not scored, so no count-control claim is confirmatory. Human judgments penalize object count on long captions, but count-matched precision does not track them better (Section 8).<!-- A-N2 conclusion per PD-23 (a): LBA-P1 PASS, LBA-P2 FAIL, KA2 wording, hit_max disclosure (CP-041). §10.6 "Open items" removed (PD-23 readability); B3 status in Section 7.7. -->
