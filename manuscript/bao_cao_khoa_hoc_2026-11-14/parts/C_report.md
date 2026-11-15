# Phần C. Ví dụ truy hồi hay ví dụ ngẫu nhiên? Sinh chú thích ảnh theo ngữ cảnh có tiền đăng ký cho tiếng Việt và tiếng Anh (Retrieved or Random Examples? Preregistered In-Context Captioning in Vietnamese and English)

## C.1 Thông tin chung

**Tên bài và tạp chí đích.** Bài báo có tên tiếng Anh "Retrieved or Random Examples? Preregistered In-Context Captioning in Vietnamese and English" (11 từ theo ghi chú đầu tệp `00_abstract.md`). Tạp chí đích là ACM Transactions on Asian and Low-Resource Language Information Processing (ACM TALLIP). Thư mục bài báo ghi lại các giới hạn sau của tạp chí: tên bài không quá 12 từ; tóm tắt 150–200 từ, không dùng ngôi thứ nhất, không trích dẫn và phải nêu trọng tâm thực tiễn (ghi chú đầu `00_abstract.md` và `V2_PROGRESS_C.md`); bản thảo soạn bằng lớp `acmart` ở chế độ `manuscript`, trích dẫn kiểu tác giả–năm; hình cần độ phân giải từ 600 dpi trở lên kèm mô tả; bài thuộc loại "Long paper" (từ 13 trang trở lên, không ghi nhận giới hạn trên). Cũng theo `V2_PROGRESS_C.md`, tạp chí mong đợi thống kê kiểm định kèm giá trị p, trong khi bài dùng quy tắc dựa trên khoảng tin cậy; chế độ ẩn danh của vòng phản biện chưa được xác định trong hồ sơ; khối tác giả, ORCID và mã CCS còn phải hoàn tất. Bản thảo hiện ở dạng ẩn danh.

**Loại bài.** Đây là bài nghiên cứu thực nghiệm dạng phân tích. Bài tự xác định rằng nó không đề xuất phương pháp mới: "The study proposes no new method. It is a registered evaluation of when retrieved in-context examples help, and its contributions are of that kind." (Mục 1).

**Điều bài báo khẳng định.** Sinh chú thích theo ngữ cảnh có truy hồi (retrieval in-context captioning) đưa vào lời nhắc của một mô hình ngôn ngữ lớn đa phương thức (MLLM) các chú thích của những ảnh trong bộ nhớ giống ảnh truy vấn, và không cần huấn luyện. Bài hỏi: mức tăng so với lời nhắc không ví dụ (zero-shot) phản ánh tác dụng của việc truy hồi, hay chỉ phản ánh việc mô hình được thấy văn phong chú thích trong miền? Để trả lời, bài so sánh nhánh truy hồi `ret` với nhánh `rand` (cùng số k chú thích, rút ngẫu nhiên từ cùng bộ nhớ), báo cáo riêng từng mô hình nền (backbone), theo thiết kế tiền đăng ký với một lần nhìn (one look) cho mỗi tập kiểm tra. Trên OpenViIC test (1,941 ảnh), `ret` hơn `rand` +4.49 [3.52, 5.57] điểm CIDEr-D đã lược dấu câu cuối (stripped CIDEr-D), gộp hai mô hình nền, phán quyết đăng ký "PASS"; mức tăng do Qwen2.5-VL mang là chính và không được phát hiện ở InternVL3. Trên XM3600 tiếng Việt, mức tăng không được phát hiện (+0.70 [−0.45, 1.97]; "FAIL", khoảng tin cậy chứa 0). Với cấu hình đóng băng mang sang tiếng Anh, COCO Karpathy test lặp lại một mẫu hình đã biết (+3.08 [2.08, 4.03] điểm PTB CIDEr-D; "PASS"); trên NoCaps val, điểm ước lượng +1.73 [0.94, 2.50] nằm dưới ngưỡng đăng ký +2.0 ("FAIL"). Trên Flickr30K test, lời nhắc có truy hồi cao hơn một cài đặt lại của LMCap từ +28.77 đến +37.87 điểm PTB CIDEr-D với ba mô hình nền, nhưng phần lớn khoảng cách của InternVL3 đã có sẵn ở chế độ không ví dụ. Câu kết của tóm tắt giữ mức thận trọng: "The focus is empirical and practical: crediting a gain to retrieval requires an equal-k random control and per-backbone results."

**Các đóng góp như bài nêu (Mục 1).**

1. Một thiết kế đánh giá có đăng ký cho ngôn ngữ ít tài nguyên: so sánh ví dụ truy hồi, ngẫu nhiên, cố định và không ví dụ cho chú thích ảnh tiếng Việt với MLLM không huấn luyện, ví dụ chỉ ở dạng văn bản, bộ nhớ tiếng Việt trong miền; đối chứng ngẫu nhiên rút cùng k từ cùng bộ nhớ nên mức tăng so với không ví dụ tách thành phần truy hồi và phần văn phong trong miền; mọi hàng báo cáo theo từng mô hình nền; mỗi tập kiểm tra chỉ được nhìn một lần theo quy tắc cố định trước.
2. Kết quả trong miền ở hai ngôn ngữ: dự đoán chính qua trên OpenViIC test (P1) và COCO Karpathy test (P1-EN); ở cả hai ngôn ngữ mức tăng do Qwen2.5-VL mang là chính; với InternVL3, mức tăng không được phát hiện trên OpenViIC test và hàng COCO (hàng báo cáo, không đăng ký) nằm dưới 0; trên OpenViIC test không mô hình nào mất độ chính xác đối tượng so khớp số lượng so với chú thích không ví dụ của chính nó quá sàn đã đăng ký.
3. Ngoài nguồn của bộ nhớ: mức tăng không được phát hiện trên XM3600 tiếng Việt (XM-a "FAIL"); trên NoCaps val khoảng tin cậy nằm trên 0 nhưng điểm ước lượng dưới SESOI (S-NC "FAIL"); bài không khẳng định sự chuyển giao.
4. Một đường cơ sở trên cùng dữ liệu, kèm phân rã: trên Flickr30K Karpathy test (1,000 ảnh, một lần nhìn), lời nhắc có truy hồi cao hơn LMCap cài đặt lại với cả ba mô hình nền (ba khẳng định kiểm tra có đăng ký, kiểm soát bằng Holm); các hàng không ví dụ cho thấy bao nhiêu phần khoảng cách không cần ví dụ; hai tương phản truy hồi–ngẫu nhiên trên Flickr30K qua diễn tập nhưng thiếu biên đăng ký nên không được đưa lên kiểm tra và chỉ là hàng phát triển.
5. Một hồ sơ đầy đủ: mọi hàng đăng ký, mọi sai lệch và mọi tiếp xúc với dữ liệu kiểm tra đều được báo cáo, kể cả thất bại; điểm số, mã ảnh, mã băm, bản đăng ký và mã nguồn sẽ được công bố, còn chú thích và sổ điểm từng ảnh thì không.

**Bản đồ mục của bài báo.** Mục 1 mở đầu; Mục 2 công trình liên quan; Mục 3 phương pháp; Mục 4 dữ liệu và cách chia; Mục 5 tiền đăng ký và kế hoạch phân tích; Mục 6 kết quả tiếng Việt (6.1–6.7 là kết quả kiểm tra có đăng ký, 6.8 là chẩn đoán trên tập phát triển, 6.9 là chẩn đoán thăm dò, 6.10 là nghiên cứu phân bổ trên tập phát triển, 6.11 là chi phí tính toán); Mục 7 các công bố minh bạch; Mục 8 so sánh tiếng Anh (gồm so sánh Flickr30K ở 8.6); Mục 9 hạn chế và các mối đe doạ tính giá trị; Mục 10 kết luận; Phụ lục S chứa mọi hàng đăng ký theo từng lượt chạy và các chi tiết công bố.

**Ba mức bằng chứng cần giữ tách bạch.** Bài báo dùng nhiều lớp nhãn; báo cáo này giữ nguyên các nhãn ấy và sắp chúng thành Bảng C.1 để người đọc đối chiếu trong suốt Phần C.

**Bảng C.1.** Các mức bằng chứng và nhãn mà bài báo dùng (tổng hợp từ Mục 5, 6, 8 và Phụ lục S; không có số liệu mới).

| Mức | Nội dung | Dữ liệu | Nhãn trong bài | Được phép kết luận |
|---|---|---|---|---|
| 1. Xác nhận có đăng ký, tiếng Việt | P1, P1b, P2 (OpenViIC test); XM-a, XM-b (XM-test2500) | tập kiểm tra, mỗi tập nhìn một lần | "PASS", "FAIL", "confirmed", "not confirmed" | phán quyết theo quy tắc cố định trước |
| 2. So sánh tiếng Anh (các đăng ký riêng) | P1-EN (COCO), S-NC (NoCaps), E3a–c (Flickr30K test) | tập kiểm tra, mỗi tập nhìn một lần | "PASS", "FAIL" | chỉ trong phạm vi tiếng Anh; không tính hiệu số giữa hai ngôn ngữ |
| 3. Phân tích trên tập phát triển | các ablation AB-τ, AB-K, AB-M (Mục 6.8); nghiên cứu phân bổ C-ATTR-DEV (Mục 6.10); hàng diễn tập E1, E2 | OV-dev-A, OV-dev-B, XM-dev500, Flickr30K carve và val | "development, non-confirmatory"; "HOLDS"; "DETECTED", "NEGLIGIBLE", "REVERSED", "UNRESOLVED" | không đổi phán quyết nào; không vào tóm tắt hay danh sách đóng góp |
| Hàng báo cáo, không có quy tắc | hàng theo từng mô hình nền, theo miền, so với `zs` | như tập tương ứng | "reported row", "detected"/"not detected" (chữ thường) | chỉ mô tả, khoảng tin cậy không hiệu chỉnh |
| Hàng hậu nghiệm và thăm dò | bỏ các truy vấn bị gắn cờ; chẩn đoán lọc ví dụ (Mục 6.9); cận sao chép trên OV-dev-B | như ghi trong từng hàng | "POST HOC", "exploratory" | không có phán quyết |

## C.2 Mở đầu (Mục 1 của bài báo)

**Nội dung.** Mục mở đầu xuất phát từ quan sát rằng các MLLM mở có thể viết chú thích ảnh tiếng Việt mà không cần huấn luyện cho tác vụ, nhưng chú thích không ví dụ của chúng vẫn thấp xa các hệ thống tinh chỉnh trên KTVIC [@Pham2024KTVIC], UIT-OpenViIC [@Bui2023OpenViIC; @Bui2026OpenViICJournal] và phần tiếng Việt của XM3600 [@Thapliyal2022XM3600]. Bài dẫn một nghiên cứu đồng hành của cùng nhóm (nghiên cứu về chấm điểm, đang chuẩn bị) cho thấy quy ước của chú thích tham chiếu, chẳng hạn việc tham chiếu KTVIC không có dấu chấm cuối câu, làm CIDEr-D [@Vedantam2015CIDEr] thay đổi đáng kể; do đó một phần khoảng cách không ví dụ là chuyện khớp quy ước chứ không phải nội dung.

Bài lập luận vì sao chú thích ảnh tiếng Việt là bài toán ít tài nguyên: tiếng Việt có cộng đồng người nói lớn nhưng ít tài nguyên gán nhãn so với tiếng Anh [@Joshi2020StateFate]; các bộ dữ liệu miền chung ít và nhỏ, mỗi bộ có miền và văn phong tham chiếu riêng [@Lam2020UITViIC; @Pham2024KTVIC; @Bui2023OpenViIC; @Hoang2026HDUCap], các bộ khác chỉ nhắm một miền như y tế [@Nguyen2022VieCap4H] hay chữ trong cảnh [@Nguyen2026ViTextCaps]. Bộ nhớ mà nghiên cứu dựng từ hai bộ trong số đó có 10,501 ảnh, so với 112,255 ảnh của bộ nhớ tiếng Anh dựng từ riêng COCO; bài nói rõ không đưa ra khẳng định nào về cỡ bộ nhớ giữa hai ngôn ngữ. Các hệ đa ngữ vươn tới tiếng Việt thường dựa vào dữ liệu hoặc chú thích truy hồi dịch từ tiếng Anh [@Vu2025VELVET; @Ibrahim2025CONCAP; @Hussain2026SciRepLVLM], và văn bản tiếng Việt phải được tách từ trước khi chấm n-gram vì dấu cách ngăn âm tiết chứ không ngăn từ [@Vu2018VnCoreNLP]. Về thực tiễn, tinh chỉnh cần thời gian GPU, mã huấn luyện và giấy phép huấn luyện trên chú thích, còn lời nhắc có truy hồi dùng lại một tập huấn luyện đã có chú thích làm bộ nhớ, lúc suy luận, trên một GPU 24 GB. Nhưng nếu mức tăng đến từ việc cho mô hình xem bất kỳ chú thích trong miền nào, thì một lời nhắc rẻ hơn với ví dụ cố định hay ngẫu nhiên cũng đủ, và bộ nhớ từ miền khác có thể không giúp gì.

Bài định vị mình trong dòng công trình phân tích. Các bài phương pháp báo cáo mức tăng CIDEr lớn nhờ ví dụ truy hồi hoặc ví dụ chọn khéo [@Ramos2023LMCap; @Rebelo2025RSCap]; dòng phân tích hỏi vì sao ví dụ ngữ cảnh giúp được mô hình đa phương thức [@Yang2023ICLConfig; @Li2024RetrievalRobustness; @Baldassini2024MICL; @Chen2025TrueMICL; @Li2025UnveilingICL], phần lớn bằng tiếng Anh; MUNIChus [@Chen2026MUNIChus] so ví dụ ngẫu nhiên với ví dụ truy hồi theo độ tương tự ở cùng k trong chín ngôn ngữ không có tiếng Việt. Bài viết kèm rào đón: "As far as these papers state, none preregisters its contrasts or reports confidence intervals on the captioning score." OpenFlamingo [@Awadalla2023OpenFlamingo], dùng cách chọn ví dụ theo truy hồi [@Yang2022PICa] như Flamingo [@Alayrac2022Flamingo], báo cáo rằng ví dụ ảnh–chú thích truy hồi hơn ví dụ ngẫu nhiên trên COCO, còn trên Flickr-30K thì kém hơn ở 0, 4 và 8 ví dụ và chỉ hơn ở 32. Vì vậy nhánh tiếng Anh của bài là sự lặp lại một mẫu hình tiếng Anh đã biết dưới điều kiện khác (ví dụ chỉ là văn bản, cấu hình đóng băng, một lần nhìn), không phải phát hiện mới.

Câu hỏi nghiên cứu được phát biểu thành hai hiệu ứng: hiệu ứng của truy hồi (ví dụ mô tả ảnh tương tự) và hiệu ứng của việc thấy bất kỳ chú thích trong miền nào (ví dụ chỉ thể hiện văn phong của bộ dữ liệu). Đối chứng chính `rand` cho mô hình xem cùng số k chú thích từ cùng bộ nhớ, chọn ngẫu nhiên cho từng ảnh; đối chứng thứ hai `fix` dùng một bộ k chú thích cố định cho mọi ảnh; `zs` là lời nhắc không ví dụ. Nếu truy hồi chỉ giúp qua văn phong thì `ret` và `rand` phải cho điểm xấp xỉ nhau. Bài cũng theo dõi cái giá về độ trung thực: chú thích truy hồi mô tả ảnh khác, mô hình có thể chép đối tượng của chúng [@Li2024RetrievalRobustness]; do đó bài đăng ký dự đoán thứ hai về độ chính xác đối tượng so khớp số lượng (count-matched object precision), định nghĩa trong nghiên cứu đồng hành thứ hai, so số đối tượng được nhắc với chú thích không ví dụ của chính mô hình ở cùng số lần nhắc.

Nghiên cứu được tiền đăng ký theo ba giai đoạn, mỗi giai đoạn được cam kết trước khi dữ liệu của nó tới máy chủ GPU: (1) thăm dò trên tập phát triển A để chọn một cấu hình cho mỗi mô hình; (2) xác nhận một lần nhìn trên tập phát triển B với một cổng đã đăng ký; (3) kiểm tra một lần nhìn trên mỗi tập trong hai tập kiểm tra. Bản đăng ký kiểm tra cố định đại lượng ước lượng đích (estimand), cỡ hiệu ứng nhỏ nhất đáng quan tâm (SESOI, +2.0 điểm stripped CIDEr-D), quy tắc quyết định, cách diễn đạt cho từng kết cục và cách báo cáo thất bại. Một nhánh tiếng Anh đăng ký riêng mang cấu hình tiếng Việt đã đóng băng, với lời nhắc dịch và không tinh chỉnh cho tiếng Anh, sang COCO Karpathy test [@Lin2014COCO; @Karpathy2015Split] và NoCaps val [@Agrawal2019NoCaps]. Một đăng ký nữa, viết sau khi bốn tập kiểm tra ấy đã có quyết định, thêm so sánh trên cùng dữ liệu với LMCap [@Ramos2023LMCap] cài đặt lại trên cùng bộ nhớ và một mô hình nền thứ ba thuộc họ mô hình ngôn ngữ khác, Aya-Vision-8B [@Dash2025AyaVision], theo ba tầng: thăm dò trên một phần tách (carve) của Flickr30K train, một lần diễn tập (rehearsal) trên Flickr30K val và một lần nhìn Flickr30K Karpathy test [@Young2014Flickr30K; @Karpathy2015Split] cho các khẳng định qua diễn tập có biên. Kết quả hai ngôn ngữ được đặt cạnh nhau, mỗi bên trong ngôn ngữ và bộ chấm của mình, và không tính hiệu số xuyên ngôn ngữ.

**Nhận xét rà soát.** Mục mở đầu xác lập rõ câu hỏi và tự giới hạn đúng mức: bài nói thẳng nhánh tiếng Anh là sự lặp lại, và năm đóng góp đều thuộc loại "đánh giá có đăng ký". Có bốn điểm cần xử lý. Thứ nhất, đoạn bản đồ mục ở cuối `01_introduction.md` chỉ nhắc Mục 6.8 và Mục 6.9 như phần kết của Mục 6, trong khi `06_results.md` còn có Mục 6.10 (nghiên cứu phân bổ, dài nhất trong Mục 6) và Mục 6.11; người đọc gặp Mục 3.8 mà chưa được báo trước. Nên thêm một câu vào bản đồ mục và một câu báo trước rằng có một phân tích phát triển, không xác nhận, không thuộc đóng góp. Thứ hai, trạng thái hai nghiên cứu đồng hành không thống nhất giữa các tệp: `01_introduction.md` ghi "in preparation", còn `V2_PROGRESS_C.md` ghi cả hai "under review"; bộ chấm, bộ so khớp đối tượng và định nghĩa độ chính xác so khớp số lượng đều tựa vào hai bản thảo ấy, nên phản biện có thể đòi xem. Thứ ba, câu "none preregisters… or reports confidence intervals" được rào bằng "As far as these papers state" và phải giữ nguyên rào đón, vì Phụ lục S (phần "Literature search") thừa nhận việc tìm tài liệu chỉ là một phần. Thứ tư, đóng góp 2 nói không mô hình nào mất độ chính xác đối tượng "beyond the registered floor"; với InternVL3 cần nhắc kèm rằng 0.351 số chú thích `ret` đã lùi về chú thích không ví dụ, nên với các chú thích ấy hiệu số bằng 0 theo cấu trúc (Mục 3.5 có nói, Mục 1 và Mục 6.2 không nhắc lại).

## C.3 Công trình liên quan (Mục 2 của bài báo)

**Nội dung.** Mục 2 chia công trình trước thành hai loại. Bài phương pháp đề xuất một bộ sinh chú thích hoặc một quy trình lời nhắc và cho thấy nó đạt điểm cao (SmallCap, EXTRA, LMCap, MeaCap, EVCap, CONCAP và nghiên cứu viễn thám [@Rebelo2025RSCap]). Bài phân tích lấy mô hình sẵn có và hỏi vì sao, khi nào ví dụ ngữ cảnh có ích [@Yang2023ICLConfig; @Li2024RetrievalRobustness; @Baldassini2024MICL; @Chen2025TrueMICL; @Li2025UnveilingICL]. Bài tự xếp vào loại phân tích và định vị so với các bài phân tích.

Về truy hồi cho chú thích ảnh, bài lần lại ý tưởng mượn chú thích của ảnh huấn luyện giống nhất [@Devlin2015NN], là gốc của hai đường cơ sở `nn_top1` và `nn_cons`; các hệ điều kiện hoá bộ giải mã được huấn luyện trên chú thích truy hồi [@Ramos2023EXTRA; @Ramos2023SmallCap]; Re-ViLM [@Yang2023ReViLM]; các bộ sinh chú thích đọc văn bản truy hồi từ bộ nhớ ngoài [@Sarto2024RetrievalArch]; RAGCap [@Bazi2025RAGCap], đặt cặp ảnh–chú thích truy hồi bằng SigLIP vào lời nhắc của Qwen2-VL cho ảnh viễn thám; và ví dụ truy hồi cho phân loại bệnh [@Zhan2026RAICL]. Điểm then chốt là đối chứng chú thích ngẫu nhiên đã có tiền lệ với các bộ sinh chú thích được huấn luyện: EXTRA [@Ramos2023EXTRA] huấn luyện và đánh giá một biến thể mã hoá ảnh cùng một chú thích ngẫu nhiên từ kho, biến thể này thấp hơn mô hình truy hồi; Li và cộng sự [@Li2024RetrievalRobustness] đưa cho SmallCap, ở cùng k, các chú thích truy hồi cho ảnh khác và điểm tụt xuống dưới mô hình không truy hồi. Bài kết luận: "A random draw from the same memory is therefore an established control for trained retrieval-augmented captioners." Các hệ khác được phân biệt theo cách dùng bộ nhớ: LMCap [@Ramos2023LMCap] nhắc một mô hình ngôn ngữ chỉ văn bản bằng chú thích truy hồi xuyên ngôn ngữ; CONCAP [@Ibrahim2025CONCAP]; MeaCap [@Zeng2024MeaCap]; giải mã theo lý thuyết quyết định dựa trên ca [@Deguchi2025CBDT]; EVCap [@Li2024EVCap]; ViECap [@Fei2023ViECap]. Phát hiện rằng bộ sinh chú thích tăng cường truy hồi chép từ ngữ từ chú thích truy hồi và nhạy với thứ tự, cách chọn [@Li2024RetrievalRobustness] là động cơ cho các chẩn đoán sao chép (tỉ lệ chép 4-gram, tỉ lệ gần nguyên văn) và phân tích đối tượng chỉ-từ-láng-giềng (neighbour-only object).

Hai công trình gần nhất được nêu riêng: nghiên cứu chú thích đa ngữ không huấn luyện cho viễn thám [@Rebelo2025RSCap] và MUNIChus [@Chen2026MUNIChus], bộ đánh giá chú thích ảnh tin tức ở chín ngôn ngữ, so lời nhắc không ví dụ với ba ví dụ lấy ngẫu nhiên và ba ví dụ truy hồi theo độ tương tự cho bảy MLLM (gồm Qwen2.5-VL-7B và Aya-Vision-8B), báo cáo BLEU-4 và CIDEr dạng điểm số đơn và kết luận ba chiến lược cho kết quả lẫn lộn. Bài nêu năm khác biệt so với cả hai: ảnh đời thường với chú thích tiếng Việt; ví dụ chỉ là văn bản, không có ảnh ví dụ; một đối chứng ví dụ cố định bên cạnh đối chứng ngẫu nhiên, cùng k; khoảng tin cậy bootstrap ghép cặp cho mọi hàng, theo từng mô hình nền, cùng độ chính xác đối tượng so khớp số lượng; và kiểm tra một lần nhìn có tiền đăng ký.

Về cấu hình ngữ cảnh trong mô hình đa phương thức lớn, tiền lệ tiếng Anh gần nhất là OpenFlamingo [@Awadalla2023OpenFlamingo] với RICES [@Yang2022PICa]. Bài dẫn Bảng 9 trong phụ lục của công trình ấy (OpenFlamingo-9B): trên COCO ví dụ truy hồi hơn ngẫu nhiên +4.1 CIDEr ở 4 ví dụ và +9.5 ở 32 ví dụ; trên Flickr-30K thì kém hơn, −20.3 ở 0 ví dụ, −13.6 ở 4 ví dụ, −4.2 ở 8 ví dụ, và hơn +1.7 ở 32 ví dụ. Sự đảo chiều trên Flickr-30K cho thấy một mô hình có thể đạt điểm thấp hơn với ví dụ truy hồi so với ví dụ ngẫu nhiên, như InternVL3 trên COCO trong bài. Li và cộng sự [@Li2025UnveilingICL] quy mức tăng của ví dụ chọn theo độ tương tự cho việc chép chú thích ví dụ; tỉ lệ gần nguyên văn (Mục 6.4) và các hàng che n-gram của Bảng S19 nhìn vào cùng con đường ấy cho ví dụ văn bản. Hai phát hiện rằng học theo ngữ cảnh đa phương thức chủ yếu do văn bản ví dụ dẫn dắt [@Baldassini2024MICL] và rằng MLLM bắt chước văn bản ví dụ thay vì dùng nội dung thị giác [@Chen2025TrueMICL] là lý do cần đối chứng `rand`: mức tăng chỉ đến từ văn bản ví dụ sẽ xuất hiện ở cả `rand` lẫn `ret`. Các phương pháp gần đây về chọn ví dụ [@Allabadi2026GRIP; @Huang2026ReVisIT; @Lee2026LSD; @Thanh2026Adjudicated] và câu hỏi mô hình dùng ngữ cảnh đến đâu [@dosSantos2025ContextVLM] được nêu là ngoài phạm vi so sánh.

Về chú thích ảnh tiếng Việt, bài liệt kê UIT-ViIC, KTVIC, UIT-OpenViIC, HDUCap (15,000 ảnh cảnh tự nhiên, năm chú thích do người viết cho mỗi ảnh), tham chiếu tiếng Việt của XM3600, ViG [@Vu2026ViG], VELVET [@Vu2025VELVET] và công trình giảm ảo giác trong chú thích tiếng Việt chi tiết bằng tinh chỉnh [@Nguyen2026FAIR]; bài nói HDUCap không nằm trong các tập kiểm tra vì tập kiểm tra đã cố định trong đăng ký và trang phát hành không nêu giấy phép. Ngoài tiếng Việt có AfriCaption [@Oduwole2025AfriCaption] và một hệ dùng lời nhắc nhiều ví dụ có truy hồi cho ngôn ngữ bản địa châu Mỹ, báo cáo rằng truy hồi chỉ giúp khi kho trong miền lớn [@Dhawan2026Gators]. Về đo ảo giác đối tượng, CHAIR [@Rohrbach2018CHAIR] đếm đối tượng được nhắc mà nhãn vàng không ủng hộ; trên XM3600 bài chấm độ chính xác đã kiểm chứng theo nhãn Open Images do người xác minh [@Kuznetsova2020OpenImages]. Kiểm tra hậu kỳ bằng mô hình thứ hai là phổ biến [@Yin2023Woodpecker]; bài đã đăng ký một cơ chế chắn (guard) như vậy nhưng giả thuyết không qua ở tập phát triển và chỉ được báo cáo như một kết quả âm có đăng ký.

Bảng 1 của bài báo so thiết kế của các công trình gần nhất và của chính nghiên cứu (có huấn luyện hay không, mô hình có thấy ảnh không, nội dung truy hồi, ngôn ngữ, đối chứng ngẫu nhiên, thống kê); Bảng 1b đặt nghiên cứu giữa các bài phân tích và được tóm lược ở Bảng C.2.

**Bảng C.2.** Nghiên cứu giữa các bài phân tích về chú thích theo ngữ cảnh (rút gọn từ Bảng 1b, Mục 2; nội dung theo phát biểu của từng bài).

| Bài phân tích | Ngôn ngữ | Đối chứng ngẫu nhiên cùng k | Hàng theo từng mô hình nền | Đăng ký, một lần nhìn | Khoảng tin cậy trên điểm chú thích |
|---|---|---|---|---|---|
| [@Yang2023ICLConfig] | Anh | có, cùng số ví dụ | có | không | không |
| [@Li2024RetrievalRobustness] | Anh | có, cùng k | các cột bộ giải mã trong một bảng | không | không (trung bình ba hạt giống) |
| [@Baldassini2024MICL] | Anh | có, cùng số ví dụ (IDEFICS) | một phần | không | không |
| [@Chen2025TrueMICL] | Anh | không cho chú thích ảnh | có | không | không |
| [@Li2025UnveilingICL] | Anh | có, cùng số ví dụ | có | không | không |
| [@Chen2026MUNIChus] | chín ngôn ngữ, không có tiếng Việt | có, k = 3, ví dụ có ảnh và trích đoạn bài báo | có | – | không |
| nghiên cứu này | Việt, Anh | có, cùng k, cùng bộ nhớ | mọi hàng | có, năm tập kiểm tra, mỗi tập một lần nhìn | bootstrap ghép cặp; Holm cho họ Flickr30K |

Đoạn "Position among the analyses" nêu rõ những gì không mới: đối chứng ngẫu nhiên, quy tắc so khớp số lượng (từ nghiên cứu đồng hành) và tiền đăng ký một lần nhìn ("a reporting practice, not a contribution of this paper"). Bài chỉ nhận ba khác biệt: bối cảnh (tiếng Việt, MLLM không huấn luyện, ví dụ văn bản, bộ nhớ trong miền, lặp lại bằng tiếng Anh không tinh chỉnh lại); thiết kế (đối chứng cùng k từ cùng bộ nhớ, tách theo mô hình nền, một lần nhìn, in mọi thất bại); và một đường cơ sở trên cùng dữ liệu (LMCap cài đặt lại, kèm hàng không ví dụ), với câu giới hạn "the study does not claim that its prompt is a better method than LMCap". Câu chốt là: "We make no priority claim on retrieval in-context captioning, on the random control or on the registered design."

