# 11. Đồ thị tri thức (KG) và đồ thị cảnh (scene graph) trong sinh mô tả ảnh: xu hướng và hướng đi cho dữ liệu UIT

Ngày quét: 2026-10-10. Nguồn: OpenAlex API (đếm theo năm, lọc `title_and_abstract.search`), Semantic Scholar Graph API (venue, đếm đối chứng), arXiv API (mở trực tiếp từng ID). Mọi bài dưới đây đều đã được mở hoặc truy vấn qua API trong phiên này. Mục nào chưa xác minh được thì ghi ở phần "Chưa xác minh".

Câu hỏi: "Đồ thị tri thức trong sinh mô tả ảnh có phải chủ đề mới và đang nổi không? Có nên làm hướng này trên dữ liệu UIT không?"

**Trả lời ngắn:** "KG ngoài (ConceptNet/Wikidata) bơm vào bộ sinh caption" **không mới**. Hướng này có từ 2019-2021, còn ở thời LVLM thì gần như chỉ sống trong các miền hẹp (y tế, nghệ thuật, tin tức, viễn thám). Phần **đang tăng thật** là **biểu diễn có cấu trúc (scene graph, đồ thị mệnh đề) dùng để kiểm chứng, đánh giá và giảm ảo giác của LVLM**, cùng nhánh "knowledge-enhanced" captioning cho LMM. Tiếng Việt gần như **trống** ở cả hai nhánh. Nhánh thứ hai khớp trực tiếp với VSPS.

---

## 1. Bằng chứng xu hướng (số liệu)

### 1.1 OpenAlex: số công trình mỗi năm, khớp trong tiêu đề hoặc tóm tắt

Năm 2026 mới tính đến 10/10, nên số của năm này là **chưa đủ năm**.

| Truy vấn (boolean, title+abstract) | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026* | Xu hướng |
|---|---|---|---|---|---|---|---|---|---|---|
| `"knowledge graph" AND "image captioning"` | 4 | 3 | 7 | 3 | 5 | 10 | 16 | 22 | 18 | **Tăng** (x4 so với 2022), nền nhỏ |
| `"scene graph" AND "image captioning"` | 8 | 16 | 19 | 29 | 32 | 39 | 19 | 30 | 16 | **Đỉnh 2023, sau đó đi ngang hoặc giảm** |
| `commonsense AND "image captioning"` | 0 | 4 | 7 | 4 | 14 | 13 | 12 | 8 | 4 | **Giảm** từ 2022 |
| `("knowledge-enhanced" OR "knowledge-aware" OR "knowledge-guided") AND captioning` | 1 | 0 | 1 | 2 | 6 | 16 | 27 | 35 | 36 | **Tăng mạnh** (2026 đã vượt 2025) |
| `("entity-aware" AND captioning) OR "news image captioning"` | 2 | 2 | 9 | 4 | 7 | 13 | 10 | 9 | 13 | **Đi ngang** (~10/năm) |
| `"knowledge graph" AND hallucination AND (MLLM/LVLM/VLM)` | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 15 | 26 | **Mới nổi** (từ 0 lên 26) |
| `"scene graph" AND hallucination AND (vision-language/multimodal)` | 0 | 0 | 0 | 0 | 0 | 3 | 9 | 12 | 21 | **Mới nổi, tăng đều** |
| `"image captioning"` (mẫu số) | 388 | 567 | 575 | 728 | 887 | 1177 | 1450 | 1587 | 1209 | Tăng |

Đối chứng bằng Semantic Scholar (bulk search `"knowledge graph" +"image captioning"`, 2018-2026, tổng 62 bài): 3, 2, 6, 3, 5, 6, 11, 19, 7*. Hình dạng giống OpenAlex: tăng từ 2023 và đạt đỉnh 2025.

