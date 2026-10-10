# 11. Ảo giác quan hệ và tính nhất quán thường thức: phát hiện, giảm thiểu, và một thành phần cho caption tiếng Việt

Agent 11, ngày 2026-10-10. Góc nhìn: relation hallucination và commonsense consistency (2025-2026). Câu hỏi: các bài gần đây phát hiện lỗi quan hệ thế nào, và một KG (ConceptNet / Wikidata / prior quan hệ của Visual Genome) có gắn cờ được quan hệ phi lý không? Từ đó thiết kế một thành phần phát hiện + giảm ảo giác quan hệ cho caption tiếng Việt.

Nguồn: trang arXiv `arxiv.org/abs/<id>` (mở trực tiếp từng ID, đọc title/date/comments/abstract), WebSearch để tìm ứng viên. Hôm nay arXiv API (`export.arxiv.org`) trả rỗng, Semantic Scholar và OpenAlex trả 429, DBLP chặn bot, ConceptNet API trả 502. Mọi venue dưới đây lấy từ trường *comments* hoặc *journal-ref* của trang arXiv, trừ khi ghi khác.

---

## 0. Chẩn đoán từ repo (đọc trước, vì nó đổi hướng thiết kế)

Tôi đếm lại toàn bộ 3.701 bản ghi stage-1 (`data/stage1_records/stage1_records.tar.gz`, chỉ CPU, không gọi mô hình).

**0.1. Con số "relation precision ~30%" đến từ đâu.** Trong repo có hai con số, không phải một:
- Audit người (`data/annotations/audit/tn.json`): chỉ **7** mệnh đề relation mà máy cho SUPPORTED. Người đánh giá 3 SUPPORTED, 3 REJECTED, 1 UNCERTAIN, tức precision 3/7 ≈ 43% và tỉ lệ bị bác 42,9% (con số reviewer R2-1 trích). Với n = 7, khoảng tin cậy rất rộng, không dùng làm số chính được.
- `scripts/relation_backoff.py` (KE_HOACH_Q2, Kết luận 3): object **mới** lấy từ relation/spatial UNCERTAIN có precision 31,9% (mức lenient) đến 38,3% (mức strict). Con số "~30%" trong brief khớp với dòng này.
Cả hai đều nói một điều: kênh quan hệ hiện tại cho bằng chứng yếu.

**0.2. Gần một nửa mệnh đề relation hỏng ngay từ lúc dựng, trước khi verifier chạy.** Phân loại bằng heuristic trên `predicate.lemma_vi` và `text_vi`:

| Nhóm (relation, n = 21.406) | n | SUPPORTED | UNCERTAIN | REJECTED |
|---|---|---|---|---|
| Vị từ phủ định ("không cầm, mặc, đẩy xe máy") | 5.103 (23,8%) | 0,2% | 43,1% | 56,8% |
| Vị từ chứa luôn tân ngữ ("đang đẩy một chiếc thuyền" + object "Hai chiếc thuyền") | 6.818 (31,9%) | 2,2% | 62,0% | 35,8% |
| Lời nói meta ("không có thông tin cụ thể về mối quan hệ", "trong ảnh") | 2.659 | 0,4% | 58,9% | 40,7% |
| Chủ thể và tân ngữ cùng danh từ đầu | 886 | 4,2% | 75,4% | 20,4% |
| **Có vẻ đúng dạng** | 11.767 (55,0%) | 4,0% | 78,9% | 17,1% |

(Các nhóm chồng lên nhau, nên tổng cột n lớn hơn 21.406.)

- Mệnh đề phủ định sinh ra câu hỏi phủ định kép. Ví dụ thật trong bản ghi: `"Có đúng là một người phụ nữ KHÔNG không cầm, mặc, đẩy xe máy hai chiếc xe máy không"`. Probe kiểu này không đo được gì.
- `text_vi` ghép cụm danh từ tân ngữ vào cuối câu đã đầy đủ ("…đang ngồi trên một chiếc thuyền Hai chiếc thuyền"). Cả 7 mục relation trong audit người đều có dạng này (ví dụ "một chiếc thuyền khác một chiếc thuyền khác", "bốn người mặc trang phục đi biển một bầu trời"). Tức là audit 42,9% đang chấm phần lớn **lỗi tuyến tính hóa**, chưa chấm khả năng nhìn quan hệ.
- Trong 655 relation được SUPPORTED, 185 (28,2%) thuộc các nhóm hỏng ở trên.

