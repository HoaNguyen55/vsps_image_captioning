# Paper B+D meta-review (Area Chair, Language Resources and Evaluation)

All judgements in this file are AI opinion (a generated area chair and generated reviewers), not human peer review. Written 2026-10-29. No manuscript edits, commits or GPU use were made for this review.

## Tóm tắt cho PI (tiếng Việt)

- **Quyết định (ý kiến AI): Major revision.** Cả 5 reviewer (R1 chuyên gia lĩnh vực, R2 phương pháp/thống kê, R3 chuyên gia metric, R4 biên tập viên, R5 Codex bên ngoài) đều đề nghị major revision. Không ai đề nghị reject.
- **Điểm đồng thuận (1–5):** novelty 3, correctness 3 (R1 cho 4), contribution 3, clarity 2.5 (R2 và R4 cho 2, R1 và R3 cho 3, Codex cho 4). Mọi con số của B-1, D0, B-R1 đều khớp với file decide, hash khớp. Rule được ghi trước khi chạy. FAIL của bài kiểm tra cuối vẫn được báo cáo ở §1 và §5.1. Không có câu nào nói gain từ OpenViIC chuyển sang KTVIC.
- **Vấn đề chính, phần lớn sửa được bằng văn bản:**
  1. **Câu headline trong abstract bị nói quá** (cả 5 reviewer nêu). Câu "Training-data gains thus register mainly on the panel whose captions were used for training" áp cho cả hai chiều. Thực tế chỉ chiều thuận (train trên KTVIC) chứng minh được điều đó. Ở chiều ngược, g_R = +1.69 [−0.72, 3.91], CI chứa 0. Cách viết "no measurable gain on KTVIC references" (sec8:5, cover letter:14) biến "không có bằng chứng" thành "bằng chứng là không có". Phải giới hạn câu này vào chiều thuận.
  2. **Mức bằng chứng thấp hơn mức của tiêu đề.** Toàn bộ là dữ liệu dev: 187 ảnh, một backbone, chiều ngược chỉ 2 seed. Phía KTVIC của D0 đã biết trước từ B-1. B-1 là bản xác nhận của một kết quả single-seed (+9.40). Tập test KTVIC đã đóng nên không xác nhận được trong bài này. Cần ghi "development data" vào tiêu đề hoặc phụ đề, và ghi rõ điều này ở abstract, §1, §7.1.
  3. **CI chỉ tính việc lấy mẫu ảnh, không tính phương sai giữa seed.** Theo cách tính sơ bộ của R3, chiều ngược có gap theo từng seed là +3.53 và −0.14. Cần báo cáo slope theo từng seed (CPU, post hoc, mô tả). Việc này chuyển cho coordinator.
  4. **Bài đọc như hai bài báo ghép lại.** Tiêu đề dẫn bằng training-data gains, còn §1:9 và danh sách đóng góp dẫn bằng protocol card và kit. **PI cần chọn một trục chính** (xem mục 4).
  5. **Thiếu tài liệu liên quan.** Multi30K, COCO-CN, van Miltenburg 2017, Frank 2018, Yi 2020, Freitag 2020, Chen 2017, Kornblith 2023, Dessì 2023, Miller 2021 (Accuracy on the Line), Taori 2020. Cần nêu phần mới một cách hẹp: "đường cong theo kích thước tập train, hai panel người viết, cả hai chiều, trong tiếng Việt". Không claim "first".
  6. **"first reported" cho Tran et al. (2026)** xuất hiện ở 4 chỗ (đã grep kiểm tra). Phải đổi thành "reported". R3 nói không có claim này; R3 sai.
  7. **§5.1 chưa liệt kê đủ các lần nhìn test KTVIC liên quan MBR.** R4 đã kiểm: prereg B-F1 ghi một lần nhìn thăm dò +3.05 trước khi đăng ký (L4). Cần một câu liệt kê cả ba lần nhìn. FAIL vẫn giữ nguyên.
  8. **Nhiều câu cụ thể cần sửa:** "more than half" (CI_lo 49.38%), "nearly vanishes", "reliably improves", câu đã cũ ở sec4:20 và sec3:66, tham chiếu chéo sai, năm trích dẫn Bui 2023/2026 không thống nhất, chữ "validated", mã nội bộ (D0, O5b, P1 SESOI).
