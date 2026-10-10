# 09. Tri thức văn hoá trong VLM (2025-2026) và hướng "caption tiếng Việt trung thành văn hoá, có KG làm nền"

Ngày: 2026-10-10. Agent 09. Mọi bài trong mục 2 đã được mở trực tiếp trên trang arxiv.org/abs (đọc title, ngày, comments, abstract), hoặc trên ACL Anthology. Mục 3 và 4 là số đo **chạy trong phiên này** trên dữ liệu của repo. arXiv export API, OpenAlex và Semantic Scholar đều trả 429 (hết hạn mức) trong phiên, nên không có số đếm theo năm từ các nguồn đó.

## 0. Trả lời ngắn

1. **VLM có thất bại với thực thể văn hoá Việt không?** Có, nhưng kiểu thất bại không như giả định. Qwen2.5-VL-7B zero-shot gọi tên được các biểu tượng phổ biến, dễ thấy (nón lá, đèn lồng, áo dài): recall thuật ngữ văn hoá là 58,8% trên KTVIC test. Mô hình thất bại ở **thực thể đuôi dài** (xích lô 0/6). Nó còn **gán văn hoá thừa**: "áo dài" xuất hiện 45 lần mà không tham chiếu nào nhắc, ở chế độ detailed. Phát hiện quan trọng hơn: **chính VSPS xoá văn hoá**. Sau SFT, recall giảm từ 58,8% xuống 16,2% (short) và 23,5% (detailed). Nón lá giảm từ 12/21 xuống 0/21 (mục 4).
2. **Có KG văn hoá Việt không?** Không có KG văn hoá Việt công khai nào đúng nghĩa. Gần nhất là knowledge base gồm 156 thực thể của VietMEAgent (FAIR 2025, dùng cho VQA, không phải KG có quan hệ). Wikidata có item tiếng Việt cho phần lớn thực thể lớn, nhưng thiếu mục hoặc dễ nhầm với các vật thể đời thường (mục 5).
3. **Có mới không?** Ý tưởng "KG/RAG văn hoá cho VLM" **đã có** (CulturalGround EMNLP 2025, RAVENEA ICLR 2026, MosAIC NAACL 2025). Ý tưởng "KB văn hoá Việt" cũng **đã có** (VietMEAgent, FAIR 2025, tức đúng hội nghị của bạn). Phần **còn trống** là: (a) **caption** tiếng Việt chứ không phải VQA, (b) **kiểm chứng** thực thể văn hoá như một loại mệnh đề có kiểu trong pipeline giảm ảo giác, (c) **metric** đo đồng thời recall văn hoá và gán văn hoá thừa cho tiếng Việt. Mức mới: **trung bình**. Hướng chỉ đứng được nếu đóng khung là "giảm ảo giác mà không xoá văn hoá", không đóng khung là "thêm tri thức văn hoá".
4. **Khả thi trên UIT không?** **KTVIC: có**, khoảng 10-18% ảnh có thực thể văn hoá. **UIT-ViIC: không**, vì đây là ảnh COCO thể thao và guideline cấm ghi địa danh. **UIT-OpenViIC: có thể có** (ảnh crawl bằng từ khoá tiếng Việt), nhưng dữ liệu chưa có trong máy nên chưa đếm được. Test set KTVIC chỉ có **65 ảnh / 68 cặp (ảnh, thực thể)** đủ chắc. Cỡ đó quá nhỏ cho một benchmark, nên phải bổ sung tập đánh giá văn hoá riêng (mục 6).

---

## 1. Bối cảnh ngắn (trước 2025, mỗi mục một dòng)
- CIC (IJCAI 2024, arXiv 2402.05374): sinh câu hỏi theo hạng mục văn hoá → VQA → LLM viết caption văn hoá.
- MOSAIC-1.5k và Cultural Awareness Score (arXiv 2405.17475, 2024): metric đo mức "có ý thức văn hoá" của caption.
- Karamolegkou et al., HuCLLM@ACL 2024 (arXiv 2407.06177): caption VizWiz lọc theo văn hoá. Nhóm ghi nhận ảo giác và metric tự động lệch với đánh giá người.
- CVQA (NeurIPS 2024 D&B, 2406.05967), CulturalVQA (EMNLP 2024, 2407.10920), WorldCuisines (NAACL 2025 Best Theme Paper, arXiv 2410.12705 tháng 10/2024), Pangea (2410.16153).

## 2. Bài 2025-2026 đã xác minh

