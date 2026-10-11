# Kế hoạch nâng VSPS từ bài hội nghị FAIR 2026 lên bài tạp chí Q2

Ngày lập: 2026-10-09 · Cơ sở: bản v9 (`FAIR_28.08.26_v9_EN_IEEE.pdf`), dữ liệu trong `data/`, hai phản biện trong `PHANBIEN.txt.txt`.
Script đo lại: `scratchpad/recall_decomp.py` (cần chuyển vào `scripts/` khi làm Giai đoạn 0).

---

## 0. Chẩn đoán: recall mất ở đâu (số liệu đo ngày 2026-10-09)

Đo trên 3.700 ảnh train KTVIC (đã chạy neutralization). Gold là các object trong 5 caption tham chiếu, khớp bằng lexicon 113 mục, cùng cách tính với Bảng IV.

| Bước pipeline | Precision | Recall | Object/ảnh | Recall mất |
|---|---|---|---|---|
| Toàn bộ mệnh đề do generator sinh | 29.1 | **68.9** | 8.33 | trần của generator |
| Bỏ REJECTED | 32.7 | 66.0 | 7.09 | −2.9 |
| Chỉ giữ SUPPORTED (P⁺) | 39.8 | **48.0** | 4.19 | **−18.0 (verifier)** |
| SUPPORTED và được chọn (selected_ids trong record = **budget 5** của Stage-1) | 43.5 | 34.5 | 2.66 | −13.5, nhưng do budget 5, *không phải* B=9 |
| Caption giám sát cuối (sft.jsonl) | 42.6 | 36.6 | 2.93 | xem bảng đính chính bên dưới |

**Đính chính 2026-10-10 (D1):** ở budget 9 (cấu hình hệ chính), selector hiện có đạt R 46.9 (P 40.7); entity-first đạt 47.4; trần (mọi SUPPORTED) là 48.0. Selector chỉ mất khoảng 1 điểm. Recall mất ở **bộ lọc `--clean-props` (khoảng −4.6)** và **rendering (khoảng −4.7)** (mẫu 575 ảnh: 45.8 → 41.2 → 36.5; sft.jsonl 35.6). D1 vì vậy chỉ cho +0.5; ưu tiên chuyển sang sửa clean-props và renderer (mục D8 mới).
| Mô hình VSPS trên tập test (Bảng IV) | 41.9 | 37.1 | 3.13 | huấn luyện không làm mất |

**Kết luận 1. Recall bị giới hạn bởi dữ liệu giám sát, không phải bởi huấn luyện.** Mô hình đạt R = 37.1 trên test, gần bằng R = 36.6 của chính dữ liệu nó học. Muốn tăng recall thì phải sửa verifier (−18 điểm) và selector (−13.5 điểm). Đổi LoRA hay thêm epoch không giải quyết được.

**Kết luận 2. "Recall 100" không đo được trên KTVIC.** Lấy một caption tham chiếu của người viết so với 4 caption còn lại (leave-one-out, tập test) chỉ được **R = 46.9, P = 85.5**. Gold suy từ caption ngắn nên thiếu rất nhiều object có thật trong ảnh. Vì vậy:
- trên KTVIC, mục tiêu hợp lý là R ≥ 57 (bằng zero-shot) và F1 vượt zero-shot;
- muốn tiến gần 100 thì phải xây **gold đầy đủ do người gán** (mục B1). Khi đó "recall 100" nghĩa là nhắc đủ mọi object có thật trong ảnh, đo được và có ý nghĩa.

**Kết luận 3 (đã đính chính 2026-10-10, D2).** Ước lượng ban đầu (khoảng 15.000 lượt nhắc, P khoảng 40%) đã đếm cả các object mà SUPPORTED vốn đã có. Chỉ tính object **mới**, nhóm relation/spatial UNCERTAIN có g ≥ 0.9 chỉ còn khoảng 4.200 object với P khoảng 30%, ngang nhóm entity UNCERTAIN. Đo thật bằng `scripts/relation_backoff.py`: mức strict cho R 48.0 → 49.2 (object mới có P 38.3%); mức lenient cho R 49.9 (P 31.9%). → D2 chỉ đáng dùng ở mức strict, sau một audit nhỏ, và không phải đòn bẩy recall chính. Câu trả lời cho R2-1 vẫn giữ: có thể neutralize relation thành entity khi bằng chứng của entity đủ mạnh.

---

