# Paper A: response to the reviewers (revision 1, 2026-10-29)

Point-by-point reply to `A_META_REVIEW.md` (items 1–15). Every judgement here is AI opinion (the writer agent), not a human decision. No commits, no GPU work, no new labels and no second look at any test set were made. Paths are relative to `manuscript/journal_draft/` unless stated.

**Write safety.** Before editing, the sha256 of every draft file was snapshotted (scratchpad `A_rev/sha_before.txt`, with copies in `A_rev/orig/`). Each write re-checked the file's hash against the last recorded value and aborted on a mismatch. No mismatch occurred.

**Checks run.**
- `ngram_scan_cen.py` on every edited file and on this file: PASS, 0 hits.
- `build_A_cas.sh` into scratch: rc 0, the PDF builds, and every new citation resolves.
- Abstract: 237 words.
- Highlights: each 78–84 characters.

**PI decisions applied (PI-1029p, 2026-10-29: "Đồng ý các đề xuất mặc định, tiếp tục đi").** A second writer pass applied the PI's defaults for items 5c, 12f and 2. Write safety as above: hashes snapshotted in scratchpad `a1029p/sha_before.txt`, re-checked before every write, no mismatch. Pre-revision copies of the moved sections are in `.session_backup/2026-10-29/paperA_rev1_PI1029p/`.
- **5c (title): approved.** The title "Gold Completeness and the Verbosity Slope of Object Hallucination Metrics: A Registered Audit" stands in `abstract_A.md`, `title_page_A.md`, `cover_letter_A.md` and `outline.md` (decision recorded), and is now also printed under the heading of both supplements. `highlights_A.md` and `anon/declarations_anon.md` carry no title.
- **12f (move): done in full.** See item 12(f) below.
- **2 (permissions):** UIT-OpenViIC, KTVIC and PASCAL-50S stay "confirmed in writing" (PI-1026az). **UIT-ViIC: the authors have not given permission.** `declarations.md` (Data availability), `anon/declarations_anon.md`, §9.2 and Supplementary S6 now say that UIT-ViIC is used only through aggregates and pointers, that no per-image UIT-ViIC panel is released, and that no written permission was received. The staged deposit (`.session_backup/2026-10-21/zenodo_build`) was checked. Every JSON file was walked recursively, and none holds a per-image UIT-ViIC score array. The only per-image UIT-ViIC content is a list of 133 COCO image identifiers, which counts as a pointer. The deposit README records an 8-gram scan with no dataset text. Supplementary S6 said "We have not obtained written confirmation" for UIT-OpenViIC, which contradicted PI-1026az. It now says the UIT-OpenViIC authors confirmed this use in writing, as does §9.2.
- **Main-text words** (sec1–sec11, HTML comments removed, scratchpad `wc.py`): 13,403 before, 12,488 after (−915). Including `declarations.md`: 13,962 before, 13,080 after.

**Status counts:** 12 items done, 3 partially done (items 3, 11, 12), none not done. Two FLAG items (5b, 9b): 9b was answered from a stored file; 5b goes to the coordinator.

## Tier 1

**1. Limitations contradicted the PASCAL-50S result. Done.**
- `sec11` §10.1, Scope: the stale "registered, not run" text is replaced by the run-once statement with the failed label-gold step, −2.29 [−5.15, +0.61].
- Statistical-conclusion paragraph: adds "and failed its label-gold step on PASCAL-50S", plus the fixed-runs and deleted-files limits.
- Exposure: adds PASCAL-50S (public since 2008–2015) and the 8-gram counts.
- External validity: adds the seven-LVLM English family.

