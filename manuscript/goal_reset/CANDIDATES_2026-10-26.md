# Method candidates for the goal reset (2026-10-26)

**Status.** This is a PROPOSAL for the goal reset requested in PI-1026q. It is not a preregistration and not a ruling.

**How it was made.**
- It was written 2026-10-26 (≈ 24:00 VN) from committed or backed-up result files, `goal_reset/AUDIT_2026-10-26.md`, `goal_reset/DIAGNOSIS_2026-10-26.md`, `alt_plan/ALT_PLAN_AGENT_2026-10-26.md`, the decisions LOG (CC-114, CC-118, PI-1026l/o/q), the WORKFLOW_LOG and the NCS proposal v2 (MT4).
- I opened no caption text, prediction text or test reference. Split files were read for image and annotation counts only.
- I used no GPU and no machine.

**Labels.**
- **SPENT-TEST**: a set that has already been used as a test. A number on it is descriptive: it can motivate a direction but cannot confirm one.
- **DEV**: development data.
- **unmeasured**: an estimate that no log in the repo supports.

## Tóm tắt (tiếng Việt)

- **Mục tiêu cần đặt lại cho đúng chỗ có khoảng trống.**
  - Ở chế độ *ngắn*, SFT trên tham chiếu người đã vượt zero-shot rất xa: F1 trên gold instance COCO 49.5 → 65.5, P ≈ 99.
  - Ở chế độ *chi tiết*, zero-shot vẫn có độ phủ cao hơn SFT (R 61.9 so với 50.3) nhưng ảo giác nhiều hơn (CHAIR_i 9.5 so với 0.5). Cả hai hệ đều chưa đạt "độ phủ của zero-shot với độ chính xác của SFT".
  - **Đích ứng dụng rõ và đo được:** caption chi tiết tiếng Việt *trội Pareto* so với zero-shot **cùng backbone** (đối chứng chốt trước, không chọn trên test). Cụ thể: recall không thấp hơn (lề −2) và CHAIR_i trên COCO-80 giảm ít nhất 3 điểm. Đây đúng là "ít ảo giác hơn ở cùng độ phủ" mà PI yêu cầu.
  - Trên gold COCO-80 có khoảng trống (P 90.5 → 99.5), nhưng một phần có thể là lỗi matcher.
  - Trên gold OIV7 độc lập, trần chỉ còn khoảng 0.6 F1 (E′ H2, chế độ chi tiết). Vì vậy OIV7 chỉ dùng làm guard không-kém-hơn.
- **Kiểm tra P2 của FAIR:** P2 (không kiểm chứng) cũng sụp còn 41 từ. Vậy mất độ phủ chủ yếu do *công thức mệnh đề có ngân sách*, không phải do bộ kiểm chứng. K2 phải huấn luyện trên caption nguyên vẹn, và xác suất trước của K2 giảm còn khoảng 0.5.
- **Xếp hạng (xác suất trước có kết quả dương rõ):**
  1. **K1** (khoảng 0.85, chế độ ngắn): SFT trên toàn bộ gold tiếng Việt (KTVIC + UIT-ViIC + OpenViIC, mục tiêu fuse đa tham chiếu) với backbone mạnh hơn (Qwen3-VL-8B, InternVL3.5-8B). Hướng này chưa từng chạy.
  2. **K2** (khoảng 0.5; là headline nếu qua Gate 0/0b/1): tự chưng cất có hiệu đính bằng gold người, tiếp nối phương pháp mệnh đề kiểm chứng của Nguyen et al. (FAIR 2026). Lấy caption chi tiết zero-shot trên ảnh COCO có nhãn instance, chỉ xoá các mệnh đề có đề cập mà gold nói là vắng mặt, giữ mọi thứ khác, rồi SFT.
  3. **K3:** G-RL (CC-114), khởi tạo từ K2.
  4. **K6:** mô hình nhỏ 2–4B triển khai được (một nhánh của K1/K2).
  5. **K4:** DPO on-policy, gold quyết định, khớp độ dài (một nhánh trong K3).
  6. **K5:** giải mã hoặc kiểm chứng lúc suy luận. Loại: bằng chứng 0–3 điểm, và D sở hữu hướng này.
- **Ràng buộc cứng.**
  - Không còn tập test tiếng Việt tươi có tham chiếu tiếng Việt. "Chất lượng" theo CIDEr tiếng Việt **không thể** xác nhận trong một lần nhìn mới. Chỉ recall/F1/CHAIR trên gold instance (vi + en) và precision đã kiểm chứng trên OIV7 là xác nhận được.
  - Tập tươi: KV-primary 4,224 (đã giao cho G-RL, PI-1026l) và **OIV7 val** (41,620 ảnh, nhãn người kiểm chứng, nhóm chưa dùng; phải loại ảnh NoCaps val và XM3600).
