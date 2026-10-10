# 18. Venue và chuẩn thực nghiệm cho hướng KG/scene graph + captioning/VLM (2025-2026)

Ngày: 2026-10-10. Agent 18. Góc nhìn: các bài KG/scene graph + captioning/VLM năm 2025-2026 được đăng ở đâu, và mỗi loại venue đòi chuẩn thực nghiệm nào. Đối chiếu với `../cfp/*.json` để chọn 3 venue và lập lịch cho (i) bài metric/dataset và (ii) bài phương pháp/mô hình.

Nguồn đã dùng trong phiên này:
- Semantic Scholar Graph API: bulk search 2025-2026 cho 5 truy vấn, cùng `paper/batch` để lấy venue và abstract của 35 bài.
- arXiv HTML (`arxiv.org/html/<id>`): đọc caption các bảng và các câu nói về human eval của 10 bài chính, cộng 25 bài giảm ảo giác đã có sẵn trong scratchpad.
- Các file CFP `01..04_*.json`, do agent CFP đã xác minh trên trang chính thức.

OpenAlex hết ngân sách API hôm nay (429), nên phần đếm ở mục 1 chỉ dựa vào Semantic Scholar.

---

## 1. Các bài 2025-2026 được đăng ở đâu

### 1.1 Phân bố venue (Semantic Scholar bulk search, 2025-2026)

| Truy vấn | Tổng | arXiv hoặc chưa có venue | Venue có ≥2 bài, cùng các venue đáng chú ý |
|---|---|---|---|
| `"scene graph" +caption*` | 82 | 33 | AAAI 2, ICME 2, ICML 2, IEEE TMM 2, TCSVT 2, SIVP 2, IEEE Access 2; ngoài ra có NeurIPS, SIGIR, TIP, TGRS, Neurocomputing, EAAI, ESWA, mỗi venue 1 |
| `"knowledge graph" +caption*` | 51 | 16 | TGRS 2; ngoài ra có ICCV, ACM MM, AAAI, CIKM, ICMR, ICASSP, KBS, Multimedia Systems, ACIIDS, mỗi venue 1 |
| `"scene graph" +hallucination` | 39 | 20 | AAAI 3, ACL 2 (FIHA Findings 2025, KG-ViP 2026), SIGIR 2; ngoài ra có EMNLP, IJCAI, ICME, mỗi venue 1 |
| `"knowledge graph" +hallucination +(multimodal…)` | 103 | 19 | Phần lớn là MDPI hoặc bài ứng dụng (Applied Sciences 4, Electronics 2); Information Fusion 2, AAAI 2; ICCV và WWW mỗi venue 1 |
| `"caption evaluation" \| "captioning metric" …` | 77 | 24 | **ACL 6**, AAAI 3, **EMNLP 2**, NeurIPS 2, IEEE TMM 2, NAACL 1 |

Cách đọc bảng (đây là phân bố, không phải số tuyệt đối, vì bulk search của S2 chỉ khớp từ khóa):
- **Bài metric/benchmark caption tập trung ở \*ACL** (ACL, EMNLP, NAACL, gồm cả Findings) và AAAI/NeurIPS. Tạp chí duy nhất xuất hiện lặp lại là IEEE TMM.
- **Bài KG/SG dùng làm phương pháp chia hai nhóm.** Nhóm hội nghị CV/AI (ICCV, AAAI, ICML, ACM MM) nhận bài gắn với LVLM. Nhóm tạp chí (TMM, TCSVT, TIP, KBS, ESWA, EAAI, TGRS, Neurocomputing, SIVP) nhận bài có **miền hẹp**, chẳng hạn viễn thám, nghệ thuật, video gấu trúc, trẻ em, hoặc bài kiến trúc encoder-decoder cổ điển trên COCO.
- Khoảng 40% số bài vẫn chỉ có trên arXiv. Hướng này đông người làm, và đăng arXiv sớm để giữ ưu tiên là điều bình thường.

### 1.2 Bài đại diện đã xác minh venue (S2 `paper/batch` hoặc DOI)

