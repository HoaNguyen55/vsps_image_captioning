# 02. Metric chất lượng caption: khảo sát 2021–2026 và kế hoạch áp dụng

Phạm vi: chỉ metric chất lượng tổng quát. Benchmark ảo giác (CHAIR, POPE…) nằm ở một tài liệu khác.
Bối cảnh: KTVIC-vi (558 ảnh test, 5 tham chiếu/ảnh) và COCO-2014 en (5k). Mô hình là Qwen2.5-VL-7B + QLoRA. Chỉ được dùng **1 RTX 3090 24 GB**.
Quy ước: mọi bài đều đã kiểm trên arXiv/ACL Anthology/CVF ngày 12/10/2026. "Code ✓" nghĩa là repo GitHub đã được xác nhận tồn tại qua `gh api`. Mục nào chưa kiểm được thì ghi **UNVERIFIED**.

## 0. Vì sao CIDEr sụp: con số đo trong repo

| Hệ thống (KTVIC test) | Độ dài TB (âm tiết) | B-1 | B-4 | R-L | CIDEr |
|---|---|---|---|---|---|
| P1 gold-SFT, prompt detailed | 12.2 | 78.0 | 44.4 | 64.2 | 146.2 |
| fuse2_s42, prompt short | 12.4 | 77.4 | 42.3 | 63.7 | 143.9 |
| fuse2_s42, prompt detailed | **24.0** | 50.7 | 27.2 | 49.5 | **23.9** |

Tham chiếu KTVIC dài trung bình 12.1 âm tiết. CIDEr của pycocoevalcap thực chất là **CIDEr-D**. Hàm `sim()` nhân mỗi cặp (ứng viên, tham chiếu) với `exp(-(len_c - len_r)^2 / (2·6^2))`, nên khi lệch 12 token thì hệ số chỉ còn e^-2 ≈ 0.135. Ước lượng trên preds thật (theo âm tiết; theo từ sau RDRSegmenter thì tỉ lệ tương tự): hệ số phạt trung bình là **0.93 ở short** và **0.21 ở detailed**. Vậy riêng hình phạt độ dài đã giải thích khoảng 80% mức sụp. Phần còn lại là do cosine TF-IDF bị pha loãng bởi n-gram không có trong 5 tham chiếu, gồm cả các chi tiết *đúng* mà người chú thích không viết. Ở chế độ short, khi độ dài ngang nhau, fuse2 gần như hòa P1 về n-gram (143.9 so với 146–150).
→ Kết luận: CIDEr-D đo "giống tham chiếu ~12 âm tiết", không đo mức đầy đủ của caption. Cần bổ sung các metric không bị phạt theo độ dài, và phải tách riêng *precision* với *coverage*.

## 1. Bảng so sánh

Cột "VI": mức hỗ trợ tiếng Việt và chi phí port. "3090": chi phí cho 558 ảnh × 1 hệ thống, trừ khi ghi khác. "Độ dài": thiên lệch theo độ dài caption. "Q1": mức reviewer Q1 kỳ vọng.

