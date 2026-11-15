# Kế hoạch thực hiện goal READY FOR SUBMISSION (lập 15/11/2026)

> **Cho agent thực hiện:** làm từng nhiệm vụ theo thứ tự, đánh dấu `- [x]` khi bước có bằng chứng. Mỗi bước ghi một dòng LOG (`.session_backup/2026-10-13/decisions/LOG.md`). Đọc `manuscript/RESUME_2026-11-15_morning.md` trước.

**Mục tiêu:** đưa bản TAIMMA, rồi bài B, A, C và báo cáo khoa học tới READY FOR SUBMISSION, mỗi bài kết thúc bằng thông báo "ready to review" cho PI.

**Cách làm:** mỗi thay đổi đi qua một vòng lặp cố định (mục 2). Việc trên máy thuê theo skill `running-rented-gpu-jobs`; việc văn bản theo chuỗi gói sửa → giám khảo → lưu khớp từng byte.

**Spec:** `manuscript/GOAL_MOI_2026-11-15.md` (goal PI đặt), `manuscript/GOAL_HIEN_TAI.md` (tiến độ).

## Ràng buộc chung

- Không bản thảo nào khai báo công cụ AI; không câu nào viết rằng không dùng AI (PI-1115i).
- Không gửi email; thư chỉ là tệp nháp (PI-1115b).
- Sự chấp thuận của các nhóm dữ liệu là dữ kiện đã chốt; không hỏi lại, không gỡ (PI-1026az, PI-1110o).
- Giữ kín: kết quả bài B với PI tới dòng đóng; số liệu Mục 6.7 và S11 của bài A tới khi buổi gán bổ sung kết thúc. Chỉ đếm dòng, mã băm, giờ tệp của tệp nhãn.
- Mỗi tập kiểm tra chỉ nhìn một lần; kiểm thử và chấm điểm trên máy thuê; máy thuê không để rỗi.
- Trước khi sửa câu khai báo, câu về dữ liệu hay quyền sử dụng: tra LOG tìm quyết định cũ của PI.
- Không dòng LOG nào chứa chuỗi mốc của bài C trước 05:00Z ngày 16/11.
- Agent xong việc: giao việc tiếp hoặc đóng ngay (PI-1115e).
- Lời nhắn lưu kho không có dòng ghi công cho AI.

## 1. Phân công mô hình

| Loại việc | Mô hình | Ví dụ trong kế hoạch này |
|---|---|---|
| Nặng: phán quyết, đọc toàn văn, đối chiếu số liệu với bản đăng ký, đọc kết quả, viết đoạn khoa học | Fable 5.2 | giám khảo CC, đọc kết quả bước H, viết phần kết quả con người của bài B, lượt đọc cuối TAIMMA, chấm mù |
| Nhẹ: điều phối, tổng hợp, ghi LOG, cập nhật tệp mục tiêu và bảng theo dõi, soạn thẻ chấm, làm mới báo cáo, kiểm tra trạng thái | Opus 5.5 | thẻ mù cho TAIMMA, làm mới báo cáo, kế hoạch cắt, danh mục tệp |
| Mã: script áp gói sửa, script dựng, sửa lỗi dựng trên máy, kiểm tra cú pháp | Haiku 5.5 | `apply_*.py`, `build_lncs.sh`, `j2_host_build.sh`, script hình bài B |

Quy tắc an toàn khi dùng Haiku cho mã: mọi script do Haiku viết chỉ chạy ở chế độ kiểm tra cho tới khi kết quả khớp mã băm trong phán quyết của một giám khảo Fable. Script đụng tới tệp nhãn, khoá hoặc bước H không giao cho Haiku (đã được phán ở CC-409, giữ nguyên byte).

## 2. Vòng lặp nghiên cứu (áp cho mọi thay đổi)

```
Quan sát (kết quả mới / lỗi / ý kiến) 
  → Giả thuyết hoặc đề xuất sửa (gói OLD/NEW, có dòng bằng chứng)        [Fable viết nội dung, Haiku viết script]
  → Thử nghiệm: script chạy chế độ kiểm tra; với phép phân tích đã đăng ký: chạy đúng một lần trên máy thuê
  → Đọc: một giám khảo Fable đọc toàn bộ (lượt 1/3), ra GO / GO có điều kiện / NEXT_ROUND
  → Kết quả: lưu khớp từng byte, đẩy lên, dòng LOG; kết quả không đạt vẫn được báo cáo
  → Phản hồi: điểm mới phát sinh quay lại đầu vòng; tối đa 3 lượt, sau đó chuyển PI
```

Điều kiện dừng một vòng: phán quyết GO và mã băm khớp; hoặc hết 3 lượt; hoặc cần quyết định chỉ PI có.

## 3. Nhiệm vụ

### Nhiệm vụ 1: Bài B — đóng phần chấm (15/11, trước 18:00)

**Tệp:** `~/.cache/vsps_tunnel/remote.sh`, `~/.cache/vsps_b/host_prep_b_cc409/` (5 tệp chỉ-đọc), phán quyết CC-409.

