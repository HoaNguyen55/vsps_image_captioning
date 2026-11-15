# Related-work rows checked against the full text of the cited works (2026-11-15)

Scope: Paper A Table 2.1 (`/mnt/d/vsps_papers/vsps-paperA-spic/paper/sec2_related_work.md`, repo HEAD dafba17, file sha256 de85f341…5d080), Paper C Table 1 and Table 1b (`/mnt/d/vsps_papers/vsps-paperC-tallip/paper_v1_analysis/02_related_work.md`, repo HEAD 9b8e6ae, file sha256 da4ba374…4e887; also 01_introduction.md b731e637…, 08_english_comparison.md 72f3cd8b…, and single lines of 03_method.md, 05_preregistration_and_analysis.md, 06_results.md), the evidence file `docs/TABLE1B_W5_EVIDENCE.md` (sha256 415598fd…8bce2), and the conference version `manuscript/conf_taimma_2027/draft_v1/paper.md` (sha256 b5a44716…b61f83).

Conference draft version read: **draft_v1**. `draft_v2/paper.md` was not read: its file time was under 10 minutes old at each check (24 s at 2026-11-15T00:45:25Z, 371 s at 00:51:12Z, 173 s at 00:57:33Z). The conference blocks below are keyed by paragraph id (`p:S1-02`, `p:T1`), which draft_v2 keeps.

This file changes no paper file and nothing was committed. Every block for Paper C is marked "apply after shell C2". Sections 5.7 and 6.10 of Paper C were checked for statements about the works but get no block. Paper A Section 6.7 and supplement S11 were not opened; a name count shows that Rashidi, S. Liu and Lu are cited only in `sec2_related_work.md`.

Method. Open full texts were fetched on 2026-11-15 (00:34–00:51 UTC) with `curl` and a generic User-Agent, converted with `pdftotext`, and searched with two small scripts kept outside the download folder. PDFs are in `/tmp/claude-1000/-mnt-d-vsps-image-captioning/cbc155a0-619c-4f6d-b27a-ab9635fb7056/scratchpad/fulltext_2026-11-15/pdf/` (a scratch folder; it does not survive a reboot). A site that answered an automated read with HTTP 403 was left alone after one request per document. No browser profile was used. Page numbers are PDF pages unless a proceedings page is given. Quotes are at most 25 words; no data-set caption text is quoted.

Verdicts: CONFIRMED / WRONG / NOT STATED (not stated in the work) / NOT READ. "(Q)" marks a confirmed statement to which the full text adds a qualification that the manuscript omits. A "no" cell is confirmed only "as far as the paper states": the basis is the term search of Section 2.0.

## 1. What was read

| work | cited in | version read | URL | pages | sha256 of the PDF | version of record |
|---|---|---|---|---|---|---|
| S. Liu, Yeh, Zhang, Tian, Li 2025 | A Table 2.1 | arXiv 2407.09735 v3 (2025-02-24): main text read (Sections 1–6), all 35 pages searched; the online supplement (proofs, further simulations) not read | https://arxiv.org/pdf/2407.09735v3 | 35 | 2a932e76f7e87f7655fcbed6e5b0125f757a55d09ab8dcd3c88d5affae901398 | JASA 120(552), doi 10.1080/01621459.2025.2474266: not read (not open access per OpenAlex; not requested). The acknowledgements of v3 thank the journal's editors and three reviewers, so v3 is a revised manuscript |
| Rashidi, Zobel, Moffat 2024 | A Table 2.1 | **not read**; abstract only, from the record page of the University of Melbourne repository | https://hdl.handle.net/11343/344016 (HTML record, sha256 b84ac983…42089) | – | – | ACM TOIS 42(1), art. 19, doi 10.1145/3596511: https://dl.acm.org/doi/pdf/10.1145/3596511 answered HTTP 403 to one automated request; no arXiv copy (title search: 0 results) |
| Lu, Zhu, Li 2026 | A Table 2.1 | arXiv 2611.04099 v1 (2026-11-03): all 23 pages searched; abstract, Sections 1, 3.2–3.3, 4.1, 4.4, 6, 7, 10 and Table 19 read | https://arxiv.org/pdf/2611.04099v1 | 23 | 944c72ed864b6ba137db02e791cb83e00c014f01b37d4bae9be01fee9610c002 | none: arXiv listing on 2026-11-15 shows v1 only, comment "23 pages. Submitted to TACL", no journal reference |
| Feng et al. 2024 (added by this check) | A Table 2.1 | arXiv 2406.12663 v1 (2024-06-18), searched and read in the parts cited | https://arxiv.org/pdf/2406.12663v1 | 14 | d7a10dbe7c321ccfe6ddce98e871473117db567294f2b66ccb40db8bd1418d76 | the manuscript cites the arXiv version |
| Sarto et al. 2024 | C Table 1 | arXiv 2405.13127 v1 (2024-05-21): all 22 pages searched; Sections 1, 3.1–3.3 and 4 (all experiments) read | https://arxiv.org/pdf/2405.13127v1 | 22 | 1ef3c03cc20b80b629624353841aae2d569c23b95aad9639003f09ff2c01e7d2 | ACM TOMM 20(8), doi 10.1145/3663667: not read (ACM answered 403; the university repository copy at iris.unimore.it answered 403). Page 1 of the arXiv PDF carries the ACM reference format of the journal article |
| Bazi, Al Rahhal, Zuair 2025 (RAGCap) | C Table 1 | **not read**; abstract and results description from the authors' public code repository | https://raw.githubusercontent.com/BigData-KSU/RAGCap/main/README.md (sha256 b258d732…a583b) | – | – | IJRS 46(22), doi 10.1080/01431161.2025.2575514: not open access. TechRxiv preprint doi 10.36227/techrxiv.174140786.66325581/v1 (posted 2025-03-08, CC BY per Crossref): the site answered 403; Crossref lists the PDF only on that site |
| Awadalla et al. 2023 (OpenFlamingo) | C Table 1, Sections 1, 2, 8.2 | arXiv 2308.01390 v2 (2023-08-07), searched in full, Sections 3.2, 4, Appendix A read | https://arxiv.org/pdf/2308.01390v2 | 20 | c6157653265f4bb16e17f25dfd91e71f0d2f2931240227faaa0ab57d8cf376bc | none listed: v2 is the current arXiv version on 2026-11-15, no journal reference |
| Chen et al. 2026 (MUNIChus) | C Tables 1, 1b; conference Table 1 | LREC 2026 proceedings PDF: all 10 pages searched, Sections 2–4 read; arXiv 2603.10613 v1 compared word by word | http://www.lrec-conf.org/proceedings/lrec2026/pdf/2026.lrec2026-1.708.pdf ; https://arxiv.org/pdf/2603.10613v1 | 10 ; 10 | 93510c99a28b35af07f9fcdcafcb9ec5647805fa58fc3d6f87703e7953b32030 ; f2b8a19781d1953f396827ced1db4a10a6c39ca40097b8ead8d68e8ed5e0b2d9 | read. The two texts differ only in reading order, page numbers and the proceedings footer (pp. 9008–9017) |
| Yang et al. 2023 | C Tables 1, 1b; conference Table 1 | NeurIPS 2023 proceedings PDF, searched in full, Sections 3–4 and appendices read; arXiv 2305.14800 v6 compared | https://proceedings.neurips.cc/paper_files/paper/2023/file/804b5e300c9ed4e3ea3b073f186f4adc-Paper-Conference.pdf ; https://arxiv.org/pdf/2305.14800v6 | 20 ; 20 | 9bb3f3b43c4c94ae693e6478994fe5df821c4d3f3cf99e71dbe51e22a271c9e1 ; d0c981ea6e11be70b2f6427999cff2f88aac486d1d942d01647ca7e549eeee25 | read. Word-level comparison: identical except the arXiv stamp |
| W. Li et al. 2024 | C Tables 1, 1b; conference Table 1 | ACL 2024 proceedings PDF, searched in full, Sections 3–5 read | https://aclanthology.org/2024.acl-long.503.pdf | 15 | 1109b0474610d2a82fa2f3ccfc334baa765724ccde55fa4dcccc2b3fe0245abc | read (pp. 9285–9299) |
| Baldassini et al. 2024 | C Tables 1, 1b; conference Table 1 | CVPR 2024 Workshops, open-access version of the Computer Vision Foundation, with its supplement; Sections 3–6 read | https://openaccess.thecvf.com/content/CVPR2024W/PV/papers/Baldassini_What_Makes_Multimodal_In-Context_Learning_Work_CVPRW_2024_paper.pdf ; …/supplemental/Baldassini_What_Makes_Multimodal_CVPRW_2024_supplemental.pdf | 12 ; 9 | 2cd7d0b6bb6c2c37d0c051e462d980d38f1c4095c914bc5268571f9065fdc75d ; 0ca7af8fd51b661a6ff14a5b43fe520ffd5f8813d4a973936ac337bd3747cea8 | the PDF states that it is identical to the accepted version except for a watermark; the IEEE Xplore copy was not read. arXiv 2404.15736 v2 also stored (1e2474fa…1e7d2), not used |
| S. Chen et al. 2025 (TrueMICL) | C Table 1b | arXiv 2507.15807 v2 (2025-08-06), header "Published as a conference paper at COLM 2025"; searched in full, Sections 1, 4, Appendix D read | https://arxiv.org/pdf/2507.15807v2 | 21 | 5d3a87cd83664fb9441f2316e2b47dba01f74eb87f35495e7dbfb2864fdf4e6c | OpenReview copy of the COLM paper (forum n4JdyBGu6T) answered 403; not read |
| L. Li et al. 2025/2026 | C Table 1b; conference Table 1 | arXiv 2507.08021 v1 (2025-07-08), searched in full, Sections III–V read | https://arxiv.org/pdf/2507.08021v1 | 16 | 97fe281b204e185dab53e9916130fb3fd42adae9951e31ffc49403492aab7e34 | IEEE TPAMI 48(11), doi 10.1109/TPAMI.2026.3719106 (published 2026-07-31): not open access, not read. The preprint is a year older than the article |

