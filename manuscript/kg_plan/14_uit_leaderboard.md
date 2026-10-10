# 14. Bảng xếp hạng captioning tiếng Việt 2021-2026 và bản đồ nhóm UIT

Ngày quét: 2026-10-10. Nguồn đã mở trong phiên: arXiv API và PDF arXiv, Semantic Scholar Graph API (tra theo DOI, danh sách trích dẫn của UIT-ViIC, KTVIC, UIT-OpenViIC, VieCap4H, ViTextCaps), Crossref API, ACL Anthology, PDF của các tạp chí trong nước (VNU JCSCE, JCC, HaUI, Hồng Đức, HUFLIT). OpenAlex hết quota trong phiên này, còn DBLP chặn bot. Mọi số liệu dưới đây được chép từ bảng trong PDF đã mở, trừ các mục ghi "Chưa xác minh".

**Tóm tắt ngắn**
1. Không có bảng xếp hạng chung. Mỗi bài dùng tokenizer khác nhau (PyVI, âm tiết, word-segment) và thang khác nhau (CIDEr dạng 1.488 hay 148.8). Số giữa các bài **không so trực tiếp được**.
2. SOTA đã xác minh: **UIT-ViIC** là ObjectAoA, CIDEr 1.488 (2023). **KTVIC** là GRIT, CIDEr 136.0 (2024). **UIT-OpenViIC** là MDSANet+CAMO, CIDEr 76.48 (bản arXiv). **VieCap4H** có avg-BLEU tốt nhất 0.306 (public) và 0.329 (private). **ViTextCaps** là PhonoSTFG, CIDEr 0.646. ViG (MAPR 2026) tuyên bố vượt GRIT trên cả KTVIC lẫn UIT-ViIC, nhưng chưa xem được số.
3. **Chưa có bài nào chấm LVLM (Qwen2.5-VL, Vintern, InternVL) bằng fine-tune hay zero-shot trên KTVIC hoặc UIT-OpenViIC với các metric chuẩn.** Ngoại lệ duy nhất là GPT-4o zero-shot trên ViTextCaps.
4. **Không có dataset UIT nào có nhãn scene graph hay quan hệ.** Bài UIT-OpenViIC ghi rõ là không dùng SPICE vì "the Vietnamese language scene graph is unavailable now". Tài nguyên đồ thị tiếng Việt gần nhất là **VLSP 2025 viSemParse (AMR, 2.500 câu, HUS)**, và đây là dữ liệu chỉ có văn bản.
5. **Rủi ro va chạm lớn nhất: ViG (UIT, MAPR 2026).** Bài này gắn "Residual Relation Memory" (quan hệ cặp vùng) và "Local-Cultural Query Memory" lên GRIT đóng băng, rồi chạy trên KTVIC và UIT-ViIC. Đây đúng là ngách "relation-aware captioning tiếng Việt".
6. **Cảnh báo dữ liệu:** ViCLIP-OT (arXiv 2602.22678) phát hiện **401/558 ảnh test KTVIC trùng gần (near-duplicate) với ảnh train của UIT-OpenViIC**. Sau khi lọc trùng, tập test KTVIC chỉ còn 157 ảnh. Cảnh báo này áp dụng cho cả VSPS và hướng KG nếu có dùng mô hình đã thấy OpenViIC.

---

## 1. Bảng kết quả theo dataset

### 1.1 UIT-ViIC
Lam et al., ICCCI 2020 (arXiv 2002.00175). 3.850 ảnh COCO thể thao có bóng, 19.250 caption. Split 2.695/924/231 ảnh.

