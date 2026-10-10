# 06. Bơm đồ thị (scene graph / KG) vào transformer và LVLM: bằng chứng 2025-2026 và thiết kế cho Qwen2.5-VL/Qwen3-VL trên một RTX 3090

Ngày: 2026-10-10. Agent KG-plan 06.
Nguồn: trang `arxiv.org/abs/<id>` (mở từng ID, lấy tiêu đề, ngày, comment/venue), bản HTML toàn văn trên arXiv cho các bảng số, config HF của hai backbone, và repo VSPS cho số đo bộ nhớ và thời gian. arXiv API, Semantic Scholar và OpenAlex trả 429 trong phiên này (các agent khác đang chạy song song), nên venue chỉ lấy từ comment trên arXiv. Mục nào chưa kiểm được thì nằm ở §8.

---

## 0. Kết luận ngắn

1. **Bằng chứng 2025-2026 nghiêng hẳn về một phía.** Khi đồ thị nhỏ (vài chục nút) và có nhãn văn bản, **tuyến tính hóa thành văn bản rồi LoRA/QLoRA** ngang hoặc hơn các cách dùng GNN, graph-token hay Q-Former. Lợi thế của graph token chủ yếu là **nén ngữ cảnh**, không phải độ chính xác. Một scene graph caption có khoảng 10-30 bộ ba, tức vài trăm token (ước tính), nên không cần nén.
2. Cách bơm cấu trúc **rẻ nhất mà có tác dụng** là **sửa attention/position trên chính token văn bản của đồ thị** (mask theo topology, bias theo khoảng cách đồ thị, hiệu chỉnh position ID). Họ này gồm NAG, GTLM, GaLA, Graph-KV. Tham số thêm khoảng 10^3-10^5. Lợi ích rõ trên tác vụ *cấu trúc*, còn trên SceneGraphs (tác vụ ngữ nghĩa) thì gần bằng không.
3. Cross-attention adapter (GMT) thắng prefix trên KG completion. Nhưng nó phải sửa kiến trúc decoder của Qwen-VL, đắt về bộ nhớ, và không có bằng chứng nào cho captioning. **Không khuyến nghị** cho 3090.
4. **Khuyến nghị:** thiết kế 3 tầng, chạy ablation theo thứ tự.
   **G0**: đồ thị đã kiểm chứng tuyến tính hóa thành văn bản tiếng Việt, có thẻ trạng thái kiểm chứng. Đây là mặc định, chỉ cần QLoRA sẵn có.
   **G1**: G0 cộng mask/bias attention theo topology, khoảng 6-10K tham số.
   **G2**: G0 cộng 8-16 graph token từ một Graph Transformer nhỏ, khoảng 20-25M tham số, theo kiểu "text + soft token" của G-Retriever.
   Chỉ giữ G1/G2 nếu chúng thắng G0 qua đủ 3 seed **và** qua bài kiểm "đồ thị xáo trộn".
5. **Về novelty:** cách bơm **không nên là đóng góp chính** của bài. Bơm đồ thị vào bộ sinh caption là hướng đã trưởng thành (xem 11_). Reviewer năm 2026 sẽ đòi baseline văn bản, và baseline văn bản thường thắng. Phần còn có thể mới là **dùng trạng thái kiểm chứng (SUPPORTED/UNCERTAIN) làm tín hiệu cấu trúc** (thẻ, bias, cổng), áp cho tiếng Việt. Phần này chưa được quét novelty đầy đủ (§8).

---

## 1. Sáu cách bơm đồ thị (phân loại để ablation)

