# Mục tiêu hiện tại (cập nhật theo tiến độ)

**Cập nhật lần cuối:** 15/11/2026, 18:55 giờ Việt Nam. Goal của phiên do PI đặt bằng `/goal` rạng sáng 15/11 (PI-1114k); nguyên văn ở mục dưới. Tệp này được sửa mỗi khi mục tiêu hoặc tiến độ thay đổi; nhật ký quyết định gốc nằm ở `.session_backup/2026-10-13/decisions/LOG.md`.

## Tiến độ lúc 18:55 ngày 15/11 (bảng bên dưới là trạng thái lúc 11:56; khối này mới hơn)

PI-1115p: đội tối đa 20 agent, người điều phối không sửa mã hay văn bản. Sáu việc đang chạy hoặc vừa xong:

- **Bài B:** phần chấm đã đóng (15:08), bước H chạy một lần (15:30), kết quả đã mở cho PI (CC-418). Bản viết lại đã vào kho bài: `paper/rev_2026-11-15/`, commit 568eaec (CC-420). Còn: gói sửa các mục kiểm sẵn sàng (đang soạn), hình và Bảng 6 trên máy thuê, một lượt đọc, vòng ba giám khảo. Chờ PI: câu một dòng của người chấm thứ hai, dữ kiện về đồng thuận và đạo đức, toàn văn hai công trình Berger.
- **Bài A:** gói sửa v6 đã vào kho (95909d4 và a7f2b4e, CC-422). Ba lượt đọc toàn văn (trừ 6.7 và S11) xong: 133 phát hiện, 3 mục chặn ở phụ lục; gói v7 đang soạn. Chờ PI: giờ hai phiên gán nhãn.
- **Bài C:** gói v5 đã có phán quyết (CC-423); chuỗi 12:00 ngày 16/11 đã chạy thử trọn trên bản sao (`fix_packages/2026-11-15_C/CHAIN_REHEARSAL_2026-11-15.md`).
- **TAIMMA:** bản 3.1 sau cắt (ước 14,4 trang; CC-421), quy tắc đạt của vòng chấm mù đã chốt (CC-424), thẻ chấm mù đã dựng lại. Còn: đếm trang trên máy thuê, đối chiếu sau mốc 16/11, vòng chấm mù, vòng cuối.
- **Báo cáo khoa học:** dựng lại 18:31, 234 trang, Phần B theo bài hiện tại.
- **Máy thuê:** kế hoạch `HOST_RUN_PLAN_2026-11-16.md`, giám khảo CC-425 đang đọc; dự định thuê tối nay, tối đa 3 giờ.

Tệp cho PI: `VIEC_PI_TU_LAM_2026-11-15.md` (45 việc PI tự làm), `STUDY_BRIEF_B_2026-11-15.md` (bản học bài B; không cho người chấm thứ hai xem).

## Goal của phiên (nguyên văn PI)

> **Đưa toàn bộ báo cáo và bài báo khoa học đến trạng thái READY FOR SUBMISSION.** Hoàn tất báo cáo khoa học và đưa các bản thảo A (SPIC), B (LRE), C (TALLIP) cùng phiên bản hội nghị TAIMMA 2027 của bài C đến trạng thái READY FOR SUBMISSION một cách trung thực, có bằng chứng kiểm chứng và không đánh đổi chất lượng khoa học để chạy theo tiến độ.

**READY FOR SUBMISSION** khi đủ sáu điều: nội dung khoa học đầy đủ; số liệu, kết quả và trích dẫn có bằng chứng xác minh; mã, thực nghiệm, bảng, hình và phụ lục đã kiểm tra; không còn mâu thuẫn giữa nội dung và kết quả; đúng khuôn mẫu và yêu cầu của nơi nhận; đã rà soát toàn văn, ngôn ngữ và lỗi kỹ thuật. Ba trạng thái: **READY** (đủ tiêu chí, có thể nộp); **BLOCKED** (chờ dữ liệu, quyết định hoặc hành động của PI); **NOT READY** (còn lỗi tôi chủ động xử lý được). Không tuyên bố READY khi còn điều kiện chưa xác minh.

Thứ tự ưu tiên: (1) báo cáo khoa học: ghép, kiểm tra, dựng DOCX và PDF, gửi PI; (2) bài B: chấm cặp xong trước 18:00 ngày 15/11, bước H trước 12:00 ngày 16/11; (3) bài C: dòng mốc khối 2 và bản cập nhật thứ nhất, dòng K7 từ 12:00 ngày 16/11 và bản cập nhật thứ hai; (4) bản TAIMMA: ba giám khảo đọc, phản biện, chỉnh sửa, đủ sớm để PI nộp trước 18:59 ngày 3/12; (5) bài A: ứng dụng web trên localhost cho quy trình gán nhãn (xem dữ liệu, hiện mẫu, chọn và lưu nhãn, tiến độ, kiểm tra, xuất; quy trình người gán nhãn thứ hai độc lập; kiểm tra lưu trữ, khôi phục, xuất; không mất, không ghi đè nhãn), rồi người gán nhãn thứ hai, buổi bổ sung của PI, chạy mã, cập nhật Mục 6.7 và Phụ lục S11; (6) cập nhật báo cáo khi kết quả giữ kín được mở.

