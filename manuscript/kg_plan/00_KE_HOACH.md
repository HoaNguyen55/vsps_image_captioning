# Kế hoạch lớn: Image captioning tiếng Việt với Transformer + Đồ thị tri thức — **bản v2** (sau vòng phản biện 2, 2026-10-10)

Nguồn: vòng 1 `01..20_*.md`; vòng 2 `R2_01..R2_06_*.md` (11 BLOCKER, ~35 MAJOR); bản trước `00_KE_HOACH_v1.md`. Số "ước tính" là của agent, **chưa đo**, trừ khi ghi "đo được". Mọi "chưa có ai làm" viết là **"chưa tìm thấy"**.

## 0. Thay đổi so với v1 (mỗi dòng xử lý một BLOCKER)

| # | BLOCKER vòng 2 | Xử lý trong v2 |
|---|---|---|
| B1 | Tự trùng với VSPS (salami) — R2-04 | Bảng phân đóng góp (mục 6): mỗi đóng góp thuộc đúng một bài; P2 lấy VSPS làm baseline chính, chỉ claim phép lùi phân cấp có KG cho caption |
| B2 | Lùi IsA không phải LOW (CLC NeurIPS'25, CSS, SpeciaRL CVPR'26, Conformal Factuality; "người phụ nữ→người" chính là VSPS) — R2-01, R2-04 | Hạ xuống **MED về ý tưởng, chưa tìm thấy cho caption**; claim thu hẹp: lùi *có cấu trúc theo KG* cho cả thực thể **và vị từ quan hệ** trong caption; baseline bắt buộc: viết lại kiểu CLC không dùng KG |
| B3 | Reward phụ thuộc cha–con đã có (2604.01460 COLM'26 trong reward GRPO; FoCUS) — R2-01 | E3 bỏ khỏi đóng góp; chỉ còn ablation trong bản mở rộng, baseline = reward có cổng hai đầu |
| B4–B7 | M1 khoảng precision sai mẫu số và không xếp hạng được; gold 3 trạng thái không mới (M-HalDetect, HalDec-Bench); PDG không định nghĩa được — R2-02 | M1 định nghĩa lại (ước lượng điểm + danh sách từ rỗng + điểm độ cụ thể); gold do người gán **mù** verdict máy; PDG thay bằng "chênh lỗi có/không có ảnh trên chính caption" |
| B8 | "Bộ chấm điểm caption tiếng Việt đầu tiên" sai (Crossmodal-3600 EMNLP'22 đã chấm người tiếng Việt, không công bố) — R2-03 | Claim thành **"đầu tiên được công bố, ở cấp caption và cấp mệnh đề"**, trích XM3600; thêm 100–150 ảnh XM3600 (CC BY 4.0) để phát hành được |
| B9 | Giờ công 815–990 vượt năng lực đội (300–450) — R2-06 | Kế hoạch MVP ~200 giờ người gán + ~90 giờ NCS (mục 8) |
| B10 | Rò dữ liệu: 401/558 test và 2.464/3.769 train KTVIC trùng UIT-OpenViIC (ViCLIP-OT 2602.22678) — R2-06 | Tuần 1: dedup all-vs-all (SSCD, <2 GPU-h); test gold dựng lại từ ảnh sạch; **đo cả trùng train↔test nội bộ KTVIC cho bài VSPS** |
| B11 | Verifier logit chưa kiểm, hỏng thì mất ~1.150 GPU-h — R2-05 | Cổng **T0.5** trước mọi lượt dựng đồ thị; chỉ dựng cho KTVIC/OpenViIC sạch, không làm nhánh 20k |

## 1. Phản biện tổng thể (cập nhật)

| Thành phần | Trùng lặp | Tính mới còn lại | Khả thi | Quyết định |
|---|---|---|---|---|
| KG ngoài bơm vào generator; adapter graph-token; encoder quan hệ | HIGH | — | — | **Bỏ** |
| Reward SG (phẳng hoặc có cổng hai đầu) | HIGH | — | trung bình (GRPO cần vòng lặp tự viết, 10–15 h/run) | Baseline/ablation, bản mở rộng |
| Lọc SG dự đoán bằng VLM | MED-HIGH | — | cao | Kỹ thuật |
| **Lùi phân cấp có KG cho thực thể + vị từ trong caption** | MED (CLC, CSS, SpeciaRL; chưa tìm thấy cho caption) | trung bình: có cấu trúc (IsA/vị từ), gắn trạng thái kiểm chứng, đánh giá trên caption, tiếng Việt | cao | **Lõi P2** — phải thắng viết-lại-CLC và lùi-sau-sinh |
| GEPA (preference cục bộ từ sửa đồ thị) | MED (loss = HALVA/DPA mức cụm; SceneAlign cho VQA) | nguồn negative từ đồ thị kiểm chứng + node REJECTED | trung bình | Thành phần P2, **không claim loss mới** |
| Graph-then-caption SFT | MED (CCoT, SaGe) | — | trung bình (train ×1,5–1,7, suy luận ×3–4, ước tính) | Thành phần P2, so với caption-only |
| Metric M1 (ViVG-P/R sửa) + H-R | MED (PoSh, DSG, HalDec-Bench, Taxonomy-Aware Eval chấm văn bản tự do bằng P/R phân cấp) | tiếng Việt + gold người mù verdict + điểm độ cụ thể + xử lý từ rỗng | cao | **Lõi P1** |
| Bộ chấm điểm người cấp caption + mệnh đề tiếng Việt | MED (XM3600 có chấm VN nhưng không công bố) | công bố được, cấp mệnh đề | cao | **Lõi P1** |
| Gold SG tiếng Việt trên ảnh sạch | MED (VietSGG có box, ảnh thể thao) | caption chi tiết, ảnh đời sống, 3 trạng thái | cao | Lõi P1 |
| Parser caption→SG tiếng Việt | chưa tìm thấy parser VN | trung bình | cao | P1; luật +3 F1 so với **2 baseline**: dịch→FACTUAL và AMR (viSemParse)→SG |
| M2 lỗi quan hệ (định nghĩa lại) | MED (R-Bench, CDH-Bench, VLind-Bench) | trên caption tự do tiếng Việt | cao | P1, phụ |
| M4 văn hóa | MED (M²CQA, VietMEAgent Cultural Accuracy, RAVENEA có captioning) | — | cao | **Phân tích**, không claim metric |
| M5 TBW | ≈ 1 − precision verifier | — | — | **Chẩn đoán**, không claim |
| M6 NVL | tự thiên vị phương pháp | — | — | **Thay** bằng tỷ lệ "nội dung không kiểm được từ ảnh" do người chấm cho mọi hệ |
| Entity/news captioning; captioner nhỏ | MED-HIGH / phụ thuộc | — | thấp | **Hoãn**; GRIT chỉ là baseline |

**Kết luận v2.** Đóng góp sống sót là hẹp và cụ thể: (P1) tài nguyên đánh giá tiếng Việt công bố được + metric đồ thị biết độ cụ thể; (P2) phép lùi phân cấp có KG cho caption, chứng minh hơn cả viết-lại-bằng-LLM và lùi-sau-sinh, không đánh đổi bằng "nói ít đi". Chuỗi đầy đủ vẫn "chưa tìm thấy" (bài nhiều nhất ghép 2 mắt xích).

## 2. Phương pháp P2: **ViHG-Cap** (bản MVP)

```
Ảnh (train sạch) ─► (A) mệnh đề Stage-1 VSPS có sẵn + box OWLv2/Florence-2 (khác họ Qwen)
                 ─► (B) kiểm chứng 3 trạng thái:
                        cổng cấu trúc mệnh đề (bỏ phủ định kép, tách object khỏi vị từ)
                        Vintern logit P(Có)/P(Không) một lượt  ── cổng T0.5
                        hình học từ box: chỉ được NÂNG, không bao giờ REJECT vì thiếu box (sửa luật verify.py)
                 ─► (C) lùi phân cấp UNCERTAIN: thực thể theo IsA (Wikidata subset đóng băng + bảng tay ~250 dòng,
                        KG văn hóa ≤100 thực thể); vị từ: đang cưỡi → ở trên → ở gần → chỉ giữ thực thể
                        REJECTED → negative cho (E2)
                 ─► (D) đồ thị G* ─► (E1) SFT graph-then-caption, Qwen2.5-VL-7B, 3 seed (+ caption-only để so)
                                  ─► (E2) GEPA một biến thể (cụm bị sửa + KL theo token)
```

Backbone thứ 2 (chuẩn tạp chí): **Qwen2.5-VL-3B** cùng môi trường (Qwen3-VL-8B cần env riêng vì transformers 4.51.3 → bản mở rộng). Sửa lỗi `qwen_vl.py` nạp checkpoint Qwen2-VL bằng class Qwen2.5 trước khi dùng R1-SGG.

**Baseline bắt buộc của P2**: zero-shot Qwen2.5-VL-7B; SFT trên caption zero-shot không kiểm chứng; **VSPS** (bảng đối đầu chỉ đổi phép lùi: xóa vs neutralize giới tính vs lùi phân cấp KG); **viết-lại-CLC** (LLM viết lại span UNCERTAIN bớt cụ thể, không KG); **lùi-sau-sinh** trên zero-shot; HALVA; RLAIF-V-7B; GRIT; decoding VCD/DoLa. Đối chứng đồ thị xáo trộn.

**Chống "nói ít đi" (SCAPO 2609.35294)**: luôn báo số claim đúng/caption, H-R và điểm độ cụ thể cạnh CHAIR/M1-P; không claim "không mất thông tin" nếu H-R giảm > 2 điểm.

## 3. Độ đo P1 (định nghĩa sửa)

- **M1 ViVG-P/R**: P = (claim khớp node SUPPORTED-gold + ước lượng tỷ lệ đúng của claim khớp UNCERTAIN-gold và claim không khớp, từ 50+50 claim/hệ người kiểm) / (mọi claim trừ từ rỗng). Từ rỗng ("vật", "có", "ở gần"…) báo riêng. Thuộc tính/quan hệ của object bịa tính là lỗi. Kèm **điểm độ cụ thể trung bình** (độ sâu IsA). R có trọng số độ nổi bật, tách salient/exhaustive.
- **H-R**: recall phân cấp, điểm một phần cho tổ tiên đúng (trích Taxonomy-Aware Eval, khác ở caption tiếng Việt + vị từ).
- **SFA (định nghĩa lại)**: áp **một phép lùi sau sinh chung** k = 0..3 mức cho *mọi* hệ, vẽ đường Trung thực–Độ cụ thể; so diện tích ở cùng dải độ cụ thể. ViHG-Cap phải hơn baseline mạnh nhất + lùi sau sinh.
- **M2**: với mỗi quan hệ trong chính caption, chấm đúng/sai; chia quan hệ theo mức ảnh làm đổi log-prob (có ảnh vs ảnh trống/che); báo chênh tỷ lệ lỗi giữa nhóm "ảnh hầu như không đổi" và phần còn lại. Quan hệ đối xứng không tính đảo chủ/tân.
- **Phụ trợ**: CHAIR-vi, object P/R/F1, POPE/AMBER, CIDEr/BLEU, SPICE qua dịch; M4 văn hóa (phân tích, gold ~300 ảnh có/không + ảnh bẫy không có yếu tố văn hóa); tỷ lệ nội dung không kiểm được do người chấm.

**Meta-eval A (MVP)**: ~400 ảnh sạch + 100–150 ảnh XM3600; 4 ứng viên đóng băng 15/11 (Qwen2.5-VL-7B zero-shot, Vintern-3B, VSPS-SFT, tham chiếu giữ lại) — **không có ViHG-Cap** để tránh tự phục vụ; 2 người chấm mù hệ, 2 trục; τ_c chính, τ_b; cấp caption + hệ; bootstrap; báo lại sau khi bỏ VSPS.

## 4. Dữ liệu (sửa)

| Tập | Vai trò | Ghi chú |
|---|---|---|
| **ViSG-test ~400 ảnh** (dev 80 / test 320) = 157 KTVIC-sạch + ~243 OpenViIC-test sạch | gold SG + meta-eval | sau dedup all-vs-all; đếm lại giao với 300 ảnh object-gold |
| XM3600 tiếng Việt 100–150 ảnh (CC BY 4.0) | phần phát hành được của meta-eval | nối với nghiên cứu người VN duy nhất trước đó |
| Train KTVIC/OpenViIC **sạch** | silver G*, SFT | không dùng ảnh trùng test |
| Gán SG | máy gợi ý bằng **OWLv2/Florence-2 + họ mô hình khác Qwen**; 100 ảnh gán từ đầu (đo anchoring); gán đôi 25% | κ ≥ 0,7 object, F1 ≥ 0,6 triple; người gán không thấy verdict VSPS |
| Bản quyền | thư xin phép KTVIC + **chủ EVJVQA (UIT)** + OpenViIC; hết 30/11 chưa có → phát hành "chỉ ID + annotation" | Wikipedia text CC BY-SA: không đưa vào gói CC BY-NC-SA; Wikidata CC0 dùng được |

## 5. Cổng stop/go

| Cổng | Khi | Điều kiện | Nếu trượt |
|---|---|---|---|
| T0 | tuần 1, 0 GPU | precision object REJECTED trên mục audit ≥ 70% | bỏ loại sửa "thay node REJECTED" trong GEPA |
| T-dedup | tuần 1, <2 GPU-h | dedup xong; báo trùng train↔test KTVIC cho VSPS | sửa số liệu bài VSPS |
| **T0.5** | 11/2026 | logit khớp greedy `chat()` ≥ 98%; κ với K=5 ≥ 0,7; precision SUPPORTED ≥ 63,1% (đo trên split audit **dev**, không chỉnh trên test) | giữ K=5, thu hẹp phạm vi dựng đồ thị |
| T2 | 12/2026 | IAA đạt | gộp vị từ; **không mở rộng** trong 2026–27 |
| T3 | 01/2027 | parser hơn cả 2 baseline ≥ 3 F1 | phát hành như công cụ |
| **G-P2** | 31/01/2027 | E1 hơn SFT-không-kiểm-chứng trên M1-P (dev, CI 95%) **và** không thua viết-lại-CLC | P2 → IP&M/TOMM, không ACM MM |
| T4 | 02/2027 | τ_c của M1 không kém VLM-judge > 0,03 | định vị M1 là chẩn đoán |
| T-human | 03/2027 | người chấm: ViHG-Cap trung thực hơn zero-shot (VSPS hiện 3,91 < 4,17) | không claim "giảm ảo giác" trước người |

## 6. Phân đóng góp theo bài (chống salami)

| Đóng góp | P0 VSPS (TALLIP) | P1 tài nguyên (EMNLP ARR) | P2 phương pháp (IP&M SI / TOMM; ACM MM nếu qua G-P2) |
|---|---|---|---|
| Kiểm chứng 3 trạng thái, trung tính hóa giới tính, render truy vết | ✔ (đã có) | — | baseline |
| Sửa lỗi VSPS (cổng cấu trúc, dedup, CI văn hóa, CIDEr) | ✔ | — | — |
| Gold SG tiếng Việt, bộ chấm điểm người, parser, M1/H-R/M2 | — | ✔ | dùng để đánh giá |
| Lùi phân cấp KG cho thực thể + vị từ, GEPA, graph-then-caption | — | — | ✔ |

## 7. Việc ngay cho bài VSPS (P0)

1. Dedup all-vs-all, **đo trùng train↔test nội bộ KTVIC** (chưa từng đo) và trùng với UIT-OpenViIC; báo kết quả trên 157 ảnh sạch.
2. 45% mệnh đề quan hệ hỏng cấu trúc (regex, cần kiểm tay ~100); thêm cổng cấu trúc; audit lại ≥150 quan hệ (hiện chỉ 7 mục).
3. `geometric_check()` chưa từng chạy (0 box) → nêu trong bài hoặc thêm box.
4. Xóa từ văn hóa sau SFT (58,8% → 16,2–23,5%, gold 65 ảnh) → hạn chế, kèm bootstrap CI.
5. Đoạn giải thích CIDEr 17,3 vs GRIT 136.
6. Human faithfulness VSPS 3,91 < zero-shot 4,17 → viết thẳng, không giấu.

## 8. Giờ công và GPU (MVP)

Người gán ~200 h, NCS ~90 h (R2-06 §4.3, ước tính, dư ~30%). GPU nhánh KTVIC/OpenViIC sạch: ~515–760 GPU-h (R2-05); thời gian SFT 3,6 h/lượt **đo được trên chính RTX 3090 này** (v2raw: 1.800 bước, 3 h 35 m), nên nghiêng về cận dưới (~4 tuần máy).

## 9. Lộ trình

| Thời gian | Người gán | NCS / GPU | Cổng |
|---|---|---|---|
| 10/10–31/10/2026 | tuyển, xin phép | hoàn thiện P0 (mục 7); dedup; thư xin phép KTVIC/EVJVQA/OpenViIC; hướng dẫn v0.1 + IsA; caption 4 ứng viên | T0, T-dedup; đóng băng ứng viên 15/11 |
| 11/2026 | hiệu chuẩn, anchoring 100 ảnh, gán SG | verifier logit + cổng cấu trúc + box; gợi ý ViSG-test; silver G* trên train sạch | T0.5; giấy phép 30/11 |
| 12/2026 | xong SG, sửa parse + liên kết nút | IAA; parser bạc → ViT5; bắt đầu E1 | T2 |
| 01/2027 | meta-eval A (chậm, có thi) | E1 3 seed + xáo trộn + caption-only; baseline CLC/lùi-sau-sinh | T3; **G-P2 31/01** |
| 02/2027 (Tết 06/02) | nghỉ ~2 tuần, xong meta-eval A | GEPA 3 seed; backbone 3B; tính M1–M4 | T4 |
| 03/2027 | gold văn hóa, human eval P2 | viết P1 | T-human; ACM MM chỉ khi G-P2 đạt |
| 04/2027 | — | P1 lên arXiv; viết P2 | — |
| ~15/05/2027 | — | P1 nộp EMNLP ARR (kiểm lại hạn) | — |
| 06–08/2027 | — | P2 nộp IP&M SI (31/08) hoặc TOMM; bản mở rộng: E3, G1/G2, Qwen3-VL-8B | — |

## 10. Rủi ro còn lại

- Va chạm nhóm: UIT (Kiet/Ngan Nguyen — metric THR; ViG — quan hệ trên KTVIC), HCMUS (EVENTA). arXiv P1 sớm.
- Chưa xác minh: venue SceneAlign, CLC, Conformal Factuality, NES, M²CQA, KG-ViP; DOI VietSGG; nội dung ViG, HDUCap, bài FAIR 2025 về KG-captioning (paywall) → đọc trước khi nộp.
- Verifier 63,1% lan sang G*: không claim đảm bảo trung thực.
- Quyền riêng tư: vòng 1 có 8 agent gửi email người dùng trong mailto/User-Agent (OpenAlex/Crossref/Wikidata) trước khi có quy tắc; từ vòng 2 cấm rõ.

## 11. Vòng lặp

Vòng 2 → v2 (bản này). Vòng 3: kiểm lại v2 trên 3 trục bằng 3 critic mới (không đọc phản biện cũ trước khi tự đánh giá). Dừng nếu không còn BLOCKER.
