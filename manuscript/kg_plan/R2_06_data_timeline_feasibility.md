# R2-06. Phản biện vòng 2: khả thi về dữ liệu, công gán nhãn, giấy phép và lộ trình

Critic 06, ngày 2026-10-10. Đối tượng: `00_KE_HOACH.md` (bản nháp vòng 1), các mục 4, 5 (cổng), 6, 8.
Giả định đội: **1 nghiên cứu sinh (NCS) + 2 người gán nhãn bán thời gian**, 1× RTX 3090.

Nguồn đã mở trong phiên này (yêu cầu ẩn danh, không gửi dữ liệu cá nhân):
- ViCLIP-OT, arXiv 2602.22678 (trang abs và HTML; nộp 2026-02-26): §5.1, Phụ lục A, Phụ lục B, Bảng 5.
- UIT-EVJVQA, arXiv 2302.11752 (HTML): Bảng 2 "Participation summary".
- UIT-OpenViIC, arXiv 2305.04166 (HTML) và trang `uit-together.github.io/datasets/UIT-OpenViIC/`.
- UIT-ViIC, arXiv 2002.00175 (abs và HTML); HF API `ttrung1402/UIT-ViIC`.
- GitHub API và README của `Moobbot/VietSGG` và `pacman-ctm/ktvic`.
- Trang `Wikidata:Licensing`.
- Wikipedia "Chinese New Year": ngày Tết 2027.
- `../cfp/01_intl_conferences.json`, `../cfp/03_special_issues.json`.
- Các bảng giờ công trong 03, 08, 09, 15, 16.

Mọi con số giờ công dưới đây là **ước tính**: mình cộng lại các ước tính của agent vòng 1 và thêm giả định của riêng mình (ghi rõ ở từng dòng). Chưa có số bấm giờ thật.

---

## 1. Kết luận theo từng thành phần

| Thành phần | Kết luận | Lý do chính |
|---|---|---|
| §4 Dữ liệu: chọn ảnh test (gold SG 500 ảnh KTVIC test) | **fail** | 401/558 ảnh test KTVIC gần trùng ảnh train của UIT-OpenViIC (đã xác nhận). Kế hoạch lại dùng OpenViIC train để huấn luyện, nên benchmark bị rò rỉ dữ liệu. Ngoài ra chỉ có 157 ảnh sạch, không đủ để có 500 |
| §4 Dữ liệu: giấy phép | **needs-fix** | Ảnh KTVIC là ảnh UIT-EVJVQA, bộ này được phát qua thỏa thuận dữ liệu có ký. Tuyên bố CC BY 4.0 của VietSGG chỉ là một dòng trong README. Ghi chú "UIT-ViIC CC BY" là thẻ của bản tải lại do bên thứ ba đăng |
| §3 + §8: công người cho meta-eval | **fail** | Thiết kế cần 6 người chấm và khoảng 300 giờ, trong khi đội chỉ có 2 người gán |
| §4: gold SG pilot | **needs-fix** | Khoảng 122–200 giờ là làm được, nhưng bị cộng trùng với nhánh B, với gold của parser và với phần C của meta-eval |
| §3: gold cho parser (300 + 650 caption) | **needs-fix** | Gộp được vào lượt gán SG. Phần gán riêng 300 caption train là thừa |
| §7: audit VSPS | **pass** (cần ghi giờ vào kế hoạch) | Khoảng 15–30 giờ. Nhỏ, nhưng rơi đúng vào tháng 10 vốn đã quá tải |
| §2, §4: gold văn hóa và KG văn hóa 150–300 thực thể | **needs-fix** | Kế hoạch không ghi giờ công. Ước tính 80–165 giờ, hầu hết do NCS làm |
| §5: các cổng T0–T4 | **needs-fix** | T2 (mở rộng lên 1.500 ảnh) không thể làm trong khung thời gian này. Thiếu cổng go/no-go cho P2 trước hạn nộp. T1 kéo theo một nhánh việc không phục vụ P1 lẫn P2 |
| §5: ngân sách GPU | **needs-fix** (MINOR) | Con số 450–600 GPU-h chưa tính 3 seed × backbone thứ hai |
| §6, §8: lộ trình 10/2026 → 04–05/2027 | **fail** cho bản đầy đủ, **pass** cho bản rút gọn ở mục 4 | Nhu cầu khoảng 800–1.000 giờ người, gấp đôi năng lực. Tháng 02/2027 có Tết (06/02/2027), và chính tháng đó được xếp E2 + E3 + backbone thứ hai |

