# Hướng phát triển VSPS không đánh đổi precision ↔ recall (tổng hợp, 11/10/2026)

Nguồn: 4 báo cáo chi tiết trong thư mục này (01 pipeline kiểm chứng–sửa, 02 tối ưu sở thích, 03 giải mã, 04 cách đo). Mọi số liệu dưới đây được chép từ bảng trong bài gốc, các báo cáo con ghi rõ số bảng. Hội nghị của SC-Captioner (ICCV 2025), MARINE (ICML 2025), HALVA (ICLR 2025) và REVERSE (NeurIPS 2025) đã được kiểm tra lại trên trang chính thức. Những mục chưa xác minh được thì các báo cáo con đánh dấu UNVERIFIED.

## 1. Vì sao bài trước phải đánh đổi: tài liệu chỉ ra đúng cơ chế

Một tín hiệu sửa lỗi **chỉ biết xóa** thì sẽ làm mất recall. Điều này đã được nhiều nhóm đo độc lập:
- **Woodpecker** là phương pháp hậu kiểm, xóa hoặc viết lại phần sai, gần với VSPS nhất. Khi bài khác chạy lại: recall 40,3 → 38,0, Cover 51,0 → 48,9, độ dài 53,4 → 49,7. Xem báo cáo 01.
- **LURE** làm mất 0,7–2,7% đối tượng đúng (01).
- **DPO thuần precision**: OPA-DPO Cover 51,6 → 47,9; HSA-DPO 51,0 → 47,3; CHiP 61,0 → 57,8. Riêng FGAIF làm caption co từ 216 xuống 60 từ (02).
- **Giải mã**: PAI, DoLa, OPERA, VGD, EOS đều làm Cover hoặc recall giảm (03).

VSPS v1/v2 chính là "kiểm chứng rồi xóa". Verifier chỉ có thể loại bớt, nên recall chỉ có thể giảm (36,7 so với 57,1 của zero-shot).

## 2. Ba cơ chế được chứng minh là tăng cả hai phía

| Cơ chế | Bằng chứng (cả hai phía đều được đo) | Chỗ áp dụng trong VSPS |
|---|---|---|
| **A. Thêm bằng chứng thị giác lúc đề xuất** (detector mở từ vựng) | **MARINE** (ICML 2025): trung bình trên 5 VLM, CHAIR_i 5,2 → 3,7 và recall 40,3 → 44,5. **HALC** (ICML 2024): CHAIR_s 26,2 → 21,7, recall 58,5 → 63,4, độ dài không đổi | Thêm kênh detector (Florence-2 / OWLv2 / Grounding DINO) vào bước đề xuất thực thể. Detector cũng cho bounding box, nhờ đó bật được `geometric_check` (đến nay chưa chạy lần nào vì không có box) |
| **B. Phần thưởng/loss kiểu F1**: thưởng phần thêm đúng, phạt phần sai | **SC-Captioner** (ICCV 2025), Qwen2-VL-7B, so với SFT: P 79,99 → 80,20, R 62,68 → 66,00. **BalCapRL / MOCHa**: khi bỏ thành phần recall thì caption co lại (203 → 152). Phản chứng: chỉ dùng tín hiệu độ phủ thì ảo giác quay lại (25,9 so với 10,3) | Phần thưởng mức đối tượng tính trên tập mệnh đề đã kiểm chứng của VSPS: + cho đối tượng SUPPORTED được nhắc, − cho REJECTED, UNCERTAIN không tính. Đây đúng là metric M1 trong kế hoạch KG |
| **C. Loss cục bộ theo cụm từ**, không đè cả caption | **HALVA** (ICLR 2025, LoRA): AMBER CHAIR 7,8 → 6,6 và Cover 51,0 → 53,0, Pareto trên cả 3 mô hình. **mDPO** (EMNLP 2024): CHAIR 7,4 → 4,4, Cover 51,8 → 52,4 | VSPS đã có sẵn dữ liệu cho loại loss này: mỗi mệnh đề REJECTED là một "cụm từ ảo giác" gắn với một mệnh đề đúng cùng chủ thể. Ghép cặp ở mức cụm từ thay cho DPO cả câu (DPO cả câu từng thất bại ở v9 §IV-9) |

Ngưỡng của verifier đóng vai trò cái núm điều chỉnh, giống τ của **REVERSE** (NeurIPS 2025). Ở ngưỡng vừa phải, CHAIR 7,8 → 6,0 và Cover 51,0 → 52,2. Ở ngưỡng gắt, Cover sụp xuống 26,9. Vì vậy phải chọn ngưỡng trên tập dev theo F1, chứ không theo precision.

