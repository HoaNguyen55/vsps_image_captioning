# Paper C: dated systematic search for analyses of in-context and retrieval-augmented image captioning

Item C-N15 of fix package v1 (second half); answer F6, option (a), of the corresponding author. This file proposes text only. It changes no paper file and is not a package.

## Part 1. Protocol (written 2026-11-15T02:14Z, before the first query of this search)

Lookups made earlier today for the full-text check (`RELATED_FULLTEXT_CHECK_2026-11-15.md`: known works fetched by DOI or arXiv id) are not part of this search. No search query on this topic was sent before this part was written.

### 1.1 Question

The search is meant to test, not to support, this sentence of Paper C (`01_introduction.md` l.9; in the conference version, paragraph `p:S1-02`):

> As far as these papers state, none preregisters its contrasts or reports confidence intervals on the captioning score. [conference version adds:] and none covers Vietnamese.

"These papers" are the analyses of Table 1b (Yang et al. 2023; W. Li et al. 2024; Baldassini et al. 2024; S. Chen et al. 2025; L. Li et al. 2025/2026; MUNIChus, Chen et al. 2026).

Two questions:
- Q-A. Which studies, dated 2021-01-01 to 2026-11-15, analyse in-context examples or retrieval augmentation for image captioning and are missing from Paper C Table 1, Table 1b and the conference Table 1?
- Q-B. Does any study of in-context or retrieval-augmented image captioning in that window (a) preregister its hypotheses or contrasts, (b) report confidence intervals on a caption score, or (c) include Vietnamese?

A work answers Q-B "yes" and contradicts the sentence if it passes the criteria below and its full text states (a), (b) or (c). Standard deviations, standard errors and significance tests on a caption score are not confidence intervals; they are recorded in their own column and reported, because they bear on how the sentence should be worded.

### 1.2 Inclusion criteria (all of I1 to I3, and one of the classes of I4)

- I1. Publication or first posting date from 2021-01-01 to 2026-11-15.
- I2. The work evaluates image captioning: text describing a still image, scored with a caption metric. Remote-sensing and news image captioning count.
- I3. At inference the captioner is given examples or retrieved material: in-context demonstrations in a prompt, or retrieved captions, image-caption pairs or concepts.
- I4. One of three classes:
  - P-A (analysis): the work compares conditions of example selection or retrieval for captioning (for instance similar against random examples, order, number, corrupted retrieval), or sets out to explain why or when such examples help. Candidates for Table 1b and the conference Table 1.
  - P-B (closest design): a training-free captioner that puts retrieved examples into the prompt of a language or multimodal model. Candidates for Table 1.
  - P-C (watch list for Q-B): any work meeting I1 to I3 whose title or abstract names Vietnamese, a preregistration, or confidence or bootstrap intervals.

### 1.3 Exclusion criteria

- E1. Not image captioning in the sense of I2: video or audio captioning only; visual question answering or classification only; radiology or medical report generation; text-only tasks; image generation.
- E2. No examples or retrieved material at inference (fine-tuning or architecture work only).
- E3. A trained retrieval-augmented captioner with no analysis of example selection (class X-M). Counted, not tabulated: Table 1 already shows this design through SmallCap, EXTRA, EVCap and CONCAP.
- E4. Surveys and position papers without own captioning experiments. Counted.
- E5. Duplicates: a preprint and its published version are one work.
- E6. Work of this group.
- E7. Full text not in English.

### 1.4 Sources

1. OpenAlex, `https://api.openalex.org/works`, with the group's key sent as a query parameter read from its file by curl (never printed, logged or written to a file) and `mailto=vsps-research@example.org`. Budget: at most 1,500 credits. Credit use is read from the response headers; if no header reports it, each list call is counted as 10 credits and each single-work lookup as 1. No cached full-text download is requested from OpenAlex.
2. arXiv, `https://export.arxiv.org/api/query`, at least 3 seconds between calls.
3. Semantic Scholar, only through `~/.config/vsps/s2get.sh` (bulk search endpoint).
4. ACL Anthology search page, one request; if it does not return results to a plain request, that is recorded and the Anthology is covered through the three sources above.

Full texts for the last screening step: open copies only (arXiv, proceedings, anthology). A site that answers an automated read with a refusal is left alone after one request and the work is marked NOT READ.

### 1.5 Query strings (fixed here; sent exactly as written)

Date window in every query: 2021-01-01 to 2026-11-15.

OpenAlex, filter `title_and_abstract.search`, plus `from_publication_date:2021-01-01,to_publication_date:2026-11-15`; 200 records per page, relevance order, at most 3 pages per query:
- OA-1: `("image captioning" OR "image caption") AND ("in-context learning" OR "in-context examples" OR "in-context example" OR "in-context demonstrations" OR "few-shot prompting")`
- OA-2: `("image captioning" OR "image caption") AND ("retrieval-augmented" OR "retrieval augmented" OR "retrieved captions" OR "retrieval-based")`
- OA-3: `captioning AND ("example selection" OR "demonstration selection" OR "in-context example selection" OR "RICES")`
- OA-4: `("multimodal in-context learning" OR "multimodal in-context") AND (captioning OR caption)`
- OA-5: `("image captioning" OR "image caption") AND Vietnamese`
- OA-6: `("image captioning" OR "image caption") AND (preregistered OR "pre-registered" OR preregistration OR "registered report")`
- OA-7: `("image captioning" OR "image caption") AND ("in-context" OR "retrieval-augmented" OR "retrieval augmented" OR "few-shot") AND ("confidence interval" OR "confidence intervals" OR bootstrap)`
- OA-8: `("image captioning" OR "image caption") AND (multilingual OR "low-resource") AND ("in-context" OR "retrieval-augmented" OR "retrieval augmented" OR "few-shot")`

OpenAlex, citing works of seven seed papers (filter `cites:<id>`, plus `title_and_abstract.search:caption OR captioning`, same dates, at most 2 pages each). The seeds are looked up by DOI or title:
- OA-C1 Yang et al. 2023 (doi 10.52202/075280-1782, or its arXiv record); OA-C2 W. Li et al. 2024 (doi 10.18653/v1/2024.acl-long.503); OA-C3 Baldassini et al. 2024 (doi 10.1109/CVPRW63382.2024.00161); OA-C4 S. Chen et al. 2025 (arXiv 2507.15807); OA-C5 L. Li et al. (doi 10.1109/TPAMI.2026.3719106); OA-C6 Chen et al. 2026, MUNIChus (doi 10.63317/3cu2uxnphh3g); OA-C7 Ramos et al. 2023, SmallCap (looked up by title "SmallCap: Lightweight Image Captioning Prompted with Retrieval Augmentation").