**Cách đọc số liệu:**
- KG+captioning chỉ chiếm khoảng **1,4%** số bài image captioning năm 2025 (22/1587). Hướng này tăng nhanh hơn mẫu số nhưng vẫn là ngách. Phần lớn các bài nhiều trích dẫn thuộc **miền hẹp**: báo cáo X-quang (MKCL, J. Biomed. Inform. 2023), viễn thám (TGRS 2023), gốm sứ hoặc nghệ thuật (KALE, IJCAI 2024), tin tức (TMM 2023).
- Scene graph cho captioning *kiểu cũ* (GCN encoder trên COCO) đã qua đỉnh năm 2023. Bài vẫn đều, nhưng không còn tăng.
- Thời LVLM (2023 trở đi) đổi vai của đồ thị. Đồ thị không còn là **đặc trưng đầu vào** của bộ sinh caption nữa, mà trở thành (i) **công cụ kiểm chứng/đánh giá** (FaithScore, DSG, FIHA, PROVE, CompreCap), (ii) **chuỗi suy luận trung gian** (CCoT: sinh scene graph trước rồi mới trả lời), (iii) **ngữ cảnh truy hồi để giảm ảo giác** (KG-ViP, RelCheck, VaLiK, AKGMA), (iv) **định dạng chú thích** (GBC: caption dạng đồ thị). Hai dòng "hallucination" trong bảng đi từ 0 lên 21-26 bài/năm, và đây là phần nổi thật.
- Lưu ý về nhiễu: truy vấn khớp trên title+abstract, nên có lẫn bài y tế hoặc công nghiệp chỉ nhắc đến captioning. Con số dùng để đọc **hình dạng đường cong**, không phải số tuyệt đối.

---

## 2. Bài tiêu biểu 2023-2026 (đã xác minh)

Ký hiệu: **[TOP]** = hội nghị đỉnh (CVPR/ICCV/ICLR/ACL/EMNLP/AAAI/IJCAI/ACM MM). **[J-Q1]** = tạp chí mà SJR thường xếp Q1 (cần kiểm tra lại hạng năm hiện hành trước khi trích). **[arXiv]** = chưa có venue.

### A. KG ngoài, bơm tri thức vào bộ sinh caption (hướng "cổ điển", nay chạy sang LMM)
| # | Bài | Venue/năm | Link | Phương pháp (1 dòng) |
|---|---|---|---|---|
| A1 | Boosting Entity-Aware Image Captioning With Multi-Modal Knowledge Graph | IEEE TMM 2023 **[J-Q1]** | https://doi.org/10.1109/tmm.2023.3301279 (arXiv 2107.11970) | Xây KG đa phương thức nối thực thể trong bài báo với ảnh để sinh caption tin tức đúng tên riêng. |
| A2 | KALE: An Artwork Image Captioning System Augmented with Heterogeneous Graph | IJCAI 2024 **[TOP]** | arXiv 2409.10921 | Đồ thị dị thể (tác giả, trường phái, chủ đề) làm ngữ cảnh cho VLM mô tả tranh. |
| A3 | Knowledge-Enhanced Image Captioning with Adaptive Graph-based Multimodal Alignment and LLM (AKGMA; G. Li et al.) | AAAI 2026 **[TOP]** | https://doi.org/10.1609/aaai.v40i18.38532 | KG thích nghi dẫn hướng căn chỉnh thị giác-tri thức cho LMM, nhắm vào "knowledge hallucination" với thực thể hoặc cảnh chưa thấy. |
| A4 | Aligning Vision to Language: Annotation-Free Multimodal KG Construction for Enhanced LLMs Reasoning (VaLiK) | ICCV 2025 **[TOP]** | arXiv 2503.12972 | Dựng KG đa phương thức không cần nhãn bằng chuỗi VLM mô tả ảnh rồi lọc, dùng cho suy luận của LLM. |
| A5 | MMCOMET: A Large-Scale Multimodal Commonsense Knowledge Graph | arXiv 2026-03 **[arXiv]** | arXiv 2603.01055 | Mở rộng ATOMIC2020 sang thị giác (hơn 900K bộ ba đa phương thức), thử trên kể chuyện bằng ảnh. |
| A6 | A unified framework for early childhood image captioning via knowledge-grounded metrics and process-level reinforcement (Z. Wang et al.) | Eng. Appl. of AI (Elsevier) 2026 **[J-Q1]** | https://doi.org/10.1016/j.engappai.2026.116162 | Metric dựa trên tri thức miền làm phần thưởng RL cho captioning chuyên miền. Đây là ví dụ cho thấy "KG + metric + RL" lên được tạp chí Q1. |
| A7 | VLCE: A Knowledge-Enhanced Framework for Image Description in Disaster Assessment | ALVR workshop @ACL 2026 | https://doi.org/10.18653/v1/2026.alvr-main.15 | Tri thức miền thiên tai bổ sung cho mô tả ảnh. |

