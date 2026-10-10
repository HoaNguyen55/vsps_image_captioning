# Bức tường nghiên cứu VSPS — tổng hợp 11 agent (2026-10-10)

Nguồn chi tiết: `01..11_*.md` cùng thư mục. Mọi con số "dự kiến" bên dưới là ước tính của agent, **chưa đo**.

## 1. Trùng lặp

- **Không có bài HIGH** ở 10/11 hướng. Ngoại lệ: hướng RL (07) — reward precision+recall theo claim đã có (BalCapRL 2605.07394, CCCaption, ClaimDiff-RL, CuRe) → **không được quảng bá GRPO-VSPS là ý tưởng reward mới**.
- Medium, phải trích dẫn và đối chiếu:
  | Bài | Vì sao gần | Điểm khác của VSPS |
  |---|---|---|
  | REVERSE (NeurIPS 2025, 2504.13169) | gắn nhãn cụm confident/unconfident | REVERSE backtrack lúc suy luận; VSPS trung tính hóa dữ liệu, suy luận một lượt |
  | IntroConformal (EMNLP 2026, 2609.01375) | lọc claim bằng ngưỡng hiệu chỉnh | không verifier ngoài, không 3 trạng thái, không tạo dữ liệu SFT |
  | Entity-Faithful Repair (ACM MM 2026, 2608.00994) | kiểm chứng điều khiển chất lượng giám sát | viết lại quanh thực thể phát hiện, không mệnh đề có kiểu / 3 trạng thái |
  | ProVision (2412.07012), CompCap (ICCV 2025) | văn bản tổng hợp "đúng theo cấu tạo" | VSPS render từ mệnh đề *đã kiểm chứng* trên ảnh thật |
  | SSAV (2609.17269), VGD (2607.27823) | kiểm chứng vật thể bằng vùng / sửa khi giải mã | chạy lúc suy luận, nhị phân |
  | DEJIMA (2512.00773), ViX-Ray (LREC 2026) | dữ liệu Nhật kiểm với detector; fact nguyên tử tiếng Việt | không đo ảo giác / chỉ để đánh giá |
- Mối đe dọa định vị: SimLoss (2609.00591: một lượt ≈ pipeline đa bước, rẻ 20×), CapRL++ (SFT là giới hạn) → bài cần một đoạn trả lời trực tiếp.
- Khẳng định còn giữ được: **chưa có CHAIR/POPE/benchmark ảo giác vật thể tiếng Việt**; MHR (TOMM 2026) không có tiếng Việt (08 đã kiểm 13 ngôn ngữ) → "first for Vietnamese detailed captioning" đứng vững.

## 2. Bài bắt buộc trích thêm (ngoài danh sách novelty/)

REVERSE, IntroConformal, Entity-Faithful Repair, ProVision, BalCapRL, SimLoss, Precision-or-Recall? (Findings EMNLP 2024), Geigle et al. EMNLP 2024 (grounding ít giảm ảo giác), VL-RewardBench + Multimodal RewardBench (judge ~65–72% → 63,1% là bình thường), yes-bias (Findings ACL 2026 2601.12430; VaPR 2510.01700), Lupascu et al. Information Fusion 2026, M²CQA (Findings ACL 2026), SEA-VL (ACL 2025), MTVQA, Sci. Rep. 2026 Urdu/Arabic QLoRA Qwen2.5-VL, Rethinking-CD (greedy ≥ VCD trên Qwen2.5-VL → giải thích kết quả VCD).

## 3. Chuẩn reviewer Q1/Q2 2026 (08) và khoảng trống của v10

| Chuẩn | v10 |
|---|---|
| ≥2 backbone (thường 3) | **thiếu** (chỉ Qwen2.5-VL-7B) |
| ≥4 baseline training-free (VCD + OPERA/DoLa…) | thiếu OPERA, DoLa; nên thêm SPIN/ONLY, PAI |
| CHAIR + POPE, AMBER cho caption chi tiết | **thiếu POPE, AMBER** |
| mean ± sd 3 seed | có |
| human eval ~200 ảnh, 3 người, κ | đang chờ object gold 300 ảnh |
| thời gian/bộ nhớ suy luận | cần bảng GPU-hours (mẫu trong 05) |
| kiểm định thống kê | đã vượt chuẩn (bootstrap, Wilcoxon) |

Baseline tiếng Việt reviewer sẽ đòi: zero-shot Vintern-3B (đã đăng ký trong repo, chưa chạy), Qwen3-VL-8B, InternVL3.5-8B; và SFT trên caption zero-shot Qwen **không kiểm chứng** (09).

## 4. Cải tiến xếp hạng (lợi ích / chi phí trên 1× RTX 3090)

