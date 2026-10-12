# 01 — Thước đo ảo giác / trung thực ngoài CHAIR (khảo sát 10/2026)

Bối cảnh: hiện chỉ có CHAIR_s/CHAIR_i tiếng Việt (lexicon 113 lớp, gold suy từ 5 tham chiếu KTVIC), cộng CHAIR/P/R trên COCO-5000 (`coco_probe.py`, gold = instances_val2014 ∪ tham chiếu). Kiểm tra AI-silver (300 ảnh) cho thấy khoảng 56% "ảo giác" theo tham chiếu là đối tượng có thật nhưng không được nhắc. Vì vậy thước đo bổ sung phải (a) không phụ thuộc tham chiếu thiếu, hoặc (b) dùng gold đầy đủ do người xác nhận.

Ràng buộc: 1 RTX 3090 24 GB. Qwen2.5-VL-7B bf16 vừa bộ nhớ. Không chạy song song hai mô hình 7B bf16 (judge + VLM): chạy tuần tự, hoặc nạp judge 4-bit.

Quy ước thời gian (ước lượng, chưa đo trên 3090): caption ngắn ~2,6 s/ảnh (1,88 s trên 4090 × ~1,4), caption chi tiết 160 token ~5 s, caption 512 token ~10 s, câu hỏi có/không ~0,4 s. "Hệ" = một checkpoint (zero-shot, P1, fuse2, VSPS, VCD…).

Xác minh: mọi mục có arXiv ID/venue đã được tra web ngày 12/10/2026, trừ các ô ghi **UNVERIFIED** hoặc "(nhớ)" (biết từ trước, lần này chưa tra lại).

## 1. Bảng so sánh

Ký hiệu loại: E = tồn tại, A = thuộc tính, R = quan hệ, C = đếm. "Tham chiếu?" nghĩa là cần caption tham chiếu khi chấm. "Gold người?" nghĩa là cần nhãn người trên chính tập chấm. Kỳ vọng Q1 (TMM/PR/Neurocomputing): ★★★ gần như bắt buộc, ★★ hay bị hỏi, ★ có thì tốt.

