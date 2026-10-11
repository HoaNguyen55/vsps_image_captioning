# R2-05: Ngữ pháp danh ngữ tiếng Việt như một tín hiệu mô hình hoá (vai: nhà ngôn ngữ học)

**Tóm tắt 5 dòng**
1. Danh ngữ tiếng Việt có khuôn cố định [Lượng][Loại từ][Danh từ đầu][Định ngữ][Tính từ] và là ngôn ngữ head-initial. Vì vậy bỏ bớt phần bên phải, hoặc thay một ô bằng giá trị trung tính (bare / `người` / `xanh` / `một vài`), luôn cho ra một mệnh đề **yếu hơn nhưng vẫn được hàm ý**. Đó là một "thang hàm ý" có sẵn trong ngữ pháp, không cần từ rào đón.
2. Đo trên CPU hôm nay: mệnh đề có số đếm chính xác (≥2) chỉ được SUPPORTED 26,6%, so với 65,1% khi dùng lượng từ mơ hồ. Có 2.787 mệnh đề người mang giới tính bị UNCERTAIN/REJECTED trong khi gold có `người`.
3. Phát hiện đo lường: `object_prf.py` so khớp chính xác, trong khi CHAIR-vi lại chấp nhận hypernym. VSPS nói `người` trung tính ở 420/558 ảnh test; 117 lần trong số đó bị tính là FP. Áp đúng quy tắc của CHAIR-vi thì P của VSPS là 41,5 → 48,2.
4. Loại từ (con/cái/chiếc) trong KTVIC gần như là hoà hợp từ vựng, không mang thêm thông tin thị giác: tín hiệu yếu (in-gold 0,314 so với 0,367), khớp với Pham & Kohnert (2009). Ý tưởng "loại từ làm verifier" vì thế bị **hạ cấp**.
5. Đề xuất 2 hướng chính cùng 1 hướng phụ: (I1) verifier đi xuống thang hàm ý thay vì loại bỏ; (I2) trục thứ ba "gọi tên ở mức nào" cho Know-and-Mention, kèm gold mức referent; (I3, phụ) loại từ chỉ dùng làm bậc trên cùng của thang.

---

## 1. Repo đã mã hoá những gì (đã đọc `rescap/vi/*`, `rescap/pipeline/realize.py`, `rescap/chair.py`)

- `classifier.py`: luật NUM+CL+N+ADJ, tính từ đứng sau danh từ, `classifier_for`, `check_agreement`. Docstring khẳng định "classifier là hoà hợp ngữ pháp, không phải thuộc tính của referent", nên lỗi loại từ được tính là lỗi fluency. Số liệu ở §3 **ủng hộ** khẳng định này.
- `color.py`: `xanh` có ba trạng thái (BLUE/GREEN/UNRESOLVED), tách CONFUSION khỏi UNDER-SPEC.
- `lexicon.py`: `HYPERNYMS` (đàn ông/phụ nữ/trẻ em → người; xe máy/ô tô/thuyền → phương tiện; …), `EXACT_COUNT_LIMIT=5`, `GENDERED_NOUNS`, `NEUTRAL_PERSON="người"`.
- `realize.py::_safe_head_noun`: khi giới tính chưa được kiểm chứng, đổi danh từ giới tính thành `người` **ở bước render**, tức là chỉ áp cho mệnh đề đã SUPPORTED.
- `verify.py`: số đếm lớn hơn 5 bị chặn trần ở UNCERTAIN.
- `chair.py::_gold_objects`: thêm hypernym vào gold, nên nói `người` cho gold `phụ nữ` được coi là đúng. Ngược lại, `scripts/object_prf.py` dựng gold bằng `objects_in` **không có hypernym**.

Còn thiếu: mọi bước làm yếu mệnh đề (giới tính → người, số → mơ hồ, xanh) đều xảy ra **sau** verifier. Không có cơ chế nào **cứu** một mệnh đề UNCERTAIN/REJECTED bằng cách lùi về dạng yếu hơn. Thêm vào đó, metric P/R đang phạt chính chính sách trung tính của hệ thống.