arXiv, `search_query`, each with `AND submittedDate:[202101010000 TO 202611152359]`; 200 records per call, relevance order, at most 2 calls per query:
- AX-1: `abs:"image captioning" AND (abs:"in-context" OR abs:"few-shot") AND (abs:retrieval OR abs:retrieved OR abs:"example selection" OR abs:demonstrations)`
- AX-2: `abs:"image captioning" AND (abs:"retrieval-augmented" OR abs:"retrieval augmented")`
- AX-3: `abs:captioning AND (abs:"in-context learning" OR abs:"in-context examples" OR abs:"multimodal in-context")`
- AX-4: `abs:captioning AND abs:Vietnamese`
- AX-5: `abs:captioning AND (abs:preregistered OR abs:"pre-registered" OR abs:preregistration)`
- AX-6: `abs:"image captioning" AND (abs:"in-context" OR abs:"retrieval-augmented" OR abs:"few-shot") AND (abs:"confidence interval" OR abs:"confidence intervals" OR abs:bootstrap)`

Semantic Scholar bulk search (`/graph/v1/paper/search/bulk`, `year=2021-2026`, fields title, year, venue, externalIds, abstract, publicationDate; one page of up to 1,000 records per query):
- S2-1: `("image captioning" | "image caption") + ("in-context" | "few-shot") + (retrieval | retrieved | "example selection" | demonstrations)`
- S2-2: `("image captioning" | "image caption") + ("retrieval-augmented" | "retrieval augmented")`
- S2-3: `captioning + ("multimodal in-context" | "in-context learning" | "in-context examples")`
- S2-4: `("image captioning" | "image caption") + Vietnamese`
- S2-5: `("image captioning" | "image caption") + (preregistered | "pre-registered" | preregistration)`
- S2-6: `("image captioning" | "image caption") + ("in-context" | "retrieval-augmented" | "few-shot") + ("confidence interval" | "confidence intervals" | bootstrap)`

ACL Anthology: `https://aclanthology.org/search/?q=in-context+image+captioning`.

### 1.6 Screening steps

0. Merge the records of all queries; remove duplicates by DOI, arXiv id, then normalised title.
1. Title screen. A record passes if its title or abstract contains "caption" and its title or abstract contains one of: in-context, few-shot, retriev, demonstration, example selection, exemplar, prompt; this first pass is by script. The titles that pass are then read, and a record is dropped only if the title alone shows E1 (video, audio, report generation, generation of images), E4 or E6.
2. Abstract screen, by reading: I1 to I4 and E1 to E7. Every record gets one code: P-A, P-B, P-C, or the exclusion code. A record with no abstract in any source is kept for step 3 if its title passes.
3. Full text, for every work that passed step 2 and is not already in the tables: the cells of Table 1 (trained; sees the image; retrieved content; languages; random control; statistics) and of Table 1b (registered; confidence intervals on the caption score), each with the place in the paper and a quote of at most 25 words, or NOT READ with the reason. The terms "preregist", "pre-regist", "registered", "confidence interval", "bootstrap", "standard deviation", "std", "±", "seed", "p-value", "error bar", "Vietnam" are counted in each full text.

"Already in the tables" is decided against Paper C at `9b8e6ae` (Table 1, Table 1b, and the citations of `02_related_work.md` through `paperC.bib`) and the conference `draft_v1` (Table 1).

### 1.7 Stop rules and limits

- OpenAlex: stop at 1,500 credits; whatever was not run is listed.
- Per-query caps as given in 1.5; if a query has more hits than its cap, the total is recorded and the rest is not screened.
- The search covers titles and abstracts in three indexes. It does not search full texts, so a work that mentions captioning only in its body can be missed. Works not indexed in any of the three sources are missed.

### 1.8 What will be reported

Per source and query: the string as sent without any key, the UTC time, the number of hits, the number of records fetched; then the counts at each screening step, the table of works that passed the abstract screen, the works to add to the tables, any work that contradicts the sentence, and wording if the sentence must be narrowed. Deviations from this protocol are listed with the time and the reason.

## Part 2. Run log

(filled in below as the search runs)

Everything above this line is the protocol as it stood before the first query: the first 11,025 bytes of this file have sha256 `258617e91dc036401b7e2910307b8d00ad1ffe84acbfbf385129551f8079c28f`. A read-only copy with that sha was made at 2026-11-15T02:24:13Z, just before the first query went out in the same second. The text below was appended after the search; nothing above was edited.

### 2.1 Queries as sent (all on 2026-11-15, UTC; no key is part of any string below)

Every OpenAlex list call also carried `per-page=200`, `page=1`, a `select` list of fields and `mailto=vsps-research@example.org`. No query reached its cap, so every hit of every query was fetched: hits and fetched are the same number in each row.

