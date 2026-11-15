---
title: "Báo cáo khoa học: ba bài báo về đánh giá chú thích ảnh tiếng Việt (A, B, C) và bản hội nghị của bài C"
subtitle: "Tài liệu rà soát và hoàn thiện bài báo, lập ngày 15/11/2026"
---

# Phần mở đầu

## 0.1 Mục đích và phạm vi

Báo cáo này tổng hợp toàn bộ nội dung khoa học của ba bài báo đang được hoàn thiện trong đề tài và của bản hội nghị rút từ bài thứ ba. Mục đích của nó là làm tài liệu đối chiếu: người đọc đi qua từng mục của từng bài, thấy mục ấy khẳng định điều gì, dựa trên cơ sở lý thuyết, dữ liệu, phương pháp và kết quả nào, rồi thấy ngay những chỗ còn yếu hoặc còn phải sửa trước khi nộp.

Báo cáo gồm sáu phần. Phần A, Phần B và Phần C lần lượt trình bày bài A, bài B và bản tạp chí của bài C. Phần D trình bày bản hội nghị của bài C. Phần E ghi tình trạng hoàn thiện của từng bài và các nghiên cứu đang chạy mà văn bản bài báo chưa phản ánh. Phần mở đầu này nêu quy ước chung và bức tranh tổng thể.

Nguồn của các phần A đến D là văn bản bài báo trong kho riêng của từng bài, ở trạng thái đã lưu vào kho ngày 14/11/2026, cùng phụ lục, bảng kê số liệu và tệp tài liệu tham khảo của chính bài đó. Riêng với bài B, Phần B còn dùng bản thảo viết lại, lưu vào kho bài báo ngày 15/11/2026; đó là bài B như hiện nay (các mục B.14 đến B.28), còn văn bản lưu ngày 14/11/2026 là văn bản trước đó (B.1 đến B.13). Nguồn của Phần D là bản thảo hội nghị thứ nhất, kế hoạch viết và báo cáo khảo sát hội nghị. Báo cáo không bao gồm đề cương nghiên cứu sinh và các kịch bản trình bày đề cương, vì đó không phải là bài báo.

## 0.2 Quy ước trình bày

**Số liệu.** Mọi con số trong các phần A đến D được chép nguyên dạng in trong bài báo hoặc trong bảng kê số liệu của bài: dấu chấm là dấu thập phân, dấu phẩy ngăn hàng nghìn, số chữ số giữ nguyên, khoảng tin cậy giữ nguyên dạng. Báo cáo không làm tròn lại, không đổi đơn vị và không tính thêm số mới. Cách viết này khác thông lệ tiếng Việt, nhưng nó cho phép đối chiếu từng con số với bài báo tiếng Anh và đã được kiểm bằng chương trình: mỗi số thập phân, mỗi tỉ lệ phần trăm và mỗi số nguyên từ 100 trở lên trong báo cáo đều phải xuất hiện đúng như vậy trong nguồn.

**Phán quyết đã đăng ký.** Mỗi dự đoán đăng ký trước có một phán quyết do quy tắc đã đăng ký sinh ra. Báo cáo chép phán quyết ấy nguyên văn tiếng Anh trong ngoặc kép, chẳng hạn "PASS", "FAIL", "MIXED" hay "INCONCLUSIVE", rồi mới giải thích bằng tiếng Việt. Một phán quyết "FAIL" được nêu rõ cùng ước lượng, khoảng tin cậy và ngưỡng đã đăng ký. Cụm "không phát hiện được" không đồng nghĩa với "không có hiệu ứng".

**Mức bằng chứng.** Báo cáo giữ nguyên nhãn mà bài báo gắn cho từng kết quả: kết quả xác nhận đã đăng ký trước; kết quả thăm dò (exploratory); kết quả hậu kiểm (POST HOC), đặt cạnh kết quả đăng ký và không có phán quyết; kết quả chỉ trên tập phát triển (development only), không phải bằng chứng xác nhận.

**Tài liệu tham khảo.** Mỗi phần chỉ trích dẫn những công trình có trong tệp tài liệu tham khảo của chính bài báo đó; danh mục ở cuối mỗi phần được sinh tự động từ tệp ấy. Báo cáo không thêm tài liệu nào.

**Cấu trúc của mỗi mục.** Mỗi mục của bài báo ứng với một mục của báo cáo, gồm hai khối. Khối "Nội dung" thuật lại đầy đủ và trung thành nội dung của mục. Khối "Nhận xét rà soát" là phân tích của người đọc phản biện: mục ấy chứng minh được gì, chỗ nào chưa nhất quán, người phản biện có thể hỏi gì và cần sửa gì. Cuối mỗi phần có bảng đối chiếu khẳng định với bằng chứng, danh mục việc cần rà soát và bảng thuật ngữ.

