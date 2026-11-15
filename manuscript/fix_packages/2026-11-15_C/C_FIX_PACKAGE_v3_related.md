# Paper C (journal version, ACM TALLIP): fix package v3, related-work rows

Prepared 2026-11-15T01:06Z (2026-11-15, 08:06 Vietnam time). Nothing in this package has been applied, staged or committed. It is for a judge to read first.

## 0. Scope, state it applies to, and conventions

- **What it is.** The text changes that follow from the full-text check of the related-work rows (`manuscript/reviews/RELATED_FULLTEXT_CHECK_2026-11-15.md`, sha256 `8fa296ddedd5dac7ca42e58a5e2fc1aefcfb0fb795b974b9ba08333f8b1e1f81`; ids such as "C-66" below are the verdict lines of that file). It closes the reading half of item C-N15 of fix package v1 (two works described "from the abstract", the OpenFlamingo numbers) for the works that could be read. The dated systematic search of C-N15 is not part of it.
- **Paper HEAD the OLD strings were checked against:** `9b8e6ae` (`9b8e6aecd17c6107dfbb4e06ebea4f83fb87545e`), read with `git show`.
- **Two files change:** `paper_v1_analysis/02_related_work.md` (7 blocks) and `docs/TABLE1B_W5_EVIDENCE.md` (7 blocks; an internal evidence file, not paper text).
- **Independent of the freeze shell C2.** `c_attr_c2_transfer.py` (sha256 `030c369d…`) changes `06_results.md`, `05_preregistration_and_analysis.md`, `07_disclosures.md`, `03_method.md` and `number_manifest_C.tsv`, and its gate looks only at those five files. Neither file of this package is among them.
- **Independent of fix package v2.** The file list of `apply_c_v2.py` (and of `apply_c_v2_cc408.py`, the package as ruled) is `00_abstract.md`, `01_introduction.md`, `03_method.md`, `04_data_and_splits.md`, `05_preregistration_and_analysis.md`, `06_results.md`, `08_english_comparison.md`, `09_limitations.md`, `11_supplement_registered_rows.md`, `V2_PROGRESS_C.md` and the manifest. `02_related_work.md` is not in that list: `apply_c_v2.py` names it in `UNTOUCHED` and asserts that it does not change. `docs/TABLE1B_W5_EVIDENCE.md` is outside `paper_v1_analysis/`. There is no file in common, so the OLD strings here are the same before and after shell C2 and before and after package v2 (checked in memory, section 5).
- **Order.** Any order is possible. Two gates of the scripts matter in practice: (1) the write mode of `apply_c_v2_cc408.py` requires every section file to be clean against HEAD, so if this package is written first it must be committed before package v2 is written; (2) the write mode of `apply_c_v3_related.py` refuses when anything is staged, so that the package becomes a commit of its own.
- **What it does not touch.** `03_method.md`, `05_preregistration_and_analysis.md`, `06_results.md`, `07_disclosures.md`, `number_manifest_C.tsv`, Sections 5.7 and 6.10, the abstract, the bibliography. The RAGCap row of Table 1 keeps "from its abstract" and its three "–" cells, because that work could not be read.
- **Block format** as in v1 and v2: the OLD string is the text between the `OLD>>>` line and the `NEW>>>` line, without the line break that ends it; the NEW string likewise, up to the `EVIDENCE>>>` line; an `END>>>` line closes the block. The file token is the path inside the paper repository. Block ids are `C-L01` … `C-L13`.
- **Apply script:** `manuscript/fix_packages/2026-11-15_C/apply_c_v3_related.py`. Default mode is a check that writes nothing; `--write --ruling <id>` writes the two files to the working tree only if the results equal the targets of section 5.
- **Custody.** Public full texts of cited works and the paper's own related-work section only. No test-set score book, per-image ledger, caption file, label file or key file was opened. No dataset caption and no model output is printed. No number of the paper changes.

## 1. Table of items

