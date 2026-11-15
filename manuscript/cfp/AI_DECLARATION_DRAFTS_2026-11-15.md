# Statement on the use of AI tools: per-venue drafts for the three authors, 2026-11-15

**Status: DRAFT for approval. Nothing here is in any paper. No paper file was changed and nothing was committed.**

Basis: answer A3 of the corresponding author (one truthful content for all four manuscripts, placed where each publisher wants it), and the investigator's standing rules: never a false "no AI" statement; AI use is declared where the venue requires it, after its current policy is read.

How to read this file:

- Text in a quote block is draft wording.
- `[S1]`, `[S2]` … are **slots**: the authors fill or confirm them. A slot is never a fact until an author confirms it.
- "Record" means a file or commit in the project repositories that states something. A record shows what was written at the time; it does not replace the authors' confirmation.
- Publisher wording is quoted only from pages read on the live sites on 2026-11-14 UTC (table in `VENUE_RECHECK_2026-11-15.md`). The ACM policy was **not read** and no ACM rule is used as a fact here.
- No author name, identifier or address appears in this file.

---

## 1. What each manuscript says today about the authors' use of AI tools

Read in the night of 14–15 Nov 2026 (UTC); the reading ended at 00:21 UTC on 15 Nov, and the paper-repo file hashes were taken at 00:09 UTC.

| Manuscript | Where looked | What it says today | Version read |
|---|---|---|---|
| Paper A (SPIC) | `paper/declarations.md`, `paper/cover_letter_A.md`, `paper/title_page_A.md`, `paper/sec3_measurement_setup.md`, `paper/anon/declarations_anon.md`, supplements | **Nothing.** No AI section in the declarations. Section 3.6 "Analysis code and provenance" begins "The analysis follows four rules" and names no tool. The cover letter has no AI line. Section 3.1 says of the metric: "we use no LLM judge". | repo `vsps-paperA-spic` at `dafba17`, clean |
| Paper B (LRE) | `paper/sec7_limitations_ethics.md` (7.4 "Analysis provenance", 7.5 "Statements and Declarations"), `paper/cover_letter_B.md`, `paper/title_page_B.md`, `paper/sec3_data_and_audit.md` | **Nothing.** Section 7.5 has Funding, Competing interests, Ethics approval, Data and code availability, Authors' contributions; no AI item. Section 7.4 ends "The authors take responsibility for all analyses and text." The v3 matcher rules are described as "derived from training-split counts" with "no human sign-off". | repo `vsps-paperB-lre` at `edf7fee`, clean (the held draft folders were not opened) |
| Paper C (TALLIP) | `paper_v1_analysis/07_disclosures.md`, `10_conclusion.md`, `03_method.md`, `tex/body.tex`, `tex/paperC.tex` | **Nothing.** No AI statement, no acknowledgment block on AI. | repo `vsps-paperC-tallip` at `9b8e6ae`, with uncommitted changes in `tex/` |
| Conference draft (TAIMMA) | `manuscript/conf_taimma_2027/draft_v2/paper.md`, `DRAFT_NOTES.md` | **Nothing.** `DRAFT_NOTES.md` l.91: "No statement on writing tools or AI appears anywhere." "Acknowledgments" and "Disclosure of Interests" are placeholders for the investigator. | `paper.md` sha256 `88cb6a7f…` at 00:06 UTC, `7fe94c48…` at 00:09 UTC and `986d870d…` at 00:21 UTC: the file was being revised by another agent while it was read; the last version still has no AI statement |

### Records of earlier wording and of decisions