---

## 2. Các phát hiện

### B1 (BLOCKER). Nhu cầu giờ người gấp khoảng 2 lần năng lực của đội

**Kế hoạch nói.** "Gold scene graph … ~122–260 giờ công" (§4). Meta-eval dùng "3 người chấm 2 trục … 600 cặp … nhãn cấp mệnh đề trên 200 ảnh" (§3). Lộ trình dồn toàn bộ phần gán nhãn vào 11/2026–03/2027 (§8).

**Bằng chứng: tổng giờ người mà kế hoạch ngầm đòi hỏi.**

| Dòng việc | Nguồn ước tính | Giờ người |
|---|---|---|
| Gold SG pilot 500 ảnh, nhánh A (hướng dẫn, công cụ, hiệu chuẩn, đối chứng anchoring, gán chính, gán đôi 100 ảnh, phân xử) | 16 §5: 122 (85 của người gán + 37 của NCS). 03 §3: 85–115 riêng phần gán đôi, cộng 10–15 phân xử | 122–175 |
| Gold SG nhánh B (sửa 2.500 parse caption và liên kết với nút ảnh) | 16 §5 | ~23 |
| Mở rộng lên 1.500 ảnh (cổng T2) | 16 §6: ~100 + 15 | ~115 |
| Meta-eval đầy đủ (Likert A, cặp B, mệnh đề C, nhiễu, QA, pilot) | 15 §4 (giả định 6 người chấm) | ~300 |
| Gold parser (300 train + 650 test) | 08 §3.6 | 70–90 |
| Audit VSPS ở §7 (kiểm tay 100 mệnh đề cấu trúc, audit lại ≥150 quan hệ có gán đôi, kiểm 2% silver) | Ước tính của mình: 100 × 1 phút; 150 × 1,5 phút × 2; 16 §6 cho phần silver | 20–30 |
| Human eval cho phương pháp (03/2027; kế hoạch **không có số**) | Mình giả định 200 ảnh × 4 hệ × 2 người × ~1,5 phút | 40–50 |
| Gold văn hóa (65 ảnh hiện có là quá ít; 09 §5 đề xuất thêm 300–500 ảnh) | Mình giả định ~1 phút/ảnh, gán đôi 20%, cộng khâu chọn ảnh | 20–40 |
| Dựng KG: KG văn hóa 150–300 thực thể × 6–8 quan hệ ("một người 2–3 tuần" theo 09 §4), IsA ~250 dòng, gold liên kết 113 mục lexicon, bảng tiền nghiệm quan hệ phi lý | 09 §4 và 20, quy đổi 40 giờ/tuần cho phần KG văn hóa | 105–165 |
| **Tổng bản đầy đủ** | | **~815–990** |

Ghi chú về con số "122–260" trong kế hoạch: mức 260 của file 03 đã gồm 55–130 giờ "chấm người cho metric validation". Phần này lại được tính lần nữa trong 300 giờ của meta-eval, tức là bị cộng hai lần.

**Năng lực thực tế** (giả định của mình, cần NCS xác nhận):
- Hai người gán, mỗi người 6–10 giờ/tuần. Đây là nhịp 3 buổi × 2 giờ của 16 §5, cộng thêm một chút.
- Số tuần có ích từ 02/11/2026 đến 26/03/2027 là khoảng 21 tuần. Trừ khoảng 2 tuần thi cuối học kỳ 1 và khoảng 2 tuần nghỉ Tết (Tết Đinh Mùi 2027 rơi vào **06/02/2027**), còn khoảng 17 tuần.
- Như vậy người gán làm được 2 × (6–10) × 17 ≈ **200–340 giờ**.
- NCS có thể dành khoảng 5 giờ/tuần cho gán nhãn và dựng KG, tức khoảng **100–110 giờ**. Phần còn lại của NCS là kỹ thuật, GPU, sửa P0 và viết hai bài.
- Tổng năng lực: **~300–450 giờ**, chỉ bằng 35–55% nhu cầu.