| id | check line | file | line at 9b8e6ae | what | status |
|---|---|---|---|---|---|
| C-L01 | C-66 (WRONG) | `paper_v1_analysis/02_related_work.md` | 9 | Li et al. 2024: SmallCap is robust to the order of the retrieved captions, not sensitive to it | BLOCK |
| C-L02 | C-05, C-51, C-71, C-86 | `paper_v1_analysis/02_related_work.md` | 30 | Table 1 caption: one sentence on the language cells; the "–" sentence now names the one row it covers | BLOCK (goes with C-L03) |
| C-L03 | C-05, C-06, C-07 | `paper_v1_analysis/02_related_work.md` | 49 | Table 1, Sarto row: "from the abstract" removed, three "–" cells filled | BLOCK |
| C-L04 | C-51, C-71, C-86, C-97, C-108 | `paper_v1_analysis/02_related_work.md` | 52 | Table 1b caption: language cells; what "no" means in the last two columns; the "–" clause goes | BLOCK (goes with C-L05) |
| C-L05 | C-47 | `paper_v1_analysis/02_related_work.md` | 61 | Table 1b, MUNIChus row: "registered, one look" from "–" to "no" | BLOCK |
| C-L06 | C-77 (WRONG) | `paper_v1_analysis/02_related_work.md` | 57 | Table 1b, Li et al. 2024 row: "decoder columns in one table" corrected | BLOCK |
| C-L07 | C-81, C-82 (qualification) | `paper_v1_analysis/02_related_work.md` | 20 | Baldassini et al.: the voting finding is for classification; for captioning the paper says otherwise | BLOCK (recommended; a judge may strike it) |
| C-L08 | – | `docs/TABLE1B_W5_EVIDENCE.md` | 3 | head paragraph: the re-check of 2026-11-15 and the versions read | BLOCK (goes with C-L05) |
| C-L09 | C-77 | `docs/TABLE1B_W5_EVIDENCE.md` | 16 | evidence row behind C-L06 | BLOCK (goes with C-L06) |
| C-L10a | label error | `docs/TABLE1B_W5_EVIDENCE.md` | 31 | Li et al. 2025: "§V-A" is Section IV-A in arXiv v1 | BLOCK |
| C-L10b | label error | `docs/TABLE1B_W5_EVIDENCE.md` | 32 | the same label, second row | BLOCK |
| C-L11 | C-29 to C-49 | `docs/TABLE1B_W5_EVIDENCE.md` | 36 | new evidence rows for MUNIChus | BLOCK (goes with C-L05) |
| C-L12 | C-01 to C-07 | `docs/TABLE1B_W5_EVIDENCE.md` | 38 | new evidence paragraph for the Sarto row of Table 1 | BLOCK (goes with C-L03) |
| C-L13 | C-117 | `docs/TABLE1B_W5_EVIDENCE.md` | 40 | Outcome sentence: six papers, MUNIChus included | BLOCK (goes with C-L11) |
| – | C-08 to C-16 | `02`, `03`, `06` | – | RAGCap: row, sentence and the label "as used by RAGCap" | NOT CHANGED: work not read (section 3) |
| – | C-116 | `01_introduction.md` | 9 | "These analyses are in English." | NOT IN THIS PACKAGE (section 3) |
| – | T-01 to T-18 | conference draft | – | blocks T-1 to T-3 of the check file | NOT IN THIS PACKAGE (section 3) |

Counts: 14 OLD/NEW blocks under 13 ids; 7 in the paper file, 7 in the evidence file. Two blocks correct a wrong statement (C-L01, C-L06), two fill cells (C-L03, C-L05), two are caption notes (C-L02, C-L04), one is a recommended qualification (C-L07), seven keep the evidence file in step. No block falls in `03`, `05`, `06`, `07` or the manifest, so nothing is deferred for the freeze.

Groups that stand or fall together: {C-L02, C-L03, C-L12}; {C-L04, C-L05, C-L08, C-L11, C-L13}; {C-L06, C-L09}. C-L01, C-L07, C-L10a and C-L10b are free-standing. The apply script holds pinned targets for the full package and for the package without C-L07; any other choice needs targets fixed by the ruling.

## 2. Blocks

### C-L01. Li et al. 2024: order robust, content sensitive (check line C-66, WRONG)

The paper file says that retrieval-augmented captioners "are sensitive to their order and selection". The cited paper reports the opposite for the order, in a section headed "Order Robust but Content Sensitive", and it studies one captioner, SmallCap. The sentence that follows in the paper file ("This motivates our copy diagnostics …") is unchanged and still follows.

