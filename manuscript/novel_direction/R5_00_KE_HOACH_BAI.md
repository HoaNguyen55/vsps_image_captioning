# R5-00: Kế hoạch bài và cơ sở bằng chứng cho vòng R6

12/10/2026, nhánh `paper-v10`. File này gộp R4-00, R4-01, R5-01, 06, bản đăng ký trước trong `manuscript/prereg/`, năm báo cáo kiểm định đối kháng V1–V5 của vòng nghiên cứu 2, và hàng đợi GPU đọc lúc 11:15 UTC (18:15 giờ VN). File có hai vai trò:
1. Kế hoạch bài sau kiểm định.
2. Cơ sở bằng chứng và ràng buộc cho vòng R6. R6 tìm một phương pháp mới, có tính mới đột phá, đạt điểm tốt nhất trên KTVIC (§2).

Khi viết file này không dùng GPU, không nạp mô hình, không sửa gì trên n2/n3.

**Ràng buộc**
- Chỉ dùng dataset và nhãn người có sẵn. Không gán nhãn mới. `data/object_gold/annot_claude.json` (AI-silver) không phải bằng chứng.
- Bài chỉ claim một RTX 3090 24 GB. n2 và n3 chỉ để tăng thông lượng, mỗi job dùng 1 GPU.
- Khi V1–V5 khác báo cáo ứng viên A1–A8 hoặc khác R4-00, theo V1–V5.

**Nguồn**
- `R2` = `/tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/research_r2`. Đây là scratchpad: không nằm trong repo và có thể mất. Số lấy từ `R2` phải được tái lập bằng script trong repo trước khi vào bài (quy tắc của R4-00).
- Mã trích dẫn:
  - [R4-00], [R4-01], [R5-01], [06]: các file cùng thư mục này.
  - [PRE] = `manuscript/prereg/2026-10-12_ladder_predictions.json`. [PRE-V4] = `manuscript/prereg/2026-10-12_frontier_invariance_V4.txt` (bản sao của V4).
  - [Vk] = `R2/V_Vk/VERIFY.txt`. [A6] = `R2/A6/REPORT.txt`.
  - [Q-n2], [Q-n3] = `/root/queue/queue.log` và `/root/queue/*.sh` trên n2 (`ssh -p 2022 root@n2.ckey.vn`) và n3 (`ssh -p 2241 root@n3.ckey.vn`).
  - [res] = `data/results/<tên>.json`: điểm n-gram word-level (RDRSegmenter, VnCoreNLP-1.2), thang ×100; CHAIR-vi bản đang dùng.
- Số trong ngoặc vuông là CI 95% bootstrap theo ảnh, trừ khi ghi khác. "chưa có" nghĩa là chưa chạy hoặc chưa về.

## 1. Tóm tắt điều hành

1. **Luận điểm sau kiểm định.** SFT trên caption ghép từ caption người (fuse2) tăng object recall ở cùng độ dài. Phần lớn chi phí precision đo bằng tham chiếu của KTVIC là tính điển hình của nhóm viết tham chiếu. Câu cho bài (V3): *"An independent panel halves fusion's precision cost; most of the remainder is already in the fused human references; the model adds 1–2 points."*
2. **Số chính.**
   - Short, fuse2 − P1 seed 42: R +5.7 [+3.9, +7.7], F1 +4.0 [+2.1, +6.1], P −2.2 [−4.8, +0.4] (p = 0.10) [06].
   - Hai câu, theo 2 ref KTVIC giữ lại: ΔP từ −11.19 đến −12.23 (ba seed P1). Thêm panel OpenViIC thì còn −4.87 đến −5.98.
   - Target người đã mất −3.61 [−4.57, −2.67]. Phần riêng của mô hình (DiD) là −1.26 đến −2.36, chỉ có ý nghĩa với 1/3 seed P1 [V3; `R2/V_V3/v3_ktvic_did.log`].
3. **Mốc điểm số cho R6** (KTVIC test, short, word-level; §2a).
   - Tốt nhất hiện có: CIDEr 149.8, BLEU-4 45.5, ROUGE-L 64.2 (đều P1 s42); METEOR 39.4 (fuse2 s42); CHAIR_i 17.5 (tag trên P1 s43); CHAIR_s 26.7 (P1 s43).
   - CIDEr của ba seed P1 là 149.8 / 143.9 / 143.7, trung bình 145.8. SOTA đã công bố là GRIT, CIDEr 136.0.
4. **Đòn bẩy đã đo** (§2b).
   - Đổi target policy chỉ dịch dọc một đường biên precision–số đối tượng.
   - Chỉ bằng chứng từ detector (tag) từng lệch khỏi đường biên, và chưa có ý nghĩa.
   - MBR trên mẫu T = 0.8 không tăng precision và kéo CIDEr về khoảng 97.
   - Ghép lúc huấn luyện thắng ghép lúc suy luận. Tag giúp fuse2 nhưng không giúp P1.
5. **Chưa có phương pháp.** Không phương pháp huấn luyện mới nào sống qua kiểm định [V5 §0]. Chỗ "phương pháp" trong bài để trống cho R6. Storyline và xếp hạng đóng góp ở §3 là tạm thời.
6. **Bị loại:** IFCR [V1], cơ chế ngưỡng ngầm [V4], ART, CNC, CMPC, tự chưng cất VTF, số học LoRA [V5], khẩu hiệu "typicality, not truth" [V3], AI-silver và gán nhãn mới [R4-00] (§6).
7. **Việc chặn đường:**
   - Cặp kiểm tra loss mask quyết định chạy lại toàn bộ hay không (§8).
   - fuse2 s43/s44, thang 5 policy, và UIT-ViIC trong miền với cổng G3' (§7).
   - Mọi việc CPU còn lại đều 0 GPU.
8. **Venue:** Neurocomputing nếu không có phương pháp mới. Xét lại sau R6 (§11).

## 2. Cơ sở bằng chứng và ràng buộc cho vòng R6 (phương pháp)

Mục tiêu R6, theo yêu cầu mới của tác giả:
- Điểm tốt nhất có thể trên KTVIC test, short mode, word-level.
- Thứ tự ưu tiên: CIDEr, rồi BLEU-4, METEOR, ROUGE-L. CHAIR_i và CHAIR_s càng thấp càng tốt.
- Phương pháp phải có tính mới đột phá.

### 2a. Mốc điểm số hiện tại

KTVIC test 558 ảnh, prompt short, n-gram word-level, ×100. CHAIR-vi là bản đang dùng (matcher theo âm tiết, xem §10). In đậm là tốt nhất trong các run của repo.

| Hệ | BLEU-4 | METEOR | ROUGE-L | CIDEr-D [CI] | CHAIR_i [CI] | CHAIR_s | Nguồn |
|---|---|---|---|---|---|---|---|
| GRIT, SOTA đã công bố (huấn luyện XE, beam 5, không SCST) | 40.6 | 36.6 | 59.7 | 136.0 | — | — | KTVIC Bảng 3, arXiv 2401.08100; `R2_01_sota_bar.md` |
| P1 s42 (`p1-gold`) | **45.5** | 39.1 | **64.2** | **149.8** [140.9, 159.1] | 19.2 [16.7, 21.7] | 28.7 | [res] `p1-gold-short`; `data/results/score_ci/score_ci_fuse2_s42-vs-p1-short.json` |
| P1 s43 | 45.2 | 39.1 | 64.0 | 143.9 | 17.7 | **26.7** | [res] `p1_s43-short` |
| P1 s44 | 44.8 | 39.1 | 63.8 | 143.7 | 18.3 | 27.6 | [res] `p1_s44-short` |
| P1, trung bình 3 seed (sd) | 45.2 (0.38) | 39.1 (0.01) | 64.0 (0.22) | 145.8 (3.46) | 18.4 (0.74) | 27.7 (0.99) | tính từ ba dòng trên |
| fuse2 s42 | 42.3 | **39.4** | 63.7 | 143.9 [135.4, 152.7] | 21.9 [19.4, 24.5] | 35.8 | [res] `fuse2_s42-short`; score_ci như trên |
| fuse2 s42 + tag Grounding DINO | 43.7 | 39.1 | 63.8 | 146.4 [137.7, 155.1] | 19.5 [16.9, 22.0] | 32.1 | [res] `tags_fuse2_s42-short`; `score_ci_tags_fuse2_s42-vs-p1-short.json` |
| P1 s43 + tag Grounding DINO | 44.7 | 38.7 | 64.0 | 145.0 | **17.5** | **26.7** | [res] `tags_p1_s43-short` |
| E5 (RFT trên mẫu tự sinh) s42 | 41.3 | 38.9 | 62.5 | 137.9 | 22.5 | 36.0 | [res] `e5_s42-short` |
| E5-DPO s42 | 36.4 | 37.4 | 59.6 | 123.1 | 23.0 | 37.6 | [res] `e5dpo_s42-short` |
| MBR k = 1 trên 6 mẫu T = 0.8: P1 s43 / fuse2 s42 | 33.5 / 32.7 | 37.6 / 37.6 | 58.2 / 57.3 | 96.7 / 98.0 | 22.3 / 27.1 | 37.5 / 49.6 | [res] `p1_s43mbr-short`, `fuse2_s42mbr-short` |
| Zero-shot Qwen2.5-VL-7B | 5.5 | 24.4 | 25.6 | 29.0 [26.5, 31.6] | 42.9 [40.3, 45.6] | 62.0 | [res] `zeroshot-short`; `score_ci_zeroshot-vs-p1-short.json` |
| VSPS (bài FAIR), main s42 | 7.0 | 22.1 | 30.9 | 17.3 | 44.6 | 58.8 | [res] `main_s42-short` |

Đọc bảng:
- Cả ba seed P1 vượt GRIT ở mọi n-gram metric.
  - Nhưng số GRIT chép từ bài, chưa chạy lại trên cùng evaluator. METEOR có thể lệch theo bản cài đặt (`R2_01_sota_bar.md`; `manuscript/Q1_GAP.md` mục 4).
  - Không kiểm định ý nghĩa với số chép từ bài khác [R4-00 §6].
- ViG (MAPR 2026, DOI 10.1109/MAPR72750.2026.11685699) tuyên bố vượt GRIT ở mọi metric chuẩn nhưng chưa có số (UNVERIFIED, `R2_01_sota_bar.md`). R6 phải tìm số này trước khi viết "SOTA".
- CIDEr do seed chi phối.
  - Dải ba seed P1 là 6.1 điểm CIDEr, trong khi BLEU-4 chỉ 0.8 và METEOR gần như không đổi.
  - MDE CIDEr là 13.9–16.0 với 1 seed mỗi nhánh và 12.7 với 3 seed mỗi nhánh (khác công thức) [A6 §1.1].
  - Muốn thắng P1 có ý nghĩa (power 0.8, 3 seed mỗi nhánh), trung bình CIDEr cần khoảng 145.8 + 12.7 = 158.5. Nếu không, phải dùng thêm seed.
