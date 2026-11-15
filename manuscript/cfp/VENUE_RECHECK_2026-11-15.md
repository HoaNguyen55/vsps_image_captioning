# Venue requirements: live-page recheck, 2026-11-15

All pages were read on **2026-11-14 between 21:38 and 21:51 UTC** (= 2026-11-15, 04:38–04:51 Vietnam time). The "Read (UTC)" column gives the time on 2026-11-14.
Public pages only. No login, no form, no message to any person. No file other than this one was written or changed.

**How the pages were read**

- Plain fetch (`curl`) first. Where the plain fetch got a bot wall, one clean headless browser session (no profile, no sign-in) was tried, and one attempt with the standard fetch tool.
- No bot check was worked around. A host that showed a challenge or a block page to these tools is recorded as COULD NOT READ. The user's signed-in Chrome (the route of the 2026-11-10 AI-policy check) was **not** used.
- Quotes are copied from the saved page text. Nothing is filled from memory or from an earlier reading.

**Status words**

- CONFIRMED: read today on an official page and it matches the card.
- CHANGED: read today and it differs from the card, or it is a requirement on the live page that the card does not carry ("addition").
- NOT FOUND ON THE LIVE PAGE: the official page was read and does not state it.
- COULD NOT READ: the official page could not be opened today.
- "Publisher-wide" means the sentence is on a publisher page that covers all its journals, not on the journal's own guide.

**What could not be opened (stated once, plainly)**

| Host | Pages tried | What came back |
|---|---|---|
| sciencedirect.com (Elsevier journal pages) | SPIC guide for authors; open-access options; insights; `journalinsights.elsevier.com/journals/0923-5965` (redirects there) | Plain fetch: HTTP 403. Headless browser: "There was a problem providing the content you requested" (code CPE00001). Fetch tool: HTTP 403. Insights: "Are you a robot? Please confirm you are a human by completing the captcha challenge". |
| dl.acm.org | TALLIP author guidelines; about; open access; journal home | Plain fetch: HTTP 403 ("Just a moment..."). Headless browser: "Performing security verification ... verifies you are not a bot". Fetch tool: HTTP 403. |
| acm.org and its sub-hosts | Prior-publication policy; authorship policy; submissions; open access; `authors.acm.org`; `tallip.acm.org`; `libraries.acm.org` | Plain fetch: HTTP 403. Headless browser: "Sorry, you have been blocked". Fetch tool: HTTP 403. |
| mc.manuscriptcentral.com/tallip | TALLIP submission site front page | HTTP 403 ("Just a moment..."). |

The ScienceDirect open-access-options and insights pages, and the ACM authorship, submissions, TALLIP about and TALLIP open-access pages, were tried with the fetch tool only (about 21:48 UTC, HTTP 403 each).

Result: **no ACM page and no SPIC journal page was read today.** Every TALLIP fact, and every SPIC fact that lives only in the journal's guide, stays as last read (2026-10-27; AI rules 2026-11-10).
Also not opened today: the conference's Google Drive files (call brochure, first page of the Springer letter; their link IDs on the site are unchanged), the Microsoft CMT page (it needs a login), SCImago (third party).

---

## 1. Signal Processing: Image Communication (Elsevier) — Paper A

Card: `.claude/skills/venue-spic/SKILL.md`. The journal's guide for authors was **not readable** today. Rows marked "publisher-wide" were read on elsevier.com pages.

