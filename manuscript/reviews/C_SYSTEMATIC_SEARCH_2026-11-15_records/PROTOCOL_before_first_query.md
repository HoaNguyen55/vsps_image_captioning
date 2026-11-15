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
