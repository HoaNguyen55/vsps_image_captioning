# R5-03: Các phân tích không cần GPU mà năm verifier yêu cầu (V2–V5)

12/10/2026. Script: `scripts/two_gold_audit.py` (V3), `scripts/nap.py` (V2), `scripts/committee_headroom.py` (V5), `scripts/caption_exchangeability.py` (V4). Số liệu: `data/results/two_gold_audit.json`, `data/results/nap.json`, `data/results/committee_headroom.json`, `data/results/caption_exchangeability.json`. Mọi CI là CI 95% phân vị, lấy mẫu lại ảnh với B = 2000. Các hiệu số có cặp dùng chung lượt lấy mẫu; p hai phía, sàn 2/B = 0.001. Chỉ dùng dữ liệu và nhãn đã công bố: KTVIC, UIT-OpenViIC, UIT-ViIC, nhãn instance COCO-2014, caption tiếng Anh của COCO và Flickr30k Entities. Không gán nhãn mới, không dùng nhãn AI. Không chạy GPU, không nạp VLM/LLM.

V1 (IFCR) đã bị loại nên không port. Các bảng dưới đây không chứa nguyên văn caption OpenViIC.

## Kết luận

1. **Khoảng một nửa chi phí precision của fusion là "điển hình" của nhóm người viết KTVIC.** Trên 3,724 ảnh KTVIC train, target được dựng từ 3 caption và chấm với 2 caption còn lại, lấy trung bình 10 fold. ΔP(fuse2 − p1) là −8.93 [−9.45, −8.42] theo 2 ref KTVIC giữ lại, −4.73 [−5.27, −4.17] theo panel OpenViIC và −4.47 [−4.87, −4.08] theo hợp hai panel (cả ba p < 0.001). Panel OpenViIC xác nhận 66.1% mention sai-theo-KTVIC của p1 và 62.1% của fuse2, Δ −3.9 [−5.0, −2.9]. Mỗi target fuse2 có thêm +0.222 [0.211, 0.234] mention mà không panel nào xác nhận.
2. **Mô hình thừa hưởng profile precision của target, và thêm khoảng 1–2 điểm.** Trên 555 ảnh KTVIC test, mô hình và target người được chấm với cùng gold trong từng fold.
   - Hai câu (fuse2-detailed − P1-short), theo 2 ref KTVIC: mô hình −11.19 / −12.23 / −11.76 (P1 seed 42 / 43 / 44), target người −8.41 [−9.84, −6.98].
   - Theo 2 ref + OpenViIC: mô hình −4.87 / −5.45 / −5.98, target −3.63 [−4.60, −2.68]. DiD là −1.25 [−3.36, +0.88] (p = 0.26), −1.82 [−4.18, +0.27] (p = 0.11) và −2.35 [−4.53, −0.22] (p = 0.03). Gộp hai tầng seed × ảnh: −1.80 [−3.99, +0.28], p = 0.09.
   - Short: DiD gộp −1.24 [−3.19, +0.70], p = 0.20.
   - Mention chưa xác nhận mỗi caption (hai câu): mô hình +0.335 [0.278, 0.393], target +0.208 [0.180, 0.236]. Phần riêng của mô hình là +0.127 [0.068, 0.188]. Đây là cận trên của ảo giác do fusion gây ra ngoài tham chiếu.
3. **"+0.0 instance precision" trên UIT-ViIC là hệ quả của cách chọn ảnh.** Trên 2,687 ảnh train, sports ball có mặt ở 100% ảnh và person ở 97.6%. Hai lớp này chiếm 83.9% mention, nên một lớp rút từ hỗn hợp mention có instance 87.6% số lần chỉ do ngẫu nhiên.
   - Trên mọi lớp: ΔP_ref −5.74 [−6.41, −5.03] nhưng ΔP_inst +0.01 [−0.16, +0.19].
   - Bỏ hai lớp chọn ảnh (nosel): ΔP_ref −7.38 [−9.24, −5.50] và ΔP_inst +0.63 [−0.49, +1.73], p = 0.27. Singleton có instance 93.3% (n = 356), mức ngẫu nhiên là 30.9%.
   - Đối chứng là caption tiếng Anh của COCO trên cùng ảnh; người viết AMT không được xem gợi ý lớp. Kết quả −6.08 [−7.89, −4.28] và −0.39 [−1.42, +0.69], nên gợi ý lớp không tạo ra kết quả null.
