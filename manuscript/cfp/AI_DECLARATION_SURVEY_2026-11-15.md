# AI-use declarations in published papers, 2018 – November 2026: counts and evidence

Made on 2026-11-15. All searches and reads were done on 2026-11-15 between 00:28 and 01:10 UTC (add 7 hours for Vietnam time). One row per paper is in `AI_DECLARATION_SURVEY_2026-11-15_evidence.tsv` in this folder. This file reports counts and their limits. It makes no recommendation.

## 0. How to read the numbers

**Declaration of use.** A sentence in the paper in which the authors say that they themselves used a generative-AI or AI-assisted tool (ChatGPT, Gemini, Claude, Copilot, Grammarly, DeepL, an unnamed "AI tool" or "large language model") while writing the manuscript or doing the work, written as a disclosure. A paper that studies such tools, or that uses a model as research material or as a part of its method (a baseline, an annotator inside the experiment, a data generator), is **not** counted: it is recorded as "about AI, not a declaration". A sentence that says no such tool was used is counted separately as a "statement of no use".

**Venues.** V1 = Signal Processing: Image Communication (Elsevier). V2 = Language Resources and Evaluation (Springer). V3 = ACM Transactions on Asian and Low-Resource Language Information Processing. V4 = Communications in Computer and Information Science (Springer proceedings series), 2023–2026 only. V5 = image-captioning topic set, 2023–2026 only.

**Columns of the tables.**

- *Papers (OpenAlex)*: works of type `article` with that source and publication year (V4: all works of the series; V5: types article, conference-paper, review). For V2 the count is restricted to DOIs that start with `10.1007/s10579` (see the note in 2.2).
- *With searchable full text*: OpenAlex flag `has_fulltext:true`. Only these papers can be found by a phrase inside the body or the end matter. The other papers are searched in title, abstract and keywords only. This column is the real denominator of the index step.
- *Candidates*: papers that match declaration wording in the index (phrase lists S1–S7, exact lists G1, G2, G3, G5, G6 and the exact word Grammarly; section 5). For V4 and V5 a narrower rule is used (given under the table in 2.4), because "used ChatGPT" and "generative AI tools" are research topics there.
- *Verified declarations of use*: the statement was read in the published version (publisher page, publisher copy, or a publisher pre-proof) and is a declaration of use. For V2 and for the V4 sample this column also holds statements found by reading pages, with no index hit.
- *Declaration read in a preprint only*: the statement was read in a preprint; the published version could not be read.
- *Index hit only*: a candidate whose statement could not be read.
- *Candidates read: not a declaration*: the matched words were read and are something else (a funding sentence, a research topic, a cited title).
- *Sample: read / with a statement*: papers whose text was read without regard to index hits, and how many of them carry a statement (of use or of no use). The design differs by venue and is given under each table.

**Status words in the evidence file.** *verified*: statement read in the published version. *verified (preprint only)*: statement read in a preprint, published version not read. *declares no use*: statement read, says no tool was used. *index hit only*: the index matched declaration wording, the statement was not read. *about AI, not a declaration*: the matched words are about AI as a topic or as research material. *read, no declaration found*: the copy named in the row was read and holds no AI-use statement. The last column, `counted_in_report_tables`, names the table column in which the row is counted, or says why the row is listed but not counted (section 3). Where a record has no DOI, the `doi` column holds its OpenAlex id as a URL.

**Weak hits.** A tool word anywhere in the indexed text ("ChatGPT", "Claude", "Gemini", "Copilot", "generative AI", "large language model" with a verb) is reported as a count only. In these venues the tool is usually the research object, so a weak hit is not a candidate. The stemmed search for "Grammarly" matches the word "grammar" and is not used; the exact form is used instead.

## 1. Headline counts, 2023–2026

| Venue | Papers (OpenAlex) | With searchable full text | Candidates | Verified declarations of use | Read in a preprint only | Index hit only | Statements of no use | Sample: read / with a statement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| V1 Signal Processing: Image Communication | 548 | 49 (9%) | 5 | 4 | 1 | 0 | 0 | 25 / 4 |
| V2 Language Resources and Evaluation | 311 | 153 (49%) | 11 | 3 | 0 | 2 | 2 | 99 / 2 |
| V3 ACM TALLIP | 674 | 401 (59%) | 10 | 1 | 0 | 0 | 0 | 20 / 1 |
| V4 CCIS (Springer) | 36689 | 3412 (9%) | 38 | 23 | 2 | 2 | 0 | 240 / 2 |
| V5 image-captioning topic set | 4103 | 1715 (42%) | 26 | 9 | 1 | 8 | 1 | — |

