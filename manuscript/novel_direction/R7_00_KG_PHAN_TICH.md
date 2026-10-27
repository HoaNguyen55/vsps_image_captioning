# R7-00: Image captioning kết hợp đồ thị tri thức (KG): có hợp với bài captioning tiếng Việt không?

13/10/2026, vòng R7 (các báo cáo agent ngày 12/10/2026). Tài liệu này tổng hợp bốn báo cáo agent (K1, K2, K3, N1) và lịch sử KG trong repo. Chỉ dùng dữ liệu và nhãn người đã có. Không gán nhãn mới, không dùng nhãn AI. Mọi số trên KTVIC được tính trên CPU, trên dự đoán và mẫu của tập test, nên chỉ là **ước lượng cỡ hiệu ứng**. Mọi ngưỡng được cố định trước; không chỉnh gì trên test. CI là 95% bootstrap ghép cặp theo ảnh (B = 2000), trừ khi ghi khác.

**Nguồn.** Mỗi con số đều kèm nguồn trong ngoặc vuông.
- [K1] tài liệu và số baseline vs +KG; [K2] KG với LVLM, tài nguyên tiếng Việt, scoop; [K3] pilot trên KTVIC. File: `manuscript/research_kg/{K1_literature,K2_lvlm_vn,K3_pilot}_REPORT.txt`.
- [N1] hiện tượng tiếng Việt, phân rã giữ lại có đối chứng người: `manuscript/research_r6/N1_vietnamese_REPORT.txt`. [R6] `manuscript/research_r6/CONTEXT_R6.md`, `manuscript/research_r6/B1_rl_REPORT.txt` và bản tổng hợp `manuscript/novel_direction/R6_00_PHUONG_PHAP_DOT_PHA.md`.
- Các báo cáo trên đã được lưu trong repo (commit 2bc375a). Phán quyết của agent quyết định nằm trong nhật ký quyết định của phiên (D1–D7).
- Trong repo: [RW11] `manuscript/research_wall/11_knowledge_graph_captioning.md`; [KH] `manuscript/kg_plan/00_KE_HOACH.md` (v3, 10/10/2026); [RT17] `manuscript/kg_plan/17_novelty_redteam.md`; [R3-01] `manuscript/kg_plan/R3_01_overlap_novelty.md`; [R5-01] `manuscript/novel_direction/R5_01_SECOND_PANEL.md`.
- Ký hiệu: C = CIDEr-D, B4 = BLEU-4, M = METEOR, RL = ROUGE-L, CHi / CHs = CHAIR_i / CHAIR_s, đều ×100. P1 = SFT trên caption đầu; fuse2 = SFT trên đích ghép từ 2 caption người. "Giữ lại" = chọn trên một nhóm tham chiếu, chấm trên nhóm tham chiếu rời.

## 1. Kết luận

KG **không hợp** làm phương pháp của bài này: không hợp khi bơm vào bộ sinh caption, cũng không hợp khi đưa vào reward RL. Nguyên nhân nằm ở dữ liệu. Tham chiếu KTVIC gần như không chứa tri thức. Không caption test nào trong 2790 caption có tên riêng. Thực thể, suy luận phi thị giác và văn hóa cộng lại chỉ chiếm 2.98% token và 4.89% khối CIDEr của tham chiếu [K3 §2]. P1 thua một người chú thích 31.78 điểm C; phần tri thức chỉ chiếm 1.05 điểm trong đó. Phần lớn nằm ở chọn và gọi tên object (14.91), thuộc tính (4.54) và cảnh (4.20) [K3 §2]. Tài liệu cho thấy lợi ích của KG co lại khi baseline mạnh lên: trung vị +1.4 C ở baseline 130–140 và +0.9 ở ≥ 140 [K1 §3]. P1 đã ở 145.8 (3 seed) [R6]. Trên KTVIC, khi phép sửa kiểu KG được chọn trên tham chiếu khác với tham chiếu chấm, C đổi từ −2.5 đến 0.0 [K3 §3]. Reward có KG không hơn CIDEr-D thường [K2 §3] và trả thêm điểm cho tên gọi mơ hồ [K3 §4]. Vai trò còn đứng được là **công cụ phân tích**: dùng phân cấp tên gọi sẵn có để phân rã khoảng cách P1–người theo hiện tượng, ở chế độ giữ lại, có đối chứng người [N1 §3]. Việc này tốn 0 GPU-h nhưng không tăng metric. Đòn bẩy metric vẫn là RL trên CIDEr-D (CN-RLOO; phản biện R6 hạ kỳ vọng xuống +2 đến +6 C so với P1 cùng cách tính loss) và MBR theo CIDEr-D trên tổ hợp adapter (+7.5 đến +11.9 C, ước lượng trên test) [R6_00]. MR5 đã được đo và bị loại: −1.1 C so với P1 cùng điều kiện, seed 42 (quyết định D6). Novelty cho tạp chí Q1 sẽ không đến từ "KG + captioning" [K2 §6].

| Vai trò của KG | Verdict | Số quyết định |
|---|---|---|
| Đòn bẩy phương pháp chính cho C, B4, M, RL | **Không phù hợp** | Trung vị ΔC theo tài liệu: +1.4 ở baseline 130–140 (n = 7), +0.9 ở ≥ 140 (n = 1); ρ(baseline, ΔC) = −0.71 (n = 21) [K1 §3]. KTVIC: 0/2790 tham chiếu có tên riêng; tri thức 4.89% khối CIDEr [K3 §2]. Oracle đọc tham chiếu test, chèn mọi từ tri thức bị thiếu: +3.06 đến +3.46 C, B4 −0.42 đến −0.69 [K1 §4]. Giữ lại: −2.5 đến 0.0 C [K3 §3]. |
| Thành phần của reward RL (CN-RLOO) | **Không phù hợp** | Cộng F1 object (lexicon tay hoặc Wikidata) vào CIDEr-D: −2.9 đến +2.4 C trên tham chiếu giữ lại; 48/48 CI chứa 0 [K2 §3]. Reward chuẩn hóa KG: tương quan 0.96 với CIDEr-D; best-of-6 −1.21 [−2.76, +0.43]; reward trung bình +11 điểm, trong đó 8 điểm trả cho hypernym [K3 §4]. |
| Giảm ảo giác / CHAIR | **Không phù hợp làm phương pháp**; lexicon tay chỉ làm ablation | Term object từ lexicon tay: CHi so với panel độc lập 16.7 → 15.5 [−2.2, −0.2] ở C ≈ 0; bản Wikidata không hơn [K2 §3]. Lùi hypernym có cổng oracle, giữ lại: C +0.02, CHi −1.90 [−2.88, −1.05]. Cổng thực tế: C −1.14 [−2.25, −0.19] và −2.59 [−4.41, −1.15], CHi không đổi [K3 §3]. Ngưỡng Pareto cần CHi −4 [R6]. |
| Tri thức văn hóa (KG hoặc RAG văn hóa) | **Không phù hợp** | Văn hóa 1.52% token; khoảng cách người–P1 0.35 C [K3 §2]. Oracle văn hóa giữ lại: −0.19 đến −0.46 C [K3 §3]. RAVENEA: C 22.2 → 8.5; CONCAP tiếng Việt: −5.2 C [K1 §2.3, §2.7]. Chưa có KG văn hóa Việt công khai có giấy phép [K2 §4.4]. |
| Công cụ phân tích / đánh giá | **Phù hợp, vai trò phụ, 0 GPU-h** | P1 thừa so với người ở mức chi tiết khi gọi người: oracle +6.57 [+4.22, +9.10], giữ lại +6.13 [+3.54, +8.78]. Biến thể hình thái: oracle +26.48 nhưng giữ lại −5.37 [−8.10, −2.65]; với người +23.31 / −9.38 [N1 §3]. Chưa tìm thấy bài nào làm phân rã này [N1 §7]. |

**Cơ chế, ngắn gọn.**
1. CIDEr thưởng n-gram mà các người chú thích cùng viết. KG chỉ giúp khi nó đưa vào đúng chữ đó, như tên riêng trong tin tức [K1 §4]. KTVIC không có chữ loại này: 0 tên riêng, và chỉ 0.37% token test không có trong train [K1 §4].
2. P1 thua người ở chỗ chọn object và chọn mức tên gọi. KG biết quan hệ giữa các tên, nhưng không biết người chú thích của ảnh này chọn tên nào. Chọn tên trên tham chiếu khác cho −1.25 đến −2.47 C [K3 §3].
3. Hypernym làm câu mơ hồ hơn. CIDEr phạt điều đó: lùi đại trà mất 13.7 đến 15.5 C [K1 §2.6]. Reward có điểm hypernym lại thưởng nó: +8 điểm reward [K3 §4].

## 2. Câu hỏi và cách đánh giá

### 2.1 Câu hỏi
Người dùng hỏi (12/10/2026): ngoài RL, hướng "image captioning + KG" có hợp với bài captioning tiếng Việt không, và có novelty nào khả dĩ. Bài nhắm tạp chí Q1. Captioner là Qwen2.5-VL-7B QLoRA 4-bit, huấn luyện trên KTVIC. P1 đạt C 145.8 (3 seed, SD ~3.4); GRIT, SOTA đã công bố trên KTVIC, đạt 136.0 [R6].