| Mã | Cách bơm | Đại diện đã mở | Tham số thêm | Thay đổi kiến trúc Qwen-VL |
|---|---|---|---|---|
| **T** | Tuyến tính hóa văn bản (bộ ba, JSON, danh sách kề) trong prompt, rồi LoRA | Talk like a Graph (2310.04560, nền), Lost in Serialization (2511.10234, ICML 2026 WS), SceneGraphVLM (2605.13667, định dạng TOON) | 0 (ngoài LoRA) | Không |
| **S** | T cộng thiên kiến cấu trúc trong attention/PE: mask topology, bias SPD/RRWP/Laplacian, sửa position ID, RoPE theo phổ Laplacian | NAG (2601.22657), GTLM (2605.10247), GaLA (2606.15633, KDD 2026), Graph-KV (2506.07334), WIRE (2509.22259), UniGTE (2510.16885, NeurIPS 2025), Attention Mechanisms Perspective (2505.02130, ICML 2025) | ~10^3-10^5 | Mask 4D float qua SDPA; sửa `position_ids` 3×L của MRoPE |
| **P** | GNN hoặc graph transformer, rồi projector, rồi soft token ở đầu vào | GraphToken (2402.05862, nền), LLaGA (2402.08170, nền), G-Retriever (2402.07630, nền), KG→KGE token (2505.07554), MLaGA (2506.02568), 3DGraphLLM (2412.18450, 3D) | 5-25M | Không (dùng `inputs_embeds`) |
| **Q** | Q-Former trên nút/đồ thị, cho ra K token cố định | GraphGPT-o (2502.11925; có ghi CVPR 2025 nhưng chưa xác minh), Graph4MM MM-QFormer (2510.16990, ICML 2025), DyGEnc (2505.03581) | 10-40M | Không |
| **X** | Cross-attention adapter (graph memory, gate khởi tạo 0) chèn vào các tầng | GMT "Beyond Prefixes" (2510.08966), GNP (2309.15427, AAAI 2024, nền) | Lớn nếu thêm Wq/k/v/o mới (~51M/tầng ở d=3584). Nhỏ nếu LoRA trên trọng số dùng chung | Có (sửa decoder layer) |
| **C** | Đồ thị làm *đầu ra trung gian*: mô hình tự sinh scene graph rồi viết caption (CoT), hoặc đồ thị chỉ dùng lúc huấn luyện (DPO/RL) | SaGe "Scene Graph Thinking" (2607.05716, ICML 2026), SceneAlign (2601.05600), CCoT (CVPR 2024, nền) | 0 | Không |

---

## 2. Bằng chứng ablation 2025-2026 (số lấy từ bảng trong toàn văn)

### 2.1 Văn bản và graph token / GNN, đối đầu trực tiếp

| Bài | Thiết lập | Kết quả | Ý nghĩa |
|---|---|---|---|
| **NAG** (2601.22657, Qwen3-0.6B) | SceneGraphs (GraphQA) / ExplaGraphs / WebQSP | Qwen3-LoRA văn bản **83,71** / 62,09 / 44,37; GraphToken_G (≈G-Retriever) 68,37 / 65,52 / 40,56; NAG-LoRA **83,82** / 82,49 / 55,25 | Trên **scene graph**, văn bản + LoRA cao hơn graph token 15 điểm. Mask + PE của NAG gần như không thêm gì (+0,1). Lợi ích của S nằm ở ExplaGraphs/WebQSP |
| **DyGEnc** (2505.03581, Llama-3.2-3B, LoRA r=8) | STAR QA, chuỗi scene graph văn bản | Fine-tune với prompt văn bản **0,99**; Graph Transformer + Q-Former (1 token) **0,89** ở 0,03× ngữ cảnh; bản văn bản 8B bị OOM trên A100 80GB | Q/P đổi khoảng 10 điểm lấy 30× nén. Nén chỉ đáng khi đồ thị dài |
| **Graph4MM** (2510.16990, ICML 2025; OPT-125M) | Tóm tắt mục WikiWeb2M, CIDEr | Subgraph văn bản+ảnh 0,7790; cộng embedding GCN **0,6326** (giảm); cộng graph token 0,7736; cộng node token 0,7651; Hop-Diffused attention (S) **0,7831** | **GNN làm "một modality riêng" làm hại** sinh văn bản. Bias cấu trúc trong attention chỉ nhích nhẹ (+0,004 CIDEr) |
| **Graph-MLLM** (2506.10282; Qwen-VL-7B, LLaVA-1.5-7B) | 6 bộ đồ thị đa phương thức | MLLM fine-tune **không có cấu trúc** là tốt nhất trên cả 6 bộ (vd Movies 54,18 so với MLaGA 49,78). Thêm text láng giềng: −2,52 đến +0,58; thêm text+ảnh láng giềng: giảm trên cả 6 bộ (Movies −8,30) | Với fine-tune mạnh, cấu trúc thêm vào thường trung tính hoặc có hại. Cần thiết kế để mô hình **chọn lọc** |
| **CLEGR** "A Graph Talks, But Who's Listening?" (2508.20583; Llama3-8B, Phi3) | Node classification + suy luận tổng hợp | Soft-prompt không đồ thị ngang GLM ở Computers/Photo/History/Arxiv (vd 74,34 so với G-Token 76,13). Trên CLEGR, GLM "không khai thác được structural encoder" | **Cảnh báo phương pháp luận:** phải có đối chứng "đồ thị xáo trộn hoặc rỗng" thì mới kết luận đồ thị có tác dụng |
| **GraphInfer-Bench** (2606.11562) | 5 tác vụ suy luận vùng đồ thị | Graph-token (LLaGA, GraphGPT…) T4 ≤ 0,102; Graph2Text SFT Llama-3-8B T4 0,390, T3 0,766. Thêm tiêu đề láng giềng dạng văn bản nâng T4 của LLaGA từ 0,10 lên 0,56 | Văn bản > graph token, kể cả khi encoder có thông tin |
| **GraphGPT-o** (2502.11925; DreamLLM) | Sinh đa phương thức trên MMAG | Linearization ("Hard") và aligner Q-Former ("Soft") **mỗi bên thắng một vài metric** (ART500K CLIP-I2 77,62 so với 72,64; perplexity 347 so với 60). Thay aligner bằng GNN thì kém (CLIP-I2 65,53, PPL 599) | Q-Former hơn GNN thuần, nhưng không áp đảo văn bản |

