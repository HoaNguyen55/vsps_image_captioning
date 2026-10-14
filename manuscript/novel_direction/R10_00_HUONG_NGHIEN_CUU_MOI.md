# R10 — Hướng nghiên cứu mới cho bài VSPS: tổng hợp 20 báo cáo

*Ngày 2026-10-14. Agent tổng hợp R10: chỉ đọc, không dùng GPU, không sửa file có sẵn. Nguồn: `manuscript/research_r10/<ID>/REPORT.txt` (script và output ở `.session_backup/2026-10-14/research_r10/<ID>/`, không nằm trong git), `manuscript/research_r10/CONTEXT_R10.md`, `.session_backup/2026-10-13/decisions/PD-2.txt`. Bản chuyển cho Gemini (tiếng Anh): `manuscript/research_r10/R10_FOR_GEMINI.md`.*

**Quy ước**
- Mỗi con số đều kèm mã báo cáo và mục, ví dụ "(E1 §3c)". Số đọc trực tiếp từ file gốc của repo thì ghi đường dẫn file.
- **[MH]**: tín hiệu do mô hình tạo ra (vote của mẫu, hộp grounding, P(có), xác suất token, bảng từ vựng do agent soạn). Chỉ được dùng bên trong một phương pháp. Không bao giờ được coi là nhãn hay bằng chứng.
- **[CXM]**: chưa xác minh (trích dẫn, ID, hoặc con số chưa được chạy lại độc lập). **[SUY]**: suy luận của người tổng hợp, không phải số đo.
- Không có tuyên bố "đầu tiên". Độ mới (novelty) giữ đúng mức mà từng báo cáo tự chấm.
- Tài liệu này không chứa văn bản chú thích OpenViIC nào. OpenViIC chỉ xuất hiện dưới dạng số tổng hợp của panel đánh giá.
- X1 nộp báo cáo muộn và được tích hợp cuối cùng. Cả 20 báo cáo đều đã có.

---

## 1. Tóm tắt

**Năm phát hiện mạnh nhất**

1. **Hiệu ứng số lượng là chuyện chung của cả lĩnh vực, không riêng KTVIC (E1, X1).**
   - E1 chấm lại caption đã công bố của các phương pháp chống ảo giác tiếng Anh, khớp số đối tượng theo từng ảnh (MCP). Nguồn: repo OPERA (4 LVLM) và repo Less-is-More.
   - Ở dạng thô, 12/15 cặp có lợi ích precision có ý nghĩa thống kê. Sau MCP chỉ còn 3/15.
   - Một cặp đảo dấu: OPERA-Shikra so với beam5, −1.23 [−2.37, −0.08].
   - dP trung bình giảm từ +3.4 xuống +0.6, tức khoảng 80% lợi ích công bố đến từ số lượng (E1 §0, §3c). Con số đếm này chỉ có tính mô tả, vì các cặp dùng chung baseline.
   - X1 cho thấy đơn vị kiểm soát phải là số đối tượng, không phải độ dài. Kiểm soát độ dài vẫn cho MBR +2.60 F1 (P1) và +1.95 (fuse2). Biên theo số đối tượng chỉ cho −0.14 và −0.76.
   - Trên 32 run đã huấn luyện, R² của P theo log m là 0.960; theo log độ dài là 0.826 (X1 §0, §3c).
2. **Số mũ của biên là thuộc tính của bộ gold, không phải của mô hình (G2, G3).**
   - Cùng một tập đầu ra, b tăng đơn điệu theo số tham chiếu dùng làm gold. Trên KTVIC, b đi từ 0.403 đến 0.703 khi k = 1..5 (Δ = +0.300 [0.248, 0.347]). Nhãn instance cho b cao nhất: COCO 0.846, so với 0.643 khi dùng 5 ref (G2 §3b).
   - G3 phân rã b_sys = b_pool − D. Hai hằng số hệ thống s1 = 0.892 và D = 0.194 khớp 10 điểm precision với RMSE 0.78 P.
   - Khi chỉ khớp trên h ≤ 4, mô hình dự đoán b(5) = 0.756. Giá trị đã đăng ký trước là 0.7468 (G3 §0, §3d).
   - Hệ quả 1: không bao giờ được mang b = 0.747 sang một gold khác.
   - Hệ quả 2: một phương pháp chỉ vượt biên nếu làm thay đổi tỉ lệ s(M), tức tỉ lệ mention thuộc tập "người có thể gọi tên". Theo G3, việc chỉ xếp hạng lại bằng bằng chứng nội tại của mô hình không làm được điều đó (G3 §0).
3. **Hai chế độ: các hệ thống huấn luyện thì "khoá", còn chọn lọc theo từng ảnh thì "tách rời" (E6). Biên cũng áp dụng cho quan hệ (G1).**
   - E6 dùng hai trục: ρ_A (tính điển hình, đo bằng ref KTVIC) và ρ_I (tính độc lập, đo bằng panel OpenViIC).
   - Cả 36/36 hệ thống fine-tune trên KTVIC đều nằm ở (0, 0) trên hai trục. 37 hệ thống off-style nằm ở ρ_A −55 nhưng ρ_I chỉ −21 (E6 §3.1).
   - Khi chọn lọc theo từng ảnh có đọc tham chiếu, hai trục tách rời. Chọn bằng 2 ref KTVIC cho +6.48 F1 trên 2 ref KTVIC khác, nhưng chỉ +1.22 trên panel (κ = 0.19) (E6 §3.3).
   - G1: trên chỉ số đối tượng, MBR chỉ là dịch chuyển số lượng (residual −0.4% / −1.3%), nhưng rơi dưới biên QUAN HỆ: p1_s43mbr −17.7% [−32.0, −3.4]. Self-fusion lệch cả biên đối tượng (−6.7%) lẫn quan hệ (−22.0%) (G1 §3c; câu ở G1 §0 gộp self-fusion vào "dịch chuyển thuần" là không khớp với bảng §3c của chính nó).
4. **Phân bổ (allocation) là kênh thứ ba, và đối chứng cùng số lượng theo từng ảnh không nhìn thấy nó (M6; cùng hướng với E1 và M5).**
   - Giữ nguyên tổng số mention của greedy, phân bổ toàn cục theo vote [MH] cho +1.84 [+0.29, +3.34] F1.
   - Knapsack chọn một caption có sẵn cho mỗi ảnh cho +2.08 [+0.05, +4.11] (p .044; khoảng 6 nhánh đã thử; dev300). So với đối chứng của PD-2, nó chỉ được +0.09 (M6 §0, §3c–3e).
   - Đây là ứng viên phương pháp duy nhất của R10 có kết quả dương trên dev ở số lượng khớp. Nhưng nó khớp số lượng ở mức TỔNG, không phải theo từng ảnh.
5. **Đo lường: giao thức chấm và bộ so khớp quyết định nhiều hơn ta tưởng (E4, V1, V3).**
   - CIDEr cấp âm tiết cao hơn cấp từ từ +14 đến +16 điểm.
   - Dấu "." cuối câu làm mất 20–29% CIDEr-D. Lý do: n-gram không có trong ref nhận IDF cực đại.
   - Chi phí CIDEr của MBR là 47.2; bỏ dấu câu thì còn 18.7 (E4 §0, §3).
   - V1: cùng một lexicon nhưng có ba định nghĩa "cùng đối tượng". Bộ trích v3 đổi 34.9% gold set của test, nhưng không kết luận nào của PD-2 thay đổi: các tương phản ghép cặp đổi tối đa 0.54 F1 (V1 §0, §3.3).
   - V3: thiếu liên kết từ cô gái/chàng trai lên phụ nữ/đàn ông/người. Lỗi này chiếm 38% số "ảo giác loại người" của P1 (V3 §0).

