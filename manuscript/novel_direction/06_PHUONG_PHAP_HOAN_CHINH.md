# Phương pháp hoàn chỉnh: Latent-Set Captioning (LSC), bản v1, 11/10/2026

Nguồn: R2_01 (mốc SOTA), R2_02 (kiến trúc), R2_03 (kiểm tra bị đi trước), R2_04 (ý tưởng tiên phong), R2_05 (ngôn ngữ học tiếng Việt), cùng các phép đo CPU hôm nay.

## 0. Những sự thật buộc phải đổi hướng (đo hôm nay, trên KTVIC)

| Hệ thống | Object P | R | F1 | Số từ |
|---|---|---|---|---|
| Zero-shot Qwen2.5-VL-7B (test) | 31,6 | 57,1 | 40,7 | 117 |
| VSPS main_s42 (test) | 41,5 | 36,7 | 39,0 | 34 |
| v2raw_s42 (test) | 38,1 | 42,2 | 40,1 | 44 |
| **P1: SFT trên caption gold (test)** | **78,3** | **42,7** | **55,3** | 12 |
| Caption của 1 người gán so với 4 người còn lại (train) | 83,7 | 46,8 | 60,1 | ~12 |

1. **P1 đã trội Pareto so với bài VSPS cũ** ở cả P lẫn R, và theo R2_01 nó còn hơn ở CIDEr (149,8) và CHAIR_i (19,2%). Bài mới phải vượt P1, không phải zero-shot.
2. **Trần của metric tham chiếu chính là con người**, khoảng F1 60 và R 47. Mục tiêu "recall 100" vô nghĩa với metric này. Recall thật chỉ đo được bằng gold đầy đủ do người gán (300 ảnh, chưa có).
3. **Sai số của metric:** `object_prf.py` khớp chính xác từ, trong khi CHAIR-vi chấp nhận từ khái quát hơn. Áp nhất quán quy tắc CHAIR-vi cho mọi hệ thống thì VSPS F1 = 47,3, zero-shot = 43,2 (R2_05). Phải báo cả hai biến thể, áp cho mọi hệ thống, và giải thích đây là sửa cho nhất quán chứ không phải đổi metric sau khi đã thấy kết quả.

## 1. Luận điểm hợp nhất

**Caption tham chiếu là các nhãn một phần (partial label) của một tập đối tượng ẩn.** Mỗi người gán sinh caption từ tập đối tượng thật S của ảnh theo ba biến ẩn cho mỗi đối tượng o:
- **eₒ (tồn tại):** o có trong ảnh không;
- **μₒ (đáng nhắc):** xác suất một người gán nhắc o, nếu o có thật;
- **ℓₒ (mức gọi tên):** người gán gọi o ở mức nào trên thang khái quát, ví dụ phụ nữ → người, xe máy → xe, "ba người" → "một vài người".

KTVIC có **5 người gán cho mỗi ảnh**, nên mô hình này *định danh được* (identifiable): số người nhắc k ~ 1[e=1]·BetaBin(5, μ). Đây là bài toán học positive-unlabelled với xác suất gán nhãn phụ thuộc đối tượng (R2_02). Ba hệ quả:

1. Với đối tượng có μ thấp, tham chiếu **không nói gì** về chuyện nó có tồn tại hay không. Muốn biết thì phải dựa vào niềm tin của chính mô hình: probe trên hidden state, gộp với logit của Vintern.
2. Caption tối ưu là tập đối tượng **tối đa hóa F1 kỳ vọng so với một người gán chưa thấy**, chọn riêng cho từng ảnh (General F-measure Maximizer), kèm một sàn trung thực eₒ ≥ τ_e. Hai mục tiêu "khớp tham chiếu" và "không ảo giác" được điều khiển bởi **hai biến khác nhau**, nên không còn phải đánh đổi qua một ngưỡng duy nhất.
3. Khi niềm tin tồn tại ở mức cụ thể còn yếu, **lùi xuống mức gọi tên khái quát hơn**, nơi niềm tin cao hơn (thang suy diễn của tiếng Việt: danh từ chính đứng đầu nên bỏ phần bên phải vẫn đúng). Cách này đổi *độ cụ thể* chứ không đổi *sự có mặt*, nên recall được giữ.

## 2. Đóng góp (đã đối chiếu với R2_03; ghi rõ cái gì còn sống)