- **V1.** 4 verified declarations of use (2023: 0, 2024: 0, 2025: 1, 2026: 3) and 1 more read in a preprint only (2026). Only 49 of 548 papers (9%) have searchable full text. All 25 publisher copies that could be read in full were read: 4 carry a declaration (2023: 0 of 3; 2024: 0 of 5; 2025: 1 of 5; 2026: 3 of 12).
- **V2.** Every public article page was read (all 311 papers of 2023–2026). 3 declarations of use (2023: 0, 2024: 0, 2025: 0, 2026: 3) and 2 statements of no use (2023: 0, 2024: 0, 2025: 1, 2026: 1). 2 of the 3 declarations of use were not found by the index and were found only by reading the pages.
- **V3.** 1 verified declaration of use (2023: 0, 2024: 0, 2025: 0, 2026: 1). 401 of 674 papers (59%) have searchable full text. The publisher site refuses automated reads, so reading was limited to 29 copies cached by OpenAlex (10 candidates and a sample of 5 papers per year: 20 read, 1 with a declaration; one paper is in both).
- **V4.** 23 verified declarations of use (2023: 0, 2024: 0, 2025: 4, 2026: 19) and 2 read in a preprint only. 3412 of 36689 works (9%) have searchable full text. In a seeded random sample of 240 chapter pages, 2 show a declaration of use in the public part of the page (2023: 0 of 60; 2024: 0 of 60; 2025: 0 of 60; 2026: 2 of 60).
- **V5.** 9 verified declarations of use (2023: 0, 2024: 0, 2025: 4, 2026: 5), 1 read in a preprint only, 8 index hits not read, 1 statement of no use. 1715 of 4103 works (42%) have searchable full text.
- **2018–2022 (V1–V3).** Measured, not assumed: 0 declarations. The index gives 0 + 2 + 1 candidates in those years (V1 + V2 + V3); none was found to be a declaration (one V2 paper of 2022 that names Grammarly is behind the paywall and could be read in its end matter only). For V2 the public pages of all 197 papers of 2018–2022 were also read: no statement.

These are counts of statements that could be found and read. They are lower bounds for each venue, for the reasons in section 6.

## 2. Counts per venue and year

### 2.1 V1 Signal Processing: Image Communication (ISSN 0923-5965)

| Year | Papers (OpenAlex) | With searchable full text | Candidates (declaration wording in the index) | Verified declarations of use | Declaration read in a preprint only | Index hit only (statement not read) | Candidates read: not a declaration | Statements of no use | Sample: read / with a statement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 176 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 2019 | 193 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 2020 | 153 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 2021 | 214 | 38 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 2022 | 135 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 2023 | 92 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 3 / 0 |
| 2024 | 82 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 5 / 0 |
| 2025 | 141 | 10 | 1 | 1 | 0 | 0 | 0 | 0 | 5 / 1 |
| 2026 | 233 | 19 | 4 | 3 | 1 | 0 | 0 | 0 | 12 / 3 |
| **2018–2026** | 1419 | 175 | 5 | 4 | 1 | 0 | 0 | 0 | — |
| **2023–2026** | 548 | 49 | 5 | 4 | 1 | 0 | 0 | 0 | 25 / 4 |
| **2018–2022** | 871 | 126 | 0 | 0 | 0 | 0 | 0 | 0 | — |

Weak hits (a tool word anywhere in the indexed text; not candidates):

| Year | "generative AI" | "ChatGPT" | Grammarly (exact) | "Copilot" | "Claude" | "Gemini" | "large language model" + verb |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2019 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2020 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2021 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2022 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2023 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2024 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2025 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 2026 | 3 | 3 | 2 | 0 | 1 | 1 | 4 |

- Sample design: not a draw. In 2023–2026 only 25 papers have a publisher-hosted copy (OpenAlex `has_content.grobid_xml:true` and open-access status hybrid or bronze) that could be read in full, fewer than 25 in every year, so all 25 were read (OpenAlex cached copy, whole text: body, acknowledgements, declarations). Counts per year are in the last column.
- The 5 candidates were all read. Four are in publisher copies (three of them marked "Journal Pre-proof"). The fifth was read in the arXiv preprint only; its published version is on ScienceDirect, which refuses automated reads.
- Weak hits read as well: 4 publisher copies, 4 arXiv preprints and 1 PMC copy; none carries a statement. Three more weak-hit papers were not read: one whose only open copy is on SSRN, and two closed-access papers matched in title, abstract or keywords (one of them is about large language models). All are rows in the evidence file; none is counted as a candidate.
- Papers of V1 with no searchable full text, which could be neither searched inside nor read: 2023: 86, 2024: 68, 2025: 131, 2026: 214.

### 2.2 V2 Language Resources and Evaluation (ISSN 1574-020X)

| Year | Papers (OpenAlex) | With searchable full text | Candidates (declaration wording in the index) | Verified declarations of use | Declaration read in a preprint only | Index hit only (statement not read) | Candidates read: not a declaration | Statements of no use | Sample: read / with a statement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 30 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 2019 | 39 | 17 | 1 | 0 | 0 | 0 | 1 | 0 | — |
| 2020 | 31 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 2021 | 43 | 29 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 2022 | 54 | 35 | 1 | 0 | 0 | 1 | 0 | 0 | — |
| 2023 | 73 | 42 | 2 | 0 | 0 | 0 | 2 | 0 | 25 / 0 |
| 2024 | 89 | 44 | 1 | 0 | 0 | 1 | 0 | 0 | 25 / 0 |
| 2025 | 79 | 34 | 3 | 0 | 0 | 0 | 3 | 1 | 25 / 1 |
| 2026 | 70 | 33 | 5 | 3 | 0 | 1 | 2 | 1 | 24 / 1 |
| **2018–2026** | 508 | 259 | 13 | 3 | 0 | 3 | 8 | 2 | — |
| **2023–2026** | 311 | 153 | 11 | 3 | 0 | 2 | 7 | 2 | 99 / 2 |
| **2018–2022** | 197 | 106 | 2 | 0 | 0 | 1 | 1 | 0 | — |