**Cập nhật 35_e (RL CN-RLOO, chỉ thưởng CIDEr), đã đối chiếu `data/results/rl/` (C-029) và `.session_backup/2026-10-13/decisions/D14.txt`.**
- Verdict KILL KHÔNG SẠCH: CIDEr dev 144.33 → 145.90, tức +1.57 [−6.26, +9.55], dưới ngưỡng +3.0. Guard G4 (sao chép nguyên văn ref) trượt: 1.00 → 1.70 → 1.60 → 2.25%, vượt giới hạn 1.33%. CIDEr trên panel −0.5 [−3.7, +2.6].
- Kết quả khớp số lượng so với P1_dev: ΔF1 +1.77 [−0.52, +4.08]; Δresidual biên +1.46 [−0.80, +3.64]; mention 1.763 → 1.793.
- D14 đóng nhánh RL (YES 99%) và ghi kết quả thành kết quả âm đăng ký trước N11; 35_f và 35_g bỏ qua (0 GPU-h); tổng chi RL 3.79 GPU-h (theo coordinator; riêng huấn luyện 3.153 GPU-h).
- **Dự đoán đăng ký trước của M4 cho run này: 3/4 đúng.**
  - C1 mention ∈ [1.65, 1.90] → 1.793: đúng.
  - C3 F1 dev ∈ [53.1, 56.6] → 56.34: đúng.
  - C4 ≤ 15/300 caption không nêu lớp nào → 12/300: đúng. Người tổng hợp tự đếm bằng objects_in; P1_dev 9/300 khớp M4 §3a.
  - C2 ∈ [−1.5, +2.0], CI chứa 0: trượt sát trên chính endpoint cm của M4, +2.07 [−0.20, +4.27] (Gemini tính sau khi tổng hợp: `.session_backup/2026-10-13/r10_cpu/n11_35e_posthoc_r10_battery.json`, khoá `1_M4_cm_endpoint`). Nếu đọc theo residual biên thì +1.46 nằm trong khoảng. Trên panel, cm chỉ +0.47 [−0.90, +1.82].
- Hệ quả: M4 cần judge mở lại nhánh RL; theo luật nhánh của chính M4 (§4a), kill không sạch nghĩa là "engine không tin cậy", nên M4 xuống cuối danh sách (§4).

**Điều mới nhất hiện nay** (điểm novelty tự chấm): G3 4/5 (phân rã b "moderate-high"; câu hỏi "vì sao 0.75" "moderate"); E1, E6, X1 3/5 nhưng impact 4/5; M7 3/5 (định lý "rào đón không thoát được biên" tự chấm "high" cho từng phần); CAR của M6 3/5. Công trình gần nhất có thể trùng ý là LeHaCE (NeurIPS 2024, DOI 10.52202/079017-3538): đường cong độ dài–ảo giác riêng cho từng mô hình, đo theo SỐ TỪ chứ không theo số đối tượng (X1 §2b) [CXM: X1 mới đọc slide và abstract]. Chưa có phương pháp nào vượt biên theo endpoint hiện hành của PD-2; M3 có khoảng 25–30% khả năng qua (M3 §0); M4 (~25%, M4 §0) đang bị chặn bởi D14.

**Phát hiện của người tổng hợp từ file gốc** (đã kiểm tra): ba giá trị kill-2 của UPE (+0.07/+0.03/+0.17) tính trên gold PANEL OpenViIC, không phải ref KTVIC. Trong `data/results/upe/test/upe_mbr_ktvic_test.json`, khối `p1assist_s4x.vs_count` chỉ có `panel_obj` và `panel_cider`, không có `obj_ktvic`. M6 §1 H5 và V1 F-3 lại so với các số này như thể chúng tính trên gold KTVIC (xem MT2, §5).

---

## 2. Bảng 20 hướng

N/F/I/R lần lượt là novelty / tính khả thi trên một RTX 3090 / impact / rủi ro (rủi ro 5 là cao nhất). Đây là điểm tự chấm ở §7 của mỗi báo cáo. Cột "Kết luận" dùng các nhãn: DƯƠNG (phương pháp vượt đối chứng), ÂM (thất bại), ĐG (chỉ là đóng góp đánh giá/phương pháp luận), CHỜ (cần GPU để kết luận). Đường dẫn file tính từ `.session_backup/2026-10-14/research_r10/`.

