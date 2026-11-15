# Phần E. Tình trạng hoàn thiện và các nghiên cứu đang tiến hành

Phần này ghi lại trạng thái của từng bài tính đến rạng sáng ngày 15/11/2026 (giờ Việt Nam) và những nghiên cứu đang chạy mà văn bản bài báo chưa phản ánh. Các phần A đến D mô tả bài báo đúng như văn bản hiện có; phần này cho biết văn bản ấy sẽ còn thay đổi ở đâu và vì sao.

## E.1 Phạm vi và nguyên tắc giữ kín

Hai nghiên cứu đang chạy có phần chấm của con người, và nhà nghiên cứu chính là một trong những người chấm. Để câu trả lời của người chấm không bị ảnh hưởng bởi kết quả, các số liệu sau đây chưa được đưa vào báo cáo này:

- Bài A: các số liệu chi tiết tính từ câu trả lời của nhà nghiên cứu trên bộ nhãn mới của XM3600 (mức đồng thuận, tỉ lệ theo lớp, các số đếm, số liệu theo từng hệ thống và giá trị độ dốc), cùng một số chi tiết về cách dựng bản phân công. Chúng được giữ kín cho tới khi buổi gán nhãn bổ sung của nhà nghiên cứu kết thúc. Bảy phán quyết của lần chấm phần 1 đã được báo cho nhà nghiên cứu từ ngày 13/11/2026 và được chép ở Phần A.
- Bài B: không còn số liệu nào được giữ kín. Phần chấm của bài B đã đóng ngày 15/11/2026, phép phân tích phần chấm đã chạy, và toàn bộ kết quả của nghiên cứu đã được công bố cho nhà nghiên cứu; chúng được trình bày ở các mục B.14 đến B.28.

Vì vậy, với nghiên cứu của bài A, báo cáo chỉ trình bày thiết kế ở mức văn bản bài đã công bố trong kho bài báo, khối lượng công việc và các mốc thời gian. Khi điều kiện giữ kín hết hiệu lực, phần kết quả sẽ được bổ sung theo đúng quy trình đã dùng cho các phần khác: số liệu chép từ tệp kết quả đã đăng ký, phán quyết chép nguyên văn.

## E.2 Bài A

**Bộ nhãn hiện diện đối tượng trên 600 ảnh XM3600.** Văn bản về bộ nhãn này nằm ở Mục 6.7 và Phụ lục S11 của bài (xem A.9 và A.15). Lần chấm phần 1 đã chạy một lần ngày 12/11/2026; bảy phán quyết của nó đã có trong bài, tất cả mang nhãn "single annotator". Nhà nghiên cứu, với tư cách người gán nhãn là tác giả và biết nội dung nghiên cứu, đã gán nhãn xong cả ba phần của bản phân công chính vào sáng 14/11/2026.

**Người gán nhãn thứ hai.** Một đồng nghiệp cùng công ty, không phải tác giả, chưa xem thông tin nào của nghiên cứu, đọc tiếng Việt thành thạo và đã đồng ý bằng văn bản, sẽ trả lời lại phần chung gồm 150 ảnh (332 màn hình, 1,110 câu hỏi), sau một vòng làm quen. Người này làm việc từ xa, một mình, qua một đường dẫn riêng có khóa tới đúng trang và đúng hướng dẫn mà nhà nghiên cứu đã dùng. Hai lưu ý về từ ngữ được đưa cho mọi người gán nhãn với cùng một nguyên văn: từ «bóng» chỉ quả bóng, và từ «cầu» chỉ cây cầu.

**Buổi gán nhãn bổ sung.** Nhà nghiên cứu còn một buổi bổ sung gồm 943 màn hình với 1,755 câu hỏi. Buổi này không có hạn cứng và được xếp sau khi phần chấm của bài B đóng.

