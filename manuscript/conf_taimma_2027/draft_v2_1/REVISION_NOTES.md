# REVISION_NOTES: TAIMMA draft v1 to v2 of Paper C

Written by the revising writer (an agent), 2026-11-15. Draft only: no tex, no build, no commit, nothing sent. `draft_v1/` is byte-unchanged (all six files re-hashed after the work).

Specification: ruling CC-399 (round 1, NEXT_ROUND). This revision covers the text items B1 to B6, the cuts of ruling 6 and the cheap NON-BLOCKING items. The gates G1 (page count), G2 (re-join after K7) and G3 (rubric) are not part of it.

## 1. Files and state

| File | sha256 |
|---|---|
| `paper.md` | d97cd24aa89d1384f9becab414c2e290fd61f8985177e49f99c1f647ef641e08 |
| `number_manifest_TAIMMA.tsv` | 506ab1d6a9a7ff5d042b865314776b2d9e7130454ef4d1cef061fba9ce5cb6c6 |
| `PARAGRAPH_SOURCES.tsv` | c5f2fa689651729027b11a8eae94c21aeacf308e7fdfb087403cee68b1b0bb3e |
| `CHECKS.md` (output of the last checker run) | 160f25f5604d908ef9b963ed99026938aa3439a0f03fe02708f4f23204f22159 |
| `V1_TO_V2.diff` | d5f80398f5d001a12fbc43b93cdb25fe3c91b9be0ff956e6848ca3a7592a4205 |
| `check_draft.py` (byte-identical to v1) | 281e087565af30c0ba8ae62dc56d466b4d9c85659d09e822a7666c8300bda21f |

`V1_TO_V2.diff` holds three unified diffs in this order: `paper.md`, the manifest, `PARAGRAPH_SOURCES.tsv`.

**The Paper C repo moved during this revision.** It was at d558df0 with an uncommitted update when the work began. Three commits were then made there by another writer: 6a5d36a, 9b8e6ae (2026-11-14T23:50Z) and 55315ca (2026-11-15T02:26Z, related work only).

- Every journal sentence used below was re-read with `git show d558df0:paper_v1_analysis/<file>`, pinned to the commit and not to HEAD. All line numbers below are d558df0 line numbers. At 9b8e6ae several of them have moved (05 l.64 is no longer the XM-a row; 07 l.46 is empty).
- `check_draft.py` reads the working tree of that repo. The last `--build-manifest` and the last check therefore read the journal manifest of 9b8e6ae (sha 83414dc3…), not that of d558df0 (83a9ebc3…).
- Effect on the conference manifest, measured: all 295 rows have the same number, key, raw value, sha prefix and status as at d558df0. One row (`60`, max new tokens) carries the newer `used_in` cell, which adds the supplement file. No other cell differs.
- The journal manifest and the bib are unchanged between 9b8e6ae and 55315ca, so the last check stands at 55315ca.
- Nothing from the three commits entered the draft, and no block-2 or attribution development result is in it (ruling 2 guard).
- For G2 only, seen while comparing the commits:
  - at 9b8e6ae, `06_results.md` l.93 now states the H_G pass rule in words, with the same two conditions as the sentence added here for N4;
  - at 55315ca, the two Table 1 rows used for B6 (02 l.37, l.39) are byte-equal to d558df0; the MUNIChus row of Table 1b changes its "registered" cell from "–" to "no" (the conference Table 1 says "not stated").

## 2. BLOCKING text items B1 to B6

Source column: file and line under `paper_v1_analysis/` at d558df0.

