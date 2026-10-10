# R3-03: Khả thi của kế hoạch v2 (GPU 1× RTX 3090, code repo, giờ công, lộ trình, bản quyền, dedup)

Critic 03, vòng 3, 2026-10-10. Trục: **khả thi**. Tôi tự đánh giá `00_KE_HOACH.md` (v2) trước, đối chiếu code thật trong `rescap/`, `scripts/`, `configs/`, `data/`, rồi mới mở R2-05 và R2-06 để xem v2 đã sửa đúng chưa. Máy này không có GPU (không có `nvidia-smi`), nên mọi số GPU dưới đây là **(đo)** khi có file trong repo, **(code)** khi đọc từ mã nguồn, và **(ước tính)** trong các trường hợp còn lại.

Nguồn đã mở trong phiên này:
- XM3600: arXiv 2205.12522 (EMNLP 2022, toàn văn PDF) và trang `google.github.io/crossmodal-3600`.
- Open Images v7: trang facts & figures, phần license.
- HALVA: arXiv 2405.18654 (abs + HTML, ICLR 2025).
- RLAIF-V-7B: HF `openbmb/RLAIF-V-7B`.
- CLC: arXiv 2502.19110, NeurIPS 2025 (trang papers.neurips.cc).
- UIT-OpenViIC: arXiv 2305.04166v2 (HTML).
- SSCD: GitHub `facebookresearch/sscd-copy-detection`.
- License từ HF API: Qwen2.5-VL-3B, Qwen2.5-VL-7B, Vintern-1B-v3_5. Thêm thẻ HF của InternVL2_5-1B và Florence-2-large.

---

## 1. Kết luận theo từng thành phần

| Thành phần v2 | Kết luận | Lý do ngắn |
|---|---|---|
| T-dedup tuần 1 (SSCD all-vs-all, <2 GPU-h) | **pass, có điều kiện** | GPU thật sự chỉ < 1 h cho khoảng 25k ảnh. Code SSCD MIT, chạy bằng torchscript. Điểm nghẽn là **tải dữ liệu**: repo chưa có OpenViIC, UIT-ViIC hay XM3600, và chưa có dòng code nào cho SSCD. |
| Ngân sách GPU §8 ("~515–760, KTVIC/OpenViIC sạch") | **needs-fix** | Con số chép từ R2-05, mà R2-05 là đường **chỉ KTVIC** và có cả GRPO, G1, Qwen3-VL, R1-SGG (v2 đã bỏ). Ngược lại, nó **thiếu** mọi baseline mới. Tính lại ở §3 thì MVP còn ≈ 345–570 GPU-h, nhưng có một khoản tăng vọt nếu T0.5 trượt. |
| Baseline mới: viết-lại-CLC, lùi-sau-sinh, SFA cho mọi hệ | **needs-fix** | SFA "cho *mọi* hệ" nghĩa là chạy verifier trên đầu ra của khoảng 12 hệ. Đi đường logit thì tốn 31–63 GPU-h; nếu T0.5 trượt và phải về K=5 thì lên khoảng 150–250 GPU-h. Plan chưa tính khoản này. |
| HALVA, RLAIF-V-7B | **needs-fix** | Cả hai chỉ có checkpoint **tiếng Anh, nền LLaVA-1.5**, nên cần venv thứ ba và một bước dịch máy. Đó là một biến gây nhiễu, không phải baseline tiếng Việt. |
| Backbone Qwen2.5-VL-3B | pass | Cùng class, cùng env. `train_stage2.py` hard-code `MODEL_ID`, chỉ cần thêm `--model-id`. License là **qwen-research**, khác 7B (Apache-2.0). |
| XM3600 100–150 ảnh | **pass, cần sửa câu chữ** | Có tiếng Việt (`vi`). Annotation CC BY 4.0. Ảnh là Open Images, "listed as CC BY 2.0", không phải CC BY 4.0. Giờ công cho phần XM3600 chưa có trong tổng 200 h. |
| 100 ảnh gán từ đầu (anchoring) | **needs-fix** | MVP gốc R2-06 chỉ có 30 ảnh. Lên 100 ảnh thì thêm khoảng 15–19 h mà không được cộng. |
| Giờ công ~200 người gán + ~90 NCS | **fail** | Chép nguyên bảng R2-06 §4.3 (viết cho MVP *trước* v2), không cộng các việc v2 thêm vào. Nhu cầu thật khoảng 290–380 h, rơi dồn vào 01–03/2027, đúng lúc năng lực thấp nhất (thi, Tết). Hệ quả là trượt hạn P1. |
| Công kỹ thuật của NCS (không có trong plan) | **needs-fix** | Khoảng 38–50 ngày công trước G-P2, nhưng plan không ghi ở đâu. "NCS 90 h" chỉ là phần gán nhãn. |
| Cổng T3 (parser hơn 2 baseline) | **needs-fix** | "AMR (viSemParse)→SG": viSemParse là shared task VLSP 2025, **không có parser phát hành**. Muốn có baseline này phải tự train trên 1.750 câu, license chưa rõ. |
| Cổng G-P2 31/01 | **needs-fix** | Phụ thuộc parser (T3, cùng tháng 01) và gold dev 80 ảnh (T2, 12/2026). Với 80 ảnh, CI 95% rất có thể chưa ngã ngũ, mà plan không nói khi đó làm gì. |
| Bản quyền (KTVIC/EVJVQA/OpenViIC, Wikidata) | pass, một sửa nhỏ | Có thư xin phép và phương án "chỉ ID". Thiếu thứ tự gán: đang gán ảnh OpenViIC trước khi biết có được phép. |
| T0.5 (verifier logit) | pass, một sửa nhỏ | "Split audit dev" vẫn là ảnh **test** KTVIC. |
| Lộ trình tổng 10/2026–08/2027 | **needs-fix** | GPU không phải nút thắt. Nút thắt là giờ người trong Q1/2027 và công kỹ thuật trước 31/01. |

