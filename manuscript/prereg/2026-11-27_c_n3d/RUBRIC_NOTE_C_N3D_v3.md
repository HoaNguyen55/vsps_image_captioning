# RUBRIC NOTE C-N3D v2 (v1 2026-11-27T12:14Z; revised under CC-509)

Rubric `RUBRIC_v1.md` (sha256 3071ed8d…), JOURNAL weights. The baseline is BENCH_C_2026-11-27: 76.4, with C9 at level 4.

## Target criterion: C9, Quality of analysis (weight 8)

Level 5 reads "analysis explains why the results arise: ablations or controlled contrasts, **error or failure analysis with categories**, subgroup or sensitivity analysis, alternative explanations tested, limits stated per claim". The paper already has every element except the categorised failure analysis.

In v2 the verdicts use placebo-differenced contrasts (W4, W5). A PASS can therefore no longer come from the score definition alone, and a reviewer has less reason to discount it.

| outcome | C9 level [P] | points | P(outcome) [P] |
|---|---|---|---|
| H1 or H2 PASS for at least one backbone (placebo-differenced) | 5 | +1.6 | about 0.3 |
| H3 PASS only | 5 is arguable | +1.6 at P about 0.4 | about 0.15 |
| NULL, **with the G0 rows and the placebo rows printed** [N3] | a categorised failure analysis exists (a level-5 element), but "why" is weak | +1.6 at P about 0.3 | about 0.55 |

Expected gain [P]: about +0.6 to +0.8 points. This matches CC-509 ruling 4.

**C9 credit for a NULL result is argued only if the G0 and placebo rows are printed. [N3]**

The route to 80 still needs K1 + K2:
- 76.4 + 2.0 + 1.4 + 1.6 = 81.4 if C9 reaches level 5.
- BENCH l.120 gives N3(d) "P 0.4 alone".
- BENCH l.105 gives P(all three) about 0.3–0.35. [N2]

## Other criteria

- **C2, C5:** no change. This is not a method, and it claims no new element. **No novelty is claimed for a categorised failure analysis; it is standard practice** [N3]. **C7:** neutral. **C8:** no change.
- **H1 honesty:** keep the development labels; §7 lists every number already seen, including the derivable SD of d and the W7 count.
- **H2 originality:** the categories reuse Paper C's own instruments and T8's list. N3D supersedes T8 (CC-509).
- **Integrity:**
  - no new gold, no AI-silver; the VLM verifier is excluded;
  - the verified labels are public OIV7 labels, not Paper A's gold;
  - no test set is used, and the W3 custody check runs before any decode file is opened;
  - no C-CONF host is used.

## What the round-2 judge should check

1. W4: the placebo-differenced Δ is computed with the same flag rules on the d1 caption against its own shown list.
2. W5: the H3 PASS conditions and the printed C_W, C_all, C_P− and C_P+.
3. W1–W3: the PUSH LIST and HASH-ONLY LIST, the host rule, and step 2a.
4. W6: Holm treats NOT DECIDABLE as p̃ = 1 with m = 6; the rng call is exact; the gold pins and loaders are fixed.
5. W7: the count of 335 appears in every OV-dev-B table note.
6. The new OQ-11: the OpenViIC dev annotation hash differs between the laptop copy and the pin.
