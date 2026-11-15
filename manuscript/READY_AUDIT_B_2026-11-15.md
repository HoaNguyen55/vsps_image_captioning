# Paper B (LRE): submission-readiness audit of the committed shell, 2026-11-15

Written 2026-11-15T08:45Z (15:45 Vietnam time). This audit is outcome-free. It scores only the items that do not depend on results. It does not repeat any figure or outcome of the study. Where the committed repo prints results of an earlier route, the report points to the file and line only.

## Scope and custody

- **Paper repo:** `/mnt/d/vsps_papers/vsps-paperB-lre`, HEAD `edf7fee5978a58d97f276f9d20bb83f50feed3c2`, clean working tree. No paper file was changed and nothing was committed.
- **Venue sources:**
  - `.claude/skills/venue-lre/SKILL.md` (sha256 prefix 18c09b3e9fcfd440);
  - `manuscript/cfp/VENUE_RECHECK_2026-11-15.md` §2, rows B1–B30 (sha256 prefix 066abf12cd0dba95; the LRE guidelines page was read in full);
  - the Springer Nature template's own declarations list at `paper/build/templates/springer_sn_jnl/sn-article.tex:551-566`.
- **Build:** run in scratch from `git archive HEAD paper`, into `/tmp/claude-1000/-mnt-d-vsps-image-captioning/cbc155a0-619c-4f6d-b27a-ab9635fb7056/scratchpad/bbuild/`. The repo copy was laid out under the path the script expects (see item 7). Only the page count, the placeholder list and the citation-label check were read from the build.
- **Not opened:** `.session_backup/` (apart from the grep below and, after the 08:40Z custody release by CC-418, the two ruling files `CC-415.txt` and `CC-417.txt`), `~/vsps_labels_b`, any `key.json`, any label file, the held rewritten draft, and the run-repo records of the pair arm. The release does not widen the audit. The audit stays scoped to the committed shell.
- **LOG exception:** `.session_backup/2026-10-13/decisions/LOG.md` was searched with grep for the five named ids. **Deviation:** the pattern also matched and displayed two other lines that cite CC-415 in their text, `OPS-1115s-cc415-w1` and `PI-1115n`. Nothing that appears only in those two lines is used here. Every disclosure item below comes from INC-1115a, INC-1115b, CC-415, CC-417 or OPS-1115ak.

## Counts

46 items: **READY 17**, **NOT READY 12**, **BLOCKED 11**, **WAITS FOR THE RESULT TRANSFER 6**.

## A. Article type, length and format

| # | Item | Status | Evidence / what to do |
|---|---|---|---|
| 1 | Article type and scope | READY | Full-length resource/evaluation paper (audit, protocol card, kit) fits B1 "creation, annotation, and use of language resources ... evaluation". |
| 2 | Length | WAITS | The scratch build gives **29 pages** against "typically 18-25" (B2). There is no hard limit. The rewritten draft adds the rater arm, so recount after the transfer and trim or justify. The comment at `paper/sec7_limitations_ethics.md:63` speaks of a "25-page limit". The journal sets no such limit; it is a target of our own. |
| 3 | Title | READY | `paper/title_page_B.md:5` is concise and informative (B5 gives no number). Re-check it if the rater arm becomes a headline contribution. |
| 4 | Abstract | NOT READY | `paper/outline_B.md:10` has **145 words** after comments are stripped, below the 150-word floor (B6). "CIDEr" and "CIDEr-D" are not expanded, and B6 forbids undefined abbreviations. Fix both when the abstract is rewritten at the transfer. |
| 5 | Keywords | READY | `paper/outline_B.md:13` has 6 keywords (B7: 4–6). |
| 6 | Headings, footnotes, formulas | READY | At most 3 levels in sec1–sec8. No endnotes. No displayed formulas (B10). |
| 7 | Editable source files, and the build | NOT READY | `paper/build/build_B_springer.sh:7` reads `$repo/manuscript/journal_draft_B`, which does not exist in the paper repo, so the committed repo cannot build itself. Fix: point `src` at `paper/`. B11: without a complete set of editable sources at every submission and revision, the paper "will not be considered". Ship the `.tex`, `.bib`, `sn-jnl.cls` and `sn-apacite.bst` (with the DOI patch). |

## B. Special Focus on less-resourced languages (B3, B4)

