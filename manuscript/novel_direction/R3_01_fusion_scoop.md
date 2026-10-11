# R3-01: Scoop check cho consensus selection + reference fusion

**Tóm tắt (5 dòng)**
1. (a) consensus selection: **PARTIAL, gần SCOOPED**. Nagasawa et al. (MAI Workshop 2021) đã chấm điểm mỗi reference bằng độ tương đồng trung bình với các reference còn lại, rồi sample theo điểm đó. Phần còn mới chỉ là đo agreement ở mức object và áp dụng cho MLLM.
2. (b) reference fusion: **PARTIAL, phần lõi còn OPEN**. Đã có LLM-fusion (FuseCap, Bianco/Celona, IC3, CapsFusion), nhưng nguồn fuse là caption do model sinh hoặc output của vision expert. Chưa thấy bài nào train trên target ghép thuần từ caption người, chọn greedy theo số object mới.
3. Framing (partial label / mentionability): **PARTIAL**. Berg 2012 và Misra 2016 đã tách mention khỏi presence; CHAIR đã lấy union 5 reference làm ground truth. Phần mới chỉ là dùng framing này để giải thích precision drop của target fuse.
4. Claim sống sót: target ghép chỉ từ human mention tăng object recall/F1 trên KTVIC tiếng Việt. Claim này cần ablation đối chứng với VBCS và LLM-fusion, cùng bằng chứng presence cho phần precision bị mất.
5. Không claim "đầu tiên chọn reference theo consensus" hay "đầu tiên fuse caption làm target chi tiết".

---

## 1. Prior work đã kiểm tra

| # | Công trình | Venue/năm, link | Trùng | Không trùng |
|---|---|---|---|---|
| P1 | Nagasawa, Watanabe, Iyatomi: *Validity-Based Sampling and Smoothing for Multiple Reference Image Captioning* | MAI Workshop 2021, https://aclanthology.org/2021.maiworkshop-1.6 | **(a) gần trực tiếp.** Mình đã đọc PDF: VBCS (Eq.1–2) tính s_j = trung bình f_metric(ref_j, ref_k) với k≠j (BLEU, ROUGE-L hoặc CIDEr), lấy softmax rồi sample mỗi epoch, "prioritize captions that have a high degree of similarity to other reference captions". | Agreement đo bằng n-gram, không theo object. Soft sampling, không phải argmax. Model Up-Down trên MSCOCO, không phải MLLM hay tiếng Việt. Không có phân tích object P/R. |
| P2 | Devlin et al.: *Exploring Nearest Neighbor Approaches for Image Captioning* | arXiv 2015, https://arxiv.org/abs/1505.04467 | Chọn caption "consensus" có BLEU/CIDEr trung bình cao nhất so với các caption khác. | Chọn lúc inference, trên caption của ảnh láng giềng. |
| P3 | Zheng, Ma, Huang: *Multi-Reference Training with Pseudo-References* | EMNLP 2018, https://arxiv.org/abs/1808.09564 | Gộp các human reference thành lattice rồi sinh pseudo-reference để train; có thí nghiệm captioning. | Pseudo-ref là paraphrase, không nhằm làm union nội dung hay tăng độ phủ object. |
| P4 | Rotstein et al.: **FuseCap** | WACV 2024, https://arxiv.org/abs/2305.17718 | LLM fuse caption gốc với output detector/attribute/OCR, train BLIP trên 12M cặp. | Chi tiết thêm vào đến từ **vision expert**, có thể là nội dung không do người viết. Không fuse nhiều caption người. |
| P5 | Bianco, Celona et al.: *Improving Image Captioning Descriptiveness by Ranking and LLM-based Fusion* | Neural Comput. & Appl. 37(32), 2025, https://arxiv.org/abs/2306.11593 | Xếp hạng bằng BLIPScore, LLM fuse **top-2**, train captioner trên caption fuse làm GT. Đây là cấu trúc gần (b) nhất. | Caption được fuse là **caption do model sinh**. Tiêu chí chọn là alignment, không phải số object mới. Số liệu train-on-fused chưa kiểm chứng (UNVERIFIED). |
| P6 | Chan et al.: **IC3**, *Image Captioning by Committee Consensus* | EMNLP 2023, https://aclanthology.org/2023.emnlp-main.556 | Lập luận rằng train theo một reference "tốt nhất" sinh caption nghèo thông tin; dùng LLM tổng hợp nhiều "viewpoint" để tăng recall. | Committee là các sample của model, tổng hợp lúc inference. |
| P7 | Yu et al.: **CapsFusion** | CVPR 2024 (venue UNVERIFIED), https://github.com/baaivision/capsfusion | LLM fuse caption raw và caption synthetic. | Không phải caption người; mục tiêu là pretraining. |
| P8 | Chen et al.: *What Makes for Good Image Captions?* | Findings EMNLP 2025, https://arxiv.org/abs/2405.00485 | Baseline "human detailed caption" = **nối 5 caption COCO**. | Chỉ là baseline đánh giá VQA, không phải SFT target, không chọn greedy. |
| P9 | Shen et al.: **Chain-of-Talkers** | arXiv 2025 (EMNLP 2025 UNVERIFIED), https://arxiv.org/abs/2505.22627 | Annotator sau chỉ ghi phần "residual" còn thiếu, giống tiêu chí "thêm object mới". | Đây là giao thức thu thập, không phải fuse các caption có sẵn. |
| P10 | DOCCI (ECCV 2024), ImageInWords (2024), DCI, ShareGPT4V | https://arxiv.org/abs/2404.19753 ; https://arxiv.org/abs/2405.02793 ; DCI/ShareGPT4V UNVERIFIED | Dense caption dùng cho SFT. | Mỗi ảnh một người viết dài, hoặc người sửa bản nháp của model, hoặc caption do GPT-4V sinh. Không bài nào fuse nhiều caption ngắn độc lập. |
| P11 | Berg et al.: *Understanding and Predicting Importance in Images* | CVPR 2012, https://mlanthology.org/cvpr/2012/berg2012cvpr-understanding | Importance = xác suất một object được người mô tả nhắc tới; có mô hình dự đoán cái gì sẽ được mention. Đây chính là "mentionability". | Không bàn tới training target. |
| P12 | Misra et al.: *Seeing through the Human Reporting Bias* | CVPR 2016, https://arxiv.org/abs/1512.06974 | **Framing:** tách P(present) khỏi P(mentioned \| present). | Dùng cho classifier hai head, không tạo target bằng fusion. |
| P13 | Rohrbach et al.: **CHAIR** | EMNLP 2018, https://arxiv.org/abs/1809.02156 | Ground truth object = segmentation ∪ object trích từ 5 caption người. | Chỉ dùng để đánh giá. |

