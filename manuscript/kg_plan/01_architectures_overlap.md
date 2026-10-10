# 01. Kiến trúc 2025-2026 kết hợp transformer/LVLM với KG hoặc scene graph cho captioning: ma trận trùng lặp và ô trống

Ngày quét: 2026-10-10. Agent KG-plan 01, góc: **kiến trúc**.
Nguồn đã dùng trong phiên: trang `arxiv.org/abs/<id>` (mở trực tiếp từng ID để lấy tác giả, ngày nộp, comment venue, abstract), Semantic Scholar Graph API (bulk search 2025-2026 và `paper/batch` để lấy venue/abstract), trang IJCAI proceedings, PDF gốc của hai bài Việt Nam (ACIIDS 2025, TNU JST 2025).
Hạn chế của phiên: arXiv export API và OpenAlex trả 429/hết budget giữa chừng, nên phần quét rộng chủ yếu đi qua Semantic Scholar (truy vấn ở mục 6). Bài nào chưa mở được trang gốc thì ghi ở mục 5 "Chưa xác minh".

**Kết luận ngắn:**
1. Ở tiếng Anh, gần như **mọi điểm bơm đồ thị đơn lẻ đều đã có người làm** trong 2025-2026: token đầu vào (AKGMA, PSGP, KG-ViP), cross-attention (LUX, các bài encoder-decoder cũ), giải mã (MMCD), phần thưởng RL (SC-Captioner, FoCUS, video structured reward), DPO hard negative (SceneAlign), hậu kiểm (RelCheck, multi-hop KG), RAG (MERGE, SEAR, ExpArt-KG, ArtRAG, MsRAG).
2. Các ô **còn trống thật** nằm ở *tổ hợp*: (a) đồ thị **mang trạng thái kiểm chứng** (không chỉ xác suất) dùng làm **dữ liệu/target huấn luyện** của captioner; (b) **KG ngoài làm nguồn hard negative cho verifier/DPO** của caption chi tiết; (c) **leo phân cấp IsA của KG để trung tính hóa** nút chưa chắc chắn; (d) **quy tắc phụ thuộc cha-con kiểu DSG** đưa vào **lúc sinh** hoặc **vào reward**; (e) mọi thứ trên cho **tiếng Việt**.
3. Phía Việt Nam: có 3 bài KG-captioning 2025 của nhóm Việt (ACIIDS 2025, Vietnam J. Sci. Technol. 2025, TNU JST 2025) nhưng **đều chạy trên COCO/Flickr30k/Visual Genome tiếng Anh**, kiến trúc CNN/Transformer cổ điển + ConceptNet. **Không có** bài nào trên UIT-ViIC/UIT-OpenViIC/KTVIC/ViTextCaps dùng KG hay scene graph.

---

## 1. Danh sách bài (đã mở trang gốc hoặc API)

Ký hiệu cột "Code": ✔ = link code/project xuất hiện trên trang arXiv/abstract; – = không thấy link trên trang đã mở (không có nghĩa là không có code).

### 1.1 Captioning ảnh / mô tả chi tiết (lõi)