- MDE 3 seed của CHAIR_i là 3.7 [A6 §1.1]. Mốc tương ứng là khoảng 18.4 − 3.7 = 14.7.
- Số theo âm tiết không so được với số theo từ: P1 s42 đạt CIDEr 165.4 theo âm tiết và 149.8 theo từ [res].
- Trùng ảnh:
  - Khoảng 15/558 ảnh test có bản sao trong KTVIC train (cos ≥ 0.93). Tập đã lọc còn 543 ảnh (`data/dedup/README.md`).
  - 401/558 ảnh test có bản sao trong OpenViIC train [R5-01 §2].

### 2b. Đòn bẩy: bằng chứng nói gì dịch được metric, gì không

| Đòn bẩy | Kết quả đo | Nguồn | Hệ quả cho R6 |
|---|---|---|---|
| Đổi target policy (P1, cons, fuse2, E5…) | Mọi run trên target người hoặc tự sinh nằm trên một đường biên P–số đối tượng. 7 run không phải neo: residual gộp CI [−0.59, +1.07]. E5 (chọn mẫu vì precision) cũng nằm trên đường biên: −0.44 (short), −0.29 (hai câu) | [PRE-V4 §0, §4] | Đổi target chỉ dịch dọc đường biên. Thang 5 policy đang chạy sẽ kiểm điều này (§7) |
| Bằng chứng từ detector: tag Grounding DINO trong prompt | Run duy nhất lệch khỏi đường biên: +1.87 [−0.27, +3.90], CI còn chứa 0. Trên fuse2: CIDEr 143.9 → 146.4, CHAIR_i 21.9 → 19.5, ΔP so với P1 từ −2.2 về 0.0 | [PRE-V4 §4]; [06]; [res] | Bằng chứng thị giác từ ngoài là ứng viên duy nhất từng dịch đường biên. Nhưng lợi P của tag phần lớn là tính điển hình: short +2.1 theo ref KTVIC, +0.8 n.s. theo gold hợp; hai câu +0.2 [−1.5, +1.8] theo P hiệu chỉnh [V5 §7] |
| Tag trên P1 | ΔF1 +0.4 [−0.9, +1.7], n.s. CIDEr 145.0 so với 143.9 (cùng seed 43) | [06]; [res] | Tag chỉ giúp mô hình phủ rộng (fuse2), không giúp P1 |
| MBR k = 1 trên 6 mẫu T = 0.8 | Không phải đòn bẩy precision: P1 R +5.5, P −4.1; fuse2 R +6.0, P −4.9. CIDEr còn 96.7 (P1) và 98.0 (fuse2) | [06]; [res] | Mẫu nhiệt độ cao lệch văn phong tham chiếu. Không dùng mẫu T = 0.8 làm tập ứng viên |
| Ghép lúc huấn luyện so với ghép lúc suy luận | fuse2-detailed hơn P1 tự ghép (k = 2) ở cùng độ dài: ΔP +4.7 [+2.6, +7.0], ΔF1 +3.2 [+1.3, +5.2], p = 0.002 | [06]; commit 63761c0 | Thông tin nằm trong target huấn luyện. Hậu xử lý không tái tạo được |
| Bỏ phiếu mẫu (VTF) trên ảnh chưa thấy | ΔP +2.4 [+0.3, +4.6] theo ref KTVIC; +1.2 [−0.3, +2.9] theo gold hợp; +0.1 [−1.8, +2.1] theo P hiệu chỉnh | [V5 §2.1] | Lợi theo ref KTVIC phần lớn là khớp quy ước của nhóm KTVIC |
| Committee nhiều policy (MBR-F1, cover) | Phần vượt dây cung theo gold hợp: +2.0 [+1.0, +3.0] (short), +2.2 [+1.0, +3.3] (hai câu). P hiệu chỉnh +1.6 [0.0, 3.0] và +2.1 [0.4, 3.7] | [V5 §2.2, §2.6] | Ngoại lệ duy nhất sống qua panel độc lập. Tốn K lần suy luận |
| RFT trên mẫu tự sinh (E5) | Null: short F1 57.3 so với 58.1; CIDEr 137.9 so với 143.9 | [06]; [res] | Trên ảnh đã train, mẫu "tốt nhất" là caption nhớ lại |
| DPO (E5-DPO) | Short hỏng: CIDEr 123.1, F1 54.8 | [06]; [res] | Cặp chỉ có prompt detailed làm hỏng văn phong short |
| Prompt "hai câu" cho P1 | P1 vẫn viết 1 câu (11.9 từ). Zero-shot với prompt này đạt F1 42.5 | [06] | Độ dài do target quyết định, không do prompt |
| Độ dài dưới CIDEr-D | fuse2-detailed: CIDEr-D 23.9, CIDEr không phạt độ dài 100.4 | `data/results/metrics_v2/TABLE.md` | Mode hai câu không thể thắng CIDEr-D. R6 nhắm short |
| Seed và template | CIDEr 149.8 / 143.9 / 143.7, F1 sd 0.56. Hai seed P1 viết cùng caption short ở 234/558 ảnh; CIDEr thưởng việc khớp template của tham chiếu | [A6 §0 mục 5, §1.1] | Nhiễu CIDEr chủ yếu đến từ chọn template. Mọi so sánh CIDEr cần ≥ 3 seed |
| Ghi nhớ | Loss giảm 0.074 nats/token qua ranh giới epoch, nhiều hơn lợi khi gấp đôi dữ liệu mới (khoảng 0.05). Epoch 2 chủ yếu ghi nhớ. P1 chép nguyên văn 21.5% (reviewer vòng 1 đo, chưa tái lập trong repo) | [A6 §1.2] | R6 phải báo tỉ lệ chép nguyên văn và số trên tập 543 ảnh |
| Biến thể adapter (rank, DoRA, LoRA+), curriculum | Không chạy. Lợi đã công bố 0.7–1.9 điểm, dưới MDE 2.5–3.8 | [A6 §0 mục 2, 4] | Không đáng thử |
| CLIP-S, BERTScore | fuse2 = P1 (BERT-F 0.95, CLIP-S 0.54, RefCLIP-S 0.66). CLIP-S chấm zero-shot (0.65) cao hơn mô hình đã fine-tune | [06]; `metrics_v2/TABLE.md` | Không dùng CLIP-S làm metric chính |
| Chưa đo | 1024 token thị giác (job 73 chưa xếp), backbone 3B (57/58 đang xếp), loss mask (§8) | — | chưa có |

### 2c. Chẩn đoán làm xương sống cho phương pháp

1. **Metric theo tham chiếu KTVIC thưởng tính điển hình.**
   - Bảng X (§4): panel độc lập giảm một nửa chi phí P của fusion. Target người đã mang phần lớn phần còn lại.
   - Các bước chọn lúc suy luận tăng P theo ref KTVIC nhưng mất phần lớn lợi đó theo gold hợp, và gần hết theo P hiệu chỉnh [V5 §0b].
   - Hệ quả: phương pháp nào tăng CIDEr, BLEU, ROUGE-L hoặc giảm CHAIR theo ref KTVIC thì phần lớn đang khớp quy ước viết của nhóm KTVIC. R6 được làm vậy, vì đó là benchmark. Nhưng mọi câu về độ trung thực phải kèm P theo gold hợp hai panel và P hiệu chỉnh.
2. **Đường biên bất biến.**
   - Đổi target chỉ dịch dọc một đường biên. Chỉ bằng chứng thị giác từ ngoài từng lệch khỏi nó (+1.87, chưa có ý nghĩa) [PRE-V4].
   - Hệ quả: muốn CHAIR thấp hơn ở cùng độ phủ thì phải đưa thông tin mới vào (bằng chứng thị giác, hoặc một learner khác). Phải chứng minh bằng residual dương so với đường biên, CI không chứa 0, ở cùng số đối tượng.
   - Dự báo của R6 nên đăng ký trước theo đúng khuôn của [PRE].
3. **Dư địa precision thật còn nhỏ.**
   - P hiệu chỉnh: P1-short 98.3 [95.8, 100], fuse2-short 97.6 [95.0, 100] [V5 §2.6]. Dư địa thật ở short khoảng 2.4 điểm, dưới MDE một seed. Ước lượng này dựa trên giả định độ nhạy của panel (V3 P5).
   - CHAIR_i 18–22 theo ref KTVIC phần lớn là tham chiếu thiếu và khác cách gọi tên. "Lỗi" gọi tên của P1 được panel thứ hai xác nhận như của người: 68.7% [59.4, 78.2] so với 67.5% [60.6, 74.6] [V5 §2.4].
4. **Thông tin phải có ngay trong huấn luyện.** Ghép lúc huấn luyện thắng ghép lúc suy luận. RFT trên ảnh đã thấy là null. MBR trên mẫu T = 0.8 làm hỏng văn phong (§2b).
5. **CIDEr là metric của template.** Nhiễu seed lớn và chủ yếu do template; CIDEr-D phạt độ dài. Phương pháp nhắm CIDEr phải được đo bằng trung bình nhiều seed và bootstrap 2 tầng seed × ảnh.

### 2d. Ràng buộc cho R6

- **Dữ liệu.** Chỉ dataset và nhãn người có sẵn. Không gán nhãn. AI-silver không phải bằng chứng [R4-00].
- **Không train trên UIT-OpenViIC.** 401/558 ảnh test KTVIC có bản sao trong OpenViIC train, và OpenViIC là panel đánh giá độc lập [R5-01; V5 §7].
- **Ảnh ngoài làm dữ liệu train** (UIT-ViIC, COCO, XM3600) phải được kiểm trùng với KTVIC test trước, theo luật hai tín hiệu của `scripts/match_openviic.py`.
- **Phần cứng.** Một RTX 3090 24 GB. Mỗi thí nghiệm khoảng ≤ 10 GPU-h (`R2/CONTEXT.md`). Báo tổng GPU-h. Chỉ dùng mô hình mở, không API trả phí [R4-00 §6].
- **Tập test.**
  - Không chỉnh gì trên 558 ảnh test.
  - Chọn cấu hình trên nửa cross-fit của train. `xfit/gold_fuse2_A` và `_B` đã có trên n3 (3,768 và 3,770 dòng) [R4-00 §6; Q-n3].
- **Đánh giá.**
  - Word-level RDRSegmenter cho mọi n-gram metric.
  - ≥ 3 seed mỗi nhánh. So với P1 trung bình 3 seed (145.8), không với seed tốt nhất (149.8).
  - Bootstrap 2 tầng seed × ảnh, hiệu chỉnh Holm.
  - Báo thêm tập 543 ảnh và tỉ lệ chép nguyên văn.
