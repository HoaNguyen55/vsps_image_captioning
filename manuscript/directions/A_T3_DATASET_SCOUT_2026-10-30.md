# A-T3 dataset scout: a fresh set for Paper A's non-Qwen confirmatory replication (2026-10-30)

Written 2026-10-30 ~01:55Z (08:55 VN). Scouting only: AI opinion, no ruling, no prereg. Nothing decoded, no model
run, nothing committed, no paper or prereg file edited, no download > 1 GB, no e-mail in any request.

## Tóm tắt (tiếng Việt)

- **Đề xuất chính: COCO val2017 phần "tươi" (3,746 ảnh; còn khoảng 3,737 sau khi loại trùng Flickr).** Gold =
  nhãn instance COCO-80 (vét cạn trên 80 lớp, đúng từ vựng của bộ matcher A), cùng 5 caption người.
  - Đã loại: 593 ảnh Karpathy test (A và C-EN đã dùng), 608 ảnh Karpathy val (thuộc MT4/D) và 53 ảnh CHAIR-500 (N9).
  - Không ảnh nào từng được chấm điểm.
  - Khoảng 3,640 ảnh nằm trong **bộ nhớ truy hồi** của C: C-EN và C-T1 dùng caption của chúng làm ví dụ, chưa từng
    giải mã hay chấm điểm. "Memory có tính là đã dùng không" là **câu hỏi cho judge**, không phải tôi quyết.
- **Premise đo trước, không cần output** (chỉ gold, tính trên laptop, xem §6 về custody):
  - nhãn/1 caption = **2.16** (≥ 2, đạt);
  - nhãn ≥ 2·(1 caption ∩ nhãn): 1.17 (đạt);
  - nhãn/hợp 5 caption = 1.40 (< 2, chỉ mô tả).
  - Trên Karpathy restval (pool dev, 30,504 ảnh) gần như y hệt: 2.09 / 1.13 / 1.39.
- **Cảnh báo quan trọng (đã đối chiếu với prereg):** A4 đã đăng ký so nhãn với **hợp toàn bộ tham chiếu**
  (P50 PREREG l.225: voc20 − refs50).
  - Trên COCO, tỉ lệ đó là **1.40 < 2**. Nếu A-T3 giữ cổng premise 2x của A-T1, bước label **dạng đã đăng ký
    TRƯỢT premise**.
  - Chỉ biến thể hẹp L − R1 (2.16) qua cổng. Chọn biến thể này là câu hỏi cho judge, vì dễ bị đọc là "chọn cái
    qua".
  - X4 không có cổng 2x trong p50x.py, nhưng chỉ còn một mức (k = 1 so với hợp 5) và Σ|R5|/Σ|R1| = 1.54, nên
    power thấp. Tier 1 sẽ trả lời.
  - O2 và X5 (1.17) kiểm được. O2 là phần meta-review coi là gần như cơ học.
  - Vậy COCO chắc chắn chỉ mang **O2, X5 và bước label dạng k = 1**. Hai dạng rủi ro của A (A4 so với hợp tham
    chiếu, X4) thì một trượt premise, một yếu power. PI quyết có đáng ~23 GPU-h không.
- **Custody:** premise 2.16 được tính trên laptop từ chính gold của test dự kiến (val2017). Dùng restval cũng ra số
  scout gần như y hệt. Judge cần biết điều này (§6).
- **Họ mô hình ngoài Qwen:** InternVL3-8B, Gemma-3-4B, Aya-Vision-8B, LLaVA-OV-7B, Idefics3-8B. Pin có sẵn trong
  các registry A-N2, L1-b, C-T1.
- **GPU-h:** khoảng 12.5 cho tier 3, khoảng 3.4 cho tier 1, khoảng 6.7 cho tier 2; tổng ≈ 23, cap đề xuất 30.
- **Dự phòng: VG paragraph test (Krause 2017).** Có 1,262 ảnh không thuộc COCO, hoàn toàn chưa dùng. Nhưng
  **premise TRƯỢT** trên train: 1.18 và 0.73, giống ADE20K (1.24). Mỗi ảnh chỉ có 1 đoạn văn, nên không kiểm được
  O2/X4; chỉ còn AD-1 ở dạng mô tả. Nói thẳng: nếu judge coi memory là "đã dùng" thì **không có bộ nào vừa tươi vừa
  đạt premise**. Khi đó A-T3 không có dữ liệu xác nhận, PI phải chọn: nới luật hoặc không có GPU mới.