| # | Fact | Card says | Live page says today | Status | URL | Read (UTC) |
|---|---|---|---|---|---|---|
| A1 | Quartile | SJR 2025: Q2 | Publisher pages carry no quartile. Elsevier catalogue page: "Impact factor: 2.1", "5 Year impact factor: 2.9". SCImago not opened (third party). | NOT FOUND ON THE LIVE PAGE | https://shop.elsevier.com/journals/signal-processing-image-communication/0923-5965 | 21:47 |
| A2 | Scope | Includes "Multimedia quality assessment and measures" and "content-based media indexing and retrieval, semantics" | Catalogue page lists "Multimedia quality assessment and measures, models for QoS and QoE" and "Multi-camera video analysis, motion analysis, content-based media indexing and retrieval, semantics, face and gesture processing". Also: "A publication of the European Association for Signal Processing (EURASIP)". | CONFIRMED (Elsevier catalogue page) | same | 21:47 |
| A3 | Article types | "original research work, tutorial and review articles, and accounts of practical developments, including standards related technical work" | "The journal features original research work, tutorial and review articles, and accounts of practical developments." The words "including standards related technical work" are not on the catalogue page. | CONFIRMED (catalogue page, first part only) | same | 21:47 |
| A4 | Length limit | No limit found | — | COULD NOT READ | https://www.sciencedirect.com/journal/signal-processing-image-communication/publish/guide-for-authors | 21:39 |
| A5 | Abstract | ≤ 250 words | — | COULD NOT READ | same | 21:39 |
| A6 | Keywords | 1–7 | — | COULD NOT READ | same | 21:39 |
| A7 | Highlights required by SPIC; graphical abstract encouraged | Required; graphical abstract encouraged | — | COULD NOT READ | same | 21:39 |
| A8 | Highlights format | 3–5 bullets, each ≤ 85 characters with spaces | Publisher-wide: "Highlights are three to five ... bullet points"; "Each Highlight can be no more than 85 characters, including spaces". | CONFIRMED (publisher-wide) | https://www.elsevier.com/researcher/author/tools-and-resources/highlights | 21:47 |
| A9 | When highlights are due, and their file form | "Required" (no stage given) | Publisher-wide: "Not part of editorial consideration and not required until the final files stage"; "Must be provided as a Word document". The journal's guide may say otherwise; it was not read. | CHANGED (addition, publisher-wide) | same | 21:47 |
| A10 | Review model | Single anonymized; at least 2 reviewers | — | COULD NOT READ | SPIC guide (as A4) | 21:39 |
| A11 | Title page content; cover letter | Not recorded | — | COULD NOT READ | SPIC guide (as A4) | 21:39 |
| A12 | LaTeX template exists (CAS, single and double column) | Elsevier CAS LaTeX (`els-cas-templates.zip`) or Word | Publisher-wide: the `elsarticle` package, and "Two additional class files and templates are available for single and double column" (the link is `els-cas-templates.zip`). "Most journals accept a PDF of your manuscript at initial submission." | CONFIRMED (publisher-wide) | https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions | 21:47 |
| A13 | Word is single-column; only LaTeX may be double-column | As stated | — | COULD NOT READ | SPIC guide (as A4) | 21:39 |
| A14 | Reference style | Numbered, square brackets, order of appearance; journal names abbreviated | Publisher-wide page only says: "Some journals require a specific reference style. Please check the Guide for Authors". | COULD NOT READ | SPIC guide (as A4) | 21:39 |
| A15 | Figure resolution | Photos ≥ 300 dpi; bitmap line art ≥ 1000 dpi; each figure a separate file; captions | Publisher-wide: line art "minimum resolution of 1000 dpi (or 1200 dpi if the image contains very fine line weights)"; grayscale and RGB images "minimum resolution of 300 dpi"; combination art "Resolution 500 dpi"; "All illustrations are provided as separate files (unless the journal's guide for authors prescribes otherwise)". | CONFIRMED (publisher-wide) | https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-types and `/artwork-formats-checklist` | 21:50, 21:49 |
| A16 | PNG accepted for photos | TIFF/JPG/PNG | Publisher-wide checklist: "My files are in the correct format: EPS, PDF, TIFF or JPEG, or Microsoft Office files (Word, PowerPoint, Excel)". PNG is not named. | NOT FOUND ON THE LIVE PAGE | `/artwork-formats-checklist` (as A15) | 21:49 |
| A17 | Supplementary material rule | Not recorded | — | COULD NOT READ | SPIC guide (as A4) | 21:39 |
| A18 | Meaning of research-data "Option C" | Deposit and cite or link, or explain why not; statement at submission | Publisher-wide: "Option C ... You are required to: Deposit your research data in a relevant data repository; Provide a link to the dataset during the submission process; If sharing your research data isn't possible, make a statement explaining why during the submission process. The statement will appear in your published article". | CONFIRMED (publisher-wide) | https://www.elsevier.com/researcher/author/tools-and-resources/research-data/data-guidelines | 21:49 |
| A19 | SPIC follows Option C | As stated | "We recommend you read your chosen journal's guide for authors for details about which option the journal supports." | COULD NOT READ | SPIC guide (as A4) | 21:39 |
| A20 | Competing interests through the declarations tool; funding statement | As stated (funding not recorded) | — | COULD NOT READ | SPIC guide (as A4) | 21:39 |
| A21 | CRediT statement required | Required | Publisher-wide wording only: "CRediT statements should be provided during the submission process and will appear above the acknowledgment section of the published paper". Whether SPIC makes it mandatory was not read. | COULD NOT READ | SPIC guide (as A4); https://www.elsevier.com/researcher/author/policies-and-guidelines/credit-author-statement | 21:39, 21:47 |
| A22 | Ethics and consent for human annotators | Not recorded | — | COULD NOT READ | SPIC guide (as A4) | 21:39 |
| A23 | AI used in writing: declaration, place, wording | New section before the reference list; names tool, purpose, oversight | "Authors should disclose the use of AI tools for manuscript preparation in a separate AI declaration statement included in their manuscript upon submission. This statement will appear in the published article." "you must include a separate declaration section at the end of your manuscript, immediately before the references". Recommended title and statement: see "Consequences". Translation: "you should disclose the use of AI tools for translations". "Policy updated June 2026." | CONFIRMED (publisher policy) | https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals | 21:38 |
| A24 | Grammar and spelling tools exempt | Exempt | "Basic checks of grammar, spelling and punctuation do not need a declaration statement. However, when an AI tool makes substantive changes to sentence structure or organization of a part of the text, this should be disclosed." Also exempt: "basic reference manager functions". | CONFIRMED (publisher policy) | same | 21:38 |
| A25 | AI in the research process, including AI-written code | Described in Methods | "Where AI tools are used as part of the research process rather than manuscript preparation, this use should be described in detail in the Methods section." "If authors write or edit code using AI tools as part of their research, they should declare this in detail in the Methods section". Code formatting only: "should be reported in the AI declaration". | CONFIRMED (publisher policy) | same | 21:38 |
| A26 | AI used on references | Declared in the manuscript | "If these or any other AI tool are used to select, collate, generate or edit references, this should be declared in the manuscript." "Inclusion of fabricated references may lead to rejection of a manuscript." | CONFIRMED (publisher policy) | same | 21:38 |
| A27 | AI is not an author; images | Not an author; images only as disclosed explanatory images or data plots | "Authors should not list AI tools as an author or co-author". Explanatory images: disclosed "in the caption of each image ... and in the general AI disclosure statement". Data plots "only when the visual output is directly derived from underlying data". Also: "General-purpose generative AI image tools must not be used to create graphical abstracts." | CONFIRMED (publisher policy) | same | 21:38 |
| A28 | AI section inside the SPIC guide | Same title, read 2026-11-10 | — | COULD NOT READ | SPIC guide (as A4) | 21:39 |
| A29 | Prior publication (publisher ethics page) | (from the 2026-11-13 conference note) no submission of a paper "published previously, except in the form of an abstract or as part of a published lecture or academic thesis or as an electronic preprint" | "In general, an author should not submit for consideration in another journal a paper that has been published previously, except in the form of an abstract or as part of a published lecture or academic thesis or as an electronic preprint." "Submitting the same manuscript to more than one journal concurrently constitutes unethical behaviour". | CONFIRMED (publisher-wide) | https://www.elsevier.com/about/policies-and-standards/publishing-ethics | 21:47 |
| A30 | Extending a conference paper (how much new, how disclosed) | Not recorded | The publisher ethics page has no rule for conference papers. The journal's own "submission declaration" was not read. | NOT FOUND ON THE LIVE PAGE | same | 21:47 |
| A31 | Preprint | Allowed | Publisher-wide: "Authors can share their preprint anywhere at any time". But: "Some society-owned titles and journals that operate double-anonymized peer review have different preprint policies — please check the journals' Guide for Authors". SPIC is a EURASIP publication (A2), and its guide was not read. | CONFIRMED (publisher-wide) | https://www.elsevier.com/about/policies-and-standards/sharing | 21:49 |
| A32 | Free SSRN preprint service | Optional | Not on the pages read. | NOT FOUND ON THE LIVE PAGE | same | 21:49 |
| A33 | Open-access charge | USD 2,830 | Elsevier APC price list ("Prices as of date: 05-Oct-2026"): "0923-5965, Signal Processing: Image Communication, Hybrid Open Access, USD 2830, EUR 2580, GBP 2270, JPY 368560". | CONFIRMED | https://legacyfileshare.elsevier.com/els_com_pricing/article-publishing-charge.xlsx (linked from https://www.elsevier.com/about/policies-and-standards/pricing) | 21:48 |
| A34 | Subscription (no-fee) route | Hybrid; subscription route has no fee | Price list: "Hybrid Open Access". Pricing page: "Authors publishing in hybrid journals can publish under the subscription model at no cost". "Our waiving policy does not apply to hybrid journals." | CONFIRMED | https://www.elsevier.com/about/policies-and-standards/pricing | 21:47 |
| A35 | Embargo | 24 months | Elsevier list "Journal Specific Embargo Periods 2025": "0923-5965, Signal Processing: Image Communication, 24". | CONFIRMED | Embargo list linked from https://www.elsevier.com/about/policies-and-standards/sharing | 21:49 |
| A36 | Turnaround and acceptance rate | 15 days to first decision; 198; 436; 8; acceptance 9% | — | COULD NOT READ | https://journalinsights.elsevier.com/journals/0923-5965 | 21:49 |

