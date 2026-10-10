# 02. Metric đánh giá caption dựa trên đồ thị / cấu trúc (2025-2026) và đề xuất metric mới cho caption tiếng Việt có KG

KG-plan agent 02, ngày 2026-10-10. Góc: các metric dùng scene graph hoặc đơn vị mệnh đề có cấu trúc để chấm caption (họ hậu SPICE). Với mỗi metric, ghi: nó đo gì, gold graph lấy từ đâu, tương quan với người được báo cáo bao nhiêu, hỗ trợ ngôn ngữ nào, chi phí. Sau đó đề xuất 4 metric mới cho caption tiếng Việt có KG.

**Cách xác minh.** Mỗi bài dưới đây đều đã được mở hôm nay qua arXiv API (`export.arxiv.org`, lấy tiêu đề, ngày, comment, tóm tắt), OpenAlex (tóm tắt) hoặc trang HTML trên arXiv (lấy số liệu tương quan trong bảng). Semantic Scholar và OpenAlex bị giới hạn tần suất (429) trong phần lớn phiên, nên venue nào chỉ có trong trường comment của arXiv thì ghi đúng như comment. Những mục không mở được thì nằm ở §6.

**Không lặp lại** `../../manuscript/research_wall/02_caption_evaluation_metrics.md`, file đã có định nghĩa CAPEval, PoSh, VELA, HalDec-Bench, OVFact, CAPability, CapArena cho VSPS. File này chỉ bổ sung **góc đồ thị** (gold graph lấy từ đâu, phụ thuộc giữa các phần tử, quan hệ, phân cấp) và **thiết kế metric mới**.

**Tài sản sẵn có trong repo** (phải dùng lại, không viết lại):
- `rescap/svp/matching.py`: so khớp mệnh đề theo 3 tầng EXACT / LEXICAL (từ đồng nghĩa và lưới hypernym) / SOFT, so khớp ở mức entity, bỏ qua loại từ.
- `rescap/metrics_svp.py`: `proposition_prf`, `hallucination_rates` (đã tách ảo giác **primary** và **inherited**, tức đã có dạng quy tắc phụ thuộc kiểu DSG), `pgf`/`vcf` (precision luôn đi kèm coverage).
- `rescap/chair.py` và `rescap/vi/lexicon.py`: CHAIR tiếng Việt, `HYPERNYMS` một chiều.

Vậy các metric mới phải vượt **cả** những gì đã có trong repo. Nếu không, reviewer nội bộ sẽ hỏi "khác gì VCF".

---

## 1. Bảng so sánh các metric/benchmark dựa trên cấu trúc

Viết tắt: PCC = Pearson, τ = Kendall, ρ = Spearman. Chi phí ghi theo cách metric chạy, không phải giá đo được.

### 1.1 Nền tảng (trước 2025, mỗi mục một dòng)
| Metric | Đo gì / gold | Ghi chú |
|---|---|---|
| SPICE (ECCV 2016, arXiv 1607.08822) | F1 trên các tuple (object), (object, attr), (obj, rel, obj) parse từ caption tham chiếu | Gold là đồ thị **parse từ caption người viết**. Chỉ có tiếng Anh. Không gắn tuple với từng thực thể cụ thể (hai "người" bị gộp làm một). |
| JaSPICE (CoNLL 2023, arXiv 2311.04192) | SPICE cho tiếng Nhật: dựng đồ thị từ cấu trúc phụ thuộc và vị từ-tham tố, mở rộng bằng từ đồng nghĩa | **Tiền lệ trực tiếp**: "SPICE cho một ngôn ngữ không phải tiếng Anh" đã được nhận ở hội nghị ACL-family. Bộ Shichimi có 103.170 đánh giá người. Tóm tắt nói JaSPICE vượt các baseline về tương quan, nhưng không ghi số. |
| DSG (ICLR 2024, arXiv 2310.18235) | Đồ thị câu hỏi nguyên tử có phụ thuộc cha-con. Cha bị trả lời "không" thì bỏ con | Dùng cho T2I. Quy tắc phụ thuộc này là nguồn của "inherited" trong repo. |
| FaithScore (Findings EMNLP 2024, arXiv 2311.01477) | Tách câu trả lời thành atomic fact có kiểu, kiểm chứng từng fact bằng VLM | Tương quan với người (bảng 3, LLaVA/InstructBLIP): Pearson 48,2 / Spearman 38,4 / Kendall 47,6 (%), so với SPICE 20,2 / 21,3 / 25,4. Không có gold graph, verifier đóng vai gold. |
| VALOR-EVAL (Findings ACL 2024, arXiv 2404.13874) | Faithfulness và coverage cho object/attribute/relation, so khớp bằng LLM với danh sách đặc trưng người gán | Pearson với người theo loại: relation positional 0,78 / 0,86, các loại khác 0,89-0,99 (bảng 4). Ảnh được chọn theo **associative bias**. |
| ALOHa (NAACL 2024, arXiv 2404.02904) | Ảo giác object từ vựng mở, so khớp bằng embedding | Chỉ object. |
| AMBER (arXiv 2311.07397) | Benchmark ảo giác không cần LLM: object, attribute, relation | Chỉ tiếng Anh. |