Meta-eval còn có vấn đề về thiết kế: nó cần **3 người khác nhau trên mỗi caption** và có tới 6 người chấm. Với 2 người gán, NCS buộc phải là người chấm thứ ba trên toàn bộ caption, kể cả caption VSPS do chính NCS làm ra. Đây là thiên lệch tác giả mà reviewer EMNLP sẽ hỏi.

**Sửa.** Thay §8 bằng lộ trình rút gọn ở mục 4 của file này. Thêm vào §4 một bảng giờ công có cột năng lực, theo đúng mẫu bảng trên. Ghi vào §3: "meta-eval dùng 2 người chấm độc lập, mù hệ thống; NCS chỉ phân xử, không chấm caption của VSPS."

### B2 (BLOCKER). Chuỗi rò rỉ dữ liệu KTVIC ↔ UIT-OpenViIC

**Kế hoạch nói.**
- §4: "KTVIC … 401/558 ảnh test gần trùng train UIT-OpenViIC → báo thêm tập 157 ảnh sạch."
- §4: "UIT-OpenViIC: train/test thứ 2."
- §4: "pilot 500 ảnh KTVIC test."
- §5: sinh đồ thị cho "20k ảnh", tức gồm cả OpenViIC train.
- §8: "sinh G* cho KTVIC train."

**Bằng chứng (đã mở ViCLIP-OT, arXiv 2602.22678).** Phụ lục B và Bảng 5 dùng SSCD `sscd_disc_mixup`, ngưỡng cosine ≥ 0,8, so với tập train của UIT-OpenViIC.
- KTVIC-test: **401/558 (71,9%)** ảnh là gần trùng, còn lại **157** ảnh.
- KTVIC-train: **2.464/3.769 (65,4%)** ảnh là gần trùng, còn lại **1.305** ảnh. Kế hoạch bỏ sót con số này.
- Crossmodal-3600: 0 ảnh trùng.

Con số 401/558 được **xác nhận**. Bài chỉ phát hành mô hình (HF `minhnguyent546/viclip-ot`) chứ không phát hành danh sách ID ảnh trùng, nên phải tự chạy lại.

Hệ quả:
1. Benchmark gold SG lấy 500 trên 558 ảnh KTVIC test. Như vậy ít nhất 343 ảnh (500 − 157) là gần trùng OpenViIC train. Trong khi đó, bước sinh G*, parser bạc và captioner đều được huấn luyện trên OpenViIC train. Đây là rò rỉ train→test trực tiếp cho P1 lẫn P2.
2. Chỉ có 157 ảnh sạch, nên không thể có "500 ảnh KTVIC test sạch".
3. ViCLIP-OT **không** đo các cặp KTVIC-train ↔ KTVIC-test, OpenViIC-test ↔ OpenViIC-train và OpenViIC-test ↔ KTVIC-train. Ảnh của hai bộ đều có gốc từ UIT, và 65–72% ảnh KTVIC "trùng" OpenViIC. Vì vậy nhiều khả năng cũng có trùng bắc cầu giữa KTVIC train và KTVIC test. Điều này ảnh hưởng thẳng tới P0 (VSPS train KTVIC, test KTVIC). Hiện **chưa đo**.
4. Nếu gộp KTVIC train với OpenViIC train để làm "20k ảnh", khoảng 2.464 ảnh sẽ bị đếm hai lần.

**Sửa (đưa thành việc tuần 1 trong §8, tốn dưới 2 GPU-h).**
- Chạy SSCD (cùng checkpoint, ngưỡng 0,8) **all-vs-all** trên KTVIC train/test, OpenViIC train/val/test và UIT-ViIC. Phát hành danh sách cụm trùng.
- Thay dòng KTVIC trong §4 bằng:
  > "Tập test sạch = ảnh test không có láng giềng SSCD ≥ 0,8 trong bất kỳ tập train nào được dùng. Ảnh train có láng giềng trong một tập test bất kỳ bị loại khỏi train."
