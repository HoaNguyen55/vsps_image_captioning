# Việc PI phải tự làm trước khi nộp, theo từng bài (15/11/2026)

**Lập lúc:** 18:16 giờ Việt Nam ngày 15/11/2026 (11:16Z, đọc từ `date`). Tệp này không chứa kết quả nghiên cứu nào: không có kết quả của Mục 6.7 hay Phụ lục S11 bài A, cũng không có số liệu nào của bài B. Các thông báo "ready to review" sắp tới dẫn tệp này theo mã dòng (ví dụ T3, B2, A1).

**Nguồn:** `READY_AUDIT_A_2026-11-15.md`, `READY_AUDIT_B_2026-11-15.md`, `READY_AUDIT_C_2026-11-15.md` (các dòng BLOCKED), `GOAL_HIEN_TAI.md`, `KE_HOACH_GOAL_2026-11-15.md`, `cfp/TAIMMA_CONF_2026-11-13.md`, các mục "For the PI" của phán quyết CC-414 đến CC-421, và các dòng PI-1115a đến PI-1115p trong LOG. Ngoài ra có đọc: `cfp/VENUE_RECHECK_2026-11-15.md` (các dòng D15, D21, C7, C14, C15, C17), mục H của `conf_taimma_2027/WRITING_PLAN_C_TAIMMA_v1.md` (D1–D12), và §17 trong bản đăng ký bài B (mục PI-2, PI-3, PI-4, PI-6; CC-420 ghi PI-2, PI-3, PI-6 là chưa trả lời).

## Cách đọc bảng

- **Loại**
  - **(a)** Dữ kiện hoặc hành động chỉ PI cung cấp hay làm được. Agent không tự điền.
  - **(b)** Quyết định dành riêng cho PI: nộp bài, giấy phép, kho lưu trữ, công bố dữ liệu, tiền vượt hạn mức, và các quyết định bản đăng ký để dành cho PI (PI-2, PI-3, PI-6 của bài B). Cần PI nói "đồng ý" rõ ràng, độ tin cậy cao đến đâu cũng vậy (PI-1115k).
  - **(c)** Quyết định thường. Theo PI-1115k, khuyến nghị có độ tin cậy **trên 70%** được coi là đã duyệt nếu PI không phản đối. Điều phối viên xác nhận lại trước khi áp dụng.
- **Độ tin cậy** là ước lượng của người soạn tệp này, không phải của PI.
- **Chặn**
  - **RTR:** agent không hoàn tất được văn bản nếu thiếu mục này, nên thông báo "ready to review" phải chờ. Nếu thông báo vẫn gửi, nó phải ghi rõ mục còn treo.
  - **NỘP:** chỉ chặn bước nộp. Văn bản tạm giữ một chỗ đánh dấu cho tới lúc đó.
  - **—:** không chặn gì vì đã có mặc định hoặc câu thay thế.

## 0. Đã chốt, không hỏi lại

1. Không bản thảo nào có câu khai báo về công cụ AI, và không câu nào nói rằng không dùng AI (PI-1115c, PI-1115i mục 6).
2. Sự chấp thuận của tác giả các bộ dữ liệu là dữ kiện đã chốt: PASCAL-50S, UIT-OpenViIC, và KTVIC kể cả việc huấn luyện (PI-1026az, PI-1110o, PI-1115i mục 8).
   - Câu "đã đồng ý" đứng cạnh câu huấn luyện KTVIC (CC-416).
   - Bản ghi đính chính đứng cạnh bản đăng ký PASCAL-50S (b9d3deb).
   - PI không phải làm gì thêm.
3. Không ai trong các phiên gửi e-mail (PI-1115b). Các thư trong `letters_2026-11-15/` là tệp văn bản; tác giả tự quyết có gửi hay không.
4. Không viết thư cho ban tổ chức TAIMMA hay cho biên tập viên của bộ CCIS (PI-1115i mục 4). Thư L1 không dùng.
5. Thứ tự nộp: TAIMMA, rồi B, A, C (PI-1115i mục 9).
6. Tạp chí dự phòng của bài A là JVCIR (PI-1115i mục 9).
7. Việc huấn luyện trên tập huấn luyện UIT-ViIC được nêu trong bài A (PI-1115i mục 7).
8. D8 đã đóng: bản TAIMMA in công cụ count-matched precision của bài A trước, ghi công cho nghiên cứu đi kèm (PI-1115k (a)). CC-414 Q1 và mục mang sang của CC-421 vì vậy cũng đã đóng.
9. Dòng W2 của PI về phiên người chấm thứ hai bài B đã có (PI-1115n). Câu công bố R0 dùng đúng như CC-417 phán. Câu về vòng làm quen (R3) và câu nói người chấm thứ hai làm tại laptop của PI, theo lời PI, dùng mặc định "có" của CC-415 và CC-417.
10. PI viết lại mọi bài sau thông báo ready to review, rà ngay khi nhận thông báo, và tự nộp (PI-1115i mục 5 và 12).
11. Cổng chấm mù so với các bài CCIS (CC-414 Q2) giữ theo mặc định. Không cần PI trả lời.

