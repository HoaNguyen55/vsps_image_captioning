# Paper C (ACM TALLIP): submission-readiness audit, 2026-11-15

Written 2026-11-15T08:51Z (15:51 Vietnam time). This is a report only. No paper file was changed and nothing was committed or staged. Builds and checks ran on scratch copies.

**Object.**
- Paper repo `/mnt/d/vsps_papers/vsps-paperC-tallip`, HEAD `55315cad9e57073a9ccd346597fae34e393db69a`.
- Paper text: `paper_v1_analysis/00`–`11_*.md`.
- Manifest: `paper_v1_analysis/number_manifest_C.tsv`, 5,667 rows, sha256 prefix `83414dc3d863bbe6`.
- Bibliography: `paper_v1_analysis/paperC.bib`, 67 entries, sha256 prefix `a415c4daa4d8c40b`.

**The tex/ and PDF files.** The uncommitted files in `paper_v1_analysis/tex/` are a toolchain build of HEAD. A scratch rebuild from the HEAD Markdown gave a `body.tex`, `supp_body.tex` and `paperC.tex` byte-identical to them (`paperC.tex` sha256 prefix `d5289775821edd86`). The committed `tex/paperC.pdf` dates from 2026-11-11 (43 pages) and is stale.

**Rules applied.**
- The checklist of `.claude/skills/venue-tallip/SKILL.md`.
- `manuscript/cfp/VENUE_RECHECK_2026-11-15.md`: no ACM page could be read on 2026-11-14/15. Every item whose rule exists only on an ACM page is therefore **BLOCKED**, even when the paper meets the card value of 2026-10-27; the measurement is given beside it.
- The six criteria of `manuscript/GOAL_MOI_2026-11-15.md` section 1.

**Statuses.** READY, NOT READY (fixable by us: what and where), BLOCKED (needs the investigator, or a page only a person can open), SCHEDULED (known pending work, not a defect).

**Sequencing rule for every NOT READY fix below.** The freeze transfer `c_attr_c2_transfer.py` (shell C2, 2026-11-16) needs `03`, `05`, `06`, `07` and the manifest equal to HEAD. Package v2 (ruling CC-408) applies after C2, and package v4 (ruling CC-413, which rewrites `paperC.bib`) applies after v2. So every fix that touches those files or the bibliography is made **after C2 → v2 → v4 and before the tex rebuild**.

---

## 1. Verdict

**Paper C is NOT READY for submission.**

- No item fails in a way that needs a new run or a test-set look.
- What remains is four kinds of work:
  1. the scheduled pipeline: C2, v2, v4, the cut plan, the rebuild;
  2. nine NOT READY fixes, all text, bibliography or tooling;
  3. investigator items: author block, ORCID, anonymity, the repository and DOI, the FAIR DOI, the conference relation;
  4. every venue rule, which stays BLOCKED until a person reads the ACM pages in a normal browser.

Item counts in section 3 (34 rows):

| status | rows |
|---|---|
| READY | 6 |
| NOT READY | 9 |
| BLOCKED | 15 |
| SCHEDULED | 4 |

Several rows also carry a SCHEDULED part; the table counts each row once, by its first status.

---

## 2. The six criteria (GOAL_MOI section 1)

