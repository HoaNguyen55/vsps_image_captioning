# Revision notes: TAIMMA draft v2 to v2.1 (step R1 of CC-414)

Written 2026-11-15T04:45Z (date -u). Ruling: `.session_backup/2026-10-13/decisions/CC-414.txt`, sha256 eb218211289597419fae17f19f645ba38e062d438d7c622559e40614d9d74be6.

`draft_v2/` is frozen and byte-unchanged (all eight files re-hashed after the work; `paper.md` d97cd24a…). `draft_v2_1/` started as a copy of it. `REVISION_NOTES.md`, `DRAFT_NOTES.md` and `V1_TO_V2.diff` in this folder are the unchanged v2 files.

## 1. Pairs applied

All eight OLD/NEW pairs of Annex A, in the ruled order, by a script that reads each pair from the ruling file between its marker lines. Each OLD matched exactly once before its write; each NEW is the ruling's bytes. Nothing else in `paper.md` was changed (`V2_TO_V2_1.diff`: 6 hunks, 6 changed lines).

| pair | status in the ruling | unit | section | words, OLD to NEW (whitespace count) |
|---|---|---|---|---|
| W1 | BLOCKING | S3-05 | §3 | 26 to 79 |
| W2 | BLOCKING | S2-05 | §2 | 37 to 39 |
| W3 | BLOCKING | S4-04 | §4 | 32 to 70 |
| W4a | BLOCKING | S5-04 | §5 | 11 to 18 |
| W4b | BLOCKING | S6-03 | §6 | 9 to 26 |
| N1 | NON-BLOCKING, ruled "apply" | S4-03 (B2 gloss) | §4 | 40 to 27 |
| N2 | NON-BLOCKING, at the writer's choice; applied | S4-03 | §4 | 9 to 35 |
| N3 | NON-BLOCKING, at the writer's choice; applied | S3-05 | §3 | 10 to 11 |

N2 costs 26 words; if the page count of G1 is too high, it is the first of these pairs that the ruling allows to be taken back ("if pages allow").

## 2. Word count (checker's counter, running text)

Before (v2): 4,521. After (v2.1): 4,647. Change: +126. The ruling's estimate was "about 4,610" from W1 to W4 and N1; it did not add N2 (+26) and N3 (+1), and the checker counts W1 at +52 where the ruling wrote +44.

| section | v2 | v2.1 | plan | v2.1 against plan |
|---|---|---|---|---|
| Abs | 212 | 212 | 200 | +12 |
| §1 | 505 | 505 | 500 | +5 |
| §2 | 346 | 348 | 330 | +18 |
| §3 | 705 | 757 | 620 | +137 |
| §4 | 587 | 638 | 560 | +78 |
| §5 | 712 | 719 | 700 | +19 |
| §6 | 348 | 362 | 380 | −18 |
| §7 | 698 | 698 | 540 | +158 |
| §8 | 206 | 206 | 160 | +46 |
| Decl | 202 | 202 | 110 | +92 |

## 3. Checker

`check_draft.py` 281e0875… (unchanged), run inside `draft_v2_1/` with `python3 -I -B`: `--sync-first-words`, then `--build-manifest ../WRITING_PLAN_C_TAIMMA_v1.md` (plan 0d4cb107…), then plain mode to `CHECKS.md`. Paper C repo at HEAD 55315ca; its md files, manifest (83414dc3…) and bib (a415c4da…) as in the ruling.

- Sync: 79 rows; one row changed (S2-05 first six words, from W2). No other column of `PARAGRAPH_SOURCES.tsv` was edited.
- Manifest build: 303 of 303 Annex D1 pairs found, 295 rows written, 7 pairs not printed (the same 7 as in v2). The new manifest is byte-identical to the v2 manifest (506ab1d6…): not even a section list changed, because the NEW texts add no number.
- Plain mode: 12 of 13 PASS; the one FAIL is the known word-budget check.

| check | result | measured |
|---|---|---|
| Paragraph markers and PARAGRAPH_SOURCES.tsv | PASS | 79 units, 79 rows, 54 of 54 claim-map rows carried |
| Limits known today | PASS | title 14 words, abstract 212 words, 5 keywords, 7 tables, 1 figure |
| Plan word budgets | FAIL (known) | 4,647 against 4,100 planned |
| Numbers keyed | PASS | 417 numeric tokens, 0 without a row |
| Estimate and CI read from one key | PASS | 86 triples, 0 without a single key stem |
| Manifest rows equal the source manifest and are all printed | PASS | 295 rows (27 label rows), 0 problems |
| Registered negatives and labels (plan A.5) | PASS | 24 required statements, 0 missing |
| Citation keys exist in the bib | PASS | 34 keys used, 0 not in the bib (67 entries) |
| No host or IP pattern | PASS | 0 hits |
| No writing-tool statement | PASS | 0 hits |
| No promotional word | PASS | 0 hits |
| No journal-only content | PASS | 0 hits outside the allowed sentences, 4 allowed |
| No data-set caption text | PASS | 0 Vietnamese letters, 0 unexpected quoted strings |

Nothing in the ruling's NEW texts made the checker flag anything beyond the word budget (§2, §3, §4 and §5 rise; §6 stays under its budget).

## 4. Left open (not part of R1)

- `PARAGRAPH_SOURCES.tsv` column 3 was not edited: the checker does not require it. The journal sources the ruling names for the new sentences (W1: 09 l.24; W3: the multiplicity bullet of 05; N2: the thresholds paragraph of 05; N3: 06 l.93) should be added at the G2 refresh, which re-points every row to the new journal HEAD.
- N4 (Table 1 caption and the Li et al. row), N5 (search works) and the N8 list wait for G2 or later, as ruled.
- N6: `CHECKS.md` still opens "TAIMMA draft v1": a fixed string of the unchanged checker. The file describes draft v2.1 (`paper.md` f65f53ab…).
- N7: section 5a of `REVISION_NOTES.md` cites the search file as acdae5aa; that is the sha of its first 47,582 bytes. The file `manuscript/reviews/C_SYSTEMATIC_SEARCH_2026-11-15.md` is now 8613bdf9, with Part 7 appended (both values from the ruling; not re-hashed here).
- Next step of the ruling: R2, the preliminary LNCS build of v2.1 for the page count.

## 5. Files (sha256)

| file | sha256 |
|---|---|
| `paper.md` | f65f53ab991cb7d2f94908ae9681b7d19fa8d53fa30571216ad209d07e267c35 |
| `number_manifest_TAIMMA.tsv` | 506ab1d6a9a7ff5d042b865314776b2d9e7130454ef4d1cef061fba9ce5cb6c6 |
| `PARAGRAPH_SOURCES.tsv` | 619a5e07bcfed3fb6787be4685b8d350d09fd1af5e0b13b1c1681e9c86cc13b4 |
| `CHECKS.md` | 328daf2ff973f7d36f1c817a1d243b952eaf3d90a7949350a1ff62d71ca88976 |
| `V2_TO_V2_1.diff` | 42660b4abb1dbc631976033f158e9ca1c3ca3f3188a51a812c24e2f9ab9e0a0c |
| `check_draft.py` | 281e087565af30c0ba8ae62dc56d466b4d9c85659d09e822a7666c8300bda21f |

No label folder, key file, sealed folder or held folder was opened. No commit was made.
