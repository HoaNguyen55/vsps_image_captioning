# Paper B fix package v1

Written 2026-11-15T11:58Z (2026-11-15, 18:58 Vietnam time). Target journal of the paper: Language Resources and Evaluation (Springer).

**What this file is.** Proposed changes to the rewritten Paper B in `/mnt/d/vsps_papers/vsps-paperB-lre`, folder `paper/rev_2026-11-15/`, for the items that ruling CC-420 marks as owed before submission and that an agent can close without the investigator. Each text change is an exact OLD/NEW pair with its evidence (Section 5), or a step of the script described in Section 6. Nothing has been applied, staged or committed. The script `apply_b_v1.py` of this folder rebuilds the files in memory and compares them with the sha256 values of Section 9.

**Inputs, each read in full.**
- Ruling `.session_backup/2026-10-13/decisions/CC-420.txt` (sha256 `994552078aab6439…`); rulings CC-418 (`1153c67575c2441b…`), CC-415 (`d24a1b595da296d3…`) and CC-417 (`3947bc839e6db01e…`) for the sentences that are fixed word for word.
- Audit `manuscript/READY_AUDIT_B_2026-11-15.md` (`5dcce86549bbbc24…`). It was written against the earlier text; its twelve NOT READY items are re-checked in Section 2.
- Venue card `.claude/skills/venue-lre/SKILL.md` (`18c09b3e9fcfd440…`); rows B13 to B26 of `manuscript/cfp/VENUE_RECHECK_2026-11-15.md` (`066abf12cd0dba95…`).
- Paper repository at HEAD `568eaec`, working tree clean: `paper.md`, `online_resource.md`, `cover_letter.md`, `title_page.md` of `paper/rev_2026-11-15/`; of the earlier text, the lines that the blocks cite, the build folder and `title_page_B.md`.
- The draft's checker `.session_backup/2026-11-14/b_text_held/draft_v3_1/check_draft.py` (`0d9d21fa0b396e3d…`), read and run from a scratch copy only.
- For block B1-M01: `scripts/b_pa1/b_pa1_registry.json` (`3651d1a815cd1234…`), `manuscript/prereg/2026-11-01_b_pa1_tier1/PREREG_DRAFT_v3_1.md` (`e9b30ca74678a06b…`) §6.1, §6.2, §7.1, §7.2, the three files of `data/results/b_pa1_t1_1111/` (keys `config`, `judge_prompt`, `accepted`), the two lock files of `scripts/b_pa1/`.
- Not opened or listed: any label file, key file, assignment or practice file, `~/vsps_labels*`, any Paper A or Paper C text. `BUILD.json` and `HUMAN.json` were read by the checker only (after its sha256 checks) and were not printed. The two held switch annexes were read by the checker only.

**Not in this package, by instruction.** Reference DOIs, the Berger sources and every other reference mark (another agent; `B_REFS_LOOKUP_2026-11-15.md` of this folder). No statement on AI tools as writing aids is added, and no sentence says that no AI tool was used. No number, no registered label and no ruled sentence is changed by the default run (Section 7).

## 1. Counts