**Nội dung không xuất hiện.** Báo cáo không chép câu chú thích nào của bất kỳ bộ dữ liệu nào và không chép đầu ra của mô hình. Một số kết quả đang được giữ kín vì nhà nghiên cứu là người chấm trong nghiên cứu tương ứng; Phần E nêu rõ đó là những kết quả nào.

## 0.3 Bức tranh chung của ba bài

Ba bài cùng bàn về độ tin cậy của phép đo trong sinh chú thích ảnh tiếng Việt, nhưng mỗi bài xét một khâu khác nhau của phép đo. Bài A xét tập chuẩn đối tượng mà các điểm ảo giác đối tượng dựa vào. Bài B, ở bản thảo viết lại, xét khâu xử lý văn bản đầu vào của phép chấm dựa trên tham chiếu (đơn vị, vị trí dấu thanh, dấu câu, chữ hoa); phép kiểm định bộ chuẩn KTVIC của văn bản trước nay là phụ lục trực tuyến của bài. Bài C xét cách so sánh có đối chứng cho lời nhắc dùng ví dụ truy hồi, và bản hội nghị trình bày phần lõi của bài C trong khuôn khổ ngắn hơn. Bảng 0.1 tóm lược câu hỏi và kết quả chính của từng bài đúng như văn bản hiện có; mọi con số trong bảng được giải thích ở phần tương ứng.

**Bảng 0.1.** Câu hỏi, kết quả chính và cơ sở bằng chứng của từng bài (chép từ các mục "Thông tin chung" A.1, B.1, C.1 và D.1).

| Bài | Nơi gửi | Câu hỏi | Kết quả chính như bài báo in | Cơ sở bằng chứng |
|---|---|---|---|---|
| A (Phần A) | Signal Processing: Image Communication | Khi giữ nguyên chú thích và thay tập chuẩn đối tượng, điểm ảo giác đối tượng (CHAIR, F1 đối tượng) thay đổi ra sao? | Khẳng định xác nhận duy nhất: độ dốc dài dòng của F1 đối tượng được xếp thứ tự từ một tham chiếu, đến tất cả tham chiếu, đến nhãn đã kiểm chứng. Phép lặp lại trên PASCAL-50S thất bại ở bước tập chuẩn theo nhãn. Chín dự đoán đã đăng ký thất bại và được báo cáo đầy đủ. | 600 ảnh XM3600 với sáu hệ thống của một mô hình nền; mô hình nền thứ hai trên 537 ảnh; 3,226 ảnh COCO val2017 được để dành; các phép thử chính đều đăng ký trước, các hàng hậu kiểm mang nhãn riêng |
| B (Phần B, các mục B.14 đến B.28) | Language Resources and Evaluation | Một phép so sánh hai hệ thống sinh chú thích tiếng Việt có cho cùng kết luận dưới mọi khâu xử lý văn bản đầu vào chấp nhận được hay không? | Thủ tục FE-CERT trên một họ 72 thành viên và một lần áp dụng đã đăng ký. P1 "INCONCLUSIVE": 2 trong 72 chứng nhận sát biên vỡ dưới các thành viên để dành (0.028; cận 0.005 và 0.085), kèm nhãn "LOW-SENSITIVITY". P2 "NOT SUPPORTED": "the certificate changed few conclusions in this pool (2 of 10)". Phần đánh giá của con người: hai người chấm, 300 cặp, đồng thuận thấp (kappa của Cohen 0.351), nên hai giả thuyết không mang nhãn ("no label: low inter-rater agreement"). | 1101 phép so sánh phát triển trên tệp của chính nhóm (một mô hình nền; tham chiếu KTVIC đã dùng trước); 22 phép so sánh trên đầu ra do nhóm khác công bố, 20 từ một kho; đối chứng tiếng Anh "CONTROL: NOT RUN"; phép kiểm định KTVIC và các nghiên cứu đăng ký trước (B.1 đến B.13) nay ở phụ lục trực tuyến |
| C (Phần C) | ACM TALLIP | Mức tăng của lời nhắc có ví dụ truy hồi so với lời nhắc không ví dụ đến từ việc truy hồi, hay từ việc mô hình được thấy văn phong chú thích trong miền? | OpenViIC test (1,941 ảnh): nhánh truy hồi hơn nhánh ngẫu nhiên +4.49 [3.52, 5.57] điểm CIDEr-D đã lược dấu câu cuối, "PASS". XM3600 tiếng Việt: +0.70 [−0.45, 1.97], "FAIL". COCO Karpathy test: +3.08 [2.08, 4.03], "PASS". | Thiết kế tiền đăng ký, báo cáo theo từng mô hình nền, mỗi tập kiểm tra nhìn một lần; bài tự xác định không đề xuất phương pháp mới |
| Bản hội nghị của C (Phần D) | TAIMMA 2027, mẫu Springer LNCS | Như bài C, giới hạn ở nghiên cứu chính đã đăng ký: chú thích ví dụ được truy hồi có cho điểm cao hơn cùng số chú thích ngẫu nhiên từ cùng bộ nhớ không? | Cùng các phán quyết của bài C trên OpenViIC, XM3600, COCO và NoCaps. Bản nháp viết "The study proposes no new method" và không khẳng định sự chuyển giao ở cả hai ngôn ngữ. | Phép thử tiếng Việt và nhánh tiếng Anh ở dạng cô đọng; nghiên cứu quy kết, phần Flickr30K, các phép cắt bỏ và phụ lục để lại cho bản tạp chí. Báo cáo khảo sát đánh giá độ tin cậy của hội nghị là "unclear". |

