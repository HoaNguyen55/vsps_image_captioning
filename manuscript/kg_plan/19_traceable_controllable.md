# 19. Truy vết và điều khiển caption bằng đồ thị: "graph-controllable, span-traceable Vietnamese captioning"

Ngày: 2026-10-10. Agent KG-plan 19. Nguồn: arXiv API (`export.arxiv.org`, truy vấn `abs:` và `id_list`, mở abstract từng bài), trang abs arXiv (WebFetch cho FoCUS, PANORAMA), WebSearch để dò. OpenAlex và Semantic Scholar trả 429 suốt phiên, nên **venue chỉ lấy theo comment arXiv** khi có; bài không có comment thì ghi "arXiv". Số liệu VSPS ở mục 1 tôi đo trực tiếp trên `data/stage1_records/stage1_records.tar.gz` trong phiên này.

**Trả lời ngắn.**
- Từng mảnh riêng lẻ đều **đã có người làm** trong 2025-2026 (tiếng Anh). Gắn cụm từ với vùng ảnh: GroundCap, COCONut-PanCap, DenseWorld-1M, PANORAMA. Điều khiển caption bằng thành phần scene graph: FoCUS (EMNLP 2026), SGDiff (AAAI 2025). Kiểm chứng và định vị lỗi caption: GAVEL. Trích dẫn bằng chứng thị giác: FinRAGBench-V, CiteVQA-attribution.
- **Phần còn trống là tổ hợp:** (i) mỗi span trỏ tới một **nút mệnh đề đã kiểm chứng 3 trạng thái** (không chỉ trỏ tới box); (ii) người dùng **sửa đồ thị** (giữ, bỏ, tập trung, bật hedge) rồi caption sinh lại, với đảm bảo theo cấu tạo cho bộ render ký hiệu và đo được cho mô hình học; (iii) làm cho **tiếng Việt**, nơi chưa có grounded captioning, controllable captioning hay mô tả ảnh cho người khiếm thị (truy vấn arXiv 2025-2026 ra 0 bài).
- Mức mới: **MED** (mới ở mức tổ hợp, không mới ở mức cơ chế).
- Mức hữu ích: **cao cho VSPS**, vì gần như miễn phí: bộ realizer đã sinh provenance theo span. Với accessibility thì **chưa chứng minh được** nếu không có nghiên cứu người dùng.
- Khuyến nghị: đưa vào bản mở rộng Q2 của VSPS làm **đóng góp phụ có metric riêng** (Traceability Rate, Control Accuracy). Chỉ tách thành bài riêng khi làm được bước học (mục 4, chế độ B) và có user study.

---

## 1. VSPS đã có sẵn gì (đo trong phiên)

`rescap/pipeline/realize.py` khai báo bất biến `Facts(C) ⊆ P*`. Bộ planner ký hiệu ghi `proposition_ids` cho từng span, kèm `char_start/char_end`, `span_role`, `is_factual`. Nó cũng có bộ phát hiện `ungrounded_spans`. Đo trên 3.700 bản ghi stage-1:

| Đại lượng | Giá trị |
|---|---|
| Bản ghi có caption | 3.687 / 3.700 |
| Số span trung bình / caption | 5,02 (tổng 18.526 span) |
| Span trỏ tới mệnh đề SUPPORTED / UNCERTAIN / REJECTED | 13.223 / 6.615 / **0** |
| `ungrounded_spans` khác rỗng | **0** ảnh |
| Tỷ lệ ký tự chữ-số được span phủ | trung bình 93,2% (min 66,7%). Phần còn lại là liên từ (`còn có`, `bên cạnh đó`), được miễn theo thiết kế |
| Span `is_factual=true` | 74% (26% là hedge hoặc liên từ đi kèm) |
| `generator` | `template` cho toàn bộ 3.687 caption |

