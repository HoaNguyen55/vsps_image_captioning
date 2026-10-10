# Kế hoạch lớn: Image captioning tiếng Việt với Transformer + Đồ thị tri thức (bản nháp vòng 1, 2026-10-10)

Nguồn: 20 báo cáo `01..20_*.md` trong thư mục này + `../research_wall/11_knowledge_graph_captioning.md`. Mọi con số chi phí/hiệu quả gắn "ước tính" là của agent, **chưa đo**. API học thuật (arXiv/OpenAlex/S2) bị giới hạn trong phiên, nên mọi khẳng định "chưa ai làm" phải rà lại trước khi nộp (mục 9).

---

## 1. Phản biện tổng thể (3 trục, chỉ xét công trình 2025 → nay)

| Thành phần ứng viên | Trùng lặp | Tính mới | Khả thi (1× RTX 3090) | Quyết định |
|---|---|---|---|---|
| Bơm KG ngoài (ConceptNet/Wikidata) vào bộ sinh caption, GCN | **HIGH** (AKGMA AAAI'26, MERGE AAAI'26; KG+caption chỉ ~1,4% bài 2025 và đi ngang) | thấp | cao | **Bỏ** làm đóng góp |
| Adapter graph-token / Q-Former đồ thị vào Qwen-VL | **HIGH** (PSGP, 3DGraphLLM ICCV'25, DyGEnc); text+LoRA ≥ graph-token trên đồ thị nhỏ (06) | thấp | trung bình | **Chỉ ablation** |
| Encoder nhận biết quan hệ cho tiếng Việt | **HIGH** (ViG MAPR'26 trên KTVIC/UIT-ViIC) | thấp | cao | **Bỏ** |
| Lọc scene graph dự đoán bằng VLM | MED-HIGH (CP-SGG CVPR'25, PRISM-0, RelCheck) | thấp | cao | Kỹ thuật, không claim |
| Reward RL theo scene graph (phẳng) | MED-HIGH (SC-Captioner ICCV'25, FoCUS EMNLP'26, CCCaption CVPR'26) | thấp | trung bình | **Baseline bắt buộc** |
| KG-RAG văn hóa | MED (RAVENEA ICLR'26, CulturalGround EMNLP'25, MsRAG) | trung bình nếu có cổng kiểm chứng từng fact | cao | Thành phần phụ |
| Dataset scene graph tiếng Việt | MED (VietSGG 2025 đã có 2.873 ảnh thể thao; CompreCap, SVG) | trung bình (caption chi tiết, ảnh đời sống) | cao | Đóng góp phụ |
| **Trung tính hóa node UNCERTAIN theo phân cấp IsA** (người phụ nữ → người, bánh xèo → bánh, đang cưỡi → ở trên → ở gần) | **LOW** (chỉ Taxonomy-Aware Eval CVPR'25, và chỉ đánh giá) | **cao** | cao | **Lõi phương pháp** |
| **Reward/loss có phụ thuộc cha–con** (quan hệ chỉ được thưởng khi node cha đã kiểm chứng) | LOW-MED (reward hiện có đều phẳng; quy tắc phụ thuộc mới có ở metric, arXiv 2604.01460) | cao | trung bình | **Lõi huấn luyện** |
| **Preference cục bộ từ chỉnh sửa đồ thị (GEPA)** | MED (SceneAlign ACL'26 chỉ cho reasoning/VQA; 0 hit cho caption) | trung bình-cao | trung bình | **Lõi huấn luyện** |
| **Metric biết trạng thái kiểm chứng (gold 3 trạng thái)** + recall phân cấp | MED (PoSh ICLR'26, DSG, CAPTURE; tất cả gold nhị phân, chỉ tiếng Anh) | trung bình-cao | cao | **Lõi đánh giá** |
| KG chỉ làm *tiền nghiệm một chiều* cho quan hệ (hạ xuống UNCERTAIN, không bao giờ REJECT) | chưa thấy bài trùng (cần rà lại) | trung bình | cao | Thành phần |
| Caption truy vết từng span + điều khiển bằng sửa đồ thị | MED (GroundCap, PANORAMA, FoCUS, GAVEL) | trung bình (3 trạng thái + tiếng Việt) | cao (renderer đã link 100% span) | Mục phụ |
| Entity-aware news captioning tiếng Việt | MED-HIGH rủi ro va chạm (nhóm HCMUS: OpenEvents/EVENTA) | trung bình-cao | thấp (cần dữ liệu báo mới, bản quyền) | **Hoãn** |
| Captioner nhỏ có KG (non-LVLM) | MED (ViG, HDUCap JVCIR'26) | phụ thuộc thí nghiệm GRIT vs LVLM | cao | **Cổng quyết định** ở tháng 1 |

**Kết luận phản biện.** Mọi thành phần riêng lẻ đã xuất hiện ở hội nghị đỉnh 2025–2026 (cho tiếng Anh). Cái **chưa ai làm** là *chuỗi*: đồ thị kiểm chứng 3 trạng thái → lùi theo phân cấp IsA thay vì xóa → huấn luyện với tín hiệu phụ thuộc cha–con và preference cục bộ → đánh giá bằng metric biết trạng thái kiểm chứng, trên tiếng Việt. Đóng gói như *phương pháp có cấu trúc* chứ không phải "thêm KG vào transformer".

Những khẳng định **không được dùng**: "benchmark scene graph tiếng Việt đầu tiên" (VietSGG), "đầu tiên của tác giả Việt về KG-captioning" (4 bài 2025, có FAIR 2025), "đảm bảo trung thực" (verifier precision 63,1%).

---

## 2. Phương pháp mới đề xuất: **ViHG-Cap** (Verified Hierarchical Graph Captioning)

```
Ảnh ─┬─► (A) Đề xuất đồ thị: Qwen2.5-VL-7B mệnh đề có kiểu (VSPS) + REACT++/R1-SGG-7B + OWLv2 box
     │
     ├─► (B) Kiểm chứng 3 trạng thái mỗi node/cạnh:
     │       • cổng cấu trúc mệnh đề (bỏ phủ định kép, tách object khỏi vị từ)
     │       • Vintern logit P(Có)/P(Không) một lượt (thay K=5) + ngưỡng theo loại, hiệu chỉnh conformal
     │       • bằng chứng hình học từ box (quan hệ không gian)
     │       • tiền nghiệm KG một chiều: chỉ tăng ngưỡng bằng chứng cho quan hệ phi lý, không tính là bằng chứng
     │
     ├─► (C) Lùi phân cấp (Hierarchical Back-off) cho node/cạnh UNCERTAIN:
     │       thực thể: lá → cha trong IsA (Wikidata subset + bảng ánh xạ tay ~250 dòng + KG văn hóa 150–300 thực thể)
     │       quan hệ: vị từ cụ thể → vị từ chung (đang cưỡi → ở trên → ở gần → chỉ giữ thực thể)
     │       REJECTED → negative node (dùng cho preference), không xuất hiện trong target
     │
     ├─► (D) Đồ thị kiểm chứng phân cấp G* (mỗi node: nhãn, mức IsA, trạng thái, box, nguồn bằng chứng)
     │
     └─► (E) Huấn luyện captioner (Qwen2.5-VL-7B / Qwen3-VL-8B, QLoRA):
             E1. SFT "graph-then-caption": target = G* tuyến tính hóa (văn bản tiếng Việt, gắn nhãn trạng thái) + caption
                 render từ G*; một lượt suy luận, đồ thị là chuỗi suy luận trung gian (kiểu SaGe ICML'26)
             E2. GEPA: cặp preference cục bộ tạo bằng sửa G* (thay node REJECTED, đảo quan hệ, đổi số đếm, nêu giới tính
                 UNCERTAIN, lùi sai mức IsA); loss chỉ trên cụm bị sửa + KL theo token (khắc phục DPO toàn caption từng thất bại)
             E3. (tùy chọn) GRPO với reward phụ thuộc cha–con trên G*, so với reward phẳng (baseline FoCUS/SC-Captioner)
```

**Vì sao đây là "transformer + KG" thật**: KG (Wikidata subset + KG văn hóa + phân cấp IsA) tham gia ở 3 chỗ có kiểm soát — quyết định mức lùi (C), làm tiền nghiệm cho quan hệ (B), sinh negative cho preference (E2) — thay vì đổ thẳng fact vào prompt (nguồn ảo giác tri thức, NES AAAI'26).

**Biến thể mô hình** (ablation, 06): G0 đồ thị dạng văn bản (0 tham số thêm, mặc định); G1 + mặt nạ attention theo topo (~7,8K tham số); G2 + 8 graph token (~23M). Đối chứng bắt buộc: đồ thị bị xáo trộn — nếu điểm không đổi thì mô hình không đọc đồ thị và dừng nhánh G1/G2.

**Mô-đun văn hóa (09, 05)**: thực thể văn hóa (nón lá, áo dài, xích lô, phở…) là một loại node riêng; SUPPORTED giữ tên, UNCERTAIN lùi về cha ("bánh xèo" → "bánh"), fact KG không nhìn thấy được bị chặn khỏi caption. Động lực đo được: VSPS hiện xóa từ văn hóa (recall 58,8% zero-shot → 16,2–23,5% sau SFT; gold 65 ảnh, cần CI).

---

## 3. Bộ độ đo mới

| Mã | Tên | Định nghĩa ngắn | Gần nhất / khác biệt |
|---|---|---|---|
| M1 | **ViVG-P/R** | P/R trên đồ thị gold 3 trạng thái; precision là *khoảng* [strict, lenient] theo node UNCERTAIN; gắn thuộc tính đúng chủ thể; recall có trọng số độ nổi bật; quy tắc phụ thuộc cha–con | DSG/PoSh/CAPTURE: gold nhị phân, tiếng Anh |
| M2 | **ViRHR** + **PDG** | Tỷ lệ ảo giác quan hệ, chỉ tính khi cả hai đầu đúng; tỷ lệ đảo chủ/tân; *Prior Dependency Gap* = chênh tỷ lệ chấp nhận quan hệ "quen thuộc" vs "lạ" giữa ảnh thật và ảnh trắng | R-Bench, Reefknot: QA yes/no, không đo trên caption tự do tiếng Việt |
| M3 | **H-R** và **SFA** | Recall phân cấp (điểm một phần cho từ chung hơn đúng); diện tích đường cong Trung thực–Độ cụ thể khi quét mức IsA | Taxonomy-Aware Eval CVPR'25 (chỉ đánh giá phân loại) |
| M4 | **CulR / CulOA** | Recall thực thể văn hóa và tỷ lệ gán văn hóa quá đà (nêu áo dài/nón lá khi không có) | CulturalVQA/RAVENEA: không có Việt Nam, không caption |
| M5 | **TBW** (Traced-But-Wrong) | Tỷ lệ span truy vết được nhưng mệnh đề nguồn sai theo người | GAVEL: không có trạng thái kiểm chứng |
| M6 | **NVL** (Non-Visual Leakage) | Tỷ lệ fact KG không thể thấy trong ảnh lọt vào caption | NES: đo copy entity, không đo fact phi thị giác |

Metric phụ trợ báo kèm: CHAIR-vi, object P/R/F1, POPE/AMBER (chuẩn tạp chí), CIDEr/BLEU (để so leaderboard UIT), SPICE qua dịch sang Anh (baseline vì chưa có SPICE-vi).

**Kiểm chứng metric (meta-evaluation, 15)**: 500 ảnh (KTVIC, UIT-OpenViIC, UIT-ViIC) × 5 caption từ ≥5 hệ thống (có hệ không thuộc VSPS), 3 người chấm 2 trục (đúng / đầy đủ), 600 cặp so sánh, nhãn cấp mệnh đề trên 200 ảnh, ~6.000 nhiễu tự động (gồm lỗi riêng tiếng Việt: Unicode NFC/NFD, vị trí dấu, tách từ). Ngưỡng: Krippendorff α ≥ 0,67; κ ≥ 0,6 (cặp), ≥ 0,7 (mệnh đề). Báo Kendall τ_c (chính) và τ_b, cấp caption và cấp hệ thống, bootstrap + Williams test, Holm. **Chống vòng lặp tự phục vụ**: báo lại mọi kết quả sau khi bỏ caption VSPS/ViHG-Cap; ảnh meta-eval tách khỏi ảnh huấn luyện parser. Đây đồng thời là **bộ dữ liệu chấm điểm caption tiếng Việt đầu tiên** (chưa tìm thấy bộ nào).

**Parser caption → đồ thị tiếng Việt (08)**: Qwen 7–8B few-shot tạo đồ thị bạc → tinh chỉnh ViT5-base (chính), Qwen 1.5B LoRA (ablation). Gold: 300 caption train + 650 test (500 ngắn, 150 chi tiết). Luật dừng: nếu không hơn "dịch sang Anh → FACTUAL/DiscoSG" ≥3 F1 thì phát hành như công cụ, không claim parser mới.

---

## 4. Dữ liệu

| Nguồn | Dùng cho | Ghi chú |
|---|---|---|
| KTVIC (4.327 ảnh) | train/test chính | 401/558 ảnh test gần trùng train UIT-OpenViIC → báo thêm tập 157 ảnh sạch; repo không có license |
| UIT-OpenViIC | train/test thứ 2 | ảnh crawl Google/Bing, "non-commercial" |
| UIT-ViIC + VietSGG (2.873 ảnh, CC BY 4.0) | thử metric miễn phí: 1.236 ảnh có cả caption Việt, SG Việt, SG Anh của VG (cần xác minh id) | ảnh thể thao COCO, không có địa danh |
| Gold scene graph tiếng Việt (mới) | pilot 500 ảnh KTVIC test (300 ảnh object-gold + 200) | ~122–260 giờ công, 15–20 GPU-h (ước tính); 2 người + trọng tài; κ ≥ 0,7 object, F1 ≥ 0,6 triple |
| Wikidata subset (đóng băng) | IsA, liên kết thực thể | 18/20 nghĩa đúng ở hạng 1; ≥87/113 lexicon khớp; nhầm nghĩa (áo→Áo, bát→bath) → reranker theo ngữ cảnh + bảng ánh xạ tay; "mô tô" vs "xe máy" |
| KG văn hóa Việt (mới, 150–300 thực thể) | node văn hóa | không có KG công khai; VietMEAgent (FAIR'25) có KB 156 thực thể cho VQA |

Phát hành: chỉ phát hành annotation (CC BY-NC-SA 4.0), xin phép tác giả dataset bằng văn bản trước.

---

## 5. Thí nghiệm

**Baseline** (chuẩn Q1/Q2 2026: ≥2 backbone, ≥4 baseline, 3 seed, human eval, bảng latency/bộ nhớ):
zero-shot Qwen2.5-VL-7B, Qwen3-VL-8B, InternVL3.5-8B, Vintern-3B; SFT trên caption zero-shot không kiểm chứng; VSPS (bài hiện tại); FoCUS/SC-Captioner-style GRPO reward SG phẳng; KG-in-prompt (AKGMA-style, KG dạng văn bản); RAVENEA-style RAG; GRIT (leaderboard KTVIC); decoding: VCD, DoLa, OPERA/SPIN.

**Ablation chính**: (−) lùi IsA (xóa thay vì lùi); (−) tiền nghiệm KG; (−) box/hình học; K=5 vs logit; graph-then-caption vs caption-only; GEPA vs DPO toàn caption; reward phụ thuộc vs phẳng; G0/G1/G2 + đồ thị xáo trộn; mức IsA tối đa (đường cong SFA).

**Cổng quyết định (stop/go)**
- T0 (tuần 1, 0 GPU): precision các object REJECTED trên 244 mục đã audit → nếu < 70% thì GEPA bỏ loại sửa "thay node REJECTED".
- T1 (tháng 1): GRIT vs QLoRA Vintern-1B / Qwen2.5-VL-3B / 7B trên KTVIC → quyết định có làm nhánh captioner nhỏ.
- T2 (pilot gold 500 ảnh): đạt κ/F1 ngưỡng mới mở rộng 1.500 ảnh.
- T3 (parser): luật +3 F1.
- T4 (metric): τ_c của M1 không kém VLM-judge quá 0,03 → nếu kém, định vị M1 là chẩn đoán, không thay judge.

**Ngân sách GPU (ước tính, 1× RTX 3090)**: sinh đồ thị 20k ảnh ~1 tuần; verifier logit lại toàn bộ ~vài ngày; mỗi SFT ~3,6 h (đo được); ablation tiêm đồ thị ~75–140 GPU-h; GEPA ~80–100 GPU-h; graph-target SFT ~65–75 GPU-h; GRPO 6–8 h/run. Tổng ~450–600 GPU-h ≈ 3–4 tuần máy chạy liên tục.

---

## 6. Sản phẩm công bố

| Bài | Nội dung | Venue (thứ tự) | Mốc |
|---|---|---|---|
| **P0** (đang có) | VSPS mở rộng Q2 | ACM TALLIP | thêm: hạn chế xóa văn hóa, tập KTVIC sạch, sửa lỗi quan hệ (mục 7) |
| **P1** | Benchmark + metric: gold SG tiếng Việt 500 ảnh, bộ chấm điểm người, M1–M6, parser | EMNLP 2027 (ARR ~05/2027, chưa xác nhận) → IP&M SI low-resource multimodal (Q1, hạn 31/08/2027) → LRE (nếu P0 dùng TALLIP) | arXiv ~04/2027 để giữ ưu tiên |
| **P2** | Phương pháp ViHG-Cap | ACM MM 2027 (~04/2027, chưa xác nhận) → ACM TOMM → JVCIR | 1–2 tháng sau P1 |

---

## 7. Việc làm ngay cho VSPS (phát hiện phụ của vòng 1, có ích cho bài Q2 hiện tại)

1. **45% mệnh đề quan hệ hỏng cấu trúc** trước verifier (23,8% vị từ phủ định → câu hỏi phủ định kép; 31,9% object dán vào vị từ; 28% quan hệ SUPPORTED cũng hỏng) — đếm bằng regex, cần kiểm tay ~100 mục; thêm cổng cấu trúc.
2. **`geometric_check()` chưa từng chạy**: 0/28.912 thực thể có box → mọi quan hệ không gian không có bằng chứng hình học.
3. "Relation precision ~30%" chỉ dựa trên 7 mục audit → không báo; audit lại ≥150 quan hệ.
4. **Xóa từ văn hóa** sau SFT (58,8% → 16,2–23,5%) → nêu là hạn chế, kèm bootstrap CI.
5. **KTVIC test gần trùng UIT-OpenViIC train** (401/558) → báo thêm tập 157 ảnh.
6. CIDEr VSPS 17,3 vs GRIT 136 trên KTVIC → một đoạn giải thích (caption chi tiết vs tham chiếu ngắn).

---

## 8. Lộ trình (10/2026 → 08/2027)

| Tháng | Việc |
|---|---|
| 10/2026 | T0; sửa cổng cấu trúc quan hệ + verifier logit; box OWLv2; schema SG v0.1, IsA ~250 dòng, KG văn hóa v0; hướng dẫn gán nhãn; hoàn thiện P0 |
| 11/2026 | Pilot gold SG 500 ảnh (máy gợi ý → người sửa); thử metric trên VietSGG∩VG; sinh G* cho KTVIC train |
| 12/2026 | Parser (bạc → ViT5); thu thập phán đoán người cho meta-eval; T2 |
| 01/2027 | T1 (GRIT vs LVLM); SFT graph-then-caption (E1), G0/G1/G2 + xáo trộn; T3 |
| 02/2027 | GEPA (E2); baseline GRPO phẳng vs phụ thuộc (E3); backbone thứ 2 (Qwen3-VL-8B) |
| 03/2027 | Meta-eval M1–M6, T4; 3 seed; human eval phương pháp; bảng latency |
| 04/2027 | Viết P1, đưa arXiv; nộp P2 ACM MM (nếu hạn xác nhận) |
| 05/2027 | Nộp P1 EMNLP (ARR) |
| 06–08/2027 | Phản hồi reviewer; dự phòng IP&M SI (31/08) / TOMM / JVCIR |

---

## 9. Rủi ro và việc rà lại

- **Va chạm nhóm**: UIT (nhóm Kiet/Ngan Nguyen có metric THR; nhóm ViG làm quan hệ trên KTVIC), HCMUS (Trung-Nghia Le: EVENTA/OpenEvents). Đặt arXiv sớm.
- **Rà lại khi API hết giới hạn**: tính mới LOW của lùi IsA (17), tiền nghiệm KG một chiều (11), "chưa có bộ chấm điểm caption tiếng Việt" (15), "chưa có preference sửa đồ thị cho caption" (12); đọc bài FAIR 2025 về KG-captioning, ViG, HDUCap (đều paywall).
- **Verifier yếu (63,1%)** lan sang đồ thị → phải nâng precision trước (logit + ngưỡng + box) rồi mới xây G*.
- **Bản quyền dữ liệu**: KTVIC không license; OpenViIC non-commercial.
- **Quyền riêng tư**: 8 agent vòng 1 đã gửi email người dùng trong tham số mailto/User-Agent tới OpenAlex/Crossref/Wikidata trước khi có quy tắc cấm; từ vòng 2 mọi brief cấm rõ.

## 10. Vòng lặp phản biện

Vòng 2: các agent phản biện độc lập đọc bản nháp này và soi 3 trục (trùng lặp — săn bài trùng *chuỗi* ViHG-Cap và từng metric M1–M6; tính mới — chỉ ra chỗ "đổi tên"; khả thi — kiểm chi phí, dữ liệu, giả định). Phát hiện được xác nhận → sửa bản này → vòng 3 nếu còn HIGH. Dừng khi không còn HIGH, mọi đóng góp có điểm khác biệt kiểm chứng được, và mọi bước chạy được trên phần cứng; tối đa 3 vòng.