## 1. Mục tiêu định lượng (tiêu chí đạt để nộp Q2)

| Chỉ số | v9 hiện tại | Mục tiêu v2 | Ghi chú |
|---|---|---|---|
| KTVIC Halluc./cap (detailed) | 1.57 | ≤ 1.6 | giữ nguyên, không đánh đổi ngược |
| KTVIC object P / R / F1 | 41.9 / 37.1 / 39.3 | ≥ 42 / **≥ 55** / **≥ 48** | F1 phải vượt zero-shot (40.7) |
| COCO P / R / F1 | 88.2 / 45.9 / 60.4 | ≥ 88 / **≥ 62** / **≥ 73** | F1 phải vượt zero-shot (70.9) |
| COCO CHAIR_s | 15.4% | ≤ 18% | |
| Recall trên gold đầy đủ (B1) | chưa có | **≥ 80**, P ≥ 90 | đây là nơi nói về mức "100" |
| Người đánh giá: faithfulness | 3.91 (zero-shot 4.17) | **> zero-shot, p < 0.05** | đang là điểm yếu lớn nhất |
| Người đánh giá: completeness / fluency | 2.64 / 3.17 | ≥ 3.8 / ≥ 4.0 | |
| Độ tin cậy verifier | 63.1% xác nhận, chỉ audit SUPPORTED | **ma trận nhầm lẫn đủ 3 trạng thái**, ≥ 600 mệnh đề, ≥ 80% xác nhận | |

Thông điệp chính của bài Q2: *VSPS-v2 giảm ảo giác **mà không** mất coverage* (vượt zero-shot về F1 và faithfulness do người chấm). Bản v9 bị gắn nhãn "precision-oriented", và phản biện R1-1 cùng H5 đều nói đó là điểm yếu.

---

## 2. Các hướng việc

### A. Kết nối pipeline (tái lập end-to-end, vòng lặp khép kín)

| # | Việc | Đầu ra | Ưu tiên |
|---|---|---|---|
| A1 | Một lệnh chạy hết: `stage1 → person_uncap → select → render → filter → SFT → eval` (Makefile hoặc `scripts/run_all.sh`), mọi siêu tham số đọc từ một file config | `make all SEED=42` tái lập đúng Bảng II/IV | P0 |
| A2 | Sửa các lệch đã biết: README không tái lập được `train_stage2`/`build_dpo_data`; dpo.jsonl có 12.806 cặp trong khi bài từng ghi 13.009; còn 35 target có ký tự CJK; danh từ có giới tính lọt qua text của mệnh đề | commit sửa + test kiểm tra hồi quy | P0 |
| A3 | Đưa `recall_decomp.py` vào `scripts/`, in bảng phân rã ở Mục 0 mỗi lần build dữ liệu (theo dõi recall và precision của từng bước) | thành một hình mới trong bài: *recall funnel* | P0 |
| A4 | **Vòng lặp tự huấn luyện (round 2)**: dùng chính mô hình VSPS-r1 làm generator trên ảnh train để sinh thêm mệnh đề, verify, hợp với tập r1, rồi SFT lại. Nhắm vào trần generator 68.9 | đường cong R/P theo số vòng (1, 2, 3) | P1 |
| A5 | Mở rộng dataset: UIT-OpenViIC làm tập thứ ba (out-of-domain, tiếng Việt) | thêm một cột trong bảng chính | P1 |

### B. Giảm ảo giác và đo cho đúng

| # | Việc | Lý do |
|---|---|---|
| B1 | **Gold object đầy đủ do người gán** cho 300 ảnh test KTVIC: 2 người gán, ghi mọi object nhìn thấy, đo κ | CHAIR KTVIC hiện chỉ là cận trên (H3). Có B1 mới đo được recall thật và mới nói được về mức "100" |
| B2 | Metric cấp mệnh đề cho attribute / count / relation (theo kiểu FaithScore): tách caption thành mệnh đề rồi chấm bằng người (200 caption) và bằng LLM-judge đã hiệu chỉnh theo người | H3; tạp chí Q2 sẽ hỏi về ảo giác ngoài phạm vi object |
| B3 | Kiểm chứng relation và spatial bằng **vùng ảnh**: detector open-vocabulary (Grounding DINO / OWLv2) cho bbox, rồi kiểm tra hình học | hiện 0/26.795 spatial được SUPPORTED, relation bị bác 42.9% (R1-2, R2-1) |
| B4 | Lọc lại dữ liệu: bỏ CJK, bỏ hedge, chặn danh từ giới tính nằm trong value của attribute/action, bỏ cụm lặp; ghi số mẫu bị loại | chất lượng đầu ra, H6 |
| B5 | Benchmark chuẩn quốc tế: AMBER (phần generative) hoặc CHAIR trên COCO với prompt tiếng Anh, để so được với các bài khác | Q2 cần so sánh ngoài phạm vi tiếng Việt |

