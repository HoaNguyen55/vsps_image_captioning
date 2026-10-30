# Paper A all-out plan (PI-1030b/c), 2026-10-30

Everything in this file is **AI opinion** (planning agent), not a judge ruling and not a human decision. No paper text was edited, nothing was committed, no machine was touched. Times are Vietnam time (UTC+7). Review paths are relative to `manuscript/reviews/`.


> **CC-181 (2026-10-30T01:40Z) applied to this plan (W1, W10).** A-T2 as a confirmatory/one-look test is **NO-GO** (r4, 96%): no unscored XM3600 image exists. The 600 (A, `data/xm3600_subset.txt`), 500 (C dev, `xm_dev500.files`) and 2,500 (C one-look test, `xm_test2500.files`) sets are pairwise disjoint and cover all 3,600 images; the 1,519-image resolved pool is 1,271 (C test2500) + 248 (C dev500), the 1,984-image OIV7-labelled pool is 1,673 + 311. A-T2 tiers 1–3, its schedule rows and the Q1 test assignment are struck below (kept legible, not deleted). Any A use of XM3600, even descriptive on XM600, needs a PI lift of CC-153 r4 (W11). Venue figures (SJR values, 436 days) are **UNVERIFIED** until checked on scimagojr.com and the journal pages (CC-154 W10). Dates: target freeze 11-10 / submit 11-12, **hard cap 18/12** (PI-1026ba, LOG l.636), pending PI Q6.

## Tóm tắt cho PI (tiếng Việt)

- **Xác suất được nhận ở SPIC hiện nay (ý kiến AI): khoảng 35% (khoảng 25–45%).** Con số này gồm khoảng 25% rủi ro bị từ chối ngay ở vòng biên tập (bài dài khoảng 12.500 từ, đọc giống nghiên cứu đánh giá NLP, nhiều mã đăng ký nội bộ), và khoảng 50% được nhận sau khi bài đã vào vòng phản biện. Hai vòng sửa vừa qua đã xử lý hết các lỗi văn bản. Các điểm yếu còn lại nằm ở cấu trúc của bằng chứng:
  - cơ sở xác nhận hẹp: một bộ 600 ảnh và hai backbone cùng họ Qwen;
  - nhánh "label gold" thất bại trên PASCAL-50S;
  - kết quả chính phần lớn là hệ quả gần như tất yếu của cách xây dựng gold, nên tính mới chỉ ở mức trung bình;
  - không có kết quả xác nhận nào về kiểm soát số đối tượng;
  - độ phù hợp với SPIC còn yếu.
- **Ba việc nên làm trước:**
  1. **(0 GPU, làm ngay hôm nay)** Đo tiền đề của phép thử A4 trên PASCAL-50S mà không cần output mô hình (mục FLAG 5b): so tổng số lớp V20 trong 50 reference với 1.782 nhãn VOC. Việc này trả lời đúng điều reviewer nói là "assumed, not measured". Cần một judge cho phép staging lại reference.
  2. **(văn bản, 10-30 → 11-08)** Rút thân bài từ khoảng 12.500 xuống ≤ 9.000 từ và đóng khung lại theo hướng SPIC ("độ đo chất lượng phụ thuộc tập tham chiếu"). Đồng thời sửa các mục còn mở:
     - thêm câu A-T1 PREMISE_NOT_MET vào supplement (bắt buộc theo đăng ký);
     - xử lý hai trích dẫn mới chỉ đọc tiêu đề;
     - sửa câu sec7:38 nói rằng phần XM3600 còn lại "được giữ cho một nghiên cứu đăng ký riêng".
  3. ~~**(GPU, nếu PI và judge đồng ý)** A-T2: lặp lại phép thử thứ tự slope trên **1.519 ảnh XM3600 còn lại** (cùng giao thức, nhãn OIV7 do người kiểm), với **thêm các họ mô hình ngoài Qwen** (InternVL3, Gemma-3, Aya-Vision-8B, LLaVA-OV). Thực hiện theo đúng ba tầng: dev trên 600 ảnh đã dùng → rehearsal → một lần nhìn. Tổng khoảng 25–35 GPU-h. Phải xác minh trước là 1.519 ảnh này chưa từng được chấm, vì sổ test-set hiện ghi "XM3600 (all) spent". Kiểm tra cục bộ hôm nay: trong `data/results/` không có file chấm nào vượt quá 600 ảnh đã đăng ký; bản sao máy GPU và các file của bài B/FAIR thì chưa kiểm tra.~~ **CC-181: NO-GO** — 1.519 ảnh này là tập dev500 và test2500 (đã dùng) của bài C; không còn ảnh XM3600 nào chưa chấm.
