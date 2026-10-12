# Bộ gán nhãn vật thể (300 ảnh)

## Trong thư mục này

| File | Dùng để |
|---|---|
| `gan_nhan.html` | công cụ gán nhãn, mở bằng Chrome, Edge hoặc Firefox, không cần mạng |
| `tasks.js` | danh sách ảnh và câu hỏi (không sửa) |
| `images/` | ảnh |
| `huong_dan.md` | hướng dẫn gán nhãn; cũng mở được trong công cụ bằng nút **Hướng dẫn** |

## Người gán nhãn

1. Giải nén file zip (chuột phải → *Extract All* / *Giải nén tại đây*). Không mở trực tiếp từ bên trong file zip.
2. Mở `gan_nhan.html` trong thư mục vừa giải nén. Nhập **mã người gán** do người phụ trách đưa (ví dụ `nguoi1`) và dùng đúng mã đó ở mọi buổi.
3. Đọc hướng dẫn, làm **Phần 1** (300 ảnh) rồi mới làm **Phần 2**.
4. Bài làm tự lưu trong trình duyệt. Không dùng chế độ ẩn danh và không xoá dữ liệu duyệt web khi chưa xuất file. Cuối mỗi buổi, bấm **Xuất file**: file `vsps-objgold-v1_<mã>.json` sẽ nằm trong thư mục *Tải về* (Downloads).
5. Nếu cần chuyển sang máy khác: mở công cụ trên máy mới, bấm **Nhập file** rồi chọn file vừa xuất.
6. Làm xong: bấm **Xuất file** và gửi file `.json` mới nhất cho người phụ trách qua email hoặc Zalo. Không cần gửi lại ảnh.

## Người phụ trách

**Gửi.** Gửi file zip của bộ này (qua Google Drive nếu email không nhận được file lớn) cho **hai** người gán, mỗi người một mã riêng. Giữ lại `key.json` nằm cạnh file zip và **không gửi file đó**. Bộ `…-batch2.zip` (Phần 3) là đợt 2 tùy chọn, chỉ gửi khi cần.

**Hiệu chuẩn.** Hai người làm 20 ảnh đầu của Phần 1, xuất file rồi gửi về. Chạy lệnh chấm với `--partial`. Nếu pooled κ < 0.6, cùng xem lại hướng dẫn (không sửa bài của nhau) rồi mới làm tiếp.

**Chấm** (trong repo, thay `OUT` bằng thư mục đã build bộ này):

```bash
export NCS_DATA=$PWD/data
# hiệu chuẩn hoặc xem tiến độ: chỉ tính phần cả hai người đã làm
python3 scripts/score_human_gold.py --key OUT/key.json --a1 nguoi1.json --a2 nguoi2.json --partial
# phân xử: OUT_ADJ/vsps-objgold-v1-adj.zip chứa mọi chỗ hai người khác nhau, dạng câu hỏi có/không
python3 scripts/score_human_gold.py --key OUT/key.json --a1 nguoi1.json --a2 nguoi2.json --write-adjudication OUT_ADJ
# gửi zip đó cho người thứ ba, nhận lại file JSON của họ, rồi chấm đầy đủ
python3 scripts/score_human_gold.py --key OUT/key.json --a1 nguoi1.json --a2 nguoi2.json --adj nguoi3.json \
    --out data/results/human_gold.json --pope-out data/object_gold/pope_vi_ktvic.json
```

Nếu có làm đợt 2, đặt file đợt 2 ngay sau file chính của cùng người: `--a1 nguoi1.json nguoi1_batch2.json`. Kiểm tra script: `python3 scripts/score_human_gold.py --self-check`.