- **Thí nghiệm mới:** bản revise này không cần GPU, nhãn mới hay lần nhìn test mới. Có **3 mục phân tích lại bằng CPU** chuyển cho coordinator (mục 3, 9b, 11b). Cả ba đều post hoc, mô tả, chỉ trên dev, không có verdict.
- **Ước tính sau khi sửa (ý kiến AI):** novelty 3→3.5, correctness 3→4, contribution 3→3.5, clarity 2.5→3.5. Dự kiến minor revision ở vòng sau.
- **Cần PI quyết (kèm khuyến nghị mặc định):**
  (a) Trục chính của bài (mục 4). Mặc định: giữ tiêu đề training-gain, thêm "on development data", và đưa §5.4–5.5 lên ngay sau phần dữ liệu.
  (b) Giấy phép dữ liệu (mục 15). cover_letter:27 ghi tác giả KTVIC/OpenViIC "confirmed in writing (2026-10-28)", nhưng outline:72 vẫn ghi [AUTHOR TO PROVIDE]. Mặc định: nếu xác nhận là thật thì cập nhật outline/STATUS; nếu không thì sửa cover letter.
  (c) Zenodo DOI và ORCID (mục 15). Thuộc nhóm việc hành chính ưu tiên thấp, nhưng Codex coi kit chưa có DOI là chặn chấp nhận.

## Panel

| ID | Role | File | Nov | Cor | Con | Cla | Rec | Conf |
|----|------|------|-----|-----|-----|-----|-----|------|
| R1 | Senior area expert | BD_R1_area.md | 3 | 4 | 3 | 3 | major | 4 |
| R2 | Methods and statistics | BD_R2_methods.md | 3 | 3 | 3 | 2 | major | 4 |
| R3 | Evaluation-metrics specialist | BD_R3_metrics.md | 3 | 3 | 3 | 3 | major | 4 |
| R4 | Handling editor | BD_R4_editor.md | 3 | 3 | 3 | 2 | major | 4 |
| R5 | External reviewer (Codex) | BD_codex_review.md | 3 | 3 | 3 | 4 | major | n/a |

## Consensus scores (AI opinion)

| Criterion | Consensus | Spread | Disagreement |
|-----------|-----------|--------|--------------|
| Novelty | **3** | 3–3 | None on the score. The reviewers cite different missing prior art: R1 (same-image multi-panel sets: Multi30K, COCO-CN, van Miltenburg, Frank, Yi), R2 (ID/OOD scaling: Miller 2021, Taori 2020), R3 (reference style drives scores: Freitag 2020, Kornblith 2023) and R4 (cross-domain captioning: Chen 2017, Dessì 2023). All agree that the new part is the training-size slope against two human panels in both directions, and that the audit items are useful but incremental. |
| Correctness | **3** | 3–4 | R1 gives 4: the numbers are exact and the problems are wording. R2–R5 give 3 for inference errors: the reverse direction is generalised, a null is read as absence, seed variance is missing from the CIs, D0's KTVIC side was partly known in advance, and (R5) the panel effect is not causally identified. No arithmetic error was found by anyone. R3 wrongly states that no unverified 'first' claim exists. The AC checked and found four, so that point stands against the manuscript. |
| Contribution | **3** | 3–3 | None. The audit, protocol card and kit fit LRE well. The two-panel result is a useful warning, but it rests on development data from one backbone and has no held-out confirmation. R5 adds that the kit is not yet citable (the Zenodo DOI is a placeholder). |
| Clarity | **2.5** | 2–4 | This is the largest disagreement. R5 (4) reads the paper as clear and careful. R2 and R4 (2) find that the merge produced two spines, §5.4–5.5 put about 40 CIs into prose with no table, and internal codes leak into the text. R1 and R3 (3) are in between. The AC sides with the majority: the structural problem is real, but it can be fixed. |

## Decision (AI opinion)

