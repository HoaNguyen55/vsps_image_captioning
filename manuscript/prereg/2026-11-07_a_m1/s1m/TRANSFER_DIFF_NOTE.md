# A-M1 transfer to the paper repo: diff note for the one-judge diff read (CC-289r2 R6(f))

## Basis

- **Paper repo:** /mnt/d/vsps_papers/vsps-paperA-spic. HEAD was d0cb698 with a clean tree (`git status --porcelain` empty), so the line anchors of COMPANION_EDITS hold.
- **Source:** the s1m package committed at 26af89f (CC-289r2 GO 88):
  - S1M_DRAFT.md 9481b79c
  - S5_TABLE.md 247a1123
  - MAIN_SENTENCE.md 4346859c
  - COMPANION_EDITS.md 429f1b81
- **Status:** working tree only. Nothing is committed in either repo.

## Transfer rules applied (CC-289r2 R6(b))

- Only the text between the BEGIN and END markers is copied.
- Every INTERNAL HEADER, the FOR-THE-S1.M-READ block (Remark 4) and every HTML comment, src comments included, are stripped.
- No wording inside the blocks is changed.
- The only change is formatting: the S1.M headings are demoted one level (`##` → `###`, `###` → `####`) so that S1.M sits under the existing "## S1 Proofs and derivations".
- Remark 4 is not transferred (R2). E2, E3 and E4 are not transferred (R3; the S5 table carries only the narrow BOUND_ONLY list plus the E5 counts).

## Step by step, mapped to COMPANION_EDITS rows

| Row | File (paper/) | Edit made |
|---|---|---|
| 1 | sec5_exchangeability.md | After §5.3 (end of file), added "## 5.4 How much do five references leave unnamed?" and the 49-word sentence from MAIN_SENTENCE.md, its src comment stripped. The sentence ends "(Chao, 1987; Supplementary S1.M, S5)." |
| 2 | sec5_exchangeability.md | l.39 "Consequences for reporting": "…, not human ceilings." becomes "…, not human ceilings; for COCO-5000 and UIT-ViIC (development data) see Section 5.4." The rest of the sentence is unchanged. |
| 3 | supplementary.md | l.535, item 3: after "we report none." appended "For COCO-5000 and UIT-ViIC (development data) see Supplementary S1.M and S5." The withdrawn-values comment on that line is untouched. |
| 4 | supplementary_SPIC.md | l.425, item 3: the same append as row 3. |
| 5 | supplementary.md, supplementary_SPIC.md | S1.M (S1.M.1–S1.M.6, the paper-text block of S1M_DRAFT.md) inserted at the end of S1, just before the first "## S2" heading. No Remark 4. |
| 6 | supplementary.md, supplementary_SPIC.md | Table S5.M and its notes (the paper-text block of S5_TABLE.md, src comments stripped) inserted at the end of S5: before "<!-- end S5 -->" in supplementary.md, and before "## S6" in supplementary_SPIC.md. |
| 7 | sec11_limitations_ethics.md | §9.1: a new paragraph "**Construct validity: reference-only bound.** …" before "Construct validity: vocabulary and matchers". It carries the five-writer caveat, in the COMPANION row 7 wording. |
| 8 | sec2_related_work.md, paperA.bib | sec2, the "F-measures, thresholds and incomplete gold" paragraph: one sentence (R4) added after the species-accumulation sentence (quoted below). paperA.bib gains three entries (below). |
| 9 | supplementary_SPIC.md l.595, supplementary.md l.745 | After "No test of the estimator was registered." appended: "X1 extrapolates each run's mention precision, whereas Supplementary S1.M bounds the coverage of the reference gold itself, independent of any system." No X1 number is reused. |
| 10 | main text | Word recount (below). |
| 11 | sec5_exchangeability.md l.29 | Not an edit. It stays a note for the next A diff: "independent-annotator" for UIT-ViIC. |

## Row 8, the sec2 sentence (R4; verified content only, no priority claim)

