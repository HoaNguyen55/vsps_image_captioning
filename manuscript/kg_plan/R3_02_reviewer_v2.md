# R3_02. Mô phỏng phản biện bản v2 (P1: 2 reviewer EMNLP-ARR; P2: 2 reviewer IP&M/TOMM + 1 reviewer ACM MM) và kiểm tra nhất quán nội bộ

Critic 02, vòng 3, ngày 2026-10-10. Đối tượng: `00_KE_HOACH.md` (v2). Tôi tự đánh giá trước, sau đó mới đối chiếu `R2_04`, `R2_05`, `R2_06`. Ngoài plan, tôi đọc thêm kế hoạch P0 đang chạy trong repo, `.paper_work/KE_HOACH_Q2.md`. v2 không nhắc tới file này, nhưng nó quyết định câu trả lời cho câu hỏi salami.

**Nguồn đã mở trong vòng này** (ẩn danh, không có email):
- arXiv API: 2502.19110 (CLC, comment trống, nên venue chưa xác minh), 2609.35294 (SCAPO, "Beyond Saying Less", 2026-09-28), 2604.01460 ("Accepted by COLM 2026"), 2205.12522 (XM3600, "EMNLP 2022"), 2603.03197 (SpeciaRL, "Accepted at CVPR 2026"), 2604.05623 (DetailVerifyBench), 2503.00436 (HalCECE), 2305.04166 (UIT-OpenViIC).
- Toàn văn PDF: XM3600 (§3 human evaluation; tiếng Việt nằm trong nhóm L_EXT) và Vintern-1B 2408.12480 (Bảng 1, dữ liệu fine-tune).
- File trong repo: `.paper_work/KE_HOACH_Q2.md`.

---

## 1. Kết luận theo từng thành phần

| Thành phần v2 | Kết luận | Lý do ngắn |
|---|---|---|
| §6 Bảng phân đóng góp (chống salami) | **fail** | Bảng mâu thuẫn với kế hoạch P0 đang chạy (`KE_HOACH_Q2.md`). P0 hiện vẫn chứa lùi IsA cho thực thể (D3), lùi quan hệ về thực thể (D2), box và hình học (B3/C4), hội đồng verifier có ngưỡng hiệu chỉnh (C1/C3), gold object 300 ảnh (B1) và metric cấp mệnh đề do người chấm (B2). Bảng cũng bỏ sót tầng FAIR 2026 |
| §2 ViHG-Cap (lõi P2) | needs-fix | Claim đã hẹp lại đúng hướng. Nhưng cổng G-P2 không kiểm tra đúng phần khác biệt, và baseline HALVA/RLAIF-V trên tiếng Việt chưa có cách làm cụ thể |
| §3 M1 ViVG-P/R | **fail** (với vai trò metric) | Precision trộn tỷ lệ đúng do người ước lượng ở cấp hệ vào điểm cấp caption. Như vậy τ_c cấp caption (T4) không có nghĩa, và M1 không còn là metric tự động |
| §3 Meta-eval A | needs-fix | Chỉ 4 hệ, nên tương quan cấp hệ vô nghĩa. Phần phát hành được (XM3600) lại không có gold SG |
| §4 Dữ liệu | needs-fix | Ảnh audit T0.5 lấy từ ảnh test KTVIC; Vintern có thể đã thấy ảnh UIT |
| §5 Cổng | needs-fix | G-P2 dùng M1 trước khi T4 kiểm M1. G-P2 so với một baseline mà VSPS vốn đã thắng |
| §8 Giờ công, GPU | **fail** (nhất quán) | Số 515–760 GPU-h và ~200 giờ chưa tính lại sau khi phạm vi đổi, và không tính phần việc của P0 |
| §9 Lộ trình | needs-fix | Nhánh ACM MM không có ô thời gian để viết. Hai bản nâng cấp verifier khác nhau cùng chạy trong 11/2026 |
| §0 B8 (XM3600) | pass | Đã xác minh: XM3600 §3 có chấm người side-by-side trên 600 ảnh (XM600), 3 người chấm, thang 7 mức; tiếng Việt thuộc nhóm L_EXT. Không công bố dạng điểm từng caption |
| §0 B10 (dedup), B11 (T0.5) | pass | Đúng hướng, rẻ, có cổng |

---

## 2. Mô phỏng reviewer

### P1, EMNLP 2027 (ARR): "ViSG: Vietnamese verification-aware scene-graph resources and specificity-aware graph metrics for captioning"