**0.3. Kênh hình học có code nhưng chưa bao giờ chạy.** `rescap/pipeline/verify.py` đã có `geometric_check()` (test bbox cho bên_trái/bên_phải/trên/dưới/trong…, có dead-band, trả `None` cho quan hệ phụ thuộc độ sâu). Nhưng **0/28.912** entity có bbox (entity do Qwen2.5-VL liệt kê, không qua detector). Vì vậy `geometric.checks_passed/failed` rỗng ở cả 48.201 mệnh đề relation + spatial, `geometric_check.consistent = None` ở cả 26.795 spatial. Đó là lý do **0 spatial nào được SUPPORTED**. Với spatial, nút thắt là thiếu box, không phải thiếu tri thức.

**0.4. Vị từ phổ biến** (đầu vị từ): relation có "đang" 8.075, "không" 4.827, "mặc" 2.415, "đẩy" 378, "cầm" 289. Spatial có "trên" 7.545, "bên cạnh" 6.350, "phía sau" 3.103, "phía trước" 2.062, "gần" 1.967, "dưới" 1.510, "trong" 1.499. Khoảng 70% spatial (trên, dưới, trong, bên cạnh, gần, trái/phải) quyết định được bằng box 2D. "Phía trước/sau" (khoảng 19%) cần độ sâu.

**Hệ quả cho thiết kế:** thứ tự đúng là (1) sửa cấu trúc, (2) bật hình học, (3) rồi mới dùng KG. KG đặt trước hai bước kia sẽ chỉ đi lọc rác.

---

## 1. Bài liên quan (đã mở trang arXiv)

