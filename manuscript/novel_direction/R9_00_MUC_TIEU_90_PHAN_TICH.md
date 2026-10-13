# R9-00: Mục tiêu "≥ 90" cho object P/R/F1 trên KTVIC và object F1 trên COCO: trần đo được, chuẩn công bố và đề xuất

13/10/2026, vòng R9, nhánh `paper-v10`, HEAD `9d81fe5`. Tài liệu này tổng hợp 10 báo cáo agent (C1–C10), bối cảnh vòng R8 (UPE-MBR, CC-ADD) và kết quả POPE-vi. Chỉ dùng dữ liệu và nhãn người đã có. Không gán nhãn mới; nhãn do AI sinh không phải bằng chứng. Số KTVIC test tính trên CPU từ dự đoán hay mẫu có sẵn là ước lượng cỡ hiệu ứng; không luật nào được chọn trên test. Thang ×100; CI 95% là bootstrap ghép cặp theo ảnh, trừ khi ghi khác. Tài liệu không ra quyết định chạy hay không chạy; quyết định thuộc judge (§9).

**Nhãn số**
- (đo): đo trên dữ liệu của dự án; số do bài báo công bố ghi "(đo, tài liệu)". (ước tính): dự báo, proxy một bước, mô phỏng, ngoại suy. (cận trên): oracle, trần mô hình, hoặc mức "kế hoạch" chưa thành câu.
- Nhãn ở đầu một dòng hay một ô áp cho mọi số trong đó, trừ số có nhãn riêng. "Suy ra" = phép tính của tài liệu này trên số của báo cáo.
- [MH] = tín hiệu do mô hình sinh (tag detector, mẫu, phiếu, probe, câu trả lời có/không). Chỉ dùng bên trong phương pháp, không bao giờ làm nhãn.

**Nguồn viết tắt**
- [C1]…[C10] = `manuscript/research_r9/<thư mục>/REPORT.txt`. [T1], [T2], [T3] = `manuscript/research_r8/<thư mục>/REPORT.txt`. [CTX] = `CONTEXT_R9.md` của vòng này (để ngoài repo, xem §10).
- [POPE] = `data/results/pope_vi/scores.txt`. [UPE-A] = `data/results/upe/upe_choose_t.json`. [SP] = `data/results/second_panel.json`. [PRE] = `manuscript/prereg/2026-10-13_upe_mbr.md`.
- [D10] = phán quyết D10 của judge, 13/10/2026 (`decisions/D10.txt` trong scratchpad của phiên; dòng D10 và U-001 của `decisions/LOG.md`). Số do judge tự kiểm ghi "(đo, judge kiểm)".
- Ký hiệu: P1 = SFT trên caption số 1; fuse2 = SFT trên đích ghép đồng thuận; C = CIDEr-D mức từ; C-âm tiết = CIDEr-D mức âm tiết (chỉ để chẩn đoán); M = số lớp object mỗi caption.

## 1. Tóm tắt

**≥ 90 trên từng độ đo: không đạt được bằng caption. Lý do nằm ở cách xây gold, không ở mô hình.**
- **KTVIC P: không**, ở mức recall dùng được. P1 đang ở 78.8–79.1, một người chú thích ở 85.3 (đo) [CTX; C10 §1a]. P ≥ 90 chỉ xuất hiện khi R còn 12–26 (đo): vote ≥ 0.8 cho 92.2/11.8 [C1 §2d]; chỉ giữ mention được 6/6 mẫu đồng ý cho 90.5/16.4 [C3 §2e].
- **KTVIC R: không.** Chỉ oracle đọc nhãn test đạt: danh sách 4 lớp gold cho R 90.4 ở C 30.7 (cận trên) [C1 §1, §5]. Ở trần nhiễu, R ≥ 90 kéo P xuống ≤ 83.5–87.5 (cận trên) [C1 §3].
- **KTVIC F1: không.** Trần nhiễu/Bayes của chính metric là 84.3–89.4 (cận trên; mô hình đã kiểm trên các ô người) [C1 §3; C9 §2c]. Chỉ các biến thể bị ma trận người bác bỏ mới vượt 90.
- **COCO F1: không, nếu là caption.** Năm người tiếng Anh gộp: 79.4–79.5; hệ tốt nhất: 73.4; committee: 75.4 (đo) [C1 §4; C6 §1.2]. Gần 90 chỉ có inventory: mọi lớp có instance ≥ 32² px cho 91.5 (cận trên) [C7 §2h]; tagger cỡ Query2Label quy về 87.7–87.9 (ước tính) [C1 §4].
- **Vì sao.** Gold KTVIC là hợp những gì 5 người *chọn* gọi tên: 34.6% lớp gold chỉ 1/5 người gọi (đo) [C1 §1]. Gold COCO là instance đầy đủ: 37.2% lớp instance không ai trong 5 người gọi (đo) [C1 §4]. Mọi lever đo được chỉ dời hệ dọc một đường precision–số lớp cố định [C9 §0].

**Cái đạt được thật.** KTVIC F1 từ 64.8 (đo, tốt nhất) [C1 §2b] lên vùng hai người: 70.9 (đo), 72–73 so với hợp 5 người mới (ước tính) [C1 §2a]. UPE-MBR: +2.24 F1 KTVIC trên dev (đo) [UPE-A]. Kế hoạch PLAN-F1: 64.9 (cận trên) [C5 §3c]. COCO caption: 74–76 (đo: 75.4 mức tập, 74.3 trên ảnh mới với luật đóng băng) [C5 §3g]. POPE/RePOPE F1 ≥ 90 đã có (đo) [POPE], nhưng đó là câu hỏi khác (§8).

**Hướng đề xuất để judge xét (D10).**
1. Đổi tiêu chí thành "trên đường biên người, kèm chi phí CIDEr" [C10 §5 R2–R3].
2. Giữ UPE-MBR (D9) làm lõi; chồng FOPR với 0 GPU-h, dùng lại mẫu của UPE [C3 §6A].
3. Nếu cần đòn bẩy F1 KTVIC lớn hơn: PLAN-F1, chặn sớm bằng cổng độ trung thành K1 (khoảng 5–6 GPU-h) [C5 §5].
4. COCO: chỉ các cách giữ dạng caption (UGZ theo luật CC-ADD; VGR). Inventory báo riêng như tagging.

**D10 đã ra (§9).** Judge duyệt pilot PLAN-F1 trên dev300 (85%), sàng S0 Qwen3-VL-8B (88%), VGR theo giai đoạn (78%), sửa dấu thanh (90%), cột tỉ lệ CJK ở 0 GPU (82%) và đối chứng độ phân giải KTVIC 2,048 token (78%); bác cả bốn sửa đổi của PLAN-F1 (trong đó có FOPR) và bác UGZ (87%); hoãn P-A (92%) và để P-B sau kết quả 35_e (85%). Hai mục 78% (dưới ngưỡng 80%) đã được người dùng chốt ở U-001: VGR chạy bước 0 WiSE-FT trước rồi mới quyết SFT; đối chứng KTVIC-2048 được duyệt chạy ở ưu tiên thấp. Judge khác hướng đề xuất trên ở mục 2 (FOPR) và mục 4 (UGZ).

## 2. Độ đo và số liệu hiện tại

### 2a. Định nghĩa (`scripts/object_prf.py`) [CTX; C5 §1]
- **KTVIC.** M = các lớp caption nêu, qua lexicon 113 mục (`rescap/chair.py`, `objects_in`), khớp chính xác, không cộng điểm hypernym. G = hợp các lớp của 5 tham chiếu. P = Σ|M∩G| / Σ|M| (micro, gộp mọi mention). R = trung bình, trên các ảnh có G ≠ ∅, của |M∩G|/|G| (macro). F1 = 2PR/(P+R). 558 ảnh test. Lexicon chỉ thấy khoảng 42% mention danh từ của tham chiếu (đo, báo cáo K2) [CTX].
- **COCO.** Caption tiếng Việt → lớp COCO-80 qua matcher v2 (`score_coco_probe.vi_objects`, 224 từ trong `coco80_vi.json`). G = lớp instance COCO-2014 của ảnh, chỉ instance. 2,500 ảnh Karpathy test (`data/coco_probe/manifest.json`); |G| trung bình 2.82, 27 ảnh rỗng (đo) [C1 §4]. Matcher không phải nút cổ chai: viết gold ra tiếng Việt rồi khớp lại cho 100/100/100 (đo) [C1 §4].
- **Nguồn gold.** 5 tham chiếu KTVIC. Nhãn instance COCO-2014, khớp `instance_gold.json` trên 2,500/2,500 ảnh [C1 §4]. Panel UIT-OpenViIC (555 ảnh test, 5.39 caption/ảnh) chỉ để đánh giá, không bao giờ huấn luyện [SP]. Tham chiếu tiếng Anh Karpathy (từ đồng nghĩa Rohrbach) cho trần người trên COCO [C1 §4]. Nhãn RePOPE cho POPE [POPE].
- **Thang.** Với output dạng caption, recall trung bình theo ảnh dễ hơn recall gộp (OR) 6–12 điểm (đo) [C9 §2e]; OF1 trong tài liệu chỉ so được gần đúng.

### 2b. KTVIC test (đo; [CTX] trừ khi ghi khác)
| Hệ | P / R / F1 | C |
|---|---|---|
| zero-shot short | 52.3 / 32.5 / 40.1 | 28.98 [C3 §2a] |
| zero-shot detailed | 31.6 / 57.1 / 40.7 | 0.0 [C9 §2a] |
| P1 response-only s42 / s43 | 78.8 / 42.9 / 55.5; 79.1 / 42.3 / 55.1 | |
| P1 legacy s42 / s43 / s44 | 77.9 / 41.4 / 54.1; 78.8 / 41.7 / 54.5; 78.9 / 42.4 / 55.2 | 145.8, trung bình 3 seed [T2 §3] |
| fuse2 s42 / s43 / s44 | 75.7 / 47.1 / 58.1; 75.4 / 47.6 / 58.4; 75.7 / 46.8 / 57.8 | 143.9 (s42) [C1 §5] |
| fuse2 + tag Grounding-DINO trong prompt [MH] | 77.9 / 46.7 / 58.4 | |
| MR5 | 77.9 / 42.8 / 55.3 | |
| MBR đồng thuận object trên fuse2 | 70.9 / 53.1 / 60.7 | 98.0 [C5 §3c] (xem §7) |
| fuse2 s42 detailed | 68.0 / 61.2 / 64.4 | 23.9 [C1 §5] |
| P cao nhất: p1_s43-detailed | 79.9 / 42.3 / 55.3 [C1 §2b] | |
| F1 cao nhất: e5dpo_s42-detailed | 69.3 / 60.8 / 64.8 [62.8, 66.7] [C1 §2b] | |
| Người: 1 so với 4 người còn lại (1v4) | 85.3 / 46.9 / 60.5 [58.7, 62.3] [C10 §1a] | |
| Người: 2 gộp so với 3 còn lại (2v3) | 76.1 / 66.6 / 70.9 [C10 §1a] | |
| Người: 1 người, gold thêm panel OpenViIC | P 94.0 [CTX] | |

### 2c. COCO, 2,500 ảnh (đo) [CTX; C1 §4]
| Hệ | short P / R / F1 | detailed P / R / F1 |
|---|---|---|
| zero-shot | 90.8 / 48.5 / 63.3 | 80.5 / 67.5 / 73.4 |
| P1 s43 | 89.5 / 44.3 / 59.3 | 89.8 / 44.4 / 59.4 |
| fuse2 s42 | 90.9 / 44.2 / 59.4 | 88.9 / 52.3 / 65.8 |
| zero-shot + VCD | — | 82.0 / 63.5 / 71.6 |
| VSPS (distill) | — | 86.4 / 49.5 / 63.0 |

Adapter KTVIC mất recall COCO so với zero-shot [CTX]. Ở chế độ short, phần mất nằm ở lớp caption KTVIC hiếm gọi: lớp < 20 mention 32.9 → 26.3, lớp 20–199 31.0 → 24.3; lớp ≥ 200 lại tăng 51.2 → 57.7 (đo, zero-shot → fuse2) [C6 §1.4].

### 2d. UPE-MBR (R8; đang chạy theo D9)
- Luật: chọn trong pool greedy + 6 mẫu [MH] theo CIDEr-D đồng thuận, CIDEr-D với tham chiếu truy hồi, và λ·EF1 kỳ vọng với q = 1 − (1 − v)^5 từ phiếu mẫu [MH]. Hằng số đóng băng: λ 2, m 5, margin 0.5, E|G| 6 [PRE].
- CPU, pool T = 1.0, luật đóng băng (đo, dev): panel F1 +4.0 [+2.6, +5.4], KTVIC F1 +3.0 [+1.2, +4.9], C −0.4 [−5.0, +4.1] [T3 §3b]. Test (ước tính): panel F1 +3.7 (P1 s43) và +2.5 (fuse2, panel P −2.1) [T3 §3d]; KTVIC F1 +3.1 [+1.9, +4.3] (P1) và +2.2 [+0.9, +3.5] (fuse2) [C5 §3d].
- Bước A của D9, mẫu GPU thật trên dev300 (đo) [UPE-A]: T* = 0.5. So với greedy: KTVIC P −0.34 [−2.08, +1.43], R +3.00 [+1.73, +4.41], F1 +2.24 [+0.94, +3.68]; panel F1 +2.25 [+1.20, +3.35]; C +0.30 [−5.05, +5.47]. Ở T = 0.8: F1 +1.61 [+0.27, +3.09], P −2.96 [−5.03, −0.96], C −3.82, trượt luật chi phí.
- Nhánh COCO (UIT-ViIC, dự báo F2) chưa có kết quả.

## 3. Trần đo được

