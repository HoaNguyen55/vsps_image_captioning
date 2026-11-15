# Paper C (journal version, ACM TALLIP): fix package v4, works found by the dated search

**Applies after the CC-408 commit** (fix package v2 as ruled, itself applied after the freeze shell on 2026-11-16). Prepared 2026-11-15T03:34Z (2026-11-15, 10:34 Vietnam time). Nothing in this package has been applied, staged or committed. It is for a judge to read first.

## 0. Scope, state it applies to, and conventions

- **What it is.** The text changes that follow from the dated systematic search of item C-N15 (`manuscript/reviews/C_SYSTEMATIC_SEARCH_2026-11-15.md`, sha256 `acdae5aab11e0e8c2ababae41f9c5b907bb1626cc0c64182a42166acb22c5b38`; "N1" to "N23" below are the rows of its section 4.2). Four works get a place in Section 2: UniRAG (N1) and Freitas et al. (N2) as rows of Table 1; Xiang et al. (N3) and Freitas et al. as rows of Table 1b; VL-ICL Bench (N4) as one sentence. The sentence on what is specific to this study loses "text-only example captions".
- **Two corrections to the search file**, found when the four works were read again for this package. The search file is accepted as it stands and is not edited; this package carries the corrected text.
  1. Section 5.3 of the search file proposes "UniRAG reports the same direction on COCO for three multimodal models". That is wrong for one cell: for GPT-4o with one example the random pair scores higher than the retrieved pairs (block C-S01).
  2. Row N2 says "C: yes, equal k = 3" without saying that the random condition was run for one of the three model configurations only (blocks C-S04, C-S06).
- **Paper HEAD the OLD strings were checked against:** `55315ca` (`git show HEAD:`), and for `11_supplement_registered_rows.md` the text that package v2 as ruled produces (sha256 `5a71a8a0…`, the target of CC-408 Ruling 9), built in memory.
- **Five files change:**

| file | blocks | must be at (sha256) | why that state |
|---|---|---|---|
| `paper_v1_analysis/02_related_work.md` | 8 | `8dbc299bd816bb2fd9ec689b1ef1b97a1c2cab1e331232072dc4d7afee1a60fb` | HEAD `55315ca`; package v2 checks the file at this value and does not change it |
| `docs/TABLE1B_W5_EVIDENCE.md` | 4 | `11a291b36b7822f3d006ac2e25ac1c01f243f136beb37f46fb079326c4458ab2` | HEAD `55315ca`; an internal evidence file, not paper text |
| `paper_v1_analysis/paperC.bib` | 1 | `a415c4daa4d8c40b5b14432913d62bfefdcc30d7ff347df05637f332c23010e2` | HEAD `55315ca`; not read by the freeze shell or by package v2 |
| `paper_v1_analysis/paperC_bib_audit.tsv` | 1 | `a1af33399c668a31efa2f13b91b85983f6f1ea780e1ccda0b3aaabcb9adb3826` | HEAD `55315ca`; not read by either |
| `paper_v1_analysis/11_supplement_registered_rows.md` | 1 | `5a71a8a08085cdaabe385539208f008275aed18fabbd6c962cf0d0c5c44f0ff9` | the text AFTER package v2 (CC-408 Ruling 9); HEAD `55315ca` holds another text |

- **Order, binding.** Shell C2, then package v2 (CC-408), then this package. Package v2 checks `02_related_work.md` at `8dbc299b…`; this package changes that file, so it must not be written before the CC-408 commit. The apply script enforces this: its write mode refuses unless `11_supplement_registered_rows.md` at HEAD has the CC-408 target `5a71a8a0…`, whether or not block C-S15 is applied.
- **`paperC.bib` and the v2 gate.** Neither `apply_c_v2.py` nor `apply_c_v2_cc408.py` names `paperC.bib` or `paperC_bib_audit.tsv`. Their gate reads `paper_v1_analysis/*.md` and the manifest only (`check_pre`; write mode: `PD.glob('*.md')` and a `git status` on `paper_v1_analysis/*.md` and the manifest). The bibliography is therefore not pinned by v2; the order matters because of `02_related_work.md`, not because of the bibliography. `tex/paperC.bib` is a build copy made by `tex/build.sh` and is not touched here.
- **What it does not touch.** `01_introduction.md`, `03_method.md`, `05_preregistration_and_analysis.md`, `06_results.md`, `07_disclosures.md`, `number_manifest_C.tsv`, Sections 5.7 and 6.10, the abstract. No number of the paper changes. No manifest row is added or needed (section 5).
- **Block format** as in v1 to v3: the OLD string is the text between the `OLD>>>` line and the `NEW>>>` line, without the line break that ends it; the NEW string likewise, up to the `EVIDENCE>>>` line; an `END>>>` line closes the block. The file token is the path inside the paper repository. Block ids are `C-S01` … `C-S15`. In block C-S14 the fields of each row are separated by tab characters.
- **Apply script:** `manuscript/fix_packages/2026-11-15_C/apply_c_v4_search.py`. Default mode is a check that writes nothing. `--write --ruling <id>` writes the five files to the working tree only if every file is at the value of the table above and every result equals its target (section 6).
- **Sources.** Each cell and each sentence rests on the full text of the cited work, as far as the paper states. Versions read: UniRAG on the proceedings PDF of the ACL Anthology (sha256 `450d54d1cba4…`, pp. 2026–2039; PDF page n is proceedings page 2025 + n) and on arXiv v3; Freitas et al. on the CEUR-WS proceedings PDF (sha256 `adc23d6bcde1…`; the PDF pages carry no printed numbers, so "p. n" is the n-th PDF page of pp. 3518–3528); Xiang et al. on arXiv 2609.27682 v2 (sha256 `9348711ae2a6…`), because the Springer chapter is not open; VL-ICL Bench on arXiv 2403.13164 v4 (sha256 `d03a4c78f1fd…`), whose first page reads "Published as a conference paper at ICLR 2025".
- **Custody.** Public full texts of cited works, bibliographic records, and the paper's own Section 2, evidence file, bibliography and supplement paragraph on the literature search. No test-set score book, per-image ledger, caption file, label file or key file was opened. No dataset caption and no model output is printed. The bibliographic lookups are recorded in `manuscript/reviews/C_SYSTEMATIC_SEARCH_2026-11-15_records/bib_lookups/` (`lookups.tsv` and the raw responses).

## 1. Table of items

