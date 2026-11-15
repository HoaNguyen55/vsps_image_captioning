# Paper A (SPIC): full read of printed Sections 6 (to 6.6), 7, 8, 9 and the declarations

Written 2026-11-15T11:20Z (18:20 Vietnam time). Audit item A6-02 of `manuscript/READY_AUDIT_A_2026-11-15.md`. Read-only: no paper file was changed, nothing was staged or committed.

## 1. What was read

Paper repo `/mnt/d/vsps_papers/vsps-paperA-spic`, HEAD `0b542cf`, `paper/` clean. File numbers and printed numbers differ; this report uses the printed numbers and gives the file and line for every finding.

| File (sha256 prefix at HEAD) | Printed section | Lines read |
|---|---|---|
| `sec6_rescoring_published_methods.md` | none (comment only, no printed text) | 1 |
| `sec7_verbosity_sign.md` (`b6f46b8aaf33`) | Section 6, up to the end of 6.6 | 1–123 only |
| `sec8_human_validity.md` (`4572367c38fb`) | Section 7 | all |
| `sec9_preference_audit.md` | none (comment only, no printed text) | 1 |
| `sec10_discussion.md` (`d48ce382b275`) | Section 8 | all |
| `sec11_limitations_ethics.md` (`dff441d598ae`) | Section 9 | all |
| `declarations.md` (`3b2381ca23d2`) | Declarations | all |

Context only: `outline.md` (headings), `abstract_A.md`, `sec1_introduction.md`, Sections 3.3, 3.6, 3.7 and 4.2, and the published supplement before S11 (lines 1–1171) where a main-text sentence points to it. Registration texts used: `prereg/2026-10-28_pascal50s/PREREG.md` (`1448ab13fcb5`) §9; `prereg/2026-10-29_a_companion/RULE.md`; `prereg/2026-10-30_a_g0/NOTE.md`; `prereg/2026-10-30_a_t3/PREREG.md` §0 and §7.

Not read: `sec7_verbosity_sign.md` from line 124 (the heading of Section 6.7) to the end, and the supplement from `## S11`. Not opened: any label folder, key file, label file or `gt_cache.json`.

Fix package v6 was read in full. Nothing it fixes is reported again (3,419 in Section 7.2; the Part P and Part V glosses in Section 9.1; the heading of the declarations; the supplement headings).

## 2. How each check was done

- **(a) Numbers.** Every decimal, percentage and integer of 100 or more in the printed text was looked up in column 1 of `number_manifest.tsv` (`dd2bce1797bb`). All are there with the same value, except 3,419 (in package v6). Four tokens differ in form only: −36.60 (manifest −36.6), +4.80 (4.8), 6.94 and 1.59 (6.944 and 1.593), and the setting T = 0.8. Signs and the meaning of each row were checked by reading for the values named in the findings. Integers below 100 are not covered by the script; those checked by hand are in F45.
- **(b) Citations.** 21 author-year mentions in the lines read; each resolves to one key in `paperA.bib`. `paperA_manual.bib` holds no entry.
- **(c)–(f)** by reading each sentence against Table 1, Sections 3.3, 3.6, 4.2, the other sections read, and the registration texts above.
- **Internal ids and history wording.** No decision id, ruling id or revision word is printed in the lines read (the pattern hits are inside comments).

## 3. Findings

Classes: (a) number, (b) citation, (c) contradiction, (d) claim against its label or its evidence, (e) undefined term, internal label or cross-reference, (f) English, (g) the registered caveat of Section 6.4.

