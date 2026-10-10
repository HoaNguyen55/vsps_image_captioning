# 03. Khả thi về tài nguyên cho KG/scene-graph captioning tiếng Việt

Agent KG-plan 03, ngày 2026-10-10. Góc nhìn: FEASIBILITY.
Nguồn đã mở trong phiên này: trang arXiv abs/html, OpenAlex (trước khi hết quota), HF Hub API, GitHub API (`gh api`), Wikidata API/SPARQL, wiki ConceptNet, file VG `image_data.json`. Ở lần gọi này, arXiv export API và Semantic Scholar trả 429, OpenAlex hết quota ngày, `api.conceptnet.io` trả 502.

**Phát hiện quan trọng nhất (sửa file 11 §3.2):** tiếng Việt **đã có** một bộ scene graph là **VietSGG** (GitHub `Moobbot/VietSGG`, CC BY 4.0, README ghi "Accepted at EAI GOODTECHS 2025"). Bộ này dựng trên ảnh UIT-ViIC (thể thao COCO), gán nhãn bán tự động bằng Grounding DINO + GPT-4, baseline là RelTR/EGTR/SGTR. Vì vậy câu "Vietnamese has no scene-graph data" trong brief và file 11 là **sai**. Câu đúng phải là: "chưa có scene graph cho ảnh đời sống Việt Nam (KTVIC/OpenViIC), chưa có parser text→SG tiếng Việt, và chưa có metric dạng đồ thị".

---

## 1. Dataset UIT và liên quan

| Dataset | Kích thước (đã xác minh) | Split | Kiểu caption | Có object/region? | Tải về / license |
|---|---|---|---|---|---|
| **UIT-ViIC** (arXiv 2002.00175, ICCCI 2020) | 3.850 ảnh COCO (thể thao có bóng), 19.250 caption | theo bài gốc | ngắn, 5 caption/ảnh | Không, nhưng ảnh là COCO nên **có box COCO**. Khoảng 1.236/2.873 ảnh VietSGG nằm trong Visual Genome (xem §1.1) | Bài gốc: "published on our lab website". HF: `ttrung1402/UIT-ViIC` (tag cc-by-4.0, bản cộng đồng), `SEACrowd/uit_viic` (license unknown) |
| **UIT-OpenViIC** (arXiv 2305.04166, "submitted to Elsevier") | 13.100 ảnh, 61.241 caption | train 9.088/41.238 · val 2.011/10.002 · test 2.001/10.001 | trung bình 17,61 (từ), ảnh Việt Nam phức tạp | Không | https://uit-together.github.io/datasets/UIT-OpenViIC/ dẫn tới Google Drive mở. Bài ghi "non-commercial research", trang tải **không ghi license** |
| **KTVIC** (arXiv 2401.08100) | 4.327 ảnh, 21.635 caption | train 3.769/18.845 · test 558/2.790 (khớp bản local `data/datasets/ktvic`) | ngắn, ~10,97 từ, 5 caption/ảnh, có `segment_caption` | Không. Ảnh lấy từ UIT-EVJVQA | `github.com/pacman-ctm/ktvic`, repo **không có file LICENSE**. HF `Skyler215/KTVIC` (không license) |
| **ViTextCaps** (arXiv 2604.27712, 2026-04) | 15.729 ảnh, 74.970 caption | train 10.996 · dev 1.641 · test 3.092 (ảnh) | 22,1 từ (median 19), scene-text | Bài có OCR box và region feature, nhưng format công bố chỉ có `image_id, file_name, captions` | **Chưa tìm thấy bản phát hành**: GitHub search và HF search đều rỗng. Trang arXiv chỉ có badge CC BY-NC-SA cho *bài báo* |
| **UIT-EVJVQA** (arXiv 2302.11752) | 33.000+ cặp QA (vi/en/ja), ~5.000 ảnh Việt Nam | theo challenge VLSP 2022 | QA mở | Không | HF `dinhanhx/evjvqa` (license unknown) |
| **OpenViVQA** (arXiv 2305.04183; DOI 10.1016/j.inffus.2023.101868) | 11.000+ ảnh, 37.000+ QA mở | — | QA mở | Không | HF `uitnlp/OpenViVQA-dataset`, **MIT**, không gated |
| **VietSGG** (GitHub, 2025) | 2.873 ảnh (train 2.649 / val 224), 22.306 box, 25 lớp object (train), **71 predicate**, 11.024 bộ ba (train 10.160 / val 864). Đã tải và đếm trong phiên này | train/val | — | **Có**: box và quan hệ, ontology Việt-Anh | CC BY 4.0. Nhãn **bán tự động** (GDINO + GPT-4), miền thể thao hẹp (vận động viên, quả bóng, sân...) |
| Bản dịch máy (5CD-AI) | `5CD-AI/Vietnamese-ShareGPT4Vision-gg-translated` (100K-1M, dịch Google), `Vietnamese-LLaVA-Instruct-150K-gg-translated`, `Viet-Localization-VQA` (gated manual) | — | **caption chi tiết** (dịch) | ShareGPT4V không có SG | HF, không ghi license. Đây là nguồn caption dài tiếng Việt duy nhất, nhưng là bản dịch |

