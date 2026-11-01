# Bài C — hướng PVR, bản v4.1 theo PI-1101u và CC-219 (02/11/2026)

**v4.1 = v4 (`C_DIRECTION_v4_2026-11-01.md`, sha 6cf5cb5f, giữ nguyên byte làm hồ sơ) cộng ba sửa: hai của CC-219 và một của CC-219r2:** W1 (B1, sổ mức ảnh: tập đã dùng mà C lấy làm dev là chủ sở hữu trước; nối G-A với đủ 3.600 id XM3600; nguồn NoCaps test) W2 (B2, niêm phong G-B) và NB-W25 của CC-219r2 (n_e trước/sau W25, phương án (ii)). Hội đồng CC-219r3 GO 92 (02/11). Mọi dòng khác giữ như v4. Khi mâu thuẫn, v4.1 thắng v4. Các dòng sửa được đánh dấu **[CC-219 W1]** hoặc **[CC-219 W2]**.

Đây là ý kiến AI, chưa có chuyên gia thẩm định. Chưa commit. Không file nào được gửi đi. Lượt viết v4 không đọc dữ liệu nào ngoài danh sách id và các file đếm đã commit (§0).

**Mục đích.** CC-214r3 (vòng 3, median 92, cả ba judge 92) ra ESCALATE_TO_PI vì một mốc khách quan trượt: `vietnamese_caption_test_available`. PI chọn ở PI-1101u (LOG 2026-11-01T14:48:45Z): "Duyệt, chấm tiếng Việt bằng nhãn người". Bài C nhận PVR ("Verify Before You Borrow"). Caption tiếng Việt trên ảnh NoCaps test được chấm object precision so với nhãn người có sẵn của Open Images, qua một bộ khớp VN→lớp tất định, cộng proxy chữ trong cảnh tiếng Việt (OpenViVQA). NoCaps tiếng Anh (EvalAI) chỉ là benchmark. Nơi nộp TALLIP. Thêm ViTextCaps nếu bộ này được phát hành.

v4 = v3 cộng ba việc:
1. viết rõ thiết kế chính đã được chọn (§1, §3, §4, §8, §9.3);
2. cố định tên nhánh theo CC-214r3 N-n, với mọi tên bài giữ "Vietnamese" (§10);
3. ghi cách xử lý từng mục không chặn của CC-214r3 (§13).

**Thứ tự ưu tiên.** Khi có mâu thuẫn, **v4 thắng v3**. v3 (`C_DIRECTION_v3_2026-11-01.md`, sha 99dbe46b) giữ nguyên làm hồ sơ.

**Các dòng PI ràng buộc:**
- **PI-1101u:** thiết kế ở trên.
- **PI-1101t:** claim chính của mọi bài là tiếng Việt; tiếng Anh chỉ làm benchmark. Vì vậy nhánh N-D chỉ-tiếng-Anh của v3 bị rút.
- **PI-1101s:** dữ liệu đã phát hành công khai thì dùng không cần thư; không dùng dữ liệu chưa phát hành.
- **PI-1101o/p:** bài báo không nhắc chuyện trùng lặp.

**Phán quyết vòng 3:** `.session_backup/2026-10-13/decisions/CC-214r3.txt` (sha f3bb8065).

**Hướng không đổi.** PVR (Proposition-Verified Retrieval) là truy hồi có kiểm chứng ở mức mệnh đề, không cần huấn luyện.

**Thay đổi chính so với v3 (một dòng mỗi mục):**
- **Outcome chính.** Bây giờ là P_obj của **caption tiếng Việt** trên NoCaps test, chấm bằng nhãn người kiểm của Open Images V7 (có cả nhãn khẳng định có mặt lẫn khẳng định vắng mặt), qua bộ khớp của A đã commit (§0, §3.1). Tiếng Anh trên cùng ảnh chỉ là benchmark (CIDEr EvalAI, ≤ 5 nhánh có tên; §8).
- **Ghim bộ khớp.** Đổi từ evaluator trong `.session_backup` sang 4 file đã commit của đường OIV7 của A (commit, path, sha ở §0). Từ vựng đã ánh xạ là 69 lớp của `vi_oiv7_map.json`, cố định ngay bây giờ (W3).
- **SESOI, headroom và chọn biến thể UNCERTAIN.** Chuyển từ KT-C sang **XM3600-vi** (tiếng Việt, nhãn Open Images). KT-C chỉ còn làm dev cho nhánh benchmark tiếng Anh (§3.3, §4, §5.3).
- **Cổng độ phủ.** Bỏ ngưỡng 90% ở cấp ảnh của v3 với tư cách là cổng. Thay bằng phép đếm một lần cộng cổng power. Lý do: cùng bộ khớp chỉ phủ 58,9% ảnh XM3600 (§3.2). **Đây là thay đổi thiết kế, cần judge đọc** (§14 Q2).
- **Cổng mô hình sạch tiếng Việt.** Phải có mô hình nói được tiếng Việt và SẠCH trên ảnh NoCaps test, làm captioner và bộ kiểm chứng. Đây là cổng trước khi thuê máy. Không có thì áp dòng Dừng (§5.2, §10.1).
- **Tên nhánh.** N-C và N-D giữ tên của v3 nhưng cả hai có claim tiếng Việt. Mọi nhánh dùng tên bài của đề cương v16 (§10).
- **T_B bị gạch.** Các mục CC-214r3 W1–W21 được xử lý ở §13.

## 0. Đầu vào và hash

| File | sha256 đầu | Ghi chú |
|---|---|---|
| `manuscript/directions/C_DIRECTION_v3_2026-11-01.md` | 99dbe46b | Không đổi; hồ sơ |
| `.session_backup/2026-10-13/decisions/CC-214r3.txt` | f3bb8065 | Phán quyết vòng 3; W1–W21 |
| `manuscript/PLAN_2026-11-01.md` | 06e5df23 | Không sửa ở lượt này; xem §0.1 |
| `manuscript/ncs_proposal/DeCuong_NCS_LHU_2026-10_v16_final.md` | cec765aa | l.321 [CT4]: tên bài chính, TALLIP 03/2027; ISJ, PRIA dự phòng |
| `manuscript/directions/B_DIRECTION_v3_2026-11-01.md` | ef1e3cc5 | Ranh giới (§2(e)) và mẫu luật W25 |
| `manuscript/prereg/2026-10-28_w25_neardup/RULE.md` | 289c0a59 | W25 §3 (C1 ∨ C2 ∨ C3) |
| `manuscript/prereg/2026-10-28_w25_neardup/oiv7_val_ids.txt` | 4b7a1813 | 41.620 id OIV7 val (cổng G-A) |
| `manuscript/prereg/2026-10-28_w25_neardup/xm3600_in_oiv7_val_ids.txt` | 54966ca7 | 456 id XM3600 trong OIV7 val, giữ cho C (RULE l.21) |
| `.claude/skills/venue-tallip/SKILL.md` | ff4fdfb2 | Luật tên 6–12 từ, nguồn ở §10 (W19) |
| `.session_backup/2026-11-01/c_direction_v3_idcheck/idcheck.py` / `idcheck_out.txt` | 040e78ef / 13d59e15 | Kiểm id của v3; commit cùng prereg tầng 1 (W8) |

**Bộ khớp VN→lớp Open Images của A** (ghim bằng commit, path và sha; tất cả đã được git theo dõi, không có thay đổi chưa commit ở HEAD 219704f):

| Thành phần | Path | Commit cuối | sha256 đầu | Vai trò |
|---|---|---|---|---|
| Bộ trích mention | `rescap/chair.py` (`objects_in`, `raw_tone=False`) | a0accb5 (14/10) | e47d249a | Caption → tập lớp của từ điển; chuẩn hoá dấu thanh (matcher v2) |
| Từ điển | `rescap/vi/lexicon.py` | 996c32f (11/10) | fbc945f2 | Danh sách lớp và loại từ |
| Bảng ánh xạ | `data/xm3600/vi_oiv7_map.json` | e564ed6 (12/10) | 27f2b1ca | Lớp từ điển → lớp OI `pos` / `neg` (69 lớp đã ánh xạ; `_skipped` ghi lý do bỏ các lớp khác) |
| Luật trạng thái | `scripts/xm3600_oiv7.py` (`status`, `statuses`) | e564ed6 (12/10) | 9a79403f | Có mặt / vắng mặt / không rõ; nhãn hai chiều mâu thuẫn tính là không rõ |
| Số đếm tham chiếu | `data/xm3600/manifest.json` (khoá `coverage`) | e564ed6 (12/10) | 263015f9 | Độ phủ của cùng bảng ánh xạ trên XM3600 (§3.2) |

- **Cả 4 file đều có trước các con số OIV7 của A** (A8.4, 18/10; `number_manifest.tsv` l.542–543, l.918). Vì vậy HEAD chính là phiên bản A đã dùng.
- Pin cũ của v3 (`.session_backup/2026-10-14/r12_verify/evaluate_xm3600_predictions_v3.py`, 24356632) là evaluator chấm theo tham chiếu và COCO-80. File đó gọi lại `xm3600_oiv7` và `objects_in`. v4 ghim trực tiếp các thành phần, còn pin cũ chỉ là nguồn gốc các con số của A.
- **Không dùng độ đo của B.** Ranh giới với B giữ nguyên (§2(e)).

### 0.1 Các dòng PLAN bị v4 thay thế (không sửa PLAN; v4 thắng)