| # | Đóng góp | Trạng thái tính mới |
|---|---|---|
| C1 | Mô hình sinh tham chiếu (e, μ, ℓ) định danh được nhờ 5 người gán; phân rã "đánh đổi" thành ảo giác, lệch độ nổi bật, lệch mức gọi tên và bỏ sót | Phép phân rã định lượng: chưa ai làm (mới có nhận xét định tính ở ALOHa, THRONE, AMBER). Phần định danh PU với nhiều người gán: **UNVERIFIED**, cần tìm kỹ thêm |
| C2 | Quy tắc quyết định theo F1 kỳ vọng cho từng ảnh, cộng sàn tồn tại | Từng phần đã có (Lipton 2014, GFM 2011); áp vào captioning với hai biến tách rời thì chưa có |
| C3 | Lùi mức gọi tên theo thang suy diễn tiếng Việt khi kiểm chứng | Chưa thấy trong captioning; gần nhất là "Hedging your bets" (Deng, CVPR 2012) cho phân loại ảnh |
| C4 | Huấn luyện một lượt: tự huấn luyện trên **các mẫu do chính mô hình sinh**, chọn theo tiện ích U (F1 kỳ vọng + CIDEr − rủi ro ảo giác), xuất phát từ P1 (văn phong người) thay vì template | Dùng nhãn probe làm mục tiêu SFT: chưa có. PatchGate (2608.21819) làm lúc giải mã; Salience-LLaVA (2608.28218) dạy độ nổi bật nhưng không có trục tồn tại. Cả hai là baseline bắt buộc |
| C5 | Tài nguyên tiếng Việt: gold 300 ảnh đầy đủ, POPE/CHAIR tiếng Việt | Chưa có cho tiếng Việt |

Đã bị đi trước, không được tuyên bố: "mô hình biết nhiều hơn nó nói" và phép đo bỏ sót (PatchGate); các đặc trưng độ nổi bật (Berg 2012); lý thuyết ROC/F*/2.

## 3. Bằng chứng ban đầu (CPU, đo hôm nay)

- **Hai trục bổ sung cho nhau.** AUROC phân biệt đúng/sai của đối tượng ứng viên, kiểm chứng chéo 5 fold theo ảnh: chỉ bằng chứng tồn tại 0,667–0,725; chỉ tiên nghiệm đáng nhắc 0,696; cả hai 0,776. Ở mức tập đối tượng: P 46,0 / R 56,7 / F1 50,8, so với SUPPORTED P 39,3 / R 50,7 / F1 44,3. Kết quả này trội cả hai chiều.
- **Chọn theo F1 kỳ vọng cho từng ảnh:** F1 51,0 (P 47,3 / R 55,4).
- **Nút thắt là bước render bằng template:** khi render, recall rơi từ 56,7 xuống 40,9. Đây là lý do C4 thay template bằng chính câu chữ của mô hình.
- **Đầu vào tốt nhất là văn phong người:** thêm đối tượng có điểm ≥ 0,5 vào caption người làm F1 60,1 → 61,4 và R 46,8 → 56,6, nhưng P 83,7 → 67,1. So với P1, đây vẫn là **đánh đổi**: F1 chỉ tăng nhẹ. Muốn tăng recall mà không mất precision thì cần trục tồn tại tốt hơn (probe) và thang gọi tên (C3), chứ một ngưỡng thì không làm được. Phải thừa nhận rõ điều này.

## 4. Thí nghiệm theo thứ tự, có cổng dừng

| Bước | Nội dung | Tài nguyên | Cổng |
|---|---|---|---|
| E1 | Đo lại Table IV với cả hai biến thể khớp (chính xác / khái quát) cho **mọi** hệ thống, gồm P1, kèm CI bootstrap | CPU | Cả hai biến thể đều được báo cáo |
| E2 | Probe trên token thị giác của Qwen-7B: AUROC tồn tại so với Vintern, trên 500 ảnh train (nhãn tham chiếu, có hiệu chỉnh PU) | khoảng 2 GPU-giờ | Probe > Vintern với ΔAUROC ≥ 0,03; nếu không, bỏ phần probe |
| E3 | Thang gọi tên: cận trên trên CPU, sau đó hỏi lại Vintern bằng logit ở mức khái quát | khoảng 1 GPU-giờ | Lấy lại ≥ 3 điểm R ở mức mệnh đề, P giảm không quá 1 |
| E4 | Mô hình μ (beta-binomial, bỏ ra 1 người gán để kiểm định) cộng quy tắc GFM, đánh giá offline | CPU | F1 offline ≥ F1 của ngưỡng cố định + 1,5 |
| E5 | Tự huấn luyện 2 vòng từ P1 với tiện ích U, QLoRA lớp trên | khoảng 8 GPU-giờ mỗi seed | Trên test: F1 > 55,3 (P1), CIDEr ≥ 136 (GRIT), CHAIR_i ≤ 19,2 |
| E6 | Gold 300 ảnh: phân rã C1, P/R đầy đủ, kiểm định kép (R tăng, P giảm không quá 1) so với P1 | **cần người gán** | Đây là bảng chính của bài |