- **CHAIR.** Matcher đã sửa (V2) cho mọi số mới, kèm số theo matcher cũ để đối chiếu bài FAIR (§10).
- **GRIT.** Chạy lại GRIT-vicap trên cùng evaluator, hoặc ghi rõ "số chép từ bài, không kiểm định" (`Q1_GAP.md` mục 4; [R4-00 §6]).
- **Loss mask.** R6 dùng cùng mask với baseline của nó, theo quyết định ở §8.
- **Prior art chỉ được làm baseline, không làm novelty:**
  - SCST tối ưu CIDEr (1612.00563). Bảng 3 của KTVIC chưa dùng SCST.
  - MBR: Jinnai et al. 2311.05263, ASC 2405.13131, IC3 2302.01328.
  - Ensemble/committee: Graphene 2110.09131, UA-MBR 2503.05318, ATED 2510.18321.
  - Tag trong prompt: OSCAR, VinVL, Tag2Text 2303.05657.
  - RL thưởng theo đối tượng: BalCapRL 2605.07394, CCCaption 2602.21655, ClaimDiff-RL 2605.20278, VCap 2605.28023.
  - DPO chống ảo giác: HALVA 2405.18654, TL-DPO 2506.11417.
  - Nguồn: [R4-00 §2b]; [V5 §4].
- **Không đề xuất lại** 29 ý tưởng đã loại ở R4-00 §2b và 10 ứng viên ở V5 §3 nếu chưa sửa được lý do chúng bị loại.

## 3. Storyline và đóng góp xếp hạng (tạm thời, cập nhật sau vòng R6 (phương pháp))

Ô "phương pháp" để trống cho R6. Nếu R6 có phương pháp, nó thành đóng góp 1, và các mục dưới đây thành phân tích hỗ trợ.

### 3a. Storyline

1. **Vấn đề.**
   - P1 (SFT trên caption đầu tiên) chính xác nhưng nêu ít đối tượng: short P 77.9, R 41.4 [06].
   - Trên cùng gold 4 caption, một caption tham chiếu giữ lại đạt R 46.9 [45.1, 48.7]. P1 kém nó 4.1 [1.8, 6.4] điểm R [R4-01 §2a].
2. **Recipe.**
   - Target SFT = caption đồng thuận (prompt short) + ghép tham lam 2 caption người (prompt detailed). Chỉ trích xuất, không LLM (`scripts/build_gold_sft.py`).
   - Ở cùng độ dài: R +5.7, F1 +4.0 (§1).
   - Không thay được bằng ghép mẫu lúc suy luận (§2b).
3. **Cái giá nhìn thấy.** Theo 5 ref KTVIC, mode hai câu mất P: ΔP −10.4 [−13.0, −7.8] [R5-01 §4].
4. **Phân tích trung tâm.**
   - Panel người thứ hai (UIT-OpenViIC, 555/558 ảnh test) tách cái giá đó thành ba phần (Bảng X, §4).
   - Thêm ref của chính nhóm KTVIC không thu hẹp khoảng cách: −9.7 đến −11.1 (R4-00 §2b VN1; số "đo trong vòng", chưa tái lập). Thêm một panel của nhóm khác thì khoảng cách giảm một nửa.
5. **Cơ chế.** Mọi target policy chung một đường biên precision–số đối tượng (§5b), đã đăng ký trước.
6. **Mỏ neo sự thật.**
   - Nhãn instance COCO có sẵn cho hai cận. Cảnh thể thao (UIT-ViIC) gần như không mất P theo instance. Cảnh COCO chung mất tới khoảng một nửa (§5a).
   - Mức mô hình chờ job 36, 38, 52_a/52_b.
7. **Vệ sinh đánh giá tiếng Việt.** CHAIR-vi v2 và dải độ nhạy NAP không đổi thứ hạng nào [V2 §1.6].

### 3b. Đóng góp xếp hạng

| # | Đóng góp | Trạng thái bằng chứng | Số chính (nguồn) | Câu được phép viết | Không được viết |
|---|---|---|---|---|---|
| 0 | Phương pháp R6 | chưa có | chưa có | chưa có | — |
| 1 | Đánh giá hai panel chi phí precision của fusion (Bảng X, DiD) | **Đã có** (R5-01 trong repo; DiD trong `R2`). **Cần tính, 0 GPU:** port `scripts/two_gold_audit.py` (~250 dòng, ~30–40 phút CPU, V3 §4). **Chờ GPU:** hàng fuse2 s43/s44 | §4 | V3: "An independent panel halves fusion's precision cost; most of the remainder is already in the fused human references; the model adds 1–2 points." Bản dài ở §4 | "typicality, not truth"; "96% là thật"; "không có ảo giác" |
| 2 | Recipe fusion chỉ dùng chữ người, có đối chứng cùng độ dài và cùng số bước | **Đã có** (1 seed fuse2). **Chờ GPU:** fuse2 s43/s44 (50, 51), p1ep4 (56) | short R +5.7 [+3.9, +7.7], F1 +4.0 [+2.1, +6.1]; tự ghép k = 2: ΔF1 +3.2 [+1.3, +5.2] [06] | "At equal length, training on fused human references raises object recall by 5.7 points [3.9, 7.7] over training on the first caption; CIDEr differences are within seed noise." Thay bằng trung bình 3 seed khi có | "first to fuse", "no trade-off", "reduces hallucination", "detailed captioning" |
| 3 | Đường biên bất biến, đăng ký trước | **Đã đăng ký trước, chờ GPU** (40, 41, 42, 55, 56, 50, 51) | residual gộp 7 run: CI [−0.59, +1.07]; tag +1.87 [−0.27, +3.90] [PRE-V4 §0, §4] | Chỉ khi H0 đạt: "Every policy trained on human or self-sampled targets falls on one precision–count frontier; fusion's F1 gain is a move along it, not a better learner." | "fusion lowers an implicit threshold"; "τ = 0.5 explains P1's recall" |
| 4 | Cận sự thật bằng nhãn instance COCO có sẵn | **Đã có** ở mức target (V3). **Cần tính, 0 GPU:** lexicon v2, chấm G3'. **Chờ GPU** ở mức mô hình (36, 38, 52_a/52_b) | UIT-ViIC, lớp ngoài nhóm chọn ảnh: dP_ref −7.38 [−9.25, −5.60], dP_inst +0.63 [−0.46, +1.73]. COCO-5000: −7.67 [−8.06, −7.30] và −4.00 [−4.30, −3.68] [V3 §0] | V3: "On exhaustively labelled COCO-80 objects, fused references lose no instance precision in sports scenes (UIT-ViIC, excluding the two classes present in every image) and at most about half of their reference-precision loss in general scenes (COCO)." | Chuyển "+0.0" của UIT-ViIC sang KTVIC; gọi instance COCO là gold đầy đủ |
| 5 | Vệ sinh metric đối tượng tiếng Việt (CHAIR-vi v2, NAP, φ) | **Cần tính, 0 GPU** (~1 ngày công, V2 §4) | 29–44% mention sai theo tham chiếu là lỗi tách từ hoặc tên đồng nghĩa/thượng vị; không thứ hạng nào đổi (19 luật P × 7 định nghĩa R); φ đạt AUROC 0.961 trên Flickr30k Entities [V2] | "Naming and segmentation account for 29–44% of reference-false mentions; no system ranking changes under any matcher." | "khoảng một nửa ảo giác là do gọi tên"; báo NAP-P một mình |
| 6 | Committee nhiều policy (phân tích lúc suy luận) | **Pilot đã có** (V5). **Chờ GPU** cho thành viên (thang, seed); 0 GPU-h thêm | Gold hợp, phần vượt dây cung +2.0 (short), +2.2 (hai câu), CI không chứa 0; P hiệu chỉnh +1.6 [0.0, 3.0] và +2.1 [0.4, 3.7] [V5; `R2/V_V5/v5_headroom_cls.log`] | "A committee of captioners trained under different reference policies gains about 2 points of union-gold precision at matched object count, at K× inference cost." Trình bày như phân tích | hệ triển khai; "novel ensemble" |

Lý do xếp hạng:
- 1 có bằng chứng mạnh nhất và mới nhất. V3 kết luận nó đủ mức Q1 khi là phần phân tích, không đủ khi là đóng góp chính.
- 2 thực dụng nhưng incremental (VBCS, Zheng 2018, LLaVA, FuseCap, CCCaption; R4-00 §5).
- 3 rẻ và trung thực, novelty thấp đến vừa [PRE-V4 §5].
- 4 còn chờ job đang chạy. 5 và 6 là phụ.

Phải cite (từ V1–V5): Chen et al. 2015 §4.2 (Precision-at-Human-Recall, 1504.00325), CHAIR §2.1 (1809.02156), Misra 2016 (1512.06974), Feng 2024 (2406.12663), RePOPE (2504.15707), CCCaption (2602.21655), HalCECE (2503.00436), VALOR-EVAL (2404.13874), hierarchical P/R CVPR 2025 (2504.05457), Hodosh 2010, Young 2014, ManyNames, Menon 2015, Elkan–Noto 2008, Lipton 2014.

## 4. Bảng X trung tâm: DiD hai panel trên KTVIC

**Bảng X. Chi phí precision của fusion dưới bằng chứng người độc lập (KTVIC test, 555 ảnh có panel OpenViIC).**

**Panel A. Mô hình. Gold = 5 ref KTVIC, so với hợp 5 ref KTVIC + panel OpenViIC (B = 5000)** [R5-01 §4; `data/results/second_panel.json`]

| So sánh (cùng prompt; fuse2 luôn là seed 42) | ΔP, gold KTVIC | ΔP, gold hợp | ΔF1, gold hợp |
|---|---|---|---|
| fuse2 − P1 s42, hai câu | −10.4 [−13.0, −7.8] | −5.2 [−7.1, −3.2] | +15.1 [13.7, 16.5] |
| fuse2 − P1 s43, hai câu | −11.9 [−14.6, −9.4] | −6.0 [−7.8, −4.1] | +15.5 [14.1, 16.9] |
| fuse2 − P1 s44, hai câu | −10.6 [−13.2, −8.0] | −6.5 [−8.4, −4.6] | +14.6 [13.2, 16.1] |
| fuse2 − P1 s42, short | −2.2 [−4.9, +0.4] | −1.1 [−3.0, +0.9] | +4.5 [3.1, 6.0] |

**Panel B. Hiệu của hiệu (DiD): mô hình so với chính target người của nó, cùng ảnh, cùng gold** [V3 §2b; `R2/V_V3/v3_ktvic_did.log`]

Mỗi fold dựng target người từ 3 caption KTVIC. Gold là 2 caption KTVIC còn lại, có hoặc không thêm panel OpenViIC.
- Hai câu: mô hình = fuse2_s42-detailed − P1-short; target = `fused()` của 2 caption − caption sớm nhất.
- Short: mô hình = fuse2_s42-short − P1-short; target = caption đồng thuận − caption sớm nhất.
- DiD = mô hình − target. Target người giống nhau ở cả ba dòng của một mode.

