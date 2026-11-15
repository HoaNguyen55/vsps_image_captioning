# Paper C (journal version, ACM TALLIP): fix package v2

Prepared 2026-11-15 (UTC). Nothing in this package has been applied, staged or committed. It is for a judge to read first.

## 0. Scope, state it applies to, and conventions

- **Applies to "HEAD after shell C2".** The paper repo is at `9b8e6ae` (package v1 applied under CC-405). The freeze transfer `c_attr_c2_transfer.py` (sha256 `030c369d…`) runs on 2026-11-16 after 05:00Z and needs `03_method.md`, `05_preregistration_and_analysis.md`, `06_results.md`, `07_disclosures.md` and `number_manifest_C.tsv` equal to HEAD. This package is therefore applied only after the shell C2 commit, in one commit of its own. No file of it may sit in the working tree before C2 runs.
- **How "HEAD after shell C2" was built for the checks.** The four section files that C2 changes were built in memory from `git show 9b8e6ae:` with the script's own `swap` calls and its `c2a_text` on the pinned text package (`e3820d3b…`). Their text does not depend on the K7 line, so the result is exact. The manifest after C2 is the `9b8e6ae` manifest plus two appended rows; one of them carries the stamp and id of the K7 line, which do not exist yet, so the manifest has no fixed sha256 here and is checked by structure (section 7).
- **Inputs.** Answers C1 to C5 of the corresponding author (read-only copy `manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_7e8f958d.md`; only those five answers were read, and no personal data of that file is copied here). Ruling CC-405 (`.session_backup/2026-10-13/decisions/CC-405.txt`), open points N1 to N9.
- **Block format** as in v1: the OLD string is the text between the `OLD>>>` line and the `NEW>>>` line, without the line break that ends it; the NEW string likewise, up to the `EVIDENCE>>>` line; an `END>>>` line closes the block. Block ids are `C-V01` … `C-V08`.
- **Apply script:** `manuscript/fix_packages/2026-11-15_C/apply_c_v2.py`, prepared and not run. It refuses to write unless the tree is exactly "HEAD after shell C2", every OLD occurs once, and the results equal the targets of section 7.
- **Custody.** Development-set material and registrations only. No test-set score book, per-image ledger, caption file, label file or key file was opened. No dataset caption and no model output is printed. The prompt template of C-V03a is the study's own instruction text.

## 1. Table of items

| id | source | file | what | status |
|---|---|---|---|---|
| C-V01 | answer C1; CC-405 N7 | `00_abstract.md` | new abstract with InternVL3's COCO row; "images" becomes "entries" | BLOCK |
| C-V02a | answer C3; CC-405 N1 (Annex B) | `04_data_and_splits.md` | entries against distinct images of OV-test, as ruled | BLOCK |
| C-V02b | answer C3 (note at Table 3) | `04_data_and_splits.md` | one sentence under Table 3 | BLOCK (wording not yet ruled; optional) |
| C-V03a | answer C5 (ii) | `11_supplement_registered_rows.md` | the prompt template in full, Vietnamese and English | BLOCK |
| C-V03b | answer C5 (ii) | `03_method.md` | pointer from Section 3.3 | BLOCK |
| C-V03c | answer C5 (ii) | `08_english_comparison.md` | pointer from Section 8.1 | BLOCK |
| C-V04 | answer C4, adopted part; follow-up F3 | `05_preregistration_and_analysis.md` | paragraph in Section 5.4: why interval rules and not p-values | BLOCK |
| C-V05a | CC-405 N2 | `04_data_and_splits.md` | what the filters of OV-dev-A/B and KTVIC dev299 compare against | BLOCK |
| C-V05b | CC-405 N2 | `08_english_comparison.md` | the same for the 997 Flickr30K test images, in the registration's words | BLOCK |
| C-V06 | CC-405 N3 | `V2_PROGRESS_C.md` | "under review" becomes "in preparation" | BLOCK |
| C-V07 | CC-405 N5 (C-N07) | `06_results.md` | how the "exploration halves" were defined | BLOCK |
| C-V08 | CC-405 N6 | `01_introduction.md` | roadmap clause for Sections 6.10 and 6.11, as ruled | BLOCK |
| C-R01 | CC-405 N4; answer C2 | `05`, `06`, `08`, `09`, `11` | Tables 10 to 18 renumbered by one scripted pass, 41 labels | OPERATION (section 3) |
| C-M01 | CC-405 N1 | `number_manifest_C.tsv` | rows 71 and 73 restored | OPERATION (section 4) |
| – | CC-405 N8 | `06_results.md` | Table 17 rows after C2 | CHECKED, no text (section 5) |
| – | CC-405 N9 | – | evidence slip of v1, C-F13 | RECORD (section 5) |
| – | CC-405 N5: reference for the Open Images V7 labels; C-N15 reading | `paperC.bib`, `02` | needs the network | DEFERRED (section 6) |
| – | answer C5 (i): release of per-image scores | `01`, `09`, `10` | waits for the check of the dataset terms | DEFERRED (section 6) |
| – | answer C4, second part: post hoc p-like column in the supplement | – | not adopted | NOT DONE (section 6) |
| – | answer C2: shorter Sections 5.7 and 6.10 | – | plan only, in `C_CUT_PLAN_v1.md` | PLAN |

Counts: 12 OLD/NEW blocks under 8 ids, 1 renumbering operation (41 labels in 5 files), 1 manifest operation (2 rows edited, none added).

## 2. Blocks

### C-V01. Abstract: InternVL3's COCO row restored (answer C1), "entries" (CC-405 N7)

At HEAD the abstract gives the pooled COCO number with PASS and no per-backbone row, while `07_disclosures.md` (Box 2 and the deviation summary) says that the abstract quotes InternVL3's COCO row, labelled as a reported row. The corresponding author chose to restore the row. The OLD paragraph has 193 words; the NEW one has 198 (whitespace-separated tokens, the count `wc -w` gives).

