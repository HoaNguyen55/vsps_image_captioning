# R11: Bản đồ tài liệu theo cách Litmaps, khoảng trống và novelty mới

*Ngày 2026-10-14.*

**Nguồn**
- Sáu báo cáo `manuscript/research_r11/L1..L6/REPORT.txt`.
- Brief: `manuscript/research_r11/CONTEXT_R11.md`.
- Bảng cầu nối: `manuscript/research_r11/bridge_table.txt`.
- Bản đồ đầy đủ do Gemini dựng lại: `.session_backup/2026-10-14/r11_litmaps_n3/summary.txt` (Claude đã review: không có yêu cầu thất bại, ghép phiên bản bài báo đúng).
- Bản đồ tương tác: https://claude.ai/artifact/MMrek8w7qSMnP3W5MaeNWJ

**Quy ước:** [MH] là tín hiệu do mô hình tạo; [CXM] là chưa xác minh; [SUY] là suy luận của người tổng hợp. Không có tuyên bố "đầu tiên". Tài liệu không chứa câu chú thích OpenViIC nào.

---

## 1. Tóm tắt

1. **Làm lại Litmaps trên dữ liệu mở.** Ứng dụng Litmaps cần đăng nhập cá nhân, nên vòng này tái tạo logic "Discover" của Litmaps.
   - 50 bài gốc, chia 12 cụm.
   - Thu mọi bài trích dẫn hoặc được trích dẫn qua OpenAlex (bản đầy đủ 19.268 bài, Gemini chạy lại từ máy GPU) và Semantic Scholar (41 bài gốc).
   - Với mỗi cặp cụm, đếm số bài nối hai cụm và so với số kỳ vọng nếu hai cụm độc lập.
2. **Khoảng trống rõ và vững nhất:** đánh giá ảo giác × lý thuyết tối ưu F-measure.
   - 0 bài nối, so với 74,1 bài kỳ vọng.
   - Với "null công bằng" (L1, hiệu chỉnh việc các cụm xa nhau vốn ít trích dẫn nhau) vẫn kỳ vọng khoảng 5–19 bài, nên kết quả vẫn có ý nghĩa.
   - Các khoảng trống khác:
     - metric caption × độ đầy đủ gold: 0/1.016;
     - DPO × độ đầy đủ gold: 1/330;
     - RL cho caption × Goodhart: 1/229;
     - kiểm soát độ dài/số lượng × DPO: 2/16, và cả 2 bài đều chỉ là COCO và Visual Genome.
3. **Novelty mạnh nhất, đã có bằng chứng:** dấu của mức "nói nhiều được thưởng" trong F1 đối tượng thô phụ thuộc vào độ đầy đủ của gold (L1, D-C).
   - Số đối tượng tối ưu cho F1 là M* = b·Ḡ/(1−b).
   - Khi gold thưa, độ dốc của F1 theo log M đổi dấu:
     - KTVIC, 36 hệ thống: 1 ref −10,65 → 5 ref +14,15;
     - COCO-2500: 1 ref −4,28 → 5 ref +11,08 → nhãn instance +22,41.
   - Cả 4 dự đoán cho COCO được viết trước khi chạy và đều đúng.
4. **Đính chính lớn cho bài báo:** 5 câu tham chiếu KTVIC của một ảnh do MỘT người viết.
   - Bài báo KTVIC, mục 3.2: giai đoạn đầu chỉ có 3 người; giao diện yêu cầu một người điền 5 ô cho một ảnh. Claude đã đọc trực tiếp bản PDF.
   - L2 đo được: 71% đối tượng xuất hiện đúng 2 lần nằm ở hai câu liền kề (KTVIC test), so với 40% nếu các câu độc lập. UIT-ViIC 0,38, COCO 0,40, panel OpenViIC 0,43–0,46.
   - Vì vậy "mức con người 1v4" trên KTVIC là độ nhất quán của một người viết với chính mình, không phải độ đồng thuận giữa các người chú thích. Trong bảng ghi là "leave-one-out trên câu tham chiếu (một người viết mỗi ảnh)". Các claim về biên của con người chuyển sang COCO, UIT-ViIC và panel OpenViIC (PD-3).