Hệ quả:
1. **Truy vết span → nút đạt 100% theo cấu tạo** ở bộ render ký hiệu. Đây là "traceability guarantee". Nó **không phải** faithfulness guarantee: nó chỉ đúng tương đối so với P\*. Precision SUPPORTED đo trên audit là 63,1%, nên ước tính khoảng 1/3 span "có nguồn" vẫn trỏ tới một mệnh đề sai. Bài phải nói rõ hai khái niệm này và báo cả hai con số.
2. **Entity không có `bbox`** trong stage-1 records (`bbox` xuất hiện 0 lần, verifier ghi `missing bounding box`). Muốn truy vết span → vùng thì phải thêm bộ grounder (mục 4).
3. File `data/supervision_v2/clean/sft.jsonl` chỉ giữ `response` dạng chuỗi, nên **student SFT mất toàn bộ provenance**. Đây là khoảng hở cần lấp nếu muốn traceability ở mô hình đã huấn luyện.
4. `data/object_gold` chỉ có nhãn lớp (không box). Ảnh COCO (UIT-ViIC, probe `coco5000`) có sẵn box COCO, nên dùng được để chấm vùng mà không cần gán nhãn thêm.

---

## 2. Bài liên quan 2025-2026 (đã mở abstract trên arXiv)

### 2.1 Grounded captioning: span ↔ vùng
| Bài | Venue (theo comment arXiv) | arXiv | Điểm chính | So với ý tưởng |
|---|---|---|---|---|
| GroundCap (Oliveira, Teodoro, Martins de Matos) | arXiv (v3 2025-06) | 2502.13898 | Thẻ ID giữ danh tính đối tượng qua nhiều lần nhắc, nối action với object. 52.016 ảnh phim. Metric **gMETEOR** = chất lượng caption + độ chính xác grounding. Fine-tune Qwen2.5-VL-7B | **Gần nhất về định dạng** (thẻ ID nội tuyến). Không có trạng thái kiểm chứng, không có điều khiển, tiếng Anh |
| COCONut-PanCap (Deng et al.) | arXiv (chưa xác nhận venue) | 2502.02589 | Caption vùng gắn mask panoptic, người sửa | Dữ liệu grounding, không có điều khiển hay kiểm chứng |
| DenseWorld-1M (X. Li et al.) | arXiv | 2506.24102 | Pipeline 3 bước: mask → caption từng vật → gộp thành caption dày có quan hệ | Cùng ý "caption ghép từ đơn vị vật thể". Tiếng Anh, không có trạng thái |
| PANORAMA (Pieri, Kazakos, Chen, Sivic, Schmid) | arXiv 2026-09 | 2609.19143 | Benchmark PanoCaps, metric **gPQ** chấm đồng thời văn bản và mask, chọn mask cho từng cụm từ | Chuẩn mới về metric vùng. Nên mượn cách khớp cụm từ-mask |
| Describe Anything / DAM (Lian et al.) | arXiv (venue chưa xác nhận) | 2504.16072 | Caption chi tiết cho vùng người dùng chọn (focal prompt), DLC-Bench không cần caption tham chiếu | Điều khiển theo vùng (đầu vào là mask). Không truy vết ngược span → vùng |

### 2.2 Điều khiển caption bằng scene graph hoặc tín hiệu có cấu trúc
| Bài | Venue | arXiv | Điểm chính | So với ý tưởng |
|---|---|---|---|---|
| **FoCUS** (Hyun, Kim, Kim) | **EMNLP 2026 Main** | 2609.00709 | Prompt điều khiển bằng ngôn ngữ tự nhiên. Caption được parse và căn với object/attr/rel của SG, trọng số có dấu, tối ưu GRPO. Benchmark **SCoPE** với ràng buộc **Include/Avoid** | **Đe dọa lớn nhất về controllability.** Khác biệt: FoCUS điều khiển *trọng tâm ngữ nghĩa* qua prompt. Ở đây điều khiển là *chỉnh sửa tập nút đã kiểm chứng*, và mỗi span có id. Phải dùng giao thức Include/Avoid tương thích SCoPE |
| SGDiff (X. Zhang et al.) | AAAI 2025 (comment: "Accept by AAAI-2025") | 2512.01975 | Box của người dùng → scene graph → nhiều cặp (caption, mask) bằng diffusion | Điều khiển bằng box. Không phải LVLM, không có kiểm chứng |
| SG-FSCFormer (cùng nhóm) | arXiv 2026-03 | 2603.20887 | Bản video của SegCaptioning | Video, bỏ qua |
| Reward-guided decoding cho MLLM (Mañas et al.) | ICCV 2025 | 2508.11616 | Hai reward model (precision/recall object) trộn lúc giải mã. Người dùng chỉnh tỷ lệ precision-recall | Điều khiển "mức độ thận trọng". Có thể làm baseline cho núm "chỉ SUPPORTED vs SUPPORTED+UNCERTAIN" |
| SEA-Cap (Cai et al.) | arXiv 2026-07 | 2607.25789 | Caption cảm xúc với bằng chứng cấp object, kiểm tra ảo giác bằng đa tác tử | Ý "bằng chứng có cấu trúc làm điều khiển". Miền khác |