| id | task item | file | line | what | status |
|---|---|---|---|---|---|
| C-S01 | (b) | `paper_v1_analysis/02_related_work.md` | 20 | one sentence on UniRAG after the OpenFlamingo precedent, with the cell where random scored higher | BLOCK |
| C-S02 | (c), text citation | `paper_v1_analysis/02_related_work.md` | 20 | one sentence on VL-ICL Bench where the `rand` control is motivated | BLOCK (recommended as text, not as a row; section 3) |
| C-S03 | (c) | `paper_v1_analysis/02_related_work.md` | 45 | Table 1: new row, UniRAG | BLOCK |
| C-S04 | (c) | `paper_v1_analysis/02_related_work.md` | 47 | Table 1: new row, Freitas et al. | BLOCK |
| C-S05 | (c) | `paper_v1_analysis/02_related_work.md` | 60 | Table 1b: new row, Xiang et al. | BLOCK (recommended as a row; section 3) |
| C-S06 | (c) | `paper_v1_analysis/02_related_work.md` | 61 | Table 1b: new row, Freitas et al. | BLOCK (it is an analysis in the sense of the table; section 3) |
| C-S07 | (c) | `paper_v1_analysis/02_related_work.md` | 64 | "Position among the analyses": the three works are cited where the random control is said not to be new | BLOCK |
| C-S08 | (a) | `paper_v1_analysis/02_related_work.md` | 69 | what is specific to this study: "text-only example captions" goes; Freitas et al. is named as sharing it | BLOCK |
| C-S09 | (d) | `docs/TABLE1B_W5_EVIDENCE.md` | 3 | head paragraph: the rows added on 2026-11-15 and the versions read | BLOCK |
| C-S10 | (d) | `docs/TABLE1B_W5_EVIDENCE.md` | 43 | evidence rows for the two new rows of Table 1b | BLOCK |
| C-S11 | (d) | `docs/TABLE1B_W5_EVIDENCE.md` | 47 | evidence paragraphs for the two new rows of Table 1 and for the VL-ICL Bench sentence | BLOCK |
| C-S12 | (d) | `docs/TABLE1B_W5_EVIDENCE.md` | 49 | Outcome sentence: eight papers; "(or SD/SE/tests)" narrowed, because Xiang et al. report standard deviations | BLOCK |
| C-S13 | (e) | `paper_v1_analysis/paperC.bib` | end | four bibliography entries | BLOCK |
| C-S14 | (e) | `paper_v1_analysis/paperC_bib_audit.tsv` | end | four audit rows with the lookups | BLOCK |
| C-S15 | added by the package writer | `paper_v1_analysis/11_supplement_registered_rows.md` | 938 after v2 (927 at `55315ca`) | "Literature search (Section 2)": the sentence "OpenAlex and Semantic Scholar were not searched systematically" is no longer true | BLOCK (not in the task list; a judge may strike or defer it; targets for both cases are pinned) |
| – | – | `01_introduction.md` | 9 | the tested sentence | NOT CHANGED: it stands (section 3) |
| – | – | `number_manifest_C.tsv` | – | – | NOT CHANGED: no row needed (section 5) |
| – | N18 to N23 | – | – | six works not read | NO ROW, NO CLAIM: list for a manual read (section 3) |

Counts: 15 OLD/NEW blocks under 15 ids: 8 in the related-work file, 4 in the evidence file, 1 each in the bibliography, the bibliography audit table and the supplement. The package is one unit, with one exception: C-S15 can be left out. The apply script holds targets for the full package and for the package without C-S15; any other choice needs targets fixed by the ruling.

## 2. Blocks

### C-S01. UniRAG beside the OpenFlamingo precedent (task item b)

One sentence, placed after the sentence on the Flickr-30K reversal, because UniRAG holds a second case in which random examples score higher than retrieved ones. No score of UniRAG is printed, so no manifest row is needed; "Table 3" is the table number in the cited paper.

```text
<<<C-S01 paper_v1_analysis/02_related_work.md OLD>>>
The Flickr-30K reversal also shows that a model can score lower with retrieved than with random examples, as InternVL3 did on COCO (Section 8.2).
<<<C-S01 paper_v1_analysis/02_related_work.md NEW>>>
The Flickr-30K reversal also shows that a model can score lower with retrieved than with random examples, as InternVL3 did on COCO (Section 8.2). UniRAG [@Sharifymoghaddam2025UniRAG] makes the same comparison on COCO for three off-the-shelf multimodal models, with retrieved and random image-caption pairs at one and five examples: by CIDEr in its Table 3, the retrieved pairs score higher in five of the six model-by-shot cells, and for GPT-4o with one example the random pair scores higher.
<<<C-S01 EVIDENCE>>>
Source: Sharifymoghaddam, Upadhyay, Chen and Lin, Findings of NAACL 2025, proceedings PDF (https://aclanthology.org/2025.findings-naacl.108.pdf, sha256 450d54d1cba4…); the same passages are in arXiv 2405.10311 v3.
Models: p. 2027; quote: "we use a variety of off-the-shelf proprietary and open-source LVLM models" (LLaVA, GPT-4o and Gemini-Pro for captioning).
Random against retrieved, same number of examples: p. 2028; quote: "random selection of queries and their ground-truth candidates from the dataset (baseline 2)". Table 3 caption, p. 2031; quote: "Column k ∈ {0, 1, 5} shows the number of few-shot examples in each run".
The six cells, Table 3, p. 2031, CIDEr with one example / with five examples (two retrievers, then random): LLaVA 162.9 and 166.9 against 79.2 / 128.9 and 129.0 against 27.9; Gemini-Pro 83.3 and 83.4 against 79.4 / 96.4 and 94.4 against 92.4; GPT-4o 63.3 and 67.1 against 72.5 / 87.5 and 90.4 against 61.1. Retrieved is higher in five cells; in the sixth (GPT-4o, one example) random is higher, and its SPICE (18.7) equals the better retriever's.
The paper's own words on random examples: p. 2032; quote: "increasing the number of randomly selected examples to five degrades the generators' effectiveness".
The values were read on the page in layout mode in both versions (the plain text extraction interleaves the two shot rows).
<<<C-S01 END>>>
```

### C-S02. VL-ICL Bench: the style explanation has a published statement (task item c, as text)

VL-ICL Bench says for English captioning what this paper calls the style effect, and tests it by changing the metric, not by a random control. The sentence is placed after the one that gives the reason for the `rand` control. Section 3 gives the reason for a sentence and not a row, and a point for the investigator about the introduction.

```text
<<<C-S02 paper_v1_analysis/02_related_work.md OLD>>>
Both findings are why the `rand` control is needed: a gain that comes from the example text alone, and not from its match to the image, appears in `rand` as well as in `ret`.
<<<C-S02 paper_v1_analysis/02_related_work.md NEW>>>
Both findings are why the `rand` control is needed: a gain that comes from the example text alone, and not from its match to the image, appears in `rand` as well as in `ret`. VL-ICL Bench [@Zong2025VLICLBench] states the style side of this for English captioning: it conjectures that few-shot gains on COCO come largely from learning the data set's caption style, and reports that the gain almost disappears when a language model scores the captions in place of CIDEr.
<<<C-S02 EVIDENCE>>>
Source: Zong, Bohdal and Hospedales, ICLR 2025, read on arXiv 2403.13164 v4 (sha256 d03a4c78f1fd…).
Conjecture: Section 2.2, p. 3; quote: "We conjectured that this is largely due to the VLLM learning about each dataset's preferred answer style".
For captioning: p. 3; quote: "in captioning zero-shot VLLMs tend to produce more verbose captions than COCO ground-truth, and they learn to be more concise through ICL".
The test: p. 3; quotes: "we use GPT-3.5 to score the quality of the generated caption on a scale of score 1-10" and "the curves have almost fully flattened out". Figure 3 caption, p. 4; quote: "ICL on these benchmarks primarily learns answer style/format".
CIDEr is the standard metric of its COCO panel (Figure 3 (a), p. 4; Table 15, p. 30).
Not stated in the passages read: how the COCO examples are chosen. The sentence therefore does not say "random".
<<<C-S02 END>>>
```

### C-S03. Table 1: row for UniRAG (task item c)

