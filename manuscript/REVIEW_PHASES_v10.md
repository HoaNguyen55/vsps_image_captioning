# Review tính nhất quán: VSPS (bài báo) và FAIR_VSPS_v10_talk.pptx

Ngày: 2026-10-09 · Bài báo: `m48739-hoa final.pdf` (giống v9, chỉ khác email; không có file `a108-hoa final.pdf`) · Slide: `FAIR_VSPS_v10_talk.pptx` (17 slide)
5 agent review độc lập. Ba lỗi nghiêm trọng ở mục H đã được kiểm chứng lại trực tiếp trên dữ liệu. **Chưa sửa file nào.**

Nhãn: **[XN]** xác nhận từ nguồn · **[DG]** diễn giải hợp lý · **[KN]** khuyến nghị · **[KBC]** không báo cáo / không xác định được.

---

## A. Kết luận

**Tổ chức 2 pha là đúng kỹ thuật.** [XN] Ranh giới pha mà bài dùng là *offline, chạy một lần* và *mỗi ảnh lúc triển khai*. Tính chất cốt lõi "kiểm chứng không chạy lúc suy luận" được định nghĩa đúng tại ranh giới đó. Xây dữ liệu và SFT đều là chi phí offline, nên cùng nằm trong Pha 1. Fig. 1 ghi rõ "Supervision construction and training" và "Only the fine-tuned model is used at deployment" (§III-A, tr. 2). Hàm mất mát là SFT chuẩn; kiểm chứng chỉ tác động qua thành phần dữ liệu (§III-C, phương trình L; code `train_stage2.py` che nhãn prompt/ảnh bằng −100). Không chỗ nào trong bài gọi VSPS là kiến trúc mới, hàm mất mát mới, hay bộ kiểm chứng chạy lúc suy luận.

**Lỗi thật hay chỉ là chuyện rõ ràng?** Cấu trúc pha chỉ có vấn đề về độ rõ ràng: slide 6 ghi "Pha 1 · Huấn luyện"; §III-A viết "generation … never run at inference"; tên "Phase-1 records" trong §IV-B. Nhưng quá trình review phát hiện thêm **3 lỗi sự kiện**, không liên quan tới cấu trúc pha, phải sửa (mục H, nhóm "Bắt buộc"):
1. Bài ghi audit 244 mệnh đề lấy "from the training records" (§IV-E7). Thực tế **cả 83 ảnh được audit đều là ảnh test**, lấy từ lần chạy pipeline trên ảnh test (Untrained VSPS). Đã kiểm: 0/83 thuộc train.
2. Fig. 3(B) và slide 17 gọi verdict của ảnh #2921 là "Phase-1". Nhưng **#2921 là ảnh test**, mâu thuẫn với câu "no test image is processed in Phase 1" (§IV-A).
3. Bài ghi chi phí "about 30 GPU-hours on one RTX 4090 … 29 s per image … fifteen times more" (§IV-B, §IV-E7). Trường `seconds` trong 3.700 record cộng lại là **88,1 giờ** (trung vị 79,7 s/ảnh), còn thời gian thực từ timestamp là 24,2 giờ (chạy song song). Không số nào khớp "30 GPU-giờ trên một 4090". Ngoài ra, "29 s/ảnh" là thông lượng khi chạy song song, đem so với độ trễ batch-1 là so hai đại lượng khác nhau.

Ngoài ra có hai điểm **chưa công bố**, cần nói rõ trong bài:
- Untrained VSPS dùng biến thể A (hedge phần không chắc) với budget 5. Dữ liệu huấn luyện dùng biến thể B (loại phần không chắc) với budget 9 (`render_vsps_preds.py`, `build_dpo_data.py`). Vì vậy so sánh "1,51 so với 1,57" không cùng cấu hình.
- Lưới chọn B=9, số epoch và chính sách hedging (§IV-E4) nhiều khả năng được chấm trên 558 ảnh test. Mọi file kết quả trong repo đều là `test_data.json`. Bài không nói rõ split nào. [KBC trong bài; DG từ repo]

**Trước buổi trình bày FAIR cần sửa:**
- slide 6 (nhãn Pha 1, ô "Kiểm chứng", mũi tên Pha 1 → Pha 2, typo "SFT00");
- slide 7 (vai trò từng mô hình, ô đầu ra D_VSPS);
- slide 17 (bỏ chữ "Pha 1");
- slide 11 (COCO là ngoài miền SFT, không phải "chưa thấy"; số lượt suy luận);
- slide 12 (thêm F1 COCO 70,9 → 60,4);
- slide 13 (diễn đạt kết quả người chấm, nguồn audit);
- chuẩn bị sẵn câu trả lời mục G.

