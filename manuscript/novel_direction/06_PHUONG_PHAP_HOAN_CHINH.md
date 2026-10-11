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
