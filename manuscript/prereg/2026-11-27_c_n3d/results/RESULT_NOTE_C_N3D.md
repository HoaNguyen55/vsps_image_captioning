# Result note: Paper C, study C-N3D (registered result; DEVELOPMENT)

- **Written by:** an agent that is neither the study's coder, its operator, nor Paper C's writer (ruling CC-517, ruling 7).
- **Source:** the decision file C_N3D_DECISION.json (sha256 c2c65680bc9088daeeebde53f167c8b527eab70ab15c45de086f63cf236acfbf, byte-identical to the pulled file); consistent with the judge's recomputation (check_cc517_output.txt, CONSISTENT, 0 failures). Every number here and in the text package has a row in NUMBER_MANIFEST_N3D.tsv (`file::json-pointer`, raw value, check within half a unit of the last printed digit). The builder `build_n3d_package.py` also reproduces each value CC-517 quotes and every family line of the check output, or it exits.
- **Label of every row:** "DEVELOPMENT / C-N3D, NON-CONFIRMATORY; rule-based categories, no human labels". Development data only: OV-dev-B (n = 925) carries the rule; XM-dev500 (n = 500) and the English Flickr30K carve (n = 1,000) carry labels and no conclusion. Per backbone, never pooled.

## Design in three sentences

1. On stored batch-size-1 decodes, images are split by d = s(`ret`) − s(`rand` d0) (stripped CIDEr-D × 100) into losers L (d < −10) and winners W (d > +10), and by the placebo e = s(`rand` d1) − s(`rand` d2) into P− and P+; four rule-based flags (BO borrowed unsupported object, CP near-verbatim copy, ZL lost supported zero-shot content, LN length off) come from existing instruments.
2. H1 (BO) and H2 (ZL) test Δ_f = [Pr(f | L) − Pr(f | W)] − [Pr(f | P−) − Pr(f | P+)] ≥ +0.10 with a Holm-adjusted p̃ < 0.025; H3 tests coverage C_L = 1 − Pr(OTHER | L) ≥ 0.60 (p̃ for C_L ≤ 0.50), C_L − C_W ≥ +0.10 and a non-negative margin beyond the placebo.
3. One Holm family of six (H1–H3 × Qwen2.5-VL-7B, InternVL3-8B on OV-dev-B), one-sided α = 0.025, B = 2,000, seed 1127001, p̃ = (1 + k)/2,001; everything else is secondary or sensitivity, with no rule.

## Registered outcome (OV-dev-B, development data; labels exactly as the decision file prints them)

| hypothesis | backbone | estimand [95% CI] | p̃ | Holm-adjusted p̃ | verdict |
|---|---|---|---|---|---|
| H1 | Qwen2.5-VL-7B | +0.047 [−0.052, 0.144]; SR7 +0.16 | 0.1829 | 0.5487 | **FAIL** |
| H2 | Qwen2.5-VL-7B | −0.023 [−0.140, 0.095]; SR7 −0.06 | 0.6507 | 1.0000 | **FAIL** |
| H3 | Qwen2.5-VL-7B | 0.756 [0.690, 0.819] (C_L); C_L − C_W +0.157; beyond the placebo +0.036 [−0.094, 0.160] | 0.0005 | 0.0030 | **PASS** |
| H1 | InternVL3-8B | +0.115 [0.041, 0.194]; SR7 +0.52 | 0.0010 | 0.0040 | **PASS** |
| H2 | InternVL3-8B | −0.046 [−0.165, 0.066]; SR7 −0.17 | 0.7831 | 1.0000 | **FAIL** |
| H3 | InternVL3-8B | 0.752 [0.686, 0.808] (C_L); C_L − C_W +0.212; beyond the placebo −0.048 [−0.167, 0.062] | 0.0005 | 0.0030 | **FAIL** |

Groups |L| / |W| / |P−| / |P+|: Qwen2.5-VL-7B 168 / 359 / 211 / 191; InternVL3-8B 202 / 331 / 226 / 219; all ≥ 30, so no row is NOT DECIDABLE and the NULL row of registration §8 does not apply. InternVL3-8B H1 is "PASS", not "PASS (base-rate attributed)": its SR7 point (+0.52) has the sign of Δ, so falsifier 5 is not met.

**Secondary and descriptive rows (no rule).** G0 (E) and the exclusive shares S3 are in Tables S28 (a) and S29; S1 and S2 with their placebo twins in Table S31 (each with its coupling stated and its twin beside it, no sentence beyond the row); Aya-Vision-8B on OV-dev-B (S4, placebo flagged) and XM-dev500 (S5) in Tables 13b, S28–S30; SR1–SR7 in Table S32; English in Table S33. SR6 changes the largest exclusive category among the losers only for Aya-Vision-8B on OV-dev-B (falsifier 4 fires for that cell).

## What the result allows and forbids (ruling CC-517, rulings 4 and 5)

