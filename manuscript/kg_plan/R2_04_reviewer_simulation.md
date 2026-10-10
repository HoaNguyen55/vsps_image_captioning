# R2_04. Mô phỏng phản biện, trục TÍNH MỚI (novelty)

Critic 04, vòng 2, ngày 2026-10-10. Đối tượng: `00_KE_HOACH.md`. Tôi mô phỏng 3 reviewer ACM MM 2027 cho **P2 (ViHG-Cap)** và 2 reviewer EMNLP 2027 (ARR) cho **P1 (benchmark + metric)**. Trọng tâm: ViHG-Cap có tách được khỏi bài VSPS đã có không (rủi ro tự trùng lặp, cắt lát "salami").

**Nguồn đã mở trong vòng này.** Bài VSPS v10 (`FAIR_28.08.26_v10_EN_IEEE.pdf`, đọc toàn văn qua pdftotext). arXiv export API (ẩn danh, không có email) cho: 2402.10978, 2502.19110, 2405.18654, 2402.11411, 2310.01779, 2311.17076, 2601.05600, 2607.05716, 2510.19060, 2504.05457, 2604.01460, 2609.00709, 2508.06125. Venue lấy theo comment arXiv nếu có. Venue không có trong comment thì ghi "chưa xác minh". Bài chỉ được dẫn lại từ file vòng 1 thì có ghi rõ.

---

## 1. Kết luận theo từng thành phần (trục tính mới)

| Thành phần | Kết luận | Lý do ngắn |
|---|---|---|
| ViHG-Cap (A) đề xuất đồ thị | **fail** (với vai trò đóng góp) | Generator chính là generator của VSPS. REACT++/OWLv2 chỉ là thay linh kiện |
| (B) kiểm chứng 3 trạng thái + cổng cấu trúc + logit + box | **fail** (với vai trò đóng góp) | 3 trạng thái là đóng góp (2) của VSPS. Cổng cấu trúc và box là sửa lỗi VSPS, và cũng nằm trong danh sách P0 (§7) |
| (B) tiền nghiệm KG một chiều | **needs-fix** | Cùng nguyên lý với "ceiling rules may only lower a verdict" của VSPS (§III-B2). Đây chỉ là thêm một luật trần |
| (C) lùi phân cấp IsA / vị từ | **needs-fix** | Mức trùng LOW trong bảng §1 là sai. Bản thân VSPS đã làm việc này cho giới tính, và có Conformal Factuality, CLC (mục 2, F1) |
| (D) đồ thị G* | **fail** (với vai trò đóng góp) | Là bản ghi bằng chứng của VSPS, thêm một trường mức IsA |
| (E1) SFT graph-then-caption | **needs-fix** | Mới so với VSPS, nhưng trùng CCoT và SaGe. Chỉ đủ làm ablation |
| (E2) GEPA | **needs-fix** | Loss của GEPA là biến thể DPA của HALVA (file 12 tự ghi vậy). Negative sinh từ đồ thị là của SceneAlign |
| (E3) reward phụ thuộc cha–con | **fail** (như bảng §1 đang ghi) | Câu "reward hiện có đều phẳng" mâu thuẫn với chính file 17 về 2604.01460 (COLM 2026) |
| P1: gold SG tiếng Việt + bộ chấm điểm người | **pass** (có điều kiện) | Đây là chỗ mới thật nhất của cả kế hoạch, với điều kiện gold không bị neo vào VSPS |
| P1: M1 ViVG-P/R (gold 3 trạng thái) | **needs-fix** | Phải định nghĩa lại UNCERTAIN là độ mơ hồ của người gán nhãn, không phải verdict của máy |
| P1: M2 PDG, M5 TBW, M6 NVL | **needs-fix** | Sáu metric cho một bài là phình metric. Mỗi metric chỉ được kiểm chứng sơ sài |
| P1: M3 H-R/SFA | **needs-fix** | Gần Taxonomy-Aware Eval. Metric này được thiết kế để làm nổi phương pháp của chính nhóm (P2) |
| Kế hoạch công bố P0/P1/P2 (§6) | **fail** | Cùng một phần khác biệt được tính cho cả P0 (TALLIP) lẫn P2 (ACM MM). Cả hai đều là venue của ACM |