---

## 2. Language Resources and Evaluation (Springer) — Paper B

Card: `.claude/skills/venue-lre/SKILL.md`. The submission guidelines page was read in full (about 59,700 characters).

| # | Fact | Card says | Live page says today | Status | URL | Read (UTC) |
|---|---|---|---|---|---|---|
| B1 | Scope | Creation, annotation and use of language resources; evaluation, including benchmarking | "devoted to the acquisition, creation, annotation, and use of language resources, together with methods for evaluation of resources, technologies, and applications"; evaluation includes "benchmarking". | CONFIRMED | https://link.springer.com/journal/10579/aims-and-scope | 21:41 |
| B2 | Types and lengths | Full "typically 18-25 pages"; surveys the same; project notes 8–10; squibs 6–8; book reviews 1,000–3,000 words; no hard limit found | "Full-length submissions are typically 18-25 pages in length." "Survey articles follow the same format as full-length papers." "Project notes are typically 8-10 pages in length, but no minimum or maximum length is required." "Squibs are typically 6-8 pages". "Reviews are typically between 1,000 and 3,000 words." No hard limit is stated. | CONFIRMED | https://link.springer.com/journal/10579/submission-guidelines | 21:39 |
| B3 | Special Focus on less-resourced languages | Focus on the language's properties; no textbook re-description; comprehensive evaluation; resources public or reasons stated; flag in cover letter; weak English "returned without review" | All six points are on the page with the same wording ("The cover letter should clearly indicate that the submission is intended for the special focus section on Less-resourced Languages"; "will be returned without review"). | CONFIRMED | same | 21:39 |
| B4 | Special Focus: further conditions | Not in the card | "A literature review should be included, covering both previous work utilizing the same methods as well as previous work addressing the same problem but using different methods." "The work should involve state-of-the-art methods (e.g., transformers rather than statistical methods); if older methods are applied their use should be justified." "In general, the paper should not provide a comprehensive overview of the linguistic characteristics of the language." | CHANGED (addition) | same | 21:39 |
| B5 | Title limit | Not found | "The title should be concise and informative." No number. | NOT FOUND ON THE LIVE PAGE | same | 21:39 |
| B6 | Abstract | 150–250 words; no undefined abbreviations or unspecified references | "Please provide an abstract of 150 to 250 words. The abstract should not contain any undefined abbreviations or unspecified references." | CONFIRMED | same | 21:39 |
| B7 | Keywords | 4–6 | "Please provide 4 to 6 keywords". | CONFIRMED | same | 21:39 |
| B8 | Highlights | Not found | Not on the page. | NOT FOUND ON THE LIVE PAGE | same | 21:39 |
| B9 | Review model | Single-blind; at least 2 referees | "This journal follows a single-blind reviewing procedure." "at least two referees per manuscript". | CONFIRMED | same | 21:39 |
| B10 | Template and text format | Word (10 pt Times) or the Springer Nature LaTeX template; at most 3 heading levels; footnotes, not endnotes | "Manuscripts should be submitted in Word." "10-point Times Roman". "Manuscripts with mathematical content can also be submitted in LaTeX. We recommend using Springer Nature's LaTeX template." "no more than three levels". "Always use footnotes instead of endnotes." | CONFIRMED | same | 21:39 |
| B11 | Editable source files | Not in the card | "Please ensure you provide all relevant editable source files at every submission and revision. Failing to submit a complete set of editable source files will result in your article not being considered for review." | CHANGED (addition) | same | 21:39 |
| B12 | Citation and reference style | (Author, year); alphabetical list; APA 7 author-number rule; full DOI links | "Cite references in the text by name and year in parentheses." "alphabetized by the last names of the first author". "encouraged to follow official APA version 7 guidelines on the number of authors". "always include DOIs as full DOI links". | CONFIRMED | same | 21:39 |
| B13 | Statements and Declarations | Before the reference list: Funding, Competing interests, Ethics approval, Consent, Data/Material/Code availability, Authors' contributions; missing → "returned as incomplete"; acknowledgments on the title page | "submissions that do not include relevant declarations will be returned as incomplete". "placed in a 'Declarations' section before the reference list under a heading of 'Funding' and/or 'Competing interests'. Other declarations include Ethics approval, Consent, Data, Material and/or Code availability and Authors' contribution statements." "Acknowledgments ... should be placed in a separate section on the title page." | CONFIRMED | same | 21:39 |
| B14 | Declarations entered in the submission system | Not in the card | "Author Contribution information and Competing Interest information must be provided at submission via the submission interface. Only the information submitted via the interface will be used in the final published version." Funding "needs to be disclosed upon submission of the manuscript in the peer review system". Author contributions "should be listed at the separate title page". | CHANGED (addition) | same | 21:39 |
| B15 | Ethics and consent for human participants (raters, annotators) | "Ethics approval, Consent" listed | Authors are asked to include "study-specific approval by the appropriate ethics committee for research involving humans" and "informed consent if the research involved human participants". Data section: "Participant consent should be obtained and documented prior to data collection." A section "Compliance with Ethical Standards" lists "Research involving Human Participants and/or Animals" and "Informed consent" ("if applicable"). | CONFIRMED | same | 21:39 |
| B16 | AI use, journal page | LLM use documented in Methods; AI-assisted copy editing need not be declared; LLMs are not authors | "Large Language Models (LLMs), such as ChatGPT, do not currently satisfy our authorship criteria." "Use of an LLM should be properly documented in the Methods section (and if a Methods section is not available, in a suitable alternative part) of the manuscript. The use of an LLM (or other AI-tool) for 'AI assisted copy editing' purposes does not need to be declared." | CONFIRMED | same | 21:39 |
| B17 | AI use, publisher framework | All AI use described; "an AI Declaration in your manuscript"; place and wording not fixed; stricter layer applies | Journal-policies page: authors "Disclose AI use for trust and transparency"; polishing language with an LLM: "Permitted. Disclosure enhances trust and transparency". Manuscript page: grammar and language editing, translation, drafting from author input: "Clearly describe use and confirm author accountability". "provided in an AI Declaration in your manuscript". "Where AI use is not declared, editors may need to investigate or request clarification". No place, title or wording is fixed. | CONFIRMED | https://link.springer.com/brands/springer/journal-policies ; https://www.springernature.com/gp/policies/editorial-policies/ai-manuscript-preparation ; `/using-ai-in-research` | 21:41, 21:44 |
| B18 | AI field in the submission form; position of the AI Declaration | Not verified | Editor guidance: "authors and reviewers will also be asked to confirm that they have read and complied with the Springer Nature AI Editorial Policies when submitting a manuscript". The form itself needs a login and was not opened. No page fixes the position. | NOT FOUND ON THE LIVE PAGE | https://www.springernature.com/gp/policies/editorial-policies/ai-editor-guidance | 21:42 |
| B19 | AI-assisted figures | Disclosed in the caption or legend | "Specific disclosure should be provided within the caption or legend of the visual content." Visual content without verifiable sources "is considered opaque and is not permitted". | CONFIRMED | https://www.springernature.com/gp/policies/editorial-policies/ai-manuscript-preparation | 21:44 |
| B20 | Data availability statement | Required for original research | "authors must add a Data Availability Statement to original research articles"; "All original research must include a data availability statement." | CONFIRMED | submission guidelines (as B2) | 21:39 |
| B21 | Figures | EPS vector / TIFF; halftone ≥ 300, combination ≥ 600, line art ≥ 1200 dpi; bold "Fig. N", no final period; patterns plus colour; contrast ≥ 4.5:1 | "For vector graphics, the preferred format is EPS; for halftones, please use TIFF format." "minimum resolution of 1200 dpi" (line art); "300 dpi" (halftone); "600 dpi" (combination). "Figure captions begin with the term Fig. in bold type"; no punctuation at the end. "Patterns are used instead of or in addition to colors"; "contrast ratio of at least 4.5:1". | CONFIRMED | same | 21:39 |
| B22 | Figure size class for LRE (84/174 mm or 119 mm) | Not found | Both classes are printed ("large-sized journals ... 84 mm ... or 174 mm"; "small-sized journals ... 119 mm"). The page does not say which class LRE is. | NOT FOUND ON THE LIVE PAGE | same | 21:39 |
| B23 | Supplementary material | "Online Resource N"; files ESM_N; each file carries title, journal, authors, affiliation, corresponding e-mail | "Refer to the supplementary files as 'Online Resource'"; "Name the files consecutively, e.g. 'ESM_3.mpg'"; "include in each file the following information: article title, journal name, author names; affiliation and e-mail address of the corresponding author". Text files "in PDF format". | CONFIRMED | same | 21:39 |
| B24 | Cover letter | Per author: verified ORCID, university homepage or online CV, or a paragraph on experience; Special Focus flag; reused and unpublished material disclosed | "at least one of the following items for each contributing author": "a verified ORCID profile", "a link to the author's university homepage", "a link to an up-to-date online Curriculum Vitae"; "If none of these are available, add a paragraph". Corresponding author: "providing transparency on re-use of material and mention any unpublished material ... in a cover letter to the Editor". | CONFIRMED | same | 21:39 |
| B25 | Title page | Not itemised in the card | Title; author names; affiliations; "A clear indication and an active e-mail address of the corresponding author"; "If available, the 16-digit ORCID". | CHANGED (addition) | same | 21:39 |
| B26 | Prior publication; extending earlier work | (2026-11-13 note) original and unpublished "unless the new work concerns an expansion of previous work", with transparency on re-use | "The submitted work should be original and should not have been published elsewhere in any form or language (partially or in full), unless the new work concerns an expansion of previous work. (Please provide transparency on the re-use of material to avoid the concerns about text-recycling ('self-plagiarism')." "The manuscript should not be submitted to more than one journal for simultaneous consideration." | CONFIRMED | same | 21:39 |
| B27 | Share of new content needed for an extension; how the conference paper is cited | Not recorded | No percentage and no citation form are given. | NOT FOUND ON THE LIVE PAGE | same | 21:39 |
| B28 | Publishing model and charge | Hybrid; OA £2590 / USD 3590 / €2890 | "Language Resources and Evaluation is a hybrid journal." "The current APC ... is £2590.00 GBP / $3590.00 USD / €2890.00 EUR." | CONFIRMED | https://link.springer.com/journal/10579/how-to-publish-with-us | 21:41 |
| B29 | Subscription (no-fee) route | Hybrid (implied) | "Authors can also choose to publish under the subscription publishing model (no APC charges apply); both options will be offered after the paper has been accepted." | CONFIRMED | same | 21:41 |
| B30 | Time to first decision | Median 36 days | "Submission to first decision (median) 36 days". Also shown: "Journal Impact Factor 2.0 (2025)". | CONFIRMED | https://link.springer.com/journal/10579 | 21:41 |