| ID | Bài | Tác giả (đầu) | Venue, năm | Link | Phương pháp (1 dòng) | Dữ liệu | Metric | Code |
|---|---|---|---|---|---|---|---|---|
| P1 | Knowledge-Enhanced Image Captioning with Adaptive Graph-based Multimodal Alignment and LLM (AKGMA) | Guoyi Li, Die Hu, ... | AAAI 2026 | https://doi.org/10.1609/aaai.v40i18.38532 | EKA nối thực thể thị giác với KG cho một LM nhỏ; AKGC dùng **RL** dựng subgraph liên quan ảnh để tối ưu knowledge prompt; SCKA lấy tri thức ngữ cảnh từ **scene graph** bơm vào LLM | UniKnowCap (mới) + benchmark khác (abstract không liệt kê) | "multiple metrics", knowledge accuracy, detail consistency | – |
| P2 | MERGE: Multimodal Entity-aware RAG for News Image Captioning | Xiaoxing You, Qiang Huang, ... Jun Yu | AAAI 2026 (comment arXiv) | arXiv 2511.21002 | Dựng KB đa phương thức lấy thực thể làm trung tâm (văn bản + ảnh + **tri thức cấu trúc**), truy hồi động theo nội dung ảnh, chiến lược hypothesis-caption nhiều bước | GoodNews, NYTimes800k | CIDEr (+6,84/+1,16), NER F1 (+4,14/+2,64) | – (xem mục 5) |
| P3 | SEAR: Retrieval-Augmented Image Captioning via Synthesized Entity-Aware Knowledge Representations | Lin Shen, Chenxu Cui, ... Bo Li | CIKM 2025 | https://doi.org/10.1145/3746252.3761265 | Gom cụm ảnh, dùng mô hình lớn trích **KG** từ caption của cụm, **KG pruner** giữ subgraph liên quan ảnh truy vấn, đưa vào captioner nhẹ | MSCOCO, Flickr30k, NoCaps | caption metric chuẩn | – |
| P4 | MsRAG: Knowledge Augmented Image Captioning with Object-level Multi-source RAG | Yuming Qiao, Yuechen Wang, ... | IJCAI 2025 | https://doi.org/10.24963/ijcai.2025/678 | RAG mức đối tượng không cần câu hỏi (search engine + DB miền), chọn prompt theo tri thức truy hồi, visual prompting để căn tri thức với vật thể; **không phải KG** | (abstract không nêu) | định tính + định lượng | – |
| P5 | ExpArt-KG: Artwork Image Description Generation through Iterative Exploration of KGs | Yuta Kato, Shintaro Ozaki, ... Taro Watanabe | arXiv 2609.00629 (2026-09) | arXiv 2609.00629 | LVLM luân phiên sinh câu trả lời và **truy hồi KG**, dừng theo phán đoán đúng/sai; dựng KG nghệ thuật | ExpArt-KG (mới) | độ chi tiết, chi phí truy hồi | – |
| P6 | ArtRAG: RAG with Structured Context for Visual Art Understanding | Shuai Wang, ... Marcel Worring | ACM MM 2025 (theo S2) | arXiv 2505.06020 | Training-free: tự dựng **Art Context KG** rồi truy hồi subgraph làm ngữ cảnh cho MLLM mô tả tranh | (dataset nghệ thuật, chưa đọc) | – | – |
| P7 | VLCE: Knowledge-Enhanced Framework for Image Description in Disaster Assessment | Md. Mahfuzur Rahman, ... Roy George | ALVR@ACL 2026 (xem file 11); arXiv 2509.21609 | arXiv 2509.21609 | VLM sinh caption có điều kiện YOLOv8, rồi CNN-LSTM/Transformer tinh chỉnh bằng từ vựng 1.566 thuật ngữ trích từ **ConceptNet + WordNet** | xBD, RescueNet | CLIPScore, InfoMetIC, human pref | – |
| P8 | SC-Captioner: Improving Image Captioning with Self-Correction by RL | Lin Zhang, Xianfang Zeng, ... Tao Chen | ICCV 2025 | arXiv 2508.06125 | **Reward RL** từ phép trừ tập object/attribute/relation (parse **scene graph** văn bản) giữa caption đầu và caption tự sửa, đối chiếu tham chiếu | COCO, RefinedCaps (6,5K, mới) | metric cải tiến từ CAPTURE | – |
| P9 | FoCUS: Controllable Image Captioning with Prompt-Conditioned Scene Rewards | Jongyeop Hyun, Taeyoung Kim, Hyounghun Kim | EMNLP 2026 Main (comment arXiv) | arXiv 2609.00709 | Caption parse rồi căn với thành phần **scene graph**; trọng số theo yêu cầu (kể cả âm), tối ưu **GRPO**, kiểm chứng attribute/relation bằng suy luận | SCoPE (mới), 2 backbone VLM | coverage + suppression (Include/Avoid) | ✔ project page |
| P10 | PSGP: Probabilistic Scene Graph Prompting | Zichao Li | WACV 2026 Workshops | https://doi.org/10.1109/WACVW68408.2026.00183 | Mô hình SGG như **phân phối** trên đồ thị, mã hóa bất định vào **soft prompt token** điều kiện MLLM (VQA và captioning) | GQA, VSR, Ambiguous-GQA (mới) | accuracy, faithfulness, calibration | – |
| P11 | LUX: Lesion-Aware Graph-Conditioned VL Architecture for Explainable Endoscopic Captioning | A. I. Escamilla-Lopez, ... Sharib Ali | arXiv 2608.23853 (2026-08) | arXiv 2608.23853 | **Scene graph tổn thương** từ Grad-CAM/CBAM, embedding đồ thị đưa vào **cross-attention** của decoder T5 | nội soi viêm loét đại tràng | caption metric | – |
| P12 | K-DFIC: Enriched Image Captioning Based on Knowledge Divergence and Focus | An-An Liu, Quanhan Wu, Ning Xu, ... | IEEE TCSVT 2025 | https://doi.org/10.1109/TCSVT.2024.3525158 | Prompt **nhận biết scene graph** cho GPT-3.5 "phân kỳ" sinh tri thức, mạng tinh chỉnh lọc tri thức, hợp nhất với đặc trưng thị giác cho decoder | MSCOCO Karpathy | CIDEr-D 148,4 | – |
| P13 | RelCheck: Dual-Evidence Spatial Grounding for VLM Hallucination Correction | Siddhi Patil, Navrati Saxena, W. B. Andreopoulos | arXiv 2609.27890 (2026-08) | arXiv 2609.27890 | **Hậu kiểm** training-free: bộ ba **SG** (RelTR) + vị từ không gian từ box + claim kiểu Woodpecker thành "visual KB", LLM viết lại câu | MME (LLaVA v1 13B) | MME hallucination | – |
| P14 | Beyond Generation: Multi-Hop Reasoning for Factual Accuracy in VLMs | Shamima Hossain | NewInML@ICML 2025 (poster) | arXiv 2511.20531 | Nhận diện thực thể → duyệt **KG** nhiều bước → tinh chỉnh caption theo fact | tập tự dựng (sơ bộ) | factual accuracy (~+31%) | – |
| P15 | Image Captioning ... Multi-Step Cross-Attention ... External Commonsense Knowledge Augmentation | Liang Wang, Meiqing Jiao, ... | Electronics (MDPI) 2025 | https://doi.org/10.3390/electronics14163325 | CLIP-ViT + Faster R-CNN + BERT + GPT-2, cross-attention nhiều bước, bơm **commonsense ngoài** | (COCO, theo bối cảnh; chưa đọc full) | caption metric | – |
| P16 | Knowledge-Driven Image Captioning | A. Haque, Sayeed Ghani, Muhammad Saeed | IEEE Access 2025 | https://doi.org/10.1109/ACCESS.2025.3642465 | Capsule Network mã hóa ảnh + **KG** cho ngữ cảnh + Transformer decoder | – | – | – |
| P17 | KG-Augmented Image Captioning: Hybrid ViT-GAT | Subasish Mohapatra, ... | CSI AISP 2025 | https://doi.org/10.1109/AISP68263.2025.11396297 | ViT + embedding **ConceptNet** qua **GAT**, Transformer decoder | Flickr30k | BLEU-4 0,38, CIDEr 1,02 | – |
| P18 | MKG-CottonCapT6 | Chenzi Zhao, ... Shuai Yang | Applied Sciences 2026 | https://doi.org/10.3390/app16063029 | **MMKG** miền bệnh cây bông + CrossViT + T5 | dữ liệu bông (mới) | – | – |
| P19 | KARG-RSIC: Knowledge-Augmented Retrieval Generation for RS Image Captioning | Yan Zhang, Quan Zou, ... | IEEE JSTARS 2026 | https://doi.org/10.1109/JSTARS.2026.3684341 | Tri thức phi tham số truy hồi qua căn chỉnh manifold PCA + rerank đa dạng (không hẳn KG) | viễn thám | – | – |