| # | Item | Status | Evidence / what to do |
|---|---|---|---|
| 8 | Flag in the cover letter | READY | `paper/cover_letter_B.md:7`. |
| 9 | Focus on the language's properties, without a comprehensive linguistic overview | READY | The cover letter names segmentation, tone marks and classifier nouns. `paper/sec1_intro.md:7` gives a short low-resource paragraph, not a linguistic survey. |
| 10 | No textbook re-description of known methods | READY | sec1–sec8 have no metric formulas or method walk-throughs. |
| 11 | Literature review of both kinds (same methods; same problem with other methods) | READY (committed scope) | `paper/sec2_related.md:5-39` covers datasets, systems, metrics and their reporting, benchmark validity, hallucination, reference independence and second caption sets, with the comparison table at :23. The new pair arm needs its own literature on human preference judgments of captions; see checklist R13. |
| 12 | State-of-the-art methods | READY | Transformer VLM backbones (Qwen2.5-VL, `paper/sec4_system.md`). |
| 13 | "Comprehensive evaluation" | WAITS | Depends on the transferred results. |
| 14 | English standard ("returned without review") | BLOCKED | Needs the investigator's language pass on the final text. Standing rule: the PI rewrites after the "ready" notice. |

## C. Review model

| # | Item | Status | Evidence / what to do |
|---|---|---|---|
| 15 | Single-blind | READY | Names and affiliations are in the manuscript (B9). No anonymisation is needed. |

## D. Statements and Declarations (B13, B14, B16–B18)

