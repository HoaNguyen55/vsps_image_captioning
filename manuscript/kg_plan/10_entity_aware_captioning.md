# 10. Entity-aware / knowledge-aware / news image captioning (2025-2026): có nên làm bản tiếng Việt gắn KG?

Ngày quét: 2026-10-10. Nguồn: Semantic Scholar Graph API (bulk search + batch, lấy abstract/venue/tác giả), trang arXiv abs/HTML (mở trực tiếp), arXiv listing search, HuggingFace Hub API, GitHub API. arXiv export API và OpenAlex bị rate-limit trong phiên này (429 / hết budget ngày), nên **không có số đếm theo năm mới**. Số xu hướng lấy lại từ `../research_wall/11` (OpenAlex: `entity-aware captioning OR news image captioning` đi ngang khoảng 10 bài/năm, 2025: 9, 2026*: 13).

## 0. Trả lời ngắn

- **Mô hình news captioning tiếng Anh (GoodNews/NYTimes800k)**: bão hòa. Bài mới nhất là MERGE (AAAI 2026), RAG trên KB thực thể đa phương thức. Thêm "KG vào bộ sinh caption tin tức" thì không mới.
- **Phần đang mở là đa ngôn ngữ và tiếng Việt.** MUNIChus (LREC 2026) là benchmark news captioning đa ngữ **đầu tiên**, có 9 ngôn ngữ, **không có tiếng Việt** (đã đọc bảng thống kê). MERLIN (TACL 2025) có tiếng Việt, nhưng chỉ cho **entity linking trên tiêu đề bài + ảnh** (1.000 tiêu đề, 1.343 mention, 475 thực thể Wikidata), **không có caption**. Quét S2 và arXiv không thấy bộ news/entity-aware captioning tiếng Việt nào.
- **Chỗ mới khả dĩ** (novelty trung bình-cao cho Q2/LREC/TALLIP): (1) bộ dữ liệu news captioning tiếng Việt có **caption gắn QID Wikidata**; (2) metric thực thể **so khớp theo QID** (khử bí danh và dấu, ví dụ "Hồ Chí Minh"/"Bác Hồ"/"Ho Chi Minh") **tách theo nguồn bằng chứng** (ảnh / bài báo / không có, tức bịa); (3) phương pháp **trung tính hóa thực thể 3 trạng thái** kiểu VSPS: tên riêng nào không kiểm chứng được thì hạ xuống danh từ chung ("một quan chức") thay vì đoán tên.
- **Khả thi trên RTX 3090: có.** MUNIChus đã QLoRA Llama-3.2-11B-Vision và aya-vision-8b ở 4-bit NF4. Qwen2.5-VL-7B/Qwen3-VL-8B với ngữ cảnh bài báo cắt còn khoảng 1,5-2K token là vừa. Việc nặng là **thu thập dữ liệu, bản quyền, và gán QID** cho tập test.
- **Lưu ý định vị:** hướng này **không chạy trên UIT-ViIC/KTVIC/OpenViIC**, vì caption ở đó là mô tả chung, gần như không có tên riêng. Muốn bám dữ liệu UIT thì chỉ có ViTextCaps (tên cửa hàng, thương hiệu trong scene text), xem 4.4.

---

## 1. Bản đồ 2025-2026 (đã mở và xác minh)