4. **Trên cảnh COCO chung, khoảng một nửa chi phí là mất sự thật.** Karpathy test có 5,000 ảnh, dùng caption tiếng Anh. ΔP_ref −7.67 [−8.05, −7.28], ΔP_inst −4.00 [−4.33, −3.68], τ = 0.544 [0.514, 0.575]; τ là cận trên. Với 36 lớp "tin cậy" (chọn trên Karpathy val) là −6.22 / −3.33 và τ = 0.513 [0.473, 0.555]. τ giảm khi cảnh phức tạp hơn: 0.857 (1–2 lớp instance), 0.433 (3–4) và 0.285 (từ 5). Singleton chỉ có instance ở 59.2% (n = 2,356).
5. **Cổng G3 cũ không thể trượt. G3' đã được đóng băng trong repo trước khi 52_a/52_b được chấm.** Trên 1,155 ảnh UIT-ViIC test+val, target người fuse2 đạt G3 = 98.6% [97.8, 99.3] với mọi lớp và 93.7% [90.5, 96.8] với nosel (lexicon v1), trong khi mức ngẫu nhiên khoảng 88%.
   - G3'a/b/c và luật cho job 36 nằm trong `G3_PRIME` của script và trong JSON. Script tự đọc kết quả (`verdicts`).
   - Mốc của người: τ_human (lexicon v2, nosel) = 0.090 [0.041, 0.152]. Trên 2,500 ảnh COCO của job 36: 0.541 [0.502, 0.585], với lớp tin cậy 0.507 [0.451, 0.566].
   - Chưa có đầu ra của 52_a/52_b, cũng chưa có fuse2 của job 36. Hai khối `uitviic_models` và `coco_models` ghi "not landed".
6. **Ước lượng "phần thật" của R5-01 là bảo thủ, không lạc quan.** Phép kiểm dùng COCO: panel A là 3 caption tiếng Anh, panel B là 2 caption còn lại, sự thật là nhãn instance.
   - Mention không được hỗ trợ của một caption người giữ lại chỉ có instance ở 70.4% [68.6, 72.2] số trường hợp.
   - "Ước lượng − tỉ lệ thật" đi từ −10.7 [−16.6, −4.8] (zero-shot short) đến −46.3 [−49.4, −43.3] (zero-shot detailed).
   - Nên viết "được xác nhận ngang mức các mention ngoài tham chiếu của một caption người", như R5-01 đã sửa ở commit 61e405b.
7. **NAP-lite (V2) dùng tài nguyên cố định và không đổi thứ hạng nào.** Thành phần:
   - Bảng ngoại lệ chỉ giữ mục có trong ref train: 66/88 từ ghép, 19/39 cặp loại từ.
   - Đồng nghĩa lấy từ `svp.matching.canonical` có sẵn trong repo.
   - Cặp gần nghĩa chỉ được nhận khi φ train ≥ 0.9; có 2 cặp được nhận.
   - Tín dụng thượng vị chỉ trong cây danh từ chỉ người đã bổ sung 8 mục. Không tín dụng gốc trừu tượng (đồ, vật, quần áo).

   P trên KTVIC test, theo thứ tự R0 → CHAIR-vi → NAP-lite: P1-short 77.9 → 80.4 → 82.8 [80.5, 85.1]; fuse2-short 75.8 → 77.5 → 79.3; zero-shot short 52.3 → 55.5 → 64.0; fuse2-detailed 68.0 → 70.2 → 72.7; zero-shot detailed 31.6 → 33.4 → 38.5. Với một người (1v4) là 85.3 → 86.1 → 87.2 [86.0, 88.3].