| Thước đo | Nguồn (arXiv · venue) | Code | Đo gì | Tham chiếu? | Gold người? | Port sang tiếng Việt | 3090 / hệ | Q1 |
|---|---|---|---|---|---|---|---|---|
| CHAIR | 1809.02156 · EMNLP 2018 | (nhiều bản) | E, sinh tự do | Có (+ seg COCO) | Có (COCO) | Đã có (113 lớp) | đã chạy | ★★★ |
| **POPE** (random/popular/adversarial) | 2305.10355 · EMNLP 2023 | github.com/RUCAIBox/POPE | E, có/không | Không | Có (gold đối tượng) | Dễ: template "Trong ảnh có {X} không?" | 9.000 câu ≈ 1,0 h | ★★★ |
| **RePOPE** | 2504.15707 · arXiv 2025 | github.com/YanNeu/RePOPE | POPE với nhãn COCO sửa lỗi | Không | Có (đã sửa) | Như POPE | +0 (chấm lại) | ★★ (đúng luận điểm gold thiếu) |
| POPE MUL (13 ngôn ngữ) | 2408.00550 · arXiv | github.com/ssmisya/MHR | E, POPE dịch bằng GPT-3.5 | Không | Có | Không rõ có tiếng Việt (abstract không liệt kê). **UNVERIFIED** | ≈ 1,0 h | ★ |
| CLAIM (POPE đa ngữ) | 2506.11073 · ACL 2025 | (chưa tra) | E, POPE dịch Google Translate | Không | Có | Danh sách ngôn ngữ chưa kiểm | ≈ 1,0 h | ★ |
| Multi-POPE | 2604.18347 · arXiv 2026 | (chưa tra) | E | Không | Có | Chỉ DE/EN/ES/FR/IT, không có tiếng Việt | — | ★ |
| **AMBER** | 2311.07397 · arXiv (chưa thấy venue) | github.com/junyangwang0410/AMBER | E/A/R; sinh (CHAIR, Cover, Hal, Cog) + phân biệt | Không (dùng nhãn AMBER) | Có sẵn (1.004 ảnh) | Phần sinh khớp từ vựng tiếng Anh. Port = dịch ~337 từ + từ đồng nghĩa, mức trung bình. Phần phân biệt chỉ cần dịch template | gen ≈ 2,8 h + disc 14k câu ≈ 1,6 h | ★★★ |
| CHAIR theo giao thức OPERA/VCD (500 ảnh COCO, 512 token) | (giao thức) | theo OPERA/VCD | E | Có | Có (COCO) | Tiếng Anh | ≈ 1,4 h | ★★★ (để so với tài liệu decoding) |
| Object HalBench | RLHF-V 2312.00849 · CVPR 2024 | github.com/RLHF-V/RLHF-V (nhớ) | E, mô tả chi tiết, 300 ảnh COCO, 8 prompt | Có (COCO) | Có | Dùng ChatGPT trích đối tượng. Thay bằng LLM cục bộ thì không còn so sánh được | ≈ 0,9 h + judge | ★★ (bài có DPO) |
| MMHal-Bench | 2309.14525 · Findings ACL 2024 (nhớ) | LLaVA-RLHF (nhớ) | E/A/C/R…, 96 câu hỏi | Không | Có | Judge GPT-4. Port không đáng | < 0,1 h + API | ★★ (bài RLHF/DPO) |
| HallusionBench | 2310.14566 · CVPR 2024 (venue chưa tra lại) | github.com/tianyi-lab/HallusionBench | Suy luận/ảo ảnh thị giác, biểu đồ, có/không | Không | Có | Không liên quan caption | < 0,2 h | ★ (đánh giá LVLM tổng quát) |
| THRONE | 2405.05256 · CVPR 2024 | (chưa tra) | E, sinh tự do (Type I) bằng LM judge mở | Không | Có (COCO/Objects365) | LM judge tiếng Anh | ≈ 1–2 h | ★★. Thông điệp chính: Type I và Type II (POPE) **có thể nghịch tương quan** ⇒ không được chỉ báo POPE |
| CCEval | HallE-Control 2310.01779 · arXiv | github.com/bronyayang/HallE_Control | E trong caption chi tiết + coverage | Có (VG) | Có | Judge GPT-4 | API | ★ |
| ALOHa | 2404.02904 · NAACL 2024 (short) | **UNVERIFIED** | E mở từ vựng, LLM trích + khớp embedding | **Có** (tham chiếu + detection) | Không | Kế thừa vấn đề tham chiếu thiếu của KTVIC | ≈ 0,5 h với LLM cục bộ | ★★ |
| OpenCHAIR | 2312.03631 · EMNLP 2024 | github.com/assafbk/mocha_code | E mở từ vựng (ảnh sinh + LLM) | Có (ảnh tổng hợp) | Không | Benchmark tiếng Anh cố định | ≈ 1 h | ★ |
| HaELM | 2308.15126 · arXiv | github.com/junyangwang0410/HaELM | LLM nhận diện ảo giác | Có | Train trên nhãn | Phải huấn luyện lại cho tiếng Việt | — | ✗ (lỗi thời) |
| M-HalDetect | 2308.06394 · AAAI 2024 | (chưa tra) | Nhãn ảo giác mức câu/đoạn (16k) | — | Có | Bộ huấn luyện detector tiếng Anh | — | ★ |
| HalLoc | 2506.10286 · CVPR 2025 | github.com/dbsltm/cvpr25_halloc | Định vị token: E/A/R/scene | — | Có (150k) | Detector VisualBERT tiếng Anh | — | ★ |
| UniHD / MHaluBench | 2402.03190 (nhớ: ACL 2024) | EasyDetect (nhớ) | Phát hiện ảo giác mức claim | — | Có | Tiếng Anh | — | ★ |
| HalDec-Bench | 2603.15253 · arXiv 2026 | trang dự án dahlian00.github.io | Benchmark cho **detector** ảo giác caption, nhãn đoạn | — | Có | Dùng để chọn judge, không chấm mô hình | — | ★ (dẫn chứng judge có giới hạn) |
| FaithScore | 2311.01477 · Findings EMNLP 2024 | github.com/bcdnlp/FAITHSCORE (ACL Anthology lại trỏ FIHA, chưa rõ repo nào chính thức) | Tách atomic fact → VLM kiểm chứng; E/A/R/C | **Không** | Không | Trung bình: LLM cục bộ tách fact tiếng Việt + VLM kiểm chứng | ≈ 2 h / hệ (558 ảnh × 2 mode) | ★★★ (cho caption dài) |
| FIHA | 2409.13612 · arXiv | (xem trên) | Tự sinh câu hỏi chi tiết, E/A/R | Không | Không | Trung bình | ≈ 1 h | ★ |
| CapMAS factuality/coverage | 2412.15484 · ICML 2025 (nhớ; một index ghi khác) | github.com/adobe-research/CapMAS | Precision trên mệnh đề nguyên tử; coverage qua VQA trên IIW-400 | Factuality: không | Coverage: có (VQA) | Factuality port như FaithScore | ≈ 2 h | ★★ |
| DCScore / DeCapBench | 2503.07906 · ICLR 2025 | **UNVERIFIED** | Đơn vị thông tin nguyên thủy: ảo giác + độ đầy đủ | Có (đơn vị tham chiếu do người viết) | Có | Thiếu tham chiếu đơn vị tiếng Việt, judge GPT-4o | API | ★★ |
| CAPTURE / DetailCaps | 2405.19092 (nhớ) | PyPI `capture-metric` (đã thấy); GitHub **UNVERIFIED** | Khớp object/attribute/relation (scene graph) với tham chiếu | Có | Có | Parser scene graph tiếng Anh: khó | < 0,2 h CPU | ★ |
| CompreCap | 2412.08614 · CVPR 2025 | **UNVERIFIED** | Coverage + độ đúng A/R so với scene graph người, 560 ảnh | Có (scene graph) | Có | Ảnh cố định, caption phải bằng tiếng Anh | ≈ 0,8 h | ★★ (mode detailed) |
| VALOR-Eval | 2404.13874 · Findings ACL 2024 | (link GitHub trong bài) | Faithfulness + coverage E/A/R, CHAIR mở rộng khớp ngữ nghĩa | Có | Có | Judge LLM tiếng Anh | ≈ 1 h + judge | ★★ (cùng khung P/R như bài) |
| CLAIR | 2310.12971 · EMNLP 2023 | (link trong arXiv) | Điểm tổng thể bằng LLM (không riêng ảo giác) | Có | Không | Prompt tiếng Việt được | judge | ★ |
| CapArena-Auto | 2503.12329 · Findings ACL 2025 | đã mở mã (theo abstract) | So cặp, VLM-as-judge, tổng thể | Không | Không | Tiếng Anh, ~4 USD/lần | API | ★ |
| R-Bench | 2406.16449 · ICML 2024 | github.com/mrwu-mac/R-Bench | R, có/không, ảnh nocaps | Không | Có | Template dịch được | ~11k câu ≈ 1,3 h | ★★ (nếu bài khẳng định về quan hệ) |
| ARO | 2210.01936 · ICLR 2023 (nhớ) | vision-language-models-are-bows (nhớ) | Thứ tự/quan hệ/thuộc tính, cho mô hình contrastive | — | Có | Không hợp với LVLM sinh | — | ✗ |
| ROPE | 2407.06192 · NeurIPS 2024 | multi-object-hallucination.github.io | E nhiều đối tượng, prompt trỏ vùng | Không | Có | Template | ≈ 1 h | ★ |
| PhD | 2403.11116 · CVPR 2025 | (trang GitHub của tác giả) | E/A/sentiment/vị trí/C; ngữ cảnh gây nhiễu | Không | Có | Dịch câu hỏi | 102k câu: lấy mẫu | ★ |
| HaloQuest | 2407.15680 · ECCV 2024 | (chưa tra) | Tiền đề sai, thiếu ngữ cảnh; VQA | Không | Có | Không hợp caption | — | ✗ |
| Hal-Eval | 2402.15721 · ACM MM 2024 | "sẽ release" **UNVERIFIED** | E/A/R + event | — | Có | Tiếng Anh | — | ★ |
| VHTest | 2402.14683 · Findings ACL 2024 | github.com/wenhuang2000/VHTest | 8 kiểu VH, ảnh DALL-E-3 | Không | Có | Không hợp caption | — | ✗ |
| SHALE | 2508.09584 · ACM MM 2025 | github.com/BeiiiY/SHALE | 12 khía cạnh tri giác + nhiễu | Không | Tự động | Tiếng Anh | — | ★ |
| DASH / DASH-B | 2503.23573 · ICCV 2025 | (chưa tra) | Ảo giác đối tượng có hệ thống trên ảnh thật | Không | — | — | lớn | ✗ |
| DOCCI / DCI (dữ liệu mô tả dày) | DOCCI 2404.19753 · ECCV 2024; DCI 2312.08578 · CVPR 2024 (nhớ) | Google/Meta | Dataset mô tả dày, không phải thước đo | Có | Có | — | — | ✗ |
| FactVC | 2303.02961 · EMNLP 2023 | (chưa tra) | Factuality caption **video**, có nói khả năng dùng cho ảnh | Không | Train | Tiếng Anh | — | ✗ |
| SHROOM-Visions 2026 | 2608.25662 · đang review (UncertaiNLP@EMNLP 2026) | — | Span ảo giác, 5 lớp | — | Có | ZH/EN/FR/IT, không có VI | — | ✗ |
| CCHall | 2505.19108 · ACL 2025 | (chưa tra) | Ảo giác chéo ngôn ngữ × chéo phương thức | — | Có | Ngôn ngữ chưa xác định. **UNVERIFIED** | — | ★ |
| ViHallu (DSC2025) | 2601.04711 · arXiv 2026 | — | Ảo giác LLM tiếng Việt, **chỉ văn bản** | — | Có | Đã là tiếng Việt nhưng không có ảnh | — | ✗ (chỉ để dẫn) |

