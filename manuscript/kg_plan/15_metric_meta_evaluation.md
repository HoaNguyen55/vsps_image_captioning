# 15. Meta-evaluation cho metric đồ thị tiếng Việt: các bài 2025-2026 kiểm định metric mới thế nào, và giao thức đề xuất

Agent KG-plan 15, ngày 2026-10-10. Góc nhìn: một metric caption mới năm 2025-2026 phải qua những phép thử nào thì reviewer mới chấp nhận (dữ liệu phán xét của người, hệ số tương quan, độ chính xác cặp, kiểm thử độ bền, đa ngữ). Từ đó thiết kế giao thức meta-evaluation cho họ metric đồ thị tiếng Việt (graph P/R/F trên mệnh đề có kiểu, xem 11 §4 và VSPS), kèm ước tính giờ gán nhãn.

Cách xác minh: mở trang `arxiv.org/abs/<id>` (lấy title, ngày, dòng Comments ghi venue, abstract), đọc HTML với các bài cần số liệu (2503.14604, 2503.12329, 2509.25818, 2512.21582, 2502.06600), và mở trang ACL Anthology với JaSPICE và SPECS. arXiv export API, Semantic Scholar và OpenAlex đều bị giới hạn tần suất (HTTP 429, hết ngân sách) trong phiên này, nên số venue lấy từ dòng Comments của arXiv hoặc từ ACL Anthology. Những mục chỉ dựa vào file 02 thì có ghi "(theo 02)".

---

## 1. Năm 2025-2026, metric caption mới được kiểm định ra sao

### 1.1 Bảng bài (đã mở)