---

## 2. Mô phỏng reviewer

### P2, ACM MM 2027: "ViHG-Cap: Verified Hierarchical Graph Captioning for Vietnamese"

#### R1. Chuyên gia giảm ảo giác / alignment cho LVLM (gắt nhất)

**Tóm tắt.** Bài sinh đồ thị mệnh đề, kiểm chứng mỗi node thành 3 trạng thái, đưa node UNCERTAIN lùi lên hypernym, huấn luyện Qwen2.5-VL bằng SFT với đích "đồ thị rồi caption", sau đó dùng preference cục bộ trên các cụm bị sửa.

**Điểm mạnh.** Có thiết lập ít tài nguyên rõ ràng. Có đối chứng đồ thị bị xáo trộn. Có ý thức về đánh đổi precision–recall.

**Điểm yếu.**
1. **Gần như toàn bộ pipeline (A)(B)(D) là VSPS** [tự trích dẫn]. Bài VSPS đã có mệnh đề có kiểu, cặp truy vấn khẳng định/phủ định lấy mẫu K = 5 lần, 3 trạng thái, luật trần chỉ được hạ mức, và trung tính hóa UNCERTAIN thay vì xóa. Chính phần Limitations và Future work của VSPS đã liệt kê "region-grounded verification (H1, H2), proposition-level metrics (H3), coverage recovery (H5)". Bài này là bản thực hiện danh sách future work đó.
2. **Lùi phân cấp đã có tiền lệ cả về nguyên lý lẫn cách dùng.** Mohri & Hashimoto (arXiv 2402.10978): conformal prediction "corresponds to a back-off algorithm … progressively making LM outputs less specific". CLC (arXiv 2502.19110): "fine-tuning models to perform uncertainty-aware adaptive claim rewriting, … balance between factuality and specificity". HallE-Control (arXiv 2310.01779) chỉ ra ảo giác sinh ra khi mô tả mịn hơn mức vision module kiểm chứng được. VSPS đã áp nguyên lý này cho danh từ chỉ người (người phụ nữ → người).
3. **GEPA = HALVA + SceneAlign.** DPA (HALVA, arXiv 2405.18654, ICLR 2025) đã có loss cấp cụm trên các cặp "hallucinated/correct" do sửa ground truth ở mức cụm từ. POVID (arXiv 2402.11411) đã chèn ảo giác có chủ đích làm dispreferred. SceneAlign (arXiv 2601.05600) đã nhiễu đồ thị để tạo preference. File 12 của kế hoạch tự ghi loss GEPA là "biến thể DPA của HALVA".
4. Bài VSPS gốc có kết quả người chấm là **không trung thực hơn zero-shot** (3,91 so với 4,17, không có ý nghĩa thống kê), kém hơn về độ đầy đủ và độ trôi chảy. Xây tiếp trên một nền chưa thắng zero-shot theo người chấm thì phải chứng minh lại từ đầu.

**Tấn công "đây chỉ là X đổi tên".**
- "Hierarchical Back-off" = toán tử neutralization N(·) của VSPS, tổng quát hóa từ 1 nguồn bất định (giới tính) ra cây IsA. "Lùi vị từ" chính là trả lời câu VSPS đã viết: "neutralization … cannot apply to relations".
- "KG prior một chiều" = thêm một luật trần (ceiling rule) của VSPS.
- "G*" = bản ghi bằng chứng (evidence record) của VSPS thêm trường `isa_level`.
- "GEPA" = DPA/HALVA, với negative lấy từ G*.
- "Graph-then-caption" = CCoT (arXiv 2311.17076: sinh scene graph trước rồi mới trả lời) / SaGe (arXiv 2607.05716, ICML 2026).

