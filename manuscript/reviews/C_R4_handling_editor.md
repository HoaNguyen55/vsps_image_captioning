# Paper C review: Reviewer R4 (handling-editor view)

All judgements are AI opinion, not checked by a human expert. Panel output of 2026-10-29.

**Scores (1-5):** novelty 2, correctness 4, contribution 3, clarity 2.5. **Recommendation:** major revision (TALLIP). **Confidence:** 4/5. **Q1 (Neurocomputing):** not ready on fit; no method contribution.

## Summary

Carefully preregistered, honestly reported. Headline numbers match: P1 +4.49 [3.52, 5.57], P2, XM-a +0.70 [-0.45, 1.97] FAIL, XM-b, P1-EN +3.08 [2.08, 4.03], S-NC +1.73 [0.94, 2.50] FAIL. Rules match PREREG.md (2026-10-25_c_test, 2026-10-27_c_en). Both FAILs reported adequately. Main problems: (1) Table 21 is in effect a ranking, omits a higher Vietnamese row from the very table it cites (Pangea 64.3, CONCAP Tab. 10), and juxtaposes differently scored Vietnamese numbers; (2) dev-only "explain why" sentence and contribution 3 overclaim; (3) no pretraining contamination discussion for COCO/NoCaps; (4) narrow novelty, far too long for its contribution.

## What was verified

- P1 4.494 [3.524, 5.570] PASS, L false; P2 Qwen +5.41 [3.88, 7.01], InternVL3 +1.57 [0.65, 2.51]; XM-a 0.700 [-0.453, 1.974] not passed; XM-b 0.591 [-0.310, 1.544] passed; P1-EN 3.076 [2.084, 4.033] PASS; S-NC 1.726 [0.940, 2.499] FAIL, per-domain 4.64 / 1.96 / 0.43. All agree with text.
- Rules: SESOI +2.0; P1 point > +2.0 and lower bound > 0; P2 and XM-b floors -1.0; XM-a lower bound > 0; scope mapping; English rule fixed after XM-a, stricter: all match.
- Table 21 own English values trace to ledger keys (96.36 = cen_qwen25vl coco ret mean_cider_ptb).
- Published values against arXiv PDFs: SmallCap 119.7 / 77.9; EXTRA 120.9; EVCap 140.1 / 119.3; ViECap 92.9 / 66.2; MeaCap-TF 56.9 (COCO memory) / 40.2 (CC3M); LMCap vi 0.265; CONCAP vi 45.1; MDSANet 75.58.
- Searches: arXiv API, Crossref; OpenAlex and Semantic Scholar refused (429). No e-mail sent.

## Major issues

**M1. Table 21 presented as a ranking.** 08:122 vs 08:147. Change: delete the sentence; replace with one order-of-magnitude sentence (e.g. "training-free MLLM prompting falls between text-only/training-free systems and trained captioners on COCO") or drop the paragraph; print published and own rows as two separate blocks.