### 2.2 Khi nào cấu trúc tường minh thắng

| Bài | Kết quả | Điều kiện |
|---|---|---|
| **GTLM** (2605.10247; Llama-3.2-1B + LoRA; +173K tham số bias = 0,015%) | GraphQA Shortest Path 90,1 so với GraphToken 63,8; needle-in-a-graph 98,0% so với LLM văn bản 8,5% (N=128); bỏ bias Magnetic Laplacian làm Edge Count rơi từ 57,2 xuống 8,9 | Tác vụ **thuần cấu trúc**, đồ thị dài. Caption ít khi cần đếm đường đi |
| **GMT** (2510.08966; Alpaca-7B đóng băng, 32 memory token, cross-attn ở tầng 25-32, LoRA r=64) | FB15k-237 MRR 0,488; thay cross-attn bằng prefix còn 0,425 | KG completion, không phải sinh văn bản dài |
| **3DGraphLLM** (2412.18450; LLaMA3-8B) | Có cạnh ngữ nghĩa (k=2) so với không có (k=0): Scan2Cap C@0.5 85,6 so với 80,0; ScanRefer 54,3 so với 52,0. Bộ ba và chuỗi phẳng gần bằng nhau (Scan2Cap 85,6 so với 87,2). 800 token/cảnh so với 10.400 của GPT4Scene | **Quan hệ** giúp caption, còn *dạng* biểu diễn quan hệ ít quan trọng. Token hóa đáng làm vì đồ thị 3D có khoảng 100 vật |
| **G-Retriever** (2402.07630, 2024, nền; Llama2-7B) | SceneGraphs: G-Retriever+LoRA 0,8683 so với LoRA 0,7862. WebQSP: bỏ graph encoder −22,5%, bỏ textualized graph −19,2% | **Văn bản + soft token kết hợp** tốt hơn từng thứ riêng. Đây là cơ sở cho G2 |
| **SaGe** (2607.05716, ICML 2026; Qwen2.5-VL-3B/7B) | SFT với CoT scene graph dạng văn bản: V* từ 79,1 (chỉ đáp án) lên 83,2; thêm GRPO với reward nút lên 89,0 | Đồ thị **tự sinh dạng văn bản** (cách C) có tác dụng trên chính Qwen2.5-VL. Không báo POPE/CHAIR |
| **KG-ViP** (2601.11632; Qwen2.5-VL-7B) | Bỏ bước hợp nhất SG + commonsense graph: LLM-J 60,40 xuống 58,11 (FVQA 2.0+) | Bơm qua prompt (không thấy projector). Chưa rõ hình thức bơm (§8) |

### 2.3 Năm điều rút ra

