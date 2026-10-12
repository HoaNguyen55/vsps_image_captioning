# R6-00: Phương pháp của vòng R6 — CN-RLOO + C-MBR (chưa đạt mức novelty "đột phá")

13/10/2026, nhánh `paper-v10`, HEAD `67b9b6e`. Tổng hợp 14 đề xuất của 7 nhóm đòn bẩy (B1–B7) sau phản biện đối kháng, cộng các phép đo mới của file này (§1c). Đường dẫn `research_r6/…` nằm dưới `/tmp/claude-1000/-mnt-d-vsps-image-captioning/755eae04-5e4c-4ce1-ab21-d4bc106761ee/scratchpad/research_r6/`. Code và số của file này: `research_r6/S0_synthesis/` (`dev_mbr.py`, `frag_check.py`, `uitviic_karpathy_overlap.py`, `out/`). Chỉ dùng dữ liệu và caption người đã công bố. Không gán nhãn mới, không dùng nhãn AI.

**Cách đọc**
- Số KTVIC tính trên preds hay mẫu của **test** là ước lượng cỡ hiệu ứng, không phải kết quả. Không luật nào được chọn trên test.
- **dev300** là 300 ảnh KTVIC TRAIN giữ ngoài huấn luyện (`data/splits/ktvic_dev300.txt`). Số trên dev300 là phép đo hợp lệ để tinh chỉnh.
- Thang ×100, CIDEr-D mức từ (RDRSegmenter), như `data/results/*.json`. CI 95%, bootstrap cặp theo ảnh, B = 2000.
- Mỗi run vừa một RTX 3090, QLoRA 4-bit, mô hình mở [CTX].
- Ngưỡng cũ (khoảng cách vi/en 5%) đã bỏ [CTX]. Mục tiêu là số cao nhất đạt được. Thanh "đột phá" của [CTX]: +8 CIDEr so với trung bình 3 seed của P1 (145.8 → 153.8) mà CHAIR_i không tệ hơn, hoặc CIDEr ≥ P1 với CHAIR_i thấp hơn ít nhất 4 điểm. Phải lặp lại trên UIT-ViIC, và trên COCO nếu phương pháp không phụ thuộc ngôn ngữ.

**Nguồn (viết tắt)**
- [CTX] `research_r6/CONTEXT_R6.md`. [B1]…[B7], [N1]: `research_r6/<nhóm>/REPORT.txt`. [V:x]: `research_r6/verify/x.txt`.
- [G0] `n2:/root/ncs-data/rl/g0/g0_report.json`, ghi lúc 19:20 UTC 12/10 (bản sao `S0_synthesis/g0/g0_report.json`, md5 `ad64431b…`).
- [C3] `n2:/root/ncs-data/rl/dryrun_cn_s42/c3.json` và `summary.json`, 19:25 UTC 12/10 (bản sao `S0_synthesis/g0/c3.json`).
- [DEV] `S0_synthesis/out/dev_mbr.json` và `dev_mbr.log` (`dev_mbr.py`). [FRAG] `S0_synthesis/out/frag_check.log`. [OVL] `S0_synthesis/out/uitviic_karpathy_overlap.log` và `coco_en_overlap.log`.
- [R4-00] `manuscript/novel_direction/R4_00_DE_XUAT_NOVELTY.md`. [R5-00] `…/R5_00_KE_HOACH_BAI.md`. [R5-01] `…/R5_01_SECOND_PANEL.md`.
- [PRE-V4] `manuscript/prereg/2026-10-12_frontier_invariance_V4.txt`. [PRE-VI] `manuscript/prereg/2026-10-12_vietnamese_diagnostics/PREDICTIONS.md`.

## 1. Tóm tắt

### 1a. Phương pháp đề xuất: CN-RLOO → C-MBR

Hai tầng, một mục tiêu: caption khớp tâm n-gram của panel tham chiếu.

1. **Huấn luyện (1 lần giải mã/ảnh): CN-RLOO.**
   - Xuất phát từ P1-assist: SFT trên caption đầu, loss chỉ trên câu trả lời.
   - Mỗi ảnh lấy k = 8 rollout ở T = 1.0. Phần thưởng là CIDEr-D mức từ, có token EOS (SacreEOS), DF cố định từ ref train.
   - Advantage RLOO, không chuẩn hoá std. KL k3 về adapter SFT.
   - Hai lớp chặn. (a) **Mặt nạ CN**: rollout gần chép một ref (m ≥ τ = 0.90 [G0]) có advantage 0. (b) **Chặn mảnh câu** (thêm theo [V:B1-P1]): rollout kết thúc bằng một từ chưa từng đứng cuối ref train nào có advantage ≤ 0.
   - Code đã có ở HEAD: `scripts/train_rl.py`, `rl_reward.py`, `rl_report.py` (commit b71a288, 607276a).
2. **Giải mã (N lần giải mã/ảnh): C-MBR.**
   - Committee 6 adapter: 3 seed CN-RLOO và 3 seed P1-assist mà chúng xuất phát.
   - Ứng viên là caption greedy của từng adapter. Bằng chứng là greedy của các adapter khác cộng 6 mẫu của mỗi adapter ở T\* (chọn trên dev).
   - Chọn ứng viên có CIDEr-D trung bình cao nhất với bằng chứng. Đây là luật đóng băng của [B3], không có tham số.
   - Biến thể "tối đa KTVIC": thêm ref của k\* ảnh train truy hồi theo caption greedy [B4]. Biến thể này đo **tính điển hình** (typicality) và phải ghi nhãn như vậy.

**Lõi mới duy nhất là mặt nạ CN, và nó chỉ incremental.** Cơ chế "đưa điểm của một detector vào advantage để chặn một lớp rollout" đã có (2604.01476; DAPO 2503.14476) [V:B1-P1]. Mọi phần khác là thành phần đã biết: SCST/RLOO, SacreEOS, MBR committee (ECO 2405.01028; Eikema & Aziz 2108.04718), MBR có truy hồi (MBR-CBDT 2509.12677). Dữ liệu G0 mới (§1c, F1) làm lõi này yếu thêm. **Vòng R6 không tìm được phương pháp đạt mức novelty "đột phá" mà tác giả yêu cầu** (§1d, §3).

### 1b. Dự báo so với trung bình 3 seed của P1

Mốc: P1 legacy s42/s43/s44, short: CIDEr 145.8, B-4 45.2, METEOR 39.1, ROUGE-L 64.0, CHAIR_i 18.4 [CTX]. Các ô là chênh lệch so với mốc.

| Hệ | Giải mã/ảnh | ΔCIDEr | ΔB-4 | ΔMETEOR | ΔROUGE-L | ΔCHAIR_i | Bằng chứng |
|---|---|---|---|---|---|---|---|
| (a) CN-RLOO, greedy, trung bình 3 seed | 1 | +2 đến +7 (tâm +4) | +1 đến +3 | −0.5 đến +1 | +0.5 đến +2 | −1 đến +2 | +2 đến +6 so với P1 khớp mask [V:B1-P1]; mask thêm +0.99 [−3.44, +5.17], n.s. [CTX]. Bước RL 1 nat, trung bình 4 cách chia ref: +2.6 (P1), +6.4 (fuse2) [V:B1-P1]. SCST trên COCO với CE ≥ 130: +6.1 đến +14.1, trung vị +8.5; Flickr8k (6K ảnh): +2.4 SCST, +4.1 GRPO [B1 §1b] |
| (b) C-MBR trên 4–5 adapter SFT, không RL (đã đo trên test) | 16–17 | +7.5 đến +11.9 | +1.3 đến +1.7 | +0.7 đến +1.0 | +1.4 đến +1.7 | −0.8 đến −1.1 (CI chạm 0) | Chỉ seed P1: +7.54 [4.60, 10.66]; thành viên B3 chưa thấy: +8.40 [4.54, 12.17]; gần cấu hình chính: +11.91 [7.95, 16.16] [V:B3-P1]. Panel độc lập: +1.82 đến +3.66 [V:B3-P1] |
| (c) **S\* = C-MBR trên 3 CN-RLOO + 3 P1-assist** (dự báo) | 42 | +6 đến +12 (tâm ≈ +9) | +1.5 đến +3.5 | +0.5 đến +1.5 | +1.5 đến +3 | −2 đến +1 | Sàn ≈ hàng (b) nếu thành viên RL không kém thành viên SFT. Trên thành viên đã RL, MBR được dự báo chỉ thêm +1 đến +3, vì cả hai cùng tối ưu CIDEr [V:B3-P1]. **Chưa đo** |
| (d) S\* + ref truy hồi (tối đa KTVIC; typicality) | 42 | thêm +2 đến +4 | thêm +0.5 đến +1 | thêm 0 đến +0.5 | thêm +0.5 đến +1 | thêm −1 đến +1 | Committee 8 hệ: 157.5 → 160.7, trên panel −0.3 [B3 Bảng A, F]. Dev, 1 adapter, T = 1.0: +4.2 [+1.0, +8.0] so với greedy, trên panel +0.27 [−0.79, +1.47] [DEV] |