Nhận xét:
- **Mọi bộ UIT đều là caption ngắn**, 5 caption/ảnh, 11-22 từ. Không bộ nào có caption chi tiết do người viết, và không bộ nào có region hay SG, trừ VietSGG.
- **License là rủi ro thật.** KTVIC không có LICENSE, OpenViIC chỉ ghi "non-commercial", ViTextCaps chưa phát hành. Nếu công bố gold SG mới trên ảnh KTVIC/OpenViIC, cần xin phép nhóm tác giả hoặc chỉ phát hành annotation kèm ID ảnh.

### 1.1 Visual Genome trùng ảnh UIT-ViIC (đo trong phiên này)
VG `image_data.json` có 108.077 ảnh, trong đó 51.208 có `coco_id`. Trong 2.873 ảnh VietSGG (ảnh UIT-ViIC, tên file là COCO id bỏ số 0 đầu, theo `rename_image.py`), **1.236 ảnh nằm trong VG**. Nghĩa là có khoảng 1,2K ảnh có cùng lúc caption người viết tiếng Việt (UIT-ViIC), SG tiếng Việt (VietSGG) và SG tiếng Anh do người gán (VG). Đây là bộ kiểm định metric gần như miễn phí, nhưng chỉ cho miền thể thao.
KTVIC/OpenViIC là ảnh Việt Nam, **không** có trong VG/COCO.

---

## 2. Tài nguyên KG và NLP tiếng Việt

