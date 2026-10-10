# R2-05: Khả thi kỹ thuật và ngân sách GPU của ViHG-Cap (đối chiếu repo và 1× RTX 3090 24 GB)

Critic 05, vòng 2, 2026-10-10. Trục: **khả thi kỹ thuật**. Tôi đối chiếu bản nháp `00_KE_HOACH.md` với code thật trong `rescap/`, `scripts/`, `data/`, và với mã nguồn wheel `transformers==4.51.3` và `trl==0.19.1`. Hai wheel này tôi tải về scratchpad rồi grep, không chạy. Máy này không có GPU và không cài torch/trl, nên mọi điều phải chạy thật đều nằm ở mục 5, "Phải kiểm trên máy GPU".

Ghi chú: thư mục `svp/` ở gốc repo không tồn tại. Code tương ứng là `rescap/svp/` (`entailment.py`, `matching.py`).

Quy ước số liệu:
- **(đo)**: có file hoặc log trong repo.
- **(code)**: đọc thẳng từ mã nguồn.
- **(ước tính)**: suy luận của tôi, chưa đo.

---

## 1. Kết luận theo từng thành phần

| Thành phần | Kết luận | Lý do ngắn |
|---|---|---|
| (A) Đề xuất đồ thị: Qwen2.5-VL-7B + REACT++ + R1-SGG-7B + OWLv2 | **needs-fix** | Không nạp chung trên 24 GB được, phải chạy tuần tự. `QwenVLAdapter` nạp checkpoint Qwen2-VL (R1-SGG) bằng class Qwen2.5-VL, hỏng mà không báo lỗi. REACT++ cần môi trường riêng. |
| (B) Verifier logit Vintern | **needs-fix** | `chat()` chỉ trả văn bản (code), nên phải tự dựng template. Token hóa "có"/"không" chưa kiểm. Ngưỡng/conformal đang định hiệu chỉnh trên 244 mục audit, mà đó là ảnh **test**. |
| (B) Bằng chứng box/hình học | **needs-fix** | Thêm box OWLv2 sẽ kích hoạt hai luật có sẵn trong `verify.py`: thiếu box bị tính 0,0, và mâu thuẫn hình học thì quyết định luôn. Kết quả là REJECT vì lỗi detector, trái quy tắc "không bao giờ REJECT vì thiếu box". |
| (C) Lùi IsA, KG Wikidata | pass (CPU) | Không tốn GPU. Chỉ cần SPARQL ẩn danh và bảng tay. |
| (E1) SFT graph-then-caption | **pass, có điều kiện** | `SFTTrainer` + `VLCollator` hiện có dùng lại được, chỉ cần đổi dữ liệu. Chi phí ×1,5–1,7 mỗi run, suy luận chậm ×3–4. |
| G1 (mặt nạ topo), G2 (graph token) | **needs-fix (thiết kế)** | Mâu thuẫn với E1: E1 để đồ thị ở **đầu ra**, còn G1/G2 cần đồ thị ở **đầu vào**, nên phải chạy pipeline A–D lúc test. Trong 4.51.3, mặt nạ 4D làm hỏng M-RoPE (code). |
| (E2) GEPA | pass | Thêm khoảng 50 dòng vào vòng DPO tự viết sẵn có. Cần căn span theo offset token. |
| (E3) GRPO có ảnh | **needs-fix** | `GRPOTrainer` của trl 0.19.1 chỉ nhận văn bản (0 lần xuất hiện `pixel_values`), nên phải tự viết vòng lặp. Rollout dài 400–600 token, nên 6–8 h/run là thấp. |
| Backbone 2: Qwen3-VL-8B | **needs-fix** | Không có trong transformers 4.51.3 (không có thư mục `qwen3_vl`), nên phải tách venv, phá pin bắt buộc. |
| Baseline InternVL3.5-8B | needs-check | 4.51.3 không có `internvl` native. Chỉ đi được đường remote code, qua `VinternAdapter`. |
| Ngân sách 450–600 GPU-h | **fail** (thiếu hạng mục) | Bỏ sót baseline, eval, parser, meta-eval, backbone 2, GRIT, chạy lại. Dùng số 4090 cho máy 3090. Đường 20k ảnh không có cổng an toàn. Bảng sửa ở mục 3. |

---

## 2. Phát hiện

### F1. BLOCKER: cam kết đồ thị cho 20k ảnh mà không có cổng chặn nếu verifier logit thất bại