Note, not a card fact: the publisher's journal-policies page says "Springer Nature journals encourage posting of preprints of primary research manuscripts", and "Authors should disclose details of preprint posting ... upon submission".

---

## 3. ACM TALLIP — Paper C

Card: `.claude/skills/venue-tallip/SKILL.md`. **Nothing could be read today.** Every ACM host returned a block to all three reading methods (see the table at the top). The card values below are therefore unverified today.

| # | Fact | Card says | Live page says today | Status | URL | Read (UTC) |
|---|---|---|---|---|---|---|
| C1 | Scope | Asian languages and low-resource languages of Africa, Australasia, Oceania and the Americas; reproducible techniques | — | COULD NOT READ | https://dl.acm.org/journal/tallip/about | about 21:48 (fetch tool, HTTP 403) |
| C2 | Article types and lengths | Long ≥ 13 journal pages; Survey; Short typically 6–12; Notes; Review Articles | — | COULD NOT READ | https://dl.acm.org/journal/tallip/author-guidelines | 21:39 |
| C3 | Conference extension | ≥ 25% new content | — | COULD NOT READ | same | 21:39 |
| C4 | Title | Typically 6–12 words; no symbols or formulas | — | COULD NOT READ | same | 21:39 |
| C5 | Abstract | 150–200 words; no first person; no citations | — | COULD NOT READ | same | 21:39 |
| C6 | Keywords | CCS 2012 concepts plus additional keywords | — | COULD NOT READ | same | 21:39 |
| C7 | Review process; single or double anonymous | AE gets at least 3 reviews; anonymity not found | — | COULD NOT READ | same | 21:39 |
| C8 | Template and file format | Single-column PDF; `acmart` `[manuscript]`; published `acmsmall` | — | COULD NOT READ | same; https://www.acm.org/publications/authors/submissions | 21:39; about 21:48 (fetch tool) |
| C9 | Citation style | Author-year in brackets, alphabetical list | — | COULD NOT READ | author guidelines (as C2) | 21:39 |
| C10 | Statistics reporting | Statistic, df, value, p | — | COULD NOT READ | same | 21:39 |
| C11 | Figures | Numbered, captioned, about 12.7 cm wide, ≥ 600 dpi, descriptions | — | COULD NOT READ | same | 21:39 |
| C12 | Supplementary material | Optional, with readme.txt | — | COULD NOT READ | same | 21:39 |
| C13 | Cover letter | Required for Review Articles only | — | COULD NOT READ | same | 21:39 |
| C14 | ORCID | Required for the submitting author | — | COULD NOT READ | same | 21:39 |
| C15 | Declarations, CRediT, data statement, ethics for human annotators | Not found as requirements | — | COULD NOT READ | same | 21:39 |
| C16 | AI use (ACM Policy on Authorship) | Writing help: no disclosure required; research use: mandatory description in Methods; AI not an author ("updated on May 14, 2026") | — | COULD NOT READ | https://www.acm.org/publications/policies/new-acm-policy-on-authorship | about 21:48 (fetch tool, HTTP 403) |
| C17 | ACM policy on prior publication and simultaneous submissions; conference paper later extended to a journal article | Not read on the ACM page (2026-11-13 note: a search summary mentioned "at least 25%") | — | COULD NOT READ | https://www.acm.org/publications/policies/prior-publication-policy | 21:38 (plain fetch 403), 21:39 (browser block page) |
| C18 | Open access and charge | Fully OA since 2026-01-01; USD 1450 / 950; lower-middle-income USD 725 / 475; free via ACM Open or low-income country | — | COULD NOT READ | https://dl.acm.org/journal/tallip/open-access ; https://www.acm.org/publications/openaccess | about 21:48 (fetch tool); 21:50 |
| C19 | Subscription (no-fee) route | None (fully OA) | — | COULD NOT READ | same | 21:50 |
| C20 | Turnaround | Not found | — | COULD NOT READ | https://dl.acm.org/journal/tallip | 21:50 |

