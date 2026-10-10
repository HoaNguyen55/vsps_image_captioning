# 12. Hàm mục tiêu huấn luyện dùng đồ thị (2025-2026): cái gì đã được chứng minh cho captioning, cái gì còn mở

Ngày: 2026-10-10. Agent 12, kế hoạch KG-captioning.

**Cách xác minh.** Mọi arXiv ID dưới đây được tra bằng arXiv export API (`id_list`, lấy tiêu đề, tác giả, ngày và trường comment). Abstract đọc từ cùng phản hồi đó. Với SceneAlign và SaGe, tôi mở thêm full text HTML trên arxiv.org. Venue lấy theo comment của arXiv, trừ khi ghi khác. OpenAlex và Semantic Scholar trả 429 trong phần lớn phiên (nhiều agent chạy song song), nên tôi dùng web search để *tìm* bài, rồi xác minh lại bằng arXiv API. Mục nào chỉ thấy qua snippet được đưa vào "Chưa xác minh".

Đọc trước: `../research_wall/11_knowledge_graph_captioning.md`, `../research_wall/07_rl_verifiable_rewards.md` (RL cho captioning, đã phủ), `04_graph_hallucination_threats.md` (T5), `17_novelty_redteam.md` (a).

---

## 0. Trả lời ngắn

| Họ hàm mục tiêu | Có cho **captioning** 2025-2026 chưa? | Mức |
|---|---|---|
| (1) Graph-text contrastive alignment | Có cho CLIP/retrieval (compositionality). **Không thấy** bài nào cho bộ sinh caption LVLM | Đã chứng minh cho encoder. **Mở** cho generator, nhưng giá trị thấp |
| (2) Loss nhận biết cấu trúc (trọng số token/cụm theo nút đồ thị) | Có loss theo cụm (HALVA, ICLR 2025) và theo token (2605.21300), nhưng **không dùng đồ thị** | Một nửa. Trọng số theo trạng thái kiểm chứng của nút là **mở** |
| (3) SFT có điều kiện là đồ thị (đồ thị trong đích hoặc trong CoT) | Có cho suy luận và SGG (SaGe ICML 2026, Relation-R1 AAAI 2026, SGG-R³). **Không thấy** cho caption chi tiết | **Mở** cho captioning |
| (4) Cặp DPO sinh từ đồ thị (đổi nút/cạnh làm negative) | SceneAlign (ACL 2026), nhưng cho rationale VQA. HALVA đổi cụm, không qua đồ thị. Với caption: **không thấy** | **Mở một phần**, đang nóng, overlap medium |
| (5) RL/GRPO với reward khớp đồ thị | **Đã có cho captioning**: SC-Captioner (ICCV 2025), FoCUS (EMNLP 2026). Cho SGG: R1-SGG, SceneGraphVLM. Video: SAGA (EMNLP 2026), structured rewards (COLM 2026). Y tế: CheXPO-v2 | **Đã chứng minh, đông đúc**. Không được coi là đóng góp |
| (6) Curriculum theo độ phức tạp đồ thị | Có cho T2I (CompGen 2511.18378). Phased RL cho suy luận (Infi-MMR). Với captioning: **không thấy** | **Mở**, nhưng là đóng góp phụ |

Đề xuất cho mô hình KG-captioning tiếng Việt (chi tiết ở §3):
- **O1 (chính): GEPA**, Graph-Edit Phrase Alignment. Negative được sinh bằng *chỉnh sửa có kiểu* trên đồ thị mệnh đề đã kiểm chứng của VSPS: thay nút bằng thực thể verifier đã REJECTED, đổi thuộc tính, đảo chủ thể/khách thể, khẳng định giới tính khi nút là UNCERTAIN. Loss chỉ tính trên **cụm bị sửa**, kèm KL theo token với mô hình tham chiếu. Thiết kế này nhắm thẳng vào thất bại DPO cấp chuỗi đã ghi trong repo.
- **O2 (phụ, rẻ): GA-SFT + curriculum**, SFT đa nhiệm có đích phụ là đồ thị tuyến tính tiếng Việt. Thứ tự mẫu đi từ đồ thị ít nút/cạnh đến nhiều. Suy luận vẫn chỉ sinh caption.
- **Không đề xuất** GRPO-graph-reward làm đóng góp. Chỉ chạy nó như **baseline bắt buộc** (17_novelty_redteam (a)).

