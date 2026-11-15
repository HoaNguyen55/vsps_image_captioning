# Paper A fix package v3, related-work rows

Written 2026-11-15T01:31Z (2026-11-15, 08:31 Vietnam time). Target journal of the paper: Signal Processing: Image Communication.

**What this file is.** Two proposed text changes to Table 2.1 and its note in Section 2 of Paper A, each as an exact OLD/NEW pair with its evidence, for a judge to read before anything is applied. Nothing has been applied, staged or committed. They follow from the full-text check of the related-work rows (`manuscript/reviews/RELATED_FULLTEXT_CHECK_2026-11-15.md`, sha256 `8fa296ddedd5dac7ca42e58a5e2fc1aefcfb0fb795b974b9ba08333f8b1e1f81`; ids such as "A-14" below are the verdict lines of that file). The package settles part of item N-13 of fix package v1 (item D-5 of package v2.1): one of the two works that Table 2.1 described from partial reading has now been read, and the status of the concurrent manuscript has been checked.

**State the OLD strings were checked against.**
- Paper: `/mnt/d/vsps_papers/vsps-paperA-spic/paper/sec2_related_work.md`, read with `git show`, at `dafba17` (`dafba17e543c94f600d16fe0c74b0cb8f7d178b4`) and at the present HEAD `ea12e51` (`ea12e51270804d0c8cd54b208e1946085d4a2b4d`, the commit of fix package v2 under CC-407, made while this package was being written). The file is byte-identical at both: sha256 `de85f341f07c90b09d90164abcaec474f0f78c80ea1353cf7f2c3455a9d5b080`.
- **One file changes:** `paper/sec2_related_work.md`. It is not among the twelve files of package v2 and v2.1 (`V2_PROGRESS.md`, `abstract_A.md`, `anon/declarations_anon.md`, `declarations.md`, `number_manifest.tsv`, `sec10_discussion.md`, `sec11_limitations_ethics.md`, `sec3_measurement_setup.md`, `sec4_theory.md`, `supplementary.md`, `supplementary_SPIC.md`, `supplementary_provenance_internal.tsv`), and commit `ea12e51` changed exactly those twelve. So no OLD string of this package lies in a file that package v2 touches.
- **Custody zones.** Section 6.7 (`sec7_verbosity_sign.md`), Supplementary S11 (both supplement files), the abstract (`abstract_A.md`) and the highlights (`highlights_A.md`) are not written; the apply script asserts that the only file it produces is `paper/sec2_related_work.md`. No text of Section 6.7 or S11 was opened for this package.
- **The length block of `abstract_A.md` stays exact.** Both NEW strings have the same number of words as their OLD strings, so the file keeps its 2,184 words and the main text its 18,927 (method of the length block: comments stripped, whitespace split, tables included). The script asserts the equal word count.

**Inputs.** The check file named above and the public full texts it lists; `sec2_related_work.md`; the file lists of `apply_a_v2.py` and `apply_a_v2_1.py`; `A_CUT_PLAN_v1.md` (its moves 57 to 59 and its point 5 on Table 2.1); `paper/build/prep.py` (the citation pattern of the build, imported by the script, not run as a script).

## 1. Counts

- 2 blocks in 1 file. A3-L01 removes "read in part". A3-L02 is a recommended qualification that a judge may strike.
- Rows that keep their note: Rashidi et al. (2024), "described from its abstract only" (Table 2.1 caption, l.20; row, l.30; sentence, l.36). Its full text could not be read.
- Not in this package: 4 items (section 4). For the investigator: 3 items (section 4).
- Main text: 18,927 words before and after.

## 2. Table of blocks

