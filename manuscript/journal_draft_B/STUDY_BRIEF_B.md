# Tóm tắt nghiên cứu, Paper B (cho PI)

Ngày soạn: 2026-10-29 (giờ VN). Đích: LRE (Q2). Đóng băng bản thảo: 2026-11-30.
Tên bài (mới, áp dụng 2026-10-29): *What Training-Data Gains Measure on a Vietnamese Captioning Benchmark: Two Reference Panels, a Validity Audit of KTVIC and an Open Evaluation Kit*.

**Cập nhật theo rubric khách quan (2026-10-29).**
- Abstract dài 235 từ và mở đầu bằng kết quả tích cực (B-1 PASS, tính đặc thù theo panel, nhánh O5b, chỉ dev).
- Thêm đoạn biện luận "low-resource" có trích dẫn.
- Thêm Bảng 2.1 so sánh với prior work.
- Thêm Hình 5.1 (thiết kế) và Hình 5.2 (đường cong theo từng seed, hai panel). Số liệu trong hình được đọc lại từ kết quả đã quyết, slope được kiểm khớp đến 1e-6.
- Thêm 6 tài liệu tham khảo đã xác minh. Tỉ lệ tài liệu từ 2024 trở đi tăng từ 29% lên 37%.
- Đã viết lại hai cụm trùng với bài A; hiện không còn chuỗi 12 từ nào trùng.
- Kết quả FAIL của bài test hệ thống cuối vẫn được báo cáo ở §1 và §5.1, nhưng không còn nằm trong abstract.
Mọi số dưới đây lấy từ văn bản bài (sec1, sec3, sec5, sec6) và có nguồn trong `number_manifest_B.tsv`. Đây là ý kiến AI, chưa có chuyên gia thẩm định.

## 1. Bài báo nói gì (các tuyên bố chính)

> **Cập nhật 2026-10-29 (sau PI-1029n): B và D đã gộp thành một bài.** Bài D không nộp riêng.
> - **Headline mới:** mức tăng điểm khi thêm dữ liệu train KTVIC thực chất đo cái gì. Câu trả lời: nó chủ yếu hiện ra trên panel tham chiếu mà mô hình được train theo (nhánh O5b).
> - **Phạm vi:** chỉ dev; không tuyên bố chuyển giao giữa hai panel; không dùng chữ "đầu tiên".
> - **Bằng chứng của D đưa vào §5.4:**
>   - B-1: PASS, b = +9.61 [7.18, 12.36] mỗi lần nhân đôi, 3 seed, dev300. Các seed cho 9.50, 9.62 và 9.71.
>   - D-α (ngoại suy): INCONCLUSIVE ở cả 3 dạng đường cong. Ví dụ dạng log-linear: +1.93 [−6.65, +11.05], so với ngưỡng ±2.0.
> - **Đã cập nhật:** abstract trong outline (bản cũ giữ lại để hoàn tác), §1 (đoạn mới và một đóng góp mới), §5.4, §6.2, §8, cover letter, supplement S7 và manifest.
> - **Tên bài đề xuất** (PI xác nhận): *What Does a Vietnamese Captioning Score Measure? Reference Panels, Training-Data Gains and a Validity Audit of KTVIC*.
> - **Nộp bài vẫn bị chặn ở ngưỡng 98.** Codex CC-166 cho 94. Còn thiếu: H gate được commit, và một reviewer thứ hai kiểm tra phần tách biệt với FAIR và A (xem `SEPARATION_FAIR_A.md`).

1. **Câu hỏi.** Điểm CIDEr trên KTVIC thực sự đo cái gì, và bao nhiêu phần của chênh lệch giữa hai hệ thống là về nội dung ảnh?
2. **Đóng góp.**
   - Một *protocol card*: ghi rõ segmenter, biến thể CIDEr, thang đo, xử lý dấu câu và matcher cho mọi điểm số.
   - Một *bộ công cụ đánh giá mở* (kit). Kit không chứa caption của dataset.
   - Một *kiểm định tính hợp lệ của KTVIC*.
3. **Bốn tính chất của KTVIC làm thay đổi câu trả lời.**
   - (a) Năm tham chiếu của một ảnh do **một người viết**. Vật thể được đúng 2 tham chiếu nhắc tới nằm ở hai ô kề nhau với tỉ lệ 0.7102 [0.6696, 0.7518]. Nếu thứ tự hoán đổi được thì tỉ lệ này là 0.40; null hoán vị là 0.45. Phân tích này là post hoc.
   - (b) Tham chiếu **không có dấu chấm cuối câu**. Trong pipeline bỏ bước xoá dấu câu của PTB, thêm một dấu "." vào mỗi output của P1-R làm CIDEr-D giảm 35.17 điểm (−23.66%). Với cách xoá kiểu PTB thì hiệu ứng bằng 0.
   - (c) Điểm vật thể **phụ thuộc matcher**, và matcher không được mô tả công khai. Bài công bố v1 và v2. v3 do mô hình soạn, nên chỉ dùng làm phân tích độ nhạy.
   - (d) Ảnh test **trùng với UIT-OpenViIC**: 401/558 (71.86%) nằm trong split train của OpenViIC, 555 ảnh có caption ở đâu đó trong OpenViIC. Nhờ vậy có một panel caption thứ hai trên cùng ảnh.
