# Paper C, pass 3 (2026-10-28): the CC-145 fixes W7–W11

The PI approved this pass (PI-1026as): C stays at TALLIP at the tier it reaches, with no new experiment. No number was added. The checker of record lists no unsourced token that pass 2 did not already list; pass 3 removed 16 tokens (arXiv ids, DOI prefixes and decision ids). The n-gram scan reports 0 hits on every `.md` file, `tex/paperC.tex`, `tex/paperC_supp.tex` and `paperC.bib`, and its positive controls fired. Nothing was committed.

## W7. Build retired; checkers of record
- `journal_draft_C/` is the source of record. `scripts/paperC/build_c_draft.py` now starts with a comment, "RETIRED … DO NOT RUN". Its code is unchanged: the CC-145 rule 5 refusal, which would make it refuse to write, is still owed and goes through the gatekeeper.
- The checkers were copied unchanged from `.session_backup/2026-10-28/snapshots/C_pass2/` to `scripts/paperC/`. Their sha256 values:
  - `c_pass2_check.py`: a257bd14891403a1…;
  - `c_pass2_manifest.py`: 51ecd021df08e9c7…;
  - `c_pass2_supp.py`: 97953775669acb32….
- **Do not run `c_pass2_manifest.py` casually.** It rewrites the pass-2 rows of `number_manifest_C.tsv`.
- No SHA256SUMS file was written in `scripts/`, because this pass could edit only the one note there. The SUMS goes with the gatekeeper commit.

## W8. Internal ids removed from the visible text
- **Ids removed:** PI-1026b (07), C-EN (08, 11), CC-106, `exclusion.json` and "Paper A" (08), C-2 (11). The M1–M3 and K1–K3 part labels in the S14 outcome line were also reworded, to "all three parts true".
- **Companion submissions.** "Submission A/B" and "companion A/B" are now "the companion object-precision study" and "the companion scoring study", both by the same group and under review.
- **§8.5 item 5** now states the facts plainly: the companion study's evaluation sets include 130 Karpathy-val ids, and none of its outputs is reused or scored. PI-1026w bound the prereg wording, not the paper (CC-145 ruling 6a).
- **Scan.** The id scan (scratchpad `idscan_c.py`, with HTML comments stripped) finds 0 hits on 00–11 and on both `.tex` files. Ids remain only in HTML source comments, which is allowed.

## W9. EXTRA and the narrowed novelty claim
- **EXTRA (Ramos, Elliott & Martins, EACL 2023, doi 10.18653/v1/2023.eacl-main.266)** was read from the arXiv 2302.08268 PDF.
  - §5, "Encoding Irrelevant Captions": "Random Caption: encode the image with a random caption from the datastore."
  - Table 3, "The effect of training and evaluating with captions that are not expected to be useful", gives this variant below EXTRA.
  - So the random-datastore-caption control is **confirmed**. It differs from ours: it uses one random caption against k = 5 retrieved, and the model is trained with that input.
- **arXiv 2406.02265 is `Li2024RetrievalRobustness`** (ACL 2024), which was already cited. It also runs a random control at equal k on SmallCap, a trained model: "randomly retrieved captions are those retrieved with another image".
- **SmallCap (2209.15323)** has no random-caption ablation. It was already cited.
- **02 Related work** now cites EXTRA and states both controls. "What is new" is narrowed to three points:
  1. the Vietnamese training-free setting;
  2. the English comparison under one protocol;
  3. the backbone-dependence explanation, which is development-only and non-confirmatory.
  
  The random control, the count-matched rule and the preregistration are now stated as not new. The abstract and the contributions are unchanged, so no development-ablation row is in either.
- **No EXTRA or Li et al. numbers are in the paper text.**

## W10. Bibliography
- **`paperC.bib` has 31 entries:** Ken's K16 draft, the five pass-2 keys, EXTRA, and the FAIR entry copied from `paperB.bib` as Nguyen2026FAIR. Ken's empty Nguyen2026VSPSFAIR was dropped.
- **Ken's TODO venues were resolved by our own Crossref fetches:**
  - LMCap: Findings of ACL 2023;
  - Yang2023ICLConfig: NeurIPS 36;
  - Lu2025NES: AAAI 2026;
  - Li2025UnveilingICL: now TPAMI 2026.