- **l.53**, tên tạm "…for Vietnamese Image and Scene-Text Captioning": thay bằng tên bài chính ở §10.
- **l.58**, "Kiểm chứng từng mệnh đề với ảnh truy vấn bằng VSPS": thay bằng §2(c)(d) và §5. C không dùng VSPS hay VSPS-J. (v3 trích nhầm l.59; dòng đúng là **l.58**, W11.)
- **l.64**, "độ đo ảo giác có kiểm soát số đối tượng của bài A": thay bằng §3.1, tức P_obj thô theo nhãn người, không dùng bản count-matched (abstract_A l.9).
- **l.72**, "ViTextCaps test, VieCap4H private test, NoCaps test": thay bằng §3.2 và §10.
- **l.83**, "Bộ kiểm chứng này chính là thành phần lõi của bài C mới": thay bằng §2(c)(d) và §5.
- **l.75**, "03–05/2027 … TALLIP": giữ nguyên. Đề cương v16 ghi 03/2027 (§11.3).

## 1. Hướng và claim

**Phương pháp** (như v3):
1. Truy hồi caption người viết của các ảnh gần nhất trong datastore (§9.2).
2. Tách mỗi caption thành mệnh đề (vật thể, thuộc tính, quan hệ, số lượng, chuỗi chữ).
3. Kiểm từng mệnh đề với **ảnh truy vấn** bằng một bộ kiểm chứng cố định (§5).
4. Bỏ mệnh đề REJECTED, lắp lại demonstration theo luật tất định (§5.4).
5. Đưa demonstration đã lắp lại vào MLLM mở làm ví dụ ICL.

Không huấn luyện. Chạy trên một GPU 24 GB.

**Claim chính, bằng tiếng Việt (PI-1101t, PI-1101u):**
> Trên ảnh NoCaps test, caption tiếng Việt sinh với demonstration đã qua PVR có object precision cao hơn so với hiệu chỉnh hậu kiểm cùng bộ kiểm chứng (A8). Object precision được đo bằng nhãn người kiểm có sẵn của Open Images, và object recall không giảm quá biên.

**Phạm vi chữ của claim.** Claim nói về "object precision against human-verified labels", không phải chất lượng caption tiếng Việt nói chung.
- Ngoài nhánh N-A, bài **không** claim CIDEr hay chất lượng tiếng Việt dựa trên tham chiếu trên dữ liệu giữ riêng.
- Proxy chữ (§7) là claim phụ, có luật riêng.
- Tiếng Anh chỉ là benchmark: CIDEr NoCaps qua EvalAI, và P_obj tiếng Anh báo để so sánh.

**Claim tính mới được phép** (giữ từ v3): tính mới về **vị trí cộng độ mịn**. Bài kiểm chứng *đầu vào truy hồi* ở *mức mệnh đề* (có cả mệnh đề chữ) *trước* khi dùng làm ICL.

**Claim bị cấm:**
- "lần đầu kiểm chứng nội dung truy hồi với ảnh";
- "bộ kiểm chứng mới";
- "Vietnamese captioning" theo nghĩa chất lượng dựa trên tham chiếu, ngoài N-A;
- bất kỳ câu nào đặt kết quả tiếng Anh làm kết quả chính.

**Phép thử sống còn của tính mới:** PVR so với A8 (hiệu chỉnh hậu kiểm cùng bộ kiểm chứng) trên P_obj tiếng Việt (§4).

## 2. Ranh giới với VSPS-J, FAIR, Bài B và Bài A

Giữ nguyên v3 §2(a)–(e). Riêng (f) được thay:

(f) **Với Bài A.**
- C không claim lại các kết quả gold-completeness, độ dốc verbosity hay mention không kiểm được của A.
- C chỉ **dùng lại** bộ khớp VN→lớp Open Images của A (4 file ở §0, có trích dẫn), nguyên trạng.
- Không sửa, mở rộng hay chỉnh từ vựng (W3).
- Bảng xếp hạng count-matched của A không được dùng ở đâu cả.

## 3. Outcome chính và gold

### 3.1 Định nghĩa (tiếng Việt là chính)

**Ánh xạ mention (tiếng Việt).**
- Mỗi caption tiếng Việt đi qua `objects_in(caption, raw_tone=False)` và cho ra một tập lớp của từ điển.
- Chỉ giữ các lớp có trong 69 khoá của `vi_oiv7_map.json` (27f2b1ca). Đây là **từ vựng đã ánh xạ**, cố định ngay bây giờ.
- Theo cách đếm của `xm3600_oiv7.py score`, mỗi lớp được tính **một lần cho mỗi caption**.

**Trạng thái của cặp (ảnh i, lớp c),** theo `status()`:
- **có mặt:** có một lớp `pos` của c được người kiểm khẳng định có mặt (Confidence 1);
- **vắng mặt:** nếu không có mặt, và có một lớp `neg` của c được người kiểm khẳng định vắng mặt (Confidence 0);
- **không rõ:** mọi trường hợp còn lại, kể cả khi nhãn mâu thuẫn hai chiều.

Mention "sai" chỉ có được khi có **nhãn vắng mặt đã kiểm** (W4).

**Gold.** File `oidv7-{val,test}-annotations-human-imagelabels.csv` (giấy phép CC BY 4.0):
- md5 so với bucket, lọc theo id của C ngay khi đọc dòng, như `xm3600_oiv7.py build`;
- không nhãn mới, không AI-silver, không nhãn nào do mô hình sinh.

**Độ đo:**
- **Outcome chính P_obj^VI** = có mặt / (có mặt + vắng mặt). Gộp ở cấp mention, CI bootstrap theo ảnh.
  - CHAIR_i^VI = 1 − P_obj^VI.
  - CHAIR_s^VI (tỉ lệ caption có ít nhất một mention vắng mặt) là độ đo phụ.
- **Luật cho mention không rõ.** Luật chính: loại khỏi mẫu số. Phân tích độ nhạy đã đăng ký: tính là sai.
  - Claim tiêu đề cần cùng dấu dưới cả hai luật.
  - Nếu khác dấu, claim bị ghi là "phụ thuộc luật" và báo cả hai con số.
- **Báo kèm bắt buộc (W4, N5 của CC-214r2):**
  - với mỗi tập, số cặp (ảnh, lớp) có mặt đã kiểm và vắng mặt đã kiểm trên từ vựng đã ánh xạ;
  - với mỗi nhánh và mỗi tập, tỉ lệ mention kiểm được = (có mặt + vắng mặt) / tổng mention đã ánh xạ, đặt cạnh P_obj^VI.
- **Guard "nói ít đi":** R_obj^VI = số cặp có mặt đã kiểm mà caption nhắc tới / số cặp có mặt đã kiểm (verified-positive recall của `xm3600_oiv7`). Số mention mỗi caption chỉ báo để mô tả.
- **Guard chất lượng tiếng Việt.** NoCaps test không có tham chiếu tiếng Việt, nên **không có CIDEr tiếng Việt ở tầng 3**.
  - Guard CIDEr-VI theo kiểu NI chạy ở dev (XM3600-vi, KTVIC test, OpenViIC test) và ở tầng 2 (KTVIC test, OpenViIC test, cấu hình đã ghim cho tầng 2; §4).
  - Ở tầng 3, guard chất lượng tiếng Việt chỉ còn R_obj^VI.
  - Đây là giới hạn của thiết kế và được ghi rõ trong bài.
- **Benchmark tiếng Anh, cùng ảnh.**
  - Caption tiếng Anh của các nhánh S1–S5 (§8) được chấm CIDEr bằng EvalAI.
  - P_obj^EN (bảng ánh xạ tiếng Anh ghim trong prereg tầng 1, cùng nhãn OI) báo để so sánh, không phải claim.
  - Không phần tiếng Anh nào là cổng của claim tiếng Việt.

| Guard | Đơn vị | Biên | Ở đâu |
|---|---|---|---|
| δ_C (CIDEr-VI) | điểm CIDEr ×100 | 2,0 (ghi rõ là **lenient**, lý do như v3 §3.1) | Tầng 1 và 2: XM3600-vi, KTVIC test, OpenViIC test |
| δ_R (R_obj^VI) | điểm % | 2,0 | Mọi tầng |
| δ_C (CIDEr-EN, benchmark) | điểm CIDEr ×100 | 2,0 | Tầng 3, EvalAI, chỉ ước lượng điểm, không phải cổng (§8) |
| SESOI_T, δ_RT (proxy chữ) | điểm % P_text / R_text | đề xuất 2,0 / 2,0; prereg tầng 1 chốt (§7) | Proxy |

### 3.2 Tập test, độ phủ và cổng power

**Cổng độ phủ của v4 (thay v3 §3.2; cố định trước phép đếm duy nhất).**

**Vì sao đổi.** Cùng bảng ánh xạ 69 lớp chỉ phủ 2.119 / 3.600 = **58,9%** ảnh XM3600: số ảnh có ít nhất một nhãn đã kiểm trên một lớp đã ánh xạ (`data/xm3600/manifest.json`, khoá `coverage`, sha 263015f9). Ảnh XM3600 cũng là ảnh Open Images. Vì vậy ngưỡng 90% ở cấp ảnh của v3 gần như chắc chắn trượt trên NoCaps test, và với nó cả đường chính của C. Đây là dự báo từ một tập tương tự, chưa phải số đo trên NoCaps.

**Luật mới:**
1. **Không thu nhỏ tập.** P_obj^VI được tính trên **toàn bộ** NoCaps test còn lại sau §9.3. Ảnh không có nhãn đã kiểm trên lớp đã ánh xạ không đóng góp mention kiểm được nào. Vì vậy không cần chọn tập con ảnh, và luật split đầy đủ được giữ.
2. **Phép đếm duy nhất (cổng G-B, §9.3)** báo:
   - n_e = số ảnh có ít nhất một nhãn đã kiểm trên lớp đã ánh xạ;
   - số cặp có mặt đã kiểm và vắng mặt đã kiểm;
   - tỉ lệ phủ (con số tương ứng với ngưỡng 90% của v3, chỉ báo, không phải cổng).