| Năm | Bài (venue) | Mô hình | B-1 | B-4 | METEOR | ROUGE-L | CIDEr | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| 2020 | UIT-ViIC (ICCCI, arXiv 2002.00175) | pytorch-tutorial CNN-LSTM | 0.710 | 0.394 | – | 0.626 | 1.005 (CIDEr-D) | PyVI |
| 2020 | như trên | NIC | 0.682 | 0.327 | – | 0.599 | 0.818 | PyVI |
| 2022 | K. Nguyen, JCC 38(4) 327-346, DOI 10.15625/1813-9663/38/4/17548 (UIT) | Transformer + VinVL ResNeXt-152 (grid) | – | 47.30 | 37.07 | 64.84 | 137.12 | test; tốt nhất trong bài |
| 2023 | ObjectAoA, VNU JCSCE 38(1) 11-19, arXiv 2211.05405 (UIT) | ORT | 0.744 | 0.47 | 0.364 | 0.638 | 1.362 | |
| 2023 | như trên | **ObjectAoA** | 0.769 | 0.497 | 0.373 | 0.648 | **1.488** | **SOTA đã xác minh** |
| 2025 | Hoang V.D. et al., J. Sci. Tech. HaUI, DOI 10.57001/huih5804.2025.414 (HCMUTE) | PVG (ViT + BARTpho + GPT-2) | 42.3 | 16.5 | – | 47.5 | 96.5 | |
| 2026 | Hoàng A.C. et al., TC Khoa học ĐH Hồng Đức 84(2), DOI 10.70117/hdujs.84.2.2026.1139 | Attention Fusion (CLIP text emb.) | 0.679 | 0.278 | 0.236 | – | 0.874 | baseline 0.782 |
| 2026 | **ViG**, MAPR 2026, DOI 10.1109/MAPR72750.2026.11685699 (UIT) | GRIT + Relation Memory + Cultural Query | ? | ? | ? | ? | ? | abstract: "improves over GRIT on every metric" (Chưa xác minh số) |

### 1.2 KTVIC
Pham, Nguyen, Vuong, Ha (VNU-UET, RIKEN), arXiv 2401.08100, 2024. 4.327 ảnh (ảnh lấy từ UIT-EVJVQA), 21.635 caption. Train 3.769 ảnh, test 558 ảnh.

| Năm | Bài | Mô hình | B-1 | B-4 | METEOR | ROUGE | CIDEr |
|---|---|---|---|---|---|---|---|
| 2024 | KTVIC (arXiv 2401.08100) | ResNet101-LSTM | 53.0 | 15.5 | 27.5 | 42.3 | 21.8 |
| 2024 | như trên | ViT-Transformer | 56.1 | 19.3 | 30.1 | 44.7 | 36.8 |
| 2024 | như trên | **GRIT** | 74.7 | 40.6 | 36.6 | 59.7 | **136.0** (SOTA đã xác minh) |
| 2025 | HaUI (như trên) | PVG | 36.9 | 12.7 | – | 41.9 | 98.4 |
| 2025 | Nguyễn T. Khiêm et al., HUFLIT J. Sci. 9(3), DOI 10.71091/2354-113X/269 (ĐHSP TP.HCM) | Swin + Transformer dec. | 65.2 | 21.5 | 26.9 | – | 58.5 |
| 2026 | Hồng Đức (như trên) | Attention Fusion | 0.667 | 0.266 | 0.229 | – | 0.841 |
| 2026 | ViG (MAPR 2026, UIT) | như trên | ? | ? | ? | ? | ? (Chưa xác minh, tuyên bố vượt GRIT) |

Lưu ý:
- Bảng 5 của bài HaUI gán nhãn sai: dòng KTVIC 74.7/40.6/59.7/136.0 được ghi là "ViT-Transformer [13]", trong khi đó là số của GRIT.
- ViCLIP-OT (Tran, Nguyen, Pham, Đại học Cần Thơ, arXiv 2602.22678) chỉ làm truy hồi (retrieval) trên KTVIC đã lọc trùng (157 ảnh test, 1.305 ảnh train) và không có số captioning.

### 1.3 UIT-OpenViIC
Bui, Nguyen, Nguyen (UIT). arXiv 2305.04166 (2023), bản tạp chí: Signal Processing: Image Communication 140, 117430 (2026), DOI 10.1016/j.image.2025.117430. 13.100 ảnh, 61.241 caption. Train 9.088, val 2.011, test 2.001 ảnh.

| Mô hình (test, arXiv v2) | B-1 | B-4 | METEOR | ROUGE | CIDEr |
|---|---|---|---|---|---|
| Transformer | 76.71 | 36.23 | 30.27 | 47.73 | 66.90 |
| ORT | 76.93 | 35.56 | 30.48 | 47.64 | 66.89 |
| M² Transformer | 76.01 | 36.07 | 30.20 | 48.31 | 68.73 |
| AoANet | 77.32 | 36.65 | 30.72 | 48.36 | 69.42 |
| RSTNet | 77.37 | 36.77 | 30.71 | 48.96 | 72.72 |
| DLCT | 77.37 | 37.22 | 30.86 | 49.13 | 72.69 |
| DIFNet | 77.69 | 37.67 | 30.90 | 49.13 | 74.19 |
| MDSANet | 78.12 | 38.80 | 31.05 | 49.77 | 75.58 |
| **MDSANet + CAMO** | 78.71 | 38.86 | 31.29 | 50.03 | **76.48** (SOTA đã xác minh) |

