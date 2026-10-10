# 07. Scene Graph Generation (SGG) 2025-2026 làm front-end cho hệ KG-captioning tiếng Việt

Ngày quét: 2026-10-10. Agent KG-plan 07. Nguồn: trang abs/HTML của arXiv (mở trực tiếp từng ID), trang tìm kiếm arXiv (`ti:"scene graph generation"`, sắp theo ngày, 137 kết quả mới nhất), model card Hugging Face, README GitHub. arXiv API, Semantic Scholar và OpenAlex trả 429 trong phiên này (nhiều agent chạy song song), nên venue chủ yếu lấy theo trường *Comments* của arXiv. Số liệu trong bảng là số **tác giả báo cáo**, được trích từ trang HTML. Dòng nào ghi "ước tính" là ước tính của agent này, **chưa đo**.

**Trả lời ngắn**
1. Chạy được trên một RTX 3090 cho khoảng 20k ảnh: **REACT/REACT++** (closed-vocab, khoảng 20-30 ms/ảnh, MIT, có ONNX), **EGTR** (khoảng 15 FPS), **R1-SGG-7B** (MLLM, Qwen2-VL-7B, Apache-2.0, ước tính 3-110 giờ tùy cách serve). **DSFlash** (CVPR 2026) chạy 18-50 ms/ảnh trên chính RTX 3090 nhưng bản HTML ghi là code "sẽ công bố khi được nhận", nên chưa chắc đã có.
2. Đồ thị dự đoán **rất nhiễu và rất thiếu**. SGG chuyên dụng tốt nhất trên VG150 chỉ đạt R@50 khoảng 30 và mR@50 khoảng 8-16. LVLM zero-shot gần như vô dụng theo giao thức VG150: Qwen2-VL-7B có tỉ lệ lỗi định dạng 54,5% và Recall 0,69%. Muốn phủ được 75-80% bộ ba đúng thì phải giữ khoảng 800-970 bộ ba ứng viên mỗi ảnh.
3. **Kiểm chứng ba trạng thái kiểu VSPS** khớp đúng vào chỗ yếu đó: tạo nhiều ứng viên (recall cao) → kiểm chứng từng bộ ba → SUPPORTED giữ, UNCERTAIN *làm thô* (predicate/hypernym), REJECTED bỏ và cắt cạnh phụ thuộc. Đã có bài làm "lọc đồ thị dự đoán bằng VLM/VQA" (PRISM-0, CP-SGG CVPR 2025, commonsense refinement 2026), nên **không được nói là ý tưởng lọc mới**. Phần mới là ba trạng thái, trung tính hóa thay cho xóa, dùng đồ thị làm giám sát SFT cho caption, và tiếng Việt.

---

## 1. Bản đồ SGG 2025-2026 (đã mở từng bài)

Ký hiệu cột "Chạy 3090?": ✅ chắc chắn (có code/weights, kích thước nhỏ), 🟡 được nhưng cần đo, ❓ chưa có code.