5. **Lý thuyết đã có, phải trích dẫn, không được nhận:**
   - Quy tắc "F1 tăng khi precision biên > F1/2" (G2) chính là định lý của Lipton và cộng sự (ECML-PKDD 2014).
   - Mô hình precision của người theo số câu tham chiếu đã có trong Chen và cộng sự (2015, arXiv 1504.00325, mục 4.2).
6. **Vùng đông:** giải mã chống ảo giác × DPO (373 bài nối, gấp 5,1 lần kỳ vọng). Phương pháp mới ở đây khó có novelty.
   - Đóng góp nên đi vào đánh giá: chấm lại các phương pháp đã công bố ở số đối tượng khớp.
   - L6 xác nhận chưa ai làm việc này cho các phương pháp HUẤN LUYỆN (DPO/RL). Không repo nào trong 12 repo công bố output từng câu.

---

## 2. Cách dựng bản đồ và giới hạn

- **Bài gốc.** 50 bài trong 12 cụm:
  - A1 metric ảo giác; A2 giải mã chống ảo giác; A3 kiểm soát độ dài/số lượng;
  - B1 metric caption; B2 độ đầy đủ gold và người chấm; B3 tầm quan trọng đối tượng;
  - C1 Goodhart/tối ưu quá mức; C2 RL cho caption;
  - D tối ưu ưu tiên (DPO);
  - E1 thị giác–ngôn ngữ tiếng Việt; E2 đa ngữ và giao thức chấm;
  - F tối ưu F-measure và phân bổ.
- **Dữ liệu.**
  - OpenAlex: lượt đầu bị chặn vì hết hạn mức miễn phí theo IP; bản đầy đủ do Gemini chạy lại.
  - Semantic Scholar: 41 bài gốc có nhiều bản arXiv, vì OpenAlex đếm thiếu (ví dụ chỉ ghi 1 bài trích dẫn LeHaCE).
  - Các bài được gộp theo tiêu đề đã chuẩn hoá.
- **Giới hạn.**
  - Số bài nối chỉ là chỉ dấu.
  - Khoảng 7–14 lần chênh so với kỳ vọng đến từ khoảng cách giữa các ngành (L1). Một số khoảng trống chỉ là khác từ vựng: các bài RL cho caption mô tả hiện tượng Goodhart là "degeneration" nhưng không trích seed Goodhart (L4). Một số khác là khác thời kỳ: các seed về tầm quan trọng đối tượng đều cũ (L3).
  - Vì vậy mỗi khoảng trống đều đã được agent đọc bài để kiểm tra.
- **Mở trong Litmaps thật.**
  - Người dùng đăng nhập bằng tài khoản Google của mình, rồi nhập `manuscript/research_r11/litmaps_seeds_top20.bib`. Gói miễn phí giới hạn 20 bài gốc.
  - Hạt giống bổ sung cho từng khoảng trống nằm ở mục 4 của mỗi báo cáo L1–L6.

---

## 3. Bản đồ cho thấy gì

Bảng dưới dùng số của bản đồ đầy đủ (19.268 bài). Số trong ngoặc là bản gộp đầu (7.725 bài).

| Cặp cụm | Bài nối / kỳ vọng | Các bài nối thực chất là gì |
|---|---|---|
| A1 metric ảo giác × F F-measure | 0 / 74,1 (0 / 137,7) | Không có. THRONE chấm bằng F0.5 nhưng không dùng quy tắc ngưỡng của nó (L1) |
| B1 metric caption × B2 độ đầy đủ gold | 0 / 1.016 | Không có (L2) |
| A1 × B2 | 11 / 935 | Đều là bài backbone thị giác dùng ImageNet ReaL và POPE làm bảng benchmark, không bài nào nghiên cứu độ đầy đủ gold (L2) |
| B2 × D DPO | 1 / 330 | Không có bài nối thực chất (L2) |
| B3 tầm quan trọng × D | 0 / 13,1 | Không có. Gần nhất là VIFIDEL (ACL 2019): một gold, không kiểm soát số lượng (L3) |
| C1 Goodhart × C2 RL caption | 1 / 229 | Chỉ là trích dẫn chung chung như ImageNet, ResNet (L4) |
| A3 kiểm soát độ dài/số lượng × D | 2 / 15,7 | Chỉ COCO và Visual Genome (L6) |
| A1 × E1 tiếng Việt | 11 / 11,5 (12 / 26,4) | Tín hiệu yếu. Không có benchmark ảo giác hình ảnh tiếng Việt; ViHallu (2601.04711) chỉ có văn bản (L5) |
| A2 × D (vùng đông) | 373 / 72,5 | Toàn bài phương pháp DPO/RL/giải mã năm 2026 (L6) |