**Tổng: 1 BLOCKER, 7 MAJOR, 7 MINOR.**

---

## 2. Phát hiện

### B1 (BLOCKER). Bảng giờ công không được cập nhật cho những gì v2 thêm vào, nên Q1/2027 vượt năng lực và P1 trượt hạn

- **Plan nói** (§8): "Người gán ~200 h, NCS ~90 h (R2-06 §4.3, ước tính, dư ~30%)."
- **Bằng chứng**: bảng R2-06 §4.3 được viết cho MVP *trước* v2. Nó có anchoring 30 ảnh, không có XM3600, không có kiểm 50+50 claim/hệ, và không có chấm "nội dung không kiểm được" cho mọi hệ. Các việc mà v2 thêm vào nhưng không cộng giờ (ước tính, đơn giá lấy từ chính R2-06):

| Việc mới trong v2 | Cách tính | Giờ người gán |
|---|---|---|
| Anchoring 100 ảnh gán từ đầu (§4), thay cho 30 ảnh | 100 × 12–15 phút, trừ khoảng 6 h đã có | +15–19 |
| Meta-eval A trên 100–150 ảnh XM3600 (§3) | 100–150 × 5,3 phút × 2 người | +18–27 |
| Gold SG trên XM3600, cần để tính M1 và τ_c trên phần phát hành được | 100–150 × 6 phút × 1,25 | +13–19 |
| M1: "50+50 claim/hệ người kiểm" (§3) | khoảng 12 hệ × 100 claim × 0,5–1 phút × 1,2 (gán đôi) | +12–24 |
| "Tỷ lệ nội dung không kiểm được do người chấm cho mọi hệ" (§1, thay M6) | 100 ảnh × 8–12 hệ × 2 người × 1–1,5 phút | +27–60 |
| Tập hiệu chỉnh verifier từ ảnh train (xem m5) | 300–500 mệnh đề × 0,5 phút | +3–4 |
| **Cộng thêm** | | **+88–153** |

- **Tổng nhu cầu**: khoảng 290–355 h người gán, so với năng lực 192–320 h trong 02/11/2026–26/03/2027 (2 người × 6–10 h/tuần × khoảng 16 tuần có ích).
- Phân bố theo tháng (ước tính):