| ID | Ý tưởng | Kết luận | Số liệu chính (file) | N/F/I/R | GPU-h | Luật dừng chính |
|---|---|---|---|---|---|---|
| E1 | Chấm lại caption đã công bố của các phương pháp chống ảo giác (tiếng Anh) ở số đối tượng khớp theo từng ảnh (MCP) và trên biên cắt cụt (TRF); tách lợi ích thành số lượng / phân bổ / lựa chọn | ĐG, ủng hộ luận điểm | 3/15 cặp sống sót qua MCP; dP +3.4 → +0.6; LiM-EOS LLaVA-1.5-7B +7.9 → +1.08 [−0.14, +2.25] (E1/e1_decomposition.txt) | 3/5/4/2 | A: 0; B: ~15 (đủ: 30) | K2: placebo \|dP_MCP\| > 1 thì dừng; K4: hơn 1/3 cặp decoding sống sót thì đổi headline |
| E2 | Mô hình capture-recapture M_h trên 5 ref, cho ra P*/R*/F1*; tách FP thành ba phần: chưa được nêu do lấy mẫu / do hướng dẫn / ảo giác thật | ĐG; metric P* thất bại (ÂM) | Hold-out MAE 2.33, naive 6.71 (R′=3); Spearman với panel: P* 0.65, P thô 0.91; FT: 7–18 / 11–13 / 1–4 điểm (E2/e2_results.json) | 3/5/2/3 | 0 | K2: không bao giờ dùng P*/F1* làm headline; K3: CI trên của phần ảo giác > 5 điểm thì bỏ câu "FP hầu như là vật thật" |
| E3 | Metric đối tượng bất biến với hướng dẫn chú thích: tầng THING và tầng SCENE; κ chéo panel so với null xáo trộn ảnh | ĐG | Lớp gọi tên chỉ đóng ~30% khoảng cách (dev 17.88 → 12.13; test 15.74 → 10.83); C80 κ 0.89/0.96; lợi thế sân nhà 9.79 → 2.79 (E3/dev300.json, test.json) | 3/5/3/2 | 0 (≤ 0.1 nếu chạy tuỳ chọn) | K1: nullW > L0 + 15 thì lớp vô hiệu; K2: κ trên test tăng < 0.10 thì chỉ giữ phần phân rã |
| E4 | Thẻ giao thức (signature kiểu sacreBLEU); stress set gồm 15 giao thức × 26 hệ thống | ĐG | Số âm tiết 164.25 đã xác nhận (164.32/164.11/164.31); dấu "." −20–29%; τ_FT 0.92–1.00; với ref OpenViIC τ_FT −0.05 (E4/pilot_results.json) | 3/5/3/2 | 0 | K2: P12 cắt còn 5 ref mà τ_FT ≥ 0.8 trên cả 3 seed thì bỏ claim "panel đảo thứ hạng" |
| E5 | k*: số người chú thích tương đương, dựa trên độ phủ Good-Turing và ngoại suy Chao-Jost | ĐG | P1 0.89 [0.83, 0.94]; fuse2-det 1.75 [1.63, 1.88]; τ(k*, h1 so với h4) 1.00, còn F1 chỉ 0.35; không chuyển được giữa các hướng dẫn (tỉ lệ 1.27–6.09) (E5/kstar.json) | 2/5/3/2 | 0 | K3: drift của P1 trên dev300 có CI loại 0 thì rút claim bất biến; K4 đã kích hoạt |
| E6 | Bản đồ hai gold: ρ_A (điển hình) so với ρ_I (độc lập); chỉ số Goodhart G = 1 − Δρ_I/Δρ_A | ĐG | FT: 36/36 hệ thống ở (0,0); off-style ρ_A −55, ρ_I −21; khi chọn lọc κ = 0.19 (E6/map2d.json, bon_dev.json) | 3/5/4/2 | P1: ~2.0 | κ16 ≥ 0.70 thì bỏ khung 2 chiều |
| G1 | Biên số lượng cho thuộc tính và quan hệ (tuple kiểu SPICE) | ĐG | Trong ladder: b đối tượng 0.70–0.75, quan hệ 0.61–0.73, thuộc tính 0.84–0.88; off-style −19% (đối tượng), −37 đến −45% (thuộc tính/quan hệ); MBR rel_s −17.7% (G1/fit_ladder.log, fit_clean.log) | 3/5/3/2 | C: ~4 | H1: ≥ 2 run mới lệch > 10% với CI loại 0 thì bác; H5: CI chứa 0 trên cả 3 seed thì bỏ |
| G2 | Phạm vi của luật biên qua dataset, gold, cách decode và backbone; b theo độ đầy đủ của gold | ĐG | b dao động 0.40–0.99; KTVIC refs5 − refs1 +0.300; COCO inst − refs5 +0.203; nhiệt độ T không đổi b (+0.03) nhưng mẫu ở T0.8 nằm dưới biên 3–5 P (G2/g2_frontier.json) | 3/5/3/2 | B: 7–9; D: 1.5 | K1: dự đoán P1 thất bại trên ≥ 2 dataset thì chỉ báo "b phụ thuộc dataset" |
| G3 | Lý thuyết sinh của biên: P_sys = s(M)·P_pool, suy ra b_sys = b_pool − D | ĐG (lý thuyết) | s1 0.892, D 0.194, RMSE 0.78 P; dự đoán b(5) 0.756; 1 − b = 0.053 (phần tham chiếu) + 0.200 (phần hệ thống); α_pos 0.24–0.28 (G3/out/decomp_fit.log, gold_size.json) | 4/5/3/2 | 0 (E: ~1 nếu thiếu pool) | H1: max_h D − min_h D > 0.06 (CI loại 0) hoặc RMSE > 1.5 P thì bác |
| M1 | Xếp hạng lại theo grounding của chính Qwen2.5-VL [MH], giữ k_i cố định | Phương pháp; mới có trần trên CPU; dự báo ÂM (~20% qua) | Ở k_i của PLAN: oracle hiện diện +4.58; oracle đầy đủ +10.34; oracle phá hoà +1.29; tín hiệu cần AUROC độc lập ≥ ~0.70 (M1/m1_headroom.json) | 3/5/2/4 | 1.0–1.3 (tối đa ~6.6) | K1: ΔF1 so với POOL-VOTE < +1.0 hoặc cận dưới ≤ 0 thì dừng, không chạy test |
| M2 | Độ "đáng nhắc tên" học từ người chú thích (prior lớp, đồng thuận k/5, vị trí) dùng để xếp hạng | ÂM (trên CPU) | Tốt nhất −0.35 [−1.53, +0.87] so với pool-vote; oracle +9.86; các biến thể đối chứng lệch nhau tới 1.03 F1 (M2/m2_pilot.json) | 2/5/2/4 | 0 (G-SAL ≤ 0.5) | K-a/K-b/K-c của G-SAL; báo cáo khuyến nghị không chạy GPU |
| M3 | DPO với cặp có cùng số đối tượng (CM-DPO); bất biến với mọi phần thưởng phụ thuộc số lượng | Phương pháp; CHỜ GPU | 3.68 cặp/ảnh; oracle cùng số lượng +6.64 [+4.72, +8.66]; chia người chú thích +4.64; vote share chỉ +0.24 (M3/out/pilot.log) | 3/4/3/4 | 4.2 (đủ: ~33) | Stage 1: d-res ≥ +1.5, cận dưới > 0, qua guard G1–G5; nếu không thì KILL hoặc GREY |
| M4 | RLOO với baseline phân tầng theo số lượng (CS) cho phần thưởng đối tượng | Phương pháp; BỊ CHẶN: cần mở lại nhánh RL (D14), và 35_e kill không sạch (M4 §4a) | Độ dốc trong ảnh 0.479 [0.436, 0.525], còn giá biên là 0.586; gradient số lượng của CS = 0; proxy +1.4 đến +1.8 so với CIDEr-only (M4/out/m4_pilot.json); dự đoán cho 35_e: 3/4 đúng, C2 trượt sát (cm +2.07 > +2.0) | 2/4/3/4 | 4.0 (đủ: ~22) | GO chỉ khi Δ ≥ +1.0 (cận dưới > −1.0), \|dM\| ≤ 0.15, CIDEr ≥ control − 3, qua guard; nếu không thì KILL, không chạy lại |
| M5 | Adapter có điều kiện theo ngân sách đối tượng k = 1..4 | Phương pháp; dự báo H0 (~75%) | Phân bổ +1.67 đến +2.31 F1 ở tổng khớp (dev); PLAN-F1 −2.49 = xếp hạng −0.95 + phân bổ +0.68 + nền −2.23 (M5/m5_check.json) | 2/5/2/4 | 2.4 (test ~9) | K0: token count không kiểm soát được số đối tượng; K1: phần xếp hạng ≤ +0.5 thì không chạy test |
| M6 | Phân bổ một ngân sách tổng qua các ảnh (water-filling); phân rã CAR | Phương pháp + ĐG; DƯƠNG yếu trên dev (khớp ở mức tổng) | Vote toàn cục +1.84 [+0.29, +3.34]; knapsack +2.08 [+0.05, +4.11]; điểm cắt m* ≈ 2.4; UPE: C +0.92, B +0.62, A +0.14 (M6/out/m6_alloc.json) | 3/5/3/3 | a/b: 0; c: 1.7; d: 0.5 | M6b: ΔF1 gộp < +0.8 hoặc CI chứa 0; M6c: < +1.0, hoặc CI chứa 0, hoặc CIDEr < greedy − 5 |
| M7 | Caption có rào đón ("có thể có X") và điểm Brier theo lớp | ÂM với vai trò phương pháp (có định lý); ĐG dương | Rào đón so với đối chứng cùng số lượng: +0.09 [0.00, +0.29]; Brier Bayes 3 mức −15.1% (2.238 so với 2.637); ref KTVIC có 0/2,790 câu rào đón; zero-shot detailed 58% (M7/hedge_eval.json, hedge_counts.json) | 3/5/3/2 | G1: 1.5; G2: ~5 (có điều kiện) | K1: Brier giảm < 5%; K2: dF1 ở E1 > +0.5; K3: dải rào đón có tỉ lệ hiện diện > 0.75 |
| V1 | Bộ trích v3 hiểu loại từ (cây/quả), từ ghép (cửa hàng) và phủ định | ĐG (sửa đo lường) | Đổi 17.4% ref test và 34.9% gold set; P1 +1.34 F1; tương phản đổi ≤ 0.54; với v2, 'quả' có 3,806 mention nhưng chỉ 0.2% được nhãn instance xác nhận (V1/rescore.json, validate.json) | 2/5/2/1 | 0 | F-3 lật (CI loại 0) thì DỪNG và phải viết lại câu "không phương pháp nào sống sót" |
| V2 | ViPOPE+: benchmark tồn tại đối tượng tiếng Việt, mẫu âm chỉ lấy từ nhãn đầy đủ | ĐG | Mẫu âm lấy từ "0/5 ref nhắc": ở chế độ popular, 33.73% thực ra có mặt (UIT-ViIC); capture-recapture đánh giá thấp 3–6 lần; cổng salience đưa về ≤ 0.4% (V2/pilot_v2.json) | 3/5/3/2 | 9–10 (S5: +0.5–2.5) | K1: DiD < 1.0 hoặc CI chứa 0 với mọi hệ thống thì báo null; K5: ΔF1 của S5 < +0.5 |
| V3 | Phân loại lỗi caption tiếng Việt thành 15 lớp (dựa trên luật); đo vùng mù của endpoint | ĐG | Vùng mù 7–14% (FT short), 19–20% (fuse2-det), 26–35% (zero-shot); MBR: fragment −1.1 pp, CJK +0.7 pp (V3/taxonomy.json) | 2/5/3/2 | 0 (0.3 nếu thiếu file) | K1: precision của cờ đếm < 0.50 thì bỏ lớp đếm; K2: \|dP\| < 0.2 thì chỉ để chú thích |
| X1 | Định vị và kiểm tra trùng ý tưởng (scoop); đối chứng trung bình hoá phá hoà; so sánh đơn vị số đối tượng với độ dài | ĐG | Kiểm soát độ dài cho MBR +2.60/+1.95, kiểm soát số lượng −0.14/−0.76; R² 0.960 so với 0.826; trên 85 run: residual lớn nhất +1.58, không run nào có CI > 0; tie-avg (v,g) 59.22, dải ngẫu nhiên [58.74, 59.70] (X1/x1_ties.json, x1_envelope_length.txt) | 3/5/4/2 | 0 (P-C: 0.5) | P-A: họ tie-avg trải > 0.5 F1 trên test thì báo specification curve; P-B: \|α_len − α_cnt\| < 0.5 P thì bỏ claim "đơn vị đối tượng" |