- **Plan nói**: "sinh đồ thị 20k ảnh ~1 tuần; verifier logit lại toàn bộ ~vài ngày".
- **Bằng chứng**:
  - Stage-1 hiện tốn khoảng 80 s/ảnh, trung vị 88 GPU-h cho 3.700 ảnh, chạy trên **RTX 4090** với 4 shard (đo: `manuscript/build_v10.py` L141/L167; `data/results/latency_*.json` đều ghi `"gpu": "NVIDIA GeForce RTX 4090"`). Bản ghi mẫu ghi `stats.probe_calls = 102`, `stats.seconds = 67.2` (đo: `data/stage1_records/sample_00000000002.json`).
  - Gần như toàn bộ thời gian là verify với K=5 (`research_wall/05_efficiency.md` §0: khoảng 0,78 s mỗi probe call).
  - ViHG-Cap còn **thêm** bộ ba từ REACT++ (top-100) và R1-SGG vào hàng đợi kiểm chứng, cộng probe phủ định cho từng cái. Số truy vấn mỗi ảnh vì thế tăng ×2–4 (ước tính).
  - Nếu logit **không** đạt (κ thấp so với K=5, hoặc precision không tăng), đường K=5 cho 20k ảnh tốn khoảng 20.000 × 80 s × 1,3 (hệ số 3090/4090 khi decode) × 2 (bộ ba thêm) ≈ **1.150 GPU-h, chỉ riêng khâu dựng dữ liệu** (ước tính).
  - Không có cổng T nào trong plan chặn trường hợp này.
- **Sửa**:
  1. Thêm **cổng T0.5** vào mục 5: "Verifier logit trên ~100 ảnh train (khoảng 300 truy vấn có nhãn người) và trên 244 mục audit: (i) quyết định argmax trùng ≥ 98% với văn bản greedy của `chat()`; (ii) κ(logit, K=5) ≥ 0,7; (iii) precision SUPPORTED ≥ 63,1% ở cùng recall. Không đạt thì giữ K=5 và **chỉ làm KTVIC**."
  2. Đổi mục 5 "Ngân sách" và mục 8 (tháng 11) thành: "Sinh G* cho **KTVIC 4.327 ảnh** (train 3.769 + test 558). Mở rộng UIT-OpenViIC/UIT-ViIC chỉ sau T1, nếu thí nghiệm theo cỡ dữ liệu cho thấy có lợi."
  3. Với 3.700 ảnh train đã có bản ghi Stage-1, **dùng lại mệnh đề đã sinh** (`data/stage1_records/`) và chỉ chạy lại verify. Như vậy bỏ được khoảng 12–18 GPU-h sinh mệnh đề Qwen-7B.

### F2. MAJOR: ngân sách 450–600 GPU-h bỏ sót hạng mục và dùng số đo trên 4090

- **Plan nói**: "Tổng ~450–600 GPU-h ≈ 3–4 tuần".
- **Bằng chứng**: cộng các dòng của plan ra 168 + ~72 + 75–140 + 80–100 + 65–75 + GRPO ≈ 500–600. Các hạng mục **không có** trong tổng:
  - baseline: khoảng 14 hệ thống, cộng huấn luyện GRIT;
  - eval của khoảng 35 mô hình đã huấn luyện;
  - parser: đồ thị bạc từ khoảng 18,5k caption, cộng fine-tune ViT5/Qwen-1.5B;
  - meta-eval: VLM-judge và 6.000 nhiễu;
  - backbone 2 × 3 seed;
  - POPE/AMBER/PDG;
  - chạy hỏng, chạy lại, OOM.

  Ngoài ra, mọi số đo trong repo là trên 4090. Riêng con số "3,6 h/SFT" (`05_efficiency.md`: 7,3 s/it × 1.800 bước, mỗi bước 8 micro-batch, tức 7.177 ví dụ × 2 epoch / 8 ≈ 1.794 bước) **không ghi GPU**, trong khi README L136 ghi "~2 h per run on an RTX 4090". Hai số này cùng khớp với giả thuyết 3,6 h là số trên 3090, tức tỉ lệ ≈ 1,8× cho pha tính toán nặng.
- **Sửa**: thay dòng "Ngân sách GPU" ở mục 5 bằng bảng ở mục 3 dưới đây: **≈ 520–760 GPU-h cho đường chỉ KTVIC (trung tâm ~640)**, và ≈ 900–1.300 GPU-h nếu làm 20k ảnh. Ghi rõ: "hệ số 3090/4090: ×1,2–1,3 cho decode, ×1,8 cho SFT (suy từ README so với số 3,6 h); đo lại 50 bước trên 3090 trước khi chốt."

### F3. MAJOR: GRPO có ảnh không chạy được bằng trl 0.19.1, và chi phí rollout bị tính thấp

- **Plan nói**: "E3 GRPO… 6–8 h/run".
- **Bằng chứng (code)**:
  - Trong `trl/trainer/grpo_trainer.py` của trl 0.19.1, `pixel_values` xuất hiện 0 lần. Model được nạp bằng `AutoModelForCausalLM.from_pretrained` (L431). `_get_per_token_logps` chỉ truyền `input_ids` và `attention_mask` (L857–866). `_generate_and_score_completions` token hóa prompt dạng văn bản (L1051+).
  - Repo đã ghi rằng `DPOTrainer` của trl 0.19 làm rơi `image_grid_thw` (`train_stage2.py`, docstring `run_dpo`), và rằng trl 1.x không import được với transformers 4.51.3.
  - Con số 6–8 h/run (07/00_TONG_HOP) giả định caption ngắn khoảng 100 token. Với E1, mỗi rollout gồm đồ thị và caption, khoảng 400–600 token. Decode NF4 bằng HF trên 3090 đạt khoảng 12–18 token/s (ước tính). Với G=4, tốn khoảng 25–40 s mỗi prompt; 1.000 prompt ⇒ **10–15 h/run** (ước tính).
  - Reward "phụ thuộc cha–con" cần biến caption sinh ra thành đồ thị, tức phụ thuộc parser T3 (tháng 12).
