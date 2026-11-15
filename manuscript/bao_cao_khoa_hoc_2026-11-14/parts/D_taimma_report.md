# Phần D. Ví dụ truy hồi có hơn ví dụ ngẫu nhiên không? Phép thử đăng ký trước cho sinh chú thích ảnh tiếng Việt theo ngữ cảnh (Do Retrieved Examples Beat Random Ones? A Preregistered Test of In-Context Vietnamese Image Captioning)

Phần này rà soát bản nháp thứ nhất của phiên bản hội nghị của Bài báo C, soạn cho TAIMMA 2027 theo định dạng Springer LNCS. Bản đầy đủ có giải thích là bản tạp chí (Phần C); ở đây chỉ trình bày những gì bản hội nghị in ra, những gì nó giữ, rút gọn hoặc bỏ, các giới hạn của hội nghị và những quyết định còn chờ nhà nghiên cứu.

## D.1 Thông tin chung

**Hội nghị đích.** Bảng D.1 ghi các dữ kiện theo báo cáo khảo sát đọc ngày 13/11/2026 (21:30–23:15 giờ Việt Nam). Báo cáo kết luận về độ tin cậy là "unclear": con người và cơ sở tổ chức có thật, không thấy dấu hiệu gian lận, nhưng đây là kỳ đầu tiên và hai khẳng định quan trọng nhất (nhà xuất bản nhận in kỷ yếu, trường chủ nhà đăng cai) chỉ được xác nhận trên các kênh do ban tổ chức kiểm soát.

**Bảng D.1.** Dữ kiện về TAIMMA 2027 và trạng thái kiểm chứng (theo báo cáo khảo sát hội nghị).

| Dữ kiện | Theo nguồn | Trạng thái kiểm chứng |
|---|---|---|
| Tên | TAIMMA 2027, "The First International Conference on Transformative Applied Informatics and Mixed-Methods Analytics"; kỳ đầu tiên | chỉ theo trang hội nghị |
| Thời gian, địa điểm | 16–18/3/2027, Kyoto, Nhật Bản; trực tiếp 16–17/3, trực tuyến 18/3 | theo trang hội nghị; ngày vừa dời hôm 13/11/2026 từ 27–29/3/2027, thư của nhà xuất bản vẫn ghi ngày cũ |
| Hạn nộp bài (AoE, tức UTC−12) | đợt một 5/11/2026 (đã qua); đợt hai 20/11/2026 AoE, tức 21/11 18:59 giờ Việt Nam; đợt ba 2/12/2026 AoE, tức 3/12 18:59 giờ Việt Nam | đọc trên trang hội nghị |
| Thông báo; bản cuối | thông báo 30/11, 10/12, 25/12/2026 (AoE; báo cáo không quy đổi giờ Việt Nam); bản in cuối và đăng ký tác giả 10/1/2027 AoE, tức 11/1 18:59 giờ Việt Nam | theo trang hội nghị |
| Định dạng, độ dài | mẫu Springer LNCS; bài đầy đủ "minimum 12 pages, maximum 15 pages"; bài ngắn tối thiểu 6 trang, không nêu tối đa | theo trang hội nghị; trang kêu gọi bài ghi "12–15 pages recommended"; không nêu độ dài tóm tắt, số từ khóa, cách tính trang cho tài liệu tham khảo, phụ lục |
| Phản biện, nộp bài | "Single-blind"; ít nhất ba phản biện; Microsoft CMT | theo trang hội nghị; đường dẫn nộp bài chưa xác nhận được |
| Tính nguyên gốc | "Papers must be original, unpublished, and not under review elsewhere." | theo trang hội nghị |
| Xuất bản | Springer CCIS "(confirmed)" | **chưa kiểm chứng**: chỉ có trang đầu một lá thư đề ngày 10/10/2026 do ban tổ chức lưu, ghi "in principle"; trang của nhà xuất bản không nêu hội nghị; chỉ số "Q4, SJR 2025 0.18" của chuỗi chưa xác nhận |
| Phí mức sớm (đến 10/1/2027) | trực tuyến USD 155, trực tiếp USD 380; sinh viên USD 130 và USD 320 | theo trang hội nghị; không nêu quy tắc rút bài |
| Chủ đề | không nêu tên sinh chú thích ảnh hay tiếng Việt; gần nhất là "Information retrieval and recommender systems" và "NLP and LLMs" | theo trang hội nghị |

**Quan hệ với bản tạp chí.** Kế hoạch viết đề nghị phương án S1: bản hội nghị là nghiên cứu chính đã đăng ký ở dạng cô đọng, gồm phép thử tiếng Việt (OpenViIC, XM3600) và nhánh tiếng Anh (COCO, NoCaps). Phần chỉ dành cho tạp chí gồm nghiên cứu quy kết, đăng ký Flickr30K, các phép cắt bỏ trên tập phát triển, chẩn đoán lọc ví dụ và phụ lục, tức khoảng 49% văn bản chính (khoảng 15,200 trên 30,700 từ) cộng 11 trong 27 bảng phụ lục. Kế hoạch nêu thẳng ba cái giá. Một, lõi xác nhận của bản tạp chí trở thành công bố trước: bản tạp chí phải trích bản hội nghị, mô tả phần trùng và viết lại tóm tắt quanh phần mở rộng, vốn chủ yếu chỉ dùng tập phát triển. Hai, quy tắc "not under review elsewhere" cấm nộp song song, nên bản tạp chí chỉ nộp được sau khi hội nghị có kết quả. Ba, chính sách công bố trước của ACM chưa được đọc trên trang gốc; mức "≥ 25% new content" chỉ là giá trị ghi trong thẻ tạp chí và phải được đọc lại trước khi nộp hội nghị. Vì bộ quy tắc của nhà xuất bản ghi "Recycling data and texts from an Author's own published manuscripts is generally not allowed", bản nháp viết lại câu chữ thay vì chép; chỉ các nhãn đã đăng ký và câu chữ đăng ký cho XM-a thất bại được giữ nguyên văn, và hai bản mang hai tên khác nhau. Hai dữ kiện của phần chỉ dành cho tạp chí được cố ý đưa sang: chú thích † trên mọi hàng `fix` và hạn chế về thành phần lô giải mã.

**Tên tạm, khẳng định và bố cục.** Tên tạm (14 từ) là tên ở tiêu đề phần này. Câu đóng góp của kế hoạch: trong một phép thử đăng ký trước với một lần nhìn cho mỗi tập kiểm thử, chú thích ví dụ được truy hồi cho điểm cao hơn cùng số chú thích ngẫu nhiên từ cùng bộ nhớ ở nơi bộ nhớ và tập kiểm thử cùng nguồn (OpenViIC, COCO), chủ yếu ở một trong hai mô hình nền; ngoài nguồn của bộ nhớ, các dự đoán đã đăng ký thất bại (XM3600 tiếng Việt, NoCaps). Bản nháp viết "The study proposes no new method" và nêu ba đóng góp: một thiết kế đánh giá có đăng ký; kết quả trong nguồn của bộ nhớ ở hai ngôn ngữ; kết quả ngoài nguồn, không có khẳng định chuyển giao. Bố cục gồm tóm tắt, từ khóa, tám mục đánh số (ứng với Mục D.3 đến D.10 dưới đây) và các tuyên bố cuối bài; bản nháp có 7 bảng, 1 hình, thuộc loại bài đầy đủ với mục tiêu 14 trang và không giả định có phụ lục.

## D.2 Tóm tắt và từ khóa

**Nội dung.** Tóm tắt nêu vấn đề (mức tăng so với zero-shot có thể đến từ việc thấy bất kỳ chú thích trong miền nào chứ không phải từ truy hồi), thiết kế (đăng ký trước, một lần nhìn, chú thích truy hồi so với cùng số chú thích ngẫu nhiên từ cùng bộ nhớ, hai mô hình báo cáo riêng) và các kết quả chính, với số của Bảng D.6 và Bảng D.7: P1 "PASS" kèm quy tắc và câu phạm vi "carried mainly by Qwen2.5-VL; not detected for InternVL3"; P2 "PASS", chỉ nêu bằng lời; XM-a "FAIL" theo quy tắc đòi KTC trên không; P1-EN "PASS" dù hàng báo cáo của InternVL3 dưới không; S-NC "FAIL" vì điểm ước lượng dưới +2.0. Tóm tắt khép bằng "No transfer claim is made in either language" và khuyến nghị cần đối chứng ví dụ ngẫu nhiên cùng k và kết quả theo từng mô hình. Năm từ khóa: Image captioning, In-context examples, Retrieval augmentation, Vietnamese, Preregistration.

**Nhận xét rà soát.** Tóm tắt nêu đủ hai kết quả "FAIL" với ước lượng, khoảng tin cậy và quy tắc. Có ba điểm cần xem. Một, tóm tắt dài 233 từ, vượt ngân sách 200 từ của kế hoạch; nó nằm trong thông lệ 150–250 từ của bộ mẫu LNCS, nhưng giới hạn này không có trong báo cáo khảo sát. Hai, P2 không kèm giá trị sàn và không nói rõ nó so `ret` với `zs` chứ không so với `rand`, nên dễ bị hiểu thành "truy hồi không kém ngẫu nhiên về độ chính xác". Ba, tên bài chỉ nói tiếng Việt trong khi gần nửa tóm tắt là nhánh tiếng Anh.

## D.3 Giới thiệu (Introduction)

**Nội dung.** Mục 1 đi theo ba bước. Bối cảnh: mô hình đa phương thức mở viết được chú thích tiếng Việt mà không cần huấn luyện tác vụ, nhưng điểm zero-shot thấp xa các hệ tinh chỉnh; bản nháp dẫn 75.58 CIDEr của đường cơ sở tinh chỉnh tốt nhất trong bài công bố UIT-OpenViIC [@Bui2023OpenViIC] và ghi rõ đó là số đã công bố, không so sánh được với bộ chấm của nghiên cứu. Tiếng Việt ít tài nguyên theo nghĩa cụ thể [@Joshi2020StateFate]: các bộ chú thích miền chung ít, nhỏ hơn nhiều so với COCO, mỗi bộ có miền và văn phong riêng [@Pham2024KTVIC; @Bui2023OpenViIC]. Vấn đề: các bài phương pháp báo cáo mức tăng CIDEr lớn nhờ ví dụ truy hồi [@Ramos2023LMCap; @Rebelo2025RSCap], nhưng mức tăng ấy có thể phản ánh *truy hồi* (ví dụ mô tả ảnh tương tự) hoặc *văn phong trong miền* (ví dụ chỉ cho thấy cách viết của bộ dữ liệu); theo bản nháp, "As far as those papers state, none preregisters its contrasts or reports confidence intervals on the captioning score, and none covers Vietnamese". Thiết kế: bốn kiểu lời nhắc (`ret`, `rand`, `fix`, `zs`), cấu hình đóng băng trên dữ liệu phát triển qua hai giai đoạn đã đăng ký, mỗi tập kiểm thử được giải mã, chấm và quyết định một lần, và một nhánh tiếng Anh đăng ký riêng không tinh chỉnh. Mục kết bằng ba đóng góp của Mục D.1, kèm số và nhãn.