### 2.3 Kiểm chứng, định vị, trích dẫn bằng chứng
| Bài | Venue | arXiv | Điểm chính | Bài học |
|---|---|---|---|---|
| **GAVEL** (Gao, Hashimoto, Saito) | comment "conference" (chưa rõ) | 2606.26923 | Một task gộp ba việc: kiểm chứng + giải thích + **định vị bằng chứng** cho cặp ảnh-văn. Mô hình đóng vẫn kém | Bản hậu kiểm của "traceability". Ở đây truy vết **lúc sinh**, không phải sau khi sinh |
| Evidence Attribution w/o Coordinates (Liu, Zhang, Xiao) | arXiv 2026-07 | 2607.24651 | "Attribution Hallucination": trả lời đúng nhưng chỉ sai vùng bằng chứng. Trích nguyên văn và tra vị trí sau thì tốt hơn xuất toạ độ | Ủng hộ thiết kế **xuất id nút thay vì toạ độ**, toạ độ tra sau từ nút |
| Hallucinated citations in Video-LLM QA (Y. Kumar) | arXiv 2026-08 | 2608.15574 | Hỏi trực tiếp VLM "khung này có hỗ trợ claim không" bắt được **0%** (0/40 claim) do sycophancy | **Cảnh báo:** trích dẫn tạo ảo giác tin cậy. Có dẫn nguồn ≠ đúng. Phải đo "traced-but-wrong" |
| FinRAGBench-V (Zhao et al.) | arXiv 2025-05 | 2505.17471 | RAG đa phương thức có *visual citation* | Chuẩn trích dẫn ở miền tài liệu |
| ERCR (Liang et al.) | arXiv | 2509.22415 | Attribution token → vùng bằng logit-lens (giải thích nội tại) | Kiểu saliency. Có thể làm baseline "attribution hậu nghiệm" |
| PhaseWin (Gu et al.) | arXiv 2026-06 | 2606.18008 | Tìm tập vùng trung thực nhanh hơn greedy | Tương tự, saliency |
| REVERSE (Wu et al.) | NeurIPS 2025 | 2504.13169 | Gắn nhãn cụm confident/unconfident, backtrack khi suy luận | Đã có trong 00_TONG_HOP. Gần với "hedge hiển thị trong trace" |
| VGD (L. Yang et al.) / SSAV (Ren et al.) | arXiv 2026 | 2607.27823 / 2609.17269 | Kiểm chứng từng object mention lúc giải mã, hoặc bằng ổn định vùng | Kênh bằng chứng vùng cho bước grounding |

### 2.4 Accessibility (người mù, thị lực kém)
| Bài | Venue | arXiv | Điểm chính |
|---|---|---|---|
| Salience-LLaVA (J. Liang et al.) | arXiv 2026-08 | 2608.28218 | Caption xếp đối tượng theo độ quan trọng với người thị lực kém. Bộ Salience COCO/Flickr/VizWiz được người thị lực kém xác nhận |
| Smol-VL-BLV (Choudhary et al.) | EMNLP 2026 (comment) | 2609.28757 | VLM 500M, GRPO với reward hướng, khoảng cách, nguy hiểm |
| Curator-guided multilingual art description (Tsangko et al.) | arXiv 2026-05 (pilot) | 2605.31080 | Qwen2.5-VL-3B + LoRA cho tiếng Đức, Romania, Serbia. LLM-judge hiệu chỉnh theo pilot nhỏ với người khiếm thị |

Cả ba nhóm accessibility đều muốn **ưu tiên và điều khiển nội dung**, nhưng chưa nhóm nào cho người dùng **truy hỏi nguồn gốc từng cụm từ** hay **sửa đồ thị**. Không bài nào có tiếng Việt: truy vấn arXiv `abs:Vietnamese AND (blind OR "visually impaired" OR "visual impairment")` và `abs:Vietnamese AND caption AND controllable`, giới hạn 2025-2026, đều ra 0 kết quả.