- **Khuyến nghị:** một bài K1 + K2 (+ K6 làm nhánh), thuộc MT4.1. Primary là KV-primary (cần PI chuyển KV từ G-RL sang, PD-GR-1), với OIV7 val làm thước đo độc lập chống "học vẹt 80 lớp". G-RL chuyển sang OIV7 test (125,436 ảnh). Pilot dev (UIT-ViIC val 924 đầy đủ) khoảng 4–6 GPU-h trên M3 đang rỗi, nếu PI cho phép (PD-GR-3).

---

## 1. What a "clear positive applied result" can mean here

### 1.1 The gap is in detailed mode, and it is two-sided

On UIT-ViIC test 231 (SPENT-TEST, descriptive only) with COCO-80 instance gold, Qwen2.5-VL-7B, the systems compare as follows.

| Mode | System | true obj/cap | P | R | F1 | CHAIR_i | Source |
|---|---|---|---|---|---|---|---|
| short | zero-shot | — | 99.2 | 33.0 | 49.5 | — | `data/results/uitviic/object_prf-short.txt::uitviic_zeroshot` |
| short | in-domain P1 | 1.37 | 99.4 | 41.8 | 58.9 | 0.6 | `data/results/uitviic_ind_test/object_prf-short.txt::uitviic_p1_s42` |
| short | in-domain fuse2 | 1.60 | 99.5 | 48.9 | 65.5 | 0.5 | same `::uitviic_fuse2_s42` |
| detailed | **zero-shot** | 2.07 | **90.5** | **61.9** | 73.6 | **9.5** | `data/results/uitviic/object_prf-detailed.txt::uitviic_zeroshot` |
| detailed | in-domain fuse2 | 1.65 | 99.5 | 50.3 | 66.8 | 0.5 | `data/results/uitviic_ind_test/object_prf-detailed.txt::uitviic_fuse2_s42` |
| detailed | KTVIC-trained fuse2 (cross-domain) | 1.56 | 93.0 | 47.5 | 62.9 | 7.0 | `data/results/uitviic/object_prf-detailed.txt::uitviic_fuse2_s42` |
| detailed (COCO, FAIR) | zero-shot vs FAIR VSPS | — | 80.5 → 88.2 | 63.3 → 45.9 | 70.9 → 60.4 | — | FAIR v10 Table IV |

