# 05. KG-RAG cho sinh mô tả ảnh (2025-2026): truy hồi, cách bơm tri thức, ảo giác và khả thi cho tiếng Việt

Agent 05, ngày 2026-10-10. Nguồn: trang arXiv abs (mở từng ID, đọc title/date/comments/abstract), IJCAI proceedings, IR Anthology, Wikidata API + SPARQL (truy vấn trực tiếp hôm nay), Hugging Face API, dữ liệu KTVIC có sẵn trong repo. Semantic Scholar và OpenAlex trả 429 cả phiên nên không dùng được để đối chiếu venue. Mục nào chỉ thấy qua snippet tìm kiếm thì để ở phần "Chưa xác minh".

**Tóm tắt ngắn.**
1. Retrieval-augmented captioning 2025-2026 chia ba nhánh. (i) Nhánh nhẹ: truy hồi caption/tên vật thể, ví dụ SmallCap và EVCap cùng các bản kế thừa. (ii) Nhánh truy hồi thực thể/tri thức cho LVLM: MsRAG (IJCAI 2025), MERGE (AAAI 2026), RAVENEA (ICLR 2026). (iii) Nhánh multimodal GraphRAG: MMGraphRAG, mKG-RAG (SIGIR 2026), MG²-RAG, MKG-RAG-Bench (KDD 2026). Nhánh (iii) gần như toàn làm VQA, **chưa có bài nào làm captioning**.
2. Khóa truy hồi đang dịch chuyển: trước đây là embedding cả ảnh (CLIP), nay là **embedding từng vùng/đối tượng** (MsRAG) và **thực thể đã căn chỉnh** (KBMR, ACM MM 2026). OCR là khóa mạnh nhưng gần như chưa ai khai thác cho captioning.
3. Tri thức được bơm vào gần như **chỉ dưới dạng văn bản trong prompt** của LVLM. Kiến trúc cross-attention riêng (SmallCap, EVCap) giờ chỉ còn ở nhánh mô hình nhỏ.
4. Retrieval **sinh ra ảo giác mới**: thực thể lạ chen vào caption (NES, AAAI 2026), mô hình chép token đa số (ACL 2024), ngữ cảnh truy hồi làm giảm attention lên ảnh (MAD-RAG, 2026), và xung đột tri thức (MMKC-Bench, CC-VQA CVPR 2026). Cách kiểm soát hiện nay đều là **lọc trước khi bơm** hoặc **can thiệp attention**. Chưa có bài nào **kiểm chứng từng thực thể truy hồi trên ảnh rồi mới quyết định mức cụ thể của từ được dùng**.
5. Với tiếng Việt, Wikidata đủ dùng ở mức *khái niệm văn hóa* (áo dài, nón lá, phở, xích lô đều có QID, nhãn và mô tả `vi`, có cạnh P279). Ở mức *thực thể cụ thể có ảnh* thì mỏng: chỉ ~7% item thuộc Việt Nam có P18. Phân cấp P279 lại có nhiễu.

---

## 1. Bài 2025-2026 (đã mở và xác minh)