| time | source | id | query string as sent | hits = fetched |
|---|---|---|---|---|
| 02:24:13 | OpenAlex | OA-1 | `filter=title_and_abstract.search:("image captioning" OR "image caption") AND ("in-context learning" OR "in-context examples" OR "in-context example" OR "in-context demonstrations" OR "few-shot prompting"),from_publication_date:2021-01-01,to_publication_date:2026-11-15` | 24 |
| 02:24:25 | OpenAlex | OA-2 | `filter=title_and_abstract.search:("image captioning" OR "image caption") AND ("retrieval-augmented" OR "retrieval augmented" OR "retrieved captions" OR "retrieval-based"),` same two date filters | 154 |
| 02:24:27 | OpenAlex | OA-3 | `filter=title_and_abstract.search:captioning AND ("example selection" OR "demonstration selection" OR "in-context example selection" OR "RICES"),` same dates | 1 |
| 02:24:29 | OpenAlex | OA-4 | `filter=title_and_abstract.search:("multimodal in-context learning" OR "multimodal in-context") AND (captioning OR caption),` same dates | 14 |
| 02:24:31 | OpenAlex | OA-5 | `filter=title_and_abstract.search:("image captioning" OR "image caption") AND Vietnamese,` same dates | 23 |
| 02:24:33 | OpenAlex | OA-6 | `filter=title_and_abstract.search:("image captioning" OR "image caption") AND (preregistered OR "pre-registered" OR preregistration OR "registered report"),` same dates | 1 |
| 02:24:34 | OpenAlex | OA-7 | `filter=title_and_abstract.search:("image captioning" OR "image caption") AND ("in-context" OR "retrieval-augmented" OR "retrieval augmented" OR "few-shot") AND ("confidence interval" OR "confidence intervals" OR bootstrap),` same dates | 0 |
| 02:24:35 | OpenAlex | OA-8 | `filter=title_and_abstract.search:("image captioning" OR "image caption") AND (multilingual OR "low-resource") AND ("in-context" OR "retrieval-augmented" OR "retrieval augmented" OR "few-shot"),` same dates | 11 |
| 02:24:52 to 02:25:02 | OpenAlex | seeds | seven single-work lookups `works/doi:<doi>` for the seeds of 1.5 (the first seed by both of its DOIs), and one list call `filter=title.search:"SmallCap: Lightweight Image Captioning Prompted with Retrieval Augmentation"` | 1 each |
| 02:25:07 | OpenAlex | OA-C1 | `filter=cites:W7133264890,title_and_abstract.search:caption OR captioning,` same dates (Yang et al. 2023) | 11 |
| 02:25:09 | OpenAlex | OA-C2 | `filter=cites:W4402671679,` same search and dates (W. Li et al. 2024) | 12 |
| 02:25:11 | OpenAlex | OA-C3 | `filter=cites:W4402903971,` same (Baldassini et al. 2024) | 8 |
| 02:25:13 | OpenAlex | OA-C4 | `filter=cites:W4417438318,` same (S. Chen et al. 2025) | 0 |
| 02:25:14 | OpenAlex | OA-C5 | `filter=cites:W7172047923,` same (L. Li et al., TPAMI) | 0 |
| 02:25:16 | OpenAlex | OA-C6 | `filter=cites:W7160108228,` same (MUNIChus) | 0 |
| 02:25:17 | OpenAlex | OA-C7 | `filter=cites:W4386076004,` same (SmallCap) | 101 |
| 02:25:30 | arXiv | AX-1 | `search_query=abs:"image captioning" AND (abs:"in-context" OR abs:"few-shot") AND (abs:retrieval OR abs:retrieved OR abs:"example selection" OR abs:demonstrations) AND submittedDate:[202101010000 TO 202611152359]`, `start=0`, `max_results=200`, `sortBy=relevance` | 153 |
| 02:25:35 | arXiv | AX-2 | `abs:"image captioning" AND (abs:"retrieval-augmented" OR abs:"retrieval augmented") AND submittedDate:[…]` (same window) | 43 |
| 02:25:39 | arXiv | AX-3 | `abs:captioning AND (abs:"in-context learning" OR abs:"in-context examples" OR abs:"multimodal in-context") AND submittedDate:[…]` | 61 |
| 02:25:44 | arXiv | AX-4 | `abs:captioning AND abs:Vietnamese AND submittedDate:[…]` | 7 |
| 02:25:51 | arXiv | AX-5 | `abs:captioning AND (abs:preregistered OR abs:"pre-registered" OR abs:preregistration) AND submittedDate:[…]` | 4 |
| 02:25:55 | arXiv | AX-6 | `abs:"image captioning" AND (abs:"in-context" OR abs:"retrieval-augmented" OR abs:"few-shot") AND (abs:"confidence interval" OR abs:"confidence intervals" OR abs:bootstrap) AND submittedDate:[…]` | 2 |
| 02:26:12 | Semantic Scholar | S2-1 | bulk search, `query=("image captioning" \| "image caption") + ("in-context" \| "few-shot") + (retrieval \| retrieved \| "example selection" \| demonstrations)`, `year=2021-2026` | 137 |
| 02:26:14 | Semantic Scholar | S2-2 | `("image captioning" \| "image caption") + ("retrieval-augmented" \| "retrieval augmented")` | 76 |
| 02:26:17 | Semantic Scholar | S2-3 | `captioning + ("multimodal in-context" \| "in-context learning" \| "in-context examples")` | 94 |
| 02:26:35 | Semantic Scholar | S2-4 | `("image captioning" \| "image caption") + Vietnamese` | 19 |
| 02:26:37 | Semantic Scholar | S2-5 | `("image captioning" \| "image caption") + (preregistered \| "pre-registered" \| preregistration)` | 0 |
| 02:26:45, again 02:28:02 | Semantic Scholar | S2-6 | `("image captioning" \| "image caption") + ("in-context" \| "retrieval-augmented" \| "few-shot") + ("confidence interval" \| "confidence intervals" \| bootstrap)`; the first attempt ended with HTTP 429 after the helper's retries, the second answered | 2 |
| 02:27:18 | ACL Anthology | ACL-1 | `https://aclanthology.org/search/?q=in-context+image+captioning` | none: HTTP 200, a page shell with a client-side search widget and no result row |

Records fetched: OpenAlex 360 (OA-1 to OA-8: 228; OA-C1 to OA-C7: 132), arXiv 270, Semantic Scholar 328; 958 in all.

OpenAlex credits: 16 list calls at 10 credits each, 160 credits; the single-work lookups cost 0. The response headers gave 2,644 credits remaining after the first call and 2,494 after the last list call. The budget of 1,500 was not reached, and no planned query was left out. A check by script found the key string in no file of the work folder and not in this file.

Requests of step 3, which are not search queries: one OpenAlex single-work lookup (02:38:58, 0 credits) and two Semantic Scholar title matches (02:38:59, 02:39:00) to find open copies of three shared-task papers; two arXiv title searches for an open copy of one ACM paper (none found); one request to doi.org for a journal paper; one request to the MDPI site (answered HTTP 403, not repeated); and 17 PDF downloads of open copies (arXiv 11, ACL Anthology 2, CEUR-WS 2, one institutional open archive, one open-access journal site).

### 2.2 Deviations from the protocol

