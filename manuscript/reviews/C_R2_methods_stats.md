# Paper C review: Reviewer R2 (methods and statistics)

All scores, the recommendation and every judgement are AI opinion (generated reviewer). Panel output of 2026-10-29.

**Scores (1-5):** novelty 2, correctness 4, contribution 3, clarity 3. **Recommendation:** major revision (TALLIP). **Confidence:** 4/5. **Q1 (Neurocomputing):** not ready.

## Summary

Carefully preregistered and unusually transparent. Headline numbers match the decision files exactly: P1 +4.49 [3.52, 5.57] PASS, P2 PASS both backbones, XM-a +0.70 [-0.45, 1.97] FAIL, P1-EN +3.08 [2.08, 4.03] PASS, S-NC +1.73 [0.94, 2.50] FAIL. Failed tests are reported adequately; no "first" claim. Weaknesses:

- Limited novelty; OpenFlamingo's RICES-vs-random COCO comparison is not cited.
- Pooled two-backbone estimand hides opposite-signed effects on COCO.
- SESOI +2.0 has a weak basis and is carried unchanged to PTB CIDEr-D.
- A power statement promised in the stage-2 registration is missing.
- Prose under Table 21 ranks systems after saying "not a ranking".
- The §6.8 "explain" sentence claims more than its caveats allow.
- Key instruments depend on two unpublished companion papers.

## What was checked

- All section files 00-11, number manifest, bib audit, PDF (37 pp.; supp 20 pp.).
- Registrations: prereg/2026-10-22_c_stage2, 2026-10-25_c_test, 2026-10-27_c_en.
- decide_ov.json: P1 d = 4.494 [3.524, 5.570] PASS, L false; P2 Qwen +5.41 [3.88, 7.01], InternVL3 +1.57 [0.65, 2.51]. decide_xm_m3.json: XM-a 0.700 [-0.453, 1.974] FAIL. decide_coco_test.json: P1-EN 3.076 [2.084, 4.033]. decide_nocaps_val.json: S-NC 1.726 [0.940, 2.499] FAIL.
- Table 21 own rows trace to ledgers (COCO Qwen ret 96.36 = mean_cider_ptb); ((96.36 - 88.57) + (85.34 - 86.98)) / 2 = 3.08.
- Abstract 195 words.
- Novelty search partial (arXiv API, web; OpenAlex rate-limited, Semantic Scholar empty). Published Table 21 numbers not re-verified.

## Strengths

(a) Exemplary design: equal-k random control from the same memory, fixed control, zero-shot and copy baselines, paired image bootstraps, registered length rule. (b) One-look discipline documented (Section 7). (c) Failed tests prominent: 00:7, 06:61-67, 08:64 (post-XM-a rule choice disclosed 08:18, 09:41), 09:6, 10:7. (d) No priority claim (02:19, 02:49). (e) Per-backbone rows accompany pooled rows; unregistered rows labelled.

## Major issues

**M1. Missing English prior art.** OpenFlamingo (Awadalla et al. 2023, arXiv 2308.01390, Table 9): RICES vs random on COCO at equal shots, 4-shot 89.0 vs 93.1, 32-shot 99.5 vs 109.0. Not in paperC.bib. Pointers 02:17, Table 1 at 02:27-42, contribution 2 at 02:46. Change: add OpenFlamingo (RICES from Flamingo) to Table 1; present P1-EN as replication of a known English pattern under text-only examples and a one-look test; state that related-work searches were partial (02:19 is one query on one date).

**M2. Pooled estimand hides sign heterogeneity.** COCO pooled +3.08 = Qwen +7.80 and InternVL3 -1.64 [-2.79, -0.49] (08:48-49). Abstract opens "Retrieval passed its registered test in both languages" (00:7), repeated 10:5. Change: keep PASS, but state model-specificity in the same sentence (e.g. "the registered pooled test passed; the gain was detected for Qwen2.5-VL only, and InternVL3's COCO row was below zero"); in 05:19 explain why a two-model average; add limitation at 09:5; say whether any scope sentence was registered for P1-EN (08:58 uses free wording).

**M3. SESOI weak basis, applied across scales.** Stage-2 PREREG:284 takes +2.0 from a planning suggestion ("goi y +2"). No rationale in 05:19 / 01:24. Reused on PTB at 08:18, 08:24: ~2% of `rand` 88.57 vs ~6% of 31.48 stripped. S-NC would have passed under the XM-a rule. Change: give a rationale (literature differences, run-to-run, or dev-B SE); relative-size note per language; state English SESOI is relatively more lenient on COCO and that S-NC fails on the point condition alone. No verdict changes.