---

## 4. Novelty mới suy ra, xếp theo giá trị cho bài báo theo PD-2

Thang N/R là novelty/rủi ro, 1–5, do agent tự chấm. Chi phí tính trên 1 RTX 3090 hoặc CPU.

### 4.1 Nhóm A: đã có bằng chứng, rẻ, nên đưa vào bài

**N1. Dấu của mức "nói nhiều được thưởng" phụ thuộc vào gold** (L1 D-C; trụ cột C2, cùng C1 và C4; N3/R2; dưới 0,3 CPU-h)
- **Claim.** Biên TP = a·M^b cho F1 vi mô đạt cực đại tại M* = b·Ḡ/(1−b). b tăng theo độ đầy đủ của gold, nên:
  - F1 thô thưởng việc nói nhiều chỉ khi M* lớn hơn số đối tượng các hệ thống đang nhắc;
  - với gold thưa, F1 thô thưởng việc nói ít.
- **Bằng chứng** (hệ số góc F1 theo log M, bootstrap theo ảnh):
  - KTVIC, 36 hệ thống FT, mang tính THĂM DÒ: 1 ref −10,65 [−13,87; −7,28] (k ref đầu) hoặc −3,32 [−6,19; −0,48] (k ref ngẫu nhiên); 2 ref +3,77; 5 ref +14,15 [+11,67; +16,49]. Phải nêu cả hai giá trị 1 ref, vì câu đầu trong chuỗi của một người viết là đặc biệt.
  - Bằng chứng xác nhận là COCO (4/4 dự đoán đóng băng), cộng với phần lặp lại trên UIT-ViIC và XM3600.
  - COCO-2500, 9 hệ thống, dự đoán đóng băng trước, 4/4 đúng: 1 ref −4,28; 5 ref +11,08; nhãn instance +22,41.
  - Dấu dự đoán theo M* đúng ở 12/12 biến thể COCO và 16/20 biến thể KTVIC.
- **Phát hiện phụ.** Ref số 1 của KTVIC "đặc biệt": b(k=1) là 0,403 theo thứ tự file, nhưng 0,536 với tập con ngẫu nhiên. Phải chạy G2-C với tập con ngẫu nhiên.
- **Kiểm chứng tiếp.** UIT-ViIC (ref so với nhãn instance) và XM3600-VI. Luật dừng: nếu dấu sai dự đoán ở ít nhất 2 bối cảnh thì bỏ claim đổi dấu.

**N2. Kiểm định tính hoán đổi của các câu tham chiếu** (L2 D3; trụ cột C4, đồng thời sửa cách diễn đạt của C2, C3 và E5; N2/R1; dưới 0,2 CPU-h)
- **Claim.** Ba thống kê phân biệt được ba kiểu bộ tham chiếu: một người viết cả 5 câu (KTVIC), câu bị sắp xếp theo độ dài (Flickr30k), và người chú thích độc lập (COCO, UIT-ViIC, OpenViIC). Ba thống kê là: tỉ lệ đối tượng xuất hiện đúng 2 lần nằm ở hai câu liền kề; hiệu Jaccard lag-1 trừ lag-2..4; gradient precision theo vị trí câu.
- **Bằng chứng** (tỉ lệ cặp liền kề, kỳ vọng 0,40):
  - KTVIC test 0,710 [0,670; 0,752]; KTVIC train 0,667;
  - UIT-ViIC 0,384; COCO 0,402–0,406; panel OpenViIC 0,43–0,46;
  - Flickr30k 0,483, do câu được sắp xếp theo độ dài: số từ trung bình theo vị trí 19,4 → 8,9.
- **Hệ quả bắt buộc.**
  - Mọi ước lượng Chao/Good-Turing, đường cong theo k ref và "trần con người" leave-one-out trên KTVIC phải được diễn đạt là "câu tham chiếu cùng một người viết".
  - Đơn vị "người chú thích tương đương" (E5) chỉ có nghĩa trên panel OpenViIC.