- **Sửa**:
  1. Mục 2 (E3) thêm câu: "Vòng lặp GRPO tự viết trong `train_stage2.py --stage grpo` (on-policy, một lần cập nhật, nên tỉ số PPO = 1; loss = −Â·log π + β·KL với tham chiếu là adapter `ref_sft`, theo đúng mẫu `run_dpo`). Reward tra cứu offline trên G* cộng parser, không gọi verifier trực tuyến."
  2. Mục 5 sửa thành: "GRPO 10–15 h/run × 2 reward × 3 seed ≈ 60–90 GPU-h."
  3. Thứ tự phụ thuộc: E3 chỉ bắt đầu sau khi có parser (T3).

### F4. MAJOR: Qwen3-VL-8B (backbone 2) không có trong transformers đang pin

- **Plan nói**: "Qwen2.5-VL-7B / Qwen3-VL-8B, QLoRA"; tháng 02/2027 "backbone thứ 2 (Qwen3-VL-8B)".
- **Bằng chứng (code)**:
  - Wheel transformers 4.51.3 có `models/qwen2_vl`, `qwen2_5_vl`, `qwen3`, `owlv2`, nhưng **không có** `qwen3_vl` hay `internvl`.
  - README bắt buộc pin 4.51.3 và trl 0.19.1, vì bản mới hơn làm sai suy luận Qwen2.5-VL mà không báo lỗi.
  - `train_stage2.py` hard-code `MODEL_ID = "Qwen/Qwen2.5-VL-7B-Instruct"` và `Qwen2_5_VLForConditionalGeneration`.
- **Sửa**:
  1. Mục 5 ghi: "Backbone 2 chạy trong venv riêng (`.venv-q3`, transformers đủ mới cho Qwen3-VL; số phiên bản tối thiểu kiểm trên máy). Trong `train_stage2.py` thêm `--model-id` và dùng `AutoModelForImageTextToText`. Nếu trl 0.19.1 không tương thích transformers mới, thay `SFTTrainer` bằng vòng lặp tự viết (cùng collator)."
  2. Phương án dự phòng, không cần đổi môi trường: InternVL3.5-8B hoặc InternVL2.5-8B qua remote code. Cách này cần một collator mới theo format InternVL (`IMG_CONTEXT`), khoảng 1–2 ngày công.
  3. Thêm cổng: "Nếu chạy Qwen3-VL trong venv mới mà Qwen2.5-VL vẫn phải ở venv cũ, báo hai hệ thống trên **hai môi trường** trong bảng tái lập."

### F5. MAJOR: thêm box OWLv2 sẽ đẩy REJECT qua luật có sẵn trong `verify.py`

- **Plan nói**: "bằng chứng hình học từ box"; mục 7.2 "`geometric_check()` chưa từng chạy". Research wall (00_TONG_HOP mục 2) đặt quy tắc: "không bao giờ REJECT vì thiếu box".
- **Bằng chứng (code)**:
  - `rescap/pipeline/verify.py` L1003–1010: nếu **bất kỳ** thực thể nào khác trong ảnh có box mà thực thể này không có, tín hiệu `bbox` = 0,0 ("đối tượng không được định vị"). Khi OWLv2 phủ một phần thực thể, mọi thực thể detector bỏ sót sẽ bị phạt.
  - L317–320: `geometric_contradiction_c = 1.0`, với lý giải "geometry is the one channel that cannot hallucinate". Giả định này chỉ đúng với box gold. Với box detector, việc gán box cho thực thể (khớp nhãn VI→EN, chọn instance) chính là một nguồn lỗi.
- **Sửa**:
  1. Mục 2 (B) thêm câu: "Box từ detector là bằng chứng một chiều: thiếu box → `bbox` unavailable (None), không phải 0,0; mâu thuẫn hình học → tối đa UNCERTAIN (`geometric_contradiction_c` < θ_C^hi), trừ khi box là gold."
  2. Thay đổi file: thêm cờ `box_source: "detector" | "gold"` vào `VerificationConfig` (`verify.py` khoảng L291–410), rẽ nhánh ở L1003 và ở chỗ dùng `geometric_contradiction_c`.

### F6. MAJOR: verifier logit Vintern chưa làm được "một lượt" như plan mô tả, và đang định hiệu chỉnh trên test