Rows found by the first pass over the three tables: the ones marked in the manuscripts are Rashidi ("from its abstract only"), S. Liu ("read in part"), Lu ("preprint"), RAGCap ("from its abstract", three "–" cells), Sarto ("from the abstract", three "–" cells), MUNIChus in Table 1b (one "–" cell) and in the conference Table 1 ("not stated"). Added: the Feng et al. row of Table 2.1, because the source comment of `sec2_related_work.md` l.14 records "arXiv abstract read" for it.

## 2. Verdict per cell and per sentence

### 2.0 Term search behind the "no" cells (hits in the whole document, case-insensitive)

| text | preregist / pre-regist | registered | confidence interval | bootstrap | standard deviation / std / SD | ± | seed(s) | p-value | error bar | Vietnam | English | random |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sarto, arXiv v1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MUNIChus, LREC (same counts in arXiv v1) | 0 | 0 | 0 | 0 | 0 | 0 | 1 (a reference title) | 0 | 0 | 0 | 12 | 12 |
| Yang, NeurIPS | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14 |
| W. Li, ACL | 0 | 0 | 0 | 0 | 0 | 0 | 1 ("three seeds") | 0 | 0 | 0 | 1 (inside an example) | 26 |
| Baldassini, main | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 (regression and correlation coefficients) | 0 | 0 | 0 | 48 |
| Baldassini, supplement | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 35 |
| S. Chen (TrueMICL), arXiv v2 | 0 | 0 | 0 | 0 | 1 | 126 (Table 2 and appendix tables of the TrueMICL tasks) | 3 | 0 | 0 | 0 | 0 | 16 |
| L. Li, arXiv v1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| OpenFlamingo, arXiv v2 | 0 | 0 | 0 | 0 | 3 | 0 | 4 | 0 | 2 | 0 | 1 | 16 |
| S. Liu, arXiv v3 | 0 | 0 | 15 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 9 |
| Lu, arXiv v1 | 28 | 22 | 0 | 14 | 6 | 4 | 53 | 13 | 0 | 0 | 7 | 10 |
| Feng, arXiv v1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 (image sampling) | 0 | 0 | 0 | 0 | 8 |

Other searches: S. Liu: "caption" 0, "F1" 0, "F-measure" 0, "hallucinat" 0, "metric" 0. Lu: "caption" 0, "image" 0, "open-ended" 1. Sarto: "oracle" 9 (the upper bound of Table 1), "CHAIR" 0. MUNIChus: "significance", "variance", "runs": 0 relevant hits.

### 2.1 Paper A, Table 2.1 and Section 2 (`sec2_related_work.md`)