| Date | Record | What it says |
|---|---|---|
| 2026-10-21 | run repo commit `e0f094e` ("Record the authors' declarations choices in Papers A and B", CP-053); `manuscript/DECISION_BRIEF_2026-10-21.md` l.54 | The authors chose this text for Papers A and B: "During this work the authors used Claude (Anthropic) and Gemini (Google) to write and run analysis code, to draft and edit the manuscript text and to check references. The authors designed the study, directed and checked all analyses, reviewed and edited all text, and take full responsibility for the content." Methods sentence of Paper A: "Analysis code was written with AI assistance under the authors' direction". |
| 2026-10-21 | run repo commit `ec12520`, first draft of Paper A's declaration | Listed three uses: "to write, run and review analysis code and to draft pre-registration texts"; "to draft and edit the manuscript text"; "to search the literature and check cited identifiers against primary records". Tool names were an author-to-confirm placeholder. |
| 2026-11-01 | `manuscript/AI_MENTION_REMOVAL_2026-11-01.md` (sha256 `267a1b7c…`), ruling PI-1101e | Every statement on the authors' AI use was removed from Papers A, B, C and a fourth draft: 11 passages in A, 16 in B, 1 in C. "No replacement sentence was written, and nothing says that AI was not used." Paper C's removed text read "the authors used AI-assisted tools (a large language model coding and writing assistant)". Paper B's removed text included "The v3 rules were drafted by an AI model (one of the coding assistants of Section 7.4)". Funding lines in A (anonymous copy) and B lost the words "and AI-tool subscriptions". |
| 2026-11-10 | `manuscript/directions/integrity_2026-11-10/METHODS_PARAGRAPH_VERSIONS_2026-11-10.md` (PI-1110q) | Two versions of an "Implementation and verification" Methods paragraph. The investigator chose **Version 1 (no mention of AI tools)**; Version 2 (with AI tools) "stays on file". Neither version is in any manuscript today. |
| 2026-11-15 | answer A3 of the corresponding author | Option (a): one truthful content in all four manuscripts; Methods plus the publisher's declaration place; never a denial that is untrue. |
| after 2026-10-21 | paper repos `reviews/A_codex_review.md`, `reviews/BD_codex_review.md`, `reviews/C_codex_review.md`, `reviews/C_T3_codex_read.md`; run repo `manuscript/reviews/notebooklm_2026-11-11/` (holds `A_text_given_to_notebooklm.md` and review outputs); run repo commit `013c050` ("AI committee meta-reviews and responses") | Further AI tools were used to review analyses and manuscript text: Codex, NotebookLM, and AI reviewer and judge roles. None of these is named in the 2026-10-21 sentence. |

---

## 2. Inconsistencies found

1. **No manuscript carries any statement today, while A3 decides that all four carry one.** The records above show AI tools were used for analysis code, for drafting text and for checking references. Every manuscript needs the text added; none needs a text removed.
2. **Two decisions disagree on the Methods section.** PI-1110q (10 Nov) chose the Methods paragraph without AI tools. A3 (15 Nov) puts AI use in Methods for every venue. Version 2 of the Methods paragraph matches A3; Version 1 does not.
3. **The earlier statements were not one content.** Papers A and B named two tools and three uses. Paper C named no tool and spoke of one "coding and writing assistant". The first draft of A also listed drafting registration texts and searching the literature. A3 asks for one content.
4. **The tool list of 21 Oct is older than the work.** Records after that date show Codex and NotebookLM reviews and AI reviewer and judge roles. The 21 Oct sentence names none of them.
5. **Paper B, v3 matcher rules.** The paper now says the rules were "derived from training-split counts". The removal record says the earlier text was "drafted by an AI model". `paper/STUDY_BRIEF_B.md` l.83 still calls v3 AI-drafted. This is AI use in the research process, not in writing.
6. **Stale planning lines inside the paper repos** (not submission files):
   - Paper A `paper/outline.md` row 3 still names Section 3 "analysis code (AI use)"; `paper/V2_WRITING_PLAN_SPIC_2026-10-27.md` l.146 says AI use "stays described in Methods (§3.6), as it is now" and l.182 says the "existing AI declaration stays as is", while l.370 of the same file and the section files show both were removed.
   - Paper B `paper/outline_B.md` row 7 and `paper/new_vs_FAIR.md` l.34 list "AI-agent provenance" as content of Section 7 and as a new item over the conference paper; `paper/outline_B.md` l.77 and `paper/STATUS.md` l.27 keep the placeholder "AI tools and AI-drafted text (sec7.4)"; `paper/SEPARATION_FAIR_A.md` l.44 and l.81 refer to an "AI-assistance provenance sentence". Section 7.4 has none of this today.
7. **Answer A3 describes the publishers more firmly than the pages read on 14 Nov do.**
   - A3 says Springer wants the "AI Declaration" in the Statements and Declarations block at the end. The pages name "an AI Declaration in your manuscript" and fix **no place, title or wording**.
   - A3 says the Elsevier title must be used exactly. The page says the section is "titled for instance" with that title, and calls the statement a "Suggested format".
   - A3 gives a date and rules for ACM. They were not read on an ACM page today and are not used below.
