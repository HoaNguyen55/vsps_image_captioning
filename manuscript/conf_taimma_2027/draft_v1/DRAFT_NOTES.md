# DRAFT_NOTES: TAIMMA draft v1 of Paper C

Written by the drafting writer (an agent), 2026-11-14. This is a draft only. No tex was written, nothing was built, nothing was committed, nothing was sent.

## 1. Inputs, checked before writing

| Input | Value |
|---|---|
| Plan | `../WRITING_PLAN_C_TAIMMA_v1.md`, sha256 0d4cb1079110655f61dadd35598dd2111ff68fdbc4ec209ac46ef4abc53abf78. Checked at the start and again on resume; both match the CC-392 TARGET. |
| Ruling | `CC-392.txt`: rulings 1–8 and notes N1–N12 were read. N8, N9 and N11 are applied (section 4). N12 is marked for re-check (section 5). |
| Paper C | repo `vsps-paperC-tallip`, `paper_v1_analysis/` at HEAD d558df03c764641c1df2f938448776b5a69a8d80. Read-only; nothing was written there. |
| Source manifest | `number_manifest_C.tsv`, sha256 83a9ebc3930c3472…, unchanged from the plan. |
| Bib | `paperC.bib`, sha256 a415c4daa4d8c40b…, 67 entries, unchanged from the plan. |
| Venue facts | `manuscript/cfp/TAIMMA_CONF_2026-11-13.md`. |

No result file, label folder, key file, prereg folder or directions folder was opened, and no Paper A or Paper B draft was opened. Every number comes from Annex D1 of the plan, joined to the source manifest.

## 2. How the files were made

1. `paper.md` was written in the plan's drafting order (C.2): tables and Results first, then Method, Data and Disclosures, then Related work, Introduction, Conclusion and Abstract, and the declarations last.
   - Every paragraph, table and the figure carries an id marker (`<!-- p:ID -->`).
   - The sentences are re-worded, not lifted from Paper C. This follows the Springer code's text-recycling line (venue report §4; CC-392 N9).
   - Only the registered labels and the registered XM-a failure wording are copied verbatim.
2. `PARAGRAPH_SOURCES.tsv` was written by hand. Column 2 (first six words) was then filled by `python3 check_draft.py --sync-first-words`.
3. `number_manifest_TAIMMA.tsv` was built by `python3 check_draft.py --build-manifest ../WRITING_PLAN_C_TAIMMA_v1.md`, a build step run before the checks.
   - The step joins each of the 303 Annex D1 lines to the source manifest. It matches on the exact `file::key`, the number (minus sign normalised), the sha prefix and the status.
   - Result: 303 of 303 found, 0 missing.
   - The source manifest holds 4 of the keys twice (C44: the two development parity files, `identical` and `n`). The rows are equal except for their `used_in`, and the first row was taken.
   - A pair is written only if paper.md prints its value in a paragraph that carries its claim id. That gives 295 rows, 27 of them labels.
   - The first six columns are byte-copies of the source rows; the seventh gives the paper.md sections and the claim ids.
   - Seven Annex pairs are not printed: see section 3, item 4.
4. `CHECKS.md` is the output of `python3 check_draft.py`, the only check run. It reads paper.md, the draft manifest, PARAGRAPH_SOURCES.tsv, the source manifest and the bib.

## 3. Deviations from the plan