---

## 1. Bằng chứng theo họ (chỉ 2025-2026, đã xác minh)

### (1) Graph-text contrastive alignment
| Bài | Venue (theo arXiv) | Nội dung liên quan |
|---|---|---|
| CLIC, Advancing Compositional Awareness in CLIP with Efficient Fine-Tuning (Peleg, Singh, Hein), arXiv 2505.24424 | NeurIPS 2025 | Fine-tune CLIP bằng cách ghép nhiều ảnh và caption. Cải thiện compositionality ở cả mức lexical lẫn semantic (SugarCrepe++) mà không làm giảm retrieval. **Không dùng đồ thị**, và đây là encoder chứ không phải generator |
| SPAN, Learning Similarity between Scene Graphs and Images with Transformers (Cong et al.), arXiv 2304.00590 | arXiv 2023. Web search cho biết có bản TPAMI 2025, chưa mở | Contrastive giữa scene graph và ảnh. Captioning chỉ là ứng dụng hạ nguồn |

Background (một dòng): Structure-CLIP (2023) và các nghiên cứu hard-negative cho CLIP năm 2023-2024 là nền của nhánh này.

Nhận định: trong 2025-2026, contrastive graph-text vẫn chỉ sống ở **encoder hoặc retrieval**. Với LVLM sinh caption, contrastive loss trên embedding chỉ là loss phụ, và phải can thiệp vào ViT hoặc projector. Trên một RTX 3090 với QLoRA, thường chỉ LM được fine-tune (repo `train_stage2.py` cũng chỉ áp LoRA lên LM). **Không nên chọn.**

### (2) Loss nhận biết cấu trúc
| Bài | Venue | Nội dung |
|---|---|---|
| HALVA / DPA, Mitigating Object Hallucination in MLLMs via Data-augmented Phrase-level Alignment (Sarkar et al.), arXiv 2405.18654 | ICLR 2025 | Sinh cặp đúng/ảo giác bằng cách **thay cụm** trong câu trả lời đúng mà giữ nguyên cấu trúc. Loss đẩy log-prob của cụm ảo giác xuống so với cụm đúng, kèm **KL theo token** với mô hình tham chiếu đóng băng để giữ năng lực chung. Abstract báo F1 tăng tới 13,4% trên hallucination VQA và tỷ lệ ảo giác giảm tới 4,2% trên mô tả ảnh. **Đây là khung loss gần O1 nhất** |
| Reducing Object Hallucination in LVLMs via Emphasizing Image-negative Tokens (Shen et al.), arXiv 2605.21300 | arXiv 2026, chưa có venue | Chia token theo mức phụ thuộc vào ảnh (positive, invariant, negative) và đổi trọng số loss SFT theo nhóm. Không dùng đồ thị |

Nhận định: loss theo cụm hoặc token **đã được chứng minh** là giảm ảo giác vật thể. Còn **mở**: lấy cụm và trọng số **từ nút đồ thị đã kiểm chứng** (có kiểu và có 3 trạng thái) thay cho thay cụm bằng LLM hay heuristic phụ thuộc ảnh.

### (3) SFT có điều kiện là đồ thị
| Bài | Venue | Nội dung |
|---|---|---|
| Scene Graph Thinking (SaGe; Yang et al.), arXiv 2607.05716 (full text đã mở) | ICML 2026 | Data engine biến kho ảnh-văn bản thành scene graph. SFT trên 120K vết suy luận đi qua các nút có thẻ `<entity>/<bbox>/<depth>`, sau đó GRPO với reward "node-grounded" và "node-relevance" do MLLM/LLM chấm. Không có reward cạnh. Ablation: GRPO thường cho V* 85,9, đầy đủ cho 89,0, bỏ node-relevance còn 85,0. **Không có benchmark captioning hay ảo giác.** Qwen2.5-VL-3B/7B |
| Relation-R1 (Li et al.), arXiv 2504.14642 | AAAI 2026 | SFT có CoT nhận thức (đối tượng, grounding, quan hệ), sau đó GRPO cho hiểu quan hệ nhị phân và N-ngôi |
| SGG-R³ (Feng et al.), arXiv 2603.07961 | arXiv 2026 | CoT-SFT có tăng cường quan hệ, sau đó RL (GSPO) cho SGG end-to-end, nhắm vào recall thấp do đuôi dài |
| SceneGraphVLM (Makarov et al.), arXiv 2605.13667 | arXiv 2026 | SFT trên đồ thị tuần tự hóa (định dạng TOON tiết kiệm token), sau đó RL với reward cân bằng coverage/precision quan hệ và phạt object/quan hệ không có căn cứ. Dùng VLM nhỏ |
| R1-SGG, Compile Scene Graphs with RL (Chen et al.), arXiv 2504.13617 | arXiv 2025 | SFT trên SGG, sau đó GRPO với reward quy tắc theo đồ thị |