| id | line | statement in the manuscript | what the full text says (place) | quote | verdict | note |
|---|---|---|---|---|---|---|
| A-01 | 12 | tests of the SCAR assumption exist (… S. Liu et al., 2025) | Abstract p. 1; Section 6 p. 30 equates the paper's "CD" assumption with SCAR | "developing a goodness-of-fit test for the CD assumption and constructing confidence intervals for the proportion of positive instances in the target domain"; "the CD assumption is equivalent to the SCAR assumption" | CONFIRMED | |
| A-02 | 33 | Question: how to model, test and classify positive–unlabelled data when SCAR fails | Abstract p. 1; Section 1.4 pp. 7–8 (model, estimation, tests, classifier) | "the labeled and unlabeled positive data can be from different distributions" | CONFIRMED | |
| A-03 | 33 | Data and systems: simulations; one tabular data set | Section 5.1 p. 21; Section 5.2 p. 27 (20 features, four price classes) | "We conduct a simulation study to assess the performance of our proposed framework across various tasks"; "We consider the Mobile Phone Dataset from the Kaggle" | CONFIRMED | |
| A-04 | 33 | Gold used: class labels, partly hidden | Section 1.1 p. 2; Section 5.2 p. 27 builds a labelled positive sample and an unlabelled mixture from the class labels | "the second sample is unlabeled, meaning we can only access the features x but have no access to their labels y" | CONFIRMED | |
| A-05 | 33 | Needs new labels: no | Section 5: simulated data and one public data set; no label collection is described | – | CONFIRMED | our reading, as the table caption says |
| A-06 | 33 | Statistical guarantee: empirical-likelihood ratio test with a chi-square limit; confidence interval for the positive share | Theorem 3, Section 4.1 p. 20 (limits χ² with p and 1 degrees of freedom) | "we can also construct the ELR-based confidence interval for the mixture proportion π" | CONFIRMED | |
| A-07 | 33 | Languages: not applicable | no language data in the paper | – | CONFIRMED | |
| A-08 | 33 | What remains: no evaluation metric is studied | Section 2.0 searches: 0 hits; Section 5 reports rejection rates, RMSE, coverage and classification accuracy of the proposed model | – | CONFIRMED | |
| A-09 | 29 | Lu et al. (2026), "(preprint)" | arXiv listing 2026-11-15: v1 only (2026-11-03), "Submitted to TACL", no journal reference | – | CONFIRMED | re-check on the day of submission |
| A-10 | 29 | Question: do readings and rankings move when the evaluation contract changes, with predictions frozen | Abstract p. 1 | "With predictions frozen, a method ordering reverses under a gold-standard exchange" | CONFIRMED | |
| A-11 | 29 | Data and systems: document relation extraction (two gold versions), TACRED revisions, a UD probe, translation, retrieval, QA and code; boundary results on SST-2, NER and XNLI | Section 4.1 p. 5; Section 4.4 p. 8; Section 6 p. 9; Table 19 p. 23 | "Two gold versions, gD and gR (revised projection of Tan et al., 2022b), instantiate the gold-revision lever"; "The findings span SST-2 (Socher et al., 2013), NER (Tjong Kim Sang and De Meulder, 2003), XNLI" | CONFIRMED | the row does not name HacRED (one gold, Chinese), which the paper also uses |
| A-12 | 29 | Gold used: officially released gold revisions | Abstract p. 1; Section 4.1 p. 5 | "Evidence spans DocRE, HacRED, a UD probe, and released gold revisions" | CONFIRMED | |
| A-13 | 29 | Needs new labels: no | released golds only; Section 7 p. 10 reports a human check of 50 output-format violations, which is not a gold | – | CONFIRMED | our reading |
| A-14 | 29 | Statistical guarantee: paired bootstrap intervals, Holm correction, a no-flip margin lemma; registered | Section 4.1 p. 5; Section 3.3 p. 4 and Appendix B p. 19; Section 4.4 p. 8 | "All experiments follow a preregistration document frozen before any training or download"; "Lemma B: no-flip margin guarantee"; "observational breadth for Props. 1–2, outside the preregistered ledger" | CONFIRMED | (Q) the paper places its cross-task replications (retrieval, translation, QA, code, the released-gold audits) outside the registered record; block A-2 |
| A-15 | 29 | Languages: English and Chinese (relation extraction, UD); German–English and Chinese–English (translation) | Section 4.1 p. 5; Fig. 3 p. 7 and Table 5 p. 17 (English DocRED); Table 19 p. 23; Section 5 p. 8 | "HacRED (Cheng et al., 2021) (Chinese, 15 seeds) has one gold"; "English EWT r1.2 vs. r2.18 test"; "Chinese GSD r1.3 vs. r2.0 dev"; "On the WMT19 de-en and zh-en grids" | CONFIRMED | |
| A-16 | 29 | What remains: open-ended captions (outside their tested scope) | Section 3.2 p. 4; "caption" 0 hits | "open-ended generation is untested scope" | CONFIRMED | |
| A-17 | 36 | Lu et al. hold predictions fixed and exchange officially released gold versions in a registered study of structured prediction, and report open-ended generation as outside their tested scope | as A-10, A-12, A-14, A-16 | as above | CONFIRMED | |
| A-18 | 12 | with errors introduced through a model of judge error, orderings that tests report as significant can be incorrect (Rashidi et al., 2024) | full text not read. The abstract agrees | abstract: "even moderate amounts of error can lead to conclusions such as orderings of systems that statistical tests report as significant but are nonetheless incorrect" | NOT READ | |
| A-19 | 30 | Question: how do judgment errors affect retrieval measures and system orderings | full text not read. The abstract agrees | abstract: "making use of a model of systematic errors in binary relevance judgments that can be tuned" | NOT READ | |
| A-20 | 30 | Data and systems: retrieval effectiveness measures under a tunable model of judge error | full text not read; the abstract names AP, NDCG and RBP but no test collection or system set | – | NOT READ | |
| A-21 | 30 | Gold used: relevance judgments plus an error model | full text not read; the abstract agrees | – | NOT READ | |
| A-22 | 30 | Needs new labels: no (error model) | full text not read; the abstract does not say where the judgments come from | – | NOT READ | |
| A-23 | 30 | Statistical guarantee: distribution of "true" scores behind judgments that include error | full text not read; the abstract agrees | abstract: "we examine the distribution of “true” effectiveness measurements that could be underlying measurements based on sets of judgments that include error" | NOT READ | |
| A-24 | 30 | Languages: not applicable | full text not read | – | NOT READ | |
| A-25 | 30 | What remains: captioning; one-sided omissions; a length-dependent sign, not general fragility | full text not read; the abstract speaks of measures that are more or less "fragile" | – | NOT READ | |
| A-26 | 14 | Feng et al. inspect by hand the objects that CHAIR flags in LLaVA-1.5 captions of 500 COCO images and judge more than half unjustified | Section 3.2 p. 3 | "we generated captions for 500 randomly selected images from the MSCOCO validation dataset using LLaVA-1.5"; "we found that over 55% of these identified hallucinations are unjustified" | CONFIRMED | |
| A-27 | 14 | … attribute part of this to reference captions that omit detail, more so for detailed captions; then propose embedding-based metrics on image regions and caption phrases | Section 3.2 pp. 3–4; Section 4.3 pp. 6–7 | "The misjudgment is due to two main reasons, and both are exacerbated in detailed captions"; "ground-truth captions from humans often omit subassemblies" | CONFIRMED | |
| A-28 | 24 | Question (Feng row) | title and Section 3 | – | CONFIRMED | |
| A-29 | 24 | Data and systems: 500 COCO images, LLaVA-1.5 (CHAIR check); 500 Visual Genome images, 3 LVLMs | Section 3.2 p. 3; Section 5.1 p. 7 (LLaVA-1.5, mPLUG-Owl2, MiniGPT4-v2) | "we randomly pick 500 images from the validation set using the same random seed across different methods and LVLMs" | CONFIRMED | |
| A-30 | 24 | Gold used: CHAIR gold as released; Visual Genome regions for the new metrics | Section 3.2 p. 3; Section 5.1 p. 7 | – | CONFIRMED | |
| A-31 | 24 | Needs new labels: yes, manual inspection of flagged objects | Section 3.2 p. 3 | as A-26 | CONFIRMED | |
| A-32 | 24 | Statistical guarantee: none, one share, no interval | Section 2.0: 0 hits | – | CONFIRMED | |
| A-33 | 24 | Languages: English | "English" 0 hits; the data are MSCOCO and Visual Genome | – | NOT STATED | the table caption says each cell is as the authors report it; block A-3 |

Status line, not a statement about a work: l.36 "S. Liu et al. (2025), read in part" is out of date after this check (block A-1). l.20 and l.36 "Rashidi et al. (2024) … abstract only" stay true.

### 2.2 Paper C, Table 1, Table 1b and text (`02_related_work.md` unless a file is named)

Sarto et al. 2024 (arXiv v1)

| id | line | statement in the manuscript | what the full text says (place) | quote | verdict | note |
|---|---|---|---|---|---|---|
| C-01 | 7 | train captioners that read text retrieved from an external memory by visual similarity and report, on COCO and nocaps, larger gains with a larger retrieval corpus | Abstract p. 1; Section 1 p. 3; Section 4.3 p. 16 | "demonstrate that incorporating an explicit external memory can significantly enhance the quality of captions, especially with a larger retrieval corpus" | CONFIRMED | |
| C-02 | 49 | trained: yes | Section 4.1 p. 11 | "we employ the standard two-stage training protocol typically used by almost all captioning models" | CONFIRMED | |
| C-03 | 49 | sees the image: yes | Section 3.1 p. 5 | "we condition our language model on both the input image" | CONFIRMED | |
| C-04 | 49 | retrieved content: text from an external memory | Section 3.2 p. 6 | "the external memory can return all the captions of the selected images" | CONFIRMED | "captions" is the more exact word |
| C-05 | 49 | languages: "– (COCO, nocaps)" | data sets: Section 4.1 p. 10. The language is not named ("English" 0 hits) | "we train our model on COCO and evaluate on nocaps validation set" | NOT STATED | fill "English (COCO, nocaps)" with the caption note of block C-2 |
| C-06 | 49 | random control: "–" | no random-example condition: "random" 0 hits; the comparisons are a Transformer without retrieval and an oracle over the k nearest captions (Table 1 p. 12) | "in comparison with Transformer-based baselines that do not leverage additional knowledge retrieved from an external memory" | NOT STATED | fill "no" |
| C-07 | 49 | statistics: "–" | Section 2.0: 0 hits for every term; Tables 2–5 give single values | – | NOT STATED | fill "none" |

Bazi et al. 2025, RAGCap (not read)

| id | line | statement in the manuscript | what could be checked | quote | verdict | note |
|---|---|---|---|---|---|---|
| C-08 | 7 | without fine-tuning, retrieves image-caption pairs with SigLIP and places them in the prompt of Qwen2-VL for remote-sensing captioning | full text not read; the abstract in the authors' repository agrees | repository abstract: "identify relevant image-caption pairs from the training set" | NOT READ | |
| C-09 | 48 | trained: no | abstract only | repository abstract: "without the need for fine-tuning" | NOT READ | |
| C-10 | 48 | sees the image: yes | abstract only | repository abstract: "These retrieved examples, along with the test image, are processed by a multi-image capable VLM (Qwen2VL)" | NOT READ | |
| C-11 | 48 | retrieved content: image-caption pairs | abstract only | as C-08 | NOT READ | |
| C-12 | 48 | languages: "–" | not in the abstract; the repository page names the Sydney, UCM and NWPU caption sets | – | NOT READ | stays "–" |
| C-13 | 48 | random control: "–" | not in the abstract | – | NOT READ | stays "–" |
| C-14 | 48 | statistics: "–" | not in the abstract; the repository page names BLEU, ROUGE, CIDEr, SPICE | – | NOT READ | stays "–" |
| C-15 | 03_method.md 126 | "an image-caption-pair prompt format, as used by RAGCap; not RAGCap" | the abstract supports image-caption pairs given with the test image; the layout of the prompt is not in it | – | NOT READ | no block (file held until shell C2; work unread) |
| C-16 | 06_results.md 231 | the same label on the block-3 rows | as C-15 | – | NOT READ | Section 6.10: no block |

Awadalla et al. 2023, OpenFlamingo (arXiv v2, the current version)

