# 17. Red-team độ mới (novelty): 3 ý tưởng ở mục 4.2 và 5 claim ứng viên (a)-(e)

Agent 17, vai phản biện đối kháng. Ngày 2026-10-10. Phạm vi: công trình 2025-2026. Đầu vào: `../research_wall/11_knowledge_graph_captioning.md` mục 4.2 và `_BRIEF.md`.

**Cách tìm và giới hạn.** Hôm nay arXiv API, Semantic Scholar API và OpenAlex đều trả HTTP 429 (hết hạn mức chia sẻ theo IP, chắc do các agent khác chạy song song). Vì vậy tôi tìm bằng web search theo kiểu Google Scholar (cụm từ khóa và tiêu đề), sau đó **mở trang abs arXiv, ACL Anthology, CVF hoặc OpenReview** để xác nhận những bài quyết định mức trùng. Bài nào chỉ thấy qua snippet thì đưa vào mục "Chưa xác minh". Mỗi mục được chạy ít nhất 6 truy vấn (nhật ký ở mục 4). Nhiều truy vấn dùng chung cho nhiều mục.

Thang đo: **none** = không thấy ai làm. **low** = chỉ có họ hàng xa. **med** = có bài làm phần lớn ý, nhưng còn một trục khác biệt thật. **HIGH** = đã có bài làm gần như đúng ý, chỉ khác ở ngôn ngữ hoặc dữ liệu.

---

## 0. Bảng tổng hợp

| Mục | Claim | Trùng về phương pháp (bất kể ngôn ngữ) | Trùng ở tiếng Việt | Tổng | Thay đổi tối thiểu để có độ mới |
|---|---|---|---|---|---|
| Ý 1 / (b) | Graph P/R + quy tắc phụ thuộc DSG cho caption tiếng Việt | **HIGH** | none | **MED-HIGH** | Metric phải dùng **trạng thái kiểm chứng 3 mức** trong đồ thị tham chiếu (UNCERTAIN = vùng không chấm), kèm nghiên cứu tương quan với người trên KTVIC. Phụ thuộc DSG chỉ là kỹ thuật, không phải đóng góp |
| Ý 2 | KG commonsense ở 3 điểm của VSPS | (a) **HIGH**, (b) low, (c) low-med | none | **MED** | Bỏ (a) khỏi danh sách đóng góp. Giữ (b) làm lõi. (c) chỉ là phụ |
| Ý 3 | ViSGParse + benchmark ảo giác quan hệ tiếng Việt | **HIGH** | none | **MED** (bài tài nguyên) | Benchmark phải đo **caption sinh tự do** (không chỉ yes/no) và có các phân tầng riêng của tiếng Việt |
| (a) | Verified scene graph làm giám sát SFT cho LVLM captioner | **MED** | none | **MED** | Phải thắng baseline **GRPO với scene-graph reward** (SC-Captioner/FoCUS) ở cùng ngân sách. Đích SFT phải mang trạng thái UNCERTAIN (trung tính hóa), không chỉ lọc |
| (b) | Graph recall/precision + quy tắc phụ thuộc cho tiếng Việt | **HIGH** | none | **MED-HIGH** | Như Ý 1 |
| (c) | Trung tính hóa nút UNCERTAIN theo phân cấp IsA | **low** | none | **LOW → mới nhất** | Chứng minh bằng metric phân cấp kiểu Taxonomy-aware (CVPR 2025): precision tăng nhưng hierarchical recall không sụt |
| (d) | Tri thức văn hóa truy hồi từ KG, có cổng kiểm chứng thị giác | **MED** | low | **MED** | Cổng phải đặt **ở từng fact**: chỉ bơm fact khi "neo thị giác" của nó SUPPORTED. Đo "knowledge hallucination" trên tập văn hóa Việt tự dựng |
| (e) | Adapter graph-token vào Qwen-VL cho captioning ít tài nguyên | **HIGH** | none | **HIGH (khuyên bỏ)** | Chỉ giữ làm ablation: so graph-token với scene graph tuần tự hóa thành văn bản, cùng ngân sách token |

