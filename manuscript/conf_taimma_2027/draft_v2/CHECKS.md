# CHECKS: TAIMMA draft v1 of Paper C

Written by `check_draft.py` at 2026-11-15T04:17:18Z. Laptop text checks only: no template build, so no page count.

Inputs (sha256):

- `paper.md` d97cd24aa89d1384f9becab414c2e290fd61f8985177e49f99c1f647ef641e08
- `number_manifest_TAIMMA.tsv` 506ab1d6a9a7ff5d042b865314776b2d9e7130454ef4d1cef061fba9ce5cb6c6
- `PARAGRAPH_SOURCES.tsv` c5f2fa689651729027b11a8eae94c21aeacf308e7fdfb087403cee68b1b0bb3e
- `number_manifest_C.tsv` 83414dc3d863bbe62c67b64c4dd0cb9b3f9796fc7247575b08a9bf7f296d1f81
- `paperC.bib` a415c4daa4d8c40b5b14432913d62bfefdcc30d7ff347df05637f332c23010e2

## Summary

| check | result | measured |
|---|---|---|
| Paragraph markers and PARAGRAPH_SOURCES.tsv | PASS | 79 units, 79 rows, 54 of 54 claim-map rows carried |
| Limits known today (abstract 150 to 250 words, 7 tables, 1 figure) | PASS | title 14 words, abstract 212 words, 5 keywords, 7 tables, 1 figure |
| Plan word budgets (every section at or under its planned words) | FAIL | running text 4521 against 4100 planned; sections over their budget: Abs +12, §1 +5, §2 +16, §3 +85, §4 +27, §5 +12, §7 +158, §8 +46, Decl +92 |
| Numbers keyed (token -> manifest row, by section and claim) | PASS | 417 numeric tokens, 0 without a row |
| Estimate and CI read from one key | PASS | 86 triples, 0 without a single key stem |
| Manifest rows equal the source manifest and are all printed | PASS | 295 rows (27 label rows), 0 problems |
| Registered negatives and labels (plan A.5) | PASS | 24 required statements, 0 missing |
| Citation keys exist in the bib | PASS | 34 keys used, 0 not in the bib (67 entries) |
| No host or IP pattern | PASS | 0 hits |
| No writing-tool statement | PASS | 0 hits |
| No promotional word | PASS | 0 hits |
| No journal-only content | PASS | 0 hits outside the allowed sentences, 4 allowed |
| No data-set caption text | PASS | 0 Vietnamese letters, 0 unexpected quoted strings |

## Paragraph markers and PARAGRAPH_SOURCES.tsv: PASS

79 units, 79 rows, 54 of 54 claim-map rows carried



## Limits known today (abstract 150 to 250 words, 7 tables, 1 figure): PASS

title 14 words, abstract 212 words, 5 keywords, 7 tables, 1 figure



## Plan word budgets (every section at or under its planned words): FAIL

running text 4521 against 4100 planned; sections over their budget: Abs +12, §1 +5, §2 +16, §3 +85, §4 +27, §5 +12, §7 +158, §8 +46, Decl +92

| section | running text | budget | difference | table cells | captions and notes |
|---|---|---|---|---|---|
| Abs | 212 | 200 | +12 | 0 | 0 |
| §1 | 505 | 500 | +5 | 0 | 0 |
| §2 | 346 | 330 | +16 | 103 | 66 |
| §3 | 705 | 620 | +85 | 22 | 9 |
| §4 | 587 | 560 | +27 | 424 | 70 |
| §5 | 712 | 700 | +12 | 220 | 85 |
| §6 | 348 | 380 | -32 | 98 | 125 |
| §7 | 698 | 540 | +158 | 0 | 0 |
| §8 | 206 | 160 | +46 | 0 | 0 |
| Decl | 202 | 110 | +92 | 0 | 0 |
| total | 4521 | 4100 | +421 | 867 | 355 |