| Metric | Nguồn (arXiv · venue · code) | Đo gì | Ref-free | VI | 3090 | Độ dài | Q1 |
|---|---|---|---|---|---|---|---|
| **CLIPScore / RefCLIPScore** | 2104.08718 · EMNLP'21 · jmhessel/clipscore ✓ | Cosine ảnh–caption (Ref: + max cosine với tham chiếu) | Có / không | Thay CLIP bằng CLIP đa ngữ, không cần train | < 1 phút | Gần như không phạt độ dài, nhưng CLIP chỉ nhận 77 token và theo Long-CLIP (2403.15378, ECCV'24) chỉ "dùng thật" khoảng 20 token đầu, nên khó ghi nhận chi tiết thêm vào cuối | **Gần như bắt buộc** |
| **Multilingual CLIPScore** (Gomes, Zerva, Martins) | 2502.06600 · Findings NAACL'25 · gecgomes/Multilingual_IC_Eval ✓ | CLIPScore với `laion/CLIP-ViT-H-14-frozen-xlm-roberta-large-laion5B-s13B-b90k` (MLAION), cùng bản fine-tune MLF | Có | Dùng được ngay. **Lưu ý: tập human judgment của bài là tiếng Anh cộng bản dịch máy sang 9 ngôn ngữ (fr, de, es, zh, pt, it, ru, nl, ko); không có tiếng Việt** → phải tự kiểm trên human eval của mình | ~1B tham số fp16, khoảng 3 GB; vài phút cho 5k ảnh | Như CLIPScore | Trích dẫn kèm metric trên là đủ thuyết phục |
| M-CLIP (XLM-R-L + ViT-B/16+, L/14) | Carlsson et al. LREC'22 (bài **UNVERIFIED** trong phiên này) · FreddeFrallan/Multilingual-CLIP ✓ | Như trên | Có | Có XLM-R → có vi | < 1 phút | Như trên | Phương án dự phòng |
| SigLIP 2 / mSigLIP | 2502.14786 · arXiv (Google DeepMind) · HF `google/siglip2-*` | Sigmoid image–text | Có | Đa ngữ (tokenizer Gemma). Danh sách ngôn ngữ chưa kiểm; XM3600 có vi | Nhẹ | Văn bản bị cắt ở 64 token | Robustness check |
| jina-clip-v2 | 2412.08802 · ICLR'25 workshop · HF `jinaai/jina-clip-v2` | Embedding ảnh–văn bản, 89 ngôn ngữ | Có | Có vi hay không: **UNVERIFIED** (model card không liệt kê). License CC BY-NC | 0.9B, nhẹ | **Văn bản tối đa 8192 token**, nên hợp với caption dài | Robustness check cho detailed |
| ViCLIP-OT | 2602.22678 · preprint (ESWA submitted) · weights **UNVERIFIED** | CLIP tiếng Việt, có đánh giá retrieval trên KTVIC/OpenViIC | Có | Thuần Việt | Nhẹ | Chưa rõ | Đẹp nhưng chưa có weights → không dựa vào |
| PAC-S / PAC-S++ | 2303.12112 · CVPR'23; 2410.07336 (PAC-S++, arXiv'24) · aimagelab/pacscore ✓ | CLIP fine-tune với positive tăng cường | Có (+Ref) | **Chỉ tiếng Anh**; port cần train lại | Nhẹ | Kế thừa giới hạn 77 token | Chuẩn cho COCO-en |
| Polos | 2402.18091 · CVPR'24 · YuigaWada/Polos ✓ | Metric có giám sát, học từ 131K human judgment (Polaris) | Không (cần ref) | Chỉ tiếng Anh, port cần human data tiếng Việt | Nhẹ | Học từ caption ngắn | Tốt cho COCO-en |
| DENEB | 2409.19255 · ACCV'24 · Ka2ukiMatsuda/DENEB ✓ | Sim-Vec Transformer, xử lý nhiều tham chiếu, bền với ảo giác | Không | Chỉ tiếng Anh | Nhẹ | Học từ caption ngắn | Tùy chọn cho COCO |
| Pearl | 2512.21582 · AAAI'26 · code **UNVERIFIED** (pearl.kinsta.page) | LLM-free, chạy được cả có ref lẫn không ref | Cả hai | Chỉ tiếng Anh | Nhẹ | Chưa rõ | Mới, tùy chọn |
| BRIDGE | 2407.20341 · ECCV'24 · aimagelab/bridge-score ✓ | Pseudo-caption kèm đặc trưng thị giác dày | Có | Chỉ tiếng Anh | Nhẹ | 77 token | Tùy chọn |
| HICE-S | 2407.18589 · ACM MM'24 · joeyz0z/HICE ✓ | Chấm phân cấp vùng–cụm từ (cục bộ và toàn cục) | Có | Chỉ tiếng Anh (cần parser cụm từ tiếng Anh) | Cần detector + SAM, vừa phải | Chấm theo cụm nên đỡ bias hơn CLIP-S | Tùy chọn |
| InfoMetIC | 2305.06002 · ACL'23 · HAWLYQ/InfoMetIC ✓ | Text precision + vision recall + overall, chỉ ra từ sai và vùng chưa được nhắc | Có | Chỉ tiếng Anh | Nhẹ | **Có nhánh recall** nên hợp ý tưởng | Tùy chọn |
| BERTScore | 1904.09675 · ICLR'20 · Tiiiger/bert_score ✓ | Khớp token bằng embedding, P/R/F | Không | `xlm-roberta-large` (layer 17) chạy được vi ngay. PhoBERT (2003.00744, Findings EMNLP'20, VinAIResearch/PhoBERT ✓) cần input đã tách từ và tự đặt `num_layers`. ViSoBERT (2310.11166, EMNLP'23) là domain mạng xã hội, không hợp | < 5 phút | **P giảm, R tăng khi caption dài** → phải báo riêng P và R | Thường được kỳ vọng như một metric ngữ nghĩa có ref |
| MoverScore | 1909.02622 · EMNLP'19 · AIPHES/emnlp19-moverscore ✓ | EMD trên embedding | Không | Port được bằng mBERT/XLM-R | Nhẹ | Như BERTScore | Thừa nếu đã có BERTScore |
| CLAIR | 2310.12971 · EMNLP'23 · DavidMChan/clair ✓ | LLM chấm 0–100 so với ref, kèm lý do | Không | Prompt được bằng tiếng Việt. Bài cho thấy LLM mở cỡ nhỏ (Koala, Vicuna) **tương quan kém** | API, hoặc LLM 7–8B: ~0.3 GPU-h | LLM thường thích caption dài | Tùy chọn |
| FLEUR | 2406.06004 · ACL'24 · Yebin46/FLEUR ✓ | LLaVA chấm điểm có score smoothing và giải thích | Có | LLaVA-1.5 yếu tiếng Việt | LLaVA-13B cần 4-bit; ~1 GPU-h cho 5k ảnh | Thiên vị caption dài | Tùy chọn cho COCO |
| G-VEval | 2412.13647 · AAAI'25 · code **UNVERIFIED** | GPT-4o + CoT; 3 chế độ ref-free / ref-only / combined | Cả hai | GPT-4o đọc được tiếng Việt | API | Rubric có tiêu chí "conciseness" | Mạnh nếu dùng được API |
| VisCE² | 2402.17969 · arXiv'24 · code **UNVERIFIED** | VLM trích visual context (đối tượng, thuộc tính, quan hệ) rồi chấm | Có | Đổi VLM là chạy được | ~1 GPU-h | — | Tùy chọn |
| VELA + LongCap-Arena | 2509.25818 · EMNLP'25 · Ka2ukiMatsuda/VELA ✓ | Metric cho **caption dài**: LLM non-autoregressive + late fusion; chấm Descriptiveness / Relevance / Fluency | Không | Chỉ tiếng Anh (học trên DCI) | Nhẹ hơn LLM-judge | **Thiết kế riêng cho caption dài** | Rất hợp cho COCO-en detailed |
| CapArena / CapArena-Auto | 2503.12329 · Findings ACL'25 · njucckevin/CapArena ✓ | Đấu cặp caption chi tiết. Bản Auto: 600 ảnh, GPT-4o làm judge, 3 baseline, ~4 USD, tương quan 94.3% với xếp hạng người. Bài chỉ ra **METEOR có tương quan khá ở mức caption nhưng xếp hạng mô hình lệch**, còn VLM-as-judge ổn ở cả hai mức | Auto có ref | Ảnh và ref tiếng Anh; dùng **giao thức** (pairwise + baseline) cho vi | API | Pairwise giảm bias tuyệt đối nhưng judge vẫn thích caption dài | Rất được chuộng 2025–26 |
| CAPTURE | 2405.19092 · arXiv'24 · foundation-multimodal-models/CAPTURE ✓ (pip `capture-metric`) | Trích (đối tượng, thuộc tính, quan hệ) từ caption và ref, khớp 3 giai đoạn, ra F1 | Không | Parser tiếng Anh → **port bằng `rescap/svp`** (đã có `proposition_prf()`) | CPU, hoặc LLM tách mệnh đề | **Theo P/R nên công bằng với độ dài** | Rất hợp ("SPICE-vi") |
| DCScore / DeCapBench | 2503.07906 · ICLR'25 · MAGAer13/DeCapBench ✓ | Tách caption thành primitive information units, chấm từng đơn vị: hallucination (P) và comprehensiveness (R) | Cần ref chi tiết | Port bằng LLM tách đơn vị tiếng Việt | ~1 GPU-h với LLM 7B | **Công bằng với độ dài theo thiết kế** | Rất hợp |
| CompreCap | 2412.08614 · CVPR'25 · LuFan31/CompreCap ✓ | Scene graph có hướng trên 560 ảnh COCO: độ phủ đối tượng, độ đúng thuộc tính, quan hệ | Không | Ảnh COCO, annotation tiếng Anh | Nhẹ | Theo coverage | Tùy chọn cho COCO-en |
| DOCCI / DCI | 2404.19753 · ECCV'24; 2312.08578 · CVPR'24 | Dataset caption dài (DOCCI TB 136 từ, DCI > 1000 từ); dùng làm ref dài | — | Tiếng Anh | — | — | Chỉ là nguồn ref dài, không phải metric |
| DSG / TIFA | 2310.18235 · ICLR'24 · j-min/DSG ✓; 2303.11897 · ICCV'23 · Yushi-Hu/tifa ✓ | Sinh câu hỏi từ văn bản rồi VQA trên ảnh (gốc là text-to-image) | Có | Đảo chiều cho captioning: hỏi VLM về từng mệnh đề của caption = precision có grounding | ~1 GPU-h | Đo precision nên không thưởng độ dài | Hợp như "VQA-precision" |
| "When More Words Say Less" | 2601.04609 · arXiv'26 | Người chấm thích caption **cụ thể** hơn caption dài; specificity ≠ length | — | — | — | Lý do lý thuyết cho cách trình bày ở §3 | Nên trích dẫn |

Bối cảnh tiếng Việt:
- UIT-ViIC (2002.00175) dùng BLEU/ROUGE/CIDEr. KTVIC (2401.08100) dùng BLEU/METEOR/ROUGE/CIDEr. VieCap4H (VLSP 2021; 2209.01304) chỉ dùng BLEU. UIT-OpenViIC (2305.04166) dùng n-gram.
- **Không tìm thấy bài captioning tiếng Việt nào dùng CLIPScore, BERTScore hay LLM-judge, và cũng không có nghiên cứu tương quan metric–người cho tiếng Việt.** Đây vừa là khoảng trống, vừa là điểm có thể nhận làm đóng góp phụ.
- LLM tiếng Việt: Vistral-7B-Chat chỉ có model card, **không có bài công bố (UNVERIFIED)**. VinaLLaMA (2312.11011) và PhoGPT (2311.02945) chỉ có văn bản, không có thị giác.
- Doğruöz et al. (2607.02235, Findings EMNLP'26) cảnh báo LLM-judge cho ngôn ngữ ít tài nguyên thường bị tin quá mức và hiếm khi được kiểm với người. Pearl (2512.21582) chỉ ra LLM-metric **ưu ái caption do chính nó sinh**. Vì vậy **không dùng Qwen2.5-VL làm judge cho Qwen2.5-VL**.

## 2. Danh sách áp dụng (xếp hạng)

Tổng chi phí GPU dưới 4 GPU-h trên một 3090. Mọi metric được chấm cho P1, zero-shot, VSPS, fuse2 (×3 seed), ở cả short và detailed. Mọi cặp "X so với P1" có paired bootstrap (`score_ci.py`, B = 5000).

**1. Báo cáo n-gram có xét độ dài (CPU, 0 GPU-h).**
- Bảng nào cũng có thêm cột *độ dài TB (từ sau RDRSegmenter)*.
- CIDEr-D chuẩn vẫn là số chính thức. Thêm một hàng chẩn đoán: CIDEr với σ = ∞ (tắt Gaussian length penalty, giữ nguyên TF-IDF và clipping), ghi rõ là "không chuẩn, chỉ để chẩn đoán".
- KTVIC: so n-gram **ở chế độ short** (độ dài khớp nhau), vì đây là phép so công bằng duy nhất cho n-gram.
- Sửa METEOR cho detailed (lỗi pipe JVM, xem Q1_GAP §1a) hoặc ghi rõ là bỏ.

**2. Multilingual CLIPScore + RefCLIPScore (~0.2 GPU-h cho cả KTVIC lẫn COCO 5k).**
- Mô hình: `open_clip` `xlm-roberta-large-ViT-H-14` / `frozen_laion5b_s13b_b90k` (MLAION của Gomes et al. 2025). **Dùng cùng một mô hình cho vi và en** để hai bảng so được với nhau.
- Công thức: w = 2.5, CLIP-S = w·max(cos, 0). RefCLIP-S = trung bình điều hòa của CLIP-S và max cos với 5 ref.
- Với detailed, báo thêm **CLIP-S theo câu**: tách câu, lấy min và mean. Vì chỉ khoảng 20 token đầu là có hiệu lực (Long-CLIP), nên đây là proxy precision từng mệnh đề.
- Robustness: jina-clip-v2 (8192 token). Phải kiểm có vi trước khi báo.
- COCO-en: thêm CLIP ViT-B/32 gốc để so được với tài liệu.
- Kiểm định: Kendall τ_c giữa metric và human eval của repo (hiện có 50 ảnh × 2 người; nên mở rộng lên 200 × 3 theo Q1_GAP). Bước này **bắt buộc**, vì Gomes et al. không có human judgment tiếng Việt.

**3. Proposition P/R/F1 kiểu CAPTURE/DCScore, gọi là "SPICE-vi" (CPU; tùy chọn ~1 GPU-h nếu dùng LLM tách mệnh đề).**
- Dùng `rescap/svp` + `metrics_svp.proposition_prf()`.
- Ref = hợp mệnh đề của 5 tham chiếu. Báo P (đúng / tổng mệnh đề sinh ra), R (độ phủ ref), F1, tách theo loại đối tượng / thuộc tính / quan hệ, như CAPTURE.
- Đây là metric **chính** để chứng minh "dài hơn nhưng vẫn đúng".
- Lưu ý ref thiếu: P chỉ là **cận dưới**, vì chi tiết đúng mà ref không nhắc sẽ bị tính sai. Phải kèm số silver/union đã có (commit 9973c8f) hoặc gold E6.
- COCO-en: chạy song song CAPTURE gốc (pip) để đối chiếu cách port.

**4. VLM-as-judge pairwise kiểu CapArena, rubric kiểm soát độ dài (~1–2 GPU-h).**
- Judge: một VLM mở **khác họ Qwen**, vừa 3090 ở bf16 hoặc 4-bit. Chọn mô hình cụ thể sau khi kiểm thử đọc–viết tiếng Việt trên 30 ảnh (UNVERIFIED, chưa chọn).
- Tùy chọn: 1 judge API (GPT-4o hoặc Gemini) trên một tập con, ghi rõ là ngoài 3090.
- Giao thức:
  - So từng cặp (X, P1) trên 558 ảnh, **chấm cả hai thứ tự**, chỉ tính hòa khi hai lượt mâu thuẫn.
  - Rubric tách 3 tiêu chí: *đúng* (không bịa), *đầy đủ*, *trôi chảy*. Có câu lệnh "không thưởng độ dài; chi tiết sai bị trừ nặng hơn chi tiết thiếu".
  - Báo win/tie/loss kèm CI.
  - Calibrate với human (τ, % đồng ý) trên tập human eval.
- COCO-en: thêm CapArena-Auto (600 ảnh, ~4 USD) nếu có ngân sách API. Đây là benchmark caption chi tiết được dùng nhiều nhất năm 2025–26.

**5. BERTScore (~0.05 GPU-h).**
- `bert_score` với `model_type="xlm-roberta-large"` (layer 17, multi-ref lấy max). **Báo P, R, F riêng.** Không có baseline-rescale cho vi → báo số thô, hoặc tự rescale bằng cặp câu ngẫu nhiên từ KTVIC train.
- Kiểm độ nhạy: PhoBERT-large trên input đã qua RDRSegmenter (nhất quán với n-gram).

**6. Chỉ cho COCO-en: PAC-S++ và Polos (~0.3 GPU-h); tùy chọn VELA cho detailed.**
- Đây là các metric reviewer COCO 2024–26 hay hỏi.
- Không port sang vi, vì cả ba đều train trên human judgment tiếng Anh. Ghi điều này thành hạn chế.

Không chọn:
- FLEUR, VisCE²: LLaVA-1.5 yếu tiếng Việt.
- HICE-S, BRIDGE, InfoMetIC, DENEB, Pearl: chỉ tiếng Anh, và đã trùng vai trò với mục 6.
- CompreCap: tùy chọn cho COCO.
- MoverScore: trùng vai trò BERTScore.
- ViCLIP-OT: chưa có weights.

## 3. Cách trình bày so sánh công bằng theo độ dài

1. **Hai chế độ, hai câu hỏi.**
   - *Short* (độ dài khớp ref): n-gram + CLIP-S + BERTScore-F, so ngang với P1. Ở đây fuse2 ≈ P1 về CIDEr và hơn về object R.
   - *Detailed*: không dùng CIDEr làm tiêu chí xếp hạng. Xếp theo proposition P/R, object P/R, CLIP-S theo câu và judge pairwise.
   - Viết rõ trong bài: CIDEr-D có Gaussian penalty σ = 6, nên caption dài gấp đôi bị nhân khoảng 0.2. Kèm số chẩn đoán từ §0.
2. **Luôn báo cặp precision và coverage**: object P/R, proposition P/R, BERTScore P/R, CHAIR cạnh Recall. Không báo F1 hay precision đứng một mình (đúng nguyên tắc 3 trong `metrics_svp.py`).
3. **Hình Pareto**: trục x là coverage (proposition R), trục y là precision (proposition P hoặc 1 − CHAIR_i). Mỗi hệ thống là một điểm, kích thước điểm theo độ dài. Một đường "P1 bị cắt hoặc nối dài" làm tham chiếu.
4. **Đối chứng khớp độ dài**:
   - (a) Cắt caption detailed còn k từ đầu, với k = 12 hoặc bằng độ dài ref, rồi chấm lại toàn bộ metric.
   - (b) Chia bin theo độ dài, hoặc hồi quy metric ~ hệ thống + độ dài, rồi báo hệ số hệ thống.
   - Nếu fuse2 vẫn hơn P1 về R ở cùng k, thì lợi thế không đến từ độ dài. Lập luận này dựa trên 2601.04609: specificity ≠ length.
5. **Neo vào người**: báo Kendall τ của từng metric với human eval tiếng Việt. Đây là phân tích tương quan metric–người đầu tiên cho captioning tiếng Việt, có thể nhận là đóng góp phụ.
