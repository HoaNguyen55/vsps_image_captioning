# Paper C: Meta-review (Area Chair, ACM TALLIP)

Date: 2026-10-29. Every judgement, score and estimate in this file is **AI opinion** (an AI area chair summarising five AI or external-tool reviewers). None of it is evidence and none of it changes a registered verdict.

## Tóm tắt cho PI (tiếng Việt)

- **Quyết định: MAJOR REVISION** cho TALLIP (5/5 reviewer đồng ý). **Chưa sẵn sàng cho Q1 (Neurocomputing)**, cũng 5/5: bài không đề xuất phương pháp, hiệu ứng chỉ có ở 1/2 backbone (Qwen2.5-VL), và cả 2 test ngoài nguồn (XM-a, S-NC) đều FAIL. Muốn lên Q1 phải làm nghiên cứu mới (thêm backbone, thiết kế không có bước xoá, hoán đổi memory), đăng ký lại theo 3 tầng trên test set mới. Việc này không thuộc lần sửa này.
- **Điểm đồng thuận (1-5):** Novelty 2.0 (cả 5 người cho 2), Correctness ~3.6, Contribution ~2.8, Clarity ~2.9.
- **Điểm mạnh được công nhận:** mọi số headline khớp file decide_*.json. Các test FAIL được báo cáo trung thực và nổi bật. Không có claim "first".
- **5 việc quan trọng nhất (chỉ sửa chữ, không cần GPU):**
  1. Abstract/đóng góp: đặt P1 OpenViIC lên đầu và nói "chủ yếu do Qwen2.5-VL" ngay trong câu có số pooled.
  2. Bảng 21: xoá câu xếp hạng ở 08:147, nêu quy tắc chọn dòng, đánh dấu các dòng tiếng Việt là không so sánh được.
  3. Thêm Flamingo/OpenFlamingo (RICES so với random trên COCO) và VieCap4H. Trình bày P1-EN như một replication.
  4. Hạ câu "explain" ở 06:220 và bỏ đóng góp số 3.
  5. Nêu đúng nguồn gốc SESOI +2.0 (một giá trị lập kế hoạch, không hiệu chỉnh), thêm câu power đã hứa trong prereg, và nói rõ English dùng lại +2.0 mà không hiệu chỉnh.
- **Không cần thí nghiệm mới cho lần sửa này.** Các đề xuất thí nghiệm (nhiều lần rút `rand`, phân tích che n-gram trên dev, backbone thứ 3, hoán đổi memory) được chuyển cho coordinator.
- **Cảnh báo:** ba trích dẫn do một reviewer đơn lẻ đưa ra phải được kiểm tra trước khi dùng: AmericasNLP 2026 "Gators" arXiv 2605.20626, bộ dữ liệu scene-text arXiv 2604.27712, và Pangea 64.3 trong CONCAP Tab. 10. Lý do SESOI phải ghi đúng sự thật lịch sử, không được bịa một lý do hậu kiểm.
- **Ước tính sau khi sửa (ý kiến AI):** Correctness khoảng 4, Clarity khoảng 3.5-4, Contribution khoảng 3, Novelty vẫn 2-2.5. Khả năng được TALLIP chấp nhận sau vòng 2 ở mức khá.

## Reviewer files

| Reviewer | Profile | File |
|---|---|---|
| R1 | Area / general expert | manuscript/reviews/C_R1_area.md |
| R2 | Methods and statistics | manuscript/reviews/C_R2_methods_stats.md |
| R3 | Evaluation metrics, benchmark validity | manuscript/reviews/C_R3_eval_metrics.md |
| R4 | Handling-editor view | manuscript/reviews/C_R4_handling_editor.md |
| R5 | External reviewer (Codex text report) | manuscript/reviews/C_codex_review.md (already on disk; left unchanged) |

## 1. Consensus scores (AI opinion)

| Criterion | R1 | R2 | R3 | R4 | R5 | Consensus | Disagreement |
|---|---|---|---|---|---|---|---|
| Novelty | 2 | 2 | 2 | 2 | 2 | **2.0** | None. All five agree: no method, prior art on the random control (EXTRA, Li 2024, Yang 2023, Baldassini 2024) and on RICES vs random (OpenFlamingo, cited by R1-R3). |
| Correctness | 3 | 4 | 4 | 4 | 3 | **3.6 (median 4)** | R1 and R5 score lower. R1 cites the SESOI transfer, the opposite-sign pooling and the word/syllable error. R5 cites the single `rand` draw, whose variation the bootstrap does not represent. R2-R4 score the numbers and the rule fidelity higher; all five confirm the numbers match the decision files. |
| Contribution | 3 | 3 | 3 | 3 | 2 | **2.8 (median 3)** | R5 alone scores 2: the generalisable advance is narrow and rests on two backbones. |
| Clarity | 3 | 3 | 3 | 2.5 | 3 | **2.9 (median 3)** | R4 is harsher: about 21 main tables, heavy abbreviations, operations-log content. Everyone flags length (37 + 20 pp.). |

