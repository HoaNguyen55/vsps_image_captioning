# Human completion of the object gold on XM3600-600: labelling plan v1 (2026-11-11)

Scope of this file: how the labels are collected, kept and may be used. It registers no hypothesis. The hypotheses that use the labels go into a separate analysis registration, which must be committed before any label value is opened by anyone other than the annotator. Judgements are AI opinion.

## 1. What is labelled and why
- **Set.** The 600 Crossmodal-3600 images of Paper A's Vietnamese test (`data/datasets/xm3600/test_data.json`). Paper A has analysed these images before: its registered look is spent and the images have a development role. The labels are new.
- **Unit.** One (image, lexicon class) pair. Question: "is an object of this class in the image?"
- **Why.** The Open Images V7 human-verified labels settle only part of the classes that captions name. Paper A therefore reports the label-gold slope under verified precision, with a post hoc bound for the unsettled mentions (Supplementary S7.2). Human answers for the unsettled pairs replace the bound by a measurement and give a human-completed gold against which a method can be tested.
- **Who names a pair.** Twelve stored caption sets (six systems of Section 6.2; the second backbone's six XM600 runs, `g2b_q3_xm600-{short,detailed}-T{0,05,08}`) and the Vietnamese references. Classes come from the paper's matcher (`rescap.chair.objects_in`). No caption is shown or written anywhere in the labelling files.
- **Rule status.** This is a second human-labelled set, beside the ViHal set approved on 2026-11-10 (PI-1110i). It needs the PI's explicit yes before the first label (requested in chat on 2026-11-11; to be logged).

## 2. Items (built by `tools/obj_rater/build_assignment.py`, seed 20261111)
| Part | Content | Questions |
|---|---|---|
| 1 | Named pairs whose class has an Open Images mapping and whose status is unknown (1,790), mixed per image with hidden controls: 143 named pairs verified absent, 200 named pairs verified present (random), 100 unnamed pairs verified absent (random) | 2,233 |
| 2 | Named pairs whose class has no Open Images mapping | 2,100 |
| 3 | 150 random part-1 targets asked again | 150 |

Total 4,483 questions on 1,288 screens (one image per screen, 598 images with a target). Part 1 comes first: it is the bucket that the registered verified-precision estimand and the S7.2 bound cover. Image order inside a part and question order inside a screen are random with the fixed seed.

- **Wording.** A mapped class is shown with the Open Images classes of `data/xm3600/vi_oiv7_map.json` ("Open Images: …"), and the annotator is told to read the class by them, so that controls and targets measure the same construct as the Open Images labels. An unmapped class is shown by its lexicon word alone.
- **Answers.** Có (Y), Không (N), Không xác định được (U: the image cannot settle it), Tên lớp mơ hồ (A: the word does not name an object category). Depictions (drawings, statues, printed pictures) count as present. Partly hidden or small objects count as present.
- **Practice.** 15 XM3600 images outside the 600, questions with an Open Images answer, feedback shown. Practice answers are not data.

## 3. Blinding and custody
- The page shows the image, the class and the hint. It carries no caption, no system name, and no mark of which question is a target, a control or a repeat (`key.json` holds that and is not served; sha256 a2cef894…).
- The annotator today is the PI, who knows the study. He cannot see which system or reference named a class. This is disclosed wherever the labels are used.
- Every answer is appended to `~/vsps_labels/xm600_gold/labels_<annotator>.jsonl` on the Linux home filesystem (append-only, fsync per answer; a changed answer is a new line, the last line wins, all lines are kept).
- The coordinator and agents read line counts only. Nobody but the annotator opens label values before the analysis registration is committed. At the end of each session the file's sha256 and line count go into the LOG.

## 4. Quality measures (fixed now)
- **Against Open Images.** Share of the 443 control questions on which Y/N equals the Open Images label, with U and A reported apart. Reported whatever its value.
- **Within annotator.** Agreement of the 150 repeats with the first answer.
- **Second annotator.** A colleague labels every question of the 150 images in `overlap_images.txt` (25 % of the images with a target; drawn with the fixed seed), with the same page and the same instructions, without seeing the first answers. Statistic: Cohen's kappa on Y against N over questions that both answered Y or N; the U and A rates of each annotator are reported beside it.
- **Rule.** Kappa at or above 0.60: the first annotator's labels are used as the completed gold and kappa is reported. Kappa below 0.60: label-based results are reported as a sensitivity analysis only, with the disagreement table. Until the second annotator has labelled, every label-based number carries the words "single annotator".

## 5. What the labels may estimate (fixed before any value is opened)
- **Completed status.** A named pair is present if Open Images verifies it present or the human answer is Y; absent if Open Images verifies it absent or the answer is N; U and A stay unsettled and are counted. An Open Images label is never overridden by a human answer; the control questions measure the disagreement.
- **Precision (primary).** Per system, completed precision on mapped classes = present / (present + absent) over its named mapped classes. This is the registered verified-precision formula with fewer unsettled mentions. The same quantity over mapped and unmapped classes together is secondary (part 2).
- **Recall and F1.** Completion adds present classes only where some caption named them, and the most verbose system names most. So recall and F1 are reported under two golds and never mixed: (i) the gold for recall unchanged (Open Images verified-present classes, as registered); (ii) Open Images plus human Y, labelled "pooled gold; favours systems that name more". No verdict attaches to (ii).
- **Not estimated.** The labels do not say whether a caption's wording was right (the matcher's lexical ambiguity stays; the A rate measures part of it), and they are not a complete inventory of the image.

## 6. Later sessions
- The approved other-family model arm on these images (PI-1105k, PI-1107c) will name new pairs. They get a top-up session with the same page, wording and rules; its items are built by the same script from the new caption files.
- Part 2 may be finished on another day; partial part-2 labels are not used.

## 7. Limits
One annotator today, who is the PI. Class-level labels, not mention-level. Images and captions were analysed before; only the labels are new, so every result that uses them is described as "new labels on previously analysed captions", registered before the labels were opened.

## 8. Pin package (sha256, first 16 hex digits)
| File | sha256 |
|---|---|
| `tools/obj_rater/build_assignment.py` | 497e57479197faba |
| `tools/obj_rater/server.py` | e3beb9363eba8b99 |
| `tools/obj_rater/rater.html` | 160e0c7efe86c89d |
| `assignment.json` (this folder; equals the served file) | 55e07337218acc82 |
| `practice.json` | e0ed805b31fc623d |
| `overlap_images.txt` | 4f9719667c8a9294 |
| `key.json` (private, `~/vsps_labels/xm600_gold/`) | a2cef89475675b66 |

`BUILD.json` in this folder lists the counts and the sha256 of every input file. Checks run: endpoint test (private files not served; bad requests refused), headless page test on the practice round (answers, feedback, next, back, resume), load-only test of the main page.
