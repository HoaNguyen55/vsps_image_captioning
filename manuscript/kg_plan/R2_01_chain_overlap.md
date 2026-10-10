# R2_01: Trùng lặp của cả chuỗi phương pháp ViHG-Cap (phản biện vòng 2, 2026-10-10)

Trục: **trùng lặp**. Đối tượng: mục 1 và 2 của `00_KE_HOACH.md`, gồm chuỗi đồ thị kiểm chứng 3 trạng thái → lùi IsA/vị từ cho node UNCERTAIN → SFT graph-then-caption → GEPA → reward phụ thuộc cha–con.

Cách tra: arXiv export API (truy vấn `abs:`/`ti:`, lọc từ 2025), Semantic Scholar citations API (đi theo các bài trích dẫn CLC 2502.19110, Taxonomy-Aware Eval 2504.05457, CSS 2604.17487), web search. Mọi bài dưới đây đều đã mở abstract qua arXiv API. Với 2604.01460, FoCUS 2609.00709, SCAPO 2609.35294 tôi đọc thêm full text HTML trên arxiv.org. Mọi request đều ẩn danh.

Lần này API không bị chặn, nên phần "rà lại khi API hết giới hạn" (mục 9 của bản nháp) về độ trùng LOW của lùi IsA đã chạy được. Kết quả: **khẳng định LOW không đứng vững ở mức khái niệm**.

---

## 1. Kết luận theo từng thành phần