### 1.1 SGG transformer một giai đoạn và thời gian thực (closed-vocab VG150/PSG)
| Bài | Venue | Số liệu chính (tác giả báo cáo) | Chi phí | Chạy 3090? |
|---|---|---|---|---|
| EGTR (Im et al.), 2404.02072. *Nền 2024, dùng làm mốc.* | CVPR 2024 | VG150 SGDet: R@20/50/100 = 23,5/30,2/34,3; mR = 5,5/7,9/10,1; AP50 30,8. RelTR: R@50 27,5, mR@50 10,8. SGTR: R@50 24,6, mR@50 12,0 | 42,5M tham số, 14,7 FPS trên 1×V100; train 8×V100 | ✅ (github naver-ai/egtr) |
| Hydra-SGG (M. Chen et al.), 2409.10262 | ICLR 2025 | VG150 mR@50 = 16,0 (abstract) | không ghi | 🟡 |
| UniQ, 2501.05687 | arXiv (chưa venue) | chưa trích số | không ghi | 🟡 |
| REACT (Neau et al.), 2405.16116 | BMVC 2025 | PSG: R@20/50/100 = 27,6/30,9/32,3; mR = 18,3/20,1/20,9; mAP50 53,1. VG150 (trung bình K=50,100): R 27,4, mR 12,9. Cùng bảng PSG: EGTR R@50 30,3 / mR@50 14,5, 78 ms | **32,5 ms (23 ms với DCS) trên RTX 3080 Laptop 16 GB**, 43,3M tham số, detector YOLOv8m | ✅ (MIT, SGG-Benchmark, ONNX) |
| REACT++ (Neau, Falomir), 2603.06386 | arXiv 2026 | abstract: nhanh hơn REACT 20%, độ chính xác quan hệ trung bình +10% | README: khoảng 55 FPS bản ONNX, 13,4 ms (không ghi GPU) | ✅ |
| **DSFlash** (Lorenz et al.), 2603.10538 | **CVPR 2026** | PSG SGDet mR@50: DSFlash-L 30,9 / B 28,5 / S 25,05 (DSFormer 30,7 với 458 ms; HiLo-L 19,08; REACT 19,0). Tạo **đồ thị đầy đủ** (mọi cặp instance), không chỉ quan hệ nổi bật | **Đo trên RTX 3090**: S 18 ms, B 23 ms, L 50 ms; train dưới 24 giờ trên 1×GTX 1080 | ❓ (HTML ghi code công bố khi được nhận, chưa kiểm repo) |
| Salience-SGG, 2601.08728 | arXiv 2026 | abstract không ghi số | – | 🟡 |
| Dual-SGG, "Detector-Conditioned Reachability" (Qu et al.), 2607.06176 | ECCV 2026 | abstract: SGG dựa trên detector và SGG dựa trên query bổ sung cho nhau | – | 🟡 |
| Dependency-Aware Discrete Diffusion SGG 2605.09065; FlowSG 2604.18623 | arXiv 2026 | chỉ xác nhận tiêu đề qua listing | – | – |

### 1.2 SGG open-vocabulary (OVSGG)
| Bài | Venue | Số liệu | Chi phí | 3090? |
|---|---|---|---|---|
| OvSGTR (Z. Chen et al.), 2505.20106 (bản mở rộng của ECCV 2024 "Expanding Scene Graph Boundaries") | arXiv 2025 | VG150 SGDet, Swin-B: closed R@20/50/100 = 27,8/36,4/42,4 (37,6 R@50 khi có relation-aware pretrain); OvD R@50 21,35; OvR R@50 22,89 (27,92 với pretrain); OvD+R R@50 17,14 | train 8×A100; khởi tạo từ Grounding DINO | 🟡 (suy luận cỡ Grounding DINO, chưa đo) |
| RAHP, 2412.19021 | AAAI 2025 | – | – | 🟡 |
| INOVA, 2502.03856 → ACC 2511.05935 (L. Li et al.) | arXiv 2025 → **NeurIPS 2025** | abstract không ghi số; tách vật *có tương tác* và *không tương tác* cùng lớp | – | 🟡 |
| SPADE (X. Hu et al.), 2507.05798 | **ICCV 2025** | PSG closed R@50/mR@50 = 45,1/41,2; OvR 26,7/23,3; OvD+R 22,7/17,8 | diffusion backbone + Mask2Former Swin-B; train 4×A100 | 🟡 (dùng diffusion inversion, chậm) |
| Open-World SGG bằng VLM (Dutta et al.), 2506.08189 | CVPR 2025 Workshop (CVinW) | training-free; abstract không ghi số | – | 🟡 |
| PRISM-0 (Elskhawy et al.), 2504.00844 | arXiv 2025 (v2 11/2025; HTML trỏ tới "IJCV_Prism0.pdf", venue chưa xác minh) | zero-shot: lọc cặp → **VLM mô tả cặp → LLM sinh predicate → VQA kiểm chứng predicate**; abstract nói ngang mức weakly-supervised SOTA | – | 🟡 |
| Measuring Image-Relation Alignment (Neau et al.), 2509.01209 | arXiv 2025 | VLM zero-shot trên PSG: precision 14-31 (InternVL3-8B 30,97); đề xuất RelCLIPScore không cần tham chiếu; sinh dữ liệu tổng hợp từ khoảng 200K ảnh bằng LLaVA-OV-7B | VLM 7-8B | ✅ |
| ReLIC-SGG 2604.22546 | arXiv 2026 | **tác giả ghi "some errors in the experimental sections"**, không trích | – | – |
| CAGE-SGG 2604.22274 | arXiv 2026 | **đã rút bài (lỗi phương pháp)**, không trích | – | – |