- D1 (02:28:02). S2-6 was sent a second time with the same string, because the first attempt was refused for rate (HTTP 429).
- D2 (step 1). 86 records have no abstract in any source. The script passed 19 of them on the title alone and dropped 67. The titles of the 67 were read as well, and 15 were carried to step 2 by hand (titles that show retrieval or in-context captioning, or Vietnamese captioning). This only adds records.
- D3 (step 2). The 214 abstracts were read in a condensed view: the sentences that name captioning, in-context examples, retrieval, random selection, training, analysis, Vietnamese, registration or intervals. The whole abstract was read where that view left the code open. A record misjudged from this view can have been excluded wrongly.
- D4 (step 2). One exclusion code was added, X-K: the work retrieves knowledge (news articles, encyclopaedia pages, a knowledge graph, attribute tables) for entity-aware, news or art captioning and has no analysis of example selection. Class P-A was also given to benchmark studies that test retrieval augmentation for captioning against control contexts.
- D5 (step 2). Records without abstract whose titles show a trained retrieval-augmented captioner of the SmallCap line were coded E3 from the title and were not fetched.
- D6 (step 3). Full texts were not read from first to last page. Each was searched for the terms of 1.6 and read in the passages that settle each cell; the table says "read in the passages cited".
- D7 (02:26). Paper C moved from `9b8e6ae` to `55315ca` while the search ran (the related-work corrections of the full-text check were committed). The rows of Table 1 and Table 1b are the same works at both commits; one row label lost the words "from the abstract". Line numbers in Part 5 refer to `55315ca`.

## Part 3. Counts at each screening step

| step | in | out | left |
|---|---|---|---|
| records fetched | – | – | 958 |
| 0. duplicates removed | 958 | 384 | 574 unique works |
| 1. title screen | 574 | 360: script 175 (no "caption", or no method term, in title and abstract); E1 by title 151; E4 by title 22; E5 duplicate 11; not a research paper 1 | 214 |
| 2. abstract screen | 214 | 170: E1 21; E2 61; E3 (X-M) 69; X-K 15; E5 3; E7 1 | 44: 21 already in Paper C's bibliography, 23 new (P-A 12, P-B 8, P-C 3) |
| 3. full text of the 23 new works | 23 | 6 not read (no open copy, or the site refuses automated reads) | 17 read in the passages cited; 4 of them fall out on the full text (E3: 3; no caption score: 1) |

Watch-list queries for registration and intervals (OA-6, OA-7, AX-5, AX-6, S2-5, S2-6): 8 unique records. All 8 were dropped by the step-1 script and were read all the same. None is a study of in-context or retrieval-augmented image captioning:
- a music-generation paper (bootstrap intervals on a music metric);
- a data deposit for two preregistered studies of image-text verification on COCO image-caption pairs (doi 10.5281/zenodo.23810710): verification, not caption generation, and no in-context examples or retrieval;
- Concadia (arXiv 2104.08376, 2021), on image descriptions and captions, with a preregistered human-subjects experiment and no in-context examples or retrieval;
- a chart-perception study and a text-only language-model study, each preregistered;
- three records where "bootstrap" is the web framework or means "to start up" (a captioning web application, a synthetic-data captioner, a satellite-image model).

So registration does occur near this field (the second and third items), but in no study of in-context or retrieval-augmented captioning that the queries returned.

Vietnamese queries (OA-5, AX-4, S2-4): 26 unique records. 17 have no method term in title or abstract (data sets, trained captioners and shared-task systems for Vietnamese, and unrelated work); 2 are another task by title; 1 is a duplicate; 3 are trained Vietnamese models with no examples at inference (E2); 3 are already cited in Paper C (VELVET, UIT-OpenViIC, HDUCap). None uses in-context examples or retrieval at inference.

## Part 4. Works that passed the abstract screen

### 4.1 Already in Paper C (21)

| work (key in `paperC.bib`) | found by | where in Paper C |
|---|---|---|
| Yang2023ICLConfig | AX-3, OA-1, S2-3 | Table 1, Table 1b, conference Table 1 |
| Li2024RetrievalRobustness | AX-2, OA-2, S2-2 | Table 1, Table 1b, conference Table 1 |
| Li2025UnveilingICL | AX-1, AX-3, OA-1, OA-4, OA-C1, OA-C3, S2-1, S2-3 | Table 1b, conference Table 1 |
| Ramos2023EXTRA; Li2024EVCap; Sarto2024RetrievalArch | AX-2, OA-2, S2-2 (the first two also OA-C7) | Table 1 |
| Ramos2023LMCap; Ibrahim2025CONCAP; Rebelo2025RSCap | OA-2, OA-8, S2-2 and others | Table 1 |
| Zeng2024MeaCap; Fei2023ViECap | OA-C7 only | Table 1 |
| Bazi2025RAGCap | OA-2, S2-2 | Table 1 |
| Yang2023ReViLM; Lu2025NES; Thanh2026Adjudicated; Dhawan2026Gators | OA-2 and others | cited in Section 2, no table row |
| Allabadi2026GRIP; dosSantos2025ContextVLM | AX-1, AX-3, S2-1, S2-3 (GRIP also OA-4) | cited, no table row |
| Vu2025VELVET; Bui2023OpenViIC; Hoang2026HDUCap | S2-4 (all three); AX-4 (UIT-OpenViIC); OA-5 (HDUCap) | cited, no table row |

Recall against the tables' own rows. 17 prior works have a row in Table 1 or Table 1b. The queries retrieved 12 of them. They did not retrieve SmallCap, OpenFlamingo, Baldassini et al. 2024, S. Chen et al. 2025 or MUNIChus. Of the six analyses of Table 1b, three were retrieved (Yang et al., W. Li et al., L. Li et al.). This is the measured limit of this search: half of the known analyses were missed by a title-and-abstract search with these strings, and an unknown analysis of the same kind would be missed in the same way.

### 4.2 New works (23)

Cells: T = captioner trained; I = sees the image; R = retrieved content or examples; L = languages; C = random control; S = statistics on the caption score; G = registered; CI = confidence intervals on the caption score. "0 hits" refers to the counted terms of 1.6 in the whole text. Every quote of four words or more was matched by script against the page of the PDF named in the row.