3. **Cổng power.** Claim giữ riêng cần tập dượt tầng 2 cho P(PASS) ≥ 0,98, ước lượng bằng bootstrap theo ảnh ở cỡ n_e (§4). Không đạt thì không có tầng 3 cho P_obj^VI, và C dừng (§10).
4. Từ vựng không được mở rộng sau phép đếm (W3). Phép đếm chỉ chạy **một lần**.
5. **G-B không chạy cho tới khi Q2 được phán** (bởi lượt đọc v4 hoặc bởi PI). Luật nào đọc kết quả của G-B (90% của v3 hay luật của v4) phải được chốt trước phép đếm.

**Phương án còn lại cho người đọc:** giữ ngưỡng 90% của v3. Theo phép so sánh với XM3600, nhiều khả năng khi đó áp dòng Dừng ngay sau G-B. Quyết ở §14 Q2.

| Tập (vai trò) | Nguồn ảnh | P_obj^VI / R_obj^VI | CIDEr | Proxy chữ |
|---|---|---|---|---|
| **NoCaps test** (test chính, 10.600 ảnh; một lần xem) | Chỉ Open Images test (arXiv 1812.08658: test lấy từ OI test; G-A xác nhận bằng nối id) **[CC-219 W1]** | **Chính.** Chấm cục bộ trên caption tiếng Việt của mọi nhánh còn lại. Ảnh của chủ sở hữu đăng ký trước bị loại, kể cả các tập đã dùng mà C lấy làm dev (XM3600 đủ 3.600 ảnh, NoCaps val, KT-C/Karpathy test, KTVIC test, OpenViIC test), chỉ báo bằng con số (§9.3) **[CC-219 W1]** | Chỉ tiếng Anh: EvalAI, toàn tập, S1–S5 (§8). Tiếng Việt: không có tham chiếu | Không |
| ~~TextCaps val~~ | — | Bị gạch khỏi C (CC-214r2 B4). Chỉ chuyển giao khi có dòng PI cộng một phán quyết sổ không đảo ngược ≥ 92 | — | — |
| **OpenViVQA dev** (proxy VI, 1.070 ảnh / 3.545 QA) | Ảnh cảnh Việt Nam | Không | Không | **Có** (§7), chỉ khi có mô hình SẠCH (§9.1) |
| **ViTextCaps test** (nếu được phát hành công khai trước khi khoá prereg tầng 3; §10) | — | Không | CIDEr-VI giữ riêng (khoảng 4,76 tham chiếu/ảnh), claim phụ | Không có đáp án QA |
| **VieCap4H private test** (chỉ khi tham chiếu được công bố công khai; PI-1101s) | Ảnh tin tức | Không | Phụ, ghi rõ "nhiễu" (khoảng 1,05 tham chiếu/ảnh) | Không |
| **Dev tầng 1:** **XM3600-vi** (dev P_obj^VI: SESOI, headroom, UNCERTAIN); KT-C 3.907 (chỉ nhánh tiếng Anh); lát TextCaps train T_A; ViTextVQA dev; KTVIC test 558 và OpenViIC test (CIDEr-VI) | Đã dùng (spent), chỉ làm dev (PORTFOLIO l.188). COCO Karpathy val **không** có mặt ở bất kỳ vai trò nào | XM3600-vi (OI); KT-C (COCO, chỉ EN) | Có | ViTextVQA dev |
| **Tập dượt tầng 2:** NoCaps val (cổng P_obj^VI, chờ Q11); lát OpenViVQA train O_B (proxy; không dùng nếu có mô hình Vintern, v3 §5.2) | Spent hoặc split train | NoCaps val (OI) | KTVIC test, OpenViIC test (guard CIDEr-VI) | O_B |

- T_B (lát TextCaps train dượt tầng 2) **bị gạch** (W6): sau B4 không còn test chữ tiếng Anh nào.
- **UIT-ViIC:** C không dùng split nào (giữ v3 §3.2, N11).
- **Thứ tự tập test cho P_obj^VI ở tầng 3:** chỉ NoCaps test. Nếu cổng G-B hoặc cổng power trượt, không có test giữ riêng nào cho P_obj^VI. Khi đó C dừng trước tầng 3 và quyết lại theo luật đổi hướng (PLAN §7).

### 3.3 Các tập dev

**XM3600-vi** (dev chính cho tiếng Việt):
- 3.600 ảnh Open Images, mỗi ảnh có 2 hoặc 3 caption tiếng Việt người viết. Đã dùng (A; PORTFOLIO l.188).
- 456 id nằm trong OIV7 val được giữ cho C (RULE W25 l.21, `xm3600_in_oiv7_val_ids.txt` 54966ca7), nên C dùng được.
- **Loại trước decode (§9.3) [CC-219 W1]:** XM3600 (đủ 3.600 ảnh) là tập đã dùng của chủ sở hữu trước (A), và bảng ánh xạ được dựng trên nó, nên XM3600 **không** nhường. Ảnh NoCaps test trùng với bất kỳ ảnh XM3600 nào (nối id OI trên đủ 3.600 id: OI test 1.399, val 456, train 1.745 theo `data/xm3600/manifest.json`; cộng W25) **rời khỏi P_obj^VI, R_obj^VI và proxy cục bộ của C**, chỉ báo bằng con số. CIDEr-EN EvalAI giữ toàn tập. Theo tỉ lệ ngẫu nhiên, khoảng 1.399 × 10.600 / 125.436 ≈ 118 ảnh trùng. Phía dev XM3600 giữ nguyên; ảnh XM3600 trùng với chủ sở hữu khác vẫn bị bỏ khỏi dev như v4. Số còn lại được ghim trong prereg tầng 1.
- **Ghi rõ:** bảng ánh xạ `vi_oiv7_map.json` được dựng trên XM3600. Vì vậy P_obj^VI ở dev trên XM3600 có thể lạc quan. Bài toán ở đây là chênh lệch ghép cặp giữa các nhánh, không phải mức tuyệt đối. SESOI_P có sàn 1,0 điểm % (§11.1). Điều này được báo trong bài.

**KT-C** (giữ số liệu của v3 §3.3: 5.000 − 1.093 = 3.907):
- Vai trò bây giờ chỉ là dev cho **nhánh benchmark tiếng Anh**: định dạng, tốc độ, P_obj^EN mô tả.
- KT-C không còn quyết SESOI, headroom hay biến thể UNCERTAIN.
- **Công bố (W12):** việc loại 593 id A-T3 val2017 ("chưa đặt giữ") và 328 id M0 đã dùng (419 − 91 id `karpathy_test_val_ids`) khỏi KT-C là **loại dư có chủ đích, cố định trước, chỉ ở dev**. Nó không đổi tập test nào.

## 4. Các nhánh, đối chứng chính, Holm và luật quyết định

Các nhánh A0–A12 và PVR giữ nguyên định nghĩa của v3 §4. **Chọn và ghim trước output tầng 1 đầu tiên:** k = 4 (đề xuất), captioner, prompt và giải mã greedy.

**Theo ngôn ngữ:**
- Mọi nhánh chạy bằng **tiếng Việt** trên các tập tiếng Việt và trên NoCaps test (datastore D-VI; §9.2).
- Nhánh benchmark tiếng Anh chỉ gồm 5 nhánh S1–S5 (§8), chạy trên NoCaps test và KT-C (datastore D-EN).

**Đối chứng chính (một và chỉ một):** PVR − A8 trên P_obj^VI (luật chính ở §3.1), ghép cặp theo ảnh.

**Holm** áp lên họ phụ PVR so với A0–A7 và A9–A11, trên P_obj^VI.
- A12 không thuộc họ (oracle, chỉ dev).
- Nhánh bị cắt theo §11.1 ra khỏi họ, và việc cắt được báo.

**Đạt ở dev-confirm (tầng 2; cổng P_obj^VI là NoCaps val, chờ Q11)** khi cả ba điều sau cùng đúng:
1. ΔP_obj^VI(PVR − A8): cận dưới CI 95% bootstrap theo ảnh > 0 **và** ước lượng điểm ≥ SESOI_P;
2. ΔR_obj^VI(PVR − A1): cận dưới > −δ_R;
3. ΔCIDEr-VI(PVR − A8) và ΔCIDEr-VI(PVR − A1) trên KTVIC test và OpenViIC test: cận dưới > −δ_C.

Tập dượt cần P(PASS) ≥ 0,98 cho điều 1 và 2, ước lượng bằng bootstrap **ở cỡ n_e của NoCaps test** (§3.2).
- Chỉ power hay P(PASS) được chiếu sang n_e của test.
- **SESOI không bao giờ được chiếu hay co giãn theo n** (W5).

**Luật quyết định ở tầng 3 (một lần xem, viết ngay bây giờ).** Claim chính ĐẠT khi và chỉ khi trên NoCaps test (sau §9.3):
1. ΔP_obj^VI(PVR − A8): cận dưới CI 95% bootstrap theo ảnh > 0 **và** ước lượng điểm ≥ SESOI_P;
2. ΔR_obj^VI(PVR − A1): cận dưới > −δ_R;
3. dấu của (1) giữ nguyên khi mention không rõ được tính là sai. Nếu không, claim bị ghi là "phụ thuộc luật".

Báo cạnh kết quả: tỉ lệ mention kiểm được của từng nhánh, n_e, và số cặp có mặt / vắng mặt đã kiểm.

**Không phải cổng:**
- CIDEr-EN EvalAI (benchmark, ước lượng điểm theo NI; báo dù đạt hay trượt; §8);
- P_obj^EN;
- họ Holm (phụ);
- proxy chữ (claim phụ có luật riêng ở §7).