## 1. Việc chung cho nhiều bài

| # | Việc | Vì sao cần | PI cần đưa hoặc quyết định gì | Khuyến nghị mặc định (độ tin cậy) | Loại | Chặn |
|---|---|---|---|---|---|---|
| G1 | Mở các trang quy định của nơi nhận bằng trình duyệt thường, lưu toàn trang (Ctrl+S) vào `manuscript/cfp/`. Agent không đọc được các trang này vì máy chủ chặn truy cập tự động. | READY_AUDIT A (A5-01, A5-03, A5-11, A5-13; các ý chỉ có trong trang hướng dẫn tác giả của SPIC). READY_AUDIT C §5 (C1–C20). KE_HOACH §5 (tiêu chí "yêu cầu nơi nộp" của A và C ở trạng thái BLOCKED cho tới khi PI lưu trang). PI-1115i mục 11 (PI xin đường dẫn). | Lưu các trang sau:<br>**SPIC:** https://www.sciencedirect.com/journal/signal-processing-image-communication/publish/guide-for-authors<br>**TALLIP và ACM:**<br>https://dl.acm.org/journal/tallip/author-guidelines<br>https://www.acm.org/publications/authors/submissions (kèm danh sách gói TAPS được chấp nhận)<br>https://dl.acm.org/journal/tallip/about<br>https://www.acm.org/publications/policies/new-acm-policy-on-authorship<br>https://dl.acm.org/journal/tallip/open-access<br>https://www.acm.org/publications/policies/prior-publication-policy | Lưu trang SPIC trước bài A. Lưu các trang ACM trước khi **nộp TAIMMA**, vì chính lần nộp hội nghị tạo ra "công bố trước" cho TALLIP (WRITING_PLAN mục G, ghi chú 1). (95%) | (a) | A: RTR. C: RTR. TAIMMA: NỘP (trang chính sách công bố trước và điều khoản mở rộng của TALLIP) |
| G2 | Báo ngày nộp và mã số bài của từng bài ngay khi nộp. Báo kết quả TAIMMA ngay khi nhận (đợt 2: 10/12; đợt 3: 25/12). | Câu "related manuscripts" và thư gửi biên tập đổi theo trạng thái của các bài khác: A4-03 (bài A), mục 41 (bài B), mục 15 (bài C). Khi TAIMMA nhận bài, bài C bắt buộc có câu về bản hội nghị (READY_AUDIT C §5). | Một dòng mỗi lần: tên bài, ngày nộp, mã số; với TAIMMA thêm kết quả. | — | (a) | NỘP (của bài nộp sau) |
| G3 | Viết lại và rà ngôn ngữ toàn văn | Quy tắc thường trực: PI viết lại sau thông báo ready. LRE trả bài không qua phản biện nếu tiếng Anh không đạt (READY_AUDIT B mục 14). | Bản viết lại. Agent đối chiếu lại số liệu, nhãn đã đăng ký và giới hạn trang trước khi PI nộp. | Mỗi bài, gửi bản viết lại cho agent đối chiếu trước khi nộp. (90%) | (a) | NỘP |
| G4 | Kho lưu trữ Zenodo: tạo bản lưu, chọn chế độ truy cập, lấy DOI và đường dẫn cho phản biện | A: A5-07 (chưa có bản lưu nào; đường dẫn riêng đang là chỗ trống). B: mục 30 (CC-074: bản lưu chưa công khai cho tới khi có quyết định về bài A). C: mục 26. TAIMMA: D9. | Tạo bản lưu bằng tài khoản của nhóm. Quyết định khi nào công khai. Đưa DOI và đường dẫn cho agent. | Mỗi bài một bản lưu Zenodo, tạo trước khi nộp, để chế độ hạn chế truy cập kèm đường dẫn cho phản biện, công khai khi bài được nhận. Riêng bài B giữ chưa công khai tới quyết định về bài A (CC-074). TAIMMA giữ câu "available from the authors on request" cho tới camera-ready (10/1/2027). (75%) | (b) | NỘP |
| G5 | Số trang và DOI của bài FAIR 2026 trên IEEE Xplore | Bài B mục 36 và bài C mục 24: danh mục tài liệu đang in "[AUTHOR TO PROVIDE: pages and DOI …]". | Số trang và DOI khi IEEE Xplore có bài. | Nếu tới ngày nộp vẫn chưa có trên Xplore: bỏ phần ngoặc, giữ ISBN (READY_AUDIT C mục 24). (85%) | (c) | — |
| G6 | Khai báo trong hệ thống nộp: CRediT, xung đột lợi ích, tài trợ | A5-09 (tệp .docx về xung đột lợi ích của Elsevier, các ô CRediT và tài trợ). B mục 21 (LRE chỉ dùng thông tin gõ trong hệ thống). C mục 13. | Gõ vào biểu mẫu lúc nộp, cùng nội dung với bản thảo. | — | (a) | NỘP |
| G7 | Thư gửi tác giả dữ liệu và tác giả mã luận văn (L2 v2, L3, L4, hoặc thư gộp `L2_L4_MERGED_v2.md`) | Không ai trong các phiên gửi thư (mục 0.3). Riêng PI-3 của bài B: chỉ được dẫn sự cho phép về đầu ra baseline như một personal communication sau khi văn bản của sự cho phép đó được lưu (CC-092b R6, mục B3 dưới đây). | Các tác giả tự quyết gửi hay không, gửi lúc nào, và chọn hai thư hay thư gộp. Thư gộp chỉ dùng nếu một người trả lời cho cả bộ dữ liệu và kho mã (mục M-a trong tệp). | Không có khuyến nghị gửi hay không, vì đây là việc của tác giả. Thực tế cần biết: không có thư trả lời cho L4 trước hạn thì B3 rơi về mặc định. | (a) | — (chỉ ảnh hưởng nhánh B3) |