**Baseline còn thiếu.** HALVA/DPA. RLAIF-V-7B (checkpoint công khai theo file novelty vòng 1, chưa mở lại). POVID. SENTINEL. **Lùi hậu kỳ không cần huấn luyện**: caption zero-shot → parse → verifier → lùi IsA theo kiểu conformal factuality. Baseline này kiểm tra xem bước huấn luyện có cần thiết không. VSPS + bảng IsA chỉ ở renderer (phần khác biệt tối thiểu so với VSPS).

**Điểm: 3/10.** Sẽ lên 5–6 nếu: (i) có một bảng chỉ so ViHG-Cap với VSPS, mọi thứ khác giữ nguyên, và cho thấy recall hoặc độ đầy đủ theo người chấm tăng mà precision không giảm; (ii) thắng HALVA và bản lùi hậu kỳ; (iii) thắng zero-shot về độ trung thực theo người chấm.

#### R2. Chuyên gia KG / suy luận có cấu trúc

**Tóm tắt.** Bài tự nhận là "transformer + KG". KG gồm một tập con Wikidata, bảng ánh xạ viết tay khoảng 250 dòng, và KG văn hóa 150–300 thực thể.

**Điểm mạnh.** Bài cố ý tránh đổ fact vào prompt, có trích NES. KG chỉ đóng vai một chiều, không bao giờ biến thành REJECT, nên an toàn.

**Điểm yếu.**
1. **Không có KG thật sự.** Thứ được dùng là tra hypernym và một bảng tra ~250 dòng. Không có suy luận đa bước, không có embedding, không học gì từ đồ thị. Gọi đây là "Knowledge Graph captioning" là nói quá.
2. Graph token G1/G2 đã bị chính kế hoạch hạ xuống mức ablation. Vậy phần "graph" trong mô hình chỉ còn là văn bản tuyến tính hóa.
3. Câu "reward hiện có đều phẳng" (bảng §1) là sai. 2604.01460 (COLM 2026) dùng reward scene graph có cấu trúc kèm "hierarchical self-verification". File 17 của kế hoạch mô tả nó là phụ thuộc kiểu DSG.

**Tấn công "đây chỉ là X đổi tên".** "Verified Hierarchical Graph" = DSG (ràng buộc cha–con) + WordNet lookup + VSPS verdict.

**Baseline còn thiếu.** KG-in-prompt (có trong danh sách). Đồ thị văn bản kiểu CCoT không qua kiểm chứng. Reward có cấu trúc kiểu 2604.01460, chuyển sang ảnh.

**Điểm: 3/10.** Sẽ lên 5 nếu bỏ chữ "KG" khỏi tiêu đề và claim, định vị là "kiểm soát độ cụ thể có kiểm chứng", và cho thấy cấu trúc IsA thắng một baseline lùi không dùng cây (ví dụ LLM tự viết lại cho chung hơn, kiểu CLC).

#### R3. Chuyên gia đa ngôn ngữ / ít tài nguyên (thiện chí nhưng chặt về độ chặt chẽ)

**Tóm tắt.** Phương pháp hướng tiếng Việt, đánh giá trên KTVIC/UIT-OpenViIC, có mô-đun văn hóa.

**Điểm mạnh.** Có động lực đo được: VSPS làm rơi từ văn hóa từ 58,8% xuống 16,2–23,5%. Có xử lý "xanh" và giới tính, là những vấn đề riêng của tiếng Việt. Nhắm phần cứng nhỏ.

**Điểm yếu.**
1. **Bộ test nhỏ và bẩn.** 401/558 ảnh test KTVIC gần trùng train UIT-OpenViIC, tập sạch chỉ còn 157 ảnh. Gold văn hóa chỉ có 65 ảnh.
2. **Phương pháp không phụ thuộc ngôn ngữ, nhưng chỉ chạy trên tiếng Việt.** Với khán giả ACM MM, không có kết quả tiếng Anh (COCO/DOCCI) thì không biết cái lợi đến từ phương pháp hay từ việc so với các baseline tiếng Việt yếu.
3. **Đánh giá chính dùng metric của P1**, mà P1 chưa được phản biện, lại do chính nhóm thiết kế (H-R/SFA đo đúng thứ ViHG-Cap tối ưu).

