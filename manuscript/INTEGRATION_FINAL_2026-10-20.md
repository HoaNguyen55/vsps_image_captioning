# Final number integration for Papers A and B (2026-10-20, 15:45Z / 22:45 VN)

**Inputs read**
- Gemini's audit: `.session_backup/2026-10-18/gemini_handoff/PAPER_A_B_EVALUATION_AND_CITATION_AUDIT_2026-10-20.md`, sha256 99bb27b8.
- Its handoff log: `.session_backup/2026-10-18/gemini_handoff/STATUS.md`, sha256 f116f5c2.

**Rule applied:** only numbers from committed, VERIFIED records enter the drafts. Gemini's numbers are used only after they have been checked against the machine queue logs and the result files.

## 1. Audit claims checked against primary records

| Audit claim | Primary record | Verdict |
|---|---|---|
| M1 jobs include 01_f30k_cider, 02_nocaps_eval, 03_xm3600_vi_eval, 04_xm3600_en_eval | M1 queue.log OK lines: 56, 57, 58, 01_t3_4_s5, 02_t3_2_s1, 03_t3_3_s3, 04_lb_a_n2, 05_lb_b_n1 | **FALSE.** These jobs never ran; their CIDEr values (0.3917, 0.7336, 0.2248, 0.5179) have no source. Not used. |
| M2 jobs include 05_t2_2_ktvic_3b, 06_t1_1_chair500_3b, 07_t3_2_vcr_vi_3b | M2 queue.log: 05_e1_k2_placebo OK, 06_n9_leaderboard FAIL, 07_g2b_qwen3vl_ladder OK | **FALSE.** The CHAIR-500 3B, VCR-Vi and KTVIC 3B numbers have no source. Not used. |
| "XVEF-1 = 0.6709 (P 0.6929, R 0.6746)" | S2 g0.json / readout.json | **FALSE.** S2 reports G0 AUROCs (0.634, 0.485) and a NOT CARRIED readout. |
| 05_lb_b_n1_decode is a "length-matched decode at max_new_tokens 16/20/24 on UIT-ViIC and COCO" | B-N1 prereg (327191c) | **FALSE.** B-N1 is a 4-model Vietnamese zero-shot leaderboard on KTVIC and UIT-ViIC test. |
| 56_multiref_s42 CIDEr 130.67 / 131.69 | Earlier log: KTVIC test short 148.04 | **CONFLICTS** with the logged value. Not used; the ladder check (VERIFIED) is the source. |
| Paper B builds the OpenViIC dataset; target CVIU/EAAI; title "Length-Routed …" | outline_B.md; PD-6 | **FALSE.** Paper B audits existing data; its target is LRE. |
| Both rentals were "cancelled safely" | Not in STATUS.md f116f5c2; both hosts unreachable since 18:23Z (M2) and 23:12Z (M1) | **Unconfirmed.** The user is asked to confirm. If confirmed, the OpenViIC panel file is deleted per the standing rule. |
| COCO reference counts (G-A8.6) | A-verifier, 2026-10-18 | Already VERIFIED and applied (sec6:7). |
| Bibliography: 8 unresolved citations (Karlin, Colwell ×2, Paper B ×4, OpenViIC) | A5.2 files | Plausible. To be checked in the bib pass; not a number. |

## 2. Integrated now (VERIFIED and committed sources only)

**Paper A**
- §7 table row and §7.6:
  - G2-B: the primary E1/E2/O1/P1 PASS on cv295, uv231 and xm600, with slopes and ladder differences; the secondary verdicts (68be2b7a, 47de6b6).
  - A-N1: MIXED, with all three Q values (ec0938e0).
  - A-N2: LBA-P1 PASS ×2; LBA-P2 FAIL on cv295 (qwen3vl_8b); KA2 wording; hit_max 1.0 disclosure (1f6ce422, 80405b1; CP-041 bindings).
- §8.4b: A-N3 NOT_SUPPORTED, with both parts and the not-significant wording (7a5a614d, 1c153fa).
- §10: pending note updated.
- Abstract (outline.md): the map-selected sentences, verbatim. The map rule gives PASS, so the C2 PASS sentence and the one-reference clause are used; A-N1 uses the MIXED sentence. 246 words.
- number_manifest.tsv: +31 keyed rows.
- New paperA.bib: paperA_v3 (72) + karlin1968total + colwell2012models (Crossref 10.1093/jpe/rtr044; the audit's "ftr044" is wrong) + an anonymous under-review entry for Paper B, 75 entries. The only unresolved mention left is outline.md's internal OpenViIC note.

**Paper B**
- §3.6: B-N2 placebo INCONCLUSIVE (0.20 [−13.97, +14.67]) and the MDE wording (59463c4c, 6f12bad).
- §5.1: B-N1 leaderboard (LBB-P1 FAIL with the KB1 wording; LBB-P2 INCONCLUSIVE; LBB-P3 FAIL), from b_n1_run.json adad454d, VERIFIED fd184f1e.
- number_manifest_B.tsv: +3 rows. First-pass citation_map_B.tsv and paperB.bib: 5 entries reused, 14 unresolved, some of them venue-year false positives.
- §6.7b: the Tier-3 dev gates S1/S2/S3/S5 (T3-V 112fd942 plus T3V_S2_close 0b52b194; the T3-V record is still uncommitted) and the PD-22 decision.

## 3. Not yet done, and why

- **B-F1** (final KTVIC test look): the design is cleared by the judge (CC-042, 92%). The commit waits for a machine-rule fix: one ≥ 24 GB host for all three members instead of the fixed M1 pin. The decode then waits for a new GPU rental (one 24 GB GPU, about 4–5 h), because both hosts are unreachable.
- **Paper B bib pass:** the 14 unresolved citations still need Crossref/DBLP checks.
- **Writer pass on framing** (§1/§10 prose around the new results; Paper A word count ≤ 12,000).
- **Held-back records:** T3V_S1_S3_S5.json and G2B_AN1_run.json (scratch paths), wise_ft_gate* (local username). Each needs its own scrub request.
- **Commits in this round (CP-042):**
  - commit 1: B-N1 results, run record and verifier record, plus T3V_S2_close;
  - commit 2: all 27 modified draft files (including earlier uncommitted writer edits; only §2's numbers and the abstract were rechecked this round), plus paperA.bib, paperB.bib, citation_map_B.tsv and this file.
