# Bản tóm tắt nghiên cứu Paper C (cho PI), 29/10/2026

Bài: "Retrieved or Random Examples? Preregistered In-Context Captioning in Vietnamese and English". Đích: ACM TALLIP (Q2), nộp 01/2027. Hướng hiện tại: **Option E** (không pivot, thu hẹp tuyên bố theo CC-155), trừ khi ViTextCaps về trước 12/11/2026 (khi đó xét lại Option B theo CC-158). Mọi đánh giá dưới đây là ý kiến AI, chưa được chuyên gia kiểm chứng.

## 1. Câu hỏi và thiết kế

- **Câu hỏi.** Khi đưa vào prompt của MLLM các caption của ảnh huấn luyện giống ảnh cần mô tả (`ret`), mức tăng so với zero-shot đến từ việc *truy hồi đúng ảnh* hay chỉ từ việc *thấy văn phong của tập dữ liệu*? Đối chứng chính `rand`: cùng số k caption, rút ngẫu nhiên từ cùng bộ nhớ. Thêm `fix` (một bộ k caption cố định) và `zs` (zero-shot).
- **Mô hình.** Qwen2.5-VL-7B và InternVL3-8B, không huấn luyện; cấu hình (k, thứ tự, đuôi prompt, ngưỡng τ) chốt trên tập dev.
- **Quy trình.** Tiền đăng ký 3 giai đoạn, mỗi tập test chỉ nhìn một lần; SESOI = +2.0 điểm CIDEr-D; CI là paired bootstrap theo ảnh, B = 2,000, khoảng phân vị 95%.
- **Nhánh tiếng Anh.** Lặp lại y nguyên (không chỉnh lại) trên COCO Karpathy test và NoCaps val.

## 2. Kết quả chính (số lấy nguyên văn từ bản thảo, giữ cách viết số kiểu Anh: dấu phẩy ngăn hàng nghìn, dấu chấm thập phân; mọi số có khoá trong `number_manifest_C.tsv`)

| Hàng | Kết quả | Phán quyết |
|---|---|---|
| P1, OpenViIC test (1,941 ảnh), `ret` − `rand` gộp | +4.49 [3.52, 5.57] | PASS |
| P1b, Qwen2.5-VL | +8.33 [7.01, 9.76] | xác nhận |
| P1b, InternVL3 (τ = 0.10) | +0.66 [−0.68, 1.99] | chỉ báo cáo (không phát hiện) |
| P2, độ chính xác đối tượng count-matched so với `zs` | Qwen +5.41 [3.88, 7.01]; InternVL3 +1.57 [0.65, 2.51] | PASS cả hai |
| P1-EN, COCO Karpathy test (5,000 ảnh) | +3.08 [2.08, 4.03] PTB CIDEr-D | PASS |
| COCO, InternVL3 | −1.64 [−2.79, −0.49] | dưới 0 |
| XM-a, XM3600 tiếng Việt | +0.70 [−0.45, 1.97] | FAIL |
| S-NC, NoCaps val | +1.73 [0.94, 2.50] (in/near/out +4.64/+1.96/+0.43) | FAIL (điểm dưới SESOI) |
| S-zf, OpenViIC, `ret` − `zs` | +14.30 [13.38, 15.24] | đối chứng đăng ký |

## 3. Tuyên bố của bài (sau lượt sửa hôm nay)

1. **Bối cảnh tiếng Việt.** So sánh truy hồi với ngẫu nhiên ở cùng k, cùng bộ nhớ, cho MLLM không huấn luyện, caption ví dụ chỉ ở dạng văn bản. Đối chứng ngẫu nhiên tách mức tăng thành phần "truy hồi" và phần "văn phong trong miền".
2. **So sánh tiếng Anh cùng một giao thức**, không chỉnh lại cấu hình, báo cáo trong từng ngôn ngữ.
3. **Phụ thuộc backbone.** Mọi hàng tách theo mô hình; ablation trên dev (không xác nhận) giải thích một phần khác biệt.
- **Không tuyên bố:** đối chứng ngẫu nhiên là mới (EXTRA, Li et al. 2024 đã có, với captioner được huấn luyện); không tuyên bố ưu tiên; không tuyên bố "cần bộ nhớ trong miền" như một nguyên nhân. Câu cuối abstract nay chỉ nói mức tăng *chỉ qua được ở nơi bộ nhớ và tập test cùng nguồn*, kèm giới hạn: nguồn bộ nhớ và tập test thay đổi cùng nhau, nên đây là quan sát chứ không phải nguyên nhân đã kiểm định (đã sửa ở abstract, §9.1, §10).