| # | Bài | Venue (theo trường comments của arXiv hoặc proceedings) | ID | Khóa truy hồi | Cách bơm | Kiểm soát ảo giác |
|---|---|---|---|---|---|---|
| R1 | MsRAG: Knowledge Augmented Image Captioning with Object-level Multi-source RAG (Qiao et al., OPPO) | IJCAI 2025, DOI 10.24963/ijcai.2025/678 | proceedings/2025/678 | Tìm kiếm thị giác **theo từng đối tượng** (máy tìm kiếm ảnh online + CSDL miền offline), không cần câu hỏi người dùng | Kho template prompt chọn theo loại tri thức, cộng *visual prompting* để gắn đoạn văn bản vào đúng vùng ảnh | Căn chỉnh vùng-tri thức (Visual-RAG Alignment). Không có bước kiểm chứng |
| R2 | MERGE: Multimodal Entity-aware RAG for News Image Captioning | AAAI 2026 | 2511.21002 | Nội dung ảnh + bài báo, truy hồi động có dẫn hướng của ảnh vào KB đa phương thức hướng thực thể (EMKB) | Chiến lược nhiều bước "hypothesis caption" | Khớp thực thể-thị giác động |
| R3 | RAVENEA: Multimodal RAG Visual Culture Understanding | ICLR 2026 | 2505.14462 | 7 retriever đa phương thức trên 11.396 tài liệu Wikipedia do người xếp hạng | Tài liệu đưa vào context của 15 VLM, có tác vụ *culture-informed captioning* | Benchmark. Tác giả ghi nhận lợi ích khác nhau theo quốc gia |
| R4 | Negative Entity Suppression (NES) | AAAI 2026 (theo trang AAAI OJS 37705) | 2511.08909 | Ảnh tổng hợp để khóa ảnh→text nhất quán giữa train và test | Caption truy hồi | **Lọc "negative entity"** khỏi văn bản truy hồi, rồi **triệt ở mức attention**. Tác giả nói rõ retrieval "có thể làm ảo giác nặng hơn" |
| R5 | Re³Cap: Retrieval-Guided Refinement via RL | EMNLP 2026 Main | 2608.21305 | Truy hồi đa phương thức làm tín hiệu suy luận | Bộ gợi ý tinh chỉnh caption (CRS) và bộ đánh giá chất lượng (CQA) trong RL | Phát hiện ảo giác và thiếu sót qua bằng chứng truy hồi |
| R6 | DIR: Retrieval-Augmented Captioning with Comprehensive Understanding | arXiv 2024-12 | 2412.01115 | Đặc trưng ảnh, sửa thiên lệch do tối ưu theo caption GT | Khai thác văn bản truy hồi đầy đủ hơn (không chỉ caption thô hay object parse) | — |
| R7 | Hierarchical Multi-Modal Retrieval for Knowledge-Grounded News Image Captioning (M.-L. Nguyen, …, **Trung-Nghia Le**) | SOICT 2025 | 2606.18553 | Truy hồi bài báo theo cấu trúc (headline, body, vị trí ảnh) | VLM viết mô tả ngắn, cắt đoạn liên quan rồi LLM tổng hợp | Bước tinh chỉnh độ liên quan. Hạng 5 EVENTA 2025 |
| R8 | EVENTA Grand Challenge @ ACM MM 2025 (OpenEvents V1; nhóm **ĐH KHTN, ĐHQG-HCM**) | ACM MM 2025 | 2508.18904 | Track "Event-Enriched Image Retrieval and Captioning" | — | Cho thấy cộng đồng Việt Nam đã làm *retrieval + captioning*, nhưng **dữ liệu tiếng Anh** |
| R9 | MMGraphRAG | arXiv 2025-07 (v2 2026-03) | 2507.20804 | Scene graph của ảnh nối với KG văn bản qua SpecLink (spectral clustering) | Đường suy luận trên đồ thị | Thực thể và quan hệ tường minh. Làm **VQA, không làm captioning** |
| R10 | mKG-RAG | SIGIR 2026 | 2508.05318 | MLLM trích đồ thị + vision-text matching | Truy hồi hai tầng tài liệu→đồ thị | Lọc nội dung không liên quan. Làm KB-VQA |
| R11 | MG²-RAG | arXiv 2026-04 | 2604.04969 | Nút đa phương thức = thực thể text + vùng ảnh (entity-driven grounding) | Lan truyền độ liên quan trên đồ thị phân cấp | Giữ "atomic evidence" |
| R12 | MKG-RAG-Bench | KDD 2026 | 2606.26458 | Benchmark retriever trên MMKG | — | Kết luận: retrieval là nút cổ chai |
| R13 | KBMR: Entity-Aligned Retrieval for KB-VQA | ACM MM 2026 | 2608.21450 | Retriever **dựa trên MLLM**, ưu tiên định danh thực thể hơn tương tự bề mặt kiểu CLIP | — | Trọng số entity-consistency |
| R14 | KnowCoL: Open-domain Visual Entity Recognition with KGs | AAAI 2026 | 2510.13675 | Ảnh + mô tả, nhúng chung, có **phân cấp kiểu và quan hệ Wikidata** | — | Nhận dạng zero-shot trên nhãn QID (OVEN) |
| R15 | When RAG Hurts: Attention Distraction (MAD-RAG) | arXiv 2026-01 | 2602.00344 | — | — | Văn bản truy hồi **kéo attention khỏi ảnh** dù ngữ cảnh đúng. Can thiệp training-free bằng cách tách câu hỏi kép và trộn attention |
| R16 | CC-VQA: Conflict- and Correlation-Aware | CVPR 2026 | 2602.23952 | — | — | Suy luận xung đột lấy thị giác làm trung tâm, training-free |
| R17 | MMKC-Bench: Multimodal Knowledge Conflict | arXiv 2025-05 | 2505.19509 | — | — | Xung đột context-memory và inter-context |
| R18 | M²RAG + MM-RAIT | arXiv 2025-02 | 2502.17297 | Truy hồi tài liệu đa phương thức open-domain | Instruction tuning để MLLM dùng ngữ cảnh tốt hơn | Benchmark có **tác vụ captioning** |
| R19 | Gators @ AmericasNLP 2026 (cultural captioning) | arXiv 2026-05 | 2605.20626 | Truy hồi many-shot | Qwen2.5-VL sinh caption trung gian rồi dịch có RAG | Kết luận "retrieval phụ thuộc ngôn ngữ, chỉ có ích với corpus lớn đúng miền", là **cảnh báo cho tiếng Việt** |
| R20 | ViCLIP-OT: Vietnamese Image-Text Retrieval | Preprint nộp ESWA, arXiv 2026-02 | 2602.22678 | Retriever ảnh-văn bản tiếng Việt, thử trên UIT-OpenViIC/KTVIC | — | R@K trung bình 67,34% trên OpenViIC. Dùng làm **retriever tiếng Việt** được |
| R21 | Failing to See or Failing to Know? | arXiv 2026-07 | 2607.04683 | — | — | Tách lỗi "không nhận ra thực thể" khỏi lỗi "nhận ra nhưng không biết", định tuyến sang "entity support" hoặc "factual evidence" |