- [ ] 15:30: đếm dòng `practice_R2.jsonl` và `labels_R2.jsonl`. Kỳ vọng: vòng làm quen ≥ 8 dòng thì đưa PI tin nhắn M2. [Opus]
- [ ] 17:50: `remote.sh end B <OPS-id> <yes|no>`. Kỳ vọng: dòng `…-b-pref-session-end`, không còn cổng 8792/8890, không còn tiến trình cloudflared.
- [ ] Trước 18:00: `sha256sum -c SHA256SUMS && bash b_close.sh --pi-copy <bản 444 ở OPS-1114bh> [--r2-copy …]`. Kỳ vọng: mã thoát 0, in văn bản record và pin. Mã thoát 3: vẫn ghi hai dòng, không đẩy nhãn, một giám khảo đọc.
- [ ] Ghi dòng record rồi dòng pin đóng (dạng echo). Kiểm: mã băm `labels_PI.jsonl` = 91fa0a30…d65d1.

### Nhiệm vụ 2: Phiên máy thuê (tối 15/11 → trước 12:00 ngày 16/11)

**Tệp:** `manuscript/HOST_RUN_PLAN_2026-11-15.md`, `.session_backup/2026-11-15/host_prep_build/` (sums 64bc7c44), CC-409, CC-410.

- [ ] Đọc số dư, kiểm L-before, thuê 1 máy RTX 3090 đúng thông số; ghi dòng thuê (T0). [Opus]
- [ ] J1 chạy thử mã bài A theo `j1/J1_PLACE.md`. Kỳ vọng: 7 bản ghi OK, SHA256SUMS trùng. Lỗi dựng: Haiku sửa, tối đa một lần khởi động lại. Xoá J1, ghi "J1 absent".
- [ ] J2 dựng PDF bài C từ HEAD lúc dựng. Kỳ vọng: `check_610.py` in 6.10.1–6.10.9 đúng như gõ. Không lưu vào kho.
- [ ] J3 đếm trang bản TAIMMA 2.1 (hai bố cục). Kỳ vọng: `PAGE_COUNT.txt` dòng đầu `PROVISIONAL: yes`, số trang 12–15. Nếu > 15: ghi lại, chuyển Nhiệm vụ 4 bước cắt.
- [ ] G0 mới, đẩy tệp, X16 MATCH, bước H chạy đúng một lần (`bhh.sh` theo dõi). Kỳ vọng: mã trả về cuối trước 05:00Z ngày 16/11; không có: dòng NOT RUN. Mất máy: bảng quyết định CC-409.
- [ ] Kéo kết quả, xoá máy, L-after. Một giám khảo Fable đọc kết quả (thông báo cho PI không chứa kết quả cho tới khi phán quyết cho phép).

### Nhiệm vụ 3: Bài C — mốc 12:00 ngày 16/11 và hai gói sửa

**Tệp:** `manuscript/prereg/2026-11-11_c_attr_dev/paper_text/transfer/c_attr_c2_transfer.py`, `manuscript/fix_packages/2026-11-15_C/apply_c_v2_cc408.py`, `apply_c_v4_search.py`, CC-402, CC-408, CC-413.

- [ ] ≥ 05:00Z: kiểm LOG, ghi dòng mốc theo docstring, chạy script C2 một lần, lưu `C_C2_TRANSFER.diff`. Kỳ vọng: 5 tệp đổi, 2 dòng manifest mới.
- [ ] Một giám khảo Fable đọc toàn bộ kèm khớp byte (lượt 2/3) → lưu, đẩy.
- [ ] `apply_c_v2_cc408.py --write --ruling CC-408`. Kỳ vọng: 10 tệp EQUAL, 02 ở 8dbc299b → kiểm tra cổng lưu (W2, W3) → lưu.
- [ ] `apply_c_v4_search.py --write --ruling CC-413`, rồi script Annex B của CC-413. Kỳ vọng: 5 tệp khớp bảng mã băm cuối → lưu.
- [ ] Dựng lại tex/PDF ở lần thuê kế tiếp; kiểm phông bảng tiếng Việt. [Haiku sửa lỗi dựng]
- [ ] Rà sáu tiêu chí READY cho bài C (bảng ở mục 4) → báo PI "ready to review" hoặc danh sách BLOCKED.

### Nhiệm vụ 4: Bản TAIMMA — các cổng G1, G2, G3 và lượt cuối

**Tệp:** `manuscript/conf_taimma_2027/draft_v2_1/`, `calibration_ccis/`, CC-414.

