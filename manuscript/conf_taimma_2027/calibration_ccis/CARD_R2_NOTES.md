# Notes on CARD_OURS_v3_1_R2.md (CC-424 W2)

Written 2026-11-15. Coordinator file; not for scorers.

## Inputs

| file | sha256 |
|---|---|
| draft_v3_1/paper.md (text the card is built from) | b42eecb1c8e574af98ade56902fae0676a440f6cfd579dd8690984be5ee6692d |
| CARD_OURS_v3_1_PROVISIONAL.md (left untouched) | fce6012b093d68637c8e934f6f2c05c1042d33bdfaa8a8582348ba381fe6bee1 |
| annexB_cc424.py (checker, equal to the sha in CC-424 W2) | c1505b5c97bda77387ca351f15343690cd9d02edccf1d76265665fad7776ba53 |
| cards/R1.md to R5.md | equal to the shas in CC-424 (30a3886a, f45dd90c, 76afc94c, 07b49e33, 38098e9c) |

## Output

| file | sha256 |
|---|---|
| CARD_OURS_v3_1_R2.md | 773c7f033c174092f2af78a8b908f9cb1ea7b35fc78c4bae009866348cbff14e |

Not opened: KEY_DO_NOT_SHOW_SCORERS.md and SHUFFLE_KEY_DO_NOT_SHOW_SCORERS.md. Not made: blind/ copies, LOG line, scorer runs.

## What changed against the provisional card, and why

All changes are to the three removable tells of CC-424 ruling 2. No sentence, number or reference was added. Every number on the new card also appears on the provisional card and in paper.md.

1. **T-b, code type.** All backticks outside the JSON fence are removed. Arm names are plain words: ret, rand, fix, zs. The banner no longer puts file names in code type. The backtick count is now 6, which is the JSON fence only.
2. **T-c, closest_work.** 7 entries became 6, inside the reference range of 5 to 6. Dropped: "Training-free multilingual remote-sensing captioning (Rebelo et al.)". Kept: "LMCap (Ramos et al.)". Reason: paper.md S2-04 names LMCap as training-free and as listing Vietnamese among its languages. It is the only one of the seven that bears directly on Vietnamese coverage, so dropping it would flatter the novelty picture. Rebelo et al. is a multilingual remote-sensing study for which the paper names no Vietnamese coverage. The other five entries stay: OpenFlamingo, MUNIChus, Yang et al., Li et al. and Baldassini et al.
3. **T-a, length.** The paper card went from 767 words to 623 (reference cards: 564, 619, 622, 626, 630). The cuts follow one order:
   - First, favourable or neutral numbers were dropped from "Key numbers". These are the pooled ret − zs on OpenViIC (+14.30), the Qwen2.5-VL per-arm triple (39.81, 31.48, 20.05) and Qwen2.5-VL's OpenViIC row (+8.33 [7.01, 9.76]). The InternVL3 rows, every FAIL row and the NoCaps "point below +2.0" are kept.
   - Then the wording was compressed field by field. Examples: "large language models (MLLMs)" became "LLMs"; "an equal number k of random captions" became "an equal number of random ones"; the arm parentheses were shortened and "seeded" was dropped; "with no recorded calibration" became "without recorded calibration"; "are named as not printed" became "are not printed".
   - All negative and limiting items are kept. They are the following:
     - "size not printed";
     - rand and fix at the configuration picked on the ret score;
     - +2.0 as a planning value without recorded calibration, carried unchanged to English;
     - one rand draw and one decode per image;
     - the deletion-step cost (33.62 against 39.50) and "improved neither object measure";
     - the near-copy flag (12 of 1,941);
     - the NoCaps domain rows and the development ablations not reported;
     - no figure, no caption examples or error categories;
     - the release and licence gaps;
     - "NoCaps rule chosen after XM3600";
     - all seven limitations.
   - The tells that CC-424 rules as not removable (T-d to T-g) are kept as they were: preregistration, PASS and FAIL labels, one look, the Vietnamese and English sets, "no new annotation", the CIs and the GPU-hours.
4. **Banner** (outside the scorer slice). It is rewritten without the word that check g looks for and without reference-card labels. It states that this card is not yet the card of record.

Word-level deletions (git diff --word-diff against the provisional card): the dropped numbers above, the backticks, the Rebelo entry, and compressed wording only. Every insertion is a shorter wording of text that was already on the card.

## Word counts (paper-card slice as the checker counts it)

| card | words |
|---|---|
| provisional | 767 |
| R2, first pass (backticks and closest_work only) | 747 |
| R2, final | 623 |
| reference range | 564 to 630 (mean 612) |

The margin to the upper bound is 7 words.

## Checker output (python3 -I annexB_cc424.py CARD_OURS_v3_1_R2.md ../draft_v3_1/paper.md, run from calibration_ccis/)

```
ok   a words 564-630 
ok   b backtick outside the json fence 
ok   c closest_work 5 or 6 
ok   d 14 headings as R2 
ok   e keys and fixed values 
ok   f number not in the paper text 
ok   g label token 
CARD OK 623 words
```

On the provisional card the same checker prints FAIL on a, b and c (767 words), as CC-424 states.

A further check covered all numbers, including those check f skips (small integers, signed values). It found 75 number tokens, 56 of them distinct. All occur in paper.md. The only two misses are regex artefacts of a trailing comma ("911,", and "3600," from "XM3600,"). None is new against the provisional card.

## What must be re-checked if paper.md changes (the text of record, page count, any cut k1-k3)

- Re-run annexB_cc424.py against the new text. Check f fails on any number the new text no longer prints. Check a must stay at or below 630; there are only 7 words of margin.
- Re-read the fields of CC-424 ruling 3 (i) against the new text rather than carrying them over:
  - "Positioning": still two sentences? still five analyses, 2023–2026? still no table?
  - closest_work: does LMCap and the other five stay cited?
  - "Failure analysis" and "Ablations": still no figure? are the NoCaps domain rows and development ablations still named as not printed? is the deletion-step cost still printed?
  - "Data and splits" sizes.
  - Every key number after the freeze re-join.
  - The release sentence. Placeholder D9: if a public archive replaces "on request", the release field changes.
  - The licence placeholder in the data statement. If licences are filled in, "No data-set licence stated" changes.
- If the four papers of the literature search enter the text (plan l.84), re-read "Positioning", the novelty gap ("as far as they state, none ...") and closest_work. The 6-entry cap holds: an added entry means another one is dropped, with the reason recorded.
- The banner's input sha (b42eecb1) and this file's output sha must be updated. The shuffle key's row X3 then names the rebuilt card's sha (coordinator, CC-424 ruling 3 (iii)).