- **`paperC_bib_audit.tsv`** records 36 identifier checks. The brief's file name is used; CC-145 calls it `C_bib_audit.tsv`.
  - 30 entries verified, by title and first author: 35 identifier checks OK. Three of them note that the arXiv v1 year differs from the cited venue year.
  - 1 entry not checkable: Nguyen2026FAIR, the authors' own paper, which is not on Crossref.
  - VELVET's author order was set to Vietnamese family-first. Crossref deposits family = Anh, so the PI should confirm.
  - Crossref was checked through `api.crossref.org/works/<doi>`. arXiv was checked through the citation meta on `arxiv.org/abs/<id>`, because `export.arxiv.org` returned HTTP 429.
- **Text keys** are now pandoc citations (`[@Key]`, and narrative `@Key` after "X et al."). They render through natbib in ACM author-year style. The inline "arXiv …/doi …" text was removed. Bui2026OpenViICJournal and Vu2018VnCoreNLP are now cited.
- **Cross-check:** every key in the text is in the bib and every bib entry is cited. There are 0 undefined citations.

## W11. TALLIP format
- **Source.** `tex/paperC.tex` is a self-contained acmart `[manuscript,screen]` source, the class the venue card names, with `\citestyle{acmauthoryear}`. The rights block is off (`\setcopyright{none}`). The ACM Reference Format block is printed, as the card's checklist asks, with the template's placeholder volume, issue and DOI, which ACM fills at production. It has CCS 2012 concepts and keywords, Figure 1 with `\Description`, and the bibliography. `tex/` holds a copy of `paperC.bib` so that it compiles on its own.
- **Build.** `tex/build.sh <journal_draft_C>` builds it with pandoc and lualatex. The build writes into its own directory, so copy `tex/` to a scratch folder first.
- **PDF.** `tex/paperC.pdf` has **32 pages** in `[manuscript]`. The same source compiled in `acmsmall`, the published format, has **31 pages**, with references from p. 29, so the paper is a Long paper (≥ 13 pp). The build had 0 missing glyphs, 0 overfull boxes and 0 undefined references.
- **Supplement.** `tex/paperC_supp.tex` builds to `tex/paperC_supp.pdf`, 27 pp. It still has 408 small overfull boxes from narrow table columns.
- **CCS.** The concepts are 10010147.10010178.10010179.10010182 (Natural language generation, 500) and 10010147.10010178.10010224.10010225 (Computer vision tasks, 300). The ACM CCS site returned 403, so the ids were taken from the CCS 2012 subject tree of an EPrints repository (pubs.cs.uct.ac.za/view/subjects/). Check them against dl.acm.org/ccs before submission.
- **Keywords:** image captioning, Vietnamese, in-context learning, retrieval augmentation, multimodal large language models, low-resource languages, preregistration.
- **Figure 1** (`fig1_ret_minus_rand.svg`, with a PDF copy in `tex/`) is a forest plot of `ret` − `rand` for each backbone and pooled, on OpenViIC test, XM-test2500, COCO and NoCaps.
  - It sits in §8.4 and uses values from Tables 6, 7 and 18 only. `tex/fig1_forest.py` asserts every value against the manifest.
  - Its caption states which rows are registered and which are reported, and that no cross-language difference is computed.

## Open after pass 3
1. **Author block.** It is still `[AUTHOR TO PROVIDE]`: authors, affiliations, ORCID. The FAIR bib entry also still lacks its pages and DOI. Both are PI-owned.
2. **Statistics format.** There are no p-values, because TALLIP's p-value expectation needs a CP judge round first.
3. **Public DOI for the code.** This is the artifacts cell (CC-145 W6) and is PI-reserved.
4. **CCS ids** need checking against ACM's own CCS page.
5. **Build refusal.** `build_c_draft.py` still needs the refusal in code, plus the SUMS for `scripts/paperC/c_pass2_*.py`, through the gatekeeper.
6. **Supplement layout.** The wide tables need landscape pages or split tables. The text is complete, but there are 408 small overfull boxes.
7. **Bibliography warnings.** BibTeX warns about a missing address on 17 proceedings entries, and missing pages on Nguyen2018VnCoreNLP, Nguyen2026FAIR and Vu2025VELVET (no pages in the Crossref records).
8. **The 3-judge re-score** replaces the CC-145 interim scores.
9. **Two points carried over from Ken's K16 draft:**
   - Kuznetsova2020OpenImages is the V4 paper, while the text uses the V7 human-verified labels. A V7 release URL could be added.
   - Crossref's author order for Vu2026ViG looks inconsistent with Vietnamese order. It was kept as Crossref deposits it; the PI should confirm.
