# Paper A fix package v4

Written 2026-11-15T02:39Z (2026-11-15, 09:39 Vietnam time). Target journal of the paper: Signal Processing: Image Communication.

**What this file is.** Proposed text changes to Paper A in three groups that a judge can rule on, and skip, separately. Each change is an exact OLD/NEW pair with its evidence. Nothing has been applied, staged or committed. The package is outcome-free with respect to Section 6.7 and Supplementary S11: it quotes no figure and no verdict of that study, so no `*_HELD.md` file was needed.

**Inputs.**
- Paper: `/mnt/d/vsps_papers/vsps-paperA-spic/paper/`, written against commit `ea12e51` (package v2 applied under the revised CC-407) and checked against HEAD `ff6ca80`, which differs from `ea12e51` only in `sec2_related_work.md` (related-work corrections under CC-411). The working tree of `paper/` is clean.
- Ruling `CC-407`, revised text (sha256 9b64d381...), read in full: open items W4, W5, W6 and N1 to N9.
- Answer F4, option (d), of the corresponding author in `manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_c769713f.md` (only section F4 was read; no name, identifier or address from that file is copied here), and LOG line OPS-1115f-author-f4-f6, which takes that option on two conditions.
- The four registrations that name the ordering tests, the result files behind every figure of group C, and the run records of the two UIT-ViIC adapters (Section 7.5 lists what was opened).
- The decisions LOG and `manuscript/directions/integrity_2026-11-10/FIX_RESOLUTIONS_2026-11-10.md`, searched for earlier PI lines before every block that touches a declaration, a data statement or a permission clause; the lines found are cited in the evidence of those blocks. No block reverses a PI decision; group U proposes a change to wording that a PI decision set, and for that reason is not to be applied without him.

**The three groups.**
- **Group C (claim wording; answer F4, option (d)).** 4 items, 5 blocks (A4-C02 and A4-C03 are one item). Section 1 (text and Table 1), Section 6.4 and Section 8.1. The abstract, the highlights and the cover letter are not touched.
- **Group U (CC-407 W4, UIT-ViIC). NEEDS THE INVESTIGATOR: not applied without his decision.** 5 items, 7 blocks. A truthful statement that two adapters were trained on the UIT-ViIC training split and are four of the ten systems of the UIT-ViIC rows. The present wording was set by PI-1029p item (5). No agreement or permission clause is written.
- **Group N (CC-407 N1 to N9).** 4 items, 9 blocks: N1, N2, N4 and N9. N3, N5, N6, N7 and N8 need no block (Section 5.3).

Section 6.7 and Supplementary S11 stay byte-unchanged; Section 6.4 lies in the same file as Section 6.7, and the apply script asserts that the file is unchanged from `## 6.7` to its end. `sec2_related_work.md` is not touched (Table 2.1 belongs to another package).

## 1. Counts

- 21 blocks: group C 5, group U 7, group N 9. In group U two items touch both supplement files (`a` = `supplementary.md`, `b` = `supplementary_SPIC.md`); in group N item N09 has six blocks, `a` to `f`, one per unprinted comment.
- 3 steps that are not blocks: S1 two manifest rows (group U only), S2 the regenerated provenance table (groups U and N), S3 the length block (every combination).
- Deferred: 5 items (Section 6.1). For the investigator: 6 items (Section 6.2). For the judge: 6 points (Section 6.3).
- Main text: 18,927 words at HEAD. Group C +218, group N +6, group U +134; after C+N 19,151 (+224); after all three 19,285 (+358).

## 2. Table of blocks

| Id | Group | Source | File | Line at HEAD | What changes |
|---|---|---|---|---|---|
| A4-C01 | C | F4 (d) items 2, 3 | `sec1_introduction.md` | 11 | Section 1: heading and first sentence name the registered ordering prediction; one scope sentence added |
| A4-C02 | C | F4 (d) item 2 | `sec1_introduction.md` | 43 | Table 1, first row: the two passing ordering tests and the failed PASCAL-50S replication side by side |
| A4-C03 | C | F4 (d) item 2 | `sec1_introduction.md` | 47 | Table 1, FAIL row: A24 named by reference to the first row; the count stays 9 |
| A4-C04 | C | F4 (d) item 2 | `sec7_verbosity_sign.md` | 86 | Section 6.4: registered branch text untouched; one sentence added that marks it as registered text |
| A4-C05 | C | F4 (d) item 2 | `sec10_discussion.md` | 7 | Section 8.1: label of the first result names the registered ordering prediction and its scope |
| A4-U01 | U | W4 | `declarations.md` | 19 | Data availability: training of two adapters on the UIT-ViIC training split stated; "used only through" becomes "appears only as" |
| A4-U02 | U | W4 | `anon/declarations_anon.md` | 10 | Anonymised copy: same statement |
| A4-U03 | U | W4 | `sec11_limitations_ethics.md` | 44 | Section 9.2: same statement; the UIT-OpenViIC clauses unchanged |
| A4-U04a | U | W4 | `supplementary.md` | 661 | Supplementary S6: same statement (a fourth place with the old wording) |
| A4-U04b | U | W4 | `supplementary_SPIC.md` | 542 | Supplementary S6: same statement (a fourth place with the old wording) |
| A4-U05a | U | W4 | `supplementary.md` | 734 | Supplementary S7: the ten UIT-ViIC systems named |
| A4-U05b | U | W4 | `supplementary_SPIC.md` | 592 | Supplementary S7: the ten UIT-ViIC systems named |
| A4-N01 | N | N1 | `sec10_discussion.md` | 19 | Section 8.3, checklist item 3: one pointer to Section 3.3 in place of two |
| A4-N02 | N | N2 | `sec3_measurement_setup.md` | 52 | Section 3.6: "$B$ = 1,000" written in the style of the paragraph |
| A4-N04 | N | N4 | `declarations.md` | 19 | Data availability: KTVIC taken out of the list whose reason is "licences and terms of use"; its captions still not redistributed |
| A4-N09a | N | N9 | `declarations.md` | 19 | declarations.md, unprinted comment: "written acceptance" brought in line with PI-1110o |
| A4-N09b | N | N9 | `declarations.md` | 19 | declarations.md, unprinted comment on PASCAL-50S: the pending confirmation replaced by the PI's decision |
| A4-N09c | N | N9 | `declarations.md` | 19 | declarations.md, unprinted comment quoting the planned PASCAL-50S sentence: note that the printed clause differs |
| A4-N09d | N | N9 | `sec11_limitations_ethics.md` | 44 | Section 9.2, unprinted comment: same |
| A4-N09e | N | N9 | `supplementary.md` | 658 | supplementary.md S6, unprinted comment: same |
| A4-N09f | N | N9 | `supplementary.md` | 1350 | supplementary.md S10, unprinted comment: same |

## 3. Blocks

Each OLD string is given exactly as it stands in the file at HEAD, and each NEW string exactly as it should stand. A marker line is not part of a string; the string is the text between two marker lines, without the line break before the next marker. Every string is a single line. A4-C02 and A4-C03 are one item and are applied together or not at all; the same holds for each `a`/`b` pair of group U.

### Group C: claim wording (answer F4, option (d))