| id | line | statement in the manuscript | what the full text says (place) | quote | verdict | note |
|---|---|---|---|---|---|---|
| C-17 | 20 | RICES: example images chosen by image similarity, shown interleaved with their captions, at an equal number of shots | Appendix A.2 p. 14; Table 9 p. 14 | "RICES selects the top-k most similar training examples as demonstrations" | CONFIRMED | |
| C-18 | 20 | Table 9 (OpenFlamingo-9B), COCO: +4.1 CIDEr at 4 shots, +9.5 at 32 | Table 9 p. 14: 89.0 → 93.1 (+4.1); 99.5 → 109.0 (+9.5) | – | CONFIRMED | numbers read in the layout text of the page |
| C-19 | 20 | Flickr-30K: −20.3 at 0 shots (retrieval selects only the two text-only prompt examples), −13.6 at 4, −4.2 at 8, +1.7 at 32; no 16-shot row | Table 9 p. 14: 59.5 → 39.2 (−20.3); 65.8 → 52.2 (−13.6); 62.9 → 58.7 (−4.2); 61.3 → 63.0 (+1.7); rows 0, 4, 8, 32 only; footnote 2 p. 14 | footnote 2, read on the page: "In 0-shot evaluations, RICES is still used to select the two text-only examples used for the prompt" | CONFIRMED | the prose of A.2 says "CIDEr degrades by 20.4 in 0-shot evaluations" and 13.1 at 4 shots; the manuscript cites the table, as the evidence file already records |
| C-20 | 43 | trained: no task training (web-pretrained) | Section 3.2 pp. 4–5 (LAION-2B, Multimodal C4) | – | CONFIRMED | |
| C-21 | 43 | sees the image: yes | Section 3.1 p. 3 | – | CONFIRMED | |
| C-22 | 43 | retrieved content: image-caption pairs, interleaved | as C-17 | as C-17 | CONFIRMED | |
| C-23 | 43 | languages: English | Section 3.2 p. 4 names the English subset of LAION-2B for training; the language of the test sets is not named | read on the page: "We use part of the English subset and truncate captions to 32 tokens" | CONFIRMED | |
| C-24 | 43 | random control: yes, equal shots | Table 9 p. 14, columns Random and RICES per shot count | "In Table 9, we compare OpenFlamingo-9B performance using RICES to performance using randomly selected in-context examples" | CONFIRMED | |
| C-25 | 43 | statistics: three seeds with SD (random-demonstration rows) | Table 11 caption p. 18; Table 12 (RICES) and Table 9 carry no SD | "Results are averaged across 3 evaluation seeds and reported with standard deviations" | CONFIRMED | |
| C-26 | 01_introduction.md 9 | retrieved examples beat random ones on COCO; on Flickr-30K worse at 0, 4 and 8 shots and better only at 32 of the shot counts of Table 9 | as C-18, C-19 | – | CONFIRMED | |
| C-27 | 08_english_comparison.md 43 | OpenFlamingo-9B scored lower with retrieved than with random examples on Flickr-30K at 0, 4 and 8 shots, though not at 32 (its Table 9) | as C-19 | – | CONFIRMED | Section 8.2 prints no OpenFlamingo number, only the shot counts |
| C-28 | 64, 65 | compares similarity-based with random examples, with interleaved images; the COCO result "replicates the OpenFlamingo pattern" | as C-17, C-18 | – | CONFIRMED | |

Chen et al. 2026, MUNIChus (LREC 2026 proceedings; proceedings pages)

| id | line | statement in the manuscript | what the full text says (place) | quote | verdict | note |
|---|---|---|---|---|---|---|
| C-29 | 01_introduction.md 9 | compares random with similarity-retrieved examples at equal k, in nine languages that do not include Vietnamese | Sections 3.1.2–3.1.3 pp. 9010–9011; Table 1 p. 9009; "Vietnam" 0 hits | "we augmented each query with three randomly sampled examples from the same language’s training set" | CONFIRMED | |
| C-30 | 11 | nine languages: Arabic, Chinese, English, French, Hindi, Indonesian, Japanese, Sinhala, Urdu | Table 1 p. 9009 (column heads) | "Dataset statistics for MUNIChus across nine languages" | CONFIRMED | |
| C-31 | 11 | zero-shot against three random and three similarity-retrieved examples from the same language's training set, each an image with its article excerpt and caption | Sections 3.1.1–3.1.3 pp. 9010–9011 | "Each example consisted of an image, its corresponding news article excerpt, and the reference caption"; "retrieving the three training instances with the highest cosine similarity to the test image embedding" | CONFIRMED | |
| C-32 | 11 | seven MLLMs that include Qwen2.5-VL-7B and Aya-Vision-8B | Table 2 p. 9012: Aya-vision-8b, Aya-vision-32b, GPT-4o, Llama-3.2-11B, Phi-3.5-vision, Qwen2.5-VL-7B, Qwen3-VL-8B | – | CONFIRMED | |
| C-33 | 11 | reports BLEU-4 and CIDEr as point scores; concludes that the three prompting strategies gave mixed results | Section 2.1 p. 9010; Table 2 p. 9012; finding F5 p. 9013 | "we restricted our evaluation to BLEU-4 and CIDEr"; "The three prompting strategies yielded mixed results, with no clear indication that any is beneficial for news-image-captioning" | CONFIRMED | |
| C-34 | 12 | Vietnamese is a language that MUNIChus does not cover | Table 1 p. 9009; "Vietnam" 0 hits | – | CONFIRMED | the same line also covers Rebelo et al., which this check did not read |
| C-35 | 47 | trained: no (two models are fine-tuned in a separate condition) | Section 3.2 p. 9011 | "We fine-tuned aya-vision-8b and Llama3.2-11B-Vision-Instruct using TRL’s SFTTrainer" | CONFIRMED | |
| C-36 | 47 | sees the image: yes | Section 3.1 pp. 9010–9011 | – | CONFIRMED | |
| C-37 | 47 | retrieved content: three training items, each an image, an article excerpt and a caption | as C-31 | as C-31 | CONFIRMED | |
| C-38 | 47 | languages: 9, no Vietnamese | as C-30, C-34 | – | CONFIRMED | |
| C-39 | 47 | random control: yes, equal k = 3 | as C-29, C-31 | as C-29 | CONFIRMED | |
| C-40 | 47 | statistics: none (point scores) | Table 2 p. 9012: one BLEU-4 and one CIDEr value per model and language; Section 2.0: 0 relevant hits | – | CONFIRMED | the number of random draws is not stated |
| C-41 | 61 | question: whether zero-shot, random or similar few-shot prompts help news image captioning | Section 3.1; finding F5 | as C-33 | CONFIRMED | |
| C-42 | 61 | languages: the nine named | as C-30 | – | CONFIRMED | |
| C-43 | 61 | captioning data: MUNIChus (BBC news images with their articles) | Section 2 p. 9009 | "We developed a Python-based scraper to collect BBC news articles in the languages listed in Table 1" | CONFIRMED | |
| C-44 | 61 | models: seven MLLMs under prompting, including Qwen2.5-VL-7B, Qwen3-VL-8B and Aya-Vision-8B | as C-32 | – | CONFIRMED | |
| C-45 | 61 | equal-k random control: yes, k = 3, examples with image and article excerpt | as C-31 | – | CONFIRMED | |
| C-46 | 61 | per-backbone rows: yes | Table 2 p. 9012: one row per model in each prompting block | – | CONFIRMED | |
| C-47 | 61 | registered, one look: "–" | Section 2.0: 0 hits for "preregist", "pre-regist", "registered" | – | NOT STATED | fill "no", on the same basis as the other rows of the column (block C-5) |
| C-48 | 61 | CIs on the captioning score: no | as C-40 | – | CONFIRMED | |
| C-49 | 64, 69 | compares similar with random examples at equal k (k = 3, examples with images) for news image captioning in nine languages, without Vietnamese and without intervals on its scores | as C-29 to C-40 | – | CONFIRMED | |

Yang et al. 2023 (NeurIPS 2023 proceedings PDF)