8. **Chi phí precision ở short của fusion chỉ có ý nghĩa dưới các luật có thứ bậc.** fuse2 − P1, short:
   - R0: −2.19 [−4.81, +0.35], p = 0.10.
   - CHAIR-vi: −2.89 [−5.49, −0.35], p = 0.022.
   - NAP-lite: −3.51 [−6.01, −0.95], p = 0.002.
   - Chỉ φ (φ ≥ 0.9): −1.66 [−4.18, +0.76], p = 0.19.

   Ở hai câu, kết quả là −10.4 / −10.1 / −9.6 với p < 0.001 dưới mọi luật. Lợi về recall vững dưới mọi định nghĩa: R_ex +5.7 [3.8, 7.6], R_ref +6.8 [4.8, 8.7].
9. **So với một người (1v4).** P1-short − người về P: R0 −10.0 [−12.8, −7.2], CHAIR-vi −8.2 [−10.9, −5.4], NAP-lite −6.6 [−9.0, −4.1]. fuse2-short − người về recall:
   - R_ex: +1.6 [−0.8, +3.8].
   - R_ref, có tính tên cụ thể hơn: +3.0 [+0.5, +5.2].
   - R_ref, không tính tên cụ thể hơn: +1.6 [−1.0, +3.9].
   - R_cl, không dùng danh sách: +1.1 [−1.6, +3.8].

   Câu an toàn là "fuse2-short ngang recall của một người", không phải "vượt".
10. **Phần mention sai-theo-tham-chiếu được NAP-lite tín dụng** (do tách từ, đồng nghĩa, gần nghĩa hoặc thượng vị): P1-short 38.0% [31.1, 44.8], fuse2-short 28.3% [23.0, 33.4], fuse2-detailed 25.7% [22.0, 29.6], một người 21.6% [18.8, 24.6]. Với quan hệ của A7 (cách V2 tính) là 42.1 / 33.2 / 28.5 / 26.6.
11. **Caption mơ hồ: phải báo NAP-P kèm R_ref và tỉ lệ đặt tên "above".**
    - Đẩy danh từ chỉ người của P1-short lên một bậc làm P (NAP-lite) tăng 82.8 → 85.1, nhưng R_ref giảm 47.6 → 39.6 và tỉ lệ "above" tăng 8.7% → 28.9%.
    - Đẩy theo cây của A7 (lên các gốc như đồ, quần áo) làm NAP-A7 tăng 84.4 → 87.7, còn NAP-lite giảm xuống 68.8: lỗ hổng này đã đóng.
    - Caption hằng "người" vẫn đạt NAP-lite 78.7 (CHAIR-vi 65.6). Caption "người + đồ" đạt 44.5 (NAP-A7 68.1).
12. **φ đo việc hai tên chỉ cùng một thực thể.**
    - Trên KTVIC train, trung vị φ theo quan hệ A7: đồng nghĩa 1.00 (6 cặp), gần nghĩa 1.00 (3), thành viên nhóm 0.98 (5), thượng/hạ vị 0.77 (28), không liên quan 0.07 (516), các danh từ chỉ người ngang hàng −0.14 (13).
    - Trên Flickr30k Entities (31,783 ảnh, 17,539 cặp), AUROC của φ khi dự đoán "cùng thực thể" là 0.961. Với φ ≥ 0.9, 77.9% cặp là đồng tham chiếu.
    - Ví dụ man~person: φ 0.99 khi ảnh có 1 người và 0.46 khi có từ 3 người; tỉ lệ đồng tham chiếu tương ứng 1.00 và 0.54.
13. **Gần như không còn headroom precision thật ở short.**
    - Precision hiệu chỉnh độ nhạy panel (theo lớp): P1-short 98.3 [95.6, 100], fuse2-short 97.6 [94.9, 100], P1-detailed 98.5 [96.0, 100], fuse2-detailed 95.5 [92.9, 98.2], zero-shot short 89.8 [86.1, 93.9].
    - fuse2 − P1: short −0.7 [−2.9, +1.6], p = 0.57; hai câu −3.0 [−5.3, −0.5], p = 0.014 (số mới, V5 không báo).
    - Độ nhạy của panel là 59.4% [55.7, 63.0]; điều chỉnh theo lớp thì 61.5–64.8%.