**Nhận xét rà soát.** Câu hỏi nghiên cứu rõ và mục này không dùng "first" hay "novel". Phản biện có thể hỏi: (a) nhận định "score far below fine-tuned systems" tựa vào một con số mà chính câu đó nói là không so sánh được; nên viết nhẹ hơn; (b) câu "none preregisters… none covers Vietnamese" là nhận định về tài liệu, trong khi bản tạp chí (Mục 2) có ghi việc tìm tài liệu chỉ là một phần còn bản hội nghị đã bỏ câu ấy; nên khôi phục một mệnh đề; (c) đóng góp thứ hai ghi "in two languages" còn tên bài chỉ nói tiếng Việt.

## D.4 Công trình liên quan (Related work)

**Nội dung.** Mục 2 tách bài phương pháp, đề xuất bộ sinh chú thích đọc chú thích truy hồi [@Ramos2023SmallCap; @Ramos2023EXTRA; @Ramos2023LMCap; @Ibrahim2025CONCAP], khỏi bài phân tích, và xếp nghiên cứu này vào loại sau. Bản nháp thừa nhận đối chứng ngẫu nhiên đã có ở các bộ sinh chú thích được huấn luyện [@Ramos2023EXTRA; @Li2024RetrievalRobustness] và ở các nghiên cứu chọn ví dụ, phần lớn bằng tiếng Anh và có ảnh ví dụ [@Yang2023ICLConfig; @Li2025UnveilingICL]. Học theo ngữ cảnh đa phương thức được báo cáo là chủ yếu do văn bản của ví dụ chi phối [@Baldassini2024MICL; @Chen2025TrueMICL]; đó là lý do cần nhánh `rand`. Tiền lệ tiếng Anh là OpenFlamingo, nơi ví dụ truy hồi hơn ví dụ ngẫu nhiên trên COCO và thấp hơn trên Flickr30K ở các số ví dụ nhỏ [@Awadalla2023OpenFlamingo]; vì vậy kết quả COCO của bài "is not a new English finding". Gần nhất về đa ngữ là một nghiên cứu viễn thám không có đối chứng ngẫu nhiên cùng k [@Rebelo2025RSCap] và bộ đánh giá MUNIChus, có đối chứng ấy nhưng không gồm tiếng Việt và chỉ báo cáo điểm số dạng ước lượng điểm, không có khoảng [@Chen2026MUNIChus]; các công trình tiếng Việt trước huấn luyện hoặc thích nghi bộ sinh chú thích [@Vu2025VELVET; @Vu2026ViG; @Nguyen2026FAIR]. Điểm khác của bài là tổ hợp: mô hình không huấn luyện cho tiếng Việt, ví dụ dạng văn bản, đối chứng ngẫu nhiên cùng k từ cùng bộ nhớ bên cạnh đối chứng cố định, KTC bootstrap ghép cặp theo từng mô hình, và phép thử đăng ký một lần nhìn. Bảng 1 của bản nháp đặt nghiên cứu cạnh năm bài phân tích; cả năm được ghi là có đối chứng ngẫu nhiên, không bài nào được ghi là có phép thử đăng ký hay KTC trên điểm chú thích.

**Nhận xét rà soát.** Mục này nhường phần "đã có" cho công trình trước và giữ câu "No priority claim is made". Cần lưu ý: (a) các ô "no" của Bảng 1 là nhận định về bài của người khác, tuy có rào "Entries follow each paper's own statements" vẫn nên đọc lại trên bài gốc; (b) theo ghi chú bản nháp, cột đầu của Bảng 1 chỉ chứa khóa trích dẫn và sẽ hiện thành "[n]" trần trong kiểu đánh số của LNCS; (c) [@Nguyen2026FAIR] là bài hội nghị trước của chính nhóm, và kế hoạch ghi việc tự kiểm tra trùng lặp với bài này là chưa làm; (d) các số của OpenFlamingo đã bị bỏ nên câu "at the smaller shot counts it reports" mơ hồ.

## D.5 Phương pháp (Method)

**Nội dung.** *Bộ nhớ.* Bộ nhớ tiếng Việt ghép ảnh huấn luyện KTVIC ngoài phần tách phát triển [@Pham2024KTVIC] với ảnh huấn luyện UIT-OpenViIC [@Bui2023OpenViIC]: 3,469 + 9,088 = 12,557 ứng viên. Một bộ lọc định trước loại 2,056 ứng viên (tệp không đọc được, ảnh trùng hoặc gần trùng với ảnh đánh giá). 10,501 ảnh còn lại tạo thành 8,190 cụm theo một quy tắc tương tự thị giác định trước [@Pizzi2022SSCD]; mỗi cụm được hiện tối đa một lần cho mỗi truy vấn, qua một chú thích.

*Các nhánh.* Ảnh được nhúng bằng SigLIP2 [@Tschannen2025SigLIP2]. Cụm có cosine với truy vấn từ 0.92 trở lên không được hiện ở bất kỳ nhánh nào (ngưỡng cắt gần). Các nhánh dùng chung một khuôn lời nhắc và chỉ khác khối ví dụ: `ret` lấy k cụm hợp lệ có cosine cao nhất; `rand` lấy k cụm hợp lệ rút bằng bộ sinh số có hạt giống; `fix` dùng một bộ k cụm rút một lần cho mỗi tập kiểm thử; `zs` không có ví dụ. Hai đường cơ sở sao chép không dùng mô hình: chú thích của cụm gần nhất (NN-top1) và chú thích đồng thuận trong k cụm gần nhất (NN-consensus) [@Devlin2015NN].

*Lời nhắc và giải mã.* Lời nhắc đứng sau ảnh: một tiêu đề tiếng Việt cố định nói rằng các chú thích bên dưới thuộc ảnh khác và chỉ minh họa cách viết, k dòng ví dụ, và phần đuôi yêu cầu một câu tiếng Việt ngắn theo văn phong của ví dụ. Đuôi T1 yêu cầu thêm chỉ nêu những gì nhìn thấy; đuôi T2 thì không. "Order" đặt ví dụ giống nhất lên đầu, hoặc xuống cuối sát câu lệnh. Khuôn lời nhắc không chứa chú thích nào của bộ dữ liệu. Giải mã tham lam, tối đa 60 token mới, cho Qwen2.5-VL-7B-Instruct [@Bai2025Qwen25VL] và InternVL3-8B [@Zhu2025InternVL3].

*Bước xóa.* Một lớp đối tượng là "neighbour-only" khi bộ khớp đối tượng tìm thấy nó trong chú thích và trong ít nhất một ví dụ được hiện, nhưng không có trong chú thích zero-shot của cùng mô hình. Một mô hình thứ hai, bộ kiểm chứng, chấm mỗi lớp như vậy bằng

$$s = p_{\text{yes}}(\text{có ảnh}) - p_{\text{yes}}(\text{không có ảnh}), \qquad \text{lớp bị loại khi } s < \tau, \tag{D.1}$$

với $p_{\text{yes}}$ là xác suất trả lời "yes" cho một câu hỏi có/không về lớp đó và $\tau$ là ngưỡng xóa. Chú thích được cắt tại dấu phẩy, liên từ và từ chỉ vị trí; phần nào nêu lớp bị loại thì bị bỏ; nếu phần chủ ngữ bị chạm hoặc kết quả hỏng thì dùng chú thích zero-shot. Với $\tau = -\infty$ không có gì bị loại.

*Cấu hình đóng băng.* Giai đoạn phát triển A chọn một cấu hình cho mỗi mô hình theo một quy tắc viết trước khi có đầu ra (Bảng D.2); không đổi gì cho phép thử hay cho tiếng Anh. Chú thích `ret`, `rand` và `fix` của InternVL3 đi qua bước xóa ở τ = 0.10, nên bước này là một phần của đại lượng ước lượng đã đăng ký của InternVL3; chú thích của Qwen2.5-VL được chấm nguyên như giải mã. Bước xóa được giữ dù ở giai đoạn B giả thuyết bảo vệ H_G mang nhãn "not passed" (thay đổi độ chính xác gộp +2.91 [0.46, 5.31] điểm, với cái giá −4.01 điểm CIDEr-D đã tước dấu câu); bản nháp ghi "No guard claim is made".

**Bảng D.2.** Cấu hình đóng băng (Bảng 2 của bản nháp, Mục 3).

| | Qwen2.5-VL-7B | InternVL3-8B |
|---|---|---|
| k | 8 | 4 |
| thứ tự (order) | first | last |
| đuôi lời nhắc | T1 | T2 |
| ngưỡng xóa τ | −∞ (không xóa) | 0.10 |
| bộ kiểm chứng khi kiểm thử | không | Qwen3-VL-8B-Instruct |

*Chấm điểm.* Chú thích và tham chiếu tiếng Việt được chuyển chữ thường và tách từ bằng RDRSegmenter [@Nguyen2018VnCoreNLP; @Vu2018VnCoreNLP]. CIDEr-D [@Vedantam2015CIDEr] lấy tần suất tài liệu từ tham chiếu của chính tập được chấm và tính theo điểm (điểm số nhân một trăm). Cột quyết định là CIDEr-D *đã tước dấu câu* (stripped): bỏ token dấu câu ở cuối của cả ứng viên lẫn tham chiếu, để không nhánh nào được lợi chỉ nhờ dấu chấm cuối câu.

*Độ chính xác đối tượng khớp số lượng.* Bản nháp ghi đây là công cụ của một bản thảo đồng hành cùng nhóm (đang chuẩn bị) và in đầy đủ định nghĩa vì P2 dùng nó. Với ảnh $i$, $M_i(\text{run})$ và $M_i(\text{zs})$ là các lớp đối tượng phân biệt được khớp, theo thứ tự nhắc đến lần đầu, trong chú thích của lượt chạy và trong chú thích zero-shot của cùng mô hình; $tp_{cm}$ đếm số lớp trong $k_i$ lớp đầu của chú thích lượt chạy được nhãn vàng ủng hộ, $tp_{cm,zs}$ đếm tương tự cho chú thích zero-shot. Khi đó, tính bằng điểm phần trăm,

$$k_i = \min\bigl(|M_i(\text{run})|,\ |M_i(\text{zs})|\bigr), \qquad \Delta P_{cm} = \frac{\sum_i tp_{cm} - \sum_i tp_{cm,zs}}{\sum_i k_i}. \tag{D.2}$$

Số lần nhắc bằng nhau giúp chú thích dài hơn không bị phạt chỉ vì nêu nhiều đối tượng hơn. Nhãn vàng của một ảnh là hợp các lớp mà bộ khớp tiếng Việt đã chuẩn hóa dấu thanh tìm thấy trong các tham chiếu; CHAIR_i [@Rohrbach2018CHAIR] dùng cùng nhãn vàng. Độ chính xác đã kiểm chứng trên XM3600 (XM-b) đếm mọi lần nhắc so với nhãn Open Images do người kiểm chứng [@Kuznetsova2020OpenImages].

**Nhận xét rà soát.** Mục 3 đủ để hiểu bốn nhánh và hai công cụ đo mà không cần phụ lục. Các điểm cần sửa hoặc làm rõ:

- *Quy tắc của H_G không được nêu.* Người đọc thấy một thay đổi dương với KTC trên không mà nhãn lại là "not passed". Bản tạp chí (Mục 5.1 và Mục 6.7) cũng chỉ ghi nhãn. Cần thêm một mệnh đề nêu quy tắc đã đăng ký.
- *Quy tắc chọn cấu hình* bị rút còn "a rule written before any output"; bản tạp chí (Mục 3.5) nêu hàm mục tiêu, ba điều kiện và lưới tìm kiếm. Nên giữ một câu, vì hai mô hình khác nhau ở cả k, thứ tự, đuôi và τ.
- *Ký hiệu mẫu số.* Bản nháp viết Σ k_i và "in percentage points"; Bảng 4 của bản tạp chí viết "100 · (Σ tp_cm − Σ tp_cm,zs) / Σ k_cm". Hai bản nên dùng một ký hiệu.
- *Định nghĩa in trước bài gốc* là nội dung quyết định D8 (Mục D.14).
- *Khả năng lặp lại.* Biến thể SigLIP2, ngưỡng của bộ lọc gần trùng, cách chọn chú thích của một cụm và hạt giống của `rand` không còn trong bài, trong khi dữ liệu và mã mới ở mức "on request".
- *Bộ kiểm chứng Qwen3-VL-8B-Instruct* không có trích dẫn; tệp tài liệu tham khảo của Bài báo C không có mục cho mô hình này.
- *Đơn vị độ dài của quy tắc L* không được nêu; bản tạp chí đếm theo âm tiết cho tiếng Việt (Mục 3.6) và theo token PTB cho tiếng Anh (Mục 8.2).

## D.6 Dữ liệu và kế hoạch đã đăng ký (Data and registered plan)

**Nội dung.** *Dữ liệu.* Nghiên cứu chỉ dùng các bộ dữ liệu công khai với tham chiếu và nhãn đã phát hành; không gán nhãn mới và nhãn vàng không bao giờ lấy từ đầu ra của mô hình (Bảng D.3). 3,600 ảnh XM3600 [@Thapliyal2022XM3600] được chia trước khi nghiên cứu có đầu ra: 600 ảnh để riêng làm tập đánh giá của bản thảo đồng hành, phần còn lại xếp theo giá trị băm của tệp ảnh, 500 ảnh đầu là XM-dev500 và 2,500 ảnh còn lại là XM-test2500 với 5,108 tham chiếu tiếng Việt; vì thế bài không báo cáo kết quả trên toàn bộ XM3600. Bộ nhớ tiếng Việt không chứa chú thích XM3600 nào, nên XM-test2500 nằm ngoài nguồn của bộ nhớ.

**Bảng D.3.** Các tập dữ liệu (Bảng 3 của bản nháp, Mục 4). "Bộ lọc" là bộ lọc định trước của Mục 3.

| Tập | Vai trò | Số ảnh | Cách hình thành |
|---|---|---|---|
| Bộ nhớ tiếng Việt | kho truy hồi | 10,501 (8,190 cụm) | KTVIC train ngoài phần tách phát triển (3,469) cộng OpenViIC train (9,088), 12,557 ứng viên, trừ 2,056 bị bộ lọc loại |
| KTVIC dev299 | giai đoạn A: chọn cấu hình | – | phần tách phát triển của tệp huấn luyện KTVIC |
| OV-dev-A | giai đoạn A: kiểm tra chuyển tiếp | 911 | một nửa OpenViIC dev theo thứ tự băm, đã lọc |
| OV-dev-B | giai đoạn B: cổng một lần nhìn | 925 | nửa còn lại, cùng bộ lọc |
| XM-dev500 | giai đoạn B: phụ | 500 | các ảnh đầu của phần XM3600 còn lại |
| **OV-test primary** | P1, P1b, P2 | 1,941 | OpenViIC test (2,001 ảnh, là độ nhạy đã đăng ký) trừ 60 ảnh bị bộ lọc loại |
| **XM-test2500** | XM-a, XM-b | 2,500 | XM3600 trừ 600 ảnh để riêng và XM-dev500; độ nhạy đã đăng ký: 2,392 ảnh, không tính 108 ảnh có ba tham chiếu |
| Bộ nhớ tiếng Anh | kho truy hồi | 112,255 (111,927 cụm) | COCO Karpathy train và restval sau cùng quy tắc lọc |
| **COCO Karpathy test** | P1-EN | 5,000 | toàn bộ phần chia |
| **NoCaps val** | S-NC | 4,500 | toàn bộ phần chia (417 ảnh in-domain, 2,670 near-domain, 1,413 out-domain theo nhãn của bộ dữ liệu); độ nhạy đã đăng ký: 3,500 ảnh, không tính các ảnh một nghiên cứu khác của nhóm đã giải mã trước |

*Ba giai đoạn.* Mỗi giai đoạn được ghi nhận trước khi dữ liệu của nó được giải mã. Giai đoạn A, thăm dò, chọn cấu hình của Bảng D.2 trên phần tách phát triển KTVIC và kiểm tra trên OV-dev-A. Giai đoạn B nhìn OV-dev-B một lần dưới một cổng: hiệu gộp `ret` − `rand` có KTC trên không và điểm ước lượng ít nhất +4.0. Cổng trả về "PASS" với +6.04 [4.54, 7.58]; đây là kết quả phát triển và không định đoạt gì ở kiểm thử. Đăng ký kiểm thử được ghi nhận sau kết quả đó và trước mọi đầu ra kiểm thử; đăng ký tiếng Anh đến sau.

*Đại lượng ước lượng và quy tắc.* Với mô hình nền $m$ và ảnh $i$, gọi $s_{m,i}(\cdot)$ là điểm của một nhánh ở cấu hình đóng băng của $m$:

$$\Delta_{m,i} = s_{m,i}(\texttt{ret}) - s_{m,i}(\texttt{rand}), \qquad \Delta_i = \tfrac{1}{2}\bigl(\Delta_{\text{Qwen},i} + \Delta_{\text{InternVL},i}\bigr). \tag{D.3}$$

Số gộp là trung bình trên hai cặp mô hình–cấu hình khác nhau về k, thứ tự, đuôi và τ; bản nháp viết rằng nó "does not estimate the effect for a typical model" và luôn in nó cùng hai hàng theo mô hình. Cỡ hiệu ứng nhỏ nhất đáng quan tâm (SESOI) là +2.0 điểm, một giá trị hoạch định đặt trước mọi đầu ra của giai đoạn B và không suy ra từ kết quả nào trước đó. Câu phạm vi đi kèm số gộp P1 được chọn từ kết cục của P1b theo một ánh xạ cố định trước phép thử. Câu chữ cho XM-a thất bại cũng đã đăng ký: "the gain was not detected out of domain (XM3600)".

**Bảng D.4.** Dự đoán đã đăng ký và quy tắc quyết định (Bảng 4 của bản nháp, Mục 4). Δ là `ret` − `rand`; "cận dưới" là cận dưới của KTC. Các độ nhạy đã đăng ký được báo cáo bên cạnh và không bao giờ thay thế dự đoán.

| Tên | Đại lượng ước lượng | Tập | Quy tắc |
|---|---|---|---|
| **P1** (chính) | trung bình Δ_i gộp, CIDEr-D đã tước dấu câu | OV-test primary | "PASS" nếu điểm ước lượng trên +2.0 và cận dưới trên không |
| quy tắc L | theo từng mô hình, chênh lệch tương đối về độ dài chú thích trung bình giữa `ret` và `rand` | OV-test primary; COCO Karpathy test | nếu trên 0.10 ở một trong hai mô hình, "PASS" được ghi là "not separated from length" |
| P1b (không gác cổng) | trung bình Δ_m,i theo từng mô hình | OV-test primary | Qwen2.5-VL: "confirmed" nếu điểm ước lượng trên +2.0; InternVL3: chỉ báo cáo. P1b chọn câu phạm vi |
| **P2** | theo từng mô hình, ΔP_cm của `ret` so với `zs` | OV-test primary | "PASS" nếu, với mỗi mô hình, cận dưới trên −1.0 |
| **XM-a** | trung bình Δ_i gộp, CIDEr-D đã tước dấu câu | XM-test2500 | "PASS" nếu cận dưới trên không |
| **XM-b** | thay đổi độ chính xác đã kiểm chứng của `ret` so với `zs`, gộp | XM-test2500 | "PASS" nếu cận dưới trên −1.0 |
| Dự đoán XM | XM-a và XM-b | XM-test2500 | "confirmed" chỉ khi cả hai đạt; ngược lại "not confirmed" |
| **P1-EN** (chính, tiếng Anh) | trung bình Δ_i gộp, PTB CIDEr-D | COCO Karpathy test | quy tắc P1, kèm quy tắc L |
| **S-NC** (phụ, thứ tự cố định) | trung bình Δ_i gộp, PTB CIDEr-D | NoCaps val | quy tắc P1; khẳng định chuyển giao cần cả P1-EN và S-NC |
| phụ, InternVL3 ở τ = −∞ | trung bình Δ theo mô hình khi không có bước xóa | mọi tập kiểm thử | nhãn "detected" khi cận dưới trên không; không cổng nào đọc |

*Độ bất định.* KTC lấy từ bootstrap ghép cặp theo ảnh với B = 2,000 lần lấy mẫu lại và cận phân vị 95%. Với thống kê gộp, hiệu theo ảnh được lấy trung bình trên hai mô hình trước; với thống kê dạng tỉ số, tử và mẫu được lấy mẫu lại cùng nhau. Chỉ ảnh được lấy mẫu lại: mỗi ảnh có một lần rút `rand` có hạt giống và tần suất tài liệu lấy từ toàn bộ tập được chấm, nên KTC mô tả bất định do lấy mẫu ảnh có điều kiện trên cả hai; biến thiên do các lần rút khác hay giữa các lần chạy không nằm trong đó. P1 là phép thử chính duy nhất; P2 là phép thử giao–hợp (intersection–union) trên hai mô hình; dự đoán XM là một phép hội. Mọi hàng khác mang KTC không hiệu chỉnh, và không có giá trị p vì quy tắc đã đăng ký dựa trên KTC.

*Một lần nhìn.* Mỗi tập kiểm thử đi qua giải mã, chấm điểm và bước quyết định đúng một lần ở cấu hình đóng băng, và mỗi tệp quyết định mang thời điểm của nó; trong lúc chạy chỉ theo dõi số đếm, thời gian, số giây GPU và mã trả về.

**Nhận xét rà soát.** Mục 4 là xương sống của bài: nó cho thấy quy tắc có trước dữ liệu và tách dự đoán gác cổng khỏi hàng chỉ báo cáo. Các điểm cần xử lý:

- *Khả năng kiểm chứng việc đăng ký trước.* Bản nháp nói mỗi tệp quyết định "carries its time" nhưng không in thời điểm nào, và dữ liệu, mã chỉ ở mức "on request". Ghi chú bản nháp nêu rằng in các mốc thời gian cần nhà nghiên cứu đồng ý và các bản đăng ký cần được lưu ký trước khi nộp; kế hoạch (quyết định D9) cho biết hiện chưa có bản lưu ký nào. Với một bài tự gọi là "preregistered", đây là câu hỏi phản biện gần như chắc chắn.
- *Bảng 3, hàng KTVIC dev299* để trống số ảnh; Bảng 3 của bản tạp chí ghi 299.
- *Quy tắc L trên NoCaps.* Hàng S-NC của Bảng 4 ghi "the P1 rule" và Bảng 7 để "–" cho NoCaps, trong khi Bảng 11 của bản tạp chí in chênh lệch độ dài trên NoCaps (0.008 / 0.018) với nhãn "reported". Cần một mệnh đề nói rõ quy tắc L có áp dụng cho S-NC hay không.
- *Các đối chứng báo cáo ở Mục 5.3* (S-zf, `fix`, đường cơ sở sao chép, cột PTB) là phân tích phụ đã đăng ký nhưng không có trong Bảng 4; Mục 7 chỉ liệt kê các phân tích phụ *không* báo cáo.
- *Lực kiểm định.* Đoạn về lực và độ chính xác của bản tạp chí (Mục 5.4) đã bị cắt; với XM-a "FAIL" vì KTC chứa không, phản biện có thể hỏi phép thử có đủ nhạy không.

## D.7 Kết quả tiếng Việt (Results in Vietnamese)

**Nội dung.** Mọi hiệu đều ghép cặp, với KTC của Mục 4. Hiệu CIDEr-D tính bằng điểm CIDEr-D đã tước dấu câu, P2 bằng điểm độ chính xác khớp số lượng, XM-b bằng điểm độ chính xác đã kiểm chứng.

**Bảng D.5.** CIDEr-D theo nhánh, mỗi mô hình ở τ đóng băng (Bảng 5 của bản nháp, Mục 5). Hàng tiếng Việt: CIDEr-D đã tước dấu câu; hàng tiếng Anh: PTB CIDEr-D; hai thang không so sánh được. Nhánh tiếng Anh không có `fix`.

| Tập | Mô hình (τ) | `ret` | `rand` | `fix` † | `zs` |
|---|---|---|---|---|---|
| OV-test primary | Qwen2.5-VL (−∞) | 39.81 | 31.48 | 33.48 | 20.05 |
| OV-test primary | InternVL3 (0.10) | 33.62 | 32.96 | 33.01 | 24.77 |
| XM-test2500 | Qwen2.5-VL (−∞) | 57.70 | 54.56 | 51.83 | 43.74 |
| XM-test2500 | InternVL3 (0.10) | 52.85 | 54.59 | 53.65 | 42.84 |
| COCO Karpathy test | Qwen2.5-VL (−∞) | 96.36 | 88.57 | – | 59.06 |
| COCO Karpathy test | InternVL3 (0.10) | 85.34 | 86.98 | – | 78.85 |
| NoCaps val | Qwen2.5-VL (−∞) | 91.13 | 88.30 | – | 58.46 |
| NoCaps val | InternVL3 (0.10) | 83.73 | 83.10 | – | 78.30 |

† Mọi hàng `fix` đều có điều kiện trên bộ ví dụ cố định đã rút ("conditional on the realised fixed set").

**Bảng D.6.** Kết quả tiếng Việt đã đăng ký: ước lượng với KTC 95%, nhãn đúng như đăng ký và độ nhạy đã đăng ký (Bảng 6 của bản nháp, Mục 5). Phạm vi của mọi số gộp P1: "carried mainly by Qwen2.5-VL; not detected for InternVL3". Hàng "báo cáo" không có quy tắc đăng ký và mang KTC không hiệu chỉnh.

| Hàng | Ước lượng [KTC] | Nhãn | Độ nhạy đã đăng ký |
|---|---|---|---|
| *OpenViIC test, tập chính (1,941 ảnh)* | | | *toàn bộ 2,001 ảnh* |
| **P1**, `ret` − `rand` gộp | **+4.49 [3.52, 5.57]** | **"PASS"** | +4.46 [3.45, 5.38] |
| P1b, Qwen2.5-VL | +8.33 [7.01, 9.76] | "confirmed" | +8.29 [6.99, 9.59] |
| P1b, InternVL3 (τ = 0.10) | +0.66 [−0.68, 1.99] | "reported only" | +0.63 [−0.73, 1.86] |
| phụ, InternVL3 ở τ = −∞ | +3.71 [2.29, 5.14] | "detected" | +3.68 [2.20, 5.05], "detected" |
| **P2**, Qwen2.5-VL, ΔP_cm so với `zs` | **+5.41 [3.88, 7.01]** | **"PASS"** | +5.34 [3.88, 6.87] |
| **P2**, InternVL3, ΔP_cm so với `zs` | **+1.57 [0.65, 2.51]** | **"PASS"** (cả hai: "passed") | +1.35 [0.44, 2.27] |
| quy tắc L, chênh độ dài, Qwen2.5-VL / InternVL3 | 0.074 / 0.039 | "does not fire" | 0.076 / 0.042 |
| *XM-test2500 (2,500 ảnh)* | | | *2,392 ảnh* |
| **XM-a**, `ret` − `rand` gộp | **+0.70 [−0.45, 1.97]** | **"FAIL"** | +0.82 [−0.45, 2.11] |
| báo cáo, Qwen2.5-VL | +3.15 [1.50, 4.93] | – | – |
| báo cáo, InternVL3 (τ = 0.10) | −1.75 [−3.35, −0.09] | – | – |
| phụ, InternVL3 ở τ = −∞ | +0.18 [−1.36, 1.81] | "not detected" | +0.19 [−1.41, 1.79], "not detected" |
| **XM-b**, thay đổi độ chính xác đã kiểm chứng so với `zs` | **+0.59 [−0.31, 1.54]** | **"PASS"** | +0.57 [−0.41, 1.56], "PASS" |
| **Dự đoán XM** (XM-a và XM-b) | – | **"not confirmed"** | – |

*Trong nguồn của bộ nhớ: OpenViIC test (Mục 5.1).* P1 đạt "PASS": điểm ước lượng gộp vượt +2.0, KTC nằm trên không, quy tắc L không kích hoạt, và độ nhạy trên 2,001 ảnh cho cùng cách đọc ở mọi hàng. Hàng của InternVL3 ở τ đóng băng có KTC chứa không và chỉ để báo cáo. P2 đạt "PASS" cho cả hai mô hình vì cả hai cận dưới đều trên sàn −1.0; bản nháp kết luận rằng trên OpenViIC test không thấy cái giá về độ chính xác đối tượng của toàn bộ lời nhắc theo ngữ cảnh so với zero-shot, và nhấn mạnh "P2 does not compare `ret` with `rand`". Hàng phụ của InternVL3 ở τ = −∞ mang nhãn "detected" và không đổi phán quyết hay câu phạm vi nào. Với bước xóa đóng băng, một tỉ lệ 0.351 chú thích `ret` của InternVL3 rơi về chú thích zero-shot; CIDEr-D đã tước dấu câu là 33.62 so với 39.50 cho cùng lượt giải mã khi không có bước xóa; CHAIR_i là 0.254 so với 0.237; thay đổi khớp số lượng so với `zs` là +1.57 so với +5.80. Bản nháp viết: "The step lowered CIDEr-D and improved neither object measure".

Một hàng hậu nghiệm (POST HOC; không đăng ký, không phán quyết): sau phép thử, một quy tắc tương tự ảnh rộng hơn bộ lọc đã đăng ký đánh dấu 12 trong 1,941 truy vấn của tập chính có một bản gần sao của ảnh truy vấn trong ví dụ `ret` (9 trường hợp ở hạng đầu) và 0 truy vấn ở `rand`. Bỏ 12 truy vấn này, hiệu gộp là +4.47 [3.44, 5.41] trên 1,929 truy vấn, và các hàng P2 là +5.34 [3.87, 6.82] (Qwen2.5-VL) và +1.61 [0.68, 2.56] (InternVL3). P1 và P2 giữ nguyên như đã đăng ký.

*Ngoài nguồn của bộ nhớ: XM3600 tiếng Việt (Mục 5.2).* XM-a nhận "FAIL", với câu chữ đã đăng ký "The gain was not detected out of domain (XM3600)": điểm ước lượng gộp trên không, nhưng quy tắc đòi KTC trên không và KTC chứa không; độ nhạy trên 2,392 ảnh cho cùng kết cục. Hai hàng báo cáo theo mô hình trái dấu nhau, và không có bước xóa thì hàng InternVL3 là "not detected". XM-b đạt "PASS" theo quy tắc riêng của nó, nhưng dự đoán XM cần cả hai nên là "not confirmed". Bản nháp không khẳng định chuyển giao và không khẳng định truy hồi giữ được độ chính xác đối tượng trên XM3600; các hàng khớp số lượng ở đó, không quy tắc XM nào đọc, là +0.12 [−1.20, 1.49] (Qwen2.5-VL) và +0.13 [−0.83, 1.03] (InternVL3), với cận dưới thứ nhất thấp hơn mức −1.0 dùng trên OpenViIC.

*Đối chứng (Mục 5.3).* Đối chứng S-zf, `ret` − `zs` gộp, được đăng ký với cỡ kỳ vọng khoảng +10.0 và không có nhãn đạt; giá trị quan sát là +14.30 [13.38, 15.24] trên OV-test và +11.99 [10.68, 13.34] trên XM-test2500. Một cách đọc mô tả, hậu nghiệm từ Bảng D.5, không có tương phản đăng ký và không có KTC: ví dụ ngẫu nhiên từ cùng bộ nhớ đã cho điểm cao hơn hẳn zero-shot ở cả hai mô hình trên cả hai tập. Với ví dụ cố định (†), `ret` − `fix` gộp là +3.47 [2.54, 4.41] trên OV-test và +2.53 [1.32, 3.80] trên XM-test2500; ở Qwen2.5-VL là +6.33 [5.02, 7.72] và +5.87 [4.14, 7.65]; ở InternVL3 là +0.61 [−0.68, 1.87] và −0.81 [−2.41, 0.76], hai KTC chứa không. Trên OV-test, `ret` gộp hơn NN-top1 +13.98 [12.63, 15.38] và hơn NN-consensus +9.15 [7.84, 10.47]; tỉ lệ chú thích `ret` gần như chép nguyên văn là 0.015 (Qwen2.5-VL) và 0.002 (InternVL3), nên mô hình không đơn thuần trả lại chú thích của láng giềng. Ở cột PTB, `ret` − `rand` gộp là +4.91 [3.93, 6.00] trên OV-test và +0.60 [−0.54, 1.85] trên XM-test2500, cùng dấu và cùng phạm vi với cột quyết định.

**Nhận xét rà soát.** Mục 5 xác lập chắc một điều: trên OpenViIC test, với hai cặp mô hình–cấu hình đã đóng băng, hiệu gộp `ret` − `rand` vượt cả mức +2.0 lẫn không. Nó không xác lập rằng hiệu ứng có ở cả hai mô hình, và bản nháp nói đúng như vậy bằng câu phạm vi. XM-a "FAIL" được báo cáo thẳng; "không phát hiện" không bị diễn giải thành "không có hiệu ứng". Các điểm cần lưu ý:

- *Cách đọc P2 của InternVL3.* Bản tạp chí (Mục 3.5) nói rõ rằng với phần chú thích `ret` rơi về zero-shot thì ΔP_cm so với `zs` bằng không theo cách dựng. Bản hội nghị in tỉ lệ 0.351 nhưng bỏ câu này, nên +1.57 dễ bị đọc như hiệu ứng trên toàn bộ chú thích.
- *InternVL3 và bước xóa.* Hàng đã đăng ký (+0.66) và hàng phụ không có bước xóa (+3.71, "detected") cho hai hình ảnh khác nhau. Bản tạp chí (Mục 9.2) gọi việc bước xóa xử lý `ret` và `rand` khác nhau là một hạn chế thiết kế của đại lượng ước lượng đã đăng ký; danh sách hạn chế của bản hội nghị không có ý này.
- *Hai hàng trùng điểm ước lượng.* Độ nhạy đã đăng ký của P2 cho Qwen2.5-VL là +5.34 [3.88, 6.87]; hàng hậu nghiệm bỏ 12 truy vấn là +5.34 [3.87, 6.82]. Đây là hai hàng khác nhau; cần giữ nhãn để không bị xem là lỗi chép.
- *XM-b "PASS" với KTC chứa không* là kết quả của quy tắc không kém hơn với sàn −1.0, không phải bằng chứng cải thiện; cụm "under its own rule" nên được giữ.
- *Hai cách gọi.* Tiêu đề mục dùng "in/outside the memory's source", còn câu chữ đã đăng ký dùng "out of domain (XM3600)"; nên có một câu nối.
- *Phần phải kiểm lại.* Chú thích † và hai số đếm của hạn chế về lô giải mã (Mục D.9) lấy từ phần nghiên cứu quy kết của bản tạp chí, vốn còn thay đổi văn bản theo lịch; ghi chú bản nháp yêu cầu kiểm lại Mục 5 và Mục 7 sau 16/11 05:00 UTC (12:00 giờ Việt Nam).

## D.8 So sánh với tiếng Anh (English comparison)

**Nội dung.** Một đăng ký riêng mang thiết kế sang tiếng Anh mà không tinh chỉnh: cấu hình đóng băng của Bảng D.2 và bước xóa, lời nhắc được dịch, ba nhánh `ret`, `rand`, `zs`. Đăng ký này được viết sau khi đã biết các phán quyết tiếng Việt và được ghi nhận trước khi giải mã bất kỳ ảnh tiếng Anh nào; quy tắc P1 được chọn cho NoCaps sau kết quả XM-a. Cột quyết định là CIDEr-D với tách token PTB [@Chen2015COCOCaptions], một thang khác với cột tiếng Việt. Bộ nhớ là dữ liệu huấn luyện COCO [@Lin2014COCO; @Karpathy2015Split], nên COCO Karpathy test nằm trong nguồn của bộ nhớ và NoCaps val [@Agrawal2019NoCaps] nằm ngoài.

**Bảng D.7.** Kết quả tiếng Anh đã đăng ký và được báo cáo: `ret` − `rand`, điểm PTB CIDEr-D (Bảng 7 của bản nháp, Mục 6). Hàng "báo cáo" không có quy tắc đăng ký; ba hàng cuối chia NoCaps val theo nhãn miền của chính bộ dữ liệu (báo cáo, không gác cổng).

| Hàng | COCO Karpathy test (5,000) | NoCaps val (4,500) | NoCaps val, độ nhạy đã đăng ký (3,500) |
|---|---|---|---|
| **`ret` − `rand` gộp** | **+3.08 [2.08, 4.03]** | **+1.73 [0.94, 2.50]** | +1.62 [0.66, 2.52] |
| nhãn | **P1-EN: "PASS"** | **S-NC: "FAIL"** | "FAIL" |
| báo cáo, Qwen2.5-VL | +7.80 [6.40, 9.17] | +2.83 [1.69, 3.98] | – |
| báo cáo, InternVL3 (τ = 0.10) | −1.64 [−2.79, −0.49] | +0.62 [−0.37, 1.62] | – |
| phụ, InternVL3 ở τ = −∞ | −1.05 [−2.22, 0.08], "not detected" | +1.00 [−0.01, 2.01], "not detected" | +1.09 [−0.12, 2.21], "not detected" |
| quy tắc L, chênh độ dài, Qwen2.5-VL / InternVL3 | 0.019 / 0.019, "does not fire" | – | – |
| NoCaps in-domain (417 ảnh) | – | +4.64 [1.85, 7.36] | – |
| NoCaps near-domain (2,670 ảnh) | – | +1.96 [0.85, 2.99] | – |
| NoCaps out-domain (1,413 ảnh) | – | +0.43 [−0.85, 1.73] | – |

P1-EN đạt "PASS" trên COCO Karpathy test và quy tắc L không kích hoạt. Theo mô hình (hàng báo cáo), Qwen2.5-VL dương rõ còn InternVL3 ở τ = 0.10 có KTC nằm hoàn toàn dưới không; không có bước xóa, hàng của nó là "not detected". Hàng hậu nghiệm (không phán quyết): quy tắc tương tự rộng hơn đánh dấu 1 trong 5,000 truy vấn; bỏ truy vấn đó, hiệu gộp là +3.07 [2.08, 4.06] trên 4,999 truy vấn. Ví dụ ngẫu nhiên đã cao hơn xa zero-shot trên COCO: `rand` − `zs` là +29.50 [28.27, 30.79] ở Qwen2.5-VL và +8.13 [7.03, 9.21] ở InternVL3 (hàng báo cáo).

S-NC nhận "FAIL": KTC nằm trên không nhưng điểm ước lượng dưới mức +2.0 đã đăng ký, và độ nhạy đã đăng ký trên 3,500 ảnh cũng là "FAIL". Bản nháp viết: "The claim that the gain transfers to NoCaps is not made". Theo nhãn miền của bộ dữ liệu, điểm ước lượng gộp giảm dần từ ảnh in-domain đến ảnh out-domain; các khoảng chồng nhau và không có phép thử xu hướng nào được đăng ký.

![Hình D.1. `ret` − `rand` trên bốn tập được chấm, theo từng mô hình và gộp, với KTC bootstrap ghép cặp của Mục 4. Hàng gộp là các đại lượng ước lượng đã đăng ký (P1, XM-a, P1-EN, S-NC); hàng theo mô hình là hàng báo cáo, InternVL3 ở τ đóng băng. Ô tiếng Việt dùng CIDEr-D đã tước dấu câu, ô tiếng Anh dùng PTB CIDEr-D; không tính hiệu giữa hai ngôn ngữ. Đường liền: không. Đường đứt: mức +2.0 đã đăng ký, là một đại lượng khác nhau trên mỗi thang.](figs/C_fig1_ret_minus_rand.svg)

*Hai ngôn ngữ đặt cạnh nhau (hậu nghiệm; không phán quyết).* Trong Hình D.1, các dự đoán truy hồi so với ngẫu nhiên đã đăng ký chỉ đạt ở nơi bộ nhớ và tập kiểm thử cùng nguồn. Nguồn bộ nhớ và tập kiểm thử thay đổi cùng nhau, và các hàng ngoài nguồn của Qwen2.5-VL vẫn trên không, nên theo bản nháp đây là "an observation and not a tested cause".

**Nhận xét rà soát.** Mục 6 cho thấy mẫu hình tiếng Việt lặp lại ở tiếng Anh dưới cấu hình chọn ở ngôn ngữ khác, và báo cáo S-NC "FAIL" cùng độ nhạy "FAIL" không né tránh. Các điểm phản biện dễ hỏi:

- *Số gộp P1-EN che hai hàng trái dấu.* "PASS" gộp (+3.08) là trung bình của +7.80 và −1.64. Bản nháp nêu hàng âm ở tóm tắt, giới thiệu và kết luận; các rào này phải được giữ khi viết lại.
- *Mức +2.0 trên thang PTB.* Mục 7 chỉ ghi mức này được mang sang "without recalibration". Bản tạp chí (Mục 5.4 và Mục 8.1) nói thêm chiều của hệ quả: do điểm tiếng Anh cao hơn, cùng mức +2.0 tương đối dễ đạt hơn trên COCO. Nên thêm chiều này vì nó ảnh hưởng đến cách đọc P1-EN "PASS".
- *Quy tắc của S-NC được chọn sau XM-a.* Bản nháp công bố điều này. Bản tạp chí (Mục 8.3) nói thêm rằng theo quy tắc XM-a thì S-NC đã đạt; bản hội nghị chỉ ghi quy tắc P1 "is stricter". Giữ hay bỏ câu phản thực này là lựa chọn của nhà nghiên cứu, nhưng phản biện có thể tự suy ra.
- *Hình 1* đang trỏ tới tệp hình của bản tạp chí; kế hoạch yêu cầu dựng lại dạng vectơ từ bảng khóa số liệu. Trang hội nghị yêu cầu tránh hình do AI sinh ra; hình này là biểu đồ vẽ bằng mã từ số liệu.
- *Không có dự đoán về độ chính xác đối tượng ở tiếng Anh* (nêu ở Mục 7), nên kết luận "không thấy cái giá về độ chính xác" chỉ áp dụng cho OpenViIC test.

## D.9 Công bố và hạn chế (Disclosures and limitations)

**Nội dung.** Mục 7 mở bằng câu: "None of the following changed a configuration, threshold, metric, set or rule after a test output existed". Mười hai công bố là: (1) tập chính OpenViIC bỏ 60 ảnh theo bộ lọc định trước, tập đầy đủ in bên cạnh; (2) để ghim danh sách, các tập lệnh CPU đã đọc byte ảnh kiểm thử, khóa chú giải và số tham chiếu, không dùng chú thích và không tính đầu ra mô hình nào; một nghiên cứu khác đã giải mã zero-shot một số ảnh XM-dev500 (chỉ liên quan giai đoạn B); (3) nhánh tiếng Anh được quyết định trong ngày kiểm thử tiếng Việt và đăng ký sau khi biết các phán quyết tiếng Việt, trước mọi giải mã tiếng Anh; quy tắc cho NoCaps được cố định sau khi biết XM-a và chặt hơn quy tắc XM-a, nên hai kết quả ngoài nguồn trả lời hai quy tắc khác nhau; (4) mức +2.0 được mang sang tiếng Anh nguyên giá trị, không hiệu chỉnh lại cho thang PTB; (5) bước xóa tiếng Anh là một bản chuyển với bộ khớp đối tượng khác, chưa kiểm tra hiệu chỉnh, vì thế mọi hàng τ = −∞ đều được in; (6) ảnh NoCaps được tải theo mã Open Images nên byte hoặc độ phân giải có thể khác; (7) tóm tắt và phần đóng góp trích hàng COCO của InternVL3 như một hàng báo cáo, vì đăng ký tiếng Anh không cấm và riêng số gộp sẽ nói quá hiệu ứng; (8) các hàng hậu nghiệm có nhãn và không có phán quyết; (9) một chẩn đoán lọc thăm dò của cùng dự án về sau dùng lại ảnh kiểm thử trong vai trò phát triển, chỉ tạo ra hàng thăm dò; (10) các sai lệch vận hành của lượt kiểm thử (kiểm tra tương đương lặp lại, bản mã ghim tại thời điểm kiểm thử, quy tắc thử lại cho tệp ảnh bị cắt cụt) không đổi cấu hình, ngưỡng, tập hay quy tắc nào; (11) bốn phân tích phụ đã đăng ký không báo cáo ở đây (liều–đáp ứng theo cosine, báo cáo văn phong, tỉ lệ nguồn của ví dụ được hiện, độ chính xác đối tượng neighbour-only); (12) bốn đăng ký về sau không báo cáo ở đây (so sánh đường cơ sở trên Flickr30K, các phép cắt bỏ trên tập phát triển, phân tích quy kết trên tập phát triển, và chẩn đoán lọc thăm dò đã kết thúc theo quy tắc dừng đã đăng ký).