1. **Scene graph nhỏ thì dùng văn bản cộng LoRA.** NAG SceneGraphs, DyGEnc, Graph4MM, GraphInfer, Graph-MLLM đều cùng chiều. GNN-as-modality còn làm giảm chất lượng sinh văn bản (Graph4MM: CIDEr 0,779 xuống 0,633).
2. **Quan hệ có ích, định dạng thì gần như không** (3DGraphLLM: triplet ≈ flat). Nhưng LLM fine-tune **nhạy với cách tuyến tính hóa** (Lost in Serialization). Vì vậy cần cố định một định dạng và báo độ nhạy theo 2 định dạng.
3. **Bias cấu trúc trong attention rẻ và an toàn.** Nó có thể co về mô hình gốc khi bias bằng 0 (GTLM chứng minh điều này). Lợi ích trên tác vụ ngữ nghĩa thì nhỏ.
4. **Graph token chỉ đáng khi cần nén**, hoặc khi *kết hợp* với văn bản (G-Retriever). Graph token đơn độc thì luôn thua văn bản trong các bài 2025-2026 kể trên.
5. **Phải chứng minh mô hình thực sự đọc đồ thị** (CLEGR). Cần có đối chứng: đồ thị rỗng, xáo trộn nhãn nút, xáo trộn cạnh, và đồ thị của ảnh khác.

---

## 3. Đặc thù kỹ thuật của Qwen2.5-VL và Qwen3-VL (ảnh hưởng đến lựa chọn bơm)

Config lấy từ `huggingface.co/<model>/raw/main/config.json` ngày 2026-10-10:

| | Qwen2.5-VL-7B-Instruct | Qwen3-VL-8B-Instruct |
|---|---|---|
| LLM | d=3584, FFN 18944, 28 tầng, 28 head, 4 KV head | d=4096, FFN 12288, 36 tầng, 32 head, 8 KV head, head_dim 128 |
| ViT | 32 tầng, d=1280 | 27 tầng, d=1152, **DeepStack** bơm đặc trưng ViT tầng [8,16,24] vào các tầng đầu LLM (2511.21631) |
| Vị trí | MRoPE 3 trục (t,h,w) (2502.13923) | Interleaved-MRoPE |

Hệ quả:
- **P/Q** chỉ cần ghép `inputs_embeds`, thay embedding của các placeholder `<|graph_pad|>` bằng output projector. Đây là cùng cơ chế mà model dùng để chèn visual token, nên không phải sửa model.
- **S** cần một mask attention 4D dạng float, tức là `attn_implementation="sdpa"`. Repo đang dùng sdpa, còn flash-attn không nhận bias cộng. Với L khoảng 1.000 token thì mask 1×1×L×L tốn khoảng 2 MB nếu dùng chung cho mọi head; bias riêng theo head là 28×L² ≈ 56 MB/tầng nếu materialize (ước tính). Sửa position ID nghĩa là sửa `get_rope_index`: token văn bản dùng cùng chỉ số trên cả 3 trục MRoPE, nên có thể đặt lại thành chỉ số "theo nút" như NAG/GTLM.
- **DeepStack của Qwen3-VL** là đường bơm "đặc trưng phụ vào tầng sớm" có sẵn, và là ứng viên tự nhiên cho graph token kiểu residual. **Đây là ý tưởng chưa có bằng chứng** (§8). Không nên đưa vào kế hoạch chính.
- **X** phải chèn module mới vào `Qwen2_5_VLDecoderLayer`. Code dễ vỡ qua các phiên bản transformers, và gradient checkpointing với QLoRA thêm rủi ro.

---

## 4. Thiết kế khuyến nghị: VGI (Verified-Graph Injection), 3 tầng

### 4.1 Đầu vào đồ thị
Mỗi ảnh có một đồ thị gồm nút (thực thể, thuộc tính) và cạnh (quan hệ, hành động). Mỗi nút và mỗi cạnh mang trạng thái kiểm chứng ∈ {SUPPORTED, UNCERTAIN}; REJECTED bị loại. Kèm theo là độ tin cậy p từ verifier. Nguồn đồ thị lúc **huấn luyện** là mệnh đề VSPS. Nguồn lúc **suy luận** phải rẻ, xem §6 trục "nguồn đồ thị".

