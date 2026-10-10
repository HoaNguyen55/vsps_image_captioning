# 16. Bộ scene graph tiếng Việt có định vị (ViSG) trên ảnh UIT/KTVIC: giao thức xây dựng

Ngày: 2026-10-10. Agent KG-plan 16. Góc: dựng dữ liệu đồ thị cảnh tiếng Việt bằng VLM gán trước rồi người sửa. Gồm schema, pipeline, chi phí pilot 500 ảnh và kế hoạch mở rộng.

**Nguồn đã mở trong phiên này.** Các trang arXiv abs/html của 2401.08100, 2305.04166, 2302.11752, 2506.07643, 2602.23543, 2407.06723 và 2412.08614 (html). README GitHub `pacman-ctm/ktvic`. Trang dataset UIT-OpenViIC. Tài liệu Label Studio (`/tags/relations`, `/guide/predictions`). Phiên này arXiv API trả 429, còn OpenAlex và Semantic Scholar hết quota, nên việc xác minh dựa vào trang abs/html và kết quả web search. Mục nào chỉ thấy qua snippet thì ghi ở §9.

**Kết luận ngắn**
1. Hiện chưa có bộ scene graph tiếng Việt nào gắn với ảnh (xem file 11, §3.2). Dựng một pilot 500 ảnh trên **KTVIC test** là khả thi: khoảng **122 giờ công người** (+23 giờ nếu làm nhánh B) và **~15 GPU-h** trên RTX 3090 (§5). Lý do chọn KTVIC test: đã có 300 ảnh object-gold, có pipeline VSPS, có lexicon 113 mục.
2. Mức tương đồng là medium chứ không high. CompreCap (CVPR 2025) cũng gán tay scene graph cho 560 ảnh COCO, và SVG/SVG2 (2025-2026) dùng LLM tự động hoàn thiện đồ thị. Điểm mới là **ngôn ngữ, miền ảnh Việt và từ vựng bản địa** (loại từ, vật thể văn hóa, phân cấp IsA tiếng Việt). Phương pháp gán nhãn không mới.
3. Rủi ro lớn nhất là **pháp lý**. KTVIC và UIT-OpenViIC không có file license, và ảnh OpenViIC được crawl từ Google/Bing. Vì vậy chỉ phát hành annotation, không phát hành lại ảnh, và phải xin phép tác giả bằng văn bản trước khi công bố (§7).

---

## 1. Bối cảnh 2025-2026 (đã xác minh)