Nền (một dòng mỗi bài): SmallCap (CVPR 2023, 2209.15323) dùng cross-attention CLIP→GPT-2 trên caption truy hồi. EVCap (CVPR 2024, 2311.15879) dùng bộ nhớ (đặc trưng thị giác, tên vật thể) và prompt LLM bằng tên truy hồi, chỉ 3,97M tham số huấn luyện. Retrieval robustness (ACL 2024, 2406.02265) cho thấy SmallCap chép token xuất hiện trong đa số caption truy hồi. RoRA-VLM (2410.08876) dùng truy hồi hai tầng và mở rộng truy vấn neo vào ảnh. PopVQA (ACL 2025, 2412.14133) cho thấy độ chính xác tri thức thực thể tụt tới 18% khi thực thể được *nhìn* thay vì *đọc*.

---

## 2. Trả lời các câu hỏi của góc này

### 2.1 Retrieval được khóa bằng gì?
| Khóa | Đại diện 2025-26 | Ưu | Nhược với tiếng Việt |
|---|---|---|---|
| Embedding cả ảnh (CLIP/SigLIP) → caption/tài liệu | SmallCap, DIR, NES, RAVENEA | Đơn giản | Tương tự bề mặt, kéo về thực thể nhìn giống (KBMR chỉ ra). Datastore caption tiếng Việt nhỏ (KTVIC ~19K caption) |
| Embedding **vùng/đối tượng** → KB thực thể | MsRAG, MG²-RAG, MaskOVEN-Wiki (AAAI 2025, 2412.13614) | Đúng hạt mịn, gắn được vào vùng | Cần detector hoặc grounding. Qwen2.5-VL tự grounding được |
| **Thực thể đã nhận dạng** (QID) → subgraph | KnowCoL, MERGE, KBMR | Có cấu trúc, lấy được phân cấp P31/P279 | Nhận dạng thực thể Việt chưa có benchmark |
| **OCR / scene text** → khớp nhãn hoặc alias | (chưa thấy bài captioning 2025-26 nào dùng OCR làm khóa KG) | Biển hiệu "Phở", "Chợ Bến Thành" là bằng chứng *đọc được*, độ chính xác cao | Phải chuẩn hóa dấu. ViTextCaps (2604.27712) có sẵn dữ liệu |
| Bản nháp caption/câu hỏi → văn bản | R7 (VLM mô tả trước), RoRA-VLM | Không cần retriever ảnh | Lỗi của bản nháp lan sang truy hồi |

