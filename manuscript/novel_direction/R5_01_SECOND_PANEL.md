# R5-01: Panel người thứ hai cho KTVIC test (UIT-OpenViIC)

12/10/2026. Script `scripts/match_openviic.py` (ghép ảnh) và `scripts/second_panel.py` (phân tích). Số liệu: `data/ktvic_openviic_refs.json`, `data/results/second_panel.json` (B = 5000). Chỉ dùng caption người đã công bố (KTVIC, UIT-OpenViIC). Không gán nhãn mới, không dùng nhãn AI.

## Kết luận

1. **Ảnh KTVIC là ảnh của kho UIT-OpenViIC.** KTVIC lấy ảnh từ UIT-EVJVQA và giữ nguyên số hiệu file, OpenViIC dùng cùng kho đó. Khớp theo nội dung (pHash hoặc dHash ≤ 10, kể cả bản lật gương, **và** SSCD ≥ 0.5), cả 558/558 ảnh test và 3768/3769 ảnh train đều có bản sao trong 13 300 ảnh của OpenViIC. Ảnh train còn lại không khớp vì file OpenViIC bị cắt cụt. **555/558 ảnh test có bản sao kèm caption**, trung bình 5.39 caption mỗi ảnh. Kiểm bằng mắt 72 cặp (36 ngẫu nhiên và 36 cặp yếu nhất): cả 72 đều là cùng một bức ảnh, cận dưới 95% (một phía) của precision là 95.0%.
2. **Con số của ViCLIP-OT được tái lập, nhưng nó chỉ đếm OpenViIC train.** 401/558 ảnh test có bản sao trong OpenViIC train, khớp đúng 401 của ViCLIP-OT (theo luật hai tín hiệu của ta, và theo luật của họ: SSCD ≥ 0.8). Với train: 2459 (luật hai tín hiệu) hay 2461 (SSCD ≥ 0.8), họ báo 2464. 154 ảnh test còn lại nằm trong OpenViIC dev/test, nên panel thứ hai phủ 555 ảnh chứ không chỉ 401.
3. **Hai panel độc lập về người viết.** OpenViIC do 51 sinh viên UIT viết, theo quy định "ít nhất 10 từ, tả mọi thông tin thị giác". KTVIC do nhóm khác viết, theo hướng dẫn riêng. Trên 555 ảnh test không có caption nào trùng nguyên văn giữa hai bộ. 19% caption KTVIC có chung một 5-gram với panel OpenViIC của cùng ảnh (1.4% với ảnh khác): đó là từ ngữ chung khi tả cùng một cảnh, không phải chép. Caption OpenViIC dài hơn (17.5 so với 12.1 từ) và nhắc nhiều lớp object hơn (6.0 so với 3.7 lớp mỗi ảnh).
4. **Khoảng cách P giữa fuse2 và P1 giảm một nửa khi gold đầy đủ hơn.** P (khớp đúng) của fuse2-detailed là 67.8 khi so với 5 ref KTVIC và 85.3 [83.6, 87.0] khi so với hợp hai panel. ΔP (fuse2 − P1, cùng ảnh) đi từ −10.4 [−13.0, −7.8] xuống −5.2 [−7.1, −3.2]. Ở short, −2.2 (p = 0.10) thành −1.1 [−3.0, +0.9]. Với gold hợp, fuse2 vẫn hơn P1 về F1: +15.1 (detailed), +4.5 (short), p < 0.001.
5. **Panel độc lập xác nhận mention "sai theo KTVIC" của fuse2 với cùng tỉ lệ như của P1 và của một người.** Xét các mention không nằm trong 5 ref KTVIC. Phần được OpenViIC nhắc tới là 55.1% [49.4, 61.0] với fuse2-short, 54.4% [50.4, 58.5] với fuse2-detailed, 55.7% và 56.6% với P1, và 58.8% [54.9, 62.5] với một người KTVIC bị giữ lại (1v4). Δ(fuse2 − P1) là −0.5 (short) và −2.1 [−8.2, +4.0] (detailed); theo luật hypernym là −0.3 và −0.6. Chỉ khi so với seed p1_s44-detailed (62.2%) thì chênh lệch có ý nghĩa: −7.8, p = 0.013. Coi tỉ lệ của người là độ nhạy của panel, thì phần mention có thật ước khoảng 96% [88, 105] với fuse2-detailed, 97% với fuse2-short và 97–108% với P1. Zero-shot detailed chỉ đạt 57% [53, 62].
6. **Độ dài vẫn có giá thật.** Mỗi caption fuse2-detailed có thêm 0.29 [0.24, 0.34] mention mà không panel nào xác nhận (0.46 so với 0.17 của P1). Ở fuse2-short con số này là +0.05. Đây là cận trên của ảo giác, vì hai panel cộng lại chỉ phủ khoảng 84% số object nhắc được (mục 6).
7. **So với một người trên gold "4 KTVIC + OpenViIC" (1v4).** Người đạt P 94.0. fuse2-short có ΔP −5.7, ΔR +3.1 và ΔF1 +3.1 [1.5, 4.6] (p < 0.001), tức là **vượt một người về F1**. Trên gold chỉ gồm 4 caption KTVIC thì nó thua (ΔF1 −2.3, R4-01). P1-short có ΔP −4.7, ΔF1 −1.4 (p = 0.049). Khoảng cách P giữa model và người co từ 10–12 điểm (gold KTVIC) xuống 3–6 điểm.
8. **Capture-recapture.** Mỗi ảnh có khoảng 8.35 [8.05, 8.66] lớp object (trong lexicon) "nhắc được", theo Chapman gộp ảnh. Recall của panel KTVIC (5 caption) là 44.5%, của panel OpenViIC 71.9%, của hợp hai panel 84.4%. Ở mức lớp thô (gốc hypernym) là 6.93 lớp và 49.0 / 74.5 / 87.0%. Cả hai panel cùng ưu tiên object nổi bật (phụ thuộc dương), nên N bị ước thấp và các recall này là cận trên.