Nhận định: "đồ thị trong đích SFT" **đã chứng minh** cho suy luận và SGG. Với **caption chi tiết** thì chưa thấy bài nào đo xem đích phụ là đồ thị có làm caption ít ảo giác hơn hay recall cao hơn không. Đây là khoảng trống nhỏ nhưng có thật, và rẻ để kiểm tra (O2).

### (4) Cặp preference sinh từ đồ thị
| Bài | Venue | Nội dung |
|---|---|---|
| **SceneAlign** (C. Wang et al.), arXiv 2601.05600 (full text đã mở) | ACL 2026 (`2026.acl-long.779`, theo trang ACL Anthology thấy qua search) | Chọn các nút scene graph quan trọng cho suy luận rồi nhiễu bằng **4 chiến lược**: *Swap* (đảo chủ thể/khách thể của quan hệ), *Replace* (thay bằng phần tử từ pool phần tử không then chốt), *Shorten* (bỏ phần tử then chốt), *Overthink* (thêm phần tử thừa). DPO chuẩn, β=0,1, lr 5e-6, 1 epoch, 2×A100, dữ liệu A-OKVQA với 3 negative/mẫu. HallusionBench: Qwen2.5-VL-3B từ 34,28 lên 58,25. **Không có captioning, CHAIR hay AMBER** |
| Importance Sampling for Multi-Negative Multimodal DPO (X. Li, C. Wang et al.), arXiv 2509.25717 | arXiv 2025 | Cùng nhóm với SceneAlign. DPO nhiều negative |
| SENTINEL (Peng et al.), arXiv 2507.12455 | ICCV 2025 (CVF open access) | Cặp preference trong miền: kiểm tra object bằng 2 detector open-vocab rồi C-DPO ở câu đầu tiên có ảo giác. Không dùng đồ thị |
| HII-DPO (Yang et al.), arXiv 2602.10425 | arXiv 2026 | Ảnh phản thực (xóa object) dựa trên prior đồng xuất hiện theo cảnh, dùng làm cặp preference |
| Low-hallucination Synthetic Captions (Zhang et al.), arXiv 2504.13123 | arXiv 2025 | DPO cho caption tổng hợp |
| HDPO (Fu et al.), arXiv 2411.10436 | arXiv 2024, background | DPO nhắm từng nguyên nhân ảo giác, gồm cả captioning |

Truy vấn arXiv `abs:"scene graph" AND abs:DPO AND abs:hallucination` (chạy hôm nay) **trả 0 kết quả**. Truy vấn `abs:"scene graph" AND abs:"preference optimization"` cũng ra 0.

Nhận định: dùng đồ thị để sinh negative là **đã chứng minh cho suy luận** (SceneAlign) và **chưa thấy cho caption chi tiết**. Khác biệt có thể bảo vệ được: negative của SceneAlign lấy từ pool của *chính đồ thị đúng*, nên đó là lỗi nhân tạo. Đồ thị VSPS có sẵn các **nút REJECTED**, tức là thứ generator *thật sự* đã ảo giác trên đúng ảnh đó và verifier đã bác. Như vậy negative gần on-policy. Bài "On-policy data hold the key" (CVPR 2025, chỉ thấy qua search, xem "Chưa xác minh") lập luận rằng chính tính on-policy quyết định DPO có giảm được ảo giác hay không.