### 1.1 Benchmark / đánh giá ảo giác quan hệ
| # | Bài | Venue (nguồn) | ID | Cách phát hiện lỗi quan hệ | Bài học cho VSPS |
|---|---|---|---|---|---|
| 1 | **Reefknot** (K. Zheng et al.) | Findings ACL 2025 (comments) | 2408.09429 | Hơn 20K mẫu dựng từ bộ ba scene graph Visual Genome. Định nghĩa ảo giác quan hệ theo hai mặt perceptive / cognitive. Giảm thiểu dựa trên confidence (Detect-then-Calibrate), giảm trung bình 9,75% trên 3 bộ. | Phát hiện bằng **confidence của token trả lời**. VSPS chưa có logprob (Vintern `supports_logprobs=False`), nên phải bật logprob hoặc dùng Qwen làm verifier phụ. |
| 2 | **Tri-HE** (J. Wu, T. T. Chung, K. Chen, D.-Y. Yeung) | TMLR 2025 (comments) | 2410.23114 | Trích bộ ba (object, relation, object) từ câu trả lời, so với scene graph của ảnh bằng NLI hoặc GPT-4 judge. Kết luận: ảo giác quan hệ **nặng hơn** ảo giác object. Có phương pháp giảm thiểu không cần huấn luyện. | Dùng định nghĩa triple-level của Tri-HE cho metric tiếng Việt. Mệnh đề VSPS đã ở dạng triple, chỉ cần tuyến tính hóa đúng. |
| 3 | **CDH-Bench** (K. Chen et al.) | arXiv 2026-03 | 2603.27982 | 300 cặp ảnh thường thức / phản thực tế, gồm ba chiều: lỗi đếm, lỗi quan hệ, lỗi thuộc tính. Đo CF-Acc, CS-Acc, CFAD, CCR, RPD. Mô hình mạnh vẫn "sụp" về đáp án thường thức khi ảnh trái thường thức. | **Cảnh báo trực tiếp cho KG**: prior thường thức chính là nguồn gây ảo giác. KG không được dùng làm bằng chứng ủng hộ. |
| 4 | **HalDec-Bench** (K. Saito et al.) | arXiv 2026-03 (thay cho 2511.20515) | 2603.15253 | Benchmark cho **bộ phát hiện** ảo giác trong caption: caption từ nhiều VLM, nhãn người theo loại và theo đoạn. Phát hiện: detector có xu hướng cho câu ở **đầu** response là đúng, bất kể đúng sai thật. | Bằng chứng rằng VLM-as-detector có thiên lệch hệ thống. Ủng hộ việc thêm kênh không-VLM (hình học, prior). |
| 5 | **InstaBind-Lite / DSCAM** (Y. Xu et al.) | arXiv 2026-08 | 2608.16805 | Gán nhầm thuộc tính cho instance cùng lớp bên cạnh. 524 ảnh, 9.580 câu hỏi. Misbinding rate trung bình 19,84% (mã nguồn mở) và 7,55% (API). Khoảng 81% lỗi đến từ instance kề bên. | VSPS có `dan_ong_1`, `dan_ong_2`… nhưng không có box, nên không kiểm được binding theo instance. |
| 6 | **CAPTURe** (A. Pothiraj et al.) | ICCV 2025 (comments) | 2504.15485 | Đếm object bị che, nối đếm với suy luận không gian. | Counting là loại tệ nhất trong audit VSPS (human SUPPORTED 55,9%). |
| 7 | **Synthetic Visual Genome** (J. S. Park et al.) | CVPR 2025 (comments) | 2506.07643 | Theo kết quả tìm kiếm (chưa đọc full text): luật hình học cho các spatial relation phổ biến, khớp 95,1% với VG. Quan hệ chức năng thì dùng VQA có/không + CLIP trên crop. | Chính là mẫu "luật hình học trước, VLM sau" cho VSPS. |
| bg | R-Bench (M. Wu et al.), ICML 2024 (comments), 2406.16449 | | | Ba kiểu đồng xuất hiện gây ảo giác (relation-relation, subject-relation, relation-object). LVLM bỏ qua ảnh và dựa vào commonsense của LLM. | Ủng hộ việc dùng prior KG làm **giả thuyết rỗng** cần bác bỏ, không dùng làm bằng chứng. |
| bg | MMRel (J. Nie et al.), 2406.09121, v3 sửa 12/2025, chưa thấy venue | | | 22,5K QA, khoảng 400 quan hệ, có tập đối kháng "quan hệ rất bất thường". | Tập con "bất thường" là mẫu cho tập low-prior tiếng Việt. |

### 1.2 Giảm thiểu ảo giác quan hệ (2025-2026)
| # | Bài | Venue | ID | Cơ chế | Dùng được trên 3090? |
|---|---|---|---|---|---|
| 8 | **ChainMPQ** (Y. Wu et al.) | ICLR 2026 (comments) | 2510.06292 | Tách subject / object / relation thành câu hỏi đa góc nhìn, xâu chuỗi ảnh-văn bản có bộ nhớ, không huấn luyện. | Có. Nhưng nhân số lượt gọi lên 3 lần. Bản rút gọn kiểu DSG (subject ∧ object rồi mới hỏi relation) rẻ hơn. |
| 9 | **RVE: Relation-aware Visual Enhancement** (Z. Qin et al.) | arXiv 2026-05 | 2605.11808 | Điểm ARS chọn attention head nhạy với action-relation, định vị vùng ảnh, tăng attention vào đó. Thử trên MMRel, R-Bench, AMBER. | Cần can thiệp attention. Vintern/Qwen làm được nhưng tốn công kỹ thuật, ngoài trọng tâm. |
| 10 | **Geo3R** (M. Wang et al.) | ACM MM 2026 (comments) | 2607.21085 | Spatial reasoning hallucination là một nhánh con của relation hallucination. Thêm bằng chứng hình học/3D vào suy luận, không huấn luyện. | Ý tưởng dùng được cho "phía trước/sau" (khoảng 19% spatial của VSPS) bằng depth model. |
| 11 | **Predicting When to Trust VLMs for Spatial Reasoning** (M. Imran et al.) | arXiv 2026-01 | 2601.11644 | GroundingDINO lấy box, so tâm box với lời VLM nói, gộp 4 tín hiệu bằng gradient boosting (705 mẫu train). AUROC 0,674 trên BLIP-2. | Rất gần thứ VSPS cần: một bộ ước lượng tin cậy nhỏ, train trên vài trăm nhãn audit. |
| 12 | **RelCheck** (S. Patil et al.) | arXiv 2026-08 | 2609.27890 | Visual KB gồm bộ ba RelTR, vị từ không gian từ bbox và claim kiểu Woodpecker, rồi viết lại câu. | Đối thủ gần nhất về "dual evidence". Khác VSPS: hậu xử lý caption, không làm dữ liệu giám sát. |
| 13 | **When Relations Break** (P. W. Shin et al.) | arXiv 2026-05 | 2605.05045 | Xoay và nhiễu nhẹ làm suy giảm mạnh suy luận quan hệ. | Có thể dùng làm stress test rẻ (xoay ảnh rồi hỏi lại). |