### 2.2 Đã đo gì
- Tài liệu [K1 §1]: 31 bài đọc toàn văn. Lấy số baseline vs +KG trên cùng benchmark. Dùng 25 ablation COCO trong cùng bài để đo ΔC theo độ mạnh baseline. Đếm xu hướng arXiv 2019–2026 cho 10 họ truy vấn. Kiểm bài mới sau 10/10/2026.
- KG với LVLM 2024–2026 [K2 §2]: reward đồ thị, giảm ảo giác bằng đồ thị, RAG, metric đồ thị, tài nguyên văn hóa. Scoop tiếng Việt: 47 truy vấn [K2 §5].
- Pilot KTVIC [K3]: phân loại nội dung từng token; phân rã C giữa người và P1; oracle sửa caption kiểu KG ở hai chế độ (cùng tham chiếu, giữ lại); cổng thực tế không đọc tham chiếu; reward KG cho RL.
- Pilot reward [K2 §3; N1 §5]: proxy một bước RL (best-of-7, hoặc bước KL 1 nat) trên 6 mẫu T = 0.8 mỗi ảnh. Chấm trên tham chiếu giữ lại và trên panel OpenViIC.
- Tài nguyên [K2 §4]: Wikidata, ConceptNet 5.7, OMW, Kaikki, VietNet, VietSGG. Đo trên 113 mục lexicon CHAIR và 200 danh từ KTVIC thường gặp nhất. Kiểm nghĩa tự động trên 224 từ COCO-80.
- Tái lập: scorer cho đúng P1 s42 C 149.79, B4 45.55 như file kết quả đã lưu [K1 §1; K3 §1; N1 §1].

### 2.3 Ràng buộc
- Không gán nhãn mới dưới mọi hình thức. Nhãn AI không phải bằng chứng [R6]. "Sự thật" sẵn có: panel người thứ hai UIT-OpenViIC (555/558 ảnh test), nhãn instance COCO-2014 trên UIT-ViIC và COCO Karpathy, XM3600 với nhãn OIV7 đã người kiểm [R5-01; R6].
- Một RTX 3090, QLoRA 4-bit. Hai máy thuê chỉ để tăng thông lượng [R6].
- Metric trước: C, B4, M, RL trên KTVIC tăng, CHi giảm. Ngưỡng "đột phá": ≥ +8 C so với P1 trung bình 3 seed với CHi không xấu hơn, hoặc dịch Pareto (C ≥ P1 và CHi giảm ≥ 4). MDE một seed ~2.5–3.8 C [R6].

### 2.4 Điều đã đổi so với kế hoạch KG ngày 10/10/2026
- **Mục tiêu.** Kế hoạch v3 nhắm trung thực và đánh giá caption chi tiết, với tài nguyên đánh giá tiếng Việt mới: gold scene graph, bộ chấm người, parser [KH §1, §6]. Nay mục tiêu là metric n-gram trên caption ngắn.
- **Ràng buộc.** Nay cấm gán nhãn. Mọi lõi còn sống của v3 đều cần nhãn mới.
- **Phát hiện mới.** 5 tham chiếu KTVIC là một chuỗi diễn đạt lại nhau; SFT nhiều tham chiếu là đích tốt nhất [R6 B2]. Precision dựa trên tham chiếu đo độ điển hình nhiều hơn sự thật [R5-01]. Mọi đích huấn luyện nằm trên một đường precision–độ phủ; chỉ bằng chứng ngoài (tag detector) dịch được khỏi đường đó [R6]. RL trên CIDEr-D là đòn bẩy chính, kèm nguy cơ chép lại tham chiếu [R6 B1].
- **Có số.** Các file kg_plan chủ yếu ghi ai làm gì, hầu như không có số baseline vs +KG [K1 §0]. Mục 3–4 bổ sung số đó.
- **Sửa một lỗi cũ.** Con số "+11%" của RAVENEA mà kg_plan/04, 05, 09 trích là RegionScore, không phải CIDEr. CIDEr của nó giảm [K1 §6].

### 2.5 Vì sao lõi ViHG-Cap cũ không còn làm được
ViHG-Cap là phép lùi phân cấp có cấu trúc KG cho thực thể và vị từ UNCERTAIN, kèm metric đồ thị tiếng Việt [KH §1–3].
1. **Cần nhãn.** MVP cần ~200 giờ người gán và ~90 giờ NCS [KH §8]. Sau vòng 3, nhu cầu ước tính là 245–275 giờ người gán [KH §12.4]: gold scene graph ~400 ảnh, meta-eval người, IAA, chấm người cấp mệnh đề. Các cổng sau tuần 1 đều cần gold người: T2 (IAA), T3 (parser), T4 (tương quan với người), T-human, và G-P2 (đo bằng H-R, tức recall phân cấp so với gold scene graph) [KH §5, §12.3].
2. **Phép lõi đo được mà không cần nhãn, và không có lợi.** Lùi đại trà: −13.7 đến −15.5 C [K1 §2.6]. Cổng thực tế: −1.14 và −2.59 C, CHi không đổi [K3 §3]. Trần giữ lại với cổng hoàn hảo: C ≈ 0, CHi −1.83 đến −2.20 [K3 §3].
3. **Trùng lặp.** Phần thực thể trùng HIGH khi ghép Conceptual Captions (ACL 2018: thay tên riêng bằng hypernym lấy từ Google KG trong dữ liệu huấn luyện captioner) với trung tính hóa của VSPS và CLC [R3-01 F1].
4. **Tài nguyên.** Bao đóng IsA Wikidata không tuyển chọn có 72% cặp rơi vào ba từ chung [K2 §4.3]. Tuyển chọn bằng tay là gán nhãn.

## 3. Bằng chứng từ tài liệu

Venue và id theo [K1] và [K2]. [ngoài DS] = venue ngoài danh sách của vòng R7; [nền] = trước 2019; [preprint] = chưa có venue.

### 3.1 Lợi ích co lại khi baseline mạnh lên
25 ablation trong cùng bài trên COCO Karpathy, thuộc ba họ: concept/commonsense/Visual Genome, scene graph, bộ nhớ truy hồi [K1 §3].

| Dải C của baseline | n | Trung vị ΔC | Khoảng ΔC |
|---|---|---|---|
| < 115 | 4 | +2.4 | +0.7 đến +4.1 |
| 115–125 | 8 | +6.5 | +1.3 đến +8.6 |
| 125–130 | 5 | +3.0 | +0.6 đến +5.6 |
| 130–140 | 7 | +1.4 | −1.2 đến +5.7 |
| ≥ 140 | 1 | +0.9 | VinVL-L RL, 140.0 → 140.9 |
| KTVIC ~144 (repo: tag GDINO trong prompt; họ concept, không phải KG) | 2 | +1.1 (P1 s43), +2.5 (fuse2 s42) | một seed, trong MDE 2.5–3.8 |

- Spearman ρ(baseline, ΔC) = −0.42 (n = 25). Với baseline ≥ 115: ρ = −0.71 (n = 21, p xấp xỉ < 0.001; các dòng không độc lập) [K1 §3].
- Dải 115–125 là thời "SG/commonsense" 2018–2021. Lợi ích khi đó được đo so với baseline chưa huấn luyện đủ [K1 §3].
- REVEAL (CVPR 2023, 2212.05221; 145.4) và K-DFIC (IEEE TCSVT 2025, DOI 10.1109/TCSVT.2024.3525158; 148.4) không có ablation kiểm được [K1 §3, §8].
- Chưa có bài nào ablation KG sạch cho LVLM 7B instruction-tuned, trên caption ngắn, với metric n-gram [K1 §2.8].

### 3.2 Co lại ngay trong một bài, và co lại khi có đối chứng đúng [K1 §3]
| Bài | Lợi ích (C) theo độ mạnh baseline |
|---|---|
| VinVL (CVPR 2021, 2101.00529) | +5.6 (123.7) → +3.0 (127.8) → +2.8 (137.6) → +0.9 (140.0) |
| RA-Transformer (ACM TOMM 2024, 2405.13127) | +2.9 (XE 121.6) → +1.4 (SCST 135.3) |
| TSG (ACL 2023, 2305.02177) | +3.6 (128.7) → +2.2 (137.3) → +0.4 so với PureT 138.2 (khác bài) |
| Lee+ 2019 (1909.09953) [chỉ arXiv] | +1.1 (XE) → +0.6 (RL) |
| VC R-CNN (CVPR 2020, 2002.12204) | +8.2 → +3.0 và +5.6 → +3.0 khi so với đối chứng đặc trưng tương đương |
| VSUA (ACM MM 2019, 1908.02127) | +5.8 → +4.9 khi so với đối chứng dung lượng |
| GCN-LSTM (ECCV 2018, 1809.07041) [nền] | +8.6 so với Up-Down đã công bố (120.1) → ~+1.8 so với Up-Down huấn luyện lại 126.9 (khác bài, theo Lee+ 2019) |
| Zhao+ (IEEE TMM, 2107.11970) | +6.4 so với mô hình không đồ thị của chính họ → +0.2 so với SOTA trước (Tell) |
| KnowCap (ACM MM 2023, 2308.01126), trên COCO | −1.2 / +0.3 / +1.4 ở baseline 139.3 / 135.6 / 137.1 |