## 2. Những gì độc đáo về ngôn ngữ (chọn lọc, chỉ giữ những gì có hệ quả mô hình hoá)

| Hiện tượng | Tính chất | Hệ quả cho caption |
|---|---|---|
| Danh ngữ head-initial, từ ghép chính-phụ (`xe máy`, `nón lá`, `áo dài`, `cá vàng`) | Âm tiết đầu thường là hypernym, nên **tiền tố của danh ngữ được hàm ý** | Lùi mức chi tiết = cắt bớt bên phải, câu vẫn tự nhiên |
| `người` vừa là loại từ vừa là danh từ đầu (`người phụ nữ` → `người`) | Lược danh từ thì loại từ đứng làm đầu ngữ | Có sẵn một dạng trung tính giới tính, không đánh dấu (khác "person" trong tiếng Anh, vốn nghe gượng) |
| Số không biến tố; danh từ trần trung tính về số | `có chó` đúng với mọi số lượng | Có thể lùi về "có tồn tại" mà không cần cam kết số đếm |
| Tiếng Việt không có giống ngữ pháp; giới tính nằm ở danh từ/từ xưng hô (anh/chị/cô/chú, vốn mang cả tuổi) | Giới tính là lựa chọn từ vựng tự do | Người gán chọn mức chi tiết khác nhau (§3) |
| `xanh` gộp blue/green | Đã có trong `color.py` | Một bậc khác của cùng thang |
| Vật thể văn hoá (`nón lá`, `áo dài`, `xe máy`) | Thường được gọi ở mức cụ thể | Entry-level của người Việt khác tiếng Anh (van Miltenburg et al. 2017: độ quen thuộc làm tăng độ cụ thể) |
| Loại từ con/cái/chiếc | Phần lớn quy ước theo từ vựng | Ít thông tin thị giác (§3), **không** dùng làm tín hiệu chính |

Topic-comment và chuỗi động từ (serial verbs) có thật nhưng không gắn với P/R đối tượng, nên bỏ qua (YAGNI).

## 3. Số liệu đo hôm nay (CPU, chỉ đọc; script nằm trong scratchpad, không ghi vào repo)

Dữ liệu: KTVIC train (18.845 caption, 3.769 ảnh) và test (558 ảnh); `data/stage1_records/stage1_records.tar.gz` (3.700 ảnh, 28.912 mệnh đề thực thể).

**3.1 Loại từ gần như là hoà hợp từ vựng.**
- `xe`: chiếc 1.250 / cái 55 / con 0.
- `xe máy`: chiếc 538 / cái 15.
- `thuyền`: con 183 / chiếc 123. `tàu`: con 94 / chiếc 22. Đây là chỗ duy nhất có biến thiên thật.
- Giả thuyết "con = đang chuyển động" **không đứng**: tỉ lệ đi kèm động từ chuyển động là 17% (con) so với 21% (chiếc) với thuyền, và 35% so với 32% với tàu.
- Trong Stage-1, khi cặp loại từ–danh từ không khớp lexicon, tỉ lệ đối tượng có trong gold là 0,314, so với 0,367 khi khớp. Chênh lệch nhỏ, và phần lớn "lỗi" là biến thể tự do chiếc/cái (`chiếc ghế` 384, `chiếc bàn` 337), tức lexicon quá chặt chứ không phải mô hình ảo giác.
- Kết quả này khớp với Pham & Kohnert (2009): `con` chỉ đánh dấu động vật dưới 24% số lần.

**3.2 Số đếm chính xác là nơi verifier thất bại.** Phân bố trạng thái verifier theo loại lượng từ trong mệnh đề thực thể:

| Loại | n | SUPPORTED | UNCERTAIN | REJECTED |
|---|---|---|---|---|
| Số đếm chính xác ≥2 | 1.648 | 26,6% | 62,0% | 11,5% |
| Lượng từ mơ hồ (một vài/nhiều/các/những) | 5.829 | 65,1% | 26,4% | 8,5% |
| Một / danh từ trần | 21.435 | 34,5% | 43,8% | 21,6% |