| # | Bài | Venue (nguồn) | arXiv / link | Dữ liệu người dùng để kiểm định | Thước đo meta-eval |
|---|---|---|---|---|---|
| M1 | Image Captioning Evaluation in the Age of MLLMs (Sarto, Cornia, Cucchiara) | IJCAI 2025, survey (Comments) | 2503.14604 | Bảng chuẩn gồm Flickr8k-Expert, Flickr8k-CF, Polaris, Nebula, Composite, Pascal-50S, FOIL | Flickr8k-Expert/Polaris/Nebula/Composite dùng **Kendall τ_c**, Flickr8k-CF dùng **τ_b**, Pascal-50S và FOIL dùng **accuracy** |
| M2 | EXPERT (giải thích có cấu trúc) | Findings ACL 2025 (Comments) | 2506.24016 | Bộ chuẩn như M1, cộng human eval chất lượng lời giải thích | τ_b cho Flickr8k-CF, τ_c cho các bộ còn lại, accuracy Pascal-50S |
| M3 | Pearl + bộ **Spica** (~333K phán xét, 2.360 người, >75K ảnh) | AAAI 2026 (Comments) | 2512.21582 | Composite, Flickr8K-Expert, Flickr8K-CF, Nebula, FOIL; tự xây dữ liệu train | Báo cả **τ_b và τ_c**, accuracy FOIL 1-ref/4-ref, và **thời gian chạy** |
| M4 | VELA + **LongCap-Arena** (7.805 ảnh, 32.246 phán xét, 1.020 người) | EMNLP 2025 main (Comments) | 2509.25818 | Thang **5 điểm**, 3 khía cạnh (Descriptiveness / Relevance / Fluency), **≥3 người mỗi caption**, lấy trung bình; dùng mask SAM để gợi ý mức chi tiết | τ_c (τ_b ở phụ lục). **Trần người**: 6 người chia 2 nhóm, tính τ_c của từng người so với nhãn chuẩn → đây là cơ sở cho tuyên bố "superhuman" |
| M5 | CapArena (>6.000 cặp đối đầu trên ảnh DOCCI) | Findings ACL 2025 (ACL Anthology 2025.findings-acl.724) | 2503.12329 | Lúc đầu thử thang 1-5 kiểu Hodosh nhưng **đồng thuận giữa người thấp**, nên chuyển sang **so sánh cặp**. Lấy 400 mẫu chấm chéo, **agreement 0,782** | Agreement cấp caption **và** tương quan xếp hạng cấp mô hình. METEOR khớp ở cấp caption nhưng lệch hệ thống ở cấp mô hình |
| M6 | PoSh + **DOCENT** (tranh nghệ thuật, tham chiếu do chuyên gia viết, sinh viên lịch sử nghệ thuật chấm) | ICLR 2026 (Comments) | 2510.19060 | Phán xét **chi tiết (theo lỗi)** và **thô**; scene graph làm rubric cho LLM-judge | Tương quan với người (Spearman, theo 02), định vị lỗi theo span |
| M7 | DCScore / DeCapBench | ICLR 2025 (Comments) | 2503.07906 | Đơn vị thông tin nguyên thủy, 400 ảnh ImageInWords có tham chiếu chuyên gia (theo 02) | Tương quan với người, tương quan với arena cấp mô hình |
| M8 | CapMAS (metric factuality + coverage cho caption siêu chi tiết) | ICML 2025 (Comments) | 2412.15484 | Người chọn caption nào đúng sự thật hơn trên DOCCI | Độ khớp với phán xét cặp về factuality |
| M9 | CAPEval (Coverage và Precision tách riêng, checklist nguyên tử do người kiểm) | arXiv 2026-08 | 2608.02589 | 10 captioner, thí nghiệm downstream | **Kiểm định ngoài (extrinsic)**: Coverage dự báo tốt hiệu năng hiểu, Precision dự báo tốt hiệu năng sinh |
| M10 | SPECS (CLIPScore cho caption dài) | EMNLP 2025 main (ACL Anthology 2025.emnlp-main.477) | — | Giao thức DeCapBench | Tương quan với người ngang LLM-metric mã nguồn mở nhưng rẻ hơn nhiều |
| M11 | Evaluation of Multilingual Image Captioning: How far with CLIP? (Gomes, Zerva, Martins) | Findings NAACL 2025 (Comments) | 2502.06600 | **Dịch máy** VICR và VALSE sang 9 ngôn ngữ (fr, de, es, zh, pt, it, ru, nl, ko), **lọc bằng QE (COMETKiwi)**; thêm XM3600 có sẵn đa ngữ | Spearman ρ, Kendall τ_b, τ_c; accuracy phân loại entailment. **Không có tiếng Việt** (đã grep HTML) |
| M12 | CAMScore (cycle T2I) | arXiv 2025-01 | 2501.03567 | Flickr8k-Expert và các bộ khác | τ_b, τ_c |
| M13 | Redemption Score | IEEE TMM (Comments: accepted version) | 2505.16180 | Flickr8k | Kendall τ = 58,42 |
| M14 | BEiTScore (cross-encoder, tăng cường dữ liệu đối kháng bằng LLM) | arXiv 2026-05 | 2605.21728 | Sáu benchmark, cộng một benchmark mới cho caption chi tiết | Kendall τ, so với EXPERT và FLEUR |
| M15 | Rigel (video + ảnh, bộ Vid-Lepus) | arXiv 2026-06 | 2606.29997 | Bộ người tự xây | Tương quan với người |
| M16 | Structured audio captions validated by controlled perturbations | arXiv 2026-07 | 2607.21424 | Không có người: **nhiễu có kiểu, có cấp độ** áp lên nhãn chuẩn | Metric phải **bất biến với diễn đạt lại giữ nghĩa** và **nhạy với sai lệch ngữ nghĩa thật**. Đây là khuôn mẫu cho bộ kiểm thử độ bền dưới đây |
| M17 | Soft Pairwise Accuracy (SPA) | WMT 2024 (Comments) | 2409.09598 | — (meta-metric) | Ổn định hơn PA, ít hoà hơn, phân biệt được nhiều cặp metric có ý nghĩa thống kê hơn. Là metric cấp hệ thống chính thức của WMT24 |
| M18 | MetaMetrics | ICLR 2025 (Comments) | 2410.02381 | Kết hợp các metric có sẵn theo điểm người, đa ngữ, nhiều miền | — (dùng làm baseline "tổ hợp metric") |

