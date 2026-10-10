# 20. Gióng hàng KG xuyên ngôn ngữ và entity linking cho tiếng Việt (2024-2026)

Agent 20, ngày 2026-10-10. Góc nhìn: nối từ chỉ đối tượng tiếng Việt (bộ từ vựng 113 mục của VSPS) với Wikidata / ConceptNet / WordNet, có **thử thật** trên Wikidata API, rồi chọn KG nền cho hệ captioning tiếng Việt dùng KG.

**Kết luận ngắn:** Nên dùng **một tập con Wikidata cố định (snapshot), neo bằng QID**, lấy sang WordNet qua thuộc tính P8814 để nối với Visual Genome/COCO. Tầng quan hệ thị giác thì **tự dựng** (custom), lấy từ mệnh đề đã kiểm chứng của VSPS. Không nên dùng ConceptNet làm nền: API công khai đang chết (HTTP 502 trong phiên này), dữ liệu đóng băng ở bản 5.7 (2019), và độ phủ tiếng Việt chưa đo được. Entity linking cho *từ chỉ đối tượng* (không phải tên riêng) dễ hơn nhiều so với NEL kinh điển: trên 20 mục, top-1 của Wikidata search đúng **18/20**.

---

## 1. Bộ từ vựng đối tượng (113 mục) trong repo

- Vị trí: `rescap/vi/lexicon.py`, dict `NOUN_CLASSIFIER` (danh từ đầu → loại từ). Đếm được **113 khoá**. Đi kèm có `SYNONYMS` (24 mục) và `HYPERNYMS` (27 mục), ví dụ `xe đạp → phương tiện` hay `chó → động vật`.
- Đây là danh sách viết tay. Docstring của file tự nhận là chưa đầy đủ: từ không có trong danh sách thì rơi về so khớp chuỗi.
- Hệ quả cho KG: `HYPERNYMS` hiện là một cây phân loại 1 tầng tự chế. Đổi sang chuỗi P279 (subclass of) của Wikidata sẽ có cây sâu hơn, tái lập được và có nguồn để trích dẫn.

## 2. Thử nghiệm: 20 mục → Wikidata (đã chạy, có số liệu thật)

**Cách làm.** Gọi `wbsearchentities` với `language=vi, strictlanguage=1, type=item, limit=20`, ẩn danh. Chọn 20 mục: 10 mục "dễ" (động vật, xe cộ, đồ vật đặc thù Việt Nam) và 10 mục được chọn có chủ đích vì **đa nghĩa** (áo, ô, đường, cây, quả, bóng, cầu, chợ, bàn, người). Nghĩa đúng (gold QID) do agent tự gán theo nghĩa *đối tượng thị giác*. Ambiguity = số ứng viên có label/alias tiếng Việt trùng khớp chính xác với từ.

| Từ | Gold QID (en) | Hạng của gold | Số ứng viên khớp chính xác | Ứng viên gây nhiễu |
|---|---|---|---|---|
| người | Q5 human | 1 | 2 | Q215627 (khái niệm "person") |
| chó | Q144 dog | 1 | 1 | |
| mèo | Q146 cat | 1 | 0* | label là "mèo nhà", còn "mèo" chỉ là alias |
| xe máy | Q34493 motorcycle | 1 | 1 (alias) | label là "mô tô" |
| xe đạp | Q11442 bicycle | 1 | 1 | |
| ô tô | Q1420 car | 1 | 2 | Ô Tô (thành phố, Tân Cương) |
| xe buýt | Q5638 bus | 1 | 1 | |
| thuyền | Q35872 boat | 1 | 1 | |
| xích lô | Q1362895 cycle rickshaw | 1 | 2 | phim *Xích lô* (1995) |
| nón lá | Q77910039 | 1 | 1 | |
| **áo** | Q11460 clothing / Q76768 shirt | **không có trong top-20** | 4 | Áo (quốc gia), họ Áo, ... |
| ghế | Q15026 chair | 1 | 1 | |
| bàn | Q14748 table | 1 | 2 | Bàn (thành phố, Quý Châu) |
| ô | Q41607 umbrella | 1 | 2 | chữ cái Ô |
| đường | Q34442 road / Q79007 street | 1 | **6** | đường (sucrose), họ Đường, nhà Đường, ... |
| cây | Q10884 tree | 1 | 3 | cây (cấu trúc dữ liệu), cây (đồ thị) |
| quả | Q1364 fruit | 1 | 2 | trang định hướng |
| **bóng** | Q18545 ball | **2** | 2 | top-1 là Q160020 "Đổ bóng" (shadow) |
| cầu | Q12280 bridge | 1 | 2 | cung–cầu (alias) |
| chợ | Q330284 marketplace / Q132510 market | 1 | 3 | "loại hiến chương" |

