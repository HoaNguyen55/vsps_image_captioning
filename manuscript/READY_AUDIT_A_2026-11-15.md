# Paper A (SPIC): submission-readiness audit, 2026-11-15

Audited 2026-11-15 09:08 UTC (16:08 Vietnam time). Paper repo `/mnt/d/vsps_papers/vsps-paperA-spic`, HEAD `0b542cf50edd097fa7c9f9327d6ac168c8898176`. No paper file was changed and nothing was committed. The only new files are this report and `manuscript/letters_2026-11-15/L2_KTVIC_v2.md`. The CAS build was run with `OUT` pointing at the session scratchpad; it wrote nothing into the repo (git status was the same before and after).

Rules applied:
- The checklist in `.claude/skills/venue-spic/SKILL.md`.
- The live-page facts in `manuscript/cfp/VENUE_RECHECK_2026-11-15.md`. The journal's guide for authors could not be read, so every item that rests only on that page is BLOCKED.
- The six criteria of `manuscript/GOAL_MOI_2026-11-15.md` §1.
- By the investigator's decision, no manuscript carries an AI statement. Its absence is not a defect.
- Hard rule: Section 6.7 (`paper/sec7_verbosity_sign.md` lines 124–247) and Supplementary S11 (`paper/supplementary_SPIC.md` lines 1172–1732) were scanned by script for counts only. Nothing from them is quoted here and none of their figures is reported. This report also does not restate any 6.7 outcome where it appears in other files; those places are given by location only.

## Counts

| Status | Items |
|---|---|
| READY | 14 |
| NOT READY (fixable by an agent; file and line given) | 15 |
| BLOCKED (needs the investigator, the unread guide, or an event in the goal order) | 10 |
| **Total** | **39** |

