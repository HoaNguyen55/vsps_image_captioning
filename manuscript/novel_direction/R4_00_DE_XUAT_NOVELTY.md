# R4-00: Đề xuất novelty và kế hoạch 7 ngày sau vòng nghiên cứu đa tác tử

12/10/2026, nhánh `paper-v10`. Tổng hợp từ 6 nhóm khai thác tài liệu (target, RL, suy luận, tiếng Việt, hiệu năng, lý thuyết đánh giá), mỗi ý tưởng qua một phản biện đối kháng về tính mới và tính khả thi (có kiểm tra CPU trên preds sẵn có), cùng 3 reviewer Q1 giả lập (TMM / PR / Neurocomputing / TNNLS).

**Ràng buộc áp cho mọi đề xuất dưới đây**
- Quyết định của tác giả (12/10): **không gán nhãn mới**. Không làm human gold, không mở vòng đánh giá người mới, kit `annotation/` gác lại. Nhãn AI-silver (`data/object_gold/annot_claude.json`, do Claude tạo) **không** là bằng chứng và bị bỏ khỏi bài. Câu hỏi "đối tượng có thật không" chỉ được trả lời bằng nhãn người **có sẵn**: instance COCO-2014 (ảnh UIT-ViIC là ảnh COCO, cộng COCO Karpathy-test) và RePOPE (2504.15707).
- Bài chỉ claim **một RTX 3090 24 GB**. Hai máy thuê (n2, n3) chỉ để tăng thông lượng: mỗi job dùng 1 GPU, bài báo cáo tổng GPU-h.
- Trong phương pháp chỉ dùng mô hình mở.
- Số ghi "đo trong vòng" là kiểm tra CPU của agent trong scratchpad. Phải chạy lại bằng script trong repo trước khi đưa vào bài.

## 1. Tóm tắt điều hành

1. Vòng này kiểm định 24 ý tưởng, cộng 6 ý tưởng "bold" chưa kiểm định. Sau phản biện, **chỉ I1 được giữ** (MBR mức đối tượng, incremental). Sáu ý tưởng đã bị đi trước (RL-3, RL-4, I4, EFF-2, EFF-3, ET2). Số còn lại incremental với lợi ích ≈ 0 hoặc không khả thi. Không ý tưởng nào đạt mức "novel" bảo vệ được.
2. Ba reviewer kết luận bài chưa đủ Q1. Ba điểm fatal chung:
   - "P mất chủ yếu do tham chiếu thiếu" chỉ dựa trên AI-silver.
   - Novelty mỏng: LLaVA (2304.08485), VBCS, Zheng (1808.09564), FuseCap, Bianco/Celona, IC3 đã làm phần lớn.
   - P1 và fuse2 khác nhau ở nhiều biến cùng lúc: số bước, số caption, consensus, độ dài.
3. Vì không gán nhãn mới, bằng chứng presence chỉ đến từ instance COCO-2014 (UIT-ViIC trong miền, COCO transfer) và từ RePOPE hỏi bằng tiếng Việt. Các job 36/37/38/59 đã xếp hàng và nằm trên đường găng (cổng G3).
4. **Phải sửa wording.** KTVIC §3 (2401.08100) ghi "three participants", và giao diện cho **một** người nhập **năm** caption cho mỗi ảnh. Nghĩa là 5 caption của một ảnh nhiều khả năng do một người viết, khớp với hiệu ứng vị trí ở R4_01. Viết "5 caption tham chiếu", không viết "5 annotator độc lập".
5. Storyline mới: một bài **phân tích + recipe + một bước suy luận có cổng**. Đích chính là Neurocomputing; Pattern Recognition nếu G3/G4 cùng chiều. TMM/TNNLS không thực tế khi không có đánh giá người.
6. Kế hoạch gồm 12 việc code/CPU, khoảng 22 GPU-h job mới cốt lõi và ≤ 19 GPU-h job có điều kiện hoặc P3, chạy sau khoảng 75 GPU-h đã xếp hàng. 13 cổng dừng được commit trước khi có số.
7. P1 seed 44 vừa về (chưa commit). Ba seed P1 cho short F1 54.1 / 54.5 / 55.2 và CIDEr 149.8 / 143.9 / 143.7. So với trung bình P1, fuse2-short (F1 58.1, CIDEr 143.9) hơn +3.5 F1 và chỉ kém khoảng 1.9 CIDEr.

## 2. Danh mục ý tưởng

### 2a. Giữ lại và đưa vào kế hoạch (xếp hạng)

Chỉ **I1** có keep=true. Hàng 2–5 là phần cứu được từ các ý tưởng bị loại. Chúng vào bài dưới dạng phân tích, baseline hoặc hygiene, **không** được claim là novelty.

