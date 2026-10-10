# R2_03 — Phản biện vòng 2, trục TRÙNG LẶP: M4, M5, M6, bộ phán xét người, gold SG tiếng Việt, parser

Critic 03, ngày 2026-10-10. Đối tượng: `00_KE_HOACH.md` (bản nháp vòng 1), mục 3, 4 và 6 (P1). Mọi request trong phiên là ẩn danh (không email, không mailto, không User-Agent cá nhân).

---

## 1. Phán quyết theo thành phần

| Thành phần | Phán quyết | Lý do một dòng |
|---|---|---|
| M4 CulR / CulOA | **needs-fix** | CulR = object recall giới hạn trên từ vựng văn hóa; CulOA = CHAIR giới hạn trên từ vựng văn hóa. "Gán văn hóa quá đà" đã có tiền lệ (M²CQA/CFHR). Gold 65 ảnh không đủ. Chỉ giữ được với vai trò lát cắt chẩn đoán. |
| M5 TBW | **needs-fix** (gần fail với vai trò "metric mới") | Chính file 19 thừa nhận TbW ≈ 1 − precision của verifier. Khái niệm "trích dẫn đúng nguồn nhưng nguồn sai" đã có trong văn liệu attribution (Wallat et al., ICTIR 2025). Metric chỉ định nghĩa được cho hệ có trace, nên không so được với baseline. |
| M6 NVL | **needs-fix** | ViHG-Cap chặn fact phi thị giác ngay từ thiết kế, nên NVL ≈ 0 có sẵn theo cấu tạo: metric tự phục vụ. Nhãn "không kiểm chứng được bằng mắt" đã có trong HalDec-Bench. Với bài toán caption văn hóa/sự kiện (RAVENEA, EVENTA), fact phi thị giác lại là mục tiêu. |
| "Bộ dữ liệu chấm điểm caption tiếng Việt đầu tiên" | **fail ở dạng hiện tại** | Crossmodal-3600 (EMNLP 2022) đã chấm người side-by-side caption tiếng Việt, nhưng không phát hành dữ liệu. Câu "chưa tìm thấy bộ nào" là sai về mặt sự kiện. |
| Pilot gold SG tiếng Việt 500 ảnh | **needs-fix** | Trùng lặp ở mức chấp nhận được (VietSGG, CompreCap). Nhưng có hai lỗi: (a) gán trước bằng chính pipeline VSPS/Qwen gây thiên lệch neo, ưu ái hệ của mình; (b) ảnh KTVIC không có license, nên "benchmark" không phát hành được ảnh. |
| Parser caption → đồ thị | **pass có điều kiện** | Re-search vẫn không thấy parser SG tiếng Việt. Luật dừng T3 hợp lý. Thiếu một baseline: đường AMR (VLSP 2025 viSemParse → SG, tiền lệ SGRAM). Bộ test "150 caption chi tiết" không có nguồn tham chiếu do người viết. |

Tổng: **1 BLOCKER, 6 MAJOR, 4 MINOR**.

---

## 2. Phát hiện

### F1. "Bộ phán xét caption tiếng Việt đầu tiên" sai sự kiện — **BLOCKER**

- **Plan ghi (mục 3, đoạn meta-eval):** "Đây đồng thời là **bộ dữ liệu chấm điểm caption tiếng Việt đầu tiên** (chưa tìm thấy bộ nào)." P1 (mục 6) bán bộ này như đóng góp chính.
- **Bằng chứng:** Crossmodal-3600 (Thapliyal et al., EMNLP 2022, arXiv 2205.12522). Tôi đã tải PDF và đọc mục Human Evaluation:
  - Có chấm người side-by-side caption mô hình trên XM600 (600 ảnh), thang 7 mức, 3 người chấm mỗi cặp.
  - Tập ngôn ngữ L_EXT (28 ngôn ngữ) có ghi rõ "Vietnamese (vi)". Mục đích là đo tương quan CIDEr với người.
  - Bài viết: "due to the timelines involved and approvals required, we are not able to release this data with the paper."
  - Kết luận: phán xét người cho caption tiếng Việt **đã tồn tại từ 2022**. Nó chỉ chưa được phát hành, chỉ ở mức hệ thống/cặp, và không có cấp mệnh đề.
  - Re-search thêm cho kết quả âm tính: Multilingual CLIPScore (Findings NAACL 2025, 2502.06600) dùng dữ liệu dịch máy; ViTextCaps (2604.27712) chỉ audit 500 tham chiếu do người viết, không chấm output mô hình; VIVID (LREC 2026) chỉ là văn bản; UIT-OpenViIC, KTVIC và UIT-ViIC không có mục chấm người cho output (grep PDF). VMMU, ViExam và ViHallu (DSC2025) không phải chấm caption.
  - Reviewer quen XM3600 sẽ bác ngay claim "first".
