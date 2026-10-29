# Tóm tắt học tập cho PI: Paper A (SPIC), cập nhật sau PASCAL-50S

Ngày 2026-10-29. Kết quả PASCAL-50S được chấm xong lúc 13:23 giờ VN và chỉ được chấm một lần. Mọi con số dưới đây đều được chép từ file quyết định. Nguồn của từng số nằm trong `number_manifest.tsv`.

## 1. Paper A nói gì

1. **Khẳng định xác nhận duy nhất.** Độ dốc của object F1 theo ln M (M là số đối tượng caption nhắc tới) được **xếp thứ tự theo độ đầy đủ của gold**. Thứ tự là: 1 tham chiếu < tất cả tham chiếu < nhãn đã kiểm. Khẳng định này dựa trên XM3600 (600 ảnh, đăng ký trước) và backbone thứ hai Qwen3-VL-8B (537 ảnh).
2. **PASCAL-50S: lặp lại ngoài mẫu và đã THẤT BẠI (FAIL).** Thứ tự 1 tham chiếu < 50 tham chiếu thì giữ. Thứ tự 50 tham chiếu < nhãn VOC thì không giữ. Vì vậy khẳng định chỉ còn đứng trên XM3600 và backbone thứ hai. Nó không mở rộng được tới gold 50 tham chiếu so với nhãn VOC 20 lớp.
3. **Độ dốc tăng ở mọi bước thêm tham chiếu: PASS (thứ cấp).** Các bước là k = 1 → 2 → 5 → 10 → 20 → 50.
4. **Cơ chế thứ cấp X4: PASS.** So với một null xóa ngẫu nhiên cùng kích thước, gold tham chiếu thật kéo độ dốc xuống mạnh hơn. Kết quả này **phù hợp với** việc gold tham chiếu phạt caption dài qua **đối tượng nào** người viết nhắc tới, không chỉ **bao nhiêu** đối tượng; nó **không chứng minh nhân quả**. Đây là phép thử cơ chế thứ cấp và không đưa vào abstract.
5. **Đếm số đối tượng (count) chỉ là thăm dò.** Leaderboard khớp số đối tượng đã đăng ký nhưng trượt kiểm tra độ trung thực, nên không được chấm.
6. **Tổng số dự đoán đăng ký bị FAIL: 9.** Danh sách đầy đủ ở Bảng 1, gồm thêm A24 là P50-A4.

## 2. Số cần nhớ

| Nội dung | Số |
|---|---|
| XM3600: độ dốc với 1 tham chiếu / tất cả tham chiếu / nhãn OIV7 | −8.99 / −2.43 / +19.32 |
| PASCAL-50S: ảnh được phân tích, số mô hình, số run | 997 / 1,000 ảnh; 7 mô hình; 14 run (Idefics3-8B bị loại theo trần 8 GPU-h) |
| P50-A4 phần 1 (50 tham chiếu − 1 tham chiếu, V20) | +37.16 [+35.07, +39.09], PASS |
| P50-A4 phần 2 (nhãn VOC − 50 tham chiếu, V20) | −2.29 [−5.15, +0.61], FAIL (điểm ≤ 0) |
| P50-O2, năm bước | +3.51, +6.88, +5.91, +6.32, +7.93 (cả năm đều PASS) |
| Độ dốc COCO-80: 1 tham chiếu → 50 tham chiếu | −31.38 → −0.83 [−2.58, +1.07] (không dự đoán dấu) |
| Độ dốc V20: 50 tham chiếu / nhãn VOC | +9.74 / +7.45 |
| X4: observed và khoảng null 95%, 1 tham chiếu | −31.38 so với [−14.97, −12.12]; p = 0.001 |
| X4: observed và khoảng null 95%, 5 tham chiếu | −20.99 so với [−9.28, −6.87]; p = 0.001 |
| X5 | NOT_EVALUABLE: 1,782 < 2 × 1,039.6 |
| Đọc Holm family-wise (mô tả) | P50-A4 p = 0.939, không qua; O2 và X4 qua |
| X1, mô tả, không phán quyết | MAE: jackknife 4.17; pooled-uniform 6.46; raw 9.95 |
| X2, mô tả | τ_b từ 0.868 lên 0.956; khoảng tin cậy chứa 0 |