### (5) RL với reward khớp đồ thị (đông đúc)
| Bài | Venue | Ghi chú |
|---|---|---|
| SC-Captioner, arXiv 2508.06125 | ICCV 2025 | Reward là hiệu tập object/attribute/relation (parse kiểu FACTUAL) giữa caption ban đầu và caption tự sửa, so với tham chiếu. Vượt SFT+DPO |
| FoCUS, arXiv 2609.00709 | EMNLP 2026 Main | GRPO với điểm thành phần căn theo scene graph, có trọng số âm |
| SAGA, arXiv 2609.07107 | EMNLP 2026 | Reward khớp đồ thị dị thể (bộ ba + cấu trúc thời gian) cho micro-drama, trên Qwen3-VL-8B |
| Reinforcing Consistency in Video MLLMs with Structured Rewards, arXiv 2604.01460 | COLM 2026 | Kiểm toán caption theo claim phân cấp, reward có cấu trúc |
| CheXPO-v2, arXiv 2512.17213 | arXiv 2025 | KG Consistency Reward qua khớp triple (Disease, Relation, Anatomy), GRPO |
| R1-SGG, SceneGraphVLM, SaGe | xem (3) | Reward đồ thị cho SGG/suy luận |

Cộng thêm phía claim: BalCapRL, ClaimDiff-RL, CapRL++ (đã có trong 07). **Kết luận: reward khớp đồ thị cho captioning là đã chứng minh.** Một bài mới chỉ có thể đóng góp ở *nguồn* đồ thị (đã kiểm chứng, tiếng Việt, không cần tham chiếu), không phải ở reward.

### (6) Curriculum theo độ phức tạp đồ thị
| Bài | Venue | Ghi chú |
|---|---|---|
| CompGen, Synthetic Curriculum Reinforces Compositional T2I Generation, arXiv 2511.18378 | arXiv 2025 | Độ khó đo bằng độ phức tạp của scene graph. Lấy mẫu đồ thị bằng MCMC thích nghi, RL cho T2I |
| Generate Any Scene, arXiv 2412.08221 | ICLR 2026 | Liệt kê scene graph với độ phức tạp khác nhau, phục vụ T2I/T2V và reward |
| Infi-MMR, arXiv 2505.23091 | arXiv 2025 | Curriculum 3 pha cho RL suy luận đa phương thức (không theo đồ thị) |

Nhận định: **mở cho captioning**, nhưng chỉ đáng là một ablation hoặc thành phần phụ. Curriculum hiếm khi là đóng góp đứng một mình ở venue Q1/Q2.

---

## 2. Ràng buộc từ chính repo VSPS (ảnh hưởng đến thiết kế)

- `README.md` (mục "Optional: preference-tuning exploration"): DPO cấp chuỗi trên 12.806 cặp ba bậc A>B>C (`scripts/build_dpo_data.py`, `train_stage2.py --stage dpo`) là **kết quả âm có kiểm soát**: "on the 4-bit backbone, every tested dose degraded CIDEr and leaked non-Vietnamese tokens". Hai nguyên nhân hợp lý: (i) cặp B>C khác nhau về độ dài và nội dung, nên DPO học "ngắn hơn là an toàn" (docstring của `build_dpo_data.py` đã cảnh báo điều này); (ii) không có ràng buộc ở cấp token nên phân phối trôi khỏi tiếng Việt. → O1 phải **giữ nguyên độ dài và nội dung ngoài cụm sửa**, và phải có **KL theo token** (đúng như thiết kế của HALVA).
- `train_stage2.py` đã có vòng lặp DPO tự viết (`sequence_logprob`, `run_dpo`, tham chiếu bằng `disable_adapter()` hoặc adapter `ref_sft`). O1 chỉ cần thêm **mặt nạ cụm** và **số hạng KL**, khoảng 30-40 dòng. Không cần thư viện mới.
- Đồ thị đã có sẵn: mệnh đề có kiểu (entity/attribute/action/count/relation) với verdict SUPPORTED/UNCERTAIN/REJECTED trên khoảng 3.700 ảnh train KTVIC. Có sẵn `relation_audit.py`, `relation_backoff.py`, `person_backoff.py`. UIT-OpenViIC/ViTextCaps **chưa có** đồ thị. Muốn có phải chạy Stage 1 (khoảng 88 GPU-h cho KTVIC theo 08, hoặc ít hơn nhiều nếu áp verifier đọc logit một lượt, xem 00 §4 mục 1).

---

## 3. Hai hàm mục tiêu đề xuất

