# R2_01: Mức SOTA phải vượt cho captioning tiếng Việt, và chỗ VSPS đang đứng

Agent R2_01, 2026-10-11. File này mở rộng `kg_plan/14_uit_leaderboard.md` (bảng xếp hạng 2021-2026) và `research_wall/08_journal_standards_2025_2026.md` (chuẩn tạp chí), không làm lại hai file đó. Phần mới: đọc lại PDF của KTVIC để chốt giao thức token hóa, đối chiếu từng metric với số của chính repo (`data/results/*.json`), kiểm tra lại các LVLM tiếng Việt (Vintern, LaVy, Vistral-V, VinaLlama-VL), và rút ra phán quyết cho một bài Q1/Q2.

**5 dòng tóm tắt**
1. SOTA đã công bố trên KTVIC vẫn là **GRIT: B-1 74.7, B-4 40.6, METEOR 36.6, ROUGE-L 59.7, CIDEr 136.0** (arXiv 2401.08100, token hóa từ bằng RDRSegmenter). VSPS (short, seed 42) đạt **35.7 / 7.0 / 22.1 / 30.9 / 17.3**, tức kém **118.7 điểm CIDEr**.
2. Chính repo đã có **P1 (QLoRA Qwen2.5-VL-7B SFT trên caption gold) đạt CIDEr 149.8, B-4 45.5, METEOR 39.1, ROUGE-L 64.2, vượt GRIT ở mọi metric** với cùng segmenter. P1 còn có **CHAIR_i 19.2%, thấp hơn VSPS (44.6%)**. Đây là đối thủ nguy hiểm nhất, và nó nằm ngay trong bài.
3. **Chưa bài nào báo cáo SPICE, CLIPScore hay metric ảo giác** (CHAIR/POPE) trên KTVIC, UIT-ViIC hay OpenViIC. Metric ảo giác tiếng Việt duy nhất là THR của ViTextCaps (chỉ đo scene-text). Vintern, LaVy, Vistral-V và VinaLlama-VL **không có số captioning chuẩn nào** đã công bố.
4. Theo bảng của các tạp chí Q1/Q2 trong giai đoạn 2023-2026, bảng bắt buộc gồm **B-1..4, METEOR, ROUGE-L, CIDEr**, trên ≥ 2 dataset, kèm seeds. Bài nào về ảo giác thì thêm CHAIR/POPE/AMBER và human eval (200 ảnh × 3 rater, κ). Chỉ có object F1 là **không đủ**.
5. Phán quyết: để lên Q1/Q2, VSPS phải **(a)** không thua P1 về n-gram ở short mode (mục tiêu CIDEr ≥ 136, tức GRIT), **(b)** thắng P1 về CHAIR/object F1, và **(c)** có thêm một dataset thứ hai cùng tập KTVIC đã lọc trùng (157 ảnh). Nếu không đạt được (a), reviewer sẽ kết luận "cứ SFT trên gold là đủ".

---

## 1. Giao thức đo: các con số có so được với nhau không?

- **KTVIC (bài gốc)**: so sánh với ground truth là "the segmented caption", tức caption đã được tách từ bằng **RDRSegmenter** (PDF §3 và §5.1, Bảng 3). Bài chỉ báo cáo B-1, B-4, METEOR, ROUGE và CIDEr, **không có B-2, B-3 và SPICE**. Code GRIT-vicap: https://github.com/davidnvq/grit/tree/vicap.
- **Repo VSPS**: `data/results/*.json` ghi `"segmenter": "rdrsegmenter"`, `"tokenization": "từ (word-level)"` và `"scale": "x100 (như số công bố của KTVIC)"`. Như vậy, **cột word-level của repo so trực tiếp được với GRIT**. Có một điểm cần lưu ý: METEOR có thể lệch do bản cài đặt khác nhau (java METEOR 1.5 so với bản nltk). Bài cần ghi rõ bản nào được dùng, hoặc chạy lại GRIT-vicap trên cùng evaluator.
- **UIT-ViIC** dùng thang 0-1 (CIDEr 1.488 tương đương 148.8) và token PyVI. **ViTextCaps** dùng âm tiết. Không được đặt chung một bảng với KTVIC (xem `kg_plan/14`, mục tóm tắt 1).
- **Rò rỉ dữ liệu**: 401/558 ảnh test KTVIC trùng gần với ảnh train của UIT-OpenViIC (ViCLIP-OT, arXiv 2602.22678). Nếu VSPS huấn luyện thêm trên OpenViIC, bắt buộc phải báo cáo thêm tập con đã lọc trùng (157 ảnh).

