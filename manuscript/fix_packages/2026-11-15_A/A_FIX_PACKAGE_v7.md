# Paper A fix package v7

Written 2026-11-15T12:10Z (2026-11-15, 19:10 Vietnam time). Target journal of the paper: Signal Processing: Image Communication.

**What this file is.** Proposed changes for the findings of the three full reads of 2026-11-15 and for the items that ruling CC-422 carried (N9, W4) and CC-412 carried (N1). Every finding was checked again in the files at HEAD and, where it names a number, in the source result file, before a change was written. Each text change is an exact OLD/NEW pair with its evidence, or a step of the script that Section 4 describes. Nothing has been applied, staged or committed. The package holds no outcome of Section 6.7 or of Supplementary S11 and quotes nothing from them, from the abstract body or from the highlights.

**Inputs.**
- Reads: `manuscript/reviews/A_FULLREAD_sec2-5_2026-11-15.md` (sha256 `d88b1cb4be8e`, 41 findings), `A_FULLREAD_sec6-11_2026-11-15.md` (`1fa8d1720e6b`, 46 findings), `A_FULLREAD_supp_S1-S10_2026-11-15.md` (`dac9cb4ba0f0`, 46 findings, 3 BLOCKING). Rulings `CC-422.txt` (`72f03975a8ee`) and `CC-412.txt` (`64f9b55c7f84`).
- Paper: `/mnt/d/vsps_papers/vsps-paperA-spic`, HEAD `a7f2b4e`, tree clean. The first two reads give line numbers as at `0b542cf`; `sec2`, `sec3`, `sec4`, `sec7`, `sec8` and `sec10` have the same bytes at `a7f2b4e`, and the lines named in `sec5`, `sec11` and `declarations.md` did not move.
- Decisions LOG `.session_backup/2026-10-13/decisions/LOG.md`, the investigator's lines read before the blocks they bear on: PI-1101o (l.1082), PI-1101p (l.1083), PI-1105m (l.1614), PI-1106a (l.1622), PI-1110n (l.2070), and, for the declarations, PI-1026az, PI-1110o and PI-1115i.
- Registration texts: `manuscript/prereg/2026-10-28_pascal50s/PREREG.md` (`1448ab13fcb5`) §9; `2026-10-30_a_g0/NOTE.md` l.36-46; `2026-10-29_a_companion/RULE.md` l.35, l.104; `2026-11-07_a_m1/A_M1_PLAN_v2.md` l.81, l.280-283; `2026-10-18_g2b_qwen3vl_ladder.md` l.163.
- Result files, each re-read by script (sha256 prefix in the manifest rows of Section 4): `e1_x1pb_verification_v2.json`, `appC_mde.tex`, `xm3600_full_verdict.json`, `h4_r4_full5000_all9.json`, `cf_r4_full5000_all9.json`, `uitviic_paired_diffs.json`, `a_m1_result.json`, `a_n2_run.json`, `p50_decide.json`, `g2b_score_record/precheck.json`, `q2_longcap_arena.json`, `k2_scores.json`, `tier3.json`.
- Not opened: any label folder, key file, label file, `gt_cache.json`, `A_FIX_PACKAGE_v1.md`, `A_CUT_PLAN_v1.md`.
- Held zones. Of `sec7_verbosity_sign.md` only lines before the heading of Section 6.7 were displayed, and of both supplement files only lines before the heading of S11 and the reference list after it. In the six lines outside the zones that the readers list as holding a sentence on the held study, those sentences were masked before display. The abstract body, the highlights and line 13 of the cover letter were not displayed. Scripts read the files whole (to compare bytes and count words) and printed none of that text.

**The groups.**
- **M (main text, 68 blocks).** Sections 2 to 9 outside the held places: contradictions, claims weakened to their labels, undefined terms, pointers, English.
- **T (1 block).** One row of Table 1: supplement BLOCKING 3.
- **G (4 blocks, one of them an alternative that is switched off).** The registered third sentence of Section 6.4: a record of the departure, not a restoration (Section 5).
- **D (2 blocks).** Declarations: the list of third-party sets and one name.
- **S (29 blocks).** Supplementary S1 to S10 and one entry of its reference list. Two new tables in S3 (supplement BLOCKING 1).
- **B (1 block).** One author field of `paperA.bib` (CC-422 N9).
- **Steps.** S1 (129 manifest rows), W4 (the `a_m1` result file into the release results with its PROVENANCE row), S2 (published supplement and provenance table through the scrub step), S3 (length comment).

No statement on AI tools is added and nothing says that no AI tool was used. No agreement clause is touched; the script counts the clauses in every file before and after.

## 1. Counts

- 105 blocks in this file; 104 are applied with the default `SKIP = ("A7-G01a",)`. By file: `supplementary.md` 31, `sec7_verbosity_sign.md` 21, `sec3_measurement_setup.md` 16, `sec5_exchangeability.md` 9, `sec2_related_work.md` 7, `sec8_human_validity.md` 5, `sec4_theory.md` 4, `sec10_discussion.md` 4, `sec11_limitations_ethics.md` 4, `declarations.md` 2, `sec1_introduction.md` 1, `paperA.bib` 1.
- Steps: S1 (129 rows: 9 single rows, 60 rows of Table S3.2, 60 rows of Table S3.3), W4, S2, S3.
- Findings: 133 in the three reads (41 + 46 + 46). Section 6.1 gives the fate of each finding that did not become a block as written.
- The three BLOCKING findings of the supplement read:
  1. **S3 promises.** Both promised items exist in committed files, so they are built, not removed: Table S3.2 (per-comparison values) from `e1_x1pb_verification_v2.json :: pairs_15`, and Table S3.3 (minimum detectable effects) from the committed table file `appC_mde.tex`, which the source comment of the promising sentence itself names. The script recomputes every detectable effect from the intervals and requires it to equal the committed row to two decimals (blocks A7-S08, A7-S09).
  2. **Missing reference entry.** Closed at `a7f2b4e` (CC-422 W5). This package only writes the citation in the list's form and corrects the spelling "Pont-Tuset" (A7-S11, A7-S29, A7-B01).
  3. **Test X-22.** The verdict file gives the token `PASS_DRHO113_MIXED_MCP_CI_INCLUDES_1`. Table S4.0 prints that token in words and is right; Table 1 printed the single word MIXED and is aligned to the words of Table S4.0. The row stays under "Other outcomes" (A7-T01).

## 2. Table of blocks