14. **Lạm phát điển hình: các phương pháp tăng precision trông tốt hơn thực tế 1.5–3 lần nếu chỉ chấm theo ref KTVIC.** ΔP so với fuse2 cùng chế độ, theo ba gold (KTVIC / hợp / hiệu chỉnh):

    | Phương pháp | KTVIC | Hợp | Hiệu chỉnh |
    |---|---|---|---|
    | tags, short | +2.1 | +0.8 | +0.6 |
    | tags, hai câu | +2.8 | +0.8 | +0.2 |
    | VTF trên 6 mẫu | +2.4 | +1.2 | +0.1 |
    | committee FT10, MBR short | +3.5 | +2.3 | +1.6 [−0.0, +3.1] |
    | committee FT10, cover hai câu | +4.7 | +2.8 | +2.1 [+0.4, +3.8] |
15. **Committee nhiều policy.** "Vượt dây cung" là phần hơn hỗn hợp P1↔fuse2 có cùng số object, theo gold hợp.
    - SEED8 (P1 s42/s43/s44 + fuse2 s42), MBR short: vượt dây cung +1.65 [+0.61, +2.75]; P hiệu chỉnh +1.6 [−0.7, +3.4].
    - SEED8, cover theo luật đã đăng ký k = round(0.3 × 8) = 2: +1.07 [−0.00, +2.13], chưa đạt ngưỡng +1.5 của V5; P hiệu chỉnh +2.2 [+0.5, +4.0].
    - SEED8, cover k = 3 (số V5 trích): +1.92 [+0.98, +2.80], nhưng R hợp giảm 11.2 điểm.
    - FT10 (có E5): MBR +2.08 [+0.95, +3.15]; cover k = 3 +2.17 [+0.95, +3.38].
    - Ở 1v4 + OpenViIC, P của FT10 MBR là 90.6, của fuse2 là 88.3, của một người là 94.1: committee thu hẹp được 2.3 trong 5.7 điểm.
16. **V4: năm caption KTVIC không hoán đổi được cho nhau.** Hai caption ở vị trí kề nhau chung nhiều object hơn hai caption không kề: +0.172 [0.160, 0.183] (train) và +0.237 [0.206, 0.266] (test). Jaccard chênh +0.115 [0.109, 0.122] / +0.142 [0.125, 0.158]. Hợp với một caption kề thêm ít object mới hơn 21.7% so với caption không kề (train). `prereg_ladder_check.py --check` trước đây đọc một file không có trong repo; sau khi sửa một dòng, lệnh đã chạy được. Bản sửa đã vào commit 61e405b. Hiện chưa run nào của thang về.

## 1. Kiểm toán hai gold (V3, `two_gold_audit.py`)

Gold của mỗi ảnh và mỗi fold:
- A: hai caption giữ lại của chính bộ dữ liệu, tức typicality của nhóm người viết.
- I: bằng chứng độc lập, gồm panel OpenViIC của cùng ảnh (với KTVIC) hoặc nhãn instance COCO-2014 (với UIT-ViIC và COCO).
- U = A ∪ I.

τ_I = Δ(mention ngoài I)/Δ(mention ngoài A): phần chi phí precision theo tham chiếu cũng là chi phí theo sự thật.

### 1a. Target trên KTVIC train (3,724 ảnh, mọi lớp của lexicon 113 danh từ)

| policy | object/target | P_A | P_I | P_U | xác nhận % |
|---|---|---|---|---|---|
| p1 | 1.62 | 71.8 | 78.0 | 90.4 | 66.1 |
| cons | 1.76 | 71.0 | 78.0 | 90.5 | 67.2 |
| fuse2 | 2.69 | 62.9 | 73.3 | 86.0 | 62.1 |
| rnd2 | 2.33 | 64.9 | 74.6 | 87.1 | 63.4 |
| unf2 | 1.86 | 67.8 | 75.9 | 88.4 | 63.8 |
| multiref | 1.63 | 69.5 | 76.7 | 89.2 | 64.5 |