**Kết luận cho người lập kế hoạch.** Chỗ mới thật nằm ở **giao điểm** chứ không ở từng mảnh: *đồ thị đã kiểm chứng 3 mức → (i) trung tính hóa IsA cho nút UNCERTAIN → (ii) đích SFT → (iii) metric biết trạng thái kiểm chứng*, chạy trên tiếng Việt. Từng mảnh (graph metric, scene-graph reward/supervision, graph token, RAG văn hóa) đều đã có bài ở hội nghị đỉnh 2025-2026. Một reviewer gắt sẽ gọi mỗi mảnh đứng riêng là "port sang tiếng Việt".

---

## 1. Ba ý tưởng ở mục 4.2

### Ý 1: ViVSG + graph precision/recall + quy tắc phụ thuộc DSG (gộp với claim (b))

**Mức trùng: phương pháp HIGH, tiếng Việt none, tổng MED-HIGH.**

Bằng chứng (đã mở trang):
- **PoSh** (Ananthram et al., arXiv 2510.19060, **ICLR 2026**, theo comment arXiv v3 sửa ngày 2026-02-26). Dùng scene graph làm rubric có cấu trúc cho LLM-judge chấm mô tả chi tiết. Điểm tổng hợp dựa trên lỗi chi tiết (lỗi tổ hợp). Tốt hơn GPT-4o-as-judge (+0,05 Spearman ρ trên DOCENT) và dùng được làm reward. Đây là đối thủ trực tiếp nhất của ý "metric dạng đồ thị cho caption chi tiết".
- **Reinforcing Consistency in Video MLLMs with Structured Rewards** (Quan et al., arXiv 2604.01460, **COLM 2026**). Reward scene graph kiểm tra **từng phần tử** (object/attribute/relation), có phân cấp: claim quan hệ ở gốc phụ thuộc vào claim attribute và existence ở dưới. Quan hệ chỉ được tính đúng khi các phần tử nền cũng đúng. **Đây chính là quy tắc phụ thuộc kiểu DSG áp lên chấm caption.** Bài làm trên video nhưng cơ chế trùng.
- **SC-Captioner** (Zhang et al., arXiv 2508.06125, **ICCV 2025**). Parse caption thành các tập object/attribute/relation, đồng thời *sửa metric CAPTURE* (precision chưa đầy đủ, khớp quan hệ chậm). Như vậy "graph P/R cải tiến" đã có người làm.
- **Taxonomy-Aware Evaluation of VLMs** (Snæbjarnarson et al., arXiv 2504.05457, **CVPR 2025**). Hierarchical precision/recall, có điểm một phần cho câu trả lời ít cụ thể hơn nhưng không sai.
- Nền đã có ở file 11: CompreCap (CVPR 2025), DCScore (ICLR 2025), DSG (ICLR 2024), FIHA (Findings ACL 2025).
- Phía đa ngữ: **Ye et al., "Semantic and Expressive Variation in Image Captions Across Languages"** (arXiv 2310.14356, **CVPR 2025**). So độ phủ scene graph của caption ở 7 ngôn ngữ. Trang abs không liệt kê ngôn ngữ. Theo snippet, bài parse **caption đã dịch** bằng FLAN-T5 fine-tune trên FACTUAL-MR. Tức là đã có người làm "SPICE đa ngữ qua dịch". Reviewer có thể hỏi: "sao không dịch sang tiếng Anh rồi chạy DiscoSG?" **Phải có thí nghiệm trả lời câu này.**
- Tiếng Việt: không thấy metric đồ thị nào. UIT-OpenViIC tự nói đã bỏ SPICE vì không có scene graph tiếng Việt (snippet trang arXiv 2305.04166v2). Gần nhất là JaSPICE (CoNLL 2023, tiếng Nhật, cấu trúc vị từ-tham tố), cho thấy chuyển SPICE sang ngôn ngữ khác là việc đã có tiền lệ.