### 1.2 Bài Việt Nam (KG + captioning, 2025)

| ID | Bài | Tác giả | Venue, năm | Link | Phương pháp | Dữ liệu | Ghi chú |
|---|---|---|---|---|---|---|---|
| V1 | Improving Efficiency Image Captioning by Using Attention Mechanism Combined with Knowledge Graph | Tam Khoi Tran, Nguyen Thi Uyen Nhi, Thanh Manh Le, Nguyen Thi Dinh (TDTU, DUE, Huế, HUIT) | ACIIDS 2025 (Springer CCIS/LNAI) | https://doi.org/10.1007/978-981-96-6005-6_6 | Nhận diện vật thể → dựng **KG** vật thể/quan hệ + **ConceptNet** → ghép caption | MS-COCO, Flickr30k | BLEU-1/4. **Caption tiếng Anh** (đã đọc PDF) |
| V2 | RGTranCNet: Effective image captioning model using cross-attention and semantic knowledge | Thinh Van Nguyen, Lang Van Tran, V. Thanh | Vietnam J. Sci. Technol. 2025 | https://doi.org/10.15625/2525-2518/22381 | Encoder dựng **relational graph** vùng vật thể, decoder Transformer **cross-attention** với tri thức **ConceptNet** | MS COCO | **Tiếng Anh** |
| V3 | An image captioning model integrating knowledge graphs and deep learning | Nguyen Do Thai Nguyen, Nguyen Van Tuan, ... (ĐH Sư phạm TP.HCM) | TNU J. Sci. Technol. 230(07), 2025 | https://jst.tnu.edu.vn/jst/article/view/12614 | Sinh **scene graph** từ ảnh, làm giàu bằng **KG ngoài**, rồi sinh caption | MSCOCO, Visual Genome | BLEU 41,3, METEOR 31,6. **Tiếng Anh** (đã đọc PDF) |
| V4 | Developing a Knowledge Graph for The Image Captioning Problem | Dinh Thi Nguyen, Tam Khoi Tran, T. M. Le | FAIR 2025 (Kỷ yếu Hội nghị Quốc gia lần thứ 18) | https://doi.org/10.15625/vap.2025.0297 | (chưa đọc được nội dung, xem mục 5) | ? | **Cùng hội nghị FAIR với VSPS** → reviewer FAIR có thể đã thấy |