| Tháng | Năng lực | Nhu cầu |
|---|---|---|
| 12/2026 | 48–80 h | SG 50 + parse 20 + SG XM3600 13–19 ≈ 83–89 h |
| 01–03/2027 (thi, Tết) | ≈ 96–160 h | meta-eval 88–97 + claim M1 12–24 + "không kiểm được" 27–60 + văn hóa 10 + human eval 23 ≈ 160–214 h |

- **Hệ quả**:
  - Thiếu khoảng 50–100 h, tức khoảng 3–6 tuần của cả 2 người. Meta-eval A và các nhãn để tính M1 xong khoảng 04–05/2027, không phải 03/2027.
  - T4 (02/2027) không đo được đúng hạn, vì τ_c của M1 cần cả meta-eval A lẫn nhãn claim.
  - P1 lên arXiv 04/2027 và nộp ARR khoảng 15/05/2027 sẽ thiếu kết quả.
- **Sửa** (thay §8 và thêm vào §3):
  1. Thêm bảng giờ có cột **theo tháng** và cột năng lực. Mỗi việc mới phải có một dòng.
  2. Cắt phạm vi:
     - "Nội dung không kiểm được" chỉ chấm cho **4 hệ** (zero-shot, VSPS, ViHG-Cap, baseline mạnh nhất) × 100 ảnh × 2 người, khoảng 13–20 h.
     - Kiểm claim M1 chỉ cho **seed 42 của 6 hệ**, khoảng 6–12 h.
     - Meta-eval A còn 300 ảnh ViSG + 100 ảnh XM3600, khoảng 71 h. Gold SG XM3600 chỉ làm trên 100 ảnh.
  3. Đẩy phần **XM3600 của meta-eval A** lên 20/11–20/12, ngay sau khi đóng băng ứng viên 15/11 và trước gán SG chính. Tháng 01 chỉ còn phần ViSG.
  4. Ghi câu: "Nếu đến 28/02/2027 meta-eval A chưa xong ≥ 80%, P1 nhắm ARR đợt kế tiếp (kiểm hạn), không nộp thiếu."

### M1 (MAJOR). §8: ngân sách GPU lấy nhầm phạm vi, thừa việc đã bỏ, thiếu việc mới

- **Plan nói**: "GPU nhánh KTVIC/OpenViIC sạch: ~515–760 GPU-h (R2-05) … nghiêng về cận dưới (~4 tuần máy)."
- **Bằng chứng**:
  - R2-05 §3 ghi rõ "đường **chỉ KTVIC**" (4.327 ảnh). Trong đó có E3 GRPO 65–100, G1 22–24, Qwen3-VL-8B 36–42 và front-end R1-SGG/REACT++ 13–26, đều đã bị v2 bỏ.
  - Không có dòng nào cho viết-lại-CLC, lùi-sau-sinh, SFA, HALVA, RLAIF-V, 3B, XM3600 hay OpenViIC-test.
  - Đơn giá 3,6 h/SFT **đã là** đơn giá của bảng R2-05 (R2-05 §3: "coi là 3090"). "Nghiêng về cận dưới vì 3,6 h đo trên 3090" vì vậy là đếm hai lần.
  - Repo **không có log** cho con số 3 h 35 m: grep `train_runtime`, `3h35`, `1800/1800` không ra gì. `data/supervision_v2/README.md` chỉ ghi kết quả eval "RTX 3090" (7.206 dòng, 2 epoch, grad-accum 8, nên ≈ 1.800 bước, khớp).
  - Mọi `latency_*.json` đều ghi `"gpu": "NVIDIA GeForce RTX 4090"` (đo).
- **Sửa**: thay §8 bằng bảng ở §3 dưới đây. Commit `trainer_state.json` của run v2raw_s42 vào `data/results/` để con số 3,6 h có chứng cứ.

### M2 (MAJOR). SFA "áp một phép lùi sau sinh chung cho mọi hệ" là khoản GPU lớn nhất mà plan chưa tính, và nó phình ×4–5 nếu T0.5 trượt