- **Bị loại:**
  - NoCaps val: đã dùng (C-EN một lần nhìn, vg-mamf, W25). NoCaps test không công khai tham chiếu.
  - Flickr30K: toàn bộ 31,014 ảnh đã giao cho C-T1. Gold Entities lại sinh từ chính caption.
  - ADE20K: PREMISE_NOT_MET.
  - PASCAL: đã dùng.
  - OIV7 val: thuộc L2-P1. OI test quá lớn (126k).
  - DCI: test chỉ 112 ảnh.
  - AMBER: không có tham chiếu người.
  - LVIS: chỉ làm rung phụ trên cùng ảnh val2017.

## 1. What A-T3 must replicate (copied from A's registered families)

- **Label step (A4 / AD-1 form):** `slope[label | V] − slope[ref | V] > 0`, rule `sign_gt_0`. Registered on XM3600
  (PASS, verified precision), second backbone (weak PASS) and PASCAL-50S (FAIL −2.29 [−5.15, +0.61]).
- **O2:** the slope rises at every added reference rung (P50-O2: five steps, all PASS; G2B-O2 on cv295).
- **X4:** a salient few-reference gold gives a lower slope than size-matched random deletions from the
  many-reference consensus (P50 companion, PASS p ≤ 0.001).
- **X5 / AD-2:** the same null with the label gold as the complete set. Evaluable only if Σ|L| ≥ 2 Σ|N ∩ L|. It was
  NOT_EVALUABLE on PASCAL-50S.
- **Measured premise (A-T1 §3, the gate ADE20K failed):** Σ|L| / Σ|N| ≥ 2 and Σ|L| ≥ 2 Σ|N ∩ L|, computed
  output-free before any decode.

A one-reference-per-image set can carry only the label step and X5. O2 and X4 need a multi-reference ladder.

**Checked against the registrations.**

- **A4 = N1-XM-4 = P50-A4:** slope(refs1_randk) < slope(refs_all) < slope(label). Part 2 compares the label with
  the **full reference union** (P50 PREREG l.225, l.162). The 2x premise is A-T1's addition (A-T1 §3), not part of
  A4. The XM3600 PASS had OIV7 2.04 < ref union 2.35 (PD-28).
- **X4 (companion RULE l.73, l.77; p50x.py l.172-179):** no 2x gate. It is NOT_EVALUABLE only if the null's 2.5 and
  97.5 percentiles coincide.
- **X5 (p50x.py l.189):** has the gate Σ|complete| ≥ 2 Σk.

Reviewer items it answers (manuscript/reviews/A_META_REVIEW.md):

- **4:** the claim is scoped to XM3600. A-T3 adds a second dataset.
- **5(b):** the A4 premise "was assumed, not measured". A-T3 measures it first.
- **6:** system dependence. A-T3 uses five non-Qwen families, three of them new to A: Gemma-3, Aya, Idefics3 (P50
  dropped Idefics3).
- **9:** dependence on the verified-precision estimand. COCO-80 instance labels are exhaustive on V, so no
  verified-precision step is needed.

## 2. Candidate table

The ledger sources searched were:

- .session_backup/2026-10-13/decisions/LOG.md (844 lines);
- CC-108, CC-153, CC-160 and CC-181;
- the prereg dirs C-EN, C-T1, A-T1, G0, P50, L1-b and MT4/K2.

Overlaps were computed from these id files:

- Karpathy `data/datasets/karpathy/dataset_coco.json`;
- `cen_memory_allowed.tsv` / `cen_coco_kval.tsv` / `cen_nocaps_val.tsv`;
- `c_t1_f30k_lists.json`;
- `data/coco_probe/chair500_ids.txt`;
- `data/lb/sets/cv295.tsv`;
- the UIT-ViIC jsons;
- the XM3600 600/500/2,500 id files (union 3,600);
- the VG `image_data.json` (coco_id, flickr_id);
- OpenImages 2018_04 image CSVs (val, test, train-boxable; Flickr photo id parsed from `OriginalURL`), streamed
  and not stored.

