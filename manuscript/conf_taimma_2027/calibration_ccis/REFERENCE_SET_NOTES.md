# Reference set notes — CCIS calibration

Written 2026-11-14 (UTC), 2026-11-15 03:58 Vietnam time. This file names the papers, so it is not for scorers. Ids and full references are in `KEY_DO_NOT_SHOW_SCORERS.md`.

## 1. What was asked and what was delivered

- Asked: three to five recent (2024–2026) papers from CCIS volumes, on applied AI or NLP near the draft's topic, each with a public full text that was read in full, each verified as a CCIS chapter.
- Delivered: five papers, five cards (`cards/R1.md` to `cards/R5.md`). All five are verified CCIS chapters (volumes 2964, 2915, 2150, 2533, 2395). All five cards were written from the arXiv preprint of the same paper, because all five published chapters are behind the paywall.
- Not done: no scoring, no reading of the draft, no commit.

## 2. Search

Source: OpenAlex works search, filter `primary_location.source.issn:1865-0929` (the CCIS print ISSN) and `publication_year:2024-2026`. The first 25 results of each query were read by title. Citation counts were not used.

| query | open-access filter | hits |
|---|---|---|
| image captioning | no | 150 |
| vision-language model evaluation | no | 544 |
| Vietnamese | no | 185 |
| retrieval-augmented generation | no | 436 |
| image captioning | yes | 71 |
| caption | yes | 79 |
| in-context learning | yes | 1,317 (mostly unrelated matches on "context" and "learning") |
| hallucination | yes | 126 |
| low-resource language | yes | 266 |
| visual question answering | yes | 196 |
| large language models evaluation benchmark | yes | 433 |
| multimodal large language model | yes | 227 |
| Vietnamese | yes | 36 |
| retrieval-augmented | yes | 198 |
| few-shot prompting | yes | 188 |

Selection rule: keep a paper when (a) the title is on one of the four topics of the task (captioning or vision-language evaluation; retrieval-augmented or in-context generation; low-resource Asian-language NLP; empirical evaluation with statistical testing), (b) OpenAlex lists a second location with a public full text, (c) the full text could be fetched and read. Among kept papers, at most one per research group and one per topic slot, so that the five cards cover the four topics. The order of the five ids was shuffled at random afterwards.

## 3. Candidates not used

### Full text was fetched but no card was written (reserve; these four were downloaded and not read)

| DOI | title | preprint | reason |
|---|---|---|---|
| 10.1007/978-981-92-2597-2_32 | CIAN: Multi-stage Framework for Event-Enriched Image Captioning via Retrieval-Augmented Generation | arXiv 2606.17430 | same volume, same senior author and same challenge as R2; a second card would count one group twice |
| 10.1007/978-981-96-4282-3_11 | VisChronos: Revolutionizing Image Captioning Through Real-Life Events | arXiv 2606.24058 | same senior author as R2 |
| 10.1007/978-3-031-70259-4_14 | Fusing Visual and Textual Representations via Multi-layer Fusing Transformers for Vietnamese Visual Question Answering | arXiv 2610.01637 | same senior author as R1 |
| 10.1007/978-981-96-4291-5_31 | Improving Vietnamese Legal Document Retrieval Using Synthetic Data | arXiv 2412.00657 | text retrieval only; further from captioning than the five kept |

These four are usable if the set must grow or a card must be replaced. Crossref confirms each as a CCIS chapter (series title and ISSN); their volume numbers were not looked up.

### On topic, a public copy is listed, not fetched (five papers were already in hand)

| DOI | title | public copy listed by OpenAlex | reason |
|---|---|---|---|
| 10.1007/978-3-032-37933-7_22 | Accuracy is not Enough: Counterfactual Robustness Analysis for Vietnamese Hallucination Detection | a university repository | text-only, judged from the title, not read; volume print year 2027 |
| 10.1007/978-3-031-80839-5_16 | Exploring In-Context Learning: A Deep Dive into Model Size, Templates, and Few-Shot Learning for Text Classification | HAL | R3 already covers in-prompt examples; 9 pages |
| 10.1007/978-981-95-4788-3_8 | LLM-Based Evaluation of Low-Resource Machine Translation: A Reference-less Dialect-Guided Approach with a Refined Sylheti-English Benchmark | arXiv 2505.12273 | R5 already covers low-resource evaluation; 9 pages |
| 10.1007/978-981-92-0068-9_9 | End-to-End Chatbot Evaluation with Adaptive Reasoning and Uncertainty Filtering | arXiv 2603.10570 | same volume as R1; chatbot evaluation, judged from the title, not read |
| 10.1007/978-981-96-1024-2_8 | Evaluation of Retrieval-Augmented Generation: A Survey | arXiv 2405.07437 | a survey, not an empirical paper |

### On topic, no public full text found in OpenAlex (status "closed", no second location; no further search for author copies was made)