## 1. Dữ liệu

- **UIT-OpenViIC** (Bui, Nguyen, Nguyen; arXiv 2305.04166; Signal Processing: Image Communication 140:117430, 2026) có 13 100 ảnh và 61 241 caption: train 9088/41 238, dev 2011/10 002, test 2001/10 001. Bản chính thức nằm ở https://github.com/nghiangh/UIT-OpenViIC-dataset (commit e3bf744): `images.zip` (Drive `1eRWL751fGv4WPTg0dhBGMRbcUgh9xKA5`, 3 805 342 476 byte, sha256 `2da7e81f…`, 13 300 file, trong đó 200 file không có caption và 4 file bị cắt cụt) và ba file `uit-openviic-annotation-{train,dev,test}.json`. Thư mục Drive ghi trên trang https://uit-together.github.io/datasets/UIT-OpenViIC/ trả 404. **Điều khoản:** "available online for non-commercial research" (arXiv), "publicly available for research purposes" (README); không có file license. Ảnh là ảnh crawl từ Google/Bing nên bản quyền thuộc chủ ảnh. Dữ liệu nằm ở `data/datasets/openviic/` (bị gitignore) và `n3:/root/ncs-data/datasets/openviic/`.
- `data/ktvic_openviic_refs.json` chứa nguyên văn caption OpenViIC. **Không đẩy file này lên repo công khai** khi chưa hỏi tác giả: điều khoản không nói gì về việc phân phối lại.

## 2. Ghép ảnh

| | KTVIC test | KTVIC train |
|---|---|---|
| có bản sao trong OpenViIC (luật hai tín hiệu) | 558/558 | 3768/3769 |
| có bản sao kèm caption | 555 | 3724 |
| có bản sao trong OpenViIC train (luật hai tín hiệu) | 401 | 2459 |
| luật ViCLIP-OT: SSCD ≥ 0.8 với một ảnh OpenViIC train | 401 | 2461 |
| ViCLIP-OT báo cáo | 401 | 2464 |
| bản sao theo split OpenViIC (một ảnh có thể có nhiều bản) | train 401, dev 96, test 72, không caption 3 | train 2459, dev 831, test 575, không caption 48 |