| Thành phần | Bản nháp ghi | Kết luận R2 | Verdict |
|---|---|---|---|
| Cả chuỗi (≥3 mắt xích cùng lúc) | "chưa ai làm" | Không tìm thấy bài 2025–2026 nào làm ≥3 mắt xích cho captioning. Bài gần nhất chỉ gộp 2 mắt xích (2604.01460: reward SG có ràng buộc phụ thuộc + kiểm toán phân cấp, cho video; SaGe: SFT vết đồ thị + reward đồ thị, cho suy luận) | **pass** (đổi cách diễn đạt) |
| (A/B/D) Đồ thị kiểm chứng 3 trạng thái | không claim riêng | Không thấy đồ thị mang trạng thái SUPPORTED/UNCERTAIN/REJECTED dùng làm đích huấn luyện | pass |
| (C) Lùi IsA cho node UNCERTAIN | **LOW**, novelty cao, "chỉ Taxonomy-Aware Eval" | **MED về khái niệm** (lùi về mệnh đề kém cụ thể hơn thay vì xóa đã có cho LLM, kể cả fine-tune: CLC NeurIPS'25, CSS 2026). **LOW chỉ khi giới hạn** ở caption ảnh + điều kiện theo trạng thái kiểm chứng + phân cấp KG tường minh + lùi vị từ quan hệ | **needs-fix** |
| (E1) SFT graph-then-caption | LOW-MED | Không thấy cho caption. SaGe (ICML'26) làm cho suy luận | pass |
| (E2) GEPA | MED | Vẫn MED. Có thêm SCAPO (2609.35294, gán credit theo từng mệnh đề con) làm hàng xóm gần cho ý "loss cục bộ", và bài này chỉ thẳng vào rủi ro "giảm ảo giác bằng cách nói ít đi" | **needs-fix** (nhẹ) |
| (E3) Reward phụ thuộc cha–con | **LOW-MED**, "reward hiện có đều phẳng; quy tắc phụ thuộc mới có ở metric (2604.01460)" | **Sai sự thật.** 2604.01460 (COLM'26) đưa quy tắc phụ thuộc vào chính **reward GRPO**. FoCUS (EMNLP'26) cũng chỉ chấm thuộc tính trên object đã khớp. Mức trùng thực tế: **MED-HIGH** | **fail** (với claim hiện tại) |
| M3 SFA (đường cong Trung thực–Độ cụ thể) | gần nhất: Taxonomy-Aware Eval | Trục đánh đổi factuality–specificity đã là kết quả trung tâm của CLC (NeurIPS'25) và SpeciaRL (CVPR'26, correctness–specificity) | needs-fix |

---

## 2. Phát hiện

### F1. Reward "phụ thuộc cha–con" đã có trong reward huấn luyện, không chỉ ở metric. **BLOCKER**

- **Claim trong bản nháp (bảng mục 1):** "Reward/loss có phụ thuộc cha–con … LOW-MED (reward hiện có đều phẳng; quy tắc phụ thuộc mới có ở metric, arXiv 2604.01460) | novelty cao | **Lõi huấn luyện**".
- **Bằng chứng:**
  - *Reinforcing Consistency in Video MLLMs with Structured Rewards*, arXiv 2604.01460v2, comment arXiv "Accepted by COLM 2026". Mục 3.2 (full text HTML) mô tả reward scene graph dùng trong GRPO như sau: "An attribute can match only when it is attached to the same aligned object, a relation can match only when both endpoints are aligned". Bài còn có "Hierarchical factual VQA reward", kiểm xem mệnh đề cấp cao có được bằng chứng cấp thấp đỡ hay không, và một bộ kiểm toán top-down quan hệ → thuộc tính → tồn tại (RRA/ACA/ECA). Như vậy ràng buộc phụ thuộc nằm **trong reward**, không chỉ trong metric.
  - *FoCUS: Controllable Image Captioning with Prompt-Conditioned Scene Rewards*, arXiv 2609.00709, comment "EMNLP 2026 Main". Công thức (2): điểm thuộc tính là trung bình trên các object **đã khớp** ("If no objects are matched, we set S_attr = 0"). Đây cũng là một dạng ràng buộc cha–con trong reward GRPO cho caption ảnh.
- **Hệ quả:** reviewer chỉ cần đọc 2604.01460 là bác được cả hai ý "reward hiện có đều phẳng" và "novelty cao". Câu "quy tắc phụ thuộc mới có ở metric" trích sai chính bài mà bản nháp viện dẫn.
- **Sửa:**
  1. Dòng bảng mục 1 đổi thành: "Reward có điều kiện theo **trạng thái kiểm chứng** của node cha (cha UNCERTAIN → con trung tính; cha được nêu ở mức IsA cao hơn → con nhận điểm một phần) | **MED-HIGH** (2604.01460 COLM'26 và FoCUS EMNLP'26 đã gate thuộc tính/quan hệ theo object khớp) | trung bình | trung bình | **Ablation / thành phần**, không phải lõi."
  2. Mục 2 (E3) và mục 5: baseline "reward phẳng (FoCUS/SC-Captioner)" phải đổi thành **"reward SG có gate theo đầu mút (kiểu 2604.01460)"**. So với reward phẳng là so với rơm. Ablation "reward phụ thuộc vs phẳng" đổi thành "gate theo trạng thái kiểm chứng vs gate theo đầu mút khớp".
  3. Phần còn khác biệt, cần nói đúng mức: (i) gate theo trạng thái 3 mức chứ không theo khớp nhị phân với tham chiếu; (ii) điểm một phần theo mức IsA; (iii) không cần caption tham chiếu. Đây là chỗ khác về thiết kế, không phải ý tưởng mới.

### F2. Lùi về khái niệm kém cụ thể thay vì xóa đã có cho LLM, kể cả fine-tune. Claim LOW sai ở mức khái niệm. **MAJOR**

- **Claim trong bản nháp:** "Trung tính hóa node UNCERTAIN theo phân cấp IsA | **LOW** (chỉ Taxonomy-Aware Eval CVPR'25, và chỉ đánh giá) | **cao** | **Lõi phương pháp**". File 17 ghi thêm: "không thấy bài 2025-2026 nào leo hypernym có điều kiện theo độ tin cậy … để viết caption hoặc tạo dữ liệu huấn luyện".
- **Bằng chứng (đều đã mở abstract qua arXiv API):**
  - **CLC.** *Conformal Linguistic Calibration: Trading-off between Factuality and Specificity*, Jiang, Liu, Van Durme, arXiv 2502.19110, **NeurIPS 2025** (đã mở trang papers.neurips.cc). Bài viết lại mệnh đề không chắc thành phát biểu kém cụ thể hơn thay vì bỏ hẳn, kèm bảo đảm conformal, và "enables fine-tuning models to perform uncertainty-aware adaptive claim rewriting". Về khái niệm, đây chính là "lùi thay vì xóa" cộng thêm việc đưa vào huấn luyện, chỉ khác là làm trên văn bản/QA.
  - **CSS.** *Answer Only as Precisely as Justified: Calibrated Claim-Level Specificity Control for Agentic Systems*, arXiv 2604.17487, ICML 2026 Workshop. Bài tách câu trả lời thành mệnh đề, "proposes coarser backoffs", rồi xuất mỗi mệnh đề ở mức cụ thể nhất còn được hiệu chỉnh: "a local semantic backoff rather than … whole-answer refusal". Đây đúng là thao tác (C) ở cấp mệnh đề, cho văn bản.
  - **Gricean Retreat.** *Toward a Gricean Retreat: Probing LLMs for Knowledge Boundaries and Referent Specificity*, arXiv 2608.13484 (8/2026, preprint). Bài định khung "retreats up the specificity hierarchy, trading informativeness for truthfulness" và kêu gọi mục tiêu huấn luyện ghép nhận biết biên tri thức với độ cụ thể. Bài cho reviewer sẵn cái khung "Gricean" để gọi ViHG-Cap là một bản cài đặt.
  - Phía thị giác, chỉ ở phân loại:
    - **SpeciaRL**: *Specificity-aware RL for fine-grained open-world classification*, arXiv 2603.03197, **CVPR 2026**. Reward có verifier cân bằng correctness–specificity cho LMM.
    - **TARA** (arXiv 2603.00431, CVPR 2026) và **HiR²** (arXiv 2607.02909, ICML 2026): nhất quán phân cấp thô → mịn cho LMM.
  - Phía caption, chỉ ở đánh giá: **HalCECE** (arXiv 2503.00436, 2025, venue **chưa xác minh**) phát hiện ảo giác caption bằng "semantically minimal edits driven by hierarchical knowledge" (sửa theo phân cấp kiểu WordNet).
  - **Không tìm thấy** bài 2025–2026 nào lùi IsA hoặc lùi vị từ quan hệ trong **sinh caption ảnh** hay **tạo dữ liệu SFT cho captioner**. Đã tra các cụm: hypernym + caption / uncertain / VLM; specificity + caption + hallucination; hedg* + caption; granularity + uncertain + caption; backoff + claim/caption; "linguistic calibration" + image; Gricean + image; conformal + caption; taxonomy + hallucination; các citation của CLC, Taxonomy-Aware Eval và CSS.
- **Hệ quả:** reviewer quen CLC sẽ gọi (C) là "CLC cho caption, thay conformal bằng ngưỡng verifier". Giữ nguyên "LOW / novelty cao" thì dễ bị coi là không biết đến bài liên quan.
- **Sửa:**
  1. Đổi dòng bảng mục 1 thành: "Lùi phân cấp node UNCERTAIN | **MED về khái niệm** (CLC NeurIPS'25, CSS 2026: lùi mệnh đề văn bản về mức kém cụ thể; SpeciaRL CVPR'26: đánh đổi độ cụ thể cho phân loại ảnh), **LOW cho caption ảnh** (chưa thấy bài nào) | trung bình-cao | cao | Lõi phương pháp".
  2. Trong "Kết luận phản biện", thêm câu: "Ý lùi mệnh đề về mức kém cụ thể thay vì xóa đã có cho LLM văn bản (CLC, CSS); đóng góp của ta là đưa nó vào **caption ảnh**, với mức lùi do **KG/IsA tường minh** quyết định và điều kiện là **trạng thái kiểm chứng thị giác**, và mở rộng sang **vị từ quan hệ**."
  3. **Baseline bắt buộc mới (mục 5): "CLC-style rewrite"**. Cho một LLM viết lại các span UNCERTAIN thành bản kém cụ thể hơn, không dùng IsA/KG. Nếu ViHG-Cap không hơn baseline này về H-R, ViRHR hoặc độ đúng mức lùi, thì KG không đóng góp gì và claim "transformer + KG thật" sụp. Thêm vào ablation: "(−) IsA KG, thay bằng LLM tự chọn từ chung hơn".
  4. Mục 3, M3 SFA: ghi "gần nhất: CLC (đường cong factuality–specificity), SpeciaRL (correctness–specificity), Taxonomy-Aware Eval". Khác biệt còn lại: đo trên caption tự do tiếng Việt, gold 3 trạng thái, và quét theo mức IsA.
  5. Phần liên quan bắt buộc trích: CLC, CSS, Gricean Retreat, SpeciaRL, Taxonomy-Aware Eval, HalCECE.

### F3. Rủi ro "nói ít đi" đã được gọi tên và đo trong bài 2026. Lùi IsA có thể bị quy về đúng shortcut đó. **MAJOR**

- **Claim trong bản nháp:** lùi IsA và GEPA được trình bày như cách giảm ảo giác mà không mất thông tin. Mục 5 chưa có thước đo nào chặn shortcut này.
- **Bằng chứng:** *Beyond Saying Less: Fine-Grained Alignment for Informative and Faithful VLMs*, arXiv 2609.35294 (9/2026, preprint; đã đọc full text). Bài cho thấy RL on-policy hay "reducing hallucinations merely by saying less — making fewer valid claims", rồi đề xuất SCAPO, tức gán credit **độc lập cho từng mệnh đề con**, cùng tập DOPA dày đặc trên COCO. Về cơ chế, SCAPO là hàng xóm gần của "loss chỉ trên cụm bị sửa" của GEPA.
- **Hệ quả:** "người phụ nữ → người", "đang cưỡi → ở gần" là nói ít đi theo đúng nghĩa của bài này. Reviewer sẽ hỏi lùi IsA khác gì một shortcut được hợp thức hóa.
- **Sửa:**
  1. Mục 5: báo **số mệnh đề đúng trên mỗi caption** và **H-R** cạnh CHAIR/ViRHR cho mọi hệ. Thêm điều kiện dừng: nếu ViHG-Cap giảm ảo giác nhưng H-R kém VSPS > 2 điểm thì không claim "không mất thông tin".
  2. Thêm SCAPO vào related work của GEPA. Nếu GPU cho phép, thêm một ablation "gán credit theo mệnh đề con (kiểu SCAPO) thay cho cặp sửa đồ thị".
  3. Dòng GEPA trong bảng mục 1 thêm "SCAPO 2026 (credit cục bộ, on-policy)" vào cột trùng lặp. Mức MED giữ nguyên.

### F4. "Chuỗi chưa ai làm" đúng theo những gì tra được, nhưng phải nói rõ phạm vi tra. **MINOR**

- **Claim:** "Cái **chưa ai làm** là *chuỗi* …".
- **Bằng chứng:** không bài 2025–2026 nào tôi mở được gộp ≥3 mắt xích. Các bài gộp nhiều nhất:

| Bài | Mắt xích có | Thiếu |
|---|---|---|
| 2604.01460 (COLM'26, video) | SG từ caption, reward gate cha–con, kiểm toán phân cấp | trạng thái kiểm chứng, lùi IsA, SFT graph-then-caption, preference |
| SaGe 2607.05716 (ICML'26) | SFT vết suy luận qua đồ thị, reward theo node | caption, kiểm chứng, lùi |
| SceneAlign 2601.05600 (ACL'26 theo vòng 1) | nhiễu SG → DPO | caption, trạng thái, lùi |
| FoCUS 2609.00709 (EMNLP'26) | reward SG có gate thuộc tính | trạng thái, lùi, SFT đồ thị |
| SCAPO 2609.35294 | credit cục bộ theo mệnh đề | đồ thị, lùi |
| CLC 2502.19110 (NeurIPS'25) | lùi mệnh đề + fine-tune | ảnh, đồ thị, KG |

- **Sửa:** đổi "Cái **chưa ai làm** là chuỗi" thành "Đến 10/2026, qua các truy vấn ở R2_01, **không tìm thấy** bài nào gộp quá 2 mắt xích của chuỗi; bài gần nhất là 2604.01460 (video, reward có gate) và CLC (lùi mệnh đề, văn bản)." Bỏ các từ tuyệt đối.

### F5. Đồ thị trung gian trong SFT không mới với tư cách cơ chế. Hiện bản nháp chưa claim quá. **MINOR**

- **Claim:** E1 "đồ thị là chuỗi suy luận trung gian (kiểu SaGe ICML'26)".
- **Bằng chứng:** SaGe (arXiv 2607.05716, comment "ICML 2026") SFT trên 120K vết suy luận lấy mẫu từ scene graph, nhưng cho VQA/perception. Các truy vấn "scene graph" + intermediate/reasoning/SFT + caption không ra bài caption ảnh nào 2025–2026. Hai bài video gần nhất là 2502.16427 (gộp scene graph, không fine-tune) và 2603.20887 (SG-guided SegCaptioning, kiến trúc riêng).
- **Sửa:** giữ nguyên. Thêm một câu: "khác SaGe ở chỗ đồ thị trung gian mang nhãn trạng thái và mức IsA, và đầu ra là caption chứ không phải đáp án".

### F6. Thao tác GEPA "nêu giới tính UNCERTAIN" cần trích bài thiên kiến giới 2026. **MINOR**

- **Bằng chứng:** *ViD: Vision-Dominant Gender Bias Mitigation for LVLMs*, arXiv 2609.16647, comment "EMNLP 2026 Main". Bài giảm thiên kiến giới bằng can thiệp lúc suy luận, không lùi về "người". File 17 nhắc thêm 2605.31556, nhưng chỉ qua snippet.
- **Sửa:** trích ViD ở mục văn hóa/giới. Ghi khác biệt: lùi "người phụ nữ → người" chỉ khi verifier để UNCERTAIN, và giữ nguyên khi SUPPORTED.

---

## 3. Bản nháp làm đúng

- Đặt tính mới ở **giao điểm**, không ở từng mảnh, và hạ KG-injection, graph-token, encoder quan hệ xuống ablation hoặc bỏ. R2 không thấy lý do đổi các quyết định này.
- Đánh giá GEPA ở mức MED và không claim "loss mới" (file 12 đã ghi rõ DPA của HALVA) là đúng mức.
- Đã có sẵn ablation "(−) lùi IsA (xóa thay vì lùi)" và đối chứng đồ thị xáo trộn. Chỉ cần thêm baseline CLC-style (F2) và chỉ số chống "nói ít đi" (F3).
- Mục 9 đã tự đánh dấu "tính mới LOW của lùi IsA" là việc phải rà lại. R2 xác nhận việc rà lại này là cần, và kết quả là phải hạ mức.

## Truy vấn đã chạy (để vòng 3 lặp lại được)

arXiv API, lọc từ 2025:
- `abs:hypernym AND abs:caption*`
- `abs:hypernym AND abs:uncertain*`
- `abs:hypernym AND (VLM|MLLM|LVLM|"vision-language")`
- `abs:specificity AND abs:caption* AND abs:hallucinat*`
- `abs:specificity AND abs:factuality AND (image|visual|multimodal)`
- `"specificity" AND "hallucination" AND "vision-language"`
- `abs:hedg* AND abs:caption*`
- `abs:granularity AND abs:uncertain* AND abs:caption*`
- `abs:backoff AND (claim*|caption*)`
- `"back off" AND LLM`
- `"linguistic calibration" AND (image|visual|multimodal)`
- `Gricean AND (image|visual)`
- `conformal AND caption*`
- `taxonom* AND hallucinat*`
- `taxonomy AND caption* AND (VLM|MLLM|LVLM)`
- `hierarch* AND "less specific"`
- `"hierarchical consistency" AND "vision-language"`
- `abstention AND hierarch*`
- `"coarse-to-fine" AND uncertain* AND caption*`
- `"scene graph" AND caption*` kết hợp với lần lượt: `"chain-of-thought"`, `intermediate`, `reasoning AND SFT`, `"detailed caption*"`, `"fine-tun*" AND hallucinat*`, `preference`, `DPO`, `reward`, `uncertain*`
- `ti:"scene graph" AND ti:caption*`
- `"graph edit*" AND (DPO|preference)`
- `"structured caption*" AND hallucinat*`

Semantic Scholar: danh sách citation của 2502.19110, 2504.05457, 2604.17487, 2503.00436.

Web search: "graph-then-caption", "scene graph chain-of-thought captioning", hypernym hoặc "less specific" + captioning, fallback thô hơn cho MLLM, specificity calibration cho captioning.