Word budget: +10 for the clause on InternVL3's row; −5 by four trims that change no statement ("the captions" → "captions"; "may, however, reflect" → "may reflect"; "an equal number of" → "equally many"; "was already present" → "was present"). "(1,941 images)" becomes "(1,941 entries)".

```text
<<<C-V01 00_abstract.md OLD>>>
Retrieval in-context captioning shows a multimodal model the captions of memory images similar to the query and needs no training, which suits low-resource languages such as Vietnamese. A gain over zero-shot prompting may, however, reflect in-domain caption style rather than retrieval. A preregistered evaluation with one look per test set compares retrieved captions with an equal number of random captions from the same memory and reports each backbone separately. On OpenViIC test (1,941 images), retrieved examples beat random ones by +4.49 [3.52, 5.57] stripped CIDEr-D points pooled (registered PASS), carried mainly by Qwen2.5-VL and not detected for InternVL3. On XM3600 Vietnamese the gain was not detected (+0.70 [−0.45, 1.97]; FAIL, CI including zero). With frozen configurations, COCO Karpathy test replicated a known English pattern (+3.08 [2.08, 4.03] PTB CIDEr-D; PASS); on NoCaps the point, +1.73 [0.94, 2.50], fell below the registered +2.0 threshold (FAIL). On Flickr30K test, retrieval prompting scored +28.77 to +37.87 PTB CIDEr-D points above a re-implemented training-free baseline, LMCap, for three backbones, yet most of InternVL3's margin was already present zero-shot. The focus is empirical and practical: crediting a gain to retrieval requires an equal-k random control and per-backbone results.
<<<C-V01 00_abstract.md NEW>>>
Retrieval in-context captioning shows a multimodal model captions of memory images similar to the query and needs no training, which suits low-resource languages such as Vietnamese. A gain over zero-shot prompting may reflect in-domain caption style rather than retrieval. A preregistered evaluation with one look per test set compares retrieved captions with equally many random captions from the same memory and reports each backbone separately. On OpenViIC test (1,941 entries), retrieved examples beat random ones by +4.49 [3.52, 5.57] stripped CIDEr-D points pooled (registered PASS), carried mainly by Qwen2.5-VL and not detected for InternVL3. On XM3600 Vietnamese the gain was not detected (+0.70 [−0.45, 1.97]; FAIL, CI including zero). With frozen configurations, COCO Karpathy test replicated a known English pattern (+3.08 [2.08, 4.03] PTB CIDEr-D; PASS), although InternVL3's reported row was below zero (−1.64 [−2.79, −0.49]); on NoCaps the point, +1.73 [0.94, 2.50], fell below the registered +2.0 threshold (FAIL). On Flickr30K test, retrieval prompting scored +28.77 to +37.87 PTB CIDEr-D points above a re-implemented training-free baseline, LMCap, for three backbones, yet most of InternVL3's margin was present zero-shot. The focus is empirical and practical: crediting a gain to retrieval requires an equal-k random control and per-backbone results.
<<<C-V01 EVIDENCE>>>
Decision: answer C1, final decision (a): restore InternVL3's COCO row (-1.64 [-2.79, -0.49]) in the abstract and trim the surrounding words to stay under 200.
Row: .session_backup/machines/M3/root/outputs/c_en/decide_coco_test.json::scored.coco_test_5000.per_model.internvl3_8b.ret_minus_rand d -1.6426, lo -2.7931, hi -0.4899; manifest rows 3178, 3179, 3180 (status c-en-reported). Their used_in column already names 00_abstract.md, so no manifest edit is needed for this block.
Label: "reported row" is the label of the same row in 01_introduction.md l.31 ("a reported row, not registered") and 10_conclusion.md l.5; 07_disclosures.md l.28 says the abstract quotes the row "as descriptive context, labelled as a reported row". Body: 08_english_comparison.md l.43 ("a CI wholly below zero").
No claim stronger than the body: every other number of the paragraph is unchanged from HEAD; no number is added besides the three above. Qwen2.5-VL's COCO row (+7.80) is not printed: the body calls "carried by Qwen2.5-VL" on COCO a descriptive reading (08 l.43), and Section 7 asks only for InternVL3's row. The analysis part of answer C1 suggests printing Qwen2.5-VL's point beside it; that costs two more words (200 exactly) and is left to the investigator.
"entries": CC-405 N7; the registration counts 1,941 entries with 1,937 distinct images (C-V02a). Manifest row 4 (1941) names 00_abstract.md.
Venue (venue-tallip skill): abstract 150-200 words, no first person, no citations. NEW has 198 words, no first-person word and no citation; the apply script asserts all three.
Not in this block: CC-405 C-N10 (a design clause that InternVL3's registered arm includes the deletion step). It is the investigator's item with the default "no change", and the corresponding author's answers do not cover it. Two words of budget remain.
After this block the two sentences of Section 7 (07 l.17 and l.28) are true as written; 07 is not changed.
<<<C-V01 END>>>
```

### C-V02a. OV-test: entries against distinct images (answer C3; CC-405 N1, Annex B)

OLD and NEW are the strings of CC-405 Annex B, copied by script from the ruling file.