Hệ quả: câu "first KG/SG captioning *by Vietnamese authors*" là **sai**. Câu đứng được là "first KG/SG captioning *on Vietnamese-language captions* (UIT-ViIC/OpenViIC/KTVIC)". Phải trích V1-V4 và chỉ rõ khác biệt: họ dùng CNN/Transformer cổ điển, dữ liệu tiếng Anh, chỉ BLEU/METEOR, không đo ảo giác.

### 1.3 Bài lân cận (không phải captioning ảnh tĩnh, nhưng chiếm cùng ô thiết kế)

| ID | Bài | Venue, năm | Link | Vai trò của đồ thị | Code |
|---|---|---|---|---|---|
| N1 | KG-ViP: fusing scene graphs + commonsense graphs for MLLM VQA (Zhiyang Li, Ao Ke, Yukun Cao, Xike Xie) | ACL 2026 theo S2 | arXiv 2601.11632 | SG + KG commonsense, truy hồi theo câu hỏi, hợp nhất thành ngữ cảnh văn bản cho MLLM | – |
| N2 | MMGraphRAG (Xueyao Wan, Hang Yu) | arXiv 2507.20804 | arXiv 2507.20804 | SG của ảnh + KG văn bản, liên kết thực thể xuyên phương thức, GraphRAG | – |
| N3 | MMCD in "Seeing Beyond Hallucinations: LLM-based Compositional Information Extraction" (Xinwei Li, Li Lin, Shuai Wang, Hanqian Wu) | SIGIR 2025 | https://doi.org/10.1145/3726302.3730081 | **Contrastive decoding** giữa SG gốc và SG nhiễu (che vật thể chính), training-free; thử trên What's Up, SeeTrue, SugarCrepe | – |
| N4 | SceneAlign (Chuhan Wang, ... Julian McAuley, Jingbo Shang) | arXiv 2601.05600 (preprint) | arXiv 2601.05600 | Nhiễu các nút SG quan trọng (4 chiến lược) để tạo **hard negative rationale** cho **DPO** | – |
| N5 | SaGe: Scene Graph Thinking (Zhiwei Yang, ... Shouhong Ding) | ICML 2026 | arXiv 2607.05716 | Data engine biến cặp ảnh-văn thành SG, 120K trace suy luận; SFT rồi RL với reward node-as-proxy | ✔ github.com/zwyang6/SaGe |
| N6 | Relation-R1 (Lin Li, Wei Chen, ... Long Chen) | AAAI 2026 (comment arXiv) | arXiv 2504.14642 | CoT nhận thức + SFT + GRPO cho hiểu quan hệ nhị phân/N-ary | – |
| N7 | VisKG: Question-Specific KGs for Efficient Visual Reasoning (Ting-Chih Chen, ... Filip Ilievski) | arXiv 2609.35942 (2026-09) | arXiv 2609.35942 | Mô hình học **dịch ảnh thành KG theo câu hỏi** thay cho caption chi tiết; SFT (negative rationale) + GDPO | – |
| N8 | Reinforcing Consistency in Video MLLMs with Structured Rewards (Yihao Quan, ... Ruixiang Tang) | COLM 2026 | arXiv 2604.01460 | **Reward scene graph** mức instance (object/attribute/relation) + reward thời gian + VQA tự kiểm | – |
| N9 | Fine-Grained Captioning of Long Videos through Scene Graph Consolidation (Sanghyeok Chu, Seonguk Seo, Bohyung Han) | ICML 2025 | arXiv 2502.16427 | Caption đoạn → parse SG → hợp nhất đồ thị → **graph-to-text decoder** nhẹ | – |
| N10 | ISGR: Seeing Beyond the Scene (Dayong Liang, ... Qing Li) | arXiv 2505.09118 | arXiv 2505.09118 | SG tương tác (SAM + caption nhận biết tương tác), truy vấn chức năng, RL bộ nhớ dài hạn | – (link "open_upon_acceptance") |
| N11 | Graph-of-Mark (Frisoni et al.) | AAAI 2026 | arXiv 2603.06663 | Vẽ **SG lên pixel** ảnh (visual prompt) cho suy luận không gian | – |
| N12 | CheXPO-v2 (Xiao Liang, ... Bin Jing) | arXiv 2512.17213 | arXiv 2512.17213 | **KG Consistency Reward**: parse bước suy luận thành bộ ba (Disease, Relation, Anatomy) cho GRPO/process supervision | ✔ github.com/ecoxial2007/CheX-Phi4MM |
| N13 | R2GenKG (Fu-Tian Wang, ... ) | arXiv 2508.03426 | arXiv 2508.03426 | MMKG y tế (M3KG) lấy mẫu đa mức, mã hóa R-GCN, đưa vào LLM sinh báo cáo X-quang | – |
| N14 | PoSh (Amith Ananthram, ... Mohit Bansal, Kathleen McKeown) | ICLR 2026 | arXiv 2510.19060 | SG làm **rubric** cho LLM-as-judge đánh giá mô tả chi tiết (thuộc góc metric, liệt kê để đánh dấu ô "verifier/eval") | ✔ github.com/amith-ananthram/posh |
| N15 | MUNIChus (Yujie Chen, ... Marcos Zampieri) | LREC 2026 | arXiv 2603.10613 | Benchmark news captioning 9 ngôn ngữ (ar, zh, en, fr, hi, id, ja, si, ur). **Không có tiếng Việt, không dùng KG** (đã kiểm bản HTML) | – |
| N16 | MMCOMET (E. Wang, ... Jie Yang) | arXiv 2603.01055 | arXiv 2603.01055 | Tài nguyên: ATOMIC2020 mở rộng sang ảnh, hơn 900K bộ ba; thử visual storytelling | – |

