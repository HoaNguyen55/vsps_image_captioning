# Scorer brief (same text for every scorer; only {SCORER_ID} and {ORDER} differ)

You are scorer {SCORER_ID}. You score six cards, X1 to X6, in `/mnt/d/vsps_image_captioning/manuscript/conf_taimma_2027/calibration_ccis/blind/`. Read them in this order: {ORDER}. Each file holds a PAPER CARD and a DIRECTION CARD (JSON) that summarise one full paper written for an international conference in applied AI or language processing.

## Hard rules

- Read ONLY the six files `blind/X1.md` … `blind/X6.md`, this brief, and the rubric file `/mnt/d/vsps_image_captioning/manuscript/directions/calibration_2026-11-13_A_phaseB/RUBRIC_T1-T8_AND_ANCHORS.md` (sha256 572c29883b9381adfe1d411d82f0bd4e4b1a201e00f22ae29fed362639a20491).
- Do not open any other file in `calibration_ccis/` or elsewhere in the repository. In particular do not open `REFERENCE_SET_NOTES.md`, `KEY_DO_NOT_SHOW_SCORERS.md`, `SHUFFLE_KEY_DO_NOT_SHOW_SCORERS.md`, the folder `cards/`, any file whose name starts with `CARD_`, `G3_PASS_RULE.md`, or another scorer's output.
- No web search, no literature API, no other source.
- Do not try to identify the papers, their authors or which card is whose, and write no guess about it anywhere.
- No commits. Write only your one output file.

## What to score

- Score every card on T1 to T8, each an integer from 0 to 5. Use the criterion texts in section 1 of the rubric file and the anchors in its section 2 (5 exceeds expectations, a standout strength for an A* or top-Q1 committee; 4 meets the Q1 standard, no serious objection; 3 meets the Q2 standard, fixable objections; 2 minor improvement or clear shortcomings, major revision; 0–1 missing or wrong).
- Judge only on what the card says is present or absent. What a card does not mention is not credited.
- Ignore the group's internal rules about new labels or test looks: other groups are not bound by them.
- T8: every card names the same venue class, "international conference"; score T8 from that and from the impact the card designs in (release, reusable tool or measure).
- Score each card independently and with the same severity; do not rank-normalise across the six cards.

## Output

Write a tab-separated file to `/mnt/d/vsps_image_captioning/manuscript/conf_taimma_2027/calibration_ccis/scores/{SCORER_ID}.tsv`, UTF-8, no quoting:

- Header line, exactly: `scorer_id	card_id	criterion	score	reason`
- Then exactly 48 data rows, one per card and criterion, ordered X1 to X6 and, within a card, T1 to T8.
- `scorer_id` = {SCORER_ID}; `card_id` = X1 … X6; `criterion` = T1 … T8; `score` = one integer 0–5.
- `reason`: one line of at most 30 words naming what on the card drives the score; no tab, no line break.

Final reply: only the path and the line "48 rows written".

## Values filled in by the coordinator

| scorer | {ORDER} |
|---|---|
| S1 | X1, X2, X3, X4, X5, X6 |
| S2 | X6, X5, X4, X3, X2, X1 |
| S3 | X4, X5, X6, X1, X2, X3 |

The coordinator sends each scorer this brief with its row filled in and the table removed.