Title: 14 words. Abstract: 212 words (LNCS convention 150 to 250, to re-fetch). Keywords: 5. Tables: 7. Figures: 1.
Counting rule: whitespace-separated tokens that hold a letter or a digit; a citation group counts as one word; headings, the author line, keywords and comments are not counted; table cells, captions and notes are counted apart from the running text.

## Numbers keyed (token -> manifest row, by section and claim): PASS

417 numeric tokens, 0 without a row

year-like tokens left out of the check: none

One- and two-digit integers with their context (read these once):
- ABS-01: `95` in "...pped CIDEr-D points pooled (95% bootstrap CI; regi..." -> PREREG.md::§6.3 percentile CI
- S3-03: `60` in "...ing is greedy, with at most 60 new tokens, for Qwe..." -> DESIGN.md::§4.2 max new tokens
- T2: `8` in "...L3-8B | |---|---|---| | k | 8 | 4 | | order | firs..." -> frozen_config.json::models.qwen25vl_7b.k
- T2: `4` in "...B | |---|---|---| | k | 8 | 4 | | order | first | ..." -> frozen_config.json::models.internvl3_8b.k
- S4-01: `60` in "...split of 2,001 images minus 60 images that a pre-s..." -> ov_test_dev299_neardup_files.txt::line_count
- T3: `60` in "...gistered sensitivity) minus 60 excluded by the fil..." -> ov_test_dev299_neardup_files.txt::line_count
- S4-04: `95` in "...00 resamples and percentile 95% bounds. For a pool..." -> PREREG.md::§6.3 percentile CI
- T6: `95` in "... results: estimate with its 95% CI, the label as r..." -> PREREG.md::§6.3 percentile CI
- S5-05: `12` in "...he examples shown. It flags 12 of the 1,941 primar..." -> c1_ov_test_posthoc.json::pinned_ids.n
- S5-05: `9` in "...among their `ret` examples (9 of them at the first..." -> pin_c_ov_test.json::arms.ret.qwen25vl_7b.n_first_hit_rank1 ; arms.ret.internvl3_8b.n_first_hit_rank1
- S5-05: `0` in "...hem at the first rank), and 0 queries in `rand`. W..." -> pin_c_ov_test.json::arms.rand.union.n_flagged
- S5-05: `12` in "...ries in `rand`. Without the 12 queries the pooled ..." -> c1_ov_test_posthoc.json::pinned_ids.n
- S6-02: `1` in "...r similarity rule of  flags 1 of the 5,000 queries..." -> c2_coco_posthoc.json::pinned_ids.n
- S7-D01: `60` in "...ary OpenViIC set leaves out 60 images by a pre-spe..." -> ov_test_dev299_neardup_files.txt::line_count
- S7-L06: `52` in "...n the same batches and gave 52/52 identical captio..." -> e4_qwen25vl_7b.json::identical
- S7-L06: `52` in "...he same batches and gave 52/52 identical captions ..." -> e4_qwen25vl_7b.json::identical
- S7-L06: `50` in "..., non-confirmatory) decoded 50 items one at a time..." -> S10b_qwen25vl_7b.json::n
- S7-L06: `42` in "...ded 50 items one at a time: 42/50 captions were id..." -> S10b_qwen25vl_7b.json::identical
- S7-L06: `50` in "... 50 items one at a time: 42/50 captions were ident..." -> S10b_qwen25vl_7b.json::n
- S7-L06: `37` in "...dentical for Qwen2.5-VL and 37/50 for InternVL3. T..." -> S10b_internvl3_8b.json::identical
- S7-L06: `50` in "...tical for Qwen2.5-VL and 37/50 for InternVL3. That..." -> S10b_qwen25vl_7b.json::n
- S7-03: `20` in "...st used 9.59 GPU-hours of a 20-hour cap and the En..." -> PREREG.md::§12 hard cap
- S7-03: `25` in "...the English test 13.22 of a 25-hour cap, each on o..." -> PREREG.md::§10 test cap
- S7-03: `24` in "... a 25-hour cap, each on one 24 GB GPU...." -> DESIGN.md::l.10 one RTX 3090 24 GB