## 3. Thứ không giải quyết được vấn đề (đừng đặt kỳ vọng)

Giải mã lúc suy luận chỉ thêm khoảng +0,2 đến +0,6 Cover trên Qwen2.5-VL-7B (03). Tốt nhất là **ReVisiT** (ACL 2026, chậm hơn 1,006×), chỉ nên dùng như một lớp chồng thêm để lấy lại chút precision. Nó không bù được khoảng 20 điểm recall đã mất.

## 4. Phương án VSPS-2 (không đánh đổi)

1. **Đề xuất**: Qwen2.5-VL + detector mở từ vựng (cơ chế A). Bỏ trần `--max-entities 8`; đợt thử 16 thực thể đang chạy.
2. **Kiểm chứng**: verifier logit (cổng T0.5 đã qua: κ 0,794; trùng 97,8% trên các phiếu đồng thuận). Có box nên bật được kiểm tra hình học. Chọn ngưỡng trên dev theo F1.
3. **Dữ liệu mục tiêu**: các bản sửa v3 (giới tính chưa kiểm chứng 12,2% → 0,3%, lỗi "số X" 14,2% → 0,4%).
4. **Huấn luyện**: SFT trên v3, sau đó một vòng loss cụm từ kiểu HALVA dùng cặp REJECTED/SUPPORTED (cơ chế C). Có thể thêm phần thưởng F1 mức đối tượng kiểu SC-Captioner (cơ chế B). Dùng QLoRA 4-bit trên 3090, vì chưa bài nào báo cáo chạy trên một GPU 24 GB.
5. **Cách trình bày "không đánh đổi"** (04):
   - Bảng chính: P / R (Cover) / F1 / Hal / số đối tượng, trên 300 ảnh gold do người gán. Bảng phụ: gold suy ra từ caption tham chiếu (558 ảnh).
   - Hình: đường P–R của mọi hệ thống theo cùng một núm "độ chi tiết", có đường iso-F1 và CI bootstrap.
   - Kiểm định kép đăng ký trước: recall tăng có ý nghĩa **và** precision không giảm quá 1 điểm, so với cả VSPS cũ lẫn zero-shot. Chạy 3–5 seed, bootstrap hai tầng.
   - Tránh lỗi của ReflectCAP: tuyên bố "Pareto" khi precision vẫn giảm ở 2/8 backbone và không có CI.
   - Đóng các khe hở: audit mở từ vựng cho 100 caption mỗi hệ thống; POPE tiếng Việt dựng từ gold 300 ảnh. Chưa có benchmark tiếng Việt nào đo ảo giác, nên đây là một đóng góp phụ.

## 5. Tính mới so với tài liệu

- Chưa bài nào kết hợp cơ chế B và C với một verifier **ba trạng thái**, trong đó UNCERTAIN được loại khỏi phần thưởng. SC-Captioner dùng scene graph trên chú thích chuẩn; HALVA dùng phép sửa sinh tổng hợp.
- Tiếng Việt: không có benchmark ảo giác nào (04), và không có bài DPO/RL nào cho captioning tiếng Việt.
- Tính mới phải được kiểm lại với 01–03 và với `research_wall/watch.py` trước khi nộp.

## 6. Rủi ro

- Detector tiếng Anh cần được ánh xạ sang lexicon tiếng Việt; có thể dùng bộ ánh xạ COCO → vi đang có trong `score_coco_probe`.
- MARINE kém đi trên MiniGPT-v2. Tức là Pareto chưa chắc đúng trên mọi backbone, nên phải đo trên chính Qwen2.5-VL.
- Gold suy ra từ caption tham chiếu đếm thiếu đối tượng, nên precision ở đó chỉ là cận dưới (04). Tiêu đề kết quả phải dùng gold do người gán.

## Nguồn chính
- SC-Captioner, ICCV 2025: https://arxiv.org/abs/2508.06125 · https://iccv.thecvf.com/virtual/2025/poster/2454
- MARINE, ICML 2025: https://proceedings.mlr.press/v267/zhao25j.html · https://arxiv.org/abs/2402.08680
- HALVA, ICLR 2025: https://proceedings.iclr.cc/paper_files/paper/2025/hash/b73228d026ef49bfa49f95b7e330513e-Abstract-Conference.html
- REVERSE, NeurIPS 2025: https://neurips.cc/virtual/2025/poster/120029 · https://arxiv.org/abs/2504.13169
- HALC, mDPO, BalCapRL, MOCHa, ReVisiT, AMBER, CAPTURE: xem link trong 01–04.