| id | line | statement in the manuscript | what the full text says (place) | quote | verdict | note |
|---|---|---|---|---|---|---|
| C-50 | 20; 01_introduction.md 9 | compare image-selection and caption-assignment strategies for in-context captioning | Sections 3.1–3.2 p. 4 | "strategies used to configure in-context image-caption pairs" | CONFIRMED | |
| C-51 | 20, 44, 56 | "in English" / language cells "English" | "English" 0 hits; data: MSCOCO, Section 4.1 p. 6 | – | NOT STATED | caption note of blocks C-2 and C-4 |
| C-52 | 44 | trained: no | Section 3 p. 4: a pre-trained vision-language model is prompted | – | CONFIRMED | |
| C-53 | 44 | sees the image: yes | Section 3 p. 4 | – | CONFIRMED | |
| C-54 | 44 | retrieved content: image-caption pairs | as C-50 | as C-50 | CONFIRMED | |
| C-55 | 44, 56 | random control: yes, equal shots | Section 3.1 p. 4; Tables 3–8 pp. 15–17 (Random Selection against similarity-based selection at 4, 8, 16, 32 shots) | "we randomly sample n images" | CONFIRMED | |
| C-56 | 44 | statistics: none | Section 2.0: 0 hits; Tables 3–8 give single values; the number of runs is not stated | – | CONFIRMED | |
| C-57 | 56 | question: which image-selection and caption-assignment configurations help | as C-50 | – | CONFIRMED | |
| C-58 | 56 | captioning data: COCO | Section 4.1 p. 6 | "We used the Karpathy split [59] in the experiments" | CONFIRMED | |
| C-59 | 56 | models: OpenFlamingo (two versions), Otter | Appendix A p. 15 (v1 9B), Appendix B p. 16 (v2 3B), Appendix C p. 16 (Otter) | "Here we present the numerical results on Open-Flamingo v2 3B model"; "Here we present the numerical results on Otter model in Table 8" | CONFIRMED | |
| C-60 | 56 | per-backbone rows: yes | Tables 7 and 8 p. 17, one table per model | – | CONFIRMED | |
| C-61 | 56 | registered, one look: no | Section 2.0: 0 hits | – | CONFIRMED | |
| C-62 | 56 | CIs on the captioning score: no | as C-56 | – | CONFIRMED | |

W. Li et al. 2024 (ACL 2024 proceedings; proceedings pages)

| id | line | statement in the manuscript | what the full text says (place) | quote | verdict | note |
|---|---|---|---|---|---|---|
| C-63 | 01_introduction.md 9, 16 | how retrieval-augmented captioners react to random or misleading retrievals; a model can copy objects of the retrieved captions | Abstract p. 9285; Sections 3–4 | "those tokens are likely copied into the generated output" | CONFIRMED | the paper speaks of tokens; "objects" is the manuscript's word |
| C-64 | 7 | gives SmallCap, at the same k, captions retrieved for another image, and its scores fall below those of the model without retrieval | Section 3.1 p. 9287; Fig. 2 p. 9287; Section 3.3 p. 9287 | "Here the randomly retrieved captions are those retrieved with another image"; "performance drops drastically compared to the no-retrieval baseline" | CONFIRMED | |
| C-65 | 9 | retrieval-augmented captioners copy tokens from the retrieved captions | Abstract p. 9285; Section 4 | as C-63 | CONFIRMED | one model, SmallCap, with two decoders |
| C-66 | 9 | … and are sensitive to their order | Section 3.3 p. 9287, heading "Order Robust but Content Sensitive" | "is indeed robust to the order of the retrieved texts" | WRONG | correct: robust to the order of the retrieved captions; block C-1 |
| C-67 | 9 | … and to their selection | Section 3.3 p. 9287 | as C-64 | CONFIRMED | |
| C-68 | 36 | trained: yes | Section 5.1 p. 9291 (SmallCap trained on COCO) | – | CONFIRMED | |
| C-69 | 36 | sees the image: yes | Section 3.2 p. 9287 (image encoder) | – | CONFIRMED | |
| C-70 | 36 | retrieved content: captions | Section 3.1 p. 9287 | – | CONFIRMED | |
| C-71 | 36, 57 | languages: English | "English" 1 hit, inside an example; data COCO, NoCaps, VizWiz | – | NOT STATED | caption note of blocks C-2 and C-4 |
| C-72 | 36, 57 | random control: yes, equal k | Fig. 2 p. 9287 and Table 3 p. 9291, k = 1 to 4 | as C-64 | CONFIRMED | |
| C-73 | 36 | statistics: three seeds, no CI | Table 3 caption p. 9291; Section 2.0: 0 hits for the other terms | "Results are averaged over three seeds" | CONFIRMED | |
| C-74 | 57 | question: robustness of a retrieval-augmented captioner | Abstract p. 9285 | – | CONFIRMED | |
| C-75 | 57 | captioning data: COCO, NoCaps, VizWiz | Section 3.2 p. 9287; Section 5.2 p. 9291 | – | CONFIRMED | |
| C-76 | 57 | models: SmallCap (trained), two decoders | Section 3.2 p. 9287 (OPT-350M and GPT-2) | – | CONFIRMED | |
| C-77 | 57 | per-backbone rows: "decoder columns in one table" | both decoders appear in Table 1 p. 9287 (COCO) and Table 2 p. 9288 (NoCaps), and in appendix Tables 6 and 7 p. 9296, all on the order test; Section 5.1 trains with OPT only | – | WRONG | correct: decoder columns in the order tables only (blocks C-6, C-8) |
| C-78 | 57 | registered, one look: no | Section 2.0: 0 hits | – | CONFIRMED | |
| C-79 | 57 | CIs on the captioning score: no (mean of three seeds) | as C-73 | as C-73 | CONFIRMED | |
| C-80 | 06_results.md 122 | SmallCap is sensitive to tokens shared by most retrieved captions, likely copied into its output; lowered by training with retrieved captions sampled from more diverse sets | Abstract p. 9285 | "we propose to train the model by sampling retrieved captions from more diverse sets" | CONFIRMED | no block (file held) |

Baldassini et al. 2024 (CVPR 2024 Workshops; proceedings pages 1539–1550)

| id | line | statement in the manuscript | what the full text says (place) | quote | verdict | note |
|---|---|---|---|---|---|---|
| C-81 | 20, 64; 01_introduction.md 9 | multimodal in-context learning in open interleaved models is driven mainly by the text of the examples | Abstract p. 1539; Conclusion p. 1546. For captioning, Sections 4.1–4.2 pp. 1541–1542 report that the example images matter too | "M-ICL primarily relies on text-driven mechanisms, showing little to no influence from the image modality"; "Incorporating images further enhances performance by an additional 20 points, underscoring the importance of both modalities" | CONFIRMED | (Q) for captioning the paper reports an effect of the example images; block C-7 |
| C-82 | 20 | similarity-based example selection does no better than majority voting over the examples' answers | Abstract p. 1539; Section 5.1 p. 1545 limits this to classification and says the opposite for captioning | "M-ICL is not better than a simple strategy based on majority voting over context examples"; "In open-ended generation tasks, i.e. captioning and visual question answering, majority voting is insufficient" | CONFIRMED | (Q) the sentence follows the abstract; the body restricts the finding to classification; block C-7 |
| C-83 | 45 | trained: no | Section 3 p. 1541 (IDEFICS 9B prompted) | – | CONFIRMED | |
| C-84 | 45 | sees the image: yes | Section 3 | – | CONFIRMED | |
| C-85 | 45 | retrieved content: image-caption pairs | Section 3 p. 1540 (RICES over the training set) | – | CONFIRMED | |
| C-86 | 45, 58 | languages: English | "English" 0 hits; captioning data COCO and Flickr30k | – | NOT STATED | caption note of blocks C-2 and C-4 |
| C-87 | 45, 58 | random control: yes, equal shots (IDEFICS) | Fig. 4 p. 1543; supplement Tables 7 and 10 (random and RICES at 4, 8, 16, 32 shots) | – | CONFIRMED | |
| C-88 | 45 | statistics: tests on the analyses, no CI on CIDEr | Section 3 p. 1541; Tables 1–3 pp. 1544–1545 (p-values of coefficients); Section 2.0 | "We repeat each experiment 3 times and report the averaged results"; "All coeff. have a p-value < 0.001" | CONFIRMED | |
| C-89 | 58 | question: what drives multimodal in-context learning | title; Section 1 | – | CONFIRMED | |
| C-90 | 58 | captioning data: COCO, Flickr30K | Section 3 p. 1541 | – | CONFIRMED | |
| C-91 | 58 | models: IDEFICS; OpenFlamingo in an appendix | Section 3 p. 1541; supplement Section 8.1 and Table 4 p. 2 | "Evaluation results using OpenFlamingo 9B and demonstrations sampled uniformly at random" | CONFIRMED | |
| C-92 | 58 | per-backbone rows: partly (OpenFlamingo: random examples only) | supplement Table 4 p. 2 | as C-91 | CONFIRMED | |
| C-93 | 58 | registered, one look: no | Section 2.0: 0 hits | – | CONFIRMED | |
| C-94 | 58 | CIs on the captioning score: no (mean of three runs; tests on the analyses) | as C-88 | as C-88 | CONFIRMED | |