### 3a. KTVIC (558 ảnh; gold = hợp 5 tham chiếu)
| Loại trần | P / R / F1 | Nhãn | Nguồn |
|---|---|---|---|
| Nhiễu người chú thích, Beta (fit trên số người gọi mỗi lớp ở test) | F1 max 86.5 (83.5 / 89.7, τ 0.45); điểm P = R ≈ 86.2 | cận trên | [C1 §0, §3] |
| Nhiễu, hỗn hợp 2 Beta | F1 max 89.4 (84.7 / 94.6, τ 0.50); điểm P = R ≈ 88.2 | cận trên | [C1 §0, §3] |
| Nhiễu, biến thể ít lớp ẩn | F1 max 90.5 / 91.4, nhưng lệch ma trận người (1v4 P 86.3 / 87.6 so với 85.3 đo) | cận trên, bị bác | [C1 §3] |
| Bayes, beta-binomial fit trên TRAIN | F1 84.3 (84.0 / 84.6, M 3.66); đuôi lớp ẩn khớp test (×0.6): 86.7 (84.9 / 88.7) | cận trên | [C9 §2c] |
| Bayes, không có lớp ẩn | 90.9, nhưng 1v4 mô phỏng P 89.4 so với 83.6 / 85.3 đo | cận trên, bị bác | [C9 §2c] |
| Một người (1v4) | 85.3 / 46.9 / 60.5; judge kiểm lại: 85.33 / 46.90 / 60.50 (`data/results/human_parity.json`) | đo | [C10 §1a; C1 §2a; D10] |
| P ≥ 90 trên đường PR thực tế | chỉ ở R 16.4–21.9: giữ mention 6/6 mẫu đồng ý cho P1 90.5 / 16.4, fuse2 90.6 / 21.9 | đo | [C3 §2e; D10] |
| Một người, quy về hợp 5 người mới | 87.7–89.3 / 44.4–45.0 / 58.9–59.8 | ước tính | [C1 §2a] |
| Hai người gộp (2v3) | 76.1 / 66.6 / 70.9; quy về hợp 5 người mới: F1 71.7–73.3 (ước tính) | đo | [C1 §2a] |
| Bốn người gộp so với người thứ 5 (4v1) | 42.9 / 85.9 / 57.2; quy về hợp 5 người mới: F1 79.5–82.4 (ước tính) | đo | [C1 §2a] |
| Năm người độc lập (panel OpenViIC, 555 ảnh) | 44.5 / 74.0 / 55.6 (mọi caption) [C1 §2d; C4 §2]; 45.5 / 72.4 / 55.9 (5 caption) [C2 §2f] | đo | xem §3e |
| Oracle đồng thuận (lớp ≥ 2 người KTVIC gọi) | 100 / 69.8 / 82.2 | cận trên | [C1 §1] |
| Oracle biết 3 / 4 trong 5 tham chiếu | R 85.4 / 94.0; F1 92.1 / 96.9 | cận trên | [C4 §2] |
| Oracle: danh sách 4 lớp gold nhiều người gọi nhất | 100 / 90.4 / 95.0, C 30.7 | cận trên | [C1 §1, §5] |
| Pool fuse2 (greedy + 6 mẫu [MH]), lọc hoàn hảo | 100 / 71.1 / 83.1 (P1: F1 79.0) | cận trên | [C4 §2; C5 §3a] |
| Oracle chọn 1 caption/ảnh trong pool đó (best-of-7) | 89.7 / 60.7 / 72.4 (P1: F1 69.3) | cận trên | [C4 §2] |
| Pool 30 hệ short, lọc hoàn hảo | 100 / 83.3 / 90.9 | cận trên | [C5 §3a] |
| Hợp mọi output + tag GDINO [MH], lọc hoàn hảo | R 92.9, F1 96.3 | cận trên | [C9 §2d] |
| Vote ensemble 71 hệ, không oracle | F1 max 62.7 (69.5 / 57.1); P ≥ 90 chỉ khi R ≤ 11.8 | đo | [C1 §2d] |
| Đường biên tiền đăng ký V4 | R 90 cần M 5.5 ở P 59.0 (F1 71.3); P 90 ép R 29.8; F1 đỉnh 72.4 | ước tính (ngoại suy) | [C6 §1.9; C9 §2a] |
| Danh sách từ bộ phân loại: tag GDINO [MH] làm output | 34.3 / 22.0 / 26.8 | đo | [C1 §2c; C2 §2a] |
| Tagger COCO-80 hoàn hảo, dịch đúng, kiểm hoàn hảo, hợp với caption | R ≤ 64–67 (short) / 74.5 (detailed); F1 ≈ 73–74 | cận trên | [C2 §0, §2b] |
| Hệ tốt nhất hiện có | F1 64.8 (e5dpo detailed); P 79.9 (p1_s43 detailed); R 64.7 (selffuse-two, P 60.7) | đo | [C1 §2b] |
| Caption object F1 đã công bố trên KTVIC | không có; bài KTVIC chỉ báo n-gram, bài tiếng Việt Q1/Q2 không báo độ đo object | — | [C1 §0; C10 §2i] |

### 3b. COCO (2,500 ảnh Karpathy test; gold = instance)
| Loại trần | P / R / F1 | Nhãn | Nguồn |
|---|---|---|---|
| Matcher: gold viết ra tiếng Việt rồi khớp lại | 100 / 100 / 100 | đo | [C1 §4] |
| Một người (tham chiếu EN) | 92.6 / 56.6 / 70.3 (2,500 ảnh); 92.4 / 56.9 / 70.5 (2,441 ảnh) | đo | [C1 §4; C10 §1b]; [C4 §2; C6 §1.2] |
| Hai người gộp | 90.0 / 66.0 / 76.2 | đo | [C8 §3 P1; C10 §1b] |
| Năm người gộp | 85.3 / 74.3 / 79.5 (2,500), judge kiểm lại, kèm 37.2% lớp instance không người nào gọi; 85.0 / 74.4 / 79.4 (2,441) | đo | [C1 §4; C10 §1b; D10]; [C4 §2; C6 §1.2; C7 §2c] |
| Lớp được ≥ 2 trong 5 người gọi | 93.3 / 65.6 / 77.0 | đo | [C5 §3g] |
| Oracle: đúng các lớp instance mà ít nhất 1 người gọi | 100 / 74.3 / 85.3 | cận trên | [C8 §3 P1] |
| Người Việt (UIT-ViIC, ảnh COCO thể thao): 1 / 5 caption | F1 57.8–59.3 / 71.3–72.9, tùy tập con | đo | [C1 §4; C4 §2; C6 §1.2; C10 §1b] |
| Hợp output 9 hệ; giữ lớp ≥ 2/9 phiếu | 73.1 / 76.8 / 74.9; 83.0 / 69.1 / 75.4 | đo | [C1 §4; C5 §3g] |
| Pool 9 hệ, lọc hoàn hảo | 100 / 76.8 / 86.9 | cận trên | [C5 §3g] |
| Oracle best-of-8 theo F1 instance | 92.7 / 71.2 / 80.6 (80.5 trên 2,441 ảnh sạch) | cận trên | [C4 §2] |
| fuse2-short ∪ zero-shot-detailed; chỉ giữ lớp đúng | 79.6 / 69.5 / 74.2 (đo); 94.6 / 69.5 / 80.1 (cận trên) | đo / cận trên | [C7 §2j] |
| 8 output + 5 tham chiếu EN, lọc hoàn hảo | R 84.8, F1 91.8 | cận trên | [C9 §2e] |
| Nhận thức hoàn hảo, giữ nguyên P(nói ∣ thấy) | fuse2-short 62.5; zero-shot detailed 79.0 | cận trên | [C7 §2g] |
| Zero-shot detailed + mọi lớp gold cỡ M/L | 85.3 / 89.5 / 87.3 | cận trên | [C1 §4] |
| Inventory: mọi lớp có instance ≥ 32² px | 100 / 84.3 / 91.5 | cận trên (inventory) | [C1 §4; C7 §2h] |
| Bộ phân loại đa nhãn tốt nhất (Q2L CvT-w24: OP 89.2 / OR 84.6 / OF1 86.8, mAP 91.3, đo, tài liệu) | quy về metric này: F1 87.7–87.9 | ước tính | [C1 §4] |
| ADDS (mAP 93.4, không báo F1) | ≈ 88–90 | ước tính (ngoại suy) | [C1 §4] |
| Caption ∪ tagger cỡ Q2L (mô phỏng) | F1 87.8–89.0; kiểm hoàn hảo 92.6–93.7 | ước tính / cận trên | [C2 §3] |
| Phụ lục inventory từ tagger P90/R85 (mô phỏng) | 87.4 / 93.5 / 90.4 ở C-D 88.6 → 56.3 (tham chiếu EN) | ước tính | [C6 §1.7] |
| Caption object F1 cao nhất đã công bố | CHAIR-F1 79.7 (IJCV 2025, gold khác, caption EN ~100 từ); SC-Captioner 76.4 (COCO-LN500); caption Tag2Text 62.7 | đo, tài liệu | [C10 §0, §2c; C2 §4] |
| Hệ tốt nhất của ta | zero-shot detailed 73.4; giữ lớp ≥ 2/9: 75.4; luật câu đóng băng trên ảnh mới: 74.3 | đo | [C1 §4; C5 §3g] |

### 3c. Inventory khác caption
- Con số 91.5 của C7 ("mọi lớp có instance ≥ 32² px, không gì khác") là mục tiêu **inventory**, không phải mục tiêu captioning [C7 §0, §2h]. COCO F1 90 cần R ≈ 89 ở P 90.9 [C7 §0], hoặc R ≥ 81.8 ngay cả ở P 100 [C8 §0]: phải nêu object mà không người nào trong 5 người nêu.
- Q2L là tagger huấn luyện trên nhãn instance COCO ở 384 px. Viết output của nó vào caption là tagging, phải so với Q2L/ML-Decoder [C9 §5B; C1 §4].
- Trên KTVIC, inventory còn làm giảm điểm: nối danh sách GDINO [MH] vào fuse2-detailed cho F1 −6.9 [−7.9, −5.8] (đo) [C1 §2c; C9 §2d]. Gold KTVIC thưởng độ nổi bật (salience): 5 người độc lập chỉ đạt F1 ~56, dưới hệ đã huấn luyện (64.8) (đo) [C1 §2d].

### 3d. Gaming: nối danh sách và CIDEr sụp
| Thao tác | Object | CIDEr | Nhãn | Nguồn |
|---|---|---|---|---|
| fuse2-detailed + câu liệt kê tag GDINO [MH] | F1 64.4 → 57.5 | 23.9 → 5.7 | đo | [C1 §5] |
| Danh sách 4 lớp gold / mọi lớp gold (oracle) | 100 / 90.4 / 95.0; 100 / 100 / 100 | 30.7; 26.9 (fuse2-short: 143.9) | cận trên | [C1 §5] |
| Nối một mệnh đề chứa tag top-1 / mọi tag vào P1 s42 | — | C-âm tiết 165.5 → 111.0 / 75.3 | đo | [C2 §2g] |
| Greedy fuse2 + lớp gold còn thiếu (oracle) | 88.0 / 99.1 / 93.2 | 143.9 → 95.2 | cận trên | [C4 §2, §4] |
| Danh sách gold thuần | 100 / 97.6 / 98.8 | 30.3 | cận trên | [C4 §2, §4] |
| Thêm 1 object vào caption | — | khoảng −13 mỗi object | ước tính | [C4 §4] |
| Caption người UIT-ViIC + 1 lớp instance thiếu / + mọi lớp thiếu | F1 +22.6 / 99.9 | C-âm tiết −52.5 / −85.0 | cận trên | [C4 §5] |
| Phụ lục inventory tagger P90/R85, UIT-ViIC val | 90.1 / 91.2 / 90.7 | C-D 179.7 → 52.6 | ước tính | [C6 §1.7] |
| Câu thứ hai trong caption KTVIC; đoạn văn | — | ~140–150 → 18–24; 0.0 | đo | [C9 §2a] |
| Liệt kê mọi lớp: KTVIC 83 lớp; COCO 80 lớp | 4.5 / 100 / 8.6; 3.5 / 100 / 6.8 | — | đo | [C9 §2d, §2e] |
| RL với reward chỉ object F1 | inventory thắng nhóm ở 30–34% ảnh; ở trọng số 1: 1.6–2.0% | — | đo (proxy) | [C4 §0, §4] |

CIDEr sụp khi câu dài là do phạt độ dài Gauss của CIDEr-D (σ 6), không phải đánh giá chất lượng; vì vậy CIDEr không chấm được mô tả dài [C9 §2a].