Xác suất đạt thanh +8 với CHAIR_i không tệ hơn (đánh giá của file này, từ các khoảng trên):
- (a) một mình: 10–15% [V:B1-P1].
- (c) S\*: khoảng 50% so với mốc 145.8. Khoảng 30% so với trung bình 3 seed P1-assist, vì so với p1assist_s42 (148.7) committee chỉ thêm +5.5 đến +9.1 [V:B3-P1].
- Đường Pareto (CHAIR_i −4 ở CIDEr ≥ P1): khó. Veto phiếu cắt CHAIR_i −4.9 trên test nhưng mất 3.2 recall [V:P-B4-1]. Trên dev ở T = 1.0 nó mất 8.7–22.4 CIDEr [DEV].

### 1c. Đo mới trong file này (12–13/10)

- **F1. Kênh chép ở policy thật nhỏ, và phần lớn không phải học thuộc** [G0]. P1_dev, k = 8, T = 1.0.
  - 300 ảnh train mô hình đã học: rollout ở m ≥ τ chiếm 1.54% số rollout và 11.1% advantage RLOO dương. Bản chép nguyên văn: 0.67% và 6.0%.
  - 300 ảnh dev **chưa thấy**: 1.29% và 9.9%. Bản chép nguyên văn: 0.50% và 5.5%.
  - Advantage trung bình của rollout ở τ: +203.7 (train), +192.4 (dev); rollout khác: −3.2 và −2.5.
  - Vậy phần "học thuộc" chỉ thêm khoảng 1.2 điểm advantage share. Phần còn lại là caption trùng khuôn câu của ref, có cả trên ảnh chưa thấy. Mặt nạ CN chủ yếu xoá các rollout thưởng cao nhất trùng khuôn ref, không chủ yếu xoá rollout học thuộc. [V:P-B7-1 §D] thấy cùng chiều: chép nguyên văn ref của **ảnh khác** chiếm 1.83% rollout và 9.3% advantage dương, và CN không thấy kênh này.
- **F2. Dry run của G1 trượt cổng bộ nhớ C3** [C3].
  - Peak reserved 24.87 GB (allocated 21.76 GB), vượt mức 22 GB.
  - Các guard khác đạt: gap log-prob trung bình 0.012 (< 0.02), sampler = policy, reward = pycocoevalcap.
  - Tốc độ 10.1 s/ảnh ở k = 8, gần gấp đôi ước tính 4.5–6 s của [V:B1-P1].
  - Hàng đợi n2 đã chuyển sang `36_coco_b` (ps lúc 19:26 UTC). **G1 chưa chạy.** [V:B1-P1] đã dự báo 18–22 GB và chỉ cách sửa (§5b, C-R1).
- **F3. Rollout T = 1.0 là bằng chứng MBR kém. Tầng giải mã cần mẫu riêng ở T ≤ 0.8** [DEV]. Pool dev: greedy của evaluate.py (CIDEr 144.3, B-4 42.5, METEOR 37.5, ROUGE-L 62.3, CHAIR_i 23.3) cộng 8 rollout G0.
  - Mỗi rollout chỉ đạt 72.9–79.6 CIDEr.
  - Self-MBR trên 9 ứng viên: 139.6, −4.7 [−11.7, +2.6].
  - Thêm ref của 10 ảnh train truy hồi (chỉ mục = train trừ dev300): 148.5, **+4.2 [+1.0, +8.0]**. B-4 43.1, METEOR 37.7, ROUGE-L 62.6, CHAIR_i −0.6 [−2.1, +0.8]. Với k = 30: +1.9 [−2.1, +5.9].
  - Đối chứng ref của 10 ảnh ngẫu nhiên: −4.7 (bằng self-MBR). Vậy lợi là đặc thù theo ảnh.
  - Trên panel OpenViIC của cùng ảnh (296 ảnh), lợi chỉ +0.27 [−0.79, +1.47]. Đây là typicality.
  - Veto phiếu ở T = 1.0 mất 8.7 đến 22.4 CIDEr.
- **F4. Ở T = 1.0, phần thưởng KTVIC không còn chuyển sang panel độc lập** [DEV]. Chọn tốt nhất trong 9 theo ref KTVIC (oracle) được +44.7 [+38.5, +51.7] trên chính các ref đó, nhưng chỉ +0.07 [−3.66, +4.11] trên panel OpenViIC. Ở T = 0.8 trên test, cùng phép chọn được +5.6 [3.2, 8.1] (P1) và +4.5 [1.8, 7.3] (fuse2) trên panel [B1 §2.3]. Khác split và nhiệt độ, nên chỉ là tín hiệu. Rủi ro: RL ở T = 1.0 có thể chủ yếu học typicality của KTVIC. Panel là trọng tài (§2c).
- **F5. Giải mã trong run và evaluate.py khác nhau ở 55% caption** [DEV]. Cùng adapter P1_dev: greedy của `train_rl.greedy` (base NF4, batch có pad trái) và của `evaluate.py` (base bf16, từng ảnh) trùng nhau ở 45.0% ảnh dev, với CIDEr 144.4 [G0] và 144.3. Cổng phải dùng evaluate.py; số dev trong log RL chỉ để theo dõi. Báo thêm hàng `--four-bit`.
- **F6. Chặn mảnh câu đo được** [FRAG]. END = 1,158 từ đứng cuối ít nhất một trong 17,345 ref train-trừ-dev. Luật "từ cuối ∉ END" gắn cờ 3.0% greedy P1_dev trên dev, 2.3% greedy P1 s43 trên test, 13.8% rollout G0, và 36.6% caption test bị bỏ âm tiết cuối.
- **F7. Chồng lấn UIT-ViIC với Karpathy** [OVL]. UIT-ViIC train (2,695 ảnh) có 133 ảnh thuộc Karpathy test và 132 ảnh thuộc Karpathy val. UIT-ViIC val (924) và test (231) đều thuộc Karpathy train. Bộ `coco_en` test của repo (2,441 ảnh Karpathy test) không chứa ảnh nào của UIT-ViIC. Hàng chuyển sang COCO phải dùng bộ này, không dùng toàn bộ Karpathy test.

### 1d. Tác giả cần quyết

1. **Novelty.** Không đề xuất nào còn sống đạt mức "đột phá". Hai lựa chọn:
   - (i) bài "kết quả mạnh + recipe + phân tích", novelty incremental, venue như Neurocomputing [R4-00 §3];
   - (ii) mở vòng mới, nhắm phương pháp làm tăng điểm trên panel **độc lập**. Mọi đòn bẩy R6 chủ yếu tăng typicality của KTVIC (F3, F4; [B3] Bảng F; [V:P-B4-1]; [V:P-B7-1]).
2. **Cờ dữ liệu tổng hợp.** S\* không dùng target SFT do mô hình viết. Nhưng RL học từ rollout do chính policy sinh, chấm bằng ref người. [CTX] cho phép, nhưng tác giả có quyền phủ quyết (§7c).
3. **Ngân sách.** Lõi ≈ 54–103 GPU-h, tuỳ số ảnh RL chọn trên dev. Tối đa ≈ 170 GPU-h nếu mọi nhánh có điều kiện đều chạy (§5a). Ước tính 75 GPU-h của [V:B1-P1] dựa trên 4.5–6 s/ảnh; tốc độ đo được là 10.1 s/ảnh (F2).

