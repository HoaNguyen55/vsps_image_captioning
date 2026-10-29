# Paper A meta-review (Area Chair, Signal Processing: Image Communication)

All judgements in this file are AI opinion (generated area chair and reviewers), not human peer review. Written 2026-10-29. No edits, commits or GPU use were made for this review.

## Tóm tắt cho PI (tiếng Việt)

- **Quyết định (ý kiến AI): Major revision.** Cả 5 reviewer (R1 tổng quát, R2 phương pháp/thống kê, R3 chuyên gia metric, R4 biên tập viên, R5 Codex bên ngoài) đều đề nghị major revision. Không ai đề nghị reject.
- **Điểm đồng thuận (1–5):** novelty 3, correctness 3 (R4 cho 4), contribution 3, clarity 2 (R2 cho 2.5). Các con số đều khớp với file decide/prereg; thứ tự đăng ký trước khi chạy được xác nhận (commit 353437f 00:49:49Z trước khi chạy 00:51:22Z).
- **Vấn đề chính, đều sửa được bằng văn bản:**
  1. Phần Limitations (sec11:9) vẫn ghi phép thử PASCAL-50S "registered, not run", trong khi nó đã chạy và primary P50-A4 FAIL (−2.29 [−5.15, +0.61]). Đây là lỗi mâu thuẫn nặng nhất; cả 5 reviewer đều nêu.
  2. Abstract đặt hai kết quả PASS phụ (O2, X4) lên trước kết quả FAIL chính của PASCAL. Được giữ PASS làm headline, nhưng phải nêu ngắn gọn FAIL chính trong cùng câu, kèm con số.
  3. Phần thứ tự giữa các mức reference gần như đúng "theo cấu trúc" (sec4:25). Phần có rủi ro thật là "label gold > mọi reference": PASS trên XM3600 chỉ dưới verified precision, yếu trên backbone thứ hai, và FAIL trên PASCAL-50S. Cần nói rõ điều này ở §1, §9.1 và abstract; nên cân nhắc đổi tiêu đề.
  4. Tiền đề "nhãn VOC đầy đủ hơn 50 reference" chưa được kiểm; cần nêu đây là một cách đọc khác của FAIL.
  5. Kết quả PASCAL phụ thuộc vào 14 run, chia thành hai cụm ngắn/chi tiết. Hai model LLaVA có slope âm. Không thể làm kiểm định leave-one-out vì output đã xóa; phải nêu thành giới hạn.
  6. Hai sai lệch so với prereg chưa được công bố: không giữ hash file caption (PREREG §6), và đã kiểm tra cấu trúc pascal50S.json trên laptop trước khi commit.
  7. **Mâu thuẫn về giấy phép (Codex, đã kiểm lại):** declarations.md:19 viết tác giả UIT-OpenViIC/KTVIC "confirmed this use in writing", nhưng comment ở sec11:25 và chính declarations.md cho thấy xác nhận *chưa* nhận được. **PI cần xác nhận tình trạng thực tế.** Khuyến nghị mặc định: sửa thành "đã gửi yêu cầu, chưa có trả lời; chỉ dùng số liệu tổng hợp".
  8. Thiếu tài liệu liên quan trực tiếp: Feng et al. 2024 (arXiv 2406.12663), Misra et al. 2016, Spain & Perona 2010, Berg et al. 2012.
  9. Độ rõ ràng: bài khoảng 13k từ, ledger 40 dòng nằm trong phần Introduction, nhiều mã nội bộ (cv295, xm600, P50-A4…), hai file supplement trùng nhau.