Nền cũ (chỉ ghi một dòng): ASG2Caption (Chen et al., CVPR 2020, arXiv 2003.00387) điều khiển caption bằng abstract scene graph do người dùng chọn. Ý "sửa đồ thị → caption" đã có từ 2020 cho mô hình encoder-decoder, nên **không được tuyên bố là ý mới**.

---

## 3. Đánh giá độ mới và hữu ích

| Khẳng định | Mới? | Bài chặn | Cách giữ được |
|---|---|---|---|
| "Caption có span gắn vùng" | Không | GroundCap, PanCap, DenseWorld, PANORAMA | Không tuyên bố |
| "Điều khiển caption bằng scene graph" | Không | ASG2Caption (2020), FoCUS (2026), SGDiff | Không tuyên bố |
| "Mỗi span trỏ tới nút **đã kiểm chứng 3 trạng thái**, hedge hiển thị trong trace" | **Có (MED)** | REVERSE (cụm confident, không có đồ thị), GAVEL (hậu kiểm) | Định nghĩa trace = (span, node id, status, evidence, box). Báo traced-but-wrong |
| "Sửa đồ thị đã kiểm chứng → caption tiếng Việt, đảm bảo Facts ⊆ đồ thị đã sửa" | **Có ở mức tổ hợp** | FoCUS (điều khiển bằng prompt, đo Include/Avoid) | Đặt Include/Avoid tương thích SCoPE, thêm Edit Locality và Hedge Fidelity (FoCUS không có) |
| "Đầu tiên cho tiếng Việt" (grounded, controllable, traceable captioning) | **Có** | Không thấy bài nào | Giữ, kèm truy vấn tái lập |
| "Faithfulness guarantee" | **Không được nói** | — | Chỉ nói "traceability guarantee tương đối so với đồ thị". Faithfulness bị chặn trên bởi precision của verifier (63,1%) |

Hữu ích:
- **Cho bài VSPS:** cao. Truy vết biến khẳng định "giám sát đã kiểm chứng" thành thứ **kiểm toán được**: reviewer bấm vào span là thấy mệnh đề, trạng thái và lý do. Nó cũng trả lời lời phê "template caption kém trôi chảy" bằng một lợi ích mà caption tự do không có.
- **Cho accessibility:** hợp lý nhưng chưa chứng minh. Người khiếm thị cần hỏi tiếp ("người đó đang làm gì?") và bỏ qua phần không cần. Đồ thị cho đúng hai thao tác này. Tuy vậy, Geigle et al. (EMNLP 2024, đã trích trong 00_TONG_HOP) cho thấy grounding ít giảm ảo giác, còn 2608.15574 cho thấy trích dẫn có thể làm **tăng niềm tin sai**. Không được hứa "an toàn hơn" khi chưa có user study.

---

## 4. Thiết kế phương pháp: ViTrace

Đồ thị G = các mệnh đề P\* của VSPS. Nút là entity/attribute/count, cạnh là action/relation. Mỗi nút mang `status ∈ {SUPPORTED, UNCERTAIN}`, `support_score` và `explanation_vi`, và thêm `box` nếu có.

**Thao tác sửa đồ thị** (ngôn ngữ điều khiển, nhỏ và đóng):
- `keep(S)`: chỉ nói các nút trong S
- `drop(S)`: không được nhắc S
- `focus(n, k)`: nút n và lân cận k bước, nói chi tiết
- `hedge(on|off)`: cho hoặc không cho UNCERTAIN xuất hiện, có hedge
- `budget(m)`: tối đa m mệnh đề

Quy tắc phụ thuộc kiểu DSG: bỏ entity thì bỏ luôn attribute và relation con của nó.

**Chế độ A, ký hiệu (có sẵn, 0 GPU).** Áp thao tác lên P\*, rồi chạy `realize.py`. Đảm bảo theo cấu tạo: `Facts(C) ⊆ edit(P*)`. Drop thì vi phạm = 0 trừ khi realizer rò. Đo thực tế để bắt lỗi. Việc cần làm: viết hàm `edit_graph()` (khoảng 50 dòng) và tách `realize` để nhận đồ thị đã sửa.