### 3.3 Khi nào KG có ích: tham chiếu phải chứa tri thức
- **Tin tức, tên riêng dày đặc.** Zhao+ (IEEE TMM, DOI 10.1109/TMM.2023.3301279): GoodNews / NYTimes800k +6.4 / +6.0 C ở baseline 47.6 / 48.5; entity F1 +2.1 / +3.7. Riêng đồ thị phía ảnh: −0.1 / 0.0 [K1 §2.4]. MERGE (AAAI 2026, 2511.21002): bước KG +5.3 / +2.9 / +14.5 C ở baseline 86.1 / 80.1 / 109.0 (GoodNews / NYT800k / Visual News); NER-F1 +2.3 / +2.0 / −1.3 [K1 §2.4]. Ablation từng module của MERGE: riêng module KG-subgraph −0.3 (85.79 so với 86.08); phần tăng đến từ khớp thực thể với văn bản bài báo [K2 §2.4]. Với backbone Qwen2.5-VL-7B, không tách được phần của KG [K1 §2.4].
- **Object mới hoặc hiếm.** NOC-REK (CVPR 2022, 2203.14499): NoCaps val out-domain +13.2, in-domain +1.0; trên test server toàn bộ +0.5, out-domain −0.6 [K1 §2.3]. EVCap (CVPR 2024, 2311.15879): COCO +5.7, NoCaps +10.5 (bộ giải mã 13B); xóa 90% bộ nhớ chỉ làm NoCaps −1.0 [K1 §2.3].
- **Từ khóa tri thức.** KnowCap: +20.9 / +19.1 C trên tập KnowCap, nơi hơn 95% tham chiếu có từ khóa tri thức; trên COCO chỉ −1.2 đến +1.4 [K1 §2.1].
- **Quan hệ: không có ích.** SPICE relation-F1 ~5 cho mọi mô hình, có hay không có scene graph (Milewski+, AACL 2020, 2009.12313) [ngoài DS]. Riêng embedding nút scene graph: +0.3 C (TSG) [K1 §4].

### 3.4 Khi nào KG làm giảm n-gram
- **RAVENEA** (ICLR 2026, 2505.14462), captioning có thông tin văn hóa, trung bình 14 VLM gồm Qwen2.5-VL-7B: C 22.2 → 8.5, RL 18.0 → 15.3; RegionScore 57.5 → 68.8. Kendall τ giữa CIDEr và đánh giá người về văn hóa: −0.32 (không ý nghĩa) [K1 §2.3; K2 §2.4]. Bộ này có 8 nước, không có Việt Nam [K2 §2.4].
- **CONCAP** (COLM 2025, 2507.20411) [ngoài DS], 36 ngôn ngữ: không RAG 26.9 → concept 30.3 (+3.4); thêm concept văn hóa giàu: 28.6 (−1.7). Tiếng Việt (XM100): thêm lexicon XM3600 −2.4, từ văn hóa PangeaIns −5.2, Wikipedia −4.9. Số đọc từ heatmap; XM100 chỉ có 100 ảnh nên nhiễu [K1 §2.7, §8].
- **Kornblith+** (ICCV 2023, 2307.16686): làm caption cụ thể hơn thì C 126.1 → 78.6, B4 36.1 → 20.9, dù R@1 truy hồi tăng 26.5 → 44.6 [K1 §2.6].
- **MsRAG** (IJCAI 2025; báo cáo không ghi id): RAG mức object, Qwen2-VL trên Kale C 16.8 → 13.3 [K2 §2.4].
- **CulturalGround** (EMNLP 2025, 2508.07414): XM100 tiếng Việt 0.0 → 84.1 là do mô hình gốc không sinh tiếng Việt, không phải hiệu ứng KG. Ở các ngôn ngữ mô hình gốc làm được: en −2.4, es −13.6, id −6.9, sv −7.8, pl +14.2, cs +11.9 [K1 §2.7].

Cách đọc: KG có ích khi nó đưa vào đúng chữ mà người chú thích đã viết (tên riêng trong tin tức, tên object hiếm). Khi nó làm câu cụ thể hơn, hay "văn hóa" hơn so với tham chiếu, n-gram giảm.

### 3.5 Reward có cấu trúc đồ thị trong RL: n-gram dịch khoảng 1 điểm
- SPIDEr (ICCV 2017, 1612.00370) [nền]: thêm SPICE (bộ ba scene graph) vào CIDEr: C +0.5, B4 −1.1, M +0.2, RL −0.4 [K2 §2.2].
- MGRL-RSCC (2609.26166) [preprint], viễn thám: F1 bộ ba từ lexicon tay, không nhãn mới: C +0.56, B4 +1.02. Chính ablation top-k của bài dịch C −3.89 [K2 §2.2]. Đây là tương tự gần nhất của một term lexicon/KG tiếng Việt.
- RadGraph reward (Findings EMNLP 2022, 2210.12186): metric sự thật +14 đến +17, n-gram ~+1; cần bộ trích xuất học từ nhãn bác sĩ [K2 §2.2].
- SC-Captioner (ICCV 2025, 2508.06125): Qwen2-VL-7B B4 +2.8 (DOCCI), +0.7 (COCO-LN); LLaVA −1.1; chỉ +0.6 so với DPO thường; không báo C [K1 §2.5; K2 §2.2].
- FoCUS (EMNLP 2026, 2609.00709): reward scene graph không kèm CIDEr; DOCCI C 11.10 → 9.08 [K2 §2.2].
- Cho+ (Findings NAACL 2022, 2205.13115): reward CLIP-S thay CIDEr làm C 124.9 → 11.2; giữ thêm CIDEr thì 124.6 [K1 §2.5].
- Hack độ dài: ESREAL (ECCV 2024, 2403.16167) bỏ reward tổng thể thì mô hình rút ngắn câu, C 7.85 → 3.83; FGAIF (2404.05046; TMLR 2025 theo header PDF) rút caption từ 216 xuống 60 token [K2 §2.2].
- CIDEr-RL và ảo giác: Rohrbach+ (EMNLP 2018, 1809.02156): SCST làm TopDown CHs 8.4 → 13.6, CHi 6.1 → 8.8. Dai+ (EACL 2023, 2210.07688): ở baseline mạnh gần như trung tính (OFA-L CHi 4.7 → 4.2), nhưng ngoài miền tăng (VinVL-B, NoCaps out-domain, CHi 12.1 → 17.4). MOCHa (EMNLP 2024, pp. 22680-22698, DOI 10.18653/v1/2024.emnlp-main.1263), ở độ mạnh như P1: BLIP-2 C 144.3 → 144.3, CHi 1.7 → 1.4 [K2 §2.1–2.2].

### 3.6 Xu hướng 2024–2026: đồ thị chuyển từ "bơm vào" sang kiểm chứng, đánh giá, ảo giác
Số bài arXiv khớp từ khóa trong tóm tắt, mỗi năm. 2026 tính đến 09/10, khoảng 77% năm [K1 §5].

| Họ truy vấn | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026* |
|---|---|---|---|---|---|---|---|---|
| KG / commonsense / ConceptNet + captioning | 8 | 8 | 9 | 11 | 19 | 16 | 16 | 16 |
| scene graph + captioning | 8 | 12 | 15 | 8 | 23 | 12 | 19 | 24 |
| captioning tăng cường truy hồi | 0 | 0 | 2 | 2 | 6 | 22 | 26 | 29 |
| captioning thực thể / tin tức | 2 | 6 | 4 | 5 | 10 | 8 | 6 | 4 |
| CIDEr AND (SG OR KG OR commonsense) | 1 | 1 | 3 | 2 | 2 | 1 | 2 | 2 |
| (SG OR KG) + ảo giác + VLM | 0 | 0 | 0 | 0 | 2 | 13 | 17 | 24 |
| SG + đánh giá/metric + caption | 3 | 5 | 4 | 3 | 12 | 8 | 13 | 17 |
| (SG OR KG) + reward/RL + caption | 0 | 0 | 0 | 0 | 1 | 1 | 2 | 5 |
| mọi bài captioning (mẫu số) | 274 | 310 | 358 | 467 | 808 | 1112 | 1316 | 1194 |

- Bơm KG/commonsense đi ngang ở 16 bài/năm; tỉ lệ trong captioning giảm 2.9% (2019) → 1.3% (2026) [K1 §5]. OpenAlex cho cùng hình dạng: commonsense + captioning 14 (2022) → 4 (2026*); KG + ảo giác MLLM 0 → 26 [RW11 §1.1].
- Đang tăng [K1 §5]:
  - kiểm chứng và sửa ảo giác bằng đồ thị: Reefknot (Findings ACL 2025, 2408.09429), FIHA (Findings ACL 2025, 2409.13612), RelCheck (2609.27890) [preprint], KG-ViP (ACL 2026 theo Semantic Scholar, 2601.11632), CART (ACM MM 2026, 2607.16727);
  - metric đồ thị cho caption chi tiết: DSG (ICLR 2024, 2310.18235), CompreCap (CVPR 2025, 2412.08614), PROVE (ICCV 2025 theo Semantic Scholar, 2410.13121), DiscoSG (EMNLP 2025, 2506.15583), PoSh (ICLR 2026, 2510.19060);
  - reward đồ thị cho caption chi tiết: SC-Captioner, FoCUS (mục 3.5).