Không tìm thấy / không áp dụng:
- **CHAIR-MEF**: không có kết quả tìm kiếm. **UNVERIFIED, coi như không tồn tại.**
- **ViPOPE** / POPE tiếng Việt cho ảnh: không tìm thấy. Có một trang tổng hợp nhắc "ViHallu" dạng thị giác nhưng không có nguồn gốc ⇒ **UNVERIFIED**. Đây là khoảng trống mà bài có thể lấp (POPE-vi trên KTVIC).
- **RAHF** (Rich Human Feedback) thuộc text-to-image, không phải captioning. **MHumanEval** là benchmark sinh code đa ngữ. Cả hai không liên quan.

## 2. Nhận xét nhanh

1. Mọi thước đo dựa trên tham chiếu (CHAIR, ALOHa, CAPTURE, VALOR, DCScore) đều mang lỗi gold thiếu mà ta đã đo (~56% "ảo giác" thật ra có mặt). RePOPE (2025) cho thấy ngay cả nhãn COCO của POPE cũng sai đủ để đổi thứ hạng. Đây là trích dẫn mạnh để hợp thức hóa phân tích AI-silver của bài.
2. THRONE: giảm ảo giác dạng có/không (POPE) **không** kéo theo giảm ảo giác trong sinh tự do. Vì vậy reviewer sẽ đòi cả hai: POPE (phân biệt) và một thước đo sinh tự do (CHAIR/AMBER-gen/FaithScore).
3. Chưa có benchmark ảo giác VLM tiếng Việt nào được công bố (chỉ có ViHallu dạng văn bản). POPE-vi trên KTVIC + gold người là đóng góp phụ hợp lệ.
4. Judge GPT-4/4o (MMHal, CCEval, DCScore, Object HalBench gốc) mâu thuẫn với thông điệp "1 GPU, tái lập được". Dùng judge cục bộ, khác họ mô hình (không dùng Qwen chấm Qwen), và báo độ đồng thuận judge–người trên một tập nhỏ.