**N3. Đếm số lượng đối tượng trong dữ liệu ưu tiên công khai: khớp độ dài không có nghĩa là khớp số lượng** (L6 D2; trụ cột C1, động cơ cho M3; N3/R1; pilot đã chạy)
- **Bằng chứng** (chấm bằng matcher CHAIR, COCO-80):
  - Chỉ 35–69% cặp chosen/rejected có cùng số lớp đối tượng.
  - Ở HA-DPO, HSA-DPO và SENTINEL, câu chosen nhắc ít lớp hơn trong 82–90% số cặp lệch số lượng, dù độ dài chỉ chênh 1–2 từ.
  - Vì vậy các cách sửa lệch độ dài (R-DPO, SamPO, bộ lọc độ dài của RLAIF-V) vẫn để ngỏ kênh "nói ít đi".
- **Kiểm chứng tiếp.** Thêm RLAIF-V và RLHF-V (cần pyarrow để đọc file). Dự đoán: ở RLAIF-V, câu chosen nhắc ít lớp hơn trong ít nhất 60% số cặp lệch số lượng.

**N4. Hạch toán chuyển giao hai gold ở mức đối tượng** (L3 D1; trụ cột C3; N3/R2; dưới 0,2 CPU-h)
- **Claim.** Lợi ích trên ref KTVIC không chuyển sang panel vì hai lý do: các lần nhắc chỉ một hướng dẫn chú thích công nhận, và hiệu ứng pha loãng do kích thước gold khác nhau (×0,69). Nguyên nhân KHÔNG nằm ở các đối tượng ít người nhắc (k thấp).
- **Bằng chứng.**
  - UPE (test, 3 seed): lợi ích nằm ở đối tượng mà hai gold cùng công nhận (+0,016 trên +0,017 TP/ảnh).
  - UPE mất một nửa lợi ích vì bỏ các đối tượng chỉ panel nhắc (−0,008/ảnh).
  - Với 35_e, phần mất nằm ở phía đối chứng: đối chứng vote thêm đối tượng mà chỉ panel nhắc (+0,41).
  - L3 tái lập chính xác các số liệu MT2 và n11 của Gemini.

**N5. Thẻ đánh giá theo mức quan trọng của đối tượng, ở số lượng khớp** (L3 D2; trụ cột C3 và C4; N2–3/R2)
- **Tỉ lệ bỏ sót đối tượng nổi bật** (đối tượng mà mọi ref còn lại đều nhắc):
  - P1 bỏ sót 25,2% trên dev và 28,3% trên test;
  - một người chú thích để riêng ra chỉ bỏ sót 13,0% và 17,3%;
  - số đối tượng nhắc gần như bằng nhau.
- **Tách phần "ảo giác" theo panel.** 58,5–58,7% các lần P1 nhắc ngoài ref được panel nhắc tới, ngang với các đối tượng chỉ một người nhắc của chính con người (59,6–60,2%).
- **Ứng viên bị loại.** Dùng k/5 ở mức lớp để đoán đối tượng nào panel xác nhận: AUC chỉ 0,52–0,57 (L3 D3).

### 4.2 Nhóm B: thay đổi cách đánh giá, cần judge quyết

**N6. Thay cổng tỉ số κ = Δρ_I/Δρ_A (D15(iii)) bằng kiểm định tuyến tính L = Δρ_I − κ0·Δρ_A** (L4 D3; trụ cột C3; N3/R2)
- **Vì sao tỉ số κ có vấn đề.** Khi Δρ_A nhỏ thì κ mất ổn định:
  - đổi theo seed: UPE 0,07 / 0,75 / 0,40, CI rất rộng;
  - đổi theo cách kiểm soát số lượng: 35_e được 0,23 với đối chứng vote của M4, nhưng 1,12 với ρ.
- **L ổn định hơn.** UPE −0,08 [−0,41; +0,22]; 35_e +0,36 [−0,86; +1,56].
- **Đề xuất.** κ0 lấy từ κ_lin của chính pool trước huấn luyện (khoảng 0,30 trên dev300). Qua cổng khi CI của L > 0 VÀ CI của Δρ_A > 0. Đây là đề xuất cho judge phía Gemini, vì D15 thuộc về Gemini.