### 3e. Chỗ các báo cáo lệch nhau
- **Năm người EN gộp trên COCO:** 85.3 / 74.3 / 79.5 [C1; C2; C8; C9; C10] so với 85.0 / 74.4 / 79.4 [C4; C6; C7]. C6 nêu lý do: tập ảnh khác nhau (2,441 ảnh có đủ 5 caption EN so với 2,500) [C6 §1.2].
- **Một người EN trên COCO:** 92.6 / 56.6 / 70.3 [C1; C2; C5; C8; C10], 92.4 / 56.9 / 70.5 [C4; C6, 2,441 ảnh], 92.8 / 57.1 / 70.7 [C7 §2c, ghi "tham chiếu #1–#5 cho F1 70.2–70.7"], 92.9 / 56.8 / 70.5 [C9 §2e]. Hai người gộp: 90.0 / 66.0 / 76.2 [C8; C10], 89.8 / 66.2 / 76.3 [C6], 89.9 / 66.1 / 76.2 [C9].
- **Lớp instance không ai trong 5 người gọi:** 37.2% [C1; C10], 37.3% [C6] so với 25.7% [C8]. Không báo cáo nào giải thích. Nhận xét của tài liệu này (suy ra): 100 − 74.3 = 25.7 là phần bù của recall trung bình theo ảnh; 100 − 62.8 = 37.2 là phần bù của recall gộp [C1 §4].
- **Panel OpenViIC như 5 người độc lập trên KTVIC:** 44.5 / 74.0 / 55.6 [C1 §2d; C4 §2] so với 45.5 / 72.4 / 55.9 [C2 §2f]; một caption 56.6 / 37.1 / 44.8 [C1] so với 55.5 / 37.6 / 44.8 [C2]. Không nêu lý do; C1 dùng mọi caption (5.39/ảnh), C2 ghi "5 caption".
- **Trần nhiễu/Bayes KTVIC:** F1 86.5–89.4 [C1 §3] so với 84.3–86.7 [C9 §2c]. Lý do có nêu: C1 fit trên số người gọi ở test; C9 fit trên TRAIN và ghi bản ×1.0 bi quan khoảng 2 điểm trên test. Ở P ≥ 90, R tối đa 80 / 84 [C1] so với 75.3 / 81.8 [C9]; ở R ≥ 90, P tối đa 83.5 / 87.5 [C1] so với 77.6 / 83.3 [C9].
- **False positive KTVIC là object thật đến đâu (56.5% so với 97.3%):** cả hai con số đều nằm trong [SP] (`scripts/second_panel.py`), chỉ khác định nghĩa. (1) **56.5% [49.2, 63.6]** [C3 §0, §2c; D10 dùng số này] là **tỉ lệ xác nhận trực tiếp** so với 5 tham chiếu KTVIC (`confirm["p1_s43-short"]["exact"]["confirmed_share"] = 56.46`, với `p1-gold-short` là `55.65` [48.7, 62.2]; trên dev300 là `56.6%`): phần trăm mention "sai" so với 5 tham chiếu (`rf = m − gold_5`) được panel OpenViIC trực tiếp gọi tên (`|rf ∩ panel| / |rf|`). Bỏ mọi mention chưa được cả hai panel gọi đưa P của `p1_s43-short` từ 78.7 lên 86.7 (cận trên) [C3 §0, §2c]. (2) **97.3% [85.6, 109.6]** [C8 §0, §3 P2] là **ước lượng tỉ số hiệu chỉnh theo độ nhạy của panel** (`human_1v4["p1-gold-short"]["confirm_exact"]["real_fraction_est"] = 97.3`, với `p1_s43-short` là `98.5` [86.2, 111.3], `fuse2_s42-short` `96.9` [86.4, 107.9], `fuse2_s42-detailed` `95.7` [87.6, 104.6]): trong phép kiểm chéo 5-fold 1v4 (`human_1v4` của `scripts/second_panel.py`), mỗi tham chiếu người được giữ lại so với 4 tham chiếu kia; các mention "sai" của chính người thứ 5 so với 4 người kia là object thật mà 4 người kia bỏ qua, và panel OpenViIC chỉ gọi lại được `p_h = 58.78%` [54.9, 62.5] trong số đó (độ nhạy/recall của panel). Khi chấm `p1-gold-short` với cùng 4 tham chiếu, panel xác nhận `p_s = 57.21%` [51.1, 63.4]; công thức của `second_panel.py` (dòng 223–225) chia tỉ lệ xác nhận của hệ cho độ nhạy của panel trên người: `real_fraction_est = 100 × p_s / p_h = 100 × 57.21 / 58.78 = 97.3%` (CI bootstrap vượt 100% vì là tỉ số hai mẫu `d_s / d_h`), từ đó C8 suy ra bộ nhận thức hoàn hảo chỉ cộng tối đa P +0.5 [0, +2.9] cho P1-short (+1.1 [0, +3.1] cho fuse2-detailed).
- **Tỉ lệ tag được nêu khi có tag trong prompt:** C2: fuse2 24.1% → 24.4%, P1 s43 22.8% → 25.7%, zero-shot 25.0% → 42.5% (tag "thấy được" bởi lexicon) [C2 §2c]; C5: 18.1% → 17.7%, 17.4% → 19.5%, 18.9% → 30.8% [C5 §3f]. Precision của tag so với gold KTVIC: 34.3 [C1; C2; C4; C9] so với 25.1% [C5 §3f]. Lý do (kiểm từ `p0_tagfollow.py` của C5): C1/C2 ánh xạ tag GDINO qua `objects_in` (2.12 lớp lexicon/ảnh) [C1 §2c], còn C5 so trực tiếp chuỗi tag thô trong `tags_gdino.json` (2.39 tag/ảnh, gồm 10.7% ngoài lexicon và từ đồng nghĩa chưa quy về tên lớp chuẩn) với tập `objects_in(caption)`, làm mẫu số lớn hơn và thu nhỏ cả precision lẫn tỉ lệ nêu theo cùng hệ số (~0.73).
- **Số lần viết "tòa" và tỉ lệ CJK trên KTVIC (C8 so với D10):** trên zero-shot detailed (KTVIC test), C8 ghi 67 lần viết "tòa" [C8 §7], trong khi judge đếm cụm "tòa nhà" ra 107 lần và "toà nhà" 0 lần (toàn bộ cụm dấu kiểu cũ oa/oe/uy là 273 lần/558 caption) [D10 (iv)(a)]. Về tỉ lệ caption KTVIC lọt ký tự CJK sau SFT, C8 ghi 0–0.2% [C8 §2A, §7], còn judge đo trên toàn bộ 73 file dự đoán KTVIC test ra: `p1assist` (3 seed) và `p1_s43` 0.0%, `fuse2` (3 seed) 0.0–0.9%, zero-shot 0.7% (short) và 5.2% (detailed), các hệ cũ 15–42% (`roundA-detailed` 41.6%, `official-detailed` 27.8%, `VCD-detailed` 17.0%) [D10 (iv)(b)].
- **Ảnh Karpathy test nằm trong COCO train2017:** khoảng 87% [C2 §6] so với khoảng 88% [C8 §5, §7] (khi chuẩn bị S0 đã đếm chính xác là 88.1%, và 295/2,500 ảnh probe thuộc val2017).
- **Ảnh UIT-ViIC train cần bỏ:** C4 bỏ 59 ảnh probe (còn 2,636) [C4 §5, §8]; C6 bỏ cả 133 ảnh Karpathy test (còn 2,562) [C6 §1.1]; D10 phụ lục ghi nhận cả hai và khuyến nghị bỏ 133 ảnh cho sạch khi chạy P-B.
- **POPE:** C10 ghi "chưa đo (đã có job pope_vi)" [C10 §4]; C3, C7, C8 dùng kết quả pope_vi đã về lúc 07:43 [C3 §2i]. Khác thời điểm.
- **Lớp gold được ít nhất một output gọi:** C8 ghi 92.7% được gọi và 8.0% chưa bao giờ được gọi [C8 P2]; file kết quả của C8 cho thấy 92.7 là recall trung bình theo ảnh, 8.0% là tỉ lệ gộp (`out_ktvic_backbone.json`). Các pool khác: hợp 58 file R 90.6 [C7 §3e]; vote 71 hệ ở t 0.02: R 89.8 [C1 §2d].
- **Nhỏ, do làm tròn hay tập con:** người Việt 5 caption gộp 72.6 [C1, 3,850 ảnh], 71.8 [C4, 1,155], 72.9 [C6, 2,562], 71.3 / 72.0 [C10, test / val]; danh sách lớp "nhỏ" tự gán của KTVIC: 25 lớp, 10.1% lớp gold [C1 §1] so với 27 lớp, 12% cặp gold [C7 §3c]; recall theo cỡ của 5 người gộp 25.7 / 53.1 / 85.1 [C1] so với 23.8 / 52.8 / 85.0 [C7]; P1 s43 COCO short F1 59.3 [CTX] so với 59.2 [T1 §4]; P1 POPE EN trung bình 83.0 [C8 P4] so với 83.07 tính từ [POPE] (suy ra); fuse2 KTVIC F1 58.2 [C10 §1b] so với 58.1 [CTX].

## 4. Chuẩn Q1/Q2 thực tế
- Q1/Q2 là hạng của **tạp chí** (SCImago/JCR), không phải thuộc tính của kết quả. Không tạp chí Q1/Q2 hay hội nghị top nào C10 đọc dùng ngưỡng tuyệt đối kiểu "≥ 90"; bài được nhận vì tăng so với baseline mạnh dưới giao thức chuẩn [C10 §0].
- Không bài đã nhận đăng nào C10 tìm được có caption object P, R và F1 cùng ≥ 90 (đo, tài liệu) [C10 §0, §2]:
  - F1 object caption cao nhất: 79.7 (Attention Reallocation, IJCV 2025, CHAIR-F1, LLaVA-1.5-13B);
  - recall caption cao nhất: 80.8 (MemVR, ICML 2025, caption ~100 từ);
  - chỉ probe có/không chạm ~90: POPE F1 90.6–91.1 (InternVL2.5/3-8B), AMBER-discriminative F1 90.9 (RLAIF-V-12B);
  - bộ phân loại đa nhãn huấn luyện riêng trên COCO cũng chưa có OF1 ≥ 90; tốt nhất 86.8 (Q2L) [C10 §2g; C1 §4].
- Mức tăng được nhận (đo, tài liệu) [C10 §3]:

| Bài (venue) | Độ đo | Baseline → phương pháp |
|---|---|---|
| OPERA (CVPR 2024) | CHAIR_i, 512 token | 14.7 → 12.8 |
| Attention Reallocation (IJCV 2025) | CHAIR object F1 | 77.1 → 78.3 |
| SC-Captioner (ICCV 2025) | object F1 so với SFT+DPO | 75.1 → 76.4 |
| MemVR (ICML 2025) | recall | 77.1 → 80.8 |
| CLVA (PR 2026) | CHAIR_i / recall | 15.2 → 12.7 / 76.7 → 80.2 |
| PAI (ECCV 2024) | POPE F1 | 85.59 → 86.42 |
| ARA (TOMM 2025) | POPE F1, random | 84.75 → 88.63 |
| CCCaption (CVPR 2026) | correctness | 70.19 → 70.57 |

- Tóm lại (đo, tài liệu) [C10 §0]: CHAIR_i −1 đến −2 điểm tuyệt đối; object F1 +1.2 đến +1.8; recall +3 đến +4 khi CHAIR không xấu đi; POPE F1 +0.8 đến +4.
- Cùng chiều ở các báo cáo khác (đo, tài liệu): SC-Captioner trên Qwen2-VL-7B, DOCCI F1 69.32 → 71.63 [C4 §7a]; MARINE, recall trung bình 5 LVLM 40.3 → 44.5 [C2 §4]; phương pháp không huấn luyện trên Qwen2.5-VL-7B giảm CHAIR_i 0–2.8 điểm [C3 §0]; độ phân giải/tiling dời POPE −1.1 đến +4.9 [C7 §0]; Qwen3-VL 2B → 32B, recall caption 72.1 → 76.5 [C8 §4a].
- Thống kê: 7/30 bài báo cáo nhiều lần chạy; 0/30 kiểm định ý nghĩa cho phép so sánh chính (đo, tài liệu) [C10 §3]. MDE của ta: khoảng 3 F1 trên KTVIC-558, khoảng 1.3 trên COCO-2500 (ước tính, C10 suy từ CI của R4_01) [C10 §3].
- Tiếng Việt: 61 bản ghi OpenAlex 2022–2026, chỉ 2 bài tạp chí hạng Q1/Q2 (UIT-OpenViIC; HDUCap); không bài nào báo object P/R/F1, CHAIR hay POPE; mức công bố chỉ có n-gram: OpenViIC CIDEr 76.48, KTVIC GRIT 136.0 (đo, tài liệu) [C10 §2i].
- **Vì sao "90%" không phải thanh của venue:** không venue nêu; không bài nào đạt; trần người của ta thấp hơn (KTVIC R so với hai người 66.6, F1 so với 70.9, P so với một người 85.3; COCO F1 so với năm người 79.5); và đuổi theo nó ép ra caption dạng inventory, thứ reviewer sẽ bắt qua CIDEr [C10 §5 R1].
- **Khung C10 đề xuất** [C10 §5 R2–R3]: KTVIC short ngang một người (F1 60.5; fuse2 hiện 58.2, chênh −2.3, p = 0.050 [C10 §1b]); KTVIC detailed ngang hai người (70.9 ở 2.57 object/caption); COCO chạm đường biên người gộp (P 90.0 ở R 66; P 85.3 ở R 74.3). Claim chính: ΔF1 ≥ +2 so với P1 và fuse2, P và C không giảm ngoài CI, 3 seed, bootstrap ghép cặp, hiệu chỉnh Holm. C10 §5 R5 có gợi ý một câu định vị kiểu ưu tiên công bố; tài liệu này không dùng câu đó vì chưa kiểm chứng được.

## 5. Phát hiện cốt lõi: mô hình "thấy" nhiều hơn nó "nói"

### 5a. Thấy (POPE) so với nói (caption), theo cỡ object [C7 §2b, §2f]
"Thấy" = % object có mặt được trả lời "có" [MH], POPE-COCO 500 ảnh val2014, prompt tiếng Việt, nhãn RePOPE. "Nói" = % cặp (ảnh, lớp gold) mà caption gọi tên, trên 2,500 ảnh probe. Cỡ = instance lớn nhất của lớp.

| Cỡ | fuse2 thấy | fuse2-short nói | P(nói ∣ thấy) | zero-shot thấy | zero-shot detailed nói |
|---|---|---|---|---|---|
| S (< 32² px) | 67.1 | 7.2 | ≈ 11% | 55.0 | 27.5 |
| M | 88.3 | 23.5 | ≈ 27% | 83.1 | 54.0 |
| L (≥ 96² px) | 96.0 | 56.3 | ≈ 59% | 95.0 | 80.2 |