## 2. Bản TAIMMA 2027 (bài C, hội nghị), nộp đầu tiên

Theo CC-414 Q3, trước thông báo READY không còn gì cần PI. Thông báo sớm nhất lúc 12:00 ngày 16/11. Hạn nộp: đợt 2 là 18:59 ngày 21/11, đợt 3 là 18:59 ngày 3/12 (giờ Việt Nam).

| # | Việc | Vì sao cần | PI cần đưa hoặc quyết định gì | Khuyến nghị mặc định (độ tin cậy) | Loại | Chặn |
|---|---|---|---|---|---|---|
| T1 | Danh sách tác giả, thứ tự, tác giả liên hệ, đơn vị (D1) | Hội nghị phản biện một phía, tên phải có trong bài (TAIMMA_CONF §4). Thư của Springer: sau khi tệp đã gửi nhà xuất bản thì không đổi được tác giả (TAIMMA_CONF §8). Khối tác giả chiếm chỗ trong 15 trang (CC-421 Q3). | Danh sách đầy đủ, chậm nhất ngày 1/12. Bài đang in "[AUTHORS: to be set by the PI]". | — | (a) | NỘP |
| T2 | Lời cảm ơn và tài trợ (DECL-04), xung đột lợi ích (DECL-05), các dòng giấy phép | CC-421 Q3: phần chữ của PI chiếm 0,2 đến 0,4 trang trong một bài ước tính 14,4/15 trang. Thông báo READY sẽ ghi còn dư bao nhiêu chỗ và câu nào bị bỏ trước nếu không vừa (CC-421 Ruling 5). | Viết các câu đó, hoặc chỉ xác nhận bản agent chép lại từ dữ kiện tài trợ và xung đột lợi ích PI đã cung cấp trước đây. | Agent chép các dữ kiện PI đã cung cấp, viết ngắn nhất có thể; PI chỉ xác nhận. (75%) | (a) | NỘP |
| T3 | Nộp đợt nào (D4) | PI-1115a: nộp TAIMMA trước và sớm nhất có thể. Kế hoạch viết khuyến nghị đợt 3, vì đợt 2 để lại quá ít thời gian cho PI viết lại. | Chọn đợt 2 (18:59 ngày 21/11) hay đợt 3 (18:59 ngày 3/12). | Lấy đợt 3 làm hạn chắc chắn. Chỉ nộp đợt 2 nếu bản viết lại của PI và lượt đối chiếu lại xong trước ngày 20/11. (75%) | (c) | — |
| T4 | Phạm vi S1 (D2), bài đầy đủ 12–15 trang (D3) | Kế hoạch mục H. Chưa có câu trả lời trên hồ sơ, nên bản nháp đang theo mặc định. | Chỉ trả lời nếu muốn khác mặc định. | S1, bài đầy đủ. (85%) | (c) | — |
| T5 | Quyết định nộp hay không vào ngày nộp (D6) | Danh sách "CCIS Forthcoming Proceedings" của chính Springer (ngày 2/11/2026) có tên TAIMMA 2027 (VENUE_RECHECK D15). Trang hội nghị không nêu quy tắc rút bài (D21). Lựa chọn hỏi ban tổ chức đã bị loại (mục 0.4). | Nói "nộp" hoặc "không nộp" vào ngày nộp, khi đã có G1 (các trang ACM). | Nộp, nếu đến ngày đó danh sách của Springer vẫn còn tên hội nghị. (75%) | (b) | NỘP |
| T6 | Câu dẫn ba bài về chú thích ảnh tiếng Việt, trong đó có FAIR 2026, đã bị cắt (CC-421 Q1) | Hai quy tắc của PI gặp nhau ở đây: "mọi bài dẫn FAIR 2026" (PI-1102d) và "chỉ dẫn bài của mình khi cần về học thuật" (11/11). | Không cần trả lời. PI có thể tự đưa câu này lại khi viết lại. | Để cắt; khôi phục ở bước r2 nếu còn chỗ. (75%) | (c) | — |
| T7 | Bài không có hình, có bốn bảng (CC-421 Q2) | Đây là giá giữ cả hai ngôn ngữ và mọi dòng đã đăng ký trong 15 trang. | Không cần trả lời, trừ khi muốn bỏ phần tiếng Anh. Việc đó không được khuyến nghị và sẽ cần một phán quyết mới. | Giữ như hiện tại. (85%) | (c) | — |
| T8 | Tiêu đề bản hội nghị khác tiêu đề bài tạp chí (D11) | Hai bài trùng tiêu đề dễ bị hỏi ngay ở bàn biên tập (kế hoạch mục G, ghi chú 3). | Chỉ trả lời nếu muốn tiêu đề khác. | Bài tạp chí giữ tiêu đề hiện tại; bản hội nghị dùng tiêu đề làm việc hoặc tiêu đề của PI. (80%) | (c) | — |
| T9 | Tự nộp trên Microsoft CMT | PI-1115i mục 5. | Nộp tệp đã qua lượt đối chiếu lại (bản chụp và sha256 trước khi nộp). | — | (b) | NỘP |
| T10 | Giấy phép xuất bản của Springer, ký lúc camera-ready (10/1/2027) | Giấy phép độc quyền, có quyền dùng bài để huấn luyện AI. Bản tạp chí sau này cần ít nhất 30% nội dung mới, một câu nêu rõ phần mới, và câu ghi nhận công bố đầu "First published in …" (VENUE_RECHECK D27; READY_AUDIT C §5). | Đọc và ký nếu bài được nhận. | — | (a) | camera-ready |