Bảy hạn chế là: (1) chỉ có hai mô hình nền, mức tăng chủ yếu ở một mô hình và nghiên cứu không nói được thuộc tính nào của mô hình dự báo nó; (2) ngoài nguồn của bộ nhớ cả hai dự đoán đã đăng ký thất bại, và sự khớp nguồn bị lẫn với tập kiểm thử; (3) CIDEr-D thưởng cho câu chữ của tham chiếu và nghiên cứu không có đánh giá của người; (4) trên OpenViIC nhãn vàng là hợp của các tham chiếu, nên một đối tượng đúng mà không tham chiếu nào nêu bị tính là lỗi; trên XM3600 nhãn đã kiểm chứng chỉ phủ các lớp được ánh xạ; không có dự đoán về độ chính xác đối tượng ở tiếng Anh; (5) mỗi tập kiểm thử được giải mã một lần, tham lam, với một lần rút `rand` cho mỗi ảnh; (6) kết quả là kết quả của hệ thống như đã chạy, theo lô cố định: kiểm tra trước phép thử giải mã lại cùng ảnh phát triển trong cùng lô cho 52/52 chú thích giống hệt ở mỗi mô hình và chỉ chứng tỏ tính tương đương giữa các lần chạy; một kiểm tra về sau (trên tập phát triển, không xác nhận) giải mã 50 mục từng ảnh một cho 42/50 chú thích giống hệt ở Qwen2.5-VL và 37/50 ở InternVL3, dựa trên so khớp chuỗi, không so điểm; (7) dữ liệu huấn luyện của các mô hình nền không được công bố đầy đủ [@Bai2025Qwen25VL; @Zhu2025InternVL3; @Chen2024InternVL25], dữ liệu COCO hoặc Open Images có thể đã được thấy; đối chứng `rand` cùng k loại nhiễm bẩn chung của `ret` và `rand`, không loại nhiễm bẩn tương tác với truy hồi. Về tính toán, phép thử tiếng Việt dùng 9.59 giờ GPU trên trần 20 giờ và phép thử tiếng Anh 13.22 trên trần 25 giờ, mỗi phép thử trên một GPU 24 GB.

**Nhận xét rà soát.** Mục này là điểm mạnh của bản nháp: mọi thất bại và mọi lựa chọn đưa ra sau khi biết kết quả đều được gọi tên, và hai công bố cuối tránh việc im lặng bỏ qua các nghiên cứu sẽ xuất hiện trong bản tạp chí. So với bản tạp chí có bốn chỗ hổng. (a) *Tiếp xúc trước với các tập tiếng Anh:* bản tạp chí (Mục 8.5) nêu một nghiên cứu đồng hành đã chấm điểm trên Karpathy test, một lượt giải mã zero-shot trước đó trên 295 ảnh Karpathy test và 1,000 ảnh NoCaps của một nghiên cứu khác, đồng thời ghi rằng không đầu ra nào trong số đó được dùng lại. Bản hội nghị chỉ giữ phần NoCaps, dưới dạng lý do của độ nhạy 3,500 ảnh; phần COCO vắng mặt, dù COCO Karpathy test là tập của dự đoán chính P1-EN. (b) Mối đe dọa từ bước xóa đối với tính hợp lệ nội tại (Mục D.7) không có trong danh sách. (c) Bản tạp chí (Mục 9.3) nói một lượt chạy lại chính xác cần cùng các lát lô; bản hội nghị nêu hạn chế về lô nhưng không nêu hệ quả này. (d) Câu của bản tạp chí (Mục 9.2) rằng nhánh tiếng Anh là một phép thử chuyển giao thận trọng, không ước lượng thiết lập tiếng Anh tốt nhất, đã bị bỏ. Mục này đã vượt ngân sách 69 từ (609 so với 540), nên mọi bổ sung phải đi kèm cắt giảm ở chỗ khác.

## D.10 Kết luận (Conclusion)

**Nội dung.** Mục 8 gồm ba đoạn. Đoạn một nhắc kết quả trong nguồn của bộ nhớ ở hai ngôn ngữ với số, nhãn và rào của Bảng D.6 và Bảng D.7 (P1 "PASS" kèm câu phạm vi; P1-EN "PASS" kèm ghi chú hàng báo cáo của InternVL3 dưới không; P2 "PASS"). Đoạn hai nêu thất bại ngoài nguồn: XM-a "FAIL" và dự đoán XM "not confirmed"; S-NC "FAIL", kèm ghi chú "the registered sensitivity also fails"; "No transfer claim is made". Đoạn ba nêu `ret` − `zs` là +14.30 [13.38, 15.24] trên OpenViIC test và, một cách mô tả, ví dụ ngẫu nhiên trong miền đã cao hơn hẳn zero-shot; vì vậy muốn quy mức tăng cho truy hồi thì cần đối chứng ví dụ ngẫu nhiên cùng k từ cùng bộ nhớ, kết quả cho từng mô hình nền, và việc kiểm tra xem chú thích của bộ nhớ có cùng nguồn với tập đích hay không. Câu cuối giữ rào: các dự đoán chỉ đạt ở nơi cùng nguồn, nhưng nguồn và tập kiểm thử thay đổi cùng nhau và các hàng ngoài nguồn của Qwen2.5-VL vẫn trên không, nên đây là "an observation, not a tested cause".

**Nhận xét rà soát.** Kết luận không thêm khẳng định mới và lặp lại đủ các kết quả "FAIL" với ước lượng, khoảng và quy tắc. Nó dài 229 từ so với ngân sách 160 từ; phần vượt đến từ chính các rào và nhãn bắt buộc, nên nếu cần cắt thì nên cắt ở mục khác. Điều kiện thứ ba của lời khuyên dựa trên một cách đọc hậu nghiệm; câu rào đi kèm phải được giữ nguyên khi viết lại.

## D.11 Các tuyên bố cuối bài và tài liệu tham khảo

**Nội dung.** *Ethics and data statement:* nghiên cứu chỉ dùng các bộ dữ liệu công khai sẵn có với tham chiếu và nhãn đã phát hành; không gán nhãn mới, không có người tham gia; chú thích được đọc lúc chạy, chỉ đặt trong lời nhắc và không được phân phối lại. Các bộ dữ liệu được liệt kê dạng ngắn với ngôn ngữ và vai trò: KTVIC (bộ nhớ, giai đoạn A), UIT-OpenViIC (bộ nhớ, phát triển, kiểm thử), XM3600 (tham chiếu tiếng Việt; phát triển, kiểm thử), COCO với phần chia Karpathy (bộ nhớ, kiểm thử), NoCaps val (kiểm thử) và nhãn Open Images do người kiểm chứng (nhãn vàng đối tượng cho XM-b). *Data and code availability:* các bản đăng ký với danh sách đã ghim, mã kiểm thử, tệp quyết định, điểm số, mã ảnh và giá trị băm "are available from the authors on request"; không phát hành chú thích của bộ dữ liệu, chú thích của mô hình hay bản ghi theo từng ảnh. Dòng tác giả, câu về sự đồng ý của tác giả KTVIC và UIT-OpenViIC, giấy phép của từng bộ dữ liệu, lời cảm ơn và tài trợ, tuyên bố về lợi ích đều đang là ô giữ chỗ. Danh mục tài liệu sẽ được dựng theo kiểu đánh số của LNCS; bản nháp dùng 34 khóa trong 67 mục của tệp tài liệu tham khảo của Bài báo C.

**Nhận xét rà soát.** (a) Bản tạp chí (Mục 10) viết rằng tác giả của UIT-OpenViIC và KTVIC đã đồng ý cho dùng dữ liệu; kế hoạch viết ghi rằng chưa có xác nhận bằng văn bản nào được lưu, nên bản hội nghị để câu này cho nhà nghiên cứu xác nhận hoặc bỏ. Câu của bản tạp chí cần được xử lý nhất quán. (b) Hai bản nói khác nhau về công bố: bản tạp chí hứa phát hành khi xuất bản, bản hội nghị ghi "on request" (quyết định D9). (c) Các ô giữ chỗ và khối chú thích ở đầu tệp bản nháp phải được điền hoặc gỡ trước khi nộp. (d) Việc có cần mục đạo đức và tuyên bố lợi ích hay không là thông lệ của bộ mẫu LNCS mà báo cáo khảo sát chưa xác nhận.

## D.12 So sánh với bản tạp chí

Theo kế hoạch, văn xuôi của nghiên cứu chính phải giảm từ khoảng 12,500 xuống khoảng 4,100 từ (khoảng 67%), và ô bảng từ khoảng 3,000 xuống khoảng 1,000. Bảng D.8 đối chiếu từng mục theo bảng nguồn từng đoạn của bản nháp.

**Bảng D.8.** Bản hội nghị so với bản tạp chí, theo từng mục.

| Mục của bản hội nghị | Nguồn trong bản tạp chí | Trạng thái | Giữ, rút gọn, bỏ |
|---|---|---|---|
| Tên bài, từ khóa, dòng tác giả | – | mới | tên khác tên bản tạp chí |
| Tóm tắt | Tóm tắt | viết lại | bỏ câu Flickr30K; thêm quy tắc của hai kết quả "FAIL" và P2 bằng lời |
| 1 Introduction | Mục 1 | rút gọn | ba đóng góp thay cho năm (bỏ đóng góp Flickr30K và "A full record"); bốn tập kiểm thử thay cho năm |
| 2 Related work, Bảng 1 | Mục 2, Bảng 1b | rút gọn mạnh | từ khoảng 2,100 xuống khoảng 330 từ; bỏ danh mục bài phương pháp và Bảng 1 đầy đủ |
| 3 Method, Bảng 2 | Mục 3.1–3.6; "Instrument definitions" của phụ lục; Mục 6.7 | rút gọn; một phần đưa từ phụ lục vào | định nghĩa ΔP_cm in trong thân bài; kết quả H_G chuyển về đây; bỏ Mục 3.7 và Mục 3.8 |
| 4 Data and registered plan, Bảng 3 và 4 | Mục 4; Mục 5.1, 5.2, 5.4; Mục 8.1 | rút gọn, gộp | Bảng 4 gộp Bảng 4 và Bảng 10; Bảng 3 bỏ hàng Flickr30K, thêm tập tiếng Anh; ánh xạ câu phạm vi còn một câu; bỏ Box 1, đoạn lực kiểm định, Mục 5.7 |
| 5 Results in Vietnamese, Bảng 5 và 6 | Mục 6.1–6.7 | rút gọn, gộp | Bảng 6 gộp Bảng 7, 8, 9; Bảng 5 thêm hàng tiếng Anh; bỏ liều–đáp ứng, văn phong, độ chính xác neighbour-only; bỏ Mục 6.8, 6.9, 6.10 |
| 6 English comparison, Bảng 7, Hình 1 | Mục 8.1–8.4 | rút gọn, gộp | Bảng 7 gộp Bảng 11 và 12; phần đọc hai ngôn ngữ còn hai câu; bỏ Mục 8.6 (Flickr30K) và Mục 8.7 |
| 7 Disclosures and limitations | Mục 7 (Box 2), Mục 8.5, Mục 9.1, Mục 6.11 | rút gọn thành danh sách | hai công bố cuối là mới; bỏ Mục 7.5, 9.2, 9.3 |
| 8 Conclusion | Mục 10 | rút gọn | bỏ đoạn Flickr30K và câu về bước xóa trên tập phát triển |
| Tuyên bố cuối bài | Mục 4, Mục 10 | phần lớn mới | "on request" thay cho phát hành khi xuất bản |
| Phụ lục | Bảng S1–S27 | bỏ | 16 bảng là chi tiết của nghiên cứu chính, 11 bảng thuộc các nghiên cứu không báo cáo |