## 2. Vì sao phương pháp này nên hiệu quả

### 2a. Chẩn đoán: metric đo tính điển hình của một panel

1. **CIDEr kỳ vọng là độ khớp với tâm n-gram của panel.** Bỏ clip và phạt độ dài, CIDEr(c, R) = (10/4) Σ_n ⟨g_n(c), ḡ_n(R)⟩ [B7 §2, T1]. Mọi đòn bẩy CIDEr hoặc ước lượng tâm tốt hơn (mẫu, committee, ref truy hồi), hoặc quyết định tốt hơn khi đã có ước lượng (MBR, RL).
2. **Ref đo typicality nhiều hơn sự thật.**
   - Với gold là hợp hai panel, khoảng P giữa fuse2 và P1 (detailed) co từ −10.4 [−13.0, −7.8] xuống −5.2 [−7.1, −3.2] [R5-01].
   - Chỉ 44.5% [42.0, 47.1] lớp do Grounding-DINO gắn tag được ít nhất một ref KTVIC nhắc [B4 §2].
   - Trên UIT-ViIC, với nhãn instance do người gán: 51.1% [50.3, 51.9] lớp có mặt được ref Việt nhắc, 64.9% [64.0, 65.6] được ref Anh của cùng ảnh nhắc [B4 §2].
3. **5 ref là một chuỗi diễn đạt lại, nên phần thưởng nhiễu.**
   - CIDEr-D giữa hai vị trí kề nhau 199–256, giữa hai vị trí không kề 134–162 [B2].
   - Độ tin cậy của phần thưởng 5 ref trong một nhóm rollout chỉ 0.55–0.60 [B1 §2.4].
   - Oracle best-of-7 được +57.3 [51.4, 63.8]. Chọn trên ref A và chấm trên ref B rời chỉ giữ +0.1 đến +15.0 [B1 §2.3].
4. **Bất biến đường biên: đổi target SFT không đổi được đường precision–số object.** CI của residual gộp trên 7 run là [−0.59, +1.07]. Chỉ tag lệch khỏi đường, +1.87 P, CI [−0.27, +3.90], chưa có ý nghĩa [PRE-V4 §4]. MR5 thật đạt 147.5, kém P1 khớp mask 1.2 CIDEr (1 seed) [CTX].
5. **Khoảng trống nằm ở chọn nội dung cụ thể, không ở bề mặt tiếng Việt.**
   - Một ref người so với 4 ref còn lại đạt 181.5 [173.7, 189.0]; P1 đạt 143.7–149.8 [B5 §5].
   - Mẫu thưởng cao thắng nhờ gọi đúng vật nổi bật cụ thể. Lặp từ (−40) và khuôn đệm (−60) bị phạt [B1 §2.7].
   - Chỉ sửa ngữ pháp tiếng Việt: oracle +26.5 [+23.7, +29.3]; chọn trên ref A, chấm trên ref B thì −5.4 [−8.1, −2.7] [N1 §3]. Phần này không học được.

### 2b. Kê đơn

- Target SFT không đẩy được đường biên (2a.4). Vậy đòn bẩy nằm ở **quyết định**: tối ưu trực tiếp CIDEr kỳ vọng dưới panel.
- Lúc huấn luyện, RL dùng cả 5 ref làm ước lượng tâm (2a.1). Ba lớp chặn khoá các kẽ hở đã đo: EOS cho cắt cụt [B1 §2.7]; END cho mảnh câu (F6); CN cho bản chép [B1 §2.8], dù F1 cho thấy kênh này nhỏ. KL giữ policy gần SFT. Pilot cho thấy cần khoảng 0.5–1 nat để mẫu vượt greedy [B1 §2.5].
- Lúc giải mã, nhiều seed và nhiều mẫu cho ước lượng tâm tốt hơn một caption greedy. MBR chọn caption đồng thuận. Phần này chuyển được sang panel độc lập: +3.0 [1.6, 4.5] [B3 Bảng F].
- Ref truy hồi của ảnh train lân cận chỉ thêm ước lượng **cùng panel**. Nó tăng KTVIC mà không tăng panel (F3; [B3]). Chỉ dùng cho hàng "tối đa KTVIC", ghi nhãn typicality.

### 2c. Kiểm chứng

1. **KTVIC test, 3 seed.** CN-RLOO so với P1-assist cùng seed, bootstrap cặp theo ảnh gộp 3 × 558. Đối chứng thêm MR5, cũng dùng cả 5 ref [V:B1-P1, đổi 3].
2. **Hai panel người.** Mọi lợi ích được báo cả trên panel UIT-OpenViIC độc lập (555 ảnh test; panel chỉ dùng để chấm). Phần không qua được panel ghi là typicality [R5-01; CTX].
3. **Sự thật bằng nhãn instance COCO.** UIT-ViIC test + val (1,155 ảnh, `data/uitviic/instance_gold.json`): CHAIR và P/R theo instance. Văn liệu cho thấy SCST làm **tăng** ảo giác (Rohrbach 1809.02156: TopDown CHAIR_i 6.1 → 8.8) [V:B1-P1], nên file này không dự báo CHAIR giảm.
4. **UIT-ViIC trong miền** (ref Việt, ảnh COCO; train 2,695, test 231). Cùng recipe, siêu tham số đóng băng từ KTVIC.
5. **Chéo ngôn ngữ.** Cùng ảnh UIT-ViIC với ref Anh (`uitviic_en`), rồi chuyển sang `coco_en` test (2,441 ảnh Karpathy test, sạch theo F7).
6. **Chẩn đoán tiếng Việt đã đăng ký trước** [PRE-VI]. RL − P1_dev trên dev được dự báo: "những" tăng, "một vài" giảm, "có" đầu câu giảm. Phụ: "người" trơn giảm, recall từ văn hoá tăng, "đang" giảm. Không gate gì.

### 2d. Điều sẽ bác bỏ câu chuyện

- G1 không vượt P1_dev +3.0 với cận dưới > 0 sau 3,469 ảnh (cổng R1): RL không phải đòn bẩy ở quy mô này.
- Lợi của S\* trên panel có CI chứa 0: lợi chỉ là typicality.
- CHAIR theo instance trên UIT-ViIC tăng có ý nghĩa: RL đổi CIDEr lấy ảo giác.
- CN không hơn RLOO thường: lõi mới biến mất. F1 cho thấy khả năng này cao.

## 3. Novelty: prior gần nhất và delta