Nền trước 2025 (một dòng mỗi bài, chỉ để định vị): CCoT (CVPR 2024, SG làm CoT), LLaVA-SG (arXiv 2408.16224, chiếu nút SG thành token), GBC (arXiv 2407.06723, caption dạng đồ thị), TSG (ACL 2023, SG→caption), Entity-aware MMKG (TMM 2023), KALE (IJCAI 2024).

---

## 2. Ma trận trùng lặp (bài × lựa chọn thiết kế)

Ký hiệu nguồn đồ thị: **P** = SG dự đoán từ ảnh (SGG/VLM/detector); **T** = SG parse từ văn bản caption; **K** = KG ngoài (ConceptNet/Wikidata/miền); **B** = cả SG và KG.
Điểm bơm: **In** = text/JSON trong prompt; **Soft** = token liên tục/adapter; **XA** = cross-attention; **Dec** = can thiệp lúc giải mã; **Tgt** = đồ thị là target sinh ra (CoT hoặc output); **Rw** = reward RL/DPO; **Ver** = kiểm chứng/hậu kiểm; **Data** = dùng đồ thị để tạo/lọc dữ liệu huấn luyện.
Huấn luyện: **SFT**, **RL** (GRPO/PPO), **DPO**, **Fz** = đóng băng/training-free, **Cls** = huấn luyện encoder-decoder cổ điển từ đầu.