**N7. Mỗi metric đối tượng ngầm đặt một "ngưỡng tin cậy"** (L1 D-B; trụ cột C1 và C5; N3/R2)
- **Claim.**
  - F1 thô thêm một lần nhắc khi xác suất hậu nghiệm > F/2.
  - F_β đặt ngưỡng F_β/(1+β²); F0.5 của THRONE đòi 0,8·F.
  - Residual ở số lượng khớp đòi khoảng b·P_f, tức gấp đôi ngưỡng của F1.
- **Bằng chứng.** Lý thuyết này giải thích D12 (PLAN-F1 chỉ làm dịch số lượng):
  - dấu đúng ở 73/77 và 74/77 bước trên đường cong của M6;
  - F1 của vote toàn cục đạt cực đại tại m = 3,21, trùng điểm bất động của PLAN-F1.
- **Liên hệ.** Đây là dạng cụ thể cho đối tượng của "ngưỡng tin cậy tường minh" mà Kalai và cộng sự (2509.04664) đề xuất.

**N8. Định lý nhỏ: thành phần A (xếp hạng) của CAR bằng 0 với mọi quyết định Bayes dựa trên chính điểm số của đối chứng** (L1 D-A; trụ cột C1; N2/R1)
- Về bản chất, kết quả này đã có (nguyên lý xếp hạng xác suất cho F-measure). Phần mới chỉ là dùng nó như một quy tắc phân loại phương pháp.
- Chỉ những phương pháp đưa thêm bằng chứng mới có thể có A > 0: M1 grounding, hoặc probe với AUROC 0,807. Vì vậy GPU nên ưu tiên M1, không ưu tiên các luật chọn khác.

### 4.3 Nhóm C: tổng quát hoá ra ngoài KTVIC

**N9. Bảng xếp hạng ở số đối tượng khớp cho các phương pháp HUẤN LUYỆN chống ảo giác** (L6 D1; trụ cột C1; N4/R2; khoảng 6 GPU-h)
- **Cách làm.** Giải mã 9 checkpoint LLaVA-1.5-7B công khai (POVID, RLAIF-V, HALVA, CHAIR-DPO, SENTINEL, HA-DPO, HSA-DPO, OPA-DPO, …) trên CHAIR-500, rồi chấm bằng MCP, tie-avg và CAR.
- **Dự đoán.**
  - Phần lợi ích do số lượng lớn hơn so với các phương pháp giải mã (E1).
  - Dữ liệu có câu chosen ngắn hơn (dk ≤ −0,25) làm giảm số lớp nhiều hơn.
  - HALVA (hoán đổi giữ nguyên số lượng) có |dm| ≤ 0,15.
- **Đánh giá.** Novelty cao nhất trong R11. Tổng quát hoá E1 từ giải mã sang huấn luyện.

**N10. Luật dấu câu × IDF của CIDEr-D trên nhiều ngôn ngữ** (L5 D1; trụ cột C4; N2/R2)
- **Pilot XM3600** (36 ngôn ngữ, chỉ caption của người):
  - hệ số Spearman giữa tỉ lệ ref có dấu câu cuối và mức thay đổi CIDEr là 0,81;
  - dấu của hiệu ứng nhất quán ở mọi ngôn ngữ;
  - ngưỡng đăng ký trước "≤ −15%" sai (2/19 ngôn ngữ), nên chỉ giữ claim về dấu.
- **Dự đoán tiếp.** Trên KTVIC, mức phạt sâu dần khi số ref tăng. Trên UIT-ViIC (98% ref kết thúc bằng " ."), thêm dấu chấm làm CIDEr TĂNG.

**N11. Kiểm toán bộ so khớp đối tượng (matcher) theo từng bộ dữ liệu** (L5 D2; trụ cột C4, cùng C1; N3/R2; 0 GPU)
- **Bằng chứng trên UIT-ViIC.**
  - Theo một đọc từ vựng [MH, chỉ làm động cơ], 23/33 "ảo giác" là do matcher.
  - Bảng v3 rút từ KTVIC chỉ sửa được 10 (6 'quả', 4 'cầu'). CHAIR_i chỉ giảm từ 8,97% xuống 8,16%.
  - 'đứa trẻ' ×6 vẫn bị tính là ảo giác, vì ref viết 'cậu bé' mà từ này không có trong lexicon 113 mục.
  - Đổi v2 sang v3 làm lật thứ hạng giữa P1_s43 (chuyển giao) và zero-shot trên UIT-ViIC (điểm ước lượng, chưa có CI).