**Decision: MAJOR REVISION** (unanimous; reviewer confidence 4/5 for R1-R4).

**Points of full agreement:**
- All headline numbers are correct.
- Failed tests (XM-a, S-NC) are reported adequately and prominently.
- No "first" claim is made, and the hedged no-priority wording at 02:19 stands.
- Table 21 is a ranking in practice, despite its disclaimer at 08:122.

**Q1 (Neurocomputing) readiness: NOT READY** (5/5). This is a question of fit, not polish: the paper proposes no method, the gain depends on the backbone, and both transfer predictions failed. A Q1 path would require a new study (see §4). That path still requires dev-explore, then a dev-confirm rehearsal, then one look at a fresh test set. TALLIP remains the better venue.

## 2. Conflicts resolved by the AC

1. **Per-backbone numbers in the abstract.** R1 M7 notes that 05:62 forbids secondaries in the abstract and contributions, yet the abstract cites InternVL3 COCO −1.64. R2, R3, R4 and R5 want the per-backbone picture made *more* prominent. **Ruling:** keep the per-backbone information, because it is conservative. Label each such row "reported row, not registered". If 05:62 restates a registered rule, add one deviation line in the disclosures ("per-backbone rows quoted in the abstract as descriptive context; no verdict depends on them"). Do not silently edit the rule text.
2. **"Explain" at 06:220.** The registration licensed this sentence under conditions that hold. R2, R3 and R4 say the claim is still unsupported. **Ruling:** permission is not an obligation. Soften the wording, and keep the note that the registered condition held.
3. **SESOI rationale.** R1, R2 and R3 ask for a rationale. Stage-2 PREREG:284 shows that +2.0 came from a planning suggestion. **Ruling:** state the true origin. Descriptive context (relative size, dev-B SE) may be added, but no post-hoc justification may be presented as the original reason.
4. **Table 21's Vietnamese rows.** R4 M3 says drop them or flag them; R1 m3 and R3 m10 say explain the column. **Ruling:** keep the rows, mark them "not comparable", and name the column. Never re-score a used test set with a published scorer: that would be a second look.

## 3. Prioritised revision plan

Items are ordered by expected score gain per unit of effort. **No item needs a new experiment for this revision.** Items that suggest an experiment are flagged [EXP → coordinator] and are not done here. All score-lift estimates are AI opinion.