| # | Bài | Venue / ngày arXiv | Liên quan | Có Việt Nam? |
|---|---|---|---|---|
| 1 | **CultureVLM / CultureVerse** (2501.01282) | Technical report, 2025-01 | 19.682 khái niệm, 188 nước. Fine-tune VLM. Châu Á/Phi yếu hơn phương Tây | Không thấy "Vietnam" trong HTML |
| 2 | **GIMMICK** (2502.13766) | arXiv 2025-02 | 144 nước, 728 sự kiện/khía cạnh văn hoá, 6 task, 31 mô hình | Có, vài mục UNESCO của VN |
| 3 | **SEA-VL** (2503.07920) | arXiv 2025-03 (ACL 2025 theo trang dự án, **chưa xác minh venue**) | 1,28M ảnh văn hoá ĐNÁ. Crawl đạt khoảng 85% liên quan văn hoá. Ảnh sinh ra không phản ánh đúng văn hoá | Có. VN được nhắc là "cũng có mặt", không phải nhóm lớn |
| 4 | **RAVENEA** (2505.14462) | **ICLR 2026** | RAG đa phương thức cho cVQA và **culture-informed image captioning (cIC)**, 11.396 tài liệu Wikipedia | Không |
| 5 | **MAKIEval** (2505.21693) | EMNLP 2025 Findings | Liên kết thực thể văn hoá trong output với **Wikidata** để đo tự động. Chỉ có text | — |
| 6 | **CulturalFrames** (2506.08835) | EMNLP 2025 Findings | Kỳ vọng văn hoá ngầm hoặc tường minh trong T2I, kèm đánh giá metric | — |
| 7 | **CultureCLIP / CulTwin** (2507.06210) | COLM 2025 | Cặp khái niệm nhìn giống nhau nhưng khác văn hoá, dùng làm negative | — |
| 8 | **CulturalGround / CulturalPangea** (2508.07414) | **EMNLP 2025** (ACL Anthology 2025.emnlp-main.1232, theo kết quả search) | **Dùng KG Wikidata** để tìm ảnh thực thể văn hoá, sinh 22M cặp VQA (42 nước, 39 ngôn ngữ). Mở đầu bằng nhận định "MLLM hiểu sai thực thể văn hoá đuôi dài" | Có. Tiếng Việt nằm trong tập đánh giá entity |
| 9 | **VMMU** (2508.13680) | arXiv 2025-08 | Benchmark đa phương thức tiếng Việt: STEM, lái xe, IQ. **Không phải văn hoá** | VN |
| 10 | **MMA-ASIA** (2510.08608) | arXiv 2025-10 | 27K câu hỏi trắc nghiệm, 8 nước châu Á, căn chỉnh text/ảnh/tiếng nói | Có. "Vietnamese culture (62.96%) on par with Korean" |
| 11 | **IndicVisionBench** (2511.04727) | ICLR 2026 (theo mlanthology) | Benchmark văn hoá Ấn Độ, khoảng 5K ảnh | — |
| 12 | **VietMEAgent** (2511.09058) | **FAIR 2025** | **Trùng nhiều nhất.** Detector vật thể văn hoá Việt, program generation, **KB 156 thực thể văn hoá Việt**. Dataset 28.484 ảnh / 91.149 câu hỏi, 12 hạng mục (ẩm thực, kiến trúc, áo dài, lễ hội, phương tiện...), κ = 0,832. Metric "Cultural Accuracy". HF `Dangindev/viet-cultural-vqa` tồn tại (Apache-2.0). Thẻ HF ghi **28.505 ảnh / 119.012 QA**, lệch với số trong bài | **VN** |
| 13 | **ViSignVQA** (2512.22218) | arXiv 2025-12 | VQA biển hiệu tiếng Việt, 10.762 ảnh | VN |
| 14 | **M²CQA** (2602.05437) | arXiv 2026-02 | **Ảo giác văn hoá phản thực**: chấp nhận diễn giải "hợp văn hoá nhưng sai thị giác". Metric CFHR | MENA |
| 15 | **AutoViVQA** (2603.09689) | arXiv 2026-03 | VQA tiếng Việt sinh tự động. Có nhắc "culturally grounded interpretation" là thiếu | VN |
| 16 | **Culture-Aware Humorous Captioning** (2604.18091) | arXiv 2026-04 | Caption hài theo bối cảnh văn hoá, đánh giá 6 chiều | — |
| 17 | **HSTFG / PhonoSTFG** (2604.27712) | arXiv 2026-04 | Caption scene-text tiếng Việt bằng **graph fusion**. Gần với nhánh "graph + caption tiếng Việt" (nên báo cho agent phụ trách overlap) | VN |
| 18 | **MosAIC**, Bai, Borah, Ignat, Mihalcea | **NAACL 2025** long, tr. 2970-2993 (ACL Anthology 2025.naacl-long.152) | Đa tác tử LMM với persona văn hoá, viết **caption văn hoá**, đề xuất metric văn hoá. Dữ liệu Trung Quốc, Ấn Độ, Romania | Không |