### 1.3 KG / prior thường thức để kiểm tra tính hợp lý của quan hệ
| # | Bài | Venue | ID | Cách dùng tri thức | Ghi chú |
|---|---|---|---|---|---|
| 14 | **Visual Commonsense Driven Knowledge Refinements for SGG** (M. Neau et al.) | arXiv 2026-06 | 2606.06369 | Tự khai thác ràng buộc thường thức (không gian, chức năng, định tính) từ dữ liệu train, dùng suy luận khai báo để sửa và xếp hạng lại dự đoán SGG lúc inference. Không viết luật tay, không train lại. | Bằng chứng rằng "prior quan hệ khai thác từ VG làm bộ lọc" chạy được. Nhưng đây là SGG, chưa phải caption LVLM. |
| 15 | **Hallucinate, Ground, Repeat** (S. Vellamcheti et al.) | arXiv 2025-06 | 2506.05651 | LLM đề xuất vị từ hợp lý cho cặp object (prior), mô hình thị giác grounding lại theo vòng kiểu EM. | Cùng thông điệp: prior = **điều có thể đúng**, phải grounding mới thành **điều đúng**. |
| 16 | **CutPaste&Find** (C.-D. Nguyen et al.) | arXiv 2025-02 | 2502.12591 | Visual-aid KB lưu quan hệ entity-attribute kèm ảnh mẫu, phát hiện ảo giác không cần gọi LVLM. | KB dạng ảnh có thể thay KG văn bản khi ConceptNet thiếu tiếng Việt. |
| 17 | **A Study of Commonsense Reasoning over Visual Object Properties** (A. Kolari et al.) | arXiv 2025-08 | 2508.10956 | Đánh giá suy luận thường thức về thuộc tính vật thể. | Nền cho thuộc tính phi lý ("chó màu xanh lá"). |
| bg | VideoHallu (Z. Li et al.), NeurIPS 2025 (journal-ref), 2505.01481 | | | Video tổng hợp vi phạm vật lý/thường thức. Mô hình không phát hiện được vi phạm. | Chỉ là nền cho "physical plausibility". |
| bg | Survey multimodal hallucination evaluation & detection (Z. Chen et al.), 2507.19024 | | | Định nghĩa commonsense hallucination. | Trích phần định nghĩa. |

### 1.4 Đa ngữ / tiếng Việt
- MHR (2408.00550, 2024): ảo giác LVLM nặng hơn khi hỏi bằng ngôn ngữ không phải tiếng Anh (POPE 13 ngôn ngữ). Chỉ object, không có quan hệ.
- DSC2025 ViHallu (2601.04711): hallucination tiếng Việt, nhưng chỉ cho **LLM văn bản**.
- **Chưa thấy** benchmark hay phương pháp nào cho ảo giác quan hệ trong caption/VQA tiếng Việt (WebSearch hôm nay; các agent 04 và 17 cũng không thấy).