**Tấn công "đây chỉ là X đổi tên".** "VSPS v2 cho tạp chí."

**Baseline còn thiếu.** Vintern-3B/InternVL3.5 zero-shot có prompt "dùng từ chung khi không chắc". GRIT (đã có). ViG (MAPR 2026, theo file vòng 1).

**Điểm: 5/10.** Sẽ lên 6–7 nếu có một bộ tiếng Anh, tập test sạch hoặc gold ≥ 500 ảnh, CI bootstrap, và metric chính là metric ngoài (CHAIR, POPE/AMBER, người chấm), không chỉ metric của P1.

### P1, EMNLP 2027 (ARR): "Vietnamese verification-aware graph benchmark and metrics for captioning"

#### R4. Reviewer track tài nguyên / benchmark

**Tóm tắt.** Bài có gold scene graph tiếng Việt 500 ảnh, bộ chấm điểm của người cho caption tiếng Việt (500 ảnh × 5 hệ thống, 3 người chấm), parser ViT5, và 6 metric M1–M6.

**Điểm mạnh.** Theo file 15 vòng 1 thì đây là bộ phán xét người đầu tiên cho caption tiếng Việt (cần quét lại trước khi nộp). Có Krippendorff α, κ và τ_c theo chuẩn. Có luật dừng trung thực cho parser (thua "dịch → DiscoSG" thì không claim parser).

**Điểm yếu.**
1. **Gold bị neo.** Gold được làm theo kiểu "máy gợi ý → người sửa". Nếu máy gợi ý là pipeline VSPS thì gold mang thiên lệch của VSPS (anchoring), và metric sẽ có lợi cho VSPS/ViHG-Cap. Biện pháp "bỏ caption VSPS rồi báo lại" không sửa được lỗi nằm ở gold.
2. **Ý nghĩa của UNCERTAIN trong gold không rõ.** Nếu là verdict của máy thì gold không còn là gold. Nếu là độ mơ hồ theo người thì phải có giao thức và độ đồng thuận riêng cho nhãn này.
3. **Sáu metric, phần lớn là phiên bản tiếng Việt của metric đã có.** M1 ≈ DSG/PoSh/CAPTURE, M2 ≈ R-Bench/Reefknot trên caption tự do, M3 ≈ Taxonomy-Aware Eval, M4 ≈ CulturalVQA/RAVENEA, M5 ≈ GAVEL. Một bài EMNLP không kiểm chứng tử tế được sáu metric.

**Tấn công "đây chỉ là X đổi tên".** "ViVG-P/R = DSG/PoSh dịch sang tiếng Việt, cộng một vùng không chấm."

**Baseline còn thiếu.** Dịch → parser tiếng Anh (FACTUAL/DiscoSG) → SPICE/CAPTURE. PoSh trên bản dịch. VLM-judge (GPT-class và Qwen) chấm trực tiếp tiếng Việt. CIDEr, CLIPScore đa ngôn ngữ.

**Overall: 3/5** (Findings). Lên 3,5–4 nếu gold làm mù (không gợi ý máy, hoặc gợi ý từ một hệ không thuộc VSPS và đo mức neo trên 50 ảnh làm cả hai cách) và bài gọn lại còn 1–2 metric chính.

#### R5. Reviewer chuyên đánh giá / meta-evaluation

**Tóm tắt.** Như R4.

**Điểm mạnh.** Có thiết kế thống kê cẩn thận (Williams test, Holm). Có các nhiễu riêng của tiếng Việt (NFC/NFD, dấu, tách từ).