### B. Truy hồi tăng cường (RAG) cho captioning, họ hàng gần của KG
| # | Bài | Venue/năm | Link | Phương pháp |
|---|---|---|---|---|
| B1 | SmallCap (Ramos et al.) | CVPR 2023 **[TOP]** | arXiv 2209.15323 | Truy hồi caption tương tự làm prompt cho bộ giải mã nhẹ. |
| B2 | EVCap (Li et al.) | CVPR 2024 **[TOP]** | arXiv 2311.15879 / https://doi.org/10.1109/cvpr52733.2024.01303 | Bộ nhớ ngoài gồm cặp (đặc trưng thị giác, tên đối tượng) cho captioning thế giới mở. |
| B3 | Towards Retrieval-Augmented Architectures for Image Captioning | ACM TOMM 2024 **[J-Q1]** | https://doi.org/10.1145/3663667 | Khảo sát và kiến trúc kNN-memory cho captioning. |

### C. Đồ thị làm trung gian suy luận hoặc ngữ cảnh để giảm ảo giác của LVLM (nhánh **nóng**)
| # | Bài | Venue/năm | Link | Phương pháp |
|---|---|---|---|---|
| C1 | Compositional Chain-of-Thought Prompting for LMMs (CCoT; Mitra et al.) | CVPR 2024 **[TOP]** | arXiv 2311.17076 | Cho LMM tự sinh scene graph dạng JSON rồi dùng đồ thị đó làm CoT để trả lời. Không cần nhãn SG. |
| C2 | KG-ViP: Bridging Knowledge Grounding and Visual Perception in MLLMs for VQA (Z. Li et al.) | ACL 2026 theo Semantic Scholar **[TOP]** | arXiv 2601.11632 | Hợp nhất scene graph (chi tiết thị giác) với commonsense graph (tri thức) qua truy hồi theo câu hỏi, giảm ảo giác tri thức. |
| C3 | RelCheck: Dual-Evidence Spatial Grounding for VLM Hallucination Correction | arXiv 2026-08 **[arXiv]** | arXiv 2609.27890 | Hậu xử lý không cần huấn luyện. Ghép bộ ba scene graph (RelTR), vị từ không gian từ bounding box và lớp claim kiểu Woodpecker thành "visual KB" rồi viết lại câu. |
| C4 | Beyond Generation: Multi-Hop Reasoning for Factual Accuracy in VLMs | ICML 2025 workshop (NewInML) | arXiv 2511.20531 | Duyệt KG nhiều bước để kiểm chứng và tinh chỉnh caption. |
| C5 | Reefknot: Relation Hallucination benchmark | Findings ACL 2025 **[TOP-Findings]** | arXiv 2408.09429 | Benchmark ảo giác *quan hệ*, dựng từ bộ ba scene graph, kèm cách giảm thiểu. |

