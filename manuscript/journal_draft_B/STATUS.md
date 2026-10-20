# Paper B draft status (2026-10-19, B-writer; supersedes the 2026-10-15 version)

Framing: resource + validity audit with a released evaluation kit; no method claim (DEBATE D2). Complete draft due 2026-12-10. Change log: `WRITER_B_LOG.md`.

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

## Open TODOs

- PENDING runs: 3B 61/62 (M2); optional Qwen3-VL post-guard run; POPE-500 for UIT-ViIC adapters (exclude all 21, CC-005); M3 = Tier-3 S3 (a68fb66, not run); B-N1 decodes; B-N2 placebo and descriptive gaps (judge); WiSE-FT addendum items (separate task agent); UIT-ViIC append-period effect with the committed scorer; protocol-matched comparators.
- Ladder: reruns scored (6/10 runs all-in; joint 10-run CI [−0.90, +0.92]); registered H0 NOT met (PD-20: pooled part met, per-run part not).
- B-N3: NOT_RUN (PD-21b sentence verbatim in sec8.1). The FAIR-2026 human ratings support no claim in Paper B, and a search of sec1–8, the outline, STATUS and the manifest found no number or claim drawn from them.
- B2 tables and figures (MANIFEST 44430973): use only after the A-verifier marks them VERIFIED. Fig. 2 = `fig2_adjacency_Bonly` (placeholder comment in §3.2).
- Release-kit checklist: these kit components exist only in git-excluded session folders: v3 rules (cay audit, role/child), the c8 punctuation audit, the XM3600 period audit, the UIT-ViIC/COCO overlap lists, and the 8-gram scanner. Move them into a release directory and re-run before submission. Checkpoints stay "on request" until the backbone licence and KTVIC's terms are confirmed.
- Read HDUCap and ViG in full before 2026-11-01; verify the [VERIFY] citations (XM3600, Qwen3-VL report).
- Paired CI for the UIT-ViIC role/child CHAIR_i flip: `.session_backup/2026-10-18/cpu_audit_r15/uitviic_role_child_chair_flip_ci_v1.json` exists but is unverified.
- Run an automated src-comment completeness check over all sections before red-teaming.
- Resolved: run-ID clash (3B = 61/62; GPU_JOB_PLAN_v1); XM3600 period decomposition (absolute shift); matcher v3 sign-off dropped (no new annotation).