- 18 blocks: `paper.md` 12, `online_resource.md` 3, `cover_letter.md` 2, `title_page.md` 1.
- 6 steps that are not blocks (Section 6): R1 (21 pointers in 14 paragraphs of the moved old text), C2 (one ORCID link copied), S1 (the two generated side files; only `PARAGRAPH_SOURCES.tsv` changes), N1 (`SNAPSHOT.sha256`), B1 (new file `paper/build/build_B_rev.sh`), and X1 (four places inside ruled sentences; **not applied by default**, it needs a ruling).
- 7 files after the default run: 6 changed (`paper.md`, `online_resource.md`, `cover_letter.md`, `title_page.md`, `PARAGRAPH_SOURCES.tsv`, `SNAPSHOT.sha256`), 1 new (`paper/build/build_B_rev.sh`). `number_manifest_B_v2.tsv` comes out byte-equal to HEAD and is not written. No file of the earlier text is touched; `build_B_springer.sh` is not edited.
- Words, by the checker's count of running text: abstract 248 before and after. Main text in the plan's sense 9,229 before and 9,399 after (+170): declarations 355 to 498 (the data availability statement names its sources, and the materials statement is new), Section 2 +10, Section 5 +10 and Section 6 +7 (author mark; the name of Online Resource 1 in four pointers). The declarations leave their word band; 7 of 11 sections are now outside their bands (6 before). Nothing is cut: the cut is the investigator's (CC-420 N6).
- Marks left for the investigator in reader-visible text after the package: `AUTHOR TO CONFIRM` 7, `AUTHOR TO PROVIDE` 11, `AUTHORS:` 5 (checker's count over the four files and the two held annexes).

## 2. The twelve NOT READY items of the audit, re-checked against `paper/rev_2026-11-15/` at 568eaec

| # | Audit item (old text) | State in the new files | This package |
|---|---|---|---|
| 1 | Abstract 145 words; CIDEr undefined | Fixed: 248 words; CIDEr-D written out | no text change; stale length comments corrected (B1-L01, B1-L02) |
| 2 | Build script reads a folder that the paper repository lacks | Open: no script builds the new folder | step B1: new `build_B_rev.sh`; the old script is not edited |
| 3 | Declarations inside Section 7, before the Conclusion | Fixed: unnumbered section "Statements and Declarations" after Section 9 and directly before the references | none (heading name: Section 8, item 1) |
| 4 | Headings Ethics approval, Consent, Materials availability missing | Ethics approval, Consent to participate, Consent for publication exist with author marks; Materials availability missing | B1-D04 |
| 5 | Data availability is a cross-reference | Mostly fixed. Left: the sources of other groups by pointer to Table 2, with a count that differs from that table; no place of release | B1-D01, B1-D02; B1-D03 (agreement clause, see Section 8.2) |
| 6 | Author contributions not on the title page | Open: the title page has no contributions line | B1-T01; B1-D05 |
| 7 | Language model and vision-language model unnamed | Open: the passage is now in Online Resource 2, S24, a byte copy | B1-M01 |
| 8 | Three sentences say no human data were collected | Fixed: none in the four files (the one moved sentence of S23 was edited at the transfer and is marked); none in the carried-over `supplementary_B.md` | none |
| 9 | Five entries without a DOI | not checked here | other agent |
| 10 | "Supplementary S…" instead of "Online Resource" | Main text fixed. Left: four pointers to Tables E… without the name of the resource; 21 pointers in the moved old text of Online Resource 2 | B1-P01 to B1-P04; step R1 with B1-R00 |
| 11 | Cover letter: mark for the first author's ORCID | Open: one mark for all authors | B1-C02 with step C2 |
| 12 | "in preparation" for the companion manuscripts | Open in the cover letter and in Section 2 | B1-C01, B1-C03; the state stays marked for the submission day |

## 3. Ruling CC-420, item by item

- **Ruling 5, "owed".** Materials availability: B1-D04. Contributions on the title page: B1-T01. Language model and vision-language model: B1-M01, with one fact not on record left as an author mark. Five DOIs: other agent. "Supplementary S…" and old section numbers in Online Resource 2: step R1 and B1-R00 (the old section numbers were already mapped by the reading note of S.0 and are left). Items 11 and 12: B1-C01 to B1-C03. Audit items 25 to 27 (ethics review, consent, the earlier ratings) stay with the investigator; no word of the ethics and consent statements is changed. Audit R13 (earlier work on human preference judgements of captions in Section 2) is not written here: it needs sources that are read first (Section 8.2).
- **N1.** Build-script path: step B1. A scratch build of the files after this package gives 29 pages for the main text (tables set, four figure marks in place of figures, author mark), 8 pages for Online Resource 1 and 35 for Online Resource 2 with Sections S1 to S15 inserted. Table 6 by script and the figures are not part of this package.
- **N3.** The owed items of ruling 5 as above. The reference marks and the changes C1 to C3 are left to the reference work.
- **N4.** Log line ids of E.6 item 13: B1-I01. "registration l.304" and "CC-396 JQ6" stand inside sentences that CC-418 fixed (S3, S11), and CC-420 ruling 10 says the full sentences stay word for word outside the abstract; they are prepared as step X1 and not applied without a ruling. "(the PI)" inside D1 is the investigator's to change.
- **N5.** B1-L01, B1-L02.
- **N6.** Length: +170 words (Section 1); no cut.
- **N7.** The checker is not ported. It was run from a scratch tree that mirrors the paths it reads (Section 7).
- **Ruling 8.** Nothing here licenses a submission. The marks of PI-2, PI-3 and PI-6 and every reference mark are untouched.
- **Ruling 9.** Points (3) and (4): "kappa" and the pronoun of S8 are left as they are.

## 4. Table of blocks

| Id | Group | Audit or ruling item | File | Line at HEAD |
|---|---|---|---|---|
| B1-L01 | L | CC-420 N5 | `paper.md` | 3 |
| B1-L02 | L | CC-420 N5, N6 | `paper.md` | 7 |
| B1-D01 | D | audit item 5 (19); CC-420 ruling 5 | `paper.md` | 421 |
| B1-D02 | D | audit item 5 (19) | `paper.md` | 421 |
| B1-D03 | D | standing rule on the dataset authors' agreement (PI-1026az, PI-1110o) | `paper.md` | 421 |
| B1-D04 | D | audit item 4 (18); CC-420 ruling 5 ("Materials availability" is missing) | `paper.md` | 423 |
| B1-D05 | D | audit item 6 (20); venue recheck row B13 | `paper.md` | 427 |
| B1-T01 | T | audit item 6 (20); CC-420 ruling 5 | `title_page.md` | 16 |
| B1-C01 | C | audit item 12 (41) | `cover_letter.md` | 18 |
| B1-C02 | C | audit item 11 (39a) | `cover_letter.md` | 24 |
| B1-C03 | C | audit item 12 (41), same fact in the main text | `paper.md` | 64 |
| B1-P01 | P | audit item 10 (38); venue recheck row B23 | `paper.md` | 184 |
| B1-P02 | P | audit item 10 (38) | `paper.md` | 190 |
| B1-P03 | P | audit item 10 (38) | `paper.md` | 215 |
| B1-P04 | P | audit item 10 (38) | `paper.md` | 280 |
| B1-I01 | I | CC-420 N4 (the log line ids of E.6 item 13) | `online_resource.md` | 143 |
| B1-R00 | R | audit item 10 (38); CC-420 ruling 5 (old-text blocks of Online Resource 2) | `online_resource.md` | 168 |
| B1-M01 | M | audit item 7 (23); CC-420 ruling 5; venue recheck row B16 | `online_resource.md` | 336 |

## 5. Blocks

Each block is `<<<id file OLD>>>`, the exact old text, `<<<id file NEW>>>`, the exact new text, `<<<id EVIDENCE>>>` and the reason. Files are in `paper/rev_2026-11-15/`. In B1-C02 the text in braces is replaced by step C2.

<<<B1-L01 paper.md OLD>>>
The abstract is inside the venue limit only while the human-arm sentences are placeholders (see DRAFT_NOTES.md, open points). -->
<<<B1-L01 paper.md NEW>>>
The abstract is inside the venue limit of 150 to 250 words (248 words by the count of the draft's checker) since ruling CC-420 allowed short forms of the label sentences for the abstract only (its ruling 10 and edit E1). -->
<<<B1-L01 EVIDENCE>>>
Unprinted comment. The sentence was true of draft v2, whose human-arm sentences were marks. After edit E1 of CC-420 the checker counts 248 words (band 220 to 250: within). DRAFT_NOTES.md was not transferred (CC-420 ruling 6), so the pointer led nowhere in the paper repository.

<<<B1-L02 paper.md OLD>>>
LENGTH: with the human-arm sentences the abstract is above the venue's 250 words, and Sections 5, 6 and 8 are above their bands (READ_PACKAGE_V3.md, open points).
<<<B1-L02 paper.md NEW>>>
LENGTH, recounted with the draft's checker after fix package v1 of 2026-11-15 (running text; table rows, captions and figure notes not counted): abstract 248 words; main text in the plan's sense 9,399 words against a plan of about 7,500. Above their bands: Section 1 (929 words against 675 to 825), Section 5 (1,566 against 810 to 990), Section 6 (2,421 against 1,710 to 2,090), Section 8 (742 against 450 to 550), Section 9 (334 against 180 to 220) and the declarations (498 against 315 to 385). Section 7 is below its band (492 against 495 to 605). The cut is left to the PI's rewrite (CC-420 N6).
<<<B1-L02 EVIDENCE>>>
Unprinted comment. The old sentence says the abstract is above 250 words; it is 248 since CC-420 E1. READ_PACKAGE_V3.md was not transferred. The new counts are those of `CHECKS.md` from the run of the checker on the files after this package (Section 5).

<<<B1-D01 paper.md OLD>>>
The outputs of other groups are public at the repositories and commits of Table 2: two repositories under the MIT licence, and two without a licence, which were used for aggregate statistics only.
<<<B1-D01 paper.md NEW>>>
The outputs of other groups are public at five repositories, each read at a pinned commit (Table 2): `loc110504/VietnameseSportImageCaptioning` at `6d8132e` (MIT licence); `vanngthi/ViECAP-Image-Captioning-Vietnamese` at `fd71ca5` (no licence stated; used for aggregate statistics only); `trannam710/NIC-with-Soft-Attention` at `0660118` and `trannam710/Meshed-Memory-Transformer` at `6109801` (listed in Table 2 as MIT and BSD-style); and `SuperCoolGuy855/CLIP_mT5_Image_captioning` at `d786f6d` (no licence stated; aggregate statistics only). The files of the last three repositories failed the parsing rule of the structure gate and form no comparison (Section 5.2).
<<<B1-D01 EVIDENCE>>>
A data availability statement must stand alone (venue recheck row B20; audit item 19). The old sentence sends the reader to Table 2 for the sources, and its count does not match that table: Table 2 names five repositories (one MIT; one without a licence; two under `MIT; BSD-style`; one without a licence), not two and two. The new sentence copies repository, commit and licence cell from Table 2 of the same file (rows G1 to G6; registration table at l.196 to l.201) and Section 5.2 (rule 1; two groups form no comparison). No number is added: the commits are identifiers in code spans.

<<<B1-D02 paper.md OLD>>>
Released: the registration files, the result files of the stages (aggregate counts and statistics; no caption text) and the manifest that keys every number of this paper.
<<<B1-D02 paper.md NEW>>>
Released, in the archive named under Code availability: the registration files, the result files of the stages (aggregate counts and statistics; no caption text) and the manifest that keys every number of this paper.
<<<B1-D02 EVIDENCE>>>
The statement said what is released and not where. The archive and its DOI mark are in the next statement (Code availability); the cover letter (CL-5) names the same archive. No new fact.

<<<B1-D03 paper.md OLD>>>
which asks for citation (Pham et al., 2024) and states no licence.
<<<B1-D03 paper.md NEW>>>
which asks for citation (Pham et al., 2024) and states no licence; its authors agreed to our use of the data.
<<<B1-D03 EVIDENCE>>>
The earlier text printed the agreement as a fact (`paper/sec3_data_and_audit.md` l.72: the KTVIC and UIT-OpenViIC authors "agreed to our use of their data"). That paragraph was not moved into the new files, so the rewritten paper no longer states it anywhere (grep of the four files for "agreed": 0). The clause is restored where the terms of KTVIC are stated, in the words of the earlier text, for KTVIC only (UIT-OpenViIC is not a source of the present main text). No date, no "in writing", no "on file". This block can be skipped on its own; the script counts the agreement clauses (+1 with it, 0 without).

<<<B1-D04 paper.md OLD>>>
<!-- @P id=decl-4 | src=plan H.1 (code availability; licence and archive DOI left to the PI); old sec3 l.70 | claims= -->
<<<B1-D04 paper.md NEW>>>
<!-- @P id=decl-3b | src=venue recheck 2026-11-15 row B13 (declarations: Data, Material and/or Code availability); labelling plan §2.1, §10 (items: KTVIC test images with captions of the authors' own systems; images shown locally and not copied elsewhere); plan l.146 and CC-418 ruling 5 (the pair files hold caption text and are never committed); fix package v1 | claims= -->
**Materials availability.** The study produced no physical material. The rating materials of the human arm are the rating page and the pairs shown on it: KTVIC test images, each with two captions written by the authors' own systems. The rating page is part of the rating tool named under Code availability. The pair files are not released, because they hold benchmark images and caption text (Data availability). [AUTHOR TO CONFIRM: whether the instructions to the raters, which are in Vietnamese, are released with the rating tool]

<!-- @P id=decl-4 | src=plan H.1 (code availability; licence and archive DOI left to the PI); old sec3 l.70 | claims= -->
<<<B1-D04 EVIDENCE>>>
The journal lists "Data, Material and/or Code availability" among the declarations, and the Springer template has the heading "Materials availability" (`sn-article.tex` l.558 to l.566). The new paragraph sits between Data availability and Code availability. Its facts are in the same file (Section 5.5: the items; Data availability: what is not released; Code availability: the rating tool) and in the labelling plan §10. Whether the Vietnamese instructions are released is not on record, so it is an author mark.

<<<B1-D05 paper.md OLD>>>
**Authors' contributions.** [AUTHOR TO PROVIDE] **Acknowledgments (title page).** [AUTHOR TO PROVIDE: the second rater, by role; by name only with that person's written consent]
<<<B1-D05 paper.md NEW>>>
**Authors' contributions.** [AUTHOR TO PROVIDE: the same statement as on the title page and in the submission system]
<<<B1-D05 EVIDENCE>>>
Acknowledgments belong on the title page (row B13), and the title page already carries this mark (block TP-3, same words). In the declarations it printed the reader-visible words "(title page)". The contributions mark now says where the same text must also go (row B14).

<<<B1-T01 title_page.md OLD>>>
<!-- @P id=TP-4 | src=venue card (row Supplementary) | claims= -->
<<<B1-T01 title_page.md NEW>>>
<!-- @P id=TP-3b | src=venue recheck 2026-11-15 row B14 (author contributions are listed on the separate title page and typed into the submission system); old sec7 l.65 (the statement of the earlier version; not copied); fix package v1 | claims= -->
**Authors' contributions.** [AUTHOR TO PROVIDE: the contribution of each author to this version, which adds the human arm. The statement of the earlier version is in `sec7_limitations_ethics.md` l.65 and is not copied here; the same text is typed into the submission system]

<!-- @P id=TP-4 | src=venue card (row Supplementary) | claims= -->
<<<B1-T01 EVIDENCE>>>
The journal asks for the contributions on the title page (row B14: "should be listed at the separate title page"). The roles of the earlier version were written before the human arm existed, so they are not copied: the investigator states them for this version.

<<<B1-C01 cover_letter.md OLD>>>
Two companion manuscripts by the same authors are in preparation [AUTHOR TO CONFIRM: their titles and their state at submission, and which material is shared with them, as in the letter of the earlier version]; copies are available to the editor on request.
<<<B1-C01 cover_letter.md NEW>>>
Two companion manuscripts by the same authors exist [AUTHOR TO CONFIRM on the submission day: the title and the state of each (in preparation, or under review and at which journal or conference), and which material is shared with them, as in the letter of the earlier version]; copies are available to the editor on request.
<<<B1-C01 EVIDENCE>>>
"in preparation" was printed as a fact outside the mark, and it may be false on the submission day. The state now sits inside the mark, which stays until that day.

<<<B1-C02 cover_letter.md OLD>>>
**Authors.** [AUTHOR TO PROVIDE: for every author, a verified ORCID iD, a university homepage or an online CV]
<<<B1-C02 cover_letter.md NEW>>>
**Authors.** First author: {ORCID link of the first author, copied by the script} (ORCID iD, as on the title page of the earlier version). [AUTHOR TO PROVIDE: for each of the two co-authors, a verified ORCID iD, a university homepage or an online CV; and the check that the first author's ORCID profile is a verified one]
<<<B1-C02 EVIDENCE>>>
The first author's ORCID link is already in the repository (`paper/title_page_B.md` l.9). Step C2 of the script copies it from there; it is not typed in this file or in the script. The co-authors' items are theirs to give and stay marked (audit item 39b).

<<<B1-C03 paper.md OLD>>>
and the relation to a companion manuscript in preparation, are documented in Online Resource 2.
<<<B1-C03 paper.md NEW>>>
and the relation to a companion manuscript [AUTHOR TO CONFIRM on the submission day: in preparation, or under review], are documented in Online Resource 2.
<<<B1-C03 EVIDENCE>>>
Section 2 (block 2-6) prints the same state as the cover letter. The mark keeps the sentence from going out with a stale state.

<<<B1-P01 paper.md OLD>>>
after its input file had been logged (Table E5). Tool versions are in Table E4.
<<<B1-P01 paper.md NEW>>>
after its input file had been logged (Online Resource 1, Table E5). Tool versions are in Table E4 of Online Resource 1.
<<<B1-P01 EVIDENCE>>>
Tables E1 to E5b are in Online Resource 1; the journal asks that supplementary files be referred to as "Online Resource" (row B23). The pointer gains the name of the resource.

<<<B1-P02 paper.md OLD>>>
in the band that is reported without labels (Section 6.7; Table E5b).
<<<B1-P02 paper.md NEW>>>
in the band that is reported without labels (Section 6.7; Online Resource 1, Table E5b).
<<<B1-P02 EVIDENCE>>>
As B1-P01. Only the pointer changes; the sentence that CC-420 read ("No gate of the human arm fired; …") keeps its words.

<<<B1-P03 paper.md OLD>>>
72 in all (DESCRIPTIVE; Table E4).
<<<B1-P03 paper.md NEW>>>
72 in all (DESCRIPTIVE; Online Resource 1, Table E4).
<<<B1-P03 EVIDENCE>>>
As B1-P01.

<<<B1-P04 paper.md OLD>>>
Fig. 2 and Table E2 give the breaking sets
<<<B1-P04 paper.md NEW>>>
Fig. 2 and Table E2 of Online Resource 1 give the breaking sets
<<<B1-P04 EVIDENCE>>>
As B1-P01.

<<<B1-I01 online_resource.md OLD>>>
(363 saved lines, `91fa0a30…`; log line OPS-1114bh), and the non-author rater on 2026-11-15 (439 saved lines, `65f1527d…`; OPS-1115w, with the correction line OPS-1115x, which records that every answer of this rater was saved in person at the laptop and none through the remote link). A closing record (OPS-1115y) and the closing line (OPS-1115z, 2026-11-15T08:08:59Z) fix the final hashes of the two label files and of the key file (`8f7a4626…`); a correction to the closing record (OPS-1115ak) fixes the status of the second rater's file and the wording of the practice disclosure.
<<<B1-I01 online_resource.md NEW>>>
(363 saved lines, `91fa0a30…`), and the non-author rater on 2026-11-15 (439 saved lines, `65f1527d…`; a correction line beside it records that every answer of this rater was saved in person at the laptop and none through the remote link). A closing record and the closing line (2026-11-15T08:08:59Z) fix the final hashes of the two label files and of the key file (`8f7a4626…`); a correction to the closing record fixes the status of the second rater's file and the wording of the practice disclosure.
<<<B1-I01 EVIDENCE>>>
Six ids of lines of the project's internal log were printed in reader-visible text; a reader cannot look them up. The facts, the dates, the counts and the hashes stay. The ids stay in the unprinted annotation of the block (src field), which is where the checker and a later reader of the repository find them.

<<<B1-R00 online_resource.md OLD>>>
In those sections "this paper", "the main text" and "our protocol" mean the earlier version and its committed scoring protocol, which is the reference member of the present main text.
<<<B1-R00 online_resource.md NEW>>>
In those sections "this paper", "the main text" and "our protocol" mean the earlier version and its committed scoring protocol, which is the reference member of the present main text. "The supplement" means Sections S1 to S15 of this resource, and a pointer of the form "Section S6" or "Table S1.1" is to this resource. In S16 to S28 such pointers stand where the earlier text wrote "Supplement" or "Supplementary" before the number of the section or table; nothing else is changed in those paragraphs.
<<<B1-R00 EVIDENCE>>>
Goes with step R1. The reading note already explains what "Section" plus a number means inside S1 to S28; it now also says what the renamed pointers and the words "the supplement" mean.

<<<B1-M01 online_resource.md OLD>>>
we make no validity claim for the score.
<!-- @OLDEND -->
<<<B1-M01 online_resource.md NEW>>>
we make no validity claim for the score.
<!-- @OLDEND -->

<!-- @P id=S24-M1 | src=scripts/b_pa1/b_pa1_registry.json (sha256 3651d1a8…; model ids, revisions, prompts with their sha256, decode settings; pinned by two log lines of 2026-11-08); manuscript/prereg/2026-11-01_b_pa1_tier1/PREREG_DRAFT_v3_1.md §7.1 (score, answer tokens, abstain rule, judge and its selection, CLIPScore), §7.2 (the three configurations), §6.1 and §6.2 (map entries tagged instrument; dictionary-only rows); data/results/b_pa1_t1_1111/T1_RESULT.json (config d1v1; judge_prompt ja) and JOIN.json (the four accepted captioners); scripts/b_pa1/requirements_b_pa1_main.lock and requirements_b_pa1_legacy.lock (library versions); venue recheck 2026-11-15 row B16 (use of a language model is documented as method); fix package v1 (CC-420 ruling 5, audit item 7). Model ids, revisions, settings and prompts stand in code spans, so the checker does not read them as numbers; the three Vietnamese strings are prompts, not caption text | claims=E62 -->
**Models used as instruments in the study above (added for the present version; this paragraph is not part of the earlier text).** The language model and the vision-language model of the object-verification score are public checkpoints. Each was used as released, at a pinned revision, in `bfloat16` precision. *Language model (it splits a caption into propositions).* `Qwen/Qwen2.5-7B-Instruct`, revision `a09a3545…`; text input only; greedy decoding (`do_sample=False`, `num_beams=1`, `repetition_penalty=1.0`, `max_new_tokens=512`). Its prompt, with line breaks written as `\n`: `You split a Vietnamese image caption into atomic propositions. Each proposition states one fact that the caption claims about the image. Types: object (an object is present), count (how many of an object there are), colour (the colour of an object), attribute (another property of an object), action (what an object is doing), relation (how two objects relate, for example their position). Write each proposition as a short Vietnamese sentence that uses the caption's own words; do not translate, and do not add any fact that the caption does not state. For each proposition, give the head noun of the object it is about, copied from the caption. Answer with a JSON array only, one item per proposition: {"type": "<type>", "text": "<proposition>", "object": "<head noun>"}.\n\nCaption: {caption}\nAnswer:` *Vision-language model (it answers the yes-or-no questions, and it is the same-backbone judge).* `Qwen/Qwen2.5-VL-3B-Instruct`, revision `66285546…`. For the score it receives the image and one question per object proposition: `Hãy nhìn bức ảnh. Mệnh đề sau có đúng với bức ảnh không: "{prop}" Trả lời có hoặc không.` As the judge it receives the image and the whole caption once: `Hãy nhìn bức ảnh và đọc chú thích sau: "{caption}" Tất cả các vật được nhắc đến trong chú thích có thật sự xuất hiện trong ảnh không? Trả lời có hoặc không.` In both roles no text is generated: the answer is read from the probabilities of the first answer token. The probability of yes is the summed probability of the first-token ids of four spellings of the Vietnamese word for yes (with and without a capital letter and a leading space), divided by that sum plus the same sum for the word for no; an id that belongs to both sets is removed from both. The answer is yes when this value is at least one half, and it is an abstention when the most probable token is in neither set; abstentions are left out of the score. *Captioners.* The four systems whose captions were scored are `OpenGVLab/InternVL2_5-2B` (`573169ee…`), `Gregor/mblip-mt0-xl` (`5e3ca094…`), `google/gemma-3n-E4B-it` (`c1221e9c…`) and `openbmb/MiniCPM-V-4` (`6f69a823…`), each named by repository and revision. Each wrote one caption per image with greedy decoding (`max_new_tokens=60`), its own chat template and this prompt: `Mô tả bức ảnh này bằng MỘT câu tiếng Việt ngắn gọn, giống chú thích ảnh. Không liệt kê, không giải thích.` *Multilingual CLIPScore.* `laion/CLIP-ViT-H-14-frozen-xlm-roberta-large-laion5B-s13B-b90k` (`f9ab9552…`) with `xlm-roberta-large` (`c23d21b0…`), as pinned in the registry, and the weight `w=2.5`. *Choice of prompts.* The registration fixed three combinations of a language-model prompt and a question, and three judge prompts. The prompts printed here are those of the reported configuration and the judge prompt that the registered selection rule kept. *Software.* `transformers==4.53.3` and `torch==2.6.0`; `transformers==4.45.2` for the InternVL captioner. The model list, the revisions and the prompts are those of the study's registry file (sha256 `3651d1a8…`), pinned by hash in the project's log on 2026-11-08. *Word-to-class map.* [AUTHOR TO PROVIDE: the map from Vietnamese words to Objects365 classes holds entries tagged `instrument` beside its dictionary entries. The registry records them as agent-drafted under a logged amendment, with no model name and no revision. State how they were drafted, with the tool and its version, or state that this was not recorded; the registered dictionary-only rows are the analysis without them]
<<<B1-M01 EVIDENCE>>>
The passage of S24 (a byte copy of the earlier Section 6.2) names neither model. Every fact of the new paragraph was read from the registered sources: the registry `scripts/b_pa1/b_pa1_registry.json` (sha256 `3651d1a8…`, equal to its line in `scripts/b_pa1/SHA256SUMS_GPU` and to the two pin lines of 2026-11-08 in the log): keys `verifier`, `decomposer`, `models.<key>.repo`, `.revision`, `.dtype`, `.venv`, `decode`, `decomposer_decode`, `clip`, `clip_w`, `token_words`, `prompts.{d1, v1, ja, captioner}.text`; the registration `PREREG_DRAFT_v3_1.md` §7.1 and §7.2 (committed); `T1_RESULT.json` keys `config` (`d1v1`) and `judge_prompt` (`ja`), `JOIN.json` key `accepted`; the two lock files (lines `transformers==`, `torch==`). The four prompts were pasted by script from the registry, with a line break written as `\n`; their sha256 values in the registry are `f39a472f…` (d1), `0fba6d6b…` (v1), `8513ac07…` (ja), `8870589c…` (captioner). Not on record, and therefore an author mark: the tool that drafted the map entries tagged `instrument` (registry key `instrument_llm`: mode "agent-drafted, amendment-logged", id null). The old block above it is not edited. No result and no number of the study is added.

## 6. Steps that are not blocks

**R1. Pointers of the moved old text (Online Resource 2).** Inside the `@OLD` regions of `online_resource.md`, in reader-visible text only (unprinted comments are not touched): `Supplementary Table S<n.m>` becomes `Table S<n.m>`; `Supplementary S<n>` and `Supplement S<n>` become `Section S<n>`. Sections S1 to S15 are part of the same resource, so the pointer needs no other name; B1-R00 says so in the reading note. Each changed paragraph gets one unprinted comment at its end: `<!-- EDITED: fix package v1 of 2026-11-15: N pointer(s) of the form "Supplement S…" or "Supplementary S…" renamed to "Section S…" or "Table S…" of this resource; no other word, no number and no verdict changed. -->`. The checker then lists the paragraph as "edited (marked EDITED)" in `PARAGRAPH_SOURCES.tsv`. The script asserts 21 replacements in 14 paragraphs and none left. The generic words "the supplement" are not changed.

| Line at HEAD | Source of the block | Pointers | Old | New |
|---|---|---|---|---|
| 173 | `sec3_data_and_audit.md` l.9-13 | 3 | Supplement S1; Supplementary Table S1.1; Supplement S1 | Section S1; Table S1.1; Section S1 |
| 186 | `sec3_data_and_audit.md` l.17-24 | 1 | Supplementary S15 | Section S15 |
| 200 | `sec3_data_and_audit.md` l.38-40 | 1 | Supplementary S11 | Section S11 |
| 213 | `sec3_data_and_audit.md` l.50-58 | 1 | Supplementary S10 | Section S10 |
| 215 | `sec3_data_and_audit.md` l.50-58 | 1 | Supplementary S10 | Section S10 |
| 239 | `sec4_system.md` l.5-56 | 4 | Supplementary S1; Supplement S1; Supplement S6; Supplementary Table S1.1 | Section S1; Section S1; Section S6; Table S1.1 |
| 267 | `sec4_system.md` l.5-56 | 1 | Supplementary S14 | Section S14 |
| 296 | `sec5_results.md` l.7-25 | 1 | Supplement S1 | Section S1 |
| 298 | `sec5_results.md` l.7-25 | 3 | Supplement S6; Supplementary Table S1.1; Supplement S6 | Section S6; Table S1.1; Section S6 |
| 311 | `sec5_results.md` l.31-37 | 1 | Supplementary S9 | Section S9 |
| 320 | `sec5_results.md` l.45-47 | 1 | Supplement S6 | Section S6 |
| 353 | `sec7_limitations_ethics.md` l.7-9 | 1 | Supplementary S3 | Section S3 |
| 372 | `sec7_limitations_ethics.md` l.24-24 | 1 | Supplementary S8 | Section S8 |
| 414 | `sec3_data_and_audit.md` l.68-68 | 1 | Supplementary S8 | Section S8 |

**C2. The first author's ORCID link.** The script reads `paper/title_page_B.md` at HEAD, takes the one ORCID link of its reader-visible text and puts it where block B1-C02 has the text in braces. The link is not typed in this file or in the script.

**X1. Internal ids inside ruled sentences. NOT applied by default** (`SKIP = ("X1",)`). CC-420 N4 names "registration l.304" and "CC-396 JQ6" as ids to replace before submission; CC-418 fixed the sentences that hold them (S3 and S11), and CC-420 ruling 10 keeps the full sentences word for word in Sections 1, 6 and 9. A ruling has to say which binds. If it allows the change, set `SKIP = ()`; the targets are in Section 9.
- `paper.md`, three places (blocks 1-5, 7-5 and 9-1): OLD `(registration l.304)`, NEW `(registration, Section 6.5)`. Line 304 of the registration lies in its Section 6.5 "Human arm" (the bullet "Use in the certificate").
- `online_resource.md`, E.6 item 13: OLD `the recommendation sentence departs from the verbatim clause as ruled before stage H existed (CC-396 JQ6). Stage H is the analysis of the human arm; the verbatim clause` NEW `the recommendation sentence departs from the verbatim clause, as an internal read fixed before the analysis of the human arm existed; the verbatim clause`.

**S1. The two side files.** `number_manifest_B_v2.tsv` and `PARAGRAPH_SOURCES.tsv` are written by the checker from the annotations of the draft files. They were regenerated by the checker's `--write` run on a scratch copy of the files after this package, and their first line was set back to the release line of the paper repository. The copies are `number_manifest_B_v2.after_v1.tsv` and `PARAGRAPH_SOURCES.after_v1.tsv` of this folder, pinned by sha256 in the script. The manifest is byte-equal to HEAD (no number was added, removed or moved to another block). The paragraph sources change in 20 rows: 3 new rows (`decl-3b`, `TP-3b`, `S24-M1`), 14 rows that gain "edited (marked EDITED)", and 3 rows whose first six words changed (`6.4-4`, `decl-5`, `CL-6`).

**N1. `SNAPSHOT.sha256`.** The sums file of the folder, with the new sha256 of each changed file and the old line of each unchanged file, in the same order.

**B1. `paper/build/build_B_rev.sh` (new; pinned copy `build_B_rev.sh` of this folder).** It builds from `paper/rev_2026-11-15/` and `paper/paperB.bib` with the helpers of the build folder (`prep.py`, `filter.lua`, the template): the main text in the Springer Nature class, and one PDF per Online Resource (`ESM_1.pdf`, `ESM_2.pdf`; for the second it inserts the unchanged `supplementary_B.md` as Sections S1 to S15). Output goes to `$OUT` or a new temporary folder, never into the repository. It is a working build for the page count and the list of marks: keys that are cited but not yet in `paperB.bib` stay as typed text and are listed in its report, and the author block is a mark until the title page carries the authors. `build_B_springer.sh` is not edited and still names its old path.

## 7. Checks that were run

- **Script, check mode** (`python3 -I -B apply_b_v1.py`): every OLD once at HEAD and no NEW at HEAD; R1 21 pointers in 14 paragraphs; 13 ruled texts each as often as at HEAD (the label sentences S1 and S3, S5 to S8, D1 to D4, the two quotations); the multiset of reader-visible numbers unchanged in each of the four text files, counted as the checker counts them; no added wording on AI tools, no e-mail address, no IPv4 address, no "in writing" or "on file"; agreement clauses +1 (B1-D03). Result: ALL RESULTS EQUAL TARGETS, nothing written.
- **Write test on a scratch clone** (`--repo <clone> --write --ruling TEST`): 7 files written to the working tree of the clone; `git status` there shows 6 modified and 1 untracked path and nothing staged; each written file hashes to its target. The paper repository itself was not written.
- **The draft's checker** on a scratch tree that holds the written files (first line set to the checker's expected line; the checker's bytes unchanged): `--write` run and compare run both exit 0, "hard checks failing: 0", for the default result and for the result with X1. Before the package the same harness reproduces the two committed side files byte for byte (`da7614f0…`, `4514c505…`).
- **Second implementation.** The blocks and steps were also applied by a separate scratch script; its four text files are byte-equal to those of `apply_b_v1.py`.
- **Build** with the new script on a scratch copy of the repository (`git archive HEAD`) plus the written files: main text 29 pages, no missing character; `ESM_1.pdf` 8 pages, `ESM_2.pdf` 35 pages.
- Not run: any study code, any scoring, any step on a rented host.

## 8. Dropped, and left open

### 8.1 Dropped, with reasons

1. **Heading "Declarations".** The live page speaks of a "Declarations" section; the venue card and the draft use "Statements and Declarations". The section is already unnumbered and directly before the references. The checker keys its word count on the present heading, so a rename would report the section as empty. Left for the rewrite.
2. **Ethics approval, consent to participate, consent for publication.** Every fact is the investigator's (CC-420 ruling 5; audit items 25 to 27). No word is changed; the three author marks stay.
3. **References** (DOIs, Berger 1982, Berger and Hsu 1996, the drafting list under "References", every CITE-TO-VERIFY mark): other agent. The drafting list also prints internal ids ("registration l.172", "CC-394 ruling 8 (g)", "plan A.3"); it goes when the list is built from the bib file.
4. **E.6 item 12** quotes a ruling sentence verbatim, with a log line id and internal names in it. It is fixed word for word; not touched (Section 8.2, point 5).
5. **"(the PI)" inside D1**: CC-420 N4 allows "(the first author)" only if that is true and the investigator says so.
6. **Marks of PI-2, PI-3, PI-6** and the anchors: they depend on answers that do not exist.
7. **The author block of the title page**: the draft leaves names and addresses to the investigator; the script could copy the block of the earlier title page, and does not.
8. **`build_B_springer.sh`**: not edited, by instruction.
9. **`FIGURE_TABLE_SPEC.md` rule 7** ("outputs go to this held folder") is superseded by CC-420 ruling 7 step 3. It is a side file with no reader-visible text; left.
10. **The 3 pointers "Supplementary S…" and 42 pointers "Section N" inside `supplementary_B.md`** (Sections S1 to S15, carried over unchanged, outside the folder of the rewrite). The frame says this file is carried over without a change of wording, so a pass on it is a separate step with its own read.

### 8.2 For the coordinator or a judge to decide

1. **Step X1** (Section 6): ids inside ruled sentences. Recommended: allow it (confidence 80%); CC-420 N4 asks for it and the content of the sentences does not change.
2. **Block B1-D03** restores the clause that the KTVIC authors agreed to the use. The earlier text stated it; the rewrite dropped the paragraph that held it. Recommended: keep the block (confidence 85%). The same earlier paragraph said that the UIT-ViIC authors have not given permission and that none is claimed; that sentence is not in the new files either, and it is not restored here because its wording depends on how the present paper uses UIT-ViIC (image ids of two first-look groups).
3. **Block B1-M01** prints four prompts verbatim, three of them Vietnamese. They are prompts, not caption text, but the gate sentence "the only Vietnamese strings are the toy spellings of Section 3" (CC-420 G6) no longer holds as worded. It also names the four public captioner checkpoints of the earlier development study; these are public models run by the authors, not the released outputs of other groups that PI-6 is about.
4. **Length**: +170 words, mostly in the declarations.
5. **E.6 item 12**: whether a verbatim ruling sentence with internal ids stays in a public Online Resource.
6. **Audit R13**: earlier work on human preference judgements of captions is still absent from Section 2.
7. **N7**: the checker is still bound to the held folder; this package was checked through a scratch tree.

### 8.3 Left for the investigator

1. Ethics review or exemption; whether each rater's consent was recorded before that rater's first answer, with dates; consent to the release level of the judgements (declarations).
2. Authors' contributions for this version (title page, declarations, submission system).
3. Names, affiliations, the corresponding author's address (title page, the head of both Online Resources, the signature of the cover letter); acknowledgments.
4. For each co-author: a verified ORCID iD, a university homepage or an online CV (cover letter).
5. Licence and archive DOI; whether the Vietnamese instructions to the raters are released (Materials availability).
6. The state and titles of the two companion manuscripts on the submission day (cover letter; Section 2); the cover-letter sentence on the contact with the dataset authors.
7. How the map entries tagged `instrument` were drafted, with the tool and its version (mark in S24; the registry records none).
8. "(the PI)" in the author sentence; one line from the second rater (CC-417 W2); the answers to PI-2, PI-3 and PI-6.

## 9. Targets

sha256 of every file after the default run (`SKIP = ("X1",)`):

| File | sha256 |
|---|---|
| `paper/build/build_B_rev.sh` | `bd24f0c84e51d1703185247945adc0a29f9e37d8d06099048f0d1a25eba06956` |
| `paper/rev_2026-11-15/PARAGRAPH_SOURCES.tsv` | `1a4e6e5557768b3b7823d423df0d9c921d4ca4c1a58267067c944a03c53a3342` |
| `paper/rev_2026-11-15/SNAPSHOT.sha256` | `e956a461cdae3a62b504b1b1637ae1ee54413967af0aabd816550f71009b1514` |
| `paper/rev_2026-11-15/cover_letter.md` | `4432a7650c69f61ea23aaf802a1d252148be5f9df569c05483626889b8317b1e` |
| `paper/rev_2026-11-15/online_resource.md` | `a297079051410a6d1ea52d2136545545cfc173ef92f0ff26c1ae6deb2c587e9b` |
| `paper/rev_2026-11-15/paper.md` | `6c042e2d8f191bcd187c21ea9d1362288ba0dbbf66ebf864d6b7bc512dd42432` |
| `paper/rev_2026-11-15/title_page.md` | `c80121d214969cf0749076e7c5edd5088b05c9e43d16b78b6b7509c989104218` |

With step X1 as well (`SKIP = ()`), these files differ:

| File | sha256 |
|---|---|
| `paper/rev_2026-11-15/SNAPSHOT.sha256` | `33e008cb534d532e2d9ba69f0a0a89191bc7a57ae2a3a3d3c7a05dc8dad63366` |
| `paper/rev_2026-11-15/online_resource.md` | `22a6bdf844912ec0303c96c14112d7f8128b7214c42103a5123697864d1600bc` |
| `paper/rev_2026-11-15/paper.md` | `afae736135877485c1337fad2871e4f3bf4d160ce3e3abd2de80c95eb465ed9f` |

Base: commit `568eaec`; the script refuses if that commit is not HEAD or an ancestor of HEAD, if `paper/` is not clean, or if a file it reads does not have its sha256 of that commit.