## 4. Thay đổi trong lượt này (29/10/2026)

- **Tài liệu liên quan (§2)**: thêm và phân biệt 5 công trình, tất cả đã kiểm tra qua arXiv/Crossref (`paperC_bib_audit.tsv`):
  - Baldassini et al. (CVPRW 2024): ICL đa phương thức chủ yếu dựa vào văn bản; RICES không hơn bỏ phiếu đa số. Gắn với baseline `nn_cons` và lý do cần `rand`.
  - TrueMICL (Chen et al., COLM 2025): MLLM bắt chước văn bản ví dụ, bỏ qua nội dung ảnh.
  - CONCAP (COLM 2025): captioner đa ngữ được huấn luyện, thêm khái niệm vào caption truy hồi, đánh giá trên XM3600.
  - MeaCap (CVPR 2024): bộ nhớ khái niệm + mô hình ngôn ngữ dẫn bởi CLIP, không phải MLLM.
  - CBDT (EMNLP 2025): bộ nhớ ví dụ trong miền dùng lúc giải mã để chọn giả thuyết, không đổi prompt.
- **Supplement**: bảng S1–S4 (15 cột, tràn trang) tách thành phần điểm và phần "(continued)" chẩn đoán; số không đổi (kiểm bằng script đếm token số).
- **Abstract** (viết lại theo rubric khách quan, lượt 2): 195 từ, không ngôi thứ nhất; mở đầu bằng kết quả dương (PASS ở cả hai ngôn ngữ, COCO +3.08 so với SESOI +2.0, OpenViIC +4.49); InternVL3 và hai FAIL ngoài nguồn vẫn được nêu ngắn gọn, nguyên văn.
- **Lượt 2 (theo rubric)**: đoạn biện minh low-resource bằng lời của nhóm (§1, trích Joshi et al. 2020); Bảng 1 so sánh thiết kế với 11 công trình trước (§2; các bảng chính đánh số lại +1); Bảng 21 đặt điểm tuyệt đối của nghiên cứu cạnh số đã công bố (chép từ bảng của từng bài, không chạy lại, không xếp hạng; §8.6); thêm EVCap, ViECap. CCS 2012 đã đối chiếu với file XML CCS chính thức của ACM. Không thêm p-value: quy tắc đăng ký dựa trên CI, p-value sẽ là POST HOC và cần vòng CP trước.
- **Build** (`tex/build.sh`, 2 dòng chỉ về trình bày): bật `lists_without_preceding_blankline` (khoảng 40 danh sách trước đây bị dồn thành văn xuôi nay hiển thị đúng) và bỏ header minipage ở supplement (tránh lỗi LuaTeX khi hai longtable liền nhau).

## 5. Điểm scorecard (ước tính AI, thang 30)

- CC-145 (tạm, 1 giám khảo): 2/3/4/3/1/2 = 15.
- Option E sau các sửa định dạng + DOI công khai (CC-155): 2/3/4/4/2/3 = **18, Q3**.
- **Q2 cần ≥ 20, novelty ≥ 3**; Option E không cung cấp novelty 3. Chỉ Option B (cần ViTextCaps) có đường tới Q2, P(Q2) khoảng 20–25%.

## 6. Mười câu hỏi phản biện dễ gặp, kèm câu trả lời đề xuất

