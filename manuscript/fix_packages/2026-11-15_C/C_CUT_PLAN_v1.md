# Paper C: cut plan for Sections 5.7 and 6.10 (plan only)

Prepared 2026-11-15 (UTC), for answer C2 of the corresponding author. This file is a plan. No text of the paper is cut, moved or written by it: the investigator's standing rule is full drafts, and he cuts at his rewrite.

## 0. What the answer asks, and what this plan gives

Answer C2 keeps the attribution study in the main text of the journal version, labelled "development, non-confirmatory", and asks that Sections 5.7 and 6.10 go down to about 1,200–1,500 words, centred on the definitions of τ_marg and τ_pair, the nomination result from OV-dev-A to OV-dev-B at batch size 1, the LMCap positive control, the batch warning of kill gate K1 and the main reading of the copy bound; with the tables in order of appearance, the past tense after the freeze, and every operational detail, budget formula and side table in Supplement S.

This plan shows one way to do it that reaches **about 1,490 words** of running text in the two sections together (353 in Section 5.7, 1,138 in Section 6.10), from 6,583 now. It keeps every registered verdict, every limit and every NOT RUN statement in the main text. Section 4 lists them. Section 7 says what a further cut to 1,200 words would cost.

Already done or prepared elsewhere, and not repeated here: the past tense after the freeze (shell C2), the renumbering of Tables 10–18 (package v2, operation C-R01), and the definitions of τ_marg and τ_pair, which are in Section 3.8 and are not part of the two sections counted here.

## 1. Text counted and counting rule

- **Text counted:** `05_preregistration_and_analysis.md` from the heading "5.7" to the end of the file, and `06_results.md` from the heading "6.10" to the heading "6.11", as they will stand after shell C2 and after package v2 (built in memory; nothing was written to the paper repo). Table numbers are those after C-R01: Table 10 (old 15, nomination), Table 11 (old 16, the one look), Table 12 (old 17, copy bound), Table 13 (old 18, third-party arms).
- **A block** is a run of lines between two blank lines: a heading, a box, a paragraph (with the list that follows it without a blank line), a table caption or a table.
- **Words** are whitespace-separated tokens of the Markdown source, as `wc -w` counts them. Markup tokens and numbers count. Headings and the two boxes are counted in the running text. Tables and their captions are counted apart, because a word target for running text does not usually include them.

| part | words now | words in the main text after the plan | words in blocks that move |
|---|---|---|---|
| Section 5.7 (running text) | 2,522 | 353 | 2,474 |
| Section 6.10 (running text) | 4,061 | 1,138 | 3,558 |
| **both sections (running text)** | **6,583** | **1,491** | **6,032** |
| tables and captions of Section 6.10 | 1,642 | 975 stay (Tables 11 and 13) | 667 move (Tables 10 and 12) |

"Words in blocks that move" is larger than the difference of the first two columns, because a block marked "MOVE, summary stays" goes to the supplement whole and unchanged, and a new short summary is written for the main text.

| subsection | words now | main text after | what carries the cut |
|---|---|---|---|
| 5.7 The attribution registration | 2,522 | 353 | variance, memory source, document-frequency row, scoring parity, order of looks and budget move whole; the rules stay as one or two sentences each |
| 6.10 heading and box | 70 | 70 | unchanged |
| 6.10.1 What ran | 209 | 29 | counts of runs, caps and hashes move |
| 6.10.2 Kill gate K1 | 948 | 210 | six paragraphs become six short ones |
| 6.10.3 The registered claim | 654 | 223 | the per-row sentences move; the two verdicts stay word for word |
| 6.10.4 XM-dev500 | 50 | 15 | becomes one sentence of 6.10.3 |
| 6.10.5 Placebo, variance, fixed set | 349 | 74 | the six shares and the fixed-set numbers move |
| 6.10.6 The copy bound | 816 | 130 | the twelve per-row sentences and Table 12 move |
| 6.10.7 Batched rows | 83 | 15 | becomes one sentence of 6.10.2 |
| 6.10.8 Positive control and third-party arms | 691 | 181 | four paragraphs shortened |
| 6.10.9 What did not run | 191 | 191 | unchanged |

## 2. The three dispositions

