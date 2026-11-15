# Revision notes: TAIMMA draft v3 (cut) to v3.1 (ruling CC-421 applied)

Written 2026-11-15T11:09Z (date -u). This file is the addendum that CC-421 N5 asks for: `REVISION_NOTES_V3.md` and `CUT_PLAN.md` stay as the record of the proposal and are byte-unchanged copies here. Nothing was committed.

Ruling: `.session_backup/2026-10-13/decisions/CC-421.txt`, sha256 a8f0e5ebfff8eba65d158450ab75f5cb8c2242b33f1eae52bc03db61731f33f4 (CONDITIONAL GO 87 for Option B; conditions W1 and W2, closed by byte match). CC-414 (eb218211289597419fae17f19f645ba38e062d438d7c622559e40614d9d74be6) was read in full; CC-421 overrules its Ruling 2 (c4) in two places (C27 may leave whole; the NoCaps domain rows, C41, may leave the English table) and leaves the rest standing.

Place of the work: CC-421 step S1 names `draft_v3_cut/`; the coordinator's order was to apply it in a copy, `draft_v3_1/`, and to leave `draft_v3_cut/` byte-unchanged. The target sha256 values of the ruling apply to the files, not to the folder, and are compared below. All nine files of `draft_v3_cut/` were re-hashed after the work and equal the values in the header of CC-421.

## 1. Pairs applied

Applied by a script that read each OLD and NEW from the ruling file between its markers (no text retyped); each OLD was counted in its target file before its write and occurred exactly once. Order: W1.1 to W1.7, then W2a, W2b.

| pair | file | what it does | OLD count | state |
|---|---|---|---|---|
| W1.1 | check_draft.py | adds `CUT_RULED` (C27, C28, C41, C42, C43) and `N_TABLES, N_FIGURES = 4, 0` | 1 | applied |
| W1.2 | check_draft.py | paragraph rows: an absent row fails unless it is in `CUT_RULED`; a row of `CUT_RULED` that is carried fails; the summary names the five | 1 | applied |
| W1.3 | check_draft.py | table and figure counts read from the two constants (were 7 and 1) | 1 | applied |
| W1.4 | check_draft.py | limits title built from the constants; the word-budget check becomes "Plan word counts (information only ...)" with result INFO | 1 | applied |
| W1.5 | check_draft.py | title string "draft v1" becomes "draft v3 (cut)" (closes CC-414 N6) | 1 | applied |
| W1.6 | check_draft.py | prints INFO for a check without a pass/fail result | 1 | applied |
| W1.7 | check_draft.py | return code 0 unless a check is FAIL | 1 | applied |
| W2a | paper.md, S4-02 | "passed the same filter" becomes "passed the filter of Sect. 3" | 1 | applied |
| W2b | paper.md, S6-01 | "after the same filter rules" becomes "after the filter rules of Sect. 3" | 1 | applied |

NON-BLOCKING items of CC-421: the ruling marks none of them as applied, and none was applied. N1 waits for the re-join; N2 is a build setting; N3 is optional and "only if the build leaves the line"; N4 is closed as moot; N5 is this file; N6 is carried. The three NON-BLOCKING pairs of CC-414 (N1, N2, N3) were already in the v2.1 text and are still in `paper.md` (checked by string: "it equals the stage-A value", "The floors of P2 and XM-b", "a neighbour-only precision change").

Not changed, on purpose: the header comment of `paper.md` still reads "DRAFT v3 (CUT PROPOSAL, not ruled)". The ruling gives a target sha256 for `paper.md` after W2a and W2b alone, so the comment was left as it is; it is not printed. No number was changed, added or removed.

## 2. Results against the targets of the ruling

| file | sha256 after the work | target in CC-421 | result |
|---|---|---|---|
| check_draft.py | c07066475cfb703d1dbd1e4e4e8161aac8666cd7c5a4e580d465a0d8d70c8dc0 | c07066475cfb703d1dbd1e4e4e8161aac8666cd7c5a4e580d465a0d8d70c8dc0 (W1) | EQUAL |
| paper.md | b42eecb1c8e574af98ade56902fae0676a440f6cfd579dd8690984be5ee6692d | b42eecb1c8e574af98ade56902fae0676a440f6cfd579dd8690984be5ee6692d (step S1) | EQUAL |
| checker, plain mode | return code 0; 12 PASS, 1 INFO, 0 FAIL | return code 0, 12 PASS, 1 INFO (step S1) | EQUAL |

Files for which the ruling gives no target: `number_manifest_TAIMMA.tsv` 65fa8654d61f5fa2f811652eab73a21c8e03103dbf3554f5c720ae15ef1ff933 and `PARAGRAPH_SOURCES.tsv` a1838b7c069dff98eb69294a3e90d5e11b00a868522a296086be8706cfc07d94, both rewritten by the checker's helper modes and both byte-equal to the files of `draft_v3_cut/` (the ruling expected no edit of PARAGRAPH_SOURCES); `CHECKS.md` cb87b53678f374d866be889e83376480e646bc1a58093b1aad8b6e72c8a3c44a (new; it carries a time stamp).

The diff of the checker and of the paper is `V3_TO_V3_1.diff` (`diff -u` of `paper.md`, then of `check_draft.py`): 2 changed lines in `paper.md`, 9 removed and 18 added lines in `check_draft.py`.

## 3. Checker, three modes

