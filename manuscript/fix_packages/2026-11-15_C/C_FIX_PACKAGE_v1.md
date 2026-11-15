# Paper C (journal version, ACM TALLIP): fix package v1

Written 2026-11-14T21:52Z (2026-11-15 04:52, UTC+7). Nothing in this package has been applied. It is for a judge to read first.

## 0. Scope, inputs and conventions

- **Review list:** section C.14 of `manuscript/bao_cao_khoa_hoc_2026-11-14/parts/C_report.md` (items C.14.1 no. 1–12 and C.14.2 no. 1–11), with the remark blocks of C.2–C.12, and the items of D.16 of `…/parts/D_taimma_report.md` that concern the journal text.
- **Paper:** `/mnt/d/vsps_papers/vsps-paperC-tallip/paper_v1_analysis/` at git HEAD `6a5d36aeee4c22597b4188bb1d84413f04cabddf`. Every OLD string was checked against the HEAD blobs (`git show 6a5d36a:…`), not the working tree. The section files and the manifest are clean against HEAD; only `tex/` and the PDFs differ, and they are not touched here.
- **sha256 (first 16 hex) of the files at HEAD:** `03_method.md` 7e23b048208b1150; `05_preregistration_and_analysis.md` 6a20e24d1426f4b7; `06_results.md` 6e5ffa98c494ea87; `07_disclosures.md` e23e2db301ee831d; `08_english_comparison.md` 05afa220ffe9a3a5; `09_limitations.md` 76fb358f22ac5ad6; `11_supplement_registered_rows.md` c4be508db3eed048; `number_manifest_C.tsv` 6c385c21a7708769. Not changed by any fix: `00_abstract.md` 4c023726251dc023; `01_introduction.md` b731e6371c425657; `10_conclusion.md` 83d466dfb6d692e8.
- **Evidence used:** the manifest (`number_manifest_C.tsv`, cited as "manifest row N" by line number at HEAD), the decision and summary JSON files that manifest rows name, the registrations in `/mnt/d/vsps_papers/vsps-paperC-tallip/prereg/` (byte-equal to the run-repo copies where checked), the attribution registration `manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md`, and the paper's own text. No per-image ledger, caption file, label file or key file was opened, and no script of the study was run.
- **Block format.** Each FIX is one or more blocks. The OLD string is the text between the `OLD>>>` line and the `NEW>>>` line, without the line break that ends it; the NEW string likewise, up to the `EVIDENCE>>>` line. An `END>>>` line closes the block. Blocks are fenced so that no character is changed by rendering.
- **Status words:** FIX (exact pair given), DROPPED (remark wrong, or already answered at HEAD), NEEDS DECISION (no NEW text written; options and a recommendation given), WAITS FOR FREEZE (ruled text exists and is applied after 2026-11-16 12:00, UTC+7).
- **Not fixed by design:** the abstract, the introduction and the conclusion stay byte-unchanged; the four freeze sentences are not touched; nothing here needs a new analysis, a new run or a look at a test set.

## 1. Table of items

### 1.1 Items of C.14.1 (errors or contradictions)

| id | report item | file | status |
|---|---|---|---|
| C-N01 | C.14.1 no. 1: the abstract has no InternVL3 COCO row, Section 7 says it has | `00_abstract.md`, `07_disclosures.md` | NEEDS DECISION |
| C-W01 | C.14.1 no. 2: registered items of the attribution study without an outcome; freeze in the future tense | `03`, `05`, `06`, `07` | WAITS FOR FREEZE |
| C-D01 | C.14.1 no. 2, sub-point: no block numbered 2 is mentioned | `06_results.md` | DROPPED (answered by 6a5d36a) |
| C-F01 | C.14.1 no. 3 and D.16 no. 1: the pass rule of H_G is missing | `06_results.md` | FIX |
| C-N02 | C.14.1 no. 4: entries and distinct images of OV-test | `04_data_and_splits.md` | NEEDS DECISION |
| C-D02 | C.14.1 no. 4, sub-point: each entry is one bootstrap unit | `04_data_and_splits.md` | DROPPED (already stated) |
| C-F02 | C.14.1 no. 5: lost Flickr30K test score file, Section 8.6 | `08_english_comparison.md` | FIX |
| C-F03 | C.14.1 no. 5: the same, Box 2 | `07_disclosures.md` | FIX |
| C-F04 | C.14.1 no. 6 (and C.14.2 no. 9): "untested for … prompts with example images" | `09_limitations.md` | FIX |
| C-N03 | C.14.1 no. 7: the section map of Section 1 omits 6.10 and 6.11 | `01_introduction.md` | NEEDS DECISION |
| C-N04 | C.14.1 no. 7: Tables 15–18 stand before Tables 10–14; "Table 1b" | `02`, `05`, `06`, `08`, `09`, `11` | NEEDS DECISION |
| C-N05 | C.14.1 no. 8: status of the two companion studies | `01_introduction.md`, `V2_PROGRESS_C.md` | NEEDS DECISION |
| C-F05 | C.14.1 no. 9: form of the τ grid | `03_method.md` | FIX (form only; optional) |
| C-F06 | C.14.1 no. 9: predicted probabilities 0.95 / 0.70 against 0.953 / 0.700 | `08_english_comparison.md` | FIX |
| C-N06 | C.14.1 no. 9: "detected" and "DETECTED" | `05`, `06`, `08` | NEEDS DECISION |
| C-F07 | C.14.1 no. 10: Table S22 and Table S16 print two values for one batched contrast | `11_supplement_registered_rows.md` | FIX |
| C-F09 | C.14.1 no. 11: hit-max rate, near-verbatim share, 4-gram copy rate undefined | `11_supplement_registered_rows.md` | FIX (two of the three definitions rest on code; judge to confirm) |
| C-N07 | C.14.1 no. 11: "exploration halves" undefined | `06_results.md` | NEEDS DECISION |
| C-N08 | C.14.1 no. 11: what the filter of the OV-dev halves compares against (and the other filters, C.5 (ii)) | `04_data_and_splits.md` | NEEDS DECISION |
| C-F08 | C.14.1 no. 12: "moved from" headings in the supplement (5 pairs, a–e) | `11_supplement_registered_rows.md` | FIX |
| C-N09 | C.14.1 no. 12: repository link and DOI, author block, ORCID, CCS, anonymity, wide tables, source for the Open Images V7 labels, title of the supplement | several | NEEDS DECISION |

### 1.2 Items of C.14.2 (points to clarify)

| id | report item | file | status |
|---|---|---|---|
| C-F10 | C.14.2 no. 1: basis of the −1.0 floors and of the 0.10 of rule L | `05_preregistration_and_analysis.md` | FIX |
| C-N10 | C.14.2 no. 2: say in the abstract and in Section 1 that InternVL3's registered arm includes the deletion step | `00_abstract.md`, `01_introduction.md` | NEEDS DECISION |
| C-F11 | C.14.2 no. 2: recall beside P2 that 0.351 of InternVL3's `ret` captions are zero-shot captions | `06_results.md` | FIX |
| C-F12 | C.14.2 no. 3: the configuration was picked on the `ret` score | `09_limitations.md` | FIX |
| C-D03 | C.14.2 no. 3: the pooled estimand mixes two configurations (place it beside Table 2) | `03_method.md` | DROPPED (already stated twice; placement only) |
| C-F13 | C.14.2 no. 4: batch size of each backbone | `03_method.md` | FIX (three proposed manifest rows) |
| C-N11 | C.14.2 no. 4: print the prompt template in full | `11_supplement_registered_rows.md` | NEEDS DECISION |
| C-F14 | C.14.2 no. 5: `rand` − `zs` on the test sets has no interval; pointer to τ_any | `06_results.md` | FIX |
| C-N12 | C.14.2 no. 5: a POST HOC `rand` − `zs` row with an interval on the test sets | – | NEEDS DECISION (needs a new analysis; outside this package) |
| C-F15 | C.14.2 no. 6: consequences of K1 and of the single `rand` draw, two pointers in Section 9.1 (pairs a, b) | `09_limitations.md` | FIX |
| C-F16 | C.14.2 no. 7: what a label on a bound means; what a large K_nc means | `06_results.md` | FIX |
| C-N13 | C.14.2 no. 8: weight and style of the attribution part (Sections 5.7, 6.10, 7.5) | `05`, `06`, `07` | NEEDS DECISION |
| C-F04 | C.14.2 no. 9: reason for text-only examples in the main text | `09_limitations.md` | FIX (last clause of C-F04) |
| C-F17 | C.14.2 no. 10: one sentence on multiplicity across registrations | `05_preregistration_and_analysis.md` | FIX |
| C-D04 | C.14.2 no. 10: position on p-values | `05_preregistration_and_analysis.md` | DROPPED (already stated) |
| C-N14 | C.14.2 no. 10: release of the per-image score ledgers | `09`, `10` | NEEDS DECISION |
| C-N15 | C.14.2 no. 11: full text of two works; a dated, systematic literature search | `02`, `11` | NEEDS DECISION (needs new work and the network) |