| Thành phần | Prior gần nhất | Delta chính xác | Đánh giá |
|---|---|---|---|
| RL CIDEr-D cho LVLM QLoRA (RLOO, KL k3, EOS, mức từ) | SCST 1612.00563; Luo 2003.09971; RLOO 2402.14740; Dr. GRPO 2503.20783; SacreEOS 2305.12254; GRPO captioning 2503.01333; REINFORCE-CIDEr 2302.08242; SCST tiếng Việt ở VieCap4H/VLSP 2021 (2209.01304, 2211.05405) [V:B1-P1] | Qwen2.5-VL-7B QLoRA trên KTVIC; phần thưởng mức từ tiếng Việt | Ứng dụng. Không viết "SCST đầu tiên cho tiếng Việt". Chưa thấy RL-CIDEr cho LVLM 7B trên caption ngắn [B1 §1c] |
| **Mặt nạ CN** (lõi) | Advantage Modification 2604.01476; DAPO overlong filtering 2503.14476; PPO phạt giống văn bản train 2305.01550; Goldfish 2406.10209 (ở bước SFT) [V:B1-P1] | Detector chép n-gram/edit; ngưỡng = phân vị 99 trên ảnh chưa thấy | Incremental. Chỉ claim khi (a) share ở τ ≥ 10% trên ảnh đã học (**đạt**: 11.1% [G0]) **và** (b) CN hơn RLOO thường trên test, gộp ≥ 3 seed, cận dưới > 0. (b) khó: trên ảnh chưa thấy share đã là 9.9% (F1) |
| Chặn mảnh câu END | SacreEOS (chỉ chẩn đoán) | Từ cuối phải từng đứng cuối một ref train | Kỹ thuật, không claim |
| C-MBR (committee; mẫu chỉ làm bằng chứng) | ECO 2405.01028; Eikema & Aziz 2108.04718; UA-MBR 2503.05318; Farinhas 2310.11430; HESM 2306.05317; Devlin 1505.04467; m-RNN 1412.6632; IC3 2302.01328 [V:B3-P1] | Committee seed LoRA của một VLM tiếng Việt | Đã bị đi trước. Yếu tố "đa policy" của [B3] chỉ thêm +0.75 đến +1.87, mọi CI chứa 0 [V:B3-P1]. Dùng làm tầng giải mã và baseline mạnh. [R5-00] hàng 6 đã cấm claim "novel ensemble" |
| Ref truy hồi làm pseudo-ref MBR | MBR-CBDT 2509.12677 (có captioning); m-RNN §8; Devlin 2015 [V:P-B4-1] | Truy hồi theo caption greedy (TF-IDF), không theo ảnh | Incremental; lợi là typicality (F3) |
| Veto phiếu đối tượng | SelfVal 2601.22451; TLC-L 2305.07021 [V:P-B4-1; V:P-B4-2] | Ngưỡng phiếu trên mẫu, không cần nhãn | Incremental; là núm vặn CIDEr–CHAIR, không phải lợi miễn phí |
| Phân tích: biên RL, kênh chép, phân rã hai panel, bất biến đường biên, headroom tiếng Việt | Chen 2015 (1504.00325); Rohrbach 1809.02156; Kovacs 2411.03524 (thiên lệch khi utility là chính metric); Menon 2015 [PRE-V4 §5] | Đo trên LVLM tiếng Việt, có panel người độc lập trên cùng ảnh, đăng ký trước | Phần mới nhất mà bài có. Novelty trung bình–thấp |

**Kết luận novelty**
- Bài có thể claim: một recipe RL + MBR được đo kỹ cho LVLM QLoRA tiếng Việt; biên RL đo được (oracle +57, phần chuyển được nhỏ, kênh chép nhỏ); phân rã mọi lợi ích thành phần chuyển được và phần typicality bằng hai panel người; bất biến đường biên đã đăng ký trước.
- Bài không được claim: phương pháp mới đột phá; "SCST đầu tiên cho tiếng Việt"; "novel ensemble"; "giảm ảo giác" chỉ dựa trên CHAIR theo ref; lợi của ref truy hồi là chất lượng; hai GPU.

## 4. Kế hoạch bảng ablation

Thống kê chung:
- Bootstrap cặp theo ảnh, gộp các cặp cùng seed (3 × 558), B = 2000. t-test giữa seed chỉ phát hiện khoảng +12.7 [CTX], nên được báo kèm nhưng không dùng để claim.
- Họ so sánh chính (T5 − T2, D7 − mốc P1, D7 − D5) hiệu chỉnh Holm.
- Mọi hàng báo: CIDEr, B-1, B-4, METEOR, ROUGE-L, CHAIR_i, CHAIR_s, mention/caption, object P/R/F1 (`object_prf.py --seeds`), CIDEr và CHAIR_i theo panel OpenViIC, CLIP-S/RefCLIP-S (`clip_score.py`), số âm tiết, tỉ lệ chép nguyên văn caption train, distinct-2, tỉ lệ mở đầu bằng "có", số lần giải mã/ảnh, GPU-s/ảnh.
- Báo thêm tập bỏ cặp gần trùng train–test (`near_dup.py`, cos ≥ 0.90) [V:B1-P1].

| Mã | Hàng | Seed | Hiện có? | Câu hỏi |
|---|---|---|---|---|
| T0 | Zero-shot | – | có | Sàn |
| T1 | P1 legacy | 42, 43, 44 | có (145.8) | Mốc của thanh +8 |
| T2 | P1-assist (loss chỉ trên câu trả lời) | 42, 43, 44 | s42 có (148.7); s43 đang chạy (n3, `50_d`); s44 cần chạy | Điểm xuất phát của RL; so cặp cùng seed |
| T3 | MR5-assist, cùng số bước với P1 (942 bước, 0.4 epoch) | 42 (+43, 44 nếu R1 đạt) | không; bản 1 epoch (2,355 bước) có: 147.5 | RL có hơn SFT cùng dùng 5 ref không [V:B1-P1, đổi 3] |
| T4 | RLOO thường (EOS + END, không CN) | 42 (+43, 44 chỉ khi CN được claim ở R1) | không | Giá trị của CN |
| T5 | **CN-RLOO** (hoặc T4 nếu R1 chọn nhánh thường) | 42, 43, 44 | không | Phương pháp huấn luyện chính |
| T6 | T2 và T5 giải mã base 4-bit | 42, 43, 44 | không | Ảnh hưởng của NF4 so với bf16 (F5) |
| D1 | Self-MBR 1 adapter (greedy + 6 mẫu T\*) | T5 × 3 | không | MBR một adapter còn thêm gì sau RL |
| D2 | Self-MBR 1 adapter, 20 mẫu | T5 s42 | không | Đối chứng cùng số giải mã [V:B3-P1, đổi 2b] |
| D3 | EV-MBR 1 adapter (+ ref truy hồi k\*) | T5 × 3 | không | Typicality cùng panel với 7 giải mã |
| D4 | D3 với ref ngẫu nhiên; D3 với truy hồi theo ảnh (CLIP 1-NN, `data/dedup`) | T5 s42 | không | Lợi có đặc thù theo ảnh không; truy hồi theo caption hay theo ảnh |
| D5 | C-MBR chỉ P1-assist × 3 + mẫu | 1 committee | không | Baseline giải mã không RL; RL phải thắng nó |
| D6 | C-MBR chỉ T5 × 3 + mẫu | 1 committee | không | Committee seed sau RL |
| D7 | **S\* = T5 × 3 + T2 × 3 + mẫu** | 1 committee | không | Hệ chính; thành phần đăng ký trước |
| D8 | S\* + ref truy hồi k\* | 1 | không | Hàng tối đa KTVIC (ghi nhãn typicality) |
| D9 | S\* + veto phiếu t\* | 1 | không | Đường CIDEr–CHAIR (chỉ khi qua cổng D) |
| D10 | 3 committee tách seed {T5_s, T2_s} | s = 42, 43, 44 | không | Phương sai giữa các committee |
| D11 | S\* + fuse2 × 3 (tuỳ chọn) | 1 | adapter có | Yếu tố "đa policy" của [B3] trên thành viên mới |
| U1–U3 | UIT-ViIC: P1-assist × 3, CN-RLOO × 3, C-MBR của chúng (test 231); CHAIR theo instance trên test + val (1,155) | 42, 43, 44 | không | Lặp lại và sự thật |
| E1–E3 | uitviic_en: P1-assist, CN-RLOO, self-MBR 1 adapter; chuyển sang `coco_en` test | 42 (+43, 44 có điều kiện) | không | Chéo ngôn ngữ |

## 5. Kế hoạch GPU theo giai đoạn (hai RTX 3090: n2, n3)

Bài chỉ claim **một** RTX 3090. Mỗi job dùng một GPU và vừa 24 GB. Máy thứ hai chỉ để tăng thông lượng. Bài báo cáo GPU-h từng run và tổng GPU-h.

Đơn giá dùng để ước tính:
- RL k = 8: 10.1 s/ảnh, đo ở dry run [C3]. 1,000 ảnh ≈ 2.8 h; cộng 4 lần chấm dev ≈ 3.2 GPU-h. 3,469 ảnh ≈ 9.7 h. Phải đo lại sau khi sửa bộ nhớ.
- SFT P1 2 epoch: 1.93 GPU-h trên 3090 của n2 [V:B1-P1].
- Greedy short trên 558 ảnh ≈ 0.25 GPU-h [R5-00 §7a]. 6 mẫu short ≈ 3.6 s/ảnh, tức ≈ 0.6 GPU-h cho 558 ảnh [B4 §7].