| Id | File:line (printed section) | Class | Severity | OLD (exact, short) | NEW or action |
|---|---|---|---|---|---|
| F01 | `sec7_verbosity_sign.md:86` (6.4) | g, d | SHOULD | `and the label-gold part is listed in Table 1 as FAIL. Under the registered data-handling rule,` | See Section 4 of this report: the registered third sentence goes between these two sentences. |
| F02 | `sec7_verbosity_sign.md:45` (6.2) | e | SHOULD | `(times: Supplementary S10)` | `(times: Supplementary S4)`. The XM3600 commit and first-output times are printed in S4 (published supplement l.332, l.350, l.405); S10 prints no time. Sections 3.6 and 7 already point to S4. |
| F03 | `sec7_verbosity_sign.md:5` (6, lead) | c | SHOULD | `and the multi-reference sign is not predicted.` | `and the multi-reference sign is not predicted by the theory; it was registered as positive on XM3600 and failed (Section 6.2).` Section 6.2 l.49 reports the registered prediction "All-references slope > 0: FAIL", and Section 4.2 says the sign "was predicted positive and failed". |
| F04 | `sec7_verbosity_sign.md:100` (6.5) | c, d | SHOULD | `we refitted every cell of Table 6.1 with each system left out in turn` | `we refitted the one-reference, all-references and label-gold slopes of every family of Table 6.1 with each system left out in turn (clean subsets for the second backbone; the bracket columns were not refitted)`. Supplementary S7 says: "under the lower rule of the bracket no leave-one-out fit was computed", and Table S7.8 has no all-image row. |
| F05 | `sec7_verbosity_sign.md:100` (6.5) | d | SHOULD | `no single drop changes the sign of the label-gold slope in any family (smallest leave-one-out slope +1.49)` | Add after it: `under the registered precision rule; its system-jackknife interval includes 0 for the two English LVLM families and for UIT-ViIC with the Vietnamese lexicon (Supplementary Table S7.8)`. Both facts are in Supplementary S7 and are left out of the main text, which gives only the favourable half. |
| F06 | `sec10_discussion.md:29` (8.5) | c, d | SHOULD | `its positive sign under human-verified labels holds only when unverifiable mentions are excluded` | `when unverifiable mentions are counted as errors the slope stays positive at point level on both backbones, but its interval includes 0 on the second (+1.97 [−0.44, +4.01])`. The sign does not fail under the error-counting rule: Section 6.2 prints +5.83 [+3.82, +7.82] for the first backbone (manifest rows 657, 658), and Section 9.1 l.11 states it correctly. |
| F07 | `sec7_verbosity_sign.md:57` (6.2) | c | MINOR | `so the positive label-gold slope depends on excluding unverifiable mentions` | `so on the second backbone the interval of the label-gold slope excludes 0 only when unverifiable mentions are excluded`. Same point as F06. The same wording stands in `sec1_introduction.md:11` (outside this read). |
| F08 | `sec10_discussion.md:7` (8.1) | c | SHOULD | `the label step, a change of completeness plus precision rule (Table 6.2),` | `the label step, a change of gold and of precision rule (Table 6.2),`. Section 6.2 says "The label step is not a step in completeness by size" and Table 6.2 gives the label gold as 0.87 times all references. |
| F09 | `sec7_verbosity_sign.md:90` (6.4) and `:57` (6.2) | e, f | SHOULD | `Counted after the result without model outputs: On all 1,000` … `so the comparison is approximate;` | (1) The terms "label rung" and "the 2x convention" are used here and nowhere defined in the main text; l.57 points to "the 2× size convention of Section 6.4", which Section 6.4 never states. (2) The two sentences from "On all 1,000" to "stands as registered." are an outcome text fixed before the count (Supplementary S7), which explains the capital after the colon; the main text does not say so. (3) "so the comparison is approximate" does not follow from the clause before it; the supplement gives the reason. Proposed: `Counted after the result, without model outputs. By the convention of the X5 evaluability rule (Section 6.6), a gold counts as substantially more complete only if its size is at least twice that of the gold it is compared with (the 2× convention; a "rung" is a gold level). The outcome sentence was fixed before the count: "On all 1,000 … stands as registered." The registered X5 numbers already implied this outcome (1,782 VOC pairs on the 997-image analysis set against 2 × 1,039.6; Section 6.6); the analysis set cannot be rebuilt, so the comparison of 1,782 with 1,787 is approximate; per-class rows are in Supplementary S7.` Sources: `prereg/2026-10-30_a_g0/NOTE.md` l.43–46; published supplement l.774. Write "2×" in both places. |
| F10 | `sec7_verbosity_sign.md:122` (6.6) | e | SHOULD | `and X4, in the Holm family by its tier-1 power rule, passed` | `and X4, which entered the Holm family by its pre-written power rule (Supplementary Table S4.0, row A28), passed`. "tier-1" is an internal stage name, printed once and never defined. The registered paper-facing text (`2026-10-30_a_t3/PREREG.md` §7) says "its pre-written power rule". |
| F11 | `sec7_verbosity_sign.md:104` (6.6) and `sec11_limitations_ethics.md:13` (9.1) | c, e, f | SHOULD | `the 50-reference consensus (the union of the classes named in all 50 references)` and `a consensus-gold sensitivity (classes named by at least two references)` | "Consensus" means the union in Section 6.6 and "named by at least two references" in Section 9.1. "50-reference consensus" is the registered name (`RULE.md` l.35, l.104), so keep it and change the other. 6.6: `the 50-reference consensus (the union of the classes named in at least one of the 50 references)` ("named in all 50" reads as the intersection). 9.1: `a sensitivity analysis that keeps only classes named by at least two references was not computed`. |
| F12 | `sec10_discussion.md:7` (8.1) | f, e | SHOULD | `1,787 VOC label instances against 2,162 classes named in the 50 references` | `1,787 image–class pairs in the VOC labels against 2,162 named in the 50 references`. Both counts are image–class pairs (Supplementary S7: per image, classes of the label set against classes of the 50-reference set); "instances" reads as object instances. Section 6.6 l.108 already says "image–class pairs". The wording "class instances" inside the fixed sentence of Section 6.4 l.90 cannot be changed; the gloss of F09 can add "(image–class pairs)". |
| F13 | `sec11_limitations_ethics.md:25` (9.1) | e | SHOULD | `conditional on the floor (F$_w$) and on (A0), (A1) and (A1+)` | (F$_w$) and (A1+) are printed nowhere else in the main text before Section 6.7, and (A0) not before it either. Add the pointer to the supplement subsection that states them, in the form `(stated in Supplementary S11.x)`; the subsection number has to be filled by the agent that reads S11. |
| F14 | `sec11_limitations_ethics.md:53` (9.2) and `declarations.md:19` | c, f | SHOULD | `whether they will be released is not yet decided` | The Data availability statement says nothing about the new human labels, and Section 9.2 prints an open decision. One sentence is needed in both places once the investigator decides (release, or "are not released; aggregates only"). Decision for the investigator. |
| F15 | `declarations.md:19` | c | SHOULD | `The reference captions and human-judgment ratings of COCO, XM3600, UIT-ViIC, UIT-OpenViIC, LongCap-Arena, THumB, Polaris and DOCCI-Critique are not redistributed` | The list leaves out sets the paper uses: Composite and M-HalDetect (Sections 7.2, 7.3, 9.2), Flickr30k (Table 5.1), ADE20K with Localized Narratives (Section 6.4) and the seven preference sets (Section 7.3). Add them, or close the list with `and of the other third-party sets named in Sections 5–7`. No agreement clause is touched. |
| F16 | `declarations.md:23` | f, e | SHOULD | `It uses the same fine-tuned instrument.` | The sentence does not say what the instrument is (the matcher, or the adapters of Section 6.2). Name it. The supplement (S2) says the companion manuscript documents the matcher versions; the writer must confirm which is meant. |
| F17 | `sec11_limitations_ethics.md:17` (9.1) | f | SHOULD | `a rehearsed assessment of the method depended on the checks against his labels` | A reader cannot tell what "a rehearsed assessment" is. Say in plain words what the annotator was told. Same paragraph, MINOR: `The single annotator is an author.` repeats the first sentence (delete); `for a general lean` → `for a general bias`. |
| F18 | `sec7_verbosity_sign.md:28` (Table 6.2 caption) | d | MINOR | `(post hoc descriptive, no verdict)` | The COCO val2017 row holds the registered premise ratios (2.149 measured before decoding; 1.395 gives PREMISE_NOT_MET; Section 6.4). Proposed: `(post hoc descriptive, no verdict; the COCO val2017 ratios are the registered premise values of Section 6.4)`. |
| F19 | `sec7_verbosity_sign.md:55` (6.2) | f | MINOR | `the one-reference non-empty gold size missed its interval (1.8768 against 1.8831; OUT; Supplementary S7)` | `the mean one-reference gold size over images with a non-empty gold was 1.8768 against a registered 1.8831 (OUT; Supplementary S7)` (manifest rows 223, 224). |
| F20 | `sec7_verbosity_sign.md:57` (6.2) | f | MINOR | `(in-sample 0.503 against 0.549)` | `(in-sample exponent 0.503 against the transferred 0.549)` (manifest rows 239, 494). |
| F21 | `sec7_verbosity_sign.md:52` (6.2) | f, e | MINOR | `**Sign agreement with $M^*_{\text{mixed}}$ − median $M$: FAIL.** It holds for 3 of 4 gold variants` | `**The slope sign agrees with the sign of $M^*_{\text{mixed}}$ − median $M$: FAIL.**` and name the four gold variants once (the section names three golds). |
| F22 | `sec7_verbosity_sign.md:45` (6.2) | e | MINOR | `one with the gold-SFT recipe of an earlier study` | `one with the fine-tuning recipe of an earlier study` ("gold-SFT" is not defined). Same line: `The exponent is transferred` → `The exponent $b$ of the frontier (Section 3.7) is transferred`. |
| F23 | `sec7_verbosity_sign.md:39` (6.1) | f | MINOR | `as did the OPERA instance-gold prediction (+4.24 [−0.09, +8.51])` | The point is positive, so a reader cannot see why "slope > 0" failed. Add the rule, for example `(its interval includes 0)`, after checking the pre-specified rule in Supplementary S7. |
| F24 | `sec7_verbosity_sign.md:69` (6.3) | f | MINOR | `Rise at every added reference (G2B-O2): **PASS** on COCO-295 and UIT-ViIC-231.` | Add `(not registered on XM3600-600)`; Table S7.5 marks that set "not registered", and the sentence leaves the third set unexplained. |
| F25 | `sec7_verbosity_sign.md:73` (6.3) | a, f | MINOR | `(−1.124 [−11.52, 6.62]; point ≤ 0)` | `(−1.124 [−11.52, +6.62]; point ≤ 0)`: the upper bound has no sign here and has one in the manifest (row 625) and in every other interval of the section. |
| F26 | `sec7_verbosity_sign.md:77` (6.4) | f | MINOR | `(the fixed 8 GPU-hour cap dropped Idefics3-8B)` | `(Idefics3-8B was dropped under the pre-fixed cap of 8 GPU-hours)`. |
| F27 | `sec7_verbosity_sign.md:96` (6.4) | f | MINOR | `after a pre-specified filter and 6 unclean drops` | `after a pre-specified filter and 6 images dropped as unclean`. This is the opening clause, which the paragraph already says differs from the registered wording. The clause `three LLM families, two Qwen-family` is registered wording and stays; it is hard to read, and one added sentence after the registered block could name the two models. |
| F28 | `sec7_verbosity_sign.md:100` (6.5) | f | MINOR | `On XM3600 the ordering holds in all 6 leave-one-out fits` and `On the second backbone the one-reference sign is stable (−12.52 to −11.86)` | `in all 6 first-backbone leave-one-out fits` (as in Section 1) and `On the second backbone's XM3600-600 runs` (the range is that set only; manifest rows 843, 844). |
| F29 | `sec7_verbosity_sign.md:122` (6.6) | f | MINOR | `so X4 and X5 are the registered tests here that can reject uniform deletion only in that nested form, not random omission by individual references` | `so X4 and X5 can reject uniform deletion only in that nested form; they cannot reject random omission by individual references`. Same line and l.104: SCAR is written out as "selected completely at random" in l.104 and Section 2, and as "missing completely at random (SCAR)" here; use the first form. |
| F30 | `sec8_human_validity.md:6` (7, lead) | f | MINOR | `among same-image caption pairs where both differ` | `among same-image caption pairs in which both the score and the judgment differ`. |
| F31 | `sec8_human_validity.md:16` (7.1) | f | MINOR | `Relevance falls by 0.024 per additional COCO class [−0.029, −0.020]` | `Relevance changes by −0.024 [−0.029, −0.020] per additional COCO class` (the sign of the point and of the interval then agree; manifest row 358). |
| F32 | `sec8_human_validity.md:22` (7.2) | f | MINOR | `the second part is a **FAIL** under the registered rule "point ≤ 0" whose interval includes 0, so the registered outcome is not supported` | `the second part is a **FAIL** under the registered rule (point ≤ 0), although its interval includes 0, so the registered prediction is not supported`. |
| F33 | `sec8_human_validity.md:28` (7.3) | e, f | MINOR | `RLAIF-V's (Yu et al., 2025) chosen-fewer share` and `inside the kill interval [0.45, 0.55]` | `The chosen-fewer share of RLAIF-V (Yu et al., 2025)` and `inside the registered withdrawal interval [0.45, 0.55]`. "Kill" is used once in the main text; every other place says "withdrawal rule". |
| F34 | `sec10_discussion.md:7` (8.1) | f, c | MINOR | `its tally is mixed: PASS on XM3600 … and FAIL on PASCAL-50S (Section 6.4)` | The tally leaves out COCO val2017 (label over one reference PASS; against five references PREMISE_NOT_MET), which Sections 6.4 and 8.5 count. Add one clause. Also: the paragraph is one block with five bold lead-ins, some ending in a full stop and some in a colon, one followed by a capital; split it into paragraphs and use one form. |
| F35 | `sec10_discussion.md:29` (8.5) | f | MINOR | `(six systems of one backbone, in effect a short-versus-detailed contrast)` and `one-reference gold fell below a size-matched random-deletion null` | After a sentence that names both backbones the bracket is ambiguous: `(six systems per backbone; in effect a short-versus-detailed contrast)`. And `the one-reference slope fell below a size-matched random-deletion null` (a gold does not fall below a null). |
| F36 | `sec11_limitations_ethics.md:9` (9.1) | f | MINOR | `the UIT-ViIC pass is not counted` | `the UIT-ViIC pass is not counted as support`. |
| F37 | `sec11_limitations_ethics.md:19` (9.1) | e | MINOR | `(the A answer measures part of it)` | "The A answer" is not explained outside Section 6.7. To be checked by the agent that reads 6.7: either it is defined there before this use, or a gloss is needed here. |
| F38 | `sec11_limitations_ethics.md:21` (9.1) | f | MINOR | `so about 9 of its 15 pairs are short-against-detailed and 6 are near-copies` | `so 9 of its 15 pairs are short-against-detailed and 6 are near-copies` (3 × 3 = 9 and 2 × 3 = 6 exactly). |
| F39 | `sec11_limitations_ethics.md:23` (9.1) | f | MINOR | `every label-based result is "new labels on previously analysed captions"` | `every label-based result carries the label "new labels on previously analysed captions"`. |
| F40 | `sec11_limitations_ethics.md:50–51` (9.2) | f | MINOR | l.51 `**PASCAL-50S outputs.**` follows l.50 with no empty line | Insert an empty line; without it the two paragraphs are built as one. |
| F41 | `sec11_limitations_ethics.md:57` (9.3) | f | MINOR | `we do not aim to discredit specific methods, report the full specification curve, and recommend` | `we do not aim to discredit specific methods; we report the full specification curve and recommend` (as written, "do not" can be read with all three verbs). |
| F42 | `sec11_limitations_ethics.md:31` (9.1) and `declarations.md:27` | f | MINOR | `had not been scored at the time of writing` | Status wording; update with the items of audit A1-01 at submission. No change now. |
| F43 | `declarations.md:23` | f | MINOR | `this paper's 600 Crossmodal-3600 images` | `this paper's 600 XM3600 images` (the name used in the rest of the paper). |
| F44 | spelling, several lines | f | MINOR | `penalize` (`sec8_human_validity.md:16`, `sec10_discussion.md:7`, `:11`); `judgements` (`sec11_limitations_ethics.md:19`) | Section 6.6 and Section 8.1 also print "penalising", which is the registered X4 wording. Use one form: `penalise` in the three places, and `judgments` as in the rest of the paper. |
| F45 | `sec7_verbosity_sign.md:66` (6.3) and `:94` (6.4) | a | MINOR | `all 23 registered decodes` and `negative for two of seven models` | Neither count has a manifest row. Sources are in the line comments: `data/results/g2b/g2b_score_record/` (precheck 23/23) and `p50_decide.json` :: `PAIR_m_descriptive.*.voc20\|V20`. Add two rows. Other small counts checked and found keyed: 6 dropped (row 1402, labelled "Flickr-identifier drops": the label and the printed word "unclean" should be made to agree), 14 of 15 (row 226), 8 of 8 and 4 of 4 (rows 1240, 1241), 443 (row 1439). |
| F46 | `declarations.md:11` | f | MINOR | `The authors declare no competing interests.` | Check against the publisher's standard sentence when the guide for authors is read (audit A5-09). No change now. |