### 1.3 Items of D.16 that concern the journal text, and three remark-block items outside C.14

| id | report item | file | status |
|---|---|---|---|
| C-F01 | D.16 no. 1: pass rule of H_G | `06_results.md` | FIX (same block as above) |
| C-F18 | D.16 no. 9: the denominator symbol of ΔP_cm (pairs a, b) | `05`, `11` | FIX |
| C-N16 | D.16 no. 5 and remark D.11 (a): sentence on the agreement of the dataset authors | `10_conclusion.md` | NEEDS DECISION |
| C-W02 | D.16 no. 13: check of the † note and of two counts after the freeze | conference draft | WAITS FOR FREEZE (not journal text) |
| C-F19 | remark C.7.1 no. 7 (not in C.14): "for both backbones" after pooled numbers | `06_results.md` | FIX (extra) |
| C-F20 | remark C.9 no. 7 (not in C.14): Figure 1 does not say why Flickr30K is absent | `08_english_comparison.md` | FIX (extra) |
| C-F21 | remark C.7.2 (ii) (not in C.14): "about 2.95" is a difference of two point estimates | `06_results.md` | FIX (extra) |

Counts: FIX 21 ids (27 pairs); DROPPED 4; NEEDS DECISION 16; WAITS FOR FREEZE 2.

## 2. FIX blocks

### C-F01. The pass rule of the guard hypothesis H_G (Section 6.7)

Defect at HEAD: `06_results.md` l.93 reports H_G as "not passed" with a precision change whose interval lies above zero, and no file states the rule (`05_preregistration_and_analysis.md` l.18 and l.37 only name H_G). A reader cannot see why it did not pass.

```text
<<<C-F01 06_results.md OLD>>>
At stage B the guard hypothesis H_G was not passed (stage-B decision file, `ov_dev_b.H_G.passed`): pooled precision change +2.91 [0.46, 5.31], at a stripped CIDEr-D cost of −4.01.
<<<C-F01 06_results.md NEW>>>
At stage B the guard hypothesis H_G was not passed (stage-B decision file, `ov_dev_b.H_G.passed`). H_G is the change in neighbour-only object precision (Section 3.4; all mentions, reference gold) of `ret` at the guard threshold against the same decodes with no deletion (τ = −∞), pooled over the two backbones; the guard threshold is the backbone's frozen τ when that is finite and 0.00 otherwise (0.10 for InternVL3, 0.00 for Qwen2.5-VL). The stage-2 registration (§7.5) passes H_G only if both of two conditions hold: the 95% CI lower bound of this change is above zero, and the pooled stripped CIDEr-D cost of the deletion, `ret` at the guard threshold minus `ret` at τ = −∞, has a point estimate of at least −1.0. The first condition held (pooled precision change +2.91 [0.46, 5.31]); the second did not (cost −4.01), so H_G was not passed.
<<<C-F01 EVIDENCE>>>
Rule: prereg/2026-10-22_c_stage2/PREREG.md §7.5, l.325-333: H_G = NP(ret at tau_G) - NP(ret at -inf), pooled over both backbones; "Pass if both hold: the 95% CI lower bound of H_G is > 0; the CIDEr-D (stripped) cost, ret at tau_G - ret at -inf pooled, has a point estimate >= -1.0". NP = neighbour-only object precision, all mentions, no prefix cut; gold on OV sets = union of the image's references (l.325-326). tau_G rule: same file §2, l.84 (tau if finite, else 0.0).
Numbers: .session_backup/2026-10-22/c_stage2/final/decide_final.json (sha256 prefix 92a1f0e992cb), node ov_dev_b.H_G: pooled.d 2.9058, pooled.lo 0.4604, pooled.hi 5.3097, cost -4.0054, passed False, per_model.qwen25vl_7b.tau_G '0.00', per_model.internvl3_8b.tau_G '0.10'. Manifest rows 3 (passed), 342-345 (d, lo, hi, cost), all used in 06_results.md.
Check of the reading: lo 0.46 > 0, so condition 1 held; cost -4.01 < -1.0, so condition 2 failed.
New numbers in 06_results.md: "0.00" as tau_G and "-1.0" as the cost floor; proposed manifest rows M1 and M2 (section 3). "0.10" is covered by manifest row 59.
<<<C-F01 END>>>
```

### C-F02. The lost Flickr30K test score file, Section 8.6

Defect at HEAD: the loss is stated only in `09_limitations.md` l.28 (which points to Section 8.6) and, in short form, in `10_conclusion.md` l.23. The disclosure list of Section 8.6 (`08_english_comparison.md` l.137–142) does not have it.

```text
<<<C-F02 08_english_comparison.md OLD>>>
- The SESOI of +2.0 was carried over from the Vietnamese registration and not recalibrated for PTB CIDEr-D (Section 8.1); it is far below every E3 margin.
<<<C-F02 08_english_comparison.md NEW>>>
- The per-run score file of this test was lost after the decision step. Its sha256 is recorded in the registered decision file, which is the only remaining record of the test's scores (Section 9.3).
- The SESOI of +2.0 was carried over from the Vietnamese registration and not recalibrated for PTB CIDEr-D (Section 8.1); it is far below every E3 margin.
<<<C-F02 EVIDENCE>>>
Wording: the paper's own sentences in 09_limitations.md l.28 ("One ledger was not preserved: the per-run score file of the Flickr30K test (Section 8.6) was lost after the decision step. Its sha256 is recorded in the registered decision file, which is the only remaining record of that test's scores.").
Record: manifest rows 3759-3770, key .session_backup/2026-10-31/c_t3/T3_DECISION.json::test_ledger_sha256, status removed-ledger-unavailable. No new number.
<<<C-F02 END>>>
```

### C-F03. The same fact in Box 2

```text
<<<C-F03 07_disclosures.md OLD>>>
| Flickr30K registration written after the four earlier test sets were decided; Flickr30K test references read earlier by a companion study | none | references only, before the registration; no system output on the test images | no (Section 8.6) |
<<<C-F03 07_disclosures.md NEW>>>
| Flickr30K registration written after the four earlier test sets were decided; Flickr30K test references read earlier by a companion study | none | references only, before the registration; no system output on the test images | no (Section 8.6) |
| per-run score file of the Flickr30K test lost after the decision step | none on the registered decision; the decision file, which records the lost file's sha256, is the only remaining record of the test's scores | none | no (Sections 8.6 and 9.3) |
<<<C-F03 EVIDENCE>>>
Same evidence as C-F02. The row follows the four columns of Box 2 (item, effect on data, exposure of test data, verdict changed?). "No" in the last column: the loss came after the decision step (09_limitations.md l.28). The reference to Section 8.6 is true only if C-F02 is applied; if C-F02 is not applied, write "(Section 9.3)".
<<<C-F03 END>>>
```

### C-F04. Section 9.2, external validity: prompts with example images

Defect at HEAD: `09_limitations.md` l.22 says the result "is untested for … prompts with example images", while Table 18 (`06_results.md` l.236 and l.241) and Table S19 (`11_supplement_registered_rows.md` l.966) print development rows for that format. The reason for the text-only design stands only in the supplement (l.972).

```text
<<<C-F04 09_limitations.md OLD>>>
and it is untested for other model families or sizes, sampled decoding or prompts with example images.
<<<C-F04 09_limitations.md NEW>>>
and it is untested for other model families or sizes and for sampled decoding. Prompts with example images were not taken to any test set: they have development rows only (Tables 18 and S19), and the text-only design rests on cost and on parity with interleaved examples on the Vietnamese development set B, not on accuracy (Table S19).
<<<C-F04 EVIDENCE>>>
Development rows: Table 18, image-format tau_sel on OV-dev-B and XM-dev500 (data/results/c_attr_1113_b3score/res/B3_SUMMARY.json, block 3; 06_results.md l.236, l.241); Table S19, row "interleaved image-caption examples (RICES format) - text-only ret" on the Flickr30K carve (.session_backup/2026-10-30/c_t1/T1_SUMMARY.json, manifest rows 3830-3835).
Reason for the design: the paper's own sentence, 11_supplement_registered_rows.md l.972 ("The text-only design rests on cost and on that Vietnamese parity, not on accuracy."), with the parity row keyed at manifest rows 3860-3862 (T1_SUMMARY.json::sets.ov_dev_b.contrasts.qwen25vl_7b: ret_img-ret). No number is added.
The last clause (from "and the text-only design") answers C.14.2 no. 9 and can be struck without touching the rest.
For the judge, same sentence, not changed here: "untested for other model families" also has development rows (Aya-Vision-8B: Table 13 E1 and Table 16), and Aya-Vision-8B has registered test rows against LMCap (Table 14) but none for ret - rand.
<<<C-F04 END>>>
```