- **Thí nghiệm mới:** không cần cho bản revise này. Có 2 mục tùy chọn được chuyển cho coordinator (mục 5b và 9b bên dưới); cả hai đều post hoc, không có verdict, và không phải lần nhìn thứ hai vào output.
- **Ước tính sau khi sửa (ý kiến AI):** novelty 3→3.5, correctness 3→4, contribution 3→3.5, clarity 2→3.5. Dự kiến minor revision ở vòng sau.
- **Cần PI quyết:** (a) tình trạng giấy phép OpenViIC/KTVIC (mục 2); (b) có đổi tiêu đề không (mục 4; mặc định: đổi); (c) có chuyển §6 và §8.3–8.4 sang supplement không (mục 12; mặc định: có).

## Panel

| ID | Role | File | Nov | Cor | Con | Cla | Rec | Conf |
|----|------|------|-----|-----|-----|-----|-----|------|
| R1 | Senior area expert | A_R1_area.md | 3 | 3 | 3 | 2 | major | 4 |
| R2 | Methods and statistics | A_R2_methods.md | 3 | 3 | 3 | 2.5 | major | 4 |
| R3 | Evaluation-metrics specialist | A_R3_metrics.md | 3 | 3 | 3 | 2 | major | 4 |
| R4 | Handling editor | A_R4_editor.md | 3 | 4 | 3 | 2 | major | 4 |
| R5 | External reviewer (Codex) | A_codex_review.md | 3 | 3 | 3 | 2 | major | n/a |

## Consensus scores (AI opinion)

| Criterion | Consensus | Spread | Disagreement |
|-----------|-----------|--------|--------------|
| Novelty | **3** | 3–3 | None. All five reviewers find the framing (gold as an experimental factor; a size-matched random-deletion null) useful but incremental over Rohrbach 2018, IR pool bias, ImageNet ReaL/RePOPE and length-control work. R2, R4 and R5 add Feng et al. 2024; R1 and R3 add the reporting-bias and object-importance literature. |
| Correctness | **3** | 3–4 | R4 gives 4: the numbers are right, verdicts are copied rather than re-judged, and weaknesses are conceded. R1, R2, R3 and R5 give 3 because of stale or contradictory text, undisclosed deviations, an unmeasured A4 premise, unstated system conditioning, and (R5) the permission conflict and the micro- vs mixed-F1 mismatch. Nobody found an arithmetic error. |
| Contribution | **3** | 3–3 | None. The practical message (report gold, matcher and M) is useful. The confirmatory base is narrow (one Qwen family, 600 images, PASCAL primary failed), and the count-control line is not confirmatory. R4 and R5 question SPIC fit and the validation of the reporting proposal. |
| Clarity | **2** | 2–2.5 | Minor. R2 gives 2.5 for auditability. Everyone else finds the main text overloaded: ledger, internal IDs, two supplements, stub files, numbering mismatch. |

**Decision: MAJOR REVISION** (unanimous, AI opinion). Every required change is textual, a disclosure, a citation, a re-plot of existing decided values, or a restructuring. No new labels, no second look and no GPU work are required.

**Answers to the two questions put to the panel**

- *Is X4 acceptable in the abstract?* Yes (5/5). It was registered before output, it passed, and it is the only registered test that separates salience-driven missingness from random missingness (sec4:25). Three conditions apply: make the referent precise, label the test consistently, and do not let it stand in front of the failed primary.
- *Is the A4 FAIL reported adequately?* In the body, yes: §7.4 carries the verbatim branch text, plus Table 1 A24, §9.1, §9.5 and the cover letter. It is **not** adequate in Limitations (contradicted there), in contribution 1, or in the highlights, and it is borderline in the abstract.

## Prioritised revision plan

Legend. **Exp**: "no" means text only. "FLAG" means it needs a computation or a new experiment, which is NOT done in this revision and goes to the coordinator. **Gain**: estimated score change from this item, AI opinion. Paths are relative to `manuscript/journal_draft/`.

### Tier 1: blocking (contradictions and integrity)