**Major revision.** The empirical core is sound and unusually well documented: every main-text number traces to a hash-pinned decided file, and the registered FAIL is still reported. The revision is mostly scoping, framing and positioning, plus three optional CPU-only descriptive re-analyses. None of the requested changes needs new labels, GPU time or another test look.

## Binding rules for the revise step

- No new human gold labels. AI-generated labels are not evidence.
- One look per test set. KTVIC test is closed for Paper B after B-F1. Any confirmation of the two-panel finding is future work: a newly registered single look on data no adapter has been tuned or read on, after the dev-explore and dev-confirm rehearsal stages.
- Registered verdicts stay unchanged and are reported: B-1 PASS, D-α INCONCLUSIVE, D0 GO, B-R1 ASYMMETRIC, final-system test FAIL (−0.39 [−2.44, +1.67]). The FAIL stays in §1 and §5.1. A PASS headline in the abstract is fine.
- No 'first' claims without verified prior art, for us or for others.
- No caption text from OpenViIC, KTVIC or UIT-ViIC in repo files.
- Never put a personal e-mail in a web request. Use vsps-research@example.org or none.
- No commits and no GPU. Any new row is labelled POST_HOC / DESCRIPTIVE / DEV and carries no verdict.
- New references are added only after the writer verifies each DOI or arXiv ID. The reviewers' DOIs are leads, not verified bib entries; R3 did not re-verify Multi30K.

## Prioritised revision plan

Score gains are AI estimates of the effect on the consensus score once the item is done well. "EXP→coordinator" marks work that needs a computation; it is not done in this revision.

### 1. Scope the two-panel headline to the forward direction

- **Raised by:** R1 M1, R2 M1, R3 M1, R4 M1, R5 #1.
- **Files:** outline_B.md:8 (abstract), sec1_intro.md:16, sec6_discussion.md:21, sec8_conclusion.md:5, cover_letter_B.md:14.
- **Change:**
  - Replace "Training-data gains thus register mainly on the panel whose captions were used for training" with "Gains from more KTVIC training captions register mainly on KTVIC's own references (gap +9.87 [6.71, 13.35])."
  - Add the reverse result in one clause: "trained on OpenViIC captions, adapters gain +2.98 [0.94, 4.88] on that panel; the reverse own-minus-other gap, +1.69 [−0.72, 3.91], is not distinguishable from zero."
  - Delete "thus".
  - Present ASYMMETRIC as the registered rule defines it (an approximate-equivalence reading of the reverse direction). Do not present it as support for symmetry.
  - Following R5, word everything as panel-specific score associations, not as a writer mechanism.
- **New experiment:** No.
- **Estimated gain:** correctness +0.5.

### 2. Remove the negative transfer claim

- **Raised by:** R1 M2, R2 M1(c,d), R3 M2, R4 M2.
- **Files:** sec8_conclusion.md:5, cover_letter_B.md:14, sec1_intro.md:16, sec6_discussion.md:21.
- **Change:**
  - Replace "shows no measurable gain on KTVIC references" with "their gain against KTVIC references, +1.29 [−1.23, 3.75], is not distinguishable from zero, nor from the own-panel slope; whether it reaches KTVIC references is not established." This is the wording §5.5 (sec5_results.md:78–80) already uses.
  - Wherever b_K^R is interpreted, quote the σ=∞ value beside it: +2.47 [−0.19, 5.19].
  - Note that the pre-run MDE80 for this slope (5.77) was larger than the own-panel slope.
- **Binding:** do not swing to a positive transfer claim either.
- **New experiment:** No.
- **Estimated gain:** correctness +0.25.

### 3. State what the CIs cover; add seed-level spread

- **Raised by:** R2 M4, R3 M3, R4 M3, R1 m6.
- **Files:** sec5_results.md:64, :74–76; sec4_system.md:41 (Table 4.2 Uncertainty row); sec7_limitations_ethics.md:16.
- **Text change:**
  - Say that all §5.4–5.5 CIs are percentile image bootstraps with seed fixed effects. They are conditional on the trained adapters and on one draw of the nested subsets.
  - Quote the forward per-seed values from d0_decide.json: b_K 9.94 / 10.77 / 11.05.
  - Say that two reverse seeds cannot estimate seed variance.
  - Report the planned (4.19) and realised (about 2.31) g_R half-widths.
  - Fix the Table 4.2 row.