10. **Anonymity.** The anonymity setting is NOT FOUND on the venue card. If review is double-anonymous, add `anonymous,review` to the class options. The FAIR self-citation is already in the third person.

---

# Paper C, v2 pass 2 (2026-10-28): changes by scorecard criterion, and open items

Baseline: CC-126 scored C at 2/3/4/3/2/2 = 16/30. The criteria are novelty, application, evidence, venue fit, artifacts and writing. Q2 needs ≥ 20 with every criterion ≥ 2, novelty ≥ 3 and writing ≥ 3 (UPGRADE_PLAN §7). The scores below are not self-assigned; the next judge-panel scoring decides them. The sources for this pass were:
- C-EN: `decide_coco_test.json`, `decide_nocaps_val.json`, the C-EN logs and `CHAIN.log`;
- C-2: `decide.json`, the parity files and `job.log`;
- the two preregs.

No preds or caption file was opened.

## Changes by criterion

### Novelty (2 → target 3)
- `02_related_work.md` has a new paragraph, "What is new, stated against the closest work". It states the prior-art distance item by item:
  - the equal-k random control from the same memory, against similarity-vs-random studies with images in context;
  - the Vietnamese–English pair under one frozen design;
  - object precision as a registered non-inferiority prediction;
  - one-look registration with the failures kept;
  - the per-backbone split.
  
  The paper still makes no priority claim.
- FAIR 2026 is cited in the third person ([Nguyen2026FAIR]) and contrasted with C: it fine-tunes, while C changes only the prompt.
- English benchmark context has been added: COCO Karpathy, PTB CIDEr-D and the NoCaps domain labels.

### Application (3 → target 4)
- **Introduction.** A new paragraph states the deployment setting: no training run, an existing captioned set as memory, one 24 GB GPU. It also states the practical cost of mis-attributing a style gain to retrieval.
- **Conclusion.** A new paragraph, "What a practitioner can take from this", names three conditions: an equal-k random control, per-backbone results, and an in-domain memory. It adds the deletion-step caution, labelled as dev.
- **Evidence for the application claim.** The registered in-domain PASS now holds in two languages (P1, P1-EN). Out of the memory's source it fails in both (XM-a, S-NC), and this is reported plainly.
- **Abstract.** It states "The focus is practical", as TALLIP requires.

### Evidence (4, kept and broadened)
- **New §8 (`08_english_comparison.md`)** replaces the placeholder. It contains:
  - the registration (what was carried over, the scorer, Table 17 rules, references, memory counts);
  - COCO P1-EN PASS +3.08 [2.08, 4.03], with per-backbone rows (Qwen +7.80; InternVL3 −1.64 [−2.79, −0.49], a CI below zero, stated as such), the τ = −∞ secondary (not detected), rule L and the `zs` rows;
  - NoCaps S-NC FAIL +1.73 [0.94, 2.50] (CI above 0, point below the SESOI), with the transfer claim not made, the 3,500 sensitivity FAIL, the per-backbone rows, and Table 19 by domain (in +4.64, near +1.96, out +0.43, with n and CIs);
  - §8.4, a labelled post-hoc reading ("retrieval helps when the memory covers the domain") with its two limits: overlapping CIs, and the cosine tertiles not being monotone;
  - §8.5, the disclosures listed under "Threats to validity" below.
  
  There is no cross-language difference anywhere (PREREG §8, §0.3).