Kiểm tra chéo độ phủ VN, bằng cách grep "vietnam" trên HTML arXiv: **CVQA 0, CulturalVQA 0, RAVENEA 0, CultureVLM 0**. WorldCuisines có 44 món VN (khoảng 1,9%). Kết luận: **chưa benchmark caption văn hoá quốc tế nào có tiếng Việt**. Tài nguyên văn hoá Việt duy nhất là dữ liệu VQA của VietMEAgent.

## 3. Đếm ảnh có thực thể văn hoá trong dữ liệu UIT (đo trong phiên)

Phương pháp: dùng lexicon khoảng 110 thuật ngữ (ẩm thực, trang phục, phương tiện/vật dụng, lễ hội/tín ngưỡng, địa danh, biểu tượng), khớp theo ranh giới từ trên 5 caption tham chiếu. "Strict" nghĩa là ≥2/5 tham chiếu cùng nhắc một thuật ngữ, và đã loại các từ mơ hồ (gánh, sạp, chè, nem, xôi, lăng, Huế, ghe, xuồng...). Script nằm tại `scratchpad/cult.py`, chưa đưa vào repo.

| Dữ liệu | Số ảnh | Ảnh có ≥1 thuật ngữ | Strict |
|---|---|---|---|
| KTVIC train | 3.769 | 661 (17,5%) | 364 (9,7%) |
| KTVIC test | 558 | 130 (23,3%) | 66 (11,8%) |
| **KTVIC tổng** | 4.327 | 791 (18,3%) | 430 (9,9%) |

Thuật ngữ nhiều nhất trên toàn KTVIC (số ảnh): nón lá 155, áo dài 126, đèn lồng 112, xích lô 48, xuồng 41, phố cổ 37, đòn gánh 20, chùa 20, **phở 18**, tết 17, chợ nổi 17, cờ tổ quốc 13, **bánh mì 12**. Ẩm thực chỉ có ở 51 ảnh, địa danh có tên ở rất ít ảnh (chợ Bến Thành 4, chợ Đồng Xuân 3). KTVIC lấy ảnh từ UIT-EVJVQA, nên thiên về đời sống đường phố. **Phân bố đuôi rất dài và lệch về trang phục + đèn lồng.**

- **UIT-ViIC**: 3.850 ảnh COCO thể thao có bóng. Guideline ghi "no place names". Gần như **0 thực thể văn hoá Việt**, nên không dùng cho hướng này. Thông tin lấy từ `vicap-research/.../lam2020uitviic.md`.
- **UIT-OpenViIC**: 13.100 ảnh crawl Google/Bing bằng từ khoá tiếng Việt. Khả năng cao có nội dung văn hoá, nhưng guideline yêu cầu "objective". **Chưa có dữ liệu trong máy, cần đếm bằng cùng script.**
- **ViTextCaps**: 15.729 ảnh, một phần chụp thực địa ở VN. Văn hoá nằm chủ yếu qua chữ (biển hiệu), và chồng lấn với agent phụ trách scene-text.

## 4. Đo nhanh: VLM và VSPS gọi tên thực thể văn hoá ra sao (KTVIC test, đo trong phiên)

Gold là 68 cặp (ảnh, thuật ngữ), trong đó ≥2/5 tham chiếu nêu một thuật ngữ không mơ hồ (65 ảnh). Recall = caption hệ thống có nêu đúng thuật ngữ đó. Prediction lấy từ `data/results/*.preds.json`. Script nằm tại `scratchpad/ag09_recall.py`.

| Hệ thống | Recall văn hoá | nón lá | đèn lồng | áo dài | xích lô | Lần nêu thuật ngữ có ≥1 ref ủng hộ |
|---|---|---|---|---|---|---|
| Zero-shot (backbone, short) | **40/68 = 58,8%** | 12/21 | 16/18 | 7/9 | 0/6 | 51/108 = 47,2% |
| Zero-shot (detailed) | 40/68 = 58,8% | 16/21 | 16/18 | 5/9 | 0/6 | 55/169 = **32,5%** ("áo dài" 45 lần không có ref nào ủng hộ) |
| P1-gold (short) | 29/68 = 42,6% | 11/21 | 7/18 | 4/9 | **6/6** | 32/44 = 72,7% |
| official/distill (short) | 10/68 = 14,7% | 0/21 | 10/18 | 0/9 | 0/6 | — |
| **VSPS main_s42 (short)** | **11/68 = 16,2%** | **0/21** | 3/18 | 7/9 | 0/6 | — |
| VSPS main_s42 (detailed) | 16/68 = 23,5% | 2/21 | 6/18 | 8/9 | 0/6 | 20/40 = 50,0% |