---

## 4. TAIMMA 2027 (conference) and Springer proceedings rules

Earlier read: `manuscript/cfp/TAIMMA_CONF_2026-11-13.md`. The conference site was downloaded once (plain fetch, HTTP 200) and its embedded page was read in full (sha256 of the embedded block `7bec6fdb...6462`).

| # | Fact | 13 Nov survey says | Live page says today | Status | URL | Read (UTC) |
|---|---|---|---|---|---|---|
| D1 | Name and edition | "The First International Conference on Transformative Applied Informatics and Mixed-Methods Analytics (TAIMMA 2027)" | Same. | CONFIRMED | https://www.taimma-conf.org/ | 21:38 |
| D2 | Conference dates and mode | 16–18 March 2027, Kyoto; hybrid; on-site 16–17, online 18 | "16–18 March 2027, Kyoto, Japan [Hybrid Mode Conference]"; "onsite program ... on March 16–17, 2027"; "online program is scheduled for March 18, 2027". | CONFIRMED | same | 21:38 |
| D3 | Paper deadlines and time zone | 5 Nov, 20 Nov, 2 Dec 2026, AoE | "Paper Submission Deadline (AoE): First Call November 5, 2026; Second Call November 20, 2026; Third Call December 2, 2026". End of 20 Nov AoE = 21 Nov 11:59 UTC = 21 Nov 18:59 Vietnam time. End of 2 Dec AoE = 3 Dec 18:59 Vietnam time. | CONFIRMED | same | 21:38 |
| D4 | Notification dates | 30 Nov, 10 Dec, 25 Dec 2026 | Same ("Acceptance Notification (AoE)"). | CONFIRMED | same | 21:38 |
| D5 | Camera-ready, author registration, files to publisher | 10 Jan 2027; 31 Jan 2027 | "Camera-Ready Paper & Author Registration Deadline (AoE) January 10, 2027"; "Target Date for Delivering Complete Proceedings Files to the Publisher January 31, 2027". | CONFIRMED | same | 21:38 |
| D6 | News or extension since 13 Nov | Newest item: 13 Nov (dates moved) | Newest item is still "Nov 13, 2026". No "extended" wording anywhere on the page. | CONFIRMED | same | 21:38 |
| D7 | Page limits on the conference site | Full 12–15 pages; short minimum 6, no maximum stated | "Full papers: minimum 12 pages, maximum 15 pages." "Short papers: minimum 6 pages." | CONFIRMED | same | 21:38 |
| D8 | Page ranges in Springer's own author instructions | Not recorded | "The most common types of papers are full papers (12–15 (or more) pages) and short papers (6-11 pages)." "Very short papers (of fewer than 4 pages) may be moved to the back matter. Such papers will neither be available for indexing nor visible as individual papers". | CHANGED (addition, publisher document) | Springer "Instructions for Authors (PDF)", linked from https://link.springer.com/series/558/information-for-authors-and-editors | 21:45 |
| D9 | Template | Springer LNCS format (Word, LaTeX, Overleaf) | "Papers must be prepared in the Springer LNCS format." The Word and LaTeX links are Springer's own template files. | CONFIRMED | https://www.taimma-conf.org/ | 21:38 |
| D10 | Review model | Single-blind; names, affiliations, e-mails in the manuscript; at least three reviewers | "Single-blind peer review"; "Authors must include their full names, affiliations (including complete institutional addresses), and email addresses"; "at least three reviewers". | CONFIRMED | same | 21:38 |
| D11 | Submission link | Microsoft CMT, `cmt3.research.microsoft.com/TAIMMA2027` | Same link. Not opened (login page). | CONFIRMED | same | 21:38 |
| D12 | Originality rule | "Papers must be original, unpublished, and not under review elsewhere." | Same sentence. | CONFIRMED | same | 21:38 |
| D13 | AI rule on the conference site | Only "AI-generated images and diagrams should be avoided." | Same; nothing on AI-written text. | CONFIRMED | same | 21:38 |
| D14 | Proceedings statement on the conference site | "Springer's ... (CCIS) series (confirmed)"; pre-proceedings model; first page of the Springer letter linked | Same sentences; same letter link. | CONFIRMED | same | 21:38 |
| D15 | Does Springer's own site list the volume? | "Springer's own site has no TAIMMA entry"; no public Springer list of future CCIS volumes was found | Springer's document "CCIS Forthcoming Proceedings (2024–2027)" (page header "© Springer – 2nd November, 2026") lists, under "March 2027 — 3 events": "27-29 Kyoto, Japan TAIMMA 2027". The entry links to `https://www.taimma-conf.org/`. The document calls itself "a non-exclusive list of conferences". It shows the **old** dates (27–29 March). Its date (2 Nov) is before the 13 Nov survey, so the entry was missed then; it is not new. | CHANGED | "CCIS Forthcoming Proceedings (PDF)", linked from https://link.springer.com/series/558/information-for-authors-and-editors | 21:45 |
| D16 | SpringerLink search for "TAIMMA" | No results | "Sorry, No results were found". | CONFIRMED | https://link.springer.com/search?query=%22TAIMMA%22 | 21:43 |
| D17 | CCIS series indexing line | DBLP, EI Compendex, INSPEC, JST, Norwegian Register, SCImago, SCOPUS, zbMATH (series level) | Same eight names. ISSN 1865-0929, e-ISSN 1865-0937. Nothing about single volumes. | CONFIRMED | https://link.springer.com/series/7899 | 21:42 |
| D18 | Discover Informatics collection for the conference | Seven collections listed; none names TAIMMA | Seven collections listed; none names TAIMMA, Kyoto or KCGI. | CONFIRMED | https://link.springer.com/journal/44564/collections | 21:43 |
| D19 | Fees | On-site author USD 380 / JPY 60,000 (late 420 / 65,000); online 155 / 25,000 (late 180 / 30,000); student on-site 320 / 50,000 (late 350 / 55,000); student online 130 / 20,000 (late 150 / 25,000); non-author 155 / 25,000; listener free; early deadline 10 Jan 2027 | All figures the same. | CONFIRMED | https://www.taimma-conf.org/ | 21:38 |
| D20 | Extra-paper fee | USD 120 / JPY 18,000 from the second paper, same registered author | Same. | CONFIRMED | same | 21:38 |
| D21 | Withdrawal rule | Not recorded | The words "withdraw" and "withdrawal" do not occur on the page. | NOT FOUND ON THE LIVE PAGE | same | 21:38 |
| D22 | Refund rule, payment method, no-show rule | Not stated | Not stated ("refund" does not occur). | NOT FOUND ON THE LIVE PAGE | same | 21:38 |
| D23 | EasyChair call page | Still 27–29 March; only the 5 Nov deadline; "12–15 pages recommended" | Still "Kyoto, Japan, March 27-29, 2027"; "Submission deadline November 5, 2026"; "Full Papers: 12–15 pages recommended". | CONFIRMED | https://easychair.org/cfp/taimma2027 | 21:47 |
| D24 | Springer code of conduct for book authors: originality | "must not contain any plagiarism and should not have been published elsewhere in any form or language"; "Recycling data and texts ... is generally not allowed" (read through a summary; wording to re-check) | Read directly. "The submitted work must not contain any plagiarism and should not have been published elsewhere in any form or language (unless it is a complete work that follows up on a published preliminary report like an abstract, poster, conference presentation or journal article; ...)". "Recycling data and texts from an Author's own published manuscripts is generally not allowed. In case of overlap with a previously accepted / published paper transparency should be provided on how much is new ... in a letter to the series editor and / or Publisher and consequently in the work itself." | CONFIRMED | https://www.springernature.com/gp/authors/book-authors-code-of-conduct | 21:46 |
| D25 | Related manuscripts under review elsewhere (Springer code) | Not recorded | "Authors should inform the Editor or Publisher of related manuscripts under consideration for publication by the same Author(s) with another publisher and provide details of these relevant manuscripts." | CHANGED (addition, publisher page) | same | 21:46 |
| D26 | Springer AI policy for proceedings authors | 13 Nov: no AI rule on the code-of-conduct page. 10 Nov check: authors "Disclose AI use for trust and transparency"; no place or wording | Proceedings page: authors of proceedings papers must "abide by our book publishing policies and respective codes of conduct". Author instructions, section 2: "For Springer Nature's policy on the use of AI, please refer to this page." Book policies, "AI Editorial Policies": authors "Remain fully accountable for originality, accuracy, and integrity" and "Disclose AI use for trust and transparency"; low-risk use: "Permitted. Disclosure enhances trust and transparency"; "Assigning authorship or accountability to AI systems or tools": not permitted. No place, title or wording for the disclosure. | CONFIRMED (against the 10 Nov check) | https://link.springer.com/series/558/information-for-authors-and-editors ; https://www.springernature.com/gp/policies/book-publishing-policies ; Instructions for Authors (PDF) | 21:42, 21:46, 21:45 |
| D27 | Reusing the proceedings paper in a later journal article (Springer licence form) | Not recorded | "License-to-Publish Form, Singapore": the author may "publish an expanded version of their Contribution provided the expanded version (i) includes at least 30% new material (ii) includes an express statement specifying the incremental change in the expanded version (e.g., new results, better description of materials, etc.)". When reusing, the author "acknowledges and references first publication in the Volume"; minimum wording: "First published in [Volume, page number, year] by Springer Nature". | CHANGED (addition, publisher document) | "License-to-Publish Form, Singapore (Word)", linked from https://link.springer.com/series/558/information-for-authors-and-editors | 21:50 |
| D28 | Other terms of the same licence form | 13 Nov: a licence-to-publish is signed by the corresponding author | Exclusive licence. The grant covers "all forms of training, fine-tuning, developing and improving AI". Warranty: "the Contribution has not been previously published". Accepted manuscript: own website at once; institutional or funder repository public after "twelve (12) months". Author instructions: "Digital signatures are not acceptable." | CHANGED (addition, publisher document) | same; Instructions for Authors (PDF) | 21:50, 21:45 |
| D29 | Springer conditions on the conference itself | Not recorded | Guidelines for Volume Editors: "at least three reviewers per paper"; "Papers must be presented to the participants"; "we do not publish the proceedings of conferences with an extremely broad scope"; "Springer reserves the right to reject proceedings following the delivery of the files" if requirements are not met or the conference "does not take place in the sense that papers are presented and discussed in real time". | CHANGED (addition, publisher document) | "Guidelines for Volume Editors (PDF)", linked from the same Springer page | 21:45 |