- **Plan nói**: "Vintern logit P(Có)/P(Không) một lượt (thay K=5) + ngưỡng theo loại, hiệu chỉnh conformal".
- **Bằng chứng (code)**:
  - `rescap/vlm/vintern.py` đặt `supports_logprobs = False`, gọi `self._model.chat(...)` và `batch_chat(...)`; cả hai chỉ trả văn bản.
  - `verify.py` L2187–2194 tự đặt `probe_k = SELF_CONSISTENCY_K` khi backbone không có logprob.
  - `base.py::probe_yes_no` lấy confidence bằng **trung bình xác suất token sinh ra** (đường TOKEN_PROB của Qwen), không phải P(có)/(P(có)+P(không)). Bật `supports_logprobs=True` thôi thì không đủ, và còn **sai nghĩa**.
  - `_generate_many` còn `torch.cat([tiles]*n)`, nên InternViT mã hóa lại ảnh ở mỗi probe.
  - Theo memory của dự án, 244 mục audit là ảnh **test** (bản ghi Untrained-VSPS). Chỉnh ngưỡng hay conformal trên đó là rò rỉ.
- **Sửa**:
  1. Mục 2 (B) ghi: "Override `probe_yes_no` trong `VinternAdapter`: dựng query theo template của remote `chat()` (IMG_CONTEXT × num_patches), mã hóa ảnh một lần cho mỗi ảnh (`extract_feature`), chạy một forward có `logits_to_keep=1` cho cả batch truy vấn, rồi lấy P(có) = Σ softmax trên tập token id của {có, Có, ␣có} chia cho tổng trên {có…} ∪ {không…}. Nếu 'có'/'không' bị tách thành nhiều token BPE thì chấm cả chuỗi bằng teacher forcing (2 ứng viên, chung prefix)."
  2. Mục 4 thêm dữ liệu: "**Tập hiệu chỉnh từ ảnh train** (~300–500 mệnh đề, gán nhãn bằng `scripts/annotate.py`); 244 mục audit chỉ dùng để báo kết quả."

### F7. MAJOR: G1/G2 mâu thuẫn với E1, và G1 làm hỏng M-RoPE trong 4.51.3

- **Plan nói**: "G0 đồ thị dạng văn bản…; G1 + mặt nạ attention theo topo; G2 + 8 graph token. Đối chứng bắt buộc: đồ thị bị xáo trộn."
- **Bằng chứng (code)**:
  - E1 là "graph-then-caption", tức đồ thị **do mô hình tự sinh** ở đầu ra. G1/G2 lại cần đồ thị có sẵn ở **đầu vào**. Khi đó lúc test phải chạy toàn bộ A–D (khoảng 30–50 s/ảnh, ước tính) và mất claim "single pass" mà VSPS đang giữ.
  - `modeling_qwen2_5_vl.py` (4.51.3), ngay trước khi tính `get_rope_index`: "if we get 4D attention mask we cannot calculate rope deltas anymore". `position_ids` chỉ được tính khi `attention_mask.ndim == 2`.
  - Khi truyền `inputs_embeds`, nhánh trộn `pixel_values` bị bỏ qua (điều kiện `if inputs_embeds is None:`), nên G2 đi kiểu `inputs_embeds` sẽ mất ảnh.
- **Sửa**:
  1. Mục 2, "Biến thể mô hình", tách ra một chế độ riêng: "**Graph-conditioned** (đồ thị G* ở đầu vào, cần pipeline lúc test; chỉ để ablation)". Đối chứng xáo trộn cho E1 đổi thành: "ép decode một tiền tố đồ thị đã sửa hoặc xáo trộn (teacher forcing), rồi đo caption có đi theo đồ thị không". Cách này rẻ, không cần huấn luyện lại, và dùng luôn cho đường cong SFA khi quét mức IsA, nên **bỏ được khoảng 3 run SFT**.
  2. Cách làm G1: tính trước `position_ids, rope_deltas = model.get_rope_index(input_ids, image_grid_thw, None, mask2d)`; truyền `position_ids` cùng mặt nạ 4D float (sdpa hoặc eager, không flash); đặt `model.rope_deltas` thủ công sau prefill; decode bằng vòng lặp riêng.
  3. Cách làm G2: forward hook trên `get_input_embeddings()` để thay embedding ở vị trí placeholder `<|graph_k|>`. Ảnh vẫn được trộn bình thường, `generate` vẫn chạy.
  4. Cổng: chỉ làm G1/G2 nếu thí nghiệm ép tiền tố cho thấy G0 thật sự đọc đồ thị. Đề xuất **bỏ G2** khỏi lộ trình chính.

### F8. MAJOR: `QwenVLAdapter` nạp checkpoint Qwen2-VL (R1-SGG-7B) bằng class Qwen2.5-VL

- **Bằng chứng (code)**:
  - `rescap/vlm/qwen_vl.py` `load()`: `try: from transformers import Qwen2_5_VLForConditionalGeneration as _Model`, nên **luôn** dùng class 2.5 khi class này có mặt.
  - Registry có `"qwen2-vl-7b"`, và R1-SGG-7B là Qwen2-VL-7B (07 dòng 46). Hai kiến trúc vision khác nhau (Qwen2.5 dùng RMSNorm và MLP gate/up/down), nên trọng số không khớp sẽ bị khởi tạo ngẫu nhiên và đầu ra là rác, không có lỗi cứng nào báo.