Nguyên tắc: ưu tiên theo hạn và mức phụ thuộc; chủ động làm mọi việc không cần chờ PI; ghi tiến độ, bằng chứng, lỗi và lý do BLOCKED; không giả định kết quả của việc chưa làm; không lặp lại bước đã xong. Được dừng chủ động khi mọi việc còn lại đều chờ PI hoặc chờ một mốc thời gian hay điều kiện đã đăng ký; khi dừng thì bàn giao việc đã xong, hạng mục BLOCKED, điều kiện chờ, thời điểm tiếp tục và hạn. Trạng thái chờ không phải là hoàn thành.

## Trạng thái từng hạng mục

| Hạng mục | Trạng thái | Đã xong | Còn lại (ai làm) | Hạn |
|---|---|---|---|---|
| Báo cáo khoa học | ĐÃ GỬI (02:25 ngày 15/11) | ghép đủ phần mở đầu, A, B, C, D, E; mọi phần qua kiểm tra số liệu và trích dẫn; PDF 196 trang và DOCX đã gửi PI | cập nhật lại khi kết quả giữ kín được mở và sau các bản cập nhật của bài C (Claude) | theo các mốc của từng bài |
| Bài B (LRE) | BLOCKED phần chấm; NOT READY phần văn bản | mọi bước chạy trên máy (13–14/11); PI chấm xong bộ chính (363 dòng, phiên đóng 06:31 ngày 15/11; không làm vòng làm quen, đã có phán quyết CC-404 và CC-406 về cách công bố); bản thảo viết lại xong ở trạng thái mặc định trong thư mục kín; 14/14 tài liệu mới đã xác minh | người chấm thứ hai (chưa trực tuyến; phải bắt đầu muộn nhất khoảng 15:30); dòng đóng; bước H trên máy thuê (PI đã cho phép thuê máy dự phòng nếu máy hỏng); ba hình (lần thuê sau K7); năm tài liệu kinh điển chưa đọc được; phần viết về chấm của người sau bước H | đóng chấm 18:00 ngày 15/11; bước H trước 12:00 ngày 16/11 |
| Bài C (TALLIP) | NOT READY | dòng mốc khối 2; bản cập nhật văn bản thứ nhất (6a5d36a); gói sửa lỗi từ báo cáo đã qua giám khảo và lưu vào kho (9b8e6ae, CC-405); tập lệnh cho bản cập nhật thứ hai đã soạn và qua lượt đọc trước (CC-402) | dựng lại PDF từ 9b8e6ae trên máy thuê tối 15/11; dòng K7 và bản cập nhật thứ hai; gói sửa tiếp theo (câu về số mục của OV-test, đánh lại số bảng); các câu C1, C2, C5 trong tệp gửi tác giả liên hệ | K7 từ 12:00 ngày 16/11 |
| Bản TAIMMA 2027 | NOT READY | bản thảo thứ nhất (14/11); ba giám khảo đã đọc (CC-399: không sai số liệu; 6 chỗ câu chữ phải sửa; 3 cổng kiểm) | bản thảo thứ hai đang soạn, rồi đọc phần khác biệt; dựng theo mẫu LNCS để đếm trang (12–15); chấm mù so với bài CCIS và đọc phản biện; đối chiếu lại sau K7; PI trả lời D2–D4, D6, D8, danh sách tác giả; PI tự viết lại và nộp | thông báo sẵn sàng sớm nhất 12:00 ngày 16/11; nộp trước 18:59 ngày 3/12 |
| Bài A (SPIC) | BLOCKED phần gán nhãn; NOT READY phần mã và hồ sơ nộp | PI gán nhãn xong bộ chính (14/11); ứng dụng gán nhãn tại http://localhost:8788/; gói sửa lỗi từ báo cáo đã qua giám khảo và lưu vào kho (dafba17, CC-403) | phiên từ xa của người gán nhãn thứ hai (150 ảnh, 1,110 câu hỏi); buổi bổ sung của PI (1,755 câu hỏi); chạy thử mã trên máy thuê tối 15/11; các phép phân tích đã đăng ký; cập nhật Mục 6.7 và Phụ lục S11; câu khai báo về KTVIC (chặn trước khi nộp) và các câu A1–A6 trong tệp gửi tác giả liên hệ; phần chính 18,780 từ so với 8,500 | không có hạn cứng |