| Mode | P1 | ΔP mô hình, 2 KTVIC | ΔP target, 2 KTVIC | DiD, 2 KTVIC | ΔP mô hình, + OpenViIC | ΔP target, + OpenViIC | DiD, + OpenViIC |
|---|---|---|---|---|---|---|---|
| hai câu | s42 | −11.19 [−13.31, −9.16] | −8.36 [−9.76, −6.94] | −2.83 [−5.28, −0.47] | −4.87 [−6.88, −2.95] | −3.61 [−4.57, −2.67] | −1.26 [−3.44, +0.84] |
| hai câu | s43 | −12.23 [−14.42, −10.08] | −8.36 | −3.87 [−6.39, −1.43] | −5.44 [−7.50, −3.41] | −3.61 | −1.83 [−3.99, +0.37] |
| hai câu | s44 | −11.76 [−13.86, −9.64] | −8.36 | −3.40 [−5.90, −0.99] | −5.98 [−8.02, −4.03] | −3.61 | **−2.36 [−4.45, −0.28]** |
| short | s42 | −2.51 [−4.63, −0.35] | −1.70 [−2.91, −0.50] | −0.81 [−3.20, +1.65] | −0.89 [−2.78, +1.03] | −0.21 [−0.83, +0.45] | −0.68 [−2.71, +1.33] |
| short | s43 | −3.55 [−5.71, −1.40] | −1.70 | −1.85 [−4.38, +0.58] | −1.46 [−3.37, +0.42] | −0.21 | −1.25 [−3.26, +0.72] |
| short | s44 | −3.08 [−5.22, −0.80] | −1.70 | −1.38 [−3.80, +1.08] | −1.99 [−3.90, −0.11] | −0.21 | −1.78 [−3.79, +0.21] |

**Panel C. Target huấn luyện, KTVIC train (3,724 ảnh có panel OpenViIC)** [V3; `R2/V_V3/v3_ktvic_targets_panel.log`]

| Gold | P của p1 | P của fuse2 | ΔP fuse2 − p1 |
|---|---|---|---|
| 2 caption KTVIC giữ lại | 71.82 | 62.94 | −8.88 [−9.42, −8.34] |
| panel OpenViIC | 78.04 | 73.30 | −4.74 [−5.21, −4.21] |
| hợp | 90.44 | 85.97 | −4.47 [−4.86, −4.08] |

- Phần mention sai theo KTVIC mà OpenViIC xác nhận: p1 66.1% [64.6, 67.5], fuse2 62.1% [61.1, 63.2], Δ −3.9 [−5.0, −2.9].
- Mention chưa được xác nhận, fuse2 − p1: +0.222 [0.21, 0.23] mỗi target.

**Panel D. Mention không panel nào xác nhận, mỗi caption (test)** [`R2/V_V3/v3_ktvic_test_same_gold.log`]
- Hai câu: mô hình +0.335 [0.281, 0.394]; target người +0.208 [0.182, 0.235]; phần riêng của mô hình +0.127 [0.070, 0.187]. Đây là cận trên của ảo giác mà fusion thêm vào ngoài tham chiếu.
- Short: mô hình +0.058 [0.018, 0.097].
- Với gold 5 ref KTVIC: fuse2-detailed − P1 s42 là +0.29 [0.24, 0.34] [R5-01 §4].

**Cách đọc**
- Hai câu: theo 2 ref KTVIC, mô hình mất 11.2–12.2 điểm P. Thêm panel độc lập thì còn 4.9–6.0, khoảng một nửa.
- Trong phần còn lại, 3.6 điểm đã có sẵn trong target người được ghép.
- Phần riêng của mô hình là 1.3–2.4 điểm, chỉ có ý nghĩa với seed P1 44.
- Short: không DiD nào có ý nghĩa.

**Câu cho bài** (V3 §4, giữ nguyên): "Against the dataset's own references, training on fused references costs 11 points of object precision in two-sentence mode. Against an independent second panel of the same images the cost falls to 5–6 points, of which 3.6 are already present in the fused human references; the trained model adds 1–2 points (significant for one of three P1 seeds)."

**Còn thiếu**
- Hàng fuse2 s43 và s44 (job 50, 51). Khi về, chạy lại Panel A và B với bootstrap 2 tầng seed × ảnh (V3 §3).
- Script trong repo: `scripts/two_gold_audit.py`, chưa có. Port từ `R2/V_V3/v3_ktvic_did.py` và `v3_ktvic_targets_panel.py`.
- Giới hạn ghi cạnh bảng: panel thứ hai là một panel người khác, không phải sự thật. Hai panel phủ khoảng 84.4% [83.0, 85.6] số lớp nhắc được, và đây là cận trên [R5-01 §6].

## 5. Hình

### 5a. Mặt phẳng điển hình – sự thật (Hình Y của V3)

- Trục x: ΔP(fuse2 − P1) theo tham chiếu của chính dataset.
- Trục y: ΔP theo gold độc lập. KTVIC dùng hợp với OpenViIC; UIT-ViIC và COCO dùng nhãn instance COCO-2014.
- Hai đường: y = x (toàn bộ chi phí là sự thật) và y = 0 (toàn bộ là tính điển hình).
- Mỗi điểm có CI hai chiều. Ký hiệu điểm phân biệt "gold là panel người" với "gold là instance".

| Điểm | x | y | Nguồn |
|---|---|---|---|
| KTVIC test, mô hình hai câu, P1 s42 / s43 / s44 | −11.19 / −12.23 / −11.76 | −4.87 / −5.44 / −5.98 | `R2/V_V3/v3_ktvic_did.log` |
| KTVIC test, target người hai câu | −8.36 | −3.61 | như trên |
| KTVIC test, mô hình short, P1 s42 / s43 / s44 | −2.51 / −3.55 / −3.08 | −0.89 / −1.46 / −1.99 | như trên |
| KTVIC test, target người short | −1.70 | −0.21 | như trên |
| KTVIC train, target người | −8.88 | −4.47 | `R2/V_V3/v3_ktvic_targets_panel.log` |
| UIT-ViIC train, target người, lớp ngoài nhóm chọn ảnh, caption Việt (có gợi ý lớp) | −7.38 [−9.25, −5.60] | +0.63 [−0.46, +1.73] | `R2/V_V3/v3_family.log` |
| như trên, caption Anh của COCO (không gợi ý) | −6.08 [−7.88, −4.40] | −0.38 [−1.40, +0.62] | `R2/V_V3/v3_english.log` |
| COCO Karpathy test 5,000, target người, mọi lớp | −7.67 [−8.06, −7.30] | −4.00 [−4.30, −3.68] | `R2/V_V3/v3_english_clean.log` |
| như trên, 36 lớp tin cậy (chọn trên Karpathy val) | −6.22 [−6.72, −5.77] | −3.33 [−3.66, −2.99] | như trên |
| mô hình UIT-ViIC trong miền (52_a/52_b) | chưa có | chưa có | job 52 |
| mô hình KTVIC trên COCO 2,500 ảnh | chưa có | chưa có | job 36 |
| fuse2 s43 / s44 | chưa có | chưa có | job 50, 51 |

- UIT-ViIC bỏ hai lớp có mặt ở gần như mọi ảnh: sports ball 100.0%, person 97.5% số ảnh; hai lớp này chiếm 83.9% số mention [V3 §1b].
- Script: `scripts/two_gold_audit.py` (chưa có) xuất cả Bảng X và hình này.

### 5b. Đường biên bất biến, đăng ký trước (V4)

- Trục x: số lớp đối tượng mỗi caption, M. Trục y: P theo hợp 5 ref KTVIC (Bảng IV), 558 ảnh.
- Đường biên đóng băng từ P1 (3 seed, short) và fuse2_s42-detailed: TP(M) = 1.3996 · (M / 1.7826)^0.7468, P = 100 · TP / M, R = 5.486 + 25.982 · TP [PRE `anchors.frontier`].
- Vẽ mọi run đã train, hộp dự báo cho p1ep4, multiref, cons, unf2, rnd2 và fuse2 s43/s44 [PRE `runs`], và các đường iso-F1.
- Tag lệch khỏi đường biên (+1.87 [−0.27, +3.90]). Zero-shot là một learner khác (−22.5) [PRE-V4 §4].
- Điểm "1 caption người" (1v4: 1.74 đối tượng mỗi caption, P 85.3, R 46.9 [R4-01 §2a]) dùng gold 4 caption. Vẽ ở panel phụ, cùng các hệ chấm trên đúng gold đó.

Residual đã quan sát (P trừ P của đường biên tại cùng M) [PRE-V4 §4]:

| Run | residual P [CI] |
|---|---|
| fuse2_s42-short | +0.34 [−1.58, +2.29] |
| e5_s42-short | −0.44 [−2.46, +1.59] |
| e5_s42-detailed | −0.29 [−1.82, +1.16] |
| p1_s43-two | +0.25 [−0.95, +1.56] |
| P1-detailed, 3 seed | +0.31, +1.21, +0.26 |
| tags_fuse2-short | +1.87 [−0.27, +3.90] |

Trên 7 run không phải neo, residual gộp có CI [−0.59, +1.07] [PRE-V4 §0].

Lệnh kiểm: `NCS_DATA=data python3 scripts/prereg_ladder_check.py --check`.
- **Lỗi đường dẫn:** script đọc `scripts/PREDICTIONS.json`, file này không có trong repo. Phải trỏ sang `manuscript/prereg/2026-10-12_ladder_predictions.json` trước khi chấm.
- Không dựng lại dự báo. Chỉ dùng file đã commit ở 1b5d16b.

## 6. Ý tưởng bị loại hoặc hạ cấp