### 1.3 SGG bằng LVLM (prompt / SFT / RL)
| Bài | Venue | Số liệu | Chi phí | 3090? |
|---|---|---|---|---|
| LLaVA-SpaceSGG, 2412.06322 | WACV 2025 | Recall +8,6%, mean Recall +28,4% so với baseline (abstract) | – | 🟡 |
| **R1-SGG** (Z. Chen, ..., Pollefeys, C. W. Chen), 2504.13617 | arXiv (chưa thấy venue) | VG150 SGDet: zero-shot Qwen2-VL-7B **lỗi 54,46%, Recall 0,69, mRecall 0,80**; +SFT lỗi 39,54, R 9,62; R1-SGG-7B lỗi 0,08, AP50 19,47, **R 23,75, mR 11,43** (MOTIFS 27,21/7,84; OvSGTR 26,74/5,83). PSG: R1-SGG-7B R 43,48 / mR 33,71 (PSGFormer 18,6/16,7) | SFT 4×A100-80G; GRPO 16×GH200 | ✅ suy luận (HF `JosephZ/R1-SGG-7B`, Apache-2.0, 8B BF16, vLLM/SGLang); ❌ huấn luyện lại RL |
| SGG-R³ (Feng et al.), 2603.07961 | arXiv 2026 | CoT-SFT + GSPO, MLLM tăng cường quan hệ; abstract không ghi số | – | 🟡 |
| SceneGraphVLM (Makarov et al.), 2605.13667 | arXiv 2026 | VLM nhỏ, định dạng TOON tiết kiệm token; RL với **phần thưởng nhận biết ảo giác** (phạt vật thể/quan hệ không có căn cứ), vì reward thuần recall khiến đồ thị phình ra; khoảng 1 s/đồ thị | VLM nhỏ | 🟡 |
| SaGe "Scene Graph Thinking" (Z. Yang et al.), 2607.05716 | **ICML 2026** | data engine biến cặp ảnh-văn bản thành đồ thị phân cấp, khoảng 120K mẫu, SFT + RFT với reward "node-as-proxy"; 8 benchmark | – | 🟡 |
| Universal SG (S. Wu, H. Fei, T.-S. Chua), 2503.15005 | CVPR 2025 | SG hợp nhất ảnh/văn bản/video/3D (USG-Par) | – | 🟡 |
| "A Closer Look at Dynamic SGG in the Era of MLLMs", 2503.15846 | arXiv | giao thức thuần recall gây đánh đổi precision-recall nặng và quan hệ thừa; đề xuất 5 metric mới (video) | – | – |

### 1.4 SGG panoptic (PSG)
- Nền (một dòng): PSG/PSGTR/PSGFormer (ECCV 2022), Pair-Net, HiLo (2023), OpenPSG (ECCV 2024, 2407.11213), "A Fair Ranking … for PSG" (2407.09216).
- 2025-2026: **SPADE** (ICCV 2025, open-vocab PSG), **DSFlash** (CVPR 2026, thời gian thực, đồ thị đầy đủ), **R1-SGG** (PSG R 43,5 / mR 33,7), 4D-PSG (CVPR 2025, 2503.15019, ngoài phạm vi), T-STAR (2607.21228, ảnh vệ tinh, ngoài phạm vi).
- Điểm đáng chú ý: trên PSG, mR@50 khoảng 30-41 cao hơn VG150 nhiều (khoảng 8-16), vì PSG có nhãn sạch hơn và dùng mask. Nếu cần front-end chất lượng tốt, PSG (133 lớp COCO-panoptic, 56 predicate) là lựa chọn gần với ảnh COCO của UIT-ViIC.

