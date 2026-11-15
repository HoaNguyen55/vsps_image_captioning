# L2 + L4 merged v2 — one letter for the KTVIC dataset and the thesis code base (alternative)

DRAFT, not sent, and NOT COMPLETE: Part B is still a marker. A text file only; whether and when it is sent is the authors' decision (LOG PI-1115b).
This file is the alternative to sending `L2_KTVIC_v2.md` and `L4_THESIS_CODE.md` as two letters (answer F1). The sender chooses one of the two ways, never both.
Use it only if the same person answers for the dataset and for the code base: [TO CONFIRM by the sender]. By answers B3, X4 and F1 it does not go out before the Paper B rating is closed and Part B is written.
Recipient addresses: from the dataset paper or its public repository; none is stored in this file.
v1 (`L2_L4_MERGED.md`) is kept unchanged beside this file. In v2, Part 1 and the dataset half of the subject, the opening and the closing carry the text of `L2_KTVIC_v2.md`; Part 2 and everything else are as in v1.

<!-- LETTER START -->
**Subject:** Our use of the KTVIC dataset: thank you, and what our papers say; and a request for a short written confirmation on the baseline outputs in your thesis-code repository

Dear [recipient: the author who answers for both KTVIC and the thesis-code repository],

We are a research group at [affiliation] working on Vietnamese image captioning. Thank you for the KTVIC dataset (Pham et al., 2024), and thank you for agreeing to our use of it when one of us contacted you. That use includes training. Thank you also for the permission you kindly gave on [TO CONFIRM: date of the conversation, 21 or 22 October 2026] to use the baseline outputs in your repository. Before we submit our papers, we would like to tell you exactly how they use the dataset and what we will release, so that what we print matches what you agreed to (Part 1). For the baseline outputs, we ask for your written confirmation of the points in Part 2. A short reply on Part 2 is enough.

**Part 1. The dataset**

1.1 **Training** (a study of object-hallucination measurement). We trained two adapters of an open vision-language model on the training split (its 3,769 images, with the captions of that split as training targets), and scored them as systems under test. The adapter weights are not released. The matcher we plan to release holds a Vietnamese noun table; 25 of its entries were added by hand after we met those words on KTVIC images or references. The table holds words, not captions.

1.2 **Captions in prompts** (a study of in-context captioning: a journal paper and a shorter conference version). Captions of training images are placed in the prompt of an open vision-language model as examples. They are read at run time from the released file and are not redistributed. A 300-image part of the training file serves as a development set; part of the test file was read again in exploratory diagnostics.

1.3 **Release.** We plan to release code, image identifiers, file hashes and numeric scores, including, if you agree, scores per image listed by image identifier. We release no image, no caption of the dataset and no model caption.

[PART B - to be written after the Paper B rating is closed]

**Part 2. The baseline outputs**

From your repository `thesis-code` (commit 1a8d105, accessed on 22 October 2026) we used the two output files of the ResNet101+LSTM and ViT+Transformer baselines in the folder `simple_evaluate`. We also read the evaluation script in that folder; we did not run it. We ask you to confirm:

2.1 that we may compute aggregate statistics from the two files (corpus-level scores and counts) under the scoring settings of our study, and report them in a journal paper on the scoring of Vietnamese image captions;

2.2 that we may cite your permission as a personal communication, with its date.

We redistribute neither the two files nor any caption from them; readers are pointed to your repository and its commit. The paper ranks no system. The repository carries no licence file; if you prefer a particular form of credit (the thesis, the repository, or both), please tell us.

Without a written reply on Part 2 by [TO CONFIRM: reply-by date, 7–10 days before the planned submission], we will leave these aggregate scores out of the paper and cite no personal communication.

If you would like the dataset acknowledged in a particular way, or would like any particular terms followed, please tell us and we will follow them. If you would prefer any use above to be described differently, a reply by 30 November 2026 would let us change the text before our first submission in early December.

With thanks and kind regards,
[corresponding author], on behalf of the authors
[affiliation]
Copy: [principal investigator], [co-author], [TO CONFIRM: the other authors of KTVIC]
<!-- LETTER END -->

## NOTES (not part of the letter)

**Length.** The text holds the content of two letters and is longer than 350 words (count below; the count in `README.md` is for v1). It was not cut, because every point is one the recipient is told or asked to confirm. If a shorter letter is wanted, send L2 v2 and L4 as two letters.