| # | work | class | found by | version read (first 12 hex digits of the PDF's sha256) | cells, with place and quote |
|---|---|---|---|---|---|
| N1 | Sharifymoghaddam, Upadhyay, Chen, Lin. UniRAG: Universal Retrieval Augmentation for Large Vision Language Models. Findings of NAACL 2025 by the index record (doi 10.18653/v1/2025.findings-naacl.108); arXiv 2405.10311 | P-B | AX-1, AX-2, S2-1 | arXiv v3 (07865525fe56), read in the passages cited | T: no; off-the-shelf models (LLaVA, GPT-4o, Gemini-Pro) get examples at inference, and the retrievers are trained models (p. 2). I: yes. R: image-caption pairs as in-context examples, k ∈ {0, 1, 5} (p. 5). L: English, p. 9: "This work uses the English-only MSCOCO and Fashion200k datasets for evaluation". C: yes, at equal k, p. 3: "random selection of queries and their ground-truth candidates from the dataset (baseline 2)". Result, p. 7: "for Gemini-Pro, random few-shot examples significantly enhance the quality of generated captions, although they are still less effective than few-shot retrieved examples"; for the other two models, five random examples score below zero-shot (p. 7). S: none on caption scores. G: no (0 hits). CI: no; the one hit of "confidence interval" (p. 8) is in the image-generation results |
| N2 | Freitas, Bosco, Lotufo, Pereira, Carmo. Retrieval Augmented Generation and Patch-Level Explainability applied to Medical Image Captioning with Small Visual Language Models. CLEF 2026 Working Notes, CEUR-WS Vol-4283, paper 255 | P-B, with a P-A comparison | S2-1, S2-2 | proceedings PDF (adc23d6bcde1), read in the passages cited | T: no for two of the three model configurations; the third is fine-tuned (p. 2). I: yes. R: captions as text, k = 3, p. 2: "injecting the captions of the three most visually similar training images into the prompt". L: not named ("English": 0 hits); radiology captions of ROCOv2. C: yes, equal k = 3, p. 2: "The random few-shot strategy injects three randomly selected captions from the training dataset before the query image". Result, p. 7: "RAG-based prompting consistently outperforms simpler strategies within each model family". S: none (0 hits). G: no; the one hit of "registered" is the team's registration on the task platform. CI: no |
| N3 | Xiang, Nakashima, Garcia. Gender Bias in Vision-Language In-Context Learning. arXiv 2609.27682; a Springer chapter by the index record (doi 10.1007/978-3-032-37086-0_16) | P-A | AX-1, AX-3, OA-1, OA-C3, S2-1, S2-3 | arXiv v2 (9348711ae2a6), read in the passages cited | T: no. I: yes. R: image-text demonstrations; random sampling (p. 3) and two similarity-based retrieval settings, the latter on the COCO captioning subset only (p. 8); six models. L: not named; COCO and DCI captions. C: yes, p. 2: "Similarity-based retrieval methods inherit demographic imbalances from their source pool and offer no debiasing advantage over random selection". Outcome studied: gender bias; caption quality (BLEU, CLIPScore) is reported beside it, p. 2: "Standard caption quality metrics remain stable even as gender bias shifts substantially". S: mean ± standard deviation on the bias measure and on BLEU and CLIPScore in the random-sampling rows (for instance Table 30, p. 40), p. 8: "we run each experiment five times using independently sampled in-context sequences"; the retrieval rows are run once. G: no (0 hits). CI: no (0 hits) |
| N4 | Zong, Bohdal, Hospedales. VL-ICL Bench: The Devil in the Details of Multimodal In-Context Learning. ICLR 2025; arXiv 2403.13164 | P-A | AX-3, OA-1, OA-4, S2-3 | arXiv v4 (d03a4c78f1fd), read in the passages cited | T: no. I: yes. R: image-text demonstrations, 0 to 8 shots; COCO captioning as a side check (Table 15, p. 30). L: not named. C: no for captioning (random examples only); similarity-based selection is tested on three other tasks (pp. 25 to 27). Finding, Fig. 3, p. 4: "VQA and Captioning are poor benchmarks for image-to-text ICL". S: p. 7: "All experiments are conducted using three different random seeds and we report the average performance". G: no (0 hits). CI: no (0 hits) |
| N5 | Yang, Peng, Ma, Xu, Zhang, Han, Zhang. Lever LM: Configuring In-Context Sequence to Lever Large Vision Language Models. NeurIPS 2024 (doi 10.52202/079017-3185); arXiv 2312.10104. A second record, "ICD-LM", is the same work | P-A (a learned selector with random and similarity baselines) | AX-1, S2-1 | arXiv v4 (da285651095f), read in the passages cited | T: a small selector model is trained; the vision-language model is not. I: yes. R: image-caption demonstrations. L: not named; COCO. C: yes, a random baseline and similarity-based baselines at equal shots (Section 4.2.1, p. 6); p. 6: "In IC, Lever-LM outperforms the best baseline, SIIR, by 6.03 (84.32 vs. 78.29) CIDEr on OpenFlamingo". S: no SD (0 hits); p. 17: "we use OpenFlamingo to randomly select 3 sets of k-shot ICD sequences with different seeds for the image captioning task". G: no (0 hits). CI: no (0 hits) |
| N6 | Ramos, Bugliarello, Martins, Elliott. PAELLA: Parameter-Efficient Lightweight Language-Agnostic Captioning Model. Findings of NAACL 2024 (2024.findings-naacl.225) | P-C | OA-2 | anthology PDF (a534d686460b), read in the passages cited | T: yes (a mapping network). I: yes; R: captions, p. 1: "conditioned on two types of input: (i) the image itself, and (ii) a set of retrieved captions in the target language". L: 36, Vietnamese among them: Table 9, p. 16, has a column "vi"; its caption: "CIDEr results on the XM3600 benchmark across the 36 languages, ordered by the pre-training language ratio of the XGLM decoder". C: no. S: none (0 hits). G: no. CI: no |
| N7 | Futeral et al. mOSCAR: A Large-scale Multilingual and Multimodal Document-level Corpus. arXiv 2406.08707 | P-C | AX-3, S2-3 | arXiv (50fc6c2d7eb7), read in the passages cited | A corpus, and a model trained on it that is tested with 0, 4, 8 and 16 shots (tables on pp. 7 and 8). L: captioning on xFlickr&CO and XM3600, p. 7: "We also include Crossmodal3600 (XM3600) (Thapliyal et al., 2022) and MaXM (Changpinyo et al., 2022) as they cover a broader range of languages"; the language list of XM3600 on p. 28 names Vietnamese. How the shots are chosen was not found in the passages read. C: no. S: ± only on corpus statistics (p. 5). G: no. CI: no. Not an analysis of example selection |
| N8 | Chen et al. PaLI-X: On Scaling up a Multilingual Vision and Language Model. arXiv 2305.18565; a second record under a later title is the same work | P-C | AX-3, S2-3 | arXiv v1 (f3d9bf554745), read in the passages cited | A trained model, also tested few-shot. R: random shots, p. 7: "Then, for each test data point, we randomly pick N shots from the pool as the actual few-shot examples". L: p. 7: "We also report few-shot CIDEr scores averaged over 35 languages using XM3600"; Vietnamese is not named in the text (0 hits). C: random examples only. S: none (0 hits). G: no. CI: no. Not an analysis of example selection |
| N9 | Li, Yuan, Li, Aliannejadi, Hershcovich, Søgaard, Vulić. RAVENEA: A Benchmark for Multimodal Retrieval-Augmented Visual Culture Understanding. ICLR 2026; arXiv 2505.14462 | P-A (benchmark with control contexts) | AX-2, OA-2, S2-2 | arXiv (42316c8118e5), read in the passages cited | T: the retrievers are trained (p. 2); the vision-language models are prompted. I: yes. R: encyclopaedia documents from English Wikipedia (p. 4), not captioning examples. L: caption language not named in the passages read. C: control contexts, p. 9: "we design two control conditions: random character sequences, culturally unrelated documents". S: significance marks on the correlation of metrics with human judgments (p. 5); none on caption scores (0 hits for ±, interval, bootstrap). G: no (0 hits). CI: no |
| N10 | Liu, Zhu, Zhou et al. Benchmarking Retrieval-Augmented Generation in Multi-Modal Contexts. An ACM publication by the index record (doi 10.1145/3746027.3755625); arXiv 2502.17297 | P-A (benchmark) | AX-1, AX-2, OA-2, S2-1, S2-2 | arXiv v2 (ba2f3743b7d2), read in the passages cited | Abstract, p. 1: "The benchmark comprises four tasks: image captioning, multi-modal question answering"; the other two tasks are fact verification and image reranking. T: prompted models and two fine-tuned ones (p. 5). R: retrieved multimodal documents, top 1, 3 or 5 (p. 5). C: no random control; the comparison is with the model without retrieval. S: none (0 hits). G: no. CI: no |
| N11 | Seo, Lee, Lee, Lin, Mirza, Tuytelaars, Choi. Visual Grounding First, Multimodal In-context Learning Follows. arXiv 2610.30592 | P-A at the abstract; a trained method on the full text (E3) | AX-3, OA-4, S2-3 | arXiv (ffd8d42c3699), read in the passages cited | T: yes, p. 4: "ProCoRe is trained on visually contrastive image pairs". It adds a captioning benchmark for in-context learning, p. 3: "we introduce PICL, a personalized ICL captioning benchmark built around personalized concept names", scored with ROUGE-L (p. 7). C: not an analysis of similar against random examples. S: p. 30: "We summarize the mean and standard deviation over three random seeds in Tab. 16". G: no. CI: no (0 hits) |
| N12 | Penamakuri et al. RA-CoA: Training-free Fashion Image Captioning via Retrieval-Augmented Chain-of-Attributes. TMLR 06/2026; arXiv 2609.14100 | P-B | AX-2, OA-2, S2-2 | arXiv v1 (73738acf1999), read in the passages cited | T: no, p. 1: "a novel, training-free framework that disentangles fashion image captioning into two interpretable stages". I: yes. R: attribute keys, not example captions, p. 4: "RA-CoA retrieves only attribute keys and infers attribute values directly from the VLM's internal knowledge through structured reasoning". L: not named ("English": 0 hits). C: a few-shot baseline with random examples (p. 8, p. 10), not a control of the retrieval. S: none. G: no. CI: no |
| N13 | Pereira, Maranhão, Xavier, Ren, García Seco de Herrera, Abolghasemi. UFPE-Essex-UNED at ImageCLEFmed Caption 2026: Training-Free Multimodal RAG for Medical Image Captioning. CLEF 2026 Working Notes, CEUR-WS Vol-4283, paper 278 | P-B | S2-2 | proceedings PDF (27c9bfdeff66), read in the passages cited | T: no, p. 1: "employing a fully training-free pipeline based on retrieval-augmented generation (RAG) and prompt engineering, without any model fine-tuning". I: yes. R: the three most similar images with their captions as few-shot examples (pp. 4, 5 and 7). L: not named ("English": 0 hits). C: no ("random": 0 hits). S: none. G: no. CI: no |
| N14 | Gaber, Amgad, Nasri, Ragab, Mohamed. NU_Internship team at ImageEval 2025: From Zero-Shot to Ensembles: Enhancing Grounded Arabic Image Captioning. ArabicNLP 2025 shared tasks (2025.arabicnlp-sharedtasks.58) | P-B | OA-2, S2-2 | anthology PDF (ee8636a9cae6), read in the passages cited | L: Arabic. Retrieval is used to revise a generated caption, p. 2: "The retrieved examples, together with the original output, were provided to Gemini-2.5flash, which revised the caption". C: no. S: none. G: no. CI: no |
| N15 | Yin, Zhu, Chen, Ngo. Efficient Test-Time Retrieval Augmented Generation. arXiv 2511.01059 | P-B at the abstract; falls out on the full text (E3) | AX-2, OA-2, S2-2 | arXiv v1 (b83ba531c225), read in the passages cited | Its captioning runs on a trained retrieval-augmented captioner, p. 8: "For image captioning, we follow the best practices from [34] with the SMALLCAP model" |
| N16 | DS4DH group at ImageCLEFmedical Caption 2025 (notebook paper) | P-B at the title; falls out on the full text (E3) | OA-2 | open archive copy (b3d5333884c5), read in the passages cited | Fine-tuned models, p. 7: "The model is trained for 20 epochs with a learning rate of 3e-5" |
| N17 | ICL Characterization of Multi-Modal Geo-Foundation Models. AIR Journal of Mathematics and Computational Sciences, 2026 (doi 10.65737/airmcs2026446) | P-A at the abstract; falls out on the full text (I2) | S2-3 | journal PDF (e1aeb4b6fd59), searched | No caption metric (0 hits for CIDEr, BLEU, METEOR) and no captioning experiment |
| N18 | Why is a Bird's Caption a Good Demonstration? Towards Effective Multimodal In-Context Learning without Dedicated Data. ACM Multimedia 2025 (doi 10.1145/3746027.3755653) | P-A | OA-4, OA-C3, S2-3 | NOT READ: at the ACM Digital Library, which refuses automated reads (not requested); two arXiv title searches found no copy | From the abstract only: evaluations over 17 data sets and five models, two hypotheses on why demonstrations help, and two proposed retrieval metrics. The abstract names no registration, interval or Vietnamese |
| N19 | Advancing Multimodal Large Language Models: Optimizing Prompt Engineering Strategies for Enhanced Performance. Applied Sciences, 2025 (doi 10.3390/app15073992) | P-A | OA-1, OA-2, OA-C3, S2-1, S2-2, S2-3 | NOT READ: the publisher's site answered HTTP 403 to one request | From the abstract only: five prompting techniques, among them in-context learning and retrieval augmentation, over several data sets, scored with BLEU, ROUGE, METEOR, CIDEr and others |
| N20 | Strategic Application of Prompt Engineering in Multi-Modal Large Language Models. IEEE ICCE 2025 (doi 10.1109/icce63647.2025.10930109) | P-A | OA-1, S2-3 | NOT READ: no open copy found; the publisher's site was not requested | From the abstract only: three models on Flickr30k, NoCaps and MSCOCO, with in-context learning compared to chain-of-thought prompting |
| N21 | Beyond Similarity: Aligning Retrieval with Generation for Enhanced Image Captioning. IJCNN 2025 (doi 10.1109/ijcnn64981.2025.11227734) | P-A | OA-2, OA-C2, OA-C7, S2-1, S2-2 | NOT READ: no open copy found; not requested | From the abstract only: observes that highly similar retrieved results do not always help generation, and trains the retriever to fit the captioner |
| N22 | Evaluating generative AI for medical image captioning: a benchmark study on radiology images. SPIE Medical Imaging 2026 (doi 10.1117/12.3084497) | P-A | OA-1 | NOT READ: no open copy found; not requested | From the abstract only: four models on ROCOv2 under zero-shot and few-shot prompting, with automated metrics |
| N23 | Relational reasoning image captioning via multi-agent retrieval-augmented generation. Knowledge-Based Systems, 2025 (doi 10.1016/j.knosys.2025.114977) | P-B (title only; no abstract in any source) | OA-2, S2-2 | NOT READ: no open copy found; not requested | – |