| ID | Nguồn | In | Soft | XA | Dec | Tgt | Rw | Ver | Data | Huấn luyện | Ngôn ngữ | Đo ảo giác? | Tác vụ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 AKGMA | B | ✔ | ✔(adapter) | | | | ✔(RL chọn subgraph) | | | SFT+RL | EN | ✔ knowledge halluc. | caption mở |
| P2 MERGE | K(entity KB) | ✔ | | | | | | | | SFT? | EN | NER F1 | news cap |
| P3 SEAR | K(tự trích) | ✔ | | | | | | | | Cls nhẹ | EN | – | caption |
| P4 MsRAG | (RAG, không KG) | ✔ | | | | | | | | Fz | ? | – | dense cap |
| P5 ExpArt-KG | K | ✔ | | | | | | ✔(judge dừng) | | Fz | EN/JA? | – | art desc |
| P6 ArtRAG | K | ✔ | | | | | | | | Fz | EN | – | art desc |
| P7 VLCE | K | | | ✔ | | | | | | Cls | EN | – | disaster |
| P8 SC-Captioner | T | | | | | | ✔ | | | RL | EN | gián tiếp (P/R) | caption |
| P9 FoCUS | T | | | | | | ✔ | ✔(attr/rel) | | RL(GRPO) | EN | ✔ suppression | caption điều khiển |
| P10 PSGP | P(xác suất) | | ✔ | | | | | | | SFT | EN | ✔ faithfulness, calibration | VQA (+cap) |
| P11 LUX | P(lesion) | | | ✔ | | | | | | Cls | EN | – | y tế |
| P12 K-DFIC | P→LLM→K | ✔ | | ✔ | | | | | | Cls | EN | – | caption |
| P13 RelCheck | P + box | | | | | | | ✔ | | Fz | EN | ✔ MME | sửa caption |
| P14 Multi-hop | K | | | | | | | ✔ | | Fz | EN | ✔ factual | caption |
| P15-P17 | K | | | ✔ | | | | | | Cls | EN | – | caption |
| P18 Cotton | K(MMKG) | | | ✔ | | | | | | Cls | EN/ZH? | – | nông nghiệp |
| V1-V3 (VN) | K / P+K | | | ✔ | | | | | | Cls | **EN** | – | caption |
| N1 KG-ViP | B | ✔ | | | | | | | | Fz/SFT | EN | ✔ knowledge halluc. | VQA |
| N2 MMGraphRAG | B | ✔ | | | | | | | | Fz | EN | – | QA |
| N3 MMCD | P(+nhiễu) | | | | ✔ | | | | | Fz | EN | ✔ object | compositional |
| N4 SceneAlign | P | | | | | | ✔(DPO) | | ✔ | DPO | EN | ✔ | reasoning |
| N5 SaGe | P/T | | | | | ✔ | ✔ | | ✔ | SFT+RL | EN | – | reasoning |
| N6 Relation-R1 | P | | | | | ✔ | ✔ | | | SFT+RL | EN | – | relation |
| N7 VisKG | P→K | | | | | ✔ | ✔ | | | SFT+GDPO | EN | – | reasoning |
| N8 Video SR | T | | | | | | ✔ | ✔ | | RL | EN | ✔ | video cap/QA |
| N9 SG consolid. | T | | | | | ✔(trung gian) | | | | SFT nhẹ | EN | – | video cap |
| N12 CheXPO-v2 | K(miền) | | | | | | ✔ | | | RL | EN | ✔ | y tế VQA |
| N13 R2GenKG | K(MMKG) | | ✔(R-GCN) | | | | | | | SFT | EN | – | báo cáo X-quang |
| N14 PoSh | T/P | | | | | | | ✔(eval) | | Fz | EN | ✔ | metric |
| **VSPS (của mình)** | P(mệnh đề có kiểu, 3 trạng thái) | | | | | | | ✔ | ✔ | SFT (QLoRA) | **VI** | ✔ CHAIR-vi | caption chi tiết |

Cách đọc: cột "Ngôn ngữ" gần như toàn EN. Cột "Data" (đồ thị dùng để *tạo dữ liệu huấn luyện captioner*) chỉ có SceneAlign/SaGe (cho suy luận, không cho caption) và VSPS. Cột "Dec" chỉ có MMCD (không phải caption).

---

## 3. Các ô trống (chưa thấy bài 2025-2026 nào)

Thang đánh giá. Novelty: **low** = đổi ngôn ngữ/miền của một ô đã có; **med** = tổ hợp mới của hai thành phần đã có, reviewer có thể nói "A + B"; **high** = cơ chế chưa thấy trong bất kỳ ô nào. Feasibility trên 1× RTX 3090 24 GB: **H** = suy luận hoặc QLoRA ≤ 8B, vài GPU-h; **M** = cần một vòng RL/DPO hoặc dựng tài nguyên vừa; **L** = cần nhãn người lớn hoặc huấn luyện > 8B.