### 1.1 News / entity-aware captioning
| # | Bài | Venue | ID | Ý chính |
|---|---|---|---|---|
| N1 | MERGE: Knowledge Completes the Vision, Multimodal Entity-aware RAG for News Image Captioning (You et al.) | AAAI 2026 | arXiv 2511.21002 | KB thực thể đa phương thức (văn bản + ảnh + tri thức cấu trúc), hypothesis-caption nhiều bước, truy hồi động theo ảnh. GoodNews/NYTimes800k: CIDEr +6,84/+1,16, NER-F1 +4,14/+2,64. Zero-shot sang VisualNews: +20,17 CIDEr. **Đối thủ SOTA tiếng Anh.** |
| N2 | MUNIChus: Multilingual News Image Captioning Benchmark (Chen, …, Ranasinghe) | LREC 2026 | arXiv 2603.10613; HF `tharindu/MUNIChus` (cc-by-sa-4.0) | Nguồn BBC, 9 ngôn ngữ: ar, zh, en, fr, hi, id, ja, si, ur. **Không có vi.** 145K ảnh train, khoảng 1K test mỗi ngôn ngữ. Chỉ đo BLEU-4/CIDEr, **bỏ metric thực thể vì thiếu NER tốt cho ngôn ngữ ít tài nguyên** (tác giả tự nêu). Có bảng Qwen2.5-VL-7B và Qwen3-VL-8B zero-shot: BLEU-4 tổng khoảng 2,6; CIDEr tổng khoảng 25,7/29,4 (đọc từ bảng HTML, cần kiểm lại trước khi trích). QLoRA r=64 trên 8B/11B. |
| N3 | News Image Captioning via Separate Attention on Entity Categories (Ajankar & Dutta) | IEEE Access 2025 | 10.1109/ACCESS.2025.3582655 | Chú ý tách PER và GeoOrg, thêm ảnh lân cận trong cùng bài. |
| N4 | Hierarchical Multi-Modal Retrieval for Knowledge-Grounded News Image Captioning (M.-L. Nguyen, …, **Trung-Nghia Le**) | SOICT 2025 | arXiv 2606.18553 | Truy hồi bài báo theo cấu trúc (headline/body, vị trí ảnh), VLM mô tả, LLM ghép tri thức. |
| N5 | SEAR: RAG Image Captioning via Synthesized Entity-Aware Knowledge Representations | CIKM 2025 | 10.1145/3746252.3761265 | LLM dựng KG từ caption cụm, tỉa subgraph liên quan ảnh. |
| N6 | ExCap: Entity-aware zero-shot captioning via faithful synthetic alignment | Knowledge-Based Systems 2026 | 10.1016/j.knosys.2026.116639 | (Chưa đọc được abstract qua API.) |
| N7 | Entity-Faithful Repair of Synthetic Supervision for Zero-Shot Captioning | arXiv 2608.00994 | — | Sửa lệch ở mức thực thể trong dữ liệu tổng hợp. Đã nằm trong danh sách overlap của VSPS. |
| N8 | Negative Entity Suppression (NES) | arXiv 2511.08909 | — | Lọc "negative entity" khỏi nội dung truy hồi, nén attention. |
| N9 | EADIC: Entity Aware and Diverse Image Captioning | ETASR 2026 | 10.48084/etasr.18013 | CNN + token thực thể + RL. Venue yếu. |
| N10 | MsRAG: Knowledge-augmented captioning with object-level multi-source RAG | IJCAI 2025 | 10.24963/ijcai.2025/678 | Truy hồi theo đối tượng khi không có truy vấn người dùng. |
| N11 | Tell as You Want: image narrative with knowledge and thoughts | AAAI 2026 | 10.1609/aaai.v40i14.38180 | Mô tả giàu tri thức, tùy biến theo nhu cầu người dùng. |
| N12 | MEKA: external knowledge augmentation for social-media captioning | ICICT 2025 | 10.1109/ICICT64582.2025.00081 | Web search + reverse image search + NER. |