Ngoài goal: **đề cương nghiên cứu sinh** v18.48 cùng kịch bản v18.49 đang chờ PI đọc (còn mở: câu 12, F15, F17, tháng bảo vệ cấp Trường).

## Kênh hỏi tác giả liên hệ

Từ 15/11 (PI-1114m, PI-1114n): câu hỏi mở được ghi vào `/mnt/d/RESPONSE_FROM_CORESSPONDING_AUTHOR.md` (29 câu, không chứa kết quả đang giữ kín); tác giả liên hệ trả lời ngay trong tệp; mỗi ý được cân nhắc theo bằng chứng trước khi áp. PI chỉ được hỏi khi việc chỉ PI làm được.

**07:03 ngày 15/11:** cả 29 câu đã có trả lời (OPS-1115a). Bảng đánh giá từng ý và ba câu hỏi tiếp theo (F1–F3) nằm ở cuối tệp. Việc đang làm từ các ý được chấp nhận: gói sửa lần 2 của bài A (câu khai báo về việc huấn luyện trên KTVIC) và của bài C (tóm tắt, câu về số mục và số ảnh, khuôn lời nhắc, đoạn giải thích ở Mục 5.4; áp sau bản cập nhật ngày 16/11); bản nháp bốn thư (`manuscript/letters_2026-11-15/`); bản nháp câu khai báo về công cụ AI cho từng nơi nhận. Bản đầy đủ của bài được giữ nguyên độ dài; phần rút gọn chỉ lập thành kế hoạch để PI dùng khi viết lại. Không áp: cột giá trị p hậu kiểm ở bài C. Chờ PI xác nhận: thứ tự nộp mới (TAIMMA, B, A, C), quy tắc dừng ngày 1/12 của TAIMMA, ai gửi thư, việc tải dữ liệu lên Zenodo.

**08:05 ngày 15/11:** bài A: lần sửa thứ hai đã lưu (kho bài, ea12e51; CC-407 bản sửa, đạt có điều kiện 87, khớp từng byte): câu khai báo việc huấn luyện trên KTVIC; các câu "đã đồng ý" của UIT-OpenViIC và PASCAL-50S giữ nguyên theo PI-1110o. Còn chặn việc nộp bài A: việc huấn luyện trên UIT-ViIC chưa được nêu (chờ PI), thuật ngữ nội bộ ở S11 (sau khi mở phần giữ kín), câu về văn bản xác nhận trong bản đăng ký PASCAL-50S (chờ PI). Bài C: gói sửa lần 2 đạt có điều kiện (CC-408 bản sửa, 88), áp sau mốc 12:00 ngày 16/11. Bài B: phiên từ xa của người chấm thứ hai mở từ 07:21 (OPS-1115c). Quyết định của PI trong ngày: nộp TAIMMA trước và sớm nhất có thể (PI-1115a); không gửi email nào (PI-1115b); câu khai báo công cụ AI: chờ PI đọc khảo sát (PI-1115d). Đang chạy: khảo sát khai báo AI, giám khảo đọc gói bước H (CC-409), bản sửa TAIMMA lần 2, gói dựng trên máy thuê, hai gói sửa nhỏ về tài liệu liên quan.

**11:56 ngày 15/11:** bài A ở 59648b7 (cách gọi dự đoán thứ tự, khai báo UIT-ViIC theo PI-1115i); bài C ở 55315ca, hai gói đã duyệt chờ mốc 16/11 (CC-408, CC-413); bản TAIMMA 2.1 (CC-414: còn đếm trang, đối chiếu sau mốc, chấm mù, lượt đọc cuối); bài B: phiên người chấm thứ hai mở, chưa có câu trả lời nào được lưu. Quyết định PI-1115i: không khai báo AI, không gửi thư, thứ tự nộp TAIMMA, B, A, C. Bản nháp goal mới để PI đặt: `manuscript/GOAL_MOI_2026-11-15.md`.

## Ràng buộc đang có hiệu lực

- PI là người chấm của bài B: không cho PI xem số liệu hay kết luận của nghiên cứu đang chạy của bài B cho tới khi PI đóng phần chấm của mình.
- Một số số liệu của bài A giữ kín cho tới khi buổi gán nhãn bổ sung của PI kết thúc.
- Trang gán nhãn đã đăng ký của bài A được giữ nguyên từng byte; ứng dụng gán nhãn mới chỉ bao quanh nó (tiến độ, kiểm tra, xuất), không hiện giá trị nhãn và không tính số liệu nào từ nhãn.
- Mỗi lúc chỉ một trang chấm trên máy của PI. Máy thuê chỉ dùng khi có việc đã duyệt, xoá ngay khi xong.
- Báo PI trước khi nhìn tập kiểm tra, đổi hướng chính của một bài, hoặc nộp.

Kế hoạch chi tiết sau khi gán nhãn xong: `manuscript/KE_HOACH_SAU_GAN_NHAN_2026-11-14.md`.