- Metric đồ thị chỉ hơn CIDEr ở caption **chi tiết**, nơi tương quan của CIDEr với người chỉ ~0.05–0.08: CIDEr PCC 0.083 (bảng của CAPTURE, 2405.19092 [preprint]), 0.052 (bảng của DCScore, ICLR 2025, 2503.07906); Spearman −0.106 (bảng của PoSh) [K2 §2.5]. Mọi metric loại này cần parser tiếng Anh, scene graph tay hoặc LLM judge.
- Sau 10/10/2026: arXiv (đến 09/10) và Crossref (đến 12/10) không có bài nào đổi kết luận [K1 §6].

### 3.7 Phía tiếng Việt (scoop, 47 truy vấn) [K2 §5]
- Chưa tìm thấy bài nào đưa KG, scene graph hay tri thức văn hóa vào sinh caption, đánh giá caption hay reward RL tiếng Việt.
- ViG (MAPR 2026, DOI 10.1109/MAPR72750.2026.11685699): GRIT đóng băng + Residual Relation Memory + Local-Cultural Query Memory khai thác từ caption train, trên KTVIC và UIT-ViIC; nói là hơn GRIT. Tóm tắt không nhắc KG hay RL; chưa thấy số. K1 không tìm được nguồn; K2 tìm được DOI [K1 §8; K2 §5].
- "Developing a Knowledge Graph for The Image Captioning Problem" (FAIR 2025, DOI 10.15625/vap.2025.0297): không đọc được PDF. Các bài khác của cùng nhóm dùng caption tiếng Anh (COCO, Flickr30k) với ConceptNet. Đây là cùng hội nghị FAIR với bài VSPS, nên phải trích.
- HDUCap (JVCIR, 11/2026, DOI 10.1016/j.jvcir.2026.104963): transformer biết không gian + một bộ dữ liệu tiếng Việt mới; chưa có tóm tắt [chưa xác minh].
- RL/SCST tiếng Việt đã có: ObjectAoA (VNU JCSCE 2023, 2211.05405; CE rồi SCST trên UIT-ViIC, C 148.8); lời giải UIT cho VieCap4H (VNU JCSCE 2022, DOI 10.25073/2588-1086/vnucsce.371; 1 epoch SCST); baseline UIT-OpenViIC (DOI 10.1016/j.image.2025.117430; CE rồi SCST). Chưa thấy RL trên KTVIC, chưa thấy RL trên LVLM.
- Dữ liệu scene graph tiếng Việt đã có: VietSGG (GitHub Moobbot/VietSGG; README ghi "Accepted at EAI GOODTECHS 2025"; chưa thấy DOI).

## 4. Bằng chứng trên KTVIC

### 4.1 Tham chiếu KTVIC hầu như không chứa tri thức
Phân loại token của 2790 tham chiếu test (29 805 token) [K3 §2]. "Khối" là phần trọng số tf-idf CIDEr-D của tham chiếu, trung bình n = 1–4. "prop" chia trọng số một n-gram cho các token của nó; "touch" gán cả n-gram cho mọi loại mà nó chạm tới.

| Loại token | % token tham chiếu | % token P1 s42 | % khối (prop) | % khối (touch) |
|---|---|---|---|---|
| thực thể có tên / bách khoa | 0.17 | 0.22 | 0.32 | 0.58 |
| văn hóa | 1.52 | 1.33 | 2.23 | 4.16 |
| cảnh / địa điểm | 6.57 | 6.42 | 8.57 | 15.44 |
| gọi tên object | 25.57 | 24.39 | 30.26 | 54.84 |
| thuộc tính | 4.42 | 2.72 | 5.12 | 10.69 |
| quan hệ / hành động | 19.76 | 19.52 | 22.45 | 45.66 |
| hư từ / khuôn câu | 42.00 | 45.41 | 31.04 | 59.76 |
| K_broad = thực thể + phi thị giác + văn hóa | 2.98 | 2.46 | 4.89 | 9.67 |

- Tên riêng: 0 trong 2790 caption test. Ở train: 67/18 845 caption, thuộc 36 ảnh (việt nam 20, bến thành 11, hồ chí minh 8, ...) [K3 §2]. Không caption test nào có chữ hoa [K1 §4].
- Token test không có trong train: 109/29 805 (0.37%) [K1 §4].
- Nhóm "loại KG" (văn hóa chặt + thực thể + từ hiếm ở train) mang 4.5% trọng số IDF unigram của CIDEr [K1 §4].
- K1 và K3 dùng danh sách khác nhau, nhưng ra cùng bậc độ lớn: ~3–5% [K1 §4; K3 §2].

### 4.2 Khoảng cách P1–người nằm ở chọn object, thuộc tính, cảnh; không nằm ở tri thức
Leave-one-out: tham chiếu k so với 4 tham chiếu còn lại, và P1 s42 so với cùng 4 tham chiếu; trung bình 5 fold [K3 §2].

| Phần của CIDEr-D | Người | P1 s42 | Chênh |
|---|---|---|---|
| Tổng | 181.54 | 149.76 | 31.78 |
| gọi tên object | 73.71 | 58.80 | 14.91 |
| thuộc tính | 9.15 | 4.61 | 4.54 |
| cảnh | 24.07 | 19.88 | 4.20 |
| hư từ / khuôn câu | 37.00 | 32.99 | 4.01 |
| quan hệ / hành động | 29.62 | 26.04 | 3.58 |
| văn hóa | 6.69 | 6.34 | 0.35 |
| thực thể có tên | 1.30 | 1.10 | 0.20 |
| K_broad | 11.07 | 10.02 | 1.05 |

- P1 đã lấy được n-gram văn hóa gần bằng người: 6.34 so với 6.69 [K3 §2].
- Đối chứng người theo hiện tượng (P1 s42 và một tham chiếu người, cùng 4 tham chiếu; oracle(4) / giữ lại 2→2) [N1 §3]:
  - Mức chi tiết khi gọi người (người ↔ người phụ nữ ↔ cô gái ↔ chàng trai): P1 − người +6.57 [+4.22, +9.10]; giữ lại +6.13 [+3.54, +8.78].
  - Lượng từ số nhiều (những / nhiều / một vài): +3.15 [+1.90, +4.52]; giữ lại +3.93 [+2.50, +5.46].
  - Đồng nghĩa cùng mức: +0.51 [−0.59, +1.69]; giữ lại +1.57 [+0.49, +2.70].
- Biến thể hình thái tiếng Việt (loại từ, lượng từ, đang/đã/được, ở/của, khuôn "có ... xuất hiện"): sửa trên đủ 5 tham chiếu +26.48 [+23.74, +29.28]; chọn trên A chấm trên B −5.37 [−8.10, −2.65]. Caption người cũng vậy: +23.31 / −9.38 [N1 §0, §3]. Đây là nhiễu tham chiếu, không phải điểm yếu của P1.
- Phần chuyển giao được ở mức corpus: gọi tên +2.0 [−0.5, +4.6]; lượng từ +0.8 [−0.6, +2.1]; văn hóa đuôi dài +1.0 [−0.1, +2.5] [N1 §0].
- Văn hóa đuôi dài là khoảng trống thật nhưng nhỏ. Recall 1v4 nhóm giữa: P1 28.6%, người 49.0%. Nhóm đuôi: P1 0%, người 48.4% (n = 31). Bỏ sót có hệ thống: sạp 0/15 (P1 viết "quầy hàng"), xuồng 0/10 ("thuyền") [N1 §4.4].

### 4.3 Trần oracle và trần giữ lại
Các phép sửa caption kiểu KG dùng đồ thị từ vựng sẵn có của repo: 409 dạng bề mặt, gồm đồng nghĩa, hypernym, và từ văn hóa → từ chung [K3 §3]. Δ so với caption chưa sửa:

| Phép (oracle) | Cùng tham chiếu, P1 s42: ΔC | ΔCHi | Giữ lại A → B, ΔC: s42 / s43 / s44 | ΔCHi giữ lại: s42 / s43 / s44 |
|---|---|---|---|---|
| a2 chọn tên | +5.34 [+4.07, +6.76] | −3.46 [−4.81, −2.13] | −1.25 [−3.04, +0.48] / −2.20 [−3.87, −0.53] / −2.47 [−4.15, −0.84] | −0.97 / −0.85 / −1.08 |
| b lùi hypernym | +0.97 [+0.43, +1.63] | −3.55 [−4.78, −2.41] | +0.02 [−0.85, +0.92] / −0.21 / −0.19 | −1.90 [−2.88, −1.05] / −1.83 / −2.20 |
| c chèn từ văn hóa | +0.13 [−0.99, +1.16] | −0.26 [−0.73, +0.11] | −0.19 [−1.23, +0.77] / −0.38 / −0.46 | −0.22 / −0.14 / −0.22 (n.s.) |
| d cả ba | +6.16 [+4.78, +7.72] | −4.69 [−6.18, −3.22] | — | — |