- **Kỳ vọng (ý kiến AI):**
  - làm 1 và 2: khoảng 42%;
  - nếu A-T2 PASS: khoảng 50%;
  - nếu A-T2 FAIL (vẫn báo cáo ngắn): khoảng 39%.
- **Tạp chí:** giữ **SPIC** làm đích chính. Phương án dự phòng sau khi có quyết định của SPIC là **JVCIR**, chuyển bài qua dịch vụ chuyển bài của Elsevier. **Không chọn IEEE Access:** trang chính thức hôm nay ghi tỷ lệ nhận 20% và chỉ có hai kết quả nhận hoặc từ chối, không có vòng sửa lớn, trong khi bài A hiện ở mức "major revision".
- **PI cần quyết (kèm khuyến nghị):**
  - ~~Q1: cho A-T2 dùng 1.519 ảnh XM3600 làm test nếu xác minh chưa chấm (**khuyến nghị: đồng ý**).~~ (gạch bỏ theo CC-181 r4)
  - Q2: ưu tiên A trên M2 trước BD-T1 (**đồng ý**).
  - Q3: gia hạn M2 sau 11-02 04:46 hoặc chuyển A-T2 sang M1 (**chuyển sang M1, không gia hạn trừ khi A-T2 tầng 1 đạt**).
  - Q4: giữ SPIC, dự phòng JVCIR (**đồng ý**).
  - Q5: có lấy lại test KV-4,224 từ MT4 cho A hay không (**không**).
  - Mốc khóa bản thảo là 11-10 và nộp 11-12 (mục tiêu); hạn cứng 18/12 (PI-1026ba), chờ PI xác nhận (CC-181 Q6). Địa chỉ bưu điện, link cho reviewer và DOI Zenodo vẫn là việc của PI và chặn việc nộp.

## 1. Current estimate and the top five reasons it is not higher

### 1.1 Estimate (AI opinion)

| Component | Now (after revision rounds 1–2) | Basis |
|---|---|---|
| P(desk reject at SPIC) | ≈ 25% | SPIC scope lists "Multimedia quality assessment and measures" (Elsevier journal page, fetched today), but R1 and R4 both say the paper reads as NLP evaluation (A_R1_area.md:221; A_R4_editor.md:109–121). Main text is 12,488 words (A_RESPONSE_TO_REVIEWERS.md:17), still dense |
| P(accept \| sent to review), after one or two revision rounds | ≈ 50% | AI panel: unanimous major → expected minor after fixes (A_META_REVIEW.md:7, :220). Discounted, because an AI panel is not SPIC's reviewer pool and the open issues below are structural |
| **P(accept at SPIC)** | **≈ 35% (25–45%)** | Consistent with the coordinator's 35–45% (LOG l.840) |

### 1.2 Top five reasons, with what revision already did and what is left

