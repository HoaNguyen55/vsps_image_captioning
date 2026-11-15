# Revision notes: TAIMMA draft v2.1 to v3 (cut proposal)

Written 2026-11-15T09:08Z (date -u). This is a proposal: no ruling covers the cuts that go beyond CC-414 Ruling 2 (c1 to c4), and nothing was committed.

`draft_v2_1/` is byte-unchanged (`paper.md` f65f53ab991cb7d2f94908ae9681b7d19fa8d53fa30571216ad209d07e267c35 before and after). `draft_v3_cut/paper.md` was made from it by 34 exact OLD/NEW pairs; each OLD was checked to occur exactly once before its write. No number was changed, and no number was added that v2.1 did not print.

## 1. How to put one unit back

Each pair below is independent of the others except where its "basis" line says "follows" or "as". To restore a unit, replace its NEW text by its OLD text in `paper.md`. Three more steps are needed after some restores:

- A restored table or figure changes the printed table numbers. The markers keep their v2.1 names: `T4`, `T5`, `T6`, `T7` now print "Table 1" to "Table 4". After a restore, renumber the labels and the cross-references (pairs marked "renumbering").
- A restored unit that had its own marker (`S2-01`, `T1`, `S3-02b`, `T2`, `T3`, `S5-10`, `F1`) needs its row back in `PARAGRAPH_SOURCES.tsv` (copy the row from `draft_v2_1/PARAGRAPH_SOURCES.tsv`).
- Then run the checker in its three modes (section 4).

## 2. The pairs

"Saving" is in pages, from `PAGE_BUDGET.md` (an estimate, not a build).

### H0 | unit header comment

- Basis: record only (not printed)
- Saving: 0

OLD:

~~~text
'<!--\nDRAFT v2: conference version of Paper C (scope S1 of WRITING_PLAN_C_TAIMMA_v1.md), for TAIMMA 2027, Springer LNCS format.\nRevised from draft v1 after ruling CC-399 (round 1): text items B1 to B6 applied and the redundancy of ruling 6 cut; every change is listed in REVISION_NOTES.md.\nLENGTH WARNING (plan item A16): the venue limit for a full paper is 12 to 15 pages. This is the page-budgeted draft (plan D10).\nThe measured words per section are in CHECKS.md and REVISION_NOTES.md (DRAFT_NOTES.md is the record of draft v1). Pages are NOT measured: no LNCS build was run in this step.\nThe full explained text is Paper C itself; PARAGRAPH_SOURCES.tsv points each paragraph (marker "p:ID") to the lines it was condensed from.\nEvery number is keyed in number_manifest_TAIMMA.tsv. No data-set caption appears anywhere in this draft.\nSections 5 and 7: to re-check after 16 Nov 05:00Z (CC-392 N12). Two units wait for that re-check and were not edited in v2 beyond the one sentence ruled for B5: C26 (the Table 5 dagger note and S5-09) and C44 (S7-L06) (CC-399 G2).\n-->'
~~~

NEW:

~~~text
<!--
DRAFT v3 (CUT PROPOSAL, not ruled): conference version of Paper C (scope S1 of WRITING_PLAN_C_TAIMMA_v1.md), for TAIMMA 2027, Springer LNCS format.
Made from draft v2.1 (paper.md sha256 f65f53ab...) after the LNCS build of 15 Nov 2026 gave 19 pages against a limit of 15.
Every removed or changed unit is listed with its OLD text in REVISION_NOTES_V3.md, so that each can be put back singly. No number was changed.
LENGTH WARNING (plan item A16): the venue limit for a full paper is 12 to 15 pages. The page estimate of this draft is in PAGE_BUDGET.md; it is an estimate from the measured pages of v2.1, not a build.
Table labels were renumbered after three tables were removed: markers T4, T5, T6, T7 now carry the printed labels Table 1 to Table 4.
Every number is keyed in number_manifest_TAIMMA.tsv. No data-set caption appears anywhere in this draft.
Sections 5 and 7: to re-check after 16 Nov 05:00Z (CC-392 N12). Two units wait for that re-check and are byte-unchanged from v2.1: C26 (the dagger note of the per-arm table and S5-09) and C44 (S7-L06) (CC-399 G2).
-->
~~~

### E01 | unit S1-01

- Basis: new cut (tightening; one reference leaves with its clause)
- Saving: 0.10 (the reference entry; the text change is under one line)

OLD:

~~~text
'Vietnamese captioning is low-resource in a concrete sense [@Joshi2020StateFate]. The public general-domain caption sets are few and far smaller than English sets such as COCO, and each has its own domain and reference style [@Pham2024KTVIC; @Bui2023OpenViIC].'
~~~

NEW:

~~~text
Vietnamese captioning is low-resource: the public general-domain caption sets are few and far smaller than English sets such as COCO, and each has its own domain and reference style [@Pham2024KTVIC; @Bui2023OpenViIC].
~~~

### E02 | unit S1-02

- Basis: follows E07 (the related-work table is removed)
- Saving: 0

OLD:

~~~text
'(Sect. 2, Table 1)'
~~~

NEW:

~~~text
(Sect. 2)
~~~

### E03 | unit S1-03

- Basis: CC-414 Ruling 2 (c3)
- Saving: 0.02