| # | Change | Raised by | File(s) | Exact change | New exp.? | Est. lift |
|---|---|---|---|---|---|---|
| 1 | Headline reframing: per-backbone first, Vietnamese primary first | R1 M2/M7, R2 M2/m9, R3 m8/m9, R4 M7, R5 M2 | 00_abstract.md:7; 01_introduction.md:30-31; 05_preregistration_and_analysis.md:19, :62; 08_english_comparison.md:58; 10_conclusion.md:5; 09_limitations.md:5 | (a) Open the abstract's results with P1 OpenViIC (PASS +4.49 [3.52, 5.57]), then P1-EN. (b) Put "the gain was carried by Qwen2.5-VL; InternVL3 was not detected on OpenViIC and its COCO row was below zero (reported row, not registered)" in the same sentence as each pooled number. (c) In §5.2, one sentence: the pooled estimand averages two backbone-plus-configuration pairs (different k/order/tail/τ) and is not a "typical MLLM" effect. (d) At 08:58, state that no English scope sentence was registered and that the wording is a descriptive reading. (e) Add a limitation at 09:5. (f) Add a deviation line for 05:62 (see §2.1). Keep every verdict word for word. Stay within 200 abstract words. | No | Correctness +0.3, Clarity +0.3 |
| 2 | Table 21 is not a ranking | R1 M4/m2/m3, R2 M5, R3 M2, R4 M1/M2/M3/m7/m8 | 08_english_comparison.md:122-147; number_manifest_C.tsv (used_in) | (a) Delete every ordinal sentence at 08:147. Keep one sentence: a training-free prompt remains far below fine-tuned systems on OpenViIC. (b) Print published and own rows as two blocks. (c) Add columns: memory/training data, scorer/tokeniser/column, #images (subset), image source. (d) Caption: "No ordering is implied." (e) State an inclusion rule (e.g. "every system in the cited table" or "best trained / best training-free / closest design"). Then add Pangea and mBLIP from CONCAP Tab. 10, **after verifying Pangea vi 64.3 and mBLIP 35.8 in arXiv 2507.20411**, or drop the XM3600-vi block. (f) Flag own Vietnamese rows "not comparable: as-written `cider_w`, word-segmented, XM-test2500 / all 2,001 OpenViIC files". (g) LMCap label: "training-free; text-only generator, image used for retrieval". (h) Note MeaCap's COCO row uses COCO memory and its NoCaps row CC3M; EVCap uses Vicuna-13B; NoCaps images were re-fetched and scored locally. (i) Optionally move the table to the supplement. Never re-score a used test set. | No | Correctness +0.2, Clarity +0.2 |
| 3 | Related-work gaps and novelty positioning | R1 M5/m1, R2 M1/m7, R3 M1/m6/m11, R4 M6/m1, R5 #4 | 02_related_work.md:17-49 (Table 1, "What is new"); 01_introduction.md:5; 08_english_comparison.md:88; paperC.bib; paperC_bib_audit.tsv | (a) Add Flamingo (arXiv 2204.14198) and OpenFlamingo (arXiv 2308.01390; App. Tab. 9 RICES vs random on COCO: +4.1 at 4 shots, +9.5 at 32; Flickr-30K −20.3 / −13.6) to Table 1. State the difference: interleaved image-caption demonstrations vs text-only captions. (b) Present P1-EN as a replication of a known English pattern under text-only examples and a one-look test. Use the Flickr-30K reversal when discussing InternVL3's COCO sign. (c) Add VieCap4H (arXiv 2209.01304) at 02:19 and 01:5, or narrow the claim to "general-domain". (d) Add Re-ViLM (arXiv 2302.04858) and Li et al. (arXiv 2507.08021, cited by R5). (e) **Verify before citing**: AmericasNLP 2026 "Gators" (arXiv 2605.20626), Vietnamese scene-text dataset (arXiv 2604.27712), AfriCaption 2025. All three come from a single reviewer each. If the Gators paper is real, rewrite 08:88 as agreeing with that prior finding. (f) At 02:19, say the searches were partial (dates, sources). Keep "no priority claim". Run every new bib entry through the bib audit. | No | Novelty +0.0 to +0.3 (honest positioning), Correctness +0.2 |
| 4 | Mechanism overclaim and contribution 3 | R2 M6, R3 M6, R4 M4 | 06_results.md:220-222; 02_related_work.md:44-47; 06_results.md:172 | Replace "the dev ablations explain why the retrieval gain depends on the backbone" with "on OV-dev-B only, the frozen deletion step accounts for about 2.95 of InternVL3's ret−rand shortfall (+5.36 → +2.41); the ablations are consistent with, but do not establish, a backbone account, which does not carry to XM-test2500, COCO or NoCaps." Keep the note that the registered condition held. Remove item 3 from "What is new" (02:47), or reword it as a dev-only diagnostic, so it agrees with 06:172. | No | Correctness +0.2 |
| 5 | SESOI origin, cross-scale use, power statement | R1 M1/m7, R2 M3/M4/m4, R3 M4/M5/m1a/m5, R4 m9 | 05_preregistration_and_analysis.md:8, :19, §5.4; 08_english_comparison.md:16-24, :64, :82 (Fig. 1); fig1_ret_minus_rand.svg; 00_abstract.md:7 | (a) §5.2: state truthfully that +2.0 was set as a planning value at stage 2 (PREREG 2026-10-22_c_stage2:284) without calibration. (b) Descriptive rows labelled post hoc: Δ/`rand` for P1, P1-EN, XM-a, S-NC (about 6% in Vietnamese, about 2% on COCO), from existing ledger means. (c) §8.1: the English SESOI was carried over numerically, not recalibrated; on COCO it is relatively more lenient. (d) **Registered power sentence** (stage-2 PREREG:301): "At SE ≈ 1.85 per backbone, the chance of passing G1 was about 50% if the true Δ = +4." Add achieved CI half-widths for P1, XM-a, P1-EN, S-NC from existing decision files. (e) S-NC: "CI above zero, point below the registered +2.0; it would have passed under the XM-a rule (rule chosen after XM-a was known)." Put this at 08:64 and as a half-clause in the abstract. (f) Descriptive remark: XM-a's upper bound of 1.97 lies just below +2.0. (g) One sentence on bootstrap Monte Carlo error at B = 2,000. (h) Fig. 1: separate per-language panels or axes, with the line labelled "registered threshold, different scales". | No (arithmetic on existing outputs only) | Correctness +0.3 |
| 6 | InternVL3 deletion-step confound | R1 M3/m9, R2 M8, R3 m3, R4 m4 | 00_abstract.md:7; 01_introduction.md (contribution 2); 03_method.md:86-89; Table 2 note; 06_results.md:136-140; 09_limitations.md:19 | (a) One abstract clause: InternVL3's registered arm includes a verifier-based deletion step (τ = 0.10) kept after its guard hypothesis failed at stage B. (b) In the §6 narrative, bring in the registered τ = −∞ secondary, labelled secondary: OV-test +3.71 [2.29, 5.14] detected; COCO −1.05 not detected. (c) Table 2 note and §3.4: 35.1% of InternVL3 `ret` captions on OV-test are zero-shot fallbacks (ΔP_cm = 0 by construction). (d) §6.6/§9.2: on OV-test, τ = 0.10 vs −∞ worsened CHAIR_i, ΔP_cm and CIDEr-D (Table S1). (e) 09:19: a design limitation of the registered estimand, and the stage-A ΔP_cm constraint as the reason τ = 0.10 was chosen. (f) One line on verifier lineage (InternVL3's LM is Qwen2.5; Qwen3-VL is the verifier). | No | Correctness +0.2 |
| 7 | Scope of P2 (object precision) | R2 m1, R3 m2, R5 #3 | 05_preregistration_and_analysis.md:27-33; 06_results.md:45 | Reword "no object-precision cost from retrieved examples" to "relative to zero-shot, from the full in-context prompt". Add a descriptive `ret`−`rand` ΔP_cm row from Table S1 values (labelled post hoc). A *registered* `ret`-vs-`rand` precision test is **[EXP → coordinator]**: a new study on fresh data only. | Text: no. Registered test: yes, deferred | Correctness +0.1 |
| 8 | Single `rand` draw; what the CI conditions on | R5 #1, R2 m2 | 05_preregistration_and_analysis.md:19, :75-77; 03_method.md:22-29; 09_limitations.md:10 | State the estimand: CIs cover image-sampling uncertainty conditional on one seeded `rand` assignment per image, with full-set document frequencies (a standard approximation). Narrow the claims accordingly. Multiple independent `rand` draws are **[EXP → coordinator]**: allowed on dev sets only (dev-explore → dev-confirm), never on a used test set. | Text: no. Multi-draw: yes, deferred | Correctness +0.2 (moves R5) |
| 9 | Contamination and the "training-free" label | R3 M3, R4 M5 | 09_limitations.md:21-29; 08_english_comparison.md Table 21 setting column | Paragraph: what the Qwen2.5-VL and InternVL3 technical reports or model cards disclose about COCO, NoCaps, Open Images or Vietnamese caption data (desk check of public reports; no e-mail in any request). The equal-k `rand` control removes shared contamination but not contamination that interacts with retrieval. Table 21 setting: "no task training in this study; backbone training data undisclosed / may include COCO". | No | Correctness +0.1 |
| 10 | Post-hoc domain-coverage reading | R1 M2/m6, R2 m3, R3 m1b, R4 m2 | 08_english_comparison.md:88-90; 10_conclusion.md:14; 06_results.md:103-105 | Recast heading 08:88 as a question or hypothesis. Acknowledge Qwen's positive out-of-source rows (XM +3.15 [1.50, 4.93]; NoCaps +2.83 [1.69, 3.98]): for Qwen the gain shrinks rather than vanishes. Note the XM high-cosine tertile cuts against the reading. Soften practitioner item 3 to "consider". Remove the "not interpreted further" vs §8.4 contradiction. A memory-swap test is **[EXP → coordinator]**. | No | Correctness +0.1, Contribution +0.1 |
| 11 | Segmentation description | R1 M6 | 08_english_comparison.md:16; 09_limitations.md:22; 03_method.md:93 | State once: CIDEr-D uses RDRSegmenter word tokens (stripped decision column); length is counted in syllables. Change "syllable-segmented" at 08:16 and 09:22 to match. (AC check: 08:16 and 09:22 do say "syllable-segmented"; verify 03:93 before editing.) | No | Correctness +0.1 |
| 12 | Self-contained instruments | R1 m8, R2 M7, R4 m3, R5 m2 | 11_supplement_registered_rows.md (new section); 03_method.md:54-69, :91-97 | Give operational definitions in the supplement: scoring kit and stripping, tone-normalised matcher, count-matched precision P_cm (class list, gold construction from **existing** labels only), and the English class map. Provide anonymised companion manuscripts to the editor. No new labels. | No | Clarity +0.2, Correctness +0.1 |
| 13 | Length and operations-log content | R1 M8, R2 m8/m12, R3 m7, R4 M8/m6, R5 m3 | 07_disclosures.md; 08_english_comparison.md:94-118; 06_results.md §6.8; Tables 12-17; 03_method.md:11 | (a) Main text: one disclosure table (item, effect on data, exposure, verdict changed?) and a one-paragraph deviation summary. (b) Move §7.1-7.3, the 7.7 timestamps, §8.5, the smoke test, worktree/commit hashes, the parity rerun narrative and the "all configurations" material to the supplement. Cut §6.8 to the τ ablation plus one sentence each on k and memory size. (c) Replace internal terms ("sister study", "laptop-side", "decoding machine", "refusal list", "approved by the PI"). (d) Add a glossary table near §5. (e) Consolidate the `rand`−`zs` descriptives into one labelled table. (f) Target about 25 pp. All registered FAIL reports stay in the main text. | No | Clarity +0.5 |
| 14 | Minor bundle | R1 m4/m10-m13, R2 m5/m6/m10/m11, R4 m5/m10, R5 m1/m4 | various; tex/ | KTVIC train 3,469 origin (03:16). Multiplicity sentence (05:78). Cite Tables S10-S11 by number. Memory size: AB-M is dev-only, with no cross-language size claim (01:5). Decode parity "on the same machine and software stack" (09:10). Archive or drop the unversioned log timestamps (07:74). Optional p-values labelled POST HOC (TALLIP), or a one-line CI-only justification. Author placeholder, DOI, acmart warnings, ORCID, and the Nguyen2026FAIR bib entry (NOT_CHECKABLE). Anonymised artifact link or qualified availability statement (10:18-23). Title/abstract signal that English is a frozen-configuration transfer arm. Figure ≥ 600 dpi or vector. | No | Clarity +0.1 |