## 3. Danh sách áp dụng (xếp hạng)

### #1. CHAIR + Object P/R trên gold người đầy đủ, và POPE-vi từ cùng gold (KTVIC)
- **Vì sao:** sửa tận gốc vấn đề gold thiếu. Một lần gán nhãn nuôi được hai thước đo.
- **Gold:** 300 ảnh `data/object_gold/sample.json`, 2 người tick theo `annotate.html` (giao diện đã có, kế hoạch B1). Bắt đầu từ `annot_claude.json` làm gợi ý; người sửa và có thêm trạng thái "không chắc". Báo Cohen κ (`agreement.py`).
- **CHAIR-full:** `object_gold_score.py` / `silver_precision.py` với gold = nhãn người. Báo P, R, F1, CHAIR_i, CHAIR_s, kèm CI bootstrap theo ảnh.
- **POPE-vi:** mỗi ảnh lấy 3 đối tượng dương (gold người) và 3 âm cho mỗi split. Random: lấy từ 101 lớp. Popular: top tần suất trong train KTVIC. Adversarial: top đồng xuất hiện với các lớp dương (thống kê từ tham chiếu train). 300 × 6 × 3 = 5.400 câu. Prompt: "Trong ảnh có {tên lớp} không? Trả lời có hoặc không." Hạ tầng hỏi đã có trong `probe_existence.py`. Âm tính **phải được người xác nhận vắng mặt** (bài học RePOPE). Báo Acc/P/R/F1 và tỉ lệ "có".
- **3090:** sinh caption đã có sẵn. POPE-vi 5.400 × 0,4 s ≈ **0,6 h/hệ**, 5 hệ ≈ 3 h. Chi phí chính là thời gian gán nhãn của người.