```text
<<<C-V02a 04_data_and_splits.md OLD>>>
**OpenViIC test.** Each of the 2,001 test entries is kept with its own references and is one bootstrap unit.
<<<C-V02a 04_data_and_splits.md NEW>>>
**OpenViIC test.** The 2,001 test entries hold 1,997 distinct images: four pairs of entries are byte-identical files, kept as separate entries by the test registration. None of the eight is among the 60 images excluded below, so the 1,941 entries of the primary set hold 1,937 distinct images. Each of the 2,001 test entries is kept with its own references and is one bootstrap unit.
<<<C-V02a EVIDENCE>>>
Ruled text: CC-405 Annex B, l.241 (OLD) and l.243 (NEW), copied byte for byte.
Registration: prereg/2026-10-25_c_test/PREREG.md (sha256 prefix acecd6527217) §3.1 l.74 ("OV-test has 2,001 entries but 1,997 distinct images (sha256): 4 byte-identical pairs ... None of the 8 is in the 60, so the primary has 1,941 entries / 1,937 distinct images. Both entries of a pair are kept, each with its own references, and each entry is one bootstrap unit") and l.365.
Log: .session_backup/2026-10-26/c_test/CHAIN.log (sha256 prefix fc543266fcc6) l.33 "staged: 2001 files, sha OK 2001/2001, distinct sha 1997".
Manifest: operation C-M01 (section 4) restores rows 71 (1997) and 73 (1937). "four" and "eight" are words; row 72 stays as it is (CC-405 Annex B).
<<<C-V02a END>>>
```

### C-V02b. A short note at Table 3 (answer C3; wording not yet ruled, optional)

Answer C3 asks for the sentence of Section 4 "with a short note at Table 3". CC-405 ruled only the sentence. This block is that note; a judge may strike it.

```text
<<<C-V02b 04_data_and_splits.md OLD>>>
The English sets of the COCO and NoCaps arm are described in Section 8.1, and the three Flickr30K sets in Section 8.6.
<<<C-V02b 04_data_and_splits.md NEW>>>
The English sets of the COCO and NoCaps arm are described in Section 8.1, and the three Flickr30K sets in Section 8.6. In the two OpenViIC test rows the count is of test entries; the distinct images are counted in the paragraph on OpenViIC test below.
<<<C-V02b EVIDENCE>>>
Answer C3, final decision: the sentence in Section 4 "with a short note at Table 3". The note adds no number and points to the paragraph that C-V02a changes; if C-V02a is not applied, this block must not be applied either.
<<<C-V02b END>>>
```

### C-V03a. The prompt template in full, in the supplement (answer C5 (ii))

The eight template strings below were written into this file by script from the two pinned code files, read by syntax tree with nothing executed, and the apply script compares them again byte for byte.

```text
<<<C-V03a 11_supplement_registered_rows.md OLD>>>
Processor settings are those pinned with each snapshot.
### Context from published systems (Section 8.7)
<<<C-V03a 11_supplement_registered_rows.md NEW>>>
Processor settings are those pinned with each snapshot.

**Prompt template (Sections 3.3 and 8.1).** The in-context prompt is the header, k example lines and one tail, joined by line breaks, and it follows the image in the user turn. In an example line, {i} is the number of the example, from 1 to k, and {caption} is the shown caption of that example with its whitespace collapsed. The table prints the template in full, as it stands in the pinned code; it holds no dataset caption. The Vietnamese template is used by every Vietnamese text-example arm of the paper, and the English one, its direct translation, by every English text-example arm of Section 8. Each template is pinned by the sha256 of the UTF-8 bytes of its JSON form, `json.dumps` of the object with the keys "header", "line" and "tails" (T1, T2), with `ensure_ascii=False` and `sort_keys=True`.

| part | Vietnamese template | English template |
|---|---|---|
| header | Dưới đây là chú thích của một vài bức ảnh khác. Các chú thích này chỉ cho thấy cách viết, chúng không mô tả bức ảnh cần chú thích. | Below are captions of a few other images. These captions only show the writing style; they do not describe the image to be captioned. |
| example line | Ví dụ {i}: {caption} | Example {i}: {caption} |
| tail T1 | Hãy viết chú thích cho bức ảnh này bằng MỘT câu tiếng Việt ngắn gọn, theo cách viết của các ví dụ. Chỉ nêu những gì thực sự nhìn thấy trong ảnh. Không liệt kê, không giải thích. | Write a caption for this image in ONE short English sentence, in the style of the examples. Only state what is actually visible in the image. Do not list items or explain. |
| tail T2 | Hãy viết chú thích cho bức ảnh này bằng MỘT câu tiếng Việt ngắn gọn, theo cách viết của các ví dụ. Không liệt kê, không giải thích. | Write a caption for this image in ONE short English sentence, in the style of the examples. Do not list items or explain. |
| sha256 of the template | `7478361a133cf3944ce4e9952fd32cd97660cd747cb2f45bfdda30cd8a4a3a00` | `b329e57a62d67a5afa62ff04503ed30992028839eb65284c3c6cae93a64ed713` |

### Context from published systems (Section 8.7)
<<<C-V03a EVIDENCE>>>
Decision: answer C5, final decision 2: print the whole template (Vietnamese header, the numbered example line, both tails, the English translation of Section 8 and the sha256 of each).
Vietnamese: scripts/c_stage1/decode_icl.py, sha256 fa5a251160d4fd4fb0cd130af33614283863a84e6ed7905f3da81bb6255010db (equal to its line in manuscript/prereg/2026-10-22_c_stage1/SHA256SUMS), HEADER l.48-49, LINE l.50, TAILS l.51-56, TEMPLATE_SHA256 l.57 = 7478361a133cf3944ce4e9952fd32cd97660cd747cb2f45bfdda30cd8a4a3a00; hash rule l.65-66; prompt assembly l.194-196 ("\n".join([HEADER, *lines, TAILS[tpl]])). The same four strings are printed in the registration, prereg/2026-10-22_c_stage1/DESIGN.md §4.1 l.161-174 (sha256 prefix eacc9a9c737c), with "Prompt = HEADER, k LINEs and the tail, joined by newlines" and "An example caption is shown with its whitespace collapsed".
English: scripts/c_en/cen_decode.py, sha256 777a5af03e9f1f61d5de638747c8e18cd5b4e528de0bdba745a621f2903a3885 (equal to its line in scripts/c_en/SHA256SUMS), HEADER l.41-42, LINE l.43, TAILS l.44-49, EN_TEMPLATE_SHA256 l.50 = b329e57a62d67a5afa62ff04503ed30992028839eb65284c3c6cae93a64ed713; named in prereg/2026-10-27_c_en/PREREG.md l.50 ("direct English translations").
Check made here: both template hashes were recomputed from the strings read by syntax tree and equal the two pins. The later code (stage 2, the test, the ablations, the Flickr30K tiers and the attribution study) imports these two modules and asserts both pins (for example scripts/c_t3/c_t3.py l.1311, scripts/c_attr/c_attr.py l.1473).
No dataset caption and no model output: the strings are the study's own instruction text; {caption} is a placeholder.
Not covered, on purpose: the zero-shot prompt (it belongs to the companion studies' kit; section 6), the prompt of the interleaved image-caption arm, and LMCap's own prompt.
The OLD takes in the heading line that follows, so that a blank line stands before the heading after the insertion (at HEAD the heading follows the paragraph with no blank line).
Build note: the table has long cells; if the monospace or table font of the build lacks Vietnamese glyphs, the strings must stay in the text font. Not tested here (the LaTeX build is outside this package).
<<<C-V03a END>>>
```