## 4. Finding F01 in full: the registered caveat sentence of Section 6.4 (ruling CC-412, item N1)

**Place.** `sec7_verbosity_sign.md:86`, the paragraph that begins "On PASCAL-50S the registered ordering did not replicate". Its first two sentences are the registered branch text 9.2 of `prereg/2026-10-28_pascal50s/PREREG.md` (l.379) with the blanks filled and "Section 7.2" printed as "Section 6.2". The registered text has a third sentence, which is not printed. It belongs directly after "…and the label-gold part is listed in Table 1 as FAIL." and before "Under the registered data-handling rule, all 14 caption files…".

**Proposed sentence** (the registered sentence, word for word; nothing added):

> The images and captions have been public since 2008–2015 and may be in the pretraining data of these models; they are unseen by us, not necessarily by the models.

**What the coordinator must weigh.** The heading of §9 of the registration says the branch texts are "inserted as written once there is a verdict". Against that, the investigator's decision PI-1105m (PQ1) removed caveats of the kind "models may have seen these images" and kept one neutral sentence, which stands in Supplementary S7: "We did not examine the pretraining data of the evaluated models." PI-1110n later replaced the rule that PI-1105m applied. Two ways are open:

1. **Restore** the sentence above at the place given. It states no overlap fact and makes no claim that there is none.
2. **Record the deviation** and leave the main text as it is. Add to the deviation notes of Supplementary S4, and to the source comment of l.86: `The registered text for this outcome has a third sentence, which Section 6.4 does not print: "The images and captions have been public since 2008–2015 and may be in the pretraining data of these models; they are unseen by us, not necessarily by the models."`