| Ý tưởng | Kết luận | Lý do (nguồn) |
|---|---|---|
| IFCR, precision hiệu chỉnh kiểu capture-recapture (A4) | Loại; còn một bảng phụ lục | 5 caption KTVIC không hoán đổi được (Jaccard cặp kề − không kề +0.121 [+0.108, +0.134]). IFCR hiệu chỉnh thiếu so với cận dưới hai panel ở mọi mô hình: P1 −2.9 [−5.5, −1.9], fuse2-detailed −7.6 [−10.1, −5.8]. Phép thử độ khớp gắn cờ sai 23–54% hệ đúng mô hình ở n = 558 [V1] |
| Cơ chế ngưỡng ngầm (A1 ý 2) | Loại cơ chế; mệnh đề vào phụ lục, giữ đường biên bất biến | P1 nêu 1.78 đối tượng mỗi ảnh, mô hình ngưỡng dự báo 1.24 (+44%). "Target dài hơn thì nêu nhiều hơn" khớp mọi số đếm trong 4.4%. Định lý là sách giáo khoa (Menon 2015, Elkan–Noto 2008, Lipton 2014) [V4] |
| ART, dòng lấy mẫu lại theo annotator (A1) | Hoãn/loại | Dòng short bị multiref (đã xếp) trội trên mọi gold: +2.76 [2.39, 3.11] so với +1.34 [1.00, 1.68]. Dòng hai câu đảo chiều với panel độc lập: −0.87 [−1.17, −0.55] [V5 §2.5] |
| CNC, tương phản gọi tên đồng thuận (A2) | Loại | "Lỗi" gọi tên của P1 được OpenViIC xác nhận như của người: 68.7% [59.4, 78.2] so với 67.5% [60.6, 74.6]. Trần lợi khoảng 1.6 P [V5 §2.4] |
| CMPC, cặp tối thiểu có chứng nhận (A2) | Loại | Chính A2 ước 20% tin cậy, ≤ 1.2 P; 7 GPU-h; prior mDPO, S-VCO, V-DPO [V5 §3] |
| Tự chưng cất VTF (A8 D1) | Loại | VTF − greedy trên ảnh chưa thấy ≈ 0 theo P hiệu chỉnh (+0.1 [−1.8, +2.1]). E5 đã null. Nhánh SFT trên OpenViIC làm nhiễm panel độc lập [V5 §2.1, §3] |
| Số học LoRA P1↔fuse2 (A3) | Loại | Nội suy nằm trên dây cung (rewarded soups 2306.04488); 9.1 GPU-h [V5 §3] |
| xl-fuse (A5), grid A6, A8 D2 | Hoãn | xl-fuse chỉ phủ miền COCO và cần bước dịch bằng LLM. Grid 9.25 GPU-h không trả lời câu hỏi nào mà thang chưa trả lời. D2 chờ job 60/61 [V5 §3] |
| I1, MBR mức đối tượng (R4-00 giữ) | Hạ thành không chọn | Bỏ phiếu mẫu: +2.4 P theo ref KTVIC, +1.2 n.s. theo gold hợp, +0.1 [−1.8, +2.1] theo P hiệu chỉnh [V5 §2.1] |
| Kênh tag Grounding DINO làm đóng góp | Hạ cấp | Lợi P là tính điển hình: short +2.1 (ref KTVIC) → +0.8 n.s. (hợp); hai câu +0.2 [−1.5, +1.8] theo P hiệu chỉnh [V5 §7] |
| Khẩu hiệu "typicality, not truth" | Loại; thay bằng câu của V3 | Là hệ quả của cách chọn ảnh UIT-ViIC: sports ball có ở 100.0% ảnh, person ở 97.5%; xác suất có mặt ngẫu nhiên 87.6%. Trên COCO chung dP_inst −4.00 [−4.30, −3.68] [V3 §0] |
| NAP làm đóng góp chính | Hạ thành phụ | Không đổi thứ hạng nào. Tín dụng thượng vị đã có ở HalCECE (2503.00436) và VALOR-EVAL (2404.13874) [V2 §2, §3] |
| Nhãn AI-silver (`annot_claude.json`) | Loại khỏi bài | Nhãn do mô hình AI tạo, không phải gold người [R4-00 §1, §6]. Bảng silver trong 06 không được dùng |
| Gán nhãn mới (kit `annotation/`) | Không làm | Quyết định của tác giả ngày 12/10 [R4-00]. Panel OpenViIC có sẵn thay vai trò này cho KTVIC [R5-01] |
| Cổng G3 cũ (≥ 50% mention sai theo tham chiếu có instance) | Thay bằng G3' | Không thể trượt trên UIT-ViIC: target người đạt 98.6% [97.8, 99.3], mức ngẫu nhiên khoảng 88% [V3 P3] |
| Cổng G5 (Kendall τ_b ≥ 0.71) | Không còn là phép thử | Riêng độ dài target đã cho τ_b 0.87 [V4 §3] |

## 7. Thí nghiệm còn lại và cổng

### 7a. Ảnh chụp hàng đợi (chỉ đọc)

**n2**, đọc lúc 11:15 UTC 12/10 [Q-n2]
- Đang chạy: `33_p1_maskfix_s42`, train ở bước 201/942, 7.1 s/bước.
- Đã xong hôm nay: 30_p1_s43, 31_p1_s44, 32_tags_p1_s43, 34_metrics_clip_bert, 35_lenmatch, 36_coco_a_p1_s43.
- Chờ, theo thứ tự: 36_coco_b_fuse2_s42, 36_coco_c_score, 37_pope_a/b/c/d, 38_uitviic_eval, 39_xm3600_eval, 40_multiref_s42, 41_ladder_rnd2_s42, 42_ladder_unf2_s42, 90_pilot_resume.
- Lỗi: 26 và 33_metrics_clip_bert (đã chạy lại thành 34). Bỏ qua: 23_ctrl_fuse2plus1.

**n3**, đọc lúc 11:16 UTC [Q-n3]
- Đang chạy: `50_fuse2_s44`, bước 1,424/1,884, 7.46 s/bước.
- Lỗi: 50_fuse2_s43 (máy khởi động lại lúc 08:09 UTC; thay bằng 51).
- Chờ: 50_b_fuse2_maskfix_s42, 51_fuse2_s43_resume, 52_a_uitviic_p1_s42, 52_b_uitviic_fuse2_s42, 55_ladder_cons_s42, 56_p1_4ep_s42, 57_p1_3b_s42, 58_fuse2_3b_s42, 60–63 xfit.

Ghi chú:
- `qrun.sh` chạy `/root/queue/*.sh` theo thứ tự tên. `50_b_…` đứng trước `51_…`, nên chạy ngay sau `50_fuse2_s44`.
- Code trên cả hai máy đã có cờ `--loss-mask` (`train_stage2.py` sửa lúc 09:49–09:50 UTC). Mặc định vẫn là `legacy`.
- `50_fuse2_s44` bắt đầu lúc 08:18 UTC, trước khi code mới được chép lên, nên cùng chế độ với các run cũ.
- Job 70–83 của R4-00 không có trong hàng đợi nào.

GPU-h và ETA dưới đây là ước tính, sai số vài giờ. Chúng dựa trên:
- tốc độ đo được: 7.32–7.46 s/bước;
- thời gian eval: khoảng 0.23 h mỗi mode cho caption một câu (job 30, 32), 0.64 h cho hai mode của fuse2 (job 25_b);
- ước tính ghi trong từng script.

### 7b. n2

| Job | GPU-h (ước) | ETA, giờ VN (ước) | Quyết định được gate | Tiêu chí đạt/trượt | Nguồn tiêu chí |
|---|---|---|---|---|---|
| 33_p1_maskfix_s42 | ≈ 2.6 | 20:30 12/10 | Loss mask | §8 | file này |
| 36_coco_b_fuse2_s42, 36_coco_c_score | ≈ 2.2 + chấm CPU | 00:00 13/10 | Đóng góp 4, mức mô hình trên COCO | τ_model − τ_human có cận trên CI 95% < +0.15 thì viết "không tệ hơn fusion của người". τ_human = 0.54 [0.50, 0.59] (mọi lớp), 0.51 [0.45, 0.57] (36 lớp tin cậy). Chấm lại bằng lexicon v2 trên CPU; số mà 36_coco_c tự in dùng lexicon v1 | V3 §4 |
| 37_pope_a/b/c/d | ≈ 3.0 | 03:00 13/10 | RePOPE hỏi bằng tiếng Việt (R4-00 §5 mục 14); vi/en báo cạnh nhau (§9) | Đăng ký ở đây: CI 95% của ΔF1 (fuse2 − P1, nhãn RePOPE, câu hỏi tiếng Việt) chứa 0 hoặc dương thì viết "không thấy tăng ảo giác trên RePOPE". CI toàn âm thì ghi là giới hạn | file này |
| 38_uitviic_eval | ≈ 1.2 | 04:15 13/10 | Không gate. Bằng chứng phụ cho G3'a | Chấm theo định nghĩa G3'a (lớp ngoài nhóm chọn ảnh, lexicon v2). Chỉ báo cáo, vì n = 231 | V3 |
| 39_xm3600_eval | ≈ 2.7 | 07:00 13/10 | Ngoài miền, chấm bằng nhãn OIV7 do người kiểm; vi/en báo cạnh nhau (§9) | Đăng ký ở đây: ΔR theo nhãn dương đã kiểm (fuse2 − P1, short) > 0 với CI không chứa 0 thì viết "recall tăng cả ngoài miền". Δ mention rơi vào nhãn âm đã kiểm, mỗi caption: CI chứa 0 thì viết "không thêm ảo giác đã kiểm"; CI toàn dương thì ghi là giới hạn | file này |
| 40_multiref_s42 | ≈ 5.3 (2,356 bước) | 12:00 13/10 | Đường biên (H0), D1, H1-variance; thành viên committee | Dự báo M 1.74 [1.65, 1.84], P 79.0 [76.9, 81.1], R 41.2 [38.7, 43.7]. D1: M ≥ 1.65 ủng hộ L, 1.28–1.42 ủng hộ T. H1-variance: residual ≥ +1.0 với CI không chứa 0 | [PRE] |
| 41_ladder_rnd2_s42 | ≈ 4.5 | 16:30 13/10 | Đường biên; vai trò của chọn tham lam; G10 | rnd2-detailed: M 2.58 [2.46, 2.71], P 71.5 [69.6, 73.4], R 53.4 [50.7, 56.2], ≥ 1.95 câu, M/M_fuse2 trong [0.78, 0.86]. rnd2-short bằng fuse2-short (H0). G10: \|ΔF1 rnd2 − fuse2 (hai câu)\| < 1.5 thì chạy 76, ngược lại bỏ 76 | [PRE]; [R4-00 §4e] |
| 42_ladder_unf2_s42 | ≈ 4.6 | 21:00 13/10 | Đường biên; D4 | unf2-short: M 2.21 [2.10, 2.32], P 74.4 [72.5, 76.4], R 48.2 [45.5, 50.8]. D4: unf2/cons ≥ 0.97 ủng hộ L, ≤ 0.95 ủng hộ T | [PRE] |
| 90_pilot_resume | không rõ | — | Không gate gì (pipeline VSPS cũ) | Đề nghị tác giả gỡ khỏi hàng đợi | — |

### 7c. n3