| Id | Finding | File | What changes (first words of OLD) |
|---|---|---|---|
| A7-M01 | sec2-5 read F01 | `sec2_related_work.md` | presupposes independent raters; Section 5 tests whether caption refere |
| A7-M02 | sec2-5 read F02 | `sec2_related_work.md` | In captioning, completeness acts through verbosity and can set the sig |
| A7-M03 | sec2-5 read F02, F03 | `sec2_related_work.md` | this paper measures gold completeness as a controlled factor that can  |
| A7-M04 | sec2-5 read F05 | `sec2_related_work.md` | Berger et al. (2025) survey caption-evaluation metrics and their valid |
| A7-M05 | sec2-5 read F06 | `sec2_related_work.md` | In text RLHF, length is an established channel |
| A7-M06 | sec2-5 read F08 | `sec2_related_work.md` | UIT-OpenViIC (Bui et al., 2026) is used here only through aggregate st |
| A7-M07 | sec2-5 read F08 | `sec5_exchangeability.md` | a 555-image multi-reference panel with UIT-OpenViIC references |
| A7-M08 | sec2-5 read F09 | `sec2_related_work.md` | \| Crossmodal-3600, PASCAL-50S, COCO; released and own captions (Secti |
| A7-M09 | sec2-5 read F11, F12, F13 | `sec3_measurement_setup.md` | **Gold per set.** The third level, *label gold* (the registrations' *c |
| A7-M10 | sec2-5 read F14, F15 | `sec3_measurement_setup.md` | is the form for which Section 4's closed form is exact (both: Suppleme |
| A7-M11 | sec2-5 read F16 | `sec3_measurement_setup.md` | instance-level CHAIR, which counts repeated mentions; |
| A7-M12 | sec2-5 read F17, F18 | `sec3_measurement_setup.md` | Matchers. English outputs are matched to COCO-80 with the CHAIR synony |
| A7-M13 | sec2-5 read F19 | `sec3_measurement_setup.md` | true positives follow a power law, |
| A7-M14 | sec2-5 read F20 | `sec3_measurement_setup.md` | on the same 9 COCO systems (COCO-5000) it is |
| A7-M15 | sec2-5 read F21 | `sec3_measurement_setup.md` | **matched prefix (protocol primary; post hoc, Supplementary S3):** |
| A7-M16 | sec2-5 read F22, F23 | `sec3_measurement_setup.md` | after Holm correction and a +1.0-point SESOI, 2 remain under each orde |
| A7-M17 | sec2-5 read F22 | `sec3_measurement_setup.md` | Where a protocol fixes a smallest effect size of interest (SESOI; +1.0 |
| A7-M18 | sec2-5 read F24 | `sec3_measurement_setup.md` | but it ran in the leaderboard harness described next, so it calibrates |
| A7-M19 | sec2-5 read supplement read 21 | `sec3_measurement_setup.md` | is the allocation channel (Supplementary S2). |
| A7-M20 | sec2-5 read F27, F28 | `sec3_measurement_setup.md` | 1,000 for the second-backbone family, PASCAL-50S, |
| A7-M21 | sec2-5 read F27, F28 | `sec3_measurement_setup.md` | The adjacent-doubleton shares of Table 5.1 use $B = 1000$. |
| A7-M22 | sec2-5 read F26 | `sec3_measurement_setup.md` | ; the registered tests of Sections 6–7 report uncorrected intervals, a |
| A7-M23 | sec2-5 read F29 | `sec3_measurement_setup.md` | The frontier slope used in Sections 4 and 6 is the ordinary least squa |
| A7-M24 | sec2-5 read F30 | `sec3_measurement_setup.md` | the vertical distance to the pre-registered frontier |
| A7-M25 | sec2-5 read F31 | `sec4_theory.md` | not the claim the registered tests confirm |
| A7-M26 | sec2-5 read F32 | `sec4_theory.md` | share $s_m$ and $F_m$; they need only sit on one frontier. |
| A7-M27 | sec2-5 read F14 | `sec4_theory.md` | so the closed form is applied only to micro-F1 (Supplementary S1) |
| A7-M28 | sec2-5 read F33 | `sec4_theory.md` | on PASCAL-50S neither sign-change location was predicted either (Secti |
| A7-M29 | sec2-5 read F34 | `sec5_exchangeability.md` | COCO and UIT-ViIC, the two caption sets with a documented protocol, si |
| A7-M30 | sec2-5 read F36 | `sec5_exchangeability.md` | \| Corpus \| References \| Images \| Share \| |
| A7-M31 | sec2-5 read F36 | `sec5_exchangeability.md` | \| UIT-OpenViIC full test, exactly 5 refs (aggregates) \| — \| 1,997 \ |
| A7-M32 | sec2-5 read F37 | `sec5_exchangeability.md` | *UIT-OpenViIC rows:* the panel rows use a |
| A7-M33 | sec2-5 read F39 | `sec5_exchangeability.md` | without those that are also in the UIT-ViIC training split. |
| A7-M34 | sec2-5 read F38 | `sec5_exchangeability.md` | the crossing of Section 4 moves to larger $k$ |
| A7-M35 | sec2-5 read F38 | `sec5_exchangeability.md` | $k_{\text{eff}} = 1.99$ [1.967, 2.020] |
| A7-M36 | sec2-5 read F40 | `sec5_exchangeability.md` | 0.866 (95% CI 0.854–0.876) |
| A7-M37 | sec6-11 read F03 | `sec7_verbosity_sign.md` | and the multi-reference sign is not predicted. |
| A7-M38 | sec6-11 read F18 | `sec7_verbosity_sign.md` | (post hoc descriptive, no verdict). The label gold is not nested |
| A7-M39 | sec6-11 read F23 | `sec7_verbosity_sign.md` | as did the OPERA instance-gold prediction (+4.24 [−0.09, +8.51]). |
| A7-M40 | sec6-11 read F22 | `sec7_verbosity_sign.md` | one with the gold-SFT recipe of an earlier study |
| A7-M41 | sec6-11 read F02, F22; supplement read 20 | `sec7_verbosity_sign.md` | The exponent is transferred from COCO-2500, not refitted; the predicti |
| A7-M42 | sec6-11 read F21; supplement read 43 | `sec7_verbosity_sign.md` | It holds for 3 of 4 gold variants in-sample (the all-references gold d |
| A7-M43 | sec6-11 read F19 | `sec7_verbosity_sign.md` | the one-reference non-empty gold size missed its interval (1.8768 agai |
| A7-M44 | sec6-11 read F20 | `sec7_verbosity_sign.md` | (in-sample 0.503 against 0.549) |
| A7-M45 | sec6-11 read F24 | `sec7_verbosity_sign.md` | **PASS** on COCO-295 and UIT-ViIC-231. Language, |
| A7-M46 | sec6-11 read F25 | `sec7_verbosity_sign.md` | (−1.124 [−11.52, 6.62]; point ≤ 0) |
| A7-M47 | sec6-11 read F26 | `sec7_verbosity_sign.md` | (the fixed 8 GPU-hour cap dropped Idefics3-8B) |
| A7-M48 | sec6-11 read F09 | `sec7_verbosity_sign.md` | Counted after the result without model outputs: On all 1,000 PASCAL-50 |
| A7-M49 | sec6-11 read F09 | `sec7_verbosity_sign.md` | against 2 × 1,039.6; Section 6.6), so the comparison is approximate; p |
| A7-M50 | sec6-11 read F27 | `sec7_verbosity_sign.md` | after a pre-specified filter and 6 unclean drops; |
| A7-M51 | sec6-11 read F04, F05, F28 | `sec7_verbosity_sign.md` | Post hoc, we refitted every cell of Table 6.1 with each system left ou |
| A7-M52 | sec6-11 read F28 | `sec7_verbosity_sign.md` | On the second backbone the one-reference sign is stable (−12.52 to −11 |
| A7-M53 | sec6-11 read F11 | `sec7_verbosity_sign.md` | (the union of the classes named in all 50 references) |
| A7-M54 | sec6-11 read F29 | `sec7_verbosity_sign.md` | nested reference golds are ordered even if objects are missing complet |
| A7-M55 | sec6-11 read F10 | `sec7_verbosity_sign.md` | and X4, in the Holm family by its tier-1 power rule, passed |
| A7-M56 | sec6-11 read F30 | `sec8_human_validity.md` | among same-image caption pairs where both differ; |
| A7-M57 | sec6-11 read F31 | `sec8_human_validity.md` | Relevance falls by 0.024 per additional COCO class [−0.029, −0.020] |
| A7-M58 | sec6-11 read F32 | `sec8_human_validity.md` | the second part is a **FAIL** under the registered rule "point ≤ 0" wh |
| A7-M59 | sec6-11 read F33 | `sec8_human_validity.md` | RLAIF-V's (Yu et al., 2025) chosen-fewer share was predicted |
| A7-M60 | sec6-11 read F33; supplement read 22 | `sec8_human_validity.md` | inside the kill interval [0.45, 0.55]; |
| A7-M61 | sec6-11 read F08 | `sec10_discussion.md` | the label step, a change of completeness plus precision rule (Table 6. |
| A7-M62 | sec6-11 read F34 | `sec10_discussion.md` | and FAIL on PASCAL-50S (Section 6.4). There the registration assumed |
| A7-M63 | sec6-11 read F12 | `sec10_discussion.md` | found 1,787 VOC label instances against 2,162 classes named in the 50  |
| A7-M64 | sec6-11 read F35 | `sec10_discussion.md` | one-reference gold fell below a size-matched |
| A7-M65 | sec6-11 read F36 | `sec11_limitations_ethics.md` | and the UIT-ViIC pass is not counted. |
| A7-M66 | sec6-11 read F11 | `sec11_limitations_ethics.md` | a consensus-gold sensitivity (classes named by at least two references |
| A7-M67 | sec6-11 read F40 | `sec11_limitations_ethics.md` | **PASCAL-50S outputs.** Under the registered data rule, |
| A7-M68 | sec6-11 read F41 | `sec11_limitations_ethics.md` | we do not aim to discredit specific methods, report the full specifica |
| A7-T01 | supplement read 3 (BLOCKING); sec6-11 read note 8 | `sec1_introduction.md` | MIXED: condensed F1 (A12) and a two-panel transfer with no registered  |
| A7-G01a | sec6-11 read F01 (alternative that quotes the sentence; NOT applied by default) | `supplementary.md` | **Scope of the confirmatory evidence.** The registered evidence on the |
| A7-G01b | sec6-11 read F01 (default) | `supplementary.md` | **Scope of the confirmatory evidence.** The registered evidence on the |
| A7-G02 | sec6-11 read F01 | `sec7_verbosity_sign.md` | Two departures from the registration are disclosed in Section 9.2; nei |
| A7-G03 | sec6-11 read F01; CC-412 N1 | `sec7_verbosity_sign.md` | §9.1's "for the reference ladder only" does not apply (label rung kept |
| A7-D01 | sec6-11 read F15 | `declarations.md` | and the KTVIC reference captions are not redistributed either; all are |
| A7-D02 | sec6-11 read F43 | `declarations.md` | this paper's 600 Crossmodal-3600 images |
| A7-S01 | supplement read 15 | `supplementary.md` | (Karlin, 1968, *Total Positivity*, Vol. I; we did not check the sectio |
| A7-S02 | supplement read 15 | `supplementary.md` | Lipton et al. theorem numbering checked against arXiv 1402.1892v2 (The |
| A7-S03 | supplement read 15 | `supplementary.md` | (bibliographic data verified via Crossref; we did not check where in t |
| A7-S04 | supplement read 32 | `supplementary.md` | e.g. 0.425 vs 0.478 on COCO with one reference |
| A7-S05 | sec2-5 read F17 | `supplementary.md` | All matcher versions are pinned by file hash, and every table names th |
| A7-S06 | supplement read 31 | `supplementary.md` | falls from 0.88 to 0.68 (Supplementary S1)(comment) src: sensitivity.json |
| A7-S07 | supplement read 36 | `supplementary.md` | applies the controls of Section 3.3(b) to methods |
| A7-S08 | supplement read 1 (BLOCKING) | `supplementary.md` | #### Training-based methods: a registered leaderboard (not scored) |
| A7-S09 | supplement read 1 (BLOCKING) | `supplementary.md` | and Supplementary S3 gives the minimum detectable effect for each comp |
| A7-S10 | supplement read 22; sec6-11 read note 8 | `supplementary.md` | registered (in the Holm family by its tier-1 power rule; one test look |
| A7-S11 | supplement read 2; CC-422 N9 | `supplementary.md` | XM3600 (Thapliyal et al., EMNLP 2022)(comment) cite: thapliyal2022crossmoda |
| A7-S12 | supplement read 38 | `supplementary.md` | were added, each run only after a licence check and a committed pre-re |
| A7-S13 | supplement read 11 | `supplementary.md` | ## S5 Exchangeability: all corpus and split rows |
| A7-S14 | supplement read 11 | `supplementary.md` | With several dozen corpus–split rows in the audit (Supplementary S5),  |
| A7-S15 | supplement read 37 | `supplementary.md` | their registered verdicts are listed in Table 1 (rows X-22 to X-25). |
| A7-S16 | supplement read 39 | `supplementary.md` | give within-writer bounds at best on such data; we report none. For CO |
| A7-S17 | supplement read 39 | `supplementary.md` | Rater-equivalence units (Resnick et al.) are defined |
| A7-S18 | supplement read 24 | `supplementary.md` | \| Check against labels, D_L = (L − Ŝ^L)/L \| |
| A7-S19 | supplement read 40 | `supplementary.md` | is not supported at the registered tolerance; |
| A7-S20 | supplement read 10 | `supplementary.md` | ## S6 Numbers manifest, exploratory lexicon and data audits |
| A7-S21 | supplement read 10 | `supplementary.md` | and supports no claim in this paper (Supplementary S6 lists it with th |
| A7-S22 | supplement read 10 | `supplementary.md` | A larger noun vocabulary, tried post hoc, supports no claim (Supplemen |
| A7-S23 | supplement read 25 | `supplementary.md` | \| Mean $\Delta k$ \| Same, pairs with $\lvert\Delta\text{words}\rvert |
| A7-S24 | supplement read 22 | `supplementary.md` | inside the kill interval, so the prediction failed and the first half  |
| A7-S25 | supplement read 19 | `supplementary.md` | detailed captions (post hoc; Sections 6.3 and 8.5).** |
| A7-S26 | supplement read 41 | `supplementary.md` | **Within one prompt and zero-shot only.** |
| A7-S27 | supplement read 42 | `supplementary.md` | Totals: 1,787 label instances against 2,162 reference classes (ratio 0 |
| A7-S28 | supplement read 22 | `supplementary.md` | inside the kill interval [0.45, 0.55]; |
| A7-S29 | CC-422 N9 | `supplementary.md` | Jordi Pont Tuset, Xi Chen, and Radu Soricut. 2022. |
| A7-B01 | CC-422 N9 | `paperA.bib` | author = {Thapliyal, Ashish V. and Pont Tuset, Jordi and Chen, Xi and  |


## 3. Blocks

Format: the text between the OLD marker and the NEW marker occurs exactly once in the file at HEAD; the text between the NEW marker and the EVIDENCE marker replaces it. Line numbers in the evidence are those of the files at HEAD; "published supplement" is `supplementary_SPIC.md`.

**A7-M01** (sec2-5 read F01)

<<<A7-M01 sec2_related_work.md OLD>>>
presupposes independent raters; Section 5 tests whether caption references are.
<<<A7-M01 sec2_related_work.md NEW>>>
presupposes independent raters. Section 5 checks a weaker condition, whether the order of an image's references is exchangeable; it does not test whether the writers are independent.
<<<A7-M01 EVIDENCE>>>
sec4_theory.md l.11 ("the diagnostic does not test writer independence") and sec5_exchangeability.md l.31 ("diagnoses whether reference order is exchangeable, not whether writers are independent").

**A7-M02** (sec2-5 read F02)

<<<A7-M02 sec2_related_work.md OLD>>>
In captioning, completeness acts through verbosity and can set the sign of F1's verbosity slope, not only the size of a bias.
<<<A7-M02 sec2_related_work.md NEW>>>
In captioning, the gold acts through verbosity: F1's verbosity slope is ordered across golds (registered; Section 6.2), and in exploratory rows its sign changes with the gold (Section 6.1).
<<<A7-M02 EVIDENCE>>>
The registered claim is the ordering (sec7 l.5). The sign change between golds is exploratory (Table 6.1 row COCO-5000, sec7 l.39); the registered all-references sign on XM3600 is FAIL (sec7 l.49). Weakened to the labels.

**A7-M03** (sec2-5 read F02, F03)

<<<A7-M03 sec2_related_work.md OLD>>>
this paper measures gold completeness as a controlled factor that can set the sign of F1's verbosity slope, and applies a size-matched random-deletion null, in the manner of tests of the selected-completely-at-random assumption (Molotkov and Artomov, 2023; Teisseyre et al., 2024), to quantify that reporting bias on PASCAL-50S and COCO val2017 (Sections 6.4 and 6.6).
<<<A7-M03 sec2_related_work.md NEW>>>
this paper treats the gold as a controlled factor, tests the ordering of F1's verbosity slope across golds (registered), reports sign changes with the gold as exploratory, and applies a size-matched random-deletion null, in the manner of tests of the selected-completely-at-random assumption (Molotkov and Artomov, 2023; Teisseyre et al., 2024), to test, in a nested form, whether one-reference gold departs from uniform deletion on PASCAL-50S and COCO val2017 (Sections 6.4 and 6.6); the result is consistent with selective naming and does not measure its size.
<<<A7-M03 EVIDENCE>>>
Caption of Table 6.3 ("The p-value refers to the registered nested null only ... neither evidence against random omission by individual references nor a size guarantee") and sec7 l.122 ("consistent with ... not proof of cause"). "Quantify that reporting bias" was stronger than both.

**A7-M04** (sec2-5 read F05)

<<<A7-M04 sec2_related_work.md OLD>>>
Berger et al. (2025) survey caption-evaluation metrics and their validity.
<<<A7-M04 sec2_related_work.md NEW>>>
Berger et al. (2025) survey caption-evaluation metrics.
<<<A7-M04 EVIDENCE>>>
paperA.bib key berger2025surveying, title "Surveying the Landscape of Image Captioning Evaluation: A Comprehensive Taxonomy, Trends, and Metrics Analysis"; intext_trace_A.tsv has the row as NOT_SAMPLED. No recorded passage supports "and their validity".

**A7-M05** (sec2-5 read F06)

<<<A7-M05 sec2_related_work.md OLD>>>
In text RLHF, length is an established channel
<<<A7-M05 sec2_related_work.md NEW>>>
In reinforcement learning from human feedback (RLHF) on text, length is an established channel
<<<A7-M05 EVIDENCE>>>
The abbreviation is expanded in no main-text file (0 hits for the expansion in sec*.md).

**A7-M06** (sec2-5 read F08)

<<<A7-M06 sec2_related_work.md OLD>>>
 UIT-OpenViIC (Bui et al., 2026) is used here only through aggregate statistics (Section 9.2).<!-- cite (moved from the text): UIT-ViIC
<<<A7-M06 sec2_related_work.md NEW>>>
<!-- cite (moved from the text): UIT-ViIC
<<<A7-M06 EVIDENCE>>>
The sentence stands under "Reporting conventions" and repeats sec5 l.27 ("Only aggregates are reported (Section 9.2)"). It holds the only main-text citation of Bui et al. (2026), so block A7-M07 moves the citation to Section 5.2.

**A7-M07** (sec2-5 read F08)

<<<A7-M07 sec5_exchangeability.md OLD>>>
a 555-image multi-reference panel with UIT-OpenViIC references
<<<A7-M07 sec5_exchangeability.md NEW>>>
a 555-image multi-reference panel with UIT-OpenViIC (Bui et al., 2026) references
<<<A7-M07 EVIDENCE>>>
Keeps the citation that A7-M06 removes from Section 2 (key bui2026uit resolves by author and year in the build; checked in the scratch build: no undefined citation).

**A7-M08** (sec2-5 read F09)

<<<A7-M08 sec2_related_work.md OLD>>>
| Crossmodal-3600, PASCAL-50S, COCO; released and own captions (Section 3) |
<<<A7-M08 sec2_related_work.md NEW>>>
| Crossmodal-3600, PASCAL-50S, COCO and others; released captions and captions decoded for this study (Sections 3 and 6) |
<<<A7-M08 EVIDENCE>>>
Data and systems are described in Section 6 (sec7 l.43, l.62, l.77, l.96); UIT-ViIC and the human-judgment sets are also used.

**A7-M09** (sec2-5 read F11, F12, F13)

<<<A7-M09 sec3_measurement_setup.md OLD>>>
**Gold per set.** The third level, *label gold* (the registrations' *complete gold*), is instance gold on COCO-5000, the English LVLM families, UIT-ViIC test (*UIT-ViIC-231*) and the 295 COCO-2500 val2017 images of Section 6.3 (*COCO-295*). On the 600 XM3600 evaluation images (*XM3600-600*; Section 6.2) it is human-verified OIV7 labels,
<<<A7-M09 sec3_measurement_setup.md NEW>>>
**Gold per set.** The paper compares golds at three levels: one reference, all references, and a *label gold* (the registrations' *complete gold*). The label gold is instance gold on COCO-5000 (the 5,000 images of the COCO Karpathy test split; COCO-2500 is its seed-42 half), the two English LVLM release families of Section 3.3, UIT-ViIC test (*UIT-ViIC-231*) and the 295 COCO val2017 images drawn from COCO-2500 (Section 6.3; *COCO-295*). On the 600 XM3600 evaluation images (*XM3600-600*; Section 6.2) it is human-verified Open Images V7 (OIV7) labels,
<<<A7-M09 EVIDENCE>>>
No levels are introduced before l.13, and the list above it ends with "Instance + references". COCO-5000: sec5 l.27 ("the 5,000 Karpathy-test images"); COCO-2500: published supplement l.730 ("COCO-2500, the seed-42 half of COCO-5000"); COCO-295: sec7 l.62 ("295 COCO val2017 images from the COCO-2500 discovery set"); OIV7: sec7 l.43.

**A7-M10** (sec2-5 read F14, F15)

<<<A7-M10 sec3_measurement_setup.md OLD>>>
is the form for which Section 4's closed form is exact (both: Supplementary S1).
<<<A7-M10 sec3_measurement_setup.md NEW>>>
is the form for which the sign condition of Proposition 1(c) is exact (derivations for mixed F1 and micro-F1: Supplementary S1).
<<<A7-M10 EVIDENCE>>>
Section 4 states a sign condition (Proposition 1(c)); the closed form is in Supplementary S1 (published l.34, l.36).

**A7-M11** (sec2-5 read F16)

<<<A7-M11 sec3_measurement_setup.md OLD>>>
instance-level CHAIR, which counts repeated mentions;
<<<A7-M11 sec3_measurement_setup.md NEW>>>
instance-level CHAIR, which counts repeated mentions (the subscript is part of the name, not the image index);
<<<A7-M11 EVIDENCE>>>
$i$ is the image index in the same sentence.

**A7-M12** (sec2-5 read F17, F18)

<<<A7-M12 sec3_measurement_setup.md OLD>>>
Matchers. English outputs are matched to COCO-80 with the CHAIR synonym list; Vietnamese outputs use a tone-normalized lexicon (Supplementary S2). Every table names its matcher. Each caption
<<<A7-M12 sec3_measurement_setup.md NEW>>>
**Matchers.** English outputs are matched to COCO-80 with the CHAIR synonym list; Vietnamese outputs are matched with a tone-normalized matcher, under the COCO-80 lexicon or the Vietnamese reference lexicon (Table 6.1; Supplementary S2). Each caption
<<<A7-M12 EVIDENCE>>>
Tables 5.1, 6.2 and 6.3 name no matcher, so "Every table names its matcher" is false and is removed (not replaced by a new claim). The two Vietnamese lexicons are the row labels of Table 6.1. The other run-in heads of Section 3 are bold.

**A7-M13** (sec2-5 read F19)

<<<A7-M13 sec3_measurement_setup.md OLD>>>
true positives follow a power law,
<<<A7-M13 sec3_measurement_setup.md NEW>>>
we model true positives by a power law,
<<<A7-M13 EVIDENCE>>>
The supplement treats the power law as a model (published l.36 fit error; l.730 "a goodness-of-fit check"). No pointer is added, because no place reports a fit of the power law itself.

**A7-M14** (sec2-5 read F20)

<<<A7-M14 sec3_measurement_setup.md OLD>>>
on the same 9 COCO systems (COCO-5000) it is
<<<A7-M14 sec3_measurement_setup.md NEW>>>
on the 9 systems of COCO-5000 (Section 6.1) it is
<<<A7-M14 EVIDENCE>>>
No systems are named before l.26.

**A7-M15** (sec2-5 read F21)

<<<A7-M15 sec3_measurement_setup.md OLD>>>
**matched prefix (protocol primary; post hoc, Supplementary S3):**
<<<A7-M15 sec3_measurement_setup.md NEW>>>
**matched prefix (the primary control of the re-scoring protocol; post hoc, Supplementary S3):**
<<<A7-M15 EVIDENCE>>>
"protocol primary" is shorthand; sec3 l.40 and published supplement l.210 give the protocol as post hoc.

**A7-M16** (sec2-5 read F22, F23)

<<<A7-M16 sec3_measurement_setup.md OLD>>>
after Holm correction and a +1.0-point SESOI, 2 remain under each order-preserving control (mean gain +0.62 and +0.65 points, against +3.41 raw) and 6 under the uniform random subset (mean +2.76).
<<<A7-M16 sec3_measurement_setup.md NEW>>>
after Holm correction and a +1.0-point smallest effect size of interest (SESOI), 2 remain under each order-preserving control and 6 under the uniform random subset. Over all 15 comparisons the mean gain is +0.62 and +0.65 points under the two order-preserving controls and +2.76 under the random subset, against +3.41 raw.
<<<A7-M16 EVIDENCE>>>
.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json (184f9ccac1b9) :: overview_15_pairs.mean_dP_raw = 3.407, mean_dP_MCP_prefix = 0.621, mean_dP_MCP_sent_tieavg = 0.652, mean_dP_MCP_rand_exact = 2.764: means over all 15, re-read; they also equal the column means of the new Table S3.2 (script assertion). No number changes.

**A7-M17** (sec2-5 read F22)

<<<A7-M17 sec3_measurement_setup.md OLD>>>
Where a protocol fixes a smallest effect size of interest (SESOI; +1.0 precision points for the 15 published comparisons)
<<<A7-M17 sec3_measurement_setup.md NEW>>>
Where a protocol fixes a SESOI (+1.0 precision points for the 15 published comparisons)
<<<A7-M17 EVIDENCE>>>
The term is now expanded at its first use (A7-M16).

**A7-M18** (sec2-5 read F24)

<<<A7-M18 sec3_measurement_setup.md OLD>>>
but it ran in the leaderboard harness described next, so it calibrates the paired control only.
<<<A7-M18 sec3_measurement_setup.md NEW>>>
but it ran in the leaderboard decode harness that failed the fidelity check described next, so it calibrates the paired control only.
<<<A7-M18 EVIDENCE>>>
sec11 l.36 ("the seed placebo ran in the harness that failed its fidelity check"); published supplement l.244.

**A7-M19** (sec2-5 read supplement read 21)

<<<A7-M19 sec3_measurement_setup.md OLD>>>
is the allocation channel (Supplementary S2).
<<<A7-M19 sec3_measurement_setup.md NEW>>>
is the allocation channel (Supplementary S1).
<<<A7-M19 EVIDENCE>>>
The allocation term $B$ is defined in Supplementary S1 (published l.9-11); S2 does not treat corpus-total matching.

**A7-M20** (sec2-5 read F27, F28)

<<<A7-M20 sec3_measurement_setup.md OLD>>>
1,000 for the second-backbone family, PASCAL-50S,
<<<A7-M20 sec3_measurement_setup.md NEW>>>
1,000 for the second-backbone family, the eight-LVLM test, PASCAL-50S,
<<<A7-M20 EVIDENCE>>>
data/results/a_n2/a_n2_run.json (1f6ce422e016) :: config.n_boot = 1000, re-read; manifest row added (Section 3 of this file).

**A7-M21** (sec2-5 read F27, F28)

<<<A7-M21 sec3_measurement_setup.md OLD>>>
The adjacent-doubleton shares of Table 5.1 use $B = 1000$.
<<<A7-M21 sec3_measurement_setup.md NEW>>>
The adjacent-doubleton shares of Table 5.1 use 1,000 draws, and the bound of Section 5.4 uses 2,000.
<<<A7-M21 EVIDENCE>>>
Table 5.1: manifest rows 3944-3945 (adjacency_check.py l.43 B=1000; c3_n2 script B_BOOT = 1000). Section 5.4: manifest row 3981, data/results/a_m1/a_m1_result.json (5687a66b2078) :: sets.coco5000.B = 2000, re-read.

**A7-M22** (sec2-5 read F26)

<<<A7-M22 sec3_measurement_setup.md OLD>>>
; the registered tests of Sections 6–7 report uncorrected intervals, as registered.
<<<A7-M22 sec3_measurement_setup.md NEW>>>
; the other registered tests of Sections 6–7 report uncorrected intervals, as registered.
<<<A7-M22 EVIDENCE>>>
The same sentence names two registered families of Section 6 that use Holm.

**A7-M23** (sec2-5 read F29)

<<<A7-M23 sec3_measurement_setup.md OLD>>>
The frontier slope used in Sections 4 and 6 is the ordinary least squares slope of $F_1$ (in points) on $\ln M$ across the systems of a family, with an image-bootstrap interval; it is conditional on the systems. We call it the **verbosity slope**: it is signed, and under reference gold it is mostly negative, so it measures a reward or a penalty for naming more objects.
<<<A7-M23 sec3_measurement_setup.md NEW>>>
The slope reported in Section 6 and analysed in Section 4 is the ordinary least squares slope of $F_1$ (in points) on $\ln M$ across the systems of a family, with an image-bootstrap interval; it is conditional on the systems. We call it the **verbosity slope**. It is signed: a positive value is a reward and a negative value a penalty for naming more objects; under reference gold it is mostly negative.
<<<A7-M23 EVIDENCE>>>
"frontier slope" occurs only here; "so" did not follow. No number.

**A7-M24** (sec2-5 read F30)

<<<A7-M24 sec3_measurement_setup.md OLD>>>
the vertical distance to the pre-registered frontier
<<<A7-M24 sec3_measurement_setup.md NEW>>>
the vertical distance to the pre-declared frontier
<<<A7-M24 EVIDENCE>>>
"registered" has a defined meaning (sec3 l.54) and the proposal is untested (heading of Section 3.7).

**A7-M25** (sec2-5 read F31)

<<<A7-M25 sec4_theory.md OLD>>>
not the claim the registered tests confirm
<<<A7-M25 sec4_theory.md NEW>>>
not the claim that the registered tests address
<<<A7-M25 EVIDENCE>>>
Several registered tests failed (Table 1).

**A7-M26** (sec2-5 read F32)

<<<A7-M26 sec4_theory.md OLD>>>
share $s_m$ and $F_m$; they need only sit on one frontier.
<<<A7-M26 sec4_theory.md NEW>>>
share $s_m$ and $F_m$: they lie on one frontier and differ only in $M$.
<<<A7-M26 EVIDENCE>>>
English only.

**A7-M27** (sec2-5 read F14)

<<<A7-M27 sec4_theory.md OLD>>>
so the closed form is applied only to micro-F1 (Supplementary S1)
<<<A7-M27 sec4_theory.md NEW>>>
so condition (c) is applied only to micro-F1 (Supplementary S1)
<<<A7-M27 EVIDENCE>>>
As A7-M10.

**A7-M28** (sec2-5 read F33)

<<<A7-M28 sec4_theory.md OLD>>>
on PASCAL-50S neither sign-change location was predicted either (Section 6).
<<<A7-M28 sec4_theory.md NEW>>>
on PASCAL-50S the slope signs were not predicted (Sections 6.1, 6.2 and 6.4).
<<<A7-M28 EVIDENCE>>>
sec7 l.88 ("The slope signs were not predicted"). The three section numbers are those of the facts in the sentence.

**A7-M29** (sec2-5 read F34)

<<<A7-M29 sec5_exchangeability.md OLD>>>
COCO and UIT-ViIC, the two caption sets with a documented protocol, sit at the null, with no positive lag-1 excess; for UIT-ViIC, Lam et al. (2020)
<<<A7-M29 sec5_exchangeability.md NEW>>>
COCO and UIT-ViIC sit at the null, with no positive lag-1 excess. COCO's writers are independent; for UIT-ViIC, Lam et al. (2020)
<<<A7-M29 EVIDENCE>>>
Table 5.1 gives Flickr30k as "independent" too, and UIT-ViIC as "assignment per image not stated", so "the two caption sets with a documented protocol" contradicted the table.

**A7-M30** (sec2-5 read F36)

<<<A7-M30 sec5_exchangeability.md OLD>>>
| Corpus | References | Images | Share |
<<<A7-M30 sec5_exchangeability.md NEW>>>
| Corpus | Writers of an image's references | Images | Share |
<<<A7-M30 EVIDENCE>>>
The column holds who wrote the references.

**A7-M31** (sec2-5 read F36)

<<<A7-M31 sec5_exchangeability.md OLD>>>
| UIT-OpenViIC full test, exactly 5 refs (aggregates) | — | 1,997 |
<<<A7-M31 sec5_exchangeability.md NEW>>>
| UIT-OpenViIC full test, exactly 5 refs (aggregates) | not documented | 1,997 |
<<<A7-M31 EVIDENCE>>>
sec5 l.31: "its caption-entry protocol is not documented"; the panel row already says "not documented".

**A7-M32** (sec2-5 read F37)

<<<A7-M32 sec5_exchangeability.md OLD>>>
*UIT-OpenViIC rows:* the panel rows use a
<<<A7-M32 sec5_exchangeability.md NEW>>>
*UIT-OpenViIC rows:* the panel row uses a
<<<A7-M32 EVIDENCE>>>
Table 5.1 has one panel row.

**A7-M33** (sec2-5 read F39)

<<<A7-M33 sec5_exchangeability.md OLD>>>
without those that are also in the UIT-ViIC training split.
<<<A7-M33 sec5_exchangeability.md NEW>>>
without those that are also in the UIT-ViIC training split; Sections 5.3 and 5.4 use all 5,000 images.
<<<A7-M33 EVIDENCE>>>
Section 5.3: source comment of l.37 ("r4 = 9 systems x 5,000"). Section 5.4: data/results/a_m1/a_m1_result.json (5687a66b2078) :: sets.coco5000.n = 5000, re-read.

**A7-M34** (sec2-5 read F38)

<<<A7-M34 sec5_exchangeability.md OLD>>>
the crossing of Section 4 moves to larger $k$
<<<A7-M34 sec5_exchangeability.md NEW>>>
the sign change of Section 4.2 moves to larger $k$
<<<A7-M34 EVIDENCE>>>
Section 4.2 speaks of a sign change.

**A7-M35** (sec2-5 read F38)

<<<A7-M35 sec5_exchangeability.md OLD>>>
$k_{\text{eff}} = 1.99$ [1.967, 2.020]
<<<A7-M35 sec5_exchangeability.md NEW>>>
$k_{\text{eff}} = 1.99$ [1.97, 2.02]
<<<A7-M35 EVIDENCE>>>
.session_backup/2026-10-26/a_full5000/out/h4_r4_full5000_all9.json (39c97d0de681) :: T3.k_eff_adjacent_pair_slots2to5 = {point 1.993, ci [1.967, 2.02]}, re-read; point and interval now at the same precision; manifest row added.

**A7-M36** (sec2-5 read F40)

<<<A7-M36 sec5_exchangeability.md OLD>>>
0.866 (95% CI 0.854–0.876)
<<<A7-M36 sec5_exchangeability.md NEW>>>
0.866 [0.854, 0.876]
<<<A7-M36 EVIDENCE>>>
Interval form of the rest of Sections 3 to 6. The sentence is not the held last sentence of l.43.

**A7-M37** (sec6-11 read F03)

<<<A7-M37 sec7_verbosity_sign.md OLD>>>
and the multi-reference sign is not predicted.
<<<A7-M37 sec7_verbosity_sign.md NEW>>>
and the multi-reference sign is not predicted by the theory; it was registered as positive on XM3600 and failed (Section 6.2).
<<<A7-M37 EVIDENCE>>>
sec7 l.49 ("All-references slope > 0: FAIL"); sec4 l.25 ("was predicted positive and failed").

**A7-M38** (sec6-11 read F18)

<<<A7-M38 sec7_verbosity_sign.md OLD>>>
(post hoc descriptive, no verdict). The label gold is not nested
<<<A7-M38 sec7_verbosity_sign.md NEW>>>
(post hoc descriptive, no verdict; the two COCO val2017 ratios are the premise values of the registered test of Section 6.4). The label gold is not nested
<<<A7-M38 EVIDENCE>>>
Source comment of the caption: COCO val2017 = tier3.json analysis.premise.{L_over_R1, L_over_R5}; sec7 l.96 prints 2.149 and "premise not met" as registered.

**A7-M39** (sec6-11 read F23)

<<<A7-M39 sec7_verbosity_sign.md OLD>>>
as did the OPERA instance-gold prediction (+4.24 [−0.09, +8.51]).
<<<A7-M39 sec7_verbosity_sign.md NEW>>>
as did the OPERA instance-gold prediction (+4.24 [−0.09, +8.51]; the pre-specified rule required an interval above 0).
<<<A7-M39 EVIDENCE>>>
Published supplement l.589: "P3 (instance gold, slope > 0 with interval above 0)".

**A7-M40** (sec6-11 read F22)

<<<A7-M40 sec7_verbosity_sign.md OLD>>>
one with the gold-SFT recipe of an earlier study
<<<A7-M40 sec7_verbosity_sign.md NEW>>>
one with the fine-tuning recipe of an earlier study
<<<A7-M40 EVIDENCE>>>
"gold-SFT" is defined nowhere in the main text.

**A7-M41** (sec6-11 read F02, F22; supplement read 20)

<<<A7-M41 sec7_verbosity_sign.md OLD>>>
The exponent is transferred from COCO-2500, not refitted; the predictions and code were committed before the first output (times: Supplementary S10).
<<<A7-M41 sec7_verbosity_sign.md NEW>>>
The exponent $b$ of the frontier (Section 3.2) is transferred from COCO-2500, not refitted; the predictions and code were committed before the first output (times: Supplementary S4).
<<<A7-M41 EVIDENCE>>>
The commit and first-output times (16:38Z, 17:00Z) are in S4 (published l.332, l.350, l.405); S10 prints none. $b$ is defined in Section 3.2 (the read named 3.7; 3.2 holds the definition).

**A7-M42** (sec6-11 read F21; supplement read 43)

<<<A7-M42 sec7_verbosity_sign.md OLD>>>
It holds for 3 of 4 gold variants in-sample (the all-references gold disagrees:
<<<A7-M42 sec7_verbosity_sign.md NEW>>>
It holds for 3 of 4 gold variants in-sample (the variants are the first reference, one random reference, all references and OIV7; the all-references gold disagrees:
<<<A7-M42 EVIDENCE>>>
.session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json (0b2b3aa5e1a3) :: prereg_comparisons[20].prereg_interval_or_threshold names {refs1_firstk, refs1_randk, refs_all, oiv7_verified}; re-read. The bold registered label and its verdict token are not touched.

**A7-M43** (sec6-11 read F19)

<<<A7-M43 sec7_verbosity_sign.md OLD>>>
the one-reference non-empty gold size missed its interval (1.8768 against 1.8831; OUT; Supplementary S7)
<<<A7-M43 sec7_verbosity_sign.md NEW>>>
the mean one-reference gold size over images with a non-empty gold was 1.8768 against a registered 1.8831 (OUT; Supplementary S7)
<<<A7-M43 EVIDENCE>>>
Manifest rows 223-225 (prereg_comparisons.6: threshold 1.8831, observed 1.8768, OUT). The token OUT is kept.

**A7-M44** (sec6-11 read F20)

<<<A7-M44 sec7_verbosity_sign.md OLD>>>
(in-sample 0.503 against 0.549)
<<<A7-M44 sec7_verbosity_sign.md NEW>>>
(in-sample exponent 0.503 against the transferred 0.549)
<<<A7-M44 EVIDENCE>>>
Manifest rows 239 (b_in_sample, refs_all) and 494 (transferred b, two references). This sentence of l.57 is not the held one.

**A7-M45** (sec6-11 read F24)

<<<A7-M45 sec7_verbosity_sign.md OLD>>>
**PASS** on COCO-295 and UIT-ViIC-231. Language,
<<<A7-M45 sec7_verbosity_sign.md NEW>>>
**PASS** on COCO-295 and UIT-ViIC-231 (not registered on XM3600-600). Language,
<<<A7-M45 EVIDENCE>>>
Table S7.5 (published l.756): the G2B-O2 cells of XM3600-600 read "not registered".

**A7-M46** (sec6-11 read F25)

<<<A7-M46 sec7_verbosity_sign.md OLD>>>
(−1.124 [−11.52, 6.62]; point ≤ 0)
<<<A7-M46 sec7_verbosity_sign.md NEW>>>
(−1.124 [−11.52, +6.62]; point ≤ 0)
<<<A7-M46 EVIDENCE>>>
Manifest row 625: "-1.124 [-11.52, +6.62]".

**A7-M47** (sec6-11 read F26)

<<<A7-M47 sec7_verbosity_sign.md OLD>>>
(the fixed 8 GPU-hour cap dropped Idefics3-8B)
<<<A7-M47 sec7_verbosity_sign.md NEW>>>
(Idefics3-8B was dropped under the fixed cap of 8 GPU-hours)
<<<A7-M47 EVIDENCE>>>
English only.

**A7-M48** (sec6-11 read F09)

<<<A7-M48 sec7_verbosity_sign.md OLD>>>
Counted after the result without model outputs: On all 1,000 PASCAL-50S images,
<<<A7-M48 sec7_verbosity_sign.md NEW>>>
The count was made after the result, without model outputs. By the convention of the X5 evaluability rule (Section 6.6), a gold counts as substantially more complete only if its size is at least twice that of the gold it is compared with (the 2× convention). The next two sentences were fixed before the count; in them a "rung" is a gold level and "class instances" are image–class pairs. On all 1,000 PASCAL-50S images,
<<<A7-M48 EVIDENCE>>>
manuscript/prereg/2026-10-30_a_g0/NOTE.md l.43-46 ("The convention used by the P50 companion X5 gate ...: a gold counts as substantially more complete only if its size is at least twice that of the gold it is compared with"); published supplement l.774 ("The outcome sentence was fixed before the count"). The two fixed sentences stay word for word. This also gives sec7 l.57 its referent ("the 2× size convention of Section 6.4").

**A7-M49** (sec6-11 read F09)

<<<A7-M49 sec7_verbosity_sign.md OLD>>>
against 2 × 1,039.6; Section 6.6), so the comparison is approximate; per-class rows
<<<A7-M49 sec7_verbosity_sign.md NEW>>>
against 2 × 1,039.6; Section 6.6); that set cannot be rebuilt, so the comparison of 1,782 with the 1,787 of all 1,000 images is approximate; per-class rows
<<<A7-M49 EVIDENCE>>>
Published supplement l.774: "the analysis set cannot be rebuilt, so the comparison of 1,782 with 1,787 is approximate". The old "so" had no reason before it.

**A7-M50** (sec6-11 read F27)

<<<A7-M50 sec7_verbosity_sign.md OLD>>>
after a pre-specified filter and 6 unclean drops;
<<<A7-M50 sec7_verbosity_sign.md NEW>>>
after a pre-specified filter and 6 images dropped as unclean;
<<<A7-M50 EVIDENCE>>>
Manifest row 1327: tier3.json analysis.n_dropped_unclean = 6 (re-read). The clause is the opening clause, which the paragraph itself says differs from the registered wording.

**A7-M51** (sec6-11 read F04, F05, F28)

<<<A7-M51 sec7_verbosity_sign.md OLD>>>
Post hoc, we refitted every cell of Table 6.1 with each system left out in turn (system jackknife; Supplementary S7); no registered verdict changes. On XM3600 the ordering holds in all 6 leave-one-out fits, and no single drop changes the sign of the label-gold slope in any family (smallest leave-one-out slope +1.49).
<<<A7-M51 sec7_verbosity_sign.md NEW>>>
Post hoc, we refitted the slopes of Table 6.1 with each system left out in turn (system jackknife; the all-image rows of the second backbone and the bracket columns were not refitted; Supplementary S7); no registered verdict changes. On XM3600 the ordering holds in all 6 first-backbone leave-one-out fits, and under the registered precision rule no single drop changes the sign of the label-gold slope in any family (smallest leave-one-out slope +1.49); its system-jackknife interval includes 0 for the two English LVLM families and for UIT-ViIC with the Vietnamese lexicon (Supplementary Table S7.8).
<<<A7-M51 EVIDENCE>>>
Published supplement l.882: "Its jackknife interval (Table S7.8) includes 0 for the two English LVLM families and for UIT-ViIC with the Vietnamese lexicon. This sign stability holds under the registered precision rule; under the lower rule of the bracket no leave-one-out fit was computed." Table S7.8 has the clean-subset rows of the second backbone only (its values equal the clean-subset row of Table 6.1). The main text gave only the favourable half.

**A7-M52** (sec6-11 read F28)

<<<A7-M52 sec7_verbosity_sign.md OLD>>>
On the second backbone the one-reference sign is stable (−12.52 to −11.86).
<<<A7-M52 sec7_verbosity_sign.md NEW>>>
On the second backbone's XM3600-600 runs the one-reference sign is stable (−12.52 to −11.86).
<<<A7-M52 EVIDENCE>>>
Table S7.8, row "Second backbone, XM3600-600 (6)": −12.52 to −11.86; the other two sets have other ranges.

**A7-M53** (sec6-11 read F11)

<<<A7-M53 sec7_verbosity_sign.md OLD>>>
(the union of the classes named in all 50 references)
<<<A7-M53 sec7_verbosity_sign.md NEW>>>
(the union of the classes named in at least one of the 50 references)
<<<A7-M53 EVIDENCE>>>
manuscript/prereg/2026-10-29_a_companion/RULE.md l.35 ("50-reference consensus" = P_x(refs50)); "named in all 50" reads as the intersection. The registered name is kept.

**A7-M54** (sec6-11 read F29)

<<<A7-M54 sec7_verbosity_sign.md OLD>>>
nested reference golds are ordered even if objects are missing completely at random (SCAR); the size-matched nulls of X4 and X5 are a nested form of that SCAR case (Table 6.3), so X4 and X5 are the registered tests here that can reject uniform deletion only in that nested form, not random omission by individual references.
<<<A7-M54 sec7_verbosity_sign.md NEW>>>
nested reference golds are ordered even if the objects that references name are selected completely at random (SCAR); the size-matched nulls of X4 and X5 are a nested form of that SCAR case (Table 6.3), so X4 and X5 can reject uniform deletion only in that nested form; they cannot reject random omission by individual references.
<<<A7-M54 EVIDENCE>>>
SCAR is written out as "selected completely at random" in Section 2 and sec7 l.104. No claim changes.

**A7-M55** (sec6-11 read F10)

<<<A7-M55 sec7_verbosity_sign.md OLD>>>
and X4, in the Holm family by its tier-1 power rule, passed
<<<A7-M55 sec7_verbosity_sign.md NEW>>>
and X4, which entered the Holm family by its pre-written power rule (Supplementary Table S4.0, row A28), passed
<<<A7-M55 EVIDENCE>>>
manuscript/prereg/2026-10-30_a_t3/PREREG.md §7: "descriptive unless promoted by its pre-written power rule" (quoted in the source comment of the line). "tier-1" is an internal stage name.

**A7-M56** (sec6-11 read F30)

<<<A7-M56 sec8_human_validity.md OLD>>>
among same-image caption pairs where both differ;
<<<A7-M56 sec8_human_validity.md NEW>>>
among same-image caption pairs in which both the score and the judgment differ;
<<<A7-M56 EVIDENCE>>>
English only.

**A7-M57** (sec6-11 read F31)

<<<A7-M57 sec8_human_validity.md OLD>>>
Relevance falls by 0.024 per additional COCO class [−0.029, −0.020]
<<<A7-M57 sec8_human_validity.md NEW>>>
Relevance changes by −0.024 [−0.029, −0.020] per additional COCO class
<<<A7-M57 EVIDENCE>>>
Manifest row 358 (−0.024 with its interval). The bold registered label before it is not touched.

**A7-M58** (sec6-11 read F32)

<<<A7-M58 sec8_human_validity.md OLD>>>
the second part is a **FAIL** under the registered rule "point ≤ 0" whose interval includes 0, so the registered outcome is not supported.
<<<A7-M58 sec8_human_validity.md NEW>>>
the second part is a **FAIL** under the registered rule (point ≤ 0), although its interval includes 0, so the registered prediction is not supported.
<<<A7-M58 EVIDENCE>>>
sec3 l.52 (the three-way rule). Verdict token unchanged.

**A7-M59** (sec6-11 read F33)

<<<A7-M59 sec8_human_validity.md OLD>>>
RLAIF-V's (Yu et al., 2025) chosen-fewer share was predicted
<<<A7-M59 sec8_human_validity.md NEW>>>
The chosen-fewer share of RLAIF-V (Yu et al., 2025) was predicted
<<<A7-M59 EVIDENCE>>>
English only.

**A7-M60** (sec6-11 read F33; supplement read 22)

<<<A7-M60 sec8_human_validity.md OLD>>>
inside the kill interval [0.45, 0.55];
<<<A7-M60 sec8_human_validity.md NEW>>>
inside the interval [0.45, 0.55] of its withdrawal rule;
<<<A7-M60 EVIDENCE>>>
The rest of the paper says "withdrawal rule" (sec7 l.55, sec8 l.14; published supplement l.403 "withdrawal interval").

**A7-M61** (sec6-11 read F08)

<<<A7-M61 sec10_discussion.md OLD>>>
the label step, a change of completeness plus precision rule (Table 6.2),
<<<A7-M61 sec10_discussion.md NEW>>>
the label step, a change of gold and of precision rule (Table 6.2),
<<<A7-M61 EVIDENCE>>>
sec7 l.57: "The label step is not a step in completeness by size ... it is a change of gold and of scoring rule"; Table 6.2 gives the label gold as 0.87 times all references.

**A7-M62** (sec6-11 read F34)

<<<A7-M62 sec10_discussion.md OLD>>>
and FAIL on PASCAL-50S (Section 6.4). There the registration assumed
<<<A7-M62 sec10_discussion.md NEW>>>
FAIL on PASCAL-50S, and on COCO val2017 a larger slope than under one reference (PASS) with the premise not met against five references (Section 6.4). On PASCAL-50S the registration assumed
<<<A7-M62 EVIDENCE>>>
sec7 l.96 (registered text: label gold above one reference; against five references "premise not met") and Table 1 (A26). The tally left this set out although sec10 l.29 counts it. No number.

**A7-M63** (sec6-11 read F12)

<<<A7-M63 sec10_discussion.md OLD>>>
found 1,787 VOC label instances against 2,162 classes named in the 50 references
<<<A7-M63 sec10_discussion.md NEW>>>
found 1,787 image–class pairs in the VOC labels against 2,162 named in the 50 references
<<<A7-M63 EVIDENCE>>>
Table S7.6 ("Image–class pairs per V20 class"); sec7 l.108 says "image–class pairs". "Instances" reads as object instances.

**A7-M64** (sec6-11 read F35)

<<<A7-M64 sec10_discussion.md OLD>>>
one-reference gold fell below a size-matched
<<<A7-M64 sec10_discussion.md NEW>>>
the one-reference slope fell below a size-matched
<<<A7-M64 EVIDENCE>>>
sec7 l.96: "One reference gave a lower slope than size-matched random deletions". The other half of F35 sits in a held sentence and is left (Section 6.3 of this file).

**A7-M65** (sec6-11 read F36)

<<<A7-M65 sec11_limitations_ethics.md OLD>>>
and the UIT-ViIC pass is not counted.
<<<A7-M65 sec11_limitations_ethics.md NEW>>>
and the UIT-ViIC pass is not counted as support.
<<<A7-M65 EVIDENCE>>>
sec7 l.62: "a pass is not counted as support".

**A7-M66** (sec6-11 read F11)

<<<A7-M66 sec11_limitations_ethics.md OLD>>>
a consensus-gold sensitivity (classes named by at least two references) was not computed
<<<A7-M66 sec11_limitations_ethics.md NEW>>>
a sensitivity analysis that keeps only classes named by at least two references was not computed
<<<A7-M66 EVIDENCE>>>
"Consensus" is the registered name of the union of the 50 references (A7-M53); the second meaning is removed.

**A7-M67** (sec6-11 read F40)

<<<A7-M67 sec11_limitations_ethics.md OLD>>>
**PASCAL-50S outputs.** Under the registered data rule,
<<<A7-M67 sec11_limitations_ethics.md NEW>>>

**PASCAL-50S outputs.** Under the registered data rule,
<<<A7-M67 EVIDENCE>>>
l.51 followed l.50 with no empty line, so the two paragraphs were built as one.

**A7-M68** (sec6-11 read F41)

<<<A7-M68 sec11_limitations_ethics.md OLD>>>
we do not aim to discredit specific methods, report the full specification curve, and recommend
<<<A7-M68 sec11_limitations_ethics.md NEW>>>
we do not aim to discredit specific methods; we report the full specification curve and recommend
<<<A7-M68 EVIDENCE>>>
As written, "do not" could be read with all three verbs.

**A7-T01** (supplement read 3 (BLOCKING); sec6-11 read note 8)

<<<A7-T01 sec1_introduction.md OLD>>>
MIXED: condensed F1 (A12) and a two-panel transfer with no registered primary estimator (X-22);
<<<A7-T01 sec1_introduction.md NEW>>>
MIXED: condensed F1 (A12); PASS with a mixed estimator whose interval includes 1 and no registered primary estimator: a two-panel transfer (X-22);
<<<A7-T01 EVIDENCE>>>
Verdict file .session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json (0b2b3aa5e1a3) :: prereg_comparisons[22].in_interval_or_pass = "PASS_DRHO113_MIXED_MCP_CI_INCLUDES_1" (prediction C3-XM-PANEL-DRHO-113-TO-80; registered rule: slope below 1 with the upper bound of its 95% interval below 1). Table S4.0 prints this token in words ("PASS, with a mixed estimator whose interval includes 1 (no primary estimator registered)") and is right. Table 1 printed the one word MIXED, which is not the token. Table 1 now carries the words of Table S4.0; the row stays under "Other outcomes" and is not moved to the PASS row.

**A7-G01a** (sec6-11 read F01 (alternative that quotes the sentence; NOT applied by default))

<<<A7-G01a supplementary.md OLD>>>
**Scope of the confirmatory evidence.** The registered evidence on the verbosity sign is the out-of-sample test on XM3600.
<<<A7-G01a supplementary.md NEW>>>
**Registered outcome text for PASCAL-50S: a departure in wording.** The registration of the PASCAL-50S test fixed, before any output, the text to be printed for each outcome. For the outcome that occurred, this text has three sentences. Section 6.4 prints the first two, with the blanks filled and the section number updated; it does not print the third: "The images and captions have been public since 2008–2015 and may be in the pretraining data of these models; they are unseen by us, not necessarily by the models." In its place, Supplementary S7 states that we did not examine those data. No verdict and no number depends on this sentence; the registration file in the deposit holds the full text.

**Scope of the confirmatory evidence.** The registered evidence on the verbosity sign is the out-of-sample test on XM3600.
<<<A7-G01a EVIDENCE>>>
manuscript/prereg/2026-10-28_pascal50s/PREREG.md (1448ab13fcb5) §9.2, l.379: the registered text, third sentence copied word for word. See Section 5 of this file for why this alternative is switched off.

**A7-G01b** (sec6-11 read F01 (default))

<<<A7-G01b supplementary.md OLD>>>
**Scope of the confirmatory evidence.** The registered evidence on the verbosity sign is the out-of-sample test on XM3600.
<<<A7-G01b supplementary.md NEW>>>
**Registered outcome text for PASCAL-50S: a departure in wording.** The registration of the PASCAL-50S test fixed, before any output, the text to be printed for each outcome. For the outcome that occurred, this text has three sentences. Section 6.4 prints the first two, with the blanks filled and the section number updated; it does not print the third, which concerns the pretraining data of the evaluated models. In its place, Supplementary S7 states that we did not examine those data. No verdict and no number depends on this sentence; the registration file in the deposit holds the full text.

**Scope of the confirmatory evidence.** The registered evidence on the verbosity sign is the out-of-sample test on XM3600.
<<<A7-G01b EVIDENCE>>>
Same registration text. LOG: PI-1105m (PQ1) decided that caveats of this kind are dropped and one neutral sentence kept; PI-1106a had the same wording removed from the supplement. The main text is therefore not changed; the departure from "inserted as written" (heading of §9 of the registration) is recorded. The neutral sentence is at published supplement l.724.

**A7-G02** (sec6-11 read F01)

<<<A7-G02 sec7_verbosity_sign.md OLD>>>
Two departures from the registration are disclosed in Section 9.2; neither changes a verdict.
<<<A7-G02 sec7_verbosity_sign.md NEW>>>
Two departures from the registration in data handling are disclosed in Section 9.2, and one in the wording of the printed outcome text in Supplementary S4; none changes a verdict.
<<<A7-G02 EVIDENCE>>>
With the record of A7-G01a/b the count "two" would be incomplete. Skip this block if neither G01 block is applied.

**A7-G03** (sec6-11 read F01; CC-412 N1)

<<<A7-G03 sec7_verbosity_sign.md OLD>>>
§9.1's "for the reference ladder only" does not apply (label rung kept) -->
<<<A7-G03 sec7_verbosity_sign.md NEW>>>
§9.1's "for the reference ladder only" does not apply (label rung kept); the registered text has a third sentence, on the pretraining data of the evaluated models, which is not printed (investigator's decision PI-1105m, PQ1); the departure is recorded in Supplementary S4 (fix package v7) -->
<<<A7-G03 EVIDENCE>>>
Unprinted source comment of sec7 l.86; it said "inserted as written" for a text of which two of three sentences are printed.

**A7-D01** (sec6-11 read F15)

<<<A7-D01 declarations.md OLD>>>
and the KTVIC reference captions are not redistributed either; all are available from their original sources.
<<<A7-D01 declarations.md NEW>>>
and the KTVIC reference captions are not redistributed either; the same holds for the other third-party sets named in Sections 5 to 7; all are available from their original sources.
<<<A7-D01 EVIDENCE>>>
The list left out Composite, M-HalDetect, Flickr30k, ADE20K with Localized Narratives and the seven preference sets, all used in Sections 5 to 7. The sentence before it already says "Third-party data are given as pointers only". LOG read first: PI-1026az, PI-1110o, PI-1110n (5), PI-1115i. No agreement clause is touched (count asserted).

**A7-D02** (sec6-11 read F43)

<<<A7-D02 declarations.md OLD>>>
this paper's 600 Crossmodal-3600 images
<<<A7-D02 declarations.md NEW>>>
this paper's 600 XM3600 images
<<<A7-D02 EVIDENCE>>>
The Data availability statement and the paper use "XM3600".

**A7-S01** (supplement read 15)

<<<A7-S01 supplementary.md OLD>>>
(Karlin, 1968, *Total Positivity*, Vol. I; we did not check the section number against a primary page, because the book has no DOI or Crossref record and only its author, title and year could be checked; the step itself was re-derived and checked numerically)
<<<A7-S01 supplementary.md NEW>>>
(Karlin, 1968, *Total Positivity*, Vol. I; the step was re-derived and checked numerically)<!-- reference check (out of the printed text since fix package v7): no section number is cited; the book has no DOI or Crossref record, and only its author, title and year were checked -->
<<<A7-S01 EVIDENCE>>>
A working note on reference checking printed as text; it names a section number that the sentence does not give. The note is kept as a source comment, which the scrub step writes to the provenance table.

**A7-S02** (supplement read 15)

<<<A7-S02 supplementary.md OLD>>>
Lipton et al. theorem numbering checked against arXiv 1402.1892v2 (Theorem 1, Corollary 1; numbering in the LNCS version not checked).
<<<A7-S02 supplementary.md NEW>>>
Theorem numbers of Lipton et al. (2014) are those of arXiv 1402.1892v2.
<<<A7-S02 EVIDENCE>>>
As A7-S01; the reader needs only which numbering is used.

**A7-S03** (supplement read 15)

<<<A7-S03 supplementary.md OLD>>>
 (bibliographic data verified via Crossref; we did not check where in the paper the product inequality appears, because the publisher full text is behind a bot challenge), so coverage
<<<A7-S03 supplementary.md NEW>>>
<!-- reference check (out of the printed text since fix package v7): bibliographic data verified via Crossref; the place of the product inequality in the paper was not checked, the publisher full text could not be opened -->, so coverage
<<<A7-S03 EVIDENCE>>>
As A7-S01. The open check itself is listed for the authors in Section 6.2 of this file (I-5).

**A7-S04** (supplement read 32)

<<<A7-S04 supplementary.md OLD>>>
e.g. 0.425 vs 0.478 on COCO with one reference
<<<A7-S04 supplementary.md NEW>>>
e.g. 0.425 vs 0.478 on COCO-2500 with the first reference
<<<A7-S04 EVIDENCE>>>
Manifest rows 20 and 3960: c1_b1_b6_reproduction.json :: B1_L1_mstar_and_stopping.check_coco_gold.refs1_firstk.{d_recall, b}; that file is the COCO-2500 run (sec5 l.21 source comment).

**A7-S05** (sec2-5 read F17)

<<<A7-S05 supplementary.md OLD>>>
All matcher versions are pinned by file hash, and every table names the matcher.
<<<A7-S05 supplementary.md NEW>>>
All matcher versions are pinned by file hash.
<<<A7-S05 EVIDENCE>>>
As A7-M12: several tables name no matcher.

**A7-S06** (supplement read 31)

<<<A7-S06 supplementary.md OLD>>>
falls from 0.88 to 0.68 (Supplementary S1)<!-- src: sensitivity.json
<<<A7-S06 supplementary.md NEW>>>
falls from 0.88 to 0.68 on COCO-2500 (the COCO-5000 value, 66%, is in Supplementary S1)<!-- src: sensitivity.json
<<<A7-S06 EVIDENCE>>>
Published l.176: the COCO rows of this list are on COCO-2500; S1 (published l.74) prints 66% for COCO-5000.

**A7-S07** (supplement read 36)

<<<A7-S07 supplementary.md OLD>>>
applies the controls of Section 3.3(b) to methods
<<<A7-S07 supplementary.md NEW>>>
applies the controls of Section 3.3 for published outputs to methods
<<<A7-S07 EVIDENCE>>>
Section 3.3 has no item (b).

**A7-S08** (supplement read 1 (BLOCKING))

<<<A7-S08 supplementary.md OLD>>>
#### Training-based methods: a registered leaderboard (not scored)
<<<A7-S08 supplementary.md NEW>>>
**Table S3.2.** POST HOC per-comparison values behind Table S3.1 (not registered; no verdict). Precision gain of each published method over its baseline, in points, with its unadjusted 95% bootstrap interval: raw and under the three controls. Rows are in the order of the result file. LiM-EOS is the end-of-sequence stopping method of Yue et al. (2024).

| Method | Baseline | Backbone | Images | Raw ΔP | Matched prefix | Sentence tie-average | Uniform random subset |
|---|---|---|---|---|---|---|---|
| OPERA | greedy | InstructBLIP | 495 | +4.74 [+2.49, +7.04] | +3.88 [+2.49, +5.27] | +4.21 [+2.76, +5.67] | +4.93 [+3.06, +6.87] |
| OPERA | beam search | InstructBLIP | 495 | +3.86 [+1.89, +5.87] | +1.09 [+0.07, +2.14] | +1.26 [+0.27, +2.27] | +3.43 [+1.94, +4.93] |
| OPERA | greedy | LLaVA-1.5 | 499 | +1.41 [−0.38, +3.29] | +0.07 [−0.99, +1.21] | +0.02 [−1.10, +1.21] | +1.22 [−0.32, +2.73] |
| OPERA | beam search | LLaVA-1.5 | 499 | +1.43 [−0.24, +3.12] | +0.48 [−0.61, +1.54] | +0.29 [−0.77, +1.35] | +1.11 [−0.24, +2.44] |
| OPERA | greedy | MiniGPT-4 | 499 | +2.83 [+0.48, +5.10] | +0.81 [−0.20, +1.87] | +0.92 [−0.12, +2.02] | +2.37 [+0.74, +3.99] |
| OPERA | beam search | MiniGPT-4 | 499 | +1.74 [+0.08, +3.40] | +0.19 [−0.39, +0.78] | +0.23 [−0.38, +0.85] | +1.42 [+0.22, +2.56] |
| OPERA | greedy | Shikra | 499 | +6.72 [+4.00, +9.44] | −1.23 [−2.62, +0.08] | −1.14 [−2.44, +0.12] | +5.45 [+3.36, +7.40] |
| OPERA | beam search | Shikra | 499 | +3.47 [+0.75, +6.03] | −1.23 [−2.42, −0.08] | −1.39 [−2.55, −0.25] | +2.63 [+0.78, +4.54] |
| VCD | greedy | LLaVA-1.5-7B | 495 | +0.50 [−0.22, +1.19] | +0.06 [−0.44, +0.54] | +0.04 [−0.50, +0.51] | +0.42 [−0.18, +1.00] |
| OPERA | greedy | LLaVA-1.5-7B | 495 | +1.49 [+0.27, +2.79] | +0.26 [−0.51, +0.98] | +0.29 [−0.50, +1.01] | +1.32 [+0.25, +2.38] |
| OPERA-fast | greedy | LLaVA-1.5-7B | 495 | +2.00 [+0.23, +3.69] | +0.80 [−0.53, +2.02] | +0.68 [−0.68, +1.93] | +1.49 [−0.10, +2.96] |
| LiM-EOS | greedy | LLaVA-1.5-7B | 495 | +7.91 [+6.01, +9.87] | +1.08 [−0.07, +2.25] | +1.42 [+0.24, +2.58] | +6.06 [+4.40, +7.68] |
| LiM-EOS | greedy | LLaVA-1.5-13B | 495 | +3.56 [+1.80, +5.38] | +0.43 [−0.71, +1.57] | +0.36 [−0.75, +1.48] | +2.66 [+1.26, +4.04] |
| LiM-EOS | greedy | LLaVA-7B | 495 | +3.75 [+1.65, +5.86] | −0.20 [−1.21, +0.76] | −0.19 [−1.27, +0.79] | +2.27 [+0.73, +3.77] |
| LiM-EOS | greedy | MiniGPT-v2 | 495 | +5.69 [+3.36, +8.23] | +2.81 [+0.91, +4.67] | +2.78 [+1.06, +4.50] | +4.70 [+2.77, +6.79] |

**Table S3.3.** Minimum detectable effect of each comparison of Table S3.2, in precision points (POST HOC; no verdict): normal approximation, 80% power, standard error from the width of the 95% interval. In each cell the first value is for α = 0.05 and the second for α = 0.05/15.

| Method | Baseline | Backbone | Raw ΔP | Matched prefix | Sentence tie-average | Uniform random subset |
|---|---|---|---|---|---|---|
| OPERA | greedy | InstructBLIP | 3.25; 4.38 | 1.99; 2.68 | 2.08; 2.80 | 2.72; 3.67 |
| OPERA | beam search | InstructBLIP | 2.84; 3.83 | 1.48; 1.99 | 1.43; 1.93 | 2.14; 2.88 |
| OPERA | greedy | LLaVA-1.5 | 2.63; 3.54 | 1.57; 2.12 | 1.65; 2.23 | 2.18; 2.94 |
| OPERA | beam search | LLaVA-1.5 | 2.40; 3.23 | 1.53; 2.06 | 1.51; 2.04 | 1.91; 2.58 |
| OPERA | greedy | MiniGPT-4 | 3.30; 4.45 | 1.48; 2.00 | 1.53; 2.07 | 2.32; 3.12 |
| OPERA | beam search | MiniGPT-4 | 2.37; 3.20 | 0.83; 1.12 | 0.88; 1.19 | 1.67; 2.26 |
| OPERA | greedy | Shikra | 3.89; 5.24 | 1.93; 2.60 | 1.83; 2.47 | 2.89; 3.89 |
| OPERA | beam search | Shikra | 3.78; 5.09 | 1.67; 2.25 | 1.64; 2.21 | 2.69; 3.62 |
| VCD | greedy | LLaVA-1.5-7B | 1.01; 1.36 | 0.70; 0.94 | 0.71; 0.96 | 0.84; 1.14 |
| OPERA | greedy | LLaVA-1.5-7B | 1.80; 2.43 | 1.06; 1.43 | 1.07; 1.45 | 1.52; 2.05 |
| OPERA-fast | greedy | LLaVA-1.5-7B | 2.47; 3.33 | 1.82; 2.46 | 1.86; 2.51 | 2.18; 2.94 |
| LiM-EOS | greedy | LLaVA-1.5-7B | 2.76; 3.72 | 1.66; 2.24 | 1.67; 2.25 | 2.34; 3.16 |
| LiM-EOS | greedy | LLaVA-1.5-13B | 2.56; 3.46 | 1.63; 2.19 | 1.59; 2.14 | 1.99; 2.68 |
| LiM-EOS | greedy | LLaVA-7B | 3.01; 4.06 | 1.40; 1.89 | 1.47; 1.98 | 2.18; 2.93 |
| LiM-EOS | greedy | MiniGPT-v2 | 3.48; 4.69 | 2.69; 3.62 | 2.46; 3.31 | 2.87; 3.87 |

#### Training-based methods: a registered leaderboard (not scored)
<<<A7-S08 EVIDENCE>>>
The per-comparison table that the title of S3 and main Section 8.3 promise (Table S3.2), and the minimum detectable effects that the positive-control paragraph promises (Table S3.3). Table S3.3: every value is recomputed by script from the intervals with the stated convention and must equal, to two decimals, the row of the committed file .session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex (ab2d63f5ddf5), which also gives the row labels (method, baseline, backbone) and the image counts; 60 manifest rows. Table S3.2: every cell is read by script from .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json (184f9ccac1b9; committed in the paper repository as results/session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json, same sha256) :: pairs_15.<pair>.{dP_raw, dP_MCP_prefix, dP_MCP_sent_tieavg, dP_MCP_rand_exact}.{est, ci95} and .n_img; 60 manifest rows. The column means equal overview_15_pairs.mean_dP_* (asserted). The apply script rebuilds the table from the file and compares it with this text.

**A7-S09** (supplement read 1 (BLOCKING))

<<<A7-S09 supplementary.md OLD>>>
and Supplementary S3 gives the minimum detectable effect for each comparison
<<<A7-S09 supplementary.md NEW>>>
and Table S3.3 gives the minimum detectable effect for each comparison
<<<A7-S09 EVIDENCE>>>
The promise is now kept by Table S3.3 (block A7-S08), whose values exist in a committed file: .session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex (ab2d63f5ddf5; in the paper repository under results/, same sha256), named by the source comment of this very sentence.

**A7-S10** (supplement read 22; sec6-11 read note 8)

<<<A7-S10 supplementary.md OLD>>>
registered (in the Holm family by its tier-1 power rule; one test look)
<<<A7-S10 supplementary.md NEW>>>
registered (in the Holm family by its pre-written power rule; one test look)
<<<A7-S10 EVIDENCE>>>
As A7-M55 (Table S4.0, row A28).

**A7-S11** (supplement read 2; CC-422 N9)

<<<A7-S11 supplementary.md OLD>>>
XM3600 (Thapliyal et al., EMNLP 2022)<!-- cite: thapliyal2022crossmodal,
<<<A7-S11 supplementary.md NEW>>>
XM3600 (Thapliyal et al., 2022)<!-- cite: thapliyal2022crossmodal,
<<<A7-S11 EVIDENCE>>>
The form of every other citation of the supplement; the entry was added to the list at a7f2b4e (CC-422 W5).

**A7-S12** (supplement read 38)

<<<A7-S12 supplementary.md OLD>>>
were added, each run only after a licence check and a committed pre-registration (the LongCap-Arena pre-registration; the results file was written after the commit)<!-- added under PD-7;
<<<A7-S12 supplementary.md NEW>>>
were planned, each to be run only after a licence check and a committed pre-registration; the LongCap-Arena test was run (its results file was written after the commit of its pre-registration)<!-- added under PD-7;
<<<A7-S12 EVIDENCE>>>
Only one of the two was run; the old sentence said both were added and run.

**A7-S13** (supplement read 11)

<<<A7-S13 supplementary.md OLD>>>
## S5 Exchangeability: all corpus and split rows
<<<A7-S13 supplementary.md NEW>>>
## S5 Exchangeability: further corpus rows
<<<A7-S13 EVIDENCE>>>
S5 prints no split row; the split values are only in an unprinted source comment.

**A7-S14** (supplement read 11)

<<<A7-S14 supplementary.md OLD>>>
With several dozen corpus–split rows in the audit (Supplementary S5), one small-split excursion
<<<A7-S14 supplementary.md NEW>>>
With several dozen corpus–split rows in the audit (not printed here), one small-split excursion
<<<A7-S14 EVIDENCE>>>
As A7-S13. The pointer led to rows that the part does not print.

**A7-S15** (supplement read 37)

<<<A7-S15 supplementary.md OLD>>>
their registered verdicts are listed in Table 1 (rows X-22 to X-25).
<<<A7-S15 supplementary.md NEW>>>
their registered verdicts are listed in Table S4.0 (rows X-22 to X-25).
<<<A7-S15 EVIDENCE>>>
Table 1 is grouped by outcome and has no row per id; Table S4.0 has the rows (published l.281-282).

**A7-S16** (supplement read 39)

<<<A7-S16 supplementary.md OLD>>>
give within-writer bounds at best on such data; we report none. For COCO-5000 and UIT-ViIC (development data) see Supplementary S1.M and S5.
<<<A7-S16 supplementary.md NEW>>>
give within-writer bounds at best on such data; we report none for single-writer data. The bound for COCO-5000 and UIT-ViIC (development data) is in Supplementary S1.M and Table S5.M.
<<<A7-S16 EVIDENCE>>>
"we report none" stood beside a pointer to a reported bound; sec5 l.39 has the same content in the main text.

**A7-S17** (supplement read 39)

<<<A7-S17 supplementary.md OLD>>>
Rater-equivalence units (Resnick et al.) are defined
<<<A7-S17 supplementary.md NEW>>>
Rater-equivalence units (Resnick et al., 2021) are defined
<<<A7-S17 EVIDENCE>>>
Year as in the main text and the list.

**A7-S18** (supplement read 24)

<<<A7-S18 supplementary.md OLD>>>
| Check against labels, D_L = (L − Ŝ^L)/L |
<<<A7-S18 supplementary.md NEW>>>
| Check against labels, D_L = (L − Ŝ^L)/L, where L is the number of (image, class) pairs in the instance labels and Ŝ^L the estimate computed on the references restricted to the labelled classes |
<<<A7-S18 EVIDENCE>>>
manuscript/prereg/2026-11-07_a_m1/A_M1_PLAN_v2.md l.81 (arm L: classes in the instance labels; L = sum over images) and l.281-283 ("D_L = (L − Ŝ^L)/L"; "on the same references restricted to labelled classes"). No number.

**A7-S19** (supplement read 40)

<<<A7-S19 supplementary.md OLD>>>
is not supported at the registered tolerance;
<<<A7-S19 supplementary.md NEW>>>
is not supported at the pre-set tolerance;
<<<A7-S19 EVIDENCE>>>
The check is called pre-specified, not registered, in the same notes (published l.528) and in S1.M (l.136).

**A7-S20** (supplement read 10)

<<<A7-S20 supplementary.md OLD>>>
## S6 Numbers manifest, exploratory lexicon and data audits
<<<A7-S20 supplementary.md NEW>>>
## S6 Numbers manifest and data audits
<<<A7-S20 EVIDENCE>>>
S6 holds no list or description of the larger noun vocabulary. No line of the main text names the heading by its title.

**A7-S21** (supplement read 10)

<<<A7-S21 supplementary.md OLD>>>
and supports no claim in this paper (Supplementary S6 lists it with that label).
<<<A7-S21 supplementary.md NEW>>>
and supports no claim in this paper.
<<<A7-S21 EVIDENCE>>>
As A7-S20: the pointer led to nothing.

**A7-S22** (supplement read 10)

<<<A7-S22 supplementary.md OLD>>>
A larger noun vocabulary, tried post hoc, supports no claim (Supplementary S6).
<<<A7-S22 supplementary.md NEW>>>
A larger noun vocabulary, tried post hoc, supports no claim.
<<<A7-S22 EVIDENCE>>>
As A7-S20.

**A7-S23** (supplement read 25)

<<<A7-S23 supplementary.md OLD>>>
| Mean $\Delta k$ | Same, pairs with $\lvert\Delta\text{words}\rvert \le 2$ |
<<<A7-S23 supplementary.md NEW>>>
| Mean $\Delta k$ | Chosen names fewer, among unmatched pairs with $\lvert\Delta\text{words}\rvert \le 2$ |
<<<A7-S23 EVIDENCE>>>
Published l.562: "on pairs within two words the share stays at 0.854, 0.763, 0.886 and 0.791" (the values of this column for the four sets).

**A7-S24** (supplement read 22)

<<<A7-S24 supplementary.md OLD>>>
inside the kill interval, so the prediction failed and the first half of the rule is met
<<<A7-S24 supplementary.md NEW>>>
inside the withdrawal interval, so the prediction failed and the first half of the rule is met
<<<A7-S24 EVIDENCE>>>
The same paragraph in S4 (published l.403) says "withdrawal interval".

**A7-S25** (supplement read 19)

<<<A7-S25 supplementary.md OLD>>>
detailed captions (post hoc; Sections 6.3 and 8.5).**
<<<A7-S25 supplementary.md NEW>>>
detailed captions (post hoc; Section 6.3).**
<<<A7-S25 EVIDENCE>>>
The printed text of Section 8 does not mention the cap (0 hits for the word in sec10_discussion.md outside comments).

**A7-S26** (supplement read 41)

<<<A7-S26 supplementary.md OLD>>>
**Within one prompt and zero-shot only.**
<<<A7-S26 supplementary.md NEW>>>
**Within one prompt.**
<<<A7-S26 EVIDENCE>>>
The paragraph holds no zero-shot-only result.

**A7-S27** (supplement read 42)

<<<A7-S27 supplementary.md OLD>>>
Totals: 1,787 label instances against 2,162 reference classes (ratio 0.83);
<<<A7-S27 supplementary.md NEW>>>
Totals: 1,787 image–class pairs in the labels against 2,162 in the references (ratio 0.83);
<<<A7-S27 EVIDENCE>>>
Table S7.6 calls both image–class pairs. The quoted fixed sentence after it is not touched.

**A7-S28** (supplement read 22)

<<<A7-S28 supplementary.md OLD>>>
inside the kill interval [0.45, 0.55];
<<<A7-S28 supplementary.md NEW>>>
inside the interval [0.45, 0.55] of its withdrawal rule;
<<<A7-S28 EVIDENCE>>>
The S10 copy of the sentence of A7-M60.

**A7-S29** (CC-422 N9)

<<<A7-S29 supplementary.md OLD>>>
Jordi Pont Tuset, Xi Chen, and Radu Soricut. 2022.
<<<A7-S29 supplementary.md NEW>>>
Jordi Pont-Tuset, Xi Chen, and Radu Soricut. 2022.
<<<A7-S29 EVIDENCE>>>
Reference list of the supplement (after the end of S11; no byte of S11 moves). The same person is "Pont-Tuset" in the list's 2020 entry and on the arXiv record 2205.12522 (CC-422 N9).

**A7-B01** (CC-422 N9)

<<<A7-B01 paperA.bib OLD>>>
author = {Thapliyal, Ashish V. and Pont Tuset, Jordi and Chen, Xi and Soricut, Radu},
<<<A7-B01 paperA.bib NEW>>>
author = {Thapliyal, Ashish V. and Pont-Tuset, Jordi and Chen, Xi and Soricut, Radu},
<<<A7-B01 EVIDENCE>>>
paperA.bib l.780 against l.543 and l.1268 of the same file ("Pont-Tuset, Jordi"). The main reference list is built from this file.



## 4. Steps that are not blocks

**S1. Manifest rows** (appended to `paper/number_manifest.tsv`; the script checks the sha256 prefix of every source file and rebuilds the last 120 rows from the result files):

```
1,000 (second-backbone family bootstrap draws)	A	manuscript/prereg/2026-10-18_g2b_qwen3vl_ladder.md	l.163 "1000 image-bootstrap draws per analysis set"	2e6b3e871144	keyed_text (sec3 §3.6; sec2-5 read F27; fix package v7)
2,000 (LongCap-Arena bootstrap draws)	A	.session_backup/2026-10-15/r13_human/q2_longcap_arena.json	nboot	50f3a8635fce	keyed (sec3 §3.6; sec2-5 read F27; fix package v7)
2,000 (seed placebo bootstrap draws)	A	.session_backup/2026-10-18/n9k2_scoring/k2/k2_scores.json	thresholds_from_prereg.n_boot	0f0e952eeffb	keyed (sec3 §3.6; sec2-5 read F27; fix package v7)
1,000 (eight-LVLM test bootstrap draws)	A	data/results/a_n2/a_n2_run.json	config.n_boot	1f6ce422e016	keyed (sec3 §3.6; sec2-5 read F28; fix package v7)
23 (registered second-backbone decodes, all checked before scoring)	A	data/results/g2b/g2b_score_record/precheck.json	registered_runs = checked_ok	02bdca27949e	keyed (sec7 §6.3; sec6-11 read F45; fix package v7)
2 of 7 (PASCAL-50S models with a negative VOC-label slope)	A	data/results/p50/p50_decide.json	PAIR_m_descriptive.*.voc20|V20 (count below 0: llava15_7b, llava_ov_7b)	0da4cab90fe9	DERIVED (descriptive; sec7 §6.4; sec6-11 read F45; fix package v7)
1.99 [1.97, 2.02] (k_eff of an adjacent pair of references, COCO-5000)	A	.session_backup/2026-10-26/a_full5000/out/h4_r4_full5000_all9.json	T3.k_eff_adjacent_pair_slots2to5.{point,ci} = 1.993 [1.967, 2.02]	39c97d0de681	keyed (rounded to two decimals; sec5 §5.3; sec2-5 read F38; fix package v7)
16% (OPERA on Shikra against beam search: fewer objects named)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	1 - pairs_15.opera/shikra__ours vs opera/shikra__beam5.M_ratio.est (0.842)	184f9ccac1b9	DERIVED (POST HOC; supp S3; supplement read 17; fix package v7)
[0.414, 0.647] (XM3600 adjacency share interval, 150 images with three references)	A	.session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json	n2_reference_adjacency_verification.full_3600_150_3ref_images.bootstrap_ci95_b5000 = [0.4141, 0.6471]	0b2b3aa5e1a3	keyed (rounded to three decimals; post hoc check; supp S5, S7; supplement read 17; fix package v7)
+4.74 [+2.49, +7.04] (Table S3.2: OPERA vs greedy, InstructBLIP, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/instructblip__ours vs opera/instructblip__greedy.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
3.25 / 4.38 (Table S3.3: minimum detectable effect, OPERA vs greedy, InstructBLIP, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & InstructBLIP", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/instructblip__ours vs opera/instructblip__greedy.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+3.88 [+2.49, +5.27] (Table S3.2: OPERA vs greedy, InstructBLIP, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/instructblip__ours vs opera/instructblip__greedy.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.99 / 2.68 (Table S3.3: minimum detectable effect, OPERA vs greedy, InstructBLIP, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & InstructBLIP", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/instructblip__ours vs opera/instructblip__greedy.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+4.21 [+2.76, +5.67] (Table S3.2: OPERA vs greedy, InstructBLIP, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/instructblip__ours vs opera/instructblip__greedy.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.08 / 2.80 (Table S3.3: minimum detectable effect, OPERA vs greedy, InstructBLIP, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & InstructBLIP", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/instructblip__ours vs opera/instructblip__greedy.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+4.93 [+3.06, +6.87] (Table S3.2: OPERA vs greedy, InstructBLIP, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/instructblip__ours vs opera/instructblip__greedy.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.72 / 3.67 (Table S3.3: minimum detectable effect, OPERA vs greedy, InstructBLIP, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & InstructBLIP", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/instructblip__ours vs opera/instructblip__greedy.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+3.86 [+1.89, +5.87] (Table S3.2: OPERA vs beam search, InstructBLIP, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/instructblip__ours vs opera/instructblip__beam5.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.84 / 3.83 (Table S3.3: minimum detectable effect, OPERA vs beam search, InstructBLIP, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & InstructBLIP", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/instructblip__ours vs opera/instructblip__beam5.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.09 [+0.07, +2.14] (Table S3.2: OPERA vs beam search, InstructBLIP, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/instructblip__ours vs opera/instructblip__beam5.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.48 / 1.99 (Table S3.3: minimum detectable effect, OPERA vs beam search, InstructBLIP, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & InstructBLIP", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/instructblip__ours vs opera/instructblip__beam5.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.26 [+0.27, +2.27] (Table S3.2: OPERA vs beam search, InstructBLIP, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/instructblip__ours vs opera/instructblip__beam5.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.43 / 1.93 (Table S3.3: minimum detectable effect, OPERA vs beam search, InstructBLIP, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & InstructBLIP", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/instructblip__ours vs opera/instructblip__beam5.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+3.43 [+1.94, +4.93] (Table S3.2: OPERA vs beam search, InstructBLIP, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/instructblip__ours vs opera/instructblip__beam5.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.14 / 2.88 (Table S3.3: minimum detectable effect, OPERA vs beam search, InstructBLIP, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & InstructBLIP", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/instructblip__ours vs opera/instructblip__beam5.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.41 [-0.38, +3.29] (Table S3.2: OPERA vs greedy, LLaVA-1.5, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__greedy.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.63 / 3.54 (Table S3.3: minimum detectable effect, OPERA vs greedy, LLaVA-1.5, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & LLaVA-1.5", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__greedy.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.07 [-0.99, +1.21] (Table S3.2: OPERA vs greedy, LLaVA-1.5, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__greedy.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.57 / 2.12 (Table S3.3: minimum detectable effect, OPERA vs greedy, LLaVA-1.5, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & LLaVA-1.5", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__greedy.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.02 [-1.10, +1.21] (Table S3.2: OPERA vs greedy, LLaVA-1.5, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__greedy.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.65 / 2.23 (Table S3.3: minimum detectable effect, OPERA vs greedy, LLaVA-1.5, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & LLaVA-1.5", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__greedy.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.22 [-0.32, +2.73] (Table S3.2: OPERA vs greedy, LLaVA-1.5, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__greedy.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.18 / 2.94 (Table S3.3: minimum detectable effect, OPERA vs greedy, LLaVA-1.5, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & LLaVA-1.5", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__greedy.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.43 [-0.24, +3.12] (Table S3.2: OPERA vs beam search, LLaVA-1.5, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__beam5.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.40 / 3.23 (Table S3.3: minimum detectable effect, OPERA vs beam search, LLaVA-1.5, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & LLaVA-1.5", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__beam5.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.48 [-0.61, +1.54] (Table S3.2: OPERA vs beam search, LLaVA-1.5, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__beam5.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.53 / 2.06 (Table S3.3: minimum detectable effect, OPERA vs beam search, LLaVA-1.5, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & LLaVA-1.5", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__beam5.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.29 [-0.77, +1.35] (Table S3.2: OPERA vs beam search, LLaVA-1.5, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__beam5.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.51 / 2.04 (Table S3.3: minimum detectable effect, OPERA vs beam search, LLaVA-1.5, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & LLaVA-1.5", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__beam5.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.11 [-0.24, +2.44] (Table S3.2: OPERA vs beam search, LLaVA-1.5, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__beam5.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.91 / 2.58 (Table S3.3: minimum detectable effect, OPERA vs beam search, LLaVA-1.5, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & LLaVA-1.5", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/llava-1.5__ours vs opera/llava-1.5__beam5.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+2.83 [+0.48, +5.10] (Table S3.2: OPERA vs greedy, MiniGPT-4, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/minigpt4__ours vs opera/minigpt4__greedy.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
3.30 / 4.45 (Table S3.3: minimum detectable effect, OPERA vs greedy, MiniGPT-4, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & MiniGPT-4", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/minigpt4__ours vs opera/minigpt4__greedy.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.81 [-0.20, +1.87] (Table S3.2: OPERA vs greedy, MiniGPT-4, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/minigpt4__ours vs opera/minigpt4__greedy.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.48 / 2.00 (Table S3.3: minimum detectable effect, OPERA vs greedy, MiniGPT-4, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & MiniGPT-4", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/minigpt4__ours vs opera/minigpt4__greedy.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.92 [-0.12, +2.02] (Table S3.2: OPERA vs greedy, MiniGPT-4, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/minigpt4__ours vs opera/minigpt4__greedy.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.53 / 2.07 (Table S3.3: minimum detectable effect, OPERA vs greedy, MiniGPT-4, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & MiniGPT-4", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/minigpt4__ours vs opera/minigpt4__greedy.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+2.37 [+0.74, +3.99] (Table S3.2: OPERA vs greedy, MiniGPT-4, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/minigpt4__ours vs opera/minigpt4__greedy.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.32 / 3.12 (Table S3.3: minimum detectable effect, OPERA vs greedy, MiniGPT-4, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & MiniGPT-4", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/minigpt4__ours vs opera/minigpt4__greedy.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.74 [+0.08, +3.40] (Table S3.2: OPERA vs beam search, MiniGPT-4, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/minigpt4__ours vs opera/minigpt4__beam5.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.37 / 3.20 (Table S3.3: minimum detectable effect, OPERA vs beam search, MiniGPT-4, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & MiniGPT-4", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/minigpt4__ours vs opera/minigpt4__beam5.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.19 [-0.39, +0.78] (Table S3.2: OPERA vs beam search, MiniGPT-4, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/minigpt4__ours vs opera/minigpt4__beam5.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
0.83 / 1.12 (Table S3.3: minimum detectable effect, OPERA vs beam search, MiniGPT-4, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & MiniGPT-4", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/minigpt4__ours vs opera/minigpt4__beam5.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.23 [-0.38, +0.85] (Table S3.2: OPERA vs beam search, MiniGPT-4, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/minigpt4__ours vs opera/minigpt4__beam5.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
0.88 / 1.19 (Table S3.3: minimum detectable effect, OPERA vs beam search, MiniGPT-4, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & MiniGPT-4", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/minigpt4__ours vs opera/minigpt4__beam5.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.42 [+0.22, +2.56] (Table S3.2: OPERA vs beam search, MiniGPT-4, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/minigpt4__ours vs opera/minigpt4__beam5.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.67 / 2.26 (Table S3.3: minimum detectable effect, OPERA vs beam search, MiniGPT-4, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & MiniGPT-4", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/minigpt4__ours vs opera/minigpt4__beam5.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+6.72 [+4.00, +9.44] (Table S3.2: OPERA vs greedy, Shikra, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/shikra__ours vs opera/shikra__greedy.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
3.89 / 5.24 (Table S3.3: minimum detectable effect, OPERA vs greedy, Shikra, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & Shikra", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/shikra__ours vs opera/shikra__greedy.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
-1.23 [-2.62, +0.08] (Table S3.2: OPERA vs greedy, Shikra, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/shikra__ours vs opera/shikra__greedy.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.93 / 2.60 (Table S3.3: minimum detectable effect, OPERA vs greedy, Shikra, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & Shikra", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/shikra__ours vs opera/shikra__greedy.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
-1.14 [-2.44, +0.12] (Table S3.2: OPERA vs greedy, Shikra, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/shikra__ours vs opera/shikra__greedy.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.83 / 2.47 (Table S3.3: minimum detectable effect, OPERA vs greedy, Shikra, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & Shikra", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/shikra__ours vs opera/shikra__greedy.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+5.45 [+3.36, +7.40] (Table S3.2: OPERA vs greedy, Shikra, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/shikra__ours vs opera/shikra__greedy.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.89 / 3.89 (Table S3.3: minimum detectable effect, OPERA vs greedy, Shikra, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & Shikra", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/shikra__ours vs opera/shikra__greedy.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+3.47 [+0.75, +6.03] (Table S3.2: OPERA vs beam search, Shikra, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/shikra__ours vs opera/shikra__beam5.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
3.78 / 5.09 (Table S3.3: minimum detectable effect, OPERA vs beam search, Shikra, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & Shikra", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/shikra__ours vs opera/shikra__beam5.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
-1.23 [-2.42, -0.08] (Table S3.2: OPERA vs beam search, Shikra, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/shikra__ours vs opera/shikra__beam5.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.67 / 2.25 (Table S3.3: minimum detectable effect, OPERA vs beam search, Shikra, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & Shikra", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/shikra__ours vs opera/shikra__beam5.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
-1.39 [-2.55, -0.25] (Table S3.2: OPERA vs beam search, Shikra, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/shikra__ours vs opera/shikra__beam5.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.64 / 2.21 (Table S3.3: minimum detectable effect, OPERA vs beam search, Shikra, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & Shikra", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/shikra__ours vs opera/shikra__beam5.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+2.63 [+0.78, +4.54] (Table S3.2: OPERA vs beam search, Shikra, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.opera/shikra__ours vs opera/shikra__beam5.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.69 / 3.62 (Table S3.3: minimum detectable effect, OPERA vs beam search, Shikra, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & beam5 & Shikra", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.opera/shikra__ours vs opera/shikra__beam5.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.50 [-0.22, +1.19] (Table S3.2: VCD vs greedy, LLaVA-1.5-7B, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r2-vcd vs lim/r1-llava1.5-7b.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.01 / 1.36 (Table S3.3: minimum detectable effect, VCD vs greedy, LLaVA-1.5-7B, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "VCD & greedy & LLaVA-1.5-7B", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r2-vcd vs lim/r1-llava1.5-7b.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.06 [-0.44, +0.54] (Table S3.2: VCD vs greedy, LLaVA-1.5-7B, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r2-vcd vs lim/r1-llava1.5-7b.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
0.70 / 0.94 (Table S3.3: minimum detectable effect, VCD vs greedy, LLaVA-1.5-7B, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "VCD & greedy & LLaVA-1.5-7B", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r2-vcd vs lim/r1-llava1.5-7b.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.04 [-0.50, +0.51] (Table S3.2: VCD vs greedy, LLaVA-1.5-7B, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r2-vcd vs lim/r1-llava1.5-7b.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
0.71 / 0.96 (Table S3.3: minimum detectable effect, VCD vs greedy, LLaVA-1.5-7B, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "VCD & greedy & LLaVA-1.5-7B", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r2-vcd vs lim/r1-llava1.5-7b.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.42 [-0.18, +1.00] (Table S3.2: VCD vs greedy, LLaVA-1.5-7B, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r2-vcd vs lim/r1-llava1.5-7b.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
0.84 / 1.14 (Table S3.3: minimum detectable effect, VCD vs greedy, LLaVA-1.5-7B, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "VCD & greedy & LLaVA-1.5-7B", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r2-vcd vs lim/r1-llava1.5-7b.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.49 [+0.27, +2.79] (Table S3.2: OPERA vs greedy, LLaVA-1.5-7B, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r3-opera vs lim/r1-llava1.5-7b.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.80 / 2.43 (Table S3.3: minimum detectable effect, OPERA vs greedy, LLaVA-1.5-7B, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & LLaVA-1.5-7B", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r3-opera vs lim/r1-llava1.5-7b.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.26 [-0.51, +0.98] (Table S3.2: OPERA vs greedy, LLaVA-1.5-7B, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r3-opera vs lim/r1-llava1.5-7b.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.06 / 1.43 (Table S3.3: minimum detectable effect, OPERA vs greedy, LLaVA-1.5-7B, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & LLaVA-1.5-7B", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r3-opera vs lim/r1-llava1.5-7b.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.29 [-0.50, +1.01] (Table S3.2: OPERA vs greedy, LLaVA-1.5-7B, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r3-opera vs lim/r1-llava1.5-7b.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.07 / 1.45 (Table S3.3: minimum detectable effect, OPERA vs greedy, LLaVA-1.5-7B, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & LLaVA-1.5-7B", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r3-opera vs lim/r1-llava1.5-7b.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.32 [+0.25, +2.38] (Table S3.2: OPERA vs greedy, LLaVA-1.5-7B, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r3-opera vs lim/r1-llava1.5-7b.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.52 / 2.05 (Table S3.3: minimum detectable effect, OPERA vs greedy, LLaVA-1.5-7B, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA & greedy & LLaVA-1.5-7B", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r3-opera vs lim/r1-llava1.5-7b.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+2.00 [+0.23, +3.69] (Table S3.2: OPERA-fast vs greedy, LLaVA-1.5-7B, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r4-opera-fast vs lim/r1-llava1.5-7b.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.47 / 3.33 (Table S3.3: minimum detectable effect, OPERA-fast vs greedy, LLaVA-1.5-7B, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA-fast & greedy & LLaVA-1.5-7B", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r4-opera-fast vs lim/r1-llava1.5-7b.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.80 [-0.53, +2.02] (Table S3.2: OPERA-fast vs greedy, LLaVA-1.5-7B, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r4-opera-fast vs lim/r1-llava1.5-7b.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.82 / 2.46 (Table S3.3: minimum detectable effect, OPERA-fast vs greedy, LLaVA-1.5-7B, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA-fast & greedy & LLaVA-1.5-7B", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r4-opera-fast vs lim/r1-llava1.5-7b.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.68 [-0.68, +1.93] (Table S3.2: OPERA-fast vs greedy, LLaVA-1.5-7B, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r4-opera-fast vs lim/r1-llava1.5-7b.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.86 / 2.51 (Table S3.3: minimum detectable effect, OPERA-fast vs greedy, LLaVA-1.5-7B, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA-fast & greedy & LLaVA-1.5-7B", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r4-opera-fast vs lim/r1-llava1.5-7b.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.49 [-0.10, +2.96] (Table S3.2: OPERA-fast vs greedy, LLaVA-1.5-7B, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r4-opera-fast vs lim/r1-llava1.5-7b.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.18 / 2.94 (Table S3.3: minimum detectable effect, OPERA-fast vs greedy, LLaVA-1.5-7B, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "OPERA-fast & greedy & LLaVA-1.5-7B", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r4-opera-fast vs lim/r1-llava1.5-7b.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+7.91 [+6.01, +9.87] (Table S3.2: LiM-EOS vs greedy, LLaVA-1.5-7B, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r5-ours-inst vs lim/r1-llava1.5-7b.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.76 / 3.72 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, LLaVA-1.5-7B, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & LLaVA-1.5-7B", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r5-ours-inst vs lim/r1-llava1.5-7b.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.08 [-0.07, +2.25] (Table S3.2: LiM-EOS vs greedy, LLaVA-1.5-7B, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r5-ours-inst vs lim/r1-llava1.5-7b.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.66 / 2.24 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, LLaVA-1.5-7B, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & LLaVA-1.5-7B", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r5-ours-inst vs lim/r1-llava1.5-7b.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+1.42 [+0.24, +2.58] (Table S3.2: LiM-EOS vs greedy, LLaVA-1.5-7B, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r5-ours-inst vs lim/r1-llava1.5-7b.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.67 / 2.25 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, LLaVA-1.5-7B, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & LLaVA-1.5-7B", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r5-ours-inst vs lim/r1-llava1.5-7b.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+6.06 [+4.40, +7.68] (Table S3.2: LiM-EOS vs greedy, LLaVA-1.5-7B, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r5-ours-inst vs lim/r1-llava1.5-7b.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.34 / 3.16 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, LLaVA-1.5-7B, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & LLaVA-1.5-7B", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r5-ours-inst vs lim/r1-llava1.5-7b.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+3.56 [+1.80, +5.38] (Table S3.2: LiM-EOS vs greedy, LLaVA-1.5-13B, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r8-ours-cap vs lim/r7-llava1.5-13b.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.56 / 3.46 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, LLaVA-1.5-13B, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & LLaVA-1.5-13B", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r8-ours-cap vs lim/r7-llava1.5-13b.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.43 [-0.71, +1.57] (Table S3.2: LiM-EOS vs greedy, LLaVA-1.5-13B, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r8-ours-cap vs lim/r7-llava1.5-13b.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.63 / 2.19 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, LLaVA-1.5-13B, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & LLaVA-1.5-13B", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r8-ours-cap vs lim/r7-llava1.5-13b.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+0.36 [-0.75, +1.48] (Table S3.2: LiM-EOS vs greedy, LLaVA-1.5-13B, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r8-ours-cap vs lim/r7-llava1.5-13b.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.59 / 2.14 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, LLaVA-1.5-13B, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & LLaVA-1.5-13B", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r8-ours-cap vs lim/r7-llava1.5-13b.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+2.66 [+1.26, +4.04] (Table S3.2: LiM-EOS vs greedy, LLaVA-1.5-13B, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r8-ours-cap vs lim/r7-llava1.5-13b.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.99 / 2.68 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, LLaVA-1.5-13B, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & LLaVA-1.5-13B", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r8-ours-cap vs lim/r7-llava1.5-13b.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+3.75 [+1.65, +5.86] (Table S3.2: LiM-EOS vs greedy, LLaVA-7B, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r10-ours-cap vs lim/r9-llava-7b.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
3.01 / 4.06 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, LLaVA-7B, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & LLaVA-7B", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r10-ours-cap vs lim/r9-llava-7b.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
-0.20 [-1.21, +0.76] (Table S3.2: LiM-EOS vs greedy, LLaVA-7B, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r10-ours-cap vs lim/r9-llava-7b.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.40 / 1.89 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, LLaVA-7B, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & LLaVA-7B", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r10-ours-cap vs lim/r9-llava-7b.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
-0.19 [-1.27, +0.79] (Table S3.2: LiM-EOS vs greedy, LLaVA-7B, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r10-ours-cap vs lim/r9-llava-7b.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
1.47 / 1.98 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, LLaVA-7B, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & LLaVA-7B", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r10-ours-cap vs lim/r9-llava-7b.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+2.27 [+0.73, +3.77] (Table S3.2: LiM-EOS vs greedy, LLaVA-7B, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r10-ours-cap vs lim/r9-llava-7b.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.18 / 2.93 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, LLaVA-7B, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & LLaVA-7B", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r10-ours-cap vs lim/r9-llava-7b.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+5.69 [+3.36, +8.23] (Table S3.2: LiM-EOS vs greedy, MiniGPT-v2, raw)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r12-ours-cap vs lim/r11-minigptv2.dP_raw.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
3.48 / 4.69 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, MiniGPT-v2, raw; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & MiniGPT-v2", columns of raw	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r12-ours-cap vs lim/r11-minigptv2.dP_raw.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+2.81 [+0.91, +4.67] (Table S3.2: LiM-EOS vs greedy, MiniGPT-v2, matched prefix)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r12-ours-cap vs lim/r11-minigptv2.dP_MCP_prefix.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.69 / 3.62 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, MiniGPT-v2, matched prefix; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & MiniGPT-v2", columns of matched prefix	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r12-ours-cap vs lim/r11-minigptv2.dP_MCP_prefix.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+2.78 [+1.06, +4.50] (Table S3.2: LiM-EOS vs greedy, MiniGPT-v2, sentence tie-average)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r12-ours-cap vs lim/r11-minigptv2.dP_MCP_sent_tieavg.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.46 / 3.31 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, MiniGPT-v2, sentence tie-average; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & MiniGPT-v2", columns of sentence tie-average	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r12-ours-cap vs lim/r11-minigptv2.dP_MCP_sent_tieavg.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
+4.70 [+2.77, +6.79] (Table S3.2: LiM-EOS vs greedy, MiniGPT-v2, uniform random subset)	A	.session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json	pairs_15.lim/r12-ours-cap vs lim/r11-minigptv2.dP_MCP_rand_exact.{est,ci95}	184f9ccac1b9	keyed (POST HOC; supp Table S3.2; fix package v7)
2.87 / 3.87 (Table S3.3: minimum detectable effect, LiM-EOS vs greedy, MiniGPT-v2, uniform random subset; alpha 0.05 and 0.05/15)	A	.session_backup/2026-10-18/paperA_tasks/A8.5/appC_mde.tex	table row "LiM-EOS & greedy & MiniGPT-v2", columns of uniform random subset	ab2d63f5ddf5	DERIVED (80% power, se from pairs_15.lim/r12-ours-cap vs lim/r11-minigptv2.dP_MCP_rand_exact.ci95 of .session_backup/2026-10-13/r10_cpu/e1_x1pb_verification_v2.json; recomputed by apply_a_v7.py and equal to the row; POST HOC; fix package v7)
```


Notes on S1.
- The six interval bounds of Table 5.1 that the sec2-5 read lists (F35) already have rows since fix package v6 (manifest l.3948, l.3954, l.3959), and the draw count of Table 5.1 has rows l.3944-3945. The bounds 0.579 and 37.27 of the supplement read (finding 17) have rows l.69 and l.127; the reader's search was by single value and missed combined rows.
- The count "6 images dropped as unclean" has row l.1327 (`tier3.json :: analysis.n_dropped_unclean`). Row l.1402 is another count of 6 (identifier drops of the exclusion list); neither label needs a change.
- No draw count is added for the condensed-F1 test: `data/results/g2b/an1_score.json` holds no draw-count key, so Section 3.6 does not name that test.

**W4. The `a_m1` result file in the release results (CC-422 W4).** `data/results/a_m1/a_m1_result.json` (sha256 `5687a66b20785c626646d1b54934c590274c4a5244c4cb27150ab6292f00dcb4`; tracked and clean in the run repository, last commit `a245481`) is copied byte for byte to `results/data/results/a_m1/a_m1_result.json` of the paper repository, and one row is added to `PROVENANCE.md` after the row of `results/data/results/a_g0/g0.json`:

`| results/data/results/a_m1/a_m1_result.json | data/results/a_m1/a_m1_result.json | clean | a245481 | 5687a66b…dcb4 | cited by draft |` (with the backticks of the table).

The file holds 20 strings (labels, states and hashes), no caption text, no path, no address; the script asserts it. 19 manifest rows of fix package v6 point to this file.

**S2. Published supplement and provenance table.** `supplementary_SPIC.md` and `supplementary_provenance_internal.tsv` are produced from the changed `supplementary.md` by `scrub()` of `paper/build/scrub_supp.py`, as in v6. S11 is bounded by the next level-2 heading (CC-422 N2); its bytes are asserted unchanged in both files.

**S3. Length comment.** The comment block before the abstract in `abstract_A.md` gets the new word counts ("recounted after fix package v7"). The abstract itself is byte-unchanged (asserted).

## 5. The registered third sentence of Section 6.4 (sec6-11 read F01; CC-412 N1)

**Fact.** The registration of the PASCAL-50S test (§9, heading: "inserted as written once there is a verdict") fixes three sentences for the outcome that occurred (§9.2, l.379). Section 6.4 (`sec7_verbosity_sign.md` l.86) prints the first two. The third is a caution on the pretraining data of the evaluated models.

**The investigator's lines.** PI-1105m (LOG l.1614), answering PQ1 of CC-262: caveats of the kind "models may have seen these images" are dropped, and one neutral sentence is kept. PI-1106a (l.1622): the same wording is to be removed from `declarations.md` and `supplementary.md` in that same revision. The neutral sentence stands in Supplementary S7 ("We did not examine the pretraining data of the evaluated models."). PI-1110n (l.2070) later replaced the overlap rule PI-1101o by "state the fact only where the overlap affects reported statistics"; it does not ask for the caveat back.

**Conclusion.** The present wording of the main text was decided by the investigator. The sentence is therefore NOT restored. The package records the departure instead:
- **A7-G01b (default).** A paragraph in Supplementary S4 says that the registered text has three sentences, that Section 6.4 prints two, what the third concerns, and that S7 carries the neutral sentence. It does not print the registered sentence, because PI-1106a removed that wording from the supplement.
- **A7-G01a (alternative, in SKIP).** The same paragraph with the registered sentence quoted word for word, as the coordinator's task text asked. It is switched off because quoting the sentence puts back into the supplement the wording that PI-1106a had removed; only the investigator can decide that. To use it, put `A7-G01b` in SKIP in place of `A7-G01a` and take the targets of the ruling.
- **A7-G02.** Section 6.4 says "Two departures from the registration"; with the record it would be incomplete, so the sentence names the third, a departure in wording.
- **A7-G03.** The unprinted source comment of the paragraph no longer says "inserted as written" without qualification.

My recommendation is A7-G01b with A7-G02 and A7-G03 (confidence about 80%). The same check for the COCO val2017 paragraph found no missing registered sentence (sec6-11 read, Section 4, last paragraph); nothing is changed there except the opening clause, which the paragraph already says is not the registered wording (A7-M50).

## 6. Findings that did not become a block as written

### 6.1 Dropped or changed, with the reason

| Finding | What was done | Reason |
|---|---|---|
| sec2-5 F04 | no block | The sentence describes the method of S11.1; it is read with S11 (Section 6.3). The open check of the supporting passage is item I-5. |
| sec2-5 F07 | dropped | The journal build prints numbered citations (`build_A_cas.sh`, step `numcites`); no author-year copy is built, so the "a" and the initial are never printed. |
| sec2-5 F10 | dropped | One table-numbering scheme for the whole paper is a layout choice for the rewrite; no label is wrong. |
| sec2-5 F12 | changed | Definitions written from the paper's own sentences; "COCO-2500 val2017 images" replaced by "COCO val2017 images drawn from COCO-2500". |
| sec2-5 F17 | changed | The false sentence "Every table names its matcher" is removed in the main text and in S2; no caption was given a vocabulary, because the vocabulary of each row of Table 5.1 was not verified here. |
| sec2-5 F19 | changed | "we model"; no pointer added, because no place reports a fit of the power law itself. |
| sec2-5 F25 | dropped | Renaming a symbol touches Section 3, S2, S3 and the figures; for the rewrite. |
| sec2-5 F27 | partly | Three rows added; the Table 5.1 count already had rows (v6). |
| sec2-5 F28 | partly | Eight-LVLM test and Section 5.4 added; the condensed-F1 count has no key in its result file. |
| sec2-5 F35 | dropped | Already in the manifest since v6 (l.3948, l.3954, l.3959). |
| sec2-5 F38 | changed | Both printed to two decimals from the source (1.993 [1.967, 2.02]). |
| sec2-5 F41 | no block | A sentence on the held study (Section 6.3). |
| sec6-11 F01 | changed | Recorded as a departure, not restored (Section 5). |
| sec6-11 F06, F07 | no block | The OLD text stands inside a sentence that also reports the held study (Section 6.3). |
| sec6-11 F09 | changed | The reason for "approximate" is taken from Supplementary S7; the two fixed sentences stay word for word and are not put in quotation marks. |
| sec6-11 F13, F17, F37, F38, F39, F42 | no block | Lines 15-31 of Section 9.1 describe the held study and will be rewritten with it (Section 6.3). F17 also needs a fact from the investigator (I-3). |
| sec6-11 F14, F16 | no block | Decisions of the investigator (I-1, I-2). |
| sec6-11 F21 | changed | The bold registered label is not reworded; only the four gold variants are named after it. |
| sec6-11 F26 | changed | "fixed cap", not "pre-fixed": the word of the present text is kept. |
| sec6-11 F27 | partly | The added sentence naming the two Qwen-family models is not written (no source read for it). |
| sec6-11 F33 | changed | "the interval of its withdrawal rule", without the added word "registered". |
| sec6-11 F34 | partly | The COCO val2017 clause is added; splitting the paragraph is layout for the rewrite. |
| sec6-11 F35 | partly | Second half done (A7-M64); the first half is inside a held sentence. |
| sec6-11 F44 | dropped | "penalize" in Section 7.1 is inside a bold registered label and "penalising" is registered wording of X4; one spelling for the paper is a choice for the rewrite. "judgements" is in l.19 of Section 9.1 (held lines). |
| sec6-11 F45 | changed | Two rows added; the label of row l.1402 is right for its own count (see notes on S1). |
| sec6-11 F46 | dropped | No change until the guide for authors is read (audit A5-09). |
| supplement 2 | closed | Done at `a7f2b4e`; the form of the citation and the spelling are in this package. |
| supplement 4 | no block | The fit file `cf_r4_full5000_all9.json` (`39e64bdbbdf8`) holds four fitted points (`obs_b2to5`, `pred_b2to5`), which supports "four", against "five" in two other sentences. Whether the one-reference point entered the fit is not in the file: item I-6. |
| supplement 5 | no block | Two keys give 1.24 (`h4_r4_full5000_all9.json :: T2_microF1_randk.1.Mstar_micro`) and 1.38 (`w4_summary.json :: P3_refs1.Mstar_micro`); the clause that explains the difference needs the authors (I-6). |
| supplement 6, 7, 8, 9, 14, 16 | no block | Structural; proposal for the cut plan (Section 6.4). |
| supplement 10, 11 | changed | The promise is removed (titles and pointers); no content is added. |
| supplement 12 | no block | Outcomes (i) and (ii) must be defined in the words of the design file; not located in this pass (for an agent, with the design of the precision bracket). |
| supplement 13 | no block | Renaming the labels of S1.M must be done together with S11, which may use them (Section 6.3). |
| supplement 17 | changed | Rows added for 16% and the rounded interval; 6.03, 5.27, 4.67 and 3.36 are now cells of Table S3.2 with rows; 0.579 and 37.27 had rows. |
| supplement 18 | no block | Citations by identifier need new entries in the reference list; done when the list is rebuilt (CC-422 W3 (c)). |
| supplement 22 | partly | "kill interval" (two places) and "tier-1 power rule" replaced; the other internal terms stand in S7 "Extended text" and S10 (Section 6.4) or need facts (what a "hit" is). |
| supplement 23 | no block | The two variants ("links", "entries") must be described from `sensitivity.json`; not read here. |
| supplement 26 | no block | Definitions of the columns of Table S8.1 must come from the registration of that test. |
| supplement 27, 28, 29, 30, 45, 46 | no block | Captions, callouts, table order, abbreviations, typography: for the rewrite, after the cuts of Section 6.4 (renumbering the tables of S7 would also change six pointers of the main text). |
| supplement 33 | no block | 1.6000 and 1.61 are two keys (the registered all-image gold size; `bracket_result.json :: sets.s75.mean_gold_size.refs1_randk` = 1.6066); the clause that explains them needs the authors (I-6). |
| supplement 34 | dropped | Both sentences name their baseline (beam search; greedy decoding), and Table S3.2 now shows the two rows. |
| supplement 35 | no block | The ninth checkpoint must be named from the registration of the leaderboard. |
| supplement 37 | partly | Pointer corrected; the repeated last sentence stays. |
| supplement 43 | partly | Done in the main text (A7-M42); the S10 copy is in the cut proposal. |
| supplement 44 | no block | The three values of the secondary measure were not read. |

### 6.2 Left for the investigator and the authors

- **I-1 (sec6-11 F14).** Will the new human labels for XM3600-600 be released? One sentence is then needed in Section 9.2 and in the Data availability statement. My recommendation: decide at the deposit; until then the present sentence of Section 9.2 is true.
- **I-2 (sec6-11 F16).** "It uses the same fine-tuned instrument" (Related manuscripts): name the instrument (the matcher, or the adapters). Depends on the statements for the companion manuscript, which wait for the submission dates.
- **I-3 (sec6-11 F17).** "a rehearsed assessment of the method": say in plain words what the annotator was told. Only the people who sent the message know it.
- **I-4 (Section 5).** Confirm the record of the third registered sentence in the form A7-G01b, or choose A7-G01a.
- **I-5 (open reference checks).** Karlin (1968): no section is cited. Esary, Proschan and Walkup (1967): the place of the product inequality in the paper was not checked. Fernández-Barrios et al. (2026): identity from the abstract page only; no recorded passage for "for F1 with single-label items". An author with access to the full texts should check the three.
- **I-6 (facts only the authors have).** Four or five fitted points in S1 (supplement 4); the two values of the one-reference optimum, 1.24 and 1.38 (supplement 5); the two one-reference gold sizes, 1.6000 and 1.61 (supplement 33).
- **I-7 (style, at the rewrite).** One table-numbering scheme; one spelling (-ise or -ize); the symbol $B$ used for the comparator and for the draw count.
- **For the coordinator.** (a) CC-422 W3 stays open (cover letter, reference list rebuild after the S11 update). (b) `mde.json` and `build_a8_5_mde.py` (`.session_backup/2026-10-18/paperA_tasks/A8.5/`) are not in the paper repository; the committed `appC_mde.tex` is the source used here, and the script recomputes its values, so nothing blocks; adding the two files to the release would let a reader re-run them. (c) In Table 1 the row that holds X-22 to X-25 gives Sections of the main text as their place, while Table S4.0 says "this table only"; not changed. (d) `outline.md` still lists the old section plan; it is not built.

### 6.3 Left for the update of Section 6.7 and S11 (place only)

- `sec7_verbosity_sign.md` from the heading of Section 6.7 (l.124) to the end.
- `supplementary.md` and `supplementary_SPIC.md`, S11 (from its heading to the heading of the reference list).
- `cover_letter_A.md:13`.
- `abstract_A.md`, the abstract paragraph; `highlights_A.md`.
- `sec1_introduction.md:49` (Table 1, last row).
- `sec2_related_work.md:12` (the sentence that points to Supplementary S11.1; sec2-5 F04).
- `sec5_exchangeability.md:43` (last sentence; sec2-5 F41).
- `sec7_verbosity_sign.md:57` (the sentence that ends with the pointer to Section 6.7.2; sec6-11 F07 is inside it).
- `sec10_discussion.md:7` (last sentence).
- `sec10_discussion.md:29` (four sentences; sec6-11 F06 and the first half of F35 are inside one of them).
- `sec11_limitations_ethics.md:11` (last sentence).
- `sec11_limitations_ethics.md:15-31` (design and limits of the held study; sec6-11 F13, F17, F37, F38, F39, F42 and "judgements" of F44).
- `declarations.md:27` (first sentence).
- Table S4.0 of the supplement, rows A31 to A37, D-1 to D-4 and P-5, and two sentences of S10 (named by the supplement read; not displayed here).
- Supplementary S1.M, the labels (A1) to (A4) (supplement 13), to be renamed together with S11.

### 6.4 Proposal for the cut plan (not in this package)

The supplement read proposes cuts that would close its findings 6, 7, 8, 9, 14 and 16 and most of 22, 27 to 30 and 46. None is made here. Proposal, for a separate ruling:

1. **S10 "Extended text for Sections 1 to 9" (published l.1010-1171).** Cut every paragraph that repeats the main text or another part of the supplement; keep only paragraphs that hold a number or a disclosure printed nowhere else, moved to the part they belong to. This removes the eight uses of "ordered by gold completeness", the four statements that the PASCAL-50S label premise "was assumed, not measured", the "Earlier caption of Table 1 / 5.1 / 6.1" paragraphs, the note at l.1012 and the fragments listed in finding 16.
2. **S7, the second half ("Extended text", published l.811-886).** Keep Table S7.8 and its three paragraphs (the main text points to them); cut the paragraphs that give an earlier, longer wording of Sections 6.2 to 6.5, and the note at l.813.
3. **S9 "Longer wording of Section 2" (published l.981-1008).** Cut; keep "Extended related work" (l.965-979).
4. **Duplicates inside S1 to S8 (finding 8).** Of each pair keep the longer version: S1 l.15 and l.62, l.36 and l.40; S2 l.158-163 and l.167-172; S3 l.232 and l.248, l.236 and l.250, l.244 and l.254; S4 l.332 tail and l.405 tail, l.403 and S6 l.566; S5 l.428-430 and l.464-466, Table S5.2 inside Table S5.1, l.445 and l.485, l.447-448 and l.489-490; S6 l.538 and l.568; S7 l.587-590 and l.734, l.742 and l.825, l.744 and l.838, l.746 and l.842; S8 l.902-904 and l.939-941, l.906 and l.951.
5. **After the cuts:** the self-pointers (finding 9), the order of the tables of S7 (finding 29) and the run-in heads (finding 16) in one pass, with the pointers of the main text.

Each cut must first be checked for numbers that are keyed only to the cut paragraph (manifest rows whose status names S10) and for pointers from the main text.

## 7. Verification

### 7.1 Check mode against HEAD `a7f2b4e`

```
HEAD a7f2b4e | base a7f2b4e is HEAD or an ancestor | SKIP ('A7-G01a',)
blocks applied: 104 of 105 (each OLD once at HEAD; no NEW at HEAD outside its OLD); Tables S3.2 and S3.3 rebuilt from the result file and equal to the package
S1: 129 manifest rows; the sha256 prefix of each source file equals the file in the run repository
W4: data/results/a_m1/a_m1_result.json copied to results/ (sha256 5687a66b2078, 19 manifest rows point to it) and one PROVENANCE row added
S2: published supplement = scrub(source); S11 bytes unchanged in both files; leak hits only inside S11
main text words: 19284 -> 19746 {'sec1_introduction.md': 8, 'sec2_related_work.md': 51, 'sec3_measurement_setup.md': 108, 'sec4_theory.md': 6, 'sec5_exchangeability.md': 13, 'sec7_verbosity_sign.md': 220, 'sec8_human_validity.md': 12, 'sec10_discussion.md': 24, 'sec11_limitations_ethics.md': 6, 'declarations.md': 14}
custody: Section 6.7, S11, the abstract body, Section 9.1 l.15-31 and Section 1 outside l.48 byte-unchanged; cover letter, highlights, title page and anonymised declarations not written; 11 sentences on the held study in 6 other lines unchanged; 0 shared runs of 8 words with Section 6.7, S11, the printed abstract, the highlights; agreement clauses unchanged in every file
OK    ../PROVENANCE.md ee19795c2de5a872734a0587b9dcb4c670a79a77ed32cdd44cdf40f97c95382e
OK    ../results/data/results/a_m1/a_m1_result.json 5687a66b20785c626646d1b54934c590274c4a5244c4cb27150ab6292f00dcb4
OK    abstract_A.md 5b3b482617ac75cc8942dea045e4e713300da207699c779ac334adb50479af41
OK    declarations.md 8a34830ceedf189ae4ef4091814aa10162c3e9125ddee42376cd9559f433b603
OK    number_manifest.tsv 1b0f01fca69856666391186d86b0d40c47ba9bec842679f38c9c93b831f10b3f
OK    paperA.bib 753a2a5269458c8bb93027fd6460cb58b8df7d87ba5eee4e759e531a27e7fd30
OK    sec10_discussion.md 5ec1a049e04fdaf83384570ee4b229ed3c8dd9b5480cb90ac75cf7ae2e676bcb
OK    sec11_limitations_ethics.md 0d1d409afcf08d4eb1095a0d60af4ca328a2f98e84da4ebcde830ad9721d8e3d
OK    sec1_introduction.md 1a7f0851df9ee79f66296531d6d9e59e8ebefd16f833453a5f3e32ba0e7e1aa8
OK    sec2_related_work.md 29d97036fa4015079a519484304c59094cd21aaefcb40e9d486ba3b28d79ea8b
OK    sec3_measurement_setup.md ba8c15a499a34396a20b5b2a9010d122eadda762c3aca1988c9371620be5e3e7
OK    sec4_theory.md 11a0e672302a3b0d06073f9e4890198f209bc982253b02694ff9c2ecc49ff5fa
OK    sec5_exchangeability.md ea3d21cf50430631a05fbd369d3d7cf3b01c114ebe122c407e571597a5a090cd
OK    sec7_verbosity_sign.md 0d823927e932868a7883a59751b780f7545a8ec2bb8dfa5c26fe9e3b50a5e9b2
OK    sec8_human_validity.md 539f58d45c1c90e8629b272cccb43e51f7aeb530fea6e76e0ada477021194d2b
OK    supplementary.md ad2213823a139ccf91b2d4650001916620b5a6a78413162ac7fc860cf4361ce5
OK    supplementary_SPIC.md c6a5229ec213de72f9198a55d1b0950dce48f7f730f071eefb82a48ae014ef5d
OK    supplementary_provenance_internal.tsv 46addaa25bbab9f3aff2b0f52101bc034d7ba53d5e0ab92b26c9d2a409218f06
ALL RESULTS EQUAL TARGETS
CHECK MODE: nothing written
```

### 7.2 Write mode on a scratch clone, and the journal build

```
Scratch clone of the paper repository at a7f2b4e (session scratch folder, not a repository of record):
  python3 -I -B apply_a_v7.py --repo <clone> --write --ruling SCRATCH-TEST
  -> ALL RESULTS EQUAL TARGETS; 18 files written to the clone (17 changed, 1 new); nothing staged.
Main text, build/build_A_cas.sh on the clone (pandoc, xelatex; output in the scratch folder; the PDF was not opened):
  39 pages; undefined references and citations 0; missing characters 0; 17 overfull boxes (17 before this package);
  78 entries in the reference list; the entry of Bui et al. (2026) is in the list; "Pont-Tuset" in the Crossmodal-3600 entry.
Supplement, build/build_A_supp.sh on the clone:
  160 pages (158 before this package); undefined references 0; missing characters 0; 77 overfull boxes (72 before;
  the 5 new ones are counted, not located: Tables S3.2 and S3.3 have 8 and 7 columns).
```

### 7.3 What the script asserts

- Every OLD occurs once at HEAD and once when its block is applied; no NEW stands at HEAD outside its OLD; a block changes the printed text unless it is the one comment-only block (A7-G03).
- Blocks in `sec7_verbosity_sign.md` end before the heading of Section 6.7; blocks in `supplementary.md` lie before the heading of S11 or after the heading of the reference list.
- Byte-unchanged: Section 6.7 to the end of its file; S11 in both supplement files; the abstract paragraph and everything after it; lines 15-31 of Section 9.1; every line of Section 1 except l.48. Not written: cover letter, highlights, title page, anonymised declarations.
- In the six other lines that hold a sentence on the held study, each such sentence stands unchanged in the result.
- No run of 8 words of Section 6.7, S11, the printed abstract paragraph or the highlights occurs in this file or in the script.
- The count of the printed clause "agreed to this use" is unchanged in every file; no NEW holds wording on AI tools.
- Tables S3.2 and S3.3 and their 120 manifest rows are rebuilt from the two source files and must equal the text of this file; the column means of Table S3.2 equal the means printed in Table S3.1.
- Write mode writes only if every result equals TARGETS, and never stages.