8. **Placement differed for no stated reason.** Before removal: A had a titled section before the references, B a paragraph inside Section 7.5, C a paragraph inside the acknowledgments block. Sections 4.1–4.4 below give one placement per venue.

---

## 3. Common factual core

One set of facts, the same in all four manuscripts. Only the placement and the sentence form change per venue.

### 3.1 Slots the authors must fill or confirm

| Slot | What to fill | What the records say (not a confirmation) |
|---|---|---|
| **S1** Tools | For each tool: name, model or version, developer. Elsevier asks for "the name of the model or tool, the version used, and the developer or manufacturer" where a tool is part of the methods. | The authors' text of 21 Oct names Claude (Anthropic) and Gemini (Google) (commit `e0f094e`). Later records add Codex and NotebookLM (review files listed in Section 1). No record gives versions. |
| **S2** Uses in the research process | Tick what is true: (a) writing and running analysis code; (b) writing the self-tests and mutation tests; (c) drafting registration documents; (d) searching for related work; (e) checking cited identifiers against their records; (f) reading or reviewing analyses and code; (g) other. | (a), (e): text of 21 Oct. (c), (d): first draft of 21 Oct (commit `ec12520`). (b), (d): Version 2 of the Methods paragraph ("written and checked with the assistance of a generative-AI coding tool … also used to search for related work"). (f): the Codex review files. |
| **S3** Uses in preparing the manuscript | Tick what is true: (a) drafting text from the authors' notes and results; (b) editing and restructuring text; (c) language correction only; (d) translation; (e) organising or checking references; (f) reviewing drafts. | (a), (b), (e): text of 21 Oct ("to draft and edit the manuscript text and to check references"). (f): the review files. (d): no record either way. |
| **S4** Human oversight | Who checked the code and its tests; who verified the numbers against the manifest; who read the cited sources; who reviewed, edited or rewrote the text. State only what was done. | Text of 21 Oct: "The authors designed the study, directed and checked all analyses, reviewed and edited all text". Paper A repo `README.md` l.9: "The authors rewrite the text before submission." Version 2 keeps its oversight sentence in brackets "until the PI confirms it is true". |
| **S5** Code in scope, per paper | The list of analysis code the statement covers (for example object matching, scoring, paired bootstrap, table and figure generation). | Version 2 lists "object matching, scoring, paired bootstrap and table generation". |
| **S6** Software versions | Python and NumPy versions from each paper's lock file. | Per-paper check listed in the Methods-paragraph file. |
| **S7** Self-test coverage, per paper | Which scripts have a self-test and a mutation test. If only some, name them. | Per-paper check listed in the Methods-paragraph file. |
| **S8** AI as a judge or label source | Per paper: confirm whether any reported score or label comes from an AI model acting as judge. | Paper A, Section 3.1: "we use no LLM judge". Paper B, Section 7.4 rule 4: "Model-generated signals are never gold or human evidence." No such sentence was found in Paper C or the conference draft. |
| **S9** Paper B, v3 matcher rules | Whether the v3 results stay in the rewritten paper, and how the rules were made. | Removal record items B2, B4, B9: earlier text said "drafted by an AI model" and "not reviewed by a person". |
| **S10** Data and text given to the tools | Whether unpublished manuscript text, restricted third-party data (captions, human ratings) or personal data were entered into any tool, and whether each tool's terms keep the input private and unused for training. | `A_text_given_to_notebooklm.md` shows that Paper A text was given to NotebookLM. No record was found on restricted data. |
| **S11** Translation | Whether any manuscript text was translated by an AI tool. | No record. |
| **S12** Figures | Whether any figure was created or altered by an AI image tool, or all figures are plots produced by scripts from the result files. | No record of an AI image tool. |
| **S13** Section numbers | The Methods section number in each manuscript where the paragraph goes. | Paper A: Section 3.6. Paper B: Section 7.4 today (the rewrite may move it). Paper C and the conference draft: to be set. |

### 3.2 Core wording, long form

Part M, for the Methods section (research process). It is Version 2 of the 10 Nov file, with the tool sentence opened into slots.