Thay đổi tối thiểu để có độ mới:
1. **Metric phải dùng trạng thái kiểm chứng 3 mức của VSPS.** Nút/cạnh SUPPORTED thì tính vào recall. Nút UNCERTAIN là "vùng không chấm": nhắc đến không bị phạt, không nhắc cũng không mất điểm. Nếu nhắc ở mức hypernym thì được điểm một phần (nối với (c)). Nút REJECTED: caption nhắc đến thì phạt precision. Chưa thấy metric nào có đồ thị tham chiếu *mang trạng thái kiểm chứng*. ALOHa (2024) chỉ bỏ object "hedged" ở phía *candidate*.
2. **Baseline "dịch rồi parse tiếng Anh"** (Ye et al. CVPR 2025, DiscoSG). Phải cho thấy parse trực tiếp tiếng Việt tốt hơn, nhất là ở loại từ ("con", "chiếc"), từ ghép và giới từ không gian.
3. **Tương quan với người** trên ≥300 caption KTVIC. So với CIDEr, lexicon recall hiện có, CHAIR-vi và PoSh dịch. Không có bước này thì độ mới gần như không còn.
4. Quy tắc phụ thuộc DSG chỉ nên trình bày là **thủ thuật giảm lời gọi verifier, có đo số lời gọi**, không gọi là đóng góp. 2604.01460 và DSG đã có rồi.

### Ý 2: KG commonsense ở 3 điểm của VSPS (KG-VSPS)

**(a) Hard negative từ đồng xuất hiện: HIGH.**
- POPE (2023) với split *adversarial* đã lấy object vắng mặt nhưng hay đồng xuất hiện. Đây là chuẩn mặc định.
- **HOPE: "What Makes 'Good' Distractors for Object Hallucination Evaluation"** (Xie et al., arXiv 2508.06530, 2025-08). Chỉ ra lối lấy mẫu theo đồng xuất hiện của POPE đã yếu, và đề xuất distractor dựa trên nội dung ảnh (CLIP) cùng distractor mô tả sai. Distractor tốt hơn KG đồng xuất hiện đã có sẵn.
- Khác biệt duy nhất còn lại: dùng negative để *kiểm chứng dữ liệu huấn luyện* chứ không phải để đánh giá. Khác biệt này mỏng.
- → **Thay đổi tối thiểu:** không gọi là đóng góp. Dùng distractor kiểu HOPE làm bước hiệu chỉnh verifier (nhắm vào con số 63,1% SUPPORTED đúng). Nếu cần thì báo cáo như một ablation.

**(b) Trung tính hóa theo IsA: low** (chi tiết ở claim (c), mục 2). Đây là mảnh mới nhất của toàn bộ kế hoạch.

**(c) Lọc quan hệ phi lý bằng ràng buộc thường thức: low-med.**
- Đã có ở file 11: RelCheck (arXiv 2609.27890, hậu xử lý bằng "visual KB"), C4 multi-hop KG kiểm chứng caption (arXiv 2511.20531), KG-ViP (ACL 2026).
- Tìm kiếm không thấy bài nào dùng **ràng buộc ConceptNet/commonsense để hạ mức** quan hệ trong *pipeline dữ liệu SFT*. Tuy vậy, ý "kiểm tra fact bằng KG" là kiến thức chung (NAACL 2024 "Can KGs reduce hallucinations in LLMs?"). Rủi ro khả thi: chưa kiểm chứng được độ phủ tiếng Việt của ConceptNet (file 11, mục 5).
- → **Thay đổi tối thiểu:** chỉ giữ nếu đo được tỉ lệ quan hệ bị hạ mức mà *người duyệt đồng ý là sai*. Nếu không đo được thì bỏ.

**Tổng Ý 2: MED.** Đóng khung lại thành "(b) là lõi, (c) là phụ, (a) chỉ là kỹ thuật".

### Ý 3: ViSGParse + benchmark ảo giác quan hệ tiếng Việt