**Ứng dụng gán nhãn.** Từ ngày 15/11/2026, quy trình gán nhãn của bài A có một ứng dụng web chạy trên máy của nhà nghiên cứu. Ứng dụng cho biết từng phiên (bộ chính, buổi bổ sung, phần chung của người gán nhãn thứ hai) đang ở đâu, dẫn tới trang gán nhãn khi phiên đang mở, kiểm tra tệp nhãn ở mức tệp và tạo bản xuất chỉ đọc có bảng kê mã sha256. Trang gán nhãn đã đăng ký được giữ nguyên từng byte, vì bản đăng ký và câu công bố về người gán nhãn thứ hai đều yêu cầu hai người dùng cùng một trang và cùng hướng dẫn; ứng dụng chỉ bao quanh trang ấy. Ứng dụng không đọc nội dung của dòng nhãn, không hiện giá trị nhãn và không tính số liệu nào từ nhãn, nên không chạm tới các nguyên tắc giữ kín ở E.1. Phần kiểm tra gồm ba điều: bản phân công đúng mã đã ghim; dòng cuối của tệp nhãn được ghi trọn; và mọi bản sao chỉ đọc tạo ở cuối mỗi phiên là phần đầu của tệp nhãn hiện tại, tức tệp chỉ được ghi nối thêm và không nhãn nào bị ghi đè.

**Mã phân tích.** Mã phân tích theo từng người gán nhãn đã qua hai lượt đọc và còn chờ một lần chạy thử trên máy thuê. Sau đó, mỗi phép phân tích đã đăng ký chỉ chạy một lần: phép chấm của nhánh mô hình khác họ chạy sau buổi bổ sung; độ đồng thuận giữa hai người gán nhãn tính sau phiên cuối của người thứ hai; phân tích theo từng người gán nhãn chạy sau lần chạy thử, lượt đọc bản ghi và dòng mở niêm phong.

**Văn bản bài sẽ thay đổi ở đâu.** Mục 6.7 và Phụ lục S11 còn chờ bốn nhóm nội dung, mỗi nhóm chỉ được đưa vào sau sự kiện của nó: câu về độ đồng thuận giữa hai người gán nhãn và quy tắc kappa đi kèm; các hàng của phần 2 và mức đồng thuận của phần lặp lại; các hàng của buổi bổ sung; và câu công bố về người gán nhãn thứ hai. Khi đó các phán quyết đang mang cụm "single annotator" trong tóm tắt, phần nêu bật (highlights) và Bảng 1 được xử lý theo quy tắc kappa đã đăng ký (xem A.9): hoặc giữ nguyên, hoặc chuyển thành "sensitivity analysis only". Câu công bố về cách làm việc của người gán nhãn thứ hai được thêm cạnh các câu công bố hiện có về người gán nhãn, với nguyên văn đã đăng ký: "The second rater worked alone and unsupervised, on their own device, through a private key-protected link to the same rating page and instructions; the author who sent the link did not observe the sessions."

## E.3 Bài B

**Nghiên cứu đang chạy.** Bài B có một nghiên cứu đã đăng ký gồm các bước tính trên máy và một phần chấm của con người. Mọi bước tính trên máy đã chạy đúng một lần trong hai ngày 13 và 14/11/2026 trên một máy thuê, và kết quả đã được đọc. Phần chấm của con người đóng ngày 15/11/2026 và phép phân tích của nó chạy một lần cùng ngày. Kết quả của mọi bước đã được công bố cho nhà nghiên cứu và được trình bày ở B.19 đến B.21: hai dự đoán của các bước tính trên máy nhận nhãn "INCONCLUSIVE" (kèm "LOW-SENSITIVITY") và "NOT SUPPORTED"; hai giả thuyết của phần chấm của con người không nhận nhãn nào, vì mức đồng thuận giữa hai người chấm thấp.