**Bổ sung box (khoảng 1-2 GPU-h / 3.700 ảnh).** Với mỗi entity, hỏi Qwen2.5-VL-7B (4-bit) ở chế độ grounding JSON, hoặc dùng OWLv2/Florence-2, với nhãn `category_vi` đã dịch sang tiếng Anh. Ghi `box` và `box_source`. Theo nguyên tắc ở mục 4 của 00_TONG_HOP, kênh này **không bao giờ REJECT** mệnh đề chỉ vì thiếu box. Theo 2607.24651, mô hình xuất **id nút**, còn toạ độ được tra từ nút, không bắt mô hình sinh toạ độ.

**Chế độ B, học (đóng góp phương pháp nếu làm bài riêng).**
- Dữ liệu (CPU): với mỗi bản ghi stage-1, lấy mẫu K = 4 phép sửa ngẫu nhiên (keep/drop/focus/hedge/budget) và render lại bằng chế độ A. Mỗi bản ghi cho K+1 cặp (đồ thị đã sửa dạng chuỗi gọn + lệnh, caption có thẻ). Định dạng thẻ theo kiểu GroundCap: `<p id=P18>một vài con thuyền</p>`. Thu được khoảng 18K cặp từ 3.687 ảnh, không tốn GPU.
- Huấn luyện: QLoRA trên Qwen2.5-VL-7B (đã có pipeline SFT), hoặc Vintern-3B để có backbone thứ 2. Có hai đầu vào:
  - (B1) ảnh + đồ thị + lệnh → caption có thẻ. Đây là sinh có điều khiển.
  - (B2) chỉ ảnh → `[đồ thị tóm tắt] → caption có thẻ`, kiểu CCoT. Đây là tự truy vết khi không có đồ thị ngoài.
- Lúc suy luận: kiểm tra thẻ theo cách xác định. Id phải tồn tại trong G, và text trong thẻ phải khớp `text_vi` hoặc head noun của nút (lexicon + loại từ đã có trong `rescap/vi`). Phần text ngoài thẻ chạy qua bộ phát hiện `ungrounded_spans` hiện có.
- Ablation: có/không thẻ, có/không augmentation sửa đồ thị, có/không trạng thái trong đầu vào, B1 vs B2.

Chi phí ước tính (chưa đo): 1 lần QLoRA 7B trên khoảng 18K mẫu ở cấu hình hiện tại là 4-6 GPU-h. Nhân 3 seed thì khoảng 15 GPU-h trên RTX 3090.

---

## 5. Thiết kế đánh giá: metric mới

Ký hiệu: C là caption, s là span có nội dung (đã loại liên từ và hedge marker theo danh sách `HEDGE_MARKERS`/connective của `realize.py`), G là đồ thị đầu vào hoặc đồ thị tự sinh, E là phép sửa.

### 5.1 Truy vết
| Metric | Định nghĩa | Cách chấm |
|---|---|---|
| **TR_struct** (Traceability Rate, cấu trúc) | Tỷ lệ span nội dung có thẻ trỏ tới id tồn tại trong G | Xác định, CPU |
| **TR_sem** (ngữ nghĩa) | Tỷ lệ span có thẻ mà text **khớp** nút được trỏ: cùng head noun/lớp trong lexicon, và thuộc tính/động từ trùng `text_vi` | Lexicon + luật. Phần mơ hồ đưa cho LLM judge (Qwen2.5-7B 4-bit), kiểm tay 100 mục |
| **CharCov** | Tỷ lệ ký tự chữ-số nằm trong span có thẻ | Xác định. Chế độ A hiện đạt 93,2%, làm mức trần |
| **USR** (Ungrounded Span Rate) | Claim do parser tách ra mà không nằm trong span có thẻ nào | Dùng parser caption → mệnh đề (xem 08_text_graph_parsing) |
| **Traced-but-Wrong (TbW)** | Trong các span TR_sem đúng, tỷ lệ nút được trỏ bị người đánh giá là sai so với ảnh | 244 mục audit + mẫu mới 200 span. Đây là metric "trung thực" bắt buộc báo cạnh TR |
| **RegionAcc@0.5** | Span entity mà box tra từ nút có IoU ≥ 0,5 với box COCO cùng lớp | Chỉ trên ảnh COCO (UIT-ViIC, coco5000). Không cần gán nhãn mới. Có thể báo thêm theo gPQ của PANORAMA nếu dùng mask |