Các baseline bắt buộc: P1, PatchGate, gán tag kiểu RAM++ hoặc Grounding DINO vào prompt, Salience-LLaVA (nếu có code), cùng hai ablation chỉ dùng một trục.

## 5. Rủi ro

- PatchGate có thể đã xuất bản trước khi bài này được nộp, nên phần probe chỉ là thành phần, không làm luận điểm chính.
- Gold 300 ảnh là đường găng: không có nó thì không có C1 và không có tuyên bố về recall.
- Metric tham chiếu bão hòa ở khoảng F1 60, nên phần lợi trên metric này nhỏ. Bài phải được bán bằng gold đầy đủ, phép phân rã và CIDEr, không phải chỉ bằng F1 tham chiếu.

## 6. Kết quả các cổng (cập nhật 11/10/2026)

**E1 (đạt).** Bảng đầy đủ ở `data/results/object_prf_dual.md` (`scripts/object_prf.py --ci`). P1 đứng trên mọi hệ thống ở cả ba quy tắc, CI không chồng lấn: F1 55,3 / 55,0 / 58,6. Theo quy tắc khớp chính xác, VSPS và zero-shot ngang nhau (CI chồng lấn). Theo R_vague, VSPS hơn zero-shot (47,3 so với 43,1, CI tách rời). R_spec trả lại thứ tự cũ, nên khác biệt nằm ở mức gọi tên chứ không ở nội dung.

**E4 (trượt, bỏ C2 khỏi danh sách đóng góp).** Chạy `e4_mention_gfm.py` trên 3.700 ảnh train, CV 5 fold theo ảnh:
- Mô hình đếm binomial (k/5 người nhắc) cho AUROC 0,7766, so với 0,7764 khi dùng nhãn gộp. Số người nhắc không thêm thông tin xếp hạng.
- GFM trên gold gộp đạt F1 51,0, so với ngưỡng cố định tốt nhất khoảng 50,8, tức +0,2. Với một người gán giữ lại, GFM trên q đạt 37,2 so với 36,6 của ngưỡng tốt nhất, tức +0,6.
- Cả hai đều dưới cổng +1,5.

Kết luận: quy tắc quyết định không phải đòn bẩy. Nút thắt là chất lượng điểm tồn tại (E2) và bước render (C4/E5). GFM chỉ còn là chi tiết cài đặt.

**E3, cận trên CPU (trượt, ngay cả ở mức oracle; hạ C3 thành phân tích).** Chạy `e3_ladder_bound.py` trên 3.700 ảnh train, đo theo đối tượng và gold gộp:

| tập đối tượng | P | R | F1 | P_h | số đối tượng/ảnh |
|---|---|---|---|---|---|
| SUPPORTED | 39,3 | 50,5 | 44,2 | 44,2 | 4,45 |
| + bậc lùi oracle (hypernym + cắt danh ngữ ghép), chỉ khi bậc đó có trong gold | 39,9 | **52,1** | 45,2 | 44,7 | 4,50 |
| + luôn lùi 1 bậc, không kiểm chứng | 34,8 | 52,1 | 41,7 | 40,8 | 5,17 |
| + mọi đối tượng không SUPPORTED (không verifier) | 30,0 | 67,9 | 41,6 | 33,0 | 7,95 |

- Oracle chỉ cứu được 1.708 trong 10.394 đối tượng sai mức hoặc vắng, và chỉ thêm 1,6 điểm R. Lý do: bậc lùi gần như luôn gom về `người` hoặc `xe`, vốn đã nằm sẵn trong tập.
- Trong khi đó, **2.308 đối tượng không SUPPORTED đã đúng ngay ở mức cụ thể**. Đây là phần verifier bỏ phí, và là nơi duy nhất còn khoảng R lớn (50,5 → 67,9).

