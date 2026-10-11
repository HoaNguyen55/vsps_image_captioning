# Đề xuất hướng mới: Nhân chứng đa ngôn ngữ (Cross-Lingual Witnesses, XWit)

*Bản nháp v0, 11/10/2026. Cần phản biện và kiểm tra tính mới trước khi dùng.*

## 1. Luận điểm khoa học (không ghép phương pháp có sẵn)

**Sự đánh đổi precision ↔ recall trong captioning trung thực không phải là thuộc tính của mô hình, mà là của điểm vận hành (operating point) trên một đường ROC cố định.** Hầu hết các phương pháp "giảm ảo giác" (xóa hậu kiểm, DPO thuần precision, giải mã thận trọng) chỉ dịch điểm vận hành dọc theo đường ROC hiện có. VSPS v1/v2 cũng vậy, nên cứ lấy được precision thì phải mất recall. Chỉ một **nguồn bằng chứng mới có sai số không tương quan** với bằng chứng cũ mới đẩy được cả đường ROC lên trên. Khi đó, tồn tại một điểm vận hành mà precision không thấp hơn VSPS cũ còn recall cao hơn hẳn: đây là "không đánh đổi" theo đúng nghĩa (lập luận Neyman–Pearson).

**Giả thuyết về nguồn bằng chứng đó:** ảo giác của VLM có hai gốc.
- **Gốc tri giác**: vision encoder thấy sai. Lỗi này *giống nhau* dù hỏi bằng ngôn ngữ nào.
- **Gốc tiên nghiệm ngôn ngữ**: mô hình ngôn ngữ "đoán" đối tượng hay đi kèm, ví dụ có bàn ăn thì sinh ra "dĩa". Đồng xuất hiện trong văn bản tiếng Việt, tiếng Anh và tiếng Trung khác nhau, nên lỗi gốc này *ít tương quan giữa các ngôn ngữ*.

Một đối tượng thật thì bất biến theo ngôn ngữ. Vì thế, nếu một đối tượng được nhắc độc lập khi mô tả cùng một ảnh bằng tiếng Việt, tiếng Anh và tiếng Trung (mỗi ngôn ngữ là một "nhân chứng"), thì đó là bằng chứng thị giác; còn nếu chỉ một ngôn ngữ nhắc tới, nhiều khả năng đó là tiên nghiệm ngôn ngữ.

Hệ quả cho tiếng Việt, một ngôn ngữ ít tài nguyên:
- **mượn recall** từ ngôn ngữ mạnh: VLM mô tả bằng tiếng Anh đầy đủ hơn (Hinck et al. 2024);
- **mượn precision** từ sự đồng thuận;
- giữ đầu ra bằng tiếng Việt tự nhiên.

## 2. Đóng góp dự kiến

1. **Phép đo mới: tương quan ảo giác giữa các ngôn ngữ (ρ).** Cùng một ảnh, cùng một mô hình, mô tả bằng L ngôn ngữ, quy đối tượng về một lexicon chung. Nếu ρ thấp, phần lớn ảo giác là ngôn ngữ; nếu ρ cao, chúng là tri giác. Từ đó tách được ảo giác theo gốc **tri giác / ngôn ngữ** mà không cần nhãn. Theo những gì đã biết, chưa có bài nào đo được việc này (cần kiểm tra lại). Kết quả nào cũng là một phát hiện có giá trị.
2. **Lý thuyết điểm vận hành.** Một mệnh đề ngắn chứng minh rằng: nếu điểm số mới có ROC trội hơn điểm số cũ, thì tại điểm vận hành Neyman–Pearson với ràng buộc precision ≥ p₀ (p₀ là precision của VSPS cũ), recall mới ≥ recall cũ. Kèm theo đó là quy tắc chọn ngưỡng tối ưu F1 (ngưỡng tối ưu bằng F*/2, Lipton et al. 2014), giải thích *vì sao* các verifier gắt luôn thua zero-shot về F1.
3. **Phương pháp XWit**: điểm tồn tại của đối tượng = f(số nhân chứng ngôn ngữ, logit của verifier Vintern, tiên nghiệm đồng xuất hiện theo từng ngôn ngữ). Có thể học f trên tập dev; chỉ cần một hồi quy logistic nhỏ.
4. **Chưng cất về một mô hình**: dữ liệu mục tiêu được dựng tại điểm vận hành đã chọn. Mô hình SFT tiếng Việt một lượt chạy tại thời điểm suy luận không cần sinh đa ngôn ngữ.
5. **Tiếng Việt**: benchmark POPE/CHAIR tiếng Việt dựng từ gold 300 ảnh do người gán.

## 3. Giả thuyết có thể bác bỏ, kèm cổng dừng

| ID | Giả thuyết | Cách đo | Bác bỏ nếu |
|---|---|---|---|
| H1 | Ảo giác ít tương quan giữa các ngôn ngữ hơn giữa các mẫu cùng ngôn ngữ | So ρ_cross-lingual với ρ_within (K mẫu cùng ngôn ngữ), trên 558 ảnh test | ρ_cross ≥ ρ_within |
| H2 | Số nhân chứng ngôn ngữ phân biệt đúng/sai tốt hơn K=5 cùng ngôn ngữ | AUROC mức đối tượng so với gold | AUROC tăng không quá 0,02 |
| H3 | Gộp nhân chứng với verifier thì ROC trội hơn verifier đơn lẻ | ROC trên dev, có CI bootstrap | Không trội ở dải precision của VSPS |
| H4 | Mô hình chưng cất giữ được ưu thế: P ≥ VSPS cũ, R > VSPS cũ, F1 > zero-shot | KTVIC test, 3 seed, kiểm định kép | Một trong ba điều kiện thất bại |

**Exp-0** (khoảng 1–2 GPU-giờ, chạy được ngay khi GPU rảnh): Qwen2.5-VL-7B mô tả 558 ảnh test bằng vi/en/zh, mỗi ngôn ngữ thêm K=3 mẫu, rồi đo H1 và H2. Nếu H1 hoặc H2 bị bác bỏ thì dừng hướng này, và vẫn giữ được phép đo ρ như một phát hiện.

## 4. Rủi ro đã biết

- Ánh xạ đối tượng giữa các ngôn ngữ: lexicon 113 lớp phải dịch tay sang en/zh, nhất quán. Đây là nguồn sai số lớn nhất.
- Các ngôn ngữ chia sẻ cùng một LM Qwen, nên tiên nghiệm có thể tương quan cao. Chính H1 kiểm tra điều này.
- Recall bị chặn bởi ngôn ngữ mạnh nhất: thứ mà không ngôn ngữ nào thấy thì vẫn mất.
- Tiếng Trung chưa chắc là nhân chứng độc lập. Có thể thay bằng ngôn ngữ khác hoặc bằng prompt diễn đạt khác.