| # | Reason | Reviewer evidence | Already done | Still open |
|---|---|---|---|---|
| 1 | **Narrow confirmatory base.** One 600-image set; the second backbone is the same Qwen family on the same images; two of five XM3600 predictions failed | A_R4_editor.md:122, :233; A_codex_review.md:16; A_R2_methods.md:204 | Stated plainly in the abstract and §1 (scope "on XM3600 and its second backbone") | No new data. Only a new held-out set or system family can move it (§3, G1) |
| 2 | **The risky label-gold leg is fragile.** It needs verified precision; reference signs rest on one verbose system; it FAILED on PASCAL-50S | A_R1_area.md:20–21, :47; A_R3_metrics.md:101; A_codex_review.md:24 | Tally given honestly (PASS / weak PASS / FAIL); bracket +1.97 [−0.44, +4.01] in abstract; verifiable share 43.4–69.7% | The A4 premise is "assumed, not measured" (A_META_REVIEW.md:96, :98). FLAG 5b is unrun. A-T1 tried to measure it on ADE20K and got PREMISE_NOT_MET (LOG l.810); the paper does not report this yet |
| 3 | **The headline ordering is near-mechanical, so novelty is incremental (3/5 from all five)** | A_R1_area.md:20, :217; A_R3_metrics.md:42; A_R4_editor.md:202 | Title changed; expected and risky parts separated; X4 placed as the informative result | Novelty lever left: X4 is the only non-SCAR result; it rests on one set (PASCAL-50S) |
| 4 | **No confirmatory count-control result**, though it is the most actionable part for practitioners | A_R1_area.md:219; A_R4_editor.md:235; A_codex_review.md (Contribution) | Scoped as "confound control here; no count-control claim is confirmatory" (highlight 5) | Cannot be fixed under the no-new-labels rule before 11-10. Keep it scoped; do not oversell |
| 5 | **Venue fit and reading burden** | A_R1_area.md:221; A_R4_editor.md:109–121, :113; A_META_REVIEW.md:40 | Ledger moved to S4.0; codes renamed; §6 and §8.3–8.4 moved; Intro paragraph citing González-Chávez et al. 2024 (SPIC) | 12,488 words is still long. SPIC framing appears in one paragraph and §9.4 only |

Also open, and text can only disclose it: PASCAL-50S per-image auditability, because the outputs were deleted (A_R1_area.md:86; A_R4_editor.md:227; A_codex_review.md:20).

## 2. Venue check

Source limits: scimagojr.com and ScienceDirect "insights" both returned **HTTP 403** today. SJR and quartile values come from `manuscript/cfp/venue_fit_2026-10-28.json`. That file was built from a non-official SJR parquet that matched 28/28 values fetched live on 10-14, so treat every value below as **unverified**. A person re-checks it on scimagojr.com before filing (CC-154 W10). Review times marked "carried" come from a 10-14 ScienceDirect fetch. No e-mail was sent in any request.

| Venue | SJR 2025 (CS quartile, PI-1026bi) | Scope fit for A | Review / speed | Acceptance | CC-154 fit for A | Verdict (AI opinion) |
|---|---|---|---|---|---|---|
| **Signal Processing: Image Communication** | 0.607, Q2 (CV&PR) **UNVERIFIED** | Scope lists "Multimedia quality assessment and measures" (Elsevier page, today). Direct precedent: SPIC 2024 caption-metric validity (10.1016/j.image.2023.117071); UIT-OpenViIC also published there | carried: 15 d to first decision, **436 d to acceptance** (**UNVERIFIED**) | not published | 8 | **Primary** |
| J. Visual Communication and Image Representation | 0.573, Q2 (CV&PR), Q1 Media Tech **UNVERIFIED** | Visual representation and quality; no A-type precedent found | carried: 15 d first decision, 215 d to acceptance | not published | 5 | **Fallback** (after the SPIC decision; Elsevier transfer route unverified) |
| Pattern Recognition Letters | 0.793, Q1 (CV&PR) | Concise letters | carried 196 d to acceptance; 2011 IAPR figure 29% | ≈ 29% (2011) | 5 | No. A would need cutting to a letter; the registered-ledger content does not survive that |
| IEEE Access | 0.884, Q1 (CS misc.) | Broad | **4–6 weeks; binary accept/reject** (official About page, today) | **20%** (official page, today) | 6 | No. Binary review means no major-revision round; A sits at major now |
| Multimedia Tools and Applications | 0.798, Q1 (Media Tech) | Broad | carried median 34 d | — | 2 | **Excluded: WoS SCIE "On Hold"** (MJL, 10-28) |
| Computer Vision and Image Understanding | 0.82, Q1 (CV&PR) | Method-leaning CV | unknown | unknown | 5 | No. Higher bar, weaker fit; Q1 type cap 2 for an audit paper |

**Recommendation (AI opinion):** primary **SPIC**, which is unchanged from CC-154 (3/3, no switch). Fallback, used only after a SPIC decision, is **JVCIR**. CC-154 listed EMNLP 2027 as A's fallback; JVCIR is offered because the PI's target is a Q2 journal, and it is a PI decision.