### 4.2 G0: văn bản có thẻ trạng thái (mặc định)
```
<sg>
[n1] người (S) | [n2] xe máy (S) | [n3] mũ bảo hiểm (U) | [n4] màu đỏ (S)
(n1, đang lái, n2)(S) (n1, đội, n3)(U) (n2, có màu, n4)(S)
</sg>
```
- Mỗi nút dùng ID ngắn, bộ ba sắp theo nút, nhãn tiếng Việt, và thẻ S/U. Thẻ U tương ứng với hành vi trung tính hóa đã có trong VSPS.
- Kích thước: khoảng 15 nút và 20 cạnh. Ước tính 250-450 token Qwen; con số này **chưa đo** và cần đo bằng tokenizer trên 100 ảnh.
- Tham số thêm: 0. Dùng QLoRA sẵn có (r=16, α=32, q/k/v/o/gate/up/down phía ngôn ngữ, NF4, sdpa, 512 visual token, theo `scripts/train_stage2.py`).
- Số tham số LoRA tính từ config: Qwen2.5-VL-7B có r·Σ(in+out)·L = 16·90.112·28 ≈ **40,4M**. Qwen3-VL-8B có 16·75.776·36 ≈ **43,6M**.

### 4.3 G1: G0 + attention có cấu trúc (S)
- **Mask:** token của nút i chỉ nhìn được (a) chính nút i, (b) các nút kề i, (c) toàn bộ ảnh và instruction. Token caption phía sau nhìn được mọi thứ (causal). Cách này giống NAG/Graph-KV, chỉ áp trong khối `<sg>`.
- **Bias:** b[h, bucket(SPD(i,j))] học được, cộng một bias riêng cho cạnh U so với S. Bias trạng thái này là phần có thể mới (§8).
- **Position:** đặt lại position ID trong `<sg>` để mỗi bộ ba bắt đầu từ cùng một offset (NAG/GTLM). Mục đích là giảm suy giảm attention của RoPE khi hai nút kề nhau nằm xa trong chuỗi (GaLA).
- Tham số: 28 tầng × 28 head × (8 bucket SPD + 2 trạng thái) ≈ **7,8K** (Qwen2.5). Với Qwen3-VL là 36 × 32 × 10 ≈ 11,5K. Khởi tạo bằng 0 để G1 ≡ G0 lúc bắt đầu.
- Bộ nhớ thêm: dưới 0,3 GB (mask và bias; ước tính). Lưu ý: phải tắt mọi đường flash-attn.

### 4.4 G2: G0 + graph token (P, kiểu G-Retriever)
- Embedding nút và cạnh = mean-pool embedding token (đóng băng) của nhãn tiếng Việt, cho ra 0 tham số mới. Tiếp theo là Linear 3584→512, cộng embedding trạng thái S/U và log p, rồi 2 tầng Graph Transformer (d=512, 8 head, bias SPD). Sau đó attention-pool ra K=8 token, rồi MLP 512→3584→3584. Các token này đặt trước `<sg>` văn bản.
- Tham số (ước tính): proj vào 1,8M + GT 2 tầng khoảng 6,3M + MLP ra khoảng 14,7M ≈ **23M**. Huấn luyện bằng bf16 + AdamW fp32 tốn khoảng 23M × 14 B ≈ 0,32 GB.
- Huấn luyện 2 pha (theo GraphGPT/LLaGA). Pha 1: chỉ projector, tác vụ "đọc lại đồ thị" (graph→text), khoảng 0,5 epoch. Pha 2: projector + LoRA trên caption.
- **Biến thể Q** (Q-Former 2 tầng, K=16 query, khoảng 10M) chỉ chạy nếu G2 thắng G0. Mục đích là thử nén cho đồ thị KG ngoài lớn (ConceptNet subgraph), không dùng cho scene graph nhỏ.

### 4.5 Không khuyến nghị
- **X (cross-attention):** không có bằng chứng cho captioning, sửa decoder, tốn nhiều bộ nhớ và nhiều công kỹ thuật.
- **GNN thay hẳn văn bản:** Graph4MM, NAG và DyGEnc đều cho thấy nó thua văn bản.
- **Bơm đồ thị qua DeepStack** trước khi G0/G2 có kết quả.

### 4.6 Ngân sách trên RTX 3090 (24 GB)

