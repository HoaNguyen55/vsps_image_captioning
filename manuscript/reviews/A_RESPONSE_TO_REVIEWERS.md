# Paper A: response to the reviewers (revision 1, 2026-10-29)

Point-by-point reply to `A_META_REVIEW.md` (items 1–15). Every judgement here is AI opinion (the writer agent), not a human decision. No commits, no GPU work, no new labels and no second look at any test set were made. Paths are relative to `manuscript/journal_draft/` unless stated.

**Write safety.** Before editing, the sha256 of every draft file was snapshotted (scratchpad `A_rev/sha_before.txt`, with copies in `A_rev/orig/`). Each write re-checked the file's hash against the last recorded value and aborted on a mismatch. No mismatch occurred.

**Checks run.**
- `ngram_scan_cen.py` on every edited file and on this file: PASS, 0 hits.
- `build_A_cas.sh` into scratch: rc 0, the PDF builds, and every new citation resolves.
- Abstract: 237 words.
- Highlights: each 78–84 characters.

**Status counts:** 12 items done, 3 partially done (items 3, 11, 12), none not done. Two FLAG items (5b, 9b): 9b was answered from a stored file; 5b goes to the coordinator.

## Tier 1

**1. Limitations contradicted the PASCAL-50S result. Done.**
- `sec11` §10.1, Scope: the stale "registered, not run" text is replaced by the run-once statement with the failed label-gold step, −2.29 [−5.15, +0.61].
- Statistical-conclusion paragraph: adds "and failed its label-gold step on PASCAL-50S", plus the fixed-runs and deleted-files limits.
- Exposure: adds PASCAL-50S (public since 2008–2015) and the 8-gram counts.
- External validity: adds the seven-LVLM English family.

**2. Conflicting permission statements. Done; coordinator corrected to "confirmed in writing" per PI-1026az (LOG.md, 2026-10-28).**
- `declarations.md`: "the UIT-OpenViIC and KTVIC authors confirmed this use in writing" now reads "written permission was requested … at submission no reply had been received". This matches the file's own comment and PD-2 Q4.
- PASCAL-50S "confirmation obtained 2026-10-28" is kept, because it is recorded in the committed registration (PREREG `2026-10-28_pascal50s` l.109, commit 353437f). The PI should confirm that the written document is on file.
- The cover letter does not mention the permissions.

**3. Visible placeholders. Partially done.**
- Polaris (BSD) and DOCCI-Critique (CC BY 4.0) were verified from the licence tags of their Hugging Face releases (no e-mail sent), and the `[AUTHOR TO CONFIRM]` placeholder is removed.
- Still open, and PI admin items (low priority, but they block submission): the postal addresses in `title_page_A.md` and `cover_letter_A.md`, and the private reviewer link in `declarations.md`, `title_page_A.md` and `cover_letter_A.md`.

## Tier 2

**4. State the PASCAL primary FAIL and scope the claim. Done.**
- Abstract: the FAIL and its number come before the secondary PASSes. "Nine registered predictions failed" is stated. The text adds "conditional on the systems scored" and "every registered level". The PASCAL item is dropped from the later failure list.
- Contribution 1 names P50-A4 as the failed primary in the same sentence as P50-O2.
- Ledger row A24 carries both parts with their numbers, and A24a/A24b are labelled secondary/companion.
- Highlight 1 is scoped to XM3600 with two backbones, "not PASCAL-50S labels".
- The cover letter gives the same balance as the abstract.
- The PASS headline is kept.

**5. Separate the expected part from the risky part.**
- (a) Done: §1 and §9.1 now say that the reference levels are ordered even under SCAR, and give the tally for the non-nested label-gold step: XM3600 PASS under verified precision; second backbone PASS, with the lower bracket at +1.97 [−0.44, +4.01]; PASCAL-50S FAIL.
- (b) Done: §7.4 and §10.1 add that the premise "VOC labels are more complete than 50 references" was assumed, not measured. The V20 50-reference slope (+9.74 [+7.29, +12.12]) is above the VOC-label slope (+7.45 [+4.98, +9.94]). The LLaVA-1.5-7B and LLaVA-OneVision-7B per-model slopes are negative.
- (c) Done (PI default applied; PI may revert): the title is now "Gold Completeness and the Verbosity Slope of Object Hallucination Metrics: A Registered Audit" in the abstract, the title page and the cover letter. The choice is recorded in `outline.md`.
- **(5b) FLAG, coordinator.** Output-free gold sizes per level on V20 were not computed: that would need the PASCAL-50S references re-staged, which the data rule may forbid. The text says "was not tested", and the §10.1 comment marks the values "not retained".