| Job | GPU-h (ước) | ETA, giờ VN (ước) | Quyết định được gate | Tiêu chí đạt/trượt | Nguồn tiêu chí |
|---|---|---|---|---|---|
| 50_fuse2_s44 | ≈ 4.5 | 20:00 12/10 | Claim 3 seed của đóng góp 2; Bảng X 2 tầng; mốc fuse2 cho R6 | Dự báo hai câu: M 3.15 [3.05, 3.25], P 68.0 [66.5, 69.5], R 61.2 [59.7, 62.7]. Short: M 2.09 [2.03, 2.15], P 75.7 [74.2, 77.2], R 47.1 [45.6, 48.6]. Claim 3 seed: ΔR và ΔF1 short (3 seed fuse2 − 3 seed P1) dương, CI 2 tầng không chứa 0 | [PRE]; [R4-00 §3] |
| 50_b_fuse2_maskfix_s42 | ≈ 4.5 | 00:30 13/10 | Loss mask | §8 | file này |
| 51_fuse2_s43_resume | ≈ 2.6 | 03:00 13/10 | Như 50_fuse2_s44 | Như trên. Ghi rõ: tiếp từ checkpoint-943, RNG của dropout không được khôi phục | [PRE]; script 51 |
| 52_a_uitviic_p1_s42, 52_b_uitviic_fuse2_s42 (tức "59a/59b" ở R4-00 và V3) | ≈ 6.4 | 09:30 13/10 | G3' (thay G3), G4, đường biên trên dataset thứ hai | **G3'a**, short: CI 90% của dP_inst nằm trong [−3, +3] và CI 95% của dR_inst > 0. **G3'b**, hai câu: DiD_inst = [P_inst(fuse2-detailed) − P_inst(P1)] − [P_inst(target người ghép) − P_inst(một caption người)], target dựng từ 3 trong 5 caption, cùng ảnh. Đạt nếu cận dưới CI 95% > −3. Loại ("mô hình mất sự thật riêng") nếu cận trên < −3. **G3'c**: τ_model = Δ(instance vắng)/Δ(sai theo tham chiếu); "chủ yếu điển hình" nếu cận trên CI 95% < 0.5, "chủ yếu sự thật" nếu cận dưới > 0.5; mốc τ_human 0.09 [0.04, 0.15]. Điều kiện chung: test + val 1,155 ảnh, lớp COCO-80 ngoài nhóm chọn ảnh, lexicon v2, paired bootstrap B = 5000. **G4**: ΔR short > 0 với CI không chứa 0, và ΔF1 ≥ 0, trên cả test lẫn val. Số object_prf mà 52_b tự in là G3 cũ với lexicon v1: chỉ báo kèm ghi chú "không có thông tin trên UIT-ViIC" | V3 §4 (đăng ký trong repo bằng commit này); [R4-00 §4e] |
| 55_ladder_cons_s42 | ≈ 2.6 | 12:00 13/10 | Đường biên; D3; H1-bleed | cons-short: M 2.17 [2.06, 2.28], P 74.7 [72.8, 76.7], R 47.5 [44.9, 50.1]. D3: M/M_P1 ≤ 1.30 ủng hộ L, ≥ 1.40 ủng hộ T. So với fuse2-short: \|ΔM\| ≤ 0.12 và \|ΔP\| ≤ 1.5 (không có hiệu ứng tràn). H1-bleed: ≤ 0.52 mention không được hỗ trợ mỗi caption, và residual ≥ +0.34 + 1.0 với CI không chứa 0 | [PRE] |
| 56_p1_4ep_s42 | ≈ 4.5 | 16:30 13/10 | Đối chứng cùng số bước; D2; V5-S2 | p1ep4-short: M 1.72 [1.63, 1.82], P 79.2 [77.1, 81.3], R 40.9 [38.5, 43.4]. D2: L dự báo 1.63–1.82; T dự báo giảm về 1.24. Đăng ký ở đây: ΔR (fuse2_s42 − p1ep4_s42, short) > 0 với CI không chứa 0 thì viết "lợi không đến từ số bước". V5-S2: nếu R short ≥ R của P1 + 2.5 thì chạy fuse2_s42/checkpoint-943 (0.75 GPU-h, n3) | [PRE]; [V5 §6]; file này |
| 57_p1_3b_s42, 58_fuse2_3b_s42 | ≈ 1.6 + 2.6 | 21:00 13/10 | G4, backbone thứ hai | ΔF1 short > 0 | [R4-00 §4e] |
| 60–63 xfit | ≈ 11.6 | 08:30 14/10 | Baseline RFT; mở lại V5-D2 | Báo dù kết quả ra sao [R4-00]. Đăng ký ở đây: chỉ mở lại D2 nếu ΔF1 (xfit_s42 − fuse2_s42, hai câu) có CI 95% không chứa 0 | [R4-00 §3]; [V5 §3]; file này |

Sau khi thang và seed về:
- Committee (V5) chạy trên CPU với luật đã đăng ký: cover k = round(0.3 × số caption), ≤ 2 câu; short dùng MBR-F1 trên pool, chỉ ứng viên short.
- Giữ claim của committee nếu phần vượt dây cung theo gold hợp ≥ +1.5 với CI không chứa 0, và P hiệu chỉnh tăng ≥ 0 (luật V5 đặt cho S1).

Kết quả của hàng đợi mà R6 cần:
1. fuse2 s43/s44: trung bình 3 seed của fuse2 cho bảng mốc §2a.
2. Cặp loss mask: recipe chuẩn cho mọi run R6.
3. Thang 5 policy: đường biên mà phương pháp R6 phải vượt.
4. 3B: backbone thứ hai.
5. p1ep4: thêm bước có làm tăng CIDEr hay chỉ tăng ghi nhớ.
6. xfit: baseline RFT. Các nửa A/B là tập dev cho R6.

### 7d. Việc CPU, 0 GPU

| Việc | Chặn cái gì | Nguồn |
|---|---|---|
| Lexicon `data/coco_probe/coco80_vi.json` v2: thêm cầu thủ, vận động viên, VĐV, thủ môn, trọng tài, khán giả; nuốt "bóng bàn", "ghi bàn", "bàn thắng"; sửa "gấu bông". Bản hiện tại chưa có các từ chỉ người này, và "bàn" khớp cả trong "bóng bàn" | Chấm 36, 38, 52. Commit trước khi chấm | V3 P2 |
| Sửa `scripts/prereg_ladder_check.py --check` để đọc `manuscript/prereg/2026-10-12_ladder_predictions.json` | Chấm thang | §5b |
| `scripts/two_gold_audit.py` | Bảng X, Hình 5a | V3 §4 |
| Bootstrap 2 tầng seed × ảnh trong `object_prf.py` (`--seeds`) | Claim 3 seed, Bảng X, mọi so sánh của R6 | R4-00 C-2 |
| CHAIR-vi v2, `scripts/nap.py`, `scripts/phi_validate.py`; giữ `--matcher v1` | Mọi số CHAIR_i trong bài; phụ lục FAIR | V2 §4 |
| Port `R2/V_V5/v5_committee.py` vào `scripts/` | Đóng góp 6 | V5 |
| Chép `R2/V_V1`, `V_V2`, `V_V3`, `V_V5/VERIFY.txt` vào repo (chỉ V4 đã có trong `manuscript/prereg/`) | Truy vết số | file này |
| Bỏ phần AI-silver và khung LSC của 06 khỏi bản thảo | Wording | R4-00 §6 |

### 7e. Job của R4-00 (70–83) chưa xếp: trạng thái sau V1–V5

| Job | GPU-h | Trạng thái |
|---|---|---|
| 70_zs512 | 1.3 | Giữ: zero-shot không bị cắt ở 160 token (R4-00 §5 mục 15). Không cần adapter, nên chạy được trong lúc chờ quyết định loss mask |
| 71 tag placebo/oracle, 79a/79b | 1.4; 5.5/1.0 | Bỏ: lợi P của tag là tính điển hình [V5 §7] |
| 72 mẫu cho MBR, 82 MBR trên UIT-ViIC | 4.5; 1.9 | Bỏ: I1 bị hạ [V5 §2.1]. Chỉ chạy S1 (1.1 GPU-h) nếu tác giả muốn |
| 73 1024 token thị giác | 1.6 | Tuỳ chọn (G8), ưu tiên thấp |
| 74 first + greedy, 75 LLM-fusion | 4.7; 6.0 | Không bị V nào loại. Chỉ xếp sau quyết định loss mask, để dùng recipe cuối |
| 76 thêm seed cho rnd2 | 8.6 | Theo G10 |
| 77 mask-fix | 4.3 | Đã thay bằng 33 và 50_b |
| 78 Vintern-3B zero-shot | 0.8 | Tuỳ chọn (R4-00 §5 mục 7). Không cần adapter |
| 81 đo chi phí, 83 ảnh xám | 0.5; 0.3 | Giữ: bảng chi phí cho claim 1 GPU; đối chứng tiên nghiệm ngôn ngữ |

## 8. Quyết định loss mask

**Sự thật**
- Mọi run trước 12/10 dùng mask legacy.
  - VLCollator đo độ dài prompt trên template trước khi token ảnh được mở rộng. Vì vậy câu lệnh và header assistant nằm trong loss.
  - Token caption chỉ chiếm khoảng 30% số token được giám sát ở dòng P1, và khoảng 68% ở dòng fuse2 hai câu (commit 7dacd8f).
- Cùng commit đó gọi `set_seed(args.seed)` trước khi dựng mô hình. Trước đó init LoRA không phụ thuộc `--seed` [R4-00 §5 mục 6].
  - Vì vậy run mới khác run cũ ở cả mask lẫn init. Quyết định dưới đây so "code mới" với "code cũ", đúng với cái sẽ được chạy lại.
  - Các job thang đang xếp (40–42, 55, 56) sẽ chạy mask legacy nhưng init theo seed. Neo P1/fuse2 của chúng là run cũ.
- Tỉ lệ token caption khác nhau giữa hai nhánh (30% so với 68%). Nếu lỗi có tác dụng, nó có thể tác dụng không đều lên P1 và fuse2. Vì vậy đại lượng quyết định là hiệu của hiệu, không phải từng nhánh riêng.

**Cặp kiểm tra**

| Job | Máy | Run | Mode eval | So với (run cũ, cùng seed 42) | ETA, giờ VN (ước) |
|---|---|---|---|---|---|
| 33_p1_maskfix_s42 | n2, đang chạy | p1mask_s42 | short, detailed, two | p1-gold-short, p1-gold-detailed. Mode two chỉ có p1_s43-two (khác seed) | 20:30 12/10 |
| 50_b_fuse2_maskfix_s42 | n3, sau 50_fuse2_s44 | fuse2mask_s42 | detailed, short | fuse2_s42-detailed, fuse2_s42-short | 00:30 13/10 |

**Đại lượng.** Paired bootstrap theo ảnh, B = 5000, `object_prf.py`. P theo gold hợp (`second_panel.py`) là phụ.
- Dịch chuyển từng nhánh: s_P1 = p1mask_s42 − p1-gold; s_F2 = fuse2mask_s42 − fuse2_s42; cùng mode.
- DiD = s_F2 − s_P1 = Δ_mới(fuse2 − P1) − Δ_cũ(fuse2 − P1).
- Metric: P, R, F1 (5 ref), CHAIR_i, CIDEr-D (short).