Một test ĐÃ ĐĂNG KÝ mà TRƯỢT vẫn được báo ngắn, không bao giờ giấu.

**Luật dừng.** Giữ v3 §4: PVR không thắng A8 theo SESOI_P, hoặc chỉ thắng khi trượt guard. Hệ quả: bỏ claim phía đầu vào, không đăng ký tầng 3, áp luật đổi hướng, và bản thảo CC-212 là phương án dự phòng.

**Các điều kiện bác bỏ khác:**
- **Chữ (W1).** A11 bằng PVR trong phạm vi **SESOI_T** (đơn vị P_text, không phải SESOI_P) trên proxy: phần OCR bị coi là tầm thường và bỏ khỏi claim.
- **Headroom.** Oracle A12 − A1 < 2 điểm % P_obj^VI trên **XM3600-vi** ở tầng 1, tính sau luật tự truy hồi (§9.2): dừng trước tầng 2.

## 5. Bộ kiểm chứng, mô hình theo vai trò và UNCERTAIN

### 5.1 Loại bộ kiểm chứng

Giữ v3 §5.1. Dùng lược đồ 3 nhãn của FAIR (SUPPORTED/UNCERTAIN/REJECTED; `rescap/metrics_svp.py:51`): prompt sinh nhãn, phân tích nhãn đầu ra, giải mã greedy. Không có ngưỡng vô hướng nào để chỉnh. Không dùng S_hi hay ngưỡng theo loại mệnh đề của VSPS-J.

### 5.2 Mô hình theo vai trò và ngôn ngữ (cổng mô hình sạch tiếng Việt)

Với claim tiếng Việt, **captioner tiếng Việt và bộ kiểm chứng mệnh đề tiếng Việt** đều phải qua B10 (§9.1) trên ảnh NoCaps test, tức ảnh Open Images val và test.

| Vai trò | Ứng viên đã biết | B10 trên NoCaps test (chưa chạy) |
|---|---|---|
| Captioner VI, bộ kiểm chứng VI | Vintern-1B-v3_5 (cấu hình FAIR) | Thẻ không liệt kê dữ liệu → **KHÔNG KIỂM ĐƯỢC**, tính là nhiễm (v3 §5.2) |
| | Vintern-1B-v2 | "in part" cộng tập gated → KHÔNG KIỂM ĐƯỢC nếu không có quyền truy cập (v3 §5.2) |
| | Qwen2.5-VL-7B-Instruct, InternVL3-8B (đã có trên M8), Aya-Vision-8B (gated) | **Chưa kiểm.** Tầng 1 đọc thẻ và báo cáo kỹ thuật, nối id những phần SFT công khai. Phần SFT không công bố → KHÔNG KIỂM ĐƯỢC theo luật fail-closed |
| | Ứng viên khác có dữ liệu SFT công khai và nói được tiếng Việt | Liệt kê ở tầng 1, trước khi thuê máy |
| Captioner EN, bộ kiểm chứng EN (benchmark) | LLaVA-1.5-7B | Có thể SẠCH sau phép nối id, theo cách hiểu PI-1 (v3 §5.2; §14 Q5). Tiếng Việt yếu, nên không phải ứng viên VI |
| Bộ tách mệnh đề VI / EN | Bộ tất định dựa trên luật (VI: bộ tách từ ghim trong prereg; EN: cây phụ thuộc) | Không thấy ảnh, nên không có nhiễm ảnh theo cách dựng |
| Bộ mã hoá truy hồi | Bộ mã hoá của `cen_memory_emb` (C-EN) | Pretrain web-scale ghi là "chưa biết" (PI-1) |

**Lưu ý khi nối id.** Localized Narratives phủ ảnh Open Images train, val và test, và hay có mặt trong các hỗn hợp SFT phổ biến. Bất kỳ tập SFT nào dựng trên ảnh Open Images đều phải được nối theo id OI với NoCaps test. Có ảnh trùng thì là TRÚNG.

**Cổng G-C (trước khi thuê máy cho C).**
- Phải có ít nhất một mô hình nói được tiếng Việt và SẠCH trên NoCaps test cho vai trò captioner VI. Phải có ít nhất một mô hình như vậy cho vai trò bộ kiểm chứng VI. Hai vai trò có thể dùng cùng một mô hình.
- Cách hiểu "kiểm được" lấy theo câu trả lời Q5 của PI.
- Không có mô hình như vậy thì áp §10.1 dòng 2 (Dừng).
- Lượt này **không dự đoán** kết quả của cổng này.

**Luật chọn** (giữ v3): bộ kiểm chứng là mô hình đầu tiên qua B10 cho mọi tập test đã đăng ký. Mô hình chạy với đúng prompt 3 nhãn của FAIR, được chọn và ghim trước output tầng 1 đầu tiên, và không thay sau khi thấy kết quả dev.

### 5.3 Luật UNCERTAIN

Giữ v3 §5.3 (PVR-drop và PVR-keep ở tầng 1; lỗi phân tích nhãn tính là UNCERTAIN; tỉ lệ UNCERTAIN luôn được báo). Thay đổi duy nhất là **tập dùng để chọn**: XM3600-vi thay cho KT-C.
- **Thứ tự:** (i) luật tự truy hồi; (ii) SESOI_P từ A12 và A1 trên XM3600-vi; (iii) chọn biến thể.
- **Luật chọn:** chọn nhánh có P_obj^VI dev cao hơn, với điều kiện qua δ_C (CIDEr-VI) và δ_R so với A1. Nếu |ΔP_obj^VI| < SESOI_P/2 thì chọn PVR-drop.

### 5.4 Demonstration bị rỗng và lắp lại tất định

Giữ nguyên v3 §5.4, áp riêng cho từng ngôn ngữ. Bộ tách và luật lắp lại cho tiếng Việt được ghim trong prereg tầng 1.

## 6. Vệ sinh gold

Giữ nguyên v3 §6:
- TextCaps-vi là AI-silver (dịch máy) và không bao giờ được chấm.
- ViOCRVQA là gold lấy từ metadata nhà sách, không phải tập test dự phòng.

Nhãn Open Images dùng ở đây là nhãn người kiểm có sẵn (Confidence 0/1 trong các file human-imagelabels). Không nhãn nào do mô hình sinh.

## 7. Đặc tả proxy chữ trong cảnh

Giữ nguyên v3 §7 mục 1–6 (chọn câu hỏi bằng regex trên văn bản câu hỏi, bộ trích, bộ chuẩn hoá, khớp/lệch/không được phủ, w = 1 và w = 0, guard R_text). Thêm mục 7.

7. **Luật quyết định của proxy (W1).** Phải chốt trong prereg tầng 1, **trước output tầng 1 đầu tiên**, và không chỉnh sau. Đề xuất để prereg chốt:
   - **Đối chứng chính:** PVR − A8 trên P_text (w = 1), ghép cặp theo ảnh. Kiểm thêm tính tầm thường: PVR − A11 trên P_text.
   - **SESOI_T** = 2,0 điểm % P_text, cố định. Không suy ra từ dữ liệu, vì phía chữ không có oracle tương tự A12. Không co giãn theo n.
   - **Biên guard δ_RT** = 2,0 điểm % R_text. ΔR_text(PVR − A1) cần cận dưới > −δ_RT.
   - Claim proxy cần cùng dấu dưới w = 1 và w = 0.

## 8. NoCaps test: một lần xem, benchmark tiếng Anh qua EvalAI

**Cùng một lần xem đã đăng ký.** Caption tiếng Việt của mọi nhánh còn lại và caption tiếng Anh của S1–S5 được sinh trên NoCaps test và chấm trong **cùng một lần xem**:
- P_obj^VI và R_obj^VI chấm cục bộ trên laptop, theo nhãn OI;
- CIDEr-EN do EvalAI chấm.

**Năm nhánh có tên, mỗi nhánh nộp một lần** (bản tiếng Anh của cùng phương pháp): S1 PVR (biến thể UNCERTAIN đã chọn), S2 A8, S3 A1, S4 A0, S5 A6.
- Không nộp lại.
- Lượt nộp hỏng định dạng được báo là "thiếu", không thay bằng nhánh khác. Trình kiểm định dạng chạy trước trên NoCaps val.

**Luật CIDEr-EN** (benchmark, không phải cổng): chỉ ước lượng điểm. CIDEr(S1) − CIDEr(S2) ≥ −δ_C và CIDEr(S1) − CIDEr(S3) ≥ −δ_C. Kết quả được báo dù đạt hay trượt. Không có CI.

**Trần nộp của EvalAI (W13).** Con số "5 lượt nộp suốt đời tài khoản" phải được **xác minh trên trang thi NoCaps của EvalAI trong prereg tầng 3**, kèm ngày đọc.
- Nếu trần thật lớn hơn 5: vẫn chỉ 5 nhánh.
- Nếu nhỏ hơn: cắt theo thứ tự S5 → S4.

**Luật không loại ảnh:** giữ v3 §8. CIDEr-EN được tính trên toàn tập. P_obj^VI và R_obj^VI tính trên N trong 10.600 ảnh, sau một lần loại cố định trước, chỉ báo bằng con số. Không bao giờ viết "no overlap" (PI-1101o/p).

**Tài khoản:** một địa chỉ nhóm nhận thư được, không phải của PI, không phải `vsps-research@example.org` (§14 Q6). Chưa có tài khoản thì không xem NoCaps test.

**Giữ ảnh test (CC-209 r1(a), CC-215r2).**
- Ảnh NoCaps test và OpenViVQA dev chỉ nằm trên máy test của C, máy này được ghi tên trong prereg tầng 3.
- Đặc trưng W25 của các ảnh đó tính trong tmpfs cách ly (W25 §5).
- Ảnh test không bao giờ được chép sang máy đang chạy job của bài khác.