| Set | Ledger status (computed) | Premise (output-free) | Hypotheses testable | Licence / size | Tier-3 GPU-h (5 fam × 2 prompts) | Verdict |
|---|---|---|---|---|---|---|
| **COCO val2017 fresh** | **5,000 total.** Spent: 593 Karpathy test (A COCO-5000, C-EN one look, cv295 = 295 of them). Owned: 608 Karpathy val (KV, MT4/D). Used: 53 CHAIR-500 restval (N9). **Fresh 3,746**: never scored. 3,693 of the 3,799 restval ids are in C's retrieval memory (`cen_memory_allowed`; C-T1 COCO memory). No UIT-ViIC overlap (all train2017). Flickr-id hits: 5 Flickr30K (C), 3 NoCaps val, 1 other OIV7 val, 0 of the 1,855 XM3600 ids that map. | L/R1 **2.162**, L/(2·R1∩L) **1.173**, L/R5 1.404 (n = 3,799 pre-CHAIR-cut) | **O2**, **X5** (1.17), label step **k = 1 variant** (2.16). The registered A4 form (L vs R5 union) fails the A-T1 premise (1.40). X4 has a single level (R1 vs R5) and Σ|R5|/Σ|R1| = 1.54, so power is low | COCO annotations CC BY 4.0, images Flickr per-image licences. annotations_trainval2017.zip 241 MB, val2017 images 788 MB (per-file fetch possible) | ≈ 12.5 | **PRIMARY** (pending the memory ruling) |
| **VG paragraph test** (Krause et al. 2017) | 2,489: 51 Karpathy test, 38 Karpathy val, 1,138 COCO train/restval (C memory), 1,262 non-COCO. Flickr-id hits: 2 OIV7 val, 44 OI train, 2 OI test, 0 XM3600 (of the mapped 1,855), 1 Flickr30K (a COCO image). No VG use anywhere in repo preregs (PORTFOLIO B4 plans VG relations on COCO restval only). | **FAIL** on train non-COCO (n = 7,454): L/N **1.179**, L/(2·N∩L) **0.734** (same matcher both sides, objects.json v1.4) | label step only (1 paragraph per image), X5 NOT_EVALUABLE, no O2/X4 | VG CC BY 4.0. Paragraph files: licence not stated on the mirror (to verify). objects.json.zip 55 MB, images per-file URLs | ≈ 8.3 (all 2,489) / 4.2 (1,262) | **BACKUP**, descriptive at best |
| NoCaps val | Spent: C-EN one look (S_NC FAIL), vg-mamf 1,000, W25 4,457 | n/a | n/a | n/a | n/a | out |
| NoCaps test | References hidden (eval server) | n/a | none | n/a | n/a | out |
| Flickr30K (+ Entities) | All 31,014 assigned by C-T1: carve 1,000, memory 28,000, val 1,014, test 1,000. The test is C-only (PI-1029h Q3). Entities gold = phrases of the same captions, so not independent of the references. | n/a | none | n/a | n/a | out |
| COCO Karpathy test / val | A + C-EN / MT4-D KV | n/a | n/a | n/a | n/a | out |
| COCO Karpathy restval (30,504) | C memory, CHAIR-500 has 372 | L/R1 2.094, L/(2·R1∩L) 1.134, L/R5 1.390 | all | as COCO | ≈ 102 (full split) | dev pool only |
| LVIS v1 val | COCO 2017 images (same constraints). Federated, so not exhaustive, but it lists verified negatives. | not computed | secondary rung (verified precision, OIV7-like) on the same fresh val2017 ids | CC BY 4.0, lvis_v1_val.json.zip (size to verify) | +0 (same decodes) | secondary rung |
| ADE20K val | A-T1 PREMISE_NOT_MET on train D1 (1.244) | failed | — | — | — | out (re-using it = forking path) |
| OIV7 val / OI test + LN | Val reserved to L2-P1 (PI-1029h Q4). Test is 125,436 images, so the full-split rule puts it above 100 GPU-h. | — | — | — | > 100 | out |
| PASCAL VOC + other captions | Only PASCAL Sentences / 50S exist, both on the same 1,000 VOC2008 images (spent, P50) | — | — | — | — | out |
| DCI (SA-1B) | Unused. The test set is 112 base images. Mask labels come from the caption annotators. Images need the SA-1B click-through. | — | — | CC BY-NC | — | out |
| AMBER | Has no human references (A-T1 §0.1) | — | — | — | — | out |