- **Plan nói** (§3): "áp **một phép lùi sau sinh chung** k = 0..3 mức cho *mọi* hệ."
- **Bằng chứng**:
  - Lùi sau sinh cần nhãn SUPPORTED/UNCERTAIN cho từng claim của từng caption, tức là phải chạy verifier trên đầu ra của mỗi hệ. Còn k = 0..3 thì chỉ là CPU.
  - Caption zero-shot dài 117 từ, ứng với 4,26 claim bịa mỗi caption (đo, `supervision_v2/README.md`).
  - Đường logit: khoảng 12 hệ × 550 ảnh (ViSG-test + XM3600) × 15–30 s ≈ **27–55 GPU-h** (ước tính).
  - Nếu T0.5 trượt thì K=5 tốn khoảng 80 s × 1,3 cho mỗi ảnh (R2-05 F1), tức khoảng **150–250 GPU-h**. Cộng thêm verify lại train khoảng 110 GPU-h, tổng MVP lên **≈ 650–900 GPU-h**.
  - Nhánh "nếu trượt" của T0.5 hiện chỉ ghi "thu hẹp phạm vi dựng đồ thị", không nhắc tới SFA.
- **Sửa**:
  1. §3 đổi "cho *mọi* hệ" thành: "cho 6 hệ seed 42 (zero-shot 7B, SFT-không-kiểm-chứng, VSPS, viết-lại-CLC, ViHG-Cap, GEPA) trên ViSG-test."
  2. Cổng T0.5, cột "Nếu trượt", thêm: "SFA chỉ trên 4 hệ và 320 ảnh test; lùi-sau-sinh chỉ trên zero-shot."

### M3 (MAJOR). HALVA và RLAIF-V-7B không phải baseline tiếng Việt chạy được trong env hiện tại

- **Plan nói** (§2): baseline bắt buộc có "HALVA; RLAIF-V-7B".
- **Bằng chứng**:
  - HALVA (arXiv 2405.18654, ICLR 2025): base là LLaVA-v1.5 7B/13B và VILA-v1.5 13B. Dữ liệu là khoảng 21,5k cặp đúng/bịa (câu trả lời đúng do Gemini Vision Pro tạo). Huấn luyện trên 4×A100-80GB, khoảng 1,5–3 h.
  - RLAIF-V-7B (HF): base là llava-v1.5-7B, ngôn ngữ ghi trên thẻ là English.
  - Dùng hai checkpoint này cho caption tiếng Việt có hai đường:
    - (a) prompt tiếng Việt cho Vicuna-7B: chất lượng tiếng Việt kém, so sánh không công bằng;
    - (b) caption tiếng Anh rồi dịch máy: lỗi dịch lẫn vào M1/CHAIR-vi.
  - Cả hai đường đều cần venv thứ ba cho LLaVA (repo gốc pin transformers đời cũ, **chưa xác minh** bản cụ thể), trong khi `requirements.txt` bắt buộc pin 4.51.3.
  - Chính plan đã ghi loss của GEPA là "HALVA/DPA mức cụm" (§1).
- **Sửa** (§2, dòng baseline):
  > "**DPA-vi** (tái hiện loss HALVA trên Qwen2.5-VL-7B, cùng code GEPA, negative do LLM sinh bằng tăng cường mức cụm thay vì từ node REJECTED), 3 seed. Đây là đối chứng trực tiếp cho claim 'nguồn negative từ đồ thị kiểm chứng'. HALVA-7B và RLAIF-V-7B gốc chỉ báo trong bảng phụ 'EN→VI, tham khảo', 1 lượt, trên KTVIC-test-clean; nếu venv LLaVA tốn > 1 ngày công thì bỏ."

  Chi phí của DPA-vi là sinh dữ liệu khoảng 6 GPU-h, cộng 3 × 6–10 h huấn luyện.

### M4 (MAJOR). Công kỹ thuật của NCS trước G-P2 (31/01) không có trong plan, và ước tính khoảng 38–50 ngày công