- **STAY:** the block stays in the main text, word for word.
- **MOVE:** the whole block goes to the supplement, word for word. Nothing of it stays, apart from a pointer where one is needed.
- **MOVE, summary stays:** the whole block goes to the supplement, word for word, so that the ruled wording is kept in full there. The main text gets a short summary of about the number of words given, which must hold the items named in the column "what the main text keeps". The summaries are new text. This plan does not write them.

## 3. Block by block

Files: blocks `5.7-…` are in `05_preregistration_and_analysis.md`; blocks `6.10-…` are in `06_results.md`. "Heading" is the number of the subsection the block stands under. The two running totals are in words: "moved" adds the size of every block that leaves the main text; "main" adds what stays. Tables and captions are outside both totals.

| block | heading | kind | first words … last words | words | disposition | main text after (words) | what the main text keeps | moved, running total | main, running total |
|---|---|---|---|---|---|---|---|---|---|
| 5.7-01 | 5.7 | heading | 5.7 The attribution registration (development) | 6 | STAY | 6 | heading | 0 | 6 |
| 5.7-02 | 5.7 | box | Development data only: DEVELOPMENT / C-ATTR-DEV, … verdict of Sections 6.2–6.9 or 8. | 42 | STAY | 42 | the box, whole: development data only; no test set staged, decoded, scored or opened; no verdict of Sections 6.2–6.9 or 8 changes | 0 | 48 |
| 5.7-03 | 5.7 | para | Files and order. The registration (C-ATTR-DEV, version … code (Section 5.7, "Order of looks"). | 138 | MOVE, summary stays | 20 | registered before any output; addendum v1.2 after K1 fired and before any output was scored | 138 | 68 |
| 5.7-04 | 5.7 | para | Sets. OV-dev-A (911 images) nominates; OV-dev-B (925) … image of a set is decoded. | 52 | MOVE, summary stays | 20 | OV-dev-A nominates; OV-dev-B carries the one registered look; XM-dev500 has no rule | 190 | 88 |
| 5.7-05 | 5.7 | para | What a first look means here. On … τ_sel" and stays outside every family. | 200 | MOVE, summary stays | 40 | τ_sel was already known on both halves; the words "split of a known τ_sel"; a pass is reported as "the nominated split held on a re-used development set, at batch size 1", never as new evidence that retrieval helps | 390 | 128 |
| 5.7-06 | 5.7 | para | Interval and p-like statistic. Every interval is … it is not an exact p-value. | 81 | MOVE, summary stays | 20 | paired image bootstrap, B = 2,000; the one-sided p-like statistic and that it is not an exact p-value | 471 | 148 |
| 5.7-07 | 5.7 | para | Labels. With SESOI = +2.0 stripped CIDEr-D … - UNRESOLVED: none of the above. | 185 | MOVE, summary stays | 60 | the four label rules in one sentence each: DETECTED (point ≥ +2.0 and p̃ under the Holm threshold at one-sided 0.025), REVERSED, NEGLIGIBLE (90% interval inside ±2.0), UNRESOLVED | 656 | 208 |
| 5.7-08 | 5.7 | para | For m = 1 this matches the … one-sided 0.05 of the Flickr30K registration. | 54 | MOVE | 0 | – | 710 | 208 |
| 5.7-09 | 5.7 | para | Nomination, then one look. 1. Nomination (OV-dev-A). … decodes), are descriptive rows with labels. | 181 | MOVE, summary stays | 45 | items 1, 3 and 5: the nomination rule on OV-dev-A (95% lower bound ≥ +2.0), PASS on OV-dev-B = DETECTED within the Holm family of the nominated claims, and the sentence used if nothing is nominated | 891 | 253 |
| 5.7-10 | 5.7 | para | Multiplicity. One registered family: the nominated claims. … stand beside it, labelled post hoc. | 60 | MOVE, summary stays | 15 | one registered family (the nominated claims); the secondary family S-BB, with the pointer to "What did not run" | 951 | 268 |
| 5.7-11 | 5.7 | para | Failure wording, fixed in the registration. A … no registered claim about the split. | 67 | MOVE | 0 | – (registered failure wording; no nominated claim failed) | 1018 | 268 |
| 5.7-12 | 5.7 | para | XM-dev500. Rows are reported per backbone with … nor NEGLIGIBLE can be decided reliably. | 41 | MOVE, summary stays | 10 | XM-dev500 rows carry no rule | 1059 | 278 |
| 5.7-13 | 5.7 | para | Third-party arms and the positive control. Block … bound is computed for block 3. | 167 | MOVE, summary stays | 30 | the one registered rule of block 3: LMCap's τ_sel on OV-dev-B must be DETECTED, or the third-party rows are printed without interpretation | 1226 | 308 |
| 5.7-14 | 5.7 | para | Variance. (a) For each backbone and set … with a number from this analysis. | 282 | MOVE | 0 | – (the placebo flag rule and the `fix` label rule are named with their outcomes in the summary of 6.10.5) | 1508 | 308 |
| 5.7-15 | 5.7 | para | Copy bound: tiers and reading. On OV-dev-B … any other outcome gives "partly bounded". | 117 | MOVE, summary stays | 15 | the copy bound is post hoc on OV-dev-B and a first look at κ on XM-dev500; its reading sentences were fixed in the registration | 1625 | 323 |
| 5.7-16 | 5.7 | para | Memory source (English only). The registered Vietnamese … configuration with the near cut, and | 122 | MOVE | 0 | – (block 4 was not run; the NOT RUN statement stays in 6.10.9) | 1747 | 323 |
| 5.7-17 | 5.7 | para | δ = mean_i {[s_i(ret; M_T) − s_i(rand; … − [s_i(ret; M_O) − s_i(rand; M_O)]}, | 14 | MOVE | 0 | – | 1761 | 323 |
| 5.7-18 | 5.7 | para | with the interval and label above and … reading sentence is applied to it. | 182 | MOVE | 0 | – | 1943 | 323 |
| 5.7-19 | 5.7 | para | Document-frequency sensitivity. CIDEr-D document frequencies come from … is descriptive and has no rule. | 101 | MOVE | 0 | – | 2044 | 323 |
| 5.7-20 | 5.7 | para | Scoring parity. Before any new run was … reproduce its own ledger within 1e-4. | 37 | MOVE | 0 | – | 2081 | 323 |
| 5.7-21 | 5.7 | para | Order of looks. The scoring ran in … previous stage's file and ran once. | 229 | MOVE, summary stays | 15 | the scoring order was enforced by the code: nomination file before any OV-dev-B run, batched outputs last, the positive control first in block 3 | 2310 | 338 |
| 5.7-22 | 5.7 | para | Budget. Block 1 had a hard cap … every step not finished by then. | 164 | MOVE, summary stays | 15 | the freeze sentence, word for word (14 words) | 2474 | 353 |
| 6.10-01 | 6.10 | heading | 6.10 Attribution of the retrieval gain on development data | 10 | STAY | 10 | heading | 2474 | 363 |
| 6.10-02 | 6.10 | box | Development data only (OV-dev-A, OV-dev-B, XM-dev500): … τ_sel was already known (Section 5.7). | 60 | STAY | 60 | the box, whole: development only; registered after every test set was decided; changes no verdict; not in the abstract or the contributions; τ_sel already known | 2474 | 423 |
| 6.10-03 | 6.10.1 | heading | 6.10.1 What ran | 4 | STAY | 4 | heading | 2474 | 427 |
| 6.10-04 | 6.10.1 | para | Block 1 decoded the perm, fix and … the scoring parity gate passed (ok). | 205 | MOVE, summary stays | 25 | blocks 1, 1b and 3 ran; every registered step finished, with no cap stop and no job stop (GPU-hours are in Section 6.11) | 2679 | 452 |
| 6.10-05 | 6.10.2 | heading | 6.10.2 Batch composition changed greedy captions (kill gate K1) | 10 | STAY | 10 | heading | 2679 | 462 |
| 6.10-06 | 6.10.2 | para | What was registered. The attribution registration assumed … rows are printed "A1 not met". | 133 | MOVE, summary stays | 30 | assumption A1 and the two 50-item checks; failure of check (b) = kill gate K1 | 2812 | 492 |
| 6.10-07 | 6.10.2 | para | What happened. Host parity held for every … sha256 logged, before any score existed. | 83 | MOVE, summary stays | 35 | the three counts (42/50, 37/50, 31/50) and the registered sentence, word for word: "K1 fired: no backbone met A1 under registration v1.1; block 1 as registered carries no claim." | 2895 | 527 |
| 6.10-08 | 6.10.2 | para | What it means. The decoder is greedy … coupling of images within a slice. | 252 | MOVE, summary stays | 25 | a decode is reproducible given its batch and not invariant to the batch; the reading of the decoder code is post hoc and was not tested | 3147 | 552 |
| 6.10-09 | 6.10.2 | para | What it does not show. No score … stack and 50 OV-dev-B items each. | 77 | MOVE, summary stays | 40 | every limit of the paragraph: string identity only, no score compared; nothing on quality, sign or size; no batched result of the paper shown to be biased; three models, one stack, 50 items each | 3224 | 592 |
| 6.10-10 | 6.10.2 | para | Consequences for this paper. Every registered contrast … and Box 2 are corrected accordingly). | 135 | MOVE, summary stays | 40 | registered contrasts were decoded in fixed batches with one policy for both arms; rows are results of the systems as run, no number changes, none is relabelled; the 52/52 checks show run-to-run parity, not batch invariance | 3359 | 632 |
| 6.10-11 | 6.10.2 | para | Consequences for the attribution study. After K1 … effect; this reading was not tested. | 258 | MOVE, summary stays | 30 | addendum v1.2: every contrast arm decoded anew at batch size 1; D1 passed for all three backbones; the two row labels ("batch size 1; registered in v1.2 after K1 fired, on string-identity counts only" and "A1 not met; batched decode; descriptive") | 3617 | 662 |
| 6.10-12 | 6.10.3 | heading | 6.10.3 The registered claim (nomination, then one look) | 9 | STAY | 9 | heading | 3617 | 671 |
| 6.10-13 | 6.10.3 | caption | Table 10. Nomination on OV-dev-A (911 images) … K1 fired, on string-identity counts only". | 60 | MOVE with its table | – | – | – | – |
| 6.10-14 | 6.10.3 | table | ¦ backbone ¦ estimand ¦ difference [95% … τ_sel ¦ not a candidate ¦ | 131 | MOVE (table) | – | the nomination table goes to the supplement; the next block names the two nominated claims | – | – |
| 6.10-15 | 6.10.3 | para | On OV-dev-A, 2 claims met the nomination … at family-wise one-sided α = 0.025. | 48 | STAY | 48 | whole: 2 claims nominated, the nomination file hashed before any OV-dev-B output was scored, Holm family of size 2 | 3617 | 719 |
| 6.10-16 | 6.10.3 | caption | Table 11. The one look at OV-dev-B … K1 fired, on string-identity counts only". | 75 | STAY with its table | – | caption to be shortened at the rewrite; the three fixed labels become table notes | – | – |
| 6.10-17 | 6.10.3 | table | ¦ backbone ¦ estimand ¦ difference [95% … ¦ placebo flagged (Section 6.10.5) ¦ | 336 | STAY (table) | – | the one look at OV-dev-B, all twelve rows | – | – |
| 6.10-18 | 6.10.3 | para | H_pair(Qwen2.5-VL-7B): PASS. On OV-dev-B, Qwen2.5-VL-7B's τ_pair was … not new evidence that retrieval helps. | 96 | STAY | 96 | whole, word for word: the two registered verdicts H_pair PASS with their intervals, thresholds and the two fixed sentences | 3617 | 815 |
| 6.10-19 | 6.10.3 | para | Qwen2.5-VL-7B's τ_marg on OV-dev-B was +0.96 [0.01, … descriptive row with no registered claim. | 263 | MOVE, summary stays | 45 | τ_marg NEGLIGIBLE for both backbones; "NEGLIGIBLE means inside ±2.0, not zero" (Qwen2.5-VL-7B's 95% interval excludes zero); low power by design, said once; τ_sel and τ_any rows are descriptive | 3880 | 860 |
| 6.10-20 | 6.10.3 | para | Aya-Vision-8B has no OV-dev-A decodes, so its … flagged on this set (Section 6.10.5). | 209 | MOVE, summary stays | 25 | Aya-Vision-8B: a first look with labels and no registered claim; placebo flagged on this set | 4089 | 885 |
| 6.10-21 | 6.10.3 | para | Recomputing document frequencies inside 200 bootstrap resamples … is descriptive and has no rule. | 29 | MOVE | 0 | – | 4118 | 885 |
| 6.10-22 | 6.10.4 | heading | 6.10.4 XM-dev500 at batch size 1 (no rule) | 9 | MOVE | 0 | – (heading dropped; the next block becomes one sentence of 6.10.3) | 4127 | 885 |
| 6.10-23 | 6.10.4 | para | On XM-dev500 the rows carry no rule: … a family or a scope sentence. | 41 | MOVE, summary stays | 15 | XM-dev500 rows carry no rule and enter no family or scope sentence | 4168 | 900 |
| 6.10-24 | 6.10.5 | heading | 6.10.5 Placebo, variance components and the fixed set | 9 | STAY | 9 | heading | 4168 | 909 |
| 6.10-25 | 6.10.5 | para | The rand d1 − d2 placebo of … of Aya-Vision-8B's draw-averaged τ_sel on XM-dev500. | 198 | MOVE, summary stays | 40 | the flagged placebo of Aya-Vision-8B on OV-dev-B with its interval; the recorded review; flagged rows carry the flag; the range of the six draw shares | 4366 | 949 |
| 6.10-26 | 6.10.5 | para | With five fixed sets on OV-dev-B, ω̂ … this section enters a test table. | 142 | MOVE, summary stays | 25 | by the registered rule every `fix` row is "conditional on the realised fixed set"; no test interval is widened, recomputed or relabelled | 4508 | 974 |
| 6.10-27 | 6.10.6 | heading | 6.10.6 The copy bound (post hoc on OV-dev-B; first look at κ on XM-dev500) | 15 | STAY | 15 | heading | 4508 | 989 |
| 6.10-28 | 6.10.6 | caption | Table 12. Copy bound at n = … "A1 not met; batched decode; descriptive". | 75 | MOVE with its table | – | – | – | – |
| 6.10-29 | 6.10.6 | table | ¦ set ¦ backbone ¦ unit ¦ … not met; batched decode; descriptive ¦ | 401 | MOVE (table) | – | the copy-bound table goes to the supplement, beside Table S24 | – | – |
| 6.10-30 | 6.10.6 | para | On OV-dev-B, Qwen2.5-VL-7B, unit (i) syllables, L_cp … was computed once on stored outputs. | 254 | MOVE, summary stays | 25 | on all six OV-dev-B rows the L_cp point is ≤ 0, so the registered reading applies, quoted once word for word; these rows are post hoc | 4762 | 1014 |
| 6.10-31 | 6.10.6 | para | On XM-dev500, Qwen2.5-VL-7B, unit (i) syllables, L_cp … on this set had been seen. | 250 | MOVE, summary stays | 15 | the same reading on the six XM-dev500 rows, a first look at κ | 5012 | 1029 |
| 6.10-32 | 6.10.6 | para | Reading the labels of Table 12. REVERSED … force on every row (column "bound"). | 121 | MOVE, summary stays | 20 | no K_nc row is REVERSED, so the bound is in force on every row; it is a bound under an assumption, not an estimate of copying | 5133 | 1049 |
| 6.10-33 | 6.10.6 | para | The English copy bound on the Flickr30K … construction; the scorer's self-test checks it. | 40 | STAY | 40 | whole: the English copy bound was not coded and was not run | 5133 | 1089 |
| 6.10-34 | 6.10.6 | para | A post hoc companion compares the retrieval … run with a hash of record). | 136 | MOVE, summary stays | 15 | the memory-source companion is post hoc and size-confounded, with no reading sentence; rule L on its four cells: NOT RUN | 5269 | 1104 |
| 6.10-35 | 6.10.7 | heading | 6.10.7 Batched rows (descriptive sensitivity row) | 7 | MOVE | 0 | – (heading dropped) | 5276 | 1104 |
| 6.10-36 | 6.10.7 | para | Table S22 prints the batched block-1 rows … so no base arm was re-decoded. | 76 | MOVE, summary stays | 15 | the batched rows are in Table S22 with the label "A1 not met; batched decode; descriptive" | 5352 | 1119 |
| 6.10-37 | 6.10.8 | heading | 6.10.8 The positive control and the third-party arms (block 3) | 11 | STAY | 11 | heading | 5352 | 1130 |
| 6.10-38 | 6.10.8 | caption | Table 13. Third-party arms at batch size … none ("–"); no difference is computed. | 197 | STAY with its table | – | caption to be shortened at the rewrite; the fixed row labels become table notes | – | – |
| 6.10-39 | 6.10.8 | table | ¦ set ¦ system ¦ estimand ¦ … ¦ block 1b; no rule ¦ | 367 | STAY (table) | – | the OV-dev-B rows; the five XM-dev500 rows may go to the supplement beside Table S21 | – | – |
| 6.10-40 | 6.10.8 | para | The positive control (registered). LMCap's text generator … of those runs is used here). | 88 | MOVE, summary stays | 55 | the registered result, word for word in its core: the value with its interval, "DETECTED", "The positive control was met."; first look at this contrast | 5440 | 1185 |
| 6.10-41 | 6.10.8 | para | What the positive control shows, and what … any test set or about XM-dev500. | 236 | MOVE, summary stays | 55 | every limit: nothing on sensitivity near +2.0; no negative control; does not re-validate the rows of 6.10.3; nothing on LMCap's published numbers, on any test set or on XM-dev500 | 5676 | 1240 |
| 6.10-42 | 6.10.8 | para | LMCap's split on OV-dev-B. LMCap's τ_pair was … not a check of those rows. | 196 | MOVE, summary stays | 30 | LMCap: τ_pair DETECTED, τ_marg NEGLIGIBLE; the same label pattern as the two backbones; a description, not a check of those rows | 5872 | 1270 |
| 6.10-43 | 6.10.8 | para | The image format on OV-dev-B. Qwen2.5-VL-7B's image-format … an unregistered contrast between prompt formats. | 93 | MOVE, summary stays | 20 | image format: τ_sel DETECTED; no difference or ratio to the text-example row is computed | 5965 | 1290 |
| 6.10-44 | 6.10.8 | para | XM-dev500. Every XM-dev500 row of Table 13 … own label; no difference is computed. | 67 | MOVE, summary stays | 10 | XM-dev500 rows of the table have no registered rule | 6032 | 1300 |
| 6.10-45 | 6.10.9 | heading | 6.10.9 What did not run | 6 | STAY | 6 | heading | 6032 | 1306 |
| 6.10-46 | 6.10.9 | para | Block 2, which would have added backbones … the secondary family S-BB is empty. | 32 | STAY | 32 | whole: block 2 not run by its cut-off or before the freeze; S-BB empty | 6032 | 1338 |
| 6.10-47 | 6.10.9 | para | Scope (registration §7.6), counting the non-Qwen backbones … language model and is not counted. | 88 | STAY | 88 | whole: the registered scope sentence with its post hoc label and its flag | 6032 | 1426 |
| 6.10-48 | 6.10.9 | para | Block 3 ran (Section 6.10.8). … Block 3 ran (Section 6.10.8). | 5 | STAY | 5 | whole | 6032 | 1431 |
| 6.10-49 | 6.10.9 | para | Block 4 was not run before the … out-of-source Vietnamese memory exists in it. | 60 | STAY | 60 | whole: block 4 not run before the freeze | 6032 | 1491 |

## 4. What must stay in the main text

Each item names the block that holds it now. An item marked "word for word" is registered or ruled wording and should be copied, not paraphrased.

**Registered verdicts and labels**

1. The kill gate (6.10-07), word for word: "K1 fired: no backbone met A1 under registration v1.1; block 1 as registered carries no claim." With it, the three counts 42/50, 37/50 and 31/50, and that D1 passed for all three backbones (6.10-11).
2. The nomination (6.10-15): two claims met the rule on OV-dev-A, H_pair(Qwen2.5-VL-7B) and H_pair(InternVL3-8B); the nomination file was hashed before any new OV-dev-B output was scored; one Holm family of size 2.
3. The two verdicts (6.10-18), word for word, each with its interval, its p-like statistic and its Holm threshold: "H_pair(Qwen2.5-VL-7B): PASS." and "H_pair(InternVL3-8B): PASS.", and after each of them "the nominated split held on a re-used development set, at batch size 1. This is a split of a known τ_sel, not new evidence that retrieval helps."
4. The marginal component (6.10-19, 6.10-20): τ_marg is NEGLIGIBLE for all three backbones on OV-dev-B, with "NEGLIGIBLE means inside ±2.0, not zero" and the fact that Qwen2.5-VL-7B's 95% interval excludes zero.
5. The positive control (6.10-40), word for word in its core: "+16.92 [15.00, 19.06] (p̃ = 1/2,001, its floor), DETECTED. The positive control was met."
6. The copy bound (6.10-30, 6.10-31), the registered reading, once and word for word: "the bound does not exclude that the whole retrieval-specific effect is carried by copied n-grams; this agrees with, and does not prove, the published short-cut account". With it, that no K_nc row is REVERSED, so the bound is in force on every row (6.10-32).
7. The fixed-set label (6.10-26): by the registered rule every `fix` row is "conditional on the realised fixed set".
8. The placebo flag (6.10-25): the `rand` d1 − d2 placebo of Aya-Vision-8B on OV-dev-B was flagged, a recorded review followed, and its rows that contain a `rand` arm carry the flag.
9. The registered scope sentence (6.10-47), with its two qualifiers: "the retrieval-specific effect was seen for one backbone outside the Qwen line", the row being post hoc and carrying the placebo flag.
10. The fixed row labels, wherever a row is printed: "DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY"; "batch size 1; registered in v1.2 after K1 fired, on string-identity counts only"; "A1 not met; batched decode; descriptive"; "split of a known τ_sel"; "batch-1 re-decode of a known τ_sel".

**Limits**

11. The two boxes (5.7-02 and 6.10-02), whole: development data only; no test set staged, decoded, scored or opened; registered after every test set of the paper was decided; no verdict of Sections 6.2–6.9 or 8 changes; not in the abstract or the contributions; τ_sel already known on OV-dev-A and OV-dev-B.
12. What K1 does not show (6.10-09): string identity only; no score compared; nothing on the quality of either caption or on the sign or size of any score difference; no batched result of the paper is shown to be biased; the numerical cause is not identified; three models, one software stack, 50 OV-dev-B items each.
13. What K1 means for the registered results (6.10-10): they are results of the systems as run; no number changes and none is relabelled; the 52/52 checks show run-to-run parity, not batch invariance. The reading of the decoder code is post hoc and was not tested (6.10-08).
14. NEGLIGIBLE has low power by design (6.10-19), said once instead of three times.
15. What the positive control does not show (6.10-41): nothing about sensitivity near +2.0; no negative control; it does not re-validate or strengthen the rows of Section 6.10.3; nothing about LMCap's published numbers, about any test set or about XM-dev500.
16. XM-dev500 rows carry no rule (6.10-23, 6.10-44), and no difference between the two prompt formats is computed (6.10-43).
17. The copy bound is post hoc on OV-dev-B and a first look at κ on XM-dev500, and it bounds the stored, batched contrast, not the batch-size-1 τ_sel (caption of Table 12, 6.10-28; this sentence must be kept in the running text if the table moves).
18. "No test interval is widened, recomputed or relabelled" with a number of this study (6.10-26; 5.7-14).

**NOT RUN statements**

19. Block 2 (6.10-46), whole: not run by its registered cut-off or before the freeze; the secondary family S-BB is empty; no backbone first decoded under this registration was run (6.10-47).
20. Block 4 (6.10-49), whole: not run before the freeze; the English `perm` and extra `rand` arms and the size-matched memory swap have no rows.
21. The English copy bound (6.10-33), whole: "was not coded and was not run".
22. Rule L on the four cells of the memory-source companion (6.10-34): NOT RUN, with its reason; one sentence may replace the four.
23. The freeze sentence (5.7-22), word for word: "A freeze at 2026-11-16 12:00 (UTC+7) ended every step not finished by then."

## 5. Tables

| table (after C-R01) | words, caption + body | plan | reason |
|---|---|---|---|
| Table 10 (old 15), nomination on OV-dev-A | 60 + 131 | to the supplement | its outcome is one sentence (item 2); the six values are needed only to check the rule |
| Table 11 (old 16), the one look at OV-dev-B | 75 + 336 | stays, all twelve rows | it holds the two registered verdicts and the labels of every other row |
| Table 12 (old 17), copy bound at n = 3 | 75 + 401 | to the supplement, beside Table S24 (the bound at every n) | every row has the same reading (item 6) |
| Table 13 (old 18), third-party arms | 197 + 367 | stays; its five XM-dev500 rows may go beside Table S21 | it holds the registered positive control |

- The captions of Tables 11 and 13 carry fixed labels and are long (75 and 197 words). At the rewrite the labels can become table notes; no label may be dropped.
- If Tables 10 and 12 move, the main-text tables are numbered once more (the one look becomes Table 10, the third-party arms Table 11, the English tables 12–16). The pass of C-R01 can be run again with a new map; the plan does not do it.

## 6. Where the moved blocks go, and what else changes with them

- **Place in the supplement:** one new section before "Attribution study (C-ATTR-DEV): every row", holding the moved blocks in their present order, first those of Section 5.7 and then those of Section 6.10, under their present run-in titles. The two moved tables take supplement numbers.
- **The moved blocks are ruled text** (the text package of the attribution study and its transfers). Moved word for word, they need a byte check and no new ruling of content. The summaries are new text and need a ruled text and a one-judge read before they enter the paper.
- **Pointers into the two sections** (counts on the text after package v2). They must be re-read after the cut, because several point to a paragraph that will be in the supplement:

| what is pointed to | occurrences, by file |
|---|---|
| "Section 5.7" in any form | 03: 3; 05: 6; 06: 5; 07: 9; 11: 1 |
| the paragraph "Order of looks" by name | 05: 2 |
| "scoring parity gate" | 05: 1; 06: 2; 07: 3 |
| "Section 6.10" or "Section 6.10.x" in any form | 01: 1 (after block C-V08); 03: 8; 05: 3; 06: 20, beside its own ten headings; 07: 9; 09: 7; 11: 22 |
| "registration §7.x" (paragraphs of the registration) | 06: 11; 11: 4 |

- **Subsection numbers:** 6.10.4 and 6.10.7 are folded into 6.10.3 and 6.10.2, so 6.10.5–6.10.9 change their numbers; the pointers above to "6.10.5", "6.10.8" and "6.10.9" follow.
- **Box 1 and Box 2** name terms and sections of the two sections (A1, K1, D1, the four labels, "positive control"); they are checked with the pointers.
- **Section 7.5** (disclosures of the attribution study) is not in this plan. The answer names Sections 5.7 and 6.10 only; Section 7.5 has about 1,470 words of the same kind and can follow the same three dispositions at the rewrite.
- **Share of new material against the conference version:** the answer chose to keep the study in the main text partly for that share. The plan keeps every result of the study in the main text; the share itself is not computed here.

## 7. What a cut to 1,200 words would cost

The plan lands at the upper end of the range. About 290 more words would have to leave to reach 1,200. The only blocks of that size left in the main text are on the must-stay list:

- the two boxes (102 words) and Section 6.10.9 (191 words), which are limits and NOT RUN statements;
- the two verdict sentences (96 words), which are registered wording;
- the limits of K1 and of the positive control (about 95 words as planned).

A cut below about 1,450 words therefore means dropping or paraphrasing an item of section 4. My recommendation is to stop at about 1,450–1,500 words and, if a shorter text is wanted, to shorten Section 7.5 instead.

## 8. Checks

- Word counts, block limits and running totals were produced by script from the text built in memory ("HEAD after shell C2" plus package v2); the 71 blocks of the table cover the two sections with no gap (5.7: 22 blocks; 6.10: 49 blocks).
- The quoted sentences of section 4 were copied from that text by search, not retyped from memory, except where the item says that one sentence may replace several.
- No test-set file, score ledger, caption file or label file was opened. The plan prints no dataset caption and no model output.