Term counts over the 17 full texts: "preregist" and "pre-regist" 0 in all; "registered" 1, in N2 and in another sense; "confidence interval" 1, in N1 and not on a caption score; "bootstrap" 0; "Vietnam" in N7 only (two language lists), with "vi" as a language code in N6.

## Part 5. Findings

### 5.1 Does any work contradict the sentence?

**No work found by this search contradicts it.** In the 17 full texts read, and in the abstracts of the 5 unread works that have one, nothing states a preregistration of hypotheses or contrasts, and nothing reports a confidence interval on a caption score. No analysis of example selection or retrieval for captioning includes Vietnamese.

The search found three things that bear on the wording, not on the truth, of the sentence:

1. **Standard deviations on caption scores exist.** N3 (Xiang et al.) reports mean ± standard deviation over five example draws on BLEU and CLIPScore in its random-sampling rows. N11 reports mean and standard deviation over three seeds on a captioning benchmark. The sentence says "confidence intervals", which stays true. The wider wording of `docs/TABLE1B_W5_EVIDENCE.md` l.49 ("or SD/SE/tests") holds for the six papers of Table 1b and would not hold for N3 if N3 became a row.
2. **Vietnamese appears in multilingual model and method papers, not in analyses.** N6 (PAELLA) is a trained retrieval-augmented captioner scored on the 36 languages of XM3600, like LMCap and CONCAP, which Table 1 already lists as "36, incl. Vietnamese". N7 (mOSCAR) and N8 (PaLI-X) test trained models with a few in-context examples on XM3600; only N7 names Vietnamese, in a language list. None of the three compares similar with random examples. So "none covers Vietnamese" is true of the analyses and must stay tied to them, as it is in the conference version ("Analyses of this question exist … none covers Vietnamese").
3. **A comparison with text-only example captions exists.** N2 (Freitas et al., CLEF 2026 working notes) gives small vision-language models three random or three retrieved captions as text, with the query image, for radiology captioning. It has no interval and no registration, so it does not touch the sentence. It does touch the list of what is specific to Paper C (5.3).

