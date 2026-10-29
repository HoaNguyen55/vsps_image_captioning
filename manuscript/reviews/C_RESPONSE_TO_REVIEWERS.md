# Paper C: Response to reviewers (revision 1, 2026-10-29)

Target: ACM TALLIP. Source: `manuscript/reviews/C_META_REVIEW.md` (R1-R5). Every judgement, score and readiness estimate in this file is **AI opinion**; none of it is evidence or changes a registered verdict.

No new experiment, GPU job, human label or test-set look was used. Every new number is arithmetic on values already in the decision files or ledgers, or a value copied from a published table, and each is a row of `number_manifest_C.tsv`. New rows use status `derived-post-hoc` (arithmetic on keyed raw values; the formula is in the key), `published-reported` or `prereg-quoted`. The n-gram scan (`ngram_scan_cen.py`) gave 0 hits on every edited file. Files were hash-checked against a snapshot before each write. No file changed underneath during this pass; the only hash change outside the checked write path was this pass's own regeneration of Figure 1. `tex/` was not rebuilt in revision 1; revision 2 rebuilt it (below).

## Summary for the coordinator

| # | Item | Status |
|---|---|---|
| 1 | Headline reframing | done |
| 2 | Table 21 not a ranking | done (now supplement Table S15, revision 2) |
| 3 | Related-work gaps | done; 3(d) Li et al. was already cited |
| 4 | Mechanism overclaim, contribution 3 | done |
| 5 | SESOI origin, power, scale | done |
| 6 | InternVL3 deletion confound | done |
| 7 | P2 scope | text done; registered `ret`-vs-`rand` precision test → X3 |
| 8 | Single `rand` draw | text done; multiple draws → X1 |
| 9 | Contamination | done (desk check of public reports) |
| 10 | Domain-coverage reading | text done; memory swap → X5 |
| 11 | Segmentation | done |
| 12 | Self-contained instruments | partially done |
| 13 | Length and operations log | mostly done in revision 2 (13,978 words, 33 + 26 pp); the ~25 pp target and the 13(e) `rand`−`zs` merge are not met |
| 14 | Minor bundle | partially done |

## Revision 2 (2026-10-29, PI-1029p (3) and (5))

Moves to the supplement, no new number and no verdict change. Main text (`00`–`10` md files, `wc -w`, abstract file and comments included) went from 17,715 to 13,978 words; the abstract body (194 words) is unchanged. The build gives 33 main pages and 26 supplement pages, with no undefined reference or citation.
- **Moved to the supplement:**
  - old Table 19 and its inclusion rule → Table S15 ("Context from published systems"); §8.6 keeps one paragraph and the one reading the table supports;
  - old Tables 12 and 14 (stage B, deletion decomposition) → Tables S16–S17; §6.7 keeps the H_G negative, the gate PASS (+6.04 [4.54, 7.58]) and the registered τ = −∞ secondary (now Table 9);
  - old Tables 9, 10, 11, 15 dropped as duplicates of S5, S7, S6, S14; their registered headline numbers stay in §6.4–6.6 and §6.8 prose (S-zf, `fix`, copy baselines, PTB, dose-response, style, neighbour-only precision, P-τ/P-K/P-M);
  - new supplement section "Disclosure detail": the §5.4 power and Monte Carlo paragraphs, the §7.1 split list, the §7.2 earlier-contact record, the §8.1 English memory counts, the §8.5 earlier-contact list, the §6.8 ablation disclosures, and the §2 literature-search note; the §3.3 pinned-revision table moved to "Instrument definitions".