### C-F05. Form of the τ grid in Section 3.5 (form only; optional)

Defect at HEAD: `03_method.md` l.60 prints the grid as "0.0, 0.1, 0.2, 0.3"; Table 2 (l.69), `07_disclosures.md` l.42 and Table S12 print the same values as 0.00, 0.10, 0.20, 0.30. The values are equal; only the form differs.

```text
<<<C-F05 03_method.md OLD>>>
τ ∈ {−∞, 0.0, 0.1, 0.2, 0.3, +∞}
<<<C-F05 03_method.md NEW>>>
τ ∈ {−∞, 0.00, 0.10, 0.20, 0.30, +∞}
<<<C-F05 EVIDENCE>>>
Registered grid: prereg/2026-10-22_c_stage1/DESIGN.md l.224, written "0.0, 0.1, 0.2, 0.3". The ledger keys and the decision files write two decimals ('0.00', '0.10': decide_final.json::ov_dev_b.H_G.per_model.*.tau_G; manifest row 59 '0.10').
Manifest follow-up if applied: row 55 keys the brace string of Section 3.5 verbatim (number column "{-inf, 0.0, 0.1, 0.2, 0.3, +inf}" in the registration's form) and must take the new printed form with its raw value unchanged; rows 3880-3883 (0.0, 0.1, 0.2, 0.3; used only in 03_method.md) lose their use; rows 3884-3886 (0.00, 0.20, 0.30 "printed" forms) gain 03_method.md; 0.10 is row 59.
Alternative for the judge: no change. Section 3.5 quotes the grid in the registration's own form, and the manifest was built on that. I recommend the fix only if a single printed form is wanted; it changes no value.
<<<C-F05 END>>>
```

### C-F06. Predicted probabilities in the text of Section 8.6

Defect at HEAD: `08_english_comparison.md` l.116 writes "(0.95 and 0.70)"; Table 13 (l.110–111) prints 0.953 and 0.700 for the same two values.

```text
<<<C-F06 08_english_comparison.md OLD>>>
(0.95 and 0.70)
<<<C-F06 08_english_comparison.md NEW>>>
(0.953 and 0.700)
<<<C-F06 EVIDENCE>>>
.session_backup/2026-10-30/c_t2/T2_DECISION.json::full.claims.E1 aya_vision_8b: ret-rand.p_test = 0.95270 (manifest row 3739, "0.953"); ::full.claims.E2 qwen25vl_7b: ret-rand.p_test = 0.70038 (manifest row 3743, "0.700"). Manifest follow-up: rows 3907 and 3908 (the forms 0.95 and 0.70, used only in 08_english_comparison.md) lose their use.
<<<C-F06 END>>>
```

### C-F07. Table S22 and Table S16: two values for the batched `ret` − `rand` of one backbone and set

Defect at HEAD: Table S22 (`11_supplement_registered_rows.md` l.1005) prints τ_sel = +9.25 [7.59, 11.14] for Qwen2.5-VL-7B on OV-dev-B, and Table S16 (l.855) prints `ret` − `rand` = +9.67 [7.68, 11.72] for the same backbone and set, both from batched decodes. Table S22 has an "R, D" column (3, 2), but no sentence says that the two rows are different quantities.

```text
<<<C-F07 11_supplement_registered_rows.md OLD>>>
Aya-Vision-8B's OV-dev-B row contains `rand` arms (τ_sel, τ_marg, τ_any): placebo flagged on this set (Section 6.10.5).
<<<C-F07 11_supplement_registered_rows.md NEW>>>
Aya-Vision-8B's OV-dev-B row contains `rand` arms (τ_sel, τ_marg, τ_any): placebo flagged on this set (Section 6.10.5).

On OV-dev-B the τ_sel column averages R = 3 `rand` draws per image (column "R, D"), whereas the stage-B `ret` − `rand` rows of Tables S16 and S17 use the single draw d0 with the same stored `ret` decodes. The two are different quantities: for Qwen2.5-VL-7B on OV-dev-B this table prints +9.25 [7.59, 11.14] and Table S16 prints +9.67 [7.68, 11.72]. No difference between them is computed.
<<<C-F07 EVIDENCE>>>
Table S22 value: data/results/c_attr_1112_score/res/SUMMARY.json (sha256 prefix 1d78cd205ff8)::batched.ov_dev_b.rows.qwen25vl_7b|tau_sel: d 9.2550, lo 7.5931, hi 11.1371, "R": 3, "D": 2, "registered_R_D": [3, 2] (manifest row 4460 and its lo and hi rows).
Table S16 value: .session_backup/2026-10-22/c_stage2/final/decide_final.json::ov_dev_b.gate.per_model.qwen25vl_7b.vs_rand.d = 9.6696 (manifest row 354), one seeded rand assignment per image (05_preregistration_and_analysis.md l.54).
Same ret decodes: caption of Table S22 ("the ret, zs and rand d0 columns are the stored decodes"), and the scoring parity gate of Section 5.7 (stored per-image scores of the six stage-B OV-dev-B runs reproduced within 1e-4; SUMMARY.json::parity).
The note states the difference of definition and prints the two values; it does not claim that the draws explain the whole gap, which was not computed. The same holds for InternVL3-8B at tau = -inf (+5.19 here, SUMMARY.json row 4478; +5.36 in Table S17, manifest row 385), which the note covers by naming Table S17. No new number.
<<<C-F07 END>>>
```

### C-F08. "moved from" in five headings of the supplement

Defect at HEAD: five headings of `11_supplement_registered_rows.md` keep an editing trace ("moved from Section …"): l.739, l.792, l.803, l.846, l.867. Each NEW keeps the section pointer, in the form the other headings of the supplement already use (for example l.929 and l.955).

```text
<<<C-F08a 11_supplement_registered_rows.md OLD>>>
### Test-run operations (moved from Sections 7 and 8.5 of the main text)
<<<C-F08a 11_supplement_registered_rows.md NEW>>>
### Test-run operations (Sections 7 and 8.5)
<<<C-F08a EVIDENCE>>>
The main text cites this section by its name only ("Test-run operations": 04_data_and_splits.md l.26, 07_disclosures.md l.3, 08_english_comparison.md l.82, 09_limitations.md l.9); the name is unchanged.
<<<C-F08a END>>>
```

```text
<<<C-F08b 11_supplement_registered_rows.md OLD>>>
- **Pinned revisions (moved from Section 3.3).**
<<<C-F08b 11_supplement_registered_rows.md NEW>>>
- **Pinned revisions (Section 3.3).**
<<<C-F08b EVIDENCE>>>
03_method.md l.33 points to "the supplement, Instrument definitions" for the hub ids and revisions; the bullet stays in that section.
<<<C-F08b END>>>
```

```text
<<<C-F08c 11_supplement_registered_rows.md OLD>>>
### Context from published systems (moved from Section 8.7)
<<<C-F08c 11_supplement_registered_rows.md NEW>>>
### Context from published systems (Section 8.7)
<<<C-F08c EVIDENCE>>>
Section 8.7 exists in the main text (08_english_comparison.md l.144) and points to Table S15, which this section holds.
<<<C-F08c END>>>
```

```text
<<<C-F08d 11_supplement_registered_rows.md OLD>>>
### Stage B and the decomposition of InternVL3's contrast (moved from Section 6.7)
<<<C-F08d 11_supplement_registered_rows.md NEW>>>
### Stage B and the decomposition of InternVL3's contrast (Section 6.7)
<<<C-F08d EVIDENCE>>>
Section 6.7 (06_results.md l.93) points to Tables S16-S17, which this section holds.
<<<C-F08d END>>>
```