- [ ] G2 (sau Nhiệm vụ 3): `check_draft.py --build-manifest` rồi kiểm tra trên HEAD mới của bài C; rà các đơn vị ở Ruling 4 của CC-414. Kỳ vọng: 0 số lệch. [Fable]
- [ ] Đưa bốn bài mới từ lượt tìm tài liệu vào bản nháp bằng câu chữ đã sửa của CC-413 (chỉ sau khi gói v4 của bài C đã lưu).
- [ ] G1 chính thức: đếm trang trên văn bản sau G2. Nếu > 15 trang: cắt theo thứ tự N2, c1–c4 của CC-414, chạy lại bộ kiểm.
- [ ] G3: Opus soạn thẻ mù cho bản nháp (venue = "international conference", năm 2027, mục "Key numbers"); ba người chấm Fable chấm mù cùng 5 thẻ CCIS, không tra web; một lượt đọc chuyên gia. Kỳ vọng: điểm của ta ≥ trung vị 5 thẻ tham chiếu ở T1, T5, T6.
- [ ] Lượt đọc thứ ba (cuối) của một giám khảo Fable; GO → báo PI "ready to review". Không đạt → chuyển PI.

### Nhiệm vụ 5: Bài B — văn bản sau bước H

**Tệp:** `.session_backup/2026-11-14/b_text_held/draft_v2/` (28 chỗ chờ số của bước H), kho bài `vsps-paperB-lre`.

- [ ] Sau phán quyết đọc kết quả: Fable điền 28 chỗ chờ đúng từ tệp kết quả; câu công bố của CC-406 nguyên văn; câu về người chấm thứ hai theo đúng nhánh (hai người chấm hoặc một người chấm).
- [ ] Haiku viết script hình 1, 2, EF1; dựng trên máy thuê. Kỳ vọng: số trên hình trùng manifest.
- [ ] Chuyển vào kho bài bằng gói + giám khảo + lưu khớp byte. Mở giữ kín theo phán quyết.
- [ ] Rà sáu tiêu chí → báo "ready to review".

### Nhiệm vụ 6: Bài A — hai buổi gán nhãn và phân tích một lần

**Tệp:** `tools/obj_rater/` (giữ nguyên byte), `tools/label_console/` (cổng 8788), CC-367, CC-395, CC-412.

- [ ] Sau khi bài B đóng: mở phiên người gán thứ hai (150 ảnh, 1.110 câu) qua `remote.sh start A <OPS-id> <tệp thẻ>`; rồi buổi bổ sung của PI (1.755 câu). Theo dõi bằng bảng 8788.
- [ ] Sau dòng kết thúc buổi bổ sung: chạy các phép phân tích đã đăng ký đúng một lần trên máy thuê (mã đã qua J1).
- [ ] Fable viết Mục 6.7 và S11 từ tệp kết quả; sửa thuật ngữ nội bộ ở S11 (CC-407 W5); dòng đính chính PASCAL-50S (W6); đưa lại câu "đã đồng ý" cạnh câu KTVIC (PI-1115i mục 8). Gói + giám khảo + lưu.
- [ ] Đồng bộ tóm tắt, điểm nhấn, thư gửi biên tập; rà sáu tiêu chí → báo "ready to review".

### Nhiệm vụ 7: Báo cáo khoa học — làm mới

**Tệp:** `manuscript/bao_cao_khoa_hoc_2026-11-14/` (`checks/run_all.sh`, `build.sh`).

- [ ] Sau Nhiệm vụ 3: Opus cập nhật Phần C, D, E. Sau Nhiệm vụ 5 và 6: Phần B và A. Kỳ vọng mỗi lần: `ALL PARTS rc=0`, dựng DOCX và PDF, gửi PI.

## 4. Bảng rà READY (dùng ở cuối mỗi bài)

| Tiêu chí | Bằng chứng phải có |
|---|---|
| Đầy đủ khoa học | mọi mục có nội dung; mọi phép thử đã đăng ký có kết quả hoặc dòng NOT RUN |
| Số liệu và trích dẫn | bộ kiểm manifest 0 lỗi; bảng tài liệu liên quan đã đối chiếu toàn văn hoặc ghi "theo tóm tắt" |
| Kỹ thuật | PDF dựng được; hình trùng manifest; mã đã chạy thử trên máy thuê |
| Nhất quán | lượt đọc cuối của giám khảo: 0 điểm chặn |
| Yêu cầu nơi nộp | danh mục của skill `venue-*` đã tích hết; mục nào chưa đọc được trang gốc ghi BLOCKED |
| Rà soát cuối | quét n-gram đạt; không tên máy, địa chỉ, tên công cụ |

## 5. Điểm cần soát kỹ

- Người chấm thứ hai không xong trước 17:50 → nhánh một người chấm đã đăng ký; không kéo dài phiên.
- Mất máy khi bước H đang chạy → chỉ một lần chạy lại, theo bảng CC-409.
- Bản TAIMMA vượt 15 trang → cắt theo thứ tự đã phán, không cắt câu công bố hay kết quả không đạt.
- Trang hướng dẫn của SPIC và ACM chưa đọc được → tiêu chí "yêu cầu nơi nộp" của bài A và C là BLOCKED cho tới khi PI lưu trang.
- Mức dùng tăng hơn 20 điểm trong 3 giờ → báo PI, viết tệp RESUME trước.