#### R-A. Reviewer track tài nguyên / đa ngôn ngữ

**Tóm tắt.** Bài có gold SG tiếng Việt cho khoảng 400 ảnh đã dedup (dev 80 / test 320), gán mù verdict máy, có đo anchoring. Bài có thêm bộ chấm điểm người ở cấp caption và cấp mệnh đề (4 hệ, 2 người chấm, 100–150 ảnh XM3600 có thể phát hành), một parser luật/ViT5, và M1 (P/R + điểm độ cụ thể) cùng H-R.

**Điểm mạnh.**
1. Dedup all-vs-all và tập test sạch. Đây là đóng góp thật cho cộng đồng KTVIC/OpenViIC, vì ViCLIP-OT mới chỉ đo một chiều.
2. Gold mù verdict, đo anchoring trên 100 ảnh, gán đôi 25%.
3. Nối với XM3600: có điểm neo quốc tế, và có thể phát hành.

**Điểm yếu.**
1. **M1 không phải metric tự động.** Mỗi hệ mới cần người kiểm 50+50 claim (§3). Một bài metric ở EMNLP mà mỗi lần chấm lại cần người là bài giao thức đánh giá, không phải bài metric.
2. **Phần phát hành được không chạy được metric chính.** 100–150 ảnh XM3600 chỉ nằm trong meta-eval, không có gold SG (§4 chỉ gán SG cho ViSG-test). Nếu xin phép KTVIC/EVJVQA/OpenViIC thất bại, người đọc không tái lập được M1/H-R trên bất kỳ ảnh nào.
3. **Quy mô nhỏ.** Test 320 ảnh, so với DetailVerifyBench (1.000 ảnh, gán mức token, arXiv 2604.05623) và HalDec-Bench. Bài phải nói rõ vì sao 320 ảnh là đủ (bằng power analysis hoặc độ rộng CI của từng metric).
4. **Tính mới của metric.** PoSh, DSG, Taxonomy-Aware Eval, DetailVerifyBench. Phần mới là tiếng Việt, gold có trạng thái và điểm độ cụ thể. Điều này ổn cho Findings, khó cho main.

**Câu hỏi.** Bộ chấm điểm người có công bố điểm từng caption không? Có so với chấm side-by-side kiểu XM3600 trên cùng ảnh XM600 không?

**Điểm (ARR).** Soundness 2,5 · Excitement 2,5 · **Overall 2,5** (Findings, sát biên). Lên 3,5 nếu: M1 tự động hoàn toàn; gold SG có trên phần XM3600 phát hành được; meta-eval có ≥ 8 hệ.

#### R-B. Reviewer chuyên meta-evaluation

**Tóm tắt.** Như R-A.

**Điểm mạnh.** Đóng băng ứng viên trước (15/11) và loại ViHG-Cap khỏi meta-eval, tức là không có vòng lặp tự phục vụ. Dùng τ_c, bootstrap, và báo lại sau khi bỏ VSPS.

**Điểm yếu.**
1. **M1-P cấp caption bị ô nhiễm.** Phần "ước lượng tỷ lệ đúng của claim khớp UNCERTAIN-gold và claim không khớp" là một tỷ lệ của cả hệ (từ 50+50 claim). Đem tỷ lệ này gán cho từng caption làm mọi caption của cùng hệ bị kéo về trung bình của hệ, nên τ_c cấp caption phản ánh hệ, không phản ánh caption. So M1 (có người trong vòng lặp) với VLM-judge (hoàn toàn tự động) ở T4 cũng không công bằng.
2. **4 hệ thì tương quan cấp hệ không kiểm được.** Kendall với n = 4 chỉ có 24 hoán vị; ngoài trường hợp đúng hoàn toàn, không đạt ý nghĩa thống kê. Hai trong bốn hệ (Qwen zero-shot, VSPS-SFT) cùng họ Qwen, và một hệ là tham chiếu người.
3. **Điểm độ cụ thể = độ sâu IsA trong Wikidata** không so được giữa các nhánh. Độ sâu của "chó poodle" và của "nón lá" phụ thuộc cách Wikidata mô hình hóa, không phụ thuộc độ cụ thể nhận thức.
4. Danh sách "từ rỗng" được đặt tay (§3), dễ bị xem là tùy tiện. Cần báo độ nhạy theo danh sách.