### 5.2 Điều khiển (tương thích SCoPE, thêm hai metric riêng)
Bộ lệnh sinh tự động trên tập test (ví dụ 500 ảnh × 4 lệnh). Lệnh được lấy mẫu từ các nút SUPPORTED để việc đúng/sai không phụ thuộc verifier.

| Metric | Định nghĩa |
|---|---|
| **IncR** (Include Recall) | Tỷ lệ nút được yêu cầu (keep/focus) có xuất hiện trong C. Theo thẻ, và đối chiếu bằng parser để không tin thẻ mù quáng |
| **AvoidViol** | Tỷ lệ nút bị drop vẫn được nhắc trong C. Phát hiện bằng parser + lexicon CHAIR tiếng Việt, **không dựa vào thẻ** |
| **CtrlAcc** (Control Accuracy) | Tỷ lệ lệnh thoả **cả hai** điều kiện: mọi nút include có mặt và không nút avoid nào xuất hiện |
| **EditLocality** | Sau phép sửa E, tỷ lệ nút *không bị E chạm tới* (và vẫn trong budget) còn được nói. Đo độ "sửa một chỗ, giữ phần còn lại". FoCUS không đo |
| **HedgeFid** | Với `hedge(on)`: tỷ lệ nút UNCERTAIN được nói kèm hedge marker. Với `hedge(off)`: tỷ lệ nút UNCERTAIN bị lọt ra |
| **BudgetErr** | \|số mệnh đề nói ra − m\| / m |

### 5.3 Chất lượng và ảo giác (giữ để không đánh đổi ngầm)
CHAIR-vi, recall object gold (300 ảnh), CIDEr so với tham chiếu UIT, độ trôi chảy (LLM judge + 3 người trên 100 caption, κ), tỷ lệ output không phải tiếng Việt. Thẻ được bỏ trước khi chấm.

### 5.4 Nghiên cứu người dùng (tối thiểu, khả thi)
- **Nhiệm vụ kiểm toán** (sinh viên làm người đánh giá, 12 người × 30 ảnh): tìm lỗi trong caption, có hoặc không có trace bấm được. Đo độ chính xác phát hiện lỗi, thời gian, và **mức tin sai** (đánh dấu "đúng" cho span sai có nguồn). Mức tin sai kiểm tra cảnh báo của 2608.15574.
- **Accessibility** (tùy chọn, chỉ làm khi liên hệ được hội người mù địa phương, chưa xác minh): 5-8 người dùng screen reader, giao diện hỏi tiếp/bỏ qua theo nút đồ thị. Nếu chưa có thì **không** tuyên bố lợi ích accessibility, chỉ nói "động cơ".

### 5.5 Baseline
1. Qwen2.5-VL-7B zero-shot, prompt xuất caption kèm grounding (box/ref), sau đó căn box → nút.
2. Vintern-3B zero-shot, prompt "chỉ nói về X, không nói Y". Đây là baseline điều khiển bằng prompt kiểu FoCUS nhưng không huấn luyện.
3. VSPS SFT hiện tại (không thẻ) + **attribution hậu nghiệm**: parse caption rồi khớp với G. Đây là đối chứng chính cho câu hỏi "truy vết lúc sinh có hơn truy vết sau khi sinh không".
4. Chế độ A (ký hiệu). Đây là mức trần của TR/CtrlAcc và mức sàn của độ trôi chảy.
5. (Nếu đủ GPU) GRPO kiểu FoCUS với reward Include/Avoid tra offline. 12_graph_training_objectives và 17_novelty_redteam đã coi đây là baseline bắt buộc nếu tuyên bố phương pháp điều khiển.

Giả thuyết kiểm định (chưa đo):
- B1 đạt CtrlAcc gần chế độ A và trôi chảy hơn rõ.
- TR_sem của B1 cao hơn baseline 3.
- TbW xấp xỉ 1 − precision của verifier. Điều này cho thấy trace phơi bày lỗi verifier chứ không che nó.

---

## 6. Khả thi, rủi ro, chỗ đặt

