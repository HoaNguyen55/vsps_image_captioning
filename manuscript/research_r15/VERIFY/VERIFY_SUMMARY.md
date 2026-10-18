# R15 – Kiểm chứng danh mục tài liệu (2026-10-18)

Đầu vào: `A/papers_A.json` (70) + `B/papers_B.json` (70) → **122 bài duy nhất** (117 arXiv, 5 DOI). Chi tiết từng bài: `verify.json`.

## Số liệu
- Trang gốc: tiêu đề khớp 122/122. Tác giả đầu khớp 122/122 (bài HaUI: Crossref không ghi tác giả, đã kiểm bằng PDF).
- PDF: tải được 119/122 (117 arXiv, bản preprint arXiv của UIT-OpenViIC và bài HaUI truy cập mở). Tất cả bắt đầu bằng `%PDF`, lớn hơn 50 KB, có sha256 trong `verify.json`.
- Tiêu đề có ở trang 1 của PDF: 118/119. Bài lệch duy nhất là UIT-OpenViIC (xem dưới).
- Nhận định trong REVIEW: 146 dòng (bài, dòng). **SUPPORTED 138, NOT FOUND 5, CONTRADICTED 3.**
- 1 bài không có dòng nào trong REVIEW nhắc tới: HallE-Control (arXiv 2310.01779).

## Không tải được PDF (paywall, chỉ kiểm metadata Crossref)
- doi:10.1016/j.jvcir.2026.104963 (HDUCap, JVCIR)
- doi:10.1109/mapr72750.2026.11685699 (ViG, MAPR)
- doi:10.1007/978-3-032-05994-9_8 (30VNFoods, LNNS)

## Lệch metadata
- Bài HaUI (doi:10.57001/huih5804.2025.414) không bị paywall, vì DOI trỏ thẳng tới PDF. Tác giả theo PDF: Van Dung Hoang, Duc Nhan Bui, Thien Nhan Huynh, Trieu Phi Dai (HCMUTE). Trường authors trong papers_B.json cần điền.
- UIT-OpenViIC (doi:10.1016/j.image.2025.117430): PDF là preprint arXiv 2305.04166v2, tên khác: "UIT-OpenViIC: A Novel Benchmark for Evaluating Image Captioning in Vietnamese". Bản tạp chí tên là "An open-domain benchmark ...". Khi trích dẫn bản SPIC thì dùng tên tạp chí, đúng như REVIEW_B dòng 18 đã ghi.

## CONTRADICTED (phải sửa)
1. **REVIEW_A dòng 67, Sandhu et al. (2608.24966).** REVIEW viết bài này "cho thấy lợi ích của SPIN/VCD không bền khi cố định ngân sách token". Sai: kết quả cố định ngân sách nói về phương pháp head-targeted của chính tác giả (mức giảm CHAIR vẫn còn và tăng theo ngân sách: 23% ở 64 token, 58% ở 128 token). Bài nói rõ các so sánh với SPIN/VCD "chỉ đúng trong giao thức này, không phải kết luận chung". Các bản nháp Paper A (sec1, sec2, sec6, outline) đã mô tả đúng, không cần sửa.
2. **REVIEW_A dòng 75, COCO-ReM (2403.18819).** REVIEW viết "điểm thay đổi nhưng thứ hạng phần lớn ổn định" cho cả COCO-ReM và Penquitt. Với COCO-ReM là sai: bài báo thấy thứ hạng thay đổi, nhiều cặp mô hình đổi chỗ. Câu "thứ hạng ổn định" chỉ đúng với Penquitt et al. (2609.21822). Lỗi lý do bị thiếu: COCO-ReM chủ yếu sửa mask không chính xác, không phải chỉ thiếu đối tượng.
3. **REVIEW_B dòng 28, ViCLIP-OT (2602.22678).** REVIEW viết "đã huấn luyện trên KTVIC nên có rủi ro rò dữ liệu". Sai: mô hình chỉ huấn luyện trên UIT-OpenViIC, còn KTVIC và XM3600 chỉ dùng để đánh giá zero-shot. Rủi ro rò thật đến từ chỗ khác: 401/558 ảnh test và 2.464/3.769 ảnh train của KTVIC là near-duplicate của tập train UIT-OpenViIC, và tác giả đã loại các ảnh này bằng SSCD.
   - Lỗi này đã lan sang bản nháp: `journal_draft_B/sec2_related.md` dòng 9 ("it has seen KTVIC in training") và `journal_draft_B/sec7_discussion.md` dòng 30 ("a model trained on KTVIC (for example ViCLIP-OT)").