Chỉ 7,1% caption gốc dùng số đếm ≥2, trong khi 43,6% dùng lượng từ mơ hồ. Người Việt mô tả số lượng phần lớn bằng lượng từ mơ hồ.

**3.3 Mức gọi tên người.**
- Mệnh đề người mang giới tính mà gold chỉ có `người` (cha của nó): UNCERTAIN 2.113, REJECTED 674, SUPPORTED 50. Trong đó đàn ông 1.605, phụ nữ 1.132, trẻ em 95.
- Trong 2.428 ảnh train có người, ở **598 ảnh (24,6%)** các người gán chia rẽ: có người viết `người` trung tính, có người viết danh từ giới tính.
- Trong 5.052 đối tượng "singleton" (chỉ 1/5 người gán nhắc), **738 (14,6%)** là cùng một referent được người gán khác gọi ở mức khác: người 316, phụ nữ 179, đàn ông 161. Như vậy một phần của con số "38% gold chỉ 1/5 người nhắc" là **biến thể cách gọi tên, không phải biến thể nội dung**.
- Trên test, 106/558 ảnh có cả tổ tiên lẫn hậu duệ trong cùng một gold set, nên |G| bị đếm trùng.

**3.4 Metric không nhất quán (KTVIC test, cùng một quy tắc áp cho mọi hệ thống).**
- P_h: tính đúng nếu đối tượng nằm trong gold ∪ hypernym(gold), giống hệt quy tắc của CHAIR-vi.
- R_spec: gold được tỉa về các lớp cụ thể nhất.
- R_vague: được tính điểm khi nói hypernym của một lớp gold.

| Hệ thống | P (hiện tại) | R (hiện tại) | P_h | R_spec | F1 | R_vague | F1 |
|---|---|---|---|---|---|---|---|
| zero-shot Qwen2.5-VL-7B | 31,6 | 57,1 | 33,4 | 55,8 | 41,8 | 61,1 | 43,2 |
| VSPS main_s42 | 41,5 | 36,7 | 48,2 | 34,2 | 40,0 | 46,4 | 47,3 |
| main_s43 / s44 | 42,4 / 41,7 | 37,3 / 37,2 | 49,5 / 48,4 | 34,6 / 34,7 | 40,7 / 40,5 | 46,6 / 47,0 | 48,0 / 47,7 |
| p2-noverif4090 | 39,0 | 42,0 | 44,8 | 39,6 | 42,0 | 51,6 | 48,0 |

Toàn bộ phần tăng của P_h ở VSPS đến từ đúng một từ: `người` (+117 TP). Zero-shot chỉ được thêm 56 TP từ `người` và 8 TP từ `đàn ông`.

**Cảnh báo bắt buộc:** đổi metric sau khi đã thấy kết quả là một tín hiệu đỏ đối với reviewer. Cách bảo vệ hợp lệ duy nhất có ba phần: (a) metric mới chỉ là **quy tắc mà CHAIR-vi của chính bài đã dùng**, nên đây là sửa sự không nhất quán; (b) báo cáo **cả** R_spec lẫn R_vague; (c) áp cho mọi baseline. R_vague cho điểm câu "có người" khi gold là "phụ nữ", tức là ít thông tin hơn. Nó không được thay thế R_spec.

## 4. Các ý tưởng

### I1. Verifier đi xuống "thang hàm ý" của danh ngữ (Entailment-Ladder Verification, ELV)

**Luận điểm.** Hiện verifier ra quyết định nhị phân trên một mệnh đề cố định, nên mệnh đề cụ thể mà không chắc thì bị loại, làm mất 15–20 điểm recall (theo brief). Trong tiếng Việt, mỗi mệnh đề thực thể có một **thang hữu hạn, do ngữ pháp sinh ra**, gồm các mệnh đề yếu dần, mỗi bậc được bậc trên hàm ý:

```
hai người phụ nữ mặc áo dài xanh lá
 → hai người phụ nữ mặc áo dài xanh      (bỏ phân giải xanh)
 → mấy/một vài người phụ nữ mặc áo dài   (số chính xác → mơ hồ)
 → một vài người mặc áo dài              (giới tính → loại từ làm đầu ngữ)
 → một vài người mặc áo                  (ghép → âm tiết đầu)
 → có người                              (tồn tại)
```

Mỗi bước là phép xoá hoặc thay **một ô** trong khuôn danh ngữ. Ngôn ngữ đơn lập đảm bảo kết quả vẫn đúng ngữ pháp, không cần rào đón (`có vẻ`). Verifier hỏi bậc cao nhất trước, rồi đi xuống cho đến khi gặp bậc đầu tiên SUPPORTED. Mục tiêu SFT là bậc đó, không phải "bỏ".

- **Vì sao giúp cả precision lẫn recall:** referent có thật nhưng chi tiết không chắc vẫn được nhắc, nên recall tăng. Chi tiết không chắc thì không bị khẳng định, nên precision ở mức chi tiết không giảm.
- **Đây không phải ghép lego:** đây là thuật toán *hedging your bets* (Deng et al. 2012) được chuyển từ phân loại sang **sinh văn bản có cấu trúc**, với cây phân cấp không phải WordNet do con người dựng mà là **chính cú pháp danh ngữ**. Nhờ đó số phép hỏi verifier bị chặn bởi số ô (tối đa ~5), không phụ thuộc kích thước taxonomy.

**Thí nghiệm đầu tiên.**
1. *CPU, ~30 phút:* lấy các mệnh đề thực thể UNCERTAIN/REJECTED trong `stage1_records`, sinh thang bằng `parse_noun_phrase` + `HYPERNYMS` + `NUMBER_MARKERS`. Tính **cận trên oracle**: nếu bậc lùi khớp gold (P_h/R_spec như §3.4) thì recall của tập giữ lại tăng bao nhiêu. Số liệu đã có cho thấy cận trên lớn: 2.787 mệnh đề người, 1.648 mệnh đề số đếm.
2. *GPU, ≤1 giờ:* chạy lại verifier ở chế độ logit một lượt (commit a8e4e01, κ=0,79 so với K=5) trên các bậc lùi. Ước lượng ~10–15k probe; con số này **UNVERIFIED**, cần đo thông lượng thực. Thước đo: recall của tập SUPPORTED theo số người nhắc (bảng 05 §2) và P_h, trước và sau ELV.
3. *Cổng dừng:* recall của tập SUPPORTED tăng ≥8 điểm và P_h giảm ≤1 điểm. Bác bỏ nếu bậc lùi chỉ cứu được dưới 20% số mệnh đề bị loại.

**Kiểm tra tính mới (nhanh).** Phía classification có Deng et al. CVPR 2012 (DARTS). Phía metric có partial credit trong VALOR-EVAL (2024). Tìm kiếm không thấy bài nào dùng **hypernym/specificity back-off như cơ chế giảm ảo giác trong captioning**, và cũng không thấy bài nào dùng cấu trúc danh ngữ của một ngôn ngữ cụ thể làm thang. Đánh giá: **mới ở mức trung bình–cao**. Rủi ro là reviewer nói "chỉ là hypernym back-off". Câu trả lời: thang ở đây là ngữ pháp, gồm nhiều chiều (số, giới tính, ghép, màu), và được học điểm dừng.

### I2. Trục thứ ba cho Know-and-Mention: "gọi tên ở mức nào" (Name-Level), kèm gold mức referent

**Luận điểm.** Know-and-Mention tách *tồn tại* × *đáng nhắc*. Số liệu §3.3 cho thấy còn một trục thứ ba bị trộn vào hai trục kia: **mức gọi tên**. Cùng một người, 5 người gán chọn `người` / `người phụ nữ` / `cô gái`, nên metric hiện tại đếm thành nhiều "đối tượng gold" khác nhau. Hệ quả có ba mặt: |G| bị phình ra (106/558 ảnh test), 14,6% singleton thật ra là biến thể tên, và chính sách trung tính giới tính của VSPS bị phạt như ảo giác (117 FP).