OLD:

~~~text
' A separately registered English arm repeated the test with the frozen configurations and no English tuning.'
~~~

NEW:

~~~text
'\n' (the sentence is deleted; this is what is left of the line end)
~~~

### E04 | unit S2-01

- Basis: new cut (whole unit; one reference leaves with it)
- Saving: 0.19 (0.09 text, 0.10 reference entry)

OLD:

~~~text
'<!-- p:S2-01 -->Work on retrieval for captioning is of two kinds. Method papers propose a captioner or a prompting pipeline that reads retrieved captions [@Ramos2023SmallCap; @Ramos2023EXTRA; @Ramos2023LMCap; @Ibrahim2025CONCAP]. Analysis papers take existing models and ask when and why in-context examples help (Table 1). This study is an analysis and proposes no captioner.'
~~~

NEW:

~~~text
(deleted)
~~~

### E05 | unit S2-02

- Basis: last sentence: CC-414 Ruling 2 (c1); the sentence before it: new cut (one reference leaves with it)
- Saving: 0.15 (0.07 text, 0.08 reference entry)

OLD:

~~~text
' Multimodal in-context learning is reported to be driven mainly by the text of the examples [@Baldassini2024MICL; @Chen2025TrueMICL]. This is the reason for the `rand` control: if the text of the examples alone produces a gain, `rand` shows it as much as `ret` does.'
~~~

NEW:

~~~text
'\n' (the sentence is deleted; this is what is left of the line end)
~~~

### E06 | unit S2-05

- Basis: CC-414 Ruling 2 (c4): the related-work table replaced by two sentences that keep, for every row, the language, the random control and the two cells that read no; the column of the examples shown is dropped (S2-02 and S2-04 describe them for four of the five papers)
- Saving: costs 0.07

OLD:

~~~text
'<!-- p:S2-05 -->**What differs here.** An analysis of training-free Vietnamese captioning'
~~~

NEW:

~~~text
<!-- p:S2-05 -->**What differs here.** Five earlier analyses have a random control at equal shots or equal k, four on English caption data [@Yang2023ICLConfig; @Li2024RetrievalRobustness; @Baldassini2024MICL; @Li2025UnveilingICL] and one multilingual without Vietnamese [@Chen2026MUNIChus]. A search of each paper's full text found no statement of a registered one-look test and no CI on the captioning score. This study is an analysis of training-free Vietnamese captioning
~~~

### E06b | unit S2-04