**Điểm (ARR).** Soundness 2 · Excitement 2,5 · **Overall 2,5**. Lên 3,5 nếu sửa điểm 1–2 (F2, F5 bên dưới).

### P2, IP&M SI "Multilingual and Multimodal … Low Resource" / ACM TOMM: "ViHG-Cap: KG-structured hierarchical back-off for faithful Vietnamese captioning"

#### R-C. IP&M, reviewer xử lý thông tin / NLP ít tài nguyên

**Tóm tắt.** Bài lấy mệnh đề đã kiểm chứng của VSPS [P0]. Node/cạnh UNCERTAIN được lùi theo IsA (Wikidata + bảng tay) và theo thang vị từ, sau đó SFT graph-then-caption và preference cục bộ (GEPA). Baseline chính là VSPS chỉ đổi toán tử lùi, cộng viết-lại-CLC và lùi-sau-sinh.

**Điểm mạnh.** Bảng đối đầu với VSPS chỉ đổi một biến; baseline CLC kiểm giá trị của KG; báo số claim đúng/caption và H-R để chống "nói ít đi" (SCAPO 2609.35294).

**Điểm yếu.**
1. **Tự trùng với P0.** Kế hoạch P0 công khai trong repo (`KE_HOACH_Q2.md` D3) có "lùi loài/kiểu về nhóm cha (`chó poodle` → `con chó`)", "đếm trên 5 → `nhiều`", "`xanh dương`/`xanh lá` → `xanh`", và D2 "relation → entity". Nếu bản TALLIP ra trước với các mục này, phần khác biệt của P2 chỉ còn nấc vị từ trung gian và nguồn IsA từ Wikidata.
2. **KG nhỏ.** Gồm Wikidata subset, bảng ~250 dòng và ≤100 thực thể văn hóa. Reviewer IP&M sẽ chấp nhận nếu bài thắng CLC; nếu không thắng thì chữ "KG" trong tiêu đề là nói quá.
3. **Liên quan còn thiếu.** HalCECE (2503.00436): "semantically minimal edits driven by hierarchical knowledge" trên caption, tức là cùng miền, khác mục đích (phát hiện, không sinh). Còn thiếu cả Mohri & Hashimoto 2402.10978 và HallE-Control 2310.01779. R2-01 đã yêu cầu trích, nhưng v2 không ghi lại danh sách này.
4. Tập test ~320 ảnh sạch và gold văn hóa ~300 ảnh: được với tạp chí, nhưng phải có CI.

**Điểm.** **Major revision** (có xu hướng reject nếu điểm 1 không được giải quyết trước khi nộp).

#### R-D. TOMM, reviewer ảo giác LVLM / đa phương tiện

**Điểm mạnh.** Có cổng T-human (thừa nhận VSPS 3,91 < zero-shot 4,17). Có đường cong Trung thực–Độ cụ thể với cùng một phép lùi sau sinh cho mọi hệ (SFA).

**Điểm yếu.**
1. **Nền VSPS chỉ trượt dọc đường cong P/R.** Số đo chính của repo (`KE_HOACH_Q2.md`, v2 raw s42): VSPS P 38,1 / R 42,2 / F1 40,1, so với zero-shot 31,6 / 57,1 / 40,7. Nếu ViHG-Cap chỉ đổi toán tử lùi thì phải cho thấy nó **vượt lên trên** đường của zero-shot + lùi-sau-sinh, không chỉ hơn SFT-không-kiểm-chứng về precision.
2. **Baseline HALVA, RLAIF-V-7B** là checkpoint họ LLaVA, tiếng Anh. Chạy trên caption tiếng Việt thì đó là baseline rơm. Plan không nói sẽ cài lại loss DPA trên Qwen2.5-VL hay dùng nguyên checkpoint.
3. **Backbone thứ hai** (Qwen2.5-VL-3B) vẫn cùng họ Qwen. Chưa chứng minh được phương pháp không gắn với một họ mô hình.
4. Human eval P2 (150 ảnh × 3 hệ) không có viết-lại-CLC và lùi-sau-sinh, trong khi đây là hai đối chứng quyết định.

**Điểm.** **Major revision.**

#### R-E. ACM MM 2027 (chỉ khi qua G-P2)

**Điểm yếu thêm.** Bài chỉ chạy trên tiếng Việt, không có COCO/DOCCI hay AMBER tiếng Anh cho phương pháp (P0 lại có COCO 5.000 ảnh, B5). Phần "KG" chỉ là tra cứu, không có học trên đồ thị. Metric chính đến từ một bài P1 chưa qua phản biện.