### C-V03b. Pointer from Section 3.3

```text
<<<C-V03b 03_method.md OLD>>>
and is pinned by its sha256 in the code to be released (prefix `7478361a`).
<<<C-V03b 03_method.md NEW>>>
and is pinned by its sha256 in the code to be released (prefix `7478361a`); it is printed in full in the supplement ("Instrument definitions").
<<<C-V03b EVIDENCE>>>
Follows from C-V03a; apply only with it. The OLD is in Section 3.3 (03_method.md l.31) and is far from the anchor of shell C2 in this file (the "Other registered arms" paragraph, l.132).
<<<C-V03b END>>>
```

### C-V03c. Pointer from Section 8.1

```text
<<<C-V03c 08_english_comparison.md OLD>>>
The prompt header, example line and tails are direct English translations, pinned by hash.
<<<C-V03c 08_english_comparison.md NEW>>>
The prompt header, example line and tails are direct English translations, pinned by hash and printed in the supplement ("Instrument definitions").
<<<C-V03c EVIDENCE>>>
Follows from C-V03a; apply only with it. 08_english_comparison.md l.7.
<<<C-V03c END>>>
```

### C-V04. Section 5.4: why the registered rules read intervals and not p-values (answer C4, the adopted part)

Adopted: one explanatory paragraph. Not adopted: any post hoc p-value or p-like column; nothing was computed and no score file was opened. The corresponding author's answer to follow-up F3 agrees with both points.

```text
<<<C-V04 05_preregistration_and_analysis.md OLD>>>
The Flickr30K registration decides with a registered p-like bootstrap statistic, described in Section 8.6.
<<<C-V04 05_preregistration_and_analysis.md NEW>>>
The Flickr30K registration decides with a registered p-like bootstrap statistic, described in Section 8.6.

**Why the registered rules read intervals and not p-values.** The registered decisions of the Vietnamese, COCO and NoCaps registrations are rules on a paired 95% percentile bootstrap interval and its point estimate (Table 4; Section 8.1). P1, P1-EN and S-NC pass when the lower bound is above zero and the point estimate is above the SESOI of +2.0; XM-a passes when the lower bound is above zero; P2 and XM-b pass when the lower bound is above a floor of −1.0. Five of the six rules carry a margin, so that a decision depends on size as well as on a difference from zero: under P1, P1-EN and S-NC a gain passes only if its point estimate is above the smallest effect size of interest, and under P2 and XM-b a claim of no precision cost holds only if the lower bound stays above the floor. A p-value against a zero difference expresses neither margin. An interval that excludes zero corresponds only approximately, for a percentile bootstrap, to a two-sided test of a zero difference at the 0.05 level, and no exact equivalence is claimed here. Every registered interval is printed with its point estimate, so a reader can see for each one whether zero lies inside it and whether the SESOI, or the floor, lies inside it. S-NC shows why this matters: its interval lies above zero and contains the SESOI, its point estimate is below the SESOI, and the registered rule fails (Section 8.3). The two later registrations that did register a p-like bootstrap statistic, the Flickr30K comparison and the development attribution study, report it (Sections 8.6 and 5.7).
<<<C-V04 EVIDENCE>>>
Decision: answer C4, final decision (c), part (1), and the answer to follow-up F3: an explanatory paragraph in Section 5.4 only; no post hoc p-value column unless the journal's own guidelines or the editors require a printed p-value, and then only with the investigator's agreement.
Limit on wording (coordinator, with F3): the answer says that an interval excluding zero "equals" p < 0.05. NEW does not say so. It says that the correspondence with a two-sided test at the 0.05 level is approximate for a percentile bootstrap interval and that no exact equivalence is claimed, in line with the paper's own words in 08 Section 8.6 ("neither an exact p-value under the null nor an exact CI inversion") and 05 Section 5.7 ("agrees with 95% percentile lower bound > 0 except ...").
What the registered rule is: Table 4 of the same file (P1: point > +2.0 and CI lower bound > 0; P2: lower bound > -1.0 for each backbone; XM-a: lower bound > 0; XM-b: lower bound > -1.0) and Section 8.1 of 08_english_comparison.md (P1-EN and S-NC: the P1 rule). The table of Section 8.1 is not named by its number, so that the block holds no table label that C-R01 changes.
Why it was chosen: the registrations fix the rules and record no reason for their form (searched: stage-1 design, stage-2, test and English registrations; no mention of a p-value). The sentence "Five of the six rules carry a margin, so that ..." is the authors' reason, as given in answers C4 and F3 (an interval with the SESOI says more about the size of an effect), and it says only what the rules do by construction. It is not presented as a quotation of a registration.
What a reader can read: every registered interval is printed with its point estimate (Tables 7 and 8 of 06_results.md and the results table of Section 8.2). S-NC as the example: 08 l.49 ("The CI lies above zero, but the point is below the registered SESOI of +2.0, so the registered rule fails"); its printed interval contains +2.0. No number of it is repeated.
No p-value and no adjusted statistic is quoted. Numbers printed: 95 (manifest row 84), +2.0 (row 10), -1.0 (rows 80-81) and the 0.05 level (row 3872, the level of the Flickr30K registration, already named for this file). No reference is added.
The existing bullet "p-values" (l.116) is unchanged and still says that a p-value added now would be post hoc.
The OLD is the last sentence of the bullet list of Section 5.4 (l.116); shell C2 changes only the freeze sentence of the Budget paragraph of Section 5.7 in this file.
<<<C-V04 END>>>
```