Pages read on the publisher site (every paper):

| Year | Papers (LRE DOI) | Public page read | Open access: whole text on the page | Not open access: end matter only | Declarations of use found | Statements of no use found |
|---|---:|---:|---:|---:|---:|---:|
| 2018 | 30 | 30 | 6 | 24 | 0 | 0 |
| 2019 | 39 | 39 | 13 | 26 | 0 | 0 |
| 2020 | 31 | 31 | 10 | 21 | 0 | 0 |
| 2021 | 43 | 43 | 24 | 19 | 0 | 0 |
| 2022 | 54 | 54 | 23 | 31 | 0 | 0 |
| 2023 | 73 | 73 | 34 | 39 | 0 | 0 |
| 2024 | 89 | 89 | 42 | 47 | 0 | 0 |
| 2025 | 79 | 79 | 28 | 51 | 0 | 1 |
| 2026 | 70 | 70 | 24 | 46 | 3 | 1 |

Weak hits (not candidates):

| Year | "generative AI" | "ChatGPT" | Grammarly (exact) | "Copilot" | "Claude" | "Gemini" | "large language model" + verb |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2019 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2020 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2021 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 2022 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 2023 | 0 | 0 | 0 | 0 | 1 | 0 | 3 |
| 2024 | 1 | 5 | 0 | 0 | 0 | 0 | 11 |
| 2025 | 2 | 11 | 0 | 0 | 1 | 1 | 22 |
| 2026 | 2 | 11 | 0 | 0 | 1 | 3 | 23 |

- Papers: OpenAlex lists 498 articles for 2020 and 46 for 2018 under this source. 467 of the 2020 records and 16 of the 2018 records have no DOI; they were not checked one by one and are left out. The table counts records whose DOI starts with `10.1007/s10579`. The "searchable full text" column is the OpenAlex count for the source and year and was not re-restricted.
- The public Springer page shows the end matter (Acknowledgements, Funding, Ethics declarations, Notes, Data availability) for every article, and the whole text for open-access articles. Each page was fetched once and scanned twice by pattern (section 5); every flagged sentence was read.
- Sample design (as asked): per year, the open-access pages sorted by DOI, `random.Random(20261115 + year).shuffle`, first 25 (frame sizes 2023: 34, 2024: 42, 2025: 28, 2026: 24). The draw is in section 5.3. The sample is a subset of the full reading, so the full-reading table above is the stronger result.
- Many index hits on "during the preparation of this manuscript" are the standard Springer funding sentence ("no funds, grants, or other support were received during the preparation of this manuscript"), not an AI statement.

### 2.3 V3 ACM TALLIP (ISSN 2375-4699)

| Year | Papers (OpenAlex) | With searchable full text | Candidates (declaration wording in the index) | Verified declarations of use | Declaration read in a preprint only | Index hit only (statement not read) | Candidates read: not a declaration | Statements of no use | Sample: read / with a statement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 43 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 2019 | 61 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 2020 | 75 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 2021 | 153 | 21 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| 2022 | 208 | 60 | 1 | 0 | 0 | 0 | 1 | 0 | — |
| 2023 | 273 | 244 | 2 | 0 | 0 | 0 | 2 | 0 | 5 / 0 |
| 2024 | 178 | 64 | 1 | 0 | 0 | 0 | 1 | 0 | 5 / 0 |
| 2025 | 136 | 78 | 5 | 0 | 0 | 0 | 5 | 0 | 5 / 0 |
| 2026 | 87 | 15 | 2 | 1 | 0 | 0 | 1 | 0 | 5 / 1 |
| **2018–2026** | 1214 | 503 | 11 | 1 | 0 | 0 | 10 | 0 | — |
| **2023–2026** | 674 | 401 | 10 | 1 | 0 | 0 | 9 | 0 | 20 / 1 |
| **2018–2022** | 540 | 102 | 1 | 0 | 0 | 0 | 1 | 0 | — |

Weak hits (not candidates):

| Year | "generative AI" | "ChatGPT" | Grammarly (exact) | "Copilot" | "Claude" | "Gemini" | "large language model" + verb |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2019 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2020 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2021 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2022 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 2023 | 1 | 5 | 2 | 0 | 5 | 1 | 8 |
| 2024 | 0 | 8 | 0 | 0 | 0 | 0 | 8 |
| 2025 | 1 | 17 | 0 | 0 | 3 | 6 | 35 |
| 2026 | 1 | 8 | 0 | 1 | 4 | 8 | 21 |