### 1.5 SGG yếu giám sát từ caption
- Nền: LLM4SGG (CVPR 2024, 2310.10404) dùng LLM trích bộ ba từ caption và căn với từ vựng đích.
- 2025-2026, mảng ảnh tĩnh **mỏng**: tìm trên arXiv (`weakly supervised scene graph`) chỉ ra INOVA/ACC (pretrain từ caption), OvSGTR (caption làm giám sát yếu), PRISM-0 (zero-shot). Phần còn lại là **video**: ICLR 2025 2502.15370 (NL supervision cho VidSGG), TRKT 2508.04943, Pair Affinity 2603.21559.
- Ý nghĩa cho UIT: caption tiếng Việt có sẵn (UIT-ViIC, KTVIC, UIT-OpenViIC) chính là nguồn giám sát yếu. Nhưng **chưa có parser tiếng Việt → bộ ba** (xem file 11 §3.2), nên đây là nút thắt chung với hướng ViSGParse.

### 1.6 Hậu xử lý / lọc đồ thị dự đoán (gần VSPS nhất)
| Bài | Venue | Cơ chế | Số liệu |
|---|---|---|---|
| **CP-SGG** (Nag et al.), 2503.13947 | **CVPR 2025** | Conformal prediction tạo *tập* đồ thị có bảo đảm phủ, sau đó **MLLM (BLIP-2 FLAN-T5-XL, 8-bit)** chọn bộ ba hợp lý | Muốn phủ bộ ba 75-80% thì tập phải có **816-972 bộ ba/ảnh**. Lọc bằng MLLM giảm hơn 50% (xuống 389-464) mà gần như không mất phủ. Không model nào đạt mức phủ mục tiêu. Chạy trên 4×RTX 3090 |
| PRISM-0, 2504.00844 | arXiv 2025 | VQA kiểm chứng từng predicate do LLM sinh | – |
| Visual Commonsense Refinements (Neau et al.), 2606.06369 | arXiv 2026 | Khai thác ràng buộc thường thức (không gian, chức năng) từ dữ liệu train, suy luận khai báo để **sửa và xếp hạng lại** dự đoán, không train lại | abstract không ghi số |
| SceneGraphVLM, 2605.13667 | arXiv 2026 | reward phạt nút/cạnh không có căn cứ | – |
| RelCheck, 2609.27890 (file 11, C3) | arXiv 2026 | Bộ ba RelTR + vị từ không gian từ bbox, làm "visual KB" để sửa caption | – |
| Reefknot, 2408.09429 | Findings ACL 2025 | benchmark ảo giác quan hệ, hơn 20K mẫu từ VG; giảm thiểu dựa trên confidence | ảo giác giảm trung bình 9,75% trên 3 bộ |

---

## 2. Quan hệ dự đoán nhiễu đến mức nào? (tổng hợp có số)

1. **Thiếu (recall thấp)**: VG150 SGDet R@50 khoảng 24-37 (EGTR 30,2; OvSGTR 36,4; R1-SGG-7B 23,75), mR@50 khoảng 8-16. Nghĩa là **phần lớn quan hệ có nhãn bị bỏ sót**, và predicate đuôi dài gần như không ra.
2. **Sai/không căn cứ (precision)**: VG chú thích thiếu ("a considerable amount of true relations unannotated"), predicate không loại trừ nhau ("talking to" và "beside" có thể cùng đúng), dữ liệu VG thô có nhiều nhãn nhiễu (2509.01209). Vì vậy precision tính theo VG **không đo được ảo giác thật**: precision của VLM trên PSG 14-31 là cận dưới bị nhiễu. Chính 2509.01209 kết luận precision là chỉ báo kém. Đây là lý do cần **người duyệt** trên ảnh UIT, chứ không thể tin số đo của VG.
3. **LVLM zero-shot**: Qwen2-VL-7B lỗi định dạng 54,5%, R 0,69 (R1-SGG). Một phần do lệch từ vựng VG150, không chỉ do ảo giác. Nhưng điều này cho thấy **không thể dùng thẳng "LVLM, hãy liệt kê scene graph" làm front-end** nếu không có SFT hoặc ràng buộc định dạng.
4. **Reward thuần recall làm đồ thị phình ra kèm ảo giác** (SceneGraphVLM 2605.13667; "Closer Look" 2503.15846). Điều này trùng với hiện tượng recall-precision của VSPS.
5. **Không gian/hướng**: VLM yếu với cặp chênh lệch kích thước, cặp xa nhau, và quan hệ có hướng hoặc đảo chiều (2509.01209; SPADE cũng nêu VLM yếu suy luận không gian).
6. **Detector giới hạn trần recall**: SGDet không thể vượt recall của detector. Dual-SGG (ECCV 2026) cho thấy SGG dựa trên detector và dựa trên query bổ sung cho nhau, nên **hợp nhất nhiều front-end** sẽ tăng phủ.