| Tài nguyên | Đo được hôm nay | Ghi chú |
|---|---|---|
| **Wikidata nhãn `vi`** | Lấy 101 lớp object của bộ object-gold KTVIC (`data/object_gold/sample.json`). `wbsearchentities` (strictlanguage=vi) khớp đúng label/alias cho **78/101 (77%)**. Không khớp: biển báo, biển hiệu, dép, mèo(*), em bé, đứa trẻ, xe ba gác, xe đẩy, mái chèo... | (*) cận dưới, vì khớp theo chuỗi. SPARQL trên 10 từ cho thấy **nhập nhằng nghĩa**: `bát` → Q3565837 "bath"; `chợ` → market / marketplace / **forum**. Cha `P279` thường **thiếu nhãn vi** (dog Q144 có 1 cha nhưng 0 cha có nhãn vi; chair → "đồ nội thất" thì có). Kết luận: Wikidata dùng được làm **xương sống IsA**, nhưng phải map nghĩa bằng tay cho ~100-300 lớp (khoảng 1-2 ngày người) |
| **ConceptNet 5** | Wiki "Languages" ghi Vietnamese thuộc tier **"common"** (vocab ≥10K, có vector, không có API riêng), **54.774 term** | API 502 nên không đếm được số cạnh vi. Theo hiểu biết chung, cạnh vi chủ yếu là `Synonym`/`RelatedTo`/dịch từ Wiktionary, ít `AtLocation`/`UsedFor`. Khuyên đi qua tiếng Anh: vi → en (Wikidata/lexicon) → ConceptNet en |
| **WordNet tiếng Việt** | `zeloru/vietnamese-wordnet` chỉ là **danh sách từ** (cào từ viet.wordnet.vn và vi.wiktionary, 2018). Không có cấu trúc synset/hypernym dùng được | Không có viWordNet dùng được. `HYPERNYMS` trong `rescap/vi/lexicon.py` (~30 cặp) hiện là nguồn IsA duy nhất |
| **VnCoreNLP** | 678 sao, push cuối 2023-02, license NOASSERTION | Tách từ, POS, NER, dependency. Ổn định nhưng đứng yên |
| **underthesea** | 1.806 sao, Apache-2.0, push 2026-10-08 | Còn bảo trì, có dependency parse |
| **PhoBERT / PhoNLP** | PhoBERT MIT (repo), `vinai/phobert-base-v2` trên HF ghi **AGPL-3.0**. PhoNLP BSD-3 | PhoNLP là multi-task POS+NER+dep |
| **ViT5 / BARTpho** | `VietAI/vit5-base` MIT. BARTpho MIT | Đủ làm backbone seq2seq cho parser text→SG |
| **OpenIE / RE tiếng Việt** | `voducthuan/Vietnamese-OIE` (0 sao, Java, rule), `minhpqn/vlsp2020-relex` (RE VLSP 2020, quan hệ thực thể có tên) | Không phải relation thị giác. **Không dùng được** cho SG |
| **Parser text→scene graph** | Tiếng Anh: `lizhuang144/flan-t5-{small,base,large}-(VG-)factual-sg` (FACTUAL), `sqlinn/DiscoSG-Refiner-Large`. Tiếng Việt: **không có** | Đường tắt: vi→en bằng `vinai/vinai-translate-vi2en-v2` (AGPL-3.0) rồi FACTUAL parser. Cách này mất loại từ/số đếm, chỉ dùng làm baseline |
| **Từ vựng quan hệ VG dịch sang Việt** | Không có bản VG150 dịch chính thức. Gần nhất là **ontology 71 predicate của VietSGG** (thể thao) và 17 quan hệ không gian đóng trong `SPATIAL_RELATIONS` của VSPS | Gộp hai nguồn này cộng dịch 50 predicate VG150 thì được bộ ~100 predicate. Việc này mất khoảng 1 ngày, cần 2 người duyệt |
| VLSP 2025 viSemParse (web search, jcsce.vnu.edu.vn) | 2.500 câu, AMR-like, Smatch tốt nhất 58% | Là semantic parsing, không phải SG thị giác. Chưa mở bài gốc, xem "Chưa xác minh" |

---

## 3. Bộ sinh scene graph zero-shot cho ảnh Việt Nam, chi phí trên RTX 3090