### D. Đồ thị làm thước đo hoặc định dạng cho caption chi tiết (nhánh **nóng**, gần VSPS nhất)
| # | Bài | Venue/năm | Link | Phương pháp |
|---|---|---|---|---|
| D1 | FaithScore | Findings EMNLP 2024 | arXiv 2311.01477 | Tách câu trả lời thành atomic fact có kiểu (entity/attribute/relation...), kiểm chứng từng fact bằng VLM. |
| D2 | Davidsonian Scene Graph (DSG; Cho et al.) | ICLR 2024 **[TOP]** | arXiv 2310.18235 | Đồ thị câu hỏi nguyên tử có phụ thuộc cha-con (cha sai thì bỏ con). Dùng cho T2I eval. |
| D3 | FIHA: Hallucination Evaluation with Davidson Scene Graphs | Findings ACL 2025 | arXiv 2409.13612 | Tự động dựng câu hỏi theo DSG để đo ảo giác chi tiết của LVLM, không cần nhãn người. |
| D4 | PROVE: Programmatic VLM Evaluation in the Wild (Prabhu et al.) | ICCV 2025 theo Semantic Scholar **[TOP]** | arXiv 2410.13121 | Biến caption siêu chi tiết thành scene graph, cho LLM sinh QA kèm *chương trình* chạy trên đồ thị để kiểm chứng. Đo cả helpfulness lẫn truthfulness. |
| D5 | CompreCap: Benchmarking LVLMs via Directed Scene Graph (Lu et al.) | CVPR 2025 **[TOP]** | arXiv 2412.08614 | Ảnh được phân vùng thủ công, dựng scene graph có hướng, đo độ phủ đối tượng/thuộc tính/quan hệ của caption chi tiết. |
| D6 | DCScore / DeCapBench (Ye et al.) | ICLR 2025 **[TOP]** | arXiv 2503.07906 | Tách caption thành "đơn vị thông tin nguyên thủy", đo cả precision lẫn recall. |
| D7 | Graph-Based Captioning (GBC; Hsieh et al.) | arXiv 2024 (chưa có venue theo S2) | arXiv 2407.06723 | Caption dạng đồ thị có nhãn (nút thực thể, nút tổ hợp, nút quan hệ), mỗi nút là văn bản. Dataset GBC10M. |
| D8 | FACTUAL: Faithful Textual Scene Graph Parsing | Findings ACL 2023 | https://doi.org/10.18653/v1/2023.findings-acl.398 | Benchmark và parser câu thành scene graph trung thực, làm nền cho SPICE/SoftSPICE. |
| D9 | DiscoSG: Discourse-Level Text Scene Graph Parsing | EMNLP 2025 (oral) **[TOP]** | arXiv 2506.15583 | Parse **caption nhiều câu** (caption chi tiết) thành scene graph bằng tinh chỉnh lặp. Cải thiện metric dạng SPICE cho caption dài. |
| D10 | Transforming Visual Scene Graphs to Image Captions (TSG) | ACL 2023 **[TOP]** | arXiv 2305.02177 | Đại diện cuối của dòng "SG làm đầu vào cho bộ sinh". |

Tóm lại về venue: nhánh C/D gần như toàn hội nghị đỉnh, từ 2024-2026, và liên quan trực tiếp đến **ảo giác của caption chi tiết**. Nhánh A lên tạp chí Q1 (TMM, EAAI) chủ yếu khi có **miền hẹp**.

---

## 3. Phía tiếng Việt

### 3.1 Dữ liệu (đã xác minh)
| Dataset | Nguồn | Ghi chú cho hướng KG/SG |
|---|---|---|
| UIT-ViIC | arXiv 2002.00175; ICCCI 2020 (LNCS) | Ảnh COCO thể thao, caption tiếng Việt. Không có SG hay KG. |
| UIT-OpenViIC | arXiv 2305.04166 (2023) | Ảnh đời sống Việt Nam. Không có SG. |
| KTVIC | arXiv 2401.08100 (2024) | Miền đời sống. VSPS đang dùng. |
| OpenViVQA | arXiv 2305.04183; Information Fusion 2023 **[J-Q1]** | VQA mở tiếng Việt. Có thể dùng làm nguồn câu hỏi kiểm chứng. |
| UIT-EVJVQA | arXiv 2302.11752; J. Comput. Sci. Cybern. 2023 | VQA đa ngữ Anh-Việt-Nhật. |
| ViTextVQA | arXiv 2404.10652; Expert Systems with Applications **[J-Q1]** | Chữ trong ảnh. |
| **ViTextCaps** (mới) | arXiv 2604.27712 (2026-04; N. N.-Y. Nguyen, A.-D. Nguyen, N. H. Nguyen, **K. V. Nguyen**, nhóm UIT) | 15.729 ảnh, 74.970 caption scene-text. Đề xuất **HSTFG/PhonoSTFG**, tức đồ thị *hợp nhất đặc trưng* (OCR, thị giác, ngữ âm), không phải KG tri thức. |