Hệ quả: đòn bẩy còn lại là **chất lượng trục tồn tại** (E2: probe so với Vintern) và **văn phong đầu ra** (E5). C3 chỉ còn là phân tích đo lường (R_vague, E1), không còn là cơ chế.

**Hướng mới: mục tiêu SFT ghép từ nhiều caption người** (`build_gold_sft.py --select consensus --fuse 2`, xem kiểm tra tính mới ở R3_01). Ước lượng offline không rò nhãn: chọn 3 trong 5 caption để dựng mục tiêu, đo với 2 caption còn lại, trung bình qua 10 cách chia.

| mục tiêu | P | R | F1 |
|---|---|---|---|
| caption đầu tiên (P1) | 71,8 | 52,5 | 60,7 |
| caption đồng thuận | 71,1 | 56,6 | 63,0 |
| ghép 2 caption ngẫu nhiên | 64,5 | 67,9 | 66,1 |
| đồng thuận + ghép tham lam (của bài) | 63,0 | 73,6 | 67,9 |
| ghép cả 3 | 61,2 | 76,7 | 68,1 |

Phần lớn mức tăng đến từ việc *ghép*. Chọn tham lam chỉ thêm +1,8 F1 so với ghép ngẫu nhiên, nên phải báo cáo trung thực đúng như vậy. Mô hình fuse2_s42 đang chờ GPU.

**E2 (đạt, vượt xa cổng).** `scripts/probe_existence.py`: 497 ảnh train, 4.046 câu hỏi "Trong ảnh có X không?", CV 5 fold theo ảnh. Nhãn là "có người gán nào nhắc X không", nên AUROC đo **tồn tại × đáng nhắc**, chưa phải tồn tại thuần.

| tín hiệu | AUROC |
|---|---|
| Vintern K=5 (tỉ lệ phiếu "có") | 0,612 |
| tiên nghiệm lớp (out-of-fold) | 0,710 |
| Qwen P(có): có ảnh / không ảnh | 0,709 / 0,453 |
| probe layer 8 / 16 / 20 / **24** / 28, có ảnh | 0,714 / 0,765 / 0,790 / **0,807** / 0,801 |
| probe, không ảnh (đối chứng rò tiên nghiệm) | 0,708 ở mọi layer |
| Vintern + tiên nghiệm | 0,743 |
| probe L24 + Vintern + tiên nghiệm | **0,817** |

- Probe hơn Vintern +0,195; cổng chỉ đòi ≥ 0,03. Bỏ ảnh đi thì probe chỉ còn bằng tiên nghiệm lớp, nên phần thông tin tăng thêm đến từ ảnh.
- Thông tin về tồn tại nằm ở các layer giữa và sau (20–28), không ở đầu ra. P(có) ở đầu ra chỉ đạt 0,709.

Tập đối tượng trên cùng 497 ảnh, đo với gold gộp (`e2_probe_sets.py`):

| tập | P | R | F1 | số đối tượng/ảnh |
|---|---|---|---|---|
| SUPPORTED (record gốc) | 47,9 | 32,6 | 38,8 | 2,92 |
| Vintern + tiên nghiệm ≥ 0,50 | 59,8 | 30,9 | 40,8 | 2,31 |
| Vintern + tiên nghiệm ≥ 0,30 | 50,2 | 53,6 | 51,9 | 4,69 |
| **probe + V + tiên nghiệm ≥ 0,45** | **66,0** | **43,9** | 52,7 | 2,91 |
| probe + V + tiên nghiệm ≥ 0,30 | 59,0 | 52,3 | **55,5** | 3,92 |

Với cùng số đối tượng mỗi ảnh như SUPPORTED, P tăng +18,1 và R tăng +11,3. Đây là kết quả "không đánh đổi" đầu tiên đo được trên cùng một tập ứng viên. Bước tiếp theo:
1. Dùng điểm probe để chọn nội dung cho mục tiêu SFT, thay cho Vintern.
2. Kiểm định trên gold 300 ảnh để tách phần tồn tại khỏi phần đáng nhắc.