---

## B. Pipeline dựng lại từ bài

| # | Thao tác | Nhóm | Mô hình | Nguồn |
|---|---|---|---|---|
| 0 | 3.700 ảnh train KTVIC, không dùng caption gốc | Pha 1A · dữ liệu | — | §III-A, §IV-A |
| 1 | Sinh và chuẩn hóa mệnh đề P = G(I), khoảng 52 mệnh đề/ảnh | 1A | Qwen2.5-VL-7B gốc (vai trò: sinh) | §III-B1, §IV-B |
| 2 | Kiểm chứng 3 trạng thái: q⁺/q⁻, K = 5, Γ → Φ; luật trần chỉ được hạ mức | 1A | Vintern-1B (bộ kiểm chứng) | §III-B2 |
| 2b | Kiểm chéo màu: bất đồng → UNCERTAIN | 1A | Qwen2.5-VL-7B gốc (bộ sinh) | §III-B2 |
| 3 | Trung hòa N(p), điều kiện A(p), τ = 0,9; offline, không hỏi lại mô hình | 1A | luật | §III-B3 |
| 4 | Chọn S(P⁺, B_m) và kết xuất R (template; constrained-LM cho 650 mẫu); hậu kiểm | 1A | luật và Qwen2.5-VL-7B gốc (kết xuất) | §III-B4 |
| 5 | Kho D_VSPS: 7.177 mẫu / 3.617 ảnh | đầu ra 1A | — | §IV-B (khớp `sft.jsonl`) |
| 6 | QLoRA-SFT, hàm mất mát SFT chuẩn, một adapter cho hai chế độ | Pha 1B · tinh chỉnh | Qwen2.5-VL-7B 4-bit + LoRA | §III-C, §IV-B |
| 7 | Adapter cuối epoch 2 (không có bước chọn checkpoint) | đầu ra Pha 1 | — | [KBC trong bài] code: `trainer.save_model` |
| 8 | Ảnh mới → một lượt greedy → mô tả ngắn hoặc chi tiết | Pha 2 · suy luận | base + adapter | §III-C, §IV-E7 (0,81 / 1,88 s) |
| — | *Untrained VSPS*: các thao tác 1–4 chạy trên ảnh test, chỉ để chẩn đoán, không vào D_VSPS | đánh giá | G + V | §IV-D |

Các bước 2, 3, 4 không chạy lúc triển khai [XN]. Trong bài, generator, verifier và mô hình triển khai đều được tách vai trò, nhưng chỉ ở §IV-B. Bài cũng chưa nói rằng G và bộ kết xuất là checkpoint gốc, không gắn adapter.

---

## C. Audit bài báo