---

## 2. Trả lời câu hỏi: KG có gắn cờ quan hệ phi lý được không?

**Được, nhưng chỉ theo một chiều, và chỉ sau khi đã có hình học.**

1. **Chiều đúng (low prior → đòi thêm bằng chứng).** Bộ ba gần như không bao giờ xuất hiện trong VG hoặc mâu thuẫn với ConceptNet (`người – ăn – xe máy`, `thuyền – trên – mái nhà`) gần như chắc là lỗi khi ảnh là ảnh đời thường (KTVIC, UIT-OpenViIC). Bài 14 cho thấy loại ràng buộc này sửa được dự đoán SGG.
2. **Chiều sai (high prior → coi là đúng).** R-Bench và CDH-Bench cho thấy LVLM ảo giác **chính vì** quan hệ hợp lý: "người cầm vợt" trên sân tennis được nói ra dù không ai cầm. Nếu prior cao được tính là bằng chứng ủng hộ, KG sẽ khuếch đại đúng kiểu lỗi mà verifier đang mắc (yes-bias, 63,1% precision).
3. **Ảnh phản thực tế.** Nếu low prior bị REJECTED thẳng, các quan hệ hiếm nhưng thật sẽ mất (kiểu CDH). Vì vậy low prior chỉ hạ xuống **UNCERTAIN** (không vào SFT), không bao giờ REJECTED, trừ khi hình học bác bỏ.

Từ đó, vai trò hợp lý của KG là **giả thuyết rỗng có hiệu chỉnh**: mức bằng chứng thị giác cần có phụ thuộc vào prior. Bằng chứng phải vượt mức prior (ví dụ P(yes | ảnh) − P(yes | ảnh trắng) > δ, theo Post-Hoc Debias đã ghi ở research_wall/06). Low prior thì phải có thêm bằng chứng hình học.

**Độ phủ tài nguyên (thực tế cho tiếng Việt):**
- Prior VG: không có nhãn tiếng Việt. Phải map danh từ đầu tiếng Việt sang lớp VG/COCO. `rescap/chair.py` + `rescap/vi/lexicon.py` đã có lexicon object tiếng Việt cho CHAIR, có thể mở rộng thành bảng vi→en. Vị từ tiếng Việt (đang cầm, cưỡi, đẩy, mặc, ở trên…) cần một bảng map tay khoảng 50-80 vị từ, phủ phần lớn tần suất ở §0.4.
- ConceptNet: API 502 hôm nay, độ phủ tiếng Việt **chưa xác minh**. Nên dùng qua khái niệm tiếng Anh sau khi map, hoặc dùng dump offline.
- Wikidata: có nhãn `vi`, nhưng gần như không có quan hệ thị giác (affordance/không gian). Chỉ hữu ích cho phân cấp IsA (hypernym), không dùng để kiểm quan hệ.

---

## 3. Thiết kế: ViRelGuard, một thành phần phát hiện + giảm ảo giác quan hệ cho VSPS

Bốn tầng, xếp từ rẻ đến đắt. Mỗi tầng chỉ được **hạ** một verdict (SUPPORTED → UNCERTAIN → REJECTED), trừ tầng hình học, là tầng duy nhất được nâng. Như vậy không tầng nào có thể đưa thêm ảo giác vào dữ liệu SFT.