- Một kết quả WebSearch nói CIDEr test "59.52-62.47", có thể là của bản tạp chí 2026. Mình **chưa mở được** bản ScienceDirect (403), nên con số này để ở mục Chưa xác minh.
- Ngoài các baseline của chính bài gốc, không tìm thấy bài nào khác báo cáo captioning trên OpenViIC. ViCLIP-OT chỉ dùng OpenViIC để huấn luyện retrieval.

### 1.4 VieCap4H (VLSP 2021, y tế)
Le, Dang, Nguyen, Nguyen, Vu, VNU JCSCE 2022, DOI 10.25073/2588-1086/vnucsce.341. Train 8.032 ảnh / 9.429 caption, public test 1.002 ảnh, private test 1.034 ảnh. Metric là trung bình BLEU. Có 927 lượt nộp hợp lệ.

| Bài | Mô hình | Public | Private |
|---|---|---|---|
| Ban tổ chức (vnucsce.341) | đội tốt nhất | **0.306** | **0.329** |
| Nguyen T.T. et al., arXiv 2209.01304 / JCSCE (vnucsce.369) | Swin + attention-LSTM | 0.302 | hạng 3 private (0.293 theo snippet) |
| ObjectAoA (arXiv 2211.05405, UIT) | ObjectAoA | 0.2959 | 0.2852 |
| K. Nguyen, JCC 2022 (UIT) | MI (X152 + VinVL grid) | 29.23 | 28.82 |
| Bui Cao D. et al., JCSCE (vnucsce.371, UIT) | RSTNet + PhoBERT, grid, SCST | 30.3 (snippet) | 28.9 (snippet) |
| Do B.G. et al., NICS 2022; Vi-DRSNet, MAPR 2022 (UIT) | TG2F / DLCT + M² + adaptive dec. | "competitive" | – (Chưa xác minh số) |

Từ 2023 đến nay không còn bài mới nào trên VieCap4H. Dataset này đã "đóng băng".

### 1.5 ViTextCaps (scene-text, 2026)
Nguyen N.N.-Y., Nguyen A.-D., Nguyen N.H., **Nguyen K.V.**, **Nguyen N.L.-T.** (UIT), arXiv 2604.27712, nộp 2026-04-30. 15.729 ảnh, 74.970 caption. Train 10.996, dev 1.641, test 3.092 ảnh, chia theo nguồn ảnh. Tokenize theo âm tiết, có CI 95%.

| Mô hình (test) | B-1 | B-4 | METEOR | ROUGE-L | CIDEr |
|---|---|---|---|---|---|
| AoA / BUTD / M² | ≈0-0.41 | 0.000 | – | – | ≤0.048 |
| M4C | 0.244 | 0.087 | 0.172 | 0.221 | 0.594 |
| HSTFG | 0.222 | 0.085 | 0.164 | 0.219 | 0.640 |
| **PhonoSTFG** | 0.251 | 0.098 | 0.174 | 0.227 | **0.646** |
| GPT-4o (zero-shot) | 0.283 | 0.106 | 0.282 | 0.255 | 0.140 |
| Human | 0.300 | 0.118 | 0.218 | 0.272 | 0.808 |

- Bài đề xuất các metric chẩn đoán mới: **THR (Text Hallucination Rate)**, NF và OTR. Tác giả công bố "release ViTextCaps, all model code, and evaluation tools".
- Đồ thị trong bài là đồ thị hợp nhất đặc trưng OCR/thị giác/ngữ âm, không phải scene graph. Chính bài còn ghi nhận rằng cạnh cross-modal có thể làm hại kết quả.