| # | Ý tưởng | Cơ chế (1 dòng) | Loại, novelty, framing bảo vệ được | Hiệu ứng kỳ vọng (P/R/CIDEr/CHAIR_i) | GPU-h mới | Cổng |
|---|---|---|---|---|---|---|
| 1 | **I1: MBR mức đối tượng** (keep=true) | Sinh 6 mẫu cộng output greedy. Mỗi ứng viên được chấm bằng F1 đối tượng so với **hợp** đối tượng của 5 mẫu còn lại (mô phỏng gold hợp-5-tham-chiếu), cộng λ·CIDEr đồng thuận. Chọn argmax, không viết lại câu. Utility và λ chỉ chọn trên ảnh cross-fit mô hình chưa thấy | **Incremental.** Framing: "một bước MBR không cần huấn luyện, utility mô phỏng metric hợp-tham-chiếu, tăng R ở cùng P cho mode hai câu trên nền fusion-SFT, đổi lại k× thời gian suy luận". Phải cite IC3 (EMNLP'23, 2302.01328), SelfVal (2601.22451), Jinnai et al. (ICML'24, 2311.05263), ECO (2405.01028), ASC (EMNLP'24, 2405.13131) và Kovacs et al. (WMT'24, 2411.03524, thiên lệch khi utility ≈ metric). Không claim "panel annotator tổng hợp", không claim kênh probe | Short: P +1–2, F1 +0.3–1.2 (thường n.s.), CIDEr 0 đến +4. Hai câu: R +1.5–4 ở ΔP ≈ 0, F1 +0.5–2. CHAIR_i ≈ 0. Hậu kiểm CPU trên test (chỉ để định hướng): tổ hợp 5 hệ cho R +4.1 [3.1, 5.0] ở ΔP +0.1; panel chỉ gồm mẫu P1 không thêm F1 | 6.4 (72, 82) | G1, G2, G2b |
| 2 | Phân rã presence bằng nhãn người có sẵn (cứu từ ET1, ET3, VN4) | Mention "sai theo tham chiếu" của fuse2 và P1 được tách thành có / không có instance COCO-2014. Dữ liệu: UIT-ViIC test+val trong miền, COCO Karpathy 2500 ảnh. Thêm RePOPE hỏi bằng tiếng Việt và tiếng Anh | Phân tích, incremental: CHAIR (EMNLP'18, 1809.02156) và ALOHa (NAACL'24, 2404.02904) đã dùng instance ∪ tham chiếu. Phần mới là lượng hoá có CI cho một captioner tiếng Việt đã fine-tune. Chưa thấy POPE tiếng Việt: POPE-MUL (2408.00550) và CLAIM (ACL'25, 2506.11073) đều không có vi | Chưa biết; kết quả quyết định chọn luận điểm A hay B. Giới hạn: chỉ phủ 80 lớp COCO, và instance COCO cũng thiếu (2609.21822 tìm thêm khoảng 40% đối tượng nhỏ hoặc bị che) | 0 (36/37/38/59 đã xếp, ≈ 15) | G3, G4 |
| 3 | Thang target-policy + xếp hạng offline (cứu từ RL-1, T4, R4_01) | 7 policy (p1, cons, unf2, multiref, rnd2, **first+greedy**, fuse2), đối chứng cùng số bước p1ep4, và **LLM-fusion** của đúng 2 caption. Tính Kendall τ giữa F1 offline (target dựng từ 3 caption, chấm bằng 2 caption giữ lại) và F1 sau train | Giao thức, incremental: "xếp hạng target trước khi train, kiểm chứng bằng τ". Phải cite VBCS (2021.maiworkshop-1.6), Zheng (EMNLP'18, 1808.09564), LLaVA, FuseCap (WACV'24, 2305.17718), Bianco/Celona (2306.11593), Chen et al. (Findings EMNLP'25, 2405.00485) | Thứ tự offline: fuse2 67.7 > rnd2 65.7 > cons 62.9 > unf2 61.9 > p1 60.6 > multiref 58.9. first+greedy tách riêng phần đóng góp của consensus (offline cons − p1 = +2.3 F1). LLM-fusion dự kiến P/R ±1, CIDEr câu đầu có thể cao hơn | 10.7 (74, 75), +8.6 nếu đạt điều kiện (76) | G5, G9, G10 |
| 4 | Chẩn đoán kênh tag (cứu từ I4) | Chạy fuse2_s42 với tag giả (hoán vị có seed giữa các ảnh) và tag oracle (đối tượng trong tham chiếu, rò rỉ có chủ đích). Kết quả quyết định rẽ sang SFT có tag (79a) hay tag 112 lớp lexicon (79b) | Baseline, không phải novelty: OSCAR (ECCV'20), VinVL (CVPR'21), Tag2Text (2303.05657); ID của hai bài đầu UNVERIFIED | Tag GDINO hiện tại ở short: ΔP +2.2, ΔR −0.4, tức tag chỉ lọc chứ không thêm đối tượng. Tag đúng mà caption bỏ sót chỉ được dùng 10.5% (short) và 16.3% (detailed) (đo trong vòng). Nếu chạy 79a: R short +1–3 ở cùng P (không chắc) | 1.4 + (5.5 hoặc 1.0) | G6, G7 |
| 5 | Đánh giá công bằng độ dài và chuẩn hoá tiếng Việt (cứu từ ET2, T2, T4) | Chuẩn hoá vị trí dấu thanh (oà/uý). Extractor nhận từ ghép trước (cửa hàng, cây cầu, quả bóng…). Một quy tắc canonical chung cho CHAIR và P/R. Báo CIDEr câu đầu, CIDEr từng câu, tỉ lệ đầu ra 1 câu; định nghĩa F1 rõ ràng | Tài nguyên đánh giá, không phải novelty: Lin (2004, W04-1013), Chen et al. (1504.00325), IC3, CIDEr-R (2109.13701) | Không đổi hệ thống. ΔF1 ≤ +1.4 ở mọi hệ, thứ hạng giữ nguyên (đo trong vòng). CIDEr-D mode hai câu của fuse2 là 147.8 trên 48 đầu ra 1 câu so với 12.2 trên 510 đầu ra 2 câu (trung bình 23.9). Câu đầu của output detailed trùng output short ở 65.8% ảnh | 0 | G0 |

### 2b. Ý tưởng bị loại

| ID | Ý tưởng | Kết luận | Lý do chính | Prior art chặn |
|---|---|---|---|---|
| T1 | ABC-Fuse: committee LoRA theo "annotator" | incremental, bỏ | KTVIC không có ID annotator. Oracle với người: bỏ phiếu hạ F1 từ 68.1 xuống 60.4. Phần lợi thực chất chỉ là ensemble chung (đưa vào I1 làm ablation) | ASC 2405.13131; Gillick & Favre 2009 (W09-1802); Chen et al. WACV'21 |
| T2 | PSF: ghép thành 1 câu | incremental, bỏ | Lợi CIDEr chỉ là hiệu ứng độ dài: hậu xử lý 0 GPU đã đạt 37.4 → 100.1 (CIDEr theo âm tiết) | Marsi & Krahmer ENLG'05; Barzilay & McKeown CL'05; Cheung & Penn EMNLP'14 |
| T3 | Hiệu chỉnh PU theo propensity | lợi không đáng kể | Mức phạt bị chặn bởi λ (E5: P +1.0, R −0.8). 57% lỗi rơi vào lớp người/cảnh mà detector không phủ | PU-DPO 2608.05341; Misra CVPR'16 1512.06974; Jain KDD'16; Link 2003 |
| T4 | CoverageDial (k caption) | incremental, bỏ | fuse2 đã là một dial 2 mức lồng nhau. Mức k=3 thoái hoá (68% ảnh có T3 = T2); auto-k chọn k=1 ở 99% ảnh | Deng ECCV'20 2007.09580; Florence-2 2311.06242; CaptionSmiths 2507.01409 |
| RL-1 | ACF-RLOO, panel giữ lại | sai thiết kế | `consensual()` đọc cả panel, nên target nhớ được đạt 81.7 F1 trên panel so với 56.7 của caption thường → lặp lại E5 | SCST 1612.00563; BalCapRL 2605.07394; CCCaption 2602.21655 |
| RL-2 | PanelOPSD | incremental, bỏ | Panel 3 caption chỉ xác nhận 24.5% đối tượng mà bước greedy thêm vào, nên sẽ kéo R xuống. Cơ hội thắng multiref chỉ 15–20% | OPSD 2601.18734; DOPD 2606.30626; OP2SD 2608.09228 |
| RL-3 | FuseEdit-DPO | đã bị đi trước | Phép sửa (đổi hoặc thêm đối tượng COCO) không trùng loại mention sai theo tham chiếu phổ biến nhất của fuse2: gọi tên người 34%, cảnh 23%. Off-policy | HALVA ICLR'25 2405.18654; TL-DPO CVPR'25 2506.11417; RLHF-V 2312.00849 |
| RL-4 | Phần thưởng PU có cổng bằng chứng | đã bị đi trước | Cơ chế đã có trong RL captioning; dải "trung tính" đã được ablate | ClaimDiff-RL 2605.20278; VCap 2605.28023; CuRe 2607.05150; SENTINEL 2507.12455 |
| I2 | MIND: inventory + cổng EOS | incremental, bỏ | Lõi giải mã chính là PatchGate. Trần ở mức tập đối tượng chỉ ≈ +1–2 F1. Chặn EOS làm hỏng tính mạch lạc | PatchGate 2608.21819; SCN CVPR'17 1611.08002; 2507.20077 |
| I3 | Complement decoding | còn 1 hàng ablation | `self_fuse.py --k 2` (job 35) đã làm phần này. Recall cũng không phải nút thắt | Melas-Kyriazi EMNLP'18 (D18-1084); DBD 2406.12663; AVES-DPO 2604.24395 |
| I4 | Tự gán box (SGI) | đã bị đi trước | Nút thắt là mô hình không dùng tag (tỉ lệ dùng 10–16%), không phải nguồn tag | R-CoV 2604.20696; VGD 2607.27823; CCoT CVPR'24 2311.17076 |
| VN1 | TriPool-Gold, capture-recapture | incremental, bỏ | Không có QA của EVJVQA cho tập test. Khoảng P giữa fuse2 và P1 không co lại khi thêm tham chiếu (−9.7 đến −11.1) | Trushkowsky ICDE'13 1202.2335; Chao 1987; ViCLIP-OT 2602.22678 |
| VN2 | PoolSFT với OpenViIC | incremental, bỏ | Làm nhiễm tập test OpenViIC; giấy phép phi thương mại; lợi dự kiến dưới 1 F1 | LLaVA; SVIT 2307.04087; Ye et al. CVPR'25 2310.14356 |
| VN3 | Pivot inventory qua tiếng Anh | incremental, bỏ | Kế hoạch do chính mô hình sinh không thêm thông tin. Chỉ giữ khoảng cách en−vi trên RePOPE (job 37, miễn phí) | muPLAN EACL'24 2305.14205; Narayan TACL'21 2104.07606; CLAIM 2506.11073 |
| VN4 | Transfer chéo ngôn ngữ, XM3600 | phần lớn đã xếp | Job 36/37 đã phủ phần COCO. XM3600 chỉ có 2 tham chiếu mỗi ảnh | Berger & Ponti NAACL'25 2409.16646; Ye et al. CVPR'25 |
| EFF-1 | LoRA chọn độ sâu theo probe | incremental, bỏ | Chỉ tiết kiệm khoảng 35–40% SFT; probe không chỉ ra được lớp nào cần tune | VFL-LoRA NeurIPS'25 2509.24791; AdapterDrop 2010.11918; Hase NeurIPS'23 2301.04213 |
| EFF-2 | Seed soup, nội suy P1↔fuse2 | đã bị đi trước | Đường nội suy trùng với dây cung nối hai đầu, không tạo điểm Pareto mới. Chỉ giữ dây cung làm đường tham chiếu trong hình | Rewarded soups NeurIPS'23 2306.04488 §3.2; HallE-Control 2310.01779; Llama 3 2407.21783 |
| EFF-3 | Factorial backbone làm đóng góp | đã bị đi trước | Phân rã theo cỡ mô hình và độ phân giải đã có. Backbone 3B đã xếp hàng (57/58) | HallE-Control; Li et al. ICLR'25 2411.03312; Matryoshka MM 2405.17430 |
| EFF-4 | Giảm token thị giác khi train | không khả thi | Box COCO-80 chỉ phủ 44% đối tượng trong target, nên tiết kiệm được khoảng 6% | LoBART ACL'21 2105.03801; PyramidDrop CVPR'25 2410.17247 |
| ET1 | VeriPool | ngoài phạm vi | Cần nhãn người kiểm chứng | Open Images V4 1811.00982; LVIS 1908.03195; Kamalloo ACL'23 2305.06984 |
| ET2 | Parity công bằng độ dài, CIDEr-F2 | đã bị đi trước | CIDEr-F2 đo số câu chứ không đo chất lượng (178.9 cho đầu ra 2 câu so với 41.5 cho 1 câu). Chỉ giữ phần hygiene | Chen et al. 1504.00325 §4.2; ROUGE jackknife W04-1013; IC3 |
| ET3 | Mô hình occupancy | ngoài phạm vi | Cần mỏ neo nhãn người; kênh mẫu tự nhất quán bị vòng tròn | Miller Ecology 2011; Chambert MEE 2018; Misra 2016 |
| ET5 | POPE-vi-H từ ảo giác tự sinh | ngoài phạm vi | Cần nhãn người; RePOPE-vi (job 37) thay thế | DASH-B 2503.23573; ConBench NeurIPS'24 2405.14156 |
| bold ×6 | Set-target MRT; thưởng chéo ngôn ngữ trên Flickr30k; steering theo mention; nghiên cứu ngân sách gán nhãn; student 4B zoom; PU-RFT | chưa kiểm định | Chưa qua phản biện, nằm ngoài ngân sách 7 ngày, và vài ý phụ thuộc ý tưởng đã bị loại (T1, ET3) | — |

## 3. Storyline mới

**Tiêu đề đề xuất:** *Fuse, Don't Pick: High-Coverage Vietnamese Image Captioning from Multiple Partial References*. Nếu G3 trượt: *Fusing Human References for Vietnamese Captioning: Coverage Gains and Their Precision Cost*.

**Luận điểm A (dùng nếu G3 đạt).**
> Target SFT được ghép từ caption tham chiếu do người viết: caption đồng thuận, cộng caption thêm nhiều đối tượng mới nhất, không qua LLM. Cách này đưa object recall của Qwen2.5-VL-7B QLoRA lên ngang một caption tham chiếu ở cùng độ dài (R +5.7, F1 +4.0, CIDEr không khác có ý nghĩa; phải giữ được trên 3 seed). Ở mode hai câu, R tăng +18. Chi phí huấn luyện là 3.6 GPU-h trên một RTX 3090, và suy luận không tốn thêm. Trên ảnh COCO có nhãn instance do người gán, phần lớn mention "sai theo tham chiếu" là đối tượng có thật. Vì vậy khoảng cách còn lại tới tham chiếu người nằm ở precision, và precision tính theo tham chiếu đánh giá thấp captioner phủ rộng.

**Luận điểm B (dùng nếu G3 trượt).**
> Fusion là một núm điều chỉnh độ phủ, với chi phí precision đã được lượng hoá trên nhãn người. Ở short, fuse2 + tag cho R +5.3 tại P bằng P1. Mode hai câu đổi khoảng 10 P lấy khoảng 18 R.

| Đóng góp | Nội dung | Novelty | Bằng chứng / cổng |
|---|---|---|---|
| C1 | Recipe fusion chỉ dùng chữ người viết (trích xuất, không LLM), kèm giao thức xếp hạng target offline không rò rỉ. Giao thức được kiểm chứng bằng Kendall τ trên 7 policy, có đối chứng cùng số bước | Incremental. Khác VBCS, Zheng, LLaVA, FuseCap, Bianco/Celona ở ba điểm: giữ nguồn gốc chữ người, tiêu chí "đối tượng mới", và τ được đăng ký trước | 41/42/55/56/74/75 + multiref; G5 |
| C2 | "Precision đi đâu": parity với caption tham chiếu giữ lại; phân rã presence bằng instance COCO (UIT-ViIC trong miền, COCO transfer); RePOPE hỏi bằng tiếng Việt | Incremental; lần đầu cho tiếng Việt theo các tìm kiếm của vòng này | 36/37/38/59; G3, G4 |
| C3 | MBR mức đối tượng không cần huấn luyện (chỉ đưa vào nếu G1/G2 đạt) | Incremental | 72, 82 |
| C4 | Bộ đánh giá công bằng độ dài cho tiếng Việt: chuẩn hoá dấu thanh, extractor nhận từ ghép, CIDEr câu đầu và từng câu, tỉ lệ đầu ra 1 câu | Tài nguyên, không phải novelty | CPU |

**Không phải đóng góp (ghi rõ trong bài):**
- Baseline và ablation: P1 (3 seed), p1ep4, multiref, cons, unf2, rnd2, first+greedy, LLM-fusion, zero-shot (160/512 token, prompt `two`), P1 với prompt `two`, self-fusion k=2 (job 35), VCD, tag GDINO cùng placebo/oracle.
- Cross-fit RFT (60–63): baseline dùng phần thưởng, báo cáo dù kết quả ra sao.
- Phụ lục: E5/E5-DPO, backbone 3B (57/58), Vintern-3B zero-shot, 1024 token thị giác, beam-5, best-of-N theo log-prob.
- Phụ lục "những gì không hiệu quả": probe E2, thang gọi tên E3, GFM E4, XWit, template, relation back-off.

**Hệ chính đóng băng từ nay:** fuse2 (QLoRA r16, 512 token thị giác, 2 epoch, 3 seed). Biến thể lúc suy luận chỉ được thêm khi qua cổng: +tag (G6), +MBR (G1/G2).

Trần đo trên tham chiếu:
- Short: 1 caption so với 4 caption còn lại đạt F1 60.5; fuse2 trên cùng gold đạt 58.2.
- Hai câu: 2 caption so với 3 caption còn lại đạt 70.9; fuse2 đạt 61.5.
- Dư địa còn lại chủ yếu nằm ở P.

**Venue:** Neurocomputing là đích chính, chuyển sang Pattern Recognition nếu G3, G4 và backbone 3B cùng chiều. Không nhắm TMM/TNNLS.

## 4. Kế hoạch 7 ngày (13–19/10) trên 2 RTX 3090

### 4a. Hàng đợi đã có (không xếp lại)

| Job | Nội dung | Dùng cho |
|---|---|---|
| 26 | CLIPScore/RefCLIPScore (XLM-R ViT-H/14) và BERTScore cho mọi hệ | metric phụ, không phụ thuộc lexicon |
| 32, tags s43/s44 | tag trên p1_s43; tag trên fuse2 s43/s44 | G6, seed |
| 35 | zeroshot-two, p1_s43-two; 6 mẫu short mỗi ảnh test cho p1_s43 và fuse2_s42, rồi self_fuse k=1/k=2 | đối chứng độ dài; I1 ở short |
| 36 | COCO Karpathy (2500 ảnh): p1_s43, fuse2_s42 ở hai mode; chấm theo instance và tham chiếu | C2 |
| 37 | POPE/RePOPE bằng tiếng Việt và tiếng Anh cho zero-shot, p1_s43, fuse2_s42 | C2, khoảng cách en−vi |
| 38 | UIT-ViIC test (231 ảnh), transfer: zero-shot, p1_s43, fuse2_s42 | C2 |
| 41, 42, 55, 56 | rnd2, unf2, cons, p1ep4 (s42) | C1, G5 |
| 57, 58 | P1, fuse2 trên Qwen2.5-VL-3B | backbone 2, Pareto hiệu năng |
| 59a/b | UIT-ViIC trong miền, P1 so với fuse2, test 231 + val 924, có instance COCO | G3, G4 |
| 60–63 | cross-fit: fuse2_A/B train trên từng nửa, lấy 6 mẫu detailed trên nửa chưa thấy, chọn best-of-6, train lại | baseline reward; tập dev cho I1 |
| khác | P1 s44 (đã về), fuse2 s43/s44, multiref s42, pilot pipeline cũ | seed, thang target |

### 4b. Code và việc CPU cần làm trước (ngày 0–1)

| Mã | File | Thay đổi | ~dòng | Cho |
|---|---|---|---|---|
| C-1 | `rescap/vi/normalize.py` (mới), `rescap/chair.py` | NFC; đặt dấu thanh kiểu mới (oà, oá, uý…). Khoá từ ghép được nhận trước (cửa hàng, cửa sổ, cầu thang, cây cầu, quả bóng, bàn tay, bóng râm, xe hơi/xe ô tô → ô tô, heo → lợn, trái cây, hoa quả). Có selftest | 60 | mọi số |
| C-2 | `scripts/object_prf.py` | `canonical()` như CHAIR-vi; `--exclude` (dedup-543); bootstrap 2 tầng `--seeds`; in thêm R vi mô | 40 | §5 |
| C-3 | `scripts/metrics_v2.py` | `cider --prefix` (câu đầu; 12 âm tiết đầu), `--per-sentence`, tỉ lệ đầu ra 1 câu | 30 | C4 |
| C-4 | `scripts/mbr_select.py` (mới) | utility `pairwise` / `union` / `consensus`; `--lam`; `--greedy FILE` (thêm output greedy vào tập ứng viên); `--pool` (gộp preds của nhiều hệ để làm tổ hợp hệ thống); `--objects ktvic\|coco80`; `--pick logprob` (best-of-N); `--dev` chấm theo tham chiếu train; selftest | 90 | I1 |
| C-5 | `scripts/e5_sample.py` | `--greedy` (do_sample=False, n=1); `--logprob` (log-prob trung bình mỗi mẫu qua `compute_transition_scores`) | 12 | 72, 82 |
| C-6 | `scripts/evaluate.py` | `--num-beams`; `--blank-image` (ảnh xám cùng kích thước) | 6 | 72, 83 |
| C-7 | `scripts/build_gold_sft.py` | `--fuse-base consensus\|first`, thêm vào `_check()` | 6 | 74 |
| C-8 | `scripts/human_parity.py` | thêm policy `ffuse2` vào `offline` | 5 | G5 |
| C-9 | `scripts/make_tag_controls.py` (mới) | placebo: hoán vị tag có seed, không ảnh nào giữ tag của chính nó; oracle: đối tượng trong tham chiếu | 25 | 71 |
| C-10 | `scripts/llm_fuse.py` (mới) | LLM mở, chỉ văn bản, gộp 2 câu thành 1. Lint nguồn gốc: tập đối tượng đầu ra phải bằng hợp đối tượng của 2 câu nguồn; trượt thì giữ bản nối. Ghi tỉ lệ fallback | 50 | 75 |
| C-11 | `scripts/target_lint.py` | thêm mẫu "nhắc lại cùng đối tượng ở câu 2" và "số đếm mâu thuẫn" | 6 | M10 |
| C-12 | có điều kiện | `build_gold_sft --tags/--tag-rate` (79a); `tag_images --vocab` + `data/coco_probe/ktvic112_en.json` (79b); `train_stage2 --mask-fix` (77); nhánh Vintern trong `evaluate.py` (78) | 10–30 mỗi việc | P3 |

### 4c. Job GPU mới

Đặt tên từ 70 trở lên. `qrun.sh` chạy theo thứ tự tên, nên các job này chạy sau hàng đợi hiện tại. Trước khi xếp, kiểm tra `/root/queue` để không trùng số. Lệnh phác thảo nằm ở khối ngay sau bảng.

| Job | Mục đích | Code | Phụ thuộc | GPU-h | Ưu tiên |
|---|---|---|---|---|---|
| 70_zs512 | Zero-shot detailed với 512 token (280/558 caption hiện bị cắt ở 160). VCD (285/558 bị cắt): chỉ chấm câu hoàn chỉnh, làm trên CPU | – | – | 1.3 | P1 |
| 71_tagctrl_fuse2 | Tag placebo và oracle trên fuse2_s42, hai mode | C-9 | – | 1.4 | P1 |
| 72_mbr_samples | Dev: 6 mẫu short và greedy short/detailed trên nửa chưa thấy (mẫu detailed lấy từ job 62). Test: 6 mẫu detailed, 6 mẫu short (seed 43) có log-prob, beam-5 | C-5, C-6 | 60, 61 | 4.5 | P1 |
| 73_vt1024 | fuse2_s42 và p1_s43 với 1024 token thị giác, hai mode | – | – | 1.6 | P2 |
| 74_ladder_ffuse2_s42 | first + greedy (tách riêng phần consensus) | C-7 | – | 4.7 | P1 |
| 75_llmfuse_s42 | LLM-fusion của đúng 2 caption, sau đó SFT; eval short/detailed/two | C-10 | – | 6.0 | P2 |
| 76_rnd2_s43_s44 | thêm seed cho rnd2 | – | 41; G10 | 8.6 | có điều kiện |
| 77_maskfix_fuse2_s42 | kiểm tra lỗi mask prompt (VLCollator) | C-12 | – | 4.3 | P3 |
| 78_vintern3b_zs | Vintern-3B zero-shot, hai mode | C-12 | – | 0.8 | P3 |
| 79a_tagsft_fuse2_s42 | SFT có tag (50% số dòng), eval có và không có tag | C-12 | 71; G6 | 5.5 | có điều kiện |
| 79b_tags112 | Tag GDINO theo 112 lớp lexicon, eval fuse2_s42 | C-12 | 71; G6 | 1.0 | có điều kiện |
| 81_cost | Latency/VRAM cho P1, fuse2, fuse2+tag (cộng thời gian GDINO), MBR | – | – | 0.5 | P2 |
| 82_mbr_uitviic | 6 mẫu có log-prob trên UIT-ViIC test+val từ uitviic_fuse2_s42, rồi MBR và chấm theo instance | C-4, C-5 | 59b | 1.9 | P1 |
| 83_noimage_fuse2 | fuse2_s42 trên ảnh xám, hai mode (đối chứng tiên nghiệm ngôn ngữ, R2-W3) | C-6 | – | 0.3 | P2 |
| 80_cpu | CPU trên máy GPU (RDRSegmenter cần JDK): chấm lại mọi hệ sau C-1/C-2; CIDEr câu đầu/từng câu; parity; τ; bootstrap 2 tầng; target_lint | C-1–C-3, C-8, C-11 | cập nhật theo kết quả | 0 | luôn chạy |

```bash
# Đầu mỗi job như các job 35–59: cd /root/vsps && . .venv/bin/activate && export NCS_DATA=/root/ncs-data JAVA_HOME=...; set -e
E="python scripts/evaluate.py --model qwen2.5-vl-7b --split test_data.json"; RUN=$NCS_DATA/runs; R=$NCS_DATA/results; X=$NCS_DATA/xfit; S=$NCS_DATA/samples
# 70
$E --prompt detailed --max-new-tokens 512 --name zeroshot512-detailed
# 71
python scripts/make_tag_controls.py --tags $R/tags_gdino.json --placebo $NCS_DATA/tags_placebo.json --oracle $NCS_DATA/tags_oracle.json
for t in placebo oracle; do for p in short detailed; do $E --adapter $RUN/fuse2_s42 --prompt $p --tags $NCS_DATA/tags_$t.json --name tag${t}_fuse2_s42-$p; done; done
# 72 (--limit 750 + seed 42 mặc định chọn lại đúng 750 ảnh mà job 62 đã chọn)
for h in A:B B:A; do m=${h%:*}; o=${h#*:}
  python scripts/e5_sample.py --adapter $RUN/fuse2_$m --images-file $X/$o.txt --limit 750 --prompt short --n 6 --logprob --out $X/samples_${m}on${o}-short.jsonl
  for p in short detailed; do python scripts/e5_sample.py --adapter $RUN/fuse2_$m --images-file $X/$o.txt --limit 750 --prompt $p --greedy --out $X/greedy_${m}on${o}-$p.jsonl; done; done
python scripts/e5_sample.py --adapter $RUN/fuse2_s42 --split test_data.json --limit 0 --prompt detailed --n 6 --logprob --out $S/fuse2_s42-test-detailed.jsonl
python scripts/e5_sample.py --adapter $RUN/fuse2_s42 --split test_data.json --limit 0 --prompt short --n 6 --seed 43 --logprob --out $S/fuse2_s42-test-short-s43.jsonl
for p in short detailed; do $E --adapter $RUN/fuse2_s42 --prompt $p --num-beams 5 --name fuse2_s42beam5-$p; done
# 73
for m in fuse2_s42 p1_s43; do for p in short detailed; do $E --adapter $RUN/$m --prompt $p --max-vision-tokens 1024 --name ${m}vt1024-$p; done; done
# 74 (75 giống hệt, thay bước build bằng: python scripts/llm_fuse.py --sft $NCS_DATA/gold_fuse2/sft.jsonl --model Qwen/Qwen2.5-7B-Instruct --out $NCS_DATA/gold_llmfuse)
python scripts/build_gold_sft.py --annotations $NCS_DATA/datasets/ktvic/train_data.json --out $NCS_DATA/gold_ffuse2 --select first --fuse 2 --fuse-base first
python scripts/train_stage2.py --stage sft --data $NCS_DATA/gold_ffuse2 --out $RUN/ffuse2_s42 --epochs 2 --seed 42
for p in short detailed two; do $E --adapter $RUN/ffuse2_s42 --prompt $p --name ffuse2_s42-$p; done
# 76 (chỉ khi G10)
for s in 43 44; do python scripts/train_stage2.py --stage sft --data $NCS_DATA/gold_rnd2 --out $RUN/rnd2_s$s --epochs 2 --seed $s; for p in detailed short; do $E --adapter $RUN/rnd2_s$s --prompt $p --name rnd2_s$s-$p; done; done
# 77 / 78 (P3)
python scripts/train_stage2.py --stage sft --data $NCS_DATA/gold_fuse2 --out $RUN/fuse2mf_s42 --epochs 2 --seed 42 --mask-fix   # rồi eval hai mode
for p in short detailed; do python scripts/evaluate.py --model vintern-3b --split test_data.json --prompt $p --name vintern3b-$p; done
# 79a (G6b trượt) / 79b (G6b đạt)
python scripts/tag_images.py --split train_data.json --out $NCS_DATA/tags_gdino_train.json && python scripts/build_gold_sft.py --annotations $NCS_DATA/datasets/ktvic/train_data.json --out $NCS_DATA/gold_fuse2tag --select consensus --fuse 2 --tags $NCS_DATA/tags_gdino_train.json --tag-rate 0.5   # rồi SFT, eval có/không --tags
python scripts/tag_images.py --split test_data.json --vocab data/coco_probe/ktvic112_en.json --out $R/tags_lex112.json   # rồi $E --adapter $RUN/fuse2_s42 --tags $R/tags_lex112.json
# 81
for a in p1_s43 fuse2_s42; do python scripts/measure_latency.py --adapter $RUN/$a --max-vision-tokens 512 --n 60 --out $R/latency_$a.json; done
# 82 (máy giữ uitviic_fuse2_s42)
export NCS_DATASET=uitviic; for s in test val; do for p in short detailed; do python scripts/e5_sample.py --adapter $RUN/uitviic_fuse2_s42 --split ${s}_data.json --limit 0 --prompt $p --n 6 --logprob --out $S/uitviic_fuse2_s42-$s-$p.jsonl; done; done
# 83
for p in short detailed; do $E --adapter $RUN/fuse2_s42 --prompt $p --blank-image --name fuse2_s42blank-$p; done
# 80 (CPU, ví dụ)
python scripts/mbr_select.py $S/fuse2_s42-test-detailed.jsonl --greedy $R/fuse2_s42-detailed.preds.json --utility union --lam 0 --out $R/fuse2_s42mbr-detailed.preds.json
python scripts/object_prf.py --results $R --ci --mode detailed --vs fuse2_s42 --exclude data/dedup/ktvic_dup_train_test.json
```

Ngân sách GPU-h mới:
- Cốt lõi (70–75, 81–83): 22.2.
- Có điều kiện (76, 79): ≤ 14.1.
- P3 (77, 78): 5.1.

Mỗi job ≤ 8.6 GPU-h và vừa một 3090 (QLoRA 4-bit; suy luận bf16 như các job đã chạy). Job phụ thuộc phải chạy trên máy đang giữ adapter đầu vào: 72 cùng máy với 60/61, 82 cùng máy với 59b.

### 4d. Lịch

| Ngày | n2 | n3 | CPU / quyết định |
|---|---|---|---|
| 0 (12–13/10) | Làm C-1 đến C-11 kèm selftest, commit, scp lên máy. Xếp 70, 71, 73, 75 | Xếp 74, 81, 83 | Commit file cổng (§4e) trước mọi số mới (G0). Chấm lại các hệ đã có bằng C-1/C-2, báo cả trước lẫn sau |
| 1 (13/10) | hàng đợi hiện có, theo thứ tự tên (35–42; 36–38 ở máy đang giữ chúng) | 55 → 56 → 57/58 → 59a/b | CIDEr câu đầu và từng câu; target_lint; parity |
| 2 (14/10) | 60–63 → 70, 71, 73 | 59 xong → 82; 74 | G3/G4 (từ 36/38/59); G6 (từ 71), chọn 79a hay 79b |
| 3 (15/10) | 72 → 75 | 81; 79a hoặc 79b | G1 trên dev, đóng băng cấu hình I1, rồi G2 trên test |
| 4 (16/10) | 76 (nếu G10) | 77, 78 (P3, nếu máy rảnh) | G2b (từ 82); G9 (từ 75) |
| 5 (17/10) | seed còn lại về | – | Bootstrap 2 tầng seed×ảnh, hiệu chỉnh Holm; τ cuối cùng (G5); G11 |
| 6–7 (18–19/10) | để trống, dự phòng chạy lại | để trống | Đóng băng bảng và hình (Pareto P–R với đường iso-F1, trần tham chiếu, dây cung P1↔fuse2); viết bài; chọn venue theo kết quả các cổng |

### 4e. Cổng dừng (đăng ký trước; commit cùng file này)

| Cổng | Phép đo | Đạt nếu | Đạt → / Trượt → |
|---|---|---|---|
| G0 | Code chuẩn hoá (C-1/C-2) và file cổng | commit trước khi có kết quả của các job 70+ | bắt buộc |
| G1 | I1 trên dev: 1500 ảnh cross-fit chưa thấy, 5 tham chiếu train, paired bootstrap với greedy của cùng adapter nửa | Hai câu: ΔF1 ≥ +1.0, CI_low > 0, ΔP ≥ −1.0. Short: ΔF1 ≥ +0.5, ΔP ≥ −1.0. Utility ∈ {pairwise, union}, λ ∈ {0, 0.1} chỉ chọn trên dev | đóng băng cấu hình / I1 chuyển thành null trong phụ lục |
| G2 | I1 trên test so với fuse2_s42 greedy | CI_low(ΔF1) > 0 ở mode hai câu, và vượt self_fuse k=1 (35), beam-5 và best-of-6 theo log-prob ít nhất +0.5 F1 | giữ C3 / chỉ để làm ablation |
| G2b | I1 trên UIT-ViIC test+val (82) | ΔP theo gold tham chiếu ∪ instance ≥ −1.0 và ΔR theo instance ≥ 0 | được claim "R tăng không phải ảo giác" / chỉ claim lợi trên metric tham chiếu |
| G3 | Presence, UIT-ViIC test+val (59), fuse2 so với P1, mention thuộc COCO-80 | ≥ 50% mention sai theo tham chiếu của fuse2 có instance, **và** CI_low của ΔP theo gold tham chiếu ∪ instance ≥ −3.0 (mode hai câu). COCO transfer (36) cùng chiều thì dùng làm bằng chứng phụ | luận điểm A / luận điểm B |
| G4 | Tính tổng quát (59, 57/58) | UIT-ViIC: ΔR short > 0 với CI không chứa 0 và ΔF1 ≥ 0 trên cả test lẫn val. Backbone 3B: ΔF1 short > 0 | claim tính tổng quát / giới hạn claim ở KTVIC và 7B |
| G5 | Kendall τ_b giữa F1 offline và F1 sau train, 7 policy | τ_b ≥ 0.71 (≤ 3 cặp đảo trên 21) | claim giao thức C1 / thang chỉ còn là ablation |
| G6 | Tag (71) so với không tag | (a) ΔP của placebo ≥ 0.7 × ΔP của GDINO thì lợi P của tag chỉ là hiệu ứng prompt. (b) ΔR short của oracle < +3.0 thì mô hình không dùng được kênh tag | (a) bỏ claim "tag giúp grounding"; (b) chạy 79a, ngược lại chạy 79b |
| G7 | 79a so với fuse2+tag GDINO | ΔR short ≥ +2.0 ở ΔP ≥ −1.0, và F1 khi không có tag nằm trong ±1 | giữ làm biến thể / bỏ |
| G8 | 1024 token (73) | ΔR ≥ +1.5 ở ΔP ≥ −1.0 | ghi "recall bị chặn bởi độ phân giải" / ghi "512 token không phải nút thắt" |
| G9 | LLM-fusion (75) | Không dừng. Nếu ΔF1 trong ±1, ΔCHAIR_i ≤ +1 và ≥ 95% đầu ra qua lint | bán fusion bằng chữ người như phương án **rẻ hơn**, không bán là tốt hơn / ngược lại thì dùng làm bằng chứng cho việc giữ nguồn gốc |
| G10 | rnd2_s42 so với fuse2_s42 ở mode hai câu | \|ΔF1\| < 1.5 | chạy 76 / bỏ 76 |
| G11 | mask-fix (77) | \|ΔF1\| ≤ 1.0 ở hai mode và \|ΔCIDEr\| ≤ 5 ở short | chỉ công bố trong bài / chạy lại P1 và fuse2 s42 với bản sửa (khoảng 8.6 GPU-h) |

## 5. Trả lời các điểm yếu fatal và major của reviewer

| # | Điểm yếu (reviewer) | Mức | Xử lý | Chi phí |
|---|---|---|---|---|
| 1 | Presence chỉ dựa AI-silver (R1, R2, R3) | F | Bỏ AI-silver khỏi bài. Đo presence bằng nhãn người có sẵn: UIT-ViIC + instance COCO (59), COCO Karpathy (36), RePOPE-vi (37). Với KTVIC chỉ báo P theo tham chiếu cùng parity. Ghi giới hạn: chỉ 80 lớp COCO, instance gold cũng thiếu (2609.21822). Không gán nhãn mới; kit 101 ô gác lại, nên lỗi thiết kế mà R2-W12 chỉ ra không còn áp dụng | 0 GPU-h mới (≈ 15 đã xếp) |
| 2 | Novelty mỏng (R1, R3) | F | Định vị lại thành phân tích + recipe (§3). Cite LLaVA, FuseCap, Bianco/Celona, IC3, VBCS, Zheng, Chen 2405.00485, GBC 2407.06723 (venue UNVERIFIED), CCCaption. Bỏ mọi chữ "first" | viết |
| 3 | P1 và fuse2 khác nhau ở nhiều biến (R1, R2, R3) | F | Thang đối chứng cùng số bước: p1ep4, cons, unf2, rnd2, multiref, first+greedy, LLM-fusion. Báo số bước tối ưu của mọi run | 10.7 |
| 4 | Headline "detailed" không cùng độ dài (R2; R1, R3) | F | Đổi tên thành "mode hai câu". Đối chứng độ dài: zeroshot-two, p1_s43-two, self-fusion k=2 (35), unf2/cons/p1ep4-two. Vẽ P–R theo số đối tượng mỗi caption, có iso-F1 và trần tham chiếu | 0 mới |
| 4b | Gold tham chiếu đo mức đáng nhắc; thiếu sàn và đối chứng (R2-W3) | M | Báo sàn của caption hằng (5 lớp phổ biến nhất: F1 29.6), đối chứng ảnh xám (83), P khi gộp các lớp người, trần tham chiếu với số tham chiếu khớp (R4_01). Phân rã FP chỉ dựa trên văn bản: gọi tên người 20%, mơ hồ hơn gold 7%, lỗi extractor 5% (đo trong vòng) | 0.3 |
| 5 | Metric và target dùng chung lexicon (R1, R3) | M | rnd2 (caption ghép thêm không chọn theo lexicon); instance COCO (matcher COCO-80 khác lexicon 113 mục); CLIPScore/BERTScore P/R (26). Tuỳ chọn: khớp cụm danh từ ngoài lexicon bằng VnCoreNLP | CPU |
| 6 | Chỉ 1 seed (R1, R2, R3) | M | P1 đã đủ 3 seed; fuse2 s43/s44 đã xếp. Báo mean ± sd, bootstrap 2 tầng, Holm. Ghi rõ LoRA init không theo seed (`set_seed` chạy sau `get_peft_model`) | 0–8.6 |
| 7 | 1 dataset, 1 backbone (R1, R2, R3) | M | UIT-ViIC trong miền và transfer, COCO, Qwen2.5-VL-3B (đều đã xếp). Vintern-3B zero-shot (78). Qwen3-VL-8B để ngỏ vì cần venv transformers ≥ 4.57 | 0.8 |
| 8 | Over-claim (R1, R2) | M | Bỏ "no trade-off", "giảm ảo giác", "detailed captioning". Kiểm định kép đăng ký trước trên gold tham chiếu ∪ instance (G3) | 0 |
| 9 | Không có đánh giá người cho hệ mới (R1, R2, R3) | M | **Không làm** (quyết định 12/10), ghi là giới hạn. CLIPScore/BERTScore chỉ là metric phụ vì chưa được kiểm định cho tiếng Việt (2502.06600). Rủi ro reviewer: **cao**. Nếu tác giả đổi ý, việc đáng làm nhất là so sánh từng cặp kiểu THumB (NAACL'22, 2111.08940) | 0 |
| 10 | Không đo faithfulness ngoài đối tượng (R1, R2) | M | Audit target ghép bằng CPU (C-11); RePOPE-vi. FaithScore-vi để ngỏ vì cần kiểm định bằng người | CPU |
| 11 | Dùng CIDEr sai ở mode hai câu (R2) | M | Không xếp hạng bằng CIDEr-D hay CIDEr-noLP. Báo CIDEr câu đầu, CIDEr từng câu và tỉ lệ đầu ra 1 câu | CPU |
| 12 | Extractor và chuẩn hoá chưa được kiểm (R2) | M | C-1/C-2; công bố lexicon; báo số trước và sau khi sửa (ΔF1 ≤ 1.4, thứ hạng giữ nguyên) | CPU |
| 13 | Thống kê yếu, dùng lại tập test (R1, R2, R3) | M | Định nghĩa F1 (P vi mô, R vĩ mô) và in thêm bản vi mô; F1_spec là metric phụ. Kiểm định paired, hiệu chỉnh Holm. Mọi lựa chọn làm trên nửa cross-fit; UIT-ViIC val không dùng để chọn; báo thêm dedup-543 | CPU |
| 14 | Thiếu benchmark ảo giác chuẩn (R2, R3) | M | RePOPE-vi (37) và CHAIR theo instance COCO (36): cần cả đo yes/no lẫn tự do theo THRONE (CVPR'24, 2405.05256) | 0 mới |
| 15 | Baseline bị cắt ở 160 token (R2) | M | Job 70; VCD chỉ chấm câu hoàn chỉnh | 1.3 |
| 16 | Baseline yếu, thiếu RL và PatchGate (R1, R3) | M | Cross-fit RFT (60–63) là baseline reward, báo dù kết quả ra sao. PatchGate: viết phần thảo luận định vị (từ vựng 1 token của nó không biểu diễn được 54/112 tên nhiều âm tiết); tái hiện thì để ngỏ | 0 |
| 17 | Thiếu framing parity (R3) | M | Đã có (R4_01). Đổi "1 người" thành "1 caption tham chiếu", ghi nghi vấn mỗi ảnh do một người viết | CPU |
| 18 | Hiệu năng, quan hệ với bài FAIR, kết quả âm, sao chép nguyên văn (m) | m | Bảng chi phí (81), so với 88 GPU-h của stage-1 VSPS. VSPS chỉ còn 1 hàng. Kết quả âm đưa vào phụ lục. Báo tỉ lệ caption trùng nguyên văn với train, distinct-n và dedup-543 | 0.5 |

## 6. Không được claim, không được làm

- Không viết "đầu tiên ghép caption", "không đánh đổi", "giảm ảo giác" hay "detailed captioning". Các khẳng định về ảo giác chỉ dựa trên G3 và gold instance.
- Không viết "5 annotator độc lập" hay "parity với con người". Viết "5 caption tham chiếu" và "parity với một caption tham chiếu giữ lại".
- Không dùng AI-silver làm bằng chứng, kể cả dưới dạng một hàng "LLM so với người", vì không có gold người để so.
- Không giữ khung LSC "định danh được nhờ 5 người gán". Theo Link (2003, Biometrics 59:1123) thì không định danh được. Bỏ khung này khỏi 06_PHUONG_PHAP.
- Không gọi probe E2 là bộ phát hiện tồn tại, vì nhãn của nó là "có người nhắc". Không claim "mô hình biết nhiều hơn nó nói" (PatchGate 2608.21819; 2508.04567).
- Không trình bày CIDEr-noLP như thước đo chất lượng. Không claim multilingual CLIPScore đã được kiểm định cho tiếng Việt. Không gọi instance COCO là gold đầy đủ.
- Không claim loss chỉ tính trên token trả lời. Thực tế VLCollator lấy độ dài prompt từ template chưa mở rộng token ảnh, nên câu lệnh và header assistant vẫn nằm trong loss. Lỗi này như nhau ở mọi hệ: công bố trong bài, kiểm bằng 77, không sửa giữa thang.
- Không claim seed thay đổi LoRA init.
- Không chỉnh thêm gì trên 558 ảnh test. Không dùng UIT-ViIC val để chọn. Không dùng OpenViIC để train: 401/558 ảnh test KTVIC trùng gần với ảnh train OpenViIC (2602.22678).
- Không kiểm định ý nghĩa với số GRIT chép từ bài khác. Không claim hai GPU. Không đưa API trả phí vào phương pháp.
- Không mở lại các hướng đã null (E5 trên ảnh đã thấy, DPO với cặp chỉ có prompt detailed, thang gọi tên, GFM, XWit, template).
- Không lưu và không dùng mật khẩu root đã dán trong yêu cầu. Đổi mật khẩu root trên n3 và chỉ dùng SSH key. Agent không SSH vào máy GPU trong vòng này.