- Cả bảng là số đo; tỉ lệ P(nói ∣ thấy) do C7 tính. Nhãn POPE gốc cho số "thấy" thấp hơn 4–8 điểm; xu hướng trả lời "có" của adapter (tỉ lệ có 41–47%) làm phồng số của P1 [C7 §2f].
- Trong 55.8 điểm recall fuse2-short mất trên COCO: 14.0 (25%) là object nhỏ; 21.5 (39%) là object LỚN, trung vị 42 token thị giác (đo) [C7 §2b]. 29.8 điểm là lớp mà một file caption khác gọi tên trên cùng ảnh, ở cùng độ phân giải (đo) [C7 §2e].
- Vì vậy nhận thức hoàn hảo chỉ đưa fuse2-short từ F1 59.4 lên 62.5 (cận trên) [C7 §2g].

### 5b. Bỏ sót là do chính sách gọi tên; mention "sai" phần lớn là object thật [C8 §3; C3 §2]
- KTVIC: 81.6% lớp P1-short bỏ sót được ≥ 2 trong 70 output khác của **cùng backbone** gọi tên; 69.9% được ≥ 5 output gọi; 47.6% được riêng zero-shot detailed gọi (đo) [C8 P2]. fuse2-short: 80.0 / 67.4 / 46.6% (đo) [C8 P2].
- Chỉ 8.0% lớp gold không output nào trong 71 gọi, và phần này chủ yếu là cách chọn từ: cô gái, nam thanh niên, toà nhà, sạp hàng (đo) [C8 P2].
- COCO: lớp "nổi bật với người" bị bỏ sót nhưng được output khác gọi: 67% (fuse2-short), 68% (P1-short), 31% (zero-shot detailed) (đo) [C8 P1].
- Mention "sai" so với tham chiếu KTVIC: trên 555 ảnh có panel OpenViIC độc lập [SP], panel trực tiếp gọi tên 56.5% [49.2, 63.6] mention "sai" (so với 5 tham chiếu) của P1-short (đo; C3 §0, §2c; D10 dùng số này). Vì trong phép kiểm chéo 1v4 một người chú thích KTVIC nêu object ngoài 4 người kia cũng chỉ được panel OpenViIC gọi lại p_h = 58.8% [54.9, 62.5] (đo, độ nhạy của panel), ước lượng tỉ số hiệu chỉnh độ nhạy trong [SP] (`real_fraction_est = 100 × p_s / p_h`) là 57.21 / 58.78 = 97.3% [85.6, 109.6] cho `p1-gold-short` (98.5% cho `p1_s43-short`, 95.7% cho `fuse2_s42-detailed`; ước tính) [C8 §0, §3 P2] — tức phần dư chưa xác nhận của SFT ngang mức của người, và bộ nhận thức hoàn hảo chỉ cộng tối đa P +0.5 [0, +2.9] (§3e).
- Giải phẫu false positive của P1-short (21.2% mention): 12.3 điểm là danh từ cảnh/vật không tham chiếu nào gọi; 5.5 điểm là danh từ chỉ người khác với tham chiếu; chỉ 1.7 điểm là object COCO-80, loại lỗi CHAIR/POPE nhắm tới (đo) [C3 §2b]. Bộ kiểm GDINO [MH] chỉ có 9/1,017 mention để bỏ, dP +0.0 [−0.2, +0.3] (đo) [C3 §0].

### 5c. Một đường precision–số lớp cố định [C9 §0, §2]
- KTVIC: mọi adapter (P1, fuse2, e5, MR5, tags; short hay detailed) nằm trong −2.0..+1.6 F1 quanh đường biên tiền đăng ký, trừ selffuse (−3.8 / −4.2) (đo) [C9 §0].
- COCO: mọi output Qwen2.5-VL-7B nằm trong −1.7..+1.6 F1 quanh một đường fit trên các tiền tố của đoạn zero-shot; ngoại lệ là VSPS-short (−4.5) (đo). Khác biệt F1 COCO 59–73 giữa các hệ gần như chỉ là số object nêu ra [C9 §0].
- Người nằm trên đường của mô hình 5.9–7.5 F1 ở cùng độ dài (đo) [C9 §0, §2e]: người chọn object tốt hơn.
- Ở độ dài fuse2-detailed (M 3.15), khoảng cách tới oracle Bayes gần như toàn là xếp hạng: +18.9..+21.8 F1; độ dài chỉ +0.6..+1.3 (ước tính, mô hình Bayes) [C9 §2c].
- Lọc hoàn hảo trên nội dung đã sinh đưa fuse2-detailed lên F1 75.9 (cận trên) [C9 §2d]: object đã có trong cái ta sinh; chọn chúng mới là nút cổ chai.

### 5d. Chọn lựa là nút cổ chai, không phải phát hiện [C5 §0, §3; C2 §2d]
- Ở mức tập lớp (kế hoạch, chưa thành câu), quyết định Bayes cho metric nâng F1 của P1 54.5 → 62.9 (+8.3 [+6.5, +10.3]) và fuse2 58.1 → 64.9 (+6.8 [+5.1, +8.6]); P giảm 10–12, R tăng 17–18 (cận trên của bản thành câu; luật đóng băng từ dev) [C5 §0, §3c].
- Khi chỉ được chọn **một** caption có sẵn mỗi ảnh, MBR expected-F1 đã hiệu chỉnh hòa UPE: trên biên F1–CIDEr, chênh −0.9..+1.1 F1 (đo) [C5 §0, §3d].
- Adapter hiện tại bỏ qua danh sách object trong prompt: tag được nêu 18.1% → 17.7% (fuse2), 17.4% → 19.5% (P1) (đo) [C5 §3f].
- Bằng chứng detector [MH] thêm chút AUROC so với mẫu, nhưng khi thành câu thì gần như không thêm F1: +0.3 [−0.3, +1.0] (đo) [C2 §2d]. C2 kết luận: thành câu, không phải phát hiện, là nút cổ chai.
- COCO: mất ở chế độ short là mất từ vựng trên lớp KTVIC hiếm gọi (§2c) [C6 §1.4]; ở chế độ detailed là mất độ phủ object không người nào nêu (37.3% cặp instance) [C6 §0].

**Hệ quả.** Đòn bẩy còn lại là quyết định nêu object nào và đưa nó vào câu mà không phá CIDEr. Trên KTVIC, độ phân giải, backbone và detector thêm rất ít [C7 §0; C8 §0; C2 §0].

## 6. Các đề xuất (xếp hạng)