**Metric, benchmark, parser (dùng làm mẫu cho bài (i))**
| Bài | Venue | Ghi chú |
|---|---|---|
| CompreCap (arXiv 2412.08614) | CVPR 2025 | Scene graph có hướng do người gán, dùng làm benchmark caption chi tiết |
| DCScore / DeCapBench (2503.07906) | ICLR 2025 | Đơn vị thông tin nguyên thủy, đo precision và recall |
| CapArena (2503.12329) | ACL 2025 | Hơn 6.000 cặp so sánh do người vote |
| EXPERT (2506.24016) | ACL 2025 | Metric có giải thích theo cấu trúc |
| FIHA (doi 10.18653/v1/2025.findings-acl.622) | Findings ACL 2025 | Đánh giá ảo giác theo cấu trúc DSG |
| DiscoSG (2506.15583) | EMNLP 2025 | Parser scene graph cho caption nhiều câu |
| SPECS (2509.03897) | EMNLP 2025 | CLIPScore cho caption dài |
| Multilingual CLIPScore eval (2502.06600) | NAACL 2025 | Đánh giá caption đa ngữ, rất gần trường hợp tiếng Việt |
| DISCODE (2512.14420) | AAAI 2025 (theo S2) | Benchmark MCEval gồm 6 miền |
| L-CLIPScore (2507.08710) | IEEE TMM (doi TMM.2026.3665006) | Metric nhẹ, dùng được cả để huấn luyện |
| PROVE (2410.13121) | ICCV 2025 (theo S2) | QA kiểm chứng bằng chương trình chạy trên scene graph |

**Phương pháp KG/SG cho captioning/VLM (dùng làm mẫu cho bài (ii))**
| Bài | Venue |
|---|---|
| AKGMA, KG thích nghi cho captioning bằng LMM (doi 10.1609/aaai.v40i18.38532) | AAAI 2026 |
| SC-Captioner, reward RL tính từ tập object/attribute/relation lấy bằng scene-graph parsing (2508.06125) | ICCV 2025 |
| VaLiK, dựng MMKG không cần nhãn (2503.12972) | ICCV 2025 |
| ArtRAG, KG cộng RAG cho mô tả tranh (2505.06020) | ACM MM 2025 |
| SEAR, RAG kèm KG tỉa (doi 10.1145/3746252.3761265) | CIKM 2025 |
| Scene-graph consolidation cho video dài (2502.16427) | ICML 2025 |
| KG-ViP, scene graph cộng commonsense graph (2601.11632) | ACL 2026 (theo S2) |
| K-DFIC, knowledge divergence-focus (doi 10.1109/TCSVT.2024.3525158) | IEEE TCSVT 2025 |
| Video captioning dựa trên MMKG (doi 10.1016/j.knosys.2026.115568) | Knowledge-Based Systems 2026 |
| ViS2T, scene graph sang văn bản cho video gấu trúc (doi 10.1016/j.eswa.2026.133544) | ESWA 2026 |
| KG-grounded metric cộng RL cho caption về trẻ em (doi 10.1016/j.engappai.2026.116162) | EAAI 2026 |

**Phương pháp giảm ảo giác (chuẩn baseline/benchmark mà reviewer sẽ đối chiếu)**
| Bài | Venue (S2) |
|---|---|
| VISTA (2502.03628) | ICML 2025 |
| REVERSE (2504.13169) | NeurIPS 2025 |
| SPIN (2505.16411) | EMNLP 2025 |
| ONLY (2507.00898) | ICCV 2025 |

**Tiền lệ tiếng Việt (S2, 2025-2026)**
| Bài | Venue |
|---|---|
| UIT-OpenViIC (doi 10.1016/j.image.2025.117430) | **Signal Processing: Image Communication 2025** |
| HDUCap, spatially-aware transformer (doi 10.1016/j.jvcir.2026.104963) | **JVCIR 2026** |
| ViG, grounded adaptation cho captioning tiếng Việt tài nguyên thấp (doi 10.1109/MAPR72750.2026.11685699) | **MAPR 2026** |
| AutoViVQA (2603.09689) | ACIIDS 2026 |
| ViTextCaps (2604.27712) | vẫn chỉ có arXiv |

Kết luận: captioning tiếng Việt đã vào được tạp chí Q2 về thị giác (SPIC, JVCIR) bằng bài **dataset kèm kiến trúc**. Chưa có bài tiếng Việt nào về graph/KG ở \*ACL hay MM.

---

## 2. Chuẩn thực nghiệm 2025-2026 (đọc từ bảng và mục human eval của chính các bài)