**M2. Row selection has no stated rule and favours this study.** XM3600-vi row cites CONCAP 45.1 from @Ibrahim2025CONCAP Tab. 10 (08:142); the same table (arXiv 2507.20411) lists Pangea vi 64.3 (above this study's 59.13) and mBLIP vi 35.8. LMCap Tab. 6 lists BB+CC baseline 0.336 next to LMCap 0.265. Change: state an inclusion rule in the caption; add Pangea (and mBLIP) or remove the XM3600-vi block.

**M3. Vietnamese rows not comparable but printed as comparable.** Own XM3600/OpenViIC values are `cider_w` on VnCoreNLP-segmented text, XM-test2500, OpenViIC all 2,001 files; published values use other tokenisation and full sets. 08:147 itself says "the scorers differ too much for a position". Change: drop own Vietnamese rows from Table 21, or flag "not comparable: different segmentation and image subset". Do NOT re-score used test sets with a published scorer (second look).

**M4. Mechanism claim beyond evidence.** 06:220 "explain why"; 06:221-222 concede not a clean contrast, uptake not settled, account fails on XM-test2500, COCO, NoCaps; 02:47 lists it as contribution 3. Registration permission does not make the claim supported. Change: "on OV-dev-B only, the deletion step accounts for part of InternVL3's smaller contrast; the ablations are consistent with, but do not establish, a backbone explanation"; remove as numbered contribution or reword as dev-only diagnostic.

**M5. Pretraining contamination not discussed** (grep contamin/pretrain/leak: nothing). Qwen2.5-VL and InternVL3 very likely saw COCO images/captions, possibly NoCaps/Open Images. Bears on absolute COCO/NoCaps positions vs COCO-only systems, and possibly on `ret`-`rand` (retrieved COCO captions may cue memorised wording). Change: paragraph in §9.1 or §9.2 with what is known of each model's training data; mark Table 21 English rows. No new experiment on used test sets.

**M6. Narrow contribution; two omitted works.** 01:34 "does not propose a new method"; §2 concedes prior art. Omitted: Re-ViLM (arXiv 2302.04858), retrieval-augmented zero/few-shot captioning; AmericasNLP 2026 "Gators" submission (arXiv 2605.20626), retrieval-augmented many-shot prompting for low-resource-language captioning with Qwen2.5-VL, reporting retrieval helps only with large in-domain data; anticipates the post-hoc domain-coverage reading at 08:88. Change: cite and position both; rewrite 08:88 as agreeing with prior finding, not new. Neurocomputing: not ready on fit.

**M7. Headline pooled result depends on one backbone and two configurations; abstract is method-level first.** 00:7 opens "Retrieval passed its registered test in both languages" and gives the COCO pooled number before any scope sentence; 05:39-47 requires the scope sentence "beside every pooled number". InternVL3 +0.66 [-0.68, 1.99] OpenViIC, -1.64 [-2.79, -0.49] COCO; different k/order/tail/τ (Table 2). Change: (a) abstract leads with Vietnamese P1 (English arm registered after); (b) "carried mainly by Qwen2.5-VL" in the same sentence as each pooled number; (c) §5.2 states the pooled estimand averages two backbone-plus-configuration pairs. Third backbone / memory-swap = new study (dev-explore, dev-confirm rehearsal, single look at fresh test set): future work only.

**M8. Length and internal bookkeeping.** 37 pp. + 20 pp., ~21 main tables. Internal terms: working-log timestamps and "approved by the principal investigator" (07:74), "sister study ... now stopped" (07:53), "refusal list" (03:11), "decoding machine", worktree/commit hashes (07:17-19; 08:98), parity rerun narrative (07:7-13). Change: move Tables 12-14, most of §6.8, §7.1-7.3, §8.5 and "all configurations" material to supplement; one-paragraph deviations summary; reader-facing terms; target ~25 pages.

## Minor issues

- m1. 02:19 omits VieCap4H (VLSP 2021; arXiv 2209.01304) and a 2026 Vietnamese scene-text captioning dataset (arXiv 2604.27712); list or qualify "general-domain".
- m2. 10:14 practitioner advice from two failed tests; XM high-cosine tertile lowest point (06:103-105) cuts against it. Shorten item 3; cite AmericasNLP 2026 as external support.
- m3. Companion-study definitions (01:3, 01:16, 03:59, 03:93-97): give operational definitions in supplement; anonymised companion manuscripts to the editor.
- m4. InternVL3 `ret` at τ = 0.10 falls back to zero-shot for 0.351 of OV-test (06:136); state in Table 2 note and §3.4.
- m5. TALLIP asks for test statistics with p-values; 09:35 says none. Justify CI-only rule in one sentence, or add p-values labelled POST HOC, no verdict change.
- m6. Abbreviation glossary near §5; plain names in abstract and conclusion.
- m7. Table 21 caption (08:124): which column is shown; EVCap uses Vicuna-13B; MeaCap COCO row is its in-domain (COCO-memory) setting (arXiv 2403.03715 Tab. 2).
- m8. Manifest `used_in` does not list 08_english_comparison.md for Vietnamese Table 21 values (59.13, 53.47, 33.64, 29.70); values trace correctly to `cider_w`; bookkeeping only.
- m9. Abstract NoCaps number: add "point below the +2.0 SESOI".
- m10. acmart warnings ("several authors in the same \author macro", "No city present for an affiliation"); author placeholder; confirm anonymity mode on ScholarOne.
- m11. Consolidate `rand` - `zs` descriptives (06:84, 08:60) into one labelled descriptive table.

## Specific checks

- Failed tests adequate: yes (00:7, 01:31, 06:61-67, 08:64, 09:6, 10:7); XM prediction "not confirmed" despite XM-b; NoCaps rule choice disclosed. Mild concern: §8.4 and conclusion item 3 turn failures into a positive recommendation.
- Comparison table a ranking: in effect yes (M1-M3).

## Constraints

No new human labels, AI labels, GPU runs or test re-looks. Further experiments (third backbone, memory-swap) go through the three tiers on fresh test sets: future work. No dataset caption text in any file.

## Recommendation

Major revision for TALLIP. With M1-M5 fixed and main text shortened, a credible, careful TALLIP article whose main value is evaluation methodology. Not recommended for Neurocomputing as is.