---

## 3. Câu chuyện thống nhất cho bài báo

**Luận điểm một câu:** Chỉ số đối tượng trong captioning chủ yếu đo hai thứ: số mention, và độ đầy đủ cùng văn phong của bộ gold. Khi đã kiểm soát cả hai, không phương pháp nào — của nhóm hay đã công bố — vượt được một biên lập chỉ mục theo gold. Bài báo giải thích vì sao, đưa ra công cụ đo, và báo cáo các phương pháp được thiết kế riêng cho endpoint này.

### 3.1 Các mạch, theo thứ tự lập luận

1. **Chỉ số thô thưởng cho việc nói nhiều.**
   - G2 §1 đưa ra đẳng thức b = p_marg/P. Từ đó, F1 tăng khi thêm mention khi và chỉ khi p_marg > F1/2. Ở P1: 0.747 × 78.5 = 58.6, lớn hơn nhiều so với 27.3, nên F1 tăng đơn điệu trên toàn dải đã quan sát.
   - E6 §3.1: corr(log M, F1_I) = 0.84 trên 73 hệ thống. Tập Pareto thô chính là các hệ thống nói nhiều.
   - X1 H2: chuẩn hoá theo từng mention (CHAIR_i) lại thưởng cho việc nói ít. Chuẩn hoá không thay được kiểm soát.
2. **Một luật đo lường.**
   - TP = a·M^b đúng trong cùng một văn phong. Trên ladder KTVIC, R² từ 0.87 đến 0.99 cho mọi loại tuple (G1 §3a).
   - b do gold quyết định, không do mô hình (G2 §3b). Lý thuyết b_sys = b_pool − D giải thích giá trị 0.75 (G3).
   - E6 cho một kiểm chứng chéo [SUY]: biên trên panel OpenViIC có b = 0.899, cao hơn 0.745 của biên trên ref KTVIC. Panel này gọi tên 6.0 lớp/ảnh, so với 3.7 của KTVIC. Đây đúng là hướng mà luật độ đầy đủ của G2 dự đoán (E6 §3.1).
   - Phạm vi: luật chỉ đúng với đầu ra greedy của các hệ thống huấn luyện trên KTVIC. Off-style lệch −19% TP đối tượng và −37 đến −45% với thuộc tính/quan hệ (G1 §0); tính theo P là −19 đến −46 P (G2 §3c). Mẫu ở T0.8 nằm dưới biên (M6 §3h: −4.32; G2 §3d). Self-fusion mất phần s1 (G3 §3g).
   - X1 §3b: biên này là một "đường bao" kiểu SFA/DEA trên 85 run. Không run nào có CI của residual nằm trên 0.
3. **Mọi lợi ích phải được phân rã.** CAR chia lợi ích so với greedy thành nền D, số lượng C, phân bổ B, xếp hạng A (M6 §3e); đối chứng của PD-2 chỉ thấy phần A. TRF/MCP của E1 và xếp hạng/phân bổ/nền của M5 cùng cấu trúc. Telescoping phụ thuộc thứ tự cộng, nên phải lấy trung bình Shapley qua 6 thứ tự (X1 §2d).
4. **Áp dụng cho phương pháp của người khác và của nhóm.** E1 (đã công bố); UPE (D11); PLAN-F1 (D12); E5-DPO (residual −1.97 [−4.33, +0.18], M3 §1); salience (M2); rào đón (M7: +0.09 [0.00, +0.29]); RL 35_e = N11 (Δresidual +1.46 [−0.80, +3.64] ở +0.03 mention, D14). Phần xếp hạng A ≈ 0 ở mọi nơi đã đo; phần còn lại là số lượng, cộng thêm phân bổ.
5. **"Khớp số lượng trên ref KTVIC" vẫn chỉ đo tính điển hình.** E6 thêm trục thứ hai và chỉ số Goodhart. E3: khoảng cách giữa hai hướng dẫn gồm ~30% cách gọi tên, ~70% chọn cái để nhắc. E2 tách FP thành ba phần. E5 đổi sang "đơn vị người chú thích": chưa hệ thống nào bằng một nhóm người ở cùng số lượng (dC < 0 với cả 11). Mốc người: P1 ngang người trên trục độc lập (+1.2 F1 ở cùng M) nhưng kém người KTVIC 5.4 F1 về tính điển hình (E6 §3.2). Ví dụ Goodhart thật, đã chấm: 35_e tối ưu CIDEr KTVIC (+1.57, không có ý nghĩa) trong khi CIDEr panel −0.5 và tỉ lệ chép nguyên văn ref tăng 3.4 lần (D14).
6. **Ngoài đối tượng.** Quan hệ và thuộc tính có biên riêng, MBR làm hỏng quan hệ (G1); lỗi hình thức và vùng mù của endpoint (V3); rào đón không thoát được biên, chỉ quy tắc proper như Brier thưởng cho nó (M7).
7. **Tính hợp lệ của phép đo.** Thẻ giao thức, lỗi do dấu câu/chữ hoa, sửa Bảng 3 KTVIC (E4); matcher v2 với v3 làm độ nhạy (V1, V3); mẫu âm sinh từ caption bị nhiễm (V2); đối chứng định nghĩa duy nhất bằng trung bình hoá phá hoà (X1 §3a).
8. **Mốc baseline.** P1 response-only: CIDEr 148.23 (SD 0.38), giao thức cấp từ (PD-2). Không đặt cạnh 136.0 của GRIT khi chưa khớp giao thức: khớp thì chênh +12.2, lệch thì thành +28.3 (E4 §3).

### 3.2 Đề cương bài báo

**Phương án tiêu đề** (giữ tiếng Anh vì bài viết bằng tiếng Anh):
1. *Counting Before Comparing: Count- and Gold-Controlled Evaluation of Object Content in Image Captioning*
2. *Typicality Is Not Truth: A Gold-Indexed Count Frontier for Vietnamese Image Captioning*
3. *No Free Objects: Count, Allocation and Reference Completeness in Caption Hallucination Evaluation*
4. *What Object Metrics Measure: Count Frontiers, Two Golds and a Controlled Vietnamese Baseline*

**Đóng góp** (không câu nào được nói "đầu tiên"):
- C1. Quy trình đánh giá khớp số lượng: đối chứng trung bình hoá phá hoà (X1); phân rã CAR có trung bình Shapley (M6, X1); kết quả áp dụng lên phương pháp tiếng Anh đã công bố (E1) và lên phương pháp của nhóm.
- C2. Luật biên lập chỉ mục theo gold, có tuyên bố phạm vi; lý thuyết hai thừa số b = b_pool − D; biên riêng cho từng loại tuple (G1–G3).
- C3. Đánh giá hai gold: chế độ khoá/tách rời và chỉ số Goodhart (E6); phân rã gọi tên/chọn lọc (E3); FP ba phần (E2); đơn vị k* (E5).
- C4. Tính hợp lệ của phép đo cho tiếng Việt: thẻ giao thức (E4); phiên bản matcher và v3 (V1, V3); dấu thanh, tỉ lệ CJK, sửa Bảng 3 KTVIC (PD-2).
- C5. Baseline KTVIC mạnh có kiểm soát, cùng các kết quả âm đăng ký trước (UPE, PLAN-F1, E5 RFT, MR5, KG, N11 = 35_e). Nếu M3 hoặc M6 qua, thêm kết quả phương pháp ở số lượng khớp.

