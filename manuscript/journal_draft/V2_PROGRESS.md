# Paper A v2 (SPIC): progress, 2026-10-27

## Pass 3 (2026-10-28, writer; nothing committed)

Pre-edit backup: `.session_backup/2026-10-28/snapshots/A_pass3/before/` (39 files, `SHA256SUMS`). Final files: `.session_backup/2026-10-28/snapshots/A_pass3/` (`SNAP.sha256`). No new number: a numeric-token diff of the visible text against the backup finds only section, list and row ids (3.1, 3.6, 6.5, 9.3, X-0, SHA-256, uv231, XM3600). No new citation, experiment or annotation.

### Changes, by scorecard criterion (CC-126 W1 anchors; A was 2/2/3/2/1/2 = 12)

| Criterion (anchor) | Change | Where |
|---|---|---|
| Novelty (prior-art distance) | **Contributions** became a numbered list of four, opened by one positioning sentence (prior validity work asks whether metrics measure what they should; this paper makes the gold the experimental factor). Item 1 is scoped as §9.5 scopes it ("on XM3600, repeated with a second backbone on the same images"). New closing paragraph **"Position of this paper"** in §2 names three features, each restating a claim already made and cited in §2: the gold as factor, versus gold-quality work on classification and probing labels, with §2's own contrast that the captioner chooses how many objects it names; per-image count matching on released captions, versus LeHaCE and CCEval; registration with failures. | sec1 "Contributions"; sec2 last paragraph |
| Application (registered PASS share) | §9.3 is retitled "Using the results: a checklist for authors and reviewers". A new use-case paragraph shows (i) a reviewer's request for $M$ plus one count-matched difference, citing the OPERA-on-Shikra reversal against the two gains that survive in the **post hoc** re-scoring (§6.2), and (ii) a preference-data builder's count check (four of seven sets, §8.4). Contribution 4 points to the checklist. | sec10 §9.3; sec1 |
| Evidence (headline REG PASS and LOO-stable) | §10.1 is renamed **"Threats to validity"**, and its eight paragraphs are regrouped: construct (precision rule; vocabulary and matchers), internal (truncation; count control; exposure), statistical conclusion (system dependence plus one new multiplicity sentence: uncorrected registered intervals, so the claim rests on the ordering that passed on both backbones) and external ((A3) family scope; human-judgment regime). The paragraph text is unchanged apart from the labels, the moved (A3) sentence and a shortened truncation sentence, which keeps "within-cluster slopes are not interpreted" (plan §2, Ken W7). The §10.1 intro and the §9.1 opener were also shortened. | sec11 §10.1 |
| Venue fit (type match and format) | Elsevier `[dataset]` tags on all 16 dataset references; 0 overfull boxes; "Page N of M" corrected; one abstract source for both builds; third-person self-citation. Build details are below. | build, sources |
| Artifacts (released, DOI, external run) | §6.5 stub replaced by **"6.5 Code and reproducibility"**. It describes only what exists: the manifest with SHA-256, commit times, Table 1, the §6.1 fidelity check, the X-0 frozen-input hash check and the restricted record. It says plainly that the record is not public and that the code has not been run outside the group. §9.2 "archive the scorer" became "deposit the code". No "released scorer" claim is left anywhere. | sec6 §6.5; sec10 §9.2 |
| Writing (guide compliance) | Main text cut 11,413 → **11,348** words, with all additions absorbed. Cuts came only from exploratory or duplicated prose whose detail is in S7/S8 or another section: §7.1 condensed; the §7 intro; §7.3's INCONCLUSIVE intervals (P2, P3a, P4) and the A13 τ values, both in S7; the §7.3 nested-rungs sentence (in §4.2 and §10.1); the §7.5 within-prompt sentence and the −0.38 correlation (S7); the §7.5 scope sentence (§9.5, §10.1); §8.3 condensed (S8); §8.5; the §8 intro annotation sentence (§3.6 (iii), Ethics); §9.1 bullets merged; §5.3; §2's Chen et al. sentence (still cited in §4.1); §6 intro and registration. No registered FAIL sentence was removed. Every Table 1 "Where" target still exists. | all sections |

**Anonymization (body).**
- "our earlier work (Nguyen et al., 2026a)" → "earlier work (…)" (sec1) and "an earlier study (…)" (sec7).
- "companion manuscript (Nguyen et al., in preparation; …)" → "(in preparation; …)" (sec5).
- The supplement was already third person.
- A grep of visible text in sec*, abstract and highlights for the author names, affiliations, "our earlier", "withheld" and "Anonymous" finds 0 hits.
- The title page, the CAS author block and the CRediT names are **kept**: PI-1026ad set SPIC to single-anonymized (see CC-140 item 6).