### 3.2 Bài KG/SG captioning tiếng Việt
- Quét OpenAlex (`Vietnamese AND ("scene graph" OR "knowledge graph") AND (image OR visual)`, 2020-2026) chỉ ra **2 kết quả**, đều không phải captioning. Quét arXiv (`Vietnamese AND ("scene graph" OR "knowledge graph")`) ra 4 kết quả, toàn là KG văn bản (sách lịch sử, tóm tắt, entity linking), **không có** captioning.
- Bài tiếng Việt duy nhất có "graph" + caption là **ViTextCaps/PhonoSTFG (2026)**. Bài này dùng đồ thị làm kiến trúc hợp nhất đặc trưng, không dùng KG hay scene graph ngữ nghĩa.
- **Chưa thấy** (sau khi quét cả OpenAlex lẫn arXiv): (i) Vietnamese Visual Genome hay bộ scene graph tiếng Việt; (ii) parser câu tiếng Việt thành scene graph; (iii) SPICE tiếng Việt; (iv) captioning tiếng Việt dùng KG ngoài; (v) đánh giá ảo giác tiếng Việt dựa trên đồ thị.

### 3.3 Khoảng trống
1. Không có **parser văn bản tiếng Việt thành scene graph** và **metric dạng đồ thị** (SPICE, CompreCap, DCScore) cho tiếng Việt. Mọi bài caption tiếng Việt vẫn báo BLEU/CIDEr.
2. Không có **benchmark ảo giác quan hệ/thuộc tính** cho caption chi tiết tiếng Việt (Reefknot, FIHA, PROVE chỉ có tiếng Anh).
3. Không có tài nguyên **commonsense đa phương thức** gắn ngữ cảnh Việt (áo dài, xe máy, chợ, nón lá) dù UIT-OpenViIC/KTVIC giàu những đối tượng này.

---

## 4. Đánh giá và hướng đi

### 4.1 Kết luận
- **"KG cho image captioning" nói chung thì trưởng thành, ngách, không mới.** Dòng commonsense/ConceptNet-captioning đã giảm sau 2022. Scene-graph-làm-đầu-vào đạt đỉnh 2023. Một bài theo kiểu "thêm ConceptNet vào encoder caption tiếng Việt" sẽ bị reviewer Q2 năm 2026 coi là cũ, và khó thắng được Qwen2.5-VL zero-shot.
- **"Đồ thị có cấu trúc để kiểm chứng, đánh giá và giảm ảo giác của LVLM" đang nổi** (từ 0 lên 21-26 bài/năm, toàn hội nghị đỉnh). Nhánh "knowledge-enhanced LMM captioning" (AKGMA, AAAI 2026) cũng đang tăng. Đây là góc **còn mới cho tạp chí Q2 năm 2026-2027**, nhất là khi chuyển sang tiếng Việt, vì hiện chưa có bài tiếng Việt nào.
- Lợi thế riêng của VSPS: **mệnh đề có kiểu (entity/attribute/action/count/relation) + trạng thái kiểm chứng 3 mức về bản chất là một scene graph đã kiểm chứng.** VSPS gần như đã có sẵn đồ thị. Chỉ cần gọi đúng tên và khai thác nó.

### 4.2 Ba ý tưởng cụ thể