### 2.2 Tri thức KG được bơm vào transformer/LVLM thế nào?
- **Văn bản trong prompt** (phổ biến nhất 2025-26): MsRAG (template theo loại), RAVENEA, MERGE, R7, R19. Với LVLM có sẵn thì đây là cách duy nhất rẻ.
- **Cross-attention hoặc token tri thức qua module nhẹ**: SmallCap, EVCap. Hợp với mô hình nhỏ (Vintern-1B) khi muốn huấn luyện ít tham số.
- **Gắn tri thức vào vùng ảnh** (visual prompting, nút đa phương thức): MsRAG, MG²-RAG.
- **Đường đi trên đồ thị làm chuỗi suy luận**: MMGraphRAG, mKG-RAG. Chỉ có trong VQA.
- **Làm tín hiệu thưởng hoặc tinh chỉnh**: Re³Cap (RL).
- Kết luận: "bơm KG vào encoder" (kiểu GCN 2019-2022) **không còn là hướng chính**. Đổi mới hiện nay nằm ở **chọn cái gì được bơm**, không phải *bơm bằng cách nào*.

### 2.3 Retrieval sinh ra ảo giác gì, và kiểm soát ra sao?
| Loại ảo giác do retrieval | Bằng chứng | Kiểm soát hiện có |
|---|---|---|
| Thực thể truy hồi không có trong ảnh nhưng được chép vào caption | NES (AAAI 2026), Retrieval robustness (ACL 2024) | Lọc negative entity, triệt attention, lấy mẫu caption truy hồi đa dạng |
| Ngữ cảnh văn bản làm mô hình "bớt nhìn" ảnh | MAD-RAG (2602.00344) | Tách câu hỏi kép, trộn attention |
| Xung đột giữa tri thức truy hồi và tri thức tham số hoặc thị giác | MMKC-Bench, CC-VQA (CVPR 2026) | Suy luận xung đột lấy thị giác làm trung tâm |
| Nhầm thực thể nhìn giống | KBMR (ACM MM 2026) | Retriever MLLM có entity-consistency |
| **Sự thật phi thị giác** từ KG (lịch sử, xuất xứ) chen vào caption mô tả | Suy ra từ R2/R3/R7: các bài này *muốn* thêm bối cảnh. Với caption mô tả thuần (KTVIC) thì đó chính là ảo giác | **Chưa thấy bài nào lọc theo "thuộc tính có kiểm chứng được bằng mắt không"** |
| **Quá cụ thể** (gọi "bánh xèo" khi chỉ thấy "bánh") | Chưa thấy bài 2025-26 nào đo riêng loại này | Chưa có cơ chế lùi theo phân cấp. Gần nhất là hypernymization 2023 (2304.13130), làm cho pretraining, không phải suy luận |