Notes on D15 and D27:

- D15 is publisher-side support for the claim "accepted in principle". It is not a promise that the volume will appear (see D29), and it says nothing about indexing of this volume. Springer's list has not been updated for the new dates.
- D27: which licence form a given volume uses is Springer's choice. The Singapore form was read because the 10 Oct letter came from Springer Nature Singapore. The "Default" form was not read. The 30% figure is a right the publisher grants to the author; the journal that receives the expanded paper applies its own rule as well.

---

## Consequences for the papers

**Paper A (SPIC)**

1. The journal's guide could not be read today. Abstract ≤ 250 words, 1–7 keywords, the highlights requirement, single-anonymized review, numbered references and research-data Option C are **still not re-checked**. A person must open the guide in a normal browser before submission.
2. AI declaration (publisher policy, "updated June 2026", same version as on 10 Nov): if generative AI was used to prepare the manuscript, a separate section "immediately before the references" is required. Recommended title: "Declaration of generative AI and AI-assisted technologies in the manuscript preparation process". Recommended statement: "During the preparation of this work, the author(s) used [NAME OF TOOL / SERVICE] in order to [REASON]. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the published article." Translation by AI is disclosed. Grammar, spelling and basic reference-manager functions are exempt.
3. AI in the research process, including AI-written or AI-edited code, goes in Methods "in detail". AI used "to select, collate, generate or edit references" is declared in the manuscript.
4. Money: open access USD 2,830 (list of 5 Oct 2026); the subscription route costs nothing; embargo 24 months.
5. Highlights: 3–5 bullets, each ≤ 85 characters with spaces, as a Word file. The publisher-wide page says they are not needed until the final files; keep them ready anyway, because the journal's own rule was not read.
6. Conference-to-journal: the publisher's ethics page lists only an abstract, a published lecture, a thesis and a preprint as allowed earlier forms. It has no clause for an extended conference paper. A full proceedings paper on the same research is therefore a risk for A until the journal's "submission declaration" is read.
7. Preprint: allowed publisher-wide, but society-owned journals may differ, and SPIC is a EURASIP journal. Not settled today (A stays without a preprint in any case).
8. Figures: line art ≥ 1000 dpi, photos ≥ 300 dpi, combination art 500 dpi. Use TIFF, JPEG, EPS or PDF; PNG is not on the publisher's format list.