| Id | Check line | File | Line at HEAD | What changes | Status |
|---|---|---|---|---|---|
| A3-L01 | A-01 to A-08 | `paper/sec2_related_work.md` | 36 | the sentence on what Table 2.1 rests on: S. Liu et al. (2025) is no longer "read in part"; it was read in its arXiv version. The cells of its row are confirmed and unchanged | BLOCK |
| A3-L02 | A-14 (qualification) | `paper/sec2_related_work.md` | 29 | Lu et al. (2026) row, "Statistical guarantee": "registered" becomes "partly registered" | BLOCK (recommended; a judge may strike it) |
| – | A-09 | `paper/sec2_related_work.md` | 29 | Lu et al. (2026), label "(preprint)" | CHECKED, no text: still arXiv v1 on 2026-11-15 |
| – | A-18 to A-25 | `paper/sec2_related_work.md` | 12, 20, 30, 36 | Rashidi et al. (2024): row, caption note, sentence | NOT CHANGED: work not read |

The apply script holds pinned targets for both blocks together and for A3-L01 alone.

## 3. Blocks

### A3-L01. S. Liu et al. (2025): the row rests on the main text (check lines A-01 to A-08)

The main text of the work was read in its arXiv version and every cell of its row in Table 2.1 is confirmed (section 5.2 lists them). The sentence keeps the note for Rashidi et al. (2024). OLD and NEW have 31 words each.

```text
<<<A3-L01 paper/sec2_related_work.md OLD>>>
Table 2.1 rests on the main text of each work, except Rashidi et al. (2024), of which only the abstract was read, and S. Liu et al. (2025), read in part.
<<<A3-L01 paper/sec2_related_work.md NEW>>>
Table 2.1 rests on the main text of each work, S. Liu et al. (2025) in its arXiv version, except Rashidi et al. (2024), of which only the abstract was read.
<<<A3-L01 EVIDENCE>>>
Source: Liu, Yeh, Zhang, Tian and Li, arXiv 2407.09735 v3 of 2025-02-24 (https://arxiv.org/pdf/2407.09735v3, sha256 2a932e76f7e8…, 35 pages). Read: the main text, Sections 1 to 6; all pages searched. Not read: the online supplement (proofs, further simulations) and the journal article (JASA 120(552), doi 10.1080/01621459.2025.2474266, not open access).
Why "in its arXiv version" stays in the sentence: the reference list gives the journal article, and the text read is the preprint. v3 is a revised manuscript; its acknowledgements say: "We sincerely thank the joint editor and associate editor for their time and effort in overseeing the review of this manuscript".
Row, question ("when SCAR fails"): abstract, p. 1; quote: "the labeled and unlabeled positive data can be from different distributions"; Section 6, p. 30; quote: "the CD assumption is equivalent to the SCAR assumption".
Row, data ("Simulations; one tabular data set"): Section 5.1, p. 21; Section 5.2, p. 27; quote: "We consider the Mobile Phone Dataset from the Kaggle".
Row, gold ("Class labels, partly hidden"): Section 1.1, p. 2; quote: "the second sample is unlabeled, meaning we can only access the features x but have no access to their labels y".
Row, guarantee: Theorem 3, Section 4.1, p. 20 (chi-square limits of the two likelihood-ratio statistics); quote: "we can also construct the ELR-based confidence interval for the mixture proportion π".
Row, last column ("No evaluation metric is studied"): 0 hits for "caption", "F1", "F-measure", "hallucinat", "metric" in the whole text.
Sentence at l.12 ("tests of that assumption exist"): abstract, p. 1; quote: "developing a goodness-of-fit test for the CD assumption and constructing confidence intervals for the proportion of positive instances in the target domain".
Build: the citation pattern of paper/build/prep.py finds the same mentions before and after (73 in the file; "S. Liu et al. (2025)" resolves by its initial, "Rashidi et al. (2024)" as before); in the numbered style the sentence reads "S. Liu et al. [n] in its arXiv version, except Rashidi et al. [m], of which only the abstract was read".
A shorter NEW is possible: end the sentence after "was read" and drop the clause on S. Liu et al. It has 8 words fewer, so the length block of abstract_A.md would then need its two counts changed, which is outside this package.
<<<A3-L01 END>>>
```

### A3-L02. Lu et al. (2026): which part is registered (check line A-14; recommended)

The cell says "registered" without limit. The "Data and systems" cell of the same row lists TACRED revisions, translation, retrieval, QA and code, and the authors place exactly these cross-task replications outside their registered record. The column is one of the two that give this paper's own reading (Table 2.1 caption). OLD and NEW have 12 words each: the article before "no-flip" is dropped so that the word count of the file does not change. The sentence at l.36 ("in a registered study of structured prediction") stays: the gold-exchange study on document relation extraction is registered.