- dl.acm.org answered HTTP 403 to a plain request, so no ACM page was read. Reading used the copies cached by OpenAlex (publisher PDFs of open-access or free-to-read articles, parsed to text).
- All 10 candidates with searchable full text were read: 1 declaration of use (2026, in the Acknowledgment). The others are research uses or topics (for example "used GPT-4" inside a data pipeline). One candidate has no full text in the index and was classed from its title.
- Sample design: per year, the works with a cached publisher copy (frame sizes 2023: 243, 2024: 54, 2025: 78, 2026: 14) sorted by OpenAlex id, `random.Random(20261115 + year).shuffle`, first 5. Five per year, not 25: each cached file costs 100 of the 10,000 daily OpenAlex credits, and the key is shared. The draw is in section 5.3. With 5 papers per year the sample cannot estimate a rate; it only checks the index (no declaration was found that the phrase lists had missed).
- The weak-hit papers of V3 (several hundred, mostly papers about language models) were not read one by one. A declaration that uses none of the listed wordings would be missed.

### 2.4 V4 Communications in Computer and Information Science (ISSN 1865-0929), 2023–2026

| Year | Papers (OpenAlex) | With searchable full text | Candidates (declaration wording in the index) | Verified declarations of use | Declaration read in a preprint only | Index hit only (statement not read) | Candidates read: not a declaration | Statements of no use | Sample: read / with a statement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 6649 | 774 | 2 | 0 | 0 | 0 | 2 | 0 | 60 / 0 |
| 2024 | 7674 | 823 | 2 | 0 | 0 | 1 | 1 | 0 | 60 / 0 |
| 2025 | 11370 | 968 | 8 | 4 | 1 | 0 | 3 | 0 | 60 / 0 |
| 2026 | 10996 | 847 | 26 | 19 | 1 | 1 | 7 | 0 | 60 / 2 |
| **2023–2026** | 36689 | 3412 | 38 | 23 | 2 | 2 | 13 | 0 | 240 / 2 |

Weak hits (not candidates):

| Year | "generative AI" | "ChatGPT" | Grammarly (exact) | "Copilot" | "Claude" | "Gemini" | "large language model" + verb |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 32 | 63 | 0 | 4 | 10 | 2 | 68 |
| 2024 | 126 | 154 | 1 | 11 | 14 | 13 | 223 |
| 2025 | 292 | 232 | 0 | 20 | 36 | 72 | 661 |
| 2026 | 371 | 200 | 7 | 36 | 70 | 116 | 774 |

Seeded random sample of chapter pages (publisher site):

| Year | Pages drawn | Pages read | Open access (whole text) | Page shows Acknowledgements, Ethics declarations or Disclosure | Declaration of use on the page | Statement of no use on the page |
|---|---:|---:|---:|---:|---:|---:|
| 2023 | 60 | 60 | 1 | 21 | 0 | 0 |
| 2024 | 60 | 60 | 1 | 19 | 0 | 0 |
| 2025 | 60 | 60 | 0 | 24 | 0 | 0 |
| 2026 | 60 | 60 | 1 | 32 | 2 | 0 |

- Subset covered, exactly: (a) the index step covers the whole series for 2023–2026 but can see inside only the works with searchable full text (second column); (b) every candidate chapter was looked up on its public Springer page, and on an open repository copy where OpenAlex lists one; (c) a random sample of 60 works per year, drawn by OpenAlex itself (`sample=60&seed=20261115`, section 5.3), whose public pages were read.
- The public chapter page shows Acknowledgements and Ethics declarations when the chapter has them; the body is visible only for open-access chapters. A statement placed in the body of a paywalled chapter cannot be seen.
- Candidate rule for V4 and V5: a match on S1, S2a, S3a, S3b, S6, G3, G5 or G6, or a match on (G1 or G2 or exact Grammarly) together with (G4 or S3c). Three hits on records of whole proceedings volumes are listed in the evidence file and not counted.

### 2.5 V5 image-captioning topic set, 2023–2026

| Year | Papers (OpenAlex) | With searchable full text | Candidates (declaration wording in the index) | Verified declarations of use | Declaration read in a preprint only | Index hit only (statement not read) | Candidates read: not a declaration | Statements of no use | Sample: read / with a statement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 824 | 406 | 1 | 0 | 0 | 0 | 1 | 0 | — |
| 2024 | 1052 | 452 | 1 | 0 | 0 | 1 | 0 | 0 | — |
| 2025 | 1257 | 516 | 11 | 4 | 0 | 3 | 3 | 1 | — |
| 2026 | 970 | 341 | 13 | 5 | 1 | 4 | 3 | 0 | — |
| **2023–2026** | 4103 | 1715 | 26 | 9 | 1 | 8 | 7 | 1 | — |

Weak hits (not candidates):

| Year | "generative AI" | "ChatGPT" | "Copilot" | "Claude" | "Gemini" | "large language model" + verb |
|---|---:|---:|---:|---:|---:|---:|
| 2023 | 4 | 29 | 0 | 5 | 1 | 75 |
| 2024 | 18 | 96 | 2 | 6 | 24 | 243 |
| 2025 | 62 | 114 | 9 | 29 | 99 | 362 |
| 2026 | 64 | 55 | 1 | 28 | 64 | 290 |