### 2.1 Bài metric/dataset
| Bài | Dữ liệu người gán | Đối chứng / metric so sánh | Human eval / tương quan | Phần thêm |
|---|---|---|---|---|
| CompreCap (CVPR 25) | Phân vùng thủ công, scene graph có hướng | 10 LVLM | Tương quan với điểm người (Bảng 3); hiệu năng của người làm trần | Kèm QA (CompreQA) và LLM chấm trực tiếp |
| DCScore (ICLR 25) | DeCapBench | BLEU-4… so với các metric dựa trên mô hình | PCC, Kendall, Spearman (Bảng 1) | Dùng metric làm phản hồi cho preference optimization trên nhiều VLM |
| CapArena (ACL 25) | Hơn 6.000 cặp vote | 14 VLM và người; metric cổ điển và VLM-as-judge | Đo ở cả mức caption lẫn mức hệ thống | Bản tự động CapArena-Auto đạt tương quan 94,3% với xếp hạng người |
| PROVE (ICCV 25) | 10,6k QA trên DOCCI | Nhiều VLM | 3 người mỗi mẫu, 100 ảnh/170 QA; Pearson 0,81 và 0,45 | Đo cả helpfulness lẫn truthfulness |
| DiscoSG (EMNLP 25) | 400 cặp do chuyên gia gán + 8.430 cặp tổng hợp; 2 người gán, đồng thuận 90% | Sent+Merge, FACTUAL-T5, GPT-4o | Kendall/Spearman trên DetailCaps và CapArena (SPICE: 40,7→42,2 và 36,3→40,7) | Nhanh hơn GPT-4o 86 lần; đếm lỗi bằng GPT-4o, đối chiếu với đếm tay |
| SPECS (EMNLP 25) | Không có tập người gán mới | Metric RS và metric LLM | PCC, 1−R², Kendall, Spearman; kiểm cả trên COCO/Flickr | So sánh chi phí với metric LLM |
| EXPERT (ACL 25) | 42k giải thích | Các metric có giải thích (FLEUR…) | Human eval chất lượng giải thích | Bảng thời gian suy luận và chi phí GPT-4o |
| SC-Captioner, phần metric (ICCV 25) | RefinedCaps 6,5K | BLEU-4, METEOR, CAPTURE | 100 ảnh, 4 người xếp hạng; Kendall 45,99 so với CAPTURE 37,66 | Tách điểm theo object/attribute/relation |
| Multilingual CLIPScore (NAACL 25) | VICR dịch máy sang 9 ngôn ngữ, cộng XVNLI và MaRVL | Nhiều CLIP | Tương quan với xếp hạng người theo từng ngôn ngữ | Có cả kiểm tra trên dữ liệu đa ngữ gốc |
| ViTextCaps (arXiv 26, tiếng Việt) | 15.729 ảnh | — | 5 người audit 500 cặp, phân tích đồng thuận giữa người gán | Phân tích hiện tượng riêng của tiếng Việt (va chạm dấu thanh) |

**Ngưỡng tối thiểu rút ra cho một bài metric/dataset tiếng Việt năm 2027:**
1. Có tập vàng do người gán: **400-1.000 mục**, ít nhất 2 người gán, báo cáo đồng thuận (κ hoặc % agreement).
2. Đo tương quan với người theo **Kendall τ, Spearman và Pearson**, ở **cả mức caption lẫn mức hệ thống**. So với ít nhất 6-8 metric: BLEU, METEOR, CIDEr, SPICE (hoặc bản Việt), CLIPScore đa ngữ, CAPTURE/DCScore, và một LLM-as-judge.
3. Benchmark **≥10 VLM**: Vintern-1B/3B, Qwen2.5-VL, Qwen3-VL, InternVL, cùng 1-2 model đóng nếu có. Lấy hiệu năng của người làm trần.
4. Có bảng chi phí/tốc độ so với GPT-4o hoặc LLM-judge. Đây đã thành mục chuẩn từ DiscoSG, SPECS và EXPERT.
5. Điểm cộng: dùng metric làm reward hoặc bộ lọc dữ liệu và cho thấy lợi ích ở downstream (DCScore, SC-Captioner).
6. Phân tích hiện tượng riêng của tiếng Việt (loại từ, từ ghép, giới từ không gian) để chặn nhận xét "chỉ là bản dịch".

