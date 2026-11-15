# L3 — authors of the UIT-OpenViIC dataset

DRAFT, not sent. A text file only; whether and when it is sent is the authors' decision (LOG PI-1115b). Answer X4 places the three data letters after the Paper B rating is closed.
Recipient addresses: from the dataset paper or its public page; none is stored in this file.

<!-- LETTER START -->
**Subject:** Request for written confirmation of our research use of the UIT-OpenViIC dataset

Dear [recipient: authors of UIT-OpenViIC],

We are a research group at [affiliation] working on Vietnamese image captioning. Thank you for the UIT-OpenViIC dataset, which we use and cite (Bui et al., 2026). Before we submit our papers, we ask for your written confirmation that the uses below are acceptable to you. A short reply is enough.

[TO CONFIRM: earlier contact and its date, or delete this line.]

1. **Aggregate statistics** (a study of object-hallucination measurement). We computed a diagnostic of reference order on your references: on a 555-image multi-reference panel and on the test split (2,001 images). Only aggregate statistics are reported. No caption, n-gram or per-image file of the dataset appears in the paper or its release.

2. **Captions in prompts** (a study of in-context captioning: a journal paper and a shorter conference version). Captions of training images are placed, as examples, in the prompt of an open vision-language model. They are read at run time from the released files and are not redistributed.

3. **Evaluation** (the same study). The development split, divided into two halves, serves for development. The test split serves for the registered test: model captions are scored against your released references.

4. **Release** (the captioning study). We plan to release code, image identifiers, file hashes and numeric scores, including, if you agree, scores per image listed by image identifier. We release no image, no caption of the dataset and no model caption.

The terms we could find mention research use, but not derived releases of this kind. Which terms should we follow, and how would you like the dataset acknowledged?

If any use needs a different form, please tell us and we will change it. Our first submission deadline is in early December; a reply by 30 November 2026 would help us greatly.

Thank you for making the dataset available.

Kind regards,
[corresponding author], on behalf of the authors
[affiliation]
Copy: [principal investigator], [co-author]
<!-- LETTER END -->

## NOTES (not part of the letter)

Repos read: Paper A `/mnt/d/vsps_papers/vsps-paperA-spic` at commit `dafba17`; Paper C `/mnt/d/vsps_papers/vsps-paperC-tallip` at commit `9b8e6ae` (its `tex/` files have uncommitted changes; the `.md` sections cited below are as committed); Paper B `/mnt/d/vsps_papers/vsps-paperB-lre` at commit `edf7fee` (licence-terms lines only).

| Statement in the letter | Source (file:line) |
|---|---|
| Reference-order diagnostic on a 555-image multi-reference panel and on the test split (2,001 images) | Paper A `paper/sec5_exchangeability.md:27`; `paper/supplementary_SPIC.md:445` |
| Only aggregates; no caption, n-gram or per-image panel in the paper or its release | Paper A `paper/sec11_limitations_ethics.md:44`; `paper/supplementary_SPIC.md:540`; `paper/sec2_related_work.md:18` |
| Cited as Bui et al., 2026 | Paper A `paper/sec2_related_work.md:18` |
| Captions of 9,088 training images are in the example pool before the filter | Paper C `paper_v1_analysis/03_method.md:7`; `04_data_and_splits.md:9` |
| Captions read at run time, placed only in prompts, never redistributed | Paper C `03_method.md:9`; `04_data_and_splits.md:3` |
| Development split (2,011 files) divided into two halves for the development stages | Paper C `04_data_and_splits.md:11-12` |
| Test split (2,001 files; primary set 1,941) for the registered test, scored against the released references | Paper C `04_data_and_splits.md:14-15` and `:24` |
| Release of scores, image ids and hashes; no captions | Paper C `09_limitations.md:28`; `10_conclusion.md:25`; Paper A `paper/declarations.md:19` |
| Terms found mention research use, not derived releases | Paper A `paper/supplementary_SPIC.md:540` ("record non-commercial research use but no explicit permission for derived per-image panels") |
| Conference version exists and uses the same data | answer T2 (context); `manuscript/conf_taimma_2027/draft_v1/paper.md:262` |

Not put in the letter, but true of the work and available if the recipients ask: half of the test set was read again in exploratory diagnostics (Paper C `07_disclosures.md:22`); development and test images are used as protected sets when near-duplicates are filtered out of the example pool (Paper C `03_method.md:9`); 60 test images are left out of the primary set by a filter fixed in advance and the full 2,001-image result is reported beside it (Paper C `04_data_and_splits.md:24`). The letter makes no statement about overlap between datasets.

`[TO CONFIRM]` items:

- L3-a. **Earlier contact.** Paper A prints that one of us contacted the UIT-OpenViIC authors, who agreed (`paper/declarations.md:19`, `paper/sec11_limitations_ethics.md:44`), and a comment on the first line says that written acceptance was obtained on 2026-10-28. Answer X4 says no written confirmation is in the project files. Only the principal investigator can say whether a message exists. If it does: put its date in the slot and file a copy. If not: delete the slot line.
- L3-b. **Scores per image.** Paper C now says that per-image ledgers will not be released (`09_limitations.md:28`, `10_conclusion.md:25`). The request follows answer X4 (item 1) and row C5 of the coordinator's table. If that plan is dropped, delete the words "including, if you agree, scores per image listed by image identifier". Note that Paper A's own text promises no per-image file of this dataset; the request concerns Paper C only.
- L3-c. **Terms of use.** The two paper repos describe the terms differently: Paper A says the terms found "record non-commercial research use" (`paper/supplementary_SPIC.md:540`); Paper B says the dataset "state[s] no licence" and asks "only for citation and research use" (`paper/sec3_data_and_audit.md:70`, `paper/sec7_limitations_ethics.md:28`). The letter uses the weaker common part ("mention research use"). Someone should read the dataset's public page once before sending.
- L3-d. **Reply-by date** "30 November 2026" is a proposal. It sits one day before the text lock of the conference version (1 December 2026, answer X4 rule 2).
- L3-e. Paper B's own uses of this dataset, if any, are not listed in this draft (Paper B text was not read for this purpose).

Slots to fill before sending: `[recipient: authors of UIT-OpenViIC]`, `[affiliation]` (twice), `[corresponding author]`, `[principal investigator]`, `[co-author]`.