## 9. Nhiễm dữ liệu, datastore, luật mức ảnh và các cổng tầng 1

Mọi việc ở mục này chỉ là kiểm tra nội bộ, fail-closed. Bài báo không bao giờ nhắc tới (PI-1101o/p). Phần loại chỉ báo bằng con số.

### 9.1 Nhiễm qua dữ liệu huấn luyện mô hình (B10)

Giữ cách kiểm và ba trạng thái SẠCH / TRÚNG / KHÔNG KIỂM ĐƯỢC của v3 §9.1. Phạm vi bây giờ:
- **mọi mô hình của C theo vai trò và ngôn ngữ (§5.2)** × NoCaps test, OpenViVQA dev, và ViTextCaps test hay VieCap4H test nếu được phát hành;
- ViTextVQA (mọi split) là nguồn tham chiếu chéo;
- với NoCaps test, phép nối dùng id ảnh Open Images (§5.2, lưu ý về Localized Narratives).

Kết quả của G-C (§5.2) được ghi vào prereg tầng 1.

### 9.2 Datastore và luật tự truy hồi

Giữ v3 §9.2:
- D-EN = 80.083;
- D-TC chỉ phục vụ T_A, vì T_B đã bị gạch;
- D-VI = caption train của KTVIC và OpenViIC, trừ H-500 và id của mọi chủ sở hữu khác, không có UIT-ViIC.

Luật tự truy hồi ở mọi tầng giữ nguyên.

**Bản đồ tập truy vấn → datastore (thay bảng của v3):**

| Tập truy vấn (vai trò) | Datastore |
|---|---|
| XM3600-vi (dev tầng 1, VI, P_obj^VI) | D-VI |
| KT-C (dev tầng 1, nhánh benchmark EN) | D-EN |
| T_A (dev tầng 1, chữ EN) | D-TC |
| ViTextVQA dev (dev tầng 1, chữ VI) | D-VI |
| KTVIC test, OpenViIC test (CIDEr-VI dev và guard tầng 2) | D-VI |
| NoCaps val (dượt tầng 2, VI) | D-VI |
| O_B (dượt tầng 2, chữ VI) | D-VI |
| **NoCaps test, nhánh VI (test tầng 3, chính)** | **D-VI** |
| NoCaps test, nhánh benchmark EN S1–S5 | D-EN |
| OpenViVQA dev (proxy VI) | D-VI |
| ViTextCaps test, VieCap4H private test (nếu được phát hành) | D-VI |

**Còn chờ trước decode** (v3 §9.2, đã thêm các cặp mới):
- W25 đầy đủ cho NoCaps test × D-VI và × D-EN;
- XM3600 × D-VI;
- NoCaps val × D-VI;
- mọi tập truy vấn tiếng Việt × D-VI;
- C3 cho KT-C × D-EN.

SESOI, headroom và cổng đi/dừng chỉ được tính sau khi luật tự truy hồi đã áp dụng.

### 9.3 Luật mức ảnh trên toàn sổ và các cổng tầng 1

Giữ v3 §9.3 (danh sách chủ sở hữu, phương pháp W25, luật 1, 2, 4), với các sửa sau.

- **Luật 3, ghi lại thời điểm (W7).** Các tập test của C vào sổ theo **PI-1101u** (LOG l.1112), không theo CC-214r2 (vòng đó là NEXT_ROUND). Ghi chú: dấu thời gian trong LOG không theo thứ tự thời gian. PI-1101u ghi 14:48:45Z, còn CC-214r3, phán quyết mà PI-1101u trả lời, ghi 16:00Z. Thứ tự đúng là theo nội dung: PI-1101u trả lời CC-214r3.
  - Các dòng PORTFOLIO của C chỉ **có hiệu lực qua commit của gatekeeper**, commit đó ghi ngày theo PI-1101u.
  - Kết luận về thứ tự không đổi: C đăng ký sau B và sau mọi chủ sở hữu hiện có. Ảnh trùng bị loại khỏi P_obj^VI, R_obj^VI và proxy cục bộ của C. CIDEr-EN EvalAI giữ toàn tập.
- **Tập đã dùng mà C lấy làm dev là chủ sở hữu trước [CC-219 W1].** XM3600 (đủ 3.600 ảnh), NoCaps val, KT-C/Karpathy test, KTVIC test và OpenViIC test đã được dùng trước khi C đăng ký (PORTFOLIO l.191). Theo PORTFOLIO l.188 (phần trùng bị bỏ khỏi tập đăng ký sau), mọi ảnh NoCaps test trùng với một trong các tập này **rời khỏi P_obj^VI, R_obj^VI và proxy cục bộ của C** và chỉ được báo bằng con số; CIDEr-EN EvalAI giữ toàn tập. Thay dòng v4 "XM3600-vi × NoCaps test, NoCaps val × NoCaps test" thuộc luật 2.
- **Luật 2 (phía dev nhường) chỉ áp cho các split chưa dùng của chính C** (lát TextCaps train T_A, lát OpenViVQA train O_B) **[CC-219 W1]**. Các tập COCO hoặc ảnh Việt Nam (KT-C, KTVIC, OpenViIC) không có id OI; phần gần trùng của chúng với NoCaps test do W25 (luật 1) bắt và được xử lý như trên.
- **n_e và kiểm tra power được tính sau phần loại này [CC-219 W1; sửa theo CC-219r2 NB-W25, phương án (ii)]** (§3.2). G-B chạy một lần, trước mọi máy thuê, nên chỉ loại được phần trùng theo id của G-A; W25 chạy sau, trên máy thuê, trước decode. Vì vậy: (a) **n_e(G-B)** là n_e sau phần loại của G-A; (b) kiểm tra power dùng giá trị bảo thủ **n_e(G-B) − (số ảnh NoCaps test bị W25 gắn cờ)**; số này đếm chỉ từ pixel, không đọc nhãn nào; (c) chênh lệch chính xác do W25 được tính **một lần**, từ file trung gian đã niêm phong, lúc đóng băng tầng 3. Không có lần đọc nhãn test thứ hai.
- **Q11 (NoCaps val × L2-P1):** giữ mặc định GIỮ LẠI. **Phán quyết Q11 là điều kiện tiên quyết của prereg tầng 2** (W9). Prereg tầng 1 ghi rõ: dưới mặc định đó C không có tập dượt P_obj^VI và **dừng trước tầng 2** (v3 l.431). Đây là phép bác bỏ chính trên đường đi của C.

**Các cổng tầng 1 có tên (chạy theo thứ tự, trước bất kỳ máy thuê nào cho C; chỉ đếm):**

| Cổng | Nội dung | Đọc gì | Output |
|---|---|---|---|
| **G-A** nối id (W2; NB4, N-e) | Tải `nocaps_test_image_info.json` (công khai; chỉ id và id OI, không caption) và ghim sha trong prereg tầng 1. Nối id OI của NoCaps test với `oiv7_val_ids.txt` (4b7a1813), với **đủ 3.600 id XM3600** (OI test 1.399, val 456, train 1.745; danh sách chỉ-id lấy từ file caption XM3600 công khai, sha ghim trong prereg tầng 1; không chỉ 456 id của 54966ca7) **[CC-219 W1]**, với id NoCaps val, và với danh sách id OIV7 test. Xác nhận NoCaps test chỉ thuộc OI test | Chỉ id | Số ảnh NoCaps test thuộc OI val, OI test, 41.164 ảnh của L2-P1 và 3.600 ảnh XM3600 (dự kiến ≈ 118 trùng theo ngẫu nhiên). Số ảnh còn lại sau phần loại theo id của §9.3 |
| **G-B** phép đếm độ phủ duy nhất (W3; N9, N-d) | Chạy **sau** G-A và **sau khi Q2 được phán** (§3.2 mục 5), với từ vựng đã cố định (27f2b1ca, 69 lớp). Đọc dòng `oidv7-{val,test}-annotations-human-imagelabels.csv` (md5 so với bucket), lọc theo id NoCaps test còn lại. Chạy **một lần**, trên CPU laptop, trên tập còn lại sau phần loại theo id của G-A (W25 chạy sau, xem §9.3 mục n_e) **[CC-219 W1; CC-219r2 NB-W25]** | Chỉ nhãn người; không caption, không output | n_e, số cặp có mặt / vắng mặt đã kiểm, tỉ lệ phủ (§3.2). Phần loại W25 về sau được báo lại dưới dạng chênh lệch đếm. **Niêm phong [CC-219 W2]:** G-B chỉ ghi và in n_e, tổng số cặp có mặt / vắng mặt đã kiểm và tỉ lệ phủ. Không ghi file hay con số nhãn NoCaps test theo lớp hoặc theo ảnh; cấm dùng lại đường dựng XM3600 (`scripts/xm3600_oiv7.py` l.161 `pairs_per_class`, l.174-176 file LABELS theo ảnh). Mọi file trung gian chỉ giữ sha cho tới lúc đóng băng tầng 3. Code G-B được ghim trong prereg tầng 1 trước khi chạy; k, captioner và prompt được ghim trước khi G-B chạy |
| **G-C** mô hình sạch | §5.2, §9.1 | Thẻ mô hình, danh sách SFT, id | Trạng thái SẠCH / TRÚNG / KHÔNG KIỂM ĐƯỢC cho từng mô hình × tập |
| **G-D** kiểm id (W8; NB15, N-h) | Chép `idcheck.py` và `idcheck_out.txt` (040e78ef / 13d59e15) vào `scripts/` (ví dụ `scripts/c_pvr/`) cùng prereg tầng 1, chạy lại, rồi so output byte với byte | Chỉ id | Cùng sha 13d59e15, hoặc báo chênh |