## 2. Bảng chính: metric, SOTA hiện tại, VSPS hiện tại, khoảng cách

Dataset KTVIC test (558 ảnh), short mode, token hóa từ bằng RDRSegmenter, thang x100. Cột "VSPS" lấy từ `data/results/main_s42-short.json` (VSPS proposed, seed 42). Trung bình 3 seed theo v7: CIDEr 17.4 ± 0.2. Cột "P1" lấy từ `p1-gold-short.json`.

| Metric | Best đã công bố (bài, venue, link) | VSPS hiện tại | Gap vs SOTA | P1 gold-SFT (repo) | Zero-shot Qwen2.5-VL-7B (repo) |
|---|---|---|---|---|---|
| BLEU-1 | **74.7**, GRIT, KTVIC arXiv 2024, https://arxiv.org/abs/2401.08100 | 35.7 | **−39.0** | 79.0 | 30.7 |
| BLEU-2 | không công bố trên KTVIC | 23.4 | n/a | 66.0 | 17.5 |
| BLEU-3 | không công bố trên KTVIC | 13.9 | n/a | 54.7 | 9.8 |
| BLEU-4 | **40.6**, GRIT (như trên) | 7.0 | **−33.6** | 45.5 | 5.5 |
| METEOR | **36.6**, GRIT (như trên) | 22.1 | **−14.5** (chưa thống nhất bản cài đặt) | 39.1 | n/a |
| ROUGE-L | **59.7**, GRIT (như trên) | 30.9 | **−28.8** | 64.2 | 25.6 |
| CIDEr | **136.0**, GRIT (như trên). ViG (MAPR 2026, DOI 10.1109/MAPR72750.2026.11685699) tuyên bố vượt GRIT "on every standard metric" nhưng **UNVERIFIED** (bài closed, chưa có số) | **17.3** (17.4 ± 0.2) | **−118.7** | **149.8** | 29.0 |
| SPICE | **chưa ai công bố**: không có parser scene graph tiếng Việt (UIT-OpenViIC ghi rõ, arXiv 2305.04166) | chưa đo (`SPICE=None`) | không xác định | chưa đo | chưa đo |
| CLIPScore / RefCLIPScore | **chưa ai công bố** trên dataset caption tiếng Việt. Multilingual CLIP-S: Gomes et al., Findings NAACL 2025, https://arxiv.org/abs/2502.06600 (bài không nói rõ có tiếng Việt) | chưa đo | không xác định | chưa đo | chưa đo |
| CHAIR_i (↓) | **chưa ai công bố** trên KTVIC | 44.6% | không có mốc | **19.2%** | 42.9% |
| CHAIR_s (↓) | chưa ai công bố | 58.8% | không có mốc | 28.7% | 62.0% |
| Object P/R/F1 | chưa ai công bố | 41.5 / 36.7 / 39.0 (brief) | không có mốc | chưa tính (cần chạy) | 31.6 / 57.1 / 40.7 |
| Metric ảo giác tiếng Việt khác | **THR** (Text Hallucination Rate) của ViTextCaps, chỉ áp dụng cho scene-text, arXiv 2604.27712 (2026) | không áp dụng | không áp dụng | không áp dụng | không áp dụng |
| Human eval | chưa ai làm trên KTVIC | faithfulness 3.91, completeness 2.64, fluency 3.17 (50 ảnh, 2 rater, κ 0.86-0.95) | không có mốc | chưa có | 4.17 / 4.47 / 4.29 |

Detailed mode trên KTVIC (không có SOTA nào công bố, vì KTVIC chỉ có caption ngắn):

| | VSPS (`main_s42-detailed`) | Zero-shot | P1 gold-SFT |
|---|---|---|---|
| CHAIR_i / CHAIR_s | 50.1% / 79.2% | 65.1% / 98.0% | 19.5% / 29.2% |
| Mentions/caption | 3.13 | 6.54 | 1.83 (thực chất vẫn là caption ngắn) |
| CIDEr (word) | 2.8 | 0.0 | 146.2 |