Ví dụ (ảnh 1998). ZS: "Người phụ nữ **đội nón lá** ngồi bên cạnh quầy hoa…". VSPS: "Có một người áo màu trắng, quần đen." Ảnh 1185 tương tự: ZS ghi "mặc áo dài đỏ… đội nón lá", VSPS chỉ ghi "Có một người mặc áo màu đỏ."

Cách đọc:
- **VSPS đổi ảo giác lấy sự nghèo văn hoá.** Từ vựng mệnh đề có kiểu (và từ điển Vietnamese→COCO object) không có lớp "nón lá" hay "xích lô". Mô hình học cách nói chung chung ("người", "mũ", "áo"). Đây là một hạn chế cụ thể, đo được, mà reviewer có thể hỏi. Nó cũng là **động lực trực tiếp** cho hướng KG văn hoá.
- Zero-shot không "mù văn hoá". Lỗi chính của nó là **gán thừa** (áo dài, phố cổ, đèn lồng) và **trượt ở đuôi dài** (xích lô).
- Lưu ý: "không có ref ủng hộ" **chưa phải ảo giác**, vì tham chiếu có thể bỏ sót. Cần người gán nhãn kiểm tra khoảng 100 trường hợp trước khi viết chữ "hallucination". n = 68 nên khoảng tin cậy rất rộng (cần bootstrap). Backbone zero-shot lấy theo README là "same backbone" (Qwen2.5-VL-7B, theo bối cảnh VSPS).

## 5. KG văn hoá Việt: hiện trạng
- **Không có KG văn hoá Việt công khai** sau khi tìm (web search 2 lượt, HF search). Các KG tiếng Việt có tồn tại đều thuộc miền khác: VieMedKG (y học cổ truyền, bioRxiv 2024), KG án lệ (arXiv 2309.09069).
- **VietMEAgent KB**: 156 thực thể được chuyên gia xác nhận. Đây là KB, không phải đồ thị quan hệ. Bài không mô tả schema, và HF chỉ chứa dataset VQA.
- **Wikidata** (tra `wbsearchentities` với `language=vi` trong phiên): có item cho nón lá (Q77910039), áo dài (Q252187), xích lô (Q1362895), chợ nổi Cái Răng (Q10748803), Tết Nguyên Đán (Q912988), bánh chưng (Q564567), áo bà ba (Q615111). **Bị lỗi**: "phở" khớp nhầm thành "đường/phố" (Q79007), "bánh mì" chỉ khớp tới bánh mì nói chung (Q7802), "múa lân" thành "nhảy múa", "đòn gánh" và "đèn lồng Hội An" không có. Vậy Wikidata dùng được làm **hạt giống**, nhưng phải **tuyển tay** và xử lý dấu thanh (phở/phố).
- Ước lượng hợp lý cho một KG nhỏ: **khoảng 150-300 thực thể × 6-8 quan hệ** (is_a, worn_on/used_for, region, occasion, visual_cue, confusable_with, material). Nguồn: lexicon KTVIC + Wikidata + 12 hạng mục của VietMEAgent. Một người làm khoảng 2-3 tuần.

## 6. Đánh giá theo 3 chiều

**Overlap (2025-2026):**
- VietMEAgent (FAIR 2025): KB văn hoá Việt + VQA + metric "Cultural Accuracy". **Rủi ro cao nhất** vì cùng hội nghị, có thể cùng reviewer. Bắt buộc trích và phân biệt rõ: họ làm VQA và detector, mình làm caption và kiểm chứng.
- CulturalGround: KG Wikidata → dữ liệu huấn luyện. RAVENEA: retrieval → cIC. MosAIC: caption văn hoá đa tác tử + metric. Ba bài này phủ ý "KG/RAG làm cho VLM văn hoá hơn", nên **không thể claim** phần đó là mới.
- M²CQA: ảo giác do gán văn hoá. Ý "gán thừa" đã có, nhưng ở dạng phát biểu đúng/sai chứ không phải caption, và không có tiếng Việt.

