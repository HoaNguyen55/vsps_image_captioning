# Q1_GAP: kiểm tra mức sẵn sàng cho tạp chí Q1 (11/10/2026)

Chuẩn so sánh: IEEE TMM, Pattern Recognition, Neurocomputing, IEEE TNNLS. Cơ sở: `06_PHUONG_PHAP_HOAN_CHINH.md`, `KE_HOACH_Q2.md`, `R2_01_sota_bar.md`, cùng việc đọc trực tiếp `scripts/` và `data/results/`. File này không có số đo mới. Mọi số đều lấy từ file đã có trong repo.

**Phán quyết.** Bài chưa đủ điều kiện nộp. Đối thủ mạnh nhất vẫn là P1 (SFT trên caption gold), và chính repo đã có nó. P1 thắng mọi hệ thống trên mọi metric. Phương pháp mới (mục tiêu fuse2 rồi E5) **chưa có một con số nào trên tập test**. Các mục dưới đây là điều kiện cần, chưa phải điều kiện đủ.

---

## 1. Metric

### 1a. Code đo được những gì

| Metric | Script | Trạng thái | Thiếu gì cho bảng Q1 |
|---|---|---|---|
| BLEU-1..4, ROUGE-L, CIDEr | `evaluate.py` (pycocoevalcap, RDRSegmenter mức từ, thang ×100) | Có | CI bootstrap cho B-4 và ROUGE-L (`score_ci.py` mới có CIDEr) |
| METEOR | `evaluate.py` | **Chỉ có ở short.** Bị tắt ở detailed vì pipe JVM deadlock. Thêm một lỗi: khi chấm lại bằng `--predictions` mà không truyền `--prompt`, giá trị mặc định là `detailed`, nên METEOR bị **bỏ qua mà không báo**, và file ghi sai `prompt_style` | Chấm lại với `--prompt short` (CPU). Cần ghi rõ METEOR 1.5 không có bảng paraphrase tiếng Việt, tức chỉ khớp exact/stem |
| SPICE | `rescap/metrics.py` gọi SPICE Java | Mọi file đều `SPICE=None`. Parser của SPICE chỉ chạy được tiếng Anh, nên dù chạy được cũng vô nghĩa với tiếng Việt | **Thiếu.** Thay bằng "SPICE-vi": F1 ở mức mệnh đề kiểu CAPTURE/DCScore, dùng parser mệnh đề `rescap/svp`. Chưa có script |
| CLIPScore / RefCLIPScore | không có | Thiếu | Cần một CLIP đa ngôn ngữ (ví dụ jina-clip-v2 hoặc M-CLIP XLM-R). Đây là dependency mới |
| BERTScore | `metrics.py` chỉ nhắc trong docstring | Không tính | Không bắt buộc |
| CHAIR_i / CHAIR_s (vi) | `evaluate.py` → `rescap/chair.py` (113 lớp, gold suy từ 5 tham chiếu) | Có, ghi ở khóa `chair` của mọi `*-{short,detailed}.json` | Đây chỉ là **cận trên**, vì gold thiếu. Bản đo trên gold đầy đủ cần E6 |
| Object P/R/F1 + CI | `object_prf.py --ci` (exact, hypernym, R_spec, R_vague; 1.000 lần bootstrap) | Có cho `*-detailed.preds.json` | Chưa có cho short. Chưa có kiểm định paired giữa hai hệ thống (chỉ so CI có chồng nhau hay không) |
| CI bootstrap paired | `score_ci.py` (CIDEr, CHAIR_i, B=5.000, paired) | Có code, nhưng **chưa lưu kết quả nào** trong `data/results` | Chạy cho mọi cặp ứng viên so với P1 rồi commit JSON |
| POPE-vi | không có. `probe_existence.py` đã có hạ tầng hỏi "Trong ảnh có X không?" | Thiếu | Cần gold E6 cho câu dương; câu âm lấy theo random/popular/adversarial |
| Human eval | `human_eval_*.py` | 50 ảnh × 2 người chấm, κ 0,86-0,95 | Chuẩn Q1 là ≥ 200 ảnh × 3 người chấm, Fleiss κ, blind |

**Một chỗ lệch cần sửa trước khi viết bảng:** `evaluate.py` in số GRIT tham chiếu là "B-4 34.2 · METEOR 28.5 · ROUGE-L 56.1", còn R2_01 ghi theo PDF KTVIC là B-4 40.6 / METEOR 36.6 / ROUGE-L 59.7. Hai bộ số không thể cùng đúng. Phải đối chiếu lại Bảng 3 của PDF. **Đã đối chiếu (11/10):** Bảng 3 của arXiv 2401.08100 ghi GRIT 74.7 / 40.6 / 36.6 / 59.7 / 136.0; 34.2 và 28.5 không xuất hiện trong bài. `evaluate.py` đã sửa theo Bảng 3.