```text
<<<C-F08e 11_supplement_registered_rows.md OLD>>>
### Disclosure detail (moved from Sections 5.4, 6.8, 7.1, 7.2, 8.1 and 8.5 of the main text)
<<<C-F08e 11_supplement_registered_rows.md NEW>>>
### Disclosure detail (Sections 5.4, 6.8, 7.1, 7.2, 8.1 and 8.5)
<<<C-F08e EVIDENCE>>>
The main text cites this section by its name only ("Disclosure detail": 02_related_work.md l.22, 05_preregistration_and_analysis.md l.116, 07_disclosures.md l.3); each sub-heading of the section already carries its own section pointer (l.869, l.875, l.888, l.898, l.906, l.913).
<<<C-F08e END>>>
```

### C-F09. Definitions of the three copy and token-limit diagnostics (judge to confirm)

Defect at HEAD: the stage-A rule of Section 3.5 (`03_method.md` l.57–58) uses the near-verbatim copy share and the hit-max rate, and Tables S1–S4, S6, S10 and S11 print them with the 4-gram copy rate; "Instrument definitions" (`11_supplement_registered_rows.md` l.782–790) defines none of the three.

```text
<<<C-F09 11_supplement_registered_rows.md OLD>>>
of the companion scoring study's verifier protocol; the score is defined in Section 3.4.
<<<C-F09 11_supplement_registered_rows.md NEW>>>
of the companion scoring study's verifier protocol; the score is defined in Section 3.4.
- **Copy and token-limit diagnostics (Section 3.5; Tables S1–S4, S6, S10 and S11).** The *4-gram copy rate against the memory* is the share of a caption's syllable 4-grams that are found in the shown caption of any memory cluster; the zero-shot arm is its baseline. The *near-verbatim copy share* is the share of captions whose copy statistic m against the examples shown with them is at least 0.90; m is the maximum, over those examples, of the larger of 1 − (edit distance / length of the longer of the two captions) and the single-reference BLEU-4, both computed on syllables. The *hit-max rate* is the share of captions whose generation reached the limit of 60 new tokens without an end-of-sequence token.
<<<C-F09 EVIDENCE>>>
4-gram copy rate: prereg/2026-10-22_c_stage1/DESIGN.md §6.2, l.256 ("the share of the caption's syllable 4-grams found in any shown-caption of any memory cluster. zs is the baseline."). Settled by the registration.
Near-verbatim copy share: DESIGN.md l.257 ("captions with rl_reward.copy_stat m >= 0.90 against the examples shown"). The registration names the statistic and its threshold but does not write its formula. The formula in NEW is read from code: scripts/rl_reward.py l.147-151 (m = max over references of max(1 - edit/max(len), single-reference BLEU-4)), called on syllables against the shown examples in scripts/c_stage1/score.py l.42 and l.170-171.
Hit-max rate: DESIGN.md l.258 names it and l.276 sets its limit; no registration text defines it. The definition in NEW is read from code: scripts/lb/decode_hf_vlm.py l.213-217 (the flag is set when no end-of-sequence token occurs within max_new_tokens); the limit of 60 new tokens is DESIGN.md §4.2 (manifest row 43).
Limit of this evidence: the code files were read as they stand today in the run repo (sha256 prefixes rl_reward.py 3b18b7a3620c, score.py 258daa8499d6, decode_hf_vlm.py e2de18811e2f); I did not check them against the hashes pinned at stage A. If the judge wants registration text only, keep the first sentence of the bullet and the first clause on the near-verbatim share (up to "at least 0.90"), and strike the rest.
New number in 11_supplement_registered_rows.md: 0.90 (proposed manifest row M3); 60 has row 43, whose used_in column gains 11_supplement_registered_rows.md.
<<<C-F09 END>>>
```

### C-F10. Where the −1.0 floors and the 0.10 of rule L came from (Section 5.2)

Defect at HEAD: `05_preregistration_and_analysis.md` l.52 explains the origin of the SESOI only; the −1.0 floors of P2 and XM-b and the 0.10 of rule L (Table 4, l.61–65) have no stated origin.

```text
<<<C-F10 05_preregistration_and_analysis.md OLD>>>
Descriptive context for its size, added post hoc, is in Section 5.4.
<<<C-F10 05_preregistration_and_analysis.md NEW>>>
Descriptive context for its size, added post hoc, is in Section 5.4.

**Where the other thresholds came from.** The −1.0 floor on ΔP_cm (P2) and the 0.10 threshold of rule L are fixed values of the design note written before stage A; the −1.0 floor on verified precision (XM-b) is a fixed value of the stage-B registration. All three were set before any stage-B output and carried unchanged into the test registration. As with the SESOI, the registrations record no derivation or calibration of them.
<<<C-F10 EVIDENCE>>>
Floor on dP_cm: prereg/2026-10-22_c_stage1/DESIGN.md §7.2 l.274 (eligibility, >= -1.0) and §7.3 l.284 (A2, lower bound > -1.0); stage-2 PREREG.md §7.2 G2 (l.296) and §8 P2 (l.349); test PREREG.md l.184. Rule L: DESIGN.md l.289 (0.10); stage-2 PREREG.md l.298; test PREREG.md l.161. Floor on verified precision: stage-2 PREREG.md §7.3 S2 (l.310) and §8 "Secondary XM" (l.352); test PREREG.md l.195 and l.355 ("PCM floor -1.0, VP floor -1.0").
"No derivation or calibration recorded": I searched the three files (DESIGN.md, stage-2 PREREG.md, test PREREG.md) for every occurrence of -1.0 and of the 0.10 length threshold; each occurrence states the value or cites a ruling number, and none gives a derivation. The rulings themselves were not read; if one of them holds a reason, the last sentence should be replaced by that reason.
Consistent with the paper's own sentence at l.40 ("the SESOI and every threshold come from the stage-B registration or from the plan written before stage A"). Numbers -1.0 and 0.10 are manifest rows 79-81, already used in this file.
<<<C-F10 END>>>
```

### C-F11. Beside P2: the share of InternVL3's `ret` captions that are zero-shot captions (Section 6.2)

Defect at HEAD: `03_method.md` l.72 says that 0.351 of InternVL3's `ret` captions fell back to the zero-shot caption and have a ΔP_cm of zero by construction; the P2 paragraph (`06_results.md` l.45) does not recall it beside the verdict.

```text
<<<C-F11 06_results.md OLD>>>
for either backbone. P2 does not compare `ret` with `rand`.
<<<C-F11 06_results.md NEW>>>
for either backbone. P2 does not compare `ret` with `rand`. InternVL3's row is at its frozen τ = 0.10, where 0.351 of its `ret` captions fell back to the zero-shot caption and so have a ΔP_cm of zero by construction (Section 3.5); the same decodes without the deletion step give +5.80 (Table S1; Section 6.6).
<<<C-F11 EVIDENCE>>>
0.351: ledger_ov_test_1941.jsonl::ct_internvl3_8b_ov_test-ret-k4-last-T2@0.10:fallback_rate = 0.35085 (manifest row 339, already used in 06_results.md). +5.80: the same ledger, ...@-inf:pcm_vs_zs = 5.798 (manifest row 499, already used in 06_results.md). The ledger itself was not opened; the two values are read from the manifest rows.
Wording: 03_method.md l.72 ("for those captions dP_cm against zs is zero by construction") and 06_results.md l.89 ("dP_cm against zs +1.57 against +5.80"). No new number, no new claim.
<<<C-F11 END>>>
```

### C-F12. The configuration was picked on the `ret` score (Section 9.2)

Defect at HEAD: Section 3.5 (`03_method.md` l.55–60) says that the stage-A rule picked the highest stripped CIDEr-D among the `ret` runs; no limitation says that `ret` − `rand` is therefore measured at a configuration picked for `ret`.

```text
<<<C-F12 09_limitations.md OLD>>>
Configurations were frozen on development data and each test set was looked at once.
<<<C-F12 09_limitations.md NEW>>>
Configurations were frozen on development data and each test set was looked at once. Each backbone's configuration was picked from its `ret` runs alone (Section 3.5), and `rand` and `fix` run at the picked k, tail and τ, so `ret` − `rand` is measured at a configuration selected on the `ret` score; the `rand` and `fix` runs at the other stage-A settings are listed in Table S10.
<<<C-F12 EVIDENCE>>>
prereg/2026-10-22_c_stage1/DESIGN.md §7.2 l.272-277 ("For each backbone, the candidates are the 7 ret runs x 6 thresholds ... Pick the eligible candidate with the highest stripped CIDEr-D") and §7.3 l.282 ("Each backbone uses its picked (ret run, tau), and rand and fix at the same k, template and tau").
Table S10 (11_supplement_registered_rows.md l.279-493) lists rand and fix runs on KTVIC dev299 at k = 2, 4, 8 with tail T1 (and k = 4 with tail T2 for InternVL3-8B), so the NEW sentence does not say that other settings were never run for rand; it says only which runs the pick rule read.
Placed in the paragraph on researcher degrees of freedom so that "One threat remains" in the paragraph on internal validity (l.18) stays true as written. No number.
<<<C-F12 END>>>
```