**Nhận xét rà soát.** Mục 2 trung thực về tính mới và đây là điểm mạnh khi gặp phản biện khắt khe, nhưng cũng làm lộ rằng đóng góp nằm ở bối cảnh và độ chặt của thiết kế chứ không ở ý tưởng; người viết lại cần giữ đúng mức này và không thêm chữ "đầu tiên" ở bất kỳ đâu. Các điểm cần sửa hoặc làm rõ như sau. (i) Hai hàng của Bảng 1 (RAGCap và công trình [@Sarto2024RetrievalArch]) được lập "from its abstract", để dấu "–" ở các cột ngôn ngữ, đối chứng và thống kê; trước khi nộp nên đọc toàn văn để điền hoặc ghi rõ lý do. (ii) Phụ lục S thừa nhận việc tìm tài liệu là một phần và OpenAlex, Semantic Scholar chưa được tìm có hệ thống; một phản biện trong lĩnh vực có thể nêu một công trình còn sót, nên cần một lượt tìm có hệ thống và ghi ngày tìm. (iii) Mục 2 nêu năm khác biệt so với hai công trình gần nhất nhưng ba khác biệt so với các bài phân tích; hai danh sách chồng lấn (ví dụ "đối chứng cố định" chỉ có trong danh sách năm), nên hợp nhất để tránh cảm giác đếm hai lần. (iv) Theo `V2_PROGRESS_C.md`, khoá [@Kuznetsova2020OpenImages] là bài về bản V4 trong khi văn bản dùng nhãn do người xác minh của bản V7; cần bổ sung nguồn cho bản V7. (v) Các con số của OpenFlamingo được dẫn từ một bảng phụ lục của bài ấy và là số của công trình khác; cần đối chiếu lại với bản in cuối của nguồn. (vi) Bài tự trích công trình trước của nhóm [@Nguyen2026FAIR] ở ngôi thứ ba; nếu vòng phản biện là ẩn danh hai chiều thì cách viết này phù hợp, nhưng chế độ ẩn danh của tạp chí còn để ngỏ trong hồ sơ. (vii) Tên "Bảng 1b" không theo lối đánh số thông thường của tạp chí; nên đổi thành một bảng có số riêng.

## C.4 Phương pháp (Mục 3 của bài báo)

**Nội dung.** Phương pháp gồm bốn phần: một bộ nhớ có chú thích (3.1), cách chọn ví dụ cho từng ảnh truy vấn (3.2), lời nhắc và bộ giải mã (3.3), và một bước xoá sau giải mã (3.4). Mục 3.5 nêu cấu hình mà các giai đoạn phát triển đã đóng băng, Mục 3.6 mô tả bộ chấm, Mục 3.7 hai nhánh thêm cho đăng ký Flickr30K, và Mục 3.8 các nhánh của nghiên cứu phân bổ trên tập phát triển.

### C.4.1 Bộ nhớ (Mục 3.1)

Bộ nhớ (memory) ghép các ảnh huấn luyện KTVIC nằm ngoài phần tách phát triển của KTVIC với các ảnh huấn luyện UIT-OpenViIC: 3,469 + 9,088 = 12,557 ứng viên, trong đó 3,469 là 3,769 ảnh của tệp huấn luyện KTVIC trừ đi phần tách phát triển 300 ảnh (KTVIC không có tập validation chính thức). Một bộ lọc định trước loại 2,056 ứng viên (bộ lọc cũng bỏ ảnh không đọc được), còn lại 10,501 ảnh. Bộ lọc bỏ một ảnh bộ nhớ khi nó trùng từng byte hoặc gần trùng với một ảnh của tập được bảo vệ: ảnh kiểm tra và phát triển của KTVIC, ảnh phát triển và kiểm tra của OpenViIC, và toàn bộ 3,600 ảnh XM3600; bộ lọc cũng bỏ ảnh có mã băm nằm trong một danh sách loại trừ cố định trước. Hai ảnh được coi là gần trùng khi giá trị nhỏ hơn trong hai khoảng cách pHash và dHash (trực tiếp hoặc lật gương) không quá 10 và cosine SSCD ít nhất 0.5. 10,501 ảnh được gom thành 8,190 cụm theo một quy tắc tương tự thị giác định trước trên mã băm tri giác và mô tả SSCD [@Pizzi2022SSCD]. Mỗi cụm chỉ được đưa ra nhiều nhất một lần cho mỗi truy vấn. Với truy vấn OpenViIC, chú thích được hiển thị là chú thích đầu tiên của thành viên OpenViIC trong cụm nếu có; ngược lại, và với mọi truy vấn XM3600, là chú thích đầu tiên của thành viên đầu tiên. Chú thích được đọc lúc chạy và chỉ đặt vào lời nhắc.

### C.4.2 Chọn ví dụ (Mục 3.2)

Ảnh được nhúng bằng tháp ảnh SigLIP2 [@Tschannen2025SigLIP2] (so400m, patch 14, 384 px; chuẩn hoá L2, fp16); bộ nhớ nhúng một đại diện cho mỗi cụm. Một cụm có cosine với truy vấn ≥ 0.92 không bao giờ được đưa cho truy vấn ấy ở bất kỳ nhánh nào; bài gọi đây là ngưỡng cắt cận của truy hồi (retrieval near cut). Ngưỡng cắt cận dùng độ tương tự SigLIP2, còn bộ lọc bộ nhớ dùng mã băm tri giác với SSCD; một quy tắc rộng hơn áp dụng hậu nghiệm sau kiểm tra vẫn gắn cờ 12 truy vấn của tập chính (Mục 6.2). Bốn nhánh (arm) được định nghĩa ở Bảng C.3.

**Bảng C.3.** Các nhánh và ví dụ được đưa cho truy vấn q (theo bảng ở Mục 3.2).

| Nhánh | Ví dụ đưa cho truy vấn q |
|---|---|
| `ret` | k cụm hợp lệ có cosine với q cao nhất; hoà thì xếp theo mã cụm |
| `rand` | k cụm hợp lệ rút cho q bởi một bộ sinh số có hạt giống lấy từ mã băm của tên tập và mã ảnh |
| `fix` | một bộ k cụm, rút một lần cho mỗi tập kiểm tra từ các cụm nằm dưới ngưỡng cắt cận đối với mọi ảnh của tập, đưa cho mọi ảnh |
| `zs` | không có ví dụ; cùng lời nhắc chú thích ngắn không ví dụ mà các bài đồng hành dùng |

Ở mọi nhánh, danh sách ví dụ ngắn hơn là tiền tố của danh sách 8 ví dụ. Ba nhánh `ret`, `rand`, `fix` dùng chung một khuôn lời nhắc và chỉ khác khối ví dụ. `nn_top1` và `nn_cons` không phải nhánh mô hình: chúng xuất thẳng một chú thích của bộ nhớ (chú thích của cụm gần nhất, hoặc chú thích đồng thuận trong k cụm gần nhất, với tần suất tài liệu lấy từ kho bộ nhớ) và không cần GPU.

### C.4.3 Lời nhắc và giải mã (Mục 3.3)

Lời nhắc đứng sau ảnh trong lượt người dùng của khuôn hội thoại riêng của mỗi mô hình và gồm ba phần: một tiêu đề tiếng Việt cố định nói rằng các chú thích bên dưới thuộc về ảnh khác, chỉ cho thấy cách viết và không mô tả ảnh cần chú thích; k dòng ví dụ có đánh số; và phần đuôi yêu cầu một câu tiếng Việt ngắn theo văn phong của ví dụ, không liệt kê, không giải thích. Đuôi T1 yêu cầu thêm rằng chỉ nêu những gì nhìn thấy; đuôi T2 bỏ câu đó. "Thứ tự" quy định vị trí của ví dụ giống nhất: `first` đặt nó đầu tiên, `last` đặt nó sát chỉ dẫn. Khuôn được viết riêng cho nghiên cứu, không chứa chú thích của bộ dữ liệu nào và được ghim bằng sha256 trong mã sẽ công bố (tiền tố `7478361a`). Giải mã là tham lam (một chùm, không lấy mẫu), tối đa 60 token mới, ở bf16, với ảnh chụp mô hình và thiết lập bộ xử lý đã ghim: Qwen2.5-VL-7B-Instruct và InternVL3-8B làm bộ sinh, Qwen3-VL-8B-Instruct làm mô hình kiểm chứng của InternVL3, cùng bộ nhúng SigLIP2. Mọi tệp ảnh chụp mô hình và môi trường ảo được ghim bằng mã băm, không đổi từ giai đoạn A.

### C.4.4 Đối tượng chỉ-từ-láng-giềng và bước xoá (Mục 3.4)

Một lớp đối tượng o trong chú thích là đối tượng chỉ-từ-láng-giềng (neighbour-only) khi thoả ba điều kiện: bộ so khớp đối tượng tìm thấy o trong chú thích; o vắng trong chú thích không ví dụ của chính mô hình ấy cho ảnh; và o xuất hiện trong ít nhất một ví dụ được đưa kèm ảnh. Mỗi lớp như vậy có thể được đưa cho một mô hình kiểm chứng (verifier), mô hình này trả lời một câu hỏi có/không bằng tiếng Anh về lớp đó. Với p là xác suất đã chuẩn hoá của "yes" tại vị trí trả lời, điểm kiểm chứng là

$$s = p(\text{có ảnh}) - p(\text{chỉ câu hỏi}) \tag{C.1}$$

và lớp bị bác khi $s < \tau$, với τ là ngưỡng xoá. Các lớp bị bác được gỡ theo quy tắc cố định: cắt chú thích tại dấu phẩy, chấm phẩy, liên từ và từ chỉ vị trí; bỏ mỗi đơn vị có nêu một lớp bị bác rồi nối phần còn lại; và lùi về chú thích không ví dụ của mô hình (fallback) khi đơn vị chủ ngữ bị chạm hoặc kết quả sai dạng. Ở τ = −∞ không lớp nào bị bác và chú thích giữ nguyên. Khác với Negative Entity Suppression [@Lu2025NES], bước này tác động sau giải mã, trên chú thích của chính mô hình, và chỉ trên các lớp do ví dụ đưa vào. Mô hình kiểm chứng của mỗi bộ sinh là một VLM khác: với InternVL3-8B là Qwen3-VL-8B-Instruct, với Qwen2.5-VL-7B là InternVL3-8B. Bài nêu rõ dòng dõi có phần chung: mô hình ngôn ngữ của InternVL3-8B là Qwen2.5-7B, và Qwen3-VL thuộc dòng Qwen. Một lượt chạy dừng nếu, trên 20 câu hỏi đầu, trung vị khối xác suất dồn vào "yes" và "no" dưới 0.5, vì khi đó vị trí được đọc không phải vị trí trả lời.

### C.4.5 Cấu hình đóng băng (Mục 3.5)

Giai đoạn phát triển A chọn một cấu hình cho mỗi mô hình nền trên phần tách phát triển KTVIC 299 ảnh. Quy tắc chọn cấu hình có stripped CIDEr-D cao nhất trong các ứng viên thoả ba điều kiện: ΔP_cm so với không ví dụ ít nhất −1.0; tỉ lệ sao chép gần nguyên văn không quá 0.05; tỉ lệ hit-max không quá 0.02. Phạm vi tìm gồm 7 lượt `ret` cho mỗi mô hình nền (k ∈ {2, 4, 8} × hai thứ tự với đuôi T1, cộng k = 4, `last`, đuôi T2), mỗi lượt chấm ở τ ∈ {−∞, 0.0, 0.1, 0.2, 0.3, +∞}. Các cấu hình này sau đó đi tiếp trên nửa A của tập phát triển OpenViIC và qua một cổng đã đăng ký trên tập phát triển B; không gì được thay đổi cho kiểm tra.

**Bảng C.4.** Cấu hình đóng băng, không đổi từ các giai đoạn phát triển (Bảng 2, Mục 3.5).

| | Qwen2.5-VL-7B | InternVL3-8B |
|---|---|---|
| k | 8 | 4 |
| thứ tự | first | last |
| đuôi lời nhắc | T1 | T2 |
| ngưỡng xoá τ | −∞ (không xoá) | 0.10 |
| mô hình kiểm chứng lúc kiểm tra | không | Qwen3-VL-8B-Instruct |

Ở τ đóng băng của mình, chú thích `ret`, `rand` và `fix` của InternVL3 đi qua bước xoá trước khi chấm; chú thích của Qwen2.5-VL được chấm như lúc giải mã. Bước xoá vì thế là một phần của đại lượng ước lượng đích đã đăng ký của InternVL3. Nó được giữ lại sau khi giả thuyết về cơ chế chắn thất bại ở giai đoạn B, vì quy tắc giai đoạn A đã chọn τ = 0.10 dưới ràng buộc ΔP_cm và không gì được chọn lại sau đó. Trên OV-test, 0.351 số chú thích `ret` của InternVL3 lùi về chú thích không ví dụ (Bảng S1); với các chú thích ấy ΔP_cm so với `zs` bằng 0 theo cấu trúc.

### C.4.6 Chấm điểm (Mục 3.6)

Mọi nhánh được chấm bằng bộ công cụ của nghiên cứu đồng hành về chấm điểm, nạp theo mã băm. Chú thích ứng viên và tham chiếu được tách từ bằng RDRSegmenter [@Nguyen2018VnCoreNLP] (VnCoreNLP 1.2 [@Vu2018VnCoreNLP]) và chuyển chữ thường, nên n-gram của CIDEr-D là trên token từ. Độ dài chú thích (quy tắc L) tính theo âm tiết, tức đơn vị ngăn bởi dấu cách trước khi tách từ. CIDEr-D (×100) dùng tần suất tài liệu (document frequency) tính trên chính các tham chiếu của tập được chấm. Cột quyết định là stripped CIDEr-D: token dấu câu ở cuối bị bỏ khỏi ứng viên và tham chiếu, để không nhánh nào được lợi chỉ nhờ một dấu chấm cuối; cột nguyên trạng (as-written) và cột tách token kiểu PTB cũng được báo cáo. Bộ so khớp đối tượng là bộ so khớp chuẩn hoá dấu thanh của nghiên cứu đồng hành về độ chính xác đối tượng. CHAIR_i và độ chính xác so khớp số lượng dùng hợp các tham chiếu của ảnh làm nhãn vàng. Độ chính xác đã kiểm chứng trên XM3600 được chấm ngoại tuyến theo nhãn Open Images do người xác minh, và các nhãn này không bao giờ tới máy chủ GPU.

### C.4.7 Các nhánh thêm cho đăng ký Flickr30K (Mục 3.7)

Đăng ký Flickr30K thêm hai nhánh tiếng Anh. Aya-Vision-8B [@Dash2025AyaVision] là mô hình nền thứ ba, thuộc họ mô hình ngôn ngữ khác; cấu hình của nó (k = 4, ví dụ đặt cuối, đuôi T1) được chọn trên tập phát triển tiếng Việt theo quy tắc giai đoạn A với τ cố định ở −∞, mang sang tiếng Anh không tinh chỉnh và chạy không có bước xoá. LMCap được cài đặt lại theo công thức đã công bố [@Ramos2023LMCap]: truy hồi ảnh–chú thích bằng CLIP đa ngữ [@Carlsson2022MCLIP] lấy K = 4 chú thích, N = 3 minh hoạ cố định, XGLM-2.9B [@Lin2022XGLM] với chùm 3, và xếp hạng lại ba ứng viên bằng CLIP đa ngữ. Bài công bố bốn sai khác so với bài gốc: kho chỉ giữ một chú thích hiển thị cho mỗi cụm bộ nhớ thay vì mọi chú thích; ngưỡng cắt cận (cosine SigLIP2 ≥ 0.92) cũng loại các láng giềng gần nhất của LMCap; việc sinh dừng ở 40 token mới, giá trị bài gốc không nêu; và XGLM chạy ở fp16. Mã đã công bố không có tệp giấy phép nên phương pháp được cài đặt lại từ bài báo; hàng kết quả đo bản cài đặt lại này, không đo hệ thống đã công bố.

### C.4.8 Các nhánh và đại lượng của nghiên cứu phân bổ, chỉ trên dữ liệu phát triển (Mục 3.8)

Tương phản đăng ký `ret` − `rand` cho biết ví dụ truy hồi có hơn ví dụ ngẫu nhiên hay không, nhưng không cho biết vì sao. Một danh sách truy hồi khác một danh sách ngẫu nhiên ở hai điểm cùng lúc: nó hợp với chính ảnh này, và nó thuộc kiểu danh sách mà truy hồi tạo ra cho bất kỳ ảnh nào (chú thích của cảnh gần điển hình, độ dài và cách dùng từ tương tự). Một nghiên cứu phát triển về sau, đăng ký riêng và mang nhãn "development, non-confirmatory", tách tương phản thành hai phần ấy bằng một nhánh thêm, và đặt cận cho phần mức tăng có thể đi qua các n-gram chép từ chú thích được đưa. Nghiên cứu chỉ dùng tập phát triển và không đổi kết quả đăng ký nào.

**Nhánh hoán vị.** Trong `perm`, ảnh q được cho xem danh sách truy hồi của một ảnh khác cùng tập. Các ảnh của tập, theo thứ tự trong danh mục, được hoán vị bằng một hoán vị vòng $\pi_p$ không có điểm bất động, dựng bằng thuật toán Sattolo [@Sattolo1986] từ bộ sinh số có hạt giống là tên tập và chỉ số hoán vị p, nên $\pi_p$ không phụ thuộc nội dung ảnh hay bất kỳ đầu ra nào. Ảnh q nhận bảng xếp hạng hợp lệ của ảnh cho $q' = \pi_p(q)$ và giữ k cụm đầu có cosine với q cũng dưới 0.92; khi ngưỡng cắt cận của q loại một trong tám cụm đầu của ảnh cho, danh sách được bù từ phía dưới bảng xếp hạng. Quy tắc thứ tự, đuôi lời nhắc và k là của nhánh `ret` của mô hình nền. Dùng hai hoán vị (p = 1, 2). Nếu hơn 10% trong tám vị trí của một tập phải bù thì `perm` trên tập ấy chỉ là chẩn đoán không có quy tắc; tỉ lệ bù được tính trước mọi lượt giải mã (Bảng S26).

**Nhánh, số lần rút và mô hình nền.** `rand` được rút R lần cho mỗi ảnh, lần rút d có hạt giống là tên tập, mã ảnh và d; `perm` được dựng D = 2 lần. R = 3 trên OV-dev-B và XM-dev500, R = 1 trên OV-dev-A. Các bộ `fix` f1–f4 được thêm trên OV-dev-B và XM-dev500 cho Qwen2.5-VL-7B. Mọi nhánh của một mô hình nền dùng chung khuôn lời nhắc, k, quy tắc thứ tự và bộ giải mã, chỉ khác khối ví dụ; mã kiểm tra rằng mã băm lời nhắc của hai nhánh chỉ khác qua khối đó. Ba mô hình nền là Qwen2.5-VL-7B và InternVL3-8B ở cấu hình Bảng C.4 và Aya-Vision-8B ở cấu hình Mục 3.7. InternVL3-8B chạy không có bước xoá (τ = −∞, không mô hình kiểm chứng) ở mọi nhánh của nghiên cứu này, vì việc lùi về chú thích không ví dụ sẽ biến `perm` thành hỗn hợp của hai nhánh; các hàng đăng ký ở τ = 0.10 không bị đụng tới. Qwen2.5-VL-7B và InternVL3-8B chung dòng mô hình ngôn ngữ Qwen2.5; mô hình ngôn ngữ của Aya-Vision-8B là Command R7B.

**Đại lượng ước lượng đích.** Với một mô hình nền ở cấu hình của nó, một tập và ảnh i, gọi $s_i(a)$ là stripped CIDEr-D của nhánh a; với `rand` và `perm`, $s_i$ là trung bình trên R lần rút hoặc D hoán vị của ảnh. Khi đó

$$\tau_{\text{any}} = \operatorname{mean}_i\,[s_i(\texttt{rand}) - s_i(\texttt{zs})],\qquad \tau_{\text{sel}} = \operatorname{mean}_i\,[s_i(\texttt{ret}) - s_i(\texttt{rand})], \tag{C.2}$$

$$\tau_{\text{marg}} = \operatorname{mean}_i\,[s_i(\texttt{perm}) - s_i(\texttt{rand})],\qquad \tau_{\text{pair}} = \operatorname{mean}_i\,[s_i(\texttt{ret}) - s_i(\texttt{perm})]. \tag{C.3}$$

$\tau_{\text{any}}$ là mức tăng do thấy bất kỳ chú thích trong miền nào; $\tau_{\text{sel}}$ là tương phản truy hồi đã đăng ký, theo từng mô hình nền; $\tau_{\text{marg}}$ là phần mà bất kỳ danh sách kiểu truy hồi nào cũng đem lại, dù nó được truy hồi cho ảnh nào; $\tau_{\text{pair}}$ là phần cần danh sách được truy hồi cho chính ảnh này. Theo từng ảnh,

$$\texttt{ret} - \texttt{zs} = \tau_{\text{any}} + \tau_{\text{marg}} + \tau_{\text{pair}},\qquad \tau_{\text{sel}} = \tau_{\text{marg}} + \tau_{\text{pair}} \tag{C.4}$$

đúng chính xác. Không đại lượng nào được gộp qua các mô hình nền. Bài lưu ý: τ có chỉ số dưới là đại lượng ước lượng, còn τ đứng riêng vẫn là ngưỡng xoá của Mục 3.4.

**Cận sao chép (copy bound).** Với chú thích y và danh sách S các chú thích được đưa, $\text{masked}_n(y, S)$ bỏ khỏi y mọi token nằm trong một n-gram cũng có mặt trong một chú thích của S. Mất mát là $\text{loss}(y; S) = s(y) - s(\text{masked}_n(y, S))$ với cùng tham chiếu và tần suất tài liệu; tham chiếu không bao giờ bị che. Token được đếm theo hai đơn vị: (i) âm tiết và (ii) từ sau khi tách bằng RDRSegmenter. n = 3 là giá trị quyết định; n = 2 và n = 4 là hàng độ nhạy. Với ảnh q và $R_q$ là k chú thích đưa cho q trong `ret`,

$$\kappa_q = \text{loss}(y_{\text{ret},q}; R_q) - \text{loss}(y_{\text{zs},q}; R_q). \tag{C.5}$$

Chú thích không ví dụ được viết khi không có $R_q$, nên mất mát của nó so với $R_q$ đo phần trùng không cần sao chép (một giả dược, placebo). Từ đó

$$K_{\text{ret}} = \operatorname{mean}_q \kappa_q,\qquad L_{\text{cp}} = \operatorname{mean}_q\,[(s_q(\texttt{ret}) - s_q(\texttt{rand})) - \kappa_q], \tag{C.6}$$

trong đó $K_{\text{ret}}$ là cận trên của phần `ret` − `zs` do sao chép mang, và $L_{\text{cp}}$ là cận dưới của phần tương phản truy hồi không đi qua n-gram được chép. Cả hai dựa trên giả định A_cp: nếu không có sao chép, việc che bằng $R_q$ sẽ làm chú thích `ret` và `zs` mất cùng một lượng điểm. Bài lập luận A_cp chỉ có thể sai theo một chiều (chú thích `ret` tốt hơn chia sẻ nhiều từ đúng hơn với chú thích của ảnh tương tự, nên $K_{\text{ret}}$ chỉ có thể nói quá mức sao chép); $L_{\text{cp}}$ còn giả định sao chép không làm giảm điểm `rand`. Chiều của A_cp được kiểm bằng

$$K_{\text{nc}} = \operatorname{mean}_q\,[\text{loss}(y_{\text{rand},q}; R_q) - \text{loss}(y_{\text{zs},q}; R_q)], \tag{C.7}$$

vì chú thích `rand` cũng chưa từng thấy $R_q$. Nếu $K_{\text{nc}}$ mang nhãn "REVERSED" trên một tập thì chiều đã nêu bị bác và cận bị rút cho tập ấy. Hai kiểm tra nữa: κ của một lượt `zs` so với chính nó bằng 0 theo cấu trúc (tự kiểm của bộ chấm), và $K_{\text{ret}}$ được kiểm xem có tăng từ n = 2 lên n = 4 không; nếu tăng, cận mang cờ "monotonicity check failed". Ba đại lượng đi kèm chỉ mang tính mô tả: $K_{\text{rand}}$, $K_{\text{ret}} - K_{\text{nc}}$ (được in, không bao giờ gọi là cận) và mất mát của chú thích mù ảnh. Cận sao chép được tính trên CPU từ các lượt giải mã đã lưu của các đăng ký trước, nên $L_{\text{cp}}$ là cận cho tương phản `ret` − `rand` d0 đã lưu, giải mã theo lô, chứ không phải phép tách của $\tau_{\text{sel}}$ ở cỡ lô 1; với Aya-Vision-8B trên XM-dev500 không có lượt lưu nên hàng của nó dùng lượt giải mã theo lô của khối 1.

**Nhánh bên thứ ba (khối 3) và đối chứng dương.** Đăng ký áp phép tách cho hai hệ nữa, chỉ trên OV-dev-B và XM-dev500. Thứ nhất là LMCap cài đặt lại (không phải mã của tác giả, không phải phát biểu về số đã công bố), ở đây viết chú thích tiếng Việt từ bộ nhớ tiếng Việt đã đăng ký; bộ sinh văn bản của nó không bao giờ thấy ảnh, ảnh chỉ tới nó qua chú thích truy hồi và qua bước xếp hạng lại ba chùm bằng CLIP đa ngữ. Ba nhánh chỉ khác ở K = 4 chú thích của truy vấn: `lmcap_ri` (truy hồi của chính LMCap), `lmcap_rand` (4 cụm đầu trong danh sách `rand` d0 của truy vấn không trùng N = 3 minh hoạ cố định), và `lmcap_perm` (4 cụm đầu trong danh sách truy hồi LMCap của ảnh cho $\pi_1(q)$ qua được ngưỡng cắt cận của truy vấn và không phải cụm minh hoạ). Thứ hai là định dạng cặp ảnh–chú thích cho Qwen2.5-VL-7B (kiểu RAGCap dùng, nhưng không phải RAGCap [@Bazi2025RAGCap]): `ret_img` và `rand_img` cho xem các cụm `ret` và `rand` d0 dưới dạng ảnh kèm dòng chú thích; hàng $\tau_{\text{sel}}$ của định dạng này được in cạnh hàng ví dụ văn bản nhưng không tính hiệu số giữa hai định dạng, vì đó sẽ là một tương phản chưa đăng ký. Vì bộ sinh của LMCap không thấy ảnh, truy hồi buộc phải mang thông tin ảnh tới nó, và thay chú thích truy hồi bằng chú thích ngẫu nhiên phải làm điểm giảm; $\tau_{\text{sel}}$ của LMCap trên OV-dev-B vì thế là đối chứng dương (positive control) đã đăng ký của phân tích phân bổ. Mọi nhánh khối 3 được giải mã ở cỡ lô 1 trên một máy thuê không chạy việc GPU nào khác; phép kiểm tất định D1 được làm trên chính nhánh mà mỗi bộ chạy giải mã trong khối 3 (50/50 và 50/50 chuỗi giống hệt), và hai nhánh `lmcap_ri`, `ret_img` trên OV-dev-B được giải mã lại trên máy khối 3 để mọi tương phản khối 3 ghép các lượt giải mã của cùng một máy và một đường mã (sai lệch có công bố so với đăng ký, cố định trước mọi đầu ra khối 3). Lần khởi chạy đầu dừng khi nạp trọng số XGLM-2.9B, trước khi sinh chú thích nào (73 giây GPU bị tính, không có đầu ra). Cuối mục, bài nêu một câu: đăng ký còn nêu một phép hoán đổi bộ nhớ trên ảnh tiếng Anh cố định và thêm các mô hình nền ngoài dòng mô hình ngôn ngữ Qwen.

**Nhận xét rà soát.** Mục 3 đủ chi tiết để tái lập các nhánh và bộ chấm, và mọi lựa chọn bất lợi cho nghiên cứu (bước xoá là một phần của đại lượng đăng ký của InternVL3, dòng dõi chung của mô hình kiểm chứng, bốn sai khác của bản cài đặt lại LMCap) đều được nêu. Các điểm sau cần được người viết lại xử lý.