### 2.4 Khả thi với tiếng Việt (đo hôm nay)
**Wikidata `vi`** (SPARQL, query.wikidata.org, 2026-10-10):
- Item có `P17 = Việt Nam`: 39.216. Trong đó **23.073** có nhãn `vi`, **14.433** có mô tả `vi`, nhưng **chỉ 2.845 có ảnh P18 (~7%)**. Hệ quả: bộ nhớ thị giác kiểu EVCap không dựng được từ riêng Wikidata, phải lấy ảnh từ crop KTVIC/OpenViIC.
- Item có `P495 (xuất xứ) = Việt Nam` và nhãn `vi`: 1.044.
- Khái niệm văn hóa đều có: áo dài Q252187, nón lá Q77910039, phở Q420646, bánh xèo Q50633, bánh chưng Q564567, xích lô Q1362895, múa rối nước Q747876, cà phê sữa đá Q2673042, chợ Bến Thành Q3232879. Số statement mỗi item mỏng, **8-16**.
- **P279 có nhưng nhiễu**: xích lô P279 ⊃ {xe đạp, tắc xi, xe kéo, **xe lăn**, tricycle}. Nhiều cha *không có nhãn `vi`* (pancake, noodle soup, headgear, coffee drink). Như vậy leo phân cấp phải theo **danh sách cha "an toàn" do người duyệt**, không leo tự do được.
- **Nhập nhằng khi tra nhãn**: `wbsearchentities("phở", vi)` trả **Q79007 "đường/street"** ở hạng 1, vì khớp không dấu với "phố". "thúng chai" trả một tiểu khu ở Thái Lan. **Không thể** linking bằng chuỗi thô; phải dùng chuỗi có dấu đầy đủ, lọc theo kiểu P31/P279, và kiểm chứng trên ảnh.

**Dữ liệu KTVIC trong repo** (`data/datasets/ktvic/*.json`, đếm chuỗi con trên caption chữ thường):
- Train có 3.769 ảnh và 18.845 caption. **12,8% ảnh train và 14,9% ảnh test** có ít nhất một từ khái niệm văn hóa (áo dài, nón lá, phở, xích lô, đèn lồng, chùa, đền, gánh...).
- Tần suất trên caption: chợ 4,2%, xe máy 4,1%, áo dài 1,25%, nón lá 1,18%, đèn lồng 1,0%, xích lô 0,47%, phở 0,38%.
- **Thực thể có tên riêng gần như bằng 0**: "hồ Gươm" và "Hoàn Kiếm" 0 lần, "Hà Nội" 6 lần, "Bến Thành" 12 lần. Caption tham chiếu UIT/KTVIC **không nêu tên riêng**, nên KG-RAG ở mức thực thể cụ thể **sẽ không được BLEU/CIDEr thưởng**, thậm chí có thể bị phạt. Giá trị thật nằm ở **mức khái niệm** (đúng "nón lá" thay vì "cái mũ") và ở **giảm ảo giác**.

**Công cụ có sẵn** (HF API): ViCLIP-OT (2602.22678, retriever tiếng Việt), `jinaai/jina-clip-v2` (đa ngữ), `google/siglip2-so400m-patch16-384`, `BAAI/bge-m3` (văn bản đa ngữ), `5CD-AI/Vintern-Embedding-1B` (tạo 2025-08, gắn tag visual-document-retrieval), `5CD-AI/ColVintern-1B-v1`. Tất cả chạy được trên RTX 3090.

**Đối thủ Việt Nam cần theo dõi**: nhóm Trung-Nghia Le (ĐH KHTN, ĐHQG-HCM) đã có EVENTA (ACM MM 2025) và R7 (SOICT 2025) về retrieval + captioning, cộng VNCultureVQA (xem phần Chưa xác minh). Đây là nhóm có khả năng làm "RAG captioning văn hóa Việt" sớm nhất.

---

## 3. Đề xuất: **ViVeriKG-RAG**, KG-RAG "kiểm chứng trước khi bơm" với lùi phân cấp