- **New experiment (EXP→coordinator, CPU only):** compute per-seed reverse slopes and gaps (b_O^R, b_K^R, g_R per seed) from the existing dev predictions, plus an optional seed-and-image two-stage bootstrap. Label it POST_HOC / DESCRIPTIVE. R3's −1.37 / +3.94 are a reviewer's derivation and must not be quoted until they are recomputed and logged.
- **Estimated gain:** correctness +0.25.

### 4. One spine for the merged paper (PI decision)

- **Raised by:** R4 M6, R2 M7(b), R3 m1–m3, R1 clarity, R5 #2.
- **Files:** title_page_B.md:5, outline_B.md:5–8, sec1_intro.md:5, :9, :18–23, sec5_results.md:1 (section title), sec6_discussion.md:21 (subsection), sec8_conclusion.md, supplementary_B.md:5–7.
- **Change:** choose one of two options.
  - **Option A (AC default):** keep the training-gain title with "on development data" added, for example "What Training-Data Gains Measure on a Vietnamese Captioning Benchmark: A Development Study with Two Reference Panels, plus a Validity Audit of KTVIC and an Open Evaluation Kit". Move §5.4–5.5 to its own section right after the data section, present the audit findings as the explanation, and rewrite §1:9 ("Our answer is a protocol card…") and the contribution order to match.
  - **Option B:** restore the audit-and-kit title and present the two-panel study as one supporting section.
  - **Either way:**
    - Retitle §5 ("The audit applied to the controlled system").
    - Give the training-gain discussion its own §6 subsection instead of placing it under "Object scores need count control".
    - Update the supplement header and section map, adding the B-1, D-α, D0 and B-R1 verdict lines (R3 m14, R4 m13).
- **New experiment:** No.
- **Estimated gain:** clarity +0.5, contribution +0.25.

### 5. Match the headline to the evidence tier

- **Raised by:** R1 M3, R2 M3, R3 M4, R4 M4, R5 #2, R2 M5.
- **Files:** outline_B.md:8, sec1_intro.md:5, :16, sec5_results.md:57, :64, :74, sec7_limitations_ethics.md (§7.1).
- **Change:**
  - (a) Say in §5.4 that B-1 is the registered three-seed confirmation of an earlier single-seed dev result (+9.40, supplementary_B.md:286), and that the PASS bar (CI_lo > +1) was set below it.
  - (b) Say that D0's KTVIC-side slope was predictable from the decided B-1 result when the D0 rule was written. D0's new information is b_O and the gap. "Fixed before any of its scores were computed" must be qualified.
  - (c) Say that GO was near-certain given SESOI 1.0, and that the ASYMMETRIC margin 4.93 = 0.5·g is data-dependent and exceeds the own-panel reverse slope. Carry this weak-bound caveat into the abstract or §1:16 in one clause.
  - (d) Call B-R1 a pilot (2 seeds × 3 sizes).
  - (e) In the abstract, §1 and §7.1, say that the result stays at the dev-explore tier (187 images, one backbone), that KTVIC test is closed under one-look, and that confirmation is left to a future single registered look on unseen data.
- **New experiment:** No. The future confirmation is out of scope; note it for the coordinator as a candidate registration on non-KTVIC-test data only.
- **Estimated gain:** correctness +0.25, contribution +0 (honest scoping avoids a reviewer downgrade).

### 6. Related work and novelty statement