**Expected outcome:**
- SPIC: P(accept) ≈ 35% now, ≈ 42–50% after this plan. Time to acceptance is about 12–15 months if the carried 436 d holds (**UNVERIFIED**), so acceptance would land around Q4 2027 to Q1 2028.
- JVCIR as second shot: ≈ 35–40% (AI opinion), about 7 months.

The 436-day figure (**UNVERIFIED**, CC-154 W10) is the one real penalty of SPIC. The PI should know it before submission, because "accepted" may slip into 2028.

## 3. Ranked action list

### 3.0 The binding constraint: test sets

A owns no unspent test set any more:
- PASCAL-50S is spent.
- ADE20K val is closed by A-T1 PREMISE_NOT_MET; its registered consequence forbids changing the share, V or threshold, so re-opening ADE20K would be a forking path.
- KV-4,224 belongs to L3-P1/MT4 (committed prereg, commit 70c898a).
- OIV7 val belongs to L2-P1, and AMBER to L2-P2.
- XM3600 is listed "all spent" (PORTFOLIO_3Y §2.3, l.187).

~~There is one possible exception. The paper says the 600 XM3600 images were "a random draw (seed 0) from the 2,119 XM3600 images with a verified label on a mapped OIV7 class … The other XM3600 images are held out for a separate registered study" (sec7_verbosity_sign.md:38). If the other **1,519** images were never scored by any line, they are the cheapest same-protocol held-out set A could get. **This must be verified first**. Local check done today: no score or decide file under `data/results/` holds XM3600 outputs for more than the registered 600 (`data/xm3600_subset.txt`, 600 ids), and the 10-14 full verdict file covers the same runs. Machine backups, Paper B/FAIR evaluation files and any L2-a dev use were **not** checked; a judge must finish that check (grep every decide and score file for XM3600 ids outside the 600). The ledger then needs a judge and PI line, because the ledger and the paper currently disagree.~~

**Correction (CC-181 r4, r5).** The "never scored" check above searched `data/results/` only. The C mirrors (`c_test` on M1/M3) hold C's decodes and guard scoring of the 2,500 test images. The chair's partition check: `data/xm3600_subset.txt` (600), `.session_backup/2026-10-22/c_stage2/subsets/xm_dev500.files` (500) and `.session_backup/2026-10-26/c_test/staging/xm_test2500.files` (2,500) overlap 0/0/0 and their union is 3,600. The 1,519 images are 1,271 of C's spent test set + 248 of C's dev set, so there is no exception: the ledger's "XM3600 all spent" is correct and sec7:38 "held out" is wrong (fixed per W3).

No new **confirmatory** result fits before 11-10; any GPU work is descriptive, with a small gain.

### 3.1 (a) Text-only fixes still open, ranked by gain

| # | Fix | Answers | Gain in P(accept) (AI) |
|---|---|---|---|
| T1 | Cut the main text 12,488 → ≤ 9,000 words. §6.1–6.3 is the next lever (A_RESPONSE:144). Move derivations, specification-curve detail and ledger prose to the supplement | Reason 5; A_R4_editor.md:113 | +3 to +4 (mostly the desk-reject risk) |
| T2 | Re-frame for SPIC: "an object-hallucination score is a reference-dependent quality measure; its sign depends on gold completeness, as full-reference quality measures depend on the reference". Put it in the title-page abstract lead, §1 paragraph 1, §9.4 and the cover letter, citing 2–3 SPIC quality-measure papers after reading them | Reason 5; A_R1_area.md:221 | +2 |
| T3 | Add the registered A-T1 sentence to the supplement (fixed text, PREREG §6 clause 0): "the label rung was measured and was not twice as complete as one narrative on ADE20K training images" (1.24×, LOG l.810). No mention of ADE20K exists in any submitted A file (sec*.md, both supplements) now. One clause in §6.4 too, so the PASCAL FAIL reading is honest | Reason 2; registered-failure rule | +0.5, and it removes an integrity risk |
| T4 | Fix sec7:38 "held out for a separate registered study" to match the ledger: either "not used" or, if A-T2 runs, its result | Integrity | removes a reviewer trap |
| T5 | Citations: Spain & Perona 2010 and Berg et al. 2012 are cited "at title level, full text not read" (paperA.bib:1232). Read them or drop them. Add `intext_trace.tsv` rows for the four new citations; recount "29 of 804 rows" (manifest is now 1,241 lines) | Integrity, A_RESPONSE:107, :192 | +0.5 |
| T6 | `anon/declarations_anon.md` lacks the reproducibility sentence (A_RESPONSE:193) | A_codex_review.md:20 | small |
| T7 | Deposit per-image sufficient statistics for XM3600 and COCO-295 (class-id sets per image and run, no caption text) where licences permit. This is the only real auditability fix | Reason 1 and auditability; A_codex_review.md:20 | +1 (PI/coordinator decision) |
| T8 | PI admin, blocking submission only: postal addresses, reviewer link, Zenodo DOI | A_META_REVIEW item 3 | blocks submission |