Hệ quả thiết kế: front-end nên **tối đa recall** (hợp nhiều nguồn, top-K rộng), còn **precision giao cho bước kiểm chứng**. Đây đúng là triết lý VSPS. Hướng này còn được CP-SGG đỡ lưng: phải giữ khoảng 800+ bộ ba/ảnh mới phủ được 75-80%.

---

## 3. Chạy được gì trên 1×RTX 3090 cho khoảng 20k ảnh (KTVIC + UIT-OpenViIC + UIT-ViIC)

| Front-end | Thời gian/ảnh | 20k ảnh | VRAM | Ghi chú |
|---|---|---|---|---|
| REACT / REACT++ (YOLO, ONNX) | 23-32,5 ms trên 3080 Laptop (tác giả báo cáo) | **khoảng 8-11 phút** (ước tính) | dưới 4 GB (ước tính) | Từ vựng VG150/PSG/IndoorVG. MIT. Lựa chọn mặc định |
| EGTR | khoảng 68 ms (14,7 FPS V100) | khoảng 25 phút (ước tính) | nhỏ (42,5M) | Có checkpoint VG150/OI-V6 |
| DSFlash-S/B/L | 18/23/50 ms **trên 3090** | 6-17 phút | không ghi | ❓ phải kiểm tra repo trước |
| OvSGTR Swin-B | chưa đo (cỡ Grounding DINO) | ước tính 1-3 giờ | ước tính 8-12 GB | Open-vocab, cho phép thêm nhãn mới |
| R1-SGG-7B (Qwen2-VL-7B, BF16 khoảng 16-17 GB) | ước tính 0,5-2 s (vLLM batch) đến 10-20 s (HF tuần tự), vì sinh vài trăm token | **ước tính 3-11 giờ (vLLM) / 55-110 giờ (HF)** | khoảng 18-22 GB BF16; 4-bit nếu thiếu | Open-ish, PSG mR 33,7. Phải đo thật trước khi cam kết |
| Bộ kiểm chứng VSPS (Vintern-1B/3B hoặc Qwen2.5-VL-7B 4-bit) | — | xem §4.3 | — | Đây mới là chi phí chính |

Huấn luyện: **không** tái lập được GRPO của R1-SGG (16×GH200) hay pretrain OvSGTR (8×A100). Trên 3090 chỉ nên (a) suy luận các checkpoint công khai; (b) fine-tune nhẹ REACT/EGTR (cỡ 40M tham số) hoặc LoRA một VLM nhỏ cho SGG trên tập UIT người duyệt (vài trăm đến vài nghìn ảnh), nếu thật sự cần.

Lệch miền tiếng Việt: từ vựng VG150 (150 vật, 50 predicate) và PSG (133/56) đều là tiếng Anh, và thiếu các khái niệm đặc thù Việt (nón lá, áo dài, gánh hàng). Cách làm: ánh xạ EN→VI cho khoảng 200-250 nhãn (thủ công, khoảng 1 ngày); dùng R1-SGG/OvSGTR hoặc caption tiếng Việt (giám sát yếu) để bù khái niệm ngoài từ vựng.

---

## 4. Làm sạch đồ thị dự đoán bằng kiểm chứng ba trạng thái kiểu VSPS (đề xuất "VG-Clean")

### 4.1 Pipeline
1. **Tạo ứng viên, ưu tiên recall**: hợp các nguồn REACT++ (top-100 bộ ba), R1-SGG-7B (đồ thị JSON) và mệnh đề tách từ caption tiếng Việt có sẵn của UIT. Gộp nút qua IoU bbox và đồng nghĩa nhãn.
2. **Chuyển bộ ba thành mệnh đề có kiểu của VSPS**: nút → `entity`/`count`, thuộc tính → `attribute`, cạnh → `relation`/`action`. Render thành câu hỏi có/không tiếng Việt kèm vùng ảnh (crop hợp subject∪object, hoặc vẽ bbox).
3. **Kiểm chứng**: verifier VLM trả P(có). Hai nguồn bằng chứng độc lập (giống RelCheck): (a) VLM, (b) **hình học** (vị từ không gian tính từ bbox/mask: trên/dưới/bên cạnh/trong) và điểm của detector. Sau đó:
   - **SUPPORTED**: VLM đồng ý và hình học không mâu thuẫn → giữ.
   - **UNCERTAIN**: VLM dao động (phương sai qua K mẫu, hoặc P(có) ở vùng giữa), hoặc VLM và hình học bất đồng → **trung tính hóa**: làm thô predicate theo phân cấp ("riding" → "on" → "near"/"ở cạnh"; "đứng trên" → "ở trên"), hypernym cho nút ("chó" → "con vật"). Không xóa.
   - **REJECTED** → bỏ.