- Trần cùng tham chiếu cho mọi phương pháp KG kiểu đổi tên, lùi, chèn văn hóa: +6.2 C, +1.7 B4, +1.0 RL, −4.7 CHi (seed 43/44: +5.1/+5.2 C). Trần này bị thổi phồng vì chọn trên chính tham chiếu chấm [K3 §5].
- Chọn trên tham chiếu khác thì phần C biến mất: −2.5 đến 0.0 [K3 §3].
- Tên do panel độc lập OpenViIC chọn, chấm trên 5 tham chiếu KTVIC: C −12.19 [−15.81, −8.92], CHi +3.04 [+1.43, +4.70] [K3 §3]. Tên "đúng" theo một nhóm người khác bị tham chiếu KTVIC phạt. Đây chính là hiện tượng "độ điển hình hơn sự thật" của R5-01.
- Phép không oracle a1 (mỗi mention đổi về tên phổ biến nhất ở train): +0.35 [+0.06, +0.68] / 0.00 / +0.05. Gần 0 vì P1 đã dùng tên đó: chỉ 3 dạng bề mặt trong 1674 caption P1 khác tên đó [K3 §0, §3].
- Oracle chèn token (K1): chèn mọi token "loại KG" bị thiếu mà tham chiếu test đồng thuận: +3.06 đến +3.46 C (kèm cửa sổ ngữ cảnh: +3.98 đến +4.83); B4 giảm 0.42 đến 0.69 [K1 §4].
- Mọi số trên đều là cận trên. Một KG thật không biết người chú thích đã chọn chữ nào.

### 4.4 Lùi hypernym (phép lõi của ViHG-Cap)
- Lùi đại trà bằng bảng HYPERNYMS của repo: C 135.67 / 130.25 / 128.43 so với 149.79 / 143.92 / 143.90 (P1 s42 / P1 s43 / fuse2 s42), tức −14.1 / −13.7 / −15.5; B4 −3.7 / −3.4 / −4.2; sửa 187 / 171 / 211 caption [K1 §2.6].
- Chỉ lùi khi từ vắng khỏi cả 5 tham chiếu (cổng hoàn hảo, đọc tham chiếu): +0.35 / +0.30 / +0.21 C; trường hợp tốt nhất +0.47 / +0.44 / +0.64 [K1 §2.6].
- Cổng thực tế, không đọc tham chiếu: lùi khi ít hơn τ = 3 trong 6 mẫu T = 0.8 đồng ý (ngưỡng cố định trước) [K3 §3].
  - p1_s43: C −1.14 [−2.25, −0.19], CHi −0.03 [−0.78, +0.69].
  - fuse2_s42: C −2.59 [−4.41, −1.15], CHi +0.38 [−0.73, +1.59], CHs +1.79 [+0.18, +3.58].
  - Chỉ 12/35 và 27/64 mention bị lùi là mention CHAIR gắn cờ. Phần còn lại là tên tham chiếu có dùng: cô gái → người phụ nữ, áo → đồ.
- Phần CHAIR mà mọi phép phân cấp chạm tới được rất nhỏ. P1 s42 có 192 mention bị gắn cờ trên 1002 mention. Chỉ 38 (20%) có tổ tiên KG được tham chiếu hỗ trợ. 80% còn lại là object mà tham chiếu không nhắc dưới bất kỳ dạng nào KG biết [K3 §3].

### 4.5 Reward có KG đẩy về phía mơ hồ
Reward chuẩn hóa KG, trên 6 mẫu T = 0.8 mỗi ảnh; số ghi theo fuse2_s42 / p1_s43 [K3 §4]:
- Reward trung bình: R0 (CIDEr-D thường) 120.8; R_syn (gộp đồng nghĩa) 123.6; R_kg (thêm điểm cho hypernym) 131.9. Phần thêm của R_kg trả cho "người", "xe", "đồ" ở những chỗ một số người chú thích viết từ cụ thể.
- Tương quan trong ảnh với R0: 0.986 / 0.988 (R_syn), 0.960 / 0.962 (R_kg). Gần như cùng một reward.
- Không giảm nhiễu: tương quan giữa hai nửa tham chiếu 0.393 → 0.380 (fuse2). Kém hợp lệ hơn: tương quan với panel độc lập 0.283 → 0.269.
- Chọn best-of-6 trên A, chấm CIDEr-D thường trên B: R_kg −1.21 [−2.76, +0.43] / −1.17 [−2.68, +0.30]; R_root −0.25 [−2.14, +1.60] / −1.86 [−3.64, −0.14]. Trên panel, mọi thay đổi nằm trong ±0.32 và CI chứa 0.
- Nhiễu tham chiếu KTVIC không nằm ở biến thể tên gọi: gộp đồng nghĩa chỉ đổi lựa chọn ở 3–4% ảnh.

Term F1 object cộng vào CIDEr-D, proxy best-of-7; chọn trên tham chiếu {0,1,2}, chấm trên {3,4} và trên panel; λ ∈ {0.25, 0.5, 1, 2}, mọi λ đều báo [K2 §3]:
- C giữ lại: −2.9 đến +2.4 trên 48 cấu hình; mọi CI chứa 0 (hai CI chạm 0). B4 trong ±0.6; RL −0.5 đến +0.9.
- CHi so với panel, lexicon tay, λ = 1: P1 16.7 → 15.5 [−2.2, −0.2] trên cả hai split; fuse2 19.0 → 18.4 [−1.4, +0.3] và 20.1 → 19.3 [−1.8, +0.1].
- Bản Wikidata (đồng nghĩa; thêm IsA) không hơn lexicon tay. Ảo giác mức danh từ: −0.9 đến +0.2.

N1 thử 17 reward thay thế; không cái nào hơn CIDEr-D mức từ [N1 §0, §5]. F1 tên object: KL1 −0.40 [−0.75, −0.06] và −1.00 [−1.66, −0.36] với P1, không ý nghĩa với fuse2. Recall từ văn hóa: trung tính đến âm. F1 tên làm reward duy nhất: −18.1 [N1 §5.2].

### 4.6 Tài nguyên KG tiếng Việt: phủ được nhãn, không phủ được quan hệ dùng được
Đo trên 200 danh từ thường gặp nhất của KTVIC train (phủ 85.6% token danh từ); trong ngoặc là tỉ lệ có trọng số theo ảnh [K2 §4.1–4.2].

| Tài nguyên (giấy phép) | Nhãn/nút tiếng Việt | Cha IsA | Đồng nghĩa vi | Cách hỏng |
|---|---|---|---|---|
| Wikidata (CC0) | 162/200 = 81.0% [87.2%] | 72.5%; cha có nhãn vi 53.0% [60.7%] | 43.5% | Liên kết nghĩa tự động đúng ~84–88% (kiểm trên COCO-80). Lỗi: con chó → một hợp chất ruthenium; áo → nước Áo (Q40); phương tiện → "upaya"; nón → hình nón. 174/241 cặp IsA (72%) rơi vào sản phẩm (61), phần (59), hàng hoá (54); chó, mèo, cây ⊂ phần. |
| ConceptNet 5.7 (CC BY-SA 4.0; API trả 502) | 185/200 [97.6%] | 0 | 44/200 | 171 987 cạnh có nút vi; 0 cạnh IsA, 0 quan hệ commonsense. Thực chất là từ điển dịch. Commonsense chỉ có qua pivot tiếng Anh; hai pivot (ConceptNet, Wikidata) đồng ý nghĩa ~74%. |
| OMW wn-wikt-vie (CC BY-SA 3.0 + GFDL) | 107/200 = 53.5% [59.4%] | theo PWN 3.0 | 62/200 | ~5000 lemma. Các WordNet tiếng Việt lớn (32 413 và 40 788 synset) không phát hành. |
| Kaikki / Wiktionary (CC BY-SA + GFDL) | 192/200 = 96.0% [98.8%] có gloss | hypernym cho 1 danh từ | 65/200 | Từ điển vi → en tốt, không có IsA. |
| VietSGG (CC BY 4.0 theo README) | 0.3% mention danh từ | — | — | 25 lớp object thể thao, 71 vị từ; ngoài miền. |

- So với 27 cặp HYPERNYMS tay của repo: 19 cặp liên kết được cả hai đầu; P279* tái tạo 11/19; 7/8 thất bại là lỗi liên kết nghĩa [K2 §4.3]. Cạnh có tồn tại. Nút thắt là liên kết nghĩa của các từ ngắn, chung chung.
- 13 từ văn hóa thường gặp nhất: Wikidata có 11/13 (thiếu đòn gánh, cờ tổ quốc); bánh mì → bread chung; cha của xích lô gồm taxi và rickshaw. ConceptNet 11/13 nhưng 0 IsA. OMW 5/13 [K2 §4.4].
- Chưa có KG văn hóa Việt công khai có giấy phép. CulturalGround có 3230 thực thể Việt Nam có ảnh (Đức: 332 650) [K2 §4.4, §2.6].
- Lexicon CHAIR của repo (113 mục) chỉ thấy 42.0% mention danh từ trong tham chiếu test [K2 §4.1].
- Kết luận về tài nguyên: không tuyển chọn thì 12–16% nghĩa sai và IsA rơi vào từ chung. Tuyển chọn tay là gán nhãn, bị cấm. Không tài nguyên nào làm pilot tốt hơn lexicon tay [K2 §4.7].