<<<A4-C01 sec1_introduction.md OLD>>>
**The confirmatory claim.** Our one confirmatory claim is that object F1's verbosity slope is **ordered from one reference to all references to verified labels**. It rests on a registered test on one image set,
<<<A4-C01 sec1_introduction.md NEW>>>
**The registered ordering prediction and the scope of its support.** The central registered prediction of this paper is that object F1's verbosity slope is **ordered from one reference to all references to verified labels**; where later sections and the registered texts they quote speak of the confirmatory claim, they mean this prediction as tested on XM3600 and with the second backbone. Its support is limited to those tests: the ordering passed on XM3600 with two Qwen-VL backbones and holds in all 6 post hoc leave-one-system-out fits there (Section 6.5), whereas with other label golds the evidence is mixed, because the registered PASCAL-50S replication failed at its VOC label step (post hoc label-to-reference size ratio 0.83) and on COCO val2017 the label-gold slope exceeded the one-reference slope (+35.46 points) but the step against five references did not meet its registered size premise (Section 6.4). The ordering rests on a registered test on one image set,
<<<A4-C01 EVIDENCE>>>
Source: answer F4, option (d), of the corresponding author (`manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_c769713f.md`, section F4; only that section was read). Item (2) asks for a heading that names the registered ordering prediction and the scope of its support in place of "Our one confirmatory claim"; item (3) asks for one scope sentence. Registration wording (run repo, `manuscript/prereg/`): (i) XM3600, `2026-10-14_xm3600_predictions.md` (sha256 prefix 1dfaeb0f6d1b) l.60-61: under "Relative-form predictions", "`N1-XM-4 (Ordering)`: slope(refs1_randk) < slope(refs_all) < slope(oiv7_verified)"; that file gives the test no tier and uses neither "primary" nor "confirmatory". (ii) Second backbone, `2026-10-18_g2b_qwen3vl_ladder.md` (2e6b3e871144) l.193: "G2B-O1 | primary | cv295, uv231, xm600 | ordering (Proposition 1): slope(one reference) < slope(all references) < slope(complete gold)"; verdict rules l.176 (`sign_gt_0`: PASS if ci95_lo > 0; FAIL if point <= 0; else INCONCLUSIVE) and l.180 (`compound`); l.216 "Every registered verdict is quoted as the evaluator computed it (PASS, FAIL, INCONCLUSIVE or NOT_EVALUABLE)". (iii) PASCAL-50S, `2026-10-28_pascal50s/PREREG.md` (1448ab13fcb5) l.225: "P50-A4 | primary (replicates A4) | slope(refs1_randk) < slope(refs50) < slope(voc20), on the V20 vocabulary", compound; l.235 "primary family {P50-A4 (2 parts)}"; verdict rules l.215-216 and l.230; branch text §9.2 l.379; l.384 "Every branch: Table 1 gets a new row, with the verdict copied from the decide file." (iv) Companion protocol, `2026-10-29_a_companion/RULE.md` (082c71badcb2) l.89: "Companion confirmatory family: {X4, X5}". Reading: the one registered text that calls the XM3600 and second-backbone tests "the confirmatory claim of this paper" is the PASCAL-50S branch text (l.379), and it calls the PASCAL-50S test "a failed out-of-sample replication"; the tier word "primary" belongs to G2B-O1 and to P50-A4, not to N1-XM-4. This is the case the brief foresees, so the new headings are neutral ("registered ordering prediction", "ordering tests (registered)"), the registered words stay where they stand, "primary" is printed only for the PASCAL-50S test, as Table 1 prints it at HEAD, and the verdict words are PASS and FAIL as in the decide files. Departures from the wording of the answer: "prediction" in place of "hypothesis" (the registrations and Table 1 say predictions) and no "Primary" in the heading (N1-XM-4 has no tier). "Confirmatory" keeps its methodological sense: the new first sentence says what later sections and the registered texts mean by "the confirmatory claim" (`sec7_verbosity_sign.md` l.5, l.86 (registered text) and l.104; `sec11_limitations_ethics.md` l.9; Supplementary S4 and Table S4.0), and "The confirmation supports the empirical pattern" (same paragraph) and "No count-control result is confirmatory" (l.13) are unchanged. "It rests on" becomes "The ordering rests on", because after the inserted sentence "It" would have no clear referent. Figures, each already printed in Section 6.4, Section 6.5 or Table 1 and re-read by the builder from its result file: XM3600 ordering PASS: `.session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json` (0b2b3aa5e1a3) :: prereg_comparisons[19].in_interval_or_pass = PASS (N1-XM-4); manifest l.243; second backbone PASS on 537 images: `data/results/g2b/g2b_score.json` (68be2b7a0904) :: datasets.xm600.predictions.G2B-O1 (both parts PASS, n_images = 537); manifest l.927, l.928, l.931; PASCAL-50S FAIL, -2.29 [-5.15, +0.61]: `data/results/p50/p50_decide.json` (0da4cab90fe9) :: analysis_set.P50-A4.verdict = FAIL, parts[1].{point = -2.2885, ci95 = [-5.1506, 0.6123], verdict = FAIL}; manifest l.1084 to l.1088; 0.83: `data/results/a_g0/g0.json` (23e12cbd179e) :: ratio_voc_over_ref = 0.8265 (1,787 / 2,162; post hoc descriptive, no verdict); manifest l.1252; +35.46 and the size premise: `data/results/a_t3/tier3.json` (5735bd20f26b) :: analysis.AD1p.{point = 35.4553, verdict = PASS}, analysis.L_vs_R5.verdict = PREMISE_NOT_MET, analysis.premise.L_over_R5 = 1.3947 (< 2); manifest l.1333, l.1336, l.1352, l.1353; 6 of 6 leave-one-system-out fits: `data/results/a1_robustness/loo_triples.json` (d74f34c431fb) :: xm3600_loo_n_ordered = 6, xm3600_loo_n_drops = 6 (DERIVED, POST HOC); manifest l.1067. The clause "dropping the verbose system flips the reference signs" of the answer is not repeated here because the same paragraph already states it with its figures. Earlier PI line on the same point: PI-1029m (decisions LOG l.756: PASS headline; registered test FAILs are still reported briefly and not hidden). The block does not reverse it: the abstract, the highlights and the cover letter are unchanged, the passing tests keep the first place, and the failure it names is already printed in this paragraph and in Table 1. The choice of answer F4 option (d) for this package is LOG line OPS-1115f-author-f4-f6 (l.2639), on two conditions: the names of the registration stay verbatim and every figure is re-checked.

<<<A4-C02 sec1_introduction.md OLD>>>
| Confirmatory, PASS | Slope ordered one reference < all references < verified labels on XM3600 (A4) and with a second backbone on 537 of the same images (A6) | 6.2, 6.3 |
<<<A4-C02 sec1_introduction.md NEW>>>
| Ordering tests (registered): PASS on XM3600 and with a second backbone; FAIL in the PASCAL-50S replication | Slope ordered one reference < all references < verified labels: PASS on XM3600 (A4) and PASS with a second backbone on 537 of the same images (A6). Out-of-sample replication on PASCAL-50S (one reference < 50 references < VOC labels; primary): FAIL at its label-gold step, −2.29 [−5.15, +0.61] (A24; counted once, among the nine of the FAIL row) | 6.2–6.4 |
<<<A4-C02 EVIDENCE>>>
Source: answer F4, option (d), of the corresponding author (`manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_c769713f.md`, section F4; only that section was read). Item (2): the first row of Table 1 lists the passing tests and the failed out-of-sample replication side by side, with a cross-reference to the nine failures so that nothing is counted twice. Registration wording and lines: as in the evidence of A4-C01 (N1-XM-4 has no tier; G2B-O1 and P50-A4 are "primary"; the verdict words PASS and FAIL come from the decide files). Ledger ids as in Supplementary Table S4.0 (A4 = N1-XM-4, A6 = the second-backbone primary claims, A24 = P50-A4). Figures: XM3600 ordering PASS: `.session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json` (0b2b3aa5e1a3) :: prereg_comparisons[19].in_interval_or_pass = PASS (N1-XM-4); manifest l.243; second backbone PASS on 537 images: `data/results/g2b/g2b_score.json` (68be2b7a0904) :: datasets.xm600.predictions.G2B-O1 (both parts PASS, n_images = 537); manifest l.927, l.928, l.931; PASCAL-50S FAIL, -2.29 [-5.15, +0.61]: `data/results/p50/p50_decide.json` (0da4cab90fe9) :: analysis_set.P50-A4.verdict = FAIL, parts[1].{point = -2.2885, ci95 = [-5.1506, 0.6123], verdict = FAIL}; manifest l.1084 to l.1088. Must be applied together with A4-C03 (otherwise the value of A24 would stand in two rows). For the judge: the registration line l.384 ("Table 1 gets a new row") was met at HEAD by the FAIL row and by row A24 of Table S4.0; after this block A24 stands in the first row with its verdict word copied from the decide file and stays in the FAIL row by reference. The registered sentence of Section 6.4, "the label-gold part is listed in Table 1 as FAIL", stays true. PI-1029m and LOG line OPS-1115f: as in A4-C01.

<<<A4-C03 sec1_introduction.md OLD>>>
| FAIL (9) | PASCAL-50S primary at its label-gold step, −2.29 [−5.15, +0.61] (A24); XM3600 all-references sign (A2)
<<<A4-C03 sec1_introduction.md NEW>>>
| FAIL (9) | PASCAL-50S primary, the ordering replication of the first row (A24); XM3600 all-references sign (A2)
<<<A4-C03 EVIDENCE>>>
Pair of A4-C02. The FAIL row keeps its count: the ledger ids in the row are the same nine before and after (A24, A2, A5, A10, A14, A15, A18, A19, A21; counted by the builder), and A24 is named once with its figures (first row) and once by reference (this row). "primary" is the tier of P50-A4 in its registration (`2026-10-28_pascal50s/PREREG.md` l.225) and stood in this row at HEAD. The count sentences elsewhere ("nine registered predictions failed (Table 1)", Sections 1 and 8.5) are unchanged.