| B − p1 | ΔP_A | ΔP_I | ΔP_U |
|---|---|---|---|
| fuse2 | −8.93 [−9.45, −8.42] | −4.73 [−5.27, −4.17] | −4.47 [−4.87, −4.08] |
| rnd2 | −6.94 [−7.40, −6.51] | −3.49 [−3.97, −3.01] | −3.30 [−3.65, −2.96] |
| unf2 | −4.03 [−4.51, −3.59] | −2.17 [−2.63, −1.68] | −2.08 [−2.41, −1.74] |
| multiref | −2.30 [−2.77, −1.85] | −1.35 [−1.84, −0.87] | −1.26 [−1.62, −0.90] |
| cons | −0.78 [−1.22, −0.33] | −0.09 [−0.48, +0.31] | +0.07 [−0.22, +0.35] |

Một lớp chỉ 1 trong 5 caption KTVIC nhắc thì OpenViIC cũng nhắc ở 57.2% số trường hợp; lớp được cả 5 caption nhắc thì 88.8%.

### 1b. Bảng X, panel A: KTVIC test, mô hình và target người trên cùng gold (555 ảnh)

| | gold | mô hình (s42 / s43 / s44) | target người | DiD (s42 / s43 / s44) | DiD gộp 2 tầng |
|---|---|---|---|---|---|
| hai câu | 2 ref KTVIC | −11.19 / −12.23 / −11.76 | −8.41 [−9.84, −6.98] | −2.77 / −3.82 / −3.35 | −3.31 [−5.83, −0.91] p = 0.009 |
| hai câu | 2 ref + OpenViIC | −4.87 / −5.45 / −5.98 | −3.63 [−4.60, −2.68] | −1.25 / −1.82 / −2.35 | −1.80 [−3.99, +0.28] p = 0.09 |
| short | 2 ref KTVIC | −2.51 / −3.55 / −3.08 | −1.70 [−2.91, −0.53] | −0.81 / −1.85 / −1.38 | −1.34 [−3.92, +1.07] p = 0.28 |
| short | 2 ref + OpenViIC | −0.89 / −1.46 / −1.99 | −0.21 [−0.86, +0.42] | −0.68 / −1.25 / −1.78 | −1.24 [−3.19, +0.70] p = 0.20 |

Ở hai câu, mô hình (fuse2-detailed) được so với P1-short; target người là cặp ghép so với caption đầu. Ở short, mô hình là fuse2-short so với P1-short; target là caption đồng thuận so với caption đầu. Mỗi seed fuse2 hiện chỉ có s42, nên tầng seed chỉ lấy mẫu lại P1. Khi s43/s44 về, chạy lại `--blocks ktvic_models` là đủ.

### 1c. Bảng X, panel C: cận sự thật bằng nhãn instance (target người, fuse2 − p1)

| tập | họ lớp | ΔP_ref | ΔP_inst | τ_I | singleton có instance (n; ngẫu nhiên) |
|---|---|---|---|---|---|
| UIT-ViIC train, VI (có gợi ý lớp) | mọi lớp | −5.74 [−6.41, −5.03] | +0.01 [−0.16, +0.19] | 0.03 | 98.1% (1,323; 87.6%) |
| UIT-ViIC train, VI | nosel | −7.38 [−9.24, −5.50] | +0.63 [−0.49, +1.73] | 0.10 [0.07, 0.14] | 93.3% (356; 30.9%) |
| UIT-ViIC train, EN (không gợi ý) | nosel | −6.08 [−7.89, −4.28] | −0.39 [−1.42, +0.69] | 0.13 [0.10, 0.16] | 87.3% (741; 32.7%) |
| COCO test 5,000, EN | mọi lớp | −7.67 [−8.05, −7.28] | −4.00 [−4.33, −3.68] | 0.54 [0.51, 0.57] | 59.2% (2,356; 17.6%) |
| COCO test 5,000, EN | 36 lớp tin cậy | −6.22 [−6.68, −5.75] | −3.33 [−3.67, −3.00] | 0.51 [0.47, 0.56] | 57.9% (1,044; 24.1%) |

Lexicon v2 (`LEX_V2` trong script) xử lý ba loại lỗi. Nó thêm các danh từ chỉ người mà v1 bỏ sót: cầu thủ, vận động viên, VĐV, thủ môn, trọng tài, khán giả, người chơi. Nó nuốt các cụm không phải object như "bóng bàn", "ghi bàn" và "bàn thắng". Nó cũng sửa "gấu bống", "chó bông" và "màn hình máy tính". Trên UIT-ViIC train nosel, v2 cho −7.40 / +0.43; trên val+test nosel cho −5.33 [−7.90, −2.81] / +0.87 [−0.46, +2.23].