| Vị trí | Hiện tại | Phát hiện | Mức | Bằng chứng | Đề xuất |
|---|---|---|---|---|---|
| §IV-E7 | "re-labeled 244 machine-SUPPORTED propositions from the training records" | Sai nguồn: cả 83 ảnh đều thuộc test, lấy từ `stage1_test_union` | **Bắt buộc** | `tn.json` × `test_data.json`; `audit_round2_sample.json` | F-1 |
| Fig. 3(B) | "Phase-1 verdicts of the verifier and a human judge" | #2921 là ảnh test, nên không thể là Pha 1 | **Bắt buộc** | `test_data.json` | F-2 |
| §IV-A | "no test image is processed in Phase 1" | Đúng với D_VSPS, nhưng mâu thuẫn bề ngoài với Untrained VSPS, Fig. 3B và audit | Nên sửa | §IV-D | F-3 |
| §IV-B, §IV-E7 | "about 30 GPU-hours on one RTX 4090"; "about 29 s per image … fifteen times more" | Không khớp record (88,1 h tổng `seconds`, 24,2 h thời gian thực). Đang so thông lượng song song với độ trễ batch-1 | **Bắt buộc** | trường `stats` trong record Stage-1 | F-4 |
| §III-B4, §IV-E4 | "chosen on a grid over the same verdicts"; quét epoch và hedging | Không nói split nào. Repo chỉ có kết quả trên test. B_short trong code là `[:2]` của lựa chọn detailed, không phải S(P⁺, B_short) độc lập | Nên sửa (thành Bắt buộc nếu là test) | `build_dpo_data.py` | F-5 |
| §IV-D, §IV-E7 | "Untrained VSPS runs the full construction pipeline"; "reaches similar factuality (1.51 vs 1.57)" | Cấu hình khác: biến thể A, budget 5. Tên "Untrained" dễ hiểu nhầm là "mô hình VSPS trước SFT" | Nên sửa | `render_vsps_preds.py` | F-6 |
| §III-A | "generation, verification, selection, and rendering never run at inference" | "generation" dễ hiểu là sinh caption; thiếu "neutralization" | Nên sửa | §III-C | F-7 |
| §III-A / §IV-B | vai trò các mô hình chỉ nêu ở §IV-B | Thiếu: G và bộ kết xuất là checkpoint gốc không adapter; Qwen còn kiểm chéo màu | Nên sửa | §III-B2 | F-8 |
| §IV-B | "Building the Phase-1 records" | "Phase 1" ở đây chỉ phần xây dữ liệu; thời gian SFT không báo cáo | Nên sửa | §III-A | F-4 |
| §IV-A | "69 for screening the construction pipeline" | Không định nghĩa "screening". Repo: 69 ảnh train ngoài Stage-1, dùng xếp hạng thô các biến thể pipeline; **không phải tập validation SFT** | Nên sửa | `data/screening/val_manifest.json` | F-3 |
| (không có) | validation / chọn checkpoint | Không báo cáo. Code: không có `eval_dataset`, không early stopping, dùng adapter cuối | Nên sửa (thêm 1 câu) | `train_stage2.py` | F-9 |
| §IV-B | cấu hình QLoRA | Khớp code. Thiếu: LoRA dropout 0,05; LoRA chỉ trên LM (vision tower giữ nguyên); phiên bản trl; scheduler | Tùy chọn | `train_stage2.py` | F-9 |
| §III-C, §IV-E7 | "data-level distillation"; "behaviour is distilled" | Dễ hiểu là KD dùng logit. §III-C đã phủ định, §IV-E7 chưa | Tùy chọn | — | F-10 |
| §III-C heading | "Model fine-tuning and inference" | Tiêu đề cắt ngang ranh giới hai pha | Tùy chọn | Fig. 1 | F-11 |
| Fig. 2 | "Three-way", "P^B = S(P⁺, B)", "phrase ← proposition ← verdict" | Lệch chữ với văn bản; thiếu tên mô hình và bước kiểm chéo màu | Tùy chọn | §III-B | F-12 |
| §III-B2 | "27.4% … are split" | Không tái lập được (agent đo được 25,5% hoặc 35,4% tùy định nghĩa) | Tùy chọn (định nghĩa rõ) | record | — |
| Tóm tắt, Bảng IV | P/R/F1 là trung bình 3 seed, các số khác là seed 42 | Trộn hai loại số mà không nói | Tùy chọn | README: seed 42 là 41,5 / 36,7 / 39,0 | ghi chú bảng |
| H2 | "share the Qwen language-model family" | Chưa nêu bộ sinh tự kiểm chéo màu của chính nó | Tùy chọn | §III-B2 | F-13 |

---

## D. Audit slide