Nền (trước 2025, mỗi mục một dòng): Polos/**Polaris** (CVPR 2024, 2402.18091; 131K phán xét, 550 người). DENEB/**Nebula** (ACCV 2024, 2409.19255; 32.978 ảnh, 805 người; bền với ảo giác trên FOIL). BRIDGE (ECCV 2024, 2407.20341). FACTUAL/SoftSPICE (Findings ACL 2023, 2305.17497). **JaSPICE** (CoNLL 2023, ACL Anthology 2023.conll-1.28): SPICE cho tiếng Nhật, kèm bộ **Shichimi** gồm 103.170 phán xét người trên 10 mô hình.

### 1.2 Những gì đã thành "chuẩn tối thiểu" năm 2025-2026

1. **Kendall τ_c là hệ số chính, τ_b đi kèm.** Bảng M1 và M3 đều dùng quy ước theo bộ: τ_b cho Flickr8k-CF, τ_c cho các bộ còn lại. Spearman chỉ là phụ (M6, M11). Pearson gần như không còn được báo.
2. **Hai cấp đánh giá.** Cấp caption (τ, hoặc agreement theo cặp) **và** cấp hệ thống (xếp hạng mô hình). M5 cho thấy một metric có thể khá ở cấp caption mà vẫn sai ở cấp hệ thống.
3. **Kiểm thử ảo giác bắt buộc.** FOIL accuracy (thay một từ đối tượng) có trong M1, M3 và DENEB. Với caption chi tiết thì có thêm phán xét factuality (M8, M9) và lỗi gắn thuộc tính/quan hệ (M6).
4. **Tách precision và coverage.** M4 (Desc./Rel.), M8, M9 và DCScore đều chấm hai trục riêng. Một điểm vô hướng duy nhất đang bị coi là lỗi thiết kế.
5. **Trần người (human ceiling).** M4 so metric với từng người chấm. Nếu bài định tuyên bố metric "gần người" thì phải có con số này.
6. **Chi phí/thời gian chạy** là một cột trong bảng (M3, M4, M10). Metric LLM-free được bán bằng lập luận "trung lập và rẻ" (M3).
7. **Đa ngữ:** chỉ có M11, và M11 dựa trên **dịch máy có lọc QE**. Chính M11 viết rằng các bộ có phán xét người tốt (VICR, Polaris) "remain limited to English". Không bộ nào có tiếng Việt.

---

## 2. Khoảng trống và rủi ro trùng lặp cho tiếng Việt

- **Chưa thấy bộ phán xét người nào cho caption tiếng Việt.** Đã kiểm M11 (9 ngôn ngữ, không có vi), SHROOM-Visions 2026 (zh/en/fr/it, theo 02), và tìm web "Vietnamese image captioning human evaluation metric correlation", không ra kết quả nào. Đây là đóng góp dữ liệu có thể nêu là "first", với điều kiện quét lại ngay trước khi nộp.
- **Trùng lặp với JaSPICE (2023):** reviewer sẽ đọc "SPICE tiếng Việt + bộ phán xét người" là "JaSPICE cho tiếng Việt". Phần mới phải nằm ở chỗ khác: (i) mệnh đề **có kiểu, đã kiểm chứng** với quy tắc phụ thuộc kiểu DSG, (ii) dùng cho **caption chi tiết** chứ không phải câu ngắn, (iii) **P/R tách riêng** như CAPEval, (iv) **bộ kiểm thử độ bền riêng cho tiếng Việt** (§3.4).
- **Trùng lặp với PoSh (ICLR 2026):** PoSh đã dùng scene graph làm rubric cho LLM-judge, nên "scene graph + judge" không còn mới. Khác biệt cần nhấn mạnh: chạy cục bộ trên 3090, tiếng Việt, và có chế độ không dùng LLM.
- **Rủi ro vòng tròn (quan trọng nhất):** parser và verifier của metric dùng chung pipeline mệnh đề với VSPS. Như vậy metric có thể ưu ái các hệ thống huấn luyện bằng VSPS. Bắt buộc: (a) trong các ứng viên phải có hệ thống không dính VSPS, (b) báo τ **cả khi loại** đầu ra VSPS, (c) ảnh meta-eval tách hẳn khỏi ảnh dùng huấn luyện parser và chỉnh ngưỡng.

---

## 3. Giao thức đề xuất: ViGraphEval-Human (tên tạm)

### 3.1 Dữ liệu

| Thành phần | Số lượng | Ghi chú |
|---|---|---|
| Ảnh | **500**: 200 KTVIC test, 200 UIT-OpenViIC test, 100 UIT-ViIC test (miền COCO, để nối với CHAIR-vi) | Chia **dev 100 / test 400**, phân tầng theo bộ. Chỉ chỉnh ngưỡng và hyper-parameter của metric trên dev |
| Ứng viên mỗi ảnh | **5**: 3 caption chi tiết (Qwen2.5-VL-7B zero-shot, Vintern-3B, VSPS-SFT) và 2 caption ngắn (1 tham chiếu người giữ lại, 1 mô hình ngắn fine-tune UIT-ViIC/KTVIC) | Trộn ngắn và dài để tránh metric chỉ học độ dài. Cách giữ lại một tham chiếu làm ứng viên theo kiểu Flickr8k. **Cần kiểm số tham chiếu/ảnh của từng bộ** |
| Tổng caption | **2.500** (test: 2.000) | Với n = 2.000, SE của τ dưới H0 ≈ 0,015; với n = 400 (một bộ con) ≈ 0,034 (công thức Kendall chuẩn, đã tính) |
| Hệ thống cho phân tích cấp hệ thống | 8-10 (thêm Qwen3-VL-8B, Vintern-1B, bản DPO, beam vs sampling) | Chỉ chạy metric và judge, không cần thêm người. Lấy điểm người cấp hệ thống từ §3.2-B |

### 3.2 Ba loại phán xét của người

**A. Likert theo caption (chính, phục vụ τ).** Thang **1-5**, **3 người/caption**, chấm **hai trục riêng**: *Đúng (precision/faithfulness)* và *Đủ (coverage)*, cộng một điểm *Tổng thể* để so được với các bộ English. Thang này lấy từ M4, còn việc tách trục theo M8 và M9. Ảnh hiện một lần, các caption của ảnh được xáo thứ tự và giấu tên hệ thống (dùng lại cách làm của `scripts/human_eval_sample.py`). Có hướng dẫn kèm 10 ví dụ neo cho mỗi mức điểm.

**B. So sánh cặp (phụ, tránh nhiễu thang).** **600 cặp** caption chi tiết, mỗi cặp **2 người**, người thứ 3 phân xử khi hai người lệch nhau. Hỏi hai câu: "caption nào ít sai hơn" và "caption nào đủ hơn". Lý do: M5 thấy thang 1-5 cho đồng thuận thấp với caption dài. Chạy cả hai thứ tự trình bày để khử thiên vị vị trí.

**C. Gán nhãn mệnh đề (kiểm parser và metric ở cấp mệnh đề).** **200 ảnh × 2 caption chi tiết.** Người gán nhãn đánh dấu từng mệnh đề do parser trích ra là ĐÚNG / SAI / KHÔNG KIỂM ĐƯỢC, sửa các mệnh đề bị parse sai, và ghi các mệnh đề quan trọng bị thiếu so với ảnh. **100 ảnh được gán nhãn đôi.** Dùng lại `scripts/agreement.py`, vốn đã khớp mệnh đề theo nội dung chứ không theo vị trí. Phần này cho biết parser F1 và precision từng mệnh đề, tức là xác nhận *trực tiếp* metric chứ không chỉ qua tương quan.

**Người chấm:** 6 người bản ngữ (sinh viên UIT), mỗi phần giao cho 3 người. Pilot trên 50 ảnh dev. Tiền công và đạo đức: xin chấp thuận của khoa, không thu thông tin cá nhân.

### 3.3 Ngưỡng đồng thuận

| Loại | Hệ số | Ngưỡng chấp nhận | Nếu không đạt |
|---|---|---|---|
| A (Likert) | **Krippendorff α thứ bậc**, tính riêng mỗi trục | ≥ 0,67 (ngưỡng thường dùng, xem "Chưa xác minh") | Sửa hướng dẫn, chạy lại pilot. Nếu sau 2 vòng vẫn < 0,6 thì báo con số đó như một phát hiện và dựa chủ yếu vào B |
| B (cặp) | Cohen κ (2 người), kèm raw agreement | κ ≥ 0,6. Để tham khảo, M5 đạt agreement 0,782 | Bỏ cặp hoà khỏi phép tính accuracy |
| C (mệnh đề) | Cohen κ trên ba nhãn, cộng tỷ lệ mệnh đề khớp được giữa hai người | κ ≥ 0,7 | Hợp nhất nhãn KHÔNG KIỂM ĐƯỢC rồi tính lại |
| Trần người | τ_c của từng người so với trung bình các người còn lại (leave-one-out) | — | Báo cạnh τ của metric (kiểu M4) |

### 3.4 Bộ kiểm thử độ bền (tự động, 10% có người kiểm)

Xuất phát từ khoảng 1.000 caption được nhãn A chấm là đúng. Mỗi caption sinh ra nhiều biến thể có kiểu (khuôn từ M16 và FOIL), tổng khoảng **6.000 biến thể**.

| Nhóm | Biến đổi | Kỳ vọng |
|---|---|---|
| Tiêm ảo giác | thay đối tượng bằng đối tượng hay đồng xuất hiện (lấy thống kê từ KTVIC); **thêm** một mệnh đề sai vào cuối caption dài (HalDec-Bench chỉ ra vị trí cuối là nơi detector bỏ sót, theo 02) | điểm(gốc) > điểm(nhiễu); báo **accuracy** |
| Thuộc tính | đổi màu, đổi số lượng ("hai" thành "ba"), đổi giới tính | như trên |
| Quan hệ | trái↔phải, trên↔dưới, đảo vai chủ thể và đối tượng ("người dắt chó" thành "chó dắt người") | như trên. Đây là lỗi mà SPICE kiểu túi bộ ba hay bỏ qua |
| Phủ định | thêm "không" | như trên |
| Giữ nghĩa | thay từ đồng nghĩa (xe máy/xe gắn máy, ô tô/xe hơi), đổi trật tự mệnh đề, đổi loại từ (con/chiếc) | **bất biến**: \|Δ\| < ε (chọn ε trên dev), báo tỷ lệ bất biến |
| Riêng tiếng Việt | Unicode NFC↔NFD, kiểu bỏ dấu cũ/mới (hoà/hòa), tách từ (syllable so với VnCoreNLP word) | bất biến. BLEU/CIDEr gần như chắc chắn trượt nhóm này, nên đây là bằng chứng rẻ |

Người kiểm 600 biến thể (10%) để chắc rằng nhiễu thật sự đổi nghĩa, hoặc thật sự giữ nghĩa.

### 3.5 Kiểm định đa ngữ (rẻ, theo M11)

Dịch tập ứng viên và tham chiếu của Flickr8k-Expert và Composite sang tiếng Việt bằng MT, lọc bằng QE (COMETKiwi theo M11, cần kiểm xem có hỗ trợ vi không), rồi chạy metric tiếng Việt và so τ với chính metric đó chạy trên tiếng Anh. Phép thử này **không thay được** bộ người ở §3.2, vì điểm vẫn là điểm người Anh chấm cho câu Anh. Nó chỉ trả lời câu hỏi "đổi ngôn ngữ thì metric mất bao nhiêu", và cho một con số có thể đặt cạnh bảng M1.

### 3.6 Thống kê

- **Hệ số:** τ_c (chính) và τ_b, tính giữa điểm metric và **trung bình** người, ở cấp caption, cho từng trục A và cho cả bộ test. Spearman ρ để ở phụ lục. Với B thì báo **pairwise accuracy** (bỏ cặp hoà của người). Ở cấp hệ thống, báo Kendall τ trên 8-10 hệ thống (n nhỏ, ghi rõ hạn chế) và **SPA** (M17).
- **Khoảng tin cậy:** **paired bootstrap theo ảnh** (B = 10.000, seed cố định). Resample ảnh chứ không resample caption, vì 5 caption của một ảnh phụ thuộc nhau. Dùng lại khung của `scripts/score_ci.py`.
- **So hai metric:** kiểm định hoán vị/bootstrap ghép cặp cho Δτ (H1: τ_mới > τ_baseline). Hiệu chỉnh **Holm-Bonferroni** trên khoảng 8 baseline × 2 trục. Williams test cho tương quan phụ thuộc chỉ để phụ lục.
- **Độ bền:** accuracy kèm CI Wilson, chia theo nhóm nhiễu.
- **Phân tích vòng tròn:** tính lại tất cả số liệu khi loại các caption VSPS (§2).
- **Ổn định:** τ tính riêng trên từng bộ (KTVIC / OpenViIC / ViIC) và tách caption ngắn với caption chi tiết.

### 3.7 Baseline phải thắng (hoặc phải hoà khi rẻ hơn)

| Baseline | Trạng thái cho tiếng Việt | Kỳ vọng |
|---|---|---|
| BLEU-4, ROUGE-L, METEOR (khớp chính xác), CIDEr | Chạy được. Báo **cả hai cách tách** (âm tiết và từ VnCoreNLP) | Phải thắng có ý nghĩa thống kê |
| BERTScore (PhoBERT / XLM-R) | Chạy được | Phải thắng |
| "SPICE-vi" | **Không tồn tại** (11 §3.2). Dùng **SPICE-pivot**: dịch caption sang tiếng Anh rồi chạy SPICE. Có thể thêm **DiscoSG-pivot** cho caption dài | Phải thắng. Đây là đối thủ trực tiếp của metric đồ thị |
| CLIPScore đa ngữ | Mô hình fine-tune trong M11 hoặc multilingual CLIP. **Cần kiểm xem có hỗ trợ tiếng Việt không** | Phải thắng trên trục Đúng |
| CHAIR-vi và object P/R | Đã có trong repo (`coco80_vi.json` vẫn là bản nháp, `object_gold_score.py`) | Metric đồ thị phải bao được CHAIR: tương quan ít nhất ngang CHAIR trên trục Đúng, cao hơn trên trục Đủ |
| VLM-as-judge (Qwen2.5-VL-7B, prompt tiếng Việt, kiểu CapArena) | Chạy cục bộ được | **Không kém có ý nghĩa** (non-inferiority, biên Δτ = 0,03). Bán metric bằng chi phí, tính diễn giải và tính trung lập (M3) |
| Bản port PoSh-vi hoặc DCScore-vi (judge cục bộ) | Tuỳ chọn, nếu kịp | Như trên |
| MetaMetrics (tổ hợp các baseline) | Chạy được, cần train trên dev | Cận trên "rẻ" để so cho công bằng |

**Tiêu chí thành công (định trước, ghi vào kế hoạch trước khi xem test):**
(1) τ_c trên trục Đúng và trục Đủ cao hơn BLEU, CIDEr, SPICE-pivot và mCLIPScore với p < 0,05 sau hiệu chỉnh Holm.
(2) Không kém VLM-judge quá 0,03.
(3) Accuracy ≥ 90% trên nhóm tiêm ảo giác, quan hệ và thuộc tính; tỷ lệ bất biến ≥ 90% trên nhóm giữ nghĩa và nhóm riêng tiếng Việt.
(4) Kết luận (1) vẫn đứng khi loại các caption VSPS.

---

## 4. Ước tính giờ gán nhãn

Giả định thời gian: nhìn ảnh 20 giây mỗi ảnh; caption chi tiết (100-150 từ) chấm 3 trục mất khoảng 90 giây; caption ngắn khoảng 25 giây. Các con số này là **ước lượng, cần đo lại ở pilot**.

| Phần | Phép tính | Người-giờ |
|---|---|---|
| Đào tạo và pilot (6 người, 50 ảnh) | 6 × ~3 giờ | ~18 |
| A. Likert | 500 ảnh × 3 người × (20 + 3×90 + 2×25 = 340 giây) | **~142** |
| B. Cặp | 600 × 2 người × 120 giây, cộng phân xử khoảng 25% (150 × 120 giây) | ~45 |
| C. Mệnh đề | 400 caption × ~6 phút, cộng 200 caption gán nhãn đôi × 6 phút | ~60 |
| Kiểm nhiễu (10%) | 600 × 20 giây × 2 người | ~7 |
| Phân xử và QA (~10%) | — | ~25 |
| **Tổng** | | **~300 người-giờ** (khoảng 6 người × 50 giờ, tức 4-6 tuần làm bán thời gian) |

**Bản tối thiểu** nếu thiếu kinh phí: 300 ảnh × 4 ứng viên × 3 người cho phần A (khoảng 70 giờ), bỏ phần B, phần C chỉ làm 100 ảnh (khoảng 25 giờ). Cộng pilot và QA thì khoảng **110 người-giờ**. Bản này vẫn đủ τ và CI cho một bài Q2, nhưng mất phần đánh giá cấp hệ thống.

GPU: chạy toàn bộ baseline cùng metric mới trên 2.500 caption và 6.000 biến thể. VLM-judge 7B (đánh giá cặp chạy cả hai thứ tự) tốn khoảng **3-6 GPU-giờ** trên 3090. Các metric còn lại không đáng kể.

---

## 5. Thứ tự làm

1. Viết hướng dẫn chấm và ví dụ neo, sinh bảng chấm (mở rộng `human_eval_sample.py` cho 5 ứng viên và 2 trục), chạy pilot 50 ảnh, tính α. Khoảng 1 tuần.
2. Song song: viết bộ sinh nhiễu §3.4 (một script, có self-check bằng assert) và chạy baseline (§3.7).
3. Gán nhãn A, rồi C, rồi B.
4. Chốt metric trên dev, chạy test **một lần**, rồi báo bảng kiểu M1 (τ_b/τ_c theo bộ, accuracy độ bền, thời gian chạy, trần người).
5. Phát hành bộ phán xét (giấy phép tương thích với KTVIC/OpenViIC). Bản thân bộ này có thể thành một bài dataset riêng.

---

## Chưa xác minh

- Mô tả chi tiết của Flickr8k-Expert và Composite (số caption, thang điểm, số người chấm). Ở đây chỉ dùng quy ước τ_b/τ_c theo bảng M1, không trích số mô tả.
- Fu & Liu, "How Reliable is Multilingual LLM-as-a-Judge?" (Findings EMNLP 2025, Fleiss κ ≈ 0,3): lấy theo file 02, chưa mở lại trong phiên này.
- Hệ số của PoSh (+0,05 Spearman trên DOCENT) và chi tiết DCScore (400 ảnh): theo 02.
- DISCODE (được trích là AAAI 2026 trong Rigel): chưa mở.
- Mô hình CLIPScore đa ngữ của M11 và COMETKiwi có hỗ trợ tiếng Việt hay không: chưa kiểm.
- Ngưỡng Krippendorff α ≥ 0,667 và Williams test là quy ước nền (Krippendorff; Graham & Baldwin cho MT), chưa mở nguồn trong phiên.
- Số tham chiếu mỗi ảnh của UIT-OpenViIC và KTVIC: cần kiểm trước khi chốt cách giữ lại một tham chiếu.
- Mọi con số thời gian trong §4 là giả định, phải đo lại ở pilot.
- Tìm kiếm "không có bộ phán xét caption tiếng Việt" chỉ dựa trên tìm web và M11, vì các API học thuật bị giới hạn trong phiên này. Cần quét lại Semantic Scholar và OpenAlex trước khi nộp.