- SSCD dùng `sscd_disc_mixup` (TorchScript, tiền xử lý small_288, cạnh dài tối đa 1152), cosine. Hash là imagehash 4.3.2 64 bit. Phần nhúng chạy trên CPU của n3. Có 4660 cặp khớp, trong đó 4325 là cặp cùng tên file; với các cặp này pHash ≤ 2 ở phân vị 99 và SSCD ≥ 0.96 ở phân vị 1. 335 cặp khác tên là ảnh trùng ngay trong kho OpenViIC (một ảnh test có tới 4 bản).
- **Ca biên** (kiểm bằng mắt, không đưa vào khớp). 12 cặp chỉ có hash gần (dHash 5–6, SSCD < 0.15) đều là 12/12 ảnh khác nhau, tức hash một mình không đủ. Với cặp chỉ có SSCD cao (hash > 10): ở mức SSCD ≥ 0.8, 11/12 là cùng ảnh bị cắt khung mạnh; ở 0.7–0.8 là 8/12; ở 0.5–0.7 là 0/24 (cùng địa danh hay cửa hàng nhưng là ảnh khác). Như vậy luật hai tín hiệu bỏ sót 52 bản trùng bị cắt mạnh trong kho (SSCD ≥ 0.8, 50 trong số đó thuộc ảnh KTVIC train), nhưng 51 trong 52 ảnh KTVIC đó đã khớp một bản khác. Hash không bất biến khi lật ảnh nên phải hash thêm bản lật gương; việc này thêm 11 cặp.

## 3. Object P/R/F1 với ba gold (555 ảnh)

Gold là hợp các lớp `objects_in` trong (a) 5 ref KTVIC, (b) panel OpenViIC, (c) hợp hai panel. Số liệu dùng `object_prf.image_counts/scores`. CI 95% của P theo gold hợp nằm trong ngoặc.

| short | P KTVIC | P OpenViIC | P hợp | R KTVIC | R hợp | F1 KTVIC | F1 hợp |
|---|---|---|---|---|---|---|---|
| p1-gold | 77.9 | 78.6 | 90.2 [88.2, 92.0] | 41.5 | 24.7 | 54.1 | 38.7 |
| p1_s43 | 78.7 | 78.6 | 90.7 [88.8, 92.6] | 41.8 | 24.9 | 54.6 | 39.1 |
| p1_s44 | 78.8 | 79.3 | 91.2 [89.3, 92.9] | 42.5 | 25.1 | 55.2 | 39.3 |
| fuse2_s42 | 75.7 | 78.3 | 89.1 [87.2, 90.9] | 47.2 | 28.6 | 58.1 | 43.3 |
| tags_fuse2_s42 | 77.8 | 77.7 | 89.9 [88.0, 91.7] | 46.7 | 27.7 | 58.4 | 42.4 |
| e5_s42 | 75.0 | 78.3 | 88.7 [86.8, 90.7] | 46.3 | 28.2 | 57.2 | 42.9 |
| e5dpo_s42 | 73.0 | 77.5 | 88.4 [86.5, 90.2] | 43.9 | 27.3 | 54.8 | 41.8 |
| zeroshot | 52.2 | 70.8 | 76.2 [73.7, 78.5] | 32.5 | 25.0 | 40.1 | 37.6 |

| detailed | P KTVIC | P OpenViIC | P hợp | R KTVIC | R hợp | F1 KTVIC | F1 hợp |
|---|---|---|---|---|---|---|---|
| p1-gold | 78.3 | 79.0 | 90.6 [88.6, 92.4] | 42.8 | 25.3 | 55.3 | 39.5 |
| p1_s43 | 79.8 | 79.7 | 91.4 [89.6, 93.1] | 42.4 | 24.9 | 55.4 | 39.2 |
| p1_s44 | 78.4 | 79.8 | 91.8 [90.1, 93.5] | 43.3 | 25.6 | 55.8 | 40.0 |
| fuse2_s42 | 67.8 | 74.4 | 85.3 [83.6, 87.0] | 61.2 | 40.2 | 64.4 | 54.7 |
| tags_fuse2_s42 | 70.6 | 74.6 | 86.2 [84.4, 87.9] | 59.7 | 38.1 | 64.7 | 52.8 |
| e5_s42 | 67.2 | 73.5 | 84.3 [82.7, 86.0] | 62.2 | 41.0 | 64.6 | 55.2 |
| e5dpo_s42 | 69.2 | 74.3 | 86.1 [84.3, 87.8] | 60.8 | 39.7 | 64.8 | 54.4 |
| zeroshot | 31.5 | 48.5 | 53.7 [52.1, 55.2] | 57.1 | 51.3 | 40.6 | 52.5 |

R theo gold hợp thấp vì gold lớn hơn (7.0 lớp mỗi ảnh). Chỉ so các hệ với nhau trên cùng một gold.

## 4. Mention sai theo KTVIC mà panel độc lập xác nhận