4. **Phụ thuộc kiểu DSG**: nút REJECTED thì tự động bỏ mọi cạnh và thuộc tính gắn với nó, không cần gọi verifier cho con. Cạnh chỉ kiểm khi cả hai đầu ≥ UNCERTAIN.
5. **Hiệu chỉnh ngưỡng bằng conformal** trên khoảng 300 ảnh người duyệt (mượn cách làm của CP-SGG), để báo được mức phủ hoặc mức sai mục tiêu thay vì ngưỡng tùy chọn.
6. **Đầu ra**: "verified Vietnamese scene graph" cho mỗi ảnh. Dùng cho (i) render caption chi tiết làm dữ liệu SFT (VSPS hiện tại), (ii) metric graph-recall (file 11, ý 1), (iii) benchmark ảo giác quan hệ tiếng Việt.

### 4.2 Thí nghiệm cần có (để không bị nói "chỉ là lọc")
- So sánh 4 chế độ: front-end thô / lọc nhị phân (giống PRISM-0, CP-SGG) / ba trạng thái + xóa UNCERTAIN / **ba trạng thái + trung tính hóa**. Báo graph precision và recall trên 300-500 ảnh người duyệt, kèm CHAIR và recall trên caption SFT sinh ra.
- Ablation nguồn bằng chứng: chỉ VLM / chỉ hình học / cả hai.
- Ablation phụ thuộc DSG: số lời gọi verifier tiết kiệm được so với độ chính xác mất đi.
- Baseline bắt buộc: CP-SGG (CVPR 2025), PRISM-0, commonsense refinement (2606.06369) nếu có code, và reward nhận biết ảo giác kiểu SceneGraphVLM nếu có code.

### 4.3 Chi phí kiểm chứng (ước tính, phải đo)
- Giả sử khoảng 30 bộ ba sau gộp mỗi ảnh. Thêm khoảng 15 nút thì khoảng 45 truy vấn/ảnh, nhân 20k ảnh là **khoảng 0,9 triệu truy vấn**. Nếu dùng **K=5 mẫu** như VSPS thì thành khoảng 4,5 triệu lượt sinh. Nặng với 7B.
- Giảm chi phí: (a) **một forward lấy logit P(có)/P(không)** thay cho K=5 mẫu (chậm hơn khoảng 5 lần nếu lấy mẫu); dùng phương sai hoặc entropy từ logit để xác định UNCERTAIN; (b) prefix caching ảnh (mã hóa ảnh 1 lần/ảnh); (c) phụ thuộc DSG (bỏ con của nút bị REJECTED); (d) dùng Vintern-1B để lọc thô, chỉ chuyển ca UNCERTAIN lên Qwen2.5-VL-7B.
- Ước tính với (a)+(b) trên Vintern-1B: khoảng 20-50 ms/truy vấn, tức **khoảng 5-13 giờ** cho 20k ảnh. Với Qwen2.5-VL-7B 4-bit cho khoảng 20% ca UNCERTAIN thì thêm khoảng 5-10 giờ. Tổng nằm trong một tuần GPU.

---

## 5. FEASIBILITY / OVERLAP / NOVELTY (chỉ xét 2025-2026)

**Feasibility: cao.** Front-end closed-vocab chạy vài phút cho 20k ảnh. R1-SGG-7B chạy được trong 24 GB. Phần tốn thật là (i) kiểm chứng (một tuần GPU, ước tính), (ii) **người duyệt 300-500 ảnh** để có tập vàng (trùng với tập vàng 300 ảnh VSPS đang làm, nên tái dùng được), (iii) ánh xạ nhãn EN→VI. Rủi ro: DSFlash chưa có code; R1-SGG chưa có venue; thông lượng R1-SGG trên 3090 chưa đo.