1. **Word budgets: over by 356 words of running text (about 9%).** The plan budget is 4,100 words; the draft measures 4,456. Thirteen checks ran: twelve pass, and only the "Plan word budgets" check fails.

   | section | measured | budget | difference | cause |
   |---|---|---|---|---|
   | Abstract | 233 | 200 | +33 | Inside the LNCS convention of 150–250 (to re-fetch). It holds both FAILs with estimate, CI and rule, the scope sentence, P2 in words, and InternVL3's COCO row in words (C50, C51). |
   | §1 Introduction | 509 | 500 | +9 | |
   | §2 Related work | 333 | 330 | +3 | |
   | §3 Method | 680 | 620 | +60 | The full count-matched definition (A8; D8) and the H_G negative (C06, placed in §3 as the plan allows). |
   | §4 Data and plan | 563 | 560 | +3 | |
   | §5 Results in Vietnamese | 713 | 700 | +13 | |
   | §6 English comparison | 385 | 380 | +5 | |
   | §7 Disclosures and limitations | 609 | 540 | +69 | The six disclosures added by CC-392 E3 came after the budget was set. All twelve disclosures, seven limitations and the compute line are kept, as a compact list. |
   | §8 Conclusion | 229 | 160 | +69 | The N8 clause on the S-NC sensitivity FAIL (C38), plus C22, C24, C54, C52 and C53, each in one clause. |
   | Declarations | 202 | 110 | +92 | The N11 short-form data statement (six data sets) and the `[PI]` placeholders. |
   | **Total** | **4,456** | **4,100** | **+356** | |

   - **Tables offset part of the overshoot:** table cells come to 836 words against the planned "about 1,000" (about 3,000 cut by two thirds), and captions and notes to 312 words.
   - **Pages are not measured.** No LNCS build was run (by rule). If the compiled PDF exceeds 15 pages, the plan's own cut order (section B) applies:
     - the English rows of Table 5 (C43);
     - Table 1;
     - C42;
     - C28;
     - C27.
   - Nothing in plan A.5 was cut to meet a budget.
2. **Manifest name and columns.** The task's file name `number_manifest_TAIMMA.tsv` and its seventh column are used, not plan A12's `number_manifest_C_TAIMMA.tsv` with `used_in` rewritten. The seventh column is `used_in_paper_md`: the sections, then the claim ids in brackets.
3. **Numerals outside Annex D1 are left out or written as words.** Among them:
   - the 299 and 300 of the KTVIC carve (Table 3 prints "–" for its size; "KTVIC dev299" is a set name);
   - the 2,011 OpenViIC dev files;
   - the 1,000 images behind the NoCaps 3,500;
   - the hash and SSCD cut-offs, the stage-A grid and its thresholds;
   - the SigLIP2 variant;
   - the "×100" (written as "the score times one hundred") and the "100 ·" of the ΔP_cm formula (written as "in percentage points");
   - every OpenFlamingo delta and shot count;
   - language and model counts in related work;
   - caption-length means; the 0.75 similarity cosine; the 121 and 295 earlier-contact counts;
   - the third model's 31/50 parity count and the ω values;
   - all dates and time stamps.
4. **Annex D1 pairs not printed (7 of 303).**
   - C08 `scope.row`: an internal row code. The scope sentence itself (`scope.sentence`) is printed.
   - C47: the four decision and job time stamps. The plan says they are not printed unless the PI wants them; the text says each decision file "carries its time".
   - C48: the two time stamps of the English-arm decision. The disclosure is stated in words.
   - For the PI (CC-392 N7): printing the registration times needs his yes.
5. **Placement of claims within the plan's options.**
   - C05 (stage-B gate) is in §4.
   - C06 (H_G "not passed") is in §3.
   - C16 is in §5.1.
   - Table 5 sits in §5 and keeps the English per-arm rows (C43) as the plan's C.4 asks. So C43's numbers are in §5, while the claim-map row lists §6; Table 5 is the first item on the cut list.
   - P2 (C13, C14) is in the abstract in words only (PASS, no numbers), and InternVL3's COCO row (C34) in words. Both follow C50 and the D07 disclosure.
6. **Data statement (N11): licences are `[PI]` placeholders, not "not reported by the dataset authors".**
   - The licence of each set is not in any source this task allowed me to open, so a written "not reported" would be an unchecked statement.
   - The placeholder tells the PI to write "not reported by the dataset authors" where nothing is documented.
7. **Declarations.**
   - Paper C's declarations hold no funding, acknowledgment or interests sentence, so all three are `[PI]` placeholders.
   - The dataset-authors' agreement sentence is a `[PI]` item, as plan A6 asks (no written confirmation is on record).
   - Availability uses the D9 default, "available from the authors on request", in place of Paper C's "released on publication".
   - No statement on writing tools or AI appears anywhere.
