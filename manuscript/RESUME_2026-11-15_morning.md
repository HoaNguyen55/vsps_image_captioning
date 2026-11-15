# RESUME 2026-11-15 (viết 09:35 giờ VN, sau khi một agent dừng vì chạm hạn mức)

Đọc tệp này trước, rồi `manuscript/GOAL_HIEN_TAI.md`, rồi các dòng LOG từ `OPS-1115a` (`.session_backup/2026-10-13/decisions/LOG.md`). Tệp này không chứa số liệu đang giữ kín, không chứa đường dẫn hay khoá của phiên chấm.

## Mốc giờ cứng (giờ VN)

| Mốc | Việc | Lệnh / tệp |
|---|---|---|
| chậm nhất 15:30 hôm nay | người chấm thứ hai (R2) của bài B phải bắt đầu | phiên từ xa đang mở: `OPS-1115c-b-pref-start`; khi R2 báo "Xong vòng làm quen": `~/.cache/vsps_tunnel/remote.sh practice-check B`, rồi đưa PI tin nhắn M2 (addendum v1.1) |
| 17:50 hôm nay (10:50Z) | kết thúc phiên R2, xong hay chưa (CC-409 W3) | `~/.cache/vsps_tunnel/remote.sh end B <OPS-id mới> <yes\|no>` |
| trước 18:00 hôm nay (11:00Z) | đóng phần chấm bài B | `cd ~/.cache/vsps_b/host_prep_b_cc409 && sha256sum -c SHA256SUMS && bash b_close.sh --pi-copy <bản 444 nêu ở OPS-1114bh> [--r2-copy <đường dẫn>]`; ghi dòng record rồi dòng pin đóng (dạng echo, không dùng bpin.sh: CC-409 N4); mã thoát 3 = không đẩy nhãn, một giám khảo đọc |
| tối nay, sau dòng đóng | thuê 1 máy RTX 3090; thứ tự J1 → xoá J1 → J2 → J3 → G0 mới → bước H | `manuscript/HOST_RUN_PLAN_2026-11-15.md`; CC-409 (bước H, bảng mất máy) và CC-410 (J1–J3) đã đóng bằng khớp byte: OPS-1115k, OPS-1115m; skill `running-rented-gpu-jobs`; đọc số dư trước khi thuê |
| trước 12:00 ngày 16/11 (05:00Z) | bước H phải có mã trả về cuối, nếu không: dòng NOT RUN | CC-409 |
| từ 12:00 ngày 16/11 | bài C: dòng mốc, shell C2, đọc, lưu; rồi gói sửa lần 2 | docstring của `manuscript/prereg/2026-11-11_c_attr_dev/paper_text/transfer/c_attr_c2_transfer.py`; sau khi lưu C2: `python3 -I manuscript/fix_packages/2026-11-15_C/apply_c_v2_cc408.py --write --ruling CC-408` (CC-408 bản sửa ae06c9f5; 02 nay phải là 8dbc299b) |

Không dòng LOG nào được chứa chuỗi mốc của bài C (gạch-c-gạch-k7-hai chấm) trước mốc 12:00 ngày 16/11.

## Kho bài (HEAD lúc viết)

- Bài A: `ff6ca80` (hôm nay: ea12e51 theo CC-407 bản sửa; ff6ca80 theo CC-411). Còn chặn nộp: UIT-ViIC (chờ PI), thuật ngữ nội bộ ở S11 (sau khi mở phần giữ kín), câu về văn bản xác nhận trong bản đăng ký PASCAL-50S (chờ PI).
- Bài B: `edf7fee`; bản thảo viết lại đang giữ kín ở `.session_backup/2026-11-14/b_text_held/draft_v2/` (người điều phối không mở).
- Bài C: `55315ca` (hôm nay: CC-411). 11 tệp tex/PDF cũ chưa lưu và `docs/CC309_PARAGRAPH_DRAFT.md` không bao giờ được stage.
- Kho chạy: nhánh `paper-v10`; hôm nay chưa lưu gì vào kho chạy (các gói sửa, phán quyết CC-407 đến CC-411, script chuyển C1/C2 còn nợ một lần lưu hồ sơ).

## Quyết định của PI trong ngày

PI-1115a nộp TAIMMA trước, sớm nhất có thể · PI-1115b không gửi email nào · PI-1115c không khai báo AI, rồi PI-1115d mở lại, chờ PI đọc khảo sát (`manuscript/cfp/AI_DECLARATION_SURVEY_2026-11-15.md`) · PI-1115e agent idle thì đóng hoặc giao việc ngay · PI-1114o được thuê máy dự phòng nếu máy bước H hỏng.

Quyết định cũ phải nhớ: PI-1026az và PI-1110o (sự chấp thuận của các nhóm dữ liệu đã được PI xác nhận, bài viết như một dữ kiện, không hỏi lại, không gỡ).

## Việc đang chạy lúc viết

- `taimma-v2-reviser`: bản thảo TAIMMA thứ hai ở `manuscript/conf_taimma_2027/draft_v2/` (đã có `V1_TO_V2.diff`, `REVISION_NOTES.md`). Sau đó: lượt đọc diff (CC-399 là phán quyết trước), thẻ chấm mù + chấm so với 5 bài CCIS (`calibration_ccis/`), đếm trang trên máy thuê, đối chiếu lại sau mốc 16/11.
- `a-fix-package`: gói sửa bài A v4 (cách gọi "xác nhận" theo trả lời F4; khai báo UIT-ViIC, chỉ áp khi PI quyết; các mục không chặn của CC-407).
- `related-fulltext-check`: lượt tìm tài liệu có hệ thống cho bài C, `manuscript/reviews/C_SYSTEMATIC_SEARCH_2026-11-15.md`.

## Chờ PI

Giờ R2 online · quyết định khai báo AI · UIT-ViIC ở bài A · sự chấp thuận của KTVIC có gồm huấn luyện không · tạp chí dự phòng JVCIR · thứ tự nộp và quy tắc dừng 1/12 của TAIMMA · ai gửi thư (bản nháp ở `manuscript/letters_2026-11-15/`, không ai trong phiên gửi thư) · các trang cần trình duyệt của PI (hướng dẫn SPIC, trang ACM, ba bài chưa đọc được) lưu vào `manuscript/cfp/pi_saved/`.

## Kênh tác giả liên hệ

`/mnt/d/RESPONSE_FROM_CORESSPONDING_AUTHOR.md`: 29 câu + F1–F6 đã trả lời và đã cân nhắc (OPS-1115a, d, e, f). Bản sao chỉ-đọc `manuscript/RESPONSE_FROM_CORESSPONDING_AUTHOR.answers_*.md` chứa dữ liệu cá nhân: không lưu vào kho.

## Hạn mức

Một agent dừng lúc 09:29 vì chạm hạn mức của mô hình; PI đặt lại lúc khoảng 09:30. Đồng hồ đọc được (`~/.config/vsps/usage_check.sh`) chỉ hiện mức 7 ngày: 59% lúc 09:30 (35% lúc 07:00), không hiện hạn mức riêng của mô hình.