**Điểm.** **4/10 (weak reject)**. Lên 6 nếu: có một bộ tiếng Anh, thắng CLC trước người chấm, và trội Pareto so với lùi-sau-sinh.

### Điểm yếu chí mạng còn lại (tổng hợp)

1. Salami với P0 chưa được gỡ ở **kế hoạch thực thi** (F1).
2. M1 không phải metric tự động và không định nghĩa được ở cấp caption (F2).
3. Cổng G-P2 không kiểm tra đúng phần khác biệt của P2 (F3).
4. Ngân sách người và GPU không cộng phần việc của P0, nên hai bài tranh cùng một đội và cùng một GPU (F4, F5b).

---

## 3. Phát hiện (claim → bằng chứng → mức → cách sửa)

### F1. BLOCKER. §6 "mỗi đóng góp thuộc đúng một bài", nhưng kế hoạch P0 đang chạy vẫn chứa lõi của P2 và P1

- **Plan nói.** §6: P0 chỉ có "kiểm chứng 3 trạng thái, trung tính hóa giới tính, render truy vết" và "sửa lỗi VSPS". §7 liệt kê 6 việc cho P0, đều là sửa lỗi.
- **Bằng chứng.** `.paper_work/KE_HOACH_Q2.md` (lập 2026-10-09, đính chính 2026-10-10) là kế hoạch P0 lên TALLIP:
  - **D3**: "lùi loài/kiểu về nhóm cha (`chó poodle` → `con chó`)", màu, đếm. Đây là phần thực thể của (C) trong ViHG-Cap.
  - **D2**: relation → entity, đã đo +1,2 R strict. Đây là nấc cuối của thang vị từ (C).
  - **B3/C4**: OWLv2/Grounding DINO + hình học. Đây là (B) của P2.
  - **C1/C3**: hội đồng verifier (Vintern-1B + InternVL2.5-8B), ngưỡng hiệu chỉnh trên dev. Đây là đối thủ trực tiếp của cổng T0.5 (logit một lượt) trong v2.
  - **B1**: gold object 300 ảnh test, 2 người gán, κ. **B2**: metric cấp mệnh đề, người chấm 200 caption + LLM-judge hiệu chỉnh. Cả hai đè lên claim "đầu tiên được công bố, ở cấp caption và cấp mệnh đề" của P1.
  - §3.6 của file này còn ghi: TALLIP yêu cầu ≥ 25% nội dung mới, ≥ 30% nếu bài FAIR đã vào kỷ yếu.
- **Hệ quả.** Có **bốn** tầng chứ không phải ba: FAIR 2026 → P0 TALLIP → P1 → P2, và §6 không có cột FAIR. Nếu P0 chỉ giữ các việc ở §7 v2 thì phần mới của TALLIP chỉ là sửa lỗi, khó qua ngưỡng 25–30%. Nếu P0 giữ D2/D3/B1/B2 như `KE_HOACH_Q2.md` thì P2 mất lõi và P1 mất claim "đầu tiên". Hiện cả hai kế hoạch cùng hiệu lực.
- **Sửa.**
  1. Thêm cột **"P(-1) FAIR 2026"** vào §6. Thêm dòng: "P0 phải mở rộng ≥ 30% so với FAIR; phần mở rộng lấy từ danh sách sau, và chỉ từ danh sách này."
  2. Ghi cứng trong §6 và §7, đồng thời sửa `KE_HOACH_Q2.md` tương ứng trước 31/10/2026:
     > "**P0 (TALLIP) gồm**: A1–A3 (tái lập, funnel), D1 + D8 (selector, renderer), B4, B5 (COCO/AMBER), C1/C3 (hội đồng verifier + ngưỡng hiệu chỉnh) **hoặc** logit T0.5 (chọn một, xem F6), B3/C4 (box + hình học), C2 (audit 3 trạng thái 600 mệnh đề), dedup, hạn chế văn hóa, A4 (vòng tự huấn luyện).
     > **Chuyển khỏi P0**: D2, D3 → P2 (lùi phân cấp). B1, B2 → P1 (gold và chấm cấp mệnh đề). P0 chỉ báo CHAIR/P/R trên KTVIC-clean và COCO; nếu cần recall thật thì trích bản arXiv của P1."
  3. Thêm vào phần Related Work của P2 một câu cố định: "P0 [TALLIP] trung tính hóa giới tính, không lùi IsA hay vị từ; mọi thí nghiệm lùi phân cấp lần đầu xuất hiện ở bài này."
  4. Nếu P0 không đạt 30% nội dung mới khi bỏ D2/D3: chọn **phương án B** của R2-04 (gộp lùi IsA vào P0, P2 hoãn tới khi có đóng góp khác). Đừng giữ cả hai.