G-A và G-B không phải một lần xem test: chúng không có caption, dự đoán hay điểm. Cả hai được ghi vào prereg tầng 1 trước khi chạy. **Lượt viết v4 không chạy cổng nào.**

## 10. Nhánh, tên bài và nơi nộp

**Tên bài chính (mọi nhánh):** *Verify Before You Borrow: Proposition-Verified Retrieval for Vietnamese Image Captioning*.
- Tên này khớp đề cương v16 l.321 [CT4].
- Có 10 từ, hoặc 11 nếu tách phần có gạch nối.
- Luật TALLIP "Typically … from 6 to 12 words" lấy từ trang author guidelines (https://dl.acm.org/journal/tallip/author-guidelines, đọc 2026-10-27; `.claude/skills/venue-tallip/SKILL.md` l.13, l.27; W19).

**Đối chiếu với CC-214 ruling 6.** Ruling 6 đòi gold người ViTextCaps hoặc VieCap4H thì mới được có tên hay claim "Vietnamese captioning". PI-1101u, dòng PI mới nhất, định nghĩa lại mốc `vietnamese_caption_test_available`: nhãn người Open Images trên caption tiếng Việt bây giờ là gold. Vì vậy tên bài chính được phép. Phạm vi claim bị giới hạn theo §1: object precision so với nhãn người kiểm, không phải chất lượng dựa trên tham chiếu, trừ N-A.

**Hạn cho dữ liệu.** v3 đặt hạn cứng 15/11. Theo PI-1101u ("thêm ViTextCaps nếu được phát hành"), v4 đề xuất kiểm lại **hằng tuần** cho tới khi khoá prereg tầng 3 (§14 Q7).
- Bộ dữ liệu được phát hành công khai trước lúc khoá thì vào nhánh N-A hoặc N-B.
- Phát hành sau lúc khoá thì không thêm vào C.

| Nhánh | Điều kiện | Claim (luôn là tiếng Việt) | Nơi nộp |
|---|---|---|---|
| N-A | ViTextCaps test có tham chiếu người viết được phát hành công khai trước khi khoá prereg tầng 3, qua B8/B10 | Chính: P_obj^VI trên NoCaps test. Phụ: CIDEr-VI giữ riêng trên ViTextCaps test, proxy VI. Benchmark: EN NoCaps | TALLIP. Neurocomputing chỉ khi cả hai phần tiếng Việt đều đạt |
| N-B | Chỉ tham chiếu VieCap4H private test được công bố công khai | Như N-C, cộng VieCap4H là test **phụ** (CIDEr ghi "nhiễu") | TALLIP |
| **N-C** (mặc định khi không có bộ nào được phát hành) | Không có bộ nào; OpenViVQA dev có mô hình SẠCH | **Chính: P_obj^VI trên NoCaps test.** Phụ: proxy chữ VI trên OpenViVQA dev, ghi rõ là proxy. Benchmark: CIDEr EN NoCaps (EvalAI) | TALLIP (NB3) |
| **N-D** | N-C, nhưng OpenViVQA dev không có mô hình SẠCH | **Chính: P_obj^VI trên NoCaps test.** Chữ trong cảnh chỉ ở mức dev, ghi rõ. Benchmark: CIDEr EN NoCaps. **Không phải bài chỉ-tiếng-Anh** (PI-1101t) | Imaging Science Journal, dự phòng PRIA (NB3) |
| Dừng | Luật dừng ở §4; **hoặc** §10.1 dòng 2; **hoặc** G-B / cổng power trượt; **hoặc** Q11 giữ ở mặc định (dừng trước tầng 2) | Bỏ claim phía đầu vào. Áp luật đổi hướng | Bản thảo CC-212 là phương án dự phòng (chỉ PI chọn được việc quay về CC-212) |

**Luật nơi nộp (NB3, chốt ở cổng tầng 3):**
- TALLIP nếu proxy OpenViVQA có mô hình sạch và đã được đăng ký;
- nếu không, Imaging Science Journal, rồi PRIA.

Claim ở **mọi** nhánh là tiếng Việt. Không nhánh nào là bài chỉ-tiếng-Anh. Nhánh N-D chỉ-tiếng-Anh của v3 đã bị rút (PI-1101t).

**Ghi nhận cho PI.** Khi claim chính là tiếng Việt, TALLIP vẫn hợp với N-D, kể cả khi không có proxy. Mặc định vẫn theo NB3 như yêu cầu (§14 Q8).

### 10.1 Nhánh không có mô hình sạch (thay v3 §10.1)

| # | Điều kiện (sau §9.1) | Hệ quả |
|---|---|---|
| 1 | Một tập test giữ riêng không có mô hình SẠCH cho mọi vai trò của nó | Claim trên tập đó bị bỏ. Tập đó không được chấm ở tầng 3. Không thay bằng tập khác |
| 2 | **NoCaps test không có captioner VI hay bộ kiểm chứng VI nào SẠCH** (G-C) | Không còn claim tiếng Việt giữ riêng → **Dừng**. Không được rút về bài chỉ-tiếng-Anh (PI-1101t) |
| 2b | NoCaps test không có mô hình EN SẠCH cho benchmark | Không chạy benchmark EN, báo "không chạy (mô hình)". Claim VI không bị ảnh hưởng |
| 3 | OpenViVQA dev không có mô hình SẠCH | Nhánh N-D |
| 4 | ViTextCaps test hay VieCap4H test không có mô hình SẠCH | Tập đó chỉ ở mức dev; nhánh rơi về N-C (hoặc N-D nếu dòng 3 cũng đúng) |

**Salami:** giữ v3 §10. Chỉ một bài; bản thảo CC-212 là phương án dự phòng, chỉ kích hoạt ở dòng Dừng.

## 11. Bảng điều kiện tiên quyết, chi phí và lịch

### 11.1 Tầng 1 (dev-explore)

| Mục | Nội dung |
|---|---|
| Giấy phép | PI-1101u nhận hướng. Prereg tầng 1 cần lượt đọc judge riêng và commit của gatekeeper trước job GPU đầu tiên. Lượt đọc v4 làm trước (§14 Q1) |
| Cổng trước khi thuê máy | G-A, G-B, G-C, G-D (§9.3), theo thứ tự; lượt đọc prereg tầng 1; số dư đủ (dưới đây); thứ tự 4090 (dưới đây) |
| Dữ liệu | Chỉ dev: **XM3600-vi**, KT-C (chỉ EN), lát T_A, ViTextVQA dev, KTVIC test, OpenViIC test. Không chạm Karpathy val, NoCaps val, O_B hay bất kỳ tập test nào |
| Thứ tự trước decode | (1) §9.3 W25 trên toàn sổ và loại; (2) luật tự truy hồi §9.2; (3) ghim XM3600-vi, KT-C và các datastore cuối cùng (sha); rồi mới decode |
| Luật quyết định | Bốn việc, theo thứ tự: (i) SESOI_P; (ii) headroom (§4); (iii) biến thể UNCERTAIN (§5.3); (iv) đi tiếp nếu ước lượng điểm ΔP_obj^VI(PVR − A8) ≥ SESOI_P trên XM3600-vi. Luật quyết định của proxy được chốt trước output đầu tiên (§7.7) |
| SESOI_P (W5) | SESOI_P = max(1,0 điểm %; 0,25 × (P_obj^VI(A12) − P_obj^VI(A1)) trên XM3600-vi ở tầng 1, sau §9.2). Cố định cuối tầng 1, trước tầng 2. **Không co giãn theo n của test.** Chỉ power và P(PASS) được chiếu sang n_e |
| Biên NI | δ_C = 2,0 CIDEr-VI (ghi là lenient), δ_R = 2,0 điểm % (§3.1) |
| Máy | Một RTX 4090 24 GB. ID máy ghi vào prereg lúc thuê, trước bài đo tốc độ |
| Đo tốc độ | ≤ 1,0 GPU-giờ: 200 ảnh XM3600-vi × mọi nhánh VI, cộng 200 ảnh KT-C × S1–S5 EN |
| Trần GPU | ⌈1,25 × P1⌉, **trần cứng 20 GPU-giờ** (khoảng 350 nghìn đồng ở 17.499 đ/giờ, giá M8) |
| Thứ tự cắt nhánh | Giữ v3 (A10 → A5 → A9 → A3 → A2 → A4 → A11). Không bao giờ cắt PVR-drop, PVR-keep, A8, A1, A0, A6, A7, A12 |
| Kiểm tiền (W16) | Số dư mới nhất trong LOG: **552.505 đ lúc 21:38 giờ VN ngày 01/11** (OPS-1101m8-rent). M1 + M8 tiêu 26.781 đ/giờ, nên về 0 khoảng **18:15 giờ VN ngày 02/11** nếu không nạp. Việc nạp tiền theo PI-1101r chưa được ghi. Lúc thuê cần số dư ≥ 1,25 × P1 × 17.499 đ + thời gian setup |
| Thứ tự 4090 (CC-214r3 ruling 7, Q9) | B tầng 1 (CC-217) và VSPS-J E2b (CC-215r2) dùng 4090 riêng trước. C tầng 1 chạy sau các job đó |
| Điều kiện dừng (W16) | Đạt trần; hoặc số dư < 3 giờ 4090; hoặc hai lần khởi động lại thất bại; hoặc tới lượt máy của **B tầng 1 (CC-217)**, B tầng 3 hay VSPS-J E2b; hoặc headroom < 2 điểm % |

### 11.2 Tầng 3 (một lần xem test)

| Mục | Điều kiện trước khi đăng ký |
|---|---|
| Hướng | PI-1101u; v4 qua lượt đọc (§14 Q1); prereg tầng 1 và tầng 2 đã qua judge và đã commit |
| Tầng 1 và 2 | Chỉ trên dev. Tập dượt P(PASS) ≥ 0,98 ở n_e: **NoCaps val** (P_obj^VI, sau Q11) và **O_B** (proxy; không dùng nếu có mô hình Vintern). Guard CIDEr-VI đạt trên KTVIC test và OpenViIC test. **T_B bị gạch** (W6) |
| Công bố (W6) | Ảnh TextVQA train trong SFT của LLaVA-1.5 trùng với ảnh TextCaps train (cùng nguồn). Vì vậy T_A, một lát dev của TextCaps train, bị nhiễm với LLaVA-1.5. Chỉ là dev, được công bố |
| Cổng độ phủ | G-B đã chạy một lần. Cổng power ở n_e đạt (§3.2) |
| Mô hình sạch | G-C: có captioner VI và bộ kiểm chứng VI SẠCH trên NoCaps test |
| Dữ liệu được phát hành | Kiểm lại ViTextCaps lần cuối ngay trước lúc khoá (§10) |
| EvalAI | Tài khoản nhóm (Q6); trần nộp đã xác minh trên trang thi (W13); đúng 5 nhánh S1–S5 |
| Giữ ảnh test | Máy test của C được ghi tên; ảnh test chỉ nằm trên máy đó (§8) |
| Luật mức ảnh | §9.3 đã chạy, đã ghi số ảnh loại cho mọi tập |
| Quét lại tính mới | Như v3 §11.2 (S2 12/12 truy vấn; 2609.00591, 2601.22451, 2605.20278; RA-CoA toàn văn; DOI của Adjudicated Captioning; các con số của Li 2024) |
| GPU | Trần lấy từ tốc độ đo ở tầng 1. Mốc lập kế hoạch ở §11.3. Dùng split đầy đủ |

### 11.3 Chi phí cho PI, công và lịch (W17, W18)

**GPU** (giá 4090 là 17.499 đ/giờ):

| Hạng mục | GPU-giờ | Tiền |
|---|---|---|
| Tầng 1 (trần cứng) | ≤ 20 | ≤ khoảng 350 nghìn đ |
| Tầng 3, mốc của CC-214r3 W17 | khoảng 70–90 | khoảng 1,22–1,57 triệu đ |
| Toàn bộ C, mốc W17 | khoảng 110 | khoảng 1,92 triệu đ |
| **Ước lượng lập kế hoạch của v4, tầng 3** | khoảng 95–125 | khoảng 1,66–2,19 triệu đ |

- **Vì sao v4 cao hơn.** v3 sinh caption tiếng Anh cho khoảng 13 nhánh trên NoCaps test. v4 sinh caption tiếng Việt cho khoảng 13 nhánh **cộng** 5 nhánh tiếng Anh, tức khoảng × 1,38.
- Đây chỉ là ước lượng lập kế hoạch. Trần thật lấy từ tốc độ đo ở tầng 1.

**Công** (ngày làm việc của tác tử; ước lượng):

| Việc | Ngày |
|---|---|
| Lượt đọc v4; prereg tầng 1 và lượt judge | 3 |
| Cổng G-A đến G-D | 1 |
| W25 cho các tập của C (CPU nặng, chạy trên máy thuê) | 1–2 |
| Tầng 1: chạy và phân tích | 3 |
| Prereg tầng 2, Q11, chạy, phân tích | 4 |
| Prereg tầng 3, EvalAI, chạy (4–5 ngày thực), chấm | 7 |
| Viết bản thảo TALLIP và các lượt judge | 12 |
| **Tổng** | **khoảng 31–32 ngày tác tử** |

- PI: khoảng 2–3 ngày (trả lời Q1–Q11, tài khoản EvalAI, nạp tiền, đọc study brief).

**Lịch (làm sớm nhất có thể):**
- tầng 1: cuối 11/2026, sau B tầng 1 và E2b;
- tầng 2: 12/2026;
- lần xem test: **01/2027**, nếu Q11 đã được phán và các cổng đạt;
- bản thảo: 02/2027;
- nộp: 03/2027 (đề cương v16).

Báo cáo tháng 01/2027 (PI-1026v) sẽ có trạng thái lần xem test, dù đạt hay chưa. Mốc 02/2027 cho lần xem test của v3 là sau tháng báo cáo; v4 kéo lên 01/2027 (W18).

## 12. Trạng thái sau CC-214r3 và PI-1101u

**G1 (mốc `vietnamese_caption_test_available`).** Mốc này được đóng bằng lựa chọn của PI ở PI-1101u, không phải bằng sửa văn bản. Gold tiếng Việt là nhãn người kiểm Open Images trên caption tiếng Việt, và không phải AI-silver.

**Các mốc khác** giữ như CC-214r3:
- prior_art_checked;
- no_new_labels (nhãn OI là nhãn người có sẵn);
- no_circularity (không outcome nào do bộ kiểm chứng, VLM hay độ đo của B tính);
- kv4224_and_owner_exclusions_checked.

`narrowing_rule_written` được viết lại ở §10 với các nhánh có claim tiếng Việt.

**B1–B7 của CC-214r2** vẫn đóng như v3 §12, với các thay đổi:
- B4 thêm việc gạch T_B;
- B7 (phạm vi N-D chỉ-tiếng-Anh) được thay bằng N-D có claim tiếng Việt (§10).

**Những gì v4 không tự cấp phép:**
- không decode;
- không thuê máy;
- không tải tập nào được giữ riêng (G-A chỉ tải file id công khai, và chỉ sau khi prereg tầng 1 ghi cổng đó);
- không commit.

## 13. Các mục không chặn của CC-214r3: cách xử lý từng mục

Nhãn lấy theo output của panel (J1 N1–N13; J2 NB1–NB15; J3 N-a…N-o). Cột "W" là mục đã gộp trong file CC-214r3.

| Mục | W | Xử lý (một dòng) |
|---|---|---|
| N1 | W1 | §7.7: đối chứng chính, SESOI_T và δ_RT của proxy được chốt trong prereg tầng 1 trước output đầu tiên; điều kiện A11 dùng SESOI_T (§4) |
| N2 | W2 | Cổng G-A có tên, chỉ đếm, chạy trước khi thuê máy (§9.3); cổng 90% được thay bằng phép đếm cộng cổng power ở n_e sau phần loại của §9.3 (§3.2, Q2) |
| N3 | W4 | Báo số cặp có mặt / vắng mặt đã kiểm cho từng tập, cùng tỉ lệ mention kiểm được (§3.1); "sai" cần nhãn vắng mặt đã kiểm |
| N4 | W5 | SESOI không co giãn theo n; chỉ power/P(PASS) chiếu sang n_e (§4, §11.1) |
| N5 | W6 | T_B bị gạch (§3.2, §11.2); công bố chuyện TextVQA-train của LLaVA-1.5 trùng TextCaps train (§11.2) |
| N6 | W7 | Luật 3 ghi theo PI-1101u; các dòng PORTFOLIO chỉ có hiệu lực qua commit của gatekeeper (§9.3) |
| N7 | W8 | G-D: commit idcheck.py và output vào `scripts/` cùng prereg tầng 1, rồi chạy lại (§9.3) |
| N8 | W9 | Prereg tầng 1 ghi: dưới mặc định GIỮ của Q11, C không có tập dượt P_obj^VI và dừng trước tầng 2 (§9.3) |
| N9 | W3 | Từ vựng cố định bây giờ (69 lớp, 27f2b1ca) trước phép đếm G-B duy nhất; không mở rộng (§3.1, §9.3) |
| N10 | W10 | §14 Q2 cũ: khuyến nghị là KHÔNG, mặc định bị gạch; dòng PORTFOLIO đọc trung lập (§15) |
| N11 | W11 | Trích PLAN l.58 (§0.1) |
| N12 | W12 | Công bố việc loại dư có chủ đích ở dev cho KT-C (593 A-T3, 328 M0) (§3.3) |
| N13 | W13 | Trần nộp EvalAI được xác minh trong prereg tầng 3 (§8, §11.2) |
| NB1 | W10 | Như N10 |
| NB2 | W14 | Tên nhánh theo file: N-C là mặc định, N-D là N-C không có mô hình OpenViVQA sạch; cả hai bây giờ có claim tiếng Việt (§10) |
| NB3 | W15 | Luật nơi nộp ở cổng tầng 3: TALLIP nếu proxy có mô hình sạch và đã đăng ký, nếu không thì ISJ rồi PRIA; claim luôn là tiếng Việt (§10) |
| NB4 | W2 | Như N2 (G-A, G-B) |
| NB5 | W9 | Như N8: phán quyết Q11 là điều kiện tiên quyết của prereg tầng 2 (§9.3) |
| NB6 | W16 | Dòng dừng thêm B tầng 1 (CC-217); dòng tiền cập nhật 552.505 đ / 26.781 đ mỗi giờ (§11.1) |
| NB7 | W17 | Chi phí cho PI: 70–90 GPU-giờ tầng 3 (khoảng 1,22–1,57 triệu đ), khoảng 110 tổng; ước lượng v4 là 95–125 cho tầng 3 (§11.3) |
| NB8 | W7 | Như N6 |
| NB9 | W18 | Ước lượng công khoảng 31–32 ngày tác tử cộng 2–3 ngày PI; dòng STATE đề xuất (§15); lần xem test kéo lên 01/2027 (§11.3) |
| NB10 | W19 | Nguồn luật 6–12 từ: author guidelines của TALLIP, đọc 2026-10-27 (§10) |
| NB11 | W1 | Như N1 |
| NB12 | W11 | Như N11 |
| NB13 | W20 | Đọc lại theo PI-1101s: dữ liệu công khai không cần thư; ViTextCaps (chưa phát hành) và tham chiếu private VieCap4H (chưa công bố) vẫn không dùng được; kiểm ViTextCaps hằng tuần (§10, §14 Q7) |
| NB14 | W6 | Như N5 |
| NB15 | W8 | Như N7 |
| N-a | W11 | Như N11 |
| N-b | W10 | Như N10 |
| N-c | W12 | Như N12 |
| N-d | W3 | Như N9 |
| N-e | W2 | Như N2 |
| N-f | W9 | Như N8 |
| N-g | W13 | Như N13 |
| N-h | W8 | Như N7 |
| N-i | W16 | Như NB6 |
| N-j | W1 | Như N1 |
| N-k | W5 | Như N4 |
| N-l | W6 | Như N5 |
| N-m | W7 | Như N6 |
| N-n | W14 | Như NB2; tên bài chính thống nhất "Verify Before You Borrow … Vietnamese Image Captioning" (§10) |
| N-o | W20 | Dòng TextCaps ở C_PUBLIC_DATA_CHECK §3 đã sửa ở lượt này, trích PI-1101s (§15) |
| (chủ toạ) | W21 | Toàn bộ v4: N-D bị rút, claim chính tiếng Việt, bộ khớp và từ vựng cố định trước mọi decode, EN NoCaps chỉ là benchmark, tên bài không mở đầu bằng tiếng Anh |
| G1 | — | Được đóng bởi PI-1101u (§12) |

Bảng các mục không chặn của CC-214r2 (N1–N16) giữ như v3 §13, với một thay đổi: pin bộ khớp (N1) được thay bằng §0.

## 14. Câu hỏi cho PI

Mỗi câu kèm khuyến nghị và mặc định. Không việc nào không đảo ngược được sẽ chạy theo mặc định.

1. **Q1. Lượt đọc tiếp theo.**
   - Bối cảnh: PI-1101u ghi bước tiếp theo là "v4, rồi prereg tầng 1 với lượt đọc judge riêng". Còn chủ toạ CC-214r3 ghi "v4 cộng một panel mới theo dòng PI". Hai câu này khác nhau.
   - Khuyến nghị: **một judge đọc diff** v4 so với PI-1101u và W1–W21, ở ngưỡng không đảo ngược 92. Lượt đọc phải phán rõ ba thay đổi thiết kế: cổng độ phủ (Q2), SESOI chuyển sang XM3600-vi, cổng mô hình sạch tiếng Việt. Nếu < 92 thì mở một panel đầy đủ (CC-214r4).
   - Mặc định: như khuyến nghị.
2. **Q2. Cổng độ phủ.**
   - Khuyến nghị: thay ngưỡng 90% ở cấp ảnh bằng phép đếm một lần cộng cổng power ở n_e (§3.2). Lý do: cùng bộ khớp chỉ phủ 58,9% ảnh XM3600.
   - Mặc định: luật của v4, chờ lượt đọc ở Q1; **G-B không chạy trước khi Q2 được phán**. Nếu PI muốn giữ 90% thì C nhiều khả năng dừng ngay sau G-B.
3. **Q5 (PI-1). Thế nào là "kiểm được"?** Câu này bây giờ quyết cổng G-C cho các mô hình tiếng Việt.
   - Khuyến nghị: dữ liệu SFT/fine-tune đã công bố và nối được id; pretrain web-scale và pretrain căn chỉnh web-scale ghi là "chưa biết".
   - Mặc định: dùng cách hiểu đó để lọc danh sách ở tầng 1. Đăng ký tầng 3 chờ phán quyết. Nếu không có mô hình tiếng Việt nào SẠCH thì Dừng (§10.1 dòng 2).
4. **Q11. NoCaps val × L2-P1.**
   - Khuyến nghị: sửa dòng L2-P1 thành 36.707 ảnh chưa dùng, rồi nhả NoCaps val cho C làm tập dượt P_obj^VI. Việc này phán trước prereg tầng 2.
   - Mặc định: **GIỮ**. Khi đó C dừng trước tầng 2.
5. **Q6 (PI-2). Tài khoản EvalAI.**
   - Khuyến nghị: một địa chỉ nghiên cứu do nhóm quản lý, không phải của PI.
   - Mặc định: không xem NoCaps test cho tới khi có tài khoản.
6. **Q9. Nạp tiền và thứ tự 4090.**
   - Khuyến nghị: C tầng 1 (trần 20 GPU-giờ, khoảng 350 nghìn đ) chạy sau B tầng 1 và VSPS-J E2b, sau G-A–G-D, và sau lượt đọc prereg tầng 1. Theo LOG, số dư về 0 khoảng 18:15 VN ngày 02/11 nếu không nạp (M1 + M8).
   - Mặc định: C không thuê máy cho tới khi có tiền và có lượt đọc.
7. **Q7 (PI-3). Hạn cho ViTextCaps.**
   - Khuyến nghị: kiểm hằng tuần (thứ Hai, giờ VN) cho tới khi khoá prereg tầng 3, thay cho hạn cứng 15/11 của v3, theo PI-1101u. Không gửi thư (PI-1101s).
   - Mặc định: như khuyến nghị (đảo ngược được; không có lần xem nào bị ảnh hưởng).
8. **Q8 (PI-4). Nơi nộp cho N-D.**
   - Khuyến nghị: theo NB3 (ISJ, rồi PRIA). Ghi nhận rằng với claim tiếng Việt, TALLIP vẫn hợp với N-D. PI có thể chọn giữ TALLIP.
   - Mặc định: NB3, quyết ở cổng tầng 3.
9. **Q2 cũ (TextCaps val sang C?).**
   - Khuyến nghị: **KHÔNG** (panel từ CC-214r2 D3).
   - Mặc định: bị gạch khỏi C.
10. **Q3, Q4, Q10 cũ.** Giữ như v3 §14:
    - ảnh trùng với L2-P1 thuộc L2-P1;
    - C không chạm Karpathy val;
    - D-VI không có UIT-ViIC.
11. **VieCap4H qua aihub** (câu hỏi mở từ C_PUBLIC_DATA_CHECK): khuyến nghị tính là công khai chỉ cho train. Bản đó không có tham chiếu private test, nên không mở được N-B.

## 15. Thay đổi trong file khác ở lượt này, và dòng STATE đề xuất

**`manuscript/directions/C_PUBLIC_DATA_CHECK_2026-11-01.md` §3** (W20, N-o): dòng "phần tiếng Anh vẫn chạy được (NoCaps test qua EvalAI, TextCaps val)" được sửa cho khớp B4, PI-1101t và PI-1101u. sha trước 709903fa, sau f8d111ae.

**`manuscript/directions/PORTFOLIO_3Y_2026-10-29.md` §2.3**: chỉ sửa các dòng của C. File đã có diff chưa commit của tác tử khác; lượt này không động tới phần đó.
- Dòng ViTextCaps, NoCaps test, OpenViVQA dev, VieCap4H: trích PI-1101u và v4, có hiệu lực qua commit của gatekeeper.
- l.180 (TextVQA val / TextCaps val) đọc trung lập (W10).
- Đoạn vai trò dev của C: XM3600-vi; KT-C chỉ EN.
- sha trước af267647, sau 99963dad (v4). v4.1: l.193 sửa theo CC-219 W1, PORTFOLIO trong commit gatekeeper = HEAD a4bcdca1 cộng đúng các dòng C đã được đọc (l.167-170, l.180, l.193, và l.168 sửa theo N20), sha 910ab3bf (CC-219r3 N19); các hunk B5/Objects365 của tác tử khác không vào commit.

**STATE_2026-11-01.md** (`.claude/agents/`; bên điều phối áp dụng). Dòng đề xuất thay dòng C:

`| C | ACM TALLIP (Q2); dự phòng ISJ, PRIA (NB3) | 03/2027 (đề cương v16 CT4; PLAN §4 03–05/2027); lần xem test 01/2027 nếu cổng đạt | PVR "Verify Before You Borrow … Vietnamese Image Captioning", nhận theo PI-1101u. Chính: P_obj tiếng Việt trên NoCaps test so với nhãn người OIV7, qua bộ khớp của A (vi_oiv7_map 27f2b1ca, 69 lớp). Phụ: proxy chữ VI (OpenViVQA dev). Benchmark: EN NoCaps EvalAI ≤ 5 nhánh. C_DIRECTION_v4_1 GO (CC-219r3, 92); prereg tầng 1 đang soạn. Cổng trước khi thuê: G-A nối id, G-B đếm phủ, G-C mô hình VI sạch, G-D idcheck. Dev: XM3600-vi, KT-C (EN). Dượt: NoCaps val (chờ Q11; GIỮ = dừng trước tầng 2). Không bao giờ: Karpathy val, TextCaps val, UIT-ViIC. ViTextCaps: kiểm hằng tuần |`

**Không sửa:** PLAN, HUONG_MOI, C_NOVELTY, C_TEST, C_DIRECTION_v2, C_DIRECTION_v3. Không commit.

**Kiểm câu chữ cũ (grep trên v4).** Các mẫu `test EN duy nhất`, `English Test`, `Training-Free English`, `chiếu sang n của test`, `vào sổ ở CC-214r2`, `l.59` và `15/11` chỉ còn xuất hiện trong ngữ cảnh trích dẫn hay ghi lịch sử. Các mẫu `KT-C` và `T_B` không còn ở dòng nào tính SESOI, headroom, UNCERTAIN hay dượt tầng 2. Kết quả grep ngày 01/11: 0 dòng còn hiệu lực; các dòng khớp còn lại chỉ là trích dẫn hay ghi lịch sử.