### 1b. `data/results/*.json` đang có những gì

KTVIC test, 558 ảnh. "–" nghĩa là chưa có file.

| Hệ thống | Short: B-4/M/R/C | Short CHAIR_i | Detailed CHAIR_i | Object P/R/F1 [CI] (detailed) | Seed |
|---|---|---|---|---|---|
| P1 gold-SFT | 45.5 / 39.1 / 64.2 / **149.8** | 19.2% | 19.5% | 78.3 / 42.7 / 55.3 [53.0, 57.5] | chỉ 42 |
| zero-shot Qwen2.5-VL-7B | 5.5 / **thiếu** / 25.6 / 29.0 (file ghi sai prompt_style) | 42.9% | có | 31.6 / 57.1 / 40.7 | greedy, tất định |
| VSPS main | 7.0 / 22.1 / 30.9 / 17.3 (s42); có cả s43 và s44re | 44.6% | có | 39.0 / 39.7 / 39.3 (3 seed) | 42/43/44 ✓ |
| v3_s42 | **– (chưa chạy short)** | – | 55.7% | 37.0 / 43.3 / 39.9 (chỉ trong README v3, không có trong `object_prf_dual.md`) | chỉ 42 |
| v2raw_s42 | – | – | – | 38.1 / 42.2 / 40.1 (**preds không có trong repo**) | chỉ 42 |
| fuse2 (phương pháp mới) | – | – | – | – | chưa train |
| VCD | chỉ có preds (short + detailed), chưa có JSON n-gram | – | – | 40.6 | 1 lần chạy |

SPICE, CLIPScore và POPE: không hệ thống nào có. Không file nào lưu CI của CIDEr.

---

## 2. Baseline reviewer sẽ đòi

Xếp theo rủi ro bị reviewer bắt lỗi chia cho chi phí, cao nhất trước. GPU-giờ tính trên RTX 3090. Mốc dùng để ước lượng: SFT 7,2k dòng × 2 epoch mất 3,6 giờ (log v2raw); eval 558 ảnh mất khoảng 0,2 giờ ở short và 0,5 giờ ở detailed.

| # | Baseline | Đã có code? | Khả thi ≤ 10 GPU-h? | Rủi ro reviewer | Ghi chú |
|---|---|---|---|---|---|
| 1 | **SFT nhiều tham chiếu thuần** (mỗi ảnh 5 dòng, mỗi dòng 1 caption) | Gần như có: `build_gold_sft.py` thiếu `--select all`, khoảng 5 dòng code | Có. Khoảng 18,5k dòng: 1 epoch mất khoảng 4-5 giờ, cộng 0,7 giờ eval | **Rất cao.** Đây là câu hỏi đầu tiên khi bài tuyên bố fuse | Phải so ở cùng số bước tối ưu, và ở cùng số epoch |
| 2 | **Tag trong prompt** (RAM++ hoặc Grounding DINO → tên đối tượng tiếng Việt → prompt) | Không | Có. RAM++ trên 558 ảnh dưới 0,1 giờ; sinh caption zero-shot và P1+tag khoảng 1,5 giờ | **Cao.** Rẻ và hiển nhiên | Ánh xạ tag sang tiếng Việt dùng `coco80_vi.json` và lexicon 113 lớp. Grounding DINO cần danh sách từ vựng đầu vào, nên chọn RAM++ |
| 3 | **PatchGate** (2608.21819, không cần huấn luyện, logit-lens + chỉnh logit) | Không. Code công khai: UNVERIFIED | Có về GPU (khoảng 1,5 giờ). Dev 1-2 ngày | **Cao.** Đây là đối thủ gần nhất về trục tồn tại | Khó: tên đối tượng tiếng Việt bị tokenizer của Qwen tách thành nhiều token |
| 4 | **GRIT chạy lại** trên cùng evaluator | Không. Code GRIT-vicap công khai | Nếu có checkpoint KTVIC thì khoảng 0,2 giờ; nếu phải train lại thì có thể vượt 10 giờ (UNVERIFIED) | Cao cho bảng n-gram | R2_01 xếp mục này vào nhóm bắt buộc |
| 5 | **RLAIF-V** | Không. Repo có DPO (`train_stage2.py --stage dpo`, `build_dpo_data.py`) | Bản đầy đủ thì không (sinh nhiều ứng viên + gán nhãn bằng mô hình mở cho 3,7k ảnh, vượt xa 10 giờ). Bản "lite" (P1 + DPO trên cặp do verifier tạo) thì có, khoảng 4-5 giờ | Trung bình-cao với bài về ảo giác | Phải ghi rõ đây là biến thể kiểu RLAIF-V, không phải tái lập |
| 6 | **Salience-LLaVA** (2608.28218) | Không | Không (cần QAGNet, YOLO-World và caption Janus-Pro) | Trung bình (preprint, chưa có venue) | Thay bằng ablation "chỉ dùng salience" như R2_03 §101 đề xuất: SFT khoảng 3,6 giờ |
| 7 | **OPERA** | Không (code gốc chỉ cho LLaVA/InstructBLIP/MiniGPT-4) | Có về GPU (beam 5 ở detailed khoảng 3 giờ). Port sang Qwen2.5-VL tốn công | Thấp, vì VCD đã có (`baselines.py --method vcd`) | Chỉ làm nếu còn thời gian. Self-Correction đã có code nhưng chưa có preds: khoảng 1,5 giờ |

