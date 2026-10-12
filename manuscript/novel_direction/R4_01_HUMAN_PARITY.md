# R4-01: Human parity và điểm offline của target policy

12/10/2026. Script `scripts/human_parity.py` (`parity`, `offline`, `rank`). Số liệu: `data/results/human_parity.json` và `data/results/policy_offline.json`. Chỉ dùng 5 caption người của KTVIC. Nhãn AI-silver (`data/object_gold/annot_claude.json`) không phải gold người nên không dùng ở đây.

## Kết luận

1. **Short mode so với 1 người: R ngang người, P thì không.** Trên cùng gold 4 annotator, fuse2, tags_fuse2 và e5 có R bằng một người (ΔR từ +0.7 đến +1.6, CI chứa 0), nhưng P thấp hơn 10–13 điểm (p<0.001). Khoảng cách F1 là −1.9 (tags_fuse2, p=0.10), −2.3 (fuse2, p=0.050) và −3.1 (e5, p=0.007). Theo luật hypernym (F1_spec) cả ba đều thua có ý nghĩa (−2.4 đến −3.4). "Không có ý nghĩa" không có nghĩa là "tương đương": CI của fuse2 vẫn cho phép thua tới 4.5 điểm F1. P1 thua người cả R (−4.1) lẫn F1 (−5.9).
2. **Detailed mode chưa đạt mức 2 người.** Ghép 2 caption người bằng `fused()` cho F1 70.9 với 2.57 object/caption. Các hệ detailed tốt nhất nêu nhiều object hơn (3.0–3.3) nhưng chỉ đạt F1 61.3–62.2 (ΔF1 từ −8.8 đến −9.6, p<0.001). Phần thua chủ yếu nằm ở P (−14.0 đến −17.5). R cũng thấp hơn 2.3–4.3 điểm, có ý nghĩa ở 3/4 hệ, nhưng phần này nhỏ và phụ thuộc cách gộp fold (mục 1).
3. **Xếp hạng offline không rò rỉ (train): fuse2 67.7 > rnd2 65.7 > cons 62.9 > unf2 61.9 > p1 60.6 > multiref 58.9 (F1).** Greedy hơn random +2.0 F1 (R +6.9, P −2.0), và consensus hơn P1 +2.3 F1 (R +4.1, P −0.8): cách chọn caption có tác dụng ngay ở mức target. Đây là thứ tự dự đoán để `rank` kiểm khi các run ladder có preds. Các cặp liền kề cons/unf2, unf2/p1 và p1/multiref chỉ cách nhau 1.0–1.7 F1 với CI chồng lấn hoặc chạm nhau, nên một τ thấp do đảo các cặp này chưa nói lên nhiều.
4. **Giao thức held-out riêng ("own") bị rò rỉ do chọn lọc.** `consensual()` đọc cả 5 caption, nên cons được chấm với chính những annotator đã "bỏ phiếu" chọn nó. Trên cùng gold 4 caption, cons hơn p1 tới +14.6 F1 (P +8.9), trong khi trên gold chung không rò rỉ chỉ hơn +2.3 F1 (P −0.8). fuse2, rnd2 và unf2 cũng bắt đầu bằng consensus, lại có gold khác cỡ (3 hoặc 4 caption). Bảng "own" chỉ để tham khảo, không dùng để xếp hạng.
5. **Những gì số liệu không cho thấy.** Gold ở đây là "được người nhắc tới", không phải "có trong ảnh". Vì vậy khoảng cách P giữa model và người gồm cả ảo giác lẫn object có thật mà annotator held-out không nhắc. Chưa có gold presence do người gán nên chưa tách được hai phần này. Phép đo chỉ gồm object trong lexicon 113 mục, không đo thuộc tính, quan hệ hay độ trôi chảy. So sánh 2v3 không cân độ dài. Điểm offline là điểm của target, chưa phải của model sau khi train.

## 1. Giao thức