## 3. Bài B (LRE), nộp thứ hai

Kết quả bài B đã được mở cho PI theo CC-418, nhưng tệp này không ghi số liệu nào. Bản viết lại đã được phép đưa vào kho bài sau hai bước kỹ thuật (CC-420). Theo CC-420, chưa phần nào sẵn sàng để nộp.

| # | Việc | Vì sao cần | PI cần đưa hoặc quyết định gì | Khuyến nghị mặc định (độ tin cậy) | Loại | Chặn |
|---|---|---|---|---|---|---|
| B1 | Dữ kiện về đạo đức và đồng thuận của người chấm | LRE yêu cầu ba điều: phê duyệt đạo đức hoặc lý do không cần; câu nêu đã có đồng thuận; đồng thuận được ghi nhận trước khi thu dữ liệu (READY_AUDIT B, mục E, 25–27). Ba câu đang in "không thu dữ liệu từ người" nay đã sai và phải thay (mục 24). CC-420 cũng hỏi điều này. | (i) Mỗi người chấm có bản đồng thuận ghi ngày, trước câu trả lời đầu tiên của người đó không? (ii) Có xin phê duyệt hoặc miễn phê duyệt đạo đức không? (iii) Đồng thuận của bộ chấm FAIR 2026 có bao lần dùng lại này không? | Trả lời đúng như sự việc, kèm ngày. Câu khai báo sẽ ghi đúng như vậy, không nhận là đã được phê duyệt, và không viết "documented prior to data collection" nếu điều đó không đúng. Không có mặc định, vì agent không được tự khẳng định các dữ kiện này. | (a) | RTR |
| B2 | PI-2: cách viết phát hiện về KTVIC đối với tác giả KTVIC | Đăng ký §17; CC-420: chưa trả lời, mặc định là bài không được nộp. Các phụ lục chuyển đổi đang chờ câu trả lời này. | Chọn cách viết. | Chỉ viết trung lập, theo dạng "điểm đã in được tái lập bằng quy trình X; với cách chấm thống nhất, giá trị là Y". Gửi thư cho tác giả KTVIC hay không là việc của tác giả (G7). (80%) | (b) | RTR |
| B3 | PI-3: in điểm f0 (cách chấm thống nhất) của hai baseline KTVIC | Đăng ký §17; CC-420. Việc này thay đổi câu "không hệ thống đã công bố nào được chấm lại". Sự cho phép bằng lời (CC-092b) chỉ được dẫn sau khi văn bản của nó được lưu (CC-092b R6). | Có hay không. | Có, chỉ dưới dạng điểm tổng hợp, có dẫn sự cho phép, không dùng lời xếp hạng. Điều kiện: có thư trả lời cho L4 (hoặc Phần 2 của thư gộp) trước hạn. Nếu không có: mặc định "tính nhưng không in". (75%) | (b) | RTR |
| B4 | PI-6: nêu kết luận chứng nhận (CERTIFIED, FRAGILE) cho hệ thống có tên của nhóm khác | Đăng ký §17; CC-420. Bài đang có câu "We rank no Vietnamese system". | Có hay không. | Có: nêu hệ thống bằng kho mã và commit, chỉ viết "phép so sánh X và Y được (không được) chứng nhận", không có bảng xếp hạng. Mặc định nếu PI không trả lời: chỉ đếm theo kho mã, không nêu tên. (75%) | (b) | RTR |
| B5 | Một dòng của chính người chấm thứ hai: đã trả lời một mình, không dùng công cụ AI, không tra cứu | CC-415 W7, CC-417, CC-418, CC-420 (cùng một yêu cầu). | Nhờ người chấm thứ hai viết một dòng đó. | Nên nhờ. Không có dòng này thì câu R0 chỉ dựa trên lời của PI, giữ nguyên như CC-417 đã phán. Có dòng này thì R0 được đọc "…the author and the rater". Đây là câu về cách người chấm trả lời, không phải câu khai báo AI của bài. (85%) | (a) | — |
| B6 | Chấp nhận phần chấm của người như đã chạy theo đăng ký | CC-418: chấm lại, thêm người chấm thứ ba, hay thêm quy tắc mới đều sẽ là một nghiên cứu mới. | Không cần trả lời nếu đồng ý. | Chấp nhận như hiện có. (90%) | (c) | — |
| B7 | Lưu `key.json` và hai tệp nhãn vào kho riêng (không chứa văn bản chú thích), để giữ an toàn | CC-418. | Có hay không. | Có, theo khuyến nghị của CC-418. Mặc định nếu không trả lời: không lưu vào kho, giữ cùng các bản 444. (75%) | (c); điều phối viên hỏi PI một lần trước khi lưu, vì không gỡ được khỏi lịch sử git | — |
| B8 | Một dòng về cách PI đã trả lời trên trang chấm (dùng bàn phím, tốc độ) | CC-418: thời gian hiển thị trên màn hình trong cả hai tệp chấm chưa giải thích được. Bài sẽ in đúng như số đã ghi. | Một dòng, nếu PI biết. | Không bắt buộc. | (a) | — |
| B9 | Giấy phép của bộ công cụ (kit) | READY_AUDIT B mục 31. Bài đang ghi "MIT [AUTHOR TO CONFIRM: licence]". | Xác nhận hoặc chọn giấy phép khác. | MIT cho mã. Điều khoản của từng tệp dữ liệu dẫn xuất giữ theo bộ dữ liệu gốc, như bài đã viết. (80%) | (b) | NỘP |
| B10 | Công bố câu trả lời của người chấm | READY_AUDIT B mục 32. Special Focus yêu cầu tài nguyên công khai, hoặc nêu lý do không công khai. Mục 8 trong các quyết định của bài B. | Công bố (mã câu hỏi, mã ảnh, tên tệp, câu trả lời; không có văn bản chú thích) hay chỉ công bố thống kê tổng hợp. | Công bố dạng đó sau dòng đóng, nếu cả hai người chấm đồng ý bằng văn bản. Mặc định: chỉ công bố thống kê tổng hợp và nêu lý do trong bài. (70%) | (b) | NỘP |
| B11 | Lời cảm ơn trên trang tiêu đề | READY_AUDIT B mục 45 (LRE đặt lời cảm ơn ở trang tiêu đề); mục PI-4 (d). | Có cảm ơn người chấm thứ hai và các nhóm dữ liệu không; nêu tên hay chỉ nêu vai trò. | Chỉ nêu vai trò, trừ khi người đó đồng ý bằng văn bản cho nêu tên. (85%) | (c) | — |
| B12 | Hình thức bài viết lại: nghiên cứu điểm kiểm tra đối tượng chuyển sang phụ lục; các phần khác của hướng cũ chuyển sang Online Resource; tiêu đề làm việc (a); không thêm phần so sánh tiếng Anh | Mục 5, 6, 7 và 9 trong các quyết định của bài B. Chưa có câu trả lời trên hồ sơ, nên mặc định đang áp dụng. | Chỉ trả lời nếu muốn khác. PI có thể đổi khi viết lại. | Theo mặc định của từng mục. (80%) | (c) | — |
| B13 | Độ dài và tóm tắt khi viết lại | READY_AUDIT B mục 2: LRE ghi "typically 18–25" trang và không có giới hạn cứng; bản dựng cũ dài 29 trang. CC-420: tóm tắt đã cắt còn 250 từ. | Quyết định cắt hay giữ độ dài khi viết lại. | Được viết lại câu chữ của tóm tắt, nhưng mỗi nhãn đã đăng ký và các số đếm đi kèm phải giữ nguyên (CC-420). | (a) | NỘP |