| # | Việc | Hướng tác động | Chi phí | Nguồn |
|---|---|---|---|---|
| 1 | **Verifier đọc logit P(Có)/P(Không) một lượt** thay K=5; mã hóa ảnh 1 lần, gộp batch câu hỏi; chỉnh ngưỡng theo loại mệnh đề trên 244 mục audit (ngưỡng hiện là `v1.0-doc07-UNTUNED`) | cost 80 s → ~2–25 s/ảnh; precision SUPPORTED > 63,1%; bỏ điểm yếu "untuned" | ~0 GPU để thử trên mục audit; chạy lại verify + SFT | 04, 05, 06 (3 agent độc lập cùng đề xuất) |
| 2 | **Thu hồi recall ở khâu verify/cap, không phải generator**: funnel R 65,4 (đề xuất) → 61,9 (bỏ REJECTED) → 36,2 (SUPPORTED); 41% entity rơi UNCERTAIN; `--max-entities 8` cắt 86,9% ảnh không xếp hạng → xếp hạng entity trước khi cắt (A1), thêm detector OWLv2/Florence-2 làm kênh bằng chứng thứ 2 (A2, không bao giờ REJECT vì thiếu box) | recall ↑ (hướng tới R≥55) | A1 ~0; A2 ~1 GPU-h / 3.700 ảnh | 03 |
| 3 | Probe "biết nhưng không nói" cho object gold bị bỏ sót | xác định recall mất do budget/render hay do nhận thức | ~1 GPU-h | 02 |
| 4 | Coverage guard cho renderer constrained-LM (chỉ nhận nếu phủ mọi object của template, nếu không thì fallback), áp cho cả 3.560 target | độ trôi chảy ↑, recall không thấp hơn template | 2–5 GPU-h (pilot 100 ảnh trước) | 09 |
| 5 | Budget 9 → ~14 + probe ℓ1 trên từng object mention lúc suy luận (kiểu VGD) | recall ↑, CHAIR ↓; mất claim "single-pass" → báo cả hai chế độ | 1–2 GPU-h + 1 lần QLoRA | 01 |
| 6 | Backbone thứ 2 (InternVL2.5-8B hoặc Qwen2-VL-2B) × 3 seed trên cùng sft.jsonl | đáp ứng chuẩn khó nhất | ~11 GPU-h | 08 |
| 7 | Baseline rẻ: DoLa/ICD/M3ID trong `scripts/baselines.py`; beam search (SAKED: −4 CHAIR_s) | đủ số baseline | ~1 GPU-h mỗi cái (kiểm `dola_layers` với Qwen2.5-VL trước) | 01, 08 |
| 8 | English-pivot CHAIR cho COCO + sửa 8 mục rủi ro trong `coco80_vi.json` (vẫn "BẢN NHÁP"); một câu "caption không phải bản dịch" | chặn đòn phản biện về COCO | <1 GPU-h | 10 |
| 9 | GRPO reward tra cứu verdict offline (G=4, GDPO, chặn hedge/length/CJK), khởi từ zero-shot và từ SFT; reward trên ½ lexicon, báo trên ½ còn lại; trl 0.19.1 không hỗ trợ ảnh → vòng lặp riêng trong `train_stage2.py` | đường trực tiếp nhất tới R≥55 & F1>40,7 | 6–8 GPU-h/run | 07 |
| 10 | Thêm metric không tốn GPU: AMBER Cover/Hal/Cog, recall salient vs exhaustive, tỷ lệ output không phải tiếng Việt, so sánh ở cùng độ dài | đủ metric 2026 | 0 | 02, 09, 10 |

Không khuyến nghị: DoRA/PiSSA (không hơn LoRA, 2606.10428); cắt visual token của captioner (tăng ảo giác/giảm recall, AgilePruner ICLR 2026); GCN+ConceptNet sinh caption (11).

## 5. Đã sửa ngay

- `scripts/object_gold_score.py`: chế độ lenient để một "người" phủ mọi lớp người trong gold (thổi phồng recall của caption trung tính hóa). Nay mỗi mention mơ hồ phủ đúng một lớp; thêm assert trong `--self-check` (pass).

## 6. Đồ thị tri thức (11) — hướng cho dữ liệu UIT

Một nửa cũ (KG ngoài → bộ sinh caption: ~1,4% bài captioning 2025, đi ngang/giảm), một nửa đang nổi (đồ thị để **kiểm chứng/đánh giá/giảm ảo giác LVLM**: 0 → 21–26 bài/năm, chủ yếu hội nghị đỉnh). Tiếng Việt trống: chưa có scene graph, parser, SPICE/graph-metric tiếng Việt. Ý nên làm trước: đồ thị mệnh đề đã kiểm chứng + graph P/R cho caption tiếng Việt với quy tắc phụ thuộc kiểu DSG, trên UIT-OpenViIC/KTVIC.

## 7. Theo dõi định kỳ

Chạy `python3 .paper_work/research_wall/watch.py` mỗi tháng (arXiv + OpenAlex, chỉ in bài mới so với lần trước). Truy vấn Google Scholar / Semantic Scholar alert đầy đủ ở mục (e) của từng file 01–10.