| Slide | Chỗ dễ hiểu nhầm | Rủi ro | Câu thay thế (tiếng Việt) | Lời nói |
|---|---|---|---|---|
| 1 (ghi chú) | "chưng cất kết quả kiểm chứng vào mô hình thông qua SFT" | Hiểu là KD dùng logit hoặc KL | "…đưa kết quả kiểm chứng vào mô hình **gián tiếp qua dữ liệu SFT**: chưng cất ở mức dữ liệu, không dùng logit mô hình thầy, không thêm hàm mất mát." | "Bộ kiểm chứng không tham gia hàm mất mát." |
| 2 | "cô", "túi" tô màu là ảo giác, trong khi slide 16 thừa nhận túi có trong ảnh | Tự mâu thuẫn | Dưới trích dẫn: "*Tô màu: CHAIR tính là ngoài tham chiếu, không nhất thiết sai*" | "Vì thế CHAIR trên KTVIC là cận trên." |
| 3–4 | "4.26", "46.9%" lẫn với "55,4%"; "23/49 ảnh có dấu hiệu giới tính" | Không thống nhất dấu thập phân; mẫu số dễ hiểu sai | "4,26"; "46,9% (23/49 ảnh có dấu hiệu giới tính, tập thử thách 50 ảnh)" | — |
| 5 | Hàng "Hạn chế" bị ô câu hỏi che | Khán giả không thấy động cơ của VSPS | (dời ô câu hỏi xuống) | "VSPS thuộc nhóm dữ liệu: không đổi kiến trúc, không thêm loss, không thêm bước nào lúc suy luận." |
| **6** | "Pha 1 · Huấn luyện" | Khán giả tưởng bước kiểm chứng là huấn luyện | "**Pha 1 · Xây dựng dữ liệu + tinh chỉnh** (một lần, offline)" | "Pha 1 gồm hai việc nối tiếp: dựng dữ liệu xong rồi mới tinh chỉnh." |
| **6** | Ô "Kiểm chứng mệnh đề" (Fig. 1 ghi "Create VSPS supervision data") | Không thấy đầu ra là một kho dữ liệu | "**1A · Dựng dữ liệu VSPS** (4 bước, có kiểm chứng)" và "**1B · Tinh chỉnh QLoRA-SFT** · Qwen2.5-VL-7B · loss SFT chuẩn" | "Bốn bước tạo kho 7.177 mẫu; QLoRA-SFT chỉ đọc kho này." |
| **6** | Không có mũi tên Pha 1 → Pha 2 | Hai cột trông như hai hệ thống rời nhau | Mũi tên: "**chỉ mô hình này được triển khai**" | "Đầu ra Pha 1 là adapter LoRA trên Qwen2.5-VL-7B." |
| **6** | "không kiểm chứng / không hậu xử lý" | Thiếu "truy hồi"; không nói rõ không gọi Vintern | "một lượt greedy · không kiểm chứng · không truy hồi · không hậu xử lý" | "Lúc triển khai không gọi Vintern-1B, không sinh hay chọn mệnh đề." |
| **6** | "không SFT00"; "Không dùng: ảnh kiểm tra, tham chiếu"; "69 ảnh rà soát" | Typo; chữ "rà soát" trùng với audit ở slide 13 | "COCO-2014: 5.000 ảnh, không dùng để SFT" · "Không dùng: ảnh test, câu tham chiếu gốc" · "**69 ảnh thử pipeline** (không SFT, không đánh giá)" | — |
| **6** | "Mệnh đề đã kiểm chứng → SFT" | Tưởng SFT học thẳng trên mệnh đề | "…→ Mệnh đề đã kiểm chứng → **Mô tả giám sát** → SFT → Mô tả một lượt" | — |
| **7** | "Qwen2.5-VL", "Vintern-1B" không ghi vai trò; không có ô đầu ra | Nhầm bộ sinh với mô hình được tinh chỉnh; không thấy rằng 4 bước diễn ra trước SFT | "Qwen2.5-VL-7B (**bộ sinh**)" · "Vintern-1B (**bộ kiểm chứng**, chỉ ở Pha 1)" · "tối đa 2 (ngắn) / 9 (chi tiết)" · chân slide: "→ **Kho 7.177 mẫu / 3.617 ảnh** · chạy một lần, offline → **sau đó** mới QLoRA-SFT" | "Cùng backbone với mô hình sẽ được tinh chỉnh, nhưng ở đây chỉ chạy suy luận để sinh dữ liệu." |
| 8 | "Gộp 10 câu trả lời → 3 trạng thái"; tiêu đề trùng slide 7 | Sai cơ chế: hai nhánh được tổng hợp riêng rồi mới kết hợp | Tiêu đề "… · Bước 2"; "Tổng hợp từng nhánh (5 + 5) → 3 trạng thái · luật trần chỉ hạ mức" · "Mệnh đề màu: hỏi thêm **bộ sinh** Qwen2.5-VL-7B" | "Chỉ một câu trả lời lệch ở nhánh khẳng định là đã thành KHÔNG CHẮC CHẮN." |
| 9 | "461 → 83 · Không tạo được dữ liệu giám sát"; ghi chú đọc các số 32.967… không có trong bài | 461 là số ảnh không có mệnh đề SUPPORTED, không phải không có dữ liệu | "ảnh huấn luyện không còn mệnh đề dùng được (trước → sau trung hòa)" · "trung hòa offline, dùng lại câu trả lời đã lưu" | "Các số chi tiết lấy từ record Pha 1 công bố trong repo." |
| 10 | Hàng giới tính 46,9 / 10,2 / 4,1 nằm cạnh các chỉ số tính trên 558 ảnh; P2 không định nghĩa; ghi chú "không đơn thuần do nói ít hơn" | Lẫn mẫu số; lập luận bị đảo | "…(tập thử thách 50 ảnh) 46,9% (23/49) · 10,2% · 4,1% (2/49)" · chú thích "P2: cùng Qwen2.5-VL-7B + QLoRA-SFT, dữ liệu chưa kiểm chứng" | "Một phần mức giảm là do nói ít hơn (6,54 → 3,13 đối tượng), nhưng CHAIRi theo lần nhắc vẫn giảm 65,1 → 50,1, và ở độ phủ gần như P2 (3,80 so với 3,13), VSPS vẫn ít ảo giác hơn (2,05 so với 1,57)." |
| **11** | VCD và Tự sửa lỗi đặt ngang hàng; không có chi phí; COCO không kèm cảnh báo; hai ô −7% và −63,1% đè lên nhau | Bỏ sót số lượt suy luận; COCO bị hiểu là "chưa từng thấy" | "VCD (lúc suy luận, 2 lượt/ảnh)" · "Tự sửa lỗi (2 lượt/ảnh)" · "VSPS (1 lượt/ảnh)" · chân slide: "COCO: ngoài miền SFT, có thể nằm trong dữ liệu tiền huấn luyện; không chứng minh khái quát đa ngôn ngữ" | "Chúng tôi không so độ trễ trực tiếp vì chưa đo cùng giao thức; số lượt là theo thiết kế." |
| **12** | Ghi chú "F1 thay đổi không nhiều" (bỏ COCO); "chỉ đưa ra thông tin đã đủ bằng chứng" | Bỏ sót F1 COCO giảm hơn 10 điểm; ngụ ý mô hình tự kiểm chứng lúc suy luận | Thêm "COCO: P 80,5 → 88,2 · R 63,3 → 45,9 · **F1 70,9 → 60,4**" · "VSPS: trung bình 3 seed" | "Mô hình học được phong cách thận trọng từ dữ liệu; lúc triển khai không có gì kiểm chứng lại." |
| **13** | "chênh lệch không có ý nghĩa thống kê"; "một người rà soát … 244 mệnh đề" | Nghe như "trung thực ngang zero-shot"; nguồn audit sai | "So với zero-shot: VSPS **không** được chấm trung thực hơn (3,91 so với 4,17; p = 0,12; tốt hơn ở 16 ảnh, kém ở 24)" · "Người gán nhãn độc lập xem lại 244 mệnh đề mà bộ kiểm chứng gán ĐƯỢC HỖ TRỢ (**khi chạy pipeline trên ảnh test**)" | "CHAIR KTVIC phạt cả vật có thật mà tham chiếu không nhắc, người chấm thì không; câu ghép theo khuôn mẫu làm giảm độ trôi chảy." |
| 14 | "bốn hạn chế"; "dùng LM viết câu tự nhiên hơn"; câu tóm tắt cuối | Bài báo có 6 hạn chế; constrained-LM đã được dùng cho 650 mẫu; tóm tắt bỏ sót kết quả người chấm | "Bài báo nêu sáu hạn chế (H1–H6), gộp thành bốn nhóm" · "Mở rộng LM có ràng buộc (hiện 650/3.560)" · "…người chấm xác nhận lợi ích so với SFT chưa kiểm chứng, nhưng chưa thấy VSPS trung thực hơn zero-shot" | — |
| 15 | email hoanguyen@bos-semi.com, bài báo final dùng nguyenleh760@gmail.com | Không thống nhất | thống nhất một email | — |
| 16 | "CHAIR tính nhầm 'cửa' trong 'cửa hàng'" | Bài báo không nói vậy (văn bản đã tách từ) | "Ngoài tham chiếu theo CHAIR: 'cửa', 'túi' (túi có trong ảnh)" · "Đầu ra Pha 2, nguyên văn" | "Chỉ số giới tính không đo độ đúng giới tính thực." |
| **17** | "Bước kiểm chứng: máy cho là…", Fig. 3B gọi là "Pha 1" | #2921 là ảnh test | Tiêu đề: "Ví dụ B: một lỗi của bộ kiểm chứng (pipeline chạy trên ảnh test, không phải đầu ra triển khai)" | "Lỗi kiểu này cũng có trong dữ liệu giám sát; lúc triển khai không có bộ kiểm chứng nào chạy." |