- **Sửa** (1 dòng): chọn class theo `AutoConfig.from_pretrained(model_id).model_type`, hoặc dùng `AutoModelForImageTextToText`. Trước khi chạy R1-SGG, kiểm log "missing/unexpected keys" phải rỗng.

### F9. MAJOR: E1 tăng chi phí cả huấn luyện lẫn eval, nhưng plan chỉ cộng cho huấn luyện

- **Bằng chứng**:
  - Đồ thị tuyến tính hóa dài khoảng 250–450 token (06 §4, ước tính). Chuỗi SFT hiện có khoảng 512 token ảnh + khoảng 60 token prompt + khoảng 30–120 token đáp án, tức khoảng 650–700 token. Thêm đồ thị thì thành khoảng 1.000–1.150 token, chi phí ×1,5–1,7, tức **5,4–6,1 h/run 7B**.
  - Latency suy luận chế độ detailed hiện là 2,06 s (160 token, 4090, đo). Với 400–600 token, ước tính khoảng 6–9 s trên 3090. Một lượt eval 558 ảnh từ khoảng 25 phút thành khoảng 1–1,3 h.
- **Sửa**:
  1. Mục 5 thêm dòng: "eval graph-then-caption ≈ 1–1,3 h mỗi mô hình mỗi tập test".
  2. Bảng latency phải báo **cả token đồ thị**, vì đây là cái giá của "single pass".
  3. `scripts/evaluate.py` cần tách khối đồ thị khỏi caption trước khi chấm (`--strip-graph`), và lưu đồ thị cho M1.

### F10. MINOR

1. **Không nạp chung các mô hình được.** Qwen2.5-VL-7B bf16 (khoảng 15,2 GB, `qwen_vl.py` docstring) cộng R1-SGG-7B bf16 (khoảng 16–17 GB) vượt 24 GB. Phải chạy thành **các lượt tuần tự** ghi JSONL:
   - (1) REACT++ ONNX, trong env riêng;
   - (2) OWLv2, có sẵn trong 4.51.3 (`models/owlv2`), khoảng 1–2 GB;
   - (3) R1-SGG-7B với `max_pixels` giới hạn;
   - (4) verify Vintern-1B (khoảng 2 GB).

   Bộ đôi Qwen-7B + Vintern-1B đang chạy chung được (`generate_stage1.py` L151–153).
2. **REACT++** dựa trên SGG-Benchmark/YOLOv8 và có bản ONNX (07). Không nên cài vào venv pin torch cu121; dùng `onnxruntime-gpu` trong env riêng. Nhãn VG150/PSG là tiếng Anh, cần bảng EN→VI khoảng 250 nhãn (khoảng 1 ngày công).
3. **R1-SGG qua vLLM**: vLLM không có trong `requirements.txt`, đòi torch riêng và WSL2 + CUDA. Ngân sách của tôi dùng HF tuần tự, 10–20 s/ảnh (07, ước tính). Cần đo 20 ảnh trước.
4. **OPERA** viết cho transformers đời cũ và LLaVA; port sang Qwen2.5-VL tốn nhiều công. Đề xuất thay bằng DoLa (có trong `generate` của 4.51.3, cần kiểm với Qwen2.5-VL) cộng VCD (đã có trong `scripts/baselines.py`). Nếu bỏ OPERA thì ghi rõ lý do.
5. **GEPA**: y⁺ và y⁻ khác số token ở cụm sửa, nên KL trên "token ∉ σ" phải căn phần hậu tố theo offset ký tự (`return_offsets_mapping`, tokenizer fast của Qwen2). Đặt span ở ranh giới từ để tránh token BPE vắt qua mép span. Bộ nhớ: tham chiếu full-vocab cho khoảng 1.100 token fp32 tốn khoảng 0,7 GB, chấp nhận được. Mức 19,15 GB đo cho DPO 4-bit với 512 vt (`train_stage2.py` docstring) cho thấy còn chỗ.
6. **GRIT** (leaderboard KTVIC) có repo và môi trường riêng (CUDA op deformable). Huấn luyện lại trên KTVIC ước tính 10–20 GPU-h, chưa xác minh. Nên xin checkpoint hoặc dự đoán từ tác giả trước.
7. **Wikidata IsA**: CPU, SPARQL ẩn danh (không gửi email trong User-Agent), cache về `data/kg/`. Không cần dump.

---

## 3. Ngân sách GPU đã sửa (1× RTX 3090, đường **chỉ KTVIC**)