**Paper B (LRE)** — every card fact that the live pages state was confirmed; four additions and five items the pages do not state are in the table.

1. Length: full paper "typically 18-25 pages", no hard limit. Abstract 150–250 words. Keywords 4–6. Single-blind. References by name and year, APA 7.
2. Requirements on the live page that are not in the card (besides the title-page list, B25): (a) author contributions and competing interests must be typed into the submission system, and only that text is published; (b) editable source files at every submission, or the paper is not considered; (c) for the Special Focus route: a literature review of both kinds of earlier work, and state-of-the-art methods or a reason for older ones.
3. Human raters (the pairwise-preference study): the page asks for an ethics-approval statement where applicable, an informed-consent statement, and says "Participant consent should be obtained and documented prior to data collection."
4. AI: the journal page says LLM use is "documented in the Methods section" and copy editing "does not need to be declared". The publisher framework asks authors to "Clearly describe use" even for language editing, in "an AI Declaration in your manuscript", with no fixed place or wording, and says authors "will also be asked to confirm" compliance at submission. The two layers still differ; the stricter one is the publisher's.
5. Conference-to-journal: allowed as "an expansion of previous work", with "transparency on the re-use of material" and a note in the cover letter. No percentage is given.
6. Money: open access £2,590 / USD 3,590 / €2,890; the subscription route has "no APC charges".