**Sources.** Part 1 repeats the text of `L2_KTVIC_v2.md` and Part 2 the text of `L4_THESIS_CODE.md`, with no new statement about our work. The source file and line of every statement are in the NOTES tables of those two files. Four statements are worded for this file only:

| Statement | Source |
|---|---|
| The merge is an option if both letters go to the same person | answer F1 in `manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_4b4ec736.md`; LOG line OPS-1115d-author-followup (`.session_backup/2026-10-13/decisions/LOG.md:2634`: "taken as an option in the drafts, to be decided by the sender") |
| Both public repositories exist under the same account | checked by the coordinator (message to this drafter, 2026-11-15); the LOG line above records that both repositories exist, each with a null licence field |
| Subject in two clauses: the dataset clause informs (L2 v2 subject), the code clause asks for a short written confirmation (L4 subject) | `L2_KTVIC_v2.md:9`; `L4_THESIS_CODE.md:7` |
| Opening: the request for written confirmation is tied to Part 2 only, so that Part 1 informs and asks nothing again | `L2_KTVIC_v2.md:6` and `:13` (the agreement is stated as a fact, goal §3); v1 opening of this file for the thanks and the date slot of the oral permission (L4) |

Changes from v1 (`L2_L4_MERGED.md`):
- Subject and opening: the dataset half uses the v2 wording of L2 (thanks, the earlier agreement, "That use includes training", "so that what we print matches what you agreed to"); the thanks for the oral permission and its date slot are kept; "we ask for your written confirmation" now covers Part 2 only.
- The line `[TO CONFIRM: earlier contact about the dataset and its date, or delete this line.]` is removed (as L2-a in v2).
- 1.1, 1.2 and 1.3 carry the v2 text of points 1, 2 and 3 of L2, with the numbering of this file.
- 1.4 Terms (the question under which terms the data may be used) is removed (as L2-d in v2).
- The closing line "If any use needs a different form, please tell us. Our first submission deadline is in early December; a reply by 30 November 2026 would help us greatly." is replaced by the v2 closing paragraph of L2 (the offer to follow any acknowledgement or terms, and the 30 November 2026 reply).
- Unchanged: the salutation, the Part B marker, all of Part 2, the reply-by sentence for Part 2, the sign-off and the copy line.
- Notes: line 4 and the Sources line point to `L2_KTVIC_v2.md`; items M-c, M-d and M-h are closed as in L2 v2.

Word count of the letter text (between the `LETTER START` and `LETTER END` marks, slots included, `wc -w`): 639 (v1: 588).

`[TO CONFIRM]` items:

- M-a. **Same person.** That one account holds both repositories does not show that one person answers for both, or that this person may speak for all authors of the dataset. The sender confirms this before choosing this file. If the consent of the other dataset authors is needed, they go in copy (slot in the copy line) or get L2 v2 instead.
- M-b. **Date of the oral permission** (as L4-a): the Paper B text prints 2026-10-21, the question file says 22 October 2026.
- M-c. **Earlier contact about the dataset**: closed, as L2-a in v2. The slot is replaced by the paper's own clause, with no date and without "in writing" or "on file".
- M-d. **Adapter weights**: closed, as L2-b in v2, by the printed sentence in Paper A.
- M-e. **Scores per image** (as L2-c): drop the clause in 1.3 if the plan is dropped.
- M-f. **Reply-by date for Part 2** (as L4-c): depends on the planned submission date of Paper B. The date 30 November 2026 for Part 1 is a proposal (as L2-e).
- M-g. **Part B.** `[PART B - to be written after the Paper B rating is closed]`
- M-h. **Terms of use**: closed as a question, as L2-d in v2. The letter offers to follow any acknowledgement or terms the authors name. It does not say, and must not be edited to say, that the data are free of terms.
- M-i. **Thread.** Answer F1 adds: if the oral permission of October already sits in a message thread of the principal investigator, the reply for Part 2 may be asked in that thread instead. The principal investigator knows whether such a thread exists.

Slots to fill before sending: `[recipient ...]`, `[affiliation]` (twice), `[corresponding author]`, `[principal investigator]`, `[co-author]`, and the copy slot for the other dataset authors.