### 1.2 Event-enriched captioning (nhánh "kế nhiệm" GoodNews/VisualNews, nhóm Việt Nam dẫn dắt)
| # | Bài | Venue | ID | Ghi chú |
|---|---|---|---|---|
| E1 | OpenEvents V1 (H. Nguyen, …, **Minh-Triet Tran, Trung-Nghia Le**) | ACM MM 2025 | arXiv 2506.18372 | 200K bài và 400K ảnh từ **CNN + The Guardian, tiếng Anh**. 3 tác vụ: event-aware caption, image→article, text→image. |
| E2 | EVENTA Grand Challenge @ ACM MM 2025 | ACM MM 2025 | arXiv 2508.18904 | 45 đội. Chưa thấy công bố EVENTA 2026 (web search ngày 2026-10-10). |
| E3 | ReCap; ENRIC; EVENT-Retriever; ZSE-Cap | ACM MM 2025 / arXiv | 2509.01259; 10.1145/3746027.3762090; 2509.00751; 2507.20564 | Bài các đội dự thi: truy hồi bài báo rồi LLM viết caption. |
| E4 | Beyond Vision (Q. L. P. Nguyen et al.); CIAN (Trinh & T.-N. Le); Lightweight Entity Extraction for Event Retrieval | arXiv 2512.20042; 2606.17430; 2512.21221 | — | Đều chạy trên OpenEvents V1. CIAN báo CIDEr chỉ từ 0,030 lên 0,094, tức metric n-gram gần như vô nghĩa với caption sự kiện. Đây là lý lẽ để làm **metric dựa trên thực thể/KG**. |

### 1.3 Multimodal entity linking (MEL) và KG
| # | Bài | Venue | ID | Ghi chú |
|---|---|---|---|---|
| L1 | **MERLIN**: Multilingual Multimodal Entity Recognition and Linking (Ramamoorthy, …, Khanuja, Neubig) | TACL 2025 | arXiv 2510.14307; github rsathya4802/merlin | Tiêu đề BBC + ảnh, 5 ngôn ngữ **có vi**. Phần vi: 1.000 tiêu đề, 1.343 mention, 475 thực thể duy nhất, 170 mention không link được, Cohen's κ = 0,88. Ảnh giúp nhất ở PER. Gán nhãn bằng INCEpTION, 6 người Việt qua Prolific. |
| L2 | Think Before You Link: Rarity, Reasoning, Retrieval in Multilingual EL (Pengpun, Khanuja, Neubig) | EMNLP 2026 | arXiv 2609.10745 | VLM có suy luận tự tìm trên Wikipedia. Trên MERLIN: +6,9% tổng, tới +23,3% ở thực thể hiếm. Phát hành MERLIN-Rare. |
| L3 | KGMEL (SIGIR 2025, arXiv 2504.15135); DeepMEL (IP&M 2025, 2508.15876); VP-MEL (Findings ACL 2025); ThinkLinker (Findings ACL 2026) | — | — | MEL đơn ngữ (chủ yếu tiếng Anh/Trung), dùng LLM/KG. Có thể lấy làm baseline linker. |
| L4 | WikiVQABench (arXiv 2605.21479) | — | — | VQA dựa trên Wikipedia + Wikidata, có người duyệt. Là mẫu cho "tri thức ngoài ảnh". |

### 1.4 Nền (trước 2025, chỉ một dòng)
GoodNews (Biten 2019), NYTimes800k/Transform-and-Tell (Tran 2020), VisualNews (Liu 2021), multimodal KG cho entity-aware captioning (arXiv 2107.11970, TMM 2023), LMM cho contextualized news captioning trên GoodNews (arXiv 2408.04331), M3LS (arXiv 2302.06560, BBC 20 ngôn ngữ), XL-HeadTags (ACL 2024).

---

## 2. Tiếng Việt: hiện có gì?