**Các phần**:
1. Mở đầu.
2. Công trình liên quan: CHAIR, POPE, CCEval/HallE, LeHaCE, AMBER, THRONE, SPICE/CAPTURE, sacreBLEU/Rogue Scores, Chao và capture-recapture, rater equivalence.
3. Dữ liệu, hệ thống, phép đo: KTVIC, UIT-ViIC, COCO-2500; panel OpenViIC chỉ để đánh giá; thẻ giao thức; matcher.
4. Biên số lượng: luật, phạm vi, lý thuyết (G2, G3, G1).
5. Đánh giá khớp số lượng và phân rã CAR (PD-2, M6, X1, E1, các kết quả âm của nhóm).
6. Tính điển hình và sự thật (E6, E3, E2, E5, mốc người).
7. Phương pháp dưới endpoint mới (M3/M6 nếu đã chạy; N11 và các dự đoán đúng của M4; định lý M7; các kết quả âm M1/M2/M5).
8. Ngoài đối tượng (G1, V3; V2 nếu chạy).
9. Hạn chế: chỉ một panel độc lập, một backbone, các lần đã nhìn test, giấy phép.

Phụ lục: bảng stress giao thức (E4), phân loại lỗi (V3), bảng matcher (V1), bảng k* (E5).

**Hình và bảng chính đề xuất**
- Hình 1: P thô và P ở MCP cho 15 cặp phương pháp tiếng Anh (E1 §3c), kèm so sánh kiểm soát độ dài với kiểm soát số lượng (X1 §3c).
- Hình 2: b theo số ref k = 1..5 và theo nhãn instance trên KTVIC, COCO, UIT-ViIC (G2 §3b); chồng thêm b_pool(h) và b_sys(h) (G3 §3b, §3d).
- Hình 3: bản đồ hai gold cho 73 hệ thống, có các mốc người (E6 §3.1–3.2).
- Hình 4: biểu đồ thác CAR cho UPE, PLAN-F1, knapsack, sau trung bình Shapley (M6 §3e; X1 §2d).
- Hình 5: phân bố residual của 85 run, theo họ hệ thống (X1 §3b).
- Bảng: thẻ giao thức và stress set (E4 §3); biên theo loại tuple (G1 §3a); kết quả âm đăng ký trước (Bảng B9, gồm N11).

---

## 4. Ứng viên phương pháp, xếp hạng

Xếp theo: hợp lệ với endpoint của PD-2 × xác suất qua / chi phí. Thứ tự brief (M3, M4, M6, M5, M1) đổi ở ba điểm: M4 xuống cuối vì D14; M6 lên thứ 2 nhưng có điều kiện; M1 trước M5 vì rẻ hơn và P cao hơn (20% so với 10%).

| Hạng | Ứng viên | P(qua), theo báo cáo | GPU-h (lần đầu / đủ) | Endpoint bắt buộc | Điều kiện trước khi chạy |
|---|---|---|---|---|---|
| 1 | **M3** CM-DPO | T1 trên test ~25–30%; null 60–70% (M3 §0, §6) | 4.2 / ~33 | PD-2 cho phương pháp huấn luyện: residual biên ở số lượng của chính run + Δresidual ghép cặp so với P1_dev và C2. **Đề xuất thêm:** Δρ_I trên panel làm tiêu chí đồng-chính; báo cáo CAR | Pin matcher; panel đồng-chính; thêm guard sao chép kiểu G4; tính lại phép chia người chú thích với ref 0–1 → 3–4; xác nhận D14 không bao trùm DPO |
| 2 | **M6** knapsack (có điều kiện) | Báo cáo không nêu; dev p .028–.044 với ~6 nhánh (M6 §6) | 0 (M6a/b) / 1.7 (M6c) | ΔF1 mức tập so với greedy tại Δm = 0 (khớp TỔNG) + phần B của CAR; đối chứng từng ảnh của PD-2 cho ≈ 0 theo cấu trúc (+0.09) | Judge thêm endpoint "khớp tổng"; nếu không, M6 chỉ là đóng góp đánh giá. P-M6b (CPU, test) phải qua trước M6c |
| 3 | **M1** grounding | ~20% (M1 §0) | 1.0–1.3 / ~6.6 | Đối chứng từng ảnh (tie-avg thay cho POOL-VOTE) tại k_i của PLAN, greedy và top-3: thuần phần A | Gộp G-SAL của M2; đánh dấu [MH] |
| 4 | **M5** k theo từng ảnh | Vượt biên ~10%; H0 ~75% (M5 §0) | 2.4 / ~9 | CẢ HAI: (a) residual biên; (b) phần xếp hạng so với top-m_i theo R ở cùng k_i | Sau CAR của M6 (phân rã đã làm được trên CPU) |
| 5 | **M4** CS-RLOO — **cần mở lại nhánh RL** | ~25% (M4 §0); P(GO) ~0.3 (§4e) | 4.0 / ~22 | Dev: cm (= phần A); test: residual biên 3 seed. **Đề xuất thêm:** Δρ_I ≥ 0 bắt buộc; CAR | D14 đóng nhánh RL ("no further RL runs"); theo M4 §4a, kill không sạch thì engine không tin cậy; phải chẩn đoán G4 (chép ref tăng 3.4 lần) trước |

**Tương tác phải ghi rõ trong bản đăng ký trước**