| # | criterion | status | basis |
|---|---|---|---|
| 1 | Scientifically complete | NOT READY + SCHEDULED | **Present:** every registered verdict, FAILs included (abstract: XM3600 FAIL, NoCaps FAIL). The English arm is complete (Section 8), not a placeholder. The instruments of the two companion studies are defined in the supplement "usable without the companion manuscripts" (`11_supplement` l.784–790). **Open:** the freeze update (C2) and the cut plan v1.1 are SCHEDULED. The reference for the Open Images V7 human-verified labels is not covered by any package (item 20). |
| 2 | Numbers and citations evidenced | NOT READY + BLOCKED | All 67 citation keys resolve. The numbers match the manifest after normalisation, except four unkeyed values. Findings: the repo's checker points at the wrong manifest; manifest pointers are stale; three bibliography entries are outdated; the FAIR entry prints a placeholder (BLOCKED). Items 13–18. |
| 3 | Code, tables, figures, appendices checked | NOT READY (minor) + SCHEDULED | The acmart build compiles from HEAD with 0 undefined citations or references. The one figure is vector with a `\Description`. Open: 3 overfull boxes, one font substitution, no supplement `readme.txt` (items 8, 23). The rebuild is SCHEDULED. |
| 4 | No contradictions | SCHEDULED | Checks run: each abstract triple (+4.49 [3.52, 5.57], +0.70 [−0.45, 1.97], +3.08 [2.08, 4.03], +1.73 [0.94, 2.50], +28.77, +37.87, +30.77) appears identically in the results section and the conclusion; the manifest's printed values agree with its raw values (item 15). No contradiction found. **Known:** "ends every step" in Section 5 becomes "ended" through C2 (`C2B_OLD/C2B_NEW`, `c_attr_c2_transfer.py` l.48–49); the abstract lacks InternVL3's COCO row, which the conclusion carries (C-V01). Re-check after the packages. This audit is not a full read. |
| 5 | Meets the venue's requirements | BLOCKED + NOT READY | No ACM page was readable (VENUE_RECHECK §3, C1–C20). The card values are met where measured (items 1–8). The NOT READY venue items are 9 (bibliography), 12 (project label) and 23 (readme). |
| 6 | Whole text reviewed | SCHEDULED | A whole-text read now would be stale: C2, v2 (12 blocks and the renumbering of Tables 10–18), v4 (15 blocks and Annex B), the cut plan (about −5,050 words) and the rebuild all still change the text. The last full-scope reads were on earlier states: the section-by-section review (`9b8e6ae`) and the related-work full-text check (`55315ca`). The whole-text read runs on the rebuilt PDF. |

---

## 3. Item by item

### 3a. Venue checklist (TALLIP card, last read 2026-10-27; ACM pages unread today)

| # | item | measured | status | what is needed |
|---|---|---|---|---|
| 1 | Title 6–12 words, no symbols or formulas | "Retrieved or Random Examples? Preregistered In-Context Captioning in Vietnamese and English": **11 words**; only a question mark | BLOCKED (meets card) | A person confirms C4 on the author-guidelines page. |
| 2 | Abstract 150–200 words; no first person, no "This paper", no citations, no planned work, no display maths | **193 words** now (whitespace count, comments removed). None of the excluded forms; it ends "The focus is empirical and practical". The C-V01 NEW abstract counts **198**. | BLOCKED (meets card); SCHEDULED C-V01 | Confirm C5. After C-V01 only 2 words remain. Any clause added at the rewrite (CC-405 C-N10, the deletion-step clause) needs equal cuts. |
| 3 | CCS 2012 concepts, keywords, ACM reference block | Two concepts: 10010147.10010178.10010179.10010182 "Natural language generation" (500) and 10010147.10010178.10010224.10010225 "Computer vision tasks" (300). Seven keywords. The ACM Reference Format block renders. | BLOCKED (meets card) | Confirm C6. The reference block shows the author placeholder (item 14). |
| 4 | Author-year citations in brackets; alphabetical list | Renders as [Pham et al. 2024], [Bui et al. 2023, 2026], and "Rebelo et al. [2025]" in running text. Uses `\citestyle{acmauthoryear}` and `ACM-Reference-Format`. | BLOCKED (meets card) | Confirm C9. |
| 5 | Statistics: statistic, df, value, p | The registered rules read paired-bootstrap 95% CIs. A Holm-stepped p̃ is printed only for the attribution study's DETECTED rule. No F/t statistic with df. | BLOCKED; SCHEDULED C-V04 | Confirm C10. C-V04 (Section 5.4: why interval rules and not p-values) is scheduled. Per answer F3, a printed p-value is added only if the guidelines or the editor require it, and only with the investigator's agreement. |
| 6 | Figures ≥ 600 dpi, legible at 12.7 cm, described | One figure (`fig1_ret_minus_rand`): vector PDF from SVG, no raster image (`pdfimages`: none), fonts embedded. Type is about 6.9 pt at 12.7 cm (13 px in a 680 px SVG). The build adds `\Description`. | BLOCKED (meets card) | Confirm C11. Resolution does not apply to a vector figure. |
| 7 | `acmart` manuscript source; TAPS packages | `\documentclass[manuscript,screen]{acmart}`, LuaLaTeX. Extra packages: longtable, booktabs, array, calc, newunicodechar. `\footnotetextcopyrightpermission` is emptied. Compiles; 0 undefined citations or references. | BLOCKED | Confirm C8 and the TAPS accepted-package list (on acm.org, unread). Production may require pdfLaTeX and listed packages only. |
| 8 | Layout warnings | 3 overfull boxes in the main build: 2.1 pt, 1.2 pt and **15.9 pt** (Table 1, the OpenFlamingo cell). Font substitution "inconsolata/m/it undefined" (main and supplement). | NOT READY (cosmetic) | At the rebuild: break or shorten the Table 1 cell at `body.tex` l.419 (source: the Table 1 rows in `02_related_work.md`, after v4, which adds rows to Table 1). Use upright code font or a font with italics. |
| 9 | Article type and length | Scratch `acmsmall` build: **69 pages** (body to p. 64, references pp. 65–69); supplement 44. Manuscript build: 66 + 35. Running text 01–10: 31,432 words. | BLOCKED (meets card minimum of Long ≥ 13 pp); SCHEDULED cut plan v1.1 | Confirm C2; the card has no maximum. The cut plan takes Sections 5.7 and 6.10 from 6,583 to about 1,530 words, which still leaves about 26,400 words. Whether that length suits TALLIP is the investigator's call at the rewrite. |
| 10 | Supplementary material with a short `readme.txt` | No `readme.txt` exists in the repo. | NOT READY (see item 23) | — |
| 11 | ORCID of the submitting author | None. The author block reads "[AUTHOR TO PROVIDE: authors, affiliations, ORCID]". | BLOCKED | Investigator: confirm C14 and supply the ORCID iDs. |
| 12 | Anonymity setting | Not known (card: NOT FOUND). The draft has an anonymous author block. Self-references are in the third person (`@Nguyen2026FAIR`; "A companion study by the same group … in preparation"). | BLOCKED | Read the ScholarOne form (C7). If double-anonymous, the phrase "by the same group" (`01_introduction.md` l.3) identifies the group and is reworded. |
| 13 | Declarations, AI wording | No AI-use statement: the investigator's decision, **not a defect**. No sentence anywhere says that no AI tool was used (searched in the main and supplement Markdown and the rendered text; 0 hits). No funding or competing-interest statement. | READY (AI wording); BLOCKED (funding, competing interests, CRediT, ethics: C15 unread) | Investigator: once C15 is read, decide whether funding and competing-interest lines are needed. ScholarOne may collect them. |
| 14 | Author block and reference block | Placeholders print on p. 1 and in every running head. | BLOCKED | Investigator supplies names, affiliations, ORCID; or confirms the anonymous form (item 12). |
| 15 | Relation to the conference version | Paper C has **no sentence** on the TAIMMA 2027 conference version, which the investigator submits first. | BLOCKED | See section 5. |