- Basis: new cut, LAST in the order and FIRST to restore: the sentence on other Vietnamese work (three references leave with it, one of them the group's own conference paper)
- Saving: 0.33 (0.02 text, 0.31 for three reference entries)

OLD:

~~~text
' Other Vietnamese work trains or adapts captioners [@Vu2025VELVET; @Vu2026ViG; @Nguyen2026FAIR]; this study trains nothing.'
~~~

NEW:

~~~text
'\n' (the sentence is deleted; this is what is left of the line end)
~~~

### E07 | unit T1

- Basis: CC-414 Ruling 2 (c4): the related-work table (Table 1 of v2.1) removed (see E06)
- Saving: 0.82

OLD:

~~~text
'<!-- p:T1 -->**Table 1.** This study among analyses of in-context captioning. Entries follow each paper\'s own statements; a language cell gives the language of the caption data where a paper does not name it, and a cell that reads *no* means that a search of the paper\'s full text found no such statement. "Registered" means that contrasts and decision rules were fixed before the evaluation data were decoded.\n\n| analysis | language(s) | examples shown | equal-k random control | registered one-look test; CIs on the captioning score |\n|---|---|---|---|---|\n| Yang et al. [@Yang2023ICLConfig] | English | image-caption pairs | yes, equal shots | no; no |\n| Li et al. [@Li2024RetrievalRobustness] | English | captions, to a trained captioner | yes, equal k | no; no |\n| Baldassini et al. [@Baldassini2024MICL] | English | image-caption pairs | yes, equal shots (IDEFICS) | no; no |\n| Li et al. [@Li2025UnveilingICL] | English | image-caption pairs | yes, equal shots | no; no |\n| Chen et al. [@Chen2026MUNIChus] | multilingual, no Vietnamese | image, article excerpt and caption | yes, equal k | no; no |\n| **this study** | **Vietnamese, English** | **captions, as text** | **yes, equal k, same memory** | **yes, four test sets; paired bootstrap CIs** |'
~~~

NEW:

~~~text
(deleted)
~~~

### E08 | unit S3-02b

- Basis: new cut: the copy baselines leave the paper (with E22; named in S7-D12; one reference leaves)
- Saving: 0.10 (0.04 text, 0.06 reference entry)

OLD:

~~~text
"<!-- p:S3-02b -->Two copy baselines use no model: the nearest cluster's caption (NN-top1) and the consensus caption among the k nearest (NN-consensus) [@Devlin2015NN]."
~~~

NEW:

~~~text
(deleted)
~~~

### E09 | unit S3-05

- Basis: new cut: the configuration table (Table 2 of v2.1) folded into one sentence (every cell kept)
- Saving: costs 0.07

OLD:

~~~text
'by a rule written before any output (Table 2): the highest stripped CIDEr-D among its `ret` runs on the KTVIC carve that met three pre-set conditions, one of them a floor on the object-precision change against zero-shot.'
~~~

NEW:

~~~text
by a rule written before any output: the highest stripped CIDEr-D among its `ret` runs on the KTVIC carve that met three pre-set conditions, one of them a floor on the object-precision change against zero-shot. The frozen configurations are: Qwen2.5-VL-7B, k = 8, order first, tail T1, τ = −∞ (no deletion), no verifier at test; InternVL3-8B, k = 4, order last, tail T2, τ = 0.10, verifier at test Qwen3-VL-8B-Instruct.
~~~

### E10 | unit T2

- Basis: new cut: the configuration table removed (see E09)
- Saving: 0.19

OLD:

~~~text
'<!-- p:T2 -->**Table 2.** Frozen configurations, unchanged from the development stages.\n\n| | Qwen2.5-VL-7B | InternVL3-8B |\n|---|---|---|\n| k | 8 | 4 |\n| order | first | last |\n| prompt tail | T1 | T2 |\n| deletion threshold τ | −∞ (no deletion) | 0.10 |\n| verifier at test | none | Qwen3-VL-8B-Instruct |'
~~~

NEW:

~~~text
(deleted)
~~~

### E11 | unit S4-01

- Basis: new cut: the sets table (Table 3 of v2.1) folded into the text (with E12, E13, E24); here: the size of the primary set and the role of XM-dev500
- Saving: costs 0.02 with E11b

OLD:

~~~text
'nothing was annotated for it, and gold never comes from a model output (Table 3). The primary OpenViIC test set (OV-test primary) is the full test split'
~~~

NEW:

~~~text
nothing was annotated for it, and gold never comes from a model output. The primary OpenViIC test set (OV-test primary, 1,941 images) is the full test split
~~~

### E11b | unit S4-01

- Basis: as E11
- Saving: see E11

OLD:

~~~text
'The first 500 form XM-dev500 and the other 2,500 form XM-test2500,'
~~~

NEW:

~~~text
The first 500 form XM-dev500, a secondary set of stage B, and the other 2,500 form XM-test2500,
~~~

### E12 | unit T3

- Basis: new cut: the sets table removed; its facts are in S3-01, S4-01, S4-02, S6-01 and the caption of the rules table (list in REVISION_NOTES_V3.md)
- Saving: 0.90

OLD:

~~~text
'<!-- p:T3 -->**Table 3.** Every set, with its size and how it was formed. "Filter" is the pre-specified filter of Sect. 3.\n\n| set | role | images | how it was formed |\n|---|---|---|---|\n| Vietnamese memory | retrieval pool | 10,501 (8,190 clusters) | KTVIC train outside the development carve (3,469) plus OpenViIC train (9,088), 12,557 candidates, less 2,056 excluded by the filter |\n| KTVIC dev299 | stage A: configuration choice | – | a development carve of the KTVIC training file |\n| OV-dev-A | stage A: advance check | 911 | one half of OpenViIC dev by a hash order, filtered |\n| OV-dev-B | stage B: one-look gate | 925 | the other half, same filter |\n| XM-dev500 | stage B: secondary | 500 | the first images of the hash-ordered XM3600 remainder |\n| **OV-test primary** | **test: P1, P1b, P2** | **1,941** | OpenViIC test (2,001 images, the registered sensitivity) minus 60 excluded by the filter |\n| **XM-test2500** | **test: XM-a, XM-b** | **2,500** | XM3600 (3,600) minus 600 set aside and minus XM-dev500; registered sensitivity: 2,392 images, without the 108 three-reference images |\n| English memory | retrieval pool | 112,255 (111,927 clusters) | COCO Karpathy train and restval after the same filter rules |\n| **COCO Karpathy test** | **test: P1-EN** | **5,000** | the full split |\n| **NoCaps val** | **test: S-NC** | **4,500** | the full split; 417 in-domain, 2,670 near-domain and 1,413 out-domain images by the set\'s own label; registered sensitivity: 3,500 images, without those decoded earlier by another study of the group |'
~~~

NEW:

~~~text
(deleted)
~~~

### E13 | unit S4-02

- Basis: as E11: the two development halves with their sizes; the configuration table is now Sect. 3
- Saving: costs 0.02

OLD:

~~~text
'chose the configurations of Table 2 on a KTVIC development carve and checked them on one half of the OpenViIC development set (OV-dev-A). Stage B gave one look at the other half (OV-dev-B) under a gate:'
~~~

NEW:

~~~text
chose the configurations of Sect. 3 on a KTVIC development carve and checked them on one half of the OpenViIC development set (OV-dev-A, 911 images; the halves follow a hash order and passed the same filter). Stage B gave one look at the other half (OV-dev-B, 925 images) under a gate:
~~~

### E14 | unit S4-03

- Basis: renumbering
- Saving: 0

OLD:

~~~text
'Table 4 lists each registered prediction with its rule.'
~~~

NEW:

~~~text
Table 1 lists each registered prediction with its rule.
~~~

### E15 | unit T4

- Basis: new cut: the columns estimand, set and rule joined into one (every word of every cell kept, two words of two row names moved into their cells); the count of three-reference images and the words on the earlier decode moved here from the sets table
- Saving: 0.19

OLD:

~~~text
'<!-- p:T4 -->**Table 4.** Registered predictions and decision rules. Δ is `ret` − `rand`; "lower bound" is that of the CI of Sect. 4. Registered sensitivities are reported beside a prediction and never replace it: all 2,001 OpenViIC test images; XM-test2500 without the three-reference images (2,392); NoCaps val without the images decoded earlier (3,500).\n\n| name | estimand | set | rule |\n|---|---|---|---|\n| **P1** (primary) | mean pooled Δ_i, stripped CIDEr-D | OV-test primary | PASS if the point is above +2.0 and the lower bound is above zero |\n| rule L | per backbone, relative gap in mean caption length between `ret` and `rand` | OV-test primary; COCO Karpathy test | if above 0.10 for either backbone, a PASS is recorded as "not separated from length" |\n| P1b (non-gating) | per-backbone mean Δ_m,i | OV-test primary | Qwen2.5-VL: "confirmed" if the point is above +2.0; InternVL3: reported only. P1b selects the scope sentence |\n| **P2** | per backbone, ΔP_cm of `ret` against `zs` | OV-test primary | PASS if, for each backbone, the lower bound is above −1.0 |\n| **XM-a** | mean pooled Δ_i, stripped CIDEr-D | XM-test2500 | PASS if the lower bound is above zero; a positive point with a CI that includes zero is printed as a descriptive number only |\n| **XM-b** | change in verified object precision of `ret` against `zs`, pooled | XM-test2500 | PASS if the lower bound is above −1.0 |\n| XM prediction | XM-a and XM-b | XM-test2500 | "confirmed" only if both pass; otherwise "not confirmed" |\n| **P1-EN** (primary, English) | mean pooled Δ_i, PTB CIDEr-D | COCO Karpathy test | the P1 rule, with rule L |\n| **S-NC** (secondary, fixed order) | mean pooled Δ_i, PTB CIDEr-D | NoCaps val | the P1 rule; the transfer claim needs P1-EN and S-NC |\n| secondary, InternVL3 at τ = −∞ | per-backbone mean Δ without the deletion step | every test set | labelled "detected" when the lower bound is above zero; read by no gate |'
~~~

NEW:

~~~text
<!-- p:T4 -->**Table 1.** Registered predictions and decision rules. Δ is `ret` − `rand`; "lower bound" is that of the CI of Sect. 4. Registered sensitivities are reported beside a prediction and never replace it: all 2,001 OpenViIC test images; XM-test2500 without the 108 three-reference images (2,392); NoCaps val without the images decoded earlier by another study of the group (3,500).

| name | estimand and set: rule |
|---|---|
| **P1** (primary) | mean pooled Δ_i, stripped CIDEr-D, on OV-test primary: PASS if the point is above +2.0 and the lower bound is above zero |
| rule L | per backbone, relative gap in mean caption length between `ret` and `rand`, on OV-test primary and on the COCO Karpathy test: if above 0.10 for either backbone, a PASS is recorded as "not separated from length" |
| P1b (non-gating) | per-backbone mean Δ_m,i, on OV-test primary: Qwen2.5-VL: "confirmed" if the point is above +2.0; InternVL3: reported only. P1b selects the scope sentence |
| **P2** | per backbone, ΔP_cm of `ret` against `zs`, on OV-test primary: PASS if, for each backbone, the lower bound is above −1.0 |
| **XM-a** | mean pooled Δ_i, stripped CIDEr-D, on XM-test2500: PASS if the lower bound is above zero; a positive point with a CI that includes zero is printed as a descriptive number only |
| **XM-b** | change in verified object precision of `ret` against `zs`, pooled, on XM-test2500: PASS if the lower bound is above −1.0 |
| XM prediction | XM-a and XM-b, on XM-test2500: "confirmed" only if both pass; otherwise "not confirmed" |
| **P1-EN** (primary) | English: mean pooled Δ_i, PTB CIDEr-D, on the COCO Karpathy test: the P1 rule, with rule L |
| **S-NC** (secondary) | English, fixed order: mean pooled Δ_i, PTB CIDEr-D, on NoCaps val: the P1 rule; the transfer claim needs P1-EN and S-NC |
| secondary, InternVL3 at τ = −∞ | per-backbone mean Δ without the deletion step, on every test set: labelled "detected" when the lower bound is above zero; read by no gate |
~~~

### E16 | unit T5

- Basis: CC-414 Ruling 2 (c4): the English rows of the per-arm table and the caption sentences on them (the dagger note below the table is byte-unchanged)
- Saving: 0.16

OLD:

~~~text
'<!-- p:T5 -->**Table 5.** CIDEr-D per arm, each backbone at its frozen τ. Vietnamese rows: stripped CIDEr-D; English rows: PTB CIDEr-D. The two scales are not comparable. The English arm had no `fix` arm.\n\n| set | backbone (τ) | `ret` | `rand` | `fix` † | `zs` |\n|---|---|---|---|---|---|\n| OV-test primary | Qwen2.5-VL (−∞) | 39.81 | 31.48 | 33.48 | 20.05 |\n| OV-test primary | InternVL3 (0.10) | 33.62 | 32.96 | 33.01 | 24.77 |\n| XM-test2500 | Qwen2.5-VL (−∞) | 57.70 | 54.56 | 51.83 | 43.74 |\n| XM-test2500 | InternVL3 (0.10) | 52.85 | 54.59 | 53.65 | 42.84 |\n| COCO Karpathy test | Qwen2.5-VL (−∞) | 96.36 | 88.57 | – | 59.06 |\n| COCO Karpathy test | InternVL3 (0.10) | 85.34 | 86.98 | – | 78.85 |\n| NoCaps val | Qwen2.5-VL (−∞) | 91.13 | 88.30 | – | 58.46 |\n| NoCaps val | InternVL3 (0.10) | 83.73 | 83.10 | – | 78.30 |'
~~~

NEW:

~~~text
<!-- p:T5 -->**Table 2.** Stripped CIDEr-D per arm on the two Vietnamese test sets, each backbone at its frozen τ.

| set | backbone (τ) | `ret` | `rand` | `fix` † | `zs` |
|---|---|---|---|---|---|
| OV-test primary | Qwen2.5-VL (−∞) | 39.81 | 31.48 | 33.48 | 20.05 |
| OV-test primary | InternVL3 (0.10) | 33.62 | 32.96 | 33.01 | 24.77 |
| XM-test2500 | Qwen2.5-VL (−∞) | 57.70 | 54.56 | 51.83 | 43.74 |
| XM-test2500 | InternVL3 (0.10) | 52.85 | 54.59 | 53.65 | 42.84 |
~~~

### E17 | unit T6

- Basis: renumbering (caption label only; every cell byte-unchanged)
- Saving: 0

OLD:

~~~text
'<!-- p:T6 -->**Table 6.**'
~~~

NEW:

~~~text
<!-- p:T6 -->**Table 3.**
~~~

### E18 | unit S5-02

- Basis: renumbering
- Saving: 0

OLD:

~~~text
'pooled over the two backbones (Table 6)'
~~~

NEW:

~~~text
pooled over the two backbones (Table 3)
~~~

### E19 | unit S5-04

- Basis: renumbering
- Saving: 0

OLD:

~~~text
'and not detected on XM-test2500 (Table 6)'
~~~

NEW:

~~~text
and not detected on XM-test2500 (Table 3)
~~~

### E20 | unit S5-08

- Basis: renumbering
- Saving: 0

OLD:

~~~text
'post hoc reading of Table 5,'
~~~

NEW:

~~~text
post hoc reading of Table 2,
~~~

### E22 | unit S5-10

- Basis: CC-414 Ruling 2 (c4) removes C28 (the PTB sentence) and cuts C27 to one clause; new cut beyond the ruling: the remaining clause of C27 also leaves (with E08; named in S7-D12)
- Saving: 0.19

OLD:

~~~text
"<!-- p:S5-10 -->**Copy baselines and tokenisation (registered secondaries, non-gating).** On OV-test, pooled `ret` exceeds NN-top1 by +13.98 [12.63, 15.38] and NN-consensus by +9.15 [7.84, 10.47]; the near-verbatim share of `ret` captions is 0.015 for Qwen2.5-VL and 0.002 for InternVL3, so the models are not simply returning a neighbour's whole caption. In the PTB-tokenised column, pooled `ret` − `rand` is +4.91 [3.93, 6.00] on OV-test and +0.60 [−0.54, 1.85] on XM-test2500, the same sign and scope as the decision column."
~~~

NEW:

~~~text
(deleted)
~~~

### E23 | unit S6-01

- Basis: follows E10
- Saving: 0

OLD:

~~~text
'the frozen configurations of Table 2 and the deletion step'
~~~

NEW:

~~~text
the frozen configurations of Sect. 3 and the deletion step
~~~

### E24 | unit S6-01

- Basis: as E11: the English memory and the two English test sets, from the sets table
- Saving: costs 0.05

OLD:

~~~text
"The memory is COCO training data [@Lin2014COCO; @Karpathy2015Split], so the COCO Karpathy test lies in the memory's source and NoCaps val [@Agrawal2019NoCaps] outside it."
~~~

NEW:

~~~text
The memory is COCO training data [@Lin2014COCO; @Karpathy2015Split], the Karpathy train and restval images after the same filter rules: 112,255 images in 111,927 clusters. The COCO Karpathy test (the full split, 5,000 images) therefore lies in the memory's source and NoCaps val (the full split, 4,500 images) [@Agrawal2019NoCaps] outside it.
~~~

### E25 | unit T7

- Basis: new cut: the three NoCaps rows by domain label (C41) and their caption sentence; every other row unchanged; label renumbered
- Saving: 0.13

OLD:

~~~text
'<!-- p:T7 -->**Table 7.** Registered and reported English results: pooled and per-backbone `ret` − `rand` in PTB CIDEr-D points with CIs as in Sect. 4. "Reported" rows have no registered rule. The last three rows split NoCaps val by the set\'s own domain label (reported, non-gating).\n\n| row | COCO Karpathy test (5,000) | NoCaps val (4,500) | NoCaps val, registered sensitivity (3,500) |\n|---|---|---|---|\n| **pooled `ret` − `rand`** | **+3.08 [2.08, 4.03]** | **+1.73 [0.94, 2.50]** | +1.62 [0.66, 2.52] |\n| label | **P1-EN: PASS** | **S-NC: FAIL** | FAIL |\n| reported, Qwen2.5-VL | +7.80 [6.40, 9.17] | +2.83 [1.69, 3.98] | – |\n| reported, InternVL3 (τ = 0.10) | −1.64 [−2.79, −0.49] | +0.62 [−0.37, 1.62] | – |\n| secondary, InternVL3 at τ = −∞ | −1.05 [−2.22, 0.08], not detected | +1.00 [−0.01, 2.01], not detected | +1.09 [−0.12, 2.21], not detected |\n| rule L, length gap, Qwen2.5-VL / InternVL3 | 0.019 / 0.019, does not fire | – | – |\n| NoCaps in-domain (417 images) | – | +4.64 [1.85, 7.36] | – |\n| NoCaps near-domain (2,670 images) | – | +1.96 [0.85, 2.99] | – |\n| NoCaps out-domain (1,413 images) | – | +0.43 [−0.85, 1.73] | – |'
~~~

NEW:

~~~text
<!-- p:T7 -->**Table 4.** Registered and reported English results: pooled and per-backbone `ret` − `rand` in PTB CIDEr-D points with CIs as in Sect. 4. "Reported" rows have no registered rule.

| row | COCO Karpathy test (5,000) | NoCaps val (4,500) | NoCaps val, registered sensitivity (3,500) |
|---|---|---|---|
| **pooled `ret` − `rand`** | **+3.08 [2.08, 4.03]** | **+1.73 [0.94, 2.50]** | +1.62 [0.66, 2.52] |
| label | **P1-EN: PASS** | **S-NC: FAIL** | FAIL |
| reported, Qwen2.5-VL | +7.80 [6.40, 9.17] | +2.83 [1.69, 3.98] | – |
| reported, InternVL3 (τ = 0.10) | −1.64 [−2.79, −0.49] | +0.62 [−0.37, 1.62] | – |
| secondary, InternVL3 at τ = −∞ | −1.05 [−2.22, 0.08], not detected | +1.00 [−0.01, 2.01], not detected | +1.09 [−0.12, 2.21], not detected |
| rule L, length gap, Qwen2.5-VL / InternVL3 | 0.019 / 0.019, does not fire | – | – |
~~~

### E26 | unit S6-02

- Basis: renumbering
- Saving: 0

OLD:

~~~text
'PTB CIDEr-D points (Table 7), and rule L does not fire.'
~~~

NEW:

~~~text
PTB CIDEr-D points (Table 4), and rule L does not fire.
~~~

### E27 | unit S6-02

- Basis: CC-414 Ruling 2 (c4): C42
- Saving: 0.05

OLD:

~~~text
' Random examples already score far above zero-shot on COCO: `rand` − `zs` is +29.50 [28.27, 30.79] for Qwen2.5-VL and +8.13 [7.03, 9.21] for InternVL3 (descriptive rows).'
~~~

NEW:

~~~text
'\n' (the sentence is deleted; this is what is left of the line end)
~~~

### E28 | unit S6-03

- Basis: CC-414 Ruling 2 (c2) cuts the numbers of the first sentence; new cut beyond the ruling: both sentences leave with the domain rows (C41; named in S7-D12)
- Saving: 0.07

OLD:

~~~text
" By the set's own domain label the pooled point falls from +4.64 [1.85, 7.36] for in-domain images, through +1.96 [0.85, 2.99], to +0.43 [−0.85, 1.73] for out-domain images. The intervals overlap, and no trend test was registered."
~~~

NEW:

~~~text
' ' (the sentence is deleted; this is what is left of the line end)
~~~

### E28b | unit S6-03

- Basis: follows E28 (joins the two remaining sentences); renumbering
- Saving: 0

OLD:

~~~text
'is also a FAIL.  InternVL3 at τ = −∞ is not detected on COCO or on either NoCaps set (Table 7).'
~~~

NEW:

~~~text
is also a FAIL. InternVL3 at τ = −∞ is not detected on COCO or on either NoCaps set (Table 4).
~~~

### E29 | unit F1

- Basis: new cut: Fig. 1 removed; every interval it draws is printed in the two results tables
- Saving: 1.00

OLD:

~~~text
'<!-- p:F1 -->![**Fig. 1.** `ret` − `rand` on the four scored sets, per backbone and pooled, with the paired bootstrap CIs of Sect. 4. Pooled rows are the registered estimands (P1, XM-a, P1-EN, S-NC); per-backbone rows are reported rows, InternVL3 at its frozen τ. The Vietnamese panel is in stripped CIDEr-D and the English panel in PTB CIDEr-D; no cross-language difference is computed. Solid line: zero. Dashed line: the registered +2.0, which is a different quantity on each scale; the XM-a rule had no point threshold.](fig1_ret_minus_rand.svg)'
~~~

NEW:

~~~text
(deleted)
~~~

### E30 | unit S6-04

- Basis: follows E29: the reading points at the two results tables; the last sentence keeps the caption's statement on the two scales
- Saving: costs 0.02

OLD:

~~~text
"In Fig. 1 the registered retrieved-against-random predictions passed only where the memory and the test set share a source. Memory source and test set changed together, and Qwen2.5-VL's out-of-source rows stayed above zero, so this is an observation and not a tested cause."
~~~

NEW:

~~~text
In Table 3 and Table 4 the registered retrieved-against-random predictions passed only where the memory and the test set share a source. Memory source and test set changed together, and Qwen2.5-VL's out-of-source rows stayed above zero, so this is an observation and not a tested cause. No cross-language difference is computed.
~~~

### E31 | unit S7-D12

- Basis: addition, so that no cut row leaves silently (nothing is removed from the bullet)
- Saving: costs 0.05

OLD:

~~~text
'the cosine dose-response, the style report, the source share of shown examples and neighbour-only object precision.'
~~~

NEW:

~~~text
the cosine dose-response, the style report, the source share of shown examples, neighbour-only object precision, the copy baselines and the PTB-tokenised column of the Vietnamese sets. Also not printed: the English score of each arm and the NoCaps rows by domain label.
~~~

## 3. What the cuts removed, by kind

**Units removed whole (7):** `S2-01` (opening of related work), `T1` (related-work table), `S3-02b` (definition of the copy baselines), `T2` (configuration table), `T3` (sets table), `S5-10` (copy baselines and the PTB column), `F1` (the figure).

**Where the cells of the removed sets table are now:**

| fact of the sets table (v2.1) | now in |
|---|---|
| Vietnamese memory: 10,501 images, 8,190 clusters; 3,469 + 9,088 = 12,557 candidates less 2,056 | S3-01 (unchanged) |
| KTVIC development carve, stage A | S3-01, S3-05, S4-02 (the set name with its digits is no longer printed) |
| OV-dev-A 911 and OV-dev-B 925, halves by a hash order, filtered | S4-02 |
| XM-dev500: 500, the first images of the hash-ordered remainder, stage-B secondary | S4-01 |
| OV-test primary 1,941 = 2,001 minus 60 by the filter | S4-01; the 2,001-image sensitivity in the caption of the rules table |
| XM-test2500 = 3,600 minus 600 minus 500; sensitivity 2,392 without the 108 three-reference images | S4-01; caption of the rules table |
| English memory: 112,255 images, 111,927 clusters, COCO Karpathy train and restval after the same filter rules | S6-01 |
| COCO Karpathy test 5,000, the full split; NoCaps val 4,500, the full split | S6-01; header of the English results table |
| NoCaps sensitivity 3,500, without the images decoded earlier by another study of the group | caption of the rules table; S7-D02 |
| which prediction is tested on which set | rules table |
| NoCaps domain counts 417, 2,670, 1,413 | removed with the domain rows (E25) |

**Numbers no longer printed (44 keyed pairs, all in Annex D1 of the plan):** C27 (8: the two copy-baseline contrasts and the two near-verbatim shares), C28 (6: the PTB column on the two Vietnamese sets), C32 (3: the NoCaps domain counts), C41 (9: the NoCaps rows by domain label), C42 (6: `rand` minus `zs` on COCO), C43 (12: the English score of each arm). None is a registered verdict, a registered negative label, a registered sensitivity or a post hoc overlap row. The bullet S7-D12 ("Not reported here") names the copy baselines, the PTB column, the English score of each arm and the NoCaps rows by domain label.

**Reference entries that left (7), each only because the sentence that cited it left:** Joshi2020StateFate (E01), Ramos2023SmallCap (E04), Chen2025TrueMICL (E05), Vu2025VELVET, Vu2026ViG, Nguyen2026FAIR (E06b), Devlin2015NN (E08). 27 keys remain.

**Statements of the removed captions that were kept elsewhere:** "no cross-language difference is computed" (figure caption) is now the last sentence of S6-04; "a different scale" stays in S6-01; the English arms `ret`, `rand`, `zs` (so no `fix` arm) stay in S6-01; the note that the +2.0 was carried to the PTB scale without recalibration stays in S7-D04; the XM-a rule without a point threshold stays in the rules table.

**Not touched:** the abstract; S1-04 to S1-07; S4-03, S4-04, S4-05; the Vietnamese results table (label renumbered only); S5-01 to S5-09 except three table numbers; every bullet of Section 7 except the addition to S7-D12; the compute line; Section 8; the end sections with their [PI] placeholders. The two units that wait for the re-check after 16 Nov 05:00Z are byte-unchanged: the dagger note with S5-09 (C26) and S7-L06 (C44).

## 4. Checker

`check_draft.py` 281e087565af30c0ba8ae62dc56d466b4d9c85659d09e822a7666c8300bda21f (byte copy of the v2.1 file), run inside `draft_v3_cut/` with `python3 -I -B`: `--sync-first-words`, then `--build-manifest ../WRITING_PLAN_C_TAIMMA_v1.md`, then plain mode to `CHECKS.md`.

- `number_manifest_TAIMMA.tsv` was copied unchanged from v2.1 (506ab1d6...). The second mode rewrites it, as it did for v2 and v2.1: 303 of 303 Annex D1 pairs found, 251 rows written (v2.1: 295), 51 pairs not printed (the 7 of v2.1 and the 44 listed in section 3). No row was typed by hand.
- `PARAGRAPH_SOURCES.tsv`, edited by a script: the 7 rows of the removed units deleted (79 to 72 rows); column 3 of S2-05, S3-05, S4-01, S4-02 and S6-01 extended with the source of the table whose content moved there; column 4: C03 added to S4-02 (the sizes 911 and 925), C43 taken off T5, C42 off S6-02, C41 off T7 and S6-03. Column 2 was refreshed by the first mode.
- Plain mode: 10 of 13 PASS, 3 FAIL.

| check | result | measured |
|---|---|---|
| Paragraph markers and PARAGRAPH_SOURCES.tsv | FAIL | 72 units, 72 rows, 49 of 54 claim-map rows carried |
| Limits known today (abstract 150 to 250 words, 7 tables, 1 figure) | FAIL | title 14 words, abstract 212 words, 5 keywords, 4 tables, 0 figure |
| Plan word budgets (every section at or under its planned words) | FAIL | running text 4522 against 4100 planned; sections over their budget: Abs +12, §3 +143, §4 +99, §7 +184, §8 +46, Decl +92 |
| Numbers keyed (token -> manifest row, by section and claim) | PASS | 344 numeric tokens, 0 without a row |
| Estimate and CI read from one key | PASS | 74 triples, 0 without a single key stem |
| Manifest rows equal the source manifest and are all printed | PASS | 251 rows (27 label rows), 0 problems |
| Registered negatives and labels (plan A.5) | PASS | 24 required statements, 0 missing |
| Citation keys exist in the bib | PASS | 27 keys used, 0 not in the bib (67 entries) |
| No host or IP pattern | PASS | 0 hits |
| No writing-tool statement | PASS | 0 hits |
| No promotional word | PASS | 0 hits |
| No journal-only content | PASS | 0 hits outside the allowed sentences, 4 allowed |
| No data-set caption text | PASS | 0 Vietnamese letters, 0 unexpected quoted strings |

The three FAILs:

1. **Paragraph markers: FAIL, 49 of 54 claim-map rows carried.** The five rows are C27, C28, C41, C42, C43: the cut content itself. C28, C42 and C43 are on the cut list of CC-414 Ruling 2 (c4); C27 (ruled down to one clause) and C41 (ruled down to a pointer at the table) are cut further here. The check would pass if the five ids were left in column 4, but that column would then be untrue. Markers, rows and first words all match (72 units, 72 rows).
2. **Limits known today: FAIL, 4 tables and 0 figures.** The unchanged checker holds the constants "7 tables, 1 figure" of the plan. Abstract (212 words), title and keywords are inside their limits.
3. **Plan word budgets: FAIL, 4,522 against 4,100** (v2.1: 4,647). Known since v2; CC-414 ruled that the page count decides, not this figure. Sections 1, 2, 5 and 6 are now under their word budgets.

The check "Registered negatives and labels (plan A.5)" passes with 24 of 24 required statements, the same 24 places as in v2.1.

## 5. Open points for the ruling and for the PI

- Everything beyond c1 to c4 needs a ruling: the figure, the configuration table, the sets table, the two-column rules table, the NoCaps domain rows, the copy baselines, S2-01, one sentence of S2-02, one clause of S1-01, one sentence of S2-04.
- E06b removes the only citation of the group's own earlier conference paper, with two other Vietnamese captioning papers. It is the last cut in the order and the first to restore (+0.33 page). A PI decision.
- With 4 tables and no figure, the checker's constants (7 and 1) and the plan's table list (section C.4) need an update if this option is taken.
- The addition to S7-D12 and the last sentence of S6-04 are new sentences. They state what is not printed and repeat a caption statement; they carry no number.
- `PARAGRAPH_SOURCES.tsv` column 3 still points at the journal lines of d558df0, as in v2.1 (to refresh at G2).

## 6. Files (sha256)

| file | sha256 |
|---|---|
| `paper.md` | 0019a2c4387859a65fb1da15a4439bc7b6f2ac116ab4aebbf53e1f3469a9260d |
| `V2_1_TO_V3.diff` | f3d1d45ec89b0251b06065c85ef0f180c2f60c343c94fe6b2a7a9a5e73b8ef66 |
| `number_manifest_TAIMMA.tsv` | 65fa8654d61f5fa2f811652eab73a21c8e03103dbf3554f5c720ae15ef1ff933 |
| `PARAGRAPH_SOURCES.tsv` | a1838b7c069dff98eb69294a3e90d5e11b00a868522a296086be8706cfc07d94 |
| `CHECKS.md` | 67d62fd520c9be5cdd7c981e5a5baad35dfe429bc5bc459a9570eaf92a4002a8 |
| `check_draft.py` | 281e087565af30c0ba8ae62dc56d466b4d9c85659d09e822a7666c8300bda21f |
| `PAGE_BUDGET.md` | 490b4ba74d678bc17abd2285e65057c1e16668a1c717195bf02055bca60c676d |
| `CUT_PLAN.md` | 04208a51690b2fbdbf2ec111793e58b4559618a242e6d3ffb33a9593090f36be |

No label folder, key file, sealed folder or held folder was opened. Under `.session_backup/2026-11-15/` only `taimma_build/` was read. No existing file was changed and no commit was made.