### 5a. Ngân sách

| Giai đoạn | Lõi (GPU-h) | Có điều kiện (GPU-h) | Cổng dừng |
|---|---|---|---|
| 0. Code, đăng ký trước, dry run | 0.1 | 0.1 (thử lại ở k = 4) | C3 |
| 1. Pilot dev: G1 hai nhánh, mẫu dev, P1-assist s44 | 10.5 | 13.8 (kéo dài) + 3.2 (D1b) + 3.2 (dự phòng T = 0.8) + 0.3 (mẫu dev của RL_dev) | R1, D |
| 2. KTVIC full train, 3 seed, giải mã | 50 (N\* = 3,469) hoặc 22 (N\* = 1,000) | 4.0 (MR5 942 bước s43/s44) + 19.9 (RLOO thường s43/s44) | R2 |
| 3. UIT-ViIC trong miền | 31 (hoặc ≈ 15 nếu N\* = 1,000) | – | R3 |
| 4. Tiếng Anh và COCO | 11.5 (≈ 6 nếu N\* = 1,000) | 21 (seed 43/44) | R4 |
| **Tổng** | **≈ 54–103** | **tối đa ≈ 170** | |

### 5b. Thay đổi code (trong repo; agent R6 không sửa repo)

| Mã | File | Thay đổi | Kiểm tra |
|---|---|---|---|
| C-R1 | `scripts/train_rl.py` | (a) Bộ nhớ: sau `build_model`, ép mọi tham số fp32 không thuộc LoRA về bf16 (embed_tokens, lm_head, các norm mà `prepare_model_for_kbit_training` đã nâng lên fp32); job đặt `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`. (b) `--no-dev` cho run full train: không chấm dev, chỉ lưu `last/`. (c) `--resume RUN`: policy lấy từ `RUN/last`, ref vẫn là adapter SFT, bỏ qua các ảnh đã dùng trong schedule, lưu và nạp trạng thái AdamW. (d) Advantage ≤ 0 cho rollout đã xong mà từ cuối ∉ END; log `fragment_rate` và mention/caption. (e) `--prompt short` hoặc `short_en`. (f) `--temperature`, chỉ cho nhánh dự phòng: chia logits cho T ở sampler và ở `token_logprobs` của cả policy lẫn ref | Dry run C3: reserved ≤ 22 GB, gap log-prob trung bình < 0.02, sampler = policy. `--self-check` thêm ca END |
| C-R2 | `scripts/rl_reward.py` | END = các từ (đã tách từ) đứng cuối ít nhất một ref train, bỏ ảnh dev nếu có `--dev-file`; hàm `fragment()`; `rloo(r, mask, nonpos)`. `--lang en`: tách token như đường tiếng Anh của evaluate.py (PTB), vẫn thêm EOS | Ca "… điện thoại di" bị gắn cờ; greedy P1_dev bị gắn cờ 3.0% (F6) |
| C-R3 | `scripts/rl_report.py` | Cổng v2 (R1 ở §5d): Δ dev của **checkpoint cuối** theo evaluate.py, có cận dưới bootstrap cặp; các guard mới; phán quyết pass, extend, kill hoặc under-moved. `compare()` đối xứng, bỏ `KEEP_PLAIN_MARGIN`. `panel()` thêm `--split test`. In tỉ lệ trùng giữa greedy NF4 và bf16 | Chạy lại trên log của dry run |
| C-R4 | `scripts/mbr_decode.py` (mới) | Luật đóng băng của [B3] (CIDEr-D trung bình với bằng chứng, sigma 6) + ref truy hồi của [B4] (TF-IDF 1–2 gram trên 5 ref mỗi ảnh train, truy vấn = caption greedy) + veto phiếu + đối chứng ref ngẫu nhiên và truy hồi theo ảnh. DF và chỉ mục chỉ từ ref train, bỏ dev300 khi chạy dev (assert). Làm tròn utility đến 1e-9 rồi chọn chuỗi nhỏ nhất. Port từ `B3_decoding/pilot.py`, `verify/pb41/evmbr_check.py` và `S0_synthesis/dev_mbr.py` | Self-check: tái lập 156.15 của [B3] (đủ 558/558 caption) và các số [DEV] |
| C-R5 | `manuscript/prereg/2026-10-13_R6_method/PREDICTIONS.md` | Cổng C3, R1, D, R2–R4; bảng dự báo §1b; thành phần của S\*; sha256 của C-R1–C-R4 | Commit **trước** output G1 đầu tiên |
| C-R6 | `scripts/train_rl.py` (tuỳ chọn) | `rollout()` chạy prefill của prompt một lần cho k mẫu, như `token_logprobs` đã làm (hiện ViT và prefill chạy k lần) | Gap log-prob của C3. Chỉ làm nếu thời gian là nút thắt |

Biến chung của mọi job (theo mẫu các job 35–59):

```bash
cd /root/vsps && . .venv/bin/activate && set -e
export NCS_DATA=/root/ncs-data JAVA_HOME=<như job 35_b> PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
RUN=$NCS_DATA/runs; RL=$NCS_DATA/rl; R=$NCS_DATA/results; S=$NCS_DATA/samples
TRD=data/splits/ktvic_train_minus_dev300.txt; DEV=data/splits/ktvic_dev300.txt
DEVDS=<thư mục dev của job 35_a, tạo bởi ktvic_dev_split.py --json-dir>
E="python scripts/evaluate.py --model qwen2.5-vl-7b"
```

Tên job chỉ là đề xuất. Trước khi xếp, tác giả kiểm `/root/queue` để không trùng số. `qrun.sh` chạy theo thứ tự tên, nên các tên `35_*` chạy trước các job 36+ đang chờ.

### 5c. Giai đoạn 0: code, đăng ký trước, dry run (0.1 GPU-h)

Việc: C-R1 đến C-R5 kèm self-check, commit, chép lên n2 và n3. Prereg C-R5 phải commit trước output đầu tiên của G1.

```bash
# 35_e_cn_dryrun_bf16 (n2)
python scripts/train_rl.py --adapter $RUN/p1dev_s42 --out $RL/dryrun2_cn_s42 --images-file $TRD --dev-file $DEV \
  --dev-limit 20 --n-images 20 --k 8 --tau 0.9 --eval-every 20 --dry-run --seed 42 \
|| python scripts/train_rl.py --adapter $RUN/p1dev_s42 --out $RL/dryrun2_cn_k4_s42 --images-file $TRD --dev-file $DEV \
  --dev-limit 20 --n-images 20 --k 4 --tau 0.9 --eval-every 20 --dry-run --seed 42
```

**Cổng C3.** Mọi guard của C3 phải đạt, kể cả peak reserved ≤ 22 GB.
- Đạt ở k = 8: K = 8.
- Chỉ đạt ở k = 4: K = 4, ghi vào prereg.
- Trượt cả hai: dừng RL. Hệ của bài là C-MBR trên adapter SFT (hàng (b) của §1b).

### 5d. Giai đoạn 1: pilot trên dev (lõi 10.5 GPU-h)