**Novelty còn lại (đóng khung đề xuất):**
- (N1) **"Cultural erasure under hallucination-reducing SFT"**: đo được, có số (mục 4), chưa thấy bài nào đo cho caption. *Chưa xác minh hết: mới tìm bằng 6 lượt web search, API học thuật bị chặn.*
- (N2) **Mệnh đề có kiểu loại `cultural_entity`** trong VSPS: thực thể được KG đề xuất (tên + visual_cue), được VLM verifier kiểm chứng, rồi mới vào supervision. Đây là KG dùng để **kiểm chứng/đề xuất từ vựng**, khớp với nhánh "graph-for-verification" đang lên (file 11), chứ không phải KG bơm vào decoder.
- (N3) **Metric tiếng Việt hai phía**: Cultural Recall (như bảng mục 4) + Cultural Over-attribution Rate (nêu thực thể văn hoá mà ảnh không có, do người xác nhận). Tuỳ chọn thêm một chỉ số "confusable" (gọi nón lá thành mũ thì coi là lỗi nhẹ, gọi áo dài thành áo bà ba thì coi là sai). MAKIEval là tiền lệ cho phần link thực thể tự động.

**Feasibility (1× RTX 3090):**
- Dữ liệu train: 364 ảnh strict trên KTVIC train. Đủ cho LoRA trên một lớp mệnh đề mới **nếu** trộn với supervision VSPS hiện có. Khả thi.
- Đánh giá: 65 ảnh KTVIC test quá ít. Có hai cách: (a) gán nhãn thêm khoảng 300-500 ảnh văn hoá lấy từ UIT-OpenViIC test hoặc ViTextCaps (sau khi đếm); (b) dùng tập VietMEAgent (Apache-2.0) làm **tập đánh giá ngoài miền**. Ảnh có, nhưng không có caption tham chiếu, chỉ có QA, nên dùng cho recall thực thể (nhãn hạng mục/thực thể), không dùng cho CIDEr.
- Compute: verifier và SFT giống VSPS hiện tại, không cần thêm GPU.
- Rủi ro: (i) lexicon tiếng Việt và dấu thanh (phở/phố) cần chuẩn hoá. (ii) Thực thể đuôi dài quá hiếm cho test thống kê. (iii) Văn hoá dễ trượt thành "gán nhãn khuôn mẫu", nên cần metric over-attribution ngay từ đầu.

**Kết luận:** Không nên đưa thành *đóng góp chính* của dòng KG, vì phần tri thức văn hoá đã đông người làm. Nên đưa thành **một trục đánh giá + một loại mệnh đề** trong phương pháp KG/scene-graph chung. Câu chuyện là: "verified-graph supervision giảm ảo giác nhưng xoá thực thể văn hoá (−42,6 điểm recall). KG văn hoá nhỏ làm nguồn đề xuất + kiểm chứng giúp lấy lại recall mà không tăng gán thừa." Rẻ, đo được, có số ngay từ dữ liệu có sẵn.

### Việc làm tuần 1 (≤ 3 ngày)
1. Chạy `cult.py` trên UIT-OpenViIC và ViTextCaps khi có dữ liệu, chốt cỡ tập đánh giá văn hoá.
2. Cho người kiểm tra 100 lần nêu "không có ref ủng hộ" của zero-shot (áo dài/phố cổ/đèn lồng) để tách "ref bỏ sót" khỏi "gán thừa thật".
3. Thêm bootstrap CI cho bảng mục 4. Nếu bảng còn đứng vững, thêm 1 câu vào phần Limitations của bài VSPS v10.

## 7. Chưa xác minh
- Venue của SEA-VL (ACL 2025?) và của IndicVisionBench (ICLR 2026, mới chỉ thấy qua mlanthology).
- ACL Anthology ID của CulturalGround, mới thấy qua kết quả search. Số liệu Underline (2,3M cặp, 6 ngôn ngữ) lệch với arXiv v2 (22M, 39 ngôn ngữ).
- Số liệu VietMEAgent: bài ghi 28.484 ảnh / 91.149 câu hỏi, thẻ HF ghi 28.505 / 119.012. Chưa tải dataset về để đếm. Bài không công bố số metric dạng bảng trong phần đã đọc (chỉ có hình).
- "Không có KG văn hoá Việt" và "chưa ai đo cultural erasure trong caption" chỉ là kết luận **âm tính sau tìm kiếm hạn chế**. Cần quét lại bằng Semantic Scholar/OpenAlex khi hết rate-limit.
- Chưa có số đếm theo năm cho chủ đề "cultural captioning" (OpenAlex hết budget).