Hai nội dung đi theo chiều ngược lại, từ phần chỉ dành cho tạp chí sang bản hội nghị: chú thích † của hàng `fix` và hạn chế về lô giải mã với hai số đếm 42/50 và 37/50.

## D.13 Giới hạn của hội nghị và số đo hiện tại

Số trang chưa được đo vì chưa dựng bản LNCS; các số đo dưới đây là số từ, lấy từ tệp số đo của bản nháp. Kế hoạch ước tổng cộng khoảng 13.8 trang ở ngân sách khoảng 4,100 từ văn bản chạy, với giả định khoảng 450 từ mỗi trang và giả định tài liệu tham khảo có tính vào số trang; cả hai giả định đều chưa được kiểm.

**Bảng D.9.** Giới hạn của hội nghị hoặc ngân sách của kế hoạch so với số đo của bản nháp; nửa dưới là số từ văn bản chạy theo mục.

| Hạng mục | Giới hạn hoặc ngân sách | Số đo | Chênh hoặc đánh giá |
|---|---|---|---|
| Số trang, bài đầy đủ | tối thiểu 12, tối đa 15 (trang hội nghị) | chưa đo | chưa kết luận được |
| Tên bài | không nêu giới hạn | 14 từ | – |
| Từ khóa | không có trong báo cáo khảo sát | 5 | phải đọc lại |
| Bảng và hình | – | 7 bảng (ô bảng 836 từ so với dự kiến khoảng 1,000; chú thích 312 từ), 1 hình | – |
| Tóm tắt | thông lệ LNCS 150–250 từ (chưa xác nhận); ngân sách 200 | 233 | +33 |
| §1 | 500 | 509 | +9 |
| §2 | 330 | 333 | +3 |
| §3 | 620 | 680 | +60 |
| §4 | 560 | 563 | +3 |
| §5 | 700 | 713 | +13 |
| §6 | 380 | 385 | +5 |
| §7 | 540 | 609 | +69 |
| §8 | 160 | 229 | +69 |
| Tuyên bố cuối bài | 110 | 202 | +92 |
| **Tổng văn bản chạy** | **4100** | **4456** | **+356** (khoảng 9%) |

Mọi mục đều vượt ngân sách; phần vượt lớn nhất nằm ở các tuyên bố cuối bài, Mục 7, Mục 8 và Mục 3, tức ở chính những chỗ chứa công bố, rào và định nghĩa bắt buộc. Nếu bản PDF vượt 15 trang, kế hoạch quy định thứ tự cắt: (1) các hàng tiếng Anh của Bảng 5; (2) Bảng 1, thay bằng hai câu; (3) hàng `rand` − `zs` trên COCO; (4) cột PTB; (5) đường cơ sở sao chép, rút còn một mệnh đề. Các kết quả âm đã đăng ký không bao giờ bị cắt; nếu bản PDF dưới 12 trang thì khôi phục chi tiết từ bản tạp chí. Tệp số đo ghi các kiểm tra khác đều đạt: mọi con số có khóa trong bảng khóa số liệu (445 số, 0 số không có hàng), đủ 24 câu bắt buộc về kết quả âm và nhãn đã đăng ký, và mọi khóa trích dẫn có trong tệp tài liệu tham khảo. Các giới hạn chưa được báo cáo khảo sát xác nhận và phải đọc lại trước khi nộp gồm: độ dài tóm tắt, số từ khóa, cách tính trang cho tài liệu tham khảo, các tuyên bố bắt buộc, kiểu trích dẫn, khả năng nộp phụ lục, định dạng hình và quy tắc rút bài.

## D.14 Quyết định còn chờ nhà nghiên cứu

Bảng D.10 gom mọi quyết định mà kế hoạch viết và ghi chú bản nháp để lại cho nhà nghiên cứu. Các mốc của kế hoạch tính theo giờ Việt Nam, trừ khi ghi AoE.

**Bảng D.10.** Quyết định còn chờ, phương án, khuyến nghị của tài liệu và thời hạn.

| Nhãn | Quyết định | Phương án | Khuyến nghị; mặc định nếu không trả lời | Cần trước |
|---|---|---|---|---|
| D1 | Danh sách và thứ tự tác giả, tác giả liên hệ, đơn vị | do nhà nghiên cứu cung cấp; không đổi được sau khi tệp đã gửi nhà xuất bản | không có mặc định; thiếu thì không nộp được | 1/12 (giờ Việt Nam) |
| D2 | Phạm vi | S1 (nghiên cứu chính cô đọng) hoặc S2 (chỉ nghiên cứu quy kết) | S1; mặc định S1 | 14–15/11 (giờ Việt Nam) |
| D3 | Loại bài | bài đầy đủ, mục tiêu 14 trang; hoặc bài ngắn khoảng 8 trang (khoảng 2,300 từ, ba bảng, không hình) | bài đầy đủ | 14–15/11 (giờ Việt Nam) |
| D4 | Đợt nộp | đợt hai (21/11 18:59 giờ Việt Nam) hoặc đợt ba (2/12 AoE, tức 3/12 18:59 giờ Việt Nam) | đợt ba; đợt hai để lại chưa đầy một ngày cho việc viết lại | 14–15/11 (giờ Việt Nam) |
| D5 | Dự trực tiếp hay trực tuyến | trực tuyến USD 155 (sinh viên USD 130); trực tiếp USD 380 hoặc USD 320 cộng chi phí đi Kyoto | trực tuyến | 10/1/2027 |
| D6 | Có nộp khi trang của nhà xuất bản chưa liệt kê tập kỷ yếu | D6a: cho phép hỏi ngay biên tập viên của chuỗi hoặc trường chủ nhà. D6b: chỉ nộp ngày 2/12 nếu quy tắc rút bài đã được đọc hoặc trả lời. D6c: nếu được rút bài, điểm quyết định thật đặt trước bước bản in cuối (10/1/2027); không có xác nhận thì rút và gửi bản đầy đủ cho tạp chí. D6d: nếu không được rút hoặc không rõ, lần nộp là điểm không quay lại | khuyến nghị D6a; mặc định: chuẩn bị bài đến trạng thái sẵn sàng, không nộp và không ai viết cho nhà xuất bản hay trường khi chưa có sự đồng ý | 1/12 (giờ Việt Nam) |
| D7 | Thời điểm và khung của bản tạp chí | nộp tạp chí sau kết quả hội nghị (10/12 hoặc 25/12), trích bản hội nghị, viết lại tóm tắt quanh phần mở rộng | như bên; đọc chính sách công bố trước của ACM trước khi nộp hội nghị | 1/12 (giờ Việt Nam) |
| D8 | In định nghĩa độ chính xác khớp số lượng trước bài gốc của nó | (a) bài về độ chính xác đối tượng (Phần A) được nộp hoặc đăng trước và bản này trích nó; (b) chấp nhận bằng văn bản cái giá đối với bài đó, vì kỷ yếu sẽ là nơi in công cụ lần đầu | chọn (a) hoặc (b); mặc định: giữ định nghĩa có ghi nguồn, không nộp khi chưa có câu trả lời | trước khi nộp (2/12) |
| D9 | Công bố bản đăng ký, tệp quyết định và mã | kho công khai có DOI, hoặc cung cấp theo yêu cầu | kho có DOI; hiện chưa có bản lưu ký nào; mặc định ghi "available from the authors on request" | 10/1/2027 |
| D10 | Dạng bản nháp bàn giao | bản đầy đủ bỏ qua giới hạn độ dài, hoặc bản theo ngân sách trang kèm bảng nguồn từng đoạn | bản theo ngân sách trang (đã làm) | – |
| D11 | Tên bài | tên tạm hoặc tên do nhà nghiên cứu đặt; bản tạp chí giữ tên hiện tại | như bên | trước khi nộp |
| D12 | Bước đối chiếu chất lượng | chấm theo thang tiêu chí so với ba đến năm bài CCIS gần đây về AI ứng dụng hoặc NLP; hoặc bỏ bước này | giữ; bỏ thì cần sự đồng ý | 21/11 (giờ Việt Nam, theo lịch lùi của kế hoạch) |
| – | Các ô giữ chỗ | giấy phép của từng bộ dữ liệu; câu về sự đồng ý của tác giả KTVIC và UIT-OpenViIC (xác nhận hoặc bỏ); lời cảm ơn và tài trợ; tuyên bố lợi ích | không có mặc định | trước khi nộp |
| – | In các mốc thời gian của đăng ký và quyết định | in hoặc không in | cần sự đồng ý của nhà nghiên cứu | trước khi nộp |
| – | Khai báo theo chính sách hiện hành của nhà xuất bản về công cụ hỗ trợ viết | do nhà nghiên cứu quyết định | đọc lại trang chính sách; không khai sai | ngày nộp |

Lịch lùi của kế hoạch cho đợt ba (giờ Việt Nam) đặt việc viết lại của nhà nghiên cứu vào 21–30/11, việc kiểm lại văn bản đã viết lại vào 30/11–1/12 và việc nộp vào 2/12, còn dư thời gian đến 3/12 18:59. Kế hoạch nêu năm rủi ro mà các quyết định trên phải cân: hội nghị kỳ đầu; khẳng định về nhà xuất bản chưa kiểm chứng; hệ quả đối với bản tạp chí; thời gian viết lại ngắn; và việc in công cụ của một bài khác trước bài đó.

## D.15 Bảng đối chiếu khẳng định – bằng chứng

Khóa được ghi theo dạng tên tệp và khóa; đường dẫn đầy đủ nằm trong `number_manifest_TAIMMA.tsv`. Trạng thái "REGISTERED (nhãn)" là hàng đã đăng ký mà quy tắc trả về một nhãn khác PASS và FAIL; nhãn được in nguyên văn.

**Bảng D.11.** Khẳng định của tóm tắt, giới thiệu và kết luận, đối chiếu với bằng chứng.