Thuật ngữ trên toàn deck:
- Không dùng "huấn luyện" làm tên Pha 1.
- "rà soát" chỉ dùng cho audit con người; với 69 ảnh dùng "thử pipeline".
- "xác nhận": máy thì nói "gán ĐƯỢC HỖ TRỢ", người thì nói "xác nhận".
- Không dùng "validation / kiểm định".
- Gắn nhãn pha cho các slide 7–9, 13, 16, 17.

---

## E. Sơ đồ đề xuất (giữ định nghĩa 2 pha)

1A/1B là **bước con trong Pha 1**, không phải định nghĩa lại pha. Lý do:
- Điểm cắt nằm đúng tại một artefact thật, D_VSPS. Không có gì đi ngược từ 1B về 1A.
- 1A là đóng góp của bài; 1B là công thức chuẩn, P1, P2 và VSPS cùng dùng.

**Không nên đổi thành 3 pha**:
- Mâu thuẫn với §III-A, Fig. 1, tóm tắt và kết luận.
- Gây cảm giác huấn luyện là một đóng góp riêng.
- "Dữ liệu → huấn luyện → suy luận" đúng với mọi bài SFT, nên làm mờ cái mới của VSPS.

```
╔══ PHA 1 · XÂY DỰNG GIÁM SÁT VÀ TINH CHỈNH (offline · chạy một lần) ══════════════╗
║ ┌ 1A · Xây dựng dữ liệu giám sát ───────────────────────────────────────────┐ ║
║ │ 3.700 ảnh train (không dùng câu tham chiếu)                               │ ║
║ │ ① Sinh mệnh đề ⟨Qwen2.5-VL-7B · bộ sinh⟩ → ② Kiểm chứng 3 trạng thái       │ ║
║ │ ⟨Vintern-1B · bộ kiểm chứng⟩ → ③ Trung hòa (offline) → ④ Chọn + kết xuất   │ ║
║ │ ⟨Qwen2.5-VL-7B · kết xuất⟩ ──▶ [D_VSPS · 7.177 mẫu / 3.617 ảnh]            │ ║
║ └──────────────────────────────────────────────────────────────┬───────────┘ ║
║ ┌ 1B · Tinh chỉnh QLoRA-SFT ──────────────────────────────────▼───────────┐ ║
║ │ Qwen2.5-VL-7B 4-bit (đóng băng) + LoRA r=16 (được học) · loss SFT chuẩn  │ ║
║ │ ──▶ [Adapter LoRA · một adapter cho cả hai chế độ]                       │ ║
║ └──────────────────────────────────────────────────────────────┬───────────┘ ║
╚════════════ chỉ adapter LoRA đi qua ranh giới ═══════════════════╪═════════════╝
╔══ PHA 2 · TRIỂN KHAI (mỗi ảnh · một lượt) ═══════════════════════▼═════════════╗
║ Ảnh mới → Qwen2.5-VL-7B + adapter → giải mã greedy → mô tả ngắn | chi tiết   ║
║ không sinh mệnh đề · không kiểm chứng · không chọn/kết xuất · không hậu xử lý ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

Hiển thị cùng một backbone ở nhiều vai trò:
- Qwen dùng một chip duy nhất, luôn kèm nhãn vai trò.
- Ở 1A chip màu xám, ghi "chỉ suy luận".
- Màu cam chỉ dành cho LoRA.
- Chú thích: "Cùng trọng số gốc Qwen2.5-VL-7B-Instruct; chỉ adapter LoRA (cam) được học. Bộ kiểm chứng là mô hình khác (Vintern-1B)."

---

## F. Câu sửa cụ thể cho bài báo

- **F-1 (§IV-E7).** "…re-labeled 244 machine-SUPPORTED propositions ~~from the training records~~ **from pipeline records of test images (the Untrained VSPS run; these records never enter D_VSPS)** (at most three per image)…". *Hoặc*: lấy mẫu lại 244 mệnh đề từ record train rồi audit lại. Cách này tốn công hơn, nhưng mới đúng với tuyên bố "bounds the precision of the supervision".
- **F-2 (Fig. 3 caption).** "(B) ~~Phase-1 verdicts~~ **verdicts of the construction pipeline run on a test image (Untrained VSPS)** of the verifier and a human judge."
- **F-3 (§IV-A).** "…69 **held-out training images used only to compare construction-pipeline variants (not used for SFT, checkpoint selection, or any reported metric)**, … and no test image **contributes to the supervision data or to fine-tuning; the diagnostic Untrained VSPS baseline (Section IV-D) applies the construction operators to test images at evaluation time only.**" *(Cần tác giả xác nhận rằng 69 ảnh không được dùng cho số liệu nào trong bài.)*
- **F-4 (§IV-B, §IV-E7).** Thay bằng số đo thật, ví dụ: "Building the supervision-construction records (Phase 1a) for 3,700 images took [X] GPU-hours ([N] concurrent workers, 24 h wall-clock); a single-pass caption takes 1.88 s." *Tác giả cần xác định nguồn của con số "30 GPU-hours"*. Nếu chỉ còn record làm căn cứ: tổng `seconds` là 88,1 h, tức khoảng 86 s/ảnh, gấp khoảng 45 lần 1,88 s. Như vậy kết luận "đắt hơn nhiều lần" còn mạnh hơn bản hiện tại.
- **F-5 (§III-B4, §IV-E4).** "…chosen on a grid over the same verdicts **and scored on [split]**…". Nếu là test: "**These settings were compared on the test split; we report them as sensitivity analyses.**" Mô tả B_short đúng như code: "the short target takes the first two SUPPORTED propositions of the detailed selection."
- **F-6 (§IV-D, §IV-E7).** "**Pipeline-only VSPS** (no SFT) runs the construction pipeline, verifier included, on each test image at evaluation time and outputs its template rendering **(uncertain content hedged, budget 5)**". §IV-E7: "…reaches similar factuality (1.51 vs. 1.57) **under its own rendering settings** only by running the verifier on every input."
- **F-7 (§III-A).** "Phase 1 runs offline on the training images: it first builds the supervision store D_VSPS from verified propositions, without using their gold captions (Section III-B, Fig. 2), and then fine-tunes Qwen2.5-VL-7B on it with QLoRA (Section III-C). Phase 2 deploys only the fine-tuned model, so **proposition** generation, verification, **neutralization,** selection, and rendering never run at inference."
- **F-8 (§III-A, câu thêm).** "In Phase 1, the frozen base Qwen2.5-VL-7B acts as proposition generator G, colour cross-checker, and constrained-LM renderer, and Vintern-1B [8] acts as verifier V; the deployed model is the same Qwen2.5-VL-7B with the trained LoRA adapter."
- **F-9 (§IV-B, câu thêm).** "No validation split or early stopping is used; the adapter after the second epoch is evaluated. LoRA (dropout 0.05) is applied to the language-model projections only; the vision encoder is frozen."
- **F-10 (§IV-E7).** "which is why its behaviour is distilled into a single-pass model" → "which is why its outputs are used, offline, as training targets for a single-pass model".
- **F-11 (§III-C).** Tiêu đề: "C. Fine-tuning (Phase 1) and single-pass inference (Phase 2)". Câu mở: "D_VSPS is used to fine-tune the base Qwen2.5-VL-7B with QLoRA [19] and LoRA [20]; only the LoRA parameters θ are trained…"
- **F-12 (Fig. 1/2).**
  - Fig. 1, nhãn Pha 1: "Phase 1 (offline): supervision construction (1a) and QLoRA-SFT (1b)".
  - Fig. 1, nhãn khác: "Fine-tuned model (base + LoRA adapter)".
  - Fig. 2: đổi "Three-way" thành "Three-state"; viết "P^B_m = S(P⁺, B_m)"; viết "span ← proposition ← verdict". Caption Fig. 2 thêm "(Phase 1a; training images only, not run at inference)".
- **F-13 (H2).** Thêm: ", and colour propositions are additionally cross-checked by the generator itself."
- **F-14 (Tóm tắt, tùy chọn).** "…so ~~inference is a single pass~~ **the deployed model captions in a single pass**."

---

## G. Câu hỏi phản biện có thể gặp (trả lời ngắn; bản đầy đủ có trong báo cáo của agent 5)

1. **VSPS là phương pháp huấn luyện hay xây dữ liệu?** Là phương pháp xây dữ liệu. Phần huấn luyện là QLoRA-SFT chuẩn, không có logit mô hình thầy, không thêm loss (§III-C). P2 và VSPS dùng cùng backbone và cùng công thức, chỉ khác dữ liệu: ảo giác 2,05 → 1,57, CHAIR_s 88,2 → 79,2 (Bảng II).
2. **Mô hình có học trong bước kiểm chứng không?** Không. Bước kiểm chứng chỉ chạy suy luận Vintern-1B và ghi lại bằng chứng; trung hòa chạy offline. SFT chỉ bắt đầu khi kho `sft.jsonl` đã cố định.
3. **Đầu ra Pha 1 là gì?** Kho D_VSPS (7.177 mẫu / 3.617 ảnh, đã công bố) và một adapter LoRA (r = 16) dùng chung cho hai chế độ. Chỉ adapter đi sang Pha 2.
4. **Bộ kiểm chứng có chạy lúc suy luận không?** Không. Mỗi ảnh chỉ một lượt greedy: 0,81 s (ngắn), 1,88 s (chi tiết). Chỉ baseline chẩn đoán Untrained VSPS chạy bộ kiểm chứng trên ảnh test.
5. **VSPS khác QLoRA-SFT thế nào?** QLoRA-SFT là cách tối ưu; VSPS quyết định mô hình học cái gì. P1, P2 và VSPS cùng công thức SFT, nên khác biệt giữa chúng là do dữ liệu.
6. **Sao không chia 3 pha?** Ranh giới pha trong bài là offline/một lần với mỗi ảnh/triển khai, và tính chất "không kiểm chứng lúc suy luận" được định nghĩa tại ranh giới đó. 1A/1B là bước con trong Pha 1. Chia 3 pha sẽ khiến người nghe tưởng huấn luyện là đóng góp.
7. **Tập validation và chọn checkpoint?** Bài không báo cáo. Code không có tập validation, không early stopping, dùng adapter cuối epoch 2; cấu hình cố định trước. Lý do (ghi trong code): chỉ số tính từ bộ kiểm chứng sẽ tối ưu độ đồng thuận với Vintern, không phải với ảnh. Độ ổn định thể hiện qua 3 seed (1,55 ± 0,04). Thừa nhận đây là một hạn chế.
8. **69 ảnh có phải validation không?** Không. Đó là 69 ảnh train ngoài Stage-1, dùng xếp hạng thô các biến thể pipeline; không dùng cho SFT, không có số nào vào bài.
9. **Untrained VSPS xử lý ảnh test, có trái với "no test image in Phase 1" không?** Không ảnh test nào vào D_VSPS (đã kiểm: 0/3.700 record là ảnh test). Untrained VSPS là baseline chẩn đoán chạy riêng. Nói trung thực: baseline này dùng hedge với budget 5, khác cấu hình dữ liệu huấn luyện.
10. **Qwen vừa sinh dữ liệu vừa học, có phải vòng tròn không?** Thứ được chưng cất là cả pipeline sinh, kiểm chứng và chọn lọc. P2 chính là đối chứng "tự học trên đầu ra chưa kiểm chứng của mình": VSPS tốt hơn P2 về ảo giác (2,05 → 1,57) và độ trung thực do người chấm (2,60 → 3,91). Bộ kiểm chứng là mô hình khác; đánh giá dùng nguồn độc lập với bộ kiểm chứng. Thừa nhận H2 (cùng họ Qwen) và việc mô hình không thể học nội dung mà bộ sinh chưa từng đề xuất, đó là một lý do recall giảm.
11. **B = 2/9 chọn trên dữ liệu nào?** Bài không nói. *Người trình bày cần xác nhận trước buổi nói.* Nếu là tập test, nói rõ đây là phân tích độ nhạy. B_short trong code là hai mệnh đề SUPPORTED đầu tiên của lựa chọn detailed.
12. **Huấn luyện ở 4-bit, triển khai ở bf16 có lệch không?** Mã đánh giá mặc định tải bf16, còn bảng phần cứng trong README ghi 4-bit. Chưa đo so sánh; nói thẳng là chưa đo.
13. **LoRA chỉ trên LM thì có học bám ảnh không?** Bộ mã hóa ảnh được giữ nguyên; mô hình học *chọn điều nên nói*. Bằng chứng không chỉ là hiệu ứng độ dài: CHAIR_i theo lần nhắc giảm 65,1 → 50,1; chỉ đưa ràng buộc vào prompt thì giảm 7%.
14. **Audit 244 mệnh đề đo chất lượng dữ liệu huấn luyện?** Trả lời trung thực: audit lấy từ record pipeline trên ảnh test, cùng bộ kiểm chứng và cùng quy trình, nên là ước lượng *gián tiếp* cho độ chính xác của dữ liệu giám sát (sửa câu chữ trong bài theo F-1).

---

## H. Danh sách hành động theo ưu tiên

**Bắt buộc (sai sự kiện hoặc phương pháp)**
1. Nguồn audit 244 mệnh đề, §IV-E7 (F-1) và slide 13.
2. "Phase-1 verdicts" của ảnh #2921: Fig. 3B (F-2) và slide 17.
3. Chi phí 30 GPU-giờ / 29 s / 15× (F-4): xác định nguồn số liệu hoặc thay bằng số đo được.
4. Nói rõ split dùng cho lưới budget, epoch và hedging (F-5). Nếu là test thì ghi rõ, hoặc chạy lại trên 69 ảnh.
5. Typo "SFT00" ở slide 6.

**Nên sửa (dễ gây hiểu nhầm)**
6. Slide 6: nhãn Pha 1, ô 1A/1B, mũi tên "chỉ mô hình này được triển khai", "69 ảnh thử pipeline".
7. Slide 7: vai trò từng mô hình, ô đầu ra "Kho 7.177 mẫu → sau đó QLoRA-SFT".
8. Slide 11: COCO là ngoài miền SFT; 2 lượt so với 1 lượt; tách hai ô −7% và −63%.
9. Slide 12: thêm F1 COCO 70,9 → 60,4. Slide 13: viết lại câu so sánh với zero-shot và giải thích vì sao CHAIR khác người chấm.
10. Bài báo: F-3, F-6, F-7, F-8, F-9.
11. Slide 8: mô tả lại cơ chế "5 + 5". Slide 10: ghi rõ tập thử thách 50 ảnh, định nghĩa P2, sửa lập luận trong ghi chú.

**Tùy chọn (văn phong)**
12. F-10 đến F-14; dấu thập phân "4,26"; thống nhất email; slide 2 thêm chú thích về tô màu; slide 14 ghi "6 hạn chế"; slide 16 bỏ câu về "cửa hàng".
13. Code: đổi mặc định `--epochs` thành 2; README sửa "Phase 2 = 4-bit"; định nghĩa lại 27,4%.