1. **Cấu hình được chọn theo điểm của `ret`.** Mục 3.5 cho biết quy tắc giai đoạn A chọn cấu hình có stripped CIDEr-D cao nhất trong các lượt `ret`; `rand` thừa hưởng k, thứ tự và đuôi đó. Tương phản `ret` − `rand` vì vậy được đo tại cấu hình tối ưu cho `ret`. Tập kiểm tra là tập mới nên không có rò rỉ, nhưng phản biện có thể hỏi liệu `rand` có cấu hình tốt hơn hay không; nên nêu thẳng điều này trong Mục 9.2 (mối đe doạ nội tại).
2. **Đại lượng gộp trộn hai cấu hình khác nhau.** Hai mô hình nền khác k, thứ tự, đuôi và τ (Bảng 2); Mục 5.2 và Mục 9.1 đã nói đại lượng gộp không phải hiệu ứng cho một MLLM điển hình. Nên đặt câu ấy ngay dưới Bảng 2 để người đọc không hiểu số gộp là trung bình theo mô hình.
3. **Mô hình kiểm chứng gần mức ngẫu nhiên.** Bảng S9 cho AUROC của điểm s trong khoảng 0.519 đến 0.582 ở giai đoạn B, và Bảng S12 cho 0.560 trên OV-test; Mục 3.4 và 3.5 không nhắc tới chất lượng phân biệt này. Phản biện sẽ hỏi vì sao một bước xoá với mô hình kiểm chứng yếu vẫn nằm trong đại lượng đăng ký; câu trả lời của bài (quy tắc đã đóng băng, không chọn lại) nên được nói ngay tại Mục 3.5 kèm dẫn chiếu tới hai bảng.
4. **Ký hiệu chồng nghĩa.** τ vừa là ngưỡng xoá vừa là gốc của bốn đại lượng $\tau_{\text{any}}$, $\tau_{\text{sel}}$, $\tau_{\text{marg}}$, $\tau_{\text{pair}}$; K vừa là số chú thích của LMCap (K = 4), vừa là tiền tố của $K_{\text{ret}}$, $K_{\text{nc}}$, vừa là cổng dừng K1; κ vừa là $\kappa_q$ vừa là hệ số đồng thuận ở Mục 6.9; R vừa là số lần rút vừa là danh sách $R_q$; D vừa là số hoán vị vừa là phép kiểm D1. Bài có ghi chú phân biệt, nhưng với bản tạp chí nên đổi ký hiệu (ví dụ đặt tên khác cho bốn đại lượng phân bổ) thay vì dựa vào ghi chú.
5. **Lưới τ viết không thống nhất.** Mục 3.5 viết {−∞, 0.0, 0.1, 0.2, 0.3, +∞}, trong khi Bảng 2, Mục 7.3 và Bảng S12 viết 0.00, 0.10, 0.20, 0.30. Nên dùng một dạng.
6. **Cỡ lô không được nêu ở Mục 3.3.** Mục 6.10.2 cho thấy thành phần lô làm đổi chú thích tham lam, và Mục 9.3 nói cỡ lô của mỗi mô hình nền được cố định trong mã sẽ công bố; nhưng Mục 3.3 không in cỡ lô. Đây là tham số cần cho tái lập và nên có trong bài.
7. **Khuôn lời nhắc chỉ được ghim bằng mã băm.** Bài nói khuôn không chứa chú thích của bộ dữ liệu nào; vì vậy có thể in nguyên văn khuôn (tiêu đề, dòng ví dụ mẫu rỗng, hai đuôi) trong phụ lục để phản biện đánh giá được chỉ dẫn mà mô hình nhận.
8. **Mục 3.8 lẫn phương pháp với nhật ký vận hành.** Các chi tiết như định dạng tệp trọng số, số giây GPU của lần khởi chạy hỏng hay việc giải mã lại hai nhánh thuộc về phần công bố (Mục 7.5) hoặc phụ lục; Mục 3.8 nên chỉ giữ định nghĩa nhánh, đại lượng và giả định.
9. **Ba chẩn đoán dùng trong quy tắc chọn chưa được định nghĩa.** Quy tắc giai đoạn A (Mục 3.5) dùng tỉ lệ sao chép gần nguyên văn và tỉ lệ hit-max; các bảng S1–S4 còn có cột tỉ lệ chép 4-gram. Phần "Instrument definitions" của Phụ lục S định nghĩa bộ chấm, bộ so khớp, P_cm, bộ so khớp tiếng Anh và câu hỏi kiểm chứng, nhưng không định nghĩa ba đại lượng này; cần bổ sung công thức của từng đại lượng.
10. **Các nhánh "đã đăng ký khác" chưa có kết cục.** Câu cuối Mục 3.8 nêu phép hoán đổi bộ nhớ và các mô hình nền ngoài dòng Qwen; Mục 5.7 mô tả chi tiết quy tắc cho phép hoán đổi này, nhưng Mục 6.10 không báo cáo kết quả và cũng không ghi "NOT RUN" (xem nhận xét ở C.7.3).

## C.5 Dữ liệu và cách chia tập (Mục 4 của bài báo)

**Nội dung.** Mọi dữ liệu là các bộ công khai sẵn có với tham chiếu và nhãn đã phát hành; không có chú giải mới và không đầu ra mô hình nào được dùng làm nhãn vàng. Chú thích KTVIC và UIT-OpenViIC chỉ được dùng làm dữ liệu nghiên cứu, đặt vào lời nhắc lúc chạy và không phát tán lại. Bảng C.5 chép lại Bảng 3 của bài.

**Bảng C.5.** Mọi tập dữ liệu, kích thước đầy đủ và cách hình thành (Bảng 3, Mục 4).

| Tập | Vai trò | Số ảnh | Cách hình thành |
|---|---|---|---|
| bộ nhớ | kho truy hồi | 10,501 (8,190 cụm) | KTVIC train trừ phần tách phát triển 300 ảnh (3,469) cộng OpenViIC train (9,088), bớt 2,056 ảnh do bộ lọc định trước |
| KTVIC dev299 | giai đoạn A: chọn cấu hình | 299 | phần tách phát triển KTVIC trừ một ảnh bị bộ lọc định trước loại |
| OV-dev-A | giai đoạn A: kiểm tra đi tiếp | 911 | OpenViIC dev (2,011 tệp) chia theo thứ tự băm thành 1,005 / 1,006, rồi lọc |
| OV-dev-B | giai đoạn B: cổng một lần nhìn | 925 | nửa còn lại, lọc bằng cùng bộ lọc |
| XM-dev500 | giai đoạn B: thứ cấp | 500 | các ảnh đầu của phần còn lại của XM3600 theo thứ tự băm |
| **OV-test primary** | **kiểm tra (P1, P1b, P2)** | **1,941** | toàn bộ OpenViIC test trừ 60 ảnh bị bộ lọc định trước loại, cố định trước mọi đầu ra kiểm tra |
| OV-test full | độ nhạy đã đăng ký | 2,001 | mọi tệp OpenViIC test |
| **XM-test2500** | **kiểm tra (XM-a, XM-b)** | **2,500** | XM3600 trừ XM600 và trừ XM-dev500 |
| XM-test2500 bỏ ảnh ba tham chiếu | độ nhạy đã đăng ký | 2,392 | bớt 108 ảnh có từ ba tham chiếu tiếng Việt trở lên |
| Flickr30K carve (Anh) | đăng ký Flickr30K: thăm dò | 1,000 | ảnh rút từ phần train Karpathy của Flickr30K [@Young2014Flickr30K; @Karpathy2015Split] |
| Flickr30K val (Anh) | đăng ký Flickr30K: diễn tập, dùng một lần | 1,014 | toàn bộ phần val Karpathy |
| **Flickr30K test (Anh)** | **kiểm tra (E3a–c), một lần nhìn** | **1,000** | toàn bộ phần test Karpathy; 997 ảnh còn lại sau bộ lọc định trước được báo cáo cạnh kết quả đăng ký |

Với OpenViIC test, mỗi mục trong 2,001 mục kiểm tra được giữ với tham chiếu riêng và là một đơn vị bootstrap. 60 ảnh bị loại khỏi tập chính là các tệp kiểm tra OpenViIC mà cùng quy tắc gần trùng khớp với một ảnh của phần tách phát triển KTVIC; kết quả trên đủ 2,001 ảnh được báo cáo ngay cạnh trong bảng chính. Ba tệp kiểm tra bị cắt cụt nằm trong cả tập chính lẫn tập đầy đủ; chúng được giải mã bằng bộ đọc nghiêm ngặt trước và chỉ khi thất bại mới bật chế độ đọc tệp cắt cụt cho riêng lần gọi đó; không tệp nào bị loại. Với XM3600, toàn bộ 3,600 ảnh được chia trước khi có bất kỳ đầu ra nào của nghiên cứu: 600 ảnh (XM600), tập đánh giá của nghiên cứu đồng hành về độ chính xác đối tượng, được để riêng; 3,000 ảnh còn lại được xếp theo mã băm của byte ảnh, 500 ảnh đầu thành XM-dev500 và 2,500 ảnh sau thành XM-test2500. Vì thế bài không báo cáo kết quả trên toàn bộ XM3600. Phép kiểm tra dùng tham chiếu tiếng Việt đã phát hành của 2,500 ảnh (5,108 tham chiếu) và, chỉ ngoại tuyến, nhãn Open Images do người xác minh. Các tập tiếng Anh của nhánh COCO và NoCaps được mô tả ở Mục 8.1, ba tập Flickr30K ở Mục 8.6.

**Nhận xét rà soát.** Cách chia tập minh bạch và mọi tập đều có kích thước đầy đủ. Bốn điểm cần bổ sung. (i) Bản đăng ký kiểm tra (`prereg/2026-10-25_c_test/PREREG.md`, §3.1) ghi OV-test có 2,001 mục nhưng chỉ 1,997 ảnh phân biệt (bốn cặp trùng từng byte), và tập chính có 1,941 mục, tức 1,937 ảnh phân biệt; cả hai mục của một cặp được giữ, mỗi mục là một đơn vị bootstrap. Mục 4 và Bảng 3 của bài gọi 1,941 và 2,001 là số "ảnh" và không nêu số ảnh phân biệt. Đây là chỗ bài và bản đăng ký nói khác nhau, và vì các bản đăng ký sẽ được phát hành cùng bài (Mục 10) nên người đọc sẽ thấy cả hai cách nói. Cần cân nhắc thêm một câu vào Mục 4 (số mục, số ảnh phân biệt, và việc mỗi mục là một đơn vị bootstrap) hoặc ít nhất đổi tiêu đề cột thành số mục, vì phản biện có thể hỏi về các đơn vị bootstrap trùng ảnh. (ii) Cụm "pre-specified filter" được dùng cho nhiều bộ lọc khác nhau (bộ nhớ, dev299, hai nửa OV-dev, 60 ảnh OV-test, 997 ảnh Flickr30K). Mục 3.1 định nghĩa quy tắc gần trùng và Mục 4 nói 60 ảnh là các tệp khớp với phần tách phát triển KTVIC, nhưng bài không nói hai nửa OV-dev (từ 1,005 và 1,006 xuống 911 và 925) được lọc so với tập nào; cần một câu cho mỗi bộ lọc. (iii) Bảng 3 không nói phần tách Flickr30K 1,000 ảnh được rút theo cách nào (hạt giống, thứ tự băm). (iv) Trên XM-test2500 có 5,108 tham chiếu cho 2,500 ảnh và chỉ 108 ảnh có từ ba tham chiếu trở lên, tức đa số ảnh có ít tham chiếu; phản biện có thể hỏi về độ ổn định của CIDEr-D trong điều kiện này. Bài đã có phân tích độ nhạy bỏ 108 ảnh, nhưng nên nói rõ số tham chiếu điển hình cho mỗi ảnh.

## C.6 Tiền đăng ký và kế hoạch phân tích (Mục 5 của bài báo)

**Nội dung.** Mục 5 mở bằng một bảng thuật ngữ (Box 1), được gộp vào mục C.15 của báo cáo này. Phần còn lại gồm bảy tiểu mục.

### C.6.1 Ba giai đoạn (Mục 5.1)

**Bảng C.6.** Ba giai đoạn của nghiên cứu tiếng Việt (bảng ở Mục 5.1).

| Giai đoạn | Dữ liệu | Điều được cố định hoặc kiểm | Trạng thái |
|---|---|---|---|
| A (thăm dò) | KTVIC dev299, OV-dev-A | một cấu hình cho mỗi mô hình nền, chọn bằng quy tắc viết trước mọi đầu ra | ghi chú thiết kế được cam kết trước mọi đầu ra; mọi cấu hình đã thử ở Bảng S10–S11 |
| B (một lần nhìn) | OV-dev-B, XM-dev500 | cổng trên OV-dev-B: `ret` − `rand` gộp có cận dưới khoảng tin cậy > 0 và điểm ước lượng ≥ +4.0 (gấp đôi SESOI), cùng giả thuyết cơ chế chắn H_G | đăng ký được cam kết trước khi giải mã ảnh dev-B nào; cổng "PASS", H_G không qua |
| kiểm tra (mỗi tập một lần nhìn) | OV-test, XM-test2500 | P1, P1b, P2, XM-a, XM-b và các hàng thứ cấp có tên | đăng ký và mã kiểm tra được cam kết, mã được kiểm, trước khi ảnh hay tham chiếu kiểm tra nào tới máy chủ GPU |

Bản đăng ký kiểm tra được cam kết sau khi biết kết quả giai đoạn B và trước khi có đầu ra kiểm tra nào; không gì trong đó được đặt từ một tập kiểm tra. "Một lần nhìn" trong thực hành nghĩa là mỗi tập kiểm tra được giải mã, chấm và quyết định một lần với cấu hình đóng băng; trong lúc chạy không ai đọc chú thích kiểm tra, dòng sổ điểm, điểm số hay đầu ra quyết định dở dang, việc giám sát chỉ dùng số đếm, thời gian, giây GPU và mã trả về. Khối OpenViIC chạy trước, rồi khối XM3600; khối XM3600 được cam kết trước là sẽ chạy bất kể phán quyết OpenViIC.

### C.6.2 Đại lượng ước lượng đích và quy tắc quyết định (Mục 5.2)

Với mô hình nền m và ảnh i, $\Delta_{m,i}$ là stripped CIDEr-D của `ret` trừ của `rand`, mỗi nhánh ở cấu hình đóng băng của m. Hiệu gộp là

$$\Delta_i = \tfrac{1}{2}\,(\Delta_{\text{qwen},i} + \Delta_{\text{internvl},i}), \tag{C.8}$$

và SESOI = +2.0 điểm stripped CIDEr-D. Bài nói rõ đại lượng gộp là trung bình của hai cặp mô hình nền–cấu hình khác nhau về k, thứ tự, đuôi và τ, không phải ước lượng hiệu ứng cho một MLLM điển hình, và mọi số gộp được in cạnh hai hàng theo mô hình nền. Về nguồn gốc SESOI, bài viết: giá trị +2.0 được đặt ở giai đoạn 2, trước mọi đầu ra giai đoạn B, như một giá trị hoạch định gợi ý trong ghi chú thiết kế; bản đăng ký giai đoạn 2 nói nó không được suy ra từ thử nghiệm giai đoạn A hay bất kỳ số nào của giai đoạn 1, "and no calibration of it is recorded". Nhánh tiếng Anh mang nguyên +2.0 sang, không hiệu chỉnh lại cho thang PTB. Về điều kiện của khoảng tin cậy: mỗi ảnh có một phép gán `rand` có hạt giống, và tần suất tài liệu của CIDEr-D lấy từ toàn tập được chấm; bootstrap chỉ lấy mẫu lại ảnh, nên khoảng tin cậy phủ bất định do lấy mẫu ảnh, có điều kiện theo một lần rút `rand` ấy và theo tần suất tài liệu toàn tập; biến thiên do rút các ví dụ ngẫu nhiên khác không nằm trong khoảng tin cậy.

**Bảng C.7.** Dự đoán đã đăng ký và quy tắc quyết định (Bảng 4, Mục 5.2).

| Tên | Đại lượng | Tập | Quy tắc |
|---|---|---|---|
| **P1 (chính)** | trung bình của $\Delta_i$ gộp | OV-test primary (1,941) | "PASS" nếu điểm ước lượng > +2.0 **và** cận dưới khoảng tin cậy 95% > 0 |
| quy tắc độ dài L | theo từng mô hình nền, trị tuyệt đối của (len_ret − len_rand) chia len_rand trên tập chính (số âm tiết trung bình) | OV-test primary | nếu > 0.10 với một trong hai mô hình nền, P1 được ghi là "PASS, not separated from length" |
| P1b (không gác cổng) | trung bình $\Delta_{m,i}$ theo mô hình nền | OV-test primary | Qwen2.5-VL: "confirmed" nếu điểm ước lượng > +2.0; InternVL3: chỉ báo cáo, không có dự đoán; P1b chọn câu phạm vi (scope sentence) |
| **P2** | theo từng mô hình nền, ΔP_cm của `ret` so với `zs` | OV-test primary | với **mỗi** mô hình nền, cận dưới khoảng tin cậy 95% > −1.0 |
| XM-a | trung bình của $\Delta_i$ gộp | XM-test2500 | cận dưới khoảng tin cậy 95% > 0; điểm dương với khoảng tin cậy chứa 0 chỉ được in như số mô tả |
| XM-b | hiệu độ chính xác đối tượng đã kiểm chứng của `ret` so với `zs`, gộp trên các lần nhắc và mô hình nền | XM-test2500 | cận dưới khoảng tin cậy 95% > −1.0 |
| dự đoán XM | XM-a ∧ XM-b | XM-test2500 | "confirmed" chỉ khi cả hai qua; ngược lại "not confirmed" |

Độ chính xác so khớp số lượng được định nghĩa như sau (Mục 5.2 và phần "Instrument definitions" của Phụ lục S). Với ảnh i, gọi $M_i(\text{run})$ và $M_i(\text{zs})$ là các lớp phân biệt được so khớp trong chú thích của lượt chạy và trong chú thích không ví dụ của cùng mô hình, theo thứ tự nhắc; $k_i = \min(|M_i(\text{run})|, |M_i(\text{zs})|)$; tp đếm số lớp trong $k_i$ lớp đầu mà nhãn vàng ủng hộ. Khi đó

$$\Delta P_{\text{cm}} = 100 \cdot \frac{\sum \text{tp}_{\text{cm}} - \sum \text{tp}_{\text{cm,zs}}}{\sum k_{\text{cm}}}. \tag{C.9}$$

Các phân tích độ nhạy đã đăng ký được báo cáo cạnh mỗi dự đoán và không bao giờ thay thế nó: với P1, P1b, P2 là OV-test đầy đủ (2,001); với XM-a, XM-b là XM-test2500 bỏ ảnh ba tham chiếu (2,392).

**Bảng C.8.** Câu phạm vi, cố định trước kiểm tra và chỉ áp dụng nếu P1 qua (Bảng 5, Mục 5.2).

| Kết cục P1b | Câu đặt cạnh mọi số gộp |
|---|---|
| điểm Qwen > +2.0, cận dưới InternVL3 ≤ 0 | "carried mainly by Qwen2.5-VL; not detected for InternVL3" |
| điểm Qwen > +2.0, cận dưới InternVL3 > 0, điểm InternVL3 < điểm Qwen | "carried mainly by Qwen2.5-VL; smaller for InternVL3" |
| điểm Qwen > +2.0, cận dưới InternVL3 > 0, điểm InternVL3 ≥ điểm Qwen | "present for both backbones" |
| điểm Qwen ≤ +2.0, điểm InternVL3 > +2.0 và cận dưới > 0 | "carried mainly by InternVL3; not at the SESOI for Qwen2.5-VL" |
| điểm Qwen ≤ +2.0, mọi kết cục khác của InternVL3 | "not carried by either backbone at the SESOI" |

Bài liệt kê các khẳng định và cổng của chúng: "ví dụ truy hồi hơn ví dụ ngẫu nhiên trên OpenViIC test" cần P1 qua và quy tắc L không kích hoạt; "không có cái giá về độ chính xác đối tượng" cho mô hình nền m cần P2 qua cho m và chỉ áp dụng cho OpenViIC test, cái giá được đo so với không ví dụ từ toàn bộ lời nhắc ngữ cảnh, P2 không so `ret` với `rand`; "mức tăng chuyển sang XM3600 tiếng Việt" cần XM-a qua; "dự đoán XM đã đăng ký được xác nhận" cần cả XM-a và XM-b; không khẳng định nào về cơ chế chắn được phép. Cách diễn đạt cho thất bại cũng được đăng ký: XM-a thất bại được báo cáo là "the gain was not detected out of domain (XM3600)" kèm khoảng tin cậy; P1 thất bại sẽ được báo cáo là "the dev-B gain did not replicate on OV-test", không có phân tích hậu nghiệm thay thế.

### C.6.3 Các hàng thứ cấp (Mục 5.3)

Không hàng thứ cấp nào có thể biến một dự đoán thất bại thành qua, và không hàng nào vào tên bài, tóm tắt hay đóng góp: S-zf (`ret` so với `zs` và với `fix`, với kỳ vọng so với `zs` khoảng +10.0 gộp, nêu trước kiểm tra và không có nhãn qua); hai đường cơ sở NN-top1 và NN-consensus; cột PTB; liều–đáp ứng (dose-response) theo tam phân vị cosine; báo cáo văn phong và tỉ lệ nguồn dữ liệu của ví dụ; độ chính xác đối tượng chỉ-từ-láng-giềng; và việc in mọi số gộp cạnh hai giá trị theo mô hình nền. Một hàng thứ cấp có động cơ từ giai đoạn B: `ret` − `rand` theo từng mô hình nền ở τ = −∞, hậu nghiệm ở giai đoạn B và được định trước cho kiểm tra. Chỉ hàng InternVL3 là mới; hàng này không có dạng gộp, mang nhãn "detected" khi cận dưới khoảng tin cậy > 0, không cổng hay quy tắc phạm vi nào đọc nó, và luôn được in sau kết quả đăng ký ở τ = 0.10.

### C.6.4 Bất định và đa kiểm định (Mục 5.4)

Mọi khoảng tin cậy là bootstrap ghép cặp theo ảnh với B = 2,000 lần lấy mẫu lại và khoảng phân vị 95%. Mỗi tập được chấm rút một ma trận chỉ số từ một bộ sinh số mới với hạt giống 0, dùng cho mọi khoảng tin cậy trên tập ấy (1,941, 2,001, 2,500 và 2,392 ảnh); các ma trận được rút độc lập nên ma trận của tập này không phải tập con của tập kia. Thống kê gộp lấy trung bình hiệu theo ảnh qua các mô hình nền trước khi lấy mẫu lại; với thống kê dạng tỉ số (ΔP_cm, độ chính xác đã kiểm chứng, độ chính xác chỉ-từ-láng-giềng), tử và mẫu được lấy mẫu lại cùng nhau. Về đa kiểm định: P1 là phép kiểm chính duy nhất nên không cần hiệu chỉnh; P2 là phép kiểm giao–hợp trên hai mô hình nền; dự đoán XM3600 là hội của XM-a và XM-b; trong đăng ký tiếng Anh S-NC được gác theo thứ tự cố định sau P1-EN; ba khẳng định kiểm tra Flickr30K được hiệu chỉnh Holm; mọi thứ khác là thứ cấp với khoảng tin cậy không hiệu chỉnh. Không giá trị p nào được báo cáo cho các đăng ký tiếng Việt, COCO và NoCaps, vì chúng cố định quy tắc dựa trên khoảng tin cậy; bài viết rằng một giá trị p thêm vào lúc này sẽ là hậu nghiệm và không đổi phán quyết nào.

Về công suất và độ chính xác, đăng ký giai đoạn 2 nêu công suất của cổng giai đoạn B (khoảng 50% nếu hiệu gộp thật là +4); không có phát biểu công suất riêng nào được đăng ký cho P1. Nửa độ rộng khoảng tin cậy 95% đạt được của các đại lượng gộp đã đăng ký là 1.02 (P1), 1.21 (XM-a), 0.97 (P1-EN) và 0.78 (S-NC). SESOI bằng khoảng 6.2% điểm `rand` gộp trên OV-test, 3.7% trên XM-test2500 và 2.3% trên COCO và NoCaps, nên trên COCO cùng mức +2.0 tương đối dễ dãi hơn. Sai số Monte Carlo của bootstrap tối đa khoảng 0.05 điểm cho mọi hàng đăng ký. Về ngân sách (Mục 5.5), kiểm tra có trần cứng 20 giờ GPU trên một GPU 24 GB (nhu cầu ước tính 13.7), và trần không bị chạm.

### C.6.5 Các đăng ký về sau (Mục 5.6)

Hai nghiên cứu được đăng ký sau kiểm tra tiếng Việt, mỗi cái trong tệp riêng cam kết trước mọi đầu ra của nó, không sửa đăng ký kiểm tra: nhánh tiếng Anh (Mục 8) và các ablation cơ chế (Mục 6.8, thay đổi τ, k và cỡ bộ nhớ trên OV-dev-B, một lần nhìn, nhãn "development set, non-confirmatory"). Đăng ký ablation cố định trước điều kiện để Mục 6.8 được nói rằng ablation giải thích sự phụ thuộc mô hình nền; điều kiện ấy thoả, nhưng Mục 6.8 dùng cách nói yếu hơn. Đăng ký thứ ba, viết sau khi bốn tập kiểm tra đã có quyết định, là so sánh Flickr30K (Mục 8.6) theo quy tắc ba tầng. Hai nghiên cứu thăm dò về lọc ví dụ được đăng ký muộn hơn nữa (Mục 6.9). Cuối cùng, một đăng ký viết sau khi mọi tập kiểm tra của bài đã có quyết định tách tương phản truy hồi chỉ trên dữ liệu phát triển (Mục 5.7).

### C.6.6 Đăng ký phân bổ trên dữ liệu phát triển (Mục 5.7)

Mục 5.7 mở bằng khung nhãn: "Development data only: DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. No test set was staged, decoded, scored or opened. No reported test row, interval or label changes because of a number of this study."

**Tệp và thứ tự.** Bản đăng ký (phiên bản 1.1) được cam kết trước mọi đầu ra, kèm một đính chính viết trước lượt giải mã đầu. Sau khi cổng dừng (kill gate) K1 kích hoạt và trước khi bất kỳ đầu ra nào được chấm, một phụ lục (phiên bản 1.2) đổi cỡ lô và phép kiểm độc lập theo lô, cùng những hệ quả (giải mã lại mọi nhánh của tương phản, trần tính toán mới, nhãn hàng cho hai chính sách giải mã, thứ tự chấm đặt đầu ra theo lô sau cùng); không tập, danh sách, nhánh, lần rút, hạt giống, k, lời nhắc, bộ nhớ, ảnh chụp mô hình, SESOI, α, quy tắc nhãn hay quy tắc họ nào thay đổi.

**Tập và ý nghĩa của "lần nhìn đầu".** OV-dev-A (911 ảnh) dùng để đề cử (nomination); OV-dev-B (925) mang một lần nhìn đã đăng ký; XM-dev500 (500) cho các hàng báo cáo không có quy tắc. Trên OV-dev-A và OV-dev-B, tổng $\tau_{\text{sel}} = \tau_{\text{marg}} + \tau_{\text{pair}}$ đã biết từ các giai đoạn phát triển với Qwen2.5-VL-7B và InternVL3-8B, và trên OV-dev-B còn biết với Aya-Vision-8B. Vì đồng nhất thức đúng theo từng ảnh, $\tau_{\text{pair}}$ và $\tau_{\text{marg}}$ trên các tập này là lần nhìn đầu vào cách một tổng đã biết tách ra, không phải vào độ lớn của hiệu ứng truy hồi. Mọi hàng và câu về hai đại lượng ấy của ba mô hình nền trên hai tập này vì vậy mang cụm "split of a known τ_sel", và một lần qua trên OV-dev-B được báo cáo là "the nominated split held on a re-used development set, at batch size 1", không bao giờ là bằng chứng mới rằng truy hồi có ích.

**Khoảng tin cậy và thống kê dạng p.** Mọi khoảng là bootstrap ghép cặp theo ảnh của các hiệu theo ảnh, B = 2,000 lần lấy mẫu lại rút bằng `numpy.random.default_rng(0).integers(0, n, (B, n))`, một ma trận chỉ số cho mỗi tập, cận phân vị. Thống kê dạng p một phía là