**Điểm yếu.**
1. **Vòng lặp tự phục vụ.** Metric có trạng thái kiểm chứng và H-R tồn tại để đo đúng cơ chế của P2. Reviewer sẽ hỏi: metric có giá trị khi không có ViHG-Cap không? Câu trả lời phải là τ_c trên các hệ không thuộc VSPS.
2. **T4 cho phép thua VLM-judge tới 0,03.** Nếu M1 không thắng judge thì đóng góp metric chỉ còn là "chẩn đoán". Khi đó bài là bài dữ liệu, và phải viết như bài dữ liệu ngay từ đầu.
3. PDG (ảnh trắng) là phép thử language prior đã quen thuộc trong dòng bài contrastive decoding và benchmark ảo giác. Chưa xác minh bài nào đã đặt đúng tên PDG, nhưng ý tưởng không mới.

**Overall: 2,5/5.** Lên 3,5 nếu M1 thắng hoặc ngang VLM-judge ở cấp hệ thống với chi phí thấp hơn nhiều, có kết quả cho từng ngôn ngữ con (caption ngắn và chi tiết), và M2/M5/M6 chuyển vào phụ lục.

---

## 3. Phát hiện (claim → bằng chứng → mức → cách sửa)

**F1. BLOCKER. Bảng §1, dòng "Trung tính hóa node UNCERTAIN theo phân cấp IsA … LOW (chỉ Taxonomy-Aware Eval CVPR'25)".**
- Bằng chứng: (a) Chính ví dụ trong dòng này, "người phụ nữ → người", là đóng góp (2) của VSPS v10, có công thức A(pᵢ) và con số 11.769 mệnh đề được khôi phục. (b) arXiv 2402.10978: conformal prediction = back-off "progressively making LM outputs less specific". (c) arXiv 2502.19110 (CLC): huấn luyện "adaptive claim rewriting" để cân bằng factuality–specificity. File novelty/00_TONG_HOP.md vòng trước đã xếp CLC vào mức "C3 HIGH (về nguyên lý)", nhưng kế hoạch không dùng thông tin đó. (d) HallE-Control 2310.01779: ảo giác do mô tả mịn hơn mức vision kiểm chứng được.
- Sửa: đổi ô trùng lặp thành **"MED (nguyên lý: Conformal Factuality, CLC; tự trùng: VSPS neutralization giới tính)"**, ô tính mới thành **"trung bình: mở rộng từ một nguồn bất định sang cây IsA thực thể + thang vị từ cho quan hệ, cho ảnh, ở mức dữ liệu SFT"**. Viết lại câu kết luận §1 thành: "…→ mở rộng toán tử trung tính hóa của VSPS [P0] từ giới tính sang phân cấp IsA và thang vị từ…". Thêm Mohri & Hashimoto, CLC và HallE-Control vào danh sách bắt buộc trích dẫn và vào danh sách baseline (bản lùi hậu kỳ).

**F2. BLOCKER. Rủi ro salami / tự trùng lặp giữa P0 (TALLIP) và P2 (ACM MM).**
- Bằng chứng: §7 mục 1–2 (cổng cấu trúc quan hệ, box hình học) được đưa vào P0, nhưng cũng là thành phần (B) của ViHG-Cap. Mục 4 (xóa văn hóa) là động lực chính của mô-đun văn hóa trong P2. VSPS v10 đã có (A), (B), (D) và nửa đầu của (C). TALLIP và ACM MM đều là venue của ACM, nên bản thảo sẽ bị đối chiếu trùng văn bản trong cùng hệ thống (chi tiết ngưỡng theo chính sách ACM: chưa xác minh).
- Sửa (chọn một, ghi vào §6):
  - **Phương án A (khuyên dùng):** P0 = VSPS + sửa lỗi (cổng cấu trúc, box, KTVIC sạch, hạn chế văn hóa). P2 chỉ claim phần **lùi phân cấp + huấn luyện dùng nó**. Trong P2, VSPS (đã kèm các sửa lỗi) là baseline chính, không phải thành phần.
  - **Phương án B:** gộp lùi IsA vào P0 (bản journal sẽ mạnh hơn rõ), bỏ P2 hoặc để P2 thành bài khác hẳn (ví dụ lấy GEPA hoặc RL làm lõi).
  - Thêm vào §6 một dòng: "Bảng phân định đóng góp P0/P1/P2. Mỗi thành phần chỉ được claim ở đúng một bài. Các bài còn lại trích dẫn nó như công trình trước."

