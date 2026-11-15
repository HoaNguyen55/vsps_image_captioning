# L2 — authors of the KTVIC dataset

DRAFT, not sent, and NOT COMPLETE: Part B is still a marker. A text file only; whether and when it is sent is the authors' decision (LOG PI-1115b). By answers B3, X4 and F1 it does not go out before the Paper B rating is closed and Part B is written. Alternative: `L2_L4_MERGED.md` joins this letter with L4.
Recipient addresses: from the dataset paper or its public repository; none is stored in this file.

<!-- LETTER START -->
**Subject:** Request for written confirmation of our research use of the KTVIC dataset

Dear [recipient: authors of KTVIC],

We are a research group at [affiliation] working on Vietnamese image captioning. Thank you for the KTVIC dataset, which we use and cite (Pham et al., 2024). Before we submit our papers, we ask for your written confirmation that the uses below are acceptable to you. A short reply is enough.

[TO CONFIRM: earlier contact and its date, or delete this line.]

1. **Training** (a study of object-hallucination measurement). We trained two adapters of an open vision-language model on the 3,769 images of the released training file, as systems under test. [TO CONFIRM: the adapter weights are not released.] The matcher we plan to release holds a Vietnamese noun table; 25 entries were added by hand after we met the words on KTVIC images or references. It holds words, not captions.

2. **Captions in prompts** (a study of in-context captioning: a journal paper and a shorter conference version). Captions of training images are placed, as examples, in the prompt of an open vision-language model. They are read at run time from the released file and are not redistributed. A 300-image part of the training file is a development set; part of the test file was read again in exploratory diagnostics.

3. **Release.** We plan to release code, image identifiers, file hashes and numeric scores, including, if you agree, scores per image by image identifier. We release no image, no caption of the dataset and no model caption.

[PART B - to be written after the Paper B rating is closed]

The public repository has no licence file, and its README states no terms. Under which terms may the data be used for training and evaluation in research, and how would you like the dataset acknowledged?

If any use needs a different form, please tell us. Our first submission deadline is in early December; a reply by 30 November 2026 would help us greatly.

With thanks and kind regards,
[corresponding author], on behalf of the authors
[affiliation]
Copy: [principal investigator], [co-author]
<!-- LETTER END -->

## NOTES (not part of the letter)

Repos read: Paper A `/mnt/d/vsps_papers/vsps-paperA-spic` at commit `dafba17`; Paper C `/mnt/d/vsps_papers/vsps-paperC-tallip` at commit `9b8e6ae` (its `tex/` files have uncommitted changes; the `.md` sections cited below are as committed). The licence fact rests on the coordinator's public reads of 2026-11-15 (LOG lines in the table), not on a paper text.

| Statement in the letter | Source (file:line) |
|---|---|
| Two adapters trained on the 3,769 images of the KTVIC training split; they are among the six systems scored in Section 6.2 | Paper A `paper/sec7_verbosity_sign.md:45`; same wording in `paper/supplementary_SPIC.md:574` |
| The dataset is cited as Pham et al., 2024 | Paper A `paper/sec1_introduction.md:17` |
| Matchers are part of the planned deposit | Paper A `paper/declarations.md:19` |
| Noun table: 29 hand-added entries, 25 of them met on KTVIC images or references | Paper A `docs/ZENODO.md:12-14`; `docs/PORTING.md:15` (12 compounds "met on real KTVIC images" and 13 nouns met on KTVIC references; the other 4 come from a boat-image caption whose dataset the line does not name) |
| Memory holds KTVIC training images outside the 300-image development carve (3,469 before the filter) | Paper C `paper_v1_analysis/03_method.md:7`; `04_data_and_splits.md:9` |
| Captions read at run time, placed only in prompts, never redistributed | Paper C `03_method.md:9`; `04_data_and_splits.md:3` |
| 300-image carve of the training file as development set (299 after the filter) | Paper C `04_data_and_splits.md:10`; `03_method.md:55` |
| Part of the KTVIC test set read again in exploratory diagnostics | Paper C `07_disclosures.md:22` |
| Release of scores, image ids and hashes; no captions ("scores per image by image identifier" is a request, see L2-c) | Paper C `09_limitations.md:28`; `10_conclusion.md:25`; Paper A `paper/declarations.md:19` |
| The public repository has no licence file and its README states no terms | `.session_backup/2026-10-13/decisions/LOG.md:2634-2635` (lines OPS-1115d-author-followup and OPS-1115e-ktvic-readme: public reads on 2026-11-15; no licence file, licence field null, no terms sentence in the README); answer F2 in `manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_4b4ec736.md` |
| Conference version exists and uses the same data | answer T2 (context); `manuscript/conf_taimma_2027/draft_v1/paper.md:262` |

Not put in the letter, but true of the work and available if the recipients ask: KTVIC test and development images are used as protected sets when near-duplicates are filtered out of the example pool (Paper C `03_method.md:9`). The letter makes no statement about overlap between datasets.

`[TO CONFIRM]` items:

- L2-a. **Earlier contact.** Paper A `paper/declarations.md:19` prints "one of us contacted the UIT-OpenViIC and KTVIC authors, who agreed to this use", and a comment on that line says that written acceptance was obtained on 2026-10-28. Answer X4 says no written confirmation is in the project files. Only the principal investigator can say whether a message exists. If it does: put its date in the slot and file a copy. If not: delete the slot line.
- L2-b. **Adapter weights.** The Paper A repo lists what will be deposited (`paper/declarations.md:19`) and the list has no model weights, but no sentence says "the weights are not released". Answer A1 decides that they are not. Confirm, then replace the slot by "The adapter weights are not released."
- L2-c. **Scores per image.** Paper C now says that per-image ledgers will not be released (`09_limitations.md:28`, `10_conclusion.md:25`). The request for per-image scores follows answer X4 (item 1) and row C5 of the coordinator's table ("after the terms are checked"). If that plan is dropped, delete the words "including, if you agree, scores per image listed by image identifier".
- L2-d. **Terms of use: checked, no longer open.** The coordinator's public reads of 2026-11-15 (LOG lines above) found no licence file, a null licence field and no terms sentence in the README. The same LOG line says that nothing is known about terms stated elsewhere. The letter therefore asks under which terms the data may be used; it does not say, and must not be edited to say, that the data are free of terms.
- L2-e. **Reply-by date** "30 November 2026" is a proposal. It sits one day before the text lock of the conference version (1 December 2026, answer X4 rule 2).
- L2-f. **Part B.** `[PART B - to be written after the Paper B rating is closed]`
- L2-g. Paper B's own uses of KTVIC are not listed in this draft. Add them with Part B.

Slots to fill before sending: `[recipient: authors of KTVIC]`, `[affiliation]` (twice), `[corresponding author]`, `[principal investigator]`, `[co-author]`.
