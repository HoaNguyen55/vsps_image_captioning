# Phần B. Tính hợp lệ của bộ chuẩn đánh giá trong sinh chú thích ảnh tiếng Việt: kiểm định KTVIC, phiếu giao thức và bộ công cụ đánh giá (Benchmark validity in Vietnamese image captioning: a KTVIC audit, protocol card and evaluation kit)

**Cách đọc Phần B (cập nhật ngày 15/11/2026).** Phần B gồm hai lớp, và người đọc cần biết mình đang ở lớp nào. Các mục B.14 đến B.28 mô tả bài báo như hiện nay: bản thảo viết lại, lưu trong kho bài báo ở thư mục `paper/rev_2026-11-15/`, với tên mới, câu hỏi mới và một nghiên cứu đã đăng ký mới gồm cả phần đánh giá của con người; kết quả của nghiên cứu ấy đã được công bố cho nhà nghiên cứu. Các mục B.1 đến B.13 (trừ B.1.8) mô tả văn bản trước đó, tức các tệp `sec1`–`sec8` và `supplementary_B.md`; chúng được giữ nguyên vì phần lớn nội dung ấy nay là Online Resource 2 của bản thảo viết lại, nhưng tên bài, tóm tắt, các đóng góp và các khẳng định nêu ở đó không còn là của bài báo hiện nay. Nguồn của B.14 đến B.28 là `paper.md`, `online_resource.md` và bảng kê số liệu `number_manifest_B_v2.tsv` của bản thảo viết lại. Mục B.1.8 cho biết hai lớp này nối với nhau như thế nào.

Quy ước trình bày của phần này như sau. Mọi số liệu được chép nguyên dạng in trong bài (dấu chấm thập phân, dấu phẩy ngăn cách hàng nghìn, cùng số chữ số, cùng dạng khoảng). Phán quyết đã đăng ký được giữ nguyên bằng tiếng Anh trong ngoặc kép rồi mới giải thích bằng tiếng Việt. Các hàng hậu nghiệm (POST HOC), thăm dò (exploratory) hoặc chỉ trên dữ liệu phát triển (development only) giữ nguyên nhãn và không kèm phán quyết. Nguồn là thư mục bài báo ở trạng thái đã commit: các tệp mục `sec1`–`sec8`, phụ lục `supplementary_B.md`, `outline_B.md` (nơi chứa tóm tắt), bảng kê số liệu `number_manifest_B.tsv`, và hai tệp đăng ký trước của nghiên cứu ở Mục 5.3 khi cần nguyên văn quy tắc. Bài hầu như không in công thức: công thức (B.1) chép phép tính của Mục 3.2; các công thức (B.2), (B.3), (B.4) và (B.7) viết lại bằng ký hiệu những định nghĩa mà bài nêu bằng lời; các công thức (B.5) và (B.6) lấy từ hai tệp đăng ký trước. Bài không có tệp hình nào.

## B.1 Thông tin chung

### B.1.1 Tên bài, nơi gửi và các giới hạn do thư mục bài ghi nhận

Bài có tên tiếng Anh như ở tiêu đề phần này, được ghi thống nhất trong `title_page_B.md`, `outline_B.md` và thư gửi ban biên tập. Trang tên bài liệt kê ba tác giả với ba đơn vị công tác; tác giả đứng thứ ba là tác giả liên hệ; mã ORCID mới chỉ có cho tác giả thứ nhất, còn địa chỉ thư điện tử đã được lược khỏi bản lưu trong kho. Tạp chí đích là Language Resources and Evaluation (Springer). Thư gửi ban biên tập đề nghị xét bài trong chuyên mục Special Focus dành cho ngôn ngữ ít tài nguyên (less-resourced languages), với lý do tiếng Việt là ngôn ngữ ít tài nguyên trong nghiên cứu thị giác–ngôn ngữ và phép kiểm định đo xem các đặc điểm của tiếng Việt (tách từ so với tách theo âm tiết, dấu thanh, danh từ loại thể trong so khớp đối tượng) làm thay đổi ý nghĩa của một điểm số như thế nào.

Các giới hạn của tạp chí mà thư mục bài ghi lại gồm: tóm tắt dài 150–250 từ; độ dài bài thường trong khoảng 18–25 trang; phản biện kín một chiều (single-blind); thư gửi ban biên tập phải có mã ORCID hoặc trang cá nhân tại trường, lý lịch trực tuyến của từng tác giả; phần Statements and Declarations phải đứng ngay trước danh mục tài liệu tham khảo; không dùng chữ viết tắt chưa định nghĩa; phụ lục nộp dưới dạng Online Resource 1. Về quan hệ với bản hội nghị, `outline_B.md` ghi rằng áp dụng điều khoản chung của Springer về "expansion of previous work", phải công bố bài FAIR 2026 và có "≥ 30% new". Thư mục không ghi tên loại bài theo phân loại chính thức của tạp chí; các tệp trạng thái mô tả bài là một bài tài nguyên theo hướng kiểm định và bộ công cụ (audit-and-kit resource paper). Từ khoá do `outline_B.md` ghi là: Vietnamese image captioning; benchmark validity; dataset audit; evaluation protocol; reporting practice; CIDEr.

### B.1.2 Điều bài báo khẳng định

Tóm tắt đặt vấn đề rằng sinh chú thích ảnh (image captioning) tiếng Việt là bối cảnh ít tài nguyên: một vài bộ chuẩn đánh giá (benchmark) nhỏ gánh phần lớn bằng chứng, và các hệ thống được so sánh chủ yếu bằng CIDEr trên KTVIC. Câu hỏi của bài là một điểm CIDEr trên KTVIC, và một mức tăng của nó, thực sự đo điều gì. Phép kiểm định (audit) cho thấy năm chú thích tham chiếu (reference) của mỗi ảnh đến từ một người viết, với tỉ lệ kề nhau (adjacent share) 0.7102 so với 0.40 dưới giả thiết hoán đổi được (exchangeability). Thêm một dấu chấm, thứ mà không tham chiếu nào có, làm mất 35.17 điểm ở quy trình chấm bỏ bước loại dấu câu của Penn Treebank và không mất điểm nào ở quy trình giữ bước đó. Cách tách từ làm điểm thay đổi 15.64 điểm. Với một mô hình Qwen2.5-VL-7B đã tinh chỉnh (một mô hình nền), mỗi lần nhân đôi số ảnh huấn luyện KTVIC làm CIDEr-D (×100) tăng +9.61 [7.18, 12.36] trên 300 ảnh phát triển (đã đăng ký); đây là kết quả ở mức phát triển và việc khẳng định cần một lần nhìn duy nhất trong tương lai trên dữ liệu chưa thấy. Bài công bố một phiếu giao thức (protocol card) và một bộ công cụ đánh giá (evaluation kit) mở để chạy lại phép kiểm định trên dữ liệu của người đọc.

### B.1.3 Các đóng góp theo lời bài báo

Mục 1 của bài nêu ba đóng góp. Thứ nhất là một phép kiểm định tính hợp lệ của bộ dữ liệu KTVIC (Mục 3), gồm ba tính chất nêu ở B.2 và độ nhạy theo cách tách từ. Thứ hai là một phiếu giao thức (Mục 4.2) ghi rõ bộ tách từ, biến thể CIDEr, thang điểm, cách xử lý dấu câu và bộ so khớp đối tượng (object matcher) cho mọi điểm số, được áp dụng cho một hệ thống có kiểm soát mà điểm đã commit được một máy thứ hai tái lập đúng từng byte. Thứ ba là một bộ công cụ đánh giá (Mục 3.6): bộ chấm điểm và phiếu giao thức, mã so khớp, các tập lệnh chia dữ liệu và các tập lệnh kiểm định, dưới giấy phép mã nguồn mở; mỗi phép kiểm định của Mục 3 có một tập lệnh trong bộ công cụ (Bảng S13.2), chạy trên bản dữ liệu và đầu ra hệ thống của chính người đọc. Bộ công cụ chứa danh sách từ của bộ so khớp do tác giả xây dựng (v1 và v2), không chứa số đếm nào suy ra từ KTVIC, không chứa chú thích của bộ dữ liệu, và không chứa các quy tắc v3 chưa được người kiểm chứng.

### B.1.4 Những điều bài báo không khẳng định

Bài tuyên bố không khẳng định kết quả tốt nhất (state of the art) trên KTVIC và không báo cáo điểm của hệ thống tiếng Việt đã công bố nào dưới giao thức của mình để so sánh: đầu ra công khai của hai hệ thống cơ sở KTVIC chỉ đi vào tương quan thứ hạng ở Mục 3.4 và phép kiểm định dấu câu ở Mục 3.3; ba hệ thống bên ngoài ở Mục 3.6 chỉ được chấm mô tả, mỗi hệ thống trên tập kiểm tra của riêng nó, không so với nhau và không so với hệ thống của bài. Điểm 136.0 của GRIT đến từ một giao thức khác. Bài không khẳng định gì về đánh giá của con người đối với chất lượng chú thích vì không thu thập chú thích mới của con người. Nhãn và phiếu bầu do mô hình sinh ra chỉ là thành phần của phương pháp, không bao giờ là bằng chứng.

### B.1.5 Sơ đồ các mục của bài

**Bảng B.1.** Sơ đồ mục của bài theo `outline_B.md` (cột "So với FAIR" là đánh giá của chính tệp đó) và vị trí tương ứng trong phần báo cáo này.

| Mục của bài | Tệp | Nội dung | So với FAIR | Mục báo cáo |
|---|---|---|---|---|
| Tóm tắt, tên bài | `outline_B.md` | tên bài và tóm tắt | mới | B.1 |
| 1 | `sec1_intro.md` | vấn đề, các phát hiện kiểm định, đóng góp, quan hệ với FAIR 2026 và bài song hành | viết lại | B.2 |
| 2 | `sec2_related.md` | dữ liệu và hệ thống tiếng Việt; chấm không tham chiếu; mô hình thị giác–ngôn ngữ; độ đo dựa trên tham chiếu; tính độc lập của tham chiếu | mới | B.3 |
| 3 | `sec3_data_and_audit.md` | kiểm định KTVIC: một người viết, dấu câu, tách từ, bộ so khớp v1/v2/v3; bộ công cụ, ba hệ thống bên ngoài, tính sẵn có của dữ liệu | mới | B.4 |
| 4 | `sec4_system.md` | công cụ đo (zero-shot, P1, P1-R, fuse2), phiếu giao thức, các cổng tái lập | phần lớn mới (công thức huấn luyện P1 lấy từ FAIR) | B.5 |
| 5 | `sec5_results.md` | hệ thống có kiểm soát trên KTVIC; UIT-ViIC; kích thước tập huấn luyện (dữ liệu phát triển) | mới | B.6 |
| 6 | `sec6_discussion.md` | điểm CIDEr trên KTVIC đo gì; khuyến nghị; bộ công cụ gắn với khuyến nghị | mới | B.7 |
| 7 | `sec7_limitations_ethics.md` | hạn chế, dữ liệu và phát hành, quan hệ với hai bài khác, nguồn gốc phân tích, các tuyên bố | mới | B.8 |
| 8 | `sec8_conclusion.md` | kết luận | mới | B.9 |
| S | `supplementary_B.md` | S1–S15: hồ sơ các phép thử phía phương pháp và hồ sơ của bộ công cụ | mới | B.10 |

Bài không có mục so sánh với dữ liệu tiếng Anh: Bảng S12.1 của phụ lục ghi ở hàng "English data" là "none" đối với bài này.

### B.1.6 Phân định với bài hội nghị FAIR 2026 và với bài báo song hành (Paper A)

Hai tệp `new_vs_FAIR.md` và `SEPARATION_FAIR_A.md` ghi cách bài này khác với bài hội nghị trước của cùng nhóm tác giả [@nguyen2026vsps] và với bài báo song hành đang soạn [@companion2026underreview]. Ba bài đặt ba câu hỏi khác nhau. Bài FAIR 2026 hỏi liệu giám sát từ các mệnh đề đã kiểm chứng (phương pháp VSPS) có giảm ảo giác trong chú thích chi tiết tiếng Việt hay không, với bằng chứng chính là phương pháp VSPS, hệ đối chứng P1 và đánh giá của người chấm. Bài song hành hỏi khi nào một điểm ảo giác ở mức đối tượng đủ để so sánh hai hệ thống, trên XM3600, UIT-ViIC, COCO, Flickr30k và UIT-OpenViIC (số tổng hợp), và không có số chính nào trên KTVIC. Bài này hỏi một điểm KTVIC và một mức tăng của nó đo điều gì, với KTVIC là dữ liệu chính.

So với FAIR 2026, phần được dùng lại và đã công bố gồm: bối cảnh KTVIC/COCO và tập kiểm tra 558 ảnh; công thức QLoRA trên Qwen2.5-VL-7B; hệ zero-shot và hệ P1; điểm CIDEr 149.8 của P1 với hạt giống 42, chỉ dùng làm mốc tham chiếu chứ không phải khẳng định; bộ từ vựng đối tượng 113 mục, nay là bộ so khớp v1; và các trích dẫn công trình liên quan. Hai nhận định mà FAIR đã nêu (giá trị CHAIR trên KTVIC là cận trên vì tập chuẩn vàng lấy từ tham chiếu; độ chính xác của P1 đi kèm chú thích ngắn theo kiểu tham chiếu) được bài này thừa nhận. Kết quả âm của DPO 4-bit chỉ được trích dẫn. Phương pháp VSPS, bộ kiểm chứng, đánh giá của người chấm và việc trung tính hoá giới không được dùng. Cách chia tập huấn luyện cũng khác: FAIR dùng 3,700 ảnh huấn luyện và để riêng 69 ảnh, còn các hệ thống chính của bài này dùng cả 3,769 ảnh, và họ hệ thống có cổng phát triển dùng 3,469 ảnh cùng dev300. Về trùng lặp văn bản, `new_vs_FAIR.md` ghi phép đo trên một bản thảo cũ hơn (phần chính 9,946 từ, phụ lục 5,768 từ): tỉ lệ token nằm trong chuỗi chung với bản FAIR là 0.69% với n = 5 và 0.09% với n = 8; phép đo này không phát hiện diễn đạt lại. `SEPARATION_FAIR_A.md` ghi một lần kiểm sau đó: 3 chuỗi 8 từ chung trên 13,681, đều thuộc một câu gọi tên phương pháp của FAIR, và không có chuỗi 12 từ chung nào.

So với bài song hành, nguyên tắc là không có con số nào là kết quả chính ở cả hai bài (Bảng S12.1). Bài song hành chấm đầu ra của các hệ P1 và fuse2 huấn luyện trên KTVIC của bài này trên XM3600 và UIT-ViIC cho các khẳng định riêng của nó; bài này chỉ dùng các đầu ra ấy cho phép kiểm định dấu câu và chuyển miền. Các công cụ dùng chung gồm bộ chấm điểm, bộ so khớp v1/v2, các đối chứng khớp số lượng (count-matched controls) và thống kê hoán đổi được; trong đó các đối chứng khớp số lượng và thống kê hoán đổi được được định nghĩa và kiểm chứng ở bài song hành, bài này chỉ dùng như công cụ, còn phiếu giao thức và bộ công cụ đánh giá là đóng góp của bài này. Mỗi bài có kho lưu trữ riêng. Lần kiểm văn bản ghi trong tệp phân định cho 13 chuỗi 8 từ chung trên 15,578 và hai chuỗi 12 từ chung, sau đó hai chuỗi này đã được viết lại trong bài này. Bài này không có tệp hình và không dùng hình của bài song hành.

Thư gửi ban biên tập còn công bố một bản thảo liên quan thứ hai của cùng nhóm tác giả, cũng đang soạn, vốn chấm điểm bằng bộ công cụ của bài này, dùng chú thích huấn luyện của KTVIC và UIT-OpenViIC làm ví dụ trong lời nhắc, và dùng lại nửa thăm dò của tập kiểm tra KTVIC trong vai trò phát triển.

### B.1.7 Nhận xét rà soát về thông tin chung

Thứ nhất, tóm tắt hiện hành trong `outline_B.md` đếm theo khoảng trắng được 145 từ, tức ngắn hơn giới hạn dưới 150 từ mà chính thư mục bài ghi cho tạp chí; `STUDY_BRIEF_B.md` còn mô tả một tóm tắt 235 từ mở đầu bằng kết quả tích cực ở mức phát triển, không khớp với tóm tắt hiện hành. Thứ hai, tóm tắt viết phép kiểm định "shows" rằng năm tham chiếu đến từ một người viết, trong khi Mục 3.2 nói rõ bước suy từ thống kê sang "one writer" dựa vào tài liệu của KTVIC chứ không dựa riêng vào thống kê; tóm tắt cũng không nói con số 35.17 là của một hệ thống với một hạt giống và hàng "không mất điểm" là hậu nghiệm. Thứ ba, tóm tắt dùng thì hiện tại "We release", trong khi Mục 3.6, Mục 7.2 và Mục 7.5 còn các chỗ trống `[AUTHOR TO CONFIRM: licence]` và `DOI: [AUTHOR TO PROVIDE]`. Thứ tư, trang tên bài đã có ORCID của tác giả thứ nhất nhưng thư gửi ban biên tập vẫn để chỗ trống cho cả ba tác giả. Thứ năm, `outline_B.md` ghi tạp chí là Q1 còn `STUDY_BRIEF_B.md` ghi Q2; cần đối chiếu lại nguồn xếp hạng. Thứ sáu, dòng đầu của `outline_B.md` ghi rằng kết quả chính còn chờ quyết định định hướng, và tệp này cùng `STATUS.md`, `new_vs_FAIR.md`, `SEPARATION_FAIR_A.md` còn mô tả các phiên bản cũ (các nghiên cứu hai tập tham chiếu trên dữ liệu phát triển, phép kiểm định trùng ảnh KTVIC–OpenViIC, "Section 5.5", các bảng "S13.1" và "S14.2" theo số cũ) không còn trong văn bản hiện hành; trong danh sách kiểm của tệp phân định, bốn trên năm ô còn để trống. Thứ bảy, số trang 25 với dư khoảng một dòng trong `V2_PROGRESS_B.md` là của một lần dựng trước các thay đổi về sau (rút các nghiên cứu hai tập tham chiếu, thêm đoạn ở Mục 3.1, Mục 5.3 và Mục 6.2), nên cần dựng lại để biết số trang hiện tại.

### B.1.8 Bản thảo viết lại ngày 15/11/2026 và cách đọc Phần B

Bản thảo viết lại mang tên "Front-end validity of Vietnamese caption-score comparisons: a listed family, a per-comparison certificate and a registered application". Nó không còn hỏi một điểm CIDEr trên KTVIC đo điều gì, mà hỏi một phép so sánh hai hệ thống có cho cùng kết luận dưới mọi khâu xử lý văn bản đầu vào (front end) chấp nhận được hay không. Phép kiểm định KTVIC, hệ thống có kiểm soát, phiếu giao thức và các nghiên cứu đăng ký trước đây không bị bỏ: bản thảo mới chuyển chúng sang Online Resource 2 và ghi rõ rằng không nghiên cứu nào trong số đó là khẳng định của bài mới, còn mọi phán quyết đã đăng ký được chép nguyên. Vì vậy các mục B.2 đến B.10 vẫn là bản thuật lại đúng của phần nội dung ấy, và danh mục rà soát ở B.12 vẫn áp dụng cho phần văn bản được giữ lại. Bảng B.29 chép sơ đồ chuyển chỗ mà mục S.0 của Online Resource 2 nêu.

**Bảng B.29.** Vị trí mới của các mục thuộc văn bản trước, theo ghi chú đọc ở mục S.0 của Online Resource 2, và mục tương ứng của phần báo cáo này.

| Mục của văn bản trước | Vị trí trong bản thảo viết lại | Mục báo cáo |
|---|---|---|
| Mục 2 | S27 | B.3 |
| Mục 3.1 | S16 | B.4.1 |
| Mục 3.2 | S17 | B.4.2 |
| Mục 3.3 | Mục 3 của thân bài mới; hai đoạn về hai tập tham chiếu khác ở S18 | B.4.3 và B.17 |
| Mục 3.4 | Mục 3 của thân bài mới | B.4.4 và B.17 |
| Mục 3.5 | S19 | B.4.5 |
| Mục 3.6 | S28 và các tuyên bố về tính sẵn có trong thân bài mới | B.4.6 và B.24 |
| Mục 4 | S20 | B.5 |
| Mục 5.1 | S21 | B.6.1 |
| Mục 5.2 | S22 | B.6.2 |
| Mục 5.3 và Mục 6.3 | S23 | B.6.3 và B.7.3 |
| Mục 6.2 | S24 | B.7.2 |
| Mục 6.4 | S25 và Mục 7 của thân bài mới | B.7.4 và B.22 |
| Mục 7.1 | S26 | B.8.1 |
| Phụ lục S1 đến S15 | giữ nguyên lời văn, là phần đầu của Online Resource 2 | B.10 |

Ba điểm của các mục B.1 đến B.13 không còn đúng với bản thảo viết lại và cần được đọc cùng các mục mới. Thứ nhất, tên bài, tóm tắt, các đóng góp và sơ đồ mục ở B.1.1 đến B.1.5 là của văn bản trước; thông tin tương ứng của bản thảo viết lại ở B.14. Thứ hai, câu nói rằng bài không thu thập đánh giá mới của con người (B.1.4 và B.8) đã được thay: bản thảo viết lại có một phần đánh giá của con người, được thuật lại đầy đủ ở B.19.5 và B.21. Thứ ba, bảng đối chiếu khẳng định với bằng chứng của bản thảo viết lại là Bảng B.38 ở B.26, còn Bảng B.27 chỉ đối chiếu các khẳng định của văn bản trước.

## B.2 Mục 1 của bài: Mở đầu (Introduction)

**Nội dung.** Mục mở đầu xuất phát từ thực tế rằng các bộ chuẩn đánh giá công khai cho sinh chú thích ảnh tiếng Việt gồm UIT-ViIC [@lam2020uit], KTVIC [@pham2024ktvic], UIT-OpenViIC [@bui2026uit] và HDUCap [@hoang2026hducap], cùng một số tập cho miền hẹp hơn, và các hệ thống được so sánh trên đó chủ yếu bằng CIDEr. Trên KTVIC, một mô hình thị giác–ngôn ngữ (vision–language model, VLM) đã tinh chỉnh nay đạt điểm cao hơn nhiều so với hệ cơ sở transformer đã công bố: hệ tinh chỉnh chỉ tính mất mát trên phần trả lời của Qwen2.5-VL-7B do bài xây dựng đạt CIDEr-D mức từ 148.23 (độ lệch chuẩn 0.38 trên ba hạt giống), còn GRIT được báo cáo ở mức 136.0 dưới một giao thức mà bài không khớp được. Bài nhận xét rằng khoảng cách cỡ này dễ dẫn đến cách đọc kiểu bảng xếp hạng, và vì vậy đặt câu hỏi: một điểm CIDEr trên KTVIC, và một mức tăng của nó, đo điều gì, và bao nhiêu phần của chênh lệch giữa hai hệ thống là về hình ảnh. Ngay đoạn đầu, bài cũng nêu kết quả ở mức phát triển: với một mô hình nền, thêm dữ liệu huấn luyện KTVIC làm CIDEr-D so với tham chiếu KTVIC tăng +9.61 [7.18, 12.36] cho mỗi lần nhân đôi (Mục 5.3).

Lập luận về bối cảnh ít tài nguyên được dựng như sau. Phần lớn ngôn ngữ trên thế giới có ít dữ liệu gán nhãn so với tiếng Anh [@joshi2020state], và các ngôn ngữ Đông Nam Á vẫn được dữ liệu đa phương thức công khai bao phủ mỏng [@lovenia2024seacrowd]. Sinh chú thích ảnh tiếng Việt dựa trên vài bộ chuẩn, mỗi bộ từ vài nghìn đến khoảng mười lăm nghìn ảnh [@lam2020uit; @pham2024ktvic; @bui2026uit; @hoang2026hducap], và dữ liệu chú thích ở các ngôn ngữ ngoài tiếng Anh thường nhỏ hoặc được dịch từ tiếng Anh [@vanmiltenburg2024image; @hussain2026benchmarking]. Trong bối cảnh ấy một bộ chuẩn gánh phần lớn bằng chứng cho một hệ thống mới: một mức tăng mà ở tiếng Anh sẽ được kiểm chéo trên nhiều bộ dữ liệu thì ở đây thường chỉ được kiểm trên KTVIC. Vì những cộng đồng ngôn ngữ khác nhau, và những nhóm chú thích khác nhau, mô tả cùng một ảnh theo cách khác nhau [@buettner2024quantifying; @buettner2025multimodal; @berger2025crosslingual], giao thức viết tham chiếu của bộ chuẩn duy nhất ấy định hình điểm số của nó.

Câu trả lời của bài là một phép kiểm định bộ dữ liệu, dùng một hệ thống có kiểm soát làm công cụ đo, kèm một phiếu giao thức và một bộ công cụ đánh giá để người đọc chạy lại. Ba tính chất của KTVIC làm thay đổi câu trả lời.

Tính chất thứ nhất là năm tham chiếu của một ảnh đến từ một người viết. Giao diện chú thích của KTVIC yêu cầu một người chú thích nhập cả năm chú thích của một ảnh, với tổng cộng ba người chú thích [@pham2024ktvic]. Do đó các tham chiếu không phải là các lần rút độc lập. Trong số các đối tượng được đúng hai tham chiếu nêu, tỉ lệ nằm ở hai vị trí kề nhau là 0.7102 [0.6696, 0.7518], so với 0.40 nếu thứ tự hoán đổi được; một phân phối không theo hoán vị giữ nguyên tỉ lệ nêu đối tượng của từng vị trí cho 0.45 (hậu nghiệm; Mục 3.2).

Tính chất thứ hai là tham chiếu không có dấu câu cuối câu, được bài gọi là một rủi ro giao thức đã đo được mà cái giá của nó phụ thuộc vào quy trình chấm. Không tham chiếu nào trong 2,790 tham chiếu kiểm tra kết thúc bằng dấu chấm. Các độ đo dịch máy đã được chỉ ra là nhạy với một dấu câu cuối câu [@jwalapuram2023pulling], và hiệu ứng dấu chấm ở đây là hiện tượng tương ứng trong quy trình chấm chú thích ảnh. Bộ tách token PTB của pycocoevalcap xoá dấu câu trước khi chấm; một quy trình thay nó bằng bộ tách từ tiếng Việt, như bộ chấm đã commit của bài, thì mất bước xoá đó. Dưới quy trình như vậy, thêm một dấu "." vào mọi đầu ra của hệ tinh chỉnh chính P1-R (hạt giống 42), vốn không bao giờ kết thúc chú thích bằng dấu chấm, làm CIDEr-D giảm 35.17 điểm (−23.66%), còn đầu ra zero-shot, vốn kết thúc bằng dấu chấm, tăng từ 28.98 lên 33.30 khi dấu chấm bị gỡ. Với cách xoá kiểu PTB (hậu nghiệm), cả hai hiệu ứng bằng không và mô hình nền zero-shot đạt 34.97. Mã công khai của các hệ cơ sở KTVIC dùng bộ tách token PTB; bài không xác minh được quy trình nào đã tạo ra các điểm KTVIC đã công bố.

Tính chất thứ ba là điểm đối tượng phụ thuộc vào một bộ so khớp không được công bố. Việc chuẩn hoá dấu thanh, các danh từ loại thể như *cây* và các danh từ chỉ vai làm thay đổi việc một chú thích "nêu" những đối tượng nào. Bài mô tả ba phiên bản bộ so khớp; chỉ v1 và v2 đã được xác nhận, còn v3 là một tập quy tắc chưa có người duyệt nên chỉ được báo cáo như phân tích độ nhạy và không được phát hành.

Về mức tăng do dữ liệu huấn luyện, bài viết rằng trên 300 ảnh phát triển, mỗi lần nhân đôi số ảnh huấn luyện KTVIC làm CIDEr-D tăng +9.61 [7.18, 12.36], với phán quyết đã đăng ký "PASS". Đây là lần xác nhận ba hạt giống cho một kết quả phát triển một hạt giống trước đó (+9.40), và ngưỡng đạt (cận dưới của khoảng tin cậy lớn hơn +1) được đặt thấp hơn kết quả ấy. Kết quả dừng ở mức phát triển (một mô hình nền), và tập kiểm tra KTVIC đã đóng theo quy tắc một lần nhìn (one-look rule) của nhóm tác giả.

Sau ba đóng góp đã liệt kê ở B.1.3, mục mở đầu mô tả phép chạy bộ công cụ trên hệ thống bên ngoài: ngoài đầu ra công khai của hai hệ cơ sở KTVIC, nhóm tác giả đã chạy bộ công cụ trên 3 hệ thống bên ngoài từ 3 nguồn theo một bản đăng ký trước chỉ nhằm mô tả, tức ba checkpoint công khai, mỗi cái được nhóm giải mã một lần trên tập kiểm tra mà nó báo cáo và chấm dưới mọi cột giao thức. Bài nói rõ đây là một lần chạy của chính tác giả, chưa có nhóm bên ngoài nào chạy bộ công cụ, và các hàng chỉ mang tính mô tả: không hệ thống nào được xếp hạng hay so với hệ thống của bài. Các phép thử huấn luyện và giải mã chạy với cùng hệ thống được chuyển toàn bộ sang phụ lục với phán quyết không đổi. Hai kết quả thất bại được giữ lại trong thân bài: việc sửa dấu câu không làm đổi thứ hạng của bốn VLM công khai (Kendall τ_b = 1.0; dự đoán đã đăng ký "FAIL"; Phụ lục S4), và phép thử duy nhất đã đăng ký trước của hệ thống cuối cùng đã thất bại (Mục 5.1).

Đoạn về quan hệ với công trình trước nêu rằng bài hội nghị của cùng nhóm tác giả [@nguyen2026vsps] giới thiệu VSPS, đã báo cáo hệ đối chứng P1 trên KTVIC (hạt giống 42) như một hệ cơ sở, và đã ghi nhận hai điểm nêu ở B.1.6; bài này viết rằng mình "quantifies both points" và không kết quả chính nào của bài xuất hiện ở đó. Bài song hành [@companion2026underreview] nghiên cứu khi nào điểm ảo giác ở mức đối tượng hỗ trợ một phép so sánh giữa các hệ thống; nó không báo cáo số chính nào trên KTVIC nhưng chấm đầu ra của các hệ thống của bài này trên XM3600 và UIT-ViIC.

**Nhận xét rà soát.** Mục mở đầu nêu đúng phạm vi và giữ được các rào chắn quan trọng (không khẳng định kết quả tốt nhất, không có đánh giá của người, kết quả nhân đôi dữ liệu chỉ ở mức phát triển). Có sáu điểm cần xem lại.

Một là cách đếm không thống nhất giữa các chỗ: `sec1_intro.md` nói "Three properties of KTVIC change the answer" và đưa độ nhạy tách từ vào gạch đầu dòng đóng góp, Mục 6.1 nói "four sources of variation", còn sơ đồ mục trong `outline_B.md` ghi "four audit findings" cho Mục 1. Nên chọn một cách đếm và dùng xuyên suốt.

Hai là nguồn của con số 136.0. Bảng kê số liệu ghi nguồn của nó là Bảng I của bài FAIR 2026 ("GRIT ... as reported for KTVIC", trạng thái "literature (protocol not matched)"), tức một bảng trong bài trước của chính nhóm tác giả chứ không phải nguồn gốc. Vì con số này xuất hiện ở Mục 1, Mục 3.4, Mục 5.1, Mục 6.1 và Mục 8 như mốc để so độ lớn của các hiệu ứng, phản biện có thể yêu cầu trích trực tiếp nguồn gốc đã báo cáo điểm của GRIT trên KTVIC; văn bản hiện chỉ trích GRIT [@nguyen2022grit] ở Mục 2 mà không nói con số 136.0 được lấy từ đâu.

Ba là câu "This paper quantifies both points". Tệp `new_vs_FAIR.md` gắn việc định lượng điểm thứ nhất (CHAIR trên KTVIC là cận trên) với "the second panel (Section 5.3)", tức phần đã bị rút khỏi văn bản. Trong văn bản hiện hành, điểm này chỉ còn được đỡ gián tiếp bởi Mục 3.2 (tính nhất quán trong cùng một người viết) và Mục 5.2 (tập chuẩn vàng thứ hai trên UIT-ViIC). Cần kiểm tra xem chữ "quantifies" còn đúng cho cả hai điểm hay phải thu hẹp.

Bốn là các thuật ngữ được dùng trước khi định nghĩa: "one-look rule" và "development tier" xuất hiện ở Mục 1 và Mục 7.1 nhưng không nơi nào trong thân bài định nghĩa quy tắc một lần nhìn hay các mức bằng chứng; "gold-SFT" và "SFT" cũng không được giải thích.

Năm là sự căng giữa câu "now scores far above the reported transformer baseline" ở đoạn đầu và tuyên bố không khẳng định kết quả tốt nhất ở cuối mục. Bài đã tự rào bằng cụm "under a protocol we could not match", nhưng người đọc lướt vẫn có thể hiểu 148.23 so với 136.0 là một phép so sánh; nên đưa lời rào lên cùng câu.

Sáu là gạch đầu dòng về bộ công cụ viết "under an open-source licence" và "Each audit of Section 3 has a script in the kit", trong khi giấy phép còn chờ tác giả xác nhận và Bảng S13.2 chưa liệt kê tập lệnh của phép chạy hệ thống bên ngoài (xem B.4 và B.10).

## B.3 Mục 2 của bài: Công trình liên quan (Related work)

**Nội dung.** Mục 2 được tổ chức theo chín nhóm và một bảng so sánh.

Về các bộ dữ liệu chú thích tiếng Việt, UIT-ViIC [@lam2020uit] cung cấp chú thích tiếng Việt cho ảnh thể thao lấy từ COCO [@lin2014microsoft], do các người chú thích độc lập viết; ảnh kiểm tra của nó là ảnh COCO train2017. KTVIC [@pham2024ktvic] bao phủ miền đời sống với 4,327 ảnh và 21,635 chú thích; một người chú thích nhập cả năm chú thích của một ảnh. UIT-OpenViIC [@bui2026uit; @bui2023openviic] là bộ chuẩn miền mở lớn hơn, có giao thức nhập chú thích không được mô tả đủ chi tiết để biết các chú thích có độc lập hay không. HDUCap [@hoang2026hducap] thêm 15,000 ảnh cảnh tự nhiên, mỗi ảnh năm chú thích mà tác giả của nó mô tả là được viết độc lập, nhấn mạnh biểu thức không gian. Phần tiếng Việt của Crossmodal-3600 [@thapliyal2022crossmodal] cung cấp một tập tham chiếu viết độc lập mà bài dùng cho một phép kiểm dấu câu liên kho ngữ liệu; ảnh của nó đến từ Open Images. Ngoài ra còn có dữ liệu miền hẹp: thử thách VLSP 2021 VieCap4H về ảnh y tế [@le2022viecap4h] và một bộ chú thích chữ trong cảnh [@nguyen2026scenetext]; van Miltenburg tổng quan các bộ dữ liệu chú thích ngoài tiếng Anh [@vanmiltenburg2024image].

Về các hệ thống chú thích tiếng Việt, các kết quả KTVIC đã công bố đến từ các mô hình transformer; GRIT [@nguyen2022grit] là mốc được trích nhiều nhất cho KTVIC. Hai hệ thống gần đây liên quan trực tiếp là HDUCap [@hoang2026hducap] và ViG [@vu2026vig]. Với HDUCap, nhóm tác giả chỉ đọc được tóm tắt và bản xem trước của nhà xuất bản; với ViG, không lấy được toàn văn. Vì thế bài không biết cách chia dữ liệu, cách tách từ, biến thể CIDEr hay thang điểm của hai bài ấy, không báo cáo con số nào của chúng và không dùng chúng làm đối chứng; chúng chỉ trở thành đối chứng nếu giao thức khớp với giao thức của bài ở cả bốn điểm. Bài lưu ý rằng chỉ riêng cách tách từ đã làm CIDEr-D thay đổi nhiều hơn khoảng cách được báo cáo giữa hệ thống của bài và GRIT, và rằng hiệu ứng của biến thể CIDEr hay thang điểm chưa được đo.

Về chấm điểm không cần tham chiếu, CLIPScore [@hessel2021clipscore] chấm một chú thích so với ảnh bằng một mô hình ảnh–văn bản; với tiếng Việt cần một mô hình ảnh–văn bản tiếng Việt, và ViCLIP-OT [@tran2026viclipot] là một mô hình như vậy, được huấn luyện trên UIT-OpenViIC; bài không bao giờ dùng nó làm độ đo hay bộ đánh giá trên tập kiểm tra KTVIC. Về mô hình thị giác–ngôn ngữ, Vintern-1B [@doan2024vintern] và Qwen2.5-VL [@bai2025qwen25vl] viết chú thích tiếng Việt trôi chảy ở chế độ zero-shot; phụ lục còn dùng Qwen3-VL [@bai2025qwen3vl] và InternVL3 [@zhu2025internvl3].

Về độ đo dựa trên tham chiếu và cách báo cáo, CIDEr [@vedantam2015cider] gán trọng số cho n-gram theo tần suất tài liệu nghịch đảo trên tập tham chiếu và chia cho chuẩn của các vectơ n-gram; Mục 3.3 chỉ ra rằng phép chia này biến một n-gram có tần suất tài liệu bằng không, chẳng hạn n-gram chứa dấu chấm mà tham chiếu không bao giờ dùng, thành một khoản phạt thuần tuý. Caglayan và cộng sự chỉ ra các trường hợp thất bại khác của các độ đo chuẩn [@caglayan2020curious]; trong dịch máy, chèn hoặc xoá một dấu câu cuối câu làm cả độ đo dựa trên chuỗi lẫn dựa trên mô hình cho điểm khác biệt đáng kể [@jwalapuram2023pulling]. sacreBLEU [@post2018call] làm cho cách tách token và tham số tham chiếu của BLEU báo cáo được qua một chữ ký phiên bản, và SacreEOS [@hu2023request] làm điều tương tự cho quy ước kết thúc chuỗi. Phiếu giao thức của bài áp dụng cùng ý tưởng cho chú thích ảnh tiếng Việt: nó ghi bộ tách từ (RDRSegmenter trong VnCoreNLP [@nguyen2018fast; @vu2018vncorenlp]), biến thể CIDEr, thang điểm và chính sách dấu câu.

Về tính hợp lệ của bộ chuẩn và tài liệu hoá dữ liệu, bài tự xếp vào dòng công trình hỏi các bộ chuẩn đo điều gì [@bowman2021fix; @raji2021everything] và yêu cầu bộ dữ liệu ghi lại cách chúng được xây dựng [@bender2018datastatements; @gebru2018datasheets]; phiếu giao thức là phần tương ứng ở phía đánh giá. Kilickaya và cộng sự đã đánh giá lại độ đo chú thích tự động so với đánh giá của người [@kilickaya2016reeval]. Về ảo giác đối tượng, CHAIR [@rohrbach2018object] đếm các đối tượng được nêu mà vắng trong tập chuẩn vàng dựng từ nhãn thực thể và tham chiếu, POPE [@li2023evaluating] dò đối tượng bằng câu hỏi có/không; cả hai dựa vào một từ vựng ánh xạ từ sang lớp, và với tiếng Việt từ vựng ấy phải xử lý vị trí dấu thanh, danh từ loại thể và danh từ chỉ vai. Bài song hành [@companion2026underreview] nghiên cứu việc độ đầy đủ của tập chuẩn vàng và số đối tượng được nêu gây nhiễu các độ đo này; bài này chỉ dùng các đối chứng khớp số lượng của nó làm công cụ, trong phụ lục.

Về tính độc lập của tham chiếu, các độ đo chú thích coi các tham chiếu của một ảnh là các mẫu độc lập về cách con người mô tả ảnh; Chen và cộng sự mô hình hoá sự đồng thuận giữa các chú thích của người trên cơ sở ấy [@chen2015microsoft], và các phân tích tương đương người chấm giả định người chấm độc lập [@resnick2026principled]. Khi vài người chú thích viết phần lớn một bộ dữ liệu, mô hình học nhận ra họ và hiệu năng giảm trên ví dụ của người chú thích chưa thấy [@geva2019modeling]; người mô tả đến từ các ngôn ngữ gần nhau nêu nhiều thực thể giống nhau hơn [@berger2025crosslingual]; chất lượng tham chiếu tự nó quan trọng cho đánh giá chú thích [@kasai2022transparent]. Thiết kế một người viết của KTVIC phá vỡ giả định độc lập ngay từ cấu trúc, và bài đo mức độ đó. Bromonschenkel và cộng sự huấn luyện trên chú thích bản ngữ và chú thích dịch máy tiếng Bồ Đào Nha Brazil của cùng ảnh Flickr30K và kiểm tra chéo [@bromonschenkel2026brazilian]. Các nghiên cứu về quy mô dữ liệu tinh chỉnh đo hiệu năng theo lượng dữ liệu, luôn so với một tập tham chiếu [@zhang2024scaling; @lin2024selecting], như bài này làm trên KTVIC.

Về tập chú thích thứ hai và phong cách tham chiếu, bài điểm lại Multi30K [@elliott2016multi30k] và COCO-CN [@li2019cococn], sự khác biệt mô tả giữa các ngôn ngữ [@vanmiltenburg2017crosslinguistic], sở thích của người bản ngữ giữa mô tả viết độc lập và mô tả dịch [@frank2018assessing], ảnh hưởng của tham chiếu lên điểm số [@yi2020improving; @freitag2020bleu; @kornblith2023guiding], chú thích liên miền [@chen2017show; @dessi2023cross] và dịch chuyển phân phối trong phân loại ảnh [@taori2020measuring; @miller2021accuracy]. Bài thừa nhận rằng việc huấn luyện theo một phong cách tham chiếu làm tăng điểm so với phong cách ấy đã được biết một cách định tính, và tự giới hạn phần mình thêm vào: "What we add is narrow: a measured account of how one Vietnamese benchmark's reference-writing protocol and scoring pipeline shape its scores, and a training-set-size slope measured against its references." Cuối cùng, về tinh chỉnh theo sở thích và học tăng cường, bài nhắc huấn luyện tự phê bình [@rennie2017self], phương pháp dựa trên phần thưởng [@tang2026cccaption], kết quả DPO [@rafailov2023direct] trong bản FAIR [@nguyen2026vsps] và nội suy trong không gian trọng số [@wortsman2022robust]; các biện pháp này chỉ được báo cáo trong phụ lục như kết quả âm.

**Bảng B.2.** Điều công trình liên quan nghiên cứu, so với bài này (theo Table 2.1, Mục 2 của bài). "Hai tập tham chiếu" nghĩa là cùng các ảnh được chấm so với hai tập tham chiếu viết riêng rẽ.

| Công trình | Dữ liệu và bài toán | Điều được nghiên cứu | Hai tập tham chiếu trên cùng ảnh | Đường cong theo dữ liệu huấn luyện |
|---|---|---|---|---|
| KTVIC [@pham2024ktvic] | chú thích tiếng Việt, 4,327 ảnh | bộ dữ liệu và các hệ cơ sở trên tập kiểm tra của chính nó | không | không |
| UIT-OpenViIC [@bui2026uit] | chú thích tiếng Việt, 13,100 ảnh | bộ dữ liệu và các hệ cơ sở huấn luyện, kiểm tra trên chính nó | không | không |
| HDUCap [@hoang2026hducap] | chú thích tiếng Việt, 15,000 ảnh | bộ dữ liệu mới và một transformer nhận biết không gian; đánh giá trong miền, zero-shot và trộn dữ liệu | không (các tập ảnh riêng, theo tóm tắt và bản xem trước) | không nêu trong bản xem trước |
| ViCLIP-OT [@tran2026viclipot] | truy hồi ảnh–văn bản tiếng Việt | mô hình truy hồi huấn luyện trên UIT-OpenViIC, zero-shot trên KTVIC | không | không |
| Bromonschenkel và cộng sự [@bromonschenkel2026brazilian] | chú thích tiếng Bồ Đào Nha Brazil, Flickr30K | chú thích bản ngữ so với dịch máy của cùng ảnh, huấn luyện trên một tập và kiểm tra trên tập kia | có, một của người và một dịch | không |
| Buettner và Kovashka [@buettner2024quantifying] | truy hồi ảnh–văn bản đa ngữ | huấn luyện trên chú thích dịch so với bản ngữ | không (chỉ chú thích huấn luyện) | không |
| Multi30K [@elliott2016multi30k]; COCO-CN [@li2019cococn] | chú thích tiếng Đức và tiếng Trung | tập chú thích thứ hai, ở ngôn ngữ khác, cho cùng ảnh | có, ở hai ngôn ngữ | không |
| Yi và cộng sự; Freitag và cộng sự; Kornblith và cộng sự [@yi2020improving; @freitag2020bleu; @kornblith2023guiding] | đánh giá chú thích và dịch | tham chiếu và phong cách của chúng làm điểm thay đổi ra sao | không | không |
| Taori và cộng sự; Miller và cộng sự [@taori2020measuring; @miller2021accuracy] | phân loại ảnh | độ chính xác trong và ngoài phân phối | không (hai phân phối kiểm tra) | không (giữa các mô hình) |
| Zhang và cộng sự; Lin và cộng sự [@zhang2024scaling; @lin2024selecting] | tinh chỉnh mô hình ngôn ngữ lớn | hiệu năng tinh chỉnh theo lượng dữ liệu (và cỡ mô hình) | không | có, một tập tham chiếu |
| Bài này | chú thích tiếng Việt, KTVIC | một điểm KTVIC và một mức tăng do dữ liệu huấn luyện đo điều gì | không | có, một tập tham chiếu (dữ liệu phát triển) |

**Nhận xét rà soát.** Mục 2 bao phủ rộng, các trích dẫn đều có khoá trong `paperB.bib`, và bài tự rào khi không đọc được toàn văn (HDUCap, ViG). Các điểm cần xem lại như sau.

Thứ nhất, cột "Two panels on the same images" của Table 2.1 nay ghi "no" cho chính bài này, nên cột không còn phân biệt bài với công trình trước; cột này, cùng hai đoạn "Independence of references" và "Second caption sets and reference style", được viết để định vị một nghiên cứu hai tập tham chiếu không còn trong văn bản. Nên bỏ cột hoặc viết lại bảng theo ba trục mà bài còn giữ (kiểm định bộ dữ liệu, phiếu giao thức, đường cong theo dữ liệu trên một tập tham chiếu), và rút gọn hai đoạn nói trên cho tương xứng.

Thứ hai, Mục 2 viết rằng bài không bao giờ dùng ViCLIP-OT làm độ đo trên tập kiểm tra KTVIC, nhưng Mục 6.2 dùng "multilingual CLIPScore" làm đối chứng trên ảnh Objects365 mà không nêu mô hình ảnh–văn bản nào. Cần ghi tên mô hình và nói rõ quan hệ với câu ở Mục 2.

Thứ ba, Mục 2 liệt kê bốn mục của phiếu giao thức (bộ tách từ, biến thể CIDEr, thang điểm, chính sách dấu câu) còn Mục 1 và Bảng 4.2 thêm bộ so khớp; nên thống nhất.

Thứ tư, câu "They become comparators only if their protocol matches ours on all four points" dựa vào bốn điểm được nêu ở câu trước (cách chia dữ liệu, tách từ, biến thể CIDEr, thang điểm) mà không có chính sách dấu câu, dù Mục 3.3 cho thấy dấu câu là yếu tố lớn nhất; phản biện sẽ hỏi vì sao điều kiện khớp giao thức không gồm dấu câu.

Thứ năm, một số tên dữ liệu và công cụ xuất hiện trong bài nhưng không có mục trong `paperB.bib`: Flickr30k và Open Images (Mục 2, Mục 3), Objects365 (Mục 6.2), M-HalDetect (Mục 3.6, Phụ lục S13) và pyvi (Mục 3.4). Ngược lại, hai mục `pizzi2022sscd` và `lewis2020overlap` còn trong tệp bib và trong `citation_map_B.tsv` nhưng không còn được trích trong văn bản hiện hành; bảng ánh xạ trích dẫn còn vài dòng trỏ tới các câu đã bị cắt. Khoá `resnick2026principled` mang năm 2026 trong tên nhưng mục ghi năm 2021 và văn bản trích "Resnick et al., 2021"; điều này không sai nhưng nên kiểm khi dựng danh mục.

Thứ sáu, phản biện có thể hỏi vì sao một bài về tính hợp lệ của bộ chuẩn không tự đọc được toàn văn hai công trình gần nhất (HDUCap, ViG); bài đã nêu trung thực giới hạn này ở Mục 2 và Mục 7.1, nhưng nên thử lại việc truy cập trước khi nộp.

## B.4 Mục 3 của bài: Dữ liệu và phép kiểm định tính hợp lệ của KTVIC (Data and a validity audit of KTVIC)

**Nội dung.** Mục 3 kiểm định KTVIC như một công cụ đo. Mỗi phép kiểm định đi kèm một tập lệnh trong bộ công cụ đánh giá (Mục 3.6), để người đọc chạy lại trên đầu ra của hệ thống khác hoặc trên một bộ dữ liệu tiếng Việt khác. Mục gồm sáu tiểu mục, được trình bày lần lượt dưới đây.

### B.4.1 Dữ liệu và cách chia (Mục 3.1)

Với KTVIC, bài dùng tập kiểm tra chính thức gồm 558 ảnh với 2,790 tham chiếu và tập huấn luyện với 18,845 tham chiếu; KTVIC không có tập thẩm định chính thức. Các hệ thống của thân bài (P1, P1-R, fuse2) và thang giám sát được huấn luyện trên toàn bộ 3,769 ảnh huấn luyện; riêng P1 hạt giống 42 thì số ảnh huấn luyện không được ghi lại (Phụ lục S1). Cách chia chính thức được dùng nguyên như phát hành. Trong đó có hai ảnh huấn luyện trùng từng byte với ảnh kiểm tra, và thêm 14 ảnh kiểm tra có ảnh gần trùng trong tập huấn luyện theo một quy tắc dựa trên băm tri giác và phát hiện sao chép, tổng cộng 16 trên 558. Vì các hệ thống huấn luyện trên toàn bộ tập huấn luyện, bài thừa nhận điểm kiểm tra của chúng có thể bị nâng nhẹ. Theo một hàng hậu nghiệm (POST HOC), khi bỏ 16 ảnh này thì trung bình ba hạt giống là 148.88 (độ lệch chuẩn 0.36) trên 542 ảnh, tính từ điểm từng ảnh như đã tính trên cả 558 ảnh; hàng này không có phán quyết và con số báo cáo 148.23 không đổi.

Cho những lựa chọn cần dữ liệu để riêng (quy tắc giải mã và các cổng phát triển trong phụ lục), tập huấn luyện được chia một lần, với hạt giống cố định, thành 3,469 ảnh huấn luyện và một tập phát triển 300 ảnh gọi là "dev300". Phép chia này có trước các phép thử ấy và không được định cỡ theo lực thống kê. Chỉ họ hệ thống có cổng phát triển được huấn luyện không có dev300 (xét theo mã ảnh); Bảng S1.1 liệt kê các hệ thống này và số ảnh của từng hệ thống kèm nguồn. Các quy tắc chỉnh trên dev300 được áp dụng nguyên vẹn cho tập kiểm tra; chúng được chỉnh trên một hệ thống huấn luyện không có dev300 và áp dụng cho P1-R, hệ thống có huấn luyện trên dev300.

Với UIT-ViIC, bài dùng tập kiểm tra chính thức (231 ảnh) cho chuyển miền giữa các bộ dữ liệu và cho một lần lặp lại trong miền (Mục 5.2). Ảnh UIT-ViIC lấy từ COCO, nên chú thích thực thể của COCO cho một tập chuẩn vàng thứ hai, không dựa trên chú thích, cho cùng các ảnh. Cả 231 ảnh kiểm tra đều là ảnh COCO train2017, nên bất kỳ mô hình nền nào tiền huấn luyện trên COCO, kể cả mô hình của bài, đều có thể đã thấy chúng. Vì vậy bài dùng UIT-ViIC như một bộ dữ liệu thứ hai với quy ước tham chiếu riêng và một tập chuẩn vàng độc lập, không như dữ liệu chưa thấy. Với XM3600 tiếng Việt, bài chỉ dùng tham chiếu cho phép kiểm định dấu câu ở Mục 3.3; ảnh của nó là ảnh Open Images nên cũng có khả năng đã bị thấy; việc đánh giá hệ thống trên XM3600 thuộc về bài song hành và bài này không báo cáo điểm nào của bài ấy.

### B.4.2 Năm tham chiếu của một ảnh đến từ một người viết (Mục 3.2)

Cơ sở của phép kiểm định là mô tả trong bài KTVIC về một giao diện trong đó một người chú thích gõ cả năm chú thích của một ảnh [@pham2024ktvic], trong khi các độ đo nhiều tham chiếu giả định các tham chiếu là các mô tả độc lập. Bài kiểm trực tiếp giả định này bằng một thống kê hoán đổi được trên các lần nêu đối tượng. Xét mọi lớp đối tượng được đúng hai trong năm tham chiếu của một ảnh nêu, gọi là một cặp đôi (doubleton). Nếu năm vị trí hoán đổi được thì hai tham chiếu nêu đối tượng ấy sẽ kề nhau (vị trí *i* và *i*+1) với xác suất

$$P_0 = \frac{4}{10} = 0.40, \qquad \text{(B.1)}$$

trong đó 10 là số cặp vị trí có thể có trong năm vị trí và 4 là số cặp kề nhau. Thống kê quan sát là tỉ lệ kề nhau, tức tỉ lệ các cặp đôi rơi vào hai vị trí kề nhau. Thống kê bổ trợ là hiệu giữa độ tương đồng Jaccard của tập đối tượng giữa hai tham chiếu liên tiếp (độ trễ 1) và trung bình độ tương đồng ở các độ trễ 2–4.

**Bảng B.3.** Thống kê hoán đổi được trên KTVIC (Mục 3.2 và Phụ lục S15 của bài). Hàng phân phối không theo hoán vị là POST HOC.

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| Tỉ lệ kề nhau, tập kiểm tra | 0.7102 [0.6696, 0.7518] | 566 cặp đôi; z = 15.07 so với giá trị không 0.40 |
| Tỉ lệ kề nhau, tập huấn luyện | 0.6673 [0.6499, 0.6852] | cùng dạng |
| Tỉ lệ kề nhau, dev300 | 0.631 [0.5649, 0.6962] | cùng dạng |
| Giá trị không khi các vị trí hoán đổi được | 0.40 | công thức (B.1) |
| Phân phối không giữ tỉ lệ nêu của từng vị trí (POST HOC), tập kiểm tra | trung bình 0.4504; 95% của 1,000 lần rút nằm trong [0.4134, 0.4876] | không lần rút nào đạt 0.7102 |
| Độ dôi Jaccard ở độ trễ 1, tập kiểm tra | 0.135 [0.1178, 0.1538] | giá trị không theo hoán vị 0.0355; không lần rút nào đạt 0.135 |

Bài diễn giải mẫu hình này là phù hợp với giao diện một người viết: một chuỗi diễn đạt lại, mỗi câu được viết khi câu trước còn trước mắt. Bài cũng tự nêu một cách giải thích thay thế: một xu hướng theo vị trí cũng có thể nâng cả hai thống kê, vì vị trí 0 nêu ít đối tượng hơn các vị trí sau (Mục 4.1). Để tách hai cách giải thích, bài dùng một phân phối không theo hoán vị (hậu nghiệm): trong mỗi ảnh, gán lại tham chiếu nào nêu đối tượng nào, giữ nguyên cả số đối tượng mỗi tham chiếu nêu lẫn số tham chiếu nêu mỗi đối tượng (Phụ lục S15). Dưới phân phối này, tỉ lệ kề nhau trung bình là 0.4504 và không lần rút nào trong 1,000 lần đạt giá trị quan sát; tập huấn luyện và dev300 cho cùng kết quả. Bài kết luận rằng tỉ lệ nêu theo vị trí chỉ nâng giá trị không lên một chút trên 0.40 và không giải thích được sự kề nhau.

Bài tự giới hạn suy luận theo ba bước. Một tỉ lệ trên 0.40 tự nó không đặc hiệu cho một người viết. Thống kê được định nghĩa ở bài song hành, nơi báo cáo nó trên các kho ngữ liệu khác: COCO và UIT-ViIC, đều do các người chú thích độc lập viết theo giao thức đã công bố, không có độ dôi kề nhau; Flickr30k, cũng do người viết độc lập, nằm trên mức đó, điều mà bài song hành quy cho thứ tự tệp không ngẫu nhiên; và toàn bộ tập kiểm tra UIT-OpenViIC, có giao thức nhập chú thích không được ghi lại, cũng nằm trên mức đó. Bài song hành lại để trường hợp KTVIC cho bài này, nên sự tương phản giữa KTVIC và các kho khác bị chia giữa hai bài và không bài nào tự mình cho thấy nó. Bài viết nguyên văn rằng tỉ lệ của KTVIC cao hơn hẳn mọi giá trị bài song hành báo cáo và bài KTVIC có ghi lại giao diện một người viết, "but the step from the statistic to 'one writer' rests on that documentation, not on the statistic alone".

Từ đó bài rút ra hai hệ quả cho đánh giá. Hệ quả thứ nhất: các tham chiếu là góc nhìn của một người viết, lặp năm lần. Phép so bỏ-một-ra (leave-one-out) từng tham chiếu với bốn tham chiếu còn lại cho độ chính xác, độ phủ và F1 về đối tượng là 85.33 / 46.90 / 60.50; vì cả năm tham chiếu chung một người viết, đây là con số về tính nhất quán trong cùng người viết chứ không phải trần của con người, và bài không so hệ thống với nó dưới tên "human parity". Hệ quả thứ hai: năm tham chiếu có giá trị ít hơn năm. Tập chuẩn vàng đối tượng của một ảnh là hợp của các tham chiếu; dưới một chuỗi diễn đạt lại, các tham chiếu thêm đóng góp ít đối tượng mới hơn so với các chú thích độc lập, nên độ phủ so với hợp ấy đánh giá thấp những gì một chú thích nói đúng về ảnh. Văn bản hiển thị không mô tả hình nào ở tiểu mục này; trong tệp nguồn chỉ có một ghi chú ẩn dành chỗ cho một hình về tỉ lệ kề nhau, chưa được chèn, và không có tệp hình.

### B.4.3 Tham chiếu không có dấu câu và cái giá của một dấu chấm (Mục 3.3)

Về hiện trạng dữ liệu, không tham chiếu nào trong 2,790 tham chiếu kiểm tra và 18,845 tham chiếu huấn luyện kết thúc bằng dấu chấm. Một hệ thống tinh chỉnh trên KTVIC học điều này: không đầu ra nào trong 558 đầu ra kiểm tra của P1-R (hạt giống 42) kết thúc bằng dấu chấm, trong khi 557 trên 558 đầu ra zero-shot của cùng mô hình nền có dấu chấm cuối.

Về cơ chế, CIDEr-D gán trọng số cho mỗi n-gram bằng tần suất tài liệu nghịch đảo trên tập tham chiếu và chia tích vô hướng cho chuẩn của vectơ ứng viên và vectơ tham chiếu. Bài mô tả cơ chế bằng lời và không in công thức; viết lại bằng ký hiệu, thành phần được nhắc tới có dạng

$$\mathrm{sim}(c, r) = \frac{\mathbf{g}(c)\cdot\mathbf{g}(r)}{\lVert\mathbf{g}(c)\rVert\,\lVert\mathbf{g}(r)\rVert}, \qquad \text{(B.2)}$$

với $c$ là chú thích ứng viên, $r$ là một tham chiếu và $\mathbf{g}(\cdot)$ là vectơ n-gram có trọng số tần suất tài liệu nghịch đảo. Một n-gram chứa "." có tần suất tài liệu bằng không trong tham chiếu của KTVIC: nó không thể khớp, tức không đóng góp vào tử số, nhưng vẫn đi vào chuẩn của ứng viên ở mẫu số, nên mỗi dấu chấm kéo điểm của cả chú thích xuống.

Về quy trình chấm, bộ chấm chuẩn của COCO là pycocoevalcap tách token bằng bộ tách PTB rồi xoá mọi token trong danh sách dấu câu của nó khỏi ứng viên và tham chiếu [@chen2015microsoft]. Bài viết rằng các quy trình tiếng Việt thay bộ tách ấy bằng một bộ tách từ và cùng với đó bỏ bước xoá dấu câu. Bộ chấm đã commit của bài là một quy trình như vậy (RDRSegmenter; giao thức P0): nó chấm dấu câu như được viết, và cơ chế trên áp dụng cho nó.

**Bảng B.4.** Hiệu ứng của dấu chấm trên tập kiểm tra KTVIC (Mục 3.3 của bài; CIDEr-D ×100; P1-R hạt giống 42 và mô hình nền zero-shot). Cột xoá dấu câu kiểu PTB là POST HOC.

| Đại lượng | Giao thức P0 (dấu câu như được viết) | Xoá dấu câu kiểu PTB (POST HOC) |
|---|---|---|
| P1-R, đầu ra như được viết, năm tham chiếu | 148.66 | 148.70 |
| P1-R, thêm một "." vào mỗi đầu ra, năm tham chiếu | 113.49 | thay đổi 0.00 |
| Thay đổi của P1-R, năm tham chiếu | −35.17 (−23.66%) | 0.00 |
| Thay đổi của P1-R, một tham chiếu | −36.17 (−16.73%) | 0.00 |
| Zero-shot, đầu ra như được viết | 28.98 | 34.97 |
| Zero-shot, gỡ dấu chấm cuối | 33.30 | — |
| Khoảng cách P1-R trừ zero-shot | 119.68 [110.67, 128.44] | 113.73 [104.65, 122.50] |

Dưới P0, mức mất tuyệt đối giữ gần 35 điểm khi thêm tham chiếu, còn mức mất tương đối tăng, vì bản thân điểm số giảm khi có nhiều tham chiếu hơn. Bài kết luận rằng dưới P0 một phần khoảng cách giữa hệ zero-shot và hệ tinh chỉnh trên KTVIC là do dấu câu chứ không do nội dung. Hàng xoá kiểu PTB được thêm sau một lần rà soát nội bộ bản thảo và được ghi nhãn hậu nghiệm: dùng RDRSegmenter như P0, rồi xoá mọi token thuộc danh sách dấu câu PTB của pycocoevalcap khỏi ứng viên và tham chiếu. Dưới giao thức ấy, thêm một dấu chấm làm CIDEr-D thay đổi 0.00 với mọi hệ thống và mọi số tham chiếu từ một đến năm, vì token được thêm bị xoá trước khi chấm; bước xoá cũng loại 775 token khỏi đầu ra zero-shot, 1 token khỏi đầu ra P1-R và không token nào khỏi tham chiếu, trong khi 19 token dấu câu thuộc 2 loại không có trong danh sách vẫn còn lại trong đầu ra zero-shot (Phụ lục S11). Khoảng tin cậy của khoảng cách giữa hai hệ thống là bootstrap ghép cặp theo ảnh, 2,000 lần rút. Bài viết: hiệu ứng dấu chấm là thuộc tính của quy trình chấm chứ không riêng của KTVIC; nơi quy trình giữ dấu câu, một dấu chấm mỗi chú thích làm CIDEr-D thay đổi "by up to 35 points", còn với cách xoá kiểu PTB thì không thay đổi.

Về các hệ cơ sở đã công bố, mã công khai của các hệ cơ sở KTVIC chấm bằng bộ tách PTB của pycocoevalcap, tức có xoá dấu câu (Phụ lục S14 nêu đường dẫn mã và commit); việc các điểm KTVIC đã công bố có được tạo bằng mã ấy hay không là không rõ và bài không xác minh được. Cùng kho mã chứa đầu ra kiểm tra của hai hệ cơ sở KTVIC đã công bố, ResNet101+LSTM và ViT+Transformer, được dùng với sự cho phép của tác giả kho (trao đổi cá nhân); kho không có giấy phép, nhóm tác giả chỉ tính thống kê tổng hợp và không phân phối lại đầu ra nào. Theo một kiểm tra hậu nghiệm, ngoài dấu gạch dưới nối các âm tiết của một từ, không chú thích nào trong 558 chú thích của mỗi hệ cơ sở chứa ký tự dấu câu, nên cách xoá kiểu PTB để nguyên CIDEr-D của cả hai. Bài nêu rõ: mọi phán quyết đã đăng ký trong bài được tính dưới P0 và không đổi.

**Bảng B.5.** Quy ước dấu chấm cuối câu của tham chiếu và của đầu ra hệ thống (Mục 3.3 của bài).

| Tập | Số kết thúc bằng dấu chấm |
|---|---|
| Tham chiếu kiểm tra KTVIC | không tham chiếu nào trong 2,790 |
| Tham chiếu huấn luyện KTVIC | không tham chiếu nào trong 18,845 |
| Tham chiếu kiểm tra UIT-ViIC | 1,133 trên 1,155 (98.10%) |
| Tham chiếu kiểm tra XM3600 tiếng Việt | 217 trên 1,227 (17.69%) |
| Đầu ra P1-R (hạt giống 42) trên tập kiểm tra KTVIC | không đầu ra nào trong 558 |
| Đầu ra zero-shot trên tập kiểm tra KTVIC | 557 trên 558 |
| Đầu ra trên ảnh XM3600: P1 (mặt nạ cũ, hạt giống 43) và fusion (hạt giống 42) | 0.0% |
| Đầu ra trên ảnh XM3600: mô hình nền zero-shot | 99.5% |

UIT-ViIC theo quy ước ngược lại với KTVIC, nhưng hiệu ứng của việc thêm dấu chấm lên CIDEr-D trên UIT-ViIC chưa được đo bằng bộ chấm đã commit. Với XM3600, nơi tham chiếu có dấu câu một phần, thêm dấu chấm vào mọi đầu ra của các hệ tinh chỉnh dưới P0 làm CIDEr-D của chúng tăng +2.71 [2.23, 3.21] với P1 và +2.75 [2.32, 3.20] với fusion (bootstrap ghép cặp theo ảnh); với cách xoá kiểu PTB (hậu nghiệm) thì không thay đổi (0.00). Bài diễn giải: tinh chỉnh trên KTVIC truyền sang khuôn mẫu không dấu câu của KTVIC, và một quy trình giữ dấu câu tính phí cho điều đó ngay cả trên một tập tham chiếu có dấu câu một phần. Bài chỉ đo phần đóng góp của dấu chấm vào các chênh lệch và không phân rã phần còn lại.

**Bảng B.6.** Điểm hệ thống trên ảnh XM3600 đứng sau phép kiểm định dấu chấm (Phụ lục S11 của bài; CIDEr-D ×100, lời nhắc ngắn). Hàng PTB là POST HOC.

| Đại lượng | Zero-shot | P1 (mặt nạ cũ, hạt giống 43) | fusion (hạt giống 42) |
|---|---|---|---|
| Điểm dưới P0 | 48.39 | 41.17 | 38.61 |
| Chênh lệch so với zero-shot dưới P0 | — | −7.22 [−11.48, −2.86] | −9.78 [−13.93, −5.61] |
| Thay đổi khi thêm dấu chấm dưới P0 | — | +2.71 [2.23, 3.21] | +2.75 [2.32, 3.20] |
| Điểm với xoá kiểu PTB (POST HOC) | 47.23 | 42.21 | 39.71 |
| Chênh lệch so với zero-shot với xoá kiểu PTB (POST HOC) | — | −5.02 [−9.32, −0.61] | −7.51 [−11.71, −3.24] |

Khuyến nghị của tiểu mục là: một quy trình tiếng Việt thay bộ tách PTB nên khôi phục bước xoá dấu câu trên ứng viên và tham chiếu, hoặc báo cáo điểm có và không có bước ấy; trong cả hai trường hợp, chính sách dấu câu phải đi kèm mọi điểm KTVIC.

### B.4.4 Độ nhạy theo cách tách từ và bộ chấm (Mục 3.4)

CIDEr tiếng Việt phụ thuộc vào tách từ (word segmentation). Bộ chấm đã commit tách từ bằng RDRSegmenter (VnCoreNLP 1.2), vốn tái tạo đúng cách tách từ của chính KTVIC trên cả 2,790 trong 2,790 tham chiếu kiểm tra.

**Bảng B.7.** Cùng đầu ra của P1 (mặt nạ cũ, hạt giống 42) dưới ba cách tách (Mục 3.4 của bài; CIDEr-D ×100). Tương quan thứ hạng tính trên 26 hệ thống được chấm: 24 hệ thống của bài và đầu ra của hai hệ cơ sở KTVIC đã công bố.

| Cách tách | CIDEr-D | Kendall τ so với bộ chấm đã commit |
|---|---|---|
| RDRSegmenter (bộ chấm đã commit) | 149.79 | — |
| Tách theo âm tiết ở khoảng trắng | 165.43 | 0.969 |
| pyvi thay cho RDRSegmenter | 149.12 | 0.994 |

Thứ hạng của các hệ thống phần lớn được giữ, nhưng giá trị tuyệt đối không so sánh được giữa tách từ và tách theo âm tiết. Chênh lệch 15.64 điểm chỉ do cách tách token lớn hơn khoảng cách tới điểm GRIT được báo cáo, trong khi một bộ tách từ thứ hai làm điểm thay đổi ít hơn nhiều; bài kết luận rằng hiệu ứng lớn là giữa có tách từ và không tách từ, không phải giữa hai bộ tách từ này. Đầu ra của hai hệ cơ sở được phát hành ở dạng đã tách từ, với 705 và 817 từ nối bằng gạch dưới; nhóm tác giả thay mỗi gạch dưới bằng khoảng trắng trước khi tách, và RDRSegmenter khi đó tái tạo đúng cách tách đã phát hành của 558 và 557 trên 558 chú thích (hậu nghiệm). Bản FAIR trước đã báo cáo 149.8 cho lần chạy này dưới cùng bộ chấm.

### B.4.5 Ba phiên bản bộ so khớp đối tượng (Mục 3.5 và Phụ lục S10)

Các điểm ở mức đối tượng (CHAIR, độ chính xác và độ phủ đối tượng) cần một bộ so khớp ánh xạ từ tiếng Việt sang lớp đối tượng. Phiên bản v1 là bộ từ vựng tiếng Việt 113 mục của bản FAIR, áp dụng trên văn bản thô. Phiên bản v2 thêm chuẩn hoá dấu thanh: hai cách đặt dấu thanh trong các âm tiết như *hoà/hòa* được quy về một dạng. v2 là bộ so khớp chính của bài; phép chuẩn hoá không làm đổi tham chiếu nào trong 2,790 tham chiếu kiểm tra KTVIC, nhưng làm đổi các đối tượng khớp được của 30 trên 73 hệ thống KTVIC thuộc lần chấm lại theo chuẩn hoá dấu thanh, vì một số đầu ra dùng cách đặt dấu kia. Phiên bản v3 thêm quy tắc cho danh từ loại thể, từ ghép và danh từ chỉ vai: *cây* vừa là danh từ chỉ cây cối vừa là loại từ cho vật dài, và *cầu* trong *cây cầu* là cây cầu. Trong 980 token *cây* mà bộ so khớp rút ra từ tham chiếu huấn luyện, 210 là cách dùng loại từ và 160 là *cây cầu*; v1 và v2 đếm tất cả vào lớp cây. Bài in đậm rằng các quy tắc v3 được suy ra từ số đếm trên tập huấn luyện và chưa có người duyệt; vì thế v3 chỉ được báo cáo như phân tích độ nhạy, không kết luận nào phụ thuộc vào nó, và quy tắc của nó không nằm trong bộ công cụ.

Theo Phụ lục S10, lựa chọn bộ so khớp quan trọng với giá trị tuyệt đối và ít quan trọng với phép so sánh. Với P1-R (hạt giống 42), v3 làm số lớp được nêu trên mỗi chú thích giảm từ 1.823 xuống 1.706 và nâng F1 đối tượng từ 55.51 lên 56.95; F1 bỏ-một-ra trong cùng người viết đi từ 60.50 lên 61.67; số mũ của đường biên dùng trong thang giám sát là 0.7468 dưới v2 và 0.7470 dưới v3. Trên UIT-ViIC, các danh từ chỉ vai và trẻ em chi phối các ảo giác được đếm so với lớp COCO; một phép chuẩn hoá vai/trẻ em riêng, cũng chưa có người duyệt, hạ CHAIR_i của P1 huấn luyện trên KTVIC (mặt nạ cũ, hạt giống 43) từ 30.02 xuống 21.39 nhưng của hệ zero-shot chỉ từ 27.12 xuống 26.01, tức làm đảo thứ tự hai hệ thống. Bài không báo cáo khoảng tin cậy cho sự đảo này và kết luận rằng một thứ hạng đảo theo một quy tắc so khớp chưa được xác nhận không phải là phát hiện về hệ thống mà là lý do để công bố bộ so khớp cùng điểm số.

### B.4.6 Bộ công cụ đánh giá và tính sẵn có của dữ liệu (Mục 3.6)

Bài coi các phép kiểm định của Mục 3 là đóng góp dùng lại được và sẽ phát hành chúng thành một bộ công cụ gồm năm phần: bộ chấm điểm và phiếu giao thức; bộ so khớp đối tượng (v1 và v2); các tập lệnh chia dữ liệu; một tập lệnh kiểm định cho mỗi phép kiểm định của mục này; và các hồ sơ (tệp đăng ký trước, bản sao chỉ còn điểm số của các tệp kết quả mà bảng kê số liệu trích, và chính bảng kê ấy). Các trường chú thích được gỡ khỏi tệp kết quả vì lý do giấy phép và mã SHA-256 của từng tệp gốc được nêu. Mỗi tập lệnh chạy trên bản dữ liệu và đầu ra hệ thống của người đọc. Bài viết rằng mỗi tập lệnh `kit_b` đã được chạy lại từ kho lưu trữ và tái tạo mọi giá trị mà bảng kê trích từ nó; Phụ lục S13 nêu các ngoại lệ.

Để thử bộ công cụ trên đầu ra không do mình tạo, nhóm tác giả tự chạy nó trên các hệ thống chú thích tiếng Việt của bên thứ ba. Một bản đăng ký trước chỉ nhằm mô tả đã cố định, trước khi tải bất kỳ đầu ra nào, quy tắc đủ điều kiện, một tập kiểm tra cho mỗi hệ thống, công thức giải mã, các cột giao thức, mức trần 3 giờ GPU và ngưỡng thành công. Không tệp nào trong mười tệp đầu ra đã công bố mà nhóm tìm được qua được cổng cấu trúc đã đăng ký. Ba checkpoint đã phát hành, từ ba chủ sở hữu khác, tải được và qua bước thử khói: Swin-BART (K1, tập kiểm tra KTVIC), SmolVLM2-500M-vi-stage1 (K5, tập kiểm tra UIT-ViIC) và Vie-BLIP (K6, tập kiểm tra UIT-OpenViIC). Mỗi hệ thống được giải mã một lần với thiết lập do tác giả của nó ghi lại và được chấm một lần; mọi bước GPU dùng 620 giây GPU trên một card RTX 3090 24 GB. Kết quả đạt ngưỡng đã định trước (ít nhất ba hệ thống từ ít nhất ba chủ sở hữu khác nhau) trong một lần chạy của chính tác giả; bộ công cụ chưa được một nhóm bên ngoài chạy. Lần chạy không mang phán quyết, không xếp hạng hệ thống nào và không so hàng nào với hệ thống của bài; bảng điểm nằm ở Phụ lục S8 (xem Bảng B.23).

Về giấy phép và lưu trữ, mã của bộ công cụ sẽ được phát hành theo giấy phép MIT, kèm chỗ trống `[AUTHOR TO CONFIRM: licence]`, và sẽ được lưu trên Zenodo trước khi phản biện, với DOI còn là `[AUTHOR TO PROVIDE]`. KTVIC, UIT-ViIC và UIT-OpenViIC không nêu giấy phép; chúng chỉ yêu cầu trích dẫn và dùng cho nghiên cứu. Người đọc lấy dữ liệu từ nguồn gốc. Một người trong nhóm tác giả đã liên hệ với tác giả KTVIC và UIT-OpenViIC, những người đồng ý cho dùng dữ liệu. Tác giả UIT-ViIC chưa cho phép việc dùng này và bài không khẳng định có sự cho phép nào: trong bài và bộ công cụ, UIT-ViIC chỉ xuất hiện dưới dạng điểm và thống kê tổng hợp cùng các con trỏ (mã ảnh và nơi lấy dữ liệu), không chú thích hay bảng theo từng ảnh nào của UIT-ViIC được trình bày hay phát hành. Không ảnh, tham chiếu, đầu ra hệ thống, số đếm hay danh sách mã suy ra từ KTVIC, hay trọng số tinh chỉnh nào được phát hành; ngoại lệ duy nhất là các mã ảnh trong tệp đăng ký trước của nghiên cứu phát triển ở Mục 5.3 (các tập con huấn luyện lồng nhau), vốn chỉ chứa mã định danh và mã băm. Trước khi nộp lưu trữ, mọi tệp của kho được quét so với tham chiếu của KTVIC, UIT-ViIC, UIT-OpenViIC và XM3600 tiếng Việt, cùng M-HalDetect và đầu ra đã phát hành của hai hệ cơ sở, để tìm các chuỗi chung gồm n = 8 token liên tiếp; phép quét không tìm thấy chú thích nào của bộ dữ liệu, và các trùng khớp duy nhất là các cụm ví dụ do tác giả viết trong các tệp mã bị ghim bởi các bản đăng ký trước. Bài nói rõ cụm "No dataset captions" được hiểu theo nghĩa này.

**Nhận xét rà soát.** Mục 3 là phần mang bằng chứng chính và nhìn chung trung thực về giới hạn. Các điểm dưới đây xếp theo tiểu mục.

Về Mục 3.1, có ba điểm. (i) Quy tắc "perceptual-hash and copy-detection" xác định 14 ảnh gần trùng không được mô tả (công cụ, ngưỡng) và không có trích dẫn; tệp bib còn một mục về bộ mô tả phát hiện sao chép không được trích, gợi ý rằng trích dẫn đã bị rơi khi cắt văn bản. (ii) Hàng hậu nghiệm 148.88 trên 542 ảnh chỉ được tính cho P1-R; các con số kiểm tra khác (Bảng 5.1, phép thử hệ thống cuối, phép kiểm định dấu câu) không có hàng tương ứng, và bài nên nói rõ điều đó ở Mục 7.1. (iii) Mục 5.3 nêu 7 ảnh dev300 có ảnh trùng hoặc gần trùng trong tập huấn luyện, nhưng Mục 3.1 chỉ nói về trùng lặp giữa tập huấn luyện và tập kiểm tra, còn Phụ lục S1 viết "no dev-side number above is inflated" (xét theo mã ảnh). Ba chỗ này cần một câu thống nhất về trùng lặp phía phát triển.

Về Mục 3.2, phản biện nhiều khả năng hỏi năm điều. (i) Thống kê phụ thuộc vào bộ so khớp, nhưng tiểu mục không nói phiên bản nào được dùng và cách tính khoảng tin cậy của tỉ lệ kề nhau (đơn vị lấy mẫu lại là ảnh hay cặp đôi); giá trị z = 15.07 ngầm coi các cặp đôi là độc lập. (ii) Phân phối không theo hoán vị, lập luận then chốt chống lại cách giải thích bằng xu hướng vị trí, là hậu nghiệm. (iii) Bằng chứng tương phản với các kho ngữ liệu viết độc lập nằm ở một bài chưa công bố, nên người phản biện không kiểm được; bài đã nói thẳng điều này, nhưng tóm tắt và câu mở đầu Mục 8 lại diễn đạt mạnh hơn thân bài. (iv) KTVIC có ba người chú thích; bài không báo cáo thống kê theo từng người và không nói có làm được hay không. (v) Hệ quả thứ hai ("Five references are worth less than five") chỉ được lập luận định tính; văn bản hiện hành không có con số nào đo mức hụt độ phủ của hợp năm tham chiếu. Ngoài ra, giá trị dev300 được in với ba chữ số thập phân (0.631) trong khi hai tập kia in bốn chữ số.

Về Mục 3.3, đây là phát hiện có sức nặng nhất nhưng cũng dễ bị chất vấn nhất. (i) Mọi con số cỡ hiệu ứng trên KTVIC đến từ một hạt giống của một hệ thống (P1-R hạt giống 42) và mức −35.17 không có khoảng tin cậy. (ii) Câu "Vietnamese pipelines replace that tokenizer with a word segmenter, and with it they drop the punctuation removal" ở Mục 3.3 là một khẳng định chung về các quy trình tiếng Việt, trong khi Mục 1 đã được viết ở dạng điều kiện ("a pipeline that replaces it ..., as our committed scorer does"); mức độ phổ biến của các quy trình như vậy không có nguồn, và chính bài cho biết mã công khai của các hệ cơ sở KTVIC có xoá dấu câu. Phản biện sẽ hỏi rủi ro này ảnh hưởng đến ai ngoài bộ chấm của chính nhóm tác giả; nên sửa câu ở Mục 3.3 về dạng điều kiện như Mục 1. (iii) Cụm "by up to 35 points" không khớp với chính bảng số của bài, nơi mức mất với một tham chiếu là 36.17 điểm. (iv) Hàng xoá kiểu PTB, tức hàng cho thấy hiệu ứng biến mất, là hậu nghiệm; tóm tắt nên mang nhãn này. (v) Hiệu ứng trên UIT-ViIC chưa được đo, nên phần diễn giải kết quả chuyển miền ở Mục 5.2 còn bỏ ngỏ đúng yếu tố mà mục này cho là lớn nhất. (vi) Trên XM3600 dấu của hiệu ứng ngược lại (thêm dấu chấm làm tăng điểm), bài chỉ đo phần của dấu chấm và nói rõ không phân rã phần còn lại; nên giữ nguyên lời rào này khi viết lại.

Về Mục 3.4, con số 15.64 là hiệu của hai điểm của một lần chạy (P1 mặt nạ cũ, hạt giống 42), chính là lần chạy mà Mục 5.1 cho biết không tái lập được bằng huấn luyện lại; điều này không ảnh hưởng đến phép so hai cách tách trên cùng đầu ra nhưng nên được nói rõ. Bài không nêu biến thể của hệ số Kendall ở đây, trong khi Phụ lục S4 dùng τ_b và Mục 6.2 dùng τ_c. Phép so "larger than the gap to the reported GRIT score" đặt một hiệu ứng nội bộ cạnh một khoảng cách giữa hai giao thức không khớp, và bài không in giá trị của khoảng cách ấy; nên in con số và nhắc lại lời rào.

Về Mục 3.5, ba kiểm kê hệ thống khác nhau xuất hiện mà không có giải thích: 73 hệ thống ở lần chấm lại theo dấu thanh, 79 hệ thống của phép kiểm định thứ hạng ở Mục 5.1, và 26 hệ thống ở Mục 3.4. Nguồn gốc của quy tắc v3 cũng cần thống nhất: thân bài chỉ nói "derived from training-split counts" và "no human sign-off", còn `STUDY_BRIEF_B.md` viết rằng v3 do mô hình soạn; cần một câu chính xác về ai hoặc cái gì đã soạn quy tắc.

Về Mục 3.6, có bốn việc. (i) Các chỗ trống về giấy phép và DOI phải được điền trước khi nộp. (ii) Câu về việc chạy lại các tập lệnh và câu về phép quét văn bản mô tả một kho lưu trữ mà `V2_PROGRESS_B.md` ghi là còn phải dựng lại và quét lại; Phụ lục S13 viết ba tệp mã với 9 dòng trùng trong khi ghi chú nguồn của chính đoạn ấy nêu một số đếm khác, và tệp tiến độ ghi đây là mâu thuẫn chưa giải quyết. (iii) Tập lệnh của lần chạy hệ thống bên ngoài, của nghiên cứu kích thước tập huấn luyện và của nghiên cứu ở Mục 6.2 không có trong Bảng S13.2, dù Mục 3.6 viết rằng bảng ấy liệt kê mọi tệp. (iv) Danh sách dữ liệu ở đoạn "Datasets" thiếu Objects365 (dùng ở Mục 6.2), và M-HalDetect xuất hiện trong phép quét mà không có giải thích vì sao nó liên quan.

## B.5 Mục 4 của bài: Công cụ đo và phiếu giao thức (The measuring instrument and its protocol card)

**Nội dung.** Mục 4 mô tả hệ thống dùng làm công cụ đo, phiếu giao thức đứng sau mọi điểm số, và hai cổng tái lập.

### B.5.1 Các hệ thống (Mục 4.1)

Phép kiểm định cần một hệ thống mà sự khác biệt của nó so với các hệ thống khác là đã biết. Mọi hệ thống dùng chung một mô hình nền, Qwen2.5-VL-7B-Instruct [@bai2025qwen25vl], và một công thức tinh chỉnh, là công thức QLoRA của bài FAIR trước [@dettmers2023qlora; @hu2021lora]: lượng tử hoá 4-bit NF4, LoRA hạng 16, α 32, tốc độ học 10⁻⁴, lô hiệu dụng 8, hai epoch, 512 token thị giác. Có hai lời nhắc: lời nhắc ngắn (một câu) và lời nhắc chi tiết. Giải mã là tham lam trừ khi nói khác. Các hệ thống chỉ khác nhau ở đích huấn luyện, ở mặt nạ hàm mất mát, hoặc, ở Mục 5.3, ở kích thước tập huấn luyện.

**Bảng B.8.** Các hệ thống của thân bài: đích huấn luyện cho mỗi ảnh và các token đi vào hàm mất mát (Table 4.1, Mục 4.1 của bài).

| Hệ thống | Đích huấn luyện cho mỗi ảnh huấn luyện | Mất mát |
|---|---|---|
| Zero-shot | không có | — |
| P1 | tham chiếu đầu tiên theo thứ tự tệp, lời nhắc ngắn | lời nhắc và phần trả lời (mặt nạ cũ, legacy mask) |
| P1-R (P1 chỉ tính trên phần trả lời; hệ thống chính) | như P1 | chỉ các token trả lời |
| fuse2 | hàng ngắn của P1, cộng một hàng lời nhắc chi tiết nối tham chiếu đồng thuận nhất với tham chiếu thêm nhiều đối tượng mới nhất, mỗi câu kết bằng dấu chấm | mặt nạ cũ |
| Các adapter theo kích thước tập huấn luyện (Mục 5.3; ba hạt giống × năm kích thước) | như P1-R (tham chiếu KTVIC đầu tiên), trên các tập con lồng nhau của 3,469 ảnh huấn luyện ngoài dev300 | chỉ các token trả lời |

Bài quy ước "P1-R" luôn là hệ chỉ tính mất mát trên phần trả lời và "P1" đứng riêng luôn là hệ mặt nạ cũ, kèm hạt giống mỗi lần. Đoạn "Which P1" của bài cho biết hệ thống nào đứng sau phép phân tích nào; Bảng B.9 sắp lại thông tin ấy.

**Bảng B.9.** Hệ thống dùng cho từng phép phân tích (tổng hợp từ đoạn "Which P1" của Mục 4.1 và từ Mục 3.3, Mục 5.2 của bài).

| Phép phân tích | Hệ thống | Hạt giống |
|---|---|---|
| Kiểm định dấu câu trên KTVIC (Mục 3.3), độ nhạy v3 (Mục 3.5), Mục 5.1 | P1-R | 42 |
| Kiểm định tách từ (Mục 3.4) | P1 (mặt nạ cũ) | 42 |
| Dịch chuyển do dấu chấm trên XM3600 (Mục 3.3), các phân tích UIT-ViIC (Mục 3.5, Mục 5.2) | P1 (mặt nạ cũ); kèm fuse2 hạt giống 42 | 43 |
| Hàng P1 của Bảng 5.1 | P1 (mặt nạ cũ) | ba hạt giống |

Các phát hiện về giao thức đến từ các hệ thống huấn luyện trên toàn bộ 3,769 ảnh huấn luyện KTVIC (riêng P1 hạt giống 42 không có số được ghi lại). Chỉ các biện pháp có cổng phát triển trong phụ lục, phép thử cuối cùng (Phụ lục S6) và nghiên cứu kích thước tập huấn luyện ở Mục 5.3 dùng phần tách 300 ảnh. P1-R là hệ thống bài báo cáo làm hệ cơ sở KTVIC của mình: nó là P1 với mất mát giới hạn ở các token trả lời, còn dưới mặt nạ cũ thì văn bản hướng dẫn và phần đầu của lượt trợ lý vẫn nằm trong mất mát. Các đích hợp nhất (fusion) chỉ được dựng từ tham chiếu của người: mọi đối tượng trong một đích hợp nhất đều do một người chú thích viết, và bước tham lam dừng khi không tham chiếu nào thêm đối tượng mới. Đích ngắn của P1 dùng vị trí 0 của chuỗi một người viết; vị trí 0 là chú thích được gõ đầu tiên và nêu ít đối tượng hơn các vị trí sau, nên số đối tượng của họ P1 thấp hơn của các hệ thống huấn luyện trên đích đồng thuận hay hợp nhất, và bài công bố điều này mỗi khi so hai loại.

### B.5.2 Phiếu giao thức (Mục 4.2)

**Bảng B.10.** Phiếu giao thức: thiết lập chấm đứng sau mọi điểm KTVIC trong bài trừ khi một mục nói khác (Table 4.2, Mục 4.2 của bài).

| Mục | Thiết lập |
|---|---|
| Tập kiểm tra | tập kiểm tra chính thức của KTVIC, 558 ảnh, mỗi ảnh 5 tham chiếu |
| Bộ tách từ | RDRSegmenter, VnCoreNLP 1.2 (bài in mã SHA-256 của tệp jar); cùng bộ tách cho ứng viên và tham chiếu |
| Độ đo n-gram | pycocoevalcap: BLEU-4, ROUGE-L, CIDEr-D, tất cả ×100 |
| Dấu câu | không xoá, không thêm (giao thức P0): RDRSegmenter thay bộ tách PTB nên dấu câu được chấm như được viết trên ứng viên và tham chiếu; Mục 3.3 còn báo cáo biến thể gỡ, biến thể thêm và, hậu nghiệm, cách xoá kiểu PTB |
| Giải mã | tham lam, một chú thích cho mỗi ảnh với mỗi lời nhắc |
| Bộ so khớp đối tượng | v2 (đã chuẩn hoá dấu thanh); v1 và v3 làm độ nhạy |
| P / R / F1 đối tượng | độ chính xác lấy trung bình vi mô trên các lần nêu; độ phủ lấy trung bình vĩ mô trên các ảnh có tập chuẩn vàng khác rỗng; F1 là trung bình điều hoà của hai giá trị; tập chuẩn vàng là hợp các tham chiếu của ảnh |
| Độ bất định | bootstrap phân vị ghép cặp theo ảnh; khi gộp các hạt giống, hệ số dốc mang hiệu ứng cố định theo hạt giống và chỉ ảnh được lấy mẫu lại, nên các khoảng là có điều kiện theo các adapter đã huấn luyện và không gồm phương sai giữa các hạt giống |
| Hạt giống | 42, 43, 44 |

Với $P$ là độ chính xác và $R$ là độ phủ như định nghĩa trong bảng, F1 đối tượng là

$$F_1 = \frac{2PR}{P + R}. \qquad \text{(B.3)}$$

Một bản để điền của phiếu này đi kèm bộ công cụ. Việc chấm chạy như một tiến trình tách khỏi việc sinh. Phiên bản bộ chấm và mã SHA-256 của mọi tệp kết quả đã commit được liệt kê trong bảng kê số liệu; bản thân các dự đoán không được phát hành.

### B.5.3 Các cổng tái lập (Mục 4.3)

Huấn luyện và suy luận vừa trên một card NVIDIA RTX 3090 24 GB; Phụ lục S14 nêu các phiên bản phần mềm được ghim. Hai phép kiểm bảo vệ con số chính, và bài nói rõ cả hai chỉ bao phủ việc chấm: chúng cho thấy các dự đoán đã commit được chấm một cách tất định, không cho thấy huấn luyện hay giải mã tái lập được. Ở phép kiểm máy thứ hai, một máy khác lấy kho mã ở một commit cố định, chấm lại các dự đoán đã commit của P1-R hạt giống 42 và tái tạo tệp kết quả đã commit đúng từng byte; CIDEr-D 148.66 của nó bằng giá trị đã commit. Ở phép kiểm bộ tách từ chạy trực tiếp, cả ba hạt giống của P1-R được chấm lại với một lần chạy VnCoreNLP 1.2 trực tiếp; CIDEr-D, BLEU-4 và ROUGE-L khớp tệp đã commit trên mọi hạt giống: tám trong chín hiệu bằng đúng không, và hiệu thứ chín (CIDEr-D, hạt giống 44) là 2.8 × 10⁻¹⁴, một đơn vị ở chữ số cuối của số thực được lưu. Phán quyết của cổng là "PASS".

**Nhận xét rà soát.** Mục 4 rõ ràng về thiết kế "một mô hình nền, một công thức", và phiếu giao thức là phần dễ dùng lại nhất của bài. Các điểm cần xem lại như sau.

Thứ nhất, phiếu giao thức ghi P0 cho mọi điểm KTVIC "unless a section says otherwise", nhưng tệp đăng ký trước của nghiên cứu ở Mục 5.3 định nghĩa cột quyết định là CIDEr-D của bộ công cụ với dấu câu cuối của ứng viên đã được gỡ ("kit B, final punctuation stripped"), và ghi rằng CIDEr-D như được viết được báo cáo bên cạnh. Mục 5.3 của bài không nói cột nào được in. Cần thêm một câu ở Mục 5.3 hoặc một hàng trong phiếu.

Thứ hai, trong Bảng 4.1 fuse2 dùng mặt nạ cũ còn P1-R dùng mặt nạ chỉ-trả-lời, nên phép so fuse2 với P1-R ở Mục 5.1 thay đổi đồng thời đích huấn luyện và mặt nạ. Hệ đối chứng khớp mặt nạ là P1; Bảng 5.1 có sẵn hàng này và cách đọc thứ nhất của Mục 5.1 nên dựa vào nó.

Thứ ba, đích chi tiết của fuse2 kết thúc bằng dấu chấm trong khi tham chiếu KTVIC không có dấu chấm. Theo Mục 3.3, dưới P0 điều này tự nó kéo CIDEr-D xuống, và Mục 5.1 thừa nhận không tách phần này khỏi phần còn lại. Vì hàng xoá kiểu PTB đã có sẵn công cụ, phản biện có thể yêu cầu điểm của fuse2 (chi tiết) dưới cách xoá ấy; bài hiện không in con số này.

Thứ tư, việc ba phép kiểm định dùng ba cặp hệ thống–hạt giống khác nhau (Bảng B.9) được nêu nhưng không được giải thích. Nên đưa một bảng như Bảng B.9 vào bài và nói vì sao không dùng một hệ thống duy nhất.

Thứ năm, F1 đối tượng là trung bình điều hoà của một độ chính xác vi mô và một độ phủ vĩ mô; đây là định nghĩa không quen thuộc và bài không nêu lý do. Phản biện có thể hỏi kết quả có đổi không nếu cả hai cùng kiểu trung bình.

Thứ sáu, hai cổng tái lập chỉ nói về việc chấm, và bài đã viết đúng như vậy. Tuy nhiên Mục 4.3 không nhắc rằng lần chạy P1 hạt giống 42 đạt 149.79 không tái lập được bằng huấn luyện lại (Mục 5.1); một câu dẫn chiếu sẽ giúp người đọc không hiểu quá về mức tái lập. Chữ "PASS" ở đây là kết quả của một cổng kỹ thuật, không phải phán quyết của một giả thuyết đã đăng ký, và nên được gọi tên như vậy để tránh lẫn với các phán quyết ở Mục 5.

## B.6 Mục 5 của bài: Kết quả (Results: the controlled system, cross-dataset scoring and a training-data gain)

**Nội dung.** Mục 5 gồm ba tiểu mục: hệ thống có kiểm soát trên KTVIC, chấm chéo bộ dữ liệu trên UIT-ViIC, và nghiên cứu kích thước tập huấn luyện trên dữ liệu phát triển. Điểm đối tượng dùng bộ so khớp v2.

### B.6.1 Hệ thống có kiểm soát trên KTVIC (Mục 5.1)

P1-R đạt CIDEr-D mức từ 148.66, 148.06 và 147.96 trên các hạt giống 42, 43 và 44, trung bình 148.23, độ lệch chuẩn 0.38. BLEU-4 là 45.88 và 45.63 trên hạt giống 42 và 43, ROUGE-L là 64.57 trên hạt giống 42.

**Bảng B.11.** Trung bình ba hạt giống trên tập kiểm tra KTVIC (558 ảnh) dưới phiếu giao thức: CIDEr-D ×100; F1 đối tượng với bộ so khớp v2 so với hợp các tham chiếu của mỗi ảnh; M là số lớp được nêu trên mỗi chú thích (Table 5.1, Mục 5.1 của bài).

| Hệ thống (lời nhắc) | CIDEr-D | M | F1 đối tượng |
|---|---|---|---|
| P1 (ngắn) | 145.80 | 1.78 | 54.60 |
| P1-R (ngắn) | 148.23 | 1.79 | 55.44 |
| fuse2 (ngắn) | 143.73 | 2.09 | 58.10 |
| fuse2 (chi tiết) | 22.36 | 3.21 | 64.24 |

Bài rút ra hai cách đọc. Cách đọc thứ nhất: CIDEr và F1 đối tượng xếp hạng hệ thống khác nhau. fuse2 nêu nhiều đối tượng hơn và có F1 đối tượng cao hơn P1-R nhưng CIDEr-D thấp hơn; ở chế độ chi tiết CIDEr-D của nó sụp xuống 22.36 trong khi F1 đối tượng cao nhất bảng. Một phần của sự sụp này là mức phạt độ dài của CIDEr-D và dấu chấm kết thúc các đích chi tiết của fuse2; phần còn lại là việc CIDEr thưởng cho sự khớp với khuôn mẫu tham chiếu ngắn, không dấu câu hơn là cho việc mô tả nhiều hơn về ảnh. Bài nói rõ không tách các phần này. Cách đọc thứ hai: mặt nạ chỉ-trả-lời không phải là một cải tiến đã được kiểm định. Trung bình của P1-R cao hơn trung bình ba hạt giống 145.80 của P1, nhưng hạt giống 42 của P1 đạt 149.79 dưới cùng bộ chấm (giá trị mà bản FAIR báo cáo là 149.8). Số ảnh huấn luyện của lần chạy ấy không xác lập được: văn bản của bản FAIR chỉ tới 3,700 ảnh, mã được commit cùng điểm số chỉ tới cả 3,769 ảnh, và không hồ sơ chạy nào phân định. Bản lặp P1 cùng hạt giống huấn luyện trên cả 3,769 ảnh, p1mask_s42, đạt 147.67 (một kết quả có sẵn, được trích chứ không chấm lại; mặt nạ cũ, đã sửa việc đặt hạt giống). Lần chạy 149.79 có trước bản sửa hạt giống ấy và không tái lập được bằng huấn luyện lại, nên khoảng cách giữa hai con số không phân định số ảnh huấn luyện. Bài báo cáo P1-R như một hệ cơ sở mạnh, ổn định và không khẳng định mặt nạ giúp ích.

Về phép thử cuối cùng, lần đánh giá duy nhất đã đăng ký trước trên tập kiểm tra của hệ thống cuối cùng là đồng thuận hạt giống MBR-3 trên ba hạt giống (Phụ lục S6). Đại lượng được đăng ký là hiệu ghép cặp giữa điểm của phép chọn MBR-3 và trung bình điểm của ba thành viên,

$$D_{\mathrm{MBR}} = C_{\mathrm{MBR}} - \frac{1}{3}\sum_{s \in \{42, 43, 44\}} C_{s}, \qquad \text{(B.4)}$$

trong đó $C_{\mathrm{MBR}}$ là CIDEr-D của phép chọn MBR-3 và $C_s$ là CIDEr-D của thành viên có hạt giống $s$, với khoảng tin cậy bootstrap theo ảnh, B = 5,000. Theo Phụ lục S6, quy tắc là "PASS" nếu cận dưới lớn hơn 0 và "FAIL" nếu ước lượng điểm không lớn hơn 0. Kết quả: 145.15 CIDEr-D trên 558 ảnh kiểm tra, so với 145.55 là trung bình của các thành viên (hạt giống 42, 43 và 44: 144.18, 144.86 và 147.60); hiệu ghép cặp là −0.39 [−2.44, +1.67]; phán quyết đã đăng ký là "FAIL", và khoảng chứa 0. Không điều kiện huỷ nào kích hoạt: CHAIR_i tăng 0.10 điểm, dưới ngưỡng gây hại 1.0 điểm đã đăng ký (K2), và F1 đối tượng thay đổi −0.18 [−0.74, +0.39] (K3). Các thành viên được huấn luyện trên 3,469 ảnh ngoài dev300, còn P1-R dùng cả 3,769 ảnh; như đã đăng ký, điểm tuyệt đối của chúng được đọc theo nghĩa mô tả và khẳng định là hiệu ghép cặp. Không hệ thống nào được huấn luyện lại, và bản đăng ký đóng tập kiểm tra KTVIC sau lần đánh giá này.

**Bảng B.12.** Ba lần nhìn tập kiểm tra KTVIC có liên quan đến đồng thuận hạt giống (Mục 5.1 và Phụ lục S6 của bài).

| Lần nhìn | Thành viên và bộ chấm | Hiệu so với trung bình thành viên | Tình trạng |
|---|---|---|---|
| Phép thay thế thăm dò, thấy trước khi đăng ký | các hạt giống P1-R; CIDEr mức âm tiết với tần suất tài liệu lấy từ tham chiếu kiểm tra | +3.05 [+1.03, +5.11] | exploratory; không dùng để chọn biến thể |
| Lần đánh giá đã đăng ký | ba thành viên huấn luyện trên 3,469 ảnh; bộ chấm của phiếu giao thức; 145.15 so với 145.55 | −0.39 [−2.44, +1.67] | "FAIL" |
| Hàng hậu nghiệm sau khi việc đóng tập kiểm tra được gỡ có công bố | ba đầu ra sẵn có của P1-R (cả 3,769 ảnh); cùng phép chọn, bộ chấm và bootstrap; 151.37 so với 148.23 | +3.14 [+1.11, +5.16] | POST HOC, không phán quyết |

Bài cũng ghi rằng tập kiểm tra KTVIC đã được chấm cho 79 hệ thống của một phép kiểm định thứ hạng, nên trong bài này nó đỡ cho mô tả chứ không cho các khẳng định về phương pháp. Bài không xếp hạng hệ thống tiếng Việt nào: điểm 136.0 của GRIT và các hệ thống sau được chấm dưới giao thức khác về bộ tách từ, thang điểm hoặc dấu câu; hai hệ cơ sở KTVIC, ba hệ thống bên thứ ba ở Mục 3.6 và bảng bốn VLM ở Phụ lục S4 chỉ đi vào theo nghĩa mô tả.

### B.6.2 Chấm chéo bộ dữ liệu trên UIT-ViIC (Mục 5.2 và Phụ lục S9)

**Bảng B.13.** CIDEr-D (×100) trên 231 ảnh kiểm tra UIT-ViIC, lời nhắc ngắn (Mục 5.2 của bài).

| Hệ thống | Dữ liệu huấn luyện | CIDEr-D |
|---|---|---|
| Zero-shot | không | 32.99 |
| P1 (mặt nạ cũ, hạt giống 43) | KTVIC | 41.71 |
| fuse2 (hạt giống 42) | KTVIC | 38.52 |
| P1 (hạt giống 42) | UIT-ViIC (trong miền) | 132.07 |
| fuse2 (hạt giống 42) | UIT-ViIC (trong miền) | 117.70 |

Bài kết luận khuôn mẫu của KTVIC chuyển miền kém xét theo n-gram, và nêu rằng việc dấu câu có giải thích một phần khoảng cách trên UIT-ViIC hay không chưa được đo bằng bộ chấm đã commit. Vì ảnh kiểm tra UIT-ViIC là ảnh COCO train2017 và mọi hệ thống được so ở đây cùng chịu khả năng đã thấy ấy, bài coi đây là so sánh giữa các hệ thống, không phải khẳng định về ảnh chưa thấy.

Về việc lặp lại hiệu ứng hợp nhất trong miền, trên UIT-ViIC chú thích thực thể của COCO cho một tập chuẩn vàng mà không người viết chú thích nào tạo ra. So với tập ấy, fuse2 trong miền nâng F1 đối tượng so với P1 trong miền +6.67 điểm phần trăm [4.63, 8.75] (tập kiểm tra, lời nhắc ngắn). Bài kết luận rằng mức tăng do hợp nhất trên KTVIC không phải là sản phẩm phụ của việc chấm so với chính các tham chiếu mà đích huấn luyện lấy từ đó. Phụ lục S9 bổ sung: trên mười hệ thống UIT-ViIC (chuyển miền và trong miền, lời nhắc ngắn và chi tiết), một mức tăng về sự khớp đối tượng với tham chiếu chuyển sang mức tăng so với nhãn thực thể COCO với hệ số dốc κ = 0.878 [0.457, 1.171]; còn trong kho mẫu của một hệ thống, chọn chú thích theo sự khớp với hai tham chiếu rồi chấm trên các tham chiếu để riêng và nhãn thực thể thì phần chuyển sang, sau khi loại ảnh hưởng của số lượng, là 0.010 [−0.106, 0.131]. Nói cách khác, khác biệt giữa các hệ thống đã huấn luyện chuyển được sang một tập chuẩn vàng không do người viết chú thích tạo, còn việc xếp lại các mẫu trong một kho theo sự khớp với tham chiếu không chuyển được gì ngoài số lượng.

### B.6.3 Một mức tăng theo kích thước tập huấn luyện đo điều gì (Mục 5.3; chỉ dữ liệu phát triển)

Tiểu mục này chỉ báo cáo dữ liệu phát triển: dev300 là một phần tách của tập huấn luyện KTVIC và không ảnh kiểm tra nào đi vào. Nhóm tác giả huấn luyện công thức của hệ thống có kiểm soát trên các tập con lồng nhau của 3,469 ảnh huấn luyện ngoài dev300 (216, 433, 867, 1,734 và 3,469 ảnh), với ba hạt giống ở mỗi kích thước, theo một quy tắc được đăng ký trước khi huấn luyện. Theo tệp đăng ký trước, mô hình thống kê chính là

$$y_{s,L} = a_s + b\,x_L + \varepsilon, \qquad x_L = \log_2 N_L, \qquad \text{(B.5)}$$

trong đó $y_{s,L}$ là CIDEr-D trung bình trên dev300 của hạt giống $s$ ở mức kích thước $L$ (theo tệp đăng ký, đây là cột đã gỡ dấu câu cuối của ứng viên), $N_L$ là số ảnh huấn luyện ở mức ấy, $a_s$ là hệ số chặn riêng của từng hạt giống (hiệu ứng cố định theo hạt giống), và $b$ là hệ số dốc chung, tức số điểm CIDEr-D cho mỗi lần nhân đôi số ảnh huấn luyện KTVIC. Khoảng tin cậy là bootstrap phân vị ghép cặp theo 300 ảnh phát triển với 2,000 lần rút, chỉ bao phủ việc lấy mẫu ảnh. Quy tắc chính được đăng ký nguyên văn là "FUND_EXTERNAL_IMAGE_DATA if CI_lo(b) > +1; CLOSE_DATA_VOLUME_LEVERS if b < +1; INCONCLUSIVE otherwise (reported as PASS / FAIL / INCONCLUSIVE)".

**Bảng B.14.** Kết quả của nghiên cứu kích thước tập huấn luyện trên dev300 (Mục 5.3 của bài; hệ số dốc tính bằng điểm CIDEr-D ×100 cho mỗi lần nhân đôi). Chỉ dữ liệu phát triển, một mô hình nền.

| Hàng | Ước lượng | Số ảnh | Tình trạng |
|---|---|---|---|
| Hệ số dốc gộp, đã đăng ký | +9.61 [7.18, 12.36] | 300 | "PASS" |
| Hàng độ nhạy đã đăng ký: bỏ một ảnh phát triển trùng từng byte với một ảnh huấn luyện chỉ dùng ở kích thước lớn nhất | +9.61 [7.17, 12.37] | 299 | mô tả; cùng quy tắc áp dụng theo nghĩa mô tả cũng cho "PASS"; không phán quyết |
| Bỏ 7 ảnh phát triển có ảnh trùng từng byte hoặc gần trùng trong tập huấn luyện | +9.77 [7.28, 12.53] | 293 | POST HOC, mô tả |
| Hệ số dốc theo từng hạt giống | 9.50, 9.62 và 9.71 | 300 | mô tả |
| Hệ số dốc của F1 đối tượng so với tập chuẩn vàng KTVIC (bộ so khớp lớp chính xác) | +1.19 [0.60, 1.81] | 300 | mô tả |
| Kết quả tiền thân một hạt giống (Phụ lục S6) | +9.40 | 300 | kết quả phát triển trước đó |

Bài nêu rằng nghiên cứu này là lần xác nhận ba hạt giống đã đăng ký cho kết quả tiền thân một hạt giống, mà kết quả đã đăng ký của nó là khuyến nghị thêm dữ liệu ảnh bên ngoài, và rằng ngưỡng đạt được đặt thấp hơn hẳn kết quả ấy. Độ dài đầu ra trung bình giữ gần 11.8 âm tiết ở mọi kích thước.

Một phép thử ngoại suy được đăng ký riêng hỏi liệu các đường cong khớp trên bốn kích thước nhỏ hơn có dự đoán được điểm ở kích thước đầy đủ trong phạm vi ±2.0 CIDEr-D hay không. Theo tệp đăng ký của nó, đại lượng ước lượng là sai số dự đoán

$$e = \frac{1}{|S|}\sum_{s \in S}\left(y_{s,L5} - \hat{y}_{s,L5}\right), \qquad \text{(B.6)}$$

với $S$ là tập các hạt giống của hàng đang xét, $y_{s,L5}$ là điểm quan sát ở kích thước đầy đủ và $\hat{y}_{s,L5}$ là dự đoán của đường cong khớp trên bốn kích thước nhỏ; $e > 0$ nghĩa là dạng đường cong dự đoán thấp. Ba dạng được cố định trước là tuyến tính theo logarit, luỹ thừa trên thang log–log, và luỹ thừa bão hoà. Quy tắc ba ngả với ngưỡng T = 2.0 là: "EXTRAPOLATES" nếu cả khoảng tin cậy nằm trong [−T, +T]; "FAILS" nếu khoảng không giao với [−T, +T]; "INCONCLUSIVE" trong các trường hợp còn lại. Kết quả bài in: với cả ba dạng, khoảng tin cậy giao với ngưỡng mà không nằm trọn trong đó, nên phán quyết là "INCONCLUSIVE"; với dạng tuyến tính theo logarit trên các hạt giống 43 và 44, sai số dự đoán là +1.93 [−6.65, +11.05]. Bài khép tiểu mục bằng nhận định rằng mức tăng là lớn và tương tự nhau giữa các hạt giống.

**Nhận xét rà soát.** Mục 5 báo cáo thẳng các kết quả thất bại và giữ đúng nhãn cho các hàng hậu nghiệm. Các điểm cần xem lại được xếp theo tiểu mục.

Về Mục 5.1. (i) Bảng 5.1 chỉ có độ lệch chuẩn cho P1-R; các hàng khác là trung bình ba hạt giống không kèm độ phân tán, và trung bình của P1 gồm lần chạy 149.79 mà bài tự cho là không tái lập được. (ii) Bảng B.12 cho thấy hai lần nhìn không đăng ký trên các đầu ra P1-R cho hiệu dương với khoảng không chứa 0, còn lần đã đăng ký trên các thành viên huấn luyện trên 3,469 ảnh cho "FAIL". Bài xử lý đúng (hàng hậu nghiệm không có phán quyết), nhưng không đưa ra giải thích nào cho sự khác dấu, và phản biện sẽ hỏi. Khi viết lại không được biến hàng hậu nghiệm thành bằng chứng ủng hộ phương pháp. (iii) Phép chọn MBR-3 không được định nghĩa ở đâu trong văn bản hiển thị: chữ viết tắt không được khai triển và tiêu chí chọn giữa ba đầu ra không được mô tả. (iv) Việc 16 trên 558 ảnh kiểm tra có ảnh trùng hoặc gần trùng trong tập huấn luyện (Mục 3.1) không được nhắc lại ở phép thử cuối cùng.

Về Mục 5.2. (i) Mọi con số là một hạt giống, và hai hệ thống chuyển miền dùng hai hạt giống khác nhau (43 và 42). (ii) Kết luận "The fusion gain on KTVIC is not an artifact ..." suy từ UIT-ViIC sang KTVIC và dựa trên F1 thô, trong khi Mục 6.2 và khuyến nghị 4 của Mục 6.4 yêu cầu so sánh ở số lượng khớp trước khi nói về mức tăng. Bảng 5.1 cho thấy fuse2 nêu nhiều đối tượng hơn; bài cần nói mức tăng +6.67 điểm phần trăm có được kiểm ở số lượng khớp hay không. (iii) Yếu tố dấu câu trên UIT-ViIC chưa đo, như đã nêu ở B.4.

Về Mục 5.3, đây là kết quả tích cực duy nhất có phán quyết đã đăng ký trong thân bài, nên cần chặt nhất. (i) Tiêu đề tiểu mục và câu hỏi của bài hứa trả lời một mức tăng "đo điều gì", nhưng nội dung chỉ xác lập rằng mức tăng tồn tại so với tham chiếu KTVIC trên dữ liệu phát triển; chính Mục 6.3 viết rằng không thể phân biệt mô tả tốt hơn với sự khớp gần hơn với người viết của KTVIC nếu chỉ dùng tham chiếu KTVIC. Tiêu đề và tóm tắt nên được chỉnh cho khớp với điều thực sự được chứng minh. (ii) Tệp đăng ký yêu cầu in cả 15 điểm của đường cong trong một bảng phụ lục, kèm điểm zero-shot, tỉ lệ trùng của bước kiểm tra giải mã lại và hai hàng lặp lại; phụ lục hiện hành không có bảng này. (iii) Tệp đăng ký định nghĩa một quy tắc phụ theo hạt giống ("STABLE iff every b_s > +1"), độ cong và bước tăng ở hai kích thước lớn nhất như các đại lượng được báo cáo, và việc in dự đoán đóng băng [0, +2] của hệ số dốc F1 là trúng hay trượt; bài in ba hệ số dốc theo hạt giống và hệ số dốc F1 nhưng không in các nhãn và đại lượng ấy. (iv) Tệp đăng ký ghi rõ bộ chấm của nghiên cứu này không phải bộ chấm của kết quả tiền thân, nên +9.61 và +9.40 nằm trên hai thang chấm khác nhau; bài gọi nghiên cứu này là "confirmation" của +9.40 mà không nói điều đó và không in hàng lặp lại trên cùng thang mà bản đăng ký đã dự liệu. (v) Tệp đăng ký của phép thử ngoại suy tự nhận phép thử không mù ở kích thước đầy đủ (các tác giả đã biết điểm của công thức ấy trên một hạt giống và trên tập kiểm tra) và quy định mọi câu báo cáo kết quả chính phải kèm lời công bố này; câu trong Mục 5.3 không có lời công bố ấy, và chỉ in ước lượng của một trong ba dạng đường cong. (vi) Khoảng [−6.65, +11.05] rộng hơn nhiều so với ngưỡng ±2.0, nên phép thử gần như không thể cho kết luận; nên nói rõ đây là giới hạn về lực của thiết kế. (vii) Bộ so khớp dùng cho F1 đối tượng ở đây được gọi là "exact-class matcher", không gắn với v1, v2 hay v3 của Mục 3.5. (viii) Khoảng tin cậy chỉ gồm việc lấy mẫu ảnh; với ba hạt giống, bài nên nhắc lại ngay tại Mục 5.3 rằng phương sai giữa các hạt giống không nằm trong khoảng, như Mục 7.1 đã nói.

## B.7 Mục 6 của bài: Thảo luận (Discussion)

**Nội dung.** Mục 6 tổng hợp các phát hiện thành câu trả lời cho câu hỏi của bài, báo cáo một nghiên cứu phát triển đã đăng ký trước về một điểm số không cần tham chiếu, và đưa ra các khuyến nghị.

### B.7.1 Một điểm CIDEr trên KTVIC đo điều gì (Mục 6.1)

Gộp các Mục 3–5, bài xác định bốn nguồn biến thiên trong một điểm CIDEr trên KTVIC và nói rõ chúng không phải là các phần cộng được: mỗi nguồn được đo trên một phép so sánh khác nhau. Nguồn thứ nhất là sự thích nghi với bài toán và sự khớp khuôn mẫu: một hệ thống tinh chỉnh trên KTVIC học định dạng bài toán (một câu tiếng Việt ngắn) và mẫu câu ngắn, không dấu câu của một người viết, và bài không tách hai thứ này; dưới giao thức đã commit, tinh chỉnh đưa điểm từ 28.98 (zero-shot) lên vùng 140, và chỉ riêng việc gỡ dấu chấm cuối của đầu ra zero-shot đã nâng điểm lên 33.30. Nguồn thứ hai là dấu câu, ở nơi quy trình giữ nó: một dấu chấm mỗi chú thích làm một hệ thống không bao giờ đặt dấu câu mất 35.17 điểm, còn với cách xoá kiểu PTB thì không mất gì. Nguồn thứ ba là cách tách token: tách từ so với tách theo âm tiết làm cùng đầu ra thay đổi 15.64 điểm, còn một bộ tách từ thứ hai làm thay đổi chưa tới một điểm. Nguồn thứ tư là nội dung hình ảnh, tức điều mà điểm số được thiết kế để đo. Ba nguồn đầu là thuộc tính của giao thức và của người viết tham chiếu, không phải của hình ảnh, và dưới giao thức đã commit mỗi nguồn đều lớn hơn khoảng cách giữa hệ thống của bài và điểm GRIT được báo cáo. Bài kết luận: một chênh lệch CIDEr trên KTVIC chỉ diễn giải được giữa các hệ thống chung bộ tách từ, chính sách dấu câu và phong cách tham chiếu, và ngay cả khi ấy nó vẫn thưởng cho việc khớp với một người viết.

### B.7.2 Điểm đối tượng cần kiểm soát số lượng và một tập chuẩn vàng được ghi rõ (Mục 6.2)

Các độ đo ở mức đối tượng tránh được vấn đề khuôn mẫu nhưng gặp hai vấn đề khác. Về số lượng, trong Bảng 5.1 F1 đối tượng cao hơn của fuse2 đi cùng việc nêu nhiều đối tượng hơn, và mọi biện pháp trong phụ lục từng nâng F1 đối tượng thô đều làm vậy bằng cách nêu nhiều đối tượng hơn (Phụ lục S2, S5). Về tập chuẩn vàng không đầy đủ của một người viết, năm tham chiếu của KTVIC là lời kể của một người (Mục 3.2), và coi chúng là năm lời kể độc lập là phóng đại mức bao phủ ảnh của chúng.

Cùng tiểu mục này, bài báo cáo một nghiên cứu phát triển đã đăng ký trước về điểm kiểm chứng đối tượng phân rã (decomposed object-verification score), một điểm số không dùng chú thích tham chiếu. Một mô hình ngôn ngữ tách một chú thích thành các mệnh đề; một mô hình thị giác–ngôn ngữ trả lời có hoặc không cho từng mệnh đề đối tượng ánh xạ được sang một lớp Objects365; điểm số là tỉ lệ các mệnh đề ấy được trả lời có,

$$s(c) = \frac{n_{\mathrm{yes}}(c)}{n_{\mathrm{obj}}(c)}, \qquad \text{(B.7)}$$

trong đó $n_{\mathrm{obj}}(c)$ là số mệnh đề đối tượng của chú thích $c$ ánh xạ được sang một lớp Objects365 và $n_{\mathrm{yes}}(c)$ là số mệnh đề trong đó được trả lời có.

Cùng mô hình thị giác–ngôn ngữ ấy, khi được hỏi một lần cho mỗi chú thích rằng mọi đối tượng được nêu có hiện diện hay không, đóng vai trò bộ phán có/không cùng mô hình nền (same-backbone yes/no judge). Nghiên cứu dùng 2,000 ảnh huấn luyện của Objects365 v2, được bốn hệ sinh chú thích tạo chú thích tiếng Việt; tiêu chí là độ chính xác đối tượng theo tập chuẩn vàng hộp bao (box-gold object precision).

**Bảng B.15.** Nghiên cứu phát triển đã đăng ký trước về điểm kiểm chứng đối tượng phân rã (Mục 6.2 của bài). Chỉ dữ liệu phát triển trên ảnh thuộc tập huấn luyện; cấu hình tốt nhất trong ba cấu hình đã đăng ký được chọn trên chính các ảnh này; không có đánh giá trên dữ liệu để riêng.

| Đại lượng | Giá trị |
|---|---|
| Số chú thích mà cả điểm số lẫn tiêu chí đều xác định | 2,579 (trong 5,541 chú thích có nêu đối tượng ánh xạ được) |
| Kendall τ_c của điểm kiểm chứng đối tượng phân rã với độ chính xác đối tượng theo hộp bao | 0.068 |
| Kendall τ_c của bộ phán có/không cùng mô hình nền | 0.104 |
| Kendall τ_c của CLIPScore đa ngữ | 0.094 |
| Hiệu so với bộ phán | −0.036 (cận dưới một phía 95%: −0.061) |
| Hiệu ứng nhỏ nhất đáng quan tâm đã đăng ký | 0.02 |
| Hệ quả | quy tắc dừng đã đăng ký kết thúc nghiên cứu trước giai đoạn diễn tập và giai đoạn dữ liệu để riêng |

Bài viết rằng hiệu so với bộ phán "fell short of the preregistered smallest effect of interest of 0.02, so the preregistered stop rule ended the study before the rehearsal and held-out stages", và khép lại bằng ba lời rào: đây là kết quả phát triển chỉ trên ảnh thuộc tập huấn luyện, với cấu hình tốt nhất trong ba cấu hình đã đăng ký được chọn trên chính các ảnh ấy; không có đánh giá trên dữ liệu để riêng nào được chạy; và bài không đưa ra khẳng định nào về tính hợp lệ của điểm số này.

### B.7.3 Một mức tăng do dữ liệu huấn luyện trên KTVIC đo điều gì (Mục 6.3)

Trên dữ liệu phát triển với một mô hình nền, thêm ảnh huấn luyện KTVIC nâng CIDEr-D so với tham chiếu KTVIC +9.61 cho mỗi lần nhân đôi (Mục 5.3). Bài nhấn mạnh đây là kết quả phát triển so với một tập tham chiếu và chưa có xác nhận trên dữ liệu để riêng. Việc một mức tăng như vậy phản ánh mô tả tốt hơn hay sự khớp gần hơn với chính người viết của KTVIC thì không thể phân định chỉ từ tham chiếu KTVIC; một khẳng định về mô tả tốt hơn cần một tập tham chiếu viết riêng rẽ và đánh giá của con người, những thứ bài này không thu thập.

### B.7.4 Khuyến nghị, bộ công cụ và vai trò của hệ thống có kiểm soát (Mục 6.4–6.6)

Bài đưa ra sáu khuyến nghị cho đánh giá chú thích ảnh tiếng Việt. (1) Báo cáo một phiếu giao thức cùng mọi điểm số: bộ tách từ và phiên bản, biến thể CIDEr, thang điểm, chính sách dấu câu, số tham chiếu và cách giải mã. (2) Khôi phục bước xoá dấu câu của bộ tách PTB, hoặc báo cáo CIDEr có và không có bước ấy, khi một quy trình tiếng Việt thay bộ tách đó bằng một bộ tách từ; nêu quy trình nào tạo ra mỗi điểm được so sánh. (3) Công bố bộ so khớp đối tượng cùng điểm đối tượng, nói rõ quy tắc có được người kiểm hay không, và không rút kết luận phụ thuộc vào quy tắc chưa được xác nhận. (4) So các độ đo đối tượng ở số lượng khớp trước khi khẳng định mức tăng độ chính xác. (5) Dùng một tập chuẩn vàng thứ hai ở nơi có, như nhãn thực thể COCO cho UIT-ViIC. (6) Không gọi sự đồng thuận trong cùng người viết là trần của con người trên KTVIC.

Phần lớn khuyến nghị có một thành phần tương ứng trong bộ công cụ (Bảng S13.1; xem Bảng B.25); khuyến nghị 4 dựa vào các đối chứng của bài song hành. Các tập lệnh cần chú thích KTVIC, OpenViIC hay COCO đọc chúng từ bản của người đọc, và không thứ gì suy ra theo từng ảnh từ OpenViIC rời khỏi máy của người đọc. Áp dụng cho ba hệ thống bên thứ ba trên tập kiểm tra của riêng chúng, bộ công cụ đã báo cáo khuyến nghị 1 và 2 cho từng hệ thống: các cột của phiếu giao thức và CIDEr-D có và không có bước xoá dấu câu. Về vai trò của hệ thống có kiểm soát, P1-R là một hệ cơ sở đơn giản, ổn định: ba hạt giống nằm trong phạm vi 0.7 CIDEr-D của nhau, với điểm đã commit được máy thứ hai tái lập đúng từng byte. Giá trị của nó ở đây nằm ở vai trò công cụ hơn là ở điểm số: vì mô hình nền, công thức và cách giải mã được cố định, các khác biệt mà bài quy cho tham chiếu, dấu câu, bộ so khớp và tập chuẩn vàng không thể là khác biệt giữa các kiến trúc.

**Nhận xét rà soát.** Mục 6.1, 6.3 và 6.4 diễn đạt cẩn trọng và khớp với bằng chứng. Vấn đề chính nằm ở Mục 6.2.

Thứ nhất, nghiên cứu ở Bảng B.15 là một kết quả thực nghiệm mới được đưa vào lần đầu ngay trong phần thảo luận. Nó không có phần phương pháp, không có mục trong phụ lục, và không được tóm tắt, mở đầu hay kết luận nhắc tới. Văn bản không nêu tên mô hình ngôn ngữ, mô hình thị giác–ngôn ngữ, bốn hệ sinh chú thích hay mô hình của "multilingual CLIPScore"; không nêu ba cấu hình là gì; không in tổng số chú thích; và không phát biểu quy tắc quyết định dưới dạng đầy đủ. Bảng kê số liệu cho thấy ngưỡng 0.02 đến từ một quy tắc có dạng giá trị lớn hơn giữa 0.02 và hai lần sai số chuẩn (ghi chú "registered SESOI rule max(0.02, 2 SE_A)"), điều mà văn bản không nói. Objects365 không có trong danh sách dữ liệu của Mục 3.1, đoạn "Datasets" của Mục 3.6, Bảng S12.1 hay tệp bib.

Thứ hai, nghiên cứu này không có nhãn đăng ký theo hệ bốn nhãn của Phụ lục S1, trong khi Mục 7.4 viết rằng mọi phép thử mang một trong bốn nhãn. Phụ lục tự mô tả là hồ sơ đầy đủ của các phép thử, nên nghiên cứu này cần một mục hồ sơ ở đó.

Thứ ba, tiêu đề tiểu mục nói về kiểm soát số lượng và tập chuẩn vàng, trong khi đoạn này nói về một điểm số không cần tham chiếu; mạch lập luận nối hai phần không được viết ra. Có hai cách sửa: chuyển nghiên cứu sang phụ lục và để lại một câu dẫn kèm lời rào, hoặc dành cho nó một tiểu mục riêng với mô tả phương pháp tối thiểu.

Thứ tư, cách diễn đạt kết quả cần giữ nguyên mức độ. Bài không in một từ phán quyết nào cho nghiên cứu này; điều bài in là hiệu so với bộ phán không đạt hiệu ứng nhỏ nhất đáng quan tâm và quy tắc dừng đã kích hoạt. Khi viết lại không nên đổi thành "điểm số không hợp lệ": kết quả chỉ là trên dữ liệu phát triển, với cấu hình được chọn trên chính dữ liệu ấy, và bài chỉ nói mình không khẳng định tính hợp lệ.

Thứ năm, bài dùng ba ký hiệu tương quan thứ hạng ở ba nơi (τ ở Mục 3.4, τ_b ở Phụ lục S4, τ_c ở Mục 6.2) mà không giải thích lý do chọn từng biến thể.

Thứ sáu, câu cuối Mục 6.6, "Every result in the main text comes from one model", và câu tương ứng ở Mục 7.1 không còn đúng theo nghĩa đen: Mục 3.6 báo cáo ba hệ thống bên ngoài và Mục 6.2 dùng bốn hệ sinh chú thích cùng một bộ phán. Nên giới hạn câu này vào các hệ thống do nhóm tác giả huấn luyện.

Thứ bảy, khuyến nghị 4 dựa vào một công cụ của bài song hành chưa công bố và không có trong bộ công cụ; phản biện có thể hỏi người đọc thực hiện khuyến nghị này bằng cách nào trước khi bài kia xuất hiện.

## B.8 Mục 7 của bài: Hạn chế và đạo đức (Limitations and ethics), gồm các tuyên bố

**Nội dung.** Mục 7 gồm năm tiểu mục: hạn chế; dữ liệu, giấy phép và phát hành; quan hệ với bài hội nghị và bài song hành; nguồn gốc phân tích; và Statements and Declarations.

### B.8.1 Hạn chế (Mục 7.1)

Bài nêu chín hạn chế. Một họ mô hình: mọi kết quả trong thân bài đến từ Qwen2.5-VL-7B-Instruct với một công thức QLoRA; mô hình nền thứ hai đã đăng ký (Qwen3-VL-8B-Instruct) dừng ở bước kiểm zero-shot, và đầu ra của phương án dự phòng 3B chưa được kiểm chứng và không được báo cáo; các phát hiện kiểm định về tham chiếu không phụ thuộc vào mô hình, nhưng điểm của hệ thống thì có. Các phép thử phía phương pháp: thang giám sát, bảng xếp hạng và các biện pháp can thiệp chỉ được báo cáo trong phụ lục, phần lớn với một hạt giống; phép thử duy nhất đã đăng ký trước của hệ thống cuối cùng trả về "FAIL": −0.39 [−2.44, +1.67] CIDEr-D so với trung bình các thành viên. Không có đánh giá của con người: không thu chú thích mới của người; các con số bỏ-một-ra trong cùng người viết không phải trần của con người; tín hiệu do mô hình sinh ra (phiếu bầu mẫu, tiên nghiệm kNN) chỉ phục vụ bên trong phương pháp. Về các đánh giá của người trước đây, bài viết rằng các đánh giá của bản FAIR 2026 (2 người chấm, 150 chú thích) vượt cổng đồng thuận đặt trước (điểm giống hệt nhau trên 71–87% chú thích cho mỗi thang, so với ngưỡng 50%), nên, như đã cố định trước, không phân tích tiêu chí nào được chạy; cổng là một quy tắc dừng đặt trước khi tính bất kỳ thống kê nào, không phải một phán quyết về các đánh giá ấy, và các đánh giá ấy không là bằng chứng cho khẳng định nào trong bài. Nghiên cứu kích thước tập huấn luyện chỉ ở mức phát triển: dùng dev300 và một mô hình nền; kết quả dừng ở mức thăm dò–phát triển vì tập kiểm tra KTVIC đã đóng với bài này theo quy tắc một lần nhìn, và một xác nhận cần một lần nhìn duy nhất mới được đăng ký trên dữ liệu chưa adapter nào được chỉnh hay đọc; các khoảng chỉ lấy mẫu lại ảnh nên không gồm phương sai giữa các hạt giống. Bộ so khớp v3 chưa được xác nhận. Các phân tích thăm dò và hậu nghiệm: hàng xoá dấu câu kiểu PTB ở Mục 3.3 được thêm sau một lần rà soát nội bộ và là hậu nghiệm; các kết quả v3 là phân tích độ nhạy; các bản đăng ký được định trước và có dấu thời gian nội bộ (commit và mã băm tệp trong kho của nhóm) nhưng không được nộp cho một cơ quan đăng ký bên ngoài. Về đối chứng: không có khẳng định xếp hạng nào; toàn văn HDUCap và ViG không lấy được. Về hệ thống bên ngoài: lần chạy gồm ba hệ thống, mỗi bộ dữ liệu một hệ thống, đều từ checkpoint vì không tệp nào trong mười tệp đầu ra đã công bố qua được cổng cấu trúc; nhóm tự giải mã với thiết lập do từng tác giả ghi lại, trong môi trường của mình, nên lần chạy cho thấy bộ công cụ chấm được đầu ra nó không tạo ra, không cho thấy một nhóm bên ngoài đã dùng bộ công cụ, cũng không cho thấy các lần giải mã tái tạo đầu ra của tác giả; hai hệ thống chỉ được báo cáo ở dạng tổng hợp vì giấy phép, và lần chạy không đỡ cho khẳng định nào về chất lượng của bất kỳ hệ thống nào.

### B.8.2 Dữ liệu, giấy phép, phát hành và con người trong ảnh (Mục 7.2)

Bài không phân phối lại ảnh hay tham chiếu. Bộ công cụ chứa mã và tài liệu của nhóm, các tệp đăng ký trước, bản sao chỉ còn điểm số của các tệp kết quả được trích và bảng kê số liệu; mã sẽ phát hành theo giấy phép MIT (còn chờ tác giả xác nhận) và sẽ được lưu trên Zenodo trước khi bản thảo được gửi phản biện (DOI còn trống). UIT-ViIC chỉ xuất hiện dưới dạng tổng hợp và con trỏ, không khẳng định có sự cho phép của tác giả bộ dữ liệu. Đầu ra hệ thống và trọng số tinh chỉnh không được phát hành. Qwen2.5-VL-7B-Instruct theo giấy phép Apache-2.0 và Qwen2.5-VL-3B-Instruct theo Qwen Research License Agreement chỉ cho mục đích phi thương mại. Về con người trong ảnh: chú thích mô tả cảnh đời thường có người; không thực hiện nhận dạng danh tính; tham chiếu và đầu ra hệ thống dùng danh từ chỉ vai và giới; các quy tắc so khớp cho những danh từ này được ghi lại để có thể xem ảnh hưởng của chúng lên điểm số, và bài không báo cáo phân tích nào theo giới.

### B.8.3 Quan hệ với bài hội nghị và bài song hành (Mục 7.3)

Bài hội nghị trước [@nguyen2026vsps] chia sẻ một phần thiết lập; đóng góp của nó, giám sát VSPS từ các mệnh đề đã kiểm chứng, không phải đóng góp của bài này. Thứ được dùng lại là thiết lập KTVIC/COCO, công thức QLoRA và hệ đối chứng P1; điểm hạt giống 42 của P1 (149.8 ở đó, 149.79 ở đây dưới cùng bộ chấm) chỉ làm mốc tham chiếu. Bảng S12.1 so bài này với bản thảo song hành đang soạn [@companion2026underreview]; không con số nào là kết quả chính ở cả hai bài; mỗi bài có kho lưu trữ riêng. Sự chồng lấn còn đi qua thống kê hoán đổi được: nó được định nghĩa ở bài song hành, nơi báo cáo nó trên các kho ngữ liệu khác và để KTVIC cho bài này, nên mỗi bài dựa vào bài kia cho một nửa của sự tương phản.

### B.8.4 Nguồn gốc phân tích (Mục 7.4)

Bài nêu năm quy tắc. Mọi con số được đọc từ một tệp đầu ra, hoặc từ một phép suy dẫn được nêu rõ từ các giá trị ấy, hoặc được trích từ tài liệu, và được liệt kê trong bảng kê số liệu kèm mã băm tệp khi có; bảng kê sẽ được lưu trữ cùng bản sao chỉ còn điểm số của các tệp nguồn, và các hàng trích nguồn không phát hành được sẽ được đánh dấu là giữ lại. Một con số không có nguồn tính toán thì không được dùng. Mọi phép thử mang một trong bốn nhãn đăng ký, tính từ thời điểm commit, đẩy lên kho từ xa, tệp và đầu ra (Phụ lục S1); chỉ các phép thử có dự đoán được commit trước đầu ra mà chúng dự đoán mới được tính là đã đăng ký, các phép thử khác được coi là thăm dò; kho lưu trữ sẽ kèm các tệp đăng ký trước nhưng không kèm lịch sử quản lý phiên bản, nên thời điểm commit đứng sau các nhãn là tự chứng thực: người đọc kiểm được tệp khớp mã SHA-256 được trích, nhưng không kiểm được chúng được commit khi nào. Tín hiệu do mô hình sinh ra không bao giờ là chuẩn vàng hay bằng chứng của người, và không có chú thích mới nào của người được thu. Mọi mã định danh được trích đều được kiểm trên trang gốc, và bài chưa đọc thì được trích mà không dùng số của nó. Các tác giả nhận trách nhiệm về mọi phân tích và văn bản.

### B.8.5 Statements and Declarations (Mục 7.5)

Về tài trợ, nghiên cứu không nhận tài trợ bên ngoài; mọi chi phí, gồm cả thời gian GPU thuê, do nhóm tác giả chịu. Về xung đột lợi ích, các tác giả tuyên bố không có. Về phê duyệt đạo đức, bài ghi không áp dụng vì không thu dữ liệu mới từ người tham gia. Về tính sẵn có của dữ liệu và mã, bài dẫn về Mục 3.6: bộ công cụ sẽ phát hành theo giấy phép MIT (còn chờ xác nhận) và dữ liệu lấy từ nguồn gốc. Về đóng góp của tác giả theo CRediT: tác giả thứ nhất đảm nhận hình thành ý tưởng, phương pháp, phần mềm, thẩm định, phân tích hình thức, khảo sát, quản lý dữ liệu, viết bản thảo gốc, rà soát và biên tập, trực quan hoá và quản trị dự án; tác giả thứ hai và tác giả thứ ba (tác giả liên hệ) cùng đảm nhận hình thành ý tưởng, phương pháp, giám sát, rà soát và biên tập.

**Nhận xét rà soát.** Mục 7 là điểm mạnh của bài về tính minh bạch. Các việc cần làm như sau.

Thứ nhất, danh sách hạn chế chưa có bốn mục mà thân bài đã tự nêu ở nơi khác hoặc cần nêu: nghiên cứu phát triển ở Mục 6.2 và giới hạn của nó; các ảnh trùng và gần trùng giữa tập huấn luyện và tập kiểm tra ở Mục 3.1 cùng việc chỉ một con số được tính lại; việc mức độ phổ biến của các quy trình bỏ bước xoá dấu câu không có nguồn; và việc mọi kết luận kiểm định chỉ về một bộ chuẩn, không có dữ liệu tiếng Anh để đối chiếu (Bảng S12.1 ghi "none").

Thứ hai, đoạn "Earlier human ratings" khó hiểu với người đọc bên ngoài: nó nói các đánh giá "exceeded our pre-set agreement gate" và vì thế không phân tích nào được chạy, trong khi trực giác thông thường coi đồng thuận cao là điều tốt. Cần một câu nói rõ cổng này nhằm phát hiện điều gì (theo cách diễn đạt của bài, đây là một quy tắc dừng chứ không phải phán quyết về các đánh giá) và vì sao đồng thuận vượt ngưỡng lại dẫn đến dừng.

Thứ ba, Mục 7.3 chỉ nói về một bài song hành, trong khi thư gửi ban biên tập công bố thêm một bản thảo liên quan thứ hai có dùng lại một nửa tập kiểm tra KTVIC trong vai trò phát triển. Vì Mục 5.1 và Mục 7.1 nhấn mạnh tập kiểm tra KTVIC đã đóng, người đọc cả hai bản thảo sẽ cần một câu ở Mục 7.3 giải thích hai điều này tương thích ra sao (Mục 7.1 đã dùng cụm "for this paper").

Thứ tư, sơ đồ mục trong `outline_B.md` gọi Mục 7.4 là "AI-agent provenance" và `STATUS.md` còn mục chờ tác giả xác nhận về công cụ AI và văn bản do AI soạn, nhưng Mục 7.4 hiện hành không có câu nào về việc dùng công cụ AI. Tác giả cần đọc lại chính sách hiện hành của tạp chí và quyết định có khai báo hay không, ở đâu; báo cáo này không đề xuất nội dung khai báo.

Thứ năm, bảng kê số liệu chưa đồng bộ với văn bản: nhiều hàng còn ghi vị trí theo số mục cũ (ví dụ "§5.4", "S7", "Supplement S9 Table S9.1") trong khi văn bản hiện hành dùng Mục 5.3, Phụ lục S6 và Bảng S8.1; và bảng kê còn các hàng mang nhãn đã rút cho những nghiên cứu không còn trong bài. Vì Mục 7.4 cam kết lưu trữ bảng kê, cần làm sạch trước khi nộp lưu trữ.

Thứ sáu, phần Statements and Declarations hiện nằm trước Mục 8, trong khi thư mục bài ghi yêu cầu của tạp chí là đặt ngay trước danh mục tài liệu tham khảo; các chỗ trống về giấy phép và DOI lặp lại ở Mục 7.2 và Mục 7.5.

Thứ bảy, việc các bản đăng ký không được nộp cho cơ quan bên ngoài và chỉ tự chứng thực đã được công bố trung thực; phản biện có thể vì thế coi nhẹ chữ "registered". Bài nên chuẩn bị sẵn cách cho ban biên tập kiểm dấu thời gian nếu được yêu cầu.

## B.9 Mục 8 của bài: Kết luận (Conclusion)

**Nội dung.** Kết luận gồm ba đoạn. Đoạn thứ nhất viết rằng một điểm CIDEr trên KTVIC đo nhiều thứ ngoài hình ảnh: tham chiếu từ một người viết, theo tài liệu của KTVIC và thống kê của bài (tỉ lệ kề nhau 0.7102 so với 0.40 cho các vị trí hoán đổi được và 0.45 dưới một phân phối không giữ tỉ lệ theo vị trí); một quy ước dấu câu mà cái giá phụ thuộc vào quy trình (thêm dấu chấm làm một hệ tinh chỉnh không bao giờ đặt dấu câu mất 35.17 điểm CIDEr-D trong quy trình không có bước xoá dấu câu PTB, và không mất gì với cách xoá kiểu PTB); cách tách từ (15.64 điểm so với tách theo âm tiết); và các quy tắc so khớp. Trên dữ liệu phát triển với một mô hình nền, mỗi lần nhân đôi số ảnh huấn luyện KTVIC nâng CIDEr-D so với tham chiếu KTVIC +9.61 [7.18, 12.36] (đã đăng ký); việc xác nhận kết quả phát triển này cần một lần nhìn duy nhất đã đăng ký trong tương lai trên dữ liệu chưa thấy.

Đoạn thứ hai viết rằng không hiệu ứng nào trong số này nói về việc hệ thống nào mô tả ảnh tốt hơn, và rằng dưới giao thức đã commit, hiệu ứng thêm dấu chấm và hiệu ứng tách từ mỗi cái đều lớn hơn khoảng cách được báo cáo giữa hệ thống có kiểm soát và điểm GRIT đã công bố. KTVIC vẫn hữu ích nhưng chỉ với một giao thức được nêu rõ: bộ tách từ, biến thể CIDEr, thang điểm, chính sách dấu câu và bộ so khớp, báo cáo cùng mọi điểm số, và các phép so đối tượng được thực hiện ở số lượng khớp hoặc so với một tập chuẩn vàng thứ hai. Phiếu giao thức và bộ công cụ sẽ phát hành cùng bài làm cho việc báo cáo ấy rẻ, và các tập lệnh chạy được trên bất kỳ bộ dữ liệu tiếng Việt nào người đọc có. Theo một bản đăng ký trước chỉ nhằm mô tả, nhóm đã chạy bộ công cụ trên 3 hệ thống bên ngoài từ 3 nguồn (điểm mô tả, không xếp hạng); nó báo cáo mọi cột giao thức cho từng hệ thống; chưa nhóm bên ngoài nào chạy nó.

Đoạn thứ ba viết rằng phụ lục ghi lại, với phán quyết không đổi, các phép thử huấn luyện và giải mã đã đăng ký trước chạy với cùng hệ thống: không phép thử nào tạo ra mức tăng được xác nhận trên tập kiểm tra. Phép thử duy nhất đã đăng ký trước của hệ thống cuối cùng không nâng CIDEr-D so với trung bình các thành viên (−0.39 [−2.44, +1.67]; phán quyết đã đăng ký "FAIL").

**Nhận xét rà soát.** Kết luận trung thành với thân bài và giữ kết quả thất bại ở vị trí dễ thấy. Có bốn điểm nhỏ. (i) Câu mở đầu liệt kê "matcher rules" trong những thứ mà "A KTVIC CIDEr score measures", nhưng quy tắc so khớp chỉ ảnh hưởng đến điểm đối tượng, không ảnh hưởng đến CIDEr; nên viết "A KTVIC score" hoặc tách thành hai câu. (ii) Cụm "their scripts run on any Vietnamese dataset a reader holds" rộng hơn điều đã được thử; bằng chứng trong bài là các lần chạy trên KTVIC, UIT-ViIC, UIT-OpenViIC và XM3600. (iii) Câu "None of these effects is about which system describes the image better" đúng với ba hiệu ứng giao thức, nhưng hệ số dốc theo dữ liệu huấn luyện được nhắc ngay trước đó là trường hợp mà chính Mục 6.3 nói chưa phân định được; nên tách hệ số dốc khỏi phạm vi của chữ "these". (iv) Kết luận không nhắc nghiên cứu ở Mục 6.2 và các kết quả UIT-ViIC; nếu Mục 6.2 được giữ trong thân bài thì cần một mệnh đề ở đây.

## B.10 Phụ lục trực tuyến của bài (Supplementary material: the method-side record)

**Nội dung.** Phụ lục tự mô tả như sau: thân bài kiểm định một điểm KTVIC đo điều gì, nêu giao thức chấm trong một phiếu giao thức và sẽ phát hành một bộ công cụ; nghiên cứu ở mức phát triển về mức tăng do dữ liệu huấn luyện là kết quả thứ yếu. Phụ lục giữ hồ sơ đầy đủ của các phép thử huấn luyện và giải mã chạy với hệ thống có kiểm soát của Mục 4. Mỗi phán quyết là phán quyết mà bản đăng ký hoặc quy tắc của nó tạo ra. Phụ lục viết rằng không kết quả nào ở S1–S7 là đóng góp của bài hay làm đổi khung của bài, và chúng được báo cáo "so that no test is left out". S8 khác về bản chất: đó là hồ sơ chạy và bảng điểm của lần chạy hệ thống bên ngoài. S9–S15 chứa các đoạn chuyển từ thân bài sang. Đoạn sơ đồ ở đầu phụ lục tóm tắt các phán quyết: giả thuyết bất biến đường biên của thang giám sát không được thoả; trong ba dự đoán đã đăng ký cho bảng xếp hạng bốn mô hình, hai thất bại và một không kết luận được; trong bốn biện pháp có cổng phát triển, đồng thuận hạt giống qua cổng phát triển, phép chọn dựa trên bộ kiểm chứng không được mang tiếp, DPO khớp số lượng thất bại, và quy tắc về kích thước tập huấn luyện đề nghị thêm dữ liệu ảnh bên ngoài nhưng dữ liệu ấy không được thêm; mô hình nền thứ hai dừng ở bước kiểm zero-shot; xếp lại theo đồng thuận đối tượng, học tăng cường chỉ theo CIDEr và phép chọn theo phiếu bầu toàn cục thất bại theo quy tắc đã đăng ký, lập kế hoạch đối tượng không được chạy, và nội suy trọng số không cho mức tăng; phép thử cuối cùng có phán quyết "FAIL".

### B.10.1 S1: nhãn đăng ký và các hệ thống bổ sung

Mọi phép thử trong phụ lục mang một trong bốn nhãn, tính từ thời điểm commit, đẩy lên kho từ xa, tệp và đầu ra. REGISTERED: dự đoán hoặc cổng được commit vào hệ quản lý phiên bản trước đầu ra đầu tiên mà nó bao phủ. LOCALLY_FROZEN: một tệp có cùng SHA-256 đã nằm trên đĩa trước đầu ra đầu tiên nhưng được commit sau đầu ra ấy; các phép thử này được coi là thăm dò và thời điểm được nêu. POST_HOC: bản đăng ký được viết vào lúc hoặc sau đầu ra đầu tiên, chẳng hạn vì nó trích chính kết quả của phép thử. EXPLORATORY: không bản đăng ký nào bao phủ phân tích. Thời điểm của hệ thống tệp là bằng chứng hỗ trợ, không phải chứng minh. Hai phép thử REGISTERED được commit trước đầu ra đầu tiên nhưng chỉ được đẩy lên kho từ xa sau đó. "KILL" nghĩa là một điều kiện dừng đã đăng ký kích hoạt.

Ngoài các hệ thống của Mục 4.1, thang giám sát dùng thêm các đích huấn luyện sau, đều với mặt nạ cũ: P1-4ep (như P1, bốn epoch, đối chứng về tính toán); cons (tham chiếu đồng thuận nhất, tức nêu nhiều đối tượng mà một tham chiếu khác cũng nêu nhất, lời nhắc ngắn); multiref (cả năm tham chiếu thành các hàng ngắn riêng); unf2 (hai tham chiếu được hợp nhất thành hai hàng ngắn riêng, đối chứng cho việc nối); và rnd2 (như fuse2 nhưng tham chiếu thứ hai được rút ngẫu nhiên, đối chứng cho phép chọn tham lam).

**Bảng B.16.** Số ảnh huấn luyện KTVIC của từng nhóm hệ thống (rút gọn từ Table S1.1, Phụ lục S1 của bài; số trong ngoặc là số hàng huấn luyện khi khác số ảnh).

| Nhóm hệ thống | Ảnh huấn luyện (số hàng) | Có thấy dev300 |
|---|---|---|
| P1 hạt giống 42 (P1 của bản FAIR) | không xác lập: 3,700 theo văn bản FAIR, 3,769 theo mã được commit cùng điểm số | có, nếu là 3,769 |
| P1 hạt giống 43, 44; P1-R hạt giống 42–44; bản lặp P1 với cờ mặt nạ không tác dụng; P1-4ep; cons | 3,769 | có |
| fuse2 hạt giống 42–44; rnd2 | 3,769 (7,538) | có |
| unf2 | 3,769 (6,472) | có |
| multiref; MR5 | 3,769 (18,845) | có |
| E5 RFT | 3,769 (8,996: 7,538 hàng của fuse2 cộng 1,458 hàng lấy mẫu từ 1,500 ảnh huấn luyện) | có |
| E5 DPO | 1,327 cặp ưu tiên từ cùng 1,500 ảnh | có |
| P1-dev hạt giống 42–44 (các thành viên của phép thử cuối cùng); trung bình trọng số của ba hạt giống | 3,469 | không |
| Học tăng cường chỉ theo CIDEr | 3,469, cộng học tăng cường trên 1,000 ảnh đầu của 3,469 | không |
| DPO và RFT khớp số lượng | dữ liệu ưu tiên từ 1,000 trong 3,469 ảnh (DPO 1,966 cặp; RFT 334 hàng) | không |
| Mô hình nền thứ hai | đăng ký trên 3,469; chưa bao giờ được huấn luyện | không |
| Kích thước tập huấn luyện (tiền thân một hạt giống) | 867 và 1,734 (và 3,469) | không |
| P1 trên UIT-ViIC | 2,695 ảnh huấn luyện UIT-ViIC | — |

Về P1 hạt giống 42, phụ lục giải thích rằng số ảnh huấn luyện không đọc được từ hồ sơ nào vì không nhật ký huấn luyện, báo cáo dựng dữ liệu, số bước hay adapter nào của lần chạy ấy còn lại, và hai nguồn còn tồn tại thì mâu thuẫn nhau (văn bản FAIR chỉ tới 3,700; mã dựng dữ liệu không có bộ lọc ảnh chỉ tới 3,769). Về các quy tắc chỉnh trên dev300 (trọng số và hệ số nhân của tiên nghiệm kNN, bộ hiệu chỉnh số lượng của PLAN-F1, nhiệt độ lấy mẫu và hằng số của UPE-MBR), chúng được khớp trên đầu ra của P1-dev hạt giống 42, hệ chưa từng thấy dev300, rồi áp dụng nguyên vẹn cho các kho mẫu kiểm tra của P1-R, hệ có huấn luyện trên dev300. Phụ lục viết rằng không quy tắc nào được khớp trên đầu ra dev300 của một hệ thống đã huấn luyện trên dev300 xét theo mã ảnh; ngoại lệ là tập dò phát triển của tiên nghiệm kNN, có 42 trong 497 ảnh thuộc dev300. Trên tập kiểm tra, mỗi quy tắc được chỉnh cho hệ 3,469 ảnh và áp dụng cho hệ 3,769 ảnh; ảnh hưởng của việc chuyển này không được đo và bài không khẳng định chiều của nó.

### B.10.2 S2: thang giám sát (supervision ladder)

Thang giám sát hỏi liệu việc đổi đích huấn luyện, khi giữ nguyên mô hình nền, công thức và cách giải mã, có đưa một hệ thống ra khỏi đường biên độ chính xác–số lượng của P1 hay chỉ dịch chuyển dọc theo nó. Các dự đoán được đóng băng và commit trước khi có bất kỳ đầu ra nào của thang. Đường biên được neo trên P1 qua ba hạt giống: số lớp được nêu trung bình trên mỗi chú thích M₁ = 1.7826 (giá trị đã đăng ký; phép tính lại dưới v2 cho Bảng 5.1 cho 1.7825), độ chính xác 78.5188, độ phủ 41.8507 và số mũ độ chính xác–số lượng b = 0.7468. Phần dư so với đường biên của một lần chạy là độ chính xác quan sát trừ độ chính xác mà đường biên dự đoán ở số lượng của nó; phụ lục không in phương trình của đường biên và ghi rằng đường biên khớp số lượng là phương pháp của bài song hành, ở đây chỉ dùng như công cụ. Các công thức đích làm đổi số đối tượng trên mỗi đích: đích của P1 mang 1.618 đối tượng mỗi hàng và của cons mang 2.033; các ngưỡng hỗ trợ tham chiếu tương ứng là 0.505 và 0.352. Hai mô hình được đối chiếu: dưới *L*, số lượng của mô hình tinh chỉnh đi theo độ dài đích và độ chính xác đi theo một đường biên của bộ học, nên đổi đích chỉ dịch chuyển dọc đường biên và phần dư bằng không; dưới *T*, một bộ học lý tưởng đặt ngưỡng trên mức hỗ trợ tham chiếu của từng đối tượng. Giả thuyết H0 đã đăng ký (bất biến đường biên) là một phép hội: phần dư điểm của mỗi lần chạy phải nằm trong ±1.0, và trung bình phần dư trên mọi lần chạy đã về phải có khoảng tin cậy 95% chứa 0 với ước lượng điểm trong [−0.8, +0.8]. Bản đăng ký tự ghi rằng khoảng tin cậy phần dư của một lần chạy khoảng ±2 điểm ở 558 ảnh.

**Bảng B.17.** Các lần chạy của thang giám sát trên tập kiểm tra KTVIC, bộ so khớp v2 (Table S2, Phụ lục S2.2 của bài). Khoảng trong ngoặc vuông ở cột M và P là khoảng [thấp, cao] đã đăng ký mà giá trị quan sát nằm ngoài; "trong" nghĩa là nằm trong cả ba khoảng đã đăng ký.

| Lần chạy | M | P | R | Trong? | Phần dư P so với đường biên [KTC 95%] |
|---|---|---|---|---|---|
| 54 P1-4ep (ngắn) | 1.7258 | 77.5701 | 39.772 | có | −1.5946 [−3.4578, 0.2019] |
| 55 cons (ngắn) | 2.0735 | 77.0095 [72.8, 76.7] | 47.5311 | không (P ngoài) | 1.4397 [−0.0688, 2.8764] |
| fuse2 hạt giống 43 (chi tiết) | 3.2545 [3.054, 3.254] | 66.9604 | 62.4452 | không (M ngoài) | −0.4574 |
| fuse2 hạt giống 44 (chi tiết) | 3.2258 | 66.7222 | 60.9353 | có | −0.8467 |
| fuse2 hạt giống 43 (ngắn) | 2.1093 | 75.446 | 47.5978 | có | 0.2034 |
| fuse2 hạt giống 44 (ngắn) | 2.0627 | 75.6733 | 46.7868 | có | 0.0039 |
| 56 multiref (ngắn; chạy lại) | 1.833 | 78.006 | 42.767 | có | +0.04 [−1.85, +2.01] |
| 58 unf2 (ngắn; chạy lại) | 2.056 [2.096, 2.32] | 76.199 | 46.954 | không (M ngoài, phía dưới) | +0.46 [−1.18, +2.20] |
| 57 rnd2 (chi tiết; chạy lại) | 2.545 | 72.465 | 53.744 | có | +0.71 [−1.02, +2.30] |
| 57 rnd2 (ngắn; chạy lại) | 2.004 [2.031, 2.151] | 76.208 | 45.677 | không (M ngoài, phía dưới) | −0.02 [−1.95, +1.86] |

Phán quyết được phụ lục ghi là: tiêu chí gộp được thoả (trung bình phần dư trên 10 lần chạy là −0.007, tính từ các ước lượng điểm từng lần chạy đã in; khoảng tin cậy 95% là [−0.90, +0.92], chứa 0, với ước lượng điểm trong ±0.8), nhưng tiêu chí từng lần chạy thì không (8 trong 10 lần chạy trong ±1.0; P1-4ep −1.59, cons +1.44), "so H0 as registered is not met". Sáu trong mười lần chạy nằm trong cả ba khoảng đã đăng ký. Trước các lần chạy lại, sáu lần chạy đã về khi ấy cho −0.2086 điểm phần trăm [−1.1403, 0.7604].

Phụ lục công bố các bổ sung về sau. Một phụ chương diễn giải thêm hai kiểm định tương đương một phía (TOST), với biên ±1.0 cho từng lần chạy và ±0.8 cho trung bình gộp; vì nó được commit sau khi đã có đầu ra của thang và tự trích một phần dư gộp tạm thời, các kiểm định của nó mang nhãn hậu nghiệm. Với sáu lần chạy, khoảng tin cậy 90% là [−0.9877, 0.5659], không nằm trong ±0.8, nên TOST thất bại và tương đương ở ±0.8 không được chứng tỏ. Cùng khoảng ấy nằm trong ±1.0 (p = 0.048) và ±2.0 (p = 0.001), nhưng không tệp nào định hai biên này cho trung bình gộp nên hai kết quả ấy là EXPLORATORY và chỉ mang tính mô tả; hiệu ứng tối thiểu phát hiện được với lực 80% là 1.362. Về các lần chạy cụ thể: lần chạy 55 có độ chính xác 77.0095, trên khoảng đã đăng ký, với phần dư có khoảng chứa không và kiểm định tương đương riêng cũng thất bại (p = 0.7323 ở biên ±1.0 và p = 0.2478 ở biên mô tả ±2.0), CIDEr-D của nó là 147.09; fuse2 hạt giống 43 (chi tiết) trượt sát với số lượng 3.2545 vượt cận trên 3.254; các lần chạy 56–58 bị mất do hỏng máy và được chạy lại trên GPU thuê, các bản chạy lại không so được với bản gốc đã mất và tệp dự đoán của chúng chưa được kiểm chứng lại độc lập; hai bản chạy lại nêu ít đối tượng hơn mức đã đăng ký (2.056 và 2.004 dưới các cận dưới 2.096 và 2.031). Về đối chiếu *L* với *T*: số lượng 1.7258 của P1-4ep nằm trên sàn 1.63 của *L* và xa mức 1.24 mà *T* dự đoán; tỉ số số lượng của cons so với neo P1 là 1.1632, nằm trong khoảng đã đăng ký [1.153, 1.277] của *L*, so với 1.467 của *T*; so với fuse2, cons khác −0.0179 về số lượng và 1.2597 điểm phần trăm về độ chính xác, trong các biên đã đăng ký. Cả hai phép phân biệt đã đăng ký nghiêng về *L*, nhưng theo phụ chương điều này chỉ có nghĩa là số lượng đi theo độ dài đích. Phụ lục kết luận rằng không lần chạy nào cho thấy mức tăng độ chính xác ở số lượng bằng nhau với khoảng tin cậy loại trừ không, và cách đọc thực tế là "a rule, not a law": một mức tăng điểm đối tượng thô do tuyển chọn đích phải được kiểm ở số lượng khớp trước khi được gọi là mức tăng độ chính xác. Với các hệ thống của thân bài, phần dư trên F1 (trung bình ba hạt giống, P1 làm neo) là 0.81 cho P1-R, 0.64 cho fuse2 (ngắn) và −0.42 cho fuse2 (chi tiết).

### B.10.3 S3: mô hình nền thứ hai và phương án dự phòng 3B

Để kiểm xem đường biên và các phát hiện kiểm định có phụ thuộc mô hình nền không, nhóm đăng ký mô hình nền thứ hai Qwen3-VL-8B-Instruct [@bai2025qwen3vl] trước khi có bất kỳ đầu ra KTVIC nào của nó, với giao thức ba bước có cổng. Bước 1 là bước kiểm ngôn ngữ zero-shot trên dev300 (khoảng 0.2 giờ GPU): chú thích ngắn phải có ít nhất 0.98 là tiếng Việt, với tỉ lệ ký tự CJK tối đa 0.02 (0.05 cho chú thích chi tiết). Bước 2 huấn luyện một hạt giống trên 3,469 ảnh huấn luyện ngoài dev300 (khoảng 1.8 giờ GPU); các hạt giống 43 và 44 chỉ chạy nếu đầu ra dev300 có ít nhất 0.99 là tiếng Việt với tỉ lệ CJK tối đa 0.01. Bước 3 là dự đoán đường biên: điểm cuối chính là sự tương đương của phần dư so với đường biên với không trong ±2.0 điểm; ngân sách đủ ba hạt giống là 7.0–8.0 giờ GPU. Kết quả, được phụ lục gọi là kết quả biên đã đăng ký trước: dừng ở Bước 1 như đã đăng ký. Chú thích ngắn có tỉ lệ CJK 0.03 (9 trong 300), trên mức tối đa 0.02; chú thích chi tiết có 5.11 lớp được nêu mỗi chú thích, trên mức tối đa đã đăng ký 3.5; tỉ lệ tiếng Việt là 1.0 ở cả hai chế độ. Bước 2 không được chạy. Phương án dự phòng là Qwen2.5-VL-3B-Instruct; các lần chạy 3B (P1 và fuse2, hạt giống 42) đã có đầu ra nhưng chưa được kiểm chứng và không được báo cáo. Một ghi chú hiệu chỉnh hậu nghiệm thừa nhận mức tối đa 3.5 được đặt mà không kiểm với chính mô hình nền của bài: chú thích chi tiết zero-shot của Qwen2.5-VL-7B trên tập kiểm tra KTVIC có 6.54 lớp được nêu mỗi chú thích, nên bước kiểm chặt hơn mức mà mô hình nền chính tự nó qua được; việc dừng được báo cáo như đã đăng ký và không được diễn giải lại.

### B.10.4 S4: bảng xếp hạng theo phiếu giao thức của các VLM công khai

Một bảng xếp hạng đã đăng ký chấm các VLM công khai ở chế độ zero-shot dưới giao thức của bài: trên toàn bộ tập kiểm tra KTVIC, với các ảnh không có bản sao trong OpenViIC làm tập độ nhạy, và trên tập kiểm tra UIT-ViIC. Bốn mô hình được chấm: Qwen2.5-VL-3B và -7B [@bai2025qwen25vl], Qwen3-VL-8B [@bai2025qwen3vl] và InternVL3-8B [@zhu2025internvl3]; 16 lần chạy, không lần nào bị loại.

**Bảng B.18.** Ba dự đoán đã đăng ký của bảng xếp hạng bốn mô hình (Phụ lục S4 của bài).

| Dự đoán | Ước lượng | Phán quyết đã đăng ký |
|---|---|---|
| 1. Việc sửa dấu câu làm đổi thứ hạng CIDEr-D zero-shot trên tập kiểm tra KTVIC (lời nhắc ngắn) | tau_b 1.0 [1.0, 1.0] | "FAIL" |
| 2. Dưới bản sửa, tập kiểm tra KTVIC và tập kiểm tra UIT-ViIC xếp hạng các hệ zero-shot tương đương | tau_b 0.667 [0.333, 0.667], so với ngưỡng đã đăng ký 0.6 | "INCONCLUSIVE" |
| 3. Bản sửa nâng sự đồng thuận giữa hai bộ chuẩn | hiệu 0.0 [−0.333, 0.0] | "FAIL" |

Với dự đoán 1, bản sửa để nguyên thứ hạng; hệ quả đã đăng ký là bài chỉ báo cáo dịch chuyển điểm của bản sửa và không khẳng định rằng bản sửa xếp hạng lại các hệ thống công khai. Với dự đoán 2, hai thứ hạng khác nhau ở một cặp, Qwen2.5-VL-7B so với Qwen3-VL-8B, dù có hay không có bản sửa. Phụ lục lưu ý rằng với bốn hệ thống, một tương quan thứ hạng chỉ nhận vài giá trị và các khoảng phản ánh điều đó; bảng xếp hạng là một minh hoạ của giao thức, không phải một kết quả xếp hạng.

### B.10.5 S5: kết quả âm của các biện pháp huấn luyện và giải mã

Phụ lục viết rằng mọi biện pháp dưới đây trông như một mức tăng dưới điểm thô, và mỗi biện pháp đều trượt cổng đã đăng ký hoặc một phép so có kiểm soát số lượng.

**Bảng B.19.** Kết quả âm trên KTVIC (rút gọn từ Table S5.1, Phụ lục S5 của bài; lược các mốc thời gian và mã commit).

| Họ biện pháp | Nhãn đăng ký | Phép thử | Kết cục |
|---|---|---|---|
| Tiên nghiệm kNN văn bản trên kho mẫu | LOCALLY_FROZEN, coi là thăm dò | ΔF1 ≥ 0.5 với khoảng trên 0 so với hai đối chứng khớp số lượng, cộng cổng "panel" | tiêu chí chính không đạt; theo quy tắc của tệp: dương thứ yếu hoặc không kết luận |
| UPE-MBR, xếp lại theo đồng thuận đối tượng | REGISTERED | quy tắc dừng 2: độ chính xác "panel" bằng đối chứng COUNT (khoảng chứa 0) trên ít nhất 2 trong 3 hạt giống | "KILL" (kích hoạt trên 3 trong 3) |
| Học tăng cường chỉ theo CIDEr (CN-RLOO) | REGISTERED | đạt cần mức tăng CIDEr phát triển ≥ +3.0 với cận dưới trên 0 và mọi điều kiện bảo vệ được giữ | "KILL" (điều kiện bảo vệ về sao chép bị vi phạm), không sạch |
| P-M6b, chọn theo phiếu bầu toàn cục | REGISTERED chỉ cho lần nhìn 1; lần nhìn 2 là POST_HOC | huỷ nếu ΔF1 gộp < +0.8 hoặc khoảng chứa 0 | "KILL" (lần nhìn 1: ΔF1 dưới +0.8) |
| PLAN-F1, lập kế hoạch đối tượng | các lần chạy đã đăng ký không bao giờ được thực hiện; phần phê bình trên dev300 là POST_HOC | phép thử đã đăng ký không chạy | "NOT_RUN": không phán quyết |
| WiSE-FT, nội suy trọng số của fuse2 | REGISTERED; có sai lệch thực thi được công bố | chọn α* theo F1 trên tập thẩm định UIT-ViIC trong các α có CIDEr-D ngắn trên KTVIC ≥ 140.7; cổng vô ích cho bước tiếp | điều kiện bảo vệ không ràng buộc; α* = 0.75; ΔF1 < 0 ở cả hai α; không vô ích (bước tiếp chưa chạy); bốn mục của phụ chương không được tính |
| Tự hợp nhất k = 2 | EXPLORATORY | phần dư so với đường biên | dưới đường biên |
| E5 RFT, E5 DPO, MR5 nhiều tham chiếu, mặt nạ mất mát của P1, thẻ đối tượng | EXPLORATORY | phần dư F1 so với đường biên | không có mức tăng phần dư |

Về tiên nghiệm kNN (S5.1), tiên nghiệm chấm mỗi đối tượng ứng viên theo tần suất các chú thích của ảnh huấn luyện giống về thị giác nêu nó. Trên dev300 nó tách đối tượng đúng khỏi sai với AUROC 0.6142; trên tập kiểm tra giá trị này giảm còn 0.5806 so với tập chuẩn vàng KTVIC. Hiệu ứng nhỏ nhất đáng quan tâm là ΔF1 = 0.5. Gộp ba hạt giống, tiên nghiệm hơn đối chứng (v, g) lấy trung bình hoà +0.03 [−0.41, 0.46] và hơn đối chứng POOL-VOTE +0.31 [−0.13, 0.75] (p Holm = 0.4295); cổng "panel" cũng trượt, L = +0.10 [−0.18, 0.37]. Tiêu chí chính không đạt; quy tắc kết cục của tệp có ba lớp và xếp kết quả này vào lớp giữa. Nhãn "KILL (NEGATIVE)" mà tập lệnh đánh giá lưu không thuộc ba lớp ấy và không được dùng. Vì tệp được commit sau đầu ra, phép thử được báo cáo là thăm dò. Phụ lục cũng công bố rằng AUROC phát triển là lạc quan do 42 trong 497 ảnh của một tập dò trước đó thuộc dev300.

Về UPE-MBR (S5.2), phương pháp chọn trong các chú thích lấy mẫu của một hệ thống chú thích có đối tượng được các mẫu khác xác nhận nhiều nhất. So với giải mã tham lam nó trông như một mức tăng rõ: F1 đối tượng theo "panel" OpenViIC +1.91 [1.45, 2.35] và CIDEr-D +2.34. Quy tắc dừng 2 so UPE với một bộ xếp lại COUNT chọn mẫu có cùng số đối tượng. Trọng số của đối chứng COUNT được đặt trên chính các kho mẫu kiểm tra (0.90, 0.90 và 0.85 cho các hạt giống 42, 43 và 44, trong khi 0.65 là giá trị trên dev300); lựa chọn chỉ đọc đầu ra của hệ thống, không đọc tham chiếu kiểm tra, nhưng được làm trên tập kiểm tra, nên phụ lục gọi đối chứng là khớp trên tập kiểm tra. Các hiệu độ chính xác là +0.42 [−0.37, 1.23], +0.63 [−0.05, 1.32] và +0.45 [−0.47, 1.36]; cả ba khoảng chứa không nên quy tắc 2 kích hoạt. F1 so với cùng đối chứng cũng phẳng: +0.07 [−0.59, 0.65], +0.03 [−0.73, 0.70] và +0.17 [−0.24, 0.60]. Phụ lục tách hai phép so: UPE so với đối chứng (v, g) lấy trung bình hoà ở chính số lượng của UPE cho −0.02 [−0.356, +0.324], tức không có mức tăng ngoài điều số lượng giải thích; UPE so với bộ xếp lại COUNT, mỗi bên được lấy phần dư so với đối chứng phiếu bầu của mình, cho +0.347 [0.111, 0.599], nhưng hiệu dương này đến từ việc COUNT rơi dưới đối chứng của nó (−0.382 [−0.707, −0.07]) chứ không từ việc UPE vượt đối chứng của mình (−0.035 [−0.281, 0.221]).

Về học tăng cường chỉ theo CIDEr (S5.3), trên dev300 CIDEr-D đi từ 144.33 lên 145.90, mức tăng +1.57 [−6.26, 9.55], dưới ngưỡng đạt đã đăng ký +3.0; một điều kiện bảo vệ cũng bị vi phạm: bản sao nguyên văn của tham chiếu huấn luyện tăng lên 2.25% ở khối cuối, trên giới hạn 1.33%. Theo quy tắc đã đăng ký, mọi vi phạm điều kiện bảo vệ là một lần huỷ, nên phán quyết là "KILL", không sạch; nếu mọi điều kiện bảo vệ được giữ, mức tăng +1.57 sẽ rơi vào dải xám (+1.0 đến +3.0) của quy tắc. Một điểm cuối khớp số lượng hậu nghiệm cho +2.07 [−0.19, 4.24], so với khoảng được dự đoán [−1.5, +2.0]; dự đoán ấy là LOCALLY_FROZEN và cả hai được coi là thăm dò.

Về P-M6b (S5.4), ở lần nhìn 1 đã đăng ký, ΔF1 = +0.65 [+0.02, +1.27], p = 0.044; khoảng loại trừ không nhưng hiệu ứng dưới mức +0.8 nên phán quyết đã đăng ký là "KILL", và không hàng nào trong 12 hàng đã đăng ký của lần nhìn 1 đạt. Lần nhìn 2, hậu nghiệm, với bootstrap gom cụm theo ảnh cho ΔF1 = +0.65 [−0.02, 1.34]; phụ lục viết rằng một lần nhìn thứ hai hậu nghiệm không thể cứu một lần huỷ đã đăng ký. Phụ lục còn công bố rằng một bản chụp tập lệnh của lần nhìn 1 đã in dòng báo mọi cổng đạt do một lỗi lọc, trong khi mọi hàng của bảng cho thấy thất bại; dòng ấy đã được rút lại. Về PLAN-F1 (S5.5), phần phê bình hậu nghiệm trên dev300 cho thấy kế hoạch nâng số lớp được nêu mỗi chú thích từ 1.763 lên 2.627 với phần dư so với đường biên −2.49, và so với đối chứng phiếu bầu kho mẫu khớp số lượng thì hiệu F1 là −0.95 [−2.09, 0.18].

**Bảng B.20.** Cổng WiSE-FT (Table S5.2, Phụ lục S5.6 của bài). CIDEr-D ngắn trên tập kiểm tra KTVIC là điều kiện bảo vệ đã đăng ký (≥ 140.7), không phải ước lượng trên dữ liệu để riêng. Tập thẩm định UIT-ViIC (924 ảnh COCO) được chấm so với nhãn thực thể COCO, riêng và hợp với tham chiếu.

| Hệ thống | CIDEr-D ngắn trên tập kiểm tra KTVIC (điều kiện bảo vệ) | F1, nhãn thực thể | F1, nhãn thực thể + tham chiếu | ΔF1 so với fuse2, nhãn thực thể [KTC 95%] | ΔF1 so với fuse2, nhãn thực thể + tham chiếu [KTC 95%] |
|---|---|---|---|---|---|
| fuse2 (α = 1) | 143.90 | 59.20 | 59.13 | — | — |
| α = 0.75 (được chọn) | 140.14 (không đạt) | 57.71 | 57.65 | −1.49 [−2.58, −0.47] | −1.49 [−2.58, −0.47] |
| α = 0.5 | 116.48 (không đạt) | 54.95 | 54.89 | −4.25 [−5.59, −2.98] | −4.24 [−5.57, −2.98] |

WiSE-FT [@wortsman2022robust] đưa trọng số của fuse2 lùi một phần về phía mô hình nền zero-shot; α = 1 là chính fuse2. Không α nào qua điều kiện bảo vệ nên quy tắc quay về cả hai ứng viên và α* = 0.75 được chọn chỉ theo F1 trên tập thẩm định UIT-ViIC; vì thế không siêu tham số nào được chọn trên tập kiểm tra KTVIC. Nội suy về phía mô hình nền hạ F1 theo nhãn thực thể ở cả hai điểm, với khoảng loại trừ không. Cổng vô ích trả về "not futile" nên bước huấn luyện tiếp theo vẫn đủ điều kiện theo bản đăng ký riêng; nó chưa được chạy. Bốn mục báo cáo đã đăng ký trong phụ chương không được tính và không được báo cáo.

**Bảng B.21.** Phần dư F1 so với đường biên đã đóng băng (điểm phần trăm) trên tập kiểm tra KTVIC, hạt giống 42 trừ khi nói khác (Phụ lục S5.7 của bài).

| Biện pháp | Phần dư F1 [KTC 95%] |
|---|---|
| Tự hợp nhất k = 2 trên fuse2 | −4.21 [−6.11, −2.27] |
| Tự hợp nhất k = 2 trên P1 (hạt giống 43) | −3.84 [−5.89, −1.96] |
| E5 RFT tương đối theo nhóm (phần thưởng CIDEr + độ chính xác đối tượng) | −0.15 [−2.55, 2.06] |
| E5 DPO ngoại tuyến [@rafailov2023direct] | −1.97 [−4.33, 0.18] |
| MR5 (cả năm tham chiếu, chỉ-trả-lời) | 0.25 [−2.10, 2.54] |
| Bản lặp P1 có cờ mặt nạ không tác dụng | 0.25 [−2.17, 2.59] |
| Hợp nhất có điều kiện theo thẻ của bộ phát hiện (đích fuse2) | 1.55 [−0.64, 3.78] |

Phụ lục nhận xét chung (S5.8): mỗi biện pháp làm tăng số đối tượng được nêu hoặc đổi phong cách chú thích, và mỗi mức tăng thô biến mất khi phép so được làm ở số lượng bằng nhau hoặc so với một "panel" độc lập; trên KTVIC, F1 đối tượng thô và CIDEr không phân biệt được một hệ thống tốt hơn với một hệ thống nói nhiều hơn hoặc đặt dấu câu khác đi.

### B.10.6 S6 và S7: các biện pháp có cổng phát triển, phép thử cuối cùng và các sai lệch

Bốn biện pháp được đăng ký trước khi có đầu ra và chỉ được xét cổng trên dev300; các cổng quyết định đi tiếp hay dừng, không cổng nào là khẳng định trên tập kiểm tra. DPO khớp số lượng và tinh chỉnh bằng lấy mẫu loại bỏ: "FAIL", mọi nhánh đều gặp một quy tắc dừng. Bộ kiểm chứng VLM độc lập (InternVL3-8B, chỉ làm bộ chấm, là tín hiệu do mô hình sinh ra và được gắn cờ): cổng của bộ kiểm chứng đạt (AUROC trong ô 0.634 ≥ 0.58; AUROC không ảnh 0.485 ≤ 0.60), nhưng nhánh chọn không được mang tiếp vì nó cải thiện F1 đối tượng +1.51 và CHAIR_i −1.89 (×100) so với đối chứng khớp số lượng nhưng tốn 2.62 CIDEr-D, vượt sàn đã đăng ký −2.0. Kích thước tập huấn luyện (tiền thân một hạt giống của nghiên cứu ở Mục 5.3): CIDEr-D tăng 9.40 cho mỗi lần nhân đôi (cận dưới khoảng tin cậy 95% là 4.87; một hạt giống cho mỗi kích thước nên khoảng chỉ bao phủ việc lấy mẫu ảnh), cao hơn hẳn dự đoán đóng băng từ +1 đến +4; chỉ điểm kích thước đầy đủ được huấn luyện trên một ảnh trùng từng byte với một ảnh dev300, nên điểm ấy, và qua nó là hệ số dốc, có thể bị lệch lên bởi một ảnh phát triển, và hệ số dốc không được tính lại khi bỏ ảnh đó; kết cục của quy tắc là khuyến nghị thêm dữ liệu ảnh bên ngoài, nhưng dữ liệu ấy không được thêm vì phân tích đăng ký trước dự kiến huấn luyện chung với dữ liệu tiếng Việt khác chỉ làm KTVIC thay đổi khoảng ±1. Đồng thuận hạt giống: biến thể MBR-3 qua cổng phát triển (+2.55 [+0.004, +5.24] CIDEr-D so với trung bình thành viên; ΔCHAIR_i −0.19), rồi lần đánh giá duy nhất trên tập kiểm tra cho D_MBR = −0.391 [−2.437, +1.666], phán quyết đã đăng ký "FAIL"; K2 không kích hoạt (ΔCHAIR_i = +0.103) và K3 không kích hoạt (ΔF1 = −0.18 [−0.74, +0.39]). Phép kiểm dự đoán, vốn không phải phán quyết, cho thấy ΔCIDEr-D (−0.39) nằm ngoài khoảng dự đoán [1.0, 3.0] và ΔBLEU-4 (+0.234) nằm ngoài [0.5, 1.0], còn ΔF1 và ΔCHAIR_i nằm trong khoảng của chúng. Về hàng hậu nghiệm trên P1-R (POST_HOC, không phán quyết): so với trung bình thành viên, BLEU-4 thay đổi +0.73, CHAIR_i −1.04 điểm và F1 đối tượng +0.63 [+0.05, +1.19]; phép chọn lấy hạt giống 42 trên 400 ảnh, hạt giống 43 trên 127 ảnh và hạt giống 44 trên 31 ảnh, và ba thành viên viết cùng một chú thích cho 31.9% số ảnh; hàng này không đổi phán quyết "FAIL", và việc đóng tập kiểm tra có hiệu lực trở lại.

**Bảng B.22.** Các sai lệch đã công bố của các phép thử REGISTERED (rút gọn từ Table S7, Phụ lục S7 của bài).

| Phép thử | Sai lệch |
|---|---|
| Thang giám sát | các lần chạy 56–58 bị mất do hỏng máy và được chạy lại; phép kiểm đã đăng ký chấm chúng một lần; phụ chương TOST là POST_HOC |
| Mô hình nền thứ hai | dừng ở bước kiểm của Bước 1 như đã đăng ký; ngưỡng chế độ chi tiết chưa được kiểm với mô hình nền của bài |
| UPE-MBR; cổng học tăng cường | commit trước đầu ra đầu tiên nhưng chỉ đẩy lên kho từ xa sau đó |
| P-M6b | lần nhìn thứ hai và các khoảng gom cụm theo ảnh là POST_HOC |
| Cổng WiSE-FT | cổng đã đăng ký chạy sau tác vụ, ngoài máy GPU, do một lỗi môi trường lúc nạp; mã không đổi và đầu vào được kiểm mã băm; điều kiện bảo vệ trên tập kiểm tra KTVIC không ràng buộc |
| Kích thước tập huấn luyện (cổng phát triển) | quy tắc khuyến nghị dữ liệu ảnh bên ngoài; dữ liệu ấy không được thêm |
| Phép thử cuối cùng | sau kết quả, việc đóng tập kiểm tra được gỡ cho một hàng POST_HOC; hàng chạy một lần và được một lần chạy lại độc lập tái tạo đúng từng byte; không có phán quyết, và phán quyết "FAIL" không đổi |
| DPO khớp số lượng (cổng phát triển) | bản đăng ký của nó đã được sửa đổi |

### B.10.7 S8: bộ công cụ trên các hệ thống bên ngoài

Danh sách ứng viên gộp một kiểm kê 22 sản phẩm chú thích tiếng Việt với một lần tìm kho mã có ghi ngày, và được cố định trước khi tải bất kỳ tệp nào. Một hệ thống đủ điều kiện nếu thoả bốn điều kiện: báo cáo trên một trong ba tập kiểm tra chính thức; là của bên thứ ba và mới; công bố đầu ra kiểm tra theo từng ảnh, hoặc phát hành một checkpoint nạp được theo quy tắc đã đăng ký; và không phải là một mô hình tổng quát zero-shot. Hai hệ cơ sở KTVIC đã công bố chỉ làm phép kiểm bộ chấm: bộ công cụ phải tái tạo đúng các giá trị trước đó của chúng trước khi tính bất kỳ điểm bên ngoài nào, và chúng không được đếm. Được chọn là mười tệp đầu ra đã công bố, bao phủ chín hệ thống từ bốn chủ sở hữu, và ba checkpoint từ ba chủ sở hữu khác. Cổng cấu trúc ánh xạ mỗi tệp đầu ra sang mã ảnh kiểm tra chính thức theo mã và tên tệp, không bao giờ theo vị trí; một tệp chỉ đạt nếu phân tích được, tập mã của nó đúng bằng tập kiểm tra chính thức, và dưới một nửa số dự đoán sao chép một tham chiếu. Cả mười tệp trượt và bị loại mà không sửa chữa: ba tệp vì không phân tích được, bảy tệp vì mã không xác định. Phụ lục công bố một sai lệch: một lần đọc chỉ về cấu trúc, hậu nghiệm, đã mở các tệp đã tải trước khi có điểm số, trái với quy tắc giám sát đã đăng ký; phụ lục lập luận đó không phải một lần nhìn vì không tệp nào trong số ấy có thể được chấm. Lần đọc ấy cũng phát hiện một khiếm khuyết tiềm ẩn của bộ phân tích, không ảnh hưởng đến tệp nào.

Ba checkpoint được tải ở các bản sửa đổi được ghim với mọi mã băm tệp được kiểm, và mỗi cái qua một bước thử khói trước khi ảnh kiểm tra nào được giải mã. Thiết lập giải mã là tìm kiếm chùm 4 nhánh từ cấu hình của chính checkpoint cho K1, giải mã tham lam với lời nhắc của thẻ mô hình cho K5, và ví dụ chùm 5 nhánh của thẻ mô hình cho K6. Lần chạy dừng hai lần; mỗi lần dừng dẫn tới một sửa đổi có ghi ngày được thông qua trước khi chạy lại, và không sửa đổi nào làm đổi công thức, cột, tập chia, danh sách, mức trần, quy tắc một lần nhìn hay ngưỡng thẩm định. Lần dừng thứ nhất xảy ra vì K5 sinh chuỗi rỗng trên ảnh thử khói màu xám phẳng; lần dừng thứ hai vì thư viện ảnh từ chối một ảnh bị cắt cụt khi giải mã K6. Một phép kiểm trên CPU đối với toàn bộ 2,001 ảnh được liệt kê thấy đúng ba ảnh hỏng khi giải mã nghiêm ngặt, với byte khớp mã băm được ghim, tức sự cắt cụt nằm trong bản phát hành; quy tắc được thông qua là giải mã nghiêm ngặt trước rồi thử lại một lần ở chế độ cho phép ảnh cắt cụt chỉ cho lần gọi ấy, và không ảnh nào bị loại. Việc chấm chạy một lần sau khi khối GPU kết thúc. K1 và K6 chỉ được báo cáo ở dạng tổng hợp vì giấy phép của chúng là không có và "other" và chưa xin được phép; không dự đoán nào của ba hệ thống được phát hành; điểm trên thẻ mô hình thu được dưới giao thức không rõ và không được so sánh.

**Bảng B.23.** Bộ công cụ trên các hệ thống bên ngoài (rút gọn từ Table S8.1, Phụ lục S8 của bài; mô tả, không phán quyết, không xếp hạng, không so với các con số đã đăng ký của nhóm). P0: RDRSegmenter, dấu câu như được viết; P0s: P0 với các token dấu câu cuối của ứng viên được gỡ; PTB: P0 với danh sách dấu câu PTB được xoá khỏi ứng viên và tham chiếu; SYL: âm tiết ở khoảng trắng; PYVI: tách từ bằng pyvi. Mọi điểm ×100; khoảng là bootstrap phân vị 95% theo ảnh (B = 2,000).

| Mã | Hệ thống và tập kiểm tra | n | Đầu ra rỗng | Tỉ lệ kết thúc bằng dấu câu | CIDEr-D P0 [KTC 95%] | BLEU-4 P0 | ROUGE-L P0 | CIDEr-D P0s | CIDEr-D PTB [KTC 95%] | CIDEr-D SYL | CIDEr-D PYVI |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | Swin-BART; tập kiểm tra KTVIC | 558 | 0 | 0.0000 | 106.85 [99.02, 115.12] | 35.29 | 56.49 | 106.85 | 106.85 [99.02, 115.12] | 119.77 | 107.35 |
| K5 | SmolVLM2-500M-vi-stage1; tập kiểm tra UIT-ViIC | 231 | 57 | 0.2381 | 2.75 [2.03, 3.56] | 0.00 | 11.80 | 2.62 | 3.17 [2.33, 4.13] | 1.64 | 2.75 |
| K6 | Vie-BLIP; tập kiểm tra UIT-OpenViIC | 2,001 | 0 | 0.0000 | 41.71 [40.10, 43.44] | 26.69 | 43.47 | 41.71 | 41.71 [40.10, 43.44] | 47.39 | 41.56 |

Như đã đăng ký, phụ lục chỉ mô tả việc các cột của mỗi hệ thống khác nhau thế nào. Đầu ra của K1 và K6 không chứa dấu câu hay gạch dưới nên P0, P0s và PTB trùng nhau cho mỗi hệ thống. Với K5, 23.81% chú thích kết thúc bằng một token dấu câu và cách xoá kiểu PTB loại 198 token; 57 trong 231 đầu ra của nó là chuỗi rỗng, và BLEU-4, ROUGE-L dưới PTB của nó là 0.00 và 10.09. Phụ lục nêu bốn giới hạn: phạm vi (ba hệ thống, mỗi bộ dữ liệu một hệ thống, đều từ checkpoint); ai giải mã (nhóm tác giả, trong môi trường của mình, nên không nói được các lần giải mã có tái tạo đầu ra của tác giả hay không); chạy bởi chính nhóm (không phải bởi một nhóm bên ngoài); và cách báo cáo (hai hệ thống chỉ ở dạng tổng hợp; dữ liệu huấn luyện của K1 chỉ biết qua tên; lần chạy không đỡ cho khẳng định nào về chất lượng).

### B.10.8 S9–S15: các đoạn chuyển từ thân bài

S9 (tham chiếu so với nhãn thực thể trên UIT-ViIC) đã được trình bày ở B.6.2; S10 (độ nhạy của v3 và danh từ chỉ vai, trẻ em) ở B.4.5; S11 (điểm hệ thống trên XM3600 và số token bị xoá) ở B.4.3 và Bảng B.6; S15 (phân phối không giữ tỉ lệ theo vị trí) ở B.4.2 và Bảng B.3.

**Bảng B.24.** Điều bài này và bài song hành khẳng định, và dữ liệu mỗi bài dùng (rút gọn từ Table S12.1, Phụ lục S12 của bài).

| | Bài song hành (đang soạn) | Bài này |
|---|---|---|
| Câu hỏi | Khi nào một điểm ảo giác ở mức đối tượng đỡ cho phép so sánh giữa hai hệ thống? | Một điểm CIDEr hay điểm đối tượng trên KTVIC đo điều gì? |
| Khẳng định chính | một khẳng định xác nhận về hệ số dốc của F1 theo logarit số đối tượng, có thứ tự theo độ đầy đủ của tập chuẩn vàng (đăng ký trên XM3600); các phần thứ yếu đã đăng ký và phần thăm dò | kiểm định KTVIC: tham chiếu một người viết, quy ước dấu câu, độ nhạy tách từ, các phiên bản bộ so khớp; phiếu giao thức và bộ công cụ đánh giá |
| KTVIC | không có số chính | bộ dữ liệu chính |
| XM3600 (tiếng Việt) | phép thử dấu của tính dài dòng đã đăng ký, chấm trên sáu hệ thống gồm P1 và fuse2 của bài này | tỉ lệ tham chiếu kết thúc bằng dấu chấm; CIDEr-D của mô hình nền zero-shot và cùng các đầu ra P1, fuse2 dưới P0 và với xoá kiểu PTB; hiệu ứng thêm dấu chấm |
| UIT-ViIC | hệ số dốc của F1 đối tượng theo số đối tượng dưới ba tập chuẩn vàng (thăm dò); thống kê hoán đổi được | CIDEr-D chuyển miền; hiệu ứng hợp nhất trong miền so với nhãn thực thể COCO; sự đảo do bộ so khớp vai/trẻ em; hệ số dốc chuyển từ tham chiếu sang nhãn thực thể |
| UIT-OpenViIC | thống kê hoán đổi được (chỉ số tổng hợp) | lần chạy hệ thống bên ngoài ở S8 (chỉ số tổng hợp) |
| Dữ liệu tiếng Anh | COCO, Flickr30k, các họ mô hình tiếng Anh, đánh giá của người và dữ liệu ưu tiên công khai | không có |
| Đối chứng khớp số lượng | được phát triển và kiểm chứng ở đó | dùng như công cụ, chỉ trong phụ lục |
| Thống kê hoán đổi được | được định nghĩa ở đó; báo cáo trên COCO, UIT-ViIC, Flickr30k và UIT-OpenViIC | chỉ báo cáo trên KTVIC |
| Kho lưu trữ | kho riêng | kho Zenodo riêng, chỉ chứa các thành phần của Bảng S13.2 |
| Hệ thống | hệ thống đã công bố và các mô hình zero-shot; cả đầu ra của các hệ tinh chỉnh của bài này trên XM3600 và UIT-ViIC | các bản tinh chỉnh Qwen2.5-VL-7B (P1, P1-R, fuse2) và mô hình nền zero-shot; các hệ thống được huấn luyện và sở hữu ở đây |

**Bảng B.25.** Khuyến nghị của Mục 6.4 và thành phần của bộ công cụ thực hiện từng khuyến nghị (Table S13.1, Phụ lục S13 của bài).

| Khuyến nghị | Thành phần của bộ công cụ |
|---|---|
| 1. Phiếu giao thức | bộ chấm và mẫu phiếu giao thức; mọi tệp kết quả bộ chấm ghi lại bộ tách từ, cách tách token và thang điểm |
| 2. Xoá dấu câu, hoặc cả hai con số | phép kiểm định dấu câu, tập lệnh giao thức PTB và phép kiểm định dấu chấm trên XM3600 |
| 3. Công bố bộ so khớp | mã so khớp và danh sách từ v1, v2 do tác giả xây dựng; quy tắc v3 chưa được xác nhận không nằm trong đó |
| 4. So sánh ở số lượng khớp | không có trong bộ công cụ này; các đối chứng thuộc về bài song hành |
| 5. Tập chuẩn vàng thứ hai | giao thức hai tập chuẩn vàng (nhãn thực thể COCO cho UIT-ViIC) |
| 6. Không gọi đồng thuận trong cùng người viết là "human ceiling" | phép thử hoán đổi được và tập lệnh bỏ-một-ra |

**Bảng B.26.** Các thành phần của bộ công cụ đánh giá (rút gọn từ Table S13.2, Phụ lục S13 của bài).

| Thành phần | Nội dung | Dùng ở |
|---|---|---|
| Bộ chấm và phiếu giao thức | bộ chấm với RDRSegmenter trên ứng viên và tham chiếu, BLEU-4, ROUGE-L và CIDEr-D ×100 bằng pycocoevalcap; một bản cài đặt lại từng dòng các bộ chấm và các giao thức tách của Mục 3.4; mẫu phiếu để điền | Mục 3.3, 3.4, 4.2 |
| Bộ so khớp đối tượng | mã so khớp có chuẩn hoá dấu thanh (v2) và danh sách từ v1, v2; mọi điểm đối tượng ghi phiên bản bộ so khớp; không có quy tắc v3 | Mục 3.5 |
| Tập lệnh chia dữ liệu | quy tắc hạt giống cố định của phép chia dev300 và phần huấn luyện còn lại, có kiểm danh sách tạo lại với mã MD5 đã đăng ký | Mục 3.1 |
| Tập lệnh kiểm định | tỉ lệ cặp đôi kề nhau và độ dôi Jaccard; bỏ-một-ra trong cùng người viết; đường cong gỡ và thêm dấu chấm cho một đến năm tham chiếu; giao thức PTB (hậu nghiệm); tỉ lệ dấu chấm cuối và dịch chuyển trên XM3600; phép kiểm định *cây*; các đối chứng hậu nghiệm; chấm hai tập chuẩn vàng | Mục 3.2–3.5, 5 |
| Hồ sơ | các tệp đăng ký trước; bản sao chỉ còn điểm số của các tệp kết quả được trích; bảng kê số liệu với đường dẫn lưu trữ cho mỗi hàng | mọi mục; phụ lục |

Về các phép kiểm của bộ công cụ, phụ lục viết rằng mỗi tập lệnh `kit_b` đã được chạy lại từ kho lưu trữ trên đầu vào gốc và tái tạo mọi giá trị mà bảng kê trích từ nó; ngoại lệ là hai giá trị Kendall τ của Mục 3.4 và n = 26 hệ thống của chúng, vì cần đầu ra của hai hệ cơ sở đã công bố mà bộ công cụ không chứa. Kho còn kèm một tập lệnh đã đăng ký tính một thống kê khác và không phải nguồn của các con số ở Mục 3.2. Về phép quét văn bản, mọi tệp không bị ghim bởi một bản đăng ký trước có không trùng khớp nào; ba tệp mã bị ghim bằng SHA-256 nên được giữ nguyên, chúng chứa 9 dòng cụm ví dụ do tác giả viết có chung 8–9 token liên tiếp với một tham chiếu nào đó; không trùng khớp nào từ 12 token trở lên xuất hiện trong kho. S14 nêu rằng mã công khai của các hệ cơ sở KTVIC và nhánh GRIT mà kho ấy trỏ tới đều tách token bằng bộ tách PTB trước khi chấm; mã được đọc, không được chạy. Về phần mềm, huấn luyện và giải mã dùng các phiên bản thư viện được ghim, PyTorch dựng cho CUDA 12.1; việc chấm dùng pycocoevalcap 1.2; một số lần chạy thực hiện trên GPU thuê; bài không nêu tổng lượng tính toán.

**Nhận xét rà soát.** Phụ lục ghi lại kết quả âm một cách đầy đủ và giữ nhãn đăng ký cẩn thận. Có tám việc cần làm.

Thứ nhất, câu "We report them so that no test is left out" và cụm "complete record" cần được đối chiếu lại với văn bản hiện hành. `outline_B.md` ghi rằng các nghiên cứu hai tập tham chiếu trên dữ liệu phát triển đã được rút khỏi văn bản bài, và danh sách khẳng định của cùng tệp còn nêu một phép thử rò rỉ dữ liệu (ghi là "placebo INCONCLUSIVE, headline NOT_EVALUABLE") mà phụ lục hiện hành không còn mục nào; nghiên cứu ở Mục 6.2 cũng chưa có hồ sơ trong phụ lục. Hoặc bổ sung một dòng hồ sơ cho mỗi phép thử đã chạy, hoặc thu hẹp câu về tính đầy đủ.

Thứ hai, khái niệm "panel" (tập chú thích của UIT-OpenViIC cho ảnh KTVIC) được dùng ở S4 ("the images that have no OpenViIC copy"), S5.1 ("panel gate"), S5.2 ("OpenViIC-panel object F1", "panel precision") và S5.8, nhưng không còn được định nghĩa ở đâu trong thân bài hay phụ lục. Hàng UIT-OpenViIC của Bảng S12.1 lại ghi rằng bài này chỉ dùng UIT-OpenViIC ở lần chạy S8, không khớp với S5.2. Cần một đoạn định nghĩa ngắn trong phụ lục và sửa hàng của bảng. S4 cũng nêu một tập độ nhạy nhưng không báo cáo kết quả nào trên tập ấy.

Thứ ba, nhiều chữ viết tắt và mã nội bộ không được khai triển: MBR, UPE, CN-RLOO, P-M6b, E5, MR5, RFT, DPO, SFT, CHAIR_i, đối chứng (v, g), POOL-VOTE, các số hiệu lần chạy 54–58, và "our other test set (T6)" ở S8. Thư mục bài tự ghi yêu cầu của tạp chí là không dùng chữ viết tắt chưa định nghĩa.

Thứ tư, một số câu ở S6 và S8 mô tả vai trò và thao tác nội bộ mà người đọc tạp chí không có ngữ cảnh ("The judge ruled the result genuine and final", "approved by the judge", "the principal investigator lifted that closure", "Scoring ran once, on the laptop"). Nên viết lại theo nghĩa khoa học (ai có thẩm quyền quyết định theo bản đăng ký, quyết định gì, trước hay sau khi có dữ liệu). S8 còn in tên tài khoản của các chủ kho mã và tên tệp ảnh cụ thể; cần cân nhắc có nên giữ trong bản nộp hay không.

Thứ năm, Bảng S2 in số với độ chính xác không đều (tới bốn chữ số thập phân cho sáu lần chạy đầu, hai hoặc ba cho các bản chạy lại) và thiếu khoảng tin cậy của phần dư cho bốn hàng fuse2; trung bình gộp −0.007 được tính từ các ước lượng điểm đã in vì phép kiểm không in ước lượng điểm. Nên nói rõ trong chú thích bảng. Phụ lục cũng tự nhận rằng với khoảng tin cậy từng lần chạy rộng như vậy, mệnh đề từng lần chạy của H0 có ít lực phân biệt; phán quyết vẫn phải được báo cáo như đã đăng ký.

Thứ sáu, câu của S1 về việc không con số phía phát triển nào bị thổi phồng cần được đặt cạnh các công bố về ảnh trùng phía phát triển ở Mục 5.3 và S6 (xem B.4).

Thứ bảy, trong Bảng S8.1 điểm CIDEr-D 41.71 của K6 trên UIT-OpenViIC trùng về giá trị với điểm 41.71 của P1 hạt giống 43 trên UIT-ViIC ở Mục 5.2; đây là hai hệ thống và hai bộ dữ liệu khác nhau, và một chú thích ngắn sẽ tránh nhầm lẫn.

Thứ tám, số đếm của phép quét văn bản ở S13 và danh mục tệp của Bảng S13.2 cần được cập nhật sau khi kho lưu trữ được dựng lại (xem B.4, nhận xét về Mục 3.6).

## B.11 Bảng đối chiếu khẳng định – bằng chứng

Bảng dưới đây gồm mỗi khẳng định của tóm tắt, mục mở đầu và kết luận một hàng. Cột tình trạng dùng các nhãn REGISTERED (kèm phán quyết nguyên văn), POST HOC, DESCRIPTIVE và EXPLORATORY. Cột cuối dẫn tới danh sách khoá của bảng kê số liệu đặt ngay sau bảng; khoá được viết theo dạng tên tệp và khoá như trong `number_manifest_B.tsv`.

**Bảng B.27.** Đối chiếu khẳng định với bằng chứng của bài.

| Số | Khẳng định (rút gọn) | Tình trạng | Mục của bài | Bảng trong báo cáo | Số chính | Khoá |
|---|---|---|---|---|---|---|
| 1 | Năm tham chiếu của mỗi ảnh đến từ một người viết; tỉ lệ kề nhau cao hơn giá trị không | DESCRIPTIVE (bước suy sang một người viết dựa vào tài liệu của KTVIC) | 3.2 | Bảng B.3 | 0.7102 [0.6696, 0.7518] so với 0.40; 566 cặp đôi | m1 |
| 2 | Tỉ lệ nêu theo vị trí không giải thích được sự kề nhau | POST HOC | 3.2, S15 | Bảng B.3 | trung bình không 0.4504; không lần rút nào trong 1,000 đạt giá trị quan sát | m2 |
| 3 | Không tham chiếu KTVIC nào kết thúc bằng dấu chấm | DESCRIPTIVE | 3.3 | Bảng B.5 | 2,790 tham chiếu kiểm tra; 18,845 tham chiếu huấn luyện | m3 |
| 4 | Một dấu chấm làm hệ tinh chỉnh mất 35.17 điểm ở quy trình giữ dấu câu | DESCRIPTIVE (một hạt giống, không có khoảng tin cậy) | 3.3 | Bảng B.4 | −35.17 (−23.66%); 148.66 xuống 113.49 | m4 |
| 5 | Với cách xoá kiểu PTB, dấu chấm không làm mất điểm | POST HOC | 3.3 | Bảng B.4 | 0.00; zero-shot 34.97 | m5 |
| 6 | Đầu ra zero-shot tăng khi gỡ dấu chấm cuối | DESCRIPTIVE | 3.3 | Bảng B.4 | 28.98 lên 33.30 | m6 |
| 7 | Cách tách từ làm cùng đầu ra thay đổi 15.64 điểm | DESCRIPTIVE (hiệu suy dẫn, một lần chạy) | 3.4 | Bảng B.7 | 149.79 so với 165.43; τ = 0.969 trên 26 hệ thống | m7 |
| 8 | Điểm đối tượng phụ thuộc bộ so khớp; v3 chỉ là độ nhạy | DESCRIPTIVE; v3 là phân tích độ nhạy chưa có người duyệt | 3.5, S10 | — | 30 trên 73 hệ thống; 980, 210 và 160 token; F1 55.51 lên 56.95 | m8 |
| 9 | Hệ thống có kiểm soát đạt CIDEr-D 148.23 qua ba hạt giống | DESCRIPTIVE | 5.1 | Bảng B.11 | 148.23, độ lệch chuẩn 0.38 | m9 |
| 10 | Điểm đã commit được máy thứ hai tái lập đúng từng byte | DESCRIPTIVE (cổng kỹ thuật, chỉ về việc chấm) | 4.3 | — | 148.66; hiệu lớn nhất 2.8 × 10⁻¹⁴ | m10 |
| 11 | Trung bình ba hạt giống khi bỏ 16 ảnh kiểm tra trùng hoặc gần trùng với ảnh huấn luyện | POST HOC, không phán quyết | 3.1 | — | 148.88, độ lệch chuẩn 0.36, trên 542 ảnh | m11 |
| 12 | Mỗi lần nhân đôi số ảnh huấn luyện nâng CIDEr-D trên dev300 | REGISTERED "PASS" (chỉ dữ liệu phát triển, một mô hình nền) | 5.3 | Bảng B.14 | +9.61 [7.18, 12.36] | m12 |
| 13 | Hệ số dốc khi bỏ ảnh phát triển trùng với ảnh huấn luyện | hàng độ nhạy đã đăng ký (mô tả, không phán quyết) và POST HOC | 5.3 | Bảng B.14 | +9.61 [7.17, 12.37] trên 299 ảnh; +9.77 [7.28, 12.53] trên 293 ảnh | m13 |
| 14 | Đường cong khớp trên bốn kích thước nhỏ có dự đoán được kích thước đầy đủ trong ±2.0 hay không | REGISTERED "INCONCLUSIVE" (chỉ dữ liệu phát triển) | 5.3 | — | +1.93 [−6.65, +11.05] | m14 |
| 15 | Phép thử duy nhất đã đăng ký của hệ thống cuối cùng không nâng CIDEr-D | REGISTERED "FAIL" | 5.1, S6 | Bảng B.12 | −0.39 [−2.44, +1.67]; 145.15 so với 145.55 | m15 |
| 16 | Cùng phép chọn trên đầu ra P1-R cho hiệu dương | POST HOC, không phán quyết | 5.1, S6 | Bảng B.12 | +3.14 [+1.11, +5.16] | m16 |
| 17 | Việc sửa dấu câu không xếp hạng lại bốn VLM công khai | REGISTERED "FAIL" | 1, S4 | Bảng B.18 | tau_b 1.0 [1.0, 1.0] | m17 |
| 18 | Bộ công cụ đã chạy trên 3 hệ thống bên ngoài từ 3 nguồn | DESCRIPTIVE (đăng ký trước chỉ nhằm mô tả; không phán quyết) | 3.6, S8 | Bảng B.23 | 3 hệ thống; 3 nguồn; 620 giây GPU | m18 |
| 19 | Khuôn mẫu KTVIC chuyển miền kém; hiệu ứng hợp nhất lặp lại trong miền trên UIT-ViIC | DESCRIPTIVE | 5.2 | Bảng B.13 | 41.71 và 38.52 so với 32.99; +6.67 điểm phần trăm [4.63, 8.75] | m19 |
| 20 | Điểm kiểm chứng đối tượng phân rã thấp hơn bộ phán cùng mô hình nền và CLIPScore đa ngữ trên dữ liệu phát triển | REGISTERED (chỉ dữ liệu phát triển; quy tắc dừng kích hoạt; bài không in từ phán quyết; không khẳng định tính hợp lệ) | 6.2 | Bảng B.15 | 0.068 so với 0.104 và 0.094; hiệu −0.036, cận dưới −0.061; ngưỡng 0.02 | m20 |
| 21 | Hiệu ứng dấu chấm và tách từ mỗi cái lớn hơn khoảng cách tới điểm GRIT đã công bố | DESCRIPTIVE (so giữa các giao thức không khớp; bài không in giá trị khoảng cách) | 6.1, 8 | — | 35.17 và 15.64; 148.23 và 136.0 | m21 |
| 22 | Không phép thử huấn luyện hay giải mã đã đăng ký nào tạo mức tăng được xác nhận trên tập kiểm tra | REGISTERED: "FAIL", "KILL" hoặc giả thuyết không được thoả, tuỳ phép thử | 8, S2–S7 | Bảng B.17, B.19 | H0 của thang giám sát không được thoả; hai "FAIL" và một "INCONCLUSIVE" ở S4 | — |
| 23 | Thêm dấu chấm làm tăng điểm của hệ tinh chỉnh trên XM3600 dưới P0 | DESCRIPTIVE; hàng PTB là POST HOC | 3.3, S11 | Bảng B.6 | +2.71 [2.23, 3.21]; +2.75 [2.32, 3.20]; 0.00 | m22 |
| 24 | Đồng thuận bỏ-một-ra trong cùng người viết không phải trần của con người | DESCRIPTIVE | 3.2 | — | 85.33 / 46.90 / 60.50 | m23 |
| 25 | Không kết quả chính nào xuất hiện ở bài FAIR 2026; không con số nào là kết quả chính ở cả bài này và bài song hành | DESCRIPTIVE (tuyên bố của tác giả) | 1, 7.3, S12 | Bảng B.24 | — | — |

Danh sách khoá của bảng kê số liệu:

- m1: `c3_n2_exchangeability_all_datasets.json::k5_exchangeability_audit.ktvic_test_objects_in.adjacent_share` (cùng `adjacent_share_ci95`, `adjacent_share_null`, `total_doubletons`)
- m2: `slot_null.json::splits.ktvic_test_objects_in.adjacent_share.null_mean`
- m3: `c1_b1_b6_reproduction.json::B5_L5_cider_punct_and_uitviic_chair.ktvic_period_audit.test_refs_ending_period`
- m4: `c8_l5_d1_d3a_cpu_audit.json::l5_d1_punct_idf_law|ktvic_test_k1_to_k5_curves|p1assist_s42-short|first_k|k=5|d_abs`
- m5: `ptb_protocol.json::ktvic_test.systems.p1assist_s42-short.PTB.first_k.k=5.d_add_minus_strip` và `ptb_protocol.json::ktvic_test.systems.zeroshot-short.PTB.first_k.k=5.as_written`
- m6: `c8_l5_d1_d3a_cpu_audit.json::l5_d1_punct_idf_law|ktvic_test_k1_to_k5_curves|zeroshot-short|first_k|k=5|cider_strip`
- m7: `pilot_results.json::protocols|P1_syllable_raw(evaluate.py --also-syllable)|CIDEr|p1-gold` trừ `pilot_results.json::protocols|P0_official_rdr|CIDEr|p1-gold` (hàng "derived"); `pilot_results.json::ranking|P1_syllable_raw(evaluate.py --also-syllable)|tau_all`
- m8: `SUMMARY.json::meta.ktvic_systems_with_any_change`; `cay_audit.json::references.ktvic_train_refs.emitted_cay_tokens`
- m9: `cider_3seed_mean.json::mean` và `cider_3seed_mean.json::sd_sample_ddof1`
- m10: `g1_repro_gate_machine2.json::metric_comparisons.CIDEr.rescored_value`
- m11: `b2_ktvic_test_posthoc.json::estimate.mean` (cùng `estimate.sd`, `n_after`)
- m12: `decide.json::P-B1.b ; P-B1.ci95 ; P-B1.verdict ; P-B1.rule`
- m13: `decide.json::sensitivity_minus_dev_twin.pooled.b ; .ci95`; `b1_mask7_posthoc.json::estimate.b`
- m14: `d_extrap::primary.forms.F1.e ; primary.forms.F1.ci95`
- m15: `b_f1_run.json::primary.D_MBR_x100_mean_lo_hi.0` và `b_f1_run.json::primary.verdict`
- m16: `b_posthoc_mbr3_run.json::primary.D_MBR_x100_mean_lo_hi[0..2]`
- m17: `b_n1_run.json::predictions.LBB-P1.{point,ci95,verdict}`
- m18: `scores.json::external_systems` và `scores.json::distinct_sources`; `gpu_seconds.tsv` (tổng, hàng "derived")
- m19: `uitviic_p1_s43-short.json::results[0].scores_scaled_x100.CIDEr`; `uitviic_52a_52b_comparison.json::test.short.fuse2_minus_p1_paired_b5000.inst_only_norm.F1[0]`
- m20: `T1_RESULT.json::tau_c.b`, `T1_RESULT.json::tau_c.judge`, `T1_RESULT.json::delta_judge`, `T1_RESULT.json::h1a.lower_bound_95`; `T1_THRESHOLDS.json::sesoi`
- m21: con số 136.0 là hàng "literature (protocol not matched)" của bảng kê, không có khoá tệp
- m22: `xm3600_period_cider_decomposition_v1.json::cross_system_drop_decompositions_token_level.p1_s43_short_vs_zeroshot_short.drop_decomposition.by_append_period_to_ft_pred.cider_shift_x100.est`
- m23: `human_parity.json::1v4.human.P` (cùng `1v4.human.R`, `1v4.human.F1`)

## B.12 Danh mục việc cần rà soát và hoàn thiện

Danh mục gộp các nhận xét ở B.1–B.10, xếp theo mức quan trọng trong từng nhóm, kèm vị trí trong bài và đề xuất cụ thể.

### B.12.1 Lỗi hoặc mâu thuẫn cần sửa

1. **Câu hỏi về mức tăng chưa được trả lời đúng như tiêu đề hứa.** Vị trí: tóm tắt, tiêu đề Mục 5.3 và Mục 6.3, dòng đầu `outline_B.md`. Mục 5.3 chỉ xác lập mức tăng tồn tại trên dữ liệu phát triển; Mục 6.3 tự nói không phân định được nó đo gì. Đề xuất: quyết định kết quả chính của bài, rồi sửa tiêu đề Mục 5.3 và câu hỏi trong tóm tắt cho khớp với điều được chứng minh.
2. **Nghiên cứu ở Mục 6.2 thiếu toàn bộ phần đỡ.** Vị trí: Mục 6.2, Mục 3.1, Mục 3.6, Mục 7.1, Mục 7.4, Phụ lục S1, Bảng S12.1, `paperB.bib`. Đề xuất: thêm mô tả phương pháp (tên các mô hình, ba cấu hình, tổng số chú thích, quy tắc quyết định đầy đủ), nhãn đăng ký, một mục hồ sơ trong phụ lục, mục dữ liệu và trích dẫn cho Objects365, và một đoạn hạn chế; hoặc chuyển cả nghiên cứu sang phụ lục và giữ một câu dẫn kèm lời rào.
3. **Mục 5.3 chưa đáp ứng các nghĩa vụ báo cáo của chính tệp đăng ký.** Vị trí: Mục 5.3, phụ lục. Đề xuất: nêu cột quyết định (đã gỡ dấu câu cuối) và in giá trị như được viết bên cạnh; thêm bảng 15 điểm của đường cong với điểm zero-shot và hai hàng lặp lại; in nhãn của quy tắc phụ theo hạt giống, độ cong, bước tăng ở hai kích thước lớn nhất và kết quả trúng hay trượt của dự đoán F1; nói rõ +9.40 và +9.61 dùng hai bộ chấm khác nhau; thêm lời công bố rằng phép thử ngoại suy không mù ở kích thước đầy đủ và in ước lượng của cả ba dạng đường cong.
4. **Câu về tính đầy đủ của phụ lục và các thuật ngữ treo.** Vị trí: đoạn mở đầu phụ lục; S4, S5.1, S5.2, S5.8; Bảng S12.1. Đề xuất: bổ sung dòng hồ sơ cho các phép thử đã chạy nhưng không còn được báo cáo, hoặc thu hẹp câu "no test is left out"; định nghĩa "panel" trong phụ lục; sửa hàng UIT-OpenViIC của Bảng S12.1.
5. **Tóm tắt dưới giới hạn độ dài và mạnh hơn thân bài.** Vị trí: `outline_B.md`. Đề xuất: đưa tóm tắt về khoảng 150–250 từ; thay "shows" bằng diễn đạt khớp Mục 3.2; ghi nhãn hậu nghiệm cho hàng PTB; đổi "We release" cho khớp tình trạng phát hành; đồng bộ `STUDY_BRIEF_B.md`.
6. **Khẳng định chung về quy trình tiếng Việt và cụm "up to 35 points".** Vị trí: Mục 3.3. Đề xuất: viết câu về quy trình ở dạng điều kiện như Mục 1; sửa cụm số cho khớp mức 36.17 điểm với một tham chiếu.
7. **Câu "Every result in the main text comes from one model".** Vị trí: Mục 6.6, Mục 7.1. Đề xuất: giới hạn vào các hệ thống do nhóm huấn luyện, vì Mục 3.6 và Mục 6.2 dùng hệ thống khác.
8. **Câu mở đầu kết luận và phạm vi của chữ "these effects".** Vị trí: Mục 8. Đề xuất: tách quy tắc so khớp khỏi danh sách những thứ một điểm CIDEr đo; tách hệ số dốc theo dữ liệu khỏi câu "None of these effects ...".
9. **Bảng 2.1 và câu "quantifies both points".** Vị trí: Mục 2, Mục 1. Đề xuất: bỏ hoặc thay cột "Two panels"; kiểm lại chữ "quantifies" cho điểm về CHAIR.
10. **Trùng lặp ảnh và các câu về phía phát triển.** Vị trí: Mục 3.1, Mục 5.3, Phụ lục S1 và S6. Đề xuất: một đoạn thống nhất nêu quy tắc phát hiện, số ảnh ở cả phía kiểm tra (16 trên 558) và phía phát triển (7 ảnh), và con số nào đã được tính lại.
11. **Chỗ trống của tác giả.** Vị trí: Mục 3.6, Mục 7.2, Mục 7.5 (giấy phép, DOI); thư gửi ban biên tập (ba dòng ORCID, trong khi trang tên bài đã có ORCID của tác giả thứ nhất); mục FAIR 2026 trong `paperB.bib` (trang và DOI).
12. **Vị trí của Statements and Declarations và chữ viết tắt chưa định nghĩa.** Vị trí: Mục 7.5; toàn bài và phụ lục (MBR, UPE, SFT, DPO, RFT, CHAIR_i, "one-look rule", các mức bằng chứng, T6). Ghi thêm: ký hiệu K2 vừa là một điều kiện huỷ ở Mục 5.1 vừa là mã của một tệp bị loại ở S8.
13. **Câu chữ về vai trò nội bộ trong phụ lục.** Vị trí: S6, S8. Đề xuất: viết lại theo nghĩa khoa học; cân nhắc bỏ tên tài khoản chủ kho mã và tên tệp ảnh.
14. **Tệp phụ trợ lỗi thời.** Vị trí: `STATUS.md`, `new_vs_FAIR.md`, `SEPARATION_FAIR_A.md`, danh sách khẳng định trong `outline_B.md`, `citation_map_B.tsv`, hai mục bib không còn được trích, ghi chú vị trí và các hàng đã rút trong `number_manifest_B.tsv`, số đếm của phép quét văn bản ở S13, danh mục tệp của Bảng S13.2. Đề xuất: cập nhật sau khi văn bản ổn định và kho lưu trữ được dựng lại; chạy lại phép kiểm trùng lặp văn bản với FAIR và với bài song hành trên văn bản hiện hành.
15. **Ba kiểm kê hệ thống (73, 79, 26) và xếp hạng tạp chí (Q1 so với Q2).** Vị trí: Mục 3.4, Mục 3.5, Mục 5.1; `outline_B.md` và `STUDY_BRIEF_B.md`.

### B.12.2 Điểm nên làm rõ

1. Mục 3.2: phiên bản bộ so khớp dùng cho thống kê, cách tính khoảng tin cậy, giả định đứng sau giá trị z; có báo cáo được theo từng người chú thích hay không; con số nào đo hệ quả "năm tham chiếu có giá trị ít hơn năm".
2. Mục 3.1: mô tả và trích dẫn quy tắc phát hiện ảnh gần trùng.
3. Mục 3.4 và các nơi so với GRIT: biến thể hệ số Kendall; in giá trị khoảng cách tới 136.0 và nguồn gốc của con số này.
4. Mục 4: thêm bảng hệ thống theo phép phân tích (như Bảng B.9); lý do của định nghĩa F1 trộn vi mô và vĩ mô; dùng P1 làm đối chứng khớp mặt nạ cho fuse2; điểm của fuse2 (chi tiết) dưới cách xoá kiểu PTB.
5. Mục 5.1: định nghĩa phép chọn MBR-3; độ phân tán cho các hàng của Bảng 5.1; cách diễn đạt sự khác dấu giữa lần nhìn đã đăng ký và hai lần nhìn không đăng ký.
6. Mục 5.2: mức tăng +6.67 điểm phần trăm có được kiểm ở số lượng khớp không; yếu tố dấu câu trên UIT-ViIC.
7. Mục 3.5 và Mục 7.4: nguồn gốc của quy tắc v3; quyết định về việc khai báo công cụ AI theo chính sách hiện hành của tạp chí.
8. Mục 7.1: giải thích cổng đồng thuận của các đánh giá trước đây; thêm các hạn chế còn thiếu (một bộ chuẩn, không có dữ liệu tiếng Anh, mức phổ biến của quy trình bỏ bước xoá dấu câu).
9. Mục 7.3: nhắc bản thảo liên quan thứ hai mà thư gửi ban biên tập đã công bố và cách nó dùng tập kiểm tra KTVIC.
10. Phụ lục: chú thích về độ chính xác số của Bảng S2; chú thích tránh nhầm hai giá trị 41.71; kết quả của tập độ nhạy ở S4.
11. Dựng lại bản thảo theo mẫu của tạp chí để biết số trang hiện tại.

### B.12.3 Câu hỏi phản biện có thể gặp

1. Các quy trình chấm bỏ bước xoá dấu câu của PTB phổ biến đến đâu, và rủi ro này ảnh hưởng đến ai ngoài bộ chấm của nhóm tác giả, khi mã công khai của các hệ cơ sở KTVIC có xoá dấu câu?
2. Vì sao suy luận "một người viết" đáng tin khi các kho ngữ liệu đối chứng nằm trong một bài chưa công bố và phân phối không theo hoán vị là hậu nghiệm?
3. Mức tăng +9.61 cho mỗi lần nhân đôi đo điều gì, vì sao chỉ có trên dữ liệu phát triển, và lần nhìn xác nhận sẽ được làm trên dữ liệu nào khi tập kiểm tra KTVIC đã đóng?
4. Vì sao phép thử đã đăng ký của hệ thống cuối cùng cho "FAIL" trong khi hàng hậu nghiệm trên đầu ra P1-R cho hiệu dương?
5. Vì sao không so với các hệ thống tiếng Việt đã công bố dưới giao thức khớp? `STUDY_BRIEF_B.md` đã chuẩn bị câu trả lời: điểm công bố dùng giao thức khác và quy trình của họ không xác minh được.
6. Vì sao không có đánh giá của con người, và vì sao một cổng đồng thuận cao lại dừng phân tích các đánh giá trước đây?
7. Các bản đăng ký trước có kiểm chứng được từ bên ngoài không, khi chúng chỉ tự chứng thực?
8. Các kết luận có giữ với mô hình nền khác không, khi mô hình nền thứ hai dừng ở bước kiểm và phương án 3B không được báo cáo?
9. Đã có ai ngoài nhóm tác giả chạy bộ công cụ chưa, và khi nào kho lưu trữ có DOI công khai?
10. 16 ảnh kiểm tra trùng hoặc gần trùng với ảnh huấn luyện ảnh hưởng thế nào đến các con số kiểm tra ngoài con số đã được tính lại?
11. Nghiên cứu ở Mục 6.2 đóng vai trò gì trong lập luận của bài khi nó dừng ở giai đoạn phát triển và bài không khẳng định tính hợp lệ?

Về các câu trả lời đã chuẩn bị, `STUDY_BRIEF_B.md` có bảy câu trả lời ngắn; câu thứ bảy ở đó (về số chuỗi 12 từ trùng với bài song hành) không khớp với dòng cập nhật ở đầu chính tệp ấy và với danh sách kiểm của `SEPARATION_FAIR_A.md`, nên cần sửa trước khi dùng.

## B.13 Thuật ngữ và ký hiệu

**Bảng B.28.** Thuật ngữ và ký hiệu của bài, kèm thuật ngữ tiếng Việt dùng trong phần báo cáo này.

| Tiếng Anh | Tiếng Việt | Nghĩa trong bài |
|---|---|---|
| benchmark | bộ chuẩn đánh giá | bộ dữ liệu kèm tập kiểm tra dùng để so sánh hệ thống; ở đây chủ yếu là KTVIC |
| image captioning | sinh chú thích ảnh | sinh một câu mô tả cho một ảnh |
| reference (caption) | chú thích tham chiếu, tham chiếu | chú thích do người viết, dùng làm chuẩn chấm; KTVIC có năm tham chiếu mỗi ảnh |
| audit | kiểm định | phép đo một thuộc tính của bộ dữ liệu hoặc của quy trình chấm, có tập lệnh chạy lại được |
| protocol card | phiếu giao thức | bảng ghi bộ tách từ, biến thể CIDEr, thang điểm, chính sách dấu câu, cách giải mã và bộ so khớp của mọi điểm số |
| evaluation kit | bộ công cụ đánh giá | bộ chấm, phiếu giao thức, bộ so khớp, tập lệnh chia dữ liệu, tập lệnh kiểm định và hồ sơ |
| controlled system, measuring instrument | hệ thống có kiểm soát, công cụ đo | P1-R: một mô hình nền, một công thức, giải mã cố định, dùng để đo ảnh hưởng của giao thức |
| backbone | mô hình nền | Qwen2.5-VL-7B-Instruct |
| fine-tuning; zero-shot | tinh chỉnh; zero-shot | huấn luyện tiếp trên KTVIC; dùng mô hình nền không huấn luyện thêm |
| P1, P1-R, fuse2 | giữ nguyên | P1: đích là tham chiếu đầu tiên, mặt nạ cũ; P1-R: như P1, mất mát chỉ trên phần trả lời; fuse2: thêm hàng chi tiết hợp nhất hai tham chiếu |
| loss mask (legacy; response-only) | mặt nạ hàm mất mát (cũ; chỉ-trả-lời) | các token đi vào hàm mất mát khi huấn luyện |
| dev300 | giữ nguyên | tập phát triển 300 ảnh tách từ tập huấn luyện KTVIC bằng hạt giống cố định |
| seed | hạt giống | hạt giống ngẫu nhiên của một lần huấn luyện (42, 43, 44) |
| word segmentation; syllable tokenisation | tách từ; tách theo âm tiết | tách văn bản thành từ (RDRSegmenter, pyvi) hoặc thành âm tiết ở khoảng trắng |
| PTB-style punctuation removal | xoá dấu câu kiểu PTB | xoá các token trong danh sách dấu câu của bộ tách PTB khỏi ứng viên và tham chiếu trước khi chấm |
| P0; P0s; PTB; SYL; PYVI | giữ nguyên | các cột giao thức: dấu câu như được viết; gỡ dấu câu cuối của ứng viên; xoá kiểu PTB; âm tiết; pyvi |
| object matcher (v1, v2, v3) | bộ so khớp đối tượng | ánh xạ từ tiếng Việt sang lớp đối tượng; v1 là từ vựng 113 mục, v2 thêm chuẩn hoá dấu thanh, v3 thêm quy tắc chưa có người duyệt |
| gold | tập chuẩn vàng | tập đối tượng được coi là đúng cho một ảnh: hợp các tham chiếu, hoặc nhãn thực thể COCO |
| exchangeability | tính hoán đổi được | giả thiết rằng thứ tự năm tham chiếu không mang thông tin |
| doubleton | cặp đôi | lớp đối tượng được đúng hai trong năm tham chiếu của một ảnh nêu |
| adjacent share | tỉ lệ kề nhau | tỉ lệ cặp đôi nằm ở hai vị trí tham chiếu kề nhau; giá trị không 0.40 |
| slot | vị trí | thứ tự của một tham chiếu trong năm tham chiếu của ảnh |
| permutation null (slot-rate-preserving) | phân phối không theo hoán vị (giữ tỉ lệ theo vị trí) | phân phối tham chiếu khi gán lại ai nêu đối tượng nào mà giữ các tổng theo tham chiếu và theo đối tượng |
| leave-one-out | bỏ-một-ra | so mỗi tham chiếu với bốn tham chiếu còn lại |
| pre-registration; registered verdict | đăng ký trước; phán quyết đã đăng ký | dự đoán và quy tắc quyết định được commit trước đầu ra; kết luận mà quy tắc ấy tạo ra |
| REGISTERED, LOCALLY_FROZEN, POST_HOC, EXPLORATORY | giữ nguyên | bốn nhãn đăng ký của Phụ lục S1 |
| stop rule; kill condition; KILL | quy tắc dừng; điều kiện huỷ | điều kiện đặt trước làm dừng một nghiên cứu hoặc huỷ một biện pháp; K2 và K3 là hai điều kiện huỷ của phép thử cuối cùng |
| one-look rule | quy tắc một lần nhìn | quy tắc của nhóm tác giả theo đó tập kiểm tra KTVIC đã đóng sau lần đánh giá đã đăng ký; bài dùng thuật ngữ này mà không định nghĩa |
| smallest effect of interest | hiệu ứng nhỏ nhất đáng quan tâm | ngưỡng hiệu ứng đặt trước để coi một khác biệt là có ý nghĩa |
| supervision ladder; frontier; frontier residual | thang giám sát; đường biên; phần dư so với đường biên | chuỗi công thức đích huấn luyện; đường độ chính xác–số lượng neo trên P1; độ chính xác quan sát trừ độ chính xác đường biên dự đoán |
| count-matched control | đối chứng khớp số lượng | phép so ở cùng số đối tượng được nêu; công cụ của bài song hành |
| seed consensus (MBR-3) | đồng thuận hạt giống | phép chọn một chú thích trong ba đầu ra của ba hạt giống; hệ thống cuối cùng của phép thử đã đăng ký |
| companion paper | bài báo song hành | bản thảo đang soạn của cùng nhóm tác giả về điểm ảo giác ở mức đối tượng |
| M | giữ nguyên | số lớp đối tượng được nêu trên mỗi chú thích |
| P, R, F1 | độ chính xác, độ phủ, F1 | điểm đối tượng theo công thức (B.3) |
| CHAIR_i | giữ nguyên | biến thể của CHAIR mà bài dùng (CHAIR đếm các đối tượng được nêu mà vắng trong tập chuẩn vàng); bài không khai triển chỉ số i |
| τ, τ_b, τ_c | hệ số Kendall | tương quan thứ hạng; bài dùng ba ký hiệu ở Mục 3.4, Phụ lục S4 và Mục 6.2 |
| $b$, $a_s$, $x_L$, $N_L$, $y_{s,L}$ | giữ nguyên | hệ số dốc cho mỗi lần nhân đôi, hệ số chặn theo hạt giống, logarit cơ số 2 của số ảnh huấn luyện, số ảnh huấn luyện, điểm trung bình trên dev300, theo công thức (B.5); trong Phụ lục S2 chữ b còn chỉ số mũ của đường biên |
| $e$, T | giữ nguyên | sai số dự đoán của phép thử ngoại suy theo công thức (B.6) và ngưỡng ±2.0 của nó |
| $D_{\mathrm{MBR}}$ | giữ nguyên | hiệu ghép cặp giữa phép chọn MBR-3 và trung bình thành viên, công thức (B.4) |
| α | giữ nguyên | hệ số nội suy trọng số của WiSE-FT (α = 1 là fuse2); cũng là tham số α của LoRA ở Mục 4.1 |
| κ | giữ nguyên | hệ số dốc chuyển từ sự khớp với tham chiếu sang sự khớp với nhãn thực thể (Phụ lục S9) |
| K1, K5, K6 | giữ nguyên | mã của ba hệ thống bên ngoài ở Phụ lục S8 |


## B.14 Bản thảo viết lại: thông tin chung

Các mục từ đây đến B.28 thuật lại bản thảo viết lại của bài B. Quy ước trình bày như ở đầu Phần B. Nguồn là ba tệp của bản thảo: thân bài `paper.md`, hai phụ lục trực tuyến trong `online_resource.md` và bảng kê số liệu `number_manifest_B_v2.tsv`. Bài in rất ít công thức; các công thức (B.8) đến (B.13) viết lại bằng ký hiệu những định nghĩa mà bài nêu bằng lời. Bốn hình của bài (Fig. 1, Fig. 2, Fig. 3 và Fig. EF1) mới có chú thích và đặc tả, chưa có tệp hình, nên phần này không chèn hình nào. Một số tài liệu bài trích chưa có trong `paperB.bib`; phần này gọi chúng bằng tên tác giả và năm trong lời văn, không dùng khoá trích dẫn.

### B.14.1 Tên bài, nơi gửi và trạng thái soạn thảo

Tên bài là "Front-end validity of Vietnamese caption-score comparisons: a listed family, a per-comparison certificate and a registered application". Tạp chí đích vẫn là Language Resources and Evaluation. Từ khoá bài ghi là: Vietnamese image captioning; evaluation methodology; tokenisation; word segmentation; CIDEr; preregistration. Dòng tác giả còn để trống, chờ nhà nghiên cứu chính đặt.

Bản thảo ở một trạng thái soạn thảo có chủ ý chưa đầy đủ, và chính nó nói rõ điều này. Bản đăng ký còn một dự đoán thứ ba (P3) và một phép kiểm phương pháp (P4), thuộc một bước đăng ký chạy sau các bước khác; ở trạng thái mặc định hiện nay chúng được giữ ngoài văn bản, Mục 6.6 ("Reproduction of published scores") chỉ là một chỗ neo trống, và bài ghi: "The paper is not submitted in this state". Việc đưa P3 và P4 vào, việc in điểm của các hệ cơ sở và việc gọi tên hệ thống của nhóm khác là các quyết định còn chờ nhà nghiên cứu chính. Bài cũng tự ghi rằng nó dài hơn kế hoạch ở các Mục 5, 6 và 8, theo nguyên tắc viết bản đầy đủ trước rồi tác giả cắt khi viết lại.

### B.14.2 Điều bài báo khẳng định

Tóm tắt nêu rằng điểm của chú thích ảnh tiếng Việt phụ thuộc vào khâu xử lý văn bản đầu vào: đơn vị (âm tiết hay từ đã tách), vị trí dấu thanh, dấu câu và chữ hoa. Bài trình bày FE-CERT, một thủ tục "combining known ideas", tuyên bố một phép so sánh hai hệ thống là CERTIFIED chỉ khi hiệu CIDEr-D có ý nghĩa thống kê theo cùng một chiều dưới mọi thành viên của một họ khâu xử lý chấp nhận được và được liệt kê sẵn. Bài báo cáo một lần áp dụng đã đăng ký, và tóm tắt in từng nhãn đúng như nó rơi:

- P1 (held-out front-end check) là "INCONCLUSIVE": trong 72 chứng nhận sát biên trên họ phát triển (68 DEVELOPMENT, 4 lần chấm đầu tiên), 2 chứng nhận vỡ dưới các thành viên để dành (0.028; hai cận Clopper–Pearson một phía 95% là 0.005 và 0.085, chỉ có nghĩa danh nghĩa vì các phép so sánh dùng chung tệp).
- P1 mang thêm nhãn đăng ký "LOW-SENSITIVITY": họ âm tiết bị các đơn vị phát triển khác làm vỡ ở 6 trong 915 chứng nhận của nó (0.0066; quy tắc: nhiều nhất 0.05).
- P2, trên lần chấm đầu tiên các đầu ra do nhóm khác công bố, là "NOT SUPPORTED": "the certificate changed few conclusions in this pool (2 of 10)".
- Ở phần đánh giá của con người, hai người chấm đánh giá 300 cặp chú thích; mức đồng thuận giữa hai người chấm thấp (Cohen's kappa 0.351), nên theo quy tắc đã đăng ký không giả thuyết nào mang nhãn: thứ tự khi bỏ dấu câu khớp với lựa chọn của cả hai người chấm ở 16 trong 28 cặp quyết định (p một phía = 0.286), và thứ tự theo từ ở 37 trong 75 cặp (p hai phía = 1.000).
- Khâu xử lý tham chiếu vẫn là mặc định để báo cáo; phần đánh giá của con người không cho kết quả có nhãn nào để khuyến nghị một thành viên khác.

Tóm tắt là dạng rút gọn; các câu đầy đủ, in nguyên văn ở Mục 1, Mục 6 và Mục 9 của bài, được chép ở B.15, B.20 và B.21.

### B.14.3 Điều bài báo thêm vào, theo lời bài

Mục 1 và Mục 2 của bài nói FE-CERT là sự kết hợp các ý tưởng đã biết, mỗi phần được ghi nguồn, và bài viết: "We make no priority claim". Phần bài tự nhận là thêm vào gồm bốn điều, đều là việc áp các ý tưởng ấy vào khâu xử lý văn bản khi chấm chú thích tiếng Việt: một họ được liệt kê với một quy tắc chấp nhận nêu rõ; một phép kiểm phán quyết dưới các khâu xử lý để dành, có quy tắc có thể không đạt và có đối chứng độ nhạy; một phép đếm số kết luận thay đổi trên đầu ra do nhóm khác công bố; và một phần ưu tiên của con người, được báo cáo không kèm nhãn vì đồng thuận giữa hai người chấm thấp. Bài gọi đây là các khác biệt kỹ thuật so với công trình được trích, và còn để dấu phải kiểm lại các phát biểu về tính mới.

### B.14.4 Những điều bài báo không khẳng định

Mục 1 nêu giới hạn ngay từ đầu. Kết quả trên tệp của chính nhóm tác giả là kết quả DEVELOPMENT trên các tham chiếu đã dùng trước đó, và các tệp ấy là biến thể của hệ thống của chính nhóm. Đầu ra của các nhóm khác chỉ được chấm lần đầu ở đây; ngoài nghĩa đó không có gì là "chưa thấy" theo nghĩa mạnh hơn. Bài không xếp hạng hệ thống tiếng Việt nào và không báo cáo điểm của hệ thống tiếng Việt đã công bố nào dưới giao thức của mình để so sánh. Bài không khẳng định gì ngoài tiếng Việt. Các nghiên cứu đăng ký trước đây của đề tài, vốn đặt câu hỏi khác trên cùng bộ chuẩn, được ghi ở Online Resource 2 với phán quyết không đổi. Mục 9 thêm rằng các nhãn được báo cáo từng nhãn một và không được gộp thành một phát biểu chung về phương pháp.

### B.14.5 Sơ đồ các mục của bản thảo viết lại

**Bảng B.30.** Sơ đồ mục của bản thảo viết lại (`paper.md` và `online_resource.md`) và vị trí tương ứng trong phần báo cáo này.

| Mục của bài | Nội dung | Mục báo cáo |
|---|---|---|
| Tóm tắt, từ khoá | câu hỏi, thủ tục, bốn nhóm nhãn, thành viên mặc định | B.14 |
| 1 Introduction | vấn đề, khoảng trống, thủ tục, các nhãn đúng như đã rơi, giới hạn | B.15 |
| 2 Related work and positioning | độ đo và cách báo cáo; dữ liệu, đơn vị và bộ tách từ tiếng Việt; nguồn của các ý tưởng; tách từ so với đánh giá của con người; quan hệ với công trình trước | B.16 |
| 3 Background | ba loại lựa chọn của người chấm; hai phép đo POST HOC về đơn vị và dấu câu | B.17 |
| 4 The front-end certificate | họ, thống kê và khoảng, quy tắc quyết định, điều được và không được bảo đảm | B.18 |
| 5 Registered design and data | đăng ký và nhãn bằng chứng; các tập so sánh; thứ tự các bước; dự đoán và quy tắc; thiết kế phần con người | B.19 |
| 6.1–6.5 Results | họ và điều kiện tiên quyết; so sánh phát triển; P1; P2; các hàng phụ và đối chứng | B.20 |
| 6.6 | chỗ neo trống ở trạng thái mặc định | B.20.6 |
| 6.7 Human preferences | kết quả phần đánh giá của con người, các công bố về cách tiến hành | B.21 |
| 7 Discussion and recommendations | chứng nhận dùng để làm gì; điều lần áp dụng cho phép nói; ba khuyến nghị; thành viên được khuyến nghị | B.22 |
| 8 Limitations | sáu nhóm hạn chế và một đoạn về các nghiên cứu đăng ký trước đây | B.23 |
| 9 Conclusion; Statements and Declarations | kết luận và các tuyên bố | B.24 |
| Online Resource 1 (E.0–E.7) | hồ sơ của nghiên cứu FE-CERT đã đăng ký | B.25.1 |
| Online Resource 2 (S.0, S1–S28) | các nghiên cứu đăng ký trước đây và phần kiểm định chuyển từ thân bài cũ | B.25.2; nội dung ở B.2–B.10 |

### B.14.6 Nhận xét rà soát về thông tin chung

Thứ nhất, bài chưa ở trạng thái nộp được và tự nói như vậy: P3, P4 và Mục 6.6 vắng mặt, dòng tác giả trống, và nhiều chỗ còn dấu `[CITE-TO-VERIFY]`, `[TO VERIFY]`, `[TO RE-VERIFY]`, `[AUTHOR TO PROVIDE]`, `[AUTHOR TO CONFIRM]`. Người đọc cần coi mỗi dấu ấy là một việc còn mở (B.27 gom lại). Thứ hai, tóm tắt gọi thành viên mặc định là "the reference front end", còn thân bài gọi là `f0`; hai cách gọi chỉ cùng một thành viên (Mục 4.1 của bài), nên dùng một tên và định nghĩa nó ở lần xuất hiện đầu. Thứ ba, tóm tắt in nhãn "LOW-SENSITIVITY" kèm con số 0.0066 nhưng không nói rằng phép tính đã dùng tập dự phòng thay cho tập sát biên; chi tiết này chỉ có ở Mục 1, Mục 6.3 và Mục 9. Đó là dạng rút gọn do giới hạn độ dài, nhưng người đọc chỉ xem tóm tắt sẽ không biết câu đăng ký gắn với nhãn không mô tả đúng tập đã dùng (xem B.20.3). Thứ tư, số bảng không theo thứ tự xuất hiện: Table 7 nằm ở Mục 6.5, trước Table 6 ở Mục 6.7. Thứ năm, bài viết số nguyên lớn theo hai kiểu: 2,790 có dấu phẩy, còn 1101 và 1123 thì không; nên thống nhất. Thứ sáu, bốn hình đều chưa dựng; đặc tả yêu cầu hình vectơ, dùng hoa văn bên cạnh màu, và không in giá trị nào không có trong bảng tương ứng.

## B.15 Mục 1 của bản thảo viết lại: Mở đầu (Introduction)

**Nội dung.** Mục mở đầu xuất phát từ nhận xét rằng một điểm chú thích không được tính trên văn bản thô: trước khi đếm n-gram, một khâu xử lý văn bản đầu vào (text front end) quyết định thế nào là một token. Với tiếng Việt, khâu này có nhiều chỗ để lựa chọn hơn tiếng Anh. Các âm tiết viết rời nhau và một từ thường gồm hai âm tiết trở lên, nên bộ chấm phải đếm âm tiết hoặc gọi một bộ tách từ, mà có nhiều bộ tách từ đang được dùng. Dấu thanh của một số âm tiết có thể đặt trên một trong hai nguyên âm. Các bộ chấm còn khác nhau ở chỗ giữ hay bỏ dấu câu và chữ hoa. Bài dẫn hai phép đo trên một bộ chuẩn, làm trước nghiên cứu này và vì thế mang nhãn POST HOC, để cho thấy độ lớn của các lựa chọn ấy: riêng đơn vị đã làm CIDEr-D của một hệ thống xê dịch 15.64 điểm, và một dấu chấm thêm vào làm một hệ thống khác mất 35.17 điểm dưới bộ chấm giữ dấu câu.

Đoạn thứ hai đặt bối cảnh ít tài nguyên: tiếng Việt là ngôn ngữ ít tài nguyên trong nghiên cứu thị giác–ngôn ngữ [@joshi2020state; @lovenia2024seacrowd]; nghiên cứu chú thích dựa vào một vài bộ chuẩn, mỗi bộ từ vài nghìn đến khoảng mười lăm nghìn ảnh [@lam2020uit; @pham2024ktvic; @bui2026uit; @hoang2026hducap], và một hệ thống mới thường chỉ được so với các hệ trước trên một bộ. Một phép so sánh mà ở tiếng Anh sẽ được kiểm chéo trên nhiều bộ dữ liệu thì ở đây được quyết định bởi một hiệu điểm, còn khâu xử lý đứng sau hiệu ấy ít khi được báo cáo đầy đủ.

Đoạn thứ ba nêu khoảng trống. Việc bộ tách token làm điểm không so sánh được là điều đã biết: sacreBLEU gắn chữ ký phiên bản vào điểm và cảnh báo rằng điểm dưới các bộ tách khác nhau không so được với nhau [@post2018call]; SacreEOS làm điều tương tự cho một quy ước huấn luyện trong sinh chú thích [@hu2023request]. Với chú thích tiếng Việt, công trình gần nhất báo cáo điểm của các mô hình của chính nó dưới vài cách tách và độ trải giữa chúng [@nguyen2026scenetext]; câu này còn mang dấu phải đọc lại phụ lục của công trình ấy. Một chữ ký cho biết khâu xử lý nào đã được dùng, một bảng độ trải cho biết điểm thay đổi; không cái nào trả lời câu hỏi của người đọc bảng kết quả: phép so sánh hai hệ thống này có cho cùng kết quả dưới mọi khâu xử lý mà một người chấm cẩn thận có thể đã dùng hay không.

Đoạn thứ tư giới thiệu thủ tục và lần áp dụng. FE-CERT liệt kê một họ khâu xử lý chấp nhận được cho chú thích tiếng Việt (bốn đơn vị, ba mức vị trí dấu thanh, ba mức dấu câu và hai mức chữ hoa) và tuyên bố một phép so sánh là CERTIFIED khi hiệu CIDEr-D của nó có ý nghĩa theo cùng một chiều dưới mọi thành viên. Bảo đảm đứng sau phán quyết là danh nghĩa và dựa trên nguyên lý giao–hợp (intersection–union). Lần áp dụng được đăng ký trước khi bất kỳ đại lượng nào của nó tồn tại, và gồm: một phép kiểm dưới các khâu xử lý để dành, kèm đối chứng độ nhạy; một lần chấm đầu tiên các đầu ra do nhóm khác công bố; và các ưu tiên theo cặp của con người, chấm mù, vốn chỉ có thể quyết định thành viên nào được khuyến nghị để báo cáo và "are reported without labels because inter-rater agreement was low".

Đoạn thứ năm in từng nhãn đã đăng ký đúng như nó rơi, theo thứ tự của bản đăng ký. Về P1, bài viết: "P1 (held-out front-end check) is INCONCLUSIVE: of N = 72 near-margin certificates on the development family (z_min <= 4; 68 DEVELOPMENT, 4 first scorings of released outputs), 2 broke under the held-out front ends (r = 0.028; one-sided 95% Clopper-Pearson upper bound 0.085, lower bound 0.005)", và thêm rằng các phép so sánh dùng chung tệp nên không độc lập, cận Clopper–Pearson chỉ là một tóm tắt danh nghĩa. P1 mang nhãn đăng ký "LOW-SENSITIVITY" (quy tắc $r_{NC} \le 0.05$): họ âm tiết bị các đơn vị phát triển khác làm vỡ ở 6 trong 915 chứng nhận của nó ($r_{NC}$ = 0.0066); chỉ có 54 chứng nhận sát biên, ít hơn 59, nên phương án dự phòng đã đăng ký dùng toàn bộ các chứng nhận. Một hàng POST HOC đứng cạnh: cả 6 lần vỡ đều nằm trong 54 chứng nhận ấy. P2 là "NOT SUPPORTED", với lời đăng ký "the certificate changed few conclusions in this pool (2 of 10)"; 20 trong 22 phép so sánh lập được trong tập ấy đến từ một kho mã.

Về phần đánh giá của con người, Mục 1 in đầy đủ đoạn sau, nguyên văn: "In the human arm, two raters judged 300 caption pairs. Inter-rater agreement was low (Cohen's kappa = 0.351, bootstrap 95% interval 0.270 to 0.433; registered band 0.20 to below 0.40), so by the registered rule neither hypothesis carries a label. On pairs whose order changes with punctuation handling, the order with punctuation removed matched both raters' choice in 16 of 28 decisive pairs (0.571; 95% interval 0.372 to 0.755; one-sided p = 0.286). On pairs whose order changes with the unit, the word order matched both raters' choice in 37 of 75 decisive pairs (0.493; 0.376 to 0.611; two-sided p = 1.000). Neither test was rejected under Holm's correction; no label is attached." Nghĩa tiếng Việt: ở phần đánh giá của con người, hai người chấm đánh giá 300 cặp chú thích; đồng thuận giữa hai người chấm thấp (kappa của Cohen = 0.351, khoảng bootstrap 95% từ 0.270 đến 0.433; dải đã đăng ký từ 0.20 đến dưới 0.40), nên theo quy tắc đã đăng ký không giả thuyết nào mang nhãn. Ở các cặp mà thứ tự đổi theo cách xử lý dấu câu, thứ tự khi bỏ dấu câu khớp với lựa chọn của cả hai người chấm ở 16 trong 28 cặp quyết định (0.571; khoảng 95% từ 0.372 đến 0.755; p một phía = 0.286). Ở các cặp mà thứ tự đổi theo đơn vị, thứ tự theo từ khớp với lựa chọn của cả hai người chấm ở 37 trong 75 cặp quyết định (0.493; 0.376 đến 0.611; p hai phía = 1.000). Không phép thử nào bị bác bỏ sau hiệu chỉnh Holm; không nhãn nào được gắn. Đoạn này khép bằng câu về thành viên mặc định: "`f0` remains the default for reporting (registration l.304); the human arm, at low inter-rater agreement, gave no labelled result on which to recommend another member", và chỉ người đọc tới Table 6 để xem tỉ lệ riêng của từng người chấm.

Đoạn cuối nêu các giới hạn đã chép ở B.14.4.

**Nhận xét rà soát.** Mục mở đầu làm đúng điều một bài đăng ký trước cần làm: in mọi nhãn, kể cả ba nhãn không thuận lợi và một kết quả không có nhãn, trước khi người đọc tới phần kết quả. Có năm điểm cần xem lại. (i) Đoạn in nhãn dài và lặp nguyên văn ở Mục 6 và Mục 9; khi rút gọn, mỗi nhãn và các số đếm của nó phải còn nguyên, và không được thay "no label" bằng một cách nói khác nghe như một phán quyết. (ii) Câu về thành viên mặc định chứa một tham chiếu nội bộ tới số dòng của bản đăng ký ("registration l.304"); người đọc bên ngoài không tra được, nên trước khi nộp cần thay bằng tên mục của bản đăng ký hoặc của Online Resource 1. (iii) Ở đoạn này bài viết "kappa" bằng chữ, còn Mục 5.5 và Table 6 dùng ký hiệu κ; nên thống nhất một cách viết mà không đổi nội dung câu. (iv) Hai con số mở đầu (15.64 và 35.17) đều là POST HOC và đều của một hệ thống trên một bộ chuẩn; bài đã ghi nhãn, nhưng người đọc dễ hiểu chúng là kết quả của nghiên cứu đã đăng ký nếu chỉ đọc đoạn đầu, nên giữ chữ POST HOC ngay trong câu như hiện nay. (v) Câu về công trình gần nhất [@nguyen2026scenetext] còn dấu phải đọc lại; toàn bộ lập luận về khoảng trống tựa vào việc công trình ấy không cho phán quyết theo từng phép so sánh, nên phải đọc lại nguồn trước khi giữ câu.

## B.16 Mục 2 của bản thảo viết lại: Công trình liên quan và định vị (Related work and positioning)

**Nội dung.** Mục 2 gồm sáu đoạn có tiêu đề. Đoạn về các độ đo dựa trên tham chiếu và cách báo cáo nhắc rằng CIDEr gán trọng số cho n-gram của một chú thích theo tần suất văn bản nghịch đảo trên tập tham chiếu [@vedantam2015cider], nên một lựa chọn tách token đổi cả n-gram lẫn trọng số. Các độ đo chuẩn có những trường hợp hỏng đã biết [@caglayan2020curious] và đã được đánh giá lại so với đánh giá của con người [@kilickaya2016reeval]. Trong dịch máy, thêm hoặc bớt một dấu câu cuối câu làm đổi điểm của cả độ đo dựa trên chuỗi lẫn độ đo dựa trên mô hình [@jwalapuram2023pulling]; Mục 3 của bài cho đối ứng trong sinh chú thích, và FE-CERT đặt dấu câu thành một trục của họ. sacreBLEU làm cho thiết lập tách token và tham chiếu có thể báo cáo qua một chữ ký [@post2018call], SacreEOS làm vậy cho quy ước kết thúc chuỗi của huấn luyện tự phê bình [@hu2023request]. FE-CERT đi bước tiếp sau chữ ký: hỏi một phép so sánh có đứng vững qua các khâu xử lý được liệt kê hay không; câu rằng sacreBLEU không cho phán quyết theo từng phép so sánh còn mang dấu phải kiểm.

Đoạn về dữ liệu, đơn vị và bộ tách từ tiếng Việt liệt kê UIT-ViIC [@lam2020uit], KTVIC [@pham2024ktvic], UIT-OpenViIC [@bui2026uit] và HDUCap [@hoang2026hducap]. KTVIC công bố chú thích đã tách từ bằng RDRSegmenter, bộ tách từ của VnCoreNLP [@nguyen2018fast; @vu2018vncorenlp]. Công trình khác chấm theo âm tiết tách ở khoảng trắng, hoặc dùng pyvi và underthesea (hai tài liệu phần mềm này chưa có trong danh mục). Nghiên cứu tiếng Việt gần nhất, về chú thích văn bản trong cảnh, chấm mô hình của chính nó dưới vài cách tách, báo cáo độ trải và một lần đổi thứ tự ở mức ký tự, rồi chọn một đơn vị vì lý do tái lập [@nguyen2026scenetext]. Bài viết rằng công trình ấy không cho phán quyết theo từng phép so sánh, không cho ý nghĩa thống kê theo từng cách tách, không kiểm dưới khâu xử lý để dành, không chấm đầu ra của nhóm khác và không có đánh giá của con người; cả câu còn mang dấu phải kiểm với bài gốc.

Đoạn về nguồn của các ý tưởng ghi rõ từng thành phần. Ý cốt lõi, kiểm một kết luận dưới mọi đặc tả có thể bảo vệ được, là của phân tích đường cong đặc tả (Simonsohn và cộng sự, 2020) và phân tích đa vũ trụ (Steegen và cộng sự, 2016). Bảo đảm là lập luận giao–hợp (Berger, 1982; Berger và Hsu, 1996), và bài ghi rằng cả hai nguồn phải được đọc trước khi trích. Phép thử cho mỗi thành viên là bootstrap ghép cặp dùng cho độ đo ở mức ngữ liệu (Koehn, 2004; Dror và cộng sự, 2018). Các tài liệu này chưa có trong `paperB.bib` và đều mang dấu chờ kiểm. Phần bài tự nhận là thêm vào đã chép ở B.14.3.

Đoạn về tách token so với đánh giá của con người dẫn một nghiên cứu đặt các cách tách token cạnh đánh giá của con người cho tóm tắt văn bản ở các ngôn ngữ khác (Mondshine và cộng sự, 2025; chờ kiểm). Phần con người của bài khác ở ba điểm: nó về chú thích tiếng Việt; nó lấy mẫu các cặp mà hai khâu xử lý xếp hai chú thích theo thứ tự khác nhau; và quy tắc quyết định của nó được đăng ký trước khi có bất kỳ đánh giá nào. Đoạn về tính hợp lệ của bộ chuẩn đặt bài vào dòng nghiên cứu hỏi bộ chuẩn đo điều gì [@bowman2021fix; @raji2021everything], với phần thêm vào hẹp: một cách phát biểu, cho một phép so sánh trên một bộ chuẩn tiếng Việt, rằng phán quyết có phụ thuộc cách xử lý văn bản hay không. Đoạn cuối nêu quan hệ với công trình trước của cùng nhóm tác giả: một bài hội nghị đề xuất phương pháp xây dựng giám sát huấn luyện cho chú thích chi tiết tiếng Việt [@nguyen2026vsps]; bài viết đó là một công trình độc lập, và bài này dùng lại công thức tinh chỉnh của nó cho các hệ thống được chấm, không dùng kết quả nào. Các nghiên cứu đăng ký trước đây trên cùng bộ chuẩn và quan hệ với bản thảo song hành đang soạn được ghi ở Online Resource 2.

**Nhận xét rà soát.** Mục 2 trung thực về nguồn gốc ý tưởng, và đó là điểm mạnh trước một phản biện sẽ hỏi FE-CERT khác gì một bảng đa vũ trụ kèm quy tắc quyết định; chính Mục 8 của bài cũng nêu câu hỏi ấy. Điểm yếu là mức sẵn sàng của trích dẫn. Mười bốn tài liệu được liệt kê là cần thêm và chưa có trong `paperB.bib` (trong đó một tài liệu chỉ được trích ở phần đang giữ ngoài văn bản), và mỗi tài liệu chỉ được thêm sau khi định danh của nó được kiểm trên trang gốc. Hai nguồn của nguyên lý giao–hợp phải được đọc trước khi trích; nếu chưa đọc được, câu bảo đảm ở Mục 4.4 mất chỗ dựa. Ba câu phủ định về công trình khác (sacreBLEU không cho phán quyết theo từng phép so sánh; công trình tiếng Việt gần nhất không có năm điều; các phát biểu về tính mới) đều còn dấu phải kiểm, và phản biện sẽ đối chiếu chúng với bài gốc. Riêng vế "no significance per tokenisation" cần được kiểm kỹ nhất, vì một công trình có thể báo cáo ý nghĩa thống kê dưới đơn vị nó chọn; nếu vậy vế này phải thu hẹp. Cuối cùng, bài không có đoạn nào về các nghiên cứu trước đây thu thập ưu tiên của con người đối với chú thích ảnh; một phản biện của tạp chí về tài nguyên và đánh giá có thể chờ đoạn ấy khi bài có một phần con người.

## B.17 Mục 3 của bản thảo viết lại: Bối cảnh về khâu xử lý văn bản khi chấm chú thích tiếng Việt (Background)

**Nội dung.** Mục 3 nêu ba loại lựa chọn mà chữ viết tiếng Việt đặt ra cho người chấm. (i) Đơn vị: âm tiết cách nhau bằng khoảng trắng, nhiều từ là từ ghép hai âm tiết trở lên; bộ chấm có thể đếm âm tiết hoặc gọi một bộ tách từ để nối các âm tiết của một từ thành một token, và các bộ tách từ không nối cùng những âm tiết như nhau. (ii) Vị trí dấu thanh: ở các âm tiết có cặp nguyên âm oa, oe và uy, có hai cách đặt dấu thanh đang được dùng, và cả hai xuất hiện trong đầu ra của hệ thống. (iii) Dấu câu và chữ hoa: các tập tham chiếu khác nhau ở chỗ câu có kết thúc bằng dấu chấm hay không, và các bộ chấm khác nhau ở chỗ có bỏ dấu câu và quy về chữ thường hay không. Mỗi lựa chọn là một trục của họ ở Mục 4.

Bài nói rõ rằng các con số của mục này được tính ở một giai đoạn trước của đề tài, trước bản đăng ký ở Mục 5, trên tập kiểm tra KTVIC [@pham2024ktvic]. Chúng là bối cảnh POST HOC: chúng là lý do cho hai trục của họ và không phải kết quả của nghiên cứu đã đăng ký.

Về đơn vị (POST HOC): dưới bộ chấm đã commit của đề tài, vốn tách đầu ra và tham chiếu bằng RDRSegmenter, một hệ thống tinh chỉnh của nhóm đạt CIDEr-D 149.79. Tách cùng đầu ra và tham chiếu ấy thành âm tiết cho 165.43, tức xê dịch 15.64 điểm chỉ do đơn vị. Thứ tự các hệ thống phần lớn được giữ (Kendall τ = 0.969 trên 26 hệ thống), nên đơn vị làm đổi giá trị tuyệt đối nhiều hơn hẳn làm đổi thứ hạng. Một bộ tách từ thứ hai làm đổi điểm ít hơn nhiều: với pyvi cùng đầu ra đạt 149.12 (τ = 0.994 so với bộ chấm đã commit). RDRSegmenter tái lập đúng cách tách của chính bộ chuẩn trên 2,790 trong 2,790 tham chiếu kiểm tra.

Về dấu câu (POST HOC): không tham chiếu nào trong 2,790 tham chiếu kiểm tra của KTVIC kết thúc bằng dấu chấm. CIDEr-D không cho điểm một n-gram không bao giờ xuất hiện trong tham chiếu, nhưng n-gram ấy vẫn làm dài vectơ của chú thích ứng viên, nên mỗi dấu chấm làm giảm điểm của cả chú thích khi bộ chấm giữ dấu câu. Dưới bộ chấm đã commit, thêm một dấu chấm vào mọi đầu ra của một hệ thống tinh chỉnh vốn không bao giờ viết dấu chấm làm CIDEr-D của nó giảm từ 148.66 xuống 113.49 (−35.17 điểm, −23.66%). Khi token dấu câu được bỏ trước khi chấm, như bộ tách PTB của bộ chấm COCO chuẩn vẫn làm [@chen2015microsoft], cùng thay đổi ấy làm điểm xê dịch 0.00. Bài kết luận rằng cái giá của một dấu chấm là một tính chất của quy trình chấm. Hai phép đo đi kèm trên hai tập tham chiếu khác nằm ở Online Resource 2.

Đoạn cuối nói điều đã biết định hình bản đăng ký như thế nào. Bộ tách từ underthesea, về sau là đơn vị để dành, đã từng được chạy trên chú thích tham chiếu ở giai đoạn trước nhưng chưa bao giờ trên đầu ra của một hệ thống. Bản đăng ký cũng nêu, như một kỳ vọng chứ không phải một dự đoán, rằng ít phép so sánh giữa các hệ thống tinh chỉnh của nhóm sẽ đổi theo khâu xử lý và nhiều phép hơn sẽ đổi giữa các đầu ra zero-shot.

**Nhận xét rà soát.** Mục 3 dùng lại hai phép đo mà các mục B.4.3 và B.4.4 đã thuật chi tiết; các con số trùng với văn bản trước (149.79, 165.43, 15.64, 0.969, 149.12, 0.994, 148.66, 113.49, 35.17, 23.66%). Ba nhận xét cũ vẫn đúng: con số 35.17 là của một hệ thống với một hạt giống; hàng "0.00" là một phép tính hậu nghiệm; và τ được tính trên 26 hệ thống của chính nhóm. Điểm mới cần lưu ý là sự nhất quán về vai trò: Mục 3 gọi cả mục là POST HOC, nên không câu nào ở Mục 6 và Mục 7 được dựa vào hai con số này như bằng chứng của FE-CERT; bản thảo hiện giữ đúng ranh giới ấy. Đoạn cuối nêu một "kỳ vọng" của bản đăng ký nhưng không in con số nào cho nó; bài nên nói rõ ở Mục 6.2 kỳ vọng ấy được nhìn lại ra sao, hoặc nói rằng nó không được kiểm, vì phản biện sẽ hỏi. Việc underthesea đã chạy trên tham chiếu là một công bố cần giữ: nó giới hạn nghĩa của chữ "để dành" ở mức "chưa từng chạy trên đầu ra hệ thống".

## B.18 Mục 4 của bản thảo viết lại: Chứng nhận theo khâu xử lý văn bản (The front-end certificate)

**Nội dung.**

*Họ khâu xử lý chấp nhận được (Mục 4.1).* Một khâu xử lý là một dãy bước cố định áp lên một chú thích; FE-CERT áp cùng một dãy cho đầu ra của hệ thống và cho tham chiếu. Trước mọi thành viên có một bước chuẩn hoá: hợp nhất Unicode, thay mỗi dấu gạch dưới bằng một khoảng trắng, gộp và cắt khoảng trắng. Bước này không phải một trục; nó làm cho các đầu ra công bố ở dạng từ nối bằng gạch dưới so được với văn bản thường. Bốn trục theo sau theo thứ tự cố định: vị trí dấu thanh (T), xử lý dấu câu trước đơn vị (P), đơn vị (U) và chữ hoa (C). Với mức bỏ toàn bộ dấu câu, các token chỉ gồm dấu câu bị loại sau bước chữ hoa. Chữ hoa được xử lý sau đơn vị để bộ tách từ thấy văn bản đúng như được viết.

**Bảng B.31.** Họ khâu xử lý: trục, mức và đơn vị (Table 1 của bài, DESCRIPTIVE). Mỗi đơn vị có 3 × 3 × 2 = 18 thành viên.

| Trục | Mức | Định nghĩa | Vai trò |
|---|---|---|---|
| T, vị trí dấu thanh | `tw` | như được viết | |
| | `tm` | trong một chuỗi chữ cái kết thúc bằng một trong các cặp nguyên âm oa, oe, uy có một dấu thanh, dấu được chuyển sang nguyên âm thứ hai | |
| | `tf` | cùng phạm vi; dấu được chuyển sang nguyên âm thứ nhất | |
| P, dấu câu | `pk` | giữ như được viết | |
| | `pf` | bỏ chuỗi dấu câu kết câu và khoảng trắng ở cuối | |
| | `pa` | tách riêng mọi ký tự dấu câu và bỏ mọi token chỉ gồm dấu câu | |
| C, chữ hoa | `cf` | quy về chữ thường | |
| | `ck` | giữ nguyên | |
| U, đơn vị | `syl` | âm tiết: tách ở khoảng trắng | phát triển |
| | `rdr` | từ, RDRSegmenter (`VnCoreNLP 1.2`) | phát triển; đơn vị của thành viên tham chiếu |
| | `pyvi` | từ, pyvi (`0.1.1`) | phát triển |
| | `uts` | từ, underthesea (`9.5.0`) | để dành |
| | `chr` | ký tự | không chấp nhận được; chỉ có trong các hàng DESCRIPTIVE |

Một thành viên là một mức cho mỗi trục. Một thành viên là chấp nhận được khi (a) đơn vị của nó được một bộ chấm hoặc một bài báo công khai về chú thích tiếng Việt dùng, hoặc là một bộ tách từ tiếng Việt đã phát hành có phiên bản ghim, và (b) mỗi mức còn lại của nó được một bộ chấm như thế dùng, hoặc chỉ khác một mức đã được dùng ở vị trí dấu thanh, chữ hoa hoặc dấu câu cuối. Hai loại trừ được cố định cùng với họ. Đơn vị ký tự thoả (a), nhưng nơi duy nhất dùng nó báo cáo rằng nó làm méo điểm [@nguyen2026scenetext] (câu còn dấu phải đọc lại), nên nó bị loại đích danh và chỉ xuất hiện trong các hàng DESCRIPTIVE. Một quy trình lệch, tức xử lý đầu ra khác với tham chiếu, không bao giờ chấp nhận được.

Họ đầy đủ $F$ có 72 thành viên. Họ phát triển $F_{dev}$ gồm 54 thành viên của ba đơn vị âm tiết, RDRSegmenter và pyvi, là các đơn vị đề tài đã từng chạy trên đầu ra hệ thống. Họ để dành $F_{held}$ gồm 18 thành viên của underthesea, đơn vị đề tài chưa từng chạy trên đầu ra hệ thống. Bài nhấn mạnh: "Held-out" trong bài mô tả thành viên của họ khâu xử lý, không bao giờ mô tả dữ liệu. Thành viên tham chiếu `f0` là RDRSegmenter với dấu thanh như được viết, giữ dấu câu và quy về chữ thường; đó là giao thức đã tính các điểm trước đây của đề tài, và là thành viên mà một tác giả sẽ dùng để báo cáo. Với một phép so sánh, hai thành viên thuộc cùng một lớp (class) khi chúng cho dãy token giống hệt nhau trên mọi đầu ra và mọi tham chiếu liên quan; lớp được lập chỉ theo sự đồng nhất token, không bao giờ theo điểm.

*Thống kê và khoảng (Mục 4.2).* Một phép so sánh là một cặp tệp đầu ra $a$ và $b$ trên một danh sách ảnh, với các tập tham chiếu của một tệp tham chiếu. Dưới thành viên $f$, thống kê là trung bình trên các ảnh của hiệu CIDEr-D theo ảnh [@vedantam2015cider], với tần suất văn bản lấy từ các tham chiếu của danh sách ảnh dưới $f$:

$$D_f \;=\; \frac{1}{n}\sum_{i=1}^{n}\Big(c_f(a,i) - c_f(b,i)\Big) \tag{B.8}$$

trong đó $n$ là số ảnh của danh sách và $c_f(x,i)$ là CIDEr-D theo ảnh của tệp $x$ ở ảnh $i$ dưới thành viên $f$. Khoảng của $D_f$ có hai đầu là phân vị 2.5 và 97.5 của một bootstrap ghép cặp trên ảnh với 10,000 lần rút (hạt giống 20261112):

$$[L_f,\,U_f] \;=\; \big[\,Q_{2.5}(D_f^{*}),\; Q_{97.5}(D_f^{*})\,\big] \tag{B.9}$$

Cùng các lần rút được dùng cho mọi thành viên và mọi phép so sánh trên cùng danh sách ảnh, còn tần suất văn bản giữ ở giá trị của toàn danh sách. Khoảng là hai phía ở mức 95% vì chiều của phép so sánh được đọc từ dữ liệu. Khoảng chỉ nắm sự lấy mẫu ảnh: đầu ra, tham chiếu và các lần huấn luyện đứng sau hệ thống là cố định.

*Quy tắc quyết định (Mục 4.3).* Với một họ $G$ (có thể là $F_{dev}$, $F_{held}$ hoặc $F$), đặt

$$\text{sig}^{+}_f \iff L_f > 0, \qquad \text{sig}^{-}_f \iff U_f < 0. \tag{B.10}$$

Một phép so sánh nhận một trong các phán quyết sau, chép theo định nghĩa của bài. "CERTIFIED (a > b over G)": sig+ ở mọi lớp của $G$; "CERTIFIED (b > a)": sig− ở mọi lớp; đầu ra nêu chiều. "REVERSED": sig+ dưới một thành viên và sig− dưới một thành viên khác. "FRAGILE": không được chứng nhận và có ý nghĩa dưới ít nhất một thành viên; REVERSED là một tập con của nó. "NULL-STABLE": không có ý nghĩa dưới thành viên nào. Một phép so sánh FRAGILE được báo cáo kèm tập phá vỡ (breaking set): các lớp mà dưới đó chiều danh nghĩa của nó không có ý nghĩa, đếm theo mức của từng trục. Chiều danh nghĩa là chiều có ý nghĩa dưới `f0`, hoặc, khi `f0` không có ý nghĩa, là chiều có ý nghĩa dưới nhiều lớp hơn. Số đếm nối chứng nhận với thực hành là CHANGED: một phép so sánh là CHANGED khi nó có ý nghĩa dưới `f0` và không CERTIFIED trên $G$; mẫu số của tỉ lệ CHANGED là số phép so sánh có ý nghĩa dưới `f0`. Các phép so sánh NULL-STABLE và các phép chỉ có ý nghĩa dưới thành viên khác được báo cáo ở hàng riêng và không bao giờ vào tỉ lệ ấy. Một lần lật dấu điểm ước lượng (point-sign flip), tức hai lớp có dấu của $D_f$ trái nhau, được báo cáo không kèm phán quyết.

*Điều một chứng nhận bảo đảm và không bảo đảm (Mục 4.4).* Xét giả thuyết không rằng với một thành viên $f$ nào đó của $G$, hiệu trung bình tổng thể không lớn hơn không, trong đó tổng thể là các ảnh hoán đổi được với danh sách ảnh, còn tham chiếu và đầu ra là cố định. Một phép thử chỉ tuyên bố CERTIFIED (a > b) khi phép thử của mọi thành viên bác bỏ ở mức α thì có mức α đối với giả thuyết không dạng hợp ấy, và không cần hiệu chỉnh theo số thành viên. Đây là nguyên lý giao–hợp (Berger, 1982; Berger và Hsu, 1996); bài viết rằng lập luận là của các tác giả ấy và ở đây chỉ được áp dụng. Bảo đảm là danh nghĩa chứ không chính xác: mỗi phép thử theo thành viên là một bootstrap phân vị ở mức một phía 2.5% cho mỗi chiều, và bảo đảm có điều kiện theo các tập tham chiếu và tần suất văn bản của toàn danh sách. Những điều không được bảo đảm, theo nguyên văn bản đăng ký mà bài trích: "front ends outside G; learned metrics; human agreement; anything about another language; the absence of training exposure of the systems (irrelevant to the certificate, which concerns the metric's verdict on given outputs, not system quality)". Chứng nhận bảo thủ theo thiết kế: đòi mọi thành viên đều đạt làm giảm tỉ lệ phép so sánh được chứng nhận, và các hàng NULL-STABLE, FRAGILE ở Mục 6 cho thấy cái giá ấy.

Giữa các phép so sánh, bài không đưa ra khẳng định nào ở mức cả họ phép thử (family-wise). Các số đếm ở Mục 6 là số đếm quyết định theo từng phép so sánh ở mức 2.5% cho mỗi chiều, và, theo câu bài trích, "about 2.5% of comparisons with a true null under some member may be certified in error". Các phép so sánh dùng chung một tệp đầu ra không độc lập. CIDEr-D là độ đo duy nhất mang phán quyết; chứng nhận dưới BLEU-4 và ROUGE-L được tính cùng quy tắc và báo cáo không kèm phán quyết.

**Nhận xét rà soát.** Mục 4 là phần lý thuyết của bài và được viết gọn, đúng với một thủ tục mà phần mới nằm ở cách ráp chứ không ở từng mảnh. Bốn điểm cần làm rõ. (i) Bảo đảm ở Mục 4.4 được phát biểu cho giả thuyết không dạng hợp trên các thành viên, nhưng quy tắc ở Mục 4.3 phát biểu theo lớp; vì các thành viên cùng lớp cho cùng token nên cùng $D_f$, hai cách nói tương đương, và bài nên viết một câu nối để phản biện khỏi hỏi. (ii) Bài nói bảo đảm là danh nghĩa vì dùng bootstrap phân vị, nhưng không nói gì về độ phủ của bootstrap phân vị với kích thước danh sách ảnh nhỏ như 100 hoặc 279 ảnh của hai nhóm chấm lần đầu (Bảng B.32); đây là câu hỏi phản biện dễ gặp. (iii) Quy tắc chấp nhận (a)–(b) do nhóm tác giả đặt, và ba quyết định chấp nhận (giữ các thành viên giữ chữ hoa, loại đơn vị ký tự, giữ các thành viên giữ dấu câu) là của nhóm; bài đã tự nêu ở Mục 8 và cho Table 7 làm phép kiểm độ nhạy, nên giữ liên kết ấy khi cắt. (iv) Câu trích "about 2.5% of comparisons with a true null under some member may be certified in error" là lời của bản đăng ký; nó nói về tỉ lệ sai theo từng phép so sánh, không phải về các số đếm ở Mục 6, và bài nên giữ nó trong ngoặc kép như hiện nay. Về hình thức, Fig. 1 chưa được dựng.

## B.19 Mục 5 của bản thảo viết lại: Thiết kế đã đăng ký và dữ liệu (Registered design and data)

**Nội dung.**

### B.19.1 Đăng ký và các nhãn bằng chứng (Mục 5.1)

Thiết kế được đăng ký trước khi mã phân tích tồn tại và trước khi bất kỳ tệp nào của nhóm khác được chấm. Bản đăng ký và kế hoạch của phần con người được commit vào kho của đề tài ngày 2026-11-12 (commit `9208b39`); mã phân tích theo sau ngày 2026-11-13 (commit `9e6578a`), sau một lượt đọc mã có tự kiểm và kiểm đột biến, và các bước chạy sau commit ấy. Các bản đăng ký được đóng dấu thời gian bằng commit và mã băm của tệp; chúng không được gửi tới một cơ quan đăng ký bên ngoài. Online Resource 1 gom các mã băm, hồ sơ chạy và mọi sai lệch vào một chỗ.

Mỗi con số mang một trong các nhãn bằng chứng của bản đăng ký. DEVELOPMENT: tính trên các tệp đề tài đã chấm trước đó, trên các tham chiếu đã dùng. POST HOC: một con số đã tồn tại trong một tệp lưu trước bản đăng ký, hoặc một hàng thêm sau khi đã nhìn. FIRST SCORING OF RELEASED OUTPUTS: điểm n-gram đầu tiên mà đề tài từng tính trên một tệp đầu ra do nhóm khác công bố; các tham chiếu được dùng có thể đã dùng rồi. HELD-OUT FRONT END: một thành viên của họ chưa từng được đề tài chạy trên đầu ra hệ thống nào trước commit của bản đăng ký. REGISTERED PREDICTION: một quy tắc được cố định trước khi đại lượng nó chi phối tồn tại trong bất kỳ tệp nào. DESCRIPTIVE: báo cáo không kèm phán quyết. CONTROL: đối ứng tiếng Anh, không kèm phán quyết.

### B.19.2 Các tập so sánh (Mục 5.2)

*Các phép so sánh phát triển.* Tập của chính nhóm gồm 73 tệp đầu ra trên tập kiểm tra KTVIC (558 ảnh, 2,790 tham chiếu). Chúng là biến thể của hệ thống của chính nhóm tác giả: một mô hình nền dưới các mục tiêu huấn luyện, hạt giống và lời nhắc khác nhau, thuộc 26 họ hệ thống và ba tầng lời nhắc (33, 35 và 5 tệp). Tập D gồm mọi cặp tệp của nhóm cùng tầng và khác họ, cùng một cặp của hai hệ cơ sở đã công bố của bộ chuẩn; đầu ra của hai hệ cơ sở này được dùng với sự cho phép của tác giả kho mã và chỉ ở dạng thống kê tổng hợp. D có 1101 phép so sánh. Trước khi chấm bất kỳ phép so sánh nào, `f0` tái lập CIDEr-D đã commit của từng tệp trong 67 tệp của nhóm có tệp điểm đã commit, trong dung sai đã đăng ký 0.01 (hiệu lớn nhất 0.0016; DEVELOPMENT); 6 tệp của nhóm không có tệp điểm đã commit. Một lượt kiểm kê các tệp điểm đã lưu (67 của nhóm và 1 tệp khác) không phát hiện lần chạy nào trước đó của đơn vị để dành trên đầu ra hệ thống, nên đơn vị ấy vẫn là để dành.

*Các phép so sánh chấm lần đầu.* Tệp đầu ra của các nhóm khác được lấy từ các kho công khai ở commit đã ghim. Một phép so sánh chỉ được lập trong nội bộ một nhóm tệp, tức giữa các tệp trên cùng danh sách ảnh với cùng tệp tham chiếu. Việc nhận tệp là cơ học và không dùng điểm nào. Một tệp phải phân tích được thành một chú thích cho mỗi mã ảnh (quy tắc 1); phủ ít nhất 95% số mã tham chiếu, với nhiều nhất 5% số dòng nằm trên mã lạ; và có nhiều nhất 1% mã trùng, nhiều nhất 1% chú thích rỗng, nhiều nhất 5% bản sao của một tham chiếu và ít nhất 50% chú thích có dấu tiếng Việt. Hai tệp được nhận lập thành một phép so sánh khi các mã chúng phủ trùng nhau ở ít nhất 95% số mã tham chiếu. Bài công bố rằng các ngưỡng được đặt sau khi các giá trị cấu trúc của một lần tải trước đã được nhìn thấy; không có điểm nào liên quan. Trong 19 tệp qua cổng, 16 được nhận và 3 không đạt quy tắc 1. Tổng cộng 22 phép so sánh được lập, so với mức tối đa đã đăng ký là 32, và 20 trong 22 phép đến từ một kho mã. Hai nhóm có tệp không đạt quy tắc 1 không lập được phép so sánh nào.

*Tình trạng tham chiếu của các nhóm chấm lần đầu.* Với nhóm G1, 578 mã ảnh tham chiếu rơi vào các phần huấn luyện (401), kiểm định (149) và kiểm tra (28) của UIT-ViIC theo cách chia của đề tài, không mã nào nằm ngoài. Với nhóm G3, 924 mã ảnh tham chiếu trùng với tập mã của phần kiểm định UIT-ViIC của đề tài. Đây là các sự kiện về mã ảnh (DESCRIPTIVE); lời văn tham chiếu không được so. Bài viết: "This project used these images before: its log pins the three split files by hash in runs that predate the registration", tức đề tài đã dùng các ảnh này trước đó. Với các nhóm G2 và G4, tham chiếu là tệp của chính kho mã, được mô tả bằng kho, commit và tệp; mã của chúng không được so. Việc hệ thống của các nhóm khác có tiếp xúc dữ liệu khi huấn luyện hay không không phải việc của chứng nhận (Mục 4.4), và bài không rút kết luận nào về điều đó.

**Bảng B.32.** Các tập so sánh (Table 2 của bài; DESCRIPTIVE, chỉ cấu trúc, không có điểm). Bài gọi nguồn bằng tên kho và commit, không gọi tên hệ thống; bảng này thay tên kho bằng số thứ tự.

| Tập hoặc nhóm | Nguồn | Giấy phép | Tệp qua cổng / được nhận | Số ảnh mỗi phép so sánh | Số phép so sánh | Tệp tham chiếu và tình trạng |
|---|---|---|---|---|---|---|
| D, phát triển | 73 tệp của nhóm thuộc 26 họ, ba tầng 33, 35 và 5 tệp; 2 tệp của hai hệ cơ sở đã công bố | của nhóm; hệ cơ sở theo sự cho phép, chỉ tổng hợp | 2 / 2 (các tệp hệ cơ sở) | 558 | 1101 | kiểm tra KTVIC, 2,790 tham chiếu; đề tài đã dùng trước |
| G1 | kho thứ nhất; danh sách UIT-ViIC của kho | MIT | 5 / 5 | 578 | 10 | mã nằm trong các phần UIT-ViIC của đề tài: huấn luyện 401, kiểm định 149, kiểm tra 28; lời văn không được so |
| G2 | cùng kho và commit; tập thể thao của kho | MIT | 5 / 5 | 279 | 10 | tệp của kho; mã không được so |
| G3 | kho thứ hai; UIT-ViIC | không có: chỉ tổng hợp | 2 / 2 | 924 | 1 | tập mã trùng phần kiểm định UIT-ViIC của đề tài (924 mã); lời văn không được so |
| G4 | cùng kho và commit; một tập thể thao từ Flickr | không có: chỉ tổng hợp | 2 / 2 | 100 | 1 | tệp của kho; mã không được so |
| G5 | hai kho khác; UIT-ViIC | MIT; kiểu BSD | 2 / không (quy tắc 1) | – | không lập được | – |
| G6 | một kho khác; kiểm tra KTVIC | không có: chỉ tổng hợp | 1 / không (quy tắc 1) | – | không lập được | – |

### B.19.3 Các bước và thứ tự (Mục 5.3)

Mọi bước chạy đúng một lần, trên một máy thuê, trên CPU, ngày 2026-11-13 (UTC). Mỗi bước là một lệnh con từ chối khởi động nếu thiếu mã băm của đầu vào và dòng nhật ký của bước trước. Thứ tự là: điều kiện tiên quyết và họ; kiểm kê; cổng cấu trúc; các phép so sánh phát triển dưới $F_{dev}$ cùng đối chứng độ nhạy; ghim các kết quả ấy; các phép so sánh chấm lần đầu dưới $F_{dev}$, bước này cố định tập phán quyết của P1; rồi các thành viên để dành trên cả hai tập. Tệp của cổng được ghi nhật ký trước khi có bất kỳ điểm chấm lần đầu nào. Kết quả phát triển và đối chứng được ghim trước khi bất kỳ thành viên để dành nào chạy. Tập phán quyết được ghi nhật ký trước bước để dành. Không bước nào kết thúc bằng FAULT và không bước nào chạy lại. Một bước đăng ký nữa chạy sau đó, một lần, sau khi tệp đầu vào của nó được ghi nhật ký; thiết kế của bước này đang được giữ ngoài văn bản (B.14.1).

### B.19.4 Các dự đoán và quy tắc (Mục 5.4)

P1 hỏi các chứng nhận cấp trên họ phát triển có đứng vững dưới các thành viên để dành hay không. Tập phán quyết $V$ là các phép so sánh được chứng nhận trên $F_{dev}$ có biên chuẩn hoá nhỏ nhất không quá 4, với

$$z_{\min} \;=\; \min_{\text{lớp}}\; \frac{|D_f|}{\mathrm{sd}^{*}(D_f)} \;\le\; 4, \tag{B.11}$$

trong đó $\mathrm{sd}^{*}$ là độ lệch chuẩn bootstrap; nếu có ít hơn 59 phép so sánh sát biên theo nghĩa này thì $V$ là mọi phép so sánh được chứng nhận. Một lần vỡ (break) là một chiều đã được chứng nhận mà không có ý nghĩa dưới ít nhất một lớp để dành. Quy tắc so các cận Clopper–Pearson một phía của tỉ lệ vỡ với một ngưỡng cố định (Clopper và Pearson, 1934; chờ kiểm):

$$r = \frac{\text{số lần vỡ}}{N},\qquad \overline{r}_{95} \le 0.05 \Rightarrow \text{PASS},\qquad \underline{r}_{95} > 0.05 \Rightarrow \text{FAIL},\qquad \text{còn lại} \Rightarrow \text{INCONCLUSIVE}. \tag{B.12}$$

Một đối chứng độ nhạy, tính trên D và được ghim trước khi bất kỳ thành viên để dành nào chạy, áp cùng quy tắc với các thành viên âm tiết làm họ cấp chứng nhận và hai đơn vị phát triển còn lại làm họ phá vỡ. P2 đếm, trong các phép so sánh chấm lần đầu có ý nghĩa dưới `f0`, những phép CHANGED trên $F$. Trong các cổng dừng đã đăng ký được báo cáo ở văn bản này, có một cổng kích hoạt: cổng độ nhạy, gắn một nhãn thứ hai cho P1. Về phần con người, bài viết: "No gate of the human arm fired; its agreement rule placed both hypotheses in the band that is reported without labels".

**Bảng B.33.** Các quy tắc đã đăng ký và nhãn của chúng (Table 3 của bài; REGISTERED PREDICTION; nhãn của đối chứng độ nhạy tính trên dữ liệu DEVELOPMENT). Bài ghi rằng mọi hàng có cùng dạng dù nhãn rơi theo hướng nào.

| Dự đoán | Đại lượng ước lượng | Quy tắc đã đăng ký | Nhãn |
|---|---|---|---|
| P1, kiểm dưới khâu xử lý để dành | r = số lần vỡ / N, với N là cỡ của tập phán quyết V | N < 59: "NOT_EVALUABLE". Cận trên Clopper–Pearson một phía 95% ≤ 0.05: "PASS". Cận dưới > 0.05: "FAIL". Còn lại: "INCONCLUSIVE". Đối chứng độ nhạy $r_{NC}$ ≤ 0.05: P1 mang thêm "LOW-SENSITIVITY" | "INCONCLUSIVE"; "LOW-SENSITIVITY" (Mục 6.3) |
| P2, số kết luận thay đổi trên đầu ra của nhóm khác | $k_{FL}$ trong $n_{FL}$: $n_{FL}$ = số phép so sánh chấm lần đầu có ý nghĩa dưới `f0`; $k_{FL}$ = số phép CHANGED trên F | $n_{FL}$ < 10: "NOT_EVALUABLE". $k_{FL}$ ≥ 3 và $k_{FL}/n_{FL}$ ≥ 0.10: "SUPPORTED". Còn lại: "NOT SUPPORTED" | "NOT SUPPORTED" (Mục 6.4) |
| H-P, tầng dấu câu của phần con người | $q_P$ = tỉ lệ cặp quyết định mà chú thích được ưa là chú thích xếp cao hơn khi bỏ dấu câu | phép thử nhị thức chính xác, một phía, so với 0.5, Holm trên hai phép thử. Bị bác bỏ: "SUPPORTED". Không bị bác bỏ với ít nhất 47 cặp quyết định: "NOT SUPPORTED". Không bị bác bỏ với ít hơn: "UNDERPOWERED" | "no label: low inter-rater agreement (Section 6.7)" |
| H-U, tầng đơn vị của phần con người | $q_U$ = tỉ lệ cặp quyết định mà chú thích được ưa là chú thích xếp cao hơn dưới đơn vị từ | phép thử nhị thức chính xác, hai phía, so với 0.5, Holm trên hai phép thử. Bị bác bỏ: "WORD AGREES MORE" hoặc "SYLLABLE AGREES MORE". Nếu không, khoảng Clopper–Pearson 90% nằm trong 0.40 đến 0.60: "EQUIVALENT within ±0.10". Còn lại: "INCONCLUSIVE" | "no label: low inter-rater agreement (Section 6.7)" |

Cột nhãn của hai hàng cuối là điều cần đọc kỹ: các từ nhãn ở cột quy tắc (SUPPORTED, NOT SUPPORTED, UNDERPOWERED, WORD AGREES MORE, SYLLABLE AGREES MORE, EQUIVALENT, INCONCLUSIVE) là các khả năng mà quy tắc đã định sẵn; không từ nào trong số đó được gắn cho H-P hay H-U, vì quy tắc về đồng thuận (B.19.5) đã đặt cả hai giả thuyết vào dải báo cáo không kèm nhãn.

### B.19.5 Thiết kế phần đánh giá của con người (Mục 5.5)

Chứng nhận nói một phép so sánh có đứng vững qua mọi khâu xử lý chấp nhận được hay không. Nó không nói khâu xử lý nào khớp với con người khi các khâu xử lý bất đồng, và phần con người lấy mẫu đúng các trường hợp ấy. Một mục chấm là một ảnh kiểm tra KTVIC cùng hai chú thích do hai hệ thống của chính nhóm viết (33 tệp lời nhắc ngắn); không tệp nào của nhóm khác được cho người chấm xem. Ba tầng được rút với hạn ngạch và hạt giống cố định: 100 cặp lật theo dấu câu, là các cặp mà thứ tự CIDEr-D theo ảnh khác nhau giữa giữ dấu câu và bỏ dấu câu, với đơn vị cố định là từ; 160 cặp lật theo đơn vị, là các cặp mà thứ tự khác nhau giữa âm tiết và từ, với dấu câu đã bỏ; và 40 cặp đối chứng, ở đó ba thành viên được dùng cho cùng thứ tự. Một sự khác biệt chỉ được tính khi biên trên ảnh đạt 10.0 điểm. Thêm 30 cặp được cho xem lần thứ hai với hai bên đổi chỗ, làm các lần lặp ẩn. Hai người chấm đánh giá mọi cặp một cách độc lập và chọn chú thích A, chú thích B, hoà, hoặc "cannot judge".

Hai chú thích được hiển thị sau một bước chuẩn hoá hiển thị, bỏ dấu câu cuối và viết hoa chữ đầu, để những dấu mà thành viên dấu câu chấm không làm lộ tầng hay loại hệ thống; bài nói rõ các dấu hiệu còn sót lại (độ dài, từ vựng, dấu phẩy bên trong, phong cách của bộ chuẩn ở đầu ra tinh chỉnh). Mã câu hỏi là mã băm có muối, để người chấm không thể suy ra hệ thống hay lần lặp từ trang. Một cặp là quyết định (decisive) khi cả hai người chấm ưa cùng một chú thích, và hai giả thuyết của Bảng B.33 được kiểm trên các cặp quyết định với hiệu chỉnh Holm (Holm, 1979; chờ kiểm):

$$q_P = \frac{k_P}{n_P},\qquad q_U = \frac{k_U}{n_U}, \tag{B.13}$$

với $n_P$, $n_U$ là số cặp quyết định của tầng dấu câu và tầng đơn vị, còn $k_P$, $k_U$ là số cặp trong đó mà chú thích được ưa là chú thích xếp cao hơn khi bỏ dấu câu, tương ứng dưới đơn vị từ.

Đồng thuận được đo bằng κ của Cohen trên danh tính chú thích (Cohen, 1960; chờ kiểm), và quy tắc đọc ba dải: từ 0.40 trở lên, hai giả thuyết mang nhãn; từ 0.20 đến dưới 0.40, chúng được báo cáo không kèm nhãn; dưới 0.20, phần con người là "NOT_EVALUABLE".

Về người chấm, bài in câu đã đăng ký: "One rater is an author (the PI), who knows the study's hypotheses but could not see which system or front end produced a caption." Nghĩa là: một người chấm là tác giả (nhà nghiên cứu chính), người biết các giả thuyết của nghiên cứu nhưng không thể thấy hệ thống nào hay khâu xử lý nào tạo ra một chú thích. Người chấm thứ hai không phải tác giả. Các đánh giá là đánh giá mới của con người trên các chú thích đã được phân tích trước đó, được đăng ký trước khi có bất kỳ đánh giá nào.

Như đã dựng, có 165 ảnh kiểm tra đủ điều kiện cho tầng dấu câu, 266 cho tầng đơn vị và 558 cho tầng đối chứng; sau khi để riêng các ảnh đã rút cho tầng trước, còn 215 ảnh cho tầng đơn vị và 298 cho tầng đối chứng. Mọi hạn ngạch đều đạt (100, 160 và 40 cặp; không tầng nào thiếu), cho 300 cặp chính và, cùng 30 lần lặp, 330 màn hình. 8 màn hình luyện tập của kế hoạch đã được dựng. Ngay tại đây bài in công bố về vòng luyện tập: "In a departure from the registered procedure, neither rater took the eight-pair practice round: both answered on the main page, where the instructions panel starts closed; the registered analysis uses all answers unchanged." Nghĩa là: lệch khỏi quy trình đã đăng ký, không người chấm nào làm vòng luyện tập tám cặp; cả hai trả lời trên trang chính, nơi khung hướng dẫn ban đầu ở trạng thái đóng; phép phân tích đã đăng ký dùng mọi câu trả lời, không đổi gì. Các sai lệch khác so với quy trình đã đăng ký được nêu ở Mục 6.7 (B.21.1).

**Nhận xét rà soát.** Mục 5 đầy đủ về thứ tự và về cái gì được cố định trước cái gì; đây là chỗ bài đứng vững nhất trước câu hỏi về rò rỉ thông tin. Các điểm cần xem lại như sau. (i) Mục 5.3 viết mọi bước chạy ngày 2026-11-13 trên một máy thuê, trong khi phép phân tích phần con người chạy ngày 2026-11-15 trên một máy thuê khác (Mục 6.7 và Table E5 của Online Resource 1); Mục 5.3 nên có một câu nói rõ phép phân tích phần con người là một bước riêng, chạy sau khi phần chấm đóng. (ii) Các ngưỡng của cổng cấu trúc được đặt sau khi đã nhìn giá trị cấu trúc của một lần tải trước; bài công bố điều này, và phản biện có thể hỏi các ngưỡng có được chọn để giữ hay loại một tệp cụ thể không. Table E1 cho thấy mọi tệp được nhận đều cách xa ngưỡng và ba tệp bị loại đều do quy tắc 1, nên có thể dẫn bảng ấy làm câu trả lời. (iii) Tập chấm lần đầu nhỏ và tập trung: 20 trong 22 phép so sánh từ một kho, và hai nhóm trong số đó dùng danh sách chỉ 100 và 279 ảnh. (iv) Với G1 và G3, ảnh thuộc các phần UIT-ViIC mà đề tài đã dùng trước; bài nói rõ đây là sự kiện về mã ảnh và lời văn tham chiếu không được so. Câu "This project used these images before" là một khẳng định về việc dùng trước của chính đề tài, không phải về sự trùng lặp nội dung, và không nên được viết lại thành điều gì mạnh hơn hay yếu hơn. (v) Ở Mục 5.5, cách đếm ảnh đủ điều kiện có thể gây hiểu lầm: 266 ảnh đủ điều kiện cho tầng đơn vị nhưng chỉ còn 215 sau khi để riêng ảnh của tầng trước, và Table 6 chỉ in 266; nên in cả hai con số trong bảng hoặc chú thích bảng. (vi) Câu về người chấm là tác giả chứa cụm "(the PI)", một cách gọi nội bộ; nếu muốn đổi thành vị trí tác giả thì chỉ được đổi khi điều đó đúng, vì đây là câu đã đăng ký. (vii) Bài chưa nói người chấm thứ hai là ai theo vai trò (trình độ tiếng Việt, quan hệ với nhóm), ngoài việc không phải tác giả; phản biện của một phần đánh giá của con người gần như chắc chắn sẽ hỏi. (viii) Khung P3 và P4 đang giữ ngoài văn bản để lại ba chỗ neo trong mục này; bản nộp không thể còn các chỗ neo ấy.

## B.20 Mục 6.1 đến 6.6 của bản thảo viết lại: Kết quả của các bước tính trên máy (Results)

**Nội dung.**

### B.20.1 Họ và điều kiện tiên quyết (Mục 6.1)

Mọi đơn vị từ đều qua điều kiện tiên quyết. Mỗi bộ trong ba bộ tách từ trả về đầu ra thẳng hàng và không rỗng cho cả 2,790 tham chiếu kiểm tra KTVIC; không phát hiện chuỗi hỏng nào, so với cận đã đăng ký 0.5%, và không có lần nào phải lùi về tách theo khoảng trắng. Không đơn vị nào bị loại, và họ được hiện thực đúng như đăng ký: 54 thành viên phát triển, 18 thành viên để dành, 72 tất cả (DESCRIPTIVE). Trên 9 chuỗi thử đã đăng ký, vốn không phải văn bản của bộ dữ liệu, RDRSegmenter và underthesea mỗi bộ trả về cùng token cho hai cách đặt dấu thanh ở 9 trong 9 trường hợp; dưới pyvi, token bằng nhau không được phát hiện trên các chuỗi này (0 trong 9). Vậy hai bộ tách từ ấy tự viết lại vị trí dấu thanh, và các mức dấu thanh có thể rơi vào cùng một lớp dưới chúng. Việc các thành viên có rơi vào cùng lớp ở một phép so sánh cụ thể hay không được đo bằng sự đồng nhất token, không được giả định.

### B.20.2 Các phép so sánh phát triển (Mục 6.2)

Trong 1101 phép so sánh phát triển, 909 là CERTIFIED trên họ phát triển và 908 trên họ đầy đủ; 59 và 62 là FRAGILE, trong đó 2 là REVERSED ở cả hai trường hợp; 133 và 131 là NULL-STABLE (DEVELOPMENT). Trong 936 phép so sánh có ý nghĩa dưới `f0`, 27 là CHANGED trên họ phát triển (tỉ lệ 0.0288) và 28 trên họ đầy đủ (0.0299). Lật dấu điểm ước lượng xảy ra ở 58 và 65 phép so sánh. Bài nhắc rằng các số đếm này mô tả biến thể của hệ thống của chính nhóm trên các tham chiếu đã dùng; cặp hai hệ cơ sở đã công bố là một trong 1101 phép và không được báo cáo riêng; và đây là số đếm quyết định theo từng phép so sánh, trong khi các phép so sánh dùng chung tệp.

**Bảng B.34.** Số đếm chứng nhận dưới CIDEr-D (Table 4 của bài). FRAGILE bao gồm REVERSED. Các hàng trên D là DEVELOPMENT; các hàng trên tập chấm lần đầu (FL) là FIRST SCORING OF RELEASED OUTPUTS; các hàng trên F gồm cả các thành viên HELD-OUT FRONT END. "not detected" thay cho số đếm 0 trong tập ấy. Phần dưới: số đếm của P2 theo kho và khi bỏ từng kho (kho 1 = các nhóm G1 và G2; kho 2 = các nhóm G3 và G4).

| Tập, họ | Số phép so sánh | CERTIFIED | FRAGILE | trong đó REVERSED | NULL-STABLE | Có ý nghĩa dưới `f0` | CHANGED | Tỉ lệ CHANGED | Lật dấu điểm ước lượng |
|---|---|---|---|---|---|---|---|---|---|
| D trên $F_{dev}$ | 1101 | 909 | 59 | 2 | 133 | 936 | 27 | 0.0288 | 58 |
| D trên F | 1101 | 908 | 62 | 2 | 131 | 936 | 28 | 0.0299 | 65 |
| FL trên $F_{dev}$ | 22 | 9 | 6 | not detected | 7 | 10 | 1 | 0.1000 | 3 |
| FL trên F | 22 | 8 | 8 | not detected | 6 | 10 | 2 | 0.2000 | 3 |
| P2, kho 1 | | | | | | 9 | 2 | | |
| P2, kho 2 | | | | | | 1 | not detected | | |
| P2, mọi kho trừ kho 1 | | | | | | 1 | not detected | | |
| P2, mọi kho trừ kho 2 | | | | | | 9 | 2 | | |

### B.20.3 Phép kiểm dưới khâu xử lý để dành, P1 (Mục 6.3)

Tập phán quyết được cố định chỉ từ điểm của họ phát triển và được ghi nhật ký trước khi bất kỳ thành viên để dành nào chạy. Trong 1123 phép so sánh của cả hai tập, 918 được chứng nhận trên họ phát triển (909 phát triển, 9 chấm lần đầu), và 72 trong số đó là sát biên ($z_{\min}$ ≤ 4). Vì 72 không nhỏ hơn 59, $V$ là tập sát biên: N = 72, gồm 68 phép so sánh phát triển và 4 phép chấm lần đầu (DESCRIPTIVE).

Phán quyết đã đăng ký là "INCONCLUSIVE". Trong 72 chứng nhận sát biên, 2 chứng nhận vỡ dưới các khâu xử lý để dành: r = 0.028, cận trên Clopper–Pearson một phía 95% là 0.085 và cận dưới là 0.005. Theo quy tắc (B.12), "PASS" cần cận trên không quá 0.05 và "FAIL" cần cận dưới lớn hơn 0.05; không điều nào xảy ra. Nói bằng lời: số lần vỡ quan sát được ít, nhưng với 72 chứng nhận thì cận trên của tỉ lệ vỡ vẫn vượt ngưỡng 0.05, nên dữ liệu không đủ để nói các chứng nhận đứng vững, và cũng không cho thấy chúng không đứng vững. Bài thêm rằng các phép so sánh dùng chung tệp nên không độc lập, và cận Clopper–Pearson chỉ là một tóm tắt danh nghĩa.

P1 còn mang nhãn đăng ký "LOW-SENSITIVITY" (quy tắc $r_{NC} \le 0.05$): họ âm tiết bị các đơn vị phát triển khác làm vỡ ở 6 trong 915 chứng nhận của nó ($r_{NC}$ = 0.0066); chỉ 54 chứng nhận là sát biên, ít hơn 59, nên phương án dự phòng đã đăng ký dùng toàn bộ. Nhãn này có nghĩa là một phép kiểm cùng loại, dựng từ các đơn vị đã biết, hầu như không làm vỡ chứng nhận nào; nó được đăng ký để đo, trước khi bất kỳ thành viên để dành nào chạy, liệu phép kiểm để dành có khả năng không đạt hay không. Bản đăng ký gắn cho nhãn này một câu giả định tập sát biên: "a one-unit family was broken by the other development units in at most 5% of its near-margin certificates, so the held-out check had little room to fail". Bài trích câu này để lưu hồ sơ và nói rõ: phương án dự phòng đã thay tập sát biên, nên câu ấy không mô tả tập đã được dùng, và nó không được khẳng định như một phát hiện. Một hàng POST HOC đứng cạnh nhãn vì lý do đó: cả 6 lần vỡ đều nằm trong 54 chứng nhận sát biên; hàng này không làm đổi nhãn nào.

**Bảng B.35.** Phép kiểm dưới khâu xử lý để dành (Table 5 của bài). Các hàng trên thành viên để dành là HELD-OUT FRONT END; đối chứng độ nhạy là DEVELOPMENT; các hàng không có phán quyết được ghi rõ. Các cận là cận Clopper–Pearson một phía 95% và là danh nghĩa vì các phép so sánh dùng chung tệp.

| Hạng mục | Giá trị | Nhãn hoặc tình trạng |
|---|---|---|
| Được chứng nhận trên $F_{dev}$, cả hai tập | 918 (909 phát triển, 9 chấm lần đầu) | DEVELOPMENT; FIRST SCORING OF RELEASED OUTPUTS |
| Sát biên ($z_{\min}$ ≤ 4) trong số đó | 72; không nhỏ hơn 59, nên V là tập sát biên | DESCRIPTIVE |
| Tập phán quyết V | N = 72 (68 phát triển, 4 chấm lần đầu) | cố định trên $F_{dev}$ trước bước để dành |
| Số lần vỡ trong V | 2 (1 trong 68 phát triển, 1 trong 4 chấm lần đầu) | HELD-OUT FRONT END; hai phần là DESCRIPTIVE |
| r, kèm các cận | 0.028; trên 0.085, dưới 0.005 | REGISTERED PREDICTION: "INCONCLUSIVE" |
| Đảo chiều trong V | not detected | HELD-OUT FRONT END |
| Đối chứng độ nhạy: chứng nhận âm tiết trên D | 915; 54 sát biên, ít hơn 59, nên phương án dự phòng dùng cả 915 | DEVELOPMENT |
| Đối chứng độ nhạy: số lần vỡ dưới các đơn vị phát triển khác | 6; $r_{NC}$ = 0.0066, quy tắc $r_{NC}$ ≤ 0.05 | "LOW-SENSITIVITY", gắn vào P1 |
| Các lần vỡ ấy rơi vào đâu | cả 6 nằm trong 54 chứng nhận sát biên | POST HOC; không làm đổi nhãn nào |
| Hàng chấm lần đầu | 1 trong 9; các cận 0.006 và 0.429 | FIRST SCORING OF RELEASED OUTPUTS; không có phán quyết |
| Mọi chứng nhận trên $F_{dev}$ | 2 trong 918: 1 trong 909 phát triển, 1 trong 9 chấm lần đầu | HELD-OUT FRONT END; không có phán quyết |
| Khi thêm đơn vị ký tự vào họ để dành | 16 lần vỡ và 3 lần đảo chiều trong 72 | DESCRIPTIVE; đơn vị ký tự không chấp nhận được |

Về các hàng đứng cạnh nhãn: trong 9 phép so sánh chấm lần đầu được chứng nhận trên họ phát triển, 1 phép vỡ (các cận 0.006 và 0.429); cận dưới không vượt 0.05 nên bản đăng ký không yêu cầu phát biểu nào cạnh nhãn P1. Họ để dành chỉ có một đơn vị, nên tỉ lệ cho đơn vị để dành bằng r. Không phát hiện lần đảo chiều nào.

### B.20.4 Lần chấm đầu tiên các đầu ra do nhóm khác công bố, P2 (Mục 6.4)

Tập chấm lần đầu là lần chấm đầu tiên các đầu ra do nhóm khác công bố; tham chiếu của nó là tệp tham chiếu của các nhóm ở Bảng B.32, với các trùng mã đã nêu. Trong 22 phép so sánh, 9 là CERTIFIED trên họ phát triển và 8 trên họ đầy đủ; 6 và 8 là FRAGILE; không phát hiện phép REVERSED nào trong tập này; 7 và 6 là NULL-STABLE.

Phán quyết đã đăng ký của P2 là "NOT SUPPORTED". Trong 22 phép so sánh, 10 có ý nghĩa dưới `f0`, vừa đạt mức tối thiểu đã đăng ký là 10, và 2 trong số này là CHANGED trên họ đầy đủ (tỉ lệ 0.2000). Quy tắc đòi ít nhất 3 phép CHANGED và tỉ lệ ít nhất 0.10; điều kiện về tỉ lệ đạt, điều kiện về số đếm không đạt. Lời đã đăng ký cho nhãn này là: "the certificate changed few conclusions in this pool (2 of 10)". Theo kho, các số đếm là 2 trong 9 và 0 trong 1; khi lần lượt bỏ từng kho, chúng là 0 trong 1 và 2 trong 9. Riêng trên họ phát triển, 1 trong 10 là CHANGED (0.1000). Phán quyết được báo cáo dưới dạng số đếm theo kho, và hệ thống không được gọi tên.

Với nhãn này, bản đăng ký nói phương pháp khi đó được trình bày "as a cheap check whose usual answer is CERTIFIED, with the counts". Bài chỉ in mệnh đề ấy trong một phạm vi: trong các phép so sánh có ý nghĩa dưới `f0`, 8 trong 10 (FL) và 908 trong 936 (D, DEVELOPMENT) là CERTIFIED trên F. Trên toàn bộ 22 phép so sánh chấm lần đầu, CERTIFIED không phải câu trả lời thường gặp: 8 là CERTIFIED, 8 FRAGILE và 6 NULL-STABLE. Fig. 2 và Table E2 cho tập phá vỡ của các phép FRAGILE theo mức của từng trục; mọi mức của mọi trục đều xuất hiện trong tập phá vỡ của cả hai tập, và bài lưu ý các số đếm không so được giữa các trục, vì một trục có ít mức hơn dồn cùng số thành viên vào ít ô hơn.

### B.20.5 Các hàng phụ và đối chứng (Mục 6.5)

Không hàng nào ở Bảng B.36 mang phán quyết; tất cả là DESCRIPTIVE và tính trên cả hai tập gộp lại (1123 phép so sánh). Về biên dưới một thành viên: bản đăng ký hỏi biên dưới riêng `f0` dự báo CHANGED tốt đến đâu. Theo chiều đã mã hoá, diện tích dưới đường cong là xác suất để một phép CHANGED có biên chuẩn hoá dưới `f0` nhỏ hơn một phép không CHANGED, hoà tính một nửa: 0.8012 (30 phép CHANGED, 1093 phép không). Bản đăng ký không nêu chiều; chiều đã mã hoá được dùng. Một hàng thứ hai, thêm vào và không đăng ký, chỉ giữ 946 phép so sánh có ý nghĩa dưới `f0`: 0.9546.

Về các độ đo khác: với cùng quy tắc, 862 trong 1123 phép so sánh là CERTIFIED trên F dưới BLEU-4 và 891 dưới ROUGE-L; tỉ lệ CHANGED là 0.0517 (47 trong 909) và 0.0814 (79 trong 970). Khoảng của BLEU-4 lấy mẫu lại số đếm n-gram theo ảnh, một cách đọc đã được quyết định trước khi chạy. Về các quyết định chấp nhận: không có các thành viên giữ chữ hoa, 919 phép là CERTIFIED và 27 trong 946 là CHANGED (0.0285). Khi thêm đơn vị ký tự, 893 là CERTIFIED và 53 trong 946 là CHANGED (0.0560); đơn vị ký tự không chấp nhận được, nên hàng này cho thấy việc loại nó làm đổi điều gì. Không có các thành viên giữ dấu câu, 925 là CERTIFIED; `f0` giữ dấu câu và không thuộc họ ấy, nên ba ô phụ thuộc `f0` không xác định. Về đối chứng tiếng Anh, bài in: "CONTROL: NOT RUN". Không tệp đầu ra tiếng Anh nào được nêu tên ở lượt đọc mã, và hệ quả đã đăng ký được áp dụng: "No claim beyond Vietnamese is made from it".

**Bảng B.36.** Các hàng phụ và đối chứng trên cả hai tập gộp lại, 1123 phép so sánh (Table 7 của bài; DESCRIPTIVE; không có phán quyết). "not detected" thay cho số đếm 0.

| Hàng | Số phép so sánh | CERTIFIED | FRAGILE | trong đó REVERSED | NULL-STABLE | Có ý nghĩa dưới `f0` | CHANGED | Tỉ lệ CHANGED | Lật dấu điểm ước lượng |
|---|---|---|---|---|---|---|---|---|---|
| BLEU-4 trên F | 1123 | 862 | 120 | 20 | 141 | 909 | 47 | 0.0517 | 118 |
| ROUGE-L trên F | 1123 | 891 | 122 | 16 | 110 | 970 | 79 | 0.0814 | 94 |
| CIDEr-D, F không có thành viên giữ chữ hoa | 1123 | 919 | 63 | not detected | 141 | 946 | 27 | 0.0285 | 51 |
| CIDEr-D, F thêm đơn vị ký tự (không chấp nhận được) | 1123 | 893 | 119 | 4 | 111 | 946 | 53 | 0.0560 | 104 |
| CIDEr-D, F không có thành viên giữ dấu câu | 1123 | 925 | 53 | not detected | 145 | không xác định (`f0` không là thành viên) | không xác định | không xác định | 63 |

### B.20.6 Mục 6.6 của bài

Mục 6.6 ("Reproduction of published scores") vắng mặt ở trạng thái mặc định: bài chỉ để một chỗ neo, còn nội dung và bảng của nó được giữ ngoài văn bản cho tới khi nhà nghiên cứu chính quyết định (B.14.1). Phần báo cáo này vì thế không thuật lại kết quả nào của mục ấy.

**Nhận xét rà soát.** Phần kết quả trên máy được in đúng kỷ luật: mỗi nhãn đi kèm quy tắc, số đếm và các hàng không có phán quyết; hàng POST HOC không bị dùng để đổi nhãn. Các điểm cần xem lại. (i) Về P1, ba cách hiểu sai dễ xảy ra và bài cần chặn cả ba: "INCONCLUSIVE" không phải là "đạt" dù chỉ có 2 lần vỡ; "LOW-SENSITIVITY" không phải một kết quả xấu về FE-CERT mà là lời cảnh báo rằng phép kiểm để dành khó có thể không đạt; và hàng POST HOC "cả 6 lần vỡ nằm trong 54 chứng nhận sát biên" không phục hồi câu đăng ký. Bản thảo hiện viết đúng cả ba; khi cắt cần giữ đủ. (ii) Về P2, $n_{FL}$ = 10 đúng bằng mức tối thiểu; nếu chỉ thiếu một phép so sánh có ý nghĩa dưới `f0` thì nhãn đã là "NOT_EVALUABLE". Phản biện sẽ lưu ý độ mong manh này, và 9 trong 10 phép đến từ một kho. Câu "the certificate changed few conclusions in this pool (2 of 10)" là lời đăng ký; tỉ lệ 0.2000 nghe không "ít", nên bài cần giữ câu trong ngoặc kép và giữ giải thích rằng điều kiện không đạt là điều kiện về số đếm. (iii) Số 946 (số phép có ý nghĩa dưới `f0` trên cả hai tập) bằng 936 của D cộng 10 của FL theo Bảng B.34; còn hàng BLEU-4 và ROUGE-L có số phép có ý nghĩa dưới `f0` khác (909 và 970) vì đó là độ đo khác. Con số 909 xuất hiện ở hai nghĩa (số chứng nhận phát triển dưới CIDEr-D và số phép có ý nghĩa dưới `f0` theo BLEU-4); nên có một ghi chú để người đọc khỏi nhầm. (iv) Diện tích dưới đường cong 0.8012 được tính theo một chiều mà bản đăng ký không nêu; bài công bố điều đó và thêm một hàng không đăng ký (0.9546); cả hai phải giữ nhãn DESCRIPTIVE và nhãn "extra". (v) Đối chứng tiếng Anh "NOT RUN" nghĩa là bài không có phần đối chiếu với dữ liệu tiếng Anh; đây vẫn là điểm nhà nghiên cứu cần quyết định, vì định hướng chung của đề tài muốn mỗi bài có đối chiếu ấy. (vi) Table E2 ghi rằng các số đếm trên F là giá trị của mã và không tính lại được từ các thống kê đã lưu; giới hạn này cũng áp cho số lần vỡ của P1 và số CHANGED trên F (B.25.1), và nên được nhắc ở Mục 8 như hiện nay. (vii) Fig. 2 chưa dựng.

## B.21 Mục 6.7 của bản thảo viết lại: Ưu tiên của con người (Human preferences)

**Nội dung.** Điều cần nắm trước hết: phần đánh giá của con người đã chạy đúng như đăng ký với hai người chấm, nhưng mức đồng thuận giữa hai người chấm thấp, nên theo quy tắc cố định từ trước, hai giả thuyết của nó (H-P và H-U) không nhận nhãn nào. Bài in các tỉ lệ, các phép thử và mọi đại lượng về đồng thuận, nói rõ rằng không nhãn nào được gắn, và công bố đầy đủ cách phiên chấm đã diễn ra, kể cả những chỗ lệch khỏi quy trình đã đăng ký. Kết quả này không làm đổi họ F, không làm đổi chứng nhận nào và không làm đổi nhãn P1 hay P2.

### B.21.1 Cách phần chấm đã diễn ra và các công bố (đoạn mở của Mục 6.7)

Bài mở mục bằng cách gọi đúng tên loại bằng chứng: các đánh giá là "new human judgements on previously analysed captions", được đăng ký trước khi có bất kỳ đánh giá nào. Hai người chấm đánh giá toàn bộ 300 cặp chính và 30 lần lặp ẩn. Sau đó là một chuỗi công bố, mỗi câu được in nguyên văn trong bài; dưới đây chép từng câu tiếng Anh kèm nghĩa tiếng Việt.

1. *Người chấm là tác giả.* "One rater is an author (the PI), who knows the study's hypotheses but could not see which system or front end produced a caption." Một người chấm là tác giả (nhà nghiên cứu chính), người biết các giả thuyết của nghiên cứu nhưng không thể thấy hệ thống nào hay khâu xử lý nào tạo ra một chú thích. Người chấm thứ hai không phải tác giả.
2. *Vòng luyện tập.* "In a departure from the registered procedure, neither rater took the eight-pair practice round: both answered on the main page, where the instructions panel starts closed; the registered analysis uses all answers unchanged." Lệch khỏi quy trình đã đăng ký, không người chấm nào làm vòng luyện tập tám cặp: cả hai trả lời trên trang chính, nơi khung hướng dẫn ban đầu ở trạng thái đóng; phép phân tích đã đăng ký dùng mọi câu trả lời, không đổi gì.
3. *Phiên của người chấm thứ hai.* "The second rater answered in person on an author's laptop, on the same rating page and instructions; a key-protected remote link had been prepared and opened but no answer was saved through it. During the session the author passed on one request to pause and one to continue, and said nothing about the items. That this rater worked alone, without the author watching or explaining and without search or AI tools, rests on the statement of the author; no third party observed the session, and the rating server keeps no record of the answering client." Người chấm thứ hai trả lời trực tiếp trên máy tính xách tay của một tác giả, trên cùng trang chấm và cùng hướng dẫn; một đường dẫn từ xa có khoá bảo vệ đã được chuẩn bị và đã được mở, nhưng không câu trả lời nào được lưu qua đường dẫn ấy. Trong phiên chấm, tác giả chuyển lời một yêu cầu tạm dừng và một yêu cầu tiếp tục, và không nói gì về các mục chấm. Việc người chấm này làm việc một mình, không có tác giả nhìn hay giải thích, và không dùng công cụ tìm kiếm hay công cụ AI, dựa trên lời khẳng định của tác giả; không bên thứ ba nào quan sát phiên chấm, và máy chủ của trang chấm không lưu bản ghi nào về máy khách đã trả lời.
4. *Trang chấm bị lộ trước khi chấm.* "Before the second rater began, that rater's rating page was reachable for about 27 minutes at a public address without the access key, opened by another software tool on the laptop; no answer existed at that time, and it is not known whether anyone opened the page." Trước khi người chấm thứ hai bắt đầu, trang chấm của người này có thể truy cập được trong khoảng 27 phút tại một địa chỉ công khai mà không cần khoá truy cập, do một công cụ phần mềm khác trên máy mở ra; khi đó chưa có câu trả lời nào, và không biết có ai đã mở trang hay không.
5. *Đóng phần chấm và chạy phân tích.* Phần chấm được đóng ngày 2026-11-15 lúc 08:08:59Z (UTC), trước thời hạn muộn nhất đã đăng ký, sau khi cả hai người chấm nói đã xong; phép phân tích đã đăng ký của phần con người sau đó chạy một lần, trên một máy thuê, trên CPU. Bài viết: "No sensitivity analysis exists", tức không có phép phân tích độ nhạy nào.
6. *Dấu hiệu còn sót.* Bước chuẩn hoá hiển thị để lại các dấu hiệu còn sót đã nêu ở Mục 5.5.
7. *Điều phần này không ước lượng.* Phần con người không ước lượng hệ thống nào tốt hơn, không ước lượng thứ tự ở mức hệ thống, không nói về tính hợp lệ của CIDEr-D nói chung, không nói gì về các thành viên ngoài ba thành viên nó dùng, và không nói gì về ngôn ngữ khác.
8. *Phạm vi tác động.* Kết quả của con người "never changes F, a certificate, a P1 to P3 label or the P4 method check"; nó chỉ quyết định thành viên nào được khuyến nghị để báo cáo (Mục 7).
9. *Giữ kín kết quả với người chấm là tác giả.* "Under the project's custody rule, the results of the other stages were withheld from the author rater until the labelling was closed; the project log records no disclosure to him before that." Theo quy tắc giữ kín của đề tài, kết quả của các bước khác được giữ không cho người chấm là tác giả biết cho tới khi phần chấm đóng; nhật ký của đề tài không ghi nhận lần tiết lộ nào cho người này trước thời điểm đó.

### B.21.2 Kết quả chính và Table 6

Đoạn kết quả mở bằng đoạn văn đã chép nguyên văn ở B.15, rồi thêm các số đếm. Cả hai người chấm trả lời toàn bộ 300 cặp chính, và không ai dùng lựa chọn "cannot judge". Số cặp quyết định là 129. 171 cặp còn lại không quyết định: ở 128 cặp có ít nhất một người chấm chọn hoà, và ở 43 cặp hai người chấm ưa hai chú thích khác nhau; không thiếu câu trả lời nào. Các tỉ lệ được báo cáo bất kể nhãn. Ở các cặp đối chứng, bài viết: "On control pairs, which all three members order the same way, both raters chose the caption the metric ranks higher in 20 of 26 decisive pairs (0.769; 0.564 to 0.910)", tức ở các cặp mà cả ba thành viên xếp cùng thứ tự, cả hai người chấm chọn chú thích mà độ đo xếp cao hơn ở 20 trong 26 cặp quyết định. Ở tầng đơn vị, tỉ lệ nghiêng về âm tiết là 0.507.

Hai sự kiện về cỡ mẫu được đặt cạnh các tỉ lệ, và bài nói rõ chúng không phải nhãn: 28 cặp quyết định của tầng dấu câu ít hơn 47 cặp mà bản đăng ký đã tính cho công suất 80% tại tỉ lệ thật 0.70; và 75 cặp quyết định của tầng đơn vị ít hơn khoảng 215 cặp mà nó đã tính cho một kết luận tương đương.

**Bảng B.37.** Phần đánh giá của con người (Table 6 của bài; đánh giá mới của con người trên các chú thích đã được phân tích trước đó). Một cặp "khớp" khi chú thích được ưa là chú thích xếp cao hơn khi bỏ dấu câu (tầng dấu câu), dưới đơn vị từ (tầng đơn vị) hoặc theo cả ba thành viên (tầng đối chứng). Khoảng của tỉ lệ là khoảng Clopper–Pearson 95%; khoảng của κ là khoảng bootstrap. Không nhãn nào được gắn cho giả thuyết nào (low inter-rater agreement). Các hàng của riêng từng người chấm không có phán quyết và không có khoảng. Phần dưới: các đại lượng trên toàn bộ cặp chính.

| Đại lượng | Lật theo dấu câu (P) | Lật theo đơn vị (U) | Đối chứng (C) |
|---|---|---|---|
| Ảnh đủ điều kiện | 165 | 266 | 558 |
| Cặp được cả hai người chấm đánh giá | 100 | 160 | 40 |
| Cặp quyết định (hai người chấm ưa cùng một chú thích) | 28 | 75 | 26 |
| Đồng thuận: cặp quyết định khớp | 16 | 37 | 20 |
| Tỉ lệ đồng thuận [khoảng 95%] | 0.571 [0.372, 0.755] | 0.493 [0.376, 0.611] | 0.769 [0.564, 0.910] |
| p nhị thức chính xác so với 0.5 | 0.286, một phía | 1.000, hai phía | không đăng ký phép thử |
| Hiệu chỉnh Holm ở mức 0.05 | không bị bác bỏ | không bị bác bỏ | không đăng ký phép thử |
| Nhãn đã đăng ký | "no label: low inter-rater agreement" | "no label: low inter-rater agreement" | không đăng ký nhãn |
| Riêng người chấm không phải tác giả: cặp khớp, trên số cặp người này quyết định | 24 trong 46 | 59 trong 114 | không có trong tệp kết quả |
| Riêng người chấm không phải tác giả: tỉ lệ; p | 0.522; 0.441, một phía | 0.518; 0.779, hai phía | không có trong tệp kết quả |
| Riêng người chấm là tác giả: cặp khớp, trên số cặp người này quyết định | 38 trong 63 | 70 trong 139 | không có trong tệp kết quả |
| Riêng người chấm là tác giả: tỉ lệ; p | 0.603; 0.065, một phía | 0.504; 1.000, hai phía | không có trong tệp kết quả |
| κ của Cohen trong tầng | 0.345 | 0.260 | 0.516 |
| Biên không quá trung vị của tầng: cặp quyết định khớp | 8 trong 14 | 20 trong 38 | 11 trong 13 |
| Biên trên trung vị của tầng: cặp quyết định khớp | 8 trong 14 | 17 trong 37 | 9 trong 13 |
| Toàn bộ cặp chính; cặp được cả hai người chấm trả lời | 300; 300 | | |
| Cặp quyết định | 129 | | |
| Không quyết định: ít nhất một người chấm chọn hoà | 128 | | |
| Không quyết định: ưu tiên trái nhau | 43 | | |
| Không quyết định: "cannot judge"; thiếu | không người chấm nào dùng; không có | | |
| κ của Cohen, ba hạng mục [khoảng bootstrap 95%]; dải đã đăng ký | 0.351 [0.270, 0.433]; 0.20 đến dưới 0.40 | | |
| Đồng thuận thô | 0.567 (170 trong 300) | | |
| AC1 của Gwet | 0.355 | | |
| κ, hai hạng mục, trên các cặp cả hai người chấm đều quyết định | 0.470 (172 cặp) | | |
| Tỉ lệ hoà: người chấm là tác giả; người chấm không phải tác giả | 0.200 (60); 0.363 (109) | | |
| Trong cùng người chấm, 30 lần lặp ẩn, người chấm là tác giả: thô; κ | 0.933; 0.891 | | |
| Trong cùng người chấm, 30 lần lặp ẩn, người chấm không phải tác giả: thô; κ | 0.567; 0.363 | | |

Fig. 3 của bài (chưa dựng) sẽ vẽ ba tỉ lệ đồng thuận kèm khoảng Clopper–Pearson 95% theo tầng, tỉ lệ riêng của từng người chấm ở hai tầng giả thuyết như các dấu riêng không có khoảng, và một đường tham chiếu ở 0.5; chú thích hình ghi: "No label is attached (low inter-rater agreement)".

### B.21.3 Đồng thuận giữa hai người chấm và trong cùng người chấm

κ của Cohen trên ba hạng mục, trên 300 cặp chính, là 0.351 (khoảng bootstrap 95% từ 0.270 đến 0.433). Bài viết: "The band is set by the point value; its interval reaches above 0.40", tức dải được xác định bởi giá trị điểm, còn khoảng của nó vươn lên trên 0.40. Đồng thuận thô là 0.567 (170 trong 300), và AC1 của Gwet là 0.355 (Gwet, 2008; chờ kiểm). Trên hai hạng mục, trên 172 cặp mà cả hai người chấm đều quyết định, κ là 0.470. Theo tầng, κ là 0.345 (dấu câu), 0.260 (đơn vị) và 0.516 (đối chứng). Người chấm là tác giả chọn hoà ở 0.200 số cặp (60) và người chấm không phải tác giả ở 0.363 (109).

Trong cùng người chấm, trên 30 lần lặp ẩn sau khi hoàn nguyên việc đổi bên, đồng thuận thô của người chấm là tác giả là 0.933 (κ 0.891) và của người chấm không phải tác giả là 0.567 (κ 0.363). Bài nói rõ: đồng thuận trong cùng người chấm được báo cáo như đã đăng ký; nó không phải một cổng, và không câu trả lời nào bị loại hay bị gán trọng số vì nó.

### B.21.4 Các hàng đứng cạnh giả thuyết (không có phán quyết)

Riêng với người chấm không phải tác giả, 24 trong 46 cặp người này quyết định ở tầng dấu câu khớp với thứ tự khi bỏ dấu câu (0.522; p một phía = 0.441), và 59 trong 114 cặp ở tầng đơn vị khớp với thứ tự theo từ (0.518; p hai phía = 0.779). Riêng với người chấm là tác giả, các số đếm là 38 trong 63 (0.603; p một phía = 0.065) và 70 trong 139 (0.504; p hai phía = 1.000). Tệp kết quả không chứa khoảng nào cho bốn hàng này và bài không in khoảng nào; không hàng nào mang nhãn. Theo ngăn biên, số cặp quyết định khớp, ở mức không quá trung vị của tầng và trên trung vị, là 8 trong 14 và 8 trong 14 ở tầng dấu câu, 20 trong 38 và 17 trong 37 ở tầng đơn vị, và 11 trong 13 và 9 trong 13 ở tầng đối chứng.

### B.21.5 Nhánh đã đăng ký đã rơi

Quy tắc đã đăng ký đọc hai giả thuyết theo κ của Cohen. Từ 0.40 trở lên, chúng mang nhãn. Từ 0.20 đến dưới 0.40, theo nguyên văn: "the hypotheses are reported without labels, with the words 'low inter-rater agreement', and each rater's own shares are reported beside the consensus". Dưới 0.20, phần con người là "NOT_EVALUABLE". Nhánh thứ hai đã rơi, theo giá trị điểm của κ. Các điều kiện đã đăng ký khác không áp dụng: người chấm thứ hai đã xong khi phần chấm đóng, nên cách diễn đạt cho trường hợp một người chấm không được dùng; mỗi tầng có số ảnh đủ điều kiện lớn hơn cổng của nó (100 cho tầng đơn vị, 40 cho tầng dấu câu); và phép phân tích kết thúc trước cổng thời gian.

**Nhận xét rà soát.** Mục 6.7 là phần thay đổi lớn nhất so với văn bản trước, và cũng là phần nhà nghiên cứu sẽ bị hỏi nhiều nhất. Các nhận xét dưới đây xếp theo mức quan trọng.

(i) *Kết quả là một kết quả không có nhãn, và phải được nói đúng như thế.* Không từ nào trong các từ SUPPORTED, NOT SUPPORTED, UNDERPOWERED, WORD AGREES MORE, SYLLABLE AGREES MORE, EQUIVALENT hay INCONCLUSIVE được gắn cho H-P hoặc H-U, kể cả dưới dạng diễn đạt lại. Hai phép thử không bị bác bỏ, nhưng "không bị bác bỏ" ở đây không được đọc thành "không có khác biệt", cũng không được đọc thành "thiếu công suất" như một nhãn: bài chỉ nêu hai sự kiện về cỡ mẫu (28 so với 47; 75 so với khoảng 215) và ghi rõ chúng không phải nhãn. Khi viết lại, nhà nghiên cứu cần giữ cụm "low inter-rater agreement" và giữ câu "no label is attached" ở mọi nơi in nhãn P1 và P2 (tóm tắt, Mục 1, Table 3, Mục 6.7, Mục 9).

(ii) *Dải được xác định bởi giá trị điểm.* κ = 0.351 nằm trong dải 0.20 đến dưới 0.40, nhưng khoảng của nó vươn tới 0.433. Bài nói điều này và không dùng nó; đó là cách xử lý đúng, vì quy tắc đã đăng ký đọc giá trị điểm. Phản biện có thể hỏi vì sao không báo cáo nhãn "có điều kiện"; câu trả lời là quy tắc được cố định trước và không có nhánh như vậy.

(iii) *Không hàng nào của riêng một người chấm được nâng lên.* Hàng dấu câu của riêng người chấm là tác giả (38 trong 63; p một phía = 0.065) là một trong bốn hàng không có nhãn. Nó không được gọi là xu hướng, gần có ý nghĩa hay gợi ý, và không được tách ra khỏi ba hàng kia. Người chấm này là tác giả và biết giả thuyết, nên hàng ấy càng không thể mang sức nặng riêng.

(iv) *Đồng thuận trong cùng người chấm khác nhau rõ giữa hai người chấm.* Người chấm là tác giả lặp lại câu trả lời đầu ở 0.933 số lần lặp, người chấm không phải tác giả ở 0.567. Bài báo cáo cả hai, không diễn giải, và nói rõ không loại hay gán trọng số câu trả lời nào. Phản biện gần như chắc chắn sẽ hỏi về độ tin cậy của người chấm thứ hai. Bài hiện không đưa ra cách đọc nào cho mức đồng thuận thấp; nếu nhà nghiên cứu muốn thêm một cách đọc, nó phải được ghi rõ là hậu nghiệm, đặt ở phần hạn chế, và không bao giờ được dùng làm lý do để loại hay gán trọng số câu trả lời. Mọi phương án chấm lại, thêm người chấm thứ ba hay đặt quy tắc mới sẽ là một nghiên cứu mới, không phải nghiên cứu này.

(v) *Các công bố về phiên chấm phải còn nguyên văn.* Bốn câu ở các mục 1 đến 4 của B.21.1 là các câu đã cố định từng chữ. Hiện câu về vòng luyện tập xuất hiện ba lần (Mục 5.5, 6.7 và 8), các câu về phiên của người chấm thứ hai và về trang bị lộ xuất hiện hai lần (Mục 6.7 và 8). Khi cắt bớt chỗ lặp, mỗi câu phải còn nguyên văn ít nhất một lần trong Mục 6.7, cạnh câu về người chấm là tác giả; Mục 8 khi đó có thể dẫn chiếu tới Mục 6.7. Không câu nào trong bài được nói rằng một người chấm đã luyện tập trước, và hàng của riêng người chấm không phải tác giả không được mô tả là không chịu sai lệch này.

(vi) *Lời khẳng định về việc làm việc một mình mới chỉ là của tác giả.* Câu hiện viết "rests on the statement of the author". Chỉ khi có một dòng xác nhận của chính người chấm thứ hai thì mới được viết "of the author and the rater". Đây là việc nhà nghiên cứu cần làm trước khi nộp: xin người chấm thứ hai một dòng xác nhận rằng người này đã trả lời một mình, không dùng công cụ tìm kiếm hay công cụ AI.

(vii) *Việc lộ trang 27 phút.* Bài công bố rằng không biết có ai đã mở trang hay không. Vì khi đó chưa có câu trả lời nào, sự việc không chạm tới dữ liệu, nhưng nội dung các cặp của người chấm thứ hai có thể đã bị đọc; phản biện có thể hỏi điều này có ảnh hưởng tới tính độc lập không, và câu trả lời trung thực là bài không biết.

(viii) *Câu về giữ kín kết quả.* Câu cuối của đoạn mở nói nhật ký không ghi nhận lần tiết lộ nào; nó không khẳng định tuyệt đối rằng người chấm là tác giả không thấy con số nào. Cần giữ đúng mức ấy. Câu dùng đại từ "him" cho người chấm là tác giả; có thể đổi thành "that rater" mà không đổi nghĩa.

(ix) *Chỗ chưa nhất quán nhỏ.* Table 6 in 266 ảnh đủ điều kiện cho tầng đơn vị, còn Mục 5.5 cho biết chỉ 215 ảnh còn lại sau khi để riêng ảnh của tầng trước (và 298 cho tầng đối chứng thay vì 558). Hàng "Eligible images" nên có chú thích. Đoạn chính viết "kappa" bằng chữ, đoạn về đồng thuận dùng κ. Table 6 hiện được điền tay; đặc tả yêu cầu sinh lại bằng tập lệnh từ tệp kết quả và so từng ô.

(x) *Điều mục này cho phép và không cho phép kết luận.* Ở tầng đối chứng, nơi ba thành viên cùng thứ tự, tỉ lệ đồng thuận là 0.769 trên 26 cặp quyết định; đây là hàng mô tả, không có phép thử đăng ký. Ở hai tầng giả thuyết, các tỉ lệ đồng thuận (0.571 và 0.493) có khoảng chứa 0.5. Bài không rút ra khuyến nghị thành viên nào từ đó, và giữ `f0` làm mặc định (B.22). Không câu nào của bài nói dữ liệu con người "không phân biệt được" các phương án, vì mệnh đề nguyên văn ấy của bản đăng ký dành cho nhánh có nhãn.

## B.22 Mục 7 của bản thảo viết lại: Thảo luận và khuyến nghị (Discussion and recommendations)

**Nội dung.** Mục 7 có bốn phần. Phần thứ nhất nói một chứng nhận dùng để làm gì. Một chứng nhận là một phát biểu về một phép so sánh dưới một độ đo: trên họ được liệt kê, chiều của hiệu không phụ thuộc khâu xử lý. Nó không phải phát biểu về chất lượng của một hệ thống, và không nói gì ngoài họ. Công dụng của nó là trong báo cáo. Người đọc thấy CERTIFIED trên F cạnh một hiệu CIDEr-D biết rằng một phản bác thường gặp với bảng kết quả tiếng Việt, rằng bộ tách từ khác hay chính sách dấu câu khác sẽ làm đổi phán quyết, đã được kiểm cho các phương án được liệt kê. Người đọc thấy FRAGILE cùng tập phá vỡ biết phán quyết phụ thuộc vào những lựa chọn nào. NULL-STABLE nói rằng phép so sánh chưa ngã ngũ dưới mọi thành viên, và đó cũng là thông tin.

Phần thứ hai giới hạn điều lần áp dụng cho phép nói. Mệnh đề của bản đăng ký cho nhãn P2, "a cheap check whose usual answer is CERTIFIED", chỉ đúng ở đây trong một phạm vi: trong các phép so sánh có ý nghĩa dưới `f0`, 8 trong 10 (FL) và 908 trong 936 (D, DEVELOPMENT) là CERTIFIED trên F. Bài viết rằng đây không phải bằng chứng cho việc có thể bỏ qua khâu xử lý: trong các tập này, 28 kết luận phát triển và 2 kết luận chấm lần đầu có thay đổi; P2 là "NOT SUPPORTED" trong một tập 10 phép so sánh có ý nghĩa gần như đến từ một kho; và P1 mang các nhãn "INCONCLUSIVE" và "LOW-SENSITIVITY", mà bài không thêm cách đọc nào ngoài các số đếm ở Mục 6.3. Bài không phát biểu gì về tần suất khâu xử lý làm đổi kết luận ngoài các số đếm ấy.

Phần thứ ba là ba khuyến nghị cho việc báo cáo điểm chú thích tiếng Việt. Một: báo cáo khâu xử lý cùng mỗi điểm, gồm đơn vị, bộ tách từ và phiên bản, cách xử lý vị trí dấu thanh, chính sách dấu câu và chữ hoa, cùng biến thể CIDEr và thang điểm. Hai: khi một quy trình thay bộ tách PTB bằng một bộ tách từ, khôi phục bước bỏ token dấu câu hoặc báo cáo CIDEr-D cả khi có và không có bước ấy, và nói rõ quy trình nào tạo ra mỗi điểm được so. Ba: cạnh một hiệu được khẳng định giữa hai hệ thống, báo cáo chứng nhận trên họ được liệt kê: phán quyết, họ, số lớp và, với một phép FRAGILE, tập phá vỡ. Mã được công bố tính dòng thứ ba từ hai tệp đầu ra và một tệp tham chiếu; nó không cần mô hình và không cần GPU. Các khuyến nghị của giai đoạn trước về điểm ở mức đối tượng nằm ở Online Resource 2.

Phần thứ tư nói về thành viên được khuyến nghị để báo cáo, bằng câu đã cố định: "`f0` remains the default for reporting (registration l.304); the human arm, at low inter-rater agreement, gave no labelled result on which to recommend another member." Nghĩa là: `f0` vẫn là mặc định để báo cáo; phần con người, ở mức đồng thuận thấp giữa hai người chấm, không cho kết quả có nhãn nào để dựa vào đó khuyến nghị một thành viên khác. Bài nói rõ câu này không phải mệnh đề nguyên văn của bản đăng ký, vốn dành cho trường hợp cả hai giả thuyết mang nhãn; lời văn cho các nhánh còn lại đã được quyết định trước khi phép phân tích phần con người tồn tại (Online Resource 1, E.6). Bài nhắc lại rằng kết quả của con người "never changes F, a certificate, a P1 to P3 label or the P4 method check".

**Nhận xét rà soát.** Mục 7 thận trọng đúng mức với ba nhãn không thuận lợi và một kết quả không có nhãn. Điểm cần cân nhắc là sức nặng còn lại của bài. Với P1 "INCONCLUSIVE" kèm "LOW-SENSITIVITY", P2 "NOT SUPPORTED" và phần con người không có nhãn, đóng góp bài có thể bảo vệ là thủ tục, họ được liệt kê, mã chạy được trên CPU và một lần áp dụng được báo cáo trung thực; bài không có bằng chứng rằng khâu xử lý làm đổi nhiều kết luận, và tự nói như vậy. Nhà nghiên cứu cần chuẩn bị cho câu hỏi "vậy bài đóng góp gì" bằng chính các câu của Mục 7, không bằng một cách đọc lạc quan hơn về các nhãn. Thứ hai, khuyến nghị ba đòi tác giả khác báo cáo chứng nhận, trong khi mã và giấy phép còn là các chỗ chờ tác giả điền ở phần tuyên bố; khuyến nghị chỉ thực hiện được khi mã thật sự được công bố. Thứ ba, câu về thành viên mặc định dẫn số dòng của bản đăng ký; cần thay bằng dẫn chiếu người đọc tra được. Thứ tư, cụm "P1 to P3 label or the P4 method check" nhắc tới P3 và P4 trong khi hai mục này đang vắng mặt trong văn bản; nếu P3 và P4 tiếp tục được giữ ngoài bài thì câu trích cần một chú thích, vì người đọc không biết P3 và P4 là gì.

## B.23 Mục 8 của bản thảo viết lại: Hạn chế (Limitations)

**Nội dung.** Mục 8 gồm bảy đoạn có tiêu đề: sáu đoạn về hạn chế của nghiên cứu mới và một đoạn về các nghiên cứu đăng ký trước đây.

*Một họ mô hình nền.* 73 tệp của nhóm là biến thể của hệ thống của chính nhóm trên một mô hình nền. Các số đếm phát triển không nói gì về phép so sánh giữa các kiến trúc khác nhau.

*Một độ đo, một họ được liệt kê, một bảo đảm danh nghĩa.* CIDEr-D là độ đo duy nhất có phán quyết, và các độ đo học được nằm ngoài chứng nhận. Họ được liệt kê, nên không có gì được bảo đảm ngoài nó. Ba quyết định chấp nhận là của nhóm tác giả (giữ các thành viên giữ chữ hoa, loại đơn vị ký tự, giữ các thành viên giữ dấu câu); Table 7 cho thấy mỗi quyết định làm đổi điều gì. Phép thử theo thành viên là bootstrap phân vị, bảo đảm là danh nghĩa và có điều kiện theo tham chiếu cùng tần suất văn bản của chúng, các phép so sánh dùng chung tệp, và không có khẳng định nào ở mức cả họ phép thử.

*Một sự kết hợp, và một đơn vị để dành.* FE-CERT kết hợp các ý tưởng đã biết, và người đọc có thể xem nó là một bảng đa vũ trụ kèm quy tắc quyết định; bài viết: "we claim no more than that". Họ để dành là một bộ tách từ, nên P1 kiểm các chứng nhận với một đơn vị duy nhất mà đề tài chưa từng chạy trên đầu ra hệ thống, không phải với các khâu xử lý nói chung. Đối chứng độ nhạy được đăng ký để đo, trước khi thành viên để dành nào chạy, liệu một phép kiểm như vậy có thể không đạt hay không; nhãn của nó đứng cạnh nhãn P1.

*Tham chiếu đã dùng và một tập chấm lần đầu nhỏ, tập trung.* Ảnh và tham chiếu KTVIC đã được đề tài dùng trước, nên mọi kết quả trên tệp của nhóm và trên hai hệ cơ sở là DEVELOPMENT. Tham chiếu của tập chấm lần đầu là tệp của chính các nhóm, với các trùng mã ở Table 2; đề tài đã dùng ảnh của các nhóm G1 và G3 trước đó. Trong 22 phép so sánh chấm lần đầu, 20 đến từ một kho. Bản đăng ký đã đếm 12 trong 14 hệ thống của nhóm khác thuộc tập dự kiến là không có bài báo, và tập thực tế nhỏ hơn: 3 tệp không qua quy tắc phân tích của cổng, nên hai nhóm không lập được phép so sánh nào.

*Ngôn ngữ và con người.* Đối chứng tiếng Anh là "NOT RUN", và bài không khẳng định gì ngoài tiếng Việt. Ưu tiên của con người theo từng ảnh không nói trực tiếp gì về thứ tự ở mức hệ thống. Tiếp theo là các câu về người chấm, nguyên văn: "Two raters judged the pairs, one of them an author. They agreed on the preferred caption or on a tie in 170 of 300 pairs (kappa 0.351). On the 30 hidden repeats the author rater repeated the first answer in 0.933 of cases and the non-author rater in 0.567. The rows of each rater alone are in Table 6; none carries a verdict." Nghĩa là: hai người chấm đánh giá các cặp, một trong hai là tác giả. Họ đồng ý về chú thích được ưa hoặc về việc hoà ở 170 trong 300 cặp (kappa 0.351). Trên 30 lần lặp ẩn, người chấm là tác giả lặp lại câu trả lời đầu ở 0.933 số trường hợp và người chấm không phải tác giả ở 0.567. Các hàng của riêng từng người chấm ở Table 6; không hàng nào mang phán quyết. Sau đó Mục 8 in lại nguyên văn ba công bố đã chép ở B.21.1: về vòng luyện tập, về phiên của người chấm thứ hai và về việc trang chấm bị lộ khoảng 27 phút.

*Đăng ký và lượt đọc.* Các bản đăng ký được đóng dấu thời gian bằng commit và mã băm trong kho của đề tài và không được gửi tới cơ quan đăng ký bên ngoài. Các nhãn được tính lại từ các tệp kết quả đã lưu bởi một người viết không phải người viết mã và không phải người chấm, và được cố định bởi một lượt đọc nội bộ duy nhất; các nhãn liên quan tới thành viên để dành dựa trên chuỗi phán quyết của chính mã.

*Các nghiên cứu đăng ký trước đây.* Các nghiên cứu đề tài đăng ký trước trên cùng bộ chuẩn đặt câu hỏi khác. Chúng được báo cáo ở Online Resource 2 với phán quyết không đổi: một nghiên cứu về kích thước tập huấn luyện trên dữ liệu phát triển (phán quyết đã đăng ký "PASS") cùng phép thử ngoại suy của nó ("INCONCLUSIVE"); phép thử đăng ký duy nhất của một hệ thống cuối ("FAIL"); ba dự đoán đăng ký về bảng xếp hạng trên các mô hình công khai ("FAIL", "INCONCLUSIVE" và "FAIL"); một nghiên cứu phát triển về điểm kiểm chứng đối tượng mà quy tắc dừng đã đăng ký kết thúc trước mọi giai đoạn để dành; và một lần chạy chỉ mô tả của bộ công cụ trên các hệ thống bên ngoài (không có phán quyết). Bài viết: "None of them is a claim of this paper". Các nghiên cứu này được thuật ở B.6, B.7 và B.10.

**Nhận xét rà soát.** Mục 8 đầy đủ và trùng khớp với các mục kết quả; mọi hạn chế, sai lệch và công bố mà bài nêu đều đã được chép ở trên. Ba điểm cần xem. (i) Đoạn thứ bảy ("Earlier registered studies") không phải một hạn chế của nghiên cứu mới mà là một lời dẫn tới Online Resource 2; nên tách nó thành một đoạn chuyển tiếp để người đọc không hiểu các phán quyết cũ là hạn chế của FE-CERT. (ii) Hạn chế về con người hiện không nói rằng phần con người chỉ dùng ba thành viên và các cặp chỉ lấy từ 33 tệp lời nhắc ngắn của một mô hình nền; hai điều này có ở Mục 5.5 và Mục 6.7, và nên được nhắc một câu ở đây vì chúng giới hạn phạm vi của mọi tỉ lệ ở Table 6. (iii) Câu "fixed by a single internal read" là một công bố trung thực về quy trình kiểm; phản biện có thể hỏi vì sao không có lượt đọc độc lập thứ hai, và Online Resource 1 (mục 11 của E.6) nói rõ là không có. Ngoài ra, các nhận xét (v) đến (vii) của B.21 áp dụng nguyên cho các câu công bố được in lại ở mục này.

## B.24 Mục 9 của bản thảo viết lại và các tuyên bố: Kết luận (Conclusion); Statements and Declarations

**Nội dung.** Kết luận gồm một đoạn. Nó mở bằng câu rằng FE-CERT biến một cảnh báo đã biết, rằng bộ tách token làm điểm không so sánh được, thành một phán quyết về một phép so sánh hai hệ thống sinh chú thích tiếng Việt trên một họ khâu xử lý được liệt kê. Sau đó nó in lại, nguyên văn như Mục 1, các câu nhãn: P1 "INCONCLUSIVE" với N = 72, 2 lần vỡ, r = 0.028 và hai cận 0.085, 0.005; nhãn "LOW-SENSITIVITY" với 6 trong 915 ($r_{NC}$ = 0.0066), 54 chứng nhận sát biên ít hơn 59, và hàng POST HOC; P2 "NOT SUPPORTED" với lời đăng ký "(2 of 10)"; đoạn về phần con người với κ 0.351, khoảng 0.270 đến 0.433, 16 trong 28 và 37 trong 75, không phép thử nào bị bác bỏ sau hiệu chỉnh Holm và không nhãn nào được gắn; và câu `f0` vẫn là mặc định. Kết luận khép bằng câu: "The labels are reported one by one and are not combined into one statement about the method."

Phần Statements and Declarations đứng sau kết luận và trước danh mục tài liệu. Về tài trợ, nghiên cứu không nhận tài trợ bên ngoài; mọi chi phí, gồm thời gian máy thuê, do nhóm tác giả chịu. Về xung đột lợi ích, các tác giả tuyên bố không có. Về phê duyệt đạo đức, bài nêu sự kiện: hai người chấm trưởng thành đánh giá các cặp chú thích do máy viết cho ảnh của bộ chuẩn trên một trang cục bộ; không dữ liệu cá nhân nào được lưu ngoài một mã người chấm; còn việc cơ quan của tác giả có đòi xét duyệt hay miễn trừ cho việc này hay không thì để chờ tác giả cung cấp. Về đồng ý tham gia và đồng ý công bố, việc mỗi người chấm có đồng ý bằng văn bản trước khi chấm, và có đồng ý với mức công bố được chọn cho các đánh giá hay không, đều chờ tác giả xác nhận.

Về tính sẵn có của dữ liệu, không ảnh và không chú thích tham chiếu nào được tạo cho nghiên cứu này. KTVIC có ở kho của tác giả bộ dữ liệu, nơi yêu cầu trích dẫn [@pham2024ktvic] và không nêu giấy phép. UIT-ViIC có từ nhóm tác giả của nó [@lam2020uit] cho mục đích nghiên cứu, không nêu giấy phép. Đầu ra của các nhóm khác là công khai tại các kho và commit ở Table 2: hai kho theo giấy phép MIT, và hai kho không có giấy phép, chỉ được dùng cho thống kê tổng hợp. Đầu ra đã công bố của hai hệ cơ sở của bộ chuẩn được dùng với sự cho phép của tác giả kho mã, chỉ cho thống kê tổng hợp. Không được phát hành, vì điều khoản của nguồn không cho phép hoặc tác giả không giữ quyền: ảnh, chú thích tham chiếu, tệp đầu ra của bất kỳ nhóm nào và trọng số tinh chỉnh của nhóm. Được phát hành: các tệp đăng ký, các tệp kết quả của các bước (số đếm và thống kê tổng hợp; không có lời văn chú thích) và bảng kê gắn khoá cho mọi con số của bài. Các đánh giá của con người chỉ được phát hành ở dạng thống kê tổng hợp (tệp kết quả của phần con người; không có lời văn chú thích), là mức mặc định đã đăng ký. Về mã, mã FE-CERT ở commit đã dùng để chạy, các tệp đăng ký và công cụ chấm của phần con người sẽ được phát hành trong một kho lưu trữ; giấy phép và DOI của kho lưu trữ chờ tác giả cung cấp. Đóng góp của từng tác giả và lời cảm ơn (người chấm thứ hai, theo vai trò; theo tên chỉ khi có sự đồng ý bằng văn bản của người đó) cũng chờ tác giả cung cấp.

**Nhận xét rà soát.** Kết luận không nói gì vượt quá các nhãn và tự cấm việc gộp nhãn; khi rút gọn cần giữ câu cuối. Về các tuyên bố, có sáu việc còn mở mà chỉ tác giả làm được: xét duyệt hay miễn trừ đạo đức; đồng ý tham gia của từng người chấm; đồng ý công bố; giấy phép mã; DOI của kho lưu trữ; đóng góp của tác giả và lời cảm ơn. Tuyên bố về đồng ý phải nói đúng điều đã làm và thời điểm làm, không hơn. Bài chưa có mục "Materials availability" theo danh mục tuyên bố của tạp chí. Mức phát hành các đánh giá của con người hiện là mức mặc định đã đăng ký (chỉ thống kê tổng hợp); nếu nhà nghiên cứu muốn phát hành mức chi tiết hơn thì đó là một quyết định cần sự đồng ý của người chấm. Cuối cùng, nghiên cứu phát triển về điểm kiểm chứng đối tượng, vốn dùng một mô hình ngôn ngữ và một mô hình thị giác–ngôn ngữ làm thành phần của phương pháp, nay nằm ở mục S24 của Online Resource 2 và vẫn chưa nêu tên mô hình, phiên bản, lời nhắc hay thiết lập (xem mục 2 của B.12.1).

## B.25 Hai phụ lục trực tuyến của bản thảo viết lại (Online Resource 1 và 2)

**Nội dung.**

### B.25.1 Online Resource 1: hồ sơ của nghiên cứu FE-CERT đã đăng ký

Phụ lục này gom các con trỏ tới bản đăng ký, mã và tệp kết quả, cùng năm bảng, một danh sách sai lệch và một hình. Bài không in danh sách từng phép so sánh chấm lần đầu: phán quyết được báo cáo dưới dạng số đếm theo kho.

*E.1.* Bản đăng ký, kế hoạch của phần con người và phụ lục về mã câu hỏi có muối được commit ngày 2026-11-12; mã như đã chạy ở commit ngày 2026-11-13. Mỗi tệp kết quả bằng đúng mã băm đã được ghi nhật ký cho nó trước khi bước tiếp theo bắt đầu, và mang mã băm của bản đăng ký, của các mô-đun mã và của tệp bước trước.

*E.2, Table E1 (cổng cấu trúc theo tệp).* Trong 19 tệp, 16 được nhận và 3 không đạt quy tắc 1. Năm tệp của G1 có giá trị giống hệt nhau (578 dòng, phủ 1.0000 số mã tham chiếu, không dòng nào trên mã lạ, không mã trùng, không chú thích rỗng, không bản sao tham chiếu, mọi chú thích có dấu), và năm tệp của G2 cũng vậy với 279 dòng. Hai tệp của G3 có 924 dòng và tỉ lệ bản sao tham chiếu 0.0087 và 0.0032; hai tệp của G4 có 100 dòng. Hai tệp hệ cơ sở đã công bố (cặp của chúng thuộc D) có 558 dòng và tỉ lệ bản sao tham chiếu 0.0036 và 0.0108. Hai tệp của G5 không phân tích được thành một chú thích cho mỗi mã ảnh; tệp của G6 là một tệp giá trị độ đo, không có cột chú thích.

*E.3, Table E2 và E2b.* Table E2 đếm, cho các phép FRAGILE, số cặp gồm một phép so sánh và một thành viên trong một lớp phá vỡ mà thành viên ấy mang mức đang xét, theo mười hai mức của bốn trục và bốn hàng (D và FL, trên $F_{dev}$ và trên F). Bài ghi rằng các số đếm trên F là giá trị của mã và không tính lại được từ các thống kê đã lưu. Table E2b là một hàng của mã không có hàng đăng ký riêng và không có phán quyết: chứng nhận chỉ trên các thành viên để dành, cả hai tập gộp lại, cho 937 CERTIFIED, 32 FRAGILE (không phát hiện REVERSED), 154 NULL-STABLE trong 1123 phép so sánh và 40 lần lật dấu điểm ước lượng; các ô phụ thuộc `f0` không xác định vì `f0` không thuộc họ ấy.

*E.4, Table E4.* Bảng ghi điều kiện tiên quyết của ba bộ tách từ (2,790 chuỗi tham chiếu mỗi bộ; không phát hiện chuỗi hỏng), kết quả trên 9 chuỗi thử, phép tái lập điểm đã commit (67 tệp, đều trong 0.01; hiệu lớn nhất 0.0016; 6 tệp không có tệp điểm đã commit), lượt kiểm kê tệp điểm (không phát hiện lần chạy nào của đơn vị để dành hay đơn vị ký tự trên đầu ra hệ thống; 22 tệp điểm của nhóm còn chứa các hàng chấm theo khoảng trắng, không thuộc loại nào trong hai loại ấy) và phiên bản công cụ.

*E.5, Table E5 và E5b.* Table E5 là hồ sơ chạy: mọi bước chạy một lần và kết thúc bình thường ngày 2026-11-13 (UTC) trên một máy thuê, trên CPU; phép phân tích phần con người chạy một lần ngày 2026-11-15 (UTC), trên một máy thuê khác, trên CPU, với mã trả về 0, sau dòng đóng của phần chấm. Bước dựng cặp cho phần con người chạy giữa bước ghim và bước chấm lần đầu; nó không đọc điểm nào và đầu ra của nó không được mở. Table E5b liệt kê các cổng dừng đã đăng ký được báo cáo ở trạng thái văn bản này: các cổng về điều kiện tiên quyết không kích hoạt; cổng về số phép chấm lần đầu có ý nghĩa dưới `f0` (ít hơn 10) không kích hoạt (10); cổng về số phép chấm lần đầu lập được (ít hơn 20) không kích hoạt (22); cổng N dưới 59 không kích hoạt (N = 72); cổng độ nhạy ($r_{NC}$ không quá 0.05) kích hoạt ($r_{NC}$ = 0.0066) và gắn "LOW-SENSITIVITY" cho P1; cổng của phần con người không kích hoạt (mỗi tầng trên cổng ảnh đủ điều kiện của nó; người chấm thứ hai đã xong; κ = 0.351 không dưới 0.20 nên phần này đánh giá được, và dải báo cáo không kèm nhãn được áp dụng); cổng thời gian không kích hoạt.

*E.6, danh sách sai lệch và công bố.* Mười bốn mục, trong đó mục cuối là chỗ neo của phần đang giữ ngoài văn bản. Các mục 1 đến 12 thuộc các bước tính trên máy: máy thuê được chọn không phải gói rẻ nhất đạt yêu cầu (một sai lệch được ghi nhận); các phép kiểm trước khi chạy (tự kiểm đạt 47 trong 47, tự kiểm của bộ dựng cặp đạt 39 trong 39 hai lần, kiểm đột biến loại 94 trong 94 đột biến, kiểm trang chấm đạt 19 trong 19 trên dữ liệu giả lập); một lần đẩy dữ liệu bị dừng và cách sửa (một tên tệp trong 73 được đẩy; hai dòng của trình trợ giúp được sửa, không mã nghiên cứu nào đổi; lần đẩy sau gồm 167 tệp); một gói hệ thống cài sau các phép kiểm; thứ tự và việc giữ kín lần chạy; các sự kiện hồ sơ; những gì đã được nhìn thấy trước các bước đăng ký (các ngưỡng của cổng, bản in lược đồ dùng để viết bộ phân tích); các lần chạy trước của các đơn vị (pyvi đã chạy trên đầu ra của nhóm và trên ba hệ thống bên ngoài nên là đơn vị phát triển; underthesea chỉ từng chạy trên tham chiếu nên là đơn vị để dành); các cách đọc bản đăng ký đã được mã hoá (khoảng của BLEU-4; mọi sai khác trong phép tái lập là FAULT; chiều của hàng biên; đối chứng tiếng Anh "NOT RUN"); câu gắn với nhãn độ nhạy và hàng POST HOC; cách các nhãn được kiểm (tính lại từ tệp đã lưu bởi một người viết không phải người viết mã và không phải người chấm; một lượt đọc nội bộ duy nhất, không có lượt đọc độc lập thứ hai); và một câu công bố nguyên văn về việc giữ kín các giá trị in, thuộc bước đang giữ ngoài văn bản.

Mục 13 của E.6 là hồ sơ của phần con người, gồm bốn phần. *Giữ kín nhãn:* phiên của mỗi người chấm kết thúc bằng một dòng nhật ký ghi số dòng và mã băm của tệp nhãn cùng bản sao chỉ đọc: người chấm là tác giả ngày 2026-11-14 (363 dòng đã lưu) và người chấm không phải tác giả ngày 2026-11-15 (439 dòng đã lưu, kèm một dòng đính chính ghi rằng mọi câu trả lời của người này được lưu trực tiếp tại máy và không câu nào qua đường dẫn từ xa). Một bản ghi đóng và dòng đóng (2026-11-15, 08:08:59Z) cố định mã băm cuối của hai tệp nhãn và tệp khoá; một đính chính của bản ghi đóng cố định tình trạng tệp của người chấm thứ hai và lời văn công bố về vòng luyện tập. Các bản sao chỉ đọc sau đó được đẩy lên một máy thuê có kiểm mã băm; phép phân tích đã đăng ký chạy một lần, mã trả về 0; tệp kết quả chỉ chứa số đếm và thống kê, không có lời văn chú thích. Tệp nhãn được xoá khỏi máy sau khi kết quả được kéo về, và máy được xoá. Không có phép phân tích độ nhạy nào. *Các mục như đã dựng:* các số ở B.19.5 (165, 266, 558; 215 và 298; 100, 160 và 40; 300 cặp chính, 30 lần lặp, 330 màn hình; 8 màn hình luyện tập mà không người chấm nào làm). *Nhánh:* nhánh không kèm nhãn đã rơi; câu khuyến nghị lệch khỏi mệnh đề nguyên văn theo điều đã quyết định trước khi phép phân tích tồn tại. *Nhịp chấm (mô tả):* theo dấu thời gian của máy chủ trang chấm, người chấm là tác giả lưu 363 dòng cho 330 màn hình trong khoảng 67 phút, và người chấm không phải tác giả lưu 439 dòng cho 330 màn hình trong khoảng 68 phút; một câu trả lời được đổi là một dòng mới. Kế hoạch dự kiến khoảng 20 giây mỗi màn hình. Trang chấm còn lưu một trường thời gian trên màn hình: thời gian, do trình duyệt gửi, từ lúc trang đặt ảnh của một màn hình mới tới lúc một câu trả lời được bấm, một giá trị cho mỗi dòng đã lưu (kể cả câu trả lời được đổi). Trung vị của trường này là 614 ms (người chấm là tác giả) và 336 ms (người chấm không phải tác giả). Bài viết rằng cả hai trung vị thấp hơn nhiều so với khoảng thời gian trên mỗi màn hình; "they are not explained". Chúng được in đúng như đã ghi, không được diễn giải và không được dùng, và không câu trả lời nào bị loại hay gán trọng số theo nhịp chấm.

*E.7, Fig. EF1 (chưa dựng).* Hình sẽ vẽ phân bố biên chuẩn hoá dưới `f0` của các phép CHANGED trên F và các phép không CHANGED, với hai diện tích dưới đường cong 0.8012 và 0.9546 đã nêu ở B.20.5.

### B.25.2 Online Resource 2: các nghiên cứu đăng ký trước đây và phần kiểm định chuyển từ thân bài cũ

Mục S.0 nói phụ lục này là hồ sơ của giai đoạn trước của đề tài trên cùng bộ chuẩn: giai đoạn ấy kiểm định xem một điểm KTVIC đo điều gì, với một hệ thống có kiểm soát, và đăng ký một số nghiên cứu riêng. Không nghiên cứu nào trong đó là khẳng định của bài này; chúng được báo cáo để không kết quả đăng ký nào bị bỏ sót, và mọi phán quyết đã đăng ký được chép không đổi. Phụ lục có hai phần. Các mục S1 đến S15 là phụ lục của phiên bản trước, mang sang không đổi lời văn. Các mục S16 đến S28 là các phần chuyển ra khỏi thân bài cũ; mỗi mục là bản sao của các dòng nêu trong tiêu đề của nó, và chỗ nào một câu phải đổi vì bài hiện tại khác bài trước thì chỗ đổi được đánh dấu trong khối. Ghi chú đọc cho biết trong S1 đến S28, "Section" kèm một số và các Table 2.1, 4.1, 4.2 và 5.1 chỉ phiên bản trước; sơ đồ chuyển chỗ đã chép ở Bảng B.29. Trong các mục ấy, "this paper", "the main text" và "our protocol" nghĩa là phiên bản trước và giao thức chấm đã commit của nó, tức thành viên tham chiếu của thân bài hiện tại. Nội dung của các mục này đã được thuật ở B.2 đến B.10.

**Nhận xét rà soát.** Online Resource 1 làm đúng vai trò "mọi sai lệch ở một chỗ". Sáu điểm cần xem. (i) Mục 13 của E.6 gọi các dòng nhật ký bằng mã nội bộ và nhắc một mã quyết định nội bộ; người đọc bên ngoài không tra được các mã này, nên trước khi nộp cần thay bằng lời mô tả. Cũng vậy với tên gọi nội bộ của bước phân tích phần con người. (ii) Trung vị thời gian trên màn hình dưới một giây ở cả hai người chấm là chi tiết lạ nhất của hồ sơ. Bài in nó kèm định nghĩa của trường và chữ "not explained", không bỏ nó vì nó trông lạ; đó là cách xử lý đúng với một đại lượng đã được yêu cầu báo cáo trước khi có nhãn. Phản biện có thể đọc nó như dấu hiệu trả lời vội. Câu trả lời hiện có là hai khoảng thời gian tổng (khoảng 67 và 68 phút cho 330 màn hình) và việc người chấm là tác giả, người đã biết rõ, cũng có trung vị cùng cỡ; một phép thử công cụ trên một phiên giả lập có thể giải thích trường này mà không cần mở tệp nhãn, và nếu nhà nghiên cứu nhớ mình đã trả lời bằng cách nào thì một dòng mô tả sẽ giúp phép thử ấy. (iii) Số dòng đã lưu lớn hơn số màn hình (363 và 439 so với 330) vì câu trả lời được đổi tạo dòng mới; phần vượt ở người chấm không phải tác giả lớn hơn, và bài không diễn giải điều đó. (iv) Mục 12 của E.6 là một câu nguyên văn về một bước đang vắng mặt trong thân bài; nếu P3 và P4 tiếp tục ở ngoài thì người đọc không hiểu câu ấy nói về điều gì. (v) Trong các khối văn bản cũ của Online Resource 2 còn những dẫn chiếu "Supplementary S..." và số mục của phiên bản trước; ghi chú đọc ở S.0 giải thích, nhưng một bản nộp sạch nên sửa các dẫn chiếu ấy. (vi) Các nhận xét ở B.10 và danh mục B.12 vẫn áp dụng cho phần mang sang; đặc biệt các chỗ thiếu của nghiên cứu về điểm kiểm chứng đối tượng (mục 2 của B.12.1) nay thuộc S24.

## B.26 Bảng đối chiếu khẳng định – bằng chứng của bản thảo viết lại

Bảng dưới đây gồm mỗi khẳng định của tóm tắt, mục mở đầu và kết luận của bản thảo viết lại một hàng. Cột tình trạng dùng nhãn của chính bài. Khoá ở cột cuối viết theo dạng tên tệp và khoá như trong `number_manifest_B_v2.tsv`.

**Bảng B.38.** Đối chiếu khẳng định với bằng chứng của bản thảo viết lại.

| Khẳng định (rút gọn) | Tình trạng | Mục của bài | Bảng, hình | Số liệu chính | Khoá trong bảng kê |
|---|---|---|---|---|---|
| Riêng đơn vị làm CIDEr-D của một hệ thống xê dịch 15.64 điểm | POST HOC | 1, 3 | – | 149.79 so với 165.43; τ = 0.969 trên 26 hệ thống | các khoá của văn bản trước (xem Bảng B.27) |
| Một dấu chấm thêm vào làm mất 35.17 điểm dưới bộ chấm giữ dấu câu | POST HOC | 1, 3 | – | 148.66 xuống 113.49; −23.66%; 0.00 khi bỏ token dấu câu | các khoá của văn bản trước (xem Bảng B.27) |
| Họ có 72 thành viên: 54 phát triển, 18 để dành | DESCRIPTIVE | 4.1, 6.1 | Table 1 | 72; 54; 18 | `FAMILY.json::family.F`, `FAMILY.json::family.F_dev` |
| Trên D, 909 trong 1101 phép so sánh là CERTIFIED trên họ phát triển; 27 trong 936 là CHANGED | DEVELOPMENT | 6.2 | Table 4 | 909; 1101; 0.0288 | `RESULT.json::counts.D_over_F_dev_DEVELOPMENT.CERTIFIED`, `RESULT.json::counts.D_over_F_dev_DEVELOPMENT.comparisons`, `RESULT.json::counts.D_over_F_dev_DEVELOPMENT.CHANGED_share` |
| P1: 2 trong 72 chứng nhận sát biên vỡ dưới thành viên để dành | REGISTERED PREDICTION: "INCONCLUSIVE" | tóm tắt, 1, 6.3, 9 | Table 5 | N = 72 (68 và 4); r = 0.028; cận 0.085 và 0.005 | `RESULT.json::P1.N`, `RESULT.json::P1.breaks`, `RESULT.json::P1.r`, `RESULT.json::P1.cp_upper_95`, `RESULT.json::P1.cp_lower_95` |
| P1 mang nhãn độ nhạy: 6 trong 915 chứng nhận âm tiết vỡ | nhãn đăng ký "LOW-SENSITIVITY" (tính trên DEVELOPMENT) | tóm tắt, 1, 6.3, 9 | Table 5 | $r_{NC}$ = 0.0066; 54 sát biên, ít hơn 59 | `NC.json::V_NC`, `NC.json::breaks`, `NC.json::r_NC` |
| Cả 6 lần vỡ của đối chứng nằm trong 54 chứng nhận sát biên | POST HOC; không làm đổi nhãn | 1, 6.3, 9 | Table 5 | 6 trong 54 | `owed/N9_OUTPUT.txt::breaks`, `owed/N9_OUTPUT.txt::near-margin Cert_NC` |
| P2: 2 trong 10 phép chấm lần đầu có ý nghĩa dưới `f0` là CHANGED | REGISTERED PREDICTION: "NOT SUPPORTED" | tóm tắt, 1, 6.4, 9 | Table 4 | 2 trong 10; 0.2000; 22 phép lập được, 20 từ một kho | `RESULT.json::P2.k_FL`, `RESULT.json::P2.n_FL`, `GATE2.json::formed` |
| Hai người chấm đánh giá 300 cặp; đồng thuận thấp | đại lượng đã đăng ký; "no label: low inter-rater agreement" | tóm tắt, 1, 6.7, 9 | Table 6 | κ = 0.351 [0.270, 0.433]; dải 0.20 đến dưới 0.40 | `HUMAN.json::inter_rater.n`, `HUMAN.json::inter_rater.kappa`, `HUMAN.json::inter_rater.kappa_ci95.0`, `HUMAN.json::inter_rater.kappa_ci95.1` |
| H-P: thứ tự khi bỏ dấu câu khớp ở 16 trong 28 cặp quyết định | đại lượng đã đăng ký; không có nhãn | tóm tắt, 1, 6.7, 9 | Table 6, Fig. 3 | 0.571 [0.372, 0.755]; p một phía = 0.286 | `HUMAN.json::strata.P.k_word`, `HUMAN.json::strata.P.n_dec`, `HUMAN.json::strata.P.q`, `HUMAN.json::p.H-P` |
| H-U: thứ tự theo từ khớp ở 37 trong 75 cặp quyết định | đại lượng đã đăng ký; không có nhãn | tóm tắt, 1, 6.7, 9 | Table 6, Fig. 3 | 0.493 [0.376, 0.611]; p hai phía = 1.000 | `HUMAN.json::strata.U.k_word`, `HUMAN.json::strata.U.n_dec`, `HUMAN.json::strata.U.q`, `HUMAN.json::p.H-U` |
| Cặp đối chứng: 20 trong 26 cặp quyết định | DESCRIPTIVE (hàng đã đăng ký, không có phán quyết) | 6.7 | Table 6 | 0.769 [0.564, 0.910] | `HUMAN.json::strata.C.k_word`, `HUMAN.json::strata.C.n_dec`, `HUMAN.json::strata.C.q` |
| Đồng thuận thô, AC1, κ hai hạng mục, κ theo tầng | DESCRIPTIVE (không có phán quyết) | 6.7 | Table 6 | 0.567 (170 trong 300); 0.355; 0.470; 0.345, 0.260, 0.516 | `HUMAN.json::inter_rater.raw`, `HUMAN.json::inter_rater.ac1`, `HUMAN.json::inter_rater.kappa_two_category`, `HUMAN.json::inter_rater.kappa_per_stratum.P` |
| Đồng thuận trong cùng người chấm trên 30 lần lặp ẩn | DESCRIPTIVE (không phải cổng) | 6.7, 8 | Table 6 | 0.933 (κ 0.891); 0.567 (κ 0.363) | `HUMAN.json::within_rater.PI.raw`, `HUMAN.json::within_rater.PI.kappa`, `HUMAN.json::within_rater.R2.raw`, `HUMAN.json::within_rater.R2.kappa` |
| Hàng của riêng từng người chấm | DESCRIPTIVE (không có phán quyết, không có khoảng) | 6.7 | Table 6, Fig. 3 | 24 trong 46; 59 trong 114; 38 trong 63; 70 trong 139 | `HUMAN.json::rater_alone.R2.P.k_word`, `HUMAN.json::rater_alone.R2.U.k_word`, `HUMAN.json::rater_alone.PI.P.k_word`, `HUMAN.json::rater_alone.PI.U.k_word` |
| `f0` vẫn là mặc định để báo cáo | hệ quả của nhánh không kèm nhãn | tóm tắt, 1, 7, 9 | – | – | – |
| Đối chứng tiếng Anh | "CONTROL: NOT RUN" | 6.5, 8 | Table 7 | – | – |
| Các nghiên cứu đăng ký trước đây giữ nguyên phán quyết | "PASS", "INCONCLUSIVE", "FAIL", "FAIL", "INCONCLUSIVE", "FAIL"; một quy tắc dừng | 1, 8 | Online Resource 2 | – | xem Bảng B.27 |

## B.27 Danh mục việc cần rà soát và hoàn thiện của bản thảo viết lại

Danh mục gộp các nhận xét ở B.14 đến B.25. Danh mục B.12 vẫn áp dụng cho phần văn bản được mang sang Online Resource 2.

### B.27.1 Lỗi hoặc mâu thuẫn cần sửa

1. **Bài chưa ở trạng thái nộp được.** Vị trí: Mục 5.3, 5.4, 6.6, Table 3, Table E5, mục 14 của E.6. P3, P4 và Mục 6.6 đang vắng mặt; bài tự ghi không nộp ở trạng thái này. Đề xuất: nhà nghiên cứu trả lời ba quyết định còn mở (đưa P3 và P4 vào; in điểm của các hệ cơ sở; gọi tên hệ thống của nhóm khác); sau đó xoá mọi chỗ neo.
2. **Các câu công bố về phiên chấm phải còn nguyên văn.** Vị trí: Mục 5.5, 6.7, 8. Đề xuất: khi cắt chỗ lặp, giữ mỗi câu trong bốn câu (người chấm là tác giả; vòng luyện tập; phiên của người chấm thứ hai; trang bị lộ khoảng 27 phút) nguyên văn ít nhất một lần ở Mục 6.7; Mục 8 dẫn chiếu tới đó.
3. **Không từ nhãn nào cho H-P và H-U.** Vị trí: tóm tắt, Mục 1, Table 3, Mục 6.7, Mục 7, Mục 9. Đề xuất: khi viết lại, kiểm rằng mỗi nơi in nhãn P1 và P2 đều in "no label" kèm cụm "low inter-rater agreement", và không có cách diễn đạt nào nghe như một phán quyết (kể cả "thiếu công suất", "xu hướng", "gần có ý nghĩa").
4. **Mã và số dòng nội bộ trong văn bản người đọc thấy.** Vị trí: câu về `f0` ở Mục 1, 7 và 9 ("registration l.304"); mục 13 của E.6 (mã của các dòng nhật ký và một mã quyết định); cụm "(the PI)" trong câu về người chấm là tác giả. Đề xuất: thay bằng dẫn chiếu tới mục của bản đăng ký hoặc của Online Resource 1; với "(the PI)", chỉ đổi thành vị trí tác giả khi điều đó đúng.
5. **Số bảng không theo thứ tự.** Vị trí: Table 7 ở Mục 6.5 đứng trước Table 6 ở Mục 6.7. Đề xuất: đánh số lại.
6. **Mục 5.3 nói mọi bước chạy trong một ngày trên một máy.** Vị trí: Mục 5.3 so với Mục 6.7 và Table E5. Đề xuất: thêm một câu rằng phép phân tích phần con người chạy ngày 2026-11-15 trên một máy thuê khác, sau khi phần chấm đóng.
7. **Số ảnh đủ điều kiện ở Table 6.** Vị trí: hàng "Eligible images" (266 và 558) so với Mục 5.5 (215 và 298 sau khi để riêng). Đề xuất: thêm chú thích hoặc in cả hai.
8. **Các tuyên bố còn trống.** Vị trí: Statements and Declarations. Đề xuất: điền xét duyệt đạo đức, đồng ý tham gia, đồng ý công bố, giấy phép, DOI, đóng góp, lời cảm ơn; thêm mục "Materials availability".
9. **Trích dẫn chưa kiểm.** Vị trí: Mục 2, 4.4, 5.4, 5.5, 6.7; danh sách tài liệu cần thêm. Đề xuất: kiểm định danh của từng tài liệu trên trang gốc rồi mới thêm vào `paperB.bib`; đọc hai nguồn của nguyên lý giao–hợp trước khi trích; đọc lại phụ lục của công trình tiếng Việt gần nhất và thu hẹp các vế phủ định nếu cần.
10. **Cách viết chưa thống nhất.** Vị trí: "kappa" và κ; `f0` và "the reference front end"; 2,790 so với 1101 và 1123. Đề xuất: chọn một cách viết cho mỗi trường hợp, không đổi nội dung các câu đã cố định.
11. **Hình và bảng chưa dựng bằng tập lệnh.** Vị trí: Fig. 1, Fig. 2, Fig. 3, Fig. EF1; Table 6. Đề xuất: dựng hình vectơ theo đặc tả; sinh Table 6 từ tệp kết quả và so từng ô với bảng điền tay.

### B.27.2 Điểm nên làm rõ

1. Vai trò và trình độ của người chấm thứ hai, theo vai trò chứ không theo tên (Mục 5.5).
2. Một dòng xác nhận của chính người chấm thứ hai rằng người này trả lời một mình, không dùng công cụ tìm kiếm hay công cụ AI; chỉ khi có dòng này mới được viết "of the author and the rater" (Mục 6.7, Mục 8).
3. Một câu nối giữa bảo đảm phát biểu theo thành viên (Mục 4.4) và quy tắc phát biểu theo lớp (Mục 4.3).
4. Số 909 mang hai nghĩa ở Table 4 và Table 7; thêm ghi chú.
5. Kỳ vọng của bản đăng ký nêu ở cuối Mục 3 được nhìn lại ra sao.
6. Phạm vi của phần con người (ba thành viên; 33 tệp lời nhắc ngắn; một mô hình nền) nên được nhắc ở Mục 8.
7. Trường thời gian trên màn hình: một phép thử công cụ trên phiên giả lập, không mở tệp nhãn, để giải thích hai trung vị dưới một giây (mục 13 của E.6).
8. Mức phát hành các đánh giá của con người: giữ mặc định (chỉ tổng hợp) hay phát hành chi tiết hơn với sự đồng ý của người chấm.
9. Một đoạn công trình liên quan về các nghiên cứu thu thập ưu tiên của con người đối với chú thích ảnh (Mục 2).
10. Có thêm phần đối chiếu với dữ liệu tiếng Anh hay không, khi đối chứng đã đăng ký là "NOT RUN".

### B.27.3 Câu hỏi phản biện có thể gặp

1. Với P1 "INCONCLUSIVE" kèm "LOW-SENSITIVITY", P2 "NOT SUPPORTED" và phần con người không có nhãn, bài đóng góp điều gì ngoài một thủ tục?
2. FE-CERT khác gì một phân tích đa vũ trụ kèm một quy tắc quyết định?
3. Vì sao họ để dành chỉ có một bộ tách từ, và bộ ấy đã từng chạy trên tham chiếu?
4. Bootstrap phân vị có độ phủ thế nào trên các danh sách 100 và 279 ảnh?
5. Các ngưỡng của cổng cấu trúc được đặt sau khi nhìn giá trị cấu trúc; chúng có được chọn để giữ hay loại tệp nào không?
6. Vì sao 20 trong 22 phép chấm lần đầu đến từ một kho, và kết luận về P2 có còn nghĩa khi $n_{FL}$ đúng bằng mức tối thiểu?
7. Vì sao đồng thuận giữa hai người chấm thấp, và vì sao đồng thuận trong cùng người chấm của người chấm thứ hai chỉ là 0.567?
8. Một người chấm là tác giả và biết giả thuyết; hàng dấu câu của riêng người này (p một phía = 0.065) có ý nghĩa gì? Câu trả lời đúng: không có nhãn, không được nêu riêng.
9. Không người chấm nào luyện tập, người chấm thứ hai chấm trên máy của tác giả, và không bên thứ ba nào quan sát; điều gì bảo đảm tính độc lập? Câu trả lời đúng: lời khẳng định của tác giả, được công bố đúng như thế.
10. Trung vị thời gian trên màn hình dưới một giây nghĩa là gì? Câu trả lời đúng hiện nay: chưa được giải thích; không được dùng.
11. Vì sao không chấm lại hoặc thêm người chấm thứ ba? Câu trả lời đúng: quy tắc đã được cố định trước; mọi phương án như vậy là một nghiên cứu mới.
12. Các bản đăng ký không nằm ở một cơ quan đăng ký bên ngoài và các nhãn chỉ qua một lượt đọc nội bộ; điều gì cho phép bên ngoài kiểm lại?

## B.28 Thuật ngữ và ký hiệu của bản thảo viết lại

**Bảng B.39.** Thuật ngữ và ký hiệu thêm của bản thảo viết lại, kèm thuật ngữ tiếng Việt dùng ở B.14 đến B.27. Các thuật ngữ đã có ở Bảng B.28 không lặp lại, trừ κ, nay mang nghĩa khác.

| Tiếng Anh | Tiếng Việt | Nghĩa trong bài |
|---|---|---|
| (text) front end | khâu xử lý văn bản đầu vào, khâu xử lý | dãy bước cố định áp lên chú thích trước khi đếm n-gram: chuẩn hoá, vị trí dấu thanh, dấu câu, đơn vị, chữ hoa |
| family of admissible front ends, $F$ | họ khâu xử lý chấp nhận được | tập 72 thành viên được liệt kê theo quy tắc chấp nhận |
| member | thành viên | một mức cho mỗi trục T, P, U, C |
| development family, $F_{dev}$ | họ phát triển | 54 thành viên của ba đơn vị đã từng chạy trên đầu ra hệ thống |
| held-out family, $F_{held}$; HELD-OUT FRONT END | họ để dành; thành viên để dành | 18 thành viên của underthesea; "để dành" nói về thành viên, không nói về dữ liệu |
| reference member, `f0` | thành viên tham chiếu | RDRSegmenter, dấu thanh như được viết, giữ dấu câu, quy về chữ thường |
| class | lớp | các thành viên cho dãy token giống hệt nhau trên một phép so sánh |
| comparison | phép so sánh | một cặp tệp đầu ra trên một danh sách ảnh với một tệp tham chiếu |
| $D_f$, $L_f$, $U_f$ | giữ nguyên | hiệu CIDEr-D trung bình dưới thành viên $f$ và hai đầu khoảng bootstrap 95%, công thức (B.8) và (B.9) |
| CERTIFIED | giữ nguyên | có ý nghĩa cùng một chiều dưới mọi lớp của họ |
| FRAGILE; REVERSED | giữ nguyên | không được chứng nhận nhưng có ý nghĩa dưới ít nhất một thành viên; có ý nghĩa theo hai chiều trái nhau |
| NULL-STABLE | giữ nguyên | không có ý nghĩa dưới thành viên nào |
| CHANGED | giữ nguyên | có ý nghĩa dưới `f0` và không CERTIFIED trên họ đang xét |
| breaking set | tập phá vỡ | các lớp mà dưới đó chiều danh nghĩa không có ý nghĩa |
| point-sign flip | lật dấu điểm ước lượng | hai lớp có dấu của $D_f$ trái nhau; không có phán quyết |
| certificate | chứng nhận | phán quyết CERTIFIED cho một phép so sánh trên một họ |
| break | lần vỡ | một chiều đã chứng nhận không có ý nghĩa dưới ít nhất một lớp để dành |
| verdict set $V$; $N$ | tập phán quyết | các chứng nhận sát biên trên $F_{dev}$ dùng cho P1; $N$ là cỡ của nó |
| near-margin; $z_{\min}$ | sát biên | biên chuẩn hoá nhỏ nhất không quá 4, công thức (B.11) |
| $r$; $r_{NC}$ | giữ nguyên | tỉ lệ vỡ của P1; tỉ lệ vỡ của đối chứng độ nhạy |
| sensitivity control; LOW-SENSITIVITY | đối chứng độ nhạy | phép kiểm cùng quy tắc dựng từ các đơn vị phát triển; nhãn gắn thêm cho P1 khi $r_{NC}$ không quá 0.05 |
| first-look pool (FL); FIRST SCORING OF RELEASED OUTPUTS | tập chấm lần đầu | đầu ra do nhóm khác công bố, được đề tài chấm lần đầu |
| structure gate | cổng cấu trúc | các quy tắc cơ học nhận tệp của nhóm khác, không dùng điểm |
| kill gate | cổng dừng | điều kiện đã đăng ký làm đổi cách báo cáo một dự đoán |
| human arm | phần đánh giá của con người, phần con người | nghiên cứu ưu tiên theo cặp với hai người chấm |
| stratum (P, U, C) | tầng | ba nhóm cặp: lật theo dấu câu, lật theo đơn vị, đối chứng |
| decisive pair | cặp quyết định | cặp mà cả hai người chấm ưa cùng một chú thích |
| consensus share, $q_P$, $q_U$ | tỉ lệ đồng thuận | tỉ lệ cặp quyết định khớp với thứ tự của thành viên đang xét, công thức (B.13) |
| hidden repeat | lần lặp ẩn | cặp được cho xem lần hai với hai bên đổi chỗ |
| inter-rater agreement; Cohen's κ | đồng thuận giữa hai người chấm; κ của Cohen | ở B.14 đến B.27, κ là hệ số đồng thuận của Cohen, khác với κ ở Bảng B.28 |
| within-rater agreement | đồng thuận trong cùng người chấm | mức lặp lại câu trả lời trên các lần lặp ẩn; không phải cổng |
| author rater; non-author rater | người chấm là tác giả; người chấm không phải tác giả | hai người chấm của phần con người |
| "low inter-rater agreement" | giữ nguyên | cụm từ đã đăng ký cho dải κ từ 0.20 đến dưới 0.40; hai giả thuyết không mang nhãn |
| display normalisation | chuẩn hoá hiển thị | bỏ dấu câu cuối và viết hoa chữ đầu trước khi cho người chấm xem |
| intersection–union principle | nguyên lý giao–hợp | cơ sở của bảo đảm danh nghĩa ở Mục 4.4 |