| Công trình | Năm/venue | Cách tạo đồ thị | Bài học cho ViSG |
|---|---|---|---|
| Synthetic Visual Genome (SVG; Park et al.), arXiv 2506.07643 | CVPR 2025 (comment trên arXiv; có bản CVF open access) | Một teacher MLLM bổ sung quan hệ còn thiếu vào scene graph sẵn có, kèm bước lọc. SG-EDIT dùng GPT-4o để sửa đồ thị do ROBIN dự đoán. Quy mô 146K ảnh, 5,6M quan hệ, 2,6M vật thể. | Cách làm mặc định của 2025 là để LLM **đề xuất quan hệ** trên các vật thể đã có, rồi lọc. Vật thể làm trước, quan hệ làm sau. |
| Synthetic Visual Genome 2, arXiv 2602.23543 | arXiv 2026-02 (v3 2026-03), chưa có venue | Pipeline tự động: panoptic seg, tracking, GPT-5 suy luận quan hệ. Người chỉ kiểm tra độ đúng: **vật thể 93,8%, thuộc tính 88,3%, quan hệ 85,4%**. | Thứ tự khó tăng dần theo object, attribute, relation. Thời gian người nên dồn vào **quan hệ**. Mẫu báo cáo nên theo kiểu "độ chính xác do người kiểm trên mẫu" khi làm tập silver lớn. |
| CompreCap (Lu et al.), arXiv 2412.08614 | CVPR 2025 | 560 ảnh COCO panoptic. Người gán lại mask, nhãn (412 lớp, gộp từ RAM, COCO, OpenImages, Objects365), thuộc tính (hình dạng, kích thước, màu, chất liệu) và quan hệ SVO. 20 người gán. Loại ảnh có mask phủ dưới 95%. **Bài không báo thời gian hay chi phí**, và trong phần đã đọc không thấy quy trình QC. | Đây là tiền lệ gần nhất về quy mô: khoảng 500 ảnh gán tay đã đủ làm benchmark ở CVPR. ViSG cần làm tốt hơn ở **IAA và báo cáo chi phí**, vì CompreCap thiếu cả hai. |
| Graph-Based Captioning (GBC), arXiv 2407.06723 | arXiv 2024, chưa có venue | Hai bước: xác định và mô tả nút thực thể, sau đó nối nút bằng composition và relation. Dùng MLLM và detector có sẵn, cho GBC10M trên CC12M. | Đồ thị có thể mang **nút văn bản** (mô tả vùng). Schema ViSG giữ một trường `desc_vi` tùy chọn cho mỗi nút. |
| Hindi Visual Genome (LREC 2022, nền cũ) | 2022 | Dịch máy caption vùng của VG, rồi người hậu biên tập có xem ảnh. | Đây là dạng phản biện cần tránh ("chỉ là dịch VG"). ViSG không dịch mà gán trực tiếp trên ảnh Việt. |
| GeneAnnotator, arXiv 2109.02226 (nền cũ) | 2021 | Công cụ bán tự động cho scene graph, có gợi ý quan hệ theo luật. | Ý tưởng "gợi ý quan hệ rồi người chọn" đã có từ trước. LLM chỉ thay luật. |

**Thiên lệch neo (anchoring) khi gán trước bằng LLM.** Phần này mới thấy qua web search, chưa mở bài gốc (§9). Có báo cáo rằng mức đồng ý với nhãn LLM tăng mạnh khi người gán được xem gợi ý. Điều này làm IAA đẹp hơn thực tế. Giao thức ở §4.3 có **tập đối chứng gán từ đầu** để đo hiệu ứng này, không mặc định cho rằng nó bằng 0.

## 2. Chọn ảnh pilot

- **500 ảnh KTVIC test** = toàn bộ 300 ảnh object-gold (`data/object_gold/sample.json`, seed 42, phân tầng) + 200 ảnh rút thêm cùng seed và cùng tầng từ 258 ảnh còn lại.
- **58 ảnh còn lại** để phát triển hướng dẫn và hiệu chuẩn. Chúng không vào gold, nên gold không bị nhiễm bởi các vòng sửa hướng dẫn.
- Lý do chọn test thay vì train: dùng làm benchmark cho graph P/R của caption (Ý 1 trong file 11) và tập kiểm tra cho parser ViSGParse (Ý 3). Bản ghi VSPS stage-1 có sẵn cho **3.700 ảnh train và 0 ảnh test** (đã đếm trong `data/stage1_records/stage1_records.tar.gz`), nên phải chạy pre-annotation mới cho test (§5).
- 300 ảnh object-gold, sau khi người gán xong theo `.paper_work/OBJECT_GOLD_PROTOCOL.md`, trở thành **ràng buộc tầng vật thể**. Nhãn lớp có/không của object-gold được nạp vào làm prior và dùng để đo độ ổn định giữa hai lần gán.

## 3. Schema ViSG v0.1

Định dạng là JSON theo từng ảnh, gần với Visual Genome (objects, attributes, relationships) để dùng lại được công cụ SGG, kèm các trường riêng cho tiếng Việt.