### 1.2 Các metric 2024-H2 đến 2026 (trọng tâm)
| # | Metric / benchmark | Venue (đã kiểm) | Đo gì | Gold graph lấy từ đâu | Tương quan người được báo cáo | Ngôn ngữ | Chi phí |
|---|---|---|---|---|---|---|---|
| G1 | **CAPTURE** / DetailCaps (arXiv 2405.19092) | arXiv 2024, venue chưa xác minh | F1 trên object/attribute/relation, khớp 3 tầng (chính xác, đồng nghĩa, embedding mềm) | Parse từ caption chi tiết tham chiếu (chuyên gia, GPT-4V, Gemini-1.5-Pro) bằng text SG parser | Trung bình DetailCaps-100/4870: PCC 0,509, τ 0,386, mẫu-τ 0,602. SPICE là 0,439 / 0,324 / 0,472 | Anh | Rẻ: parser và embedding, không cần LLM |
| G2 | **DCScore** / DeCapBench (arXiv 2503.07906) | ICLR 2025 | Precision (ảo giác) và recall (độ phủ) trên "primitive information unit" | LLM tách caption tham chiếu người viết thành đơn vị. Đơn vị của candidate được kiểm chứng bằng LLM/VLM | Trên 500 caption: PCC cao hơn SOTA 0,2375, τ cao hơn 0,1082. DeCapBench–Arena Elo ρ = 0,90 | Anh | Cao: nhiều lời gọi GPT-4o mỗi caption |
| G3 | **CompreCap** (arXiv 2412.08614) | CVPR 2025 | Độ phủ object, độ chính xác attribute, điểm relation then chốt | **Người gán thủ công**: phân vùng (từ COCO panoptic), thuộc tính, quan hệ có hướng. 560 ảnh, 412 lớp | Bảng phụ lục, theo LVLM (tức cấp mô hình): PCC 0,989, τ 0,927, ρ 0,982. CLIPScore là 0,691 / 0,426 / 0,539 | Anh | Gán nhãn rất tốn. Chấm bằng Llama3 |
| G4 | **PROVE** (arXiv 2410.13121) | ICCV 2025 theo S2 (file 11), chưa đối chiếu proceedings | Helpfulness và truthfulness của câu trả lời mở, chấm bằng **chương trình chạy trên scene graph** | LLM dựng SG từ caption siêu chi tiết (DOCCI), 10,5K cặp QA | Tóm tắt không có số. Phân tích đánh đổi helpfulness-truthfulness | Anh | Trung bình |
| G5 | **FIHA** (arXiv 2409.13612) | Findings ACL 2025 | Ảo giác chi tiết (object/attr/relation) bằng QA có/không, tổ chức theo DSG | Tự động, không cần LLM hay nhãn người (detector và captioner) | Tóm tắt không ghi số | Anh | Rẻ |
| G6 | **Tri-HE** (arXiv 2410.23114) | TMLR 2025 | Ảo giác **triplet** (obj, rel, obj) trích từ câu trả lời mở, chấm bằng LLM judge | Triplet gold từ GQA/SG, câu hỏi do GPT-4V sinh | Judge khớp tốt với người (bảng 3). Kết luận: **ảo giác quan hệ nặng hơn ảo giác object** | Anh | Trung bình (GPT-4 trích triplet) |
| G7 | **R-Bench** (arXiv 2406.16449) | ICML 2024 | Ảo giác quan hệ dạng có/không, mức ảnh và mức instance | Từ SG/nhãn người | Benchmark phân biệt, không phải metric caption. Tìm ra 3 loại đồng xuất hiện gây ảo giác: rel-rel, subj-rel, rel-obj. LVLM **dựa vào commonsense của LLM** | Anh | Rẻ |
| G8 | **Reefknot** (arXiv 2408.09429) | Findings ACL 2025 | Ảo giác quan hệ: tri giác và nhận thức. Có Y/N, MCQ và VQA | Bộ ba từ Visual Genome, hơn 20.000 mẫu | Không phải metric tương quan người | Anh | Rẻ |
| G9 | **CapMAS** (arXiv 2412.15484) | ICML 2025 | Hai metric: factuality và coverage cho caption siêu chi tiết | Tách claim bằng LLM, kiểm chứng. Coverage dựa trên QA | Factuality–người ρ = 70,2, so với FactScore 67,9 và FaithScore 62,5 | Anh | Cao |
| G10 | **DiscoSG** (arXiv 2506.15583) | EMNLP 2025 (oral) | Parser **caption nhiều câu → SG** (đồng tham chiếu xuyên câu), tác vụ mới | 400 cặp chuyên gia gán và 8.430 cặp tổng hợp | Refiner cao hơn baseline 30% SPICE, nhanh gấp 86 lần GPT-4o. Cải thiện chấm caption mức diễn ngôn | Anh | Nhẹ (mã nguồn mở) |
| G11 | **PoSh** (arXiv 2510.19060) | ICLR 2026 | Scene graph làm **rubric** cho LLM-as-judge, điểm định vị được đến từng span | SG trích từ **tham chiếu chuyên gia** (DOCENT, tranh nghệ thuật) | Cao hơn đối thủ open-weight tốt nhất 0,05 ρ, vượt cả GPT-4o-as-judge. F1 phát hiện mistakes 0,580, omissions 0,680 | Anh | Trung bình (judge open-weight) |
| G12 | **CAPEval** (arXiv 2608.02589) | arXiv 2026-08 | Tách Coverage và Precision trên checklist nguyên tử do người kiểm | Caption người viết và checklist nguyên tử do người xác nhận | Đo **validity theo tác vụ hạ nguồn** (coverage dự đoán hiểu, precision dự đoán sinh), không phải τ với người | Anh | Trung bình |
| G13 | **CapProbe** (arXiv 2608.11074) | arXiv 2026-08 | QA dày đặc theo vùng (MCQ, có lựa chọn "Uncertain"), Effective Accuracy, điểm theo mật độ | Phân vùng thô, QA do mô hình sinh. 346 ảnh, 25.650 câu hỏi | Tóm tắt nói xếp hạng ổn định, không nêu τ với người | Anh | Trung bình |
| G14 | **ClaimDiff-RL** (arXiv 2605.20278) | arXiv 2026-05 | Hiệu claim nguyên tử giữa caption actor và caption tham chiếu, có kiểu lỗi và mức nặng, dùng làm reward | Caption tham chiếu và judge đa phương thức | Bộ chẩn đoán 160 ảnh do người gán. Cho thấy reward vô hướng **giảm ảo giác bằng cách bỏ sót** | Anh | Cao |
| G15 | **HalCECE** (arXiv 2503.00436) | arXiv 2025 | Phát hiện ảo giác bằng **counterfactual khái niệm**: sửa tối thiểu theo **phân cấp tri thức (WordNet)**, có ảo giác vai (role) | Khái niệm trong caption tham chiếu, đi qua WordNet | Tóm tắt không có số | Anh | Rẻ (tất định) |
| G16 | **ReflectCAP** (arXiv 2604.12357) | arXiv 2026-04 | Phương pháp, không phải metric. Đạt **biên Pareto** factuality–coverage | (dùng metric có sẵn) | — | Anh | — |
| G17 | **DetailVerifyBench** (arXiv 2604.05623) | arXiv 2026-04 | Định vị ảo giác mức token trong caption dài hơn 200 từ, 1.000 ảnh, 5 miền | Người gán mức token | — | Anh | — |
| G18 | **CHI** (arXiv 2609.33343, tóm tắt văn bản) | arXiv 2026-09 | Chỉ số ảo giác hợp nhất entity/relation/quantity, kết hợp bằng trung bình điều hòa | Văn bản nguồn | ρ cấp hệ thống 0,66 trên SummEval | Anh | Rẻ |
| G19 | Structured consistency audit (arXiv 2604.01460, video) | COLM 2026 (theo comment) | Kiểm **từ trên xuống**: claim quan hệ đúng ở gốc có được attribute và existence bên dưới đỡ không. Reward SG có nhận biết instance | SG từ caption | — | Anh | — |