Ba điểm chung đáng lưu ý khi đọc bảng. Thứ nhất, cả ba bài là bài về phép đo và đánh giá; không bài nào khẳng định một hệ thống đạt kết quả tốt nhất. Thứ hai, mỗi bài đều in các dự đoán đăng ký không đạt cạnh các dự đoán đạt, và báo cáo này giữ nguyên cách trình bày ấy. Thứ ba, bài A và bài B dùng chung một số công cụ (bộ chấm điểm, bộ so khớp đối tượng, các đối chứng khớp số lượng), nhưng theo nguyên tắc ghi ở B.1.6, không con số nào là kết quả chính ở cả hai bài.

Tại thời điểm lập báo cáo, chưa bài nào ở trạng thái có thể nộp. Phần E nêu từng việc còn lại, việc nào chờ nhà nghiên cứu và việc nào chờ một mốc thời gian đã đăng ký.

## 0.4 Nguyên tắc phương pháp chung

Ba bài dùng chung một bộ nguyên tắc; mỗi bài mô tả cách áp dụng cụ thể trong phần phương pháp của mình.

1. **Đăng ký trước.** Dự đoán, quy tắc quyết định và phân tích được viết ra và lưu vào kho trước khi nhìn dữ liệu mà chúng chi phối. Một phân tích viết sau khi đã nhìn kết quả được gắn nhãn hậu kiểm.
2. **Mỗi tập kiểm tra chỉ nhìn một lần.** Việc thăm dò diễn ra trên tập phát triển; một cấu hình chỉ được chấm trên tập kiểm tra sau khi đã chốt, và chỉ một lần.
3. **Báo cáo cả kết quả không đạt.** Một dự đoán đăng ký không đạt vẫn được nêu trong tóm tắt, phần mở đầu và kết luận của bài, không bị giấu và không bị diễn giải lại.
4. **Nhãn tham chiếu là nhãn do con người tạo.** Nhãn do mô hình sinh ra không được dùng làm bằng chứng. Nhãn mới do con người gán chỉ có ở hai nơi đã được quyết định riêng: bộ nhãn hiện diện đối tượng trên 600 ảnh XM3600 của bài A và phần so sánh cặp của bài B, đã chấm xong và được báo cáo ở B.21 (xem thêm Phần E).
5. **Dùng trọn các tập chia chính thức.** Không cắt bớt dữ liệu để tiết kiệm thời gian; mọi loại trừ đều có nguyên tắc, được cố định trước và được công bố cạnh kết quả đầy đủ.
6. **Đối chiếu với dữ liệu tiếng Anh.** Bài C có một mục riêng so sánh với tiếng Anh (Mục 8 của bài). Bài A không có mục riêng nhưng dùng dữ liệu tiếng Anh xuyên suốt (xem A.1). Bài B hiện chưa có phần này: ở bản thảo viết lại, đối chứng tiếng Anh đã đăng ký ghi "CONTROL: NOT RUN" và bài không khẳng định gì ngoài tiếng Việt (xem B.20.5); ở văn bản trước, Bảng S12.1 của phụ lục ghi "none" ở hàng "English data" (xem B.1.5). Đây là một điểm nhà nghiên cứu cần quyết định khi hoàn thiện bài B.
7. **Truy vết số liệu.** Mỗi con số trong bài có một dòng trong bảng kê số liệu, chỉ tới tệp và khóa sinh ra nó.

## 0.5 Cách dùng báo cáo

Người đọc nên đi theo thứ tự: mục "Thông tin chung" của từng phần để nắm khẳng định của bài; bảng đối chiếu khẳng định với bằng chứng để biết mỗi khẳng định đứng trên kết quả nào; rồi danh mục việc cần rà soát để biết phải sửa gì. Khi viết lại một mục của bài, người đọc mở mục tương ứng của báo cáo để đối chiếu định nghĩa, công thức, bảng và phán quyết. Phần E cho biết những chỗ văn bản sẽ còn thay đổi vì nghiên cứu chưa kết thúc.