```bash
# 35_f_g1_cn (n2): nhánh CN, 1,000 ảnh
python scripts/train_rl.py --adapter $RUN/p1dev_s42 --out $RL/g1_cn_s42 --images-file $TRD --dev-file $DEV \
  --n-images 1000 --k $K --tau 0.9 --beta 0.03 --lr 2e-5 --eval-every 250 --seed 42
NCS_DATASET=$DEVDS $E --adapter $RL/g1_cn_s42/last --split dev_data.json --prompt short \
  --name g1_cn_s42-dev300-short --out $RL/g1_cn_s42-dev300-short.json
python scripts/rl_report.py --gate $RL/g1_cn_s42 --p1dev $RL/p1dev_s42-dev300-short.json \
  --rl $RL/g1_cn_s42-dev300-short.json --g0-report $RL/g0/g0_report.json
python scripts/rl_report.py --panel $RL/p1dev_s42-dev300-short.preds.json $RL/g1_cn_s42-dev300-short.preds.json \
  --out $RL/g1_cn_s42-panel.json
NCS_DATA=data python scripts/vi_diagnostics.py --split dev --preds $RL/p1dev_s42-dev300-short.preds.json \
  $RL/g1_cn_s42-dev300-short.preds.json --out $RL/g1_cn_s42-vi.json        # [PRE-VI], không gate

# 35_g_g1_plain (n3, sau khi chép runs/p1dev_s42 và rl/g0/ từ n2): giống hệt, thêm --no-copy-mask, out g1_plain_s42

# 50_e_p1assist_s44 (n3)
python scripts/train_stage2.py --stage sft --data $NCS_DATA/gold_p1 --out $RUN/p1assist_s44 --epochs 2 --seed 44 \
  --loss-mask assistant
$E --adapter $RUN/p1assist_s44 --prompt short --name p1assist_s44-short

# 50_f_dev_samples (n3): bằng chứng MBR trên dev; không dùng lại rollout T = 1.0 (F3)
for T in 0.5 0.8; do
  python scripts/e5_sample.py --adapter $RUN/p1dev_s42 --split train_data.json --images-file $DEV --limit 0 \
    --prompt short --n 6 --temperature $T --top-p 0.95 --out $S/p1dev_s42-dev300-short-T$T.jsonl
done
python scripts/e5_sample.py --adapter $RUN/p1dev_s42 --split train_data.json --images-file $DEV --limit 0 \
  --prompt short --n 24 --temperature 0.8 --top-p 0.95 --seed 43 --out $S/p1dev_s42-dev300-short-T0.8-n24.jsonl
# CPU: lưới dev k ∈ {10, 30}, veto ∈ {không, 2/7, 3/7}, T ∈ {0.5, 0.8}; đối chứng self-MBR 25 ứng viên,
# ref ngẫu nhiên, truy hồi theo ảnh
python scripts/mbr_decode.py --dev --greedy $RL/p1dev_s42-dev300-short.preds.json \
  --samples $S/p1dev_s42-dev300-short-T0.5.jsonl $S/p1dev_s42-dev300-short-T0.8.jsonl \
  --control-samples $S/p1dev_s42-dev300-short-T0.8-n24.jsonl --grid --out $RL/decode_dev_grid.json
# Sau R1 (0.3 GPU-h): 6 mẫu ở T* của adapter G1 thắng trên dev300, rồi đo D1/D3/D5-D7 phiên bản dev
# (cộng dồn RL + MBR trên dev, [V:P-B4-1, đổi 5])
```

**Cổng R1 (từng nhánh G1; đăng ký trước trong C-R5).** Δ = CIDEr dev của checkpoint cuối theo evaluate.py − 144.33 (P1_dev).
- **Đạt ở 1,000 ảnh** khi Δ ≥ +3.0, cận dưới bootstrap cặp > 0, và đủ guard [V:B1-P1, đổi 2 và 4; F6]:
  - exact-copy của khối 250 ảnh cuối ≤ 2 × step-0 (≤ 1.33% [G0]);
  - kết thúc bằng hư từ ≤ 1%;
  - cờ END trên greedy dev ≤ 4.0% (P1_dev: 3.0%);
  - số âm tiết ≥ 10.7 (0.9 × 11.9) và mention/caption ≥ 1.58 (0.9 × 1.76).
  Khi đó N\* = 1,000.
- **Vùng xám** (+1.0 ≤ Δ < +3.0, hoặc Δ ≥ +3.0 mà cận dưới ≤ 0): kéo dài bằng `--resume` tới 3,469 ảnh (≈ 6.9 GPU-h), chấm lại một lần theo cùng luật. Đạt thì N\* = 3,469. Hai lần nhìn, mỗi lần đòi cận dưới > 0, nên một nhánh không có hiệu ứng lọt qua với xác suất cỡ 5%.
- **Under-moved** (KL mỗi caption ở khối cuối < 0.2 nat): chạy lại đúng một lần ở lr 5e-5 (luật D1b đã đăng ký, `rl_report.py`).
- **Trượt** (Δ < +1.0 với KL ≥ 0.2, hoặc vẫn ở vùng xám sau khi kéo dài): nhánh chết.
- **Chọn nhánh** cho giai đoạn 2: nhánh đạt có Δ cao hơn ở cùng số ảnh. **Chỉ claim CN** khi CN − thường ≥ +3.0 với cận dưới > 0 trên dev; khi đó giai đoạn 2 chạy thêm RLOO thường s43, s44. Ngược lại, CN chỉ là ablation 1 seed.
- **Cả hai nhánh trượt**: một nhánh dự phòng, rollout ở T = 0.8 với log-prob của phân phối đã chia nhiệt (C-R1f), 1,000 ảnh, cùng cổng. Lý do: rollout T = 1.0 chỉ đạt 72–78 CIDEr-D so với greedy 140–148 [G0], và không chuyển sang panel (F4). Nhánh này thay cho phép thử cross-fit của [B1], vì F1 cho thấy học thuộc không phải kênh chính. Dự phòng cũng trượt: RL chết; hệ của bài là hàng (b) §1b.

**Cổng D (tầng giải mã; dev300; adapter p1dev_s42).**
- Chọn T\* và k\* theo CIDEr dev cao nhất, với điều kiện CHAIR_i ≤ CHAIR_i của greedy.
- Giữ ref truy hồi chỉ khi PE-MBR (7 ứng viên) − self-MBR (25 ứng viên) ≥ +2.0 **và** PE-MBR − greedy ≥ +4.0 với cận dưới > 0 [V:P-B4-1, đổi 3]. Ở T = 1.0 đã có +4.2 [+1.0, +8.0] so với greedy (F3); còn thiếu đối chứng 25 ứng viên.
- Giữ veto chỉ khi ΔCIDEr ≥ −1.0 và ΔCHAIR_i ≤ −1.5 so với không veto.
- Luật committee không có tham số; đóng băng theo [B3].

### 5e. Giai đoạn 2: KTVIC full train, 3 seed (lõi 22–50 GPU-h)

Chỉ chạy khi R1 đạt. Thông số đóng băng từ R1: nhánh, K, β = 0.03, lr 2e-5, N\*, τ = 0.90 [G0]. Không còn dev, nên dùng checkpoint cuối.

```bash
# 64_rl_s{42,43,44}: chạy ở máy giữ adapter p1assist tương ứng (hoặc chép sang)
for s in 42 43 44; do
  python scripts/train_rl.py --adapter $RUN/p1assist_s$s --out $RL/cn_s$s --n-images $NSTAR --k $K --tau 0.9 \
    --beta 0.03 --lr 2e-5 --no-dev --seed $s                    # thêm --no-copy-mask nếu R1 chọn nhánh thường
  $E --adapter $RL/cn_s$s/last --prompt short --name cn_s$s-short
  $E --adapter $RL/cn_s$s/last --prompt short --four-bit --name cn_s$s-4bit-short                  # T6
  $E --adapter $RUN/p1assist_s$s --prompt short --four-bit --name p1assist_s$s-4bit-short           # T6
done
# 65_samples_test: bằng chứng cho C-MBR, 6 thành viên
for m in $RL/cn_s42/last $RL/cn_s43/last $RL/cn_s44/last $RUN/p1assist_s42 $RUN/p1assist_s43 $RUN/p1assist_s44; do
  python scripts/e5_sample.py --adapter $m --split test_data.json --limit 0 --prompt short --n 6 \
    --temperature $TSTAR --top-p 0.95 --out $S/<tên của $m>-test-short-T$TSTAR.jsonl
done
python scripts/e5_sample.py --adapter $RL/cn_s42/last --split test_data.json --limit 0 --prompt short --n 20 \
  --temperature $TSTAR --top-p 0.95 --seed 43 --out $S/cn_s42-test-short-n20.jsonl               # D2
# 66_rl_alt_s42 (T4, 1 seed): như 64 với nhánh còn lại (--no-copy-mask hoặc ngược lại)
# 67_mr5assist942_s42 (T3): như job của mr5assist_s42 (67b9b6e) nhưng --epochs 0.4 (942 bước); s43, s44 có điều kiện
# CPU: chọn và chấm (ref test chỉ được đọc khi chấm)
python scripts/mbr_decode.py --test --members cn_s42,cn_s43,cn_s44,p1assist_s42,p1assist_s43,p1assist_s44 \
  --samples-dir $S --temperature $TSTAR --out $R/s_star-short.preds.json       # D7; thêm --retrieve-k $KSTAR cho D8
$E --predictions $R/s_star-short.preds.json --prompt short --name s_star-short
python scripts/rl_report.py --panel --split test $R/p1_s43-short.preds.json $R/s_star-short.preds.json \
  --out $R/s_star-panel.json
```