**Phần so sánh cặp.** Trong phần chấm của con người, mỗi màn hình cho người chấm xem một ảnh của tập kiểm tra KTVIC cùng hai chú thích do các hệ thống của chính nhóm sinh ra, và người chấm chọn giữa hai chú thích theo hướng dẫn trên trang. Có hai người chấm: nhà nghiên cứu và người chấm thứ hai (cùng người với bài A). Cả hai đã chấm xong toàn bộ các cặp; người chấm thứ hai trả lời trực tiếp tại máy của nhà nghiên cứu chứ không qua đường dẫn từ xa đã chuẩn bị, và không người chấm nào làm vòng luyện tập. Phần chấm đã đóng ngày 15/11/2026, trước thời hạn đã đăng ký, và bước phân tích phần chấm (bước H) đã chạy một lần trên một máy thuê. Các số liệu và các câu công bố về cách phiên chấm diễn ra được chép ở B.19.5 và B.21.

**Văn bản bài sẽ thay đổi ở đâu.** Bản thảo viết lại của bài B đã được hoàn tất với kết quả của phần chấm và đã qua một lượt đọc; nó đang chờ bước chuyển vào kho bài báo, kèm các quyết định cần nhà nghiên cứu trả lời. Phần B của báo cáo nay mô tả cả hai lớp văn bản: các mục B.1 đến B.13 mô tả văn bản hiện có trong kho bài báo, tức văn bản trước nghiên cứu này, và các mục B.14 đến B.28 mô tả bản thảo viết lại. Trong bản thảo viết lại, các câu nói rằng bài không có đánh giá của con người đã được thay, và các câu công bố về hai người chấm được in nguyên văn (xem B.21.1). Bản thảo viết lại chưa ở trạng thái nộp được; các việc còn lại nêu ở B.27.

## E.4 Bài C, bản tạp chí

Văn bản hiện có trong kho bài báo đã chứa phần phân tích quy kết (attribution) trên tập phát triển, gồm cả kết quả của khối 3 (xem Phần C, Mục 6.10 của bài). Ba việc còn lại đều đã có lịch:

1. Dòng mốc của khối 2 đã được ghi rạng sáng ngày 15/11/2026, đúng nguyên văn mẫu đã đăng ký: khối 2 không chạy trước mốc 18:00 ngày 14/11/2026. Bản cập nhật văn bản thứ nhất đi kèm dòng này chưa được đưa vào kho bài báo; nó thêm một mục con nói rõ phần nào không chạy, và được một lượt đọc phần khác biệt trước khi lưu. Bản cập nhật này cũng sửa lỗi đánh số tiêu đề: Mục 6.10 hiện đi thẳng từ phần mở đầu sang 6.10.2, thiếu tiêu đề 6.10.1.
2. Dòng mốc K7 của bản đăng ký được ghi từ 12:00 ngày 16/11/2026, kèm bản cập nhật văn bản thứ hai.
3. Bản PDF của bài đã được dựng lại nhưng chưa đưa vào kho; nó sẽ được dựng lại lần nữa trên máy thuê sau hai bản cập nhật trên.

## E.5 Bài C, bản hội nghị TAIMMA 2027

Kế hoạch viết đã được duyệt và bản thảo thứ nhất đã xong ngày 14/11/2026 (xem Phần D). Các bước còn lại: ba người đọc phản biện bản thảo; nhà nghiên cứu tự viết lại; một lượt đọc phần khác biệt; nhà nghiên cứu tự nộp trước 18:59 ngày 3/12/2026 (giờ Việt Nam). Mục 5 và Mục 7 của bản thảo phải được đối chiếu lại sau 12:00 ngày 16/11/2026, vì chúng phụ thuộc vào dòng mốc K7 của bản tạp chí. Các quyết định còn chờ nhà nghiên cứu được liệt kê ở Phần D.

## E.6 Các mốc thời gian

**Bảng E.1.** Các mốc cứng và mốc dự kiến, giờ Việt Nam.

