# Paper B draft status (2026-10-20, B-writer; supersedes the 2026-10-19 version)

Framing (PD-24, 2026-10-20): audit-and-kit resource paper for LRE. Main text = dataset-validity audit + protocol card + evaluation kit (sec1–sec8, 8,115 words without comments; abstract 249 words at the top of outline_B.md). The ladder, second backbone/3B, B-N1, B-N2 detail and all former Section 6 moved to `supplementary_B.md` with verdicts unchanged; sec1 lists them in one line. Files renamed: sec7_discussion → sec6_discussion, sec8_limitations_ethics → sec7_limitations_ethics; new sec8_conclusion; sec6_negatives removed (content in the supplement). No method claim (DEBATE D2). Complete draft due 2026-12-10. Change log: `WRITER_B_LOG.md`.

## Sections

| File | Status |
|---|---|
| outline_B.md | updated 10-19 (ladder per W8 Amendment 1; kNN outcome; PENDING list; kit rows) |
| sec1_intro.md | ladder bullet fixed (no "equivalent within ±1.0"); negatives bullet relabelled. A kit bullet was NOT added (edit rejected at the 10-18 pause) |
| sec2_related.md | CC-024 exposure labels (UIT-ViIC test = COCO train2017; XM3600 = Open Images); [VERIFY] tags remain |
| sec3_data_and_audit.md | XM3600 period shift (+2.71 / +2.75, absolute only); c8 UIT-ViIC values withdrawn (B2); §3.7 release kit (Table 3.1); CC-024; B-N2 placeholder |
| sec4_system.md | §4.3 addendum margins and timing (first registered output = fuse2_s44, 10-12 12:27Z); §4.5 G1 exact diffs, WiSE-FT has run, M3/S3 scale disclosure; new §4.6 deviations table (Table 4.1, PD-11 sentence verbatim) |
| sec5_results.md | ladder per W8 Amendment 1 (registered H0 NOT met: pooled part met, per-run part not, PD-20; ±0.8 TOST POST_HOC and FAILS; 6/10 runs all-in); EV-RANK POST_HOC; B-N1 placeholder; UIT-ViIC transfer caveat (CC-024) |
| sec6_negatives.md | registration labels per D-W13-6 / A4.4 (verbatim); kNN LOCALLY_FROZEN, rule outcome SECONDARY_POSITIVE_OR_INCONCLUSIVE; UPE kill 2 on panel P; RL rule; P-M6b per PD-10 (b); PLAN-F1 NOT_RUN; new §6.6 WiSE-FT (Table 6.2, PD-14 sentence verbatim, addendum items [PENDING-WISE-ADDENDUM]) |
| sec7_discussion.md | ladder wording softened; new §7.4 (kit mapped to the recommendations) |
| sec8_limitations_ethics.md | ladder, WiSE-FT, XM3600, exploratory list, AI-provenance item 3 relabelled; ViCLIP-OT corrected (UIT-OpenViIC, not KTVIC) |
| number_manifest_B.tsv | 422 rows: 388 keyed, 7 derived, 5 literature, 5 REMOVED, 11 PENDING, 4 PENDING-WISE-ADDENDUM, 1 RESULT (WiSE-FT), 1 DROPPED (v3 sign-off); built by scratchpad `update_manifest.py`, values read by key and display-checked |
| new_vs_FAIR.md | punctuation row updated; release-kit row added (estimate not recomputed) |

## Gemini `_v2` prose errors (STATUS 2026-10-15 list)

1–4 are not present in sec1–sec8. Their residual forms were fixed: sec1 ±1.0 equivalence, sec5 and sec7 "frontier shown", sec8 ±1.0 TOST. 5 was resolved earlier. 6: the draft uses the committed 28.98 and the JSON's 99.5.

## Open items (2026-10-20)

- Author placeholders: the MIT licence (kit); [AUTHOR TO PROVIDE] Zenodo DOI; [AUTHOR TO PROVIDE] terms under which KTVIC, UIT-ViIC and UIT-OpenViIC were obtained (PD-24 b user question); [AUTHOR TO CONFIRM] AI tools/versions and AI-drafted text (sec7.4); [AUTHOR TO PROVIDE] FAIR 2026 proceedings title, pages, DOI (paperB.bib).
- B-F1 ran once on 2026-10-21: registered verdict FAIL (D_MBR −0.391 [−2.437, +1.666]; data/results/b_f1/b_f1_run.json, CP-071).
- Not run: POPE-500 for UIT-ViIC adapters; UIT-ViIC append-period effect; slot-rate-preserving permutation null (R1-M2); 8-gram scan of the kit archive; WiSE-FT addendum items; protocol-matched comparators.
- Unverified, not reported: 3B 61/62 outputs (M2 logs); UIT-ViIC role/child flip CI.
- Kit components still live only in git-excluded session folders (v3 rules, c8 punctuation audit, XM3600 period audit, overlap lists, 8-gram scanner): move into a release directory and re-run before deposit.
- Tier-3 S1/S2/S3/S5 numbers in supplementary_B.md S7 have no manifest rows yet (pre-existing gap).
- Bib: all 39 citations resolved in paperB.bib (DOI/arXiv-checked 2026-10-20); VES-RFT dropped (no DOI/arXiv).