- **Raised by:** R1 M4, R2 M6, R3 M7, R4 M7.
- **Files:** sec2_related.md:13–19, Table 2.1 (sec2_related.md:21–32), sec1_intro.md:23, paperB.bib.
- **Change:**
  - Add a short paragraph and rows in Table 2.1 for these works, each verified before it is added:
    - same-image second caption sets: Multi30K (Elliott et al. 2016, 10.18653/v1/W16-3210), van Miltenburg et al. 2017 (10.18653/v1/W17-3503), Frank, Elliott and Specia 2018 (10.1017/S1351324918000074), COCO-CN (Li et al. 2019, 10.1109/TMM.2019.2896494);
    - reference variance and reference style: Yi et al. 2020 (10.18653/v1/2020.acl-main.93), Freitag et al. 2020 (10.18653/v1/2020.emnlp-main.5), Kornblith et al. 2023 (arXiv 2307.16686);
    - cross-domain captioning: Chen et al. 2017 (arXiv 1705.00930), Dessì et al. 2023 (arXiv 2304.01662; read it before citing);
    - ID/OOD scaling: Miller et al. 2021 (arXiv 2107.04649), Taori et al. 2020.
  - Optionally check nocaps and Localized Narratives.
  - State the novelty narrowly: "the same images, two human panels, a training-set-size slope in both directions, in a low-resource language". Say that the qualitative effect (training on one reference style raises scores against that style) is known.
  - Re-read Bromonschenkel et al. (2026) in full before relying on "Training-data curve: no" (R4 m12).
  - No priority claim.
- **New experiment:** No. This is a literature check only; any API call uses vsps-research@example.org or no e-mail.
- **Estimated gain:** novelty +0.5.

### 7. Remove priority wording about Tran et al.

- **Raised by:** R1 m2, R2 M2, R4 m2. R3 missed it; the AC confirmed it by grep.
- **Files:** sec1_intro.md:14, sec2_related.md:9, sec3_data_and_audit.md:64, cover_letter_B.md:13.
- **Change:** "first reported" / "were the first to report" → "reported".
- **New experiment:** No.
- **Estimated gain:** correctness +0.1 (required by a binding rule).

### 8. Complete the test-look ledger in §5.1

- **Raised by:** R4 M5.
- **Files:** sec5_results.md:25.
- **Change:** add one sentence listing all KTVIC-test looks related to MBR:
  - (a) the exploratory proxy seen before registration, +3.05 [+1.03, +5.11] (prereg/2026-10-20_b_f1_final_stack.md, ledger row L4). It used a different scorer and different members and was not used to choose the variant.
  - (b) the registered B-F1 look: FAIL, −0.39 [−2.44, +1.67].
  - (c) the post hoc full-train row, +3.14 [+1.11, +5.16], with no verdict (supplementary_B.md:289).

  Also say that KTVIC test has been scored for about 79 systems in the ranking audit, so in this paper it supports description, not method claims. The FAIL keeps its place.
- **New experiment:** No.
- **Estimated gain:** correctness +0.1.

### 9. Put the two-panel scoring protocol on the card

- **Raised by:** R1 M7, R3 M6 / m4, R4 m7, R2 M4(d).
- **Files:** sec4_system.md:32–42 (Table 4.2), sec5_results.md:64.
- **Text change:**
  - Add a "two-panel dev" column or note to Table 4.2: 187 images; k = min(5, available) references per panel (mean 4.42); CIDEr-D document frequencies computed per panel over the 187 images; trailing punctuation stripped from hypotheses (scripts/b_d0/d0.py:203); σ=∞ co-primary for GO_BOTH only.
  - Add one sentence on noisy per-panel IDF, and say that the log-scale companion handles level differences but not IDF differences.
  - Use the dev reference lengths (17.09 vs 12.80) instead of the test lengths at sec5_results.md:80 (R4 m6).
- **New experiment (EXP→coordinator, CPU only, 9b):** recompute the forward and reverse gaps with metrics that do not use per-panel IDF (BLEU-4, ROUGE-L, chrF, CIDEr-D with df pooled over both panels) on the existing dev predictions. Label it POST_HOC / DESCRIPTIVE / DEV; the decided verdicts are unchanged.
- **Estimated gain:** correctness +0.25 if the robustness row is done; clarity +0.1.

### 10. Name annotator identity as a live alternative; narrow the mechanism language