**Kết quả trên 20 mục:**
- **hit@1 = 18/20 (90%)**, **hit@20 = 19/20 (95%)**.
- **Đa nghĩa (≥2 ứng viên khớp chính xác) = 12/20 (60%)**. Số ứng viên khớp trung bình khoảng 2,1, nhiều nhất là 6 (*đường*).
- Bộ lọc kiểu "chỉ giữ ứng viên có P279", với giả thuyết rằng từ chỉ đối tượng thì gọi tên *lớp*: cũng đạt **18/20**. Bộ lọc này loại đúng thành phố, họ và phim, nhưng không cứu được *bóng* (vì shadow cũng là một lớp) hay *áo* (vì gold không nằm trong top-5). Truy vấn SPARQL `P279* → physical object (Q223557)` bị **timeout (504)** nên không dùng được làm bộ lọc trực tuyến.
- Hai lỗi đều mang tính hệ thống: (i) **từ đơn tiết bị trùng với tên riêng Hán-Việt** (Áo = Austria, Đường = nhà Đường); (ii) **trùng nghĩa trừu tượng hoặc hiện tượng** (bóng = shadow). Ngữ cảnh caption, chẳng hạn "đá **bóng**" hay "mặc **áo** đỏ", giải quyết được cả hai. Đây là chỗ cho linker dùng LLM hoặc dùng ngữ cảnh (mục 4).

**Quét toàn bộ 113 mục** (chỉ đo độ phủ, không có gold): 87/113 có ít nhất một ứng viên khớp chính xác label/alias, và 40/113 có ≥2 ứng viên. Con số 87 là **cận dưới** vì phép so chuỗi của agent quá chặt:
- *mèo* có alias "mèo" nhưng API trả về `match.text` là "mèo nhà";
- *toà nhà* bị tính là trượt, nhưng Wikidata tự chuẩn hoá vị trí dấu thanh và trả về Q41176 "tòa nhà" ở hạng 1. Vì vậy **bắt buộc chuẩn hoá NFC và kiểu bỏ dấu cũ/mới (toà/tòa)** trước khi so khớp.
- Các mục trượt thật chủ yếu là **cụm mô tả hoặc phân loại xã hội**, không phải khái niệm KG: *nam thanh niên, cô gái trẻ, bạn trẻ, đôi bạn, con vật, đứa trẻ, dãy nhà, mỏm đá, con đường*, cùng một số đồ vật hẹp (*cọc neo, bánh lái, mái chèo, biển báo, xe ba gác, dép, dù*). Muốn link các mục này thì phải **tách lấy danh từ đầu** (con đường → đường; cô gái trẻ → cô gái + thuộc tính "trẻ") hoặc tra qua nhãn tiếng Anh.

**Cầu nối sang WordNet/Visual Genome (đã kiểm tra):** 19/20 gold QID có **P8814 (WordNet 3.1 synset ID)**, ví dụ dog → `02086723-n`. Chỉ *nón lá* là không có. Như vậy chuỗi `từ Việt → QID → synset WN3.1` nối thẳng được sang nhãn đối tượng của Visual Genome (VG dùng synset WordNet; cần bảng chuyển offset 3.0↔3.1). Mục đặc thù Việt Nam không có synset (*nón lá*) thì bắt buộc đi qua P279 (nón lá ⊂ nón/hat).