### T0. Cổng cấu trúc (CPU, quyết định, khoảng 1 ngày code)
- Tuyến tính hóa lại từ các trường của triple (`subject.text_vi` + động từ + `object.text_vi`), **không** dùng `text_vi` do LLM viết. Cắt cụm tân ngữ đã lọt vào `predicate.lemma_vi`.
- Bộ ba có vị từ phủ định ("không …"): không phải mệnh đề quan hệ. Bỏ hẳn, hoặc chuyển thành "absence claim" riêng (giữ cho NegBench-style probe, không vào SFT).
- Bỏ lời nói meta ("không rõ", "không có thông tin", "trong ảnh"), self-loop, và cặp cùng danh từ đầu mà không phân biệt được instance.
- Kiểm nhất quán số lượng giữa mệnh đề: object "Hai chiếc thuyền" nhưng vị từ nói "một chiếc thuyền" → mâu thuẫn, hạ cả hai về UNCERTAIN. Kiểm này miễn phí, dùng trường `number` của entity.
- Tác động đo được ngay trên dữ liệu có sẵn: khoảng 45% relation bị loại hoặc sửa. Đây là phần trả lời trực tiếp cho R2-1 ("relation không nhất quán") mà **không cần GPU**.

### T1. Kênh hình học (GPU nhỏ, khoảng 3-5 ngày)
- Grounding DINO-T hoặc OWLv2 lấy box cho từng entity (query bằng nhãn tiếng Anh đã map). Ghi vào `entities[*].bbox` để `geometric_check()` có sẵn chạy được. Đây cũng chính là B3/C4 trong KE_HOACH_Q2.
- Luật DSG: relation chỉ được xét khi **cả hai đầu** có box với điểm detector ≥ τ (chọn τ trên `data/object_gold`). Thiếu một đầu → UNCERTAIN.
- Spatial 2D (trên/dưới/trong/trái/phải): geometric_check quyết định. Thêm test cho "gần"/"bên cạnh" (khoảng cách mép box chia đường chéo ảnh, có dead-band). "Phía trước/sau": để UNCERTAIN, hoặc thêm Depth Anything làm tùy chọn (kiểu Geo3R), coi như mở rộng sau.
- Instance binding: với nhiều instance cùng lớp, gán thuộc tính/quan hệ vào đúng box (theo hướng InstaBind-Lite). Hỏi VLM trên crop của box đó.

### T2. Cổng prior KG bất đối xứng (CPU, khoảng 1 tuần kể cả map từ vựng)
- Prior: `π(p | s, o)` đếm từ quan hệ Visual Genome (làm mượt Laplace, gộp vị từ đồng nghĩa), cộng cạnh ConceptNet `CapableOf/UsedFor/AtLocation/ReceivesAction` để bù cặp mà VG chưa có.
- Luật:
  - π thấp (dưới phân vị 5% của các bộ ba VG có cùng cặp lớp) và không có xác nhận hình học → **UNCERTAIN** (flag "implausible"). Không bao giờ REJECTED chỉ vì prior.
  - π cao → **vùng rủi ro ngôn ngữ**: chỉ SUPPORTED nếu bằng chứng vượt baseline ảnh trắng: `P(yes | ảnh) − P(yes | ảnh trắng) > δ`, hoặc tỉ lệ có/không trong K mẫu tương đương nếu không có logprob.
  - π trung bình → giữ luật cũ.
- Đây là điểm mới chính (xem §4): KG không cấp bằng chứng mà **đặt ngưỡng** bằng chứng.

### T3. Probe VLM phân rã trên vùng (GPU, dùng lại verifier)
- Hỏi trên crop của hộp hợp subject ∪ object (kèm viền), không hỏi trên ảnh đầy đủ. Ba câu theo thứ tự cha-con (kiểu ChainMPQ/DSG): subject có không → object có không → quan hệ. Cha sai thì dừng, tiết kiệm lượt gọi.
- Chỉ áp cho relation chức năng/hành động (cầm, đẩy, cưỡi, mặc…) mà hình học không quyết định được.