1. **Goodhart (E6) ↔ M3/M4.** Nhãn thắng/thua của M3 và phần thưởng của M4 đều đọc hợp 5 ref KTVIC của từng ảnh huấn luyện. Chọn lọc có đọc ref chỉ chuyển sang panel với κ = 0.19 (E6 §3.3), còn huấn luyện lại ở chế độ "khoá" (E6 §3.1); chưa biết M3/M4 thuộc chế độ nào. 35_e là ví dụ đã chấm: CIDEr KTVIC +1.57 (không có ý nghĩa) nhưng CIDEr panel −0.5 [−3.7, +2.6] (D14). Vì vậy kiểm tra phía sự thật phải là tiêu chí CHÍNH: ρ_I khớp số lượng trên panel OpenViIC (dev300 có panel cho 296/300 ảnh: E3 §3, M1 §3a), và precision trên nhãn instance COCO (nhánh A+C của M3; UIT-ViIC val). Hiện M3 để panel "phụ, không làm cổng" (M3 §4), M4 "báo cáo, không làm cổng" trên dev (M4 §4c). Đề xuất cho judge: ở test, Δρ_I > 0 với cận dưới > 0; ở dev, κ = Δρ_I/Δρ_A ≥ 0.35 (ngoài vùng tách rời theo H3 của E6); báo cáo kèm G. [SUY] Nếu κ = 0.19 đúng cho phép chia người chú thích của M3 (+4.64), phần sang panel chỉ còn ~+0.9 F1.
2. **Endpoint riêng cho từng phương pháp (M6).** M1: thuần phần A. M5: phần A + residual biên. M6: khớp tổng + phần B. M3, M4: residual biên + CAR, để chứng minh lợi ích nằm ở A chứ không ở B. Với M4, cm trên dev không thấy cải thiện phân bổ còn residual trên test thì thấy: hai endpoint đo hai thứ khác nhau.
3. **Sao chép tham chiếu (35_e G4) ↔ M3.** 35_e trượt G4 trên đúng 1,000 ảnh huấn luyện mà M3 dùng (M3 §3f: cùng ảnh, cùng adapter khởi đầu P1_dev). Builder của M3 chỉ bỏ cặp có độ sao chép m ≥ 0.90; cổng G1–G5 không có guard tỉ lệ chép. Đề xuất thêm guard cùng dạng G4 (≤ 2 lần tỉ lệ của mô hình khởi đầu).
4. **Hằng số biên khớp trên test (M4 §3b(v)).** Đã đối chiếu `manuscript/prereg/2026-10-12_ladder_predictions.json`: "metric" ghi "union of the 5 test references, 558 images". Không đưa hằng số này vào hàm mục tiêu huấn luyện hay vào luật chọn lọc tinh chỉnh trên dev (CS của M4 và builder của M3 đã tuân theo). Trên dev chỉ dùng Δ ghép cặp với guard |Δm| (M3 ≤ 0.20; M4 ≤ 0.15), khi đó hằng số gần như không còn ảnh hưởng.
5. **Cùng một trần thông tin.** mr5assist (SFT trên đủ 5 ref) vẫn nằm trên biên: +0.25 [−2.10, +2.54] (M4 §3f, M5 §3). M3 và M4 đọc đúng thông tin ấy, chỉ dùng khác (tương phản on-policy ở cùng số lượng). 35_e (CIDEr trên cùng ref) cho Δresidual +1.46 không có ý nghĩa (D14). [SUY] Nếu M3 bị KILL sạch, M4 nên bị bỏ hẳn.
6. **Đối chứng và pool.** M4: 8 rollout T1.0; M1/M2/M6/PLAN: 13 caption T0.5 + T0.8; M6/M7 trên test: 7 caption; M5 trên test: 19. Thống nhất bằng đối chứng tie-avg (X1 P-A); M4 vốn dùng "ties at expected TP", tương đương.
7. **Matcher.** Nhãn và phần thưởng của M3/M4 dùng objects_in v2, thừa hưởng lỗi loại từ, từ ghép, quan hệ cấp trên của người (V1 §1, §5.3; V3 §0). Pin hash matcher trong builder; chấm lại với v3 như phân tích độ nhạy.
8. **Guard CIDEr.** Lỗi dấu câu (E4) có thể đánh trượt oan một phương pháp (M3: CIDEr dev ≥ 141.33; M4: control − 3; M6c: greedy − 5). Đăng ký trước guard nào ràng buộc: P0 hay P7 (bỏ dấu câu).
9. **Chuỗi diễn giải giữa ref kề nhau** (E6 §3.3; G3 §5.9). M3 chọn bằng ref 0–1, chấm bằng 2–4; ref 1 và 2 kề nhau nên có thể rò rỉ. Tính lại với 0–1 → 3–4 (M4 đã dùng {0,1} và {3,4}).
10. **Mẫu sinh ra nằm dưới biên** (M6 §3h; G2 §3d). Không chấm rollout T1.0 (M4) hay pool mẫu (M3) bằng biên greedy.
11. **G3 H4.** Chỉ tín hiệu ngoài bằng chứng của mô hình mới đổi được s. Ref của người là tín hiệu ngoài (M3, M4); grounding của base model ngoài một phần (M1); vote của chính mô hình là tín hiệu trong (M5, M6). Lợi ích của M6 nằm ở phân bổ, không ở s (xem MT12).

**Tín hiệu do mô hình tạo [MH] bên trong các ứng viên** (nhãn luôn là ref người hoặc nhãn instance COCO):
- M1: P(có), hộp grounding, attention của Qwen2.5-VL. M2 G-SAL: hộp grounding.
- M3: pool mẫu của chính policy (làm ứng viên cặp). M4: rollout của policy.
- M5: vote của pool để đặt k_i. M6: vote và q; bộ hiệu chỉnh q lấy vote làm đầu vào, được khớp trên ref người theo cross-fit.
- M7: vote quyết định câu rào đón. G2 của M7 còn đưa vote của P1_dev vào chính đích SFT.
- V1: bảng từ vựng do agent soạn, cần người ký duyệt. E3 bước 4: embedding. V2 S5: P(có) của probe.

---

## 5. Mâu thuẫn và những điểm cần thống nhất giữa các báo cáo

**MT1. Matcher: ba định nghĩa, hai phiên bản, ba đề xuất "v3".**
- Ba định nghĩa "cùng đối tượng" (V1 §1c): CHAIR và upe_mbr gọi canonical(); object_prf ktvic_block và prereg_ladder_check (L158/L166) thì không.
- Phiên bản trôi: PLAN-F1 chỉ tái lập với fd1d0123 = v1 (M6 §3a, §5.1). M2, E2, X1 §3a dùng v1 (RESCAP_RAW_TONE=1); M1, M3, M4, M7, E3, E5, E6, X1 §3b dùng v2.
- "v3" bị đề xuất ba lần với ba nội dung: V1 (loại từ, từ ghép, phủ định, gộp lớp bị tách); V3 (liên kết cấp trên cho danh từ chỉ người); E3 L1 (đồng nghĩa, "dù = ô").
- **Thống nhất:** một bộ v3 duy nhất gồm các phần đặt tên rõ; bảng soạn lại trên train-minus-dev300 và có người ký duyệt, vì bảng hiện tại do agent soạn [MH] (V1 §4 bước 0). v2 vẫn là matcher chính (PD-2 blocker 6).

**MT2. UPE là "dịch chuyển số lượng thuần" (D11; E5 §3b; E6 §3.4; G2 §3d) hay "không thuần" (M6 §3e)?**
- Hai bên đo hai thứ khác nhau: D11 đo phần A (so với đối chứng từng ảnh); M6 phân rã lợi ích so với greedy.
- Trên dev chỉ phần C có ý nghĩa: +0.92 [+0.52, +1.32]. B +0.62 [−0.38, +1.71] và D +0.57 [−0.55, +1.77] đều có CI chứa 0.
- Theo file gốc, kill-2 tính trên gold panel; JSON không có Δ so với COUNT trên gold KTVIC. Telescoping phụ thuộc thứ tự (X1 §2d). Residual UPE của G2 chỉ là suy ra gần đúng (G2 §5.5).
- **Đề xuất câu chữ:** "UPE không có lợi ích nào so với đối chứng vote cùng số lượng; lợi ích so với greedy là số lượng, cộng phân bổ và xếp hạng lại theo vote, hai phần sau không có ý nghĩa trên dev." Chạy P-M6a trên test với Shapley, trên cả gold KTVIC lẫn panel.

**MT3. Hằng số biên khớp trên test.** M4: cấm dùng trong huấn luyện. M3, M5 và residual "official" của M6: dùng biên chính thức làm cổng dev. G2: không mang b sang gold hay tập ảnh khác. M4 §3b(v): không khớp lại được trên dev300 vì fuse2 đã huấn luyện trên các ảnh đó. **Thống nhất:** biên chỉ là công cụ đánh giá; trên dev dùng Δ ghép cặp có guard Δm; báo cáo cả bản "official" lẫn bản neo trên dev (như M6).

**MT4. Định nghĩa đối chứng cùng số lượng.** PD-2: (v, g), hoà còn lại không quy định. M2: POOL13 làm chính, điều kiện qua là thắng max của họ biến thể xác định. X1: s_N trung bình hoá phá hoà làm chính, điều kiện qua là thắng max của họ tie-avg, và "không lấy max qua các cách phá hoà tuỳ ý". M1: POOL-VOTE 12v+g (59.37 với v2; M2 ra 59.90 với v1). M4: 8 rollout, hoà chia theo TP kỳ vọng. M5: phá hoà theo thứ tự mention của greedy rồi theo tên. Biến thể xác định trải 58.87–59.90; họ tie-avg chỉ 59.22–59.60 (X1 §3a). **Đề xuất:** (v,g) tie-avg làm chính (giữ đúng câu chữ ràng buộc của PD-2); họ tie-avg của X1 để kiểm tra độ vững. Judge quyết định.

**MT5. Đơn vị residual và "đường bao".** G2 §3c: tags_fuse2-detailed +1.75 P, CI loại 0, nằm TRÊN biên. X1 §3b: 0/85 run có CI residual (đơn vị F1) trên 0. E6: cùng hệ thống ρ_A +2.4 [−1.2, +5.5] (%TP). **Thống nhất:** một đơn vị (residual F1 cho claim theo PD-2) và một cách bootstrap.