---

## 3. Độ chặt thống kê

| Hệ thống | Seed đang có | Cần chạy thêm | GPU-h |
|---|---|---|---|
| P1 (baseline chính) | 42 | **43, 44** | 2 × (1,5 train + 0,7 eval) ≈ 4,4 |
| fuse2 | chưa có (42 chờ; 43/44 đã xếp hàng) | 42/43/44, eval **cả short lẫn detailed** | đã xếp hàng; kiểm tra lại là job eval có chạy cả 2 mode |
| SFT nhiều tham chiếu | – | 42 trước; 43/44 nếu kết quả sát fuse2 | 5 + (10 nếu cần) |
| E5 (tự huấn luyện từ P1) | – | 3 seed | khoảng 8 mỗi seed (theo 06) |
| v2raw / v3 | 42 | Không chạy thêm. Hạ xuống làm ablation một seed và ghi rõ như vậy. Cần chép preds v2raw từ máy remote về repo | 0 |
| VSPS main | 42/43/44 | đủ | 0 |
| Zero-shot, VCD | greedy | không cần | 0 |
| Human eval | 50 × 2 | 200 × 3 rater, có P1 và hệ thống mới | 0 GPU, nhưng tốn công người |

Kiểm định: mọi khẳng định "A > P1" phải dùng `score_ci.py` paired (CIDEr, CHAIR_i). Cần thêm paired bootstrap cho object F1 trong `object_prf.py`. Báo mean ± sd qua 3 seed.

---

## 4. Tổng quát hóa sang dataset thứ hai

| Lựa chọn | Code hiện tại đo được chưa? | Cần làm gì | Chi phí |
|---|---|---|---|
| **UIT-ViIC** (3.850 ảnh COCO chủ đề thể thao, 5 caption/ảnh, file định dạng COCO) | Gần như có. `evaluate.py` và `train_stage2.py` đọc `$NCS_DATA/datasets/ktvic/{split, images/}`, nên chỉ cần trỏ `NCS_DATA` sang một thư mục có `datasets/ktvic` → UIT-ViIC (symlink), **không phải sửa code** | Tải dataset; tải ảnh COCO bằng `download_coco_images.py`; kiểm tra lexicon CHAIR-vi có các lớp thể thao (vợt, gậy...). Bài gốc dùng PyVI, thang 0-1, nên phải báo theo protocol của mình và chạy lại baseline trên cùng evaluator | Transfer (P1, fuse2, zero-shot) khoảng 0,5 giờ. SFT trong miền (P1-UIT, fuse2-UIT) khoảng 4 giờ |
| UIT-OpenViIC | Như trên | Có rò rỉ: 401/558 ảnh test KTVIC trùng gần với train OpenViIC. Chỉ dùng làm tập test | khoảng 1 giờ |
| COCO dịch sang tiếng Việt | Không có tham chiếu tiếng Việt | Phải dịch máy 25k caption, kéo theo câu hỏi về chất lượng bản dịch. Không khuyến nghị | — |
| COCO tiếng Anh (Karpathy, `data/datasets/karpathy`) | CHAIR/P/R tiếng Việt trên COCO-5000 đã có cho zero-shot, VSPS s42/43/44 và VCD (`coco*_scores.json`). Chưa có P1 và fuse2 | Chạy `coco_probe.py` cho P1 và fuse2 (chỉ CHAIR, vì tham chiếu là tiếng Anh, không chấm n-gram được) | khoảng 1 giờ mỗi hệ thống |

Khuyến nghị: UIT-ViIC làm dataset thứ hai có n-gram, cộng COCO-5000 cho CHAIR. Tập KTVIC đã lọc trùng (543 ảnh, `data/dedup`) đã có cho P/R.

---

## 5. Gold đối tượng do người gán (E6)