- **Cách sửa.** Rút bảng danh từ chỉ vai trò và trẻ em (cầu thủ, vận động viên, cậu bé, …) từ train UIT-ViIC, rồi đóng băng.

**N12. Hai thí nghiệm về Goodhart** (L4 D1 và D2; trụ cột C3)
- **D1: Goodhart dạng hồi quy hay dạng cực trị, tách theo metric dùng để chọn.**
  - Với chọn theo đối tượng: κ gần như không đổi theo n và xấp xỉ κ_lin 0,30, tức dạng hồi quy.
  - Với chọn theo n-gram: có thêm phần cực trị.
  - Chạy trên pool E6 P1 (2 GPU-h, đã có trong kế hoạch).
- **D2: đường WiSE-FT trên hai gold.** Dùng output 59_wise_ft đã nằm trong hàng đợi, 0 GPU-h thêm. Câu hỏi: đoạn cuối của fine-tune có chỉ mua thêm "tính điển hình" hay không.

### 4.4 Nhóm D: tốn hơn hoặc rủi ro cao, để sau

- **L6 D3: chạy M3 trên dữ liệu công khai tiếng Anh**, bằng DPO trên tập con khớp số lượng. Khoảng 10 GPU-h, rủi ro 4: bộ nhớ của 3090 và hiện tượng dịch chuyển likelihood.
- **L5 D3: cặp tối thiểu về loại từ** (vi/zh/ja/th) cho matcher và VLM. 0,3 CPU-h cộng khoảng 1 GPU-h.
- **L2 D4: nhiễu nhãn trong cặp ưu tiên khi gold không đầy đủ.** Liên hệ với N3.
- **L2 D2: precision hiệu chỉnh Chao.** Chỉ chạy trên các bộ tham chiếu hoán đổi được (COCO, UIT-ViIC).
- **L2 D1: thẻ độ đầy đủ gold**, chỉ khi đặt thành kiểm định "thứ hạng có lật không".
- **L1 D-D: F1 có trọng số propensity.** Rủi ro 4.

---

## 5. Rủi ro trùng ý tưởng, cập nhật sau R11

| Hạng mục | Rủi ro | Công trình phải trích dẫn và cách viết |
|---|---|---|
| C1 đánh giá ở số lượng khớp + CAR | THẤP | Nhiều nhóm đã nhận ra yếu tố nhiễu này (LeHaCE, SumGD, CAS, DSCC, CheXalign, "Beyond Saying Less" 2609.35294), nên KHÔNG được nhận ý tưởng chung. Chỉ claim: khớp số lượng theo từng ảnh, biên đăng ký trước, CAR, chấm lại output của nhóm khác. Số cặp sống sót của E1 phụ thuộc đối chứng: 2/15 (Holm + SESOI, khớp giữ thứ tự) đến 6/15 (tập con ngẫu nhiên). Phải nêu đối chứng và báo cả đường đặc tả (RV3) |
| Quy tắc p_marg > F1/2 (G2) | CAO | Lipton và cộng sự 2014, Định lý 1 và Hệ quả 1. Trình bày như một hệ quả |
| C2 luật biên theo gold | THẤP–TRUNG BÌNH | Chen và cộng sự 2015, mục 4.2 (precision của người theo k ref). Trình bày b_pool như sự tổng quát hoá của mục 4.2 |
| C3 bản đồ hai gold, κ, G | THẤP về công cụ, TRUNG BÌNH về khung | "Accuracy on the line" 2107.04649; 2106.15831; 2004.06063; các bài RL 2026 có bộ chấm độc lập (2610.05425, 2605.12474, 2608.11669); Kovacs và cộng sự 2411.03524 (MBR với metric X bị đánh giá cao quá mức) |
| C4 matcher loại từ, ViPOPE+ | THẤP | Chưa có benchmark ảo giác hình ảnh tiếng Việt |
| C4 "tách từ làm đổi CIDEr tiếng Việt" | TRUNG BÌNH | ViTextCaps 2604.27712 |
| C4 chữ ký giao thức | CAO | sacreBLEU, SacreEOS 2305.12254. Chỉ trích dẫn, không claim |
| E2 tách FP thành 3 phần | TRUNG BÌNH | ReaL, RePOPE 2504.15707, Jain 2016/2017 (PU, propensity) |
| E5 k* | TRUNG BÌNH | Resnick v3, App. G. Dùng Chao–Jost làm phương pháp chính. KTVIC là một người viết, nên chỉ panel có đơn vị "người" |
| M3 CM-DPO | TRUNG BÌNH | HALVA (hoán đổi giữ số lượng), RLAIF-V (lọc độ dài), mDPO, "Beyond Saying Less". Thu hẹp claim về: luật cặp cùng số lượng, bổ đề triệt tiêu, đối chứng vote, kiểm định biên |
| M5 ngân sách đối tượng | THẤP về khung, CAO về phương pháp | 2101.08000 (điều khiển số danh từ), LaBERT, CaptionSmiths |
| M6 phân bổ toàn tập | THẤP về đánh giá | Bản thân luật phân bổ là lý thuyết F-measure chuẩn (Lipton, Ye, Koyejo, Schultheis). P-M6b trên test THẤT BẠI. RV3 đã tính lại: gộp +0,65 [−0,02; +1,34] theo luật M6, +0,47 [−0,24; +1,21] so với (v,g) tie-avg; thành phần phân bổ ≈ 0. Luật đã cố định trong commit 6c647a6, 44 giây trước lần nhìn test, nhưng không có file prereg |