**Cổng R2 (claim cuối; đăng ký trước).**
- Claim huấn luyện: T5 − T2, bootstrap cặp gộp 3 seed, cận dưới > 0. Báo thêm T5 − T3 (MR5) và T5 − T4.
- Thanh "đột phá": D7 − 145.8 ≥ +8.0 với cận dưới > 0, và ΔCHAIR_i ≤ 0 với cận trên < +1.0. Báo cùng lúc so với trung bình 3 seed P1-assist và so với thành viên tốt nhất, trên cả ref KTVIC lẫn panel [V:B3-P1, đổi 3 và 6].
- "Chất lượng chuyển được" chỉ khi Δ trên panel OpenViIC có CI > 0. Ngược lại ghi "typicality của KTVIC".
- Guard chống ăn gian: số âm tiết trong ±1 so với P1; tỉ lệ chép nguyên văn caption train ≤ 1.5 × P1 (P1: 20–23% [V:B2-1]); distinct-2 ≥ 0.9 × P1; CLIP-S và RefCLIP-S không thấp hơn P1 với CI. Trượt guard nào thì claim tương ứng bị hạ, nhưng số vẫn được báo.

### 5f. Giai đoạn 3: UIT-ViIC trong miền (lõi ≈ 31 GPU-h)

Siêu tham số đóng băng từ KTVIC. N\*_U = N\* × 2,695 / 3,469. τ = 0.90, không hiệu chỉnh lại: không có dev, và UIT-ViIC val không được dùng để chọn [R4-00 §6]. Nếu job `52_a` đã chạy với mask legacy, P1 của UIT-ViIC phải chạy lại với `--loss-mask assistant`.

```bash
export NCS_DATASET=uitviic
for s in 42 43 44; do
  python scripts/train_stage2.py --stage sft --data <dữ liệu SFT của 52_a> --out $RUN/uitviic_p1assist_s$s \
    --epochs 2 --seed $s --loss-mask assistant
  python scripts/train_rl.py --adapter $RUN/uitviic_p1assist_s$s --out $RL/uitviic_cn_s$s --n-images $NSTAR_U \
    --k $K --tau 0.9 --beta 0.03 --lr 2e-5 --no-dev --seed $s
  for sp in test val; do
    $E --adapter $RUN/uitviic_p1assist_s$s --split ${sp}_data.json --prompt short --name uitviic_p1assist_s$s-$sp-short
    $E --adapter $RL/uitviic_cn_s$s/last --split ${sp}_data.json --prompt short --name uitviic_cn_s$s-$sp-short
  done
done
# 6 mẫu ở T* cho C-MBR trên test (231 ảnh), như job 65.
# CPU: CHAIR và P/R theo instance COCO trên test + val, dùng đúng script và lexicon v2 của cổng G3' ([R5-00] §7c).
```

**Cổng R3.**
- "Lặp lại được" khi CN-RLOO − P1-assist trên test UIT-ViIC có cận dưới > 0 (gộp 3 seed).
- "Không thêm ảo giác theo nhãn người" khi ΔCHAIR_i theo instance COCO trên test + val (1,155 ảnh) có cận trên < +1.0.
- Báo tỉ lệ chép nguyên văn. 41% ref test UIT-ViIC có nguyên văn trong ref train + val [V:P-B4-1 §3f], nên rủi ro chép ở đây cao hơn KTVIC.

### 5g. Giai đoạn 4: tiếng Anh và COCO (lõi ≈ 11.5 GPU-h)

```bash
export NCS_DATASET=uitviic_en
python scripts/train_stage2.py --stage sft --data <dữ liệu SFT của 53_a> --out $RUN/uitviic_en_p1assist_s42 \
  --epochs 2 --seed 42 --loss-mask assistant                    # bỏ qua nếu 53_a đã chạy với mask assistant
python scripts/train_rl.py --adapter $RUN/uitviic_en_p1assist_s42 --out $RL/en_cn_s42 --prompt short_en --lang en \
  --n-images $NSTAR_U --k $K --tau 0.9 --beta 0.03 --lr 2e-5 --no-dev --seed 42
for m in $RUN/uitviic_en_p1assist_s42:en_p1assist_s42 $RL/en_cn_s42/last:en_cn_s42; do
  $E --adapter ${m%%:*} --split test_data.json --prompt short_en --name uitviic_${m#*:}-short_en
  NCS_DATASET=coco_en $E --adapter ${m%%:*} --split test_data.json --prompt short_en --name coco_${m#*:}-short_en
done
```

**Cổng R4.** Claim "không phụ thuộc ngôn ngữ" chỉ khi Δ (RL − P1) trên test `uitviic_en` có cận dưới > 0. Với 1 seed phải ghi rõ là một seed. Chạy seed 43, 44 (≈ 21 GPU-h) chỉ khi R3 đạt và Δ của seed 42 ≥ +2.0. Hàng `coco_en` là chuyển miền, chỉ báo cáo.

### 5h. Lịch (ước tính)

| Ngày | n2 | n3 | CPU và quyết định |
|---|---|---|---|
| 0 (13/10) | xong `36_coco_b`; chạy `35_e` (C3) | `50_d` (P1-assist s43) đang chạy → `50_e`, `50_f` | C-R1 đến C-R5; commit prereg trước `35_f` |
| 0–1 (13–14/10) | `35_f` (G1 CN, ≈ 3.2 h); kéo dài nếu ở vùng xám (≈ 6.9 h) | `35_g` (G1 thường) | Cổng R1; lưới dev và cổng D |
| 1–2 (14–15/10) | `64_rl` s42, s44 | `64_rl` s43; `65` mẫu test | `mbr_decode`; cổng R2 |
| 2–4 (15–17/10) | Giai đoạn 3 | Giai đoạn 3 và 4 | Cổng R3, R4 |

Hàng đợi hiện có (37–42 trên n2; 52–63 trên n3 [R5-00 §7]) dùng chung GPU. Tác giả quyết thứ tự.

## 6. Đề xuất bị loại ở vòng này