### 1.3 Đọc bảng
1. **Gold graph đi theo ba đường**: (a) parse từ caption người viết (SPICE, CAPTURE, PoSh, DCScore), rẻ nhưng **không đầy đủ**, vì thứ người viết không nhắc đến lại bị tính là ảo giác. (b) gán thủ công trên ảnh (CompreCap, CAPEval, DetailVerifyBench), đúng nhưng đắt. (c) tự động bằng detector, SG generator hoặc VLM (FIHA, PROVE), rẻ nhưng nhiễu. **Không bài nào dùng gold graph đã kiểm chứng ba trạng thái (SUPPORTED/UNCERTAIN/REJECTED)**. Trong các bài đã mở, gold luôn là nhị phân: có hoặc không.
2. **Tương quan người thường đo ở cấp mô hình** (CompreCap 0,98, DeCapBench–Elo 0,90). Ở cấp caption thì thấp hơn nhiều (CAPTURE τ ≈ 0,39, FaithScore τ ≈ 0,48). Một metric mới chỉ thuyết phục khi báo **cấp caption**.
3. **Tách P/R và không gộp thành một số** đã thành chuẩn năm 2026 (CAPEval, ClaimDiff-RL, CapMAS, VALOR-EVAL).
4. **Phụ thuộc cha-con** (DSG, FIHA, audit từ trên xuống trong 2604.01460) đã được dùng cho QA và video, **chưa thấy** áp vào P/R của caption sinh tự do theo cách liên kết instance.
5. **Phân cấp IsA**: chỉ HalCECE (giải thích bằng WordNet) và lưới hypernym của SPICE/CAPTURE/repo (khớp hoặc không khớp). **Chưa thấy metric nào cho điểm một phần theo độ đặc hiệu.**
6. **Thường thức/KG**: R-Bench và VALOR-EVAL chỉ ra ảo giác do thiên kiến đồng xuất hiện, nhưng mới dùng để **chọn ảnh** cho benchmark. Chưa thấy metric nào chấm theo từng caption để tách "ảo giác hợp lý theo prior" khỏi "ảo giác ngẫu nhiên". Truy vấn arXiv `caption AND commonsense AND (violation OR implausible OR plausibility) AND evaluation` không ra kết quả.
7. **Tiếng Việt**: không có metric nào ở trên hỗ trợ. Quét arXiv `Vietnamese AND (image captioning OR image description)` từ 2025 chỉ ra ViTextCaps (2604.27712) và AutoViVQA (2603.09689), không có metric. Metric đa ngữ gần nhất là CLIPScore đa ngữ (Findings NAACL 2025, arXiv 2502.06600), và metric này không có cấu trúc.