- **Kept in the main text:** every registered verdict with its CI, including P1 PASS, P2 PASS ×2, XM-a FAIL, XM-b PASS / XM not confirmed, P1-EN PASS, S-NC FAIL and its 3,500 sensitivity, InternVL3's no-gain rows (P1b +0.66 [−0.68, 1.99]; COCO −1.64 [−2.79, −0.49]; τ = −∞ on all four sets), Box 2 and the deviation summary.
- **Renumbered:** old Tables 13, 16, 17, 18 are now Tables 9, 10, 11, 12; every in-text reference was checked against an existing caption or heading. §9.2 and §9.3 were condensed.
- **Build (CC-167 W3):** `tex/build.sh` now writes the inlined supplement to `paperC_supplement.tex`, so `paperC_supp.tex` keeps its `\input{supp_body.tex}` stub and edits of `11_supplement_registered_rows.md` reach the supplement PDF (checked with `pdftotext`). The supplement now has a bibliography, so `Rohrbach2018CHAIR` and the Table S15 citations resolve.
- **UIT-ViIC (PI-1029p (5)):** §7.2 and the §10 data statement say that UIT-ViIC is not a data set of this study, appears only as aggregate counts and image-id pointers, that no UIT-ViIC caption or per-image panel is shown or released, and that no permission from its authors is claimed. The UIT-OpenViIC and KTVIC "confirmed in writing" sentence is unchanged (PI-1026az).
- **Checks:** every CI that left the main text is in the supplement; no new number lacks a manifest row (`c_pass2_check.py`); the n-gram scan gave 0 hits on every edited file; files were hash-checked against a rolling snapshot, and no outside change was detected at the final check.

## Point by point

**1. Headline reframing (R1 M2/M7, R2 M2/m9, R3 m8/m9, R4 M7, R5 M2). Done.**
- (a) The abstract now opens its results with P1 OpenViIC, followed by P1-EN. It is 192 words, with no first person.
- (b) The abstract sentence that reports each pooled number also reports the per-backbone picture. InternVL3's COCO row is labelled reported. The intro contribution 2 marks it "a reported row, not registered".
- (c) §5.2 now says the pooled estimand averages two backbone-plus-configuration pairs and is not a "typical MLLM" effect. §9.1 repeats this.
- (d) §8.2 says that no English scope sentence was registered, so "carried by Qwen2.5-VL" is a descriptive reading.
- (e) The §9.1 limitation was extended.
- (f) A line is in the §7 "Deviation summary". Correction to the meta-review: the test PREREG (l.214) bars Vietnamese secondaries from the abstract; the Vietnamese per-backbone wording is the registered scope sentence, so it complies, and the English registration has no such rule. InternVL3's COCO row is therefore recorded as descriptive context, not as a rule breach. The registered rule text in §5.3 is unchanged.
- Every verdict word is unchanged.

**2. Table 21 is not a ranking (R1 M4/m2/m3, R2 M5, R3 M2, R4 M1-M3/m7/m8). Done.** This is now §8.6 and Table 19, renumbered because the old Tables 16-17 moved to S14.
- The ordinal paragraph was deleted. One sentence remains: a training-free prompt is far below fine-tuned systems on OpenViIC.
- The table is split into Block A (published) and Block B (this study). It has columns for memory/training data, images and scorer, and the caption says "No ordering is implied".
- Explicit inclusion rule:
  - English sets: every system discussed in §2.
  - XM3600-vi: every system in LMCap Tab. 6 and CONCAP Tab. 10, except CONCAP's own ablation variants.
  - OpenViIC: the best of the eight dataset-paper baselines.
- New rows, verified in the PDFs:
  - CONCAP Tab. 10: Pangea vi 64.3 and mBLIP vi 35.8.
  - LMCap Tab. 6: BB+CC vi 0.336 (shown as 33.6) and LG vi 0.182 (shown as 18.2).
- Memory/training-data and image cells not read in the sources say "see source" or "as in source" rather than guess.
- Labels and notes added:
  - Our Vietnamese rows are flagged **not comparable**.
  - LMCap's setting is relabelled.
  - Notes cover the MeaCap COCO vs CC3M memories, EVCap's Vicuna-13B and the re-fetched NoCaps images.
  - Block B states "no task training in this study; backbone training data not fully disclosed".
- No test set was re-scored.