## 3. Gold completeness: how the numbers were made (scouting, gold-only, no verdict)

**Matcher.** The frozen `score_coco_probe.en_classes` with `load_synonyms()` (= `score_g2b MATCH["coco80"]["en"]`)
was applied to both sides:

- VG object names;
- COCO instance category names (∩ COCO-80);
- paragraphs and captions.

No synsets were used on one side only.

**COCO.**

- R1 = the first listed caption, as a scout shortcut. A prereg uses the frozen `draw()` (rng 1). R5 = the union of
  the first five.
- L = the instance categories present (any instance, crowd included).
- Pinned public files:
  - annotations_trainval2014.zip sha256 031296bb…;
  - annotations_trainval2017.zip sha256 113a836d…;
  - fresh id list sha256 81b826c5… (3,746 ids, scratchpad only).
- The quick public-statistics argument agrees with these numbers. COCO has about 2.9 categories per image. One COCO
  caption names about 1.3 COCO-80 classes, which gives ≈ 2.2 against one reference and < 1.5 against five.

**VG.**

- objects.json.zip v1.4 sha256 efa45606…; image_data.json.zip b87a9491….
- Mirror of the Krause splits: github.com/chenxinpeng/im2p/data, because cs.stanford.edu refused the connection.
  test_split.json aa93f163…, train c1a5685d…, val d7e735db…, paragraphs_v1.json 19473770… (full file deleted).
- The counts (14,575 / 2,487 / 2,489) match the widely cited Krause et al. 2017 split. The paper itself was not
  re-read here: verify before any prereg.
- The VG premise fails because VG object boxes were drawn for things the region describers mentioned. The label rung
  is therefore not exhaustive by construction, and a ~61-word paragraph already names most of the same COCO-80
  classes.

**Real ratio for a prereg (G0 style).** The tier-0 `gold` step should repeat this on its own D1 on the dev host. On
the test set, it should run on m3 before the first decode and be logged in LOG.md:

- pinned files, frozen matcher, ids only;
- Σ|L|, Σ|R1|, Σ|R5|, Σ|R1∩L|, Σ|R5∩L| and per-class differences;
- `stage` refuses if the premise fails.

## 4. GPU-h (one RTX 3090)

**Basis.** P50 measured 17,027.9 GPU-s for 14,000 decodes plus 16 smoke runs (7 A-N2 models × short/detailed ×
1,000 images, M1 3090), i.e. **≈ 1.2 s per decode** including loads. Aya-8B and Gemma-3-4B have no English
captioning timing yet. I assume the same ±50%; C-T1's Aya ledger will give a real number.

| Tier | Data | Decodes (5 fam × 2 prompts) | GPU-h (est.) | Machine role |
|---|---|---|---|---|
| 0 | gold premise on D1 / D2 / test (CPU) | 0 | 0 | m4 for D1/D2; m3 for the test |
| 1 dev-explore | D1 = 1,000 Karpathy restval ids not in val2017 and not in CHAIR-500, ordered by sha256(id) | 10,000 | ≈ 3.4 | m4 (dev-only) |
| 2 dev-confirm rehearsal | D2 = next 2,000 (exact tier-3 analysis, run once). Predicted P(PASS) on N = 3,737 must be ≥ 98%. | 20,000 | ≈ 6.7 | m4 |
| 3 one look | val2017 fresh (≈ 3,737 after pre-fixed exclusions) | ≈ 37,400 | ≈ 12.5 | m3 (test-capable), test images and gold only on m3 |
| Total | | | ≈ 23 (cap 30) | |