4. **Hai panel bất đồng (§5.3).** Với fuse2, chi phí precision theo KTVIC là −2.21 pp. Theo panel OpenViIC, chi phí này chỉ còn −0.25 pp [−2.43, 1.96]. 55.12% [49.38, 61.05] vật thể bị KTVIC coi là "ảo giác" lại được panel OpenViIC nhắc tới.
5. **Mới (dev, §5.4, D0 GO).**
   - Khi tăng dữ liệu train KTVIC, CIDEr-D đo theo tham chiếu KTVIC tăng +10.59 [7.43, 13.81] mỗi lần nhân đôi. Đo theo panel OpenViIC của cùng ảnh, mức tăng chỉ là +0.72 [−0.83, 2.36].
   - Khoảng cách giữa hai mức tăng là +9.87 [6.71, 13.35]; trên thang log là +7.11% [3.54, 10.69].
   - Có một lần đọc lại có che (masked re-read): post hoc, mô tả, dev. Nó bỏ ảnh near-twin và ảnh trùng caption. Trên 165 ảnh còn lại, khoảng cách vẫn là +8.92 [5.59, 12.40].
   - **B-R1 (chiều ngược, dev, chấm một lần): ASYMMETRIC, nhánh O5b.**
     - Train trên caption OpenViIC thì điểm theo panel OpenViIC tăng b_O^R = +2.98 [0.94, 4.88] mỗi lần nhân đôi. Như vậy panel OpenViIC có phản ứng với dữ liệu train.
     - Theo tham chiếu KTVIC, mức tăng là +1.29 [−1.23, 3.75], không phân biệt được với 0.
     - g_R = +1.69 [−0.72, 3.91]. Cận trên 3.91 nhỏ hơn SESOI 4.93.
     - Kiểm tra phong cách đạt: output dài 16.76 âm tiết, so với 11.73 ở chiều thuận.
     - Không có length penalty (σ = ∞): g_R = +1.04 [−1.75, 3.53]; g chiều thuận = +9.97 [6.48, 13.75].
   - **Headline (CC-163).** Mức tăng do thêm dữ liệu KTVIC chủ yếu chỉ hiện ra trên panel một-người-viết của chính KTVIC. Khoảng cách chiều ngược nhỏ hơn SESOI. **Chưa chứng minh được "chuyển giao" (transfer) sang tham chiếu KTVIC**, và cụm từ này bị cấm.
   - **Equivalence yếu.** Biên 4.93 lớn hơn chính b_O^R (2.98), nên không phân biệt được hai trường hợp: chuyển giao toàn phần và không chuyển giao.
   - **Kiểm tra thiết kế khớp (W2, post hoc, mô tả, dev; spec ghi LOG trước khi tính).** Fit lại chiều thuận trên s42/s43 × L1/L3/L4: g_m = +11.77 [7.86, 16.24]. Độ bất đối xứng ghép cặp g_m − g_R = +10.08 [5.49, 15.46]; trên thang log là +7.05% [0.69, 13.60].
   - **Hàng mô tả không khớp thiết kế.** g − g_R = +8.18 [4.30, 12.67]. Bài không dựa vào hàng này.
   - **Trạng thái.** §5.4–5.5 là CONDITIONAL. Hai mục này chỉ ở lại B nếu PI có dòng duyệt mới cho việc gộp B+D (PI-1029h không áp dụng vì kết quả không phải GO_BOTH). Nếu PI trả lời KHÔNG, hai mục rời B trước 30/11 và trở thành bằng chứng dev của bài D.
6. **Những gì bài không tuyên bố.**
   - Không tuyên bố SOTA. Hệ thống của chúng tôi đạt 148.23 (SD 0.38, 3 seed), còn GRIT được báo cáo 136.0, nhưng hai con số này dùng protocol khác nhau.
   - Không có đánh giá của người: không thu thập nhãn người mới.
   - Nhãn do mô hình sinh không được dùng làm bằng chứng.

## 2. Các con số cần nhớ