### 3.2 (b) Experiments

Costs are scaled from the measured P50 anchor: **4.73 GPU-h for 7 models × 2 prompts × 1,000 images** (LOG l.730), i.e. ≈ 0.34 GPU-h per model-prompt per 1,000 images. Vietnamese decodes are ×1.3 (longer tokens).

| Rank | Item | Storyline fit | Reviewer concern answered | GPU-h (one 3090) | Tier-1 dev feasible? | New prereg / test spent | P(FAIL) | ΔP(accept) (AI) | Start on M2 11:00 today? |
|---|---|---|---|---|---|---|---|---|---|
| **G0** | **FLAG 5b: output-free V20 gold sizes**. Σ\|refs50 ∩ V20\| vs Σ\|voc20\| = 1,782, plus set differences, by level k = 1…50 | Exact: tests the premise behind the A4 FAIL | Reason 2; A_META_REVIEW.md:96–98; A_R2_methods.md:62 | **0** (CPU, laptop or M1) | n/a (no outputs) | No prereg; post hoc descriptive. Needs a **one-judge ruling** on re-staging PASCAL-50S references (data rule) | none (no verdict) | **+2 to +3**: either "the label rung was not more complete" (the FAIL is explained, as consistent-with) or "it was more complete" (the FAIL is real and stated so) | CPU, yes, once the ruling is in |
| ~~**G1**~~ | ~~**A-T2: held-out XM3600 replication with new families.** Same G2-B protocol (verified precision primary; "unverifiable = error" pre-declared as co-reported), ≥ 4 families: Qwen2.5-VL-7B, InternVL3-8B, Gemma-3-4B (12B does not fit a 3090 in bf16), Aya-Vision-8B (already pinned for C-T1), LLaVA-OV-7B. Short and detailed. Pre-registered system leave-one-out. Language validity pre-declared in tier 1: each model's Vietnamese-output rate is measured, models under a threshold fixed before any slope is seen are dropped, and the existing clean-caption analysis-set rule applies (otherwise English-leaking models score zero mentions and distort M). **Per-image class-id sets kept** (no text), so the result is auditable even if 8-gram hits force caption deletion / Exact: the label-gold ordering of the confirmatory claim, out of sample on the same population / Reasons 1 and 2; A_R4_editor.md:122, :233; A_R1_area.md:55–66 (system dependence) / Tier 1: XM3600-600 split D1 300 / D2 300, 6 models × 2 prompts ≈ 0.34 × 12 × 0.3 × 1.3 ≈ **1.6** per half. Tier 3: 1,519 × 12 runs ≈ **8.1**; with English prompts + XM3600 English refs ≈ **16**. Cap 25 / **Yes**: 600 spent images are dev / Tier-1/2 prereg (reversible ≥ 90, one judge); tier-3 prereg (irreversible: 92–98 band per PI-1029o, panel + Codex, ranked options). **Spends the 1,519 held-out XM3600 images**, only if verified unscored and assigned to A / ≈ 30–40% for the full label-gold ordering; lower for the reference rungs. A non-Qwen family may hit the one-verbose-system issue. Tier 2 gates it at P(PASS) ≥ 98% / From the ≈ 42% post-text baseline: **PASS +8 (→ ≈ 50%), FAIL −3 (→ ≈ 39%)**; P(reaching tier 3) ≈ 0.4–0.5, so expected ≈ +3 to +4. Only run the test if tier 2 predicts P(PASS) ≥ 98% / Tier 1 only if the judge lifts the M1-only XM3600 rule (PI-1029h Q5 lifted CC-153 r4 for M1, not M2). Else M1 from 10-31 03:45~~ **NO-GO (CC-181 r4)** |
| G2 | **English comparison on XM3600-600** (descriptive, dev). The same new families with English prompts, scored with XM3600 English references and the same OIV7 labels | PI English rule; the paper already has PASCAL-50S English | Reason 1 (one language on the confirmatory set) | ≈ 0.34 × 12 × 0.6 ≈ **2.5** | It *is* dev | No test spent. Post hoc descriptive, no verdict | n/a | +1 | Same M2 rule as G1; bundle with G1 tier 1 |
| G3 | **KV-4,224 COCO-80 test** (COCO instance labels are exhaustive for 80 classes; 5 references). The CHAIR home benchmark, English, exhaustive labels | Strong: exhaustive label gold, CHAIR vocabulary | Reasons 1, 2 and 3 | Tier 1+2 on Karpathy-train 2 × 1,000 ≈ **9.5**; test 4,224 × 14 runs ≈ **20** (cap 30) | Yes (Karpathy-train is dev) | Needs the PI to **take KV-4,224 from MT4/L3-P1** (committed prereg 70c898a; irreversible; CC-174 K1+K6 branch). Plus a measured premise (labels ≥ 2× one reference, output-free on train, CPU) | ≈ 25–35% | From ≈ 42%: PASS +8, FAIL −3. But it costs MT4 its only committed test | No (PI decision first; the premise check is CPU and could run today) |
| G4 | **PASCAL-50S leave-one-model-out by re-decoding** | Robustness of a decided verdict | A_R4_editor.md:227; A_R2_methods.md:73 | ≈ **4.7** (same 14 runs) | n/a | The meta-review refuses it as a second look (A_META_REVIEW.md:110, :207). Outputs would hit the 8-gram rule again and be deleted. bf16 re-decode on another host is not guaranteed bit-identical, so it is not a regeneration | n/a | ≈ 0, or negative if a reviewer reads it as a second look | **No.** Judge FLAG only. The XM3600 system LOO already exists (`data/results/a1_robustness/a1_system_robustness.json`, `sign_stable_under_loo`) |
| G5 | Larger XM3600 image set for the *same* registered test | — | — | — | — | Not possible: the 600 are a registered draw. The only "larger set" route is G1 | — | — | — |
| G6 | Confirmatory count control | Reason 4 | A_R4_editor.md:235 | — | — | Needs a human-judgment test set, which conflicts with the no-new-labels rule. Out of scope before 11-10 | — | — | No. Keep it scoped as future work |