| Lựa chọn | Trạng thái | Chi phí trên 3090 (ước lượng) | Nhận xét |
|---|---|---|---|
| **Qwen2.5-VL-7B prompt ra SG JSON** (kiểu CCoT) | Đã có trong VSPS (`rescap/vlm/qwen_vl.py`) | Đo trong repo: 4-bit, 512 visual token: **7,7 GB VRAM, 0,87 s/ảnh** cho caption ngắn (`data/vram/vram_4-bit-512vt_cap_12GB.json`). Caption chi tiết 160 token mất 2,06 s/ảnh *trên 4090* (`data/results/latency_main_s42.json`). SG JSON khoảng 300-500 token, nên **ước tính 5-10 s/ảnh trên 3090**. OpenViIC 13,1K ảnh mất khoảng 18-36 giờ GPU | Rẻ nhất, xuất thẳng nhãn Việt. Nhưng chưa được kiểm chứng, nên cần verifier |
| **Qwen3-VL-8B** | HF Apache-2.0 | ~như trên, 4-bit vừa 24 GB | Bản mạnh hơn cho bước sinh hoặc làm judge |
| **Pipeline VSPS hiện tại** (generate → verify K=5) | Có sẵn. **3.700 bản ghi stage-1** đã có (`data/stage1_records/stage1_records.tar.gz`) | ~80 s/ảnh do K=5 (file 05_efficiency). Đọc logit một lượt thì ước tính 8-16 s/ảnh | Đây là **silver SG đã kiểm chứng** cho ~3,7K ảnh KTVIC, miễn phí |
| **R1-SGG** (arXiv 2504.13617; `gpt4vision/R1-SGG` Apache-2.0; HF `JosephZ/R1-SGG-7B`, base Qwen2-VL-7B, apache-2.0) | Có trọng số | 7B nên giống Qwen 4-bit, khoảng 8-10 GB | Huấn luyện trên VG150/PSG nên **từ vựng đóng tiếng Anh**, phải dịch nhãn. Dùng làm baseline SGG chuẩn |
| **Pix2Grp** (CVPR 2024, `SHTUPLUS/Pix2Grp_CVPR2024`, BSD-3) | Có code | Vừa 24 GB khi suy luận | Open-vocab nhưng tiếng Anh. Mốc 2024 |
| **RelTR / EGTR** (`yrcong/RelTR` không license; `naver-ai/egtr` Apache-2.0) | Có code. VietSGG đã train trên ontology Việt | DETR-size, train trên 3090 được | Đóng từ vựng, phải train lại cho miền Việt |
| CAGE-SGG (arXiv 2604.22274), Min et al. ICCV 2025 | Chỉ thấy qua web search | — | Xem "Chưa xác minh" |

Kết luận phần 3: dùng **LVLM-prompted SG + verifier VSPS** để có silver graph tiếng Việt. Dùng R1-SGG/RelTR làm baseline. **Không cần** train SGG chuyên dụng.

---

## 4. Ngân sách gán nhãn gold SG 500 ảnh (để kiểm định metric)

Giả định: ảnh KTVIC test (558 ảnh, đã có 300 ảnh object-gold 101 lớp). Annotator **sửa** silver SG từ VSPS chứ không gán từ đầu. Mỗi ảnh mẫu có ~49 mệnh đề ứng viên (`sample_00000000002.json`: 15 attribute, 9 action, 8 entity, 8 counting, 5 spatial, 4 relation).

| Hạng mục | Ước lượng |
|---|---|
| Soạn guideline + ontology (~100 predicate, ~150 lớp) + pilot 30 ảnh | 2-3 ngày, 1 người |
| Sửa silver SG (chấp nhận/xóa/thêm node-edge) | ~5-7 phút/ảnh, tức **42-58 giờ/người** cho 500 ảnh |
| Gán kép 100% để đo agreement (κ / graph-F1 giữa người) | ×2, tức **85-115 giờ** |
| Phân xử bất đồng | ~10-15 giờ |
| Chấm người cho metric validation: 500 ảnh × 4 hệ thống, chấm caption 1-5 | ~2 phút/caption × 2.000 × 2 người, khoảng 130 giờ (có thể giảm còn 200 ảnh, ~55 giờ) |
| **Tổng** | **~150-260 giờ người**, tức 2 annotator × 3-4 tuần bán thời gian. Với mức 40-60K VND/giờ sinh viên (giả định, chưa khảo sát) thì khoảng **6-16 triệu VND** |

Công cụ: `data/object_gold/annotate.html` (một file HTML, giao diện gán object KTVIC) mở rộng thêm cạnh/quan hệ được, khoảng 1-2 ngày code. Script agreement có sẵn: `scripts/agreement.py`, `scripts/mark_double_annotated.py`, `scripts/object_gold_score.py`.
Phương án rẻ hơn: thử metric trước trên **1.236 ảnh UIT-ViIC ∩ VG**, vì đã có SG người (VG tiếng Anh) và VietSGG. Chỉ cần map ontology, không cần gán mới. Sau đó mới chi tiền cho 500 ảnh KTVIC.

---