Các dataset khác (VSPS **chưa chạy** trên dataset nào trong số này):

| Dataset | SOTA đã xác minh | Nguồn | VSPS |
|---|---|---|---|
| UIT-ViIC | ObjectAoA, B-4 0.497, METEOR 0.373, ROUGE-L 0.648, CIDEr 1.488 | VNU JCSCE 38(1) 2023, https://arxiv.org/abs/2211.05405 | chưa chạy |
| UIT-OpenViIC | MDSANet+CAMO, B-1 78.71, B-4 38.86, METEOR 31.29, ROUGE-L 50.03, CIDEr 76.48 (bản arXiv). Bản tạp chí: Signal Processing: Image Communication 140 (2026) 117430, DOI 10.1016/j.image.2025.117430. Số của bản tạp chí **UNVERIFIED** (Crossref không có abstract, ScienceDirect trả 403) | https://arxiv.org/abs/2305.04166 | chưa chạy |
| VieCap4H | avg-BLEU 0.306 (public) / 0.329 (private) | VNU JCSCE 2022, DOI 10.25073/2588-1086/vnucsce.341 | ngoài phạm vi (y tế) |
| ViTextCaps | PhonoSTFG, CIDEr 0.646 (âm tiết). GPT-4o zero-shot đạt CIDEr 0.140 | arXiv 2604.27712 (2026) | ngoài phạm vi (scene-text) |
| HDUCap | **UNVERIFIED**: JVCIR 2026, DOI 10.1016/j.jvcir.2026.104963, bài closed, không có abstract trên Crossref | | |

## 3. LVLM tiếng Việt: có ai đã đặt mốc captioning chưa?

Kiểm tra trong phiên này (arXiv API với `abs:vietnamese AND abs:captioning`, 9 kết quả, mới nhất là 2026-06; thêm bản HTML của từng bài):

- **Vintern-1B** (Doan et al., arXiv 2408.12480, 2024): chỉ báo cáo VQA với GPT-4o làm giám khảo (OpenViVQA-dev, ViTextVQA-dev, khoảng 7.7/10) và VLSP 2023 (F1 3.46, avg-BLEU 0.442). **Không có số captioning trên KTVIC, UIT-ViIC hay OpenViIC.** https://arxiv.org/abs/2408.12480
- **LaVy** (arXiv 2404.07922, preprint, chưa có venue): OpenViVQA zero-shot 45.3 (Gemini chấm), LaVy-Bench "Detail description" 53.1. **Không dùng BLEU/CIDEr**; bài còn đề xuất bỏ BLEU. https://arxiv.org/abs/2404.07922
- **Vistral-V, VinaLlama-VL**: không tìm thấy bài báo hay bảng captioning nào. **UNVERIFIED**, nhiều khả năng chỉ có model card.
- **ViG** (MAPR 2026) tuyên bố "outperforms a substantially larger fine-tuned multimodal model" trên KTVIC, nhưng tên mô hình và số liệu đều **UNVERIFIED**. Đây là mốc nguy hiểm nhất: nếu LVLM fine-tune mà ViG so sánh nằm quanh mức P1 của repo (149.8), thì ViG đặt mốc trên 136 và có thể trên cả 149.8.
- Kết luận: **chưa ai công bố bảng LVLM captioning chuẩn trên KTVIC.** P1 của repo (CIDEr 149.8) nhiều khả năng là con số LVLM fine-tune cao nhất từng đo trên KTVIC. Đây là một đóng góp phụ hợp lệ ("first LVLM baseline table on KTVIC"), với điều kiện chạy lại GRIT trên cùng evaluator.

## 4. Các tạp chí Q1/Q2 (2023-2026) yêu cầu những bảng gì

Bổ sung cho `research_wall/08` (file đó đã có protocol của Sci. Rep. 2026, Metric-RL IEEE Access 2026, MHR TOMM 2026, CLVA PR 2026 và các bài TALLIP 2025). Quartile được ghi theo cảm nhận chung của cộng đồng; cần đối chiếu SJR trước khi nộp (**UNVERIFIED** từng journal).