```text
<<<C-S03 paper_v1_analysis/02_related_work.md OLD>>>
| @Baldassini2024MICL | no | yes | image-caption pairs | English | yes, equal shots | tests on the analyses, no CI on CIDEr |
<<<C-S03 paper_v1_analysis/02_related_work.md NEW>>>
| @Baldassini2024MICL | no | yes | image-caption pairs | English | yes, equal shots | tests on the analyses, no CI on CIDEr |
| UniRAG [@Sharifymoghaddam2025UniRAG] | no (off-the-shelf models; trained retrievers) | yes | image-caption pairs | English | yes, equal k | none |
<<<C-S03 EVIDENCE>>>
Source as for C-S01 (proceedings PDF, pp. 2026–2039).
Trained "no (off-the-shelf models; trained retrievers)": p. 2027, quote as in C-S01; the retrievers, p. 2027; quote: "CLIP Score Fusion and BLIP Feature Fusion models which are instruction-tuned".
Sees the image "yes": the generators are vision-language models that receive the query image (Section 3.2, p. 2028).
Retrieved content "image-caption pairs": Table 3 caption and Section 4.3, pp. 2030–2031 (retrieved pairs added as in-context examples).
Languages "English": p. 2034; quote: "This work uses the English-only MSCOCO and Fashion200k datasets for evaluation".
Random control "yes, equal k": p. 2028 and Table 3 rows 2c, 3c, 4c, p. 2031 (random selection at one and five examples).
Statistics "none": Table 3 and Table 4 give single values. "confidence interval": one hit, p. 2033, in the image-generation results. Standard deviations are given for the Inception Score of generated images only (Tables 5 and 6, p. 2032). No hit for "preregist", "seed", "±"; "bootstrap" only in a reference title.
<<<C-S03 END>>>
```

### C-S04. Table 1: row for Freitas et al. (task item c)

The random condition was run for one of the three model configurations (MedGemma 4B). The cell says so.

```text
<<<C-S04 paper_v1_analysis/02_related_work.md OLD>>>
| 9, no Vietnamese | yes, equal k = 3 | none (point scores) |
<<<C-S04 paper_v1_analysis/02_related_work.md NEW>>>
| 9, no Vietnamese | yes, equal k = 3 | none (point scores) |
| @Freitas2026RAGMedCap | no (a third model configuration is fine-tuned) | yes | captions, as text | English (ROCOv2, radiology) | yes, equal k (three captions), for one of its models | none (point scores) |
<<<C-S04 EVIDENCE>>>
Source: Freitas, Bosco, Lotufo, Pereira and Carmo, CLEF 2026 Working Notes, CEUR-WS Vol-4283, pp. 3518–3528 (https://ceur-ws.org/Vol-4283/paper255.pdf, sha256 adc23d6bcde1…).
Trained: Section 2.2, p. 2 (MedGemma 4B and Qwen3-VL 4B as released; a QLoRA fine-tuned MedGemma 1.5 4B, Section 2.4, p. 3).
Sees the image, and random control: p. 2; quote: "The random few-shot strategy injects three randomly selected captions from the training dataset before the query image".
Retrieved content "captions, as text": p. 2; quote: "injecting the captions of the three most visually similar training images into the prompt"; p. 3; quote: "The user turn contains the query image followed by the retrieved captions formatted as a numbered list".
"for one of its models": Table 1, p. 6, lists seven runs: MedGemma-OneShot, MedGemma-FewShot, MedGemma-RAG; MedGemma1.5-FT-Base, MedGemma1.5-FT-RAG; Qwen3-OneShot, Qwen3-RAG. The random few-shot run exists for MedGemma 4B only.
Result, validation set, Table 2, p. 6 (overall score): MedGemma-RAG 0.327, MedGemma-FewShot 0.305, MedGemma-OneShot 0.303; p. 7; quote: "suggesting that visually retrieved context provides more useful guidance than random demonstrations or no context at all".
Languages: the paper does not name the language ("English": no hit), so by the rule of the table caption the cell gives the language of the caption data. The data are ROCOv2 (Section 2.1, p. 2), and the data paper of ROCOv2 (arXiv 2405.10004 v2, p. 4) says: "1528 images with non-English captions were removed".
Statistics "none (point scores)": Tables 2 and 3 give one value per run and metric; no hit for "±", "std", "seed", "confidence", "bootstrap"; decoding uses a sampling temperature of 0.7 (p. 2) and the number of runs or of random draws is not stated. "registered": one hit, the team's registration on the task platform (abstract).
<<<C-S04 END>>>
```

### C-S05. Table 1b: row for Xiang et al. (task item c, recommended as a row)

```text
<<<C-S05 paper_v1_analysis/02_related_work.md OLD>>>
| OpenFlamingo-v2-9B, IDEFICS-9B | yes, equal shots | yes | no | no |
<<<C-S05 paper_v1_analysis/02_related_work.md NEW>>>
| OpenFlamingo-v2-9B, IDEFICS-9B | yes, equal shots | yes | no | no |
| @Xiang2026GenderBiasICL | whether the choice of in-context demonstrations shifts gender bias | English | a gender-annotated COCO subset, DCI | six open MLLMs, including Qwen3-VL-8B and InternVL3.5-8B | yes, equal shots (COCO subset: random against two similarity-based selections) | yes | no | no (mean ± SD over five random draws; similarity rows run once) |
<<<C-S05 EVIDENCE>>>
Source: Xiang, Nakashima and Garcia, ECCV 2026 (Springer chapter, doi 10.1007/978-3-032-37086-0_16, not open), read on arXiv 2609.27682 v2 (sha256 9348711ae2a6…, 58 pages).
Question: abstract and p. 2; quote: "Similarity-based retrieval methods inherit demographic imbalances from their source pool and offer no debiasing advantage over random selection".
Language "English": not named ("English": no hit); the cell gives the language of the caption data (MSCOCO and DCI).
Data: Section 3.3, p. 5; quotes: "which we refer to as COCOBias" (the gender-annotated subset of MSCOCO) and "yielding a subset of 371 images that is split into a training pool and a gender-balanced validation set" (DCI).
Models: Section 4, p. 7: Qwen-VL, Idefics3-8B-Llama3, Phi-3.5-vision-instruct, MiniCPM-o 2.6, InternVL3.5-8B, Qwen3-VL-8B-Instruct.
Equal-k random control: Section 3.2, pp. 3–4 (Random Sample; similarity-based image-image and image-text retrieval); p. 8; quote: "SIIR and SITR are applied only to COCOBias"; shots k ∈ {0, 2, 4, 6, 8} (p. 8). Caption quality (BLEU-4, CLIPScore) is reported for the random and for the similarity settings at the same shots: Table 3, p. 12 (one model), Tables 8 to 13, pp. 29–32 (one table per model).
Per-backbone rows "yes": Tables 8 to 13 (COCO subset) and 26 to 31 (DCI), one table per model.
Registered "no": no hit for "preregist", "pre-regist", "registered".
CIs "no (mean ± SD over five random draws; similarity rows run once)": p. 8; quotes: "we run each experiment five times using independently sampled in-context sequences" and "each setting is conducted only once"; p. 10; quote: "within one standard deviation of RS"; BLEU and CLIPScore as mean ± value in the sampled settings of Tables 8 to 13 and 26 to 31. No hit for "confidence" or "bootstrap".
The paper's statement on caption scores: p. 2; quote: "Standard caption quality metrics remain stable even as gender bias shifts substantially".
<<<C-S05 END>>>
```

### C-S06. Table 1b: row for Freitas et al. (task item c)