```text
<<<C-L01 paper_v1_analysis/02_related_work.md OLD>>>
The same study [@Li2024RetrievalRobustness] finds that retrieval-augmented captioners copy tokens from the retrieved captions and are sensitive to their order and selection.
<<<C-L01 paper_v1_analysis/02_related_work.md NEW>>>
The same study [@Li2024RetrievalRobustness] finds that SmallCap is robust to the order of the retrieved captions but sensitive to which captions are retrieved, and that tokens shared by most of the retrieved captions are likely copied into its output.
<<<C-L01 EVIDENCE>>>
Source: Li, Li, Ramos, Tang and Elliott, ACL 2024 proceedings PDF (https://aclanthology.org/2024.acl-long.503.pdf, sha256 1109b0474610…, pp. 9285–9299).
Order: Section 3.3, p. 9287, heading "Order Robust but Content Sensitive"; quote: "is indeed robust to the order of the retrieved texts".
Content: Section 3.3, p. 9287; quote: "performance drops drastically compared to the no-retrieval baseline" (with captions retrieved for another image in place of the top-k captions).
Copying: abstract, p. 9285; quote: "those tokens are likely copied into the generated output" (tokens that appear in the majority of the retrieved captions).
One model: the abstract and Section 3 study SmallCap with a GPT-2 and an OPT-350M decoder; no second captioner is tested, so "retrieval-augmented captioners" becomes "SmallCap".
Same finding elsewhere in the paper, unchanged and consistent with NEW: 02_related_work.md l.7 (captions retrieved for another image); 06_results.md l.122 (tokens shared by most retrieved captions; training with sampled captions).
<<<C-L01 END>>>
```

### C-L02. Table 1 caption: language cells; which row the "–" belongs to (check lines C-05, C-51, C-71, C-86)

The caption says the table is "as stated in each paper". For several rows the language is not stated: the papers name their data sets and never the language. After C-L03 the only "–" cells of Table 1 are those of the RAGCap row. This block presupposes C-L03.

```text
<<<C-L02 paper_v1_analysis/02_related_work.md OLD>>>
The statistics column records CIs or tests on the captioning score. "–" means not stated in the part of the work that was read.
<<<C-L02 paper_v1_analysis/02_related_work.md NEW>>>
The statistics column records CIs or tests on the captioning score. A language cell gives the language of the caption data where a paper does not name it. The RAGCap row rests on the abstract of that work; "–" means not stated there.
<<<C-L02 EVIDENCE>>>
Language: hits of the word "English" in the full texts read on 2026-11-15: Sarto et al. 0; Yang et al. 0; Baldassini et al. 0 (paper and supplement); Li et al. 2024: 1, inside an example. Their caption data are COCO, nocaps, Flickr30K and VizWiz. The rows of Table 1 that this check did not read (SmallCap, EXTRA, LMCap, CONCAP, MeaCap, EVCap, ViECap, Rebelo et al.) are covered either way by "where a paper does not name it".
"–": after C-L03 the script asserts that the RAGCap row is the only row of Table 1 with a "–" cell. The RAGCap row is byte-unchanged: its full text was not read (TechRxiv answered an automated read with HTTP 403; the journal article is not open access).
<<<C-L02 END>>>
```

### C-L03. Table 1, Sarto row: full text read, three cells filled (check lines C-01 to C-07)

```text
<<<C-L03 paper_v1_analysis/02_related_work.md OLD>>>
| @Sarto2024RetrievalArch, from the abstract | yes | yes | text from an external memory | – (COCO, nocaps) | – | – |
<<<C-L03 paper_v1_analysis/02_related_work.md NEW>>>
| @Sarto2024RetrievalArch | yes | yes | text from an external memory | English (COCO, nocaps) | no | none |
<<<C-L03 EVIDENCE>>>
Source: Sarto, Cornia, Baraldi, Nicolosi and Cucchiara, arXiv 2405.13127 v1 (sha256 1ef3c03cc20b…, 22 pages; page 1 carries the ACM reference format of the journal article). Read: Sections 1, 3.1–3.3 and 4; all pages searched. The ACM article itself was not read (the publisher and the university repository answered HTTP 403).
trained "yes": Section 4.1, p. 11; quote: "we employ the standard two-stage training protocol typically used by almost all captioning models".
sees the image "yes": Section 3.1, p. 5; quote: "we condition our language model on both the input image".
retrieved content, unchanged: Section 3.2, p. 6; quote: "the external memory can return all the captions of the selected images".
languages: data sets in Section 4.1, p. 10; quote: "we train our model on COCO and evaluate on nocaps validation set". The word "English" has 0 hits, so the cell gives the language of the caption data (C-L02).
random control "no", as far as the paper states: "random" has 0 hits in the whole text. The comparisons are a Transformer without retrieval (Table 3, p. 14) and an oracle over the k nearest captions (Table 1, p. 12); quote: "in comparison with Transformer-based baselines that do not leverage additional knowledge retrieved from an external memory".
statistics "none": 0 hits for "confidence interval", "bootstrap", "standard deviation", "std", "±", "seed", "p-value", "error bar"; Tables 2 to 5 give single values.
The sentence on this work at l.7 is confirmed and unchanged.
<<<C-L03 END>>>
```

### C-L04. Table 1b caption: language cells; what "no" means; the "–" clause (check lines C-51, C-71, C-86, C-97, C-108)