**Verdict: Paper A is not ready for submission.** Goal §2 item 4 (second annotator, the investigator's extra labelling session, the code run, and the update of 6.7 and S11) is still open, and so are the 15 fixable items below.

## Method and its limits

- **Build.** `paper/build/build_A_cas.sh` (CAS cas-sc, numbered references), with `OUT=` set to the scratchpad. The result is 38 pages. The LaTeX log has no undefined citation or reference.
- **Number check.**
  - The paper repo has no number-check script of its own. I used the vsps report checker `manuscript/bao_cao_khoa_hoc_2026-11-14/checks/check_part.py`, read-only, with `--src paper/number_manifest.tsv paper/figs/VALUES.json` only. The paper's own `.md` files were not used as sources, because that would be circular.
  - The checker tests only decimals, percentages and integers ≥ 100.
  - Section 7 was checked up to the end of 6.6 (lines 1–123). The supplement was checked from S1 to S10 (lines 1–1171).
  - A second pass accepted rounding: a token counts as found if some manifest value rounds to it. This pass accepts any of about 3,900 manifest values, so a match shows that a number *can* come from the manifest, not that it does.
- **Citations.** I used `prep.py cites` (author-year mentions mapped to bib keys) and the LaTeX log.
- **Scans.** Internal ids, tool names, placeholders and AI wording were found by regex over visible text, with HTML comments removed.
- **Code.** No test was run on the laptop, because tests run on the rented host. The scorer status is taken from the committed record.

## Items by criterion

### Criterion 1: scientifically complete

| ID | Status | Item | Evidence | Fix, or what is needed |
|---|---|---|---|---|
| A1-01 | BLOCKED | The second annotator has not labelled yet. Section 6.7 and S11 still have to be updated after the second-rater session, the investigator's extra labelling session and the code run. | `paper/declarations.md:27` ("has not yet labelled (Section 6.7.1)"); goal §2 item 4 | The order is in goal §2 item 4. Afterwards, update `declarations.md:27` and every place listed under "Custody flag" below. |
| A1-02 | READY | PASCAL-50S correction record (an open point in goal item 4) | `prereg/2026-10-28_pascal50s/CORRECTION_2026-11-15.md` is committed in the paper repo. `declarations.md:19` states the agreement as a fact, without "in writing", a date or "on file". | — |
| A1-03 | READY | KTVIC data statement matches the training use | `declarations.md:19` and `sec11_limitations_ethics.md:48`: "one of us contacted the KTVIC authors, who agreed to this use" sits beside the training sentence (3,769 images, captions as targets). | — |

### Criterion 2: numbers and citations are evidenced

| ID | Status | Item | Evidence | Fix, or what is needed |
|---|---|---|---|---|
| A2-01 | READY | Numbers in the abstract, highlights, cover letter, title page, declarations, Sections 1, 2, 4, 10 and 11, and `figs/CAPTIONS.md` | Every checked token was found as written in the manifest: abstract 9/9, cover letter 11/11, declarations 4/4, Section 1 46/46, Section 2 14/14, Section 10 14/14, Section 11 22/22, captions 6/6. Section 3 had 2 tokens and Section 7 up to 6.6 had 3 tokens that were found only after rounding. | — |
| A2-02 | NOT READY | Flickr30k interval bounds 0.478 and 0.488 have no manifest row | `paper/sec5_exchangeability.md:23` | Add two rows: `.session_backup/2026-10-14/r11_verify/c3_n2_exchangeability_all_datasets.json` :: `k5_exchangeability_audit.flickr30k_entities_chains_visual.adjacent_share_ci95[0]` (0.4783) and `[1]` (0.4884). The same file is at `results/session_backup/...` in the paper repo. |
| A2-03 | NOT READY | The Chao2 coverage bound 0.866 has no manifest row and no source was located | `paper/sec5_exchangeability.md:43`. There is no `src:` comment on the line; the value is not in the paper repo `results/` or in `data/results/a_dchecks/`; the manifest has no `a_dchecks` row. Its CI bounds 0.854 and 0.876 matched some manifest value, probably by coincidence. | Find the producing file (most likely the S1.M / Table S5.M run of the A certificate work). Then add rows for the point value and both CI bounds, or remove the sentence. The same source covers supplement lines 514–519 (A2-05). |
| A2-04 | NOT READY | 3,419 COCO-2014 images (A-N3) has no manifest row | `paper/sec8_human_validity.md:22`; also `supplementary_SPIC.md:1128` | Add a row: `data/results/a_n3/a_n3_run.json` (sha256 prefix `7a5a614d2068`) :: `checks.analysis_set.reproduced.images_analysis` = 3419. Its neighbour 13,997 is already manifest row 640. |
| A2-05 | NOT READY | 36 supplement numbers (S1–S10) are not in the manifest, even after rounding | `paper/supplementary_SPIC.md` lines 34 (1), 234 (1), 246 (1), 248 (2), 439 (2), 441 (1), 442 (2), 453 (1), 481 (2), 514 (5), 515 (2), 516 (3), 517 (1), 518 (3), 519 (4), 592 (1), 746 (1), 821 (1), 929 (1), 1128 (1). Eleven further hits were arXiv ids and page numbers (lines 38, 256, 538, 698) and are not defects. | Add manifest rows. Lines 439 and 481 use the A2-02 source. Lines 514–519 (Table S5.M / S1.M) use the A2-03 source, and `data/results/a_dchecks/gate.json` holds 10,388 as `cells.coco/F1/U.n_slots`. Line 1128 uses the A2-04 source. |
| A2-06 | READY | Every citation in the main text resolves | 118 author-year mentions matched to bib keys and 0 were left unmatched. One tie (sec2 "Zhou et al., 2024a") was resolved by the trace map. The build has 78 numbered references, 15 `[dataset]` tags and no undefined citation. | — |
| A2-07 | NOT READY | The supplement has no reference list. 30 works cited in S1–S10 are in no printed list. | `supplementary_SPIC.md` has no References heading. Keys cited in S1–S10 that are missing from the main list: bai2024hallucination, buttcher2007reliable, chen2024right, cheng2025caparena, esary1967association, fu2025mitigating, gupta2019lvis, huang2026capprobe, jain2016extreme, jing2024faithscore, karlin1968total, lee2025robust, liu2024survey, liu2025capability, long2026beyond, lu2016effect, lu2025benchmarking, napoles2011evaluating, nguyen2026metric, onoe2024docci, penquitt2026object, saito2025haldec, singh2024benchmarking, sun2019compare, wang2026detailverifybench, webber2009score, ye2025painting, yilmaz2006estimating, zhou2024aligning, zobel1998reliable. | Add a "References for the Supplementary Material" list built from `paperA.bib`: these 30 keys plus any S11 keys, the latter found by the agent that updates S11. Add it to `supplementary.md`, then regenerate `supplementary_SPIC.md`. The supplement keeps author-year citations while the main text is numbered; that is acceptable if the supplement has its own list. |

### Criterion 3: code, tables, figures and appendices checked

| ID | Status | Item | Evidence | Fix, or what is needed |
|---|---|---|---|---|
| A3-01 | READY | Scorer fidelity record | `docs/fidelity/FIDELITY.md`: every compared family is exact, 0 different. `docs/fidelity/R3_LOG.md`: clean-environment runs, last commit `1526b34`. Not re-run by this audit (tests run on the rented host). The Section 6.7 code run is still pending; it is part of A1-01. | — |
| A3-02 | NOT READY | Figure captions are missing from the manuscript. The built PDF prints only "Fig. 1", "Fig. 2" and "Fig. 3". | `paper/build/filter.lua` renders the image alt text as the caption. Images are at `sec3_measurement_setup.md:15`, `sec7_verbosity_sign.md:26` and `:92`, and Fig. S1 at `supplementary_SPIC.md:78`. The full captions exist only in `figs/CAPTIONS.md` (lines 5, 7, 9, 11). | Put each caption paragraph from `figs/CAPTIONS.md` into the source under its image, or make the build read it. Do not copy line 3 of `CAPTIONS.md`: it holds an internal id and file paths. |
| A3-03 | READY | Figure files | `paper/figs/fig1–fig4_*.pdf` are vector PDFs with all fonts embedded. `pdfimages` finds no raster image in the build. Each figure is a separate file. The publisher-wide rules were confirmed live (VENUE_RECHECK A15). Upload the PDFs: SVG is not on Elsevier's format list (A16). | — |
| A3-04 | READY | Tables and cross-references | All 12 tables have a bold "Table N." caption. Every "Section N.N", "Table N" and "Supplementary S…" pointer in the main text and in S1–S10 resolves to an existing heading or caption. Two hits were false: a citation's "Section 2.2" at supp:114 refers to Chao and Colwell, and one table label inside 6.7 was not matched by my caption pattern; it was not inspected (hard rule). | — |
| A3-05 | NOT READY | The supplement has no submission build | No script builds `supplementary_SPIC.md` into a PDF, and Fig. S1 is referenced as `.svg` (supp:78). The publish step `scrub_supp.py` would stop on its leak check because of hits inside S11 (V2_PROGRESS.md:63; counts in the "Held sections" table below). `supplementary_SPIC.md` is byte-equal to `scrub(supplementary.md)` (653 comments removed), checked by importing `scrub()`. | Add a pandoc build of `supplementary_SPIC.md` to PDF that uses `figs/fig4_lambda_channels.pdf`. Run it after the S11 update (A1-01). |
| A3-06 | NOT READY | The published supplement still prints revision-history wording | 45 occurrences of "revision 1/2", "Material moved", "Moved from" and similar, in S1–S10 headings and lead lines. Lines: 198, 230, 266, 811, 813, 819–864, 886, 894, 955, 981. The whole of S10 (line 1010, "Material moved from the main text in revision 2", and its "From Section N" sub-headings at 1014–1150) is titled this way. | Retitle by content, e.g. "S10 Extended text for Sections 1–9" and "Further detail for Section N". Delete the "moved from … in revision N" lead clauses in `supplementary.md`, then regenerate the published copy. |
| A3-07 | NOT READY | Text runs into the margin in the built PDF | 23 overfull boxes in total, 11 of them wider than 10 pt. Seven are DOI strings in the reference list, up to 78 pt wide. Four are in a table of Section 6.7.4 (counted only). | Allow breaks in DOIs/URLs in `paper/build/cas.pandoc.tex` (e.g. `\usepackage{xurl}`). Fix the 6.7.4 table during the 6.7 update. |

### Criterion 4: no contradictions

| ID | Status | Item | Evidence | Fix, or what is needed |
|---|---|---|---|---|
| A4-01 | READY | The headline numbers agree across the abstract, cover letter, Section 1 and highlights | Wherever they appear, the values agree: −8.99 [−10.89, −6.99], −2.43, +19.32 [+17.43, +21.13], 537 of 600, PASCAL-50S −2.29 [−5.15, +0.61], 3,226 images / four LVLMs, 2.149, +35.46 [+34.19, +36.56], +10.52, +1.97 [−0.44, +4.01], "two of five" XM3600 failures. Their scope also agrees: the full ordering claim is limited to XM3600 and the second backbone, and label gold against five references is not claimed. The highlights (`highlights_A.md:5–9`) contradict none of these. | — |
| A4-02 | NOT READY | The cover letter is less balanced than the abstract | `abstract_A.md:17` reports the whole set of outcomes on the new single-annotator labels and says that the proposed certificate was not validated. `cover_letter_A.md:13` gives one passing outcome from that set and omits the rest and the certificate sentence. Detail is left out here under the hard rule. | Add the abstract's two clauses (from "Of seven predictions…" to "…was not validated") to the Main-result bullet at `cover_letter_A.md:13`, or remove the single outcome so that the letter matches the abstract. |
| A4-03 | BLOCKED | Related-manuscript statements depend on the order of submission | `declarations.md:23` and `cover_letter_A.md:25` call Paper B "in preparation". The goal order submits B before A, so at A's submission B will be under review at LRE. Neither statement names the TAIMMA 2027 conference version of Paper C, which prints A's count-matched precision before A (goal §2 item 2; VENUE_RECHECK, Consequences A6). C's title, as printed in both places, matches the C repo (`paper_v1_analysis/00_abstract.md:1`, `tex/paperC.tex:22`). | At A's submission, change B to "submitted to *Language Resources and Evaluation*", and add one sentence naming the TAIMMA 2027 conference version of C as a related submission that uses the measure defined here. This needs the B and TAIMMA submission dates from the investigator. |
| A4-04 | NOT READY | Undefined internal labels in the printed main text | `sec1_introduction.md:45`: "AD-1′" is used once and defined nowhere in the main text; "PREMISE_NOT_MET" is a raw verdict token, while the rest of the text writes "premise not met". `sec11_limitations_ethics.md:25`: "Part P" and "Part V" are defined only in S11.5 and S11.6. | sec1:45: drop "AD-1′" (ledger row A26 already identifies the test) and write "premise not met". sec11:25: write "the released image sets of the 15 published comparisons (Supplementary S11.6)" and "the instance-only rows of the development check (Supplementary S11.5)". |

### Criterion 5: venue requirements (SPIC)

| ID | Status | Item | Evidence | Fix, or what is needed |
|---|---|---|---|---|
| A5-01 | BLOCKED | Abstract length | 250 words (wc -w, comments stripped), one paragraph, no references. That is exactly the card's limit, so any other counting method breaks it. The rule is guide-only and was not re-read (VENUE_RECHECK A5). | Someone opens the guide in a normal browser. A5-02 frees words in any case. |
| A5-02 | NOT READY | The abstract does not stand alone | `abstract_A.md:17` has one section pointer, eight hypothesis codes that are not defined in the abstract, and "LVLMs", which is not spelled out. | Remove the section pointer and the codes, and write "large vision-language models" out once. The sentences say the same without the codes. |
| A5-03 | BLOCKED | Keywords | 7 (`abstract_A.md:27`), the card's maximum. The rule is guide-only (A6). | Same guide check as A5-01. |
| A5-04 | READY | Highlights content | 5 bullets of 83, 81, 77, 84 and 81 characters (limit 85), confirmed publisher-wide (A8). | — |
| A5-05 | NOT READY | No highlights Word file | The publisher-wide page asks for a Word document (A9). `paper/highlights_A.docx` does not exist. Whether highlights are needed at first submission is in the unread guide. | `pandoc` the five bullets of `highlights_A.md` (without the comments) to `highlights_A.docx`. |
| A5-06 | BLOCKED | Title-page facts | `title_page_A.md:11–13`: three postal addresses are placeholders, and two of them show in the built PDF. `:15`: the corresponding author's e-mail. `:17`: the second author's e-mail. ORCID is given only for the first author (`:9`). The cover-letter signature (`cover_letter_A.md:32`) has the same placeholders. | The investigator supplies the addresses and e-mails, and any further ORCIDs. |
| A5-07 | BLOCKED | Data availability: deposit and link | `docs/ZENODO.md:3`: nothing is deposited. There is a private-link placeholder at `title_page_A.md:19`, `cover_letter_A.md:21` and in the comment at `declarations.md:19`. Option C itself was confirmed publisher-wide (A18); whether SPIC uses Option C is guide-only (A19). | The investigator decides on and makes the Zenodo restricted deposit and gives the link. |
| A5-08 | READY | Declarations content | CRediT for all three authors (`declarations.md:7`), competing interests (`:11`), funding (`:15`), data statement (`:19`), related manuscripts (`:23`), ethics (`:27`). | — |
| A5-09 | BLOCKED | Declarations in the submission system | The competing-interests tool (.docx) and CRediT/funding entries in the form; whether CRediT is mandatory is guide-only (A20, A21). | These are done by the investigator at submission. |
| A5-10 | READY | No AI statement, and no "no AI" sentence | No AI-use or "no AI" wording in any printed file (abstract, title page, highlights, Sections 1–11, declarations, cover letter, supplement S1–S10, captions). The 6.7 and S11 ranges were scanned with 0 hits. This follows goal §3. | — |
| A5-11 | BLOCKED | Reference style | The build gives numbered references in square brackets in order of appearance (elsarticle-num-names), as the card says. The rule and LTWA journal abbreviation are guide-only (A14). All 18 cited journal articles carry full journal names (e.g. *Transactions of the Association for Computational Linguistics*, *International Journal of Computer Vision*, *Journal of the American Statistical Association*). | Guide check. If abbreviation is required, put the LTWA forms in the `journal` fields of `paperA.bib` for those 18 entries. |
| A5-12 | NOT READY | An internal note is printed as a heading | `declarations.md:1` "# Declarations (placed immediately before the references)" is printed in the PDF. | Change it to "# Declarations", or drop the H1; the sub-headings carry the content. |
| A5-13 | BLOCKED | Length | 19,265 words of main text (Sections 1–11 plus declarations, comments stripped, tables included), against the project target of 8,500 (`abstract_A.md:4–5`). The card found no journal limit, and the guide was not re-read (A4). | The investigator cuts the text at the rewrite. The candidate moves are listed at `abstract_A.md:8`. |
| A5-14 | READY | Review model and author identity | Single-anonymized per the card, so the CAS build carries the names; no anonymized build is needed. Guide re-check as A5-01. | — |
| A5-15 | READY | Cover letter | `cover_letter_A.md` names the journal and article type, has a scope-fit sentence, states originality, no concurrent submission and no preprint, and is signed by the corresponding author. Cover-letter rules are guide-only (A11). Placeholders are under A5-06 and A5-07; balance is under A4-02. | — |
| A5-16 | READY | No internal ids or tool names in the printed main text, abstract, highlights, declarations or cover letter | Regex for decision ids, LOG/ruling words, repo paths, tool names and fix-package words. The remaining hits are legitimate: public repo commit shas (`sec11:53`), "LLM judge" as a related-work subject (`sec3:20`), DOI digits, and "writer" meaning a caption writer. Registry ids such as P50-A4 and G2B-O2 are ledger identifiers mapped in Table S4.0. Exceptions are A4-04 and A3-06. | — |

### Criterion 6: the full text has been reviewed

| ID | Status | Item | Evidence | Fix, or what is needed |
|---|---|---|---|---|
| A6-01 | BLOCKED | Section 6.7 and S11 could not be reviewed by this audit | The hard rule applies, and both sections await the update (A1-01). Scripted counts are in "Held sections" below. | After the update and the closing line, an agent allowed to read 6.7 and S11 reviews them, including the S11 leak hits. |
| A6-02 | NOT READY | No full read since fix packages v2–v5 of 2026-11-15 | This audit read the abstract, highlights, title page, declarations, cover letter and Section 1 in full. Sections 2–11 and S1–S10 were covered only by the automated checks above. | Do a sentence-by-sentence read of Sections 2–11 (6.7 excepted) and S1–S10 now. Repeat it for 6.7 and S11 after A1-01. |

## Held sections: counts only (Section 6.7 and S11)

| Count | Section 6.7 (sec7 l.124–247) | S11 (supp l.1172–1732) |
|---|---|---|
| Visible words | 3,964 | 20,855 |
| Bracket placeholders ([PENDING …], [PI …], TODO, TBD, ??, XX and similar) | 0 | 0 |
| Table cells holding only a dash or ellipsis (could be "not applicable" or a placeholder; not inspected) | 8 | 82 |
| Tables | 6, all captioned | not counted |
| Decision-id hits | 0 | 1 |
| File-name / path hits | 0 | 9 |
| Hex strings of 8+ characters | 1 | 21 |
| "Part", "Phase" or "writer" terms | 0 | 31 |
| "judge"/LOG words | 0 | 1 |
| AI-wording hits | 0 | 0 |
| Overfull boxes > 10 pt in the build | 4 (one table in 6.7.4) | not built |

The S11 decision-id and path hits are the ones that stop `scrub_supp.py` (V2_PROGRESS.md:63). This is the open "internal terms in S11" point of goal item 4.

## Custody flag (for the coordinator; not counted above)

Outcomes of the Section 6.7 hypotheses are printed outside the held sections, at:
- `abstract_A.md:17`
- `cover_letter_A.md:13`
- `sec1_introduction.md:11` and `:49` (a Table 1 row)
- `sec10_discussion.md:29`
- `sec11_limitations_ethics.md:11`
- `sec5_exchangeability.md:43` (last sentence)
- `declarations.md:27` (status only)

If the figures of 6.7 are held from the investigator, these lines carry them where the investigator may read them. Decide the custody scope before this report or the paper files reach the investigator. If they are held, replace these clauses by neutral pointers until the closing line. This report repeats none of them.

## Letter L2 (KTVIC)

The corrected draft is `manuscript/letters_2026-11-15/L2_KTVIC_v2.md`; v1 is unchanged. Changes:
- The request for written confirmation, the earlier-contact slot and the terms question are removed. They conflicted with the paper's clause and with goal §3 (agreement stated as a fact, not asked again).
- The letter opens with the earlier contact and the authors' agreement in the paper's own words, with no date, no "in writing" and no "on file". It says the agreed use includes training.
- The adapter-weight slot is resolved from `declarations.md:19` and `sec11:48`.
- Acknowledgement and terms are now an offer, not a request. The letter still never says that the data are free of terms.
- Part B, the slots, the reply-by date and the DRAFT status are kept.
- `L2_L4_MERGED.md` probably needs the same change. It was not edited.