### C. Tăng độ chính xác (precision của verifier, độ tin cậy dữ liệu giám sát)

| # | Việc | Lý do |
|---|---|---|
| C1 | **Hội đồng verifier khác họ mô hình**: Vintern-1B + InternVL2.5-8B (hoặc một VLM ngoài họ Qwen). SUPPORTED cần đủ đồng thuận; khi bất đồng thì hạ xuống UNCERTAIN | H1, H2 (cùng họ Qwen), R1-2 |
| C2 | **Audit đủ 3 trạng thái**: 600 mệnh đề, lấy mẫu phân tầng theo trạng thái × loại, 2 người gán. Báo cáo precision/recall của verifier từ ma trận nhầm lẫn | hiện chỉ audit SUPPORTED (244 mệnh đề), CI rộng |
| C3 | Hiệu chỉnh ngưỡng: thay luật "5/5 đồng ý" bằng ngưỡng chọn trên một tập dev có nhãn người (đường cong precision–recall của verifier, chọn điểm làm việc) | luật đang chặn 27.4% nhóm truy vấn vì chỉ cần một câu trả lời lệch |
| C4 | Relation chỉ được SUPPORTED khi detector xác nhận đủ cả hai đối tượng (kết hợp với B3) | R2-1: sửa thật chứ không chỉ giải thích |

### D. Tăng recall (trọng tâm; xếp theo chi phí tăng dần)

| # | Việc | Bước mục tiêu (Mục 0) | Ước lượng |
|---|---|---|---|
| D1 | **Selector ưu tiên entity**: mỗi entity SUPPORTED phải được nhắc ít nhất một lần trước khi thêm attribute; budget thích ứng theo số entity SUPPORTED của ảnh (B_detailed = 9 → khoảng 12–15). Kết quả cũ "9 → 12 không tăng (+0.02 object)" là do hàm mục tiêu ưu tiên attribute | selector, −13.5 | R dữ liệu 34.5 → khoảng 46. **Không tốn GPU để thử**: chỉ chạy lại selection rồi đo funnel |
| D2 | **Neutralization relation → entity** (Kết luận 3) | verifier, −18 | thêm khoảng 15.000 lượt nhắc object với P ≈ 40% |
| D3 | Mở rộng U_rem của neutralization: màu (`xanh dương`/`xanh lá` → `xanh` khi hai model bất đồng), đếm trên 5 → `nhiều`, lùi loài/kiểu về nhóm cha (`chó poodle` → `con chó`) | verifier | thu hồi các mệnh đề hiện đang bị bỏ vì một chi tiết |
| D4 | Hội đồng verifier (C1) cộng ngưỡng hiệu chỉnh (C3) | verifier | giảm UNCERTAIN do dao động khi sampling |
| D5 | Detector đề xuất entity bổ sung cho generator; crop/tile ảnh độ phân giải cao | trần generator 68.9 | nâng trần |
| D6 | Round 2 (A4) | trần generator | |
| D7 | (tuỳ chọn, tốn nhiều) RL với phần thưởng = coverage đã kiểm chứng − ảo giác (kiểu CCCaption), chạy bf16 trên GPU thuê | sau SFT | chỉ làm nếu D1–D6 chưa đủ F1 |
| D8 | **Giảm mất mát ở clean-props và renderer** (đo được −4.6 và −4.7 điểm recall ở B=9): xem lại luật lọc nào bỏ mệnh đề có object; renderer phải nhắc mọi object của mệnh đề đã chọn; kiểm tra bằng funnel | clean-props + rendering, −9.3 | ưu tiên số 1 sau đính chính |