---

## 2. Tài nguyên tiếng Việt cho metric dạng đồ thị (kiểm hôm nay)

| Tài nguyên | Trạng thái | Ghi chú |
|---|---|---|
| Wikidata nhãn `vi` và `P279` (subclass of) | **Có**. Đã gọi API: Q144 = "chó", Q1420 = "ô tô", Q5 = "người", Q34493 = "mô tô" | Nhãn chuẩn khác cách nói đời thường ("mô tô" và "xe máy"), nên **bắt buộc** phải có bảng alias nối `vi/lexicon.py` với QID. |
| ConceptNet 5 tiếng Việt | **Chưa kiểm được**. `api.conceptnet.io` trả 502 cả hôm nay | Đừng thiết kế metric phụ thuộc ConceptNet cho đến khi đếm được độ phủ. |
| Parser câu → SG tiếng Việt | **Không có** (file 11 §3.2) | Phải tự làm: prompt Qwen2.5-7B-Instruct 4-bit hoặc fine-tune ViT5 / Qwen2.5-1.5B trên 1-2K cặp. |
| Lexicon, từ đồng nghĩa, hypernym, loại từ, màu `xanh` | **Có trong repo** | `vi/lexicon.py`, `svp/matching.py`. |
| Mệnh đề VSPS đã kiểm chứng (đồ thị 3 trạng thái) | **Có** | Nguồn gold rẻ cho mọi metric ở §3 (cần người duyệt lại tập con). |
| Object gold đầy đủ 300 ảnh | Đang làm (`OBJECT_GOLD_PROTOCOL.md`, theo 00_TONG_HOP) | Dùng lại làm tập kiểm định. |

---

## 3. Đề xuất 4 metric mới

Ký hiệu chung. Ảnh I. **Gold graph** G = (V, X): V là các nút instance, X là các phần tử gồm object o ∈ V, attribute (o, a), relation (o₁, r, o₂) và count (lớp, n). Mỗi phần tử x có:
- trạng thái s(x) ∈ {S, U, N}, lần lượt là SUPPORTED, UNCERTAIN và REJECTED/adversarial (tức là sai đã biết);
- độ nổi bật w(x) ∈ (0, 1], là tỉ lệ caption tham chiếu và đề xuất VSPS có nhắc đến x, cộng với cờ "nổi bật" do người duyệt đặt;
- tập cha pa(x): pa(o, a) = {o}, pa(o₁, r, o₂) = {o₁, o₂}, còn object là gốc.

**Candidate graph** Ĝ được parse từ caption. **Căn chỉnh instance** π: V̂ → V ∪ {∅} là phép ghép song phương trọng số cực đại (thuật toán Hungarian). Trọng số là sim(v̂, v) = 1[canonical khớp ở tầng LEXICAL] cộng với λ·(tỉ lệ attribute khớp), nên thuộc tính dùng để phân định hai "người". Tầng khớp được ghi rõ theo quy ước của `svp/matching.py`.

### M1. ViVG-P/R: precision/recall trên đồ thị đã kiểm chứng, liên kết instance, phụ thuộc cha-con, precision dạng khoảng
**Định nghĩa.** Mỗi phần tử x̂ của Ĝ được phân loại như sau:
- **INH** (inherited) nếu tồn tại cha p ∈ pa(x̂) với π(p) = ∅ hoặc p bị FP. Phần tử INH bị loại khỏi tử số và mẫu số của số đo primary, và được báo riêng.
- **TP** nếu x̂ khớp x ∈ X với s(x) = S.
- **FP** (ảo giác đã xác nhận) nếu x̂ khớp x với s(x) = N, hoặc **mâu thuẫn** một phần tử S cùng nút thuộc lớp loại trừ (màu, số đếm, cặp không gian ngược nhau như trên/dưới, trái/phải, trước/sau).
- **ABS** nếu x̂ khớp x với s(x) = U. Phần tử ABS bị loại khỏi cả hai phía của phép tính (gold không biết). Khối lượng ABS được báo cáo.
- **UNK** nếu không khớp và không mâu thuẫn với gì.