S. Chen et al. 2025, TrueMICL (arXiv v2 with the COLM 2025 header)

| id | line | statement in the manuscript | what the full text says (place) | quote | verdict | note |
|---|---|---|---|---|---|---|
| C-95 | 20, 64; 01_introduction.md 9 | MLLMs tend to imitate the text of the demonstrations rather than use their visual content | Abstract p. 1 | "they tend to neglect visual cues and over-rely on textual patterns, leading to mere text imitation rather than genuine multimodal adaptation" | CONFIRMED | |
| C-96 | 59 | question: whether models use the demonstrations' visual content | Abstract p. 1; Section 1 p. 2 | as C-95 | CONFIRMED | |
| C-97 | 59 | language: English | "English" 0 hits; data MSCOCO and the paper's own tasks | – | NOT STATED | caption note of block C-4 |
| C-98 | 59 | captioning data: COCO, as a side check | Section 4.1 p. 6; Appendix Table 8 p. 19 | "Accuracy is used for VQAv2, GQA, and A-OKVQA and CIDEr used for COCO" | CONFIRMED | |
| C-99 | 59 | models: Qwen2-VL, Idefics3, Phi-3.5-Vision | Section 4.1 p. 5 | – | CONFIRMED | GPT-4o is also reported, for the TrueMICL tasks |
| C-100 | 59 | equal-k random control: no for captioning (random examples only) | Table 8 p. 19: rows Zero-shot, No-image, Random, LoRA, DARA; RICES appears only in Table 2 p. 7 | – | CONFIRMED | |
| C-101 | 59 | per-backbone rows: yes | Table 8 p. 19, one block per model | – | CONFIRMED | |
| C-102 | 59 | registered, one look: no | Section 2.0: 0 hits | – | CONFIRMED | |
| C-103 | 59 | CIs on the captioning score: no (SDs on a non-captioning task only) | Table 2 p. 7 (TrueMICL accuracy with SD); Table 8 p. 19 point values | "Experiments are averaged over 3 different seeds, and the performance is in percentage with the standard deviations" | CONFIRMED | |

L. Li et al. 2025/2026 (arXiv v1; the TPAMI article was not read)

| id | line | statement in the manuscript | what the full text says (place) | quote | verdict | note |
|---|---|---|---|---|---|---|
| C-104 | 20; 01_introduction.md 9 | analyse shot count, retrieval and attention inside such models | Abstract p. 1 | – | CONFIRMED | |
| C-105 | 20 | for OpenFlamingo and IDEFICS on COCO, examples chosen by image similarity raise CIDEr over randomly sampled ones | Section IV-C, "Image Similarity", p. 11; Fig. 9 p. 11 | "using visually similar ICE images increases CIDEr scores for both LMMs" | CONFIRMED | |
| C-106 | 20 | … and attribute the gain to copying of the example captions, measured by a CIDEr score between the output and the examples' captions | Finding 5 p. 11; Section IV-B p. 8 | "While using visually similar ICE images increases CIDEr scores, this is essentially due to short-cut phenomenon where captions from ICE are copied"; "It is calculated by getting the CIDEr score between generated captions and ICE captions" | CONFIRMED | |
| C-107 | 60 | question: shot count, retrieval and attention inside the model | Abstract p. 1 | – | CONFIRMED | |
| C-108 | 60 | language: English | "English" 0 hits; data MSCOCO | – | NOT STATED | caption note of block C-4 |
| C-109 | 60 | captioning data: COCO | Section IV-A p. 7 | "we use the Karpathy split [78] in the experiments" | CONFIRMED | |
| C-110 | 60 | models: OpenFlamingo-v2-9B, IDEFICS-9B | Section IV-A p. 7 | "IDEFICS v1-9B [28] are employed for evaluating" | CONFIRMED | |
| C-111 | 60 | equal-k random control: yes, equal shots | Section III-B p. 4; Section IV-A p. 7; Fig. 9 p. 11 (dashed line: Random Sampling) | "we experimented with shot counts of 4, 8, 16, and 32" | CONFIRMED | values are read from a plot |
| C-112 | 60 | per-backbone rows: yes | Figs. 5–9 pp. 8–11, one panel per model | – | CONFIRMED | |
| C-113 | 60 | registered, one look: no | Section 2.0: 0 hits | – | CONFIRMED | |
| C-114 | 60 | CIs on the captioning score: no | Section 2.0: 0 hits | – | CONFIRMED | |
| C-115 | 05_preregistration_and_analysis.md 170; 06_results.md 215, 217 | "the published short-cut account" | Section III-C p. 6 ("short-cut inference"); Finding 5 p. 11 | as C-106 | CONFIRMED | Sections 5.7 and 6.10: no block |

Label error in the evidence file, found while checking this row: `docs/TABLE1B_W5_EVIDENCE.md` cites "§V-A" for the data and the models of Li2025UnveilingICL. In arXiv v1 the experiments are Section IV ("IV. Experiments and Analyses", "A. Datasets and Settings", p. 7) and Section V is the conclusion (block C-9). It is a label in the evidence file, not a cell of the paper, and is not counted in Section 2.4.

Sentences over several works

| id | line | statement in the manuscript | basis | verdict | note |
|---|---|---|---|---|---|
| C-116 | 01_introduction.md 9 | "These analyses are in English." | none of the five analysis papers names the language (Section 2.0); their caption data are COCO, Flickr30K, NoCaps and VizWiz | NOT STATED | true of the data sets; the papers do not say it |
| C-117 | 01_introduction.md 9 | "As far as these papers state, none preregisters its contrasts or reports confidence intervals on the captioning score." | Section 2.0, six papers: 0 hits for registration terms and for "confidence interval"; the SDs of TrueMICL are on its own tasks, the p-values of Baldassini on regression coefficients | CONFIRMED | |
| C-118 | 64 | "mostly in English and with interleaved images" | as C-116 for the language; interleaved example images: C-17, C-55, C-111 | CONFIRMED | the language part falls under C-116 |

### 2.3 Conference version (`conf_taimma_2027/draft_v1/paper.md`)

| id | line / paragraph | statement in the manuscript | basis | verdict | note |
|---|---|---|---|---|---|
| T-01 | 26, p:S1-02 | "As far as those papers state, none preregisters its contrasts or reports confidence intervals on the captioning score, and none covers Vietnamese." | Section 2.0: 0 hits for registration terms, "confidence interval" and "Vietnam" in Yang, W. Li, Baldassini, L. Li, MUNIChus, and in S. Chen (cited in p:S2-02) | CONFIRMED | |
| T-02 | 40, p:S2-02 | another study gives a trained captioner, at the same k, captions retrieved for a different image | C-64 | CONFIRMED | |
| T-03 | 40, p:S2-02 | studies of in-context selection compare similarity-chosen with random examples, with example images [Yang; L. Li] | C-55, C-111 | CONFIRMED | |
| T-04 | 40, p:S2-02 | … "mostly in English" | C-51, C-108 | NOT STATED | as C-116 |
| T-05 | 40, p:S2-02 | multimodal in-context learning is reported to be driven mainly by the text of the examples [Baldassini; S. Chen] | C-81, C-95 | CONFIRMED | (Q) as C-81 |
| T-06 | 42, p:S2-03 | OpenFlamingo: retrieved examples beat random ones on COCO; on Flickr30K lower at the smaller shot counts it reports | C-18, C-19 | CONFIRMED | |
| T-07 | 44, p:S2-04 | MUNIChus compares random with similarity-retrieved examples at equal k in several languages that do not include Vietnamese, and reports point scores | C-29 to C-40 | CONFIRMED | |
| T-08 | 52, p:T1 | Yang row: language "English" | C-51 | NOT STATED | |
| T-09 | 52, p:T1 | Yang row: image-caption pairs; yes, equal shots; "no; no" | C-54, C-55, C-61, C-62 | CONFIRMED | |
| T-10 | 53, p:T1 | W. Li row: language "English" | C-71 | NOT STATED | |
| T-11 | 53, p:T1 | W. Li row: captions, to a trained captioner; yes, equal k; "no; no" | C-68, C-70, C-72, C-78, C-79 | CONFIRMED | |
| T-12 | 54, p:T1 | Baldassini row: language "English" | C-86 | NOT STATED | |
| T-13 | 54, p:T1 | Baldassini row: image-caption pairs; yes, equal shots; "no; no" | C-85, C-87, C-93, C-94 | CONFIRMED | |
| T-14 | 55, p:T1 | L. Li row: language "English" | C-108 | NOT STATED | |
| T-15 | 55, p:T1 | L. Li row: image-caption pairs; yes, equal shots; "no; no" | C-111, C-113, C-114 | CONFIRMED | preprint read, not the TPAMI article |
| T-16 | 56, p:T1 | MUNIChus row: multilingual, no Vietnamese; image, article excerpt and caption; yes, equal k | C-30, C-31, C-34 | CONFIRMED | |
| T-17 | 56, p:T1 | MUNIChus row: registered "not stated" | C-47 | NOT STATED | fill "no" (block T-1) |
| T-18 | 56, p:T1 | MUNIChus row: CIs "no" | C-48 | CONFIRMED | |