Adding the two pinned A-N2 extras (LLaVA-1.5-7B, SmolVLM2-2.2B) gives 14 runs, as P50 had, and raises the total by
about 40%. With only 10 runs the slope CIs are wider (the slope is OLS across runs).

**Models and pins.** No new download is needed for the pins; weights still need fetching per host.

- InternVL3-8B-hf 259a3b64, LLaVA-OV-7B 0d506805 and Idefics3-8B fddb4ff7 are in the A-N2 registry
  (2026-10-19_a_n2_lvlm_gold_ladder.json).
- Gemma-3-4B-it 093f9f38 is in l1b_registry.json.
- Aya-Vision-8B d7601ac8 is in c_t1_registry.json.
- A `register` step must copy the Gemma and Aya pins and their venvs, since neither is in A-N2.

Host state after the 10-30 re-rent:

- InternVL3-8B-hf comes with setup_gpu.sh on both hosts.
- Aya is fetched on M1 only (OPS-1030m-op, PI token per command).
- Gemma-3 and Idefics3 depend on the L1-b fetch on M2 (OPS-1030s-op says step-4 downloads were done; check the
  list).
- LLaVA-OV-7B is not known to be on any current host.

## 5. A-T3 prereg sketch (primary: COCO val2017 fresh)

1. **Rulings needed first.**
   - (a) Is C's retrieval memory (captions used as in-context examples, images never decoded or scored) "spent" for
     A? Irreversible tier, ≥ 92.
   - (b) The full-split rule: the 1,263 excluded val2017 ids (593 + 608 + 53 + about 9 Flickr-id hits) are spent or
     reserved images, not leakage. Is a pre-fixed spent-set exclusion allowed, with no "full 5,000" result beside it?
     Scoring those images would itself be a second look.
   - (c) Lift or confirm CC-153 r4 for the Flickr-id/pHash check against XM3600.
2. **Sets** (ids only, fixed before any decode).
   - Test = val2017 minus Karpathy test/val, minus CHAIR-500, minus Flickr-id hits in Flickr30K, NoCaps val or OIV7
     val, minus pHash/dHash ≤ 10 near-dups of XM3600, PASCAL-50S, NoCaps val and Flickr30K test (B-R1/W25 rule).
   - 1,745 XM3600 ids are outside OI train-boxable/val/test, so the Flickr-id map does not cover them and pHash has
     to.
   - D1/D2 come from Karpathy restval minus val2017 minus CHAIR-500.
3. **Gold.**
   - L = COCO-80 instances (primary).
   - R1 = caption 1 and R5 = all five, with the k-ladder 1, 2, 5 through a frozen `draw()` (rng 1, 20 replicates).
   - LVIS verified positive/negative = secondary verified-precision rung (descriptive).
4. **Hypotheses (copied).**
   - **H1 label step, registered form (copied):** slope[L] − slope[R5] > 0 (`sign_gt_0`). Under A-T1's premise
     gate this form fails (1.40 < 2), so it can be run only if the judges rule that A4's original no-premise form is
     the replication target. A FAIL would then be uninterpretable, as at PASCAL.
   - **H1′ narrower variant (not "copied"):** slope[L] − slope[R1] > 0 clears the gate (2.16 / 1.17). Choosing H1′
     over H1 is a **judge question**, since it can read as picking the comparator that passes. If H1′ is used,
     report H1 beside it with its CI.
   - **H2 O2:** each rung step 1→2→5 is > 0.
   - **H3 X4:** R1 versus 1,000 size-matched random deletions from R5. PASS iff observed < null 2.5th percentile.
     There is no 2x gate, but R5 is only 1.54 × R1 in size and has one level (P50 had two levels on 50
     references). Tier-1 power decides.
   - **H4 X5:** gold = R1∩L, complete = L, same null. Evaluable iff Σ|L| ≥ 2 Σ|R1∩L|.