- **Raised by:** R1 M6, R5 #1 and #4, R2 m4, R4 m4.
- **Files:** sec5_results.md:80, sec7_limitations_ethics.md:16, sec3_data_and_audit.md:19–21, :32–38, outline_B.md:8, sec8_conclusion.md:5–7.
- **Change:**
  - Put annotator-identity learning (Geva et al. 2019; KTVIC has three annotators) beside reference homogeneity as an equally live, untested explanation.
  - If annotator IDs are recoverable, describe in one sentence how a writer-held-out split would separate the two. This is text only; do not run it.
  - In the abstract and conclusion, keep "one writer" tied to the KTVIC documentation plus the statistic, and add the slot-rate-preserving null (0.45).
  - Keep the punctuation cost tied to the pipeline condition. Rephrase it as "appending a period … costs 35.17 points in a pipeline without PTB punctuation removal, and nothing with it".
  - Keep the protocol condition (CIDEr-D ×100, P0) next to each headline number (R5 m5).
  - Source or soften "Vietnamese pipelines replace the PTB tokenizer" (R3 m12).
- **New experiment:** No.
- **Estimated gain:** correctness +0.1.

### 11. One main-text results table for §5.4–5.5, with internal codes removed

- **Raised by:** R2 M7(a,c), R3 m15, R4 m5, R1 m9 / m11, R2 m11.
- **Files:** sec5_results.md:57–94, sec6_discussion.md:21, number_manifest_B.tsv, figs.
- **Text change:**
  - Add a table with direction (forward / reverse) × panel (KTVIC / OpenViIC): slope [CI], gap, g_rel, σ=∞ gap, number of images, seeds × sizes, and a pointer to the five confounds of g − g_R. Per-seed values go in once item 3 delivers them.
  - Move the descriptive rows and the procedure (hashes, id-set hashes, k rule) to a supplement subsection.
  - Replace D0, B-R1, O5b, P1 SESOI, kit_b, fuse2, P1-R and "registered sense" with plain names.
  - Explain once that the ASYMMETRIC sub-label was added after scoring as a recorded deviation.
  - Disambiguate "with both CIs above zero" (R2 m5).
  - Explain σ=∞ (R2 m6).
  - Say that the bootstrap is order-dependent (R2 m7).
  - Mark the exact-class matcher caveat at sec5:70 (R2 m10).
  - Name the matcher for the +1.19 object F1 (R3 m7).
  - Map PASS to FUND_EXTERNAL_IMAGE_DATA (R3 m8).
- **Figures (11b, EXP→coordinator, CPU plotting only):**
  - Fig 5.2: per-seed points or bootstrap bands, marker shapes for greyscale, a caption note that the panels sit on different score levels, and a note that the reverse direction has 3 sizes × 2 seeds.
- **Estimated gain:** clarity +0.5.

### 12. Fix wording that overstates

- **Raised by:** R1 M5 / m1 / m3, R3 M5, R4 m3 / m8.
- **Files:** sec8_conclusion.md:5 (and check sec5_results.md:45 and sec6_discussion.md:21 for the same claim), sec1_intro.md:5, :14, outline_B.md:8.
- **Change:**
  - "more than half" → "about half (55.12% [49.38, 61.05]; one contrast, one seed)".
  - "nearly vanishes" → "is smaller and not distinguishable from zero against the second panel (−0.25 [−2.43, 1.96]; one contrast, one seed)".
  - "reliably improves the model" / "improves the system reliably" → "raises CIDEr-D against KTVIC references by +9.61 [7.18, 12.36] per doubling (development data, one backbone)".
  - "the same slope across seeds" → "similar (9.50, 9.62, 9.71)".
  - In the abstract, add the +10.59 CI [7.43, 13.81] and name both image sets (300 for B-1, 187 for the two-panel study), so the sentence reads "On the 187 development images that also have UIT-OpenViIC captions…".
- **New experiment:** No.
- **Estimated gain:** correctness +0.1, clarity +0.1.

### 13. Fix statements made stale by the merge

- **Raised by:** R1 M8, R3 m5 / m13, R4 m9.
- **Files:** sec4_system.md:7, :20, sec4_system.md:9–16 (Table 4.1), sec3_data_and_audit.md:66, :86.
- **Change:**
  - sec4:20: §5.4–5.5 also use the dev300 carve and 3,469-image nested subsets.
  - sec3:66: six OpenViIC-trained dev adapters now exist. They are dev-only and were never decoded on a test split, so the registered leakage test is still not evaluable.
  - Add Table 4.1 rows for the B-1 and B-R1 adapters (first caption, 3,469-image pool, assistant-only loss, k = 1 OpenViIC caption for the reverse direction).
  - sec4:7: the "differ only in targets or loss mask" sentence must also mention training-set size.
  - Reconcile the "no ID lists released" statement with the 187 dev ids in the rule files and r1_lists.json.