### 2.4 Counts

Lines of Sections 2.1–2.3: 169 (counted by script from the verdict column). CONFIRMED 133, WRONG 2, NOT STATED 17, NOT READ 17.

- WRONG (2): C-66 and C-77, both on W. Li et al. 2024.
- CONFIRMED with a qualification (4 of the 133): A-14, C-81, C-82, T-05.
- NOT STATED (17): 13 language cells or language sentences (A-33, C-05, C-51, C-71, C-86, C-97, C-108, C-116, T-04, T-08, T-10, T-12, T-14), one issue that a caption note per table closes; and 4 dash or "not stated" cells that the full text now lets the authors fill (C-06, C-07, C-47, T-17). C-05 is both a language cell and a dash cell.
- NOT READ (17): Rashidi et al. (A-18 to A-25, 8 lines) and RAGCap (C-08 to C-16, 9 lines).
- By manuscript: Paper A 33 lines (24 CONFIRMED, 1 NOT STATED, 8 NOT READ); Paper C 118 lines (97 CONFIRMED, 2 WRONG, 10 NOT STATED, 9 NOT READ); conference version 18 lines (12 CONFIRMED, 6 NOT STATED).

Two quotes (C-19, C-23) sit in a two-column page whose text extraction interleaves the columns; they were read on the page layout and are marked "read on the page". Every other quote was matched by script against the extracted text.

## 3. Proposed text blocks (OLD / NEW)

No block was applied. OLD strings are copied from the files at the shas named at the top.

### 3.1 Paper A, `paper/sec2_related_work.md`

Block A-1 (l.36; removes "read in part": the row is confirmed, A-01 to A-08).

```
OLD: Table 2.1 rests on the main text of each work, except Rashidi et al. (2024), of which only the abstract was read, and S. Liu et al. (2025), read in part.
NEW: Table 2.1 rests on the main text of each work, except Rashidi et al. (2024), of which only the abstract was read; S. Liu et al. (2025) was read in its arXiv version (2407.09735 v3).
```

Basis: the main text of arXiv v3 (Sections 1–6) was read and all 35 pages were searched; the online supplement was not read. If the investigator reads the JASA article and finds the row unchanged, the last clause can be dropped. The Table 2.1 caption (l.20) and the Rashidi row (l.30, "(abstract only)") stay as they are: the full text was not read.

Block A-2 (l.29, optional; qualification A-14).

```
OLD: | Paired bootstrap intervals, Holm correction, a no-flip margin lemma; registered |
NEW: | Paired bootstrap intervals, Holm correction, a no-flip margin lemma; registered, except the cross-task replications, which the authors place outside the registered record |
```

Block A-3 (l.20, optional; A-33). Checked for the Feng row only; the language cells of the Neuhaus, Wei, Fazli and Min rows were not checked.

```
OLD: Each cell describes a work as its authors report it, except the "Statistical guarantee" and last columns, which give our reading;
NEW: Each cell describes a work as its authors report it, except the "Statistical guarantee" and last columns, which give our reading, and "Languages", which gives the language of the data where the authors do not name it;
```

No cell of the S. Liu, Lu or Feng rows needs a change. The source comment at l.14 ("feng2024details (arXiv abstract read)") can be updated to "main text read 2026-11-15 (arXiv v1)"; it is a comment, not paper text.

### 3.2 Paper C, `paper_v1_analysis/02_related_work.md` (every block: apply after shell C2)

Block C-1 (l.9; corrects C-66). Apply after shell C2.

```
OLD: The same study [@Li2024RetrievalRobustness] finds that retrieval-augmented captioners copy tokens from the retrieved captions and are sensitive to their order and selection.
NEW: The same study [@Li2024RetrievalRobustness] finds that SmallCap is robust to the order of the retrieved captions but sensitive to which captions are retrieved, and that tokens shared by most of the retrieved captions are likely copied into its output.
```

Block C-2 (l.30, Table 1 caption; C-05, C-51, C-71, C-86). Apply after shell C2.

```
OLD: The statistics column records CIs or tests on the captioning score. "–" means not stated in the part of the work that was read.
NEW: The statistics column records CIs or tests on the captioning score. A language cell gives the language of the caption data where a paper does not name it. "–" marks the cells of the RAGCap row that its abstract does not settle.
```

Block C-3 (l.49, Table 1, Sarto row; removes "from the abstract", fills three cells; C-01 to C-07). Basis: Sections 1, 3.1–3.3 and 4 of arXiv v1 read, all 22 pages searched; the ACM article itself not read. Apply after shell C2.

```
OLD: | @Sarto2024RetrievalArch, from the abstract | yes | yes | text from an external memory | – (COCO, nocaps) | – | – |
NEW: | @Sarto2024RetrievalArch | yes | yes | captions from an external memory | English (COCO, nocaps) | no | none |
```

The RAGCap row (l.48) keeps "from its abstract" and its three "–" cells: the work was not read.

Block C-4 (l.52, Table 1b caption; C-51, C-71, C-86, C-97, C-108, C-47). Apply after shell C2.

```
OLD: Entries follow each paper's own statement; "–" means not stated or not applicable.
NEW: Entries follow each paper's own statement; a language cell gives the language of the caption data where a paper does not name it, and "no" in the last two columns means that a search of the paper's full text found no such statement.
```

Block C-5 (l.61, Table 1b, MUNIChus row, last three cells; C-47). Apply after shell C2.

```
OLD: | yes, k = 3, examples with image and article excerpt | yes | – | no |
NEW: | yes, k = 3, examples with image and article excerpt | yes | no | no |
```

Block C-6 (l.57, Table 1b, W. Li row; corrects C-77). Apply after shell C2.

```
OLD: | yes, equal k | decoder columns in one table | no | no (mean of three seeds) |
NEW: | yes, equal k | decoder columns in the order tables only | no | no (mean of three seeds) |
```

Block C-7 (l.20, recommended; qualifications C-81 and C-82). Apply after shell C2.

```
OLD: @Baldassini2024MICL find that multimodal in-context learning in open interleaved models is driven mainly by the text of the examples, and that similarity-based example selection does no better than majority voting over the examples' answers; our `nn_cons` baseline, the consensus caption of the k nearest neighbours, is the captioning counterpart of that voting baseline.
NEW: @Baldassini2024MICL find that multimodal in-context learning in open interleaved models is driven mainly by the text of the examples, and that, for classification, similarity-based example selection does no better than majority voting over the examples' answers; for captioning they report that such voting is insufficient and that the example images also contribute. Our `nn_cons` baseline, the consensus caption of the k nearest neighbours, is the captioning counterpart of that voting baseline.
```

No block for 01_introduction.md: its sentences on these works are confirmed; "These analyses are in English." (C-116) is true of the data sets and can stay, or read "These analyses use English caption data." No block for 03_method.md, 05_preregistration_and_analysis.md, 06_results.md, 07_disclosures.md or number_manifest_C.tsv, and none for Sections 5.7 and 6.10. No number of Paper C changes.

### 3.3 Paper C, `docs/TABLE1B_W5_EVIDENCE.md` (apply after shell C2)

Block C-8 (corrects the evidence line behind C-77; adds the versions now read).

```
OLD: | | per-backbone rows | decoder columns in one table | Table 1 (order test); §5.1 uses OPT only |
NEW: | | per-backbone rows | decoder columns in the order tables only | Tables 1 and 2 (order test, COCO and NoCaps; appendix Tables 6 and 7); §5.1 uses OPT only |
```