**Kết quả D8 (2026-10-10, 3.700 ảnh, chưa commit):** sửa renderer (bỏ giới hạn 2 lần chuyển chủ đề, gộp entity dư thành câu "Còn có X, Y và Z", khi quá độ dài thì giữ lại object duy nhất) và sửa clean-props (gắn lại mệnh đề có mệnh đề con vào đúng chủ ngữ thay vì bỏ). Recall của caption giám sát so với tham chiếu: bản phát hành 38.0 → **42.5** (tính danh từ giới tính là "người": 48.8 → khoảng 54); P 42.6 → 40.7 (cận dưới, vì tham chiếu ngắn). Khoảng chênh 4.3 điểm = 630 dòng constrained-LM (−1.1) + renderer cũ (−3.2). Bước kế tiếp: build lại sft.jsonl, SFT 3 seed, đo trên test (cần GPU).

**Kết quả GPU D8, v2 raw seed 42 (2026-10-10, KTVIC test 558 ảnh, detailed):** P 38.1 / R 42.2 / F1 40.1, halluc/cap 2.14, 44 từ, so với bản phát hành s42 là P 41.5 / R 36.7 / F1 39.0, halluc/cap 1.57, 34 từ, và zero-shot là 31.6 / 57.1 / 40.7, 4.26, 117 từ. Recall tăng 5.5 và F1 tăng 1.1, nhưng ảo giác trên mỗi caption tăng 36%: mô hình chỉ trượt dọc đường cong P/R về phía zero-shot, không vượt lên trên đường cong đó. **Chỉ sửa dữ liệu render không đủ để đạt R≥55 với F1>40.7**; cần nâng precision của verifier (logit + ngưỡng theo loại, research_wall mục 4 #1) và recall entity ở khâu verify (mục 4 #2) trước khi train lại. v2 clean s42: P 37.6 / R 41.0 / F1 39.2, halluc/cap 2.12 — kém v2 raw ở mọi cột, nên sửa lặp tại chỗ không có lợi; giữ v2 raw.

Rendering: mở constrained-LM cho toàn bộ 3.560 mẫu detailed (hiện chỉ 650), có fallback về template. Mục đích là sửa fluency (H6) và lỗi lặp cụm.

---

## 3. Thay đổi nội dung bài (từ 8 trang hội nghị lên khoảng 25–30 trang tạp chí)

1. **Related work** mở rộng: các phương pháp dựa vào dữ liệu SFT/RLAIF (RLAIF-V, HA-DPO, HALVA, LRV-Instruction), metric caption chi tiết (CAPTURE, DetailCaps, AMBER), captioning tiếng Việt.
2. **Method**: thêm D1–D3 và C1, trình bày recall funnel là động lực thiết kế.
3. **Experiments**:
   - thêm backbone thứ hai (InternVL2.5-8B hoặc Vintern) để chứng minh phương pháp không gắn với một mô hình;
   - thêm baseline LURE / Woodpecker (post-hoc) và một phương pháp SFT-data (LRV hoặc HALVA);
   - ablation **thuần**, mỗi bước chỉ đổi một thành phần (v9 tự nhận Bảng V "không phải chuỗi ablation thuần");
   - đường cong precision–recall khi quét budget, quét chính sách hedging và quét ngưỡng τ, để thấy "độ thận trọng" là một trục điều chỉnh được;
   - B1, B2, B5, C2;
   - đánh giá người với ≥ 100 ảnh, 3 người chấm, chế độ blind thật (cắt về cùng độ dài, hoặc chấm từng mệnh đề).
4. **Phân tích lỗi** theo loại mệnh đề, kèm ví dụ thất bại.
5. **Hạn chế H1–H6**: cập nhật hạn chế nào đã được giải quyết.
6. Chọn tạp chí (đã kiểm quartile trên SJR 2025, chi tiết trong `.paper_work/Q2_LITERATURE.md`): ưu tiên *ACM TALLIP* (Q2; yêu cầu ≥ 25% nội dung mới; giảm 50% APC cho Việt Nam), sau đó *JVCIR* hoặc *Signal Processing: Image Communication* (Q2, computer vision); dự phòng *Multimedia Systems*, *Applied Intelligence*, *Machine Vision and Applications*. *Neural Computing and Applications* và *IEEE Access* là **Q1**, không phải Q2; *ACM TOMM* (Q1) là mục tiêu vươn lên nếu đạt mọi chỉ tiêu ở Mục 1.
   Lưu ý: nếu bài FAIR đã đăng kỷ yếu, bản tạp chí phải mở rộng ≥ 30% nội dung mới và trích dẫn bài FAIR (theo chính sách của từng tạp chí).

---

## 4. Lộ trình (ước tính, 1 RTX 4090)

| Giai đoạn | Thời gian | Việc | Cổng đi tiếp |
|---|---|---|---|
| 0. Nền | Tuần 1 | A1, A2, A3, B4 | `make all` tái lập v9 chênh ≤ 0.02 |
| 1. Recall không tốn GPU | Tuần 2 | D1, D2, D3 chạy offline trên verdict sẵn có, đo funnel | R dữ liệu ≥ 45, P dữ liệu ≥ 40. Không đạt thì xem lại hàm mục tiêu |
| 2. Huấn luyện lại | Tuần 3 | SFT 3 seed trên dữ liệu v2, eval KTVIC + COCO 5.000 | F1 KTVIC ≥ 45, COCO ≥ 70, Halluc./cap ≤ 1.6 |
| 3. Verifier | Tuần 4–6 | C1, C3, B3/C4 (chạy lại stage-1 khoảng 30–45 GPU-giờ), C2 audit | ma trận nhầm lẫn xong, xác nhận ≥ 80% |
| 4. Vòng 2 và mở rộng | Tuần 7–8 | A4, D5, A5, backbone thứ hai | đạt toàn bộ bảng Mục 1 |
| 5. Đánh giá người | Tuần 8–9 | B1 (300 ảnh), B2, đánh giá người v2 | faithfulness > zero-shot, p < 0.05 |
| 6. Viết bài | Tuần 10–12 | Mục 3, nội bộ phản biện chéo | nộp |

Nếu sau Giai đoạn 2 F1 vẫn dưới zero-shot: định vị bài là *"một trục thận trọng điều chỉnh được"*. Khi đó đường cong P–R của VSPS phải **trội Pareto** so với VCD, Self-Correction và Instructed zero-shot ở mọi điểm, đây là phương án dự phòng vẫn đủ cho Q2. Nếu không thì mới làm D7.

---

## 5. Việc làm ngay (đã có thể chạy)

1. `python scripts/recall_decomp.py <stage1_neutralized>`, lưu bảng Mục 0 làm baseline.
2. Viết selector entity-first (D1) như một hàm thay thế trong bước selection, chạy lại trên verdict sẵn có, so funnel.
3. Viết `relation_to_entity` (D2), đặt cạnh `scripts/person_uncap.py`, theo cùng tiêu chí đã đăng ký trước: bằng chứng đồng thuận, không hỏi lại mô hình.

---

## 6. Cập nhật 11/10/2026 (CPU, máy GPU không truy cập được)

Đo trên 3.701 bản ghi stage-1 đã lưu. Proxy là P/R của caption mục tiêu so với tham chiếu train; v2raw cho proxy 40,6/42,4 và mô hình đạt 38,1/42,2 trên test, nên proxy này dự báo tốt.

- **Bộ lọc vị ngữ quan hệ** (`relation_predicate`): giữ 5.704/21.406 mệnh đề. Tất cả 468 mệnh đề SUPPORTED bị loại trong mẫu kiểm tra đều hỏng. Chỉ 2,5% mệnh đề được chọn là quan hệ, nên bộ lọc giúp precision chứ không giúp recall.
- **`unanimous_uncap.py`** (chạy sau person_uncap): tập SUPPORTED đạt R 48,0 → 50,7 với P 39,8 → 39,3.
- **Budget không phải điểm nghẽn**: tăng 9 → 15 chỉ được +0,7 R.
- **Dữ liệu v3** (`data/supervision_v3`): F1 strict 41,6 (v2raw 41,5); R lenient 56,6 (v2raw 54,2). Lỗi trong caption mục tiêu: giới tính chưa kiểm chứng 12,2% → 0,3%, "một số X" đọc thành danh từ 14,2% → 0,4%, đại từ thừa 2,8% → 0. Nguyên nhân gốc: `NUMBER_MARKERS` thiếu "một số".
- **Trần recall strict** cho mô hình trung tính giới tính là 83,7, nên giới tính không phải giới hạn.

Kết luận: chỉ sửa dữ liệu mục tiêu thì recall strict của mục tiêu mới quanh 42–44. Muốn đạt R ≥ 55 (strict) thì phải tăng chính tập SUPPORTED, gồm verifier logit (T0.5), xếp hạng thực thể trước khi cắt `--max-entities` và kênh detector, và việc nào cũng cần chạy lại stage-1 trên GPU. Việc GPU kế tiếp: huấn luyện v3 seed 42 (lệnh trong `data/supervision_v3/README.md`), rồi đo T0.5 bằng `VinternAdapter.yes_no_logit` (đã viết, chưa chạy).