- Set: OpenAlex works whose title or abstract matches "image captioning" or "caption generation" (stemmed search), types article, conference-paper and review. No sample was drawn for V5.
- Candidates were read in the open copy that OpenAlex lists (publisher PDF, ACL Anthology, CEUR-WS, journal sites) or in Europe PMC. MDPI, PeerJ, MIT Press Direct returned HTTP 403; ScienceDirect, Wiley and SSRN were not attempted. Those rows are "index hit only".
- Outside the counted set, listed in the evidence file for their wording only: 16 records of other types (preprints on arXiv, Research Square and SSRN, one data paper, one book chapter): 10 verified (preprint only), 3 read, no declaration found, 2 verified, 1 index hit only.

## 3. Totals

| Venue (2023–2026) | Papers | With searchable full text | Candidates | Verified declarations of use | Read in a preprint only | Index hit only | Candidates read: not a declaration | Statements of no use |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| V1 | 548 | 49 | 5 | 4 | 1 | 0 | 0 | 0 |
| V2 | 311 | 153 | 11 | 3 | 0 | 2 | 7 | 2 |
| V3 | 674 | 401 | 10 | 1 | 0 | 0 | 9 | 0 |
| V4 | 36689 | 3412 | 38 | 23 | 2 | 2 | 13 | 0 |
| V5 | 4103 | 1715 | 26 | 9 | 1 | 8 | 7 | 1 |
| **All, 2023–2026** | 42325 | 5730 | 90 | 40 | 4 | 12 | 36 | 3 |

V1–V3, 2018–2022: V1: papers 871, with searchable full text 126, candidates 0, declarations 0; V2: papers 197, with searchable full text 106, candidates 2, declarations 0; V3: papers 540, with searchable full text 102, candidates 1, declarations 0.

**Evidence file against these tables.** The evidence file has 129 rows. 98 are counted in the tables above, each in the column named in its last field. 31 are listed but not counted: 16 records of the image-captioning set whose OpenAlex type is not article, conference-paper or review (10 verified (preprint only), 3 read, no declaration found, 2 verified, 1 index hit only), 12 weak-hit papers of V1 that were read or classed, and 3 records of whole proceedings volumes in V4. So the file holds 42 rows with the status *verified* and 40 of them are in the tables. The other 2 are image-captioning records of 2026 that OpenAlex types as data-paper (a data paper in Data in Brief) and book-chapter (an overview paper on CEUR-WS); they are outside the counted V5 set only because of that type.

The venues overlap in a few records (a V4 chapter can also be in V5), so the last line is a sum of venue lines, not a count of distinct papers. Rates should not be computed from the first column: the statement could be looked for only in the papers of the second column, in the V2 pages, and in the samples.

## 4. What the declarations say the tool was used for

Verified declarations of use in published versions, counted venues only: 40.

| Use named in the statement | V1 | V2 | V3 | V4 | V5 | All |
|---|---:|---:|---:|---:|---:|---:|
| language editing only | 4 | 2 | 0 | 12 | 5 | 23 |
| language editing together with another use | 0 | 1 | 1 | 11 | 2 | 15 |
| language editing, rest of the statement not recovered from the PDF text | 0 | 0 | 0 | 0 | 1 | 1 |
| drafting text | 0 | 0 | 0 | 1 | 0 | 1 |
| code | 0 | 1 | 1 | 2 | 1 | 5 |
| data analysis | 0 | 1 | 0 | 1 | 0 | 2 |
| translation | 0 | 0 | 0 | 3 | 0 | 3 |
| figures | 0 | 0 | 1 | 1 | 0 | 2 |
| other (formatting, reference formatting, idea generation, minor verifications) | 0 | 0 | 0 | 6 | 3 | 9 |
| Declarations (each can name several uses) | 4 | 3 | 1 | 23 | 9 | 40 |

| Where the statement sits | V1 | V2 | V3 | V4 | V5 | All |
|---|---:|---:|---:|---:|---:|---:|
| acknowledgements | 1 | 1 | 1 | 9 | 2 | 14 |
| declarations block (Springer: Ethics declarations) | 0 | 2 | 0 | 11 | 0 | 13 |
| titled section before the references or in the appendix | 3 | 0 | 0 | 1 | 6 | 10 |
| body text (end of conclusions or limitations, methods) | 0 | 0 | 0 | 1 | 1 | 2 |
| footnote | 0 | 0 | 0 | 1 | 0 | 1 |

Tools named in the quoted part of the statement or in the row note (a statement can name several): ChatGPT / GPT: 22, tool not named: 9, Grammarly: 5, Gemini: 4, Claude: 3, DeepL: 2, QuillBot: 1, Copilot: 1, Grok: 1.

The 14 statements read in preprints only (all venues, including the records outside the counted V5 set) name the same uses: 14 name language editing, 4 name code, 1 data analysis, 1 drafting text.

Statements of no use: 3 (V2: 2, V4: 0, V5: 1).

## 5. The query behind every number