## Estimate and CI read from one key: PASS

86 triples, 0 without a single key stem

| unit | estimate [lo, hi] | key stem |
|---|---|---|
| ABS-01 | +4.49 [3.52, 5.57] | decide_ov.json::P1 |
| ABS-01 | +0.70 [−0.45, 1.97] | decide_xm_m3.json::XM_a |
| ABS-01 | +3.08 [2.08, 4.03] | decide_coco_test.json::P1_EN |
| ABS-01 | +1.73 [0.94, 2.50] | decide_nocaps_val.json::S_NC |
| S1-06 | +4.49 [3.52, 5.57] | decide_ov.json::P1 |
| S1-07 | +0.70 [−0.45, 1.97] | decide_xm_m3.json::XM_a |
| S1-07 | +1.73 [0.94, 2.50] | decide_nocaps_val.json::S_NC |
| S3-05 | +2.91 [0.46, 5.31] | decide_final.json::ov_dev_b.H_G.pooled |
| S4-02 | +6.04 [4.54, 7.58] | decide_final.json::ov_dev_b.gate.pooled_vs_rand |
| T6 | +4.49 [3.52, 5.57] | decide_ov.json::P1 |
| T6 | +4.46 [3.45, 5.38] | decide_ov.json::sensitivity.ov_test_2001 |
| T6 | +8.33 [7.01, 9.76] | decide_ov.json::P1b.qwen25vl_7b |
| T6 | +8.29 [6.99, 9.59] | decide_ov.json::sets.ov_test_2001.detail.per_model.qwen25vl_7b.vs_rand |
| T6 | +0.66 [−0.68, 1.99] | decide_ov.json::P1b.internvl3_8b |
| T6 | +0.63 [−0.73, 1.86] | decide_ov.json::sets.ov_test_2001.detail.per_model.internvl3_8b.vs_rand |
| T6 | +3.71 [2.29, 5.14] | decide_ov.json::secondary_devb_motivated.internvl3_neg_inf.ov_test_1941 |
| T6 | +3.68 [2.20, 5.05] | decide_ov.json::secondary_devb_motivated.internvl3_neg_inf.ov_test_2001 |
| T6 | +5.41 [3.88, 7.01] | decide_ov.json::P2.qwen25vl_7b |
| T6 | +5.34 [3.88, 6.87] | decide_ov.json::sets.ov_test_2001.detail.per_model.qwen25vl_7b.pcm_vs_zs |
| T6 | +1.57 [0.65, 2.51] | decide_ov.json::P2.internvl3_8b |
| T6 | +1.35 [0.44, 2.27] | decide_ov.json::sets.ov_test_2001.detail.per_model.internvl3_8b.pcm_vs_zs |
| T6 | +0.70 [−0.45, 1.97] | decide_xm_m3.json::XM_a |
| T6 | +0.82 [−0.45, 2.11] | decide_xm_m3.json::sensitivity.xm_test2392 |
| T6 | +3.15 [1.50, 4.93] | decide_xm_m3.json::per_model.qwen25vl_7b |
| T6 | −1.75 [−3.35, −0.09] | decide_xm_m3.json::per_model.internvl3_8b |
| T6 | +0.18 [−1.36, 1.81] | decide_xm_m3.json::secondary_devb_motivated.internvl3_neg_inf.xm_test2500 |
| T6 | +0.19 [−1.41, 1.79] | decide_xm_m3.json::secondary_devb_motivated.internvl3_neg_inf.xm_test2392 |
| T6 | +0.59 [−0.31, 1.54] | decide_xmb.json::XM_b |
| T6 | +0.57 [−0.41, 1.56] | decide_xmb.json::XM_b_sensitivity.xm_test2392 |
| S5-02 | +4.49 [3.52, 5.57] | decide_ov.json::P1 |
| S5-02 | +8.33 [7.01, 9.76] | decide_ov.json::P1b.qwen25vl_7b |
| S5-02 | +0.66 [−0.68, 1.99] | decide_ov.json::P1b.internvl3_8b |
| S5-03 | +5.41 [3.88, 7.01] | decide_ov.json::P2.qwen25vl_7b |
| S5-03 | +1.57 [0.65, 2.51] | decide_ov.json::P2.internvl3_8b |
| S5-04 | +3.71 [2.29, 5.14] | decide_ov.json::secondary_devb_motivated.internvl3_neg_inf.ov_test_1941 |
| S5-04 | +3.68 [2.20, 5.05] | decide_ov.json::secondary_devb_motivated.internvl3_neg_inf.ov_test_2001 |
| S5-05 | +4.47 [3.44, 5.41] | c1_ov_test_posthoc.json::estimate.P1 |
| S5-05 | +5.34 [3.87, 6.82] | c1_ov_test_posthoc.json::estimate.P2.qwen25vl_7b |
| S5-05 | +1.61 [0.68, 2.56] | c1_ov_test_posthoc.json::estimate.P2.internvl3_8b |
| S5-06 | +0.70 [−0.45, 1.97] | decide_xm_m3.json::XM_a |
| S5-06 | +0.82 [−0.45, 2.11] | decide_xm_m3.json::sensitivity.xm_test2392 |
| S5-06 | +3.15 [1.50, 4.93] | decide_xm_m3.json::per_model.qwen25vl_7b |
| S5-06 | −1.75 [−3.35, −0.09] | decide_xm_m3.json::per_model.internvl3_8b |
| S5-07 | +0.59 [−0.31, 1.54] | decide_xmb.json::XM_b |
| S5-07 | +0.12 [−1.20, 1.49] | decide_xm_m3.json::sets.xm_test2500.detail.per_model.qwen25vl_7b.pcm_vs_zs |
| S5-07 | +0.13 [−0.83, 1.03] | decide_xm_m3.json::sets.xm_test2500.detail.per_model.internvl3_8b.pcm_vs_zs |
| S5-08 | +14.30 [13.38, 15.24] | decide_ov.json::S_zf.pooled_vs_zs |
| S5-08 | +11.99 [10.68, 13.34] | decide_xm_m3.json::S_zf.pooled_vs_zs |
| S5-09 | +3.47 [2.54, 4.41] | decide_ov.json::S_zf.pooled_vs_fix |
| S5-09 | +2.53 [1.32, 3.80] | decide_xm_m3.json::S_zf.pooled_vs_fix |
| S5-09 | +6.33 [5.02, 7.72] | decide_ov.json::S_zf.per_model.qwen25vl_7b.vs_fix |
| S5-09 | +5.87 [4.14, 7.65] | decide_xm_m3.json::S_zf.per_model.qwen25vl_7b.vs_fix |
| S5-09 | +0.61 [−0.68, 1.87] | decide_ov.json::S_zf.per_model.internvl3_8b.vs_fix |
| S5-09 | −0.81 [−2.41, 0.76] | decide_xm_m3.json::S_zf.per_model.internvl3_8b.vs_fix |
| S5-10 | +13.98 [12.63, 15.38] | decide_ov.json::sets.ov_test_1941.nn.vs_nn_top1.pooled |
| S5-10 | +9.15 [7.84, 10.47] | decide_ov.json::sets.ov_test_1941.nn.vs_nn_cons.pooled |
| S5-10 | +4.91 [3.93, 6.00] | decide_ov.json::sets.ov_test_1941.pooled_ptb_vs_rand |
| S5-10 | +0.60 [−0.54, 1.85] | decide_xm_m3.json::ptb |
| T7 | +3.08 [2.08, 4.03] | decide_coco_test.json::P1_EN |
| T7 | +1.73 [0.94, 2.50] | decide_nocaps_val.json::S_NC |
| T7 | +1.62 [0.66, 2.52] | decide_nocaps_val.json::S_NC_sensitivity_3500 |
| T7 | +7.80 [6.40, 9.17] | decide_coco_test.json::scored.coco_test_5000.per_model.qwen25vl_7b.ret_minus_rand |
| T7 | +2.83 [1.69, 3.98] | decide_nocaps_val.json::scored.nocaps_val_4500.per_model.qwen25vl_7b.ret_minus_rand |
| T7 | −1.64 [−2.79, −0.49] | decide_coco_test.json::scored.coco_test_5000.per_model.internvl3_8b.ret_minus_rand |
| T7 | +0.62 [−0.37, 1.62] | decide_nocaps_val.json::scored.nocaps_val_4500.per_model.internvl3_8b.ret_minus_rand |
| T7 | −1.05 [−2.22, 0.08] | decide_coco_test.json::scored.coco_test_5000.secondary_neg_inf_internvl3 |
| T7 | +1.00 [−0.01, 2.01] | decide_nocaps_val.json::scored.nocaps_val_4500.secondary_neg_inf_internvl3 |
| T7 | +1.09 [−0.12, 2.21] | decide_nocaps_val.json::scored.nocaps_val_3500.secondary_neg_inf_internvl3 |
| T7 | +4.64 [1.85, 7.36] | decide_nocaps_val.json::per_domain.in-domain |
| T7 | +1.96 [0.85, 2.99] | decide_nocaps_val.json::per_domain.near-domain |
| T7 | +0.43 [−0.85, 1.73] | decide_nocaps_val.json::per_domain.out-domain |
| S6-02 | +3.08 [2.08, 4.03] | decide_coco_test.json::P1_EN |
| S6-02 | +7.80 [6.40, 9.17] | decide_coco_test.json::scored.coco_test_5000.per_model.qwen25vl_7b.ret_minus_rand |
| S6-02 | −1.64 [−2.79, −0.49] | decide_coco_test.json::scored.coco_test_5000.per_model.internvl3_8b.ret_minus_rand |
| S6-02 | +3.07 [2.08, 4.06] | c2_coco_posthoc.json::estimate |
| S6-02 | +29.50 [28.27, 30.79] | decide_coco_test.json::scored.coco_test_5000.per_model.qwen25vl_7b.rand_minus_zs |
| S6-02 | +8.13 [7.03, 9.21] | decide_coco_test.json::scored.coco_test_5000.per_model.internvl3_8b.rand_minus_zs |
| S6-03 | +1.73 [0.94, 2.50] | decide_nocaps_val.json::S_NC |
| S6-03 | +1.62 [0.66, 2.52] | decide_nocaps_val.json::S_NC_sensitivity_3500 |
| S6-03 | +4.64 [1.85, 7.36] | decide_nocaps_val.json::per_domain.in-domain |
| S6-03 | +1.96 [0.85, 2.99] | decide_nocaps_val.json::per_domain.near-domain |
| S6-03 | +0.43 [−0.85, 1.73] | decide_nocaps_val.json::per_domain.out-domain |
| S8-01 | +4.49 [3.52, 5.57] | decide_ov.json::P1 |
| S8-01 | +3.08 [2.08, 4.03] | decide_coco_test.json::P1_EN |
| S8-02 | +0.70 [−0.45, 1.97] | decide_xm_m3.json::XM_a |
| S8-02 | +1.73 [0.94, 2.50] | decide_nocaps_val.json::S_NC |