### C-F13. Batch size of each backbone (Section 3.3)

Defect at HEAD: Section 6.10.2 shows that the batch changes greedy captions and `09_limitations.md` l.28 says the batch size of each backbone is fixed in the code; no section prints the batch sizes.

```text
<<<C-F13 03_method.md OLD>>>
Every snapshot file and virtual environment is pinned by hash, unchanged from stage A (hub ids and revisions in the supplement, "Instrument definitions").
<<<C-F13 03_method.md NEW>>>
Every snapshot file and virtual environment is pinned by hash, unchanged from stage A (hub ids and revisions in the supplement, "Instrument definitions"). Outside the runs stated to be at batch size 1 (Section 6.10.2), captions are decoded in fixed batch slices of 4 images for Qwen2.5-VL-7B and 2 for InternVL3-8B, as registered in the design note of stage A; Aya-Vision-8B (Section 3.7) is registered at 2.
<<<C-F13 EVIDENCE>>>
prereg/2026-10-22_c_stage1/DESIGN.md §4.2, table l.179-182: batch 4 (qwen25vl_7b), batch 2 (internvl3_8b); l.186 "lb.decode_slices with fixed slices". Carried on: prereg/2026-10-27_c_en/PREREG.md l.48 ("the B-N1 batch sizes ... unchanged") and l.87 ("fixed batch slices"); prereg/2026-10-28_c2_ablation/PREREG.md l.93 ("b = 4 / 2").
Aya-Vision-8B: prereg/2026-10-30_c_t1/c_t1_registry.json::models.aya_vision_8b.batch_size = 2.
Runs at batch size 1: 06_results.md l.142 (LMCap re-implementation and the interleaved image-caption arm) and l.144 (attribution arms, block 1b and block 3).
Limit of this evidence: these are the registered values. The run files that record the batch size of each decode hold captions and were not opened; the decoder checks the batch size as a provenance field against the registry (scripts/lb/decode_hf_vlm.py l.46).
New numbers in 03_method.md: proposed manifest rows M4, M5, M6 (section 3).
<<<C-F13 END>>>
```

### C-F14. `rand` − `zs` on the test sets: pointer to the development rows that have intervals (Section 6.4)

Defect at HEAD: `06_results.md` l.71 says that the `rand` − `zs` comparison on the test sets is descriptive, with no interval; rows of the same contrast with intervals exist on development data (Section 6.8 l.118; Table 16 l.174–176) and are not pointed to.

```text
<<<C-F14 06_results.md OLD>>>
random examples from the same memory already score well above zero-shot for both backbones on both sets.
<<<C-F14 06_results.md NEW>>>
random examples from the same memory already score well above zero-shot for both backbones on both sets. Development rows of this contrast with intervals are in Section 6.8 (pooled, OV-dev-B) and in Table 16 (τ_any, per backbone, at batch size 1 and with InternVL3 at τ = −∞); they are development rows, not test results.
<<<C-F14 EVIDENCE>>>
Section 6.8, 06_results.md l.118 (pooled rand - zs on OV-dev-B, post hoc remark). Table 16, l.174-176 (tau_any rows; data/results/c_attr_1112_score/res/VERDICT.json::sets.ov_dev_b.rows.*|tau_any). tau_any is defined as rand - zs in 03_method.md l.107; InternVL3-8B runs at tau = -inf in that study (03_method.md l.104).
A pointer only: no number is repeated, no interval is attached to a test row, and Section 6.4 keeps its sentence that the test comparison has no registered contrast or CI. The other option of the report, a POST HOC row with an interval on the test sets, is C-N12.
<<<C-F14 END>>>
```

### C-F15. Section 9.1: two pointers to the attribution study's rows

Defect at HEAD: the bullet on batch composition (`09_limitations.md` l.11) does not point to the tables that print batched and batch-size-1 rows of the same contrasts; the bullet on the single `rand` draw (l.9) does not point to the development estimate of the draw's share of variance or to the flagged placebo (`06_results.md` l.192).

```text
<<<C-F15a 09_limitations.md OLD>>>
the check is by string identity and says nothing about which policy gives better captions.
<<<C-F15a 09_limitations.md NEW>>>
the check is by string identity and says nothing about which policy gives better captions. The batched rows of the same development contrasts are printed in Table S22, beside the batch-size-1 rows of Tables 15, 16 and S21; the paper computes no difference between the two decoding policies.
<<<C-F15a EVIDENCE>>>
Table S22 (11_supplement_registered_rows.md l.999-1012): batched rows on OV-dev-A, OV-dev-B and XM-dev500. Batch-size-1 rows of the same sets: Table 15 (06_results.md l.148-157), Table 16 (l.161-176), Table S21 (11_... l.991-997). 06_results.md l.225 calls Table S22 "a descriptive sensitivity row". No difference between the policies is printed anywhere in the files at HEAD. No number.
<<<C-F15a END>>>
```

```text
<<<C-F15b 09_limitations.md OLD>>>
they do not include the variation from drawing other random examples, or run-to-run variation.
<<<C-F15b 09_limitations.md NEW>>>
they do not include the variation from drawing other random examples, or run-to-run variation. Development estimates of the share of the image-bootstrap variance of `ret` − `rand` that the random draw accounts for, and a `rand` d1 − d2 placebo that was flagged for one backbone on one set, are in Section 6.10.5; no test interval is widened, recomputed or relabelled with them.
<<<C-F15b EVIDENCE>>>
06_results.md l.192 (placebo of Aya-Vision-8B on OV-dev-B flagged; six variance shares) and Table S23(a) (11_... l.1018-1025). The last clause repeats the registered sentence of 05_preregistration_and_analysis.md l.166 ("No test interval is widened, recomputed or relabelled with a number from this analysis."). No number is carried into Section 9.1.
<<<C-F15b END>>>
```

### C-F16. Section 6.10.6: what a label on a bound means

Defect at HEAD: Table 17 (`06_results.md` l.200–213) puts the label REVERSED on L_cp, which is a lower bound, and DETECTED on K_nc in every row; the text repeats the registered reading sentence for each row and does not say how these two labels are to be read.

```text
<<<C-F16 06_results.md OLD>>>
The English copy bound on the Flickr30K carve and Flickr30K val, registered as a post hoc row, was not coded and was not run.
<<<C-F16 06_results.md NEW>>>
**Reading the labels of Table 17.** L_cp is a lower bound, so the label REVERSED on it says only that the interval of the bound lies below zero: on that row the bound gives no information about the part of the retrieval contrast that does not travel through copied n-grams (the registered reading above), and it does not say that this part is negative. K_nc is the direction check of assumption A_cp (Section 3.8): the `rand` caption never saw R_q, so a K_nc labelled DETECTED is overlap that needs no copying, of the sign the registration expected. The bound therefore stays in force on every row, and K_ret remains an upper bound that can only overstate copying.

The English copy bound on the Flickr30K carve and Flickr30K val, registered as a post hoc row, was not coded and was not run.
<<<C-F16 EVIDENCE>>>
manuscript/prereg/2026-11-11_c_attr_dev/C_ATTR_DEV_PREREG_v1_1.md §8, l.378 (L_cp "a lower bound on the retrieval-specific effect that does not travel through copied n-grams"), l.379 ("K_ret can only overstate copying"), l.380 ("the rand caption never saw R_q, so K_nc measures overlap that needs no copying. Expected sign: >= 0. If K_nc is REVERSED on a set ... the bound is withdrawn for that set"), l.382 (reading sentences); §7.4 l.283 (REVERSED = the 95% upper bound < 0).
Table 17: column "bound" is "in force" on all twelve rows (06_results.md l.202-213); K_nc is DETECTED on all twelve.
For the judge: Section 6.10.6 was transferred from the ruled paper-text package of the attribution study. The paragraph adds no number, no label and no reading sentence; each statement restates §8 or the definition of REVERSED. It does not touch any string that the after-freeze transfer uses (section 5).
<<<C-F16 END>>>
```

### C-F17. One sentence on multiplicity across the registrations (Section 5.4)

Defect at HEAD: the Multiplicity bullet (`05_preregistration_and_analysis.md` l.113) lists what each registration controls and does not say that nothing is claimed across them.