**F3. MAJOR. Dòng "Reward/loss có phụ thuộc cha–con … LOW-MED (reward hiện có đều phẳng)".**
- Bằng chứng: abstract 2604.01460 (COLM 2026) có "structured reward … instance-aware scene-graph reward … VQA reward for hierarchical self-verification" và một "top-down audit" trong đó claim quan hệ phụ thuộc vào attribute và existence. File 17 vòng 1 kết luận đó "chính là quy tắc phụ thuộc kiểu DSG áp lên chấm caption".
- Sửa: đổi thành **"MED-HIGH (2604.01460, video; DSG)"**, gỡ khỏi nhãn "Lõi huấn luyện", ghi là E3 = ablation tùy chọn. Bỏ cụm "reward hiện có đều phẳng".

**F4. MAJOR. Dòng GEPA: "MED (… 0 hit cho caption)".**
- Bằng chứng: DPA/HALVA (2405.18654, ICLR 2025): cặp sửa ở mức cụm từ, loss cấp cụm, áp cho mô tả ảnh ("image description tasks"). POVID (2402.11411): chèn ảo giác làm negative. File 12 tự mô tả loss GEPA là "biến thể DPA của HALVA".
- Sửa: đổi thành **"MED-HIGH (HALVA/DPA: loss cấp cụm + KL; SceneAlign: negative từ đồ thị)"**. Phần khác biệt duy nhất được claim: "negative lấy từ trạng thái kiểm chứng (REJECTED thật, lùi sai mức IsA), không phải nhiễu ngẫu nhiên". Bắt buộc có ablation A2 (GEPA với negative ngẫu nhiên, kiểu HALVA) như file 12 đã đề xuất, và chỉ claim GEPA nếu thắng A2.

**F5. MAJOR. "Vì sao đây là transformer + KG thật" (§2).**
- Bằng chứng: KG ở đây chỉ là tra IsA cộng bảng ~250 dòng (§2, §4). Graph token đã bị hạ xuống ablation (§1).
- Sửa: bỏ đoạn này, hoặc viết lại: "KG chỉ dùng làm phân cấp khái niệm và tiền nghiệm hạ mức. Chúng tôi không claim đóng góp về kiến trúc đồ thị." Bỏ chữ "Graph"/"KG" khỏi tên phương pháp nếu không có thí nghiệm cho thấy cấu trúc IsA thắng baseline lùi không dùng cây (LLM tự viết chung hơn, kiểu CLC).

**F6. MAJOR. Nền VSPS chưa thắng zero-shot theo người chấm.**
- Bằng chứng: VSPS v10, Bảng VI: độ trung thực 3,91 (VSPS) so với 4,17 (zero-shot), độ đầy đủ 2,64 so với 4,47.
- Sửa: thêm vào §5 một **cổng T5**: "Human eval ViHG-Cap so với zero-shot Qwen2.5-VL-7B trên ≥ 100 ảnh. Nếu độ trung thực không vượt zero-shot với CI tách nhau thì P2 không nộp ACM MM, chuyển xuống TOMM/JVCIR." Claim chính của P2 phải là **khôi phục độ đầy đủ (H5 của VSPS) mà không mất độ trung thực**.

**F7. MAJOR. Gold của P1 có thể bị neo vào VSPS.**
- Bằng chứng: §4 ghi pilot gold làm theo kiểu "máy gợi ý → người sửa", và §8 tháng 11 dùng pipeline của nhóm.
- Sửa: thêm vào §4: "Gợi ý cho người gán nhãn lấy từ một hệ không thuộc VSPS (ví dụ InternVL3.5 thô, không kiểm chứng). Trên 50 ảnh, làm cả hai kiểu, có và không có gợi ý, để đo mức neo (F1 giữa hai bản gold)." Định nghĩa UNCERTAIN trong gold là "người gán nhãn không xác định được từ ảnh", có κ riêng cho nhãn này.