- **Plan nói**: "NCS ~90 h". Đây chỉ là phần hướng dẫn, phân xử và KG, lấy từ R2-06 §4.3.
- **Bằng chứng** (code):
  - Repo hiện **chưa có**:
    - loader OpenViIC hay XM3600: `scripts/evaluate.py` chỉ gọi `references(args.split)` của KTVIC; `data/datasets/` chỉ có `ktvic`, `karpathy`, `coco_probe`;
    - code SSCD;
    - `--model-id` trong `train_stage2.py` (L41 hard-code `MODEL_ID`, L119 hard-code `Qwen2_5_VLForConditionalGeneration`);
    - verifier logit (`vintern.py` vẫn `supports_logprobs = False`, theo R2-05 F6);
    - `detect_boxes.py`, `build_graph_sft.py`, parser, `metrics_graph.py`, GEPA;
    - baseline CLC, lùi-sau-sinh, DoLa (`baselines.py` chỉ có `selfcorrect`/`vcd`).
  - Ước tính ngày công (theo R2-05 §4, bỏ các bước đã cắt, cộng các bước v2 thêm):

| Nhóm việc | Ngày công |
|---|---|
| Kiểm máy, verifier logit, cổng cấu trúc, box, IsA/KG, dựng G*, sửa eval | 12–15 |
| Parser và M1–M4 | 5–7 |
| GEPA | 2 |
| Dedup + loader OpenViIC/XM3600 | 2 |
| CLC | 1–2 |
| Lùi-sau-sinh và đường SFA | 2–3 |
| DPA-vi | 2–3 |
| GRIT (env riêng, op CUDA deformable, train lại) | 2–3 |
| `--model-id` cho 3B | 0,5–1 |
| Parser baseline (dịch→FACTUAL; xem M5) | 2–4 |
| P0 (§7) | 5–8 |
| **Cộng** | **≈ 38–50 ngày công, khoảng 300–400 h** |

  - Từ 10/10/2026 đến 31/01/2027 có khoảng 16 tuần. Trừ 90 h gán nhãn thì gần như **không còn dư** để viết P1 trước 04/2027.
- **Sửa**:
  1. Thêm vào §8 một dòng "Công kỹ thuật NCS: ~300–400 h đến 31/01" và một cột "NCS-kỹ thuật" vào bảng lộ trình §9.
  2. Cắt khỏi MVP: GRIT (chỉ trích số leaderboard, ghi rõ là không cùng test sạch), DoLa (giữ VCD, vì code đã có), HALVA/RLAIF-V gốc (xem M3).
  3. Thứ tự bắt buộc trước 31/01: dedup → verifier logit → G* → E1 + 3 baseline cho G-P2 (SFT-không-kiểm-chứng, CLC, caption-only). Mọi baseline khác dời sang 02–03/2027.

### M5 (MAJOR). Cổng T3: baseline "AMR (viSemParse)→SG" không có công cụ để chạy

- **Plan nói** (§1): "luật +3 F1 so với **2 baseline**: dịch→FACTUAL và AMR (viSemParse)→SG."
- **Bằng chứng**:
  - Theo file 08 dòng 20–21, VLSP 2025 viSemParse là shared task và ngữ liệu (2.500 câu: train 1.750 / public 150 / private 1.200). Smatch tốt nhất là 0,58. Không có parser phát hành.
  - Bản HF `MochiVN/ViAMR-v1.0` là dữ liệu của bên thứ ba, "chưa kiểm license".
  - Muốn có baseline này phải tự train parser AMR, rồi viết luật AMR→SG. Ước tính 3–5 ngày công, cộng 2–5 GPU-h (file 08 dòng 63), đúng tháng 01/2027 khi T3 và G-P2 trùng nhau.
- **Sửa**: thay "AMR (viSemParse)→SG" bằng "**Qwen2.5-7B-Instruct few-shot → JSON SG**" (0 huấn luyện, khoảng 1–2 GPU-h). AMR chỉ để lại trong phần thảo luận, kèm câu "Chưa xác minh license dữ liệu".

### M6 (MAJOR). G-P2 31/01 phụ thuộc hai việc cùng tháng và có thể chưa ngã ngũ