```text
<<<C-S06 paper_v1_analysis/02_related_work.md OLD>>>
| yes, k = 3, examples with image and article excerpt | yes | no | no |
<<<C-S06 paper_v1_analysis/02_related_work.md NEW>>>
| yes, k = 3, examples with image and article excerpt | yes | no | no |
| @Freitas2026RAGMedCap (a shared-task working note; the comparison is its captioning experiment) | whether retrieved captions in the prompt improve radiology captioning over a single instruction and over random captions | English | ROCOv2 (radiology) | MedGemma 4B; Qwen3-VL 4B (no random condition); a fine-tuned MedGemma variant | yes, three captions each, as text, for MedGemma 4B only | yes | no | no (point scores) |
<<<C-S06 EVIDENCE>>>
Source as for C-S04.
It is an analysis in the sense of Table 1b: the abstract, p. 1, states the question; quote: "we investigate whether Retrieval-Augmented Generation (RAG) with similar cases improves Visual Language Model (VLM) based captioning quality compared to one-shot prompting strategies". What the paper calls one-shot is the image with a single instruction and no example (Section 2.2, p. 2).
Language, data, models, random control: as in C-S04 (Sections 2.1 and 2.2, p. 2; Table 1, p. 6). Qwen3-VL 4B has the one-shot and the retrieval run only; the fine-tuned MedGemma 1.5 4B has a base run and a run fine-tuned with retrieved captions.
Per-backbone rows "yes": Table 2, p. 6, one row per run.
Registered "no" and CIs "no (point scores)": as in C-S04.
A detail not used in the row: the system prompt tells the model not to copy the retrieved captions (p. 3; quote: "explicitly prohibits copying them").
<<<C-S06 END>>>
```

### C-S07. "Position among the analyses": the three works where the random control is said not to be new (task item c)

```text
<<<C-S07 paper_v1_analysis/02_related_work.md OLD>>>
[@Awadalla2023OpenFlamingo; @Yang2023ICLConfig; @Li2025UnveilingICL], and in nine languages for news image captioning [@Chen2026MUNIChus].
<<<C-S07 paper_v1_analysis/02_related_work.md NEW>>>
[@Awadalla2023OpenFlamingo; @Yang2023ICLConfig; @Li2025UnveilingICL; @Sharifymoghaddam2025UniRAG; @Xiang2026GenderBiasICL], in nine languages for news image captioning [@Chen2026MUNIChus], and with example captions shown as text for radiology images [@Freitas2026RAGMedCap].
<<<C-S07 EVIDENCE>>>
The sentence says that studies of in-context selection compare similarity-based with random examples, "mostly in English and with interleaved images". UniRAG (C-S01, C-S03) and Xiang et al. (C-S05) are such studies, in English and with example images. Freitas et al. (C-S04, C-S06) make the comparison with captions as text and no example image, so they are named apart.
<<<C-S07 END>>>
```

### C-S08. What is specific to this study (task item a)

```text
<<<C-S08 paper_v1_analysis/02_related_work.md OLD>>>
What remains specific to this study is the Vietnamese setting, text-only example captions, per-backbone intervals and a registered one-look test.
<<<C-S08 paper_v1_analysis/02_related_work.md NEW>>>
A working note from a shared task on radiology captioning [@Freitas2026RAGMedCap] is close in prompt design: it gives MedGemma 4B, which sees the query image, three retrieved or three random captions as text, and reports point scores. What remains specific to this study is the Vietnamese setting, per-backbone intervals and a registered one-look test; text-only example captions it shares with that note.
<<<C-S08 EVIDENCE>>>
Evidence as in C-S04 (p. 2 and p. 3 for captions as text with the query image; Table 1, p. 6, for the one model with a random run; Tables 2 and 3 for point scores).
What stays unchanged and true: the list of five differences "from both" closest studies (l.12 to l.16), since neither of those two studies shows captions as text only; the item "text-only example captions" in point 1 of "Position among the analyses" (l.65), which describes the setting and claims no priority; the last sentence of l.69 ("We make no priority claim …").
<<<C-S08 END>>>
```

### C-S09. Evidence file, head paragraph: the rows added from the search (task item d)

```text
<<<C-S09 docs/TABLE1B_W5_EVIDENCE.md OLD>>>
After that re-check no cell of Table 1b holds "–". Record: manuscript/reviews/RELATED_FULLTEXT_CHECK_2026-11-15.md in the run repository.
<<<C-S09 docs/TABLE1B_W5_EVIDENCE.md NEW>>>
After that re-check no cell of Table 1b holds "–". Record: manuscript/reviews/RELATED_FULLTEXT_CHECK_2026-11-15.md in the run repository. On 2026-11-15 two rows were added to Table 1b (Xiang2026GenderBiasICL, Freitas2026RAGMedCap) and two to Table 1 (Sharifymoghaddam2025UniRAG, Freitas2026RAGMedCap) from a dated search (record: manuscript/reviews/C_SYSTEMATIC_SEARCH_2026-11-15.md in the run repository). Versions read: Xiang2026GenderBiasICL on arXiv 2609.27682 v2, because the Springer chapter is not open; Freitas2026RAGMedCap on the CEUR-WS proceedings PDF, whose pages carry no printed numbers ("p. n" is the n-th PDF page); Sharifymoghaddam2025UniRAG on the proceedings PDF of the ACL Anthology. Six further works that passed the abstract screen of that search were not read and have no row.
<<<C-S09 EVIDENCE>>>
States what was done and on which versions; the six unread works are listed in section 3 of this package and in section 4.2 of the search file (N18 to N23).
<<<C-S09 END>>>
```

### C-S10. Evidence file: rows for the two new rows of Table 1b (task item d)

```text
<<<C-S10 docs/TABLE1B_W5_EVIDENCE.md OLD>>>
the number of random draws is not stated |
<<<C-S10 docs/TABLE1B_W5_EVIDENCE.md NEW>>>
the number of random draws is not stated |
| Xiang2026GenderBiasICL (ECCV 2026, Springer chapter not open; checked on arXiv 2609.27682 v2) | language(s) | English | "English": no hit; the cell gives the language of the caption data (MSCOCO and DCI, §3.3, p. 5) |
| | data | a gender-annotated COCO subset, DCI | §3.3, p. 5 ("which we refer to as COCOBias"; DCI: "yielding a subset of 371 images that is split into a training pool and a gender-balanced validation set") |
| | models | six open MLLMs, including Qwen3-VL-8B and InternVL3.5-8B | §4, p. 7 (Qwen-VL, Idefics3-8B-Llama3, Phi-3.5-vision-instruct, MiniCPM-o 2.6, InternVL3.5-8B, Qwen3-VL-8B-Instruct) |
| | equal-k random control | yes, equal shots (COCO subset: random against two similarity-based selections) | §3.2, pp. 3–4 (Random Sample; SIIR; SITR); p. 8 ("SIIR and SITR are applied only to COCOBias"; k ∈ {0, 2, 4, 6, 8}); BLEU-4 and CLIPScore for all settings in Table 3, p. 12, and Tables 8 to 13, pp. 29–32 |
| | per-backbone rows | yes | Tables 8 to 13 (COCO subset) and 26 to 31 (DCI), one table per model |
| | registered, one look | no | full-text search: no hit |
| | CIs | no (mean ± SD over five random draws; similarity rows run once) | p. 8 ("we run each experiment five times using independently sampled in-context sequences"; "each setting is conducted only once"); p. 10 ("within one standard deviation of RS"); mean ± value on BLEU and CLIPScore in the sampled settings of Tables 8 to 13 and 26 to 31; no hit for "confidence", "bootstrap" |
| Freitas2026RAGMedCap (CLEF 2026 Working Notes, CEUR-WS Vol-4283, pp. 3518–3528; "p. n" is the n-th PDF page) | language(s) | English | "English": no hit; the cell gives the language of the caption data, ROCOv2 (§2.1, p. 2), whose data paper (arXiv 2405.10004 v2, p. 4) says "1528 images with non-English captions were removed" |
| | data | ROCOv2 (radiology) | §2.1, p. 2 ("ROCOv2 consists of curated radiology images sourced from biomedical articles of the PMC OpenAccess subset"); the comparison is on the validation set (Table 2, p. 6) |
| | models | MedGemma 4B; Qwen3-VL 4B (no random condition); a fine-tuned MedGemma variant | §2.2, p. 2; Table 1, p. 6 (seven runs; the fine-tuned model is MedGemma 1.5 4B, §2.4, p. 3) |
| | equal-k random control | yes, three captions each, as text, for MedGemma 4B only | §2.2, p. 2 ("The random few-shot strategy injects three randomly selected captions from the training dataset before the query image"; "injecting the captions of the three most visually similar training images into the prompt"); Table 1, p. 6: a random few-shot run for MedGemma 4B only |
| | per-backbone rows | yes | Table 2, p. 6, one row per run |
| | registered, one look | no | "registered": one hit, the team's registration on the task platform (abstract) |
| | CIs | no (point scores) | Tables 2 and 3, pp. 6 and 8: one value per run and metric; no hit for "±", "std", "seed", "confidence", "bootstrap"; sampling temperature 0.7 (p. 2), number of runs not stated |
<<<C-S10 EVIDENCE>>>
The rows repeat, in the format of this file, the evidence of C-S05 and C-S06; every quoted string was matched by script against the text extracted from the PDF named in the row.
<<<C-S10 END>>>
```