**6. System dependence and auditability of PASCAL-50S. Done.**
- New "System dependence" paragraph in §7.4:
  - the 14 runs are held fixed;
  - V20 M forms two clusters, short 1.12–1.35 and detailed 1.61–2.24, so the slope is a short-versus-detailed contrast;
  - the per-model VOC-label slope ranges from −1.05 to +14.75;
  - the cap hit was "not recorded";
  - no system-level interval can be computed, because the caption files were deleted;
  - the deposit contents are listed.
- The PAIR_m table note in the supplement says each entry is a two-run contrast and that the vocabularies differ between columns.
- No leave-one-out run or matcher fix was requested or done.

**7. Undisclosed departures from the registration. Done.**
- (a) The missing hash is labelled a departure from PREREG §6, in §7.4, §10.1, the declarations and S7.
- (b) The laptop refcheck of the pascal50S.json structure is disclosed in §7.4, §10.1 and S7.
- (c) The per-file 8-gram counts (18–419) are given as aggregates in the new Table S7.P2, with a "generic phrase or memorised text; not a verdict input" sentence in §7.4 and §10.1.

**8. Tidy X4 and X5. Done.**
- X4 is labelled "co-primary in its registered companion family {X4, X5}; secondary to the paper's confirmatory claim" in §7.6, §9.1 and Table S4.0.
- "997-image analysis set (of 1,000)".
- "p ≤ 0.001" is stated as the floor, with the gold-randomisation reading.
- "Holm, X4 alone" is replaced by "one evaluable member; no adjustment", and the family-wise reading (0.939 / 0.001 / 0.001) is added in the main text.
- The anticipated direction is stated: 8/8 exploratory cells, and 4/4 cells of a post hoc check on spent development sets (RULE l.78, l.120; manifest rows keyed_text).
- The X4 link to the b-channel is added.
- X5: the rationale is deleted, the condition is stated as 1,782 < 2,079.2 image–class pairs, and its observed value is not reported.
- The timestamp now reads "before the run started (00:51:22Z)".
- §3.6 names the Holm families.

**9. Dependence on the verified-precision estimand.**
- (a) Done: the justification is added in §3.1 and §10.1.
- (b) Already present: the abstract and the §9.5 conclusion give the lower bracket +1.97 [−0.44, +4.01].
- **(9b) Answered without a new pass.** `data/results/n_f1/bracket_result.json` already stores `verifiable_share` per system (manifest-keyed). §10.1 now reports that OIV7 can verify 43.4%–69.7% of the mapped mentions, and Table S7.3 already lists them. No coordinator ruling is needed.

**10. Theory vs the primary outcome (micro- vs mixed-F1). Done.**
- §4.2 states that Proposition 1 is a micro-F1 result that motivates, but does not derive, the mixed-F1 ordering.
- Tables 7.1–7.3, Fig. 2, Fig. 3 and Table S7.P1 now name their F1 variant.
- A real discrepancy was found and resolved: on XM3600 images the registered label-gold F1 pairs verified precision with micro recall (G2-B prereg md:130, md:164), not mixed F1. The Table 7.1 caption and the supplement now say so, replacing "both variants".

## Tier 3

**11. Missing prior art. Partially done.**
- Added after reading, to `paperA.bib`, §2 text, Table 2.1 and the positioning sentence:
  - Feng et al. 2024 (arXiv 2406.12663; abstract read);
  - Misra et al. 2016 (Crossref plus the arXiv abstract).
- Added at title level only, from the Crossref records (full text not read):
  - Spain & Perona (IJCV 91(1), 2011 issue, online 2010);
  - Berg et al. 2012.
  - These are used in §2 and §4.1.
- Already present: Rohrbach et al. 2018 (§7.6).
- Not cited:
  - Amirloo et al. 2024: its abstract does not state the CHAIR–recall trade-off.
  - Chen et al. 2026: it exists, but it concerns language bias.
  - Vedantam et al. 2015's more-references finding: body not read.
- "None matches" is scoped to "the works cited here", and the searched scope is stated as partial. No "first" claims.
- Coordinator: the new mentions have no rows in `manuscript/review/citation_audit/intext_trace.tsv`. The build resolves them by author and year.

## Tier 4

**12. Restructure for an SPIC reader. Partially done.**
- (a) Done: Table 1 is now a five-row summary (confirmatory / other registered PASS / FAIL (9) / other / post hoc). The 40-row ledger moved verbatim to Supplementary Table S4.0.
- (b) Done in the main text:
  - cv295, uv231 and xm600 are now COCO-295, UIT-ViIC-231 and XM3600-600;
  - "rung" is now "level", and "family ALL" is now "all 14 runs";
  - the raw evaluator token is now a verdict phrase, with the verbatim token kept in a comment;
  - no CC-, PI- or W- identifiers remain in visible text;
  - inside the frozen registration texts of S4, the original codes are kept verbatim, and a one-line code map opens S4.