**Paper C (TALLIP)**

1. Nothing was re-checked. All ACM hosts refused every reading method used today.
2. The values in the card (title 6–12 words, abstract 150–200 words, ≥ 25% new content for a conference extension, the AI rule of the 14 May 2026 policy, the charges) are as last read on 2026-10-27 and 2026-11-10. They are not confirmed for today.
3. The ACM policy on prior publication and simultaneous submissions has **never** been read on the ACM page in this project (blocked on 13 Nov and again today). A person must open it in a normal browser.

**Conference (TAIMMA 2027)**

1. The site has not changed since 13 Nov: same dates, deadlines, page limits, template, review model, fees and links. Second call closes 21 Nov 18:59 Vietnam time; third call 3 Dec 18:59.
2. New for the project: Springer's own list of forthcoming CCIS proceedings (dated 2 Nov 2026) names TAIMMA 2027. This supports the publisher claim. The list shows the old dates, is "non-exclusive", and Springer keeps the right to refuse a volume after delivery. Volume-level indexing is still promised nowhere.
3. Springer's instructions give short papers as 6–11 pages and full papers as 12–15 (or more).
4. A paper published there can be expanded into a journal article only with at least 30% new material and an express statement of what is new (Springer licence form), and the first publication must be acknowledged. The target journal's own rule applies on top: LRE accepts "an expansion of previous work" with transparency; Elsevier's publisher page has no such clause; ACM's rule was not read.
5. AI: Springer asks proceedings authors to disclose AI use; no wording is fixed. The conference adds only that AI-generated images should be avoided.
6. The licence is exclusive and includes rights to use the paper for AI training. Papers must be presented. Withdrawal, refund and no-show rules are not stated.

---

## Sources read today (2026-11-14 UTC)

Springer and Springer Nature (clean headless browser unless marked):
- https://link.springer.com/journal/10579/submission-guidelines (21:39); https://link.springer.com/journal/10579 (21:41); `/aims-and-scope` (21:41); `/how-to-publish-with-us` (21:41)
- https://link.springer.com/brands/springer/journal-policies (21:41)
- https://www.springernature.com/gp/policies/editorial-policies/ai-manuscript-preparation (21:44); `/using-ai-in-research` (21:44); `/ai-editor-guidance` (21:42)
- https://www.springernature.com/gp/policies/book-publishing-policies (21:46); https://www.springernature.com/gp/authors/book-authors-code-of-conduct (21:46)
- https://link.springer.com/series/558/information-for-authors-and-editors (21:42) and four files it links (plain fetch, 21:45–21:50): "CCIS Forthcoming Proceedings (PDF)" (sha256 `42a781a1...6b9e`), "Instructions for Authors (PDF)" (`b6a56391...a385`), "Guidelines for Volume Editors (PDF)" (`f800c076...263e`), "License-to-Publish Form, Singapore (Word)" (`627ead08...39ac`)
- https://link.springer.com/series/7899 (21:42); https://link.springer.com/search?query=%22TAIMMA%22 (21:43); https://link.springer.com/journal/44564/collections (21:43)

Elsevier (plain fetch):
- https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals (21:38)
- https://www.elsevier.com/about/policies-and-standards/publishing-ethics (21:47); `/pricing` (21:47); `/sharing` (21:49)
- APC price list https://legacyfileshare.elsevier.com/els_com_pricing/article-publishing-charge.xlsx (21:48; sha256 `abaf1002...119a`); embargo list linked from the sharing page (21:49)
- https://shop.elsevier.com/journals/signal-processing-image-communication/0923-5965 (21:47)
- https://www.elsevier.com/researcher/author/tools-and-resources/highlights (21:47); `/researcher/author/policies-and-guidelines/latex-instructions` (21:47); `/credit-author-statement` (21:47); `/researcher/author/tools-and-resources/research-data/data-guidelines` (21:49); artwork pages `artwork-types` (21:50) and `artwork-formats-checklist` (21:49)

Conference:
- https://www.taimma-conf.org/ (plain fetch, 21:38); https://easychair.org/cfp/taimma2027 (21:47)

One address guessed by me returned "Page Not Found" and is not a source: `https://link.springer.com/journal/10579/open-access-publishing`.