**Ranked recommendation (AI opinion):**
1. T1–T6 and G0 (no GPU).
2. ~~G1, with G2 bundled into its tier 1, if the 1,519 images are verified unscored.~~ NO-GO (CC-181 r4). G2 also needs a PI lift of CC-153 r4 (W11); recommended NO before the freeze.
3. G3 only if the PI chooses to take KV-4,224 from MT4. Not recommended, because it trades MT4's only committed test for about the same gain G1 offers.
4. G4, G5 and G6: no.

~~Budget: G1 + G2 cost ≈ 25 GPU-h of the ≈ 200 machine-hours PI-1030b buys. The rest stays for C-T1, L1-b and BD-T1.~~ (G1 closed, CC-181 r4)

**What M2 can honestly start at 11:00 today.** No A job has a committed prereg, so no A GPU job can start at 11:00.
- ~~If the A-T2 tier-1 prereg gets a one-judge GO (≥ 90) and a ruling lets XM3600 dev images on M2, G1 tier 1 + G2 (≈ 4 GPU-h) can start around 16:00–20:00 today.~~ (CC-181 r4, r6: no A XM3600 job, not on M2.)
- Until then, and as filler, M2 runs BD-T1 (keep-GPU-queue-full rule).

## 4. Day-by-day schedule to a submission-ready A

Target: **freeze 11-10, submit 11-12** (SPIC); hard cap **18/12** (PI-1026ba), pending PI Q6 (CC-181 r10). A-T2 cells struck per CC-181 W1.