## Manifest rows equal the source manifest and are all printed: PASS

295 rows (27 label rows), 0 problems



## Registered negatives and labels (plan A.5): PASS

24 required statements, 0 missing

- XM-a FAIL (C17), Abs: ABS-01
- XM-a FAIL (C17), §1: S1-07
- XM-a FAIL (C17), §5: S5-06
- XM-a FAIL (C17), §8: S8-02
- S-NC FAIL (C37), Abs: ABS-01
- S-NC FAIL (C37), §1: S1-07
- S-NC FAIL (C37), §6: S6-03
- S-NC FAIL (C37), §8: S8-02
- S-NC sensitivity FAIL (C38), §6: T7, S6-03
- guard H_G not passed (C06), §3: S3-05
- P1 PASS with its scope (C07, C08), Abs: ABS-01
- P1 PASS with its scope (C07, C08), §1: S1-06
- P1 PASS with its scope (C07, C08), §5: T6, S5-02
- P1 PASS with its scope (C07, C08), §8: S8-01
- InternVL3 at tau=-inf, XM (C20), §5: T6
- InternVL3 at tau=-inf, COCO (C35), §6: T7
- InternVL3 at tau=-inf, NoCaps (C40), §6: T7
- XM prediction (C22), §5: T6, S5-07
- XM prediction (C22), §8: S8-02
- S-NC sensitivity in the conclusion (C38, CC-392 N8), §8: S8-02
- InternVL3 below zero on COCO (C34), Abs: ABS-01
- InternVL3 below zero on COCO (C34), §1: S1-06
- InternVL3 below zero on COCO (C34), §6: S6-02
- InternVL3 below zero on COCO (C34), §8: S8-01