### 3b. Evidence and internal checks

| # | item | measured | status | what is needed |
|---|---|---|---|---|
| 16 | Repo's own number checker, as shipped | `scripts/paperC/c_pass2_check.py` (sha256 prefix `a257bd14891403a1`), run unmodified and read-only on `00`–`11`. It **hard-codes the archive copy** `manuscript/journal_draft_C/number_manifest_C.tsv` (3,775 rows, sha256 prefix `f452d162`), not the paper repo's manifest (5,667 rows): **581 tokens flagged**. | NOT READY (tooling) | In the paper repo, point `MAN` at `paper_v1_analysis/number_manifest_C.tsv`. Normalise U+2212, "+" and "," on the manifest side too: the shipped code normalises only the text side, so 256 manifest rows printed with "−" give false positives. Independent of C2; the fix goes in a tooling commit. |
| 17 | Numbers against the repo manifest | A scratch copy of the checker with `MAN` pointed at the repo manifest, run raw, flags 191 tokens. With both sides normalised and section/table references dropped, **37 residual tokens** remain. 33 are not quantities: dates and times, years (2021, 2022, 2026), section numbers, sha prefixes and comment text. **Four unkeyed quantities:** α = **0.025** (Holm, `05` l.145, `06`); Holm threshold **0.0125** = 0.025/2 (`06` l.178); mutant counts **22** of 22 and **33** of 33 (`07_disclosures.md` l.56; 73 of 73 is keyed). | NOT READY | After C2 → v2 → v4: add manifest rows: 0.025 as `prereg-quoted` (C-ATTR-DEV registration), 0.0125 as derived, 22 and 33 as `log` with their mutant-run records. |
| 18 | Manifest internal consistency | Of 5,667 rows, 5,133 have numeric printed and raw values; the printed value equals the raw value rounded for 5,132. One difference: `12.47` against raw `12.475` (`decide_coco_test.json::…per_model.internvl3`, `c-en-reported`). Binary 12.475 lies just below the half, so `f"{x:.2f}"` gives 12.47. Formatting artefact, not blocking. The decide file was not opened. | READY | — |
| 19 | Manifest `used_in` pointers (auxiliary check) | **323** row-file pairs name a file that no longer contains the number. Examples: 25 for `00_abstract.md` (the P1b and P2 per-backbone triples that left the abstract), 186 for `06_results.md`. Five `used_in` fields join a file name and a tag with "&#124;", e.g. `08_english_comparison.md&#124;c-pass2`. | NOT READY | After C2 → v2 → v4: refresh the `used_in` column from the final text and split the "&#124;tag" fields. The printed numbers are unaffected. |
| 20 | Reference for the Open Images V7 human-verified labels | `02_related_work.md` l.24 cites `@Kuznetsova2020OpenImages` (the Open Images **V4** paper) for the "V7 human-verified labels". `03_method.md` l.80 and `04_data_and_splits.md` l.32 use the labels with no citation. CC-405 N5 asked for a verified reference; package v2 §6 defers it (needs the network). No package covers it. | NOT READY | Find the source that documents the V7 human-verified image-level labels. Cite it at 02 l.24, 03 l.80 and 04 l.32, with a bib entry and an audit row. After C2 → v2 → v4. |
| 21 | Citation keys and bib entries | 67 keys cited, 67 entries, 0 unresolved, 0 uncited. Every entry has its required fields. Only `Nguyen2026FAIR` lacks a DOI or URL. | READY (keys) | — |
| 22 | Bib entries against Crossref today (08:4xZ) | (a) `Hussain2026SciRepLVLM`: the note "volume and article number not yet assigned (Crossref, 2026-10-30)" is stale. Crossref now gives *Scientific Reports* **16**, article **36452**. (b) `Yang2023ReViLM` is `@misc` with note "Findings of EMNLP 2023 (per the arXiv record)"; the published version is Findings of EMNLP 2023, doi `10.18653/v1/2023.findings-emnlp.793`. (c) `Oduwole2025AfriCaption` is `@misc`, arXiv only; the published version is Proc. 7th AfricaNLP Workshop (2026), doi `10.18653/v1/2026.africanlp-main.5`. None of the three keys appears in packages v2 or v4. | NOT READY | After v4 (it rewrites `paperC.bib`): update the three entries and their rows in `paperC_bib_audit.tsv`. The card asks for published versions where they exist. A text year changes for (c) if the key year is printed (2025 → 2026); check the citations. |
| 23 | Supplement `readme.txt` | Missing (card: supplementary material with a short readme.txt). | NOT READY | At packaging, write a short `readme.txt` listing the supplement PDF and what it holds. |
| 24 | `Nguyen2026FAIR` entry | Prints "[AUTHOR TO PROVIDE: pages and DOI once listed on IEEE Xplore]" in the reference list (p. 65 of the build). | BLOCKED | Investigator: pages and DOI when listed. If not listed by submission, drop the bracket and keep the ISBN. |
| 25 | `Vu2025VELVET` name order | The audit row says "author order deliberately set to Vietnamese family-first … PI to confirm". | BLOCKED (low) | Recommendation: follow the published record (Crossref deposits family = Anh), unless the investigator knows the author's own form. Default if no answer: the Crossref form. |
| 26 | Data and code availability | The statement is present (`10_conclusion.md` l.20–25). It ends with a printed bracket: "[Repository link and archive DOI to be added after review; an anonymised copy of the registrations, code and decision files can be provided to the editor.]" | BLOCKED | Investigator: the repository and archive (DOI), and answer C5 (i) on the release of per-image scores (the dataset-terms check; v2 §6 deferred). Then the bracket becomes a plain sentence. If the repository waits until after review, keep the sentence without brackets. |
| 27 | Internal ids, tool names, hosts in printed text | Rendered main text: no CC-, PI-, OPS- or CP- ids; no agent or tool name; no host, IP or path. HTML comments carrying ids (e.g. `10_conclusion.md` l.25) are dropped by pandoc and do not print. The supplement prints `decide_coco_test.json`, `decide_nocaps_val.json` and 12-hex sha prefixes as provenance; acceptable. **One project label prints:** "C-ATTR-DEV", 8 times in the main text and 6 in the supplement, in captions and stamps such as "DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY". Box 1 defines it. | NOT READY | After C2 → v2 → v4: replace it with a reader-facing name, e.g. "the attribution-study registration". Places: Box 1 and §5.7 (`05` l.27, 134, 136), `06` table captions (l.126, 148, 161, 198, 231), `11` l.978–1109. Same treatment as A's internal terms in S11. Prompt tails T1/T2 and claim names (P1, S-NC, E3a–c) are defined paper terms and stay. |
| 28 | Registered verdicts verbatim, FAILs included | The abstract and conclusion print PASS and FAIL as registered (P1 PASS, XM3600 FAIL, P1-EN PASS, NoCaps S-NC FAIL, E3a–c PASS). | READY | — |
| 29 | Placeholder sections | None. Section 8 (English arm) is complete. | READY | — |
| 30 | Companion studies "in preparation" | Two instruments come from companion manuscripts (the scoring kit; count-matched precision). The supplement defines both for use without them. | READY | Optional at the rewrite: add a pointer to the supplement definitions at `01_introduction.md` l.16. |