**MT6. Ba phép phân rã.** E1: TRF/MCP. M5: xếp hạng/phân bổ/nền, tham chiếu là phân bổ đều. M6: CAR, tham chiếu là phân bổ của greedy. Phần phân bổ của PLAN-F1: +0.68 (M5) và −1.08 (M6), cả hai đúng vì tham chiếu khác. Phần xếp hạng của PLAN-F1: −0.95 so với POOL13, +0.08 so với RAW, −0.27 so với (v,g) tie-avg. **Đề xuất:** CAR có Shapley; MCP của E1 là bản tương ứng cho tiếng Anh.

**MT7. "Oracle count".** M5 dùng k_i = min(|G_i|, 4) và kết luận "oracle chỉ chạm biên" (−0.39). M6: cấp k_i theo |G_i| thật còn tệ hơn phân bổ đều (−2.58), còn oracle "dừng khi biết gold" cho +14.7. Câu ở M5 §0 phải sửa: dưới macro-R, kích thước gold là oracle sai.

**MT8. Phạm vi bất biến của biên.** CONTEXT §2 viết "giữ trên mọi run", nhưng biên lệch ở: zero-shot trong dải số lượng (−29.7%, G1); zero-shot −19 đến −25 P và legacy −25 đến −46 P (G2); P1 trên gold instance UIT-ViIC (−5 P, G2); mẫu T0.8 (M6 §3h); self-fusion (G3); 4/32 hệ thống ladder (G1, G2). Câu đúng: "đầu ra greedy của các hệ thống huấn luyện trên KTVIC, chấm trên ref KTVIC".

**MT9. b ở k nhỏ.** G2: 0.403 tại k = 1 (OLS, k ref đầu theo thứ tự file). G3: 0.561 tại h = 1 (hai anchor, mọi tập con). Ref KTVIC có "chuỗi diễn giải" (ref kề nhau giống nhau), nên tập con theo thứ tự file bị lệch. Chạy G2-C.

**MT10. Ba mô hình cho quá trình tham chiếu, trên cùng dữ liệu tần suất.** E2: M_h với K = 3, N̂ 4.87–5.50. E5: BB cắt cụt a = 0.448, b = 1.315, tiệm cận 6.9. G3: BB a = 1.63, b = 2.43 với Chao2, N = 4.37 (U(5) bị khớp thiếu 0.14). Cả ba đều giả định người chú thích hoán đổi được, mà giả định này bị vi phạm. Bài báo chỉ nên dùng một mô hình, kèm cận dưới Chao.

**MT11. "Phần hệ thống" D không phải ảo giác.** 79% của (1 − b) gộp cả vật thật mà hướng dẫn KTVIC không cho gọi tên (G3 §1). Với hệ FT, E2 cho phần ảo giác chỉ 1–4 điểm; G2 thấy phần lớn độ suy giảm là vật thật chưa có trong ref. G3-C và G3-D sẽ tách.

**MT12. G3 H4 và M6.** G3: phương pháp dùng bằng chứng nội tại giữ nguyên s. M6: phân bổ theo vote vượt biên khi m < m* ≈ 2.4. Bằng chứng của G3 lấy ở m ≥ 2.6 (PLAN-F1). P-M6b sẽ phân xử.

**MT13. File "MBR" không phải UPE-MBR.** G1, E5, V3, E4 và X1 §3c phân tích p1_s43mbr và fuse2_s42mbr. UPE-MBR không lưu lựa chọn thành preds (G2 §3d; G1 §4A.3). Nguồn gốc các file MBR chưa xác minh (G1 §5.5).

**MT14. Lệch 0.06–0.08.** Recall của P1_dev 43.13 so với 43.07 (M3, M7); precision 1v4 của người 85.25 so với 85.33 (G3, V1); within 60.43 so với 60.50 (E3). Hai lời giải thích: phiên bản matcher, và gộp thay cho trung bình theo fold. D14 xác nhận v1 cho 43.07, v2 cho 43.13 trên dev300 (`data/results/rl/`), tức phần recall là do matcher. Hai lệch còn lại để Gemini phân xử.

**MT15. Đổi trục có đổi thứ hạng không?** E6 §1(ii): không, trong nhóm FT. E4: τ_FT −0.05 (CIDEr trên panel). E3: τ 0.546 (F1 đối tượng, không khớp số lượng). Ba metric khác nhau; cần thêm Kendall τ giữa ρ_A và ρ_I trong 36 hệ thống FT, có CI.

**MT16. Định vị E1 và E6.** MCP thiên lệch do cắt cụt, nghiêng về phía bị cắt (X1 §2d, §6; E1 §6 đã tự ghi). Cần thêm TRF và tập con ngẫu nhiên tie-avg. E1, G2, E6 chưa trích LeHaCE. §2 của E6 còn chỗ trống "<<REFS>>": thiếu danh sách công trình liên quan.

**MT17. Các lần đã nhìn test cần công bố.** E3: một lần nhìn khám phá, script đóng băng. V1: khám phá luật trên ref TEST, bảng phải soạn lại. E6: biên I khớp trên test. G1: biên tuple khớp trên đầu ra test. X1 §3b–3c: hậu kiểm trên bảng test. E2, E4, E5, G2, V3, M7: đọc test để mô tả. Chỉ dùng dev: M1–M6.

**MT18. Trùng lặp.** G3-E ≈ "votes + prior" của M2, vốn đã ÂM (−1.22 [−2.29, −0.22]). G-SAL của M2 ≈ GEOMETRY_ONLY của M1. Phân rã M5 ≈ CAR của M6. E2/E5/G3: ba mô hình propensity (MT10). V1/V3/E3: ba bản sửa matcher (MT1).

**MT19. G2-B và PD-2 Q5.** G2-B chạy Qwen3-VL-8B zero-shot trên COCO-2500, chạm vào thiết kế S0 mà PD-2 Q5 đã bác (probe bị nhiễm). Endpoint của G2 là Δb, không phải mức tuyệt đối. Judge phán quyết.

**MT20. Endpoint của M4.** M4 dùng cm (đối chứng từng ảnh) làm endpoint chính trên dev cho một phương pháp HUẤN LUYỆN, trong khi PD-2 định nghĩa endpoint huấn luyện là residual biên; M3 dùng d-res. Hiện chưa cấp thiết (M4 bị chặn), nhưng phải sửa trước khi mở lại.

**MT21. 35_e đã có kết quả (N11), nên mục "đăng ký trước cho 35_e" không còn áp dụng.**
- Dự đoán của M4: C1, C3, C4 đúng. C2 trượt sát trên endpoint cm của chính M4: +2.07 [−0.20, +4.27], ngưỡng ≤ +2.0 (Gemini đã tính bằng m4_endpoint.py). Nếu đọc theo residual biên (+1.46) thì C2 đúng (§1).
- E6 H4 khớp nhưng yếu: KTVIC CIDEr +1.57 không có ý nghĩa (tiền đề "RL làm tăng CIDEr" chưa được đáp ứng); CIDEr panel −0.5; ρ_I đối tượng chưa tính.
- V3 H4 mới một phần: fragment 9 → 12 (vẫn qua guard G2), chưa có CI.
- Dự đoán trong E6, V3, G1, G3 được viết trước verdict (báo cáo ghi lúc 08:51–08:59 +07; 35_f/35_g thoát lúc 03:19 UTC = 10:19 +07) nhưng không nộp vào `manuscript/prereg/`. Bài báo chỉ gọi chúng là "dự đoán có dấu thời gian", không phải đăng ký trước.
- Không có lần decode test nào, nên G1 H1 và G3 H4 chỉ chấm được trên dev, dưới dạng mô tả.
- Δresidual +1.46 dương nhưng chỉ một seed, CI ±2.2: "phù hợp với bất biến", không phải "chứng minh không có hiệu ứng".