**Mô hình.**
- Gom các mention của 5 người gán thành **referent** theo `HYPERNYMS` (và bước tiếp theo là theo bbox nếu có).
- Học P(mức | lớp, ảnh) từ phân phối người gán. Đây là bản tiếng Việt của entry-level naming (Ordonez et al. ICCV 2013) và ManyNames (Silberer et al. LREC 2020).
- Mục tiêu SFT: với mỗi referent đã qua trục tồn tại và đáng nhắc, gọi tên ở **mức cụ thể nhất mà cả verifier lẫn phân phối người Việt cho phép**. I1 cung cấp cận trên của mức (cái gì được kiểm chứng), I2 cung cấp mức ưa dùng (cái gì người Việt hay nói).
- Kết quả phụ: một quan sát văn hoá đo được. `nón lá` chiếm 222/280 lần xuất hiện của `nón`, `áo dài` 237/2.277 lần của `áo`, tức vật thể văn hoá được gọi ở mức cụ thể, phù hợp với van Miltenburg et al. (2017).

**Thí nghiệm đầu tiên (CPU, ~1 giờ).**
1. Định nghĩa đã chạy được ở §3.4 (P_h, R_spec, R_vague), báo cáo cho mọi file `*-detailed.preds.json`.
2. Dựng lại bảng "recall theo số người nhắc" (05 §2) **trên referent** thay vì trên lớp từ vựng: tỉ lệ 38% singleton giảm còn bao nhiêu?
3. Fit một mô hình mức tên đơn giản (logistic theo lớp + diện tích/độ trung tâm nếu có trong records). Đo log-likelihood của mức do người gán chọn so với baseline "luôn chọn mức cụ thể nhất".

*Cổng dừng:* nếu xếp hạng giữa các hệ thống theo F1(P_h, R_spec) giống hệt theo metric hiện tại thì trục này chỉ là ghi chú đo lường, không phải đóng góp. Hiện tại xếp hạng **có đổi**: theo R_vague, VSPS vượt zero-shot về F1 (47,3 so với 43,2). Cần gold người gán 300 ảnh để khẳng định `người` thật sự đúng trong các trường hợp đó.

**Kiểm tra tính mới.** ManyNames và Ordonez nghiên cứu biến thiên tên ở tiếng Anh, theo từng đối tượng đơn lẻ. Ye et al. (CVPR 2025) đo khác biệt *nội dung* giữa các ngôn ngữ, không đo *mức gọi tên* bên trong một ngôn ngữ. Chưa thấy bài nào dùng biến thiên tên giữa nhiều người gán để (a) sửa recall của captioning và (b) làm mục tiêu SFT. Đánh giá: **mới ở mức trung bình**. Giá trị cao nhất của trục này là làm Know-and-Mention chặt chẽ hơn, không phải làm một bài riêng.

### I3 (phụ, hạ cấp). Loại từ làm bậc trên cùng của thang

Theo §3.1, loại từ không đáng làm verifier độc lập. Nó chỉ có ích ở **bậc cuối** của I1: khi danh từ đầu cũng không được kiểm chứng, hỏi ở mức loại từ-siêu loại: "có **con** vật nào…", "có **người** nào…", "có **chiếc** xe nào…". `người` và `con` là hai loại từ có ngữ nghĩa ổn định nhất (động vật/người). Thí nghiệm: gộp vào bước 2 của I1, chỉ thêm ~1 probe cho mỗi mệnh đề. Tính mới thấp. Có một khoảng trống đáng ghi (chưa thấy VLM nào được kiểm tra về loại từ, kể cả với tiếng Trung, nơi chỉ có nghiên cứu tâm lý ngôn ngữ và text-only), nhưng **không** nên theo đuổi trong bài này.

## 5. Khuyến nghị

- Gộp I1 và I2 vào Know-and-Mention thành *tồn tại × đáng nhắc × mức tên*, trong đó I1 là cơ chế thực thi trục tồn tại theo từng bậc.
- **Ưu tiên ngay (CPU, không cần GPU):** sửa sự không nhất quán giữa `object_prf.py` và CHAIR-vi trong *báo cáo*. Báo cáo cả hai. Không sửa code khi chưa có quyết định của người dùng.
- Không theo đuổi "loại từ mang thông tin thị giác". Dữ liệu và văn liệu đều phản bác.