| Cấu hình | Tham số train | Đỉnh VRAM | Thời gian/run SFT |
|---|---|---|---|
| Đường cơ sở VSPS (đo trong repo) | 40,4M LoRA | 4-bit + 512 visual token chạy tới 19,15 GB khi có cả pass reference của DPO (docstring `train_stage2.py`). SFT thấp hơn | 7,3 s/it × 1.800 step ≈ **3,6 h** (đo, ghi trong research_wall/05) |
| G0 | 40,4M | **+~0,5 GB** (ước tính: khoảng 400 token thêm; logits fp32 152k vocab ≈ 0,6 MB/token, cộng checkpoint activation) | +15-30% (độ dài chuỗi tăng từ khoảng 700 lên 1.100; ước tính) |
| G1 | 40,4M + 7,8K | G0 + <0,3 GB | ≈ G0 (sdpa có mask có thể chậm hơn 10-20%; ước tính) |
| G2 | 40,4M + 23M | G0 + ~0,4 GB | G0 + pha 1 khoảng 0,5 h |
| Qwen3-VL-8B (mọi biến thể) | 43,6M + … | **chưa đo**. Trọng số 4-bit nặng hơn 7B khoảng 1 GB, 36 tầng. Có thể phải hạ visual token xuống 384 | ước tính ×1,3 |

Mọi ô ghi "ước tính" phải được đo bằng `torch.cuda.max_memory_allocated` trên 20 step trước khi đưa vào bài.

---

## 5. Hướng tích hợp với VSPS (để không mâu thuẫn với câu chuyện chính)
- VSPS hiện tại là **đồ thị lúc huấn luyện, không có đồ thị lúc suy luận** (single-pass). Bơm đồ thị lúc suy luận làm mất claim "một lượt, rẻ" và cần một nguồn đồ thị lúc test.
- Vì vậy kế hoạch nên có **hai chế độ**, báo cả hai:
  - (a) **Graph-conditioned**: G0/G1/G2, đồ thị lấy từ nguồn rẻ lúc test.
  - (b) **Graph-as-CoT** (cách C, kiểu SaGe/CCoT): SFT để mô hình *tự sinh* `<sg>…</sg>` rồi mới viết caption. Huấn luyện dùng đồ thị VSPS đã kiểm chứng làm target, nên lúc test không cần pipeline ngoài.
  Chế độ (b) cũng là cách bơm có bằng chứng 2026 mạnh nhất trên Qwen2.5-VL (SaGe, V* từ 79,1 lên 83,2 nhờ SFT CoT).
- **Graph dropout** khi huấn luyện chế độ (a): bỏ `<sg>` với xác suất 0,3. Mô hình vẫn chạy khi không có đồ thị, và có thể đo được "đồ thị đóng góp bao nhiêu".

---

## 6. Kế hoạch ablation (thứ tự chạy, chi phí)

Dữ liệu: tập SFT VSPS khoảng 3.560 mục KTVIC. Thêm UIT-OpenViIC nếu đã có đồ thị. Metric: CHAIR-vi, object recall/precision (gold 300 ảnh), graph-recall theo loại (ý 1 của 11_), CIDEr/BLEU (tham khảo), tỷ lệ output không phải tiếng Việt, và độ dài. Mỗi run SFT khoảng 3,6-4,7 h.

| Pha | Run | Câu hỏi | Seed | GPU-h (ước tính) |
|---|---|---|---|---|
| A. Có cần đồ thị không | A0 VSPS gốc (không `<sg>`); **A1 = G0**; A2 G0 với đồ thị **xáo trộn giữa các ảnh**; A3 G0 với `<sg>` rỗng | Lợi ích có đến từ nội dung đồ thị không? (đối chứng CLEGR) | A0, A1 × 3; A2, A3 × 1 | ~32 |
| B. Định dạng văn bản | B1 bộ ba; B2 JSON; B3 câu tự nhiên; B4 G0 bỏ thẻ S/U | Độ nhạy với tuyến tính hóa; thẻ trạng thái có tác dụng không | 1 | ~18 |
| C. Cấu trúc trong attention | C1 G1 chỉ mask; C2 G1 mask + SPD bias; C3 C2 + bias trạng thái; C4 C3 + sửa position | Đóng góp của S (kỳ vọng nhỏ theo NAG SceneGraphs) | 1, rồi bản tốt nhất × 3 | ~25 |
| D. Graph token | D1 chỉ token (bỏ văn bản); D2 G2 (token + văn bản); D3 Q-Former K=16 + văn bản | Lặp lại phát hiện "token đơn độc thua văn bản; kết hợp thắng" của G-Retriever trên caption tiếng Việt | 1, bản tốt nhất × 3 | ~25 |
| E. Nguồn đồ thị lúc test | E1 đồ thị VSPS đầy đủ (oracle-ish); E2 detector OWLv2/Florence-2 + quan hệ không gian từ bbox; E3 đồ thị tự sinh (chế độ CoT); E4 E2 có nhiễu: bỏ 30% cạnh, thêm 2 vật giả | Độ bền khi đồ thị lúc test rẻ và nhiễu. **Đây là câu reviewer sẽ hỏi đầu tiên** | 1 | ~10 (suy luận) + 4 (CoT SFT) |
| F. Backbone | Cấu hình tốt nhất từ A-D trên Qwen3-VL-8B | Chuẩn ≥2 backbone (00_ §3) | 3 | ~15 |
| G. KG ngoài (tùy chọn) | Thêm cạnh IsA/AtLocation (Wikidata `vi` hoặc ConceptNet) vào `<sg>`, đánh dấu (K) | KG commonsense có giúp hay tăng ảo giác (prior đồng xuất hiện)? | 1 | ~5 |