Script thử nằm ở scratchpad của phiên (`kg20/wd.py, rank.py, classfilter.py, all113.py`), dùng stdlib, không cần khoá API. Chạy lại khoảng 2 phút. Nếu cần đưa vào repo thì nên đặt ở `tools/`.

## 3. Tài liệu 2024-2026 (đã mở hoặc xác nhận trong phiên)

| Mục | Nguồn | Liên quan |
|---|---|---|
| MERLIN: testbed cho multilingual multimodal entity recognition & linking | arXiv 2510.14307 (2025-10-16) | **Có tiếng Việt.** Tiêu đề tin BBC kèm ảnh, 5 ngôn ngữ (hi, ja, id, **vi**, ta), khoảng 7K mention → khoảng 2,5K thực thể Wikidata. Thêm ảnh giúp nhiều nhất cho LLM yếu đa ngữ. Đây là benchmark EL đa phương thức tiếng Việt *gần nhất* với captioning, nhưng là thực thể có tên (người, tổ chức) chứ không phải đối tượng. |
| LELA: end-to-end LLM-based EL, zero-shot domain adaptation | arXiv 2605.26956 (2026-05); IJCAI-26 theo kết quả tìm kiếm (chưa mở PDF proceedings) | LLM làm bộ phân giải zero-shot trên KB bất kỳ. Mẫu thiết kế cho bước "chọn QID theo ngữ cảnh caption". |
| DBLPLink 2.0 | arXiv 2507.22811 (2025-07) | Xếp hạng lại ứng viên bằng log-prob của token "yes" từ LLM. Đây là cách rẻ nhất để phân giải *bóng/áo/đường* bằng Qwen hoặc Vintern trên 3090. |
| LLMs as Cultural Archives: Cultural Commonsense KG Extraction | arXiv 2601.17971, **EACL 2026 main** | KG commonsense văn hoá do LLM trích *tốt hơn khi trích bằng tiếng Anh*, kể cả với văn hoá phi Anh. Nên dựng tri thức bằng tiếng Anh rồi neo QID, thay vì sinh trực tiếp bằng tiếng Việt. |
| Do LLMs exhibit the same commonsense capabilities across languages? (MULTICOM) | arXiv 2509.06401 (2025-09) | Commonsense của LLM ở ngôn ngữ ít tài nguyên kém hơn rõ rệt. Đây là rủi ro khi dùng LLM sinh KG tiếng Việt. |
| mCSQA | arXiv 2406.04215, Findings ACL 2024 | Dựng QA commonsense đa ngữ từ đồ thị con ConceptNet + LM + người. Không thấy có tiếng Việt trong phần đã đọc. |
| Nền (một dòng mỗi mục) | DaMuEL arXiv 2306.09288 (2023, 53 ngôn ngữ, có vi, KB = Wikidata); Botha et al. EMNLP 2020 (EL 100+ ngôn ngữ); ReFinED arXiv 2207.04108 | Dữ liệu huấn luyện EL đa ngữ có tiếng Việt *đã có*, nhưng đều cho tên riêng. |

**Khoảng trống xác nhận được:** không tìm thấy (qua WebSearch và arXiv abs) bài 2024-2026 nào về **entity linking hoặc concept linking cho danh từ đối tượng tiếng Việt**, **Vietnamese WordNet bản mới** (bản gần nhất tìm được là Lam & Kalita, *Computación y Sistemas* 2022, xây bằng dịch máy wordnet), hay **multilingual KG embedding đánh giá trên tiếng Việt**. Kết hợp với `11_knowledge_graph_captioning.md` §3.2 thì phía tiếng Việt đang trống cả về KG thị giác lẫn về linking.

## 4. Khả thi / Trùng lặp / Mới