## NOT FOUND (làm mềm câu chữ hoặc bỏ)
- REVIEW_A dòng 9 và 59: MARINE (2402.08680) "ICML 2025". Comment arXiv chỉ ghi "25 pages, 13 figures, 25 tables", không có journal-ref, PDF cũng không nhắc. Phải kiểm trên trang ICML, hoặc ghi "arXiv preprint".
- REVIEW_B dòng 25: GRIT "là baseline được trích nhiều nhất trên KTVIC". Bài GRIT không thể chứng minh điều này. Nếu giữ thì cần dẫn nguồn khác (chính bài KTVIC).
- REVIEW_B dòng 27: Vintern-1B "zero-shot captioner". Bài giới thiệu mô hình cho OCR, trích xuất tài liệu và VQA, không nói gì về captioning. Nên viết rằng đây là cách chúng ta dùng mô hình.
- REVIEW_B dòng 85: Resnick et al. "giả định người chấm độc lập". Luận điểm chính của bài là phản đối chấm theo majority vote (dựa trên tính khách quan và tính ngang bằng giữa người chấm) và đề xuất chấm theo từng người. Cần viết lại cho đúng.

## Lưu ý (vẫn tính SUPPORTED)
- REVIEW_A dòng 45: khảo sát của Bai et al. (2404.18930) có nhắc, qua POPE, rằng CHAIR bị độ dài caption ảnh hưởng. Câu "không bài nào coi số đối tượng là confound" vẫn đúng ở mức "không kiểm soát", nhưng nên nói rõ ý đó.
- Các venue lấy từ comment arXiv chưa được kiểm lại trên trang hội nghị, ngoài trường hợp MARINE ở trên.

## Kiểm 6 lỗi Gemini nêu (r15_verified_literature_and_gaps.json, sha 922f9278)
Cả 6 đều đúng theo nguồn gốc (Crossref, arXiv, CVF), nhưng phần lớn chỉ ra sai vị trí "where_found":
- BUG-1, CONFIRMED BUG: theo Crossref, 10.18653/v1/2024.findings-acl.657 là bài ICC (Yanuka et al.). OpenCHAIR/MOCHa là 2024.emnlp-main.1263 (EMNLP 2024, tr. 22680-22698). Lỗi nằm ở `novelty/08_preference_rl_captioning.md` dòng 38. papers_A.json ghi "arXiv preprint", nên nâng cấp lên EMNLP 2024.
- BUG-2, CONFIRMED BUG (về DOI): theo Crossref, .50 là Inducer-tuning và .45 là Crossmodal-3600 (tr. 715-729). Tuy vậy không tìm thấy chuỗi "emnlp-main.50" ở đâu trong manuscript/, kể cả dòng 10 của file 09. Có thể lỗi đã được sửa từ trước; papers_B.json không có DOI.
- BUG-3, CONFIRMED BUG (về metadata): trang CVF xác nhận tên "VES-RFT: Rewarding Visual Evidence Sensitivity to Mitigate Hallucinations in Large Vision-Language Models" và 7 tác giả (Hou, Li, Li, Shu, Wang, Chen, Wang). Nhưng VES-RFT không có trong papers_B.json; file 08 đã ghi đúng tên. Gemini ghi sai vị trí.
- BUG-4, CONFIRMED BUG: PDF của HaUI xác nhận 4 tác giả như Gemini nêu (xem mục Lệch metadata).
- BUG-5, CONFIRMED BUG (về ID): arXiv 2411.12004 là bài hóa lượng tử của Semidalas et al. Nhưng ID này và NOAH không có trong papers_A.json hay ở đâu trong manuscript/, nên không có gì để sửa.
- BUG-6, CONFIRMED BUG (về ID): arXiv 2304.10113 là SATA (Chakrabarty et al.). Nhưng ID này và ViOCRVQA không có trong papers_B.json hay manuscript/, nên không có gì để sửa.

## Việc cần làm
1. Sửa REVIEW_A dòng 67 (Sandhu), dòng 75 (tách COCO-ReM khỏi câu "thứ hạng ổn định") và dòng 9/59 (venue của MARINE).
2. Sửa REVIEW_B dòng 28 và hai chỗ trong Draft B (sec2 dòng 9, sec7 dòng 30): ViCLIP-OT huấn luyện trên UIT-OpenViIC, và rủi ro rò là ảnh KTVIC trùng UIT-OpenViIC (401/558 ảnh test).
3. Sửa REVIEW_B dòng 25, 27 và 85 theo mục NOT FOUND.
4. Điền tác giả HaUI vào papers_B.json, nâng MOCHa lên EMNLP 2024 (sửa DOI trong file 08).
5. Bổ sung dòng nhận định cho HallE-Control trong REVIEW_A, hoặc bỏ bài khỏi papers_A.json.
