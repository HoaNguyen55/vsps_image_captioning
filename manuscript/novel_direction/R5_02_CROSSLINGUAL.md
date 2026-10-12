# R5-02: Việt – Anh trên cùng ảnh

12/10/2026. Script `scripts/crosslingual_gap.py` (`build`, `score`, `embed`, `report`). Sửa tối thiểu `scripts/evaluate.py` và `scripts/build_gold_sft.py`. Hành vi mặc định (tiếng Việt) giữ nguyên từng byte: các `_check()` đều qua, và `sft.jsonl`, `_build_report.json` của P1 và fuse2 (KTVIC, UIT-ViIC) trùng với bản HEAD. Theo chỉ thị mới của người dùng (12/10), **không dùng ngưỡng 5%**. Mọi metric được báo cáo song song vi | en | vi − en, kèm CI 95%. Không có luật đạt/không đạt và không có "metric thay thế". Từ 12/10, mọi điểm object COCO-80 tiếng Việt dùng bộ khớp **v2** (`score_coco_probe.LEX_V2`, sáu luật đã đông cứng cho G3', hằng `VI_LEXICON`; phiên bản được ghi vào mọi JSON đầu ra). Bảng chính dùng v2, v1 nằm ở phụ lục (mục 6).

## Kết luận đến lúc này (chỉ trần người, CPU)

Mới có số của người viết. Số của hệ thống sẽ có khi các job ở mục 3 chạy xong.

1. **Ngay ở mức người, metric n-gram đã khác hẳn giữa hai ngôn ngữ, và chiều chênh lệch đổi theo tập.** Trên UIT-ViIC, 5 ref tiếng Việt giống nhau hơn nhiều so với 5 ref COCO tiếng Anh của cùng ảnh. CIDEr-D của một người là 163.1 (vi, theo từ) so với 51.9 (en) trên test, và 163.5 so với 59.9 trên val; BLEU-4 trên test là 50.9 so với 17.5. Trên XM3600 chiều ngược lại: CIDEr-D 68.1 so với 113.0, và ref tiếng Việt ở đây dài gần gấp đôi (17.6 âm tiết so với 9.5 token). Số thô của BLEU, METEOR, ROUGE-L và CIDEr-D vì vậy phản ánh trước hết độ đồng nhất của bộ ref trong từng ngôn ngữ.
2. **Cách tách từ không giải thích được chênh lệch này.** Đổi cách tách tiếng Việt (theo từ, theo âm tiết, PTB) làm CIDEr-D tiếng Việt thay đổi tới 17 điểm (163.1 → 179.9 trên UIT-ViIC test). Nhưng vi − en giữ nguyên dấu và cùng cỡ ở mọi cách tách: từ 111 đến 128 trên UIT-ViIC test, từ −45 đến −35 trên XM3600.
3. **METEOR tiếng Việt cao hơn tiếng Anh ở cả hai tập có ref hai ngôn ngữ** (40.5 so với 24.5 trên UIT-ViIC test, 22.1 so với 17.1 trên XM3600), dù chỉ tiếng Anh được cộng điểm stem/synonym/paraphrase. Kể cả trên XM3600, nơi CIDEr-D tiếng Việt thấp hơn tiếng Anh.
4. **So với nhãn instance (gold chung), với bộ khớp v2, precision và recall của người gần như nhau ở hai ngôn ngữ.** Trên UIT-ViIC, P là 99.6 so với 99.0 (test) và 99.2 so với 99.3 (val). R là 40.8 so với 42.3 (test, vi − en = −1.5 [−3.6, 0.6]) và 42.3 so với 44.6 (val, −2.3 [−3.4, −1.2]). Với v1, R tiếng Việt chỉ là 30.1 và 30.4, chênh −12 đến −14 điểm. Chênh lệch đó đến từ bộ khớp: v1 không có "cầu thủ", "vận động viên", "khán giả". Person recall (cặp ảnh có người, ref) tiếng Việt từ v1 lên v2 là 53.8 → 94.2 (train), 53.1 → 94.2 (val), 56.3 → 94.0 (test); tiếng Anh là 87.2, 85.2, 84.3. So với ref thì tiếng Việt cao hơn tiếng Anh (P 96.1 so với 92.0, R 75.5 so với 61.8 trên test), cùng chiều với n-gram: ref tiếng Việt đồng nhất hơn. Sports ball vẫn khác: "ball" khớp, còn "bóng" đứng một mình bị loại khỏi lexicon vì đa nghĩa.
5. **Trần người tiếng Anh trên COCO cùng cỡ với trần người thường thấy trên COCO:** CIDEr-D 88.3 [86.3, 90.4], SPICE 21.0, BLEU-4 19.4 trên 2 441 ảnh. Trên UIT-ViIC trần tiếng Anh thấp hơn (51.9 ở test, 59.9 ở val), có thể vì tập chỉ gồm ảnh thể thao nên IDF của các n-gram thể thao thấp.

## 1. Thiết kế

**Câu hỏi.** Chạy cùng một quy trình bằng tiếng Việt và bằng tiếng Anh trên **cùng ảnh**, thì chất lượng caption và hiệu ứng của phương pháp (Δ = fuse2 − P1) có giống nhau không? Metric nào đã cho kết quả khác nhau giữa hai ngôn ngữ ngay ở mức người?

**Tập song song.**

| tập | ảnh | ref tiếng Việt | ref tiếng Anh | gold không phụ thuộc ngôn ngữ |
|---|---|---|---|---|
| UIT-ViIC test | 231 | 5 (UIT-ViIC) | 5 (COCO: 5 câu đầu trong `dataset_coco.json` của Karpathy) | nhãn instance COCO-2014 |
| UIT-ViIC val | 924 | 5 | 5 | nhãn instance |
| COCO Karpathy test | 2 441 (2 500 ảnh của manifest trừ 59 ảnh thuộc UIT-ViIC train) | không có | 5 | nhãn instance |
| XM3600 (600 ảnh của job 39) | 600 | 2 (2 câu đầu; 27 ảnh có 3) | 2 | không dùng (bản đồ OIV7 chỉ có cho lexicon tiếng Việt) |

- Dữ liệu nằm ở `$NCS_DATA/datasets/{uitviic_en,coco_en,coco_vi}` (do `crosslingual_gap.py build` tạo; `images/` là symlink tới ảnh gốc), `xm3600_en` (agent XM3600 đã tạo bằng `xm3600_oiv7.py build`) và `data/coco_probe/instance_gold.json` (nhãn instance của 2 500 ảnh manifest).
- Kiểm tra khi build: mỗi ảnh UIT-ViIC trùng đúng file COCO-2014 của Karpathy (tên file và phần train2014/val2014 mà `build_uitviic_gold.py` đã đối chiếu). uitviic_en có train 2 695 ảnh × 5 = 13 475 caption, val 924 × 5, test 231 × 5; coco_en có 2 441 × 5. Hai bản XM3600 có cùng 600 id. Bản sao trên n2, n3 và máy local trùng md5.
- `coco_vi` chỉ liệt kê ảnh, không có caption. Với split như vậy, `evaluate.py` sinh caption rồi dừng, không chấm.
- Caption UIT-ViIC do người Việt viết riêng, không phải bản dịch caption COCO. Hai bộ ref vì vậy khác cả người viết lẫn hướng dẫn.

**Hệ thống.** Zero-shot (Qwen2.5-VL-7B), P1 và fuse2. P1 và fuse2 được huấn luyện **trong từng ngôn ngữ** trên UIT-ViIC train (2 695 ảnh), cùng siêu tham số với 52_a/52_b: 2 epoch, seed 42, `--loss-mask` mặc định. fuse2 tiếng Anh chọn consensus và ghép tham lam 2 caption theo 80 lớp COCO tiếng Anh (`--objects coco80en --lang en`). Prompt tiếng Anh dịch sát prompt tiếng Việt (`short_en`, `detailed_en` trong `evaluate.PROMPTS`). Mọi caption được sinh bằng `evaluate.py` với cùng cấu hình cho cả hai ngôn ngữ: bf16, 512 vision token, greedy, 160 token mới. Cấu hình của `coco_probe.py` (1 024 token) không được dùng.

**Metric (mỗi ngôn ngữ).**
- BLEU-1/4, METEOR, ROUGE-L, CIDEr-D (pycocoevalcap, ×100). Tiếng Việt được tách theo ba cách: theo từ (RDRSegmenter, như bảng chính), theo âm tiết (khoảng trắng), và bằng tokenizer PTB. PTB là cách tách của tiếng Anh (bỏ dấu câu), nên cột này là đối chứng cùng tokenizer.
- SPICE (chỉ tiếng Anh).
- Object P/R/F1, CHAIR_i = 100 − P và CHAIR_s trên 80 lớp COCO (`coco80_vi.json` / synonyms của CHAIR), so với các lớp mà ref nêu và so với nhãn instance.
- CLIP-S, RefCLIP-S (MLAION xlm-roberta-large-ViT-H-14) và BERTScore F (xlm-roberta-large). Hai ngôn ngữ dùng cùng mô hình.
- Độ dài caption.

**Trần người, chuẩn hoá, Δ, CI.**
- Trần người: mỗi ref so với k − 1 ref còn lại (k = 5; với XM3600 k = 2), lấy trung bình trên k fold.
- Hệ thống được chấm với cả k ref (số thô, như `evaluate.py`) và với đúng k − 1 ref của từng fold.
- Chuẩn hoá = điểm fold của hệ thống / trần người cùng ngôn ngữ, ×100 (100 = ngang thêm một người viết).
- Δ = fuse2 − P1 trong từng ngôn ngữ, tính cả trên số thô lẫn số chuẩn hoá.
- CI: bootstrap 95% trên ảnh (B = 1000). Hai ngôn ngữ và mọi hệ thống dùng chung các mẫu, nên vi − en và Δ_vi − Δ_en là so sánh ghép cặp.
- METEOR là thống kê toàn tập của jar METEOR, nên chỉ có giá trị điểm.

## 2. Trần người (CPU n2, 12/10)

Bộ khớp object tiếng Việt: v2. Mỗi ô là vi / en / vi − en [CI 95%]. CIDEr-D, BLEU, ROUGE-L, SPICE nhân 100; object là %; độ dài tính theo token. METEOR không có CI. Độ dài theo từ/âm tiết tính cả dấu câu như `evaluate.py`. Ở tập coco, các hàng n-gram chỉ có tiếng Anh. Bảng đầy đủ: `data/results/crosslingual_human_report.json` (v2) và `_v1.json`. Dữ liệu từng ảnh: `$NCS_DATA/results/xl/human_score.json` (v2) và `human_score_v1.json` trên n2 và n3. Số đã có trước khi bất kỳ caption hệ thống nào được sinh.

| metric | uitviic_test (231 ảnh, k=5): vi / en / vi − en | uitviic_val (924 ảnh, k=5): vi / en / vi − en | xm3600 (600 ảnh, k=2): vi / en / vi − en | coco (2441 ảnh, k=5): vi / en / vi − en |
|---|---|---|---|---|
| BLEU-1 (vi word) | 81.3 / 61.6 / 19.7 [18.1, 21.1] | 80.3 / 63.1 / 17.2 [16.4, 18.0] | 30.1 / 36.0 / -5.9 [-7.9, -4.0] | – / 62.7 / – |
| BLEU-1 (vi syllable) | 81.9 / 61.6 / 20.3 [18.7, 21.8] | 80.6 / 63.1 / 17.5 [16.7, 18.4] | 32.7 / 36.0 / -3.3 [-5.2, -1.4] | – / 62.7 / – |
| BLEU-1 (vi PTB) | 80.6 / 61.6 / 19.0 [17.4, 20.6] | 79.3 / 63.1 / 16.2 [15.3, 17.1] | 33.6 / 36.0 / -2.4 [-4.3, -0.5] | – / 62.7 / – |
| BLEU-4 (vi word) | 50.9 / 17.5 / 33.4 [30.7, 36.1] | 49.4 / 19.3 / 30.1 [28.6, 31.4] | 6.2 / 9.5 / -3.3 [-4.9, -1.9] | – / 19.4 / – |
| BLEU-4 (vi syllable) | 56.4 / 17.5 / 38.9 [36.1, 41.4] | 54.8 / 19.3 / 35.5 [34.2, 36.7] | 8.1 / 9.5 / -1.5 [-3.0, 0.0] | – / 19.4 / – |
| BLEU-4 (vi PTB) | 55.5 / 17.5 / 38.0 [35.3, 40.5] | 54.0 / 19.3 / 34.6 [33.3, 35.9] | 8.4 / 9.5 / -1.1 [-2.7, 0.3] | – / 19.4 / – |
| METEOR (vi word) | 40.5 / 24.5 / 16.0 | 39.6 / 25.4 / 14.2 | 22.1 / 17.1 / 5.0 | – / 24.1 / – |
| METEOR (vi syllable) | 39.9 / 24.5 / 15.4 | 38.9 / 25.4 / 13.5 | 21.7 / 17.1 / 4.6 | – / 24.1 / – |
| METEOR (vi PTB) | 40.1 / 24.5 / 15.6 | 39.2 / 25.4 / 13.7 | 21.8 / 17.1 / 4.6 | – / 24.1 / – |
| ROUGE-L (vi word) | 68.8 / 45.5 / 23.3 [21.8, 24.8] | 67.9 / 47.6 / 20.4 [19.5, 21.2] | 29.0 / 33.8 / -4.8 [-6.5, -3.2] | – / 46.5 / – |
| ROUGE-L (vi syllable) | 69.8 / 45.5 / 24.3 [22.8, 25.8] | 68.8 / 47.6 / 21.2 [20.4, 22.1] | 31.2 / 33.8 / -2.5 [-4.2, -0.9] | – / 46.5 / – |
| ROUGE-L (vi PTB) | 67.6 / 45.5 / 22.1 [20.6, 23.6] | 66.5 / 47.6 / 18.9 [18.0, 19.8] | 32.1 / 33.8 / -1.6 [-3.4, 0.0] | – / 46.5 / – |
| CIDEr-D (vi word) | 163.1 / 51.9 / 111.1 [100.0, 122.3] | 163.5 / 59.9 / 103.6 [97.2, 110.2] | 68.1 / 113.0 / -44.9 [-56.4, -34.4] | – / 88.3 / – |
| CIDEr-D (vi syllable) | 179.7 / 51.9 / 127.8 [116.1, 138.6] | 178.3 / 59.9 / 118.4 [111.7, 125.0] | 74.2 / 113.0 / -38.8 [-50.5, -28.2] | – / 88.3 / – |
| CIDEr-D (vi PTB) | 179.9 / 51.9 / 128.0 [116.6, 138.3] | 179.3 / 59.9 / 119.4 [112.8, 125.9] | 78.0 / 113.0 / -35.1 [-46.8, -24.3] | – / 88.3 / – |
| SPICE | – / 20.1 / – | – / 21.8 / – | – / 25.2 / – | – / 21.0 / – |
| P vs references | 96.1 / 92.0 / 4.1 [2.6, 5.6] | 96.4 / 93.5 / 3.0 [2.3, 3.7] | 68.0 / 76.6 / -8.6 [-13.3, -3.4] | – / 92.9 / – |
| R vs references | 75.5 / 61.8 / 13.7 [10.3, 17.1] | 76.9 / 63.8 / 13.2 [11.5, 14.9] | 69.7 / 78.5 / -8.8 [-13.5, -3.7] | – / 68.8 / – |
| F1 vs references | 84.5 / 73.9 / 10.6 [7.9, 13.3] | 85.6 / 75.8 / 9.8 [8.5, 11.1] | 68.5 / 77.4 / -9.0 [-13.8, -3.8] | – / 79.1 / – |
| CHAIR_i vs references | 3.9 / 8.0 / -4.1 [-5.6, -2.6] | 3.6 / 6.5 / -3.0 [-3.7, -2.3] | 32.0 / 23.4 / 8.6 [3.4, 13.3] | – / 7.1 / – |
| CHAIR_s vs references | 5.3 / 11.2 / -5.9 [-7.8, -4.0] | 4.8 / 9.2 / -4.4 [-5.3, -3.4] | 17.3 / 12.9 / 4.4 [1.8, 6.8] | – / 8.9 / – |
| P vs instances | 99.6 / 99.0 / 0.6 [-0.4, 2.0] | 99.2 / 99.3 / -0.1 [-0.5, 0.4] | – | – / 92.4 / – |
| R vs instances | 40.8 / 42.3 / -1.5 [-3.6, 0.6] | 42.3 / 44.6 / -2.3 [-3.4, -1.2] | – | – / 56.9 / – |
| F1 vs instances | 57.8 / 59.2 / -1.4 [-3.5, 0.8] | 59.3 / 61.6 / -2.2 [-3.3, -1.2] | – | – / 70.5 / – |
| CHAIR_i vs instances | 0.385 / 1.032 / -0.647 [-1.993, 0.360] | 0.780 / 0.727 / 0.053 [-0.357, 0.479] | – | – / 7.6 / – |
| CHAIR_s vs instances | 0.519 / 1.212 / -0.693 [-1.991, 0.519] | 1.061 / 1.039 / 0.022 [-0.541, 0.607] | – | – / 9.5 / – |
| length (vi words / en PTB tokens) | 11.2 / 10.6 / 0.6 [0.3, 0.8] | 11.0 / 10.5 / 0.5 [0.4, 0.6] | 15.9 / 9.5 / 6.4 [6.0, 6.8] | – / 10.4 / – |
| length (vi syllables / en PTB tokens) | 13.3 / 10.6 / 2.7 [2.4, 2.9] | 13.1 / 10.5 / 2.6 [2.5, 2.7] | 17.6 / 9.5 / 8.1 [7.7, 8.5] | – / 10.4 / – |

## 3. Job đã xếp hàng

| máy | job | nội dung | GPU-h ước tính | xong khoảng (UTC) |
|---|---|---|---|---|
| n2 | `39_b_parallel_zeroshot` | zero-shot tiếng Anh trên uitviic_en test+val và xm3600_en; zero-shot tiếng Việt trên UIT-ViIC val (test đã có ở job 38) | ≈ 5.9 | ≈ 02:00 13/10 |
| n2 | `39_y_coco_zeroshot` | zero-shot trên 2 441 ảnh COCO: tiếng Anh (coco_en, chấm với 5 ref) và tiếng Việt (coco_vi, chỉ sinh) | ≈ 10.3 | ≈ 15:00 13/10 |
| n2 | `39_z_crossling_metrics` | CLIP-S/RefCLIP-S/BERTScore (GPU), n-gram/object (CPU) cho mọi hệ thống trên n2 (job 38, 39_b, 39_xm3600_eval, 39_y), rồi `report_n2.md` | ≈ 0.5 (+ 0.5 h CPU) | ≈ 16:00 13/10 |
| n3 | `53_a_uitviic_en_p1_s42` | P1 tiếng Anh: train uitviic_en, đánh giá trên uitviic_en test+val và coco_en | ≈ 4.8 | ≈ 07:00 13/10 |
| n3 | `53_b_uitviic_en_fuse2_s42` | fuse2 tiếng Anh (`--objects coco80en --lang en`), đánh giá như 53_a | ≈ 7.3 | ≈ 14:30 13/10 |
| n3 | `53_c_uitviic_vi_coco` | P1/fuse2 tiếng Việt của 52_a/52_b trên ảnh COCO (coco_vi), rồi CLIP/BERT + n-gram/object cho các hệ thống trên n3 và `report_n3.md` | ≈ 5.0 (+ 0.5 h CPU) | ≈ 20:00 13/10 |

- Tổng cộng ≈ 34 GPU-h. Tốc độ dùng để ước tính là số đo thật trên KTVIC (n2): zero-shot 1.32 s/ảnh (short) và 6.09 s/ảnh (detailed); P1 1.45/1.45; fuse2 1.48/2.56; huấn luyện 7.3 s/bước. Detailed zero-shot trên COCO chiếm ≈ 8.3 GPU-h. Giờ xong là ước tính theo các job đang đứng trước.
- Thứ tự trong hàng đợi: 39_b chạy trước 39_xm3600_eval (theo tên), 39_y và 39_z chạy sau nó. Ở n3, các job 53_* chạy sau 52_* và trước 55–63, nên đẩy các job đó lùi ≈ 17 giờ.
- Mỗi lệnh `evaluate.py` được bọc `timeout … || echo WARN`, với giới hạn bằng khoảng 2 lần thời gian dự kiến: 7 200 s cho UIT-ViIC, 10 800 s cho zero-shot UIT-ViIC/XM3600, 14 400 s cho COCO in-domain, 28 800 s cho COCO zero-shot. Riêng COCO detailed zero-shot cần ≈ 4.1 h nên không thể dùng 7 200 s. Mọi job đã qua `bash -n`.
- Phần chấm object tiếng Việt của 36_coco_c, 38, 52_b, 39_z và 53_c dùng v2. v2 được triển khai lên n2/n3 lúc 12:38 UTC 12/10, trước khi bất kỳ job nào trong số đó chạy. Riêng target huấn luyện (`build_gold_sft.py --objects coco80`) giữ v1, nên dữ liệu huấn luyện của 52_b vẫn trùng từng byte.
- 52_* và 53_* dùng cùng `train_stage2.py` với `--loss-mask` mặc định (legacy). Nếu 52_* chuyển sang `--loss-mask assistant` thì 53_* phải chuyển theo.

## 4. Báo cáo cuối

```bash
# n2, sau 39_z (n2) và 53_c (n3); X=$NCS_DATA/results/xl
scp -P 2241 root@n3.ckey.vn:/root/ncs-data/results/xl/{score,embed}_n3.json $X/
python scripts/crosslingual_gap.py report $X/human_score.json $X/score_n2.json $X/score_n3.json \
    $X/embed_n2.json $X/embed_n3.json --out $X/report_all.json > $X/report_all.md
```

Mỗi tập có các bảng sau: trần người; từng hệ thống × chế độ (số thô, rồi chuẩn hoá); Δ fuse2 − P1 (số thô, rồi chuẩn hoá). Cột luôn là vi | en | vi − en [CI 95%].

## 5. Những chỗ hai ngôn ngữ khác nhau do cách đo

Cần nêu các điểm này khi đọc bảng:
- METEOR 1.5 chạy với `-l en`. Tiếng Anh được cộng điểm khớp gốc từ, từ đồng nghĩa (WordNet) và paraphrase; tiếng Việt chỉ có khớp chính xác.
- Về tách từ, `evaluate.py` giữ dấu câu như một token ở tiếng Việt (UIT-ViIC viết " ." cuối câu), còn PTB bỏ dấu câu ở tiếng Anh. Cột "vi PTB" tách cả hai ngôn ngữ bằng cùng tokenizer.
- Một từ tiếng Việt gồm 1–3 âm tiết, nên n-gram theo âm tiết và theo từ cho số khác nhau, và độ dài của hai ngôn ngữ không cùng đơn vị.
- CLIP-S cắt văn bản ở 77 token XLM-R. Caption detailed tiếng Việt tốn nhiều token hơn, nên phần nội dung bị cắt sớm hơn.
- Giới hạn 160 token mới tác động tương tự: mỗi token Qwen chứa ít nội dung tiếng Việt hơn tiếng Anh.
- COCO không có ref tiếng Việt. Ở tập này chỉ so được CLIP-S, object so với nhãn instance và độ dài.
- Bộ khớp vật thể khác nhau ở hai ngôn ngữ: tiếng Việt v2, tiếng Anh dùng danh sách synonyms chuẩn của CHAIR (Rohrbach). Danh sách này không có "batter", "catcher", "umpire", "crowd", "spectators", "athlete". Trong caption tiếng Anh UIT-ViIC train trên ảnh có người mà không khớp person, các từ này xuất hiện 328, 133, 63, 45, 20, 11 lần. Vì vậy person recall của người viết tiếng Anh (≈ 85%) thấp hơn tiếng Việt v2 (≈ 94%). Danh sách tiếng Anh được giữ nguyên vì là chuẩn của CHAIR.
- Ref của hai ngôn ngữ do hai nhóm người viết theo hai hướng dẫn khác nhau (UIT-ViIC và COCO). Trần người khác nhau vì vậy không chỉ do ngôn ngữ.

## 6. Phụ lục: bộ khớp v1, và danh từ người chưa thêm vào v2

**Trần người, object tiếng Việt v1 → v2 (tiếng Anh trong ngoặc).** Các hàng n-gram, SPICE và độ dài không đổi giữa v1 và v2.

| metric | UIT-ViIC test | UIT-ViIC val | XM3600 |
|---|---|---|---|
| P vs references | 90.8 → 96.1 (92.0) | 90.1 → 96.4 (93.5) | 67.6 → 68.0 (76.6) |
| R vs references | 49.8 → 75.5 (61.8) | 48.6 → 76.9 (63.8) | 69.3 → 69.7 (78.5) |
| F1 vs references | 64.3 → 84.5 (73.9) | 63.1 → 85.6 (75.8) | 68.1 → 68.5 (77.4) |
| CHAIR_i vs references | 9.2 → 3.9 (8.0) | 9.9 → 3.6 (6.5) | 32.4 → 32.0 (23.4) |
| CHAIR_s vs references | 9.1 → 5.3 (11.2) | 9.4 → 4.8 (9.2) | 17.4 → 17.3 (12.9) |
| P vs instances | 99.4 → 99.6 (99.0) | 98.7 → 99.2 (99.3) | – |
| R vs instances | 30.1 → 40.8 (42.3) | 30.4 → 42.3 (44.6) | – |
| F1 vs instances | 46.3 → 57.8 (59.2) | 46.5 → 59.3 (61.6) | – |

**Danh từ người khai thác từ train, chưa thêm.** Ứng viên được lấy từ caption UIT-ViIC train và KTVIC train, không xem test. Điều kiện giữ:
- xuất hiện ≥ 3 lần trong train;
- mọi ngữ cảnh trong train đều chỉ người;
- không chứa và không cắt ngang một từ COCO-80.

Kết quả là 23 danh từ: cô bé, bé trai, thanh niên, bạn trẻ, đôi bạn, cặp đôi, ông lão, bà cụ, ông cụ, học sinh, học viên, phụ huynh, huấn luyện viên, anh em, chị em, cha con, nhân viên, công nhân, bộ đội, du khách, khách du lịch, cùng hai lỗi gõ "vận dộng viên", "đứa tẻ". Bị loại:
- "ông già": ngữ cảnh "hình/đồ ông già noel";
- "tay vợt": cắt ngang "vợt tennis";
- "cảnh sát": "xe/đồn cảnh sát";
- các từ < 3 lần.

Thêm 23 từ này, person recall tiếng Việt tăng thêm khoảng 2 điểm (train 96.2, val 96.4, test 95.6). Tuy vậy, G3' **không** giữ nguyên: số của `two_gold_audit.py` ở family nosel đổi, ví dụ `uitviic_valtest|v2|nosel` fuse2 − p1 dP_A −5.335 → −5.357, dR_I 8.793 → 8.803, CI của tau_I [0.041, 0.152] → [0.041, 0.151]. Lý do là consensus và ghép trong target người chọn caption theo mọi lớp, kể cả person, rồi mới cắt về nosel. Vì G3' phải giữ nguyên, v2 = đúng sáu luật đã đông cứng. Với v2 này, đầu ra `uitviic_valtest`/`uitviic_train` của `two_gold_audit.py` trùng hoàn toàn với HEAD, và tập lớp của 32 863 caption (UIT-ViIC, KTVIC) không đổi. Nếu muốn dùng 23 từ này để chấm, cần một phiên bản riêng (ví dụ v3) chỉ cho chấm điểm, còn G3' giữ v2. Đây là quyết định của tác giả.