| Tài nguyên | Có tiếng Việt? | Có caption? | Có link KG? |
|---|---|---|---|
| MUNIChus (BBC news captioning) | **Không** | Có | Không |
| MERLIN | **Có** (1.000 tiêu đề) | **Không** (chỉ tiêu đề) | Có (Wikidata) |
| M3LS | **Không**: danh sách crawler trên GitHub có 20 ngôn ngữ, không có vi (đã kiểm `scrapy-code/`) | Có (ảnh + caption) | Không |
| OpenEvents V1 / EVENTA | Không (CNN/Guardian) | Có (caption sự kiện) | Không |
| MERVIN (arXiv 2605.16120), AI Challenge HCMC | Có (video tin tức VN) | Không (truy hồi sự kiện) | Không |
| UIT-ViIC / KTVIC / UIT-OpenViIC / HDUCap (JVCIR 2026) / ViG (MAPR 2026) | Có | Có, nhưng **mô tả chung, không tên riêng** | Không |
| ViTextCaps (arXiv 2604.27712) | Có | Có, có scene text (tên quán, biển hiệu) | Không |
| KG tiếng Việt | VietMedKG (TALLIP 2025), KG pháp luật, lịch sử, fact-checking | — | KG văn bản, không đa phương thức |

**Kết luận:** **chưa có** bộ news/entity-aware image captioning tiếng Việt, và chưa có caption tiếng Việt nào gắn Wikidata. Các truy vấn đã chạy: S2 `Vietnamese +(caption|captioning)` 2025-26 (21 kết quả), `Vietnamese +news +(image|multimodal)`, `Vietnamese +multimodal +(NER|entity linking)` 2018-26, arXiv `Vietnamese news image`, `VnExpress`. Lỗ hổng có thật và **đối chứng được** nhờ MUNIChus (bài tự nhận tiếng Anh độc quyền, và họ không chọn vi).

Điểm lạ cần ghi chú: MERLIN viết rằng tiêu đề được chọn "from M3LS", nhưng crawler M3LS không có tiếng Việt. Nguồn của phần vi trong MERLIN vì vậy chưa rõ (xem mục Chưa xác minh).

---

## 3. Đánh giá theo 3 trục

### 3.1 OVERLAP
| Đối thủ | Mức | Vì sao | Khác biệt phải giữ |
|---|---|---|---|
| MUNIChus (Surrey/Lancaster) | **Cao nếu chỉ làm "thêm tiếng Việt"** | Cùng nguồn BBC, cùng giao thức. Họ có thể thêm vi ở v2. | Phải có **KG-link + metric thực thể + phương pháp**, không dừng ở bộ dữ liệu. Nên lấy cả nguồn báo Việt, không chỉ BBC Tiếng Việt. |
| MERLIN / Think Before You Link (CMU) | Trung bình | Đã có EL đa phương thức tiếng Việt. | Họ link tiêu đề, còn ta link **caption sinh ra** và dùng link để **đánh giá/kiểm chứng**. Có thể tái dùng MERLIN-vi làm tập dev cho linker. |
| MERGE (AAAI 2026) | Trung bình | KB thực thể + RAG cho news captioning. | Tiếng Anh, không trung tính hóa, không kiểm chứng 3 trạng thái, metric NER-F1 so chuỗi. |
| Nhóm HCMUS (T.-N. Le, M.-T. Tran): OpenEvents, EVENTA, CIAN, N4 | **Rủi ro cạnh tranh cao nhất** | Người Việt, có hạ tầng crawl tin tức và tổ chức challenge, có thể ra "OpenEvents-Vi". | Đi nhanh và nhấn mạnh KG/QID và faithfulness thực thể, thứ họ chưa làm (họ dùng BLEU/CIDEr và retrieval mAP). Cân nhắc liên hệ hợp tác. |
| Entity-Faithful Repair, NES | Thấp-trung bình | Faithfulness mức thực thể, nhưng là thực thể đối tượng (dog, car), không phải tên riêng, và là zero-shot captioning. | Trích dẫn và phân biệt. |