### 2.2 Bài phương pháp/mô hình
| Bài | Dữ liệu | Baseline / backbone | Metric | Human eval / phần thêm |
|---|---|---|---|---|
| K-DFIC (TCSVT 25) | MSCOCO Karpathy | SOTA encoder-decoder | Bộ COCO, CIDEr-D 148,4 | Ablation, minh họa |
| SEAR (CIKM 25) | MSCOCO, Flickr30k, NoCaps (in-domain và out-of-domain) | RAIC nhẹ và nặng | Bộ COCO | — |
| ArtRAG (MM 25) | SemArt, Artpedia | Baseline huấn luyện nặng; bản thân ArtRAG không cần huấn luyện | Bộ caption | **Có human eval** |
| AKGMA (AAAI 26) | Dataset mới UniKnowCap | "Baselines across multiple metrics" (chi tiết chưa đọc) | Đo độ chính xác tri thức và độ nhất quán chi tiết | — |
| SC-Captioner (ICCV 25) | DOCCI500, COCO-LN500 | Qwen2-VL-7B cùng nhiều model khác; so với DPO | BLEU-4, METEOR, CAPTURE, cộng 7 khía cạnh của metric mới | Human Kendall |
| KG-ViP (ACL 26) | FVQA 2.0+, MVQA | Các phương pháp VQA | Accuracy | — |
| ONLY (ICCV 25) | POPE, CHAIR, MME-Hall, LLaVA-Bench, MMBench, MM-Vet | Nhiều phương pháp không huấn luyện | Chấm bằng GPT-4V | **Latency và bộ nhớ GPU đỉnh**, 3 seed |
| SPIN (EMNLP 25) | CHAIR, POPE nhiều lượt, MME, MMMU | 3 LVLM (có Qwen2) | Chấm accuracy và detailedness bằng GPT-4o | Kiểm tra giữ năng lực chung |
| REVERSE (NeurIPS 25) | CHAIR, CLAIR, HaloQuest, MMHal, AMBER, POPE, MME | Nhiều phương pháp giảm ảo giác | Có 95% CI | Bảng hiệu quả |
| VISTA (ICML 25) | CHAIR, POPE, MME | 4 LVLM | — | Throughput và latency |

**Ngưỡng tối thiểu cho bài phương pháp KG/SG cho caption tiếng Việt năm 2027** (khớp với mục 3 của `00_TONG_HOP.md`):
1. **≥2-3 backbone**: Qwen2.5-VL-7B, Qwen3-VL-8B, Vintern-3B hoặc InternVL.
2. **≥4 baseline**: VCD cùng OPERA, DoLa hoặc ONLY/SPIN; một baseline RAG/KG kiểu SEAR hoặc ArtRAG; và SFT trên caption chưa kiểm chứng.
3. Metric gồm ba nhóm:
   - Nhóm cổ điển trên UIT-OpenViIC/KTVIC: BLEU, CIDEr.
   - Nhóm ảo giác: CHAIR, POPE, AMBER. Bản tiếng Việt lấy từ bài (i).
   - Metric đồ thị của bài (i).
4. Kiểm tra mô hình giữ năng lực chung (MME hoặc MMMU), có bảng latency/bộ nhớ, chạy 3 seed hoặc báo CI.
5. Human eval khoảng 200 ảnh, 3 người, báo κ.
6. Chỉ venue \*ACL/CVF mới đòi thêm kết quả tiếng Anh (COCO, DOCCI) để chứng minh tính tổng quát. Tạp chí Q2 thị giác chấp nhận bài chỉ có tiếng Việt, như tiền lệ SPIC 2025 và JVCIR 2026.

---

## 3. Đối chiếu với danh sách CFP (`../cfp/*.json`) tính từ hôm nay

Các mốc quá sớm hoặc rủi ro so với khối lượng việc:
- ARR 2026-10-12 cho NAACL/COLING: còn 2 ngày.
- CVPR 2027: 2026-11-16.
- SI của IJCV: 2026-11-01.
- SI của Displays và J. Imaging: 2026-10-31.
- ICME 2027: khoảng 2026-12-15, chưa xác minh.