| Thành phần | Trạng thái |
|---|---|
| `object_gold_sample.py` | Xong. Đã commit `sample.json`: 300 ảnh test, phân tầng theo số đối tượng trong tham chiếu, seed 42 |
| `annotate.html` + `thumbs/` | Xong, đã commit |
| `object_gold_score.py` | Xong. `--self-check` qua. Tính κ giữa 2 người gán, gold `agreed`/`union`/có trọng tài, P/R/F1 theo exact và lenient |
| `annot_claude.json` (chưa track) | **Nhãn do AI tạo**: `annotator: "claude_AI"`, `ai_produced: true`, 300/300 ảnh, trung bình 7,2 lớp/ảnh. Claude xem từng thumbnail rồi tick. **Không được gọi là human gold**, không được dùng làm người gán A/B hay trọng tài, không được dùng để tính κ "giữa người với người" |
| Nhãn người | **0/300.** Đây là đường găng của C1 và mọi tuyên bố về recall |

Đề xuất:
- Không commit `annot_claude.json` vào bộ gold. Nếu giữ lại thì đổi tên thành `draft_ai_*.json`, và chỉ dùng cho hai việc: tiền điền giao diện (nhưng như vậy gây anchoring bias, nên tốt nhất là không dùng), hoặc làm một hàng "LLM-as-annotator so với người" trong bài.
- `object_gold_score.py` hiện **không kiểm tra** trường `ai_produced`. Nên thêm một guard từ chối file có `ai_produced: true` (khoảng 3 dòng).
- Cần 2 người gán thật và 1 trọng tài. Ước lượng khoảng 300 ảnh × 1-2 phút, tức 5-10 giờ mỗi người.

---

## 6. Danh sách job GPU theo thứ tự ưu tiên (để thêm vào queue remote; **chưa xếp hàng job nào**)

Tiền tố chung: `export NCS_DATA=...; E="python3 scripts/evaluate.py --model qwen2.5-vl-7b"`. Mỗi lần eval chạy cả `--prompt short` và `--prompt detailed`.

| # | Tên job | Lệnh (phác) | GPU-h |
|---|---|---|---|
| 1 | fuse2_s42/s43/s44 (đã xếp hàng) | đảm bảo có eval hai mode: `$E --adapter runs/fuse2_s4X --prompt {short,detailed} --name fuse2_s4X-{mode}` | (đã tính) + 0,7/seed nếu thiếu |
| 2 | p1_s43, p1_s44 | `train_stage2.py --stage sft --data $NCS_DATA/stage2_gold --out runs/p1_s4X --epochs 2 --seed 4X` rồi `$E` hai mode | 4,4 |
| 3 | multiref_s42 | (CPU) thêm `--select all` vào `build_gold_sft.py`, build ra `stage2_multiref`; `train_stage2.py --stage sft --data stage2_multiref --epochs 1 --seed 42` rồi `$E` | 5,5 |
| 4 | tags_ramxx | (dev) `scripts/tags_baseline.py`: RAM++ → tag tiếng Việt → prompt; chạy cho zero-shot và cho P1 | 1,5 |
| 5 | uitviic_transfer | shim `NCS_DATA_UIT` rồi `$E --split test.json` cho zero-shot, P1 và fuse2_s42 (chỉ short) | 0,5 |
| 6 | coco_p1_fuse2 | `coco_probe.py` (detailed + short) cho P1 và fuse2_s42 → `score_coco_probe.py` | 2,0 |
| 7 | patchgate_reimpl | (dev) logit-lens inventory + chỉnh logit trên Qwen2.5-VL-7B, test 558 ảnh, hai mode | 1,5 |
| 8 | uitviic_indomain | `build_gold_sft.py` trên UIT train (first, rồi fuse 2) → SFT → eval | 4,0 |
| 9 | rlaifv_lite_s42 | `train_stage2.py --stage dpo --adapter runs/p1_s42 --data <cặp do verifier tạo>` rồi `$E` | 5,0 |
| 10 | salience_only_s42 | (CPU) dựng target chỉ theo salience → SFT → eval | 4,3 |
| 11 | selfcorrect | `baselines.py --method selfcorrect --prompt {short,detailed}` | 1,5 |
| 12 | multiref_s43/s44 | chỉ chạy nếu job 3 cách fuse2 trong khoảng CI | 11,0 |
| 13 | E5_s42/43/44 | theo 06 §4 | khoảng 24 |

Tổng các job 2-11 (chưa tính E5 và job 12): khoảng **34 GPU-giờ**.

Việc CPU nên làm trước, không tốn GPU:
- (a) Chấm lại `zeroshot-short`, `off4090sft-short`, `roundA-short` với `--prompt short` để có METEOR.
- (b) Chạy `score_ci.py` cho từng cặp so với P1 rồi commit JSON.
- (c) Chạy `evaluate.py` cho `vcd-short.preds.json`.
- (d) Đối chiếu lại số GRIT.
- (e) Chép preds v2raw về repo.