"Ref-false" là lớp được nhắc mà không thuộc gold 5 ref KTVIC (khớp đúng). "Xác nhận" nghĩa là OpenViIC có nhắc lớp đó. Cột 1v4 dùng cùng giao thức với người: gold là 4 caption KTVIC còn lại, lấy trung bình 5 fold. Cột "phần thật" bằng tỉ lệ 1v4 của hệ chia cho tỉ lệ 1v4 của người.

| | ref-false/caption | xác nhận % [CI] | chưa xác nhận/caption | 1v4 xác nhận % | phần thật % [CI] |
|---|---|---|---|---|---|
| **1 người KTVIC (1v4)** | 0.26 | | | 58.8 [54.9, 62.5] | (100) |
| p1-gold-short | 0.40 | 55.7 [48.9, 62.5] | 0.18 | 57.2 | 97 [86, 110] |
| fuse2_s42-short | 0.51 | 55.1 [49.4, 61.0] | 0.23 | 57.0 | 97 [86, 108] |
| tags_fuse2_s42-short | 0.45 | 54.6 [48.1, 61.1] | 0.20 | 56.5 | 96 [85, 108] |
| zeroshot-short | 1.04 | 50.2 [45.8, 54.3] | 0.52 | 51.6 | 88 [79, 97] |
| p1-gold-detailed | 0.40 | 56.6 [49.8, 63.1] | 0.17 | 58.4 | 99 [88, 112] |
| p1_s43-detailed | 0.36 | 57.3 [50.2, 64.3] | 0.15 | 59.3 | 101 [89, 113] |
| p1_s44-detailed | 0.39 | 62.2 [55.8, 68.6] | 0.15 | 63.5 | 108 [97, 120] |
| fuse2_s42-detailed | 1.02 | 54.4 [50.4, 58.5] | 0.46 | 56.3 | 96 [88, 105] |
| tags_fuse2_s42-detailed | 0.87 | 53.0 [48.6, 57.3] | 0.41 | 55.0 | 94 [85, 102] |
| e5_s42-detailed | 1.07 | 52.4 [48.5, 56.4] | 0.51 | 54.4 | 93 [85, 101] |
| zeroshot-detailed | 4.49 | 32.4 [30.6, 34.2] | 3.04 | 33.5 | 57 [53, 62] |

Paired (B − A, cùng ảnh, B = 5000):

| B − A | ΔP KTVIC | ΔP hợp | ΔF1 hợp | Δ tỉ lệ xác nhận | Δ xác nhận/caption | Δ chưa xác nhận/caption |
|---|---|---|---|---|---|---|
| fuse2 − p1-gold, short | −2.2 [−4.9, +0.4] p=0.10 | −1.1 [−3.0, +0.9] p=0.28 | +4.5 [3.1, 6.0] p<0.001 | −0.5 [−6.9, +5.9] p=0.88 | +0.06 [+0.02, +0.10] | +0.05 [+0.01, +0.09] |
| fuse2 − p1-gold, detailed | −10.4 [−13.0, −7.8] p<0.001 | −5.2 [−7.1, −3.2] p<0.001 | +15.1 [13.7, 16.5] p<0.001 | −2.1 [−8.2, +4.0] p=0.50 | +0.33 [+0.27, +0.38] | +0.29 [+0.24, +0.34] |
| fuse2 − p1_s43, detailed | −11.9 [−14.6, −9.4] | −6.0 [−7.8, −4.1] | +15.5 [14.1, 16.9] | −2.9 [−9.2, +3.7] p=0.39 | +0.35 | +0.31 |
| fuse2 − p1_s44, detailed | −10.6 [−13.2, −8.0] | −6.5 [−8.4, −4.6] | +14.6 [13.2, 16.1] | −7.8 [−13.7, −1.8] p=0.013 | +0.31 | +0.32 |
| tags_fuse2 − p1-gold, short | −0.1 [−2.7, +2.5] | −0.3 [−2.1, +1.6] | +3.7 [2.2, 5.1] | −1.0 [−7.4, +5.5] | +0.02 | +0.03 |

Cách đọc: fuse2-detailed nhắc thêm khoảng 0.62 lớp mỗi caption mà KTVIC không nhắc. Panel độc lập xác nhận khoảng một nửa số đó (+0.33), cùng tỉ lệ với các mention thừa của P1 và của một người. Vì vậy phần lớn khoảng hụt P của fuse2 theo gold KTVIC là do **gold thiếu**, không phải do một kiểu ảo giác mới. Phần còn lại (+0.29 mention chưa xác nhận mỗi caption) là cận trên của chi phí ảo giác thật khi viết dài.