## 5. Các novelty khả dĩ và đánh giá trung thực

Mỗi ứng viên gồm: mới ở đâu, bài gần nhất, hiệu ứng kỳ vọng, chi phí, verdict. Ngưỡng so sánh: +8 C, hoặc Pareto với CHi −4 [R6].

### 5.1 (a) Term KG trong reward CN-RLOO
- **Mới ở đâu.** Term object/IsA lấy từ KG tiếng Việt (Wikidata), cộng vào reward CIDEr-D mức từ của CN-RLOO, cho một LVLM.
- **Gần nhất.** SPIDEr (ICCV 2017, 1612.00370); MGRL-RSCC (2609.26166) [preprint]: F1 bộ ba từ lexicon tay + reward metric; CheXPO-v2 (2512.17213) [preprint]: KG-consistency trong GRPO; SC-Captioner (ICCV 2025, 2508.06125) và FoCUS (EMNLP 2026, 2609.00709): reward scene graph; Re3Cap (EMNLP 2026, 2608.21305): truy hồi bên trong RL caption [K2 §2.2, §2.4].
- **Hiệu ứng kỳ vọng.** C ≈ 0: −2.9 đến +2.4, mọi CI chứa 0 [K2 §3]. R_kg −1.21 [−2.76, +0.43] và đẩy về mơ hồ [K3 §4]. F1 tên object: KL1 −0.40 [−0.75, −0.06] và −1.00 [−1.66, −0.36] với P1 [N1 §5.2]. CHi so với panel ~−1.2, chỉ với lexicon tay [K2 §3]. Tài liệu: term đồ thị dịch n-gram khoảng 1 điểm [K2 §0].
- **Chi phí.** Như CN-RLOO, ~10 GPU-h mỗi seed [R6 B1], cộng phần liên kết KG. Muốn IsA an toàn phải tuyển chọn tay, tức gán nhãn [K2 §4.3].
- **Verdict: bỏ, như một đóng góp.** Nếu còn GPU sau các lượt chính, chạy một ablation "term object từ lexicon tay" làm chốt chặn ảo giác. Không gọi là KG, không gọi là mới. Kiểm nó ở nơi reward không rò: nhãn instance COCO (UIT-ViIC, COCO Karpathy) và panel OpenViIC. CHi trên KTVIC dùng chung gold với reward, nên đo trên KTVIC là Goodhart [K2 §6]. Lý do giữ ablation: trong miền, các lựa chọn oracle best-of-n theo CIDEr của B1 còn làm CHi KTVIC giảm 17.7 → 10.9; rủi ro ảo giác của CIDEr-RL nằm ngoài miền, đúng bối cảnh tái lập trên UIT-ViIC và COCO [K2 §2.1].

### 5.2 (b) Lùi phân cấp có cấu trúc KG để giảm CHAIR (lõi ViHG-Cap)
- **Mới ở đâu (theo v3).** Lùi có điều kiện theo kết quả kiểm chứng, cho cả thực thể và vị từ, trên caption tiếng Việt [KH §1].
- **Gần nhất.** Conceptual Captions (ACL 2018, P18-1238); hypernymization 2304.13130 (2023); Ordonez+ (ICCV 2013); CLC (NeurIPS 2025, 2502.19110); Taxonomy-Aware Eval (CVPR 2025, 2504.05457); SpeciaRL (CVPR 2026, 2603.03197); tự trùng với trung tính hóa giới tính của VSPS [R3-01 F1, F4; RT17 (c)].
- **Hiệu ứng kỳ vọng.** Đại trà: −13.7 đến −15.5 C [K1 §2.6]. Cổng thực tế: −1.14 / −2.59 C; CHi −0.03 / +0.38 [K3 §3]. Trần giữ lại với cổng hoàn hảo: C ≈ 0, CHi −1.83 đến −2.20 [K3 §3]. 80% mention bị CHAIR gắn cờ nằm ngoài tầm với của mọi phép phân cấp [K3 §3].
- **Chi phí.** Cần một verifier tốt hơn nhiều so với đồng thuận mẫu. Chứng minh được cần gold người, ~200 giờ trong v3 [KH §8].
- **Verdict: bỏ.**

### 5.3 (c) KG khái niệm văn hóa Việt
- **Mới ở đâu.** Chưa có KG văn hóa Việt công khai, có giấy phép [K2 §4.4]. Chưa thấy bài nào đưa tri thức văn hóa vào caption tiếng Việt bằng KG [K2 §5].
- **Gần nhất.** RAVENEA (ICLR 2026); CulturalGround (EMNLP 2025); CONCAP (COLM 2025); VietMEAgent (FAIR 2025): KB 156 thực thể cho VQA, bỏ KB làm Cultural Accuracy 0.723 → 0.334; ViG (MAPR 2026): đã có Local-Cultural Query Memory khai thác từ caption train KTVIC [K2 §2.6, §5].
- **Hiệu ứng kỳ vọng.** Văn hóa chiếm 1.52% token và 2.23% khối CIDEr; khoảng cách người–P1 0.35 [K3 §2]. Oracle chèn văn hóa: cùng tham chiếu +0.13 [−0.99, +1.16], giữ lại −0.19 đến −0.46 [K3 §3]. Theo N1: oracle +6.53, giữ lại +1.32 [−0.66, +3.48] [N1 §3]. Bonus recall văn hóa trong reward: trung tính đến âm [N1 §5.2]. Tài liệu: RAVENEA C −13.7; CONCAP tiếng Việt −5.2 [K1 §2.3, §2.7].
- **Vì sao không có lợi.** Chính người chú thích chia rẽ. Ở 20 ảnh được sửa, tham chiếu dùng từ văn hóa 1.9/5 lần và từ chung 2.4/5 lần. Từ văn hóa chỉ áp đảo ở 6/20 ảnh (xuồng, ghe so với thuyền) [K3 §3].
- **Chi phí.** Dựng KG văn hóa là gán nhãn (cấm). Wikidata thiếu 2/13 từ văn hóa hàng đầu và sai nghĩa ở vài từ khác [K2 §4.4].
- **Verdict: bỏ, như một phương pháp.** Ghi khoảng trống văn hóa đuôi dài thành một giới hạn: recall nhóm giữa 28.6% so với người 49.0%, nhóm đuôi 0% so với 48.4% (n = 31) [N1 §4.4].

### 5.4 (d) KG / đồ thị làm công cụ phân tích và đánh giá
**(d1) Phân rã giữ lại, biết phân cấp tên gọi, có đối chứng người.**
- **Mới ở đâu.** N1 không tìm thấy bài nào phân rã headroom CIDEr thành biến thể riêng của ngôn ngữ và nội dung chuyển giao được, với tham chiếu giữ lại và đối chứng người (26 truy vấn) [N1 §7]. K3 thêm lớp tri thức và các phép kiểu KG vào cùng giao thức [K3 §2–3].
- **Gần nhất.** ManyNames (LREC 2020, 2020.lrec-1.710); Ordonez+ (ICCV 2013); Berger & Ponti (2409.16646) [preprint]: biến thể xuyên ngôn ngữ trên XM3600, có tiếng Việt, không có phương pháp; Taxonomy-Aware Eval (CVPR 2025) [N1 §7; R3-01].
- **Hiệu ứng.** Không tăng metric. Nó giải thích vì sao chuẩn hóa bề mặt, tách từ, reward KG và bơm tri thức không dịch được C, và vì sao đòn bẩy nằm ở RL và đích huấn luyện. Số chính ở mục 4.2–4.3.
- **Chi phí.** 0 GPU-h; đã chạy trên CPU. Phân cấp tên gọi là đồ thị từ vựng sẵn có của repo (409 dạng) [K3 §3]; không gán nhãn mới.
- **Kèm theo.** Chẩn đoán đăng ký trước cho các lượt CN-RLOO (MR5 đã bị loại theo D6): tỉ lệ gọi người theo tuổi (P1 29% → tham chiếu 38.5%); tần suất "những" (0.034 → 0.19); recall văn hóa nhóm giữa (28.6% → ~49%) [N1 §6].
- **Verdict: giữ, làm mục phân tích.** Gọi là phân cấp tên gọi (naming hierarchy), không gọi là phương pháp KG.

**(d2) Độ điển hình và sự thật, gộp theo phân cấp.**
- **Ý.** Gộp tên theo đồng nghĩa và hypernym trước khi đối chiếu mention với panel OpenViIC và nhãn COCO. Mục đích: tách "sai theo KTVIC" thành ảo giác thật và lệch tên gọi.
- **Bằng chứng sẵn có.** Mention sai theo KTVIC được panel độc lập xác nhận ở 55.7% (P1), 55.1% (fuse2), 58.8% (một người) [R5-01 §4]. R5-01 đã báo bản theo luật hypernym của chênh fuse2 − P1 (−0.3 short, −0.6 detailed). Tên do panel độc lập chọn bị KTVIC phạt −12.19 [−15.81, −8.92] C [K3 §3]. NAP-lite của repo: 81% referent đã được gọi bằng tên phổ biến nhất; 50% mention sai theo tham chiếu không liên quan tới danh từ nào trong tham chiếu [K3 §3].
- **Giới hạn của Wikidata.** Nó chỉ có ích nếu vượt lexicon 113 mục (CHAIR thấy 42% mention danh từ). Nhưng 12–16% nghĩa sai và 72% cặp IsA rơi vào từ chung [K2 §4]. Trên COCO-80, repo đã có matcher tiếng Việt riêng (`scripts/score_coco_probe.py`) [R6]; Wikidata chỉ liên kết đúng cho 61/80 lớp [K2 §4.3].
- **Verdict: giữ có điều kiện**, làm phân tích độ nhạy với phân cấp sẵn có của repo. Wikidata chỉ làm kiểm tra phụ trên tập liên kết được. Biến thể Wikidata chưa được đo.