```text
<<<A3-L02 paper/sec2_related_work.md OLD>>>
| Paired bootstrap intervals, Holm correction, a no-flip margin lemma; registered |
<<<A3-L02 paper/sec2_related_work.md NEW>>>
| Paired bootstrap intervals, Holm correction, no-flip margin lemma; partly registered |
<<<A3-L02 EVIDENCE>>>
Source: Lu, Zhu and Li, arXiv 2611.04099 v1 of 2026-11-03 (sha256 944c72ed864b…, 23 pages). Status on 2026-11-15 (export.arxiv.org): v1 only, comment "23 pages. Submitted to TACL", no journal reference; the label "(preprint)" of the row is correct.
Registered: Section 4.1, p. 5; quote: "All experiments follow a preregistration document frozen before any training or download". The gold exchange on document relation extraction, quote: "Two gold versions, gD and gR (revised projection of Tan et al., 2022b), instantiate the gold-revision lever"; the UD probe, Table 19, p. 23, "separately preregistered".
Outside the registration: Section 4.4, p. 8, on retrieval, translation, QA, code and the released-gold audits (among them the TACRED revisions); quote: "observational breadth for Props. 1–2, outside the preregistered ledger".
Unchanged parts of the cell: Section 4.1, p. 5, document-paired bootstrap and "The three preregistered comparisons (Holm(3))"; Section 3.3, p. 4, and Appendix B, p. 19, "Lemma B: no-flip margin guarantee".
If the judge strikes this block, the cell stays as it is; the script holds a target for A3-L01 alone.
<<<A3-L02 END>>>
```

## 4. Not changed, not in this package, and what needs the investigator

**Not changed, because the work was not read (8 check lines, A-18 to A-25).** Rashidi, Zobel and Moffat (2024): the row (l.30), the caption note (l.20), the note in l.36 and the sentence at l.12 stay. The abstract, read on the record page of the University of Melbourne repository, agrees with the row and the sentence. That record holds no file, and there is no arXiv copy.

**Not in this package:**
- The caption of Table 2.1 says each cell is "as its authors report it"; the language cell of the Feng et al. row is not stated in that paper (check line A-33). A caption note on the "Languages" column needs the other rows checked first and adds words; it is left for the rewrite or for the move of the table.
- The source comment at l.14 ("feng2024details (arXiv abstract read)") could say that the main text was read on 2026-11-15; it is a comment, not paper text.
- The other parts of item N-13: one more row for the source of the certificate, and the two reference keys whose year differs from the `.bib` entry.
- `A_CUT_PLAN_v1.md` plans to move Table 2.1, its caption and the last sentences of the paragraph "Position of this paper" to Supplementary S9 (moves 57 to 59), and its point 5 asks that the two works read in part be read in full first. After this package one of the two is done and Rashidi et al. remains. If the move is made later, the changed sentence and cell move with the table.

**Needs the investigator:**
1. Rashidi et al. (2024), by hand in a browser: https://dl.acm.org/doi/pdf/10.1145/3596511 (open access at the publisher according to OpenAlex and to a co-author's publication page; the site answers an automated read with HTTP 403). To check: the test collections and system runs (cells "Data and systems", "Needs new labels?"), the form of the judge-error model, and that the result on orderings reported as significant stands in the body as in the abstract. Until then "abstract only" stays.
2. S. Liu et al. (2025), the JASA article: optional. If it is read and the row holds, the clause "S. Liu et al. (2025) in its arXiv version" can go at the rewrite.
3. Lu et al. (2026): check the arXiv version and status again on the day of submission.

## 5. Checks run

### 5.1 OLD occurs exactly once (every block)

| Id | File | Count of OLD at dafba17 | Count of OLD at ea12e51 (HEAD) | Count when the blocks are applied in id order | Exactly once |
|---|---|---|---|---|---|
| A3-L01 | `paper/sec2_related_work.md` | 1 | 1 | 1 | yes |
| A3-L02 | `paper/sec2_related_work.md` | 1 | 1 | 1 | yes |