<<<A4-C04 sec7_verbosity_sign.md OLD>>>
and the verdicts can be recomputed by re-running the pinned job (Section 9.2).<!-- rev4 (A_SPIC_2026-11-03 META_REVIEW item 1, 13;
<<<A4-C04 sec7_verbosity_sign.md NEW>>>
and the verdicts can be recomputed by re-running the pinned job (Section 9.2). The first two sentences of this paragraph follow the registered text for this outcome, with its blanks filled and the section number updated; "the confirmatory claim" in them is the registered ordering prediction of Section 1, tested on XM3600 and with the second backbone.<!-- rev4 (A_SPIC_2026-11-03 META_REVIEW item 1, 13;
<<<A4-C04 EVIDENCE>>>
Source: answer F4, option (d), of the corresponding author (`manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_c769713f.md`, section F4; only that section was read). Item (2) names this place (l.86) for the change of wording. The wording cannot change here: the sentence "We report this as a failed out-of-sample replication of the ordering claim of Section 6.2; the confirmatory claim of this paper is restricted to the XM3600 and second-backbone tests, and the label-gold part is listed in Table 1 as FAIL." is the registered branch text (`manuscript/prereg/2026-10-28_pascal50s/PREREG.md` (1448ab13fcb5) §9 heading l.373 "inserted as written once there is a verdict", §9.2 l.379), and the source comment of the paragraph records the fills. The registered text says "Section 7.2"; the paper prints "Section 6.2" since the renumbering of version 2. The block therefore leaves both registered sentences byte-unchanged and adds, after the last sentence of the paragraph, one sentence that says they are registered text and what "the confirmatory claim" in them denotes; the COCO val2017 paragraph of the same section does the same for its registered text ("follow the registered text with its blanks filled"). The judge may skip this block alone: Section 1 (A4-C01) already carries the same explanation. Section 6.7 lies in the same file and is byte-unchanged (asserted from `## 6.7` to the end of the file). No number.

<<<A4-C05 sec10_discussion.md OLD>>>
**Gold ladder (confirmatory).** Object F1's verbosity slope is ordered
<<<A4-C05 sec10_discussion.md NEW>>>
**Gold ladder (registered ordering prediction and the scope of its support).** Object F1's verbosity slope is ordered
<<<A4-C05 EVIDENCE>>>
Source: answer F4, option (d), of the corresponding author (`manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_c769713f.md`, section F4; only that section was read). Item (2) names Section 8.1 (l.7). Only the label changes: the paragraph already gives the scope (PASS on XM3600, PASS with the second backbone under the registered precision rule, FAIL on PASCAL-50S, "The ordering claim therefore rests on XM3600 and the second backbone"). In the same paragraph "**Which objects references name (registered).**" and "**Count:** no confirmatory claim (Section 3.3)" are unchanged; in the second, "confirmatory" separates registered from exploratory and post hoc results and stays. Registration wording and lines: as in the evidence of A4-C01 (N1-XM-4 has no tier; G2B-O1 and P50-A4 are "primary"; the verdict words PASS and FAIL come from the decide files).

### Group U: UIT-ViIC training statement (CC-407 W4). NEEDS THE INVESTIGATOR: not applied without his decision

<<<A4-U01 declarations.md OLD>>>
UIT-ViIC (Lam et al., 2020) is likewise used only through aggregates and pointers, and no per-image UIT-ViIC panel is released; we have not received written permission from the UIT-ViIC authors and claim none.
<<<A4-U01 declarations.md NEW>>>
Two further adapters of the first backbone were trained on the UIT-ViIC training split (Lam et al., 2020; its 2,695 images, with captions of that split as training targets); with a short and a detailed prompt each, they are four of the ten systems of the UIT-ViIC rows of Table 6.1. UIT-ViIC appears in the paper and the release only as aggregates and pointers: no UIT-ViIC image or caption, no per-image UIT-ViIC panel and no trained adapter weight is released; we have not received written permission from the UIT-ViIC authors and claim none.
<<<A4-U01 EVIDENCE>>>
CC-407 W4 (blocking before submission): the statement "used only through aggregates and pointers" is untrue, because two adapters were trained on the UIT-ViIC training split. Run records (run repo): `.session_backup/machines/n3/ncs-data/uitviic_gold_p1/_build_report.json` (sha256 prefix 5c6b8fbea906): source = `.../datasets/uitviic/train_data.json`, images_with_caption = 2695, captions_total = 13481, captions_used = 2695, policy "short row: first caption"; the training file beside it has 2,695 rows (row count only; no caption was printed). `data/datasets/uitviic/train_data.json` has sha256 prefix 441d22d29eb7 (the pin of `scripts/queue/check_g1_pass.py` l.43), 2,695 images and 13,481 captions. Run folders `.session_backup/machines/n3/ncs-data/runs/uitviic_p1_s42` and `.../runs/uitviic_fuse2_s42`: `adapter_config.json` base model Qwen/Qwen2.5-VL-7B-Instruct, LoRA r = 16; `metrics.jsonl` ends at step 672 (epoch 1.994) and at step 1,346 (epoch 1.997); the two adapter files equal `scripts/queue/adapters_canonical.sha256` l.20-22 (281d4572eb52, 6c192b9a5cdc). INFERRED, not read from a record: no build report and no queue script for the training file of `uitviic_fuse2_s42` is in the n3 backup or among the tracked files of the run repo; that it was built from the same split is inferred from the run name, from the step count (1,346 against 672: twice the rows, as for the KTVIC pair, 1,884 against 942) and from the build report of the same recipe on KTVIC (two rows per image). Which systems: `.session_backup/2026-10-14/r11_verify/c2_n1_uitviic_mstar.json` (bed1dc259aef) :: uitviic_test.systems has 10 entries, four of them `ind_p1_s42-short`, `ind_p1_s42-detailed`, `ind_fuse2_s42-short` and `ind_fuse2_s42-detailed`; the script beside it (`c2_n1_uitviic_mstar.py`, 09a149d42fc2, l.7-10) names them "in-domain uitviic_p1_s42 (short, detailed) and uitviic_fuse2_s42 (short, detailed) [from data/results/uitviic_ind_test/]" and the other six as zero-shot and "transfer" (the two KTVIC adapters; n2 `queue/done/38_uitviic_eval.sh`, model qwen2.5-vl-7b). The four score files in `data/results/uitviic_ind_test/` have split = test_data.json, n_images = 231 and an empty adapter field, so the link from those files to the two run folders is by name and by that script header. Paper rows: the two UIT-ViIC rows of Table 6.1 (`sec7_verbosity_sign.md` l.14-15, "(10; ...)") are keyed to `groups.all_10` of that file (manifest l.210 to l.222, l.486, l.489); Supplementary S7 says "Ten Vietnamese systems". Release: the staged archive `.session_backup/2026-10-21/zenodo_build` holds no model weight file (README l.30 "no images, no reference captions and no model weights"), and the deposit list of `declarations.md` l.19 names no weights. Earlier PI lines on the same point (decisions LOG): PI-1026bc (l.649, 2026-10-28): permission of the UIT-ViIC authors obtained, data statements to say so; PI-1029p item (5) (l.776, 2026-10-29, the newest decision on UIT-ViIC and the source of the present wording): "UIT-ViIC: no author permission, papers state aggregates and pointers only"; PI-1029q (l.777, 2026-10-29): the datasets are public and may be used freely, the permission letter is a courtesy, and "papers release aggregates and pointers only" stays binding; PI-1110o (l.2072) and F-19 (`FIX_RESOLUTIONS_2026-11-10.md` l.33) concern the agreement clauses of UIT-OpenViIC, KTVIC and PASCAL-50S and do not name UIT-ViIC. The workflow log already calls these systems UIT-ViIC-trained (D-W14-2, `manuscript/WORKFLOW_LOG.md` l.468-469, l.634, l.642). **NEEDS THE INVESTIGATOR: not applied without his decision**, because the block changes wording that PI-1029p item (5) set. It writes no agreement or permission clause; the clause that no written permission was received is kept word for word. It makes no statement on overlap between training and test images (PI-1110n). "Two further adapters": the sentence before this one states the two KTVIC adapters.

<<<A4-U02 anon/declarations_anon.md OLD>>>
UIT-ViIC (Lam et al., 2020) is likewise used only through aggregates and pointers, and no per-image UIT-ViIC panel is released; we have not received written permission from the UIT-ViIC authors and claim none.
<<<A4-U02 anon/declarations_anon.md NEW>>>
Two further adapters of the first backbone were trained on the UIT-ViIC training split (Lam et al., 2020; its 2,695 images, with captions of that split as training targets); with a short and a detailed prompt each, they are four of the ten systems of the UIT-ViIC rows of Table 6.1. UIT-ViIC appears in the paper and the archive only as aggregates and pointers: no UIT-ViIC image or caption, no per-image UIT-ViIC panel and no trained adapter weight is released; we have not received written permission from the UIT-ViIC authors and claim none.
<<<A4-U02 EVIDENCE>>>
Same change as A4-U01 in the anonymised copy ("the archive" as in the sentences around it). Run records, release and earlier PI lines: as in the evidence of A4-U01. **NEEDS THE INVESTIGATOR: not applied without his decision** (the wording was set by PI-1029p item (5)). No agreement or permission clause is written. Whether the copy is still needed is item I-2.

<<<A4-U03 sec11_limitations_ethics.md OLD>>>
**UIT-OpenViIC and UIT-ViIC.** Both are used only through aggregate statistics and pointers (image identifiers and file hashes); no caption, n-gram or per-image panel of either appears in this paper or its release (UIT-OpenViIC aggregates: Table 5.1 and Supplementary S5). One of us contacted the UIT-OpenViIC authors, who agreed to this use; we have not received written permission from the UIT-ViIC authors (Lam et al., 2020).
<<<A4-U03 sec11_limitations_ethics.md NEW>>>
**UIT-OpenViIC and UIT-ViIC.** UIT-OpenViIC is used only through aggregate statistics and pointers (image identifiers and file hashes), and UIT-ViIC appears in this paper and its release only in that form; no caption, n-gram or per-image panel of either appears in this paper or its release (UIT-OpenViIC aggregates: Table 5.1 and Supplementary S5). One of us contacted the UIT-OpenViIC authors, who agreed to this use; we have not received written permission from the UIT-ViIC authors (Lam et al., 2020). Two adapters of the first backbone (not those of Section 6.2) were trained on the UIT-ViIC training split: its 2,695 images, with captions of that split as training targets. With a short and a detailed prompt each, they are four of the ten systems of the UIT-ViIC rows of Table 6.1; no trained adapter weight is part of this paper's release.
<<<A4-U03 EVIDENCE>>>
Section 9.2, same change. Run records, release and earlier PI lines: as in the evidence of A4-U01. **NEEDS THE INVESTIGATOR: not applied without his decision** (the wording was set by PI-1029p item (5)). No agreement or permission clause is written. The UIT-OpenViIC clauses ("used only through", the agreement clause of PI-1110o) are kept word for word. "(not those of Section 6.2)": the KTVIC paragraph, which follows this one, describes the two adapters of Section 6.2.

<<<A4-U04a supplementary.md OLD>>>
**UIT-ViIC.** UIT-ViIC (Lam et al., 2020) is used only through aggregate statistics and pointers (image identifiers and file hashes). No UIT-ViIC caption, n-gram or per-image panel appears in this paper or its release, and we have not received written permission from the UIT-ViIC authors.
<<<A4-U04a supplementary.md NEW>>>
**UIT-ViIC.** UIT-ViIC (Lam et al., 2020) appears in this paper and its release only as aggregate statistics and pointers (image identifiers and file hashes). Two adapters of the first backbone were trained on its training split (2,695 images, with captions of that split as training targets); with a short and a detailed prompt each, they are four of the ten systems of the UIT-ViIC rows of Table 6.1. No UIT-ViIC caption, n-gram or per-image panel and no trained adapter weight appears in this paper or its release, and we have not received written permission from the UIT-ViIC authors.
<<<A4-U04a EVIDENCE>>>
A fourth statement of the same wording, in Supplementary S6 (source l.661, journal file l.542); CC-407 Ruling 5 lists three. Left as it is, it would contradict A4-U01 to A4-U03. Run records, release and earlier PI lines: as in the evidence of A4-U01. **NEEDS THE INVESTIGATOR: not applied without his decision** (the wording was set by PI-1029p item (5)). No agreement or permission clause is written.

<<<A4-U04b supplementary_SPIC.md OLD>>>
**UIT-ViIC.** UIT-ViIC (Lam et al., 2020) is used only through aggregate statistics and pointers (image identifiers and file hashes). No UIT-ViIC caption, n-gram or per-image panel appears in this paper or its release, and we have not received written permission from the UIT-ViIC authors.
<<<A4-U04b supplementary_SPIC.md NEW>>>
**UIT-ViIC.** UIT-ViIC (Lam et al., 2020) appears in this paper and its release only as aggregate statistics and pointers (image identifiers and file hashes). Two adapters of the first backbone were trained on its training split (2,695 images, with captions of that split as training targets); with a short and a detailed prompt each, they are four of the ten systems of the UIT-ViIC rows of Table 6.1. No UIT-ViIC caption, n-gram or per-image panel and no trained adapter weight appears in this paper or its release, and we have not received written permission from the UIT-ViIC authors.
<<<A4-U04b EVIDENCE>>>
A fourth statement of the same wording, in Supplementary S6 (source l.661, journal file l.542); CC-407 Ruling 5 lists three. Left as it is, it would contradict A4-U01 to A4-U03. Run records, release and earlier PI lines: as in the evidence of A4-U01. **NEEDS THE INVESTIGATOR: not applied without his decision** (the wording was set by PI-1029p item (5)). No agreement or permission clause is written.

<<<A4-U05a supplementary.md OLD>>>
Ten Vietnamese systems were scored with two matchers.
<<<A4-U05a supplementary.md NEW>>>
Ten Vietnamese systems of the first backbone were scored with two matchers: zero-shot, the two adapters trained on the KTVIC training split (Section 6.2) and two adapters trained on the UIT-ViIC training split (its 2,695 images), each with a short and a detailed prompt.
<<<A4-U05a EVIDENCE>>>
Supplementary S7 (source l.734, journal file l.592) is where the paper describes these systems, and it names none of them. The new sentence lists the ten as the result file has them (zero-shot 2, `transfer_` 4, `ind_` 4). Run records, release and earlier PI lines: as in the evidence of A4-U01. **NEEDS THE INVESTIGATOR: not applied without his decision** (the wording was set by PI-1029p item (5)). No agreement or permission clause is written. Optional within the group: the judge may drop this pair and keep A4-U01 to A4-U04.

<<<A4-U05b supplementary_SPIC.md OLD>>>
Ten Vietnamese systems were scored with two matchers.
<<<A4-U05b supplementary_SPIC.md NEW>>>
Ten Vietnamese systems of the first backbone were scored with two matchers: zero-shot, the two adapters trained on the KTVIC training split (Section 6.2) and two adapters trained on the UIT-ViIC training split (its 2,695 images), each with a short and a detailed prompt.
<<<A4-U05b EVIDENCE>>>
Supplementary S7 (source l.734, journal file l.592) is where the paper describes these systems, and it names none of them. The new sentence lists the ten as the result file has them (zero-shot 2, `transfer_` 4, `ind_` 4). Run records, release and earlier PI lines: as in the evidence of A4-U01. **NEEDS THE INVESTIGATOR: not applied without his decision** (the wording was set by PI-1029p item (5)). No agreement or permission clause is written. Optional within the group: the judge may drop this pair and keep A4-U01 to A4-U04.

### Group N: CC-407 N1, N2, N4 and N9

<<<A4-N01 sec10_discussion.md OLD>>>
check it with a seed placebo (a check of the paired control only; Section 3.3), and show the others in a specification curve (Section 3.3).
<<<A4-N01 sec10_discussion.md NEW>>>
check it with a seed placebo (a check of the paired control only), and show the others in a specification curve (Section 3.3).
<<<A4-N01 EVIDENCE>>>
CC-407 N1: block A2-F12 left two "(Section 3.3)" pointers in one checklist item; the ruling says to drop the first. Both things are in Section 3.3 (`sec3_measurement_setup.md` l.38 the specification curve, l.40 the seed placebo), so the one pointer at the end of the item covers both. No number.

<<<A4-N02 sec3_measurement_setup.md OLD>>>
The adjacent-doubleton shares of Table 5.1 use $B$ = 1,000.
<<<A4-N02 sec3_measurement_setup.md NEW>>>
The adjacent-doubleton shares of Table 5.1 use $B = 1000$.
<<<A4-N02 EVIDENCE>>>
CC-407 N2: block A2-F10 wrote "$B$ = 1,000" in a paragraph that writes "$B = 500$" (twice) and "$B = 5000$"; one style. The form with the number inside the formula and no thousands separator is the one the paragraph already uses for 5000. The value is unchanged (manifest rows l.3944-3945, added under CC-407).

<<<A4-N04 declarations.md OLD>>>
The reference captions and human-judgment ratings of COCO, XM3600, UIT-ViIC, UIT-OpenViIC, KTVIC, LongCap-Arena, THumB, Polaris and DOCCI-Critique are not redistributed, because of their licences and terms of use; they are available from their original sources.
<<<A4-N04 declarations.md NEW>>>
The reference captions and human-judgment ratings of COCO, XM3600, UIT-ViIC, UIT-OpenViIC, LongCap-Arena, THumB, Polaris and DOCCI-Critique are not redistributed, because of their licences and terms of use, and the KTVIC reference captions are not redistributed either; all are available from their original sources.
<<<A4-N04 EVIDENCE>>>
CC-407 N4 (before submission): the sentence gives "their licences and terms of use" as the reason for KTVIC too, but no KTVIC licence or terms are known: decisions LOG l.2635 (OPS-1115e-ktvic-readme): the public repository has no licence file, a null licence field and no terms sentence in its README, and "nothing is known here about terms stated elsewhere". The new sentence keeps the fact (the KTVIC captions are not redistributed) and gives no reason for it. Earlier PI lines on the same point: PI-1029q (l.777): "no caption text from OpenViIC/KTVIC/UIT-ViIC committed to the repo, papers release aggregates and pointers only" stays binding, so the non-redistribution is the PI's rule and is kept; PI-1026az (l.635) and PI-1110o (l.2072) concern the agreement of the authors, not a licence; no PI line states a KTVIC licence. ALTERNATIVE for the judge (not in the block; the ruling's "e.g. with F2's fact"): after "redistributed either" add "(its public repository carried no licence file when read on 15 November 2026)"; the block leaves it out because data licences are among the items the PI keeps (PI-1114n, l.2625) and the sentence must never read as "free of terms". The anonymised copy has no such clause (`anon/declarations_anon.md` l.10) and needs no change.

<<<A4-N09a declarations.md OLD>>>
<!-- plan §3.3, CC-126 W17; PI-1026az (LOG.md, 2026-10-28): the PI obtained written acceptance from the UIT-OpenViIC, KTVIC and PASCAL-50S authors; rev1 item 2 reverted to this wording on that record. -->
<<<A4-N09a declarations.md NEW>>>
<!-- plan §3.3, CC-126 W17; PI-1026az (LOG.md, 2026-10-28) and PI-1110o (LOG.md, 2026-11-10): the PI states that the UIT-OpenViIC, KTVIC and PASCAL-50S authors accepted; no document is filed in the repo, so the text states the agreement as a fact without "in writing", a date or "on file"; for KTVIC no agreement clause is printed since CC-407, where the stated use includes training (CC-407 N9); rev1 item 2 reverted to this wording on that record. -->
<<<A4-N09a EVIDENCE>>>
CC-407 N9. PI-1110o (decisions LOG l.2072, 2026-11-10): the PI states that the dataset authors' acceptance has been confirmed and that no document will be filed in the repo; the papers state the agreement as a fact; "in writing", the date and "on file with the corresponding author" are not written; item closed, no further question to the PI. Same in `FIX_RESOLUTIONS_2026-11-10.md` l.33 (F-19: A-16, B-06, C-09). The comment is not printed (`scrub()` removes it from the journal supplement; pandoc drops it elsewhere); it is brought in line with that decision and keeps its pointer to PI-1026az (l.635). No printed word changes.

<<<A4-N09b declarations.md OLD>>>
(PI statement in the committed registration, 353437f); PI to confirm the written document is on file -->
<<<A4-N09b declarations.md NEW>>>
(PI statement in the committed registration, 353437f); PI-1110o (LOG.md, 2026-11-10): the PI states that the authors accepted, no document is filed in the repo and the item is closed, so no confirmation of a document is pending (CC-407 N9; the sentence of the registration itself is CC-407 W6) -->
<<<A4-N09b EVIDENCE>>>
As A4-N09a (CC-407 N9; PI-1110o, decisions LOG l.2072; F-19, `FIX_RESOLUTIONS_2026-11-10.md` l.33). No printed word changes. The old comment asks the PI to confirm that a written document is on file; PI-1110o closes that question.

<<<A4-N09c declarations.md OLD>>>
no caption or image is redistributed." (prereg 2026-10-28_a_p50_kladder §1.4) -->
<<<A4-N09c declarations.md NEW>>>
no caption or image is redistributed." (prereg 2026-10-28_a_p50_kladder §1.4); the clause on written confirmation in that quoted sentence is no longer in the text, which says "the dataset authors were contacted by one of us and agreed to this use" (PI-1110o, F-19; CC-407 N9) -->
<<<A4-N09c EVIDENCE>>>
As A4-N09a (CC-407 N9; PI-1110o, decisions LOG l.2072; F-19, `FIX_RESOLUTIONS_2026-11-10.md` l.33). No printed word changes. The comment quotes the sentence as it was planned on 2026-10-29, with "written confirmation ... on file with the corresponding author"; the quotation is a record and stays, and one clause says that the printed sentence now differs.

<<<A4-N09d sec11_limitations_ethics.md OLD>>>
<!-- PI-1026az: written acceptance from the UIT-OpenViIC authors obtained by the PI; per-image panels still not released -->
<<<A4-N09d sec11_limitations_ethics.md NEW>>>
<!-- PI-1026az and PI-1110o: the PI states that the UIT-OpenViIC authors accepted; no document is filed in the repo (CC-407 N9); per-image panels still not released -->
<<<A4-N09d EVIDENCE>>>
As A4-N09a (CC-407 N9; PI-1110o, decisions LOG l.2072; F-19, `FIX_RESOLUTIONS_2026-11-10.md` l.33). No printed word changes.

<<<A4-N09e supplementary.md OLD>>>
<!-- rev1 (PI-1029p; PI-1026az, LOG.md 2026-10-28): written acceptance from the UIT-OpenViIC, KTVIC and PASCAL-50S authors; replaces 'We have not obtained written confirmation from the dataset authors.', which contradicted declarations.md -->
<<<A4-N09e supplementary.md NEW>>>
<!-- rev1 (PI-1029p; PI-1026az, LOG.md 2026-10-28; PI-1110o, LOG.md 2026-11-10): the PI states that the UIT-OpenViIC, KTVIC and PASCAL-50S authors accepted; no document is filed in the repo (CC-407 N9); replaces 'We have not obtained written confirmation from the dataset authors.', which contradicted declarations.md -->
<<<A4-N09e EVIDENCE>>>
As A4-N09a (CC-407 N9; PI-1110o, decisions LOG l.2072; F-19, `FIX_RESOLUTIONS_2026-11-10.md` l.33). No printed word changes. Source file of the supplement only (S6, l.658); the journal file has no comments and is unchanged by this block; the provenance table is regenerated (step S2).

<<<A4-N09f supplementary.md OLD>>>
<!-- PI-1026az: written acceptance from the UIT-OpenViIC authors obtained by the PI; per-image panels still not released -->
<<<A4-N09f supplementary.md NEW>>>
<!-- PI-1026az and PI-1110o: the PI states that the UIT-OpenViIC authors accepted; no document is filed in the repo (CC-407 N9); per-image panels still not released -->
<<<A4-N09f EVIDENCE>>>
As A4-N09a (CC-407 N9; PI-1110o, decisions LOG l.2072; F-19, `FIX_RESOLUTIONS_2026-11-10.md` l.33). No printed word changes. Source file of the supplement only (S10, l.1350, before S11); the journal file is unchanged by this block; the provenance table is regenerated (step S2).


## 4. Steps that are not blocks

**S1. Two rows appended to `number_manifest.tsv`** (only when group U is applied; tab-separated, in the format of the file; shown here with the tabs as they are):

```
2,695 (uitviic_p1_s42 training images; UIT-ViIC training split)	A	.session_backup/machines/n3/ncs-data/uitviic_gold_p1/_build_report.json	images_with_caption	5c6b8fbea906	keyed (adapters' training split; declarations, sec11 §9.2, supplement S6 and S7; fix package v4 group U)
4 of 10 (UIT-ViIC test systems from adapters trained on the UIT-ViIC training split)	A	.session_backup/2026-10-14/r11_verify/c2_n1_uitviic_mstar.json	uitviic_test.systems: the four ind_ entries (ind_p1_s42 and ind_fuse2_s42, short and detailed) of len = 10	bed1dc259aef	DERIVED (count; names per c2_n1_uitviic_mstar.py l.7-10; fix package v4 group U)
```

Groups C and N print no number that is new to the paper, so they add no row: every figure of group C is already keyed (rows cited in the evidence lines).

**S2. `supplementary_provenance_internal.tsv` regenerated** (when `supplementary.md` changes: groups U and N) from the rows that `scrub()` returns, written in the format of `scrub_supp.py`'s `main()` (header line, tab-joined rows). `scrub_supp.py` itself is not run (CC-403 W2; CC-407 W5).

**S3. Length block at the top of `abstract_A.md`** (an HTML comment, not paper text; the file is byte-unchanged from `## Abstract` to its end, so the abstract paragraph, its 250 words and the keywords line do not change). For C+N the replacements are:

- `recounted after fix package v2 of 2026-11-15).` -> `recounted after fix package v2 of 2026-11-15; recounted after fix package v4 of 2026-11-15).`
- `Main text now: 18,927 words` -> `Main text now: 19,151 words`
- `Over the limit by 10,427 words.` -> `Over the limit by 10,651 words.`
- `Longest files: sec7_verbosity_sign.md 7,523; sec2_related_work.md 2,184; sec11_limitations_ethics.md 2,054.` -> `Longest files: sec7_verbosity_sign.md 7,567; sec2_related_work.md 2,184; sec1_introduction.md 2,064.`

For another combination the script computes the numbers from the files it has built. If the ruling reads "abstract byte-unchanged" as the whole file, put `"S3"` into `SKIP`; the length block is then out of date and must be updated in a later commit.

## 5. Notes

### 5.1 Group C

1. **What the registrations call these tests.** The XM3600 registration lists the ordering as `N1-XM-4 (Ordering)` under "Relative-form predictions" and gives it no tier. The second-backbone registration lists `G2B-O1` as "primary". The PASCAL-50S registration lists `P50-A4` as "primary (replicates A4)", and its registered branch text for a failed replication says that "the confirmatory claim of this paper is restricted to the XM3600 and second-backbone tests". So the registration itself calls the XM3600 and second-backbone tests the confirmatory claim and the PASCAL-50S test a failed out-of-sample replication. The brief rules this case: those words stay, and the grouping gets a neutral heading. The package therefore writes "registered ordering prediction" and "ordering tests (registered)", not "Primary preregistered ordering hypothesis" as the answer proposes: "primary" is not the tier of the XM3600 test, and the registrations and Table 1 speak of predictions.
2. **Where "confirmatory" stays.** It stays wherever it separates registered tests from exploratory or post hoc ones, and in registered text: `sec1_introduction.md` l.11 ("The confirmation supports the empirical pattern") and l.13; `sec3_measurement_setup.md` l.40 and l.60; `sec7_verbosity_sign.md` l.5, l.86 (registered text) and l.104; `sec10_discussion.md` l.7 ("**Count:** no confirmatory claim"), l.11 and l.29; `sec11_limitations_ethics.md` l.9 and l.36; Supplementary S3, S4 (with Table S4.0) and S10. The new first sentence of the Section 1 paragraph says what "the confirmatory claim" in those places denotes, so none of them needs a change. The abstract and the highlights do not use the word; the cover letter uses it once, for the count control.
3. **Section 6.4.** The answer names l.86 for the change. The two sentences there are registered branch text and are left byte-unchanged; A4-C04 adds one sentence after the paragraph's last sentence. The judge may skip A4-C04 alone.
4. **Table 1.** The first row now holds the two passing tests and the failed replication; the FAIL row names A24 by reference and keeps the count 9. The value of A24 is printed once in the table, as before. The registration line "Every branch: Table 1 gets a new row, with the verdict copied from the decide file" is for the judge to read against this layout (point J-3).
5. **Earlier PI line.** PI-1029m (PASS headline; registered FAILs reported briefly, not hidden) is not reversed: the abstract and the highlights are unchanged, the passing tests keep the first place, and the failure was already in the paragraph and in the table.
6. **Length.** Group C adds +218 words to a main text that is over the limit used so far; the cut plan (`A_CUT_PLAN_v1.md`) is not changed by this package.

### 5.2 Group U

1. **What the records show.** Two LoRA adapters of Qwen2.5-VL-7B (run folders `uitviic_p1_s42` and `uitviic_fuse2_s42` in the n3 backup) exist beside the two KTVIC adapters. For the first, the build report gives the UIT-ViIC training file as its source: 2,695 images, one caption per image out of 13,481. The result file behind the two UIT-ViIC rows of Table 6.1 lists ten systems; four of them are these two adapters with a short and a detailed prompt, and the script that wrote the file calls them "in-domain".
2. **What is inferred.** No build report and no queue script for the training file of the second adapter was found (n3 backup; tracked files of the run repo). Its source split is inferred from the run name, the step count and the recipe. The sentence "with captions of that split as training targets" therefore rests on a record for one adapter and on inference for the other (item I-4). The link from the four score files to the two run folders is by name and by the script header; the score files do not record an adapter path.
3. **Why the group waits for the investigator.** The newest PI decision on UIT-ViIC is PI-1029p item (5): no author permission, and the papers state aggregates and pointers only. The proposed text keeps "aggregates and pointers" for what the paper and the release contain, and adds the training, which that decision did not foresee. The choice is his (item I-1).
4. **Places.** CC-407 Ruling 5 names three statements (`declarations.md`, the anonymised copy, Section 9.2). A fourth with the same wording stands in Supplementary S6 (A4-U04), and Supplementary S7 is where the ten systems are mentioned without being named (A4-U05, optional within the group).
5. **What the blocks do not say.** No agreement or permission clause is added; the existing clause that no written permission was received is kept word for word. No licence or terms wording. No statement on overlap between training and test images (PI-1110n).
6. **Release.** "No trained adapter weight" follows the staged archive of 2026-10-21, as for KTVIC; it is a statement about a release that does not exist yet (item I-5).

### 5.3 Group N

- **N1, N2, N4, N9:** blocks A4-N01, A4-N02, A4-N04 and A4-N09a to A4-N09f.
- **N3 (no block):** items I-3 and I-4 of package v2 are superseded by PI-1115c and OPS-1115e; this package repeats neither.
- **N5 (no block; recorded here as the ruling asks):** the link between the first KTVIC adapter and its training file is direct: n2 `queue/done/30_p1_s43.sh` runs the training with `--data /root/ncs-data/gold_p1 --out /root/ncs-data/runs/p1_s43 --epochs 2 --seed 43`. The link between `fuse2_s42` and `gold_fuse2` is INFERRED: no training command for it is in the n2 queue backup; it follows from the build report (7,538 rows), the final step (1,884 = 7,538 x 2 / 8) and a skipped control script that names `gold_fuse2` as the data of a continuation from `fuse2_s42`. The two UIT-ViIC adapters have the same status (5.2 note 2).
- **N6 (no block):** checked. The earlier conference paper (latest PDF in the run repo root, sha256 prefix 449c2ad0a4c1) states in its section on experimental datasets that KTVIC has 3,769 training and 558 test images and that 3,700 training images were used for supervision construction and fine-tuning. So that paper states the data of the "distilled" system. Whether this PDF equals the published version was not checked.
- **N7 (no block):** met by this package's evidence lines, which say for each block on a declaration, data statement or permission clause which records were searched and which PI lines were found.
- **N8:** for the investigator (item I-2).

## 6. Deferred items, items for the investigator, points for the judge

### 6.1 Deferred (not in this package)

- **D-1. CC-407 W5:** internal terms in the quoted registered text of Section 6.7 and Supplementary S11, and the leak hits of the scrub. Waits for the release of the hold; until then `scrub_supp.py` must not be run.
- **D-2. Abstract, highlights and cover letter:** unchanged by item (1) of answer F4; one sync after the release.
- **D-3. Table 2.1 of Section 2:** another package (applied at `ff6ca80`).
- **D-4. Length:** no text is cut here; the package adds words (Section 1).
- **D-5. The title** (answer A6 of the first round): unchanged.

### 6.2 For the investigator

- **I-1. Group U.** Three ways: (a) state the training as in the blocks and keep "we have not received written permission"; (b) report the UIT-ViIC rows without the four systems (the result file already holds a six-system group, but the two rows of Table 6.1 and the sentences that quote them would change, which is a change of reported exploratory numbers); (c) another wording of his own. Recommended: (a); it changes no number and makes the three statements true. Default if no answer: group U stays unapplied and W4 stays blocking before submission.
- **I-2. CC-407 N8:** keep or retire `anon/declarations_anon.md` (built for an earlier double-anonymised target; this journal reviews single-anonymised).
- **I-3. CC-407 W6:** the PASCAL-50S registration says that written confirmation is on file with the corresponding author. A committed registration is not edited; CC-407 Ruling 2 (b) lists what he must produce if that wording is to be relied on.
- **I-4. A record for the second UIT-ViIC adapter:** if a copy of its training file's build report or of the n3 queue scripts exists outside the backups, it closes the inference of note 5.2 (2).
- **I-5. Adapter weights:** the new sentences say that no trained adapter weight is part of the release, now for the UIT-ViIC adapters too. Confirm, or say that the adapters will be released.
- **I-6. KTVIC and the dated repository fact** (alternative text in the evidence of A4-N04): data licences are among the items he keeps (PI-1114n), so the block itself adds no licence wording.

### 6.3 Points for the judge

- **J-1.** Heading wording of group C: "registered ordering prediction" against the answer's "Primary preregistered ordering hypothesis" (note 5.1 (1)).
- **J-2.** A4-C04: keep or skip the added sentence of Section 6.4.
- **J-3.** Whether the first row of Table 1 after A4-C02 meets the registration line "Table 1 gets a new row".
- **J-4.** A4-U05 (Supplementary S7) is optional within group U.
- **J-5.** A4-N04: the block as written, or with the dated repository fact.
- **J-6.** Step S3 writes the comment at the top of `abstract_A.md`; the abstract itself is byte-unchanged (asserted).

## 7. Checks run

### 7.1 OLD occurs exactly once (every block)

| Id | File | Count of OLD at HEAD | Count when all three groups are applied in the order of Section 3 | Exactly once |
|---|---|---|---|---|
| A4-C01 | `sec1_introduction.md` | 1 | 1 | yes |
| A4-C02 | `sec1_introduction.md` | 1 | 1 | yes |
| A4-C03 | `sec1_introduction.md` | 1 | 1 | yes |
| A4-C04 | `sec7_verbosity_sign.md` | 1 | 1 | yes |
| A4-C05 | `sec10_discussion.md` | 1 | 1 | yes |
| A4-U01 | `declarations.md` | 1 | 1 | yes |
| A4-U02 | `anon/declarations_anon.md` | 1 | 1 | yes |
| A4-U03 | `sec11_limitations_ethics.md` | 1 | 1 | yes |
| A4-U04a | `supplementary.md` | 1 | 1 | yes |
| A4-U04b | `supplementary_SPIC.md` | 1 | 1 | yes |
| A4-U05a | `supplementary.md` | 1 | 1 | yes |
| A4-U05b | `supplementary_SPIC.md` | 1 | 1 | yes |
| A4-N01 | `sec10_discussion.md` | 1 | 1 | yes |
| A4-N02 | `sec3_measurement_setup.md` | 1 | 1 | yes |
| A4-N04 | `declarations.md` | 1 | 1 | yes |
| A4-N09a | `declarations.md` | 1 | 1 | yes |
| A4-N09b | `declarations.md` | 1 | 1 | yes |
| A4-N09c | `declarations.md` | 1 | 1 | yes |
| A4-N09d | `sec11_limitations_ethics.md` | 1 | 1 | yes |
| A4-N09e | `supplementary.md` | 1 | 1 | yes |
| A4-N09f | `supplementary.md` | 1 | 1 | yes |

The same count (exactly once, in the running text) holds in each of the seven group combinations (C, N, U, C+N, C+U, N+U, C+N+U): no block of one group touches the string of a block of another group.

### 7.2 Other checks (all in memory; no paper file was written)

- Paper HEAD `ff6ca8084a8bb57e1bac48cff044df6eb3a3b618`; `git status --porcelain -- paper` empty. The blocks were written against `ea12e51`, which is an ancestor of HEAD; files changed between the two: `paper/sec2_related_work.md`. Every file this package changes is byte-equal at `ea12e51` and at HEAD. OLD strings were checked against `git show HEAD:paper/<file>`.
- Every NEW string occurs exactly once in its file after application, in every combination.
- Figures of group C and facts of group U were re-read from their result files and run records by the builder (assertions on the sha256 prefix of each file and on each value): XM3600 ordering PASS: `.session_backup/2026-10-14/r12_verify/xm3600_full_verdict.json` (0b2b3aa5e1a3) :: prereg_comparisons[19].in_interval_or_pass = PASS (N1-XM-4); manifest l.243; second backbone PASS on 537 images: `data/results/g2b/g2b_score.json` (68be2b7a0904) :: datasets.xm600.predictions.G2B-O1 (both parts PASS, n_images = 537); manifest l.927, l.928, l.931; PASCAL-50S FAIL, -2.29 [-5.15, +0.61]: `data/results/p50/p50_decide.json` (0da4cab90fe9) :: analysis_set.P50-A4.verdict = FAIL, parts[1].{point = -2.2885, ci95 = [-5.1506, 0.6123], verdict = FAIL}; manifest l.1084 to l.1088; 0.83: `data/results/a_g0/g0.json` (23e12cbd179e) :: ratio_voc_over_ref = 0.8265 (1,787 / 2,162; post hoc descriptive, no verdict); manifest l.1252; +35.46 and the size premise: `data/results/a_t3/tier3.json` (5735bd20f26b) :: analysis.AD1p.{point = 35.4553, verdict = PASS}, analysis.L_vs_R5.verdict = PREMISE_NOT_MET, analysis.premise.L_over_R5 = 1.3947 (< 2); manifest l.1333, l.1336, l.1352, l.1353; 6 of 6 leave-one-system-out fits: `data/results/a1_robustness/loo_triples.json` (d74f34c431fb) :: xm3600_loo_n_ordered = 6, xm3600_loo_n_drops = 6 (DERIVED, POST HOC); manifest l.1067; UIT-ViIC build report, training split, the two run folders and the system list as in the evidence line of A4-U01.
- Table 1 after group C: the first row holds the ledger ids A4, A6 and A24; the FAIL row holds the same nine ids as at HEAD; the string "−2.29 [−5.15, +0.61]" occurs as often in `sec1_introduction.md` as at HEAD (it moves from the FAIL row to the first row).
- Supplement sync in every combination: `scrub(supplementary.md)` equals `supplementary_SPIC.md` byte for byte (`scrub()` imported from `paper/build/scrub_supp.py` with bytecode writing off; the script was not run). Comments removed by the scrub: 653.
- Leak pattern of the scrub on the journal supplement: 4 hits at line(s) 1486, 1728 after all groups, all inside S11 (deferred item D-1); no new hit in any combination.
- Custody zones byte-unchanged in every combination (asserted): everything from `## S11 ` to the end of both supplement files; `sec7_verbosity_sign.md` from `## 6.7` to the end of the file; `abstract_A.md` from `## Abstract` to the end; `highlights_A.md`, `cover_letter_A.md`, `title_page_A.md` and `sec2_related_work.md` are not written.
- Main-text words by the method of the length block: 18,927 at HEAD; after C+N 19,151 (+224); after C+N+U 19,285 (+358). By file after C+N+U: `sec1_introduction.md` +166; `sec7_verbosity_sign.md` +44; `sec10_discussion.md` +6; `sec11_limitations_ethics.md` +74; `declarations.md` +68.
- No e-mail address, no personal name outside the paper's own citations, no dataset caption and no model output in any OLD, NEW or EVIDENCE string (address pattern asserted by the builder).

### 7.3 Files and sha256

Base: the 12 files below, equal at `ea12e51` and at HEAD `ff6ca80`. The apply script checks that `ea12e51` is an ancestor of HEAD and pins these base values, not a fixed HEAD.

| File | sha256 at HEAD |
|---|---|
| `paper/abstract_A.md` | 0d249d7c484ef41dfa8b4afc22d3e8cea1f78e7aa97790421cabf2c99561edd4 |
| `paper/anon/declarations_anon.md` | 066a325d31be854ffda7abba6f1aa46995c573fadfb904136f4e438471c473db |
| `paper/declarations.md` | 4149bb37b23fd250164af378ea189d119e437f20b0d0dfa8049ec43ec7506fb4 |
| `paper/number_manifest.tsv` | d3ca0672f389ebd1621a49de625aa3d926e3603f0f78d7e1ae6881b1b2b41c8b |
| `paper/sec10_discussion.md` | 77ceb4083d5c1e39206f8badfabaa8651f6a6a4fb4af7627579035fa04e76a54 |
| `paper/sec11_limitations_ethics.md` | eec0ec50fbe5159b08412b43f1171d5a5c5e22959841e7e68214f72ef835e4df |
| `paper/sec1_introduction.md` | 46b7534e1936ce4841d8c23b5baf09a6e4457e651917c5055ef872de2475c914 |
| `paper/sec3_measurement_setup.md` | bfc5c286c533b52d881899486ef1eef534dd43940d4028898adc98da9ae8bd8d |
| `paper/sec7_verbosity_sign.md` | b6f46b8aaf33ef133b54e5e4d91f2c1f037e061d48f495e1b23eed5b0aaf4817 |
| `paper/supplementary.md` | eb1b65708c56a2dd1e89cfbde7ffe01152586fdc88a5a0a0dad3d5daa33bd882 |
| `paper/supplementary_SPIC.md` | a76c820f0bbcbe1e54957ebf10f542ab49cdb7bc83480a634bdcae919b265305 |
| `paper/supplementary_provenance_internal.tsv` | 82b663b1d2106662c3d1e6a4e9025ecb94288053239de5d1cde40643a87c5998 |

Results per group combination (the writer's own computation; the ruling fixes the targets). A file missing from a table is not changed by that combination.

**C+N** (the combination that needs no decision of the investigator): 9 files, main text 19,151 words.

| File | sha256 after |
|---|---|
| `paper/abstract_A.md` | 67f37c9686a54ba203b9f6b6c78118e9b56e6651e1dbf81a91c003ccb3ae4f7b |
| `paper/declarations.md` | 8fb28692d32e3688d0694ae6c84353f63d8968032e53f9bdf3c6b933ffbe288b |
| `paper/sec10_discussion.md` | d48ce382b275e73e3f6de34e08814f7c7205a51fb394d5742ed382f9e8e252bf |
| `paper/sec11_limitations_ethics.md` | 9ff1cd8ecb84b000a08ed9e3f7ab5dc4bef8d745376860fc937c7662ee3523b7 |
| `paper/sec1_introduction.md` | 7d6267cd363ceb68ab00760119ff4034f489af81b82b9890a62a2e57e7730233 |
| `paper/sec3_measurement_setup.md` | 665c60aa1956df8dedab070db395bd794297fec88cf07d7242c6bc7c31e74575 |
| `paper/sec7_verbosity_sign.md` | 0e344d32b21457d66572022f6ceb72b77c1188df70068f52c52a5c5505211cc1 |
| `paper/supplementary.md` | 0349454b2d0549051da9b64eccf2c12b0843ce51c75882927425dafb6d1ec927 |
| `paper/supplementary_provenance_internal.tsv` | 1162582f16633e11d26d9d1a72fd20a3b04389a51453c3e1e8c2605068002a07 |

**C+N+U** (all three groups): 12 files, main text 19,285 words.

| File | sha256 after |
|---|---|
| `paper/abstract_A.md` | 4b83b95edda87eec1cfb219909d23d3440de842bf0eff0e4c1cda445ea50e214 |
| `paper/anon/declarations_anon.md` | ec71a9b953ab3609a31f457b8368814c35a82443035885cfa64d9d8df84a96cb |
| `paper/declarations.md` | 5920d0fa7461f0a75cd6aae6d58df7e7588111ba9ad39ff76e1aa3af4c4702ba |
| `paper/number_manifest.tsv` | dd2bce1797bb5bbe52da2d832750038bbfc7f2d39c10d99fe6eacb9de9b716c8 |
| `paper/sec10_discussion.md` | d48ce382b275e73e3f6de34e08814f7c7205a51fb394d5742ed382f9e8e252bf |
| `paper/sec11_limitations_ethics.md` | a7258f2eddb6e137d6abe6990063ce2cc8a4e8e57c9e6bddcef6161e54d2a1e4 |
| `paper/sec1_introduction.md` | 7d6267cd363ceb68ab00760119ff4034f489af81b82b9890a62a2e57e7730233 |
| `paper/sec3_measurement_setup.md` | 665c60aa1956df8dedab070db395bd794297fec88cf07d7242c6bc7c31e74575 |
| `paper/sec7_verbosity_sign.md` | 0e344d32b21457d66572022f6ceb72b77c1188df70068f52c52a5c5505211cc1 |
| `paper/supplementary.md` | dd7277069ced9d4d66c2b57e933d06a9b05cc41aae546b5cefa0c10ddcccc2ee |
| `paper/supplementary_SPIC.md` | 0c746c2127cac8bcb25340172e3859cc3c023d4739e7e8d812967287e554f280 |
| `paper/supplementary_provenance_internal.tsv` | 1162582f16633e11d26d9d1a72fd20a3b04389a51453c3e1e8c2605068002a07 |

**C**: 4 files, main text 19,145 words.

| File | sha256 after |
|---|---|
| `paper/abstract_A.md` | c7be9fb60405f35b8bc27e52d06ea8e4032ac0d91ae2f3c09a37219370f97a40 |
| `paper/sec10_discussion.md` | 3a2ac0007c10daf050a784aff4db54570649460b3cfde026e5dd3b06864ad9c2 |
| `paper/sec1_introduction.md` | 7d6267cd363ceb68ab00760119ff4034f489af81b82b9890a62a2e57e7730233 |
| `paper/sec7_verbosity_sign.md` | 0e344d32b21457d66572022f6ceb72b77c1188df70068f52c52a5c5505211cc1 |

**N**: 7 files, main text 18,933 words.

| File | sha256 after |
|---|---|
| `paper/abstract_A.md` | 20be01d754a70915348cd6d21a0d76e2ae18cce2519a763db09dc42ad28d94d4 |
| `paper/declarations.md` | 8fb28692d32e3688d0694ae6c84353f63d8968032e53f9bdf3c6b933ffbe288b |
| `paper/sec10_discussion.md` | 76c94324d302ef36351e357269c2e6b2cbe1bce24a4ec29552f55f9149d88d62 |
| `paper/sec11_limitations_ethics.md` | 9ff1cd8ecb84b000a08ed9e3f7ab5dc4bef8d745376860fc937c7662ee3523b7 |
| `paper/sec3_measurement_setup.md` | 665c60aa1956df8dedab070db395bd794297fec88cf07d7242c6bc7c31e74575 |
| `paper/supplementary.md` | 0349454b2d0549051da9b64eccf2c12b0843ce51c75882927425dafb6d1ec927 |
| `paper/supplementary_provenance_internal.tsv` | 1162582f16633e11d26d9d1a72fd20a3b04389a51453c3e1e8c2605068002a07 |

**U**: 8 files, main text 19,061 words.

| File | sha256 after |
|---|---|
| `paper/abstract_A.md` | 2ddd6bb3176c412efa0c054c1473847461bf02634524c5d7b4c2a6b38a2a4907 |
| `paper/anon/declarations_anon.md` | ec71a9b953ab3609a31f457b8368814c35a82443035885cfa64d9d8df84a96cb |
| `paper/declarations.md` | 336e29b0453f8185e1e5797c9a81e27c24967f705f5464f7de1a29925d37d504 |
| `paper/number_manifest.tsv` | dd2bce1797bb5bbe52da2d832750038bbfc7f2d39c10d99fe6eacb9de9b716c8 |
| `paper/sec11_limitations_ethics.md` | ad831dea733e47600ba6d22b90ac5097e00a4a332f78ee78ca32f496709bc4d9 |
| `paper/supplementary.md` | 78d33c2c1f19dc4e1dcdc67c6869e31bc5de0df725089d281fb9dcbb58864b0b |
| `paper/supplementary_SPIC.md` | 0c746c2127cac8bcb25340172e3859cc3c023d4739e7e8d812967287e554f280 |
| `paper/supplementary_provenance_internal.tsv` | 82b663b1d2106662c3d1e6a4e9025ecb94288053239de5d1cde40643a87c5998 |

**C+U**: 11 files, main text 19,279 words.

| File | sha256 after |
|---|---|
| `paper/abstract_A.md` | 44f2a36c4a68111078c355c38ca6b346371b17550fcdde893600f5fb9cbb7abf |
| `paper/anon/declarations_anon.md` | ec71a9b953ab3609a31f457b8368814c35a82443035885cfa64d9d8df84a96cb |
| `paper/declarations.md` | 336e29b0453f8185e1e5797c9a81e27c24967f705f5464f7de1a29925d37d504 |
| `paper/number_manifest.tsv` | dd2bce1797bb5bbe52da2d832750038bbfc7f2d39c10d99fe6eacb9de9b716c8 |
| `paper/sec10_discussion.md` | 3a2ac0007c10daf050a784aff4db54570649460b3cfde026e5dd3b06864ad9c2 |
| `paper/sec11_limitations_ethics.md` | ad831dea733e47600ba6d22b90ac5097e00a4a332f78ee78ca32f496709bc4d9 |
| `paper/sec1_introduction.md` | 7d6267cd363ceb68ab00760119ff4034f489af81b82b9890a62a2e57e7730233 |
| `paper/sec7_verbosity_sign.md` | 0e344d32b21457d66572022f6ceb72b77c1188df70068f52c52a5c5505211cc1 |
| `paper/supplementary.md` | 78d33c2c1f19dc4e1dcdc67c6869e31bc5de0df725089d281fb9dcbb58864b0b |
| `paper/supplementary_SPIC.md` | 0c746c2127cac8bcb25340172e3859cc3c023d4739e7e8d812967287e554f280 |
| `paper/supplementary_provenance_internal.tsv` | 82b663b1d2106662c3d1e6a4e9025ecb94288053239de5d1cde40643a87c5998 |

**N+U**: 10 files, main text 19,067 words.

| File | sha256 after |
|---|---|
| `paper/abstract_A.md` | 464e857b5a91374d799f1f286de352bb46adc2b1d227fe3e1ec5f3686a0640d7 |
| `paper/anon/declarations_anon.md` | ec71a9b953ab3609a31f457b8368814c35a82443035885cfa64d9d8df84a96cb |
| `paper/declarations.md` | 5920d0fa7461f0a75cd6aae6d58df7e7588111ba9ad39ff76e1aa3af4c4702ba |
| `paper/number_manifest.tsv` | dd2bce1797bb5bbe52da2d832750038bbfc7f2d39c10d99fe6eacb9de9b716c8 |
| `paper/sec10_discussion.md` | 76c94324d302ef36351e357269c2e6b2cbe1bce24a4ec29552f55f9149d88d62 |
| `paper/sec11_limitations_ethics.md` | a7258f2eddb6e137d6abe6990063ce2cc8a4e8e57c9e6bddcef6161e54d2a1e4 |
| `paper/sec3_measurement_setup.md` | 665c60aa1956df8dedab070db395bd794297fec88cf07d7242c6bc7c31e74575 |
| `paper/supplementary.md` | dd7277069ced9d4d66c2b57e933d06a9b05cc41aae546b5cefa0c10ddcccc2ee |
| `paper/supplementary_SPIC.md` | 0c746c2127cac8bcb25340172e3859cc3c023d4739e7e8d812967287e554f280 |
| `paper/supplementary_provenance_internal.tsv` | 1162582f16633e11d26d9d1a72fd20a3b04389a51453c3e1e8c2605068002a07 |


### 7.4 The apply script

`apply_a_v4.py` in this folder reads the blocks from this file (pinned by sha256), checks that `ea12e51` is an ancestor of the paper HEAD, that `paper/` is clean and that every file it can change has its base sha256, rebuilds the changed files in memory from `git show HEAD:paper/<file>`, runs steps S1 to S3 and the custody assertions, and prints the resulting sha256 values against its target table for the chosen groups. Groups are chosen with `--groups` (default `C,N`). In its default mode it writes nothing. It writes only with `--write --ruling <id>`, only if every result equals the target table, and for group U only with `--pi-decision <LOG id of the investigator's decision>` in addition. If the judge drops or changes a block, `SKIP` is set and the targets are those of the ruling. It never stages or commits. It was run in check mode only, once for each of the seven group combinations; each run ended with ALL RESULTS EQUAL TARGETS and CHECK MODE: nothing written.

### 7.5 What was opened for this package

- Ruling CC-407 (revised text); answer F4 only; decisions LOG lines found by searches for the PI ids and topics named in the evidence lines (addresses masked in the output); `FIX_RESOLUTIONS_2026-11-10.md`; `manuscript/WORKFLOW_LOG.md` lines on D-W14-2.
- Registrations: `2026-10-14_xm3600_predictions.md`, `2026-10-18_g2b_qwen3vl_ladder.md`, `2026-10-28_pascal50s/PREREG.md`, `2026-10-29_a_companion/RULE.md` (the lines cited) and three lines of `2026-10-30_a_t3/PREREG.md`.
- Result files of group C: the six files named in Section 7.2 (the keys named there).
- Run records of group U: the build reports of the n3 backup (fields only), the two run folders (`adapter_config.json`, the first and last line of `metrics.jsonl`, the model card), the line count of one training file (no content displayed), `data/datasets/uitviic/train_data.json` (sha256 and counts only), `c2_n1_uitviic_mstar.json` (structure and system names) and the header of its script, four score files in `data/results/uitviic_ind_test/` and two in `data/results/uitviic/` (name, split, image count and adapter field only), `scripts/queue/adapters_canonical.sha256`, n2 queue scripts `30_p1_s43.sh` and `38_uitviic_eval.sh` and the file names of that queue.
- For N6: a text search of the earlier conference paper's PDF for its training-data sentences.
- Not opened: any label folder, `key.json`, `assignment.json`, `practice.json`, `gt_cache.json`, label `.jsonl` files, the held Paper B folders, `CC-394.txt`, `CC-396.txt`, any mailbox, any answer other than F4. No e-mail was written or sent.
- Two disclosures. A search of the tracked files of the run repo for the adapter names displayed lines of Paper B draft files and of UIT-ViIC score summaries in the session; none is copied here. A search of the numbers manifest for one system name displayed rows keyed to Section 6.7 and Supplementary S11 in the session; none is copied into this package or into any message.