**Abstract.** Unchanged, 235 words. A closing checklist sentence was considered and dropped: the abstract's own note binds it to ≤ 240 words (CC-129 W5), and the abstract sits next to judge question J1.

**Tense of the deposit.** §6.5 repeats the declarations' present tense ("are deposited … as a restricted record"). The Zenodo record is still PI-pending (Open items, PI 2). §6.5 and the Data availability statement become true only once the PI creates the restricted record. The declarations are the authors' text and were not reworded.

### Remaining writer work from pass 2: status

1. **The cut to 11,350.** Done: 11,348 words (same counter: comments stripped, sec1–sec11 plus declarations, `wc -w`).
2. **outline.md abstract vs abstract_A.md.** `build_A_cas.sh` already read `abstract_A.md` in pass 2. Pass 3 also points `build_A_elsarticle.sh` (the IP&M/JVCIR-template path) at `abstract_A.md` and marks the `outline.md` abstract SUPERSEDED in a comment. `outline.md` text is otherwise untouched. The elsarticle build was run once into scratch after the change: exit 0, 72 pages (legacy IP&M anonymized route; its anonymity scan flags the FAIR bib entry, as before). It is otherwise untested.
3. **`[dataset]` tags.** `build_A_cas.sh` now prefixes `[dataset]` in the `.bbl` after bibtex, then runs two more xelatex passes. The step is idempotent: re-running in the same directory gives single tags.
   - Tagged (16, all cited): lin2014microsoft, chen2015microsoft, thapliyal2022crossmodal, lam2020uit, young2014image, plummer2015flickr30k, matsuda2025vela, wadhawan2025vapr, kasai2022transparent, aditya2015images, wada2024polos, gordon2025unblocking, onoe2024docci, gunjal2024detecting, bui2026uit, pham2024ktvic.
   - young2014image (Flickr30k) and onoe2024docci (DOCCI) were added to the pass-2 list because both are datasets used in the text.
   - Borderline: chen2015microsoft (COCO Captions) is now cited only in §4.1, for its naming model. The entry is the dataset paper of captions this paper uses, so the tag is kept; the gatekeeper may drop it.
   - **Not tagged:** huang2024opera and yue2024less. These keys are method papers. The data actually used are their released CHAIR logs, which would need separate `[dataset]` entries for the log repositories, with URLs checked on the primary record. Not done; flagged.
   - **`[software]`:** none yet. The only candidate is our own Zenodo record, which does not exist publicly.
4. **§6.5.** "After R2/R3" refers to writing-plan §3.5, the scorer-release steps: R1 package, R2 fidelity test, R3 clean-environment external run, R4 DOI. None was executed: there is no `vsps-eval` package, no commit and no hashes. §6.5 is now complete without them (see the table above). If R1–R4 run before 11-06, §6.5 gains one sentence per step, and the manifest gains the R3 hashes.
5. **CAS build:** see "Build, pass 3" below.
6. **11-05 supplement strip:** checklist below, not executed.

### Build, pass 3