- **Plan nói**: "G-P2 31/01/2027: E1 hơn SFT-không-kiểm-chứng trên M1-P (dev, CI 95%) **và** không thua viết-lại-CLC."
- **Bằng chứng**:
  - M1-P cần parse caption sinh ra thành claim, nên cần parser. Mà T3 (parser) cũng rơi vào 01/2027.
  - Dev chỉ có 80 ảnh, khoảng 80 × 5–8 claim. Đo được trên chính repo: v2raw và VSPS chênh nhau −3,4 điểm precision object trên 558 ảnh, 1 seed. Ở cỡ chênh này, CI 95% trên 80 ảnh rất có thể cắt qua 0 (ước tính).
  - Plan không nói khi CI chưa ngã ngũ thì làm gì.
- **Sửa** (§5, dòng G-P2):
  > "Đo bằng parser bạc (xong 12/2026), không chờ T3. Bootstrap theo ảnh trên dev 80 + KTVIC-test-clean 157 (object-level P, không cần gold SG). Nếu CI cắt 0: coi là **trượt** (P2 → IP&M/TOMM), không gia hạn."

### M7 (MAJOR). Dedup tuần 1: GPU thì rẻ, nhưng dữ liệu và code chưa có

- **Plan nói**: "Tuần 1: dedup all-vs-all (SSCD, <2 GPU-h)."
- **Bằng chứng**:
  - SSCD (GitHub, MIT) chạy bằng torchscript `sscd_disc_mixup.torchscript.pt`, resize cạnh ngắn 288, vector 512 chiều. Khoảng 25k ảnh (KTVIC 4.327 + OpenViIC 13.100 + UIT-ViIC + XM3600 3.600) chạy dưới 1 GPU-h (ước tính). So all-vs-all 25k² bằng tích ma trận thì không đáng kể.
  - Repo **chưa có** ảnh OpenViIC (13.100 ảnh: train 9.088 / val 2.011 / test 2.001, theo 2305.04166v2), UIT-ViIC hay XM3600. Phải tải ba bộ trong tuần 1, song song với P0, thư xin phép, hướng dẫn v0.1 và caption 4 ứng viên. Đây đúng là chỗ R2-06 M6 đã cảnh báo tháng 10 quá tải.
  - Ngưỡng 0,8 lấy theo ViCLIP-OT. Plan không có bước kiểm tay biên ngưỡng.
- **Sửa**:
  1. §9 tháng 10 ghi: "T-dedup hạn **24/10** (không phải tuần 1). Trước hết là KTVIC train↔test (dữ liệu đã có, phục vụ P0), sau đó mới tới OpenViIC/XM3600."
  2. Kiểm tay 50 cặp ở dải 0,7–0,85, khoảng 1 h NCS, rồi báo ngưỡng.
  3. Phát hành danh sách cụm trùng cùng P0.

### m1 (MINOR). XM3600: có tiếng Việt, nhưng license ảnh và "nối với nghiên cứu người VN" bị viết sai

- **Bằng chứng** (2205.12522, toàn văn):
  - 36 ngôn ngữ, có "Vietnamese (vi)". Mỗi ngôn ngữ có 100 ảnh chụp ở vùng nói ngôn ngữ đó. Mỗi ảnh có khoảng 2 caption cho **mỗi** ngôn ngữ (261.375 caption). Caption `vi` dài trung bình khoảng 18 từ.
  - "released XM3600 under a CC-BY4.0 license". Đây là license của annotation.
  - Ảnh lấy từ Open Images. Trang Open Images ghi: "images are listed as having a CC BY 2.0 license", đồng thời từ chối bảo đảm, phải "verify the license for each image yourself".
  - Đánh giá người: chỉ có so sánh cặp side-by-side (thang 7 mức, 3 người) trên XM600, ở **cấp hệ**. `vi` nằm trong nhóm L_EXT. Trang tải không có file rating nào.
- **Sửa** (§4, dòng XM3600):
  > "XM3600 `vi`, 100–150 ảnh (ưu tiên 100 ảnh chụp tại VN). Caption CC BY 4.0; ảnh Open Images 'listed as CC BY 2.0', phát hành ID + URL + file attributions gốc, không đóng gói lại ảnh. Nghiên cứu người trước đó chỉ là SxS cấp hệ, không công bố rating, nên chỉ trích, không so số."