### 3.2 NOVELTY (theo thứ tự mạnh đến yếu)
1. **Metric thực thể theo QID có nguồn bằng chứng** (gọi tạm là *EntQID-F1 / EntHall*): mỗi tên riêng trong caption được link sang QID và gán 1 trong 3 nhãn: (a) **có trong bài báo**, (b) **chỉ suy ra từ ảnh** (biển hiệu, logo, khuôn mặt nổi tiếng), (c) **không có bằng chứng**, tức bịa. MUNIChus bỏ hẳn metric thực thể. MERGE dùng NER-F1 so chuỗi. CIAN cho thấy CIDEr gần 0. Chưa thấy bài 2025-26 nào đo ảo giác **tên riêng** theo QID cho caption, kể cả tiếng Anh (quét `entity hallucination caption`, kết quả không trúng). Đây là đóng góp mạnh nhất.
2. **Trung tính hóa thực thể 3 trạng thái** (mở rộng VSPS): tên được bài báo và ảnh cùng ủng hộ là SUPPORTED, giữ tên. Tên chỉ có trong bài nhưng không xác định được ai trong ảnh là UNCERTAIN, viết thành vai trò ("Thủ tướng [tên] (thứ hai từ trái)" chuyển thành "các đại biểu, trong đó có Thủ tướng [tên]", hoặc chỉ ghi chức danh). Tên trái với ảnh hay KG (sai giới, sai quốc tịch, đã mất) là REJECTED. Chưa thấy ai làm. Gần nhất là REVERSE (backtrack lúc suy luận) và MERGE (truy hồi), nhưng không có trạng thái UNCERTAIN cho tên riêng.
3. **Bộ ViNewsCap-KG**: bộ news captioning tiếng Việt đầu tiên, có QID ở caption. Mới, nhưng là đóng góp *tài nguyên*.
4. "Bơm KG Wikidata vào bộ sinh": **không mới** (A1 TMM 2023, MERGE). Chỉ dùng làm baseline hoặc thành phần.

### 3.3 FEASIBILITY
| Hạng mục | Đánh giá | Ghi chú |
|---|---|---|
| GPU | Cao | QLoRA Qwen2.5-VL-7B / Qwen3-VL-8B. Ngữ cảnh: ảnh 448-672px + tóm tắt hoặc đoạn bài liên quan khoảng 1,5K token (MUNIChus trung bình 1.412 token nội dung). Vintern-3B làm backbone thứ 2 (chuẩn ≥2 backbone, xem 00_TONG_HOP §3). |
| Dữ liệu thô | Cao về kỹ thuật | BBC Tiếng Việt (bbc.com/vietnamese) có caption biên tập sẵn dưới ảnh, crawl theo đúng quy trình MUNIChus. Có thể thêm VnExpress/VietnamPlus/Tuổi Trẻ. |
| Bản quyền | **Rủi ro** | MUNIChus phát hành BBC dưới cc-by-sa-4.0 (tiền lệ, nhưng chưa chắc đúng pháp lý). Báo Việt thường cấm sao chép: chỉ phát hành URL + script + caption/QID, không phát hành ảnh. |
| Entity linking tiếng Việt | Trung bình | Wikidata có nhãn và alias tiếng Việt cho thực thể lớn. Thực thể địa phương (xã, cán bộ cấp tỉnh, doanh nghiệp nhỏ) **thiếu QID**: MERLIN-vi có 170/1.343 (12,7%) mention không link được. Cần nhãn NIL. Linker: NER tiếng Việt (PhoBERT-NER/VLSP) + truy vấn `wbsearchentities` (language=vi) + Qwen2.5-7B rerank. MERLIN-vi dùng làm dev. |
| Gán nhãn test | Tốn công nhất | Khoảng 1.000-1.500 ảnh test: 2 người gán QID cho mention trong caption tham chiếu, và nhãn nguồn bằng chứng (bài/ảnh/không) cho caption của khoảng 4 hệ thống trên 300 ảnh. Ước tính 3-4 tuần × 2 người (MERLIN: 6 người cho 1.000 tiêu đề). |
| Nhận diện "ai trong ảnh" | Thấp | Face recognition người nổi tiếng là vùng nhạy cảm đạo đức. **Khuyên không làm**, để UNCERTAIN xử lý (ý 2), và ghi điều này thành nguyên tắc đạo đức trong bài. |

---

## 4. Đề xuất cụ thể

