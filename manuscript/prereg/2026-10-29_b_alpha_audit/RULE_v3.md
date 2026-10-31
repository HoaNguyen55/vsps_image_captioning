# B-α: protocol-disclosure audit of published Vietnamese captioning papers, by pre-written patterns (Paper B, LRE)

**Status:** RULE v3 (final text for the commit), written 2026-10-31 by our own writer agent.
- v3 = v2 (`RULE_DRAFT_v2.md`, sha256 be594dbc…) + CC-210 W1–W8 (CC-210 W9) + PI-1101b (new B title) + CC-210a W1–W9 + CC-210b W1–W4 + CC-210c W1–W6 + CC-210d W1–W4 (code fixes and the rule sentences they need). v1 (`RULE_DRAFT.md`, 6c9b82f0…) and v2 are kept unchanged as audit records.
- The fix-to-line maps are in `JUDGE_READ_REQUEST_CC210a.md` (CC-210), `JUDGE_READ_REQUEST_CC210b.md` (CC-210a), `JUDGE_READ_REQUEST_CC210c.md` (CC-210b), `JUDGE_READ_REQUEST_CC210d.md` (CC-210c) and `JUDGE_READ_REQUEST_CC210e.md` (CC-210d); the diffs are `CC210b.diff` (against the CC-210a subject), `CC210c.diff` (against the CC-210b subject), `CC210d.diff` (against the CC-210c subject) and `CC210e.diff` (against the CC-210d subject).
- The frozen strings of this rule are the `patterns.json` block of §2.1, byte-equal to `scripts/b_alpha/patterns.json`. The selftest checks the equality.
- Context, not a rule change: PI-1031m (2026-10-31) makes B-α the registered result of B's lead axis (audit, protocol card, kit). The verdict rule, T and the reporting duties are unchanged (CC-210, "For the PI").
- The candidate search has not run.
- No paper of the audit population has been opened for this audit.
- No pattern has been run on any third-party text.
- Live web calls made before the commit are disclosed in §8.1 (W8).
- The rule binds only after the code read CC-210a and a gatekeeper commit with `scripts/b_alpha/` and its `SHA256SUMS`, byte-identical to the CC-210e subject (the one-judge diff read after CC-210d). 2026-11-05 is a deadline, not a gate (CC-210 ruling 5).
- Nothing here is committed or run.

**Label:** a mechanical count over public documents, not annotation.
- It labels no dataset item.
- No human or AI judges or corrects any cell (CC-147 ruling 2, conditions (a)–(e)).
- Results are pattern bounds, not true disclosure rates.
- **The audit is AI-designed and not expert-validated (PI-1026bg, CC-156 W14).** The same sentence goes into the supplement.

**Design precedent (W14):** Marie, Fujita and Rubino (2021), "Scientific Credibility of Machine Translation Research: A Meta-Evaluation of 769 Papers", ACL 2021, DOI 10.18653/v1/2021.acl-long.566 (Crossref-verified in CC-156). The B writer adds it to `paperB.bib`; this rule does not edit the bib.