Đơn giá dùng trong bảng:
- SFT 7B caption-only: 3,6 h / 7.177 ví dụ × 2 epoch (đo; GPU chưa ghi, coi là 3090), tức khoảng 0,9 s mỗi ví dụ-epoch.
- SFT graph-then-caption: ×1,5–1,7.
- 3B ≈ 0,45 × 7B.
- Eval caption: 2,7 s/ảnh (đo). Eval graph-then-caption: ×2,5–3.
- Dựng dữ liệu bằng logit: 10–25 s verify + 10–20 s R1-SGG mỗi ảnh (ước tính).

| # | Hạng mục | Cách tính | GPU-h |
|---|---|---|---|
| 1 | Kiểm máy, benchmark 50 bước SFT, 20 ảnh R1-SGG, 50 ảnh verify | | 2–3 |
| 2 | Cổng T0.5: logit so với K=5 trên khoảng 100 ảnh train + 244 mục audit | K=5: 100 × 80 s × 1,3 | 2–4 |
| 3 | Front-end: REACT++, OWLv2, R1-SGG-7B (HF) cho 4.327 ảnh | 0,1 + 1–2 + 4.327 × 10–20 s | 13–26 |
| 4 | Sinh mệnh đề Qwen-7B | dùng lại bản ghi Stage-1 (train); chỉ test 558 × 15 s | 2–3 |
| 5 | Verify logit (mệnh đề + bộ ba SGG + phủ định, 300–400 truy vấn/ảnh) | 4.327 × 10–25 s | 12–30 |
| 6 | Máy gợi ý cho pilot gold SG 500 ảnh | số của plan | 15–20 |
| 7 | E1 SFT 7B: chính × 3 seed, caption-only cùng dữ liệu × 3 seed, 5 ablation (−IsA, −KG, −box, nhãn K=5, xáo trộn) × 1 seed | 11 × 5,4–6,1 | 59–67 |
| 8 | G1 (chỉ khi có go) × 3 seed, cộng G* lúc test cho 558 ảnh; G2 bỏ | 3 × 5,5–6 + 558 × 40 s | 22–24 |
| 9 | E2 GEPA: lưới 3B khoảng 10 run; 7B 4 cấu hình × 3 seed | 10 × 1,5–2 + 12 × 4–6 | 63–92 |
| 10 | E3 GRPO (vòng tự viết): 2 reward × 3 seed, cộng debug | 6 × 10–15 + 5–10 | 65–100 |
| 11 | Backbone 2 (Qwen3-VL-8B): chính và đối chứng × 3 seed | 6 × 6–7 | 36–42 |
| 12 | Baseline: khoảng 14 hệ thống × 2 tập test, VCD (×2 decode), GRIT huấn luyện lại | 14–28 + 2–4 + 10–20 | 26–52 |
| 13 | Eval khoảng 35 mô hình đã huấn luyện (KTVIC; tập chéo chỉ cho hệ chính) | 35 × 1–1,3 + 10 × 1,1 | 40–60 |
| 14 | Parser: đồ thị bạc từ khoảng 18,5k caption (7B, text) + fine-tune ViT5 / Qwen-1.5B | 18,5k × 2–4 s + 5–8 | 15–28 |
| 15 | Meta-eval: caption 500 ảnh × 5 hệ thống, VLM-judge 2.500 caption + 6.000 nhiễu | | 9–13 |
| 16 | POPE / AMBER / PDG (ảnh trắng) cho khoảng 6 mô hình | | 15–20 |
| | **Cộng** | | **396–584** |
| | **+30% chạy hỏng, chạy lại, OOM, đo lại hệ số 3090** | | **≈ 515–760 (trung tâm ~640)** |

- **Đường 20k ảnh**: cộng thêm khoảng 15,7k ảnh × 40–65 s (phải sinh mệnh đề mới, vì không có bản ghi) ≈ 175–285 GPU-h. Các run E1 chính cũng dài ra ×3–4. Tổng thành **≈ 900–1.300 GPU-h**. Nếu logit trượt T0.5 và phải giữ K=5, khâu dựng dữ liệu 20k ảnh đã khoảng 1.150 GPU-h. **Không khả thi** trong khung 01–03/2027.
- **Lịch máy**: 640 GPU-h ở mức sử dụng khoảng 80% ≈ 33 ngày máy. Đoạn găng 01–02/2027 (mục 7–11) cần khoảng 245–325 GPU-h, cộng 30% thì khoảng 320–420 h trên tổng 1.416 h đồng hồ của hai tháng. Khả thi nếu chỉ một người dùng GPU và dữ liệu (mục 3–5) xong trước 31/12.
- **Câu thay cho mục 5 của plan**: "Ngân sách GPU (1× RTX 3090; đơn giá đo trên 4090 quy đổi ×1,2–1,8, cần đo lại): ≈ 520–760 GPU-h cho đường KTVIC (≈ 4–5 tuần máy); đường 20k ảnh ≈ 900–1.300 GPU-h, chỉ mở sau T0.5 và T1."

---

## 4. Danh sách việc kỹ thuật theo thứ tự phụ thuộc (thay đổi ở cấp file)