Registration was found twice near the field, outside the scope of the sentence: a 2021 paper on image descriptions with a preregistered human-subjects experiment, and a 2026 data deposit for two preregistered studies of image-text verification (Part 3). Neither studies in-context examples or retrieval for captioning.

The test has clear limits. The queries retrieved three of the six analyses already in Table 1b (4.1); six works that passed the abstract screen were not read; and the search reads titles and abstracts only. It cannot show that no such study exists. The words "As far as these papers state" already confine the sentence to the papers named, and in that form it stands.

### 5.2 Works that would have to be added

To Table 1 (design of the closest prior work):
- **N1, UniRAG.** Off-the-shelf multimodal models see the image and retrieved image-caption pairs, with a random-example control at equal k, on COCO. It is as close to the English arm as OpenFlamingo with RICES. Row: no | yes | image-caption pairs | English | yes, equal k | none.
- **N2, Freitas et al. 2026.** The only prior work found that shows example captions as text only to a model that sees the query image, and compares retrieved with random captions at equal k. Row: no (one of three configurations is fine-tuned) | yes | captions, as text | not named (radiology captions of ROCOv2) | yes, equal k = 3 | none (point scores).
- N6, PAELLA, optional: a trained multilingual captioner of the LMCap and CONCAP line. Row: yes | yes | captions | 36, incl. Vietnamese | no | none.