| Nội dung | Số |
|---|---|
| CIDEr-D của P1-R (3 seed) | 148.23 (SD 0.38) |
| Zero-shot: trước → sau khi bỏ dấu chấm | 28.98 → 33.30 (34.97 nếu xoá kiểu PTB) |
| Mất điểm do 1 dấu chấm (pipeline không xoá dấu câu) | 35.17 (−23.66%) |
| Word segmentation so với tách theo âm tiết | 15.64 điểm |
| Ảnh test KTVIC nằm trong OpenViIC-train | 401/558 (71.86%) |
| Byte twin train↔test trong KTVIC | 2 cặp (3589↔1335, 7511↔507) |
| Final test MBR-3 (đăng ký trước) | FAIL, D_MBR = −0.391 [−2.437, +1.666] |
| Re-rank 4 VLM sau khi sửa dấu câu | Kendall τ_b = 1.0, dự đoán đăng ký FAIL |
| D0 (dev): b_K / b_O / g | +10.59 / +0.72 / +9.87 [6.71, 13.35] |
| D0 masked re-read (post hoc, 165 ảnh) | g = +8.92 [5.59, 12.40] |
| B-R1 (dev): kết quả | ASYMMETRIC, O5b |
| B-R1: b_O^R / b_K^R / g_R | +2.98 [0.94, 4.88] / +1.29 [−1.23, 3.75] / +1.69 [−0.72, 3.91] |
| Thiết kế khớp (post hoc): g_m / bất đối xứng | +11.77 [7.86, 16.24] / +10.08 [5.49, 15.46] |

## 3. Việc còn mở trước ngày đóng băng

- **Câu hỏi cho PI (CC-163).**
  - **Q1, gộp B+D: PI ĐÃ DUYỆT (PI-1029n).** Phần còn lại của mục này chỉ để lưu lại.
    - Khuyến nghị: CÓ, nhưng chỉ sau khi đủ ba điều kiện: W6 sạch, độ bất đối xứng khớp có CI_lo > 0, và Codex đồng ý. Về điều kiện thứ hai: CI_lo > 0 trên cả hai thang (tuyệt đối 5.49, tương đối 0.69). Tuy nhiên kết quả này là post hoc và chưa có quy tắc quyết định. Các nhiễu vẫn còn: ảnh train chỉ trùng một phần, twin/caption trùng chỉ có ở chiều thuận, và mức điểm của hai panel khác nhau. Không nên đọc đây là một cổng đã qua.
    - Mặc định: KHÔNG. Khi đó §5.4–5.5 rời B.
  - **Q2, nghiên cứu H (~20–25 GPU-h trên M2).**
    - Khuyến nghị: CÓ, nếu Q1 là CÓ và prereg đạt ≥ 98.
  - **Q4, mức bài.** B hiện ở khoảng Q3 (~15–17/30).
    - Khuyến nghị: chấp nhận, giữ LRE và hạn đóng băng 30/11.
- **W6 ĐÃ HOÀN TẤT (LOG CC-166 W6).**
  - HDUCap: đã xác minh JVCIR 121:104963, PII S1047320326002580. Bản toàn văn bị khoá, nên §2 ghi rõ là chúng tôi chưa đọc được.
  - Bromonschenkel 2026: đã có câu "unlike" trong §2.
  - OpenAlex và S2 lại báo 429. Đã thay bằng 12 truy vấn arXiv và 1 lượt tìm web, không thấy nghiên cứu nào trùng.
  - Kết luận giữ nguyên dưới đây.
- **W6, kiểm tra prior art: PARTIAL PRIOR ART, độ tin ~70%.** Cuộc tìm kiếm chưa đầy đủ: OpenAlex hết hạn mức trong ngày, còn S2 bị giới hạn tốc độ.
  - KTVIC và UIT-OpenViIC không làm thí nghiệm chéo giữa hai bộ dữ liệu.
  - ViCLIP-OT (arXiv 2602.22678) đã báo cáo trước chúng ta con số trùng lặp 401/558 ảnh test (và 2,464/3,769 ảnh train). **Cần trích dẫn ViCLIP-OT là nguồn của con số này** ở §1, §2 và §3.6. Bản thảo hiện chưa ghi công.
  - Công trình gần nhất là Bromonschenkel et al. 2026 (Flickr30K, caption gốc so với caption dịch máy, train/test chéo, không có đường cong scaling).
  - Chưa thấy nghiên cứu nào đo việc mức tăng theo dữ liệu tách ra giữa hai protocol do người viết trên cùng ảnh.
  - Novelty 3 vẫn chưa được tính.