```
OLD: **Outcome.** None of the five analysis papers preregisters its contrasts or reports CIs (or SD/SE/tests) on the captioning score,
NEW: **Outcome.** None of the six analysis papers (the five above and MUNIChus) preregisters its contrasts or reports CIs (or SD/SE/tests) on the captioning score,
```

Block C-9 (corrects two section labels of the Li2025UnveilingICL rows; arXiv v1 numbering).

```
OLD: | Li2025UnveilingICL (TPAMI; checked on arXiv 2507.08021) | data | COCO | §V-A, p. 7 (Karpathy split) |
NEW: | Li2025UnveilingICL (TPAMI; checked on arXiv 2507.08021) | data | COCO | §IV-A, p. 7 (Karpathy split) |
```

```
OLD: | | models | OpenFlamingo-v2-9B, IDEFICS-9B | §V-A |
NEW: | | models | OpenFlamingo-v2-9B, IDEFICS-9B | §IV-A, p. 7 |
```

A line to add under the first paragraph of the file: "Re-checked 2026-11-15 on the proceedings versions where they are open (NeurIPS 2023 PDF of Yang2023ICLConfig, identical text to arXiv v6; ACL 2024 PDF; the open-access CVPR Workshops PDF and supplement; LREC 2026 PDF of MUNIChus). Chen2025TrueMICL was re-checked on arXiv v2, which carries the COLM 2025 header; Li2025UnveilingICL on arXiv v1 only, the TPAMI article not being open. Record: manuscript/reviews/RELATED_FULLTEXT_CHECK_2026-11-15.md in the run repo."

### 3.4 Conference version, `draft_v1/paper.md` (for the reviser of draft_v2, by paragraph id; apply after shell C2 unless the lead rules that the conference draft is outside that hold)

Block T-1 (p:T1, l.56; T-17).

```
OLD: | [@Chen2026MUNIChus] | multilingual, no Vietnamese | image, article excerpt and caption | yes, equal k | not stated; no |
NEW: | [@Chen2026MUNIChus] | multilingual, no Vietnamese | image, article excerpt and caption | yes, equal k | no; no |
```

Block T-2 (p:T1 caption, l.48, optional; T-08, T-10, T-12, T-14, T-17).

```
OLD: Entries follow each paper's own statements.
NEW: Entries follow each paper's own statements; a language cell gives the language of the caption data where a paper does not name it, and "no" means that a search of the paper's full text found no such statement.
```

Block T-3 (p:S1-02, l.26, optional; ties the sentence to the table, as the corresponding author's answer F6 suggests).

```
OLD: Analyses of this question exist for English and for multilingual news captioning (Sect. 2).
NEW: Analyses of this question exist for English and for multilingual news captioning (Sect. 2, Table 1).
```

## 4. New evidence rows for MUNIChus (proposed text for `docs/TABLE1B_W5_EVIDENCE.md`; apply after shell C2)

In the format of the existing table (paper | cell | value in Table 1b | evidence):

```
| Chen2026MUNIChus (LREC 2026 proceedings, pp. 9008–9017; body text identical to arXiv 2603.10613 v1) | data | MUNIChus (BBC news images with their articles) | §2, p. 9009 ("We developed a Python-based scraper to collect BBC news articles in the languages listed in Table 1"); Table 1, p. 9009 (nine languages; no Vietnamese; "Vietnam": 0 hits) |
| | models | seven MLLMs under prompting, including Qwen2.5-VL-7B, Qwen3-VL-8B and Aya-Vision-8B | Table 2, p. 9012 (Aya-vision-8b, Aya-vision-32b, GPT-4o, Llama-3.2-11B, Phi-3.5-vision, Qwen2.5-VL-7B, Qwen3-VL-8B); §3.2, p. 9011: two models are fine-tuned in a separate condition |
| | equal-k random control | yes, k = 3, examples with image and article excerpt | §3.1.2, p. 9010 ("three randomly sampled examples from the same language's training set"); §3.1.3, p. 9011 (the three training instances most similar to the test image, same format) |
| | per-backbone rows | yes | Table 2, p. 9012: one row per model in each prompting block |
| | registered, one look | no | full-text search: 0 hits for "preregist", "pre-regist", "registered" |
| | CIs on the captioning score | no | Table 2, p. 9012: one BLEU-4 and one CIDEr value per model and language; 0 hits for "±", "std", "standard deviation", "confidence", "bootstrap"; "seed" only in a reference title; the number of random draws is not stated |
```

## 5. What stays unread, and what the investigator would have to fetch by hand

1. **Rashidi, Zobel and Moffat 2024** (Paper A Table 2.1 row and one sentence; 8 lines NOT READ). The article is open access at the publisher according to OpenAlex (status "bronze") and to a co-author's publication page, but https://dl.acm.org/doi/pdf/10.1145/3596511 answers 403 to an automated read. The starting list named a university repository copy: the record https://hdl.handle.net/11343/344016 holds no file (its access field reads "This item is currently not available from this repository"; its file list is empty). There is no arXiv copy. By hand, in a browser: download the PDF from the ACM page and check (a) which test collections and system runs are used (cells "Data and systems", "Needs new labels?"), (b) the form of the judge-error model, (c) that the result on orderings reported as significant is stated in the body as in the abstract, (d) the comparison of AP, NDCG and RBP. Until then the row, the caption note and the sentence of l.36 keep "abstract only".
2. **Bazi, Al Rahhal and Zuair 2025, RAGCap** (Paper C Table 1 row, one sentence, and the label "as used by RAGCap" in Sections 3 and 6.10; 9 lines NOT READ). The TechRxiv preprint (https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.174140786.66325581/v1, CC BY, posted 2025-03-08) and the journal article (doi 10.1080/01431161.2025.2575514, not open access) both need a browser or a library login. To check: caption language of the three data sets, whether any random-example or no-retrieval condition is reported, any statistics on the scores, and the exact prompt layout (image followed by caption per example), which the label in Sections 3 and 6.10 relies on.
3. **L. Li et al., IEEE TPAMI 2026** (doi 10.1109/TPAMI.2026.3719106). Only the 2025 preprint was read. The article appeared a year later, so its text may differ: check Finding 5, the two models, the shot counts, Fig. 9 and whether seeds or intervals were added. Medium priority, because Table 1b and the conference Table 1 say "no; no" for this row.
4. **Sarto et al., ACM TOMM 2024** (doi 10.1145/3663667), **S. Liu et al., JASA 2025** (doi 10.1080/01621459.2025.2474266), **S. Chen et al., COLM 2025** (OpenReview forum n4JdyBGu6T), **Baldassini et al., IEEE Xplore copy**: versions of record not read; an author version was read in each case (arXiv v1 with the ACM reference format; arXiv v3; arXiv v2 with the COLM header; the Computer Vision Foundation copy, which states it is identical to the accepted version). Low priority.
5. **Lu, Zhu and Li 2026**: arXiv v1 is current on 2026-11-15. Re-check version and status on the day Paper A is submitted.
6. **Not covered by this check**: the other rows of Paper C Table 1 (SmallCap, EXTRA, LMCap, CONCAP, MeaCap, EVCap, ViECap, Rebelo et al.) and of Paper A Table 2.1 (Neuhaus and Hein, Wei et al., Fazli et al., Min et al., Molotkov and Artomov, Teisseyre et al.), which the manuscripts do not mark as partly read. Source comments of Paper A Section 2 record that some text sentences outside Table 2.1 rest on an abstract or a title (Fazli et al. quote; Sandhu et al.; Datta and Sundararaman; González-Chávez et al.; Misra et al.); they are not table rows and were not checked here.
7. **draft_v2 of the conference version** was not read (file under 10 minutes old at each of three checks). Blocks T-1 to T-3 are written against draft_v1.

## 6. The starting list against what was found

The list from the corresponding author's answer F6 was input to verify. Confirmed: the open arXiv copies of S. Liu (v3), Lu (v1, still a preprint), Sarto (v1), OpenFlamingo (v2, the current version, Table 9 numbers as printed in Paper C) and MUNIChus (v1); the four fills of the Sarto row; the MUNIChus cells; that the evidence file lacks MUNIChus. Not confirmed: a university repository copy of Rashidi et al. (the record holds no file); the open TechRxiv copy of RAGCap exists but could not be read by an automated request. One point beyond the list: the Sarto paper does not name the language of its data, so "English" is a statement about COCO and nocaps, not a quotation.