### 3c. Scheduled work (listed, not counted as defects)

| # | item | state |
|---|---|---|
| 31 | Freeze update, shell C2 (2026-11-16, from 12:00 Vietnam time) | Not run. It changes 03, 05, 06, 07 and appends two manifest rows; it includes "ends" → "ended" (item 4 of section 2). |
| 32 | Fix package v2 (CC-408, conditional GO) | 12 blocks, the renumbering of Tables 10–18 (C-R01) and the manifest operation C-M01. The renumbering pattern `TABLE_REF` (`apply_c_v2.py` l.73) handles "Tables 7, 8 and 11" in the Figure 1 caption (`08` l.65). |
| 33 | Fix package v4 (CC-413, conditional GO 88) | 15 blocks plus Annex B. Applies after the CC-408 commit. Rewrites `02`, the evidence file, `paperC.bib` (four new entries), the audit table and the supplement. |
| 34 | Cut plan v1.1; tex rebuild | The plan takes Sections 5.7 and 6.10 to about 1,530 words. The rebuild follows all packages, then the whole-text read (criterion 6). |

---

## 4. NOT READY list (fixable by us)

1. **Item 8.** Table 1 overfull box of 15.9 pt, plus the inconsolata-italic substitution. Fix at the rebuild, after v4.
2. **Item 16.** `scripts/paperC/c_pass2_check.py` reads the archive manifest and does not normalise "−" and "+" on the manifest side. Fix in a tooling commit in the paper repo.
3. **Item 17.** Four unkeyed quantities: 0.025, 0.0125 (`05`, `06`) and the mutant counts 22 and 33 (`07` l.56). Add manifest rows after C2 → v2 → v4.
4. **Item 19.** 323 stale `used_in` pointers and five fields joined with "&#124;tag". Refresh the manifest after C2 → v2 → v4.
5. **Item 20.** No verified reference for the Open Images V7 human-verified labels (02 l.24, 03 l.80, 04 l.32; CC-405 N5, deferred and in no package).
6. **Item 22a.** `Hussain2026SciRepLVLM`: set volume 16, article 36452, and drop the stale note. After v4.
7. **Item 22b.** `Yang2023ReViLM`: change to `@inproceedings` Findings of EMNLP 2023 with doi `10.18653/v1/2023.findings-emnlp.793`. After v4.
8. **Item 22c.** `Oduwole2025AfriCaption`: change to AfricaNLP 2026 with doi `10.18653/v1/2026.africanlp-main.5`. After v4.
9. **Item 23.** No supplement `readme.txt`. Write it at packaging.
10. **Item 27.** The project label "C-ATTR-DEV" prints 14 times. Rename in 05, 06 and 11 after C2 → v2 → v4.