Mỗi bước chỉ bắt đầu khi bước nó phụ thuộc đã xong. "≈" là công người, ước tính.

**Bước 0. Kiểm máy (0,5 ngày).**
- `scripts/verify_environment.py`: in tên GPU và phiên bản; kiểm file remote code của Vintern (mục 5); chạy `train_stage2.py --stage sft --limit 400` để đo s/it trên 3090.

**Bước 1. Verifier logit (2–3 ngày). Phụ thuộc: 0.**
- `rescap/vlm/vintern.py`:
  - thêm tham số `confidence="sc"|"logit"`;
  - khi là `logit`: `supports_logprobs=True` và override `probe_yes_no()` và `probe_with_negation()`, trả `YesNo` với `ConfidenceMethod.TOKEN_PROB`; INCONCLUSIVE khi P(có)+P(không) < τ_mass;
  - cache `pixel_values` / `vit_embeds` cho mỗi ảnh;
  - batch các truy vấn của một ảnh.
- `rescap/vlm/registry.py`: thêm `"vintern-1b-logit"`. Giữ `"vintern-1b"` (K=5) để tái lập kết quả cũ.
- `configs/verify_logit.json`: ngưỡng và trọng số mới. `VerificationConfig.from_config` bắt buộc phải có (L382–396).
- `scripts/calibrate_logit.py`: quét ngưỡng theo loại mệnh đề trên **tập hiệu chỉnh từ ảnh train**.
- Kiểm tra tối thiểu: `scripts/test_vintern_logit.py`, so argmax logit với văn bản greedy `chat()` trên 200 probe, đạt ≥ 98%.
- → **Cổng T0.5.**

**Bước 2. Cổng cấu trúc mệnh đề (1 ngày). Phụ thuộc: không; song song với bước 1.**
- `scripts/clean_supervision.py` (`--clean-props` đã có) và `rescap/pipeline/generate.py`: tách object khỏi vị từ; viết lại vị từ phủ định để không sinh câu hỏi phủ định kép.

**Bước 3. Box và hình học (1,5 ngày). Phụ thuộc: không.**
- Mới: `scripts/detect_boxes.py`. OWLv2 qua `transformers.Owlv2ForObjectDetection` (có trong 4.51.3); câu truy vấn lấy từ ánh xạ VI→EN trong `rescap/vi/lexicon.py`; ghi `entity["bbox"] = [x, y, w, h]` theo pixel tuyệt đối, đúng schema `as_box()` (L671–709).
- `rescap/pipeline/verify.py`: thêm cờ `box_source`, rẽ nhánh ở L1003 (thiếu box → None) và ở `geometric_contradiction_c` (detector → tối đa UNCERTAIN) (F5).

**Bước 4. Front-end SGG (2–3 ngày). Phụ thuộc: 3, dùng box để gộp theo IoU.**
- `rescap/vlm/qwen_vl.py`: chọn class theo `model_type` (F8).
- Mới: `scripts/sgg_r1.py` (R1-SGG-7B, HF, `max_pixels` giới hạn, ghi JSONL).
- Mới: `scripts/sgg_react.py` (env riêng, ONNX).
- Mới: `data/kg/vg150_en_vi.tsv`.
- Mới: `scripts/merge_graph.py`: gộp nút theo IoU và đồng nghĩa; xuất truy vấn cho verify.

**Bước 5. IsA và KG (3–4 ngày, CPU). Phụ thuộc: không.**
- Mới: `data/kg/isa_vi.tsv` (khoảng 250 dòng tay) và `data/kg/culture_vi.tsv` (150–300 thực thể).
- Mới: `scripts/build_wikidata_isa.py` (SPARQL ẩn danh, có cache).
- Hàm `parent(label)` đặt trong `rescap/vi/lexicon.py`.
- Logic lùi: mở rộng `scripts/extra_backoff.py` / `scripts/relation_backoff.py` thay vì viết module mới.

**Bước 6. Dựng G* cho KTVIC (dùng khoảng 30–60 GPU-h). Phụ thuộc: 1–5.**
- Chạy verify với `vintern-1b-logit` trên mệnh đề Stage-1 có sẵn, cộng truy vấn từ bước 4.
- Mới: `scripts/build_graph_sft.py`. Dùng lại phần chọn của `build_dpo_data.py` và phần render của `rescap/pipeline/realize.py`. Xuất `sft.jsonl` với `response = "<đồ thị>…</đồ thị>\n" + caption`.

**Bước 7. E1 (dùng khoảng 60–67 GPU-h). Phụ thuộc: 6.**
- `scripts/train_stage2.py`: **không cần đổi** gì ngoài `--data`.
- `scripts/evaluate.py`: thêm `--strip-graph`, lưu khối đồ thị riêng; nâng `--max-new-tokens` cho chế độ đồ thị.
- Mới: `scripts/forced_prefix_probe.py`, đối chứng xáo trộn và quét IsA bằng tiền tố ép (F7).