Ứng viên thực tế:
| Venue | Hạn (nguồn CFP) | Loại | Phù hợp với (i) / (ii) |
|---|---|---|---|
| ACL 2027 (ARR) | 2027-01-04, đã xác minh | CORE A*, có Findings | (i) chỉ khi kịp xong tập vàng, rất gấp |
| **EMNLP 2027 (ARR)** | khoảng 2027-05-15, **chưa xác minh** | A*, có Findings | **(i)**, đúng mẫu DiscoSG/SPECS/CapArena |
| **ACM MM 2027** | khoảng 2027-04-01, **chưa xác minh** | A* | **(ii)**, đúng mẫu ArtRAG/Entity-Faithful Repair; cũng nhận được (i) |
| IJCNN 2027 | 2027-01-31, đã xác minh | B | (ii) bản ngắn 6 trang, phương án dự phòng |
| ICMR 2027 | 2027-01-31 | B | (ii) hoặc (i) bản ngắn |
| **IP&M SI "Multilingual and Multimodal… Low Resource…"** | 2027-08-31, đã xác minh; review cuốn chiếu | Q1, IF 8.1 | **(i)**: CFP ghi rõ "dataset construction" và "VLM low-resource" |
| Pattern Recognition SI | 2027-03-31 | Q1 | (ii), lệch trọng tâm (representation learning) |
| Complex & Intelligent Systems collection | 2027-03-29 | Q1, OA | (ii) |
| **ACM TOMM** | cuốn chiếu | Q1 (SJR 0.925) | **(ii)**, tiền lệ: bài ảo giác LVLM đa ngữ của Qu et al. năm 2026 |
| **JVCIR** | cuốn chiếu | Q2/Q1 | **(ii)**, tiền lệ HDUCap (captioning tiếng Việt, 2026) |
| **TALLIP** | cuốn chiếu | Q2 | **(i)**, hợp về ngôn ngữ, hướng tài nguyên |
| LRE (Springer) | cuốn chiếu | chưa có quartile | (i) dạng resource paper |
| MAPR 2027 (UIT) | khoảng 2027-05-15, chưa xác minh | IEEE Xplore | Bản ngắn hoặc demo; tiền lệ ViG 2026 |

---

## 4. Khuyến nghị

### (i) Bài metric/dataset: "ViSG-Eval"
Nội dung gồm parser caption tiếng Việt thành scene graph, metric precision/recall dạng đồ thị, và benchmark ảo giác quan hệ/thuộc tính. Tương ứng ý 1 và ý 3 trong file 11.

| Thứ tự | Venue | Lý do |
|---|---|---|
| 1 (chính) | **EMNLP 2027 qua ARR khoảng 15/05/2027** (chưa xác minh; nếu chỉ vào Findings vẫn chấp nhận) | Các bài cùng loại năm 2025 (DiscoSG, SPECS, CapArena, EXPERT, Multilingual CLIPScore) đều lên \*ACL; chưa có bài graph-metric tiếng Việt nào |
| 2 (tạp chí Q1) | **IP&M SI Multilingual/Multimodal Low-Resource**, hạn 2027-08-31 | CFP ghi rõ việc dựng dataset và VLM cho ngôn ngữ ít tài nguyên. Review cuốn chiếu, nên nộp sớm thì có kết quả sớm |
| 3 (an toàn) | **ACM TALLIP** (Q2, cuốn chiếu) | Phù hợp ngôn ngữ nhất. Nếu bản mở rộng VSPS cũng dự định nộp TALLIP, đổi bài này sang LRE để tránh hai bài chồng nội dung ở cùng một tạp chí |

Lịch:
- **10/2026-12/2026**: viết guideline gán nhãn bộ ba tiếng Việt. Gán 500 ảnh KTVIC/UIT-OpenViIC, 2 người, đo κ. Seed lấy từ mệnh đề VSPS rồi người sửa, theo đúng quy trình DiscoSG.
- **01/2027-02/2027**: parser dùng Qwen2.5-1.5B (QLoRA) hoặc ViT5. Thu human judgment cho 300 ảnh × 8-10 hệ thống bằng xếp hạng hoặc so cặp. Chạy ≥10 VLM.
- **03/2027-04/2027**: bảng tương quan Kendall/Spearman/Pearson ở mức caption và mức hệ thống, so với ≥6 metric. Thêm bảng chi phí so với GPT-4o/LLM-judge. Đăng arXiv.
- **15/05/2027**: nộp ARR cho EMNLP 2027.
- **08/2027**: nếu meta-review yếu, chuyển bản mở rộng sang IP&M SI trước 31/08/2027. Nếu IP&M từ chối, nộp TALLIP hoặc LRE.