### C-V05a. What the filters of OV-dev-A, OV-dev-B and KTVIC dev299 compare against (CC-405 N2)

```text
<<<C-V05a 04_data_and_splits.md OLD>>>
No file was excluded.
<<<C-V05a 04_data_and_splits.md NEW>>>
No file was excluded.

**What the other pre-specified filters compare against.** Each filter is described here by what it removed; none of these statements says that no other overlap exists. *OV-dev-A and OV-dev-B.* The 2,011 OpenViIC dev files were split into 1,005 and 1,006 before any filtering. Under the near-duplicate rule of Section 3.1, an image of the first half was dropped if it is on the exclusion list of Section 3.1 or is a near-duplicate of an image of the KTVIC test set, the OpenViIC test set, XM3600, the KTVIC development carve or the second half; the second half was filtered against the same sets except the first half. This left 911 and 925 images. *KTVIC dev299.* The one image removed from the 300-image development carve is a near-duplicate of a test image. *Flickr30K test.* Section 8.6 states what the three images outside the 997 were matched to.
<<<C-V05a EVIDENCE>>>
Ruling: CC-405 Ruling 3, C-N08, and N2: state what each "pre-specified filter" compares against, in the registrations' words, as a statement of what was removed and never as a claim that no other overlap exists.
OV-dev halves: prereg/2026-10-22_c_stage1/DESIGN.md (sha256 prefix eacc9a9c737c) §2.3 l.85-87: split of the 2,011 files into 1,005 and 1,006 "assigned before de-duplication"; "A-raw is then filtered: an image is dropped if it is listed in exclusion.json or is a near-duplicate of KTVIC test, OpenViIC test, XM3600, any --protected set, KTVIC dev300 or any B-raw image"; "B-raw is filtered against the same sets except dev-A". Counts: LISTS_ADDENDUM.md (sha256 prefix aa3923b9fe51) l.14-15 (1,005 -> 911; 1,006 -> 925).
"any --protected set" is left out: LISTS_ADDENDUM.md l.21 lists the groups hashed in the build (KTVIC memory part, KTVIC dev300, KTVIC test, XM3600, OpenViIC train, dev and test) and no further protected folder.
Rule of the OV-dev halves: LISTS_ADDENDUM.md l.7 (the lists were built with the registered matcher, the rule that Section 3.1 states). The Flickr30K filter uses a broader rule (C-V05b), so the paragraph names the rule of Section 3.1 only for the OV-dev halves.
KTVIC dev299: DESIGN.md §2.2 l.80 ("KTVIC dev300 minus image [id], a near-duplicate of a test image"). The registration's words are used as they are; which test set the image matches is not stated there. The image id is not printed; manifest row 61 (the id, status removed-PI-1101o) stays as it is.
Numbers: 2,011, 1,005, 1,006, 911, 925, 300 and 997 are all in this file at HEAD (Table 3). No new number.
Placed after the paragraph on the truncated files, so that it shares no string with C-V02a or C-V02b.
<<<C-V05a END>>>
```

### C-V05b. The 997 Flickr30K test images, in the registration's words (CC-405 N2)

```text
<<<C-V05b 08_english_comparison.md OLD>>>
Three of the 1,000 test images were excluded by a pre-specified filter fixed before decoding; the result on all 1,000 images is the registered result, and the result on the remaining 997, shown beside it, has the same verdicts.
<<<C-V05b 08_english_comparison.md NEW>>>
Three of the 1,000 test images were byte-identical or near-duplicates of a retrieval-memory, carve, val or earlier test image and were identified before decoding, by a rule fixed in the registration; the result on all 1,000 images is the registered result, and the result on the remaining 997, shown beside it, has the same verdicts.
<<<C-V05b EVIDENCE>>>
Registered sentence for the paper: prereg/2026-10-31_c_t3/PREREG.md (sha256 prefix 94caed740d7d) l.307-309: "Test images that were byte-identical or near-duplicates of any retrieval-memory, carve, val or earlier test image were identified before decoding (n = N of 1,000, W25 rule); the result on all 1,000 images is the registered result, and the result without them is shown beside it." N = 3 and 997 are the paper's own numbers at HEAD (08 l.126; Table 14).
Reference sets: the same file §6 l.130-137: (a) the COCO memory, (b) the carve, (c) val, (d) earlier test files (within test, the later file of a matching pair is excluded).
For the judge: the registered rule (§6 l.124-127) is broader than the rule of Section 3.1: byte-identical, or the rule of Section 3.1, or an SSCD cosine above 0.75 alone. NEW says "a rule fixed in the registration" and does not print the 0.75, because no manifest row for 0.75 names this file (row 3969 names 06_results.md only). If the criterion should be printed, add "(the rule of Section 3.1, with an SSCD cosine above 0.75 as a further sufficient condition)" and add 08_english_comparison.md to the used_in of a row keyed to c_t3 PREREG §6.
Which reference set each of the three images matched is not stated; the file that holds it is not named by a manifest row and was not opened.
No new number.
<<<C-V05b END>>>
```