### 6a. Bảng đề xuất (một dòng mỗi đề xuất; C1 chỉ đo, không đề xuất)
| # | Đề xuất: cơ chế | Novelty (báo cáo tự đánh giá) | Prior gần nhất (arXiv) | KTVIC P / R / F1 | COCO F1 | Loại số | Chi phí C | GPU-h | Kill (tóm tắt) | Bằng chứng | D10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R | **UPE-MBR** (R8; D9 đang chạy): MBR chọn caption theo expected object F1 với panel chưa thấy; phiếu mẫu [MH] | trung bình-thấp [T3 §0] | 1512.06974; 1206.4625; 2601.22451; 2302.01328 | −0.34 / +3.00 / +2.24 (dev, T 0.5) | chưa đo (F2, UIT-ViIC) | đo [UPE-A] | +0.30 [−5.05, +5.47] | ~3.5 [T3 §5] | F1–F3 và kill của [PRE] | mạnh | D9, đang chạy; D10 không đổi |
| 1 | **C2-A CG-TagSFT**: SFT fuse2 có tag [MH] trong prompt; dropout 40% từng tag, 50% cả danh sách; tag nhiễu theo tỉ lệ FP; unlikelihood phạt chép tag vắng [C2 §5A] | trung bình (một tổ hợp) | 2307.16525; 2406.10839; 2310.01779; 2405.18654; 2402.09801 | short +1..+2 / +1..+3 / +1..+2.5; detailed F1 +0.5..+2 | +1..+4 | ước tính | −2..+3 | ~8 tới cổng; ~19 cho 3 seed | dev300: dR < +2.0, dP < −1.0, F1 không tag lệch quá ±1; placebo ≥ 70% dF1; > 10% tag nhiễu bị nêu; C < fuse2 − 3 | yếu: kênh tag hiện bị bỏ qua; trần oracle F1 +7..+8 (short) | Bác như sửa đổi (a) của PLAN-F1 (85%); bản chạy riêng không có trong D10 |
| 2 | **C2-B PREC**: P(gold) = P(có mặt ∣ tagger, VLM có/không) × P(liên quan ∣ có mặt, loại gold); thêm lớp theo luật plug-in F1; tagger COCO phải sạch [C2 §5B] | không ghi mức; báo cáo tự gắn cờ "metric-shaped" | 1512.06974; 2402.08680; 2310.16045; 2404.19752; 2403.00425 | F1 0..+0.8 | hợp 87.8–89.0; có bộ kiểm: 88 đến 92.6–93.7 | mô phỏng; cận trên | lớn: một mệnh đề inventory −54 C-âm tiết | ~1.8 với checkpoint công khai; +8–10 nếu tự huấn luyện tagger | F1 tập < 88 ở P ≥ 88 trên ảnh COCO-2014-train giữ lại; C UIT-ViIC giảm > 10; bản câu < 50% bản tập | yếu; chỉ báo như "caption + inventory đã kiểm" | Không duyệt; inventory chỉ là baseline gaming (i, 93%) |
| 3 | **C3-A FOPR**: veto mention có q = P(được người gọi ∣ ảnh, lớp) < F̂/2; q từ phiếu mẫu [MH], hiệu chỉnh isotonic trên dev300; đổi sang ứng viên gần nhất [C3 §6A] | trung bình-thấp | 2305.07021; 2601.22451; 2607.27823; 2303.08896; 1402.1892 | +1.5..+3 (sau đòn recall +3..+5) / −0.3..−2 / 0..+0.5 | ±0.3 | đo (luật đóng băng: P +1.8 [+1.0, +2.6], F1 +0.0) và ước tính | −0.5..−1.5 | 0 (dùng mẫu UPE); ~3.5 nếu chạy riêng | dev: CI dưới của dF1 < −0.3 hoặc dP < +1.5; C < −1.5; UIT-ViIC CI dưới < −0.5; không hơn veto ngẫu nhiên cùng số | mạnh, hiệu ứng nhỏ | **Bác** như sửa đổi (b) của PLAN-F1 (85%) |
| 4 | **C3-B VGD-vi**: bộ kiểm L1-logistic tại span mention COCO-80 (attention, entropy, hidden state); nhãn instance COCO-2014 train; rollback và cấm lớp [C3 §6B] | thấp | 2607.27823 | P 0..+0.5 | ±0.5 (P +1.5..+2.5) | ước tính | ≈ −2 | ~2 | dP COCO < +1.5; CI F1 < 0; C KTVIC < −1 | yếu | Không có trong D10 |
| 5 | **C4-PA Union-F1 CN-RLOO**: reward C/s_C + λ·F1 với hợp tham chiếu của ảnh train, λ 1; chặn danh sách [C4 §8] | thấp ("ablation, không phải đóng góp") | 2109.05115; 2508.06125; 2605.07394; 1612.00370 | so với SFT: +1.3..+2.0 / +1.6..+2.5 / +1.5..+2.2; so với nhánh chỉ CIDEr: F1 +1.6..+2.7 | 0, có thể giảm | ước tính (proxy cross-fit); in-sample +11..+15 là cận trên | −1..−5 so với nhánh chỉ CIDEr | ~4/seed (1,000 ảnh); ~8 cho 2 seed | dF1 so với nhánh CIDEr < +1.5 hoặc CI chứa 0; C dev thấp hơn > 3; mention/caption > tham chiếu + 0.3, âm tiết +1.5, chặn danh sách > 3%; panel F1 thấp hơn | trung bình (hai pool khớp) | **Hoãn** tới kết quả 35_e (v, 92%) |
| 6 | **C4-PB ILV-RLOO**: cùng engine trên UIT-ViIC train (bỏ ảnh probe), reward C + λ·F1 với nhãn instance người [C4 §8] | trung bình-thấp | 2504.07954; 2503.01785; 2109.05115; 2508.20181; 2101.09865 | ≈ 0 | short +4..+7 (→ 63–66); detailed → 70–74 | ước tính | UIT-ViIC −3..−8 | ~12.5; thử 1,000 ảnh ~4 | val: F1 − SFT < +3 hoặc CI chứa 0; F1 theo caption EN có CI chứa 0; C val giảm > 3; chặn danh sách > 3% | yếu (tỉ lệ chuyển mượn từ KTVIC) | Để sau, không trước kết quả 35_e; chưa duyệt (85%) |
| 7 | **C5-M1 PLAN-F1**: hậu nghiệm "được panel gọi" hiệu chỉnh trên dev300 (phiếu [MH], cờ greedy, prior lớp) → luật plug-in dạng đóng cho P micro / R macro, chặn 3 lớp → realiser control-SFT [C5 §5] | trung bình-thấp | 1402.1892; 1206.4625; 1411.4952; 1612.00576; 2508.11616; 2608.21819 | kế hoạch chặn 3: −5.1 / +9.7 / +4.9 (fuse2), −7.7 / +12.2 / +6.8 (P1); không chặn: F1 +6.8 / +8.3 | ≤ +2 | cận trên (kế hoạch); bản câu chưa đo | chưa đo; ngân sách −5 | ~5–6 | K1: nêu < 85% lớp kế hoạch hoặc > 0.3 lớp ngoài; K2: dF1 dev < +3.0, CI chứa 0, hoặc hơn UPE < +1.0; K3: C < greedy − 5 hoặc B-4 < greedy − 3 | trung bình (kế hoạch bền qua 3 nguồn hiệu chỉnh); độ trung thành chưa biết | **Duyệt** pilot dev300 (ii, 85%); bác cả bốn sửa đổi (a)–(d) |
| 8 | **C5-M2** kế hoạch mức câu cho COCO: bỏ câu mà mọi lớp < 2 phiếu; thêm câu của hệ khác cho lớp ≥ 2 phiếu [C5 §5] | thấp (phụ lục) | 2405.13131; 2402.10978 | không áp dụng | +0.9 [+0.5, +1.3] (ảnh mới, đóng băng); +1.8 trên tập chính | đo | không đo được (ảnh probe không có tham chiếu Việt) | 0 | đã qua, sát, khi lặp lại trên ảnh mới | mạnh, nhỏ | Không có trong D10 |
| 9 | **C6-1 VGR**: thêm ~2,000 dòng "liệt kê đồ vật", đích là nhãn instance COCO-2014 viết bằng tiếng Việt; chọn lớp theo khoảng trống từ vựng KTVIC [C6 §4] | "gần prior, chưa bị scoop" | 1606.07770; 1806.06004; 2009.13682; 2403.01244 | P 0..+2 / ±1 / ±1 | short 61–64; detailed 67–71 | ước tính (trần stand-in +5.45 [+4.48, +6.39] là cận trên) | KTVIC short 0..−3 | ~9/seed; ~23 cho 2 seed + baseline WiSE-FT | val UIT-ViIC: dF1 < +2.0 hoặc CI chứa 0; không hơn LoRA-scaling; C KTVIC < 140.7; rò danh sách > 1% | trung bình | **Duyệt theo giai đoạn** (78%, dưới ngưỡng 80%; U-001 chốt chạy bước 0 WiSE-FT trước, quyết VGR sau; luật vô ích) |
| 10 | **C6-2 IVSR**: caption detailed zero-shot của mô hình gốc [MH] trên 2,000 ảnh Karpathy-train, bỏ mệnh đề nêu lớp không có instance; thêm vào hỗn hợp VGR [C6 §4] | incremental | 2402.13669; 2403.01244; 2609.16639; 2508.20181; 2311.13614 | ±1 | detailed 70–75 | ước tính | KTVIC short 0..−3; detailed có rủi ro | +5/seed (cần VGR trước) | dev detailed không ≥ VGR + 3; < zero-shot − 1 hoặc < 1.5 lớp/caption; P detailed KTVIC giảm > 2 hoặc C short giảm > 3 | yếu | Không có trong D10 |
| 11 | **C7-P1 UGZ**: ứng viên = lớp của caption detailed trừ lớp của caption short; probe "có" một token [MH]; zoom tile chỉ khi probe không chắc; chèn ≤ 2 object (KTVIC: luật CC-ADD; COCO: mệnh đề cố định) [C7 §6] | không ghi mức | 2403.00425; 2502.17422; 2405.19092; 2504.14920; 2411.16044; 2312.14135 | F1 +1..+3 (phần zoom ≤ 0.5 R) | 72–75 từ 59.4 (phần zoom ≈ +1) | ước tính (trần pool 74.2 đo / 80.1 cận trên) | KTVIC −1.2 [−4.7, +1.7] (CC-ADD, R8); COCO không đo được | ~3–4 | zoom − không zoom < +0.5 F1; C KTVIC giảm > 3 hoặc dF1 < +1; POPE object nhỏ vẫn < mức object vừa − 10 | yếu–trung bình; rủi ro inventory | **Bác** (87%) |
| 12 | **C7-P2** kiểm chứng độ phân giải: KTVIC 2,048 token; COCO phóng 2×; POPE 2× [C7 §6] | không nhận novelty | 2403.13043 (S²) | dR ±1, dP ±1 | dR ≤ +1.4 (short) | ước tính | không nêu | ~4.3–5.3 | KTVIC dR < +1 và COCO dR < +1.5 → báo âm, đóng lever | trung bình (đo âm trên CPU, lẫn nội dung) | Chỉ phần KTVIC 2,048 token (iv-c, 78%, dưới ngưỡng 80%; U-001 duyệt chạy ở ưu tiên thấp); bác COCO 2× và POPE 2× |
| 13 | **C8-A Qwen3-VL-8B** (C8-B InternVL3.5-8B dự phòng): cùng công thức QLoRA; sàng zero-shot S0 → cổng dev G1 → 3 seed fuse2 [C8 §5] | không (kỹ thuật) | 2606.27373; 2412.03555; 2503.19786 | P 0..+0.5 / R 0..+1 / F1 0..+1 | sau SFT +1..+3 (short 60.3–62.7) | ước tính (chiếu) | 0..+2 | 2.5 (S0) + 4.2 (G1) + 21 | S0: dF1 COCO detailed ≥ +2.0 hoặc short ≥ +1.5 với CI > 0, tỉ lệ absent không tăng; G1: COCO short ≥ +1.5, F1 dev giảm ≤ 1.5, C giảm ≤ 3, ≤ 22 GB | yếu; rủi ro nhiễm COCO-2017 | **Duyệt** S0 Qwen3-VL-8B ngay (88%); G1 thay 57/58 nếu S0 qua; C8-B không được nêu |
| 14 | **C9-A PCD-GAFS**: SFT đích ghép theo đồng thuận; câu 1 là caption; viết tiếp khi lớp mới có q trung bình > F̂/2, q theo loại gold [C9 §5A] | thấp đến trung bình | 2007.09580; 2507.01409; 2402.14545; 2310.01779; 2311.06242 | caption không đổi; mô tả 63–65 / 67–71 / +1..+3 | mô tả +4..+7 (→ 70–73) | ước tính; chi phí caption đo = 0 | 0 cho caption (đo: C-âm tiết +1.3..+2.2, CI chứa 0) | ~10–14 | C câu 1 thấp hơn short > 2.0; mô tả < +1.0 (KTVIC) và < +3.0 (COCO); CHAIR_i COCO > 19.5 | trung bình; chỉ hợp lệ khi khai báo hai đầu ra | Bác gộp vào PLAN-F1 (d, 80%); **duyệt** giao thức báo cáo hai đầu ra của C9, 0 GPU |
| 15 | **C9-B inventory khai báo**: đầu ra thứ ba là danh sách tên lớp; zero-shot hoặc QLoRA trên nhãn COCO-train2014 + hợp tham chiếu KTVIC [C9 §5B] | thấp (giá trị chẩn đoán) | 2303.05657; 2306.03514; 2311.06242; 2107.10834 | ≈ 0 (64–68) | inventory: zero-shot 73–76; có giám sát 80–88 | ước tính | 0 (đầu ra riêng) | ~10 | zero-shot < 75.0; có giám sát < 85.0 → bỏ mọi claim COCO ≥ 90 | yếu; phải báo như tagging | Không duyệt; inventory chỉ là baseline gaming (i) |
| 16 | **C10 R2–R3** khung mục tiêu: đường biên người + ΔF1 ghép cặp [C10 §5] | không phải phương pháp | — | — | — | — | 0 | 0 | mọi CI F1 dưới 60.5 (short) và 70.9 (detailed) → chỉ claim tăng ghép cặp | — | Theo (i) (93%): mục tiêu nêu theo trần đo được và mốc của C10 |
| 17 | **C10 R4** độ đo chuẩn để so: CHAIR 64/512 token (gold Rohrbach), POPE + RePOPE, AMBER [C10 §5] | không phải phương pháp | 2504.15707; 2311.07397 | — | — | — | 0 | ~10 (POPE đã xong) | > 5% không parse được → chỉ báo P/R/F1 kèm trần | — | Không có trong danh mục GPU của D10 |

### 6b. Xếp hạng: lợi kỳ vọng × độ mạnh bằng chứng ÷ (GPU + chi phí CIDEr)
Chỉ số heuristic, suy ra ở đây: I = G·E / (K + 1). G = tổng trung điểm khoảng lợi kỳ vọng trên bốn độ đo (KTVIC P, R, F1; COCO F1), lấy từ bảng 6a; độ đo không nêu tính 0. E = độ mạnh bằng chứng do tài liệu này đánh giá: 3 = đo với luật đóng băng; 2 = proxy CPU hoặc cận trên đo được, hiệu ứng ước tính; 1 = chiếu, mô phỏng, tài liệu. K = GPU-h tới cổng kill sớm nhất + |trung điểm chi phí C| (chi phí dương tính 0). Thứ tự trong cùng mức I không có ý nghĩa thống kê.

| Hạng | Đề xuất | G | E | K | I | Ghi chú |
|---|---|---|---|---|---|---|
| — | UPE-MBR (tham chiếu, D9) | 4.9 | 3 | 3.5 | 3.3 | đã có bằng chứng GPU trên dev |
| 1 | C7-P1 UGZ | 16.1 | 1 | 4.7 / 56 | 2.8 / 0.3 | số sau: cộng chi phí mệnh đề nối trên COCO, mượn −52.5 C-âm tiết của [C4 §5] |
| 2 | C5-M2 | 0.9 | 3 | 0 | 2.7 | phụ lục; lợi tuyệt đối nhỏ |
| 3 | C3-A FOPR | 1.35 | 3 | 1.0 | 2.0 | đòn duy nhất nâng KTVIC P có số đo; F1 ≈ 0 |
| 4 | C5-M1 PLAN-F1 | 11.4 | 2 | 10.5 | 2.0 | cận trên; đổi P lấy R; độ trung thành chưa biết |
| 5 | C9-A PCD-GAFS | 11.3 | 2 | 12 | 1.7 | là F1 của mô tả, không phải của caption |
| 6 | C4-PA | 5.55 | 2 | 7 | 1.4 | nâng cả P và R; nhánh đối chứng của gate v2 đã có ngân sách |
| 7 | C2-A | 7.75 | 1 | 8 | 0.9 | |
| 8 | C6-2 IVSR | 6.7 | 1 | 6.5 | 0.9 | 0.4 nếu tính cả GPU của VGR |
| 9 | C6-1 VGR | 4.1 | 2 | 10.5 | 0.7 | |
| 10 | C4-PB | 5.5 | 1 | 9.5 | 0.5 | |
| 11 | C8-A (C8-B) | 3.35 | 1 | 6.7 | 0.4 | |
| 12 | C7-P2 | 0.65 | 2 | 4.8 | 0.2 | G từ "tốt hơn một cỡ" của [C7 §2g]; là phép kiểm reviewer sẽ đòi |
| 13 | C3-B | 0.25 | 1 | 4 | 0.05 | |
| ngoài hạng | C2-B, C9-B (inventory/tagging); C10 R2–R4 (khung báo cáo) | | | | | không phải độ đo caption; gộp vào bảng caption là gaming |

**Đọc bảng.**
- Chỉ số ưu tiên đòn rẻ, đã đo, lợi nhỏ (UPE, C5-M2, FOPR). Lợi tuyệt đối lớn nằm ở PLAN-F1 (KTVIC F1 +4.9..+8.3 ở mức kế hoạch), UGZ (COCO, nhưng nhánh mệnh đề cố định gần với inventory) và PCD-GAFS (mô tả). Không đòn nào đổi câu trả lời về 90: kể cả khi chồng, F1 KTVIC kỳ vọng vẫn dưới vùng hai người 70.9–73 và dưới trần Bayes 84–89; COCO dạng caption vẫn dưới 79.5.
- Tổng G che mất đổi chác P–R: PLAN-F1 và PCD-GAFS tăng R, F1 bằng cách hạ P; chỉ FOPR và C4-PA nâng được KTVIC P.
- Thứ tự gợi ý để judge cân nhắc (không phải quyết định): (a) FOPR trên mẫu UPE có sẵn, 0 GPU-h; (b) cổng K1 về độ trung thành của PLAN-F1; (c) C4-PA làm nhánh λ của gate v2; (d) COCO: UGZ chỉ với cách chèn kiểu CC-ADD, hoặc VGR; (e) sàng S0 của C8 (2.5 GPU-h) như phép chẩn đoán, sau khi sửa lỗi tòa/toà nếu dùng KTVIC (§7); (f) inventory chỉ như dòng tagging khai báo.
- **Chỗ D10 khác với bảng chỉ số I và thứ tự gợi ý trên (§9):** (1) **UGZ (hạng 1 theo I) bị bác (87%):** phần mới (zoom) chỉ thêm ≤ +1 F1 theo ước tính của chính C7 nên dễ chạm kill 1; phần còn lại là hoàn thiện có kiểm, trên COCO nối mệnh đề cố định (trúng mục gaming (c) của C9 §4) mà không có cổng giữ CIDEr trên COCO, còn trên KTVIC (+1..+3; CC-ADD đo được +1.1) trùng với PLAN-F1 và UPE; (2) **FOPR (hạng 3 theo I) bị bác làm sửa đổi (b) của PLAN-F1 (85%):** cắt ở q < F/2 = 0.27–0.29 trên cùng hậu nghiệm trong khi PLAN-F1 đã lọc quanh P* = 0.61–0.66, nên chỉ bỏ bin 0 phiếu (~3% mention, F1 +0.0 [C3]) và tạo thêm nhánh ngã ba (forking path); (3) **Nhánh COCO được judge xếp hạng theo giá trị thông tin và cổng kiểm thay vì I:** hạng 1 là **S0 Qwen3-VL-8B** (hạng 11 theo I; duyệt ngay, 88%, vì chỉ tốn 2.5 GPU-h suy luận, có cổng PASS/KILL tiền đăng ký, không có đường gaming, quyết định câu hỏi backbone lẫn slot backbone thứ hai), hạng 2 là **VGR** (hạng 9 theo I; duyệt theo giai đoạn ở 78%, U-001 chốt chạy bước 0 WiSE-FT trước), hạng 3 là **C4-PB** (hạng 10 theo I; hiệu ứng COCO kỳ vọng lớn nhất +4..+7 có neo CIDEr, nhưng để sau phán quyết 35_e, 85%); (4) **C4-PA bị hoãn (92%)** tới sau kết quả 35_e để không nhìn lần hai trên engine chưa qua cổng; (5) **PLAN-F1 được duyệt chạy pilot dev300 (85%)** vì là đòn duy nhất có kế hoạch vượt đường biên chọn mẫu trên dev (cross-fit, chặn 3 ở T = 0.8: +3.7 [+1.5, +5.8] so với greedy; +1.3 [−0.5, +3.2] / +2.4 / +2.1 so với UPE ở T = 0.8 / 1.0 / 0.5 [C5 §3c, p16]).