1. **"Đối chứng ngẫu nhiên đã có trong EXTRA và Li et al. 2024, cái mới là gì?"** Đề xuất: thừa nhận ngay ở §2; cái mới là bối cảnh (MLLM không huấn luyện, tiếng Việt, ví dụ dạng văn bản, cùng k, cùng bộ nhớ) và so sánh Việt–Anh dưới một giao thức. Không tranh cãi ưu tiên.
2. **"Mức tăng do Qwen gánh, InternVL3 không có; kết luận có tổng quát không?"** Đề xuất: đồng ý, bài đã báo cáo theo từng backbone và nói rõ trong abstract; §9.1 nêu rằng với 2 backbone không thể biết thuộc tính nào dự báo mức tăng. Nếu được yêu cầu thêm backbone thì đó là thí nghiệm mới, cần PI và tập test chưa dùng.
3. **"Tại sao không có p-value (TALLIP yêu cầu thống kê dạng F, df, p)?"** Đề xuất: quy tắc đăng ký dựa trên CI bootstrap; nếu biên tập viên yêu cầu thì thêm p-value có nhãn POST HOC sau một vòng CP, không đổi phán quyết.
4. **"CIDEr-D là metric dựa trên tham chiếu; mức tăng có phải chỉ do bắt chước câu chữ?"** Đề xuất: thừa nhận (§9.1); có cột PTB và cột stripped đồng thuận, tỉ lệ copy 4-gram và near-verbatim được báo cáo; không có đánh giá người theo quy tắc không tạo nhãn mới.
5. **"'Cần bộ nhớ trong miền' có được kiểm định không?"** Đề xuất: không; bài nay chỉ nói đây là quan sát, nguồn bộ nhớ và tập test bị gộp (confounded). Đây là điểm yếu thật; ViTextCaps/Option B mới kiểm định được.
6. **"KTVIC và OpenViIC dùng chung ảnh; có rò rỉ giữa bộ nhớ và test?"** Đề xuất: đã loại ảnh trùng byte và gần trùng giữa bộ nhớ và mọi tập được bảo vệ; giới hạn dưới ngưỡng pixel được ghi trong §9.
7. **"Tại sao NoCaps FAIL dù CI trên 0?"** Đề xuất: quy tắc đăng ký yêu cầu điểm ≥ SESOI +2.0 và cận dưới > 0; +1.73 dưới SESOI nên FAIL, báo cáo nguyên văn.
8. **"Bước xoá hậu giải mã (guard) có ích không?"** Đề xuất: giả thuyết guard không qua ở dev, báo cáo là kết quả âm đã đăng ký (§6.7); ablation dev cho thấy nó xoá nhiều hơn ở `ret` so với `rand`.
9. **"Mã và dữ liệu có công khai không?"** Đề xuất: phát hành đăng ký, mã test, file quyết định, điểm, id ảnh và sha256; không phát hành caption hay ledger theo từng ảnh. Cần PI quyết DOI công khai (đây là điều kiện để ô artifacts lên 2).
10. **"Công trình này khác gì Rebelo et al. 2025 (captioning đa ngữ không huấn luyện cho viễn thám)?"** Đề xuất: ảnh đời thường tiếng Việt, đối chứng ngẫu nhiên và cố định cùng k, độ chính xác đối tượng count-matched, test một lần có tiền đăng ký; đã nêu ở §2.

## 7. Việc còn mở (PI quyết hoặc cần làm trước khi nộp)

- **DOI công khai cho mã C** (PI): artifacts 1 → 2; thiếu nó thì không qua cổng Q3 "mọi ô ≥ 2". Đề xuất: CÓ, tại thời điểm nộp.
- **Khối tác giả, ORCID, chế độ ẩn danh** (PI): vẫn là `[AUTHOR TO PROVIDE]`.
- **p-value** (TALLIP): cần một vòng CP nếu PI muốn thêm, nhãn POST HOC.
- **ViTextCaps**: thư đã gửi 29/10; hạn chờ 12/11/2026 (giờ VN). Không có dữ liệu thì giữ Option E, Q3.
- **Chấm lại 3 giám khảo** thay cho điểm tạm CC-145.