**Mốc nhiễu seed** [A6 §1.1; V5 §1]

| MDE với 1 seed mỗi nhánh | P | R | F1 | CHAIR_i | CIDEr-D |
|---|---|---|---|---|---|
| short, cùng công thức | 2.7 | 2.8 | 3.0 | 2.7 | 13.9 |
| short, khác công thức | 3.8 | 3.5 | 3.7 | 3.7 | 16.0 |
| hai câu (cùng công thức; P và CHAIR_i kèm mức khác công thức) | 2.5 (khác: 3.8) | 3.4 | 1.9–3.2 | 3.5 (khác: 4.6) | — |

Ba seed P1, short: F1 54.1 / 54.5 / 55.2; CIDEr 149.8 / 143.9 / 143.7 (dải 6.1, sd 3.46) [06; A6].

**Luật** (đăng ký trong file này, trước khi cặp kiểm tra về)
1. **Chạy lại toàn bộ** với `--loss-mask assistant` nếu có ít nhất một điều sau:
   - a. Một DiD (P, R hoặc F1; short hoặc hai câu) có CI 95% không chứa 0 **và** |DiD| ≥ 2.5, tức MDE một seed nhỏ nhất.
   - b. Một hiệu ứng chính đổi dấu: short ΔR, ΔF1; hai câu ΔP, ΔR, ΔF1.
   - c. Một dịch chuyển s_P1 hoặc s_F2 vượt MDE khác công thức (P 3.8, R 3.5, F1 3.7). Khi đó bản sửa đổi mô hình nhiều ngang việc đổi P1 sang fuse2.
2. **Giữ run cũ, chỉ công bố** nếu không có điều nào ở mục 1, **và** mọi dịch chuyển object nằm dưới MDE cùng công thức (short: P 2.7, R 2.8, F1 3.0, CHAIR_i 2.7; hai câu: P 2.5, R 3.4, CHAIR_i 3.5), **và** |dịch chuyển CIDEr short| ≤ 6.1, tức nằm trong dải 3 seed P1.
   - Bài ghi lỗi mask, đưa cặp kiểm tra thành một hàng "độ bền", và viết: "the fix changes no conclusion beyond seed noise (single-seed MDE 2.5–3.8 points)".
   - Với 1 seed mỗi nhánh, "dưới MDE" nghĩa là không phát hiện được, không phải bằng 0.
3. **Vùng giữa** (không thuộc mục 1, không thuộc mục 2): chạy lại lõi P1 và fuse2 × 3 seed với bản sửa (≈ 13.7 GPU-h ngoài cặp kiểm tra) cho bảng chính. Thang, 3B, UIT-ViIC và transfer giữ code cũ, chỉ so với neo cũ (các run P1, fuse2 cũ vẫn còn), và ghi rõ trong bài.

Với R6: mọi baseline và phương pháp của R6 dùng recipe mà luật này chọn.

**Thời điểm**
- Quyết định có khi 50_b về, khoảng 00:30 ngày 13/10 (giờ VN). Lúc đó n3 tự chạy 51 (fuse2 s43 tiếp từ checkpoint cũ). n2 bắt đầu 40 (multiref) khoảng 07:00 ngày 13/10.
- Nếu mục 1 kích hoạt:
  - 51 phải train lại từ đầu, không tiếp checkpoint cũ được.
  - 40–42, 52_a/b, 55–58 và 60–63 phải thêm `--loss-mask assistant` trước khi chạy.
- Để không phí GPU trong lúc chờ, tác giả có thể chèn job không dùng adapter ngay sau 50_b: 70_zs512 (1.3 GPU-h), 78_vintern3b_zs (0.8 GPU-h) [R4-00 §4c]. File này không sửa hàng đợi.

**Chi phí chạy lại toàn bộ**

| Nhóm | Run | GPU-h | Cách tính (nguồn) |
|---|---|---|---|
| Cặp kiểm tra (đang chạy) | p1mask_s42 (3 mode), fuse2mask_s42 (2 mode) | ≈ 7.1 | P1 train 6,938 s (`30_p1_s43.log`) + 0.23 h mỗi mode; fuse2 train 13,798 s [A6 §1.2] + 0.64 h cho 2 mode (25_tags_b trong queue.log) |
| Lõi | P1 s43, s44; fuse2 s43, s44 | ≈ 13.7 | 2 × 2.39 h (job 30, 31 trong queue.log) + 2 × 4.47 h |
| Thang, s42 | cons 942 bước; p1ep4 1,884; rnd2 1,884; unf2 ≈ 1,888; multiref 2,356 | ≈ 21.5 | bước × 7.35 s + 0.23 h mỗi mode. Batch hiệu dụng 8 (`--grad-accum 8`). multiref có 18,845 dòng (wc trên n2); unf2 có 1.72 dòng mỗi ảnh [PRE] |
| Backbone 3B | 57, 58 | ≈ 4.2 | ước tính ghi trong script 57, 58 [Q-n3] |
| UIT-ViIC trong miền | 52_a, 52_b | ≈ 6.4, ước thô | 674 + 1,348 bước × 7.35 s; eval 1,155 ảnh × 2 mode theo tốc độ KTVIC |
| Cross-fit RFT | 60–63 | ≈ 11.6, ước thô | 942 + 943 bước; lấy mẫu như job 20 (2.57 h); train cuối khoảng 2,250 bước nếu chọn khoảng 1,458 dòng như E5 vòng 1 [06] |
| Suy luận lại trên adapter mới | 35, 36 (P1, fuse2), 37 (P1, fuse2), 38 và 39 (4/6 run), tag (25_b, 32) | ≈ 10.7 | queue.log: 35 hết 1.64 h (gồm cả phần zero-shot), 36_coco_a 1.19 h, 25_b 0.64 h, 32 0.45 h. Ước tính trong script: 36_b 2.2; 37 1.0 mỗi job; 38 1.2; 39 2.7 |
| **Tổng** | | **≈ 75** (≈ 68 ngoài cặp kiểm tra) | khoảng 34 giờ đồng hồ trên 2 GPU |
| Tối thiểu (lõi + thang) | | ≈ 35 ngoài cặp kiểm tra | |

E5 và E5-DPO (phụ lục, kết quả null) không chạy lại. Giữ code cũ và ghi rõ.

## 9. So sánh chéo ngôn ngữ vi/en (giữ chỗ, chờ kết quả)

Một agent khác đang chạy phần này. Mục này chỉ là khung báo cáo. Không có ngưỡng đạt/trượt và không có luật thay metric.

Cách báo:
- Mỗi metric được tính cho tiếng Việt và tiếng Anh trên **cùng** tập ảnh, đặt cạnh nhau.
- Ba mức, mỗi số kèm CI 95% bootstrap theo ảnh:
  1. giá trị thô;
  2. giá trị chuẩn hoá theo trần người: giá trị của hệ chia cho giá trị của một caption người giữ lại, cùng ngôn ngữ, cùng ảnh, cùng gold (giao thức 1vK như R4-01);
  3. hiệu ứng phương pháp Δ(fuse2 − P1), ghép cặp trên cùng ảnh.
- Metric tính theo % thì báo theo điểm.

Dữ liệu dự kiến (đã có sẵn, cùng ảnh, hai ngôn ngữ):
- XM3600: 600 ảnh, caption người tiếng Việt và tiếng Anh (job 39; caption Anh ở `$NCS_DATA/datasets/xm3600_en/`) [R5-01, cuối file].
- POPE/RePOPE: 500 ảnh val2014, 5,127 câu hỏi, hỏi bằng tiếng Việt và tiếng Anh (job 37). Không có trần người, nên không có mức 2.
- UIT-ViIC: ảnh COCO có 5 caption Việt và caption Anh của COCO (V3 đã dùng làm đối chứng không gợi ý).

| Dữ liệu | Metric | Mức | vi [CI] | en [CI] |
|---|---|---|---|---|
| XM3600, 600 ảnh | P/R/F1 đối tượng; CIDEr, BLEU-4, METEOR, ROUGE-L | thô | chờ kết quả | chờ kết quả |
| XM3600 | như trên | chuẩn hoá theo trần người | chờ kết quả | chờ kết quả |
| XM3600 | như trên | Δ(fuse2 − P1) | chờ kết quả | chờ kết quả |
| POPE/RePOPE, 500 ảnh | accuracy, F1, tỉ lệ "có" | thô | chờ kết quả | chờ kết quả |
| POPE/RePOPE | như trên | Δ(fuse2 − P1) | chờ kết quả | chờ kết quả |
| UIT-ViIC (ảnh COCO) | P/R/F1 đối tượng | thô / chuẩn hoá theo trần người / Δ(fuse2 − P1) | chờ kết quả | chờ kết quả |

## 10. Rủi ro và công bố