- **New experiment:** No.
- **Estimated gain:** correctness +0.1, clarity +0.1.

### 14. Consistency and copy-edit batch

- **Raised by:** R1 m5 / m8 / m10 / m12, R2 m2 / m3 / m4 / m8 / m9 / m13, R3 m9–m11 / m16 / m17, R4 m1 / m10 / m11 / m14, R5 m1 / m2 / m3 / m4.
- **Files:** various.
- **Change:**
  - sec3:11 cross-reference "Section 5.3" → 5.2.
  - Cite UIT-OpenViIC consistently, using the journal version; paperB.bib:36/:48.
  - Add the missing period at sec2:5.
  - "validated" → the sec8 wording at sec1:21 and sec3:80 (R4 m1, R5 m2).
  - Use two decimals in Table 5.1.
  - Make the GRIT 136.0 comparison relative only, or drop it.
  - Consider "pre-specified (internally time-stamped)" for "preregistration", or deposit the rule files with an external timestamp.
  - Say once that the masked re-read and the matched design were post hoc.
  - Optionally rename the §5.2 heading to "Cross-dataset scoring on UIT-ViIC".
  - Separate task adaptation from template match at sec6:9.
  - Complete the FAIR 2026 citation and make the reused-vs-new split easy to check (R5 m1).
  - Give one main-text line on why the exchangeability statistic uses object doubletons and adjacent slots (R5 m4).
  - Keep "no new human judgments" visible next to "better descriptions" (R5 m3).
  - Strip the internal HTML comments in the submission build.
  - Trim the length by moving §3.3, §3.6 and the §5.5 descriptive rows to the supplement.
  - Re-date the cover letter.
- **New experiment:** No.
- **Estimated gain:** clarity +0.25.

### 15. Submission blockers held by the PI (low priority, but needed before acceptance)

- **Raised by:** R5 #3, R1 m12.
- **Files:** cover_letter_B.md:25, :27, outline_B.md:72, STATUS.md:27, sec3_data_and_audit.md:82, sec7_limitations_ethics.md:28.
- **Change:**
  - Make the kit resolvable and citable: a Zenodo DOI or public repository with versioned instructions that match the stated archive contents.
  - Reconcile the data-permission status. cover_letter:27 says confirmations were received in writing on 2026-10-28, while outline:72 still says [AUTHOR TO PROVIDE]. Default: if the confirmations are real, update outline/STATUS; otherwise reword the cover letter.
  - Add the ORCIDs.
- **New experiment:** No.
- **Estimated gain:** contribution +0.25 (R5 treats the missing archive as blocking).

## Items sent to the coordinator (not done in this revision)

All of these are CPU only, on existing dev outputs, post hoc and descriptive, with no verdict. None is a new test look and none uses new labels.

1. **Item 3:** per-seed reverse slopes and gaps, plus an optional seed-and-image two-stage bootstrap, for both directions.
2. **Item 9b:** a metric-robustness row with BLEU-4, ROUGE-L, chrF and pooled-df CIDEr-D for the forward and reverse gaps.
3. **Item 11b:** a redraw of Figure 5.2 from figs/fig_values_B.json.
4. **Future, outside this paper's test budget:** a registered single-look confirmation of the forward two-panel gap on data no adapter has seen. KTVIC test is excluded.

## Expected scores after revision (AI opinion)

| Criterion | Now | After | Main drivers |
|-----------|-----|-------|--------------|
| Novelty | 3 | 3.5 | item 6 |
| Correctness | 3 | 4 | items 1, 2, 3, 5, 7–10, 12, 13 |
| Contribution | 3 | 3.5 | items 4, 15 |
| Clarity | 2.5 | 3.5 | items 4, 11, 14 |

Expected outcome at the next round, if items 1–14 are done and item 15 is resolved: minor revision (AI opinion).