### m2 (MINOR). Qwen2.5-VL-3B có license khác 7B

- **Bằng chứng** (HF API): `Qwen/Qwen2.5-VL-3B-Instruct` mang tag `qwen-research`, còn 7B là `license:apache-2.0`.
- **Sửa**: thêm một dòng vào bảng "Bản quyền": "adapter 3B phát hành theo Qwen Research License (phi thương mại); adapter 7B Apache-2.0."

### m3 (MINOR). "Khác họ Qwen" chỉ đúng một nửa

- **Bằng chứng**: Vintern-1B-v3_5 fine-tune từ InternVL2.5-1B, mà thẻ InternVL2_5-1B ghi LLM là **Qwen2.5-0.5B-Instruct**.
- Vì vậy verifier, generator (Qwen2.5-VL) và 3/4 ứng viên meta-eval cùng có LLM gốc Qwen2.5. Câu "máy gợi ý bằng OWLv2/Florence-2 + họ mô hình khác Qwen" (§4) chưa nêu tên mô hình gợi ý quan hệ.
- **Sửa** (§4):
  > "Gợi ý object: OWLv2 (native trong 4.51.3). Gợi ý quan hệ: không dùng VLM (annotator tự thêm), hoặc nêu tên mô hình cụ thể và họ LLM của nó."
- Florence-2 cần `trust_remote_code` (thẻ HF). Việc nó tương thích với transformers 4.51.3 **chưa xác minh**, nên bỏ khỏi MVP.

### m4 (MINOR). Gán OpenViIC trước khi biết có được phép

- **Bằng chứng**: §9 cho bắt đầu gán SG từ 11/2026, trong khi hạn giấy phép là 30/11. ~243/400 ảnh ViSG-test là OpenViIC.
- **Sửa**: "Thứ tự gán: 157 KTVIC-clean → XM3600 → OpenViIC (chỉ sau 30/11, hoặc sau khi có phản hồi)."

### m5 (MINOR). T0.5 "đo trên split audit dev" vẫn là ảnh test KTVIC

- **Bằng chứng**: R2-05 F6 cho biết 244 mục audit lấy từ ảnh test (bản ghi Untrained-VSPS).
- **Sửa**: "hiệu chỉnh trên 300–500 mệnh đề từ **ảnh train** (gán bằng `scripts/annotate.py`, ~3–4 h); 244 mục audit chỉ để báo."

### m6 (MINOR). Còn sót chữ từ v1

- **Bằng chứng**: §2 ghi "Sửa lỗi `qwen_vl.py` … trước khi dùng R1-SGG", nhưng pipeline (A) của v2 không còn R1-SGG.
- Lỗi này (`qwen_vl.py` L66–69 luôn chọn class 2.5) **không** ảnh hưởng 3B, vì 3B vẫn là Qwen2.5.
- **Sửa**: chuyển câu này sang "bản mở rộng".

### m7 (MINOR). CLC: rewriter chính thức là tiếng Anh

- **Bằng chứng**: CLC (Jiang, Liu, Van Durme, NeurIPS 2025, 2502.19110) phát hành rewriter và dữ liệu cho QA tiếng Anh (SimpleQA, NQ).
- **Sửa**: ghi "viết-lại-**kiểu**-CLC bằng prompt Qwen2.5-7B (không dùng rewriter gốc, không có bảo đảm conformal)".
- Chi phí: viết lại khoảng 7,2k mục tiêu × 2–4 s ≈ 4–8 GPU-h, cộng 3 SFT.

---

## 3. Ngân sách GPU tính lại cho MVP v2 (1× RTX 3090)

Đơn giá:
- SFT caption 7B: 3,6 h/run (đo, chưa có log trong repo).
- SFT graph-then-caption: ×1,5–1,7, tức 5,4–6,1 h.
- 3B ≈ 0,45 × 7B.
- Eval trên khoảng 950 ảnh (ViSG 400 + XM 150 + phần KTVIC-test để báo CIDEr): caption 0,7 h, graph 1,8–2,2 h.
- Verify logit: 10–25 s/ảnh (ước tính, R2-05).