After C-L05 no cell of Table 1b holds "–", so the clause that explains it goes. This block presupposes C-L05.

```text
<<<C-L04 paper_v1_analysis/02_related_work.md OLD>>>
Entries follow each paper's own statement; "–" means not stated or not applicable.
<<<C-L04 paper_v1_analysis/02_related_work.md NEW>>>
Entries follow each paper's own statement; a language cell gives the language of the caption data where a paper does not name it, and "no" in the last two columns means that a search of the paper's full text found no such statement.
<<<C-L04 EVIDENCE>>>
Language: the word "English" has 0 hits in Yang et al. (NeurIPS PDF), Baldassini et al., Chen et al. 2025 and Li et al. 2025, and 1 hit, inside an example, in Li et al. 2024. MUNIChus names its nine languages.
"no": for each of the six rows the full text was searched for "preregist", "pre-regist" and "registered" (0 hits in all six) and for "confidence interval", "bootstrap", "standard deviation", "std", "±", "seed", "p-value", "error bar" (counts in section 2.0 of the check file). What the searches found is already in the cells: "mean of three seeds", "mean of three runs; tests on the analyses", "SDs on a non-captioning task only".
One row rests on a preprint: for Li et al. (TPAMI 2026) the text searched is arXiv 2507.08021 v1; the journal article is not open access (section 3, for the investigator).
The script asserts that no cell of Table 1b is "–" after C-L05.
<<<C-L04 END>>>
```

### C-L05. Table 1b, MUNIChus row: "registered, one look" is "no" (check line C-47)

OLD and NEW are the last four cells of the row; the rest of the row is unchanged.

```text
<<<C-L05 paper_v1_analysis/02_related_work.md OLD>>>
| yes, k = 3, examples with image and article excerpt | yes | – | no |
<<<C-L05 paper_v1_analysis/02_related_work.md NEW>>>
| yes, k = 3, examples with image and article excerpt | yes | no | no |
<<<C-L05 EVIDENCE>>>
Source: Chen et al., LREC 2026 proceedings PDF (http://www.lrec-conf.org/proceedings/lrec2026/pdf/2026.lrec2026-1.708.pdf, sha256 93510c99a28b…, pp. 9008–9017); its body text is the same, word for word, as arXiv 2603.10613 v1 apart from reading order, page numbers and the proceedings footer.
Search of the whole text: "preregist" 0, "pre-regist" 0, "registered" 0. The cell gets "no" on the same basis as the five rows above it.
The other cells of the row are confirmed (check lines C-41 to C-48): nine languages, Table 1, p. 9009; three random and three similar examples, Sections 3.1.2 and 3.1.3, pp. 9010–9011; seven models, Table 2, p. 9012; point scores only.
<<<C-L05 END>>>
```

### C-L06. Table 1b, Li et al. 2024 row: decoder columns (check line C-77, WRONG)

```text
<<<C-L06 paper_v1_analysis/02_related_work.md OLD>>>
| yes, equal k | decoder columns in one table | no | no (mean of three seeds) |
<<<C-L06 paper_v1_analysis/02_related_work.md NEW>>>
| yes, equal k | decoder columns in the order-test tables only | no | no (mean of three seeds) |
<<<C-L06 EVIDENCE>>>
Source: ACL 2024 proceedings PDF as in C-L01.
Both decoders (GPT-2 and OPT) have columns in Table 1, p. 9287 (order of the retrieved captions, COCO), in Table 2, p. 9288 (the same on NoCaps) and in appendix Tables 6 and 7, p. 9296: four tables, not one, and all of them on the order test. The random-caption comparison (Fig. 2, Table 3) is not split by decoder; Section 5.1, p. 9291, trains with the OPT-350M decoder only.
<<<C-L06 END>>>
```

### C-L07. Baldassini et al.: the voting finding is for classification (check lines C-81, C-82; recommended)

The sentence in the paper file follows the abstract of the cited paper. The body of that paper limits the majority-vote finding to classification and says the opposite for captioning. The next clause of the paper file ties the finding to a captioning baseline, so the qualification matters here. A judge may strike this block; the script holds a target for the package without it.