**2. Conflicting permission statements. Done; coordinator corrected to "confirmed in writing" per PI-1026az (LOG.md, 2026-10-28).**
- `declarations.md`: the first pass had changed the text to "written permission was requested … no reply had been received". The coordinator then restored "the UIT-OpenViIC and KTVIC authors confirmed this use in writing", following PI-1026az, and PI-1029p confirms that restoration.
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
- (c) Done and approved by the PI (PI-1029p): the title is now "Gold Completeness and the Verbosity Slope of Object Hallucination Metrics: A Registered Audit" in the abstract, the title page and the cover letter. The choice is recorded in `outline.md`.
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
- (f) Done (PI default, approved in PI-1029p):
  - **Former §6 → Supplementary S3.**
    - Its introduction, data and fidelity text, Table 6.1 (now Table S3.1) and the leaderboard paragraph were copied verbatim, with their src comments. Its curve and placebo paragraphs were already in S3.
    - `sec6_rescoring_published_methods.md` is now a comment-only stub.
    - §3.3 keeps a four-sentence summary: 15 comparisons, 12 raw significant, 2/2/6 remaining, the registered seed placebo HELD (A22, calibration only), and the registered leaderboard not scored after its fidelity FAIL, |ΔCHAIR_i| = 1.49 > 1.0 (A23).
    - The old §6.5 (code and reproducibility) is folded into §3.6, because §1 contribution 4 and §8.2 point to it.
  - **Former §8.3–8.4 → Supplementary S8 and S6.** The full §8.4 text and Table S6.1 (all seven rows, same values as old Table 8.1) were already in S6. New §7.3 is a four-sentence summary that keeps the registered verdicts with estimate, interval and rule:
    - A21 RLAIF-V: 0.514 [0.509, 0.520] against ≥ 0.60, FAIL, inside the kill interval;
    - A20 VaPR: 0.849 [0.845, 0.853], PASS.
  - **Renumbering.**
    - Sections: old §7→§6, §8→§7 (old §8.4→§7.3, §8.5→§7.4), §9→§8, §10→§9.
    - Tables: old 7.1–7.3 → 6.1–6.3; old 6.1 → S3.1; old 8.1 → S6.1.
    - Method: one regex pass on visible text only, with no chained replacements.
    - Also covered: Table 1's Sections column, the Where column of Table S4.0, supplement headings, the cover letter, both declarations (the anon copy's stale "Section 11.2" is now 9.2) and the Fig. 2 labels (SVG and `scripts/figures/paperA_figs.py`: Section 7.2/7.3 → 6.2/6.3).
    - "Experiments II/III" are now "Experiments I/II".
    - A resolver confirmed that every visible "Section N" and "Table N" reference has a target.
  - **Registered results stay in the main text:**
    - every PASS/FAIL row of Table 1, including the PASCAL-50S FAIL (A24) in §1, Table 1 and §6.4, untouched;
    - A20 and A21 in §7.3;
    - A22 and A23 in §3.3.
  - `supplementary_SPIC.md` was regenerated from `supplementary.md` with `scrub_supp.py` (rc 0), and `supplementary_provenance_internal.tsv` was regenerated with it.
- (g) Done: an Introduction paragraph on reference-set dependence of quality measures (González-Chávez et al., 2024) was added.
- Net effect (first pass): visible main-text words went from 12,571 to 13,389 (+818). After the PI-1029p moves: 13,403 → 12,488 (sec1–sec11, scratchpad `wc.py`, all comments stripped). The first-pass 13,389 used a different counter, and the coordinator made edits between the passes, so the two series are not directly comparable. AI opinion: further cuts in §6.1–6.3 (old §7.1–7.3) are the next clarity lever.

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

1. Resolved (PI-1029p): UIT-OpenViIC, KTVIC and PASCAL-50S are confirmed in writing (the PI forwards the e-mails to the corresponding author). UIT-ViIC has no permission, so aggregates and pointers only.
2. Resolved (PI-1029p): the new title is kept, and §6 and §8.3–8.4 are moved in full.
2a. Coordinator: `manuscript/journal_draft_B/cover_letter_B.md` l.19 still cites Paper A under its old title ("Object Metrics Under Incomplete Gold …"). It was not edited, because it is outside A's scope.
2b. Coordinator: the bib entries for old Table 8.1's POVID and mDPO (zhou2024aligning, wang2024mdpo) and DOCCI (onoe2024docci) are now cited only in the Supplementary Material. They drop out of the main reference list (CAS build report).
3. Coordinator, FLAG 5b: V20 gold sizes per level. This needs the references re-staged; check whether the data rule allows it. It would be post hoc, with no verdict.
4. Coordinator:
   - any change to the deposit contents (item 15);
   - rows for the four new citations in `intext_trace.tsv`;
   - recount the "29 of 804 rows" in `declarations.md` and `anon/declarations_anon.md`, now that the manifest has grown.
   - `anon/declarations_anon.md` was edited in the PI-1029p pass: it gained the UIT-ViIC sentence, and its Section 11.2 reference became 9.2. It still lacks the new reproducibility sentence.
5. PI admin, low priority: addresses and the reviewer link (item 3).