**F8. MAJOR. P1 có quá nhiều metric.**
- Sửa §3: giữ **M1 (kèm H-R làm chế độ chấm một phần)** là metric chính. Gộp M3 vào M1. M2/M4 thành phân tích phụ. M5/M6 chuyển sang P2 hoặc phụ lục. Bài P1 nên định vị là **bài tài nguyên** (gold SG tiếng Việt + bộ phán xét người), metric là phần thứ hai.

**F9. MINOR. Lùi vị từ và tiền nghiệm KG được ghi là "chưa thấy bài trùng".**
- Bằng chứng: VSPS §III-B2: "Ceiling rules may only lower a verdict". VSPS §III-B3 nói rõ quan hệ không trung tính hóa được. Repo đã có `scripts/relation_backoff.py` (D2, chỉ +1,2 recall theo memory ngày 2026-10-10).
- Sửa: ghi "tự trùng với VSPS (luật trần); lùi quan hệ → thực thể đã thử trong repo (+1,2 recall strict)". Phần còn mới là thang ~30 vị từ trung gian (đang cưỡi → ở trên → ở gần). Phải đo phần đóng góp của riêng nấc trung gian, tách khỏi nấc "chỉ giữ thực thể".

**F10. MINOR. Venue ghi trong bảng chưa khớp nguồn.**
- SceneAlign: comment arXiv 2601.05600 chỉ ghi "Preprint", nhưng bảng ghi ACL'26. Venue này chưa xác minh, cần kiểm trên ACL Anthology hoặc ghi "arXiv 2026". Venue NeurIPS 2025 của CLC lấy từ file novelty vòng 1, arXiv không có comment: chưa xác minh. Venue của Mohri & Hashimoto: chưa xác minh (arXiv không có comment).

**F11. MINOR. Mốc thời gian P1 và P2 chồng nhau.**
- P2 (ACM MM, ~04/2027) dùng metric của P1, mà P1 nộp ARR ~05/2027. Reviewer ACM MM sẽ thấy một bài đánh giá bằng metric chưa được phản biện. Sửa: P2 dùng CHAIR-vi, POPE/AMBER và người chấm làm metric chính, M1 là metric phụ có trích arXiv của P1.

---

## 4. Tổng hợp: cái gì mới thật, cái gì là VSPS đóng gói lại

| Đóng góp đang claim | Mới so với VSPS? | Mới so với tài liệu 2024–2026? | Phân loại |
|---|---|---|---|
| Đồ thị mệnh đề có kiểu + 3 trạng thái (A, B, D) | Không | Không | **VSPS đóng gói lại** |
| Cổng cấu trúc, logit verifier, box OWLv2 | Là sửa lỗi VSPS | Không | Kỹ thuật, thuộc P0 |
| Tiền nghiệm KG một chiều | Không (luật trần) | Thấp | Kỹ thuật |
| Lùi IsA cho thực thể | Một phần (VSPS chỉ làm giới tính) | Trung bình (Conformal Factuality, CLC chỉ cho văn bản) | **Phần khác biệt chính của P2** |
| Thang vị từ cho quan hệ | Có (VSPS nói không làm được) | Trung bình-thấp | Phần khác biệt chính (cần đo riêng) |
| Graph-then-caption SFT | Có | Thấp (CCoT, SaGe) | Ablation |
| GEPA | Có (VSPS: DPO thất bại) | Thấp-trung bình (HALVA, SceneAlign) | Chỉ claim nếu thắng A2 |
| Reward phụ thuộc cha–con | Có | Thấp (2604.01460) | Ablation tùy chọn |
| Mô-đun văn hóa có cổng | Có | Trung bình (RAVENEA, CulturalGround) | Phụ |
| Gold SG tiếng Việt (ảnh đời sống, caption chi tiết) | Có | Trung bình-cao (VietSGG chỉ thể thao) | **Mới thật (tài nguyên)** |
| Bộ phán xét người cho caption tiếng Việt | Có | Cao (chưa thấy, cần quét lại) | **Mới thật (tài nguyên)** |
| M1 với gold mang trạng thái | Có | Trung bình | Metric chính của P1 |

