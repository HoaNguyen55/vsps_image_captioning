# CONFIRMATION MAP, Amendment 6

**Status.** Drafted by the A-writer, 2026-10-22, under the judge's CC-088 A-1 (YES 92%,
`.session_backup/2026-10-13/decisions/CC-088.txt`), for the judge. Committed by the gatekeeper together with the post hoc
result `data/results/a1_robustness/a1_system_robustness.json` and the text it changes.

**Scope.** Wording after a post hoc analysis:
- the realized sentence "The one-reference slope is negative in every confirmation test (registered; the theory does
  not derive it)." (Amendment 4 row) is removed, as CC-088 makes binding, and replaced by row 36;
- rows 37-39 shorten three realized abstract sentences to keep the abstract within 250 words; no verdict or number in
  them changes;
- row 40 replaces highlight 2; rows 41-42 add one post hoc sentence each to the confirmatory-claim paragraph of §1 and
  to §10.5.
- No registered verdict, verdict rule, fill rule, selection logic or precondition changes. The registered one-reference
  predictions (N1-XM-1 PASS; G2B-E1 PASS on cv295, uv231 and xm600) keep their verdicts; what is removed is the
  generalisation "in every confirmation test", which the system-level analysis does not support.

**Timing.** Written after the post hoc analysis ran (2026-10-22). The analysis is POST_HOC, carries no verdict and
changes no registered verdict.

## Sentence pairs

| # | Place | Old sentence | New sentence | Verdict | Strength |
|---|---|---|---|---|---|
| 36 | abstract | The one-reference slope is negative in every confirmation test (registered; the theory does not derive it). | The registered negative one-reference slopes held; post hoc, dropping any system never changes the label-gold sign, but XM3600's one-reference slope turns positive (+10.52, not −8.99) without one verbose system. Inference concerns these Qwen-VL systems. | N1-XM-1 PASS, G2B-E1 PASS x3 (unchanged); post hoc LOO | weaker |
| 37 | abstract | A registered count-matched leaderboard of six public LLaVA-1.5-7B anti-hallucination checkpoints failed its fidelity check and was not scored, so no count-control claim is confirmatory; the post-hoc re-scoring of 15 published comparisons is exploratory. | A registered count-matched leaderboard failed its fidelity check and was not scored, so no count-control claim is confirmatory; re-scoring 15 published comparisons is post hoc. | C1 NOT-TESTABLE (unchanged) | same |
| 38 | abstract | Public human judgments give mixed evidence: LongCap-Arena Relevance falls with object count, … | In public human judgments, LongCap-Arena Relevance falls with object count, … (rest unchanged, MIXED kept) | MIXED (unchanged) | same |
| 39 | abstract | The length- and style-matched preference set VaPR is mostly but not fully count-matched (positive control, PASS). | The length- and style-matched VaPR preferences are mostly, not fully, count-matched (positive control, PASS). | PASS (unchanged) | same |
| 40 | highlight 2 | With a single reference, the F1 slope is negative in every confirmation test | Label-gold slopes survive dropping any system; reference-gold signs can hinge on one | post hoc | weaker |
| 41 | §1 claim paragraph | (added after "The negative one-reference slope is registered but not derived from the theory.") | Post hoc, at the system level (Section 7.8), the label-gold slope is positive and keeps its sign when any one system of a family is dropped; under reference gold the sign depends on the systems: on XM3600, dropping its one verbose system (the zero-shot detailed run) turns the one-reference slope from −8.99 to +10.52 and the all-references slope from −2.43 to +18.07. The intervals of Table 7.1 hold the systems fixed, so this inference concerns these Qwen-VL systems, not object F1 in general. | post hoc | added |
| 42 | §10.5 | (added after "… the multi-reference sign and the crossing point are not predicted.") | Post hoc, the label-gold slope keeps its sign when any one system is dropped, but on XM3600 the reference-gold sign rests on one verbose system (Section 7.8); these results concern these Qwen-VL systems. | post hoc | added |

The abstract is 249 words after rows 36-39 (HTML comments stripped, `wc -w`). Highlight 2 is 84 characters.