> Treating repeated samples as sampling occasions, species-richness estimators bound from below the number of classes that no sample has recorded (Chao, 1987; Chao and Colwell, 2017), and estimators of this kind have been applied to human-produced lists, to estimate the size of a set enumerated by crowd workers (Trushkowsky et al., 2013) and class cardinality in a knowledge graph (Luggen et al., 2019); Section 5.4 applies the incidence form pooled over (image, class) pairs, with an image's references as its sampling occasions.

Sources for each clause:
- **The lower bound:** Chao 1987 is credited only for the bound, as Chao and Colwell 2017, §2.2, credit it (CC-289 check 8). That full text was read.
- **Trushkowsky et al. 2013:** set-size estimation from crowd answer lists. The content comes from the arXiv preprint 1202.2335, read in the in-house W3 prior-art note.
- **Luggen et al. 2019:** class-cardinality estimation in Wikidata, from the abstract read on 2026-11-07.

## Row 8, paperA.bib entries added (appended at the end, with provenance comments)

- **chao1987estimating:** Chao, A. (1987). Biometrics 43(4), 783–791, doi 10.2307/2531532. The record was verified at CC-289. It is closed access and was not read.
- **chao2017thirty:** Chao, A. and Colwell, R. K. (2017). "Thirty years of progeny from Chao's inequality: Estimating and comparing richness with incidence data and incomplete sampling", SORT 41(1), 3–54, doi 10.2436/20.8080.02.49. The entry was built by hand from the publisher PDF, because the DOI is not in Crossref.
- **luggen2019nonparametric:** Luggen, M., Difallah, D., Sarasua, C., Demartini, G. and Cudré-Mauroux, P. (2019). The Semantic Web – ISWC 2019, LNCS, pp. 453–469, doi 10.1007/978-3-030-30793-6_26. All five authors are listed.
- **Already present, unchanged:** Colwell et al. 2012 (colwell2012models), Chao et al. 2014 (chao2014rarefaction) and Trushkowsky et al. 2013 (trushkowsky2013crowdsourced).
- **A title that contains a banned word:** the Luggen et al. title contains "Completeness", and the Chao and Colwell title contains "incomplete". Both are the publishers' titles, quoted in the bib entries only. No added paper text uses those words.

## Row 10, the word count

- **Counter:** the V2_PROGRESS counter, i.e. HTML comments stripped, sec1–sec11 plus declarations.md, whitespace-split word count.

| File | Before (d0cb698) | After |
|---|---|---|
| sec2_related_work.md | 859 | 941 (934 + 7 for CC-291 W1) |
| sec5_exchangeability.md | 506 | 573 |
| sec11_limitations_ethics.md | 769 | 812 |
| Main text total | 11,107 | 11,299 (+192; CC-291 W1 adds 7) |

- **The 8,500-word cap (PI-1105k)** was already exceeded by this counter before the transfer: 11,107 > 8,500. The transfer adds 185 words. Reaching the cap is not part of this transfer, so this is flagged for the PI rewrite, which cuts to the cap.

## Checks at transfer (COMPANION_EDITS list)

- **Numbers:** every number in the transferred blocks is the s1m text verbatim, and those were checked against data/results/a_m1/a_m1_result.json (5687a66b) at CC-289r2.
- **Direction words:** Ĉ is called an upper bound on coverage; Ŝ and m̂ are called lower bounds. These are unchanged from the s1m blocks.
- **Banned words:** none in the added text. The grep over the added lines (`git diff`) hits only words that were already in the edited lines: "completeness estimators", "human ceilings", "incomplete gold", "first-order jackknife" and "SCAR … completely".
- **No AI mention, no data-overlap wording, no statement that the sets share images.**
- **Remark 4:** no text reached the paper repo.
- **NGRAM:** one scan per touched file; results are in the report.

## CC-291 W1 (coordinator, 2026-11-07T21:01:55Z)
- sec2_related_work.md: the clause "applies the incidence form to the references of each image" was replaced verbatim by the CC-291 W1 text ("pooled over (image, class) pairs, with an image's references as its sampling occasions"); +7 words; NGRAM PASS; sha a0e4bd43.