| # | Item | Status | Evidence / what to do |
|---|---|---|---|
| 16 | Placement and form | NOT READY | The block is subsection 7.5 inside "Limitations and ethics" (`paper/sec7_limitations_ethics.md:55`), before Section 8 Conclusion. Fix: make it an unnumbered "Declarations" section after the Conclusion and immediately before the References (B13; template `sn-article.tex:551`). |
| 17 | Funding; Competing interests (text) | READY | `paper/sec7_limitations_ethics.md:57,59`. |
| 18 | Missing headings | NOT READY | The template expects "Ethics approval and consent to participate", "Consent for publication" and "Materials availability", writing "Not applicable" where a heading does not apply (`sn-article.tex:558-566`). None of the three is present. The consent content itself is item 26. |
| 19 | Data availability is not self-contained | NOT READY | `paper/sec7_limitations_ethics.md:63` reads "See Section 3.6". B20 requires a data availability statement. Write it in full in the Declarations: repository, DOI, access route, third-party sources and their terms, and what is withheld and why. |
| 20 | Author contributions on the title page | NOT READY | B14: contributions "should be listed at the separate title page". They are only in 7.5 (`:65`); copy them to `paper/title_page_B.md`. |
| 21 | Declarations typed into the submission system | BLOCKED | B14: contributions, competing interests and funding must be entered in the interface, and "only the information submitted via the interface will be used". This is the investigator's task at submission. |
| 22 | AI-tool statement | READY | The investigator decided on no AI-tool statement. A grep of all `paper/*.md` finds no sentence claiming that no AI tool was used. Nothing to add. (The publisher form asks the submitter to confirm compliance, B18; that is the investigator's choice at submission.) |
| 23 | AI used as a research instrument, described in Methods | NOT READY | This is separate from item 22, and the investigator's decision does not cover it. B16: LLM use in the research "should be properly documented in the Methods section". `paper/sec6_discussion.md:23` (Discussion, added at HEAD) describes a score in which "a language model splits a caption into propositions" and "a vision-language model answers yes or no". It gives neither model name nor version nor prompt nor settings, and no Methods section describes them. Fix: describe both models, their versions, prompts and decoding settings in Section 4 (or a methods subsection), and point to it from 6.2. |

## E. Ethics and consent of the raters (B15)

LRE asks for three things:
- (i) "study-specific approval by the appropriate ethics committee for research involving humans", or the reason it does not apply;
- (ii) a statement that informed consent was obtained;
- (iii) per the data section, "Participant consent should be obtained and documented prior to data collection".

The template adds "Consent for publication" (Not applicable unless identifying information is shown).

**What exists in the paper repo** (`git grep` over HEAD for consent, information sheet, ethics committee, IRB, institutional review): no consent form or consent record, no information sheet, no rater instructions, no ethics approval or exemption, and no registration or addendum of the pair arm. The only hits are the venue card and the template. The run repo commits `aee9520` and `5eee5e3` (subjects seen in the session context, files not opened) carry the remote-access addendum and the pin package. Neither subject mentions consent.

| # | Item | Status | Evidence / what to do |
|---|---|---|---|
| 24 | Sentences that are now false | NOT READY | Three committed sentences say that no human data were collected: `paper/sec7_limitations_ethics.md:11` ("No human judgments ... no new human annotation"), `:50` (item 4 of 7.4) and `:61` ("Ethics approval. Not applicable: no new data from human participants were collected"). They must be replaced in the rewritten draft. The replacement text comes with the transfer. |
| 25 | Ethics approval, or a stated exemption with its reason | BLOCKED | The investigator must say whether any committee approval or exemption exists. If none was sought, the statement says so and gives the reason; it must not claim approval. |
| 26 | Informed consent, documented before collection | BLOCKED | The investigator must say whether a dated consent record exists for each of the two raters from before their answers. If none was documented before collection, this cannot be repaired afterwards. The text must then state what was done, and must not say "documented prior to data collection". |
| 27 | Earlier FAIR-2026 ratings that the paper reuses | BLOCKED | `paper/sec7_limitations_ethics.md:13` reuses an earlier two-rater set. The investigator must say whether the consent given then covers this use. |
| 28 | Rater-procedure disclosures | WAITS | Checklist R1–R14 below. |
| 29 | Wording "and the rater" | BLOCKED | CC-417 W2 is BLOCKING for the paper: the paper may say that the rater confirms working alone only with the rater's own written line. Without it, the claim rests on the investigator's statement and is worded that way (R5). |

## F. Data availability (B3, B20)

| # | Item | Status | Evidence / what to do |
|---|---|---|---|
| 30 | Zenodo DOI and deposit timing | BLOCKED | Placeholders at `paper/sec3_data_and_audit.md` (Licence and archive paragraph) and `paper/sec7_limitations_ethics.md:28`; the build shows both in the PDF. The record stays unpublished until the Paper A decision (comment at `paper/cover_letter_B.md:25`, CC-074). The investigator decides the timing and the reviewer access link. |
| 31 | Kit licence | BLOCKED | "[AUTHOR TO CONFIRM: licence]" at `paper/sec3_data_and_audit.md` (same paragraph), `paper/sec7_limitations_ethics.md:28,63`. |
| 32 | Availability of the rater answers | WAITS | The Special Focus asks for resources to be public "or the reasons stated". The statement on the pair-arm labels (released, withheld, or on request, and why) follows the transfer. |
| 33 | Third-party dataset terms and permission wording | READY | The visible text says the KTVIC and UIT-OpenViIC authors "agreed" (sec3 Datasets paragraph), without "in writing". UIT-ViIC is handled as aggregates with no permission claimed. One check is recommended: the hidden comment at `paper/sec7_limitations_ethics.md:63` and `paper/outline_B.md:77` speak of a "written confirmation ... e-mails on file". After the Paper A PASCAL-50S correction (run-repo commit b9d3deb), check that record before any later text says "in writing". |

## G. References (B12)

| # | Item | Status | Evidence / what to do |
|---|---|---|---|
| 34 | Author-year style, alphabetical, APA 7 | READY | `sn-jnl` with `sn-apa` and `sn-apacite.bst`. The build's label check: 108 mentions matched, 0 without exactly one rendered label, 63 of 66 bib keys cited (the 3 uncited keys are left out of the list). |
| 35 | Full DOI links | NOT READY | Five cited entries have no DOI field: `lovenia2024seacrowd`, `buettner2024quantifying`, `buettner2025multimodal`, `zhang2024scaling`, `lin2024selecting` (arXiv ids only, `paper/paperB.bib`). Check each primary page for a proceedings DOI or the arXiv DOI. Do not guess. |
| 36 | FAIR 2026 reference | BLOCKED | The PDF reference list prints "[AUTHOR TO PROVIDE: pages and DOI once listed on IEEE Xplore]" (`nguyen2026vsps`). It waits on the external listing. |

## H. Figures and supplementary material (B19, B21–B23)

| # | Item | Status | Evidence / what to do |
|---|---|---|---|
| 37 | Figure rules | READY | The committed main text has 0 figures (build report). Any figure in the rewritten draft must meet checklist R14. |
| 38 | Online Resource naming and file | NOT READY | Section 1 names the supplement "Online Resource 1" once (`paper/sec1_intro.md:23`). It is then cited about 30 times as "Supplementary S…" / "Supplementary Table S…" (sec1 4, sec3 13, sec4 3, sec5 3, sec6 2, sec7 6). B23 says to refer to it as "Online Resource". Name the file `ESM_1.pdf`. The supplement build crashed in the repo copy only because the e-mail is redacted (`build_B_springer.sh`, supp_meta step), so no Online Resource PDF was produced. Fill the e-mail at submission, then build. |

## I. Cover letter (B24, B26)

| # | Item | Status | Evidence / what to do |
|---|---|---|---|
| 39a | First author: ORCID | NOT READY | `paper/cover_letter_B.md:31` is a placeholder, but `paper/title_page_B.md:9` already has the first author's ORCID. Copy it across. |
| 39b | Co-authors: ORCID, homepage or CV | BLOCKED | `paper/cover_letter_B.md:32-33` are placeholders. These need the co-authors' own identifiers, which must not be looked up or invented. |
| 40 | Re-use of the FAIR 2026 paper | READY | `paper/cover_letter_B.md:17` (B26 "transparency on the re-use of material"). |
| 41 | Related unpublished manuscripts | NOT READY (at submission) | Lines 18–19 describe Paper A and Paper C as "in preparation". Update both to their status on the submission day (A at SPIC; C's conference version at TAIMMA 2027 if submitted by then). |
| 42 | Body content | WAITS | `paper/cover_letter_B.md:11-14` print figures of the earlier route (not repeated here). The rater arm is not mentioned. Rewrite from the transferred draft. |

## J. Title page (B13, B25)

| # | Item | Status | Evidence / what to do |
|---|---|---|---|
| 43 | Active e-mail of the corresponding author (title page and cover letter) | BLOCKED | Redacted in the repo copy (`paper/title_page_B.md:15`, `paper/cover_letter_B.md:40`) by standing rule. The investigator fills it at submission. Co-author ORCIDs ("if available") are the same request as 39b. |
| 44 | Title, names, affiliations, corresponding-author mark | READY | `paper/title_page_B.md:5-15`. |
| 45 | Acknowledgments section on the title page | WAITS | B13 places acknowledgments on the title page. None exists. Whether the raters or the dataset authors are thanked follows the transfer, and is bound by item 29. |

## Disclosures the rewritten draft must contain (rater procedure)

Sources: INC-1115a, INC-1115b, CC-415, CC-417, OPS-1115ak. The ruling files `CC-415.txt` and `CC-417.txt` were read after the coordinator's note that custody was released at 2026-11-15T08:40Z (CC-418; CC-418 itself was not read). The two fixed paper sentences are quoted word for word in R0 and R3. Counts and figures in the rulings are not carried here.

- [ ] **R0 Fixed paper disclosure (CC-417 ruling 5, word for word; it replaces the CC-415 ruling 4 sentence; CC-417 W2 BLOCKING before submission). Place it beside plan l.83.** "The second rater answered in person on an author's laptop, on the same rating page and instructions; a key-protected remote link had been prepared and opened but no answer was saved through it. During the session the author passed on one request to pause and one to continue, and said nothing about the items. That this rater worked alone, without the author watching or explaining and without search or AI tools, rests on the statement of the author; no third party observed the session, and the rating server keeps no record of the answering client." R1, R4, R5 and R7 below are the facts behind this sentence. They are covered by R0 and need no extra sentence unless a reviewer asks.
- [ ] **R1 Mode.** The second rater (R2) answered **in person at an author's laptop**. That is the mode of the registration (prereg PI-5) and a **departure from addendum v1.1** (remote session). The remote-only sentence of addendum l.39 is **not** used. Plan l.205 ("shown locally") holds as written (CC-415 ruling 4).
- [ ] **R2 Route of the answers.** R2's answers were saved through the laptop's loopback address, not through the key gate, and message M2 was never sent. This is the addendum v1.1 step 7 case (INC-1115b). The coordinator kept the rating server running instead of stopping it, which is a stated deviation from the word "stop" of step 7 (INC-1115b). Whether this goes into the paper or only the record follows the CC-415 record-line sentences.
- [ ] **R3 Practice round (word for word, OPS-1115ak (b), CC-415 ruling 3; supersedes the CC-406 ruling 2 sentence).** "In a departure from the registered procedure, neither rater took the eight-pair practice round: both answered on the main page, where the instructions panel starts closed; the registered analysis uses all answers unchanged."
- [ ] **R4 One pause request and one continue request.** The investigator relayed one pause request and one continue request to the rater at the request of the coordinator, and said nothing about items (OPS-1115ak (c)). CC-417 calls both procedural and requires them to be disclosed.
- [ ] **R5 Working alone.** The claim that the rater worked alone **rests on the investigator's statement** (OPS-1115ak (a), CC-417). If that statement has any clause about tools the rater used, word it as part of the investigator's statement about the rater's answers. It must never read as a paper-wide statement on AI use (the investigator decided on no AI-tool statement, and nothing may say that no AI tool was used).
- [ ] **R6 "And the rater".** R0 may read "rests on the statement of the author and the rater" only once the rater's own line is on record (CC-417 ruling 5 and W2; CC-415 W7, still open; item 29). The recommended step, from CC-417 "For the PI", is to ask the rater for one line saying they answered alone, without AI tools or search. Without that line, R0 stays as worded.
- [ ] **R7 Status of R2's file.** It is R2's data by CC-417 (option 1), on the investigator's statement. The browser-client check (CC-415 W1) is recorded as **inconclusive, not passed**: the browser ran outside the Linux side. Its disqualifying trigger did not fire: no non-browser client was seen, no second tunnel ran, and no save went through the gate. No record excludes a program on the other side of the laptop (OPS-1115ak (a)). In the paper this is carried by the last clause of R0 ("the rating server keeps no record of the answering client"). No further sentence is ruled.
- [ ] **R8 Exposure without the key (INC-1115a; CC-415 ruling 6: one clause in the paper's disclosure of the human arm, wording not fixed and NON-BLOCKING; CC-417 ruling 5: "INC-1115a clause stands").** For **about 27 minutes** (1,639 s, before R2's session), a second public tunnel exposed R2's pair page **without the key gate**. The tunnel was started by another tool. Not known: its address, who received it, and whether any person or automated reader opened the page. The rating server keeps no request log. No answer was written during that time. The tunnel was stopped when it was found.
- [ ] **R9 One rater is an author.** The other rater is the investigator. INC-1115b refers to the same practice-round departure as "ruled for the PI in CC-404 and CC-406". The paper states that one of the two raters is an author, and how that rater was kept from the outcome.
- [ ] **R10 Analysis unchanged.** The registered analysis, the pinned code and the return codes are unchanged (CC-417 ruling 6). The registered analysis uses all answers (R3). No sensitivity, exclusion or weighting was added because of the incident. If the pinned code took the single-rater path, plan l.159 wording applies and R0 is not printed as a two-rater disclosure (CC-417 ruling 6). Which path was taken is a result and is not stated here.
- [ ] **R10a Practice prohibitions (CC-404 W6 as extended by CC-415 ruling 3).** No sentence may say that either rater took practice first. The registered "non-author rater alone" row may not be described as free of this departure.
- [ ] **R10b Pace line (CC-417 W4, NON-BLOCKING).** If a pace line goes into the supplement (CC-406 W5), say what the on-screen time field measures: the time from when the screen was shown to the save. Pace is descriptive and never used to exclude (CC-415 ruling 2, CC-406 ruling 4).
- [ ] **R11 Not done.** No public route was opened to the rating port, and no bot protection was switched off (INC-1115a). This is for the record. Print it only if R8 is printed in a way that makes it relevant.
- [ ] **R12 Ethics and consent text.** Replace the three false sentences (item 24) with the facts from items 25–27.
- [ ] **R13 Literature.** Add earlier work on human preference judgments of captions to Section 2 (Special Focus literature rule, item 11).
- [ ] **R14 Any new figure.** EPS/TIFF; line art ≥ 1200 dpi, halftone ≥ 300, combination ≥ 600. Bold "Fig. N" captions with no final period. Patterns as well as colour, and contrast ≥ 4.5:1 (B21). Disclose AI-assisted visuals in the caption (B19).

The non-blocking items of both rulings are mapped as follows:
- CC-415 W5 is covered by R0, R3, R8 and R10a.
- CC-415 W6 is a record line, not a paper item.
- CC-415 W7 is covered by R6.
- CC-417 W3 is the investigator's line on the relayed pause, a record item.
- CC-417 W4 is covered by R10b.
- CC-417 W5 carries CC-415 W6 and W7.

## NOT READY, one line each

1. Abstract is 145 words (< 150) and leaves CIDEr/CIDEr-D undefined (`paper/outline_B.md:10`).
2. The build script reads `manuscript/journal_draft_B`, which is absent in the paper repo, so the editable sources cannot be rebuilt (`paper/build/build_B_springer.sh:7`).
3. Declarations is subsection 7.5 before the Conclusion; move it to an unnumbered section right before the References.
4. The headings "Ethics approval and consent to participate", "Consent for publication" and "Materials availability" are missing.
5. The data availability statement is the cross-reference "See Section 3.6"; make it self-contained.
6. Author contributions are not on the title page.
7. The LLM and VLM of the Section 6.2 score are unnamed, with no versions, prompts or settings, and no Methods description.
8. Three sentences say no human data were collected (`paper/sec7_limitations_ethics.md:11, :50, :61`).
9. Five cited arXiv-only bib entries lack a DOI link.
10. The supplement is cited as "Supplementary S…" (~30×) instead of "Online Resource 1"; the file is not named ESM_1 and no PDF was built.
11. The cover letter has a placeholder for the first author's ORCID, which is already on the title page.
12. The cover letter's lines on related manuscripts (A, C) give "in preparation"; update them on the submission day.
