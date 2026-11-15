# L2 v2 — authors of the KTVIC dataset

DRAFT, not sent, and NOT COMPLETE: Part B is still a marker. This is a text file only; whether and when it is sent is the authors' decision (LOG PI-1115b). By answers B3, X4 and F1, it does not go out before the Paper B rating is closed and Part B is written. v1 (`L2_KTVIC.md`) is kept unchanged beside this file.
Recipient addresses come from the dataset paper or its public repository; none is stored in this file.

Why v2: Paper A now prints "one of us contacted the KTVIC authors, who agreed to this use" beside the training sentence (`paper/declarations.md:19`, `paper/sec11_limitations_ethics.md:48`). Goal §3 says the data groups' agreement is stated as a fact and is not asked again. v1 asked for written confirmation and asked under which terms the data may be used; both are removed here.

<!-- LETTER START -->
**Subject:** Our use of the KTVIC dataset: thank you, and what our papers say

Dear [recipient: authors of KTVIC],

We are a research group at [affiliation] working on Vietnamese image captioning. Thank you for the KTVIC dataset (Pham et al., 2024), and thank you for agreeing to our use of it when one of us contacted you. That use includes training. Before we submit our papers, we would like to tell you exactly how they use the dataset and what we will release, so that what we print matches what you agreed to.

1. **Training** (a study of object-hallucination measurement). We trained two adapters of an open vision-language model on the training split (its 3,769 images, with the captions of that split as training targets), and scored them as systems under test. The adapter weights are not released. The matcher we plan to release holds a Vietnamese noun table; 25 of its entries were added by hand after we met those words on KTVIC images or references. The table holds words, not captions.

2. **Captions in prompts** (a study of in-context captioning: a journal paper and a shorter conference version). Captions of training images are placed in the prompt of an open vision-language model as examples. They are read at run time from the released file and are not redistributed. A 300-image part of the training file serves as a development set; part of the test file was read again in exploratory diagnostics.

3. **Release.** We plan to release code, image identifiers, file hashes and numeric scores, including, if you agree, scores per image listed by image identifier. We release no image, no caption of the dataset and no model caption.

[PART B - to be written after the Paper B rating is closed]

If you would like the dataset acknowledged in a particular way, or would like any particular terms followed, please tell us and we will follow them. If you would prefer any use above to be described differently, a reply by 30 November 2026 would let us change the text before our first submission in early December.

With thanks and kind regards,
[corresponding author], on behalf of the authors
[affiliation]
Copy: [principal investigator], [co-author]
<!-- LETTER END -->

## NOTES (not part of the letter)

Repos read for v2:
- Paper A: `/mnt/d/vsps_papers/vsps-paperA-spic` at `0b542cf` (re-verified on 2026-11-15).
- Paper C: rows carried over from v1 unchanged. v1 read the C repo at `9b8e6ae`; the C repo is now at `55315ca`, and its rows were not re-read for v2.

| Statement in the letter | Source (file:line) | Status in v2 |
|---|---|---|
| Earlier contact; the authors agreed to the use | Paper A `paper/declarations.md:19`; `paper/sec11_limitations_ethics.md:48` ("One of us contacted the KTVIC authors, who agreed to this use.") | re-verified at 0b542cf |
| The agreed use includes training | Comment at Paper A `paper/declarations.md:19` (PI-1115i item 8: the acceptance the PI received covers the training) | re-verified at 0b542cf |
| Two adapters trained on the 3,769 training images, captions as targets | Paper A `paper/declarations.md:19`; `paper/sec11_limitations_ethics.md:48`; `paper/sec7_verbosity_sign.md:45` | re-verified at 0b542cf |
| Adapter weights are not released | Paper A `paper/declarations.md:19` and `paper/sec11_limitations_ethics.md:48` ("no trained adapter weight is part of the release") | re-verified at 0b542cf (closes v1 item L2-b) |
| Dataset cited as Pham et al., 2024 | Paper A `paper/sec1_introduction.md:17` | re-verified at 0b542cf |
| Noun table: 25 hand-added entries met on KTVIC images or references | Paper A `docs/ZENODO.md:12-14` | re-verified at 0b542cf |
| Matchers are part of the planned deposit | Paper A `paper/declarations.md:19` | re-verified at 0b542cf |
| Captions read at run time, placed only in prompts, never redistributed; 300-image development carve; test file read again in diagnostics; release of scores, ids and hashes | Paper C `03_method.md:9`, `04_data_and_splits.md:3`, `:10`, `07_disclosures.md:22`, `09_limitations.md:28`, `10_conclusion.md:25` | carried over from v1, not re-read |
| A conference version exists and uses the same data | answer T2; `manuscript/conf_taimma_2027/draft_v1/paper.md:262` | carried over from v1 |

Changes from v1:
- **L2-a (earlier contact), closed.** The slot is replaced by the paper's own clause. No date is given and the letter does not say "in writing" or "on file", because no document is filed in the repo. This follows the wording rule applied to PASCAL-50S (commit `b9d3deb`).
- **L2-b (adapter weights), closed** by the printed sentence in Paper A.
- **L2-d (terms).**
  - The question "Under which terms may the data be used" is removed, because it asked again for an agreement that the paper states as a fact (goal §3).
  - It is replaced by an offer to follow any acknowledgement or terms the authors name.
  - The letter still does not say, and must not be edited to say, that the data are free of terms. The public repository has no licence file and its README states no terms (LOG OPS-1115d-author-followup, OPS-1115e-ktvic-readme).
- **Subject and opening.** The subject is no longer a request for written confirmation. The letter now informs and thanks.

Still open:
- **L2-c. Scores per image.** Paper C says per-image ledgers will not be released (`09_limitations.md:28`, `10_conclusion.md:25`, as read for v1). If that plan stands, delete "including, if you agree, scores per image listed by image identifier".
- **L2-e. Reply-by date.** "30 November 2026" is a proposal. It falls one day before the text lock of the conference version (1 December 2026, answer X4 rule 2).
- **L2-f. Part B** is still to be written.
- **L2-g.** Paper B's own uses of KTVIC are not listed yet; add them with Part B.
- `L2_L4_MERGED.md` still carries the v1 wording (the request for written confirmation and the terms question) and needs the same change. It was not edited.

Slots to fill before sending: `[recipient: authors of KTVIC]`, `[affiliation]` (twice), `[corresponding author]`, `[principal investigator]`, `[co-author]`.