### 6c. Chồng lấn và cách ghép
**Ống ghép PLAN-F1 (C5) + realiser có copy-guard (C2) + veto precision (C3) + probe có mặt (C7) + đầu ra kép (C9).**
1. Bằng chứng [MH]: greedy + k mẫu. Các job mẫu của UPE đã có: dev 36_z (T 0.5 / 0.8), test 50_f, UIT-ViIC 52_c [C3 §6A; PRE].
2. Hậu nghiệm "được gọi tên": calibrator của C5 (phiếu, cờ greedy, prior lớp) [C5 §5]. Probe "có" của C7 làm thêm đặc trưng có mặt, có ích chủ yếu cho COCO; trên KTVIC, tín hiệu có mặt gần như không thêm: AUROC 0.762 → 0.765 [C5 §3b], tag +0 F1 [C2 §2d].
3. Quyết định: luật plug-in của PLAN-F1, chặn 3 lớp [C5 §2, §5]. FOPR là nửa precision của cùng luật F/2 (Lipton 1402.1892), nên không chạy riêng ở mức tập; dùng nó ở bước kiểm câu, để veto lớp có trong câu mà không có trong kế hoạch [C3 §6A].
4. Thực hiện: realiser control-SFT của C5, huấn luyện với copy-guard của C2 (dropout tag, tag nhiễu, unlikelihood) để không chép mù lớp sai của kế hoạch [C2 §5A; C5 §5]. Cổng K1 của C5 (≥ 85% lớp kế hoạch được nêu, ≤ 0.3 lớp ngoài) quyết định ống còn sống hay không.
5. Đầu ra: theo C9, câu 1 là caption (giữ C), phần mô tả mang kế hoạch đầy đủ và dừng theo luật F/2 gắn với loại gold; mỗi đầu ra chấm bằng độ đo của chính nó [C9 §4, §5A].
- Rủi ro: lớp sai trong kế hoạch thành câu sai mà trôi chảy, chỉ bị tính vào P, không vào C [C5 §7]; adapter hiện bỏ qua danh sách trong prompt [C5 §3f; C2 §2c]; hiệu ứng các bước không được giả định là cộng dồn.
- **Phán quyết D10 đối với ống ghép trên [D10 (ii)]:** Judge **chỉ duyệt PLAN-F1 nguyên bản như C5-M1 đặc tả** (pilot trên dev300, 85%) kèm **giao thức báo cáo hai đầu ra của C9 ở 0 GPU trên các dự đoán sẵn có** (80%), và **bác cả bốn sửa đổi (a)–(d)**: (a) *copy-guard (C2)* (NO, 85%): huấn luyện realiser bỏ bớt lớp trong danh sách, ngược trực tiếp với cổng K1 (đòi nêu ≥ 85% lớp kế hoạch), trong khi lỗi của kế hoạch chủ yếu là object thật mà người chú thích không nêu (panel OpenViIC xác nhận 56.5% FP của P1 [C3]) chứ không phải vật thể vắng mặt, lại tốn thêm tín hiệu tagger (~1 GPU-h, ~80 dòng code); (b) *veto FOPR (C3)* (NO, 85%): cắt ở q < F/2 = 0.27–0.29 trên cùng hậu nghiệm mà PLAN-F1 đã lọc quanh P* = 0.61–0.66, chỉ bỏ bin 0 phiếu (~3% mention, F1 +0.0) và thêm một forking path; (c) *probe có mặt (C7)* (NO cho pilot, 80%; chỉ xét như ablation sau pilot): nhắm vào loại lỗi thiểu số, C3/R6 đã thấy probe ngang veto theo phiếu, và ứng viên kế hoạch lấy từ mẫu của chính mô hình nên mô hình đã "thấy"; (d) *gộp PCD-GAFS (C9) vào realiser* (NO, 80%): PCD-GAFS cần SFT fuse-k riêng (4–6 GPU-h) và luật dừng riêng nên không gộp được vào realiser một câu điều kiện theo danh sách; đổi lại, giao thức báo cáo hai đầu ra của C9 §4 (câu 1 là caption: CIDEr +1.3 / +1.9 / +2.2 n.s.; toàn văn là mô tả: F1 +6.0..+6.6) miễn phí và áp dụng ngay ở 0 GPU.

**Chồng lấn khác.**
- UPE là quyết định của PLAN-F1 bị giới hạn ở một ứng viên có sẵn [C5 §2]; PCD-GAFS dùng cùng biến đổi q của UPE [C9 §5A]. Ngưỡng F/2 xuất hiện trong C2-B, C3-A, C5-M1 và C9-A: chỉ được tính là **một** đóng góp, theo cách phát biểu hẹp của C5 (lựa chọn nội dung theo lý thuyết quyết định cho metric P micro / R macro) [C5 §6].
- C4-PA (huấn luyện) chồng với UPE (giải mã): chưa đo [C4 §8; T3 §5].
- C6-1 VGR và C4-PB dùng cùng nguồn nhãn instance COCO-2014 (dạng chữ so với dạng reward) và cùng vấn đề ảnh rò (§7). C2-B, C9-B và đường COCO của C1 là cùng một đường inventory.
- UGZ trên KTVIC dùng luật CC-ADD của R8 [C7 §6], nên trùng đòn "hoàn thiện có bằng chứng" với CC-ADD và UPE.

## 7. Lỗi đo lường và rủi ro rò rỉ dữ liệu
**Lỗi đo lường**
- **Dấu thanh "tòa"/"toà" trong lexicon** [C8 §7; D10 (iv)(a)]: `objects_in("một tòa nhà cao")` cho `['nhà']`, trong khi `objects_in("một toà nhà cao")` cho `['toà nhà']`. Tham chiếu KTVIC test viết `"toà nhà"` 82 lần và không lần nào viết `"tòa nhà"`; hệ SFT học `"toà"`, còn zero-shot detailed viết `"tòa nhà"` 107 lần và `"toà nhà"` 0 lần (đo, judge kiểm; C8 §7 đếm từ `"tòa"` là 67). Tính chung cả cụm dấu kiểu cũ oa/oe/uy trên 558 caption: các dòng SFT chính chỉ 1–2 (`p1assist` ×3, `p1_s43`, `fuse2` s42–44), zero-shot 64 (short) / 273 (detailed), VCD-detailed 277, các hệ cũ 15–58 (đo, judge kiểm) [D10]. **D10 duyệt sửa (90%):** chuẩn hóa vị trí dấu thanh (NFC; các họ oa/oe/uy về một kiểu thống nhất) bên trong cả hai bộ khớp (`rescap/chair.objects_in` và `score_coco_probe.vi_objects`) cho cả gold lẫn output; liệt kê mọi mục lexicon bị chạm trong prereg; chấm lại mọi bảng object và báo song song số cũ – số mới (không chọn hệ hay cấu hình theo thay đổi này); các độ đo n-gram giữ nguyên chuẩn cũ để so được với số KTVIC đã công bố (như GRIT 136.0).
- **Kiểm riêng loại từ "cây" trong "cây cầu" (chưa duyệt sửa)** [D10]: loại từ `"cây"` trong `"cây cầu"` hiện bị bộ khớp tính thành lớp `"cây"` (tree), xuất hiện 7 lần ở `p1assist-short`, 11 lần ở `fuse2-short`, 15 lần ở `fuse2-detailed` (đo, judge kiểm). D10 chưa duyệt sửa bộ khớp lần hai tại đây: chỉ đo tần suất trong các tham chiếu trước khi quyết định.
- **Lexicon thiếu liên kết hypernym:** không có cô gái / chàng trai / đứa trẻ / em bé / cậu bé → người, nên P_h (cộng điểm hypernym) chấm thấp các danh từ này; luật exact không bị ảnh hưởng [C3 §2b; C4 §2].
- **Token CJK lọt vào câu tiếng Việt** [C7 §2i; C8 §7; D10 (iv)(b)]: zero-shot detailed viết `"风筝"` thay vì `"diều"` ở 31/47 ảnh có diều; chữ Trung xuất hiện ở 56/2,500 caption fuse2-short và 260/5,000 caption zero-shot-detailed trên COCO (đo) [C7]. Trên toàn bộ 73 file dự đoán KTVIC test, judge đo tỉ lệ caption có CJK: `p1assist` ×3 và `p1_s43` 0.0%; `fuse2` 0.0–0.9%; zero-shot 0.7% (short) và 5.2% (detailed); các hệ cũ 15–42% (`roundA-detailed` 41.6%, `official-detailed` 27.8%, `VCD-detailed` 17.0%) (đo, judge kiểm; C8 ghi 0–0.2% trên KTVIC và 0.6–2.2% trên COCO sau SFT) [D10]. Khi token lọt thay đúng từ object, matcher bỏ sót; cấm CJK khi giải mã đáng khoảng +0.8 R chỉ riêng lớp diều (ước tính) [C7 §2i]. **D10 (82%):** đây là lỗi sinh văn bản của các hệ đó, không phải lỗi đo lường; **bác** giải mã lại có chặn CJK (vì sẽ làm thay đổi các baseline hiện có), **duyệt** thêm một cột tỉ lệ CJK ở 0 GPU vào mọi bảng kèm một dòng độ nhạy (sensitivity row) bỏ các caption bị ảnh hưởng.
- **Đối chứng độ phân giải (C7-P2)** [C7 §3b, §6; D10 (iv)(c)]: bằng chứng CPU đã dự báo kết quả âm (0/2,500 ảnh COCO chạm trần 1,024 token; 75 ảnh KTVIC bị thu nhỏ nhiều nhất chỉ lệch R +0.4 [−5.5, +6.5] [C7 §3b; D10]). **D10 duyệt ở 78% (dưới ngưỡng 80%, đã được người dùng chốt chạy ở U-001 với ưu tiên thấp, ~1 GPU-h) chỉ riêng phần KTVIC 2,048 token** (`P1_dev` trên dev300 ở `--max-vision-tokens 2048` so với 512 hiện có là lần chạy quyết định: chỉ mở lại lever nếu dR ≥ +2; `p1assist_s42` và `fuse2_s42` trên KTVIC test ở 2,048 làm đối chứng chỉ để báo cáo; các bảng chính giữ nguyên ở 512) và **bác** COCO 2× cùng POPE 2×.
- **Khoảng trống của matcher COCO** [C7 §2i; C8 P1]: surfboard viết "ván trượt" hay "ván lướt" trong khi `coco80_vi` chỉ có "ván lướt sóng"; skis viết "trượt tuyết" thiếu "ván"; backpack viết "túi"; bench viết "ghế". Bàn và ghế chiếm 56–62% false positive instance, là phạm vi từ vựng và nhãn thiếu, không phải ảo giác (đo) [C3 §2g]. Mở rộng matcher là thay đổi công cụ đo, phải đăng ký trước [C7 §2i].
- **CIDEr của file MBR:** CIDEr mức từ đã lưu (96.7–98.0) và C-âm tiết (140.0–141.5) không khớp nhau trên hai file MBR, trong khi trên 65 hệ còn lại hai thang tương quan r = 0.996; cần chấm lại bằng `evaluate.py` [C9 §7].
- **NF4 và bf16 greedy khác nhau trên 55% ảnh**; mọi so sánh phải dùng đúng lượng tử hóa đã triển khai [C3 §4].
- **Thang recall:** recall theo ảnh dễ hơn OR 6–12 điểm (§2a) [C9 §2e]; lexicon chỉ thấy khoảng 42% mention danh từ [CTX].
- **Nhiễu nhãn POPE:** nhãn POPE gốc chỉ đạt F1 94.1 so với nhãn RePOPE (split random), nên POPE có trần nhiễu khoảng 94 (đo) [C10 §2e]. RePOPE sửa 9.3% nhãn "yes" và 1.7% nhãn "no" (đo, tài liệu) [C3 §3].

**Rủi ro rò rỉ**
- **COCO-2017:** khoảng 87–88% ảnh Karpathy test (val2014) nằm trong train2017 (đếm chính xác khi chuẩn bị S0 là 88.1%, còn 295/2,500 ảnh probe thuộc val2017) [C2 §6; C8 §7]. Checkpoint grounding-dino-base trên HF huấn luyện có COCO, nên tag của nó trên probe COCO bị nhiễm; RAM huấn luyện trên 113K ảnh COCO; DETR của MARINE cùng vấn đề [C2 §6]. Qwen2.5-VL rất có thể đã thấy ảnh COCO khi pretrain [C6 §6]. Dữ liệu grounding của backbone mới phủ COCO, Objects365, OpenImages, RefCOCO [C8 §7]. S0 của C8 phải báo riêng tập con val2017 [C8 §5; D10].
- **Vintern:** dữ liệu fine-tune của Vintern-1B có "Viet-OpenViVQA-gemini-VQA" (mô tả do Gemini viết cho ảnh OpenViVQA), trong khi KTVIC test chung kho ảnh UIT với UIT-OpenViIC (401/558 ảnh). Chưa kiểm; phải so hash trước mọi lần dùng [C8 §2J, §7; CTX].
- **59 ảnh UIT-ViIC train nằm trong probe COCO:** đúng là 59 ảnh nằm ngoài tập 2,441 ảnh sạch [C4 §5]. UIT-ViIC train chứa 133 ảnh Karpathy test, 59 trong số đó thuộc manifest 2,500 ảnh; UIT-ViIC val/test không chồng [C6 §1.1]. C4 chỉ bỏ 59 ảnh, C6 đòi bỏ cả 133 (§3e; D10 phụ lục).
- **KTVIC test và OpenViIC:** 401/558 ảnh KTVIC test nằm trong UIT-OpenViIC train; caption OpenViIC chỉ là panel đánh giá, không bao giờ huấn luyện [CTX]. Giấy phép OpenViIC cấm phân phối lại: tài liệu này và 13 báo cáo lưu kèm không chứa caption OpenViIC (quét 8-gram, §10).
- **Nhìn test nhiều lần:** C3, C4, C5 dùng pool mẫu test ("chỉ để báo cáo cuối") để ước lượng với luật đóng băng từ dev; không chọn gì trên test, nhưng số lần nhìn tăng [C3 §7; C4 §10; C5 §7]. Claim cuối phải đến từ run đã đăng ký trước.

