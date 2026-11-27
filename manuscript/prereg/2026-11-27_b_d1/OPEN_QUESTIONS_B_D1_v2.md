# Open questions B-D1/A3 v2 (draft; v1 2026-11-27T09:22Z; v2 after CC-505)

Each question has a recommendation and a default. All are reversible and technical, so the coordinator decides them on judge advice. No question needs the PI. The path after a non-SUPPORTED H3 goes to the PI through `PIVOT_REVIEW_B_vi.md` (prereg v2 §9).

| # | question | recommendation | default if no answer |
|---|---|---|---|
| 1 | First-look pool (22 comparisons). | Closed by CC-505 B5: not used in D1 or A3. | not used |
| 2 | H3 axis design. | Closed by CC-505 B3, option (ii): unit, punctuation and case go inside the scorer-and-tokenizer grid; the label measures tone placement alone; the `syl`-only grid (the v1 estimand) is a DESCRIPTIVE row. | as in v2 §5 H3 |
| 3 | H1/H2 criterion: pool the folds {`syl`, `pyvi`, `uts`}, or `uts` only? | Pool. With `uts` alone, the FE-CERT cell is printed (1/909) and the discordant count is at most 27 per side. | pooled |
| 4 | Floors and bands. H1/H2: n ≥ 10. H3: the FE-CERT v1.1 constants R_MAX = 0.05 and N_MIN = 59. A3: upper bound ≤ 0.040 per direction at 97.5%. | Keep. The H3 constants predate every FE-CERT number. The A3 margin is the v1 margin of 1.5 points, taken per direction. | as drafted |
| 5 | AER σ_c: hold it fixed across resamples, or re-standardize within each resample? | Fixed, as this registration's own convention. Lu et al. do not state which they do. Fixing it keeps the ensemble linear in the per-image differences. | fixed |
| 6 | AER weights: per member or per token-identity class? | Per member, with per class as a DESCRIPTIVE row. | per member |
| 7 | A3 nulls: draw with or without replacement? | Without replacement (1,000 of 1,101). | without replacement |
| 8 | A3 family for r_A3: F_dev, with F as a DESCRIPTIVE row? | Yes. The rule sits on r_f0 in any case. | F_dev |
| 9 | Judge for round 2. | One-judge FULL read with `V1_TO_V2.diff`, as CC-505 ruling 10 sets. If design items stay open, round 3 is a panel. | as ruled |
| 10 | Host. | Closed by CC-505 ruling 9: a rented host only, after the C-CONF floor is paid; hard stop at 8 CPU-h. | rented host |
| 11 | Order against K0. | K0 first. The D1 text goes in only after the result read: a new subsection of §6, plus one abstract sentence per label from prereg v2 §8. | K0 first |
| 12 | H1/H2 on BLEU-4 or ROUGE-L as well? | No. CIDEr-D is the only metric with a verdict in FE-CERT. BLEU-4 and ROUGE-L enter only as scorers of the H3 grids. | no |