The OpenAlex key was sent in a request header and is in no query string. `mailto=vsps-research@example.org` was added to each call. Base: `https://api.openalex.org/works?filter=`

### 5.1 Paper counts and searchable full text

| Venue | Filter (then `&group_by=publication_year`) |
|---|---|
| V1 papers | `primary_location.source.id:S38090728,publication_year:2018-2026,type:article` |
| V1 searchable full text | the same + `,has_fulltext:true` |
| V2 papers | `primary_location.source.id:S4306424877,publication_year:2018-2026,type:article` |
| V2 searchable full text | the same + `,has_fulltext:true` |
| V3 papers | `primary_location.source.id:S4306421405,publication_year:2018-2026,type:article` |
| V3 searchable full text | the same + `,has_fulltext:true` |
| V2 papers (table) | list of the V2 filter above with `select=id,doi,...`, kept where the DOI starts with `10.1007/s10579` |
| V4 papers | `primary_location.source.id:S2764900261,publication_year:2023-2026` (all types: 36,577 conference-paper, 109 erratum, 3 retraction) |
| V4 searchable full text | the same + `,has_fulltext:true` |
| V5 papers | `publication_year:2023-2026,title_and_abstract.search:"image captioning" OR "caption generation",type:article\|conference-paper\|review` |
| V5 searchable full text | the same + `,has_fulltext:true` |
| V1, V3 reading frames | list of `primary_location.source.id:<id>,publication_year:2023-2026,type:article` with `select=...,has_content,open_access,best_oa_location`; frame = `has_content.grobid_xml` true and open-access status hybrid or bronze (V3: also version `publishedVersion`) |

Source ids were resolved with `https://api.openalex.org/sources?filter=issn:0923-5965|1574-020X|2375-4699|1865-0929`.

### 5.2 Index hits

Each phrase is one call: the venue filter of 5.1 + `,fulltext.search:<phrase>` (stemmed, stop words dropped; searches title, abstract, keywords and, where present, full text) or + `,fulltext.search.exact:<phrase list joined by OR>` (unstemmed, stop words kept). For V1–V3 every hit list was downloaded (`select=id,doi,title,publication_year,type,has_fulltext,has_content,open_access,best_oa_location,authorships,abstract_inverted_index`, cursor paging) and counted per year locally. For V4 and V5 the weak phrases S5, T1, T3, T4, T5, L1 were counted with `&group_by=publication_year` only. The V5 lists were downloaded without the type filter and filtered by type locally; the V5 weak counts used the type filter.

| Id | Kind | Search string |
|---|---|---|
| L1 | weak | `"large language model" AND ("used to" OR assist OR editing OR proofread)` |
| S1 | declaration wording, stemmed | `"Declaration of generative AI"` |
| S2 | declaration wording, stemmed | `"AI-assisted technologies in the writing process"` — as given in the task; returns 0 in every venue (long phrases with stop words are not matched reliably), so the shortened forms below were added |
| S2a | declaration wording, stemmed | `"AI-assisted technologies"` |
| S3 | declaration wording, stemmed | `"During the preparation of this work"` — as given in the task; returns 0 in every venue (long phrases with stop words are not matched reliably), so the shortened forms below were added |
| S3a | declaration wording, stemmed | `"preparation of this work"` |
| S3b | declaration wording, stemmed | `"preparation of this manuscript"` |
| S3c | declaration wording, stemmed | `"During the preparation"` |
| S4 | declaration wording, stemmed | `"AI Declaration"` |
| S5 | declaration wording, stemmed | `"generative AI"` |
| S6 | declaration wording, stemmed | `"full responsibility for the content of the publication"` |
| S7 | declaration wording, stemmed | `"use of generative AI"` |
| T1 | tool word, stemmed (weak) | `"ChatGPT"` |
| T2 | tool word, stemmed (weak) | `"Grammarly"` — stemmed form matches "grammar"; not used |
| T2x | exact word | `Grammarly` |
| T3 | tool word, stemmed (weak) | `"Copilot"` |
| T4 | tool word, stemmed (weak) | `"Claude"` |
| T5 | tool word, stemmed (weak) | `"Gemini"` |
| D1 | weak, stemmed proximity (V1–V3) | every pair `"<tool>"~25~"<writing word>"` joined by OR; tools: ChatGPT, GPT, language model, LLM, Gemini, Claude, Copilot, DeepSeek, generative AI, AI tool, AI-assisted, artificial intelligence; writing words: manuscript, proofread, polish, readability, language editing, preparation of this, writing of this. Too noisy in language venues ("Polish", "manuscript", "readability" are research topics); used only to choose extra papers to read in V1 |
| G1 | exact list | "used ChatGPT" OR "ChatGPT was used" OR "use of ChatGPT" OR "help of ChatGPT" OR "assistance of ChatGPT" OR "utilized ChatGPT" OR "used OpenAI" OR "used GPT-4" OR "used Grammarly" OR "Grammarly was used" OR "used Gemini" OR "used Claude" OR "used DeepSeek" OR "used Copilot" OR "used GitHub Copilot" OR "ChatGPT to improve" OR "ChatGPT for grammar" OR "ChatGPT to polish" OR "ChatGPT for language" OR "ChatGPT in order to" |
| G2 | exact list | "AI-assisted tools" OR "AI tools were used" OR "AI tool was used" OR "used AI tools" OR "use of AI tools" OR "generative AI tools" OR "use of generative AI" OR "generative AI was used" OR "AI-assisted technologies" OR "AI assisted technologies" OR "used a large language model" OR "used large language models to" OR "used an LLM" OR "LLM was used to" OR "LLMs were used to" OR "language model was used to" OR "AI-based tools" OR "AI writing" OR "AI language model" OR "use of artificial intelligence tools" OR "generative artificial intelligence tools" OR "AI-generated content" |
| G3 | exact list | "during the preparation of this work" OR "during the preparation of this manuscript" OR "during the preparation of this paper" OR "during the preparation of this article" OR "in the preparation of this manuscript" OR "in the writing of this manuscript" OR "in the writing of this paper" OR "in preparing this manuscript" OR "in the writing process" |
| G5 | exact list | "full responsibility for the content" OR "take full responsibility for" OR "takes full responsibility for" OR "reviewed and edited the content as needed" |
| G6 | exact list | "did not use any AI" OR "no AI tools were used" OR "not use generative AI" OR "without the use of generative AI" OR "no generative AI" OR "did not use generative AI" OR "not used any AI" OR "no AI-assisted" OR "have not used AI" OR "did not use AI" |
| G4 | exact list AND stemmed tool list (weak) | ("language polishing" OR "polish the language" OR "polish the writing" OR "polish the manuscript" OR "improve the readability" OR "improve readability" OR "improve the language" OR "language editing" OR "grammar checking" OR "proofreading" OR "language refinement" OR "linguistic polishing" OR "improve the clarity" OR "enhance the readability" OR "language and readability") with `,fulltext.search:(ChatGPT OR GPT OR "language model" OR LLM OR "generative AI" OR "AI tool" OR "AI-assisted" OR Gemini OR Claude OR Copilot OR DeepSeek OR "artificial intelligence")` |