Các ý agent tự làm, không cần PI: mô tả mô hình ngôn ngữ và mô hình thị giác–ngôn ngữ trong Methods (mục 23), chỉnh khối Declarations, các DOI còn thiếu, tên "Online Resource", sửa script dựng.

## 4. Bài A (SPIC), nộp thứ ba

Kết quả Mục 6.7 và Phụ lục S11 chỉ đến tay PI sau khi buổi gán nhãn bổ sung của PI kết thúc (CC-419). Tệp này không dẫn PI tới tệp nào của bài A.

| # | Việc | Vì sao cần | PI cần đưa hoặc quyết định gì | Khuyến nghị mặc định (độ tin cậy) | Loại | Chặn |
|---|---|---|---|---|---|---|
| A1 | Phiên của người gán nhãn thứ hai (150 ảnh, 1.110 câu hỏi) | READY_AUDIT A1-01. Goal §2 mục 4. KE_HOACH nhiệm vụ 6 (mở phiên ngay sau khi bài B đóng phần chấm; PI-1115k (f)). | Sắp xếp người gán nhãn. Khi điều phối viên mở phiên, chuyển đường dẫn và tin nhắn cố định cho người đó. Không nhìn màn hình, không giải thích. Nếu phán quyết của phiên yêu cầu, gửi một dòng xác nhận như dòng W2 của bài B. Làm rõ một điểm: PI-1115i mục 10 ghi PI nói người gán nhãn thứ hai "đang làm" khi chưa có phiên nào của bài A được mở; PI cho biết ai đã làm gì và lúc nào. | Mở phiên sớm nhất có thể. (90%) | (a) | RTR |
| A2 | Buổi gán nhãn bổ sung của PI (1.755 câu hỏi) | READY_AUDIT A1-01. Mã phân tích đã qua lần kiểm thử trên máy thuê (CC-419) và chờ dòng kết thúc buổi này. | Tự gán nhãn trên ứng dụng gán nhãn (http://localhost:8788/). | Làm sau phiên A1, như thứ tự trong KE_HOACH. (85%) | (a) | RTR |
| A3 | Lưu trang hướng dẫn tác giả của SPIC (G1) | Các ý chỉ có trong trang này: giới hạn tóm tắt (bài đang đúng 250 từ), số từ khoá (đang 7), kiểu tài liệu tham khảo và cách viết tắt tên tạp chí theo LTWA, giới hạn độ dài, CRediT có bắt buộc không, Option C cho dữ liệu, highlights có cần ở lần nộp đầu không (A5-01, A5-03, A5-11, A5-13, A5-05, A5-07, A5-09). | Lưu trang (đường dẫn ở G1). | — | (a) | RTR |
| A4 | Bản lưu Zenodo hạn chế truy cập và đường dẫn (G4) | A5-07: chưa có bản lưu nào; trang tiêu đề và thư gửi biên tập đang để trống đường dẫn riêng. | Tạo bản lưu và đưa đường dẫn. | Như G4. (75%) | (b) | NỘP |
| A5 | Cắt độ dài khi viết lại | A5-13: phần chính khoảng 19.265 từ, so với mục tiêu riêng của nhóm là 8.500. Hướng dẫn chưa đọc được nên chưa rõ có giới hạn của tạp chí không. | Quyết định cắt bao nhiêu, làm **sau khi buổi gán nhãn bổ sung đã đóng**. Danh sách phần có thể chuyển sang phụ lục sẽ đi kèm thông báo ready to review. | Cắt theo danh sách đó. Nếu trang hướng dẫn có giới hạn thì theo giới hạn đó. (70%) | (a) | NỘP |
| A6 | Câu về các bản thảo liên quan | A4-03: lúc nộp A, bài B đã ở LRE và bản TAIMMA đã nộp, nên các câu này phải theo trạng thái thật. | Ngày nộp của B và TAIMMA (G2). | — | (a) | NỘP |

Khai báo trong hệ thống nộp: xem G6. Địa chỉ, e-mail, ORCID: xem phần 6.

## 5. Bài C (TALLIP), nộp cuối

Bài C còn chờ chuỗi việc đã lên lịch: mốc 12:00 ngày 16/11 (C2), gói v2, gói v4, kế hoạch cắt, dựng lại. Các việc đó không cần PI.

| # | Việc | Vì sao cần | PI cần đưa hoặc quyết định gì | Khuyến nghị mặc định (độ tin cậy) | Loại | Chặn |
|---|---|---|---|---|---|---|
| C1 | Lưu các trang ACM và TALLIP (G1) | READY_AUDIT C §5: mọi quy tắc C1–C20 còn BLOCKED, gồm tiêu đề, tóm tắt, CCS, kiểu trích dẫn, thống kê, hình, loại bài và độ dài, điều khoản mở rộng. | Lưu trang (đường dẫn ở G1). | — | (a) | RTR |
| C2 | Thời điểm nộp TALLIP và cách nói về bản hội nghị (D7; mục 15) | Hội nghị yêu cầu bài "not under review elsewhere". Chính sách ACM về nộp đồng thời chưa đọc được. Nếu TAIMMA nhận bài, bản tạp chí cần ít nhất 30% nội dung mới, một câu nêu rõ phần mới, và câu "First published in …" (READY_AUDIT C §5). | Đồng ý thời điểm. | Chỉ nộp TALLIP sau khi có kết quả TAIMMA (chậm nhất 25/12). Nêu phần trùng và phần mới (nghiên cứu attribution, Flickr30K, phụ lục đầy đủ) trong bài và trong thư gửi biên tập. (90%) | (c) | NỘP |
| C3 | Tác giả và đơn vị trong khối tác giả (mục 11, 14) | Bài đang in chỗ trống "[AUTHOR TO PROVIDE: authors, affiliations, ORCID]" ở trang 1 và ở mọi đầu trang. | Cùng danh sách như T1, trừ khi PI muốn khác. | Dùng danh sách của T1. (85%) | (a) | NỘP |
| C4 | Chế độ ẩn danh (mục 12; C7) | Phải đọc biểu mẫu ScholarOne mới biết, và biểu mẫu cần tài khoản của PI. | Đọc biểu mẫu và báo lại: ẩn danh một chiều hay hai chiều. | Tới lúc đó giữ khối tác giả ẩn danh và cách tự dẫn ở ngôi thứ ba. Nếu là hai chiều, sửa cụm "by the same group" ở phần mở đầu. (80%) | (a) | NỘP |
| C5 | Tài trợ, xung đột lợi ích, CRediT, đạo đức (mục 13; C15) | Đọc trang ở G1 xong mới biết cần câu nào. | Xác nhận sau khi đọc trang. | Agent chép các dữ kiện PI đã cung cấp (như T2); PI chỉ xác nhận. Bài C không có người tham gia nên ghi "không áp dụng" cho phần đạo đức. (75%) | (a) | NỘP |
| C6 | Định dạng thống kê (mục 5; C10) | Theo trả lời F3, chỉ thêm giá trị p nếu hướng dẫn hoặc biên tập yêu cầu, và phải có PI đồng ý. | Chỉ trả lời nếu trang hướng dẫn yêu cầu giá trị p. | Không thêm giá trị p; đoạn C-V04 (vì sao dùng quy tắc khoảng tin cậy) đã lên lịch. (80%) | (c) | — |
| C7 | Độ dài sau kế hoạch cắt (mục 9) | Sau khi cắt còn khoảng 26.400 từ. Thẻ của tạp chí không ghi giới hạn tối đa. | Quyết định khi viết lại. | — | (a) | NỘP |
| C8 | Dữ liệu và mã: kho lưu (G4) và việc công bố điểm theo từng ảnh (mục 26; C5 (i)) | Câu về dữ liệu và mã đang kết thúc bằng một chỗ trống trong ngoặc. Bài hiện ghi rằng điểm theo từng ảnh không được công bố. | DOI và đường dẫn; có công bố điểm theo từng ảnh hay không. | Giữ như bài đang ghi (không công bố điểm theo từng ảnh). Đổi phần ngoặc thành câu thường; nếu kho chờ tới sau phản biện thì nói đúng như vậy. Nếu giữ lựa chọn này, xoá mệnh đề "scores per image" trong thư L2 v2 (mục L2-c). (75%) | (b) | NỘP |
| C9 | Thứ tự tên tác giả trong mục `Vu2025VELVET` (mục 25) | Bản ghi kiểm tra tài liệu đang ghi "PI to confirm". | Chỉ trả lời nếu biết cách chính tác giả viết tên mình. | Theo bản ghi Crossref. (80%) | (c) | — |

Số trang và DOI của FAIR 2026: xem G5.

## 6. Phần đuôi: việc hành chính, ưu tiên thấp

Các việc này làm lúc nộp. Mục nào có ghi "chặn NỘP" thì bài không nộp được nếu thiếu.

- **Địa chỉ bưu chính** của các tác giả. Bài A: trang tiêu đề và chữ ký thư gửi biên tập (A5-06). TAIMMA: khối tác giả (T1). Chặn NỘP.
- **E-mail** của tác giả liên hệ và tác giả thứ hai: trang tiêu đề và thư gửi biên tập của A và B (A5-06; B mục 43). Theo quy tắc thường trực, PI tự điền lúc nộp và e-mail không lưu trong kho. Bài B: bản dựng Online Resource (ESM_1) cần e-mail mới chạy được (mục 38). Chặn NỘP.
- **ORCID** của các đồng tác giả. A: hiện chỉ có ORCID của tác giả thứ nhất. B: thư gửi biên tập cần ORCID, trang cá nhân hoặc CV của đồng tác giả (39b). C: ORCID bắt buộc với tác giả nộp bài (C14). Agent không tra hay tự đặt ra. Chặn NỘP.
- **Tài khoản** trên hệ thống nộp: Microsoft CMT (TAIMMA), ScholarOne (TALLIP), và hệ thống của SPIC và LRE. Chặn NỘP.
- **TAIMMA: dự trực tuyến hay trực tiếp (D5) và phí đăng ký**, chỉ khi bài được nhận, hạn 10/1/2027. Giá sớm: trực tuyến USD 155, trực tiếp USD 380. Khuyến nghị: trực tuyến. (80%, loại (c))
- **Đề cương nghiên cứu sinh** v18.48 và kịch bản v18.49 (không liên quan việc nộp bài): còn mở câu 12, F15, F17 và tháng bảo vệ cấp Trường (GOAL_HIEN_TAI).

## 7. Đếm

| Bài | Mục chặn RTR | Mục chỉ chặn NỘP | Mục không chặn |
|---|---|---|---|
| TAIMMA | 0 (CC-414 Q3) | T1, T2, T5, T9; G1 (trang ACM), G2, G3, G6; T10 lúc camera-ready | T3, T4, T6, T7, T8 |
| B | B1, B2, B3, B4 | B9, B10, B13; G2, G3, G4, G6 | B5, B6, B7, B8, B11, B12; G5, G7 |
| A | A1, A2, A3 (G1) | A4 (G4), A5, A6; G3, G6 | — |
| C (TALLIP) | C1 (G1) | C2, C3, C4, C5, C7, C8; G2, G3, G4, G6 | C6, C9; G5 |