**Bước 8. Parser và metric (5–7 ngày). Phụ thuộc: 6 (schema G*).**
- Mới: `scripts/parse_silver.py`, `scripts/train_parser.py` (ViT5 qua `AutoModelForSeq2SeqLM`).
- Mới: `rescap/metrics_graph.py` (M1–M6), dùng lại `rescap/svp/matching.py` và `rescap/chair.py`.

**Bước 9. GEPA (2 ngày). Phụ thuộc: 6, 7.**
- Mới: `scripts/build_gepa_pairs.py`: sửa G*, render lại, ghi span ký tự.
- `scripts/train_stage2.py`: thêm `--stage gepa`, tái dùng `run_dpo` với mặt nạ span, KL theo token và `ref_sft`.
- Kiểm tra: `scripts/test_gepa_mask.py`, xác nhận phần ngoài span của y⁺ và y⁻ cho log-prob khớp nhau sau khi căn.

**Bước 10. GRPO (3–4 ngày). Phụ thuộc: 7, 8.**
- `scripts/train_stage2.py`: thêm `--stage grpo` (vòng tự viết, G=4, tắt gradient checkpointing hoặc bật `use_cache` khi sinh).
- Mới: `rescap/reward.py` (tra cứu G* + parser; một bản phẳng, một bản phụ thuộc cha–con).

**Bước 11. Backbone 2 (2–3 ngày). Phụ thuộc: 7.**
- Venv `.venv-q3`.
- `scripts/train_stage2.py`: thêm `--model-id`, `AutoModelForImageTextToText`, `_vision_token_budget` theo processor của Qwen3-VL.

**Bước 12. Baseline (3–4 ngày, song song từ tháng 12).**
- `rescap/vlm/registry.py`: thêm `"internvl3.5-8b"` (kind `vintern`, remote code).
- `scripts/baselines.py`: thêm `dola`; KG-in-prompt và RAG chỉ là biến thể prompt.
- GRIT dùng repo và env riêng.

**Bước 13 (tùy chọn, chỉ khi bước 7 cho go). G1.**
- Mới: `scripts/train_graph_mask.py`: tính `position_ids` trước, mặt nạ 4D, `rope_deltas` thủ công, vòng decode riêng (F7).

---

## 5. Phải kiểm trên máy GPU (không kiểm được ở đây)

1. **Remote code của Vintern-1B-v3_5**:
   - `grep -n "def chat\|def batch_chat\|def generate\|def extract_feature\|IMG_CONTEXT\|template\|system_message" ~/.cache/huggingface/hub/models--5CD-AI--Vintern-1B-v3_5/snapshots/*/modeling_internvl_chat.py`
   - Đọc thêm `conversation.py` và trường `template` trong `config.json`.

   Cần xác nhận ba điều: (a) `generate()` chuyển `**generate_kwargs` xuống `language_model.generate`, để `output_scores` và `return_dict_in_generate` đi qua được; (b) có tham số `visual_features` để không mã hóa lại ảnh; (c) system prompt mặc định của Vintern, vì template dựng tay phải khớp từng ký tự.
2. **Token hóa**: `tok.encode(x, add_special_tokens=False)` với x ∈ {"có", "Có", " có", "không", "Không", " không"}. Nếu có chuỗi bị tách thành nhiều token, dùng chấm điểm teacher forcing thay cho token đầu.
3. **Độ khớp**: argmax logit so với văn bản `chat()` greedy trên 200 probe, đạt ≥ 98%. Nếu không, template đang lệch.
4. **Tốc độ trên 3090**: s/it của SFT; s/ảnh của verify logit và R1-SGG HF; tok/s decode NF4 (cho GRPO).
5. **R1-SGG-7B**: phiên bản transformers ghi trong `config.json`, và log nạp trọng số không có missing/unexpected keys sau khi sửa F8.
6. **InternVL3.5-8B** remote code có chạy với 4.51.3 không. **Qwen3-VL** cần phiên bản transformers tối thiểu nào, và trl 0.19.1 còn tương thích với phiên bản đó không. Cả hai chưa xác minh.
7. **DoLa** (`dola_layers`) có chạy với `Qwen2_5_VLForConditionalGeneration.generate` trong 4.51.3 không.

---

## 6. Plan làm đúng ở đâu

- Chọn QLoRA và text-graph G0 làm mặc định, 0 tham số thêm. Cách này khớp với cái card chạy được (đo: 4-bit/512 vt).
- Không huấn luyện lại SGG mà dùng checkpoint công khai.
- E2 dựng trên vòng DPO tự viết có sẵn, có adapter tham chiếu `ref_sft`. Đây là lựa chọn đúng, vì trl 0.19 hỏng với VLM.
- Đổi K=5 sang logit là đòn bẩy chi phí lớn nhất. Hướng này đúng; chỉ thiếu cổng chặn (F1, F6).
- Đã có các cổng dừng/đi T1–T4 và luật dừng G1/G2. Chỉ cần thêm T0.5 và đặt lại chỗ cho đối chứng xáo trộn.