```json
{
  "image_id": "2", "file_name": "00000000002.jpg", "source": "KTVIC-test",
  "scene": {"loai_canh": "sông nước", "trong_ngoai": "ngoài trời"},
  "objects": [
    {"id": "o1", "name_vi": "thuyền", "classifier": "chiếc", "isa": "phuong_tien_thuy",
     "bbox": [x1, y1, x2, y2], "group": false, "count": 1,
     "gender": null, "age": null, "certainty": "chac_chan", "desc_vi": null,
     "provenance": "qwen25vl7b|owlv2|human_add", "edited": true}
  ],
  "attributes": [{"object": "o1", "type": "mau_sac", "value_vi": "xanh dương", "certainty": "chac_chan"}],
  "relations": [{"id": "r1", "subj": "o2", "pred_vi": "ngồi trên", "pred_type": "khong_gian_tiep_xuc",
                 "obj": "o1", "pred_en": "sitting on", "certainty": "chac_chan"}],
  "annot": {"who": "A", "seconds": 312, "tool_version": "v0.1", "pre_annotation": true}
}
```

**Quy tắc đặt tên tiếng Việt**
1. `name_vi` là danh từ đầu ở dạng chuẩn (lemma), **không chứa loại từ hay từ chỉ số nhiều**. Ví dụ "chiếc thuyền", "những con chó" thành `thuyền`, `chó`. Loại từ ghi riêng vào `classifier` vì lỗi "loại từ không rõ" đã xuất hiện trong `stats.truncations` của VSPS. Số lượng ghi vào `count`, và đặt `group=true` khi là đám đông hoặc nhóm không đếm được.
2. Lưu chuỗi tự nhiên có dấu, không dùng `_` của word segmentation. Bản tách từ (RDRSegmenter, giống KTVIC) chỉ sinh ra lúc dùng.
3. Đồng nghĩa được gộp bằng `canonical()` của `rescap/chair.py`, ví dụ `dù/ô`, `dòng sông/sông`. Giới tính và tuổi là thuộc tính của nút người, nên `phụ nữ` vẫn có `isa=người`, giống quy tắc hypernym của CHAIR-vi.
4. Vật văn hóa Việt (nón lá, áo dài, xe ba gác, gánh hàng, bánh mì, ...) là **lá riêng** trong IsA, có `gloss_en` để căn chỉnh chéo ngôn ngữ, không ép về lớp tiếng Anh gần nhất.

**Từ vựng đóng (cấu hình khi khởi tạo, chỉ mở rộng giữa các vòng)**
- *Object*: khởi đầu bằng 101 ô của object-gold, tức lexicon 113 mục đã gộp đồng nghĩa. Ô "vật thể khác" của object-gold và của pilot là nguồn bổ sung. Một từ mới được đưa vào vocab khi xuất hiện ở **≥3 ảnh** (`ponytail:` ngưỡng tần suất thô; muốn chặt hơn thì cần chuyên gia duyệt). Mục tiêu khoảng 200 lớp sau pilot, so với 412 lớp của CompreCap.
- *Attribute*: 8 loại cố định gồm `mau_sac`, `kich_thuoc`, `chat_lieu`, `hinh_dang`, `trang_thai` (đang mở, ướt, ...), `trang_phuc` (cho người), `gioi_tinh`, `do_tuoi`. Giá trị lấy từ danh sách đóng, ví dụ màu có khoảng 14 giá trị. Cho phép thêm `khac:<text>`.
- *Predicate*: khoảng 50 vị từ, chia 4 nhóm. (a) Không gian: ở trên, bên dưới, bên cạnh, phía trước, phía sau, bên trong, bên trái/phải (theo góc người xem). (b) Tiếp xúc hoặc tư thế: ngồi trên, đứng trên, nằm trên, dựa vào. (c) Hành động: cầm, mặc, đội, đeo, lái, đẩy, chèo, bán, ăn, nhìn, nói chuyện với. (d) Bộ phận hoặc sở hữu: của, có. Mỗi vị từ có `pred_en` ứng với predicate của VG để so sánh chéo. Vị từ đối xứng (bên cạnh, nói chuyện với) chỉ lưu **một cạnh** để IAA không bị đếm đôi.
- `certainty ∈ {chac_chan, khong_chac}` tương ứng SUPPORTED/UNCERTAIN của VSPS. Đồ thị người duyệt vì vậy dùng trực tiếp được để hiệu chỉnh verifier 3 trạng thái.