**Overlap: trung bình-cao với ý "lọc đồ thị dự đoán bằng VLM".**
- CP-SGG (CVPR 2025): MLLM chọn bộ ba trong tập conformal. Gần nhất về mặt hậu xử lý.
- PRISM-0 (2025): VQA kiểm chứng predicate. Gần nhất về mặt "verify từng quan hệ".
- Commonsense refinements (2026): sửa và xếp hạng dự đoán không cần train lại.
- SceneGraphVLM (2026), SaGe (ICML 2026): đưa ảo giác vào reward và dùng scene graph cho suy luận.
- RelCheck (2026): bộ ba RelTR + hình học dùng để sửa caption. Gần nhất về mặt "SG → caption trung thực".

**Novelty còn giữ được** (đã kiểm: không bài nào ở trên có):
1. **Ba trạng thái + trung tính hóa** (làm thô predicate/hypernym thay vì xóa), áp dụng cho **cạnh của scene graph**. Mọi bài lọc ở trên đều nhị phân (giữ/bỏ) hoặc xếp hạng lại.
2. Đồ thị đã kiểm chứng dùng làm **giám sát SFT cho captioning chi tiết** (không phải để báo SGG R@K).
3. **Tiếng Việt**: chưa có SG data, parser hay metric (file 11). Đây sẽ là verified SG đầu tiên trên ảnh UIT.
4. Bằng chứng kép VLM + hình học, có hiệu chỉnh conformal **cho ba trạng thái** (CP-SGG chỉ dùng cho tập dự đoán).

**Không được nói**: "đầu tiên dùng VLM để kiểm chứng scene graph dự đoán", "đầu tiên dùng SG để giảm ảo giác caption", "SGG bằng RL". Ba điều này đã có lần lượt ở CP-SGG/PRISM-0, RelCheck/Reefknot và R1-SGG.

**Khuyến nghị**: dùng REACT++ (closed-vocab, nhanh) kết hợp R1-SGG-7B (open-ish) làm front-end, cộng mệnh đề từ caption UIT. Bước kiểm chứng tái dùng verifier VSPS, chuyển từ K=5 mẫu sang logit để giảm 5 lần chi phí. Đóng khung bài theo hướng "verified Vietnamese scene graphs → faithful detailed captioning + graph metric", **không** theo hướng "SGG mới". Không nên tự train SGG mới trên 3090: không cạnh tranh được với DSFlash, SPADE hay R1-SGG, và không cần thiết cho mục tiêu caption.

---

## 6. Chưa xác minh / hạn chế
- Venue: R1-SGG (2504.13617), OvSGTR (2505.20106), SGG-R³, REACT++, Salience-SGG, PRISM-0 (HTML trỏ "IJCV_Prism0.pdf", có thể đang nộp IJCV) đều **chưa thấy venue**. ICCV 2025 của SPADE, NeurIPS 2025 của ACC, CVPR 2026 của DSFlash, ECCV 2026 của Dual-SGG và ICML 2026 của SaGe lấy theo trường Comments của arXiv, chưa đối chiếu proceedings (CVF trả 403, S2/OpenAlex trả 429).
- Bài ICCV 2025 "Vision-Language Interactive Relation Mining for OVSGG" (Min et al.) thấy trên CVF qua tìm kiếm, nhưng trang trả 403. Chưa mở được, chưa trích.
- Số của DSFlash, REACT và EGTR là số tác giả báo cáo trên GPU của họ. Thông lượng trên 3090 trong §3 (trừ DSFlash) và mọi chi phí kiểm chứng trong §4.3 là **ước tính của agent**.
- Chưa kiểm repo DSFlash có code hay chưa (tính đến 2026-10-10).
- Các bài chỉ xác nhận tiêu đề qua listing (UniQ, FlowSG, Discrete Diffusion SGG) chưa đọc abstract đầy đủ, nên không trích số.
- Tỉ lệ ảo giác quan hệ tuyệt đối của MLLM trên Reefknot không có trong abstract. Chỉ trích được mức giảm 9,75%.