### 1.6 Các bộ caption tiếng Việt khác
| Bộ | Bài | Kết quả chính |
|---|---|---|
| **HDUCap** | Hoang A.C., Nguyen H.L., Pham T.-A., Nguyen D.C. (ĐH Hồng Đức), "Benchmarking Vietnamese image captioning: A spatially-aware transformer and the HDUCap dataset", JVCIR, 11/2026, DOI 10.1016/j.jvcir.2026.104963 | Bài đóng (closed). Không có abstract trên S2 hay Crossref. Kích thước và số liệu **Chưa xác minh**. Nhóm này cũng có bài phần mềm gán nhãn bán tự động (hdujs.79.09.2025.977) |
| TPC37K (giao thông) | HaUI 2025 (trên) | 37.056 ảnh, caption **sinh bằng Gemini 2.0 Flash**. PVG đạt CIDEr 142.5 |
| 30VNFoods caption | Nguyen H.V.N. et al., LNNS 2025, DOI 10.1007/978-3-032-05994-9_8 | Chưa xác minh số |
| sViIC | Vu D.A., Pham Q.N.M., Tran G.S., VisualRoBERTa, ACM TALLIP 2024, DOI 10.1145/3654796 | B-4 0.6685, ROUGE-L 0.6320 |
| Crossmodal-3600 (vi) | VELVET, Vu D.A. et al., FAIR 2025 (VAP), DOI 10.15625/vap.2025.0261 | CIDEr 0.318 (vi) và 0.435 (en) |
| Flickr8k-vi | Lam K. et al., RIVF 2023, DOI 10.1109/RIVF60135.2023.10471815 | DeepViT+ViT5, B-4 37.98 |
| Y tế / báo cáo | ViX-Ray (arXiv 2603.15513), PET/CT report generation (arXiv 2509.24739). Các đội UIT tại ImageCLEFmedical Caption 2024-2025 (UIT-DarkCow arXiv 2405.17002, UIT-2Q2T, UIT-Oggy) làm caption tiếng Anh | ngoài phạm vi chính |

---

## 2. SOTA theo dataset (đã xác minh)

| Dataset | SOTA đã xác minh | Ứng viên mới, chưa có số |
|---|---|---|
| UIT-ViIC | ObjectAoA, CIDEr 1.488 (2023) | ViG 2026 |
| KTVIC | GRIT, CIDEr 136.0 (2024) | ViG 2026 (tuyên bố vượt GRIT và vượt "a substantially larger fine-tuned multimodal model") |
| UIT-OpenViIC | MDSANet+CAMO, CIDEr 76.48 (arXiv) | không có |
| VieCap4H | 0.306 / 0.329 avg-BLEU (leaderboard 2021) | không có |
| ViTextCaps | PhonoSTFG, CIDEr 0.646 (2026) | không có |

Khoảng trống quan sát được:
- Không bài nào báo cáo SPICE, CLIPScore tiếng Việt, CHAIR hay một metric đồ thị trên các bộ này. Metric "ảo giác" duy nhất là THR của ViTextCaps, và nó chỉ đo phần scene-text.
- Không có bảng LVLM fine-tune (QLoRA Qwen2.5-VL, Vintern) trên KTVIC hay OpenViIC. ViG chỉ nhắc tới "larger fine-tuned multimodal model" mà không nêu tên trong abstract.

---

## 3. Nhóm UIT đang hoạt động và hướng 2025-2026

| Nhóm / tác giả | Bài 2025-2026 (đã xác minh) | Hướng | Mức va chạm với KG-caption |
|---|---|---|---|
| **UIT NLP: Kiet Van Nguyen, Ngan Luu-Thuy Nguyen, Nghia Hieu Nguyen** | ViTextCaps/PhonoSTFG (2604.27712); ViTextVQA (ESWA 2026, 10.1016/j.eswa.2025.130839); ViOCRVQA (Multimedia Systems 2025); ViSignVQA (2512.22218); LiGT (IJDAR 2025, 2502.19202); ViPhoVQA (ICCCI 2025); character-level TextVQA (MAPR 2025); sinh dữ liệu VQA bằng MLLM (KSE 2025); dịch ảnh Hán-Nôm sang tiếng Việt bằng RLHF (MAPR 2026, 2607.11434); VLSP 2025 MLQA-TSR (2510.20381) | scene-text, ngữ âm/âm tiết, tài liệu, sinh dữ liệu bằng MLLM | **Trung bình**. Họ dùng "graph" như kiến trúc fusion. Họ đã có THR và tạo dữ liệu bằng MLLM, nên có thể nhanh chóng mở rộng sang hallucination |
| **UIT, Phung Do, Huynh Ngoc Nhan, Vu Thien Hieu, Pham Dinh Thang Cap** | **ViG** (MAPR 2026) | relation memory trên vùng, query văn hóa Việt, trên KTVIC và UIT-ViIC | **Cao**. Không nên lấy "encoder nhận biết quan hệ" làm điểm mới |
| UIT CV: Khang Nguyen, Doanh C. Bui | UIT-OpenViIC bản tạp chí (SPIC 2026). Không tìm thấy bài captioning mới nào khác | đóng gói benchmark | Thấp |
| UIT, Thien B. Nguyen-Tat | ImageCLEFmedical Caption 2024-2025 | caption y tế tiếng Anh | Thấp |
| Ngoài UIT | ĐH Hồng Đức (HDUCap, Attention Fusion); ĐH Cần Thơ (ViCLIP-OT); HCMUTE (TPC37K); ĐHSP TP.HCM (HUFLIT); VNU-UET (KTVIC); VNU-HUS (viSemParse AMR) | | HDUCap ("spatially-aware") có thể va chạm phần quan hệ không gian. Chưa đọc được |