Candidates: V1–V3 = any of S1, S2, S2a, S3, S3a, S3b, S3c, S4, S6, S7, T2x, G1, G2, G3, G5, G6. V4, V5 = the narrower rule in 2.4. The index does not always match a phrase that is in the text (the exact phrase "during the preparation of this work" returned 0 for a V1 paper that contains it with a capital D; the stemmed S3a found it), which is why several overlapping phrases were used.

### 5.3 Reading and samples

- OpenAlex cached copies: `https://content.openalex.org/works/<id>.grobid-xml` (54 files; V1 and V3). Each file was parsed to sections; every sentence of the back matter that names a tool, and every body sentence that names a tool together with a writing word, was read; the last fifth of each sampled paper was scanned a second time for "we / the authors used <tool>".
- Springer pages: `https://link.springer.com/article/<doi>` (V2) and `https://link.springer.com/chapter/<doi>` (V4), one plain request each at about one request per second. Two pattern passes over the sections of each page; the patterns (tool words, including Grok, DeepL, QuillBot, Paperpal, "AI", "language model", case-insensitive) are in the working scripts.
- Other copies: the open URL listed by OpenAlex (arXiv, ACL Anthology, CEUR-WS, journal sites), one plain request each; Europe PMC `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML`.
- V4 sample: `https://api.openalex.org/works?filter=primary_location.source.id:S2764900261,publication_year:<year>,type:conference-paper&sample=60&seed=20261115&per-page=200`, for each year 2023–2026.
- V1 reading frame (all read): 2023: W4320913231 W4321202326 W4383501006; 2024: W4391112959 W4396620548 W4401477554 W4401651506 W4402737984; 2025: W4406444944 W4410384083 W4416266490 W4416375729 W4416425409; 2026: W4405626817 W4407246823 W4415273197 W7125712333 W7128495137 W7131219055 W7160063674 W7164751638 W7204025187 W7220421083 W7220918838 W7225162535.
- V3 draw (seed 20261115 + year): 2023: W4388863148 W4372348768 W4386098783 W4385065630 W3202020111; 2024: W4391897129 W4394691924 W4391402376 W4394844604 W4393992782; 2025: W4412196109 W4412162046 W4412519200 W4409944764 W4415542893; 2026: W7202168129 W7223108858 W7220691620 W7221757188 W7223449029.
- V2 draw (seed 20261115 + year; DOI suffix after `10.1007/s10579-`): 2023: 023-09704-w 023-09684-x 023-09705-9 023-09655-2 023-09656-1 023-09658-z 023-09695-8 023-09654-3 023-09698-5 023-09643-6 023-09648-1 023-09646-3 023-09637-4 023-09671-2 022-09631-2 023-09673-0 023-09700-0 023-09638-3 023-09652-5 023-09689-6 023-09678-9 023-09686-9 023-09677-w 023-09668-x 023-09641-8; 2024: 023-09709-5 023-09718-4 024-09726-y 023-09711-x 024-09743-x 024-09722-2 024-09734-y 024-09769-1 024-09738-8 023-09717-5 024-09799-9 024-09777-1 024-09758-4 024-09757-5 024-09792-2 024-09771-7 024-09791-3 024-09744-w 024-09751-x 024-09721-3 024-09774-4 024-09793-1 024-09789-x 024-09736-w 024-09754-8; 2025: 025-09822-7 025-09851-2 025-09839-y 025-09852-1 025-09809-4 025-09858-9 025-09826-3 025-09828-1 025-09871-y 025-09813-8 025-09819-2 025-09850-3 025-09848-x 025-09869-6 025-09862-z 025-09821-8 025-09866-9 025-09833-4 025-09812-9 025-09864-x 025-09832-5 025-09854-z 025-09884-7 025-09831-6 025-09844-1; 2026: 026-09926-8 026-09939-3 026-09921-z 026-09929-5 026-09955-3 026-09911-1 026-09905-z 026-09936-6 025-09876-7 026-09956-2 025-09881-w 026-09925-9 026-09922-y 026-09931-x 025-09888-3 025-09887-4 025-09879-4 025-09882-9 026-09928-6 026-09907-x 025-09901-9 026-09914-y 025-09896-3 025-09875-8.
- Semantic Scholar snippet search (`https://api.semanticscholar.org/graph/v1/snippet/search`, with `venue=` and `year=`, limit 1000, through the shared queue script) was tried as a second index for V1–V3 with five declaration-like queries per venue and year (74 of 75 calls answered). It returned body text for few papers (V1 2023–2026: 19 papers; V3 2023: none) and none of the statements already known from V1 and V2, so its text does not hold the end matter of these papers. It is not a valid check and no number in this file depends on it.