**M4. Registered power statement missing.** Stage-2 PREREG:301: "At SE about 1.85 per backbone, the chance of passing G1 is about 50% if the true Delta is +4 ... the paper states this power." No power statement in any section. Change: in 05 (~line 8, stage B) and §5.2 report registered G1 power; give achieved CI half-widths or MDE for P1, XM-a, P1-EN, S-NC; an equivalence remark against ±2.0 (XM-a upper bound 1.97 just below +2.0).

**M5. Table 21 used as a ranking.** 08:122 vs 08:147. Mismatches: XM row is XM-test2500 (08:143) vs full XM3600 for LMCap/CONCAP; Vietnamese rows use as-written column; caption at 08:124 says "sets of Table 3" but OpenViIC row uses all 2,001 files; NoCaps images re-fetched from Open Images bucket (08:108). Change: delete above/below sentences at 08:147; add "differences" column (subset, tokenizer, df set, image source); consider moving Table 21 to supplement.

**M6. Mechanism overclaim.** 06:220 "the dev ablations explain why the retrieval gain depends on the backbone"; same paragraph: configs differ in k/order/tail, uptake "not settled", account fails on XM-test2500, COCO, NoCaps (06:222). Also contribution 3 (02:47). Ablation registered after test, on a non-fresh set, two of six τ points known (06:181-184). Change: bounded wording, e.g. "on OV-dev-B, the frozen deletion step accounts for about 2.95 of InternVL3's ret-rand shortfall (+5.36 to +2.41)"; drop or demote contribution 3.

**M7. Central instruments in unpublished companion work.** Scoring kit, stripping convention, tone-normalised matcher, count-matched precision, English class map (01:3, 01:16; 03:59, 03:93, 03:97; 02:21). Change: self-contained definitions of ΔP_cm and the matcher (class list, gold construction) in paper or supplement; provide anonymised companion manuscripts or code as reviewer-only material.

**M8. Design confound in confirmatory InternVL3 row.** τ = 0.10 kept after H_G failed at stage B (allowed: stage-2 PREREG:336-337; 06:140). Deletion step taxes `ret` more than `rand` (Table 15). Change: state at 09:19 as a design limitation of the registered estimand; report the stage-A ΔP_cm constraint as the reason τ = 0.10 was chosen.

## Minor issues

- m1. P2 compares `ret` with `zs` (05:28); "no object-precision cost from retrieved examples" (06:45) mixes retrieval and in-domain style. Add `ret`-vs-`rand` ΔP_cm descriptive row or reword "from in-context examples".
- m2. Bootstrap uses full-set document frequencies (05:75-77), not recomputed per resample: state as standard approximation. CIs condition on one `rand` draw per image: say so at 09:10.
- m3. Heading 08:88 reads like a finding; practitioner point 10:14 repeats it. Recast as a question/hypothesis.
- m4. At 08:64 add that S-NC would pass under the XM-a lower-bound-only rule.
- m5. Multiplicity (05:78): one sentence on why each claim is controlled at its own alpha.
- m6. Cite the "all configurations tried" appendix (11_supplement:255, Tables S10-S11) by table number.
- m7. Add VieCap4H at 02:19 / 01:5, or explain exclusion.
- m8. Move operational detail (07:7-13, 07:74, 08:98-100) to supplement; keep one-paragraph summary.
- m9. Abstract quotes InternVL3 COCO -1.64 without "reported row/unregistered" label.
- m10. Memory sizes 10,501 vs 112,255 (01:5): no size-equalised experiment; cite AB-M as dev-only; do not imply a cross-language size effect.
- m11. Placeholders ("[AUTHOR TO PROVIDE]", DOI nnnnnnn); Nguyen2026FAIR bib entry NOT_CHECKABLE.
- m12. 37-page main PDF; check TALLIP length guidance; condense Tables 13-17.

## Q1 readiness

Not ready. Would need: (i) 3-5 backbones across families/sizes so backbone dependence is an estimable moderator; (ii) a registered deletion-free design or deletion as a factor; (iii) memory-swap test on fixed images for domain coverage, under a new three-tier registration; (iv) full engagement with multimodal ICL selection literature (RICES/OpenFlamingo, Yang 2023, Li 2025, Baldassini 2024). Even then TALLIP or a language-resources venue fits better.

## Recommendation

Major revision. No requested change alters a registered verdict; changes are reframing, citations, and stating what registrations promised (power) or data already hold (relative SESOI size, CI half-widths). No new labels, no new test looks, no GPU.