## Citation keys exist in the bib: PASS

34 keys used, 0 not in the bib (67 entries)

Keys used: Agrawal2019NoCaps, Awadalla2023OpenFlamingo, Bai2025Qwen25VL, Baldassini2024MICL, Bui2023OpenViIC, Chen2015COCOCaptions, Chen2024InternVL25, Chen2025TrueMICL, Chen2026MUNIChus, Devlin2015NN, Ibrahim2025CONCAP, Joshi2020StateFate, Karpathy2015Split, Kuznetsova2020OpenImages, Li2024RetrievalRobustness, Li2025UnveilingICL, Lin2014COCO, Nguyen2018VnCoreNLP, Nguyen2026FAIR, Pham2024KTVIC, Pizzi2022SSCD, Ramos2023EXTRA, Ramos2023LMCap, Ramos2023SmallCap, Rebelo2025RSCap, Rohrbach2018CHAIR, Thapliyal2022XM3600, Tschannen2025SigLIP2, Vedantam2015CIDEr, Vu2018VnCoreNLP, Vu2025VELVET, Vu2026ViG, Yang2023ICLConfig, Zhu2025InternVL3

## No host or IP pattern: PASS

0 hits



## No writing-tool statement: PASS

0 hits



## No promotional word: PASS

0 hits