```text
<<<C-L07 paper_v1_analysis/02_related_work.md OLD>>>
@Baldassini2024MICL find that multimodal in-context learning in open interleaved models is driven mainly by the text of the examples, and that similarity-based example selection does no better than majority voting over the examples' answers; our `nn_cons` baseline, the consensus caption of the k nearest neighbours, is the captioning counterpart of that voting baseline.
<<<C-L07 paper_v1_analysis/02_related_work.md NEW>>>
@Baldassini2024MICL find that multimodal in-context learning in open interleaved models is driven mainly by the text of the examples, and that, for classification, similarity-based example selection does no better than majority voting over the examples' answers; for captioning they report that such voting is insufficient and that the example images also contribute. Our `nn_cons` baseline, the consensus caption of the k nearest neighbours, is the captioning counterpart of that voting baseline.
<<<C-L07 EVIDENCE>>>
Source: Baldassini, Shukor, Cord, Soulier and Piwowarski, CVPR 2024 Workshops, open-access version of the Computer Vision Foundation (sha256 2cd7d0b6bb6c…, pp. 1539–1550), which states that it is identical to the accepted version except for a watermark.
General finding, kept: abstract, p. 1539; quote: "M-ICL primarily relies on text-driven mechanisms, showing little to no influence from the image modality".
Voting, as the abstract has it: p. 1539; quote: "M-ICL is not better than a simple strategy based on majority voting over context examples".
Voting, in the body: Section 5.1, p. 1545; quotes: "in classification tasks, M-ICL’s effectiveness is comparable to that of a KNN"; "In open-ended generation tasks, i.e. captioning and visual question answering, majority voting is insufficient".
Example images in captioning: Section 4.2, p. 1542; quote: "Incorporating images further enhances performance by an additional 20 points, underscoring the importance of both modalities".
The sentences after this one in l.20 (Chen et al. 2025; "Both findings are why the `rand` control is needed") are unchanged and still follow: the text-driven finding is kept.
<<<C-L07 END>>>
```

### C-L08. Evidence file, head paragraph: the re-check and the versions read

```text
<<<C-L08 docs/TABLE1B_W5_EVIDENCE.md OLD>>>
Checked 2026-11-09 against each paper's own text (PDF or arXiv HTML/PDF full text; arXiv versions where the proceedings PDF was not used, as noted). Each paper's text was searched for "preregist", "pre-regist", "registered", "±", "std", "seed", "confidence", "bootstrap". "–" in the paper table = not stated or not applicable.
<<<C-L08 docs/TABLE1B_W5_EVIDENCE.md NEW>>>
Checked 2026-11-09 against each paper's own text (PDF or arXiv HTML/PDF full text; arXiv versions where the proceedings PDF was not used, as noted). Each paper's text was searched for "preregist", "pre-regist", "registered", "±", "std", "seed", "confidence", "bootstrap". Re-checked 2026-11-15 on the proceedings versions where they are open: the NeurIPS 2023 PDF of Yang2023ICLConfig (same text as arXiv v6), the ACL 2024 PDF of Li2024RetrievalRobustness, the open-access CVPR Workshops PDF of Baldassini2024MICL with its supplement, and the LREC 2026 PDF of Chen2026MUNIChus. Chen2025TrueMICL was re-checked on arXiv v2, which carries the COLM 2025 header, and Li2025UnveilingICL on arXiv v1 only, because the TPAMI article is not open. After that re-check no cell of Table 1b holds "–". Record: manuscript/reviews/RELATED_FULLTEXT_CHECK_2026-11-15.md in the run repository.
<<<C-L08 EVIDENCE>>>
Versions and sha256 of every PDF: section 1 of the check file. The NeurIPS PDF and arXiv 2305.14800 v6 were compared word by word: identical except the arXiv stamp.
The last OLD sentence goes because, after C-L05, Table 1b holds no "–".
<<<C-L08 END>>>
```

### C-L09. Evidence row behind C-L06

```text
<<<C-L09 docs/TABLE1B_W5_EVIDENCE.md OLD>>>
| | per-backbone rows | decoder columns in one table | Table 1 (order test); §5.1 uses OPT only |
<<<C-L09 docs/TABLE1B_W5_EVIDENCE.md NEW>>>
| | per-backbone rows | decoder columns in the order-test tables only | Tables 1 and 2 (order test, COCO and NoCaps; appendix Tables 6 and 7); §5.1 uses OPT only |
<<<C-L09 EVIDENCE>>>
As C-L06. The third cell is the cell of Table 1b after C-L06, byte for byte (asserted by the script).
<<<C-L09 END>>>
```

### C-L10a and C-L10b. Evidence file: the section label of Li et al. 2025

In arXiv 2507.08021 v1 the experiments are Section IV ("IV. Experiments and Analyses", with "A. Datasets and Settings" on p. 7), and Section V is the conclusion. The evidence file says "§V-A" twice. No cell of the paper changes.