**Phân cấp IsA.** Có 3 tầng trên lá.
- Gốc: `thực thể`.
- Tầng 1: `người`, `động vật`, `phương tiện`, `đồ vật`, `thực phẩm`, `thực vật`, `công trình`, `cảnh/địa hình`.
- Tầng 2: ví dụ `phương tiện` gồm `phương tiện đường bộ` và `phương tiện thủy`.
- Lá trỏ tới một synset WordNet tiếng Anh nếu có, và để trống nếu là vật bản địa.
- Lưu bằng một file `isa_vi.json` cha-con, khoảng 250 dòng, viết tay từ lexicon và `data/coco_probe/coco80_vi.json`. Không phụ thuộc ConceptNet, vì độ phủ tiếng Việt của nó chưa xác minh (file 11, §5).
- Dùng vào 3 việc: chấm lenient (nói hypernym vẫn tính đúng), trung tính hóa một bậc (Ý 2b của file 11) và gộp lớp khi tính κ.

**Phụ thuộc kiểu DSG.** Thuộc tính và quan hệ chỉ hợp lệ khi các nút vật thể của chúng tồn tại. Khi người gán xóa một vật thể, công cụ tự xóa mọi thuộc tính và quan hệ nối với nó.

## 4. Pipeline

### 4.1 Gán trước (máy; một RTX 3090)
1. **Vật thể và bbox.** Qwen2.5-VL-7B (4-bit) được prompt xuất JSON gồm `name_vi`, `classifier`, `bbox`, và **buộc chọn trong vocab** (danh sách lớp nằm trong prompt, ngoài vocab thì ghi `khac:`). Song song, chạy OWLv2 hoặc Florence-2 với tên tiếng Anh (`pred_en`/gloss) của từng lớp, đúng hướng A2 trong `00_TONG_HOP.md`. Hai nguồn được gộp bằng IoU ≥ 0.5. Box nào chỉ có một nguồn sẽ bị gắn cờ "cần xem".
2. **Thuộc tính và quan hệ.** Ảnh được vẽ thêm số hiệu box (set-of-marks), sau đó Qwen2.5-VL-7B đề xuất thuộc tính theo 8 loại và bộ ba `(oi, pred, oj)` trong vocab vị từ. Cách này giống SVG: có vật thể trước, rồi mới đề xuất quan hệ.
3. **Chấm tin cậy.** Mỗi thuộc tính và quan hệ được hỏi lại verifier dạng Có/Không (Vintern-1B, hoặc đọc logit P(Có) như cải tiến #1 trong `00_TONG_HOP.md`). Kết quả chỉ dùng để **sắp thứ tự ưu tiên duyệt** và tô màu, **không tự xóa** mục nào. Lý do là precision SUPPORTED của verifier hiện chỉ 63,1%.
4. Đầu ra là file `pre/<id>.json` theo schema ở §3, với `provenance` ghi rõ nguồn của từng mục.

### 4.2 Công cụ người sửa
| Lựa chọn | Ưu | Nhược | Quyết định |
|---|---|---|---|
| Label Studio Community | Có `RectangleLabels` cho box. Thẻ `Relations` hỗ trợ dữ liệu ảnh. Nhập pre-annotation qua khóa `predictions` (định dạng rectanglelabels có trong tài liệu) và hiển thị sẵn trên trang gán. | Vẽ quan hệ bằng mũi tên trên ảnh có 10-20 cạnh rất chậm và dễ rối. Tài liệu predictions chưa nói về định dạng relation (§9). Phải chạy server. | **Dùng cho Pass 1** (vật thể và box). |
| CVAT | Mạnh về box, mask, track. | Search không thấy hỗ trợ quan hệ giữa các vật thể (§9). | Không dùng. |
| Mở rộng `data/object_gold/annotate.html` | Đã có sẵn và người gán đã quen. Lưu localStorage, xuất/nạp JSON, không cần server. | Không vẽ được box. | **Dùng cho Pass 2**: danh sách thuộc tính và bộ ba, chấp nhận/sửa/xóa bằng phím tắt. Ảnh có overlay số hiệu box vẽ bằng `<canvas>`. Dropdown chỉ chứa vocab. Có nút "thêm bộ ba". Đồng hồ ghi `annot.seconds`. |

Lý do chia hai pass: duyệt quan hệ dạng danh sách nhanh hơn kéo mũi tên. Box thì cần một công cụ vẽ thật, và không nên tự viết lại phần đó.

### 4.3 Quy trình người (2 người gán A, B và 1 người phân xử C, ví dụ tác giả chính)
1. **Phát triển hướng dẫn** trên 58 ảnh dự trữ. A và B cùng gán 20 ảnh, đối chiếu, rồi sửa hướng dẫn. Đây là cùng cơ chế hiệu chuẩn với object-gold. Nếu κ vật thể < 0.6 hoặc F1 bộ ba < 0.5 thì sửa hướng dẫn và làm lại 20 ảnh khác.
2. **Tập đối chứng anchoring**: 30 ảnh trong 500 được A và B gán **từ đầu, không có pre-annotation**, *trước khi* thấy bản gán trước của các ảnh đó. So bản từ đầu với bản đã sửa trên cùng ảnh sẽ cho thấy (a) phần pre-annotation sai mà người vẫn giữ và (b) phần người bỏ sót vì bị neo. Kết quả này được báo trong bài.
3. **Gán chính**: 100 ảnh do cả A và B gán độc lập, dùng cho IAA và phân xử. 400 ảnh còn lại chia đôi, mỗi người gán một lần. Thứ tự ảnh xáo trộn theo seed. Mỗi buổi không quá 2 giờ, giống object-gold.
4. **Phân xử**: C xử lý mọi bất đồng trên 100 ảnh gán đôi, rồi kiểm ngẫu nhiên 10% của 400 ảnh gán đơn (40 ảnh). Nếu tỷ lệ C phải sửa ở nhóm gán đơn vượt quá 15% thì mở rộng gán đôi.

### 4.4 Kiểm soát chất lượng và IAA (tính trên 100 ảnh gán đôi)
- **Vật thể (lớp có/không)**: κ theo lớp và pooled κ. Dùng lại `scripts/object_gold_score.py` và `scripts/agreement.py`. Ngưỡng pooled κ ≥ 0.7, cao hơn mốc 0.6 của object-gold vì đã có gợi ý.
- **Box**: ghép Hungarian theo IoU ≥ 0.5 trong cùng lớp, báo F1 phần ghép được và IoU trung bình.
- **Thuộc tính**: trên các cặp vật thể đã ghép, tính κ theo (vật thể, loại thuộc tính) với giá trị là nhãn danh định. Báo riêng màu sắc vì màu thường mơ hồ (`scripts/count_colour_ambiguity.py` đã có tiền lệ).
- **Quan hệ**: F1 bộ ba giữa A và B sau khi ghép vật thể (khớp chính xác vị từ), cùng F1 "lenient" khi vị từ cùng nhóm a/b/c/d. Thêm Krippendorff α cho nhãn vị từ trên các cặp (subj, obj) mà cả hai đều nối. Ngưỡng mục tiêu F1 chính xác ≥ 0.6. Đây là *ước tính*, cần xác nhận ở bước hiệu chuẩn; tham chiếu gần nhất là độ chính xác quan hệ 85,4% do người kiểm trong SVG2, nhưng con số đó là accuracy chứ không phải độ đồng thuận.
- **Theo dõi pre-annotation**: tỷ lệ chấp nhận nguyên, sửa, xóa và thêm mới theo loại (obj/attr/rel), cùng số giây mỗi ảnh. Đây là bảng chi phí mà CompreCap không có.
- **Quy tắc gold**: giống object-gold. Mục cả hai cùng có thì vào gold. Mục chỉ một người có thì vào gold khi C đồng ý. Khi chưa phân xử, báo cả hai cận `agreed` và `union`.
- Không chỉnh κ bằng cách nới vocab sau khi đã thấy kết quả. Mọi thay đổi vocab sau hiệu chuẩn đều được ghi version (`tool_version`).

### 4.5 Nhánh B (tùy chọn, rất nên làm): đồ thị văn bản cho caption
Mỗi ảnh trong 500 có 5 caption tham chiếu, tổng cộng 2.500 caption. Qwen2.5-7B (văn bản, 4-bit) parse từng caption thành bộ ba theo cùng vocab. Người sửa, rồi **liên kết mỗi nút văn bản với nút ảnh** (`o1`, ...), hoặc đánh dấu "không có trong ảnh". Nhánh này cho ra tập test của ViSGParse (Ý 3 trong file 11), và các cạnh "không có trong ảnh" là ảo giác trong *caption người*. Đây là dữ liệu hiếm, khác với FACTUAL/DiscoSG vốn không neo vào nút ảnh.

## 5. Chi phí pilot 500 ảnh

Các con số phút/ảnh dưới đây là **ước tính** dựa trên một số đo có thật: object-gold đo được 1-1,5 phút/ảnh cho riêng phần lớp có/không với 101 ô. Phần còn lại được nội suy cho box, thuộc tính và quan hệ. Bảng sẽ được thay bằng số thật sau 20 ảnh hiệu chuẩn (`annot.seconds`).

| Hạng mục | Giả định | Giờ công |
|---|---|---|
| Viết hướng dẫn, `isa_vi.json`, vocab vị từ (C) | | 10 |
| Kỹ thuật: script gán trước, cấu hình Label Studio, mở rộng `annotate.html`, script IAA (tác giả) | dùng lại `object_gold_score.py`/`agreement.py` | 20 |
| Hiệu chuẩn 20 ảnh × 2 người + họp | 10 phút/ảnh khi còn lạ tay | 7 + 3 |
| Đối chứng anchoring 30 ảnh × 2 người, gán từ đầu | ~15 phút/ảnh | 15 |
| Gán chính 500 ảnh (Pass 1 ~2 phút, Pass 2 ~4 phút) | ~6 phút/ảnh | 50 |
| Gán đôi thêm 100 ảnh | 6 phút/ảnh | 10 |
| Phân xử 100 ảnh + kiểm 40 ảnh (C) | 3 phút/ảnh | 7 |
| **Tổng nhánh A** | | **~122 giờ** (khoảng 85 giờ của hai người gán A+B, 37 giờ của tác giả/người phân xử C) |
| Nhánh B: sửa 2.500 parse caption + liên kết nút | ~0,5 phút/caption, chỉ gán đơn, 10% gán đôi | ~23 |
| **GPU** | Gán trước bằng Qwen2.5-VL-7B 4-bit cho 2 lượt (obj, rel) ~40 s/ảnh, cộng OWLv2 ~2 s/ảnh, cộng verifier (mức hiện tại ~80 s/ảnh, giảm nhiều nếu làm cải tiến #1) | **~15-20 GPU-h** cho 500 ảnh, chạy qua đêm |

Quy đổi lịch: 2 người gán, mỗi người khoảng 43 giờ, với nhịp 6 giờ/tuần (3 buổi × 2 giờ) thì mất khoảng **7 tuần**. Nếu dồn 4 buổi/tuần thì khoảng 5-6 tuần. Mức này phù hợp với ước tính "2-3 tuần, 2 người" của file 11 cho riêng phần duyệt vật thể, còn phần quan hệ làm thời gian dài thêm. Tiền công phụ thuộc mức trả cho sinh viên, chưa có số xác minh (§9).

## 6. Kế hoạch mở rộng

| Giai đoạn | Ảnh | Cách làm | Giờ công ước tính | Dùng để |
|---|---|---|---|---|
| P0 pilot | 500 KTVIC test | §4, đầy đủ IAA | ~122 (+23 nhánh B) | Benchmark graph-P/R, test ViSGParse, hiệu chỉnh verifier |
| P1 đa miền | +1.500: UIT-OpenViIC test (2.001 ảnh, cảnh Việt crawl từ web) và UIT-ViIC (ảnh COCO thể thao) | QLoRA Qwen2.5-VL-7B trên ~400 đồ thị gold của P0 (≈1-2 GPU-h) để làm bộ gán trước tốt hơn. Bỏ gán từ đầu, chỉ gán đôi 10% | mục tiêu ≤4 phút/ảnh, tức ~100 + 15 phân xử | Kiểm tra tổng quát hóa chéo miền; **chỉ làm khi đã có giấy phép (§7)** |
| P2 silver | 10-20k ảnh train của KTVIC (3.769) và OpenViIC (9.088) | Hoàn toàn tự động. Lấy từ bản ghi VSPS stage-1 có sẵn cho 3.700 ảnh KTVIC train, và chạy mới cho OpenViIC. Người kiểm 2% mẫu để báo độ chính xác theo loại, giống SVG2. | ~15-20 cho phần kiểm; GPU khoảng 40-80 GPU-h nếu chưa tăng tốc verifier | Huấn luyện parser, SFT hoặc GRPO có reward theo đồ thị |

Cổng chuyển giai đoạn: P0 phải đạt pooled κ vật thể ≥ 0.7 và F1 bộ ba ≥ 0.6. Nếu không đạt, sửa vocab vị từ (gộp các vị từ hay bị nhầm) chứ không tăng quy mô.

Nguyên tắc về kích thước: 500 ảnh có IAA tốt là đủ cho một benchmark (tiền lệ CompreCap dùng 560 ảnh). Huấn luyện thì dùng silver có báo độ chính xác do người kiểm. **Không** gán tay hàng nghìn ảnh để huấn luyện.

## 7. Giấy phép và phân phối lại (đã kiểm trong phiên này)

| Bộ | Nguồn ảnh | License công bố | Hệ quả |
|---|---|---|---|
| KTVIC (Pham, Nguyen, Vuong, Ha; **nhóm này không thuộc UIT**, arXiv 2401.08100) | Ảnh lấy từ UIT-EVJVQA. README GitHub cho biết link EVJVQA gốc đã bị gỡ và ảnh hiện phát qua Google Drive. | Repo GitHub **không có file LICENSE**. Nhãn CC BY-NC-SA 4.0 trên arXiv là license của *bài báo*. | Chỉ phát hành annotation, khóa theo `file_name`. Không đóng gói ảnh. Gửi email xin phép tác giả KTVIC và nhóm EVJVQA. |
| UIT-EVJVQA (arXiv 2302.11752; VLSP 2022) | Khoảng 5.000 ảnh chụp tại Việt Nam. Trang abs không mô tả cách thu thập. | Trang abs không nêu license riêng cho dữ liệu. | Như trên. |
| UIT-OpenViIC (arXiv 2305.04166) | **Crawl từ Google và Bing** bằng từ khóa tiếng Việt, 13.100 ảnh. | Bài ghi "available online for non-commercial research". Trang dataset không có license hay điều khoản. | Bản quyền ảnh thuộc bên thứ ba, nên chỉ phát hành annotation và chỉ dùng phi thương mại. Không hiển thị ảnh trong demo công khai trừ khi được phép. |
| UIT-ViIC (arXiv 2002.00175) | Ảnh COCO | Ảnh COCO mang license Flickr riêng cho từng ảnh (theo hiểu biết chung, chưa mở lại trong phiên này) | An toàn nhất: phát hành theo COCO image id. |

Đề xuất phát hành annotation ViSG dưới **CC BY-NC-SA 4.0**. Lý do: không mở rộng quyền vượt quá điều kiện "non-commercial research" của nguồn, và khớp với license bài báo của các bộ gốc. Kèm datasheet (nguồn, quy trình, IAA, thiên lệch anchoring, giới hạn vocab) và một script tải ảnh từ nguồn gốc. Cần ghi rõ trong bài: "ảnh không được phân phối lại". Việc luật Việt Nam có ngoại lệ khai phá dữ liệu (TDM) hay không **chưa xác minh** (§9), nên nên hỏi ý kiến phòng pháp chế hoặc khoa trước khi công bố P1.

## 8. Đánh giá theo 3 trục

- **Khả thi: cao.** Phần GPU nhỏ (dưới 20 GPU-h). Phần người khoảng 120-145 giờ, nằm trong sức của 2 sinh viên trong một học kỳ. Hạ tầng đã có: lexicon, giao thức object-gold, script κ, HTML annotate, và pipeline VSPS để gán trước. Rủi ro thời gian nằm ở quan hệ: nếu Pass 2 tốn quá 6 phút/ảnh thì giảm vocab vị từ hoặc giới hạn 15 quan hệ nổi bật mỗi ảnh.
- **Tương đồng: medium.** CompreCap (gán tay 560 ảnh, đo độ phủ caption chi tiết) gần nhất về mục đích và quy mô. SVG/SVG2 gần nhất về pipeline LLM gán trước. GBC gần về định dạng. Nếu bài chỉ là "bộ dữ liệu + IAA" thì sẽ bị so trực tiếp với CompreCap. Vì vậy bộ dữ liệu nên là **đóng góp phụ** đi cùng metric graph-P/R tiếng Việt (Ý 1) hoặc benchmark ảo giác quan hệ (Ý 3).
- **Mới:** (i) bộ scene graph đầu tiên có định vị trên ảnh tiếng Việt, vì file 11 đã quét và không thấy bộ nào; (ii) schema tách loại từ, số lượng và IsA bản địa; (iii) báo cáo định lượng chi phí và anchoring của gán trước bằng VLM, điều mà CompreCap không làm; (iv) liên kết nút caption người với nút ảnh (nhánh B) để đo ảo giác của chính tham chiếu. Phương pháp gán nhãn tự nó không mới. Đừng quảng bá nó như một đóng góp.

## 9. Chưa xác minh
- Định dạng JSON cho **relation trong pre-annotation** của Label Studio: trang `/guide/predictions` không nói. Cần thử nhập một task mẫu trước khi chọn hẳn công cụ. Phương án dự phòng là đưa quan hệ hoàn toàn sang Pass 2 HTML, và kế hoạch này đã làm như vậy.
- CVAT không hỗ trợ quan hệ: kết luận chỉ dựa trên việc web search không tìm thấy, chưa đọc tài liệu CVAT mới nhất.
- Các nghiên cứu về anchoring: "The LLM Effect" (Choi et al., EMNLP 2024; mức đồng ý 43,9% lên 71,5%), Francis et al. (NLPerspectives 2026) và WhoSaidIt (arXiv 2605.26070) mới chỉ thấy qua snippet hoặc trang review, chưa mở bài gốc.
- Số tham chiếu RefCOCO của SVG có hai phiên bản (88,2 và 88,9) theo snippet. Kế hoạch này không dùng con số đó.
- Có bộ Open Multilingual Wordnet hay WordNet tiếng Việt dùng được cho IsA không: chưa kiểm. Kế hoạch đã chọn tự viết `isa_vi.json` để không phụ thuộc vào nó.
- Mọi số phút/ảnh ngoài mốc object-gold (1-1,5 phút) đều là ước tính và phải thay bằng số đo được từ hiệu chuẩn.
- Mức thù lao cho người gán tại Việt Nam, ngoại lệ TDM trong luật sở hữu trí tuệ Việt Nam và license từng ảnh COCO: chưa tra.
- Venue của CompreCap (CVPR 2025) lấy theo file 11 (Semantic Scholar), chưa đối chiếu proceedings trong phiên này. CVPR 2025 của SVG lấy theo comment trên arXiv và link CVF open access trong kết quả search.