---

## 6. Đính chính cần đưa vào bài báo và gửi Gemini

1. **KTVIC do một người viết cả 5 câu cho mỗi ảnh** (mục 3.2 bài báo KTVIC). Mọi câu về "người chú thích" trên KTVIC phải sửa:
   - E2, E5, G3;
   - mức con người 1v4 trong Blocker 8 của PD-2;
   - phần "chuỗi diễn giải" MT11 trong D15.
2. **Số liệu dấu câu của E4 trong nhật ký Gemini và trong D15(iv) sai.** L5 tính lại:
   - KTVIC test: 0/2.790 câu tham chiếu có dấu câu nào;
   - P1 short: 0/558 câu kết thúc bằng dấu chấm;
   - zero-shot: 557/558 câu kết thúc bằng dấu chấm;
   - JSON E4 ghi df('.') = 0, và P7 của p1assist_s42 là 148,70.
   - Các số 75,56%, 99,82% và +8,22 không có trong file. Agent review RV3 cũng thấy điều này và đang kiểm tra lại.
3. **Kiểm định X1 P-B kích hoạt luật dừng của chính nó.**
   - Trên các cặp giải mã tiếng Anh, chênh lệch có dấu α_len − α_cnt chỉ là +0,186 P [−0,257; +0,579] (L6, đọc `e1_x1pb_verification.json`).
   - Câu "đơn vị đối tượng tốt hơn độ dài" vẫn đúng khi so phương sai giải thích: R² 0,488 so với 0,053.
   - Nó cũng đúng với trường hợp KTVIC có mật độ đối tượng thay đổi (MBR +2,60 so với −0,14).
   - Nhưng theo tiêu chí đăng ký trước thì claim này không qua trên tiếng Anh, nên phải viết lại câu.
   - Con số "< 2,1% phương sai F1" của Gemini không có trong file.
4. **File kiểm tra trích dẫn của Gemini** (`r10_a4_citation_verification.json`) xác nhận các ID tồn tại, nhưng gắn sai tiêu đề hoặc tác giả ở ít nhất 10 mục:
   - S14-1015 là Yatskar et al.; 1502.04569 là Jas & Parikh; CVPR.2013.101 là Yun et al.; P19-1654 là VIFIDEL, tr. 6539–6550.
   - CLAIM: tiêu đề "…Cross-Lingual Attention Intervention", tác giả đầu Zekai Ye, dịch bằng Google Translate.
   - Tác giả đầu của UIT-OpenViIC là Doanh C. Bui.
   - 2401.16594 được đăng ở ICLR 2024.
   - DOI 10.1145/1571941.1572031 có tiêu đề "Where to stop reading a ranked list?".
   - Koyejo NIPS 2015 không có ID arXiv.