- Đổi "pilot 500 ảnh KTVIC test" thành:
  > "ViSG-test ≈ 400 ảnh = 157 ảnh KTVIC-clean + ~243 ảnh OpenViIC test sạch (phân tầng). Nếu xin phép OpenViIC không được thì thay bằng UIT-ViIC/COCO."
- Ở §7.5, sửa thành:
  > "Báo kết quả VSPS trên KTVIC-test-clean (đã loại trùng với KTVIC train và OpenViIC train)."

  Cần ghi rõ lập luận: với P0, cái cần chứng minh là KTVIC train↔test, không phải OpenViIC.
- Ghi thêm: 300 ảnh object-gold hiện có nằm trong KTVIC test, nên phần lớn có thể là ảnh gần trùng. Đếm lại giao giữa object-gold và tập sạch trước khi dùng cho T0/T2.

### M1 (MAJOR). Chuỗi quyền của KTVIC đi qua UIT-EVJVQA, bộ này có thỏa thuận dữ liệu ký tên

**Kế hoạch nói.** "Phát hành: chỉ phát hành annotation (CC BY-NC-SA 4.0), xin phép tác giả dataset bằng văn bản trước" (§4). "KTVIC không license" (§9).

**Bằng chứng.**
- README của `pacman-ctm/ktvic`: "The original link of the EVJVQA dataset was deleted by the owners". Ảnh hiện được phát qua một thư mục Google Drive. Theo GitHub API, repo có `license: null`.
- Bài EVJVQA (2302.11752, Bảng 2) ghi "#Signed Data Agreements 36", tức là dữ liệu challenge VLSP 2022 chỉ được phát cho bên đã ký thỏa thuận.
- Bản thân KTVIC (16 §7) ghi nhóm tác giả là VNU-UET và RIKEN, không phải chủ ảnh.

Vì vậy "tác giả dataset" ở đây gồm **hai bên**: nhóm KTVIC và nhóm chủ EVJVQA ở UIT. Nhóm UIT này trùng với nhóm được nêu là "va chạm" ở §9. Ngoài ra, nếu NCS chưa ký thỏa thuận EVJVQA thì quyền dùng ảnh KTVIC hiện tại cũng chưa rõ.

**Sửa (§4, dòng "Phát hành").**
> "Ảnh KTVIC có nguồn UIT-EVJVQA (phát qua thỏa thuận dữ liệu VLSP 2022). Trước 31/10/2026 gửi xin phép bằng văn bản tới (i) nhóm KTVIC, (ii) nhóm chủ UIT-EVJVQA, (iii) nhóm UIT-OpenViIC. Nếu đến 30/11 chưa có phản hồi: benchmark công bố chỉ gồm annotation + ID + script tải ảnh từ nguồn gốc. Nếu bị từ chối: thay ảnh bằng UIT-ViIC/COCO (license Flickr theo từng ảnh)."

Đồng thời đưa M1 lên đầu mục "Bản quyền dữ liệu" ở §9.

### M2 (MAJOR). Mốc nộp P2 vào ACM MM 04/2027 không khả thi

**Kế hoạch nói.** Tháng 02/2027 gồm GEPA, GRPO và backbone thứ hai. Tháng 03/2027 gồm meta-eval, 3 seed, human eval phương pháp và bảng latency. Tháng 04/2027 "nộp P2 ACM MM". §6 ghi "ACM MM 2027 (~04/2027, chưa xác nhận)".

**Bằng chứng.**
- `../cfp/01_intl_conferences.json`: ACM MM 2027 ghi "expected ~April 2027, not announced", ngày 2027-04-01, `verified: false`. EMNLP 2027 ARR ghi 2027-05-15 với `verified: false`.
- Tết 2027 là 06/02/2027, rơi đúng vào tháng có ba khối GPU lớn nhất.
- Human eval phương pháp (tháng 3) và meta-eval (tháng 3) dùng **cùng 2 người gán**, trùng thời gian.
- Bản thân G* phụ thuộc vào verifier đã được nâng cấp (T0, cổng cấu trúc, logit, box). Việc này chỉ xong sớm nhất vào cuối 11/2026.