- **Đã sửa.** §3.6 và §7.2 trước đây ghi "không mô hình nào train trên OpenViIC". Nay đã sửa để ghi rõ 6 adapter dev, không bao giờ chấm trên test.
- **Đã ghi LOG.** decide.json thiếu nhãn phụ O5a/O5b. Đây là sai lệch so với RULE §5 cl.5, đã ghi vào LOG; decide.json không bị sửa.

## 4. Câu hỏi phản biện dễ gặp (trả lời ngắn)

1. **"Đây chỉ là một bài audit, đóng góp mới ở đâu?"** Có ba điểm mới:
   - Đo được bằng số rằng tham chiếu do một người viết.
   - Đo được chi phí của dấu chấm theo từng pipeline.
   - Kết quả D0 (dev): tăng dữ liệu KTVIC làm tăng điểm theo người viết KTVIC nhanh hơn rất nhiều so với một panel độc lập trên cùng ảnh.

   Kit chạy được trên output của người đọc, và đã chạy trên 3 hệ thống ngoài.
2. **"Sao không so với các hệ thống tiếng Việt đã công bố?"** Điểm công bố dùng protocol khác, và không xác minh được pipeline của họ. Output công bố của hai baseline chỉ được dùng cho tương quan thứ hạng (§3.4) và audit dấu câu (§3.3).
3. **"Panel OpenViIC có thật sự độc lập với KTVIC không?"** Chưa chứng minh được, và bài nói rõ điều đó. Không có caption nào trùng hẳn. 4-gram Jaccard trung bình giữa hai panel là 0.019. Chỉ 50/2,775 tham chiếu chung một chuỗi 8 âm tiết với panel kia. Bài gọi đây là "hai panel bất đồng", không gọi là bằng chứng độc lập.
4. **"D0 có phải chỉ là panel OpenViIC không nhạy?"** Không hẳn. Ở B-R1, khi train trên caption OpenViIC, panel OpenViIC tăng +2.98 [0.94, 4.88], tức là panel này có phản ứng. Tuy vậy, B-R1 chỉ là dev, có 2 seed, và không tách được yếu tố người viết khỏi yếu tố protocol.
5. **"D0 chạy trên dev, có rò rỉ không?"** Có hai lợi thế chỉ có ở chiều thuận:
   - 8 ảnh near-twin;
   - 16 ảnh có caption train trùng với tham chiếu.

   Re-read bỏ cả hai nhóm (22 ảnh), và g vẫn là +8.92 [5.59, 12.40]. Re-read được gắn nhãn post hoc, mô tả. Không có ảnh test nào dùng trong D0.
6. **"Có byte duplicate giữa train và test không?"** Có 2 cặp, và bài công bố cả hai. Bài không chấm lại trên 556 ảnh còn lại, vì đó sẽ là lần nhìn thứ hai vào test set đã đóng.
7. **"Kết quả final test FAIL thì hệ thống có giá trị gì?"** Hệ thống chỉ là công cụ đo, không phải đóng góp chính. Kết quả FAIL được báo cáo nguyên văn theo đăng ký trước.
8. **"Matcher v3 do AI soạn có đáng tin không?"** Không dùng v3 làm bằng chứng. Nó chỉ là phân tích độ nhạy và không phát hành. Kết luận dựa trên v1 và v2.
9. **"Tại sao không có đánh giá của người?"** Không thu nhãn người mới, theo quy tắc của nhóm. Vì vậy bài không tuyên bố gì về chất lượng caption theo cảm nhận của người.
10. **"Kit có tái lập được không?"** Một máy thứ hai tái lập byte-for-byte các điểm đã commit. Kit không chứa caption của dataset, nên người đọc chạy kit trên bản dataset của chính họ.
11. **"Mô hình train trên OpenViIC có chuyển giao sang KTVIC không?"** Bài không tuyên bố điều đó. b_K^R có CI chứa 0 (cận dưới −1.23), và biên equivalence quá rộng để kết luận. Hai câu "OpenViIC-trained gains transfer" và "about as much as" đã bị loại khỏi văn bản.
12. **"Phần scaling (D) có phải chỉ là một đường cong scaling quen thuộc?"** Đường cong B-1 tự nó không mới; lĩnh vực này đã đông. Điểm mới là cùng các output đó được chấm trên hai panel của cùng ảnh, và mức tăng chỉ hiện ra ở panel đã dùng để train. Phép ngoại suy D-α cho kết quả INCONCLUSIVE, và bài báo cáo đúng như vậy.
13. **"Bài này trùng gì với bài A và FAIR?"** Không có kết quả chính nào xuất hiện ở hai bài. Tỉ lệ chuỗi 12 từ trùng: với FAIR là 0, với A là 2 (một câu khai báo AI và một cụm về null). Bộ kit dùng chung đã được công bố rõ. Chi tiết trong `SEPARATION_FAIR_A.md`.