## 8. Những độ đo có thể vượt 90 một cách trung thực
**POPE / RePOPE trên COCO val2014** (500 ảnh; F1, nhãn POPE / nhãn RePOPE; đo) [POPE]:

| Hệ | Ngôn ngữ | random | popular | adversarial |
|---|---|---|---|---|
| zero-shot | VI | 82.5 / 89.1 | 81.1 / 86.5 | 80.7 / 86.4 |
| zero-shot | EN | 86.5 / 92.3 | 85.6 / 90.4 | 84.7 / 89.9 |
| P1 s43 | VI | 88.2 / 92.4 | 84.9 / 88.9 | 84.0 / 88.1 |
| P1 s43 | EN | 83.8 / 90.9 | 82.9 / 89.1 | 82.5 / 89.2 |
| fuse2 s42 | VI | 84.4 / 91.0 | 82.4 / 88.5 | 81.9 / 88.4 |
| fuse2 s42 | EN | 83.4 / 90.8 | 82.7 / 89.1 | 82.4 / 89.3 |

- n = 3,000 câu hỏi mỗi split với nhãn POPE; 2,774 / 2,727 / 2,684 với nhãn RePOPE (bỏ câu mơ hồ); 0 câu không parse được [POPE].
- Vượt 90 trung thực: RePOPE split random ở 5/6 cặp hệ–ngôn ngữ (trừ zero-shot VI 89.1), và RePOPE popular của zero-shot EN (90.4). Với nhãn POPE gốc, không ô nào đạt 90 (cao nhất 88.2). Trung bình 3 split, RePOPE: zero-shot EN 90.9; VI: P1 89.8, fuse2 89.3, zero-shot 87.3 (đo) [C8 P4].
- Precision của câu trả lời "có" rất cao: 86.3–99.5 với nhãn POPE (đo) [POPE]; ở split random "có" đúng 96–99% (đo) [C3 §2i].
- SFT tiếng Việt nâng POPE-VI vì zero-shot trả lời "không" quá nhiều bằng tiếng Việt: tỉ lệ "có" của P1 VI 42.7–47.4% so với zero-shot VI 36.0–37.9% (đo) [POPE]; khoảng phạt tiếng Việt −4.2 F1 của zero-shot được SFT xóa (đo) [C8 P4].
- Mốc ngoài: RePOPE mean F1 tốt nhất 94.2 (Ovis2-4B) (đo, tài liệu) [C8 P4]; headroom tồn tại thật dưới nhãn đã sửa khoảng +3 F1 (ước tính) [C8 P4].

**Các P trung thực khác ≥ 90 (chỉ precision).**
- COCO, caption short so với gold instance: P 89.5–90.9 (đo) [CTX]; so với gold instance + tham chiếu (giao thức Rohrbach): P1-short 93.3, fuse2-short 94.5 (đo) [C3 §2g]. Veto theo phiếu [MH] đưa P lên 91.4 / 92.2 với F1 ±0 (đo) [C3 §2g].
- KTVIC, so với hợp hai panel người (KTVIC ∪ OpenViIC, 7.05 lớp/ảnh): P của p1_s43-short 90.7, p1_s43-detailed 91.4, fuse2-short 89.1; một người 94.05 (đo) [SP]. Recall theo gold lớn hơn này chỉ còn khoảng 25–29, nên đây là số precision, không phải F1.

**Vì sao đây là câu hỏi khác với F1 object của caption.**
1. POPE đưa sẵn tên object trong câu hỏi; mô hình chỉ xác nhận có mặt. Caption F1 đòi mô hình tự chọn nêu gì, và chấm theo cái người chú thích đã chọn (KTVIC) hay mọi instance (COCO) [C7 §2f; C5 §0].
2. Lỗi POPE của ta là bỏ sót, không phải bịa: "có" đúng 96–99% [C3 §2i]. Thấy 67 / 88 / 96% nhưng nói 7 / 24 / 56% theo cỡ object (§5a) [C7]. POPE cao chứng minh nhận thức không phải nút cổ chai; nó không thay được F1 của caption.
3. Nhãn POPE có nhiễu (trần khoảng 94) và ảnh val2014 có cùng rủi ro nhiễm COCO-2017 như probe (§7) [C10 §2e; C2 §6; C8 §7].
4. Cách báo: POPE/RePOPE là một dòng "độ đo chuẩn để so", tách khỏi dòng caption, đúng như C10 R4 [C10 §5]; không bao giờ đặt cạnh CIDEr của caption như thể là F1 object của caption.

## 9. Quyết định của judge (D10) và quyết định của người dùng (U-001)

Phán quyết D10 (13/10/2026) xét 6 mục `(i)`–`(vi)` về kết luận R9 và danh mục GPU; quy tắc giao thức đòi từ 80% trở lên mới thực thi, dưới 80% phải hỏi người dùng. Hai mục ở mức 78% — VGR `(iii)` và đối chứng độ phân giải KTVIC 2,048 token `(iv)(c)` — đã được người dùng quyết định tại U-001 (13/10/2026) [D10].

### 9a. Phán quyết, độ tin cậy và lý do theo từng mục `(i)`–`(vi)`
- **`(i)` Chấp nhận kết luận R9: YES (93%).** Judge tự kiểm lại các trần đo được: trên KTVIC, một người so với 4 người còn lại (1v4) đạt P/R/F1 `85.33 / 46.90 / 60.50` (`data/results/human_parity.json`), và P ≥ 90 chỉ tồn tại ở R `16.4–21.9` [C3]; trên COCO, 5 tham chiếu người gộp so với instance gold đạt `85.3 / 74.3 / 79.5` với `37.2%` lớp instance không người nào gọi (`C10 dl/human_union.out`; C6 tái tạo `85.0 / 74.4 / 79.4` trên 2,441 ảnh). Mọi con đường vượt 90 đều là inventory trả giá CIDEr lớn (C4: KTVIC F1 93.2 làm CIDEr sụp `143.9 → 95.2`; C6: COCO F1 90.4 làm CIDEr-D sụp `88.6 → 56.3` EN và `179.7 → 52.6` VI). Mục tiêu của bài báo được phát biểu theo các trần đo được và mốc so sánh của C10 (caption object F1 công bố cao nhất là 79.7; mức tăng được nhận là F1 `+1.2..+1.8`, CHAIR `−1..−2`, recall `+3..+4` khi CHAIR không xấu đi); các đường inventory và nối danh sách chỉ xuất hiện như baseline gaming.
- **`(ii)` Pilot PLAN-F1 trên dev300, sửa đổi `(a)`–`(d)`, phân bổ máy: YES cho pilot dev300 theo đúng đặc tả C5-M1 kèm K1–K3 (85%); `(a)` NO (85%); `(b)` NO (85%); `(c)` NO cho pilot — chỉ làm ablation sau pilot (80%); `(d)` NO dưới dạng gộp vào realiser, YES cho giao thức báo cáo hai đầu ra của C9 ở 0 GPU trên các dự đoán sẵn có (80%).**
  - *Lý do duyệt PLAN-F1:* là đòn duy nhất có kế hoạch vượt đường biên chọn mẫu trên dev (cross-fit, chặn 3 ở T = 0.8: `+3.7 [+1.5, +5.8]` so với greedy và `+1.3 [−0.5, +3.2] / +2.4 / +2.1` so với UPE [C5 §3c, p16]), tốn 5–6 GPU-h và có cổng kill rõ.
  - *Lý do bác `(a)`–`(d)`:* chi tiết tại §6c — `(a)` copy-guard huấn luyện realiser bỏ lớp trong danh sách (ngược với K1 ≥ 85%), trong khi lỗi kế hoạch chủ yếu là object thật mà người chú thích không nêu (panel OpenViIC xác nhận 56.5% FP của P1 [C3]); `(b)` FOPR veto ở `q < F/2 = 0.27–0.29` trên cùng hậu nghiệm đã lọc ở `P* = 0.61–0.66`, chỉ bỏ bin 0 phiếu (~3% mention, F1 +0.0) và tạo thêm forking path; `(c)` probe có mặt nhắm vào lỗi thiểu số, ngang veto theo phiếu (C3/R6), và ứng viên kế hoạch lấy từ mẫu của chính mô hình nên mô hình đã "thấy"; `(d)` PCD-GAFS cần SFT fuse-k riêng (4–6 GPU-h) và luật dừng riêng, còn giao thức báo cáo hai đầu ra của C9 §4 miễn phí ở 0 GPU.
  - *Phân bổ máy:* chạy trên máy đang chạy hàng đợi D9 ở slot trống kế tiếp sau khi commit prereg, không phá thứ tự D9 (`52_c` sau `52_a` và `52_b`); các file pool dev (`36_z` mẫu T0.5/T0.8 và `rl/g0/dev300.jsonl`) nhỏ nên chép từ máy đang chạy `35_e` sang, còn realiser huấn luyện từ mô hình gốc; những giờ kế tiếp của máy đang chạy `35_e` dành cho `35_e` và nhánh tiếp theo do cổng của nó chỉ định. Bước test chỉ chạy sau khi qua cổng dev.
- **`(iii)` Nhánh COCO (xếp hạng, duyệt tối đa hai): 1. C8 S0 Qwen3-VL-8B: YES, chạy ngay (88%); 2. C6 VGR: YES theo giai đoạn — baseline WiSE-FT trước kèm luật vô ích (78%, dưới ngưỡng 80%); 3. C4 P-B: YES-nhưng-để-sau, không trước phán quyết `35_e` nên chưa duyệt lúc này (85%); 4. UGZ: NO (87%).**
  - *Lý do:* S0 chỉ tốn 2.5 GPU-h suy luận, có cổng PASS/KILL tiền đăng ký, không có đường gaming, quyết định câu hỏi backbone và slot backbone thứ hai; VGR chỉ dùng nhãn người, đánh vào khoảng quên từ vựng đo được (zero-shot short F1 `63.4 → P1/fuse2 59.3–59.4`; detailed `73.3 → 65.7` [C6 §1.3]) với trần `+5.45` và phải thắng baseline WiSE-FT; P-B có kỳ vọng COCO lớn nhất (`+4..+7`) kèm neo CIDEr nhưng chạy trên engine CN-RLOO đang có lượt nhìn đầu tiên (`35_e`); UGZ có phần zoom mới chỉ `≤ +1` F1 (dễ chạm kill 1), phần hoàn thiện nối mệnh đề cố định trên COCO rơi vào mục gaming (c) của C9 §4 không có cổng CIDEr, còn phần KTVIC trùng PLAN-F1 và UPE (§6b).