## Round 3 (2026-10-30): ruling CC-181 text items, G0 (CC-182), plan T1–T6

Everything here is AI writer work, not a judge ruling. Nothing was committed. Every file was sha256-snapshotted before the first edit. Manuscript, bib, manifest, trace and response files were re-checked against the last known sha immediately before each write (guarded editor; no conflict seen). Not guarded: the first edits to the two plan files, the two LOG appends and the `scrub_supp.py` outputs (regenerated deterministically).

**W1 (plan).** `manuscript/directions/A_ALLOUT_PLAN_2026-10-30.md`: A CC-181 banner was added. A-T2 is struck everywhere it appears: the Vietnamese summary item 3, G1 row, ranked item 2, the M2 start note, the budget line, schedule rows 10-30 to 11-03, Q1 and Q8. §3.0 is struck and corrected: the "never scored" check had looked at `data/results` only, and the 1,519 images are C's test2500 (1,271) plus dev500 (248). Cosmetic: `~~` does not render across paragraphs, and the struck G1 row has fewer cells than its header.

**W2 (ledger).** One OPS line was appended to LOG.md. It gives both partitions: 1,519 = 1,271 + 248 (resolved pool, from the chair's check) and 1,984 = 1,673 + 311 (OIV7-labelled pool, re-run by the writer on `data/xm3600/oiv7_labels.json`). It also gives 600 + 500 + 2,500 = 3,600 with pairwise overlap 0/0/0 (re-run) and cites CC-108 r2, CC-153 r4 and CC-160 l.80. Host-clock note: the line is stamped 01:35:35Z, which is before CC-181's nominal 01:40Z, so the host clock and the ruling stamp differ by a few minutes. The line was not edited.

**W3 (sec7:38).** The sentence now reads: "The other 3,000 XM3600 images are the development (500) and one-look test (2,500) sets of a separate registered study and are not used here." A src comment names `data/xm3600_subset.txt`, `xm_dev500.files` and `xm_test2500.files`. There are three new manifest rows (counted). No other A file said "held out".

**W6 (G0; CC-182).**
- The G0 note and result arrived during this round: `data/results/a_g0/g0.json` (sha 23e12cbd), outcome B.
- §6.4 (old §7.4) has a "Gold sizes (post hoc descriptive, no verdict)" paragraph. It carries the NOTE's pinned outcome-B sentence verbatim, filled with 1,787 / 2,162 / 0.83.
- Per CC-182 W1, that paragraph also says outcome B already follows from X5 (1,782 vs 2 × 1,039.6), and it discloses 997 vs 1,000 images.
- §8.1 (old §10.1) and §9.1 carry one clause each, using "consistent with" only.
- Supplementary S7 holds the per-class table (Table S7.7) and the k-level sizes (Table S7.8).
- There are 76 G0 manifest rows.
- CC-182 integrity condition holds: S_voc 1,787 is in [1,782, 1,842], S_ref 2,162 ≥ 1,039.6, and the outcome is B.
- P50-A4 stays FAIL in §1, Table 1, §6.4, the abstract and the cover letter. The abstract and the cover letter were not edited.
- The "assumed, not measured" wording now reads "assumed at registration" wherever G0 measured the premise.

**W7 (A-T1).**
- Supplementary S7 has a new block with the registered clause-0 sentence verbatim: "the label rung was measured and was not twice as complete as one narrative on ADE20K training images".
- It also gives the numbers 1,553 / 1,248, ratio 1.24 < 2, from `gold_D1.json` (sha e0248451, matching LOG l.809).
- §6.4 has one sentence with the numbers, as PREREG §7.1 asks. It says the test was on a different dataset.
- New bib entries, both Crossref-checked: `zhou2017scene` (ADE20K) and `ponttuset2020connecting` (Localized Narratives).

**W8 (length and SPIC framing).**
- Main text went from 12,488 to 8,992 words: sec1–sec11, HTML comments stripped, scratchpad `wc.py`.
- Moved to the supplement (verbatim, with src comments):
  - Table 2.1 and the detail sentences of §2 → S9;
  - Table 6.2 → S10.1 (the same values are in Table S7.5);
  - Table 6.3 and the whole of old §6.5 → S7.6;
  - the full §6.3/§6.4 design, secondary and system-dependence paragraphs → S7;
  - every other condensed paragraph (§1, §3–§5, §6.1–6.2, §7.4, §8, §9) → new S10.
- The main text keeps condensed versions.
- Every registered FAIL, NOT_EVALUABLE and not-testable result keeps its verdict word, estimate and interval in its own main-text section: A2, A5, A10, A14, A15, A18, A19, A21, A23, A24, A24c and X-G6, checked by script.
- SPIC framing, wording only, no new citation: the opening paragraph and §8.4 now call object-hallucination scores reference-based quality measures of a visual description, whose reference is the gold.
- Number check (scratchpad `numdiff.py`): no number left the main text without appearing in the supplement, apart from the deleted heading number "7.4". Every new number has a manifest row; the only new 4-digit token is the citation year 2017.
- 8-gram/6-gram scan on all edited files: PASS, 0 hits.
- `supplementary_SPIC.md` was regenerated with `scrub_supp.py` (rc 0).
- CAS build to scratch: 21 pages, 0 overfull boxes, no placeholders.
- One regression was found and fixed during the build: the "Nguyen et al., 2026a" tie-break in §6.2 needed its cite comment next to the mention.

**W9 (citations).** Both papers were read in full text from open copies, with no e-mail in any request:
- Spain & Perona (IJCV 2011): CaltechAUTHORS author manuscript, sha 661ab380. Sect. 3 defines importance as the probability that a viewer mentions the object first.
- Berg et al. (CVPR 2012): author copy on umiacs.umd.edu, sha a6d1711d. Its abstract uses "what people describe as a proxy for importance".

Both support the §2 and §4.1 claim, so both are kept, and their bib comments were updated. `intext_trace.tsv` gained 8 A rows: Spain and Berg ×2 (SUPPORTED), Feng and Misra (NOT_SAMPLED; abstract only), ADE20K and Localized Narratives. A rows went from 88 to 96: 36 SUPPORTED, 12 PARTLY, 43 NOT_SAMPLED, 5 CANNOT_CHECK.

**W10.** SJR values and the 436-day figure are marked UNVERIFIED in the plan (§2 and banner) and in `V2_WRITING_PLAN_SPIC` l.383; the cover letter has neither. A LOG line records the target freeze 11-10 / submit 11-12 and the hard cap 18/12 (PI-1026ba), pending PI Q6.

**T6.** The reproducibility sentence was copied verbatim into `anon/declarations_anon.md`. `declarations.md` "(Section 9.1)" was corrected to 9.2, where the PASCAL departures are. §6.4 had the same stale reference, and it is fixed too.

**Not done / for the coordinator.**
1. The "29 of 804 rows" count (declarations, anon declarations, cover letter) comes from the Zenodo builder selection (CP-099, "recount at build"). It was not recounted, because the deposit was not rebuilt.
2. The abstract and the cover letter were not reframed for SPIC or extended with G0. They still state the P50-A4 FAIL.
3. No SPIC quality-measure papers were added (T2 asked for 2–3 after reading). That would need full-text reads and trace rows.
4. The moved blocks in S7, S9 and S10 keep their pre-revision section and table references and the pre-G0 "not measured" wording. A visible note at the head of each block says so. Supplementary S10 holds the pre-revision wording of condensed paragraphs. Some of it overlaps S7, and an editor may prefer it trimmed.


### Round 3, open items closed (2026-10-30, second writer pass)

This is AI writer work, not a judge ruling. Nothing was committed. Every edited file was sha256-snapshotted before its first edit (the list is `sha_before.txt` in the writer's scratch folder A_r3b). Each was re-checked against that snapshot just before it was written, and no conflict was seen. `supplementary_provenance_internal.tsv` is regenerated by `scrub_supp.py` and was not snapshotted.

**Item 2 (abstract and cover letter: SPIC framing and G0).**
- New abstract lead: "Object hallucination scores such as CHAIR and object F1 are reference-based quality measures whose reference, a gold object set, is usually incomplete."
- The G0 clause comes right after the P50-A4 FAIL, which keeps its number (−2.29 [−5.15, +0.61]). The clause reads: "a post hoc count (no verdict) found fewer VOC-label than reference-named class instances (1,787 vs 2,162), consistent with that failure".
- To stay at or under 240 words (CC-129 W5; the SPIC cap of 250 comes from the venue card), these cuts were made:
  - "(seven public LVLMs)" was dropped from the abstract; §6.4 still states it.
  - "mentions the labels cannot verify" became "unverifiable mentions".
  - The companion-test clause now uses the cover letter's wording.
  - "from one to 50 references" became "at every registered reference level".
  - Qwen3-VL-8B moved into parentheses.
- The abstract is now **239 words** (wc -w, comments stripped).
- The cover letter has the same framing sentence and the same G0 clause. Its fit sentence keeps the scope phrase "multimedia quality assessment and measures" and now calls the score a reference-based quality measure of a visual description.
- The official SPIC guide-for-authors page returned HTTP 403, so the 250-word cap was taken from `writing_guide/VENUE_CARDS_PAPER_A_Q2_2026-10-27.md` (l.24, l.67) and was not re-verified today.
- No SPIC or Elsevier skill exists in `.claude/skills/`.
- A-T3 appears only as an HTML-comment placeholder, in `abstract_A.md` and in `cover_letter_A.md`. Neither placeholder holds a number or a verdict, and neither reaches `meta.yaml` or the PDF (checked).
- Manifest rows 1250–1251 (1,787 and 2,162; `g0.json` 23e12cbd) now also list the abstract and the cover letter as uses.

**Item 4 (supplement numbering and the S10/S7 overlap).**
- S7 tables are now numbered in order of appearance:
  - old S7.7 (per-class G0 table) → **S7.6**;
  - old S7.8 (k-level sizes) → **S7.7**;
  - old S7.6 (system jackknife; Table 6.3 before revision 2) → **S7.8**.
- These numbers are cited only inside the supplement. The visible main text cites none of them.
- Stale cross-references in the moved blocks were fixed:
  - "(Table 6.2)" → Table S7.5;
  - the PASCAL-50S departures reference "Section 9.1" → 9.2;
  - S10's "random-deletion check of Section 6.3" → "on the sets of Sections 6.2–6.3 (Supplementary S7)", because §6.3 no longer describes that check.
- S10's bold main-text table labels (**Table 1.**, **Table 5.1.**, **Table 6.1.**) were relabelled "Pre-revision caption of Table …".
- The three italic notes (S7, S9, S10) now say that cross-references follow the current numbering, and they keep the pre-G0 "not measured" caveat. The S10 note also says that some paragraphs are replaced by pointers.
- Overlap removed: S10 lost four blocks that S7 already gives in full. Each was replaced by a one-line italic pointer.
  - the condensed COCO-5000 and English LVLM paragraphs (S7 "Further detail for Section 6");
  - the condensed UIT-ViIC paragraph (same S7 subsection);
  - Table S10.1, which equals the clean-subset columns of Table S7.5 value for value. Table S10.1 no longer exists; the sec7 comment that named it was updated (comment only).
  - the "PASCAL-50S outputs" paragraph (S7 "Compute and data handling" and "Departures from the PASCAL-50S registration").
- Number check (`numdiff.py`): nothing was lost, and no new number lacks a manifest row. The only distinct supplement number that changed is the section reference 9.1 → 9.2.
- `supplementary_SPIC.md` was regenerated with `scrub_supp.py` (rc 0).
- Not done: S10 "From Section 2" still partly overlaps S9 "Extended related work". The Vietnamese-data and F-measure paragraphs share 50/71 and 35/126 8-grams with it. This was out of scope for this pass.

**Item 1 (still open, flagged).**
- The "29 of 804" count needs a Zenodo deposit rebuild.
- It appears in `declarations.md` l.19 and `anon/declarations_anon.md` l.14. It is **not** in the cover letter, so the Round 3 note above is wrong on that point.
- The manifest now has 1,324 data rows, so 804 is stale. Recount at the rebuild (CP-099); do not hand-edit.

**Checks.**
- Main text: 8,992 words (sec1–sec11, comments stripped; unchanged).
- 8-gram/6-gram scan (`ngram_scan_cen.py`): 0 hits on `abstract_A.md`, `cover_letter_A.md`, `supplementary.md`, `supplementary_SPIC.md`, `sec7_verbosity_sign.md` and `number_manifest.tsv`.
- CAS build to scratch: rc 0, 21 pages, 0 overfull boxes, and no report placeholders.
  - The title page's visible "[ADDRESS: PI to supply by 11-04]" predates this pass and is a PI admin item.
  - The abstract was read back from the PDF.
- No new claim and no "first" claim was added. No A-T3 result exists, and none was written.