- **Route:** `OUT=<scratch> bash manuscript/build/build_A_cas.sh`, with pandoc 3.5, TinyTeX xelatex and `elsarticle-num-names.bst`.
- **Output:** scratchpad `A_pass3/paperA_SPIC.pdf`, with a copy in the snapshot.
- **Result:** **24 pages** (footer "Page 24 of 24"); **0 overfull hboxes** (pass 2 had 1, 117 pt); 0 undefined citations or references.
  - Mentions: 91 matched and converted (92 before; the removed mention was §2's Chen et al. 2015, which stays cited from §4.1).
  - Keys: 75 of 93 cited; `nguyen2026vsps` is still cited.
  - 16 dataset tags.
  - 1 placeholder (Polaris/DOCCI licence).
- **Overfull box cause.** Found by bisection (removing the keywords block clears it; the address placeholder and emails do not). `cas-common.sty` l.1521 puts the 117 pt keyword box in a zero-width `\hbox` with no `\hss`, by design, so the box is a logged false positive with no visible effect. **Fix** in `cas.pandoc.tex`: `\hfuzz=120pt\maketitle\hfuzz=.2pt`, where .2pt is the class default (`cas-common.sty` l.31). Caveat: this also hides any real front-matter overfull box under 120 pt, so **check page 1 by eye after the postal addresses go in on 11-04**.
- **"Page 24 of 23".** `cas-common.sty` writes `\lastpage` before the last page ships. `cas.pandoc.tex` now rewrites it after `\clearpage`.
- **Left as is (cosmetic, template):**
  - "ORCID(s):" prints empty in the first-page footnote;
  - 1 "No positions in optional float specifier" warning;
  - 3 hyperref "empty anchor" warnings.
- **Counts:** main text **11,348 words**; abstract **235 words**.
- **N-gram scan** (`ngram_scan_cen.py`; all positive controls fire): **NGRAM SCAN PASS, 0 hits**. Scope: sec*, abstract, highlights, declarations, title page, `supplementary_SPIC.md`, this file, the build's `md/*.md` and the built `.tex`.

### 11-05 supplement strip: checklist (prepared, NOT executed)

`supplementary_SPIC.md` is currently in sync with `supplementary.md`: a re-run of `scrub_supp.py` into scratch is byte-identical (442 comments, 0 leaks). On 11-05:

1. **Freeze the source.** Confirm `supplementary.md` has no edits since the last scrub (sha against the snapshot), because another tool writes in this repo.
2. **Regenerate.** Run `python3 manuscript/build/scrub_supp.py journal_draft/supplementary.md journal_draft/supplementary_SPIC.md journal_draft/supplementary_provenance_internal.tsv`. It must exit 0 with "0 leaks", since the LEAK regex covers `.session_backup`, CC/CP/PD/PI/OPS/INC ids, `manuscript/`, `data/results`, `scripts/` and `src:`.
3. **Extra greps on the published copy** (each must return 0):
   - `<!--`;
   - `/mnt/`;
   - `\b(D|K|W|J|P)[0-9]+\b` used as decision ids, checked by eye because some are table ids;
   - `Ken`, `Gemini`, `Claude` as whole words;
   - `\[(AUTHOR|PI|ADDRESS|CITE|TODO|STUB)`;
   - `Material moved`, `old §`, `v2`, `pass [0-9]`;
   - host, IP and port patterns (`([0-9]{1,3}\.){3}[0-9]{1,3}|\.local|ssh `).
4. **Cross-references to the main text.** Check each "Section N.N" in the supplement against v2 numbering. Already seen:
   - "Sections 7.3 and 9.5" (cap share): the cap limitation is now in §10.1, not §9.5;
   - "Section 8.3": check that it means v2 §8.3 (short captions) and not old §8.3 (full gold);
   - every "Section 10" and "Section 11" pointer.
5. **Citations.** The supplement keeps author-year prose. Decide (gatekeeper) whether it gets its own reference list or uses the main numbered list. SPIC asks that supplements be cited and captioned, and it publishes them as received.
6. **Captions.** Every S-table and S-figure has a caption, and the main text cites each S-section it relies on (S1–S9).
7. **N-gram scan** on the published copy: 0 hits, with the positive controls firing.
8. **Snapshot.** Write the published copy and provenance TSV to `.session_backup/<date>/snapshots/` with sha256 before upload.
9. **Provenance.** The provenance TSV and `supplementary.md` stay internal. They are never uploaded, and they go into the Zenodo restricted record only if the PI approves.

### Realistic scorecard ceiling from text alone (for the 11-08 panel; the writer's estimate, not a score)

| Criterion | CC-126 | Text can reach | Why |
|---|---|---|---|
| Novelty | 2 | 2 | The anchor is verified prior-art distance. The positioning makes the distance legible but adds no new result. 3 needs a confirmatory count-control result (A-1 did not run, N = 3). |
| Application | 2 | 2 | The anchor is the registered in- and out-of-domain PASS share, which text cannot change. The use-case paragraph helps readers, not the anchor. |
| Evidence | 3 | 3 | Unchanged registered record. Threats-to-validity are now explicit. |
| Venue fit | 2 | 3 | Type match (SPIC quality-measure framing, §9.4 and §2), numbered references, dataset tags, a clean build. Still open: postal addresses, Zenodo link, licence placeholder. |
| Artifacts | 1 | 1 | PI-1026ae keeps the record private, and R1–R4 are not done. This **fails the Q2 hard threshold** (artifacts ≥ 2). |
| Writing | 2 | 3 | Contributions, threats, length at target, no stubs, third person. |
| **Total** | **12** | **≈ 14** | Q2 (≥ 20, novelty ≥ 3, artifacts ≥ 2) cannot be reached by text. It needs A-1-type evidence and a public release with an external run. |

## For CC-140 (judge items; the writer does not decide them)

1. **W11 numbered `.bst`.**
   - **Status.** OPS-1027b (pass 2) already chose `elsarticle-num-names.bst` without a ruling. The CAS bundle (CTAN els-cas-templates v2.4) names `model1-num-names` in `cas-sc-template.tex` but does not ship it.
   - **Options:**
     - (a) ratify `elsarticle-num-names.bst`. It is Elsevier's own elsarticle bundle and gives numbered, citation-order references (the built list starts at [1] = Rohrbach et al. 2018, the first citation) with natbib author names for "Lipton et al. [n]".
     - (b) obtain `model1-num-names.bst` from Elsevier support before 11-10.
     - (c) submit the PDF and source, and let Elsevier typesetting restyle.
   - **Recommendation: (a)**, with (b) as a no-cost check if support answers before the freeze. The visible format, numbered square brackets in order of first appearance, is what the Guide for Authors asks. The `.bst` name is not checked at submission.
2. **X-21 label (N2-XM-FULL150).**
   - **Evidence.** The verdict file (`xm3600_full_verdict.json` prereg_comparisons[21]) says PASS. `tests_status.tsv` l.14 says POST_HOC, because the registration (`2026-10-14_xm3600_predictions.json :: b_N2_adjacency_audit_completed_pre_gpu.observed_full_150_images.adjacent_share` = 0.5333) quotes the check's own result.
   - **Options:**
     - (a) keep the current two-part label;
     - (b) Status "post hoc (registration quotes its result)", Verdict "PASS (verdict file)";
     - (c) registered PASS.
   - **Recommendation: (b).** Table 1's own definition ("committed before the first output it predicts") makes the status post hoc. The verdict word is still copied verbatim. (c) contradicts that definition.
3. **X-22 verdict string.**
   - **Evidence.** v1 (`xm3600_full_verdict.json`) says `PASS_DRHO113_MIXED_MCP_CI_INCLUDES_1`. The append-only v2 (`xm3600_full_verdict_v2.json`, same directory) says "MIXED — no primary estimator registered". The registered threshold names "MCP / frontier residual d_rho" without a primary, and 2 of 4 estimator CIs have an upper bound below 1. Neither verdict file is in git (`.session_backup` is untracked).
   - **Options:**
     - (a) v1 verbatim (current);
     - (b) v2 verbatim;
     - (c) v2 verbatim, plus a Table 1 note that v1 recorded `PASS_DRHO113_…`.
   - **Recommendation: (c).** v2 is the later append-only record (D21), and its string matches what the registration allows. Printing both keeps the audit trail.
4. **X-22 to X-25 sentences.**
   - **Conflict.** W1 forbids new numbers. Ruling 2 asks for an estimate sentence for MIXED rows. The κ values (0.6499 … 0.7603) sit in the verdict file but **not** in `number_manifest.tsv`.
   - **Options:**
     - (a) table-only, as now;
     - (b) one verdict-words sentence in §7.2, with no numbers: "The two-panel transfer prediction is mixed across the four registered estimators, and the three verified-label predictions for the adapters passed (Table 1; Supplementary S7)" (about 30 words, to be offset by a cut);
     - (c) (b) plus the κ estimates in S7, after the coordinator keys four manifest rows.
   - **Recommendation: (b)** now, and **(c)** only if the rows are keyed by 11-05. (b) meets ruling 2's intent without breaking W1.
5. **A16 registered threshold.**
   - **Evidence.** The prereg `manuscript/prereg/2026-10-19_a_n3_criterion_mhaldetect.md` l.54–57 (and `.json :: predictions.AN3-P2.rule`) gives AN3-P2 = "compound of sign_gt_0", where sign_gt_0 = PASS if ci95_lo > 0, FAIL if point ≤ 0, else INCONCLUSIVE. The rule sits at prediction level, which is why the parts carry no `rule` field.
   - **Check.** Part 2 is +0.010 [−0.002, +0.023], so INCONCLUSIVE, which matches the verdict and the text's "not detectably".
   - **Options:**
     - (a) keep the current text;
     - (b) add the rule in §8.2 (about 15 words: "registered rule: PASS if the lower bound exceeds 0, FAIL if the point is ≤ 0").
   - **Recommendation: (b).** The same sentence already quotes the "point ≤ 0" rule for A15, so stating A16's rule makes the pair symmetric. It needs a 15-word offset.
6. **Anonymization mode (new).**
   - **Conflict.** The 10-28 coordinator brief says "A is double-anonymized; FAIR in the third person; no author names or affiliations in the body". PI-1026ad (LOG l.523, 10-27) and the SPIC Guide for Authors say **single-anonymized**, with de-anonymization for SPIC. The build prints the title-page authors, and the declarations carry CRediT names and "by the same authors".
   - **Pass 3 did what is valid under both:** third-person self-citation and no names in the body. It kept the author block and CRediT.
   - **Options:**
     - (a) single-anonymized per PI-1026ad (current);
     - (b) double-anonymized: strip the CAS author block, move CRediT and "Related manuscript" to a separate file, use the `anon/` route.
   - **Recommendation: (a).** (b) would reverse a PI ruling and needs the PI.

## Pass 2 (coordinator instructions, after snapshot paperA_v2_pass1; backup .session_backup/2026-10-27/paperA_v2/before_pass2/, 41 files with SHA256SUMS)

- **Numbered references and CAS build (OPS-1027b).**
  - New `manuscript/build/build_A_cas.sh` builds with `cas-sc` (CTAN els-cas-templates v2.4, copied to `manuscript/build/templates/cas/` with SOURCES.txt), `elsarticle-num-names.bst`, natbib `numbers,sort&compress` and the new template `manuscript/build/cas.pandoc.tex`.
  - The new `prep.py numcites` turns the author-year mentions into numbered citations in build copies only; the sources are never written. All 92 mentions are converted (82 before pass 2, plus the new dataset citations), 75 keys are cited, and none is unresolved. It has a self-check.
  - `prep.py meta` now reads the title, abstract and keywords from `abstract_A.md` (outline.md is no longer used for A's SPIC build), and `prep.py casauthors` builds the author block from `title_page_A.md`.
  - `filter.lua` allows line breaks inside long underscore verdict strings. This changes rendering only.
  - TinyTeX gained colortbl, moreverb and sttools.
  - **PDF:** `.session_backup/2026-10-27/builds/A_cas/paperA_SPIC.pdf`, **24 pages** (sha256 1cb5e8a3…). Check report: 0 undefined citations or references; 1 overfull box (117 pt, the `\maketitle` front-matter box); 1 placeholder (Polaris/DOCCI licence).
- **Trim.** §1 prose: the contributions list became one paragraph and §1.3 became §1.2. §3 was also cut. The main text is now **11,413 words**. Table 1 is unchanged, and every registered row keeps its main-text row and sentence.
- **Figures.** `figs/fig4_lambda_channels.pdf` and `figs/fig2_slope_by_gold.pdf` (rsvg-convert).
- **Citation pass.** Seven sets are now cited in Table 8.1, each with its DOI checked on Crossref (title and first author match): HA-DPO zhao2025beyond, HSA-DPO xiao2025detecting, mDPO wang2024mdpo, SENTINEL peng2025mitigating, RLHF-V yu2024rlhf, RLAIF-V yu2025rlaif and DOCCI onoe2024docci. POVID (zhou2024aligning) has no DOI; its arXiv 2402.11411 title was checked instead.
- **Supplement scrub.**
  - New `manuscript/build/scrub_supp.py` (has a self-check) writes the published copy `supplementary_SPIC.md`, with all 442 HTML comments removed. It fails if any path or decision id remains.
  - The provenance goes to the internal manifest `supplementary_provenance_internal.tsv` (comment no., source line, heading, preceding text, comment).
  - Internal headings and labels in the source ("Material moved … in v2", "old §", "(old Table …)") are now neutral.
  - `supplementary.md` keeps its comments as the internal source of record.
- **Competing interests.** Reverted to the authors' sentence, "The authors declare no competing interests." Option for the PI: Elsevier's standard wording, "The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper."
- **§6.5** is left as a stub.

## Pass 1

Writer pass under `V2_WRITING_PLAN_SPIC_2026-10-27.md` (sha256 `a13760c6…67ee8`, checked at start and end), as amended by CC-129 and PI-1026ae. Nothing is committed. The pre-edit backup is in `.session_backup/2026-10-27/paperA_v2/before/` (29 files, `SHA256SUMS`).

## Done

- **W1 Table 1** (`sec1_introduction.md` §1.3) maps every registered row:
  - all 26 `prereg_comparisons` of `xm3600_full_verdict.json`:
    - #0 → X-0;
    - #1–15 → X-G, with #6 OUT as its own row X-G6;
    - #16–20 → A1–A5;
    - #21 → X-21;
    - #22 → X-22;
    - #23–25 → X-23–25;
  - AUDIT A6–A25;
  - post hoc rows P-1 to P-4.

  The table holds verdict words only. Old Table 11.1 moved to S4 as Table S4.1.
- **W2 de-anonymization.**
  - All 8 placeholder sites were replaced: sec1:13 (now a FAIR 2026 citation, text checked with `pdftotext`), sec5:38, sec11:41, and supplementary 74, 193, 267, 289 and 293. Each now points to Paper B ("in preparation; a copy is available to the editor") or to Table 1.
  - The IP&M residue in the title page, declarations, cover letter and bib header was removed.
- **W3 claim-map rows** are listed below.
- **W4 DERIVED row.**
  - `scripts/paperA/a1_loo_triples.py` (sha `6a7a49f4…`, has a self-check) writes `data/results/a1_robustness/loo_triples.json` (sha `d74f34c4…`): 6 of 6 drops ordered.
  - The same file holds the W9 rung-implied −6.39. CC-129 printed −6.38, from rounded inputs.
  - The manifest gained 13 rows: DERIVED ×4, W6 ×2, thresholds ×2, verdict words ×5.
- **W5 abstract** (`abstract_A.md`): variant A, **235 words**, with "537 of the same 600 images" and "both involving the all-reference gold". Also in that file: title T1 and 7 keywords.
- **W6:** C23 now cites the registered key `l6_d2_evaluation…rlaifv_all_obj_pairs` (0.514 [0.509, 0.520]).
- **W7:** highlight 2 is scoped to XM3600 and names the one verbose system (`highlights_A.md`; 5 lines of 79–84 characters).
- **W8:** the truncation and two-cluster sentence is in §7.3 and §10.1.
- **W9:** the lower-rule ordering on the second backbone is stated at point level from the DERIVED row (§7.3).
- **W10:** §6.5 is a stub that makes no claim. Nothing in the text names Ken as a runner.
- **W11:** see the open items; the numbered conversion is held.
  - Added and checked: González-Chávez et al. 2024 (Crossref) and Holm 1979 (OpenAlex; cited without a DOI).
  - Step 1 of the conversion is in `citation_map_A_v2.tsv`: 82 mentions map to 66 keys, none unresolved.
- **W12:** no Paper B number is cited.
- **Section rewrites and cuts.**
  - §8 and §9 merged; §10 → §9 and §11 → §10. `sec9_preference_audit.md` and `appB_matcher_sensitivity.md` are now comment-only.
  - Moved text is copied verbatim, with its `src` comments, into S1, S2, S4, S5, S6, S7, S8 and S9 under "Material moved … in v2".
  - Supplement cross-references were renumbered by a single-pass script.
- **Declarations** are in SPIC order, with the exact no-funding sentence and an Option C data statement (private Zenodo link).
- **Cover letter** retargeted to SPIC.
- **Title page:** order Hoa, Thinh, Lang\*; no first-author email; `[ADDRESS: PI to supply by 11-04]` placeholders.

## Word counts (comments stripped, `wc -w`, tables included; the counter reproduces the plan's 14,332 on the backup)

| File (v2 section) | Before | Now | Plan target |
|---|---|---|---|
| sec1 (§1, incl. Table 1 ≈ 675) | 1,180 | 1,512 | 1,450 |
| sec2 (§2) | 1,218 | 872 | 850 |
| sec3 (§3) | 1,416 | 1,324 | 1,250 |
| sec4 (§4) | 1,129 | 484 | 450 |
| sec5 (§5) | 729 | 572 | 500 |
| sec6 (§6) | 957 | 954 | 900 |
| sec7 (§7) | 3,813 | 2,930 | 2,900 |
| sec8 + sec9 (§8) | 1,399 + 662 | 1,216 + 0 | 1,150 |
| sec10 (§9) | 673 | 694 | 700 |
| sec11 (§10) | 805 | 723 | 750 |
| declarations | 351 | 417 | 450 |
| **Total** | **14,332** | **11,698** | ≈ 11,350 (ceiling 12,000) |

- The total is 348 over the target and under the ceiling. Most of the excess is Table 1, which came out about 225 words over its estimate because it maps all 26 entries. A further cut is possible in §1, §3 and §8.
- Abstract: 235 words. Supplement: 16,163 words.

## W3 claim-map rows (addendum to plan §4; the plan file stays unedited because it is hash-locked)

| # | Claim | § | Status | Number | file::key |
|---|---|---|---|---|---|
| C28 | Rise at every added reference (A7) | 7.3 | REGISTERED PASS | +3.99 [+1.70, +6.02] (cv295, first step) | `g2b_score.json :: datasets.cv295.predictions.G2B-O2.parts[0]` |
| C29 | Span-label agreement 1 ref → all → COCO-80 (A15) | 8.2 | REGISTERED **FAIL** | +0.057 [+0.043, +0.071]; −0.021 [−0.043, +0.002] | `a_n3_run.json :: predictions.AN3-P1.parts[0..1]` (rows 630–631) |
| C30 | Condensed F1 vs F1 on span labels (A16) | 8.2 | REGISTERED INCONCLUSIVE | +0.049 [+0.033, +0.064]; +0.010 [−0.002, +0.023] | `AN3-P2.parts[0..1]` (632–633) |
| C31 | Tone-mark normalisation (A25) | Table 1 | no verdict field | — | `data/results/tone_norm/SUMMARY.json` |
| C32 | XM3600 LOO per-drop ordering | 7.5, 9.1 | DERIVED (POST_HOC) | 6 of 6; +10.52 < +18.07 < +23.21 | `loo_triples.json :: xm3600_loo_n_ordered`, `xm3600_loo_triples.xm3600_zeroshot-detailed` |
| C33 | Second backbone lower-rule ordering (W9) | 7.3 | DERIVED (POST_HOC) | +1.97 vs −6.39 | `loo_triples.json :: g2b_xm600_*` |
| C34 | Gold-size value OUT (X-G6) | 7.2 | REGISTERED OUT | 1.8768 vs 1.8831 | `xm3600_full_verdict.json :: prereg_comparisons.6.*` (223–225) |
| C35 | Equivalence band and intercept threshold (A8–A11) | 7.3 | registered thresholds | 0.05; 2 | `g2b_score.json :: …parts[*].delta` (new rows) |
| C23′ | RLAIF-V share (W6) | 8.4 | REGISTERED FAIL | 0.514 [0.509, 0.520] | `c6_n3_rlaifv_rlhfv_audit.json :: l6_d2_evaluation.prediction_rlaifv_chosen_fewer_among_unmatched_ge_060.{rlaifv_all_obj_pairs, _ci95}` |

## Anonymization grep (CC-129 W2)

- **Pattern:** `withheld|anonymi|elsewhere|IP&M|until the decision|Anonymous`, case-insensitive. Raw files, comments included.
- **Scope:** sec1–sec11, supplementary, appB, title page, declarations, cover letter, abstract, highlights, `paperA.bib`, `paperA_manual.bib`.
- **Not in scope:**
  - `anon/`, which stays untouched by rule;
  - the hash-locked plan;
  - `outline.md`, `results_plan.md` and `paperB_outline.md` (internal notes);
  - the manifest.
- **Result:** 1 hit, `cover_letter_A.md:25`, "is not under consideration elsewhere". This is the standard submission sentence and is legitimate.

## Post-review fixes (advisor read, 2026-10-27)

- **A-1 wording.** `git log --all` finds no committed A-1 prereg, so the four places that called it a "registered confirmation" now say "planned" (sec1, sec6, §9.1, §10.1).
- **LOO scope.** The §1 sentence is now scoped to XM3600.
- **§8 times pointer.** "Times are in Table 1" now points to S4 only.
- **Table 1 coverage.** Every prediction id was enumerated from `a_n2_run.json` (LBA-P1/P2), `a_n3_run.json` (AN3-P1/P2), `an1_score.json`, `q2_longcap_arena.json` (tests i–iii), `q4_vapr`, `k2_scores.json` (K2), `g2b_score.json` (E1, E2, O1, O2, P1, P2, P3a, P3b, P4) and N9 (a)–(c). Every id has a Table 1 row.
- **New-number diff against v1.** The only new numeric tokens are section and row ids, the year 1979, and keyed values: the bracket upper CIs (rows 659–660), 1.8768/1.8831 (223–224) and −6.39 (new DERIVED row).
- **Citation diff against v1.** v1 cites 71 keys and v2 cites 67.
  - Dropped on purpose (pool-bias paragraph cut, plan §2; the text is kept in S9): buttcher2007reliable, jain2016extreme, lu2016effect, webber2009score, yilmaz2006estimating, zobel1998reliable.
  - `young2014image` had been dropped by accident and was restored in Table 5.1.
  - Added: gonzalezchavez2024metrics, holm1979simple.
  - Still unmentioned, and already unmentioned in v1: onoe2024docci and the preference-set keys (zhou2024aligning, wang2024mdpo, yu2024rlhf, yu2025rlaif, …), under the old "[CITE: all seven to be checked]" note. These need a citation pass before the build.
- **Supplement hygiene.**
  - Demoted headings in the moved blocks now carry an "old §" prefix (11 headings).
  - S5 tables are relabelled S5.1 (existing) and S5.2 (old main-text table).
  - A placeholder pointer that came back with the moved S5 text was replaced.
- **Declaration wording changed** (reverted in pass 2; see the top of this file).

## Open items

**Needs the PI**
1. Three postal addresses by 11-04: title page and cover letter.
2. The private Zenodo link at submission: data availability, title page and cover letter.
3. **Artifacts anchor:** per PI-1026ae the vsps-eval record stays private, with a reviewer-only link. The artifacts anchor therefore **stays below 2 at submission**, and this must be disclosed to the 11-08 CP panel.
4. Title choice: T1 is in place as the working title.
5. Licence wording for Polaris and DOCCI-Critique (`[AUTHOR TO CONFIRM]`, §10.2).
6. Acknowledgements text, if any.
7. Whether the OpenViIC/KTVIC confirmation has arrived (data statement).

**Needs a judge or the coordinator**
1. **W11 numbered style (resolved in pass 2: OPS-1027b, elsarticle-num-names.bst).** The CAS bundle (CTAN els-cas-templates v2.4) has no numbered `.bst`.
   - `cas-sc-template.tex` names `\bibliographystyle{model1-num-names}`, and that file is not shipped.
   - `elsarticle-num-names.bst` is available in TinyTeX and in `manuscript/build/templates/elsarticle/`.
   - Ruling needed: is that file acceptable, or must `model1-num-names.bst` be obtained from Elsevier? Steps 2–3 of the conversion are held until then.
2. **X-21 label (N2-XM-FULL150).** The verdict file says PASS; `tests_status` says POST_HOC. The text shows both and treats the check as post hoc, pending the coordinator's record (CC-129 W1).
3. **X-22 verdict string.** The v1 file has `PASS_DRHO113_MIXED_MCP_CI_INCLUDES_1`; the v2 record has "MIXED — no primary estimator registered". The v1 string is copied verbatim.
4. **X-22 to X-25** are listed in verdict words only, with no body sentence. W1 forbids new numbers, while ruling 2 asks for an estimate sentence for MIXED rows. The two rules conflict for X-22.
5. **A16 registered threshold:** the parts carry no `rule` field. The body says "not detectably", and the prereg text should be checked.
6. The 11-08 CP round must be a full three-judge panel on this draft (CC-129 ruling 8).

**Remaining writer work (no PI input)**
1. ~~Optional cut of about 350 words to reach 11,350.~~ Done in pass 3 (11,348).
2. CAS build and page count: pass 3, 24 pages, 0 overfull (W11 still to be ratified: For CC-140 item 1).
3. Done: Fig. 2 exported to `figs/fig2_slope_by_gold.pdf` (rsvg-convert). Fig. 4 is now in S1 and is still SVG only.
4. Strip the supplement for the "exactly as received" rule on 11-05 (src/CC/PD ids, `.session_backup` paths). Checklist prepared in pass 3.
5. Pass 3: `[dataset]` done at build time (16 keys); OPERA/Less-is-More log entries and `[software]` still open. Original note: the `[dataset]`/`[software]` tags, at build time. Keys: lin2014microsoft, chen2015microsoft, thapliyal2022crossmodal, lam2020uit, plummer2015flickr30k, matsuda2025vela, wadhawan2025vapr, kasai2022transparent, aditya2015images, wada2024polos, gordon2025unblocking, gunjal2024detecting, bui2026uit, pham2024ktvic, huang2024opera (logs), yue2024less (logs). Add a Zenodo entry once the record exists.
6. ~~Fill §6.5 after R2/R3.~~ Pass 3: written without R1–R4 (not executed); see Pass 3.
7. ~~Update `outline.md`'s abstract or the build script.~~ Done (pass 2 CAS build; pass 3 elsarticle build and outline note).