5. **SESOI.** A's registered rules are sign rules (`sign_gt_0`) with no SESOI, and A-T1 had none. If the judges
   want one, +2.0 F1 per ln M is an **unsourced AI suggestion** (below P50-O2's smallest step, +3.51). Set it before
   tier 1 and never after.
6. **Multiplicity.**
   - The joint registered claim = H1 (or H1′) ∧ H3 (intersection–union, each at one-sided 0.025).
   - H2 and H4 are secondary.
   - Holm applies over {H1, H3} for any single-test claim (A-T1 §5 wording).
7. **Three tiers (PI-1029n/q).**
   - Tier 1: dev-explore on D1. Outcomes are NOT_REPRODUCED, PASS_LOW_POWER or PROCEED.
   - Tier 2: rehearsal on D2 with the exact tier-3 code. It proceeds only if the image-bootstrap P(PASS on 3,737) is
     ≥ 98% for both H1 and H3.
   - Tier 3: one look on m3. Fail at the rehearsal = never touch the test.
   - All FAILs are reported briefly (papers-aim-for-pass).
   - Exposure: the P50 8-gram check (COCO captions are in most LVLM training mixes) is a disclosure, not a verdict
     input.
   - **Dev/test exposure mismatch.** train2017 = train2014 + val2014 − val2017, so the D1/D2 restval slices are
     inside train2017, which most LVLM mixes include, while val2017 is the usual held-out split. This weakens the
     tier-2 → tier-3 P(PASS) transfer. Ruling: either accept and disclose it, or carve dev from val2017 itself under
     PI-1026c Q2 (which shrinks the test).
8. **Placement.** One paragraph in §6.4, one sentence in §6.6, Table 1 rows, details in the supplement (A-T1 §0
   pattern). The paper sentences are fixed in the prereg for each outcome.

**Backup sketch (VG paragraph test, non-COCO 1,262).**

- Only H1 at k = 1 is possible. The premise is known to fail on train (1.18), so a tier-0 gate under A-T1's rule
  stops it with no GPU.
- Running it anyway needs a ruling that the original A4 form (no premise; XM3600 passed with OIV7 2.04 < ref
  union 2.35) is the replication target. Any FAIL would then be uninterpretable, as at PASCAL.
- Recommendation: do not run it as confirmatory. If (a) goes against COCO, tell the PI that no fresh set meets both
  rules.

## 6. Custody and disclosures (scouting incurred these; for the judge)

- **Paragraphs.** `paragraphs_v1.json`, which includes the VG test and val paragraphs, was on the laptop scratchpad.
  Mean word counts for test (60.9) and val (61.7) were printed. Nothing else was read from them. The file was deleted
  after the train-only extract, and the train extract was deleted too.
- **COCO.** val2017 instances and captions (the proposed tier-3 gold) were read on the laptop to compute the premise
  numbers above. This was output-free, aggregates only, and no caption text was stored. Both COCO annotation zips and
  objects.json were deleted.
- This departs from A-T1's custody pattern, where test gold stays on m3. The tier-3 rule must recompute the premise
  on m3. I recommend the judge treat the 2.162 as a disclosed pre-registration fact, not a gate result.
- **Still in the scratchpad.** Kept: VG image_data and the split id files, OI id→Flickr-id maps, the fresh id list
  and the XM id union. All are ids only.

## 7. Recommendation

1. **Primary: COCO val2017 fresh (≈ 3,737), as a narrower replication.**
   - It is the only unscored candidate with a multi-reference ladder.
   - Under A's own gates it carries O2, X5 (1.17) and the k = 1 label-step variant (2.16), with five non-Qwen
     families.
   - It does **not** cleanly carry A's two risky forms. The registered A4 (label vs reference union) fails the A-T1
     premise (1.40), and X4 has a single low-power level.
   - The PI decision is whether this narrower replication is worth ≈ 23 GPU-h.
   - Cost: ≈ 23 GPU-h over three tiers.
   - Risk: ruling (a) on C memory, and reviewers may see COCO as A's home domain. Mitigation: present it as the
     system-dependence replication (item 6) plus the measured premise (item 5b), not as a new-domain claim.
2. **Backup: VG paragraph test (non-COCO 1,262), descriptive only.** It is fully fresh, but the premise fails and it
   has one reference per image. If (a) is NO, the honest outcome is "no fresh set meets both rules". That is a PI
   decision.
