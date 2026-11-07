# Codex read-only review: Paper A S1.M package (2026-11-07T19:2xZ)

Subject: the four files in manuscript/prereg/2026-11-07_a_m1/s1m/, at these sha256 values:
- S1M_DRAFT.md 31b634fd
- S5_TABLE.md b4d1a344
- MAIN_SENTENCE.md a48fe05d
- COMPANION_EDITS.md 0c8eee1e

They were checked against the registered plan A_M1_PLAN_v3.md, the ruling CC-288 and data/results/a_m1/a_m1_result.json. Codex ran read-only and edited no files. The coordinator transcribed its findings below.

## Findings (by severity)

1. **High: Remark 3 vs CC-288** (S1M_DRAFT.md:65-67; S5_TABLE.md:27)
   - Remark 3 and the S5 note discuss classes no writer would name.
   - CC-288's MAY NOT list forbids statements about classes no writer names, yet its MAY list also explicitly permits Remark 3, so the ruling conflicts with itself.
   - Fix: the read should grant an explicit carve-out before the text is transferred. Without one, omit Remark 3 and the related S5 sentence.
2. **Medium: unverified citation** (S1M_DRAFT.md:9-13, 38-39, 51; COMPANION_EDITS.md:18)
   - The exact source of the (k−1)/k incidence factor and the citations listed are unverified. CC-288 N5 and the plan require verification before citation.
   - Fix: verify the full texts and correct the attribution. Until then, remove the source-specific attribution.
3. **No other findings**
   - Lemma 1, Proposition 2 and Remark 3 and their proofs are correct.
   - The bound directions are correct: Ĉ is an upper bound on coverage, and Ŝ and m̂ are lower bounds.
   - Every number matches the result file at its cited key, with the displayed rounding.
