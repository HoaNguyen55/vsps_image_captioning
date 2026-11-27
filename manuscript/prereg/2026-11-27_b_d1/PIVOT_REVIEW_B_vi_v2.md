# Bài B: hướng đi nếu thử nghiệm về vị trí dấu thanh không cho kết quả rõ

*Ghi chú viết trước kết quả, ngày 27/11/2026. Tôi chỉ gửi ghi chú này cho anh khi thử nghiệm đã chạy xong mà kết quả không đạt ngưỡng. Nếu kết quả đạt ngưỡng, tôi sẽ báo anh theo cách khác.*

## Mục đích

Ghi chú này đề nghị anh chọn hướng đi cho bài B trong trường hợp bài mất phần đóng góp mới cuối cùng. Các lựa chọn đều lấy từ đề cương v18.65, tức là câu hỏi nghiên cứu 9 thuộc Mục tiêu 3.3. Mỗi lựa chọn có kèm khuyến nghị của tôi và một phương án mặc định.

## Vì sao cần chọn lại

Bài B trả lời câu hỏi nghiên cứu 9 của đề cương: điểm đánh giá và thứ hạng của các hệ thống chú thích ảnh tiếng Việt có còn ổn định khi đổi cách tiền xử lý văn bản hay không.

Bài của Lu và cộng sự (arXiv 2611.04099, bản 1 ngày 3/11/2026) công bố trước ngày bài B đăng ký trước (12/11/2026). Bài này đã có trong danh sách đọc của bài A từ ngày 5/11, nhưng đến ngày 27/11 mới được đối chiếu với bài B. Cách đọc chính của họ lấy trung bình kết quả trên các cách chấm đã khai báo. Bên cạnh đó, họ báo cáo một quy tắc có cùng dạng với quy tắc quyết định của bài B: hai hệ thống bị coi là hòa nếu có bất kỳ cách chấm nào trong danh sách cho kết quả hòa, nên kết luận "hệ thống A tốt hơn hệ thống B" chỉ được giữ khi nó đúng dưới mọi cách chấm. Họ đo quy tắc này trên dịch máy, với danh sách các hàm chấm điểm; cách tách văn bản thành đơn vị từ là một trục khác mà họ cũng đo.

Cách tách từ tiếng Việt cũng là một kiểu tách văn bản thành đơn vị, nên không thể coi là phần mới so với bài của Lu. Phần chỉ bài B có là vị trí dấu thanh trong các vần oa, oe, uy, ví dụ "hòa" và "hoà".

## Thử nghiệm sẽ trả lời gì

Thử nghiệm bắt đầu với một danh sách cách chấm đã gồm ba hàm chấm điểm, ba cách tách từ, ba cách xử lý dấu câu và hai cách xử lý chữ hoa. Sau đó tôi thêm hai cách đặt dấu thanh vào danh sách, rồi đếm xem có bao nhiêu kết luận "A tốt hơn B" không còn giữ được.

Ngưỡng là 5%. Con số này đã được cố định trong bản đăng ký trước của bài B ngày 12/11, trước khi có bất kỳ kết quả nào. Tuy vậy, quyết định dùng lại con số này cho thử nghiệm mới được đưa ra ngày 27/11, sau khi một số kết quả liên quan đã được in; bản đăng ký ghi rõ điều đó. Ngưỡng 5% làm cho kết quả "vượt ngưỡng" khó đạt hơn so với ngưỡng cũ (0,5% đến 1%) đã bị bỏ.

Thử nghiệm chỉ dùng các tệp chú thích đã có. Tôi không sinh chú thích mới và không dùng tập kiểm tra nào chưa từng dùng. Khối lượng tính toán khoảng 4,5 giờ CPU, chạy trên máy thuê sau khi máy của bài C đã được thanh toán.

## Các lựa chọn nếu kết quả không vượt 5% hoặc không đủ bằng chứng

1. **Gửi bài B với phạm vi hiện tại và ghi rõ kết quả âm tính.** Tóm tắt và phần đóng góp sẽ nói rằng, trên dữ liệu này, vị trí dấu thanh không làm đổi kết luận nào đáng kể so với một danh sách cách chấm thông thường.
   - Bài vẫn giữ các phần sau: danh sách cách tiền xử lý dành cho chú thích tiếng Việt, phép kiểm tra với một công cụ tách từ để riêng, bảng tái lập điểm đã công bố của hai hệ thống gốc, và phép so sánh trực tiếp với cách làm của Lu và cộng sự.
   - Theo thang chấm nội bộ, bài B hiện đạt khoảng 62 điểm. Mức trung bình của năm bài LRE đã đọc là khoảng 66 điểm.
   - Đề cương đã ghi sẵn hai tạp chí dự phòng: VJCS (12/2027) và IEICE (07/2028).
2. **Hướng N1: chuẩn hóa dạng từ.** Hướng này đo xem phần cải thiện điểm còn lại bao nhiêu sau khi đưa các cách viết khác nhau của cùng một ý về một dạng chung.
   - Hướng này vẫn thuộc câu hỏi nghiên cứu 9 và chỉ cần CPU, khoảng ba ngày công.
   - Tuy vậy, vòng tìm tài liệu ngày 26/11 cho rằng hướng này khó nâng bài B lên mức 90. Mức thực tế ước lượng là 76–80 điểm.
3. **Một trong hai hướng mở rộng của Mục tiêu 3.3 trong đề cương:** (a) mô hình ngôn ngữ lớn đa phương thức ghi đúng dấu thanh đến mức nào khi đọc chữ tiếng Việt trong ảnh; (b) mức chênh lệch ảo giác giữa tiếng Việt và tiếng Anh.
   - Theo đề cương, hai hướng này chỉ được làm khi thử nghiệm sơ bộ đạt ngưỡng đã cố định trong bản đăng ký trước.
   - Cả hai đều là nghiên cứu mới, cần máy GPU để sinh chú thích, và không làm bài B hiện tại mạnh lên.
   - Hướng (a) có thể cần nhãn chữ trong ảnh. Theo quy tắc của anh, tôi không gán nhãn mới khi anh chưa đồng ý.
   - Hướng (b) gần với phép đo ảo giác của bài A.
4. **Dừng bài B.** Mã nguồn và kết quả được giữ trong kho. Công sức dồn cho bài A, bài C và Mục tiêu 3.1.

## Khuyến nghị và mặc định

**Khuyến nghị: lựa chọn 1.** Có ba lý do:
- một kết quả âm tính được báo cáo trung thực vẫn là câu trả lời cho câu hỏi nghiên cứu 9;
- chi phí thấp nhất;
- không lấy thời gian của bài A và Mục tiêu 3.1, là nơi đề cương đặt phần mới của năm thứ nhất.

**Mặc định nếu anh chưa trả lời:** làm theo lựa chọn 1, và không đăng ký thêm nghiên cứu nào cho bài B khi chưa có ý kiến của anh.