- **Khả thi: cao.** Wikidata search + lọc P279 + xếp hạng lại bằng LLM theo ngữ cảnh caption (kiểu DBLPLink 2.0 / LELA, dùng Qwen2.5-VL-7B hoặc Vintern-3B 4-bit) chạy được trên một 3090. Lexicon chỉ có 113 mục (sau này vài nghìn), nên **có thể gán gold bằng tay toàn bộ** và cache QID. Không cần linker trực tuyến lúc huấn luyện. Snapshot Wikidata cho khoảng 5-10K lớp liên quan (bao đóng P279 của các QID gốc) chỉ cỡ vài chục MB.
- **Trùng lặp: thấp.** MERLIN là thứ duy nhất có tiếng Việt và đa phương thức, nhưng nhắm tên riêng trong tin tức. EL bằng LLM (LELA, DBLPLink) chỉ là công cụ, không phải đóng góp cạnh tranh.
- **Mới: trung bình.** "Lexicon đối tượng tiếng Việt neo Wikidata/WordNet" tự nó là đóng góp *tài nguyên*, chưa đủ làm phương pháp. Giá trị nằm ở chỗ nó là **lớp chuẩn hoá nút** cho (a) scene graph mệnh đề của VSPS, (b) metric dạng đồ thị tiếng Việt (SPICE-vi, khớp nút theo QID và hypernym P279 thay vì chuỗi), và (c) gióng nhãn với VG/COCO để mượn dữ liệu scene graph tiếng Anh.

## 5. Khuyến nghị KG nền

1. **Nền chính: tập con Wikidata cố định.** Nút là QID, label/alias `vi` + `en`, cạnh phân loại là P279/P31, cạnh thành phần là P527/P361. Lý do: đã đo được độ phủ vi tốt (hit@1 90% trên tập khó), cập nhật liên tục, có P8814 để nối WordNet/VG, và giấy phép CC0. Ghi rõ ngày snapshot để tái lập.
2. **Tầng quan hệ thị giác: tự dựng.** Bộ ba (chủ thể, quan hệ không gian/hành động, đối tượng) lấy từ mệnh đề *đã kiểm chứng* của VSPS, với nút là QID. Wikidata gần như không có quan hệ kiểu "người *đội* nón lá" hay "xe máy *đỗ trên* vỉa hè". Đây là phần mới, và là thứ metric hay hệ kiểm chứng thật sự cần.
3. **ConceptNet: chỉ tham khảo hoặc làm baseline**, không làm nền. Lý do: API trả 502 trong phiên (index HF `conceptnet5/conceptnet5` cũng không tải xong để đếm cạnh `vi`), dữ liệu đóng băng từ 2019, và reviewer năm 2026 coi "ConceptNet + captioning" là hướng cũ (xem tệp 11 §4.1). Nếu cần commonsense thì lấy qua nhãn `en` của QID.
4. **WordNet: chỉ làm cầu nối**, đi qua P8814. Không phụ thuộc vào một Vietnamese WordNet riêng, vì chưa thấy bản mở nào được bảo trì 2024-2026.
5. **Linker:** (i) chuẩn hoá NFC và dấu thanh, tách danh từ đầu (dùng lại `NOUN_CLASSIFIER`, ưu tiên khớp dài nhất); (ii) tra bảng QID đã gán tay cho từ có trong lexicon; (iii) với từ ngoài lexicon, lấy `wbsearchentities` top-5 → lọc P279 → để VLM chọn theo ngữ cảnh caption (prompt có/không), log mọi quyết định. Thêm kiểm tra: tập 20 mục ở trên làm test hồi quy, ngưỡng hit@1 ≥ 18/20.

## Chưa xác minh

- Độ phủ ConceptNet tiếng Việt (số cạnh `/c/vi/`): API 502 và index HF chưa tải xong, nên **không có số**.
- Venue IJCAI-26 của LELA: thấy qua kết quả tìm kiếm (ijcai.org/proceedings/2026/0966.pdf) nhưng chưa mở PDF.
- Trạng thái tiếng Việt trong Open Multilingual Wordnet 2.x: chưa xác nhận.
- Bảng chuyển offset WordNet 3.0 ↔ 3.1 cho synset của Visual Genome: biết là có, nhưng chưa thử trên dữ liệu VG.
- OpenAlex và Semantic Scholar bị giới hạn tần suất trong phiên (nhiều agent chạy song song), nên chưa đếm được số bài theo năm cho góc này.