| # | Ô trống (tổ hợp) | Bài gần nhất (khác ở đâu) | Novelty | Feasibility 3090 | Ghi chú |
|---|---|---|---|---|---|
| G1 | **Đồ thị mang trạng thái kiểm chứng (SUPPORTED/UNCERTAIN/REJECTED) × Data/SFT target × caption chi tiết** | PSGP (bất định xác suất, nhưng làm soft prompt cho VQA, không tạo dữ liệu); RelCheck (KB hậu kiểm, không huấn luyện); SceneAlign (nhiễu SG cho DPO suy luận) | **med-high** | **H** (đã có pipeline VSPS) | Đây chính là VSPS nếu gọi tên đúng là "verified scene graph". Rủi ro: VSPS đã công bố ở FAIR 2026, nên novelty phải đến từ phần mở rộng (G2-G5), không phải lặp lại |
| G2 | **Quy tắc phụ thuộc cha-con kiểu DSG × Rw hoặc Dec × caption** (relation/attribute chỉ được thưởng hoặc giữ khi nút cha được kiểm chứng) | DSG/FIHA dùng phụ thuộc cho *đánh giá*; FoCUS/SC-Captioner dùng reward SG phẳng, không phụ thuộc | **high** | **M** (GRPO G=4 trên Qwen2.5-VL-3B/7B QLoRA, verdict tra offline; 6-8 GPU-h/run theo ước tính ở 00_TONG_HOP) | Ô tốt nhất cho "phương pháp mới". Reward phẳng thưởng cả quan hệ trên vật thể ảo; reward phụ thuộc thì không. Có thể đo trực tiếp: tỷ lệ relation hallucination trên nút cha bị REJECT |
| G3 | **KG ngoài (ConceptNet/đồng xuất hiện VG) × nguồn hard negative cho verifier hoặc DPO × caption chi tiết** | SceneAlign tạo negative bằng nhiễu SG nội tại (không dùng KG, không phải caption); CheXPO-v2 dùng KG cho reward y tế | **med-high** | **H** (tra KG chạy CPU; DPO QLoRA 7B chạy được) | Nhắm vào lỗi "đồ vật hay đi kèm" (fork → knife), vốn là nguồn CHAIR chính. Negative "hợp lý theo thường thức nhưng không có trong ảnh" chưa ai dựng từ KG cho caption |
| G4 | **Phân cấp IsA của KG × trung tính hóa nút UNCERTAIN × dữ liệu SFT** (chó → con vật, xe tay ga → xe máy) | Chưa thấy bài nào. Gần: REVERSE (gắn nhãn cụm không chắc, backtrack lúc suy luận), hedging | **high** | **H** (CPU + 1 lần SFT) | Tổng quát hóa luật thủ công giới tính trong VSPS. Cần ánh xạ từ vựng VI → khái niệm (độ phủ ConceptNet tiếng Việt chưa kiểm, xem file 11). Wikidata có nhãn `vi` |
| G5 | **Verified graph × Soft/graph-token adapter × caption chi tiết** (mã hóa đồ thị đã kiểm chứng thành token cho LVLM lúc suy luận) | PSGP (soft token xác suất, VQA); AKGMA SCKA (bơm SG annotation); LLaVA-SG (2024) | **med** | **M-L** (cần SGG/verify lúc suy luận → mất tính "single-pass"; adapter nhỏ thì huấn luyện được) | Không khuyên: đắt lúc suy luận, cạnh tranh trực tiếp với PSGP/AKGMA, và LVLM mạnh thường không hưởng lợi (Inference-Time Structural Reasoning 2603.27349 thấy SG chỉ giúp mô hình đã mạnh) |
| G6 | **SG/KG × Dec (graph-conditioned / contrastive decoding) × caption chi tiết** | MMCD (SIGIR 2025) chỉ làm compositional reasoning, không caption; VGD/SSAV (file 00) kiểm vật thể bằng vùng, nhị phân | **med** | **H** (training-free, chạy trên Qwen2.5-VL-7B 4-bit) | Dùng làm *baseline mạnh* hơn là đóng góp chính. Đo được trên CHAIR-vi có sẵn |
| G7 | **SG-then-caption (Tgt trung gian) × SFT × ảnh tĩnh, caption chi tiết** | CCoT (2024, prompt); N9 (video, graph-to-text decoder riêng); SaGe/VisKG (cho suy luận, không cho caption) | **low-med** | **H** | Ô hẹp. Dễ bị nói "CCoT + SFT". Chỉ đáng làm nếu đồ thị trung gian được **kiểm chứng** trước khi render (nối với G1) |
| G8 | **KG văn hóa Việt (áo dài, nón lá, chợ, xe máy) × RAG/In × entity-aware caption** | MERGE/SEAR/ArtRAG (EN, miền tin tức/nghệ thuật); MUNIChus không có VI | **med** | **M** (dựng KG nhỏ từ Wikidata `vi` + từ vựng UIT-OpenViIC; khó đo nếu không có gold) | Có câu chuyện văn hóa, nhưng UIT-OpenViIC/KTVIC ít tên riêng → lợi ích có thể nhỏ. Hợp ViTextCaps (scene text có tên riêng) hơn |
| G9 | **Mọi ô trên × tiếng Việt** | V1-V4 (VN, nhưng dữ liệu EN); ViTextCaps PhonoSTFG (đồ thị hợp nhất đặc trưng, không phải KG/SG ngữ nghĩa) | **low** nếu đứng một mình | – | Chỉ là hệ số nhân. Không được bán "first Vietnamese" như đóng góp duy nhất |
| G10 | **Reward KG-consistency (không phải SG) × caption chi tiết miền chung** | CheXPO-v2 (y tế VQA), A6 EAAI 2026 (file 11, caption trẻ em, metric tri thức + RL) | **med** | **M** | Gần G2/G3. Nếu làm thì gộp vào G2 như một thành phần reward ("quan hệ vi phạm thường thức bị phạt") |

Ô **đã chiếm, nên tránh** làm đóng góp chính: KG/ConceptNet → cross-attention encoder-decoder (P7, P12, P15-P17, V1-V3); KG-RAG prompt cho LVLM (P2-P6); reward SG phẳng cho caption bằng GRPO (P8, P9); SG+KG hợp nhất làm ngữ cảnh (P1, N1, N2); SG hậu kiểm viết lại câu (P13).