8. **Figure 1** is referenced by its existing file name, `fig1_ret_minus_rand.svg`, in the Paper C folder. It was neither copied nor redrawn. Plan C.4's vector rebuild from manifest values belongs to the build step on the rented host.
   - The SVG's text labels name only the four sets, the two backbones, "pooled", the scales and the axis ticks. It has no table pointer and no journal-only content.
   - The caption was re-worded and drops Paper C's pointer to its Tables 7, 8 and 11.
9. **"In words only" and the two carried facts.** The brief says the two facts carried from the journal-only part are stated in words only. That holds for the † note, which has no number and no pointer. The batch-composition limitation, however, prints 42/50 and 37/50: the plan's claim-map row C44 and CC-392 ruling 4 ("keep the two counts labelled development, non-confirmatory") require the counts. No other number from the attribution study appears.
10. **Table 1 (for the PI).** Its first column holds citation keys, which will render as bare "[n]" in the numeric LNCS style. At the build, add short names (for example "Yang et al. [n]").
11. **Display detail in CHECKS.md.** In the small-integer list, InternVL3's "50" and the second "52" show the Qwen2.5-VL row of the same value. The script prints the first covering row; the InternVL3 rows are in the manifest and carry the same value.

## 4. CC-392 notes carried to the draft

| Note | What was done |
|---|---|
| N8 | The conclusion states the S-NC sensitivity FAIL ("the registered sensitivity also fails"); a scripted check confirms it. |
| N9 | The text is re-worded rather than copied from Paper C, because the Springer code bars recycling text from the authors' own published manuscripts. The journal-direction terms (licence to publish) are still unknown; that bears on plan §G, not on this draft. |
| N11 | The short-form data statement gives one line per data set (source, language, role), with licence placeholders (deviation 6). |
| N12 | §5 and §7 were written now and are marked for re-check (section 5). |
| E1 / D8 | The count-matched definition is printed in full (§3) and attributed to "a companion manuscript by the same group (the object-precision study, in preparation)". No paper letter is named. |
| E3 | All six added disclosures are in §7: NoCaps image source, the English deletion-step port, the English SESOI, the English per-backbone row, re-use of test sets after the look, and the operational deviations. |
| Leaks 1 and 2 | The † note is words only: "conditional on the realised fixed set", with no number and no section pointer (Table 5, §5.3). The batch-composition limitation is §7, L06, with 52/52, 42/50 and 37/50, "development, non-confirmatory" and "no score was compared". |

## 5. Marked for re-check

- **§5 and §7: to re-check after 16 Nov 05:00Z (CC-392 N12).**
  - When: after 16 Nov 05:00Z (12:00 Vietnam time).
  - Run `--build-manifest` against the plan on the new Paper C HEAD; it repeats the Annex D1 join. Then run `check_draft.py`.
  - Rows C26 (the † label) and C44 (the 42/50 and 37/50 counts) come from the attribution part. The dated text changes touch that part (plan §0, E8), so both rows are re-checked then.
- The page count must be measured on the compiled LNCS PDF, together with every "re-fetch" item of plan §F: abstract length, keywords, whether references count toward the limit, the declarations and the citation style.

## 6. Open PI decisions that affect wording

| # | Decision | Where it shows in paper.md | Default used |
|---|---|---|---|
| D1 | Authors, affiliations, e-mails, corresponding author | `[AUTHORS: to be set by the PI]` | none (blocks submission) |
| D8 | Count-matched definition printed before the companion paper: (a) the companion paper goes out first and is cited here, or (b) the cost is accepted in writing | §3 S3-07 and the §4 mention of "the companion manuscript" | the attributed definition is printed; nothing is submitted before the PI answers |
| D9 | Public archive with a DOI, or "on request" | Data and code availability | "available from the authors on request" |
| D11 | Title | title line | working title of plan C.3, 14 words |
| – | Licence of each data set; the dataset-authors' agreement sentence; acknowledgments and funding; interests | Ethics and data statement; Acknowledgments; Disclosure of Interests | `[PI]` placeholders |

For the coordinator, not wording:
- N6: tell the PI that D10 (budgeted draft plus source table) is a reading of PI-1110p.
- N7: deposit the registrations before submission.
- N10: the one-line AI-policy gap goes in the "ready" notice.
- D12: the rubric step against CCIS papers comes before the "ready" notice.