```text
<<<C-L10a docs/TABLE1B_W5_EVIDENCE.md OLD>>>
| Li2025UnveilingICL (TPAMI; checked on arXiv 2507.08021) | data | COCO | §V-A, p. 7 (Karpathy split) |
<<<C-L10a docs/TABLE1B_W5_EVIDENCE.md NEW>>>
| Li2025UnveilingICL (TPAMI; checked on arXiv 2507.08021) | data | COCO | §IV-A, p. 7 (Karpathy split) |
<<<C-L10a EVIDENCE>>>
arXiv 2507.08021 v1 (sha256 97fe281b204e…), p. 7, Section IV-A; quote: "we use the Karpathy split [78] in the experiments".
<<<C-L10a END>>>
```

```text
<<<C-L10b docs/TABLE1B_W5_EVIDENCE.md OLD>>>
| | models | OpenFlamingo-v2-9B, IDEFICS-9B | §V-A |
<<<C-L10b docs/TABLE1B_W5_EVIDENCE.md NEW>>>
| | models | OpenFlamingo-v2-9B, IDEFICS-9B | §IV-A, p. 7 |
<<<C-L10b EVIDENCE>>>
The same page and section; quote: "IDEFICS v1-9B [28] are employed for evaluating".
<<<C-L10b END>>>
```

### C-L11. Evidence file: rows for MUNIChus

The rows are added after the last row of Li2025UnveilingICL. The third cell of each row is the cell of Table 1b after C-L05.

```text
<<<C-L11 docs/TABLE1B_W5_EVIDENCE.md OLD>>>
| | CIs | no | full-text search: no seeds, SD, CI or tests |
<<<C-L11 docs/TABLE1B_W5_EVIDENCE.md NEW>>>
| | CIs | no | full-text search: no seeds, SD, CI or tests |
| Chen2026MUNIChus (LREC 2026 proceedings, pp. 9008–9017; body text identical to arXiv 2603.10613 v1) | language(s) | Arabic, Chinese, English, French, Hindi, Indonesian, Japanese, Sinhala, Urdu | Table 1, p. 9009 (column heads); "Vietnam": no hit |
| | data | MUNIChus (BBC news images with their articles) | §2, p. 9009 ("We developed a Python-based scraper to collect BBC news articles in the languages listed in Table 1") |
| | models | seven MLLMs under prompting, including Qwen2.5-VL-7B, Qwen3-VL-8B and Aya-Vision-8B | Table 2, p. 9012 (Aya-vision-8b, Aya-vision-32b, GPT-4o, Llama-3.2-11B, Phi-3.5-vision, Qwen2.5-VL-7B, Qwen3-VL-8B); §3.2, p. 9011: two models are fine-tuned in a separate condition |
| | equal-k random control | yes, k = 3, examples with image and article excerpt | §3.1.2, p. 9010 ("three randomly sampled examples from the same language’s training set"); §3.1.3, p. 9011 (the three training instances most similar to the test image, in the same format) |
| | per-backbone rows | yes | Table 2, p. 9012: one row per model in each prompting block |
| | registered, one look | no | full-text search: no hit |
| | CIs | no | Table 2, p. 9012: one BLEU-4 and one CIDEr value per model and language; no hit for "±", "std", "confidence", "bootstrap"; "seed" only in a reference title; the number of random draws is not stated |
<<<C-L11 EVIDENCE>>>
Source: LREC 2026 proceedings PDF as in C-L05; check lines C-29 to C-49.
Quotes, each found by script in the extracted text: "We developed a Python-based scraper to collect BBC news articles in the languages listed in Table 1" (p. 9009); "three randomly sampled examples from the same language’s training set" (p. 9010).
The seven model names are the row labels of Table 2 in each of its three prompting blocks; Section 3.2, p. 9011, names the two fine-tuned models.
<<<C-L11 END>>>
```

### C-L12. Evidence file: a paragraph for the Sarto row of Table 1

The paragraph is added after the OpenFlamingo paragraph, so that the cells filled by C-L03 have their trail in the paper repository.

```text
<<<C-L12 docs/TABLE1B_W5_EVIDENCE.md OLD>>>
The appendix prose gives −20.4 / −13.1; the paper cites Table 9.
<<<C-L12 docs/TABLE1B_W5_EVIDENCE.md NEW>>>
The appendix prose gives −20.4 / −13.1; the paper cites Table 9.

**Table 1, Sarto2024RetrievalArch row (arXiv 2405.13127 v1, checked 2026-11-15; its first page carries the ACM reference format; the ACM article itself was not read).** Trained "yes": §4.1, p. 11 (two-stage training). Sees the image "yes": §3.1, p. 5 ("we condition our language model on both the input image"). Retrieved content: §3.2, p. 6 (the captions of the k nearest images). Languages "English (COCO, nocaps)": the data sets are named in §4.1, p. 10; the paper does not name the language ("English": no hit), so the cell gives the language of the caption data. Random control "no": "random": no hit; the comparisons are a Transformer without retrieval (Table 3, p. 14) and an oracle over the k nearest captions (Table 1, p. 12). Statistics "none": no hit for "±", "std", "seed", "confidence", "bootstrap"; Tables 2 to 5 give single values.
<<<C-L12 EVIDENCE>>>
As C-L03.
<<<C-L12 END>>>
```