**Mức trùng: phương pháp HIGH, tiếng Việt none, tổng MED** (đủ cho track tài nguyên, không đủ cho bài phương pháp).
- Parser: FACTUAL (Findings ACL 2023), DiscoSG (EMNLP 2025). Ngoài ra LLM4SGG và các bài khác cho thấy LLM parse tốt hơn parser cú pháp. "Fine-tune Qwen 1.5B parse caption" là công thức đã biết.
- Benchmark ảo giác quan hệ: Reefknot (Findings ACL 2025), FIHA (Findings ACL 2025), PROVE (ICCV 2025), cộng với R-Bench và Tri-HE (theo snippet, chưa mở trang). Tất cả đều tiếng Anh.
- Ảo giác đa ngữ đã được làm theo kiểu **dịch benchmark tiếng Anh**: MHR (arXiv 2408.00550, POPE/MME/AMBER-MUL, 13 ngôn ngữ; snippet ghi DOI 10.1145/3797025, chưa mở) và **CLAIM** (Ye et al., **ACL 2025** long, tr. 13080-13094, đã mở trang: can thiệp attention xuyên ngôn ngữ, đo trên POPE/MME đa ngữ). Trang không xác nhận có tiếng Việt. Nguy cơ thật: một nhóm khác dịch Reefknot sang nhiều ngôn ngữ, trong đó có tiếng Việt.
- Không có benchmark ảo giác tiếng Việt nào. Các benchmark VLM tiếng Việt 2025-2026 đều thuộc loại khác: VMMU/ViExam (thi cử, arXiv 2508.13680), AutoViVQA (2603.09689), ViTextCaps (2604.27712).
- → **Thay đổi tối thiểu:** (i) đo trên **caption sinh tự do**, có chú thích span, thay vì chỉ yes/no dịch lại. Benchmark dịch không làm được việc này. (ii) có phân tầng lỗi riêng của tiếng Việt (loại từ sai số đếm, giới từ "trên/trong/cạnh", từ ghép bị tách). (iii) ảnh đời sống Việt (UIT-OpenViIC/KTVIC), không dùng ảnh COCO.

---

## 2. Năm claim ứng viên

### (a) Verified scene graph làm giám sát SFT cho LVLM captioner. **Mức trùng: MED**

Bằng chứng:
- **SC-Captioner** (ICCV 2025, 2508.06125): RL, reward là hiệu tập object/attribute/relation (scene graph parse) giữa caption ban đầu và caption tự sửa, đối chiếu với tập tham chiếu. *Scene graph đã là tín hiệu giám sát* (qua RL). Bài vượt DPO.
- **FoCUS** (Hyun et al., arXiv 2609.00709, comment "**EMNLP 2026 Main**", nộp 2026-09-01): reward từ thành phần scene graph (object/attribute/relation) với trọng số có dấu theo prompt, tối ưu bằng GRPO, có "reasoning-based verification" cho attribute và relation. Snippet nói có pha SFT+GRPO. Trang abs không xác nhận dữ liệu SFT là gì.
- **CCCaption** (Tang et al., **CVPR 2026** poster, đã mở trang): reward kép completeness (truy vấn thị giác do nhiều LVLM sinh) và correctness (tách caption thành sub-query rồi kiểm chứng với ảnh). Đây là "tách → kiểm chứng → huấn luyện", chỉ khác là dùng RL.
- **ClaimDiff-RL** (arXiv 2605.20278, 2026-05, arXiv): reward là hiệu atomic claim, được judge đa phương thức kiểm chứng với ảnh.
- 2604.01460 (COLM 2026): reward scene graph có phân cấp (đã nêu ở Ý 1).
- Nhánh SFT/DPO trên caption đã lọc: "Low-hallucination Synthetic Captions" (arXiv 2504.13123, chỉ đọc snippet), multiagent sửa caption (Lee et al., 2412.15484, comment ICML 2025), Antidote (CVPR 2025).
- **Không thấy** bài nào lấy *đồ thị mệnh đề đã kiểm chứng 3 mức* (SUPPORTED/UNCERTAIN/REJECTED từ K mẫu) và render thành **đích SFT**, trong đó nút UNCERTAIN được *trung tính hóa* chứ không bị xóa.

Lời phản biện mạnh nhất: "Năm 2025-2026, scene graph đã làm reward cho RL (SC-Captioner, FoCUS, CCCaption). SFT trên caption đã lọc là bước lùi. Tại sao không GRPO?"