| Item | Marker | OLD | NEW | Source | Status |
|---|---|---|---|---|---|
| B1 | T4, XM-a row, rule cell | PASS if the lower bound is above zero | PASS if the lower bound is above zero; a positive point with a CI that includes zero is printed as a descriptive number only | `05_preregistration_and_analysis.md` l.64 | applied as ruled |
| B1 | S5-06 | …but the rule required a CI above zero and the CI includes zero. The registered sensitivity… | …but the rule required a CI above zero and the CI includes zero. Under the registered rule this point is a descriptive number only. The registered sensitivity… | `06_results.md` l.61 | applied as ruled |
| B2 | S4-03 | The smallest effect size of interest (SESOI) is +2.0 points, a planning value set before any stage-B output and derived from no earlier result. | The smallest effect size of interest (SESOI) is +2.0 points, a planning value set before any stage-B output; it equals the stage-one value (stages one and two are stages A and B in the registrations' numbering); the stage-two registration states that it was not derived from the stage-A pilot or any stage-one number, and no calibration is recorded. | `05_preregistration_and_analysis.md` l.52 | applied; two departures from the ruled sentence, see section 7, points 1 and 2 |
| B3 | S7-D04 | *English SESOI.* The +2.0 was carried over numerically, without recalibration to the PTB scale. | *English SESOI.* The +2.0 was carried over numerically, without recalibration to the PTB scale; because English scores are higher, it is relatively more lenient on COCO. | `08_english_comparison.md` l.11 | applied as ruled |
| B4 | S7-D02 | …Another study had decoded some XM-dev500 images zero-shot (stage B only). | …(stage B only). In English, a companion study had scored on the COCO Karpathy test, part of that test had been decoded zero-shot earlier, and another study had decoded the NoCaps images that the registered 3,500-image sensitivity removes; none of those outputs is re-used, and no design choice follows from them. | `08_english_comparison.md` l.86 | applied as ruled, in words; see section 7, point 3 |
| B5 | S7-L06 | …results of the systems as run, in fixed batches. A check before the test… | …in fixed batches. A per-image difference between arms decoded in batches can contain a batch-mate term, and the image bootstrap does not model the coupling of images within a batch slice. A check before the test… | `09_limitations.md` l.11 | applied as ruled; nothing else in S7-L06 was touched (unit C44 waits for K7) |
| B6 | S2-04 | For Vietnamese, earlier work trains or adapts captioners [three keys]; this study trains nothing. | Two multilingual retrieval-augmented captioners list Vietnamese among their languages, one of them training-free, and neither has a random control [@Ramos2023LMCap; @Ibrahim2025CONCAP]. Other Vietnamese work trains or adapts captioners [three keys]; this study trains nothing. | `02_related_work.md` l.37 and l.39 (Table 1 rows), l.7 | applied; see section 7, point 4 |

Qualifier of dissent D-b (the chair recommends it in the same diff):

| Marker | OLD | NEW | Source |
|---|---|---|---|
| S6-01 | committed before any English image was decoded | committed before any English image was decoded for this arm | `08_english_comparison.md` l.82 and l.86 |
| S7-D03 | before any English decode | before any English image was decoded for this arm | same |

## 3. Cuts of ruling 6 (the six candidates)

Words are running-text words by the checker's counting rule.

| Candidate | Marker | What was done | Words |
|---|---|---|---|
| Abstract to about 210 | ABS-01 | Seven wording cuts (full text in the diff): "in the prompt of a multimodal model" to "in a multimodal model's prompt"; "from seeing any in-domain caption and not from retrieval" to "from any in-domain caption, not from retrieval"; "each reported separately" to "reported separately"; the P1 rule in brackets dropped ("point above +2.0 and CI above zero"; both FAIL rules stay); the scope sentence joined to the PASS as one clause; "against each model's own zero-shot captions" to "against zero-shot"; "With the frozen configurations carried to English" to "In English, with the frozen configurations". Both FAILs keep estimate, CI and rule. | 233 to 212 |
| S1-06, S1-07 | S1-06 | OLD: "…and on the COCO Karpathy test (+3.08 [2.08, 4.03] PTB CIDEr-D points; P1-EN PASS)." NEW: "…and on the COCO Karpathy test (P1-EN PASS)." The P1 estimate stays: the checker's A.5 list (claim-map row C07) needs P1 with estimate, CI, PASS and scope sentence in the introduction. | 94 to 88 |
| | S1-07 | Unchanged. Both sentences are the two registered FAILs with estimate, CI and rule (plan A.5). | 54 |
| S8-03 | S8-03 | OLD: "On OpenViIC test `ret` − `zs` is +14.30 [13.38, 15.24], and, descriptively, random in-domain examples already score well above zero-shot. Crediting such a gain to retrieval needs a random-example control at equal k from the same memory, the result for each backbone, and a check of whether the memory's captions share the target set's source. The predictions passed only there, but source and test set changed together and Qwen2.5-VL's out-of-source rows stayed above zero: an observation, not a tested cause." NEW: "Descriptively, random in-domain examples already score well above zero-shot (Sect. 5.3). Crediting a gain over zero-shot to retrieval needs a random-example control at equal k from the same memory, the result for each backbone, and a check of whether the memory's captions share the target set's source (here an observation, not a tested cause; Sect. 6)." The +14.30 stays in S5-08; the confound stays in S6-04 and S7-L02. See section 7, point 5. | 79 to 56 |
| S7-D11 into S7-D12 | S7-D12 | One bullet: "*Not reported here.* Registered secondaries, none a verdict: the cosine dose-response, the style report, the source share of shown examples and neighbour-only object precision. Later registrations: a Flickr30K baseline comparison, development ablations, a development attribution analysis, and an exploratory filtering diagnostic that ended by its registered stop rules." Marker S7-D11 and its source row are removed. | 52 to 48 |
| S7-D07, S7-D08 | – | **Unchanged, byte-equal to v1.** Clause forms were tried; the best saved 3 words (48 against 51), because the two bullets hold four facts and no filler. Both are disclosures, so they were left as they were. | 51 |
| S3-03 to S3-05 | – | **No net cut.** S3-03 is unchanged: every clause is needed to read Table 2 or states the design. S3-04 and S3-05 grew by the two NON-BLOCKING additions of section 5. | 291 to 313 |

The six candidates give 54 words, not the 350 to 400 the ruling expected. Most of the named text is plan A.5 content or a disclosure.

## 4. Cuts beyond the six candidates

Each is a deletion of text that repeats a cell of the table in the same section (or, for S4-01, a sentence of S6-01 and Table 3). No label, verdict or number leaves the paper. Each can be put back from the OLD text alone.

| Marker | Removed | Where the content stays | Words |
|---|---|---|---|
| S4-01 | " The English memory is built from COCO training data, and the English test sets are the COCO Karpathy test and NoCaps val." | Table 3 (three rows), S6-01 | −22 |
| S5-02 | " (length gaps 0.074 and 0.039)" | Table 6, rule L row; "Rule L does not fire." stays | −5 |
| S5-06 | " InternVL3 at τ = −∞ gave +0.18 [−1.36, 1.81], not detected (sensitivity +0.19 [−1.41, 1.79], not detected)." | Table 6 (plan A.5 places this label in the results tables) | −14 |
| S5-07 | " (sensitivity +0.57 [−0.41, 1.56], PASS)" | Table 6, XM-b row | −5 |
| S6-02 | " (length gaps 0.019 and 0.019)" and " Without the deletion step its row is −1.05 [−2.22, 0.08], not detected." | Table 7 | −17 |
| S6-03 | " Per backbone (reported rows), Qwen2.5-VL gave +2.83 [1.69, 3.98] and InternVL3 +0.62 [−0.37, 1.62]; InternVL3 at τ = −∞ is not detected on either NoCaps set." | Table 7, Fig. 1 | −23 |
| | | **Total** | **−86** |

Kept in the text on purpose: the sensitivity of each registered FAIL (S5-06, S6-03), InternVL3's below-zero rows on XM-test2500 and COCO (plan A.5: tables and text), and S5-04 (plan A.5, row C16).

The claim lists of S4-01, S5-06, S6-02 and S6-03 in `PARAGRAPH_SOURCES.tsv` lost the claim ids whose numbers they no longer print (C32; C20; C35; C39 and C40). Each is still carried by its table.

## 5. NON-BLOCKING items applied

| Item | Marker | OLD | NEW | Source |
|---|---|---|---|---|
| N4, H_G pass rule | S3-05 | …the guard hypothesis H_G was not passed (pooled precision change +2.91 [0.46, 5.31] points, at a stripped CIDEr-D cost of −4.01). | …the guard hypothesis H_G was not passed: it needed a precision change with a CI above zero and a stripped CIDEr-D cost within a registered bound, and the cost, −4.01, lay outside that bound (pooled precision change +2.91 [0.46, 5.31] points). | Not in Paper C at d558df0 (06 l.93 prints the label and the numbers only). Rule from the stage-2 registration, section 7.5, run repo `manuscript/prereg/2026-10-22_c_stage2/PREREG.md` l.330–332. See section 7, point 6 |
| N5, caption | F1 | …a different quantity on each scale. | …a different quantity on each scale; the XM-a rule had no point threshold. | `05_preregistration_and_analysis.md` l.64; `08_english_comparison.md` l.11 |
| N6, labels | S5-10 | **Copy baselines and tokenisation.** | **Copy baselines and tokenisation (registered secondaries, non-gating).** | `05_preregistration_and_analysis.md` l.95–100 |
| N6, narrowing | S5-10 | …not simply returning a neighbour's caption. | …not simply returning a neighbour's whole caption. | `06_results.md` l.75 |
| N7 | S5-05 | …+4.47 [3.44, 5.41] on 1,929 queries, and… | …on 1,929 queries (per-image scores as stored; document frequencies not recomputed), and… | `06_results.md` l.41 |
| N7 | S6-02 | …for InternVL3 (reported rows). | …for InternVL3 (descriptive rows). | `08_english_comparison.md` l.45 |
| N8, names | T1 | bare keys in column 1 | "Yang et al.", "Li et al.", "Baldassini et al.", "Li et al.", "Chen et al." before the keys | author fields of `paperC.bib` (five or more authors each) |
| N8, Baldassini | T1 | yes, equal shots | yes, equal shots (IDEFICS) | `02_related_work.md` l.58 |
| N10, plain names first | S3-04 | below τ | below a threshold τ | – |
| | S3-07 | because P2 uses it | because the object-precision prediction P2 uses it | – |
| | S4-01 | The primary OpenViIC test set is | The primary OpenViIC test set (OV-test primary) is | Table 3 |
| | S4-02 | checked them on OV-dev-A. Stage B gave one look at OV-dev-B | checked them on one half of the OpenViIC development set (OV-dev-A). Stage B gave one look at the other half (OV-dev-B) | `04_data_and_splits.md` l.11–12 |

Cost in running words: N4 +20, plain names +17, N7 +8, N6 +4; 49 in all. T1, T4 and the Fig. 1 caption are counted apart from the running text (cells +32, captions +7).

## 5a. Full-text check and search (added after the first v2, on the lead's order)

Sources: `manuscript/reviews/RELATED_FULLTEXT_CHECK_2026-11-15.md` (sha 8fa296dd…), blocks T-1 to T-3 of its section 3.4, and `manuscript/reviews/C_SYSTEMATIC_SEARCH_2026-11-15.md` (sha acdae5aa…), section 5.3. Both were written against draft v1; none of the four edits meets a CC-399 item.

| Block | Marker | OLD | NEW | Words |
|---|---|---|---|---|
| T-1 | T1, MUNIChus row, last cell | not stated; no | no; no | cells −1 |
| T-2 | T1 caption | Entries follow each paper's own statements. | Entries follow each paper's own statements; a language cell gives the language of the caption data where a paper does not name it, and a cell that reads *no* means that a search of the paper's full text found no such statement. | caption +36 |
| T-3 | S1-02 | …multilingual news captioning (Sect. 2). | …multilingual news captioning (Sect. 2, Table 1). | +2 |
| Search 5.3 | S2-05 | Vietnamese captioning with training-free models; example captions shown as text only; an equal-k random control… | Vietnamese captioning with training-free models; an equal-k random control… | −6 |

- **T-2 departs from the block in one mark.** The block writes "no" in quotation marks; the checker allows only registered labels and defined terms in quotation marks, so v2 writes *no* in italics.
- **No Baldassini qualification was applied, because the conference draft has nothing to qualify.** The majority-vote sentence is journal text (02 l.20) and is not in this draft; S2-02 only says that in-context learning "is reported to be driven mainly by the text of the examples", which the check confirms. The Table 1 cell already reads "yes, equal shots (IDEFICS)" (section 5).
- **Open for the next round, not applied (no new reference, no new table row in this round):** the sentence and citation for the shared-task radiology study that also shows captions as text (search 5.3, for S2-05); the clause for the second English precedent (for S2-03); the candidate new rows of Table 1.
- "Captions as text" stays in the design sentences (S1-03, S1-05) and in the last row of Table 1; only the claim that it is specific to this study is gone.

## 6. NON-BLOCKING items skipped

| Item | Why |
|---|---|
| N2, credits to the companion scoring study (S3-06 kit, S3-04 class map) | It names a second unpublished companion manuscript in a conference paper. How companion manuscripts are named is with the investigator (decision D8; question Q2 of the ruling). Ready wording, from `03_method.md` l.76 and l.42: "All arms are scored with the companion scoring study's kit." and "…a yes/no question built from the fixed English class map of the companion scoring study's verifier protocol, used unchanged…". The third credit (S3-07, count-matched precision) is already in v1. |
| N3, list of protected sets (S3-01) | It adds about 30 running words to a section that ruling 6 asks to trim, and the v1 sentence is a correct summary. Ready wording, from `03_method.md` l.9: "…unreadable files, images identical or near-duplicate to an image of a protected set (the KTVIC test and development images, the OpenViIC development and test images, and all XM3600 images), and images on a pre-fixed exclusion list of other evaluation images." |
| N5, figure rebuild and hand check of plotted values | A figure build; it belongs to the build step. |
| N8, MUNIChus cell ("image and article excerpt") | Settled by the full-text check, not by this revision: its row T-16 confirms the v1 cell "image, article excerpt and caption" on the proceedings PDF, so the cell stays. |
| N8, KTVIC dev299 size in Table 3 | The number has no row in Annex D1 of the plan, so the manifest build cannot carry it. It needs an Annex row. |
| N9, more citations | Hard rule of this revision: no new reference. Two of the keys are not audited. |
| N10, other referee sentences (stage-A selection rule, why the pooled primary, deployment use, "available on request", venue topics) | No ruled wording; each is a new sentence or the investigator's decision D9. |
| N11, restamp and marker stripping | Steps of the G2 re-run and of the build. |
| N15, "(post hoc)" tag on the leniency sentence | Optional. The B3 clause is taken from 08 l.11, the registered-rules paragraph, and prints no pointer to the power paragraph. |

## 7. Where v2 departs from the ruled wording (for the diff read)

1. **B2, numerals as words.** The ruled sentence writes "stage-1" and "stage-2". The checker reads the digit after a hyphen as a number that needs a manifest row, and no such row exists. v2 writes "stage-one" and "stage-two"; nothing else in the sentence differs.
2. **B2, a gloss of thirteen words.** "stage one" and "stage two" are not defined in this draft, which names its stages A and B. The gloss says they are the same. Evidence: Paper C `05_preregistration_and_analysis.md` l.34–37 (stage A: design note, KTVIC dev299 and OV-dev-A; stage B: registration, OV-dev-B) and the stage-2 registration itself (run repo `manuscript/prereg/2026-10-22_c_stage2/PREREG.md` l.1–3, l.13, l.68; SESOI provenance at l.284–285). For the investigator's rewrite, a shorter form says the same: "it equals the stage-A value; the stage-B registration states that it was not derived from the stage-A pilot or any stage-A number, and no calibration is recorded".
3. **B4, counts.** The two counts of 08 l.86 (the Karpathy images decoded earlier; the NoCaps images of the other study) are not printed, so no manifest row was added. "3,500-image" is printed as in the ruled text. Its row already existed (claim C32); S7-D02 now carries C32 and the rebuild added §7 to that row.
4. **B6, two words left out.** The count of languages is not printed: S2-04 carries no claim id, so the checker cannot key a number there, and v1 left such counts out (DRAFT_NOTES section 3, item 3). The system name is not printed in the prose: the checker's list of journal-only words holds it, and the citation carries it.
5. **S8-03, a nine-word tag kept.** The ruling drops the restated confound. v2 drops the sentence and keeps "(here an observation, not a tested cause; Sect. 6)", so the conclusion does not read as a causal claim.
6. **N4, source and one inference.** The rule comes from the registration, not from Paper C at d558df0. "lay outside that bound" compares the keyed cost (−4.01) with the registered bound; the bound's number is not printed, so no row was added.
7. **Manifest, value match in the abstract.** The abstract now prints +2.0 once, for NoCaps. The rebuild matches by value, so the Vietnamese SESOI row still lists the abstract. It is the same registered value, carried over numerically.
8. **`CHECKS.md` title.** It reads "draft v1" because the title is a fixed string in the unchanged checker. The `paper.md` sha in its header is that of v2.

## 8. Words, before and after

| Section | v1 | v2 | Budget | v2 against budget |
|---|---|---|---|---|
| Abstract | 233 | 212 | 200 | +12 |
| §1 | 509 | 505 | 500 | +5 |
| §2 | 333 | 346 | 330 | +16 |
| §3 | 680 | 705 | 620 | +85 |
| §4 | 563 | 587 | 560 | +27 |
| §5 | 713 | 712 | 700 | +12 |
| §6 | 385 | 348 | 380 | −32 |
| §7 | 609 | 698 | 540 | +158 |
| §8 | 229 | 206 | 160 | +46 |
| Declarations | 202 | 202 | 110 | +92 |
| **Running text** | **4,456** | **4,521** | **4,100** | **+421** |
| Table cells | 836 | 867 | – | – |
| Captions and notes | 312 | 355 | – | – |

Where the 65 words come from:

| Cause | Words |
|---|---|
| B1 to B6 and the D-b qualifier | +160 |
| NON-BLOCKING items applied | +49 |
| Cuts of the six candidates | −54 |
| Cuts beyond the six candidates | −86 |
| Full-text check and search (section 5a) | −4 |
| **Net** | **+65** |

**The 4,100 target is not reached, and it cannot be reached without cutting required content.** §7 is 158 over its budget: B3, B4 and B5 add 88 words to eleven disclosures, seven limitations and the compute line, none of which may be cut. The declarations are 92 over with the `[PI]` placeholders and the data statement of CC-392 N11. These two overshoots are 250 of the 421 words. The other sections hold the definitions, rules and results that the plan requires, and what could honestly go from them has gone (sections 3 and 4).

Still available, not applied:

- Re-wording that drops numerals repeated from a table: S5-04 first sentence, S6-03 domain rows. About 20 words. They are re-wordings, not deletions, so they were left for a ruling.
- The conditional cuts of plan section B, only if the compiled PDF exceeds 15 pages and in that order: the English rows of Table 5, Table 1, C42 (about 37 words), C28 (about 31), C27 to one clause (about 25).

## 9. Checker summary (last run, 2026-11-15T04:17:18Z; full output in `CHECKS.md`)

Commands, run inside `draft_v2/`: `python3 -I check_draft.py --sync-first-words`, then `python3 -I check_draft.py --build-manifest ../WRITING_PLAN_C_TAIMMA_v1.md`, then `python3 -I check_draft.py > CHECKS.md`. The build was repeated after the last text edit and gave a byte-identical manifest.

| Check | Result | Measured |
|---|---|---|
| Paragraph markers and PARAGRAPH_SOURCES.tsv | PASS | 79 units, 79 rows, 54 of 54 claim-map rows carried |
| Limits known today | PASS | title 14 words, abstract 212 words, 5 keywords, 7 tables, 1 figure |
| Plan word budgets | **FAIL** | running text 4521 against 4100; over: Abs +12, §1 +5, §2 +16, §3 +85, §4 +27, §5 +12, §7 +158, §8 +46, Decl +92 |
| Numbers keyed | PASS | 417 numeric tokens, 0 without a row |
| Estimate and CI read from one key | PASS | 86 triples, 0 without a single key stem |
| Manifest rows equal the source manifest and are all printed | PASS | 295 rows (27 label rows), 0 problems |
| Registered negatives and labels (plan A.5) | PASS | 24 required statements, 0 missing |
| Citation keys exist in the bib | PASS | 34 keys used, 0 not in the bib (67 entries) |
| No host or IP pattern | PASS | 0 hits |
| No writing-tool statement | PASS | 0 hits |
| No promotional word | PASS | 0 hits |
| No journal-only content | PASS | 0 hits outside the allowed sentences, 4 allowed |
| No data-set caption text | PASS | 0 Vietnamese letters, 0 unexpected quoted strings |

Twelve of thirteen pass. The word-budget check is the one failure and cannot be fixed here (section 8). The manifest build found 303 of 303 Annex D1 pairs and left the same 7 unprinted as in v1.

Against v1: 28 fewer numeric tokens and 8 fewer triples (the cuts of sections 3 and 4); the same 295 manifest rows, of which 8 changed: 7 in their section list (the three `ret` − `zs` rows lose §8, the three P1-EN rows lose §1, the 3,500 row gains §7) and 1 in its `used_in` cell (section 1).

## 10. Not touched

- Unit C26: the Table 5 dagger note and S5-09 are byte-equal to v1.
- Unit C44: S7-L06 has the B5 sentence and no other change.
- S1-07, S3-03, S3-06, S5-08, S7-D07, S7-D08, S8-01, S8-02 and all declarations with their `[PI]` placeholders are byte-equal to v1.
- No label folder, key file, sealed folder or held folder was opened. No scoring, model or data script was run. The only script run was `check_draft.py`: its three modes, and its own word counter called once per folder for the per-paragraph counts of sections 3 to 5. That call left a `__pycache__` folder in `draft_v1/` and in `draft_v2/`; both were removed, and `draft_v1/` again holds its six files only.
- One file outside Paper C was read for wording: the stage-2 registration (sections 7.1 and 7.5, and its header), for the N4 rule and the stage numbering.

## 11. Open, outside this revision

- G1: no template build, so no page count. At about 450 words a page (plan section B), 4,521 words is close to one page above the plan's 13.8-page estimate, so the 15-page cap is at risk.
- G2: after K7, re-run the build and the checks on the new Paper C HEAD, re-check C26 and C44, refresh the source pointers (they are d558df0 pointers), and move the N4 source to the journal line.
- G3: rubric and expert review.
