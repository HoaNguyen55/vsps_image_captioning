# Tổng hợp và xếp hạng hướng mới (11/10/2026)

Nguồn: 00 (đề xuất XWit), 01 và 02 (kiểm tra tính mới), 03 (phản biện kiểu reviewer Q1), 04 (ba hướng thay thế độc lập).

## 1. Kết luận về XWit (nhân chứng đa ngôn ngữ): hạ xuống, không làm hướng chính

- Phần lý thuyết điểm vận hành **đã có người làm** (Davis & Goadrich 2006; Lipton 2014). Chỉ giữ được như một khung phân tích dài nửa trang.
- "Bất đồng giữa các ngôn ngữ báo hiệu ảo giác" đã có ở MHR (TOMM 2026) và Rowen-CL. Hàm điểm gộp có cấu trúc giống HaloProbe (ICML 2026).
- Cách diễn giải "tri giác hay tiên nghiệm ngôn ngữ" không xác định được: ba ngôn ngữ dùng chung LM của Qwen, có nút cổ chai tiếng Anh, và yếu tố ngôn ngữ bị lẫn với độ đa dạng prompt và độ dài caption.
- Phần mới còn lại là phép đo ρ. Nó có thể là một thí nghiệm phụ, có đối chứng diễn đạt lại bằng tiếng Việt và ảnh xám.

## 2. Hướng chính đề xuất: "Nói điều mình biết, và điều đáng nói" (Know-and-Mention)

**Luận điểm.** Bài toán chọn nội dung caption có **hai trục độc lập**, mà mọi hệ thống trước đây đều gộp lại làm một:
1. **Tồn tại**: đối tượng có trong ảnh không?
2. **Đáng nhắc**: người Việt mô tả ảnh này có buồn nhắc đối tượng đó không?

Sự đánh đổi precision ↔ recall phát sinh vì cả hai trục bị quyết định bằng một ngưỡng duy nhất. VSPS cũ còn tệ hơn: trục tồn tại được giao cho một trọng tài **yếu hơn** (Vintern-1B) thay vì lấy niềm tin nội tại của chính mô hình 7B.

**Bằng chứng ban đầu, đo hôm nay** trên 3.700 ảnh train, 13.031 đối tượng gold:

| Số người gán nhắc (/5) | n | Recall của tập SUPPORTED | Recall của tập đề xuất |
|---|---|---|---|
| 1 | 4.967 (38%) | 42,3 | 62,5 |
| 2 | 3.229 | 49,6 | 68,8 |
| 3 | 2.026 | 52,9 | 71,2 |
| 4 | 1.259 | 55,7 | 73,3 |
| 5 | 1.550 | 57,2 | 72,3 |

38% "gold" là những đối tượng chỉ 1/5 người nhắc. Recall đang phạt nặng nhất ở chính nhóm có độ nổi bật thấp này. Ngoài ra, khoảng cách giữa tập đề xuất và tập SUPPORTED vẫn ổn định ở 15–20 điểm bất kể độ nổi bật, tức là verifier đang loại cả những đối tượng nổi bật nhất. Đây là dấu hiệu của lỗi ở trục tồn tại.

**Ba đóng góp, không ghép từ bài khác:**
1. **Phép phân rã mới**, trên gold 300 ảnh do người gán.
   - Dương tính giả của zero-shot chia thành (i) vắng thật, tức ảo giác, và (ii) có thật nhưng không ai nhắc, tức lệch độ nổi bật.
   - Âm tính giả của VSPS chia thành (iii) mô hình *biết* nhưng không nói, hoặc verifier phủ quyết, và (iv) không bao giờ được đề xuất.

   Con số tiêu đề sẽ là: bao nhiêu phần của "sự đánh đổi" thực ra không phải ảo giác.
2. **Trục tồn tại lấy từ niềm tin nội tại**: một linear probe trên hidden state của chính Qwen2.5-VL-7B thay cho Vintern-1B. Bài 2508.04567 cho thấy probe đạt khoảng 95% trong khi sinh văn bản chỉ khoảng 81%; họ sửa LM head, còn chưa ai dùng probe làm *mục tiêu* SFT. Phải có đối chứng chống rò tiên nghiệm: probe chỉ trên token thị giác, và ảnh đã xóa đối tượng.
3. **Trục đáng nhắc học từ 5 người gán của KTVIC**: hồi quy theo diện tích, độ trung tâm, tiên nghiệm lớp và thứ tự nhắc đầu tiên. Dữ liệu mục tiêu SFT xếp hạng theo P(tồn tại) × P(đáng nhắc). Berg et al. (CVPR 2012) từng dự đoán độ quan trọng của đối tượng, nhưng chưa ai dùng nó để giám sát VLM hay để giải thích sự đánh đổi.

**Vì sao về cơ chế không có đánh đổi.** Tách hai trục thì một đối tượng nổi bật, có thật vẫn được giữ dù Vintern trả lời UNCERTAIN, nên recall tăng. Một đối tượng có thật nhưng không ai nhắc thì bị bỏ mà không cần verifier, nên precision so với tham chiếu tăng. Gold 300 ảnh do người gán cho phép đo riêng ảo giác thật, nhờ đó tránh được lời buộc tội "chỉnh mô hình theo metric".

**Giả thuyết và cổng dừng:**
- **H-A1:** ít nhất 40% dương tính giả của zero-shot thuộc lớp (ii). Bác bỏ nếu dưới 25%.
- **H-B1:** probe có AUROC tồn tại cao hơn Vintern.
- **H-B2:** ít nhất 30% âm tính giả của zero-shot có xác suất từ probe ≥ 0,7.
- **H-A3/H-B3:** mô hình SFT đạt P ≥ 41,5 và R ≥ 45 trên 3 seed.

## 3. Xếp hạng cuối

| # | Hướng | Mới | Khả thi | Pareto | Ghi chú |
|---|---|---|---|---|---|
| 1 | **Know-and-Mention** (gộp A và B của 04 thành một luận điểm) | cao | cao | cao | Cần gold 300 ảnh do người gán |
| 2 | Chỉ khoảng cách "biết mà không nói" (B) | trung bình | cao | trung bình | Phải đặt cạnh 2508.04567 |
| 3 | XWit | thấp đến trung bình | trung bình | chưa rõ | Nhiều yếu tố gây nhiễu |
| 4 | Hedging tiếng Việt (C) | trung bình | cao | thấp | Metric tính câu rào đón là một lần nhắc |

## 4. Phụ thuộc then chốt

Phép phân rã (đóng góp 1) và mọi kết luận "không đánh đổi" đều cần gold 300 ảnh do người gán (`data/object_gold/annotate.html`), mà hiện **chưa có ảnh nào được gán nhãn**. Phần đo được không cần gold: AUROC của probe so với tham chiếu, mô hình đáng nhắc, và đường cong P/R so với tham chiếu. Phần này chạy được ngay khi GPU rảnh (khoảng 2 GPU-giờ).