**Trả lời câu hỏi salami.** ViHG-Cap ở dạng hiện tại **không tách được** khỏi VSPS. Khoảng 60% sơ đồ (A, B, D) là VSPS. Phần còn lại là VSPS future work cộng các kỹ thuật đã công bố (HALVA, CCoT, 2604.01460). Một reviewer đã đọc VSPS (bài có repo công khai, có tên tác giả) sẽ viết đúng câu "incremental extension of the authors' prior work".

## 5. Bộ đóng góp và thí nghiệm tối thiểu còn đứng được

**P2 (ACM MM hoặc hạ xuống TOMM).** Một claim: *kiểm soát độ cụ thể có kiểm chứng*. Node/cạnh UNCERTAIN được lùi theo cây IsA và thang vị từ, ngay trong dữ liệu SFT, để lấy lại độ đầy đủ mà VSPS đã mất nhưng không mất độ trung thực.
- Bảng 1 (bắt buộc): VSPS (đã kèm sửa lỗi P0) so với ViHG-Cap, cùng verdict, cùng ngân sách, chỉ khác toán tử lùi. Ba nhánh: xóa / giữ nguyên / lùi IsA / lùi IsA + vị từ. Metric: CHAIR-vi, object P/R, H-R, người chấm (trung thực, đầy đủ), 3 seed, CI.
- Bảng 2 (baseline ngoài): zero-shot có prompt "dùng từ chung khi không chắc". Lùi hậu kỳ không cần huấn luyện (kiểu conformal factuality, trên caption zero-shot). LLM tự viết chung hơn (kiểu CLC), để kiểm tra giá trị của cây IsA. HALVA/DPA. RLAIF-V-7B. Một baseline reward scene graph (kiểu SC-Captioner), nếu ngân sách GPU cho phép.
- Bảng 3: một bộ tiếng Anh (COCO Karpathy test 5.000 ảnh như VSPS đã làm, cộng một bộ caption chi tiết) để chứng minh phương pháp không chỉ hợp với tiếng Việt.
- Ablation (không claim): graph-then-caption, G0/G1/G2 + đồ thị xáo trộn, GEPA so với A2, reward phụ thuộc so với reward phẳng.
- Cổng T5 (F6).

**P1 (EMNLP, track tài nguyên / Findings).** (1) Gold SG tiếng Việt 500 ảnh, gợi ý từ hệ không thuộc VSPS, có đo mức neo. (2) Bộ phán xét người cho caption tiếng Việt, có ≥ 2 hệ không thuộc VSPS. (3) M1 (kèm chế độ H-R), so với: dịch → DiscoSG/SPICE, PoSh trên bản dịch, VLM-judge, CIDEr. Mọi τ được báo lại sau khi bỏ caption VSPS/ViHG-Cap. (4) Parser chỉ claim nếu qua luật +3 F1. Bỏ M5/M6 khỏi P1.

---

## 6. Kế hoạch đã làm đúng (ngắn)

- Đã tự hạ đúng các mảng bão hòa: bơm KG vào generator, graph token, encoder nhận biết quan hệ. Đã liệt kê các claim "không được dùng" (VietSGG, verifier 63,1%).
- Có đối chứng đồ thị xáo trộn và các luật dừng (T0–T4). Luật +3 F1 cho parser là trung thực.
- Có biện pháp chống vòng lặp tự phục vụ ở meta-eval (bỏ caption VSPS rồi báo lại). Chỉ còn thiếu biện pháp tương tự ở phía gold.
- Đã đúng khi đặt tính mới ở *chuỗi* chứ không ở từng mảnh. Chỉ có điều, phần đầu của chuỗi chính là bài trước của nhóm.