### 4.1 Nhiệm vụ: Vietnamese KG-grounded News Image Captioning
Đầu vào: ảnh + bài báo tiếng Việt (tiêu đề, sapo, thân bài). Đầu ra: caption kiểu báo chí có tên riêng. Mỗi tên riêng mang QID hoặc NIL (ở chế độ đánh giá, linker tự gán; không bắt mô hình xuất QID).

### 4.2 Dữ liệu cần
| Thành phần | Quy mô | Nguồn / cách làm |
|---|---|---|
| Train | 30-60K cặp (ảnh, bài, caption gốc) | BBC Tiếng Việt (ưu tiên vì có tiền lệ phát hành) + 1-2 báo Việt (chỉ URL). Lọc caption < 5 từ, ảnh đồ họa, ảnh trùng. |
| Dev/Test | 2 × khoảng 1.000 | Tách theo **thời gian** (bài sau ngày cắt dữ liệu của Qwen3-VL) để đo khả năng dựa vào bài báo thay vì trí nhớ. |
| QID cho caption test | khoảng 1.000 ảnh | Người gán (INCEpTION như MERLIN), kèm κ. |
| Nhãn nguồn bằng chứng | 300 ảnh × 4 hệ thống | Để kiểm định metric (tương quan với người). |
| KG con | khoảng 5-20K QID | Wikidata dump, lọc nhãn vi + P31/P279 (giống MERLIN), thêm P106 (nghề), P39 (chức vụ), P27 (quốc tịch), P21 (giới) phục vụ kiểm tra REJECTED. |

### 4.3 Phương pháp (khung, chạy trên 3090)
1. **Article→entity graph**: NER + link tiếng Việt trên bài, thu nút QID kèm thuộc tính Wikidata (chức vụ, giới, quốc tịch).
2. **Visual propositions** (tái dùng pipeline VSPS): mệnh đề có kiểu về người, số lượng, hành động, biển chữ (OCR).
3. **Đối chiếu**: mỗi tên trong caption ứng viên (K=5 mẫu) được gán SUPPORTED (có trong bài + khớp ràng buộc ảnh: giới, số người, OCR), UNCERTAIN (chỉ có trong bài) hoặc REJECTED (không có trong bài/KG, hoặc vi phạm ràng buộc). Cuối cùng render lại caption: SUPPORTED giữ tên, UNCERTAIN chuyển thành chức danh/vai trò, REJECTED bỏ.
4. SFT QLoRA trên caption đã kiểm chứng (giống VSPS), so với SFT trên caption gốc, MERGE-style RAG, và zero-shot.

Baseline: Qwen2.5-VL-7B / Qwen3-VL-8B / Vintern-3B zero-shot có và không có bài báo; SFT caption gốc; truy hồi entity-KB kiểu MERGE (bản rút gọn); ZSE-Cap-style prompt.

### 4.4 Phương án bám dữ liệu UIT (nếu bắt buộc)
ViTextCaps: scene text có tên quán, thương hiệu, địa danh. Có thể làm "scene-text entity linking": link token OCR sang Wikidata/OSM, rồi đo EntQID-F1 cho caption scene-text. Quy mô thực thể có QID chắc nhỏ (cửa hàng địa phương phần lớn NIL), nên **chưa xác minh được tỷ lệ link**. Cần pilot 200 ảnh trước khi cam kết.

### 4.5 Metric
- **EntQID-P/R/F1**: so tập QID giữa caption sinh ra và tham chiếu (khắc phục alias, viết tắt, có dấu/không dấu).
- **EntHall@article**: tỷ lệ QID trong caption không có trong bài, cũng không có trong OCR ảnh.
- **EntConstraint-violation**: tên vi phạm thuộc tính KG so với mệnh đề ảnh (ví dụ P21 khác giới người duy nhất trong ảnh).
- **Neutralization precision**: trong các tên bị trung tính hóa, bao nhiêu thật sự không xác định được (người đánh giá).
- Kiểm định: Kendall τ với đánh giá người trên 300×4. So với CIDEr, CLIPScore và NER-F1 so chuỗi kiểu MERGE.