- **Sửa (thay nguyên văn câu):** "Đây là **bộ phán xét người cho caption tiếng Việt đầu tiên được phát hành công khai ở cấp caption và cấp mệnh đề**. Crossmodal-3600 (EMNLP 2022) đã chấm side-by-side cho tiếng Việt ở cấp cặp hệ thống nhưng không phát hành dữ liệu (Thapliyal et al., 2022, §Limitations)." Trích XM3600 trong related work của P1.
- **Thay đổi plan đi kèm (rẻ, tăng giá trị):** thêm ~100–150 ảnh XM3600 vào tập meta-eval. Ảnh này có license CC BY 4.0 và tham chiếu tiếng Việt do người bản ngữ viết, nên phát hành lại được. Đồng thời có điểm nối với nghiên cứu duy nhất từng có. Sửa cả dòng rà lại ở mục 9: "chưa có bộ chấm điểm caption tiếng Việt" → "chưa có bộ *công khai*".

### F2. M5 TBW là precision của verifier đổi tên — **MAJOR**

- **Plan ghi (bảng M5):** "Tỷ lệ span truy vết được nhưng mệnh đề nguồn sai theo người | GAVEL: không có trạng thái kiểm chứng."
- **Bằng chứng:**
  - (a) Chính `19_traceable_controllable.md` (giả thuyết cuối §5.5) viết: "TbW xấp xỉ 1 − precision của verifier." Khi caption được render từ G*, tử số của TbW là các node SUPPORTED bị người chấm sai. Đó đúng là FP/(TP+FP) của verifier trên tập node được nói ra.
  - (b) Khái niệm "trích dẫn khớp nguồn nhưng chưa chắc đúng/trung thành" đã có trong văn liệu attribution. Wallat, Heuss, de Rijke, Anand, "Correctness is not Faithfulness in RAG Attributions" (arXiv 2412.18004, ICTIR 2025, xác nhận qua trang TU Delft) tách citation correctness khỏi faithfulness. Thước đo citation precision/recall kiểu ALCE cũng thuộc dòng này. ALCE tôi **chưa mở lại trong phiên này**, nên ghi "Chưa xác minh" chi tiết.
  - (c) GAVEL (arXiv 2606.26923, Gao, Hashimoto, Saito, 25/06/2026, chưa có venue) đã làm verification + explanation + localization (box) trên cặp ảnh–caption, có tập train người gán. "Có trạng thái kiểm chứng" là khác biệt của hệ, không phải của metric.
  - (d) TBW chỉ định nghĩa được cho hệ có thẻ trace. Mọi baseline ở mục 5 (zero-shot, GRPO phẳng, RAG) không có giá trị TBW, nên metric không xếp hạng được hệ.
- **Sửa:**
  - Xóa TBW khỏi danh sách "Bộ độ đo mới". Chuyển xuống mục truy vết như **chỉ số chẩn đoán**, kèm câu: "TBW = precision người của các node được trích; khi caption render từ G* thì TBW ≈ 1 − precision verifier (đo trên 244 + 200 mục)."
  - Trích Wallat et al. (ICTIR 2025) và GAVEL.
  - Nếu muốn giữ một metric so được giữa các hệ, dùng **attribution hậu nghiệm** cho mọi hệ (baseline 3 của file 19: parse caption → khớp G → người chấm) và đặt tên theo văn liệu ("attributed-claim precision"), không đặt tên mới.

### F3. M6 NVL tự phục vụ và trùng một phần với nhãn "unknown" — **MAJOR**