- **Metric** như `object_prf.py`: object P/R/F1 khớp đúng, và biến thể hypernym (P_h, R_spec, F1_spec). Mỗi số là **trung bình qua các fold**: tính `scores()` trên từng fold (toàn bộ ảnh), rồi lấy trung bình. CI 95% lấy từ bootstrap theo ảnh (mỗi ảnh mang theo mọi fold của nó), B = 5000. Δ là paired bootstrap (hệ thống − người) trên cùng các ảnh được lấy mẫu; p hai phía, sàn 2/B = 0.0004 (ghi là p<0.001).
- Độ nhạy theo cách gộp: nếu gộp fold theo ảnh trước (mỗi ảnh nặng như nhau), R của 2 người thấp hơn 0.6 và ΔR của các hệ detailed thu hẹp còn −1.7 đến −3.8 (chỉ tags_fuse2 và e5dpo còn có ý nghĩa). Vậy phần thua về R ở 2v3 nhỏ và phụ thuộc cách gộp; phần thua về P và F1 thì không. Ở 1v4, hai cách gộp cho cùng kết luận.
- **1v4:** caption của từng annotator so với hợp object của 4 caption còn lại (5 fold). Hệ short-mode được chấm với **đúng** các union 4 caption đó.
- **2v3:** `fused()` (quy tắc ghép của fuse2) của từng cặp annotator (10 cặp) so với hợp của 3 caption còn lại. Hệ detailed-mode được chấm với đúng các union đó.
- Không dùng 5 reference như Bảng IV, vì người không thể bị chấm với chính caption của mình, còn hệ thống phải được chấm với cùng một gold. Gold càng lớn thì P càng cao: fuse2-short có P 75.7 khi so với 5 ref, nhưng 72.9 khi so với 4 ref.
- Số của bản nhanh (reviewer agent) được tái lập: 1 người 85.3/46.9, fuse2-short 72.9/48.5, P1-short 75.2/42.8, fuse2-detailed 59.6/63.6. Riêng R của 2 người là 66.6 thay vì 66.7, vì bản nhanh lấy hợp tập object của hai caption, còn ở đây `objects_in` chạy trên văn bản `fused()`. Hai cách khác nhau ở 17/5580 cặp, do token hóa ở ranh giới câu.

## 2. Human parity (KTVIC test, 558 ảnh)

### 2a. Short mode so với 1 người (gold = hợp của 4 caption còn lại)

| | obj/caption | P | R | F1 | P_h | F1_spec |
|---|---|---|---|---|---|---|
| **1 người** | 1.74 | 85.3 [84.0, 86.6] | 46.9 [45.1, 48.7] | 60.5 [58.7, 62.3] | 86.2 [84.9, 87.4] | 60.7 [58.8, 62.5] |
| p1-gold-short | 1.80 | 75.2 [72.5, 77.9] | 42.8 [40.4, 45.2] | 54.6 [52.2, 56.9] | 77.9 [75.4, 80.4] | 54.4 [51.9, 56.8] |
| fuse2_s42-short | 2.09 | 72.9 [70.4, 75.4] | 48.5 [46.2, 50.9] | 58.2 [56.0, 60.4] | 74.9 [72.5, 77.4] | 58.2 [55.9, 60.5] |
| tags_fuse2_s42-short | 2.02 | 75.0 [72.4, 77.5] | 48.1 [45.8, 50.5] | 58.6 [56.4, 60.9] | 77.1 [74.6, 79.5] | 58.3 [56.0, 60.6] |
| e5_s42-short | 2.08 | 72.3 [69.6, 74.9] | 47.6 [45.3, 50.0] | 57.4 [55.2, 59.6] | 74.3 [71.8, 76.9] | 57.3 [55.0, 59.6] |
| e5dpo_s42-short | 2.01 | 70.1 [67.5, 72.7] | 44.9 [42.6, 47.3] | 54.8 [52.6, 57.0] | 73.2 [70.7, 75.6] | 54.7 [52.4, 57.0] |
| zeroshot-short | 2.17 | 50.0 [47.4, 52.6] | 33.3 [31.0, 35.7] | 40.0 [37.8, 42.2] | 53.4 [50.8, 55.9] | 39.9 [37.7, 42.2] |