### C-L13. Evidence file: the Outcome sentence counts MUNIChus

```text
<<<C-L13 docs/TABLE1B_W5_EVIDENCE.md OLD>>>
**Outcome.** None of the five analysis papers preregisters its contrasts or reports CIs (or SD/SE/tests) on the captioning score, so the sentence in Section 1 scoped to these analyses holds and the CC-212 falsifier is not triggered.
<<<C-L13 docs/TABLE1B_W5_EVIDENCE.md NEW>>>
**Outcome.** None of the six papers of Table 1b (the five analysis papers and the MUNIChus benchmark paper) preregisters its contrasts or reports CIs (or SD/SE/tests) on the captioning score, so the sentence in Section 1 scoped to these papers holds and the CC-212 falsifier is not triggered.
<<<C-L13 EVIDENCE>>>
Sentence of Section 1 (01_introduction.md l.9, unchanged): "As far as these papers state, none preregisters its contrasts or reports confidence intervals on the captioning score." It follows the mention of MUNIChus, so "these papers" are six. Check line C-117: 0 hits for the registration terms and for "confidence interval" in all six.
<<<C-L13 END>>>
```

## 3. Not changed, not in this package, and what needs the investigator

**Not changed, because the work was not read (9 check lines, C-08 to C-16).** RAGCap (Bazi, Al Rahhal and Zuair 2025): the row of Table 1 (l.48) keeps "from its abstract" and its "–" cells; the sentence at l.7 is unchanged. The label "an image-caption-pair prompt format, as used by RAGCap; not RAGCap" (`03_method.md` l.126; `06_results.md` l.231, Section 6.10) rests on the abstract only. Both files belong to the freeze shell, so nothing could be proposed for them here in any case.

**Not in this package:**
- `01_introduction.md` l.9, "These analyses are in English." (check line C-116). It is true of the data sets; the papers do not say it. A possible wording is "These analyses use English caption data." The file is in the list of package v2, so the sentence is left for a later package or for the rewrite.
- The conference version. Blocks T-1 to T-3 of the check file are written against `draft_v1/paper.md` by paragraph id, for the reviser of draft_v2.
- The dated systematic literature search of item C-N15.
- The other rows of Table 1 (SmallCap, EXTRA, LMCap, CONCAP, MeaCap, EVCap, ViECap, Rebelo et al.), which the paper does not mark as partly read and which the check did not read.

**Needs the investigator:**
1. RAGCap, by hand in a browser: the TechRxiv preprint (https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.174140786.66325581/v1) or the journal article (doi 10.1080/01431161.2025.2575514). To settle: caption language of its data sets, any random-example or no-retrieval condition, any statistics on the scores, and the layout of its prompt.
2. Li et al., IEEE TPAMI 2026 (doi 10.1109/TPAMI.2026.3719106): the row of Table 1b and its "no; no" rest on the preprint of 2025. Check Finding 5, the two models, the shot counts and whether seeds or intervals were added.
3. Sarto et al., ACM TOMM 2024 (doi 10.1145/3663667), version of record: low priority; the arXiv copy carries the journal's reference format.

## 4. After application

- `tex/body.tex` and the PDFs are derived files; they are rebuilt by the build script, not by this package.
- No manifest row is needed: the multiset of number tokens of `02_related_work.md` is the same before and after (asserted by the script).
- No citation key is added or removed.

## 5. Checks run

Method: the apply script in its default mode (nothing written), and a read-only harness that imported `apply_c_v2.py` and `apply_c_v2_cc408.py` as modules and called their functions on texts built in memory. Nothing was written to the paper repository.

| id | file | count of OLD at 9b8e6ae | count at its turn, package order | exactly once |
|---|---|---|---|---|
| C-L01 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-L02 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-L03 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-L04 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-L05 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-L06 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-L07 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-L08 | `docs/TABLE1B_W5_EVIDENCE.md` | 1 | 1 | yes |
| C-L09 | `docs/TABLE1B_W5_EVIDENCE.md` | 1 | 1 | yes |
| C-L10a | `docs/TABLE1B_W5_EVIDENCE.md` | 1 | 1 | yes |
| C-L10b | `docs/TABLE1B_W5_EVIDENCE.md` | 1 | 1 | yes |
| C-L11 | `docs/TABLE1B_W5_EVIDENCE.md` | 1 | 1 | yes |
| C-L12 | `docs/TABLE1B_W5_EVIDENCE.md` | 1 | 1 | yes |
| C-L13 | `docs/TABLE1B_W5_EVIDENCE.md` | 1 | 1 | yes |