**3. Related-work gaps (R1 M5/m1, R2 M1/m7, R3 M1/m6/m11, R4 M6/m1, R5 #4). Done.**
- (a) Flamingo and OpenFlamingo are now in §1, §2 and Table 1. RICES is credited to its source, Yang et al. (AAAI 2022), which is OpenFlamingo's reference [38]; Flamingo is cited as also using it. The cited values come from OpenFlamingo Appendix Table 9, read from the PDF:
  - COCO: +4.1 at 4 shots and +9.5 at 32 shots.
  - Flickr-30K: −20.3 at **0** shots and −13.6 at **4** shots.
  - Two discrepancies, corrected rather than copied: one reviewer gave the Flickr-30K shot counts as 4/32, and OpenFlamingo's own prose gives 20.4/13.1. We cite the table values.
- (b) P1-EN is now presented as a replication (§1, §2 "What is new" item 2). The Flickr-30K reversal is used in §8.2 for InternVL3's COCO sign.
- (c) VieCap4H and ViTextCaps (2604.27712) were added. The claim was narrowed to "general-domain".
  - ViTextCaps calls itself "first". That word is not repeated.
- (d) Re-ViLM was added. Li et al. 2507.08021 was **already cited** as `Li2025UnveilingICL` (TPAMI version), so no new entry was needed.
- (e) Verification of the citations the reviewers suggested:
  - The Gators paper (2605.20626) is real, but R4 described it wrongly. Its retrieval-augmented prompting sits in a Gemini 2.5 Flash translation stage, not in Qwen2.5-VL. §8.4 cites it as a different pipeline whose abstract-level finding (retrieval helped only with large in-domain corpora) agrees with our post-hoc question.
  - AfriCaption (2510.17405) was verified and added. It also calls itself "first", which is not repeated.
- (f) §2 now says that the searches were partial, with dates and sources. "No priority claim" is kept.
- Eleven bib keys were added, each with a row in `paperC_bib_audit.tsv` from our own fetch: arXiv abstract pages, plus Crossref for the VieCap4H and Yang et al. DOIs. No personal e-mail was sent; the Crossref calls carried only vsps-research@example.org. The Gators and AfriCaption statements were checked against the arXiv abstract text itself.

**4. Mechanism overclaim and contribution 3 (R2 M6, R3 M6, R4 M4). Done.**
- The §6.8 heading is now "A development-set diagnostic".
- The "explain" sentence was replaced with the meta-review wording: "about 2.95 of the shortfall (+5.36 → +2.41)" and "consistent with, but do not establish". The text notes that the registered condition held and that the permission is not used. §5.6 says the same.
- "What is new" item 3 is now a development-only diagnostic.

**5. SESOI origin, cross-scale use and power (R1 M1/m7, R2 M3/M4/m4, R3 M4/M5/m1a/m5, R4 m9). Done.**
- (a) §5.2 states the true origin. The value was a planning value from the design notes, fixed at stage 2 before any stage-B output, equal to the stage-1 value. The text says only what the stage-2 PREREG §7.1 records: not derived from the stage-A pilot or any stage-1 number, and no calibration recorded. The source note "QQ34 §2.1" was not found in the repo, so nothing beyond that is claimed. No post-hoc rationale is presented as the original reason.
- (b) The ratios are labelled post hoc. Correction: the meta-review's "about 6% / about 2%" is SESOI ÷ pooled `rand`, so both quantities are now given:

  | set | SESOI ÷ pooled `rand` | Δ ÷ pooled `rand` |
  |---|---|---|
  | OV-test | 6.2% | 13.9% |
  | XM-test2500 | 3.7% | 1.3% |
  | COCO | 2.3% | 3.5% |
  | NoCaps | 2.3% | 2.0% |

- (c) §8.1 and §5.4 say the English SESOI was carried over without recalibration and is more lenient on COCO.
- (d) The registered power note is quoted with its true scope. It applies to the **stage-B gate G1** (+4.0), not to P1: "SE ≈ 1.85, about 50% if Δ = +4". The text also states that no P1 power statement was registered. Achieved half-widths: 1.02 (P1), 1.21 (XM-a), 0.97 (P1-EN), 0.78 (S-NC).
- (e) The S-NC "would have passed under the XM-a rule; rule chosen after XM-a was known" sentence is in §8.3. The abstract carries the half-clause "CI above zero but point below +2.0".
- (f) XM-a's upper bound 1.97 is noted.
- (g) Monte Carlo error is a normal-approximation formula applied to existing CI widths, with no new bootstrap. It is about 0.06 bootstrap SE, at most 0.05 points, and XM-a's lower bound is about 12 such SEs from 0.
- (h) Figure 1 was regenerated on CPU from manifest values (`tex/fig1_forest.py`; SVG plus vector PDF). It now has separate Vietnamese and English panels, and the dashed line is labelled "registered threshold +2.0 (scale differs by panel)".

**6. InternVL3 deletion-step confound (R1 M3/m9, R2 M8, R3 m3, R4 m4). Done.**
- (a) Abstract clause added.
- (b) The τ = −∞ secondary is now in the §6.2 narrative, labelled secondary: OV +3.71 [2.29, 5.14], detected; COCO −1.05, not detected.
- (c) The §3.5 note says 0.351 of `ret` captions are zero-shot fallbacks, for which ΔP_cm = 0.
- (d) §6.6 notes that on OV-test τ = 0.10 vs −∞ did worse on all three measures (Table S1): CHAIR_i 0.254 vs 0.237, ΔP_cm 1.57 vs 5.80, and CIDEr-D.
- (e) §9.2 now calls this a design limitation of the estimand, with the stage-A ΔP_cm constraint as the reason τ = 0.10 was chosen.
- (f) The lineage line was already in §3.4.

**7. Scope of P2 (R2 m1, R3 m2, R5 #3). Text done.**
- The wording is now "relative to zero-shot, from the full in-context prompt" in §5.2, §6.2 and §10.
- The `ret`−`rand` row is labelled post hoc: +2.59 for Qwen2.5-VL and +0.17 for InternVL3. Correction: this is a difference of two vs-`zs` values with no CI, **not** a count-matched `ret`-vs-`rand` comparison, because k_cm differs between the runs. The text says so.
- A registered test is **not done** → X3.

**8. Single `rand` draw (R5 #1, R2 m2). Text done.**
- §5.2 states what the CIs condition on: one seeded `rand` assignment and the full-set document frequencies.
- §9.1 was narrowed to match, and adds "same machine and software stack".
- Multiple draws are **not done** → X1.

**9. Contamination and "training-free" (R3 M3, R4 M5). Done, as a desk check.** The new §9.1 bullet states only what was read:
- The Qwen2.5-VL report describes its data by category. Its OCR data include Vietnamese. A text search finds COCO only as RefCOCO evaluation.
- InternVL3 reuses the InternVL2.5 corpora, and the InternVL2.5 report (2412.05271) lists COCO-Caption, OpenImages-Caption and TextCaps.
- The bullet adds the shared- vs interaction-contamination point and defines "training-free" as no task training in this study.

**10. Post-hoc domain-coverage reading (R1 M2/m6, R2 m3, R3 m1b, R4 m2). Text done.**
- The §8.4 heading is now a question.
- Added: Qwen's positive out-of-source rows (XM +3.15 [1.50, 4.93]; NoCaps +2.83 [1.69, 3.98]), and the fact that the XM high-cosine tertile cuts against the reading.
- Practitioner item 3 now reads "consider".
- The "not interpreted further" contradiction in §6.5 was removed.
- The memory-swap test is **not done** → X5.

**11. Segmentation (R1 M6). Done.** §3.6 now says that CIDEr-D uses RDRSegmenter word tokens and that length is counted in syllables. "Syllable-segmented" was corrected at §8.1 and §9.2.

**12. Self-contained instruments (R1 m8, R2 M7, R4 m3, R5 m2). Partially done.**
- Added a supplement section, "Instrument definitions", covering the scoring kit and stripping, the tone-normalised matcher, the P_cm formula and gold (existing references only), the English matcher, and the verifier question with its 112-class map.
- Not done:
  - The full Vietnamese lexicon and class lists are not printed. They live in the companion kit, which is to be released with the code.
  - Sending anonymised companion manuscripts to the editor is a PI or coordinator action.

**13. Length and operations log (R1 M8, R2 m8/m12, R3 m7, R4 M8/m6, R5 m3). Partially done.**
- Done:
  - §7 now opens with a disclosure-summary table (Box 2) and a deviation summary.
  - Old §7.1-7.3, the §7.7 log timestamps, and the §8.5 commit, amendment, smoke-test and guard-count paragraphs moved to a new supplement section, "Test-run operations".
  - §6.8 was cut to the τ ablation plus one paragraph on k and memory. Tables 16-17 were dropped in favour of S14, and later tables were renumbered.
  - Internal terms were replaced ("sister study", "decoding machine", "laptop", "refusal/refused", "approved by the PI", "A also used").
  - A glossary (Box 1) was added at the start of §5.
  - All registered FAILs stay in the main text.
- Not done:
  - The `rand`−`zs` descriptives were not merged into one table.
  - The ~25-page target was not met. The main-text word count rose from about 16.2k to 17.7k words, because the requested additions (items 2, 3, 5, 9) outweigh the moves. A further cut needs a PI decision on what else moves to the supplement. AI opinion: the next candidate is §6.7 Tables 12-14, together with most of §7.2.

**14. Minor bundle. Partially done.**
- Done:
  - KTVIC 3,469 = 3,769 − 300 (§3.1; from the released train file).
  - Multiplicity and p-value sentences (§5.4).
  - AB-M is dev-only and no cross-language size claim is made (§1).
  - "Same machine and software stack" (§9.1).
  - Log timestamps archived in the supplement and marked unverifiable.
  - A qualified availability line (§10).
  - The abstract signals that the English arm is a frozen-configuration transfer.
  - The "all configurations tried" appendix is now cited as Tables S10–S11 (§5.1, §7.3).
  - Figure 1 is now vector.
- Not done:
  - Author placeholder, DOI and ORCID, and the acmart warnings. These are build or PI items, and `tex/` was not rebuilt.
  - The `Nguyen2026FAIR` bib entry stays NOT_CHECKABLE until it is on Crossref.

## Experiments handed to the coordinator (not done here)

Every item below needs its own three-tier registration: dev-explore, then a dev-confirm rehearsal, then a single look at a **fresh, never-looked** test set. None may re-score OpenViIC test, XM-test2500, COCO Karpathy test or NoCaps val. None may use new human gold, and AI labels are not evidence.

| ID | Experiment | Purpose |
|---|---|---|
| X1 | several independent `rand` draws, with their variance folded into the CI (dev sets only, unless a fresh test set exists) | R5's main correctness point |
| X2 | masked-n-gram analysis of the gain on OV-dev-B, descriptive | construct validity |
| X3 | registered `ret`-vs-`rand` count-matched precision test | P2 scope |
| X4 | 3-5 backbones across families and sizes; a deletion-free arm, or deletion as a factor | Q1 path; backbone as moderator |
| X5 | memory swap on fixed images | tests the §8.4 domain-coverage question |

## Readiness (AI opinion)

- **TALLIP:** After this revision the main correctness and clarity complaints are addressed in text. AI opinion: likely about Correctness 4, Clarity 3.5, Contribution 3, Novelty 2-2.5, which points to minor revision in round 2. The remaining length is the main clarity risk.
- **Q1 (Neurocomputing):** **Not ready** (AI opinion; agrees with all five reviewers). Text alone cannot fix the reasons:
  - The paper proposes no method.
  - The gain rests on one of two backbones.
  - Both out-of-source predictions failed.
  - The English COCO result is now framed, correctly, as a replication of OpenFlamingo's pattern.

  A Q1 path needs X4 and X5 (and preferably X1) under new three-tier registrations on fresh test sets. It would also need a method or a predictive account of when retrieval helps. TALLIP remains the better venue for the present evidence.

## Files changed

- `manuscript/journal_draft_C/`:
  - `00_abstract.md`, `01_introduction.md`, `02_related_work.md`, `03_method.md`, `04_data_and_splits.md`, `05_preregistration_and_analysis.md`, `06_results.md`, `07_disclosures.md`, `08_english_comparison.md`, `09_limitations.md`, `10_conclusion.md`, `11_supplement_registered_rows.md`
  - `paperC.bib`, `paperC_bib_audit.tsv`, `number_manifest_C.tsv` (30 rows appended; `used_in` updated on 30 rows)
  - `fig1_ret_minus_rand.svg`, `tex/fig1_forest.py`, `tex/fig1_ret_minus_rand.pdf`
- New: `manuscript/reviews/C_RESPONSE_TO_REVIEWERS.md`
- Pre-edit snapshot: `/tmp/claude-1000/-mnt-d-vsps-image-captioning/5a363495-c9d6-40f3-8f9c-a7285ef7a0e6/scratchpad/C_snap/`