| hệ thống − 1 người | ΔP | ΔR | ΔF1 | ΔF1_spec |
|---|---|---|---|---|
| p1-gold-short | -10.1 [-13.0, -7.2] p<0.001 | -4.1 [-6.4, -1.8] p<0.001 | -5.9 [-8.4, -3.5] p<0.001 | -6.3 [-8.7, -3.8] p<0.001 |
| fuse2_s42-short | -12.4 [-15.1, -9.7] p<0.001 | +1.6 [-0.7, +3.8] p=0.165 | -2.3 [-4.5, +0.0] p=0.050 | -2.5 [-4.8, -0.2] p=0.036 |
| tags_fuse2_s42-short | -10.3 [-13.0, -7.6] p<0.001 | +1.2 [-1.0, +3.4] p=0.286 | -1.9 [-4.1, +0.4] p=0.097 | -2.4 [-4.7, -0.1] p=0.038 |
| e5_s42-short | -13.1 [-15.8, -10.3] p<0.001 | +0.7 [-1.6, +2.9] p=0.560 | -3.1 [-5.6, -0.8] p=0.007 | -3.4 [-5.8, -1.0] p=0.002 |
| e5dpo_s42-short | -15.2 [-18.0, -12.4] p<0.001 | -2.0 [-4.3, +0.5] p=0.102 | -5.7 [-8.1, -3.3] p<0.001 | -6.0 [-8.5, -3.5] p<0.001 |
| zeroshot-short | -35.3 [-38.2, -32.4] p<0.001 | -13.6 [-16.1, -11.1] p<0.001 | -20.5 [-23.0, -18.0] p<0.001 | -20.8 [-23.3, -18.2] p<0.001 |

### 2b. Detailed mode so với 2 người ghép (gold = hợp của 3 caption còn lại)

| | obj/caption | P | R | F1 | P_h | F1_spec |
|---|---|---|---|---|---|---|
| **2 người (fused)** | 2.57 | 76.1 [74.5, 77.6] | 66.6 [64.9, 68.3] | 70.9 [69.2, 72.5] | 77.4 [75.9, 78.9] | 71.5 [69.8, 73.1] |
| p1-gold-detailed | 1.83 | 70.7 [68.1, 73.3] | 45.8 [43.4, 48.1] | 55.6 [53.2, 57.8] | 73.2 [70.7, 75.7] | 55.8 [53.5, 58.1] |
| fuse2_s42-detailed | 3.15 | 59.6 [57.4, 61.7] | 63.6 [61.2, 65.7] | 61.5 [59.6, 63.3] | 62.3 [60.2, 64.4] | 62.6 [60.7, 64.4] |
| tags_fuse2_s42-detailed | 2.97 | 62.1 [59.9, 64.2] | 62.3 [60.1, 64.5] | 62.2 [60.3, 64.0] | 65.3 [63.2, 67.4] | 63.4 [61.5, 65.2] |
| e5_s42-detailed | 3.25 | 58.6 [56.6, 60.6] | 64.3 [62.1, 66.6] | 61.3 [59.5, 63.1] | 61.2 [59.2, 63.1] | 62.5 [60.7, 64.3] |
| e5dpo_s42-detailed | 3.08 | 60.7 [58.6, 62.7] | 63.2 [60.9, 65.6] | 61.9 [60.0, 63.7] | 64.3 [62.3, 66.3] | 63.2 [61.3, 65.0] |
| zeroshot-detailed | 6.54 | 26.9 [25.6, 28.2] | 57.8 [55.4, 60.3] | 36.7 [35.1, 38.2] | 28.8 [27.5, 30.2] | 38.2 [36.7, 39.7] |

| hệ thống − 2 người | ΔP | ΔR | ΔF1 | ΔF1_spec |
|---|---|---|---|---|
| p1-gold-detailed | -5.4 [-8.2, -2.6] p<0.001 | -20.8 [-23.2, -18.4] p<0.001 | -15.3 [-17.7, -13.0] p<0.001 | -15.7 [-18.1, -13.3] p<0.001 |
| fuse2_s42-detailed | -16.5 [-18.9, -14.1] p<0.001 | -3.1 [-5.5, -0.7] p=0.012 | -9.5 [-11.7, -7.3] p<0.001 | -8.9 [-11.1, -6.7] p<0.001 |
| tags_fuse2_s42-detailed | -14.0 [-16.4, -11.6] p<0.001 | -4.3 [-6.7, -1.9] p<0.001 | -8.8 [-10.9, -6.6] p<0.001 | -8.1 [-10.3, -6.0] p<0.001 |
| e5_s42-detailed | -17.5 [-19.8, -15.1] p<0.001 | -2.3 [-4.7, +0.1] p=0.064 | -9.6 [-11.7, -7.5] p<0.001 | -9.0 [-11.1, -6.9] p<0.001 |
| e5dpo_s42-detailed | -15.4 [-17.8, -13.0] p<0.001 | -3.4 [-5.9, -0.9] p=0.009 | -9.0 [-11.2, -6.9] p<0.001 | -8.3 [-10.4, -6.2] p<0.001 |
| zeroshot-detailed | -49.2 [-51.2, -47.1] p<0.001 | -8.8 [-11.6, -5.9] p<0.001 | -34.3 [-36.5, -32.0] p<0.001 | -33.3 [-35.5, -31.1] p<0.001 |

