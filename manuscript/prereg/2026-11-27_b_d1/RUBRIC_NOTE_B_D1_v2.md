# How far B-D1/A3 could move the rubric, v2 (PRELIMINARY; RUBRIC_v1 sha256 3071ed8d…, journal weights)

v2 follows prereg v2: H3 now asks about tone placement beyond a scorer-and-tokenizer grid, with the 5% band; A3's rule is on the per-member level. Probabilities are from CC-505 ruling 8, PRELIMINARY.

Starting point: BENCH_B_2026-11-27 gives a total of 62.2 before K0, with C2 = 2, C4 = 3, C5 = 3. One level is worth 2.4 points on C2 (weight 12), 2.0 on C5 (weight 10) and 1.2 on C4 (weight 6). The levels below are read from the anchor text, not from the benchmark's deltas. Every level is PRELIMINARY until a scorer reads the revised text.

| outcome | C2 (anchor read) | C5 (anchor read) | C4 (A3) | change in total |
|---|---|---|---|---|
| H3 SUPPORTED and H1 or H2 SUPPORTED | 2 → 3. "a new combination, setting or language for known elements" now has a measured element: tone placement overturns more than 5% of the certificates of a grid that already varies scorer, unit, punctuation and case. 4 is unlikely, because the rule is still Lu's union-of-ties. With the 5% band this outcome needs a large effect, so its chance is below CC-505's 0.20 for the v1 bands | 3 → 4. "compared with suitable baselines or alternatives; its parts are tested at least in part" (margin, AER, axis ablation) | — | +4.4 |
| H3 SUPPORTED only | 2 → 3 (same reason) | 3 → 4 is possible: the baselines were compared even though FE-CERT did not beat them. It rests on the judge's reading of "justified design" | — | +2.4 to +4.4 |
| H1 or H2 SUPPORTED only, H3 NULL, INCONCLUSIVE or NOT_EVALUABLE | stays 2: the gain is over baselines, not a new element against Lu et al. | 3 → 4 | — | +2.0 |
| NULL everywhere (H1/H2 NOT SUPPORTED or NOT_EVALUABLE, H3 NULL) | stays 2 | 3, or 4 at most: the comparison with strong baselines was made and reported, but it shows no advantage. Anchor 4's "justified design" is weakened | — | 0 to +2.0 |
| MARGIN BETTER or AER BETTER | stays 2 | could fall to 2 ("a proposed procedure whose own test failed"), or stay at 3 if the comparison is read as an honest test | — | −2.0 to 0 |
| A3 AT OR BELOW NOMINAL | — | — | 3 → 4 **only if a scorer accepts** the sentence "the per-member bootstrap was at or below its nominal level, and the intersection rule cannot raise the certificate's level above it" as tying the guarantee to a tested prediction (anchor 4). A3 tests the per-member level, not the intersection rule (CC-505 B4). CC-505 halves this row in expectation | 0 to +1.2 |
| A3 INCONCLUSIVE or ABOVE NOMINAL | — | — | stays 3. ABOVE NOMINAL forces a revision of §4.4 | 0 |

- **Expected change (CC-505 ruling 8):** about +1.4 points, with a range of 0 to +5.6. D1 does not reach 80 in expectation.
- **Best case from today:** 62.2 + 4.4 + 1.2 = 67.8, before K0.
- **Against the benchmark's ceiling.** The ceiling is 79.2: every K item, with A1–A3 at their best (A3 included).
  - Adding D1 gives 81.6 with C2 → 3, and 83.6 with C5 → 4 as well.
  - Under NULL, the total passes 80 only if C5 is read at 4 **and** every K item and A1–A2 are at their best: 79.2 + 2.0 = 81.2. A1 and A2 have low odds in the benchmark (0.25 and 0.45). So **under NULL, 80 is unlikely through D1**. The next step is then S2 (new decodes, development data only), as the benchmark notes.
- A NULL reported plainly costs nothing on C7, and integrity condition H1 stays clean.
- **Not affected:** C6, C8 and C10. C3 depends on K0 only.
