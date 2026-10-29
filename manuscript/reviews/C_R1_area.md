# Paper C review: Reviewer R1 (area / general expert)

All judgements are AI opinion (generated reviewer). Copied verbatim in substance from the review panel output of 2026-10-29.

**Scores (1-5):** novelty 2, correctness 3, contribution 3, clarity 3. **Recommendation:** major revision (TALLIP). **Confidence:** 4/5. **Q1 (Neurocomputing):** not ready as framed; the paper proposes no method.

## Summary

The manuscript is a carefully preregistered, training-free study of retrieval in-context captioning for Vietnamese, with an English arm. Retrieved example captions are compared with random captions from the same memory at equal k (plus fixed-example and zero-shot controls) on Qwen2.5-VL-7B and InternVL3-8B. Every headline number spot-checked matches the decision files exactly: P1 +4.49 [3.52, 5.57], P1-EN +3.08 [2.08, 4.03], XM-a +0.70 [-0.45, 1.97], S-NC +1.73 [0.94, 2.50], P2, XM-b, the scope sentence and the length gaps. Both failed out-of-source tests are reported prominently and honestly. Method novelty is modest, and the paper says so. The main problems are interpretive:

- The SESOI of +2.0 has no stated rationale and is carried from stripped, word-segmented Vietnamese CIDEr-D to English PTB CIDEr-D, a scale the paper itself calls non-comparable.
- The pooled two-backbone estimand hides backbones of opposite sign. On COCO the pooled test passes while InternVL3's CI is wholly below zero.
- InternVL3's null is partly confounded by keeping a deletion step whose guard hypothesis failed at stage B.
- The published-results prose (08:147) ranks systems despite the "position, not a ranking" disclaimer.
- Word vs syllable segmentation is described inconsistently.
- Missing related work: Flamingo/OpenFlamingo RICES vs random demonstrations, and VieCap4H.
- The process detail is very heavy for a journal.

## Verification performed

- Read every section file, supplement headings, the manifest structure, the bib audit, and both test preregistrations (manuscript/prereg/2026-10-25_c_test/PREREG.md; 2026-10-27_c_en/PREREG.md).
- Checked against decide_ov.json, decide_xm_m3.json, decide_xmb.json, decide_coco_test.json, decide_nocaps_val.json: P1, P1b, P2, scope row and sentence, length gaps, S-zf, NN baselines, neighbour-only precision (pooled 73.72, sum_m 2,097 = 1,933 + 164), XM-a, XM-b, XM prediction ('not confirmed'), P1-EN, S-NC and the 3,500 sensitivity all match.
- Table 4 and Table 18 decision rules match the preregistrations, including the disclosure that the NoCaps rule was fixed after XM-a was known.
- From arXiv PDFs: SmallCap 119.7 (COCO) / 77.9 (NoCaps val), MeaCap_TF 56.9 / 40.2, LMCap vi 0.265, MDSANet 75.5796 are copied correctly.
- Novelty searches (arXiv API; Crossref; OpenAlex and Semantic Scholar rate-limited; no e-mail supplied): no prior Vietnamese retrieval or in-context captioning study found. Surfaced VieCap4H (VLSP 2021) and AfriCaption (2025), not cited. No Flamingo/OpenFlamingo entry in the bib.
- LaTeX build (tex/paperC.pdf 37 pp.; paperC_supp.pdf 20 pp.): no undefined references; PDF newer than all sources.

## Major issues

**M1. SESOI unjustified, and its transfer across scales unjustified.** 05_preregistration_and_analysis.md:19 sets +2.0 stripped CIDEr-D with no rationale (test prereg :148 only cites PR2). 08_english_comparison.md:18 applies the same +2.0 to PTB CIDEr-D although 08:16 and 09_limitations.md:22 say the scales are not comparable. Relative to `rand` (OV ~31-33; COCO ~87-89), +2.0 is ~6% in Vietnamese and ~2% in English, so "stricter" NoCaps rule (08:18, 09:6, 09:41) holds structurally, not in effect size. Change: one paragraph in §5.2 on the origin of +2.0; in §8.1 state the English SESOI was carried numerically, not calibrated; report Δ/`rand` beside P1, P1-EN, XM-a, S-NC as descriptive rows.

**M2. Pooled estimand hides opposite signs.** COCO: P1-EN pooled +3.08 passes while InternVL3 is -1.64 [-2.79, -0.49] (08:49, 58). Backbones differ in k (8 vs 4), order, tail, τ (03_method.md:79-87). Out of source, Qwen's CIs exclude zero: XM +3.15 [1.50, 4.93] (06_results.md:54), NoCaps +2.83 [1.69, 3.98] (08:48); for Qwen the gain shrinks out of domain rather than vanishing. Change: lead with the per-backbone picture in 00_abstract.md:7 and 01_introduction.md:30-31; rephrase 08:88 and 10_conclusion.md:14 to acknowledge Qwen's positive out-of-source rows. Keep every verdict.