```text
<<<C-F17 05_preregistration_and_analysis.md OLD>>>
Everything else is secondary, reported with unadjusted CIs, with no family-wise claim.
<<<C-F17 05_preregistration_and_analysis.md NEW>>>
Everything else is secondary, reported with unadjusted CIs, with no family-wise claim. Each registration controls its own family, and no error rate is claimed over the five one-look test sets taken together.
<<<C-F17 EVIDENCE>>>
The same bullet, l.113: P1 single primary; P2 intersection-union; the XM prediction a conjunction; S-NC gated in a fixed order after P1-EN; the three Flickr30K claims Holm-adjusted. Five one-look test sets: OV-test, XM-test2500, COCO Karpathy test, NoCaps val (Sections 5.1 and 8.1) and Flickr30K test, "a fifth one-look test set" (08_english_comparison.md l.95). The sentence states what the paper does not claim; it adds no statistic.
<<<C-F17 END>>>
```

### C-F18. The denominator symbol of ΔP_cm (Table 4 and "Instrument definitions")

Defect at HEAD: Table 4 (`05_preregistration_and_analysis.md` l.63) and the supplement (`11_supplement_registered_rows.md` l.788) write the denominator as "Σ k_cm"; both places define k_i and never say what k_cm is.

```text
<<<C-F18a 05_preregistration_and_analysis.md OLD>>>
and tp counts the first k_i classes that the gold supports.
<<<C-F18a 05_preregistration_and_analysis.md NEW>>>
and tp counts the first k_i classes that the gold supports; Σ k_cm in Table 4 is the sum of k_i over the images.
<<<C-F18a EVIDENCE>>>
prereg/2026-10-25_c_test/PREREG.md l.181 writes the registered estimand as "100 * (sum tp_cm - sum tp_cm_zs) / sum k_cm over images"; prereg/2026-10-22_c_stage1/DESIGN.md §6.2 l.254 writes the same quantity as "... / sum k_i" with k_i = min(|M_i(run)|, |M_i(zs)|). Table 4 keeps the test registration's symbol; the added clause links the two.
<<<C-F18a END>>>
```

```text
<<<C-F18b 11_supplement_registered_rows.md OLD>>>
ΔP_cm = 100 · (Σ tp_cm − Σ tp_cm,zs) / Σ k_cm.
<<<C-F18b 11_supplement_registered_rows.md NEW>>>
ΔP_cm = 100 · (Σ tp_cm − Σ tp_cm,zs) / Σ k_cm, where Σ k_cm is the sum of k_i over the images.
<<<C-F18b EVIDENCE>>>
Same evidence as C-F18a.
<<<C-F18b END>>>
```

### C-F19 (extra, remark C.7.1 no. 7). "for both backbones" after pooled numbers (Section 6.4)

Defect at HEAD: `06_results.md` l.75 gives four pooled differences and ends "for both backbones"; the per-backbone rows are in Table S5 and are not cited in that sentence.

```text
<<<C-F19 06_results.md OLD>>>
+40.28 [38.50, 42.08] on XM-test2500, for both backbones.
<<<C-F19 06_results.md NEW>>>
+40.28 [38.50, 42.08] on XM-test2500; each backbone's own rows are also above zero, with CIs above zero (Table S5).
<<<C-F19 EVIDENCE>>>
Table S5 (11_supplement_registered_rows.md l.186-194), columns "ret - NN-top1" and "ret - NN-consensus": OV-test primary, Qwen2.5-VL +17.08 [15.57, 18.72] and +10.85 [9.22, 12.47], InternVL3 +10.89 [9.31, 12.51] and +7.45 [5.90, 9.05]; XM-test2500, Qwen2.5-VL +43.75 [41.59, 46.04] and +42.32 [40.17, 44.62], InternVL3 +38.89 [36.95, 40.83] and +38.24 [36.25, 40.28]. All eight lower bounds are above zero. No number is added to Section 6.4.
<<<C-F19 END>>>
```

### C-F20 (extra, remark C.9 no. 7). Figure 1: why Flickr30K is not shown

Defect at HEAD: the caption of Figure 1 (`08_english_comparison.md` l.65) covers four scored sets and does not say why the fifth test set is absent.

```text
<<<C-F20 08_english_comparison.md OLD>>>
dashed line: the registered +2.0, a different quantity on each scale.](fig1_ret_minus_rand.svg)
<<<C-F20 08_english_comparison.md NEW>>>
dashed line: the registered +2.0, a different quantity on each scale. Flickr30K test is not shown: no `ret` − `rand` contrast was taken to that test (Section 8.6).](fig1_ret_minus_rand.svg)
<<<C-F20 EVIDENCE>>>
08_english_comparison.md l.116 ("neither was taken to test and no rand arm was decoded on Flickr30K test"). The figure file is not changed. No number.
<<<C-F20 END>>>
```

### C-F21 (extra, remark C.7.2 (ii)). "about 2.95" is a difference of two point estimates (Section 6.8)

Defect at HEAD: `06_results.md` l.116 says the deletion step "accounts for about 2.95" of the shortfall and gives no interval; the value is the difference of two point estimates.

```text
<<<C-F21 06_results.md OLD>>>
shortfall (+5.36 → +2.41).
<<<C-F21 06_results.md NEW>>>
shortfall (+5.36 → +2.41; the difference of two point estimates, for which no interval is reported).
<<<C-F21 EVIDENCE>>>
Manifest row 3672: "derived::OV-dev-B InternVL3 ret-rand at tau=-inf minus at tau=0.10 (devb_decomposition.json ret_minus_rand_tauneginf.d - ret_minus_rand_tau010.d)" = 2.9454, status derived-post-hoc. Table S17 (11_... l.860-863) prints intervals for the two contrasts and for the two per-arm costs, and none for their difference. No new number.
<<<C-F21 END>>>
```

## 3. Proposed manifest rows and follow-ups

Six columns as in `number_manifest_C.tsv` (number, file::key, raw_value, sha256_prefix, status, used_in). `<TAB>` stands for one tab character. The sha256 prefixes are the first 12 hex digits of the source files as they stand now.

```text
M1 (C-F01)  -1.0<TAB>manuscript/prereg/2026-10-22_c_stage2/PREREG.md::§7.5 H_G pass rule, CIDEr-D cost floor (l.332)<TAB>-1.0<TAB>6d039398c88a<TAB>design<TAB>06_results.md
M2 (C-F01)  0.00<TAB>.session_backup/2026-10-22/c_stage2/final/decide_final.json::ov_dev_b.H_G.per_model.qwen25vl_7b.tau_G<TAB>'0.00'<TAB>92a1f0e992cb<TAB>reader-reference<TAB>06_results.md
M3 (C-F09)  0.90<TAB>manuscript/prereg/2026-10-22_c_stage1/DESIGN.md::§6.2 near-verbatim copy share, copy_stat m >= (l.257)<TAB>0.90<TAB>eacc9a9c737c<TAB>design<TAB>11_supplement_registered_rows.md
M4 (C-F13)  4<TAB>manuscript/prereg/2026-10-22_c_stage1/DESIGN.md::§4.2 batch, qwen25vl_7b (l.181)<TAB>4<TAB>eacc9a9c737c<TAB>design<TAB>03_method.md
M5 (C-F13)  2<TAB>manuscript/prereg/2026-10-22_c_stage1/DESIGN.md::§4.2 batch, internvl3_8b (l.182)<TAB>2<TAB>eacc9a9c737c<TAB>design<TAB>03_method.md
M6 (C-F13)  2<TAB>manuscript/prereg/2026-10-30_c_t1/c_t1_registry.json::models.aya_vision_8b.batch_size<TAB>2<TAB>09e6f90a0973<TAB>prereg-quoted<TAB>03_method.md
```

Follow-ups in the `used_in` column, no new row:
- C-F05: row 55 (the brace string) takes the new printed form; rows 3880–3883 lose `03_method.md`; rows 3884–3886 gain it.
- C-F06: rows 3907 and 3908 lose `08_english_comparison.md`.
- C-F09: row 43 (60 new tokens) gains `11_supplement_registered_rows.md`.
- All other FIX blocks reuse numbers whose rows already name the file, or add no number.

The manifest check of the paper repo was not run (nothing was applied). The rows above are what I expect it to ask for; the judge or the applier should run it after applying.

## 4. NEEDS DECISION (no NEW text written)

