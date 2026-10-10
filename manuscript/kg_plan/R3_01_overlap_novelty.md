# R3-01: Trùng lặp và tính mới của các đóng góp còn lại trong v2

Trục: **OVERLAP + NOVELTY**. Đối tượng: `00_KE_HOACH.md` v2, gồm P1 (bộ chấm người cấp caption + mệnh đề tiếng Việt, gold SG trên ảnh sạch, M1 định nghĩa lại, H-R, M2 định nghĩa lại, parser với 2 baseline) và P2 (lùi phân cấp có KG cho thực thể **và** vị từ trong caption, phải thắng viết-lại-CLC và lùi-sau-sinh).

Cách tra (10/10/2026, request ẩn danh): arXiv export API (`abs:`, lọc `submittedDate` 15/07–10/10/2026 cho các cụm caption+hallucination, caption+taxonomy/specificity, caption+KG, scene graph+metric, Vietnamese+multimodal); Semantic Scholar citations của CLC 2502.19110, Taxonomy-Aware Eval 2504.05457, CSS 2604.17487, Mohri & Hashimoto 2402.10978, SpeciaRL 2603.03197; web search. Mọi bài dưới đây đã mở abstract (arXiv API/abs) hoặc trang ACL Anthology. Conceptual Captions: đã đọc full text PDF. Tôi tự đánh giá trước, sau đó mới đối chiếu `R2_01`, `R2_02`, `R2_04`.

## 1. Verdict theo thành phần