| Mốc | Việc | Bài | Loại |
|---|---|---|---|
| 15/11/2026, 18:00 | Đóng phần chấm so sánh cặp (cả hai người chấm) | B | cứng |
| 15/11/2026 | Ba quyết định mặc định cho bản hội nghị | C (TAIMMA) | dự kiến |
| 16/11/2026, 12:00 | Bước phân tích phần chấm chạy xong trên máy thuê | B | cứng |
| 16/11/2026, 12:00 | Dòng mốc K7 và bản cập nhật văn bản thứ hai | C | theo đăng ký |
| Sau khi bài B đóng | Buổi gán nhãn bổ sung của nhà nghiên cứu (1,755 câu hỏi) | A | không có hạn cứng |
| Trước 1/12/2026 | Danh sách tác giả của bản hội nghị | C (TAIMMA) | dự kiến |
| 3/12/2026, 18:59 | Hạn nộp đợt ba của hội nghị | C (TAIMMA) | cứng |

## E.7 Những việc chỉ nhà nghiên cứu làm được

1. Xin người chấm thứ hai của bài B một dòng xác nhận rằng người này đã trả lời một mình (xem B.21); phần chấm so sánh cặp của bài B đã xong.
2. Làm buổi gán nhãn bổ sung của bài A.
3. Trả lời các quyết định của bản hội nghị (Phần D) và chốt danh sách tác giả.
4. Trả lời các quyết định còn mở của bài B và điền các tuyên bố còn trống (xem B.27.1); phần chấm đã đóng.
5. Tự viết lại từng bài trước khi nộp; báo cáo này là tài liệu đối chiếu cho việc đó.

## E.8 Trạng thái theo tiêu chí sẵn sàng nộp

Nhà nghiên cứu định nghĩa một bản thảo là sẵn sàng nộp khi đủ sáu điều: nội dung khoa học đầy đủ; số liệu, kết quả và trích dẫn có bằng chứng xác minh; mã, thực nghiệm, bảng, hình và phụ lục đã được kiểm tra; không còn mâu thuẫn giữa nội dung và kết quả; đúng khuôn mẫu và yêu cầu của nơi nhận; đã rà soát toàn văn, ngôn ngữ và lỗi kỹ thuật. Mỗi hạng mục nhận một trong ba trạng thái: "READY" (đủ tiêu chí), "BLOCKED" (chờ dữ liệu, quyết định hoặc hành động của nhà nghiên cứu) và "NOT READY" (còn việc có thể chủ động xử lý). Bảng E.2 áp định nghĩa ấy cho từng bài tại thời điểm lập báo cáo. Chưa bài nào đạt "READY".

**Bảng E.2.** Trạng thái của từng bài theo định nghĩa sẵn sàng nộp.

| Bài | Trạng thái | Việc còn chủ động xử lý được | Việc chờ nhà nghiên cứu hoặc chờ mốc đã đăng ký |
|---|---|---|---|
| A | "NOT READY" và "BLOCKED" | chạy thử mã phân tích trên máy thuê; các mâu thuẫn và chỗ cần sửa nêu ở A.17; phần chính còn dài hơn giới hạn của tạp chí (xem A.1) | phiên của người gán nhãn thứ hai; buổi gán nhãn bổ sung; sau đó mới chạy các phép phân tích đã đăng ký và cập nhật Mục 6.7, Phụ lục S11 |
| B | "NOT READY" và "BLOCKED" | các việc nêu ở B.27 đối với bản thảo viết lại và ở B.12 đối với phần văn bản được mang sang; dựng hình và bảng bằng tập lệnh; kiểm các trích dẫn còn đánh dấu | chuyển bản thảo viết lại vào kho bài báo; các quyết định của nhà nghiên cứu về bài B; các tuyên bố về đạo đức và sự đồng ý; dòng xác nhận của người chấm thứ hai |
| C, bản tạp chí | "NOT READY" | bản cập nhật văn bản thứ nhất; các việc nêu ở C.14; dựng lại bản PDF theo khuôn mẫu của tạp chí | dòng mốc K7 từ 12:00 ngày 16/11/2026, rồi bản cập nhật thứ hai |
| C, bản hội nghị | "NOT READY" và "BLOCKED" | ba người đọc phản biện bản thảo và việc sửa theo kết luận của họ; cắt phần lời cho vừa khuôn khổ đã định trong kế hoạch viết | các quyết định nêu ở Phần D; danh sách tác giả; nhà nghiên cứu tự viết lại và tự nộp |