| # | Hạng mục | GPU-h |
|---|---|---|
| 1 | Kiểm máy, benchmark 50 bước, T0.5 | 4–7 |
| 2 | SSCD dedup | 0,5–1 |
| 3 | OWLv2 box (train sạch ≤ 3.769 + test 550) | 1–3 |
| 4 | Stage-1 + gợi ý SG cho 550 ảnh test mới | 15–20 |
| 5 | Verify logit trên train sạch (dùng lại mệnh đề Stage-1) | 10–26 |
| 6 | E1 7B × 3 seed | 16–18 |
| 7 | Caption-only × 3; SFT-không-kiểm-chứng × 3 | 22 |
| 8 | Bảng đối đầu phép lùi (xóa / neutralize, train lại trên train sạch), 1–3 seed | 11–37 |
| 9 | Viết-lại-CLC: viết lại + 3 SFT | 15–26 |
| 10 | Lùi-sau-sinh + SFA (6 hệ, sửa M2) | 15–30 |
| 11 | DPA-vi × 3 (sửa M3) | 24–36 |
| 12 | GEPA × 3 | 12–18 |
| 13 | Qwen2.5-VL-3B: zero-shot, E1 × 3, caption-only × 3, cộng eval | 17–19 |
| 14 | VCD (code có sẵn) | 2–3 |
| 15 | Eval khoảng 35 mô hình | 35–50 |
| 16 | Parser: silver + ViT5 + baseline LLM few-shot | 16–30 |
| 17 | Meta-eval: caption 4 ứng viên + VLM-judge | 9–13 |
| 18 | POPE/AMBER (cần dịch câu hỏi sang tiếng Việt) | 15–20 |
| | **Cộng** | **≈ 240–380** |
| | **+30%** | **≈ 310–495 GPU-h, khoảng 2,5–3,5 tuần máy** |
| | Nếu T0.5 trượt (K=5 cho #5, #10) | **+150–250**, thành ≈ 500–750 |
| | Nếu giữ nguyên v2 (SFA mọi hệ, HALVA/RLAIF-V venv riêng, GRIT) | +40–80 |

Lịch máy:
- Đoạn găng trước G-P2 (dòng 5–7 và 9, cộng eval của chúng) cần khoảng 80–110 GPU-h, tức khoảng 5 ngày máy trong 01/2027. **GPU không phải nút thắt**; nút thắt là B1 và M4.
- Đường 20k ảnh và OpenViIC-train: giữ ngoài MVP. §4 hiện ghi "Train KTVIC/OpenViIC **sạch**" → sửa thành "**Train KTVIC sạch** (OpenViIC chỉ dùng ảnh test)". Lý do: OpenViIC train có 9.088 ảnh, không có bản ghi Stage-1, nên tốn thêm khoảng 100–165 GPU-h (40–65 s/ảnh, R2-05) và mọi SFT dài ra ×3.

---

## 4. Những gì v2 đã làm đúng

- Đã bỏ GRPO, G1/G2, Qwen3-VL-8B và nhánh 20k khỏi MVP, nên bài toán tương thích env (transformers 4.51.3 / trl 0.19.1) chỉ còn lại ở các baseline LLaVA.
- Có cổng T0.5 trước mọi lượt dựng đồ thị, và sửa luật box "chỉ được NÂNG" theo đúng R2-05 F5.
- Dedup đặt trước mọi gán nhãn, và đo cả trùng train↔test nội bộ KTVIC cho P0. Việc này rẻ, phần chấm lại P0 chạy trên CPU vì đã có file `.preds.json`.
- XM3600 là lựa chọn đúng cho phần phát hành được: có `vi`, caption CC BY 4.0, 0 ảnh trùng UIT theo ViCLIP-OT (R2-06).
- Thời gian SFT trên 3090 khớp với cấu hình đã ghi (7.206 dòng × 2 epoch / 8 ≈ 1.800 bước).
- Hạn IP&M SI 31/08/2027 đã xác minh (`manuscript/cfp/03_special_issues.json`, `verified: true`). P2 có đường lui khi trượt G-P2.