| Rủi ro | Bằng chứng | Việc phải làm / câu chữ |
|---|---|---|
| **CHAIR-vi trong bài FAIR.** §IV-C viết caption được tách từ bằng RDRSegmenter/VnCoreNLP. Thực tế `rescap/chair.objects_in` khớp theo âm tiết; VnCoreNLP chỉ dùng cho CIDEr/BLEU (`rescap/metrics.py`) | Chấm lại [V2 §1.7; `R2/V_V2/fair_rescore.out`]. Detailed: mọi tương phản chính giữ dấu và ý nghĩa dưới cả 5 matcher. VSPS − zero-shot ΔCHAIR_i −15.0 [−16.9, −13.1] (bản đã công bố) thành −9.8 [−11.9, −7.7] (từ VnCoreNLP). VSPS − P2: −3.8 [−5.7, −2.0] thành −2.4 [−4.5, −0.4]. Độ lớn đổi: "4.26 → 1.57 đối tượng ảo giác mỗi caption (−63%)" thành 2.95 → 1.46 (−51%); CHAIR_s 98.0 → 79.2 thành 92.7 → 78.0. Short: câu "0.93 → 0.84" không đứng: theo VnCoreNLP là 0.59 so với 0.77, VSPS tệ hơn +0.18 [+0.10, +0.26]; ΔCHAIR_i VSPS − zero-shot +1.7 [−1.6, +4.7] thành +5.0 [+1.4, +8.2] (tách từ A7) hoặc +7.9 [+3.9, +11.7] (VnCoreNLP) | Bài FAIR: thêm một câu mô tả matcher theo âm tiết, hoặc chấm lại, và bỏ câu short 0.93 → 0.84. Bài Q1 dùng matcher đã sửa cho mọi số CHAIR dùng lại, giữ `--matcher v1` để tái lập số FAIR |
| **Giấy phép UIT-OpenViIC** | "available online for non-commercial research" (arXiv 2305.04166); "publicly available for research purposes" (README); không có file license; ảnh crawl từ Google/Bing nên bản quyền thuộc chủ ảnh [R5-01 §1] | Chỉ dùng cho nghiên cứu phi thương mại. Không phân phối lại caption: `data/ktvic_openviic_refs.json` chỉ được loại trừ qua `.git/info/exclude` (cục bộ), phải giữ ngoài mọi bản phát hành. Email nhóm tác giả OpenViIC trước khi công bố bất kỳ file nào chứa caption của họ; chỉ phát hành script và ID ảnh. Không bao giờ train trên OpenViIC [V5 §7] |
| **Điều khoản UIT-ViIC** | Caption "published on our lab website for research purposes" (2002.00175). Thẻ cc-by-4.0 trên HF `ttrung1402/UIT-ViIC` là bản tải lại của bên thứ ba. Ảnh là COCO, license Flickr theo từng ảnh (`manuscript/kg_plan/R2_06_data_timeline_feasibility.md`) | Ghi "for research purposes"; không phân phối lại caption. Người viết được xem gợi ý lớp COCO và xem caption của nhau [V3 §2a], nên mọi số instance trên UIT-ViIC đi kèm đối chứng tiếng Anh. 133 ảnh UIT-ViIC train nằm trong COCO test-5000 (59 ảnh trong manifest 2,500 của job 36): chỉ bỏ khi chấm mô hình train trên UIT-ViIC. Qwen2.5-VL nhiều khả năng đã thấy ảnh COCO khi pre-train: ghi là giới hạn [V3 §2c] |
| **Cách gọi caption KTVIC** | KTVIC §3.2 (2401.08100): "three participants" viết; giao diện đưa cho "human annotator an image … to provide five captions"; "two experienced researchers" duyệt và sửa. Vị trí caption không hoán đổi được: Jaccard cặp kề − không kề +0.121 [+0.108, +0.134] [V1]; vị trí 5 có P 76.8 so với 85–90 ở các vị trí khác [R4-01 §2] | Viết "5 reference captions per image" (ba người viết, mỗi ảnh có năm caption nhập qua một giao diện, hai nhà nghiên cứu sửa). Không viết "5 independent annotators". "Held-out annotator" đổi thành "held-out reference caption". Ảnh KTVIC lấy từ UIT-EVJVQA, phát qua thoả thuận dữ liệu VLSP 2022 (`R2_06_data_timeline_feasibility.md`) |
| **Chỉ một GPU** | Mỗi job dùng 1 GPU; n2, n3 chỉ tăng thông lượng [R4-00 §1] | Bài claim một RTX 3090 24 GB và báo tổng GPU-h từng run. fuse2 train hết 3.83 GPU-h (log, [A6 §1.2]); R4-00 ghi 3.6, dùng số log. Nếu tag xuất hiện trong bài thì báo chi phí của Grounding DINO, mô hình thứ hai lúc suy luận [06] |
| **Nhiễu seed** | CIDEr P1: 149.8 / 143.9 / 143.7 (sd 3.46), trong khi F1 sd 0.56. MDE một seed: P/R/F1/CHAIR_i 2.5–3.8, CIDEr 13.9–16.0 [A6]; V5 tính lại MDE CIDEr là 9.6–13 khi có p1_s44 [V5 §1]. Seed cũ dùng chung một chế độ init LoRA không theo seed; run sau 7dacd8f đổi init theo seed. fuse2 hiện có 1 seed; s43 tiếp từ checkpoint-943 sau lần khởi động lại, RNG của dropout không được khôi phục | Không xếp hạng bằng CIDEr của một seed. Báo mean ± sd, bootstrap 2 tầng, Holm. Ghi rõ chế độ init và việc s43 được tiếp từ checkpoint |
| **Loss mask** | §8 | Theo luật §8 |
| **Ước lượng "phần thật" và P hiệu chỉnh** | Giả định panel nhạy với mention thừa của hệ như với của người. Trên COCO, bộ ước lượng tính thiếu cho hệ: −10.7 đến −46.3 điểm [V3 P5] | Không viết "96% là thật". Viết "as attested as a held-out reference caption's unsupported mentions" |
| **Panel thứ hai không phải sự thật** | Hai panel phủ khoảng 84.4% [83.0, 85.6] lớp nhắc được, và đây là cận trên [R5-01 §6] | Ghi cạnh Bảng X |
| **Lexicon COCO-80 v1** | Thiếu từ chỉ người (cầu thủ, vận động viên…); "bàn" khớp trong "bóng bàn" [V3 P2] | Lexicon v2 trước khi chấm 36, 38, 52 (§7d) |
| **Nguồn số nằm ngoài repo** | V1, V2, V3, V5 chỉ có trong scratchpad | Chép vào repo (§7d) |

## 11. Venue và lịch

**Venue** (ứng viên của R4-00 §3: Neurocomputing, Pattern Recognition, TMM/TNNLS)

| Venue | Khi nào | Lý do |
|---|---|---|
| Neurocomputing (chính) | Mặc định, nếu R6 không có phương pháp | Nhận bài recipe + phân tích. V3: phân tích hai panel đạt mức Q1 khi là phần hỗ trợ recipe. Không cần novelty phương pháp |
| Pattern Recognition | Khi G3'a và G3'b đạt, claim 3 seed đạt, H0 đạt và G4 (3B) đạt; hoặc khi R6 cho phương pháp mới thắng P1 trung bình 3 seed có ý nghĩa | Khi đó có luật đăng ký trước, dataset thứ hai có nhãn instance, backbone thứ hai, hoặc một phương pháp mới |
| IEEE TMM / TNNLS | Không, trừ khi R6 thay đổi bức tranh | Không có đánh giá người cho hệ mới (R4-00 §5 mục 9, rủi ro cao). Hiện chưa có phương pháp mới [V5] |

**Lịch** (giờ VN; ETA ước tính, sai số vài giờ)

| Mốc | Việc | Phụ thuộc |
|---|---|---|
| Tối 12/10 | 33 và 50_fuse2_s44 về. CPU: lexicon v2, sửa đường dẫn prereg check. Commit file này, tức đăng ký G3' và các tiêu chí mới trong §7, §8 | — |
| Khoảng 00:30 13/10 | 50_b về: áp luật §8 | 33, 50_b |
| 13/10 | n2: 36–39, rồi 40–42. n3: 51, 52_a/b, 55–58. CPU: `two_gold_audit.py`, bootstrap 2 tầng, CHAIR-vi v2. Vòng R6 chạy song song trên CPU (tài liệu, pilot) | §8 chọn giữ code cũ hoặc vùng giữa |
| Tối 13/10 – sáng 14/10 | Thang, seed, 3B, UIT-ViIC về. Chấm: prereg check (H0, D1–D4), G3', G4, Bảng X với 3 seed fuse2, committee, hai hình | Lexicon v2 |
| Sáng 14/10 | xfit (60–63) về; quyết định D2. Hai GPU rảnh cho job R6 | — |
| 15–16/10 | Dự phòng: nếu §8 chọn chạy lại toàn bộ, ≈ 68 GPU-h, tức khoảng 34 giờ trên 2 GPU; mọi mốc sau lùi khoảng 1.5 ngày, và GPU cho R6 lùi theo | §8 |
| 15–19/10 | Đóng băng bảng và hình phần phân tích; viết. Chèn kết quả R6 khi có | — |
| Trước khi nộp | Email nhóm UIT-OpenViIC. Chọn venue theo bảng trên | — |

## Phụ lục A. Mâu thuẫn giữa các nguồn

1. **Ai viết 5 caption KTVIC.** R4-00 §1 mục 4 (và brief của tác giả): một người nhập cả năm caption. `R2/VERIFY_PREAMBLE.md` (theo A1): "3 annotators + 2 reviewers". V4 §1d: "3 annotators writing 5 captions (pigeonhole) plus 2 revising reviewers". Bài KTVIC §3.2 ủng hộ cách đọc "ba người tham gia; giao diện đưa một ảnh cho một annotator điền năm ô; hai nhà nghiên cứu sửa", nhưng không nói thẳng. Wording an toàn ở §10.
2. **Tên job UIT-ViIC trong miền.** R4-00 §4a/§4e, V3 §4 và commit 8d3a0bc gọi là 59a/59b. Hàng đợi n3 gọi là `52_a_uitviic_p1_s42` và `52_b_uitviic_fuse2_s42`, nội dung như nhau.
3. **Chi phí train fuse2.** R4-00 §3 (luận điểm A) ghi 3.6 GPU-h. Log ghi 13,798 s = 3.83 GPU-h [A6 §1.2].
4. **"Thang đối chứng cùng số bước".** R4-00 §5 mục 3 gọi cả thang là cùng số bước. Script cho: cons 942 bước (bằng P1), multiref 2,356 bước (1 epoch × 18,845 dòng), p1ep4 và rnd2 1,884, unf2 khoảng 1,888 (bằng fuse2). Phải báo số bước của từng run.
5. **Tag trên fuse2 s43/s44.** R4-00 §4a ghi đã xếp. Cả hai hàng đợi đều không có; chỉ 32_tags_p1_s43 đã chạy.
6. **I1.** R4-00 giữ I1 (job 72, cổng G1/G2) là ý tưởng duy nhất. V5 đo bỏ phiếu mẫu ≈ +0.1 [−1.8, +2.1] P hiệu chỉnh so với greedy, và khuyên không chạy phương pháp nào trên GPU. Theo V5.
7. **Cổng G3 và G5 của R4-00.** G3 không thể trượt trên UIT-ViIC (98.6% với target người, mức ngẫu nhiên khoảng 88%; V3 P3), nên thay bằng G3'. G5 đạt chỉ nhờ độ dài target (τ_b 0.87; V4 §3).
8. **"Phần thật ~96%"** (R5-01 §4) và V3 P5 (bộ ước lượng tính thiếu trên COCO). Đổi câu chữ như §10.
9. **"Vượt một người về F1"** (R5-01 mục 7: +3.1 [1.5, 4.6] trên gold 4 KTVIC + OpenViIC). V2 §1.2(iii) chỉ cho phép "fuse2-short ngang recall của một caption giữ lại". V4 §1d: caption cùng người viết làm điểm "một người" lạc quan cho người. Dùng chữ "một caption tham chiếu giữ lại" và báo cả hai gold.
10. **Đường dẫn của prereg check.** `scripts/prereg_ladder_check.py --check` đọc `scripts/PREDICTIONS.json`, file không có trong repo. Commit 1b5d16b đặt dự báo ở `manuscript/prereg/`.
11. **Mục tiêu bài.** R4-00 và V5 định vị bài là "phân tích + recipe, không có phương pháp mới". Yêu cầu mới của tác giả (12/10) đòi điểm tốt nhất với phương pháp có tính mới đột phá. Vì vậy §3 là tạm thời, chờ R6.