**Vị trí caption không hoán đổi được.** F1 của "1 người" theo vị trí trong file là 60.6 / 61.7 / 61.6 / 60.9 / **57.7**; vị trí 5 có P chỉ 76.8, các vị trí còn lại 85–90. Ở 2v3, bốn cặp kề nhau (1+2, 2+3, 3+4, 4+5) có F1 64.5–68.6, thấp hơn cả sáu cặp không kề (69.7–76.1): hai caption liền nhau trong file hay nêu cùng object. Số "1 người" và "2 người" ở trên là trung bình qua mọi vị trí (từng fold có trong `per_fold` của JSON).

## 3. Điểm offline của target policy (KTVIC train, 3769 ảnh)

Policy như `build_gold_sft.py` và các job ladder. Policy nhiều hàng (unf2, multiref) được chấm từng hàng rồi lấy trung bình, tức là điểm kỳ vọng của một hàng train.

### 3a. Held-out chung (dùng để xếp hạng)

Với mỗi ảnh, duyệt cả 10 cách chọn 2 caption held-out. Mỗi policy chỉ được dựng từ 3 caption còn lại và được chấm với hợp object của 2 caption held-out. Mọi policy dùng chung gold, và việc dựng target không nhìn thấy gold.

| policy | target (từ 3 caption giữ lại) | obj/hàng | P | R | F1 | P_h | F1_spec |
|---|---|---|---|---|---|---|---|
| p1 | caption sớm nhất theo thứ tự file | 1.62 | 71.8 [71.0, 72.6] | 52.4 [51.5, 53.3] | 60.6 [59.7, 61.4] | 73.8 [73.1, 74.6] | 61.2 [60.4, 62.1] |
| cons | `consensual()` | 1.76 | 71.0 [70.2, 71.8] | 56.5 [55.5, 57.4] | 62.9 [62.0, 63.7] | 72.8 [72.0, 73.5] | 63.6 [62.7, 64.4] |
| **fuse2** | `fused(·, 2)` greedy, 1 hàng | 2.68 | 62.9 [62.2, 63.6] | 73.5 [72.7, 74.2] | **67.7** [67.0, 68.4] | 64.9 [64.3, 65.6] | 68.9 [68.3, 69.6] |
| rnd2 | consensus + 1 caption ngẫu nhiên, 1 hàng | 2.33 | 64.9 [64.2, 65.6] | 66.6 [65.8, 67.3] | 65.7 [65.0, 66.4] | 66.9 [66.3, 67.6] | 66.7 [66.0, 67.4] |
| unf2 | 2 caption của fuse2, 2 hàng | 1.86 | 67.8 [67.1, 68.5] | 57.1 [56.2, 57.9] | 61.9 [61.2, 62.7] | 69.5 [68.9, 70.2] | 62.7 [62.0, 63.5] |
| multiref | cả 3 caption, 3 hàng | 1.63 | 69.5 [68.9, 70.2] | 51.2 [50.4, 52.0] | 58.9 [58.2, 59.7] | 71.3 [70.6, 71.9] | 59.6 [58.8, 60.3] |

### 3b. Held-out riêng ("own"; tham khảo, không dùng để xếp hạng)

Policy được dựng từ cả 5 caption và chấm với các caption nó không chứa. Target ở đây trùng từng byte với `sft.jsonl` của các job ladder cons/fuse2/rnd2/unf2 (đã kiểm tra trên 3769 ảnh). multiref dùng cả 5 caption nên không còn gì để chấm.