→ **Thay đổi tối thiểu:** (1) **thêm baseline GRPO với reward scene graph** (kiểu SC-Captioner, dùng chính verifier làm judge) ở cùng ngân sách GPU, hoặc cho thấy SFT rẻ hơn mà precision tương đương trên RTX 3090 (GRPO với Qwen2.5-VL-7B trên 24 GB rất khó, đây là lý do khả thi chính đáng). (2) Đích SFT phải *mang thông tin không chắc chắn* (hypernym, xem (c)). Đây là thứ RL-reward không tạo ra trực tiếp. (3) Thiết lập ít tài nguyên: không có caption tham chiếu tiếng Việt chi tiết để làm reward, nên đồ thị kiểm chứng thay cho tham chiếu.

### (b) Graph recall/precision + quy tắc phụ thuộc cho tiếng Việt. **Mức trùng: MED-HIGH**
Xem Ý 1. Bổ sung: không thấy metric caption nào bằng tiếng Việt ngoài n-gram. Bài LLM-judge tiếng Việt duy nhất tìm được là **VIVID** (arXiv 2608.03095, LREC 2026), nhưng thuộc văn bản (thành ngữ), không thuộc ảnh. Như vậy khoảng trống tiếng Việt là có thật, nhưng phương pháp thì không mới.

### (c) Trung tính hóa nút UNCERTAIN theo phân cấp IsA. **Mức trùng: LOW**

Bằng chứng (thấy gì và không thấy gì):
- **Taxonomy-Aware Evaluation** (CVPR 2025, 2504.05457): hierarchical P/R, coi câu trả lời là hypernym đúng nhưng ít cụ thể ("conifer" cho "norway spruce") là đúng một phần. Bài chỉ ở **phía đánh giá**. Không thấy bước viết lại hay sinh.
- Hedging trong MLLM: survey "Uncertainty-Aware Decision Making in MLLMs" (arXiv 2608.17084, theo snippet) liệt kê hedging là một hành động. Không có hypernym backoff cho captioning.
- Abstention/selective prediction (conformal abstention 2502.06884, ReCoVERR Findings ACL 2024): ở mức câu trả lời, không phải mức nút.
- Trung tính giới (man/woman → person): luật thủ công cũ (2020, 2023). Bài 2026 "VLMs Suppress Female Representations Under Ambiguous Input" (arXiv 2605.31556, snippet) chỉ chẩn đoán, không đề xuất backoff.
- Sau 6 truy vấn (mục 4) **không thấy** bài 2025-2026 nào leo hypernym có điều kiện theo độ tin cậy kiểm chứng để viết caption hoặc tạo dữ liệu huấn luyện.

Rủi ro: reviewer có thể nói "chỉ là WordNet lookup". Phần khó thật là tiếng Việt: ánh xạ lexicon Việt sang synset hoặc khái niệm Wikidata, và các cặp đặc thù (xe tay ga → xe máy → xe).

→ **Thay đổi tối thiểu (để thành đóng góp chính):** đo bằng chính hierarchical P/R của Taxonomy-aware. Kỳ vọng: precision mức chi tiết tăng, hierarchical recall gần như không sụt, so với hai phương án "xóa nút UNCERTAIN" và "giữ nguyên". Kèm đánh giá người ~200 câu: caption bị trung tính hóa có bị chê là "nhạt" không. Đây là mảnh nên đặt ở trung tâm câu chuyện.

### (d) Tri thức văn hóa truy hồi từ KG, có cổng kiểm chứng thị giác. **Mức trùng: MED**

Bằng chứng:
- **RAVENEA** (arXiv 2505.14462, **ICLR 2026**, có trang proceedings): benchmark RAG văn hóa thị giác, có cả nhiệm vụ **culture-informed image captioning**, dùng tài liệu Wikipedia được người xếp hạng. Truy hồi theo văn hóa giúp captioning (snippet ghi khoảng +11% ở bản ICLR). → "RAG văn hóa cho captioning" đã được làm.
- **CulturalGround / "Grounding Multilingual Multimodal LLMs With Cultural Knowledge"** (arXiv 2508.07414, **EMNLP 2025** main 1232): lấy thực thể văn hóa từ Wikidata, sinh 22M cặp VQA, 42 nước, 39 ngôn ngữ (theo snippet). → "KG Wikidata + văn hóa + MLLM đa ngữ" đã được làm, nhưng ở dạng dữ liệu huấn luyện VQA, không có cổng kiểm chứng.
- **AKGMA** (AAAI 2026): nhắm "knowledge hallucination" trong captioning, dựng subgraph liên quan ảnh bằng RL.
- Lọc kết quả truy hồi: ARA-LVLM (ACM, 2025, theo snippet: kích hoạt truy hồi khi không chắc, lọc kết quả). Utility-oriented visual evidence selection (arXiv 2605.13277, snippet). Cả hai ở mức tài liệu, không phải từng fact có neo thị giác.
- Văn hóa Việt: chưa có benchmark captioning văn hóa. VietFashion (arXiv 2606.13427, truy hồi áo dài, snippet). MMA-ASIA (arXiv 2510.08608) có 8 nước châu Á, chưa xác nhận có Việt Nam hay không. Arabic VLCAP (2510.03295) là mẫu "captioning có khái niệm văn hóa" cho ngôn ngữ khác.