**MT22. Phần ảo giác còn lại của E2 chỉ là cận trên.** Nó dựa trên giả định độ nhạy của panel bằng người (58.78%, E2 §5.9), trong khi panel là thước đo sự thật bảo thủ, hụt 11–46 điểm (E6 §3.6), và kiểm tra dựa trên caption đánh giá thấp 3–6 lần (V2 §3A).

---

## 6. Khuyến nghị ưu tiên cho judge

### 6.1 Ngay lập tức, không tốn compute

1. **Ghi nhận N11 (D14) và kết quả các dự đoán.** Đưa 35_e vào Bảng B9. Ghi thêm một kết quả phương pháp luận: dự đoán đăng ký trước của M4 cho RL chỉ thưởng CIDEr (trung tính về đối tượng ở số lượng khớp) đúng 3/4. C2 trượt sát: cm +2.07 so với ngưỡng +2.0, dù CI vẫn chứa 0. Đây chỉ là bằng chứng một phần cho luận điểm bất biến của biên ở một phương pháp HUẤN LUYỆN, và phải báo cáo đúng là 3/4.
2. **Phán quyết về endpoint:**
   - (i) Đối chứng chính là (v,g) tie-avg; họ tie-avg để kiểm tra độ vững (X1, M2; MT4).
   - (ii) Thêm endpoint "khớp tổng" và phần B của CAR (Shapley) cho phương pháp phân bổ (M6; MT2, MT6).
   - (iii) Phía sự thật (ρ_I, nhãn instance COCO) là tiêu chí đồng-chính cho M3, và cho M4 nếu mở lại (E6).
   - (iv) Guard CIDEr tính dưới cả P0 và P7 (E4). Thêm guard tỉ lệ sao chép kiểu G4 cho M3 (35_e).
   - (v) Pin matcher; v3 chỉ là phân tích độ nhạy (MT1).
3. **Quy tắc:** không hằng số biên nào đi vào hàm mục tiêu huấn luyện hay luật chọn lọc tinh chỉnh trên dev (M4; MT3).
4. **Làm rõ phạm vi D14:** câu "no further RL runs" có bao trùm DPO (M3) không? M3 không phải RL, nhưng dùng cùng 1,000 ảnh và cùng adapter khởi đầu.

### 6.2 Phân tích chỉ dùng CPU: Gemini chạy trước (rẻ, giá trị cao), theo thứ tự

Mọi job chạy với `nice -n 19`, 1 luồng, mỗi lần một job.

| # | Việc | Báo cáo | CPU-h | Vì sao đứng ở vị trí này |
|---|---|---|---|---|
| 1 | Pin công cụ đo: một canonicalisation; hash matcher; x1_ties trên dev và test | V1 bước 2, M6 §5.1, X1 P-A | ~0.3 | Mọi việc phía sau phụ thuộc |
| 2 | CAR với Shapley cho UPE (dev và test, gold KTVIC và panel); Δ UPE − COUNT trên gold KTVIC | M6 P-M6a, X1 §2d | ~0.3 | Giải MT2 |
| 3 | Chấm hậu kiểm 35_e trên dev (gắn nhãn "post-hoc"): cm của M4 (m4_endpoint.py), ρ_I khớp số lượng (E6 H4), CAR, tuple của G1, s1/D của G3, k* của E5, lớp lỗi của V3 có CI | M4, E6, M6, G1, G3, E5, V3 | ~0.4 | Đóng C2 của M4 và H4 của E6; file đã có trong `data/results/rl/` |
| 4 | Bootstrap D(h) qua các cặp hệ thống; G2 chạy lại, b(k) trên tập con ngẫu nhiên | G3 A–B, G2 A + C | ~0.6 | Kiểm chứng lõi lý thuyết; luật dừng rẻ |
| 5 | E1 pha A chạy lại, thêm placebo và đối chứng dương; thu thêm repo (A2); X1 P-B (độ dài so với số lượng trên tiếng Anh) | E1, X1 | ~1.6 | Phát hiện có giá trị trích dẫn nhất |
| 6 | E6 P0 (CI; đối chứng chọn lọc khớp số lượng) và P2 (khối two_gold_audit) | E6 | ~0.3 | Định cổng phía sự thật cho M3 |
| 7 | E3 bước 0–2 (đăng ký tầng; endpoint chéo gold khớp số lượng) | E3 | ~0.5 | Metric hai tầng |
| 8 | E4 S1–S3 (pycocoevalcap chính thức; bảng ý nghĩa thống kê vững theo giao thức) | E4 | ~1.5 | Mọi claim CIDEr |
| 9 | G1 A1–A4 (wrapper xuất lựa chọn UPE, dùng chung với #2, E5, V3) | G1 | ~0.5 | Tổn hại quan hệ (H5) |
| 10 | Một bộ v3 gộp từ V1 và V3 P-B; V3 P-A (cờ đếm, cần CPU cluster 3 GB); V3 P-C | V1, V3 | ~1.5 | Tính vững của matcher |
| 11 | E5 S1–S3; E2 bước 1–3; M7 C1–C2 | E5, E2, M7 | ~1.5 | Các mục phân tích |
| 12 | P-M6b trên test (sau khi đăng ký trước endpoint khớp tổng) | M6 | ~0.1 | Phân xử MT12; là cổng cho M6c |

### 6.3 Pilot GPU, theo thứ tự

Chạy sau, hoặc xen kẽ với, các blocker 3–5 của PD-2 (ladder ~20 GPU-h). Judge quyết định cách xen.

| # | Pilot | GPU-h | Điều kiện | Lý do |
|---|---|---|---|---|
| 1 | M3 CM-DPO, stage 1 | 4.2 | Panel đồng-chính; guard sao chép; pin matcher; D14 không bao trùm DPO | Endpoint hợp lệ theo PD-2; P ~25–30% |
| 2 | M1, sàng lọc grounding trên dev (gộp G-SAL của M2) | 1.0–1.3 | Đối chứng tie-avg | Rẻ; luật dừng cứng; kiểm tra tín hiệu "nằm ngoài" theo G3 |
| 3 | M6 P-M6c, knapsack trên test | 1.7 | Judge chấp nhận endpoint khớp tổng VÀ P-M6b qua | Ứng viên duy nhất đã dương trên dev |
| 4 | E6 P1, đường cong Goodhart | 2.0 | — | Trụ cột đánh giá; hiệu chỉnh κ cho cổng của M3 |
| 5 | G2-D (XM3600, job 39 có sẵn), rồi G2-B | 1.5, rồi 7–9 | G2-B chờ phán quyết MT19 | Tính tổng quát của luật |
| 6 | M5 trên dev | 2.4 | Sau CAR của M6 | P ~10% |
| 7 | Mở rộng đánh giá: M7 G1; G1-C; X1 P-C; V2 S1–S4; E1 pha B | 1.5; 4; 0.5; 9–10; 15–30 | E1-B chỉ sau A2 và P-B | Tổng quát hơn nhưng tốn |
| 8 | M4 CS-RLOO, lần nhìn đầu | 4.0 | **Cần mở lại nhánh RL (D14)**; chẩn đoán G4 xong; M3 không bị KILL sạch | Cùng trần thông tin với M3; M4 §4a cấm chạy sau kill không sạch |

**Đợt GPU đầu (#1–#4): khoảng 9 GPU-h** (8.9–9.2). #3 có điều kiện. RL đã tiêu 3.79 GPU-h (theo coordinator; D14 ghi riêng huấn luyện 3.153 GPU-h).

### 6.4 Không nên chạy (hoặc gộp lại)

- GPU riêng cho M2: gộp vào M1.
- G3-E: M2 đã trả lời, kết quả âm.
- G2-B: chưa chạy khi judge chưa phán MT19.
- E1 pha B: chưa chạy khi chưa có A2 và P-B.
- M5: chưa chạy khi CAR chưa chạy.
- M4, 35_f, 35_g: chưa chạy khi D14 chưa được mở lại.
- Lấy max qua các cách phá hoà xác định (X1 §2d): cách này chọn theo nhiễu.