### F2. BLOCKER. §3 M1-P: "ước lượng tỷ lệ đúng … từ 50+50 claim/hệ người kiểm"

- **Bằng chứng.** Theo định nghĩa ở §3, tử số của P cho một caption chứa một tỷ lệ của cả hệ. T4 (§5) lại đo "τ_c của M1" so với VLM-judge, mà τ_c cấp caption cần một điểm riêng cho từng caption. Mọi hệ mới (kể cả 10+ baseline của P2) cần thêm 100 claim do người kiểm. Phần giờ này chưa có trong §8.
- **Sửa (thay câu M1 ở §3).**
  > "**M1-P** = (claim khớp node SUPPORTED-gold) / (claim khớp bất kỳ node gold nào, trừ từ rỗng). Claim khớp UNCERTAIN-gold và claim không khớp **không vào P**. Hai nhóm này được báo riêng thành **tỷ lệ không kiểm được (U-rate)**. Tùy chọn: chấm nhóm không khớp bằng một VLM-judge cố định (đóng băng 15/11) để có **M1-P⁺**. Mẫu 50+50 claim/hệ do người kiểm chỉ dùng để **hiệu chỉnh và báo sai số** của U-rate/M1-P⁺, không đi vào điểm."

  T4 so M1-P và M1-P⁺ với VLM-judge, cả hai đều tự động.

### F3. BLOCKER. §5 G-P2: "E1 hơn SFT-không-kiểm-chứng trên M1-P (dev, CI 95%) và không thua viết-lại-CLC"

- **Bằng chứng.**
  1. VSPS đã hơn SFT-không-kiểm-chứng về precision bằng cách nói ít đi (v2 raw P 38,1 so với zero-shot 31,6; R 42,2 so với 57,1). Điều kiện thứ nhất gần như chắc chắn đạt, nên không kiểm được gì về phép lùi phân cấp.
  2. Claim của P2 là "lấy lại độ cụ thể/recall mà không mất trung thực, so với VSPS-xóa", nhưng G-P2 không có VSPS và không có H-R.
  3. G-P2 (31/01) dùng M1 trước T4 (02/2027), là lúc M1 mới được kiểm.
  4. Dev chỉ có 80 ảnh, và M1-P hiện còn phụ thuộc mẫu người (F2).
- **Sửa (thay dòng G-P2).**
  > "**G-P2 (31/01/2027)**, trên dev 80 ảnh + 300 ảnh train-sạch giữ lại có gold object (bootstrap theo ảnh):
  > (a) ở cùng M1-P (±1 điểm), ViHG-Cap có H-R và số claim đúng/caption cao hơn VSPS-xóa (cùng verdict, cùng ngân sách), CI tách nhau;
  > (b) ViHG-Cap không thua viết-lại-CLC trên H-R ở cùng M1-P;
  > (c) điểm của ViHG-Cap nằm trên đường SFA của zero-shot + lùi-sau-sinh.
  > Metric dùng cho cổng: CHAIR-vi + object P/R trên gold object (đã có từ trước, không chờ T4). M1 chỉ báo kèm."

  Nếu trượt (a): P2 không được nộp ở đâu với claim phương pháp; chỉ còn là phân tích trong P1. Viết như vậy thay cho câu "P2 → IP&M/TOMM". Trượt cổng chính mà vẫn đưa bài sang tạp chí Q1 là lập luận ngược.

### F4. MAJOR. §8 "Người gán ~200 h, NCS ~90 h (R2-06 §4.3, … dư ~30%)"

- **Bằng chứng.** Bảng R2-06 §4.3 được lập cho phạm vi trước v2. v2 đã đổi phạm vi mà không tính lại:

| Hạng mục mới hoặc bị thiếu | Ước tính (giờ người gán) |
|---|---|
| Anchoring: v2 gán từ đầu 100 ảnh (bảng cũ: 30 ảnh) | +10–15 |
| Meta-eval thêm 100–150 ảnh XM3600 (bảng cũ: 400 ảnh × 5,3 phút × 2) | +18–27 |
| Gold SG cho phần XM3600 (cần cho F5) | +15–19 |
| Kiểm 50+50 claim × ~12 hệ (nếu giữ M1 như v2) | +10 |
| Human eval P2 thêm CLC + lùi-sau-sinh (5 hệ thay vì 3) | +15 |
| **Phần P0 trong `KE_HOACH_Q2.md`**: B1 300 ảnh × 2 người, B2 200 caption, C2 600 mệnh đề × 2, human eval ≥ 100 ảnh × 3 người | +60–80 (nếu P0 giữ B1/B2; giảm nhiều nếu chuyển sang P1 theo F1) |

- **Tổng.** Khoảng 330–360 giờ, chạm trần năng lực 200–340 giờ của đội, không còn dư.
- **Sửa.** Ghi lại §8 thành một sổ giờ dùng chung cho P0 + P1 + P2. Áp F1 (B1/B2 thuộc P1, làm một lần) và F2 (bỏ kiểm claim/hệ khỏi điểm). Ghi rõ: "nếu vượt 300 giờ thì cắt meta-eval xuống 300 + 100 XM3600 ảnh".

### F5. MAJOR. §3 Meta-eval A: "4 ứng viên … cấp caption + hệ" và §4 "XM3600 100–150 ảnh, phần phát hành được"

- **Bằng chứng.**
  - Với n = 4 thì tương quan cấp hệ không có độ mạnh thống kê. Hai trong bốn hệ thuộc họ Qwen.
  - XM3600 không được gán SG trong §4, nên phần phát hành được không chạy được M1/H-R/M2.
  - XM3600 đã chấm side-by-side tiếng Việt trên XM600 (đã xác minh, toàn văn §3). Đây là cơ hội nối trực tiếp, nhưng plan không chọn ảnh từ XM600.
- **Sửa.**
  > "Phần XM3600 = 100–150 ảnh **lấy từ XM600**, có **gold SG** theo cùng hướng dẫn.
  > Meta-eval cấp caption giữ 4 hệ. **Cấp hệ** dùng 8–10 hệ (thêm GRIT, Vintern-1B, InternVL3.5, một VLM thương mại, LLaVA-OneVision, caption tham chiếu thứ 2), chấm **so cặp** trên 100 ảnh XM600, theo thể thức XM3600 (thang 7 mức, 3 người chấm)."

  Nếu không đủ giờ: bỏ claim cấp hệ, chỉ báo cấp caption.

### F5b. MAJOR. §8 GPU "~515–760 GPU-h (R2-05)"

- **Bằng chứng.** Bảng R2-05 vẫn tính E3 GRPO (65–100), Qwen3-VL-8B (36–42) và G1 (22–24). v2 đã bỏ cả ba (−123 đến −166). Bảng lại **không** tính:
  - viết-lại-CLC (LLM viết lại span UNCERTAIN trên train để SFT, và trên test);
  - lùi-sau-sinh k = 0..3 cho mọi hệ (SFA = ~4 lượt eval × 14 hệ);
  - HALVA cài lại trên Qwen (thêm 3 run 7B);
  - backbone 3B × 3 seed;
  - toàn bộ phần GPU của P0 (`KE_HOACH_Q2.md`: chạy lại Stage-1 30–45 GPU-h, SFT 3 seed cho mỗi phiên bản dữ liệu, A4 vòng 2, backbone thứ hai của P0, COCO 5.000).

  Về phần cứng: `KE_HOACH_Q2.md` ghi "1 RTX 4090", v2 ghi "RTX 3090 này". Hệ số ×1,2–1,8 đổi kết quả cộng.
- **Sửa.** Một sổ GPU dùng chung, ghi rõ máy, mỗi hạng mục một dòng, có cột "thuộc bài nào". Ước tính lại theo phạm vi v2 + P0. Cắt trước: nhánh 3B và HALVA-checkpoint gốc.

### F6. MAJOR. Hai bản nâng cấp verifier cạnh tranh nhau trong 11/2026