### #2. POPE chuẩn trên COCO (+ chấm lại bằng nhãn RePOPE), hỏi bằng tiếng Anh và tiếng Việt
- **Vì sao:** reviewer Q1 gần như luôn đòi. Rẻ. Có thể so trực tiếp với số đã công bố của Qwen2.5-VL-7B gốc.
- **Cách làm:** lấy 3 file `coco_pope_{random,popular,adversarial}.json` từ RUCAIBox/POPE (500 ảnh val2014; tải ảnh bằng `download_coco_images.py`). Chạy prompt gốc tiếng Anh, sau đó bản tiếng Việt (tên lớp qua `coco80_vi.json`). Chấm lại bằng nhãn RePOPE (bỏ mục "ambiguous"). Thêm một script `scripts/pope_eval.py` khoảng 80 dòng, tái dùng `load_model` của `coco_probe.py`.
- **3090:** 9.000 câu × 0,4 s ≈ **1,0 h/hệ/ngôn ngữ**. 5 hệ × 2 ngôn ngữ ≈ 10 h. Có thể chỉ chạy song ngữ cho P1, fuse2 và zero-shot (≈ 6 h).

### #3. AMBER (sinh + phân biệt, LLM-free), tiếng Anh trên ảnh AMBER và bản port tiếng Việt
- **Vì sao:** đo E/A/R trong một khung. Cặp chỉ số Cover (độ phủ) và Hal/CHAIR khớp đúng câu chuyện đánh đổi recall/precision của bài. Không cần LLM judge nên hợp với yêu cầu 1 GPU.
- **Cách làm (EN):** chạy repo gốc. Mô hình sinh "Describe this image." bằng tiếng Anh (fine-tune tiếng Việt có thể làm giảm chất lượng tiếng Anh; cần báo rõ). Phần phân biệt gồm khoảng 14k câu có/không.
- **Cách làm (VI):** dịch danh sách đối tượng AMBER sang tiếng Việt, mỗi lớp kèm từ đồng nghĩa và tái dùng tokenizer RDRSegmenter của `rescap/chair.py`. Sinh caption tiếng Việt bằng prompt `detailed`, rồi tính CHAIR/Cover/Hal/Cog bằng công thức AMBER. Dịch template câu hỏi phân biệt (tồn tại/thuộc tính/quan hệ) bằng tay, sau đó soát.
- **3090:** gen 1.004 ảnh × ~10 s ≈ 2,8 h; disc 14k × 0,4 s ≈ 1,6 h ⇒ **≈ 4,4 h/hệ/ngôn ngữ**. Đề xuất EN cho 3 hệ + VI cho 3 hệ ≈ 26 h. Có thể bỏ phần disc tiếng Việt để còn ≈ 17 h.