Rủi ro khả thi: Wikidata/ConceptNet phủ yếu khái niệm đời sống Việt (nón lá, xe ôm, chợ tạm). Nhiều khả năng phải tự dựng KG nhỏ bằng tay.

→ **Thay đổi tối thiểu:** cổng **ở mức từng fact** với neo thị giác tường minh. Ví dụ fact "áo dài là trang phục truyền thống" chỉ được bơm khi mệnh đề `entity: áo dài` của ảnh là SUPPORTED. Fact có neo UNCERTAIN thì không bơm, hoặc bơm ở dạng hypernym ("trang phục truyền thống"). Đo tỉ lệ fact văn hóa sai neo trên một tập khoảng 300 ảnh văn hóa Việt chọn từ UIT-OpenViIC/KTVIC, so với RAG không cổng kiểu RAVENEA. Không có tập đo này thì claim chỉ là "RAVENEA tiếng Việt".

### (e) Adapter graph-token vào Qwen-VL cho captioning ít tài nguyên. **Mức trùng: HIGH, khuyên bỏ**

Bằng chứng:
- **3DGraphLLM** (Zemskova & Yudin, arXiv 2412.18450, **ICCV 2025**): biểu diễn scene graph *học được* (subgraph quanh object) đưa vào LLM, đánh giá cả Scan2Cap (captioning 3D). Bài lập luận embedding tốn ít token hơn văn bản.
- **DyGEnc** (arXiv 2505.03581, 2025-05): nén chuỗi scene graph văn bản thành token cho LLM (snippet mô tả graph encoder + Q-Former + soft prompt cho LLM tinh chỉnh LoRA). Nhiệm vụ là QA.
- Graph-tokenizing LLM là cả một dòng (LLaGA, GraphToken. Bài tổng kết "Revisiting Graph-Tokenizing LLMs", arXiv 2605.03514, theo snippet).
- AKGMA (AAAI 2026) có Scene-Context Knowledge Adapter đưa tri thức scene graph vào LLM. KG-ViP (ACL 2026) hợp nhất scene graph với commonsense graph.
- File 11 đã chỉ ra "KG-into-generator" là hướng bão hòa. Phía tiếng Việt chỉ có ViTextCaps/PhonoSTFG (graph *hợp nhất đặc trưng*).

Lời phản biện mạnh nhất: "Scene graph tuần tự hóa thành văn bản trong prompt (kiểu CCoT) là baseline miễn phí. Adapter mới phải thắng nó, mà với Qwen2.5-VL thì nhiều khả năng không thắng. Đổi sang tiếng Việt không phải đóng góp về kiến trúc." Thêm vào đó, trên RTX 3090 phải huấn luyện projector mới cùng QLoRA, tốn chi phí mà không có lợi ích đo được.

→ **Thay đổi tối thiểu (nếu vẫn giữ):** chỉ làm ablation "graph-token và SG-as-text ở cùng ngân sách token", trong đó embedding nút **mã hóa luôn trạng thái và độ tin cậy kiểm chứng**. Đây là thứ duy nhất văn bản khó truyền gọn. Không nên đặt làm đóng góp chính.

---