> **Implementation and verification.** Each confirmatory analysis in this paper was specified in a registration document, fixed by its SHA-256 hash, before the data it governs were read; exploratory analyses and analyses added later are labelled as such. The analysis code ([S5]) is written in Python [S6] with NumPy [S6]. It was written and tested with the assistance of generative-AI coding tools ([S1: name, version, developer of each]), working from the authors' specifications. [S2c: The same tools helped to draft the registration documents.] [S2d, S2e: They were also used to search for related work and to check cited identifiers against their records.] [S2f: Drafts of the code and of the analyses were also read by [S1 tool].] [S7: Each script behind a registered result] ships with a self-test on synthetic inputs with known answers and with a mutation test, in which one registered rule is broken at a time and the self-test must fail. Each reported number is listed in a manifest that names the output file and key it comes from, and the files are identified by their hashes. [S4: The authors reviewed the code and its tests, verified the reported results against the manifest, read the cited sources and checked each reference against its record.] [S8, only where true: No AI model was used as a judge or as a source of labels for any reported score.] The authors take full responsibility for the code, the results and the content of this article.

Part D, for the declaration (manuscript preparation).

> During the preparation of this work the authors used [S1] in order to [S3: draft and edit the text of the manuscript from the authors' notes and results; translate …; organise and check the references; review drafts]. After using these tools, the authors [S4: reviewed and edited] the content as needed and take full responsibility for the content of the published article.

Rules for both parts:

- Delete every bracketed clause that is not true. Add any use that is missing.
- The same tools, the same uses and the same oversight verbs appear in all four manuscripts.
- Nothing in any manuscript, cover letter or form says or implies that AI was not used.
- Paper B only, if S9 keeps v3: add in the section that describes the matcher: "The v3 rules were drafted with [S1 tool] from training-split counts and were not reviewed by a person."

---

## 4. Placement and wording per venue

### 4.1 Paper A — Signal Processing: Image Communication (Elsevier)

Policy read: https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals (14 Nov 2026, 21:38 UTC; "Policy updated June 2026."). The journal's own guide for authors could not be opened on 14 Nov (bot check); its AI section was last read on 10 Nov in `AI_POLICY_CHECK_2026-11-10.md`.

What the page requires, in its words:

- "Authors should disclose the use of AI tools for manuscript preparation in a separate AI declaration statement included in their manuscript upon submission. This statement will appear in the published article."
- Place: "you must include a separate declaration section at the end of your manuscript, immediately before the references, titled for instance: 'Declaration of generative AI and AI-assisted technologies in the manuscript preparation process.'"
- Content: "the name of the AI tool used, the purpose of its use, and the extent of their oversight".
- Research process: "Where AI tools are used as part of the research process rather than manuscript preparation, this use should be described in detail in the Methods section." Code: "If authors write or edit code using AI tools as part of their research, they should declare this in detail in the Methods section".
- References: "If these or any other AI tool are used to select, collate, generate or edit references, this should be declared in the manuscript."
- Translation: "you should disclose the use of AI tools for translations included in your manuscript."
- Exempt: "Basic checks of grammar, spelling and punctuation do not need a declaration statement. However, when an AI tool makes substantive changes to sentence structure or organization of a part of the text, this should be disclosed."
- Tool terms: "Authors must check the terms and conditions of any AI tool that they use to ensure that the privacy and confidentiality of their data and input, including their unpublished manuscripts, is maintained."
- "Authors should not list AI tools as an author or co-author".

Draft placement:

1. **Section 3.6** ("Analysis code and provenance"): Part M of Section 3.2, merged with the four rules already there.
2. **New section immediately before the references**, after the other declarations, with the publisher's suggested title and format:

> **Declaration of generative AI and AI-assisted technologies in the manuscript preparation process**
>
> During the preparation of this work the authors used [S1] in order to [S3]. After using these tools, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

3. If S3(e) or S2(e) is ticked, the words "organise and check the references" stay in the declaration; that meets the sentence on references.
4. Cover letter: the pages read ask for no AI line there. Keep none unless the journal's guide, once read, asks for one.
5. Figure captions: an AI line is needed only if S12 finds a figure made with an AI image tool.

### 4.2 Paper B — Language Resources and Evaluation (Springer)

Pages read on 14 Nov 2026: journal guidelines https://link.springer.com/journal/10579/submission-guidelines (21:39 UTC); publisher pages https://link.springer.com/brands/springer/journal-policies (21:41), https://www.springernature.com/gp/policies/editorial-policies/ai-manuscript-preparation and `/using-ai-in-research` (21:44), `/ai-editor-guidance` (21:42).

What the pages require, in their words:

- Journal page: "Use of an LLM should be properly documented in the Methods section (and if a Methods section is not available, in a suitable alternative part) of the manuscript. The use of an LLM (or other AI-tool) for 'AI assisted copy editing' purposes does not need to be declared." "Large Language Models (LLMs), such as ChatGPT, do not currently satisfy our authorship criteria."
- Publisher, writing: for language editing, translation and "drafting sections based on author input": "Clearly describe use and confirm author accountability". Not permitted: "Writing results or discussion independently; generating scientific claims or interpretations".
- Publisher, research: literature discovery and "code scaffolding": "Describe tool and purpose and take accountability"; analysis support: "Provide clear methodological description and validation steps and take accountability". Not permitted: "using sensitive or restricted data in public tools".
- Publisher, declaration: the AI Declarations policy "sets out the expectation for clear declaration of any AI use, including for research purposes, for writing/manuscript preparation and for peer review". The manuscript page names "an AI Declaration in your manuscript". **No page fixes its place, title or wording.**
- At submission: "authors and reviewers will also be asked to confirm that they have read and complied with the Springer Nature AI Editorial Policies when submitting a manuscript".
- "Where AI use is not declared, editors may need to investigate or request clarification".

The journal page and the publisher pages differ on language editing. The draft follows the publisher pages, which ask for more.

Draft placement (the place is our choice, since Springer fixes none):

1. **Methods** (the section that holds the analysis rules, Section 7.4 today): Part M of Section 3.2. If S9 keeps the v3 matcher, its provenance sentence goes in the matcher section.
2. **"Statements and Declarations", before the reference list**, as one more item beside Funding and Competing interests:

> **AI Declaration.** The authors used [S1] (i) in the research, to write and test the analysis code from the authors' specifications [S2c–S2f as true] (Section [S13]); and (ii) in preparing the manuscript, to [S3]. [S4: The authors checked the code and its tests, verified every reported number against the manifest, and reviewed and edited all text.] The authors are accountable for all content of this article. No AI tool is an author.

3. Submission system: the submitting author answers the compliance question truthfully. The form was not seen (login).
4. Cover letter: the journal's cover-letter list has no AI item. Keep none.

### 4.3 Conference draft — TAIMMA 2027, Springer CCIS proceedings

Pages read on 14 Nov 2026: https://link.springer.com/series/558/information-for-authors-and-editors (21:42 UTC); Springer "Instructions for Authors" PDF linked there (21:45); https://www.springernature.com/gp/policies/book-publishing-policies (21:46); conference site https://www.taimma-conf.org/ (21:38).

What the pages require, in their words:

- Proceedings authors must "abide by our book publishing policies and respective codes of conduct". Author instructions, section 2: "For Springer Nature's policy on the use of AI, please refer to this page."
- Book policies, "AI Editorial Policies", authors: "Remain fully accountable for originality, accuracy, and integrity"; "Disclose AI use for trust and transparency". Low-risk use: "Permitted. Disclosure enhances trust and transparency and clearly demonstrates human accountability." Use that brings new intellectual content: "Permitted with human oversight, verification, and transparency through disclosure." Not permitted: "Assigning authorship or accountability to AI systems or tools".
- **No place, title or wording is given for proceedings papers.**
- Conference site: only "AI-generated images and diagrams should be avoided."

Draft placement (our choice; kept short because the paper has a 12–15 page limit):

1. **Method section**, one sentence:

> The analysis code was written and tested with the assistance of generative-AI coding tools ([S1]) from the authors' specifications; [S4: the authors reviewed the code and verified every reported number against its output file].

2. **Under "Acknowledgments"**, the heading the draft already has, one short paragraph:

> **AI declaration.** The authors used [S1] to [S3, short: draft and edit text and check references]. The authors reviewed and edited all content and are accountable for it.

3. No AI-made image or diagram may be in the paper (S12).
4. The content must equal the Paper C statement, because the conference paper is a version of Paper C.

### 4.4 Paper C — ACM TALLIP

**ACM policy: UNREAD.** Every ACM page refused access on 13 and 14 Nov 2026 (`VENUE_RECHECK_2026-11-15.md`, section 3). No ACM rule, date or threshold is stated here, and the ones written in answers A3 and T3 are not used as facts.

Until a person reads the ACM Policy on Authorship and the TALLIP author guidelines in a normal browser:

1. The **facts** for Paper C are the common core of Section 3 (the same as for the conference draft).
2. Holding text for the Methods section: Part M of Section 3.2. It describes what was done and depends on no publisher rule.
3. Whether a separate statement on writing help is needed, where it goes, and what the submission form asks: **open**, slot **S14**.

---

## 5. What the authors must decide

Each item carries a recommendation; the decision is the authors'.

1. **Tool list (S1).** Confirm every tool, with version and developer. Recommendation: include each tool that wrote code, drafted or edited text, checked references or reviewed drafts, also those used only after 21 Oct.
2. **Methods section.** Confirm that A3 replaces the choice of 10 Nov (PI-1110q), so that Version 2 of the Methods paragraph, as opened in Section 3.2, enters each paper. Recommendation: yes; Elsevier and Springer both ask for research use in Methods.
3. **AI used to review drafts and code** (S2f, S3f). Recommendation: declare it in one clause; it costs a few words and leaves nothing unsaid.
4. **The oversight sentence (S4).** It may be signed only when it is true. If the authors rewrite the text before submission, the sentence is fixed after the rewrite, with the verb that fits ("reviewed and edited" or "rewrote"). Springer does not permit AI "writing results or discussion independently"; the authors confirm that the argument, the interpretation and the conclusions are theirs.
5. **LRE: place of the AI Declaration.** Recommendation: inside "Statements and Declarations" before the references, plus the Methods paragraph. Also declare language editing, although the journal page exempts copy editing, because the publisher pages ask for it.
6. **CCIS: place.** Recommendation: one sentence in the method section and a short paragraph under Acknowledgments (about 60 words in all).
7. **TALLIP.** Wait for the page read assigned in answer X2; then fill S14. Recommendation: do not finalise C's wording before that.
8. **Paper B, v3 matcher (S9).** If the v3 results stay, state in Methods that the rules were drafted with an AI tool and not reviewed by a person. If v3 leaves the paper, nothing is needed.
9. **Data and text given to the tools (S10).** Confirm what was entered and that each tool's terms keep it private. If restricted third-party data were entered into a public tool, tell the corresponding author before any submission; Springer lists "using sensitive or restricted data in public tools" as not permitted.
10. **Translation and figures (S11, S12).** Confirm. An AI translation is disclosed (Elsevier). An AI-made figure needs a caption line (Elsevier, Springer) and is to be avoided at the conference.
11. **Cover letters.** Recommendation: no AI line in any cover letter; no page read asks for one.
12. **Funding sentence.** The words "and AI-tool subscriptions" were removed from two funding lines on 1 Nov. No policy read asks for them. Recommendation: leave the funding sentences as they are; this is the authors' choice.
13. **One approval for all four.** All three authors approve the filled core once; the per-venue texts are then cut from it without new facts.

## 6. Open slots (summary)

S1 tools, versions, developers · S2 research uses · S3 manuscript uses · S4 oversight (who, what, which verbs) · S5 code in scope per paper · S6 Python and NumPy versions · S7 self-test coverage per paper · S8 AI as judge or label source, per paper · S9 Paper B v3 matcher · S10 data and text given to the tools, tool terms · S11 translation · S12 figures · S13 section numbers · S14 ACM placement and wording (policy unread).

After approval, the stale planning lines of inconsistency 6 are corrected in the paper repos together with the new text.

## Sources

- Answer file, sections A3 and T3 only: `manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_7e8f958d.md`.
- Live-page record: `manuscript/cfp/VENUE_RECHECK_2026-11-15.md` (rows A23–A27, B16–B19, D13, D26; URLs and read times there).
- Project records: `manuscript/AI_MENTION_REMOVAL_2026-11-01.md`; `manuscript/DECISION_BRIEF_2026-10-21.md`; `manuscript/directions/integrity_2026-11-10/METHODS_PARAGRAPH_VERSIONS_2026-11-10.md` and `AI_POLICY_CHECK_2026-11-10.md`; run repo commits `e0f094e`, `ec12520`, `013c050`; the review files named in Section 1.
- Not opened: `.session_backup/`, the held Paper B draft folders, any label or key file.