| Hạng mục | Chi phí (ước tính) | Rủi ro |
|---|---|---|
| Chế độ A + `edit_graph` + metric 5.1/5.2 | ~0 GPU, vài ngày code | Thấp. Realizer có thể rò nút khi drop entity cha → bắt bằng quy tắc DSG |
| Box cho entity | 1-2 GPU-h | Trung bình. Nhãn tiếng Việt → tiếng Anh dịch sai (đã có `coco80_vi.json` "BẢN NHÁP") |
| Chế độ B (18K cặp, QLoRA) | 4-6 GPU-h/seed | Trung bình. Thẻ làm giảm độ trôi chảy. Student có thể **gắn thẻ bừa** (thẻ đúng cú pháp, sai nội dung). TR_sem và AvoidViol do parser chấm bắt được lỗi này |
| Kiểm toán người dùng | 2 tuần, 12 người | Thấp đến trung bình |
| BLV study | Không chắc | Cao, phụ thuộc đối tác |

Rủi ro định vị:
- Reviewer có thể nói "đây là data-to-text có ràng buộc, không phải captioning". Trả lời: chế độ B học từ ảnh + đồ thị, và B2 không cần đồ thị ngoài.
- Reviewer có thể nói "FoCUS đã làm điều khiển". Trả lời: khác ở đơn vị điều khiển (nút đã kiểm chứng có id, so với emphasis bằng prompt), và có thêm EditLocality/HedgeFid/TbW.
- Caption template hiện còn vụng. Mẫu `sft.jsonl` có câu như "Người này thứ tư đang vẫy tay", nên mọi so sánh phải báo độ trôi chảy.

Chỗ đặt:
- (1) Ngắn hạn: một mục "Traceability & controllability" trong bản mở rộng Q2 của VSPS. Dùng chế độ A + box + metric 5.1/5.2 + kiểm toán người dùng, gần như 0 GPU.
- (2) Bài riêng 2027 (TALLIP, hoặc workshop accessibility hay grounding ở ACL/EMNLP): chế độ B + 2 backbone + baseline GRPO kiểu FoCUS + user study.
- Không khuyến nghị đặt accessibility làm câu chuyện chính khi chưa có người dùng khiếm thị.

---

## 7. Chưa xác minh
- Venue lấy theo comment arXiv, **chưa đối chiếu với proceedings**: FoCUS (EMNLP 2026 Main), Smol-VL-BLV (EMNLP 2026), Reward-guided decoding (ICCV 2025), SGDiff (AAAI 2025; mã arXiv 2512 nộp sau AAAI-25, nên có thể thực ra là AAAI-26), REVERSE (NeurIPS 2025). GAVEL chỉ ghi "conference".
- Venue của COCONut-PanCap, DAM, DenseWorld-1M: không có trên trang arXiv. OpenAlex và Semantic Scholar bị 429 nên chưa tra được.
- Chỉ thấy qua WebSearch, chưa mở trên arXiv/proceedings: TouchScribe (CHI 2026, arXiv 2602.07802), ESCA (NeurIPS 2025, 2510.15963), FineCaption (CVPR 2025, 2411.15411). Không dùng làm luận cứ.
- Chi tiết SCoPE (số mẫu, cách chấm Avoid) và FoCUS có pha SFT hay không: abstract không nêu, cần đọc bản đầy đủ.
- Không tìm thấy bài tiếng Việt về grounded, controllable hay accessibility captioning. Kết luận chỉ dựa trên arXiv 2025-2026, chưa quét ACL Anthology, VLSP hay tạp chí trong nước.
- Mọi chi phí GPU và giả thuyết ở mục 4-5 là **ước tính, chưa đo**.

## 8. Truy vấn theo dõi
1. arXiv: `abs:"grounded captioning" OR abs:"grounded caption"` (sắp theo ngày)
2. arXiv: `abs:controllable AND abs:"scene graph" AND abs:caption`
3. arXiv: `abs:caption AND (abs:attribution OR abs:citation) AND abs:region`
4. arXiv: `abs:Vietnamese AND (abs:caption OR abs:"visually impaired") AND (abs:grounding OR abs:controllable)`
5. Theo dõi trích dẫn của FoCUS (2609.00709), GroundCap (2502.13898), PANORAMA (2609.19143), GAVEL (2606.26923).