### 5.2 Other checks (all in memory; no paper file was written)

- Paper HEAD at the time of the checks: `ea12e51`; `git status --porcelain -- paper/sec2_related_work.md` empty; the file at HEAD is byte-equal to its `dafba17` text.
- Every NEW string occurs exactly once after application; applying the two blocks in the reverse order gives a byte-equal file; exactly two lines of the file change (29 and 36).
- Words of `sec2_related_work.md` by the method of the length block: 2,184 before, 2,184 after (A3-L01: 31 and 31 words; A3-L02: 12 and 12). The length block of `abstract_A.md` at HEAD says "sec2_related_work.md 2,184" and "Main text now: 18,927 words"; both stay true.
- Number tokens of the file: equal multisets before and after. No manifest row is needed.
- Citation mentions by the pattern of `paper/build/prep.py` (`MENTION`, comments blanked): 73 before, 73 after, the same list of (initial, surname, year). No reference is added or lost. The numbered-citation step of the build (`numcite_text`) turns the NEW sentence into "… of each work, S. Liu et al. [n] in its arXiv version, except Rashidi et al. [m], of which only the abstract was read."
- The four strings that carry the note on Rashidi et al. (caption, row label, the cell "(abstract only)", the clause of l.36) occur once before and once after.
- Cells of the S. Liu et al. row, all confirmed on the main text and unchanged: question; "Simulations; one tabular data set"; "Class labels, partly hidden"; "No"; "Empirical-likelihood ratio test with a chi-square limit; confidence interval for the positive share"; "Not applicable"; "No evaluation metric is studied; we test a metric's behaviour, not a labelling model".
- Custody: the script produces `paper/sec2_related_work.md` and nothing else.
- Quotes: every string given as a quote from a cited work in the evidence lines was found by script in the text extracted from the PDF named there; none is longer than 25 words.
- Default mode of `apply_a_v3_related.py` on the present tree: both OLD strings once, all content checks passed, the result equals the target below, nothing written.

sha256 of the file before and after (the apply script holds the same values as `PRE` and `TARGETS`):

| File | at dafba17 and at ea12e51 | after both blocks | after A3-L01 alone |
|---|---|---|---|
| `paper/sec2_related_work.md` | `de85f341f07c90b09d90164abcaec474f0f78c80ea1353cf7f2c3455a9d5b080` | `5beb9da16eec16b2c7afb67bb3512fa3422ea0b9e0a4e85fd311ed30224a38c4` | `e901f2b3081634abd1e163946a807275f85af4ec5cc3730e7e547cebd4797400` |

### 5.3 The apply script

`apply_a_v3_related.py` in this folder reads the blocks from this file (pinned by sha256), requires that `dafba17` is an ancestor of HEAD and that `paper/sec2_related_work.md` is clean against HEAD and equals its `dafba17` text, rebuilds the file in memory from `git show HEAD:`, runs the checks of section 5.2 and prints the resulting sha256. In its default mode it writes nothing. It writes the file only with `--write --ruling <id>`, only if the result equals the pinned target, and only if nothing is staged in the paper repository, so that the package is a commit of its own. If a judge changes a NEW text, the pin and the targets must be recomputed.

### 5.4 What was opened for this package, and what was not checked

- Opened: `paper/sec2_related_work.md`; the first lines of `paper/abstract_A.md` (the length block, a comment); `paper/build/prep.py`; `paperA.bib` (three entries); `citation_map_A_v2.tsv` and `intext_trace_A.tsv` (lines naming the three works); the two apply scripts and the packages of v1, v2 and v2.1 for item N-13 and their file lists; `A_CUT_PLAN_v1.md` for Table 2.1. A count of the names Rashidi, S. Liu and Lu in the other paper files found none, so no line of Section 6.7 or of Supplementary S11 was read.
- Not opened: any label folder, key file, assignment file or label file; the held Paper B folders.
- Not checked: the build of the PDF, the manifest check and the scrub of the supplement were not run, because nothing was applied and the package touches neither the supplement nor a number.