My recommendation is way 1 (confidence about 70%): the registration asks for the text as written, and the sentence is a caution, not an overlap statement. Way 2 is the default if the investigator's earlier decision is taken to still bind. With way 1 the paragraph can also say, truthfully, that its first three sentences follow the registered text with the blanks filled and the section number updated (the sentence that CC-412 Ruling 3 skipped because the list was incomplete).

**The same check for COCO val2017** (CC-412 N1, last sentence). The paragraph at `sec7_verbosity_sign.md:96` was compared with the "Joint PASS" text of `prereg/2026-10-30_a_t3/PREREG.md` §7 (l.231–238). Every registered sentence is printed, in the registered order, with the blanks filled; the opening clause differs and the paragraph says so. No sentence is missing. No finding.

## 5. Sentences outside Section 6.7 that state outcomes of the held study (location only)

- `sec7_verbosity_sign.md:57` (Section 6.2, the clause that ends with a pointer to Section 6.7.2)
- `sec10_discussion.md:7` (Section 8.1, the last sentence, on Supplementary S11)
- `sec10_discussion.md:29` (Section 8.5, four sentences)
- `sec11_limitations_ethics.md:11` (Section 9.1, the last sentence)

`sec11_limitations_ethics.md:15–31` describe the design and the limits of the held study and print no outcome figure of it. They were read for terms and English only (F13, F17, F37, F38, F39, F42).