### 4.6 Lịch (khoảng 5 tháng, 1 GPU)
| Tháng | Việc |
|---|---|
| 1 | Crawl BBC-vi, lọc, tách theo thời gian. Pilot: Qwen3-VL-8B zero-shot trên 200 ảnh; đo tỷ lệ tên bịa (go/no-go: nếu < 5% thì metric ảo giác kém thuyết phục, chuyển trọng tâm sang EntQID-F1). |
| 2 | Linker tiếng Việt (đánh giá trên MERLIN-vi), KG con, gán QID tập test. |
| 3 | Pipeline 3 trạng thái + SFT 2 backbone. |
| 4 | Baseline, ablation, gán nhãn người 300×4, kiểm định metric. |
| 5 | Viết. Đích: LREC-COLING / TALLIP (tài nguyên + metric) hoặc ghép thành chương "entity" trong bản Q2 của VSPS. |

### 4.7 Quan hệ với VSPS và các ý trong 11_knowledge_graph_captioning.md
- Đây là **phiên bản thực thể có tên** của ý 1 (verified scene graph) và ý 2b (trung tính hóa theo phân cấp IsA). Ở đây phân cấp là Wikidata P31/P39: người → chức danh → "một quan chức".
- Câu chuyện chung cho một bài lớn: *"verify-then-neutralize" cho cả thực thể chung (VSPS, KTVIC) lẫn thực thể có tên (ViNewsCap-KG)*, với metric đồ thị/QID thay cho n-gram.
- Nếu chỉ chọn một hướng KG cho bài Q2 sắp tới: ý 1 của file 11 rẻ hơn (không cần data mới). Hướng của file này hợp làm **bài thứ hai** (tài nguyên + metric), vì chi phí chủ yếu là dữ liệu.

---

## 5. Chưa xác minh
- MERLIN ghi phần tiếng Việt lấy "from M3LS", nhưng crawler M3LS (GitHub) và thẻ SEACrowd không có tiếng Việt. Nguồn thật của MERLIN-vi chưa rõ; có thể nhóm tự crawl BBC Tiếng Việt.
- Số Qwen2.5-VL/Qwen3-VL trên MUNIChus (CIDEr khoảng 25,7/29,4, BLEU-4 khoảng 2,6) được đọc từ bảng HTML đã làm phẳng. Thứ tự cột suy theo Bảng 1. Cần mở PDF kiểm lại trước khi trích.
- ExCap (KBS 2026): chưa đọc được abstract.
- XL-HeadTags (20 ngôn ngữ) có tiếng Việt hay không: chưa kiểm.
- EVENTA 2026 / OpenEvents bản tiếng Việt: web search không thấy, nhưng trang chủ challenge chưa mở được.
- Độ phủ nhãn tiếng Việt của Wikidata cho thực thể tin tức trong nước, và khả năng Qwen3-VL/Vintern nhận diện người nổi tiếng Việt Nam: chưa đo; cần pilot ở tháng 1.
- Điều khoản sử dụng nội dung BBC Tiếng Việt / VnExpress để phát hành dataset: chưa kiểm; cần tư vấn trước khi công bố.
- Số đếm xu hướng 2025-2026 không chạy lại được (OpenAlex/arXiv API bị giới hạn trong phiên này); dùng số của file 11.

## Nguồn web (ngoài API)
- [EVENTA ACM MM 2025 (HCMUS)](https://aichallenge.hcmus.edu.vn/acm-mm-2025/eventa)
- [arXiv 2508.18904 EVENTA](https://arxiv.org/abs/2508.18904v1)
- [arXiv 2512.20042](https://arxiv.org/abs/2512.20042v1)
- [OpenEvents V1 PDF](https://web3.arxiv.org/pdf/2506.18372)