Với các phần tử primary:

  P_lo = TP / (TP + FP + UNK) (bảo thủ: UNK tính như ảo giác, tương đương cận trên của ảo giác kiểu CHAIR)
  P_hi = (TP + UNK) / (TP + FP + UNK) (lạc quan)
  P_ver = (TP + UNK_S) / (TP + FP + UNK), trong đó UNK_S là phần UNK được verifier VSPS chấm SUPPORTED. Dùng tùy chọn, và phải kèm sai số verifier đo trên 244 mục audit.

  R_w = Σ_{x: s(x)=S} w(x) · 1[∃x̂ khớp x và mọi cha của x̂ được căn đúng vào cha của x] / Σ_{x: s(x)=S} w(x)

Báo cáo theo loại (O/A/R/C) và luôn báo theo **cặp (P_lo, P_hi, R_w)**, không gộp thành một số.

**Vì sao chặt hơn VCF và SPICE.**
1. **Ràng buộc instance**: "người đàn ông mặc áo đỏ, người phụ nữ mặc áo xanh" và câu bị đổi chéo thuộc tính cho ra điểm khác nhau. Nếu gộp tuple theo chuỗi, "người … áo đỏ" vẫn khớp. Tiếng Việt hay dùng "người" chung chung nên lỗi này hay xảy ra.
2. **Khoảng [P_lo, P_hi]** làm rõ nhược điểm "gold không đầy đủ" mà `chair.py` hiện chỉ ghi trong docstring. Độ rộng khoảng chính là chỉ số độ đầy đủ của gold.
3. **U là "không biết"**, không phải đúng hay sai. Đây là đặc điểm chỉ có ở gold ba trạng thái.

**Tài nguyên.** Mệnh đề VSPS đã kiểm chứng, cộng 500 ảnh KTVIC do người duyệt đồ thị (2 người, file 11 ước tính 2-3 tuần). Thêm parser tiếng Việt câu → đồ thị (xem §4) và `svp/matching.py`. GPU: chỉ parser, khoảng 1-2 s/caption với 7B 4-bit trên 3090 (ước tính, **chưa đo**).

**Kiểm định.**
- Nghiên cứu tương quan theo §5.
- **Ablation từng thành phần**: bỏ ràng buộc instance (gộp như SPICE), bỏ phụ thuộc, coi U = S, coi U = N, bỏ trọng số w. Mỗi thành phần phải làm τ cấp caption tăng có ý nghĩa (kiểm định Williams hoặc bootstrap).
- **Kiểm tra độ đầy đủ gold**: trên 300 ảnh có object gold đầy đủ, P_true phải nằm trong [P_lo, P_hi] ở ít nhất 90% hệ thống × lớp.

**Tiền lệ gần nhất và điểm khác.**
- CompreCap: gold người gán, nhị phân, không có phụ thuộc, không có khoảng.
- DCScore và CAPEval: đơn vị nguyên tử phẳng, không có instance graph.
- FIHA và DSG: phụ thuộc trên QA, không áp vào P/R của caption tự do.
- PoSh: SG làm rubric cho judge, gold từ tham chiếu.
- JaSPICE: SPICE theo ngôn ngữ, gold là tuple parse từ tham chiếu.

Điểm mới bảo vệ được: **gold ba trạng thái → precision dạng khoảng, và recall có ràng buộc instance, cho tiếng Việt**. Không được nói "metric đồ thị đầu tiên" chung chung, chỉ được nói "đầu tiên cho tiếng Việt" và "chưa thấy gold ba trạng thái trong các bài đã mở".

### M2. ViRHR: tỉ lệ ảo giác quan hệ có điều kiện, kèm chỉ số thiên kiến prior
**Định nghĩa.** Một quan hệ x̂ = (ô₁, r̂, ô₂) là **đánh giá được** khi cả hai đầu mút đều TP. Như vậy lỗi object được loại ra, chỉ còn lỗi quan hệ. Tri-HE không tách hai loại lỗi này.
- **RHR** = #{x̂ đánh giá được: FP} / #{x̂ đánh giá được}. Phần UNK được giải bằng verifier, hoặc báo theo khoảng như M1.
- **Tỉ lệ đổi vai (RSR)** = #{x̂: (π(ô₂), r̂, π(ô₁)) có trạng thái S, còn chiều thuận không} / #{đánh giá được}. Chỉ số này bắt lỗi "con chó đuổi người" khi thực tế là ngược lại.
- **Chỉ số thiên kiến prior (RPI)**: gọi P_tr(r | t₁, t₂) là phân phối quan hệ theo cặp loại object, lấy từ caption train KTVIC đã parse. RPI = E_{x̂∈FP}[pct(r̂)] − E_{x̂∈TP}[pct(r̂)], trong đó pct là percentile của r̂ trong P_tr(· | t₁, t₂). RPI > 0 nghĩa là ảo giác quan hệ thiên về quan hệ "hay gặp". Đây là phép đo theo từng caption cho phát hiện của R-Bench rằng LVLM dựa vào commonsense.
- Báo theo **họ quan hệ tiếng Việt**: không gian (trên/ở trên/bên trên, dưới, trong, cạnh/bên cạnh, trước/phía trước, sau, giữa), hành động (cầm, lái, ngồi, đi…), mặc/đội/đeo, so sánh. **Trái/phải** mặc định là U (khung tham chiếu mơ hồ) trừ khi verifier xác nhận.