**M3. InternVL3 null partly a design confound, not disclosed in the abstract.** Frozen InternVL3 keeps the post-decode deletion step at τ = 0.10 (03:86-89) although H_G failed at stage B (06:140). Dev ablation: the step taxes `ret` more than `rand` (06:214; Table 15: +5.36 without deletion vs +2.41 at τ = 0.10); 09:19 names this threat. Change: one clause in abstract and contribution 2; bring the registered τ = -∞ secondary (OV-test +3.71 [2.29, 5.14] detected; COCO -1.05 not detected) into the main narrative.

**M4. Published-results comparison read as a ranking.** 08:122 disclaims ranking, 08:147 orders systems. Rows heterogeneous: MeaCap COCO row uses COCO memory, NoCaps row CC3M memory; this study's Vietnamese rows use the as-written column on 2,001 images and XM-test2500; EVCap/SmallCap/ViECap are COCO-trained while this memory is COCO. Change: delete ordinal sentences at 08:147, keep the Vietnamese-gap sentence; add "memory / training data" and "scorer/column" columns to Table 21; caption states no ordering implied.

**M5. Missing MLLM-era precedent.** No Flamingo/OpenFlamingo/RICES in paperC.bib. Their RICES vs random demonstrations at equal shots on COCO is close to `ret` vs `rand`. VieCap4H (VLSP 2021) absent from 02:19. Change: add OpenFlamingo/Flamingo row to Table 1 with the difference (interleaved image-caption vs text-only captions); add VieCap4H. The hedged no-priority statement stands.

**M6. Segmentation described inconsistently.** 03_method.md:93 and test PREREG :123 use RDRSegmenter word segmentation; 08:147 says word-segmented; 08:16 and 09:22 say syllable-segmented; length is in syllables (05:26, 06:37-39). Change: state once that CIDEr-D uses RDRSegmenter word tokens and length uses syllables; fix 08:16 and 09:22.

**M7. Reporting rules vs English per-backbone wording.** 05:62 says no secondary (incl. per-backbone values, 05:69) enters title/abstract/contributions, yet 00:7 and 01:30 cite InternVL3 COCO -1.64. English prereg §7 registers no scope sentence, yet "carried mainly by Qwen2.5-VL" is applied to COCO at 00:7, 01:30, 08:86, 10:5. Change: label English scope wording as a descriptive reading, or amend 05:62 to allow per-backbone rows as descriptive. Prefer keeping the negative InternVL3 information.

**M8. Length / process detail.** 37 pp. + 20 pp. supplement. §7 (07_disclosures.md:1-76) and §8.5 (08:94-118) contain timestamps, PI approval times, worktree/commit hashes, mirror checksum failures, laptop-side guards, sister-study logistics. Change: one disclosure table in main text (item, effect on data, exposure, verdict changed?); move 7.1, 7.2, 7.7 timestamps, 8.5 amendment, smoke test, worktree to supplement; cut §6.8 to the τ ablation plus one sentence each on k and memory size.

## Minor issues

- m1. Add one sentence on low-resource multilingual captioning beyond Vietnamese (e.g. AfriCaption, arXiv 2025).
- m2. 08:141 "training-free, image-blind" for LMCap: image used for retrieval; suggest "training-free; text-only generator, image used for retrieval".
- m3. Table 21 Vietnamese rows use `cider_w` (as written) vs stripped decision column on 1,941 images (Qwen OV ret 33.64 vs 39.81); say so or add stripped values.
- m4. 03:16 / Table 3: one sentence on why KTVIC train is 3,469 after the 300-image carve.
- m5. `rand` - `zs` is central but descriptive/post hoc on test; mark as non-registered in Table 9 and give value with CI.
- m6. Non-monotone cosine-tertile pattern (06:105, 08:90): explain or state none is offered; "not interpreted further" conflicts with later use in 8.4.
- m7. §5.4: one sentence on Monte Carlo error of bootstrap bounds near thresholds (B = 2,000).
- m8. Give full P_cm and matcher definition in the supplement (05:28-33 partial).
- m9. Verifier lineage (InternVL3 LM is Qwen2.5; Qwen3-VL verifies InternVL3): one line on why no bias, or list in §9.
- m10. Abstract is 195 words; if M3 adds a clause, trim (merge OpenViIC sentences).
- m11. 09:10 decode-parity 52/52: add "on the same machine and software stack".
- m12. 07:74 cites unversioned working/decision logs; archive or drop timestamps.
- m13. Figure 1: separate per-language panels with own axes; check ≥600 dpi (vector PDF fine).

## Specific checks

- Failed tests reported adequately: yes (00:7, 01:31, 06:61-67, 08:64, 10:7, 09:6); registered wording verbatim; XM-b PASS does not rescue the XM prediction.
- Comparison table presented as ranking: partly yes (see M4).

## Binding constraints noted by the reviewer

No new data, labels or test looks needed; relative gains are descriptive re-expressions of existing ledger means labelled post hoc; FAILs stay as reported; no dataset caption text; no "first" claim.