### 3.1 Ý tưởng
Coi mỗi thực thể truy hồi từ Wikidata là một **mệnh đề có kiểu chờ kiểm chứng**, đúng như VSPS đang làm với mệnh đề sinh từ ảnh. Thực thể chỉ được bơm vào bộ sinh caption ở **mức cụ thể mà verifier xác nhận được**. Mức này đi từ thực thể cụ thể → khái niệm → lớp cha "an toàn" → bỏ. Thuộc tính KG phi thị giác (xuất xứ, lịch sử) bị chặn khỏi caption mô tả.

### 3.2 Pipeline (1× RTX 3090)
1. **Sinh ứng viên đa khóa** (cho tăng recall):
   - (a) Vùng: Qwen2.5-VL-7B 4-bit grounding → crop → ViCLIP-OT/SigLIP2 so với **bộ nhớ thị giác-QID** dựng từ crop KTVIC/OpenViIC train. Tên vật thể lấy từ caption, link sang QID. Đây là EVCap nhưng khóa là QID, không phải chuỗi.
   - (b) **OCR**: chữ trên biển hiệu → khớp nhãn/alias `vi` có dấu đầy đủ.
   - (c) Danh từ trong bản nháp caption.
   - Ứng viên được lọc theo P31/P279 thuộc tập kiểu "nhìn thấy được" (trang phục, món ăn, phương tiện, công trình...).
2. **Dựng subgraph nhỏ**: nhãn `vi`, mô tả `vi`, chuỗi P279 tới một **danh sách cha an toàn** khoảng 300 nút do người duyệt (sửa nhiễu kiểu "xích lô ⊂ xe lăn"). Thuộc tính được gắn cờ `visual` (màu, hình dạng, vật liệu) hoặc `non-visual` (P17, P495, P571...).
3. **Kiểm chứng trước khi bơm**, dùng lại verifier VSPS (K=5 mẫu, 3 trạng thái) trên crop:
   - SUPPORTED: dùng nhãn cụ thể ("nón lá").
   - UNCERTAIN: **lùi lên cha an toàn gần nhất được SUPPORTED** ("bánh xèo" → "bánh" → "món ăn"). Đây là sự tổng quát hóa trực tiếp của trung tính hóa trong VSPS, khớp với ý 2(b) trong file 11.
   - REJECTED: đưa vào danh sách **negative entity**, dùng làm ràng buộc phủ định khi sinh (theo NES, nhưng nguồn negative là verifier chứ không phải tần suất).
4. **Bơm**: một khối văn bản có cấu trúc trong prompt ("Thực thể đã xác minh: …; Không xuất hiện: …"), chỉ chứa thuộc tính `visual`. Có hai chế độ:
   - (i) training-free cho Qwen2.5-VL/Qwen3-VL;
   - (ii) **SFT QLoRA**: caption mục tiêu VSPS được render lại với nhãn ở đúng mức đã kiểm chứng. Nhờ đó mô hình học được *khi nào nên cụ thể*, và lúc suy luận chỉ cần một lượt, không cần retrieval.
5. **Metric mới** (khớp với deliverable "new evaluation metrics"):
   - **Hierarchical Entity Precision/Recall (HEP/HER)** trên phân cấp an toàn: gọi đúng lớp cha được tính một phần, gọi lớp con sai thì phạt.
   - **Over-specificity rate**: tỉ lệ đề cập cụ thể hơn mức mà ảnh hoặc gold hỗ trợ.
   - **Non-visual KG leakage**: tỉ lệ câu chứa sự thật phi thị giác.
   - Cả ba đều tính được trên đồ thị VSPS (ý 1 của file 11).