**Tài nguyên.** Như M1, cộng bảng canonical giới từ và động từ (mở rộng `SYNONYMS`), cộng thống kê quan hệ từ caption train. Chỉ cần CPU.

**Kiểm định.**
- 600 quan hệ đánh giá được (khoảng 100 cho mỗi họ × 6 hệ thống), 3 người gán nhãn đúng/sai/không xác định được. Báo Fleiss κ, mục tiêu ≥ 0,6.
- Accuracy và F1 của RHR so với nhãn người, so với một judge kiểu Tri-HE chuyển sang tiếng Việt (Qwen2.5-VL-7B).
- **Kiểm tra nhiễu loạn**: đảo chiều quan hệ, thay giới từ trái nghĩa. RHR phải tăng ở ≥ 95% trường hợp.
- RPI: kiểm định hoán vị khác 0.

**Tiền lệ gần nhất.**
- Tri-HE (TMLR 2025): triplet hallucination có trộn lỗi object.
- R-Bench và Reefknot: Y/N phân biệt, không chấm caption tự do.
- VALOR-EVAL: relation faithfulness bằng LLM, tiếng Anh.

Điểm khác: **có điều kiện theo đầu mút, có tỉ lệ đổi vai, có chỉ số prior theo từng caption, có họ quan hệ tiếng Việt**.

### M3. KG-plausibility split: tỉ lệ ảo giác "hợp lý" (PHS) và tỉ lệ vi phạm ràng buộc KG (KCV)
**Định nghĩa.** KG K gồm bao đóng `P279` của Wikidata, giới hạn trong các khái niệm của lexicon và nối qua bảng alias, cộng một bảng ràng buộc chọn lọc tiếng Việt viết tay, nhỏ (cỡ 50-100 động từ/giới từ). Ví dụ: `lái` cần tân ngữ IsA phương tiện; `ăn` cần IsA thức ăn; `ngồi trên` cần tân ngữ có bề mặt.
- **KCV** = #{quan hệ x̂ vi phạm ràng buộc K} / #{quan hệ x̂}.
- **PHS** = #{x̂ ∈ FP: không vi phạm K và pct(r̂ hoặc object) ≥ 0,8 theo prior đồng xuất hiện} / #FP.

PHS trả lời câu hỏi "trong số ảo giác của mô hình, bao nhiêu phần là ảo giác *hợp lý* (khó bắt nhất)?". Hai hệ thống có cùng CHAIR có thể khác nhau rất xa về PHS.

**Cảnh báo, phải ghi trong bài:**
1. Vi phạm thường thức **không đồng nghĩa với** ảo giác, vì ảnh có thể lạ. Vì vậy KCV chỉ dùng chẩn đoán, không làm headline.
2. Chọn sai động từ ("mặc mũ" thay vì "đội mũ") là lỗi **fluency**, không phải factuality. Repo đã tách hai loại này (`metrics_svp.py`, mục §3.3), nên lỗi chọn động từ được gán vào nhóm fluency, không tính vào KCV.
3. LVLM viết rất trôi chảy nên KCV có thể gần 0. Cần đo pilot trên 200 caption trước khi đưa vào bài.

**Kiểm định.** Có 3 người chấm "bộ ba này có hợp lý theo thường thức không" trên 500 bộ ba, báo κ. Validity dự đoán: PHS phải cao hơn ở hệ thống đã biết dựa vào prior (zero-shot so với VSPS), và giảm khi thêm hard negative từ KG (ý tưởng 2 của file 11). Kiểm định bootstrap.

**Tiền lệ gần nhất.** R-Bench (phân tích đồng xuất hiện), VALOR-EVAL và AMBER (chọn ảnh theo associative bias), KG-ViP / C4 trong file 11 (dùng KG để *sửa*, không để *đo*). Điểm khác: **phân rã ảo giác theo từng caption, dùng KG**. Đây là metric yếu nhất trong bốn đề xuất, nên dùng làm phân tích chứ không làm đóng góp chính.

### M4. H-R và SFA: recall có điểm một phần theo phân cấp IsA, và diện tích biên specificity-faithfulness
**Định nghĩa.** IC(c) = −log p(c), với p(c) là tần suất khái niệm c **cộng dồn cả các con** trong caption train KTVIC (information content kiểu Resnik). Với phần tử gold g (s = S) và phần tử candidate c khớp ở tầng LEXICAL:
- c ≡ g: credit 1.
- c là tổ tiên của g ("người" so với "phụ nữ"): **đúng** về precision (TP), recall nhận credit IC(c)/IC(g) ∈ (0, 1).
- c là hậu duệ của g ("phụ nữ" khi gold chỉ có "người"): UNK trừ khi verifier chấm SUPPORTED, vì đây là bịa thêm chi tiết. Quy tắc này nhất quán với hypernym một chiều trong `chair.py`.