- **Rule-timing disclosure** (C-EN PREREG §7). Judging NoCaps by the P1 rule was fixed after the XM-a result was known, and that rule is stricter than XM-a's lower-bound-only rule. This is disclosed in §8.1, §8.5 and §9.2. The two out-of-source results are therefore not written as one parallel failure. XM-a: not detected. S-NC: CI above zero, point below the SESOI. This wording is used in the abstract, the contributions, §8.4, §9.1 and §10.
- **The abstract is stable under leaving out one system.** The abstract now gives InternVL3's COCO row, which is below zero (−1.64 [−2.79, −0.49]), next to the P1-EN PASS.
- **New §6.8**, the mechanism on the development set (C-2). It is boxed as "Development data only … non-confirmatory" and covers AB-τ, AB-K and AB-M (Tables 14–16), all HOLDS.
  - It explains the backbone dependence on OV-dev-B, under the registered §2.4 condition (`section6_explains_backbone_dependence` = true). The measured part is the deletion step. InternVL3's AB-K rows and copy shares are scored at τ = 0.10, after deletion (`c2.py ab_k`). They therefore cannot separate uptake from deletion, and the text says that this question is not settled.
  - It states that the account does not carry beyond in-domain Vietnamese: InternVL3's τ = −∞ row is not detected on XM, COCO or NoCaps.
  - It gives InternVL3's non-monotone AB-M points.
  - It carries the P-K label "shaped by stage-A dev299 selection" and the W8a disclosure (the −∞ and 0.10 points were known).
  - rand − zs appears only as a labelled post-hoc remark.
  - The old §6.8 Compute is now §6.9.
- **Supplement.** Table S13 gives every C-EN row, including the per-run guard counts, shown once. Table S14 gives every C-2 decide row, dated (C-2 PREREG §9).
- **§5.6** briefly records the two later registrations and the pre-fixed §6.8 condition.

### Threats to validity and reproducibility (part of evidence, venue fit and artifacts)
- **`09_limitations.md`** is now "Limitations and threats to validity":
  - §9.1 updates the limitations for the English arm and the dev mechanism;
  - §9.2 is new and covers internal, construct, external and statistical-conclusion validity, plus researcher degrees of freedom;
  - §9.3 is new, on reproducibility. It covers the pins, the decision-file hashes, what is released (scores, ids and sha256 only; per-image ledgers are not released, per C test PREREG §0.1 and C-EN PREREG §0.4), the re-run cost of 9.59 and 13.22 GPU-h, and the per-image rates of 0.69 s and 1.24 s. §10 and the contributions no longer list the per-image ledgers as released; the old §10 did.