## 5. 1v4: so với một người, gold = 4 caption KTVIC còn lại + panel OpenViIC

| | P | R | F1 | ΔP so với người | ΔF1 so với người |
|---|---|---|---|---|---|
| **1 người KTVIC** | 94.0 [93.2, 94.8] | 25.6 | 40.3 | | |
| p1-gold-short | 89.4 | 24.8 | 38.9 | −4.7 [−6.7, −2.8] | −1.4 [−2.9, −0.0] p=0.049 |
| fuse2_s42-short | 88.3 | 28.8 | 43.4 | −5.7 [−7.7, −3.8] | **+3.1 [1.5, 4.6] p<0.001** |
| tags_fuse2_s42-short | 89.1 | 27.9 | 42.5 | −5.0 [−6.9, −3.0] | +2.2 [0.6, 3.7] p=0.007 |
| fuse2_s42-detailed | 84.5 | 40.4 | 54.7 | −9.5 [−11.4, −7.8] | +14.4 [12.8, 15.9] |
| zeroshot-short | 75.8 | 25.3 | 37.9 | −18.2 [−20.7, −15.9] | −2.4 [−4.5, −0.3] |

Chỉ dùng 4 caption KTVIC làm gold (như R4-01) thì người hơn fuse2-short 12.5 điểm P và 2.3 điểm F1. Thêm panel thứ hai thì người còn hơn 5.7 điểm P và thua 3.1 điểm F1.

## 6. Capture-recapture hai panel

Mỗi ảnh có n₁ = 3.72 lớp do KTVIC nhắc, n₂ = 6.00 lớp do OpenViIC nhắc, 2.67 lớp chung, hợp là 7.05.

| | N mỗi ảnh (Chapman gộp) | Lincoln-Petersen | Chapman trung bình theo ảnh | recall KTVIC | recall OpenViIC | recall hợp |
|---|---|---|---|---|---|---|
| lớp lexicon | 8.35 [8.05, 8.66] | 8.35 | 8.18 | 44.5 [42.9, 46.1] | 71.9 [69.8, 73.8] | 84.4 [83.0, 85.6] |
| lớp thô (gốc hypernym) | 6.93 [6.70, 7.17] | 6.93 | 6.74 | 49.0 [47.2, 50.7] | 74.5 [72.5, 76.4] | 87.0 [85.8, 88.1] |

Recall tối thiểu của hệ, tính bằng số mention được ít nhất một panel xác nhận chia cho N: P1 khoảng 19.5%, fuse2-short 22.4%, fuse2-detailed 32.3%, zero-shot detailed 42.2%.

## 7. Giới hạn

- **"Chưa xác nhận" không có nghĩa là ảo giác, và "xác nhận" không có nghĩa là có thật.** Hai panel bỏ sót khoảng 16% object nhắc được (đây là cận dưới, vì có phụ thuộc dương). Khớp từ vựng của `objects_in` có thể xác nhận nhầm, ví dụ "bàn tay" bị đọc thành "bàn"; đoán giới tính sai có thể lặp ở cả hai panel. Các sai số này đánh vào người và hệ như nhau.
- Ước lượng "phần thật" giả định panel nhạy với object thừa của hệ như với object thừa của người. Nếu object hệ nhắc thêm kém nổi bật hơn thì ước lượng này thấp hơn thực tế, và ngược lại.
- Hai nhóm người viết khác nhau, nhưng cùng ngôn ngữ và văn hóa, và cùng dùng lexicon 112 lớp. Không đo thuộc tính, quan hệ hay độ trôi chảy.
- 555 ảnh, một split. Kết luận về tỉ lệ xác nhận chỉ là "không phân biệt được" (CI ±6 điểm), chưa chứng minh được là bằng nhau.

Phần 2 của cùng đợt (XM3600 + nhãn image-level đã người kiểm của Open Images V7) đã xếp hàng trên n2 (`/root/queue/39_xm3600_eval.sh`, khoảng 2.7 GPU-h). Xem `scripts/xm3600_oiv7.py` và `data/xm3600/manifest.json`. Caption tiếng Anh của đúng 600 ảnh đó (để đánh giá cặp Việt–Anh) nằm ở `$NCS_DATA/datasets/xm3600_en/` (`images -> ../xm3600/images`); danh sách ảnh ở `data/xm3600_subset.txt`.