Phụ:
- Yun et al. (CVPR 2013, https://openaccess.thecvf.com/content_cvpr_2013/html/Yun_Studying_Relationships_between_2013_CVPR_paper.html) nghiên cứu quan hệ giữa gaze, description và detector.
- Anderson et al. (NeurIPS 2018, https://arxiv.org/abs/1806.06004) dùng chữ "partial" theo nghĩa khác: chuỗi caption bị thiếu, không phải annotator bỏ sót object.
- Không tìm thấy bài nào dùng chính thuật ngữ "mentionability".

## 2. Verdict

### (a) Consensus selection: PARTIAL (rủi ro cao)
- P1 đã có đúng cơ chế cho captioning training.
- Phần còn lại là một **variant**: agreement theo object (có hypernym) thay vì CIDEr, hard selection, MLLM QLoRA tiếng Việt, cùng phân tích P/R. Số offline của mình: P 71.1/R 56.6 so với 71.8/52.5 của first caption.
- **Bắt buộc** cite P1 và chạy baseline VBCS (CIDEr-similarity) trên KTVIC. Nếu không thắng VBCS thì (a) chỉ còn là chi tiết engineering.

### (b) Reference fusion: PARTIAL (lõi OPEN)
- Sau khoảng 14 truy vấn có định hướng (chưa phải systematic review), mình không thấy bài nào có SFT target **chỉ gồm caption người**, ghép greedy theo số object mới và đánh giá bằng held-out reference.
- Khác biệt bảo vệ được: P4/P5 có thể đưa nội dung không do người viết vào target, còn fusion của mình thì không.
- Reviewer sẽ hỏi hai câu: "Khác gì P8 cộng thêm heuristic?" và "Sao không LLM-fuse như P5?". Cần ablation: concat-5, concat-2 ngẫu nhiên, greedy-2, và LLM-fuse 2 caption người. Tất cả đo bằng held-out reference và CHAIR-vi.

### Framing: PARTIAL
- Lý thuyết nền đã thuộc về P11/P12, và P13 đã dùng union reference làm ground truth.
- Phần mới là dùng framing để giải thích precision drop. Muốn claim cần **bằng chứng presence**: một tập con có người gắn nhãn (ví dụ data/object_gold) cho thấy phần precision bị mất chủ yếu là object có thật. Nếu thiếu bằng chứng này, reviewer sẽ coi là "rationalizing hallucination".
- Nên dùng lại mô hình P(present)·P(mention|present) của P12 thay vì đặt khái niệm mới.

## 3. Claim nên viết

> "Trên KTVIC, khi chỉ dùng caption người, (i) chọn reference theo object-level agreement (biến thể của validity-based sampling [Nagasawa 2021]) và (ii) ghép greedy hai reference theo số object mới làm detailed target giúp tăng object F1 so với held-out reference (67.9 so với 60.7 offline). Khác LLM/expert fusion [FuseCap; Bianco/Celona 2025], target không chứa nội dung do model sinh. Phần precision bị giảm phù hợp với reporting bias [Berg 2012; Misra 2016] và được kiểm chứng trên một tập con có nhãn presence."

Tránh: "first", "we introduce mentionability", "hallucination-free by construction". "By construction" chỉ đúng với target, không đúng với output của model.

## 4. Việc tiếp theo
1. Đọc full text P5 (Springer) để lấy số liệu so sánh.
2. Thêm baseline VBCS và LLM-fuse-2-human vào bảng.
3. Kiểm chứng P7, P10 (DCI, ShareGPT4V) và CIDEr (Vedantam, CVPR 2015, chưa mở link) trước khi cite.
4. Chạy systematic search 2024–2026 (Semantic Scholar/ACL Anthology) để chắc chắn hơn về độ mới.