Từ đó:

  H-R = Σ_g w(g)·credit(g) / Σ_g w(g)

và báo kèm **Specificity Loss** SL = R_exact-or-ancestor − H-R, tức là phần recall bị mất do nói chung chung.

**SFA**: với một họ hệ thống có núm điều chỉnh θ (ngưỡng verifier τ của VSPS, bật/tắt trung tính hóa, ngân sách entity, độ dài), vẽ các điểm (H-R(θ), P_lo(θ)). SFA là diện tích dưới **đường bao Pareto** của các điểm đó trong [0,1]², tham chiếu tại (0,0), tức hypervolume 2 chiều. Hệ thống chỉ có một điểm thì báo **dominance** so với các họ khác, không báo SFA (hypervolume của một điểm chỉ là P·R, không có thông tin mới).

**Vì sao cần cho VSPS.** VSPS trung tính hóa (phụ nữ → người) có chủ đích. Recall phẳng chấm việc này như một lần bỏ sót, còn LEXICAL tier chấm nó là khớp hoàn toàn. Cả hai đều sai. H-R là cách chấm công bằng duy nhất cho phương pháp, nên đây là động cơ phương pháp luận, không phải thêm metric cho đẹp.

**Tài nguyên.** Lưới hypernym của repo, mở rộng bằng Wikidata `P279` qua alias. Tần suất lấy từ caption train. Chỉ cần CPU.

**Kiểm định.**
- Người so sánh từng cặp "cả hai caption đều đúng, caption nào **cung cấp nhiều thông tin hơn**", trên 400 cặp có cùng tập object nhưng khác độ đặc hiệu. Báo tỉ lệ đồng thuận pairwise của H-R, so với R phẳng và R_LEXICAL. Mục tiêu: H-R thắng có ý nghĩa (McNemar).
- Tương quan IC(c)/IC(g) với điểm thông tin người chấm (1-5) trên 100 cặp khái niệm, báo Spearman.
- SFA: báo kèm CI bootstrap. So với CAPEval / ClaimDiff-RL, những bài chỉ nói "đánh đổi" chứ không định lượng thành diện tích.

**Tiền lệ gần nhất.**
- HalCECE (sửa tối thiểu theo WordNet, để giải thích, không chấm điểm).
- Deng et al. CVPR 2012, "Hedging Your Bets" (đánh đổi accuracy-specificity cho *phân loại*, xem `novelty/03`).
- PROVE (đánh đổi helpfulness-truthfulness), ReflectCAP (biên Pareto, không có metric diện tích).
- CAPTURE và SPICE (từ đồng nghĩa và hypernym là khớp nhị phân).

Điểm khác: **credit một phần theo IC cho recall caption**, và **diện tích biên** cho một họ hệ thống.

---

## 4. Parser tiếng Việt câu → đồ thị (điều kiện tiên quyết cho M1-M4)
- **Phương án rẻ nhất**: dùng lại bước tách mệnh đề sẵn có của VSPS (đầu ra đã có kiểu), không viết parser mới. Chỉ thêm hai việc: đồng tham chiếu instance (gán id nút) và chuẩn hóa giới từ.
- **Nếu chưa đủ**: gán 1.000 caption KTVIC / UIT-OpenViIC thành đồ thị (khoảng 3 phút mỗi caption, khoảng 50 giờ công, **ước tính**), rồi fine-tune Qwen2.5-1.5B hoặc ViT5. Báo F1 bộ ba so với người trên 200 caption giữ lại.
- **Bắt buộc báo**: τ của metric khi dùng *parse gold* so với khi dùng *parse tự động*. Chênh lệch này là sai số do parser. JaSPICE, FACTUAL và DiscoSG đều cho thấy parser là nút thắt.

## 5. Giao thức kiểm định chung (cho M1, M2, M4)
- **Mẫu**: 200 ảnh KTVIC test và 50 ảnh UIT-OpenViIC (kiểm dịch miền), × 6 hệ thống: Qwen2.5-VL-7B zero-shot, Vintern-3B, Qwen3-VL-8B, VSPS-SFT, VSPS-DPO, một caption người giữ lại. Tổng 1.500 caption.
- **Nhãn người**, hai lớp như DOCENT của PoSh:
  - (a) Mức span: đánh dấu từng span ảo giác (object/attr/rel/count) và liệt kê các thứ nổi bật bị bỏ sót.
  - (b) Mức caption: faithfulness 1-5, informativeness 1-5, và 1 phép so sánh cặp trên mỗi ảnh.
- **Người gán**: 2 người bản ngữ gán toàn bộ, người thứ 3 phân xử. 300 caption được 3 người gán độc lập để đo đồng thuận.
- **Đồng thuận**: Krippendorff α cho span (mục tiêu ≥ 0,67), Fleiss κ cho nhãn phần tử, ICC(2,k) cho Likert. Nếu α < 0,67 thì sửa guideline, chưa tính tương quan.
- **Meta-evaluation**:
  - Cấp caption: Kendall τ_b là chính, kèm pairwise accuracy có xử lý tie theo cách WMT mà PoSh dùng.
  - Cấp hệ thống: Spearman. Với chỉ 6 hệ thống, phải ghi rõ là yếu, không dùng làm bằng chứng chính.
  - CI bằng bootstrap 1.000 lần, lấy mẫu lại theo ảnh. So sánh hai metric bằng kiểm định Williams hoặc bootstrap cặp.