- **`(iv)` Sửa đo lường: `(a)` Chuẩn hóa dấu thanh: YES (90%); `(b)` CJK: NO giải mã lại, YES thêm cột tỉ lệ CJK ở 0 GPU kèm một dòng độ nhạy (82%); `(c)` Độ phân giải: YES chỉ cho phần KTVIC 2,048 token (~1 GPU-h, ưu tiên thấp), NO cho COCO 2× và POPE 2× (78%, dưới ngưỡng 80%).** Lý do và số liệu judge kiểm: xem chi tiết tại §7 (cùng mục kiểm riêng loại từ `"cây"` trong `"cây cầu"` 7 / 11 / 15 lần chưa được duyệt sửa).
- **`(v)` Hoãn C4 P-A tới sau phán quyết cổng `35_e`: YES (92%).** Đối chứng của P-A chính là `35_e`; khởi động P-A trước khi có phán quyết cổng sẽ tạo lượt nhìn thứ hai trên engine chưa được chứng minh.
- **`(vi)` Hàng đợi các job cũ (85%) và phụ lục loss mask / chồng lấp ảnh (88%):**
  - *Thứ tự toàn cục (GPU nào trống trước lấy job kế tiếp đã có đủ input):* **P0 (đang chạy):** máy chạy `35_e` hoàn tất `35_e_rl_cn_v3` và nhánh tiếp theo theo cổng v2; máy chạy hàng đợi D9 chạy `50_f → 52_a → 52_b → 52_c` theo đúng thứ tự D9. **P1 (R9):** pilot dev PLAN-F1 trên máy chạy hàng đợi D9 ở slot trống kế tiếp sau khi commit prereg (có thể trước `52_a` hoặc giữa `52_a` và `52_b`); C8 S0 trên máy chạy `35_e` sau `35_e` và nhánh tiếp theo của nó, trong một venv riêng. **P2 (giữ, đã tiền đăng ký, đủ input):** `56_p1_4ep_s42` (~4.5 GPU-h, đối chứng cân bằng compute cho claim fusion `[PRE]` D2, chạy đầu tiên trong nhóm cũ); `39_xm3600_eval` (~2.7 GPU-h, tiêu chí OOD đã đăng ký ở R5_00 §7 với nhãn OIV7 người kiểm); các job bậc thang `[PRE]` (1b5d16b) trên legacy mask: `55_ladder_cons_s42` (2.6), `40_multiref_s42` (5.3; trước khi chạy phải thêm `set -e`, timeout đánh giá và kiểm đầu ra như 41/42, giữ nguyên tham số huấn luyện), `41_ladder_rnd2_s42` (4.5), `42_ladder_unf2_s42` (4.6); và `52_b` theo thứ tự D9 (G3'b). **P3:** VGR (bước 0 WiSE-FT, rồi seed 42 trừ khi vô ích); đối chứng độ phân giải KTVIC 2,048 token (~1 GPU-h); `57/58` hoặc C8 G1 tùy kết quả S0. **P4 (đẩy xuống cuối, mô tả, không cổng):** `39_b_parallel_zeroshot` (5.9), `53_a` (4.8), `53_b` (7.3), `53_c` (5.0; sạch theo kiểm tra ID), `39_z` (1.0; bỏ các tập của `39_y` khỏi input). **PARK (cuối cùng, chỉ chạy nếu GPU rảnh):** `60–63 xfit` (11.6 GPU-h; prior thấp vì E5 RFT âm — short F1 57.3 so với 58.1, CIDEr 137.9 so với 143.9 — và VTF ≈ 0). **DROP (bỏ hẳn):** `90_pilot_resume` (không gác cổng nào, R5_00 §7 khuyên bỏ) và `39_y_coco_zeroshot` (10.3 GPU-h, không gác cổng nào; nửa tiếng Việt không có tham chiếu và trùng với output COCO-probe zero-shot sẵn có; câu hỏi ngôn ngữ được trả lời trên UIT-ViIC và XM3600 nơi cả hai ngôn ngữ đều có tham chiếu người).
  - *Phụ lục loss mask và độ sạch dữ liệu (88%):* `52_a`/`52_b` giữ nguyên legacy mask (không sửa trước khi chạy) đúng như prereg D9 đã commit (257bc8c, dòng 234) vì phép đối chiếu G3' lặp lại (fuse2 so với P1) là legacy so với legacy và `53_a`/`53_b` dùng lại siêu tham số của `52_a`; mọi dòng UIT-ViIC đặt cạnh dòng KTVIC response-only phải gắn chú thích *"legacy loss mask, matching the KTVIC fuse2-vs-P1 contrast"* và không bao giờ tính độ lệch chéo giữa hai loại mask. Đồng ý `53_c` sạch (`coco_vi` và UIT-ViIC train chung 0 ảnh). Về 59 ảnh manifest trong UIT-ViIC train: phải loại bỏ khi chạy P-B (C6 khuyên bỏ cả 133 ảnh Karpathy test cho sạch) và khi chấm bất kỳ adapter nào có huấn luyện UIT-ViIC trên probe 2,500 ảnh; pool của VGR đã loại Karpathy test ngay từ cách xây dựng.
- **Quyết định của người dùng cho hai mục 78% dưới ngưỡng 80% (U-001):** (1) **VGR `(iii)`:** chỉ chạy **bước 0 WiSE-FT** trước (thu nhỏ LoRA của `fuse2_s42` ở α ∈ {0.5, 0.75}, chọn α trên UIT-ViIC val, ưu tiên P3, viết prereg trước khi chạy); việc có chạy SFT của VGR hay không sẽ quyết sau khi có kết quả WiSE-FT; (2) **Đối chứng độ phân giải KTVIC 2,048 token `(iv)(c)`:** **duyệt chạy** ở ưu tiên thấp (~1 GPU-h).

### 9b. Yêu cầu nâng độ tin cậy, điều kiện ràng buộc và rủi ro chính
- **Để nâng độ tin cậy (trước khi chạy/giải mã):**
  - `(ii)` Commit prereg PLAN-F1 qua gatekeeper trước mọi lần giải mã realiser, chốt: bộ hiệu chỉnh cross-fit (số fold, seed; đặc trưng = tỉ lệ phiếu theo lớp trên 12 mẫu T0.5/T0.8, cờ greedy, prior lớp trên train-trừ-dev300); luật plug-in chặn 3 kèm định dạng danh sách và thứ tự lớp; realiser = công thức `P1_dev` (train trừ dev300, `--loss-mask assistant`, seed 42, cùng số epoch và LR); nguyên văn K1–K3, luật test và các báo cáo bắt buộc; self-check của script dựng dữ liệu phải `assert` mọi danh sách huấn luyện bằng `objects_in(target)`.
  - `(iii)` Prereg S0: ghim revision mô hình, sha256 trọng số, danh sách ID tập con val2017 và đường dẫn venv riêng.
  - `(iv)(a)` Prereg sửa dấu thanh: `assert objects_in('một tòa nhà') == objects_in('một toà nhà')` và liệt kê mọi mục lexicon bị chạm (mục kiểm `"cây"` trong `"cây cầu"` tách riêng, chưa duyệt sửa).
- **Điều kiện ràng buộc (Binding conditions):**
  - `(ii)` *PLAN-F1:* cạnh mọi F1 phải báo: P, R và số mention/caption; KTVIC `CHAIR_i`; precision mở rộng bằng panel OpenViIC (chỉ đánh giá, không bao giờ huấn luyện); CIDEr-D, BLEU-4, METEOR, ROUGE-L; và phần dư so với đường biên ở cùng số lượng object (đường cong C9 — nếu CI chứa 0 thì gọi mức tăng là điểm vận hành suy từ độ đo, không phải xếp hạng tốt hơn). Tín hiệu phiếu lấy từ mẫu mô hình `[MH]` (gắn cờ như D9), nhãn là nhãn người (tham chiếu train của dev300, không dùng nhãn AI). Test đúng một lần, đóng băng, sau khi qua cổng dev: 12 mẫu test + greedy của `P1_dev` (~1.1 GPU-h trên máy giữ adapter `P1_dev`) và một lần giải mã realiser; báo âm nếu test `dF1 < +2` hoặc `CIDEr < greedy − 8`. Không tuyên bố "đầu tiên" (*no "first" claims*).
  - `(iii)` *S0:* báo PASS/KILL như C8 tiền đăng ký, tỉ lệ câu tiếng Việt, tỉ lệ CJK và các độ lệch trên tập con val2017; nếu S0 qua, G1 của C8 (~4.2 GPU-h) thay `57/58` làm phép kiểm backbone thứ hai (G4); nếu trượt, chạy `57/58` như kế hoạch và khai báo giấy phép `qwen-research`. *VGR:* tiền đăng ký trước mọi output; bước 0 chạy WiSE-FT trên `fuse2_s42` ở α ∈ {0.5, 0.75} (chọn α trên UIT-ViIC val); bỏ qua SFT của VGR nếu điểm WiSE-FT đã chọn tăng `≥ +3.5` short instance F1 so với `fuse2` trên UIT-ViIC val ở KTVIC short CIDEr `≥ 140.7` (vì trần `+5.45` khi đó chỉ chừa `< +2`), ngược lại chạy seed 42 với K1–K4 của C6 (sau khi có quyết định tiếp theo theo U-001); nếu `35_e` qua cổng trước khi VGR bắt đầu, điều phối viên có thể trình lại P-B vào slot này (mỗi thời điểm một nhánh huấn luyện COCO); pool rehearsal loại Karpathy test và val ngay từ cách xây dựng.
  - `(iv)` *Dấu thanh, CJK, độ phân giải:* như đã nêu tại §7.
- **Rủi ro chính (Risks):**
  - *PLAN-F1:* có thể trượt K2 sau hao hụt độ trung thành vì biên kế hoạch mỏng (`+3.7` so với ngưỡng `+3.0`; `+1.3..+2.4` so với ngưỡng `+1.0` trước UPE); theo thiết kế nó đổi precision lấy recall (plan P giảm 5–12 điểm so với greedy) nên KTVIC `CHAIR_i` tăng — đây là thoái lui trên độ đo chính trừ khi panel thứ hai chứng minh các object thêm vào là thật; vòng R9 đã nhìn pool mẫu test cho 4 luật × 2 hệ ở mức mô tả (C5 §3c), nên bản giải mã realiser trên test là lượt nhìn khẳng định duy nhất và lịch sử này phải được khai báo.
  - *Nhiễm dữ liệu và môi trường ở S0:* khoảng 88% ảnh probe Karpathy test nằm trong COCO-2017 train (dữ liệu grounding của Qwen3-VL nhiều khả năng đã phủ) và tập kiểm val2017 chỉ có khoảng 300 ảnh; Qwen3-VL đòi `transformers >= 4.57` trong khi `.venv` trên máy chạy `35_e` đang ở `4.51.3` — bắt buộc dùng venv riêng, tuyệt đối không nâng cấp venv đang chạy.
  - *Phẫu thuật hàng đợi sống:* đổi tên file sai lúc trên hàng đợi chạy theo thứ tự tên file có thể khởi động nhầm job hoặc phá thứ tự D9 (`52_c` sau `52_a` và `52_b`); mọi job bậc thang `[PRE]` không chạy phải được báo rõ là không chạy.

## 10. Nguồn
**Báo cáo R9** (lưu trong repo, `manuscript/research_r9/`): `C1_ceiling/REPORT.txt` (trần đo được), `C2_detect_tags/REPORT.txt` (detector, tag), `C3_halluc_decode/REPORT.txt` (precision, giảm ảo giác), `C4_rl_object/REPORT.txt` (RL theo object), `C5_decision_f1/REPORT.txt` (lý thuyết quyết định), `C6_multitask_data/REPORT.txt` (dữ liệu, đa nhiệm), `C7_resolution/REPORT.txt` (độ phân giải, zoom), `C8_backbone/REPORT.txt` (backbone), `C9_dense_format/REPORT.txt` (định dạng, độ dài), `C10_standards/REPORT.txt` (chuẩn venue).

**Báo cáo R8** (lưu trong repo, `manuscript/research_r8/`): `T1_decode/REPORT.txt` (CC-ADD), `T2_train/REPORT.txt` (mục tiêu huấn luyện), `T3_theory/REPORT.txt` (UPE-MBR).

**Không lưu vào repo:** `CONTEXT_R9.md` và `CONTEXT_R8.md` chứa thông tin truy cập máy (dòng ssh), nên bị giữ lại; bản gốc nằm trong scratchpad của phiên. Mọi file được quét trước khi chép: không file nào trong 13 file đã lưu có 8-gram từ của caption OpenViIC (sau khi viết thường, chuẩn hóa khoảng trắng) hay chuỗi bí mật.

**File kết quả:** `data/results/pope_vi/scores.txt` và `scores.json`; `data/results/upe/upe_choose_t.json`; `data/results/second_panel.json`; `manuscript/prereg/2026-10-13_upe_mbr.md`.

**Tài liệu then chốt (id arXiv; venue theo báo cáo):**
- Phân loại đa nhãn COCO: Query2Label 2107.10834; ML-Decoder 2111.12933 (WACV 2023); ASL 2009.14119 (ICCV 2021); ML-GCN 1904.03582 (CVPR 2019); C-Tran 2011.14027; CSRA 2108.02456; ADDS 2208.09562; RAM 2306.03514; RAM++ 2310.15200; Tag2Text 2303.05657 (ICLR 2024).
- Detector và tag trong captioning: Grounding DINO 2303.05499; MARINE 2402.08680; HALC 2403.00425; Woodpecker 2310.16045; LURE 2310.00754; HallE-Control 2310.01779; TUNA 2406.10839; ViECap 2307.16525; CBS 1612.00576; nocaps 1812.08658; PS3 1806.06004; Misra 1512.06974.
- Giảm ảo giác khi giải mã: VCD 2311.16922; OPERA 2311.17911; PAI 2407.21771; SelfVal 2601.22451; VGD 2607.27823; TLC 2305.07021; SelfCheckGPT 2303.08896; RePOPE 2504.15707; AMBER 2311.07397.
- Reward theo object: PS-NOC 2109.05115; SC-Captioner 2508.06125; ECOL-R 2101.09865; BalCapRL 2605.07394; SPIDEr 1612.00370; Perception-R1 2504.07954; Visual-RFT 2503.01785; CHAIR-DPO 2508.20181; CHAIR 1809.02156.
- Lý thuyết quyết định cho F: Lipton 1402.1892; Ye 1206.4625; Fang 1411.4952; Manas 2508.11616; PatchGate 2608.21819; CommonGen 1911.03705; Atomic Self-Consistency 2405.13131; conformal factuality 2402.10978.
- Dữ liệu và quên: NOC 1606.07770; VIVO 2009.13682; SSR 2403.01244; SDFT 2402.13669; ReDraft 2609.16639; HalluciDoctor 2311.13614; WiSE-FT 2109.01903.
- Độ phân giải và zoom: S² 2403.13043; ViCrop 2502.17422; DyFo 2504.14920; CAPTURE 2405.19092; ZoomEye 2411.16044; V* 2312.14135.
- Backbone: Qwen2.5-VL 2502.13923; Qwen3-VL 2511.21631; InternVL3.5 2508.18265; VISE 2606.27373; Vintern-1B 2408.12480.
- Định dạng và độ dài: LaBERT 2007.09580; CaptionSmiths 2507.01409; Less is More 2402.14545; Florence-2 2311.06242; CompreCap 2412.08614; DCScore/FeedQuill 2503.07906; CCCaption 2602.21655.
- Chuẩn venue: Attention Reallocation 2503.08342 (IJCV 2025); MemVR 2410.03577 (ICML 2025); CLVA 2603.25088 (PR 2026); SENTINEL 2507.12455 (ICCV 2025).