### Giảm thiểu (dùng kết quả T0-T3)
1. **Phía dữ liệu giám sát (chính).** Chỉ relation qua được T0-T3 mới vào SFT. Relation thất bại thì **lùi theo thang vị từ** thay vì bỏ: "đang cưỡi" → "ở trên" (nếu hình học xác nhận) → "ở gần" → chỉ giữ hai entity (D2 hiện có). Đây là bản quan hệ của trung tính hóa theo IsA (ý 2b trong research_wall/11). Thang khoảng 30 vị từ, viết tay một lần.
2. **Cặp âm cho DPO (tùy chọn).** Từ relation đã SUPPORTED, sinh caption bị lỗi bằng cách đảo subject/object, thay vị từ bằng vị từ hay nhầm theo VG, hoặc thay bằng vị từ có π cao nhưng hình học bác. Dùng làm rejected. Rẻ vì không gọi mô hình.
3. **Hậu xử lý lúc suy luận.** Chỉ làm baseline so sánh với RelCheck. Không nên làm đóng góp chính vì RelCheck đã có.

### Metric và benchmark đi kèm
- **ViRel-P / ViRel-R**: precision/recall cấp bộ ba theo định nghĩa Tri-HE, tách theo nhóm (spatial-2D, spatial-depth, action, possession/wearing). Tham chiếu là scene graph đã kiểm của ảnh (ý 1 ViVSG trong research_wall/11).
- **Prior Dependency Gap (PDG)**: lấy precision ở bộ ba π cao trừ precision ở bộ ba π thấp, đo trên caption của mô hình. Đây là bản caption mở và tiếng Việt của RPD trong CDH-Bench. PDG lớn nghĩa là mô hình nói theo prior.
- **Mini-benchmark ViRel-300**: 300 ảnh KTVIC/UIT-OpenViIC, mỗi ảnh khoảng 5 bộ ba người gán (subject, vị từ, object, box), cộng một tập con khoảng 60 ảnh có quan hệ low-prior thật (kiểu MMRel tập đối kháng). Tốn khoảng 2 tuần cho 2 người.

---

## 4. Đánh giá: Novelty / Overlap / Feasibility

| Thành phần | Overlap (2025-2026) | Novelty | Feasibility (RTX 3090) | Ghi chú |
|---|---|---|---|---|
| T0 cổng cấu trúc + nhất quán số lượng | Không có bài tương ứng, vì đây là sửa lỗi pipeline | **Thấp** (kỹ thuật) | **Rất cao**, 0 GPU | Bắt buộc làm trước. Không quảng bá như đóng góp, chỉ báo cáo "45% relation hỏng khi dựng" trong phần phân tích lỗi. |
| T1 hình học + luật hai đầu | RelCheck, 2601.11644, SVG (CVPR 2025), Geo3R | **Thấp-trung bình** | **Cao**: detector khoảng 2 GB VRAM, 3.701 ảnh chạy được trong vài giờ | Mới chỉ ở chỗ áp cho mệnh đề tiếng Việt và cho dữ liệu SFT. |
| T2 prior KG bất đối xứng (prior đặt ngưỡng, không làm bằng chứng) | Gần: bài 14 (refine SGG bằng ràng buộc thường thức), R-Bench và CDH-Bench (chẩn đoán prior), Post-Hoc Debias. **Chưa thấy** bài dùng prior KG để đặt ngưỡng bằng chứng một cách bất đối xứng trong kiểm chứng mệnh đề caption | **Trung bình**, là đóng góp phương pháp mạnh nhất của file này | **Cao** về GPU, **trung bình** về công sức (map vi→VG/ConceptNet) | Rủi ro: lợi ích nhỏ nếu sau T0+T1 còn ít relation. Phải chứng minh bằng PDG giảm và precision audit tăng. |
| T3 probe phân rã trên vùng | ChainMPQ (ICLR 2026), DSG | **Thấp** | Cao, nhưng tăng số lượt gọi | Chỉ cho relation hành động. |
| Thang lùi vị từ | Gần: D2 relation→entity, trung tính hóa IsA. Chưa thấy "predicate back-off lattice" cho dữ liệu giám sát | **Trung bình-thấp** | Rất cao | Hợp làm ablation. |
| PDG + ViRel-300 | Tri-HE, Reefknot, CDH-Bench, MMRel (tất cả tiếng Anh) | **Trung bình** cho tiếng Việt (chưa có benchmark quan hệ tiếng Việt), thấp về khái niệm | Trung bình (công gán nhãn) | Nguy cơ có nhóm khác dịch Reefknot sang tiếng Việt (xem 17_novelty_redteam). |