**(d3) Độ phủ của CHAIR.** CHi trên KTVIC chỉ thấy 42.0% mention danh từ của tham chiếu test [K2 §4.1]. Báo kèm ảo giác mức danh từ so với panel OpenViIC trên tập 211 danh từ (`pilot/noun_hall.py` của K2) [K2 §6]. Việc này không cần đồ thị. **Verdict: giữ**, thành một câu giới hạn.

**(d4) Metric đồ thị tiếng Việt (kiểu SPICE, CAPTURE, PoSh).** Chưa có parser văn bản → scene graph tiếng Việt. Muốn kiểm một metric như vậy phải có điểm người; repo chỉ có `data/human_eval` với 2 người chấm [K2 §2.5]. Metric đồ thị chỉ hơn CIDEr ở caption chi tiết [K2 §2.5]. **Verdict: không làm** cho bài metric-first.

### 5.5 (e) Ứng viên khác mà các báo cáo hỗ trợ
- **(e1) Truy hồi kNN caption train KTVIC vào prompt.** RA-T (ACM TOMM 2024, 2405.13127) sau SCST: +1.1 đến +1.4 C; lợi ích còn một nửa sau RL [K2 §2.4]. Nó mở kênh chép lại thứ hai (caption của ảnh hàng xóm) mà mask copy của CN-RLOO không che. NES (AAAI 2026 theo trang OJS, 2511.08909): 23.4–25.1% thực thể ảo giác đến từ văn bản truy hồi. Re3Cap đã chiếm "truy hồi trong RL caption" [K2 §2.4, §2.7]. **Verdict: không làm.**
- **(e2) Phạt object theo bằng chứng detector (họ ESREAL, ECCV 2024, 2403.16167; HALC, ICML 2024, 2403.00425).** Kỳ vọng C 0 đến +1, CHi −0.5 đến −2 [K2 §2.7]. Bằng chứng do mô hình tạo, nên người dùng có quyền bác [R6]. Đây là nhánh tag, không phải KG: tag GDINO trong prompt +1.1 / +2.5 C (một seed) [R6]; B1 đã có đề xuất EHX-RLOO dùng tag làm gợi ý khi huấn luyện [R6 B1]; reward PU có cổng bằng chứng đã bị loại ở R6 [R6]. **Verdict: không tính là KG**; nếu làm thì làm trong nhánh tag.
- **(e3) KG-RAG thực thể hoặc văn hóa từ Wikidata.** MERGE, riêng module KG: −0.3 C; MsRAG trên Kale: 16.8 → 13.3 C; RAVENEA: C 22.2 → 8.5 [K2 §2.4]. Tham chiếu KTVIC không có thực thể. **Verdict: không làm.**
- **(e4) Parser caption → scene graph tiếng Việt và benchmark ảo giác quan hệ (Ý 3 cũ).** Khoảng trống có thật: chưa có parser, SPICE hay benchmark ảo giác tiếng Việt [RW11 §3.3; K2 §2.5]. Nhưng phải gán 1000–2000 caption thành bộ ba [RW11 §4.2]. **Verdict: hoãn.** Chỉ hợp một bài tài nguyên, nếu sau này được phép gán nhãn.

### 5.6 Cái gì sống sót, và ở vai trò nào
| Ứng viên | Vai trò còn lại | GPU-h |
|---|---|---|
| (a) term KG trong reward | bỏ; tùy chọn ablation lexicon tay (không phải KG, không phải mới) | ~10/seed nếu chạy [R6 B1] |
| (b) lùi phân cấp KG | bỏ | 0 |
| (c) KG văn hóa | bỏ; khoảng trống văn hóa đuôi dài ghi thành giới hạn | 0 |
| (d1) phân rã giữ lại, có đối chứng người | **giữ: mục phân tích** | 0 |
| (d2) điển hình vs sự thật theo phân cấp | giữ có điều kiện: phân tích độ nhạy | 0 |
| (d3) độ phủ CHAIR | giữ: một câu giới hạn | 0 |
| (d4), (e1)–(e4) | bỏ hoặc hoãn | 0 |

## 6. Khuyến nghị

### 6.1 Làm gì trong bài
1. **Một đoạn ngắn "vì sao không dùng KG"** trong Related Work hoặc Discussion. Bản nháp tiếng Anh, mọi số đều có nguồn ở trên:
   > We do not use an external knowledge graph. KTVIC references contain no proper names (0 of 2,790 test captions), and named-entity, non-visual and culture-specific content carries 4.9% of their CIDEr-D mass. Reported KG gains on COCO shrink to a median of +1.4 CIDEr at baselines of 130–140 and +0.9 above 140. Vietnamese resources do not supply usable relations: ConceptNet 5.7 has no IsA or commonsense edge with a Vietnamese node, and 72% of uncurated Wikidata IsA pairs over our vocabulary end in three generic concepts. KG-style edits chosen on disjoint references change CIDEr by −2.5 to 0.0.
2. **Mục phân tích (d1):** bảng phân rã khoảng cách P1–người theo hiện tượng, có đối chứng người và chế độ giữ lại [N1 §3; K3 §2–3]. Đây là phần riêng của tiếng Việt duy nhất còn đứng được. Nó cũng giải thích vì sao đòn bẩy nằm ở RL và đích huấn luyện.
3. **Một câu giới hạn về CHAIR:** lexicon chỉ thấy 42% mention danh từ [K2 §4.1]. Báo kèm ảo giác mức danh từ so với panel.
4. **Tùy chọn, sau các lượt chính:** ablation term object lexicon tay trong CN-RLOO, kiểm trên nhãn COCO và panel. Không đặt vào phần đóng góp.
5. **GPU:** dành cho CN-RLOO và MBR tổ hợp adapter (MR5 đã bị loại theo D6), không dành cho KG [K3 §5].

### 6.2 Không được claim
- "RL/SCST đầu tiên cho captioning tiếng Việt": sai. ObjectAoA (2023), lời giải UIT cho VieCap4H (2022) và baseline UIT-OpenViIC đều dùng SCST [K2 §5]. Cách viết an toàn: "chưa tìm thấy RL trên CIDEr cho LVLM QLoRA trên KTVIC".
- "Dữ liệu scene graph tiếng Việt đầu tiên": thuộc về VietSGG [K2 §5].
- "KB văn hóa Việt đầu tiên cho VLM": thuộc về VietMEAgent (FAIR 2025) [K2 §5].
- "KG cải thiện captioning tiếng Việt": không có bằng chứng. Trên KTVIC, mọi biến thể đo được cho C ≈ 0 hoặc âm (mục 4).
- "RAVENEA: RAG văn hóa +11% cho captioning": đó là RegionScore; CIDEr giảm 22.2 → 8.5 [K1 §6].
- "ConceptNet phủ commonsense tiếng Việt": 0 cạnh IsA, 0 cạnh commonsense [K2 §4.3].
- Mọi câu "chưa ai làm" phải viết là "chưa tìm thấy" [KH].

### 6.3 Công trình liên quan phải trích
- Tiếng Việt: ViG (MAPR 2026), HDUCap (JVCIR 2026), bài KG-captioning ở FAIR 2025, ObjectAoA, VieCap4H, UIT-OpenViIC, VietSGG, VietMEAgent, KTVIC, UIT-ViIC. Phải đọc ba bài ViG, HDUCap và FAIR 2025 trước khi nộp. Các agent chưa thấy số của ViG, chưa có tóm tắt của HDUCap, và chưa mở được PDF bài FAIR 2025 [K2 §7].
- Dòng KG trong captioning: VinVL, TSG, KnowCap, Zhao+ (TMM), MERGE. Dòng văn hóa: RAVENEA, CONCAP, CulturalGround. Reward đồ thị: SPIDEr, SC-Captioner, FoCUS. Ảo giác do CIDEr-RL: Rohrbach+ 2018, Dai+ 2023. Hypernym hóa: Conceptual Captions 2018.