Ký hiệu: G = (V, E) là đồ thị đã kiểm chứng của ảnh I. Mỗi nút hoặc cạnh mang kiểu t ∈ {obj, attr, rel, count, gender} và trạng thái s ∈ {S, U, R}. y⁺ là caption đích của VSPS (render từ phần S, trung tính hóa phần U). Backbone chính là Qwen2.5-VL-7B, NF4 QLoRA (r=16), khởi từ adapter VSPS-SFT. Bản rẻ để quét lưới dùng Qwen2.5-VL-3B hoặc Vintern-3B.

### O1. GEPA: Graph-Edit Phrase Alignment

**Dựng cặp (CPU, 0 GPU).** Với mỗi ảnh, áp một phép sửa có kiểu e lên G để được G⁻, rồi render y⁻ bằng **cùng renderer, cùng template, cùng thứ tự**. Kết quả là y⁺ và y⁻ chỉ khác nhau ở cụm σ(e):

| Phép sửa | Cách làm trên đồ thị VSPS | Lỗi mô phỏng |
|---|---|---|
| E1 node-swap-R | thay một nút obj loại S bằng một nút obj loại **R của cùng ảnh** (verifier đã bác) | ảo giác vật thể *thật* của generator |
| E2 attr-swap | thay thuộc tính loại S bằng thuộc tính R. Nếu không có, lấy từ cùng nhóm (màu sang màu) | ảo giác thuộc tính |
| E3 rel-flip | đảo chủ thể/khách thể của cạnh rel loại S (như *Swap* của SceneAlign), hoặc thay vị từ bằng vị từ R | ảo giác quan hệ |
| E4 gender-assert | nút người loại U được trung tính hóa ("người") thì đổi thành dạng có giới ("người phụ nữ") | khẳng định quá mức. Đây là phép riêng của VSPS và tiếng Việt |
| E5 count | đổi số đếm loại S thành số đếm R | ảo giác số lượng |

Ràng buộc tiếng Việt: khi thay nút phải đổi cả **loại từ** đi kèm (con/chiếc/cái), lấy từ lexicon đối tượng tiếng Việt đã có. Nếu không, y⁻ sai ngữ pháp và trở thành negative quá dễ.

**Loss** (biến thể DPA của HALVA, tính trên mặt nạ cụm m_σ):

L = L_SFT(y⁺) + α · [ −log σ( β · ( Δ_θ(σ⁺) − Δ_θ(σ⁻) ) ) ] + γ · Σ_{token ∉ σ} KL( p_ref ‖ p_θ )

Trong đó Δ_θ(σ) = Σ_{tok∈σ} [log p_θ − log p_ref], và p_ref là adapter VSPS-SFT đóng băng. Vì phần ngoài σ giống hệt nhau giữa y⁺ và y⁻, tín hiệu preference chỉ rơi vào cụm bị sửa. Không có thiên lệch độ dài. Số hạng KL giữ phân phối tiếng Việt ở phần còn lại.

**Hiệu ứng dự kiến** (ước tính, chưa đo):
- CHAIR-vi_i và tỷ lệ ảo giác quan hệ (đo bằng probe có/không trên cạnh) giảm rõ hơn SFT. E1 nhắm vào đúng đuôi lỗi mà verifier đã thấy.
- Recall vật thể **không giảm**, vì y⁺ không bị rút ngắn. Đây là điểm khác cốt lõi so với DPO A>B>C đã thất bại.
- Tỷ lệ token không phải tiếng Việt ≤ mức của SFT (nhờ γ).
- Rủi ro: E1 với nút R có thể dạy mô hình "không bao giờ nói X" cho những X mà verifier bác *sai*. Precision SUPPORTED chỉ 63,1%, nên độ chính xác của REJECTED cũng cần đo trên 244 mục audit trước. Nếu precision của R thấp, dùng E1 chỉ với nút R có ≥4/5 phiếu.