| Bài | Venue, năm, DOI hoặc link | Bảng kết quả bắt buộc trong bài |
|---|---|---|
| UIT-OpenViIC (Bui, Nguyen, Nguyen) | Signal Processing: Image Communication 2026, 10.1016/j.image.2025.117430 | B-1..4, METEOR, ROUGE-L, CIDEr cho 9 baseline Transformer. Không có SPICE (vì không có scene graph tiếng Việt). Có phân tích theo độ dài và độ phức tạp của caption |
| VisualRoBERTa, sViIC (Vu, Pham, Tran) | ACM TALLIP 2024, 10.1145/3654796 | B-4 0.6685, ROUGE-L 0.6320 (theo `kg_plan/14`) |
| HDUCap, spatially-aware transformer | JVCIR 2026, 10.1016/j.jvcir.2026.104963 | **UNVERIFIED** (closed) |
| Benchmarking LVLMs for low-resource multilingual captioning (Urdu/Arabic) | Scientific Reports 2026, 10.1038/s41598-026-70568-5 | B-1..4, ROUGE-L, METEOR, chrF, BERTScore; 9 VLM × {zero-shot, LoRA, QLoRA}; 3 seed; human eval 200 ảnh × 3 rater, κ; error taxonomy (ảo giác vật thể khoảng 21%) |
| Metric-Driven RL for object hallucination | IEEE Access 2026, 10.1109/ACCESS.2026.3723028 | CHAIR + Coverage (object recall) **cộng** BLEU/METEOR/SPICE/BERTScore |
| TALLIP Hindi/Assamese captioning 2025 | 10.1145/3749641, 10.1145/3717612 | B-n + CIDEr trên COCO dịch máy (theo abstract) |
| Benchmark đa ngôn ngữ cho caption ảnh viễn thám (en/zh) | arXiv 2503.04592. Semantic Scholar ghi venue là Pattern Recognition 2025, **UNVERIFIED** | 8 LVLM × {zero-shot, SFT, multilingual}; bảng metric cụ thể **UNVERIFIED** |
| Benchmark cho detailed caption: CAPTURE | arXiv 2405.19092 | metric trên đơn vị object/attribute/relation dành cho caption dài. Có thể dùng thay SPICE khi không có parser tiếng Việt |
| DeCapBench / DCScore | ICLR 2025, https://arxiv.org/abs/2503.07906 | đánh giá detailed caption ở mức "primitive information unit", tính cả ảo giác lẫn độ đầy đủ |

Mẫu chung của bài low-resource captioning ở Q1/Q2:
1. **Bảng n-gram chuẩn COCO-style (B-1..4, M, R, C) là điều kiện cần.** Không bài nào chỉ báo cáo object F1.
2. Có ≥ 1 benchmark công khai cùng ≥ 3 baseline; bài LVLM thì thêm zero-shot và LoRA/QLoRA của 2-9 backbone.
3. Bài về ảo giác thì thêm CHAIR (và thường cả POPE/AMBER), mean ± sd trên 3 seed, human eval có κ.
4. Detailed caption thì thêm metric theo đơn vị nội dung (CAPTURE, DCScore), vì CIDEr gần như bằng 0 khi caption dài (repo: VSPS detailed đạt CIDEr 2.8).

## 5. Phân tích khoảng cách: vì sao con số 17.3 là vấn đề sống còn

1. **Khoảng cách với SOTA rất lớn: −118.7 CIDEr, −33.6 B-4.** Bản v7 giải thích rằng template "không theo phong cách" caption tham chiếu. Lời giải thích đó đúng, nhưng reviewer Q1 sẽ không chấp nhận một phương pháp kém GRIT 8 lần về CIDEr trên chính benchmark mà bài sử dụng.
2. **P1 thắng VSPS ở cả hai trục.** P1 có CIDEr 149.8 so với 17.3, và CHAIR_i 19.2% so với 44.6%. Luận điểm "VSPS giảm ảo giác" hiện chỉ đứng được khi so với zero-shot (detailed 50.1% so với 65.1%), không đứng được khi so với P1. Phần biện hộ duy nhất là P1 sinh caption ngắn (1.83 mentions/caption), nên CHAIR của nó thấp một phần nhờ nói ít. Muốn biện hộ được, phải chứng minh bằng **object recall/F1 của P1** (repo chưa tính) và bằng completeness trong human eval.
3. **Human eval hiện tại chưa ủng hộ VSPS.** Zero-shot có faithfulness 4.17, VSPS 3.91 (Wilcoxon p = 0.118, không có ý nghĩa thống kê). Completeness và fluency của zero-shot cao hơn rõ rệt (p < 0.001). Mẫu chỉ có 50 ảnh và 2 rater, dưới mức 200 × 3 của Sci. Rep. 2026.
4. **Khoảng trống còn trống, có thể chiếm được:** SPICE-vi hoặc metric đồ thị tiếng Việt, CLIPScore-vi, CHAIR-vi/POPE-vi trên KTVIC, bảng LVLM trên KTVIC. Chưa ai công bố các mục này (mục 2, mục 3). Đây là đóng góp benchmark và metric, không phải ghép lego, nhưng chỉ có giá trị nếu phương pháp chính không thua ở n-gram.

