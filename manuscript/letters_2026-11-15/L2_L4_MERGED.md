# L2 + L4 merged — one letter for the KTVIC dataset and the thesis code base (alternative)

DRAFT, not sent, and NOT COMPLETE: Part B is still a marker. A text file only; whether and when it is sent is the authors' decision (LOG PI-1115b).
This file is the alternative to sending `L2_KTVIC.md` and `L4_THESIS_CODE.md` as two letters (answer F1). The sender chooses one of the two ways, never both.
Use it only if the same person answers for the dataset and for the code base: [TO CONFIRM by the sender]. By answers B3, X4 and F1 it does not go out before the Paper B rating is closed and Part B is written.
Recipient addresses: from the dataset paper or its public repository; none is stored in this file.

<!-- LETTER START -->
**Subject:** Request for written confirmation: our research use of the KTVIC dataset and of the baseline outputs in your thesis-code repository

Dear [recipient: the author who answers for both KTVIC and the thesis-code repository],

We are a research group at [affiliation] working on Vietnamese image captioning. Thank you for the KTVIC dataset, which we use and cite (Pham et al., 2024), and for the permission you kindly gave on [TO CONFIRM: date of the conversation, 21 or 22 October 2026] to use the baseline outputs in your repository. Before we submit our papers, we ask for your written confirmation of the points below. A short reply, part by part, is enough.

[TO CONFIRM: earlier contact about the dataset and its date, or delete this line.]

**Part 1. The dataset**

1.1 **Training** (a study of object-hallucination measurement). We trained two adapters of an open vision-language model on the 3,769 images of the released training file, as systems under test. [TO CONFIRM: the adapter weights are not released.] The matcher we plan to release holds a Vietnamese noun table; 25 entries were added by hand after we met the words on KTVIC images or references. It holds words, not captions.

1.2 **Captions in prompts** (a study of in-context captioning: a journal paper and a shorter conference version). Captions of training images are placed, as examples, in the prompt of an open vision-language model. They are read at run time from the released file and are not redistributed. A 300-image part of the training file is a development set; part of the test file was read again in exploratory diagnostics.

1.3 **Release.** We plan to release code, image identifiers, file hashes and numeric scores, including, if you agree, scores per image by image identifier. We release no image, no caption of the dataset and no model caption.

1.4 **Terms.** The public repository has no licence file, and its README states no terms. Under which terms may the data be used for training and evaluation in research, and how would you like the dataset acknowledged?

[PART B - to be written after the Paper B rating is closed]

**Part 2. The baseline outputs**

From your repository `thesis-code` (commit 1a8d105, accessed on 22 October 2026) we used the two output files of the ResNet101+LSTM and ViT+Transformer baselines in the folder `simple_evaluate`. We also read the evaluation script in that folder; we did not run it. We ask you to confirm:

2.1 that we may compute aggregate statistics from the two files (corpus-level scores and counts) under the scoring settings of our study, and report them in a journal paper on the scoring of Vietnamese image captions;

2.2 that we may cite your permission as a personal communication, with its date.

We redistribute neither the two files nor any caption from them; readers are pointed to your repository and its commit. The paper ranks no system. The repository carries no licence file; if you prefer a particular form of credit (the thesis, the repository, or both), please tell us.

Without a written reply on Part 2 by [TO CONFIRM: reply-by date, 7–10 days before the planned submission], we will leave these aggregate scores out of the paper and cite no personal communication.

If any use needs a different form, please tell us. Our first submission deadline is in early December; a reply by 30 November 2026 would help us greatly.

With thanks and kind regards,
[corresponding author], on behalf of the authors
[affiliation]
Copy: [principal investigator], [co-author], [TO CONFIRM: the other authors of KTVIC]
<!-- LETTER END -->

## NOTES (not part of the letter)

**Length.** The text holds the content of two letters and is longer than 350 words (count in `README.md`). It was not cut, because every point is one the recipient is asked to confirm. If a shorter letter is wanted, send L2 and L4 as two letters.

**Sources.** Part 1 repeats the text of `L2_KTVIC.md` and Part 2 the text of `L4_THESIS_CODE.md`, with no new statement about our work. The source file and line of every statement are in the NOTES tables of those two files. Two statements are worded for this file only:

| Statement | Source |
|---|---|
| The merge is an option if both letters go to the same person | answer F1 in `manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_4b4ec736.md`; LOG line OPS-1115d-author-followup (`.session_backup/2026-10-13/decisions/LOG.md:2634`: "taken as an option in the drafts, to be decided by the sender") |
| Both public repositories exist under the same account | checked by the coordinator (message to this drafter, 2026-11-15); the LOG line above records that both repositories exist, each with a null licence field |

`[TO CONFIRM]` items:

- M-a. **Same person.** That one account holds both repositories does not show that one person answers for both, or that this person may speak for all authors of the dataset. The sender confirms this before choosing this file. If the consent of the other dataset authors is needed, they go in copy (slot in the copy line) or get L2 instead.
- M-b. **Date of the oral permission** (as L4-a): the Paper B text prints 2026-10-21, the question file says 22 October 2026.
- M-c. **Earlier contact about the dataset** (as L2-a).
- M-d. **Adapter weights** (as L2-b).
- M-e. **Scores per image** (as L2-c): drop the clause in 1.3 if the plan is dropped.
- M-f. **Reply-by date for Part 2** (as L4-c): depends on the planned submission date of Paper B. The date 30 November 2026 for Part 1 is a proposal (as L2-e).
- M-g. **Part B.** `[PART B - to be written after the Paper B rating is closed]`
- M-h. **Terms of use** (as L2-d): the letter asks under which terms the data may be used. It does not say, and must not be edited to say, that the data are free of terms.
- M-i. **Thread.** Answer F1 adds: if the oral permission of October already sits in a message thread of the principal investigator, the reply for Part 2 may be asked in that thread instead. The principal investigator knows whether such a thread exists.

Slots to fill before sending: `[recipient ...]`, `[affiliation]` (twice), `[corresponding author]`, `[principal investigator]`, `[co-author]`, and the copy slot for the other dataset authors.
