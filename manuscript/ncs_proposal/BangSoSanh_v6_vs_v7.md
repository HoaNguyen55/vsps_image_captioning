# Bảng so sánh v6 → v7 (30/10/2026)

v7 dùng mẫu LHU mới hơn theo quyết định của PI (30/10, khoảng 11:20 giờ VN): "Phụ lục. Yêu cầu về bài luận dự định nghiên cứu", tệp DOCX ngày 22/03/2026, có liên kết tại https://lhu.edu.vn/676/51911/Dang-ky-xet-tuyen-nghien-cuu-sinh.html. Bản lưu dùng để đối chiếu nằm trong scratchpad, tại lhu_fmt/docx2026/template_2026.docx (sha256 a314ecd9…). Tệp chỉ được đọc như dữ liệu, không mở trong Word.

v7 không thêm nhận định mới. Toàn bộ nội dung lấy từ v6, chỉ sắp xếp lại và đánh lại số mục. Các tham chiếu chéo "Mục x" đã được sửa theo số mục mới.

| Mục v7 (tên mục giữ nguyên câu chữ của mẫu) | Nội dung lấy từ v6 |
|---|---|
| 1. Tên đề tài dự định nghiên cứu | §4 |
| 2. Lý do chọn đề tài, tính cấp thiết đề tài | 2.1 ← §1.1; 2.2 ← §1.2; 2.3 ← §6 (lý do chọn LHU, giữ lại làm tiểu mục) |
| 3. Mục tiêu nghiên cứu | 3.1 ← §5.1; 3.2 ← §5.2; 3.3 ← §5.4 (đối tượng, phạm vi) |
| 4. Câu hỏi nghiên cứu | §5.3 |
| 5. Tổng quan (lý thuyết + nghiên cứu) liên quan tới đề tài | 5.1–5.3 ← §2.1–2.3 |
| 6. Khoảng trống nghiên cứu | §3 |
| 7. Ý nghĩa học thuật, thực tiễn của đề tài | §7.4 |
| 8. Phương pháp nghiên cứu | 8.1 ← §7.1 (bốn mô hình); 8.2 ← §7.2 (có câu về tiền xử lý tiếng Việt) |
| 9. Trích dẫn và nêu rõ danh mục tài liệu liên quan | danh mục tài liệu tham khảo của v6, đặt đúng vị trí mục 9, thêm một câu nói về kiểu trích dẫn IEEE |
| 10. Những dự định và kế hoạch thu thập số liệu từ các nguồn để thực hiện đề tài | 10.1 ← §7.3; 10.2 ← §7.5 (Hình 1); 10.3 ← §7.6 (Bảng 1, 2) |
| 11. Kinh nghiệm (…); kiến thức, sự hiểu biết và những chuẩn bị của thí sinh trong vấn đề dự định nghiên cứu | 11.1–11.3 ← §8.1–8.3 |
| 12. Đề xuất người hướng dẫn (nếu có) | §9 và phần chữ ký |

## Định dạng

Định dạng lấy theo các giá trị có sẵn trong tệp DOCX của mẫu:
- Phông Times New Roman 13.
- Cách đoạn sau 8 pt (`spacing after=160`).
- Giãn dòng 1,16 (`line=278`).
- Lề 2,54 cm ở cả bốn cạnh (`pgMar` = 1440).

Khổ giấy vẫn giữ A4. Mẫu đang để US Letter, nhưng đó là mặc định của Word bản en-US. Nếu cần đổi sang Letter, sửa một hằng số `size` trong build_v7_docx.js.

Mẫu không có trang bìa. v7 giữ trang bìa của v6 với tiêu đề "BÀI LUẬN DỰ ĐỊNH NGHIÊN CỨU". Mẫu cũng không quy định số trang.