- **§8.5 disclosures**, from the C-EN PREREG §12 and §13 and the logs:
  - the registration timing;
  - the M3 HEAD move ed1e6c41 → f8cccb68, with an empty C-EN diff;
  - Amendment 1;
  - the smoke test (96 captions, 0 empty);
  - the English guard port and its untested calibration;
  - the per-run guard counts;
  - the Open Images byte source;
  - earlier contact (A's 9 systems and 2,441 references, the 295-image zs, the vg-mamf 1,000, the 163/133 exposure, the PI-1026w Karpathy-val sentence verbatim, the 2,402 pool);
  - compute: 6.33 + 6.88 = 13.22 of 25 GPU-h.
- **`07_disclosures.md`:**
  - §7.6 now points to Table S12 and states that the C-2 registration covers the dev τ rows only;
  - §7.7 moves to the past tense, and the PI-1026l "may be submitted without" sentence is removed because the arm is complete.

### Venue fit (3 → target 4) and writing (2 → target 3)
- **Title.** "Retrieved or Random Examples? Preregistered In-Context Captioning in Vietnamese and English" has 11 words (it was 14; the limit is ≤ 12, per TALLIP and CC-126 W4).
- **Abstract.** It was rewritten to 199 words (it was about 250; the limit is 150–200). It has no first person, no "This paper", no citations and no planned work, and states that the focus is practical. It contains only P1 with its scope, P2, P1-EN, XM-a and S-NC. It has no C-2 row (CC-126 W12).
- **Contributions.** They were rewritten for the two languages, and no C-2 row is among them. The roadmap covers §§6–10.
- **Placeholders.** The §8 placeholder was removed (TALLIP checklist: "No placeholder sections"), and the `[CITE …]` comment in 02 was replaced.
- **Numbers.** Every new number is in `number_manifest_C.tsv`: 471 rows tagged `c-pass2`, each with its source path, key, raw value, the source's sha256 prefix and a status. The statuses are `c-en-registered`, `c-en-reported`, `c2-dev-nonconfirmatory`, `prereg-quoted`, `log` and `verdict`. A scratchpad checker found no unsourced numeric token in the edited files; the only tokens it left are section and table numbers, years, DOIs, arXiv ids, timestamps, hashes and a software version.
- **Caption scan.** The 6/8-gram scan (`ngram_scan_cen.py`) over every `.md` file in this folder found 0 hits on all four corpora, and the positive controls fired.

## Word counts (after this pass, `wc -w`)
- Abstract body: 198 (TALLIP 150–200). Title: 11 words.
- Main text, files 00–10: 14,527 words, including tables. That is about 19 or more `acmsmall` pages at the venue card's rate, so a Long paper (≥ 13 pp), which has no upper limit on record.
- Per file: 00 249, 01 896, 02 879, 03 1,354, 04 547, 05 1,356, 06 3,834, 07 1,552, 08 2,404, 09 1,061, 10 395; supplement 10,819.

## Numbers not sourced or not used
- **LOG GPU totals.** The LOG gives "test 13.21 of 25" and "C-EN total 13.86" (CEN-NOCAPS row). These do not reproduce from `gpu_seconds.tsv`, which gives a test total of 47,576 s = 13.22 GPU-h and a total of 49,960 s = 13.88 GPU-h. The text uses the tsv value, 13.22, and does not use the LOG values.
- **LOG wording.** The LOG phrase "Pattern replicates the Vietnamese OV result (Qwen gain, InternVL3 none)" is not accurate for InternVL3. On COCO, its row is −1.64 [−2.79, −0.49], a CI below zero. The text says so and does not use the phrase.
- Every other number in the brief matched its verdict file.

## Open items
1. **The build pipeline is stale.** The draft is a build output of `scripts/paperC/build_c_draft.py` from `scripts/paperC/src/*.md`. This pass edited `journal_draft_C/` directly, because `scripts/` is off limits. **Running the build now would overwrite this pass and its manifest rows.** Before any rebuild, someone allowed to edit `scripts/` must port the pass-2 text into `src/` and add the C-EN and C-2 decide files as JSON aliases. The `used_in` column of the build's own rows is also stale: it still names `08_english_arm_placeholder.md`, and it predates the abstract and intro rewrites.
2. **No `paperC.bib`.** Citation keys are placeholders and must be converted to TALLIP's author-year form. New keys in this pass: Nguyen2026FAIR (the entry exists in `journal_draft_B/paperB.bib`; its pages and DOI are still to be provided), Lin2014COCO, Karpathy2015Split, Agrawal2019NoCaps and Chen2015COCOCaptions.
3. **Internal identifiers in the anonymous manuscript.** The PI-1026w Karpathy-val sentence is used verbatim in §8.5 item 5 and names "Paper A", "C-EN", `exclusion.json` and CC-106. Decision ids such as PI-1026b also appear in §7.7. The PI or a judge must rule whether the verbatim rule binds the paper text, or only the prereg.
4. **The judge panel and the gatekeeper.** This pass needs a CP judge round and a rescore. The rescore was due after NoCaps (UPGRADE_PLAN §7), and the scorecard should be re-scored with a CC id. The commit goes through the gatekeeper; nothing was committed in this pass.
5. **Artifacts (2) cannot be raised by text.** That needs a public release with a DOI and an external run. The status of the OpenViIC/KTVIC written confirmation (CC-126 W17) is not stated in C, because I could not find it; once known, add "obtained / not obtained".
6. **TALLIP format items still open:**
   - CCS 2012 concepts and keywords;
   - the `acmart` `[manuscript]` source;
   - figures (none yet; candidates are the NoCaps domain rows and the AB-τ curve, at ≥ 600 dpi with `\Description`);
   - ORCID;
   - the anonymity setting.
7. **Statistics format.** TALLIP asks for test statistics with p-values. C is CI-based. Any p-value would be POST HOC and needs a CP judge round first (the venue card's project note).
8. **Length.** The main text is about 14.5k words. Moving Tables 14–16 or the detail of §8.5 to the supplement is an option if the editor asks.
9. **Mirror artifact.** `.session_backup/machines/M4/root/outputs/c2_ablation/RUNNING` (pid 11886) is present in the mirror, although the operator log says M4 was cleaned with no lock. It is probably a copy taken at job start. Check it before any further M4 job reads `/root/outputs/*/RUNNING` from the mirror.
10. **Abstract margin.** At 198 words the abstract is at the limit; check it with the venue's counter once the source is compiled.
11. **Releasing the per-image ledgers.** The registrations forbid committing them. To let third parties recompute the CIs, they need a ruling: either a captions-free ledger export, or keep them unreleased.
12. **Snapshot.** The final files are snapshotted with `SNAP.sha256` in `.session_backup/2026-10-28/snapshots/C_pass2/`. Because another tool also writes to this repo (INC-1027a), sha-check those files before review.