Tổng: khoảng **130-140 GPU-h** cho toàn bộ. Nếu cắt gọn (A, B4, C3, D2, E, F) thì khoảng **75 GPU-h**, tức 4-5 ngày máy trên một 3090.

Quy tắc giữ hoặc bỏ: một biến thể chỉ được giữ nếu hơn G0 về CHAIR-vi **và** object recall, với bootstrap 95% CI không chứa 0 trên 3 seed. Ngoài ra, A2 (đồ thị xáo trộn) phải kém A1 có ý nghĩa thống kê. Nếu A2 ≈ A1 thì kết luận "mô hình không đọc đồ thị" và dừng nhánh G1/G2.

Kiểm tra bắt buộc trước pha C/D: (i) đo số token `<sg>` thật; (ii) unit test rằng G1 với bias 0 cho logits giống hệt G0 (sai lệch dưới 1e-3); (iii) unit test rằng mask không chặn token caption nhìn ảnh.

---

## 7. Phê bình: tính khả thi, trùng lặp, novelty

- **Khả thi: cao cho G0/G1/C, trung bình cho G2.** G0 chỉ là đổi prompt. G1 cần một hook mask/position khoảng 100-200 dòng. G2 cần collator ghép `inputs_embeds` và huấn luyện 2 pha. Rủi ro lớn nhất là bộ nhớ của Qwen3-VL-8B chưa được đo.
- **Trùng lặp:**
  - "scene graph dạng văn bản trong prompt LVLM" đã có ở CCoT, KG-ViP, SaGe, SceneAlign, nên không mới.
  - "graph token cho MLLM" đã có ở LLaVA-SG (2408.16224, 2024), 3DGraphLLM, MLaGA, GraphGPT-o, nên không mới.
  - "bias cấu trúc trong attention của LLM" đã có ở NAG, GTLM, GaLA, Graph-KV, nên không mới.
  - Tổ hợp *scene graph 2D + LVLM captioner + bias attention* thì chưa thấy trong lần quét này, nhưng lần quét không đầy đủ.
- **Novelty có thể bảo vệ được:**
  - (i) Trạng thái kiểm chứng (S/U, p) làm tín hiệu cấu trúc (thẻ hoặc bias hoặc gate), tức "đồ thị không chắc chắn". Chưa quét riêng.
  - (ii) Đánh giá có đối chứng xáo trộn trên caption tiếng Việt. Đây là phần cần thiết về phương pháp, chưa phải đóng góp.
  - (iii) So sánh hai chế độ graph-conditioned và graph-as-CoT trên tiếng Việt.
  Không nên quảng bá "phương pháp bơm đồ thị mới".
- **Rủi ro diễn giải:** Graph-MLLM và CLEGR cho thấy cấu trúc thêm vào có thể trung tính. Nếu A1 ≈ A0, bài vẫn có kết quả âm có giá trị ("đồ thị đã kiểm chứng giúp ở huấn luyện, không giúp ở suy luận"), nhưng khó lên Q1.

---

## 8. Chưa xác minh / hạn chế