**Reading.**
- **Short mode.** In-domain SFT already dominates zero-shot. There is no hallucination headroom, since P ≈ 99, as DIAGNOSIS §2.1 says.
- **Detailed mode.** No system dominates. Zero-shot sees more, and SFT is cleaner.
  - Zero-shot proves the backbone can perceive about 12 recall points more than SFT shows.
  - The 9 points of CHAIR_i suggest real precision headroom under *complete* COCO-80 gold, which reference incompleteness cannot explain. Part of it may still be matcher error on long captions (negation, generic nouns; see A's `journal_draft/appB_matcher_sensitivity.md`). Gate 0 (K2) measures how much is left after the edit.
  - The two papers before this one sat at opposite corners of this frontier. FAIR VSPS bought precision and lost recall. B's fuse2 bought recall and lost length.

**Two checks against this framing (zero GPU, done 2026-10-26).**
- **FAIR P2 collapsed too.** FAIR's P2 (same recipe, *unverified* candidate propositions) also collapsed: 41 words and 3.80 objects per caption, against 117 words and 6.54 for zero-shot, with KTVIC R 42.0 against 57.1 (FAIR v10 Tables II–IV, via pdftotext).
  - So VSPS's coverage loss comes mostly from the **recipe**, propositions rendered under a budget of B_detailed = 9 (FAIR §IV), and not from the verifier.
  - K2 must therefore train on **whole captions with clause deletion only**, never recomposed propositions. Even so, no repo evidence yet shows that SFT on whole self-generated captions keeps length. This lowers K2's prior (§3).
- **Independent gold leaves little headroom.** E′ H2's ceiling under OIV7 verified gold used **detailed** captions: deleting every wrong mention gains only 0.637 F1 (Qwen2.5-VL) and 0.601 (InternVL3) on xm_dev300 (172 labelled images), against 7.5 / 7.1 under KTVIC references (`.session_backup/2026-10-25/h2_precheck/ceiling.json::ceiling.by_cell`, DEV).
  - So under an independent open-vocabulary gold on Open Images photos, detailed-mode headroom is close to zero in F1 terms.
  - The COCO-80 headroom above, if real, does not transfer to the instrument the group would use to answer the "you only learned 80 classes" critique.
  - Consequence: OIV7 is a **non-inferiority guard**, not a superiority test (§2, §5).

**Target for the reset (proposed).**

> A Vietnamese detailed captioner whose object recall is non-inferior to the **same-backbone** zero-shot model (margin −2.0; the comparator is fixed before any test, so there is no best-of-arms pick on test) while its object hallucination rate (CHAIR_i, COCO-80 instance gold) is lower by ≥ 3.0 points, confirmed once on an unspent set, with OIV7 verified precision and recall **non-inferior** (no superiority claim, per the E′ H2 ceiling below).

- This is "fewer hallucinations at matched coverage" in the PI's sense.
- It is also the form that survives A's count control: count stays the same and fewer of the objects are false. So the matched-count F1 test of CC-114 W1 is *favourable* to this target rather than lethal to it.

### 1.2 What cannot be confirmed

- **No fresh Vietnamese test with Vietnamese references remains.** KTVIC test, UIT-ViIC test, OV-test and all of XM3600 (600 + 2,500 + 500) are spent. A reference-based Vietnamese quality claim (CIDEr-D) can be DEV or descriptive only.
- **VieCap4H** (healthcare, VLSP 2021) has human Vietnamese references, but I could not find whether its test references were released (search 2026-10-26). It is not counted.
- **What can be confirmed with one look:**
  - instance-gold P/R/F1/CHAIR (Vietnamese via matcher v2; English via the CHAIR synonym list);
  - CIDEr/SPICE for the **English** arm against the 5 English COCO references;
  - OIV7 verified precision and verified recall.

## 2. Confirmation sets (one look each)

| Set | Size (full official split) | Gold | Status | Who may use it |
|---|---|---|---|---|
| COCO Karpathy val, KV-primary | 4,224 (5,000 minus ids already used by A; CC-114) | complete COCO-80 instances; 5 English refs | unspent | **G-RL paper (PI-1026l)**. Reassigning it is a PI decision (PD-GR-1) |
| **Open Images V7 validation** | 41,620; minus NoCaps-val images (NoCaps val is drawn from OI val and is C-EN's secondary set) and any XM3600 image ids. Disclosed, ID-only exclusion | 618,184 human-verified image-level labels (390,797 positive, 227,387 negative), 9,668 trainable classes (Open Images V7 facts page, fetched 2026-10-26) | **never used by the group** (the only OIV7 use so far is the labels of XM3600 images, in A). The gatekeeper must confirm this with an ID scan | proposed: the K-paper's independent instrument |
| Open Images V7 test | 125,436; minus NoCaps-test and XM3600 ids | 2,003,748 verified labels | unused | proposed: G-RL's primary if KV moves to the K-paper |
| *OIV7 instrument dependency* | — | Verified positives include abstract labels that a caption would not name. Before any prereg, fix the scored class subset (proposal: the 600 boxable classes) and freeze the vi→OIV7 matcher vocabulary. A's matcher was built for the XM3600 label set and may not cover that subset: extend it on DEV only, with the sha pinned. | — | — |
| Flickr30K Entities test | 1,000 | phrase–box chains, 5 English refs | reserved (alt-plan D3, thesis backlog) | not used here |
| NoCaps val | 4,500 | English refs | C-EN secondary | not used here |
| Karpathy test, KTVIC test, UIT-ViIC test, OV-test, XM3600 | — | — | SPENT | never |

**Dev data (full splits only, per the full-dataset rule).**
- UIT-ViIC val, 924 images, COCO-instance gold. It is the G-RL dev set under CC-118, so sharing it must be disclosed.
- OpenViIC dev, 2,011 images, Vietnamese references. C used it as OV-dev-A/B, so it is descriptive only.
- No 200-, 300- or 500-image pools.

**Consequence.**
- Only **two** applied papers can each get a fresh, one-look confirmation from what exists:
  - one on KV-primary;
  - one on OIV7 (val or test).
- Every candidate below that needs KV belongs to the same fixed-sequence family as the others that need it.
- Six separate papers would be both salami and reuse of the one look.

## 3. Candidates

GPU-h figures use measured rates where they exist.
- **Inference.** Fine-tuned Qwen2.5-VL-7B on M3 (RTX 3090): 0.55 s/img short, 0.56–0.84 s/img detailed (`WORKFLOW_LOG.md` "A W4 on M3", parity and run rates).
- **Zero-shot detailed captions** are near the token cap (99.7% for Qwen3-VL; `data/results/n_m3/caphit_result.json`). For them I assume **2.5 s/img (unmeasured)**.
- **SFT.** Qwen2.5-VL-7B QLoRA, 7,538 samples (3,769 × 2 epochs), took 6,993 s = 1.078 samples/s (`.session_backup/machines/n3/ncs-data/runs/p1assist_s43/metrics.jsonl::train_runtime`). The GPU model of n3 is not recorded, and these were short targets. Detailed targets are taken as ×1.5 (**unmeasured**).

### K1. All-gold multi-reference SFT on a stronger backbone ("Strong-SFT")

| Item | Content |
|---|---|
| Method | QLoRA SFT of **Qwen3-VL-8B** (primary) and **InternVL3.5-8B** (cross-family) on **all existing Vietnamese human gold**: KTVIC train 3,769 + UIT-ViIC train 2,532 (KV-overlap removed, CC-114 Q2) + OpenViIC train 9,088 = 15,389 images. Short mode uses one human reference per sample. Detailed mode uses B's fuse2 multi-reference targets. Exclusions are fixed in advance and disclosed: pHash near-duplicates against every test set listed in §2. OpenViIC train contains 401 KTVIC-test images (B-x11), which is harmless because KTVIC test is never looked at again. **English arm:** the same recipe on UIT-ViIC-en train (2,532), giving the English comparison on the same images. |
| Why it should work (evidence) | (i) Changing the supervision is the largest lever the group has measured: short-mode instance F1 +9.4 (P1) to +16.0 (fuse2) over zero-shot at P ≈ 99 (§1.1). (ii) More images: +9.40 CIDEr-D per doubling, CI lower bound 4.87 (`t3_4_s5_data_scaling/scaling.json::decision.b`, DEV, one seed per size). K1 is ≈ 4× B's 3,769. (iii) A fine-tuned non-Qwen2.5 backbone has **never been run** (DIAGNOSIS §3 row 6b). B1 died on a guard that the main backbone would also have failed. (iv) The FAIR VSPS bar is low: its COCO F1 of 60.4 is already below zero-shot (70.9). |
| Expected gain | Short: F1 +10 to +16 over the best zero-shot at non-inferior P. Prior **≈ 0.85** for H "K1 − best zero-shot ≥ +2.0 F1, P margin −1.0" on KV. Detailed: **not expected to dominate**. Expect R below zero-shot by about 8–12 and CHAIR_i lower by about 8 (§1.1), i.e. the same trade-off again. K1 alone does not meet the §1.1 target. |
| Confirming set | KV-primary (vi + en), one look. Secondary: OIV7 val, verified precision and recall. |
| GPU-h (one 3090) | SFT: 30,778 samples per seed per backbone ≈ 7.9 h short + about 4 h detailed (×1.5, unmeasured) ≈ 12 h. 2 backbones × 2 seeds ≈ **48 h**. English arm 2 × 3 h ≈ 6 h. Evaluation on KV: about 10 systems × 4,224 × (0.55 + 0.84 s) ≈ 16 h, zero-shot detailed rows about +9 h. Total **≈ 80 GPU-h**. OIV7 val evaluation is shared with K2. |
| Risk | Low on the short-mode claim. Medium on novelty: "fine-tune on in-domain data" alone is not publishable as a method, so K1 is the strong baseline and the data/backbone axis of the K-paper, not its headline. Qwen3-VL short CJK leakage of 0.03 (`b1_qwen3vl/step1_dev300_guard.json`) needs a language gate at decode. |
| Falsifier | K1 − best zero-shot short F1 has a lower bound ≤ 0 on KV, or verified precision on OIV7 is below the base. |
| Salami | B reports fuse2 and data size **descriptively on KTVIC under B's protocol** (B-x14, S5). K1 uses fuse2 as an ingredient, cites B and makes no KTVIC claim. Its contributions are new: multi-dataset, two new backbones, complete-gold confirmation and the English arm. Not A, C or D. |
| MT4 / home | MT4.1. It is the data/backbone axis of the K-paper. On its own it is a resource-style note (weak venue). |

### K2. Gold-verified self-distillation that keeps coverage (follows Nguyen et al., FAIR 2026) — top pick

| Item | Content |
|---|---|
| Method | (1) The base VLM (Qwen3-VL-8B; then InternVL3.5-8B) writes **zero-shot detailed Vietnamese captions** for COCO training images that carry **human instance gold**. (2) A deterministic editor removes only the clauses whose COCO-80 mention is **gold-absent**. It uses matcher **v1**, while scoring uses v2 and OIV7, so the edit instrument is not the test instrument (CC-114 W-rule). Everything else is kept, including non-COCO content, so length and coverage are preserved. (3) QLoRA SFT on edited captions (detailed mode) mixed with K1's human data (short mode). **Arm K2b, the privileged teacher:** the teacher's prompt also lists the gold-present classes whose area is at least a fixed threshold, to raise recall, then the same edit is applied. The student never sees gold. **Scale arm K2-L:** the image pool grows from UIT-ViIC train (2,532) to the full Karpathy train + restval (112,322 after C-EN's 965 exclusions; COCO train/restval images all have instance gold). It is run only if the lean arm passes its dev gate. |
| Why it should work (evidence) | (i) The §1.1 frontier: zero-shot detailed R 61.9 / CHAIR_i 9.5. Removing gold-absent mentions from the *targets* keeps nearly all true mentions, because only false ones are cut, and removes the hallucinated ones. The student therefore imitates a high-recall, high-precision target that no current system produces. (ii) This is exactly FAIR's failure, fixed. VSPS cut *uncertain* propositions with an AI verifier: 25.4% of SUPPORTED were wrong (AUDIT F6) and recall fell 57.1 → 37.1. Its own ablation recovered recall when uncertain items were kept, 23.3 → 37.7 (DIAGNOSIS §4.1). Human gold removes the verifier error. (iii) Targets are model-native text, so the SFT shift is small. Literature: HalluciDoctor cleans instruction data of hallucinations; LURE and Woodpecker revise after generation; ShareGPT4V shows caption *quality* in SFT data drives detail. Narrowed after the W23 search (K14-1; `manuscript/prereg/2026-10-28_mt4_kv/PRIOR_ART_W23.md`, STIC and ReCaption), setting novelty, not method novelty: no prior work found removes clauses from a backbone's own detailed captions by a deterministic rule against human COCO instance gold, trains the same backbone on them by plain SFT, and shows fewer hallucinations than its zero-shot output at matched coverage, with an unedited self-training control, in Vietnamese. |
| Expected gain | On KV, detailed mode, vs the same-backbone zero-shot (fixed comparator): ΔR −3 to +1, ΔCHAIR_i −4 to −7, F1 +1 to +3. Projected from §1.1, assuming the student reaches 60–80% of the target's precision gain (unmeasured). The F1 ceiling is small: if P → 100 at R 61.9, F1 is 76.5 against 73.6, i.e. +2.9. The headline is therefore CHAIR_i at matched recall, not F1. K2b: ΔR +2 to +6 more (unmeasured). On OIV7: ≈ 0 (E′ H2 ceiling 0.6 F1), so non-inferiority only. Prior **≈ 0.45–0.55** for the §1.1 target. It was lowered from 0.6–0.7 after the FAIR P2 check (§1.1): SFT on self-generated text has collapsed length once in this group, though under a proposition budget that K2 does not use. |
| Main risk | (a) **Length collapse** as in FAIR P2 (41 words). K2 trains on whole captions; Gate 0b and the Gate 1 length guard test this first. (b) The student learns *style* but not *grounding*, and still names absent objects at other images' rates. Gekhman et al. (2405.05904) show tuning on unknown content raises hallucination; K2b carries this risk most. (c) **COCO-80 gaming:** the claim is bound to COCO-80. Independent gold (OIV7) shows almost no headroom (§1.1), so it cannot show the gain transfers; it can only show nothing got worse. Mitigations: edit matcher v1 vs score matcher v2, a guard on non-COCO noun phrases per caption (kill if they fall by > 10% vs zero-shot), and OIV7 non-inferiority. A reviewer may still call it an 80-class result, and the paper must say so. (d) Self-generated Vietnamese captions are **AI-made training text**, which the no-new-gold rule may cover (PD-GR-2): the text is AI-made, the verification is human gold, and no AI label is used as evidence. |
| Falsifier | On KV: ΔR lower bound < −2.0, or ΔCHAIR_i upper bound > −3.0 (no ≥ 3-point reduction), or the matched-count F1 lower bound ≤ 0 (A's estimator), or Vietnamese-only rate < 99%, or mean words < 75% of zero-shot. On OIV7 val: verified precision or verified recall below zero-shot beyond margin −1.0 (non-inferiority fails). |
| Dev gate (before any test) | **Gate 0 (≈ 0.7 GPU-h, 2.5 s/img unmeasured):** zero-shot detailed captions on the full UIT-ViIC val 924, then the editor on CPU. This gives the *target ceiling* (P, R, CHAIR_i of the edited captions). STOP if the edit lowers R by > 1.0 or CHAIR_i by < 5.0 (if the COCO-80 headroom is mostly matcher error, this is where it shows). **Gate 0b (CPU):** STOP if edited targets average < 90% of zero-shot words. **Gate 1 (≈ 4–5 GPU-h):** K2 lean, one seed, scored on val 924. GO if ΔR ≥ −2.0, ΔCHAIR_i ≤ −3.0, Vietnamese-only ≥ 99%, and mean length within ±25% of zero-shot. SESOIs are re-checked against the measured val-924 bootstrap CI half-width before commit (DIAGNOSIS §5.4). **Pool hygiene:** K2-L's pool excludes every UIT-ViIC train/val/test id and every KV id (UIT-ViIC images are COCO-2014 images and likely sit inside Karpathy train/restval). This keeps dev decisions on val 924 uncontaminated. |
| GPU-h | Lean: teacher 2,532 × 2.5 s ≈ 1.8 h. SFT with K1 data plus 2,532 detailed ≈ 13 h per seed. 2 seeds × 2 backbones ≈ 55 h. K2b +28 h. **K2-L:** teacher 112,322 × 2.5 s ≈ 78 h, plus SFT ≈ 40 h per seed at 8B (both unmeasured; vLLM may cut the teacher cost severalfold). Run K2-L on one backbone and one seed, then a second seed if Gate 1 is strong. Evaluation: KV shared with K1. OIV7 val about 37k × 0.84 s ≈ 9 h per fine-tuned system, ≈ 26 h per zero-shot system; 4 systems ≈ 70 h. **Lean paper ≈ 150 GPU-h; with K2-L ≈ 300 GPU-h**, which means two machines for about 5–7 days. |
| Salami | **FAIR:** same family (verified SFT data). It changes the verifier (human instance gold instead of an AI tri-state verifier), the decision (cut only gold-absent mentions, keep the rest), the domain (COCO images), the backbones and the evaluation (complete gold, OIV7). It must be framed as the follow-up that fixes FAIR's coverage loss, citing FAIR. A conference-to-journal extension needs the venue's policy check. **B:** none (no KTVIC claim). **A:** tool only. **C:** none (no retrieval). **D:** training-time, not inference. **G-RL:** the reward is not used. K2's editor is the same gold signal as G-RL's reward, so the G-RL paper must treat K2 as its strong baseline, not re-claim the signal. |
| MT4 / home | **MT4.1 exactly.** NCS v2 l.60 says "tinh chỉnh có giám sát trên chú thích đã kiểm chứng, mở rộng dữ liệu giám sát của bài FAIR 2026 để vượt giới hạn độ phủ của nó". MT4.3 is touched through the coverage-preserving target. Venues: Neural Computing and Applications or Pattern Recognition Letters (from `cfp/04`; quartiles as listed there); TALLIP as fallback. |

### K3. G-RL: on-policy RL with a recall-bearing human-gold reward (CC-114 D1)

| Item | Content |
|---|---|
| Method | As in CC-114 / ALT_PLAN D1: RLOO or GRPO with a reward of COCO-80 presence F1 (instance gold), a length window, a Vietnamese gate and a repetition gate. **Change proposed here:** initialise from K2 (or K1) instead of a weak SFT-ref model, and keep K2 as the arm to beat. |
| Evidence | The reward pays for recall, which is where the headroom is (§1.1). On-policy sampling matters: OPA-DPO (2501.09695); Metric-Driven RL (2610.14976, IEEE Access) uses an object score covering correctness *and* coverage. Caption RL in English gains with judge or QA rewards (CapRL 2509.22647, CCCaption 2602.21655, SC-Captioner 2508.06125). Against: the group's only RL run (CIDEr reward) was KILLed, with CI ±8 on dev300 (`data/results/rl/g1_cn_v3_s42/gate.json`). The same 7B setup hit 24.9 GB of reserved memory. |
| Expected gain | Over its SFT init, +1 to +4 F1 at non-inferior P (unmeasured; no matched-count number exists in the literature I read). Prior **≈ 0.35–0.5**. On top of K2 the margin is smaller, because K2 already harvests the gold signal. |
| Confirming set | KV-primary under PI-1026l. If PD-GR-1 moves KV to the K-paper, then **OIV7 test** (125,436 minus NoCaps-test and XM ids), whose open-vocabulary instrument is independent of the COCO-80 reward. |
| GPU-h | CC-118: Gate 1 at full data ≈ 25–40 GPU-h; the full paper ≈ 86–100 GPU-h (ALT_PLAN, built on an unmeasured 25 s/img; Gate 0 must measure it). OIV7 test evaluation: 125k × 0.84 s ≈ 29 h per fine-tuned system. |
| Risk | High: memory, reward hacking through list-style captions, and a small margin over K2. |
| Falsifier | As CC-114 H1, plus G-RL − K2 lower bound ≤ 0, which would mean on-policy RL adds nothing over gold-edited SFT. That would be reported. |
| Salami / MT4 | Its own paper (MT4.3), later, per PI-1026o. It needs K2 as a baseline, so K2 is published first. |

### K4. On-policy, gold-labelled DPO at matched length (arm, not a paper)

- **Method.** Sample k captions from the K2 model on training images and form pairs *within a length bucket*: the chosen caption has no gold-absent COCO-80 mention, the rejected one has at least one. Then DPO with length regularisation (R-DPO, 2403.19159) or SimPO (2405.14734). Neighbours: CHAIR-DPO (2508.20181), HA-DPO (2311.16839), mDPO (2406.11839), RLHF-V (2312.00849), RLAIF-V (2405.17220).
- **Evidence against.**
  - FAIR's 4-bit DPO broke the adapter (41.4% CJK).
  - B's count-matched DPO/RFT FAILed (S3).
  - E5 DPO frontier residual −1.97.
  - Likelihood displacement (2410.08847).
- **Prior and cost.** Prior **≈ 0.2–0.3** for ≥ +2 F1. It is cheap (≈ 15 GPU-h), so it belongs as the K3 mechanism arm (H1-mech: RL vs RFT vs DPO under one gold signal), as CC-114 already specifies.
- **Confirming set.** Inherits K3's set, inside K3's fixed sequence.
- **Falsifier.** DPO − K2 init has a lower bound ≤ 0 on CHAIR_i at matched recall, or CJK/English leakage exceeds base + 1 pp.
- **Salami.** Differs from B S3, which was off-policy and count-matched, and from FAIR, which was 4-bit and off-policy. It is reported only inside K3.
- **Home.** K3 paper, MT4.2.

### K5. Inference-time decoding or verification (excluded)

- **Evidence.**
  - VCD ≈ 0 (FAIR Table III; 2311.16922).
  - UPE-MBR and P-M6b KILLed.
  - The verifier selection arm gave +1.51 F1 at −2.62 CIDEr.
  - Under verified gold, E′ H2's ceiling was 0.6 F1.
- **Ownership.** The family belongs to D (deferred).
- **The one opening.** Detailed-mode precision headroom (§1.1) could revive *selective* decoding. But K2 attacks the same headroom at training time with no inference cost, which is better for application.
- **Decision.** Excluded. MT4.5 remains as a baseline row inside the K-paper (VCD on the same backbone, ≈ 3 GPU-h).

### K6. Deployable small model (arm of K1/K2)

- **Method.** The K1 and K2 recipes on Qwen3-VL-2B/4B, with Vintern-1B (2408.12480) as a Vietnamese-native reference.
- **Evidence.** In-domain SFT moves short CIDEr 29 → 150 on the same backbone (DIAGNOSIS §3 row 1). That effect is far larger than the zero-shot gap across 3B–8B models (KTVIC short CIDEr 17.5–34.0; `b_n1_run.json::LBB-D2`).
- **Prior.** ≈ 0.7 for "4B K2 ≥ 8B zero-shot on short F1 and detailed CHAIR_i".
- **Cost.** About 20 GPU-h.
- **Why it matters.** It is the clearest *application* row: on-device Vietnamese captioning. It is an arm of the K-paper, not its own paper.
- **Confirming set.** Inherits the K-paper's set (KV-primary; OIV7 val as guard).
- **Falsifier.** On KV, the lower bound of K6-4B minus Qwen3-VL-8B zero-shot is ≤ 0 on short F1, or K6-4B's detailed CHAIR_i is not below the 8B zero-shot.
- **Salami.** None beyond K1/K2; it is a size axis.
- **Home.** The K-paper, MT4.1 (application).

## 4. Ranking

The score is prior × applied value × feasibility on 3090s, each rated 1–5.

| Rank | Candidate | Prior of a clear positive | Applied value | Feasibility | Score | Role |
|---|---|---|---|---|---|---|
| 1 | **K1 Strong-SFT** | 4.5 (≈ 0.85, short) | 3: expected trade-off in detailed | 5 | **67** | safe applied PASS; data/backbone axis of the K-paper |
| 2 | **K2 gold-edited self-distillation** (+ K2b, K2-L) | 3 (≈ 0.45–0.55) | 5: matched-recall hallucination cut, fixes FAIR | 4 | **60** | headline of the K-paper if Gate 0/1 pass |
| (folded) | K6 small model | 3.5 | 4 | 5 | (70) | arm of the K-paper; not ranked on its own |
| 4 | K3 G-RL | 2 (≈ 0.35–0.5) | 4 | 2.5 | 20 | its own later paper (MT4.3), with K2 as baseline |
| 5 | K4 on-policy DPO | 1.5 | 3 | 4 | 18 | arm of K3 |
| 6 | K5 inference-time | 1 | 2 | 4 | 8 | excluded; VCD baseline row only |

- **K6** scores highest but cannot stand alone: it is K1/K2 at a smaller size, so it is folded in.
- **K1 vs K2.** After the FAIR P2 check, K1 overtakes K2 on prior. K2 stays the headline because only K2 can meet the PI's "fewer hallucinations at matched coverage". Gate 0/0b decide this on DEV within about 1 GPU-h. If either stops K2, the K-paper's headline falls back to K1 + K6. That is a weaker but still positive applied result: the short mode beats zero-shot SOTA and VSPS, and a 4B model is deployable.

## 5. Recommendation

**One applied paper, "K-paper" (MT4.1).**

- **Arms.**
  - Zero-shot SOTA open VLMs (Qwen3-VL-8B, InternVL3.5-8B, Qwen2.5-VL-7B), plus VCD on the primary backbone.
  - FAIR VSPS as published.
  - K1 (2 backbones × 2 seeds).
  - K2 and K2b, then K2-L if Gate 1 is strong.
  - K6 at 4B.
  - English arm.
- **Primary family, fixed sequence on KV-primary, one look.**
  - H1: K1 > same-backbone zero-shot (Qwen3-VL-8B, fixed now), short F1, P margin −1.0. Other zero-shot models are reported, not tested.
  - H2: K2 meets the §1.1 target versus the same-backbone zero-shot in detailed mode: R margin −2.0, CHAIR_i ≤ −3.0, and matched-count F1 lower bound > 0.
  - H3: K2 > K1 on detailed F1.
  - H4-en: the H2 pattern in English, with CIDEr/SPICE against the 5 English references.
  - H5: K6-4B ≥ 8B zero-shot.
- **Secondary.**
  - On OIV7 val (one look): K2's verified precision and recall are non-inferior to zero-shot (margin −1.0). There is no superiority claim, because of the E′ H2 ceiling.
  - Descriptive Vietnamese CIDEr on spent sets, labelled SPENT-TEST.

**Why this ranks first.**
- It reuses only the levers that moved the metrics by 5–120 points: supervision, data and backbone.
- It targets the one place both axes can improve at once: detailed mode under complete gold.
- Its headline claim is the PI's request.
- Its cheapest step (Gate 0, ≈ 0.7 GPU-h) shows on DEV whether the target exists before any training.

**PI decisions needed.**
- **PD-GR-1. KV-primary.** Move it from G-RL (PI-1026l) to the K-paper, and give G-RL OIV7 test. *Recommended:* the K-paper has the higher prior and should take the in-domain set. G-RL benefits from an open-vocabulary test that is independent of its COCO-80 reward. The alternative is the K-paper on OIV7 val only, which is out of domain for COCO-trained data and gives a lower prior (C's XM failure is the precedent).
- **PD-GR-2. AI-generated training text.** K2 trains on the backbone's own captions after human-gold editing. Is this allowed under the no-new-gold rule (no AI label used as evidence)? Machine-translated COCO captions are the same question at larger scale. *Recommended:* allow K2 with disclosure. Translated COCO is not recommended, since K2-L reaches the same image scale with gold-verified objects and no translation.
- **PD-GR-3. Machine and timing.** Gate 0 + Gate 1 (≈ 5–6 GPU-h) on M3 now, while it is idle and before the C-EN test (12-01..12-04)? CC-118 keeps M3 for C-EN and puts the G-RL pilot on M4. Full runs (≈ 150–300 GPU-h) on two rented 3090s. Under PI-1026o the K-paper would need a submission slot: either G-RL's slot (after C), or merged with G-RL as one MT4 paper with the RL arm (K3) as H6. *Recommended:* K-paper first and G-RL after; it is the PI's call.
- **PD-GR-4. Primary endpoint.** CC-114 W1 made matched-count F1 a co-primary. *Recommended:* keep it as a co-primary for H2, where it is designed to be passable. Do not apply it to H1 (short mode), where gains are count gains by construction and P ≈ 99 makes "more correct objects" the applied benefit.

**Before any prereg.**
- The gatekeeper runs an ID-only scan that confirms OIV7 val/test, minus NoCaps and XM3600, has no prior group use.
- The arXiv scan is re-run for gold-edited self-distillation in captioning (the field moves weekly).
- Gate 0 measures s/img for zero-shot detailed decoding and replaces every "unmeasured" figure above.

## 6. Identifier checks

**arXiv.** One `id_list` call and one follow-up to export.arxiv.org, 2026-10-26. **39/39 resolved, titles matched.** Raw XML is in the session scratchpad (`cand_verify/arxiv.xml`, `a2.xml`).

| Group | IDs |
|---|---|
| Backbones | 2511.21631 Qwen3-VL; 2508.18265 InternVL3.5; 2503.19786 Gemma 3; 2509.18154 MiniCPM-V 4.5; 2408.12480 Vintern-1B; 2502.13923 Qwen2.5-VL; 2305.14314 QLoRA |
| RL | 2402.03300 DeepSeekMath (GRPO); 2503.20783 Dr.GRPO; 2503.01785 Visual-RFT; 2509.22647 CapRL; 2602.21655 CCCaption; 2605.20278 ClaimDiff-RL; 2603.09160 RubiCap; 2508.06125 SC-Captioner; 2610.14976 Metric-Driven RL; 2312.03631 MOCHa; 2608.20362 multilingual verifier bias; 2609.26097 MODL |
| Preference | 2501.09695 OPA-DPO; 2405.17220 RLAIF-V; 2312.00849 RLHF-V; 2311.16839 HA-DPO; 2402.11411 POVID; 2406.11839 mDPO; 2508.20181 CHAIR-DPO; 2403.19159 R-DPO (length); 2405.14734 SimPO; 2410.08847 likelihood displacement |
| Data / hallucination | 2311.12793 ShareGPT4V; 2311.13614 HalluciDoctor; 2310.00754 LURE; 2310.16045 Woodpecker; 2405.05904 new-knowledge hallucination; 2311.16922 VCD; 2004.06165 Oscar; 1809.02156 CHAIR; 1812.08658 nocaps; 2209.01304 vieCap4H team paper |

**DOIs** (api.crossref.org, 2026-10-26): 10.1109/ACCESS.2026.3723028 (Metric-Driven RL, IEEE Access) OK; 10.1109/CVPR52734.2025.00992 (OPA-DPO, CVPR 2025) OK.

**Not verified.**
- VieCap4H test-reference availability.
- The Open Images V7 split sizes come from the official facts page (storage.googleapis.com/openimages/web/factsfigures_v7.html), which was fetched but has no DOI.
- Venue quartiles are as listed in `cfp/04_rolling_journals.json` and were not re-checked.