| Day | Writing (laptop) | CPU / GPU | Gate |
|---|---|---|---|
| **Thu 10-30** | T3, T4, T5 start; T1 cut plan per section | G0 ruling + run (CPU). ~~Verify that the 1,519 XM3600 images are unscored. Draft the A-T2 tier-1 prereg (D1/D2 = 300/300 of XM3600-600; model list; per-image class-id retention).~~ M2: BD-T1 as filler from 11:00 | Judge: G0 data ruling ~~; A-T2 tier-1 GO (≥ 90); M2 XM3600 ruling~~ |
| Fri 10-31 | T1 (§1–§3), T2 | ~~A-T2 tier 1 on D1 (M2, or M1 after 03:45), ≈ 2–4 GPU-h.~~ G0 text written | ~~Tier-1 outcome: stop (one supplement sentence) or tier 2~~ |
| Sat 11-01 | T1 (§6), T6 | ~~A-T2 tier 2 rehearsal on D2, ≈ 2 GPU-h. Tier-3 prereg drafted with fixed paper sentences per outcome~~ | ~~Rehearsal P(PASS) ≥ 98%? If not, stop~~ |
| Sun 11-02 | T1 (§7–§9) | M2 rental ends 04:46. ~~Tier-3 prereg: panel + Codex (irreversible, actionable ≥ 92 per PI-1029o; this is judge confidence, distinct from the rehearsal's predicted P(PASS) ≥ 98%) → gatekeeper commit. PI reads the tier-3 prereg summary (PI-1029j listed a human read as evidence). Tier-3 run on M1 (≈ 8–16 GPU-h)~~ | ~~PI Q1 must be answered by now~~ |
| Mon 11-03 | ~~Integrate the A-T2 result (one §6.2 paragraph, Table 1 row, supplement)~~ | ~~Score once; mirror the decide file~~ | ~~Write-up check (one judge)~~ |
| Tue 11-04 – Thu 11-06 | Full read-through ≤ 9,000 words; figures; supplement regenerated (`scrub_supp.py`); bib and trace audit; build | — | — |
| Fri 11-07 | Mock SPIC review (expert-review / judge-panel, 4 reviewers + Codex) | — | Target: no blocking item |
| Sat 11-08 – Sun 11-09 | Fix mock-review items; PI study brief update (STUDY_BRIEF_A.md) | — | — |
| **Tue 11-10** | **Freeze**: ngram scan, sha snapshot (other tool writes the repo), manifest check, PDF build | — | Gatekeeper commit |
| Wed 11-11 – Thu 11-12 | PI fills addresses, reviewer link and DOI; PI reads and approves; **submit** | — | PI |

~~If A-T2 stops at tier 1 or 2, drop the A-T2 rows;~~ A-T2 is closed (CC-181 r4); the freeze date does not move. Report the dev ablation in one supplement sentence.

### What the PI must decide (decisions only; recommended answer = default)

| Q | Decision | Recommended (default if no reply by the stated time) |
|---|---|---|
| ~~Q1~~ | ~~Assign the 1,519 held-out XM3600 images to A as A-T2's one-look test, if verification shows they were never scored~~ | ~~**Yes** (by 11-01 12:00)~~ Struck: NO-GO (CC-181 r4); replaced by CC-181 Q1 (accept SPIC with no new confirmatory GPU result; default YES) |
| Q2 | A work goes ahead of BD-T1 on M2 whenever an A job is ready | **Yes** (immediately) |
| Q3 | Extend M2 past 11-02 04:46? | **No**: tier 3 runs on M1. Extend only if a C/L1 job needs it |
| Q4 | Venue: SPIC primary, JVCIR fallback after the SPIC decision (replaces EMNLP 2027 as A's first fallback) | **Yes** |
| Q5 | Take KV-4,224 from MT4 for an A COCO test (G3) | **No** |
| Q6 | Deposit per-image class-id statistics (no text) for XM3600 and COCO-295 (T7) | **Yes**, where licences permit |
| ~~Q8~~ | ~~Read the one-page summary of the A-T2 tier-3 prereg before its commit (PI-1029j lists a human read as evidence for irreversible steps) ~~ | ~~11-02 morning, 10 minutes~~ (no tier 3; CC-181 r4) |
| Q7 | Admin, blocking submission: addresses, reviewer link, Zenodo DOI, and the written PASCAL-50S / OpenViIC / KTVIC permissions on file | By 11-11 |