### 3.3 Đánh giá đề xuất
| Tiêu chí | Đánh giá | Lý do |
|---|---|---|
| **Novelty** | **Trung bình-khá** (khoảng 6/10) | Từng mảnh đều có: truy hồi theo vùng (MsRAG), lọc negative entity (NES), nhận dạng thực thể dùng phân cấp Wikidata (KnowCoL), kiểm chứng mệnh đề (VSPS). Phần chưa thấy ở bài nào 2025-26 gồm (1) **trạng thái kiểm chứng của từng thực thể quyết định mức cụ thể theo phân cấp KG**, (2) **chặn thuộc tính KG phi thị giác** trong caption mô tả, (3) metric over-specificity/HEP, (4) tiếng Việt |
| **Feasibility** | **Cao** | Tra KG chạy trên CPU (SPARQL dump cục bộ khoảng 25K item VN + vài nghìn khái niệm). Verifier và Qwen 4-bit đã chạy trong VSPS. Việc tốn công nhất là duyệt danh sách cha an toàn (~300 nút, vài ngày) và gán nhãn mức cụ thể cho ~300-500 ảnh (12-15% ảnh KTVIC có khái niệm văn hóa, nên cần lấy mẫu có chủ đích) |
| **Overlap risk** | Trung bình | MsRAG và NES là gần nhất. Nhóm Trung-Nghia Le có thể ra bản RAG văn hóa Việt |
| **Rủi ro chính** | — | (1) Caption tham chiếu không nêu tên riêng, nên CIDEr khó tăng; phải báo HEP và human eval. (2) Gator (R19) cho thấy retrieval chỉ có ích với corpus đủ lớn đúng miền, mà datastore tiếng Việt nhỏ. (3) Nhiễu P279 và lỗi linking không dấu. (4) Verifier hiện chỉ đúng 63,1% ở trạng thái SUPPORTED (VSPS), nên lùi phân cấp có thể quá thận trọng |
| **Bài gần nhất** | MsRAG (IJCAI 2025), NES (AAAI 2026), KnowCoL (AAAI 2026), EVCap (CVPR 2024), RAVENEA (ICLR 2026); về phía kiểm chứng là AKGMA (AAAI 2026) và RelCheck (file 11) | |

Cách lồng vào kế hoạch chung: đề xuất này dùng chung đồ thị mệnh đề VSPS (file 11, ý 1) làm nền metric, và thay luật trung tính hóa thủ công bằng lùi phân cấp KG (file 11, ý 2b). Nên làm bản **training-free trước** để có số liệu, sau đó mới làm SFT.

---

## 4. Chưa xác minh
- **Enhanced EVCap: … with Additional Caption Memory** (Springer chapter 10.1007/978-3-032-18974-5_5, theo snippet là FICTA 2025, NoCaps CIDEr 119,5): trang Springer chuyển hướng sang đăng nhập, chưa mở được. Tác giả có thể là người Việt.
- **Retrieval-Augmented Image Captioning via Synthesized Entity-Aware Knowledge Representations** (L. Shen et al., CIKM 2025, DOI 10.1145/3746252.3761265): IR Anthology xác nhận có bài, nhưng ACM trả 403 nên chưa đọc abstract.
- **Zero-Shot Image Captioning with Multi-type Entity Representations** (Zeng et al., AAAI 2025, OJS 34386): chưa mở được trang.
- **VNCultureVQA** (WACV 2027 theo README GitHub phucGR09/VNCultureVQA; 28.655 bài báo, 691.830 cặp QA; Phan, Pham, Trung-Nghia Le): mới chỉ thấy README, chưa có proceedings.
- **ReCap** (multi-agent RAG cho captioning quan hệ, Knowledge-Based Systems 2025, ScienceDirect S0950705125020155): chỉ thấy qua snippet.
- Venue của MMGraphRAG và MG²-RAG: arXiv không ghi venue. Venue NES lấy theo OJS qua snippet.
- Không đối chiếu được với Semantic Scholar/OpenAlex (429 suốt phiên).
- Số đếm KTVIC dùng khớp chuỗi con ("bánh" gồm cả "bánh mì"). Đây là cận trên thô, chưa tách từ.