**fuse2_s42 trên test (12/10/2026, 1 seed; s43/s44 đang trong hàng đợi).** Object P/R/F1 khớp chính xác, CI bootstrap 95%; CIDEr/CHAIR_i theo bootstrap ghép cặp so với P1 (`data/results/score_ci/score_ci_fuse2_s42-vs-p1-*.json`).

| mode | hệ | số từ | P | R | F1 [CI] | CIDEr [CI] | CHAIR_i |
|---|---|---|---|---|---|---|---|
| short | P1 | 12,0 | 77,9 | 41,4 | 54,1 [51,8; 56,4] | 149,8 [140,9; 159,1] | 19,2 |
| short | fuse2 | 12,4 | 75,7 | **47,1** | **58,1** [56,0; 60,3] | 143,9 [135,4; 152,7] (Δ −5,9, p = 0,11) | 21,9 (Δ +2,8, p = 0,03) |
| detailed | P1 | 12,2 | 78,3 | 42,7 | 55,3 [53,0; 57,5] | 146,2 | 19,5 |
| detailed | fuse2 | 24,0 | 68,0 | **61,2** | **64,4** [62,4; 66,3] | 23,9 | 29,0 |

- Short, cùng độ dài: R +5,7, P −2,2, F1 +4,0, CIDEr không khác có ý nghĩa. Đây vẫn là đánh đổi nhỏ, chưa phải "không đánh đổi".
- Detailed: R +18,5, F1 +9,1 (CI tách rời), nhưng P −10,3 và CHAIR_i +9,5. CIDEr thấp vì caption dài gấp đôi tham chiếu một câu, nên không so CIDEr ở mode này.
- Bước tiếp: E5 và đối chứng `ctrl_fuse2plus1` (đang chạy) xem có lấy lại P mà giữ R không.

**E5 vòng 1, SFT (12/10/2026): kết quả rỗng.** Lấy 6 mẫu cho mỗi ảnh trên 1.500 ảnh train từ fuse2_s42, chọn mẫu theo U (λ = 0,1; τ = 0,2), rồi SFT tiếp 1 epoch trên 1.458 mẫu được chọn cộng gold_fuse2.

| hệ | mode | P | R | F1 [CI] | CIDEr | CHAIR_i |
|---|---|---|---|---|---|---|
| fuse2_s42 | short | 75,7 | 47,1 | 58,1 [56,0; 60,3] | 143,9 | 21,9 |
| e5_s42 | short | 75,0 | 46,3 | 57,3 [55,1; 59,6] | 137,9 | 22,5 |
| fuse2_s42 | detailed | 68,0 | 61,2 | 64,4 [62,4; 66,3] | | 29,0 |
| e5_s42 | detailed | 67,2 | 62,2 | 64,6 [62,6; 66,6] | | |

- Trên train, mẫu được chọn rất tốt (P 84,7 / R 79,4, so với 64,3 / 62,5 của mẫu ngẫu nhiên), nhưng mức này không chuyển sang được test. Lý do khả dĩ nhất: fuse2 đã học chính các ảnh này, nên mẫu "tốt nhất" chủ yếu là caption tham chiếu mô hình nhớ lại.
- Hình phạt dựa trên probe gần như không đổi được lựa chọn (P +1,0, R −0,8 so với λ = 0), vì probe học nhãn "có người nhắc".
- Muốn RFT có ý nghĩa thì phải lấy mẫu trên ảnh mô hình chưa thấy (cross-fit 2 nửa train), hoặc dùng ảnh không nhãn. Đã bỏ đối chứng `ctrl_fuse2plus1`; vẫn giữ DPO (22) để xem cặp tốt/xấu có lấy lại được P không.

**P giảm ở fuse2 detailed: ảo giác thật hay gold tham chiếu thiếu? (12/10/2026, gold AI-silver, KHÔNG phải gold người).** `scripts/silver_precision.py --allow-ai`. Gold thứ hai là `data/object_gold/annot_claude.json`: Claude (annotator `claude_AI`) tick toàn bộ đối tượng nhìn thấy trên **300 ảnh test KTVIC** (mẫu phân tầng `sample.json`, seed 42, 101 lớp checkbox; trung bình 7,17 lớp/ảnh so với 3,66 của hợp 5 caption tham chiếu). Mention và cả hai gold đều gộp về cùng 101 lớp, khớp chính xác, CI 95% bootstrap theo ảnh. "Cứu" = tỉ lệ mention sai theo tham chiếu mà AI-silver đánh dấu có mặt.

