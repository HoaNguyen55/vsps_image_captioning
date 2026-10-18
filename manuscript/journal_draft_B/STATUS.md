# Paper B draft status (2026-10-15; stopped early on user priority: research before writing)

## Sections

| File | Status |
|---|---|
| outline_B.md | done (incl. Gemini v2 audit) |
| sec1_intro.md | done (first draft) |
| sec2_related.md | done; PD-7 Q5 applied (HDUCap/ViG cited without numbers, ViCLIP-OT leakage, OpenViIC SPIC citation); several [VERIFY] tags remain |
| sec3_data_and_audit.md | done (first draft) |
| sec4_system.md | done; PD-8 applied (B1 aborted at Step 1 guard; "two model scales of one family (7B, 3B)"; post-hoc calibration note) |
| sec5_results.md | done (first draft) |
| sec6_negatives.md | done (first draft) |
| sec7_discussion.md | done (first draft) |
| sec8_limitations_ethics.md | done; new KTVIC release wording applied |
| number_manifest_B.tsv | 329 rows: 313 keyed, 1 derived, 5 literature, 10 PENDING, 0 mismatches (generator: scratchpad `build_manifest_B.py`; not in repo) |
| new_vs_FAIR.md | done: about 88% new (range 85–91%) |

The draft has not been self-reviewed end to end and no automated check yet confirms that every in-text number has a src comment. Run that check before red-teaming.

## Open TODOs

- PENDING runs: ladder 56/57/58 reruns; 3B fallback runs; optional Qwen3-VL post-guard run; POPE-500 for UIT-ViIC adapters (exclude all 21, CC-005); EV-RANK gate → M3; WiSE-FT; protocol-matched comparators.
- **Run-ID clash:** the brief says ladder runs 56–58 are being rerun; PD-8 calls the 3B runs "57/58". Confirm which jobs carry these numbers.
- Read HDUCap and ViG in full before 2026-11-01. On 2026-10-15 ScienceDirect returned 403 and IEEE Xplore returned no content.
- XM3600: compute the fine-tuned systems' CIDEr-D with a period appended, to decompose the drop.
- Paired CI for the UIT-ViIC role/child CHAIR_i flip; human sign-off of matcher v3.
- Verify the [VERIFY] citations: XM3600, Qwen3-VL report.
- The ladder TOST (±1/±2) was committed after runs 54/55 landed. The draft labels it post-registration; keep that label.

## Mismatches found in Gemini's `_v2` tables

All 2,349 traced cells (master tables 2,209 + ledger 140) match their source keys, and every stated file hash matches. The errors are in the prose:

1. Ledger B-T2 says "5/6 runs inside all intervals". The source gives **4/6**: fuse2_s43-detailed has M = 3.2545 > 3.254.
2. B-T2 says "confirms L over T"; this overclaims, because T was refuted beforehand and four of the six runs are fuse2 seed replications.
3. B-T3 says role/child canonicalisation "resolves" CHAIR_i, but that matcher is unattested.
4. B-T5 uses the forbidden "typicality vs truth" wording.
5. RESOLVED: +20.70 / +32.72 are Paper A's (gold-completeness slope differences); removed from B.
6. Outside the v2 tables: c1 gives the zero-shot CIDEr as 34.33 → 38.02, but the committed scorer gives 28.98 → 33.30; and Gemini's XM3600 `.md` gives 99.83% where its JSON gives 99.5.