- **Bằng chứng.** v2 §2 và §5 T0.5: "Vintern logit P(Có)/P(Không) một lượt". `KE_HOACH_Q2.md` C1/C3/D4: hội đồng Vintern-1B + InternVL2.5-8B, ngưỡng hiệu chỉnh trên dev, cùng giai đoạn tuần 4–6. P2 cần "VSPS chỉ đổi phép lùi". Nếu VSPS của P0 dùng hội đồng còn ViHG-Cap dùng logit thì bảng đối đầu đổi hai biến.
- **Sửa.** Thêm vào §5: "Chỉ một verifier được chốt trước 30/11. Nó thuộc P0 và được dùng **nguyên trạng** cho cả VSPS-baseline lẫn ViHG-Cap trong P2."

### F7. MAJOR. Vệ sinh split: T0.5 "đo trên split audit dev", G-P2 trên dev 80 ảnh

- **Bằng chứng.** Theo ghi chú đính chính 2026-10-10 của repo, 244 mệnh đề audit và Fig. 3B #2921 là ảnh **test** KTVIC, và lưới chỉnh tham số của VSPS nhiều khả năng đã chấm trên test. §7 v2 không có hai mục này. 157 ảnh KTVIC-sạch trong ViSG-test có thể giao với ảnh audit.
- **Sửa.**
  - §7 thêm mục 7: "Ghi trong bài P0: audit và lưới chỉnh dùng ảnh test. Chọn lại tham số trên một dev tách từ train sạch, báo số trước/sau."
  - §4 thêm: "Ảnh có mặt trong audit 244 mục và trong lưới chỉnh bị loại khỏi ViSG-test (chỉ dùng cho dev)."

### F8. MAJOR. Baseline HALVA, RLAIF-V-7B, GRIT cho caption tiếng Việt chưa có cách làm

- **Bằng chứng.** HALVA (2405.18654) và RLAIF-V là checkpoint họ LLaVA, huấn luyện cho tiếng Anh. §2 chỉ liệt kê tên. GRIT cần môi trường riêng (R2-05 mục 6).
- **Sửa (§2).**
  > "HALVA = loss DPA cài lại trên Qwen2.5-VL-7B, cùng dữ liệu, negative ngẫu nhiên mức cụm (cũng là ablation 'GEPA−negative-đồ-thị'). Checkpoint gốc HALVA/RLAIF-V chạy với prompt tiếng Việt, chỉ để ở phụ lục. GRIT: dùng dự đoán do tác giả cung cấp, hoặc bỏ."

  Human eval P2 gồm 5 hệ: zero-shot, VSPS, viết-lại-CLC, lùi-sau-sinh, ViHG-Cap.

### F9. MAJOR. Danh sách trích dẫn bắt buộc của R2-01 bị rơi khỏi v2; "chưa tìm thấy cho caption" cần thu hẹp

- **Bằng chứng.**
  - HalCECE (2503.00436, đã mở abstract): caption, "semantically minimal edits driven by hierarchical knowledge", nhằm phát hiện ảo giác.
  - DetailVerifyBench (2604.05623): 1.000 ảnh, gán ảo giác mức token, caption > 200 từ. Gần P1.
  - R2-01 mục 57 đã yêu cầu trích CLC, CSS, Gricean Retreat, SpeciaRL, Taxonomy-Aware Eval, HalCECE. v2 §1 chỉ còn CLC, CSS, SpeciaRL.
- **Sửa.** Đổi ô §1 thành "MED (CLC, CSS, SpeciaRL; HalCECE dùng phân cấp tri thức để **phát hiện** ảo giác caption; chưa tìm thấy bài **sinh/huấn luyện** caption bằng lùi phân cấp)". Thêm vào §10 một mục "Bắt buộc trích": 2402.10978, 2502.19110, 2310.01779, 2503.00436, 2603.03197, 2604.05623, Taxonomy-Aware Eval, CSS, Gricean Retreat.

### F10. MAJOR. §9: nhánh ACM MM không có thời gian viết

- **Bằng chứng.** G-P2 31/01. GEPA 02. T-human 03, mà 03 NCS viết P1. "Viết P2" ở 04. ACM MM 2027 khoảng 01/04 (chưa xác minh, `../cfp`). Như vậy nếu G-P2 đạt thì không có tuần nào để viết bản ACM MM.
- **Sửa.** Bỏ ACM MM 2027 khỏi v2 (IP&M SI 31/08 hoặc TOMM là đích duy nhất của P2). Nếu muốn giữ: "nếu G-P2 đạt thì 03/2027 viết P2 cho ACM MM, P1 chuyển sang 04/2027 (hạn ARR ~15/05 vẫn kịp)". Đồng thời thêm một bộ tiếng Anh (COCO 5.000 ảnh đã có pipeline từ P0) vào P2.