**Sửa (§6).** P2 chuyển sang:
> "IP&M SI low-resource multimodal (hạn 31/08/2027, review cuốn chiếu) hoặc ACM TOMM. ACM MM 2027 chỉ nộp nếu cổng G-P2 (xem mục 4) đạt trước 15/02/2027."

P1 giữ EMNLP 2027 ARR. Bỏ "IP&M SI" khỏi danh sách dự phòng của P1 để hai bài không tranh cùng một special issue.

### M3 (MAJOR). Meta-eval bị xếp thứ tự vòng tròn

**Kế hoạch nói.** "Thu thập phán đoán người cho meta-eval" vào 12/2026 (§8). Tuy vậy §3 ghi "báo lại mọi kết quả sau khi bỏ caption VSPS/ViHG-Cap". Nghĩa là caption của ViHG-Cap cũng có trong bộ chấm, trong khi E1 chỉ bắt đầu từ 01/2027.

**Bằng chứng.** Bảng §8 của chính kế hoạch. 15 §3.1 chỉ liệt kê Qwen2.5-VL-7B zero-shot, Vintern-3B, VSPS-SFT, một tham chiếu giữ lại và một mô hình ngắn. Bộ này không có ViHG-Cap.

**Sửa (§3).**
> "Tập ứng viên của meta-eval được đóng băng ngày 15/11/2026 và không chứa ViHG-Cap. ViHG-Cap chỉ được chấm bằng metric và bằng human eval riêng của P2."

Bỏ chữ "/ViHG-Cap" trong câu "chống vòng lặp". Cách sửa này cũng làm mạnh lập luận chống tự phục vụ.

### M4 (MAJOR). Ba luồng gán nhãn chồng lên nhau trên cùng một tập ảnh

**Kế hoạch nói.** Có ba luồng riêng: gold parser "300 caption train + 650 test" (§3), nhánh B "sửa 2.500 parse caption + liên kết nút" (16 §4), và phần C của meta-eval "nhãn cấp mệnh đề trên 200 ảnh" (§3, 15 §3.2-C).

**Bằng chứng.** Cả ba đều là thao tác "parse caption → người sửa → gán đúng/sai so với ảnh", làm trên cùng nhóm ảnh test (08 §3.6; 15 §4; 16 §5). Cộng lại là 70–90 + 23 + 60 ≈ 150–170 giờ.

**Sửa.** Gộp thành **một lượt gán**:
- Trên ViSG-test, sửa parse của 2 tham chiếu/ảnh, liên kết từng nút với nút ảnh. Thao tác liên kết cũng cho luôn nhãn đúng/sai so với ảnh.
- Thêm 100 caption chi tiết của mô hình.

Lượt này đồng thời sinh ra test của parser, nhãn mệnh đề của meta-eval và "ảo giác trong caption người". Bỏ phần gán gold 300 caption train cho parser: dùng silver, và lấy 50 caption của lượt trên làm dev. Ước tính tiết kiệm khoảng 100 giờ.

### M5 (MAJOR). Khoảng 185–285 giờ công không có trong kế hoạch

**Kế hoạch nói.** "KG văn hóa Việt (mới, 150–300 thực thể)", "IsA ~250 dòng", "human eval phương pháp", "audit lại ≥150 quan hệ". Không mục nào có giờ công.

**Bằng chứng.** Bảng ở B1: KG 105–165, human eval 40–50, gold văn hóa 20–40, audit 20–30.

**Sửa.**
- Ghi các số này vào bảng giờ công của §4.
- Thu nhỏ KG văn hóa xuống **≤100 thực thể × 4 quan hệ** (is_a, visual_cue, confusable_with, region), làm khoảng 30–40 giờ. Dùng lại danh mục 12 hạng mục và 156 thực thể của VietMEAgent làm điểm xuất phát; cần kiểm lại license của bộ HF đó trước khi dùng.
- Bỏ "bảng tiền nghiệm quan hệ phi lý" khỏi MVP.