### C-V06. Progress note: status of the companion studies (CC-405 N3)

```text
<<<C-V06 V2_PROGRESS_C.md OLD>>>
both by the same group and under review.
<<<C-V06 V2_PROGRESS_C.md NEW>>>
both by the same group and in preparation.
<<<C-V06 EVIDENCE>>>
CC-405 Ruling 3, C-N05, and N3: the paper says "in preparation" for both companions (01_introduction.md l.3 and l.16), as ruled earlier; l.16 of this progress note is stale. The note is not paper text.
<<<C-V06 END>>>
```

### C-V07. Section 6.9: how the "exploration halves" were defined (CC-405 N5, C-N07)

```text
<<<C-V07 06_results.md OLD>>>
on a guard set drawn from the exploration halves of the KTVIC and OpenViIC test sets, re-used in a development role.
<<<C-V07 06_results.md NEW>>>
on a guard set drawn from the exploration halves of the KTVIC and OpenViIC test sets, re-used in a development role (that study's registration assigned each image of the two test sets to an exploration half or a confirmation half by the parity of the last hexadecimal digit of a sha256 hash of its image id with a fixed suffix, before any decode of that study).
<<<C-V07 EVIDENCE>>>
Ruling: CC-405 Ruling 3, C-N07: find the registration of the filtering study that defines the "exploration halves", then one clause in Section 6.9.
Registration found: manuscript/prereg/2026-11-02_c_pvr_tier1/PREREG_DRAFT_v1_2.md (sha256 0a2f07736e9f1661ecc5fd25a21302d6121dd2326109f7fa89d509663723df2b; registered by run-repo commit 8282874 of 2026-11-02), §4.2 l.345-348: "half(id): h = sha256(UTF-8 bytes of the dataset's native image id string + [suffix]).hexdigest(); explore (tier 1) iff int(h[-1], 16) % 2 == 0, else confirm (tier 2). Applied to KTVIC test and OpenViIC test before any decode"; §4 table l.335-336 (KTVIC test and OpenViIC test, "explore half only", role "guard dev").
The clause prints no count of either half and no internal id of that study. Box 2 (07_disclosures.md l.21) already says that these sets were re-used after their look; the registration is dated after the registered look at OV-test.
For the judge: the file name carries "DRAFT" although it is the committed registration; later amendments of that study (the guard amendment, v3) use the same rule ("by the §4.2 rule"). I did not read that study's results.
The OLD is in Section 6.9 (06_results.md l.122); shell C2 changes only Section 6.10.9 in this file.
<<<C-V07 END>>>
```

### C-V08. Section 1: roadmap clause for Sections 6.10 and 6.11 (CC-405 N6)

```text
<<<C-V08 01_introduction.md OLD>>>
and an exploratory diagnostic (Section 6.9); Section 7 the disclosures;
<<<C-V08 01_introduction.md NEW>>>
and an exploratory diagnostic (Section 6.9); Section 6.10 reports a development, non-confirmatory attribution study, and Section 6.11 the compute; Section 7 the disclosures;
<<<C-V08 EVIDENCE>>>
Ruled clause: CC-405 Ruling 3, C-N03 ("Section 6.10 reports a development, non-confirmatory attribution study, and Section 6.11 the compute."), to be added "at the next sync of the frozen files"; C-V01 is that sync. The clause is inserted word for word, with a semicolon in place of its full stop.
For the judge: the sentence still says that Section 6 is "ending with" Sections 6.8 and 6.9. Changing "ending with" to "followed by" would be exact, but it is outside the ruled clause and is not done here.
<<<C-V08 END>>>
```

## 3. Operation C-R01: Tables 10 to 18 renumbered (CC-405 N4; answer C2)

At HEAD, and after shell C2, Tables 15 to 18 (Section 6.10) stand before Tables 10 to 14 (Section 8). The pass is one simultaneous substitution, so it cannot be written as separate OLD/NEW pairs (a NEW of one pair would be an OLD of another).

- **Map (old → new):** 15 → 10, 16 → 11, 17 → 12, 18 → 13, 10 → 14, 11 → 15, 12 → 16, 13 → 17, 14 → 18.
- **What is a reference:** the word "Table" or "Tables" followed by a list of labels joined by ", ", " and " or "–". Only labels 10 to 18 with no "S" before them are changed. "Tab. 10" of another paper (supplement, three table cells and one sentence) is not a reference of this kind and stays.
- **Exact counts on "HEAD after shell C2" (41 labels; the pass asserts each):**

| file | labels changed, by old number | total |
|---|---|---|
| `05_preregistration_and_analysis.md` | 10: 1 | 1 |
| `06_results.md` | 13: 1; 14: 1; 15: 3; 16: 12; 17: 3; 18: 2 | 22 |
| `08_english_comparison.md` | 10: 1; 11: 2; 12: 2; 13: 3; 14: 2 | 10 |
| `09_limitations.md` | 15: 1; 16: 1; 18: 1 | 3 |
| `11_supplement_registered_rows.md` | 14: 3; 15: 1; 18: 1 | 5 |