Further checks, all passed:
- Paper HEAD at the time of the checks: `9b8e6ae`; both files clean against HEAD and byte-equal to `git show 9b8e6ae:`.
- 14 blocks under 13 ids; every NEW occurs exactly once after all blocks; applying the blocks in the reverse order gives byte-equal files; no two OLD spans overlap.
- Shell C2, built in memory from `git show 9b8e6ae:` with the transfer script's own functions (the method of `apply_c_v2_cc408.py`): `02_related_work.md` after C2 is byte-equal to its 9b8e6ae text. The file list of the shell is `06_results.md`, `05_preregistration_and_analysis.md`, `07_disclosures.md`, `03_method.md`, `number_manifest_C.tsv`.
- Package v2 as ruled (CC-408), built in memory on the after-C2 tree: it changes 11 files (ten section files and the manifest); `02_related_work.md` is not one of them.
- Order "this package, then shell C2, then package v2": with `02_related_work.md` replaced by the result of this package (all 14 blocks, and again without C-L07), the gate of `apply_c_v2_cc408.py` passes, its ten results equal the targets of CC-408 Ruling 9, and its manifest result is byte-equal to the one without this package. Its renumbering pass finds no table label 10 to 18 in the new text.
- Order "shell C2, then package v2, then this package": both files of this package are still their 9b8e6ae texts after the two, so the OLD strings and the targets below are the same.
- Number tokens of `02_related_work.md`, by the token rule of `apply_c_v2.py`: 60 before, 60 after, equal multisets. No manifest row is needed.
- After the package: the RAGCap row is byte-unchanged and is the only row of Table 1 with a "–" cell; no cell of Table 1b is "–"; the cell of C-L06 equals the cell quoted by C-L09.
- Words of `02_related_work.md` (comments stripped, whitespace split, tables included): 2,867 at 9b8e6ae, 2,950 after the package (+83); 2,932 without C-L07 (+65).
- Quotes: every string given as a quote from a cited work in the evidence lines and in the new evidence rows was found by script in the text extracted from the PDF named there; none is longer than 25 words; none is a dataset caption.
- Default mode of `apply_c_v3_related.py` on the present tree: every OLD once, all content checks passed, both results equal the targets below, nothing written.

sha256 of the two files before and after this package (the apply script holds the same values as `PRE` and `TARGETS`):

| file | at 9b8e6ae (the same after shell C2 and after package v2) | after this package, all 14 blocks | after this package without C-L07 |
|---|---|---|---|
| `paper_v1_analysis/02_related_work.md` | `da4ba3748a9b6f55d7b911378f14b19bbfa0a0588dd09b83f6bc1dd2bc14e887` | `8dbc299bd816bb2fd9ec689b1ef1b97a1c2cab1e331232072dc4d7afee1a60fb` | `a31d484361f8e794d59db6635d9a95917aa39e191856979316975b57aebff847` |
| `docs/TABLE1B_W5_EVIDENCE.md` | `415598fd8bb70d6ff4cb8f6862622657314aff2537d21e924d194f0a3668bce2` | `c3b5aa79df8109cbd7de45933ee77126c5c5a49b4ceab6daf93d01020157d56d` | `c3b5aa79df8109cbd7de45933ee77126c5c5a49b4ceab6daf93d01020157d56d` |

Not checked, and said so where it matters:
- The manifest check of the paper repository, the n-gram and caption scan and the LaTeX build were not run, because nothing was applied.
- The works named in section 3 were not read.
- If a judge changes a NEW text, `PKG_SHA256` and `TARGETS` of the apply script must be recomputed.
- If another commit changes one of the two files first, the script refuses (its `PRE` check), and the blocks must be checked again.

What was opened for this package: the two files it changes; `01_introduction.md`, `03_method.md`, `05_preregistration_and_analysis.md`, `06_results.md` and `08_english_comparison.md` for the lines that name these works; `apply_c_v2.py`, `apply_c_v2_cc408.py` and `c_attr_c2_transfer.py` for their file lists and gates; `C_FIX_PACKAGE_v1.md` and `C_FIX_PACKAGE_v2.md` for item C-N15; the check file and the public full texts it lists. Not opened: any label folder, key file, ledger, caption file or score book.