## 7. Rủi ro và giới hạn của chính phân tích này
- **Oracle trên test.** Mọi số KTVIC tính trên dự đoán và mẫu test; chúng chỉ là ước lượng cỡ hiệu ứng. Oracle đọc tham chiếu test, nên là cận trên chẩn đoán. Ngưỡng cố định trước; không chỉnh trên test [K3 §6; N1 §8]. Giữ lại kiểu 1v4 cho caption người bị lệch âm, vì các caption láng giềng trong chuỗi diễn đạt nằm trong tham chiếu chấm [N1 §8].
- **Proxy RL.** Best-of-n và bước KL 1 nat trên mẫu T = 0.8 của chính sách SFT chỉ đo một bước, không phải một lượt RL đầy đủ. RL thật có thể khuếch đại cả hiệu ứng lẫn hack [K2 §3; N1 §8].
- **Một seed.** Tag GDINO (+1.1 / +2.5 C) là một seed; mỗi pilot dùng một seed SFT cho mỗi chính sách. SD giữa các seed P1 ~3.4; MDE 2.5–3.8 [R6].
- **API tài liệu bị giới hạn.** OpenAlex và Semantic Scholar trả 429; trang OJS của AAAI và IEEE Xplore không vào được [K1 §1]. Không có số của AKGMA (AAAI 2026) và K-DFIC (TCSVT 2025; "148.4" chỉ lấy từ kg_plan/01) [K1 §8]. Số đếm xu hướng là khớp từ khóa trong tóm tắt arXiv, có nhiễu; 2026 chưa đủ năm.
- **Gộp tài liệu.** Bảng 25 điểm gộp các bài khác loại, mỗi bài nhiều dòng; ρ chỉ là mô tả, p là xấp xỉ [K1 §8].
- **Danh sách tay.** Danh sách loại token, từ văn hóa và gazetteer có thể thiếu. Dời vài loại chỉ đổi tỉ lệ vài phần mười điểm [K3 §6].
- **Sự thật không hoàn hảo.** CHAIR dùng gold suy từ tham chiếu, nên là cận trên của ảo giác. Panel OpenViIC độc lập nhưng vẫn là tham chiếu; hai panel cộng lại bỏ sót ~16% object nhắc được [R5-01 §7].
- **Độ phủ tài nguyên.** Dùng khớp chuỗi chính xác. "Có trong tài nguyên" không có nghĩa là đúng nghĩa; kiểm nghĩa chỉ có cho COCO-80; pivot ConceptNet là cận trên [K2 §7].
- **Chưa xác minh.** Số của ViG; tóm tắt của HDUCap; nội dung bài KG ở FAIR 2025; venue của CAPTURE, MGRL-RSCC, CheXPO-v2 (preprint), NES (theo trang OJS), FGAIF (theo header PDF), VietSGG (theo README); số của CONCAP đọc từ heatmap; id của MsRAG. Wang, Beck & Cohn 2019 và một bài MDPI Electronics 2025 (142.6 C) chỉ thấy qua snippet, không dùng ở đâu [K1 §8; K2 §7].

## 8. Tài liệu tham khảo
Venue, năm và id theo [K1], [K2], [N1], [R3-01], [RW11]. Ký hiệu như mục 3.

KG, scene graph và concept trong captioning:
- VinVL — CVPR 2021 — arXiv 2101.00529
- VC R-CNN — CVPR 2020 — arXiv 2002.12204
- VSUA — ACM MM 2019 — arXiv 1908.02127
- GCN-LSTM — ECCV 2018 [nền] — arXiv 1809.07041
- Lee+ 2019 — arXiv 1909.09953 [chỉ arXiv, chưa thấy venue]
- Milewski+ — AACL 2020 [ngoài DS] — arXiv 2009.12313
- TSG — ACL 2023 — arXiv 2305.02177
- KnowCap — ACM MM 2023 — arXiv 2308.01126
- Zhao+, entity-aware captioning với KG đa phương thức — IEEE TMM (K1 ghi 2024, RW11 ghi 2023) — arXiv 2107.11970, DOI 10.1109/TMM.2023.3301279
- MERGE — AAAI 2026 — arXiv 2511.21002
- NOC-REK — CVPR 2022 — arXiv 2203.14499
- EVCap — CVPR 2024 — arXiv 2311.15879
- RA-Transformer — ACM TOMM 2024 — arXiv 2405.13127, DOI 10.1145/3663667
- REVEAL — CVPR 2023 — arXiv 2212.05221
- Kornblith+ — ICCV 2023 — arXiv 2307.16686
- AKGMA — AAAI 2026 — DOI 10.1609/aaai.v40i18.38532 [chưa đọc được toàn văn, không có số]
- K-DFIC — IEEE TCSVT 2025 — DOI 10.1109/TCSVT.2024.3525158 [chưa kiểm được số]

Văn hóa, đa ngữ, gọi tên:
- RAVENEA — ICLR 2026 — arXiv 2505.14462
- CONCAP — COLM 2025 [ngoài DS] — arXiv 2507.20411
- CulturalGround — EMNLP 2025 — arXiv 2508.07414
- MsRAG — IJCAI 2025 — [id chưa ghi trong báo cáo]
- VietMEAgent — FAIR 2025 [ngoài DS]
- Berger & Ponti — arXiv 2409.16646 [preprint]
- ManyNames — LREC 2020 [ngoài DS] — 2020.lrec-1.710
- Ordonez+, entry-level categories — ICCV 2013 [nền]
- Conceptual Captions — ACL 2018 [nền] — P18-1238
- Hypernymization of named entity-rich captions — arXiv 2304.13130 (2023) [tác giả chưa xác minh]

Reward đồ thị, RL và ảo giác:
- SPIDEr — ICCV 2017 [nền] — arXiv 1612.00370, DOI 10.1109/ICCV.2017.100
- MGRL-RSCC — arXiv 2609.26166 [preprint]
- RadGraph reward (Delbrouck+) — Findings EMNLP 2022 — arXiv 2210.12186
- CheXPO-v2 — arXiv 2512.17213 [preprint]
- SC-Captioner — ICCV 2025 — arXiv 2508.06125
- FoCUS — EMNLP 2026 — arXiv 2609.00709
- Re3Cap — EMNLP 2026 — arXiv 2608.21305
- Cho+ — Findings NAACL 2022 — arXiv 2205.13115
- ESREAL — ECCV 2024 — arXiv 2403.16167
- FGAIF — TMLR 2025 theo header PDF [venue chưa xác minh] — arXiv 2404.05046
- HALC — ICML 2024 — arXiv 2403.00425
- NES — AAAI 2026 theo trang OJS [venue chưa xác minh] — arXiv 2511.08909
- Rohrbach+, Object Hallucination in Image Captioning — EMNLP 2018 — arXiv 1809.02156
- Dai+, Plausible May Not Be Faithful — EACL 2023 — arXiv 2210.07688
- MOCHa — EMNLP 2024 (main, pp. 22680-22698) — DOI 10.18653/v1/2024.emnlp-main.1263 (corrected per CC-114 W11)

Đồ thị cho kiểm chứng, đánh giá, độ cụ thể:
- Reefknot — Findings ACL 2025 — arXiv 2408.09429
- FIHA — Findings ACL 2025 — arXiv 2409.13612
- RelCheck — arXiv 2609.27890 [preprint]
- KG-ViP — ACL 2026 theo Semantic Scholar — arXiv 2601.11632
- CART — ACM MM 2026 — arXiv 2607.16727
- DSG — ICLR 2024 — arXiv 2310.18235
- CompreCap — CVPR 2025 — arXiv 2412.08614
- PROVE — ICCV 2025 theo Semantic Scholar — arXiv 2410.13121
- DiscoSG — EMNLP 2025 — arXiv 2506.15583
- PoSh — ICLR 2026 — arXiv 2510.19060
- CAPTURE — arXiv 2405.19092 [preprint]
- DCScore — ICLR 2025 — arXiv 2503.07906
- CLC — NeurIPS 2025 — arXiv 2502.19110
- Taxonomy-Aware Evaluation of VLMs — CVPR 2025 — arXiv 2504.05457
- SpeciaRL — CVPR 2026 — arXiv 2603.03197

Tiếng Việt:
- KTVIC — arXiv 2401.08100
- UIT-ViIC — ICCCI 2020 — arXiv 2002.00175
- UIT-OpenViIC — Signal Processing: Image Communication (K2 ghi 2025; R5-01 ghi tập 140, 2026) — arXiv 2305.04166, DOI 10.1016/j.image.2025.117430
- ObjectAoA — VNU JCSCE 2023 — arXiv 2211.05405
- Lời giải UIT cho VieCap4H — VNU JCSCE 2022 — DOI 10.25073/2588-1086/vnucsce.371
- ViG — MAPR 2026 — DOI 10.1109/MAPR72750.2026.11685699 [chưa thấy số]
- HDUCap — J. Vis. Commun. Image Represent., 11/2026 — DOI 10.1016/j.jvcir.2026.104963 [chưa xác minh nội dung]
- Developing a Knowledge Graph for The Image Captioning Problem — FAIR 2025 — DOI 10.15625/vap.2025.0297 [chưa đọc được PDF]
- VietSGG — EAI GOODTECHS 2025 theo README — GitHub Moobbot/VietSGG [chưa thấy DOI]

Tài nguyên: Wikidata (CC0, truy vấn WDQS 12/10/2026); ConceptNet 5.7 (bản dump, CC BY-SA 4.0); OMW wn-wikt-vie (CC BY-SA 3.0 + GFDL); Kaikki, Wiktionary tiếng Anh, phần tiếng Việt (dump 03/10/2026, CC BY-SA + GFDL) [K2 §4].