## 5. Mã VSPS dùng lại được

| Thành phần | File | Dùng cho KG/SG |
|---|---|---|
| Schema mệnh đề có kiểu (entity/attribute/action/counting/spatial_relation/relation) + entity id + verdict 3 mức + probes | `rescap/pipeline/generate.py`, bản ghi `data/stage1_records/` | **Đã là scene graph**: entity thì thành node, attribute thành node-attr, relation/spatial/action thành edge. Chỉ cần một hàm `props → graph` (~50 dòng) |
| Verifier (VQA probe, geometric check bằng box, cross-proposition consistency) | `rescap/pipeline/verify.py` (`geometric_check`, `iou`, `normalise_relation`) | Kiểm chứng cạnh SG. Vị từ không gian từ bbox là phần RelCheck (arXiv 2609.27890) làm |
| Matching 3 tầng EXACT/LEXICAL/SOFT, entity-level | `rescap/svp/matching.py` | **Lõi của metric dạng SPICE tiếng Việt** đã có. Tầng LEXICAL dùng `SYNONYMS`/`HYPERNYMS` |
| Metric P/R/F1 mệnh đề, hallucination primary vs inherited, PGF/VCF | `rescap/metrics_svp.py` (`proposition_prf`, `hallucination_rates`, `pgf`) | Thành graph-P/R theo loại. Slot `pair.parsed_claims` **đã chờ sẵn parser ngoài** cho caption tự do. Đây chính là chỗ cắm ViSGParse |
| Lexicon Việt: loại từ, màu (xanh nhập nhằng), 17 quan hệ không gian đóng, synonym vùng miền, hypernym nông, non-visual markers | `rescap/vi/lexicon.py`, `classifier.py`, `color.py` | Ontology SG tiếng Việt và chuẩn hóa node. `HYPERNYMS` là chỗ thay bằng Wikidata P279 |
| CHAIR tiếng Việt + object gold 300 ảnh / 101 lớp | `rescap/chair.py`, `data/object_gold/` | Baseline để so metric đồ thị với CHAIR |
| Audit người 600 mệnh đề, human eval 2 rater | `data/annotations/audit_*`, `data/human_eval/` | Có sẵn dữ liệu người để tính tương quan metric, không cần gán mới cho pilot |
| VLM wrapper Qwen2.5-VL / Vintern, 4-bit, đo VRAM/latency | `rescap/vlm/`, `scripts/measure_vram.py`, `scripts/measure_latency.py` | Bộ sinh SG zero-shot và đo chi phí |

---

## 6. Bảng phán quyết khả thi