## No journal-only content: PASS

0 hits outside the allowed sentences, 4 allowed

Allowed (scope sentence A9; one published result in related work): S2-03: Flickr, S7-D12: Flickr, S7-D12: ablation, S7-D12: attribution

## No data-set caption text: PASS

0 Vietnamese letters, 0 unexpected quoted strings

Statement: no data-set caption text is quoted in paper.md. The writer opened no caption, reference, prediction or ledger file. The script finds 0 Vietnamese-specific letters or tone marks in the paper and 14 distinct quoted strings, all of them registered labels, registered wordings or defined terms:

- "Filter"
- "Order"
- "Registered"
- "Reported"
- "carried mainly by Qwen2.5-VL; not detected for InternVL3"
- "confirmed"
- "detected"
- "lower bound"
- "not confirmed"
- "not reported by the dataset authors"
- "not separated from length"
- "reported"
- "the gain was not detected out of domain (XM3600)"
- "yes"

Name tokens that hold digits and are not counted as numbers: D9, Flickr30K, InternVL3, InternVL3-8B, NN-top1, P1, P1-EN, P1b, P2, Qwen2.5-VL, Qwen2.5-VL-7B, Qwen2.5-VL-7B-Instruct, Qwen3-VL-8B-Instruct, SigLIP2, T1, T2, XM-dev500, XM-test2500, XM3600, dev299, full-XM3600

## Every sentence or table row that states a registered negative