### C-S11. Evidence file: paragraphs for the two new rows of Table 1 and for the VL-ICL Bench sentence (task item d)

```text
<<<C-S11 docs/TABLE1B_W5_EVIDENCE.md OLD>>>
Tables 2 to 5 give single values.
<<<C-S11 docs/TABLE1B_W5_EVIDENCE.md NEW>>>
Tables 2 to 5 give single values.

**Table 1, UniRAG row, and the sentence on UniRAG in Section 2 (Sharifymoghaddam2025UniRAG; Findings of NAACL 2025, proceedings PDF, pp. 2026–2039, checked 2026-11-15; same passages in arXiv 2405.10311 v3).** Trained "no (off-the-shelf models; trained retrievers)": p. 2027 ("we use a variety of off-the-shelf proprietary and open-source LVLM models"; the retrievers are "instruction-tuned"). Languages "English": p. 2034 ("This work uses the English-only MSCOCO and Fashion200k datasets for evaluation"). Random control "yes, equal k": p. 2028 ("random selection of queries and their ground-truth candidates from the dataset (baseline 2)"); Table 3, p. 2031, rows 2c, 3c and 4c at one and five examples. Statistics "none": Tables 3 and 4 give single values; the one hit for "confidence interval" (p. 2033) and the standard deviations of Tables 5 and 6 concern generated images. The sentence in Section 2, CIDEr in Table 3 with one example / with five examples (two retrievers, then random): LLaVA 162.9 and 166.9 against 79.2 / 128.9 and 129.0 against 27.9; Gemini-Pro 83.3 and 83.4 against 79.4 / 96.4 and 94.4 against 92.4; GPT-4o 63.3 and 67.1 against 72.5 / 87.5 and 90.4 against 61.1. Retrieved is higher in five of the six cells; for GPT-4o with one example random is higher.

**Table 1, Freitas2026RAGMedCap row (CEUR-WS Vol-4283, pp. 3518–3528, checked 2026-11-15; "p. n" is the n-th PDF page).** Trained "no (a third model configuration is fine-tuned)": §2.2, p. 2, and §2.4, p. 3. Sees the image "yes" and retrieved content "captions, as text": p. 3 ("The user turn contains the query image followed by the retrieved captions formatted as a numbered list"). Random control "yes, equal k (three captions), for one of its models": Table 1, p. 6 (MedGemma-OneShot, MedGemma-FewShot, MedGemma-RAG; no random run for the other two configurations); validation overall score 0.327 with retrieved, 0.305 with random and 0.303 with no captions (Table 2, p. 6). Languages and statistics: as in the rows for Table 1b above.

**Sentence on VL-ICL Bench in Section 2 (Zong2025VLICLBench; ICLR 2025, checked on arXiv 2403.13164 v4, 2026-11-15).** §2.2, p. 3 ("We conjectured that this is largely due to the VLLM learning about each dataset's preferred answer style"; "the curves have almost fully flattened out" under scoring by a language model); Figure 3 caption, p. 4 ("ICL on these benchmarks primarily learns answer style/format"). The work has no row in Table 1b: its COCO check (Table 15, p. 30; mean of three seeds, p. 7) compares shot counts and has no selection comparison for captioning; similarity-based selection is tested on three other tasks (pp. 25–27). No hit for "preregist", "confidence", "bootstrap".
<<<C-S11 EVIDENCE>>>
The paragraphs repeat, in the format of this file, the evidence of C-S01 to C-S04. Table 3 of UniRAG was read on the page in layout mode.
<<<C-S11 END>>>
```

### C-S12. Evidence file: the Outcome sentence (task item d)

"(or SD/SE/tests)" was true of the six papers. It is not true of Xiang et al., who report standard deviations on BLEU-4 and CLIPScore. The paper's own sentence says "confidence intervals" and is not affected.

```text
<<<C-S12 docs/TABLE1B_W5_EVIDENCE.md OLD>>>
**Outcome.** None of the six papers of Table 1b (the five analysis papers and the MUNIChus benchmark paper) preregisters its contrasts or reports CIs (or SD/SE/tests) on the captioning score, so the sentence in Section 1 scoped to these papers holds and the CC-212 falsifier is not triggered.
<<<C-S12 docs/TABLE1B_W5_EVIDENCE.md NEW>>>
**Outcome.** None of the eight papers of Table 1b (the five analysis papers, the MUNIChus benchmark paper, Xiang et al. and the working note of Freitas et al.) preregisters its contrasts or reports CIs on the captioning score. Seven of them report no SD, SE or test on it either; Xiang et al. report mean ± SD over five random draws on BLEU-4 and CLIPScore. The sentence in Section 1 names the first six; it holds for them and for the two added rows, so the CC-212 falsifier is not triggered.
<<<C-S12 EVIDENCE>>>
Xiang et al.: C-S05 (p. 8 and Tables 8 to 13, 26 to 31). Freitas et al.: C-S04 (no hit for "±", "std", "seed", "confidence", "bootstrap"). The six earlier papers: the rows of this file, unchanged.
<<<C-S12 END>>>
```

### C-S13. Bibliography: four entries (task item e)

Appended after the last entry of `paperC.bib`. Field layout as in the file.