**Ablation (mỗi hàng 3 seed, cùng số bước):**
| # | Cấu hình | Câu hỏi |
|---|---|---|
| A0 | VSPS-SFT (adapter hiện có) | mốc |
| A1 | + DPO chuỗi A>B>C (lặp lại kết quả âm trong repo) | thất bại DPO có tái lập không |
| A2 | + GEPA, negative ngẫu nhiên từ vựng (kiểu HALVA/SceneAlign *Replace*) | nguồn đồ thị có quan trọng không |
| A3 | + GEPA, negative từ nút **R đã kiểm chứng** (E1-E5) | phương pháp đề xuất |
| A4 | A3 bỏ từng E_k (leave-one-out) | phép sửa nào có tác dụng |
| A5 | A3 với γ ∈ {0; 0,1; 1} | KL có chặn được rò rỉ ngôn ngữ không |
| A6 | A3 với loss DPO toàn chuỗi thay cho loss theo cụm (cùng cặp) | cấp cụm có cần không |
| B | GRPO với reward khớp đồ thị (kiểu SC-Captioner/FoCUS, reward tra verdict offline, G=4) | baseline bắt buộc theo 17 (a) |

Metric: CHAIR-vi (s/i), object P/R/F1 trên 300 ảnh gold, graph-P/R theo loại (idea 1 của file 11), probe ảo giác quan hệ, tỷ lệ khẳng định giới tính trên nút U, CIDEr, độ dài, tỷ lệ token không phải tiếng Việt. Kiểm định bootstrap/Wilcoxon như bài hiện tại. Thêm một lần chạy đối chứng với **ảnh xám** cho A3 (theo 2610.01908 trong 07) để loại giải thích bằng prior ngôn ngữ.

**Chi phí GPU (1× RTX 3090, ước tính; cần đo bằng `nvidia-smi` log):**
- Dựng cặp: CPU, dưới 1 giờ.
- Mỗi bước GEPA cần 2 forward/backward (y⁺, y⁻, chung ảnh, chạy batch 2) và 2 forward không grad cho tham chiếu (`disable_adapter`, nên không tốn thêm VRAM cho bản sao mô hình). Khoảng 3× chi phí một mẫu SFT.
- 7B NF4, khoảng 4.000 cặp × 1 epoch: khoảng **4-6 GPU-h/run**, VRAM khoảng 18-22 GB khi bật gradient checkpointing, batch 2, accumulation 8. Lưới A2-A6 trên 3B (khoảng 1,5-2 GPU-h/run × khoảng 10 run ≈ 20 GPU-h), rồi A0/A1/A3/B trên 7B × 3 seed (≈ 4 × 3 × 5 ≈ 60 GPU-h). B tốn khoảng 6-8 GPU-h/run (ước tính của 07). **Tổng khoảng 80-100 GPU-h, tức 4-5 ngày máy.**

**Overlap và novelty.** HALVA (loss cụm + KL), SceneAlign (nhiễu đồ thị → DPO), SENTINEL (cặp trong miền có kiểm chứng): overlap **MEDIUM**. Phần mới, cần nói đúng mức: (i) negative là *ảo giác thật đã bị verifier bác trên cùng ảnh*, không phải nhiễu nhân tạo; (ii) phép sửa E4 dựa trên trạng thái UNCERTAIN (khẳng định quá mức), không có trong HALVA hay SceneAlign; (iii) áp cho caption chi tiết tiếng Việt, với ràng buộc loại từ; (iv) chẩn đoán thất bại DPO chuỗi bằng ablation A1/A6. Không được tuyên bố "loss mới". Đó là DPA của HALVA.

### O2. GA-SFT + curriculum theo độ phức tạp đồ thị

**Nội dung.** SFT đa nhiệm trên cùng ảnh:
- Nhiệm vụ chính (70%): ảnh → caption y⁺ (như VSPS).
- Nhiệm vụ phụ (30%): ảnh → **đồ thị tuyến tính tiếng Việt** gồm các nút S và U, U có đánh dấu. Ví dụ `(người; mặc; áo dài đỏ) | (xe máy; [?]màu xanh)`. Dùng định dạng gọn kiểu TOON/triple như SceneGraphVLM để tiết kiệm token.
- Lúc suy luận chỉ chạy nhiệm vụ chính, nên **không tốn thêm chi phí suy luận**. Biến thể "graph-then-caption" (kiểu CCoT/SaGe) được báo riêng, vì nó làm mất tính một lượt và gấp đôi độ dài đầu ra.
- Curriculum: độ khó c(G) = |V_S| + 2·|E_rel,S| + |V_U|. Chia 3 bucket theo tertile. Epoch 1 đi từ dễ đến khó, epoch 2 xáo trộn đều.

