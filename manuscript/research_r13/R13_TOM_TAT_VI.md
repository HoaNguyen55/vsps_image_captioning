# R13: Tóm tắt cập nhật tài liệu (2026-10-15)
Chi tiết: `R13_LIT_UPDATE.md`. BibTeX: `r13_new_refs.bib` (51 mục, tất cả đã kiểm tra trên arXiv API, ACL Anthology hoặc Crossref).

## Rủi ro trùng ý tưởng
1. **CAO (về khung lập luận):** arXiv 2609.01888 "Does Playing it Safe Count as Faithfulness?" (9/2026).
   - Bài này chấm lại 6 phương pháp giảm ảo giác và kết luận: hallucination giảm đi kèm recall và độ chi tiết giảm, tức là giao thức chấm thưởng cho việc "nói ít".
   - Họ không khớp số đối tượng theo từng ảnh, không có đường đặc tả, không có CAR, không có lý thuyết dấu theo độ đầy đủ gold.
   - Việc cần làm: trích dẫn ở §1–§2 của bài A và viết lại đóng góp 1 thành "định lượng có đăng ký trước một mối lo đã được nêu".
2. **TRUNG BÌNH:**
   - 2608.24966: kiểm soát theo số token; SPIN và VCD không giảm ảo giác ổn định.
   - 2609.35294: lối tắt "nói ít"; gold DOPA dày đặc.
   - 2610.14976: CHAIR bị "hack" bằng cách nêu ít đối tượng.
   - Bài B: **HDUCap (JVCIR 2026)**, một bộ dữ liệu tiếng Việt mới công bố ở chính tạp chí mục tiêu. Phải đọc trước 1/11.
3. **THẤP:**
   - VaPR: chỉ nêu lệch độ dài trong dữ liệu ưu tiên, không phải kênh số lượng.
   - CapArena; 2609.21822 (gold COCO thiếu khoảng 40% đối tượng).
   - Không tìm thấy bài nào về: đảo dấu theo k, thống kê liền kề, KTVIC một người viết, chi phí CIDEr của dấu chấm, kênh số lượng trong DPO.

## Phải trích dẫn / sửa trích dẫn
- **UIT-OpenViIC** đã có bản tạp chí: Signal Processing: Image Communication 140:117430 (2026). Thay bản arXiv trong cả hai bài.
- **SumGD** là Findings of NAACL 2025, không phải arXiv 2024 (§2 bài A).
- Đối thủ so sánh của bài B (chỉ xác minh metadata, chưa đọc nội dung):
  - HDUCap: JVCIR 121:104963;
  - ViG: MAPR 2026, trang 652–657.
- Bài A, §2 và §8: CapArena (Findings ACL 2025); CAPability (NeurIPS 2025); VELA/LongCap-Arena (EMNLP 2025); CapMAS (ICML 2025); SPECS (EMNLP 2025).
- Bài B: ViCLIP-OT (2602.22678; huấn luyện trên KTVIC nên có nguy cơ rò rỉ); multilingual CLIPScore (Findings NAACL 2025); Berger NAACL 2025 (biến thiên mô tả theo ngôn ngữ, có tiếng Việt); BamiBERT (không cần tách từ).
- SENTINEL có bản v3 (5/2026). Kiểm tra lại phiên bản dữ liệu đã audit ở §9.

## Ý tưởng mới (không cần gán nhãn mới, làm kịp trước 15/11)
1. LongCap-Arena (32.246 đánh giá của người) làm phép thử giá trị thứ tư cho §8. Khoảng 1,5 ngày CPU, có prereg.
2. Dùng trận đấu cặp của CapArena để tách độ dài và số lượng: so độ đồng thuận trên cặp cùng số đối tượng với cặp khác số. Khoảng 1 ngày CPU.
3. Mở rộng E1 với các phương pháp 2025–26 (ACG, REVERSE, các bản chạy lại SPIN/VCD). Nửa ngày CPU nếu có output công khai; nếu không, 4–8 GPU-h cho mỗi phương pháp.
4. Thêm điểm gold "rất đầy đủ" (COCO-ReM hoặc bản gán lại của 2609.21822) vào Hình 2, với dự đoán đóng băng trước. Nửa ngày.
5. Dùng VaPR (đã khớp độ dài) làm đối chứng dương cho §9. Khoảng 3 giờ CPU.
6. Bài B: kiểm tra bằng metric không cần tham chiếu (mCLIPScore/ViCLIP-OT) rằng dấu chấm không đổi điểm, tức là chi phí −35 CIDEr nằm ở tham chiếu. Khoảng 1 GPU-h.
7. Bài B: bảng chữ ký giao thức cho HDUCap, ViG, OpenViIC-SPIC và ViTextCaps. Đóng blocker PD-2. 0,5–1 ngày đọc.

Không sửa file bản thảo, không commit. Không có tuyên bố "đầu tiên".