### M6 (MAJOR). Tháng 10/2026 quá tải và không ai làm việc gán

**Kế hoạch nói.** Tháng 10 gồm: T0; cổng cấu trúc; verifier logit; box OWLv2; schema SG; IsA; KG văn hóa v0; hướng dẫn gán nhãn; hoàn thiện P0.

**Bằng chứng.** Hôm nay là 10/10, nên chỉ còn 3 tuần. Bản thân P0 ở §7 đã gồm audit lại ≥150 quan hệ, kiểm tay ~100 mục và tính bootstrap CI. Kế hoạch chưa có bước tuyển người gán, xin chấp thuận đạo đức (15 §3.2: "xin chấp thuận của khoa") hay gửi thư xin phép dữ liệu, trong khi đây là các việc có độ trễ dài nhất.

**Sửa.** Tháng 10 chỉ còn: P0, dedup SSCD (B2), gửi thư xin phép (M1), tuyển người gán và xin chấp thuận, hướng dẫn v0.1 + IsA, đóng băng hệ ứng viên meta-eval (M3). Verifier logit, box và KG văn hóa chuyển sang tháng 11.

### m1 (MINOR). VietSGG "CC BY 4.0" chỉ áp dụng cho phần nhãn của VietSGG

**Bằng chứng.**
- README của VietSGG có dòng "License: CC BY 4.0", nhưng GitHub API trả `license: null` (không có file LICENSE).
- Ảnh là COCO (license Flickr theo từng ảnh). Caption của UIT-ViIC được tác giả gốc ghi là "published on our lab website for research purposes" (2002.00175).
- Thẻ `license:cc-by-4.0` của `ttrung1402/UIT-ViIC` trên HF là bản tải lại do bên thứ ba đăng, không phải nguồn có thẩm quyền.
- Nhãn VietSGG sinh bằng GPT-4 (theo README).

**Sửa (§4).** Đổi "UIT-ViIC + VietSGG (2.873 ảnh, CC BY 4.0)" thành:
> "VietSGG: nhãn SG CC BY 4.0 theo README (không có file LICENSE); caption UIT-ViIC 'for research purposes'; ảnh COCO theo license Flickr từng ảnh."

### m2 (MINOR). Trang tải UIT-OpenViIC không có điều khoản

**Bằng chứng.** Trang `uit-together.github.io/datasets/UIT-OpenViIC/` chỉ có mô tả và link tải, không có license. Câu "available online for non-commercial research" chỉ nằm trong bài 2305.04166. CC BY-NC-SA 4.0 ở arXiv là license của bài báo. Ảnh crawl từ Google/Bing, nên bản quyền thuộc bên thứ ba.

**Sửa.** Giữ chính sách "chỉ phát hành annotation + ID", và ghi nguồn của câu "non-commercial" là bài báo, không phải trang dataset.

### m3 (MINOR). Wikidata là CC0, nhưng chỉ phần dữ liệu có cấu trúc

**Bằng chứng.** `Wikidata:Licensing`: "All structured data (main, Property, Lexeme, EntitySchema namespaces) … Creative Commons Zero. Text in other namespaces … CC BY-SA 4.0."

Văn bản Wikipedia tiếng Việt cũng là CC BY-SA. Nếu đưa đoạn mô tả Wikipedia vào KG văn hóa thì điều khoản ShareAlike không tương thích với ý định phát hành CC BY-NC-SA.

**Sửa (§4, dòng KG văn hóa).**
> "Chỉ dùng statement Wikidata (CC0) và mô tả tự viết; không chép văn bản Wikipedia."

### m4 (MINOR). Đạo đức và giao thức với người

Kế hoạch có gán thuộc tính giới tính cho người thật trong ảnh (E2: "nêu giới tính UNCERTAIN"). Danh sách kiểm Responsible NLP của ARR yêu cầu nêu tiền công, hướng dẫn và cách tuyển người gán. Việc NCS làm người phân xử gold cũng phải được công khai.

**Sửa (§9).** Thêm một mục "Đạo đức": tiền công, chấp thuận của khoa, không thu PII, công bố vai trò của NCS, và giới tính chỉ gán khi rõ ràng (mặc định UNCERTAIN).