- **B1-P2 EHX-RLOO** (tag làm gợi ý khám phá cho RL): đã bị đi trước bởi Guide-GRPO (2506.13923, Eq. 6), SAGE và POPE. Greedy của một seed P1 khác thêm đúng bằng tag (+1.1 đến +2.0), nên giá trị riêng của tag ≈ 0; 0% nhóm rollout sập [V:B1-P2].
- **B2-1 MR5** (SFT trên cả 5 ref): đã bị đi trước (Zheng 2018, 1808.09564; thực hành chuẩn). Run thật kém P1 khớp mask 1.2 CIDEr [CTX]. Chỉ giữ làm đối chứng T3 [V:B2-1].
- **B2-2 PanelBridge** (panel thứ hai làm cầu nối phong cách): incremental (LaCLIP, CapsFusion, NICE 2024, MoCHA); dùng target tổng hợp; lợi ≈ 0 ± 3; tiêu mất panel độc lập; nhánh UIT-ViIC như đã viết làm rò rỉ cả 231 ảnh test; 117–225 GPU-h [V:B2-2].
- **B3-P2 chưng cất Committee-MBR**: incremental (MBR finetuning 2309.10966, C-GRPO 2602.03102, SD-FSIC WACV 2021); lợi thực tế 0 đến +3; 57% lợi của teacher là giảm phương sai mà một student không giữ được; dùng target tổng hợp [V:B3-P2].
- **P-B4-2 PM-Probe** (probe trạng thái ẩn làm veto): đã bị đi trước bởi TLC-L (2305.07021). Veto phiếu không nhãn đã bằng một probe AUROC 0.81 ở cùng CIDEr; cổng AUROC 0.85 khó đạt [V:P-B4-2].
- **B5-1 seed soup**: đã bị đi trước (SeedLoRA, LoRA Soups CAT); 80% lợi của proxy là chọn medoid; lợi thực tế khoảng +1.5, dưới MDE [V:B5-1].
- **B5-2 backbone Qwen3.5-9B**: không có novelty; lợi dự kiến ≈ 0 CIDEr; tốn công port; caption KTVIC có trên HF Hub từ 2024 [V:B5-2].
- **P-B6-1 RMH** (từ của ảnh lân cận làm gợi ý trong prompt): incremental (TUNA, DualCap, CONCAP, VLCAP, ViECap); tiền lệ tag không có ý nghĩa thống kê; nội dung gợi ý trị giá −0.4 đến −2.7 CIDEr trong proxy [V:P-B6-1].
- **P-B6-2 RHX-RLOO** (gợi ý truy hồi cho RL): đã bị đi trước bởi Re3Cap (2608.21305) và Guide-GRPO; giá trị riêng của truy hồi ≈ +0.2; khoảng trống khám phá thật chỉ 6.7% ảnh [V:P-B6-2].
- **P-B7-1 PB-RLOO** (co tâm ref về ref lân cận + phạt CHAIR): incremental (CIDErBtw đảo dấu). Một nửa lợi là rò rỉ khuôn câu của chính câu giám khảo; khi bỏ rò rỉ còn +1.18 [−0.08, +2.43]; phần phạt CHAIR là prior art [V:P-B7-1].
- **P-B7-2 CT-Veto** (critic theo ngữ cảnh cùng panel): incremental (TLC-L, SelfVal, JEC/TagProp). So với veto phiếu không nhãn ở cùng CIDEr, CHAIR_i chỉ −0.67 [−1.52, +0.16] [V:P-B7-2].
- **N1** (thành phần riêng của tiếng Việt): hai ứng viên trượt cổng CPU; 17 phần thưởng thay thế đều trung tính hoặc có hại. Chỉ giữ phân tích [N1 §0].

## 7. Rủi ro

### 7a. Ăn gian metric
- **Cắt cụt và mảnh câu.** EOS chỉ hạ tỉ lệ ảnh mà bỏ âm tiết cuối làm tăng thưởng từ 29.7% xuống 24.2% [V:B1-P1]. END bắt 36.6% bản bị cắt, với báo động giả 3.0% trên greedy [FRAG]. Guard dev: cờ END ≤ 4.0%, số âm tiết ≥ 10.7.
- **Typicality.** Truy hồi và các tín hiệu cùng panel tăng KTVIC mà không tăng panel độc lập (F3; [B3] Bảng F; [V:P-B7-1]). Ở T = 1.0, oracle theo KTVIC không chuyển sang panel (F4). Mọi claim "chất lượng" phải qua panel.
- **Chép khuôn câu.** Rollout chép nguyên văn ref của ảnh khác chiếm 9.3% advantage dương, và CN không thấy kênh này [V:P-B7-1 §D]. P1 đã chép nguyên văn caption train ở 20–23% [V:B2-1]. Báo tỉ lệ chép ở mọi hàng.
- **Thiên lệch metric của MBR** khi utility là chính metric (Kovacs 2411.03524): kiểm bằng CLIP-S, RefCLIP-S và panel.
- **CHAIR theo ref đo typicality.** SCST làm tăng CHAIR trong văn liệu. Sự thật chỉ được kiểm bằng instance COCO trên UIT-ViIC.
- Lặp từ và khuôn đệm đã bị CIDEr-D mức từ phạt (−40, −60) [B1 §2.7]. Vẫn báo tỉ lệ bigram lặp.

### 7b. Rò rỉ
- dev300 nằm ngoài pool RL (đã assert trong `train_rl.py`), ngoài chỉ mục truy hồi và DF khi tinh chỉnh (C-R4 phải assert). Chỉ mục trên toàn bộ train làm 57.4% ảnh RL chạm tới ref dev [V:P-B7-1].
- Không luật nào đọc ref test. k, T và ngưỡng chỉ chọn trên dev.
- 401/558 ảnh test KTVIC nằm trong OpenViIC train [CTX]. OpenViIC chỉ làm giám khảo, không bao giờ dùng để train.
- Báo kết quả có và không có cặp train–test gần trùng (`near_dup.py`, cos ≥ 0.90) [V:B1-P1]. Khuôn câu gần trùng giữa hai ảnh khác nhau không bị CLIP bắt (cos trung vị 0.72–0.73) [V:P-B7-1 §B].
- UIT-ViIC train có 133 ảnh Karpathy test (F7). Dùng `coco_en` test (sạch), không dùng toàn bộ Karpathy test.
- Nhiễm từ tiền huấn luyện: caption KTVIC train và test có trên HF Hub từ 2024 [V:B5-2]. Điều này ảnh hưởng số tuyệt đối và zero-shot; so sánh cặp ít bị ảnh hưởng hơn.
- Độ chính xác lúc giải mã: NF4 trong run và bf16 của evaluate.py khác nhau ở 55% caption dev (F5). Cổng dùng evaluate.py; báo thêm hàng 4-bit.

### 7c. Dữ liệu huấn luyện tổng hợp [CỜ CHO TÁC GIẢ]
- S\* không dùng target SFT do mô hình viết, không dùng nhãn AI-silver.
- RL cập nhật adapter từ rollout do chính policy sinh. Phần thưởng chỉ đến từ ref người. [CTX] cho phép tín hiệu do mô hình sinh bên trong phương pháp, nhưng yêu cầu gắn cờ. **Tác giả cần xác nhận trước giai đoạn 1.**
- Mẫu ở tầng giải mã chỉ làm bằng chứng; không dùng để train.
- Ba đề xuất dùng dữ liệu tổng hợp (B1-P2, B2-2, B3-P2) đều đã bị loại.

### 7d. Giấy phép
- UIT-OpenViIC: "non-commercial research", không có điều khoản phân phối lại [R5-01]. `data/ktvic_openviic_refs.json` chỉ được đọc, nằm ngoài git; không chép caption vào file commit. File này không trích caption nào.
- KTVIC: các report không ghi giấy phép. Kiểm điều khoản trước khi phát hành adapter hoặc preds.
- COCO: annotation CC BY 4.0; ảnh theo điều khoản Flickr của từng ảnh.
- Qwen2.5-VL-7B-Instruct: Apache-2.0. Backbone phụ Qwen2.5-VL-3B: giấy phép qwen-research [V:B5-2].
- VnCoreNLP nằm trong vòng tính phần thưởng: kiểm giấy phép trước khi đóng gói code phần thưởng.

### 7e. Tính toán và thống kê
- RL đo được 10.1 s/ảnh (F2) và chiếm phần lớn ngân sách. Nếu cần: C-R6, hoặc k = 4.
- 3 seed mỗi nhánh chỉ phát hiện khoảng +12.7 bằng t-test giữa seed [CTX]. Claim +8 dùng bootstrap cặp gộp; t-test vẫn được báo.
- SE của hiệu số trên dev300 giữa hai seed SFT là 3.0–3.3 [V:B1-P1]. Cổng +3.0 với cận dưới > 0 vì vậy đòi Δ quan sát cỡ +6; một hiệu ứng thật +4 có thể trượt. Đó là giá của việc không để nhánh rỗng lọt qua.
- Nhiều đường rẽ (hai nhánh, kéo dài, D1b, dự phòng, lưới giải mã): mọi cổng được đăng ký trước (C-R5); họ so sánh chính hiệu chỉnh Holm.

### 7f. Novelty
- Đây là rủi ro lớn nhất. Reviewer sẽ đọc S\* là "SCST + ensemble MBR". Bài chỉ đứng vững nếu số mạnh, đo kỹ, và phần phân tích (hai panel, biên RL, đường biên) được trình bày như đóng góp chính.