$$\tilde p = \frac{1 + \#\{b : \text{trung bình bootstrap}_b \le 0\}}{B + 1}, \tag{C.10}$$

có sàn 1/2,001 và không phải giá trị p chính xác.

**Bốn nhãn.** Với SESOI = +2.0, mỗi tương phản có điểm ước lượng $\hat\theta$ nhận đúng một nhãn, khớp đầu tiên. "DETECTED": $\hat\theta \ge +2.0$ và $\tilde p \le \alpha_j$, với $\alpha_j$ là ngưỡng bước xuống Holm [@Holm1979] ở α một phía theo họ bằng 0.025 trên m khẳng định của họ: các khẳng định xếp theo $\tilde p$, khẳng định thứ j được so với

$$\alpha_j = \frac{0.025}{m - j + 1}, \tag{C.11}$$

và thủ tục dừng ở khẳng định đầu tiên trượt một trong hai điều kiện. Một hàng ngoài mọi họ có m = 1. "REVERSED": cận trên 95% dưới 0. "NEGLIGIBLE": khoảng 90% nằm trong (−2.0, +2.0), tức hai phép kiểm một phía ở 0.05 mỗi phía [@Schuirmann1987]. "UNRESOLVED": không thuộc các trường hợp trên. Bài lưu ý "DETECTED" viết hoa là quy tắc đăng ký, khác chữ "detected" viết thường (cận dưới khoảng tin cậy 95% trên 0, không bao giờ là phán quyết); và với m = 1 quy tắc này trùng dạng với quy tắc P1, trừ việc P1 đòi điểm lớn hơn +2.0 còn "DETECTED" đòi ít nhất +2.0.

**Đề cử, rồi một lần nhìn.** (1) Trên OV-dev-A, với Qwen2.5-VL-7B và InternVL3-8B riêng từng mô hình, $\tau_{\text{pair}}$ và $\tau_{\text{marg}}$ được tính với R = 1 và D = 2; khẳng định H_pair(m) được đề cử nếu cận dưới 95% của $\tau_{\text{pair}}$ ít nhất +2.0, và H_marg(m) tương tự. (2) Tệp đề cử liệt kê các khẳng định; sha256 của nó được ghi vào sổ quyết định trước khi bất kỳ đầu ra OV-dev-B mới nào được chấm. (3) Trên OV-dev-B, mỗi khẳng định được đề cử "PASSES" nếu tương phản của nó là "DETECTED", với các khẳng định được đề cử làm họ Holm. (4) Nếu không gì được đề cử thì không có khẳng định đăng ký nào và các hàng OV-dev-B được báo cáo với nhãn kèm câu "no claim was nominated on OV-dev-A". (5) Các thành phần không được đề cử, và hai đại lượng của Aya-Vision-8B (không có lượt giải mã OV-dev-A), là hàng mô tả có nhãn. Cách diễn đạt thất bại cũng cố định: "FAIL: the claim nominated on OV-dev-A did not hold on OV-dev-B". Trên XM-dev500 các hàng không mang quy tắc, vì ở n = 500 nửa độ rộng đã biết của khoảng $\tau_{\text{sel}}$ của Qwen2.5-VL-7B khoảng ±3.4, nên cả "DETECTED" ở +2.0 lẫn "NEGLIGIBLE" đều không quyết định được một cách tin cậy.

**Nhánh bên thứ ba và đối chứng dương.** Khối 3 thêm, trên OV-dev-B và XM-dev500, ba đại lượng của LMCap và $\tau_{\text{sel}}$ định dạng ảnh của Qwen2.5-VL-7B, mỗi cái là một hàng riêng ngoài mọi họ (m = 1). Đăng ký cố định một quy tắc: $\tau_{\text{sel}}$ của LMCap trên OV-dev-B phải là "DETECTED"; nếu không, đối chứng dương thất bại và các hàng bên thứ ba sẽ được in không kèm diễn giải.

**Phương sai.** (a) Với mỗi mô hình nền và tập có R ≥ 2: phương sai trong ảnh trung bình qua các lần rút $\hat\sigma^2_w$, tỉ phần của nó trong phương sai bootstrap theo ảnh, và một giả dược `rand` d1 − `rand` d2 kèm khoảng tin cậy; một hàng giả dược bị gắn cờ khi trị tuyệt đối của điểm ước lượng ≥ 2.0 và khoảng 95% không chứa 0; cờ không phải lệnh dừng, tập bị gắn cờ được đưa ra rà soát trước khi dùng. (b) Với một bộ `fix` dùng chung (Qwen2.5-VL-7B, $y_{iF} = s_i(\texttt{ret}) - s_i(\texttt{fix}_F)$, F = 0 … 4), bố trí hai chiều cho $MS_F$, $MS_I$, $MS_E$ và

$$\hat V_b = \max\!\left(0, \frac{MS_F - MS_E}{n}\right),\qquad \hat\omega = \frac{\hat V_b}{\bar V_{\text{img}}}, \tag{C.12}$$

với $\bar V_{\text{img}}$ là phương sai mà bootstrap theo ảnh trên một bộ cố định nhìn thấy, và cận trên xấp xỉ 95% $\omega^U$. Quy tắc nhãn đã đăng ký: $\omega^U \le 0.25$ cho "the fixed-set rows are practically unconditional"; ngược lại mọi hàng `fix` của bài mang "conditional on the realised fixed set". Bài nêu rõ với năm bộ, $\omega^U$ bằng khoảng 4.6 lần tỉ phần tương tác ngay cả khi phương sai giữa các bộ bằng 0, một tính chất của cận. Không khoảng tin cậy kiểm tra nào bị nới, tính lại hay đổi nhãn bằng số của phân tích này.

**Cận sao chép, nguồn bộ nhớ và các kiểm tra khác.** Trên OV-dev-B cận sao chép là hậu nghiệm (được đặc tả sau khi đã thấy các hàng che ngây thơ trên tập ấy); trên XM-dev500 nó là lần nhìn đầu vào κ. Các câu đọc được cố định trước: $L_{\text{cp}}$ "DETECTED" cho "a retrieval-specific effect of at least +2.0 remains under the most pessimistic copy attribution"; điểm $L_{\text{cp}}$ ≤ 0 cho "the bound does not exclude that the whole retrieval-specific effect is carried by copied n-grams; this agrees with, and does not prove, the published short-cut account" [@Li2025UnveilingICL]; mọi kết cục khác cho "partly bounded". Về nguồn bộ nhớ, bộ nhớ tiếng Việt không thể hoán đổi sang nguồn khác (nó có 6,017 cụm chỉ chứa ảnh OpenViIC, 2,133 cụm chứa cả hai và 40 cụm chỉ chứa ảnh KTVIC), nên phép hoán đổi được đăng ký trên dữ liệu tiếng Anh, trên 1,014 ảnh Flickr30K val, cho Qwen2.5-VL-7B và Aya-Vision-8B, giữa bộ nhớ cùng nguồn $M_T$ (28,000 ảnh Flickr30K train) và bộ nhớ khác nguồn $M_O$ (28,000 cụm lấy mẫu có hạt giống từ bộ nhớ COCO), với

$$\delta = \operatorname{mean}_i\{[s_i(\texttt{ret}; M_T) - s_i(\texttt{rand}; M_T)] - [s_i(\texttt{ret}; M_O) - s_i(\texttt{rand}; M_O)]\} \tag{C.13}$$

và các câu đọc cố định cho từng nhãn; một hàng đồng hành hậu nghiệm dùng các ô đã lưu của phần tách Flickr30K 1,000 ảnh, nơi bộ nhớ khác nguồn là toàn bộ bộ nhớ COCO (111,927 cụm) so với 28,000, mang nhãn "post hoc; size-confounded". Một hàng độ nhạy tần suất tài liệu tính lại $\tau_{\text{pair}}$ và $\tau_{\text{marg}}$ của Qwen2.5-VL-7B trên OV-dev-B ở các hàng 1–200 của ma trận chỉ số với tần suất tài liệu tính lại theo mẫu. Cổng tương đương bộ chấm đòi bộ chấm tái lập điểm đã lưu của sáu lượt giai đoạn B trong sai số 1e-4 trước khi chấm lượt mới. Thứ tự nhìn được mã thực thi: giai đoạn kiểm chứng; OV-dev-A cỡ lô 1 và tệp đề cử; OV-dev-B cỡ lô 1, tệp phán quyết và hàng tần suất tài liệu; XM-dev500 cỡ lô 1 rồi mọi đầu ra theo lô; cuối cùng các hàng hậu nghiệm. Bộ chấm từ chối mọi lượt OV-dev-B trước khi có tệp đề cử và mọi lượt theo lô trước phán quyết OV-dev-B. Về ngân sách, khối 1 có trần cứng 12 giờ GPU; khối 1b có trần min(40, 1.5 P) giờ GPU với P là dự phóng từ tốc độ cỡ lô 1 đo trong D1; khối 3 có trần 5 giờ GPU ở phiên bản 1.1, được phụ lục thay bằng min(12, 1.5 P3). Bài ghi một mốc đóng băng vào 12:00 ngày 16/11/2026 (UTC+7) kết thúc mọi bước chưa xong.

**Nhận xét rà soát.** Mục 5 là xương sống của bài và được viết với độ chính xác cao: đại lượng, quy tắc, câu chữ cho thất bại và bảng câu phạm vi đều có trước dữ liệu. Để giúp rà soát, Bảng C.9 gom các dạng quy tắc quyết định mà bài dùng qua các đăng ký; bảng cho thấy các điều kiện không cùng dạng giữa các đăng ký (lớn hơn hẳn hay lớn hơn hoặc bằng +2.0; cận dưới của khoảng hai phía hay thống kê một phía), là điều một phản biện về thống kê sẽ để ý.

**Bảng C.9.** Các dạng quy tắc quyết định qua các đăng ký của bài (tổng hợp từ Mục 5.2, 5.7, 8.1 và 8.6; không có số liệu mới).

| Đăng ký | Khẳng định | Điều kiện về điểm ước lượng | Điều kiện về bất định |
|---|---|---|---|
| kiểm tra tiếng Việt | P1 | > +2.0 | cận dưới khoảng tin cậy 95% > 0 |
| kiểm tra tiếng Việt | XM-a | không có | cận dưới khoảng tin cậy 95% > 0 |
| kiểm tra tiếng Việt | P2, XM-b | không có | cận dưới khoảng tin cậy 95% > −1.0 |
| nhánh tiếng Anh | P1-EN, S-NC | > +2.0 | cận dưới khoảng tin cậy 95% > 0 |
| Flickr30K, diễn tập | E1, E2, E3a–c | ≥ +2.0 | cận dưới 95% > 0; lên kiểm tra chỉ khi xác suất qua dự phóng ≥ 0.98 |
| Flickr30K, kiểm tra | E3a–c | ≥ +2.0 | thống kê một phía hiệu chỉnh Holm < 0.05 |
| phân bổ (phát triển) | nhãn "DETECTED" | ≥ +2.0 | $\tilde p \le$ ngưỡng Holm ở α một phía 0.025 |

Các điểm cần xử lý:

1. **Nguồn gốc các ngưỡng.** SESOI +2.0 là "giá trị hoạch định" không có hiệu chỉnh nào được ghi lại (Mục 5.2); bài thẳng thắn về điều này, nhưng phản biện gần như chắc chắn hỏi vì sao +2.0. Bài chưa giải thích nguồn gốc của sàn −1.0 trong P2 và XM-b (biên không-kém-hơn) và ngưỡng 0.10 của quy tắc L. Cần một đoạn ngắn nêu căn cứ của cả ba, hoặc nói rõ chúng cũng là giá trị hoạch định.
2. **Quy tắc của H_G không có trong bài.** Mục 5.1 chỉ nhắc "the guard hypothesis H_G", và Mục 6.7 báo cáo nó "not passed" với hiệu độ chính xác gộp +2.91 [0.46, 5.31], tức khoảng tin cậy nằm trên 0. Người đọc không thể hiểu vì sao kết quả này lại không qua. Bản đăng ký giai đoạn 2 (`prereg/2026-10-22_c_stage2/PREREG.md`, §7.5) định nghĩa H_G là hiệu độ chính xác đối tượng chỉ-từ-láng-giềng của `ret` giữa ngưỡng chắn và τ = −∞, gộp hai mô hình nền, và qua khi đồng thời cận dưới khoảng tin cậy 95% > 0 và chi phí stripped CIDEr-D có điểm ước lượng không thấp hơn −1.0. Mục 6.7 in chi phí −4.01, nên H_G trượt ở điều kiện chi phí. Cần thêm định nghĩa và hai điều kiện này vào Mục 5.1 hoặc Mục 6.7.
3. **Khoảng tin cậy có điều kiện theo một lần rút `rand`.** Bài nói rõ giới hạn này. Nghiên cứu phân bổ lại cho một ước lượng trên tập phát triển về tỉ phần phương sai do lần rút (Mục 6.10.5); một câu dẫn chiếu từ Mục 5.2 tới đó sẽ trả lời trước câu hỏi "khoảng tin cậy hẹp đi bao nhiêu vì bỏ qua lần rút", với điều kiện giữ nguyên câu của bài rằng không khoảng kiểm tra nào được nới hay tính lại.
4. **Đa kiểm định qua các đăng ký.** Mỗi đăng ký kiểm soát họ riêng của nó; bài không có phát biểu nào về sai số theo họ trên cả năm tập kiểm tra. Điều này chấp nhận được vì mỗi đăng ký là một câu hỏi riêng và mọi thất bại đều được in, nhưng nên nói rõ một câu ở Mục 5.4.
5. **Giá trị p.** Hồ sơ của thư mục bài (`V2_PROGRESS_C.md`) ghi tạp chí mong đợi thống kê kèm giá trị p. Bài chỉ có thống kê dạng p cho Flickr30K và nghiên cứu phân bổ. Lập trường "giá trị p thêm vào lúc này là hậu nghiệm" là đúng về phương pháp; cần giữ lập trường ấy trong thư gửi biên tập và nêu rõ ở Mục 5.4, thay vì thêm giá trị p không nhãn.
6. **Công suất.** Không có phát biểu công suất cho P1; cổng giai đoạn B có công suất khoảng 50% tại hiệu thật +4. Với XM-a, cận trên 1.97 nằm ngay dưới +2.0 (Phụ lục S), tức khoảng tin cậy 95% của XM-a không chứa giá trị +2.0; bài chỉ nêu điều này trong phụ lục và không rút kết luận nào từ đó, và người viết lại cũng không nên diễn nó thành "không có hiệu ứng".
7. **Mục 5.7 mất cân đối với vai trò của nó.** Nghiên cứu phân bổ không vào tóm tắt hay đóng góp, nhưng Mục 5.7 chiếm một phần lớn độ dài của Mục 5 và chứa nhiều chi tiết vận hành (thứ tự các giai đoạn chấm, cổng từ chối của bộ chấm, công thức trần ngân sách). Với bản tạp chí, nên giữ trong thân bài định nghĩa nhãn, quy tắc đề cử–một lần nhìn, đối chứng dương và câu đọc của cận sao chép, và chuyển phần còn lại vào phụ lục.
8. **Mốc đóng băng ở thì tương lai và các mục đã đăng ký chưa có kết cục.** Mục 5.7 ghi mốc đóng băng 12:00 ngày 16/11/2026 (UTC+7) và mô tả đầy đủ phép hoán đổi bộ nhớ trên Flickr30K val cùng họ thứ cấp S-BB cho các mô hình nền ngoài dòng Qwen; Mục 6.10 không báo cáo kết quả của hai mục này. Trước khi nộp, đoạn này phải được viết lại ở thì quá khứ và ghi rõ từng mục đã chạy hay "NOT RUN".
9. **Hai chữ "detected".** Bài phân biệt "DETECTED" (quy tắc đăng ký) với "detected" (mô tả) chỉ bằng kiểu chữ; khi dàn trang hoặc khi phản biện trích lại, sự phân biệt này dễ mất. Nên đổi một trong hai từ.

## C.7 Kết quả (Mục 6 của bài báo)

Mọi con số kiểm tra đến từ ba tệp quyết định và sổ điểm của chúng. Ngoại lệ là Mục 6.8 và 6.10 (chỉ dùng dữ liệu phát triển) và Mục 6.9 (chẩn đoán thăm dò), cả ba đều mang nhãn tương ứng. Mọi hiệu số là ghép cặp với khoảng tin cậy bootstrap 95%. Đơn vị: P1, P1b, XM-a và mọi hiệu CIDEr-D tính bằng điểm stripped CIDEr-D; P2 bằng điểm độ chính xác so khớp số lượng; XM-b bằng điểm độ chính xác đã kiểm chứng. Báo cáo này chia Mục 6 thành ba khối theo mức bằng chứng.

### C.7.1 Kết quả kiểm tra có đăng ký trên tiếng Việt (Mục 6.1–6.7)

**Nội dung.**

**Bảng C.10.** Stripped CIDEr-D (×100) theo nhánh, mỗi mô hình nền ở τ đóng băng (Bảng 6, Mục 6.1). Cột `fix` có điều kiện theo bộ cố định đã rút (ước lượng trên tập phát triển, giải mã theo lô, Mục 6.10.5).

| Tập | Mô hình nền (τ) | `ret` | `rand` | `fix` | `zs` |
|---|---|---|---|---|---|
| OV-test primary | Qwen2.5-VL (−∞) | 39.81 | 31.48 | 33.48 | 20.05 |
| OV-test primary | InternVL3 (0.10) | 33.62 | 32.96 | 33.01 | 24.77 |
| XM-test2500 | Qwen2.5-VL (−∞) | 57.70 | 54.56 | 51.83 | 43.74 |
| XM-test2500 | InternVL3 (0.10) | 52.85 | 54.59 | 53.65 | 42.84 |

Các đường cơ sở sao chép, không dùng mô hình, đạt 22.73 (NN-top1), 26.17 (NN-consensus, k = 4) và 28.96 (k = 8) trên OV-test, và 13.96, 14.61, 15.39 trên XM-test2500.

**Bảng C.11.** Kết quả đăng ký trên OpenViIC test: tập chính và tập đầy đủ (Bảng 7, Mục 6.2).

| Hàng | OV-test primary (1,941) | Phán quyết | OV-test full (2,001), độ nhạy đã đăng ký |
|---|---|---|---|
| **P1**, `ret` − `rand` gộp | **+4.49 [3.52, 5.57]** | **"PASS"** | +4.46 [3.45, 5.38] |
| P1b, Qwen2.5-VL | +8.33 [7.01, 9.76] | "confirmed" (điểm > +2.0) | +8.29 [6.99, 9.59] |
| P1b, InternVL3 (τ = 0.10) | +0.66 [−0.68, 1.99] | "reported only" | +0.63 [−0.73, 1.86] |
| **P2**, Qwen2.5-VL, ΔP_cm so với `zs` | **+5.41 [3.88, 7.01]** | **"PASS"** (cận dưới > −1.0) | +5.34 [3.88, 6.87] |
| **P2**, InternVL3, ΔP_cm so với `zs` | **+1.57 [0.65, 2.51]** | **"PASS"** (cận dưới > −1.0) | +1.35 [0.44, 2.27] |
| chênh độ dài, Qwen2.5-VL | 0.074 | L không kích hoạt (≤ 0.10) | 0.076 |
| chênh độ dài, InternVL3 | 0.039 | L không kích hoạt | 0.042 |

Câu phạm vi cho mọi số P1 gộp là "carried mainly by Qwen2.5-VL; not detected for InternVL3". P1 "PASS": ví dụ truy hồi hơn ví dụ ngẫu nhiên +4.49 [3.52, 5.57] điểm, gộp hai mô hình nền. Quy tắc L không kích hoạt: độ dài trung bình là 18.47 âm tiết (`ret`) so với 17.20 (`rand`) ở Qwen2.5-VL, và 17.02 so với 17.72 ở InternVL3. Tập chính là tập quyết định. Bài thêm một phân tích độ nhạy hậu nghiệm, không đăng ký, không có phán quyết (POST HOC): một quy tắc tương tự ảnh rộng hơn bộ lọc đã đăng ký (thêm cosine SSCD trên 0.75 làm điều kiện đủ) gắn cờ 12 trong 1,941 truy vấn chính có ít nhất một ví dụ `ret` là bản gần sao của ảnh truy vấn (9 trường hợp ở hạng 1), và 0 truy vấn ở nhánh `rand`; bỏ các truy vấn này, hiệu gộp là +4.47 [3.44, 5.41] trên 1,929 truy vấn (điểm theo ảnh như đã lưu, tần suất tài liệu không tính lại). Kết quả đăng ký giữ nguyên.

Về P1b, hàng Qwen2.5-VL +8.33 [7.01, 9.76] vượt SESOI nên dự đoán P1b "confirmed"; hàng InternVL3 ở τ = 0.10 là +0.66 [−0.68, 1.99], khoảng tin cậy chứa 0, và hàng này không mang dự đoán. Vì nhánh đăng ký của InternVL3 gồm cả bước xoá, hàng thứ cấp không có bước xoá cho thấy ở τ = −∞ hiệu `ret` − `rand` của InternVL3 trên OV-test là +3.71 [2.29, 5.14], "detected"; nó không đổi phán quyết nào. Về P2, so với chú thích không ví dụ của chính mỗi mô hình, `ret` đổi độ chính xác so khớp số lượng +5.41 [3.88, 7.01] điểm ở Qwen2.5-VL và +1.57 [0.65, 2.51] ở InternVL3; cả hai cận dưới nằm trên sàn −1.0 và cũng trên 0. Bài kết luận rằng trên OpenViIC test không thấy cái giá về độ chính xác đối tượng so với không ví dụ từ toàn bộ lời nhắc ngữ cảnh, và nhắc lại P2 không so `ret` với `rand`. Một hàng mô tả hậu nghiệm cho hiệu giữa ΔP_cm đã đăng ký của `ret` và `rand` là +2.59 ở Qwen2.5-VL (5.41 − 2.82) và +0.17 ở InternVL3 (1.57 − 1.40), không có khoảng tin cậy. Bỏ 12 truy vấn bị gắn cờ (POST HOC, không phán quyết), ΔP_cm là +5.34 [3.87, 6.82] và +1.61 [0.68, 2.56] trên 1,929 truy vấn.

**Bảng C.12.** Kết quả đăng ký trên XM-test2500 (Bảng 8, Mục 6.3).

| Hàng | XM-test2500 (2,500) | Phán quyết | Bỏ ảnh ba tham chiếu (2,392), độ nhạy đã đăng ký |
|---|---|---|---|
| **XM-a**, `ret` − `rand` gộp | **+0.70 [−0.45, 1.97]** | **"FAIL"** (khoảng tin cậy chứa 0) | +0.82 [−0.45, 2.11] |
| theo mô hình nền, Qwen2.5-VL | +3.15 [1.50, 4.93] | hàng báo cáo, không quy tắc đăng ký, khoảng không hiệu chỉnh | +3.39 [1.55, 5.16] |
| theo mô hình nền, InternVL3 (τ = 0.10) | −1.75 [−3.35, −0.09] | hàng báo cáo, không quy tắc đăng ký, khoảng không hiệu chỉnh | −1.74 [−3.39, 0.01] |
| **XM-b**, hiệu độ chính xác đã kiểm chứng `ret` so với `zs`, gộp | **+0.59 [−0.31, 1.54]** | **"PASS"** (cận dưới > −1.0) | +0.57 [−0.41, 1.56] ("PASS") |
| **dự đoán XM** (XM-a ∧ XM-b) | | **"not confirmed"** (XM-a "FAIL") | |
| ΔP_cm so với `zs`, Qwen2.5-VL (hàng báo cáo) | +0.12 [−1.20, 1.49] | | +0.19 [−1.19, 1.55] |
| ΔP_cm so với `zs`, InternVL3 (hàng báo cáo) | +0.13 [−0.83, 1.03] | | +0.13 [−0.81, 1.06] |

XM-a "FAIL": theo câu chữ đã đăng ký, "the gain was not detected out of domain (XM3600)". Điểm ước lượng +0.70 nằm trên 0 nhưng khoảng tin cậy chứa 0, nên theo quy tắc nó chỉ là số mô tả. XM-b "PASS" theo quy tắc riêng, nhưng dự đoán XM là hội của hai phần nên "not confirmed". Bài không khẳng định mức tăng chuyển sang XM3600, và cũng không khẳng định truy hồi giữ được độ chính xác đối tượng ở đó; với Qwen2.5-VL, cận dưới của hàng so khớp số lượng (−1.20) nằm dưới giá trị −1.0 dùng trên OpenViIC. Bộ nhớ không chứa chú thích XM3600 nào (tỉ lệ nguồn dữ liệu 0.000), nên XM-test2500 kiểm tra truy hồi từ một bộ nhớ thuộc miền và văn phong tham chiếu khác. Quy tắc L chỉ định nghĩa trên 1,941 ảnh; trên XM-test2500 chênh độ dài chỉ được báo cáo (0.062 và 0.028).

**Đối chứng (Mục 6.4).** Kỳ vọng đã đăng ký cho `ret` − `zs` là khoảng +10.0 gộp và S-zf không có nhãn qua; giá trị quan sát là +14.30 [13.38, 15.24] trên OV-test và +11.99 [10.68, 13.34] trên XM-test2500. So sánh `rand` − `zs` là mô tả và hậu nghiệm (không có tương phản hay khoảng tin cậy đã đăng ký): ví dụ ngẫu nhiên từ cùng bộ nhớ đã cao hơn hẳn không ví dụ với cả hai mô hình nền trên cả hai tập. `ret` − `fix` gộp là +3.47 [2.54, 4.41] trên OV-test và +2.53 [1.32, 3.80] trên XM-test2500; Qwen2.5-VL tăng trên cả hai tập (+6.33 [5.02, 7.72] và +5.87 [4.14, 7.65]), còn khoảng tin cậy của InternVL3 chứa 0 trên cả hai (+0.61 [−0.68, 1.87] và −0.81 [−2.41, 0.76]). `ret` gộp vượt NN-top1 +13.98 [12.63, 15.38] và NN-consensus +9.15 [7.84, 10.47] trên OV-test, và +41.32 [39.52, 43.08], +40.28 [38.50, 42.08] trên XM-test2500; mô hình vì thế không đơn thuần trả lại chú thích của láng giềng. Tỉ lệ sao chép gần nguyên văn của chú thích `ret` trên OV-test là 0.015 (Qwen2.5-VL) và 0.002 (InternVL3).

**Cột PTB, liều–đáp ứng và văn phong (Mục 6.5).** Với CIDEr-D tách token kiểu PTB, `ret` − `rand` gộp là +4.91 [3.93, 6.00] trên OV-test và +0.60 [−0.54, 1.85] trên XM-test2500, cùng dấu và cùng phạm vi với cột stripped. Theo tam phân vị cosine của cụm hợp lệ gần nhất, OV-test không cho mẫu hình đơn điệu: +4.40 [2.84, 6.03], +2.95 [1.14, 4.79], +6.13 [4.36, 7.87]. Trên XM-test2500 các điểm cắt (0.624, 0.680) thấp hẳn so với OV-test (0.802, 0.865), phù hợp với một bộ nhớ thuộc miền khác, và tam phân vị cao có điểm thấp nhất (+1.64 [−0.31, 3.69], +2.28 [0.13, 4.48], −1.82 [−3.96, 0.27]). Tỉ lệ ví dụ đến từ cụm có thành viên OpenViIC gần bằng một ở mọi nhánh (0.994–1.000 trên OV-test), nên `rand` và `fix` cũng cho xem chú thích trong miền, đúng như thiết kế.

**Đối tượng chỉ-từ-láng-giềng và bước xoá (Mục 6.6).** Độ chính xác đối tượng chỉ-từ-láng-giềng trên OV-test, theo nhãn vàng tham chiếu, là 73.41 [71.27, 75.34] ở Qwen2.5-VL (1,933 lần nhắc), 77.44 [70.99, 84.02] ở InternVL3 (164 lần nhắc) và 73.72 [71.72, 75.64] gộp; trên XM-test2500, theo nhãn Open Images đã xác minh, là 92.82 [89.03, 96.28] ở Qwen2.5-VL (195 lần nhắc), 16/16 ở InternVL3 (khoảng tin cậy không có thông tin) và 93.36 [89.87, 96.59] gộp. Với InternVL3 ở τ = 0.10 trên OV-test, `ret` có 0.636 lớp bị bác mỗi ảnh; 0.122 số chú thích bị sửa và 0.351 lùi về chú thích không ví dụ. Stripped CIDEr-D của nó là 33.62, so với 39.50 của cùng lượt giải mã không xoá; với `rand` là 32.96 và 35.80. Bước xoá cũng kém hơn không xoá trên các độ đo đối tượng: CHAIR_i 0.254 so với 0.237, và ΔP_cm so với `zs` +1.57 so với +5.80. Bài kết luận: "On this test set the frozen step lowered CIDEr-D without improving either object measure."

**Cơ chế chắn, giai đoạn B và hàng thứ cấp (Mục 6.7).** Cơ chế chắn là một kết quả âm có đăng ký: ở giai đoạn B, H_G không qua, với hiệu độ chính xác gộp +2.91 [0.46, 5.31] ở chi phí stripped CIDEr-D −4.01; không có khẳng định nào về cơ chế chắn ở kiểm tra. Cổng giai đoạn B qua trên OV-dev-B với `ret` − `rand` gộp +6.04 [4.54, 7.58].

**Bảng C.13.** Hàng thứ cấp có động cơ từ giai đoạn B (hậu nghiệm ở giai đoạn B, định trước cho kiểm tra): `ret` − `rand` của InternVL3 ở τ = −∞ (Bảng 9, Mục 6.7).

| Tập | InternVL3, τ = 0.10 đã đăng ký | InternVL3, τ = −∞ (thứ cấp) | Nhãn |
|---|---|---|---|
| OV-test primary | +0.66 [−0.68, 1.99] | +3.71 [2.29, 5.14] | "detected" |
| OV-test full | +0.63 [−0.73, 1.86] | +3.68 [2.20, 5.05] | "detected" |
| XM-test2500 | −1.75 [−3.35, −0.09] | +0.18 [−1.36, 1.81] | "not detected" |
| XM-test2500 bỏ ảnh ba tham chiếu | −1.74 [−3.39, 0.01] | +0.19 [−1.41, 1.79] | "not detected" |

Hàng này không đổi phán quyết hay câu phạm vi nào.

**Nhận xét rà soát.** Khối kết quả này vững: P1 "PASS" đứng được trên tập đầy đủ, trên cột PTB và sau khi bỏ 12 truy vấn bị gắn cờ; hai thất bại được in nguyên văn kèm ước lượng, khoảng tin cậy và ngưỡng. Những điểm sau cần chú ý khi viết lại.

1. **"Not detected for InternVL3" là kết quả của InternVL3 kèm bước xoá.** Câu phạm vi đã đăng ký phải giữ nguyên, nhưng tóm tắt và Mục 1 không nói rằng nhánh đăng ký của InternVL3 gồm bước xoá, trong khi chính bài cho thấy (Bảng 9) cùng lượt giải mã không xoá cho +3.71 [2.29, 5.14], "detected", trên OV-test. Quy định ở Mục 5.3 cấm đưa hàng thứ cấp vào tóm tắt như một kết quả; song vẫn có thể thêm một mệnh đề mô tả thiết kế ("nhánh đăng ký của InternVL3 gồm một bước xoá sau giải mã") để người đọc tóm tắt không quy sai cho mô hình nền. "Not detected" không được diễn thành "không có hiệu ứng".
2. **P2 của InternVL3 một phần đúng theo cấu trúc.** 0.351 số chú thích `ret` của InternVL3 là chú thích không ví dụ (Mục 3.5, Bảng S1), và Mục 6.6 cho thấy không xoá thì ΔP_cm là +5.80 thay vì +1.57. Mục 6.2 nên nhắc cả hai điều ngay cạnh phán quyết P2.
3. **P2 nói về lời nhắc ngữ cảnh, không nói về truy hồi.** Bảng S1 cho thấy `rand` cũng có ΔP_cm dương so với `zs` (2.82 và 1.40); hiệu `ret` trừ `rand` chỉ được in như mô tả hậu nghiệm không có khoảng tin cậy. Câu ở kết luận đã cẩn thận, nhưng tóm tắt và đóng góp 2 nên giữ đúng cụm "against its own zero-shot captions".
4. **Thất bại gộp của XM-a che hai hàng trái dấu.** Qwen2.5-VL +3.15 [1.50, 4.93] và InternVL3 (τ = 0.10) −1.75 [−3.35, −0.09] là hàng báo cáo không có quy tắc; ở τ = −∞ hàng InternVL3 là +0.18 [−1.36, 1.81]. Phản biện có thể cho rằng đại lượng gộp không phù hợp khi hai thành phần trái dấu; bài đã in đủ các hàng, và nên nói thẳng ở Mục 6.3 rằng số gộp trung bình hai hàng trái dấu.
5. **`rand` − `zs` trên tập kiểm tra không có khoảng tin cậy.** Luận điểm "ví dụ ngẫu nhiên trong miền đã cao hơn hẳn không ví dụ" là một nửa thông điệp của bài nhưng trên tập kiểm tra chỉ dựa vào hiệu hai mức ở Bảng 6. Bài đã có tiền lệ in hàng POST HOC từ điểm theo ảnh đã lưu (hàng bỏ 12 truy vấn); một hàng `rand` − `zs` có khoảng tin cậy, mang nhãn POST HOC, là bổ sung hợp lý nếu quy tắc của nghiên cứu cho phép, còn không thì nên dẫn tới $\tau_{\text{any}}$ trên tập phát triển (Bảng 16).
6. **Liều–đáp ứng không ủng hộ cách đọc "ảnh càng giống càng lợi".** Tam phân vị giữa trên OV-test thấp nhất và tam phân vị cao trên XM-test2500 âm; bài dùng đúng các hàng này làm giới hạn ở Mục 8.4.
7. **Hai chỗ diễn đạt cần sửa.** Mục 6.2 có cụm "PASS for Qwen2.5-VL and PASS for InternVL3 (both: passed)" lặp ý; Mục 6.4 viết `ret` gộp vượt các đường cơ sở sao chép "for both backbones", trong khi con số là số gộp và hàng theo mô hình nền nằm ở Bảng S5.

### C.7.2 Chẩn đoán trên tập phát triển và chẩn đoán thăm dò (Mục 6.8–6.9)

**Nội dung.** Mục 6.8 mang khung nhãn: "Development data only (OV-dev-B, 925 images): a mechanism analysis, non-confirmatory." Ba ablation được đăng ký sau kiểm tra, chạy một lần trên tập giai đoạn B, không đổi phán quyết nào và không vào tóm tắt hay đóng góp. Chúng giữ hai mô hình nền ở cấu hình đóng băng và đổi một yếu tố mỗi lần: ngưỡng xoá (AB-τ, chỉ InternVL3), số ví dụ k (AB-K) và cỡ bộ nhớ (AB-M). Bài công bố ba giới hạn: tập không còn mới; hai trong sáu điểm τ đã được công bố trước khi AB-τ được đăng ký; và dự đoán về k mang nhãn "shaped by stage-A dev299 selection". Bảng C.14 gom các hàng chính từ Bảng S14.

**Bảng C.14.** Các ablation trên OV-dev-B (925 ảnh), `ret` − `rand` theo stripped CIDEr-D; nhãn "development set B mechanism, non-confirmatory" (rút từ Bảng S14 và Mục 6.8).

| Ablation | Điều kiện | Qwen2.5-VL | InternVL3 | Gộp |
|---|---|---|---|---|
| AB-τ | τ = −∞ | | +5.36 [3.53, 7.12] | |
| AB-τ | τ = 0.00 | | +4.75 [2.96, 6.62] | |
| AB-τ | τ = 0.10 (đóng băng) | | +2.41 [0.57, 4.26] | |
| AB-τ | τ = 0.20 | | +2.15 [0.35, 3.97] | |
| AB-τ | τ = 0.30 | | +1.90 [0.07, 3.74] | |
| AB-τ | τ = +∞ | | +1.45 [−0.35, 3.25] | |
| AB-K | k = 2 | +6.41 [4.46, 8.49] | +1.93 [0.16, 3.63] | |
| AB-K | k = 4 | +7.11 [5.23, 9.04] | +2.41 [0.57, 4.26] | |
| AB-K | k = 8 | +9.67 [7.68, 11.72] | +2.19 [0.73, 3.76] | |
| AB-M | 10% số cụm | +5.20 [3.30, 7.03] | +1.21 [−0.45, 2.88] | +3.21 [1.87, 4.54] |
| AB-M | 30% số cụm | +7.66 [5.76, 9.44] | +0.82 [−0.97, 2.62] | +4.24 [2.90, 5.58] |
| AB-M | 100% số cụm | +9.67 [7.68, 11.72] | +2.41 [0.57, 4.26] | +6.04 [4.54, 7.58] |
| AB-M | 10% trừ 100% | −4.47 [−6.55, −2.56] | −1.20 [−2.94, 0.35] | −2.83 [−4.18, −1.58] |

Cả ba dự đoán mang kết cục "HOLDS". Theo AB-τ, tương phản của InternVL3 giảm khi τ tăng. Ví dụ truy hồi đưa vào nhiều đối tượng chỉ-từ-láng-giềng hơn (0.340 số lớp trong chú thích `ret` của InternVL3, so với 0.152 ở `rand`), nên ở τ = 0.10 bước xoá đưa 0.344 số chú thích `ret` về không ví dụ, so với 0.182 số chú thích `rand`. Trước khi xoá, các đối tượng ấy có độ chính xác theo nhãn vàng tham chiếu 77.31 (714 lần nhắc) ở `ret`: phần lớn những gì bước xoá gỡ đi được tham chiếu ủng hộ. Theo AB-K, tương phản của Qwen2.5-VL tăng theo k; của InternVL3 nằm giữa +1.93 và +2.41 sau khi xoá, nên các hàng k của nó không tách được mức hấp thu ví dụ khỏi tác động của bước xoá. Thu bộ nhớ còn 10% số cụm làm tương phản gộp giảm −2.83 [−4.18, −1.58], mẫu hình do Qwen2.5-VL mang.

Về điều ablation cho thấy và không cho thấy, bài viết: bản đăng ký cho phép mục này nói rằng ablation giải thích sự phụ thuộc mô hình nền và điều kiện đã thoả; "that permission is not used, because the ablations do not isolate a property of the backbone." Chỉ trên OV-dev-B, bước xoá đóng băng chiếm khoảng 2.95 trong phần hụt `ret` − `rand` của InternVL3 (+5.36 → +2.41). Ngay cả không có bước xoá, tương phản của InternVL3 vẫn dưới +9.67 [7.68, 11.72] của Qwen2.5-VL, dưới các cấu hình khác nhau về k, thứ tự và đuôi, nên ablation "are consistent with, but do not establish, a backbone account". Cách giải thích này không vượt ra ngoài tiếng Việt trong miền: hàng thứ cấp τ = −∞ của InternVL3 "detected" trên OV-test nhưng không trên XM-test2500 (+0.18 [−1.36, 1.81]), COCO (−1.05 [−2.22, 0.08]) hay NoCaps (+1.00 [−0.01, 2.01]). Một nhận xét hậu nghiệm, không đăng ký, không phải khẳng định: trên OV-dev-B, `rand` − `zs` là +8.91 [7.70, 10.16] gộp.

Mục 6.9 là một chẩn đoán thăm dò về việc mô hình có tự lọc được các ví dụ nó được xem trước khi viết chú thích hay không. Một nghiên cứu thăm dò có đăng ký với bộ sinh chú thích khác, mBLIP-BLOOMZ-7B [@Geigle2024mBLIP], kết thúc ở giai đoạn đầu với quyết định dừng: không biến thể nào qua biên tổn hại CIDEr định trước trên một tập chắn rút từ các nửa thăm dò của tập kiểm tra KTVIC và OpenViIC, dùng lại trong vai trò phát triển. Với hai mô hình nền của bài, chẩn đoán lọc ví dụ chưa hoàn tất: nó dừng ở bước kiểm nguồn mẫu đã đăng ký, trước bất kỳ lời gọi lọc nào, vì có ít hơn mức tối thiểu định trước 100 đơn vị đối tượng trần có nhãn sẵn ở mỗi ô. Hậu nghiệm, trên 3,000 ảnh XM-dev500 và XM-test2500 (XM-test2500 đã chấm một lần cho kiểm tra đăng ký, dùng lại ở vai trò phát triển; thăm dò, trong mẫu), mBLIP-BLOOMZ-7B dùng làm bộ lọc ví dụ cho mức đồng thuận gần ngẫu nhiên với nhãn đối tượng sẵn có (κ = 0.008 [0.005, 0.012]; hậu nghiệm, mô tả). Bài nói rõ mục này không đưa khẳng định nào về tác dụng của việc lọc lên chú thích.

**Nhận xét rà soát.** Mục 6.8 là ví dụ tốt về sự kiềm chế: quyền dùng chữ "giải thích" đã có nhưng không dùng, và lý do được nêu. Ba điểm cần sửa. (i) Mục 6.8 mang hơn mười con số nhưng không có bảng nào trong thân bài (chỉ có Bảng S14); nên đưa một bảng gọn như Bảng C.14 vào thân bài hoặc rút bớt số trong lời. (ii) Con số "about 2.95" là hiệu của hai ước lượng +5.36 và +2.41 trên cùng tập; nên in khoảng tin cậy ghép cặp của hiệu này nếu sổ điểm cho phép, hoặc nói rõ đó là hiệu của hai điểm ước lượng. (iii) Mục 6.9 dồn ba việc khác nhau vào một đoạn văn dài: một nghiên cứu mBLIP đã dừng, một chẩn đoán cho hai mô hình nền dừng trước khi chạy, và một bảng đồng thuận hậu nghiệm. Cụm "the exploration halves of the KTVIC and OpenViIC test sets" không được định nghĩa ở Mục 4 hay nơi nào khác trong bài, trong khi nó liên quan trực tiếp đến việc dùng lại tập kiểm tra sau lần nhìn (Hộp 2 có ghi). Cần định nghĩa các nửa này, nói rõ chúng được dùng lại sau hay trước lần nhìn đăng ký, và cân nhắc chuyển toàn bộ Mục 6.9 vào phụ lục, để lại hai câu trong thân bài, vì mục này không đưa khẳng định nào.

### C.7.3 Phân bổ mức tăng truy hồi trên dữ liệu phát triển (Mục 6.10) và chi phí tính toán (Mục 6.11)

**Nội dung.** Mục 6.10 mang khung nhãn: "Development data only (OV-dev-A, OV-dev-B, XM-dev500): DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY." Nghiên cứu được đăng ký sau khi mọi tập kiểm tra đã có quyết định, không đổi phán quyết nào của Mục 6.2–6.9 hay Mục 8, không vào tóm tắt hay đóng góp; OV-dev-A và OV-dev-B là tập phát triển dùng lại, nơi $\tau_{\text{sel}}$ đã biết.

**Những gì đã chạy (6.10.1).** Khối 1 giải mã theo lô các nhánh `perm`, `fix` và `rand` thêm, cùng `zs`, `ret`, `rand` d0 của Aya-Vision-8B trên XM-dev500; nó kết thúc đủ các bước đã đăng ký trong 6.41 giờ GPU của trần 12 giờ và không mang khẳng định đăng ký nào. Khối 1b giải mã lại ở cỡ lô 1 mọi nhánh đi vào một tương phản phân bổ, dưới trần cứng 17.95 giờ GPU, dùng 12.27 giờ; cả 50 lượt cỡ lô 1 đã đăng ký đều xong. Giai đoạn kiểm chứng của việc chấm qua, với mã băm lời nhắc theo ảnh của 50 lượt được so thành 50 cặp và 0 cặp khác nhau; cổng tương đương bộ chấm qua. Khối 3 giải mã các nhánh của nó ở cỡ lô 1 trên một máy thuê khác, dưới trần cứng 5.51 giờ GPU, dùng 3.72 giờ; cả mười bước đều xong.

**Thành phần lô làm đổi chú thích tham lam: cổng dừng K1 (6.10.2).** Bản đăng ký giả định chú thích của một ảnh không phụ thuộc các ảnh khác được giải mã trong cùng lô (giả định A1). Trước khi dùng bất kỳ nhánh phân bổ nào, mỗi mô hình nền giải mã lại 50 mục đầu của lượt `ret` đã lưu trên OV-dev-B hai lần trên máy mới: (a) theo thứ tự và lát lô đã lưu, so với chú thích đã lưu (tương đương máy); (b) theo thứ tự đảo ở cỡ lô 1, so với lượt (a). Mỗi phép so chỉ in số chuỗi giống hệt; qua cần đủ 50. Thất bại của (b) là cổng dừng K1.

**Bảng C.15.** Số chuỗi giống hệt ở bước kiểm A1 và phép kiểm tất định D1 (50 mục đầu; chỉ số đếm, không có điểm; Bảng S20).

| Mô hình nền | (a) tương đương máy, OV-dev-B | (a) tương đương máy, OV-dev-A | (b) A1: đảo thứ tự, cỡ lô 1, so với (a) | K1 | D1: cỡ lô 1, thứ tự lưu so với đảo |
|---|---|---|---|---|---|
| Qwen2.5-VL-7B | 50/50 | 50/50 | 42/50 | "FAIL (K1 fired)" | 50/50, "PASS" |
| InternVL3-8B | 50/50 | 50/50 | 37/50 | "FAIL (K1 fired)" | 50/50, "PASS" |
| Aya-Vision-8B | 50/50 | – | 31/50 | "FAIL (K1 fired)" | 50/50, "PASS" |

Câu báo cáo đã đăng ký được áp dụng: "K1 fired: no backbone met A1 under registration v1.1; block 1 as registered carries no claim." Không quy tắc đề cử nào được tính trên lượt giải mã theo lô; một tệp đề cử với không khẳng định nào được ghi, kèm lý do K1, trước khi có bất kỳ điểm số nào. Bài diễn giải: phép kiểm (a) cho thấy một lượt giải mã tái lập được khi biết lô của nó; phép kiểm (b) cho thấy nó không bất biến theo lô, vì 8, 13 và 19 trong 50 chú thích tham lam đổi khi cùng ảnh được giải mã từng cái một. D1 cho thấy ở cỡ lô 1 thứ tự mục không đổi chú thích nào, nên khác biệt ở (b) đi cùng thay đổi thành phần lô chứ không cùng thay đổi thứ tự. Một cách đọc mã giải mã, làm sau khi K1 kích hoạt và chưa được kiểm chứng, là các ảnh cùng lô làm đổi phần đệm và hình dạng phép tính số, và khác biệt số nhỏ có thể lật một lựa chọn tham lam. Vì các nhánh khác nhau ở khối ví dụ nên lời nhắc có độ dài và phần đệm khác nhau; hiệu theo ảnh giữa hai nhánh giải mã theo lô vì thế có thể chứa một số hạng do bạn cùng lô, khác nhau theo nhánh; lát lô cố định không khử được nó, và bootstrap theo ảnh không thấy sự ràng buộc giữa các ảnh trong một lát. Bài cũng nêu điều phép kiểm không cho thấy: không điểm số nào được so (K1 chỉ dựa trên đồng nhất chuỗi); nó không nói gì về chất lượng chú thích, về dấu hay độ lớn của khác biệt điểm, hay chính sách giải mã nào tốt hơn; "it does not show that any batched result of this paper is biased"; nó chỉ phủ ba mô hình, một ngăn xếp phần mềm và 50 mục OV-dev-B mỗi mô hình.

Hệ quả cho bài: mọi tương phản đăng ký giữa hai nhánh ví dụ văn bản của một mô hình nền (giai đoạn A và B, kiểm tra tiếng Việt và tiếng Anh, đăng ký Flickr30K) được giải mã theo lô cố định với cùng chính sách lô cho cả hai nhánh; bản cài đặt lại LMCap và nhánh ảnh–chú thích xen kẽ được giải mã từng truy vấn một, nên tương phản của chúng với `ret` của một mô hình nền (Bảng 13, 14 và S19) đặt một lượt cỡ lô 1 cạnh một lượt theo lô. Mọi hàng ấy là kết quả của hệ thống như đã chạy; không số nào đổi và không hàng nào đổi nhãn. Các phép kiểm tương đương giải mã báo cáo trước đây là 52/52 chú thích giống hệt chỉ cho thấy tương đương giữa các lần chạy, không phải bất biến theo lô. Hệ quả cho nghiên cứu phân bổ: phụ lục phiên bản 1.2 đổi cỡ lô và phép kiểm A1; mọi nhánh của tương phản được giải mã lại ở cỡ lô 1 với cùng lời nhắc, ảnh chụp mô hình và môi trường; A1 được thay bằng D1, và D1 qua cho cả ba mô hình nền. Mọi hàng phân bổ ở Bảng 15, 16, S21 và S23(a) đến từ giải mã cỡ lô 1 và mang nhãn "batch size 1; registered in v1.2 after K1 fired, on string-identity counts only"; các hàng khối 1 theo lô chỉ được in như hàng mô tả với nhãn "A1 not met; batched decode; descriptive".

**Khẳng định đã đăng ký: đề cử rồi một lần nhìn (6.10.3).**

**Bảng C.16.** Đề cử trên OV-dev-A (911 ảnh) ở cỡ lô 1; R = 1, D = 2; quy tắc: đề cử nếu cận dưới 95% ít nhất +2.0 (Bảng 15, Mục 6.10.3). Mọi hàng: DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY.

| Mô hình nền | Đại lượng | Hiệu [khoảng tin cậy 95%] | Ghi chú | Được đề cử? |
|---|---|---|---|---|
| Qwen2.5-VL-7B | τ_pair | +7.43 [5.54, 9.20] | split of a known τ_sel | có |
| Qwen2.5-VL-7B | τ_marg | −0.06 [−1.38, 1.30] | split of a known τ_sel | không |
| Qwen2.5-VL-7B | τ_sel | +7.37 [5.48, 9.33] | batch-1 re-decode of a known τ_sel | không phải ứng viên |
| InternVL3-8B (τ = −∞) | τ_pair | +4.96 [3.12, 6.82] | split of a known τ_sel | có |
| InternVL3-8B (τ = −∞) | τ_marg | −1.43 [−2.78, −0.08] | split of a known τ_sel | không |
| InternVL3-8B (τ = −∞) | τ_sel | +3.53 [1.64, 5.39] | batch-1 re-decode of a known τ_sel | không phải ứng viên |

Hai khẳng định thoả quy tắc đề cử: H_pair(Qwen2.5-VL-7B) và H_pair(InternVL3-8B); chúng tạo một họ Holm cỡ m = 2 ở α một phía theo họ 0.025.

**Bảng C.17.** Một lần nhìn trên OV-dev-B (925 ảnh) ở cỡ lô 1; R = 3 lần rút `rand` và D = 2 hoán vị lấy trung bình theo ảnh; B = 2,000 (Bảng 16, Mục 6.10.3). Mọi hàng: DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. "Sàn" là sàn 1/2,001 của thống kê dạng p.

| Mô hình nền | Đại lượng | Hiệu [khoảng tin cậy 95%] | p̃ | Họ, m | Nhãn | Ghi chú |
|---|---|---|---|---|---|---|
| Qwen2.5-VL-7B | τ_pair | +7.30 [5.58, 9.25] | sàn | được đề cử, 2 | "DETECTED" | split of a known τ_sel |
| Qwen2.5-VL-7B | τ_marg | +0.96 [0.01, 1.94] | 0.0235 | không, 1 | "NEGLIGIBLE" | split of a known τ_sel |
| Qwen2.5-VL-7B | τ_sel | +8.27 [6.54, 10.11] | sàn | không, 1 | "DETECTED" | batch-1 re-decode of a known τ_sel |
| InternVL3-8B (τ = −∞) | τ_pair | +5.57 [3.94, 7.27] | sàn | được đề cử, 2 | "DETECTED" | split of a known τ_sel |
| InternVL3-8B (τ = −∞) | τ_marg | −0.35 [−1.40, 0.70] | 0.749 | không, 1 | "NEGLIGIBLE" | split of a known τ_sel |
| InternVL3-8B (τ = −∞) | τ_sel | +5.22 [3.67, 6.81] | sàn | không, 1 | "DETECTED" | batch-1 re-decode of a known τ_sel |
| Aya-Vision-8B | τ_pair | +6.78 [5.33, 8.30] | sàn | không, 1 | "DETECTED" | lần nhìn đầu, không khẳng định đăng ký |
| Aya-Vision-8B | τ_marg | −0.53 [−1.46, 0.41] | 0.874 | không, 1 | "NEGLIGIBLE" | lần nhìn đầu; giả dược bị gắn cờ |
| Aya-Vision-8B | τ_sel | +6.25 [4.87, 7.69] | sàn | không, 1 | "DETECTED" | giả dược bị gắn cờ |
| Qwen2.5-VL-7B | τ_any | +11.10 [9.73, 12.44] | sàn | không, 1 | "DETECTED" | – |
| InternVL3-8B (τ = −∞) | τ_any | +10.47 [9.06, 11.82] | sàn | không, 1 | "DETECTED" | – |
| Aya-Vision-8B | τ_any | +13.85 [12.71, 15.11] | sàn | không, 1 | "DETECTED" | giả dược bị gắn cờ |

Phán quyết của hai khẳng định được đề cử, theo câu chữ của bài: "H_pair(Qwen2.5-VL-7B): PASS" với $\tau_{\text{pair}}$ = +7.30 [5.58, 9.25] (ngưỡng Holm 0.025, m = 2) và "H_pair(InternVL3-8B): PASS" với +5.57 [3.94, 7.27] (ngưỡng Holm 0.0125, m = 2); cả hai kèm câu "the nominated split held on a re-used development set, at batch size 1. This is a split of a known τ_sel, not new evidence that retrieval helps." Với $\tau_{\text{marg}}$ của Qwen2.5-VL-7B (+0.96, khoảng 90% [0.17, 1.74]), bài ghi chú rằng khoảng 95% của nó không chứa 0 và "NEGLIGIBLE means inside ±2.0, not zero"; nhãn này có công suất thấp theo thiết kế: ở sai số chuẩn hoạch định của Qwen2.5-VL-7B trên OV-dev-B (khoảng 1.03) nó cần điểm ước lượng trong khoảng ±0.3 quanh 0. Khoảng 90% của hai hàng $\tau_{\text{marg}}$ còn lại là [−1.18, 0.53] (InternVL3-8B) và [−1.31, 0.27] (Aya-Vision-8B). Tính lại tần suất tài liệu trong 200 lần lấy mẫu lại (Bảng S25a) cho khoảng [5.69, 9.13] so với [5.65, 9.14] ở $\tau_{\text{pair}}$ và [0.17, 1.89] so với [0.08, 1.94] ở $\tau_{\text{marg}}$; hàng này mô tả, không có quy tắc.

**XM-dev500 ở cỡ lô 1 (6.10.4).** Các hàng không mang quy tắc. Theo Bảng S21, $\tau_{\text{sel}}$ của cả ba mô hình nền mang nhãn "UNRESOLVED" (+1.79 [−1.30, 4.95], +0.11 [−2.82, 3.31], +1.74 [−1.09, 4.53]), còn $\tau_{\text{any}}$ mang nhãn "DETECTED" (+12.14 [8.86, 15.40], +13.77 [10.33, 17.32], +23.98 [20.43, 27.93]); không hàng XM-dev500 nào vào một họ hay câu phạm vi.

**Giả dược, thành phần phương sai và bộ cố định (6.10.5).** Giả dược `rand` d1 − d2 của Aya-Vision-8B trên OV-dev-B bị gắn cờ (−2.03 [−3.42, −0.74]). Một lần rà soát có ghi lại thấy cờ chỉ giới hạn ở Aya-Vision-8B: InternVL3-8B được xem cùng danh sách `rand` d1 và d2, và giả dược của nó lẫn của Qwen2.5-VL-7B không bị gắn cờ; các khẳng định được đề cử dựa trên $\tau_{\text{pair}}$, đại lượng không chứa nhánh `rand`. Lần rút ngẫu nhiên chiếm tỉ phần 0.089, 0.163 và 0.149 của phương sai bootstrap theo ảnh của $\tau_{\text{sel}}$ lấy trung bình qua các lần rút trên OV-dev-B (Qwen2.5-VL-7B, InternVL3-8B, Aya-Vision-8B), và 0.160, 0.192, 0.203 trên XM-dev500. Với năm bộ cố định trên OV-dev-B, $\hat\omega$ = 2.51 và $\omega^U$ = 15.20; trên XM-dev500, $\hat\omega$ = 0.44 và $\omega^U$ = 4.21. Theo quy tắc đã đăng ký, mọi hàng `fix` của bài có điều kiện theo bộ cố định đã rút; các hàng này đến từ giải mã theo lô, và không khoảng tin cậy kiểm tra nào được nới, tính lại hay đổi nhãn bằng số này.

**Cận sao chép (6.10.6).**

**Bảng C.18.** Cận sao chép ở n = 3 trên các lượt giải mã đã lưu (Bảng 17, Mục 6.10.6). OV-dev-B: POST HOC. XM-dev500: lần nhìn đầu vào κ. Các hàng đặt cận cho tương phản `ret` − `rand` d0 đã lưu, giải mã theo lô. Mọi cận đều "in force".

| Tập | Mô hình nền | Đơn vị | K_ret, nhãn | L_cp, nhãn | K_nc, nhãn |
|---|---|---|---|---|---|
| OV-dev-B | Qwen2.5-VL-7B | âm tiết | +18.58 [16.56, 20.73], "DETECTED" | −8.91 [−10.71, −7.07], "REVERSED" | +5.59 [4.41, 6.75], "DETECTED" |
| OV-dev-B | Qwen2.5-VL-7B | từ | +18.74 [16.71, 20.84], "DETECTED" | −9.08 [−10.98, −7.22], "REVERSED" | +5.76 [4.71, 6.95], "DETECTED" |
| OV-dev-B | InternVL3-8B (τ = −∞) | âm tiết | +9.93 [8.31, 11.60], "DETECTED" | −4.57 [−6.46, −2.61], "REVERSED" | +2.65 [1.61, 3.76], "DETECTED" |
| OV-dev-B | InternVL3-8B (τ = −∞) | từ | +8.99 [7.48, 10.57], "DETECTED" | −3.64 [−5.55, −1.69], "REVERSED" | +2.91 [1.88, 3.94], "DETECTED" |
| OV-dev-B | Aya-Vision-8B | âm tiết | +9.02 [7.83, 10.27], "DETECTED" | −1.70 [−3.28, −0.13], "REVERSED" | +3.50 [2.74, 4.30], "DETECTED" |
| OV-dev-B | Aya-Vision-8B | từ | +7.88 [6.73, 9.11], "DETECTED" | −0.57 [−2.16, 0.99], "NEGLIGIBLE" | +2.55 [1.90, 3.25], "DETECTED" |
| XM-dev500 | Qwen2.5-VL-7B | âm tiết | +14.25 [11.59, 17.04], "DETECTED" | −9.81 [−13.67, −5.63], "REVERSED" | +7.59 [5.36, 10.00], "DETECTED" |
| XM-dev500 | Qwen2.5-VL-7B | từ | +13.23 [10.70, 15.96], "DETECTED" | −8.78 [−12.87, −4.73], "REVERSED" | +7.07 [5.12, 9.12], "DETECTED" |
| XM-dev500 | InternVL3-8B (τ = −∞) | âm tiết | +6.37 [4.35, 8.59], "DETECTED" | −4.82 [−8.72, −1.10], "REVERSED" | +4.27 [2.25, 6.49], "DETECTED" |
| XM-dev500 | InternVL3-8B (τ = −∞) | từ | +4.92 [3.37, 6.65], "DETECTED" | −3.38 [−7.17, 0.28], "UNRESOLVED" | +3.33 [1.81, 5.07], "DETECTED" |
| XM-dev500 | Aya-Vision-8B | âm tiết | +7.18 [5.35, 8.98], "DETECTED" | −6.36 [−10.11, −3.02], "REVERSED" | +5.00 [3.47, 6.73], "DETECTED" |
| XM-dev500 | Aya-Vision-8B | từ | +5.69 [4.03, 7.45], "DETECTED" | −4.87 [−8.61, −1.51], "REVERSED" | +4.09 [2.66, 5.73], "DETECTED" |

Hai hàng Aya-Vision-8B trên OV-dev-B mang cờ vì $L_{\text{cp}}$ và $K_{\text{nc}}$ chứa `rand` (giả dược bị gắn cờ); hai hàng Aya-Vision-8B trên XM-dev500 dùng lượt giải mã theo lô ("A1 not met; batched decode; descriptive"). Với mọi hàng, điểm $L_{\text{cp}}$ không dương nên câu đọc đã đăng ký được áp dụng: "the bound does not exclude that the whole retrieval-specific effect is carried by copied n-grams; this agrees with, and does not prove, the published short-cut account" [@Li2025UnveilingICL]. Cận sao chép tiếng Anh trên phần tách và val của Flickr30K, đã đăng ký như một hàng hậu nghiệm, "was not coded and was not run". Hàng đồng hành hậu nghiệm về nguồn bộ nhớ, trên 1,000 ảnh Flickr30K train, cho δ = −5.44 [−9.07, −2.04] ở Qwen2.5-VL-7B ("REVERSED") và −0.01 [−3.42, 3.36] ở Aya-Vision-8B ("UNRESOLVED"); hai bộ nhớ khác cả cỡ lẫn nguồn (111,927 so với 28,000 cụm) nên δ không tách nguồn khỏi cỡ, và không câu đọc đã đăng ký nào được áp cho nó; quy tắc L cho bốn ô đều ghi "NOT RUN". Các hàng theo lô của khối 1 (6.10.7, Bảng S22) được in cạnh hàng cỡ lô 1 như hàng độ nhạy mô tả.

**Đối chứng dương và các nhánh bên thứ ba (6.10.8).**

**Bảng C.19.** Các nhánh bên thứ ba ở cỡ lô 1, khối 3; một lần rút `rand` (d0) và một hoán vị (p = 1); m = 1 ở mọi hàng (Bảng 18, Mục 6.10.8). Mọi hàng: DEVELOPMENT / C-ATTR-DEV, NON-CONFIRMATORY. LMCap là bản cài đặt lại của nghiên cứu.

| Tập | Hệ | Đại lượng | Hiệu [khoảng tin cậy 95%] | p̃ | Nhãn | Ghi chú |
|---|---|---|---|---|---|---|
| OV-dev-B | LMCap | τ_sel | +16.92 [15.00, 19.06] | sàn | "DETECTED" | đối chứng dương đã đăng ký; lần nhìn đầu |
| OV-dev-B | LMCap | τ_pair | +17.40 [15.48, 19.41] | sàn | "DETECTED" | lần nhìn đầu; tính sau τ_sel |
| OV-dev-B | LMCap | τ_marg | −0.48 [−1.27, 0.28]; 90% [−1.14, 0.17] | 0.891 | "NEGLIGIBLE" | lần nhìn đầu; tính sau τ_sel |
| OV-dev-B | Qwen2.5-VL-7B, định dạng ảnh | τ_sel | +6.36 [4.30, 8.46] | sàn | "DETECTED" | lần nhìn đầu |
| OV-dev-B | Qwen2.5-VL-7B, ví dụ văn bản (đặt cạnh) | τ_sel | +8.27 [6.54, 10.11] | xem Bảng C.17 | "DETECTED" | khối 1b |
| XM-dev500 | LMCap | τ_sel | +16.58 [13.91, 19.19] | sàn | "DETECTED" | không quy tắc; không rút kết luận |
| XM-dev500 | LMCap | τ_pair | +17.02 [14.43, 19.42] | sàn | "DETECTED" | không quy tắc; không rút kết luận |
| XM-dev500 | LMCap | τ_marg | −0.44 [−1.50, 0.49]; 90% [−1.31, 0.38] | 0.810 | "NEGLIGIBLE" | không quy tắc; không rút kết luận |
| XM-dev500 | Qwen2.5-VL-7B, định dạng ảnh | τ_sel | +2.27 [−1.19, 5.92] | 0.101 | "UNRESOLVED" | không quy tắc; không rút kết luận |
| XM-dev500 | Qwen2.5-VL-7B, ví dụ văn bản (đặt cạnh) | τ_sel | +1.79 [−1.30, 4.95] | – | "UNRESOLVED" | khối 1b; không quy tắc |

Đối chứng dương đạt: thay chú thích truy hồi của LMCap bằng chú thích ngẫu nhiên làm điểm giảm, +16.92 [15.00, 19.06], "DETECTED". Bài nêu kỹ giới hạn của nó. Quy tắc tương phản và nhãn đã trả về "DETECTED" trong một ca mà đáp án biết trước, là bằng chứng rằng các nhánh, đường chấm của các hàng này và các quy tắc bootstrap, nhãn có thể phát hiện một hiệu ứng riêng của truy hồi khi nó có mặt. Hiệu ứng bằng khoảng 8.5 lần SESOI, nên đối chứng không nói gì về độ nhạy quanh +2.0: xác suất hoạch định để có "DETECTED" tại hiệu thật +2.0 trên OV-dev-B vẫn khoảng 0.49. Nó không có đối chứng âm nên không nói gì về tần suất "DETECTED" khi không có hiệu ứng; các hàng giả dược `rand` d1 − d2 là phép kiểm duy nhất loại đó, và một trong số chúng bị gắn cờ. Nó không xác nhận lại hay củng cố các hàng của Mục 6.10.3, và không nói gì về số đã công bố của LMCap, về tập kiểm tra nào hay về XM-dev500. Về phép tách của LMCap trên OV-dev-B, hiệu ứng riêng của truy hồi nằm ở việc ghép chú thích với truy vấn ($\tau_{\text{pair}}$ "DETECTED"), còn phần do tập chú thích được đưa nhỏ hơn 2.0 điểm theo cả hai chiều ($\tau_{\text{marg}}$ "NEGLIGIBLE"): cùng mẫu hình nhãn với hai mô hình nền ở Mục 6.10.3, và bài viết "This is a description, not a check of those rows." Hai hàng định dạng ảnh và ví dụ văn bản được giải mã trên máy khác nhau, ở khối khác nhau; không hiệu số hay tỉ số nào giữa chúng được tính và không hàng nào được gọi là lớn hơn.

**Chi phí tính toán (Mục 6.11).** Kiểm tra dùng 9.59 giờ GPU trong trần 20 giờ trên một GPU 24 GB (khối OpenViIC 4.61, khối XM3600 4.90, kiểm tương đương giải mã trước kiểm tra 0.08). Các giai đoạn phát triển dùng 6.84 và 4.91 giờ GPU dưới một trần riêng. Nghiên cứu phân bổ dùng 6.41 giờ ở khối 1 (trần 12), 12.27 ở khối 1b (trần 17.95) và 3.72 ở khối 3 (trần 5.51; trong đó 0.02 thuộc lần khởi chạy đầu dừng ở bước nạp mô hình).

**Nhận xét rà soát.** Mục 6.10 đưa ra hai điều đáng giá: một phát hiện phương pháp (thành phần lô làm đổi chú thích tham lam) và một phép tách nhất quán qua ba mô hình nền và LMCap (phần riêng của truy hồi nằm ở việc ghép danh sách với ảnh, phần biên "NEGLIGIBLE"). Cả hai là kết quả trên tập phát triển dùng lại và bài gắn nhãn đúng như vậy. Các điểm cần xử lý:

1. **Hệ quả của K1 đối với các kết quả đăng ký cần một câu trả lời định lượng.** Bài nói K1 không cho thấy kết quả theo lô nào bị chệch, và điều đó đúng vì K1 chỉ so chuỗi. Nhưng phản biện sẽ hỏi độ lớn. Bài đã có sẵn hai hàng cạnh nhau trên cùng tập: $\tau_{\text{sel}}$ theo lô ở Bảng S22 (Qwen2.5-VL-7B trên OV-dev-B: +9.25 [7.59, 11.14]) và ở cỡ lô 1 ở Bảng 16 (+8.27 [6.54, 10.11]); tương tự +5.19 [3.63, 6.79] so với +5.22 [3.67, 6.81] ở InternVL3-8B và +6.78 [5.33, 8.33] so với +6.25 [4.87, 7.69] ở Aya-Vision-8B. Bài không tính hiệu giữa hai chính sách và không nên tự tính ngoài đăng ký; nhưng Mục 9.1 nên chỉ thẳng tới cặp bảng này để người đọc thấy hai chính sách cho cùng nhãn trên tập phát triển.
2. **Bảng S22 và Bảng S16 in hai giá trị khác nhau cho cùng một tương phản theo lô.** $\tau_{\text{sel}}$ theo lô của Qwen2.5-VL-7B trên OV-dev-B là +9.25 [7.59, 11.14] ở Bảng S22 nhưng `ret` − `rand` giai đoạn B của cùng mô hình, cùng tập là +9.67 [7.68, 11.72] ở Bảng S16. Bảng S22 ghi R = 3 cho hàng này, còn cổng giai đoạn B dùng một phép gán `rand` cho mỗi ảnh; bài không nói đây có phải nguyên nhân của khác biệt hay không, nên cần một chú thích dưới Bảng S22.
3. **Giả dược bị gắn cờ chạm tới giả định của mọi khoảng tin cậy kiểm tra.** Hai lần rút `rand` của Aya-Vision-8B trên OV-dev-B lệch nhau −2.03 [−3.42, −0.74], cỡ ngang SESOI, trong khi mọi khoảng tin cậy kiểm tra có điều kiện theo một lần rút duy nhất. Bài xử lý cờ bằng một lần rà soát và ghi rằng nó chỉ giới hạn ở Aya-Vision-8B; các tỉ phần phương sai (0.089 đến 0.203) là câu trả lời định lượng duy nhất. Mục 9.1 nên nối hai điều này lại thay vì để chúng ở hai nơi.
4. **Nhãn trên một cận dễ bị hiểu sai.** $L_{\text{cp}}$ là cận dưới; nhãn "REVERSED" trên nó chỉ nói khoảng của cận nằm dưới 0, tức cận không có thông tin, chứ không nói hiệu ứng bị đảo dấu. Ngoài ra $K_{\text{nc}}$ mang nhãn "DETECTED" ở mọi hàng với giá trị lớn (ví dụ +5.59 khi $K_{\text{ret}}$ là +18.58): chú thích `rand`, vốn không thể chép $R_q$, vẫn mất nhiều điểm hơn `zs` khi bị che. Bài coi đây là chiều sai lệch đã dự liệu của A_cp (cận vẫn "in force"), nhưng nên nói rõ bằng lời rằng khi đó $K_{\text{ret}}$ nói quá mức sao chép và cận dưới trở nên vô dụng, thay vì chỉ lặp câu đọc đã đăng ký.
5. **Văn bản lặp theo khuôn.** Mục 6.10.3, 6.10.5 và 6.10.6 lặp cùng một câu cho từng hàng (riêng câu đọc của cận sao chép xuất hiện mười hai lần, câu về công suất của nhãn "NEGLIGIBLE" ba lần). Thông tin ấy đã có trong bảng; với bản tạp chí cần rút thành một câu cho mỗi bảng.
6. **Các mục đã đăng ký không có kết cục.** Bài mô tả khối 0, 1, 1b và 3 nhưng không nhắc khối nào mang số 2; phép hoán đổi bộ nhớ trên Flickr30K val (Mục 5.7) và họ thứ cấp S-BB không có hàng kết quả, cũng không có dòng "NOT RUN" như bài đã làm với cận sao chép tiếng Anh. Cần bổ sung trạng thái của từng mục.
7. **Thứ tự đánh số bảng.** Bảng 15–18 nằm ở Mục 6.10, trước Bảng 10–14 của Mục 8; tạp chí yêu cầu đánh số theo thứ tự xuất hiện.
8. **Tỉ trọng của Mục 6.10.** Một phân tích không vào tóm tắt hay đóng góp chiếm phần lớn Mục 6. Người viết lại nên quyết định dứt khoát: hoặc nâng nó thành một phần của thông điệp (khi đó tóm tắt phải nhắc và nhãn "development, non-confirmatory" phải đi kèm), hoặc chuyển phần lớn vào phụ lục. Dạng hiện tại vừa dài vừa tự phủ nhận vai trò của mình.

## C.8 Các công bố minh bạch (Mục 7 của bài báo)

**Nội dung.** Mục 7 liệt kê mọi sai lệch và mọi tiếp xúc đã chạm tới phép kiểm tra đăng ký, cùng mọi quyết định chia tập mà người đọc cần để đánh giá nó. Bài khẳng định không điều nào trong số đó làm đổi cấu hình, ngưỡng, độ đo, tập hay quy tắc sau khi có đầu ra kiểm tra. Bảng C.20 tóm lược Hộp 2 của bài; ở mọi hàng, cột "phán quyết có đổi không" của bài đều ghi "no".

**Bảng C.20.** Tóm lược các công bố (Hộp 2, Mục 7).

| Mục công bố | Tác động lên dữ liệu | Tiếp xúc với dữ liệu kiểm tra |
|---|---|---|
| kiểm tương đương giải mã trước kiểm tra cần ba lần thử | chỉ ảnh phát triển (52/52 chú thích giống hệt mỗi mô hình nền ở lần kiểm chính thức; cùng mục, cùng lát lô, nên là tương đương giữa các lần chạy, không phải bất biến theo lô) | không |
| khối XM3600 chạy từ một cây làm việc ghim ở lần cam kết kiểm tra | không; khác biệt mã kiểm tra giữa hai lần cam kết là rỗng | không |
| ba tệp OpenViIC test bị cắt cụt được giải mã theo quy tắc thử lại cố định | không tệp nào bị loại | không |
| 60 ảnh bị loại khỏi tập chính bởi bộ lọc định trước | tập đầy đủ 2,001 được báo cáo cạnh | không |
| hậu nghiệm: 12 truy vấn chính có bản gần sao của ảnh truy vấn trong ví dụ `ret` theo quy tắc rộng hơn | có hàng hậu nghiệm bỏ chúng | không |
| mã băm, mã ảnh và số tham chiếu của ảnh kiểm tra được đọc trên CPU để ghim danh sách | không có đầu ra mô hình | mã, byte, số đếm; không dùng chú thích nào |
| một nghiên cứu khác đã giải mã không ví dụ 121 ảnh XM-dev500 | chỉ giai đoạn B | không trên tập kiểm tra nào |
| một dự án không liên quan đã kiểm trước tham chiếu UIT-ViIC | không | tham chiếu tiếng Anh, ở dạng tổng hợp |
| hàng theo mô hình nền được trích trong tóm tắt và đóng góp | không | không |
| nhánh tiếng Anh đăng ký sau các phán quyết tiếng Việt; quy tắc NoCaps cố định sau XM-a | không | không |
| các hàng của bộ chấm mà không quy tắc nào đăng ký | chỉ ở Bảng S12 | không |
| đăng ký Flickr30K viết sau khi bốn tập kiểm tra trước đã có quyết định; tham chiếu Flickr30K test đã được một nghiên cứu đồng hành đọc từ trước | không | chỉ tham chiếu, trước đăng ký; không có đầu ra hệ thống trên ảnh kiểm tra |
| tập kiểm tra dùng lại sau lần nhìn, ở vai trò phát triển, bởi các chẩn đoán lọc thăm dò | chỉ hàng thăm dò | ảnh và nhãn đã nhìn được đọc lại; không có lần nhìn đăng ký mới |
| nghiên cứu phân bổ đăng ký sau mọi phán quyết kiểm tra, trên tập phát triển dùng lại nơi $\tau_{\text{sel}}$ đã biết | chỉ hàng phát triển, có nhãn | không |
| K1 kích hoạt; khối 1b ở cỡ lô 1 đăng ký sau K1, trước mọi điểm số | hàng theo lô chỉ mang tính mô tả | không |
| kiểm tra đột biến mã của khối 1 không chạy trên máy thuê; chấp nhận bản ghi trên máy tính của tác giả; các lần chạy sau không cô lập mạng | không | không |
| các kiểm tra CPU khác chạy cạnh lượt giải mã; danh sách mã kiểm của cây kết quả thiếu các dòng nhật ký cuối | không | không |
| khối 3: lần khởi chạy đầu dừng ở bước nạp mô hình; hai nhánh OV-dev-B giải mã lại; kiểm tra mã chấm làm trước trong bản nháp rồi lặp lại trong cây đã cam kết; việc khác chạy trên máy lúc giải mã; một đính chính tài liệu chạy được cam kết sau khi giải mã | tương phản khối 3 chỉ dùng lượt giải mã khối 3; không tác động nào khác được kiểm | không |

Đoạn tóm tắt sai lệch viết: bản đăng ký kiểm tra tiếng Việt cấm các hàng thứ cấp xuất hiện như kết quả trong tên bài, tóm tắt và đóng góp; thông tin theo mô hình nền bằng tiếng Việt trong tóm tắt và đóng góp là câu phạm vi đã đăng ký nên hợp lệ. Bản đăng ký tiếng Anh không có quy định ấy; theo Mục 7, tóm tắt và đóng góp trích hàng COCO theo mô hình nền của InternVL3 làm ngữ cảnh mô tả, "because the pooled number alone would overstate the effect", và không phán quyết nào phụ thuộc vào nó.

Các tiểu mục chi tiết hoá bảng trên. Mục 7.1 nhắc rằng KTVIC dev299 không phải tập mới: phần tách gốc của nó đã dùng để đặt tuỳ chọn giải mã cho một nghiên cứu đồng hành. Mục 7.2 nói về tiếp xúc trước với dữ liệu kiểm tra: các kịch bản CPU đọc khoá chú giải, byte ảnh và số tham chiếu mà không dùng, in hay ghi chú thích nào; UIT-ViIC không phải dữ liệu của nghiên cứu, chỉ xuất hiện qua công bố này, và bài không tuyên bố có sự cho phép nào từ tác giả UIT-ViIC. Mục 7.3 nêu các hàng không quy tắc nào đăng ký (InternVL3 ở τ ∈ {0.00, 0.20, 0.30, +∞}, Qwen2.5-VL ở τ = +∞, AUROC của mô hình kiểm chứng), chỉ có ở Bảng S12. Mục 7.4 nói nhánh tiếng Anh là một nghiên cứu đăng ký riêng: quyết định so sánh tiếng Anh được đưa ra trong ngày kiểm tra tiếng Việt, sau khi khối OpenViIC bắt đầu và trước khi tệp quyết định tiếng Việt đầu tiên tồn tại; bản đăng ký tiếng Anh được viết sau khi biết phán quyết tiếng Việt và điều này được công bố. Mục 7.5 dành cho nghiên cứu phân bổ: thứ tự các khối; việc kiểm tra đột biến mã không chạy được trên máy thuê do cơ chế cô lập mạng, và một lần rà soát có ghi lại chấp nhận bản ghi của cùng lượt kiểm trên mã giống từng byte (22 trên 22 đột biến bị diệt), còn các lượt sau (33 trên 33, 73 trên 73, và 107 trên 107 ở khối 3) chạy không cô lập mạng; danh sách mã kiểm của cây đầu ra; khác biệt phiên bản môi trường; công việc CPU của nghiên cứu khác chạy trên cùng máy trong lúc khối 1, 1b và 3 giải mã, trái với quy tắc "không việc nào chạy cạnh việc khác" của đăng ký và được công bố như sai lệch, kèm câu "Whether CPU load can change a greedy GPU string was not tested"; bốn lỗi bộ chấm được sửa trước khi có điểm số; và danh sách những gì là hậu nghiệm (cận sao chép trên OV-dev-B, các hàng phương sai của ba mô hình nền đã lưu trên OV-dev-B, hàng đồng hành nguồn bộ nhớ, và chính thiết kế cỡ lô 1, vốn được đăng ký sau K1 dù trước mọi điểm số). Mục cuối ghi một tiếp xúc trước đáng chú ý: trước khi đăng ký phân bổ được viết, các phép kiểm lô đầu ở hai nghiên cứu khác của nhóm đã ghi nhận một số chú thích không giống hệt giữa giải mã theo lô và từng ảnh; các số đếm ấy đã được thấy nhưng chưa phân tích, và đăng ký vẫn giả định A1 rồi kiểm nó bằng K1.

**Nhận xét rà soát.** Mức độ công bố của Mục 7 cao hơn thông lệ và là một tài sản của bài. Có ba vấn đề.

1. **Mục 7 và tóm tắt nói khác nhau về hàng COCO của InternVL3.** Đoạn tóm tắt sai lệch và Hộp 2 (hàng "per-backbone rows quoted in the abstract and contributions") nói tóm tắt trích hàng COCO theo mô hình nền của InternVL3. Tóm tắt hiện tại (`00_abstract.md`) chỉ nêu số gộp COCO +3.08 [2.08, 4.03] kèm "PASS" và không có hàng InternVL3 trên COCO (−1.64 [−2.79, −0.49]); hàng này chỉ còn ở đóng góp 2 của Mục 1 và ở kết luận. Theo chính lập luận của Mục 7, số gộp đứng một mình "would overstate the effect". Cần hoặc đưa lại hàng ấy vào tóm tắt (trong giới hạn 150–200 từ), hoặc sửa Mục 7 và Hộp 2 cho khớp.
2. **Công bố về vận hành lấn át công bố về khoa học.** Phần lớn Mục 7.5 là chi tiết hạ tầng (cô lập mạng của bộ chạy đột biến, thứ tự ghi mã kiểm, bản nháp mã chấm). Với phản biện tạp chí, các mục có hệ quả khoa học (thứ tự đăng ký so với kết quả, tập dùng lại, tiếp xúc trước với tham chiếu, việc đã biết trước hiện tượng lô) nên ở thân bài; phần còn lại nên vào phụ lục.
3. **Việc đã thấy trước hiện tượng không bất biến theo lô.** Mục 7.5 thừa nhận các số đếm chú thích không giống hệt đã được thấy ở nghiên cứu khác trước khi đăng ký giả định A1. Phản biện có thể hỏi vì sao các phép kiểm tra chính vẫn giải mã theo lô; câu trả lời của bài (cùng chính sách lô cho hai nhánh, kết quả là của hệ thống như đã chạy) nên được đặt ngay cạnh công bố này.

## C.9 So sánh với tiếng Anh (Mục 8 của bài báo)

**Nội dung.** Mục 8.1–8.5 báo cáo nhánh tiếng Anh, một đăng ký riêng mang thiết kế tiếng Việt sang tiếng Anh không tinh chỉnh; Mục 8.6 báo cáo một đăng ký nữa trên Flickr30K. Kết quả tiếng Anh chỉ được báo cáo trong phạm vi tiếng Anh; không hiệu số xuyên ngôn ngữ nào được tính và không khẳng định tiếng Việt nào thay đổi.

**Đăng ký (8.1).** Bản đăng ký tiếng Anh cố định mọi lựa chọn thiết kế từ bản tiếng Việt: cấu hình Bảng 2, giải mã tham lam 60 token mới, ngưỡng cắt cận, quy tắc lọc và gom cụm, phép rút `rand` có hạt giống, bước xoá với việc lùi về không ví dụ. Tiêu đề lời nhắc, dòng ví dụ và đuôi là bản dịch trực tiếp sang tiếng Anh, ghim bằng mã băm. Chỉ `ret`, `rand` và `zs` được giải mã; không có nhánh `fix`, không có tập phát triển tiếng Anh và không có tinh chỉnh nào cho tiếng Anh. Cột quyết định là CIDEr-D tách token kiểu PTB (×100) từ pycocoevalcap 1.2 [@Chen2015COCOCaptions]; hai cột quyết định của hai ngôn ngữ không cùng thang, và đó là một lý do không tính hiệu số xuyên ngôn ngữ. Cả hai tập dùng quy tắc P1 tiếng Việt. Việc áp cùng quy tắc này cho NoCaps được cố định sau khi biết kết quả XM-a; nó chặt hơn quy tắc XM-a (chỉ đòi cận dưới trên 0), nên hai kết quả ngoài nguồn trả lời hai quy tắc khác nhau. SESOI +2.0 được mang sang nguyên giá trị.

**Bảng C.21.** Dự đoán tiếng Anh đã đăng ký (Bảng 10, Mục 8.1).

| Tên | Tập | Đại lượng | Quy tắc |
|---|---|---|---|
| **P1-EN** (chính) | COCO Karpathy test, đủ 5,000 ảnh | trung bình $\Delta_i$ gộp (PTB CIDEr-D) | điểm > +2.0 và cận dưới khoảng tin cậy > 0; quy tắc L như Bảng C.7 |
| **S-NC** (thứ cấp, thứ tự cố định) | NoCaps val, đủ 4,500 ảnh | trung bình $\Delta_i$ gộp | cùng quy tắc |
| độ nhạy | NoCaps val bỏ 1,000 ảnh đã được giải mã trước đó (3,500) | như trên | báo cáo cạnh S-NC, không thay thế nó |

Khẳng định "mức tăng chuyển sang NoCaps val" cần cả P1-EN và S-NC cùng qua. COCO dùng 5 tham chiếu đầu của mỗi ảnh; NoCaps dùng mọi tham chiếu đã phát hành. Bộ nhớ là COCO Karpathy train và restval sau bộ lọc định trước: 112,255 ảnh trong 111,927 cụm, nên theo cấu trúc bộ nhớ thuộc miền COCO. Ảnh NoCaps val đến từ Open Images và nhãn của chính bộ dữ liệu chia chúng thành trong miền (417 ảnh, chỉ lớp COCO), gần miền (2,670) và ngoài miền (1,413, không có lớp COCO) [@Agrawal2019NoCaps].

**Bảng C.22.** Kết quả tiếng Anh đã đăng ký và được báo cáo (PTB CIDEr-D, khoảng tin cậy bootstrap ghép cặp 95%, B = 2,000; Bảng 11, Mục 8.2).

| Hàng | COCO Karpathy test (5,000) | NoCaps val (4,500) | NoCaps val bỏ 1,000 ảnh trước đó (3,500) |
|---|---|---|---|
| **`ret` − `rand` gộp** | **+3.08 [2.08, 4.03]** | **+1.73 [0.94, 2.50]** | +1.62 [0.66, 2.52] |
| phán quyết | **P1-EN "PASS"** | **S-NC "FAIL"** (điểm dưới +2.0) | "FAIL" |
| Qwen2.5-VL `ret` − `rand` (báo cáo) | +7.80 [6.40, 9.17] | +2.83 [1.69, 3.98] | +2.35 [0.96, 3.73] |
| InternVL3 `ret` − `rand`, τ = 0.10 (báo cáo) | −1.64 [−2.79, −0.49] | +0.62 [−0.37, 1.62] | +0.89 [−0.34, 2.00] |
| InternVL3 `ret` − `rand`, τ = −∞ (thứ cấp đã đăng ký) | −1.05 [−2.22, 0.08], "not detected" | +1.00 [−0.01, 2.01], "not detected" | +1.09 [−0.12, 2.21], "not detected" |
| `ret` − `zs` gộp (mô tả) | +21.89 [20.90, 22.88] | +19.05 [18.18, 19.95] | +19.04 [18.00, 20.05] |
| chênh độ dài, Qwen2.5-VL / InternVL3 | 0.019 / 0.019 (L không kích hoạt) | 0.008 / 0.018 (báo cáo) | 0.007 / 0.018 |

**COCO: P1-EN "PASS" (8.2).** Trên toàn bộ COCO Karpathy test, ví dụ truy hồi hơn ví dụ ngẫu nhiên cùng bộ nhớ +3.08 [2.08, 4.03] điểm PTB CIDEr-D, gộp hai mô hình nền. Quy tắc L không kích hoạt (độ dài trung bình theo token PTB: 11.37 so với 11.16 ở Qwen2.5-VL và 12.47 so với 12.72 ở InternVL3). Hàng POST HOC, không phán quyết: theo quy tắc tương tự rộng hơn của Mục 6.2, 1 trong 5,000 truy vấn có bản gần sao của ảnh truy vấn trong ví dụ `ret`; bỏ nó, hiệu gộp là +3.07 [2.08, 4.06] trên 4,999 truy vấn; cùng quy tắc ấy không gắn cờ truy vấn nào trong 2,500 truy vấn XM-test2500 và 4,500 truy vấn NoCaps val. Theo mô hình nền (hàng báo cáo, khoảng không hiệu chỉnh, không quy tắc đăng ký), mức tăng gộp do Qwen2.5-VL mang: +7.80 [6.40, 9.17]. Với InternVL3 ở τ = 0.10, hàng là −1.64 [−2.79, −0.49], khoảng tin cậy nằm hẳn dưới 0: trên COCO, chú thích của InternVL3 với ví dụ truy hồi đạt điểm thấp hơn với ví dụ ngẫu nhiên. Không có bước xoá, hàng là −1.05 [−2.22, 0.08], "not detected", nên trên COCO bước xoá không giải thích được việc InternVL3 thiếu mức tăng. Không câu phạm vi tiếng Anh nào được đăng ký, nên "carried by Qwen2.5-VL" là cách đọc mô tả. So với không ví dụ (hàng mô tả), ở Qwen2.5-VL `rand` − `zs` là +29.50 [28.27, 30.79] và `ret` − `zs` là +37.30 [35.80, 38.75]; ở InternVL3 là +8.13 [7.03, 9.21] và +6.49 [5.27, 7.70].

**NoCaps: S-NC "FAIL" (8.3).** `ret` − `rand` gộp là +1.73 [0.94, 2.50]: khoảng tin cậy nằm trên 0 nhưng điểm dưới SESOI +2.0, nên quy tắc đăng ký thất bại và bài viết: "The claim that the gain transfers to NoCaps val is not made." Bài nói thẳng rằng theo quy tắc XM-a thì kết quả này sẽ qua, nhưng quy tắc đăng ký cho NoCaps là quy tắc P1, chọn sau khi biết XM-a. Độ nhạy bỏ 1,000 ảnh là +1.62 [0.66, 2.52] và cũng thất bại.

**Bảng C.23.** NoCaps val theo nhãn miền của bộ dữ liệu (`ret` − `rand` gộp; hàng báo cáo, không gác cổng; Bảng 12, Mục 8.3).

| Miền | Số ảnh | `ret` − `rand` gộp |
|---|---|---|
| trong miền (chỉ lớp COCO) | 417 | +4.64 [1.85, 7.36] |
| gần miền | 2,670 | +1.96 [0.85, 2.99] |
| ngoài miền (không có lớp COCO) | 1,413 | +0.43 [−0.85, 1.73] |

Điểm ước lượng giảm từ trong miền ra ngoài miền; các khoảng chồng lấn và không phép kiểm xu hướng nào được đăng ký.

**Đọc kết quả tiếng Anh cạnh tiếng Việt (8.4).** Tiểu mục này mô tả và hậu nghiệm.

![Hình C.1. Hiệu `ret` − `rand` trên bốn tập được chấm, theo từng mô hình nền và gộp, với khoảng tin cậy bootstrap ghép cặp 95% (giá trị từ Bảng 7, 8 và 11 của bài; InternVL3 ở τ đóng băng 0.10). Hàng gộp là các đại lượng đã đăng ký (P1, XM-a, P1-EN, S-NC); hàng theo mô hình nền là hàng báo cáo. Tập tiếng Việt dùng stripped CIDEr-D và tập tiếng Anh dùng PTB CIDEr-D, ở hai ô riêng; không tính hiệu số xuyên ngôn ngữ. Đường liền: số 0; đường đứt: mức +2.0 đã đăng ký, là đại lượng khác nhau trên mỗi thang.](figs/C_fig1_ret_minus_rand.svg)

Ở mỗi ngôn ngữ, dự đoán trong miền đã đăng ký qua (P1 và P1-EN) và dự đoán trên tập ngoài nguồn của bộ nhớ không qua, nhưng hai thất bại khác nhau: trên XM3600 tiếng Việt mức tăng không được phát hiện; trên NoCaps val khoảng tin cậy nằm trên 0 và điểm dưới SESOI, theo một quy tắc chặt hơn. Bài đặt một câu hỏi hậu nghiệm, liệu truy hồi có giúp chủ yếu khi bộ nhớ phủ miền đích hay không, và tự giới hạn bằng năm quan sát: các miền NoCaps có khoảng tin cậy chồng lấn; độ tương tự cấp ảnh không sắp thứ tự được mức tăng; với Qwen2.5-VL mức tăng co lại chứ không biến mất (+3.15 [1.50, 4.93] trên XM-test2500 và +2.83 [1.69, 3.98] trên NoCaps val, hàng báo cáo); trên Flickr30K val, ngoài nguồn của bộ nhớ COCO, `ret` − `rand` vẫn dương (+5.15 [2.34, 8.03] ở Aya-Vision và +3.12 [0.57, 5.72] ở Qwen2.5-VL, hàng phát triển); và phép hoán đổi bộ nhớ trên phần tách Flickr30K là hàng mô tả bị nhiễu bởi văn phong và cỡ, không cho thấy bộ nhớ trong miền gây hại. Giả thuyết ấy không được đăng ký và không được kiểm ở đây.

**Công bố cho nhánh tiếng Anh (8.5).** Bản đăng ký được soạn sau khi ba tệp quyết định tiếng Việt đã được đọc, nhưng tập, SESOI, nhánh và cấu hình đã được cố định từ trước mọi phán quyết tiếng Việt; chỉ quy tắc NoCaps đi sau XM-a. Bước xoá tiếng Anh là một bản chuyển: τ = 0.10 của InternVL3 được chọn trên dữ liệu phát triển tiếng Việt; phía tiếng Anh dùng bộ so khớp COCO-80, chung 24 trong 80 lớp với bản đồ kiểm chứng 112 lớp tiếng Việt, và độ hiệu chuẩn của nó chưa được kiểm trong tiếng Anh, nên hàng τ = −∞ được in cạnh mọi hàng τ = 0.10. Ảnh NoCaps được tải theo mã Open Images chính thức vì máy chủ trung gian của NoCaps không còn phục vụ; byte hoặc độ phân giải có thể khác. Tiếp xúc trước với các tập tiếng Anh (việc chấm của một nghiên cứu đồng hành trên Karpathy test, một lượt giải mã không ví dụ 295 ảnh Karpathy test, và 1,000 ảnh NoCaps của một nghiên cứu khác) được liệt kê trong phụ lục. Hai khối kiểm tra dùng 6.33 (COCO) và 6.88 (NoCaps) giờ GPU, tổng 13.22 trong trần 25 giờ.

**Flickr30K: so sánh trên cùng dữ liệu với một đường cơ sở không huấn luyện (8.6).** Đăng ký này được viết sau khi bốn tập kiểm tra đã có quyết định, nên thiết kế có thể đã tính đến các kết quả ấy; khẳng định, quy tắc và tập kiểm tra được cố định trước khi giải mã ảnh Flickr30K nào. Nó thêm LMCap chạy trên cùng bộ nhớ và cùng ảnh, mô hình nền thứ ba Aya-Vision-8B (không có bước xoá), và tập kiểm tra một lần nhìn thứ năm (Flickr30K Karpathy test, 1,000 ảnh). Bộ nhớ là bộ nhớ COCO tiếng Anh, nên Flickr30K nằm ngoài nguồn của bộ nhớ. InternVL3-8B ở đây dùng k = 4, ví dụ đặt cuối, đuôi T2 ở τ = −∞, khác Bảng 2. `rand` được giải mã trên phần tách và, với Aya-Vision và Qwen2.5-VL, trên val, không bao giờ trên test. Ba tầng: (1) thăm dò trên phần tách 1,000 ảnh Flickr30K train, một khẳng định được đề cử nếu cận dưới khoảng tin cậy trên phần tách ít nhất +2.0; năm khẳng định được đề cử (E1, E2 cho `ret` − `rand`; E3a–c cho `ret` − LMCap), còn hàng `ret` − `rand` của InternVL3 trên phần tách, −1.00 [−3.03, 1.15], chỉ mô tả; (2) diễn tập trên đủ 1,014 ảnh val, dùng một lần, qua nếu điểm ít nhất +2.0 và cận dưới 95% trên 0, và chỉ lên kiểm tra nếu qua có biên, tức xác suất qua dự phóng trên test ít nhất 0.98, một giá trị hoạch định bị chệch lên vì gồm cả dữ liệu phần tách đã đề cử khẳng định; (3) một lần nhìn Flickr30K test, qua nếu điểm ít nhất +2.0 và thống kê một phía hiệu chỉnh Holm dưới 0.05.

**Bảng C.24.** Diễn tập Flickr30K (val, 1,014 ảnh; dữ liệu phát triển; PTB CIDEr-D; Bảng 13, Mục 8.6).

| Khẳng định | Hiệu trên val [khoảng tin cậy 95%] | Xác suất qua dự phóng trên test | Kết cục |
|---|---|---|---|
| E1, Aya-Vision-8B `ret` − `rand` | +5.15 [2.34, 8.03] | 0.953 | qua diễn tập, không có biên; không lên kiểm tra |
| E2, Qwen2.5-VL-7B `ret` − `rand` | +3.12 [0.57, 5.72] | 0.700 | qua diễn tập, không có biên; không lên kiểm tra |
| E3a, Aya-Vision-8B `ret` − LMCap | +24.63 [21.32, 28.05] | 1.000 | lên kiểm tra |
| E3b, InternVL3-8B `ret` − LMCap | +34.81 [30.90, 38.83] | 1.000 | lên kiểm tra |
| E3c, Qwen2.5-VL-7B `ret` − LMCap | +32.01 [28.42, 35.69] | 1.000 | lên kiểm tra |

E1 và E2 là hàng phát triển; không nhánh `rand` nào được giải mã trên Flickr30K test, và bài viết: "The study therefore makes no claim that retrieved examples beat random ones on Flickr30K."

**Bảng C.25.** Flickr30K Karpathy test (1,000 ảnh, một lần nhìn); khẳng định đã đăng ký, cột quyết định trên mọi ảnh; Holm trên ba khẳng định (Bảng 14, Mục 8.6).

| Mô hình nền | `ret` − LMCap, đủ 1,000 ảnh | Thống kê hiệu chỉnh Holm | Phán quyết | Sau bộ lọc định trước (997) | `zs` − LMCap (mô tả) | `ret` − `zs` (mô tả) |
|---|---|---|---|---|---|---|
| Aya-Vision-8B (E3a) | **+28.77 [25.19, 32.18]** | 0.0015 | **"PASS"** | +28.80 [25.21, 32.29], "PASS" | −14.50 [−17.35, −11.63] | +43.27 [40.11, 46.37] |
| InternVL3-8B, τ = −∞ (E3b) | **+37.87 [34.26, 41.39]** | 0.0015 | **"PASS"** | +37.93 [34.34, 41.45], "PASS" | +30.77 [27.34, 34.26] | +7.10 [4.68, 9.67] |
| Qwen2.5-VL-7B (E3c) | **+34.36 [30.69, 38.01]** | 0.0015 | **"PASS"** | +34.41 [30.96, 37.96], "PASS" | +12.47 [9.37, 15.55] | +21.90 [19.20, 24.68] |

Cả ba khẳng định đăng ký đều qua. Bài nói rõ điều so sánh cho thấy và không cho thấy: E3 là so sánh trên cùng dữ liệu với một đường cơ sở đã công bố, "It is not evidence that the retrieval prompt causes the margin." Cột `zs` − LMCap tách mỗi khoảng cách: với InternVL3, phần lớn đã có ở không ví dụ (+30.77 trong +37.87); với Aya-Vision, toàn bộ đến từ lời nhắc có ví dụ vì Aya-Vision không ví dụ thấp hơn LMCap (−14.50), và việc hiệu ứng ấy đến từ truy hồi hay từ việc thấy chú thích kiểu COCO bất kỳ không được kiểm vì E1 không lên kiểm tra; với Qwen2.5-VL, khoảng một phần ba đã có ở không ví dụ (+12.47 trong +34.36). Bộ sinh của LMCap là mô hình ngôn ngữ chỉ văn bản 2.9B không thấy ảnh truy vấn, còn mỗi mô hình nền là mô hình 7–8B có thấy ảnh; một phần của mọi khoảng cách là khác biệt ấy. Một cận vững thô được đăng ký trên phần tách: nếu LMCap đạt mức XM3600 tiếng Anh đã công bố 45.2 [@Ramos2023LMCap] thì khoảng cách trên phần tách vẫn vào khoảng +17.6, +30.5 và +30.2; cận này trừ một điểm số từ bộ dữ liệu và bộ chấm khác nên chỉ nói về độ lớn. Đại lượng quyết định là thống kê đuôi bootstrap phân vị không định tâm với hiệu chỉnh +1, dạng (C.10); không lần lấy mẫu lại nào rơi ở hoặc dưới 0 với bất kỳ khẳng định nào, nên mỗi giá trị chưa hiệu chỉnh nằm ở sàn 1/2,001 và giá trị hiệu chỉnh Holm 0.0015 bằng ba lần sàn đó; nó giới hạn bằng chứng theo ngân sách lấy mẫu lại chứ không đo một xác suất đuôi. Các công bố của đăng ký này: chỉ ba hàng kiểm tra của Bảng 14 là xác nhận; các mô hình nền, XGLM và bộ mã hoá truy hồi có thể đã thấy Flickr30K hoặc COCO khi tiền huấn luyện, và với E3 mức tiếp xúc có thể khác nhau giữa hai phía; tham chiếu Flickr30K test đã được một nghiên cứu đồng hành đọc trước đăng ký; lượt kiểm tra dừng một lần ở bước kiểm tiền khởi chạy, trước khi giải mã ảnh nào, và được khởi chạy lại không đổi; giải mã kiểm tra dùng 1.86 giờ GPU của trần 2.5 giờ.

**Ngữ cảnh từ các hệ đã công bố (8.7).** Bảng S15 in điểm CIDEr mà các bài khác báo cáo cạnh các lượt chạy của nghiên cứu, không phải bảng xếp hạng. Cách đọc duy nhất mà nó ủng hộ là lời nhắc không huấn luyện vẫn thấp xa hệ tinh chỉnh trên OpenViIC test (đường cơ sở công bố tốt nhất 75.58 CIDEr [@Bui2023OpenViIC]).

**Nhận xét rà soát.** Nhánh tiếng Anh làm đúng điều nó hứa: lặp lại nguyên thiết kế, không tinh chỉnh, và báo cáo cả hàng bất lợi. Các điểm cần lưu ý:

1. **P1-EN "PASS" là trung bình của một hàng dương lớn và một hàng âm.** Qwen2.5-VL +7.80 [6.40, 9.17] và InternVL3 −1.64 [−2.79, −0.49], với khoảng tin cậy của InternVL3 nằm hẳn dưới 0. Số gộp +3.08 vì thế không mô tả mô hình nào trong hai mô hình. Đây chính là lý do tóm tắt cần hàng InternVL3 (xem nhận xét 1 ở C.8).
2. **Quy tắc NoCaps được chọn sau khi biết XM-a.** Bài công bố điều này ở ba nơi (Mục 8.1, 8.3, 9.2) và nói rõ theo quy tắc XM-a thì S-NC sẽ qua. Người viết lại phải giữ cả hai nửa: phán quyết "FAIL" theo quy tắc đã đăng ký, và việc hai thất bại ngoài nguồn không phải một thất bại song song.
3. **Bước xoá tiếng Anh chưa được hiệu chuẩn.** Chỉ 24 trong 80 lớp trùng với bản đồ tiếng Việt; hàng InternVL3 ở τ = 0.10 trên COCO và NoCaps vì vậy đo một bước chuyển chưa kiểm. Hàng τ = −∞ in cạnh là biện pháp đúng; nên nhắc điều này ngay trong chú thích Bảng 11.
4. **E3 dễ bị đọc thành khẳng định về phương pháp.** Khoảng cách +28.77 đến +37.87 là con số lớn nhất trong tóm tắt, nhưng nó so mô hình 7–8B có thấy ảnh với một mô hình ngôn ngữ 2.9B không thấy ảnh, trên một bản cài đặt lại có bốn sai khác (một chú thích mỗi cụm, ngưỡng cắt cận loại láng giềng gần nhất của LMCap). Bài đã rào đón đủ; khi rút gọn, không được bỏ cụm "a re-implemented training-free baseline" và phần phân rã theo `zs`.
5. **Sổ điểm của Flickr30K test đã mất.** Mục 9.3 cho biết tệp điểm theo lượt chạy của Flickr30K test bị mất sau bước quyết định và tệp quyết định đã đăng ký là bản ghi duy nhất còn lại. Công bố này không có trong danh sách công bố của Mục 8.6 và không có trong Hộp 2; nó phải được nêu ngay tại Mục 8.6, vì nó quyết định việc Bảng 14 có thể được kiểm lại hay không.
6. **Hai dạng làm tròn của cùng một số.** Mục 8.6 viết xác suất dự phóng "(0.95 and 0.70)" trong lời nhưng Bảng 13 in 0.953 và 0.700; nên dùng một dạng.
7. **Hình 1 không có Flickr30K.** Hình chỉ gồm bốn tập có tương phản `ret` − `rand`; đây là lựa chọn đúng vì E3 là đại lượng khác, nhưng chú thích hình nên nói rõ tập thứ năm không xuất hiện vì lý do đó.

## C.10 Hạn chế và các mối đe doạ tính giá trị (Mục 9 của bài báo)

**Nội dung.** Mục 9.1 liệt kê các hạn chế sau, tất cả đều phải được giữ khi viết lại.

1. **Hai mô hình nền, và hiệu ứng do một mô hình mang.** Ở cả hai ngôn ngữ mức tăng trong miền do Qwen2.5-VL mang là chính; với InternVL3 mức tăng không được phát hiện trên OpenViIC test và hàng COCO nằm dưới 0 (−1.64 [−2.79, −0.49]). Với hai mô hình nền, nghiên cứu không thể nói thuộc tính nào của mô hình dự báo mức tăng; đại lượng gộp không phải hiệu ứng cho một MLLM điển hình.
2. **Ngoài nguồn của bộ nhớ, các dự đoán đăng ký không qua.** Không bộ nhớ nào chứa chú thích của tập đích; nguồn bộ nhớ và tập kiểm tra thay đổi cùng nhau và không phép kiểm nào đổi bộ nhớ trên ảnh kiểm tra cố định, nên sự khớp nguồn bị trộn lẫn với tập kiểm tra. Cách đọc "phủ miền" của Mục 8.4 là hậu nghiệm và chưa được kiểm.
3. **Độ đo dựa trên tham chiếu.** CIDEr-D thưởng cho việc khớp câu chữ của tham chiếu; một phần mức tăng `ret` − `rand` có thể là câu chữ gần hơn chứ không phải nội dung tốt hơn. Nghiên cứu không có đánh giá của người; theo thiết kế nó chỉ dùng dữ liệu và nhãn sẵn có.
4. **Độ đo đối tượng phụ thuộc bộ so khớp và nhãn vàng.** Trên OpenViIC, một đối tượng đúng mà không tham chiếu nào nêu bị tính là lỗi; trên XM3600 nhãn đã xác minh chỉ phủ các lớp được ánh xạ; nhánh tiếng Anh không đăng ký dự đoán nào về độ chính xác đối tượng.
5. **Một lần nhìn, một máy, một lần chạy, một lần rút ngẫu nhiên.** Khoảng tin cậy không gồm biến thiên do rút ví dụ ngẫu nhiên khác hay biến thiên giữa các lần chạy; các phép kiểm tương đương giải mã (52/52) chỉ cho thấy tương đương giữa các lần chạy, không phải độc lập với thành phần lô.
6. **Nghiên cứu phân bổ chỉ trên tập phát triển dùng lại.** Dù kết cục của lần nhìn là gì, đó là kết quả phát triển cho các mô hình nền và cấu hình của lần nhìn ấy; khẳng định đăng ký chỉ liên quan Qwen2.5-VL-7B và InternVL3-8B, hai mô hình chung dòng mô hình ngôn ngữ Qwen2.5. Cận sao chép dựa trên giả định A_cp và đặt cận cho tương phản theo lô đã lưu. Đối chứng dương không cho thấy độ nhạy quanh +2.0, không có đối chứng âm và không xác nhận lại các hàng của ba mô hình nền.
7. **Thành phần lô làm đổi chú thích tham lam.** Kết quả đăng ký của bài là kết quả của hệ thống như đã chạy; không số nào đổi, nhưng hiệu theo ảnh giữa hai nhánh giải mã theo lô có thể chứa số hạng bạn cùng lô, và bootstrap theo ảnh không mô hình hoá sự ràng buộc trong một lát lô.
8. **Dữ liệu huấn luyện của mô hình nền không được công bố đầy đủ.** Báo cáo Qwen2.5-VL [@Bai2025Qwen25VL] mô tả dữ liệu theo loại; báo cáo InternVL3 [@Zhu2025InternVL3] dựa trên kho của InternVL2.5, vốn liệt kê chú thích COCO, Open Images và TextCaps [@Chen2024InternVL25]. Đối chứng `rand` cùng k khử phần nhiễm chung của `ret` và `rand`, nhưng không khử phần nhiễm tương tác với truy hồi. "Training-free" nghĩa là không huấn luyện cho tác vụ trong nghiên cứu này; đây là kiểm tra trên giấy các báo cáo công khai, không phải kiểm toán.
9. **So sánh Flickr30K là so sánh đường cơ sở, không phải kiểm định truy hồi.** Hai khẳng định `ret` − `rand` (E1, E2) không được kiểm tra, nên truy hồi so với ngẫu nhiên trên Flickr30K chỉ dựa vào hàng phát triển; ba khẳng định E3 so mỗi mô hình nền với bộ sinh chỉ văn bản 2.9B của một bản cài đặt lại có bốn sai khác; thống kê quyết định nằm ở sàn với mọi khẳng định; SESOI +2.0 không được hiệu chỉnh lại cho PTB CIDEr-D.
10. **Không tuyên bố ưu tiên.** "This paper's contribution is the controlled, preregistered comparison, not the method."

Mục 9.2 xét bốn loại giá trị. Về giá trị nội tại, ba nhánh có ví dụ dùng chung khuôn, k và bộ giải mã; quy tắc L không kích hoạt trên OpenViIC test (0.074, 0.039) hay COCO (0.019, 0.019); mối đe doạ còn lại là bước xoá của InternVL3 xử lý chú thích `ret` và `rand` khác nhau. Về giá trị cấu trúc, trên các hàng phát triển Flickr30K, `ret` − `rand` chuyển âm với mọi mô hình nền sau khi che các 3-gram từ chung với ví dụ, nên mức tăng CIDEr đi qua câu chữ mượn giống tham chiếu; việc che thiên lệch bất lợi cho `ret`, nên các hàng này không cho thấy mức tăng là giả; nghiên cứu "claims nothing beyond lexical or style transfer from CIDEr gains". Về giá trị ngoại tại, kết quả áp dụng trong miền, trên hai bộ đánh giá ở hai ngôn ngữ, với hai MLLM mở 7–8B; nó không áp dụng ngoài nguồn của bộ nhớ và chưa được kiểm với họ hay cỡ mô hình khác, giải mã lấy mẫu hay lời nhắc có ảnh ví dụ. Về giá trị kết luận thống kê, mọi quyết định dùng quy tắc đăng ký; ba lựa chọn được đưa ra khi đã biết kết quả trước và được công bố: đăng ký tiếng Anh đi sau phán quyết tiếng Việt, quy tắc NoCaps chặt hơn đi sau XM-a, và hai trong sáu điểm τ của ablation đã biết.

Mục 9.3 về tái lập: mọi ảnh chụp mô hình, môi trường, khuôn lời nhắc, danh sách và tệp mã được ghim bằng sha256. Một sổ điểm không được giữ lại: tệp điểm theo lượt chạy của Flickr30K test bị mất sau bước quyết định; sha256 của nó được ghi trong tệp quyết định đã đăng ký, là bản ghi duy nhất còn lại về điểm của phép kiểm tra ấy. Điểm số, mã ảnh và mã băm sẽ được công bố; chú thích, tệp ví dụ, véc-tơ nhúng và sổ điểm theo ảnh thì không. Một bên thứ ba có thể chạy lại nghiên cứu trên một GPU 24 GB (9.59 giờ GPU cho kiểm tra tiếng Việt, 13.22 cho tiếng Anh và 1.86 cho Flickr30K); một lần chạy lại chính xác cần cùng lát lô ngoài cùng ảnh chụp mô hình và phần mềm.

**Nhận xét rà soát.** Mục 9 thẳng thắn và gần đủ. Năm bổ sung nên cân nhắc. (i) Câu ở Mục 9.2 rằng kết quả "untested for … prompts with example images" không khớp với chính bài: Bảng 18 báo cáo $\tau_{\text{sel}}$ của định dạng ảnh–chú thích trên tập phát triển (+6.36 [4.30, 8.46], "DETECTED" trên OV-dev-B) và Bảng S19 có hàng ví dụ xen kẽ; nên viết "chưa được kiểm trên tập kiểm tra nào". (ii) Hạn chế về việc cấu hình được chọn theo điểm `ret` (xem C.4) và về bốn cặp ảnh trùng trong OV-test (xem C.5) chưa có trong Mục 9. (iii) Việc chỉ có một bộ `fix` cho mỗi tập, với nhãn "conditional on the realised fixed set", chỉ nằm ở Mục 6.10.5 và chú thích bảng; nên có một dòng ở Mục 9.1. (iv) Việc không công bố sổ điểm theo ảnh khiến bên thứ ba không thể tính lại khoảng tin cậy nếu không chạy lại toàn bộ; `V2_PROGRESS_C.md` đã ghi đây là quyết định còn mở (xuất sổ điểm không kèm chú thích, hoặc giữ kín). Phản biện của một tạp chí coi trọng tái lập gần như chắc chắn hỏi điều này. (v) Hạn chế 8 dựa trên việc đọc báo cáo công khai của mô hình; cần đối chiếu lại với bản mới nhất của các báo cáo ấy trước khi nộp.

## C.11 Kết luận (Mục 10 của bài báo)

**Nội dung.** Kết luận nhắc lại câu hỏi và thiết kế, rồi tổng kết theo bốn khối. Trong miền, ở cả hai ngôn ngữ: P1 "PASS" trên OpenViIC test (+4.49 [3.52, 5.57]) và P1-EN "PASS" trên COCO Karpathy test (+3.08 [2.08, 4.03]); mức tăng do Qwen2.5-VL mang là chính, hàng InternVL3 không được phát hiện trên OpenViIC test và, như một hàng báo cáo, nằm dưới 0 trên COCO; trên OpenViIC test không mô hình nào mất độ chính xác đối tượng so khớp số lượng so với chú thích không ví dụ của chính nó, và bài nhắc đây là so toàn bộ lời nhắc ngữ cảnh với không ví dụ, không phải so truy hồi với ngẫu nhiên. Ngoài nguồn của bộ nhớ: trên XM3600 tiếng Việt mức tăng không được phát hiện (+0.70 [−0.45, 1.97]) và dự đoán XM3600 đã đăng ký "not confirmed"; trên NoCaps val mức tăng gộp +1.73 [0.94, 2.50] có khoảng tin cậy trên 0 nhưng điểm dưới SESOI theo quy tắc tiếng Anh chặt hơn (S-NC "FAIL"), nên khẳng định chuyển giao không được đưa ra. Về đối chứng: hàng S-zf đặt `ret` − `zs` ở +14.30 [13.38, 15.24], so với `ret` − `rand` của P1 là +4.49 [3.52, 5.57]; về mô tả, ví dụ ngẫu nhiên trong miền đã cao hơn hẳn không ví dụ. Về đường cơ sở trên cùng dữ liệu: trên Flickr30K Karpathy test, lời nhắc có truy hồi cao hơn bản cài đặt lại LMCap từ +28.77 đến +37.87 điểm với ba mô hình nền (ba khẳng định kiểm tra đăng ký, đều "PASS"); phần lớn khoảng cách của InternVL3 không cần ví dụ (+30.77 trong +37.87), khoảng một phần ba với Qwen2.5-VL (+12.47 trong +34.36) và không phần nào với Aya-Vision; bài viết: "This is a baseline comparison, not evidence for retrieval".

Bài rút ra ba điều một người làm thực hành cần trước khi quy mức tăng so với không ví dụ cho truy hồi: một đối chứng ví dụ ngẫu nhiên cùng k rút từ cùng bộ nhớ; kết quả cho từng mô hình nền chứ không chỉ số gộp; và xét xem chú thích của bộ nhớ có đến từ nguồn của tập đích không. Điều thứ ba được rào kỹ: các dự đoán truy hồi–ngẫu nhiên đã đăng ký chỉ qua ở đó, nhưng nguồn bộ nhớ và tập kiểm tra thay đổi cùng nhau và các hàng ngoài nguồn của Qwen2.5-VL vẫn trên 0, "so this is an observation and not a tested cause". Một bước xoá sau giải mã cần sự cẩn trọng tương tự: trên tập phát triển nó gỡ khỏi chú thích có ví dụ truy hồi nhiều hơn khỏi chú thích có ví dụ ngẫu nhiên. Về dữ liệu và mã, khi công bố bài sẽ phát hành các bản đăng ký kèm danh sách đã ghim, mã kiểm tra và tệp quyết định, điểm số, mã ảnh và mã băm sha256 (với Flickr30K test chỉ có tệp quyết định đã đăng ký); không chú thích của bộ dữ liệu nào, không chú thích của mô hình nào và không sổ điểm theo ảnh nào được phát hành. Bài ghi rằng một tác giả đã liên hệ các tác giả UIT-OpenViIC và KTVIC và họ đồng ý cho dùng bộ dữ liệu trong nghiên cứu; UIT-ViIC không được dùng làm dữ liệu và bài không tuyên bố có sự cho phép nào từ tác giả của nó. Đường dẫn kho mã và DOI lưu trữ còn để trống, chờ sau phản biện.

**Nhận xét rà soát.** Kết luận khớp với các bảng và giữ đủ rào đón; khác với tóm tắt, nó có hàng COCO của InternVL3. Ba việc còn lại: (i) chỗ trống cho đường dẫn kho mã và DOI phải được điền hoặc thay bằng câu về bản ẩn danh gửi biên tập viên theo đúng yêu cầu của tạp chí; (ii) sự đồng ý của các tác giả bộ dữ liệu được nêu bằng một câu; nên có văn bản xác nhận để nộp kèm nếu tạp chí yêu cầu; (iii) kết luận không nhắc phát hiện về thành phần lô, vốn có giá trị thực hành trực tiếp cho người muốn tái lập; có thể thêm một câu, giữ nhãn rằng đây là phép kiểm trên tập phát triển dựa trên đồng nhất chuỗi.

## C.12 Phụ lục S của bài báo

**Nội dung.** Phụ lục S (tệp `11_supplement_registered_rows.md`) gồm mười hai phần, được điểm qua theo thứ tự.

1. **Hàng đăng ký theo lượt chạy (Bảng S1–S4).** Cho mỗi tập được chấm (1,941, 2,001, 2,500, 2,392), bảng in từng lượt (`ret`, `rand`, `fix`, `zs` của mỗi mô hình nền ở τ đóng băng và ở τ = −∞, cùng ba đường cơ sở sao chép) với ba cột CIDEr-D (stripped, nguyên trạng, PTB), CHAIR_i, số lần nhắc mỗi ảnh và ΔP_cm; phần tiếp theo in tỉ lệ đối tượng chỉ-từ-láng-giềng, số lớp bị bác mỗi ảnh, tỉ lệ bị sửa, tỉ lệ lùi về không ví dụ, tỉ lệ chép 4-gram, tỉ lệ gần nguyên văn và tỉ lệ hit-max. Các số ở Bảng C.10 và Mục 6.6 lấy từ đây.
2. **Đối chứng, văn phong, liều–đáp ứng, đối tượng (Bảng S5–S9).** Bảng S5 cho mọi hàng đối chứng với khoảng tin cậy trên cả bốn tập; Bảng S6 báo cáo văn phong; Bảng S7 liều–đáp ứng; Bảng S8 độ chính xác chỉ-từ-láng-giềng; Bảng S9 AUROC của cơ chế chắn ở giai đoạn B (0.582 và 0.519 trên OV-dev-B, 0.551 và 0.559 trên XM-dev500 cho điểm s), chỉ là chẩn đoán và không khẳng định nào dựa vào nó.
3. **Mọi cấu hình đã thử (Bảng S10–S11).** Mọi lượt giải mã ở giai đoạn A và B, kể cả lượt hỏng.
4. **Hàng không đăng ký cho khẳng định nào (Bảng S12).** Các hàng InternVL3 ở τ khác và AUROC của mô hình kiểm chứng (0.560 cho `ret` trên tập chính).
5. **Nhánh tiếng Anh (Bảng S13).** Mọi hàng đăng ký và báo cáo, kèm số đếm của bước xoá: trên COCO, chú thích `ret` của InternVL3 có 524 mục đối tượng chỉ-từ-láng-giềng, mô hình kiểm chứng bác 302, 110 chú thích bị sửa và 182 lùi về không ví dụ; với `rand` là 123, 112, 39 và 73.
6. **Cơ chế trên tập phát triển (Bảng S14).** Mọi hàng của tệp quyết định ablation; kiểm tương đương giải mã trên 52 ảnh OV-dev-B cho 52/52; dùng 3.32 giờ GPU.
7. **Vận hành lượt kiểm tra.** Phép kiểm tương đương giải mã trước kiểm tra tiếng Việt cần ba lần thử (lần đầu dừng trước khi giải mã; lần hai cho 52/52 ở cả hai mô hình nền nhưng hồ sơ không khép được; lần ba là lần chính thức, 52/52 và 52/52), tất cả chỉ dùng dữ liệu phát triển, tổng 0.08 giờ GPU; khối XM3600 chạy từ cây làm việc ghim ở lần cam kết kiểm tra; ba tệp cắt cụt đi đường thử lại; thời điểm quyết định thêm nhánh tiếng Anh (bài ghi rằng hai dấu thời gian liên quan không thể kiểm chứng độc lập); một sửa đổi trước mọi lượt giải mã tiếng Anh và một phép thử khói trên 16 ảnh bộ nhớ.
8. **Định nghĩa công cụ.** Bộ chấm, bộ so khớp đối tượng tiếng Việt (chuẩn hoá vị trí dấu thanh), độ chính xác so khớp số lượng (công thức C.9), bộ so khớp tiếng Anh theo danh sách đồng nghĩa của CHAIR [@Rohrbach2018CHAIR], câu hỏi kiểm chứng và bảng các phiên bản mô hình đã ghim.
9. **Ngữ cảnh từ các hệ đã công bố (Bảng S15).** Khối A chép điểm CIDEr đã công bố; khối B in các lượt của nghiên cứu, với các hàng tiếng Việt mang nhãn "not comparable".
10. **Giai đoạn B và phân rã tương phản của InternVL3 (Bảng S16–S17).** Trên XM-dev500, `ret` − `rand` gộp là +1.46 [−1.07, 4.17]; bước xoá làm giảm điểm `ret` của InternVL3 nhiều hơn điểm `rand` trên cả hai tập phát triển (−5.43 [−6.76, −4.08] so với −2.48 [−3.44, −1.51] trên OV-dev-B).
11. **Chi tiết công bố.** Công suất và độ chính xác (sai số chuẩn khoảng 1.85 mỗi mô hình nền cho cổng giai đoạn B; hiệu gộp quan sát bằng khoảng 13.9% điểm `rand` với P1, 1.3% với XM-a, 3.5% với P1-EN và 2.0% với S-NC; cận trên của XM-a là 1.97); sai số Monte Carlo; chia tập; tiếp xúc trước; tham chiếu và bộ nhớ tiếng Anh (113,287 ứng viên, còn 112,255 ảnh, 111,927 cụm); công bố cho ablation; và phần tìm tài liệu.
12. **Chẩn đoán lọc ví dụ, hàng phát triển Flickr30K và nghiên cứu phân bổ (Bảng S18–S27).** Bảng S18 cho bảng đồng thuận hậu nghiệm (κ = 0.008 [0.005, 0.012] trên 2,748 đơn vị). Bảng S19 cho các hàng phát triển Flickr30K: sau khi che 3-gram từ chung với ví dụ, `ret` − `rand` trên phần tách là −3.58 [−6.39, −0.71], −10.37 [−12.83, −7.89] và −14.33 [−17.12, −11.37] (Aya-Vision-8B, InternVL3-8B, Qwen2.5-VL-7B); ví dụ ảnh–chú thích xen kẽ trừ `ret` văn bản là +8.52 [5.47, 11.35] ở Qwen2.5-VL-7B trên phần tách, trong khi trên tập phát triển B tiếng Việt cùng tương phản là −0.53 [−2.39, 1.32], và bài viết: "The text-only design rests on cost and on that Vietnamese parity, not on accuracy." Bảng S20–S27 in mọi hàng của nghiên cứu phân bổ: số đếm đồng nhất chuỗi, XM-dev500, hàng theo lô, thành phần phương sai, cận sao chép ở mọi n, độ nhạy tần suất tài liệu, hàng đồng hành nguồn bộ nhớ, chẩn đoán danh sách `perm` (tỉ lệ bù nằm trong cổng 0.10 trên mọi tập; cosine trung bình tới truy vấn của các cụm được đưa là 0.787, 0.539 và 0.512 cho `ret`, `perm`, `rand` trên OV-dev-A) và bản ghi giải mã khối 3 (tổng 13,391 giây GPU).

**Nhận xét rà soát.** Phụ lục làm đúng lời hứa in mọi hàng. Các điểm cần sửa: (i) tên "Supplement S. Registered per-run rows" không còn phản ánh nội dung, vì phần lớn phụ lục nay là hàng phát triển, hậu nghiệm và hồ sơ vận hành; nên chia thành các phụ lục có tên riêng theo mức bằng chứng. (ii) Nhiều tiêu đề còn dấu vết biên tập ("moved from Section …"); cần gỡ. (iii) Hàng ví dụ xen kẽ của Qwen2.5-VL-7B trên phần tách Flickr30K (+8.52 [5.47, 11.35]) cho thấy trên dữ liệu phát triển tiếng Anh ấy, ví dụ có ảnh đạt điểm cao hơn ví dụ văn bản; lời biện minh cho thiết kế chỉ-văn-bản ("cost and … Vietnamese parity") hiện chỉ nằm trong phụ lục, trong khi đây là lựa chọn thiết kế trung tâm mà phản biện sẽ hỏi; nên đưa một câu vào Mục 3.3 hoặc Mục 9.2. (iv) Phần "Test-run operations" chứa tên tệp quyết định, tiền tố lần cam kết và dấu thời gian; cần rà lại theo chế độ ẩn danh của tạp chí. (v) Theo `V2_PROGRESS_C.md`, bản dựng phụ lục còn nhiều bảng rộng tràn lề; các Bảng S1–S4, S10–S12 và S24 cần trang ngang hoặc tách bảng.

## C.13 Bảng đối chiếu khẳng định – bằng chứng

Bảng C.26 đối chiếu từng khẳng định của tóm tắt, mở đầu và kết luận với bằng chứng trong bài. Khoá manifest được ghi dưới dạng tên tệp nguồn kèm khoá, như ở cột thứ hai của `number_manifest_C.tsv` (phần đường dẫn thư mục được lược bỏ).

**Bảng C.26.** Khẳng định, trạng thái và bằng chứng (số bảng là số của bài báo).

| Khẳng định (rút gọn) | Trạng thái | Mục | Bảng, hình | Số chính | Khoá manifest |
|---|---|---|---|---|---|
| `ret` hơn `rand` trên OpenViIC test, gộp hai mô hình nền | REGISTERED PASS (P1) | 6.2 | Bảng 7, Hình 1 | +4.49 [3.52, 5.57] | `decide_ov.json::P1.d`; `decide_ov.json::P1.passed` |
| mức tăng do Qwen2.5-VL mang là chính; không được phát hiện ở InternVL3 (câu phạm vi) | REGISTERED (P1b "confirmed"; InternVL3 "reported only") | 6.2 | Bảng 5, Bảng 7 | +8.33 [7.01, 9.76]; +0.66 [−0.68, 1.99] | `decide_ov.json::P1b.qwen25vl_7b.d`; `decide_ov.json::P1b.internvl3_8b.d` |
| không mô hình nào mất độ chính xác đối tượng so khớp số lượng so với `zs` quá sàn trên OpenViIC test | REGISTERED PASS (P2, cả hai) | 6.2 | Bảng 7 | +5.41 [3.88, 7.01]; +1.57 [0.65, 2.51] | `decide_ov.json::P2.qwen25vl_7b.d`; `decide_ov.json::P2.internvl3_8b.d` |
| trên XM3600 tiếng Việt mức tăng không được phát hiện; dự đoán XM "not confirmed" | REGISTERED FAIL (XM-a) | 6.3 | Bảng 8 | +0.70 [−0.45, 1.97] | `decide_xm_m3.json::XM_a.d`; `decide_xmb.json::XM_prediction` |
| COCO Karpathy test lặp lại mẫu hình tiếng Anh đã biết | REGISTERED PASS (P1-EN) | 8.2 | Bảng 11, Hình 1 | +3.08 [2.08, 4.03] | `decide_coco_test.json::P1_EN.d`; `decide_coco_test.json::P1_EN.verdict` |
| hàng COCO của InternVL3 nằm dưới 0 | DESCRIPTIVE (hàng báo cáo) | 8.2 | Bảng 11 | −1.64 [−2.79, −0.49] | `decide_coco_test.json::scored.coco_test_5000.per_model.internvl3_8b.ret_minus_rand.d` |
| trên NoCaps val điểm ước lượng dưới ngưỡng +2.0; không khẳng định chuyển giao | REGISTERED FAIL (S-NC) | 8.3 | Bảng 11 | +1.73 [0.94, 2.50] | `decide_nocaps_val.json::S_NC.d`; `decide_nocaps_val.json::S_NC.verdict` |
| các hàng theo miền của NoCaps giảm từ ảnh chỉ có lớp COCO tới ảnh không có | DESCRIPTIVE | 8.3 | Bảng 12 | +4.64 [1.85, 7.36]; +1.96 [0.85, 2.99]; +0.43 [−0.85, 1.73] | `decide_nocaps_val.json::per_domain.in-domain.d`; `decide_nocaps_val.json::per_domain.near-domain.d`; `decide_nocaps_val.json::per_domain.out-domain.d` |
| trên Flickr30K test, lời nhắc có truy hồi cao hơn LMCap cài đặt lại với ba mô hình nền | REGISTERED PASS (E3a–c) | 8.6 | Bảng 14 | +28.77 [25.19, 32.18]; +37.87 [34.26, 41.39]; +34.36 [30.69, 38.01] | `T3_DECISION.json::full.claims.E3 aya_vision_8b: ret-lmcap_ri.test.d`; `T3_DECISION.json::full.claims.E3 internvl3_8b: ret-lmcap_ri.test.d`; `T3_DECISION.json::full.claims.E3 qwen25vl_7b: ret-lmcap_ri.test.d` |
| phần lớn khoảng cách của InternVL3 đã có ở không ví dụ; khoảng một phần ba với Qwen2.5-VL; không phần nào với Aya-Vision | DESCRIPTIVE | 8.6 | Bảng 14 | +30.77 trong +37.87; +12.47 trong +34.36; −14.50 | `T3_DECISION.json::full.descriptive.internvl3_8b: zs-lmcap_ri.d`; `T3_DECISION.json::full.descriptive.qwen25vl_7b: zs-lmcap_ri.d`; `T3_DECISION.json::full.descriptive.aya_vision_8b: zs-lmcap_ri.d` |
| hai tương phản `ret` − `rand` trên Flickr30K qua diễn tập không có biên, không lên kiểm tra | DEVELOPMENT (không phán quyết) | 8.6 | Bảng 13 | +5.15 [2.34, 8.03] (0.953); +3.12 [0.57, 5.72] (0.700) | `T2_DECISION.json::full.claims.E1 aya_vision_8b: ret-rand.val.d`; `T2_DECISION.json::full.claims.E2 qwen25vl_7b: ret-rand.val.d` |
| `ret` − `zs` trong miền, so với `ret` − `rand` của P1 | REGISTERED, thứ cấp không có nhãn qua (S-zf) | 6.4 | Bảng S5 | +14.30 [13.38, 15.24] | `decide_ov.json::S_zf.pooled_vs_zs.d` |
| ví dụ ngẫu nhiên trong miền đã cao hơn hẳn không ví dụ | DESCRIPTIVE, POST HOC (không có khoảng tin cậy trên tập kiểm tra) | 6.4 | Bảng 6 | 31.48 so với 20.05; 32.96 so với 24.77 | – |
| P1 đứng vững khi bỏ 12 truy vấn bị gắn cờ | POST HOC (không phán quyết) | 6.2 | trong lời | +4.47 [3.44, 5.41] trên 1,929 truy vấn | `c1_ov_test_posthoc.json::estimate.P1.d` |
| bộ nhớ tiếng Việt 10,501 ảnh, bộ nhớ tiếng Anh 112,255 ảnh | DESCRIPTIVE | 1, 3.1, 8.1 | Bảng 3 | 10,501; 112,255 | `lists.json::counts.memory_images`; `build.log::kept` |
| bước xoá gỡ khỏi chú thích có ví dụ truy hồi nhiều hơn khỏi chú thích có ví dụ ngẫu nhiên | DEVELOPMENT, non-confirmatory ("HOLDS") | 6.8 | Bảng S14 | tỉ lệ lùi về không ví dụ 0.344 so với 0.182; +5.36 [3.53, 7.12] và +2.41 [0.57, 4.26] | `decide.json::AB-tau.guard_rates.0.10.ret.fallback_rate`; `decide.json::AB-tau.guard_rates.0.10.rand.fallback_rate`; `decide.json::AB-tau.delta.-inf.d` |
| thiết kế có đăng ký, năm tập kiểm tra, mỗi tập một lần nhìn; SESOI +2.0 | DESCRIPTIVE (thiết kế) | 5.1–5.6, 8.1, 8.6 | Bảng 4, 5, 10 | B = 2,000; hạt giống 0 | – |
| cần đối chứng ngẫu nhiên cùng k và kết quả theo từng mô hình nền trước khi quy mức tăng cho truy hồi | diễn giải, dựa trên các hàng REGISTERED ở trên | 10 | – | – | – |
| các dự đoán truy hồi–ngẫu nhiên chỉ qua ở nơi bộ nhớ cùng nguồn với tập đích ("an observation and not a tested cause") | POST HOC (cách đọc, chưa kiểm) | 8.4, 10 | Bảng 12, Hình 1 | – | – |
| mọi hàng đăng ký, sai lệch và tiếp xúc đều được báo cáo | DESCRIPTIVE | 7 | Hộp 2, Phụ lục S | – | – |

Các kết quả của nghiên cứu phân bổ không nằm trong tóm tắt, đóng góp hay kết luận; để tiện tra cứu, khoá của ba kết quả chính là: phán quyết K1 ở `STEP10_qwen25vl_7b.json::A1` (và hai tệp tương ứng của hai mô hình nền kia); hai khẳng định được đề cử ở `VERDICT.json::sets.ov_dev_b.rows.qwen25vl_7b|tau_pair.d` và `VERDICT.json::sets.ov_dev_b.rows.internvl3_8b|tau_pair.d`; đối chứng dương ở `B3_SUMMARY.json::sets.ov_dev_b.rows.lmcap|tau_sel.d`. Cả ba mang trạng thái DEVELOPMENT, non-confirmatory.

## C.14 Danh mục việc cần rà soát và hoàn thiện

### C.14.1 Lỗi hoặc mâu thuẫn cần sửa

1. **Tóm tắt không còn hàng COCO của InternVL3 nhưng Mục 7 nói là có** (`00_abstract.md`; `07_disclosures.md`, đoạn tóm tắt sai lệch và Hộp 2). Đưa lại hàng −1.64 [−2.79, −0.49] vào tóm tắt trong giới hạn 150–200 từ, hoặc sửa Mục 7 và Hộp 2.
2. **Các mục đã đăng ký của nghiên cứu phân bổ không có kết cục, và mốc đóng băng viết ở thì tương lai** (Mục 3.8 câu cuối; Mục 5.7 phần nguồn bộ nhớ, họ S-BB và phần ngân sách; Mục 6.10.1). Ghi rõ cho từng mục: đã chạy với kết quả nào, hoặc "NOT RUN" kèm lý do; giải thích vì sao có khối 0, 1, 1b, 3 mà không có khối mang số 2.
3. **Quy tắc qua của H_G vắng mặt** (Mục 5.1, Mục 6.7). Thêm định nghĩa và hai điều kiện từ bản đăng ký giai đoạn 2, và nói rõ H_G trượt ở điều kiện chi phí CIDEr-D (−4.01) dù khoảng tin cậy của hiệu độ chính xác nằm trên 0.
4. **Số mục và số ảnh phân biệt của OV-test** (Mục 4, Bảng 3). Bản đăng ký ghi 2,001 mục, 1,997 ảnh phân biệt, và tập chính 1,941 mục, 1,937 ảnh phân biệt; bài chỉ nói "ảnh". Thêm một câu và nêu rằng mỗi mục là một đơn vị bootstrap.
5. **Việc mất sổ điểm Flickr30K test chỉ được nêu ở Mục 9.3 và Mục 10.** Thêm vào danh sách công bố của Mục 8.6 và Hộp 2.
6. **Mục 9.2 viết lời nhắc có ảnh ví dụ là "untested"** trong khi Bảng 18 và Bảng S19 có hàng phát triển cho định dạng này. Sửa thành chưa được kiểm trên tập kiểm tra.
7. **Bản đồ mục và đánh số bảng.** Bản đồ mục ở Mục 1 thiếu Mục 6.10 và 6.11; Bảng 15–18 đứng trước Bảng 10–14; "Bảng 1b" cần số riêng.
8. **Trạng thái hai nghiên cứu đồng hành** ghi khác nhau giữa `01_introduction.md` ("in preparation") và `V2_PROGRESS_C.md` ("under review"). Thống nhất theo trạng thái thật lúc nộp.
9. **Dạng số và thuật ngữ không thống nhất.** Lưới τ (0.0, 0.1 ở Mục 3.5 so với 0.00, 0.10 ở các bảng); xác suất dự phóng (0.95 và 0.70 trong lời so với 0.953 và 0.700 ở Bảng 13); hai chữ "detected" và "DETECTED".
10. **Bảng S22 và Bảng S16 in hai giá trị cho cùng tương phản theo lô** của Qwen2.5-VL-7B trên OV-dev-B (+9.25 [7.59, 11.14] và +9.67 [7.68, 11.72]) mà không có chú thích về số lần rút.
11. **Thuật ngữ chưa định nghĩa.** Tỉ lệ hit-max, tỉ lệ gần nguyên văn, tỉ lệ chép 4-gram (Mục 3.5, Bảng S1–S4); "exploration halves" (Mục 6.9); tập đối chiếu của bộ lọc trên hai nửa OV-dev (Mục 4).
12. **Các chỗ còn để ngỏ trong hồ sơ.** Đường dẫn kho mã và DOI (Mục 10); khối tác giả, ORCID, mã CCS, chế độ ẩn danh và bố cục bảng rộng của phụ lục (`V2_PROGRESS_C.md`); nguồn cho nhãn Open Images V7; tên phụ lục và các tiêu đề "moved from".

### C.14.2 Điểm nên làm rõ

1. **Căn cứ của các ngưỡng**: SESOI +2.0, sàn −1.0 của P2 và XM-b, ngưỡng 0.10 của quy tắc L (Mục 5.2). Nếu là giá trị hoạch định thì nói rõ cho cả ba.
2. **Phạm vi của câu "not detected for InternVL3"**: nêu trong tóm tắt và Mục 1 rằng nhánh đăng ký của InternVL3 gồm bước xoá; nhắc cạnh P2 rằng 0.351 số chú thích `ret` của InternVL3 là chú thích không ví dụ (Mục 3.5, 6.2).
3. **Cấu hình được chọn theo điểm `ret`, và đại lượng gộp trộn hai cấu hình** (Mục 3.5, 5.2): đặt hai câu này cạnh Bảng 2 và trong Mục 9.2.
4. **Tham số tái lập**: cỡ lô của mỗi mô hình nền và nguyên văn khuôn lời nhắc (Mục 3.3, 9.3).
5. **`rand` − `zs` trên tập kiểm tra** không có khoảng tin cậy (Mục 6.4); cân nhắc một hàng POST HOC hoặc dẫn tới $\tau_{\text{any}}$ ở Bảng 16.
6. **Hệ quả của K1**: trong Mục 9.1, dẫn thẳng tới cặp Bảng S22 và Bảng 16; nối cờ giả dược của Aya-Vision-8B và các tỉ phần phương sai với điều kiện "một lần rút `rand`" của khoảng tin cậy kiểm tra.
7. **Cận sao chép**: giải thích nhãn trên một cận ("REVERSED" của $L_{\text{cp}}$ nghĩa là cận không có thông tin) và ý nghĩa của $K_{\text{nc}}$ lớn (Mục 6.10.6).
8. **Tỉ trọng và văn phong của phần phân bổ**: rút gọn Mục 5.7, 6.10 và 7.5; bỏ các câu lặp theo khuôn; chuyển chi tiết vận hành vào phụ lục; quyết định dứt khoát vai trò của phần này trong thông điệp của bài.
9. **Lý do chọn ví dụ chỉ-văn-bản** (Bảng S19): đưa vào thân bài.
10. **Chính sách công bố sổ điểm theo ảnh, lập trường về giá trị p và một câu về đa kiểm định qua các đăng ký** (Mục 5.4, 9.3).
11. **Công trình liên quan**: đọc toàn văn hai công trình mới chỉ lập hàng từ tóm tắt; làm một lượt tìm tài liệu có hệ thống và ghi ngày (Mục 2, Phụ lục S).

### C.14.3 Câu hỏi phản biện có thể gặp

1. Đối chứng ngẫu nhiên, mẫu hình trên COCO và so sánh ngẫu nhiên–tương tự đa ngữ đều đã có; điều gì là mới? Câu trả lời của bài nằm ở đoạn định vị cuối Mục 2 (bối cảnh, thiết kế, đường cơ sở cùng dữ liệu; không tuyên bố ưu tiên).
2. Vì sao SESOI là +2.0 và vì sao không hiệu chỉnh lại cho thang PTB? (Mục 5.2, 5.4, 8.1.)
3. Mức tăng do một mô hình nền mang; kết luận có tổng quát không? (Mục 9.1; bài nói không thể biết thuộc tính nào dự báo mức tăng.)
4. Vì sao giữ bước xoá trong đại lượng đăng ký của InternVL3 khi mô hình kiểm chứng phân biệt kém và bước xoá làm giảm điểm? (Mục 3.5, 6.6, 6.7; Bảng 9, S9, S12.)
5. Mức tăng CIDEr có phải chỉ là mượn câu chữ? (Mục 9.2; hàng che n-gram ở Bảng S19; cận sao chép ở Mục 6.10.6; tỉ lệ gần nguyên văn; P2.)
6. Giải mã theo lô có làm chệch các tương phản đăng ký không? (Mục 6.10.2, 9.1, 9.3.)
7. Vì sao NoCaps "FAIL" khi khoảng tin cậy nằm trên 0, và vì sao quy tắc được chọn sau XM-a? (Mục 8.1, 8.3, 9.2.)
8. So sánh E3 có công bằng với LMCap không? (Mục 3.7, 8.6: bốn sai khác, chênh cỡ mô hình, cận vững thô.)
9. Khoảng tin cậy có điều kiện theo một lần rút `rand`; biến thiên do lần rút lớn đến đâu? (Mục 5.2, 6.10.5.)
10. Không có đánh giá của người và độ đo đối tượng dựa trên hợp các tham chiếu; kết luận về độ trung thực vững đến đâu? (Mục 9.1.)
11. Tạp chí mong đợi giá trị p; vì sao bài không có? (Mục 5.4.)
12. Bên thứ ba có tính lại được khoảng tin cậy không khi sổ điểm theo ảnh không được công bố và một sổ điểm đã mất? (Mục 9.3.)
13. Mô hình nền có thể đã thấy COCO khi huấn luyện; đối chứng `rand` khử được đến đâu? (Mục 9.1, hạn chế 8.)
14. Bốn cặp ảnh trùng trong OV-test được tính như đơn vị bootstrap độc lập; ảnh hưởng thế nào? (Mục 4; bản đăng ký kiểm tra.)

## C.15 Thuật ngữ và ký hiệu

**Bảng C.27.** Thuật ngữ và ký hiệu của bài báo.

| Thuật ngữ, ký hiệu (tiếng Anh) | Tiếng Việt dùng trong báo cáo | Nghĩa |
|---|---|---|
| retrieval in-context captioning | sinh chú thích theo ngữ cảnh có truy hồi | đặt chú thích của ảnh bộ nhớ giống truy vấn vào lời nhắc của MLLM, không huấn luyện |
| memory, cluster | bộ nhớ, cụm | kho ảnh có chú thích dùng để lấy ví dụ; nhóm ảnh gần trùng, mỗi cụm đưa ra nhiều nhất một lần |
| backbone | mô hình nền | MLLM sinh chú thích: Qwen2.5-VL-7B, InternVL3-8B, Aya-Vision-8B |
| `ret`, `rand`, `fix`, `zs` | nhánh truy hồi, ngẫu nhiên, cố định, không ví dụ | bốn nhánh của Bảng C.3 |
| `nn_top1`, `nn_cons` | đường cơ sở sao chép | xuất thẳng chú thích của láng giềng gần nhất hoặc chú thích đồng thuận |
| retrieval near cut | ngưỡng cắt cận | cụm có cosine SigLIP2 với truy vấn ≥ 0.92 không được đưa ở nhánh nào |
| k; order; tail T1, T2 | số ví dụ; thứ tự; đuôi lời nhắc | tham số cấu hình của lời nhắc |
| τ | ngưỡng xoá | ngưỡng trên điểm kiểm chứng s của bước xoá; τ = −∞ là không xoá |
| neighbour-only object | đối tượng chỉ-từ-láng-giềng | đối tượng có trong chú thích, vắng trong chú thích không ví dụ và có trong một ví dụ được đưa |
| verifier; deletion step; fallback | mô hình kiểm chứng; bước xoá; lùi về không ví dụ | VLM trả lời có/không về một lớp; gỡ đơn vị chứa lớp bị bác; thay bằng chú thích không ví dụ |
| guard, H_G | cơ chế chắn, giả thuyết H_G | giả thuyết giai đoạn B về bước xoá; kết quả âm có đăng ký |
| stripped CIDEr-D | CIDEr-D đã lược dấu câu cuối | cột quyết định tiếng Việt, trên văn bản đã tách từ |
| PTB CIDEr-D | CIDEr-D tách token kiểu PTB | cột quyết định tiếng Anh |
| document frequency | tần suất tài liệu | trọng số IDF của CIDEr-D, tính trên tham chiếu của tập được chấm |
| ΔP_cm (count-matched object precision) | độ chính xác đối tượng so khớp số lượng | công thức (C.9); so với chú thích không ví dụ ở cùng số lớp |
| verified precision | độ chính xác đã kiểm chứng | độ chính xác đối tượng theo nhãn Open Images do người xác minh (XM-b) |
| CHAIR_i | CHAIR_i | tỉ lệ đối tượng được nhắc mà nhãn vàng không ủng hộ |
| stage A, stage B | giai đoạn A, giai đoạn B | chọn cấu hình; cổng một lần nhìn trên tập phát triển |
| preregistration; one look | tiền đăng ký; một lần nhìn | cố định quy tắc trước dữ liệu; mỗi tập kiểm tra được giải mã, chấm, quyết định một lần |
| estimand; pooled | đại lượng ước lượng đích; gộp | đại lượng mà quy tắc quyết định dựa vào; trung bình hiệu theo ảnh qua hai mô hình nền |
| SESOI | cỡ hiệu ứng nhỏ nhất đáng quan tâm | +2.0 điểm CIDEr-D |
| P1, P1b, P2, XM-a, XM-b | dự đoán tiếng Việt đã đăng ký | Bảng C.7 |
| rule L | quy tắc độ dài L | chênh độ dài tương đối giữa `ret` và `rand` không quá 0.10 |
| scope sentence | câu phạm vi | câu cố định trước, đặt cạnh mọi số gộp (Bảng C.8) |
| P1-EN, S-NC | dự đoán tiếng Anh đã đăng ký | Bảng C.21 |
| E1, E2, E3a–c | khẳng định của đăng ký Flickr30K | `ret` − `rand` (E1, E2); `ret` − LMCap (E3a–c) |
| carve; rehearsal | phần tách; diễn tập | tập thăm dò rút từ tập huấn luyện; lần thử một lần trên val trước kiểm tra |
| paired image bootstrap | bootstrap ghép cặp theo ảnh | lấy mẫu lại ảnh, B = 2,000, khoảng phân vị 95% |
| p̃ (p-like statistic) | thống kê dạng p | công thức (C.10); sàn 1/2,001; không phải giá trị p chính xác |
| detected (chữ thường) | "detected" | hàng báo cáo có cận dưới khoảng tin cậy 95% trên 0; không phải phán quyết |
| DETECTED, REVERSED, NEGLIGIBLE, UNRESOLVED | bốn nhãn của nghiên cứu phân bổ | quy tắc nhãn ở C.6.6 |
| `perm` | nhánh hoán vị | danh sách truy hồi của ảnh khác cùng tập, lọc theo ngưỡng cắt cận của truy vấn |
| τ_any, τ_sel, τ_marg, τ_pair | bốn đại lượng phân bổ | `rand` − `zs`; `ret` − `rand`; `perm` − `rand`; `ret` − `perm` |
| split of a known τ_sel | phép tách của một τ_sel đã biết | nhãn cho τ_pair, τ_marg trên tập mà tổng đã biết |
| A1, K1, D1 | giả định độc lập theo lô, cổng dừng, phép kiểm tất định | Mục 6.10.2 |
| K_ret, L_cp, K_nc, κ_q | cận sao chép và phép kiểm chiều | công thức (C.5)–(C.7); κ_q không phải hệ số đồng thuận κ của Mục 6.9 |
| positive control | đối chứng dương | τ_sel của LMCap trên OV-dev-B, phải mang nhãn "DETECTED" |
| placebo | giả dược | `rand` d1 − `rand` d2; hoặc mất mát của chú thích `zs` khi bị che |
| ω̂, ω^U | tỉ số phương sai giữa các bộ cố định | công thức (C.12); quyết định nhãn "conditional on the realised fixed set" |
| δ | hiệu ứng nguồn bộ nhớ | công thức (C.13) |
| `lmcap_ri`, `lmcap_rand`, `lmcap_perm`; `ret_img`, `rand_img` | các nhánh bên thứ ba (khối 3) | LMCap với chú thích truy hồi, ngẫu nhiên, hoán vị; ví dụ dạng cặp ảnh–chú thích |
| C-ATTR-DEV | đăng ký phân bổ | mọi hàng mang "development, non-confirmatory" |
| AB-τ, AB-K, AB-M | ablation ngưỡng xoá, số ví dụ, cỡ bộ nhớ | Mục 6.8, chỉ trên tập phát triển |