### #4. FaithScore-vi: tách atomic fact rồi VLM kiểm chứng, không cần tham chiếu (KTVIC detailed + mẫu COCO)
- **Vì sao:** thước đo duy nhất trong danh sách vừa không dính gold thiếu, vừa chấm cả A/R/C trong caption dài, và chạy được bằng tiếng Việt. Đây là câu trả lời trực tiếp cho câu hỏi "P giảm là ảo giác hay do tham chiếu thiếu?".
- **Cách làm:**
  1. Tách fact: Qwen2.5-7B-Instruct (chỉ văn bản, bf16 ≈ 15 GB), few-shot tiếng Việt → JSON `[{fact, loại: E/A/R/C}]`.
  2. Kiểm chứng: dùng VLM **khác họ** với mô hình được chấm, ví dụ InternVL-8B (họ InternVL; Vintern là bản tiếng Việt của họ này), câu hỏi "Mệnh đề sau đúng với ảnh không: …? có/không". Lấy P(có) làm điểm mềm.
  3. Chỉ số: FaithScore = tỉ lệ fact đúng, báo thêm theo từng loại E/A/R/C.
  4. Meta-eval: 100 caption × 2 người gán nhãn fact. Báo độ đồng thuận judge–người (κ, Pearson). Nếu dưới mức chấp nhận thì chỉ báo như phân tích phụ (HalDec-Bench cho thấy judge bỏ sót ảo giác tinh vi).
- **3090 (tuần tự, không nạp đồng thời):** tách fact 1.116 caption × ~3 s ≈ 0,9 h; kiểm chứng ≈ 1.116 × 5 fact × 0,4 s ≈ 0,6 h ⇒ **≈ 1,5–2 h/hệ** trên KTVIC. 500 ảnh COCO cộng thêm ≈ 0,8 h. 5 hệ ≈ 10–14 h.

### #5. CHAIR chuẩn tiếng Anh theo giao thức OPERA/VCD (500 ảnh COCO val2014, max 512 token)
- **Vì sao:** bài đã so với VCD (repo có `coco*_scores.json`). Reviewer sẽ muốn số CHAIR_s/CHAIR_i theo đúng giao thức của nhóm bài decoding, có thể đặt cạnh số công bố.
- **Cách làm:** prompt "Please describe this image in detail.", max_new_tokens = 512, greedy. Dùng `chair.py` gốc của Rohrbach (synonyms COCO + instances_val2014). Báo thêm Recall (tỉ lệ đối tượng gold được nhắc) và độ dài, để tránh lời giải "ngắn = ít ảo giác".
- **3090:** 500 × ~10 s ≈ **1,4 h/hệ**. 5 hệ ≈ 7 h.

### #6 (tùy chọn). R-Bench image-level hoặc CompreCap
Chỉ thêm nếu bài khẳng định gì đó về quan hệ hoặc độ phủ chi tiết. R-Bench: khoảng 1,3 h/hệ, dịch template. CompreCap: khoảng 0,8 h/hệ, chỉ tiếng Anh, cần kiểm tra code (**UNVERIFIED**).

**Tổng GPU (3090, ước lượng):** #1 ≈ 3 h, #2 ≈ 6–10 h, #3 ≈ 17–26 h, #4 ≈ 10–14 h, #5 ≈ 7 h ⇒ **khoảng 45–60 GPU-giờ**. Riêng gói tối thiểu cho reviewer (#1 + #2 EN + #5 + #4 trên KTVIC cho P1/fuse2/zero-shot) ≈ 20 h.

**Không khuyến nghị:** MMHal-Bench, CCEval, DCScore, CapArena-Auto (phụ thuộc GPT-4/4o, mâu thuẫn với "1 GPU, tái lập được". Nếu reviewer đòi MMHal-Bench thì chạy riêng, 96 câu, chi phí API rất nhỏ). HallusionBench, HaloQuest, VHTest, PhD (đo VQA/suy luận, không đo caption). HaELM (lỗi thời, cần huấn luyện lại).
