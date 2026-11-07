# A-M1 companion edits for the per-paper repo (plan §10.1; CC-288 N6)

These edits are applied at transfer, in /mnt/d/vsps_papers/vsps-paperA-spic (PI-1101m), not in this repo. Line numbers are at d0cb698.

The PI rewrites wording later; the limits of plan §10.2 and CC-288 stay.

Nothing here is applied yet. Per CC-289 Ruling 8 these edits are applied only after a round-2 GO and the gatekeeper commit of the s1m files, then checked by a one-judge diff read before any paper-repo commit.

| # | File (paper/) | Where | Edit |
|---|---|---|---|
| 1 | sec5_exchangeability.md | after §5.3 (ends l.39) | Insert the new §5.4 heading and the one sentence from MAIN_SENTENCE.md. Arm U, COCO-5000 only; no UIT-ViIC number; the FAIL is not named in the main text (CC-288 N4, PI default NO). |
| 2 | sec5_exchangeability.md | l.39, the "Consequences for reporting" sentence on single-writer data | Keep it as it is for single-writer corpora. Append: "for COCO-5000 and UIT-ViIC (development data) see Section 5.4". |
| 3 | supplementary.md | l.535, item 3 (reference-sampling estimators on single-writer data; "we report none") | Keep the item for single-writer corpora. Append: "for COCO-5000 and UIT-ViIC (development data) see Supplementary S1.M and S5". The withdrawn-values comment on that line stays, and no withdrawn value is revived. N7 (CC-289): the plan §10.1 wording "see Section 5.4" is equally acceptable; the PI rewrites. |
| 4 | supplementary_SPIC.md | l.425, item 3 (same sentence) | The same append as row 3. |
| 5 | supplementary.md and supplementary_SPIC.md | Supplementary S1 | Add subsection S1.M from S1M_DRAFT.md (paper-text block only; Remark 4 stays out until the S1.M read verifies it, per J7). |
| 6 | supplementary.md and supplementary_SPIC.md | Supplementary S5 | Add Table S5.M and its notes from S5_TABLE.md. |
| 7 | sec11_limitations_ethics.md | §9.1 Threats to validity | One line: the reference-only bound assumes exchangeable, independent writers (A1). On UIT-ViIC, written by a panel of five writers, (A1) is a modelling assumption and is not checked, so the bound may fail if writers name different objects. |
| 8 | sec2_related_work.md and paperA.bib | the related-work paragraph on incomplete gold | Cite, each record verified CC-289: Chao 1987 (Biometrics 43, 10.2307/2531532; not in paperA.bib; record only, closed access, its content via Chao and Colwell 2017; credited with the inequality only, never with the (k−1)/k factor); Chao and Colwell 2017 (SORT 41(1), 3–54, 10.2436/20.8080.02.49; not in paperA.bib; cited in S1.M for §2.2 and Eq. 2a–2b); Colwell et al. 2012 (colwell2012models); Chao et al. 2014 (chao2014rarefaction; Table 2 only, no range guidance); Trushkowsky et al. 2013 (in paperA.bib); Luggen, Difallah, Sarasua, Demartini and Cudré-Mauroux 2019 (LNCS, ISWC 2019, pp. 453–469, 10.1007/978-3-030-30793-6_26; not in paperA.bib). The sec2 sentence is not drafted yet (CC-289 N6): it states only verified content (Trushkowsky [W3], read in the preprint; Luggen [A]; Colwell 2012 and Chao 2014 for rarefaction and extrapolation), makes no priority claim, and is checked at the transfer diff read. |
| 9 | supplementary_SPIC.md l.595 and its twin supplementary.md l.745 | the X1/X2 extrapolation paragraph | Add one distinction sentence: X1 extrapolates each run's mention precision, whereas S1.M bounds the coverage of the reference gold itself, independent of any system. No X1 number is reused. |
| 10 | whole main text | — | Recount words against the 8,500-word cap (PI-1105k) after rows 1, 2 and 7. |
| 11 | sec5_exchangeability.md | l.29, "The two independent-annotator caption sets with a documented protocol, COCO and UIT-ViIC" | For the A writer and the PI, at the next A diff (plan N7): the UIT-ViIC protocol (five writers, a tool that shows the others' captions) does not support "independent" as written. |

Checks at transfer:
- every number traces to data/results/a_m1/a_m1_result.json (5687a66b) by its key path;
- direction words: Ĉ is an upper bound on coverage, and Ŝ and m̂ are lower bounds;
- none of the banned words of plan §10.2 l.556 and the CC-288 MAY NOT list;
- the PI-1101e and PI-1101o wording rules, and no statement that the sets share images;
- NGRAM on every touched file.