| Tài nguyên | Có chưa? | Chất lượng | Công sức để dùng | Rủi ro |
|---|---|---|---|---|
| Caption tiếng Việt người viết (UIT-ViIC, OpenViIC, KTVIC) | Có | Tốt nhưng **ngắn** (11-18 từ) | Thấp (đã có local KTVIC) | License không rõ (KTVIC, OpenViIC). Không có caption chi tiết |
| Caption chi tiết tiếng Việt | Chỉ bản dịch máy (5CD-AI ShareGPT4V) | Trung bình (dịch Google) | Thấp | Reviewer chê "translationese" |
| ViTextCaps | Có bài, **chưa phát hành** | — | Phải xin tác giả | Cao: có thể không lấy được |
| SG tiếng Việt có box | **Có: VietSGG** (2,9K ảnh, 71 predicate, CC BY 4.0) | Bán tự động (GPT-4), miền thể thao | Thấp | **Overlap/novelty**: không thể nói "bộ SG tiếng Việt đầu tiên" |
| SG người gán cho ảnh UIT | Gián tiếp: 1.236 ảnh UIT-ViIC ∩ VG (tiếng Anh) | Cao (VG) nhưng nhiễu | Trung bình (map ontology en→vi) | Chỉ thể thao, không đại diện ảnh Việt |
| SG cho ảnh đời sống Việt (KTVIC/OpenViIC) | Silver: 3,7K bản ghi VSPS. Gold: chưa | Silver: precision SUPPORTED 63,1% (audit) | Gold 500 ảnh: ~150-260 giờ người | Ngân sách và agreement thấp ở relation |
| Parser text→SG tiếng Việt | **Không có** | — | Trung bình: 1-2K caption gán + fine-tune ViT5/Qwen2.5-1.5B (vài giờ GPU) hoặc LLM prompt | Lỗi tách từ/loại từ. Baseline dịch→FACTUAL dễ thắng nếu làm ẩu |
| Metric đồ thị tiếng Việt | Không có công khai. **Lõi matching có sẵn trong VSPS** | — | Thấp | Phải chứng minh tương quan người > CHAIR/CIDEr |
| Wikidata vi | Có, 77% lớp object khớp label | Nhập nhằng nghĩa, cha P279 thiếu nhãn vi | Thấp-TB (map tay ~1-2 ngày) | Sai nghĩa (bát→bath) nếu tự động |
| ConceptNet vi | Có, 54.774 term (tier common) | Thấp cho quan hệ thường thức | Đi qua tiếng Anh | API đang chết (502). Cần tải dump ~GB |
| viWordNet | **Không** (chỉ có wordlist) | — | — | Phải dùng Wikidata thay |
| NLP stack (underthesea, VnCoreNLP, PhoBERT, ViT5) | Có | Tốt | Thấp | PhoBERT-v2 trên HF là AGPL-3.0 |
| Bộ sinh SG zero-shot (Qwen2.5-VL/Qwen3-VL prompt, R1-SGG) | Có | Chưa đo trên ảnh Việt | Thấp, ~5-10 s/ảnh trên 3090 (ước tính) | Ảo giác quan hệ, nên cần verifier VSPS |
| Phần cứng (1× RTX 3090) | Có | — | — | Đủ cho suy luận và QLoRA 7-8B. Không đủ để train SGG lớn từ đầu (cũng không cần) |

**Phán quyết tổng:** **KHẢ THI**, với điều kiện đi theo hướng "silver SG từ VSPS + parser/metric đồ thị tiếng Việt + gold nhỏ 300-500 ảnh". Tài nguyên thiếu duy nhất phải tự làm là (i) parser text→SG tiếng Việt và (ii) gold SG cho ảnh Việt. Cả hai đều vừa ngân sách một nhóm nhỏ. Rủi ro lớn nhất không nằm ở tài nguyên mà ở **novelty claim**: VietSGG đã chiếm danh nghĩa "Vietnamese SGG benchmark đầu tiên", nên phải đóng khung khác đi: caption chi tiết, metric, kiểm chứng ảo giác, ảnh đời sống Việt. Ngoài ra phải giải quyết **license KTVIC/OpenViIC** trước khi phát hành dữ liệu.

---

## 7. Chưa xác minh
- VietSGG có thật sự nằm trong proceedings EAI GOODTECHS 2025 không. Hiện chỉ có README GitHub; OpenAlex hết quota nên chưa tra được DOI.
- Số cạnh tiếng Việt của ConceptNet và phân bố loại quan hệ (API 502).
- Open Multilingual Wordnet có Vietnamese hay không (chưa kiểm).
- Min et al., "Vision-language interactive relation mining for open-vocabulary SGG", ICCV 2025, và CAGE-SGG (arXiv 2604.22274): chỉ thấy qua web search, chưa mở.
- VLSP 2025 viSemParse (2.500 câu, Smatch 58%): chỉ thấy qua snippet web search.
- "ViHallu / DSC2025": chỉ thấy qua trang tổng hợp emergentmind.
- Thời gian 5-10 s/ảnh cho SG JSON trên 3090 là **ước tính** ngoại suy từ số đo 4090/3090 trong repo, chưa chạy.
- Giờ người và đơn giá gán nhãn là **giả định**, chưa có số đo bấm giờ.
- 1.236 ảnh ∩ VG dựa trên giả định tên file VietSGG là COCO id (theo `rename_image.py`). Chưa đối chiếu bằng file id gốc của UIT-ViIC.