| DOI | title |
|---|---|
| 10.1007/978-3-031-93709-5_3 | Leveraging English Captions for Improved Image Captioning in Low-Resource Languages |
| 10.1007/978-3-032-28454-9_32 | Cross-Lingual Benchmarking for Image Captioning: Assessing Translation in Low-Resource Settings |
| 10.1007/978-981-96-9961-2_1 | HRACap: Lightweight Image Captioning via Hierarchical Retrieval-Augmented Prompt |
| 10.1007/978-981-96-7008-6_26 | HinglishCap: A Code Mixed Hindi-English Image Captioning Framework |
| 10.1007/978-3-031-93709-5_15 | Bangla Chitra Net: An Efficient Transformer-Based Architecture for Image Captioning |
| 10.1007/978-3-032-05855-3_35 | Medical Image Captioning in Tamil Using BLIP Model |
| 10.1007/978-981-92-2600-9_24 | SelfCheckHybrid: A Hybrid Framework for Hallucination Detection in Vietnamese Large Language Models |
| 10.1007/978-3-032-21631-1_36 | TVM-SimpleQA: A Factuality Evaluation Dataset for Traditional Vietnamese Medicine |
| 10.1007/978-3-032-14674-8_9 | Optimizing Retrieval Strategies for Vietnamese Legal RAG Systems |
| 10.1007/978-981-95-4724-1_35 | Vision-Based Large Language Models for Vietnamese Handwriting Recognition |

By title, the first three of this list are closer to the topic named in the task than R3, R4 and R5. They could not be used under the rule "no card from an abstract alone".

## 4. Weaknesses of the set

1. **Preprints, not published chapters.** Every card comes from the arXiv version. For R2, R3 and R4 the preprint is in the proceedings layout with the same or nearly the same page count as the chapter. For R1 (11 preprint pages against 15 published) and R5 (7 two-column pages against 12 published) the layout differs and the chapter may contain material that the card does not show. Each card may therefore understate its paper a little.
2. **Selection on open preprints.** Of 150 CCIS hits for "image captioning", 71 are marked open access; the set draws only from that half. Groups that post preprints may differ from the series average, in either direction. The set is a sample of readable CCIS papers, not of all CCIS papers.
3. **Topic distance.** Only R2 is on retrieval-augmented image captioning. R1 is Vietnamese vision-language work but on question answering. R4 is captioning of scientific figures, not photographs. R3 and R5 are text-only. No card is about evaluation of Vietnamese image captioning, and none is a preregistered study.
4. **Unequal venues inside one series.** CCIS takes proceedings of very different events. Figures read on the publisher's book pages: SOICT 2025 (R2) 119 full and 117 short papers from 345 submissions, across five parts; ACIIDS 2026 (R1) 81 full papers in this part from 431 submissions; AI4Research 2025 (R4) 8 full papers from 35 submissions. R3 is in the volume for posters, late-breaking results and other secondary tracks of its conference, whose main track is, to my knowledge, published in another series (not checked here), so R3 probably passed a lighter review than a main-track paper. For IMLIP 2024 (R5) a search snippet gave 30 full papers from 144 submissions; this figure was not confirmed on the publisher page. Whether R2 was accepted as a full or a short paper is not marked; its length (14 pages) suggests a full paper.
5. **Small set.** Five cards give a wide uncertainty on a "venue mean"; one unusually strong or weak card moves the mean by a fifth of its distance.
6. **Countries and groups.** R1 and R2 come from the same university in Vietnam (different senior authors); R3 Japan; R4 Korea and the United States; R5 China.
7. **Year of R2.** Online on 2026-08-15, but the volume's copyright year is 2027. It meets the 2024–2026 window by online date only.
8. **Card format differs slightly from 10 Nov** ("Key numbers" on every card; `venue` = "international conference"). The card of the draft must use the same format, or the scorer can tell it apart. See the notes in the key file.
9. **One reader.** The cards were written by one agent; no second reader checked the numbers against the preprints. The numbers in "Key numbers" were copied from the preprints' tables in layout-preserving text extraction and re-read once; the two regression tables of R3, whose significance marks were detached in the extraction, were checked against a rendered image of the page.

## 5. Things that could not be verified

- The text of the published chapters (paywall): not read for any id.
- Whether the published R1 and R5 differ from their preprints beyond the abstract.
- The R5 acceptance figures (search snippet only).
- CCIS volume numbers of the four reserve papers (series confirmed by Crossref; number not looked up).

## 6. Requests and errors

| target | tool | result |
|---|---|---|
| api.openalex.org (15 searches, with the project key, no contact address) | Python urllib | no error |
| api.crossref.org (12 chapter and 9 book records, no contact address) | Python urllib | no error; volume field empty in all records |
| arxiv.org/pdf and arxiv.org/abs (9 papers, 5 s spacing) | curl | no error |
| link.springer.com book page | curl | HTTP 200 but a "Client Challenge" page, no content |
| link.springer.com chapter and book pages (10 URLs) | web-fetch agent | HTTP 303 to the publisher's login service; not followed |
| dblp.org search API (10 queries) | Python urllib, curl | a bot-check page, then HTTP 429; not used |
| four bookseller pages for the volume number | curl | HTTP 429 or 403; not used |
| link.springer.com book pages (5) and chapter pages (5) | clean headless browser, no login | loaded; series line, volume number, title, authors, pages and the public abstract were read |

No login anywhere, no personal identifier, and no e-mail address in any request. Downloaded PDFs and page copies are in the session scratch folder only, not in the repository.