Run inside `draft_v3_1/` with `python3 -I -B`: `--sync-first-words` (72 rows, return code 0), then `--build-manifest ../WRITING_PLAN_C_TAIMMA_v1.md` (plan 0d4cb1079110655f61dadd35598dd2111ff68fdbc4ec209ac46ef4abc53abf78; 303 Annex D1 pairs, 303 found, 0 missing; 251 rows written, 51 pairs not printed; return code 0), then plain mode to `CHECKS.md` (return code 0). Paper C repo at HEAD 55315ca with only `tex/` files modified, so the checker read HEAD content (`number_manifest_C.tsv` 83414dc3..., `paperC.bib` a415c4da...).

| check | result | measured |
|---|---|---|
| Paragraph markers and PARAGRAPH_SOURCES.tsv | PASS | 72 units, 72 rows, 49 of 54 claim-map rows carried; cut by ruling CC-421: C27, C28, C41, C42, C43 |
| Limits known today (abstract 150 to 250 words, 4 tables, 0 figure) | PASS | title 14 words, abstract 212 words, 5 keywords, 4 tables, 0 figure |
| Plan word counts (information only) | INFO | running text 4526 against 4100 planned; over: Abs +12, §3 +143, §4 +101, §7 +184, §8 +46, Decl +92 |
| Numbers keyed (token -> manifest row, by section and claim) | PASS | 344 numeric tokens, 0 without a row |
| Estimate and CI read from one key | PASS | 74 triples, 0 without a single key stem |
| Manifest rows equal the source manifest and are all printed | PASS | 251 rows (27 label rows), 0 problems |
| Registered negatives and labels (plan A.5) | PASS | 24 required statements, 0 missing |
| Citation keys exist in the bib | PASS | 27 keys used, 0 not in the bib (67 entries) |
| No host or IP pattern | PASS | 0 hits |
| No writing-tool statement | PASS | 0 hits |
| No promotional word | PASS | 0 hits |
| No journal-only content | PASS | 0 hits outside the allowed sentences, 4 allowed |
| No data-set caption text | PASS | 0 Vietnamese letters, 0 unexpected quoted strings |

The mutant that the judge ran (C27 put back in the sources file without a change of the constant) was not repeated here.

## 4. Word count

Checker counting rule (unchanged): running text 4,526 words (4,522 in the v3 cut draft; +2 in Section 4 from W2a and +2 in Section 6 from W2b), table cells 518, captions and notes 156. Title 14 words, abstract 212 words, 5 keywords, 4 tables, no figure. The word count decides nothing; the page count of the LNCS build decides (CC-414 Ruling 2, CC-421 Ruling 4).

## 5. Page estimate after the changes

From `PAGE_BUDGET.md` (490b4ba7..., unchanged): the v3 cut draft is estimated at 14.40 pages of content, a 15-page PDF in the default layout (about 14.47 in the other layout). It is an estimate from one measured build of v2.1, not a count.

Effect of W2a and W2b under the same model (83 characters per line, factor 1.13, 12 pt per line, 562 pt per page): each pair adds 6 characters, about 0.08 of a line, so the modelled total moves by less than 0.01 page and stays **14.4 pages of content, a 15-page PDF**. If each of the two paragraphs happens to run over into one more line, the total is 14.44. The checker edits print nothing.

The judge's own reading of this estimate (CC-421 Ruling 5): chance of 15 pages or fewer about 75 with today's placeholders and about 60 to 65 once the author block, the licences and the acknowledgment are in (0.2 to 0.4 page, not in the count). The next build is provisional and runs on the next rented host session, in both layouts and once more with dummy text of realistic length in the placeholders.

## 6. What is cut next if the build exceeds 15 pages (CC-421 Ruling 5)

One step at a time, measuring after each, stopping as soon as it fits; every step goes through the checker in its three modes and into the log line of the build.

- k0: layout only, no text and no class change: fix the overfull boxes; let no heading stand alone at a page foot.
- k1: S3-07, delete the sentence "The equal number of mentions keeps a longer caption from being penalised for naming more objects."
- k2: S1-03, delete the sentence that lists the four prompts ("Two open MLLMs caption each image under four prompts: ... and zero-shot (`zs`).").
- k3 (last resort): the per-arm table (marker T5, printed Table 2) with the second sentence of S5-08 and the first sentence of S8-03. Then "Table 3" and "Table 4" become "Table 2" and "Table 3" everywhere; in S7-D12 "the English score of each arm" becomes "the score of each arm"; the dagger of the S5-09 heading is re-worded at the re-check; constants `N_TABLES` 3 and `CUT_RULED` plus C29 and C54.
- Still over 15 pages after k3: STOP and report to the investigator. No plan A.5 row, registered negative, label, sensitivity, post hoc row, Section 7 bullet, compute line or declaration is cut for length. The S4-03 sentence on the floors of P2, XM-b and rule L is not on the cut list.

If the dummy-filled build leaves room (15 pages with the last page at most 0.6 full after the restore), the ruling restores in this order: r1 the copy baselines as one clause (C27 out of `CUT_RULED`); r2 the S2-04 sentence on other Vietnamese captioners with its three references; r3 the NoCaps rows by domain label (C41 out of `CUT_RULED`); r4 the S2-02 sentence on text-driven in-context learning. The figure and the sets table do not come back.

## 7. Blind card

`calibration_ccis/CARD_OURS_v3_1_PROVISIONAL.md` was written from this `paper.md` in the format of `CARD_OURS_v2_1_PROVISIONAL.md`. Changes against the v2.1 card follow the cut: the copy baselines left the method and baseline lines; the NoCaps numbers by domain label left the failure analysis; the positioning line describes two sentences in place of a table; the card says that the paper has no figure. Every number on the card occurs in `paper.md` (checked by script). The two key files of that folder were not opened.

## 8. Not done here

No build, no page count of record, no re-join, no rubric scoring, no log line, no commit. Open steps are S2 to S8 of CC-421 Ruling 7.