1. **Limitations contradict the PASCAL-50S result.** Raised by R1 M5, R2 M1/M2, R3 M1, R4 M1, R5 M1.
   - Files: `sec11_limitations_ethics.md` l.9, 19, 21, 23.
   - l.9: replace "the large-reference-set test is registered, not run (Section 7.4)" with "the registered PASCAL-50S replication was run once (Section 7.4); its primary prediction failed at the label-gold step (50 references vs VOC labels: −2.29 [−5.15, +0.61]), so the ordering claim rests on XM3600 and its second backbone."
   - l.21: after "which passed on both backbones" add "and failed its label-gold step on PASCAL-50S".
   - l.19: add PASCAL-50S (public since 2008–2015) to exposure.
   - l.23: add the seven-LVLM English PASCAL family to external validity.
   - Exp: no. Gain: correctness +0.5.

2. **Conflicting permission statements.** Raised by R5 M4; verified by the AC.
   - Files: `declarations.md` l.19, `sec11_limitations_ethics.md` l.25, `cover_letter_A.md` (if it mentions this).
   - The visible text of declarations.md says the UIT-OpenViIC and KTVIC authors "confirmed this use in writing". Its own comment says to update to "obtained" only if the reply arrives, and sec11:25's comment says the confirmation was not obtained.
   - Change: write the true status. **PI must confirm.** Default (recommended): "Written permission was requested from the UIT-OpenViIC and KTVIC authors; at submission no reply had been received, so only aggregates and pointers are used." Check the PASCAL-50S "confirmation obtained 2026-10-28" claim against the file on record in the same way.
   - Exp: no. Gain: correctness +0.25 (integrity; a desk-reject risk if left).

3. **Visible placeholders.** Raised by R1 m11, R3 m7, R4 M2, R5 minor 5.
   - Files: `sec11_limitations_ethics.md` l.33 ("[AUTHOR TO CONFIRM: Polaris BSD; DOCCI-Critique CC BY 4.0]"), the reviewer-link placeholder in `declarations.md`, address placeholders in `title_page_A.md` and `cover_letter_A.md`.
   - Change: confirm the licences from their primary release pages, or write "licence unverified; only aggregates reported". PI admin items are low priority, but they must be resolved before submission.
   - Exp: no. Gain: none on scores; blocks submission.

### Tier 2: claim calibration (largest score gain)

4. **Abstract, contribution 1, highlights, intro and cover letter: state the PASCAL primary FAIL and scope the claim.** Raised by R1 M1/m8/m14, R2 M2/M8, R3 M3/m10, R4 M3/m1/m6, R5 M1.
   - Files: `abstract_A.md` l.9; `sec1_introduction.md` l.9, l.27, Table 1 row A24 (l.67–69); `highlights_A.md` l.5; `cover_letter_A.md` l.10.
   - Abstract (≤240 words; it is 244 now): "On PASCAL-50S (seven public LVLMs), the registered primary replication failed at its label-gold step (50 references vs VOC labels: −2.29 [−5.15, +0.61]); the slope rose at every registered reference rung from one to 50 (registered secondary), and in a registered companion test one- and five-reference gold gave a lower slope than size-matched random deletions from the 50-reference consensus." Then:
     - replace "Registered failures are reported in full:" with "Nine registered predictions failed (Table 1), including …";
     - scope the opening claim to "on XM3600 and its second backbone";
     - add "conditional on the systems scored" to the interval statement;
     - drop the PASCAL item from the later failure list to save words.
   - Contribution 1: name P50-A4 as the failed primary in the same sentence as the O2 PASS.
   - Table 1 A24: add −2.29 [−5.15, +0.61]; mark A24a and A24b as secondary/companion in the Verdict column.
   - Highlight 1: "on XM3600 with two backbones, not at PASCAL-50S's label-gold step".
   - Cover letter: same balance as the abstract.
   - Keep a PASS headline (allowed).
   - Exp: no. Gain: correctness +0.25, contribution +0.25 (credibility).