## 6. Limits

**What could not be read, and why**

- **ScienceDirect (V1) and the ACM Digital Library (V3)** answered HTTP 403 to a plain request. No bot check, login or paywall was worked around and no browser profile was used. So for V1 the statement could be looked for in 49 of 548 papers of 2023–2026 (9%), and for V3 in 401 of 674 (59%; V3 2024: 64 of 178, 2026: 15 of 87).
- **The papers with searchable full text are the open-access ones.** Authors who pay for open access, or who post preprints, may differ from the others in how often they declare. The share found in this subset is not an estimate for the whole journal.
- **V1 publisher copies: 25 in four years.** 4 of 25 is a count, not a stable rate; with 12 papers in 2026 one paper moves the share by 8 points.
- **V3 sample: 5 per year**, because each cached file costs 1% of the daily OpenAlex allowance. It checks the index; it does not estimate a rate.
- **V2 and V4 paywalled papers**: only the end matter is public. A statement placed in the methods or in a footnote of a paywalled paper is not visible. For V2 this affects 183 of 311 papers of 2023–2026.
- **V4** is covered by the index (9% of works have searchable full text) and by 240 sampled pages out of 36689 works. Single conferences inside the series may ask for a statement and others not: the 23 verified V4 declarations come from 16 volumes, and 10 of them from the 3 volumes that have more than one. The series-wide count says little about one conference.
- **V5**: publisher PDFs on MDPI, PeerJ and MIT Press Direct returned HTTP 403; ScienceDirect, Wiley and SSRN were not attempted. Works with no open copy are searched in title, abstract and keywords only. No sample was read for V5.
- **Parsed text.** Cached copies are machine-parsed PDFs. A statement in a footnote, a margin box or a first-page note can be lost in parsing. Quotes are copied from the parsed text and can carry its artefacts (a footnote digit glued to a word, a lost ligature).
- **Pre-proofs and preprints.** Three V1 statements were read in copies marked "Journal Pre-proof"; the final typeset version was not compared. Statements read in preprints are counted in their own column.
- **Phrase lists.** A declaration that uses none of the listed wordings is found only where pages or copies were read in full (V2 all pages; V1 25 copies; V3 20 copies; V4 240 pages). One V2 statement of no use was found only on the second, broader pass.
- **First-author surnames** in the evidence file are the last word of the OpenAlex author name and were not checked against the papers.
- **2026 is incomplete** (to mid-November) and OpenAlex assigns some in-press papers to the year of the issue.

**What the numbers do not show**

- A paper without a statement is not evidence that no tool was used. The counts measure disclosure, not use. One open-access V2 paper of 2026 with no AI statement has, in its notes, a link that ends in `utm_source=chatgpt.com`; that shows a chat tool was used to find a link, not that any text was written with it, and it is not counted.
- A statement of "language editing only" is the authors' own description; nothing here checks it.
- The counts say nothing about whether a journal enforced its policy, or about how editors or reviewers treated papers with or without a statement.
- Absence in 2023–2024 does not show that statements were not required then; it shows that none was found in the text that could be read.
- Papers that use a language model inside the research (as a baseline, annotator or generator) describe that use in their methods; those are not counted here as declarations, although a publisher's policy may also cover them.

## 7. Policy sentences

The publishers' and venues' policy sentences on AI disclosure are not re-derived here. See `manuscript/cfp/VENUE_RECHECK_2026-11-15.md`.
