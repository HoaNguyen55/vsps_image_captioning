# Brief vòng 2: phương pháp hoàn chỉnh, metric tối đa, tầm Q1/Q2

## Bối cảnh (đọc trước)
- Hệ thống hiện có: VSPS cho captioning tiếng Việt trên KTVIC (UIT). Qwen2.5-VL-7B đề xuất các mệnh đề có kiểu; Vintern-1B kiểm chứng chúng theo 3 trạng thái; các mệnh đề SUPPORTED được render bằng template thành dữ liệu SFT; cuối cùng QLoRA SFT một captioner chạy một lượt. Phần cứng: một RTX 3090 24 GB.
- Số liệu KTVIC test, đối tượng P/R/F1: VSPS 41,5/36,7/39,0; v2 38,1/42,2/40,1; zero-shot Qwen2.5-VL-7B 31,6/57,1/40,7.
- Các ghi chép đã có, chỉ được mở rộng, không làm lại:
  - `.paper_work/novel_direction/00..05`, trong đó 05 là bảng xếp hạng; hướng chính là "Know-and-Mention" với hai trục *tồn tại* × *đáng nhắc*.
  - `.paper_work/no_tradeoff/00..04` (đã bị người dùng chê là ghép lego).
  - `.paper_work/research_wall/` gồm 11 báo cáo; `.paper_work/kg_plan/00_KE_HOACH.md` là kế hoạch đồ thị tri thức.
- Dữ liệu đo được hôm nay: 38% đối tượng gold chỉ được 1/5 người gán nhắc. Recall của tập SUPPORTED tăng dần theo số người nhắc: 42 → 57. Verifier làm mất 15–20 điểm recall ở mọi mức độ nổi bật.

## Yêu cầu của người dùng
"Tìm, phân tích, suy luận để tạo nhiều tính mới hơn bước hiện tại. Mục tiêu: đẩy metric lên tối đa, xây phương pháp hoàn chỉnh hơn, nâng image captioning lên tầm xứng đáng Q1/Q2." Không được ghép các bài có sẵn (lego). Muốn thứ sáng tạo, thử thách, nhưng vẫn làm được.

## Quy tắc cứng
- QUYỀN RIÊNG TƯ: tuyệt đối không đưa email, tên hay bất kỳ dữ liệu cá nhân nào của người dùng vào request (không mailto=, không email trong User-Agent, không gửi form).
- Chỉ đọc repo, ngoại trừ đúng một file đầu ra của bạn. Không chạy git, không ssh, không dùng GPU.
- Mọi trích dẫn phải có venue, năm và link kiểm chứng được. Không bịa số liệu; mục nào chưa xác minh được thì ghi UNVERIFIED.
- Viết bằng tiếng Việt (giữ nguyên thuật ngữ tiếng Anh), tối đa khoảng 2.500 từ, mở đầu bằng 5 dòng tóm tắt.