### F11. MINOR. Venue CLC không nhất quán

§0 B2 ghi "CLC NeurIPS'25", §10 ghi CLC là chưa xác minh. arXiv 2502.19110 không có comment. **Sửa**: ghi "CLC (arXiv 2502.19110, 2025)" ở mọi chỗ.

### F12. MINOR. Cách nói "chỉ claim phép lùi" ở §0 lệch với §6

§0 B1 nói P2 "chỉ claim phép lùi phân cấp", nhưng §6 gán cả GEPA và graph-then-caption cho P2. **Sửa §6**: tách hai cột, "Claim" (lùi phân cấp) và "Thành phần/ablation, không claim" (GEPA, graph-then-caption).

### F13. MINOR. Điểm độ cụ thể theo độ sâu Wikidata

**Sửa**: thay "độ sâu IsA" bằng "**bậc trong chuỗi lùi** của chính khái niệm đó (0 = gốc trong caption, 1, 2… = số nấc đã lùi)", vì đây là đại lượng mà phương pháp thực sự điều khiển. Độ sâu Wikidata chỉ báo phụ.

### F14. MINOR. OWLv2/Florence-2 nhận truy vấn tiếng Anh

**Sửa (§2 B)**: "tên thực thể được ánh xạ sang nhãn tiếng Anh qua bảng IsA/Wikidata. Thực thể không có nhãn tiếng Anh (văn hóa) thì bỏ qua bước box. Hình học chỉ được NÂNG trạng thái, như đã ghi."

### F15. MINOR. Có thể nhiễm dữ liệu ở Vintern

**Bằng chứng**: bảng 1 của 2408.12480 (Vintern-1B) có "Viet-OpenViVQA-gemini-VQA". Ảnh của UIT-OpenViIC có giao với OpenViVQA hay không: **chưa xác minh**.

**Sửa**: thêm OpenViVQA vào lượt dedup all-vs-all của T-dedup, và báo tỷ lệ ảnh ViSG-test mà Vintern có thể đã thấy.

### F16. MINOR. Ngưỡng "H-R giảm > 2 điểm"

**Sửa**: dùng "H-R giảm có ý nghĩa (CI 95% bootstrap không chứa 0)" thay cho ngưỡng cứng.

---

## 4. Trả lời câu hỏi salami (§6)

**Chưa gỡ được.**
- Về **giấy tờ**, §6 đã áp phương án A của R2-04: P2 coi VSPS là baseline và chỉ claim phép lùi. Đây là thiết kế đúng.
- Về **thực thi**, kế hoạch P0 song song (`KE_HOACH_Q2.md`) vẫn giữ D2/D3 (lùi phân cấp), B3/C4, C1/C3 (verifier) và B1/B2 (gold, chấm cấp mệnh đề). Tầng FAIR 2026 bị bỏ sót, và ngưỡng 25–30% nội dung mới của TALLIP chưa được cân với việc rút D2/D3 khỏi P0.
- Rủi ro tự trùng bây giờ gồm hai cặp: **P0↔P2** về lùi phân cấp và **P0↔P1** về gold và chấm cấp mệnh đề.
- Gỡ được bằng F1: chốt danh sách của P0 trước 31/10, sửa `KE_HOACH_Q2.md`, thêm cột FAIR. Nếu P0 không đủ 30% sau khi rút D2/D3, chọn phương án B (gộp vào P0, hoãn P2).

## 5. Kế hoạch đã làm đúng (ngắn)

- Áp đúng phương án A cho P2; có bảng đối đầu VSPS chỉ đổi phép lùi; có baseline viết-lại-CLC và lùi-sau-sinh, nên đã trả lời được câu "KG có cần không".
- Meta-eval đóng băng 15/11, không có ViHG-Cap; gold mù verdict; đo anchoring.
- Dedup all-vs-all ở tuần 1, đo cả trùng nội bộ KTVIC cho P0. Cổng T0.5 chặn đường K=5 tốn 1.150 GPU-h.
- Thừa nhận VSPS 3,91 < 4,17 và đặt T-human; dùng "chưa tìm thấy" thay cho "chưa có ai làm".
- Claim XM3600 (B8) đúng sau khi đã kiểm toàn văn.
- Hạ M4/M5/M6 xuống phân tích/chẩn đoán; bỏ E3 khỏi đóng góp.