```text
<<<C-S13 paper_v1_analysis/paperC.bib OLD>>>
  doi       = {10.1007/BF01068419}
}
<<<C-S13 paper_v1_analysis/paperC.bib NEW>>>
  doi       = {10.1007/BF01068419}
}

@inproceedings{Sharifymoghaddam2025UniRAG,
  author    = {Sharifymoghaddam, Sahel and Upadhyay, Shivani and Chen, Wenhu and Lin, Jimmy},
  title     = {{UniRAG}: Universal Retrieval Augmentation for Large Vision Language Models},
  booktitle = {Findings of the Association for Computational Linguistics: NAACL 2025},
  year      = {2025},
  pages     = {2026--2039},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2025.findings-naacl.108}
}

@inproceedings{Freitas2026RAGMedCap,
  author    = {Freitas, Gabriel and Bosco, Maria and Lotufo, Roberto and Pereira, Jayr and Carmo, Diedre},
  title     = {Retrieval Augmented Generation and Patch-Level Explainability applied to Medical Image Captioning with Small Visual Language Models},
  booktitle = {Working Notes of the Conference and Labs of the Evaluation Forum (CLEF 2026)},
  series    = {CEUR Workshop Proceedings},
  volume    = {4283},
  year      = {2026},
  pages     = {3518--3528},
  publisher = {CEUR-WS.org},
  url       = {https://ceur-ws.org/Vol-4283/paper255.pdf}
}

@inproceedings{Xiang2026GenderBiasICL,
  author    = {Xiang, Tong and Nakashima, Yuta and Garcia, Noa},
  title     = {Gender Bias in Vision-Language In-Context Learning},
  booktitle = {Computer Vision -- ECCV 2026},
  series    = {Lecture Notes in Computer Science},
  year      = {2026},
  pages     = {287--307},
  publisher = {Springer Nature Switzerland},
  doi       = {10.1007/978-3-032-37086-0_16},
  note      = {arXiv:2609.27682}
}

@inproceedings{Zong2025VLICLBench,
  author    = {Zong, Yongshuo and Bohdal, Ondrej and Hospedales, Timothy},
  title     = {{VL-ICL Bench}: The Devil in the Details of Multimodal In-Context Learning},
  booktitle = {International Conference on Learning Representations (ICLR 2025)},
  year      = {2025},
  url       = {https://openreview.net/forum?id=cpGPPLLYYx},
  note      = {arXiv:2403.13164}
}
<<<C-S13 EVIDENCE>>>
Lookups of 2026-11-15, 03:03 to 03:06 UTC; raw responses and the request list (`lookups.tsv`) are in `manuscript/reviews/C_SYSTEMATIC_SEARCH_2026-11-15_records/bib_lookups/`.
Sharifymoghaddam2025UniRAG: Crossref `api.crossref.org/works/10.18653/v1/2025.findings-naacl.108` (HTTP 200): proceedings article, title as entered, container "Findings of the Association for Computational Linguistics: NAACL 2025", pages 2026-2039, four authors in this order. The page footer of the PDF gives the same pages. arXiv API, id 2405.10311: v3, same title and authors.
Freitas2026RAGMedCap: volume index `https://ceur-ws.org/Vol-4283/` (HTTP 200): title as entered, the five authors in this order, pages 3518-3528; volume "Working Notes of the Conference and Labs of the Evaluation Forum (CLEF 2026)", Jena, Germany, 21-24 September 2026, published 2026-10-04. The work has no DOI. The first page of the PDF gives the same title and authors.
Xiang2026GenderBiasICL: Crossref `api.crossref.org/works/10.1007/978-3-032-37086-0_16` (HTTP 200): book chapter, title as entered, containers "Lecture Notes in Computer Science" and "Computer Vision – ECCV 2026", pages 287-307, publisher Springer Nature Switzerland, three authors in this order, first online 5 October 2026. The record gives no volume number, so the entry has none. arXiv API, id 2609.27682: v2, same title and authors, comment "ECCV 2026". The chapter was not read; the note field names the version that was.
Zong2025VLICLBench: arXiv API, id 2403.13164: v4, title and three authors as entered, comment "ICLR 2025". OpenReview `api2.openreview.net/notes/search?term=VL-ICL%20Bench` (HTTP 200): forum cpGPPLLYYx, venue "ICLR 2025 Poster", same title and authors. A first request with a wrong parameter name got HTTP 400. dblp.org answered with a bot-check page; it was left alone and the page was not kept. The record gives no pages, so the entry has none.
Key style as in the file (first author, year of the version cited, short name).
<<<C-S13 END>>>
```

### C-S14. Bibliography audit table: four rows (task item e)

Appended after the last row. Fields are separated by tab characters.

```text
<<<C-S14 paper_v1_analysis/paperC_bib_audit.tsv OLD>>>
JSTOR stable page did not load and Crossref api/works/10.2307/4615733 returned 404)
<<<C-S14 paper_v1_analysis/paperC_bib_audit.tsv NEW>>>
JSTOR stable page did not load and Crossref api/works/10.2307/4615733 returned 404)
Sharifymoghaddam2025UniRAG	doi:10.18653/v1/2025.findings-naacl.108	https://api.crossref.org/works/10.18653/v1/2025.findings-naacl.108 ; https://export.arxiv.org/api/query?id_list=2405.10311	200	OK (2026-11-15; Crossref: Findings of NAACL 2025, pp. 2026-2039, four authors; arXiv 2405.10311 v3 has the same title and authors; cells read on the anthology PDF)
Freitas2026RAGMedCap	url:https://ceur-ws.org/Vol-4283/paper255.pdf	https://ceur-ws.org/Vol-4283/	200	OK (2026-11-15; volume index: title, five authors, pp. 3518-3528; CLEF 2026 Working Notes, Jena, 21-24 September 2026, published 2026-10-04; no DOI)
Xiang2026GenderBiasICL	doi:10.1007/978-3-032-37086-0_16	https://api.crossref.org/works/10.1007/978-3-032-37086-0_16 ; https://export.arxiv.org/api/query?id_list=2609.27682	200	OK (2026-11-15; Crossref: book chapter, Computer Vision - ECCV 2026, LNCS, pp. 287-307, no volume number in the record; arXiv 2609.27682 v2 has the same title and authors, comment "ECCV 2026"; cells read on arXiv v2, the Springer chapter is not open)
Zong2025VLICLBench	arXiv:2403.13164	https://export.arxiv.org/api/query?id_list=2403.13164 ; https://api2.openreview.net/notes/search?term=VL-ICL%20Bench	200	OK (2026-11-15; arXiv v4, comment "ICLR 2025"; OpenReview forum cpGPPLLYYx, venue "ICLR 2025 Poster", same title and three authors; dblp.org answered with a bot-check page and was left alone)
<<<C-S14 EVIDENCE>>>
Columns as in the file: key, id, url_checked, http, status. The four statuses repeat the lookups of C-S13. The arXiv lookup was one request for the three ids (`id_list=2405.10311,2609.27682,2403.13164`); each row names its own id.
<<<C-S14 END>>>
```

### C-S15. Supplement, "Literature search (Section 2)" (added by the package writer; a judge may strike or defer it)

After this package the supplement would still say that OpenAlex and Semantic Scholar were not searched systematically, in the commit that adds four works found by such a search. The block replaces that clause. It keeps the opening "Our searches were partial", which is still true: the search retrieved three of the six analyses that Table 1b held, and six works that passed its abstract screen were not read. The works are named in words, so the supplement's reference list does not change. The numbers are written as words; the only digits are the date.

```text
<<<C-S15 paper_v1_analysis/11_supplement_registered_rows.md OLD>>>
2026-11-09; OpenAlex and Semantic Scholar were not searched systematically.
<<<C-S15 paper_v1_analysis/11_supplement_registered_rows.md NEW>>>
2026-11-09. On 2026-11-15 OpenAlex, arXiv and Semantic Scholar were searched by title and abstract under a protocol written before the first query. That search added four works to Section 2 (UniRAG, the working note of Freitas et al., Xiang et al. and VL-ICL Bench). It retrieved only three of the six analyses that Table 1b held at the time, and six works that passed its abstract screen could not be read, so it does not show that no further study exists.
<<<C-S15 EVIDENCE>>>
Search file, section 2.1 (the three indexes, the query strings, the times), section 1 (protocol, frozen before the first query; sha256 of its bytes 258617e9…), section 4.1 (three of the six analyses of Table 1b retrieved), section 4.2 (N18 to N23 not read).
OLD was checked on the text that package v2 as ruled produces for this file (sha256 5a71a8a0…, l.938); the same string is at l.927 of the file at `55315ca`. Package v2 does not change this paragraph.
`02_related_work.md` l.22 ("Our literature search was partial (details in the supplement, "Disclosure detail").") is unchanged and still true.
<<<C-S15 END>>>
```

## 3. Recommendations, what is not changed, and the list for a manual read

**Xiang et al.: a row of Table 1b (recommended), not only a citation.** Reasons: (1) it has the comparison that Table 1b is about, similar against random demonstrations at equal shots for captioning, on six current models, two of them from the model families of this study; (2) it is the one analysis found that reports a dispersion measure on a caption score, which bears on the sentence "none … reports confidence intervals on the captioning score". Showing the cell "no (mean ± SD over five random draws …)" in the table is more open than leaving the work to a citation. The cost: its outcome is gender bias, not caption quality, which the "question" cell says. If a judge prefers a citation only, C-S05, the Xiang rows of C-S10 and C-S12 go, the key stays in C-S07, and the ruling must fix the targets.

**VL-ICL Bench: a sentence (recommended), not a row.** Reasons: (1) its captioning check varies the number of examples and has no selection comparison, so every design cell of a row would read "no"; (2) what matters for this paper is its statement that few-shot gains in captioning are largely style learning, which is the alternative explanation this paper tests, and a statement belongs in the text where the `rand` control is motivated. Table 1b already has one row of this kind (Chen2025TrueMICL, "no for captioning"); a second would add length and no comparison.

**Freitas et al.: a row of Table 1b as well as of Table 1.** Its captioning experiment is the question of Table 1b (retrieved against random captions against none), stated in its abstract. It is a shared-task working note with one model in the random comparison and point scores, and the row label and cells say so.

**For the investigator: the introduction.** `01_introduction.md` l.9 presents "in-domain style" as one of two possible sources of the gain. VL-ICL Bench states the style explanation for English captioning (C-S02). After this package Section 2 cites it; the introduction does not. `01_introduction.md` is in the file list of package v2, so no block is proposed here. A possible clause after "… how the data set's captions are written)": "an explanation already proposed for English few-shot captioning [@Zong2025VLICLBench]".

**Not changed.**
- The tested sentence (`01_introduction.md` l.9): it stands. It names six papers; the two added rows of Table 1b also have no registration and no confidence interval (C-S12).
- `02_related_work.md` l.5: the list of analysis papers by citation is left as it is. Xiang et al. ask about bias, not about why examples help, and Freitas et al. is a working note; both are in Table 1b with labels that say what they are.
- `02_related_work.md` l.11 to l.16 ("Two studies are closest … five ways"): unchanged; C-S08 names Freitas et al. where the closest studies are summed up.
- Optional works of the search file (PAELLA as a Table 1 row; Lever-LM, RAVENEA, the benchmark of Liu et al., RA-CoA, the UFPE-Essex-UNED note as citations): not in this package. None of them bears on a claim of the paper.

**Deferred.**
- The clause for the introduction above (needs a package on `01_introduction.md` after v2).
- The search file itself is not corrected (section 0, two points). If a correction note is wanted there, it can be appended; the file's present bytes would stay as a prefix.
- Nothing is deferred for the manifest (section 5).

**List for a manual read (no row and no claim in this package).**

| # in the search file | work | where | what to settle |
|---|---|---|---|
| N18 | Why is a Bird's Caption a Good Demonstration? Towards Effective Multimodal In-Context Learning without Dedicated Data. ACM Multimedia 2025, doi 10.1145/3746027.3755653 | ACM Digital Library | first to read: an analysis over 17 data sets and five models; does it compare selection conditions for captioning, with which statistics |
| N19 | Advancing Multimodal Large Language Models: Optimizing Prompt Engineering Strategies for Enhanced Performance. Applied Sciences 2025, doi 10.3390/app15073992 | journal site (open access; answered HTTP 403 to an automated request) | whether its in-context and retrieval conditions have a random control on a captioning set |
| N20 | Strategic Application of Prompt Engineering in Multi-Modal Large Language Models. IEEE ICCE 2025, doi 10.1109/icce63647.2025.10930109 | IEEE Xplore | how the in-context examples are chosen on Flickr30k, NoCaps and MSCOCO |
| N21 | Beyond Similarity: Aligning Retrieval with Generation for Enhanced Image Captioning. IJCNN 2025, doi 10.1109/ijcnn64981.2025.11227734 | IEEE Xplore | the observation that highly similar retrieved results do not always help: with which control |
| N22 | Evaluating generative AI for medical image captioning: a benchmark study on radiology images. SPIE Medical Imaging 2026, doi 10.1117/12.3084497 | SPIE Digital Library | how the few-shot examples are chosen on ROCOv2; any interval |
| N23 | Relational reasoning image captioning via multi-agent retrieval-augmented generation. Knowledge-Based Systems 2025, doi 10.1016/j.knosys.2025.114977 | ScienceDirect | whether it is training-free and has a control (no abstract in any index) |

Also still open from package v3: RAGCap, the TPAMI version of Li et al., and the version of record of Sarto et al.

## 4. For the conference draft

Not applied; `draft_v2/paper.md` was read only (sha256 `7a3b8bb35cb4f92c927725c8088f306e14511c48b22a43583dc568532ba5e0fb`, last changed 2026-11-15 08:36 Vietnam time). The blocks are keyed by paragraph id; OLD is the text of draft_v2 at that sha. The four keys resolve once C-S13 is in `paperC.bib`, which the conference build reads. Added running words are given, because the draft is over its length.

**`p:S2-02` (optional, no running word).**

```text
OLD: mostly in English and with example images [@Yang2023ICLConfig; @Li2025UnveilingICL].
NEW: mostly in English and with example images [@Yang2023ICLConfig; @Li2025UnveilingICL; @Sharifymoghaddam2025UniRAG; @Xiang2026GenderBiasICL].
```

**`p:S2-03`, the English precedent (+17 words, the citation not counted).** Evidence: C-S01.

```text
OLD: OpenFlamingo reports that retrieved image-caption examples beat random ones on COCO, and that on Flickr30K they scored lower at the smaller shot counts it reports [@Awadalla2023OpenFlamingo].
NEW: OpenFlamingo reports that retrieved image-caption examples beat random ones on COCO, and that on Flickr30K they scored lower at the smaller shot counts it reports [@Awadalla2023OpenFlamingo]. UniRAG reports the same on COCO for three models, except for one model with a single example [@Sharifymoghaddam2025UniRAG].
```

**`p:S2-05`, what differs here (+21 words).** Evidence: C-S04, C-S08. The list keeps "example captions shown as text only" as a property of this study; the added sentence says who shares it.

```text
OLD: and a preregistered test with one look per set. No priority claim
NEW: and a preregistered test with one look per set. One working note on radiology captioning also shows retrieved or random captions as text, for one model and with point scores [@Freitas2026RAGMedCap]. No priority claim
```

**`p:T1`, Table 1: two rows, placed after the row of `@Chen2026MUNIChus` (table cells, not running text).** Evidence: C-S05, C-S06.

```text
| Xiang et al. [@Xiang2026GenderBiasICL] | English | image-caption pairs | yes, equal shots | no; no |
| Freitas et al. [@Freitas2026RAGMedCap] | English (radiology) | captions, as text | yes, equal k, one model | no; no |
```

**`p:S1-02`:** no change; the sentence stands for the rows of Table 1 with the two added rows.

The style statement of VL-ICL Bench (C-S02) is not proposed for the conference draft, for length; `p:S2-02` could take the key if the reviser has room: "… driven mainly by the text of the examples [@Baldassini2024MICL; @Chen2025TrueMICL], and few-shot gains in captioning have been attributed to style learning [@Zong2025VLICLBench]" (+11 words).

## 5. After application

- `tex/body.tex`, `tex/supp_body.tex`, `tex/paperC.bib` and the PDFs are derived files; they are rebuilt by `tex/build.sh`, not by this package.
- Four citation keys are added: `Sharifymoghaddam2025UniRAG`, `Freitas2026RAGMedCap`, `Xiang2026GenderBiasICL`, `Zong2025VLICLBench`. Each is cited in `02_related_work.md` and defined in `paperC.bib` by C-S13. No key is removed.
- **No manifest row is needed, and none is written.** The new text of `02_related_work.md` prints no score and no count of a cited work in digits: the example counts are written as words ("three captions", "one and five examples", "five random draws"). Its new number tokens, by the token rule of `c_pass2_check.py`, are the table number "3" (UniRAG's Table 3), "4" five times ("GPT-4o" once and the model name "4B" four times) and "8" twice (the model names "8B"); each is already a `number` of the manifest, so the review list of that check does not grow. The new text of the supplement adds the date 2026-11-15, written like the other dates of that paragraph, and the cross-references "Section 2" and "Table 1b". The step that would append manifest rows after checking for the two rows of the freeze shell is therefore not part of the apply script.
- Words of `02_related_work.md` (comments stripped, whitespace split, tables included): 2,950 at `55315ca`, 3,286 after the package (+336). The cut plan for Paper C should count this.

## 6. Checks run

Method: the apply script in its default mode (nothing written). For `11_supplement_registered_rows.md` the script builds the text after package v2 in memory with the functions of `apply_c_v2_cc408.py` (its check mode: the after-C2 tree from `git show 9b8e6ae:`, then package v2 as ruled), asserts that the result has the CC-408 target `5a71a8a0…`, and checks C-S15 on that text. Nothing was written to the paper repository.

| id | file | count of OLD in the base text | count at its turn, package order | exactly once |
|---|---|---|---|---|
| C-S01 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-S02 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-S03 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-S04 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-S05 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-S06 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-S07 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-S08 | `paper_v1_analysis/02_related_work.md` | 1 | 1 | yes |
| C-S09 | `docs/TABLE1B_W5_EVIDENCE.md` | 1 | 1 | yes |
| C-S10 | `docs/TABLE1B_W5_EVIDENCE.md` | 1 | 1 | yes |
| C-S11 | `docs/TABLE1B_W5_EVIDENCE.md` | 1 | 1 | yes |
| C-S12 | `docs/TABLE1B_W5_EVIDENCE.md` | 1 | 1 | yes |
| C-S13 | `paper_v1_analysis/paperC.bib` | 1 | 1 | yes |
| C-S14 | `paper_v1_analysis/paperC_bib_audit.tsv` | 1 | 1 | yes |
| C-S15 | `paper_v1_analysis/11_supplement_registered_rows.md` (text after v2) | 1 | 1 | yes |

Further checks, all passed:
- Paper HEAD at the time of the checks: `55315ca`; the four files that are checked at HEAD are clean against HEAD and have the values of section 0.
- 15 blocks under 15 ids; every NEW occurs exactly once after all blocks; applying the blocks in the reverse order gives byte-equal files; no two OLD spans overlap.
- Table 1 after the package: 19 rows (17 before), each with 7 cells; the RAGCap row is byte-unchanged and is the only row with a "–" cell. Table 1b: 9 rows (7 before), each with 9 cells; no cell is "–". The row for this study is the last row of each table.
- The four new keys: each is cited in `02_related_work.md` and defined exactly once in `paperC.bib` after the package; none was in the file before. Every citation key of `02_related_work.md` after the package is defined in `paperC.bib`. The bibliography has 71 entries after the package (67 before), and the braces of the four new entries balance.
- The audit table has four more rows, each with five tab-separated fields; each new bibliography key has exactly one row.
- Number tokens of `02_related_work.md` by the token rule of `c_pass2_check.py`: the tokens added are "3", "4" five times and "8" twice, and no token is removed; each is a `number` of the manifest at `55315ca` (package v2 changes two rows of the manifest and removes none of these). No table label 10 to 18 appears in the new text (package v2 renumbers those).
- The cell values of the new evidence rows of C-S10 equal the cells of the new rows of C-S05 and C-S06 (checked cell by cell by script).
- Quotes: every string given as a quote from a cited work in the evidence lines and in the new evidence text was found by script in the text extracted from the PDF named there; none is longer than 25 words; none is a dataset caption. The CIDEr values of UniRAG's Table 3 were read on the page in layout mode.
- No e-mail address and no key is in this package or in the apply script.

sha256 of the five files before and after this package (the apply script holds the same values as `PRE` and `TARGETS`):

| file | before | after this package, all 15 blocks | after this package without C-S15 |
|---|---|---|---|
| `paper_v1_analysis/02_related_work.md` | `8dbc299bd816bb2fd9ec689b1ef1b97a1c2cab1e331232072dc4d7afee1a60fb` | `4288f1fb73a3df4a2629a8e0f6369c639d7a00c3a2c12e81eb425fafd355d64a` | the same |
| `docs/TABLE1B_W5_EVIDENCE.md` | `11a291b36b7822f3d006ac2e25ac1c01f243f136beb37f46fb079326c4458ab2` | `03c79960beb66aac12b9fa482f9084b5cc3120f1aab9322099c13fc348d158c5` | the same |
| `paper_v1_analysis/paperC.bib` | `a415c4daa4d8c40b5b14432913d62bfefdcc30d7ff347df05637f332c23010e2` | `550b88d118f4bdb5dadbb930f05263e14ba65ab6df84c82285ccc824e1c777b8` | the same |
| `paper_v1_analysis/paperC_bib_audit.tsv` | `a1af33399c668a31efa2f13b91b85983f6f1ea780e1ccda0b3aaabcb9adb3826` | `55ece5075b17ff2b5d78d5760264d82b8e55918a5829d3a1545fbd45a83145d4` | the same |
| `paper_v1_analysis/11_supplement_registered_rows.md` | `5a71a8a08085cdaabe385539208f008275aed18fabbd6c962cf0d0c5c44f0ff9` (after package v2) | `fc7608a33f069f4882f1f9b55cba70b5bd784f60877b0e08d90142a376e53c36` | not changed |

Not checked, and said so where it matters:
- The write mode was not run. Before the CC-408 commit it refuses by design.
- The manifest check of the paper repository, the n-gram and caption scan and the LaTeX build were not run, because nothing was applied. The four new entries were not compiled with the ACM bibliography style.
- The Springer chapter of Xiang et al. was not read; the row rests on arXiv v2.
- The six works of section 3 were not read.
- If a judge changes a NEW text, `PKG_SHA256` and `TARGETS` of the apply script must be recomputed.
- If another commit changes one of the five files after package v2, the script refuses (its `PRE` check), and the blocks must be checked again.