## 6. Tài liệu (đã kiểm chứng venue và link, trừ chỗ ghi khác)

- Ye, Santy, Hwang, Zhang, Krishna. *Semantic and Expressive Variations in Image Captions Across Languages*. CVPR 2025, 29667–29679, DOI 10.1109/CVPR52734.2025.02762. [mlanthology](https://mlanthology.org/cvpr/2025/ye2025cvpr-semantic), [arXiv 2310.14356](https://arxiv.org/abs/2310.14356). Caption đa ngôn ngữ có trung bình nhiều hơn 29,9% đối tượng.
- van Miltenburg, Elliott, Vossen. *Cross-linguistic differences and similarities in image descriptions*. INLG 2017. [ACL W17-3503](https://aclanthology.org/W17-3503/).
- Berger, Frermann, Stanovsky, Abend. *A Large-Scale Multilingual Study of Visual Constraints on Linguistic Selection of Descriptions*. Findings EACL 2023. [ACL 2023.findings-eacl.172](https://aclanthology.org/2023.findings-eacl.172), [arXiv 2302.04811](https://arxiv.org/abs/2302.04811). Dự đoán việc dùng số từ ảnh; gần nhất với "số đếm" ở §3.2.
- Thapliyal et al. *Crossmodal-3600*. EMNLP 2022 (có tiếng Việt). [ACL 2022.emnlp-main.45](https://aclanthology.org/2022.emnlp-main.45).
- Deng, Krause, Berg, Fei-Fei. *Hedging Your Bets: Optimizing Accuracy-Specificity Trade-offs in Large Scale Visual Recognition*. CVPR 2012. [IEEE 6248086](https://ieeexplore.ieee.org/document/6248086).
- Ordonez, Deng, Choi, Berg, Berg. *From Large Scale Image Categorization to Entry-Level Categories*. ICCV 2013 (Marr Prize). [CVF](https://openaccess.thecvf.com/content_iccv_2013/html/Ordonez_From_Large_Scale_2013_ICCV_paper.html).
- Silberer, Zarrieß, Boleda. *Object Naming in Language and Vision: A Survey and a New Dataset* (ManyNames). LREC 2020. [ACL 2020.lrec-1.710](https://aclanthology.org/2020.lrec-1.710).
- VALOR-EVAL (partial credit theo khái niệm rộng hơn). [arXiv 2404.13874](https://arxiv.org/abs/2404.13874). Venue: **UNVERIFIED** (theo trí nhớ là Findings ACL 2024).
- Pham, Kohnert. *A corpus-based analysis of Vietnamese "classifiers" con and cái*. Mon-Khmer Studies 38, 2009 (bản thảo NIH ghi 2008). [PMC6326581](https://pmc.ncbi.nlm.nih.gov/articles/PMC6326581).
- Tran. Bài về cái/chiếc, Canadian Linguistic Association 2019. [PDF](https://cla-acl.artsci.utoronto.ca/pdfs/actes-2019/Tran-CLA-2019.pdf). Chưa đọc toàn văn.
- Chinese classifier prediction, text-only. [arXiv 2508.18253](https://arxiv.org/abs/2508.18253). Venue **UNVERIFIED**.
- Vu et al. *VnCoreNLP*. NAACL 2018 Demos. [ACL N18-5012](https://aclanthology.org/N18-5012). Nguyen & Nguyen. *PhoBERT*. Findings EMNLP 2020. [ACL 2020.findings-emnlp.92](https://aclanthology.org/2020.findings-emnlp.92). Phan et al. *ViT5*. NAACL SRW 2022. [ACL 2022.naacl-srw.18](https://aclanthology.org/2022.naacl-srw.18). Ba công cụ này dùng được cho bước tách từ khi dựng thang, nhưng lexicon của repo đã đủ cho thí nghiệm đầu, nên chưa cần.