Bản v2 hiện chỉ nằm trong `two_gold_audit.py`. `object_prf.py` và `score_coco_probe.py` vẫn dùng v1 (`coco80_vi.json`). Muốn đưa v2 vào JSON thì cần sửa `score_coco_probe.py` để nuốt cụm không phải object. File đó đang do agent khác sửa, nên phần việc này để lại cho họ.

### 1d. G3' (đóng băng 12/10, trước khi có bất kỳ đầu ra UIT-ViIC trong miền nào)

Dữ liệu là 1,155 ảnh UIT-ViIC test+val có đủ 5 caption, họ lớp nosel, lexicon v2, B = 5000. Các ngưỡng giống R5-00 §7a.
- **G3'a (short):** khoảng tin cậy 90% của ΔP_I (fuse2-short − P1-short) nằm trong [−3, +3], và cận dưới CI 95% của ΔR_I lớn hơn 0.
- **G3'b (hai câu):** DiD_I đạt nếu cận dưới CI 95% > −3, bị loại nếu cận trên < −3.
- **G3'c:** "chủ yếu điển hình" nếu cận trên CI 95% của τ_model < 0.5, "chủ yếu sự thật" nếu cận dưới > 0.5. Mốc τ_human = 0.090 [0.041, 0.152].
- **Job 36 (COCO 2,500, mô hình train trên KTVIC):** "không tệ hơn fusion của người" nếu cận trên CI 95% của τ_model − τ_human < +0.15. Mốc τ_human là 0.541 [0.502, 0.585] (mọi lớp) và 0.507 [0.451, 0.566] (lớp tin cậy).
- G3 cũ chỉ được báo kèm ghi chú "không mang thông tin trên UIT-ViIC".

Đường chạy đã được kiểm bằng preds thay thế: zero-shot so với VSPS trên COCO, và caption người đóng vai preds trên UIT-ViIC.

```
NCS_DATA=data python scripts/two_gold_audit.py --blocks uitviic_models coco_models \
  --uit-results <ncs-data>/results/uitviic --uit-pair uitviic_p1_s42:uitviic_fuse2_s42 \
  --coco-results data/results/coco_transfer --coco-pair p1_s43:fuse2_s42
```

### 1e. Kiểm định ước lượng "phần thật" trên COCO (sự thật = instance)

| | mention không được hỗ trợ / caption | ước lượng % | tỉ lệ thật % | ước lượng − thật |
|---|---|---|---|---|
| một caption người (1v2) | 0.174 | | 70.4% có instance | |
| zero-shot short | 0.203 | 77.3 | 88.0 | −10.7 [−16.6, −4.8] |
| zero-shot detailed | 0.887 | 35.8 | 82.2 | −46.3 [−49.4, −43.3] |
| VSPS short | 0.130 | 62.6 | 82.2 | −19.6 [−26.6, −12.8] |
| VSPS detailed | 0.370 | 45.1 | 80.4 | −35.4 [−39.7, −30.8] |

## 2. NAP-lite và φ (V2, `nap.py`)

Có ba bộ trích xuất:
- E0: `objects_in`.
- E1t: E0, thêm chuẩn hoá dấu thanh và bảng từ ghép / loại từ chỉ giữ mục có trong ref train.
- EW: lexicon khớp trên từ nguyên của pyvi, không dùng bảng nào. Đây là cận không phụ thuộc danh sách.