| hệ | mode | đối tượng/ảnh | P (a) tham chiếu | P (b) AI-silver | P (c) hợp a∪b | cứu |
|---|---|---|---|---|---|---|
| P1 | short | 1,81 | 77,2 [73,4; 81,0] | 69,3 | 89,2 [86,2; 91,6] | 52,4 |
| fuse2_s42 | short | 2,12 | 76,6 [72,9; 80,0] | 70,3 | 89,0 [86,2; 91,4] | 53,0 |
| e5_s42 | short | 2,07 | 75,1 | 70,3 | 88,1 | 52,3 |
| P1 | detailed | 1,84 | 76,9 [73,4; 80,6] | 69,1 [65,0; 73,2] | 88,8 [85,9; 91,6] | 51,6 |
| fuse2_s42 | detailed | 3,18 | 68,8 [65,5; 71,9] | 69,6 [66,0; 72,9] | 86,4 [83,5; 88,9] | 56,2 [49,6; 62,7] |
| e5_s42 | detailed | 3,28 | 66,7 | 68,9 | 84,7 | 54,1 |
| zero-shot | detailed | 6,43 | 33,7 | 54,4 | 62,3 | 43,2 |
| main_s42 (VSPS) | detailed | 3,15 | 42,1 | 64,0 | 73,9 | 54,8 |

ΔP ghép cặp fuse2 − P1 (detailed): tham chiếu −8,0 [−11,4; −4,6]; AI-silver +0,5 [−2,6; +3,6]; hợp −2,4 [−4,8; −0,2]. e5 − P1: −10,1 / −0,2 / −4,0 [−6,5; −1,5]. Short: mọi Δ chứa 0.

- Theo AI-silver, phần lớn mức "mất P" của fuse2 detailed là đối tượng có thật mà 5 caption không nhắc: khoảng 56% mention sai theo tham chiếu được AI-silver xác nhận, và khoảng cách với P1 co từ −8,0 xuống −2,4 điểm dưới gold hợp. Phần còn lại (~2–4 điểm) vẫn tách khỏi 0, nên có một phần ảo giác thật, nhỏ.
- Cùng hiện tượng nhưng mạnh hơn ở zero-shot và VSPS: P tham chiếu 33,7 / 42,1 nhưng hợp 62,3 / 73,9. Nghĩa là P theo tham chiếu phạt nặng caption dài vì gold không đầy đủ, không riêng gì fuse2.
- Giới hạn: (1) đây là nhãn của một mô hình AI, không phải người; annotator có thể chia sẻ thiên lệch với VLM sinh caption (nhìn thấy cùng thứ "thường có" trong ảnh), nên "cứu" là cận trên của tỉ lệ đối tượng có thật. (2) AI-silver cũng bỏ sót: P1 chỉ đạt 69,1 theo AI-silver, thấp hơn 76,9 theo tham chiếu. (3) n = 300, một annotator, không có độ đồng thuận; mẫu phân tầng theo số đối tượng tham chiếu nên P (a) lệch nhẹ so với số trên toàn test (76,9 so với 78,3; 68,8 so với 68,0). Kết luận chỉ chắc khi có gold người 2 annotator (B1).

**E5 vòng 1, DPO (12/10/2026): gần như không có tác dụng.** DPO chạy từ e5_s42 trên 1.327 cặp tốt nhất/tệ nhất (lr 5e-6).

| hệ | mode | P | R | F1 [CI] | CIDEr | CHAIR_i |
|---|---|---|---|---|---|---|
| e5_s42 | detailed | 67,2 | 62,2 | 64,6 [62,6; 66,6] | 19,0 | 29,9 |
| e5dpo_s42 | detailed | 69,3 | 60,8 | 64,8 [62,8; 66,7] | 18,0 | 26,6 |
| e5_s42 | short | 75,0 | 46,3 | 57,3 | 137,9 | 22,5 |
| e5dpo_s42 | short | 73,1 | 43,9 | 54,8 | 123,1 | 23,0 |

- Ở detailed: P +2,1, CHAIR_i −3,3, R −1,4. Đây là đánh đổi nhỏ, F1 không đổi.
- Ở short: cả F1 lẫn CIDEr đều giảm, tức DPO làm hỏng văn phong ngắn vì các cặp đều sinh từ prompt detailed.
- Không đưa vào hệ chính. Chờ cross-fit (60–63).