**C-N01. The abstract and Section 7 disagree on InternVL3's COCO row (C.14.1 no. 1).** `07_disclosures.md` l.17 (Box 2: "per-backbone rows quoted in the abstract and contributions") and l.28 ("the abstract and the contributions quote InternVL3's COCO per-backbone row as descriptive context … because the pooled number alone would overstate the effect") describe an abstract that no longer exists: `00_abstract.md` l.7 gives the pooled COCO number with PASS and no InternVL3 COCO row. The row is in Section 1 (contribution 2), Section 9.1 and Section 10. The abstract body has 193 words against a limit of 200.
- Option A: put the row back into the abstract (−1.64 [−2.79, −0.49], or the words "below zero for InternVL3"). The abstract is frozen and has 7 words of room, so other words must go; this needs the investigator.
- Option B: leave the abstract and correct the two sentences of Section 7 to say that the contributions and the conclusion quote the row. The reason given in l.28 would then describe a pooled number that stands alone in the abstract.
- Recommendation: A. It is the option that agrees with the paper's own reason and with its last sentence on per-backbone results. If the investigator declines, apply B and drop the clause "because the pooled number alone would overstate the effect" for the abstract. Decision: the investigator.

**C-N02. Entries and distinct images of OV-test (C.14.1 no. 4).** The test registration (`prereg/2026-10-25_c_test/PREREG.md` l.74 and l.365) states 2,001 entries with 1,997 distinct images and, for the primary set, 1,941 entries with 1,937 distinct images, both entries of a pair being kept as separate bootstrap units. The paper calls 1,941 and 2,001 "images" (Table 3 l.14–15; the abstract) and gives no distinct count. Manifest rows 71–73 hold exactly these numbers with the status `removed-PI-1101o`: they were taken out on the investigator's instruction, which was later replaced by the rule to state such facts where they affect a reported number.
- Option A: restore one sentence in Section 4 with the two pairs of counts, and set rows 71–73 back to a keyed status.
- Option B: leave the text; `04_data_and_splits.md` l.24 already says that each of the 2,001 entries is one bootstrap unit.
- Recommendation: A. The count of bootstrap units is behind every OV-test interval, and the registrations will be released with the paper, so a reader will see both numbers. Decision: the investigator, because the removal was the investigator's.

**C-N03. The section map of Section 1 (C.14.1 no. 7).** `01_introduction.md` l.36 names Sections 6.8 and 6.9 as the end of Section 6; Sections 6.10 and 6.11 exist. The introduction is frozen. Options: add one clause to the map at the investigator's rewrite; or leave it. Recommendation: add the clause, with the label "development, non-confirmatory" for 6.10. Decision: the investigator.

**C-N04. Table numbers (C.14.1 no. 7).** Tables 15–18 (Section 6.10) stand before Tables 10–14 (Section 8), and "Table 1b" has no number of its own. A simple pattern count finds 35 references to Tables 10–18 in files 05, 06, 08, 09 and 11, some in compound form ("Tables 13, 14 and S19", "Tables 15 and 16", "Tables 16 and S21", "Tables 7, 8 and 11").
- Option A: renumber by one scripted pass, after the after-freeze transfer, with the map 15→10, 16→11, 17→12, 18→13, 10→14, 11→15, 12→16, 13→17, 14→18. A swap of this kind cannot be applied safely as separate OLD/NEW pairs, because a NEW of one pair is an OLD of another. No frozen file cites Tables 10–18.
- Option B: leave the numbers until the investigator's rewrite and let the LaTeX build number the tables.
- "Table 1b": giving it its own number shifts every later table by one, and the frozen files cite Table 3 (`01_introduction.md` l.5) and Table 6 (`10_conclusion.md` l.9).
- Recommendation: A for Tables 10–18, by script with an exact-count check; leave "Table 1b" for the investigator's rewrite. Decision: a judge (A), the investigator (Table 1b).

**C-N05. Status of the two companion studies (C.14.1 no. 8).** `01_introduction.md` l.3 and l.16 say "in preparation"; `V2_PROGRESS_C.md` l.16, a progress note and not paper text, says "under review". Only the investigator knows the status at submission. Recommendation: keep the paper as it is until one of the two is submitted; correct the progress note; check again on the day of submission. Decision: the investigator.

**C-N06. "detected" and "DETECTED" (C.14.1 no. 9).** Both are registered words: "detected" is the label of the secondary in the test registration (`prereg/2026-10-25_c_test/PREREG.md` l.249) and in the English registration (`prereg/2026-10-27_c_en/PREREG.md` l.113); DETECTED is the first of the four labels of the attribution registration (§7.4). Box 1 (`05_preregistration_and_analysis.md` l.20 and l.23) already separates them. Options: no change; or mark the attribution labels with a device that survives typesetting. Recommendation: no change to either word; renaming one would depart from a registration. Decision: a judge.

**C-N07. "exploration halves" (C.14.1 no. 11).** `06_results.md` l.122 and Box 2 (`07_disclosures.md` l.21) speak of "the exploration halves of the KTVIC and OpenViIC test sets" used as a guard set by another study. No file of the paper, and no registration in the paper's `prereg/` folder, defines these halves; they belong to the registration of that other study. Options: add one clause that says how that study split the two test sets and when (before or after the registered look of this paper), with the source named by a judge; or reword without the term. Recommendation: the first, because the point bears on the re-use of a test set after its look. I could not settle the definition from the allowed files. Decision: a judge.

**C-N08. What each "pre-specified filter" compares against (C.14.1 no. 11; remark C.5 (ii)).** The registrations settle the wording: the OV-dev halves (`prereg/2026-10-22_c_stage1/DESIGN.md` §2.3 l.85–87: half A is filtered against the exclusion list, KTVIC test, OpenViIC test, XM3600, the KTVIC development carve and the unfiltered half B; half B against the same sets without half A; counts 1,005 → 911 and 1,006 → 925 in `LISTS_ADDENDUM.md` l.14–15); KTVIC dev299 (DESIGN §2.2: one image of the carve matched to a test image; manifest row 61, status `removed-PI-1101o`); the 997 Flickr30K test images (`prereg/2026-10-31_c_t3/PREREG.md` §6, the test-side pass). The paper states the rule for the memory (Section 3.1) and for the 60 OV-test images (Section 4) and says only "a pre-specified filter" for the other three. These sentences were shortened under the investigator's earlier instruction on overlap wording.
- Option A: one clause per filter in Section 4, in the words of the registrations.
- Option B: leave the text.
- Recommendation: A, since each filter fixes a set size that the paper reports. Decision: a judge under the current overlap rule; the investigator if the judge sees a conflict with it.

**C-N09. Open places in the record (C.14.1 no. 12).** (i) Repository link and archive DOI: `10_conclusion.md` l.25, frozen; the investigator. (ii) Author block, ORCID, CCS codes, anonymity mode: the investigator, from the venue's current page. (iii) Wide tables of the supplement (S1–S4, S10–S12, S24): a build matter, outside the section files. (iv) Source for the Open Images V7 human-verified labels: the text names the labels (`03_method.md` l.80; `11_…` l.788) and cites no source in the section files; `paperC.bib` holds only the V4 dataset paper. A fix needs a new reference, which this package may not add; recommendation: a judge adds the release reference after checking it. (v) Title of the supplement ("Registered per-run rows" no longer fits its content): a restructuring choice for the investigator's rewrite.

**C-N10. Say in the abstract and in Section 1 that InternVL3's registered arm includes the deletion step (C.14.2 no. 2; remarks C.2 and C.7.1 no. 1).** Both files are frozen. The fact is stated in Section 3.5 and in Section 6.2 (and beside P2 after C-F11). Options: one design clause in the abstract and in contribution 2; or leave them. Recommendation: add the clause at the investigator's rewrite, as a statement of design, never as a result (Section 5.3 bars the secondaries from the abstract as results). Decision: the investigator.

**C-N11. Print the prompt template in full (C.14.2 no. 4).** The template is pinned by hash (`03_method.md` l.31) and is said to hold no dataset caption. Printing it is a release decision and needs the template text from the code. Recommendation: print the header, one empty example line and the two tails in the supplement. Decision: the investigator.

**C-N12. A POST HOC `rand` − `zs` row with an interval on the test sets (C.14.2 no. 5).** It needs a new computation on the stored per-image test scores. Outside this package. C-F14 gives the pointer that the report names as the alternative. Recommendation: no new test-set row unless a judge rules it in under the study's post hoc rules.