- **Baseline**:
  - BLEU-4, CIDEr, CLIPScore đa ngữ (2502.06600).
  - CHAIR-vi và VCF/PGF của repo.
  - DCScore chuyển sang tiếng Việt (judge Qwen2.5-VL-7B).
  - Judge kiểu PoSh dùng đồ thị của M1 làm rubric.
- **Cỡ mẫu**: với n ≈ 1.500, sai số chuẩn của τ dưới giả thuyết không là √(2(2n+5)/(9n(n−1))) ≈ 0,017. Đủ để phân biệt Δτ ≈ 0,05 giữa hai metric (ước tính thô, kiểm định cặp còn chặt hơn).
- **Chi phí người** (ước tính): 1.500 × 2 người × khoảng 3,5 phút ≈ 175 giờ, cộng phân xử khoảng 20 giờ. GPU: parse cộng verifier cho UNK, khoảng vài GPU-giờ trên 3090 (**chưa đo**).
- **Phát hành**: đồ thị người duyệt, nhãn span và mã metric (`rescap/metrics_graph.py`, gọi lại `svp/matching.py`).

## 6. Xếp hạng và khuyến nghị
| Metric | Mới (so với các bài đã mở) | Khả thi trên 1× 3090 | Rủi ro chính | Khuyên |
|---|---|---|---|---|
| M1 ViVG-P/R | Cao (gold 3 trạng thái, precision dạng khoảng, ràng buộc instance, tiếng Việt) | Cao | "Chỉ là SPICE/CompreCap tiếng Việt" → phải có ablation chứng minh từng thành phần làm τ tăng | **Làm trước**, là đóng góp metric chính |
| M2 ViRHR + RSR + RPI | Trung bình-cao | Cao | Ít quan hệ đánh giá được mỗi caption → cần đủ mẫu | Làm cùng M1 (chung đồ thị) |
| M4 H-R + SFA | Trung bình-cao | Cao | Ước lượng IC trên tập caption nhỏ bị nhiễu, và SFA cần núm điều chỉnh | Làm, vì cần để chấm công bằng việc trung tính hóa của VSPS |
| M3 PHS/KCV | Trung bình | Trung bình (phụ thuộc alias Wikidata, ConceptNet chưa rõ) | KCV có thể gần 0, và lẫn với lỗi fluency | Chỉ làm phân tích phụ |

Cách đóng khung một câu: *"Các metric dạng đồ thị hiện nay coi gold là nhị phân và chỉ có cho tiếng Anh. Chúng tôi chấm caption tiếng Việt trên một đồ thị đã kiểm chứng ba trạng thái, có ràng buộc instance, cho ra precision dạng khoảng, recall có điểm một phần theo phân cấp và tỉ lệ ảo giác quan hệ có điều kiện, được kiểm định trên 1.500 caption có nhãn span của người."*

## 7. Chưa xác minh / hạn chế
- **Venue của CAPTURE (2405.19092)**: comment arXiv trống, Semantic Scholar bị 429. Chưa trích venue.
- **PROVE ở ICCV 2025**: chỉ theo S2 (file 11), chưa đối chiếu proceedings. **G19 (2604.01460) ở COLM 2026**: chỉ theo comment arXiv.
- **Tương quan của CompreCap (0,989 / 0,927 / 0,982)**: đọc từ bảng HTML phụ lục. Việc đây là tương quan *cấp mô hình* là suy ra từ câu "across all LVLMs", chưa đọc kỹ phụ lục A.2.
- **Số liệu chưa trích được**: DSG, FIHA, PROVE, Tri-HE (bảng 3), R-Bench, ALOHa, JaSPICE. Đã mở bài nhưng không lấy được con số, nên không dùng số nào cho các bài này.
- **ConceptNet tiếng Việt**: API 502. **Vietnamese WordNet / OMW `vie`**: chưa kiểm.
- **Không mở**: WHOOPS! (ảnh phi thường thức) và hierarchical P/R của Kiritchenko et al. Đây là nền tảng có thể nên trích cho M3/M4, cần mở trước khi dùng.
- **Quét chưa đầy đủ**: truy vấn OpenAlex và S2 cho mục §1.3-5/6 bị 429. Kết luận "chưa thấy" dựa trên arXiv API cộng các file trong `research_wall/`, `novelty/`. Cần chạy lại khi API mở: OpenAlex `title_and_abstract.search:caption AND (hierarchical OR hypernym OR "information content") AND (recall OR metric)`, và `caption AND commonsense AND hallucination AND (metric OR rate)`.
- Mọi chi phí giờ công và GPU ở §3-5 là **ước tính, chưa đo**.
