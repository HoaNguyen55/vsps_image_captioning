# L4 — author of the thesis code base (KTVIC baselines)

DRAFT, not sent. A text file only; whether and when it is sent is the authors' decision (LOG PI-1115b). Answer X4 places it after the Paper B rating is closed. The letter holds no result. Alternative: `L2_L4_MERGED.md` joins this letter with L2.
Recipient address: from the repository or the dataset paper; none is stored in this file.

<!-- LETTER START -->
**Subject:** Request for a short written confirmation: use of the baseline outputs in your thesis-code repository

Dear [recipient: author of the thesis-code repository],

Thank you for the permission you kindly gave on [TO CONFIRM: date of the conversation, 21 or 22 October 2026] to use the test outputs of the two KTVIC baselines in your public repository. We are writing to ask for a short written confirmation, because we wish to keep a written record on file before we cite a personal communication. A two-line reply to this message is enough.

**What we used.** From your repository `thesis-code` (commit 1a8d105, accessed on 22 October 2026) we used the two output files of the ResNet101+LSTM and ViT+Transformer baselines in the folder `simple_evaluate`. We also read the evaluation script in that folder to learn how captions are scored; we did not run it.

**What we ask you to confirm.**

1. That we may compute aggregate statistics from the two files (corpus-level scores and counts) under the scoring settings of our study, and report them in a journal paper on the scoring of Vietnamese image captions.
2. That we may cite your permission as a personal communication, with its date.

**What we do not do.** We redistribute neither the two files nor any caption from them; readers are pointed to your repository and its commit. The paper ranks no system.

The repository carries no licence file. If you prefer a particular form of credit (the thesis, the repository, or both), please tell us and we will use it.

If we have no written reply by [TO CONFIRM: reply-by date, 7–10 days before the planned submission], we will leave these aggregate scores out of the paper and cite no personal communication.

Thank you again for your help.

Kind regards,
[corresponding author], on behalf of the authors
[affiliation]
Copy: [principal investigator], [co-author]
<!-- LETTER END -->

## NOTES (not part of the letter)

Repo read: Paper B `/mnt/d/vsps_papers/vsps-paperB-lre` at commit `edf7fee`, only the lines that name the code base. No result of Paper B is used or repeated here.

| Statement in the letter | Source (file:line) |
|---|---|
| The repository holds the test outputs of the two published KTVIC baselines, ResNet101+LSTM and ViT+Transformer; files `result_resnetlstm.json` and `result_vittrans.json` in `simple_evaluate`; commit 1a8d105; accessed 2026-10-22 | Paper B `paper/sec3_data_and_audit.md:36` |
| Used with the permission of the repository's author, cited as a personal communication | same line (it gives the date 2026-10-21) |
| The repository carries no licence | same line; `paper/supplementary_B.md:475` (comment: checked 2026-10-22, no licence file) |
| Aggregate statistics only; none of the outputs redistributed; readers fetch the two files themselves | Paper B `paper/sec3_data_and_audit.md:36` |
| The evaluation script `simple_evaluate/test.py` was read, not run | Paper B `paper/supplementary_B.md:475` (text and its comment "code read, not run") |
| "The paper ranks no system" | Paper B `paper/sec5_results.md:27` ("We rank no Vietnamese system"); answer B5 (ii) rewords it as "We construct no leaderboard ranking of Vietnamese systems" |
| Local copies of the two files are kept outside the release | Paper B `PROVENANCE.md:364-365` |
| A written record is wanted before a personal communication is cited; without it the aggregate scores are not printed | answer B5 (i); answer X4 (letter 3) |

How the code base is credited in the paper today: by the repository address and commit in Supplementary S14 (`paper/supplementary_B.md:475`) and in Section 3.3 (`paper/sec3_data_and_audit.md:36`); the dataset paper is cited as Pham et al., 2024. A search of the Paper B repo for the word "thesis" found no hit in `paper/paperB.bib`, so the code base has no reference-list entry of its own. The letter therefore asks which form of credit the author prefers.

`[TO CONFIRM]` items:

- L4-a. **Date of the permission.** Paper B prints "personal communication, 2026-10-21" (`paper/sec3_data_and_audit.md:36`; the run-repo copy `manuscript/journal_draft_B/sec3_data_and_audit.md:38` has the same). The question file (B5, X4) says 22 October 2026. The principal investigator must give the right date; the paper line and the letter must then agree.
- L4-b. **Channel.** The letter says "the permission you kindly gave" without naming a channel. Answer B5 calls it oral and not on file. If it was given in a message thread, the corresponding author's answer to follow-up F1 suggests replying in that thread instead.
- L4-c. **Reply-by date.** It depends on the planned submission date of Paper B, which no file read here fixes. Answer B3 proposes 7–10 days for a reply.
- L4-d. **Scope wording.** "corpus-level scores and counts" is the scope the paper line states ("aggregate statistics only"). If the rewritten Paper B needs any other statistic from the two files, name it in point 1 before sending.
- L4-e. **Same person as L2?** Answer F1 suggests one merged letter if the dataset letter and this letter go to the same person; the merged text is `L2_L4_MERGED.md`. The coordinator checked that both public repositories exist under the same account (LOG line OPS-1115d-author-followup, `.session_backup/2026-10-13/decisions/LOG.md:2634`). Whether the same person answers for both is for the sender to confirm.

Slots to fill before sending: `[recipient: author of the thesis-code repository]`, `[affiliation]`, `[corresponding author]`, `[principal investigator]`, `[co-author]`.