### (ii) Bài phương pháp: KG/SG-verified supervision cho LVLM tiếng Việt
Nội dung: đồ thị đã kiểm chứng, hard negative lấy từ KG, trung tính hóa mệnh đề theo phân cấp IsA. Tương ứng ý 2 trong file 11. Bài này đánh giá bằng metric của bài (i), nên phải đi sau (i) 1-2 tháng.

| Thứ tự | Venue | Lý do |
|---|---|---|
| 1 (chính) | **ACM MM 2027, khoảng 01/04/2027** (chưa xác minh) | KG cộng VLM captioning có tiền lệ ở MM (ArtRAG 2025, Entity-Faithful Repair 2026). Cộng đồng đa ngữ/đa phương thức mạnh |
| 2 (tạp chí Q1) | **ACM TOMM** (cuốn chiếu) | Có tiền lệ ảo giác LVLM đa ngữ. Đường MM sang TOMM (bản mở rộng) là lối quen thuộc nếu MM nhận bài |
| 3 (Q2 an toàn) | **JVCIR** (cuốn chiếu) | Tiền lệ trực tiếp: HDUCap (JVCIR 2026), UIT-OpenViIC (SPIC 2025). Không đòi kết quả tiếng Anh |

Lịch:
- **11/2026-02/2027**: làm KG-VSPS gồm hard negative từ đồng xuất hiện/ConceptNet, trung tính hóa theo IsA, lọc vi phạm commonsense. Huấn luyện QLoRA trên 3090 cho Qwen2.5-VL-7B, Qwen3-VL-8B và Vintern-3B.
- **02/2027-03/2027**: chạy ≥4 baseline (VCD, OPERA/DoLa, ONLY/SPIN, SFT không kiểm chứng, một RAG-KG). Đo CHAIR/POPE/AMBER bản Việt và graph metric của (i). Đo MME để kiểm tra giữ năng lực chung, đo latency/bộ nhớ, chạy 3 seed. Human eval 200 ảnh, 3 người.
- **khoảng 01/04/2027**: nộp ACM MM 2027 (chờ CFP chính thức). Phương án dự phòng sớm là IJCNN 2027 (31/01/2027), nhưng chỉ nộp nếu không định gửi MM, vì quy định cấm nộp trùng.
- **07/2027** (khi có kết quả MM):
  - Nếu MM nhận: chuẩn bị bản mở rộng TOMM với ≥30% nội dung mới.
  - Nếu MM từ chối: nộp TOMM ngay. Nếu muốn chắc tiến độ thì nộp JVCIR.

### Lưu ý chung
- **Dual submission**: bài FAIR 2026 là công bố trước. Cả (i) và (ii) phải tách bạch rõ với VSPS-v10 và với bản mở rộng VSPS. Mỗi bài cần một bảng nêu điểm khác so với FAIR 2026.
- Nhóm UIT (ViTextCaps) đang có dữ liệu và đồ thị cho caption tiếng Việt. Nên đăng arXiv (i) sớm, vào khoảng 04/2027, để giữ ưu tiên.

---

## 5. Chưa xác minh / hạn chế
- Hạn của EMNLP 2027, ACM MM 2027, ICME 2027 và MAPR 2027 chỉ là ước lượng theo năm trước (`verified:false` trong CFP JSON). Cần kiểm lại khi CFP chính thức ra.
- Venue của PROVE (ICCV 2025), KG-ViP (ACL 2026) và DISCODE (AAAI 2025) lấy theo trường `venue` của S2, chưa đối chiếu với proceedings.
- Chưa tra lại quartile năm hiện hành của TMM, TCSVT, KBS, ESWA và EAAI. Quartile trong bảng mục 3 lấy từ CFP JSON.
- Chưa đọc chi tiết bảng baseline của AKGMA (chỉ đọc abstract), K-DFIC, SEAR và KBS 2026.
- Đếm theo venue chỉ dùng S2 bulk search (khớp từ khóa, thiếu một số bài CVPR/ICLR). OpenAlex hết quota trong ngày nên chưa đối chứng được.
- NeurIPS Datasets & Benchmarks và LREC (hai venue hợp với bài (i)) không có trong `../cfp/`, nên chưa có hạn đã xác minh.
- Venue của KTVIC không tìm thấy trên S2 (chỉ có arXiv 2401.08100).