**Ý tưởng 1: ViVSG, "Verified Scene Graph" từ VSPS, và metric recall dạng đồ thị cho caption tiếng Việt** (khuyên làm trước)
- Nội dung: gom các mệnh đề SUPPORTED/UNCERTAIN của mỗi ảnh thành đồ thị (nút = entity/attribute, cạnh = relation/action, mỗi nút hoặc cạnh mang trạng thái kiểm chứng và điểm tin cậy từ K=5 mẫu). Từ đồ thị này: (a) đo **graph precision/recall** cho caption sinh ra, tách theo loại (object/attribute/relation). Đây là bản tiếng Việt của CompreCap/DCScore và thay được recall dựa trên lexicon. (b) Áp **quy tắc phụ thuộc DSG**: cha REJECTED thì tự động bỏ con, giảm lời gọi verifier. (c) Công bố kèm tập ~500 ảnh KTVIC có scene graph người duyệt làm benchmark.
- Khả thi trên RTX 3090: cao. Không cần huấn luyện mới. Parse mệnh đề sẵn có thành đồ thị mất 0 GPU. Parser caption thành đồ thị dùng Qwen2.5-7B (4-bit) hoặc chính pipeline tách mệnh đề hiện có. Phần tốn là người duyệt 500 ảnh (khoảng 2-3 tuần, 2 người).
- Rủi ro: reviewer có thể nói "chỉ là đổi tên mệnh đề thành đồ thị". Phải chứng minh lợi ích đo được: tương quan với đánh giá người cao hơn CHAIR hoặc lexicon recall, và cắt giảm lời gọi verifier nhờ phụ thuộc cha-con. Ngoài ra, parse tiếng Việt có thể lỗi ở từ ghép hay loại từ ("con", "chiếc").
- Gần nhất: CompreCap (CVPR 2025), DCScore (ICLR 2025), DSG (ICLR 2024), FIHA (Findings ACL 2025), GBC (arXiv 2407.06723), DiscoSG (EMNLP 2025).

**Ý tưởng 2: KG commonsense hỗ trợ kiểm chứng và trung tính hóa mệnh đề (KG-VSPS)**
- Nội dung: dùng tri thức có cấu trúc ở **ba điểm** của VSPS. (a) **Hard negative**: lấy các đối tượng hay đồng xuất hiện nhưng *không có* trong ảnh (prior đồng xuất hiện từ COCO/Visual Genome, hoặc cạnh `AtLocation`/`RelatedTo` của ConceptNet) để tạo truy vấn phủ định khó cho verifier. Việc này nhắm vào hiện tượng 63,1% SUPPORTED đúng. (b) **Trung tính hóa theo phân cấp IsA**: thay luật thủ công kiểu "người phụ nữ → người" bằng việc leo một bậc hypernym trong KG (chó → con vật, xe tay ga → xe máy). Cách này tổng quát hóa cho mọi mệnh đề UNCERTAIN chứ không chỉ giới tính. (c) **Lọc mệnh đề phi lý**: quan hệ vi phạm ràng buộc thường thức (người "đứng trên" máy bay đang bay) bị chuyển xuống UNCERTAIN.
- Khả thi: trung bình đến cao. Tra KG là CPU. Vintern-1B giữ nguyên. Phần chính là dựng bảng ánh xạ từ vựng tiếng Việt sang KG (lexicon đối tượng CHAIR tiếng Việt đã có, chỉ cần map sang khái niệm).
- Rủi ro: độ phủ tiếng Việt của ConceptNet chưa xác minh được hôm nay (API trả 502), có thể phải đi qua tiếng Anh. Lợi ích của (b) khó đo nếu không có đánh giá người. Prior đồng xuất hiện có thể *tăng* ảo giác nếu dùng sai chiều.
- Gần nhất: KG-ViP (ACL 2026), RelCheck (arXiv 2609.27890), C4 multi-hop KG (arXiv 2511.20531), AKGMA (AAAI 2026). Về trung tính hóa thì xem ../novelty/04_gender_neutral_captioning.md.