Items 22a–c are one table row (item 22), and item 10 is the same finding as item 23, so this list has ten entries for the nine NOT READY rows.

---

## 5. BLOCKED list (needs the investigator or a person's browser)

**All venue rules (C1–C20).** Every ACM host refused automated reading on 2026-11-14/15. A person must open these pages in a normal browser and update the card:
- https://dl.acm.org/journal/tallip/author-guidelines (title, abstract, CCS, citation style, statistics, figures, type and length, extension rule);
- https://www.acm.org/publications/authors/submissions and the TAPS accepted-package list;
- https://dl.acm.org/journal/tallip/about;
- https://www.acm.org/publications/policies/new-acm-policy-on-authorship;
- https://dl.acm.org/journal/tallip/open-access.

**Relation to the conference version (item 15).**
- *Pages to read:*
  - the ACM Policy on Prior Publication and Simultaneous Submissions (https://www.acm.org/publications/policies/prior-publication-policy, C17). It has never been read on the ACM page in this project.
  - the TALLIP extension clause (C3; the card says ≥ 25% new content, last read 2026-10-27).
- *Already read (VENUE_RECHECK D27, Springer licence form, Singapore):* if TAIMMA accepts the paper, a journal version needs:
  - at least 30% new material;
  - an express statement of the incremental change;
  - acknowledgement of first publication: "First published in [Volume, page number, year] by Springer Nature", plus a citation.
- *Text to add:* paper C has none of this. It becomes required text (introduction or a footnote on p. 1, and the cover letter) once TAIMMA accepts. TAIMMA notifications come by 25 Dec 2026 at the latest.
- *Simultaneous submission:* if paper C goes to TALLIP while the conference paper is still under review, read the ACM policy on that point first. Springer's code (D25) also asks authors to inform the publisher of related manuscripts under consideration elsewhere.
- *Recommendation:* submit C to TALLIP only after the TAIMMA decision, and state the overlap and the new share (the attribution study, Flickr30K, the full supplement) in the paper and the cover letter.

**Author block, ORCID, anonymity (items 11, 12, 14).**
- Names, affiliations and ORCID iDs are needed.
- The anonymity mode is read from the ScholarOne form.

**Funding, competing interests, CRediT, ethics (item 13).** Decide once C15 is read. The decision of no AI statement stands, and no text says that no AI tool was used.

**Statistics format (item 5).** Whether a printed test statistic or p-value is required (C10). By answer F3 the investigator agrees before any p-value is added. C-V04 is scheduled meanwhile.

**Data and code availability (item 26).** Repository and archive DOI; the C5 (i) release decision after the dataset-terms check.

**`Nguyen2026FAIR` pages and DOI (item 24).** Awaiting the IEEE Xplore listing.

**`Vu2025VELVET` name order (item 25).** Low priority; the default is the Crossref form.

---

## 6. How the checks were run (reproducible, read-only)

- **Shipped checker.** `python3 -I scripts/paperC/c_pass2_check.py 00…11.md`, run in `paper_v1_analysis/`, flagged 581 tokens.
- **Scratch variants of the checker** (in this session's scratchpad):
  - (a) the same code with `MAN` pointed at the repo manifest: 191 tokens;
  - (b) normalised on both sides, with section and table references dropped: 37 tokens; each token was read in context.
- **Manifest consistency.** Printed value against raw value, using Decimal rounding half-up and half-even: 5,133 numeric pairs, 1 float artefact. Reverse `used_in` scan: 323 stale pairs.
- **Bibliography.**
  - A key scan of `[@…]` in 01–11 (HTML comments removed) against `paperC.bib`.
  - Field presence per entry type.
  - Crossref API, generic client name, no personal data: the DOI of the Hussain entry, and title searches for Re-ViLM, AfriCaption, the remote-sensing captioning paper (Rebelo), KTVIC and GRIP. Only Re-ViLM and AfriCaption have a published version on Crossref.
- **Builds.** `tex/build.sh` copied with its preamble and Lua filter to the scratchpad and run there against the HEAD Markdown; it reads the paper dir and writes only in its own dir.
  - `[manuscript,screen]`: 66 + 35 pages, byte-equal to the worktree `tex/` files.
  - `[acmsmall,screen]`: 69 + 44 pages.
  - Logs were scanned for undefined citations and references, overfull boxes, and errors.
  - `git status` of the paper repo was unchanged afterwards.
- **Rendered-text scans** (`pdftotext`) of main and supplement:
  - project ids (CC-, PI-, OPS-, CP-, INC-), agent and tool names, hosts, paths, IPv4 addresses, bare "PI", file names, hex strings;
  - placeholder wording ("AUTHOR TO PROVIDE", "to be added", "pending", "in preparation", "freeze");
  - any no-AI phrasing.
- **Figure.** `pdfimages -list` (no raster), `pdffonts` (embedded), SVG font sizes.
- **Forward checks on scheduled work.**
  - The C-V01 NEW abstract counts 198 words.
  - The C2 script replaces the freeze sentence (`C2B_OLD`/`C2B_NEW`).
  - v2 and v4 do not touch the three bib keys of item 22.
  - The v2 renumbering pattern covers "Tables 7, 8 and 11".

**Not done, by custody rule.** No file under `~/vsps_labels*` or `~/.vsps_sealed`, no `key.json`, no `gt_cache.json`, no test-set score book, no decide or result JSON was opened. Manifest raw values were therefore not re-resolved against their source files. `c_pass2_manifest.py` (appends to the manifest by default), `c_pass2_supp.py` and `build_c_draft.py` were not run.