5. **Separate the expected-by-construction part from the risky part, and name the untested A4 premise.** Raised by R1 M2/M4, R2 M5, R3 M2/M4, R4 M4d, R5 M1/M5.
   - Files: `sec1_introduction.md` l.9/27; `sec10_discussion.md` l.7 (§9.1); `sec7_verbosity_sign.md` l.99 (§7.4); `sec11_limitations_ethics.md` (§10.1); title in `title_page_A.md`, `abstract_A.md`, `cover_letter_A.md`, `outline.md` l.24.
   - (a) Text, in §9.1 and §1: the reference rungs are ordered even under SCAR (sec4:25), so O2 and A4 part 1 are low-risk. Tally the non-nested label-gold step honestly:
     - XM3600: PASS under verified precision;
     - second backbone: PASS, but the post hoc bracket lower bound is +1.97 [−0.44, +4.01];
     - PASCAL-50S: FAIL.
   - (b) In §7.4 l.99 and §10.1, add one sentence: "The completeness order of the VOC labels versus a 50-reference gold on the 20 VOC classes was assumed, not measured. The V20 50-reference slope (+9.74 [+7.29, +12.12]) already exceeds the VOC-label slope (+7.45 [+4.98, +9.94]), so the FAIL may reflect a label rung that is not more complete, rather than a more complete gold without a larger slope. This was not tested." Add, descriptively, that two of seven models (both LLaVA) have negative per-model VOC-label slopes (PAIR_m).
   - (c) Title: stop stating the near-mechanical part as the finding. Suggested (AI opinion): "Gold Completeness and the Verbosity Slope of Object Hallucination Metrics: A Registered Audit". **PI decision; default = change.** Record the choice in outline.md.
   - **(5b) FLAG, coordinator only:** output-free gold sizes per rung on V20 (Σ|refs50∩V20| vs Σ|voc20| = 1,782, plus the set differences). They need no model outputs, but they need the PASCAL-50S references re-staged, which the registered data rule may forbid. They would be post hoc with no verdict. If not run, state "not retained".
   - Exp: (a)–(c) no; 5b FLAG. Gain: correctness +0.25, novelty +0.25 (an honest synthesis makes X4 the clear informative result).

6. **System dependence and auditability of PASCAL-50S.** Raised by R1 M3/M6, R2 M3/M6, R3 M6/m9, R4 M5, R5 M3.
   - Files: `sec7_verbosity_sign.md` l.88–99; `sec11_limitations_ethics.md` l.21, l.34; `sec10_discussion.md` §10.1 statement on the short-vs-detailed contrast; `supplementary.md` S4 and the PAIR_m note at l.620–631.
   - In §7.4, state:
     - the intervals hold the 14 runs fixed (7 models × short/detailed);
     - V20 M forms two clusters (short ≈1.12–1.35, detailed ≈1.6–2.24), so the slope is in effect a short-vs-detailed contrast, as in every registered family;
     - the per-model voc20 slope runs from −1.05 to +14.75 (negative for LLaVA-1.5 and LLaVA-OV);
     - whether detailed captions hit the 160-token cap: report it if it is stored, else write "not recorded";
     - no system-level interval exists, and none can be computed, because the 14 caption files were deleted under the registered 8-gram rule. The decide files, EVENTS, evaluator hashes and job are in the deposit.
   - PAIR_m table: note that the COCO-80 and V20 columns are different vocabularies and each entry is a two-run contrast.
   - Do NOT request a PASCAL leave-one-out, matcher fix or per-model V20 ladder: that would be a second look, and the outputs are gone.
   - Exp: no. Gain: correctness +0.25.