### m5 (MINOR). Ngân sách GPU thiếu

**Bằng chứng.** Cộng các mục ở §5: 168 + ~72 + 75–140 + 80–100 + 65–75 ≈ 460–555, cộng GRPO, ra khoảng 450–600 GPU-h. Con số này chưa gồm:
- 3 seed cho E1/E2,
- backbone thứ hai (Qwen3-VL-8B, gần như nhân đôi E1/E2),
- khoảng 11 baseline,
- 15–20 GPU-h gán trước cho gold.

Ước tính của mình: **700–900 GPU-h**. Một GPU dùng chung với P0 thường chỉ đạt khoảng 60–70% tải, nên quy ra **6–9 tuần** chứ không phải 3–4 tuần.

**Sửa.** Trong MVP, bỏ backbone thứ hai, G1/G2 và E3 (xem mục 4).

### m6 (MINOR). Cổng T1 và T2 không phục vụ hạn nộp

T2 mở rộng lên 1.500 ảnh (~115 giờ) và cần giấy phép (16 §6), không thể xong trước 05/2027. T1 (so GRIT với LVLM) mở ra nhánh "captioner nhỏ", nhánh này không nằm trong P1 lẫn P2.

**Sửa.**
- Đổi T2 thành: "đạt κ/F1 → chốt ViSG-test; không đạt → gộp vị từ; **không mở rộng trong 2026–27**."
- Hạ T1 thành một baseline GRIT trong bảng của P2. Bỏ nhánh captioner nhỏ.

---

## 3. Những điểm kế hoạch làm đúng

- Đã nêu được vấn đề trùng 401/558 và tập 157 ảnh (số đúng với ViCLIP-OT). Đã chọn "chỉ phát hành annotation, xin phép trước".
- Nguyên tắc "500 ảnh có IAA tốt là đủ; huấn luyện bằng silver có kiểm mẫu, không gán tay hàng nghìn ảnh" (16 §6) là đúng hướng.
- Gold được làm bằng cách sửa silver chứ không gán từ đầu, và có đối chứng anchoring.
- Có cổng stop/go (T0, T3, T4) với ngưỡng định trước, và có ghi chú "chưa xác nhận" cho hạn ACM MM/EMNLP.
- T0 không tốn GPU, dựa trên 244 mục đã audit; đây là một cổng rẻ và đúng.

---

## 4. Đề xuất: lộ trình rút gọn, với P1 và P2 tối thiểu (MVP)

### 4.1 P1 tối thiểu (benchmark + metric, nộp EMNLP 2027 ARR ~15/05/2027, chưa xác nhận)

- **Ảnh:** ViSG-test khoảng 400 ảnh (dev 80 / test 320) = 157 ảnh KTVIC-clean + ~243 ảnh OpenViIC test sạch. Cả hai đều đã qua dedup all-vs-all ở B2.
- **Một lượt gán SG** gồm 3 trạng thái, box và thuộc tính đúng chủ thể. Gán đôi 25%.
- **Cùng lượt đó**, sửa parse của 2 tham chiếu/ảnh và liên kết nút (theo M4), cộng 100 caption chi tiết. Lượt này cho ra test parser và nhãn mệnh đề.
- **Meta-eval A:** 400 ảnh × 4 ứng viên đã đóng băng (Qwen2.5-VL-7B zero-shot, Vintern-3B, VSPS-SFT, tham chiếu giữ lại), 2 người chấm mù hệ thống, 2 trục. Bỏ phần cặp B. Phần C lấy từ lượt gán ở trên.
- **Metric:** chỉ M1, M2, M3 và M4. M4 dùng tập văn hóa nhỏ. Chuyển M5 (TBW, cần người chấm span) và M6 (NVL, cần fact KG) sang P2 hoặc bỏ.
- **Parser:** silver + ViT5. Áp luật +3 F1 (T3). Không có gold train.
- **KG cho P1:** chỉ bảng IsA ~250 dòng.

### 4.2 P2 tối thiểu (ViHG-Cap)