- **Venue:** GraphGPT-o ghi "CVPR 2025" theo kết quả tìm kiếm (OpenMAG trích), nhưng trang arXiv không ghi venue, nên chưa xác minh. KG-ViP ghi "ACL 2026" theo 11_ (Semantic Scholar); bản v3 trên arXiv không ghi venue. LLaVA-SG: không đọc được toàn văn (PDF trả về nhị phân), nên chưa kiểm được ablation "huấn luyện trên văn bản SG không hiệu quả".
- **Bảng G-Retriever:** nhãn của dòng "LoRA" (có textualized graph trong đầu vào hay không) được đọc qua công cụ tóm tắt và có thể sai. Cần mở Bảng 3 của 2402.07630 trước khi trích.
- **Số NAG:** công cụ trích báo một vài ô của cột GraphToken_G bị lệch cột. Cột SceneGraphs không nằm trong các ô bị báo lệch, nhưng vẫn nên kiểm lại trên PDF.
- **Số liệu ước tính, chưa đo:** độ dài token `<sg>`, VRAM thêm của G0/G1/G2, bộ nhớ và thời gian của Qwen3-VL-8B, số tham số của Graph Transformer/MLP (tính tay). Số LoRA 40,4M và 43,6M tính từ config HF, chưa đối chiếu với `print_trainable_parameters()`.
- **Novelty của "bias theo trạng thái kiểm chứng":** chưa quét. Cần tìm kiểu "uncertainty-aware graph attention LLM" và "confidence-weighted scene graph prompt" trước khi claim.
- **DeepStack làm đường bơm graph token cho Qwen3-VL:** chỉ là ý tưởng, không có bài nào đã xác minh làm việc này.
- **TokenMem (2607.22625)** và các bài KG-cross-attention khác chỉ xuất hiện trong kết quả tìm kiếm, chưa mở, nên không dùng làm bằng chứng.
- Không tìm thấy bài 2025-2026 nào so sánh trực tiếp T, P, Q, X **cho image captioning bằng LVLM**. Mọi kết luận ở §2.3 là ngoại suy từ QA trên đồ thị, KG completion, sinh văn bản trên đồ thị đa phương thức (Graph4MM) và 3D captioning (3DGraphLLM).

## Nguồn (đều đã mở trong phiên)
arXiv: [2601.22657](https://arxiv.org/abs/2601.22657) · [2605.10247](https://arxiv.org/abs/2605.10247) · [2606.15633](https://arxiv.org/abs/2606.15633) · [2506.07334](https://arxiv.org/abs/2506.07334) · [2509.22259](https://arxiv.org/abs/2509.22259) · [2510.16885](https://arxiv.org/abs/2510.16885) · [2505.02130](https://arxiv.org/abs/2505.02130) · [2505.03581](https://arxiv.org/abs/2505.03581) · [2510.16990](https://arxiv.org/abs/2510.16990) · [2506.10282](https://arxiv.org/abs/2506.10282) · [2508.20583](https://arxiv.org/abs/2508.20583) · [2606.11562](https://arxiv.org/abs/2606.11562) · [2502.11925](https://arxiv.org/abs/2502.11925) · [2510.08966](https://arxiv.org/abs/2510.08966) · [2412.18450](https://arxiv.org/abs/2412.18450) · [2607.05716](https://arxiv.org/abs/2607.05716) · [2601.05600](https://arxiv.org/abs/2601.05600) · [2601.11632](https://arxiv.org/abs/2601.11632) · [2511.10234](https://arxiv.org/abs/2511.10234) · [2506.02568](https://arxiv.org/abs/2506.02568) · [2602.05576](https://arxiv.org/abs/2602.05576) · [2603.05181](https://arxiv.org/abs/2603.05181) · [2505.07554](https://arxiv.org/abs/2505.07554) · [2412.09094](https://arxiv.org/abs/2412.09094) · [2605.13667](https://arxiv.org/abs/2605.13667) · [2511.21631](https://arxiv.org/abs/2511.21631) · [2502.13923](https://arxiv.org/abs/2502.13923) · nền: [2402.07630](https://arxiv.org/abs/2402.07630), [2402.05862](https://arxiv.org/abs/2402.05862), [2402.08170](https://arxiv.org/abs/2402.08170), [2310.13023](https://arxiv.org/abs/2310.13023), [2402.12984](https://arxiv.org/abs/2402.12984), [2310.04560](https://arxiv.org/abs/2310.04560), [2310.07478](https://arxiv.org/abs/2310.07478), [2309.15427](https://arxiv.org/abs/2309.15427), [2408.16224](https://arxiv.org/abs/2408.16224).