## 3. Chưa xác minh (chỉ thấy qua snippet tìm kiếm, chưa mở trang gốc)
- FoCUS (2609.00709): có pha SFT hay không và dùng parser nào. Trang abs không nêu.
- ClaimDiff-RL (2605.20278): nhãn supported/hallucinated/uncertain và khởi tạo SFT. Trang abs chỉ nêu error type và severity.
- Ye et al. CVPR 2025 (2310.14356): danh sách 7 ngôn ngữ và parser FLAN-T5 trên caption đã dịch.
- R-Bench, Tri-HE (benchmark ảo giác quan hệ), MHR (2408.00550, DOI 10.1145/3797025), Low-hallucination Synthetic Captions (2504.13123), TACO (2511.09228), CycleCap (2603.18282), Re³Cap (EMNLP 2026, theo model card HF), VLCAP (2510.03295), MMA-ASIA (2510.08608, có Việt Nam hay không), VietFashion (2606.13427), VMMU (2508.13680), "Uncertainty-Aware Decision Making in MLLMs" (2608.17084), 2605.31556, 2605.13277, ARA-LVLM (ACM 2025), Generate Any Scene (2412.08221), DyGEnc: kiến trúc (trang abs không mô tả).
- Venue lấy theo comment arXiv (PoSh ICLR 2026, FoCUS EMNLP 2026, 2604.01460 COLM 2026, Lee et al. ICML 2025) chưa được đối chiếu với proceedings. Đã có trang proceedings/CVF: RAVENEA (ICLR 2026), Taxonomy-aware (CVPR 2025), SC-Captioner (ICCV 2025), CCCaption (CVPR 2026, trang poster), CLAIM (ACL 2025), 3DGraphLLM (ICCV 2025, qua mlanthology), CulturalGround (EMNLP 2025, qua link ACL Anthology).
- Hạn chế: không chạy được truy vấn API có cấu trúc (429). Độ bao phủ phụ thuộc chỉ mục web search. Cần chạy lại mục 4 bằng arXiv API khi hết rate-limit, nhất là cho (c), mục duy nhất được đánh "low".

## 4. Nhật ký truy vấn (rút gọn; ≥6 truy vấn mỗi mục, nhiều truy vấn dùng chung)
- **(a)**: scene graph supervision fine-tuning VLM detailed captioning hallucination / verified atomic facts filtered captions SFT LVLM / graph-structured caption synthesis verify each node / scene graph self-training detailed caption MLLM / graph-to-caption detector-verified LVLM fine-tuning / scene graph guided caption rewriting SFT 2026 / scene graph reward RL GRPO captioning / SC-Captioner / self-consistency propositions SUPPORTED UNCERTAIN distillation / multilingual low-resource verified pseudo-captions.
- **(b)/Ý 1**: Vietnamese SPICE scene graph metric / multilingual SPICE non-English LLM parser / detailed caption P/R dependency Davidsonian / Vietnamese caption LLM-judge or hallucination benchmark / scene-graph metric hierarchical conditional skip child / multilingual text scene graph parsing language-agnostic metric.
- **(c)/Ý 2b**: hypernym backoff uncertain objects captioning WordNet / abstention specificity coarser category / uncertainty-aware hedging hypernym taxonomy / taxonomy-aware evaluation VLM / gender-neutral captioning LVLM 2025-2026 / granularity-hallucination trade-off specificity.
- **(d)**: culture-aware captioning knowledge retrieval / RAG captioning filtering visual verification / Wikidata cultural heritage MLLM verification SEA / Vietnamese culture VLM benchmark / RAVENEA / knowledge-enhanced captioning retrieve-then-verify / gating retrieved knowledge by visual evidence / Vietnamese cultural multimodal (áo dài, nón lá).
- **(e)**: scene graph tokens adapter LLaVA Qwen-VL / GNN projector graph tokens MLLM / low-resource captioning Qwen2-VL LoRA SG prompt / SG injection LVLM hallucination / AKGMA adapter / SG-as-text vs learned embedding ablation / Vietnamese captioning Vintern Qwen UIT-OpenViIC KTVIC.
- **Ý 2a/2c, Ý 3**: co-occurrence hard negatives POPE KG / commonsense KG plausibility relation hallucination ConceptNet / non-English relation hallucination benchmark / multilingual hallucination benchmark LVLM low-resource / Vietnamese scene graph dataset or parser.
