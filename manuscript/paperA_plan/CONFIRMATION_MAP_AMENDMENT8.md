# CONFIRMATION MAP, Amendment 8

**Status.** Drafted by the A-writer, 2026-10-26, under the judge's CC-104 (abstract options to a CP round as input,
82%; `.session_backup/2026-10-13/decisions/CC-104.txt`) and CP-091 Q2 (final A pass: ≤ 240 words), for the judge.
Committed by the gatekeeper together with the text it changes.

**Scope.** Wording only, for length:
- the base is option 2 of the internal abstract input, as recorded in CC-104 (word diff, l.70-74), taking only the edits
  that keep CC-104's conditions:
  - the frame sentence (row 43) is unchanged;
  - "In public human judgments" (row 38) is unchanged;
  - every number is byte-identical;
- option 2's rephrasing of the XM3600 qualifier is not taken. Row 25 is the PD-28 rename, verbatim, and row 27 is a
  fixed bracket sentence. Its "but" → "yet" change is not taken either, since it saves no word;
- the two source comments in the abstract now sit after their full stops, not before. The text is unchanged, and the
  two word counts become equal;
- no registered verdict, verdict rule, fill rule, selection logic, precondition or number changes.

## Sentence pairs

| # | Place | Old sentence | New sentence | Verdict | Strength |
|---|---|---|---|---|---|
| 45 | abstract, C2 s1 (rows 2, 44) | In confirmation tests, F1's slope on log object count is ordered by gold completeness (expected for nested reference golds) and positive under label gold on XM3600 and, with a second Qwen backbone (Qwen3-VL-8B), on the same 600 XM3600 images and 295 discovery images (a UIT-ViIC pass is not counted: possible image exposure). | In confirmation tests, F1's slope on log object count is ordered by gold completeness (expected for nested reference golds) and positive under label gold on XM3600 and, with Qwen3-VL-8B (second Qwen backbone), on the same 600 XM3600 and 295 discovery images (UIT-ViIC pass uncounted: possible image exposure). | C2 PASS (unchanged) | same |
| 46 | abstract (row 36, s1) | The registered negative one-reference slopes held; post hoc, dropping any system never changes the label-gold sign, but XM3600's one-reference slope turns positive (+10.52, not −8.99) without one verbose system. | The registered negative one-reference slopes held; post hoc, dropping any system keeps the label-gold sign, but XM3600's one-reference slope turns positive (+10.52, not −8.99) without one verbose system. | N1-XM-1 PASS, G2B-E1 PASS x3 (unchanged); post hoc LOO | same |
| 47 | abstract (row 37) | A registered count-matched leaderboard failed its fidelity check and was not scored, so no count-control claim is confirmatory; re-scoring 15 published comparisons is post hoc. | A registered count-matched leaderboard failed its fidelity check and went unscored, so no count-control claim is confirmatory; re-scoring 15 published comparisons is post hoc. | C1 NOT-TESTABLE (unchanged) | same |

The abstract is 240 words after rows 45-47. With HTML comments removed it is 240 whitespace tokens, the method that
reproduces Amendment 7's 247. With each comment replaced by a space it is also 240; it was 249 before.

The old wording of rows 46 and 47 ("never changes the label-gold sign"; "failed its fidelity check and was not scored")
also occurs outside the abstract, and is left unchanged there: cover_letter_A.md:10 (row 46); cover_letter_A.md:11,
sec1_introduction.md:9 and sec10_discussion.md:38 (row 47).