- **Thành phần giữ lại:**
  - B: cổng cấu trúc + verifier logit + box.
  - C: lùi IsA.
  - E1: SFT graph-then-caption, 1 backbone (Qwen2.5-VL-7B), 3 seed.
  - E2: GEPA, một biến thể.
  - Đối chứng đồ thị xáo trộn (G0).
- **Thành phần bỏ khỏi MVP và để dành cho bản mở rộng tạp chí:** E3 GRPO, G1/G2, Qwen3-VL-8B, KG-prior một chiều.
- **KG văn hóa:** ≤100 thực thể.
- **Human eval:** 150 ảnh × 3 hệ × 2 người.

### 4.3 Bảng giờ công của MVP (ước tính)

| Việc | Người gán (giờ) | NCS (giờ) |
|---|---|---|
| Hướng dẫn, IsA, công cụ, script IAA | — | 30 |
| Hiệu chuẩn 20 ảnh + đối chứng anchoring 30 ảnh | 20 | 3 |
| Gán SG 400 ảnh × 6 phút × 1,25 (gán đôi 25%) | 50 | — |
| Sửa parse và liên kết nút (800 tham chiếu × 0,5 phút + 100 caption chi tiết × 6 phút, gán đôi 20%) | 20 | — |
| Meta-eval A (400 ảnh × ~5,3 phút × 2 người) | 70 | — |
| Phân xử và QA | — | 15 |
| Audit VSPS ở §7 (cho P0) | 8 | 5 |
| Gold văn hóa (~300 ảnh, có/không theo danh mục) | 10 | 3 |
| KG văn hóa ≤100 thực thể | — | 35 |
| Human eval P2 (150 × 3 × 2 × ~1,5 phút) | 23 | — |
| **Tổng** | **~200** | **~90** |

Mức này vừa với năng lực của đội: 200–340 giờ cho người gán và khoảng 100 giờ cho NCS. Còn dư khoảng 30% cho trễ hạn.

### 4.4 Lộ trình sắp lại

| Thời gian | Người gán | NCS / GPU | Cổng |
|---|---|---|---|
| 10/10–31/10/2026 | Tuyển người, xin chấp thuận | Hoàn thiện P0 (gồm §7.1–7.6). Chạy dedup SSCD all-vs-all (<2 GPU-h). Gửi thư xin phép tới KTVIC, EVJVQA và OpenViIC. Viết hướng dẫn v0.1 + IsA. Sinh caption cho 4 ứng viên meta-eval | T0. Đóng băng ứng viên vào 15/11 |
| 11/2026 | Hiệu chuẩn, anchoring, bắt đầu gán SG | Verifier logit + cổng cấu trúc + box OWLv2. Gán trước ViSG-test. Silver G* trên train **sạch** | Giấy phép: hết 30/11 thì chuyển sang phương án "chỉ ID" |
| 12/2026 | Xong gán SG, sửa parse + liên kết nút | IAA. Parser bạc → ViT5. Bắt đầu E1 | T2 (chốt ViSG-test, không mở rộng) |
| 01/2027 (có thi) | Meta-eval A (nhịp chậm) | E1 với 3 seed + đồ thị xáo trộn. T3 (parser) | **G-P2, 31/01**: E1 phải hơn SFT-không-kiểm-chứng trên M1-precision (dev, CI 95%) |
| 02/2027 (Tết 06/02) | Nghỉ khoảng 2 tuần, sau đó xong meta-eval A | Chỉ GPU: GEPA E2 với 3 seed. Tính M1–M4 | T4 (τ_c của M1 so với VLM-judge) |
| 03/2027 | Gold văn hóa, human eval P2 | Viết P1 | ACM MM chỉ nộp nếu G-P2 đạt và E2 xong trước 15/02 |
| 04/2027 | — | P1 lên arXiv. Viết P2 | — |
| ~15/05/2027 | — | P1 nộp EMNLP ARR (cần kiểm lại hạn khi CFP ra) | — |
| 06–08/2027 | — | P2 nộp IP&M SI (31/08/2027) hoặc TOMM. Bản mở rộng: E3, G1/G2, backbone thứ hai | — |