| P (%) | R0 | CHAIR-vi | CHAIR-vi + cây người | NAP-lite [CI] | NAP-A7 | EW exact | EW NAP-lite |
|---|---|---|---|---|---|---|---|
| P1-short | 77.9 | 80.4 | 82.6 | 82.8 [80.5, 85.1] | 84.4 | 77.3 | 83.7 |
| fuse2-short | 75.8 | 77.5 | 78.8 | 79.3 [76.7, 81.8] | 81.0 | 74.6 | 79.6 |
| tags_fuse2-short | 77.9 | 79.8 | 80.5 | 81.6 [79.1, 84.0] | 83.1 | 77.6 | 82.1 |
| zero-shot short | 52.3 | 55.5 | 61.4 | 64.0 [61.4, 66.7] | 66.1 | 54.4 | 68.8 |
| P1-detailed | 78.3 | 80.3 | 82.5 | 82.3 [79.8, 84.6] | 83.9 | 77.3 | 83.1 |
| fuse2-detailed | 68.0 | 70.2 | 72.3 | 72.7 [70.3, 74.8] | 74.1 | 66.1 | 72.4 |
| zero-shot detailed | 31.6 | 33.4 | 36.7 | 38.5 [37.0, 39.9] | 41.9 | 33.0 | 41.5 |
| một người (1v4) | 85.3 | 86.1 | | 87.2 [86.0, 88.3] | 88.1 | 84.6 | |

| R (%) | R_ex | R_ref | R_ref không tính tên cụ thể hơn | R_ref (quan hệ A7) | R_cl (φ ≥ 0.9, EW) |
|---|---|---|---|---|---|
| P1-short | 41.4 | 47.6 | 45.7 | 49.7 | 42.0 |
| fuse2-short | 47.1 | 54.4 | 52.0 | 56.5 | 47.5 |
| fuse2-detailed | 61.2 | 67.3 | 65.7 | 69.8 | 61.6 |
| zero-shot short | 32.5 | 38.2 | 37.0 | 40.7 | 28.8 |

NAP-lite xoá 27% khoảng cách precision giữa zero-shot và P1 ở short (18.8 so với 25.7). Con số này là 3% với CHAIR-vi và 42% với EW NAP-lite. tags_fuse2 − P1 không có ý nghĩa dưới mọi luật: NAP-lite −1.3 [−3.7, +1.2]. Cặp gần nghĩa được nhận là quầy hàng~sạp hàng và quầy hàng~cửa hàng (φ = 1.0). Cặp vỉa hè~lề đường bị loại vì φ = 0.64.

## 3. Committee, headroom và lạm phát điển hình (V5, `committee_headroom.py`)

| hệ (555 ảnh) | object/caption | P hiệu chỉnh [CI] | P hiệu chỉnh, độ nhạy chung | P 1v4 + OpenViIC |
|---|---|---|---|---|
| một người | | | | 94.1 [93.3, 94.8] |
| P1-short | 1.80 | 98.3 [95.6, 100] | 99.1 | 89.4 |
| fuse2-short | 2.10 | 97.6 [94.9, 100] | 98.9 | 88.3 |
| fuse2-detailed | 3.16 | 95.5 [92.9, 98.2] | 98.2 | 84.5 |
| zero-shot short | 2.17 | 89.8 [86.1, 93.9] | 93.5 | 75.8 |
| SEED8 MBR short | 1.85 | 99.1 [96.7, 100] | 100 | 90.9 |
| FT10 MBR short | 2.03 | 99.1 [96.7, 100] | 100 | 90.6 |
| SEED8 cover k = 2 | 2.64 | 97.7 [95.0, 100] | 99.3 | 87.0 |
| FT10 cover k = 3 | 2.91 | 97.6 [95.1, 100] | 99.5 | 87.2 |

Luật committee đã được V5 đăng ký. Khi thang về, chạy lại:

```
NCS_DATA=data python scripts/committee_headroom.py --members p1-gold p1_s43 p1_s44 fuse2_s42 fuse2_s43 fuse2_s44 cons_s42 unf2_s42 rnd2_s42 multiref_s42 p1ep4_s42
```

Lệnh này cho k = round(0.3 × 22) = 7. Claim chỉ được giữ nếu phần vượt dây cung theo gold hợp ≥ +1.5 với CI không chứa 0, và P hiệu chỉnh không giảm.

## 4. Tái lập và các chỗ lệch so với verifier