7. **Undisclosed departures from the registration.** Raised by R1 M6, R2 M3/M4/m12, R3 m5/m9.
   - Files: `sec7_verbosity_sign.md` §7.4 (l.88, 97); `supplementary.md` S4 deviation list; `sec11_limitations_ethics.md` l.34; `declarations.md` l.19 (data-availability sentence).
   - (a) Label "no hash of the caption files was kept" as a departure from PREREG §6 ("only its sha256 and the aggregates leave"). p50_job.sh copied the .sha256 only on rc = 0, and all 14 files had hits.
   - (b) Disclose the off-protocol laptop refcheck of the pascal50S.json structure before the commit (PREREG §0 l.35, RULE §0; accepted under CC-159 ruling 6; no change of verdict).
   - (c) Report the per-file 8-gram hit counts (18–419; already in `data/results/p50/ngram_p50_*.preds.json`, aggregates only, no caption text). Add one sentence on what they do and do not imply: generic phrases vs possible memorisation; PREREG §6 says "a hit is not a verdict input". Use this to support "may be in the pretraining data" at sec7:97.
   - Exp: no. Gain: correctness +0.25.

8. **Tidy X4 and X5.** Raised by R1 m2–m5, R2 M7/m6/m13, R3 m1–m3, R4 M4/m3/m9.
   - Files: `sec7_verbosity_sign.md` l.88, 129–141; `sec1_introduction.md` l.69; `abstract_A.md`; `sec10_discussion.md` l.7; `sec3_measurement_setup.md` §3.6.
   - Label: "co-primary in its registered companion family {X4, X5}; secondary to the paper's confirmatory claim (CC-159 placement)". Use it everywhere.
   - "On 1,000 PASCAL-50S images" → "on the 997-image analysis set (of 1,000)".
   - p = 0.001 → "p ≤ 0.001 (the floor at R = 1,000; the null holds images and runs fixed, so p describes gold randomisation, not sampling of images or systems)".
   - Drop "Holm-corrected" for a one-member family. State that no adjustment applied, and cite the descriptive family-wise Holm reading (supplementary.md:633: 0.939 / 0.001 / 0.001), including 0.939 for P50-A4 in the main text.
   - Say once that the direction was anticipated (8/8 exploratory cells, 4/4 dev cells at p = 0.001; RULE §3.2, §9).
   - Link X4 to the b-channel of §4.2 ("consistent with"); it is the only registered test that probes non-SCAR missingness.
   - X5: delete "so the null could barely move" (that is a rationale, not an observation). State only that the evaluability condition Σ|voc20| ≥ 2Σk failed (1,782 < 2,079.2), and call the 1,782 "image–class pairs". Say once that X5's observed value was printed but carries no result, and keep it out of the paper.
   - "before the first output (00:51Z)" → "before the run started (00:51:22Z)".
   - §3.6: name the families where Holm applies.
   - Exp: no. Gain: correctness +0.25, clarity +0.1.

9. **Dependence on the verified-precision estimand.** Raised by R5 M5, R1 M2, R3 M2.
   - Files: `sec3_measurement_setup.md` l.13; `sec7_verbosity_sign.md` l.7, 16–17, 45–52; `abstract_A.md`; `sec10_discussion.md` (conclusion).
   - (a) Justify verified precision as the preferred estimand: OIV7 verifies presence or absence only for its labelled classes.
   - (b) State in the abstract and conclusion the narrower result under the alternative rule: under "unverifiable = error" the second-backbone label-gold interval includes 0. The bracket already exists in supplementary_SPIC.md:402–406.
   - **(9b) FLAG, coordinator:** quantify how many mentions verified precision excludes per system. Report it if `data/results/n_f1/bracket_result.json` already stores the count; otherwise computing it is a post hoc descriptive pass over XM3600 outputs (no verdict), which needs a coordinator ruling under the one-look rule.
   - Exp: (a)/(b) no; 9b FLAG. Gain: correctness +0.25.

10. **Theory vs the primary outcome (micro- vs mixed-F1).** Raised by R5 M2 and minor 3.
    - Files: `sec4_theory.md` l.8–23; `sec7_verbosity_sign.md` l.5–7; `supplementary_SPIC.md` l.30–34; table and figure captions.
    - Proposition 1 already says the closed form is applied only to micro-F1. Still needed:
      - present it explicitly as a micro-F1 result that motivates, but does not derive, the empirical mixed-F1 ordering;
      - state in every table and figure caption whether it uses mixed or micro F1;
      - resolve the clash between sec7 ("rows report mixed F1") and the supplement ("both variants").
    - Exp: no. Gain: correctness +0.1, clarity +0.1.