- **Plan ghi (bảng M6 + mục 2 "Mô-đun văn hóa"):** "Tỷ lệ fact KG không thể thấy trong ảnh lọt vào caption | NES: đo copy entity, không đo fact phi thị giác." Mục 2 cũng ghi: "fact KG không nhìn thấy được bị chặn khỏi caption."
- **Bằng chứng:**
  - (a) **Theo cấu tạo:** ViHG-Cap lọc fact phi thị giác trước khi sinh, nên NVL của nó ≈ 0 bất kể chất lượng. Các baseline KG-in-prompt (AKGMA-style) và RAVENEA-style RAG lại được *thiết kế* để đưa tri thức vào. Đây là metric đo đúng cái mình chặn, đúng kiểu "vòng lặp tự phục vụ" mà plan đã cảnh báo cho M1.
  - (b) HalDec-Bench (arXiv 2511.20515, preprint; tôi đã đọc HTML) gán nhãn câu correct / incorrect / **unknown**. Nhãn unknown dùng cho "non-visible attributes such as smell or wind", kế thừa sơ đồ của Gunjal et al. (AAAI 2024). Ý tưởng "nội dung không kiểm chứng được bằng mắt là một lớp riêng" đã có. Khác biệt duy nhất là HalDec *loại* lớp này khỏi đánh giá, còn NVL *đếm* nó.
  - (c) NES (arXiv 2511.08909; trang arXiv không ghi venue, "AAAI 2026" mới chỉ thấy qua snippet OJS, **chưa xác minh**) định nghĩa "negative entity" là *object* có trong caption mà không có trong ảnh. Như vậy câu "NES đo copy entity" đúng một nửa: NES là triệt, nó không đề xuất metric (abstract không định nghĩa metric).
  - (d) Bài toán caption văn hóa/sự kiện coi fact phi thị giác là *mục tiêu*: RAVENEA (cIC), "Beyond Vision" (arXiv 2512.20042, EVENTA @ ACM MM'25) nói thẳng là bổ sung "non-visual context such as event background". NVL sẽ phạt đúng thứ các baseline đó được tối ưu cho. Reviewer sẽ nói so sánh không công bằng.
  - (e) Định nghĩa phụ thuộc vào việc mỗi fact KG đã được gắn cờ visual/non-visual. Plan chưa có quy trình gắn cờ và cũng chưa có IAA cho cờ này.
- **Sửa:**
  - Đổi M6 thành **UCR (Unverifiable-Content Rate)**: tỷ lệ mệnh đề (do parser tách) mà người gán nhãn "không kiểm chứng được từ ảnh". Áp cho **mọi hệ**, không chỉ fact KG. Nhãn 3 lớp theo HalDec/M-HalDetect.
  - Báo UCR tách theo nguồn (KG / tham số mô hình) chỉ cho các hệ có KG.
  - Khai báo rõ đây là metric cho chế độ "mô tả theo mắt thấy" (literal description). Không dùng UCR để so với RAVENEA hay cIC trừ khi cùng chế độ prompt.
  - Trích HalDec-Bench và Gunjal et al. Nếu không làm được nhãn người cho UCR thì **bỏ M6**.

### F4. M4 CulR/CulOA là CHAIR/recall giới hạn từ vựng, và "over-attribution" đã có tiền lệ — **MAJOR**

- **Plan ghi (bảng M4):** "Recall thực thể văn hóa và tỷ lệ gán văn hóa quá đà | CulturalVQA/RAVENEA: không có Việt Nam, không caption."
- **Bằng chứng:**
  - (a) Về toán học: CulR = recall object trên lexicon văn hóa; CulOA = CHAIR_i trên cùng lexicon. Phần "confusable" (nón lá → mũ là lỗi nhẹ) chính là H-R của M3 áp lên node văn hóa. Như vậy M4 không phải metric mới mà là **một lát cắt** của M1 + M3 + CHAIR-vi.
  - (b) M²CQA / CFHR (Mousi et al., arXiv 2602.05437, v2 21/04/2026; trang arXiv **không ghi venue**, nên "Findings ACL 2026" trong file 04/09 **chưa xác minh**) đo việc chấp nhận diễn giải "hợp văn hóa nhưng sai thị giác", có điều kiện trên việc trả lời đúng mệnh đề thật. Đây là tiền lệ trực tiếp của "gán văn hóa quá đà", tuy ở dạng phát biểu đúng/sai và cho khu vực MENA.
  - (c) Metric caption văn hóa đã có: MosAIC (NAACL 2025, 2025.naacl-long.152, "culture-adaptable metric") và Cultural Awareness Score (arXiv 2405.17475, preprint). Trang abstract của cả hai **không nói** có phạt gán sai hay không, nên chưa kết luận được là trùng hẳn. Cần đọc PDF trước khi viết "chưa ai phạt gán thừa".
  - (d) VietMEAgent (FAIR 2025, arXiv 2511.09058) có metric "Cultural Accuracy" trên dữ liệu văn hóa Việt. Bài cùng hội nghị, nên phải nêu trong bảng "gần nhất" của M4. Plan hiện chỉ nêu CulturalVQA/RAVENEA. Ngoài ra, cột "gần nhất" gọi RAVENEA là "không caption" là sai, vì RAVENEA có tác vụ cIC.
  - (e) Gold 65 ảnh (plan tự ghi "cần CI"). Với ~65 ảnh, khoảng tin cậy bootstrap của mức chênh 58,8 → 16–23 điểm vẫn có thể có ý nghĩa, nhưng CulOA cần **ảnh bẫy không có thực thể văn hóa**, và plan chưa có tập này.
  - Re-search "Vietnamese cultural image captioning dataset 2025–2026": chỉ ra KTVIC, UIT-OpenViIC, ViTextCaps và VietFashion (retrieval). Không có bộ caption văn hóa tiếng Việt nào, nên khoảng trống dữ liệu vẫn còn.
- **Sửa:**
  - Bảng M4, cột "Gần nhất" → "M²CQA/CFHR (gán văn hóa phản thực, dạng phát biểu, MENA); MosAIC, CAS (metric caption văn hóa, tiếng Anh); VietMEAgent Cultural Accuracy (VQA tiếng Việt, FAIR'25)".
  - Định vị lại: "M4 là lát cắt văn hóa của M1/M3 + CHAIR-vi, kèm tập bẫy". Không gọi là metric mới.
  - Thêm vào mục 4: **tập văn hóa ≥300 ảnh có thực thể + ≥150 ảnh bẫy** (ảnh đời sống Việt không có áo dài, nón lá, …). Gán cùng đợt pilot gold.
  - Thêm CFHR-vi (phát biểu thật/phản thực cho 150 ảnh) làm thước đo phụ, để có điểm nối trực tiếp với M²CQA.

### F5. Pilot gold SG bị neo vào chính pipeline đang được đánh giá — **MAJOR**

- **Plan ghi (mục 4 và mục 8 tháng 11):** "Pilot gold SG 500 ảnh (máy gợi ý → người sửa)". File 16 dùng gán trước bằng `qwen25vl7b|owlv2`.
- **Bằng chứng:**
  - Máy gợi ý chính là họ mô hình sinh G* (Qwen2.5-VL-7B, mục 2A). Gold bị neo về đề xuất của Qwen sẽ thưởng cho ViHG-Cap/VSPS trên M1/M2.
  - File 16 §9 tự liệt kê nghiên cứu anchoring (Choi et al., EMNLP 2024: mức đồng ý 43,9% → 71,5%), nhưng nguồn này **chưa mở bài gốc**.
  - Plan chỉ chống vòng lặp ở meta-eval ("bỏ caption VSPS"), không chống ở gold.
- **Sửa:** thêm vào dòng "Gold scene graph" ở mục 4:
  - "(i) 100/500 ảnh gán **từ đầu, không gợi ý**, để đo độ lệch neo (F1 triple giữa gold-có-gợi-ý và gold-trắng).
  - (ii) Gợi ý bằng mô hình **khác họ** với G* (ví dụ InternVL3.5-8B + OWLv2), không dùng Qwen2.5-VL.
  - (iii) Báo M1 cho mọi hệ trên cả hai phần."

### F6. Benchmark trên KTVIC không phát hành được ảnh; claim "đầu tiên có định vị" trong file 16 sai — **MAJOR**

- **Plan ghi:** pilot 500 ảnh KTVIC test; P1 là "Benchmark … gold SG tiếng Việt 500 ảnh". Phát hành CC BY-NC-SA, "xin phép tác giả".
- **Bằng chứng:**
  - (a) KTVIC không có LICENSE (file 16 §7, mục 4 của plan). Ảnh phát qua Google Drive, link EVJVQA gốc đã gỡ. Nếu tác giả không đồng ý thì benchmark không tái lập được.
  - (b) VietSGG (README GitHub `Moobbot/VietSGG`: "A Benchmark Dataset and Baseline Models for Vietnamese Scene Graph Generation", GOODTECHS 2025 "accepted", CC BY 4.0; ResearchGate có bản ghi cùng tên; **DOI và proceedings chưa xác minh**) đã có box và quan hệ tiếng Việt. Vì vậy câu "bộ scene graph đầu tiên có định vị trên ảnh tiếng Việt" ở `16_vn_sg_dataset.md` §8 là **sai**. Plan mục 1 đã cấm claim "benchmark SG tiếng Việt đầu tiên", nhưng P1 vẫn có thể kéo câu sai từ file 16 vào.
  - Re-search "Vietnamese scene graph / visual relationship dataset" ngoài VietSGG: không thấy bộ nào khác.
  - Bài TNU JST (ĐH Sư phạm TP.HCM, 2025) kết hợp SG + KG ngoài cho captioning nhưng trên MSCOCO/VG, không phải dữ liệu tiếng Việt. Bài này **chưa mở toàn văn**.
- **Sửa:**
  - Chia pilot thành 400 ảnh KTVIC + **100 ảnh có license mở** (UIT-ViIC/COCO hoặc XM3600, CC BY), để luôn có một phần phát hành trọn vẹn.
  - Ghi vào P1 câu khác biệt so với VietSGG: "gold do người kiểm, 3 trạng thái, caption chi tiết, ảnh đời sống; VietSGG là nhãn bán tự động GDINO+GPT-4 trên ảnh thể thao COCO."
  - Sửa câu "đầu tiên có định vị" trong file 16 (hoặc gắn cờ không dùng).

### F7. Parser thiếu baseline AMR và bộ test chi tiết không có nguồn người viết — **MAJOR**

- **Plan ghi (mục 3, parser):** baseline "dịch sang Anh → FACTUAL/DiscoSG". Gold "650 test (500 ngắn, 150 chi tiết)".
- **Bằng chứng:**
  - (a) VLSP 2025 viSemParse (AMR tiếng Việt, 2.500 câu, top-1 Smatch 58%). Đã xác nhận qua bài tổng quan của BTC trên VNU JCSCE (Ha My Linh, Pham Thi Duc, Le Ngoc Toan, Nguyen Thi Minh Huyen) và qua các bài đội thi trên ACL Anthology (2025.vlsp-1.30/.32, trong đó có hệ BARTpho/ViT5 của UIT với Smatch 0,37).
  - (b) Đường AMR → scene graph đã có tiền lệ: SGRAM / "Scene Graph Parsing via AMR in Pre-trained LMs" (Choi, Heo, Punithan, Zhang, DLG4NLP@NAACL 2022, 2022.dlg4nlp-1.4; arXiv 2210.08675). Reviewer biết VLSP sẽ hỏi vì sao không dùng đường native có sẵn này.
  - (c) Caption chi tiết tiếng Việt do người viết **không tồn tại** (file 03: chỉ có bản dịch máy ShareGPT4V). Nếu 150 caption chi tiết là output VSPS/Qwen thì parser được test trên phân phối của chính hệ mình.
  - Re-search "Vietnamese text-to-scene-graph / Vietnamese SPICE": vẫn âm tính. Không có task VLSP 2026 nào về đề tài này (không tìm thấy danh sách task 2026).
- **Sửa:**
  - Thêm baseline thứ hai vào luật T3: "viSemParse-style AMR parser (Qwen3-1.7B SFT trên ngữ liệu VLSP, nếu license cho phép) → chuyển AMR → SG theo SGRAM". Luật dừng thành: "parser native phải hơn **cả hai** baseline ≥3 F1".
  - Ghi rõ nguồn của 150 caption chi tiết: lấy từ ≥3 hệ, trong đó ≥1 hệ không thuộc VSPS, cộng 50 caption do người viết mới.

### F8. NES và M²CQA đang được dẫn kèm venue chưa xác minh — **MINOR**

- **Bằng chứng:** trang arXiv của 2511.08909 (NES) và 2602.05437 (M²CQA) **không ghi venue**. "AAAI'26" và "Findings ACL 2026" chỉ đến từ snippet hoặc file khác.
- **Sửa:** trong plan, ghi "NES (arXiv 2511.08909)" và "M²CQA (arXiv 2602.05437)" cho đến khi đối chiếu được với proceedings.

### F9. Bảng M6 mô tả NES chưa đúng — **MINOR**

- **Bằng chứng:** NES định nghĩa "negative entities — objects that appear in generated caption but are absent from the input" và *triệt* chúng. Abstract không đề xuất metric nào.
- **Sửa:** "NES: triệt object truy hồi không có trong ảnh (không phải metric, không xét fact phi thị giác); HalDec-Bench: nhãn 'unknown' cho nội dung không thấy được nhưng loại khỏi đánh giá."

### F10. Rò rỉ giữa train và test của parser qua ảnh gần trùng KTVIC/OpenViIC — **MINOR**

- **Bằng chứng:** plan mục 4 ghi 401/558 ảnh KTVIC test gần trùng UIT-OpenViIC train. Parser silver sinh trên caption KTVIC, UIT-ViIC và OpenViIC (file 08), còn gold test lại lấy từ KTVIC test.
- **Sửa:** test của parser chỉ lấy từ tập 157 ảnh sạch cộng ảnh ngoài miền. Loại các ảnh gần trùng khỏi silver train.

### F11. Ngưỡng IAA mệnh đề κ ≥ 0,7 dùng cho cả nhãn 3 lớp — **MINOR**

- **Bằng chứng:** với nhãn correct / incorrect / unknown, lớp unknown thường hiếm và khó đạt đồng thuận. Chính HalDec-Bench nói "having a unified consensus on this criterion is difficult" và chọn loại lớp này.
- **Sửa:** báo κ riêng cho cặp (correct vs incorrect) và cho cờ unknown. Đặt ngưỡng cho cờ unknown là α ≥ 0,6. Nếu không đạt thì gộp unknown vào "không chấm".

---

## 3. Plan đã làm đúng (ngắn)

- Đã chủ động cấm các claim "SG tiếng Việt đầu tiên", "đầu tiên về KG-captioning" và "đảm bảo trung thực".
- Luật dừng cho parser (T3, so với dịch-rồi-parse) và cổng T4 cho M1 so với VLM-judge là kiểu cổng đúng.
- Đã nhận diện rủi ro vòng lặp tự phục vụ ở meta-eval (bỏ caption VSPS, tách ảnh parser). Cần mở rộng cùng nguyên tắc sang gold SG (F5) và M6 (F3).
- Re-search của vòng này xác nhận một số khoảng trống là thật:
  - chưa có parser text → SG tiếng Việt;
  - chưa có bộ SG tiếng Việt do người kiểm ngoài VietSGG bán tự động;
  - chưa có benchmark ảo giác đa phương thức tiếng Việt (ViHallu chỉ là văn bản);
  - chưa có bộ caption văn hóa tiếng Việt;
  - chưa có bộ phán xét người tiếng Việt được *phát hành*.

---

### Nguồn đã mở trong phiên này

- Crossmodal-3600 PDF: arxiv.org/pdf/2205.12522 (mục Human Evaluation, chú thích L_EXT, Limitations)
- HalDec-Bench HTML: arxiv.org/html/2511.20515
- NES: arxiv.org/abs/2511.08909
- M²CQA: arxiv.org/abs/2602.05437
- MosAIC: aclanthology.org/2025.naacl-long.152
- CAS: arxiv.org/abs/2405.17475
- Beyond Vision: arxiv.org/abs/2512.20042
- KnowHal: arxiv.org/abs/2608.03782 (QA, không phải caption)
- Wallat et al.: arxiv 2412.18004 + research.tudelft.nl (ICTIR 2025)
- VietSGG: github.com/Moobbot/VietSGG
- UIT-OpenViIC, KTVIC, UIT-ViIC PDF (grep chấm người: âm tính)
- ViTextCaps HTML: arxiv.org/html/2604.27712 (đọc 100k ký tự đầu)
- viSemParse: jcsce.vnu.edu.vn/index.php/jcsce/article/view/6493, aclanthology 2025.vlsp-1.32
- SGRAM: aclanthology 2022.dlg4nlp-1.4
- GAVEL: arxiv 2606.26923 (abstract qua kết quả tìm kiếm)

**Chưa xác minh:**
- venue của NES và M²CQA;
- DOI của VietSGG;
- cơ chế phạt của MosAIC metric và CAS;
- ALCE citation precision (chưa mở lại);
- toàn văn bài TNU JST.