## 3. Mười câu reviewer dễ hỏi nhất, kèm trả lời ngắn

1. **"Kết quả PASCAL-50S fail, vậy khẳng định chính có sụp không?"**
   Không. Chúng tôi báo cáo đúng nhánh văn bản đã viết sẵn trước khi chạy (§9.2). Khẳng định xác nhận được giới hạn lại ở XM3600 và backbone thứ hai. Phần fail được ghi FAIL trong Bảng 1.
2. **"Sao phần 2 bị gọi FAIL khi khoảng tin cậy chứa 0?"**
   Quy tắc đã đăng ký là: điểm ≤ 0 thì FAIL. Quy tắc này cũng khớp tiêu chí điểm ước lượng của A4 gốc. Chúng tôi không đổi quy tắc sau khi đã nhìn kết quả.
3. **"Có thể do bộ so khớp không nhận 'aeroplane' hoặc do V20 quá hẹp?"**
   Cả hai giới hạn này đã được ghi trong đăng ký trước khi chạy (§10). Chúng tôi không kiểm tra liệu chúng có giải thích kết quả fail hay không. Mọi cách giải thích như vậy là post hoc.
4. **"Mô hình có thể đã thấy ảnh PASCAL khi pretrain?"**
   Có thể. Ảnh và caption đã công khai từ 2008–2015. Bài viết nói rõ các ảnh này mới với nhóm tác giả, chưa chắc mới với mô hình.
5. **"Sao chỉ có 7 mô hình?"**
   Trần 8 GPU-giờ và thứ tự loại mô hình được cố định trước khi chạy. Idefics3-8B đứng đầu thứ tự loại. Không mô hình nào bị loại vì lỗi.
6. **"X4 có phải là kết quả mới hoàn toàn không?"**
   Không nói "first". Rohrbach et al. (2018) đã cho thấy gold chỉ dựa trên caption làm phồng điểm hallucination. Phần chúng tôi thêm vào chỉ là null xóa ngẫu nhiên cùng kích thước trên gold 50 tham chiếu.
7. **"Holm của X4 tính trên family nào?"**
   Family đăng ký là {X4, X5}. X5 là NOT_EVALUABLE nên rời khỏi family. Do đó X4 được hiệu chỉnh một mình và vẫn qua ở α = 0.025 một phía.
8. **"Bộ ước lượng jackknife (X1) có được kiểm chứng không?"**
   Không. Trên dữ liệu dev, nó không cải thiện xếp hạng, nên X1 và X2 được cố định là mô tả trước khi chạy. Trên PASCAL, MAE thấp hơn nhưng τ_b không tăng có ý nghĩa. Vị trí so với các công trình khác: Zobel (1998) ước lượng số mục liên quan; Trushkowsky et al. (2013) ước lượng kích thước tập.
9. **"Có thể tái lập không, khi caption đầu ra đã bị xoá?"**
   Theo quy tắc dữ liệu đã đăng ký, cả 14 file caption đều trùng ít nhất một 8-gram với tham chiếu PASCAL-50S, nên đã bị xoá trên máy chấm cùng ảnh và tham chiếu; không giữ mã băm nào của chúng. Phán quyết chỉ có thể tính lại bằng cách chạy lại job đã đăng ký từ snapshot mô hình, decoder và code đã ghim (không bảo đảm ra đúng từng byte). Đầu ra theo từng ảnh **không thể kiểm toán** (audit) được: chạy lại được, nhưng không kiểm tra lại được đầu ra gốc.
10. **"Bản quyền PASCAL-50S thế nào?"**
    Repo gốc có giấy phép BSD-2, không có giấy phép dữ liệu riêng. Chúng tôi đã có xác nhận bằng văn bản của tác giả bộ dữ liệu (2026-10-28). Chỉ dùng để đánh giá và không phân phối lại.

## 4. Mốc học (PI-1029)

- Đọc §7.4 và §7.6, rồi Bảng 1 (các hàng A24–A24d).
- Tự trả lời được câu 1, 2, 3 và 7 mà không cần nhìn tài liệu.