## 6. Phán quyết: một bài Q1/Q2 phải cho thấy những gì

Bắt buộc (thiếu mục nào thì bị reject ở vòng 1):
1. **Bảng n-gram KTVIC đầy đủ**: B-1..4, METEOR, ROUGE-L, CIDEr, dùng RDRSegmenter word-level và ghi rõ evaluator. Có **GRIT-vicap chạy lại** trên cùng evaluator, có P1, zero-shot, mean ± sd trên 3 seed, và bootstrap CI.
2. **Ở short mode, VSPS phải đạt ít nhất mức P1** (sàn hợp lý: CIDEr ≥ 136, tức GRIT; mục tiêu: không thấp hơn P1 quá khoảng trong bootstrap CI), đồng thời **thắng P1 về CHAIR_i và object F1**. Cách khả thi nhất là để caption gold làm "style anchor" và để các mệnh đề đã kiểm chứng làm "content constraint" (SFT trên gold cộng với lọc hoặc bổ sung bằng mệnh đề SUPPORTED). Cách này không thay gold bằng template. Đây là điều kiện tiên quyết của hướng Know-and-Mention ở `05_TONG_HOP_XEP_HANG.md`: trục *đáng nhắc* phải học từ gold, vì 38% object gold chỉ có 1/5 người nhắc.
3. **Có ≥ 2 dataset**: KTVIC cộng UIT-OpenViIC (mốc CIDEr 76.48), hoặc cộng UIT-ViIC (mốc 148.8). Có tập con KTVIC đã lọc trùng (157 ảnh).
4. **Bảng ảo giác**: CHAIR_i/CHAIR_s, object P/R/F1 và POPE-vi. AMBER nếu làm được.
5. **Detailed mode**: dùng metric theo đơn vị nội dung (kiểu CAPTURE hoặc DCScore, chuyển sang tiếng Việt bằng parser mệnh đề của chính VSPS), vì CIDEr và BLEU vô nghĩa với caption dài.
6. **Human eval**: 200 ảnh × 3 rater, Fleiss κ, kèm error taxonomy (object/attribute/count/relation/gender).

Nên có (nâng từ Q2 lên Q1):
- SPICE-vi hoặc metric đồ thị tiếng Việt kèm validation tương quan với người đánh giá. Đây là mục đầu tiên trong lĩnh vực.
- CLIPScore đa ngôn ngữ làm metric phụ không cần tham chiếu.
- Một backbone thứ hai (Qwen3-VL-8B hoặc InternVL3.5-8B) và Vintern-3B zero-shot.
- So sánh với ViG ngay khi có số (theo dõi IEEE Xplore).

Bước kiểm tra chi phí thấp nhất (không cần GPU, chạy được ngay): tính **object P/R/F1 của P1** bằng cùng script đã tính 41.5/36.7/39.0. Nếu F1 của P1 ≥ 39.0, luận điểm chính của VSPS hiện tại không đứng được ở mọi trục, và điểm mới phải nằm ở cách *kết hợp* gold với verifier (mục 6.2), không nằm ở template.

---
Nguồn đã mở trong phiên: PDF KTVIC (arXiv 2401.08100, Bảng 3 và §5.1); Crossref với DOI của ViG, OpenViIC SPIC và HDUCap; Semantic Scholar (abstract ViG, danh sách bài trích dẫn KTVIC); arXiv API; bản HTML của Vintern-1B (2408.12480) và LaVy (2404.07922). Số của repo lấy từ `data/results/{main_s42,p1-gold,zeroshot,vsps}-{short,detailed}.json`, `human_eval.json` và `.paper_work/v7.txt` (Bảng I).