### Tier 3: positioning and novelty

11. **Missing prior art.** Raised by R1 m9, R2 M9, R3 M5, R4 M6, R5 minor 1.
    - Files: `sec2_related_work.md` l.6, 10–14, 34 and Table 2.1; `sec4_theory.md` §4.1; `sec7_verbosity_sign.md` l.139–141; `paperA.bib`.
    - Add, each after reading the paper:
      - Feng et al. 2024, arXiv 2406.12663, the closest prior critique;
      - Misra et al. 2016, CVPR, doi 10.1109/CVPR.2016.320 (reporting bias, for X4 and A2);
      - Spain & Perona 2010, IJCV, doi 10.1007/s11263-010-0376-0 (object importance ≈ π in §4.1);
      - Berg et al. 2012, CVPR, doi 10.1109/cvpr.2012.6248100;
      - Rohrbach et al. 2018's own one-annotation-source finding;
      - Amirloo et al. 2024, arXiv 2407.02477 (CHAIR–recall trade-off);
      - Vedantam et al. 2015's more-references-raise-agreement finding.
    - Optional, after reading: Dai et al. 2023 (EACL), Biten et al. 2022 (WACV), Lovenia et al. 2024 (NOPE), Chen et al. 2026 (arXiv 2605.25036; verify that it exists and what it says first).
    - Positioning sentence for sec2:34: prior work knows that incomplete gold inflates hallucination. This paper adds gold completeness as a controlled factor that can set the sign of F1's verbosity reward, plus a size-matched deletion null that quantifies a known reporting bias. In §2, replace broad "no prior work" statements with the searched scope.
    - Keep the no-"first" wording. Literature lookups use vsps-research@example.org or no e-mail. The panel's search was partial: OpenAlex and S2 were rate-limited.
    - Exp: no. Gain: novelty +0.25 (sharper demarcation), contribution +0.1.

### Tier 4: clarity and fit (largest clarity gain)

12. **Restructure for an SPIC reader.** Raised by R1 M7, R2 m4/m10/m11, R3 M7/m11, R4 M7/m7, R5 minor 2.
    - Files: `sec1_introduction.md` l.36–76; all `sec*.md`; `supplementary.md` and `supplementary_SPIC.md`; `sec9_preference_audit.md` and `appB_matcher_sensitivity.md` (stubs); `outline.md`; `figs/`.
    - (a) Replace the 40-row ledger in §1 with a five-line summary (confirmatory / secondary / failed). Move the full ledger to the supplement, with plain-language test names and registry IDs in a column.
    - (b) Replace set codes (cv295, uv231, xm600, s75, "rung", "family ALL") with descriptive names. Replace the raw evaluator token "PASS_DRHO113_MIXED_MCP_CI_INCLUDES_1" (sec1:47) with a verdict word. Move governance IDs (CC-, PI-, W-) to the provenance file.
    - (c) Submit one supplement. Recommended: supplementary_SPIC.md, after merging S4 and S7 from supplementary.md.
    - (d) Remove the two stub files from the build. Align the section numbers with the file names, or keep a map in outline.md, and check every "Section N" cross-reference.
    - (e) Define "verbosity reward" once as the signed slope, since it is mostly negative under reference gold, or use "verbosity slope" (ties to item 5c).
    - (f) Move §6 (re-scoring published methods) and §8.3–8.4 to the supplement so the paper centres on RQ1. **PI decision; default = move.**
    - (g) Add one Introduction paragraph tying the result to the reference-set dependence of quality measures (SPIC fit; González-Chávez et al. 2024 in SPIC). Also bring §9.4's argument forward.
    - Exp: no. Gain: clarity +1.0.