**Expected after revision (AI opinion):** Novelty 2-2.5, Correctness about 4, Contribution about 3, Clarity about 3.5-4. That would leave a likely minor revision in round 2 at TALLIP. Items 1-5 carry most of the gain; item 13 carries the clarity gain.

## 4. Experiments handed to the coordinator (NOT done in this revision)

Every item below needs a new preregistration under the three-tier method (dev-explore → dev-confirm rehearsal → single test look on a **fresh, never-looked** test set). None may re-score OpenViIC test, XM-test2500, COCO Karpathy test or NoCaps val. No new human gold labels may be created, and AI labels cannot serve as evidence.

| ID | Experiment | Source | Purpose |
|---|---|---|---|
| X1 | Several independent `rand` draws, variance folded into the CI | R5 #1 | Correctness; dev only unless a fresh test set exists |
| X2 | Dev-only masked-n-gram analysis of the gain (OV-dev-B) | R3 m4 | Construct validity; descriptive, labelled |
| X3 | Registered `ret`-vs-`rand` object-precision test | R5 #3 | P2 scope |
| X4 | 3-5 backbones across families and sizes; a deletion-free arm or deletion as a factor | R2 Q1, R4 M7 | Q1 path; backbone as a moderator |
| X5 | Memory-swap on fixed images (domain-coverage hypothesis) | R2 Q1, R4 M7 | Q1 path; tests the §8.4 reading |

## 5. Binding-rule compliance of this plan

- No new human gold labels. AI labels are never used as evidence.
- No test-set re-look. Items 5-7 use numbers already in the decision files and ledgers, labelled post hoc where not registered.
- Registered FAILs (XM-a, S-NC) stay reported in the abstract, results, limitations and conclusion. The PASS headline is kept.
- No "first" claim. New prior art is added before any novelty wording.
- No OpenViIC, KTVIC or UIT-ViIC caption text goes into any file.
- No personal e-mail in any web request; use vsps-research@example.org or none. No commits, no GPU.
