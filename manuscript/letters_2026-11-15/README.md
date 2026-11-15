# Letters of 2026-11-15: drafts for the authors

Drafts only; nothing has been sent; whether and when a letter is sent is the authors' decision.

The drafts are text files. No mailbox draft was created and no mail tool was used (rule of the principal investigator, LOG PI-1115b).
The drafts hold no result, no caption text, no e-mail address and no personal name of an author of ours; slots such as `[corresponding author]` and `[recipient ...]` are filled by the sender.
Why they exist: answers T2, X4, A1, B3 and B5 in `manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_7e8f958d.md`, and answers F1 and F2 in `manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_4b4ec736.md` (both copies hold personal data and are not committed).

## 1. Who would send what, and the days named in the answers

Sender (answer F1): the corresponding author, from their own mailbox, with copies to the other two authors. The dataset letter does not go out before the Paper B rating is closed.

| File | To | Days named in the answers | Reply needed by | State of the draft |
|---|---|---|---|---|
| `L1_TAIMMA_CCIS.md` | TAIMMA 2027 general chairs; Springer contact for the CCIS series | latest 2026-11-18 (answer T2) | 2026-12-01 (stop rule of answer T2) | complete |
| `L2_KTVIC.md` | authors of the KTVIC dataset | not before the Paper B rating is closed (18:00 Vietnam time, 2026-11-15) and Part B is written (answers B3, X4, F1) | 2026-12-01, the text lock of the conference version (answer X4, rule 2); the letter asks for 2026-11-30 | NOT complete: Part B is a marker |
| `L3_UIT_OPENVIIC.md` | authors of UIT-OpenViIC | answer X4 puts the three data letters after the Paper B rating is closed; nothing in this letter touches Paper B | same as L2 | complete |
| `L4_THESIS_CODE.md` | author of the thesis code base of the KTVIC baselines | as L3 (answer X4, letter 3) | before the submission of Paper B; date not fixed in any file read | complete, two slots open |
| `L2_L4_MERGED.md` | one person who answers for both the KTVIC dataset and the thesis code base | as L2 | as L2 for Part 1, as L4 for Part 2 | NOT complete: Part B is a marker |

**L2 and L4, or the merged letter: the sender chooses.** Answer F1 suggests one letter with numbered parts if the dataset letter and the code letter go to the same person. `L2_L4_MERGED.md` is that letter; `L2_KTVIC.md` and `L4_THESIS_CODE.md` stay as the two-letter way. Only one of the two ways is used. The coordinator checked that both public repositories exist under the same account. Whether the same person answers for both, and may speak for the other authors of the dataset, is `[TO CONFIRM]` by the sender. If the two-letter way is chosen, L4 does not depend on Part B.

Word counts of the letter text (between the `LETTER START` and `LETTER END` marks, slots included): L1 329, L2 348, L3 332, L4 307, merged 588. The limit for a single letter is 350. L2 will pass it when Part B is added; the noun-table sentence in point 1 is the first candidate to cut or to move to an attachment. The merged letter holds the content of two letters and is over the limit as it stands.

## 2. Which sentences of which paper depend on each reply

Paths: Paper A = `/mnt/d/vsps_papers/vsps-paperA-spic` (commit `dafba17`), Paper B = `/mnt/d/vsps_papers/vsps-paperB-lre` (commit `edf7fee`), Paper C = `/mnt/d/vsps_papers/vsps-paperC-tallip` (commit `9b8e6ae`), conference version = `manuscript/conf_taimma_2027` in this repo.

**L1 (conference and series).** No printed sentence depends on it. The decision to submit the conference version does (answer T2: go on with the full paper for the third call; without a clear answer by 2026-12-01, stop and send the full paper to the journal instead). The reply on the licence also fixes what the later journal version of Paper C must do: cite the conference paper, state what is new, and carry enough new material.

**L2, or Part 1 of the merged letter (KTVIC authors).**

- Paper A `paper/declarations.md:19`: "one of us contacted the UIT-OpenViIC and KTVIC authors, who agreed to this use". The first half of that sentence ("used only through aggregates and pointers") is rewritten in any case, because Section 6.2 trains two adapters on the KTVIC training split (answer A1). By answer F2 the rewritten sentence states what was done and that the public repository carries no data licence file; it names no terms.
- Paper B `paper/cover_letter_B.md:27`: "One of us contacted the authors of KTVIC and UIT-OpenViIC, who agreed to the use of their datasets."
- Paper C `paper_v1_analysis/10_conclusion.md:25`: "One of us contacted the authors of UIT-OpenViIC and KTVIC, who agreed to the use of their datasets in this study." The same sentence is in `paper_v1_analysis/tex/body.tex:3310` and `tex/paperC.tex:3366`.
- Conference version `draft_v1/paper.md:262`: the slot "[PI: confirm or drop a sentence on the agreement of the KTVIC and UIT-OpenViIC authors to this use.]" (`draft_v2` was not read: another agent was revising it.)
- Part B of the letter will carry its own dependency (answer B3). It is not described here.