**Hiệu ứng dự kiến** (ước tính): recall quan hệ và recall vật thể trên ảnh đông tăng nhẹ (+1-3 điểm), vì đích phụ buộc mô hình liệt kê đủ nút. CHAIR gần như không đổi. Curriculum chỉ kỳ vọng tác dụng nhỏ, và có thể bằng 0. Nếu bằng 0 vẫn báo như một kết quả âm.

**Ablation (3 seed):** C0 VSPS-SFT; C1 + đích phụ đồ thị; C2 + curriculum (không có đích phụ); C3 C1+C2; C4 graph-then-caption (2 lượt); C5 đích phụ chỉ có nút S (bỏ U) để đo xem đánh dấu không chắc có giúp không; C6 curriculum ngược (khó → dễ) làm đối chứng.

**Chi phí GPU:** bằng SFT hiện tại cộng khoảng 30% token. Khoảng **3-5 GPU-h/run** cho 7B (ước tính, SFT gốc chưa có số đo wall-clock trong repo). 7 cấu hình × 3 seed trên 3B (≈ 30 GPU-h) và 3 cấu hình chính trên 7B × 3 seed (≈ 35-45 GPU-h).

**Overlap và novelty:** SaGe, Relation-R1 và SGG-R³ đều dùng đồ thị trong đích SFT, nhưng cho suy luận và SGG. Overlap **LOW-MEDIUM**. Đây là đóng góp phụ, nên gộp với O1 hoặc với metric graph-P/R của file 11, không đứng riêng.

### Thứ tự khuyến nghị
1. Đo precision của nút REJECTED trên 244 mục audit (0 GPU). Kết quả này quyết định E1 có dùng được không.
2. O1 bản 3B (A2/A3/A6), khoảng 6 GPU-h. Nếu A3 không thắng A2 trên CHAIR-vi_i thì luận điểm "nguồn đồ thị kiểm chứng" sụp đổ, nên dừng sớm.
3. O2 C1, chạy song song khi máy rảnh.
4. Chỉ sau đó mới chạy 7B × 3 seed và baseline GRPO B.

---

## 4. Chưa xác minh / hạn chế
- Venue ACL 2026 của SceneAlign lấy từ trang ACL Anthology thấy qua web search (`2026.acl-long.779`). arXiv comment chỉ ghi "Preprint". Chưa mở trang Anthology.
- Bản TPAMI 2025 của SPAN chỉ thấy qua snippet tìm kiếm.
- "Mitigating Hallucinations in LVLMs via DPO: On-Policy Data Hold the Key" (CVPR 2025, Yang et al.; arXiv 2501.09695 theo kết quả search) chưa được tra bằng arXiv API trong phiên này.
- Kamath et al. (ECCV 2024, phê phán hard-negative fine-tuning làm giảm khả năng xử lý hard positive) chỉ thấy qua snippet. Đây là bài trước 2025, chỉ dùng làm cảnh báo thiết kế: nên thêm hard positive (paraphrase của y⁺) vào kiểm tra.
- "VCap" (reward caption kết hợp tham chiếu và kiểm chứng thị giác) chỉ thấy tên trên trang tổng hợp, chưa xác định được bài.
- EMNLP 2025 "Ultra-Detailed Image Caption Generation" (DPO + critic viết lại câu) chỉ thấy qua trang preview của ACL Anthology, chưa mở.
- Mọi số GPU-h và mọi hiệu ứng ở §3 là **ước tính**, chưa đo. Repo chưa ghi wall-clock của SFT. Nên ghi lại khi chạy A0.
- OpenAlex và Semantic Scholar bị rate-limit, nên chưa có số đếm theo năm cho từng họ. Mức "nóng/đông" dựa trên số bài đã xác minh, không dựa trên thống kê.

## 5. Truy vấn theo dõi
1. arXiv: `abs:"scene graph" AND (abs:DPO OR abs:"preference optimization") AND abs:caption*`
2. arXiv: `abs:"phrase-level" AND abs:hallucination AND abs:caption*`. Theo dõi trích dẫn của HALVA (2405.18654) và SceneAlign (2601.05600) trên Semantic Scholar.
3. arXiv: `abs:curriculum AND abs:"scene graph" AND (abs:caption* OR abs:"vision-language")`
4. arXiv: `abs:"scene graph" AND abs:GRPO AND abs:caption*` (FoCUS, SC-Captioner và các bài kế tiếp)