**Sources:**
- CC-147 ruling 2 (B-α GO), W4 (tool check on B's card and FAIR only, both excluded from the population, GO needs N ≥ 10 accessible papers) and W5 (soften or source the frequency sentence; already applied at `outline_B.md` l.8).
- PI-1026be (Ken unavailable; this draft goes to our writer, then a judge read).
- PI-1026ba (loop order: B audit B-α, B panel 11-30).
- Ken's K21 §B-α (`manuscript/ken/K21_NOVELTY_SCOUT.md`, sha b9d520a4…): gap, cells, SESOI 50%, N estimate 15–30. **Overruled there by CC-147 (c):** Ken's 3-paper pilot on third-party papers with sentences marked in advance. Marking sentences in third-party papers is human coding, so it is not used.
- B's protocol card: `manuscript/journal_draft_B/sec4_system.md` §4.2, Table 4.2.

## 0. Question and what the result may change

**Question.** Among published papers from 2020–2026 that report a caption-metric score on UIT-ViIC, VieCap4H, KTVIC or UIT-OpenViIC, how many contain a pattern-detected statement of (i) the word segmenter or tokenisation unit and (ii) the CIDEr variant?

**What it may change in B.** Only one sentence: the abstract/intro sentence on how often a KTVIC number states its protocol. That sentence is currently softened (CC-147 W5). B's other results, the card and the kit do not depend on B-α.

**What it cannot show.** A true disclosure rate. Pattern misses make disclosure look rarer than it is, and two tool-check texts cannot bound the miss rate. So a high hit count can refute "rarely stated", but a low hit count cannot prove it (§5).

## 1. Population (frozen before any paper is opened)

### 1.1 Candidate search (step S1)

Candidates are the union of:

- **(Q1) Citing works** of the five dataset records, from both OpenAlex (`/works?filter=cites:<W-id>`) and Semantic Scholar Graph (`/paper/<id>/citations`). **Resolution (CC-210 W2d), written now:** OpenAlex `/works/doi:<DOI>` (an arXiv record uses its DataCite DOI `10.48550/arXiv.<id>`) gives the W-id; Semantic Scholar `/paper/DOI:<DOI>` or `/paper/ARXIV:<id>` gives the paperId. A record that resolves in one source only uses that source and is logged `one_source`. A record that resolves in neither has an empty Q1 arm, is logged `unresolved` and reported; this is not a FAULT. The table:

  | Dataset | Record | Identifier |
  |---|---|---|
  | UIT-ViIC | Lam et al., ICCCI 2020 | DOI 10.1007/978-3-030-63007-2_57 |
  | KTVIC | Pham et al., 2024 | arXiv 2401.08100 (DOI 10.48550/arXiv.2401.08100) |
  | UIT-OpenViIC | Bui et al., SPIC 2026 | DOI 10.1016/j.image.2025.117430 |
  | UIT-OpenViIC preprint | Bui et al., 2023 | arXiv 2305.04166 |
  | VieCap4H | Le et al., VNU JCSCE 2022 | DOI 10.25073/2588-1086/vnucsce.341 |

- **(Q2) Keyword search (CC-210 W2a–c),** with exactly the strings of `patterns.json` (§2.1):
  - **OpenAlex:** `/works?filter=title_and_abstract.search:<string>` (not bare `search=`, which can also match full text; CC-156 W7), cursor paging. The filter name was read on the OpenAlex documentation page on 2026-10-31 (§8.1). **The same page marks the `filter=field.search:` syntax as deprecated ("still works but is no longer recommended"); the recommended form is the `search.title_and_abstract` parameter with the same semantics. The filter form is kept (CC-210a r7).** If OpenAlex answers the filter with any 4xx other than 404 or 429, that is a FAULT at S1; the only allowed fix is the documented parameter form `search.title_and_abstract=<string>` plus `filter=publication_year:2020-2026`, by amendment, before any population text exists. The pages are re-checked if the commit falls on a later UTC day than the last documentation read in §8.1. Strings: `"Vietnamese image captioning"` (quoted phrase), `UIT-ViIC` and its space form `"UIT ViIC"` (union), `KTVIC`, `OpenViIC`, `VieCap4H`.
  - **Semantic Scholar:** `/paper/search/bulk?query=<string>` with token pagination (no 1,000-result relevance ceiling). Hyphenated terms return no match on Semantic Scholar, so only space forms are sent. Strings: `"Vietnamese image captioning"` (quoted phrase), `"UIT ViIC"`, `KTVIC`, `OpenViIC`, `VieCap4H`.
  - v2's "total > 1,000 = FAULT" clause is dropped. The request cap (§7) stays a FAULT.
- **(Q3) The dataset records themselves.** They report baseline scores, so they are candidates.

**Search settings:**
- Publication year 2020–2026, applied in both sources (OpenAlex `publication_year:2020-2026`; Semantic Scholar `year=2020-2026`, and the same range on Q1 citing works) (CC-210 W2e).
- All result pages are fetched.
- **Hitting the request cap during S1 is a FAULT before the freeze (W7).** It is not "inaccessible-relevant": candidates that were never seen cannot be counted.
- **FAULT and the one resume (CC-210a W3).** Any error from S1 through the `cells.json` write (CC-210b W1, CC-210c W1: any exception, incl. a truncated response, a changed response shape, an error in the merge or the cell step, and an interrupt: SIGINT, and SIGTERM always and SIGHUP unless ignored, mapped to the same FAULT), and, through an outermost guard around the whole run, any other Python-level error once the OUT exists (step = the last stage entered), in particular any network or parsing error (an HTTP error other than the 404 of the resolution step and the PDF case of §1.2, a connection error, a timeout, a JSON decode error) and the S1 request cap write `search_log.json` and `FAULT.json` (step, error, time) and stop the job. Exactly one path continues it: `run --run --resume --out <the same OUT>`. It is allowed only if `FAULT.json` exists, `cells.json` does not, and the OUT has not been resumed before (a `RESUMED` marker). The resume re-checks both `SHA256SUMS` and the §2.1 equality, sha-checks every cached response against `search_log.json` (a missing or differing file is a FAULT with no further resume; CC-210c W3), and replays the cache. If `candidates.json` already exists, the rebuilt bytes must equal it, else FAULT with no further resume. **One FAULT gives one resume in total**; this is the rerun of §4 and the next-day resume of §7, not two separate allowances.
- In the resolution step only HTTP 404 means "does not resolve" (logged `unresolved`/`one_source`, with the HTTP code per source); every other HTTP error, including a 429 after the retries, is a FAULT (CC-210a W2).
- The run date(s) are recorded in `search_log.json` (`run_dates`, one entry per start or resume), with every request URL, its kind (api or pdf), its HTTP code, and the response sha256 for 2xx (`requests`; CC-210b W3). A resolution URL logged as HTTP 404 is replayed as a 404 from the log on resume, not re-queried. The same holds for any API URL logged as HTTP 404: outside the resolution step a 404 is a FAULT, so a resume that reaches the same URL FAULTs again with no further resume. The `candidates.json` sha256 is written to `candidates.sha256` in the OUT folder.

**Web-request rule.**
- No personal e-mail appears in any URL, header or payload.
- The OpenAlex `mailto` parameter and the User-Agent contact are `vsps-research@example.org` or are omitted.
- No API key is used. No login is used, institutional or personal.
- Responses are cached in the job folder (sha1-of-URL file names) so the run is replayable.

**Deduplication (mechanical).**
- Records are merged on DOI, then on arXiv id, then on normalised title. Normalisation: NFC, lower case, non-alphanumerics removed. Titles must be equal after normalisation.
- A preprint and its version of record count as one paper. The version of record is used if it is accessible, otherwise the preprint.
- **Pre-declared merges (W10), by id:**
  - UIT-OpenViIC: arXiv 2305.04166 = DOI 10.1016/j.image.2025.117430.
  - KTVIC: arXiv 2401.08100 = DOI 10.48550/arXiv.2401.08100 (the same record under two ids).
  - Any record whose OpenAlex or Semantic Scholar `externalIds` lists both a DOI and an arXiv id merges on either.
  - No other preprint/version-of-record pair is known now. Pairs found later merge only through the mechanical title rule above.

**Freeze.** `candidates.json` (metadata only) is written and its sha256 is logged before step S2 fetches any full text.

### 1.2 Full text (step S2)

**Accessible** means that a PDF is downloadable without login from one of these, tried in this order:
1. the OpenAlex `best_oa_location.pdf_url`;
2. the Semantic Scholar `openAccessPdf.url`;
3. `https://arxiv.org/pdf/<id>` when an arXiv id exists.

Anything else is **inaccessible** and is counted, never dropped (CC-147 (d)). HDUCap (Hoang et al., 2026) and ViG (Vu et al., 2026) are expected to be inaccessible: B sec2 l.7 records that their full texts could not be obtained on 2026-10-15.

**Also inaccessible (W4).** A downloaded file is treated as inaccessible, with its reason counted in `population.json`, when any of these holds:
- (a) `not_pdf`: the first bytes are not `%PDF` (for example, an HTML landing page served at a PDF URL);
- (b) `scanned`: the extraction has fewer than 500 characters per page on average, or fewer than 2,000 characters in total;
- (c) `extract_fail`: `pdftotext` exits non-zero or times out (60 s per file);
- (d) `fetch_fail` (CC-210a W6): the PDF URL fails after the retries (an HTTP error, a timeout, or a truncated or dropped response; CC-210b W1). The HTTP code is recorded in `fulltext_manifest.json`; the next URL in the order above is then tried. It is never recorded as `no_oa_pdf` (no PDF URL at all). Requests to arxiv.org are spaced at ≥ 3 s (`caps.arxiv_min_spacing_s`).

As with any inaccessible candidate, it is inaccessible-relevant if its metadata matches the dataset pattern (§1.3).

**Extraction.**
- Plain `pdftotext` (poppler; version recorded; laptop version on 2026-10-31: 24.02.0), not `-layout`. With `-layout`, two-column pages merge columns into one line.
- Then NFC normalisation, removal of a line-end hyphen before a lower-case letter, and whitespace collapsed to single spaces.
- Page numbers come from form feeds.
- Each PDF and each text file is sha256'd in `fulltext_manifest.json`.

### 1.3 Inclusion (step S3; frozen pattern, applied to the pre-reference text)

A candidate is **included** if both patterns below match its **pre-reference text** (W2, option (a)). Matching is case-insensitive.

**Pre-reference text.**
- The extracted text is cut at the **last** line that matches `^\s*(?:(?:\d+|[ivxlc]+)\.?\s+)?(references|bibliography|tài liệu tham khảo)\s*:?\s*$` (CC-210 W4a: numbered headings such as "7 References" or "VII. REFERENCES" and a trailing colon), case-insensitive, multiline, read before whitespace collapse with one line per line.
- If no such heading is found, the whole text is used and the paper is flagged `no_ref_heading`. The flag count is reported.
- The cells of §2 still run on the whole text, references included (broad, as in v1).

**Patterns.**
- **Dataset name:** `UIT\s?[-‐]?\s?ViIC|KTVIC|Open\s?[-‐]?\s?ViIC|VieCap\s?[-‐]?\s?4H` (optional separators, W3)
- **Metric name:** `\b(CIDEr|BLEU|METEOR|ROUGE|SPICE)\b`

**Direction (W2, also in §8).** Running inclusion on the pre-reference text removes papers that only cite a dataset and a metric. That shrinks N_acc and removes papers that report no score, which would otherwise mostly lack S. So it moves the result away from PASS by artefact, which is the conservative direction. A missed heading (`no_ref_heading`) moves it back toward PASS, and that count is reported.

An **inaccessible** candidate is counted as *inaccessible-relevant* if its title or abstract (from the API metadata) matches the dataset-name pattern. Otherwise it is *inaccessible-unclassifiable*. Both counts are reported. Only inaccessible-relevant papers enter the bounds in §5.

### 1.4 Pre-fixed exclusions (disclosed, counted)

| # | Exclusion | Reason |
|---|---|---|
| E1 | The FAIR 2026 paper (Hòa et al.) | Tool-check text (CC-147 W4). It would otherwise pass §1.3 |
| E2 | Paper B and its preprints | Tool-check text (CC-147 W4) |
| E3 | Any other paper of our group, **by the frozen identifier list below, never by author name** (W6, J10) | Not a third-party disclosure |
| E4 | Non-paper records, by the type vocabularies below (W10) | Not a published paper |
| E5 | Full text not in English, by the rule below | The patterns are English. Count reported. See judge item J6 |

**E1–E3 identifier list (frozen now; W6).**
- Our group has no DOI or arXiv id yet: FAIR 2026's DOI and pages are not issued, and B, A, C and MT4 are unpublished.
- The list therefore holds normalised exact titles (§1.1 normalisation), with ids appended if issued before the commit:
  - FAIR 2026: "A Method for Reducing Hallucinations in Detailed Vietnamese Image Captioning Using Supervision from Verified Propositions";
  - Paper B (CC-210 W3; literal titles, not a pointer to a mutable file): "What Training-Data Gains Measure on a Vietnamese Captioning Benchmark: A Development Study with Two Reference Panels, a Validity Audit of KTVIC and an Open Evaluation Kit"; "What Training-Data Gains Measure on a Vietnamese Captioning Benchmark: Two Reference Panels, a Validity Audit of KTVIC and an Open Evaluation Kit"; "What Does a Vietnamese Captioning Score Measure? Reference Panels, Training-Data Gains and a Validity Audit of KTVIC"; "What a Vietnamese Captioning Benchmark Measures: A Validity Audit of KTVIC and an Open Evaluation Kit"; "What a Vietnamese Captioning Benchmark Measures: A Controlled Fine-Tuned VLM and a Validity Audit of KTVIC"; "Benchmark validity in Vietnamese image captioning: a KTVIC audit, protocol card and evaluation kit" (adopted title, PI-1101b, appended 2026-11-01 before CC-210a).
  - A B title adopted before the commit (e.g. after the PI-1031m reframe) is appended to this list and to `patterns.json` before CC-210a; after the commit only by amendment.
- `population.json` lists every E3 match with the list entry that matched it. A name-only match never excludes a paper.

**E4 type vocabularies (W10).**
- **OpenAlex (CC-210 W1: a full partition of the 25 documented types, read by the CC-210 judge on the OpenAlex help pages).**
  - Accepted: `article`, `preprint`, `book-chapter`, `review`, `conference-paper`, `data-paper`, `software-paper`.
  - Excluded: `book`, `book-review`, `conference-abstract`, `dataset`, `dissertation`, `editorial`, `erratum`, `letter`, `libguides`, `other`, `paratext`, `peer-review`, `reference-entry`, `report`, `retraction`, `software`, `standard`, `supplementary-materials`.
  - OpenAlex has no `proceedings-article` and no `grant` type. `type` and `type_crossref` are recorded per candidate; `type_crossref` is not used for the decision.
  - **A type in neither list (vocabulary drift) is accepted and counted as `type_unlisted` in `population.json`.** Inclusion still needs the dataset and metric patterns in the main text, so an extra type cannot add a paper that reports no score.
  - CC-210a re-checks the list against the documentation page on the commit day. Any difference is an amendment, not a silent edit.
- **Paper level (CC-210a W4).** E4 judges records, then papers. Excluded records are dropped. If a merged paper has any OpenAlex record, the paper is kept when at least one of its OpenAlex records is accepted or unlisted (`type_unlisted` is flagged when only an unlisted record keeps it); the Semantic Scholar rule below decides only papers with no OpenAlex record. **The five Q3 dataset records (§1.1 table), matched by id, bypass E4:** they were fixed by id as published papers, and J7 keeps them in.
- **Semantic Scholar-only records.** The record is accepted if `publicationTypes` contains any of `JournalArticle`, `Conference`, `BookSection`, `Review`, `Study`. If `publicationTypes` is null, it is accepted only when `externalIds` has an `ArXiv` or `DOI` entry.
  - Excluded: records whose types are only `Dataset`, `Book`, `Editorial`, `LettersAndComments`, `News`, `CaseReport`, `ClinicalTrial`, `MetaAnalysis`.
  - A `publicationTypes` value in neither list is accepted and counted as `type_unlisted` (CC-210 W1).

**E5 rule (W5).**
- A text is non-English if fewer than **15%** of its word tokens are in the fixed list of 50 English function words. v1 used 5%. English prose sits well above 15%, while a Vietnamese text with an English abstract and English references can pass 5%.
- The list is frozen in `english_words.txt` (in `SHA256SUMS`). **Source (CC-210 W7):** the first 50 function words, in rank order, of the 100 most common words of the Oxford English Corpus (the list printed in Wikipedia "Most common words in English"), written down from memory on 2026-10-31 without opening any text; the content words, numerals and adverbs of that list are skipped and named in the file header. The list is never tuned to T1, T2 or any population text.
- `population.json` records each candidate's share (CC-210 W7).
- The selftest asserts that T1 and T2 (§3) are each ≥ 15%.
- **E5 papers that are relevant enter N_inr in the primary bounds (§5).** Relevant = the metadata (title + abstract) matches the dataset pattern **or** the dataset pattern matches the pre-reference full text (CC-210a W8, settling CC-156 J6). This widens [L, U] and never moves the result toward PASS. The descriptive table also shows them as a separate row.

## 2. Cells (frozen patterns; every cell is a pattern, CC-147 (b))

All patterns are case-insensitive and run on the whole extracted text, references included. Counting a tool named only in the references is the broad, conservative choice (§5).

| Cell | Name | Pattern (Python `re`) | Role |
|---|---|---|---|
| C1 | segmenter / unit | `VnCore\s?[-‐]?\s?NLP\|RDR\s?Segmenter\|\bpyvi\b\|underthesea\|vitokenizer\|word[-‐\s]?segment\w*\|syllable[-‐\s]?(level\|based)\|word[-‐\s]?level` (W3: optional separators; `syllable[-‐\s]?based` covers v1's "syllable-based tokeni[sz]…"; CC-210 W4b: `VnCore\s?[-‐]?\s?NLP` catches "VnCore-NLP" split at a line end) | primary |
| C1t | segmenter tool named | `VnCore\s?[-‐]?\s?NLP\|RDR\s?Segmenter\|\bpyvi\b\|underthesea\|vitokenizer` (W13, J4) | descriptive |
| C2 | CIDEr variant | `CIDEr\s?[-‐–]?\s?D\b\|CIDEr\s?[-‐–]?\s?R\b\|CIDEr\s?\(D\)` (W3: also catches "CIDEr- D", the form left when a line break after the hyphen is collapsed, since the hyphen is kept before an upper-case letter) | primary |
| C2t | scorer code named | `pycocoevalcap\|coco[-‐\s]?caption(?:ing)?(?!s)\s*(evaluation\|toolkit\|code\|repo\w*)\|tylin/coco[-‐\s]?caption\|COCO (caption(?:ing)? )?evaluation (toolkit\|code\|API)` (CC-156 W1: scorer-code forms only; "server" and bare `coco[-\s]?caption` / `cococaption` dropped; CC-210 W4c: `caption(?:ing)?` catches "COCO captioning evaluation toolkit") | primary (with C2) |
| C3 | scale | `(×\|\bx\|times\|multipl\w* by\|scaled? by)\s*100\b` | descriptive |
| C4 | punctuation | `punctuation` | descriptive |
| C5 | code link | `github\.com/\|gitlab\.com/\|huggingface\.co/\|zenodo\.org/` | descriptive |

**Primary composite.** **S = C1 ∧ (C2 ∨ C2t).** A paper is "pattern-detected as stating both" if S holds.

C2t is counted with C2 because naming the COCO evaluation **code** fixes the CIDEr variant (CIDEr-D) (J3, as ruled in CC-156). The dataset name ("MS COCO Captions") and the Chen et al. (2015) title ("Microsoft COCO Captions: Data Collection and Evaluation Server") do not fix it. The selftest plants both strings as near-misses that must **not** fire C2t (W1).

**Selftest separator cases (W3).** "word-\nlevel", "word-\nsegmentation", "CIDEr-\nD" and "Open-\nViIC" are passed through the extraction normalisation (de-hyphenation, whitespace collapse). Each must still fire its cell or the dataset pattern.

**CC-210 W4 must-fire cases (added to the selftest).** "7 References", "VII. REFERENCES" and "References:" as reference headings; "VnCore-\nNLP" for C1 and C1t; "COCO captioning evaluation toolkit" for C2t. The Chen et al. (2015) title and "MS COCO Captions dataset" stay must-not-fire for C2t, and "Related references are many" must not be read as a heading.

**Broad by design.** The patterns accept generic mentions: "word-level" anywhere, any `pyvi` mention, a segmenter cited only in the references. False hits raise the stated count, which works against a "rarely stated" reading. Misses (unusual wording, a scanned PDF) work for it. That residual bias is disclosed (§8).

**Cross-paper comparison cell (K21's second cell): not adopted in this draft.** A table that copies another paper's number cannot be detected by a sentence pattern without someone reading the table, and reading tables would be coding. See judge item J5.

### 2.1 Frozen strings (byte-equal to `scripts/b_alpha/patterns.json`; CC-210 W9)

Every pattern, query, type list, title, id, threshold and pin of this rule is in the block below. If the prose and the block ever differ, the block governs; the selftest fails unless the block equals `patterns.json` byte for byte.

<!-- patterns.json BEGIN -->
```json
{
 "version": "b_alpha rule v3 (RULE_v3.md; CC-156 W1-W14 + CC-210 W1-W8 + CC-210a W1-W9)",
 "regex_flags": [
  "IGNORECASE",
  "MULTILINE"
 ],
 "dataset": "UIT\\s?[-‐]?\\s?ViIC|KTVIC|Open\\s?[-‐]?\\s?ViIC|VieCap\\s?[-‐]?\\s?4H",
 "metric": "\\b(CIDEr|BLEU|METEOR|ROUGE|SPICE)\\b",
 "ref_heading": "^\\s*(?:(?:\\d+|[ivxlc]+)\\.?\\s+)?(references|bibliography|tài liệu tham khảo)\\s*:?\\s*$",
 "cells": {
  "C1": "VnCore\\s?[-‐]?\\s?NLP|RDR\\s?Segmenter|\\bpyvi\\b|underthesea|vitokenizer|word[-‐\\s]?segment\\w*|syllable[-‐\\s]?(level|based)|word[-‐\\s]?level",
  "C1t": "VnCore\\s?[-‐]?\\s?NLP|RDR\\s?Segmenter|\\bpyvi\\b|underthesea|vitokenizer",
  "C2": "CIDEr\\s?[-‐–]?\\s?D\\b|CIDEr\\s?[-‐–]?\\s?R\\b|CIDEr\\s?\\(D\\)",
  "C2t": "pycocoevalcap|coco[-‐\\s]?caption(?:ing)?(?!s)\\s*(evaluation|toolkit|code|repo\\w*)|tylin/coco[-‐\\s]?caption|COCO (caption(?:ing)? )?evaluation (toolkit|code|API)",
  "C3": "(×|\\bx|times|multipl\\w* by|scaled? by)\\s*100\\b",
  "C4": "punctuation",
  "C5": "github\\.com/|gitlab\\.com/|huggingface\\.co/|zenodo\\.org/"
 },
 "cell_roles": {
  "C1": "primary",
  "C1t": "descriptive",
  "C2": "primary",
  "C2t": "primary (with C2)",
  "C3": "descriptive",
  "C4": "descriptive",
  "C5": "descriptive"
 },
 "primary_composite": "S = C1 and (C2 or C2t)",
 "years": [
  2020,
  2026
 ],
 "openalex": {
  "base": "https://api.openalex.org",
  "title_abstract_filter": "title_and_abstract.search",
  "per_page": 200,
  "accepted_types": [
   "article",
   "preprint",
   "book-chapter",
   "review",
   "conference-paper",
   "data-paper",
   "software-paper"
  ],
  "excluded_types": [
   "book",
   "book-review",
   "conference-abstract",
   "dataset",
   "dissertation",
   "editorial",
   "erratum",
   "letter",
   "libguides",
   "other",
   "paratext",
   "peer-review",
   "reference-entry",
   "report",
   "retraction",
   "software",
   "standard",
   "supplementary-materials"
  ],
  "unlisted_type_rule": "accept and count as type_unlisted",
  "queries": [
   "\"Vietnamese image captioning\"",
   "UIT-ViIC",
   "\"UIT ViIC\"",
   "KTVIC",
   "OpenViIC",
   "VieCap4H"
  ]
 },
 "semantic_scholar": {
  "base": "https://api.semanticscholar.org/graph/v1",
  "search_endpoint": "/paper/search/bulk",
  "fields": "paperId,externalIds,title,abstract,year,publicationTypes,openAccessPdf",
  "accepted_publication_types": [
   "JournalArticle",
   "Conference",
   "BookSection",
   "Review",
   "Study"
  ],
  "excluded_publication_types": [
   "Dataset",
   "Book",
   "Editorial",
   "LettersAndComments",
   "News",
   "CaseReport",
   "ClinicalTrial",
   "MetaAnalysis"
  ],
  "null_types_rule": "accept only if externalIds has ArXiv or DOI",
  "unlisted_type_rule": "accept and count as type_unlisted",
  "queries": [
   "\"Vietnamese image captioning\"",
   "\"UIT ViIC\"",
   "KTVIC",
   "OpenViIC",
   "VieCap4H"
  ],
  "min_spacing_s": 3
 },
 "dataset_records": [
  {
   "name": "UIT-ViIC",
   "doi": "10.1007/978-3-030-63007-2_57",
   "arxiv": null
  },
  {
   "name": "KTVIC",
   "doi": "10.48550/arXiv.2401.08100",
   "arxiv": "2401.08100"
  },
  {
   "name": "UIT-OpenViIC",
   "doi": "10.1016/j.image.2025.117430",
   "arxiv": null
  },
  {
   "name": "UIT-OpenViIC preprint",
   "doi": "10.48550/arXiv.2305.04166",
   "arxiv": "2305.04166"
  },
  {
   "name": "VieCap4H",
   "doi": "10.25073/2588-1086/vnucsce.341",
   "arxiv": null
  }
 ],
 "predeclared_merges": [
  [
   "arxiv:2305.04166",
   "doi:10.1016/j.image.2025.117430"
  ],
  [
   "arxiv:2401.08100",
   "doi:10.48550/arxiv.2401.08100"
  ]
 ],
 "e3_titles": [
  "A Method for Reducing Hallucinations in Detailed Vietnamese Image Captioning Using Supervision from Verified Propositions",
  "What Training-Data Gains Measure on a Vietnamese Captioning Benchmark: A Development Study with Two Reference Panels, a Validity Audit of KTVIC and an Open Evaluation Kit",
  "What Training-Data Gains Measure on a Vietnamese Captioning Benchmark: Two Reference Panels, a Validity Audit of KTVIC and an Open Evaluation Kit",
  "What Does a Vietnamese Captioning Score Measure? Reference Panels, Training-Data Gains and a Validity Audit of KTVIC",
  "What a Vietnamese Captioning Benchmark Measures: A Validity Audit of KTVIC and an Open Evaluation Kit",
  "What a Vietnamese Captioning Benchmark Measures: A Controlled Fine-Tuned VLM and a Validity Audit of KTVIC",
  "Benchmark validity in Vietnamese image captioning: a KTVIC audit, protocol card and evaluation kit"
 ],
 "e3_ids": [],
 "preread_set": [
  [
   "arxiv:2401.08100",
   "doi:10.48550/arxiv.2401.08100"
  ],
  [
   "arxiv:2305.04166",
   "doi:10.1016/j.image.2025.117430"
  ],
  [
   "arxiv:2602.22678",
   "doi:10.48550/arxiv.2602.22678"
  ]
 ],
 "thresholds": {
  "T": 0.5,
  "N_acc_min": 10,
  "e5_min_share": 0.15,
  "scanned_min_chars_per_page": 500,
  "scanned_min_chars_total": 2000,
  "pdftotext_timeout_s": 60,
  "quote_max_words": 40
 },
 "caps": {
  "api_requests": 400,
  "pdfs": 300,
  "wall_h": 6,
  "arxiv_min_spacing_s": 3
 },
 "pins": {
  "scanner": {
   "path": ".session_backup/2026-10-28/snapshots/C_pass3/checks/ngram_scan_cen.py",
   "sha256": "926076353d0393fc49b04f82382a6ee4ecb416b62a8436987212abb402f7adf3"
  },
  "t1_slice": {
   "path": "manuscript/journal_draft_B/sec4_system.md",
   "first_line": 29,
   "last_line": 49,
   "sha256": "78300f9fac34d90d2af1f3d01a0840dfc8e46d4624a322d1e6b2c910f5ecd255"
  },
  "t2_pdf": {
   "path": "manuscript/FAIR_28.08.26_v10_EN_IEEE.pdf",
   "sha256": "449c2ad0a4c16ac939d91ad5740bbaf51e8114d2f23e9b439dac2f3f626e7bc6"
  },
  "tools": {
   "pdftotext": "24.02.0",
   "pandoc": "3.5",
   "tlmgr_revision": "80687",
   "pdf_engine": "xelatex",
   "mainfont": "DejaVu Serif"
  }
 },
 "toolcheck_expected": {
  "T1": {
   "C1": true,
   "C1t": true,
   "C2": true,
   "C2t": true,
   "C3": true,
   "C4": true,
   "C5": false,
   "S": true
  },
  "T2": {
   "C1": true,
   "C1t": true,
   "C2": false,
   "C2t": false,
   "C3": false,
   "C4": false,
   "C5": true,
   "S": false
  }
 },
 "contact": "vsps-research@example.org"
}
```
<!-- patterns.json END -->

## 3. Tool check (before any third-party text; CC-147 (c), W4)

The patterns run first on two texts whose disclosures we know by construction. Both go through the same PDF → `pdftotext` path as the population:

| Text | Source (pinned) | Expected C1 | C1t | C2 | C2t | C3 | C4 | C5 | Expected S |
|---|---|---|---|---|---|---|---|---|---|
| T1: B's protocol card | `manuscript/journal_draft_B/sec4_system.md` **lines 29–49** (§4.2 heading through the line before §4.3: Table 4.2 and its note). Slice sha256 `78300f9fac34d90d2af1f3d01a0840dfc8e46d4624a322d1e6b2c910f5ecd255` on 2026-10-31. Rendered to PDF with pandoc 3.5 and TinyTeX (tlmgr revision 80687) (W11) | hit | hit | hit | hit | hit | hit | no hit | **true** |
| T2: FAIR 2026 | `manuscript/FAIR_28.08.26_v10_EN_IEEE.pdf`, sha256 `449c2ad0a4c16ac939d91ad5740bbaf51e8114d2f23e9b439dac2f3f626e7bc6` | hit | hit | **no hit** | no hit | no hit | no hit | hit | **false** |

**T1 slice pin (W11).** The job copies exactly the slice above and checks its sha before rendering. If `sec4_system.md` changes before the commit, the gatekeeper recomputes the line numbers and sha. The expected row stays as written, and the change is noted in the request. After the commit, the copy in the job folder is the pinned text, whatever happens to `sec4_system.md` later.

**v2 pre-check on our own texts (allowed: CC-147 (c)).** On 2026-10-31 the v2 patterns were run once in Python on two of our own texts, with the same normalisation:
- T2: plain `pdftotext` 24.02.0 output of FAIR;
- T1: the raw markdown slice, not yet rendered to PDF.

Both rows came out exactly as expected above, including the new C1t cell.

**Full T1 path before the commit (CC-210 W6).** On 2026-10-31 (~16:30Z) `b_alpha.py toolcheck` ran the whole T1 path twice on the laptop: slice (sha 78300f9f… checked) → pandoc 3.5 + TinyTeX xelatex (DejaVu Serif, `SOURCE_DATE_EPOCH=0`) → plain `pdftotext` 24.02.0 → normalisation → all 7 cells and E5. T2 went through the same extraction.
- T1: C1, C1t, C2, C2t, C3, C4 hit; C5 no hit; S true; E5 share 0.2241. Exactly as expected.
- T2: C1, C1t, C5 hit; C2, C2t, C3, C4 no hit; S false; E5 share 0.2328. Exactly as expected.
- The T1 PDF bytes differ between renders (xelatex writes a fresh document id; the two shas are in the CC-210a request), but the extracted text is identical (sha256 8ef14167…c1b5b both times). So the pin is the slice sha plus the expected cell row, not the PDF sha.

**T1 (positive control).** B's card names RDRSegmenter/VnCoreNLP, CIDEr-D, ×100, its punctuation policy and pycocoevalcap.

**T2 (negative control).**
- FAIR names the segmenter ("word-segmented with RDRSegmenter/VnCoreNLP").
- It writes plain "CIDEr [29]" with no variant, and it does not name the scorer code.
- It states no ×100 scale and says nothing on punctuation.
- It gives the repository link.

**Disclosure.** The v1 writer read FAIR's text (a keyword grep) while drafting this table, and then ran the v1 §2 patterns once on it (plain `pdftotext`, NFC, de-hyphenation). The result matched row T2 exactly, as CC-156 confirmed by its own re-run. The v2 pre-check above repeats this with the v2 patterns. FAIR is our own paper, so its disclosures are known anyway. That is why CC-147 allows it as a tool-check text and excludes it from the population.

**Pass condition.** All 14 expected cells of T1 and T2 (7 cells each, C1t included) match exactly, and both texts pass the E5 English check at ≥ 15% (W5). If any cell differs:
- the job stops (FAULT) before step S4, and no pattern is run on a third-party text;
- a fix is an amendment that a judge reads and the gatekeeper commits before any population text is opened.

## 4. Steps and one look (`scripts/b_alpha/b_alpha.py`, laptop CPU)

The script is `scripts/b_alpha/b_alpha.py` (in `SHA256SUMS`). Its contract is below; it is committed with this rule after CC-210e.

0. `--selftest` (network blocked by disabling sockets; CC-210 W9) on synthetic strings, synthetic PDFs and a mocked API: every cell pattern hits a planted sentence and misses a planted near-miss (incl. the W1 C2t near-misses and the W3 separator cases); the pre-reference cut (W2); the W4 inaccessibility reasons (a non-PDF file, a near-empty extraction, a failing extraction); the E3 id list; the E5 threshold; the S composite; the bounds; the NO-GO gate; the CC-210 W4 must-fire and must-not-fire cases; the E4 partition and `type_unlisted` rule (CC-210 W1); the bulk endpoint, space forms, quoted phrase, year filters and the `one_source`/`unresolved` resolution log on a mocked API (CC-210 W2); the two-way decide and `template_licensed` (CC-210 W5); the refusal of the live path without `--run`; the byte equality of §2.1 and `patterns.json`. **No S1/S2 code path runs without an explicit `--run` flag (CC-210 W9).** **S1/S2 code is developed and tested only on mocked API responses and synthetic PDFs; the first live API or PDF request is the run itself, after the gatekeeper commit (W8).** Then the `SHA256SUMS` check (`patterns.json`, `english_words.txt`, script, this RULE). Then the T1/T2 tool check (§3).
1. **S1 search** → `candidates.json` and its sha logged.
2. **S2 fetch and extract** → `fulltext_manifest.json`.
3. **S3 inclusion and exclusions** → `population.json`, holding:
   - N_acc = included accessible papers;
   - N_inr = inaccessible-relevant papers;
   - per-exclusion counts.
4. **GO gate.**
   - If N_acc < 10: **NO-GO** (CC-147 W4). No cell pattern runs on any third-party text, and `decide.json` records only the counts.
   - Otherwise continue.
5. **Cells, one run** → `cells.json`, one row per included paper. Each row holds the cell booleans and, per hit, page, character offset and the matched sentence. A sentence is the span between `[.!?]\s` boundaries, cut to the 40 words around the match.
6. **decide** (one look) → `decide.json`: the counts, the bounds and the verdict, computed twice (§5, CC-210 W5).

**Order and freeze.**
- `patterns.json` is in `SHA256SUMS` before step 1.
- No pattern, list or threshold changes after any population text exists on disk.
- Nobody reads a population text, `cells.json` or a quote before `decide.json` exists.
- After it exists, no cell is changed for any reason, including a reading that shows a cell is wrong. Such a case may be reported as an example of a pattern miss or false hit, with its location, never as a correction.
- A FAULT before step 5 allows the one logged resume of §1.1 (`--resume`, same OUT, same frozen files, cache replayed). A rerun or resume after `cells.json` exists is not allowed, and a second OUT folder after `cells.json` exists is a breach.
- **NO-GO record (CC-210a W1).** When N_acc < 10, `decide.json` holds verdict NO-GO with `k` = null and `L`/`U` = null in both rows, the counts N_acc, N_inr, N_all, and `template_licensed` false.

**Quotes (CC-147 (e)).**
- `quotes.tsv` holds only matched sentences of ≤ 40 words. No example caption is ever quoted.
- Rule: every quote is run through the gatekeeper n-gram scan, 6-/8-grams against KTVIC, UIT-OpenViIC, UIT-ViIC and COCO-Karpathy captions. **Scanner pin (W12):** `.session_backup/2026-10-28/snapshots/C_pass3/checks/ngram_scan_cen.py`, sha256 `926076353d0393fc49b04f82382a6ee4ecb416b62a8436987212abb402f7adf3` (byte-identical to the session scratchpad copy on 2026-10-31). The job checks this sha before scanning, or the gatekeeper commits a copy under `scripts/b_alpha/` with the same sha.
- Any quote with a 6-gram or 8-gram hit is reduced to its location (paper id, page, offset) before anything leaves the job folder.
- PDFs and full texts are never committed. Only `candidates.json` (metadata), the manifests, `population.json`, `decide.json` and the scanned `quotes.tsv` go to the gatekeeper.

## 5. Primary metric and decision rule (numbers fixed now)

**Census, not sample.** The population is every candidate the frozen search returns, so no sampling interval is computed. The bounds come from the inaccessible papers (judge item J1).

Let k = number of included accessible papers with S true, and N_all = N_acc + N_inr.

- **Lower bound:** L = k / N_all (every inaccessible-relevant paper counted as not stating both).
- **Upper bound:** U = (k + N_inr) / N_all (every one counted as stating both).
- **Threshold:** T = 0.50, Ken's SESOI (K21 §B-α item 2), fixed now and never changed.

| Verdict | Condition | What B may say |
|---|---|---|
| **REFUTES** | L ≥ 0.50 | No sentence implying that the protocol is rarely or seldom stated. B **must** report the counts in the supplement as a negative result (W9; K21: "honest, and still a result line"). |
| **PASS** | U < 0.50 | Only the template below. Never "rarely stated", "most papers do not state", or any wording that reads the pattern count as a true rate. |
| **INCONCLUSIVE** | otherwise | The softened sentence in `outline_B.md` l.8 stays as it is. The counts **must** go to the supplement with the INCONCLUSIVE label (W9). |
| **NO-GO** | N_acc < 10, or the tool check fails | The softened sentence stays. B-α is logged as not run (count reason only). |

**PASS template (pre-written; numbers filled from `decide.json` only):**
> "Of N_all published papers whose main text names UIT-ViIC, VieCap4H, KTVIC or UIT-OpenViIC together with a caption metric (2020–2026; frozen search, Supplementary S_x), N_inr could not be read, and a pre-registered keyword search found a statement of both the word segmenter and the CIDEr variant (or the scorer code) in k of the N_acc readable papers. The search is a lower bound on disclosure: it misses unusual wording."

**Pre-read sensitivity row (CC-210 W5), pre-registered now.**
- The pre-read set, frozen by id in `patterns.json`: KTVIC (arXiv 2401.08100), UIT-OpenViIC (arXiv 2305.04166 = DOI 10.1016/j.image.2025.117430), ViCLIP-OT (arXiv 2602.22678, if it is included at all). These are the papers whose full texts were read on 2026-10-29 (§8.1).
- `decide.json` computes the verdict twice with the same rule: on the full census (**primary**) and with the pre-read set removed.
- **The primary verdict is the registered verdict.** REFUTES and INCONCLUSIVE stand on the primary.
- B may use the PASS template only if PASS holds both ways. Otherwise B keeps the softened sentence and reports both rows.
- Both rows go to the supplement.
- Output fields, fixed now: `verdict` (primary), `primary` {k, N_acc, N_inr, N_all, L, U}, `verdict_without_preread`, `without_preread` {same keys}, `template_licensed` (true only if both are PASS), `T`, `descriptive` (per-cell hit counts).
- Example: primary PASS with the sensitivity row INCONCLUSIVE gives `verdict` PASS, `template_licensed` false, and B keeps the softened sentence. No label is chosen after the counts exist.

**Descriptive, never decisive:**
- per-cell hit counts for C1, C2, C2t, C3, C4 and C5;
- S by dataset and by year;
- the counts with E5 papers added back as inaccessible-relevant.

## 6. Data and machines

**Data.**
- The audit reads public bibliographic metadata and open-access PDFs only.
- No dataset file, image or caption is opened. The one exception is the n-gram scan of §4, which reads the caption files on the laptop to count overlaps and prints counts only.
- No test set is touched, so the one-look rules of the other preregistrations are unaffected.

**Machines.** Laptop CPU only. Neither the test-role machine nor the dev-only machine is used, and nothing is copied to either. No GPU host, address or port appears in this rule or its code.

**Gold labels.** None are created. No AI-silver label is produced or used as evidence.

## 7. Compute and caps

- **GPU:** 0 GPU-h.
- **CPU:** under 1 h on the laptop. Text extraction of about 30–60 PDFs takes minutes, and the patterns take seconds.
- **Requests:** at most 400 API requests in total, spaced at least 3 s apart for Semantic Scholar, with exponential backoff on HTTP 429. This follows the 2026-10-14 R11 limits: the OpenAlex anonymous daily budget and the Semantic Scholar shared pool.
- **PDFs:** at most 300 PDF downloads.
- **Exceeding a cap in S1 (search):** FAULT before the freeze (W7). Unseen candidates cannot be counted; one logged cache-replay rerun (§1.1).
- **Caps are totals over the start and the resume together (CC-210b W2).** The request counters of a resume start from the live requests already logged in `search_log.json` (cached replays do not count). So after a cap FAULT the resume re-hits the cap at once: continuing needs an amendment that raises the cap, before any population text is read. `FAULT.json` also records the sha256 of `toolcheck.json`.
- **Exceeding the PDF cap in S2:** the job continues to S3. The capped-out candidates are counted as inaccessible-relevant if their metadata matches the dataset pattern, and the cap event is logged. This counts as NOT-RUN only if N_acc < 10.
- **Wall cap:** 6 h, including OpenAlex 429 waits. If the OpenAlex budget runs out (a 429 after the retries is a FAULT), the one resume of §1.1 may start on the next UTC day, from the cache, with the same frozen files. The wall cap is checked by the script before each live request, per start (each start and the one resume get their own 6 h); exceeding it is a FAULT at the current step (S1 or S2) with the one resume; an operator SIGINT is also a FAULT (CC-210c W2).
- **Operator (CC-210c W5).** The run is started in a tmux session (the group's practice, OPS-1031e1blaunch), on AC power, with suspend inhibited. If the process ends without FAULT.json, decide.json or cells.json (power loss, SIGKILL, a crash before the first request), the OUT is not deleted, renamed or replaced and no second OUT is created. It is logged as NOT-RUN pending a one-judge ruling, and no population text in it is opened meanwhile.
- **FAULT after the cells (CC-210d W3).** A FAULT at decide or quotes (after `cells.json` exists) has no resume. If `decide.json` is missing, it is computed once, offline and with no network, by the committed `decide()` from `population.json` and the `S` values in `cells.json`, under a one-judge ruling; nothing is re-extracted and no cell is re-run. A FAULT at quotes loses only `quotes.tsv`, which is rebuilt the same way by the committed `write_quotes()`.
- **Expected N:** 15–30 included papers (K21 estimate, not a live count; the search has not run).

## 8. Disclosures (pre-written)

- The authors had read several papers likely to be in the population before this rule was written, at least the UIT-ViIC, KTVIC and UIT-OpenViIC papers (cited in B §2). So the design is not blind to them, and the expected direction ("rarely stated") came from that reading. The mechanical patterns, the frozen search and the T = 0.50 rule are the protection.
- **Asymmetric error, stated plainly.** Pattern misses lower k, which favours PASS. False hits raise k, which favours REFUTES. The patterns are broad to reduce misses, and the tool check tests one positive and one negative text. Neither bounds the miss rate on third-party papers.
- Whole-text matching of the **cells** counts a segmenter cited only in the references as "stated". This is broad and conservative.
- **Inclusion runs on the pre-reference text (W2).** This removes papers that only cite a dataset and a metric, which moves the result away from PASS. `no_ref_heading` papers move it back toward PASS; their count is reported.
- **C1 false hits.** "word-level" also fires on "word-level attention" or "word-level embeddings" (J4). C1t (named tool only) is reported beside C1 so that readers see how much of C1 is generic.
- **C2 and C2t false hits (CC-210 W8).** C2 fires on retrieval-table headers such as "CIDEr R@1" and on author initials such as "CIDEr D. Smith". C2t fires on "COCO caption evaluation server"; the server computes CIDEr-D, so this is read as a fair hit. All three move the result toward REFUTES.
- Relevant E5 papers (metadata or pre-reference full text naming a dataset; CC-210a W8) are inside N_inr in the primary bounds (W5).
- English patterns only. Non-English full texts are excluded (E5) and counted.
- "Accessible" means open access without login on the run date. Paywalled papers are counted as inaccessible, not dropped.
- The result is a count of pattern hits in public text. No human or AI judged or corrected any cell.

### 8.1 Reads and live web calls before the commit (W8 disclosure)

No S1/S2 request of this rule has been made. The table lists every known read of a likely population paper and every live call to the audit's APIs made after v1 was written (v1 file time 2026-10-29 05:16 VN = 2026-10-28T22:16Z). Sources: the decision LOG and commit messages.

| When (UTC) | Who | What | Population contact |
|---|---|---|---|
| 2026-10-28/29 | CC-156 judge | one OpenAlex filter-syntax probe | none (refused: "Rate limit exceeded") |
| 2026-10-29T07:27Z | writer B + one research subagent (CC-163 W6, LOG l.752) | **full texts read and grep-verified:** KTVIC arXiv 2401.08100 (PDF sha256 75619eda…), UIT-OpenViIC arXiv 2305.04166 (c69292e5…), ViCLIP-OT arXiv 2602.22678 (a4b41ef4…); Bromonschenkel arXiv 2602.00393 read as HTML by the subagent; OpenAlex budget exhausted (not used), Semantic Scholar 2 of 8 queries (rest HTTP 429), about 8 web searches | **yes: KTVIC and UIT-OpenViIC full texts** (both Q3 dataset records); ViCLIP-OT probably not included (a retrieval paper; it enters only if it names a caption metric) |
| 2026-10-29T09:15Z | writer B (CC-166 W6, LOG l.767) | HDUCap Crossref metadata (full text 403, no abstract found); OpenAlex 8 and Semantic Scholar 8 queries, all HTTP 429; arXiv API 12 abstract-field queries; 1 extended web search | HDUCap metadata only |
| 2026-10-30 | gatekeeper commit e30e81a (HDUCAP_OVERLAP_2026-10-30) | HDUCap entered into B "from its abstract and publisher preview"; Hussain et al. 2026 (Sci Rep) cited as support | **yes: HDUCap abstract and publisher preview**; Hussain 2026 at least metadata |
| 2026-10-31 ~13:40–13:50Z | v2 writer (B writing gate) | 6 WebSearch queries: Vietnamese captioning audit 2025–2026; two-panel reference style; caption reporting standards; capevalkit; the quoted LRE DOI; Vietnamese LVLM captioning 2026 | snippet summaries naming the UIT-ViIC, KTVIC and UIT-OpenViIC abstract pages (sizes, baseline metric names); **no full text, PDF or evaluation section opened** |
| 2026-10-31 ~15:30–15:55Z | CC-210 judge | documentation only: Semantic Scholar Graph swagger (`/paper/search`, `/paper/search/bulk`, `publicationTypes`); OpenAlex help pages (search entities, work object, work types) | none (no population record, no S1/S2 request) |
| 2026-10-31 ~15:57Z | v3 writer | documentation only: OpenAlex pages `api-entities/works/filter-works` and `api-entities/works/search-works` (confirm the `title_and_abstract.search` filter and quoted phrases); `english_words.txt` written from memory, nothing fetched | none |
| 2026-10-31 ~18:25–18:35Z | CC-210a judge | documentation only: help.openalex.org/api-entities/works/filter-works, …/works/search-works, …/works/work-object, help.openalex.org/data/work-types (25 types confirmed; `filter=field.search:` marked deprecated, still working) | none (no population record, no S1/S2 request) |
| 2026-10-31 ~13:48–13:52Z | v2 writer | Crossref works for 3 ids (10.1007/s10579-025-09814-7, 10.48550/arXiv.2109.13701, 10.48550/arXiv.2408.04909; the last two not in Crossref); arXiv API for 2109.13701, 2408.04909, 1908.07898, 2004.06063, 1804.08771 (two first attempts over http returned nothing parsable); PyPI JSON `capevalkit` | none (non-population records) |
| 2026-10-31 ~19:35–19:47Z | CC-210c judge | documentation only (CC-210b r8): help.openalex.org/api-entities/works/filter-works (last updated 2026-10-29), …/works/search-works (2026-10-28; `filter=field.search:` deprecated, still works; `title_and_abstract.search` still named), help.openalex.org/data/work-types (2026-10-26; 25 types = patterns.json accepted ∪ excluded); 3 WebFetch + 3 curl with the placeholder contact; no difference from the CC-210a read | none (no population record, no S1/S2 request) |
| 2026-10-31 ~20:22Z | CC-210d judge | documentation only (RULE l.55): help.openalex.org/api-entities/works/filter-works (last updated 2026-10-29), …/works/search-works (2026-10-28; `filter=field.search:` deprecated, still works; `title_and_abstract.search` still named; `search.title_and_abstract` documented), help.openalex.org/data/work-types (2026-10-26; 25 types = patterns.json accepted ∪ excluded); 3 curl with the placeholder contact, no WebFetch; page shas byte-identical to the CC-210c read | none (no population record, no S1/S2 request) |

**What this means for the audit.**
- The full texts of two dataset records (KTVIC, UIT-OpenViIC) were read and grep-checked on 2026-10-29, after v1 and before any pattern was frozen.
- That reading looked for cross-dataset training and second panels, not for segmenter or CIDEr-variant statements. Still, the v2 writer cannot rule out that it informed the v2 pattern edits. The v2 edits come only from CC-156 W1–W14, which were written from the B card, FAIR and two bib files.
- The mechanical patterns and the frozen T = 0.50 rule remain the protection (§8).
- None of these calls fixes a pattern, list or threshold of this rule. The CC-210 provenance check found every v2 pattern token predating the 10-29 reads (CC-156, 10-28T22:34Z) or broadening a cell; the CC-210 W4 replacements come from a judge who opened no population text.
- **No further prior-art search that can return population records** (e.g. the CC-163 W6 "re-run OpenAlex when the budget resets" action) runs before the B-α run. If one is needed, it is logged here before the commit (CC-210 W8).

## 9. Pivot condition

B-α is the only zero-GPU route to source B's frequency sentence (CC-147 ruling 2). **The pivot may fire only before S2 (W9).** Once any population text exists on disk, the result is reported whatever the verdict. Before S2: if a judge puts the doubt at ≥ 80% that it can give B a registered evidence line before 11-20, B-α is dropped (UPGRADE_PLAN §6 rule) and B keeps the softened sentence. Examples: the search is expected to yield N_acc < 10, or PASS can license only the weak template and no scorecard credit follows.

There is no fallback experiment, and no gold or AI-silver relabelling replaces it.

**Scorecard credit** is scored after the result (PI-1026ao(3) pattern). CC-147 caps it at novelty +0.5. Evidence credit depends on the verdict.

## 10. Dates

| Step | Date |
|---|---|
| One-judge read of v2 (CC-210, done 2026-10-31); code read (CC-210a, done 2026-10-31); diff reads of the fixes (CC-210b done 2026-10-31; CC-210c done 2026-10-31; CC-210d done 2026-10-31; CC-210e) | by 2026-11-03 |
| Gatekeeper commit (rule, `patterns.json`, script, `SHA256SUMS`), byte-identical to the CC-210e subject | by 2026-11-05 (deadline, not a gate) |
| Run | the first fresh UTC day after the commit (CC-210 ruling 5) |
| Text into B | by 2026-11-20 (only if the writing gate is cleared; otherwise the counts wait in the job folder) |
| B panel | 2026-11-30 (content freeze; LRE submission month per proposal v14: 05/2027, see RESUME_2026-10-31_paperB.md Q2) |

## 11. Judge items: resolved by CC-156 (2026-10-29)

| Item | CC-156 ruling | Where v2 applies it |
|---|---|---|
| J1 | census with inaccessibility bounds; no Clopper–Pearson interval | §5 unchanged |
| J2 | T = 0.50 and the three-way rule upheld; INCONCLUSIVE and REFUTES **must** be reported | §5 table (W9) |
| J3 | C2t counts only in the scorer-code form | §2 C2t (W1) |
| J4 | C1 stays broad; add the descriptive C1t | §2 C1t (W13), §8 |
| J5 | cross-paper cell not adopted | §2 unchanged |
| J6 | Vietnamese texts excluded, counted in N_inr | §1.4 E5 (W5) |
| J7 | dataset papers are in the population | §1.1 Q3 unchanged |
| J8 | open access without login only | §1.2 unchanged |
| J9 | C3 is descriptive only | §2 unchanged |
| J10 | E3 by a frozen identifier list, not author name | §1.4 (W6) |
| J11 | plain `pdftotext` + de-hyphenation; T1 via pandoc to PDF | §1.2, §3 (W3, W11) |
| J12 | (a)–(e) met after W4, W5, W7, W12 | §1.2 (W4), §1.4 (W5), §1.1 and §7 (W7), §4 (W12) |

Open items: none from v1. CC-210 and CC-210a items are closed in `JUDGE_READ_REQUEST_CC210a.md` and `JUDGE_READ_REQUEST_CC210b.md`.

## Amendments

(none; v2 is a pre-commit revision of the draft, not an amendment)