---

## 4. Dataset có nhãn đồ thị hoặc quan hệ: tình trạng
- **Không tìm thấy dataset UIT (hay dataset tiếng Việt nào) có nhãn scene graph hoặc quan hệ cho ảnh**, cả qua arXiv (`abs:vietnamese AND abs:"scene graph"` cho 0 kết quả) lẫn qua S2 và WebSearch. Cũng không có thông báo nào về chuyện này.
- Gần nhất về đồ thị nhưng chỉ có văn bản: **VLSP 2025 viSemParse** (Ha My Linh, Pham Thi Duc, Le Ngoc Toan, Nguyen Thi Minh Huyen, VNU-HUS; ACL Anthology 2025.vlsp-1.30). Bộ này có 2.500 câu AMR định dạng PENMAN, hệ thống tốt nhất đạt Smatch 58%. MASSIVE-AMR (Regan et al. 2024) cũng có tiếng Việt. Có thể dùng làm hạt giống cho parser caption→graph tiếng Việt.
- Thông tin quan hệ chỉ có ở dạng **ngầm**: ViG học quan hệ cặp vùng mà không có nhãn, còn KTVIC có quy tắc viết caption có vị trí ("ở trên", "bên cạnh").

---

## 5. Hệ quả cho kế hoạch KG
1. **Tránh lấy "relation-aware encoder trên GRIT" làm đóng góp chính** vì ViG đã làm. Nên chọn phần đang trống: (a) **nhãn đồ thị có kiểm chứng** cho KTVIC và OpenViIC (VSPS propositions sang scene graph); (b) **metric đồ thị tiếng Việt** (SPICE-vi hoặc graph P/R theo loại), vì chưa bài nào có; (c) **bảng LVLM** (Vintern, Qwen2.5-VL, Qwen3-VL) trên KTVIC và OpenViIC.
2. **Bắt buộc báo cáo trên KTVIC đã lọc trùng** (giao thức của ViCLIP-OT) hoặc giải thích rõ vì sao không. Nếu không, reviewer có thể nói có rò rỉ dữ liệu với OpenViIC.
3. Khi so sánh, phải ghi rõ tokenizer và thang đo. Nên chạy lại GRIT bằng code công khai thay vì chép số từ các bài khác.
4. Nhóm Kiet Nguyen đi rất nhanh, khoảng 2-3 bài đa phương thức mỗi quý. Nên công bố sớm, ví dụ một bản preprint benchmark, để khẳng định ưu tiên.

---

## Chưa xác minh
- Số liệu của ViG (MAPR 2026). Bài đóng, trang IEEE không đọc được. Tên "larger fine-tuned multimodal model" cũng chưa rõ.
- HDUCap: kích thước, metric, ảnh nguồn, và liệu có nhãn quan hệ không gian hay không.
- Số CIDEr test của UIT-OpenViIC bản SPIC 2026 (snippet "59.52-62.47" khác với 76.48 của bản arXiv).
- Tên đội thắng VieCap4H. Số public/private của Bui Cao D. et al. (30.3/28.9) và của Swin-LSTM private (0.293) lấy từ snippet tìm kiếm, chưa đối chiếu bảng.
- Số liệu của NICS 2022 TG2F, Vi-DRSNet và 30VNFoods caption.
- Đơn vị công tác của tác giả AutoViVQA (2603.09689), ViInfographicVQA (2512.12424) và VMMU (2508.13680) chưa kiểm tra, nên chưa xếp vào nhóm UIT.