| # | Khẳng định | Trạng thái | Mục của bản nháp | Bảng, hình | Số chính | Khóa |
|---|---|---|---|---|---|---|
| 1 | Trên OpenViIC test, `ret` hơn `rand` (gộp) | REGISTERED PASS | Tóm tắt, §1, §5.1, §8 | Bảng D.6, Hình D.1 | +4.49 [3.52, 5.57] | `decide_ov.json::P1` |
| 2 | Mức tăng "carried mainly by Qwen2.5-VL; not detected for InternVL3" | REGISTERED (nhãn) | Tóm tắt, §1, §5.1, §8 | Bảng D.6 | +8.33 [7.01, 9.76]; +0.66 [−0.68, 1.99] | `decide_ov.json::scope.sentence`; `decide_ov.json::P1b.qwen25vl_7b`; `decide_ov.json::P1b.internvl3_8b` |
| 3 | Độ chính xác khớp số lượng so với `zs` ở trên sàn cho cả hai mô hình | REGISTERED PASS | Tóm tắt, §1, §5.1, §8 | Bảng D.6 | +5.41 [3.88, 7.01]; +1.57 [0.65, 2.51] | `decide_ov.json::P2.qwen25vl_7b`; `decide_ov.json::P2.internvl3_8b` |
| 4 | Trên XM3600 tiếng Việt, mức tăng không được phát hiện | REGISTERED FAIL | Tóm tắt, §1, §5.2, §8 | Bảng D.6, Hình D.1 | +0.70 [−0.45, 1.97] | `decide_xm_m3.json::XM_a` |
| 5 | Dự đoán XM "not confirmed" | REGISTERED (nhãn) | §5.2, §8 | Bảng D.6 | – | `decide_xmb.json::XM_prediction` |
| 6 | Trên COCO Karpathy test, `ret` hơn `rand` (gộp) | REGISTERED PASS | Tóm tắt, §1, §6, §8 | Bảng D.7, Hình D.1 | +3.08 [2.08, 4.03] | `decide_coco_test.json::P1_EN` |
| 7 | Hàng InternVL3 trên COCO dưới không | DESCRIPTIVE (hàng báo cáo) | Tóm tắt, §1, §6, §8 | Bảng D.7 | −1.64 [−2.79, −0.49] | `decide_coco_test.json::scored.coco_test_5000.per_model.internvl3_8b.ret_minus_rand` |
| 8 | Trên NoCaps val, điểm ước lượng dưới +2.0; độ nhạy cũng thất bại | REGISTERED FAIL | Tóm tắt, §1, §6, §8 | Bảng D.7, Hình D.1 | +1.73 [0.94, 2.50]; +1.62 [0.66, 2.52] | `decide_nocaps_val.json::S_NC`; `decide_nocaps_val.json::S_NC_sensitivity_3500` |
| 9 | Không có khẳng định chuyển giao | REGISTERED (nhãn "not made" cho NoCaps) | Tóm tắt, §1, §6, §8 | – | – | `decide_nocaps_val.json::claim_transfers_to_nocaps` |
| 10 | `ret` − `zs` trên OpenViIC test | REGISTERED (đối chứng, không có nhãn đạt) | §5.3, §8 | – | +14.30 [13.38, 15.24] | `decide_ov.json::S_zf.pooled_vs_zs` |
| 11 | Ví dụ ngẫu nhiên trong miền đã cao hơn hẳn zero-shot | POST HOC (đọc mô tả, không KTC) | §5.3, §8 | Bảng D.5 | – | – |
| 12 | Dự đoán chỉ đạt ở nơi bộ nhớ và tập kiểm thử cùng nguồn; "an observation, not a tested cause" | POST HOC | §6, §7, §8 | Hình D.1 | – | – |
| 13 | Thiết kế đánh giá có đăng ký, một lần nhìn cho mỗi tập | DESCRIPTIVE | §1, §3, §4 | Bảng D.2, Bảng D.4 | – | – |
| 14 | Cần đối chứng ngẫu nhiên cùng k, kết quả theo từng mô hình và xét nguồn của bộ nhớ | DESCRIPTIVE (lời khuyên, không phải khẳng định đã kiểm định) | Tóm tắt, §8 | – | – | – |
| 15 | Đường cơ sở tinh chỉnh đã công bố trên OpenViIC test | DESCRIPTIVE (số đã công bố, không so sánh được) | §1 | – | 75.58 | `arXiv:2305.04166::Tab.II p.6 OpenViIC test MDSANet CIDEr 75.5796` |
| 16 | Theo lời chính các bài phân tích trước, không bài nào đăng ký trước, có KTC hay gồm tiếng Việt | DESCRIPTIVE (nhận định về tài liệu, có rào) | §1, §2 | Bảng 1 của bản nháp | – | – |

## D.16 Danh mục việc cần rà soát và hoàn thiện

**Lỗi hoặc mâu thuẫn cần sửa**

1. *Mục 3:* H_G mang nhãn "not passed" trong khi KTC in ra nằm trên không và quy tắc không được nêu. Thêm một mệnh đề nêu quy tắc đã đăng ký của H_G.
2. *Mục 7, công bố về tiếp xúc trước:* thiếu tiếp xúc trước với COCO Karpathy test mà bản tạp chí (Mục 8.5) có nêu. Thêm một mệnh đề.
3. *Mục 5.1, P2 của InternVL3:* khôi phục ý rằng phần chú thích rơi về zero-shot có ΔP_cm bằng không theo cách dựng.
4. *Bảng 3:* điền số ảnh của KTVIC dev299 như Bảng 3 của bản tạp chí.
5. *Các tuyên bố cuối bài và đầu tệp:* điền hoặc gỡ mọi ô giữ chỗ; xử lý nhất quán ở cả hai bản câu về sự đồng ý của tác giả bộ dữ liệu và cách công bố dữ liệu, mã.
6. *Bảng 1 và Bảng 2:* thêm tên ngắn cho cột đầu của Bảng 1 và đọc lại từng ô "no" trên bài gốc; thêm tài liệu tham khảo cho bộ kiểm chứng.
7. *Độ dài:* dựng bản LNCS để đo số trang; văn bản chạy đang vượt ngân sách 356 từ; áp dụng thứ tự cắt của kế hoạch nếu vượt 15 trang.

**Điểm nên làm rõ**

8. *Bảng 4 và Bảng 7:* nói rõ quy tắc L có áp dụng cho S-NC hay không, nêu đơn vị độ dài, và liệt kê các phân tích phụ đã đăng ký có báo cáo ở Mục 5.3.
9. *Mục 3:* thống nhất ký hiệu mẫu số của ΔP_cm giữa hai bản; giữ một câu về quy tắc chọn cấu hình ở giai đoạn A.
10. *Mục 7:* nêu chiều của việc không hiệu chỉnh mức +2.0 trên thang PTB; thêm mối đe dọa từ bước xóa và hệ quả của lô giải mã đối với việc chạy lại.
11. *Mục 5:* nối hai cách gọi "memory's source" và "out of domain"; giữ nhãn cho hai hàng cùng điểm ước lượng +5.34.
12. *Tên bài và Hình 1:* cân nhắc để tên phản ánh cả nhánh tiếng Anh; dựng lại hình dạng vectơ từ bảng khóa số liệu.
13. *Mục 5 và Mục 7:* kiểm lại chú thích † và hai số đếm về lô sau 16/11 05:00 UTC (12:00 giờ Việt Nam).
14. *Trước khi nộp:* đọc lại các giới hạn chưa kiểm chứng của hội nghị (Mục D.13) và chính sách công bố trước của ACM; tự kiểm tra trùng lặp với bài hội nghị trước của nhóm.

**Câu hỏi phản biện có thể gặp**

15. Bản đăng ký và các mốc thời gian được công khai ở đâu, khi dữ liệu và mã chỉ "on request"?
16. Số gộp có ý nghĩa gì khi một mô hình không cho thấy hiệu ứng (OpenViIC) hoặc cho hàng âm (COCO)?
17. Kết quả "không phát hiện" của InternVL3 có phải là hệ quả của bước xóa, trong khi giả thuyết bảo vệ đã không đạt?
18. Vì sao hai tập ngoài nguồn dùng hai quy tắc khác nhau, và phép thử XM-a có đủ nhạy không?
19. Đối chứng ngẫu nhiên cùng k và kết quả COCO đã có trong tài liệu; phần mới thực sự là gì?
20. Mức tăng CIDEr-D có phải chỉ là bắt chước câu chữ của tham chiếu, khi không có đánh giá của người?
21. Bản tạp chí sau này khác bản này ở đâu, khi lõi xác nhận đã được in?

## D.17 Thuật ngữ và ký hiệu

Các thuật ngữ dùng chung với bản tạp chí được giải thích đầy đủ trong bảng thuật ngữ của Phần C; bảng dưới đây chỉ nhắc những thuật ngữ cần để đọc phần này.

**Bảng D.12.** Thuật ngữ và ký hiệu của bản hội nghị.

| Thuật ngữ, ký hiệu | Tiếng Việt dùng ở đây | Nghĩa |
|---|---|---|
| retrieval in-context captioning | sinh chú thích theo ngữ cảnh có truy hồi | đặt chú thích của các ảnh bộ nhớ tương tự vào lời nhắc |
| memory; cluster | bộ nhớ; cụm | kho ảnh có chú thích dùng để truy hồi; nhóm ảnh gần trùng |
| `ret`, `rand`, `fix`, `zs` | nhánh (giữ tên gốc) | ví dụ truy hồi; ngẫu nhiên cùng k, cùng bộ nhớ; một bộ cố định; không ví dụ |
| backbone; frozen configuration | mô hình nền; cấu hình đóng băng | Qwen2.5-VL-7B-Instruct và InternVL3-8B; k, thứ tự, đuôi lời nhắc và τ chọn ở giai đoạn A |
| deletion step; τ | bước xóa; ngưỡng xóa | bỏ phần chú thích nêu lớp bị bộ kiểm chứng loại; τ = −∞ là không xóa |
| stripped CIDEr-D | CIDEr-D đã tước dấu câu | CIDEr-D sau khi bỏ token dấu câu ở cuối; cột quyết định tiếng Việt |
| ΔP_cm | thay đổi độ chính xác đối tượng khớp số lượng | công thức (D.2); so với chú thích zero-shot của cùng mô hình |
| Δ_m,i; Δ_i | hiệu theo mô hình; hiệu gộp | công thức (D.3) |
| SESOI | cỡ hiệu ứng nhỏ nhất đáng quan tâm | +2.0 điểm |
| CI | khoảng tin cậy (KTC) | bootstrap ghép cặp theo ảnh, phân vị 95% |
| scope sentence | câu phạm vi | câu đã đăng ký đi kèm mọi số gộp P1 |
| registered sensitivity; reported row | độ nhạy đã đăng ký; hàng báo cáo | cùng phân tích trên tập thay thế; hàng không có quy tắc đăng ký |
| "detected", "not detected" | nhãn của hàng phụ | cận dưới KTC trên không hay không; không phải phán quyết |
| in, outside the memory's source | trong, ngoài nguồn của bộ nhớ | tập kiểm thử cùng hay khác bộ dữ liệu gốc của bộ nhớ |
| H_G; rule L | giả thuyết bảo vệ; quy tắc L | giả thuyết của giai đoạn B về bước xóa; kiểm tra chênh lệch độ dài chú thích |
| AoE | Anywhere on Earth | múi giờ UTC−12 dùng cho các hạn của hội nghị |