## 6. Counts

| Severity | Findings |
|---|---|
| BLOCKING | 0 |
| SHOULD | 16 (F01–F06, F08–F17) |
| MINOR | 30 (F07, F18–F46) |
| **Total** | **46** |

By file: `sec7_verbosity_sign.md` 22 (F01–F05, F07, F09–F11, F18–F29, F45); `sec8_human_validity.md` 4 (F30–F33); `sec10_discussion.md` 5 (F06, F08, F12, F34, F35); `sec11_limitations_ethics.md` 10 (F13, F14, F17, F36–F42); `declarations.md` 4 (F15, F16, F43, F46); several files 1 (F44). F11, F14 and F42 also name a line in a second file.

By first class: (g) 1; (c) 8; (d) 2; (e) 7; (a) 2; (f) 26; (b) 0.

No finding is BLOCKING: no number disagrees with the manifest, no citation is missing, and no registered verdict token is changed or reworded in the lines read.

## 7. Read in full with no finding

- Section 6: Table 6.1 (all rows and the caption; every value matches the manifest); Section 6.3 "Design", the paragraph on the registered primary claims and "Primary result" apart from F45; Section 6.4 "Design" apart from F26, the four registered verdict bullets (l.79–83), "Without a verdict" (l.88) and "System dependence" (l.94) apart from F45; Section 6.6 bullets X4, X5 and Multiplicity (l.106–109; the arithmetic 2 × 1,039.6 = 2,079.2 and both excess values agree with the ranges) and Table 6.3 with its caption.
- Section 7: "Registration" (l.8); Section 7.1 l.12–14 and bullets (ii) and (iii).
- Section 8: 8.2, 8.3 (the checklist agrees with Sections 3.3, 3.7, 5 and 7.3) and 8.4.
- Section 9.1: "Construct validity: precision rule" apart from the held sentence; "reference-only bound"; "Development and post hoc rows"; "Prior work"; "vocabulary and matchers"; "Internal validity: count control" (agrees with Sections 1 and 3.3); "system dependence and multiplicity" (agrees with Sections 3.6 and 6.6); "External validity" (7 backbones, MIXED for DOCCI-Critique and the count-neutral statement agree with Supplementary S4 and S8).
- Section 9.2: "UIT-OpenViIC and UIT-ViIC", "KTVIC", "Licences of human-judgment data", "PASCAL-50S outputs" and "Released evaluation logs" apart from F14 and F40. The agreement clauses were read and are not touched by any finding.
- Declarations: CRediT statement, Funding, Ethics (apart from F42).
- The counts of Table 1 agree with the sections read: nine FAIL (A24, A2, A5, A10, A14, A15, A18, A19, A21), four inconclusive, one not evaluable, one gold-size value out.

## 8. Seen outside the scope of this read (not counted)

- `sec1_introduction.md:46` and `:48` (Table 1): the rows X-22 to X-25 give Sections 6.2–6.4, 6.6, 7 and 3.3, 6, 7 as their place, but Table S4.0 marks them "this table only" and no section read here reports them. Table 1 lists X-22 under MIXED, and Table S4.0 gives its verdict as "PASS, with a mixed estimator". For the reader of Section 1 and S4.
- Table S4.0, row A28 (published supplement l.309) also prints "tier-1 power rule" (see F10).