Mọi số chính của V2, V3, V4 và V5 đều tái lập được bằng script trong repo. Các chỗ lệch:
- **V3, contrast của target trên KTVIC:**
  - −8.93 so với −8.88 (target train).
  - Target trong DiD: −8.41 so với −8.36.
  - DiD theo 2 ref: −2.77 / −3.82 / −3.35 so với −2.83 / −3.87 / −3.40.
  - Nguyên nhân: script dùng quy ước của repo (`human_parity.py`) là lấy trung bình P theo fold, còn V3 cộng gộp số đếm của 10 fold trước rồi mới chia. Với mô hình thì hai cách cho cùng kết quả, vì một caption được dùng ở mọi fold.
  - Các CI lệch tối đa 0.15 vì lượt lấy mẫu bootstrap khác nhau.
- **V2:**
  - Phần được tín dụng theo quan hệ A7: 42.1 so với 43.0 (P1-short); 29.8 so với 32.0 (zero-shot detailed). Nguyên nhân: script dùng bảng ngoại lệ chỉ gồm mục có trong ref train, còn V2 dùng đủ 88 mục của A7, nên các nhóm S_pred/S_gold thay đổi.
  - Tỉ lệ "above" theo A7 của P1-short: 10.6 so với 10.2. Tấn công đẩy tên lên một bậc: NAP-A7 87.7 so với 87.8, "above" 50.6 so với 49.0. Nguyên nhân: cụm thực thể ở đây không bắc cầu (bản sửa của V2), và script dùng E1t.
  - fuse2-short − người, R_ref theo A7: +3.2 [0.7, 5.6] so với +3.4 [0.9, 5.6]. Nguyên nhân: recall 1v4 ở đây cộng gộp qua fold, còn V2 lấy trung bình theo fold trong từng ảnh.
  - Flickr30k Entities: 17,539 cặp so với 17,542. Nguyên nhân: thứ tự cộng số thực ở ngưỡng "kỳ vọng đồng nhắc = 5". AUROC vẫn là 0.961.
  - NAP-lite là tổ hợp mới mà V2 chưa tính trọn. Hai số gần nhất của V2 là "CHAIR-vi + cây người" 82.6 và "tín dụng chỉ cho danh từ chỉ người" 83.7 (P1-short).
- **V5:**
  - FT10 MBR short vượt dây cung: +2.08 [0.95, 3.15] so với +2.0 [1.0, 3.0]. Nguyên nhân: đầu P1 của dây cung ở đây là s42, còn V5 (`v5_eval.py`) dùng s43.
  - Với SEED8, V5 trích k = 3 (+1.9), trong khi chính luật V5 đăng ký, round(0.3 × 8), cho k = 2: +1.07 [−0.00, +2.13], chưa đạt ngưỡng.
- **V4:** CI test của số object chung là [0.206, 0.266] so với [0.207, 0.268], do lượt bootstrap khác nhau. `prereg_ladder_check.py --check` không chạy được (FileNotFoundError) cho tới khi sửa một dòng.

## 5. Giới hạn

- Panel OpenViIC là một panel người khác, không phải sự thật. Hai panel cộng lại phủ khoảng 84% số object nhắc được (R5-01). τ trên COCO là cận trên: phần mention vắng instance có cả lỗi nhãn và lỗi bộ khớp.
- Độ nhạy theo lớp giả định panel bắt object thật mà hệ nhắc thêm với cùng tỉ lệ như object thật mà người nhắc thêm, trong cùng một lớp. Kiểm định trên COCO (1e) cho thấy ước lượng thường thấp hơn thật. Điểm này chỉ ra hướng sai lệch, chưa xác định được độ lớn trên KTVIC.
- Mỗi điểm dữ liệu chỉ có một seed fuse2 (s42). Năm caption KTVIC không hoán đổi được (16), nên "người giữ lại" thực chất là "caption giữ lại", có thể cùng người viết với một trong 4 caption còn lại.
- NAP-lite vẫn tín dụng "người" cho mọi danh từ chỉ người, nên caption hằng "người" đạt 78.7. NAP-lite không đổi thứ hạng nào, nên chỉ hợp làm đóng góp phụ, như V2 kết luận.
- Hai file vượt ngưỡng 400 dòng của aislop: `nap.py` (586, phần lớn là bảng từ vựng của A7) và `two_gold_audit.py` (499). Chưa tách để giữ mỗi phân tích trong một file.