- **Valid after C2:** the text that shell C2 adds or changes (the block-4 paragraph of Section 6.10.9, the two sentences of 6.10.9 and of the Budget paragraph, the Block order item, the "Other registered arms" sentence) holds no table label. The counts above were taken on the after-C2 text.
- **Commutes with the blocks of section 2:** no OLD or NEW of this package holds a label 10 to 18 (asserted by the script), so the pass gives the same result before or after the blocks.
- **After the pass** the captions read in order: Tables 10 to 13 in Section 6.10 (nomination, the one look, the copy bound, the third-party arms) and Tables 14 to 18 in Section 8 (English predictions, English results, NoCaps domains, Flickr30K rehearsal, Flickr30K test). The script asserts this order.
- **Not touched:** "Table 1b" (the investigator's rewrite, CC-405 Ruling 3); `V2_PROGRESS_C.md`, whose six labels in this range belong to older numberings of a progress note; the frozen files, which cite no table of this range; `tex/` and the PDFs.

## 4. Operation C-M01: manifest rows 71 and 73 (CC-405 N1, Annex B)

Edit in place; no row is added or deleted and no line number shifts. The two rows that shell C2 appends at the end are not touched.

| line | number | field | from | to |
|---|---|---|---|---|
| 71 | 1997 | status | `removed-PI-1101o` | `keyed (restored under PI-1110n; CC-405)` |
| 71 | 1997 | used_in | `04_data_and_splits.md,07_disclosures.md` | `04_data_and_splits.md` |
| 73 | 1937 | status | `removed-PI-1101o` | `keyed (restored under PI-1110n; CC-405)` |
| 73 | 1937 | used_in | `04_data_and_splits.md` | `04_data_and_splits.md` (unchanged) |

- Sources asserted by the script: row 71 = `.session_backup/2026-10-26/c_test/CHAIN.log` (fc543266fcc6), l.33 "distinct sha 1997"; row 73 = test `PREREG.md` (acecd6527217) §3.1, "1,941 entries / 1,937 distinct images".
- For the judge: CC-405 Annex B writes "status removed-PI-1101o -> keyed (restored under PI-1110n; CC-405)". I read the bracket as part of the status string, as in the other annotated statuses of the manifest. If the status is the bare word `keyed`, change the constant `RESTORED` of the script.
- No other manifest row is needed: the number report of the script (section 7) finds no new number token without a row that names its file, apart from the tokens listed there.

## 5. CC-405 N8 and N9

- **N8 (Table 17 after C2).** Shell C2 adds no row to Table 17: its only addition to `06_results.md` is one paragraph in Section 6.10.9 and four words in the block-2 sentence. The twelve rows of Table 17 are those of HEAD, so "No K_nc row is REVERSED" of the ruled C-F16 paragraph still holds; the script asserts that the table has twelve rows, each with K_nc labelled DETECTED. After C-R01 the paragraph's title reads "Reading the labels of Table 12".
- **N9 (record).** In v1, the evidence of C-F13 cited `scripts/lb/decode_hf_vlm.py` l.46 for the check of the batch size; l.46 is the list of provenance fields, and the batch size is read from the registry at l.266. No text of the paper depends on it.

## 6. Deferred, not done, and what needs the investigator

**Deferred (not in this package):**
- CC-405 N5, second and third parts: a verified reference for the Open Images V7 human-verified labels, and the reading for C-N15 (two full texts, a dated systematic search). Both need the network, which this task does not use.
- Answer C5 (i), release of per-image scores without captions: it changes three sentences together (`01_introduction.md` l.34, `09_limitations.md` l.28, `10_conclusion.md` l.23–25) and waits for the check of each dataset's terms that the answer itself asks for. The second half of that answer (the lost Flickr30K score file in Section 8.6 and Box 2) is already in the paper since v1.
- Answer C3, last clause: the matching note in the conference version is for the package of that version.
- Answer C4: the sentence for the cover letter is outside the paper files.
- The zero-shot prompt text. Answer C5 (ii) lists the in-context template; the zero-shot prompt is the companion studies' prompt, pinned in `decode_icl.py` l.58 by its sha256. Printing it is one more line in C-V03a.

**Not done, by instruction:** answer C4, part (2), a post hoc p-like column in the supplement. Nothing was computed. The answer to follow-up F3 withdraws that part: no such column unless the journal's guidelines or the editors require a printed p-value, and then only with the investigator's agreement.

**Needs the investigator:**
1. C-V01 is a change to a frozen file; the corresponding author decided it (answer C1), and the wording here is a proposal for the investigator's rewrite to accept or replace.
2. CC-405 C-N10: whether the abstract and contribution 2 say that InternVL3's registered arm includes the deletion step. Recommendation as in CC-405: one design clause at the rewrite; the abstract of C-V01 leaves two words of budget, so the clause needs further trims.
3. Whether the zero-shot prompt is printed with the template (recommendation: yes, one line, if the companion studies' release plan allows it).
4. Answer C5 (i): who checks the dataset terms, and when the three sentences change (recommendation: with the deposit, before submission).
5. "Table 1b" and the title of the supplement stay for the rewrite (CC-405).

## 7. Checks run

Method: a read-only harness imported the apply script as a module and called its build function on texts built in memory: every section file from `git show 9b8e6ae:`, the four files of shell C2 changed by the C2 script's own `swap` calls and `c2a_text`, and the manifest of 9b8e6ae with the two rows C2 appends (the K7 row made from the script's template with a dummy stamp and id). Nothing was written to the paper repo; the apply script's `main` was not run.

| id | file | OLD occurs exactly once on "HEAD after shell C2" | also exactly once at 9b8e6ae, before C2 | outside every span that C2 changes |
|---|---|---|---|---|
| C-V01 | `00_abstract.md` | yes | yes | yes |
| C-V02a | `04_data_and_splits.md` | yes | yes | yes |
| C-V02b | `04_data_and_splits.md` | yes | yes | yes |
| C-V03a | `11_supplement_registered_rows.md` | yes | yes | yes |
| C-V03b | `03_method.md` | yes | yes | yes |
| C-V03c | `08_english_comparison.md` | yes | yes | yes |
| C-V04 | `05_preregistration_and_analysis.md` | yes | yes | yes |
| C-V05a | `04_data_and_splits.md` | yes | yes | yes |
| C-V05b | `08_english_comparison.md` | yes | yes | yes |
| C-V06 | `V2_PROGRESS_C.md` | yes | yes | yes |
| C-V07 | `06_results.md` | yes | yes | yes |
| C-V08 | `01_introduction.md` | yes | yes | yes |

Further checks, all passed:
- 12 blocks under 8 ids; each NEW occurs exactly once after all blocks; applying the blocks in the reverse order gives byte-equal files.
- No OLD or NEW holds one of the strings of shell C2 (its two OLD strings, its three anchors, its two appended clauses), and no OLD overlaps the place of the block-4 paragraph.
- C-R01: the pass changed exactly the 41 labels of section 3, file by file and number by number; after it the captions run "1, 1b, 2, …, 18" in order of appearance; no block holds a label 10 to 18.
- C-M01: of the 5,670 manifest lines after C2, only lines 71 and 73 change; the sha256 prefix in each of the two rows equals the sha256 of its source file, and the source holds the quoted words.
- C-V01: 198 words; no first-person word; no citation. Every number of the abstract has a manifest row that names `00_abstract.md`.
- C-V03a: the five table rows equal, byte for byte, the strings read from `scripts/c_stage1/decode_icl.py` and `scripts/c_en/cen_decode.py`; both files equal their pinned sha256; both template hashes recomputed from the strings equal the pins `7478361a…` and `b329e57a…`.
- CC-405 N8: Table 12 (old 17) has twelve rows after the package, each with K_nc labelled DETECTED and the bound "in force".
- Untouched by the package: `02_related_work.md`, `07_disclosures.md`, `10_conclusion.md`, `STUDY_BRIEF_C.md`, `paperC.bib`.
- The gate of the apply script accepts the simulated tree and refuses it when one file is still the text before C2, or when the manifest lacks the two rows of C2.
- Number tokens whose count grows in a file and that no manifest row names for that file: only section numbers (3.1, 3.3, 5.7, 6.10, 6.11, 8.1, 8.3, 8.6) and the new table numbers of C-R01. No result number is without a row.

sha256 of the section files before and after this package (the apply script holds the same values as `PRE` and `TARGET`):

| file | on "HEAD after shell C2" | after this package |
|---|---|---|
| `00_abstract.md` | `4c023726251dc023be30542f3d95d778af8f7b0c483fa84e1379f026a7a6d630` | `a4725e99fbd8883be97c991639020870a8bcdfa21f34483ddf5f5f18610cc51f` |
| `01_introduction.md` | `b731e6371c425657f647732faf5ddf0203001fed3dc15f5e694f410dc575ec00` | `ad60b37f045ad34d2994d6a44e2459fbb13e044f367a5e1a159ea95273cbbe0c` |
| `03_method.md` | `45888a88eddaad7fff2aafea9d30f92f82a355b1d9f7f72e9e48c13ae2ff12f5` | `5db109ab3b011cf658da599d5ef67636c7b282f378829abb3a35f176521da057` |
| `04_data_and_splits.md` | `f7d1d0e7fa48390fa78e7cccfed971c59a66401a1405f9c6dd78430e06177b99` | `b7f333a8571685cdd84c1fc1b7556ebecba3e2e98fd8e6597a30e7d82be7575c` |
| `05_preregistration_and_analysis.md` | `0137bb6bfe2245d7f3c2788aaa64105fa780daebc33984b3575ba7df69444a83` | `d46bbc40a2ed9343ea7a1d3d02b4947b7fac3d4bf3cfad397cfbbdd5cfdeae68` |
| `06_results.md` | `68f77eb9a59e8d07a293aa7cb316f407b4d2b9f38717c5ee7b73fb97ee9995fa` | `01d41de0ba50542b5a991353e7ff56f762f5ce36b33e8b732fa3d352530e60f6` |
| `08_english_comparison.md` | `72f3cd8b5f916669c54490f993447f8fa5af6ba5ce240647f5a842bf6ae10b14` | `69706e5f18ef88a5c9d9bdbcb8ad30607b565cd58043d50275a84f6e93a121f8` |
| `09_limitations.md` | `4111d0957ae1555922defef6096a396a3b76b300c57435c0778e8f8ebfe01df2` | `c52b962c41460296aefd324c7f9a53b4b6f1c149026c17d08051d279c458745c` |
| `11_supplement_registered_rows.md` | `025d744a9413ef509558496ef55694188dd7249baace8a946aa98c81c791f165` | `5a71a8a08085cdaabe385539208f008275aed18fabbd6c962cf0d0c5c44f0ff9` |
| `V2_PROGRESS_C.md` | `c208ed1b3cb6537dfee718bb057522913921aed4c3b8ba731d5d48e5e1f45d7d` | `eee308faacbd2f5f0902d65db79c34ad4ad3cfeb2954acbfaea1fe26b2c16689` |

`number_manifest_C.tsv` has no fixed sha256 here: the K7 row of shell C2 carries a stamp and an id that do not exist yet. The apply script checks it by structure (the 9b8e6ae manifest, sha256 `83414dc3…`, plus exactly the two rows of C2) and changes lines 71 and 73 only.

Not checked, and said so where it matters:
- The manifest check of the paper repo, the n-gram and caption scan and the LaTeX build were not run, because nothing was applied. The fonts of the prompt-template table were not tested.
- If shell C2 or its text package changes before it runs, or if any other commit touches these files first, the values above are void: the apply script will refuse, and the blocks must be checked again.
- If a judge changes a NEW text, `PKG_SHA` and `TARGET` of the apply script must be recomputed.
- C-V07: the results of the earlier filtering study were not read; only its registration.
- C-V05b: which reference set each of the three Flickr30K images matched was not looked up.