**L3 (UIT-OpenViIC authors).**

- Paper A `paper/declarations.md:19` (same sentence as above); `paper/sec11_limitations_ethics.md:44`; `paper/supplementary_SPIC.md:540` and `:1156`; `paper/supplementary.md:658` and `:1350`: "One of us contacted the UIT-OpenViIC authors, who agreed to this use" (or "its authors").
- Paper B `paper/cover_letter_B.md:27`; Paper C `paper_v1_analysis/10_conclusion.md:25` and the two `tex` lines; conference version `draft_v1/paper.md:262`: the same lines as under L2.
- If the authors do not agree to scores per image, Paper C keeps its present wording (`paper_v1_analysis/09_limitations.md:28`: per-image ledgers are not released).

**L4, or Part 2 of the merged letter (thesis code base).**

- Paper B `paper/sec3_data_and_audit.md:36`: "used with the permission of the repository's author (personal communication, 2026-10-21)" and, on the same line, the phrase "no published system is rescored". The run-repo copy is `manuscript/journal_draft_B/sec3_data_and_audit.md:38`.
- Answer B5 (i): with the written confirmation on file before Paper B is submitted, the aggregate scores under matched scoring are printed and the phrase "no published system is rescored" is changed to fit. Without it, they are not printed and no personal communication is cited.

## 3. Rule when no reply comes (answer X4, rule 2)

- A sentence that says dataset authors (or the code author) agreed is printed only when the written reply is on file in the project records. Memory of a talk or of a message that is not on file does not count.
- On the day the text of a paper is locked (first: the conference version, 2026-12-01, for submission on 2026-12-03), if the reply of a group is not on file, the agreement sentence for that group is removed from that paper. The paper then states only what was done with the data and that no image or caption is redistributed.
- The sentence may come back in a later submission once the reply is on file.
- Nothing is printed as "agreed" without the reply on file. This holds for Papers A, B, C and the conference version.
- The same holds if a letter is never sent: no reply on file, no agreement sentence.
- UIT-ViIC gets no letter (answer X4): the papers keep the present wording, which claims no permission.

## 4. Open points

For the authors (sender):

1. **Whether and when each letter is sent.** The days in the table above are those named in the answers; they bind nobody to send.
2. **Two letters or the merged letter** for the KTVIC dataset and the thesis code base, after confirming whether the same person answers for both (`L2_L4_MERGED.md`, item M-a).

For the principal investigator:

3. **Stop rule of 2026-12-01** (answer T2). The coordinator's table marks it as waiting for the principal investigator. L1 asks for a reply by that date.
4. **Earlier contact with the dataset authors.** Paper A prints that one of us contacted the KTVIC and UIT-OpenViIC authors and that they agreed; a comment on `paper/declarations.md:19` says written acceptance was obtained on 2026-10-28. Answer X4 finds no such document in the project files. If a message exists, file a copy and fill the slot in L2, L3 and the merged letter; if not, delete the slot line.
5. **Date of the oral permission for the thesis code**: 2026-10-21 (Paper B text) or 2026-10-22 (question file). Slot in L4 and in the merged letter. Answer F1 adds that, if the permission already sits in a message thread, the confirmation may be asked in that thread.
6. **Answers B3 and B5** are marked in the coordinator's table as waiting for the principal investigator's confirmation. L4, Part 2 of the merged letter and Part B follow from them.
7. **Planned submission date of Paper B**, to fix the reply-by date in L4 and in Part 2 of the merged letter.

For the coordinator:

8. **Scores per image** (L2 point 3, L3 point 4, merged 1.3). The request follows answer X4 and row C5 of the table. Paper C's present text says per-image ledgers are not released. Drop the clause from the letters if the plan is dropped.
9. **Adapter weights** (L2 point 1, merged 1.1). No Paper A sentence says the weights are not released; answer A1 decides they are not. Slot in both files.
10. **Terms of use.** KTVIC: checked on 2026-11-15 by public reads (LOG lines OPS-1115d-author-followup and OPS-1115e-ktvic-readme): no licence file, a null licence field, no terms sentence in the README; nothing is known about terms stated elsewhere. The letters ask under which terms the data may be used for training and evaluation in research; they do not say that the data are free of terms. UIT-OpenViIC: Paper A and Paper B describe its terms differently (L3 notes, L3-c); not checked.
11. **Part B** of L2 and of the merged letter: `[PART B - to be written after the Paper B rating is closed]`.

Each letter file ends with a NOTES section that gives the source file and line of every statement about our own work, and its own list of `[TO CONFIRM]` items.