- (c) Already the case: `supplementary_SPIC.md` is the one submitted supplement, generated from `supplementary.md` by `manuscript/build/scrub_supp.py`. It was regenerated after these edits (rc 0).
- (d) Done as a map: the stubs are comment-only, so they render nothing, and `appB` is not built. A file-to-section map was added to `outline.md`. The build scripts are unchanged.
- (e) Done: "verbosity slope" is defined once (§3.6, signed) and used throughout. The "verbosity reward" wording is replaced.
- (f) Partially done (PI default applied; PI may revert):
  - The §6.2 discussion paragraphs and §6.3 moved verbatim to S3, with short summaries left in place.
  - §8.3 moved verbatim to S8, with a summary left in place.
  - Table 6.1, §6.4–6.5 and §8.4 stay in the main text, because they carry registered verdicts (A20–A23) and the reproducibility statement. Every section cross-reference still resolves.
- (g) Done: an Introduction paragraph on reference-set dependence of quality measures (González-Chávez et al., 2024) was added.
- Net effect: visible main-text words went from 12,571 to 13,389 (+818), because the Tier 1–2 disclosures outweigh the moves. AI opinion: further cuts in §7.1–7.3 are the next clarity lever.

**13. Figures. Done.**
- New Fig. 3 (PASCAL-50S, k = 1→50 on COCO-80 and V20, plus the VOC-label point, with the failed comparison marked). It is drawn by `scripts/figures/paperA_figs.py` from manifest rows only and is referenced in §7.4.
- New Fig. 1: the gold-level schematic (no data), referenced in §3.1.
- Stale cross-references fixed: Fig. 2 (7.6→7.3, 7.5→7.2) and Fig. 4 (§4.3→S1).
- The SVGs and PDFs were re-rendered, and `VALUES.json` was updated.

## Tier 5

**14. Minor consistency. Done.**
- PASCAL-50S exception in §3.1.
- B = 1,000 for PASCAL-50S in §3.6 and §7.4.
- "Every registered level (k = 1, 2, 5, 10, 20, 50)".
- The part-2 interval includes 0, so the FAIL means "direction not shown".
- The unpredicted crossing location in §4.2.
- "50-reference consensus".
- UIUC captions: unknown whether they are among the 50; no adjacency check was registered.
- Expected false PASSes ≈ 0.5: 19 ledger rows with PASS/FAIL × 0.025, stated as a rough guide; manifest row DERIVED.
- Title consistent across all four files.

**15. Reproducibility statement. Done.**
- The declarations list what a reviewer can check (code, decide files with hashes, registration commit times, manifest) and what cannot be checked (PASCAL per-image outputs, rows not releasable).
- Deposit contents are unchanged (a coordinator/PI decision).

## Traceability

- 26 rows were appended to `number_manifest.tsv`:
  - 14 keyed 8-gram counts;
  - 4 keyed V20 M values;
  - n_boot;
  - DERIVED rows: 2,079.2, the count 19, ≈0.5, and 43.4% / 69.7%;
  - 2 keyed_text rows: the 8/8 and 4/4 counts, from the companion RULE.
- Every other new number in the text already had a manifest row (P50-NS, PAIR_m, family-wise p, bracket).
- No manifest checker script exists in the repo. The new keyed rows were read directly from their files, and the figure script resolved all 101 lookups it uses.
- X5's observed slope appears nowhere.
- No caption text from OpenViIC, KTVIC or UIT-ViIC was added.

## For the coordinator / PI

1. PI: true status of the UIT-OpenViIC and KTVIC permission (default text now says "requested, no reply"), and confirmation that the PASCAL-50S written confirmation is on file.
2. PI: keep the new title, and keep the partial move of §6/§8.3 (both reversible from `A_rev/orig/`).
3. Coordinator, FLAG 5b: V20 gold sizes per level. This needs the references re-staged; check whether the data rule allows it. It would be post hoc, with no verdict.
4. Coordinator:
   - any change to the deposit contents (item 15);
   - rows for the four new citations in `intext_trace.tsv`;
   - recount the "29 of 804 rows" in `declarations.md` and `anon/declarations_anon.md`, now that the manifest has grown.
   - `anon/declarations_anon.md` holds no permission claim and was not edited; it lacks the new reproducibility sentence.
5. PI admin, low priority: addresses and the reviewer link (item 3).