5. **`e6_mt15_verification.md` mâu thuẫn với JSON của chính nó** (L4):
   - giá trị M của A01; câu "43,1% do lạm phát số lượng"; số của A_all;
   - các dòng CIDEr không có nguồn.

6. **Kết quả review 12 hạng mục CPU R10 của Gemini** (RV1–RV3, `.session_backup/2026-10-14/review_gemini_r10/RV*/REVIEW.txt`). Số trong JSON của Gemini tái lập được từ dữ liệu gốc. Lỗi nằm ở phần lời, ở các kết luận viết cứng trong script và ở quản trị. Có 53 đính chính, trong đó những điểm đổi nội dung bài báo là:
   - **Trần con người "đã khử nhiễu Chao2" 0,9468 → 0,8478 là sản phẩm lỗi.** Script ghép các đường U(k) không tương thích, nên b_pool(1) = 1,01. Phải xoá; không ước lượng được trần đã khử nhiễu theo cách này.
   - **G3 H1 bị BÁC ở cặp 4:** 0,0642 [0,027; 0,104] > 0,06. Gemini ghi là PASS.
   - **Đối chứng của E1.** Placebo "hoán vị mệnh đề, 0,00%" và đối chứng dương "phát hiện 100%" không có trong script lẫn JSON. Placebo đã đăng ký (hai seed lấy mẫu của cùng một mô hình) CHƯA chạy.
   - **E3 không phải xác nhận.** Lần nhìn test được ghi "Confirmatory" nhưng không có file prereg và là lần nhìn thứ hai. Luật dừng K4 đã kích hoạt nhưng bị bỏ qua.
   - **r(ρ_A, ρ_I) = 0,81 giữa 36 hệ thống phụ thuộc hai run self-fusion;** bỏ chúng đi chỉ còn 0,45. Độ phân tán giữa các hệ thống nhỏ hơn nhiễu của từng hệ thống, nên với cỡ mẫu này chưa tách được hai trục.
   - **UPE so với đối chứng (v,g) tie-avg** RV1 tính lại được −0,02 [−0,32; +0,27]. Con số −0,12 trong D15-A không có trong JSON nào; kết luận vẫn giữ nguyên.
   - **Ghi sai trong kiểm tra trích dẫn của Gemini.** Gemini cho rằng CapMAS dùng FACTSCORE không cần tham chiếu, nhưng CapMAS §4.2 nói FACTSCORE có dùng tham chiếu. Vì vậy câu của E3 đúng. Báo cáo L3 đang lặp lại ý sai của Gemini, cần bỏ.
   - **Script 52_c đã chạy có hash de34fb04…, khác bản đăng ký trước** a9be0921… (commit 257bc8c). Chỉ Gemini kiểm tra được trên máy GPU. Kết quả F2 của 52_c phải tạm giữ.
   - **Rò rỉ:** 133 ảnh train UIT-ViIC nằm trong tập test COCO Karpathy (59 ảnh trong probe, 8 ảnh trong POPE-500). Adapter huấn luyện trên UIT-ViIC (52_a, 52_b) không được chấm trên COCO probe hay POPE nếu chưa loại các ảnh này.

---

## 7. Phân việc (judge đã duyệt: PD-3, YES 80–95%)

**CPU, giao Gemini, theo thứ tự:**
1. Chạy lại các kiểm tra đã có trong R11: `check_mstar.py` và `check_coco.py` (L1), `adjacency_check.py` (L2), `l3_check.py` (L3), ba công cụ của L4, `xm_punct_pilot.py` và `uitviic_chair_audit.py` (L5), `pairs_count_audit.py` (L6).
2. Mở rộng N1 sang UIT-ViIC.
3. N2 cho mọi bộ dữ liệu.
4. N6: tính L trên phần dư với đối chứng tie-avg của D15(i).
5. N11: bảng UIT-ViIC.
6. N3: thêm RLAIF-V.

**GPU, sau hàng đợi PD-2 hiện tại, chờ judge phía Gemini:**
- N9: bảng xếp hạng phương pháp huấn luyện, khoảng 6 GPU-h.
- N12 D1: dùng pool E6 P1, 2 GPU-h, đã có trong kế hoạch.
- N12 D2: 0 GPU-h, dùng output WiSE-FT.
- L5 D3: khoảng 1 GPU-h.