To Table 1b and the conference Table 1 (analyses), as rows or as citations in the text beside them:
- **N3, Xiang et al.** Similar against random demonstrations for captioning on six models, with gender bias as the outcome. Table 1b row: whether in-context demonstrations shift gender bias | not named (COCO, DCI) | a COCO subset, DCI | six open models | yes, equal shots | yes | no | no (mean ± SD over five draws).
- **N4, VL-ICL Bench.** Argues that captioning is a weak test of in-context learning. Table 1b row: whether common benchmarks test in-context learning | not named (COCO) | COCO, as a side check | several open models | no for captioning (random examples only) | yes | no | no (mean of three seeds).
- **N2** can also stand in Table 1b and in the conference Table 1, since the comparison is one of its findings. Conference row: not named (radiology) | captions, as text | yes, equal k | no; no.

Citations in the text, no row: N5 (Lever-LM) beside the sentence on learned demonstration selectors; N9 (RAVENEA) and N10 as benchmarks of retrieval augmentation that include captioning; N12 and N13 as further training-free pipelines.

Before any of these is added: each new work needs a bibliography entry checked against its proceedings page (N2 and N13 against CEUR-WS Vol-4283; N1 against the anthology, since only the arXiv version was read); and the six unread works (N18 to N23) should be read by hand, N18 first, because it is an analysis over many data sets.

### 5.3 Proposed wording (text only; no package)

**The tested sentence** (`01_introduction.md` l.9; conference `p:S1-02`): no change is needed. If N2, N3 or N4 are added to Table 1b, the sentence still holds for all rows; the cells read "registered: no" and, for the last column, "no (mean ± SD over five draws)" for N3, "no (mean of three seeds)" for N4 and "no" for N2.

**The Outcome sentence of `docs/TABLE1B_W5_EVIDENCE.md` l.49**, only if N3 becomes a row of Table 1b:

```
OLD: preregisters its contrasts or reports CIs (or SD/SE/tests) on the captioning score
NEW: preregisters its contrasts or reports CIs on the captioning score; one of them (Xiang et al.) reports standard deviations over example draws
```

together with "None of the six papers" changed to the new number of rows.

**What is specific to Paper C** (`02_related_work.md` l.69; conference `p:S2-05`). The text names text-only example captions as specific to this study, after comparing it with the two closest studies. With N2 that is no longer safe as a general statement. Proposed text for l.69:

```
OLD: What remains specific to this study is the Vietnamese setting, text-only example captions, per-backbone intervals and a registered one-look test.
NEW: A shared-task study of radiology captioning gives small vision-language models three retrieved or three random captions as text and reports point scores [citation for Freitas et al. 2026]. What remains specific to this study is the Vietnamese setting, per-backbone intervals and a registered one-look test; text-only example captions it shares with that study.
```

The list of five differences from the two closest studies (l.12 to l.16) stays true of those two studies and can stay as it is. In the conference version, `p:S2-05` lists "example captions shown as text only" under "What differs here"; one sentence after the list would cover it: "One shared-task study of radiology captioning also shows retrieved or random captions as text, with point scores only [citation]."

**The English precedent** (`02_related_work.md` l.20; conference `p:S2-03`): one clause for N1 after the OpenFlamingo sentences, for instance: "UniRAG [citation] reports the same direction on COCO for three multimodal models, with retrieved image-caption pairs against random ones at one and five examples."

## Part 6. What was not covered

- Six works that passed the abstract screen were not read (N18 to N23). By hand: N18 at the ACM Digital Library, N19 at the journal's site (open access), N20 and N21 at IEEE Xplore, N22 at SPIE, N23 at ScienceDirect.
- Recall is limited (4.1). Analyses that do not name captioning in the abstract are missed. The search of citing works helps only where OpenAlex holds the citation links: three of the seven seeds returned no citing work with a captioning term. No full-text search engine was used.
- The ACL Anthology search page gave no result to a plain request; the Anthology is covered only through the three indexes.
- 69 trained retrieval-augmented captioners (E3) and 15 knowledge-retrieval captioners (X-K) were counted and not read. A confidence interval or a random control inside one of them would be seen only if its abstract says so; the watch-list queries found no such abstract.
- Abstracts were read in a condensed view (D3) and full texts in the passages cited (D6).
- The files of the search (raw responses, the merged list with every decision code, the PDFs and their text) are in the scratch folder `/tmp/claude-1000/-mnt-d-vsps-image-captioning/cbc155a0-619c-4f6d-b27a-ab9635fb7056/scratchpad/search_2026-11-15/`, which does not survive a reboot. The decision lists are in `step1.py` and `step2.py` in `/tmp/claude-1000/-mnt-d-vsps-image-captioning/cbc155a0-619c-4f6d-b27a-ab9635fb7056/scratchpad/fulltext_scripts/`.

## Part 7. Correction note (2026-11-15T03:46Z)

Everything above this heading is unchanged: the first 47582 bytes of this file have sha256 `acdae5aab11e0e8c2ababae41f9c5b907bb1626cc0c64182a42166acb22c5b38`, the value cited by fix package v4 and by the records folder. Two statements above are corrected here; both were found when the works were read again for fix package v4 (`manuscript/fix_packages/2026-11-15_C/C_FIX_PACKAGE_v4_search.md`, blocks C-S01, C-S04 and C-S06, which carry the evidence).

1. **UniRAG (row N1; sections 5.2 and 5.3).** The clause proposed in 5.3, "UniRAG reports the same direction on COCO for three multimodal models, with retrieved image-caption pairs against random ones at one and five examples", is wrong for one cell. In Table 3 of the paper (CIDEr), the retrieved pairs score higher than the random pair in five of the six model-by-shot cells; for GPT-4o with one example the random pair scores higher (72.5 against 63.3 and 67.1 for the two retrievers). The clause must not be used; the text of block C-S01 replaces it.
2. **Freitas et al. (row N2; sections 5.1 to 5.3).** The row says "C: yes, equal k = 3" without a limit. The random condition was run for one of the three model configurations only (MedGemma 4B; Table 1 of the paper lists no random run for Qwen3-VL 4B or for the fine-tuned MedGemma 1.5 4B). The statements that the work "compares retrieved with random captions at equal k" hold for that one model.

Neither correction changes the finding of 5.1: no work found contradicts the tested sentence.