- **Allowed:** template T1 for InternVL3-8B only, with the Qwen2.5-VL-7B H1 row printed as FAIL beside it; T3 for Qwen2.5-VL-7B only, always with C_P− and C_P+ and the margin beyond the placebo (+0.036 [−0.094, 0.160]), with the InternVL3-8B H3 row printed as FAIL; T2 (FAIL) for both; the tables S3, G0 and the placebo rows; the English rows as description beside the OV-dev-B D^ret rows.
- **Forbidden:** that borrowed objects cause the loss; any statement across backbones; any reading of the Qwen2.5-VL-7B H3 PASS as specific to retrieval; that the rules explain why; anything about test sets, a transfer to XM-dev500 or a language difference; any rescue of a FAIL row; "trend"; Δ_CP or Δ_LN as findings; anything of this study in the abstract, the contributions list, the conclusion or a cover letter.
- **Judge's reading (CC-517 ruling 3):** falsifier 1 is met in form for Qwen2.5-VL-7B (the Δ_BO interval includes 0), which is why that H1 row reads FAIL. Falsifier 4 fires for Aya-Vision-8B on OV-dev-B only; for the family cells and XM-dev500 the exclusive tables may be printed.
- **Judge's reading (CC-517 ruling 4):** a mixed H3 (one PASS, one FAIL) has no row in registration §8; by analogy with the one-backbone H1 row, per-backbone wording and no general statement.

## Disclosures (CC-517 D1–D9)

1. **D1, three invocations.** The registered run completed on its third invocation; two earlier invocations stopped on code faults (an arm that is not flagged by the registration was passed to the flag step; a late-bound set index in a sensitivity row) before any study quantity was printed or written; the fixes changed no estimand. The first fix kept the zero-shot arm, which the registration uses only as a reference and never flags, out of the flag step, and added stops for an empty shown list and for an image without references. The second fix bound each cell's own image ids when the cell is created, so that a sensitivity row can no longer read the ids of the last set processed. Before the third invocation, the committed code ran unchanged, end to end, on a synthetic bundle that keeps only the structure of the pinned inputs (file names, keys, id sets and counts) with every caption replaced by seeded random text, and passed. Consoles 7380b532, 04ca4c7b and 2a584cf3; dry-run record b545d2d3.
2. **D2, host.** The study ran on the investigator's own PC, which until 2026-11-26 held unread committed test files as git objects (removed before this run); every input was pinned by sha256. A file-name scan of the PC's user folders before and after the run found no test-set file apart from committed name, id and hash lists and committed code of the group's studies, and no test image, test caption or test output; the run read those lists only for its custody check. The run ended, with its folder removed and the removal verified, before any later test-set work on that PC began.
3. **D3, software and parity.** Java on that PC was version 17.0.21.1, recorded and not pinned; it enters only the two tokenisers of the CIDEr-D scorers. The scorer parity gate passed on all 13 cells it checks (9 primary cells and 4 batched sensitivity cells): each cell's full-sample mean contrast equalled the printed value of Tables 11, S16, S17, S19 or S21 within 0.0051. It is a check of means, not of per-image scores, so the group memberships are verified only in aggregate.
4. **D4, overlap.** 335 of the 925 OV-dev-B images are OpenViIC development copies of the held-out set of a companion study of the group; none of them is a memory member (printed in every OV-dev-B table note).
5. **D5, Aya-Vision-8B.** placebo flagged on this set (Section 6.10.5) on every S4 row; falsifier 4 for that cell, so the multi-label flag rates are reported and not the exclusive ranking.
6. **D6, numbers already seen.** BO, CP and LN are labelled "shaped by aggregates already seen" (registration §7): neighbour-only object shares, near-verbatim copy shares and mean caption lengths on these sets had been printed before (Section 6.8 and Table S11).
7. **D7, POST HOC.** Group sizes below the planning values and the SR2/SR4 sign changes of the H3 margin; text in Section 6.10.10, "Post hoc observations" (PACKAGE.diff hunk 1).
8. **D8, undefined values.** SR7_CP is printed "undefined", never as a number. The decision file carries NaN and −Infinity tokens for these quantities (Python-JSON, not strict JSON); the bootstrap intervals drop the non-finite resamples.
9. **D9, limitation.** One bullet in Section 9.1 (PACKAGE.diff hunk 4): rule-based categories, matcher recall, incomplete reference-union gold, flag-score coupling, re-used development sets.

## Files and shas

- Registration: PREREG_DRAFT_C_N3D_v3.md 8648c167; ERRATUM_C_N3D_1.md a5f3df66; ERRATUM_C_N3D_2.md 8c14a253; SHA256SUMS c7950d6a.
- Code: scripts/c_n3d at e9a5898, CODE.sha256 3aaa9474 (c_n3d.py f61df892, c_n3d_host.py 05b3b827, test_c_n3d.py 9819dab1).
- Run: S0 6aeefd79; S0 statement 63ef5aff; custody 8be68f6f; run record 47c4ec62; consoles 7380b532, 04ca4c7b, 2a584cf3; deletion listing 08e44f2c; wipe find 082caaf9; post scan 85e2cc0b; pre scan 8606c002; C1 31751320. Ruling CC-517 (CONDITIONAL GO 88); judge check output f39caac3.
- Text of record: paper repo commit 9bf8f89, paper_v1_analysis/ 06, 07, 09, 11 (package in PACKAGE.diff; the tex is not rebuilt).