- Abs / ABS-01: On OpenViIC test, retrieved examples beat random ones by +4.49 [3.52, 5.57] stripped CIDEr-D points pooled (95% bootstrap CI; registered PASS), with the registered scope "carried mainly by Qwen2.5-VL; not detected for InternVL3".
- Abs / ABS-01: On XM3600 Vietnamese, outside the memory's source, the gain was not detected: +0.70 [−0.45, 1.97], a registered FAIL under a rule that required a CI above zero.
- Abs / ABS-01: On NoCaps the point, +1.73 [0.94, 2.50], lay below the registered +2.0 (FAIL).
- §1 / S1-06: Under the registered scope sentence the Vietnamese gain is "carried mainly by Qwen2.5-VL; not detected for InternVL3".
- §1 / S1-07: On XM3600 Vietnamese the gain was not detected: +0.70 [−0.45, 1.97], a FAIL under a rule that required a CI above zero.
- §1 / S1-07: On NoCaps val the interval clears zero, but the point, +1.73 [0.94, 2.50], falls short of the registered +2.0 (FAIL).
- §3 / S3-05: The step stayed, with τ as fixed at stage A, although at stage B the guard hypothesis H_G was not passed: it needed a precision change with a CI above zero and a stripped CIDEr-D cost within a registered bound, and the cost, −4.01, lay outside that bound (pooled precision change +2.91 [0.46, 5.31] points).
- §4 / S4-03: The wording for a failed XM-a was also registered: "the gain was not detected out of domain (XM3600)".
- §4 / T4: | XM prediction | XM-a and XM-b | XM-test2500 | "confirmed" only if both pass; otherwise "not confirmed" |
- §5 / T6: Table 6. Registered Vietnamese results: estimate with its 95% CI, the label as registered, and the registered sensitivity. Scope of every pooled P1 number, as registered: "carried mainly by Qwen2.5-VL; not detected for InternVL3". Rows marked "reported" have no registered rule and unadjusted CIs.
- §5 / T6: | XM-a, pooled ret − rand | +0.70 [−0.45, 1.97] | FAIL | +0.82 [−0.45, 2.11] |
- §5 / T6: | secondary, InternVL3 at τ = −∞ | +0.18 [−1.36, 1.81] | not detected | +0.19 [−1.41, 1.79], not detected |
- §5 / T6: | XM prediction (XM-a and XM-b) | – | not confirmed | – |
- §5 / S5-02: On the primary set, retrieved examples scored +4.49 [3.52, 5.57] points above random examples, pooled over the two backbones (Table 6), with the registered scope: "carried mainly by Qwen2.5-VL; not detected for InternVL3".
- §5 / S5-06: XM-a: FAIL.
- §5 / S5-06: The gain was not detected out of domain (XM3600).
- §5 / S5-07: The registered XM prediction needs both XM-a and XM-b, so it is not confirmed.
- §6 / T7: | label | P1-EN: PASS | S-NC: FAIL | FAIL |
- §6 / T7: | secondary, InternVL3 at τ = −∞ | −1.05 [−2.22, 0.08], not detected | +1.00 [−0.01, 2.01], not detected | +1.09 [−0.12, 2.21], not detected |
- §6 / S6-03: S-NC: FAIL.
- §6 / S6-03: The CI lies above zero, but the point is below the registered +2.0, so the rule fails.
- §6 / S6-03: The claim that the gain transfers to NoCaps is not made.
- §6 / S6-03: The registered sensitivity on 3,500 images, +1.62 [0.66, 2.52], is also a FAIL.
- §7 / S7-L02: - Out of the memory's source both registered predictions failed.
- §8 / S8-01: In a preregistered one-look test, retrieved example captions beat an equal number of random ones from the same memory where memory and test set share a source: by +4.49 [3.52, 5.57] stripped CIDEr-D points on OpenViIC test (P1 PASS; "carried mainly by Qwen2.5-VL; not detected for InternVL3") and by +3.08 [2.08, 4.03] PTB CIDEr-D points on the COCO Karpathy test (P1-EN PASS; InternVL3's reported row is below zero).
- §8 / S8-02: Outside the memory's source the registered predictions failed.
- §8 / S8-02: On XM3600 Vietnamese the gain was not detected: +0.70 [−0.45, 1.97], a FAIL under a rule that required a CI above zero, and the XM prediction is not confirmed.
- §8 / S8-02: On NoCaps val the point, +1.73 [0.94, 2.50], is below the registered +2.0 (FAIL; the registered sensitivity also fails).