| policy | gold | chọn có nhìn gold? | obj/hàng | P | R | F1 | F1_spec |
|---|---|---|---|---|---|---|---|
| p1 | caption 2–5 | không | 1.62 | 83.5 [82.5, 84.5] | 46.7 [45.7, 47.7] | 59.9 [58.9, 60.8] | 60.0 [59.0, 61.0] |
| cons | 4 caption còn lại | **có** | 2.03 | 92.4 [91.8, 93.0] | 62.3 [61.4, 63.2] | 74.5 [73.7, 75.2] | 74.8 [74.1, 75.6] |
| fuse2 | 3–4 caption còn lại | **có** (consensus) | 3.07 | 67.5 [66.6, 68.4] | 85.4 [84.6, 86.2] | 75.4 [74.6, 76.1] | 76.5 [75.8, 77.3] |
| rnd2 | 3 caption còn lại | **có** (consensus) | 2.51 | 75.3 [74.3, 76.2] | 69.5 [68.5, 70.5] | 72.3 [71.5, 73.1] | 73.1 [72.2, 73.8] |
| unf2 | như fuse2 | **có** (consensus) | 2.03 | 73.3 [72.5, 74.1] | 65.3 [64.4, 66.2] | 69.1 [68.3, 69.9] | 69.8 [69.0, 70.6] |

**Lưu ý khi đọc mục 3.**
- Điểm offline đo target so với người held-out, không đo model. Với policy nhiều hàng, MLE có thể học caption kiểu consensus thay vì caption "trung bình", nên model multiref/unf2 sau khi train có thể vượt điểm offline của chính nó.
- Ở 3a, p1 luôn là caption sớm nhất trong 3 caption giữ lại (vị trí 1–3, không bao giờ là 5). Vì vậy p1 > multiref một phần do vị trí 5 ít đồng thuận (mục 2), không hẳn do policy.
- Gold ở 3a chỉ có 2 caption, nên số tuyệt đối không so được với bảng test (gold 3–4 caption); chỉ thứ tự là có nghĩa.

## 4. `rank`: Kendall τ giữa offline và trained

```
NCS_DATA=data python3 scripts/human_parity.py rank \
    p1=data/results/p1-gold-short.preds.json,data/results/p1_s43-short.preds.json,data/results/p1_s44-short.preds.json \
    cons=data/results/cons_s42-short.preds.json unf2=data/results/unf2_s42-short.preds.json \
    multiref=data/results/multiref_s42-short.preds.json rnd2=data/results/rnd2_s42-detailed.preds.json \
    fuse2=data/results/fuse2_s42-detailed.preds.json,data/results/fuse2_s43-detailed.preds.json,data/results/fuse2_s44-detailed.preds.json \
    --out data/results/policy_rank.json
```

- Điểm trained là P/R/F1 so với cả 5 reference trên test, như Bảng IV. Nhiều file của cùng một policy (các seed) được lấy trung bình. τ-b được tính cho P, R và F1, với điểm offline lấy từ giao thức chung (3a).
- Ghép mỗi policy với mode đã train trên target của nó: short cho p1/cons/unf2/multiref, detailed cho fuse2/rnd2 (hàng detailed của hai policy này là target ghép). p1ep4_s42 là cùng policy p1 nhưng với số bước bằng fuse2: chạy `rank` thêm một lần với `p1=…p1ep4_s42-short…` thay vì thêm làm điểm thứ 7, vì hai điểm có cùng offline sẽ tạo tie.
- Smoke test hôm nay (mới có hai policy đã train): p1 → p1-gold-short + p1_s43-short (offline 60.6, trained 54.3 = trung bình 54.1 và 54.5), fuse2 → fuse2_s42-detailed (67.7, 64.4); τ = +1. Với 2 điểm, kết quả này chỉ cho thấy code chạy đúng.
- Độ mạnh của phép thử: với 6 policy, τ = 1 cho p = 0.003; đảo 1 cặp (τ = 0.87) cho p = 0.017; đảo 2 cặp (τ = 0.73) cho p = 0.056.

## 5. Tái lập

```
NCS_DATA=data nice python3 scripts/human_parity.py parity    # ~5 phút CPU
NCS_DATA=data nice python3 scripts/human_parity.py offline   # ~25 phút CPU
```

Muốn thêm output 2 câu ngắn (job 35) vào so sánh 2v3: `parity --vs2 <các stem detailed> zeroshot-two p1_s43-two`.