13. **Figures from existing decided values (no GPU, no new look).** Raised by R1 m6, R3 M7, R4 m2.
    - Files: `figs/fig2_slope_by_gold.svg`, `figs/VALUES.json`, `figs/CAPTIONS.md` l.5; `sec7_verbosity_sign.md` Table 7.1.
    - Add a PASCAL-50S panel: the k = 1→50 ladder plus the VOC-label point with its failed comparison marked, copied from P50-NS in p50_decide.json.
    - Fix the stale cross-references (7.6→7.3, 7.5→7.2).
    - Add the planned Fig. 1 schematic of the gold ladder (outline.md:99).
    - Exp: no (a re-plot of decided numbers). Gain: clarity +0.25.

### Tier 5: minor consistency (batch edit)

14. Raised by R1 m7/m12/m13, R2 m2/m3/m9, R3 m6/m12, R4 m5/m8/m10.
    - `sec3_measurement_setup.md` l.9: add the PASCAL-50S exception to "at most the first five references".
    - `sec3_measurement_setup.md` l.47 and §7.4: state B for each test (B = 1,000 for PASCAL vs 5,000 default).
    - "rise at every added reference" → "at every registered rung (k = 1, 2, 5, 10, 20, 50)". Locations: abstract, sec1:9/27, sec7:94.
    - §7.4: state once that part 2's interval includes 0, so the FAIL means the direction was not shown, not that the reverse was shown.
    - `sec4_theory.md` l.23: note that on PASCAL COCO-80 the slope stays ≤ 0 up to k = 50 (−0.83 [−2.58, +1.07]), while V20 changes sign between k = 10 and 50 (an unpredicted crossing location).
    - `sec7_verbosity_sign.md` l.131: "50 references as the complete gold" → "50-reference consensus".
    - `sec7_verbosity_sign.md` l.88: state that whether the 5 UIUC captions are among the 50 references is unknown, and that no adjacency/exchangeability check was registered for PASCAL-50S.
    - `sec1_introduction.md` l.9: next to "Nine registered predictions failed", add the expected number of false PASSes under the global null. This is arithmetic on the count of registered rows, not new data.
    - Title consistency across `title_page_A.md`, `abstract_A.md`, `cover_letter_A.md` and `outline.md` l.24.
    - Exp: no. Gain: clarity +0.15, correctness +0.1.

15. **Reproducibility package statement.** Raised by R5 M3, R1 M6.
    - File: `declarations.md` l.19.
    - Add one sentence listing what a reviewer can check independently: the scoring code, decide files with hashes, prereg commit times and the numbers manifest. Also list what cannot be checked: PASCAL per-image outputs and restricted rows.
    - Any change to the deposit contents (for example per-image sufficient statistics where licences permit) is a PI/coordinator decision, not part of this text revision.
    - Exp: no (deposit changes go to the coordinator). Gain: correctness +0.1.

## Items deliberately NOT requested

- No re-analysis of PASCAL-50S outputs (leave-one-model-out, matcher fix, per-model V20 ladder). That would be a second look, and the outputs were deleted.
- No new human labels. AI-generated labels are not evidence.
- No confirmatory count-control run (R5 contribution point). That is a future registered study, for the coordinator.

## Expected scores after revision (AI opinion)

| Criterion | Now | After Tiers 1–5 | Main driver |
|-----------|-----|-----------------|-------------|
| Novelty | 3 | 3.5 | items 5, 8, 11 (X4 as the informative result; sharper positioning) |
| Correctness | 3 | 4 | items 1, 2, 4–9 |
| Contribution | 3 | 3.5 | items 4, 11, 12g (credible scope; SPIC fit) |
| Clarity | 2 | 3.5 | items 12, 13, 14 |

Expected outcome at the next round, if Tiers 1–4 are done: minor revision (AI opinion). Order of work: items 1–3 → 4–9 → 10–11 → 12–15. Items 5b and 9b, and any deposit change, go to the coordinator.