| Thành phần | Mức trùng (của tôi) | Verdict | Ghi chú |
|---|---|---|---|
| P1: bộ chấm người cấp caption + mệnh đề tiếng Việt, công bố | LOW–MED | **pass** | Đến 10/10/2026 không tìm thấy bộ nào công bố. SHROOM-Visions 2026 chỉ có zh/en/fr/it. XM3600 có chấm người nhưng không công bố |
| P1: gold SG tiếng Việt trên ảnh sạch | MED | **pass** (sửa câu chữ) | VietSGG có trước. "3 trạng thái" không mới (HalDec-Bench) |
| P1: M1 (ước lượng điểm, từ rỗng, điểm độ cụ thể) | MED | **needs-fix** | Từng mảnh đều có tiền lệ: CapMAS, CapProbe (phạt caption dài mà rỗng, có lựa chọn Uncertain), SPECS (EMNLP'25, metric "specificity" cho caption), ClaimDiff-RL. Chỉ claim được tổ hợp + tiếng Việt |
| P1: H-R | MED–HIGH (phần thực thể) | **needs-fix** | Taxonomy-Aware Eval đã có hR cho văn bản tự do của VLM. Không được ghi H-R là metric "đề xuất" |
| P1: M2 định nghĩa lại | MED | pass | Ý so có ảnh/ảnh trống đã có (VCD, VLind-Bench). Phần mới hẹp, phù hợp vai "phụ" như plan đã ghi |
| P1: parser caption→SG tiếng Việt + 2 baseline | LOW | **pass** | Không tìm thấy parser tiếng Việt nào. DiscoSG và FACTUAL chỉ cho tiếng Anh |
| P2: lùi phân cấp KG cho **thực thể** | **HIGH nếu tách riêng** (ghép VSPS + Conceptual Captions + CLC) | **needs-fix** | Thay hypernym lấy từ KG vào dữ liệu huấn luyện caption đã có từ 2018 (CC3M). Chỉ còn mới ở chỗ lùi có điều kiện theo verdict kiểm chứng thị giác |
| P2: lùi **vị từ quan hệ** trong caption | LOW–MED | pass (thiếu trích dẫn) | Phân cấp vị từ đã có trong SGG (2009.05834; WACV'25 2311.12889; 2303.06842). RelCheck viết lại quan hệ sau sinh, RECAP thì từ chối trả lời. Không tìm thấy bài nào lùi vị từ trong caption hay trong dữ liệu SFT |
| P2: yêu cầu thắng CLC + lùi-sau-sinh | — | **needs-fix** | Cổng G-P2 chỉ yêu cầu "không thua CLC", và hoàn toàn không có điều kiện với lùi-sau-sinh |

**Tổng: 0 BLOCKER, 4 MAJOR, 4 MINOR.** Không thành phần nào, theo đúng phạm vi claim của v2, bị một bài 2025–2026 trùng ở mức HIGH. Có một rủi ro gần BLOCKER: nếu nấc vị từ không cho lợi ích đo được riêng, P2 chỉ còn phần thực thể, mà phần này trùng HIGH khi ghép các tiền lệ (F1, F2).

## 2. Phát hiện

### F1. [MAJOR] Thiếu tiền lệ "thay thực thể bằng hypernym từ KG trong dữ liệu caption": Conceptual Captions (ACL 2018)
- **Claim trong plan:** §1 ghi "Lùi phân cấp có KG cho thực thể + vị từ trong caption | MED (CLC, CSS, SpeciaRL; chưa tìm thấy cho caption)".
- **Bằng chứng:**
  - Sharma et al., *Conceptual Captions: A Cleaned, Hypernymed, Image Alt-text Dataset*, ACL 2018 (P18-1238, đã đọc PDF). Pipeline "use the Google Knowledge Graph (KG) Search API to match the named-entities to KG entries and exploit the associated hypernym terms", ví dụ "Harrison Ford" thành "actor", và dữ liệu này dùng để **huấn luyện captioner**. Lý do họ đưa ra: các chi tiết này không suy ra được từ ảnh.
  - arXiv 2304.13130 (2023, tác giả chưa xác minh), *Hypernymization of named entity-rich captions for grounding-based multi-modal pretraining*. Vòng 1 có nhắc (`05_kg_rag.md`), nhưng v2 không trích.
  - Ordonez et al., *From Large Scale Image Categorization to Entry-Level Categories*, ICCV 2013 (Marr Prize). Bài này chọn mức tên gọi trên cây WordNet cho ảnh, tức vấn đề "nên nói cụ thể đến mức nào".
  - HFRU arXiv 2605.08031 (05/2026) dùng reward "abstraction" cho phép thay thế hợp lệ về ngữ nghĩa khi unlearning. Trùng thấp (không có KG, bối cảnh unlearning).
- **Hệ quả:** reviewer sẽ đọc phần thực thể của P2 thành "hypernymization kiểu CC3M + điều kiện verifier kiểu VSPS". Câu "chưa tìm thấy cho caption" là sai với phần thực thể.
- **Sửa:**
  1. Dòng §1 đổi thành: "Lùi phân cấp có KG cho thực thể + vị từ | MED (nguyên lý: CLC, CSS, Conformal Factuality; **thay hypernym KG vào dữ liệu caption: Conceptual Captions 2018, 2304.13130**; tự trùng: VSPS trung tính hóa giới tính) | trung bình: lùi **có điều kiện theo verdict kiểm chứng từng mệnh đề**, mở rộng sang vị từ, tiếng Việt".
  2. Thêm vào baseline bắt buộc §2: **"hypernym-hóa vô điều kiện" (kiểu CC3M)**: lùi mọi thực thể/vị từ thuộc lớp nhạy cảm lên k=1 nấc, không phụ thuộc verdict. Nếu ViHG-Cap không hơn baseline này về M1-P ở cùng mức độ cụ thể, thì vai trò của verdict kiểm chứng không được chứng minh.
  3. Phần liên quan bắt buộc trích: CC3M, 2304.13130, Ordonez 2013, Deng 2012.

### F2. [MAJOR] Phần mới chính của P2 là thang vị từ, nhưng plan không đo riêng phần này
- **Claim:** §2 (C) "vị từ: đang cưỡi → ở trên → ở gần → chỉ giữ thực thể"; §0 B2 "claim thu hẹp: lùi có cấu trúc … cho cả thực thể **và vị từ quan hệ**".
- **Bằng chứng:** Theo F1, phần thực thể khi tách riêng là trùng HIGH theo kiểu ghép. Ở phần vị từ, phân cấp vị từ đã có trong SGG, nhưng chỉ để học bộ phân loại, không để viết caption: Zhou et al. arXiv 2009.05834 *Exploring the Hierarchy in Relation Labels for SGG*; arXiv 2311.12889 *Enhancing SGG with Hierarchical Relationships and Commonsense Knowledge*, WACV 2025 (theo comment arXiv); arXiv 2303.06842. Với quan hệ trong caption, RelCheck (2609.27890, 08/2026) sửa bằng LLM viết lại theo triple RelTR + hình học box, không lùi. RECAP (2609.26093, 08/2026) chấp nhận hoặc từ chối câu trả lời có/không về quan hệ không gian, cũng không lùi. Không tìm thấy bài lùi vị từ trong caption. R2_04 F9 đã yêu cầu đo riêng nấc trung gian, nhưng v2 chưa đưa vào.
- **Sửa:**
  1. Bảng đối đầu VSPS (§2) thêm nhánh tách: **(a) chỉ lùi thực thể; (b) lùi thực thể + "chỉ giữ thực thể" cho quan hệ (= D2 đã có); (c) (b) + các nấc vị từ trung gian**. Báo H-R_rel và M2 theo từng nhánh, 3 seed, CI.
  2. Thêm cổng vào §5: **"G-pred (31/01/2027): (c) hơn (b) về H-R_rel ≥ CI 95% mà không tăng lỗi quan hệ M2. Nếu trượt: bỏ 'vị từ' khỏi claim, và P2 không nộp ACM MM."**
  3. Phần liên quan trích 2009.05834, 2311.12889, 2303.06842, RelCheck, RECAP. Câu định vị: "phân cấp vị từ đã dùng để *phân loại* trong SGG; chúng tôi dùng nó để *chọn mức nói* trong caption theo verdict kiểm chứng".

### F3. [MAJOR] G-P2 chưa ép đúng điều kiện "phải thắng CLC và lùi-sau-sinh"
- **Claim:** §1 "Lõi P2 — phải thắng viết-lại-CLC và lùi-sau-sinh". Nhưng §5 G-P2 chỉ ghi: "E1 hơn SFT-không-kiểm-chứng trên M1-P **và không thua** viết-lại-CLC". Lùi-sau-sinh không xuất hiện trong cổng nào.
- **Bằng chứng:** CLC (arXiv 2502.19110, **NeurIPS 2025**, đã xác minh trên papers.neurips.cc) chính là baseline "lùi không cần cây". Nếu ViHG-Cap chỉ hòa CLC thì KG không đóng góp gì, đúng như R2_04 cảnh báo (điểm 3/10, "bỏ chữ KG"). BCEA (arXiv 2606.16667, 06/2026) cho thấy bộ lọc conformal cấp mệnh đề trên LVLM phải bỏ hơn 80% mệnh đề để giữ hallucination dưới 5%. Như vậy nhánh lùi/bỏ sau sinh là baseline mạnh và có trích dẫn, reviewer sẽ đòi.
- **Sửa (đổi đúng dòng G-P2):** "E1 hơn SFT-không-kiểm-chứng trên M1-P (dev, CI 95%) **và hơn cả viết-lại-CLC lẫn lùi-sau-sinh trên diện tích SFA ở cùng dải độ cụ thể (CI 95%)**. Nếu chỉ hơn SFT mà hòa CLC: bỏ 'KG' khỏi tên và claim, định vị là 'kiểm soát độ cụ thể có kiểm chứng', P2 → IP&M/TOMM." Thêm BCEA và Mohri & Hashimoto 2402.10978 vào nhánh lùi-sau-sinh (biến thể "bỏ" = lọc conformal).

### F4. [MAJOR] M1 và H-R vẫn đang được trình bày như metric mới, trong khi từng mảnh đã có
- **Claim:** §1 dòng "Metric M1 (ViVG-P/R sửa) + H-R | … | **Lõi P1**"; §3 M1 "kèm **điểm độ cụ thể trung bình** (độ sâu IsA)", "Từ rỗng … báo riêng".
- **Bằng chứng:**
  - SPECS: *Specificity-Enhanced CLIP-Score for Long Image Caption Evaluation*, EMNLP 2025 main (2025.emnlp-main.477, arXiv 2509.03897). Đây là metric "specificity" cho caption, đo tương quan với người. v2 không trích (vòng 1 chỉ nhắc ở file 15/18). Tên "điểm độ cụ thể" gần như chắc chắn sẽ bị so trực tiếp với SPECS.
  - CapProbe (arXiv 2608.11074, 08/2026): có lựa chọn "Uncertain", và "density-based metrics penalize verbose yet uninformative captions", cùng mục đích với việc xử lý từ rỗng.
  - ClaimDiff-RL (arXiv 2605.20278, 05/2026) và CapMAS (arXiv 2412.15484): chấm cấp mệnh đề, tách factuality và coverage.
  - Taxonomy-Aware Eval (arXiv 2504.05457, CVPR 2025): hP/hR trên văn bản tự do của VLM. Deng 2012: độ cụ thể theo information gain trên phân cấp.
- **Hệ quả:** H-R cho thực thể là hR của Taxonomy-Aware Eval áp lên nhiều thực thể. Mức trùng MED–HIGH. Chưa tính BLOCKER vì plan đã ghi "trích Taxonomy-Aware Eval", nhưng không được để H-R ở cột "đóng góp".
- **Sửa:**
  1. §1 tách dòng: "M1 + H-R | MED (PoSh, DSG, CapMAS, CapProbe, **SPECS**, Taxonomy-Aware Eval, Deng 2012) | **công cụ đo**, đóng góp là *thiết lập trên tiếng Việt + kiểm chứng bằng meta-eval A*, không claim metric mới". Đóng góp lõi P1 chỉ giữ: bộ chấm người công bố được, gold SG, parser.
  2. Đổi tên "điểm độ cụ thể" thành "độ sâu IsA trung bình (ID)" để không bị nhầm với SPECS. Trong meta-eval A (§3), thêm SPECS (bản đa ngữ hoặc qua dịch) làm metric so sánh, cạnh VLM-judge, ở cổng T4.

### F5. [MINOR] "3 trạng thái" trong gold SG
- §1 dòng gold SG ghi "3 trạng thái" là tính mới. HalDec-Bench (arXiv 2511.20515) và M-HalDetect đã có nhãn unknown (R2_02 đã nêu, v2 đã sửa ở §0 B4–B7 nhưng chưa sửa ở bảng §1).
- **Sửa:** ô tính mới đổi thành "caption chi tiết, ảnh đời sống Việt Nam, ảnh sạch sau dedup, cấp node/cạnh; nhãn unknown có tiền lệ cấp câu (HalDec-Bench, M-HalDetect)".

### F6. [MINOR] Bộ chấm người: nêu bằng chứng khoảng trống
- Khoảng trống được củng cố bằng SHROOM-Visions 2026 (arXiv 2608.25662, UncertaiNLP @ EMNLP 2026): span hallucination cho caption/VQA, **chỉ 4 ngôn ngữ zh/en/fr/it**. MUCH (2511.17081) cấp mệnh đề, đa ngữ nhưng là QA văn bản. ViHallu DSC2025 (2601.04711) là văn bản. Quét Vietnamese+multimodal trên arXiv đến 07/10/2026 (ViTextCaps 2604.27712, AutoViVQA 2603.09689, 2610.01637 …) không có bộ chấm người cho caption.
- **Sửa:** §1 thêm vào cột trùng lặp: "SHROOM-Visions 2026 (không có tiếng Việt), MUCH (QA văn bản)". Ghi rõ "đến 10/2026 chưa tìm thấy" để reviewer thấy phạm vi đã tra. Đây cũng là venue/cộng đồng tự nhiên để giới thiệu P1.

### F7. [MINOR] M2: thiếu tiền lệ "so có ảnh / ảnh trống"
- §3 M2 chia quan hệ theo mức ảnh làm đổi log-prob. Nguyên lý tương phản ảnh thật với ảnh nhiễu hoặc trống đã có ở VCD và VLind-Bench (plan đã trích VLind cho M2), và 2608.13267 (VLM "blind or misled", hình khoa học). Phần mới là chấm trên chính quan hệ của caption tiếng Việt.
- **Sửa:** câu M2 thêm "nguyên lý như VCD/VLind-Bench; khác ở chỗ chấm theo từng quan hệ trong caption tự do".

### F8. [MINOR] Mục "Chưa xác minh" đã lỗi thời
- §10 vẫn ghi venue CLC là chưa xác minh. Đã xác minh **NeurIPS 2025** (papers.neurips.cc, mlanthology). SpeciaRL: arXiv comment "Accepted at CVPR 2026". CSS: "ICML 2026 Workshop on Statistical Frameworks for Uncertainty in Agentic Systems". Taxonomy-Aware Eval: CVPR 2025.
- **Sửa:** chuyển CLC, SpeciaRL, CSS khỏi danh sách "Chưa xác minh" và ghi venue như trên.

## 3. Đối chiếu với vòng 2

- R2_01 (CLC/CSS/SpeciaRL, baseline CLC): **đã sửa** trong §0 B2 và §2. Chưa sửa cổng: G-P2 vẫn chỉ "không thua" (F3).
- R2_02 F8 (Taxonomy-Aware Eval): **đã trích**. H-R vẫn đứng ở cột đóng góp (F4).
- R2_04 F1 (tự trùng VSPS): **đã sửa** (§6). R2_04 F9 (đo riêng nấc vị từ trung gian): **chưa sửa** (F2).
- Mới ở vòng này: Conceptual Captions/hypernymization (F1), SPECS và CapProbe (F4), phân cấp vị từ trong SGG, RelCheck, RECAP (F2), BCEA (F3), SHROOM-Visions (F6).

## 4. Những gì plan làm đúng

- Đã hạ mọi "chưa có ai làm" xuống "chưa tìm thấy". Đã bỏ các thành phần HIGH (bơm KG vào generator, reward SG, E3).
- Đã có baseline CLC-style, lùi-sau-sinh và đối chứng đồ thị xáo trộn. Bảng §6 chống salami rõ ràng.
- P1 dựa vào khoảng trống có thật: bộ chấm người cho caption tiếng Việt được công bố, và parser caption→SG tiếng Việt. Vòng này tra tiếp đến 10/2026 vẫn không thấy bài nào lấp khoảng trống đó.
- Meta-eval A loại ViHG-Cap khỏi ứng viên để tránh tự phục vụ.

## Nguồn (đã mở)

- Conceptual Captions, ACL 2018: https://aclanthology.org/P18-1238/
- Hypernymization 2304.13130: https://arxiv.org/abs/2304.13130
- Ordonez et al. ICCV 2013: https://openaccess.thecvf.com/content_iccv_2013/html/Ordonez_From_Large_Scale_2013_ICCV_paper.html
- HFRU 2605.08031: https://arxiv.org/abs/2605.08031
- Phân cấp vị từ SGG: https://arxiv.org/abs/2009.05834 , https://arxiv.org/abs/2311.12889 , https://arxiv.org/abs/2303.06842
- RelCheck 2609.27890: https://arxiv.org/abs/2609.27890 ; RECAP 2609.26093: https://arxiv.org/abs/2609.26093
- CLC NeurIPS 2025: https://papers.neurips.cc/paper_files/paper/2025/hash/bce2501dd4edbc5d5757a1453757e883-Abstract-Conference.html
- BCEA 2606.16667: https://arxiv.org/abs/2606.16667
- SPECS EMNLP 2025: https://aclanthology.org/2025.emnlp-main.477/
- CapProbe 2608.11074: https://arxiv.org/abs/2608.11074 ; ClaimDiff-RL 2605.20278: https://arxiv.org/abs/2605.20278
- Taxonomy-Aware Eval 2504.05457, SpeciaRL 2603.03197, CSS 2604.17487 (arXiv comment cho venue)
- SHROOM-Visions 2026: https://arxiv.org/abs/2608.25662 ; MUCH: https://arxiv.org/abs/2511.17081
- Đã xem, không trùng đáng kể: ResOT 2610.11826, VGD 2607.27823, SAVOR 2609.16601, DSCC 2608.12746, Re³Cap 2608.21305 (EMNLP'26), PatchGate 2608.21819, OmniCapBench 2610.12458, Credal LLMs 2608.23244, HiR² 2607.02909 (ICML'26).