**Kết luận gộp:** riêng thành phần này không đủ làm một bài phương pháp độc lập. Nó hợp làm **mô-đun thứ hai** trong bài KG-VSPS hoặc bản Q2: "tri thức có cấu trúc dùng như prior để hiệu chỉnh kiểm chứng, không phải để sinh". Câu chuyện đó vừa đứng được trước CDH-Bench/R-Bench, vừa sửa thật lỗi R2-1.

---

## 5. Kế hoạch thử (theo thứ tự, có điều kiện dừng)

1. **(0 GPU, 1-2 ngày)** Viết T0 cạnh `scripts/relation_audit.py`. Báo cáo lại bảng §0.2 sau khi sửa. Dựng lại SFT và đếm số relation còn lại trong 25.322 mệnh đề được chọn. *Dừng nếu* sau T0 còn < 200 relation SUPPORTED: khi đó relation không đáng đầu tư thêm cho bài hiện tại, chỉ trả lời reviewer bằng T0.
2. **(audit, 2-3 ngày)** Audit **≥ 150** relation (thay cho n = 7): 50 mẫu từ mỗi nhóm SUPPORTED / UNCERTAIN / REJECTED sau T0, tuyến tính hóa sạch. Ước lượng precision thật của kênh quan hệ. Mọi con số "~30-43%" hiện tại đều trộn lỗi dựng câu.
3. **(GPU nhỏ, 3-5 ngày)** T1 với Grounding DINO. Đo spatial SUPPORTED từ 0 lên bao nhiêu, và precision trên mẫu audit. Hiệu chỉnh τ trên `data/object_gold`.
4. **(CPU, 1 tuần)** T2: bảng map vị từ + danh từ, đếm prior VG. Ablation: không prior / prior đối xứng (cộng điểm) / prior bất đối xứng. Giả thuyết cần thấy: bản đối xứng **làm tăng** PDG và hạ precision, bản bất đối xứng làm ngược lại. Nếu đúng, đây là phát hiện đáng báo cáo.
5. **(tùy chọn)** Cặp âm DPO từ thang vị từ. ViRel-300 nếu đi theo hướng bài benchmark.

Ngân sách GPU tổng: dưới 1 ngày GPU trên 3090 (detector + probe lại khoảng 500 relation còn lại sau T0), chưa tính SFT lại.

---

## 6. Chưa xác minh / hạn chế
- Venue của MMRel: arXiv v3 (12/2025) không ghi venue. Không trích như "ICML".
- Chi tiết SVG (luật 95,1%, ngưỡng CLIP 0,3) lấy từ kết quả tìm kiếm, chưa đọc full text. Chỉ ghi chắc chắn "CVPR 2025" (comments arXiv).
- Số liệu RelCheck lấy từ file 04 của cùng đợt, tôi không mở lại full text.
- Độ phủ tiếng Việt của ConceptNet: API 502 hôm nay. Dung lượng dump ConceptNet 5.7 chưa kiểm.
- Heuristic §0.2 là regex trên chuỗi, có thể đếm sai một ít. Ví dụ "không" ở giữa vị từ hợp lệ, hoặc vị từ hợp lệ chứa danh từ đầu của tân ngữ ("mặc áo" với object "áo"). Phải kiểm tay 100 mục trước khi đưa số vào bài.
- Phân vị 5% cho "low prior" và δ cho prior-subtraction là giá trị đặt trước, chưa hiệu chỉnh.
- Chưa tìm thấy bài 2025-2026 nào dùng prior KG theo đúng kiểu bất đối xứng ở T2. Đây là kết quả của một lượt WebSearch và tra arXiv theo ID, không phải quét hệ thống (arXiv API, S2 và OpenAlex đều không truy cập được hôm nay). Cần chạy lại truy vấn S2/OpenAlex `"relation hallucination" AND (prior OR "knowledge graph" OR commonsense)` trước khi viết câu "đầu tiên".