**Ý tưởng 3: ViSGParse + benchmark ảo giác quan hệ tiếng Việt (ViReefknot/ViFIHA)**
- Nội dung: (a) xây parser caption tiếng Việt thành scene graph (bản tiếng Việt của FACTUAL/DiscoSG): gán nhãn 1.000-2.000 caption UIT-OpenViIC/KTVIC thành bộ ba, rồi fine-tune một mô hình nhỏ (ViT5 hoặc Qwen2.5-1.5B). (b) Từ scene graph này sinh câu hỏi có/không theo kiểu DSG để dựng **benchmark ảo giác quan hệ và thuộc tính cho caption chi tiết tiếng Việt**. (c) Đánh giá Vintern, Qwen2.5-VL và VSPS trên benchmark này.
- Khả thi: cao về GPU (fine-tune 1.5B trên 3090 mất vài giờ), nhưng **tốn công gán nhãn** nhiều nhất trong ba ý.
- Rủi ro: đây là bài "tài nguyên + benchmark", hợp với TALLIP hoặc LREC-COLING hơn là bài phương pháp. Có thể bị nói "dịch FACTUAL". Phải nhấn mạnh hiện tượng riêng của tiếng Việt: loại từ, từ ghép, quan hệ giới từ ("ở trên", "bên cạnh"). Nhóm UIT (ViTextCaps) có thể làm song song, nên cần liên hệ hoặc kiểm tra định kỳ.
- Gần nhất: FACTUAL (Findings ACL 2023), DiscoSG (EMNLP 2025), Reefknot (Findings ACL 2025), FIHA (Findings ACL 2025), PROVE (ICCV 2025).

### 4.3 Gợi ý cách đóng khung
- Cho bản mở rộng Q2 của VSPS: lấy **ý 1** làm đóng góp phụ (metric graph-recall + phụ thuộc DSG), và (b) của **ý 2** (trung tính hóa theo IsA) làm phần mở rộng phương pháp. Không cần đổi câu chuyện chính.
- Cho bài mới riêng năm 2027: **ý 3**, dùng ViTextCaps/UIT-OpenViIC làm dữ liệu chính.
- Tránh: "GCN trên scene graph + ConceptNet để sinh caption tiếng Việt". Kiểu này cũ, và không vượt được LVLM.

---

## 5. Chưa xác minh / hạn chế
- Độ phủ tiếng Việt của ConceptNet 5: API `api.conceptnet.io` trả 502 ngày 2026-10-10, nên chưa kiểm chứng được số khái niệm tiếng Việt. Wikidata có nhãn `vi` nhưng chưa đếm.
- Venue của PROVE (ICCV 2025) và KG-ViP (ACL 2026) lấy theo trường `venue` của Semantic Scholar, chưa đối chiếu với proceedings.
- Hạng Q của tạp chí ghi "thường xếp Q1" theo hiểu biết chung về SJR, cần tra SJR năm 2025 trước khi trích.
- Số đếm OpenAlex có nhiễu (bài y tế hoặc công nghiệp chỉ nhắc captioning). Năm 2026 chưa đủ năm.

## 6. Truy vấn theo dõi (chạy lại hằng tháng)
1. OpenAlex: `filter=title_and_abstract.search:"scene graph" AND hallucination AND ("vision-language" OR multimodal),publication_year:2026&group_by=publication_year`
2. OpenAlex: `title_and_abstract.search:"knowledge graph" AND hallucination AND ("multimodal large language model" OR "vision-language model" OR LVLM OR MLLM)`
3. arXiv API: `abs:Vietnamese AND (abs:"scene graph" OR abs:"knowledge graph" OR abs:caption)`, sắp theo ngày nộp
4. arXiv API: `abs:"scene graph" AND (abs:"detailed caption" OR abs:"dense caption")`
5. Semantic Scholar: theo dõi trích dẫn của CompreCap (arXiv 2412.08614), DiscoSG (2506.15583), ViTextCaps (2604.27712)