---

## 4. Gợi ý ghép ô thành một phương pháp (để agent tổng hợp dùng)

Ghép ít ô nhất mà vẫn có cơ chế mới: **G1 (verified SG làm dữ liệu) + G2 (reward phụ thuộc DSG) + G3 (hard negative từ KG) + G4 (trung tính hóa IsA)**, chạy trên Vintern-1B/3B hoặc Qwen2.5-VL-3B/7B QLoRA, dữ liệu KTVIC + UIT-OpenViIC.
- Đóng góp chính về phương pháp là **G2**, vì chưa có bài nào. G3 và G4 là thành phần, mỗi cái có ablation riêng.
- G6 (graph contrastive decoding kiểu MMCD) dùng làm baseline training-free.
- Không cần GNN hay graph-token adapter (G5). Bỏ được rủi ro lớn nhất về chi phí suy luận và trùng PSGP/AKGMA.
- Phải trích trong bài: AKGMA, PSGP, FoCUS, SC-Captioner, SceneAlign, MMCD, RelCheck, SaGe, CheXPO-v2, V1-V4. Với FAIR, V4 là bắt buộc.

---

## 5. Chưa xác minh

- **V4 (FAIR 2025, DOI 10.15625/vap.2025.0297)**: chỉ có tiêu đề + tác giả qua Semantic Scholar. Trang DOI trả "Access is denied", nên chưa biết dữ liệu là tiếng Việt hay tiếng Anh. Cần mở kỷ yếu FAIR 2025.
- **MERGE code**: một kết quả WebSearch nói có `github.com/youxiaoxing/MERGE`, nhưng trang arXiv 2511.21002 không hiện link. Chưa mở GitHub.
- **AKGMA**: chỉ có abstract qua S2/AAAI OJS. Chưa đọc full, nên chưa biết backbone, các dataset ngoài UniKnowCap, có code hay không.
- **PSGP (WACVW 2026)**: chỉ có abstract qua S2. Abstract nói "VQA and image captioning" nhưng thí nghiệm liệt kê chỉ GQA/VSR/Ambiguous-GQA. Chưa rõ có thí nghiệm captioning không.
- **ArtRAG venue ACM MM 2025** và **KG-ViP venue ACL 2026** lấy theo trường venue của S2, chưa đối chiếu proceedings.
- **ExpArt-KG**: ngôn ngữ thí nghiệm (EN hay JA) chưa rõ. Nhóm tác giả ở NAIST/Tokyo.
- **P15, P16, P18, P19, ESWA 2025 "Implicit visual knowledge enhanced zero-shot image captioning" (10.1016/j.eswa.2025.130862), SIVP 2026 "Boosting scene captioning ... LLM integration" (10.1007/s11760-026-05613-x), ESWA 2026 ViS2T (10.1016/j.eswa.2026.133544)**: chỉ có tiêu đề/abstract một phần qua S2, chưa đọc full. Hai bài ESWA/SIVP không có abstract, nên **không đưa vào ma trận**.
- Độ phủ quét: arXiv API bị 429 sau 3 truy vấn đầu, OpenAlex hết budget ngày. Các truy vấn "graph decoding" trên S2 cũng bị 429. Có thể sót bài arXiv 2025-2026 về graph-conditioned decoding cho caption. Nên chạy lại các truy vấn ở mục 6 khi API hồi.

## 6. Truy vấn đã chạy (để lặp lại)

- arXiv: `abs:"scene graph" AND abs:captioning`; `abs:"knowledge graph" AND abs:captioning`; `abs:"scene graph" AND abs:hallucination`; `abs:"knowledge graph" AND abs:hallucination AND (abs:multimodal OR abs:vision)`; `abs:"news image captioning" OR abs:"entity-aware ... captioning"`; `abs:"knowledge-enhanced" AND abs:caption*` (sort theo ngày nộp, lọc ≥2025).
- Semantic Scholar bulk (year=2025-2026): `"scene graph" + (MLLM|LVLM|"vision-language model"|...) + (caption|captioning|hallucination)` (43 kết quả); `"scene graph" + (captioning|"image caption"|"image description")` (86); `("knowledge graph"|commonsense|ConceptNet|"knowledge-enhanced") + ("image captioning"|"image caption")` (40); `("scene graph"|"knowledge graph") + ("soft prompt"|"graph token"|...) + (MLLM|LVLM|"vision-language")` (10); `"scene graph" + (CoT|reasoning) + (caption|description|hallucination) + (MLLM|LVLM|multimodal)` (37).
- Chưa chạy được (429): `("scene graph"|"knowledge graph") + (decoding|"contrastive decoding"|"constrained decoding") + (hallucination|caption)`.