**C-N13. Weight and style of the attribution part (C.14.2 no. 8; remarks C.6 no. 7, C.7.3 no. 5 and no. 8, C.8 no. 2, C.11 (iii), C.4 no. 4 and no. 8).** Sections 5.7, 6.10 and 7.5 are long, repeat one fixed sentence per row, and carry operational detail, while the study enters neither the abstract nor the contributions. Shortening them, moving detail to the supplement, renaming overloaded symbols (τ, K, κ, R, D) or naming the batch finding in the conclusion all change ruled text or frozen text. Recommendation: one decision by the investigator on the role of this part (in the message, or mostly in the supplement), then a ruled rewrite after the freeze. No pair is offered here.

**C-N14. Release of the per-image score ledgers (C.14.2 no. 10).** The paper says they will not be released (`01_introduction.md` l.34, `09_limitations.md` l.28, `10_conclusion.md` l.25); the progress note lists this as an open decision. Options: release the per-image scores without captions; or keep the present policy and say that a third party must re-run the study to recompute an interval. Recommendation: release per-image scores without captions if the dataset terms allow it. Decision: the investigator.

**C-N15. Related work (C.14.2 no. 11; remark C.3).** Reading the full text of the two works whose rows of Table 1 come "from the abstract", a dated systematic search, and a check of the OpenFlamingo numbers against the final print all need the network and new reading. Outside this package.

**C-N16. The sentence on the agreement of the dataset authors (D.16 no. 5; remark D.11 (a)).** `10_conclusion.md` l.25 says that the authors of UIT-OpenViIC and KTVIC agreed to the use of their datasets; the conference plan notes that no written confirmation is on file. The conclusion is frozen and the fact is the investigator's to confirm. Recommendation: keep the sentence only with a written confirmation on file; otherwise remove it in both versions.

**Remark-block points not taken up as fixes (no decision asked):** "PASS for … and PASS for … (both: passed)" in Section 6.2 (style); a sentence in Section 6.3 that the pooled XM-a number averages two rows of opposite sign (the rows are printed side by side); a table for Section 6.8 in the main text; a note under Table 11 on the uncalibrated English deletion step (stated in Section 8.5); how the Flickr30K carve was drawn and the typical number of references per XM-test2500 image (the second needs a new number); a line in Section 9.1 on the single `fix` set (the † note of Table 6 and Section 6.10.5 state it). They are choices for the investigator's rewrite.

## 5. WAITS FOR FREEZE and DROPPED

**C-W01 (C.14.1 no. 2; remarks C.4 no. 10, C.6 no. 8, C.7.3 no. 6).** The outcome of the registered arms that have not run, and the tense of the freeze sentence: the "Other registered arms" sentence (`03_method.md` l.132), the freeze sentence of the Budget paragraph (`05_…` l.182), Section 6.10.9 (`06_results.md` l.254–260), the Block order item (`07_disclosures.md` l.54), and every statement on block 4 and the memory swap. A ruled text exists and is applied after 2026-11-16 12:00 (UTC+7). No pair here touches these sentences.

**C-W02 (D.16 no. 13).** A check of the conference draft after the freeze; not journal text.

**C-D01.** "No block numbered 2 is mentioned": answered at HEAD. Commit 6a5d36a added Section 6.10.9 (`06_results.md` l.254–260: block 2 not run by its registered cut-off, family S-BB empty, block 3 ran) with pointers in `05_…` l.158 and `07_…` l.54.

**C-D02.** "Each entry is one bootstrap unit" is already in `04_data_and_splits.md` l.24. The distinct-image counts are C-N02.

**C-D03.** The sentence that the pooled estimand averages two backbone-plus-configuration pairs is already in `05_…` l.50 (directly under the definition of the pooled difference) and in `09_limitations.md` l.5. Moving a copy under Table 2 is a placement choice, not a defect.

**C-D04.** The position on p-values is already stated in `05_…` l.114 and `09_limitations.md` l.24.

## 6. Notes for whoever applies the fixes

1. **The after-freeze transfer needs a clean tree.** The prepared script for the freeze (`manuscript/prereg/2026-11-11_c_attr_dev/paper_text/transfer/c_attr_c2_transfer.py`) refuses to write unless `03_method.md`, `05_…`, `06_results.md`, `07_disclosures.md` and the manifest equal HEAD, and unless each of its five anchor strings occurs exactly once. So the fixes of this package must be either committed before that script runs or applied after it; they must not sit uncommitted in the tree at the freeze.
2. **Its anchors are untouched.** No OLD or NEW of this package contains or changes one of the five anchors; the check is in section 7.
3. **The pairs do not overlap.** Applying all pairs in the listed order and in the reverse order gives byte-equal files (section 7), so any subset can be applied.
4. **C-F03 depends on C-F02** for its reference to Section 8.6 (see its evidence block).
5. **`tex/` and the PDFs** are not part of this package and are rebuilt later.

## 7. Checks run

Method: a read-only script parsed the 27 blocks of this file and compared them with the files of the paper repo at `git show 6a5d36a:paper_v1_analysis/<file>` (not the working tree). It wrote nothing. Script: `/tmp/claude-1000/-mnt-d-vsps-image-captioning/cbc155a0-619c-4f6d-b27a-ab9635fb7056/scratchpad/check_c_pkg.py` (a session file; it is not part of the package).

| id | file | OLD occurs exactly once at HEAD 6a5d36a |
|---|---|---|
| C-F01 | `06_results.md` | yes |
| C-F02 | `08_english_comparison.md` | yes |
| C-F03 | `07_disclosures.md` | yes |
| C-F04 | `09_limitations.md` | yes |
| C-F05 | `03_method.md` | yes |
| C-F06 | `08_english_comparison.md` | yes |
| C-F07 | `11_supplement_registered_rows.md` | yes |
| C-F08a | `11_supplement_registered_rows.md` | yes |
| C-F08b | `11_supplement_registered_rows.md` | yes |
| C-F08c | `11_supplement_registered_rows.md` | yes |
| C-F08d | `11_supplement_registered_rows.md` | yes |
| C-F08e | `11_supplement_registered_rows.md` | yes |
| C-F09 | `11_supplement_registered_rows.md` | yes |
| C-F10 | `05_preregistration_and_analysis.md` | yes |
| C-F11 | `06_results.md` | yes |
| C-F12 | `09_limitations.md` | yes |
| C-F13 | `03_method.md` | yes |
| C-F14 | `06_results.md` | yes |
| C-F15a | `09_limitations.md` | yes |
| C-F15b | `09_limitations.md` | yes |
| C-F16 | `06_results.md` | yes |
| C-F17 | `05_preregistration_and_analysis.md` | yes |
| C-F18a | `05_preregistration_and_analysis.md` | yes |
| C-F18b | `11_supplement_registered_rows.md` | yes |
| C-F19 | `06_results.md` | yes |
| C-F20 | `08_english_comparison.md` | yes |
| C-F21 | `06_results.md` | yes |

Further checks, all passed:
- 27 pairs under 21 FIX ids; every OLD differs from its NEW; no pair is in `00_abstract.md`, `01_introduction.md` or `10_conclusion.md`.
- Applying all pairs in the listed order and in the reverse order gives byte-equal files, and each OLD still occurs exactly once at its turn in both orders.
- After all pairs, every NEW occurs exactly once in its file.
- The five anchor strings of the after-freeze transfer script occur exactly once before and after all pairs, and no OLD or NEW contains one of them.
- sha256 (first 16 hex) of each file with all 27 pairs applied to the HEAD blob, for the applier to compare: `03_method.md` 8cf191b9fb27b2da; `05_preregistration_and_analysis.md` 194e0622797c03a2; `06_results.md` af36f664bf7aec5a; `07_disclosures.md` 72adbcb08352881c; `08_english_comparison.md` 72f3cd8b5f916669; `09_limitations.md` 842224c8ec827d62; `11_supplement_registered_rows.md` 0d602595ed238523.
- The registration copies used (`2026-10-22_c_stage1/DESIGN.md`, `2026-10-22_c_stage2/PREREG.md`, `2026-10-30_c_t1/c_t1_registry.json`) are byte-equal in the paper repo and the run repo; the sha256 prefixes of `decide_final.json` (92a1f0e992cb) and of `SUMMARY.json` (1d78cd205ff8) equal those in the manifest.

Not checked, and said so where it matters:
- The manifest check of the paper repo and the LaTeX build were not run, because nothing was applied.
- C-F09: the code files were not compared with the hashes pinned at stage A.
- C-F13: the batch sizes are the registered values; the run files were not opened.
- C-F10: the rulings cited beside the −1.0 and 0.10 values were not read.
- C-N05, C-N07, C-N16: the true status of the companion studies, the definition of the "exploration halves" and the written agreement of the dataset authors cannot be settled from the allowed files.
